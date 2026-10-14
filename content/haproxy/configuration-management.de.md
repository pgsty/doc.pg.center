---
title: "10. Einfachere Konfigurationsverwaltung"
linkTitle: "10. Konfigurationsverwaltung"
weight: 340
description: "Verfahren zur einfacheren Pflege umfangreicher HAProxy-Konfigurationen"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [Aufgabe]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

Häufig verwenden zwei HAProxy-Knoten eines Clusters bis auf wenige Adressen genau dieselbe Konfiguration. Statt für jeden Knoten eine eigene Kopie zu pflegen, die zwangsläufig irgendwann abweicht, lassen sich Umgebungsvariablen in die Konfiguration einbinden. So können mehrere Konfigurationen dieselbe Datei verwenden und sich nur in wenigen systemweiten Umgebungsvariablen unterscheiden. Diese Möglichkeit wurde in Version 1.5 eingeführt, zunächst nur für Adressen. Version 1.6 unterstützt Umgebungsvariablen an beliebigen Stellen. Die Syntax entspricht der UNIX-Shell: Eine Variable beginnt mit einem Dollarzeichen ('\$'), gefolgt von einer öffnenden geschweiften Klammer ('{'), dem Variablennamen und einer schließenden geschweiften Klammer ('}'). Außer in Adressen werden Umgebungsvariablen nur in Argumenten ausgewertet, die in doppelten Anführungszeichen stehen. Diese Einschränkung war nötig, damit bestehende Konfigurationen mit regulären Ausdrücken, die ein Dollarzeichen enthalten, weiterhin funktionieren.

Umgebungsvariablen erleichtern auch Konfigurationen für verschiedene Standorte, bei denen sich nur die Adresse ändert. Außerdem können sie dazu dienen, Passwörter aus manchen Konfigurationen zu entfernen. Im folgenden Beispiel liest das Startskript beim Start die Datei "site1.env" ein:

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
