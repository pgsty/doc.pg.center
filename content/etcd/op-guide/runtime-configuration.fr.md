---
title: "Reconfiguration en cours d'exécution"
weight: 4700
description: Prise en charge par etcd de la reconfiguration incrémentielle en cours d'exécution
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
---

etcd dispose d’un support pour la reconfiguration incrémentielle en temps d’exécution, ce qui permet aux utilisateurs de mettre à jour la composition du cluster en cours d’exécution.

Les requêtes de reconfiguration ne peuvent être traitées que lorsque la majorité des membres du cluster sont fonctionnels. Il est **fortement recommandé** de toujours disposer d'un cluster de taille supérieure à deux en production. Il est dangereux de supprimer un membre d'un cluster à deux membres. La majorité d'un cluster à deux membres est également de deux. En cas d'échec pendant le processus de suppression, le cluster pourrait ne pas être en mesure de progresser et nécessiterait un [redémarrage suite à une défaillance de la majorité][majority failure].

Pour mieux comprendre la conception sous-jacente à la reconfiguration en cours d’exécution, veuillez lire [le document de reconfiguration en cours d’exécution][runtime-reconf].

## Cas d'utilisation de la reconfiguration {#reconfiguration-use-cases}

Cette section explique certaines raisons courantes de reconfiguration d’un cluster. La plupart de ces raisons consistent simplement en des combinaisons d’ajout ou de suppression d’un membre, telles qu’expliquées ci-dessous sous [Opérations de reconfiguration du cluster][cluster-reconf].

### Rotation ou mise à niveau de plusieurs machines {#cycle-or-upgrade-multiple-machines}

Si plusieurs membres d’un cluster doivent être déplacés en raison d’une maintenance planifiée (mise à jour matérielle, coupure réseau, etc.), il est recommandé de modifier les membres un par un.

Il est sûr de supprimer le leader, mais un bref temps d'indisponibilité survient pendant le processus d'élection. Si le cluster contient plus de 50 Mo de données v2, il est recommandé de [migrer le répertoire de données du membre][member migration].

### Modifier la taille du cluster {#change-the-cluster-size}

L'augmentation de la taille du cluster peut améliorer la [tolérance aux pannes][fault tolerance table] et les performances de lecture. Comme les clients peuvent lire depuis n'importe quel membre, l'augmentation du nombre de membres accroît le débit global des lectures sérialisables.

Réduire la taille du cluster peut améliorer les performances d'écriture du cluster, au prix d'une résilience réduite. Les écritures dans le cluster sont répliquées sur la majorité des membres avant d'être considérées comme validées. Réduire la taille du cluster diminue la taille de la majorité, et chaque écriture est ainsi validée plus rapidement.

### Remplacer une machine défaillante {#replace-a-failed-machine}

Si une machine tombe en panne à cause d'une défaillance matérielle, d'une corruption du répertoire de données ou d'une autre situation critique, elle doit être remplacée dès que possible. Les machines ayant cessé de fonctionner sans avoir été retirées affectent négativement le quorum et réduisent la tolérance à une défaillance supplémentaire.

Pour remplacer la machine, suivez les instructions pour [supprimer le membre][remove member] du cluster, puis [ajouter un nouveau membre][add member] à sa place. Si le cluster contient plus de 50 Mo, il est recommandé de [migrer le répertoire de données du membre défaillant][member migration] s'il est toujours accessible.

### Redémarrer le cluster après une défaillance majoritaire {#restart-cluster-from-majority-failure}

Si la majorité du cluster est perdue ou si tous les nœuds ont changé d'adresse IP, une intervention manuelle est nécessaire pour effectuer une récupération en toute sécurité. Les étapes fondamentales du processus de récupération consistent à [créer un nouveau cluster à partir des anciennes données][disaster recovery], forcer un seul membre à agir en tant que leader, puis utiliser la configuration en cours d’exécution pour [ajouter les nouveaux membres][add member] à ce nouveau cluster un par un.

### Récupérer un cluster après une défaillance minoritaire {#recover-cluster-from-minority-failure}

Si un membre spécifique est perdu, cela revient à remplacer une machine défaillante. Les étapes sont décrites dans [Remplacer une machine défaillante](/fr/etcd/op-guide/runtime-configuration/#replace-a-failed-machine).

## Opérations de reconfiguration du cluster {#cluster-reconfiguration-operations}

Étant donné ces cas d'utilisation, les opérations concernées peuvent être décrites pour chacune.

Avant toute modification, une majorité simple (quorum) des membres etcd doit être disponible. Il s'agit essentiellement de la même exigence que pour toute écriture dans etcd.

Toutes les modifications apportées au cluster doivent être effectuées séquentiellement :

* Pour mettre à jour les peerURLs d’un seul membre, effectuez une opération de mise à jour
* Pour remplacer un membre sain, supprimez l’ancien membre puis ajoutez un nouveau membre
* Pour passer de 3 à 5 membres, effectuez deux opérations d’ajout
* Pour passer de 5 à 3 membres, effectuez deux opérations de suppression

Tous ces exemples utilisent l'outil en ligne de commande `etcdctl` fourni avec etcd. Pour modifier l'appartenance sans `etcdctl`, utilisez l’API membres gRPC [v3][member-api-grpc].

### Mettre à jour un membre {#update-a-member}

#### Mettre à jour les URL client d'annonce {#update-advertise-client-urls}

Pour mettre à jour les URL d'annonce client d'un membre, redémarrez simplement ce membre en spécifiant les URL client mises à jour via le drapeau (`--advertise-client-urls`) ou la variable d'environnement (`ETCD_ADVERTISE_CLIENT_URLS`). Le membre redémarré publiera automatiquement les URL mises à jour. Une URL client incorrectement mise à jour n'affecte pas la santé du cluster etcd.

#### Mettre à jour les URL d'annonce des pairs {#update-advertise-peer-urls}

Pour mettre à jour les URL d'annonce des pairs d'un membre, mettez à jour explicitement celles-ci à l'aide de la commande member, puis redémarrez le membre. Cette action supplémentaire est nécessaire car la mise à jour des URL de pair modifie la configuration globale du cluster et peut affecter l'intégrité du cluster etcd.

Pour mettre à jour les URL d'annonce du pair, commencez par trouver l'ID du membre cible. Pour lister tous les membres avec `etcdctl` :

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

Cet exemple utilise `update` pour le membre d’identifiant a8266ecf031671f3 et modifie sa valeur peerURLs en `http://10.0.1.10:2380` :

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### Supprimer un membre {#remove-a-member}

Supposons que l'ID du membre à supprimer soit a8266ecf031671f3. Utilisez la commande `remove` pour effectuer la suppression :

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

Le membre cible s'arrête lui-même à ce stade et imprime la suppression dans le journal :

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

Il est sûr de supprimer le leader, mais le cluster sera inactif pendant la période nécessaire à l'élection d'un nouveau leader. Cette durée correspond normalement au délai d'élection plus la durée du processus de vote.

### Ajouter un nouveau membre {#add-a-new-member}

Ajouter un membre est un processus en deux étapes :

 * Ajoutez le nouveau membre au cluster au moyen de l’[API gRPC des membres][member-api-grpc] ou de la commande `etcdctl member add`.
 * Démarrez le nouveau membre avec la nouvelle configuration du cluster, y compris la liste actualisée des membres (membres existants + nouveau membre).

`etcdctl` ajoute un nouveau membre au cluster en spécifiant le [nom][conf-name] du membre et les [URL de pair annoncées][conf-adv-peer] :

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

`etcdctl` a informé le cluster du nouveau membre et a affiché les variables d'environnement nécessaires pour le démarrer correctement. Désormais, lancez le nouveau processus etcd avec les drapeaux appropriés pour le nouveau membre :

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

Le nouveau membre s'exécutera en tant que partie du cluster et commencera immédiatement à se synchroniser avec le reste du cluster.

Lorsque vous ajoutez plusieurs membres, la meilleure pratique consiste à configurer un seul membre à la fois et à vérifier qu’il démarre correctement avant d’ajouter de nouveaux membres. Si vous ajoutez un nouveau membre à un cluster à un seul nœud, le cluster ne peut pas progresser avant que le nouveau membre ne démarre, car il faut deux membres pour atteindre la majorité nécessaire à l’atteinte du consensus. Ce comportement ne se produit que durant la période où `etcdctl member add` informe le cluster du nouveau membre et où ce dernier établit avec succès une connexion au membre existant.

#### Ajouter un nouveau membre apprenant {#add-a-new-member-as-learner}

À partir de la version v3.4, etcd prend en charge l’ajout d’un nouveau membre en tant que membre apprenant / membre non votant.
La motivation et la conception sont décrites dans le [document de conception][design-learner].
Afin de rendre le processus d’ajout d’un nouveau membre plus sûr,
et de réduire la durée d’indisponibilité du cluster lors de l’ajout du nouveau membre,
il est recommandé de faire rejoindre le nouveau membre au cluster
en tant que membre apprenant jusqu’à ce qu’il soit à jour.
Ce processus peut être décrit comme une séquence en trois étapes :

 * Ajoutez le nouveau membre comme apprenant au moyen de l'[API gRPC des membres][member-api-grpc] ou de la commande `etcdctl member add --learner`.

 * Démarrez le nouveau membre avec la configuration mise à jour du cluster, incluant la liste des membres mis à jour (membres existants + le nouveau membre).
     Cette étape est identique à celle précédente.

 * Promouvoir le membre apprenant nouvellement ajouté en membre votant via l'[API gRPC des membres][member-api-grpc] ou la commande `etcdctl member promote`.
     Le serveur etcd valide la requête de promotion afin d'assurer sa sécurité opérationnelle.
     Un membre apprenant ne peut être promu en membre votant qu'après avoir rattrapé le journal Raft du leader.
     Si un membre apprenant n'a pas encore rattrapé le journal Raft du leader, la requête de promotion échoue
     (voir la section [cas d'erreur lors de la promotion d'un membre] pour plus de détails).
     Dans ce cas, l'utilisateur doit attendre puis réessayer ultérieurement.

Dans la version 3.4, le serveur etcd limite le nombre de membres apprenants qu’un cluster peut avoir à un seul. La principale considération est de limiter la charge supplémentaire imposée au leader en raison de la propagation des données du leader vers le membre apprenant.

Utilisez `etcdctl member add` avec le drapeau `--learner` pour ajouter un nouveau membre au cluster en tant que membre apprenant.

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

Après avoir lancé le nouveau processus etcd pour le membre apprenant nouvellement ajouté, utilisez `etcdctl member promote` pour promouvoir le membre apprenant en membre votant.
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### Cas d'erreur lors de l'ajout de membres {#error-cases-when-adding-members}

Dans le cas suivant, un nouvel hôte n'est pas inclus dans la liste des nœuds énumérés. Si c'est un nouveau cluster, le nœud doit être ajouté à la liste des membres initiaux du cluster.

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

Dans cet exemple d’erreur, l’adresse spécifiée au démarrage (10.0.1.14:2380) diffère de celle enregistrée pour rejoindre le cluster (10.0.1.13:2380) :

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

Si etcd démarre en utilisant le répertoire de données d’un membre supprimé, etcd s’arrête automatiquement s’il se connecte à tout membre actif du cluster :

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### Cas d'erreur lors de l'ajout d'un membre apprenant {#error-cases-when-adding-a-learner-member}

Impossible d’ajouter un membre apprenant à un cluster si celui-ci possède déjà 1 membre apprenant (v3.4).
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### Cas d'erreur lors de la promotion d'un membre apprenant {#error-cases-when-promoting-a-learner-member}

Un membre apprenant ne peut être promu en membre votant que s’il est synchronisé avec le leader.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

Promouvoir un membre qui n’est pas un membre apprenant échouera.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

Promouvoir un membre qui n'existe pas dans le cluster échouera.
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### Mode de vérification stricte de la configuration (`-strict-reconfig-check`) {#strict-reconfiguration-check-mode--strict-reconfig-check}

Comme indiqué ci-dessus, la meilleure pratique pour ajouter de nouveaux membres consiste à configurer un seul membre à la fois et à vérifier qu’il démarre correctement avant d’ajouter d’autres nouveaux membres. Cette approche progressive est très importante, car si les nouveaux membres ne sont pas correctement configurés (par exemple, si les URL de pair sont incorrectes), le cluster peut perdre son quorum. La perte de quorum se produit car les nouveaux membres sont pris en compte dans le quorum, même s’ils ne sont pas accessibles depuis les autres membres existants. Une perte de quorum peut également survenir en cas de problème de connectivité ou de problème opérationnel.

Pour éviter ce problème, etcd met à disposition une option `-strict-reconfig-check`. Si cette option est passée à etcd, celui-ci rejette les demandes de reconfiguration lorsque le nombre de membres démarrés sera inférieur à un quorum du cluster reconfiguré.

Activé par défaut.

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /fr/etcd/op-guide/configuration#clustering
[conf-name]: /fr/etcd/op-guide/configuration#member
[design-learner]: /fr/etcd/learning/design-learner
[disaster recovery]: /fr/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /fr/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /fr/etcd/op-guide/runtime-reconf-design/
