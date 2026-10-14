---
title: Protocole du service de découverte
weight: 1500
description: "Découvrir les membres etcd lors de la phase d'amorçage d'un cluster"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
---

Le protocole de service de découverte aide un nouveau membre etcd à découvrir tous les autres membres du cluster pendant la phase d'amorçage, en utilisant un jeton de découverte partagé et une liste de points de terminaison.

Le protocole de service de découverte n’est utilisé que pendant la phase d’amorçage du cluster, et ne peut pas être utilisé pour la reconfiguration en temps réel ou la surveillance du cluster.

Le protocole utilise un nouveau jeton de découverte pour amorcer un _unique_ cluster etcd. Souvenez-vous qu’un jeton de découverte ne peut représenter qu’un seul cluster etcd. Dès que le protocole de découverte associé à ce jeton est lancé, même s’il échoue en cours de route, il ne doit pas être utilisé pour amorcer un autre cluster etcd.

Le reste de cet article explique le processus de découverte à l’aide d’exemples correspondant à un cluster de découverte auto-hébergé.

Notez que ce document ne concerne que la découverte v3. Consultez le document précédent pour plus de détails sur la découverte [v2][v2-discovery].

## Workflow du protocole {#protocol-workflow}

L'idée du protocole de découverte consiste à utiliser un cluster etcd interne pour coordonner le démarrage d'un nouveau cluster. Tout d'abord, tous les nouveaux membres interagissent avec le service de découverte et contribuent à générer la liste de membres attendue. Ensuite, chaque nouveau membre démarre son serveur en utilisant cette liste, ce qui permet d'obtenir la même fonctionnalité que l'option -initial-cluster.

Dans l'exemple de workflow suivant, nous allons lister chaque étape du protocole à l'aide de la commande `etcdctl` afin de faciliter la compréhension, et nous supposons que l'hôte `http://example.com:2379` héberge un cluster etcd pour le service de découverte.

Par convention, le protocole de découverte etcd utilise le préfixe de clé `/_etcd/registry`.


### Création d'un nouveau jeton de découverte {#creating-a-new-discovery-token}

Générez un jeton unique qui identifiera le nouveau cluster. Ce jeton sera utilisé comme préfixe unique dans l'espace de clés de découverte aux étapes suivantes. Une méthode simple consiste à utiliser `uuidgen` :

```
UUID=$(uuidgen)
```

### Spécification de la taille attendue du cluster {#specifying-the-expected-cluster-size}

Le jeton de découverte attend une taille de cluster qui doit être précisée. Cette taille est utilisée par le service de découverte pour savoir quand il a trouvé tous les membres qui formeront initialement le cluster.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

En général, la taille du cluster est de 3, 5 ou 7. Consultez [taille optimale du cluster][cluster-size] pour plus de détails.

### Mise en marche des processus etcd {#bringing-up-etcd-processes}

Définissez le jeton de découverte `${UUID}` sur le drapeau `--discovery-token`, et définissez les points de terminaison du cluster etcd qui prend en charge le service de découverte sur le drapeau `--discovery-endpoints`. Cela activera la découverte v3 pour amorcer le cluster etcd.

Chaque processus etcd suivra les étapes internes suivantes si les drapeaux `--discovery-token` et `--discovery-endpoints` sont fournis.

Si le service de découverte active l'authentification par certificat client, configurez les drapeaux suivants. Leur utilisation suit exactement le même schéma que l'utilisation de `etcdctl` pour communiquer avec un cluster etcd.
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

Si le service de découverte active l'authentification basée sur les rôles, configurez les drapeaux suivants. Leur utilisation suit exactement le même schéma que l'utilisation de `etcdctl` pour communiquer avec un cluster etcd.
```
--discovery-user
--discovery-password
```

Les valeurs par défaut de temps ou de délai d’attente peuvent également être modifiées à l’aide des drapeaux suivants, qui s’utilisent exactement de la même manière que `etcdctl` pour communiquer avec un cluster etcd.
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### S'enregistrer lui-même {#registering-itself}

La première action entreprise par chaque processus etcd consiste à s’inscrire dans le cluster nouvellement créé en tant que membre. Cela se fait en créant l’ID de membre comme clé dans la clé de registre complète.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### Vérification du statut {#checking-the-status}

Il vérifie la taille attendue du cluster et l'état d'inscription, puis détermine l'action suivante.

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

Si le nombre de membres enregistrés reste insuffisant, l'attente sera poursuivie jusqu'à l'apparition d'autres membres.

Si le nombre de membres enregistrés est supérieur à la taille attendue N, le système considère les N premiers membres enregistrés comme la liste des membres du cluster. Si le membre lui-même figure dans cette liste, la procédure de découverte réussit, et il récupère tous les pairs à partir de la liste des membres. Sinon, la procédure de découverte échoue, car le cluster est plein.

Le membre peut vérifier l'état du cluster même avant de s'être enregistré. Il peut donc échouer rapidement si le cluster est plein.

### En attente de tous les membres {#waiting-for-all-members}

Le processus d'attente continue à surveiller le préfixe de clé `/_etcd/registry/${UUID}/members` jusqu'à la découverte de tous les membres.

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
