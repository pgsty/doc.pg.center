---
title: "5. Options de liaison et de serveur"
linkTitle: "5. Options bind et server"
weight: 160
description: "Options d'écouteur, de serveur, default-server et de résolution DNS"
icon: fa-solid fa-network-wired
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/bind-and-server-options/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 5"
---

Les mots-clés « bind », « server » et « default-server » prennent en charge un certain nombre de paramètres, selon certaines options de compilation et le système sur lequel HAProxy a été compilé. Ces paramètres sont généralement composés d’un mot, parfois suivi d’une valeur, écrits sur la même ligne que la directive « bind » ou « server ». Tous ces paramètres sont décrits dans cette section.

## 5.1. Options de liaison {#section-5-1}

Le mot-clé « bind » prend en charge un certain nombre de paramètres, tous transmis sous forme d'arguments sur la même ligne. L'ordre dans lequel ces arguments apparaissent n'a aucune importance, à condition qu'ils figurent après l'adresse bind. Tous ces paramètres sont facultatifs. Certains sont des mots simples (valeurs booléennes), tandis que d'autres exigent une valeur immédiatement après leur nom. Dans ce cas, la valeur doit être fournie sans interruption après le nom du paramètre.

Les paramètres actuellement pris en charge sont les suivants.

<a id="entry-5-1-accept-netscaler-cip"></a>

**`accept-netscaler-cip <magic number>`**

```haproxy
accept-netscaler-cip <magic number>
```

Force l'utilisation du protocole d'insertion de l'adresse IP client NetScaler sur toutes les connexions acceptées par l'un des sockets TCP déclarés sur la même ligne. Le protocole d'insertion de l'adresse IP client NetScaler indique les adresses couche 3/4 de la connexion entrante à utiliser partout où une adresse est utilisée, à l'exception des règles « tcp-request connection » qui ne verront que l'adresse réelle de la connexion. Les journaux reflètent les adresses indiquées dans le protocole, sauf en cas de violation, auquel cas l'adresse réelle est toujours utilisée. Ce mot-clé, combiné à un support provenant de composants externes, peut servir de solution alternative efficace et fiable au mécanisme X-Forwarded-For, qui n'est pas toujours fiable et même parfois inutilisable. Voir également « tcp-request connection expect-netscaler-cip » pour une configuration plus fine indiquant quels clients sont autorisés à utiliser le protocole.

<a id="entry-5-1-accept-proxy"></a>

**`accept-proxy`**

```haproxy
accept-proxy
```

Force l'utilisation du protocole PROXY sur toutes les connexions acceptées par l'un des sockets déclarés sur la même ligne. Les versions 1 et 2 du protocole PROXY sont prises en charge et détectées correctement. Le protocole PROXY indique les adresses couche 3/4 de la connexion entrante, qui seront utilisées partout où une adresse est requise, à l'exception des règles « tcp-request connection » qui ne verront que l'adresse réelle de la connexion. Les journaux reflètent les adresses indiquées dans le protocole, sauf en cas de violation, auquel cas l'adresse réelle sera utilisée. Ce mot-clé, combiné à la prise en charge par des composants externes, peut servir d’alternative efficace et fiable au mécanisme X-Forwarded-For, qui n’est pas toujours fiable et même parfois inutilisable. Voir également « tcp-request connection expect-proxy » pour une configuration plus fine de quels clients sont autorisés à utiliser le protocole.

<a id="entry-5-1-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Autoriser la réception de données anticipées lors de l'utilisation de TLSv1.3. Cette fonctionnalité est désactivée par défaut, en raison de considérations de sécurité. Étant donné qu'elle est vulnérable aux attaques par répétition, vous ne devez l’autoriser que pour les requêtes qui sont sans danger en cas de répétition, c’est-à-dire les requêtes idempotentes. Vous pouvez utiliser l’action « wait-for-handshake » pour toute requête qui ne serait pas sûre avec des données anticipées. Avec QUIC, le 0rtt est pris en charge avec QuicTLS, OpenSSL >= 3.5.2 et AWS-LC. Avec TCP/TLS, le 0rtt n’est pris en charge qu’avec OpenSSL, et nécessite que le client envoie un ALPN, sinon les données anticipées ne seront pas prises en compte avant que l’établissement de la connexion n’ait lieu.

<a id="entry-5-1-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Cela active l'extension TLS ALPN et annonce la liste de protocoles spécifiée comme prise en charge au-dessus d'ALPN. La liste de protocoles est constituée d'une liste séparée par des virgules de noms de protocoles, par exemple : "http/1.1,http/1.0" (sans guillemets). Cela nécessite que la bibliothèque SSL soit compilée avec le support des extensions TLS activé (vérifiez avec haproxy -vv). L'extension ALPN remplace l'extension NPN initiale. Au niveau du protocole, ALPN est obligatoire pour activer HTTP/2 sur un frontal HTTPS et HTTP/3 sur un frontal QUIC. Toutefois, lorsque ces frontaux n'ont aucun des paramètres "npn", "alpn" ou "no-alpn" définis, une valeur par défaut de "h2,http/1.1" sera utilisée pour un frontal HTTPS régulier, et "h3" pour un frontal QUIC. Les versions d'OpenSSL antérieures à 1.0.2 ne prennent pas en charge ALPN et ne supportaient que l'extension NPN désormais obsolète. Au moment de la rédaction de ce document, la plupart des navigateurs prennent encore en charge à la fois ALPN et NPN pour HTTP/2, de sorte qu'une bascule vers NPN peut encore fonctionner pendant un certain temps. Mais ALPN doit être utilisé chaque fois que possible. Les protocoles non annoncés ne sont pas négociés. Par exemple, il est possible d'accepter uniquement les connexions HTTP/2 avec ceci :

```text
bind :443 ssl crt pub.pem alpn h2  # explicitly disable HTTP/1.1
```

QUIC ne prend en charge que h3 et hq-interop comme ALPN. h3 est utilisé pour HTTP/3, tandis que hq-interop est utilisé pour http/0.9 et pour le test d'interopérabilité QUIC (voir <https://interop.seemann.io>). Chaque instruction « alpn » remplace la précédente. Pour les supprimer, utilisez « no-alpn ».

Notez que certains anciens navigateurs, comme Firefox 88, ont pu rencontrer des problèmes avec WebSocket sur H2, et dans un tel cas, il peut être nécessaire de désactiver explicitement HTTP/2 dans la chaîne "alpn" en la forçant à "http/1.1" ou "no-alpn", ou d'activer globalement l'option "h2-workaround-bogus-websocket-clients".

<a id="entry-5-1-backlog"></a>

**`backlog <backlog>`**

```haproxy
backlog <backlog>
```

Définit la file d'attente du socket à cette valeur. Si non spécifié ou égal à 0, la file d'attente du frontal est utilisée à la place, laquelle prend généralement la valeur maxconn par défaut.

<a id="entry-5-1-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Ce paramètre n'est disponible que si le support OpenSSL a été inclus. Il indique un fichier PEM à partir duquel charger les certificats CA utilisés pour vérifier le certificat du client. Il est possible de charger un répertoire contenant plusieurs CA ; dans ce cas, HAProxy tentera de charger chaque ".pem", ".crt", ".cer", ainsi que chaque fichier .crl présent dans le répertoire. Les fichiers commençant par un point sont ignorés.

Avertissement : Le paramètre "@system-ca" peut être utilisé à la place de cafile afin d'utiliser les certificats CA fiables de votre système, comme cela est fait avec la directive server. Toutefois, vous ne devez pas l'utiliser à moins de savoir ce que vous faites. Configurer cela signifie essentiellement que la liaison acceptera tout certificat client généré à partir d'une des autorités de certification présentes sur votre système, ce qui est extrêmement dangereux.

<a id="entry-5-1-ca-ignore-err"></a>

**`ca-ignore-err [all|<errorID>,...]`**

```haproxy
ca-ignore-err [all|<errorID>,...]
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Définit une liste séparée par des virgules d'identifiants d'erreur à ignorer lors de la vérification à une profondeur supérieure à 0. Il peut s'agir d'un identifiant numérique ou du nom de constante (X509_V_ERR), disponible dans la documentation OpenSSL : <https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES>. Il est recommandé d'utiliser le nom de constante, car la valeur numérique peut évoluer dans les nouvelles versions d'OpenSSL. Si cette option est définie sur « all », toutes les erreurs sont ignorées. La négociation SSL n'est pas interrompue si une erreur est ignorée.

<a id="entry-5-1-ca-sign-file"></a>

**`ca-sign-file <cafile>`**

```haproxy
ca-sign-file <cafile>
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il indique un fichier PEM contenant à la fois le certificat de l'autorité de certification (CA) et la clé privée de la CA utilisées pour créer et signer les certificats serveur. Il s'agit d'un paramètre obligatoire lorsque la génération dynamique des certificats est activée. Voir « generate-certificates » pour plus de détails.

<a id="entry-5-1-ca-sign-pass"></a>

**`ca-sign-pass <passphrase>`**

```haproxy
ca-sign-pass <passphrase>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il correspond à la phrase secrète de la clé privée de l'autorité de certification. Ce paramètre est facultatif et n'est utilisé que lorsque la génération dynamique des certificats est activée. Voir « generate-certificates » pour plus de détails.

<a id="entry-5-1-ca-verify-file"></a>

**`ca-verify-file <cafile>`**

```haproxy
ca-verify-file <cafile>
```

Ce paramètre indique un fichier PEM à partir duquel charger les certificats CA utilisés pour vérifier le certificat du client. Il désigne les certificats CA qui ne doivent pas être inclus dans les noms de CA envoyés dans le message de salutation du serveur. En général, « ca-file » doit être défini avec les certificats intermédiaires, et « ca-verify-file » avec les certificats finalisant la chaîne, comme la CA racine.

<a id="entry-5-1-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Ce paramètre n'est disponible que sur les systèmes définissant TCP_CONGESTION, et a été validé sur Linux et FreeBSD. Il prend le nom d'un algorithme de contrôle de congestion TCP et configure l'écouteur pour qu'il utilise cet algorithme sur toutes les connexions acceptées par cet écouteur. Les noms courants incluent « reno », « cubic », et dépendent du système d'exploitation. Sur certains systèmes, des autorisations spéciales peuvent être nécessaires pour configurer certains algorithmes. Sur Linux, la liste des algorithmes disponibles se trouve dans le sysctl "net.ipv4.tcp_available_congestion_control", et la liste de ceux autorisés sans privilèges se trouve dans "net.ipv4.tcp_allowed_congestion_control". Pour accéder aux algorithmes nécessitant des autorisations supplémentaires, la capacité "cap_net_admin" peut être requise (voir « setcap » dans la section globale). En cas d'échec de configuration d'un algorithme de contrôle de congestion spécifique, l'algorithme par défaut reste inchangé et un avertissement est émis pour signaler le problème. Voir également : le mot-clé serveur « cc » ([section 5.2](/fr/haproxy/bind-and-server-options/#section-5-2)). Exemple :

```text
frontend public
    bind :443 cc bbr   # use the BBR algorithm for high bandwidths
```

<a id="entry-5-1-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de chiffrement ("cipher suite") négociés lors de l'établissement de la connexion SSL/TLS jusqu'à TLSv1.2. Le format de la chaîne est défini dans « man 1 ciphers » des pages de documentation OpenSSL. Pour des informations complémentaires et des recommandations, consulter par exemple (<https://wiki.mozilla.org/Security/Server_Side_TLS>) et (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Pour la configuration des chiffrements TLSv1.3, se référer à la directive « ciphersuites ».

<a id="entry-5-1-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré et si OpenSSL 1.1.1 ou une version ultérieure a été utilisée pour compiler HAProxy. Il définit la chaîne décrivant la liste des algorithmes de chiffrement ("cipher suite") négociés lors de la négociation TLSv1.3. Le format de la chaîne est défini dans « man 1 ciphers » des pages de documentation OpenSSL, dans la section « ciphersuites ». Pour la configuration des chiffrements TLSv1.2 et versions antérieures, veuillez consulter le mot-clé « ciphers ». Ce paramètre peut accepter des suites de chiffrement TLSv1.2, mais cette fonctionnalité n'est pas documentée et n'est pas recommandée, car elle pourrait être incohérente ou défaillante. Les suites de chiffrement TLSv1.3 par défaut d'OpenSSL sont :
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 ne prend en charge que 5 suites de chiffrement :

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Exemple :

```text
ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-5-1-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de signature liés à l'authentification cliente qui sont négociés. Le format de la chaîne est défini dans « man 3 SSL_CTX_set1_client_sigalgs » des pages de documentation OpenSSL. Il est déconseillé d'utiliser ce paramètre si aucun cas d'utilisation spécifique n'a été identifié.

<a id="entry-5-1-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il indique un fichier PEM à partir duquel charger la liste de révocation de certificats utilisée pour vérifier le certificat du client. Vous devez fournir une liste de révocation de certificats pour chaque certificat de votre chaîne d'autorité de certification.

<a id="entry-5-1-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Ce paramètre n'est disponible que lorsque le support d'OpenSSL a été intégré.

HAProxy utilise un système de mise en cache : les fichiers sont chargés une seule fois dans le stockage des certificats, et chaque mot-clé « crt » suivant utilise cette version mise en cache. Lorsqu’un certificat est déclaré dans un « crt-store », le stockage des certificats est peuplé à partir de ce dernier et ne tente pas de charger des fichiers supplémentaires en détectant les extensions de fichier.

Il désigne un fichier PEM contenant à la fois les certificats requis et les clés privées associées.
Ce fichier peut être construit en concaténant plusieurs fichiers PEM en un seul (par exemple : cat cert.pem key.pem > combined.pem). Si votre autorité de certification exige un certificat intermédiaire, celui-ci peut également être concaténé dans ce fichier. Le certificat intermédiaire peut également être partagé via le répertoire indiqué par la directive « issuers-chain-path ».

Si le fichier ne contient pas de clé privée, HAProxy tentera de charger la clé au même chemin, suffixé par un ".key".

Si l'OpenSSL utilisé prend en charge le Diffie-Hellman, les paramètres présents dans ce fichier sont chargés.

Si un nom de répertoire est utilisé au lieu d'un fichier PEM, tous les fichiers trouvés dans ce répertoire seront chargés dans l'ordre alphabétique, sauf ceux dont le nom se termine par '.key', '.issuer', '.ocsp' ou '.sctl' (extensions réservées). Les fichiers commençant par un point sont également ignorés. Cette directive peut être spécifiée plusieurs fois afin de charger des certificats depuis plusieurs fichiers ou répertoires. Les certificats seront présentés aux clients qui fournissent un champ TLS Server Name Indication valide correspondant à l'un de leurs CN ou sujets alternatifs. Les caractères génériques sont pris en charge, où un caractère générique '\*' remplace le premier composant du nom d'hôte (par exemple, \*.example.org correspond à [www.example.org](http://www.example.org) mais pas à [www.sub.example.org](http://www.sub.example.org)). Si un répertoire vide est utilisé, HAProxy ne démarrera pas à moins que le mot-clé "strict-sni" soit utilisé.

Si aucun SNI n'est fourni par le client ou si la bibliothèque SSL ne prend pas en charge les extensions TLS, ou si le client fournit un nom d'hôte SNI ne correspondant à aucun certificat, alors le premier certificat chargé sera présenté. Cela signifie qu’en chargeant des certificats à partir d’un répertoire, il est fortement recommandé de charger en premier le certificat par défaut, soit sous forme de fichier, soit en veillant à ce qu’il soit toujours le premier dans le répertoire. Pour choisir plusieurs certificats par défaut (1 RSA et 1 ECDSA), il existe 3 options :

- Un bundle de certificats multiple peut être configuré comme le premier certificat (`crt foobar.pem` dans la configuration où les fichiers existants sont `foobar.pem.ecdsa` et `foobar.pem.rsa`).
- Ou un filtre '\*' pour chaque certificat dans une ligne crt-list.
- Le mot-clé 'default-crt' peut être utilisé.

Notez que le même certificat peut être chargé plusieurs fois sans effet secondaire.

Certaines autorités de certification (comme GoDaddy) proposent une liste déroulante de types de serveurs qui ne comprend pas HAProxy lors de l’obtention d’un certificat. Si cela se produit, veillez à sélectionner un serveur web que l’autorité de certification considère comme nécessitant une autorité de certification intermédiaire (pour GoDaddy, le choix d’Apache Tomcat permet d’obtenir le bundle correct, mais de nombreux autres, par exemple NGINX, entraînent un bundle erroné qui ne fonctionnera pas pour certains clients).

Pour chaque fichier PEM, HAProxy vérifie la présence d’un fichier au même chemin, suffixé par ".ocsp". Si un tel fichier est trouvé, le support de l’extension « Certificate Status Request » TLS (également appelée « OCSP stapling ») est activé automatiquement. Le contenu de ce fichier est facultatif. S’il n’est pas vide, il doit contenir une réponse OCSP valide au format DER. Pour être valide, une réponse OCSP doit respecter les règles suivantes : indiquer un statut « bon », être une réponse unique pour le certificat du fichier PEM, et être valide au moment de son ajout. Si ces règles ne sont pas respectées, la réponse OCSP est ignorée et un avertissement est émis. Pour identifier le certificat auquel une réponse OCSP s’applique, le certificat de l’émetteur est nécessaire. Si le certificat de l’émetteur n’est pas présent dans le fichier PEM, il sera chargé à partir d’un fichier situé au même chemin que le fichier PEM, suffixé par ".issuer". Si ce fichier n’existe pas, l’opération échoue avec une erreur.

Pour chaque fichier PEM, HAProxy vérifie également la présence d’un fichier au même chemin, suffixé par ".sctl". Si un tel fichier est trouvé, le support de l’extension TLS Certificate Transparency (RFC6962) est activé. Le fichier doit contenir une liste valide de timestamps de certificat signés, comme décrit dans le RFC. Le fichier est analysé pour vérifier sa syntaxe de base, mais aucune signature n’est vérifiée.

Il existe des cas où il est souhaitable de prendre en charge plusieurs types de clés, par exemple RSA et ECDSA dans les suites de chiffrement proposées aux clients. Cela permet aux clients prenant en charge les certificats EC d'utiliser des chiffrements EC, tout en continuant à supporter les clients plus anciens ne prenant en charge que RSA.

Pour y parvenir, OpenSSL 1.1.1 est requis. Vous pouvez configurer ce comportement en indiquant une entrée crt par type de certificat, ou en configurant un « bundle de certificats » comme cela était requis avant HAProxy 1.8. Voir « ssl-load-extra-files ».

<a id="entry-5-1-crt-ignore-err"></a>

**`crt-ignore-err <errors>`**

```haproxy
crt-ignore-err <errors>
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Définit une liste séparée par des virgules d'identifiants d'erreur à ignorer lors de la vérification à une profondeur == 0. Il peut s'agir d'un identifiant numérique ou du nom de constante (X509_V_ERR), disponible dans la documentation OpenSSL : <https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES>. Il est recommandé d'utiliser le nom de constante, car la valeur numérique peut évoluer dans les nouvelles versions d'OpenSSL. Si cette option est définie sur « all », toutes les erreurs sont ignorées. La négociation SSL n'est pas interrompue si une erreur est ignorée.

<a id="entry-5-1-crt-list"></a>

**`crt-list <file>`**

```haproxy
crt-list <file>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il désigne une liste de fichiers PEM, chacun pouvant inclure une configuration SSL optionnelle et un filtre SNI par certificat, selon le format suivant pour chaque ligne :

```text
<crtfile> [\[<sslbindconf> ...\]] [[!]<snifilter> ...]
```

Les lignes vides ainsi que les lignes commençant par un dièse ('#') seront ignorées.

La liste de certificats peut être modifiée dynamiquement via la socket de statistiques. (Voir « add ssl crt-list », « del ssl crt-list », « show ssl crt-list » dans le guide d'administration).

Les listes de certificats (crt-list) sont généralement des fichiers dédiés, mais un répertoire chargé avec la directive « crt » est représenté en interne comme une crt-list. La directive « ssl-f-use » dans un frontal déclare également une crt-list liée à ce frontal.

crtfile:

```text
Il s'agit du nom du fichier de certificat, ou d'un identifiant si le
certificat a été déclaré ailleurs (via la CLI ou avec un alias dans un
crt-store, par exemple).

Le même <crtfile> peut être utilisé sur plusieurs lignes avec des options
et des filtres différents.

Les ensembles multi-certificats (voir "ssl-load-extra-files") sont pris
en charge dans une crt-list si seul le nom de base est indiqué dans
<crtfile>. HAProxy duplique la ligne crt-list en interne et ajoute une
extension d'algorithme (.rsa, .ecdsa, .dsa) lors du chargement du fichier.
```

sslbindconf:

```text
 <sslbindconf> prend en charge les mots-clés suivants de la ligne bind
 (voir section 5.1. Options bind) :

 - allow-0rtt
 - alpn
 - ca-file
 - ca-verify-file
 - ciphers
 - ciphersuites
 - client-sigalgs
 - crl-file
 - curves
 - ecdhe
 - no-alpn
 - no-ca-names
 - npn
 - sigalgs
 - ssl-min-ver
 - ssl-max-ver
 - verify

 <sslbindconf> prend aussi en charge les mots-clés suivants du mot-clé
 load de crt-store (voir section 12.7.1. Options de chargement) :

 - crt
 - key
 - ocsp
 - issuer
 - sctl
 - ocsp-update

Les paramètres de la ligne bind sont hérités dans <sslbindconf> ;
s'ils ne sont pas précisés, les options par défaut sont héritées.
Les paramètres précisés dans <sslbindconf> remplacent les valeurs héritées.
```

snifilter :

```text
Lorsque le paramètre <snifilter> est utilisé sur une ligne crt-list,
les CN et SAN ne servent plus à sélectionner le certificat de cette
ligne pendant la négociation : <snifilter> est utilisé à leur place.

<snifilter> est une liste d'entrées séparées par des espaces. Elle peut
contenir des domaines ou des jokers au format DNS, avec un seul astérisque
comme premier caractère. Un domaine peut être exclu d'un joker par un
filtre négatif : '!' placé devant un domaine unique. Un ! placé devant
un * est ignoré. Les filtres négatifs sans joker sur la même ligne ne
sont pas pris en charge. L'entrée spéciale '*' désigne les certificats
par défaut utilisés en repli lorsqu'aucun domaine ne correspond.

Les certificats sont présentés aux clients fournissant un champ TLS
Server Name Indication valide correspondant à un filtre SNI, ou aux CN
et SAN d'un <crtfile>. L'algorithme cherche d'abord un domaine positif
dans la liste, puis un joker si aucun domaine n'est trouvé. Si un joker
correspond, haproxy vérifie les filtres négatifs de la même ligne et
écarte la correspondance si nécessaire. Avec plusieurs algorithmes
(RSA,ECDSA,DSA), HAProxy tente de trouver un certificat par type et
choisit celui que le client prend en charge.

Si le client ne présente pas de SNI ou si aucun certificat ne correspond,
un certificat par défaut est utilisé. L'option 'strict-sni' désactive
ce repli. Lorsque plusieurs certificats par défaut sont définis, HAProxy
choisit le certificat ECDSA ou RSA adapté aux capacités du client.

Le premier certificat déclaré sur une ligne bind est utilisé par défaut,
qu'il provienne de l'option crt ou crt-list.
Un filtre '*' ajoute aussi le certificat à la liste des certificats
par défaut. Pour clarifier la configuration, les certificats par défaut
peuvent être explicitement indiqués (avec un filtre '*') au début de
la liste, évitant l'ajout préalable d'un certificat par défaut implicite.
Comme les ensembles multi-certificats sont dupliqués pour chaque algorithme
dans la crt-list, un seul algorithme occupe la première ligne et est
considéré comme le certificat par défaut. Désignez l'ensemble entier
comme valeur par défaut avec le filtre '*' ou sur la ligne bind.

La commande "show ssl sni" sur le socket de statistiques permet de
déboguer la configuration. (Voir "show ssl sni" dans le guide de gestion)
```

Exemple :

```shell
# comment
default.pem.rsa *
default.pem.ecdsa *
cert2.pem [alpn h2,http/1.1]
certW.pem *.domain.tld !secure.domain.tld
certS.pem [curves X25519:P-256 ciphers ECDHE-ECDSA-AES256-GCM-SHA384] secure.domain.tld
foo.crt [key bar.pem ocsp foo.ocsp ocsp-update on] foo.bar.com
```

<a id="entry-5-1-default-crt"></a>

**`default-crt <cert>`**

```haproxy
default-crt <cert>
```

Cette option a le même effet que l'option « crt », à la différence que ce certificat sera également utilisé comme certificat par défaut. Il est possible d'ajouter plusieurs certificats par défaut afin d'avoir un certificat ECDSA et un certificat RSA ; en ajouter davantage n'est pas réellement utile.

Cette option ne désactive pas les certificats par défaut implicites. Si un certificat « crt » est déclaré en premier, avant tout « default-crt » ou tout autre « crt », il sera toujours utilisé comme certificat par défaut.

Un certificat par défaut est utilisé lorsque l'option « strict-sni » n'est pas spécifiée dans la ligne bind. Un certificat par défaut est fourni lorsque l'extension servername n'a pas été utilisée par le client, ou lorsque le nom de serveur ne correspond à aucun certificat configuré.

Exemple :

```shell
# this bind line has 2 default certificates
bind *:443 default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa crt website.pem.rsa

# this bind line has 3 default certificates
bind *:443 crt website.pem.rsa default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa
```

Voir également le mot-clé « crt ».

<a id="entry-5-1-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de courbes elliptiques ("suite de courbes") négociés lors de l'échange SSL/TLS avec ECDHE. Le format de la chaîne est une liste séparée par des deux-points de noms de courbes. Exemple : "X25519:P-256" (sans guillemets). Lorsque « curves » est défini, le paramètre « ecdhe » est ignoré.

<a id="entry-5-1-defer-accept"></a>

**`defer-accept`**

```haproxy
defer-accept
```

Est un mot-clé facultatif pris en charge uniquement sur certains noyaux Linux. Il indique qu'une connexion ne sera acceptée qu'après la réception de données, ou au pire après la première retransmission. Cette option doit être utilisée uniquement avec des protocoles pour lesquels le client parle en premier (par exemple, HTTP). Elle peut légèrement améliorer les performances en garantissant que la majeure partie de la requête est déjà disponible au moment de l'acceptation de la connexion. En revanche, elle ne permet pas de détecter les connexions qui ne transmettent aucune donnée. Il est important de noter que cette option est défectueuse sur tous les noyaux jusqu'à la version 2.6.31, car la connexion n'est jamais acceptée tant que le client ne parle pas. Cela peut entraîner des problèmes avec les pare-feu frontaux, qui perçoivent une connexion établie alors que le proxy ne la voit qu'en SYN_RECV. Cette option n'est prise en charge que sur les sockets TCPv4/TCPv6 et ignorée par les autres.

<a id="entry-5-1-ecdhe"></a>

**`ecdhe <named curve>`**

```haproxy
ecdhe <named curve>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la courbe nommée (RFC 4492) utilisée pour générer les clés temporaires ECDH. Par défaut, la courbe nommée utilisée est prime256v1.

<a id="entry-5-1-ech"></a>

**`ech <dir> [ EXPERIMENTAL ]`**

```haproxy
ech <dir> [ EXPERIMENTAL ]
```

Appliquez toutes les clés ECH provenant de `<dir>` à la ligne bind. Les fichiers doivent avoir l'extension .ech et utiliser le format de fichier PEM pour ECH. ( <https://datatracker.ietf.org/doc/draft-farrell-tls-pemesni/> )

Ce mot-clé active ECH en mode partagé, HAProxy agissant à la fois en tant que terminaison TLS et en tant que terminaison ECH. Voir <https://datatracker.ietf.org/doc/draft-ietf-tls-esni/>

Il s'agit d'une fonctionnalité expérimentale, qui nécessite l'option « expose-experimental-directives » dans la section globale. Elle exige également une version d'OpenSSL prenant en charge l'ECH (
<https://github.com/openssl/openssl/tree/feature/ech>), ainsi qu'une compilation de HAProxy avec USE_ECH=1.
L'API ECH d'AWS-LC n'est pas prise en charge.

Exemple :

```shell
$ openssl ech -public_name foobar.com -out /etc/haproxy/echkeydir/foobar.com.ech

$ cat haproxy.cfg
[...]
bind :443 ech /etc/haproxy/echkeydir/ ssl crt example.com.pem

// Use the ECHCONFIG section of your .ech file
$ openssl s_client -tls1_3 -connect example.com:443 -servername example.com \
-ech_config_list AD3+DQA5cwAgACB6ybtgtFYoM5r8nJSotus4c7K0EG..9vYmFyLmNvbQAA
```

<a id="entry-5-1-expose-fd-listeners"></a>

**`expose-fd listeners`**

```haproxy
expose-fd listeners
```

Cette option n’est utilisable qu’avec le socket de statistiques. Elle permet au socket de statistiques de transmettre le descripteur d’écouteur (FD) à un autre processus HAProxy. En mode maître-worker, cette fonctionnalité n’est plus nécessaire, les écouteurs étant transmis via les socketpairs internes entre le maître et les workers. Voir également "-x" dans le guide de gestion.

<a id="entry-5-1-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Cette option impose l'utilisation de SSLv3 uniquement sur les connexions SSL instanciées à partir de cet écouteur. SSLv3 est généralement moins coûteux que ses homologues TLS pour des débits de connexion élevés. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Cette option impose l'utilisation de TLSv1.0 uniquement sur les connexions SSL instanciées à partir de cet écouteur. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Cette option impose l'utilisation de TLSv1.1 uniquement sur les connexions SSL instanciées par cet écouteur. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Cette option impose l'utilisation de TLSv1.2 uniquement sur les connexions SSL instanciées par cet écouteur. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Cette option impose l'utilisation de TLSv1.3 uniquement sur les connexions SSL instanciées à partir de cet écouteur. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-generate-certificates"></a>

**`generate-certificates`**

```haproxy
generate-certificates
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il active la génération dynamique des certificats SSL. Un certificat de l'autorité de certification (CA) et sa clé privée sont nécessaires (voir « ca-sign-file »). Lorsqu'HAProxy est configuré en tant que proxy forward transparent, les requêtes SSL génèrent des erreurs en raison d'un désaccord sur le nom commun du certificat présenté au client. Avec cette option activée, HAProxy tentera de générer un certificat en utilisant le nom d'hôte SNI indiqué par le client. Cette opération n'est effectuée que si aucun certificat ne correspond au nom d'hôte SNI (voir « crt-list »).

En cas d'erreur de génération de certificat, la connexion bascule vers le certificat par défaut. Lorsque strict-sni est utilisé, le certificat par défaut n'est pas utilisé et la connexion entraîne un échec de négociation.

Il peut également être utilisé lorsque HAProxy est configuré en tant que proxy inverse pour faciliter le déploiement d'une architecture comprenant de nombreux backends.

La création d’un certificat SSL est une opération coûteuse, aussi un cache LRU est utilisé pour stocker des certificats falsifiés (voir 'tune.ssl.ssl-ctx-cache-size'). Cela augmente la consommation mémoire de HAProxy afin de réduire la latence lorsque le même certificat est utilisé plusieurs fois.

<a id="entry-5-1-gid"></a>

**`gid <gid>`**

```haproxy
gid <gid>
```

Définit le groupe des sockets UNIX sur le GID système indiqué. Ce paramètre peut également être défini par défaut dans l'instruction « unix-bind » de la section globale. Notez que certaines plates-formes ignorent simplement ce paramètre. Ce réglage est équivalent à l'option « group », à ceci près que l'identifiant de groupe est utilisé à la place de son nom. Ce paramètre est ignoré pour les sockets non UNIX.

<a id="entry-5-1-group"></a>

**`group <group>`**

```haproxy
group <group>
```

Définit le groupe des sockets UNIX sur le groupe système indiqué. Ce paramètre peut également être défini par défaut dans l'instruction « unix-bind » de la section globale. Notez que certaines plates-formes ignorent simplement ce paramètre. Ce paramètre est équivalent à l'option « gid », à ceci près que le nom du groupe est utilisé au lieu de son identifiant gid. Ce paramètre est ignoré pour les sockets non UNIX.

<a id="entry-5-1-guid-prefix"></a>

**`guid-prefix <string>`**

```haproxy
guid-prefix <string>
```

Génère des identifiants uniques globaux sensibles à la casse pour chaque socket d'écoute allouée sur cette ligne bind.
Le préfixe sera concaténé à l'indice de position de l'écouteur sur la ligne bind courante, en utilisant le caractère '-' comme séparateur.
Voir la description du mot-clé proxy « guid » pour plus d'informations sur son format. Voir également « shm-stats-file ».

<a id="entry-5-1-id"></a>

**`id <id>`**

```haproxy
id <id>
```

Fixe l'identifiant de socket. Par défaut, les identifiants de socket sont attribués automatiquement, mais il peut parfois être plus pratique de les fixer pour faciliter la surveillance. Cette valeur doit être strictement positive et unique au sein de l'écouteur/frontal. Cette option ne peut être utilisée que lors de la définition d'une seule socket.

<a id="entry-5-1-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Définir un intervalle pour le test de vivacité périodique sur les connexions frontales inactives. Si la partie distante ne parvient pas à répondre avant le prochain test planifié, la connexion est fermée. Sinon, le délai d'expiration client est actualisé et la connexion est maintenue. Notez que les temporisateurs http-request/http-keep-alive s'exécutent en parallèle et ne sont pas actualisés par idle-ping.

Cette fonctionnalité dépend d'un support spécifique du protocole sous-jacent. Pour l'instant, seul H2 mux l'implémente.
Idle-ping est simplement ignoré par les autres protocoles.

Cette option est particulièrement utile lors de l'utilisation d'un proxy inverse HTTP. La définir sur la ligne bind est utile pour le pair chargé d'établir activement les connexions et qui recevra ensuite le trafic entrant à travers celles-ci.

<a id="entry-5-1-interface"></a>

**`interface <interface>`**

```haproxy
interface <interface>
```

Restreint la socket à une interface spécifique. Lorsqu'elle est spécifiée, seuls les paquets reçus de cette interface particulière sont traités par la socket. Cette fonctionnalité n'est actuellement prise en charge que sous Linux. L'interface doit être une interface système primaire, et non une interface aliasée. Il est également possible de lier plusieurs frontaux à la même adresse si ceux-ci sont liés à des interfaces différentes. Notez que le lien à une interface réseau nécessite des privilèges root. Ce paramètre n'est compatible qu'avec les sockets TCPv4/TCPv6. Lorsqu'il est spécifié, le trafic de retour utilise la même interface que le trafic entrant, ainsi que sa table de routage associée, même si des routes explicites via des interfaces différentes sont configurées. Cela peut s'avérer utile pour résoudre les problèmes de routage asymétrique lorsque les mêmes adresses IP clientes doivent pouvoir atteindre des frontaux hébergés sur des interfaces différentes.

<a id="entry-5-1-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Active ou désactive kTLS pour ces sockets. Si activé, kTLS sera utilisé si le noyau le prend en charge et si le chiffrement est compatible. Cette fonctionnalité n'est disponible qu'avec le noyau Linux 4.17 et versions ultérieures. Veuillez noter que certains pilotes réseau et/ou piles TLS peuvent limiter l'utilisation de kTLS à TLS v1.2 uniquement. Voir également « force-tlsv12 ».

<a id="entry-5-1-label"></a>

**`label <label>`**

```haproxy
label <label>
```

Définit une étiquette facultative pour ces sockets. Elle peut servir à regrouper les sockets par étiquette, indépendamment de l'emplacement où les lignes bind ont été déclarées.

<a id="entry-5-1-level"></a>

**`level <level>`**

```haproxy
level <level>
```

Ce paramètre est utilisé uniquement avec les sockets de statistiques pour restreindre la nature des commandes pouvant être émises sur le socket. Il est ignoré par les autres sockets. `<level>` peut prendre l'une des valeurs suivantes :

-  « user » est le niveau de privilège le plus faible ; seules les statistiques non sensibles peuvent être lues, et aucune modification n'est autorisée. Ce niveau est pertinent sur les systèmes où il n'est pas facile de restreindre l'accès à la socket.
-  « operator » est le niveau par défaut et convient à la plupart des utilisations courantes. Toutes les données peuvent être lues, et seules les modifications non sensibles sont autorisées (par exemple, réinitialiser les compteurs max).
-  « admin » doit être utilisé avec précaution, car toutes les actions sont autorisées (par exemple, réinitialiser tous les compteurs).

<a id="entry-5-1-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Limite les sockets à ce nombre de connexions simultanées. Les connexions supplémentaires resteront dans la file d'attente du système jusqu'à ce qu'une connexion soit libérée. Si non spécifié, la limite sera identique à celle du frontal maxconn. Notez que, dans le cas de plages de ports ou d'adresses multiples, la même valeur sera appliquée à chaque socket. Ce paramètre permet d'imposer des limites différentes sur les sockets coûteux, par exemple les entrées SSL qui peuvent facilement consommer toute la mémoire.

<a id="entry-5-1-mode"></a>

**`mode <mode>`**

```haproxy
mode <mode>
```

Définit le mode octal utilisé pour définir les permissions d'accès sur le socket UNIX. Ce paramètre peut également être défini par défaut dans l'instruction « unix-bind » de la section globale. Notez que certaines plates-formes ignorent simplement ce paramètre. Ce paramètre est ignoré pour les sockets non UNIX.

<a id="entry-5-1-mss"></a>

**`mss <maxseg>`**

```haproxy
mss <maxseg>
```

Définit la valeur de la taille maximale du segment TCP (MSS) à annoncer sur les connexions entrantes. Cela peut être utilisé pour imposer une MSS plus faible pour des ports spécifiques, par exemple pour les connexions passant par un VPN. Notez que cette fonctionnalité repose sur une fonctionnalité du noyau qui est théoriquement prise en charge sous Linux, mais était défectueuse dans toutes les versions antérieures à 2.6.28. Elle peut ou non fonctionner sur d'autres systèmes d'exploitation. Elle peut également ne pas modifier la valeur annoncée, mais modifier la taille effective des segments sortants. La valeur couramment annoncée pour TCPv4 sur les réseaux Ethernet est 1460 = 1500 (MTU) - 40 (IP+TCP). Si cette valeur est positive, elle sera utilisée comme MSS annoncé. Si elle est négative, elle indiquera de combien réduire le MSS annoncé par la connexion entrante pour les segments sortants. Ce paramètre n'est compatible qu'avec les sockets TCP v4/v6.

<a id="entry-5-1-name"></a>

**`name <name>`**

```haproxy
name <name>
```

Définit un nom facultatif pour ces sockets, qui sera indiqué sur la page de statistiques.

<a id="entry-5-1-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

Sous Linux, il est possible de spécifier l'espace de noms réseau auquel un socket appartiendra. Cette directive permet de lier explicitement un écouteur à un espace de noms différent de celui par défaut. Veuillez vous référer à la documentation de votre système d'exploitation pour obtenir davantage de détails sur les espaces de noms réseau.

<a id="entry-5-1-nbconn"></a>

**`nbconn <nbconn> [ EXPERIMENTAL ]`**

```haproxy
nbconn <nbconn> [ EXPERIMENTAL ]
```

Ce paramètre n'est valable que pour les instances d'écouteur utilisant HTTP inverse. Il définit le nombre de connexions à monter en parallèle. Si non spécifié, une valeur par défaut de 1 est utilisée.

Le proxy HTTP inverse est actuellement toujours en développement actif. Le mécanisme de configuration peut évoluer à l’avenir. Pour cette raison, il est marqué en interne comme expérimental, ce qui signifie que la directive « expose-experimental-directives » doit apparaître sur une ligne précédant cette directive.

<a id="entry-5-1-nice"></a>

**`nice <nice>`**

```haproxy
nice <nice>
```

Définit la « gentillesse » des connexions initiées depuis la socket. La valeur doit être comprise dans la plage -1024..1024 inclusive, et vaut zéro par défaut. Les valeurs positives signifient que ces connexions sont plus favorables aux autres et cèdent facilement leur place au planificateur. À l’inverse, les valeurs négatives signifient que les connexions souhaitent s’exécuter avec une priorité plus élevée que les autres. La différence n’apparaît que sous de fortes charges, lorsque le système est proche de saturation. Les valeurs négatives conviennent aux services à faible latence ou aux services d’administration, tandis que des valeurs élevées sont généralement recommandées pour les tâches intensives en CPU, comme le traitement SSL ou les transferts en masse, qui sont moins sensibles à la latence. Par exemple, il peut être pertinent d’utiliser une valeur positive pour une socket SMTP et une valeur négative pour une socket RDP.

<a id="entry-5-1-no-alpn"></a>

**`no-alpn`**

```haproxy
no-alpn
```

Désactive le traitement ALPN (en pratique, cela définit la chaîne ALPN sur une chaîne vide qui ne sera pas annoncée). Permet d'annuler une occurrence précédente de la directive « alpn » et de désactiver la négociation de protocole d'application. Peut également être utilisé pour empêcher un écouteur de négocier ALPN avec un client sur un écouteur HTTPS ou QUIC ; par défaut, les écouteurs HTTPS annoncent « h2,http/1.1 » et les écouteurs QUIC annoncent « h3 ». Voir également « alpn » ci-dessus. Notez qu’en utilisant « crt-list », un certificat peut remplacer le paramètre « alpn » et réactiver son traitement.

<a id="entry-5-1-no-ca-names"></a>

**`no-ca-names`**

```haproxy
no-ca-names
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il empêche l'envoi des noms de certificat autorité de certification dans le message Server Hello lorsque ca-file est utilisé. Utilisez ca-verify-file à la place de ca-file avec no-ca-names.

<a id="entry-5-1-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive le support de SSLv3 sur tous les sockets instanciés à partir de l’écouteur lorsque le chiffrement SSL est activé. Notez que SSLv2 est forcé désactivé dans le code et ne peut pas être activé via aucune option de configuration. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-no-strict-sni"></a>

**`no-strict-sni`**

```haproxy
no-strict-sni
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive l'imposition stricte du SNI provenant d'une directive précédente « strict-sni ». Il peut être nécessaire pour désactiver sélectivement l'utilisation du SNI strict sur une ligne « bind » lorsque celle-ci était déjà imposée globalement via « ssl-default-bind-options ». Voir également l'option de liaison « strict-sni ».

<a id="entry-5-1-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive la reprise de session sans état (extension TLS Ticket RFC 5077) et force l'utilisation de la reprise de session avec état. La reprise de session sans état est plus coûteuse en utilisation du processeur. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Le mécanisme des tickets TLS n'est utilisé qu'avec TLS 1.2 au maximum. La confidentialité persistante est compromise avec les tickets TLS, sauf si les clés de ticket sont régulièrement renouvelées (par rechargement ou en utilisant « tls-ticket-keys »).

<a id="entry-5-1-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive le support de TLSv1.0 sur tous les sockets instanciés à partir de l'écouteur lorsque le support SSL est actif. Notez que SSLv2 est forcé désactivé dans le code et ne peut pas être activé à l'aide d'aucune option de configuration. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive le support de TLSv1.1 sur tous les sockets instanciés à partir de l’écouteur lorsque le support SSL est activé. Notez que SSLv2 est forcé désactivé dans le code et ne peut pas être activé à l’aide d’aucune option de configuration. Cette option est également disponible dans l’instruction globale « ssl-default-bind-options ». Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive le support de TLSv1.2 sur tous les sockets instanciés à partir de l’écouteur lorsque le support SSL est activé. Notez que SSLv2 est forcé désactivé dans le code et ne peut pas être activé à l’aide d’aucune option de configuration. Cette option est également disponible dans l’instruction globale « ssl-default-bind-options ». Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il désactive le support de TLSv1.3 sur tous les sockets instanciés à partir de l’écouteur lorsque le support SSL est actif. Notez que SSLv2 est forcé désactivé dans le code et ne peut pas être activé à l’aide d’aucune option de configuration. Cette option est également disponible dans l’instruction globale « ssl-default-bind-options ». Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-1-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Cela active l'extension TLS NPN et annonce la liste de protocoles spécifiée comme prise en charge au-dessus de NPN. La liste de protocoles est constituée d'une liste séparée par des virgules de noms de protocoles, par exemple :
"http/1.1,http/1.0" (sans guillemets). Cela nécessite que la bibliothèque SSL soit compilée avec le support des extensions TLS activé (vérifiez avec haproxy -vv). Notez que l'extension NPN a été remplacée par l'extension ALPN (voir le mot-clé « alpn »), bien que celle-ci ne soit disponible qu'à partir d'OpenSSL 1.0.2. Si HTTP/2 est requis sur une version plus ancienne d'OpenSSL, NPN peut encore être utilisé, la plupart des clients le supportant encore au moment de la rédaction de ce document. Il est possible d'activer à la fois NPN et ALPN, bien que cela n'ait probablement pas de sens en dehors d'un contexte de test.

Compatibilité : OpenSSL >= 1.0.1. Non pris en charge avec AWS-LC.

<a id="entry-5-1-prefer-client-ciphers"></a>

**`prefer-client-ciphers`**

```haproxy
prefer-client-ciphers
```

Utilisez la préférence du client lors du choix de la suite de chiffrement, la préférence du serveur étant appliquée par défaut. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ».

Notez qu’avec OpenSSL \>= 1.1.1, le chiffrement ChaCha20-Poly1305 est automatiquement priorisé (même sans définir cette option), si un chiffrement ChaCha20-Poly1305 figure en tête de la liste des chiffrements du client.

Lorsqu’un ensemble à algorithmes doubles (RSA + ECDSA) est utilisé, l’algorithme de sélection choisit entre RSA et ECDSA, en privilégiant toujours ECDSA. Une fois le certificat approprié sélectionné, c’est la bibliothèque SSL qui détermine la priorité des chiffrements, des courbes, etc. Par conséquent, cette option ne peut pas être utilisée pour privilégier un certificat RSA au détriment d’un certificat ECDSA.

<a id="entry-5-1-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Force le protocole du multiplexeur à utiliser pour les connexions entrantes. Il doit être compatible avec le mode du frontal (TCP ou HTTP). Il doit également être utilisable du côté du frontal. La liste des protocoles disponibles est indiquée par haproxy -vv. Les propriétés des protocoles sont les suivantes : le mode (TCP/HTTP), le côté (FE/BE), le nom du multiplexeur et ses drapeaux.

Certains protocoles sont sujets au blocage par tête de file côté serveur (drapeau=HOL_RISK). Enfin, certains protocoles ne prennent pas en charge les mises à jour (drapeau=NO_UPG). La compatibilité HTX est également indiquée (drapeau=HTX).

Voici les protocoles pouvant être utilisés en tant qu'argument de la directive « proto » dans une ligne bind :

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
 qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
 h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
 h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
 none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
```

L'idée derrière cette option est de contourner le choix du protocole du multiplexeur optimal pour toutes les connexions instanciées à partir de ce socket d'écoute. Par exemple, il est possible de forcer l'utilisation du protocole http/2 sur un TCP non chiffré en spécifiant « proto h2 » dans la ligne bind.

Si les paramètres ALPN ou NPN sont configurés, les protocoles spécifiés doivent être compatibles avec le protocole du multiplexeur afin d'éviter tout problème. Par exemple, si « proto h1 » est défini, l'ALPN ne doit pas être configuré sur « h2 ».

QMux est un sous-ensemble de QUIC qui s'exécute sur TCP. Il correspond au protocole proposé dans le brouillon suivant : <https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. Il est actuellement considéré comme expérimental dans HAProxy.

<a id="entry-5-1-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Il s'agit d'un paramètre spécifique à QUIC permettant de sélectionner l'algorithme de contrôle de congestion pour toute tentative de connexion aux écouteurs QUIC configurés. Ils sont similaires à ceux utilisés par TCP.

Le pacing est activé au-dessus de l'algorithme de congestion afin de réduire les pertes et améliorer le débit. Il peut être désactivé via le mot-clé global "tune.quic.fe.tx.pacing". Dans la plupart des cas, le pacing doit rester activé, notamment lors de l'utilisation de BBR, qui en dépend pour fonctionner comme prévu. Utiliser BBR sans pacing peut entraîner des ralentissements ou des taux élevés de pertes pendant les transferts.

Valeur par défaut : cubic

Pour une personnalisation supplémentaire, une liste de paramètres peut être spécifiée après le jeton d'algorithme. Elle doit être écrite entre parenthèses, séparée par des virgules. Chaque argument est facultatif et peut être vide si nécessaire. Voici l'ordre obligatoire de chaque paramètre :

- taille maximale de fenêtre en octets. Elle doit être supérieure à 10 ko et inférieure à 4 Go. Par défaut, la valeur « tune.quic.fe.cc.max-win-size » est utilisée.

Exemple :

```shell
# newreno congestion control algorithm
quic-cc-algo newreno
# cubic congestion control algorithm with one megabytes as window
quic-cc-algo cubic(1m)
```

Une valeur spéciale « nocc » peut être utilisée pour forcer une fenêtre de congestion fixe, toujours réglée à sa taille maximale. Elle est réservée aux scénarios de débogage afin d’éliminer tout effet secondaire causé par le contrôleur de congestion. Elle ne doit pas être utilisée en production, car elle peut rapidement entraîner des problèmes réseau tels qu’un taux élevé de perte de paquets.

<a id="entry-5-1-quic-force-retry"></a>

**`quic-force-retry`**

```haproxy
quic-force-retry
```

Il s'agit d'un paramètre spécifique à QUIC qui force l'utilisation de la fonctionnalité de réessai QUIC pour toutes les tentatives de connexion aux écouteurs QUIC configurés. Cette fonctionnalité consiste à vérifier que les pairs sont capables de recevoir des paquets à l'adresse de transport qu'ils ont utilisée pour initier une nouvelle connexion, en leur envoyant un paquet Retry contenant un jeton. Ce jeton doit être renvoyé au destinataire du paquet Retry, qui est le seul à pouvoir valider le jeton. Notez que le réessai QUIC sera toujours utilisé, même si un seuil de réessai a été défini (voir le paramètre "tune.quic.fe.sec.retry-threshold").

Ce paramètre nécessite que le secret du cluster soit défini, faute de quoi une erreur sera signalée au démarrage (voir « cluster-secret »).

Consultez <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2> pour plus d'informations sur le réessai QUIC.

<a id="entry-5-1-quic-socket"></a>

**`quic-socket [ connection | listener ]`**

```haproxy
quic-socket [ connection | listener ]
```

Ce paramètre spécifique à QUIC permet de définir le mode d'allocation de socket pour les écouteurs spécifiques.
Voir "tune.quic.fe.sock-per-conn" pour une description complète des avantages et inconvénients de chaque mode.

Ce paramètre s'applique conjointement avec l'option globale "tune.quic.fe.sock-per-conn". Si le mode « default-on » est activé au niveau du réglage global (valeur par défaut), chaque connexion QUIC utilisera son propre socket, sauf pour les écouteurs ayant pour configuration « quic-socket listener ». Toutefois, si le mode global est défini sur « force-off », la configuration individuelle de l'écouteur sera ignorée.

<a id="entry-5-1-severity-output"></a>

**`severity-output <format>`**

```haproxy
severity-output <format>
```

Ce paramètre est utilisé uniquement avec les sockets de statistiques pour configurer le niveau de sévérité inséré en préfixe des messages de retour informatifs. Le niveau de sévérité des messages peut varier entre 0 et 7, conformément au RFC 5424 syslog. Les commandes socket valides et réussies demandant des données (par exemple, « show map », « get acl foo » etc.) ne comporteront jamais de niveau de sévérité en préfixe. Il est ignoré par les autres sockets. `<format>` peut être l’un des éléments suivants :

-  « none » (par défaut) aucun niveau de sévérité n'est ajouté aux messages de retour.
-  « number » le niveau de sévérité est ajouté sous forme de nombre.
-  « string » le niveau de sévérité est ajouté sous forme de chaîne, conformément à la convention rfc5424.

<a id="entry-5-1-shards"></a>

**`shards { <number> | by-thread | by-group }`**

```haproxy
shards { <number> | by-thread | by-group }
```

En mode multithreadé, sur les systèmes d'exploitation prenant en charge plusieurs écouteurs sur la même adresse IP:port, cela crée automatiquement ce nombre d'écouteurs identiques pour la même ligne, chacun lié à une part équitable du nombre de threads attachés à cet écouteur. Cela peut parfois être utile lors de l'utilisation de très grands nombres de threads, où le verrouillage en noyau sur une seule socket commence à entraîner une surcharge significative. Dans ce cas, le trafic entrant est réparti sur plusieurs sockets, réduisant ainsi la contention. Notez que cette opération peut facilement augmenter la consommation CPU en faisant travailler davantage de threads, même légèrement.

Si le nombre de shards est supérieur au nombre de threads disponibles, il sera automatiquement réduit au nombre de threads (c’est-à-dire un shard par thread). La valeur spéciale « by-thread » crée également autant de shards qu’il y a de threads dans la ligne « bind ». Étant donné que le système répartit uniformément le trafic entrant entre tous ces shards, il est important que ce nombre soit un diviseur entier du nombre de threads. En alternance, la valeur spéciale « by-group » crée un shard par groupe de threads. Cette option peut être utile lorsqu’il y a beaucoup de threads sans souhaiter créer trop de sockets. La répartition de la charge sera un peu moins optimale, mais la contention (notamment au niveau du système) restera inférieure à celle observée avec un seul socket.

Sur les systèmes d'exploitation qui ne prennent pas en charge plusieurs sockets liés à la même adresse, les modes « by-thread » et « by-group » basculent automatiquement vers un seul shard. Pour le mode « by-group », ce basculement s'effectue sans avertissement, car cela n'a aucune incidence sur un seul groupe, et les sockets seront dupliquées de toute façon pour chaque groupe. En revanche, pour le mode « by-thread », un avertissement diagnostique est émis si ce basculement se produit, car le nombre de listeners résultant ne correspondra pas à l'attente.

<a id="entry-5-1-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de signature négociés pendant l'échange TLSv1.2 et TLSv1.3. Le format de la chaîne est défini dans « man 3 SSL_CTX_set1_sigalgs » des pages de documentation OpenSSL. Il est déconseillé d'utiliser ce paramètre sauf si une compatibilité avec un middlebox est requise.

<a id="entry-5-1-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Il active le déchiffrement SSL sur les connexions instanciées à partir de cet écouteur. Un certificat est nécessaire (voir « crt » ci-dessus). Tous les contenus présents dans les tampons apparaîtront en clair, de sorte que les ACLs et le traitement HTTP n'auront accès qu'aux données déchiffrées. SSLv3 est désactivé par défaut ; utilisez « ssl-min-ver SSLv3 » pour l'activer.

<a id="entry-5-1-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Cette option impose l'utilisation de `<version>` ou d'une version inférieure sur les connexions SSL instanciées à partir de cet écouteur.
Utiliser ce paramètre sans « ssl-min-ver » peut prêter à ambiguïté, car la valeur par défaut de « ssl-min-ver » pourrait évoluer dans les versions futures de HAProxy. Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-min-ver ».

<a id="entry-5-1-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Cette option impose l'utilisation de `<version>` ou d'une version supérieure sur les connexions SSL instanciées à partir de cet écouteur.
La valeur par défaut est "TLSv1.2". Cette option est également disponible dans l'instruction globale « ssl-default-bind-options ». Voir également « ssl-max-ver ».

<a id="entry-5-1-strict-sni"></a>

**`strict-sni`**

```haproxy
strict-sni
```

Ce paramètre n’est disponible que si le support d’OpenSSL a été intégré. La négociation SSL/TLS est autorisée uniquement si le client fournit un SNI correspondant à un certificat. Le certificat par défaut n’est pas utilisé. Cette option permet également de démarrer sans aucun certificat sur une ligne bind, de sorte qu’un répertoire vide puisse être utilisé et rempli ultérieurement via la socket de statistiques. Cette option est également disponible dans l’instruction globale « ssl-default-bind-options », et peut être désactivée sélectivement sur une ligne bind en utilisant « no-strict-sni ». Voir l’option « crt » pour plus d’informations. Voir la commande « add ssl crt-list » dans le guide d’administration.

<a id="entry-5-1-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Active la signature TCP MD5 (RFC 2385, protection des sessions BGP via l'option de signature TCP MD5) pour toutes les connexions entrantes instanciées à partir de ce socket d'écoute. Cette option n'est disponible que sous Linux. Lorsqu'elle est activée, la chaîne `<password>` est utilisée pour signer chaque segment TCP à l'aide d'un hachage de 16 octets MD5. Cela protège la connexion TCP contre les attaques par falsification. Le cas d'utilisation principal de cette option est de permettre à BGP de se protéger contre l'introduction de segments TCP falsifiés dans le flux de connexion. Elle peut toutefois être utile pour toute connexion TCP très longue.

<a id="entry-5-1-tcp-ss"></a>

**`tcp-ss <mode>`**

```haproxy
tcp-ss <mode>
```

Active l'option TCP Save SYN pour toutes les connexions entrantes instanciées à partir de cette socket d'écoute.
Cette option est disponible sur Linux depuis la version 4.3. Elle demande au noyau de conserver une copie du paquet IP entrant contenant le drapeau TCP SYN, pour une inspection ultérieure via la fonction d'extraction d'échantillon "fc_saved_syn". L'option dispose de 3 modes : - 0 l'extraction du paquet SYN est désactivée, c'est le comportement par défaut - 1 l'extraction du paquet SYN est activée, et inclut les en-têtes IP et TCP - 2 l'extraction du paquet SYN est activée, et inclut les en-têtes ETH, IP et TCP

Cela ne fonctionne que pour les connexions TCP régulières, et est ignoré pour les autres protocoles (par exemple, les sockets UNIX).
Voir également "fc_saved_syn".

<a id="entry-5-1-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Définit le délai d'expiration utilisateur TCP pour toutes les connexions entrantes instanciées à partir de ce socket d'écoute. Cette option est disponible sur Linux depuis la version 2.6.37. Elle permet à HAProxy de configurer un délai d'expiration pour les sockets contenant des données n'ayant pas reçu d'accusé de réception après le délai configuré. Cela est particulièrement utile pour les connexions longues souffrant de longues périodes d'inactivité, telles que les terminaux distants ou les pools de connexions bases de données, où les délais d'expiration du client et du serveur doivent rester élevés afin de permettre une longue période d'inactivité, mais où il est important de détecter que le client a disparu afin de libérer toutes les ressources associées à sa connexion (et à la session du serveur). L'argument est un délai exprimé en millisecondes par défaut. Cette fonctionnalité ne s'applique qu'aux connexions TCP régulières et est ignorée pour les autres protocoles.

<a id="entry-5-1-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Est un mot-clé facultatif pris en charge uniquement sur les noyaux Linux \>= 3.7. Il active le Fast Open TCP sur le socket d'écoute, ce qui signifie que les clients prenant en charge cette fonctionnalité pourront envoyer une requête et recevoir une réponse durant la négociation en trois étapes à partir de la deuxième connexion, économisant ainsi un aller-retour après la première connexion. Cela n'a de sens que pour les protocoles utilisant des taux de connexion élevés et où chaque aller-retour compte. Cette option peut entraîner des problèmes avec de nombreux pare-feu qui n'acceptent pas de données dans les paquets SYN, elle ne doit donc être activée qu'après tests approfondis. Cette option n'est prise en charge que sur les sockets TCPv4/TCPv6 et ignorée par les autres. Vous devrez peut-être compiler HAProxy avec USE_TFO=1 si votre libc ne définit pas TCP_FASTOPEN.

<a id="entry-5-1-thread"></a>

**`thread [<thread-group>/]<thread-set>[,...]`**

```haproxy
thread [<thread-group>/]<thread-set>[,...]
```

Cela restreint la liste des threads sur lesquels cet écouteur est autorisé à s'exécuter. Il n'impose aucun de ces threads, mais élimine ceux qui ne correspondent pas. Il limite les threads autorisés à traiter les connexions entrantes pour cet écouteur.

Il existe deux schémas de numérotation. Par défaut, les numéros de thread sont absolus dans le processus, compris entre 1 et la valeur spécifiée dans global.nbthread. Il est également possible de désigner un numéro de thread en utilisant son numéro relatif au sein de son groupe de threads, en spécifiant d'abord le numéro du groupe de threads, puis un slash ('/') et le numéro de thread relatif. Dans ce cas, les numéros de thread commencent également à 1 et s'arrêtent à 32 ou 64, selon la plateforme. Lorsque des numéros de thread absolus sont spécifiés, ils sont automatiquement traduits en numéros relatifs une fois les groupes de threads connus. En général, les numéros absolus sont préférés pour les configurations simples, tandis que les numéros relatifs sont préférés pour les configurations complexes où l'organisation des processeurs a une importance pour les performances.

Après le numéro de groupe de threads facultatif, la spécification « thread-set » doit utiliser le format suivant :

```text
"all" | "odd" | "even" | [number][-[number]]
```

Comme leurs noms l'indiquent, « all » valide tous les threads du jeu (tous ceux du groupe, s'il est spécifié, ou tous ceux du processus), « odd » valide tous les threads dont le numéro est impair (chaque deuxième thread à partir du numéro 1), que ce soit pour le processus ou le groupe, et « even » valide tous les threads dont le numéro est pair (chaque deuxième thread à partir du numéro 2). Si au contraire des plages de numéros de thread sont utilisées, alors tous les threads compris entre le premier et le dernier numéro de thread sont validés. Les numéros sont soit relatifs au groupe, soit absolus, selon la présence ou non d'un numéro de groupe. Si le premier numéro de thread est omis, la valeur « 1 » est utilisée, représentant soit le premier thread du groupe, soit le premier thread du processus. Si le dernier numéro de thread est omis, on utilise soit le dernier numéro de thread du groupe (32 ou 64), soit le dernier numéro de thread du processus (global.nbthread).

Ces plages peuvent être répétées et séparées par une virgule, afin de spécifier des ensembles de threads non contigus, et le groupe, s'il est présent, doit être indiqué à nouveau pour chaque nouvelle plage. Notez qu'il n'est pas autorisé de mélanger des spécifications relatives au groupe et des spécifications absolues, car toute la ligne « bind » doit utiliser soit une notation absolue, soit une notation relative, les éléments non définis étant résolus à la fin de l'analyse.

Il est important de savoir qu’un écouteur décrit par une ligne « bind » crée au moins une socket représentée par au moins un descripteur de fichier. Comme les descripteurs de fichier ne peuvent pas s’étendre sur plusieurs groupes de threads, si une ligne « bind » spécifie une plage de threads couvrant plus d’un groupe, plusieurs descripteurs de fichier seront automatiquement créés afin d’en avoir au moins un par groupe. Techniquement, ils font tous référence à la même socket dans le noyau, mais ils obtiendront un identifiant distinct dans HAProxy et même une entrée dédiée dans les statistiques si l’option « option socket-stats » est utilisée.

Le but principal est de permettre à plusieurs lignes bind de partager la même adresse IP:port, mais pas le même thread dans un écouteur, afin que le système puisse répartir les connexions entrantes sur plusieurs files d’attente, contournant ainsi la répartition de charge interne de HAProxy. Ce fonctionnement est actuellement connu pour être pris en charge par Linux 3.9 et versions ultérieures. Voir également le mot-clé « shards » ci-dessus, qui automatise la duplication des lignes bind et leur affectation à plusieurs groupes de threads.

Ce mot-clé est compatible avec les liaisons HTTP inversées. Toutefois, il est interdit de spécifier un jeu de threads qui s'étend sur plusieurs groupes de threads pour un tel écouteur, car cela pourrait empêcher nbconn de fonctionner comme prévu.

<a id="entry-5-1-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il active la reprise de session sans état (extension TLS Ticket RFC 5077). Il est défini par défaut, mais peut être nécessaire pour réactiver sélectivement cette fonctionnalité sur une ligne « bind » si elle a été désactivée globalement via « no-tls-tickets », comme indiqué dans « ssl-default-bind-options ». Voir également le mot-clé « no-tls-tickets » pour « bind ».

<a id="entry-5-1-tls-ticket-keys"></a>

**`tls-ticket-keys <keyfile>`**

```haproxy
tls-ticket-keys <keyfile>
```

Définit le fichier contenant les clés de ticket TLS à charger. Les clés doivent avoir une longueur de 48 ou 80 octets, selon que aes128 ou aes256 est utilisé, encodées en base64 avec une clé par ligne (par exemple : openssl rand 80 \| openssl base64 -A \| xargs echo). La première clé détermine la longueur des clés suivantes : il n'est pas possible de mélanger des clés aes128 et aes256. Le nombre de clés est spécifié par l'option de compilation TLS_TICKETS_NO (valeur par défaut : 3) et au moins autant de clés doivent être présentes dans le fichier. Les TLS_TICKETS_NO dernières clés seront utilisées pour le déchiffrement et l'avant-dernière pour le chiffrement. Cela permet une rotation facile des clés en ajoutant simplement une nouvelle clé au fichier et en rechargant le processus. Les clés doivent être régulièrement renouvelées (par exemple toutes les 12 h), faute de quoi la confidentialité persistante parfaite (Perfect Forward Secrecy) sera compromise. Il est également recommandé de ne pas stocker les clés sur un support permanent tel qu'un disque dur (indice : utiliser tmpfs et empêcher ces fichiers d'être écrits dans l'espace d'échange (swap)). L'indication de durée de validité du ticket peut être modifiée à l'aide de tune.ssl.timeout.

<a id="entry-5-1-transparent"></a>

**`transparent`**

```haproxy
transparent
```

Est un mot-clé facultatif pris en charge uniquement sur certains noyaux Linux. Il indique que les adresses seront liées même si elles n'appartiennent pas à la machine locale, et que les paquets ciblant l'une de ces adresses seront interceptés comme si elles étaient configurées localement. Cela nécessite généralement que le transfert IP soit activé. Attention ! N'utilisez pas ce mot-clé avec l'adresse par défaut '\*', car cela redirigerait tout le trafic destiné au port spécifié. Ce mot-clé n'est disponible que si HAProxy est compilé avec USE_LINUX_TPROXY=1. Ce paramètre n'est compatible qu'avec les sockets TCPv4 et TCPv6, selon la version du noyau. Certains noyaux de distribution incluent des correctifs de cette fonctionnalité, vérifiez donc la prise en charge auprès de votre fournisseur.

<a id="entry-5-1-uid"></a>

**`uid <uid>`**

```haproxy
uid <uid>
```

Définit le propriétaire des sockets UNIX selon l'identifiant système UID spécifié. Ce paramètre peut également être défini par défaut dans l'instruction « unix-bind » de la section globale. Notez que certaines plates-formes ignorent simplement ce paramètre. Ce paramètre est équivalent à l'option « user », à ceci près qu'il utilise l'identifiant numérique de l'utilisateur au lieu de son nom. Ce paramètre est ignoré pour les sockets non UNIX.

<a id="entry-5-1-user"></a>

**`user <user>`**

```haproxy
user <user>
```

Définit le propriétaire des sockets UNIX sur l'utilisateur système indiqué. Ce paramètre peut également être défini par défaut dans l'instruction « unix-bind » de la section globale. Notez que certaines plates-formes l'ignorent simplement. Ce paramètre est équivalent à l'option « uid », sauf qu'il utilise le nom d'utilisateur au lieu de son identifiant uid. Ce paramètre est ignoré pour les sockets non UNIX.

<a id="entry-5-1-v4v6"></a>

**`v4v6`**

```haproxy
v4v6
```

Est un mot-clé facultatif pris en charge uniquement sur les systèmes les plus récents, y compris les noyaux Linux ≥ 2.4.21. Il permet de lier une socket à la fois à IPv4 et à IPv6 lorsqu'elle utilise l'adresse par défaut. Cette option est parfois nécessaire sur les systèmes qui, par défaut, ne lient qu'à IPv6. Elle n'a aucun effet sur les sockets non IPv6 et est annulée par l'option « v6only ».

<a id="entry-5-1-v6only"></a>

**`v6only`**

```haproxy
v6only
```

Est un mot-clé facultatif pris en charge uniquement sur les systèmes les plus récents, y compris les noyaux Linux ≥ 2.4.21. Il est utilisé pour lier une socket à IPv6 uniquement lorsqu'elle utilise l'adresse par défaut. Cette approche est parfois préférée à une configuration système entière, car elle est spécifique à chaque écouteur. Il n'a aucun effet sur les sockets non IPv6 et a une priorité sur l'option « v4v6 ».

<a id="entry-5-1-verify"></a>

**`verify [none|optional|required]`**

```haproxy
verify [none|optional|required]
```

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Si sa valeur est définie sur « none », aucun certificat client n'est demandé. C'est la valeur par défaut. Dans les autres cas, un certificat client est demandé. Si le client ne fournit pas de certificat après la demande et que « verify » est défini sur « required », la négociation est interrompue, alors qu'elle aurait abouti si la valeur était « optional ». Le certificat fourni par le client est toujours vérifié à l'aide des autorités de certification (CA) du fichier « ca-file » et des listes de révocation de certificats (CRL) facultatives du fichier « crl-file ». En cas d'échec de vérification, la négociation est interrompue, indépendamment de la valeur de l'option « verify », sauf si le code d'erreur correspond exactement à l'un des codes listés dans « ca-ignore-err » ou « crt-ignore-err ».

## 5.2. Options serveur et options par défaut pour serveur {#section-5-2}

Les mots-clés « server » et « default-server » prennent en charge un certain nombre de paramètres, tous transmis sous forme d'arguments sur la ligne du serveur. L'ordre d'apparition de ces arguments n'a pas d'importance, et tous sont facultatifs. Certains de ces paramètres sont des mots simples (valeurs booléennes), tandis que d'autres attendent une ou plusieurs valeurs après eux. Dans ce cas, les valeurs doivent immédiatement suivre le nom du paramètre. À l'exception de « default-server », tous ces paramètres doivent être spécifiés après l'adresse du serveur s'ils sont utilisés :

```text
server <name> <address>[:port] [settings ...]
default-server [settings ...]
```

Remarque : toutes ces options sont prises en charge par les mots-clés « server » et « default-server », sauf l’« id », qui n’est pris en charge que par « server ».

Les paramètres actuellement pris en charge sont les suivants.

<a id="entry-5-2-addr"></a>

**`addr <ipv4|ipv6>`**

```haproxy
addr <ipv4|ipv6>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

En utilisant le paramètre « addr », il devient possible d'utiliser une adresse IP différente pour envoyer les contrôles d'état ou pour sonder l'agent-check. Sur certains serveurs, il peut être souhaitable de réserver une adresse IP à un composant spécifique capable d'effectuer des tests complexes, plus adaptés aux contrôles d'état que l'application elle-même. Ce paramètre est ignoré si le paramètre « check » n'est pas défini. Voir également le paramètre « port ».

<a id="entry-5-2-agent-check"></a>

**`agent-check`**

```haproxy
agent-check
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Active un contrôle d'état d'agent auxiliaire exécuté indépendamment d'un contrôle d'état régulier. Un contrôle d'état d'agent est effectué en établissant une connexion TCP sur le port défini par le paramètre « agent-port » et en lisant une chaîne ASCII terminée par le premier '&#92;r' ou '&#92;n' rencontré. La chaîne est composée d'une série de mots séparés par des espaces, des tabulations ou des virgules, dans n'importe quel ordre, chacun composé de :

- Représentation ASCII d'un pourcentage entier positif, par exemple « 75% ». Les valeurs dans ce format définissent le poids proportionnellement au poids initial d'un serveur, tel qu'il est configuré au démarrage de HAProxy. Notez qu'un poids nul est affiché sur la page de statistiques sous la forme « DRAIN », car cela a le même effet sur le serveur (il est retiré de la ferme de répartition de charge). Il s'agit de la méthode héritée pour définir le poids d'un serveur. Il est préférable de le définir en utilisant le préfixe « weight: ».

- La chaîne « weight: » suivie d'un entier positif ou d'un pourcentage entier positif, sans espace. Si la valeur se termine par le signe « % », le nouveau poids sera proportionnel au poids initial du serveur. Sinon, la valeur est considérée comme un poids absolu et doit être comprise entre 0 et 256. Les serveurs faisant partie d'une ferme utilisant un algorithme de répartition de charge statique ont des limitations plus strictes, car le poids ne peut pas être modifié une fois défini. Pour ces serveurs, les seules valeurs acceptées sont 0 et 100 % (ou 0 et le poids initial). Les modifications prennent effet immédiatement, bien que certains algorithmes de répartition de charge nécessitent un certain nombre de requêtes pour prendre en compte les changements. Notez qu'un poids nul est indiqué sur la page de statistiques comme « DRAIN », car il a le même effet sur le serveur (il est retiré de la ferme de répartition de charge).

- La chaîne « maxconn: » suivie d'un entier (aucun espace entre). Les valeurs de ce format définissent la valeur maxconn d'un serveur. Le nombre maximal de connexions annoncé doit être multiplié par le nombre de répartiteurs de charge et de backends différents utilisant ce contrôle d'état afin d'obtenir le nombre total de connexions que le serveur pourrait recevoir. Exemple : maxconn:30

- Le mot « ready ». Cela met l'état administratif du serveur en mode READY, annulant ainsi tout état DRAIN ou MAINT

- Le mot « drain ». Cela mettra l'état administratif du serveur en mode DRAIN, de sorte qu'il n'acceptera aucune nouvelle connexion, à l'exception de celles qui sont acceptées via la persistance.

- Le mot « maint ». Cela placera l'état administratif du serveur en mode MAINT, ce qui empêchera toute nouvelle connexion et arrêtera les contrôles d'état.

- Les mots « down », « fail » ou « stopped », suivis éventuellement d'une chaîne de description après un trait dièse ('#'). Tous ces mots marquent l'état d'exploitation du serveur comme DOWN, mais comme le mot lui-même est rapporté sur la page de statistiques, la différence permet à un administrateur de savoir si la situation était prévue ou non : le service peut être arrêté intentionnellement, peut apparaître comme actif mais échouer à certaines vérifications de validité, ou peut être perçu comme hors service (par exemple, processus manquant ou port non réactif).

- Le mot « up » rétablit l'état opérationnel du serveur à UP si les contrôles d'état indiquent également que le service est accessible.

Les paramètres non annoncés par l'agent ne sont pas modifiés. Par exemple, un agent peut être conçu pour surveiller l'utilisation du CPU et ne rapporter qu'un poids relatif, sans jamais interagir avec l'état d'exploitation. De même, un agent pourrait être conçu comme une interface utilisateur finale avec trois boutons radio permettant à un administrateur de modifier uniquement l'état administratif. Toutefois, il est important de noter que seul l'agent peut annuler ses propres actions ; ainsi, si un serveur est mis en mode DRAIN ou en état DOWN à l'aide de l'agent, l'agent doit implémenter les actions équivalentes correspondantes pour ramener le service en exploitation.

La défaillance de connexion à l'agent n'est pas considérée comme une erreur, car la connectivité est vérifiée par le contrôle d'état régulier, activé par le paramètre « check ». Attention toutefois : il n'est pas recommandé d'arrêter un agent après qu'il a signalé « down », car seul un agent signalant « up » pourra réactiver le serveur. Notez que l'interface CLI sur le socket Unix de statistiques est également capable de forcer le résultat d'un agent afin de contourner un agent défaillant si nécessaire.

Exige que le paramètre « agent-port » soit défini. Voir également les paramètres « agent-inter » et « no-agent-check ».

<a id="entry-5-2-agent-send"></a>

**`agent-send <string>`**

```haproxy
agent-send <string>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Si cette option est spécifiée, HAProxy enverra la chaîne donnée (telle quelle) au serveur agent lors de la connexion. Vous pourriez, par exemple, encoder le nom du backend dans cette chaîne, ce qui permettrait à votre agent de renvoyer des réponses différentes selon le backend. Veillez à inclure un '&#92;n' si vous souhaitez terminer votre requête par une nouvelle ligne.

<a id="entry-5-2-agent-inter"></a>

**`agent-inter <delay>`**

```haproxy
agent-inter <delay>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « agent-inter » définit l'intervalle entre deux contrôles d'agent en `<delay>` millisecondes. Si non spécifié, le délai par défaut est de 2000 ms.

Tout comme pour tout autre paramètre basé sur le temps, il peut être spécifié dans n'importe quelle unité explicite parmi {us, ms, s, m, h, d}. Le paramètre « agent-inter » sert également de délai d'expiration pour les contrôles d'agent lorsque « timeout check » n'est pas défini. Afin de réduire les effets de « résonance » lorsque plusieurs serveurs sont hébergés sur le même matériel, les agents et les contrôles d'état de tous les serveurs sont lancés avec un léger décalage temporel entre eux. Il est également possible d'ajouter un bruit aléatoire à l'intervalle des agents et des contrôles d'état en utilisant le mot-clé global « spread-checks ». Cela a un sens, par exemple, lorsque de nombreux backends utilisent les mêmes serveurs.

Voir également les paramètres « agent-check » et « agent-port ».

<a id="entry-5-2-agent-addr"></a>

**`agent-addr <addr>`**

```haproxy
agent-addr <addr>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « agent-addr » définit l'adresse de vérification de l'agent.

Vous pouvez déléguer le contrôle d'état de l'agent à une cible différente, afin de centraliser la gestion de l'état et des poids des serveurs définis dans HAProxy, en cas d'impossibilité de mettre en œuvre des services auto-conscients et auto-gérés. Vous pouvez spécifier une adresse IP ou un nom d'hôte ; celle-ci sera résolue.

<a id="entry-5-2-agent-port"></a>

**`agent-port <port>`**

```haproxy
agent-port <port>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « agent-port » définit le port TCP utilisé pour les contrôles d'agent.

Voir également les paramètres « agent-check » et « agent-inter ».

<a id="entry-5-2-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Autorise l’envoi de données anticipées au serveur lors de l’utilisation de TLS 1.3. Notez que les données anticipées ne seront envoyées que si le client les a utilisées, ou si le backend utilise « retry-on » avec le mot-clé « 0rtt-rejected ». Avec QUIC, le 0rtt est pris en charge avec QuicTLS, OpenSSL \>= 3.5.2 et AWS-LC. Avec TCP/TLS, le 0rtt n’est pris en charge qu’avec OpenSSL.

<a id="entry-5-2-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Peut être utilisé dans les contextes suivants : tcp, http

Cela active l'extension TLS ALPN et annonce la liste de protocoles spécifiée comme prise en charge au-dessus d'ALPN. La liste de protocoles est constituée d'une liste séparée par des virgules de noms de protocoles, par exemple : « http/1.1,http/1.0 » (sans guillemets). Cela nécessite que la bibliothèque SSL soit compilée avec le support des extensions TLS activé (vérifiez avec haproxy -vv). L'extension ALPN remplace l'extension NPN initiale. ALPN est obligatoire pour se connecter à des serveurs HTTP/2. Il est également obligatoire pour pouvoir utiliser HTTP/3 via un serveur QUIC ; « h3 » sert de valeur par défaut pour les serveurs QUIC sans paramètre « alpn ». Les versions d'OpenSSL antérieures à 1.0.2 ne prennent pas en charge ALPN et ne supportaient que l'extension NPN désormais obsolète. Si HTTP/2 et HTTP/1.1 sont attendus comme étant pris en charge, les deux versions peuvent être annoncées, dans l'ordre de préférence, comme ci-dessous :

```text
server 127.0.0.1:443 ssl crt pub.pem alpn h2,http/1.1
```

Voir également « ws » pour utiliser un ALPN alternatif pour les flux WebSocket.

<a id="entry-5-2-backup"></a>

**`backup`**

```haproxy
backup
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Lorsque « backup » est présent sur une ligne de serveur, ce dernier n'est utilisé en répartition de charge que lorsque tous les autres serveurs non réservés sont indisponibles. Les requêtes portant un cookie de persistance faisant référence à ce serveur sont toutefois toujours servies. Par défaut, seul le premier serveur de secours opérationnel est utilisé, sauf si l'option « allbackups » est définie dans le backend. Voir également les options « no-backup » et « allbackups ».

<a id="entry-5-2-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support OpenSSL a été inclus. Il indique un fichier PEM à partir duquel charger les certificats CA utilisés pour vérifier le certificat du serveur. Il est possible de charger un répertoire contenant plusieurs CA ; dans ce cas, HAProxy tentera de charger chaque ".pem", ".crt", ".cer", ainsi que tous les fichiers .crl présents dans le répertoire. Les fichiers commençant par un point sont ignorés.

Afin d'utiliser les autorités de certification fiables de votre système, le paramètre "@system-ca" peut être utilisé à la place de cafile. Le chemin de ce répertoire peut être remplacé en définissant la variable d'environnement SSL_CERT_DIR.

<a id="entry-5-2-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que sur les systèmes définissant TCP_CONGESTION, et a été validé sur Linux et FreeBSD. Il prend le nom d’un algorithme de contrôle de congestion TCP et configure les connexions sortantes pour utiliser cet algorithme. Les noms courants incluent « reno » ou « cubic », qui dépendent du système d'exploitation. Sur certains systèmes, des permissions spéciales peuvent être nécessaires pour configurer certains algorithmes. Sur Linux, les algorithmes disponibles sont listés dans sysctl "net.ipv4.tcp_available_congestion_control", et ceux autorisés sans privilèges se trouvent dans "net.ipv4.tcp_allowed_congestion_control". Pour accéder aux algorithmes nécessitant des permissions supplémentaires, la capacité "cap_net_admin" peut être requise (voir « setcap » dans la section globale). En cas d’échec de configuration d’un algorithme de congestion spécifique, celui par défaut reste inchangé. Voir également : le mot-clé bind « cc » ([section 5.1](/fr/haproxy/bind-and-server-options/#section-5-1)).

<a id="entry-5-2-check"></a>

**`check`**

```haproxy
check
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option active les contrôles d'état sur un serveur :   - lorsqu'elle n'est pas définie, aucun contrôle d'état n'est effectué, et le serveur est toujours considéré comme disponible.   - lorsqu'elle est définie et qu'aucune autre méthode de contrôle n'est configurée, le serveur est considéré comme disponible lorsque la connexion peut être établie au niveau du transport le plus élevé configuré. Cela signifie TCP par défaut, ou SSL/TLS lorsque « ssl » ou « check-ssl » sont définis, pouvant éventuellement être combiné avec des préfixes de connexion tels qu'un en-tête de protocole PROXY lorsque « send-proxy » ou « check-send-proxy » sont définis. Ce comportement diffère légèrement pour les serveurs dynamiques ; consultez les paragraphes suivants pour plus de détails.   - lorsqu'elle est définie et qu'un contrôle d'état au niveau applicatif est défini, les échanges au niveau applicatif sont effectués au-dessus du niveau de transport configuré, et le serveur est considéré comme disponible si tous les échanges réussissent.

Par défaut, les contrôles d'état sont effectués sur la même adresse et le même port que ceux configurés sur le serveur, en utilisant les mêmes paramètres d'encapsulation (SSL/TLS, en-tête proxy-protocol, etc.). Il est possible de modifier l'adresse de destination à l'aide de « addr » et le port à l'aide de « port ». Lorsque cela est fait, il est supposé que le serveur n'est pas contrôlé sur le port de service, et les paramètres d'encapsulation configurés ne sont pas réutilisés. Il faut définir explicitement « check-send-proxy » pour envoyer les en-têtes de connexion, et « check-ssl » pour utiliser SSL/TLS.

Notez que la configuration implicite du protocole SSL et du protocole PROXY n’est pas appliquée aux serveurs dynamiques.
Dans ce cas, il est nécessaire d’utiliser explicitement les options « check-ssl » et « check-send-proxy » lorsqu’elles sont requises, même si le port de vérification n’est pas redéfini.

Lorsque « sni » ou « alpn » sont définis sur la ligne server, leur valeur n'est pas utilisée pour les contrôles d'état et il faut alors utiliser « check-sni » ou « check-alpn ».

L'adresse source par défaut pour le trafic de contrôle d'état est la même que celle définie dans le backend.
Elle peut être modifiée à l'aide du mot-clé « source ».

L'intervalle entre les contrôles d'état peut être défini à l'aide du mot-clé « inter », et les mots-clés « rise » et « fall » peuvent être utilisés pour préciser le nombre de contrôles d'état réussis ou échoués requis pour marquer un serveur comme disponible ou indisponible.

Des contrôles d'état au niveau applicatif optionnels peuvent être configurés à l’aide de « option httpchk », « option mysql-check », « option smtpchk », « option pgsql-check », « option ldap-check » ou « option redis-check ».

Exemple :

```shell
# simple tcp check
backend foo
  server s1 192.168.0.1:80 check
# this does a tcp connect + tls handshake
backend foo
  server s1 192.168.0.1:443 ssl check
# simple tcp check is enough for check success
backend foo
  option tcp-check
  tcp-check connect
  server s1 192.168.0.1:443 ssl check
```

<a id="entry-5-2-check-reuse-pool"></a>

**`check-reuse-pool`**

```haproxy
check-reuse-pool
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option permet aux contrôles de réutiliser les connexions inactives disponibles au lieu d'en ouvrir une dédiée. La connexion est réinsérée dans le pool une fois le contrôle terminé. L'objectif principal est de limiter le nombre d'ouvertures et de fermetures de connexions sur un serveur spécifique. Cette fonctionnalité n'est compatible qu'avec les ensembles de règles http-check. Elle est ignorée silencieusement pour les autres types de contrôle. En outre, la politique de réutilisation devrait être définie sur « aggressive » sur le backend, car chaque tentative de contrôle est effectuée sur une session dédiée.

Pour simplifier la configuration, cette option est ignorée silencieusement si une option de connexion spécifique de contrôle est définie, qu'elle soit définie sur la ligne du serveur ou via une règle personnalisée tcp-check connect.

Cette option est automatiquement activée pour les serveurs agissant en tant que passerelle HTTP inverse passive, car, pour ces serveurs, la connexion n'est prise en charge que par la réutilisation.

Voir également : « check-pool-conn-name »

<a id="entry-5-2-check-send-proxy"></a>

**`check-send-proxy`**

```haproxy
check-send-proxy
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option force l'émission d'une ligne PROXY protocol dans les contrôles d'état sortants, quelle que soit l'utilisation ou non de send-proxy par le serveur pour le trafic normal. Par défaut, le protocole PROXY est activé pour les contrôles d'état si celui-ci est déjà activé pour le trafic normal et si aucune directive « port » ni « addr » n'est présente. Toutefois, si une telle directive est présente, l'option « check-send-proxy » doit être utilisée pour forcer l'utilisation du protocole. Voir également l'option « send-proxy » pour plus d'informations.

<a id="entry-5-2-check-alpn"></a>

**`check-alpn <protocols>`**

```haproxy
check-alpn <protocols>
```

Peut être utilisé dans les contextes suivants : tcp, http

Définit les protocoles à annoncer via ALPN. La liste des protocoles est une liste séparée par des virgules de noms de protocoles, par exemple : « http/1.1,http/1.0 » (sans guillemets). Si ce paramètre n’est pas défini, le serveur ALPN est utilisé.

<a id="entry-5-2-check-pool-conn-name"></a>

**`check-pool-conn-name <name>`**

```haproxy
check-pool-conn-name <name>
```

Peut être utilisé dans les contextes suivants : tcp, http

Lorsque la réutilisation de connexion est effectuée pour les contrôles, utilise `<name>` s'il est défini comme identifiant de connexion afin de correspondre à une connexion correspondante dans le pool. Cela équivaut au mot-clé serveur « pool-conn-name ». « check-sni » sera également utilisé comme option de secours si l'option actuelle n'est pas utilisée.

Voir aussi : « check-reuse-pool »

<a id="entry-5-2-check-proto"></a>

**`check-proto <name>`**

```haproxy
check-proto <name>
```

Peut être utilisé dans les contextes suivants : tcp, http

Force le protocole du multiplexeur à utiliser pour les connexions de contrôle d'état du serveur. Il doit être compatible avec le type de contrôle d'état (TCP ou HTTP). Il doit également être utilisable du côté du backend. La liste des protocoles disponibles est indiquée par haproxy -vv. Les propriétés des protocoles sont les suivantes : le mode (TCP/HTTP), le côté (FE/BE), le nom du multiplexeur et ses indicateurs.

Certains protocoles sont sujets au blocage par tête de file côté serveur (drapeau=HOL_RISK). Enfin, certains protocoles ne prennent pas en charge les mises à jour (drapeau=NO_UPG). La compatibilité HTX est également indiquée (drapeau=HTX).

Voici les protocoles pouvant être utilisés en tant qu'argument de la directive « check-proto » sur une ligne de serveur :

```text
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

L'idée de cette option est de contourner le choix du protocole du multiplexeur optimal pour les connexions de contrôle d'état établies vers ce serveur. Si elle n'est pas définie, le protocole du serveur sera utilisé, le cas échéant.

Si les paramètres ALPN ou NPN sont configurés, les protocoles spécifiés doivent être compatibles avec le protocole du multiplexeur afin d'éviter tout problème. Par exemple, si « proto h1 » est défini, l'ALPN ne doit pas être configuré sur « h2 ».

La configuration des vérifications QUIC n’est pas entièrement implémentée pour l’instant. Premièrement, les vérifications QUIC ne peuvent être effectuées que pour les serveurs QUIC. Deuxièmement, si un ou plusieurs paramètres de connexion spécifiques sont définis sur un serveur QUIC, le protocole de vérification passera à une utilisation TCP.

<a id="entry-5-2-check-sni-auto"></a>

**`check-sni-auto`**

```haproxy
check-sni-auto
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option active la sélection automatique du SNI lors des contrôles d'état SSL, si aucune valeur n’a déjà été définie. Elle est activée par défaut, mais ce paramètre peut être utilisé en tant que paramètre « server » pour réinitialiser toute configuration « no-check-sni-auto » héritée de la directive « default-server » en tant que valeur par défaut. Il peut également être utilisé en tant que paramètre « default-server » pour réinitialiser toute configuration précédente « no-check-sni-auto » définie sur « default-server ».

Pour les connexions HTTPS, le SNI est automatiquement sélectionné, mais uniquement s’il n’existe pas de règle « http-check connect ». Dans ce cas, le SNI sélectionné est déterminé par la valeur de l’en-tête host, spécifiée via la directive « option httpchk » ou une règle « http-check send ». Aucune sélection automatique n’est appliquée pour les règles « http-check connect ». Pour les autres protocoles, cette option est ignorée.

Si la sélection automatique du SNI est utilisée pour les contrôles d'état, la valeur est affectée au nom de la connexion si l'option « check-reuse-pool » est activée, sauf si elle est remplacée par le mot-clé serveur « check-pool-conn-name ».

Voir l'option « sni-auto » pour activer la sélection automatique du SNI pour le trafic proxyé.

<a id="entry-5-2-check-sni"></a>

**`check-sni <sni>`**

```haproxy
check-sni <sni>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option permet de spécifier le SNI à utiliser lors des contrôles d'état sur SSL. Il est uniquement possible d'utiliser une chaîne pour définir `<sni>`. Si vous souhaitez définir un SNI pour le trafic proxy, consultez « sni ».

<a id="entry-5-2-check-ssl"></a>

**`check-ssl`**

```haproxy
check-ssl
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option force le chiffrement de tous les contrôles d'état via SSL, indépendamment du fait que le serveur utilise ou non SSL pour le trafic normal. Elle est généralement utilisée lorsque la directive « port » ou « addr » est explicitement définie et que les contrôles d'état SSL ne sont pas hérités. Il est important de comprendre que cette option insère une couche de transport SSL sous les contrôles, de sorte qu’un contrôle de connexion TCP simple devient une connexion SSL, remplaçant ainsi l’ancienne directive « ssl-hello-chk ». L’usage le plus courant consiste à envoyer des contrôles HTTPS en combinant « httpchk » avec des contrôles SSL. Tous les paramètres SSL sont communs aux contrôles d'état et au trafic (par exemple, les suites de chiffrement). Pour plus d'informations, consultez l’option « ssl » et « no-check-ssl » pour désactiver cette option.

<a id="entry-5-2-check-via-socks4"></a>

**`check-via-socks4`**

```haproxy
check-via-socks4
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option active les contrôles d'état sortants via un proxy socks4 en amont. Par défaut, les contrôles d'état ne passent pas par le tunnel socks, même s'il est activé pour le trafic normal.

<a id="entry-5-2-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Cette option définit la chaîne décrivant la liste des algorithmes de chiffrement négociés lors de l'établissement de la connexion SSL/TLS avec le serveur. Le format de la chaîne est défini dans « man 1 ciphers » des pages de documentation OpenSSL. Pour des informations complémentaires et des recommandations, consulter par exemple (<https://wiki.mozilla.org/Security/Server_Side_TLS>) et (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Pour la configuration des cipher suites TLSv1.3, se référer à la directive « ciphersuites ».

<a id="entry-5-2-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré au moment de la compilation et si OpenSSL 1.1.1 ou une version ultérieure a été utilisé pour compiler HAProxy. Cette option définit la chaîne décrivant la liste des algorithmes de chiffrement négociés lors de l'échange TLS 1.3 avec le serveur. Le format de la chaîne est défini dans « man 1 ciphers » des pages de documentation OpenSSL, dans la section « ciphersuites ». Pour la configuration des chiffres TLSv1.2 et versions antérieures, veuillez consulter le mot-clé « ciphers ».

<a id="entry-5-2-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de signature liés à l'authentification cliente qui sont négociés. Le format de la chaîne est défini dans « man 3 SSL_CTX_set1_client_sigalgs » des pages de documentation OpenSSL. Il est déconseillé d'utiliser ce paramètre si aucun cas d'utilisation spécifique n'a été identifié.

<a id="entry-5-2-cookie"></a>

**`cookie <value>`**

```haproxy
cookie <value>
```

Peut être utilisé dans les contextes suivants : http

Le paramètre « cookie » définit la valeur de cookie attribuée au serveur pour `<value>`. Cette valeur sera vérifiée dans les requêtes entrantes, et le premier serveur opérationnel possédant la même valeur sera sélectionné. En retour, en mode insertion ou réécriture de cookie, cette valeur sera attribuée au cookie envoyé au client. Il n’y a rien de répréhensible à ce que plusieurs serveurs partagent la même valeur de cookie, ce qui est d’ailleurs assez courant entre serveurs normaux et serveurs de secours. Voir également le mot-clé « cookie » dans la section backend.

<a id="entry-5-2-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il indique un fichier PEM à partir duquel charger la liste de révocation de certificats utilisée pour vérifier le certificat du serveur.

<a id="entry-5-2-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il indique un fichier PEM à partir duquel charger à la fois un certificat et sa clé privée associée. Ce fichier peut être créé en concaténant deux fichiers PEM. Ce certificat sera envoyé si le serveur demande un certificat client.

Si le fichier ne contient pas de clé privée, HAProxy tentera de charger la clé au même chemin, suffixé par un ".key" (à condition que l'option "ssl-load-extra-files" soit configurée en conséquence).

<a id="entry-5-2-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de courbes elliptiques ("suite de courbes") négociés lors de l'échange SSL/TLS avec ECDHE. Le format de la chaîne est une liste séparée par des deux-points de noms de courbes. Exemple : "X25519:P-256" (sans guillemets)

<a id="entry-5-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le mot-clé « disabled » place le serveur en état « disabled ». Cela signifie qu’il est marqué comme hors service en mode maintenance, et aucune connexion, hormis celles autorisées par le mode persist, ne pourra le rejoindre. Il convient particulièrement bien pour configurer de nouveaux serveurs, car le trafic normal n’y parviendra jamais, tout en permettant encore de tester le service grâce au mécanisme force-persist. Voir également le paramètre « enabled ».

<a id="entry-5-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « disabled » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « disabled » précédent défini sur « default-server ».

<a id="entry-5-2-error-limit"></a>

**`error-limit <count>`**

```haproxy
error-limit <count>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Si l'observation de la santé est activée, le paramètre « error-limit » spécifie le nombre d'erreurs consécutives qui déclenchent l'événement sélectionné par l'option « on-error ». Par défaut, il est défini à 10 erreurs consécutives.

Voir également les options « check », « error-limit » et « on-error ».

<a id="entry-5-2-fall"></a>

**`fall <count>`**

```haproxy
fall <count>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « fall » indique qu'un serveur est considéré comme défaillant après `<count>` contrôles d'état consécutifs échoués. Cette valeur vaut 3 par défaut si non spécifiée. Voir également les paramètres « check », « inter » et « rise ».

<a id="entry-5-2-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de SSLv3 uniquement lorsque le protocole SSL est utilisé pour communiquer avec le serveur. SSLv3 est généralement moins coûteux que ses homologues TLS pour des débits de connexion élevés. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-2-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de TLSv1.0 uniquement lorsque SSL est utilisé pour communiquer avec le serveur. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-2-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de TLSv1.1 uniquement lorsque SSL est utilisé pour communiquer avec le serveur. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-2-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de TLSv1.2 uniquement lorsque le protocole SSL est utilisé pour communiquer avec le serveur. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-2-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de TLSv1.3 uniquement lorsque SSL est utilisé pour communiquer avec le serveur. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver » et « ssl-max-ver ».

<a id="entry-5-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Spécifiez un identifiant global sensible à la casse pour ce serveur. Celui-ci doit être unique sur l'ensemble de la configuration haproxy, pour tous les types d'objets. Consultez la description du mot-clé proxy « guid » pour plus d'informations sur son format. Voir également « shm-stats-file ».

<a id="entry-5-2-hash-key"></a>

**`hash-key <key>`**

```haproxy
hash-key <key>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Spécifiez la manière dont les clés de nœud « hash-type consistent » sont calculées

Arguments :

```text
<key>   <key> peut prendre l'une des valeurs suivantes :

  id         Les clés des nœuds sont dérivées de l'identifiant numérique
             du serveur défini par "id", ou par défaut de sa position dans
             la liste des serveurs. C'est la valeur par défaut. Seuls les 20
             bits de poids faible de l'ID sont utilisés (soit
             (id % 1048576)) ; utilisez des valeurs entre 1 et cette
             valeur pour éviter les chevauchements.

  id32       Les clés des nœuds sont dérivées de l'identifiant numérique
             du serveur défini par "id", ou par défaut de sa position dans
             la liste des serveurs, mais les 32 bits de l'ID sont utilisés
             pour éviter les collisions. Contrairement à "id", cette
             valeur n'est pas mise à l'échelle ; utilisez-la toujours
             avec une fonction de hachage (voir "hash-key") ou avec des
             ID explicitement attribués et uniformément répartis dans
             l'espace de 32 bits.

  guid       Les clés des nœuds sont dérivées du guid du serveur s'il
             existe, sinon de "id". Cela supprime toute dépendance à
             l'ordre : seul un identifiant interne stable, réplicable
             sur plusieurs répartiteurs de charge, est utilisé.

  addr       Les clés des nœuds sont dérivées de l'adresse du serveur
             si elle est disponible, sinon de "id".

  addr-port  Les clés des nœuds sont dérivées de l'adresse et du port du
             serveur s'ils sont disponibles, sinon de "id".
```

Les options « addr » et « addr-port » peuvent être utiles dans les scénarios où plusieurs processus HAProxy répartissent le trafic vers le même ensemble de serveurs. Si l'ordre des serveurs est différent pour chaque processus (par exemple, en raison d'une résolution DNS effectuée dans un ordre différent), cela permet à chaque processus HAProxy indépendant de s'accorder sur les décisions de routage. Remarque : « balance random » utilise également « hash-type consistent », et la qualité de la répartition dépendra de la qualité des clés.

<a id="entry-5-2-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Peut être utilisé dans les contextes suivants : tcp, http

Spécifiez la section de contrôle d'état à utiliser pour effectuer le contrôle sur le serveur.

Argument :

```text
<name>    est le nom de la section de contrôle d'état.
```

Grâce à cette option, il est possible d'utiliser une configuration de contrôle d'état préalable du serveur au lieu d'utiliser la configuration du proxy. Voir également la section « healthcheck ».

<a id="entry-5-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Définir un identifiant persistant pour le serveur. Cet identifiant doit être un nombre positif sur 32 bits et unique pour le proxy. Un identifiant non utilisé sera automatiquement attribué si ce paramètre n'est pas défini. La première valeur attribuée sera 1. Cet identifiant est actuellement renvoyé uniquement dans les statistiques, et est utilisé pour positionner les nœuds de répartition de charge lors de l'utilisation d'algorithmes de hachage cohérents lorsque « hash-key » est défini sur « id » (valeur par défaut). Dans ce cas, seuls les 20 bits les plus bas de la valeur sont utilisés (c’est-à-dire (id % 1048576)), il est donc préférable d’utiliser uniquement des valeurs comprises entre 1 et cette valeur afin d’éviter les chevauchements.

<a id="entry-5-2-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Définir un intervalle pour le contrôle périodique de la disponibilité des connexions backend inactives. Si la partie distante ne parvient pas à répondre avant le prochain test planifié, la connexion est fermée. Ce mot-clé fait référence au côté backend, ce qui est utile pour vérifier que les connexions inactives restent utilisables. Notez que cela n'empêche pas la destruction de la connexion lors de la purge du pool de connexions inactives.

Cette fonctionnalité dépend d'un support spécifique du protocole sous-jacent. Pour l'instant, seul H2 mux l'implémente.
Idle-ping est simplement ignoré par les autres protocoles.

Cette option est particulièrement utile lors de l'utilisation d'un proxy inverse HTTP. La définir sur la ligne serveur est utile pour le pair qui écoute les connexions entrantes et les associe à un serveur correspondant afin de pouvoir réutiliser ultérieurement le transfert de trafic.

<a id="entry-5-2-init-addr"></a>

**`init-addr {last | libc | none | <ip>},[...]*`**

```haproxy
init-addr {last | libc | none | <ip>},[...]*
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Indiquez dans quel ordre l'adresse du serveur doit être résolue au démarrage s'il utilise un nom complet (FQDN).
Des tentatives sont effectuées pour résoudre l'adresse en appliquant successivement chacune des méthodes mentionnées dans la liste séparée par des virgules. La première méthode réussie est utilisée. Si la fin de la liste est atteinte sans trouver de méthode fonctionnelle, une erreur est levée. La méthode « last » indique de choisir l'adresse figurant dans le fichier d'état (voir « server-state-file »). La méthode « libc » utilise le résolveur interne de libc (gethostbyname() ou getaddrinfo() selon le système d'exploitation et les options de compilation). La méthode « none » indique spécifiquement que le serveur doit démarrer sans adresse IP valide, dans un état down. Cela peut être utile pour ignorer certains problèmes DNS au démarrage, en attendant que la situation soit corrigée ultérieurement. Enfin, une adresse IP (IPv4 ou IPv6) peut être fournie. Elle peut être l'adresse actuellement connue du serveur (par exemple, renseignée par un générateur de configuration), ou l'adresse d'un serveur factice utilisé pour capter les sessions anciennes et leur présenter un message d'erreur approprié. Lorsque l'algorithme de répartition de charge « first » est utilisé, cette adresse IP peut pointer vers un serveur factice utilisé pour déclencher la création d'instances nouvelles en temps réel. Cette option est par défaut définie sur « last,libc », ce qui signifie que l'adresse précédemment trouvée dans le fichier d'état (le cas échéant) est utilisée en priorité, sinon le résolveur libc est utilisé. Cela garantit une compatibilité continue avec le comportement historique. Lors de l'utilisation de résolveurs internes, il est généralement recommandé de désactiver la résolution basée sur libc, ou de la rendre explicite (voir [section 5.3](/fr/haproxy/bind-and-server-options/#section-5-3) pour plus de détails).

Exemple 1 :

```text
defaults
    # never fail on address resolution
    default-server init-addr last,libc,none
```

Exemple 2 :

```text
defaults
    # disable libc resolution in combination with resolvers
    default-server init-addr last,none
```

<a id="entry-5-2-inter"></a>

**`inter <delay>`**

```haproxy
inter <delay>
fastinter <delay>
downinter <delay>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « inter » définit l'intervalle entre deux contrôles d'état consécutifs en `<delay>` millisecondes. Si non spécifié, le délai par défaut est de 2000 ms. Il est également possible d'utiliser « fastinter » et « downinter » afin d'optimiser les délais entre les contrôles en fonction de l'état du serveur :

```text
             État du serveur                |         Intervalle utilisé
    ----------------------------------------+----------------------------------
     UP 100% (sans transition)              | "inter"
    ----------------------------------------+----------------------------------
     UP en transition (vers DOWN "fall"),  | "fastinter" si défini,
     DOWN en transition (vers UP "rise"),  | "inter" sinon.
     ou pas encore vérifié.                 |
    ----------------------------------------+----------------------------------
     DOWN 100% (sans transition)            | "downinter" si défini,
                                            | "inter" sinon.
    ----------------------------------------+----------------------------------
```

Tout comme pour tout autre paramètre basé sur le temps, ils peuvent être entrés dans n'importe quelle autre unité explicite parmi { us, ms, s, m, h, d }. Le paramètre « inter » sert également de délai d'expiration pour les contrôles d'état envoyés aux serveurs si « timeout check » n'est pas défini. Afin de réduire les effets de « résonance » lorsque plusieurs serveurs sont hébergés sur le même matériel, l'agent et les contrôles d'état de tous les serveurs sont lancés avec un petit décalage temporel entre eux. Il est également possible d'ajouter un bruit aléatoire dans l'intervalle des agents et des contrôles d'état en utilisant le mot-clé global « spread-checks ». Cela a un sens, par exemple, lorsque de nombreux backends utilisent les mêmes serveurs. Le paramètre global "tune.max-checks-per-thread", s'il est défini à une valeur non nulle, limitera le nombre de contrôles simultanés effectués en même temps sur un thread donné. Pour y parvenir, HAProxy mettra en file d'attente les contrôles qui devaient démarrer sur un thread ayant atteint cette limite, jusqu'à ce qu'un autre contrôle se termine. Cela aura pour effet d'élargir l'intervalle de contrôle effectif. Dans ce cas, réduire la valeur du paramètre « inter » aura un effet très limité, car elle ne pourra pas réduire le temps passé en file d'attente.

<a id="entry-5-2-init-state"></a>

**`init-state { fully-up | up | down | fully-down | none }`**

```haproxy
init-state { fully-up | up | down | fully-down | none }
```

Peut être utilisé dans les contextes suivants : tcp, http

Peut être utilisé dans les sections : defaults \| frontal \| listen \| backend non \| non \| oui \| oui

L'option « init-state » définit l'état initial du serveur :   - lorsqu'elle est définie sur « fully-up », le serveur est considéré comme immédiatement disponible, et, si les contrôles d'état sont activés pour ce serveur, il passera à l'état DOWN lorsque TOUS les contrôles d'état échouent.   - lorsqu'elle est définie sur « up », le serveur est considéré comme immédiatement disponible, et, si les contrôles d'état sont activés pour ce serveur, il passera immédiatement à l'état DOWN si le prochain contrôle d'état échoue.   - lorsqu'elle est définie sur « down », le serveur est initialement considéré comme indisponible, et, si les contrôles d'état sont activés pour ce serveur, il peut passer à l'état UP si le prochain contrôle d'état réussit.   - lorsqu'elle est définie sur « fully-down », le serveur est initialement considéré comme indisponible, et, si les contrôles d'état sont activés pour ce serveur, il passera à l'état UP lorsque TOUS les contrôles d'état réussissent.   - lorsqu'elle est définie sur « none » (valeur par défaut), la gestion de l'état initial est désactivée. Elle peut être utilisée pour restaurer le comportement par défaut lorsque ce paramètre était hérité d'une directive « default-server ».

L'état initial du serveur est pris en compte lors du démarrage (ou redémarrage) de l'instance HAProxy, lorsqu'un nouveau serveur est détecté (par exemple via la découverte de services ou la résolution DNS), lorsqu'un serveur dynamique devient actif, lorsqu'un serveur quitte le mode maintenance, etc. Cette directive ne peut pas être utilisée lorsque le serveur suit un autre serveur.

Exemples :

```shell
# pass client traffic ONLY to Redis "master" node
backend redis-master
  mode tcp
  balance first
  option tcp-check
  tcp-check send role\r\n
  tcp-check expect string master
  server-template redis 3 _redis._tcp.redis-headless-service.sandbox.svc.cluster.local:6379 check ... init-state down

# pass traffic to the server only after 3 successful health checks
backend google-backend
  mode http
  server srv1 google.com:80 check init-state fully-down rise 3
  server srv2 google.com:80 check init-state fully-down rise 3
```

Voir également : « option tcp-check », « option httpchk »

<a id="entry-5-2-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Active ou désactive kTLS pour ces sockets. Si activé, kTLS sera utilisé si le noyau le prend en charge et si le chiffrement est compatible. Cette fonctionnalité n'est disponible qu'avec Linux 4.17 et versions ultérieures. Veuillez noter que certains pilotes réseau et/ou piles TLS peuvent limiter l'utilisation de kTLS à TLS v1.2 uniquement. Voir également « force-tlsv12 ».

<a id="entry-5-2-log-bufsize"></a>

**`log-bufsize <bufsize>`**

```haproxy
log-bufsize <bufsize>
```

Peut être utilisé dans les contextes suivants : log

Le paramètre « log-bufsize » spécifie la taille de la mémoire tampon anneau à utiliser pour l'anneau implicite associé au serveur de journalisation dans un backend de journalisation. En l'absence de spécification, cette valeur par défaut est BUFSIZE. Une valeur plus élevée augmente l'utilisation de la mémoire, mais peut aider à éviter la perte de messages de journalisation avec des serveurs lents, car la mémoire tampon pourra contenir davantage de messages en attente. Ce mot-clé ne peut être utilisé que dans les sections de backend de journalisation (avec « mode log »).

<a id="entry-5-2-log-proto"></a>

**`log-proto <logproto>`**

```haproxy
log-proto <logproto>
```

Peut être utilisé dans les contextes suivants : log, ring

Le paramètre « log-proto » spécifie le protocole utilisé pour acheminer les messages d'événement vers un serveur configuré dans une section log ou ring. Les valeurs possibles sont « legacy » et « octet-count », correspondant respectivement à « Non-transparent-framing » et « Octet counting » dans le rfc6587. La valeur par défaut est « legacy ».

<a id="entry-5-2-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « maxconn » spécifie le nombre maximal de connexions simultanées qui seront envoyées à ce serveur. Si le nombre de connexions entrantes simultanées dépasse cette valeur, celles-ci seront placées en file d'attente, en attendant qu'une place soit libérée. Ce paramètre est très important car il peut empêcher des serveurs fragiles de tomber sous des charges extrêmes. Si un paramètre « minconn » est spécifié, la limite devient dynamique. La valeur par défaut est « 0 », ce qui signifie sans limite. Voir également les paramètres « minconn » et « maxqueue », ainsi que le mot-clé « fullconn » du backend.

En mode HTTP, ce paramètre limite le nombre de requêtes simultanées au lieu du nombre de connexions. Plusieurs requêtes peuvent être multiplexées sur une seule connexion TCP vers le serveur. Par exemple, si vous spécifiez une valeur maxconn de 50, vous pouvez observer entre 1 et 50 connexions réelles vers le serveur, mais jamais plus de 50 requêtes simultanées.

<a id="entry-5-2-maxqueue"></a>

**`maxqueue <maxqueue>`**

```haproxy
maxqueue <maxqueue>
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « maxqueue » spécifie le nombre maximal de connexions pouvant attendre dans la file d'attente pour ce serveur. Si cette limite est atteinte, les requêtes suivantes seront redirigées vers d'autres serveurs au lieu de rester indéfiniment en attente. Cela rompt la persistance, mais peut permettre à des utilisateurs de se reconnecter rapidement lorsque le serveur vers lequel ils tentent de se connecter est en panne. Certains algorithmes de répartition de charge, comme « leastconn », tiennent compte de cette valeur et acceptent d'ajouter des requêtes à la file d'attente d'un serveur jusqu'à cette limite, à condition qu'elle soit explicitement définie à une valeur strictement supérieure à zéro, ce qui permet souvent de mieux lisser la charge lorsqu'on utilise des valeurs de « maxconn » à un chiffre. La valeur par défaut est « 0 », ce qui signifie que la file d'attente est illimitée. Voir également les paramètres « maxconn » et « minconn », ainsi que « balance leastconn ».

<a id="entry-5-2-max-reuse"></a>

**`max-reuse <count>`**

```haproxy
max-reuse <count>
```

Peut être utilisé dans les contextes suivants : http, ring

Lorsqu'il est utilisé dans un contexte http :

L'argument « max-reuse » indique aux processeurs de connexions HTTP de ne pas réutiliser une connexion serveur plus de ce nombre de fois pour envoyer de nouvelles requêtes. Les valeurs autorisées sont -1 (valeur par défaut), qui désactive cette limite, ou toute valeur positive. La valeur zéro désactive effectivement keep-alive. Cette option est uniquement destinée à contourner certaines erreurs serveur qui entraînent une fuite de ressources au fil du temps. L'argument n'est pas nécessairement respecté par les couches inférieures en raison de limitations techniques pouvant rendre son application impossible. Au moins les connexions HTTP/2 vers les serveurs le respecteront.

Lorsqu'il est utilisé dans un contexte anneau :

L'argument « max-reuse » indique que les processeurs de connexion TCP du réceptacle ne doivent pas réutiliser une connexion serveur plus de ce nombre de fois pour envoyer des messages. Cela signifie que la connexion vers le serveur sera détruite de force une fois qu'au moins « max-reuse + 1 » messages auront été traités sur la même connexion. La connexion vers le serveur sera alors automatiquement recréée. En cas de traitement d'un grand nombre de messages dans un contexte multithreadé, cela peut aider à mieux répartir la charge de l'anneau sur plusieurs threads. En effet, chaque connexion est associée au même thread CPU pendant toute sa durée : contrairement au protocole HTTP, il n'existe pas de transaction syslog, aussi la connexion serveur peut-elle persister indéfiniment tant que le serveur ne ferme pas la connexion ou qu'aucune erreur réseau ne se produit. En détruisant périodiquement les connexions, on donne la possibilité aux autres threads de traiter des messages à leur tour. Cela peut également aider à effectuer une rotation propre des serveurs de journalisation dans des contextes où il existe une couche supplémentaire de répartition de charge entre HAProxy et les serveurs de journalisation. Toutefois, gardez à l'esprit qu'à chaque recyclage de connexion, un port sortant reste en état TIME_WAIT pendant environ une minute sur les systèmes d'exploitation modernes, et qu'il convient donc d'éviter d'utiliser des valeurs trop faibles afin de prévenir l'épuisement rapide des ports sources. En règle générale, assurez-vous de ne jamais fermer plus de quelques fois par seconde, et idéalement beaucoup moins souvent. Les valeurs autorisées sont -1 (valeur par défaut), qui désactive cette limite, ou toute valeur positive. Contrairement au contexte HTTP, lorsque utilisé avec des serveurs réceptacles, « max-reuse » est appliqué au mieux : les messages de l'anneau sont regroupés par lots, aussi la limite est-elle vérifiée entre chaque lot.

<a id="entry-5-2-minconn"></a>

**`minconn <minconn>`**

```haproxy
minconn <minconn>
```

Peut être utilisé dans les contextes suivants : tcp, http

Lorsque le paramètre « minconn » est défini, la limite maxconn devient une limite dynamique suivant la charge du backend. Le serveur acceptera toujours au moins `<minconn>` connexions, jamais plus de `<maxconn>`, et la limite évoluera progressivement entre ces deux valeurs lorsque le backend dispose de moins de `<fullconn>` connexions simultanées. Cela permet de limiter la charge sur le serveur en conditions normales, tout en permettant de pousser davantage la charge en cas de charges importantes, sans surcharger le serveur en cas de charges exceptionnelles. Voir également les paramètres « maxconn » et « maxqueue », ainsi que le mot-clé backend « fullconn ».

<a id="entry-5-2-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Sous Linux, il est possible de spécifier l'espace de noms réseau auquel un socket appartient. Cette directive permet de lier explicitement un serveur à un espace de noms différent de celui par défaut. Veuillez vous référer à la documentation de votre système d'exploitation pour obtenir davantage de détails sur les espaces de noms réseau.

<a id="entry-5-2-no-agent-check"></a>

**`no-agent-check`**

```haproxy
no-agent-check
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « agent-check » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « agent-check » « default-server » précédent.

<a id="entry-5-2-no-backup"></a>

**`no-backup`**

```haproxy
no-backup
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « backup » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « backup » précédent défini sur « default-server ».

<a id="entry-5-2-no-check"></a>

**`no-check`**

```haproxy
no-check
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « check » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « check » « default-server » précédent.

<a id="entry-5-2-no-check-reuse-pool"></a>

**`no-check-reuse-pool`**

```haproxy
no-check-reuse-pool
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option annule toute option « check-reuse-pool » précédemment définie, éventuellement héritée d’un « default-server ». Tous les contrôles seront effectués sur une connexion dédiée.

<a id="entry-5-2-no-check-sni-auto"></a>

**`no-check-sni-auto`**

```haproxy
no-check-sni-auto
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée en tant que paramètre « server » pour désactiver la sélection automatique du SNI pour les contrôles d'état SSL, qui est activée par défaut.

Voir l'option « no-sni-auto » pour désactiver la sélection automatique du SNI pour le trafic proxyé.

<a id="entry-5-2-no-check-ssl"></a>

**`no-check-ssl`**

```haproxy
no-check-ssl
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « check-ssl » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « check-ssl » précédent défini sur « default-server ».

<a id="entry-5-2-no-renegotiate"></a>

**`no-renegotiate`**

```haproxy
no-renegotiate
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il désactive les mécanismes de renégociation, qu'il s'agisse de l'ancien mécanisme non sécurisé ou du mécanisme plus récent « renégociation sécurisée » (extension RFC 5746 TLS Renegotiation Indication), pour le backend SSL concerné. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». La renégociation n'est plus possible dans TLS 1.3. Si ni « renegotiate » ni « no-renegotiate » n'est spécifié, le comportement par défaut de la bibliothèque SSL est conservé.
Notez qu’OpenSSL active par défaut la renégociation sécurisée, tandis qu’AWS-LC la désactive. Voir également « renegotiate ».

<a id="entry-5-2-no-send-proxy"></a>

**`no-send-proxy`**

```haproxy
no-send-proxy
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « send-proxy » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « send-proxy » « default-server » précédent.

<a id="entry-5-2-no-send-proxy-v2"></a>

**`no-send-proxy-v2`**

```haproxy
no-send-proxy-v2
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « send-proxy-v2 » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « send-proxy-v2 » précédemment défini sur « default-server ».

<a id="entry-5-2-no-send-proxy-v2-ssl"></a>

**`no-send-proxy-v2-ssl`**

```haproxy
no-send-proxy-v2-ssl
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « send-proxy-v2-ssl » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « send-proxy-v2-ssl » précédemment défini sur « default-server ».

<a id="entry-5-2-no-send-proxy-v2-ssl-cn"></a>

**`no-send-proxy-v2-ssl-cn`**

```haproxy
no-send-proxy-v2-ssl-cn
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « send-proxy-v2-ssl-cn » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « send-proxy-v2-ssl-cn » précédemment défini sur « default-server ».

<a id="entry-5-2-no-sni-auto"></a>

**`no-sni-auto`**

```haproxy
no-sni-auto
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée en tant que paramètre « server » pour désactiver la sélection automatique du SNI, qui est activée par défaut.

Voir l'option « no-check-sni-auto » pour désactiver la sélection automatique du SNI pour les contrôles d'état SSL.

<a id="entry-5-2-no-ssl"></a>

**`no-ssl`**

```haproxy
no-ssl
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « ssl » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « ssl » « default-server » précédent.

Notez que l'utilisation de la configuration `default-server ssl` et de `no-ssl` sur le serveur initie toutefois une connexion SSL, qui peut ensuite être activée via l'API d'exécution : consultez les commandes `set server` dans la documentation d'administration.

<a id="entry-5-2-no-ssl-reuse"></a>

**`no-ssl-reuse`**

```haproxy
no-ssl-reuse
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la réutilisation des sessions SSL lors de la communication avec le serveur. Elle oblige le serveur à effectuer une négociation complète pour chaque nouvelle connexion. Elle est probablement utile uniquement à des fins de benchmark, de dépannage ou pour des utilisateurs paranoïaques.

<a id="entry-5-2-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la prise en charge de SSLv3 lors de la communication avec le serveur via SSL. Notez que SSLv2 est désactivé dans le code et ne peut pas être activé à l’aide de toute option de configuration. Utilisez plutôt « ssl-min-ver » et « ssl-max-ver ».

Pris en charge dans default-server : Non

<a id="entry-5-2-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il désactive la reprise de session sans état (extension TLS Ticket RFC 5077) et force l'utilisation de la reprise de session avec état. La reprise de session sans état est plus coûteuse en ressources CPU pour les serveurs. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Le mécanisme des tickets TLS n'est utilisé qu'avec TLS 1.2 au maximum. La confidentialité persistante est compromise avec les tickets TLS, sauf si les clés de ticket sont régulièrement renouvelées (par rechargement ou en utilisant « tls-ticket-keys »). Voir également « tls-tickets ».

<a id="entry-5-2-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la prise en charge de TLSv1.0 lors de l'utilisation de SSL pour la communication avec le serveur. Notez que SSLv2 est désactivé dans le code et ne peut pas être activé à l'aide d'aucune option de configuration. TLSv1 est plus coûteux que SSLv3, il est donc souvent pertinent de le désactiver lors de la communication avec des serveurs locaux. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Privilégiez plutôt les options « ssl-min-ver » et « ssl-max-ver ».

Pris en charge dans default-server : Non

<a id="entry-5-2-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la prise en charge de TLSv1.1 lors de l'utilisation de SSL pour la communication avec le serveur. Notez que SSLv2 est désactivé dans le code et ne peut pas être activé à l'aide de toute option de configuration. TLSv1 est plus coûteux que SSLv3, il est donc souvent pertinent de le désactiver lors de la communication avec des serveurs locaux. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Privilégiez plutôt les options « ssl-min-ver » et « ssl-max-ver ».

Pris en charge dans default-server : Non

<a id="entry-5-2-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la prise en charge de TLSv1.2 lors de l'utilisation de SSL pour la communication avec le serveur. Notez que SSLv2 est désactivé dans le code et ne peut pas être activé à l'aide d'aucune option de configuration. TLSv1 est plus coûteux que SSLv3, il est donc souvent pertinent de le désactiver lors de la communication avec des serveurs locaux. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Privilégiez plutôt les options « ssl-min-ver » et « ssl-max-ver ».

Pris en charge dans default-server : Non

<a id="entry-5-2-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option désactive la prise en charge de TLSv1.3 lors de l'utilisation de SSL pour la communication avec le serveur. Notez que SSLv2 est désactivé dans le code et ne peut pas être activé à l'aide de toute option de configuration. TLSv1 est plus coûteux que SSLv3, il est donc souvent pertinent de le désactiver lors de la communication avec des serveurs locaux. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Privilégiez plutôt les options « ssl-min-ver » et « ssl-max-ver ».

Pris en charge dans default-server : Non

<a id="entry-5-2-no-verifyhost"></a>

**`no-verifyhost`**

```haproxy
no-verifyhost
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « verifyhost » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « verifyhost » « default-server » précédent.

<a id="entry-5-2-no-tfo"></a>

**`no-tfo`**

```haproxy
no-tfo
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « tfo » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre « tfo » « default-server » précédent.

<a id="entry-5-2-non-stick"></a>

**`non-stick`**

```haproxy
non-stick
```

Peut être utilisé dans les contextes suivants : tcp, http

N'ajoutez jamais les connexions attribuées à ce serveur à une table de persistance. Cela peut être utilisé conjointement avec backup afin de garantir que la persistance par table de persistance est désactivée pour les serveurs de secours.

<a id="entry-5-2-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Peut être utilisé dans les contextes suivants : tcp, http

Cela active l'extension TLS NPN et annonce la liste de protocoles spécifiée comme prise en charge au-dessus de NPN. La liste de protocoles est constituée d'une liste séparée par des virgules de noms de protocoles, par exemple :
"http/1.1,http/1.0" (sans guillemets). Cela nécessite que la bibliothèque SSL soit compilée avec le support des extensions TLS activé (vérifiez avec haproxy -vv). Notez que l'extension NPN a été remplacée par l'extension ALPN (voir le mot-clé « alpn »), bien que celle-ci ne soit disponible qu'à partir d'OpenSSL 1.0.2.

Compatibilité : OpenSSL >= 1.0.1. Non pris en charge avec AWS-LC.

<a id="entry-5-2-observe"></a>

**`observe <mode>`**

```haproxy
observe <mode>
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option active l’ajustement de l’état du serveur en fonction de l’observation de la communication avec celui-ci. Par défaut, cette fonctionnalité est désactivée, et son activation nécessite également l’activation des contrôles d’état. Deux modes sont pris en charge : "layer4" et "layer7". En mode layer4, seules les connexions TCP réussies ou non réussies sont prises en compte. En mode layer7, qui n’est autorisé que pour les proxies HTTP, les réponses reçues du serveur sont vérifiées, comme un code HTTP valide/incorrect, des en-têtes non parsables, un délai d'expiration, etc. Les codes d’état valides incluent les codes 100 à 499, ainsi que 501 et 505.

Voir également les options « check », « on-error » et « error-limit ».

<a id="entry-5-2-on-error"></a>

**`on-error <mode>`**

```haproxy
on-error <mode>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Sélectionnez l'action à effectuer lorsqu’un nombre suffisant d’erreurs consécutives est détecté. Actuellement, quatre modes sont disponibles :

- fastinter : force l'activation de fastinter
- fail-check : simule un contrôle d'état échoué, active également fastinter (par défaut)
- sudden-death : simule un échec de contrôle d'état pré-fatal, un autre échec entraînera la mise hors ligne du serveur, force l'activation de fastinter
- mark-down : met immédiatement le serveur hors ligne et force l'activation de fastinter

Voir également les options « check », « observe » et « error-limit ».

<a id="entry-5-2-on-marked-down"></a>

**`on-marked-down <action>`**

```haproxy
on-marked-down <action>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Modifiez ce qui se produit lorsque le serveur est marqué comme hors service. Actuellement, une action est disponible :

- shutdown-sessions : Arrêt des flux pairs. Lorsque cette option est activée, toutes les connexions vers le serveur sont immédiatement terminées lorsque le serveur tombe en panne. Elle peut être utilisée si le contrôle d'état détecte des cas plus complexes qu'un simple statut de connexion, et que des délais d'expiration longs entraîneraient une indisponibilité prolongée du service. Par exemple, un contrôle d'état pourrait détecter qu'une base de données est bloquée et qu'il n'y a plus aucune chance de réutiliser les connexions existantes. Les connexions interrompues de cette manière sont journalisées avec un code de terminaison « D » (pour « Down »).

Les actions sont désactivées par défaut

<a id="entry-5-2-on-marked-up"></a>

**`on-marked-up <action>`**

```haproxy
on-marked-up <action>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Modifiez ce qui se produit lorsque le serveur est marqué comme actif. Actuellement, une action est disponible :

- shutdown-backup-sessions : Interrompt les flux sur tous les serveurs de secours. Cela n'est effectué que si le serveur n'est pas en état de secours et s'il n'est pas désactivé (son poids effectif doit être supérieur à 0). Cette option peut parfois être utilisée pour forcer un serveur actif à reprendre tout le trafic après une récupération, notamment lors de sessions longues (par exemple, LDAP, SQL, ...). Cette opération peut causer plus de problèmes qu'elle n'en résout (par exemple, transactions incomplètes), aussi doit-elle être utilisée avec une extrême prudence. Les flux interrompus en raison de la remise en service d'un serveur sont journalisés avec un code de terminaison « U » (pour « Up »).

Les actions sont désactivées par défaut

<a id="entry-5-2-pool-conn-name"></a>

**`pool-conn-name <expr>`**

```haproxy
pool-conn-name <expr>
```

Peut être utilisé dans les contextes suivants : http

Lorsqu'une connexion vers un backend est établie, cette expression est évaluée afin de générer le nom de la connexion. Ce nom est l'une des propriétés clés de la connexion dans le pool de serveurs inactifs. Voir le mot-clé « http-reuse ». Lorsqu'une requête recherche une connexion inactive existante, cette expression est évaluée afin de trouver une connexion identique.

Dans un contexte où le SNI SSL est utilisé pour la connexion au backend, le nom de connexion est automatiquement attribué au résultat de l'expression « sni ». Cette configuration convient à l'utilisation la plus courante. Pour des configurations plus avancées, « pool-conn-name » peut être utilisé pour remplacer cette attribution.

Voir aussi : « http-reuse », « sni »

<a id="entry-5-2-pool-low-conn"></a>

**`pool-low-conn <max>`**

```haproxy
pool-low-conn <max>
```

Peut être utilisé dans les contextes suivants : http

Définissez un seuil bas sur le nombre de connexions inactives pour un serveur, en dessous duquel un thread ne tentera pas de voler une connexion à un autre thread. Cela peut être utile pour améliorer les performances du processeur dans les scénarios impliquant de nombreux serveurs très rapides, afin de garantir que tous les threads conservent toujours quelques connexions inactives, plutôt que de laisser les connexions s'accumuler sur un seul thread et être migrées d'un thread à l'autre. Des valeurs typiques équivalentes à deux fois le nombre de threads semblent déjà offrir de très bonnes performances avec des temps de réponse inférieurs à la milliseconde. La valeur par défaut est zéro, ce qui indique qu'une connexion inactive peut être utilisée à tout moment. Il s'agit du paramétrage recommandé pour une utilisation normale. Cette option s'applique uniquement aux connexions pouvant être partagées selon les mêmes principes que ceux régissant « http-reuse ». Dans le cas où le partage de connexion entre threads serait désactivé via "tune.idle-pool.shared", il devient très important d'utiliser ce paramètre afin de garantir qu'un thread dispose toujours de quelques connexions, sinon le taux de réutilisation des connexions diminuera à mesure que le nombre de threads augmente.

<a id="entry-5-2-pool-max-conn"></a>

**`pool-max-conn <max>`**

```haproxy
pool-max-conn <max>
```

Peut être utilisé dans les contextes suivants : http

Définir le nombre maximal de connexions inactives pour un serveur. -1 signifie un nombre illimité de connexions, 0 signifie aucune connexion inactive. La valeur par défaut est -1. Lorsque les connexions inactives sont activées, les connexions inactives orphelines qui ne sont plus associées à aucune session cliente sont transférées dans un pool dédié afin de rester utilisables par les clients futurs. Cela ne s'applique qu'aux connexions pouvant être partagées selon les mêmes principes que ceux régissant le « http-reuse ».

<a id="entry-5-2-pool-purge-delay"></a>

**`pool-purge-delay <delay>`**

```haproxy
pool-purge-delay <delay>
```

Peut être utilisé dans les contextes suivants : http

Définit le délai avant le démarrage de la suppression des connexions inactives. À chaque intervalle `<delay>`, la moitié des connexions inactives est fermée. Une valeur de 0 signifie qu'aucune connexion inactive n'est conservée. La valeur par défaut est 5s.

<a id="entry-5-2-port"></a>

**`port <port>`**

```haproxy
port <port>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

En utilisant le paramètre « port », il devient possible d'utiliser un port différent pour envoyer les contrôles d'état ou pour sonder l'agent-check. Sur certains serveurs, il peut être souhaitable de réserver un port à un composant spécifique capable d'exécuter des tests complexes, plus adaptés aux contrôles d'état que l'application elle-même. Il est courant, par exemple, d'exécuter un script simple via inetd. Ce paramètre est ignoré si le paramètre « check » n'est pas défini. Voir également le paramètre « addr ».

<a id="entry-5-2-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Peut être utilisé dans les contextes suivants : tcp, http

Force le protocole du multiplexeur à utiliser pour les connexions sortantes vers ce serveur. Il doit être compatible avec le mode du backend (TCP ou HTTP). Il doit également être utilisable du côté du backend. La liste des protocoles disponibles est indiquée par haproxy -vv. Les propriétés des protocoles sont les suivantes : le mode (TCP/HTTP), le côté (FE/BE), le nom du multiplexeur et ses indicateurs.

Certains protocoles sont sujets au blocage par tête de file côté serveur (drapeau=HOL_RISK). Enfin, certains protocoles ne prennent pas en charge les mises à jour (drapeau=NO_UPG). La compatibilité HTX est également indiquée (drapeau=HTX).

Voici les protocoles pouvant être utilisés en tant qu'argument de la directive « proto » sur une ligne de serveur :

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

L'idée de cette option est de contourner le choix du meilleur protocole multiplexeur pour toutes les connexions établies vers ce serveur.

Si les paramètres ALPN ou NPN sont configurés, les protocoles spécifiés doivent être compatibles avec le protocole du multiplexeur afin d'éviter tout problème. Par exemple, si « proto h1 » est défini, l'ALPN ne doit pas être configuré sur « h2 ».

Voir également « ws » pour utiliser un protocole alternatif pour les flux WebSocket.

QMux est un sous-ensemble de QUIC qui s'exécute sur TCP. Il correspond au protocole proposé dans le brouillon suivant : <https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. Il est actuellement considéré comme expérimental dans HAProxy.

<a id="entry-5-2-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Ce paramètre est spécifique à QUIC et permet de sélectionner l'algorithme de contrôle de congestion pour toute connexion ciblant ce serveur. Ils sont similaires à ceux utilisés par TCP. Consultez l'option bind, dont le nom est similaire, pour une description complète de toutes les options de personnalisation.

Valeur par défaut : cubic

Voir aussi : "tune.quic.be.tx.pacing" et "tune.quic.be.cc.max-win-size"

<a id="entry-5-2-redir"></a>

**`redir <prefix>`**

```haproxy
redir <prefix>
```

Peut être utilisé dans les contextes suivants : http

Le paramètre « redir » active le mode de redirection pour toutes les requêtes GET et HEAD adressées à ce serveur. Cela signifie qu’au lieu de transmettre la requête au serveur, HAProxy renvoie une réponse « HTTP 302 » dont l’en-tête « Location » est composé de ce préfixe immédiatement suivi de l’URI demandé, commençant par le « / » initial du composant de chemin. Cela implique qu’aucune barre oblique finale ne doit être utilisée après `<prefix>`. Toutes les requêtes non valides seront rejetées, et toutes les requêtes autres que GET ou HEAD seront normalement servies par le serveur. Notez que, puisque la réponse est entièrement générée, aucune modification d’en-tête ni insertion de cookie n’est possible dans la réponse. Toutefois, les cookies présents dans les requêtes sont toujours analysés, rendant cette solution entièrement utilisable pour rediriger les utilisateurs vers un emplacement distant en cas de catastrophe locale. Son usage principal consiste à augmenter la bande passante des serveurs statiques en faisant établir la connexion directe par les clients. Attention : n’utilisez jamais une localisation relative ici, cela provoquerait une boucle entre le client et HAProxy !

Exemple : server srv1 192.168.1.1:80 redir <http://image1.mydomain.com> check

<a id="entry-5-2-renegotiate"></a>

**`renegotiate`**

```haproxy
renegotiate
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option active le mécanisme de renégociation sécurisée (extension Indication de renégociation TLS RFC 5746) pour un backend SSL donné. Cela ne signifie pas que le client SSL enverra des demandes de renégociation, mais seulement qu’un backend peut renégocier lorsqu’une requête est émise par le serveur. Cette fonctionnalité nécessite que la bibliothèque SSL sous-jacente prenne effectivement en charge la renégociation. Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». La renégociation n’est plus possible dans TLS 1.3. Si ni « renegotiate » ni « no-renegotiate » n’est spécifié, le comportement par défaut de la bibliothèque SSL est conservé. Notez qu’OpenSSL active par défaut la renégociation sécurisée, tandis qu’AWS-LC la désactive.

<a id="entry-5-2-rise"></a>

**`rise <count>`**

```haproxy
rise <count>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Le paramètre « rise » indique qu'un serveur est considéré comme opérationnel après `<count>` contrôles d'état consécutifs réussis. Cette valeur vaut 2 par défaut si non spécifiée. Voir également les paramètres « check », « inter » et « fall ».

resolve-opts `<option>`,`<option>`,... Peut être utilisé dans les contextes suivants : tcp, http, log

Liste séparée par des virgules d'options à appliquer à la résolution DNS liée à ce serveur.

Options disponibles :

- allow-dup-ip Par défaut, HAProxy empêche la duplication d'adresses IP dans un backend lorsque la résolution DNS est en cours à l'exécution. Toutefois, dans certains cas, il est pertinent qu'un même backend (résolu par le même FQDN) contienne deux serveurs ayant la même adresse IP. Dans ce cas, activez simplement cette option. Il s'agit de l'inverse de prevent-dup-ip.

- ignore-weight Ignore tout poids défini dans un enregistrement SRV. Cela est utile lorsque vous souhaitez contrôler les poids à l'aide d'une méthode alternative, par exemple en utilisant un « agent-check » ou via l'API d'exécution.

- prevent-dup-ip Assure que le comportement par défaut d'HAProxy est appliqué sur un serveur : empêche la réutilisation d'une adresse IP déjà attribuée à un serveur dans le même backend et partageant le même fqdn. Cela constitue l'inverse de allow-dup-ip.

Exemple :

```text
backend b_myapp
  default-server init-addr none resolvers dns
  server s1 myapp.example.com:80 check resolve-opts allow-dup-ip
  server s2 myapp.example.com:81 check resolve-opts allow-dup-ip
```

Avec l'option allow-dup-ip activée :

- si le serveur de noms retourne une seule adresse IP, les deux serveurs l'utiliseront
- Si le serveur de noms retourne 2 adresses IP, chaque serveur choisira une adresse différente

Valeur par défaut : non définie

<a id="entry-5-2-resolve-prefer"></a>

**`resolve-prefer <family>`**

```haproxy
resolve-prefer <family>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Lorsque la résolution DNS est activée pour un serveur et que plusieurs adresses IP provenant de familles différentes sont retournées, HAProxy privilégie l'utilisation d'une adresse IP de la famille indiquée dans le paramètre « resolve-prefer ». Voir également le mot-clé global « dns-accept-family » pour imposer une utilisation stricte d'une famille spécifique. Familles disponibles : « ipv4 » et « ipv6 ».

Valeur par défaut : ipv6

Exemple :

```text
server s1 app1.domain.com:80 resolvers mydns resolve-prefer ipv6
```

<a id="entry-5-2-resolve-net"></a>

**`resolve-net <network>[,<network[,...]]`**

```haproxy
resolve-net <network>[,<network[,...]]
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option priorise le choix d'une adresse IP correspondant à un réseau. Cela est utile dans les environnements cloud pour privilégier une adresse locale. Dans certains cas, un service de haute disponibilité cloud peut être annoncé avec plusieurs adresses IP sur différents centres de données. La latence entre les centres de données n'est pas négligeable, aussi cette option permet de privilégier un centre de données local. Si aucune adresse ne correspond au réseau configuré, une autre adresse est sélectionnée.

Exemple :

```text
server s1 app1.domain.com:80 resolvers mydns resolve-net 10.0.0.0/8
```

<a id="entry-5-2-resolvers"></a>

**`resolvers <id>`**

```haproxy
resolvers <id>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Pointe vers une section « resolvers » existante afin de résoudre le nom d'hôte du serveur actuel. Il est souvent recommandé de désactiver la résolution basée sur libc lors de l'utilisation des resolvers, bien que des exceptions existent (voir [section 5.3.1](/fr/haproxy/bind-and-server-options/#section-5-3-1)). Dans tous les cas, il est bon de spécifier explicitement « init-addr » lors de l'utilisation des resolvers afin de ne pas négliger cet élément.

Exemple :

```text
server s1 app1.domain.com:80 init-addr last,none check resolvers mydns
```

Voir également [section 5.3](/fr/haproxy/bind-and-server-options/#section-5-3) pour les détails d'implémentation et les pièges à connaître.

<a id="entry-5-2-send-proxy"></a>

**`send-proxy`**

```haproxy
send-proxy
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « send-proxy » impose l'utilisation du protocole PROXY sur toute connexion établie vers ce serveur. Le protocole PROXY informe l'autre extrémité des adresses couche 3/4 de la connexion entrante, afin qu'elle puisse connaître l'adresse du client ou l'adresse publique utilisée, quel que soit le protocole de couche supérieure. Pour les connexions acceptées par un écouteur « accept-proxy » ou « accept-netscaler-cip », l'adresse annoncée sera utilisée. Seules les familles d'adresses TCPv4 et TCPv6 sont prises en charge. Les autres familles, telles que les sockets Unix, signaleront une famille INCONNUE. Les serveurs utilisant cette option peuvent être entièrement chaînés à une autre instance de HAProxy écoutant avec une configuration « accept-proxy ». Ce paramètre ne doit pas être utilisé si le serveur n'est pas conscient du protocole. Lorsqu'un contrôle d'état est envoyé au serveur, le protocole PROXY est automatiquement utilisé lorsque cette option est activée, sauf si une directive explicite « port » ou « addr » est présente, auquel cas une directive explicite « check-send-proxy » serait également nécessaire pour utiliser le protocole PROXY. Voir également l'option « no-send-proxy » de cette section et les options « accept-proxy » et « accept-netscaler-cip » de la directive « bind ».

<a id="entry-5-2-send-proxy-v2"></a>

**`send-proxy-v2`**

```haproxy
send-proxy-v2
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « send-proxy-v2 » impose l'utilisation du protocole PROXY version 2 sur toute connexion établie vers ce serveur. Le protocole PROXY informe l'autre extrémité des adresses couche 3/4 de la connexion entrante, afin qu'elle puisse déterminer l'adresse du client ou l'adresse publique utilisée, quel que soit le protocole de couche supérieure. Il envoie également les informations ALPN si une négociation ALPN a eu lieu. Ce paramètre ne doit pas être utilisé si le serveur n'est pas conscient de cette version du protocole. Voir également l'option « no-send-proxy-v2 » de cette section et l'option « send-proxy » de la directive « bind ».

<a id="entry-5-2-set-proxy-v2-tlv-fmt"></a>

**`set-proxy-v2-tlv-fmt(<id>) <fmt>`**

```haproxy
set-proxy-v2-tlv-fmt(<id>) <fmt>
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « set-proxy-v2-tlv-fmt » est utilisé pour envoyer des TLV arbitraires du protocole PROXY version 2. Pour la plage de type (`<id>`) du type TLV défini, se référer à la section 2.2.8 de la spécification du protocole PROXY. Toutefois, la valeur peut être choisie librement, à condition de ne pas dépasser la longueur maximale de 65 535 octets. Il peut également être utilisé pour acheminer des TLV en utilisant l'extraction d'échantillon « fc_pp_tlv » afin de récupérer un TLV reçu depuis le frontal. Il peut être utilisé en tant qu’option serveur ou default-server. Il doit être utilisé en combinaison avec send-proxy-v2 afin que les TLV PPv2 soient effectivement envoyés.

Exemple : server srv1 192.168.1.1:80 send-proxy-v2 set-proxy-v2-tlv-fmt(0x20) %[fc_pp_tlv(0x20)]

Dans ce cas, nous récupérons le TLV de type 0x20 sous forme de chaîne et l’attribuons comme valeur à un nouveau TLV dont le type est également 0x20.

<a id="entry-5-2-proxy-v2-options"></a>

**`proxy-v2-options <option>[,<option>]*`**

```haproxy
proxy-v2-options <option>[,<option>]*
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « proxy-v2-options » ajoute des options à envoyer dans le protocole PROXY version 2 lorsque « send-proxy-v2 » est utilisé. Les options disponibles sont :

- ssl : Voir également « send-proxy-v2-ssl ».
- cert-cn : Voir également « send-proxy-v2-ssl-cn ».
- ssl-cipher : Nom du chiffrement utilisé.
- cert-sig : Algorithme de signature du certificat utilisé.
- cert-key : Algorithme de clé du certificat utilisé.
- authority : Valeur du nom d'hôte transmise par le client (seul le SNI provenant d'une connexion TLS est pris en charge).
- crc32c : Somme de contrôle de l'en-tête PROXYv2.
- unique-id : Envoyer un identifiant unique généré à l'aide du format « unique-id-format » du frontal dans l'en-tête PROXYv2. Cet identifiant unique est principalement destiné à « mode tcp ». Il peut entraîner des résultats inattendus en « mode http », car l'identifiant unique généré est également utilisé pour la première requête HTTP au sein d'une connexion Keep-Alive.

<a id="entry-5-2-send-proxy-v2-ssl"></a>

**`send-proxy-v2-ssl`**

```haproxy
send-proxy-v2-ssl
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « send-proxy-v2-ssl » impose l'utilisation du protocole PROXY version 2 sur n'importe quelle connexion établie vers ce serveur. Le protocole PROXY informe l'autre extrémité des adresses couche 3/4 de la connexion entrante, afin qu'elle puisse déterminer l'adresse du client ou l'adresse publique utilisée, quel que soit le protocole de couche supérieure. En outre, l'extension d'information SSL du protocole PROXY est ajoutée à l'en-tête du protocole PROXY. Ce paramètre ne doit pas être utilisé si le serveur n'est pas conscient de cette version du protocole. Voir également l'option « no-send-proxy-v2-ssl » de cette section et l'option « send-proxy-v2 » de la commande « bind ».

<a id="entry-5-2-send-proxy-v2-ssl-cn"></a>

**`send-proxy-v2-ssl-cn`**

```haproxy
send-proxy-v2-ssl-cn
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « send-proxy-v2-ssl » impose l'utilisation du protocole PROXY version 2 sur n'importe quelle connexion établie vers ce serveur. Le protocole PROXY informe l'autre extrémité des adresses couche 3/4 de la connexion entrante, afin qu'elle puisse déterminer l'adresse du client ou l'adresse publique utilisée, quel que soit le protocole de couche supérieure. En outre, l'extension d'information SSL du protocole PROXY, ainsi que le nom commun issu de l'objet du certificat client (le cas échéant), sont ajoutés à l'en-tête du protocole PROXY. Ce paramètre ne doit pas être utilisé si le serveur n'est pas conscient de cette version du protocole. Voir également l'option « no-send-proxy-v2-ssl-cn » de cette section et l'option « send-proxy-v2 » du mot-clé « bind ».

<a id="entry-5-2-shard"></a>

**`shard <shard>`**

```haproxy
shard <shard>
```

Peut être utilisé dans les contextes suivants : pairs

Ce paramètre n'est utilisé que dans le contexte de la synchronisation des tables de persistance avec le protocole de pairs. Le paramètre « shard » identifie les pairs qui recevront toutes les mises à jour de la table de persistance pour les clés dont le hachage de distribution correspond à cette valeur de « shard ». Les valeurs acceptées vont de 0 à la valeur du paramètre « shards » spécifiée dans la section « peers ». La valeur 0 est la valeur par défaut, ce qui signifie que le pair recevra toutes les mises à jour des clés. Les valeurs supérieures à « shards » seront ignorées. C’est également le cas pour toute valeur fournie au pair local.

Exemple :

```haproxy
peers mypeers
     shards 3
     peer A 127.0.0.1:40001 # local peer without shard value (0 internally)
     peer B 127.0.0.1:40002 shard 1
     peer C 127.0.0.1:40003 shard 2
     peer D 127.0.0.1:40004 shard 3
```

<a id="entry-5-2-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré. Il définit la chaîne décrivant la liste des algorithmes de signature négociés pendant l'échange TLSv1.2 et TLSv1.3. Le format de la chaîne est défini dans « man 3 SSL_CTX_set1_sigalgs » des pages de documentation OpenSSL. Il est déconseillé d'utiliser ce paramètre sauf si une compatibilité avec un middlebox est requise.

<a id="entry-5-2-slowstart"></a>

**`slowstart <start_time_in_ms>`**

```haproxy
slowstart <start_time_in_ms>
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « slowstart » d'un serveur accepte une valeur en millisecondes indiquant après combien de temps un serveur revenu en service fonctionnera à pleine vitesse. Comme pour tout autre paramètre basé sur le temps, il peut être spécifié dans n'importe quelle autre unité explicite parmi { us, ms, s, m, h, d }. La vitesse augmente linéairement de 0 à 100 % durant cette période. Cette limitation s'applique à deux paramètres :

- maxconn : le nombre de connexions acceptées par le serveur passera de 1 à 100 % de la limite dynamique habituelle définie par (minconn, maxconn, fullconn).

- weight : lorsque le backend utilise un algorithme de pondération dynamique, le poids augmente linéairement de 1 à
  100 %. Dans ce cas, le poids est mis à jour à chaque contrôle d'état. Il est donc important
  que le paramètre « inter » soit inférieur au paramètre « slowstart », afin de maximiser le nombre d'étapes.

Le ralentissement initial n'est jamais appliqué au démarrage d'HAProxy, faute de quoi il pourrait perturber les serveurs en cours d'exécution. Il n'est appliqué qu'aux serveurs qui ont été précédemment identifiés comme défaillants.

<a id="entry-5-2-sni"></a>

**`sni <expression>`**

```haproxy
sni <expression>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Le paramètre « sni » évalue l'expression d'extraction d'échantillon, la convertit en chaîne de caractères et utilise le résultat comme nom d'hôte envoyé dans l'extension TLS SNI au serveur. Un cas d'utilisation typique consiste à transmettre le SNI reçu du client dans un scénario TCP/SSL en pont, en utilisant l'extraction d'échantillon "ssl_fc_sni" pour l'expression. CETTE UTILISATION NE DOIT PAS ÊTRE EMPLOYÉE POUR HTTPS, où req.hdr(host) doit être utilisé à la place, car le SNI dans HTTPS doit toujours correspondre au champ Host et les clients sont autorisés à utiliser des noms d'hôte différents sur la même connexion. Si « verify required » est défini (ce qui est le paramètre recommandé), le nom résultant sera également comparé aux noms du certificat serveur. Voir la directive « verify » pour plus de détails. Si vous souhaitez définir un SNI pour les contrôles d'état, consultez la directive « check-sni » pour plus de détails.

Par défaut, le SNI est affecté au nom de la connexion pour « http-reuse », sauf substitution par le mot-clé serveur « pool-conn-name ».

<a id="entry-5-2-sni-auto"></a>

**`sni-auto`**

```haproxy
sni-auto
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Le paramètre « sni-auto » active la sélection automatique du SNI, si aucune valeur n’a déjà été définie. Il définit l’expression « sni » sur « req.hdr(host),field(1,:) », ce qui signifie qu’un SNI sera présenté avec le nom d’hôte de la requête envoyée au serveur, en supprimant le numéro de port. Il est activé par défaut, mais ce paramètre peut être utilisé comme paramètre « server » pour réinitialiser toute configuration « no-sni-auto » héritée de la directive « default-server » en tant que valeur par défaut. Il peut également être utilisé comme paramètre « default-server » pour réinitialiser toute configuration précédente « default-server » « no-sni-auto ».

Pour les connexions HTTPS, le SNI sélectionné est déterminé par la valeur de l’en-tête hôte de la requête, le cas échéant.
Sinon, il reste non défini. Pour les autres protocoles, cette option est ignorée.

Si la sélection automatique du SNI est utilisée, la valeur est affectée au nom de la connexion pour « http-reuse », sauf substitution par le mot-clé serveur « pool-conn-name ».

Voir l'option « check-sni-auto » pour activer la sélection automatique du SNI pour les contrôles d'état SSL.

<a id="entry-5-2-source"></a>

**`source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<pl>[-<ph>]] [interface <name>] ...
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Le paramètre « source » définit l'adresse source utilisée lors de la connexion au serveur. Il suit les mêmes paramètres et principes que le mot-clé « source » du backend, à ceci près qu'il ne s'applique qu'au serveur qui le référence. Veuillez consulter le mot-clé « source » pour plus de détails.

En outre, l'instruction « source » sur une ligne de serveur permet de spécifier une plage de ports sources en indiquant les bornes inférieure et supérieure, séparées par un trait d'union ('-'). Certains systèmes d'exploitation peuvent exiger une adresse IP valide lorsqu'une plage de ports sources est spécifiée. Il est autorisé d'utiliser la même IP/plage pour plusieurs serveurs. Cette pratique permet de contourner la limite de 64k connexions simultanées au total. La limite s'élèvera alors à 64k connexions par serveur.

Depuis Linux 4.2/libc 2.23, IP_BIND_ADDRESS_NO_PORT est défini pour les connexions spécifiant l'adresse source sans port(s).

<a id="entry-5-2-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option active le chiffrement SSL sur les connexions sortantes vers le serveur. Il est essentiel de vérifier les certificats serveur en utilisant « verify » lors de la connexion SSL aux serveurs, faute de quoi la communication est vulnérable aux attaques de type « homme au milieu » simples, rendant le SSL inutile. Lorsque cette option est utilisée, les contrôles d'état sont automatiquement envoyés en SSL, sauf si une directive « port » ou « addr » indique que le contrôle doit être envoyé à une autre localisation. Consultez « no-ssl » pour désactiver l’option « ssl » et « check-ssl » pour forcer les contrôles d'état en SSL.

<a id="entry-5-2-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de `<version>` ou d'une version inférieure lorsque le protocole SSL est utilisé pour communiquer avec le serveur.
Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-min-ver ».

<a id="entry-5-2-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option impose l'utilisation de `<version>` ou d'une version supérieure lorsque le protocole SSL est utilisé pour communiquer avec le serveur.
Cette option est également disponible dans l'instruction globale « ssl-default-server-options ». Voir également « ssl-max-ver ».

<a id="entry-5-2-ssl-reuse"></a>

**`ssl-reuse`**

```haproxy
ssl-reuse
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée comme paramètre « server » pour réinitialiser tout paramètre « no-ssl-reuse » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée comme paramètre « default-server » pour réinitialiser tout paramètre précédent « default-server » « no-ssl-reuse ».

<a id="entry-5-2-stick"></a>

**`stick`**

```haproxy
stick
```

Peut être utilisé dans les contextes suivants : tcp, http

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « non-stick » hérité de la directive « default-server » en tant que valeur par défaut. Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « non-stick » précédent défini sur « default-server ».

<a id="entry-5-2-strict-maxconn"></a>

**`strict-maxconn`**

```haproxy
strict-maxconn
```

Peut être utilisé dans les contextes suivants : tcp, http

La directive maxconn aux serveurs est un peu trompeuse : elle configure en réalité le nombre maximal de requêtes envoyées à un serveur, mais, avec des connexions inactives, le nombre total de connexions vers le serveur peut être supérieur. Si une limite stricte du nombre de connexions vers un serveur est requise, la directive strict-maxconn peut être utilisée. Dans ce cas, nous n’établirons jamais plus de connexions vers un serveur qu’indiqué par maxconn, et nous tenterons de réutiliser ou de fermer des connexions si nécessaire. Veuillez noter toutefois qu’il peut en résulter des requêtes échouées si nous ne parvenons pas à établir une nouvelle connexion et qu’aucune connexion inactive n’est disponible. Cela peut survenir lorsque des connexions « privées » sont établies, c’est-à-dire des connexions liées uniquement à une session, car l’authentification a eu lieu.

<a id="entry-5-2-socks4"></a>

**`socks4 <addr>:<port>`**

```haproxy
socks4 <addr>:<port>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option active un tunnel SOCKS4 côté amont pour les connexions sortantes vers le serveur. L’utilisation de cette option ne force pas par défaut le contrôle d'état à passer par SOCKS4. Vous devrez utiliser le mot-clé « check-via-socks4 » pour l’activer.

<a id="entry-5-2-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Active la signature TCP MD5 (RFC 2385, protection des sessions BGP via l'option de signature TCP MD5) pour toutes les connexions sortantes vers ce serveur. Cette option n'est disponible que sous Linux. Lorsqu'elle est activée, la chaîne `<password>` est utilisée pour signer chaque segment TCP à l'aide d'un hachage de 16 octets MD5. Cela protège la connexion TCP contre les attaques par falsification. Le cas d'utilisation principal de cette option est de permettre à BGP de se protéger contre l'introduction de segments TCP falsifiés dans le flux de connexion. Elle peut toutefois être utile pour toute connexion TCP très longue.

<a id="entry-5-2-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Définit le délai d'expiration utilisateur TCP pour toutes les connexions sortantes vers ce serveur. Cette option est disponible sur Linux depuis la version 2.6.37. Elle permet à HAProxy de configurer un délai d'expiration pour les sockets contenant des données n'ayant pas reçu d'accusé de réception après le délai configuré. Cela est particulièrement utile pour les connexions longues en cours d'utilisation, comme les terminaux distants ou les pools de connexions vers une base de données, où les délais d'expiration du client et du serveur doivent rester élevés afin de permettre de longues périodes d'inactivité, mais où il est important de détecter qu'un serveur est devenu inaccessible afin de libérer toutes les ressources associées à sa connexion (et à la session du client). Un cas d'utilisation typique consiste également à forcer la fermeture des connexions vers un serveur défaillant lorsque les contrôles d'état sont trop lents ou lors d'un rechargement doux, puisque les contrôles d'état sont alors désactivés. L'argument est un délai exprimé en millisecondes par défaut. Cette option ne s'applique qu'aux connexions TCP régulières et est ignorée pour les autres protocoles.

<a id="entry-5-2-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option permet d'utiliser l'ouverture rapide TCP lors de la connexion aux serveurs, sur les systèmes qui la prennent en charge (actuellement uniquement le noyau Linux \>= 4.11). Consultez l'option bind « tfo » pour plus d'informations sur l'ouverture rapide TCP. Veuillez noter qu'en utilisant tfo, vous devez également utiliser les mots-clés « conn-failure », « empty-response » et « response-timeout » dans « retry-on », sinon HAProxy ne pourra pas réessayer la connexion en cas d'échec. Voir également « no-tfo ».

<a id="entry-5-2-track"></a>

**`track [<backend>/]<server>`**

```haproxy
track [<backend>/]<server>
```

Peut être utilisé dans les contextes suivants : tcp, http, log

Cette option permet de définir l'état actuel d'un serveur en suivant celui d'un autre. Il est possible de suivre un serveur qui suit à son tour un autre serveur, à condition qu'à la fin de la chaîne, un serveur ait les contrôles d'état activés. Si `<backend>` est omis, celui actuel est utilisé. Si disable-on-404 est utilisé, il doit être activé sur les deux proxies.

Exemple :

```text
backend A
server a1 1.1.1.1:80 track B/b1
server a2 1.1.1.2:80 track B/b1

backend B
server b1 2.2.2.2:80 check
```

<a id="entry-5-2-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Cette option peut être utilisée en tant que paramètre « server » pour réinitialiser tout paramètre « no-tls-tickets » hérité de la directive « default-server » en tant que valeur par défaut. Le mécanisme des tickets TLS n’est utilisé qu’avec TLS 1.2. La confidentialité persistante est compromise avec les tickets TLS, sauf si les clés de ticket sont régulièrement renouvelées (par rechargement ou en utilisant « tls-ticket-keys »). Elle peut également être utilisée en tant que paramètre « default-server » pour réinitialiser tout paramètre « no-tls-tickets » précédent défini sur « default-server ».

<a id="entry-5-2-verify"></a>

**`verify [none|required]`**

```haproxy
verify [none|required]
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support OpenSSL a été intégré. Si sa valeur est définie sur « none », la vérification du certificat du serveur est désactivée. Dans les autres cas, le certificat fourni par le serveur est vérifié à l’aide des autorités de certification (CA) provenant du fichier « ca-file » et des listes de révocation de certificats (CRL) optionnelles provenant du fichier « crl-file », après avoir vérifié que les noms présents dans les attributs subject et subjectAlternateNames du certificat correspondent soit au nom passé via la directive « sni », soit, si ce nom n’est pas fourni, au nom d’hôte statique passé via la directive « verifyhost ». Si aucun nom n’est trouvé, les noms du certificat sont ignorés. Pour cette raison, l’utilisation de « verifyhost » est essentielle en l’absence de SNI. En cas d’échec de la vérification, la négociation est interrompue. Il est essentiel de vérifier les certificats serveur lors de la connexion SSL aux serveurs, sinon la communication est vulnérable aux attaques de type « homme du milieu » simples, rendant le SSL totalement inutile. À moins que "ssl_server_verify" n’apparaisse dans la section globale, « verify » est défini par défaut sur « required ».

<a id="entry-5-2-verifyhost"></a>

**`verifyhost <hostname>`**

```haproxy
verifyhost <hostname>
```

Peut être utilisé dans les contextes suivants : tcp, http, log, peers, ring

Ce paramètre n'est disponible que si le support d'OpenSSL a été intégré, et n'a d'effet que si « verify required » est également spécifié. Cette directive définit un nom d'hôte statique par défaut utilisé pour vérifier le certificat du serveur lorsque le SNI n'a pas été utilisé pour établir la connexion. Si le SNI n'est pas utilisé, c'est la seule méthode permettant d'activer la vérification du nom d'hôte. Ce nom d'hôte statique, lorsqu'il est défini, est également utilisé pour les contrôles d'état si aucun SNI n'est fourni. Si aucun des noms d'hôte présents dans le certificat ne correspond au nom d'hôte spécifié, la négociation est interrompue. Les noms d'hôte présents dans le certificat fourni par le serveur peuvent inclure des caractères génériques. Voir également les options « verify », « sni » et « no-verifyhost ».

<a id="entry-5-2-weight"></a>

**`weight <weight>`**

```haproxy
weight <weight>
```

Peut être utilisé dans les contextes suivants : tcp, http

Le paramètre « weight » permet d’ajuster le poids d’un serveur par rapport aux autres serveurs. Tous les serveurs reçoivent une charge proportionnelle à leur poids par rapport à la somme de tous les poids, de sorte que plus le poids est élevé, plus la charge est importante. La valeur par défaut est 1, et la valeur maximale est 256. Une valeur de 0 signifie que le serveur ne participe pas à la répartition de charge, mais continue tout de même à accepter les connexions persistantes. Si ce paramètre est utilisé pour répartir la charge en fonction de la capacité du serveur, il est recommandé de choisir des valeurs pouvant à la fois augmenter et diminuer, par exemple entre 10 et 100, afin de laisser suffisamment de marge au-dessus et en dessous pour des ajustements ultérieurs.

<a id="entry-5-2-ws"></a>

**`ws { auto | h1 | h2 }`**

```haproxy
ws { auto | h1 | h2 }
```

Peut être utilisé dans les contextes suivants : http

Cette option permet de configurer le protocole utilisé lors du relais des flux WebSocket. Elle est particulièrement utile lors de l'utilisation d'un backend HTTP/2 ne prenant pas en charge les WebSocket H2 via la RFC8441.

Le mode par défaut est « auto ». Il réutilise le même protocole que celui principal. La seule différence intervient lors de l'utilisation d'ALPN : dans ce cas, il peut tenter de rétrograder l'ALPN à « http/1.1 » uniquement pour les flux WebSocket si l'ALPN serveur configuré le contient.

La valeur « h1 » est utilisée pour forcer HTTP/1.1 sur les flux websockets, via ALPN si ALPN SSL est activé pour le serveur. De même, « h2 » peut être utilisée pour forcer les websockets HTTP/2.0. Utilisez cette valeur avec précaution : le serveur doit prendre en charge la RFC8441, faute de quoi HAProxy signalera une erreur lors du relais des websockets.

Notez que NPN n'est pas pris en compte, car son utilisation a été dépréciée en faveur de l'extension ALPN.

Voir également « alpn » et « proto ».

## 5.3. Résolution d'adresse IP du serveur par DNS {#section-5-3}

HAProxy permet d'utiliser un nom d'hôte dans la ligne de serveur pour récupérer son adresse IP à l'aide de serveurs de noms.
Par défaut, HAProxy résout le nom lors de l'analyse du fichier de configuration, au démarrage, et met en cache le résultat pour la durée de vie du processus. Cette approche est insuffisante dans certains cas, par exemple sur Amazon, où l'adresse IP d'un serveur peut changer après un redémarrage, ou où une IP virtuelle ELB peut varier en fonction de la charge actuelle.

Ce chapitre décrit comment HAProxy peut être configuré pour effectuer la résolution du nom des serveurs en temps réel.

Quel que soit l'état de la résolution dynamique des noms de serveur au moment de l'exécution, HAProxy effectue par défaut la première résolution au démarrage, pendant l'analyse de la configuration, via libc, sauf si cette fonction est désactivée par le paramètre « init-addr ».

### 5.3.1. Vue d'ensemble {#section-5-3-1}

Comme nous l'avons vu dans l'introduction, la résolution de nom dans HAProxy s'effectue à deux étapes différentes du cycle de vie du processus :

```text
1. Au démarrage, HAProxy analyse la définition de la ligne server et y
   trouve un nom d'hôte. Il utilise les fonctions libc pour résoudre ce
   nom ; cette résolution repose sur le fichier /etc/resolv.conf.

2. Pendant l'exécution, HAProxy résout périodiquement les noms des
   serveurs nécessitant une résolution DNS.
```

Quelques autres événements peuvent déclencher une résolution de nom en temps d'exécution :

- quand un contrôle d'état d'un serveur aboutit à un délai d'expiration de connexion : cela peut être dû au fait que le serveur dispose d'une nouvelle adresse IP. Il est donc nécessaire de déclencher une résolution de nom afin de connaître cette nouvelle adresse.

Lors de l'utilisation de résolveurs, le nom de serveur peut être un nom d'hôte ou une étiquette SRV. HAProxy considère comme une étiquette SRV tout ce qui commence par un trait de soulignement. Si une étiquette SRV est spécifiée, les enregistrements SRV correspondants seront récupérés auprès du serveur DNS, et les noms d'hôte fournis seront utilisés. L'étiquette SRV sera vérifiée périodiquement, et si des serveurs sont ajoutés ou supprimés, HAProxy les mettra automatiquement à jour.

Quelques points importants à noter :

- tous les serveurs de noms sont interrogés en même temps. HAProxy traitera la première réponse valide.

- Une résolution est considérée comme invalide (NX, délai d'expiration, refusée), lorsque tous les serveurs renvoient une erreur.

- Le client DNS implémenté dans HAProxy est très basique et ne comprendra pas le grand nombre d'options ni les configurations avancées que le résolveur d'un système d'exploitation est capable de gérer. En conséquence, sauf dans des configurations très simples où un serveur connu par son nom complet (FQDN) ne possède qu'une seule adresse IP à la fois et peut éventuellement la renouveler (par exemple, après un redémarrage), il est fortement recommandé d'éviter de mélanger la résolution au moment de l'initialisation basée sur libc avec la résolution au runtime basée sur DNS, car de telles configurations sont connues pour entraîner des échecs lors du renouvellement d'adresse. En conclusion, sauf si vous savez exactement ce que vous faites, vous devez toujours exclure « libc » de « init-addr » lorsque vous utilisez « resolvers » dans une ligne de serveur.

### 5.3.2. La section resolvers {#section-5-3-2}

Cette section est dédiée aux informations d'hôte relatives à la résolution de noms dans HAProxy. Autant de sections resolvers que nécessaire peuvent être définies. Chaque section peut contenir plusieurs serveurs de noms.

Au démarrage, HAProxy tente de générer une section resolvers nommée « default », si aucune section n’a été nommée ainsi dans la configuration. Cette section est utilisée par défaut par httpclient et utilise le mot-clé parse-resolv-conf. Si HAProxy échoue à générer automatiquement cette section, aucune erreur ni avertissement n’est émis.

Lorsque plusieurs serveurs de noms sont configurés dans une section resolvers, HAProxy utilise la première réponse valide. En cas de réponses non valides, seule la dernière est prise en compte. L'objectif est de permettre à un serveur lent de fournir une réponse valide après un serveur rapide mais erroné ou périmé.

Lorsque chaque serveur retourne un type d'erreur différent, seule la dernière erreur est utilisée par HAProxy. Le traitement suivant est appliqué à cette erreur :

```text
1. HAProxy réessaie la même requête DNS avec un nouveau type : les
   requêtes A passent à AAAA, ou l'inverse. Les requêtes SRV ne sont pas
   concernées ; les erreurs de délai d'expiration sont aussi exclues.

2. Après le repli sur un autre type de requête (ou s'il ne s'applique pas),
   HAProxy réessaie la requête DNS originale avec le type préféré.

3. HAProxy réessaie les étapes précédentes <resolve_retries> fois.
   En l'absence de réponse valide, il arrête la résolution DNS et
   signale l'erreur.
```

Par exemple, avec 2 serveurs de noms configurés dans une section resolvers, les scénarios suivants sont possibles :

- La première réponse est valide et est appliquée directement, la deuxième réponse est ignorée

- La première réponse est invalide et la deuxième est valide, la deuxième réponse est donc appliquée

- La première réponse est un domaine NX et la deuxième une réponse tronquée, HAProxy réessaie alors la requête avec un nouveau type

- La première réponse est un domaine NX et la deuxième est un délai d'expiration, HAProxy réessaie alors la requête avec un nouveau type

- La requête a expiré pour les deux serveurs de noms, puis HAProxy la réessaie avec le même type de requête

Comme un serveur DNS ne peut pas répondre à toutes les adresses IP dans une seule requête, HAProxy conserve un cache des réponses précédentes ; une réponse est considérée comme obsolète après `<hold obsolete>` secondes sans retour d'adresse IP.

<a id="entry-5-3-2-resolvers"></a>

**`resolvers <resolvers id>`**

```haproxy
resolvers <resolvers id>
```

Crée une nouvelle liste de serveurs de noms étiquetée `<resolvers id>`. Comme indiqué ci-dessus, le nom spécial « default » existe toujours et est automatiquement créé s'il n'est pas déclaré explicitement ; il s'agit de la section sur laquelle s'appuient les services internes tels que httpclient. La déclaration d'une entrée « default » affecte la manière dont ces services effectuent la résolution de noms.

Une section resolvers accepte les paramètres suivants :

<a id="entry-5-3-2-accepted-payload-size"></a>

**`accepted_payload_size <nb>`**

```haproxy
accepted_payload_size <nb>
```

Définit la taille maximale du payload acceptée par HAProxy et annoncée à tous les serveurs de noms configurés dans cette section resolvers. `<nb>` est exprimé en octets. Si non définie, HAProxy annonce 512. (valeur minimale définie par le RFC 6891)

Note : la valeur maximale autorisée est 65535. La valeur recommandée pour UDP est 4096, et il n'est pas conseillé de dépasser 8192, sauf si vous êtes certain que votre système et votre réseau peuvent gérer cette charge (dépasser 65507 n’a pas de sens, étant donné que c’est la taille maximale du payload UDP). Si vous utilisez uniquement des serveurs DNS TCP pour gérer de grandes réponses DNS, vous devriez définir cette valeur à son maximum : 65535.

<a id="entry-5-3-2-nameserver"></a>

**`nameserver <name> <address>[:port] [param*]`**

```haproxy
nameserver <name> <address>[:port] [param*]
```

Utilisé pour configurer un serveur de noms. `<name>` du serveur de noms doit être unique. Par défaut, le `<address>` est considéré comme étant de type datagramme. Cela signifie qu’en l’absence de préfixe d’adresse spécifique (paragraphe 11.), si une adresse IPv4 ou IPv6 est configurée, le protocole UDP sera utilisé. Si un préfixe d’adresse de protocole de flux est utilisé, le serveur de noms sera considéré comme un serveur de flux (TCP par exemple), et les paramètres « server » mentionnés au paragraphe 5.2, qui sont pertinents pour la résolution DNS, seront pris en compte.
Note : actuellement, en mode TCP, 4 requêtes sont enfilées sur la même connexion. Un lot de connexions inactives est supprimé toutes les 5 secondes. La valeur « maxconn » peut être configurée pour limiter le nombre de connexions concurrentes, et TLS peut également être utilisé si le serveur le prend en charge.

<a id="entry-5-3-2-parse-resolv-conf"></a>

**`parse-resolv-conf`**

```haproxy
parse-resolv-conf
```

Ajoute tous les serveurs DNS trouvés dans /etc/resolv.conf à la liste des serveurs DNS de ce résolveur. L'ordre est équivalent à celui obtenu en plaçant individuellement chaque serveur DNS de /etc/resolv.conf dans la section resolvers à la place de cette directive.

<a id="entry-5-3-2-hold"></a>

**`hold <status> <period>`**

```haproxy
hold <status> <period>
```

Lors de la réception de la réponse DNS `<status>`, détermine si l'état d'un serveur doit passer de UP à DOWN. Pour prendre cette décision, il vérifie si une réponse d'état valide a été reçue au cours des `<period>` précédents afin de contrer l'état invalide récemment reçu.

    `<status>` : statut de la dernière résolution de nom.
           nx        Après avoir reçu un statut NXDOMAIN, vérifier s'il existe un statut valide pendant la période de conclusion.

           refused   Après avoir reçu un statut REFUSED, vérifier s'il existe un statut valide pendant la période de conclusion.

           timeout   Une fois que le « délai d'expiration de la tentative » a été atteint, vérifier s'il existe un statut valide pendant la période de conclusion.

           other     Après avoir reçu tout autre statut non valide, vérifier s'il existe un statut valide pendant la période de conclusion.

           valid     S'applique uniquement aux actions "http-request do-resolve" et
                     "tcp-request content do-resolve". Il définit la période pendant
                     laquelle le serveur maintiendra une réponse valide avant de déclencher
                     une nouvelle résolution. Il n'affecte pas la résolution dynamique des serveurs.

           obsolete  Définit la durée d'attente avant la suppression des enregistrements DNS obsolètes après la réception d'un enregistrement de réponse mis à jour. S'applique aux enregistrements SRV.

    `<period>` : Durée dans le passé pendant laquelle une réponse valide doit avoir été reçue. Le format suit celui de HAProxy et est exprimé en millisecondes par défaut.

Pour un serveur qui repose sur une résolution DNS dynamique pour déterminer son adresse IP, la réception d'une réponse DNS non valide, telle que NXDOMAIN, entraîne un changement d'état du serveur de UP à DOWN. Les directives hold définissent jusqu'où remonter dans le passé pour rechercher une réponse valide. Si une réponse valide a été reçue dans les `<period>`, l'état invalide récemment reçu sera ignoré.

À moins qu'une réponse valide n'ait été reçue pendant la période de clôture, le serveur sera marqué comme DOWN. Par exemple, si « hold nx 30s » est configuré et que la dernière réponse DNS reçue était NXDOMAIN, le serveur sera marqué comme DOWN à moins qu'une réponse valide n'ait été reçue au cours des 30 s précédentes.

Un serveur en état DOWN sera marqué comme UP dès la réception d'un statut valide provenant du serveur DNS.

Un comportement distinct existe pour « hold valid » et « hold obsolete ».

Valeur par défaut : 10 s pour « valid », 0 s pour « obsolete » et 30 s pour les autres.

<a id="entry-5-3-2-resolve-retries"></a>

**`resolve_retries <nb>`**

```haproxy
resolve_retries <nb>
```

Définit le nombre `<nb>` de requêtes à envoyer pour résoudre un nom de serveur avant d'abandonner. Valeur par défaut : 3

Une nouvelle tentative est effectuée en cas de délai d'expiration du serveur de noms ou lorsque la séquence complète de basculement des types de requête DNS est terminée et que nous devons recommencer à partir de la requête ANY par défaut.

<a id="entry-5-3-2-timeout"></a>

**`timeout <event> <time>`**

```haproxy
timeout <event> <time>
```

Définit les délais d'expiration liés à la résolution de noms `<event>` : l'événement auquel s'applique la période de délai d'expiration `<time>`. Les événements disponibles sont :   - resolve : délai par défaut pour déclencher la résolution de noms lorsque aucun autre délai n'est appliqué. Valeur par défaut : 1s   - retry : délai entre deux requêtes DNS, lorsque aucune réponse valide n'a été reçue. Valeur par défaut : 1s
`<time>` : délai lié à l'événement. Il suit le format de temps HAProxy. `<time>` est exprimé en millisecondes.

Exemple :

```text
resolvers mydns
  nameserver dns1 10.0.0.1:53
  nameserver dns2 10.0.0.2:53
  nameserver dns3 tcp@10.0.0.3:53
  parse-resolv-conf
  resolve_retries       3
  timeout resolve       1s
  timeout retry         1s
  hold other           30s
  hold refused         30s
  hold nx              30s
  hold timeout         30s
  hold valid           10s
  hold obsolete        30s
```
