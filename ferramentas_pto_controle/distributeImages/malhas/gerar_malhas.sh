#!/usr/bin/env bash
#
# Gera assets/municipios.gpkg e assets/estados.gpkg a partir da malha municipal
# do IBGE. Rode de novo quando o IBGE publicar malha nova.
#
# Uso:
#   ./gerar_malhas.sh MALHA_IBGE.gpkg PASTA_DE_SAIDA
#
# Precisa do QGIS 4 no PATH (qgis_process e ogr2ogr). No Windows, o executavel se
# chama qgis_process-qgis.bat; exporte QGIS_PROCESS com o caminho dele.
#
# POR QUE NAO E UMA SIMPLIFICACAO SIMPLES
#
# 1. A simplificacao e de COBERTURA (GEOS CoverageSimplify, algoritmo
#    native:coveragesimplify). A aresta compartilhada entre dois municipios e
#    simplificada UMA vez, entao a adjacencia sobrevive. Simplificar feicao a
#    feicao (native:simplifygeometries) abre fenda e sobreposicao entre vizinhos.
#
# 2. A tolerancia VARIA por municipio. O quadro do P08 enquadra uma feicao por
#    vez, entao o pixel no terreno muda de 3,7 m a 1097 m conforme o municipio.
#    Uma tolerancia unica ou desperdica vertice no municipio grande ou estraga o
#    pequeno.
#
# 3. Variar a tolerancia sem quebrar a adjacencia se faz com PRESERVE_BOUNDARY.
#    Cada passada roda sobre a subcobertura de uma faixa e das mais grossas, com a
#    borda EXTERNA daquela subcobertura presa. Essa borda e exatamente o conjunto
#    de arestas que a subcobertura divide com as faixas mais finas, ja fixadas na
#    passada anterior. Por isso as passadas vao da mais fina a mais grossa.
#
# Numeros medidos e criterio de escolha em LEIA-ME.md.
set -eu

FONTE="${1:?informe a malha municipal do IBGE (.gpkg)}"
SAIDA="${2:?informe a pasta de saida}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

QGIS_PROCESS="${QGIS_PROCESS:-qgis_process}"
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"

# faixa:tolerancia em grau. A faixa 1 roda na cobertura inteira, com a borda solta.
PASSOS="1:0.0002 2:0.0005 3:0.001 4:0.002 5:0.004 6:0.01"
TOLERANCIA_UF=0.005
CAMPOS_MUN="CD_MUN, NM_MUN, SIGLA_UF"

simplificar () { # entrada saida tolerancia preservar_borda
  "$QGIS_PROCESS" run native:coveragesimplify -- \
    INPUT="$1" TOLERANCE="$3" PRESERVE_BOUNDARY="$4" OUTPUT="$2" >/dev/null
}

echo "== municipios: atributos =="
ogr2ogr -f GPKG "$TMP/bruto.gpkg" "$FONTE" -nln bruto \
  -select CD_MUN,NM_MUN,SIGLA_UF -nlt MULTIPOLYGON

anterior=''
for passo in $PASSOS; do
  faixa="${passo%%:*}"; tolerancia="${passo##*:}"
  if [ -z "$anterior" ]; then
    echo "== municipios: faixa $faixa, cobertura inteira em $tolerancia grau =="
    simplificar "$TMP/bruto.gpkg" "$TMP/fx_$faixa.gpkg" "$tolerancia" 0
    python "$AQUI/classificar_faixas.py" "$TMP/fx_$faixa.gpkg"
    primeira="$faixa"
  else
    echo "== municipios: faixa $faixa em $tolerancia grau, borda presa =="
    ogr2ogr -f GPKG "$TMP/entrada_$faixa.gpkg" "$TMP/fx_$anterior.gpkg" \
      -where "faixa >= $faixa" -nln sub
    simplificar "$TMP/entrada_$faixa.gpkg" "$TMP/fx_$faixa.gpkg" "$tolerancia" 1
  fi
  anterior="$faixa"
done
ultima="$anterior"

echo "== municipios: juntando as faixas =="
mkdir -p "$SAIDA"
rm -f "$SAIDA/municipios.gpkg"
ogr2ogr -f GPKG "$SAIDA/municipios.gpkg" "$TMP/fx_$primeira.gpkg" \
  -nln municipios -nlt MULTIPOLYGON -a_srs EPSG:4674 -dialect SQLITE \
  -sql "SELECT geom, $CAMPOS_MUN FROM fx_$primeira WHERE faixa = $primeira"

for passo in $PASSOS; do
  faixa="${passo%%:*}"
  [ "$faixa" = "$primeira" ] && continue
  condicao="faixa = $faixa"
  [ "$faixa" = "$ultima" ] && condicao="faixa >= $faixa"
  ogr2ogr -f GPKG -update -append "$SAIDA/municipios.gpkg" "$TMP/fx_$faixa.gpkg" \
    -nln municipios -nlt MULTIPOLYGON -dialect SQLITE \
    -sql "SELECT geom, $CAMPOS_MUN FROM fx_$faixa WHERE $condicao"
done

echo "== estados: dissolve dos municipios ja simplificados =="
# Sai da malha municipal simplificada para as duas camadas casarem no limite
# estadual. A aresta interna some porque a cobertura tem aresta compartilhada
# identica depois do CoverageSimplify.
"$QGIS_PROCESS" run native:dissolve -- \
  INPUT="$SAIDA/municipios.gpkg" FIELD=SIGLA_UF SEPARATE_DISJOINT=0 \
  OUTPUT="$TMP/uf1.gpkg" >/dev/null
simplificar "$TMP/uf1.gpkg" "$TMP/uf2.gpkg" "$TOLERANCIA_UF" 0

echo "== estados: nome e codigo da UF =="
# A malha municipal do IBGE traz SIGLA_UF, mas o qml_estado.qml rotula por NM_UF.
rm -f "$SAIDA/estados.gpkg"
ogr2ogr -f GPKG "$SAIDA/estados.gpkg" "$TMP/uf2.gpkg" -nln estados \
  -nlt MULTIPOLYGON -a_srs EPSG:4674 -dialect SQLITE -sql "
    SELECT u.geom,
           CASE SIGLA_UF
             WHEN 'RO' THEN '11' WHEN 'AC' THEN '12' WHEN 'AM' THEN '13'
             WHEN 'RR' THEN '14' WHEN 'PA' THEN '15' WHEN 'AP' THEN '16'
             WHEN 'TO' THEN '17' WHEN 'MA' THEN '21' WHEN 'PI' THEN '22'
             WHEN 'CE' THEN '23' WHEN 'RN' THEN '24' WHEN 'PB' THEN '25'
             WHEN 'PE' THEN '26' WHEN 'AL' THEN '27' WHEN 'SE' THEN '28'
             WHEN 'BA' THEN '29' WHEN 'MG' THEN '31' WHEN 'ES' THEN '32'
             WHEN 'RJ' THEN '33' WHEN 'SP' THEN '35' WHEN 'PR' THEN '41'
             WHEN 'SC' THEN '42' WHEN 'RS' THEN '43' WHEN 'MS' THEN '50'
             WHEN 'MT' THEN '51' WHEN 'GO' THEN '52' WHEN 'DF' THEN '53'
           END AS CD_UF,
           SIGLA_UF,
           CASE SIGLA_UF
             WHEN 'RO' THEN 'Rondônia' WHEN 'AC' THEN 'Acre'
             WHEN 'AM' THEN 'Amazonas' WHEN 'RR' THEN 'Roraima'
             WHEN 'PA' THEN 'Pará' WHEN 'AP' THEN 'Amapá'
             WHEN 'TO' THEN 'Tocantins' WHEN 'MA' THEN 'Maranhão'
             WHEN 'PI' THEN 'Piauí' WHEN 'CE' THEN 'Ceará'
             WHEN 'RN' THEN 'Rio Grande do Norte' WHEN 'PB' THEN 'Paraíba'
             WHEN 'PE' THEN 'Pernambuco' WHEN 'AL' THEN 'Alagoas'
             WHEN 'SE' THEN 'Sergipe' WHEN 'BA' THEN 'Bahia'
             WHEN 'MG' THEN 'Minas Gerais' WHEN 'ES' THEN 'Espírito Santo'
             WHEN 'RJ' THEN 'Rio de Janeiro' WHEN 'SP' THEN 'São Paulo'
             WHEN 'PR' THEN 'Paraná' WHEN 'SC' THEN 'Santa Catarina'
             WHEN 'RS' THEN 'Rio Grande do Sul' WHEN 'MS' THEN 'Mato Grosso do Sul'
             WHEN 'MT' THEN 'Mato Grosso' WHEN 'GO' THEN 'Goiás'
             WHEN 'DF' THEN 'Distrito Federal'
           END AS NM_UF,
           CASE SUBSTR(CD_MUN, 1, 1)
             WHEN '1' THEN 'Norte' WHEN '2' THEN 'Nordeste'
             WHEN '3' THEN 'Sudeste' WHEN '4' THEN 'Sul' WHEN '5' THEN 'Centro-Oeste'
           END AS NM_REGIAO
    FROM uf2 u ORDER BY CD_UF"

echo "== pronto =="
ls -la "$SAIDA/municipios.gpkg" "$SAIDA/estados.gpkg"
