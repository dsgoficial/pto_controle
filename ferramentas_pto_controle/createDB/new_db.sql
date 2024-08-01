CREATE EXTENSION postgis;
CREATE SCHEMA dominios;

CREATE TABLE dominios.tipo_situacao(
	code SMALLINT NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);
ALTER TABLE dominios.tipo_situacao OWNER TO postgres;

INSERT INTO dominios.tipo_situacao (code, nome) VALUES (1, 'Não medido');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (2, 'Aguardando revisão');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (3, 'Aprovado');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (4, 'Reprovado');
INSERT INTO dominios.tipo_situacao (code, nome) VALUES (9999, 'A SER PREENCHIDO');

CREATE TABLE dominios.classificacao_ponto(
	code SMALLINT NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL
);
ALTER TABLE dominios.classificacao_ponto OWNER TO postgres;

INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (0, 'Desconhecido');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (1, 'Canto de edificação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (2, 'Entroncamento de estrada');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (3, 'Cerca ou muro');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (4, 'Elemento identificável no solo');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (5, 'Elemento não identificável no solo');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (6, 'Topo de vegetação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (7, 'Abaixo de vegetação');
INSERT INTO dominios.classificacao_ponto (code, nome) VALUES (9999, 'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_ref (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ref_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_ref OWNER TO postgres;

INSERT INTO dominios.tipo_ref (code,code_name) VALUES (1,'Altimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (2,'Planimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (3,'Planialtimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (4,'Gravimétrico');
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.sistema_geodesico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT sistema_geodesico_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.sistema_geodesico OWNER TO postgres;

INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (1,'SAD-69');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (2,'SIRGAS2000');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (3,'WGS-84');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (4,'Córrego Alegre');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (5,'Astro Chuá');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (6,'SAD-69 (96)');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (99,'Outra referência');
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencial_altim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_altim_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencial_altim OWNER TO postgres;

INSERT INTO dominios.referencial_altim (code,code_name) VALUES (1,'Torres');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (2,'Imbituba');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (3,'Santana');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (99,'Outra referência');
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.metodo_posicionamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT metodo_posicionamento_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.metodo_posicionamento OWNER TO postgres;

INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (1,'Posicionamento por ponto preciso (PPP)');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (2,'Real Time Kinematic (RTK)');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (3,'Semi-cinemático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (4,'Relativo Estático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (5,'Relativo Cinemático');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (6,'Absoluto');
INSERT INTO dominios.metodo_posicionamento (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_medicao_altura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_medicao_altura_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_medicao_altura OWNER TO postgres;

INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (1,'Base de montagem');
INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (2,'Altura inclinada');
INSERT INTO dominios.tipo_medicao_altura (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencia_medicao_altura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencia_medicao_altura_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencia_medicao_altura OWNER TO postgres;

INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (1,'Nível do solo');
INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (2,'Nível do objeto');
INSERT INTO dominios.referencia_medicao_altura (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.orbita (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT orbita_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.orbita OWNER TO postgres;

INSERT INTO dominios.orbita (code,code_name) VALUES (1,'Ultra Rápida (predita)');
INSERT INTO dominios.orbita (code,code_name) VALUES (2,'Ultra Rápida (observada)');
INSERT INTO dominios.orbita (code,code_name) VALUES (3,'Rápida');
INSERT INTO dominios.orbita (code,code_name) VALUES (4,'Final');
INSERT INTO dominios.orbita (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.orbita (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_pto_ref_geod_topo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pto_ref_geod_topo_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_pto_ref_geod_topo OWNER TO postgres;

INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (0,'Desconhecido');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (1,'Vértice de triangulação - VT');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (2,'Referência de nível - RN');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (3,'Estação gravimétrica - EG');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (4,'Estação de poligonal - EP');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (5,'Ponto astronômico - PA');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (6,'Ponto barométrico - B');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (7,'Ponto trigonométrico - RV');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (8,'Ponto de satélite - SAT');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (99,'Outros');
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.tipo_marco_limite (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_marco_limite_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.tipo_marco_limite OWNER TO postgres;

INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (3,'Municipal');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (23,'Estadual');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (24,'Internacional secundário');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (25,'Internacional de referência');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (26,'Internacional principal');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (99,'Outros');
INSERT INTO dominios.tipo_marco_limite (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.rede_referencia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT rede_referencia_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.rede_referencia OWNER TO postgres;

INSERT INTO dominios.rede_referencia (code,code_name) VALUES (0,'Desconhecida');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (2,'Estadual');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (3,'Municipal');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (14,'Nacional');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (15,'Privada');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.referencial_grav (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_grav_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.referencial_grav OWNER TO postgres;

INSERT INTO dominios.referencial_grav (code,code_name) VALUES (0,'Desconhecido');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (1,'Potsdam 1930');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (2,'IGSN71');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (3,'Absoluto');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (4,'Local');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (5,'RGFB');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (97,'Não aplicável');
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.situacao_marco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_marco_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.situacao_marco OWNER TO postgres;

INSERT INTO dominios.situacao_marco (code,code_name) VALUES (0,'Desconhecida');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (1,'Bom');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (2,'Destruído');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (3,'Destruído sem chapa');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (4,'Destruí­do com chapa danificada');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (5,'Não encontrado');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (6,'Não visitado');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (7,'Não construí­do');
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (9999,'A SER PREENCHIDO');

CREATE TABLE dominios.insumo_medicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT insumo_medicao_pk PRIMARY KEY (code)
);
ALTER TABLE dominios.insumo_medicao OWNER TO postgres;

INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (1,'Fototriangulação');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (2,'Carta Topográfica');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (3,'Ortoimagem');
INSERT INTO dominios.insumo_medicao (code,code_name) VALUES (9999,'A SER PREENCHIDO');


CREATE SCHEMA bpc;

CREATE TABLE bpc.controle_medicao_a(
  id SERIAL NOT NULL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL,
  total_pontos_aprovados smallint NOT NULL DEFAULT 0,
  total_pontos_em_avaliacao smallint NOT NULL DEFAULT 0,
  total_pontos_previstos smallint NOT NULL DEFAULT 0,
  lote VARCHAR(255),
  geom geometry(Polygon,4674) NOT NULL
);
CREATE INDEX controle_medicao_a_geom ON bpc.controle_medicao_a USING gist (geom);
ALTER TABLE bpc.controle_medicao_a OWNER TO postgres;

CREATE TABLE bpc.ponto_controle_p(
  id SERIAL NOT NULL PRIMARY KEY,
  cod_ponto VARCHAR(255) UNIQUE NOT NULL,
  data_rastreio DATE NOT NULL,
  tipo_ref SMALLINT NOT NULL REFERENCES dominios.tipo_ref(code) DEFAULT 9999,
  latitude REAL, --graus decimais
  longitude REAL, --graus decimais
  norte FLOAT,
  leste FLOAT,
  altitude_ortometrica REAL, --metros
  altitude_geometrica REAL,  --metros
  sistema_geodesico SMALLINT NOT NULL REFERENCES  dominios.sistema_geodesico(code) DEFAULT 9999,
  outra_ref_plan VARCHAR(255),
  referencial_altim SMALLINT NOT NULL REFERENCES  dominios.referencial_altim(code) DEFAULT 9999,
  outro_ref_alt VARCHAR(255),
  fuso VARCHAR(255),
  meridiano_central VARCHAR(255),
  tipo_situacao SMALLINT NOT NULL REFERENCES dominios.tipo_situacao(code) DEFAULT 9999,
  reserva BOOLEAN NOT NULL DEFAULT FALSE,
  lote VARCHAR(255),
  latitude_planejada REAL, --graus decimais
  longitude_planejada REAL, --graus decimais
  medidor VARCHAR(255),
  inicio_rastreio TIMESTAMP WITH TIME ZONE,
  fim_rastreio TIMESTAMP WITH TIME ZONE,
  classificacao_ponto SMALLINT NOT NULL REFERENCES dominios.classificacao_ponto(code) DEFAULT 9999,
  observacao VARCHAR(255),
  metodo_posicionamento SMALLINT NOT NULL REFERENCES dominios.metodo_posicionamento(code) DEFAULT 9999,
  ponto_base VARCHAR(255),
  materializado BOOLEAN NOT NULL DEFAULT FALSE,
  altura_antena REAL, --metros
  tipo_medicao_altura SMALLINT NOT NULL REFERENCES dominios.tipo_medicao_altura(code) DEFAULT 9999,
  referencia_medicao_altura SMALLINT NOT NULL REFERENCES dominios.referencia_medicao_altura(code) DEFAULT 9999,
  altura_objeto REAL, --metros
  mascara_elevacao REAL, --graus decimais
  taxa_gravacao REAL, --segundos
  modelo_gps VARCHAR(255),
  modelo_antena VARCHAR(255),
  numero_serie_gps VARCHAR(255),
  numero_serie_antena VARCHAR(255),
  modelo_geoidal VARCHAR(255),
  precisao_horizontal_esperada REAL, --metros
  precisao_vertical_esperada REAL, --metros
  freq_processada VARCHAR(255),
  data_processamento DATE,
  orbita SMALLINT NOT NULL REFERENCES dominios.orbita(code) DEFAULT 9999,
  orgao_executante VARCHAR(255),
  projeto VARCHAR(255),
  engenheiro_responsavel VARCHAR(255),
  crea_engenheiro_responsavel VARCHAR(255),
  cpf_engenheiro_responsavel VARCHAR(255),
  geometria_aproximada BOOLEAN NOT NULL DEFAULT FALSE,
  tipo_pto_ref_geod_topo SMALLINT NOT NULL REFERENCES dominios.tipo_pto_ref_geod_topo(code) DEFAULT 9999,
  tipo_marco_limite SMALLINT NOT NULL REFERENCES dominios.tipo_marco_limite(code) DEFAULT 9999,
  rede_referencia SMALLINT NOT NULL REFERENCES dominios.rede_referencia(code) DEFAULT 9999,
  referencial_grav SMALLINT NOT NULL REFERENCES dominios.referencial_grav(code) DEFAULT 9999,
  situacao_marco SMALLINT NOT NULL REFERENCES dominios.situacao_marco(code) DEFAULT 9999,
  data_visita DATE,
  valor_gravidade REAL,
  possui_monografia BOOLEAN NOT NULL DEFAULT FALSE,
  numero_fotos SMALLINT,
  possui_croqui BOOLEAN NOT NULL DEFAULT FALSE,
  possui_arquivo_rastreio BOOLEAN NOT NULL DEFAULT FALSE,
  endereco_imagem_lateral_1 VARCHAR(255),
  endereco_imagem_lateral_2 VARCHAR(255),
  endereco_imagem_lateral_3 VARCHAR(255),
  endereco_imagem_lateral_4 VARCHAR(255),
  endereco_imagem_aerea VARCHAR(255),
  endereco_monografia VARCHAR(255),
  endereco_croqui VARCHAR(255),
  endereco_rinex VARCHAR(255),
  geom geometry(POINT,4674) NOT NULL
);
CREATE INDEX ponto_controle_p_geom ON bpc.ponto_controle_p USING gist (geom);
ALTER TABLE bpc.ponto_controle_p OWNER TO postgres;

CREATE TABLE bpc.ponto_controle_virtual_p(
  id SERIAL NOT NULL PRIMARY KEY,
  cod_ponto VARCHAR(255) UNIQUE NOT NULL,
  tipo_ref SMALLINT NOT NULL REFERENCES dominios.tipo_ref(code) DEFAULT 9999,
  latitude REAL, --graus decimais
  longitude REAL, --graus decimais
  altitude_ortometrica REAL, --metros
  sistema_geodesico SMALLINT NOT NULL REFERENCES  dominios.sistema_geodesico(code) DEFAULT 9999,
  outra_ref_plan VARCHAR(255),
  referencial_altim SMALLINT NOT NULL REFERENCES  dominios.referencial_altim(code) DEFAULT 9999,
  outro_ref_alt VARCHAR(255),
  lote VARCHAR(255),
  medidor VARCHAR(255),
  classificacao_ponto SMALLINT NOT NULL REFERENCES dominios.classificacao_ponto(code) DEFAULT 9999,
  observacao VARCHAR(255),
  insumo_medicao SMALLINT NOT NULL REFERENCES dominios.insumo_medicao(code) DEFAULT 9999,
  software VARCHAR(255),
  identificacao_insumo VARCHAR(255),
  acuracia_planimetrica_insumo REAL, --metros
  acuracia_altimetrica_insumo REAL, --metros
  descricao_insumo VARCHAR(255),
  orgao_executante VARCHAR(255),
  projeto VARCHAR(255),
  engenheiro_responsavel VARCHAR(255),
  crea_engenheiro_responsavel VARCHAR(255),
  geom geometry(POINTZ,4674) NOT NULL
);
CREATE INDEX ponto_controle_virtual_p_geom ON bpc.ponto_controle_virtual_p USING gist (geom);
ALTER TABLE bpc.ponto_controle_virtual_p OWNER TO postgres;

CREATE OR REPLACE FUNCTION atualizar_controle_medicao()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bpc.controle_medicao_a a
    SET total_pontos_aprovados = (
        SELECT COUNT(*)
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom) AND p.tipo_situacao = 3
    )
    WHERE EXISTS (
        SELECT 1
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom)
    );
    UPDATE bpc.controle_medicao_a a
    SET total_pontos_em_avaliacao = (
        SELECT COUNT(*)
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom) AND p.tipo_situacao = 2
    )
    WHERE EXISTS (
        SELECT 1
        FROM bpc.ponto_controle_p p
        WHERE ST_Intersects(a.geom, p.geom)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_insert_controle_medicao
AFTER INSERT ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();

CREATE TRIGGER trigger_update_controle_medicao
AFTER UPDATE ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();

CREATE TRIGGER trigger_delete_controle_medicao
AFTER DELETE ON bpc.ponto_controle_p
FOR EACH ROW
EXECUTE FUNCTION atualizar_controle_medicao();

CREATE TABLE public.layer_styles
(
  id serial NOT NULL,
  f_table_catalog character varying,
  f_table_schema character varying,
  f_table_name character varying,
  f_geometry_column character varying,
  stylename character varying(255),
  styleqml text,
  stylesld xml,
  useasdefault boolean,
  description text,
  owner character varying(30),
  ui xml,
  update_time timestamp without time zone DEFAULT now(),
  CONSTRAINT layer_styles_pkey PRIMARY KEY (id)
);

ALTER TABLE public.layer_styles OWNER TO postgres;

INSERT INTO public.layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, description, owner, update_time) VALUES (current_database(), 'bpc', 'controle_medicao_a', 'geom', 'controle_medicao_a', '<!DOCTYPE qgis PUBLIC ''http://mrcc.com/qgis.dtd'' ''SYSTEM''>
<qgis hasScaleBasedVisibilityFlag="0" symbologyReferenceScale="-1" readOnly="0" simplifyLocal="1" maxScale="0" simplifyDrawingTol="1" simplifyDrawingHints="0" simplifyAlgorithm="0" labelsEnabled="1" version="3.24.3-Tisler" minScale="100000000" styleCategories="AllStyleCategories" simplifyMaxScale="1">
 <flags>
  <Identifiable>1</Identifiable>
  <Removable>1</Removable>
  <Searchable>1</Searchable>
  <Private>0</Private>
 </flags>
 <temporal mode="0" fixedDuration="0" enabled="0" accumulate="0" endField="" endExpression="" startField="" durationUnit="min" limitMode="0" startExpression="" durationField="">
  <fixedRange>
   <start></start>
   <end></end>
  </fixedRange>
 </temporal>
 <renderer-v2 symbollevels="0" referencescale="-1" enableorderby="0" forceraster="0" type="RuleRenderer">
  <rules key="{6849b988-2a71-47ac-9949-f4a9e6dc7e10}">
   <rule symbol="0" key="{26669cea-8daf-4154-8f2f-c0cdf37da33a}" filter="if(total_pontos_aprovados > total_pontos_em_avaliacao, 1, 0)"/>
   <rule symbol="1" key="{9508f717-f42e-432f-9454-f7b5e7394a2a}" filter="ELSE"/>
  </rules>
  <symbols>
   <symbol force_rhr="0" name="0" type="fill" clip_to_extent="1" alpha="1">
    <data_defined_properties>
     <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
     </Option>
    </data_defined_properties>
    <layer locked="0" class="LinePatternFill" pass="0" enabled="1">
     <Option type="Map">
      <Option value="45" name="angle" type="QString"/>
      <Option value="during_render" name="clip_mode" type="QString"/>
      <Option value="55,126,184,255" name="color" type="QString"/>
      <Option value="feature" name="coordinate_reference" type="QString"/>
      <Option value="2" name="distance" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="distance_map_unit_scale" type="QString"/>
      <Option value="MM" name="distance_unit" type="QString"/>
      <Option value="0.26" name="line_width" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="line_width_map_unit_scale" type="QString"/>
      <Option value="MM" name="line_width_unit" type="QString"/>
      <Option value="0" name="offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="offset_unit" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
      <Option value="MM" name="outline_width_unit" type="QString"/>
     </Option>
     <prop k="angle" v="45"/>
     <prop k="clip_mode" v="during_render"/>
     <prop k="color" v="55,126,184,255"/>
     <prop k="coordinate_reference" v="feature"/>
     <prop k="distance" v="2"/>
     <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="distance_unit" v="MM"/>
     <prop k="line_width" v="0.26"/>
     <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="outline_width_unit" v="MM"/>
     <data_defined_properties>
      <Option type="Map">
       <Option value="" name="name" type="QString"/>
       <Option name="properties"/>
       <Option value="collection" name="type" type="QString"/>
      </Option>
     </data_defined_properties>
     <symbol force_rhr="0" name="@0@0" type="line" clip_to_extent="1" alpha="1">
      <data_defined_properties>
       <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
       </Option>
      </data_defined_properties>
      <layer locked="0" class="SimpleLine" pass="0" enabled="1">
       <Option type="Map">
        <Option value="0" name="align_dash_pattern" type="QString"/>
        <Option value="square" name="capstyle" type="QString"/>
        <Option value="5;2" name="customdash" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
        <Option value="MM" name="customdash_unit" type="QString"/>
        <Option value="0" name="dash_pattern_offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
        <Option value="0" name="draw_inside_polygon" type="QString"/>
        <Option value="bevel" name="joinstyle" type="QString"/>
        <Option value="77,175,74,255" name="line_color" type="QString"/>
        <Option value="solid" name="line_style" type="QString"/>
        <Option value="0.3" name="line_width" type="QString"/>
        <Option value="MM" name="line_width_unit" type="QString"/>
        <Option value="0" name="offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="offset_unit" type="QString"/>
        <Option value="0" name="ring_filter" type="QString"/>
        <Option value="0" name="trim_distance_end" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
        <Option value="MM" name="trim_distance_end_unit" type="QString"/>
        <Option value="0" name="trim_distance_start" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
        <Option value="MM" name="trim_distance_start_unit" type="QString"/>
        <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
        <Option value="0" name="use_custom_dash" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
       </Option>
       <prop k="align_dash_pattern" v="0"/>
       <prop k="capstyle" v="square"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="dash_pattern_offset" v="0"/>
       <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="dash_pattern_offset_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="77,175,74,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0.3"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="ring_filter" v="0"/>
       <prop k="trim_distance_end" v="0"/>
       <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="trim_distance_end_unit" v="MM"/>
       <prop k="trim_distance_start" v="0"/>
       <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="trim_distance_start_unit" v="MM"/>
       <prop k="tweak_dash_pattern_on_corners" v="0"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <data_defined_properties>
        <Option type="Map">
         <Option value="" name="name" type="QString"/>
         <Option name="properties"/>
         <Option value="collection" name="type" type="QString"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </layer>
    <layer locked="0" class="SimpleLine" pass="0" enabled="1">
     <Option type="Map">
      <Option value="0" name="align_dash_pattern" type="QString"/>
      <Option value="square" name="capstyle" type="QString"/>
      <Option value="5;2" name="customdash" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
      <Option value="MM" name="customdash_unit" type="QString"/>
      <Option value="0" name="dash_pattern_offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
      <Option value="0" name="draw_inside_polygon" type="QString"/>
      <Option value="bevel" name="joinstyle" type="QString"/>
      <Option value="77,175,74,255" name="line_color" type="QString"/>
      <Option value="solid" name="line_style" type="QString"/>
      <Option value="0.46" name="line_width" type="QString"/>
      <Option value="MM" name="line_width_unit" type="QString"/>
      <Option value="0" name="offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="offset_unit" type="QString"/>
      <Option value="0" name="ring_filter" type="QString"/>
      <Option value="0" name="trim_distance_end" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
      <Option value="MM" name="trim_distance_end_unit" type="QString"/>
      <Option value="0" name="trim_distance_start" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
      <Option value="MM" name="trim_distance_start_unit" type="QString"/>
      <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
      <Option value="0" name="use_custom_dash" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
     </Option>
     <prop k="align_dash_pattern" v="0"/>
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="dash_pattern_offset" v="0"/>
     <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="dash_pattern_offset_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="77,175,74,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.46"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="ring_filter" v="0"/>
     <prop k="trim_distance_end" v="0"/>
     <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="trim_distance_end_unit" v="MM"/>
     <prop k="trim_distance_start" v="0"/>
     <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="trim_distance_start_unit" v="MM"/>
     <prop k="tweak_dash_pattern_on_corners" v="0"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <data_defined_properties>
      <Option type="Map">
       <Option value="" name="name" type="QString"/>
       <Option name="properties"/>
       <Option value="collection" name="type" type="QString"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
   <symbol force_rhr="0" name="1" type="fill" clip_to_extent="1" alpha="1">
    <data_defined_properties>
     <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
     </Option>
    </data_defined_properties>
    <layer locked="0" class="LinePatternFill" pass="0" enabled="1">
     <Option type="Map">
      <Option value="135" name="angle" type="QString"/>
      <Option value="during_render" name="clip_mode" type="QString"/>
      <Option value="55,126,184,255" name="color" type="QString"/>
      <Option value="feature" name="coordinate_reference" type="QString"/>
      <Option value="2" name="distance" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="distance_map_unit_scale" type="QString"/>
      <Option value="MM" name="distance_unit" type="QString"/>
      <Option value="0.26" name="line_width" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="line_width_map_unit_scale" type="QString"/>
      <Option value="MM" name="line_width_unit" type="QString"/>
      <Option value="0" name="offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="offset_unit" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
      <Option value="MM" name="outline_width_unit" type="QString"/>
     </Option>
     <prop k="angle" v="135"/>
     <prop k="clip_mode" v="during_render"/>
     <prop k="color" v="55,126,184,255"/>
     <prop k="coordinate_reference" v="feature"/>
     <prop k="distance" v="2"/>
     <prop k="distance_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="distance_unit" v="MM"/>
     <prop k="line_width" v="0.26"/>
     <prop k="line_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="outline_width_unit" v="MM"/>
     <data_defined_properties>
      <Option type="Map">
       <Option value="" name="name" type="QString"/>
       <Option name="properties"/>
       <Option value="collection" name="type" type="QString"/>
      </Option>
     </data_defined_properties>
     <symbol force_rhr="0" name="@1@0" type="line" clip_to_extent="1" alpha="1">
      <data_defined_properties>
       <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
       </Option>
      </data_defined_properties>
      <layer locked="0" class="SimpleLine" pass="0" enabled="1">
       <Option type="Map">
        <Option value="0" name="align_dash_pattern" type="QString"/>
        <Option value="square" name="capstyle" type="QString"/>
        <Option value="5;2" name="customdash" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
        <Option value="MM" name="customdash_unit" type="QString"/>
        <Option value="0" name="dash_pattern_offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
        <Option value="0" name="draw_inside_polygon" type="QString"/>
        <Option value="bevel" name="joinstyle" type="QString"/>
        <Option value="228,26,28,255" name="line_color" type="QString"/>
        <Option value="solid" name="line_style" type="QString"/>
        <Option value="0.3" name="line_width" type="QString"/>
        <Option value="MM" name="line_width_unit" type="QString"/>
        <Option value="0" name="offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="offset_unit" type="QString"/>
        <Option value="0" name="ring_filter" type="QString"/>
        <Option value="0" name="trim_distance_end" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
        <Option value="MM" name="trim_distance_end_unit" type="QString"/>
        <Option value="0" name="trim_distance_start" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
        <Option value="MM" name="trim_distance_start_unit" type="QString"/>
        <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
        <Option value="0" name="use_custom_dash" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
       </Option>
       <prop k="align_dash_pattern" v="0"/>
       <prop k="capstyle" v="square"/>
       <prop k="customdash" v="5;2"/>
       <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="customdash_unit" v="MM"/>
       <prop k="dash_pattern_offset" v="0"/>
       <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="dash_pattern_offset_unit" v="MM"/>
       <prop k="draw_inside_polygon" v="0"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="line_color" v="228,26,28,255"/>
       <prop k="line_style" v="solid"/>
       <prop k="line_width" v="0.3"/>
       <prop k="line_width_unit" v="MM"/>
       <prop k="offset" v="0"/>
       <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="ring_filter" v="0"/>
       <prop k="trim_distance_end" v="0"/>
       <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="trim_distance_end_unit" v="MM"/>
       <prop k="trim_distance_start" v="0"/>
       <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="trim_distance_start_unit" v="MM"/>
       <prop k="tweak_dash_pattern_on_corners" v="0"/>
       <prop k="use_custom_dash" v="0"/>
       <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <data_defined_properties>
        <Option type="Map">
         <Option value="" name="name" type="QString"/>
         <Option name="properties"/>
         <Option value="collection" name="type" type="QString"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </layer>
    <layer locked="0" class="SimpleLine" pass="0" enabled="1">
     <Option type="Map">
      <Option value="0" name="align_dash_pattern" type="QString"/>
      <Option value="square" name="capstyle" type="QString"/>
      <Option value="5;2" name="customdash" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
      <Option value="MM" name="customdash_unit" type="QString"/>
      <Option value="0" name="dash_pattern_offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
      <Option value="0" name="draw_inside_polygon" type="QString"/>
      <Option value="bevel" name="joinstyle" type="QString"/>
      <Option value="228,26,28,255" name="line_color" type="QString"/>
      <Option value="solid" name="line_style" type="QString"/>
      <Option value="0.46" name="line_width" type="QString"/>
      <Option value="MM" name="line_width_unit" type="QString"/>
      <Option value="0" name="offset" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
      <Option value="MM" name="offset_unit" type="QString"/>
      <Option value="0" name="ring_filter" type="QString"/>
      <Option value="0" name="trim_distance_end" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
      <Option value="MM" name="trim_distance_end_unit" type="QString"/>
      <Option value="0" name="trim_distance_start" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
      <Option value="MM" name="trim_distance_start_unit" type="QString"/>
      <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
      <Option value="0" name="use_custom_dash" type="QString"/>
      <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
     </Option>
     <prop k="align_dash_pattern" v="0"/>
     <prop k="capstyle" v="square"/>
     <prop k="customdash" v="5;2"/>
     <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="customdash_unit" v="MM"/>
     <prop k="dash_pattern_offset" v="0"/>
     <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="dash_pattern_offset_unit" v="MM"/>
     <prop k="draw_inside_polygon" v="0"/>
     <prop k="joinstyle" v="bevel"/>
     <prop k="line_color" v="228,26,28,255"/>
     <prop k="line_style" v="solid"/>
     <prop k="line_width" v="0.46"/>
     <prop k="line_width_unit" v="MM"/>
     <prop k="offset" v="0"/>
     <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="offset_unit" v="MM"/>
     <prop k="ring_filter" v="0"/>
     <prop k="trim_distance_end" v="0"/>
     <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="trim_distance_end_unit" v="MM"/>
     <prop k="trim_distance_start" v="0"/>
     <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <prop k="trim_distance_start_unit" v="MM"/>
     <prop k="tweak_dash_pattern_on_corners" v="0"/>
     <prop k="use_custom_dash" v="0"/>
     <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
     <data_defined_properties>
      <Option type="Map">
       <Option value="" name="name" type="QString"/>
       <Option name="properties"/>
       <Option value="collection" name="type" type="QString"/>
      </Option>
     </data_defined_properties>
    </layer>
   </symbol>
  </symbols>
 </renderer-v2>
 <labeling type="simple">
  <settings calloutType="simple">
   <text-style namedStyle="Regular" fontStrikeout="0" fontWordSpacing="0" textColor="50,50,50,255" multilineHeight="1" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="&quot;nome&quot; +  ''\n'' + ''Aprovados: '' + to_string(total_pontos_aprovados) +  ''\n'' + ''Em Avaliação: '' + to_string(total_pontos_em_avaliacao)" blendMode="0" fontSizeUnit="Point" useSubstitutions="0" allowHtml="0" fontWeight="50" fontFamily="Liberation Sans" isExpression="1" fontItalic="0" textOpacity="1" fontLetterSpacing="0" fontSize="10" legendString="Aa" textOrientation="horizontal" fontUnderline="0" capitalization="0" previewBkgrdColor="255,255,255,255" fontKerning="1">
    <families/>
    <text-buffer bufferJoinStyle="128" bufferSize="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSizeUnits="MM" bufferBlendMode="0" bufferColor="250,250,250,255" bufferDraw="0" bufferNoFill="1" bufferOpacity="1"/>
    <text-mask maskType="0" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskSize="0" maskEnabled="0" maskOpacity="1" maskJoinStyle="128"/>
    <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeBlendMode="0" shapeOffsetY="0" shapeRadiiY="0" shapeOffsetUnit="Point" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeSizeUnit="Point" shapeSVGFile="" shapeFillColor="255,255,255,255" shapeOffsetX="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeRadiiX="0" shapeBorderWidthUnit="Point" shapeOpacity="1" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeRotation="0" shapeRadiiUnit="Point" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeType="0" shapeDraw="0" shapeSizeX="0" shapeRotationType="0" shapeBorderWidth="0">
     <symbol force_rhr="0" name="markerSymbol" type="marker" clip_to_extent="1" alpha="1">
      <data_defined_properties>
       <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
       </Option>
      </data_defined_properties>
      <layer locked="0" class="SimpleMarker" pass="0" enabled="1">
       <Option type="Map">
        <Option value="0" name="angle" type="QString"/>
        <Option value="square" name="cap_style" type="QString"/>
        <Option value="229,182,54,255" name="color" type="QString"/>
        <Option value="1" name="horizontal_anchor_point" type="QString"/>
        <Option value="bevel" name="joinstyle" type="QString"/>
        <Option value="circle" name="name" type="QString"/>
        <Option value="0,0" name="offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="offset_unit" type="QString"/>
        <Option value="35,35,35,255" name="outline_color" type="QString"/>
        <Option value="solid" name="outline_style" type="QString"/>
        <Option value="0" name="outline_width" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString"/>
        <Option value="MM" name="outline_width_unit" type="QString"/>
        <Option value="diameter" name="scale_method" type="QString"/>
        <Option value="2" name="size" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString"/>
        <Option value="MM" name="size_unit" type="QString"/>
        <Option value="1" name="vertical_anchor_point" type="QString"/>
       </Option>
       <prop k="angle" v="0"/>
       <prop k="cap_style" v="square"/>
       <prop k="color" v="229,182,54,255"/>
       <prop k="horizontal_anchor_point" v="1"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="name" v="circle"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="35,35,35,255"/>
       <prop k="outline_style" v="solid"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="outline_width_unit" v="MM"/>
       <prop k="scale_method" v="diameter"/>
       <prop k="size" v="2"/>
       <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="size_unit" v="MM"/>
       <prop k="vertical_anchor_point" v="1"/>
       <data_defined_properties>
        <Option type="Map">
         <Option value="" name="name" type="QString"/>
         <Option name="properties"/>
         <Option value="collection" name="type" type="QString"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
     <symbol force_rhr="0" name="fillSymbol" type="fill" clip_to_extent="1" alpha="1">
      <data_defined_properties>
       <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
       </Option>
      </data_defined_properties>
      <layer locked="0" class="SimpleFill" pass="0" enabled="1">
       <Option type="Map">
        <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString"/>
        <Option value="255,255,255,255" name="color" type="QString"/>
        <Option value="bevel" name="joinstyle" type="QString"/>
        <Option value="0,0" name="offset" type="QString"/>
        <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
        <Option value="MM" name="offset_unit" type="QString"/>
        <Option value="128,128,128,255" name="outline_color" type="QString"/>
        <Option value="no" name="outline_style" type="QString"/>
        <Option value="0" name="outline_width" type="QString"/>
        <Option value="Point" name="outline_width_unit" type="QString"/>
        <Option value="solid" name="style" type="QString"/>
       </Option>
       <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="color" v="255,255,255,255"/>
       <prop k="joinstyle" v="bevel"/>
       <prop k="offset" v="0,0"/>
       <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
       <prop k="offset_unit" v="MM"/>
       <prop k="outline_color" v="128,128,128,255"/>
       <prop k="outline_style" v="no"/>
       <prop k="outline_width" v="0"/>
       <prop k="outline_width_unit" v="Point"/>
       <prop k="style" v="solid"/>
       <data_defined_properties>
        <Option type="Map">
         <Option value="" name="name" type="QString"/>
         <Option name="properties"/>
         <Option value="collection" name="type" type="QString"/>
        </Option>
       </data_defined_properties>
      </layer>
     </symbol>
    </background>
    <shadow shadowOffsetDist="1" shadowRadius="1.5" shadowOpacity="0.69999999999999996" shadowOffsetAngle="135" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusUnit="MM" shadowDraw="0" shadowOffsetUnit="MM" shadowOffsetGlobal="1" shadowUnder="0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowBlendMode="6" shadowRadiusAlphaOnly="0" shadowColor="0,0,0,255"/>
    <dd_properties>
     <Option type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
     </Option>
    </dd_properties>
    <substitutions/>
   </text-style>
   <text-format placeDirectionSymbol="0" addDirectionSymbol="0" reverseDirectionSymbol="0" multilineAlign="3" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" formatNumbers="0" plussign="0" useMaxLineLengthForAutoWrap="1" decimals="3" wrapChar="" autoWrapLength="0"/>
   <placement offsetUnits="MM" lineAnchorType="0" centroidInside="0" dist="0" geometryGeneratorType="PointGeometry" maxCurvedCharAngleIn="25" rotationUnit="AngleDegrees" lineAnchorClipping="0" overrunDistanceUnit="MM" priority="5" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" repeatDistanceUnits="MM" lineAnchorPercent="0.5" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" preserveRotation="1" placement="0" placementFlags="10" geometryGenerator="" distUnits="MM" fitInPolygonOnly="0" offsetType="0" polygonPlacementFlags="2" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" geometryGeneratorEnabled="0" yOffset="0" xOffset="0" centroidWhole="0" quadOffset="4" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" layerType="PolygonGeometry" maxCurvedCharAngleOut="-25" repeatDistance="0"/>
   <rendering scaleMax="0" unplacedVisibility="0" obstacle="1" displayAll="0" fontLimitPixelSize="0" mergeLines="0" maxNumLabels="2000" scaleMin="0" fontMinPixelSize="3" upsidedownLabels="0" obstacleType="1" zIndex="0" limitNumLabels="0" fontMaxPixelSize="10000" minFeatureSize="0" scaleVisibility="0" labelPerPart="0" drawLabels="1" obstacleFactor="1"/>
   <dd_properties>
    <Option type="Map">
     <Option value="" name="name" type="QString"/>
     <Option name="properties"/>
     <Option value="collection" name="type" type="QString"/>
    </Option>
   </dd_properties>
   <callout type="simple">
    <Option type="Map">
     <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString"/>
     <Option value="0" name="blendMode" type="int"/>
     <Option name="ddProperties" type="Map">
      <Option value="" name="name" type="QString"/>
      <Option name="properties"/>
      <Option value="collection" name="type" type="QString"/>
     </Option>
     <Option value="false" name="drawToAllParts" type="bool"/>
     <Option value="0" name="enabled" type="QString"/>
     <Option value="point_on_exterior" name="labelAnchorPoint" type="QString"/>
     <Option value="&lt;symbol force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot; clip_to_extent=&quot;1&quot; alpha=&quot;1&quot;>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;layer locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot; enabled=&quot;1&quot;>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/>&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_end_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_end_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;trim_distance_start&quot; v=&quot;0&quot;/>&lt;prop k=&quot;trim_distance_start_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;trim_distance_start_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" name="lineSymbol" type="QString"/>
     <Option value="0" name="minLength" type="double"/>
     <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString"/>
     <Option value="MM" name="minLengthUnit" type="QString"/>
     <Option value="0" name="offsetFromAnchor" type="double"/>
     <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString"/>
     <Option value="MM" name="offsetFromAnchorUnit" type="QString"/>
     <Option value="0" name="offsetFromLabel" type="double"/>
     <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString"/>
     <Option value="MM" name="offsetFromLabelUnit" type="QString"/>
    </Option>
   </callout>
  </settings>
 </labeling>
 <customproperties>
  <Option type="Map">
   <Option name="dualview/previewExpressions" type="List">
    <Option value="&quot;nome&quot;" type="QString"/>
   </Option>
   <Option value="0" name="embeddedWidgets/count" type="int"/>
   <Option name="variableNames"/>
   <Option name="variableValues"/>
  </Option>
 </customproperties>
 <blendMode>0</blendMode>
 <featureBlendMode>0</featureBlendMode>
 <layerOpacity>1</layerOpacity>
 <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
  <DiagramCategory backgroundColor="#ffffff" sizeType="MM" backgroundAlpha="255" scaleDependency="Area" spacing="5" maxScaleDenominator="1e+08" spacingUnit="MM" penAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" direction="0" lineSizeType="MM" labelPlacementMethod="XHeight" enabled="0" minScaleDenominator="0" minimumSize="0" showAxis="1" diagramOrientation="Up" height="15" width="15" spacingUnitScale="3x:0,0,0,0,0,0" barWidth="5" opacity="1" sizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" penColor="#000000" rotationOffset="270">
   <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
   <axisSymbol>
    <symbol force_rhr="0" name="" type="line" clip_to_extent="1" alpha="1">
     <data_defined_properties>
      <Option type="Map">
       <Option value="" name="name" type="QString"/>
       <Option name="properties"/>
       <Option value="collection" name="type" type="QString"/>
      </Option>
     </data_defined_properties>
     <layer locked="0" class="SimpleLine" pass="0" enabled="1">
      <Option type="Map">
       <Option value="0" name="align_dash_pattern" type="QString"/>
       <Option value="square" name="capstyle" type="QString"/>
       <Option value="5;2" name="customdash" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="customdash_map_unit_scale" type="QString"/>
       <Option value="MM" name="customdash_unit" type="QString"/>
       <Option value="0" name="dash_pattern_offset" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="dash_pattern_offset_map_unit_scale" type="QString"/>
       <Option value="MM" name="dash_pattern_offset_unit" type="QString"/>
       <Option value="0" name="draw_inside_polygon" type="QString"/>
       <Option value="bevel" name="joinstyle" type="QString"/>
       <Option value="35,35,35,255" name="line_color" type="QString"/>
       <Option value="solid" name="line_style" type="QString"/>
       <Option value="0.26" name="line_width" type="QString"/>
       <Option value="MM" name="line_width_unit" type="QString"/>
       <Option value="0" name="offset" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString"/>
       <Option value="MM" name="offset_unit" type="QString"/>
       <Option value="0" name="ring_filter" type="QString"/>
       <Option value="0" name="trim_distance_end" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="trim_distance_end_map_unit_scale" type="QString"/>
       <Option value="MM" name="trim_distance_end_unit" type="QString"/>
       <Option value="0" name="trim_distance_start" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="trim_distance_start_map_unit_scale" type="QString"/>
       <Option value="MM" name="trim_distance_start_unit" type="QString"/>
       <Option value="0" name="tweak_dash_pattern_on_corners" type="QString"/>
       <Option value="0" name="use_custom_dash" type="QString"/>
       <Option value="3x:0,0,0,0,0,0" name="width_map_unit_scale" type="QString"/>
      </Option>
      <prop k="align_dash_pattern" v="0"/>
      <prop k="capstyle" v="square"/>
      <prop k="customdash" v="5;2"/>
      <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <prop k="customdash_unit" v="MM"/>
      <prop k="dash_pattern_offset" v="0"/>
      <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <prop k="dash_pattern_offset_unit" v="MM"/>
      <prop k="draw_inside_polygon" v="0"/>
      <prop k="joinstyle" v="bevel"/>
      <prop k="line_color" v="35,35,35,255"/>
      <prop k="line_style" v="solid"/>
      <prop k="line_width" v="0.26"/>
      <prop k="line_width_unit" v="MM"/>
      <prop k="offset" v="0"/>
      <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <prop k="offset_unit" v="MM"/>
      <prop k="ring_filter" v="0"/>
      <prop k="trim_distance_end" v="0"/>
      <prop k="trim_distance_end_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <prop k="trim_distance_end_unit" v="MM"/>
      <prop k="trim_distance_start" v="0"/>
      <prop k="trim_distance_start_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <prop k="trim_distance_start_unit" v="MM"/>
      <prop k="tweak_dash_pattern_on_corners" v="0"/>
      <prop k="use_custom_dash" v="0"/>
      <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
      <data_defined_properties>
       <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties"/>
        <Option value="collection" name="type" type="QString"/>
       </Option>
      </data_defined_properties>
     </layer>
    </symbol>
   </axisSymbol>
  </DiagramCategory>
 </SingleCategoryDiagramRenderer>
 <DiagramLayerSettings placement="1" priority="0" linePlacementFlags="18" dist="0" showAll="1" obstacle="0" zIndex="0">
  <properties>
   <Option type="Map">
    <Option value="" name="name" type="QString"/>
    <Option name="properties"/>
    <Option value="collection" name="type" type="QString"/>
   </Option>
  </properties>
 </DiagramLayerSettings>
 <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
  <activeChecks/>
  <checkConfiguration type="Map">
   <Option name="QgsGeometryGapCheck" type="Map">
    <Option value="0" name="allowedGapsBuffer" type="double"/>
    <Option value="false" name="allowedGapsEnabled" type="bool"/>
    <Option value="" name="allowedGapsLayer" type="QString"/>
   </Option>
  </checkConfiguration>
 </geometryOptions>
 <legend showLabelLegend="0" type="default-vector"/>
 <referencedLayers/>
 <fieldConfiguration>
  <field configurationFlags="None" name="id">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="nome">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="total_pontos_aprovados">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="total_pontos_em_avaliacao">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="total_pontos_previstos">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="lote">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
  <field configurationFlags="None" name="area_otf">
   <editWidget type="TextEdit">
    <config>
     <Option/>
    </config>
   </editWidget>
  </field>
 </fieldConfiguration>
 <aliases>
  <alias index="0" field="id" name=""/>
  <alias index="1" field="nome" name=""/>
  <alias index="2" field="total_pontos_aprovados" name=""/>
  <alias index="3" field="total_pontos_em_avaliacao" name=""/>
  <alias index="4" field="total_pontos_previstos" name=""/>
  <alias index="5" field="lote" name=""/>
  <alias index="6" field="area_otf" name=""/>
 </aliases>
 <defaults>
  <default expression="" field="id" applyOnUpdate="0"/>
  <default expression="" field="nome" applyOnUpdate="0"/>
  <default expression="" field="total_pontos_aprovados" applyOnUpdate="0"/>
  <default expression="" field="total_pontos_em_avaliacao" applyOnUpdate="0"/>
  <default expression="" field="total_pontos_previstos" applyOnUpdate="0"/>
  <default expression="" field="lote" applyOnUpdate="0"/>
  <default expression="" field="area_otf" applyOnUpdate="0"/>
 </defaults>
 <constraints>
  <constraint exp_strength="0" unique_strength="1" notnull_strength="1" field="id" constraints="3"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="1" field="nome" constraints="1"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="1" field="total_pontos_aprovados" constraints="1"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="1" field="total_pontos_em_avaliacao" constraints="1"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="1" field="total_pontos_previstos" constraints="1"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="lote" constraints="0"/>
  <constraint exp_strength="0" unique_strength="0" notnull_strength="0" field="area_otf" constraints="0"/>
 </constraints>
 <constraintExpressions>
  <constraint exp="" desc="" field="id"/>
  <constraint exp="" desc="" field="nome"/>
  <constraint exp="" desc="" field="total_pontos_aprovados"/>
  <constraint exp="" desc="" field="total_pontos_em_avaliacao"/>
  <constraint exp="" desc="" field="total_pontos_previstos"/>
  <constraint exp="" desc="" field="lote"/>
  <constraint exp="" desc="" field="area_otf"/>
 </constraintExpressions>
 <expressionfields>
  <field precision="0" expression="$area" length="0" name="area_otf" type="6" typeName="" comment="" subType="0"/>
 </expressionfields>
 <attributeactions>
  <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
 </attributeactions>
 <attributetableconfig sortExpression="&quot;total_pontos_em_avaliacao&quot;" actionWidgetStyle="dropDown" sortOrder="1">
  <columns>
   <column width="-1" hidden="0" name="id" type="field"/>
   <column width="-1" hidden="0" name="nome" type="field"/>
   <column width="-1" hidden="0" name="total_pontos_aprovados" type="field"/>
   <column width="165" hidden="0" name="total_pontos_em_avaliacao" type="field"/>
   <column width="129" hidden="0" name="total_pontos_previstos" type="field"/>
   <column width="-1" hidden="0" name="lote" type="field"/>
   <column width="-1" hidden="0" name="area_otf" type="field"/>
   <column width="-1" hidden="1" type="actions"/>
  </columns>
 </attributetableconfig>
 <conditionalstyles>
  <rowstyles/>
  <fieldstyles/>
 </conditionalstyles>
 <storedexpressions/>
 <editform tolerant="1"></editform>
 <editforminit/>
 <editforminitcodesource>0</editforminitcodesource>
 <editforminitfilepath></editforminitfilepath>
 <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
    geom = feature.geometry()
    control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
 <featformsuppress>0</featformsuppress>
 <editorlayout>generatedlayout</editorlayout>
 <editable>
  <field name="area_otf" editable="0"/>
  <field name="id" editable="1"/>
  <field name="lote" editable="1"/>
  <field name="nome" editable="1"/>
  <field name="total_pontos_aprovados" editable="1"/>
  <field name="total_pontos_em_avaliacao" editable="1"/>
  <field name="total_pontos_previstos" editable="1"/>
 </editable>
 <labelOnTop>
  <field labelOnTop="0" name="area_otf"/>
  <field labelOnTop="0" name="id"/>
  <field labelOnTop="0" name="lote"/>
  <field labelOnTop="0" name="nome"/>
  <field labelOnTop="0" name="total_pontos_aprovados"/>
  <field labelOnTop="0" name="total_pontos_em_avaliacao"/>
  <field labelOnTop="0" name="total_pontos_previstos"/>
 </labelOnTop>
 <reuseLastValue>
  <field reuseLastValue="0" name="area_otf"/>
  <field reuseLastValue="0" name="id"/>
  <field reuseLastValue="0" name="lote"/>
  <field reuseLastValue="0" name="nome"/>
  <field reuseLastValue="0" name="total_pontos_aprovados"/>
  <field reuseLastValue="0" name="total_pontos_em_avaliacao"/>
  <field reuseLastValue="0" name="total_pontos_previstos"/>
 </reuseLastValue>
 <dataDefinedFieldProperties/>
 <widgets/>
 <previewExpression>"nome"</previewExpression>
 <mapTip></mapTip>
 <layerGeometryType>2</layerGeometryType>
</qgis>
', '<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ogc="http://www.opengis.net/ogc" xmlns:se="http://www.opengis.net/se" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1.0" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.1.0/StyledLayerDescriptor.xsd">
 <NamedLayer>
  <se:Name>controle_medicao_a</se:Name>
  <UserStyle>
   <se:Name>controle_medicao_a</se:Name>
   <se:FeatureTypeStyle>
    <se:Rule>
     <se:Name></se:Name>
     <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
      <ogc:Function name="if">
       <ogc:PropertyIsGreaterThan>
        <ogc:PropertyName>total_pontos_aprovados</ogc:PropertyName>
        <ogc:PropertyName>total_pontos_em_avaliacao</ogc:PropertyName>
       </ogc:PropertyIsGreaterThan>
       <ogc:Literal>1</ogc:Literal>
       <ogc:Literal>0</ogc:Literal>
      </ogc:Function>
     </ogc:Filter>
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:GraphicFill>
        <se:Graphic>
         <se:Mark>
          <se:WellKnownName>horline</se:WellKnownName>
          <se:Stroke>
           <se:SvgParameter name="stroke">#4daf4a</se:SvgParameter>
           <se:SvgParameter name="stroke-width">1</se:SvgParameter>
          </se:Stroke>
         </se:Mark>
         <se:Size>7</se:Size>
         <se:Rotation>
          <ogc:Literal>45</ogc:Literal>
         </se:Rotation>
        </se:Graphic>
       </se:GraphicFill>
      </se:Fill>
     </se:PolygonSymbolizer>
     <se:LineSymbolizer>
      <se:Stroke>
       <se:SvgParameter name="stroke">#4daf4a</se:SvgParameter>
       <se:SvgParameter name="stroke-width">2</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
       <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
      </se:Stroke>
     </se:LineSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:Name></se:Name>
     <!--Parser Error: 
syntax error, unexpected ELSE - Expression was: ELSE-->
     <se:PolygonSymbolizer>
      <se:Fill>
       <se:GraphicFill>
        <se:Graphic>
         <se:Mark>
          <se:WellKnownName>horline</se:WellKnownName>
          <se:Stroke>
           <se:SvgParameter name="stroke">#e41a1c</se:SvgParameter>
           <se:SvgParameter name="stroke-width">1</se:SvgParameter>
          </se:Stroke>
         </se:Mark>
         <se:Size>7</se:Size>
         <se:Rotation>
          <ogc:Literal>135</ogc:Literal>
         </se:Rotation>
        </se:Graphic>
       </se:GraphicFill>
      </se:Fill>
     </se:PolygonSymbolizer>
     <se:LineSymbolizer>
      <se:Stroke>
       <se:SvgParameter name="stroke">#e41a1c</se:SvgParameter>
       <se:SvgParameter name="stroke-width">2</se:SvgParameter>
       <se:SvgParameter name="stroke-linejoin">bevel</se:SvgParameter>
       <se:SvgParameter name="stroke-linecap">square</se:SvgParameter>
      </se:Stroke>
     </se:LineSymbolizer>
    </se:Rule>
    <se:Rule>
     <se:TextSymbolizer>
      <se:Label>
       <!--SE Export for "nome" + ''\n'' + ''Aprovados: '' + to_string("total_pontos_aprovados") + ''\n'' + ''Em Avaliação: '' + to_string("total_pontos_em_avaliacao") not implemented yet-->Placeholder</se:Label>
      <se:Font>
       <se:SvgParameter name="font-family">Liberation Sans</se:SvgParameter>
       <se:SvgParameter name="font-size">13</se:SvgParameter>
      </se:Font>
      <se:LabelPlacement>
       <se:PointPlacement>
        <se:AnchorPoint>
         <se:AnchorPointX>0</se:AnchorPointX>
         <se:AnchorPointY>0.5</se:AnchorPointY>
        </se:AnchorPoint>
       </se:PointPlacement>
      </se:LabelPlacement>
      <se:Fill>
       <se:SvgParameter name="fill">#323232</se:SvgParameter>
      </se:Fill>
      <se:VendorOption name="maxDisplacement">1</se:VendorOption>
     </se:TextSymbolizer>
    </se:Rule>
   </se:FeatureTypeStyle>
  </UserStyle>
 </NamedLayer>
</StyledLayerDescriptor>
', True, 'Estilo para controle de medição de pontos de controle', 'postgres', '2024-06-08 15:48:23.952276');

