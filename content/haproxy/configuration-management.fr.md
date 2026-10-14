---
title: "10. Gestion de configuration simplifiée"
linkTitle: "10. Gestion de configuration"
weight: 340
description: "Techniques pour rendre les configurations HAProxy volumineuses plus faciles à maintenir"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

Il est très courant que deux nœuds HAProxy constituant un cluster partagent exactement la même configuration, à l’exception de quelques adresses. Au lieu de devoir maintenir une configuration dupliquée pour chaque nœud, ce qui entraînera inévitablement une divergence, il est possible d’inclure des variables d’environnement dans la configuration. Ainsi, plusieurs configurations peuvent partager exactement le même fichier, en ne modifiant que quelques variables d’environnement système. Cette fonctionnalité a été introduite à partir de la version 1.5, où seules les adresses pouvaient inclure des variables d’environnement, et la version 1.6 va plus loin en permettant l’utilisation de variables d’environnement partout. La syntaxe est identique à celle du shell UNIX : une variable commence par un signe dollar ('$'), suivi d'une accolade ouvrante ('{'), puis le nom de la variable, terminé par une accolade fermante ('}'). À l’exception des adresses, les variables d’environnement ne sont interprétées que dans les arguments entourés de guillemets doubles (ce qui était nécessaire pour ne pas rompre les configurations existantes utilisant des expressions régulières impliquant le symbole dollar).

Les variables d'environnement permettent également d'écrire des configurations destinées à fonctionner sur différents sites, où seule l'adresse change. Elles peuvent aussi permettre de supprimer les mots de passe de certaines configurations. Exemple ci-dessous où le fichier "site1.env" est chargé par le script d'initialisation au démarrage :

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
