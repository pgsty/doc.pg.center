---
title: Guide de clustering
weight: 4150
description: "Initialisation d’un cluster etcd : méthode statique, découverte etcd et découverte DNS"
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/clustering.md"
---

## Aperçu {#overview}

Lancer un cluster etcd de manière statique exige que chaque membre connaisse un autre membre du cluster. Dans certains cas, les adresses IP des membres du cluster peuvent être inconnues à l'avance. Dans ces situations, le cluster etcd peut être initialisé à l'aide d'un service de découverte.

Une fois qu’un cluster etcd est en cours d’exécution, l’ajout ou la suppression de membres s’effectue via la reconfiguration en temps réel [runtime reconfiguration][runtime-conf]. Pour mieux comprendre la conception sous-jacente à la reconfiguration en temps réel, nous recommandons de lire [le document de conception de la configuration en temps réel][runtime-reconf-design].

Ce guide traite des mécanismes suivants pour amorcer un cluster etcd :

* [Statique](#static)
* [Découverte etcd](#etcd-discovery)
* [Découverte DNS](#dns-discovery)

Chaque mécanisme de mise en place initiale sera utilisé pour créer un cluster etcd composé de trois machines avec les détails suivants :

|Nom|Adresse|Nom d'hôte|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## Statique {#static}

Comme nous connaissons les membres du cluster, leurs adresses et la taille du cluster avant de commencer, nous pouvons utiliser une configuration de bootstrap hors ligne en définissant le drapeau `initial-cluster`. Chaque machine recevra soit les variables d'environnement suivantes, soit les arguments en ligne de commande :

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

Notez que les URL spécifiées dans `initial-cluster` sont les URL de pair annoncées, c’est-à-dire qu’elles doivent correspondre à la valeur de `initial-advertise-peer-urls` sur les nœuds respectifs.

Si vous lancez plusieurs clusters (ou créez et détruyez un seul cluster) avec la même configuration à des fins de test, il est fortement recommandé d’attribuer à chaque cluster un identifiant `initial-cluster-token` unique. En procédant ainsi, etcd peut générer des identifiants de cluster et de membre uniques pour chaque cluster, même s’ils ont exactement la même configuration. Cela protège etcd contre les interactions entre clusters, qui pourraient endommager les clusters.

etcd écoute sur [`listen-client-urls`][conf-listen-client] pour accepter le trafic client. Le membre etcd annonce les URL spécifiées dans [`advertise-client-urls`][conf-adv-client] aux autres membres, aux proxies et aux clients. Vérifiez que les `advertise-client-urls` sont accessibles depuis les clients prévus. Une erreur courante consiste à définir `advertise-client-urls` sur localhost ou à laisser la valeur par défaut si les clients distants doivent accéder à etcd.

Sur chaque machine, lancez etcd avec ces indicateurs :

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

Les paramètres de ligne de commande commençant par `--initial-cluster` seront ignorés lors des exécutions ultérieures de etcd. N'hésitez pas à supprimer les variables d'environnement ou les indicateurs de ligne de commande après le processus d'initialisation. Si des modifications de configuration sont nécessaires ultérieurement (par exemple, l'ajout ou la suppression de membres dans le cluster), consultez le guide [configuration en temps réel][runtime-conf].

### TLS {#tls}

etcd prend en charge la communication chiffrée via le protocole TLS. Les canaux TLS peuvent être utilisés pour la communication interne chiffrée entre pairs au sein du cluster ainsi que pour le trafic client chiffré. Cette section présente des exemples de configuration d’un cluster avec TLS pour les pairs et les clients. Des informations supplémentaires sur la prise en charge TLS par etcd sont disponibles dans le [guide de sécurité][security-guide].

#### Certificats auto-signés {#self-signed-certificates}

Un cluster utilisant des certificats auto-signés chiffrer le trafic et authentifier ses connexions. Pour démarrer un cluster avec des certificats auto-signés, chaque membre du cluster doit disposer d'une paire de clés unique (`member.crt`, `member.key`) signée par un certificat CA partagé du cluster (`ca.crt`) pour les connexions entre pairs et les connexions clients. Les certificats peuvent être générés en suivant l'exemple de configuration [TLS][tls-setup] d'etcd.

Sur chaque machine, etcd sera lancé avec ces indicateurs :

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### Certificats automatiques {#automatic-certificates}

Si le cluster nécessite une communication chiffrée mais ne requiert pas de connexions authentifiées, etcd peut être configuré pour générer automatiquement ses clés. Lors de l’initialisation, chaque membre crée son propre jeu de clés en fonction de ses adresses IP et hôtes annoncés.

Sur chaque machine, etcd sera lancé avec ces indicateurs :

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### Cas d'erreur {#error-cases}

Dans l’exemple suivant, nous n’avons pas inclus notre nouvel hôte dans la liste des nœuds énumérés. Si c’est un nouveau cluster, le nœud _doit_ être ajouté à la liste des membres initiaux du cluster.

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

Dans cet exemple, nous tentons de mapper un nœud (infra0) sur une adresse différente (127.0.0.1:2380) de celle qui est énumérée dans la liste du cluster (10.0.1.10:2380). Si ce nœud doit écouter sur plusieurs adresses, toutes ces adresses _doivent_ être indiquées dans la directive de configuration "initial-cluster".

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

Si un pair est configuré avec un ensemble différent d'arguments de configuration et tente de rejoindre ce cluster, etcd signalera une incompatibilité d'ID de cluster et quittera.

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## Découverte {#discovery}

Dans plusieurs cas, les adresses IP des pairs du cluster ne sont pas connues à l’avance. C’est fréquent lors de l’utilisation de fournisseurs de cloud ou lorsque le réseau utilise DHCP. Dans ces situations, au lieu de spécifier une configuration statique, utilisez un cluster etcd existant pour amorcer un nouveau cluster. Ce processus s’appelle la « découverte ».

Deux méthodes peuvent être utilisées pour la découverte :

* service de découverte etcd
* enregistrements DNS SRV

### etcd discovery {#etcd-discovery}

Pour mieux comprendre la conception du protocole du service de découverte, nous recommandons de lire la documentation du protocole du service de découverte [documentation][discovery-proto].

#### Durée de vie d'une URL de découverte {#lifetime-of-a-discovery-url}

Une URL de découverte identifie un cluster etcd unique. Au lieu de réutiliser une URL de découverte existante, chaque instance etcd partage une nouvelle URL de découverte pour amorcer le nouveau cluster.

En outre, les URL de découverte doivent être utilisées UNIQUEMENT pour le démarrage initial d’un cluster. Pour modifier la composition du cluster une fois qu’il est déjà en cours d’exécution, consultez le guide [reconfiguration en temps réel][runtime-conf].

#### Service de découverte etcd personnalisé {#custom-etcd-discovery-service}

La découverte utilise un cluster existant pour amorcer son démarrage. Si vous utilisez un cluster etcd privé, créez une URL comme suit :

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

En définissant la clé size à l’URL, une URL de découverte est créée avec une taille de cluster attendue de 3.

L'URL à utiliser dans ce cas sera `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` et les membres etcd utiliseront le répertoire `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` pour s'enregistrer au moment de leur démarrage.

**Chaque membre doit avoir un drapeau de nom différent spécifié. `Hostname` ou `machine-id` peut être un choix pertinent. Sinon, la découverte échouera en raison d'un nom en double.**

Nous lançons maintenant etcd avec les drapeaux pertinents pour chaque membre :

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

Cela obligera chaque membre à s'enregistrer auprès du service de découverte etcd personnalisé et à démarrer le cluster une fois que toutes les machines auront été enregistrées.

#### Service de découverte publique etcd {#public-etcd-discovery-service}

Si aucun cluster existant n'est disponible, utilisez le service de découverte publique hébergé sur `discovery.etcd.io`. Pour créer une URL de découverte privée à l'aide de l'endpoint « new », utilisez la commande :

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Cela créera le cluster avec une taille initiale de 3 membres. Si aucune taille n'est spécifiée, une valeur par défaut de 3 est utilisée.

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**Chaque membre doit disposer d'un indicateur de nom différent, faute de quoi la découverte échouera en raison de noms en double. `Hostname` ou `machine-id` peut être un bon choix.**

Nous lançons maintenant etcd avec les drapeaux pertinents pour chaque membre :

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Cela obligera chaque membre à s'enregistrer auprès du service de découverte et à démarrer le cluster une fois que tous les membres auront été enregistrés.

Utilisez la variable d'environnement `ETCD_DISCOVERY_PROXY` pour obliger etcd à utiliser un proxy HTTP afin de se connecter au service de découverte.

#### Cas d'erreur et d'avertissement {#error-and-warning-cases}

##### Erreurs du serveur de découverte {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### Avertissements {#warnings}

Il s'agit d'un avertissement inoffensif indiquant que l'URL de découverte sera ignorée sur cette machine.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### Découverte DNS {#dns-discovery}

Les enregistrements SRV [DNS][rfc-srv] peuvent être utilisés comme mécanisme de découverte.
L'option `--discovery-srv` peut être utilisée pour définir le nom de domaine DNS où les enregistrements SRV de découverte sont situés.
La configuration `--discovery-srv example.com` entraîne la recherche des enregistrements SRV dans l'ordre indiqué :

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

Si `_etcd-server-ssl._tcp.example.com` est trouvé, etcd tentera le processus d'amorçage via TLS.

Afin d’aider les clients à découvrir le cluster etcd, les enregistrements DNS SRV suivants sont recherchés dans l’ordre indiqué :

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

Si `_etcd-client-ssl._tcp.example.com` est présent, les clients tenteront de communiquer avec le cluster etcd via SSL/TLS.

Si etcd utilise TLS, l'enregistrement SRV de découverte (par exemple `example.com`) doit être inclus dans les SAN DNS du certificat SSL en plus de l'hôte, faute de quoi le cluster échouera avec des messages d'erreur similaires aux suivants :

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

Si etcd utilise TLS sans autorité de certification personnalisée, le domaine de découverte (par exemple, example.com) doit correspondre au domaine de l’enregistrement SRV (par exemple, infra1.example.com). Cela permet de limiter les attaques visant à falsifier des enregistrements SRV afin de les faire pointer vers un domaine différent ; le domaine cible aurait alors un certificat valide selon la PKI, mais serait contrôlé par un tiers inconnu.

L'option `-discovery-srv-name` configure en outre un suffixe dans le nom SRV interrogé lors de la découverte.
Utilisez cette option pour distinguer plusieurs clusters etcd situés sous le même domaine.
Par exemple, si `discovery-srv=example.com` et `-discovery-srv-name=foo` sont définis, les requêtes DNS SRV suivantes sont effectuées :

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### Créer des enregistrements DNS SRV {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### Initialiser le cluster etcd à l'aide du DNS {#bootstrap-the-etcd-cluster-using-dns}

Les membres d’un cluster etcd peuvent annoncer des noms de domaine ou des adresses IP ; le processus d’initialisation résoudra les enregistrements A DNS.
À compter de la version 3.2 (la version 3.1 affiche des avertissements), `--listen-peer-urls` et `--listen-client-urls` rejettent les noms de domaine pour la liaison sur l’interface réseau.

L'adresse résolue dans `--initial-advertise-peer-urls` *doit correspondre* à l'une des adresses résolues figurant dans les cibles SRV. Le membre etcd lit l'adresse résolue afin de déterminer s'il appartient au cluster défini dans les enregistrements SRV.

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

Le cluster peut également amorcer son démarrage à l’aide d’adresses IP au lieu de noms de domaine :

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

Depuis la version 3.1.0 (sauf la version 3.2.9), lorsque `etcd --discovery-srv=example.com` est configuré avec TLS, le serveur n’authentifie les pairs ou clients que si les certificats fournis comportent comme entrée dans le champ Nom alternatif du sujet (SAN) le domaine racine `example.com`. Voir [Notes sur le DNS SRV][security-guide-dns-srv].

### Passerelle {#gateway}

Le passerelle etcd est un proxy TCP simple qui achemine les données réseau vers le cluster etcd. Veuillez consulter le guide [gateway][gateway] pour plus d'informations.

### Proxy {#proxy}

Lorsque le drapeau `--proxy` est défini, etcd s'exécute en mode proxy [proxy mode][proxy]. Ce mode proxy ne prend en charge que l'API etcd v2 ; aucune mise en œuvre de l'API v3 n'est prévue. En revanche, pour la prise en charge de l'API v3, un nouveau proxy doté de fonctionnalités améliorées sera disponible après la sortie d'etcd 3.0.

Pour configurer un cluster etcd avec des proxys de l'API v2, veuillez consulter le document [clustering][clustering_etcd2] de la version 2.3 d'etcd.

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /fr/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /fr/etcd/op-guide/configuration/#member
[discovery-proto]: /fr/etcd/dev-internal/discovery_protocol/
[gateway]: /fr/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /fr/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /fr/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /fr/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /fr/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
