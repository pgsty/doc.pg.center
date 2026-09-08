---
title: Modèle de sécurité du transport
weight: 4125
description: Sécurisation des données en transit
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/op-guide/security.md"
aliases: [/etcd/op-guide/security/]
---

etcd prend en charge le chiffrement TLS automatique ainsi que l’authentification par certificats clients pour les communications clients vers serveur, ainsi que pour les communications entre pairs (serveur vers serveur / cluster). **Notez qu’etcd n’active pas par défaut l’authentification basée sur [RBAC][auth] ni la fonctionnalité d’authentification au niveau du transport afin de réduire les obstacles pour les utilisateurs débutants avec la base de données. En outre, modifier cette valeur par défaut constituerait une modification incompatible pour le projet, établie depuis 2013. Un cluster etcd qui n’active pas les fonctionnalités de sécurité peut exposer ses données à tout client.**

Pour démarrer, disposez tout d’abord d’un certificat CA et d’une paire de clés signées pour un membre. Il est recommandé de créer et de signer une nouvelle paire de clés pour chaque membre d’un cluster.

Pour plus de commodité, l'outil [cfssl] propose une interface simplifiée pour la génération de certificats, et nous fournissons un exemple utilisant cet outil [ici][tls-setup]. En alternative, consultez ce [guide pour générer des paires de clés auto-signées][tls-guide].

La liste des indicateurs fournie ci-dessous peut ne pas être à jour en raison des modifications en cours de développement. Pour obtenir la liste des indicateurs disponibles, exécutez `etcd --help` ou consultez l’aide de [etcd][].

## Configuration de base {#basic-setup}

etcd prend plusieurs options de configuration liées aux certificats, soit par des drapeaux en ligne de commande, soit par des variables d'environnement :

**Communication client-serveur :**

`--cert-file=<path>` : Certificat utilisé pour les connexions SSL/TLS **vers** etcd. Lorsque cette option est définie, advertise-client-urls peut utiliser le schéma HTTPS.

`--key-file=<path>` : Clé du certificat. Doit être non chiffrée.

`--client-cert-auth` : Lorsque cette option est définie, etcd vérifie que toutes les requêtes HTTPS entrantes incluent un certificat client signé par l'autorité de certification fiable. Les requêtes ne fournissant pas de certificat client valide échoueront. Si [authentification][auth] est activée, le certificat fournit les identifiants pour le nom d'utilisateur indiqué dans le champ Common Name.

`--trusted-ca-file=<path>`: Autorité de certification de confiance.

`--auto-tls` : Utilisez des certificats auto-signés générés automatiquement pour les connexions TLS avec les clients.

**Communication entre pairs (serveur vers serveur / cluster) :**

Les options de pair fonctionnent de la même manière que les options client-serveur :

`--peer-cert-file=<path>` : Certificat utilisé pour les connexions SSL/TLS entre pairs. Ce certificat sera utilisé à la fois pour écouter sur l'adresse de pair et pour envoyer des requêtes aux autres pairs.

`--peer-key-file=<path>` : Clé du certificat. Doit être non chiffrée.

`--peer-client-cert-auth` : Lorsqu'il est défini, etcd vérifie que toutes les requêtes entrantes de pair provenant du cluster sont accompagnées de certificats clients valides signés par l'autorité de certification fournie.

`--peer-trusted-ca-file=<path>`: Autorité de certification de confiance.

`--peer-auto-tls` : Utilisez des certificats auto-signés générés automatiquement pour les connexions TLS entre pairs.

Si un certificat client-serveur ou un certificat pair est fourni, la clé doit également être définie. Toutes ces options de configuration sont également disponibles via les variables d'environnement, `ETCD_CA_FILE`, `ETCD_PEER_CA_FILE` et ainsi de suite.

**Options communes :**

`--cipher-suites` : Liste séparée par des virgules des suites de chiffrement TLS prises en charge entre le serveur/client et les pairs (vide, automatiquement rempli par Go).

`--tls-min-version=<version>` Définit la version minimale TLS prise en charge par etcd.

`--tls-max-version=<version>` Définit la version TLS maximale prise en charge par etcd. Si ce paramètre n'est pas défini, la version maximale prise en charge par Go sera utilisée.

### Usage de clé et extendedKeyUsage du certificat TLS {#tls-certificate-keyusage-and-extendedkeyusage}

Lors de la génération de certificats X.509 pour sécuriser le transport etcd,
les certificats doivent inclure les champs `keyUsage` et `extendedKeyUsage` appropriés selon leur rôle.
etcd s’appuie sur les bibliothèques `crypto/tls` et `crypto/x509` de Go pour la vérification des certificats,
qui imposent ces utilisations lors de la négociation TLS.

Le tableau suivant résume les utilisations recommandées pour les rôles de certificat courants :

| Rôle du certificat | keyUsage | extendedKeyUsage |
| ------------------- | -------- | ---------------- |
| Serveur (client vers serveur) | digitalSignature, keyEncipherment | serverAuth |
| Client | digitalSignature, keyEncipherment | clientAuth |
| Pair (serveur vers serveur) | digitalSignature, keyEncipherment | serverAuth, clientAuth |

Notes :

- Lorsque `--peer-client-cert-auth` est activé, les certificats de pair sont utilisés pour établir une TLS mutuelle entre les membres etcd, ce qui impose l'utilisation de `serverAuth` et de `clientAuth`.
- Les certificats clients utilisés avec `--client-cert-auth` doivent inclure `clientAuth`.

## Exemple 1 : Sécurité du transport client-serveur avec HTTPS {#example-1-client-to-server-transport-security-with-https}

Pour cela, préparez un certificat d'autorité de certification (`ca.crt`) et une paire de clés signées (`server.crt`, `server.key`).

Configurons etcd pour fournir une sécurité de transport HTTPS simple étape par étape :

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

Cela devrait démarrer correctement, et il sera possible de tester la configuration en utilisant HTTPS avec etcd :

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

La commande doit indiquer que la négociation a réussi. Étant donné que nous utilisons des certificats auto-signés avec notre propre autorité de certification, il est nécessaire de transmettre l'autorité de certification à curl en utilisant l'option `--cacert`. Une autre possibilité consisterait à ajouter le certificat de l'autorité de certification au répertoire des certificats fiables du système (généralement situé dans `/etc/pki/tls/certs` ou `/etc/ssl/certs`).

**Utilisateurs OSX 10.9+** : curl 7.30.0 sous OSX 10.9+ ne comprend pas les certificats passés en ligne de commande.
Au lieu de cela, importez directement le certificat dummy ca.crt dans la clé, ou ajoutez le drapeau `-k` à curl pour ignorer les erreurs.
Pour tester sans le drapeau `-k`, exécutez `open ./tests/fixtures/ca/ca.crt` et suivez les invites.
Veuillez supprimer ce certificat après le test !
Si une solution de contournement existe, faites-le nous savoir.

## Exemple 2 : Authentification client-serveur avec des certificats clients HTTPS {#example-2-client-to-server-authentication-with-https-client-certificates}

Pour l'instant, nous avons donné au client etcd la capacité de vérifier l'identité du serveur et de garantir la sécurité du transport. Nous pouvons toutefois également utiliser des certificats clients pour empêcher l'accès non autorisé à etcd.

Les clients fourniront leurs certificats au serveur, qui vérifiera que le certificat est signé par l'autorité de certification fournie et décidera s'il convient de traiter la requête.

Les mêmes fichiers mentionnés dans le premier exemple sont nécessaires pour cela, ainsi qu'une paire de clés pour le client (`client.crt`, `client.key`) signée par la même autorité de certification.

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

Essayez maintenant la même requête quʼau-dessus sur ce serveur :

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

La requête doit être rejetée par le serveur :

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

Pour y parvenir, nous devons fournir au serveur un certificat client signé par l'autorité de certification :

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

La sortie doit inclure :

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

Et également la réponse du serveur :

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

Spécifiez les suites de chiffrement à bloquer [suites de chiffrement TLS faibles](https://github.com/etcd-io/etcd/issues/8320).

L’établissement de la mainshaking TLS échouerait lorsque le client Hello est demandé avec des suites de chiffrement non valides.

Par exemple :

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

Ensuite, les requêtes clientes doivent préciser l’un des suites de chiffrement spécifiées sur le serveur :

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## Exemple 3 : Sécurité du transport et certificats clients dans un cluster {#example-3-transport-security--client-certificates-in-a-cluster}

etcd prend en charge le même modèle que ci-dessus pour la **communication entre pairs**, ce qui signifie la communication entre les membres d'un cluster etcd.

En supposant que nous disposons de notre `ca.crt` et de deux membres équipés de leurs propres paires de clés (`member1.crt` & `member1.key`, `member2.crt` & `member2.key`) signées par cette autorité de certification, nous lançons etcd comme suit :


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Les membres etcd formeront un cluster et toutes les communications entre les membres du cluster seront chiffrées et authentifiées à l’aide des certificats clients. La sortie d’etcd indiquera que les adresses auxquelles il se connecte utilisent HTTPS.

## Exemple 4 : Sécurité de transport auto-signée automatique {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> Lorsque vous spécifiez ClientAutoTLS et PeerAutoTLS, la période de validité du certificat client et du certificat pair automatiquement générés par etcd est limitée à 1 an. Vous pouvez utiliser le drapeau --self-signed-cert-validity pour définir la période de validité du certificat en années.

Dans les cas où une encryption de la communication est requise, mais pas une authentification, etcd prend en charge le chiffrement de ses messages à l’aide de certificats auto-signés générés automatiquement. Cela simplifie le déploiement, car il n’est pas nécessaire de gérer séparément les certificats et les clés en dehors d’etcd.
Configurez etcd pour utiliser des certificats auto-signés pour les connexions clientes et entre pairs à l’aide des indicateurs `--auto-tls` et `--peer-auto-tls` :

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Les certificats auto-signés ne vérifient pas l'identité, donc curl renverra une erreur :

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

Pour désactiver la vérification de la chaîne de certificats, exécutez curl avec le drapeau `-k` :

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## Notes relatives au DNS SRV {#notes-for-dns-srv}

Depuis la version 3.1.0 (sauf 3.2.9), le démarrage par découverte SRV authentifie `ServerName` à l’aide d’un nom de domaine racine provenant du drapeau `--discovery-srv`. Ceci vise à prévenir les attaques de type « homme du milieu » basées sur les certificats, en exigeant que le certificat possède un nom de domaine racine correspondant dans son champ Nom alternatif du sujet (SAN). Par exemple, `etcd --discovery-srv=etcd.local` n’authentifiera les pairs ou clients que si les certificats fournis incluent `etcd.local` comme entrée dans le champ Nom alternatif du sujet (SAN).

## Notes sur le proxy etcd {#notes-for-etcd-proxy}

Le proxy etcd termine le TLS provenant de son client si la connexion est sécurisée, puis utilise sa propre clé/certificat spécifiés dans `--peer-key-file` et `--peer-cert-file` pour communiquer avec les membres etcd.

Le proxy communique avec les membres etcd à l’aide des `--advertise-client-urls` et `--advertise-peer-urls` d’un membre donné. Il achemine les requêtes clientes vers les URL de client annoncées des membres etcd, et synchronise la configuration initiale du cluster à l’aide des URL de pair annoncées des membres etcd.

Lorsqu'une authentification client est activée pour un membre etcd, l'administrateur doit s'assurer que le certificat pair spécifié dans l'option `--peer-cert-file` du proxy est valide pour cette authentification. Le certificat pair du proxy doit également être valide pour l'authentification pair si l'authentification pair est activée.

## Notes sur l'authentification TLS {#notes-for-tls-authentication}

Depuis [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [les certificats TLS sont rechargés à chaque connexion client](https://github.com/etcd-io/etcd/pull/7829). Cela est utile pour remplacer des certificats expirés sans arrêter les serveurs etcd ; cela peut être réalisé en écrasant les anciens certificats par de nouveaux. Le rechargement des certificats à chaque connexion ne devrait pas entraîner un surcroît de charge important, mais pourrait être amélioré à l’avenir grâce à une couche de mise en mémoire tampon. Des exemples de tests sont disponibles [ici](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757).

Depuis [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [le serveur refuse les certificats pairs entrants comportant une IP incorrecte `SAN`](https://github.com/etcd-io/etcd/pull/7687). Par exemple, si le certificat pair contient des adresses IP dans le champ Nom alternatif du sujet (SAN), le serveur authentifie un pair uniquement lorsque l'adresse IP distante correspond à l'une de ces adresses. Ceci vise à empêcher les points de terminaison non autorisés de rejoindre le cluster. Par exemple, la demande de signature de certificat (CSR) du pair B (avec `cfssl`) est :

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

Lorsque l'adresse IP réelle du pair B est `10.138.0.2`, et non `10.138.0.27`. Lorsque le pair B tente de rejoindre le cluster, le pair A rejette B avec l'erreur `x509: certificate is valid for 10.138.0.27, not 10.138.0.2`, car l'adresse IP distante de B ne correspond pas à celle figurant dans le champ Nom alternatif (SAN).

Depuis [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [server résout le TLS `DNSNames` lors de la vérification `SAN`](https://github.com/etcd-io/etcd/pull/7767). Par exemple, si le certificat pair ne contient que des noms DNS (aucune adresse IP) dans le champ Nom alternatif du sujet (SAN), le serveur authentifie un pair uniquement lorsque les résolutions inverses (`dig b.com`) de ces noms DNS correspondent à l'adresse IP distante. Par exemple, la demande de signature de certificat (CSR) du pair B (avec `cfssl`) est :

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

Lorsque l'adresse IP distante du pair B est `10.138.0.2`. Lorsque le pair B tente de rejoindre le cluster, le pair A recherche l'hôte entrant `b.com` afin d'obtenir la liste des adresses IP (par exemple `dig b.com`). Il rejette B si la liste ne contient pas l'adresse IP `10.138.0.2`, avec l'erreur `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`.

Depuis [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07), [le serveur accepte les connexions si l'IP correspond, sans vérifier les entrées DNS](https://github.com/etcd-io/etcd/pull/8223). Par exemple, si le certificat du pair contient des adresses IP et des noms DNS dans le champ Nom alternatif du sujet (SAN), et que l'adresse IP distante correspond à l'une de ces adresses IP, le serveur accepte simplement la connexion sans vérifier davantage les noms DNS. Par exemple, la demande de signature de certificat (CSR) du pair B (avec `cfssl`) est :

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

Lorsque l'adresse IP distante du pair B est `10.138.0.2` et que `invalid.domain` est un hôte non valide. Lorsque le pair B tente de rejoindre le cluster, le pair A authentifie B avec succès, car le champ Nom alternatif du sujet (SAN) contient une adresse IP correspondante valide. Pour plus de détails, consultez [issue#8206](https://github.com/etcd-io/etcd/issues/8206).

Depuis [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04), [server prend en charge la recherche inverse sur les noms DNS avec caractères génériques `SAN`](https://github.com/etcd-io/etcd/pull/8281). Par exemple, si le certificat pair ne contient que des noms DNS (aucune adresse IP) dans le champ Subject Alternative Name (SAN), le serveur effectue d'abord une recherche inverse de l'adresse IP distante pour obtenir la liste des noms associés à cette adresse (par exemple, `nslookup IPADDR`). Ensuite, il accepte la connexion si ces noms correspondent à un nom du certificat pair (par correspondance exacte ou avec caractère générique). Si aucune correspondance n'est trouvée, le serveur effectue une recherche directe pour chaque entrée DNS du certificat pair (par exemple, recherche de `example.default.svc` lorsque l'entrée est `*.example.default.svc`), et accepte la connexion uniquement si les adresses résolues par l'hôte correspondent à l'adresse IP distante du certificat pair. Par exemple, la demande de signature de certificat (CSR) du pair B (avec `cfssl`) est :

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

Lorsque l'adresse IP distante du pair B est `10.138.0.2`. Lorsque le pair B tente de rejoindre le cluster, le pair A effectue une recherche inverse de l'IP `10.138.0.2` afin d'obtenir la liste des noms d'hôte. Il effectue ensuite une correspondance exacte ou avec caractère générique entre les noms d'hôte et les noms DNS du certificat du pair B dans le champ Nom alternatif du sujet (SAN). Si aucune recherche inverse ni forward n'a abouti, une erreur `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]` est renvoyée. Pour plus de détails, voir [issue#8268](https://github.com/etcd-io/etcd/issues/8268).

[v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) ajoute le drapeau [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616) pour prendre en charge l'authentification [CN (Common Name)-based pour les connexions inter-membres](https://github.com/etcd-io/etcd/issues/8262). Le démarrage TLS de Kubernetes consiste à générer des certificats dynamiques pour les membres et autres composants du système (par exemple, serveur API, kubelet, etc.). Maintenir des autorités de certification (CA) différentes pour chaque composant permet un contrôle d'accès plus strict sur le cluster etcd, mais peut s'avérer fastidieux. Lorsque le drapeau --peer-cert-allowed-cn est spécifié, un nœud ne peut se joindre qu'avec un nom commun correspondant, même avec des CA partagées. La correspondance est une comparaison exacte de chaîne par rapport au champ Common Name (CN) du certificat — aucune prise en charge des caractères génériques ou des correspondances par préfixe. Pour le filtrage basé sur le nom d'hôte utilisant --peer-cert-allowed-hostname ou --client-cert-allowed-hostname, la correspondance utilise x509.Certificate.VerifyHostname() de Go, qui prend en charge à la fois les noms d'hôte exacts et les entrées génériques (par exemple, *.example.com). Par exemple, chaque membre d'un cluster à 3 nœuds est configuré avec des demandes de signature de certificat (CSRs) (avec cfssl) comme suit :




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

Ensuite, seuls les pairs possédant un nom commun identique seront authentifiés si `--peer-cert-allowed-cn etcd.local` est fourni. Les nœuds présentant des CN différents dans les demandes de signature de certificat (CSR) ou un `--peer-cert-allowed-cn` différent seront rejetés :

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

Chaque processus doit être lancé avec :

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) et [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) corrigent le rechargement TLS lorsque [le champ SAN du certificat ne contient que des adresses IP, sans nom de domaine](https://github.com/etcd-io/etcd/issues/9541). Par exemple, un membre est configuré avec les CSR suivantes (avec `cfssl`) :

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

En Go, le serveur appelle `(*tls.Config).GetCertificate` pour recharger le TLS uniquement si le champ `(*tls.Config).Certificates` du serveur n'est pas vide, ou si `(*tls.ClientHelloInfo).ServerName` n'est pas vide et que le client fournit un SNI valide. Auparavant, etcd remplissait toujours `(*tls.Config).Certificates` lors de la première négociation TLS client, en le rendant non vide. Le client était donc toujours censé fournir un SNI correspondant afin de réussir la vérification TLS et de déclencher le rechargement des ressources TLS via `(*tls.Config).GetCertificate`.

Toutefois, un certificat dont le champ SAN ne contient [aucun nom de domaine, mais uniquement des adresses IP](https://github.com/etcd-io/etcd/issues/9541) demanderait `*tls.ClientHelloInfo` avec un champ `ServerName` vide, ce qui empêcherait le rechargement TLS lors de la première négociation TLS ; cela pose problème lorsque des certificats expirés doivent être remplacés en ligne.

Maintenant, `(*tls.Config).Certificates` est créé vide lors de la première poignée de main TLS client, d'abord pour déclencher `(*tls.Config).GetCertificate`, puis pour peupler le reste des certificats à chaque nouvelle connexion TLS, même lorsque le SNI client est vide (par exemple, lorsque le certificat ne contient que des adresses IP).

## Notes pour la liste blanche d'hôtes {#notes-for-host-whitelist}

L'indicateur `etcd --host-whitelist` spécifie les noms d'hôte acceptables provenant des requêtes HTTP clients. La politique d'origine des clients protège contre les attaques de type [« rebinding DNS »](https://en.wikipedia.org/wiki/DNS_rebinding) ciblant des serveurs etcd non sécurisés. En effet, tout site web peut simplement créer un nom DNS autorisé et rediriger ce nom vers `"localhost"` (ou toute autre adresse). Ainsi, tous les points de terminaison HTTP du serveur etcd écoutant sur `"localhost"` deviennent accessibles, exposant le serveur aux attaques de rebinding DNS. Pour plus de détails, consultez [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2).

Politique d’origine du client fonctionne comme suit :

1. Si la connexion cliente est sécurisée via HTTPS, autoriser n'importe quel nom d'hôte.
2. Si la connexion cliente n'est pas sécurisée et que `"HostWhitelist"` n'est pas vide, autoriser uniquement les requêtes HTTP dont le champ Host figure dans la liste blanche.

Notez que la politique d’origine du client est appliquée, qu’une authentification soit activée ou non, pour des contrôles plus stricts.

Par défaut, `etcd --host-whitelist` et `embed.Config.HostWhitelist` sont définis sur *vide* afin d'autoriser tous les noms d'hôte. Notez qu'en spécifiant des noms d'hôte, les adresses de boucle locale ne sont pas ajoutées automatiquement. Pour autoriser les interfaces de boucle locale, ajoutez-les manuellement à la liste blanche (par exemple `"localhost"`, `"127.0.0.1"`, etc.).

## Questions fréquemment posées {#frequently-asked-questions}

### Je constate une erreur d'alerte SSLv3 handshake lors de l'utilisation de l'authentification client TLS ? {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

Le paquet `crypto/tls` de `golang` vérifie l'utilisation autorisée de la clé publique du certificat avant de l'utiliser.
Pour utiliser la clé publique du certificat à des fins d'authentification client, il faut ajouter `clientAuth` à `Extended Key Usage` lors de la création de la clé publique du certificat.

Voici comment procéder :

Ajoutez la section suivante à OpenSSL.cnf :

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

Lors de la création du certificat, veillez à le référencer dans le drapeau `-extensions` :

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### Avec l'authentification par certificat pair, j'obtiens « le certificat est valide pour 127.0.0.1, pas pour $MY_IP » {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
Assurez-vous de signer les certificats avec un nom sujet correspondant à l'adresse IP publique du membre. L'outil `etcd-ca`, par exemple, propose une option `--ip=` pour sa commande `new-cert`.

Le certificat doit être signé pour le nom DNS complet (FQDN) du membre dans son champ « Sujet », utilisez les noms alternatifs du sujet (SAN courts, IP) pour ajouter l'adresse IP. L'outil `etcd-ca` propose l'option `--domain=` pour sa commande `new-cert`, et OpenSSL peut également générer [it][alt-name].

### etcd chiffre-t-il les données stockées sur les disques ? {#does-etcd-encrypt-data-stored-on-disk-drives}
No. etcd ne chiffre pas les données clé/valeur stockées sur les disques. Si un utilisateur doit chiffrer les données stockées dans etcd, plusieurs options sont disponibles :
* Faire chiffrer et déchiffrer les données par les applications clientes
* Utiliser une fonctionnalité du système de stockage sous-jacent pour chiffrer les données stockées, comme [dm-crypt]

### J'ai un avertissement dans les journaux indiquant que « le répertoire X existe sans les permissions recommandées -rwx------ » {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
Lorsque etcd crée certains répertoires nouveaux, il définit les permissions des fichiers à 700 afin de limiter au maximum l'accès non autorisé. Toutefois, si l'utilisateur a déjà créé un répertoire selon ses préférences, etcd utilise ce répertoire existant et affiche un message d'avertissement si les permissions diffèrent de 700.

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /fr/docs/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
