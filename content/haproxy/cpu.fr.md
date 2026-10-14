---
title: "7. Utilisation du CPU"
linkTitle: "7. CPU"
weight: 310
description: "Threads, affinité CPU, saturation, profilage et comportement des performances"
icon: fa-solid fa-microchip
module: [HAPROXY]
categories: [Tâche]
aliases:
  - /haproxy/management/cpu/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 7"
---

> [!WARNING]
> Note de version : ce chapitre conserve des conseils historiques sur le fonctionnement multiprocessus. Depuis HAProxy 2.5, `nbproc` et `bind process` ne sont plus pris en charge. Pour cette édition, configurez les threads avec `nbthread`, `thread-groups` et `cpu-map` dans les [paramètres globaux](/fr/haproxy/global/#section-3-1).

HAProxy passe normalement la majeure partie de son temps en mode noyau et une part plus faible en mode utilisateur. Un processeur 3,5 GHz correctement optimisé peut supporter un débit d’environ 80 000 établissements et fermetures de connexions bout-en-bout par seconde à 100 % d’utilisation sur un seul cœur. Lorsqu’un cœur est saturé, les valeurs typiques sont :

- 95 % système, 5 % utilisateur pour des connexions TCP longues ou de grands objets HTTP
- 85 % système et 15 % utilisateur pour des connexions TCP courtes ou de petits objets HTTP en mode fermé
- 70 % système et 30 % utilisateur pour de petits objets HTTP en mode keep-alive

Le nombre de règles traitées et d'expressions régulières augmente la partie en espace utilisateur. La présence de règles de pare-feu, du suivi des connexions et de tables de routage complexes dans le système augmente quant à elle la partie noyau.

Sur la plupart des systèmes, le temps CPU observé lors des transferts réseau peut être divisé en 4 parties :

- la partie d'interruption, qui concerne tout traitement effectué lors de la réception d'E/S, avant même que le processus cible ne soit connu. En général, les paquets Rx sont comptabilisés dans l'interruption. Sur certains systèmes, comme Linux, où le traitement d'interruption peut être différé vers un thread dédié, celui-ci peut apparaître sous la forme d'un softirq, et le thread s'appelle ksoftirqd/0 (pour le CPU 0). Le CPU chargé de cette charge est généralement défini par les paramètres matériels, bien qu'en cas de softirq il soit souvent possible de rediriger le traitement vers un autre CPU. Cette partie d'interruption est souvent perçue comme parasite, car elle n'est associée à aucun processus, mais elle correspond en réalité à un traitement effectué pour préparer le travail du processus.

- la partie système, qui concerne tout traitement effectué à l’aide de code noyau appelé depuis l’espace utilisateur.
    Les appels système sont comptabilisés comme du temps système, par exemple. Tous les paquets Tx livrés de manière synchrone seront comptabilisés comme du temps système. Si certains paquets doivent être différés en raison de la saturation des files d’attente, ils pourront être traités ultérieurement dans le contexte d’interruption (par exemple : à la réception d’un ACK ouvrant une fenêtre TCP).

-  la partie utilisateur, qui exécute exclusivement du code d'application en espace utilisateur. HAProxy s'exécute exclusivement dans cette partie, bien qu'il utilise abondamment les appels système. Le traitement des règles, les expressions régulières, la compression et le chiffrement ajoutent à la consommation de CPU attribuée à la partie utilisateur.

- la partie inactive, c'est-à-dire ce que fait le processeur lorsqu'il n'a rien à faire. Par exemple, HAProxy attend qu'une connexion entrante arrive, ou attend qu'une donnée soit envoyée, ce qui signifie que le système attend un accusé de réception (ACK) du client pour transmettre ces données.

En pratique, concernant l'activité d'HAProxy, il est généralement raisonnable (mais totalement inexact) de considérer que les interruptions/softirq sont dues au traitement Rx dans les pilotes noyau, que le temps utilisateur est dû au traitement au niveau 7 dans HAProxy, et que le temps système est dû au traitement réseau sur le chemin Tx.

Étant donné que HAProxy s'exécute autour d'une boucle d'événements, il attend de nouveaux événements à l'aide de poll() (ou d'une alternative quelconque) et traite tous ces événements aussi rapidement que possible avant de retourner à poll() pour attendre de nouveaux événements. Il mesure le temps passé en attente dans poll() par rapport au temps consacré au traitement des événements. Le rapport entre le temps passé en attente et le temps total est appelé le temps « idle », c'est-à-dire la durée passée à attendre qu'une action se produise. Ce rapport est affiché dans la page de statistiques sur la ligne « idle », ou « Idle_pct » sur la CLI. Lorsqu'il est proche de 100 %, cela signifie que la charge est extrêmement faible. Lorsqu'il est proche de 0 %, cela indique qu'il y a constamment une activité. Bien qu'il ne puisse pas être très précis sur un système surchargé en raison de la préemption éventuelle du processeur par d'autres processus, il fournit tout de même une bonne estimation de la façon dont HAProxy considère qu'il travaille : si la charge est faible et que le taux d'« idle » est également faible, cela peut indiquer que HAProxy a beaucoup de travail à accomplir, probablement à cause de règles très coûteuses à traiter. À l'inverse, si HAProxy indique un taux d'« idle » proche de 100 % alors que les performances sont lentes, cela signifie qu'il ne peut rien faire pour accélérer les choses car il attend déjà des données entrantes à traiter. Dans l'exemple ci-dessous, HAProxy est complètement inactif :

```shell
$ echo "show info" | socat - /var/run/haproxy.sock | grep ^Idle
Idle_pct: 100
```

Lorsque le taux d'inactivité commence à devenir très faible, il est important de régler le système et de positionner correctement les processus et les interruptions afin de préserver au maximum les ressources CPU pour toutes les tâches. Si un pare-feu est présent, il peut être utile d’essayer de le désactiver ou de le configurer pour s’assurer qu’il n’est pas à l’origine d’une grande partie de la limitation des performances. Il convient de noter que le déchargement d’un pare-feu étatique réduit généralement à la fois le nombre d’interruptions/softirq et l’utilisation du système, car de tels pare-feux agissent à la fois sur les chemins Rx et Tx. Sous Linux, le déchargement des modules nf_conntrack et ip_conntrack permettra de vérifier s’il y a un gain à tirer. Si tel est le cas, le module fonctionne avec les paramètres par défaut, et il faudra déterminer comment le configurer pour une meilleure performance. En général, cela consiste à augmenter considérablement la taille du tableau de hachage. Sous FreeBSD, la commande "pfctl -d" désactive à la fois le pare-feu "pf" et son moteur étatique.

Si une grande partie du temps est consacrée aux interruptions et softirq, assurez-vous qu'elles ne s'exécutent pas sur le même processeur. La plupart des systèmes fixent les tâches sur le processeur qui reçoit le trafic réseau, car cela améliore certaines charges. Pour les charges très liées au réseau, c'est l'inverse : le processus HAProxy devra se battre contre son homologue côté noyau. Fixer HAProxy sur un cœur et les interruptions sur un autre, partageant le même cache L3, a tendance à augmenter sensiblement les performances réseau. En pratique, HAProxy et la pile réseau ont des quantités de travail proches et peuvent presque saturer chacun un cœur. Sous Linux, utilisez taskset pour HAProxy ou cpu-map dans sa configuration ; les interruptions sont affectées sous /proc/irq. De nombreuses interfaces réseau prennent en charge plusieurs files et interruptions. Il est généralement utile de les répartir sur un petit nombre de cœurs, à condition qu'ils partagent tous le même cache L3. Veuillez toujours arrêter irq_balance, qui fait toujours le pire possible sur de telles charges.

Pour les charges de travail intensives en CPU, telles que de nombreuses connexions SSL ou une compression importante, il peut être pertinent d'utiliser plusieurs processus dédiés à certaines tâches, bien qu'aucune règle universelle ne s'applique ici et qu'une expérimentation s'impose.

Afin d'augmenter la capacité du processeur, il est possible de faire exécuter HAProxy en plusieurs processus, en utilisant la directive « nbproc » dans la section globale. Toutefois, certaines limitations s'appliquent :

- Les contrôles d'état sont exécutés par processus, les serveurs cibles reçoivent donc autant de contrôles qu'il y a de processus en cours d'exécution ;
- Les valeurs maxconn et les files d'attente sont par processus, il faut donc définir la valeur correcte afin d'éviter de surcharger les serveurs ;
- Les connexions sortantes devraient éviter d'utiliser des plages de ports pour éviter les conflits ;
- Les tables de persistance sont par processus et ne sont pas partagées entre les processus ;
- Chaque section peers ne peut être exécutée que sur un seul processus à la fois ;
- Les opérations en ligne de commande n'agissent que sur un seul processus à la fois.

En gardant cela à l'esprit, la configuration la plus simple consiste souvent à faire fonctionner une première couche sur plusieurs processus, chargée du traitement intensif, qui transfère le trafic vers une deuxième couche exécutée dans un seul processus. Ce mécanisme convient particulièrement au chiffrement SSL et à la compression, qui sont les deux fonctionnalités les plus exigeantes en ressources CPU. Les instances peuvent facilement être chaînées via des sockets UNIX (plus économiques que les sockets TCP et qui ne gaspillent pas de ports), ainsi que via le protocole PROXY, utile pour transmettre les informations client à l'étape suivante. Lors de cette configuration, il est généralement judicieux de lier toutes les tâches mono-processus au processus numéro 1, et les tâches supplémentaires aux processus suivants, afin de faciliter la génération de configurations similaires pour différentes machines.

Sur les versions Linux 3.9 et ultérieures, exécuter HAProxy en mode multi-processus est beaucoup plus efficace lorsque chaque processus utilise un socket d'écoute distinct sur le même IP:port ; cela permet au noyau de répartir uniformément la charge entre tous les processus au lieu de les réveiller tous. Veuillez consulter l’option « process » des lignes de mot-clé « bind » dans le manuel de configuration pour plus d’informations.
