---
title: "6. Gestion de la mémoire"
linkTitle: "6. Mémoire"
weight: 300
description: "Allocation mémoire, limites, pools, tampons et dimensionnement des processus"
icon: fa-solid fa-memory
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/memory/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 6"
---

HAProxy utilise une gestion mémoire basée sur des pools, simple et rapide. Étant donné qu’il repose sur un nombre réduit de types d’objets différents, il est bien plus efficace de tirer de nouveaux objets depuis un pool déjà contenant des objets de la taille appropriée que d’appeler malloc() pour chaque taille différente. Les pools sont organisés selon une structure de pile ou LIFO, de sorte que les objets nouvellement alloués proviennent d’objets récemment libérés, encore présents dans les caches CPU. Les pools de tailles similaires sont regroupés afin de limiter la fragmentation mémoire.

Par défaut, le focus étant mis sur les performances, chaque objet libéré est remis dans le pool d’où il provient, et les objets alloués ne sont jamais libérés, car ils sont censés être réutilisés très bientôt.

Depuis la CLI, il est possible de vérifier l'utilisation de la mémoire dans les pools grâce à la commande « show pools » :

```shell
> show pools
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool cache_st (16 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccc40=03 [SHARED]
  - Pool pipe (32 bytes): 5 allocated (160 bytes), 5 used, 0 failures, 2 users, @0x9ccac0=00 [SHARED]
  - Pool comp_state (48 bytes): 3 allocated (144 bytes), 3 used, 0 failures, 5 users, @0x9cccc0=04 [SHARED]
  - Pool filter (64 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 3 users, @0x9ccbc0=02 [SHARED]
  - Pool vars (80 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccb40=01 [SHARED]
  - Pool uniqueid (128 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9cd240=15 [SHARED]
  - Pool task (144 bytes): 55 allocated (7920 bytes), 55 used, 0 failures, 1 users, @0x9cd040=11 [SHARED]
  - Pool session (160 bytes): 1 allocated (160 bytes), 1 used, 0 failures, 1 users, @0x9cd140=13 [SHARED]
  - Pool h2s (208 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccec0=08 [SHARED]
  - Pool h2c (288 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cce40=07 [SHARED]
  - Pool spoe_ctx (304 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccf40=09 [SHARED]
  - Pool connection (400 bytes): 2 allocated (800 bytes), 2 used, 0 failures, 1 users, @0x9cd1c0=14 [SHARED]
  - Pool hdr_idx (416 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd340=17 [SHARED]
  - Pool dns_resolut (480 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccdc0=06 [SHARED]
  - Pool dns_answer_ (576 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccd40=05 [SHARED]
  - Pool stream (960 bytes): 1 allocated (960 bytes), 1 used, 0 failures, 1 users, @0x9cd0c0=12 [SHARED]
  - Pool requri (1024 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd2c0=16 [SHARED]
  - Pool buffer (8030 bytes): 3 allocated (24090 bytes), 2 used, 0 failures, 1 users, @0x9cd3c0=18 [SHARED]
  - Pool trash (8062 bytes): 1 allocated (8062 bytes), 1 used, 0 failures, 1 users, @0x9cd440=19
Total: 19 pools, 42296 bytes allocated, 34266 used.
```

Le nom du pool n'est qu'indicatif : il correspond au nom du premier type d'objet utilisant ce pool. La taille entre parenthèses est la taille des objets dans ce pool. Les tailles d'objets sont toujours arrondies par excès au multiple de 16 octets le plus proche. Le nombre d'objets actuellement alloués et le nombre équivalent d'octets sont indiqués afin de faciliter l'identification du pool responsable de la plus forte utilisation mémoire. Le nombre d'objets actuellement en cours d'utilisation est également indiqué dans le champ « used ». La différence entre « allocated » et « used » correspond aux objets qui ont été libérés et sont disponibles pour une utilisation immédiate. L'adresse en fin de ligne est l'adresse du pool, et le nombre suivant est l'indice du pool lorsqu'il existe, ou est indiqué comme -1 si aucun indice n'a été attribué.

Il est possible de limiter la quantité de mémoire allouée par processus à l'aide de l'option en ligne de commande "-m", suivie d'un nombre de mégaoctets. Cette limite s'applique à l'ensemble de l'espace adressable du processus, ce qui inclut la mémoire utilisée par certaines bibliothèques ainsi que la pile, mais constitue une limite fiable lors de la construction d'un système à ressources contraintes. Elle fonctionne de la même manière que "ulimit -v" sur les systèmes qui la supportent, ou "ulimit -d" sur les autres.

Si une allocation mémoire échoue en raison d'un dépassement de la limite mémoire ou du fait que le système ne dispose pas de suffisamment de mémoire, HAProxy commencera d'abord par libérer tous les objets disponibles de tous les pools avant de tenter une nouvelle allocation mémoire. Ce mécanisme de libération de la mémoire inutilisée peut être déclenché en envoyant le signal SIGQUIT au processus HAProxy.

Pendant une opération de rechargement, le processus basculé en état d’arrêt progressif effectue également automatiquement certains vidages après avoir libéré chaque connexion, afin de libérer toute la mémoire possible et de la préserver pour le nouveau processus.
