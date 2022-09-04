---
title: 'npm Proxy'
sidebar_position: 2
---

Gerenciador npm não possui proxy definido.

## Set Proxy
Ocorre ao rodar o comando **npm install**, acusando falha de conexão. Caso o usuário esteja em uma rede com Proxy essa mensagem irá aparecer:
```
npm ERR! code ENOTFOUND
```
Para resolver, basta seguir os passos abaixo no próprio terminal.
```
npm config set strict-ssl false
npm --proxy http://nome-usuário:senha@endereço-proxy:porta
```
