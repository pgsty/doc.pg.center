---
title: FAQ
weight: 1200
description: Questions fréquemment posées
icon: fa-solid fa-circle-question
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/faq.md"
---

## etcd, général {#etcd-general}

### Qu'est-ce qu'etcd ? {#what-is-etcd}

etcd est un magasin clé-valeur distribué cohérent, principalement utilisé comme service de coordination indépendant dans les systèmes distribués. Il est conçu pour stocker de petites quantités de données pouvant tenir entièrement en mémoire.

### Comment prononce-t-on etcd ? {#how-do-you-pronounce-etcd}

etcd se prononce **/ˈɛtsiːdiː/** et signifie « répertoire `etc` distribué ».

### Les clients doivent-ils envoyer des requêtes au leader etcd ? {#do-clients-have-to-send-requests-to-the-etcd-leader}

[Raft][raft] est basé sur un leader ; le leader gère toutes les requêtes clients nécessitant un consensus au sein du cluster. Toutefois, le client n’a pas besoin de savoir quel nœud est le leader. Toute requête nécessitant un consensus envoyée à un suiveur est automatiquement redirigée vers le leader. Les requêtes ne nécessitant pas de consensus (par exemple, les lectures sérialisables) peuvent être traitées par n’importe quel membre du cluster.

## Configuration {#configuration}

### Quelle est la différence entre listen-<client,peer>-urls, advertise-client-urls et initial-advertise-peer-urls ? {#what-is-the-difference-between-listen-clientpeer-urls-advertise-client-urls-or-initial-advertise-peer-urls}

`listen-client-urls` et `listen-peer-urls` spécifient les adresses locales auxquelles le serveur etcd se lie pour accepter les connexions entrantes. Pour écouter sur un port pour toutes les interfaces, spécifiez `0.0.0.0` comme adresse IP d'écoute.

`advertise-client-urls` et `initial-advertise-peer-urls` spécifient les adresses que les clients etcd ou d'autres membres etcd doivent utiliser pour contacter le serveur etcd. Les adresses annoncées doivent être accessibles depuis les machines distantes. Ne pas annoncer d'adresses telles que `localhost` ou `0.0.0.0` dans une configuration de production, car ces adresses sont inaccessibles depuis les machines distantes.

### Pourquoi la modification de `--listen-peer-urls` ou `--initial-advertise-peer-urls` ne met-elle pas à jour les URL de pair annoncées dans `etcdctl member list` ? {#why-doesnt-changing---listen-peer-urls-or---initial-advertise-peer-urls-update-the-advertised-peer-urls-in-etcdctl-member-list}

Les URL de pair annoncées par un membre proviennent de `--initial-advertise-peer-urls` lors du démarrage initial du cluster. Modifier les URL d’écoute des pairs ou les URL initiales de pair annoncées après le démarrage du membre n'affecte pas les URL de pair annoncées, car les modifications doivent passer par le quorum afin d'éviter une divergence de la configuration d’appartenance (split brain). Utilisez `etcdctl member update` pour mettre à jour les URL de pair d'un membre.

## Déploiement {#deployment}

### Exigences système {#system-requirements}

Étant donné qu’etcd écrit des données sur le disque, ses performances dépendent fortement de la performance du disque. Un disque SSD est donc fortement recommandé. Pour évaluer si un disque est suffisamment rapide pour etcd, une possibilité consiste à utiliser un outil de benchmark disque tel que [fio][fio]. Pour un exemple de mise en œuvre, consultez [ici][fio-blog-post]. Afin d’éviter une dégradation des performances ou une surcharge involontaire du magasin clé-valeur, etcd impose un quota de taille de stockage configurable, fixé par défaut à 2 Go. Pour éviter l’utilisation du swap ou la pénurie de mémoire, la machine devrait disposer d’au moins autant de RAM que le quota. Un quota de stockage maximal de 8 Go est suggéré pour les environnements normaux, et etcd émet un avertissement au démarrage si la valeur configurée dépasse cette limite. Chez CoreOS, un cluster etcd est généralement déployé sur des machines dédiées CoreOS Container Linux dotées d’un processeur à deux cœurs, de 2 Go de RAM et d’un SSD de 80 Go *au minimum*. **Notez que les performances dépendent intrinsèquement de la charge ; testez avant un déploiement en production**. Consultez les recommandations sur le [matériel][hardware-setup].

L’environnement de production le plus stable est le système d’exploitation Linux avec l’architecture amd64 ; consultez [plateforme prise en charge][supported-platform] pour plus d’informations.

### Pourquoi un nombre impair de membres dans un cluster ? {#why-an-odd-number-of-cluster-members}

Un cluster etcd nécessite une majorité de nœuds, un quorum, pour s'accorder sur les mises à jour de l'état du cluster. Pour un cluster composé de n membres, le quorum est égal à (n/2)+1. Pour tout cluster de taille impaire, l'ajout d'un nœud augmente toujours le nombre de nœuds nécessaires au quorum. Bien qu'ajouter un nœud à un cluster de taille impaire semble améliorer la situation en augmentant le nombre de machines, la tolérance aux pannes est en réalité moindre, car exactement le même nombre de nœuds peut tomber en panne sans perdre le quorum, tout en augmentant le nombre de nœuds susceptibles de tomber en panne. Si le cluster se trouve dans un état où il ne peut plus tolérer de pannes supplémentaires, ajouter un nœud avant de supprimer des nœuds est dangereux, car si le nouveau nœud ne parvient pas à s'enregistrer dans le cluster (par exemple, en raison d'une mauvaise configuration de l'adresse), le quorum sera perdu de manière permanente.

### Quelle est la taille maximale d'un cluster ? {#what-is-maximum-cluster-size}

Théoriquement, il n’existe aucune limite rigide. Toutefois, un cluster etcd devrait normalement comporter au plus sept nœuds. [Le service de verrouillage Google Chubby][chubby], similaire à etcd et largement déployé au sein de Google depuis de nombreuses années, recommande de fonctionner avec cinq nœuds. Un cluster etcd à cinq membres peut tolérer deux défaillances de membres, ce qui suffit dans la plupart des cas. Bien qu’un cluster plus grand offre une meilleure tolérance aux pannes, les performances d’écriture se dégradent en raison de la réplication des données sur un plus grand nombre de machines.

### Qu'est-ce que la tolérance aux pannes ? {#what-is-failure-tolerance}

Un cluster etcd fonctionne tant qu’un quorum de membres peut être établi. Si le quorum est perdu à cause de pannes réseau transitoires (par exemple, des partitions), etcd reprend automatiquement et en toute sécurité une fois le réseau restauré et le quorum rétabli ; Raft garantit la cohérence du cluster. En cas de perte de courant, etcd persiste le journal Raft sur le disque ; etcd rejoue le journal jusqu’au point de panne et reprend sa participation au cluster. En cas de panne matérielle permanente, le nœud peut être retiré du cluster par [reconfiguration en cours d’exécution][runtime reconfiguration].

Il est recommandé d’avoir un nombre impair de membres dans un cluster. Un cluster de taille impaire tolère autant de défaillances qu’un cluster de taille paire, mais avec moins de nœuds. Cette différence apparaît en comparant des clusters de taille paire et impaire :

| Taille du cluster | Majorité | Tolérance aux pannes |
|:-:|:-:|:-:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

Ajouter un membre pour porter la taille du cluster à un nombre pair ne procure pas de tolérance aux pannes supplémentaire. De même, lors d’une partition du réseau en deux, un nombre impair de membres garantit qu'il y aura toujours une partition majoritaire capable de continuer à fonctionner et de servir de source de vérité lorsque la partition prendra fin.

### etcd fonctionne-t-il dans des déploiements inter-régions ou inter-centres de données ? {#does-etcd-work-in-cross-region-or-cross-data-center-deployments}

Déployer etcd sur plusieurs régions améliore la tolérance aux pannes d’etcd, car les membres sont répartis dans des domaines de défaillance distincts. Le coût est une latence accrue pour les requêtes de consensus dues au franchissement des limites des centres de données. Étant donné qu’etcd repose sur un quorum de membres pour atteindre le consensus, la latence liée au franchissement des centres de données sera plus marquée, car au moins la majorité des membres du cluster doivent répondre aux requêtes de consensus. En outre, les données du cluster doivent être répliquées sur tous les pairs, ce qui entraîne également un coût en bande passante.

En cas de latences plus élevées, la configuration par défaut d'etcd peut entraîner des élections fréquentes ou des timeouts de battement de cœur. Consultez les [réglages][tuning] pour ajuster les délais d'attente dans les déploiements à haute latence.

## Opération {#operation}

### Comment sauvegarder un cluster etcd ? {#how-to-backup-a-etcd-cluster}

etcdctl fournit une commande `snapshot` pour créer des instantanés. Consultez la section [sauvegarde][backup] pour plus de détails.

### Dois-je ajouter un membre avant de supprimer un membre défaillant ? {#should-i-add-a-member-before-removing-an-unhealthy-member}

Lors du remplacement d’un nœud etcd, il est essentiel de supprimer d’abord le membre, puis d’ajouter son remplaçant.

etcd utilise un consensus distribué fondé sur un modèle de quorum ; (n/2)+1 membres, soit une majorité, doivent être d'accord sur une proposition avant qu'elle ne puisse être validée dans le cluster. Ces propositions incluent les mises à jour clé-valeur et les modifications de membre. Ce modèle élimine totalement toute possibilité d'incohérence de type split brain. Le désavantage est que la perte permanente du quorum est catastrophique.

Application à la gestion des membres : si un cluster de 3 membres compte 1 membre hors service, il peut encore progresser, car le quorum est de 2 et 2 membres restent actifs. Toutefois, l'ajout d'un membre à un cluster de 3 membres porte le quorum à 3, puisque 3 voix sont nécessaires pour obtenir la majorité parmi 4 membres. Ce membre supplémentaire n'améliore donc pas la tolérance aux pannes : le cluster reste à 1 panne de nœud de devenir irrécupérable.

En outre, ce nouveau membre est risqué, car il se peut qu’il soit mal configuré ou incapable de rejoindre le cluster. Dans ce cas, il n’existe aucun moyen de récupérer le quorum, car le cluster dispose de deux membres hors ligne et deux membres en ligne, mais nécessite trois votes pour modifier la configuration des membres afin d’annuler l’ajout incorrect de membre. Par défaut, etcd rejette les tentatives d’ajout de membre qui pourraient entraîner une telle situation.

D’un autre côté, si le membre défaillant est supprimé de l’appartenance au cluster en premier lieu, le nombre de membres passe à 2 et le quorum reste à 2. Une fois cette suppression effectuée, l’ajout d’un nouveau membre maintient également le quorum à 2. Ainsi, même si le nouveau nœud ne peut pas être mis en service, il reste possible de supprimer ce nouveau membre via le quorum sur les membres encore actifs.

### Pourquoi etcd n’accepte-t-il pas mes modifications d’appartenance ? {#why-wont-etcd-accept-my-membership-changes}

etcd définit `strict-reconfig-check` afin de rejeter les demandes de reconfiguration qui entraîneraient une perte de quorum. Abandonner le quorum est réellement risqué (en particulier lorsque le cluster est déjà défaillant). Bien qu'il puisse être tentant de désactiver la vérification du quorum en cas de perte de quorum pour ajouter un nouveau membre, cela pourrait entraîner une incohérence complète du cluster. Pour de nombreuses applications, cela aggraverait encore le problème ("corruption de géométrie disque" étant un exemple parmi les plus effrayants).

### Pourquoi etcd perd-il son leader en cas de pics de latence disque ? {#why-does-etcd-lose-its-leader-from-disk-latency-spikes}

Cela est intentionnel ; la latence du disque fait partie de la disponibilité du leader. Supposons qu’un leader de cluster mette une minute à synchroniser sur disque avec fsync une mise à jour du journal Raft, alors que le cluster etcd a un délai d’élection d’une seconde. Même si le leader peut traiter les messages réseau dans l’intervalle d’élection (par exemple, envoyer des battements de cœur), il est effectivement indisponible car il ne peut pas engager de nouvelles propositions ; il attend le disque lent. Si le cluster perd fréquemment son leader en raison de latences disque, essayez d’[optimiser][tuning] les paramètres du disque ou les paramètres temporels d’etcd.

### Que signifie l'avertissement etcd « request ignored (cluster ID mismatch) » ? {#what-does-the-etcd-warning-request-ignored-cluster-id-mismatch-mean}

Chaque nouveau cluster etcd génère un nouvel identifiant de cluster basé sur la configuration initiale du cluster et une valeur unique `initial-cluster-token` fournie par l’utilisateur. En disposant d'identifiants de cluster uniques, etcd est protégé contre les interactions entre clusters qui pourraient corrompre le cluster.

Cet avertissement se produit généralement après avoir supprimé un ancien cluster, puis réutilisé certaines adresses de pair pour le nouveau cluster. Si un processus etcd de l’ancien cluster est toujours en cours d’exécution, il tentera de contacter le nouveau cluster. Le nouveau cluster détectera une incompatibilité d’ID de cluster, ignorera la requête et émettra cet avertissement. Ce message d’avertissement est souvent résolu en veillant à ce que les adresses de pair entre des clusters distincts soient disjointes.

### Que signifie « mvcc : espace de base de données dépassé » et comment le corriger ? {#what-does-mvcc-database-space-exceeded-mean-and-how-do-i-fix-it}

Le modèle de données [contrôle de concurrence multiversion][api-mvcc] d’etcd conserve l'historique complet de l'espace de clés. Sans effectuer régulièrement un compactage de cet historique (par exemple en définissant `--auto-compaction-mode` et `--auto-compaction-retention`), etcd finira par épuiser l'espace de stockage. Si etcd manque d'espace de stockage, il déclenche une alarme de quota d'espace afin de protéger le cluster contre des écritures ultérieures. Tant que cette alarme est active, etcd répond aux requêtes d'écriture par l'erreur `mvcc: database space exceeded`.

Pour récupérer après l'alarme de quota d'espace faible :

1. [Compacter][maintenance-compact] l'historique d'etcd.
2. [Défragmenter][maintenance-defragment] chaque point de terminaison etcd.
3. [Désarmer][maintenance-disarm] l'alarme.

### Que signifie l'avertissement etcd "etcdserver/api/v3rpc: transport : http2Server.HandleStreams a échoué à lire le cadre : lecture tcp 127.0.0.1:2379->127.0.0.1:43020 : lecture : connexion réinitialisée par la partie distante" ? {#what-does-the-etcd-warning-etcdserverapiv3rpc-transport-http2serverhandlestreams-failed-to-read-frame-read-tcp-1270012379-12700143020-read-connection-reset-by-peer-mean}

Il s'agit d'un avertissement côté gRPC lorsque le serveur reçoit un drapeau TCP RST alors que les flux côté client sont fermés prématurément. Par exemple, un client ferme sa connexion alors que le serveur gRPC n’a pas encore traité toutes les trames HTTP/2 dans la file d’attente TCP. Une partie des données peut avoir été perdue côté serveur, mais cela est acceptable tant que la connexion cliente a déjà été fermée.

Seules les [anciennes versions de gRPC](https://github.com/grpc/grpc-go/issues/1362) journalisent cet avertissement. [À partir de v3.2.13, etcd le journalise par défaut au niveau DEBUG](https://github.com/etcd-io/etcd/pull/9080) ; il n'est donc visible que lorsque l'option `--log-level=debug` est activée.

## Performances {#performance}

### Comment puis-je effectuer des tests de charge sur etcd ? {#how-should-i-benchmark-etcd}

Essayez l'outil [benchmark]. Les résultats actuels du [benchmark][benchmark-result] sont disponibles pour comparaison.

### Que signifie l'avertissement etcd « apply entries took too long » ? {#what-does-the-etcd-warning-apply-entries-took-too-long-mean}

Une fois qu'une majorité des membres etcd a accepté de valider une requête, chaque serveur etcd applique la requête à son magasin de données et persiste le résultat sur le disque. Même avec un disque mécanique lent ou un disque réseau virtualisé, tel qu’EBS d’Amazon ou PD de Google, l’application d’une requête devrait normalement prendre moins de 50 millisecondes. Si la durée moyenne d’application dépasse 100 millisecondes, etcd émettra un avertissement indiquant que les entrées mettent trop de temps à être appliquées.

Ce problème est généralement dû à un disque lent. Le disque pourrait subir une contention entre etcd et d'autres applications, ou être trop lent en soi (par exemple, un disque virtuel partagé). Pour écarter la possibilité qu’un disque lent soit à l’origine de cet avertissement, surveillez  [backend_commit_duration_seconds][backend_commit_metrics] (la durée p99 doit être inférieure à 25 ms) afin de vérifier que le disque est suffisamment rapide. Si le disque est trop lent, attribuer un disque dédié à etcd ou utiliser un disque plus rapide résout généralement le problème.

La deuxième cause la plus fréquente est la famine de CPU. Si la surveillance de l'utilisation du CPU de la machine révèle une utilisation élevée, il se peut qu'il ne reste pas assez de capacité de calcul pour etcd. Déplacer etcd vers une machine dédiée, augmenter l'isolation des ressources du processus via cgroups, ou ajuster la priorité du processus serveur etcd à un niveau supérieur peut généralement résoudre le problème.

Les requêtes utilisateur coûteuses qui accèdent à trop de clés (par exemple, la récupération de l’intégralité de l’espace de clés) peuvent également entraîner des latences d’application élevées. Toutefois, accéder à moins de quelques centaines de clés par requête devrait toujours être performant.

Si aucune des suggestions ci-dessus ne permet de supprimer les avertissements, veuillez [ouvrir un problème][new_issue] en incluant des journaux détaillés, des informations de surveillance, des métriques et éventuellement des informations sur la charge de travail.

### Que signifie l'avertissement etcd « failed to send out heartbeat on time » ? {#what-does-the-etcd-warning-failed-to-send-out-heartbeat-on-time-mean}

etcd utilise un protocole de consensus basé sur un leader pour assurer une réplication de données cohérente et l'exécution du journal. Les membres du cluster élisent un seul leader, tous les autres membres deviennent des suiveurs. Le leader élu doit périodiquement envoyer des signaux de vie à ses suiveurs afin de maintenir son leadership. Les suiveurs détectent une panne du leader s’ils ne reçoivent aucun signal de vie dans l’intervalle d’élection et déclenchent alors une nouvelle élection. Si un leader ne parvient pas à envoyer ses signaux de vie à temps, mais qu’il est toujours en cours d’exécution, l’élection est superflue et probablement due à un manque de ressources. Pour détecter ces défaillances douces, si le leader saute deux intervalles de signal de vie, etcd émettra un avertissement indiquant qu’il a échoué à envoyer un signal de vie à temps.

Ce problème est généralement dû à un disque lent. Avant que le leader n'envoie des messages de battement de cœur accompagnés de métadonnées, celui-ci peut nécessiter de persister ces métadonnées sur le disque. Le disque peut subir une contention entre etcd et d'autres applications, ou être trop lent (par exemple, un disque virtuel partagé). Pour éliminer la possibilité qu'un disque lent soit à l'origine de cet avertissement, surveillez  [wal_fsync_duration_seconds][wal_fsync_duration_seconds] (la durée p99 doit être inférieure à 10 ms) afin de confirmer que le disque est suffisamment rapide. Si le disque est trop lent, affecter un disque dédié à etcd ou utiliser un disque plus rapide résout généralement le problème. Pour déterminer si un disque est assez rapide pour etcd, un outil de benchmark tel que [fio][fio] peut être utilisé. Consultez [ici][fio-blog-post] pour un exemple.

La deuxième cause la plus fréquente est la famine de CPU. Si la surveillance de l'utilisation du CPU de la machine révèle une utilisation élevée, il se peut qu'il ne reste pas assez de capacité de calcul pour etcd. Déplacer etcd vers une machine dédiée, augmenter l'isolation des ressources du processus à l'aide de cgroups, ou ajuster la priorité du processus serveur etcd à un niveau supérieur peut généralement résoudre le problème.

Un réseau lent peut également provoquer ce problème. Si les métriques réseau entre les machines etcd indiquent des latences élevées ou un taux élevé de pertes de paquets, il se peut qu'il ne reste pas assez de capacité réseau pour etcd. Déplacer les membres etcd vers un réseau moins congestionné résout généralement le problème. Toutefois, si le cluster etcd est déployé entre plusieurs centres de données, des latences élevées entre les membres sont normales. Dans de tels déploiements, ajustez la configuration `heartbeat-interval` pour qu'elle corresponde approximativement au temps de trajet aller-retour entre les machines, et configurez `election-timeout` de manière à ce qu'elle soit au moins égale à 5 × `heartbeat-interval`. Consultez la [documentation de réglage][tuning] pour plus de détails.

Si aucune des suggestions ci-dessus ne permet de supprimer les avertissements, veuillez [ouvrir un problème][new_issue] en incluant des journaux détaillés, des informations de surveillance, des métriques et éventuellement des informations sur la charge de travail.

### Que signifie l'avertissement etcd « la sauvegarde instantanée prend plus de x secondes pour se terminer » ? {#what-does-the-etcd-warning-snapshotting-is-taking-more-than-x-seconds-to-finish--mean}

etcd envoie un instantané de son magasin clé-valeur complet pour rafraîchir les suiveurs lents et effectuer des [sauvegardes][backup]. Des délais de transfert d'instantané lents augmentent le temps de récupération après panne (MTTR) ; si le cluster reçoit des données à haut débit, les suiveurs lents peuvent entrer en blocage actif en nécessitant un nouvel instantané avant d'avoir terminé la réception d'un instantané précédent. Pour détecter les performances lentes d'instantané, etcd émet un avertissement lorsque l'envoi d'un instantané prend plus de trente secondes et dépasse le temps de transfert attendu pour une connexion 1 Gbps.


[api-mvcc]: /fr/etcd/learning/api/#revisions
[backend_commit_metrics]: /fr/etcd/metrics/#disk
[backup]: /fr/etcd/op-guide/recovery/#snapshotting-the-keyspace
[benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
[benchmark-result]: /fr/etcd/op-guide/performance/
[chubby]: http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[hardware-setup]: /fr/etcd/op-guide/hardware/
[maintenance-compact]:  /fr/etcd/op-guide/maintenance/#history-compaction-v3-api-key-value-database
[maintenance-defragment]: /fr/etcd/op-guide/maintenance/#defragmentation
[maintenance-disarm]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#alarm-disarm
[new_issue]: https://github.com/etcd-io/etcd/issues/new
[raft]: https://raft.github.io/raft.pdf
[runtime reconfiguration]: /fr/etcd/op-guide/runtime-configuration/
[supported-platform]: /fr/etcd/op-guide/supported-platform/
[tuning]: /fr/etcd/tuning/
[wal_fsync_duration_seconds]: /fr/etcd/metrics/#disk
