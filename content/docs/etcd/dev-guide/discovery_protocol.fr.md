---
title: Protocole du service de découverte
weight: 1500
description: "Découvrir les membres etcd lors de la phase d'amorçage d'un cluster"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/discovery_protocol.md"
aliases: [/etcd/dev-guide/discovery_protocol/]
---

Le protocole de service de découverte aide un nouveau membre etcd à découvrir tous les autres membres du cluster pendant la phase d'initialisation, en utilisant une URL de découverte partagée.

Le protocole de service de découverte n’est utilisé que pendant la phase d’amorçage du cluster, et ne peut pas être utilisé pour la reconfiguration en temps réel ou la surveillance du cluster.

Le protocole utilise un nouveau jeton de découverte pour initialiser un _unique_ cluster etcd. Souvenez-vous qu’un jeton de découverte ne peut représenter qu’un seul cluster etcd. Dès que le protocole de découverte associé à ce jeton est lancé, même s’il échoue en cours de route, il ne doit pas être utilisé pour initialiser un autre cluster etcd.

Le reste de cet article détaille le processus de découverte à l’aide d’exemples correspondant à un cluster de découverte auto-hébergé. Le service public de découverte, discovery.etcd.io, fonctionne de la même manière, mais avec une couche d’interface améliorée qui masque les URL complexes, génère automatiquement des UUID et met en place certaines protections contre les requêtes excessives. Au cœur de ce service public, un cluster etcd est toujours utilisé comme magasin de données, comme décrit dans ce document.

## Flot de protocole {#protocol-workflow}

L'idée du protocole de découverte consiste à utiliser un cluster etcd interne pour coordonner le démarrage d'un nouveau cluster. Tout d'abord, tous les nouveaux membres interagissent avec le service de découverte et contribuent à générer la liste de membres attendue. Ensuite, chaque nouveau membre démarre son serveur en utilisant cette liste, ce qui permet d'obtenir la même fonctionnalité que l'option -initial-cluster.

Dans l'exemple de workflow suivant, nous allons présenter chaque étape du protocole au format curl afin de faciliter la compréhension.

Par convention, le protocole de découverte etcd utilise le préfixe de clé `_etcd/registry`. Si `http://example.com` héberge un cluster etcd pour le service de découverte, l'URL complète de l'espace de clés de découverte sera `http://example.com/v2/keys/_etcd/registry`. Nous utiliserons cette URL comme préfixe dans l'exemple.

### Création d'un nouveau jeton de découverte {#creating-a-new-discovery-token}

Générez un jeton unique qui identifiera le nouveau cluster. Ce jeton sera utilisé comme préfixe unique dans l'espace de clés de découverte aux étapes suivantes. Une méthode simple consiste à utiliser `uuidgen` :

```
UUID=$(uuidgen)
```

### Spécification de la taille attendue du cluster {#specifying-the-expected-cluster-size}

Le jeton de découverte attend une taille de cluster qui doit être précisée. Cette taille est utilisée par le service de découverte pour savoir quand il a trouvé tous les membres qui formeront initialement le cluster.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size -d value=${cluster_size}
```

En général, la taille du cluster est de 3, 5 ou 7. Consultez [taille optimale du cluster][cluster-size] pour plus de détails.

### Mise en marche des processus etcd {#bringing-up-etcd-processes}

Étant donné l'URL de découverte, utilisez-la comme indicateur `-discovery` et lancez les processus etcd. Chaque processus etcd suivra automatiquement les étapes suivantes en interne s'il reçoit l'indicateur `-discovery`.

### S'enregistrer lui-même {#registering-itself}

La première étape pour le processus etcd consiste à s'inscrire dans l'URL de découverte en tant que membre. Cela se fait en créant l'ID de membre comme clé dans l'URL de découverte.

```
curl -X PUT http://example.com/v2/keys/_etcd/registry/${UUID}/${member_id}?prevExist=false -d value="${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}"
```

### Vérification du statut {#checking-the-status}

Il vérifie la taille attendue du cluster et l'état d'inscription à l'URL de découverte, puis détermine l'action suivante.

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}/_config/size
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}
```

Si le nombre de membres enregistrés reste insuffisant, l'attente sera poursuivie jusqu'à la réapparition de membres sortis.

Si le nombre de membres enregistrés est supérieur à la taille attendue N, le système considère les N premiers membres enregistrés comme la liste des membres du cluster. Si le membre lui-même figure dans cette liste, la procédure de découverte réussit et il récupère tous les pairs à partir de la liste des membres. Sinon, la procédure de découverte échoue, car le cluster est plein.

Dans l'implémentation etcd, le membre peut vérifier l'état du cluster même avant de s'enregistrer. Il peut donc échouer rapidement si le cluster est plein.

### En attente de tous les membres {#waiting-for-all-members}

Le processus d'attente est décrit en détail dans la documentation de l'API [etcd][api].

```
curl -X GET http://example.com/v2/keys/_etcd/registry/${UUID}?wait=true&waitIndex=${current_etcd_index}
```

Il continue d'attendre jusqu'à la découverte de tous les membres.

## Service de découverte publique {#public-discovery-service}

CoreOS Inc. héberge un service de découverte public à https://discovery.etcd.io/, qui offre plusieurs fonctionnalités pratiques pour faciliter l'utilisation.

### Préfixe de masquage de clé {#mask-key-prefix}

Le service de découverte publique redirigera `https://discovery.etcd.io/${UUID}` vers le cluster etcd derrière pour la clé située à `/v2/keys/_etcd/registry`. Il masque le préfixe de clé d'enregistrement afin d'obtenir une URL de découverte plus courte et plus lisible.

### Obtenir un nouveau jeton {#get-new-token}

```
GET /new

Sent query:
	size=${cluster_size}
Possible status codes:
	200 OK
	400 Bad Request
200 Body:
	generated discovery url
```

Le processus de génération dans le service suit les étapes allant de [Création d'un jeton de découverte][new-discovery-token] à [Spécification de la taille attendue du cluster][expected-cluster-size].

### Vérifier l'état de découverte {#check-discovery-status}

```
GET /${UUID}
```

L’état de ce jeton de découverte, y compris les machines qui ont été enregistrées, peut être vérifié en demandant la valeur de l’UUID.

### Dépôt open source {#open-source-repository}

Le dépôt est situé à https://github.com/coreos/discovery.etcd.io.. Il peut être utilisé pour créer un service de découverte personnalisé.

[api]: https://etcd.io/docs/v2.3/api#waiting-for-a-change
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
