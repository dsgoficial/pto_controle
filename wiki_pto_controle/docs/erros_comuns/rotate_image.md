---
title: 'rotate image'
sidebar_position: 6
---

Imagem rotacionada na monografia.

# Erro

Ocorre quando alguma imagem salva na monografia do formato .pdf é rotacionada automaticamente pela rotina generateMonograpy.py e ocasiona uma formatação indesejada no arquivo final.

# Causa

Algumas fotos já vem pré-orientedas em seu metadado. Mesmo que o visualizador de imagem da máquina exiba a foto em sua orientação salva, quando o arquivo bruto é carregado dentro do generateMonograpy.py ele é carregado na sua orientação do metadado.

# Resolução

* Instalar o [ImageMagick](https://imagemagick.org/index.php).
* Durante a instalção: autorizar colocação no PATH da máquina.
* Encontre o caminho da **"pasta_3"** conforme [Validação de Estrutura de Pastas](/guia_pto_controle/validar_estrutura_pastas.md).
* Crie um arquivo magick.ps1, para scripts do **cmd**
* Insira as seguintes informações no arquivo e salve.
```
$RootFolder = "caminho da pasta_3"
$imageFiles = @{}
$imageFiles = Get-ChildItem -Path $RootFolder -Filter *.jpg  -Recurse -ErrorAction SilentlyContinue -Force
foreach($Item in $imageFiles) {
    $imagePath = "$($Item.DirectoryName)\$($Item.Name)"
    Write-Output $imagePath
    Start-Process -FilePath "magick" "$($imagePath) -auto-orient $($imagePath) " -Wait -NoNewWindow
}
```
* Abra o prompt de comando no local onde o arquivo **magick.ps1** foi criado e execute:
```
Powershell.exe -executionpolicy remotesigned magick.ps1
```
* Verifique a saída do prompt de comando, devem estar sendo geradas novas imagens com seus metadados de orientação alterados.
* Concluído o processo, retorne a [Gerar Monografia](/guia_pto_controle/gerar_monografia.md).