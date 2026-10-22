---
title: "10. Gestión de configuración simplificada"
linkTitle: "10. Gestión de configuración"
weight: 340
description: "Técnicas para facilitar el mantenimiento de configuraciones HAProxy de gran tamaño"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 10"
---

Es muy común que dos nodos HAProxy que constituyen un clúster compartan exactamente la misma
configuración a excepción de unas pocas direcciones. En lugar de tener que mantener una configuración
duplicada para cada nodo, que acabará divergiendo inevitablemente, es posible incluir variables de
entorno en la configuración. De este modo, varias configuraciones pueden compartir exactamente el
mismo archivo con solo unas pocas variables de entorno del sistema diferentes. Esto comenzó en la
versión 1.5, donde solo las direcciones podían incluir variables de entorno, y la 1.6 va más lejos al
admitir variables de entorno en todas partes. La sintaxis es la misma que en el shell de UNIX: una
variable comienza con un signo de dólar («\$»), seguido de una llave de apertura («{»), luego el
nombre de la variable seguido de la llave de cierre («}»). Salvo en el caso de las direcciones, las
variables de entorno solo se interpretan en argumentos rodeados de comillas dobles (esto fue
necesario para no romper configuraciones existentes que usan expresiones regulares con el símbolo
del dólar).

Las variables de entorno también resultan cómodas para escribir configuraciones que se espera que
funcionen en sitios diversos donde solo cambia la dirección. También pueden permitir eliminar las
contraseñas de algunas configuraciones. Ejemplo a continuación, donde el archivo «site1.env» es
cargado por el script de inicialización en el arranque:

```shell
$ cat site1.env
LISTEN=192.168.1.1
CACHE_PFX=192.168.11
SERVER_PFX=192.168.22
LOGGER=192.168.33.1
STATSLP=admin:pa$$w0rd
ABUSERS=/etc/haproxy/abuse.lst
TIMEOUT=10s

$ cat haproxy.cfg
global
    log "${LOGGER}:514" local0

defaults
    mode http
    timeout client "${TIMEOUT}"
    timeout server "${TIMEOUT}"
    timeout connect 5s

frontend public
    bind "${LISTEN}:80"
    http-request reject if { src -f "${ABUSERS}" }
    stats uri /stats
    stats auth "${STATSLP}"
    use_backend cache if { path_end .jpg .css .ico }
    default_backend server

backend cache
    server cache1 "${CACHE_PFX}.1:18080" check
    server cache2 "${CACHE_PFX}.2:18080" check

backend server
    server cache1 "${SERVER_PFX}.1:8080" check
    server cache2 "${SERVER_PFX}.2:8080" check
```
