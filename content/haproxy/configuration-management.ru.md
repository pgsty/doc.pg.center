---
title: "10. Упрощение управления конфигурацией"
linkTitle: "10. Управление конфигурацией"
weight: 340
description: "Способы упрощения сопровождения больших конфигураций HAProxy"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [Задача]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

Очень часто два узла HAProxy, образующие кластер, используют совершенно одинаковую конфигурацию, за исключением нескольких адресов. Вместо того чтобы сопровождать отдельную копию конфигурации для каждого узла, которые неизбежно начнут различаться, можно включить в конфигурацию переменные окружения. Тогда несколько конфигураций смогут использовать один и тот же файл, различаясь лишь несколькими общесистемными переменными окружения. Эта возможность появилась в версии 1.5, где переменные окружения допускались только в адресах; версия 1.6 расширяет их поддержку на все параметры. Синтаксис такой же, как в оболочке UNIX: переменная начинается со знака доллара ('\$'), за которым следуют открывающая фигурная скобка ('{'), имя переменной и закрывающая скобка ('}'). За исключением адресов, переменные окружения интерпретируются только в аргументах, заключённых в двойные кавычки (это ограничение было необходимо, чтобы не нарушить работу существующих конфигураций с регулярными выражениями, содержащими знак доллара).

Переменные окружения также удобны для конфигураций, которые должны работать на разных площадках и различаться только адресами. Кроме того, они позволяют убрать пароли из некоторых конфигурационных файлов. В приведённом ниже примере сценарий инициализации при запуске загружает файл «site1.env»:

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
