---
title: 'Downgrade de Bibliotecas'
sidebar_position: 3
---

Downgrade para resolução de compatibilidade.

Devido o alto correlacionamento de ferramentas: QGIS, python e node.js, algumas ferramentas podem ser atualizadas e não funcionarem mais de acordo com o esperado.

Para isso, deve-se realizar o downgrade de duas bibliotecas do Python, para que as rotinas rodem em perfeito funcionamento:
* Jinja2 = 2.11.2
* MarkupSafe = 2.4.3
* markdown2 = 2.0.1
* secretary = 0.2.19

# Verificar versão
Abra o **cmd** e digite o comando ```pip list```, em seguida verifique as versões das bibliotecas acima.

# Desinstalar
Caso as versões detectadas sejam superiores as versões listadas acima, deverá ser feito a desinstalação do pacote.
```
pip uninstall nome-pacote
```

# Instalar
Caso não esteja instalado algum dos pacotes listados acima, ou tenha sido necessário desinstalar devido ao versionamento, deverão ser instalados os pacotes corretos.
```
pip install nome-pacote=numero-versao
```