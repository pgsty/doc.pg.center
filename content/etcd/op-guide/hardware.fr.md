---
title: Recommandations matérielles
weight: 4400
description: "Guidelines matériels pour l'administration des clusters etcd"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/hardware.md"
---

etcd fonctionne généralement correctement avec des ressources limitées à des fins de développement ou de test ; il est courant de développer avec etcd sur un ordinateur portable ou une machine cloud peu coûteuse. Toutefois, lors de l'exécution de clusters etcd en production, certaines recommandations matérielles sont utiles pour une administration appropriée. Ces suggestions ne sont pas des règles strictes ; elles constituent un bon point de départ pour un déploiement productif robuste. Comme toujours, les déploiements doivent être testés avec des charges simulées avant d’être mis en production.

## Processeurs {#cpus}

Peu de déploiements etcd nécessitent une grande capacité CPU. Les clusters typiques ont besoin de deux à quatre cœurs pour fonctionner correctement.
Les déploiements etcd très chargés, qui servent des milliers de clients ou des dizaines de milliers de requêtes par seconde, sont généralement limités par la CPU, car etcd peut servir les requêtes depuis la mémoire. De tels déploiements nécessitent généralement huit à seize cœurs dédiés.


## Mémoire {#memory}

etcd présente une empreinte mémoire relativement faible, mais ses performances dépendent néanmoins d'une quantité suffisante de mémoire. Un serveur etcd met en cache de manière agressive les données clé-valeur et consacre la majeure partie de sa mémoire restante à la surveillance des observateurs. En général, 8 Go sont suffisants. Pour les déploiements intensifs comportant des milliers d'observateurs et des millions de clés, allouez entre 16 Go et 64 Go de mémoire selon les besoins.


## Disques {#disks}

Les disques rapides constituent le facteur le plus critique pour les performances et la stabilité du déploiement etcd.

Un disque lent augmentera la latence des requêtes etcd et pourrait compromettre la stabilité du cluster. Étant donné que le protocole de consensus d'etcd dépend du stockage persistant des métadonnées dans un journal, une majorité des membres du cluster etcd doit écrire chaque requête sur le disque. En outre, etcd effectue également des points de contrôle incrémentiels de son état sur le disque afin de tronquer ce journal. Si ces écritures prennent trop de temps, les battements de cœur pourraient expirer et déclencher une élection, ce qui affaiblit la stabilité du cluster. En général, pour déterminer si un disque est suffisamment rapide pour etcd, un outil de benchmark tel que [fio][fio] peut être utilisé. Lisez [ici][fio-blog-post] pour un exemple.

etcd est très sensible à la latence d'écriture disque. Une capacité d'au moins 50 IOPS séquentielles (par exemple, un disque dur 7200 RPM) est généralement requise. Pour les clusters fortement sollicités, une capacité de 500 IOPS séquentielles (par exemple, un SSD local typique ou un périphérique de bloc virtuel à haute performance) est recommandée. Notez que la plupart des fournisseurs de cloud publient des IOPS concurrents plutôt que séquentiels ; les IOPS concurrents publiés peuvent être jusqu'à 10 fois supérieurs aux IOPS séquentiels. Pour mesurer les IOPS séquentiels réels, nous recommandons d'utiliser un outil de benchmark disque tel que [diskbench][diskbench] ou [fio][fio].

etcd nécessite uniquement une bande passante disque modeste, mais une bande passante disque plus élevée permet des temps de récupération plus rapides lorsque membre défaillant doit rattraper le cluster. En général, 10MB/s peut récupérer 100 Mo de données en 15 secondes. Pour les clusters de grande taille, 100MB/s ou supérieur est recommandé pour récupérer 1 Go de données en 15 secondes.

Lorsqu’il est possible, sauvegardez le stockage d’etcd avec un SSD. Un SSD offre généralement des latences d’écriture plus faibles et une variation moindre qu’un disque dur rotatif, ce qui améliore la stabilité et la fiabilité d’etcd. Si vous utilisez un disque dur rotatif, choisissez les disques les plus rapides disponibles (15 000 tr/min). L’utilisation du RAID 0 est également une méthode efficace pour augmenter la vitesse du disque, que ce soit pour les disques rotatifs ou les SSD. Avec au moins trois membres dans le cluster, les variantes de RAID avec miroir et/ou parité sont inutiles ; la réplication cohérente d’etcd assure déjà une haute disponibilité.


## Réseau {#network}

Les déploiements etcd à plusieurs membres bénéficient d’un réseau rapide et fiable. Afin que etcd soit à la fois cohérent et tolérant aux partitions, un réseau instable présentant des coupures de partition entraînera une disponibilité médiocre. Une faible latence garantit que les membres etcd peuvent communiquer rapidement. Un débit élevé permet de réduire le temps de récupération d’un membre etcd défaillant. Un réseau 1GbE est suffisant pour les déploiements courants de etcd. Pour les grands clusters etcd, un réseau 10GbE réduit le temps moyen de récupération.

Déployez les membres etcd au sein d’un même centre de données lorsque cela est possible, afin d’éviter les surcharges de latence et de réduire la probabilité d’événements de partitionnement. Si un domaine de défaillance dans un autre centre de données est nécessaire, choisissez un centre de données plus proche de celui déjà en place. Veuillez également consulter la documentation [tuning][tuning] pour plus d’informations sur le déploiement à travers des centres de données.


## Exemples de configurations matériels {#example-hardware-configurations}

Voici quelques exemples de configurations matériels sur les environnements AWS et GCE. Comme mentionné précédemment, mais doit être souligné malgré tout, les administrateurs doivent tester un déploiement etcd avec une charge de travail simulée avant de le mettre en production.

Notez que ces configurations supposent que ces machines sont entièrement dédiées à etcd. Exécuter d'autres applications en parallèle sur ces machines peut entraîner des conflits de ressources et provoquer une instabilité du cluster.

### Petit cluster {#small-cluster}

Un petit cluster gère moins de 100 clients, moins de 200 requêtes par seconde et stocke au plus 100 Mo de données.

Exemple de charge de travail d'application : un cluster Kubernetes à 50 nœuds

| Fournisseur | Type | vCPUs | Mémoire (Go) | IOPS concurrents max | Bande passante disque (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.large | 2 | 8 | 3600 | 56,25 |
| GCE | n1-standard-2 + 50Go PD SSD | 2 | 7,5 | 1500 | 25 |


### Cluster de taille moyenne {#medium-cluster}

Un cluster de taille moyenne prend en charge moins de 500 clients, moins de 1 000 requêtes par seconde et stocke au plus 500 Mo de données.

Exemple de charge de travail d'application : un cluster Kubernetes de 250 nœuds

| Fournisseur | Type | vCPUs | Mémoire (Go) | IOPS concurrents max | Bande passante disque (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.xlarge | 4 | 16 | 6000 | 93,75 |
| GCE | n1-standard-4 + 150Go PD SSD | 4 | 15 | 4500 | 75 |


### Grand cluster {#large-cluster}

Un cluster important sert moins de 1 500 clients, moins de 10 000 requêtes par seconde, et stocke au plus 1 Go de données.

Exemple de charge de travail d'application : un cluster Kubernetes de 1 000 nœuds

| Fournisseur | Type | vCPUs | Mémoire (Go) | IOPS simultanés max | Bande passante disque (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.2xlarge | 8 | 32 | 8000 | 125 |
| GCE | n1-standard-8 + 250Go PD SSD | 8 | 30 | 7500 | 125 |


### cluster xLarge {#xlarge-cluster}

Un cluster xLarge prend en charge plus de 1 500 clients, plus de 10 000 requêtes par seconde et stocke plus de 1 Go de données.

Exemple de charge de travail d'application : un cluster Kubernetes de 3 000 nœuds

| Fournisseur | Type | vCPUs | Mémoire (Go) | IOPS simultanés max | Bande passante disque (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.4xlarge | 16 | 64 | 16 000 | 250 |
| GCE | n1-standard-16 + 500Go PD SSD | 16 | 60 | 15 000 | 250 |


[diskbench]: https://github.com/ongardie/diskbenchmark
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[tuning]: /fr/etcd/tuning/
