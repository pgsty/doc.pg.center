---
title: "9. Filtres pris en charge"
linkTitle: "9. Filtres"
weight: 200
description: "Trace, compression, SPOE, cache, FastCGI, OpenTracing et filtres de débit"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/filters/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 9"
---

Voici la liste des filtres officiellement pris en charge, accompagnée de la liste des paramètres qu'ils acceptent. En fonction des options de compilation, certains de ces filtres pourraient être indisponibles. La liste des filtres disponibles est indiquée dans haproxy -vv.

Voir aussi : « filter »

## 9.1. Trace {#section-9-1}

filter trace [name `<name>`] [random-forwarding] [max-fwd `<max>`] [hexdump]

Arguments :

```text
<name>               est un nom arbitraire indiqué dans les messages.
                     Si aucun nom n'est fourni, "TRACE" est utilisé.

<quiet>              supprime les messages de trace.

<random-forwarding>  active le transfert aléatoire des données analysées.
                     Par défaut, le filtre transfère toutes les données
                     déjà analysées. Avec ce paramètre, il n'en transfère
                     qu'une quantité aléatoire.

<max>                est la quantité maximale de données transférée à la
                     fois. L'option "max-fwd" peut être combinée au
                     transfert aléatoire. <max> doit être un entier positif.
                     0 signifie qu'il n'y a pas de limite.

<hexdump>             produit un dump de toutes les données transférées
                     vers le serveur et le client.
```

Ce filtre peut servir de base pour développer de nouveaux filtres. Il définit toutes les fonctions de rappel et affiche un message sur le flux d'erreur standard (stderr) contenant des informations utiles pour chacune d'elles. Il peut être utile pour déboguer l'activité d'autres filtres ou, tout simplement, l'activité d'HAProxy.

Utiliser les paramètres `<random-parsing>` et/ou `<random-forwarding>` est une bonne manière de tester le comportement d'un filtre qui analyse les données échangées entre un client et un serveur en ajoutant des latences dans le traitement.

## 9.2. Compression HTTP {#section-9-2}

filter comp-req

Active le filtre qui tente explicitement de compresser les requêtes HTTP selon les paramètres « compression ».
Définit implicitement « compression direction request ».

filter comp-res

Active le filtre qui tente explicitement de compresser les réponses HTTP selon les paramètres « compression ».
Définit implicitement « compression direction response »

filter compression (obsolète)

Alias à des fins de compatibilité descendante, équivalent fonctionnellement à l'activation simultanée des filtres « comp-req » et « comp-res ». Le mot-clé « compression » doit être utilisé pour configurer le comportement approprié :

La compression HTTP a été déplacée dans un filtre à partir de HAProxy 1.7. Le mot-clé « compression » doit toujours être utilisé pour activer et configurer la compression HTTP. Et lorsqu'aucun autre filtre n'est utilisé, cela suffit. Lorsqu'il est utilisé avec le cache ou le fcgi-app activés, cela suffit également. Dans ce cas, la compression est toujours effectuée après que la réponse a été stockée dans le cache. Toutefois, il est obligatoire d'utiliser explicitement une ligne de filtre pour activer la compression HTTP lorsqu'au moins un filtre autre que le cache ou le fcgi-app est utilisé pour le même écouteur/frontal/backend. Il est important de connaître l'ordre d'évaluation des filtres.

Voir également : « compression », [section 9.4](/fr/haproxy/filters/#section-9-4) concernant le filtre de cache et [section 9.5](/fr/haproxy/filters/#section-9-5) concernant le filtre fcgi-app.

## 9.3. Moteur de traitement de flux (SPOE) {#section-9-3}

filter spoe [engine `<name>`] config `<file>`

Arguments :

```text
<name>      est le nom du moteur permettant de trouver la bonne portée
            dans le fichier de configuration. S'il n'est pas fourni,
            l'ensemble du fichier est analysé.

<file>      est le chemin du fichier de configuration du moteur. Ce fichier
            peut contenir la configuration de plusieurs moteurs ; chaque
            partie doit alors être placée dans sa propre portée.
```

Le moteur de traitement de flux (SPOE) est un filtre communiquant avec des composants externes. Il permet de déporter certains traitements spécifiques sur les flux dans les applications hiérarchisées. Ces composants externes et les informations échangées avec eux sont configurés dans des fichiers dédiés, pour la majeure partie. Il nécessite également des backends dédiés, définis dans la configuration HAProxy.

SPOE communique avec les composants externes à l’aide d’un protocole binaire interne, le Stream Processing Offload Protocol (SPOP).

Lorsque le SPOE est utilisé sur un flux, un flux dédié est créé pour gérer la communication avec le composant externe. Le flux principal est le flux parent de ce flux « SPOE ». Cela signifie qu’il est possible de récupérer les variables du flux principal depuis le flux « SPOE ». Voir [section 2.8](/fr/haproxy/configuration-basics/#section-2-8) concernant les variables pour plus de détails.

Pour toute information concernant la configuration SPOE et la spécification SPOP, consultez « doc/SPOE.txt ».

## 9.4. Mise en cache {#section-9-4}

filter cache `<name>`

Arguments :

```text
<name>      est le nom de la section cache utilisée par ce filtre.
```

Le cache utilise un filtre pour stocker les réponses pouvant être mises en cache. Les règles HTTP « cache-store » et « cache-use » doivent être utilisées pour définir comment et quand utiliser un cache. Par défaut, le filtre correspondant est défini implicitement. Lorsqu’aucun autre filtre que fcgi-app ou compression n’est utilisé, cela suffit. Dans ce cas, le filtre de compression est toujours évalué après le filtre de cache. Toutefois, il est obligatoire d’utiliser explicitement une ligne de filtre pour activer un cache lorsqu’au moins un filtre autre que la compression ou fcgi-app est utilisé pour le même écouteur, frontal ou backend. Il est important de connaître l’ordre d’évaluation des filtres.

Voir également : [section 9.2](/fr/haproxy/filters/#section-9-2) concernant le filtre de compression, [section 9.5](/fr/haproxy/filters/#section-9-5) concernant le filtre fcgi-app et [section 6](/fr/haproxy/cache/) concernant le cache.

## 9.5. Fcgi-app {#section-9-5}

filter fcgi-app `<name>`

Arguments :

```text
<name>      est le nom de la section fcgi-app utilisée par ce filtre.
```

L'application FastCGI utilise un filtre pour évaluer tous les paramètres personnalisés sur le chemin de la requête, et pour traiter les en-têtes sur le chemin de la réponse. Le `<name>` doit faire référence à une section fcgi-app existante. La directive « use-fcgi-app » devrait être utilisée pour définir l'application à utiliser. Par défaut, le filtre correspondant est implicitement défini. Et lorsqu'aucun autre filtre que le cache ou la compression n'est utilisé, cela suffit. Mais il est obligatoire d'utiliser explicitement une ligne de filtre pour une fcgi-app lorsqu'au moins un filtre autre que la compression ou le cache est utilisé pour le même backend. Il est important de connaître l'ordre d'évaluation des filtres.

Voir également : « use-fcgi-app », [section 9.2](/fr/haproxy/filters/#section-9-2) concernant le filtre de compression, [section 9.4](/fr/haproxy/filters/#section-9-4) concernant le filtre de mise en cache et [section 10](/fr/haproxy/fastcgi/) concernant l'application FastCGI.

## 9.6. OpenTracing {#section-9-6}

Le filtre OpenTracing ajoute un support natif de la traçabilité distribuée dans HAProxy. Ce support est activé en envoyant une requête conforme à OpenTracing à l'un des traceurs pris en charge, tels que Datadog, Jaeger, Lightstep ou Zipkin. Veuillez noter : les traceurs ne sont pas listés selon une préférence, mais par ordre alphabétique.

Cette fonctionnalité n’est activée que si HAProxy a été compilé avec USE_OT=1.

L'activation du filtre OpenTracing s'effectue de manière explicite en le spécifiant dans la configuration HAProxy.
Si cela n'est pas fait, le filtre OpenTracing ne participe en aucune manière au fonctionnement de HAProxy.

filter opentracing [id `<id>`] config `<file>`

Arguments :

```text
<id>        est l'identifiant du filtre OpenTracing permettant de trouver
            la bonne portée dans le fichier de configuration. Si aucun
            identifiant n'est indiqué, 'ot-filter' est utilisé par défaut.
            Si le fichier ne précise aucune portée, la configuration
            s'applique à tous les filtres OpenTracing définis.

<file>      est le chemin du fichier de configuration OpenTracing. Le même
            fichier peut configurer plusieurs filtres OpenTracing à la fois.
            Il n'est alors pas nécessaire de définir une portée si la même
            configuration s'applique à tous les filtres ; sinon, chaque
            filtre doit disposer de sa propre portée.
```

Une documentation plus détaillée relative au fonctionnement, à la configuration et à l'utilisation du filtre est disponible dans le répertoire addons/ot.

Note : Le filtre OpenTracing ne devrait pas être utilisé pour de nouvelles conceptions, car OpenTracing n'est plus maintenu ni soutenu par ses auteurs. En conséquence, OpenTracing sera déprécié à partir de la version 3.3 et supprimé à partir de la version 3.5. Un filtre de remplacement basé sur OpenTelemetry est disponible depuis la version 3.4, avec des instructions de compilation complètes actuellement disponibles à :

```text
https://github.com/haproxytech/haproxy-opentelemetry/
```

## 9.7. Limitation de débit {#section-9-7}

```haproxy
filter bwlim-in  <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-out <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-in  <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
filter bwlim-out <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
```

Arguments :

```text
<name>      est le nom du filtre utilisé par les actions
            'set-bandwidth-limit' pour référencer un filtre particulier
            de limitation de bande passante.

<size>      est le nombre maximal d'octets transférés pendant la période.
            Cette valeur est obligatoire pour les filtres de limitation
            par flux et partagés. Elle suit le format des tailles de HAProxy
            et s'exprime en octets.

<pattern>   est une règle d'expression d'échantillon décrite en section 7.3.
            Elle définit les éléments analysés, extraits et combinés pour
            choisir l'entrée de table dont les compteurs seront mis à jour.
            Elle n'est obligatoire que pour les filtres de limitation
            de bande passante partagés.

<table>     est une table facultative remplaçant celle par défaut : la
            stick-table déclarée dans le proxy actuel. Elle ne peut être
            indiquée que pour les filtres de limitation partagés.

<time>      est la période par défaut utilisée pour évaluer le taux de
            limitation de bande passante. Elle ne peut être indiquée que
            pour les filtres de limitation par flux. Elle suit le format
            temporel de HAProxy et s'exprime en millisecondes.

<min-size>  est le nombre minimal facultatif d'octets transférés à la fois
            par un flux, sauf le dernier paquet qui peut être plus petit.
            Cette valeur peut être indiquée pour les filtres de limitation
            par flux et partagés. Elle suit le format des tailles de HAProxy
            et s'exprime en octets.
```

Les filtres de limitation de débit devraient être utilisés pour restreindre la vitesse de transfert des données au niveau du flux. Par extension, de tels filtres limitent la bande passante réseau consommée par une ressource. Plusieurs filtres de limitation de débit peuvent être utilisés. Par exemple, il est possible de définir une limite par adresse source afin de garantir qu’un client ne consomme jamais toute la bande passante réseau, ce qui pourrait pénaliser d’autres clients, et une autre limite par flux afin de pouvoir gérer équitablement plusieurs connexions pour un même client.

L'ordre de définition de ces filtres est important. Si plusieurs filtres de limitation de débit sont activés sur un flux, le filtrage s'applique dans l'ordre de leur définition. Il est également important de comprendre que l'ordre de définition des autres filtres a une influence. Par exemple, selon que le filtre de compression HTTP est défini avant ou après un filtre de limitation de débit, la limite s'appliquera sur le contenu compressé ou non. Il en va de même pour le filtre de mise en cache.

Il existe deux types de filtres de limitation de débit. Le premier impose une limite par défaut et est appliqué par flux. Le second utilise une table de persistance pour appliquer une limite répartie également entre tous les flux partageant la même entrée dans la table.

En outre, selon le mot-clé utilisé pour un filtre, la limitation peut s'appliquer aux données entrantes, reçues du client puis transmises au serveur, ou aux données sortantes, reçues du serveur puis envoyées au client. Utilisez « bwlim-in » pour limiter les données entrantes et « bwlim-out » pour les données sortantes. Dans chaque cas, la limitation s'applique aux données transmises, au niveau du flux.

La limitation de débit est appliquée au niveau du flux et non au niveau de la connexion. Pour les protocoles multiplexés (H2, H3 et FastCGI), les flux de la même connexion peuvent avoir des limites différentes.

Pour un filtre de limitation de débit par flux, les valeurs par défaut de la période et de la limite doivent être définies. Comme leur nom l'indique, il s'agit des valeurs par défaut utilisées pour configurer le débit maximal autorisé pour un flux. Toutefois, pour ce type de filtre et uniquement pour celui-ci, il est possible de redéfinir ces valeurs à l’aide d’expressions d’échantillonnage lorsque le filtre est activé par une action TCP/HTTP « set-bandwidth-limit ».

Pour un filtre de limitation de débit partagé, selon qu'il est appliqué sur les données entrantes ou sortantes, la table de persistance utilisée doit stocker les informations correspondantes sur le débit en octets.
Le compteur "bytes_in_rate(`<period>`)" doit être stocké afin de limiter les données entrantes, et le compteur "bytes_out_rate(`<period>`)" doit être utilisé afin de limiter les données sortantes.

Enfin, il est possible de définir le nombre minimum d’octets qu’un filtre de limitation de débit peut transmettre à chaque fois pour un flux donné. Cette option devrait être utilisée pour éviter de transmettre une quantité trop faible de données, afin de réduire la charge du processeur. Elle doit être définie avec soin. Une valeur trop faible peut augmenter la charge du processeur. Une valeur trop élevée peut augmenter la latence. Elle est également fortement liée à la limite de débit définie. Si elle est trop proche de la limite de débit, des pauses peuvent survenir afin de ne pas dépasser la limite, car trop d’octets seraient consommés à chaque fois. Elle dépend fortement de la configuration du filtre. Une bonne approche consiste à commencer par une valeur d’environ 2 fois la taille maximale d’un segment TCP (MSS), généralement 2896 octets, puis à l’ajuster après quelques expérimentations.

Exemple :

```text
frontend http
    bind *:80
    mode http

    # If this filter is enabled, the stream will share the download limit
    # of 10m/s with all other streams with the same source address.
    filter bwlim-out limit-by-src key src table limit-by-src limit 10m

    # If this filter is enabled, the stream will be limited to download at 1m/s,
    # independently of all other streams.
    filter bwlim-out limit-by-strm default-limit 1m default-period 1s

    # Limit all streams to 1m/s (the default limit) and those accessing the
    # internal API to 100k/s. Limit each source address to 10m/s. The shared
    # limit is applied first. Both are limiting the download rate.
    http-request set-bandwidth-limit limit-by-strm
    http-request set-bandwidth-limit limit-by-strm limit 100k if { path_beg /internal }
    http-request set-bandwidth-limit limit-by-src
    ...

backend limit-by-src
    # The stickiness table used by <limit-by-src> filter
    stick-table type ip size 1m expire 3600s store bytes_out_rate(1s)
```

Voir également : « tcp-request content set-bandwidth-limit », « tcp-response content set-bandwidth-limit »,
« http-request set-bandwidth-limit » et « http-response set-bandwidth-limit ».
