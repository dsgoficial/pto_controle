---
title: 'ProxyError pip'
sidebar_position: 4
---

Gerenciador de bibliotecas pip não tem o proxy configurado.

# Erro
Ocorre o warning abaixo, relativo ao acesso via Proxy do sistema, na hora de realizar o download das bibliotecas via **pip** utilizando o **cmd**
```
Warning: Retrying (...) after connection broken by 'ProxyError'('Cannot connect to proxy.', OSError('...')):
```

# Solução
Pode-se configurar o proxy no **cmd** antes de executar os comandos de instalação **pip**:

Ou ainda, rodar o **pip install** em conjunto com as configurações de Proxy
```
pip install --proxy http://usuario:senha@endereço:porta -r requirements.txt