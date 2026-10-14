---
title: Mettre à jour etcd de la version 3.0 à la 3.1
weight: 6850
description: "Processus, listes de vérification et notes sur la mise à niveau d’etcd de la version 3.0 à la 3.1"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
---

Dans le cas général, la mise à niveau d’etcd 3.0 vers 3.1 peut être effectuée sans interruption de service, par mise à niveau progressive :
 - un nœud à la fois, arrêtez les processus etcd v3.0 et remplacez-les par des processus etcd v3.1
 - après avoir lancé tous les processus v3.1, les nouvelles fonctionnalités de la version v3.1 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que les opérations après migration vers v3 ne soient effectuées que si des données v3 sont présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

#### Surveillance {#monitoring}

Les métriques suivantes issues de la version 3.0.x ont été dépréciées en faveur de [go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus) :

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.1, le cluster en cours d'exécution doit être la version 3.0 ou ultérieure. Si la version est antérieure à 3.0, veuillez [mettre à jour vers la version 3.0](/fr/etcd/upgrades/upgrade_3_0) avant de procéder à la mise à jour vers la version 3.1.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl endpoint health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [sauvegardez les données etcd](/fr/etcd/op-guide/maintenance/#snapshot-backup). Si une erreur survient lors de la mise à jour, il sera possible d'utiliser cette sauvegarde pour [rétrograder](#downgrade) vers la version existante d’etcd. Veuillez noter que la commande `snapshot` ne sauvegarde que les données v3. Pour les données v2, consultez [sauvegarde du magasin de données v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version 3.1. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui détermine la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Note : Si le cluster ne contient que des données v3 et aucune donnée v2, il n'est pas soumis à cette limitation.

Si le cluster sert un jeu de données v2 dont la taille dépasse 50 Mo, chaque membre nouvellement mis à jour peut prendre jusqu’à deux minutes pour rattraper le cluster existant. Vérifiez la taille d’un instantané récent afin d’estimer la taille totale des données. Autrement dit, le plus sûr est d’attendre deux minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.1, le cluster sera mis à jour vers la v3.1, et un retour en arrière depuis cet état finalisé est **impossible**. Toutefois, si un seul membre reste en version v3.0, le cluster et ses opérations restent "v3.0", et il est possible, depuis cet état de cluster mixte, de revenir à l'utilisation d’un binaire etcd v3.0 sur tous les membres.

Veuillez [sauvegarder le répertoire de données](/fr/etcd/op-guide/maintenance#snapshot-backup) de tous les membres etcd afin de permettre la rétrogradation du cluster, même après sa mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple montre comment mettre à jour un cluster etcd à 3 membres, version 3.0, en cours d'exécution sur une machine locale.

#### 1. Vérifier les prérequis de mise à jour {#1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version 3.0.x ?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. Arrêtez le processus etcd existant {#2-stop-the-existing-etcd-process}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

Il est recommandé de procéder à une [sauvegarde des données etcd](/fr/etcd/op-guide/maintenance#snapshot-backup) à cette étape afin de disposer d’un chemin de retour en cas de problème :

```
$ etcdctl snapshot save backup.db
```

#### 3. Remplacer le binaire par etcd v3.1 et démarrer le nouveau processus etcd {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

Le nouvel etcd v3.1 publiera ses informations dans le cluster :

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec le binaire etcd v3.1 nouvellement installé :

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Les membres mis à jour émettront des avertissements similaires au suivant jusqu'à ce que l'intégralité du cluster soit mise à jour. C'est normal et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.1 :

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. Répétez l'étape 2 à l'étape 3 pour tous les autres membres {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Terminer {#5-finish}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.1 :

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
