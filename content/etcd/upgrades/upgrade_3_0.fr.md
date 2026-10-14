---
title: Mettre à jour etcd de la version 2.3 à la 3.0
weight: 6900
description: "Processus, listes de vérification et notes sur la mise à jour d’etcd de la version 2.3 à la 3.0"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

Dans le cas général, la mise à niveau d’etcd 2.3 vers 3.0 peut s'effectuer sans interruption de service, par mise à niveau progressive :
 - un par un, arrêtez les processus etcd v2.3 et remplacez-les par des processus etcd v3.0
 - après avoir lancé tous les processus v3.0, les nouvelles fonctionnalités de la version 3.0 sont disponibles pour le cluster

Avant de [lancer la mise à jour](#upgrade-procedure), lisez le reste du présent guide afin de vous préparer.

### Listes de vérification pour la mise à jour {#upgrade-checklists}

> [!WARNING]
> Lorsque [on migre depuis la version v2 sans données v3](https://github.com/etcd-io/etcd/issues/9480), le serveur etcd v3.2+ provoque une panne lorsqu'il restaure à partir d'un instantané existant mais qu'aucun fichier v3 `ETCD_DATA_DIR/member/snap/db` n'est présent. Cela se produit lorsque le serveur a été migré depuis la version v2 sans données v3 précédentes. Cela empêche également la perte accidentelle de données v3 (par exemple, le fichier `db` pourrait avoir été déplacé). etcd exige que les opérations après migration vers v3 ne soient effectuées que si des données v3 sont présentes. N'effectuez pas la mise à jour vers des versions v3 plus récentes tant que le serveur v3.0 ne contient pas de données v3.

#### Exigences de mise à jour {#upgrade-requirements}

Pour mettre à jour un déploiement etcd existant vers la version 3.0, le cluster en cours d'exécution doit être la version 2.3 ou ultérieure. Si la version est antérieure à 2.3, veuillez mettre à jour vers [2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8) avant de procéder à la mise à jour vers la version 3.0.

En outre, pour garantir une mise à niveau progressive sans incident, le cluster en cours d'exécution doit être sain. Vérifiez l'état de santé du cluster à l'aide de la commande `etcdctl cluster-health` avant de poursuivre.

#### Préparation {#preparation}

Avant de mettre à jour etcd, testez toujours les services dépendants d’etcd dans un environnement de préproduction avant de déployer la mise à jour dans l’environnement de production.

Avant de commencer, [sauvegardez le répertoire de données etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore). Si une erreur survient durant la mise à jour, il sera possible d'utiliser cette sauvegarde pour [revenir à la version d’etcd actuellement déployée](#downgrade).

#### Versions mixtes {#mixed-versions}

Lors d'une mise à jour, un cluster etcd prend en charge des versions mixtes de membres et fonctionne selon le protocole de la version commune la plus basse. Le cluster n'est considéré comme mis à jour qu'une fois que tous ses membres ont été mis à jour vers la version 3.0. En interne, les membres etcd négocient entre eux afin de déterminer la version globale du cluster, qui contrôle la version signalée et les fonctionnalités prises en charge.

#### Limitations {#limitations}

Il peut falloir jusqu’à 2 minutes pour que le membre nouvellement mis à jour rattrape le cluster existant lorsque la taille totale des données dépasse 50 Mo. Vérifiez la taille d’un instantané récent pour estimer la taille totale des données. Autrement dit, le plus sûr est d’attendre 2 minutes entre chaque mise à jour de membre.

Pour une taille totale de données bien plus importante, de 100 Mo ou plus, ce processus unique peut prendre encore plus de temps. Les administrateurs de clusters etcd très volumineux de cette ampleur peuvent librement contacter l'équipe [etcd][etcd-contact] avant la mise à jour, et nous serons heureux de leur fournir des conseils sur la procédure.

#### Rétrogradation {#downgrade}

Si tous les membres ont été mis à jour vers la version v3.0, le cluster sera mis à jour vers la version v3.0, et le retour à une version antérieure à partir de cet état finalisé est **impossible**. Si toutefois un seul membre reste en version v2.3, le cluster et ses opérations restent au niveau « v2.3 », et il est possible, depuis cet état de cluster mixte, de revenir à l’utilisation d’un binaire etcd v2.3 sur tous les membres.

Veuillez [sauvegarder le répertoire de données](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) de tous les membres etcd afin de permettre la rétrogradation du cluster, même après sa mise à jour complète.

### Procédure de mise à jour {#upgrade-procedure}

Cet exemple détaille la mise à jour d’un cluster etcd v2.3 à trois membres fonctionnant sur une machine locale.

#### 1. Vérifier les prérequis de mise à jour. {#1-check-upgrade-requirements}

Le cluster est-il sain et en cours d'exécution sous la version v.2.3.x ?

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. Arrêtez le processus etcd existant {#2-stop-the-existing-etcd-process}

Lorsque chaque processus etcd est arrêté, les autres membres du cluster enregistrent des erreurs attendues. Cela est normal, car la connexion avec un membre du cluster a été (temporairement) interrompue :

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

Il est recommandé de procéder à une [sauvegarde du répertoire de données etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) afin de disposer d’un chemin de retour en cas de problème :

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. Remplacer le binaire par etcd v3.0 et démarrer le nouveau processus etcd {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

Le nouvel etcd v3.0 publiera ses informations dans le cluster :

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

Vérifiez que chaque membre, puis l’ensemble du cluster, devient sain avec le nouveau binaire etcd v3.0 :

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


Les membres mis à jour émettront des avertissements similaires au suivant jusqu'à ce que l'intégralité du cluster soit mise à jour. C'est normal et cessera une fois que tous les membres du cluster etcd auront été mis à jour vers la version 3.0 :

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. Répétez l'étape 2 à l'étape 3 pour tous les autres membres {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Terminer {#5-finish}

Lorsque tous les membres sont mis à jour, le cluster signalera avec succès la mise à jour vers la version 3.0 :

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## Considérations complémentaires {#further-considerations}

- Les variables d'environnement etcdctl ont été mises à jour. Si `ETCDCTL_API=2 etcdctl cluster-health` fonctionne correctement mais que `ETCDCTL_API=3 etcdctl endpoints health` renvoie `Error:  grpc: timed out when dialing`, veillez à utiliser les [nouveaux noms de variables](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl).

## Problèmes connus {#known-issues}

- etcd &lt; v3.1 ne fonctionne pas correctement s'il est compilé avec Go &gt; v1.7. Consultez [Problème 6951](https://github.com/etcd-io/etcd/issues/6951) pour plus d'informations.
- Si une erreur telle que `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.` apparaît dans les journaux du serveur etcd, assurez-vous qu'etcd est une version précompilée ou bien compilée avec (etcd v3.1+ &amp; go v1.7+) ou (etcd &lt;v3.1 &amp; go v1.6.x).
- L'ajout d'un membre v3 à un cluster v2.3 pendant une mise à jour n'est pas pris en charge et peut provoquer des paniques. Consultez [Problème 7249](https://github.com/etcd-io/etcd/issues/7429) pour plus d'informations. Les versions mixtes de membres etcd ne sont autorisées que pendant la migration vers v3. Terminez les mises à jour avant d'effectuer toute modification de la composition du cluster.

[etcd-contact]: https://groups.google.com/g/etcd-dev
