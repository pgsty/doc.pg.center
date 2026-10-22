---
title: "Produits complémentaires et alternatives"
linkTitle: "Écosystème"
weight: 90
description: "Comment HAProxy s'inscrit parmi Apache, NGINX, Varnish, LVS, Envoy et d'autres répartiteurs de charge"
icon: fa-solid fa-puzzle-piece
module: [HAPROXY]
categories: [Concept]
aliases:
  - /haproxy/intro/ecosystem/
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
upstream_name: "HAProxy 3.4 Starter Guide"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, sections 4–4.4"
---

HAProxy s'intègre assez bien avec certains produits listés ci-dessous, ce qui justifie leur mention ici, même s'ils ne sont pas directement liés à HAProxy.

## 4.1. Serveur HTTP Apache {#section-4-1}

Apache est le serveur HTTP de facto. Il s'agit d'un projet très complet et modulaire, capable de servir des fichiers ainsi que du contenu dynamique. Il peut servir de frontal pour certains serveurs d'applications. Il peut même faire office de proxy pour les requêtes et mettre les réponses en cache. Dans tous ces cas d'utilisation, un répartiteur de charge frontal est généralement nécessaire. Apache peut fonctionner dans divers modes, certains étant plus lourds que d'autres. Certains modules nécessitent encore le modèle pré-forké plus lourd, ce qui empêche Apache de bien monter en charge avec un grand nombre de connexions. Dans ce cas, HAProxy peut apporter une aide considérable en imposant des limites de connexion par serveur à une valeur sûre, ce qui accélérera significativement le serveur et préservera ses ressources, qui seront mieux utilisées par l'application.

Apache peut extraire l'adresse du client à partir de l'en-tête X-Forwarded-For en utilisant l'extension "mod_rpaf". HAProxy alimente automatiquement cet en-tête lorsque l'option forwardfor est spécifiée dans sa configuration. HAProxy peut également offrir une bonne protection à Apache lorsqu'il est exposé à internet, où il résistera mieux à un grand nombre de types d'attaques DoS.

## 4.2. NGINX {#section-4-2}

NGINX est le second serveur HTTP de facto. Comme Apache, il couvre un large éventail de fonctionnalités. Conçu selon un modèle similaire à HAProxy, il gère sans difficulté des dizaines de milliers de connexions simultanées. Lorsqu'il sert de passerelle vers des applications, par exemple avec le PHP FPM inclus, il peut souvent être bénéfique de mettre en place une limitation des connexions en frontal afin de réduire la charge sur l'application PHP. HAProxy sera clairement utile à la fois comme répartiteur de charge classique et comme régulateur de trafic pour accélérer PHP en le désengorgeant. Comme ces produits consomment très peu de CPU grâce à leur architecture événementielle, il est souvent facile d'installer HAProxy et NGINX sur le même système. NGINX implémente le protocole PROXY de HAProxy ; HAProxy peut donc lui transmettre les informations de connexion du client afin que l'application dispose de toutes les informations pertinentes. Des benchmarks ont aussi montré que, pour servir de gros fichiers statiques, un hachage cohérent dans HAProxy devant NGINX peut améliorer le taux de succès du cache du système d'exploitation, qui est essentiellement multiplié par le nombre de nœuds serveurs.

## 4.3. Varnish {#section-4-3}

Varnish est un proxy inverse intelligent doté d'un cache, probablement mieux décrit comme un accélérateur d'applications web.
Varnish n'implémente pas SSL/TLS et souhaite consacrer l'intégralité de ses cycles processeur à ce qu'il fait le mieux.
Varnish implémente également le protocole PROXY d'HAProxy, de sorte qu'HAProxy peut être déployé très facilement devant Varnish en tant qu'offloader SSL ainsi qu'en tant que répartiteur de charge, tout en transmettant à Varnish toutes les informations pertinentes relatives au client.
Varnish prend naturellement en charge la décompression depuis le cache lorsqu'un serveur a fourni un objet compressé, mais ne compresse pas lui-même.
HAProxy peut alors être utilisé pour compresser les données sortantes lorsque les serveurs backend ne mettent pas en œuvre la compression, bien qu'il soit rarement une bonne idée de compresser sur le répartiteur de charge, sauf si le trafic est faible.

Lors de la mise en place de fermes de mise en cache étendues sur plusieurs nœuds, HAProxy peut utiliser le hachage URL cohérent pour répartir intelligemment la charge sur les nœuds de mise en cache et éviter la duplication de cache, ce qui permet d’obtenir une taille totale de cache égale à la somme de celles de tous les nœuds de mise en cache. En outre, la mise en cache de très petits objets bruts pendant une courte durée sur HAProxy peut parfois permettre d’éviter des allers-retours réseau et de réduire la charge CPU sur les nœuds HAProxy et Varnish. Cela n’est possible que si aucune opération n’est effectuée sur ces objets sur Varnish (cette notion est souvent désignée sous le terme de « cache favicon », par laquelle un pourcentage important de requêtes inutiles en aval peut parfois être évité). Toutefois, n'activez pas la mise en cache HAProxy pendant une longue durée (plus de quelques secondes) devant n'importe quel autre cache, car cela compliquerait considérablement le dépannage sans apporter de gains réellement significatifs.

## 4.4. Alternatives {#section-4-4}

Le répartiteur de charge Linux Virtual Server (LVS ou IPVS) est un répartiteur de charge au niveau 4 intégré au noyau Linux. Il fonctionne au niveau des paquets et gère TCP et UDP. Dans la plupart des cas, il s'agit davantage d'un complément que d'une alternative, car il ne possède aucune connaissance au niveau 7.

Pound est un autre répartiteur de charge bien connu. Il est beaucoup plus simple et offre nettement moins de fonctionnalités que HAProxy, mais Pound comme HAProxy peuvent convenir à de nombreuses configurations élémentaires. Son auteur a toujours privilégié l'auditabilité du code et souhaite conserver un ensemble restreint de fonctionnalités. Son architecture à base de threads passe moins bien à l'échelle avec un grand nombre de connexions, mais c'est un bon produit.

Pen est un répartiteur de charge relativement léger. Il prend en charge le SSL, maintient la persistance grâce à une table de taille fixe contenant les adresses IP de ses clients. Il prend en charge un mode orienté paquets, permettant de supporter le retour direct du serveur et le UDP dans une certaine mesure. Il est destiné à des charges faibles (la table de persistance ne comporte que 2048 entrées).

NGINX peut effectuer une répartition de charge à certains égards, bien qu’il ne s’agisse clairement pas de sa fonction principale.
Le trafic de production sert à détecter les défaillances de serveur, les algorithmes de répartition de charge sont plus limités, et la persistance est très limitée. Toutefois, cela peut avoir un sens dans certains scénarios de déploiement simples où NGINX est déjà présent. Le point positif est qu’étant donné son intégration très fluide avec HAProxy, il n’y a rien de mal à ajouter HAProxy ultérieurement lorsque les limites de NGINX ont été atteintes.

Varnish effectue également une répartition de charge sur ses serveurs backend et prend en charge des contrôles d'état réels. Il ne met toutefois pas en œuvre la persistance, de sorte qu’à l’instar de NGINX, cela peut suffire pour démarrer, tant que la persistance n'est pas nécessaire. De même, puisque HAProxy et Varnish s’intègrent si bien, il est facile d'ajouter HAProxy ultérieurement à l'ensemble afin de compléter les fonctionnalités offertes.
