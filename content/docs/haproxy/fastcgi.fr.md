---
title: "10. Applications FastCGI"
linkTitle: "10. FastCGI"
weight: 210
description: "Configuration, paramètres, exemples et limites d'une application FastCGI"
icon: fa-solid fa-bolt
module: [HAPROXY]
categories: [Référence]
aliases:
  - /haproxy/configuration/fastcgi/
  - /docs/haproxy/configuration/fastcgi/
  - /haproxy/fastcgi/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

HAProxy est capable d'envoyer des requêtes HTTP vers des applications FastCGI Responder. Cette fonctionnalité a été ajoutée à HAProxy 2.1. Pour cela, les serveurs doivent être configurés pour utiliser le protocole FastCGI (en utilisant le mot-clé « proto fcgi » dans la ligne du serveur) et une application FastCGI doit être configurée et utilisée par le backend gérant ces serveurs (en utilisant le mot-clé « use-fcgi-app » dans la section proxy). Plusieurs applications FastCGI peuvent être définies, mais une seule peut être utilisée à la fois par un backend.

HAProxy implémente toutes les fonctionnalités de la spécification FastCGI pour les applications Responder. En particulier, il est capable de multiplexer plusieurs requêtes sur une seule connexion.

## 10.1. Configuration {#section-10-1}



### 10.1.1. Section fcgi-app {#section-10-1-1}

<a id="entry-10-1-1-fcgi-app"></a>

**`fcgi-app <name>`**

```haproxy
fcgi-app <name>
```

Déclare une application FastCGI nommée `<name>`. Pour être valide, au moins la racine des documents doit être définie.

<a id="entry-10-1-1-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

Déclarer ou compléter une liste d'accès.

Voir le mot-clé « acl » dans la [section 4.2](/fr/docs/haproxy/proxies/#section-4-2) et la [section 7](/fr/docs/haproxy/acls-and-samples/) pour plus de détails sur l'utilisation des ACL. Les ACL définies pour une application FastCGI sont privées. Elles ne peuvent pas être utilisées par toute autre application ou par tout proxy. De la même manière, les ACL définies dans toute autre section ne sont pas utilisables par une application FastCGI. Toutefois, des ACL prédéfinies sont disponibles.

<a id="entry-10-1-1-docroot"></a>

**`docroot <path>`**

```haproxy
docroot <path>
```

Définir la racine des documents sur l'hôte distant. `<path>` sera utilisé pour construire la valeur par défaut des paramètres FastCGI SCRIPT_FILENAME et PATH_TRANSLATED. Il s'agit d'un paramètre obligatoire.

<a id="entry-10-1-1-index"></a>

**`index <script-name>`**

```haproxy
index <script-name>
```

Définir le nom du script qui sera ajouté après une URI se terminant par une barre oblique ("/") pour définir la valeur par défaut du paramètre FastCGI SCRIPT_NAME. Il s'agit d'un paramètre facultatif.

Exemple :

```text
index index.php
```

<a id="entry-10-1-1-log-stderr-global"></a>

**`log-stderr global`**

```haproxy
log-stderr global
log-stderr <target> [len <length>] [format <format>]
    [sample <ranges>:<sample_size>] <facility> [<level> [<minlevel>]]
```

Activez la journalisation des messages STDERR émis par l'application FastCGI.

Voir le mot-clé « log » dans la section [4.2](/fr/docs/haproxy/proxies/#section-4-2) pour plus de détails. Il s'agit d'un paramètre facultatif. Par défaut, les messages STDERR sont ignorés.

<a id="entry-10-1-1-pass-header"></a>

**`pass-header <name> [ { if | unless } <condition> ]`**

```haproxy
pass-header <name> [ { if | unless } <condition> ]
```

Spécifiez le nom d'un en-tête de requête qui sera transmis à l'application FastCGI. Il peut éventuellement être suivi d'une condition basée sur une ACL, auquel cas il ne sera évalué que si la condition est vraie.

La plupart des en-têtes de requête sont déjà accessibles à l'application FastCGI, préfixés par "HTTP\_". Cette directive n'est donc nécessaire que pour transmettre les en-têtes qui sont volontairement omis. Actuellement, les en-têtes « Authorization », « Proxy-Authorization » et les en-têtes hop-by-hop sont omis.

Notez que les en-têtes « Content-type » et « Content-length » ne sont jamais transmis à l'application FastCGI, car ils sont déjà convertis en paramètres.

<a id="entry-10-1-1-path-info"></a>

**`path-info <regex>`**

```haproxy
path-info <regex>
```

Définir une expression régulière pour extraire le nom du script et le chemin d'information à partir du chemin décodé URL.
Ainsi, `<regex>` peut avoir deux captures : la première pour capturer le nom du script et la deuxième pour capturer le chemin d'information. La première est obligatoire, la deuxième est facultative. Cette approche permet d'extraire le nom du script à partir du chemin en ignorant le chemin d'information. Il s'agit d'un paramètre facultatif.
Si ce paramètre n'est pas défini, aucune correspondance n'est effectuée sur le chemin, et les paramètres FastCGI PATH_INFO et PATH_TRANSLATED ne sont pas renseignés.

Pour des raisons de sécurité, lorsque cette expression régulière est définie, les caractères de saut de ligne et le caractère nul sont interdits dans le chemin, une fois décodé depuis l'URL. La raison de cette limitation est que, sinon, la correspondance échouerait toujours (en raison d'une limitation dans la manière dont les expressions régulières sont exécutées dans HAProxy). Ainsi, si l'un de ces deux caractères est détecté dans le chemin décodé depuis l'URL, une erreur est renvoyée au client. Le principe de moindre étonnement s'applique ici.

Exemple :

```text
path-info ^(/.+\.php)(/.*)?$ # both script-name and path-info may be set
path-info ^(/.+\.php)        # the path-info is ignored
```

<a id="entry-10-1-1-option-get-values"></a>

**`option get-values`**

```haproxy
option get-values
no option get-values
```

Active ou désactive la récupération des variables relatives à la gestion des connexions.

HAProxy est capable d'envoyer l'enregistrement FCGI_GET_VALUES à l'établissement de la connexion afin de récupérer la valeur des variables suivantes :

    * FCGI_MAX_REQS     Nombre maximal de requêtes simultanées que cette application acceptera.

    * FCGI_MPXS_CONNS   « 0 » si cette application ne multiplexe pas les connexions,
                        « 1 » dans le cas contraire.

Certaines applications FastCGI ne prennent pas en charge cette fonctionnalité. D'autres ferment la connexion immédiatement après avoir envoyé leur réponse. Par conséquent, cette option est désactivée par défaut.

Notez que le nombre maximal de requêtes simultanées acceptées par une application FastCGI est une variable de connexion. Elle limite uniquement le nombre de flux par connexion. Si la charge globale doit être limitée sur l'application, les paramètres serveur « maxconn » et « pool-max-conn » doivent être configurés. En outre, si une application ne prend pas en charge la multiplexion de connexions, le nombre maximal de requêtes simultanées est automatiquement fixé à 1.

<a id="entry-10-1-1-option-keep-conn"></a>

**`option keep-conn`**

```haproxy
option keep-conn
no option keep-conn
```

Indiquez à l'application FastCGI de maintenir la connexion ouverte ou non après l'envoi d'une réponse.

Si cette option est désactivée, l'application FastCGI ferme la connexion après avoir répondu à cette requête. Par défaut, cette option est activée.

<a id="entry-10-1-1-option-max-reqs"></a>

**`option max-reqs <reqs>`**

```haproxy
option max-reqs <reqs>
```

Définir le nombre maximum de requêtes simultanées que cette application acceptera.

Cette option peut être remplacée si la variable FCGI_MAX_REQS est récupérée lors de l'établissement de la connexion. En outre, si l'application ne prend pas en charge le multiplexage des connexions, cette option sera ignorée. Valeur par défaut : 1.

<a id="entry-10-1-1-option-mpxs-conns"></a>

**`option mpxs-conns`**

```haproxy
option mpxs-conns
no option mpxs-conns
```

Active ou désactive la prise en charge du multiplexage de connexions.

Cette option peut être remplacée si la variable FCGI_MPXS_CONNS est récupérée lors de l'établissement de la connexion. Elle est désactivée par défaut.

<a id="entry-10-1-1-set-param"></a>

**`set-param <name> <fmt> [ { if | unless } <condition> ]`**

```haproxy
set-param <name> <fmt> [ { if | unless } <condition> ]
```

Définissez un paramètre FastCGI qui doit être transmis à cette application. Sa valeur, définie par `<fmt>`, doit respecter les règles du format de journalisation personnalisé (voir la section [8.2.6](/fr/docs/haproxy/configuration-logging/#section-8-2-6) « Format de journalisation personnalisé »). Elle peut éventuellement être suivie d'une condition basée sur une ACL, auquel cas elle ne sera évaluée que si la condition est vraie.

Avec cette directive, il est possible de remplacer la valeur des paramètres FastCGI par défaut. Si la valeur est évaluée à une chaîne vide, la règle est ignorée. Ces directives sont évaluées dans l'ordre de leur déclaration.

Exemple :

```shell
# PHP only, required if PHP was built with --enable-force-cgi-redirect
set-param REDIRECT_STATUS 200

set-param PHP_AUTH_DIGEST %[req.hdr(Authorization)]
```

### 10.1.2. Section proxy {#section-10-1-2}

use-fcgi-app `<name>` Définir l'application FastCGI à utiliser pour le backend.

Arguments :

```text
<name>    est le nom de l'application FastCGI à utiliser.
```

Ce mot-clé n'est disponible que pour les proxies HTTP disposant de la capacité backend et comportant au moins un serveur FastCGI. Toutefois, les serveurs FastCGI peuvent être combinés avec des serveurs HTTP. Mais, sauf si une bonne raison s'impose, cette configuration n'est pas recommandée (voir [section 10.3](/fr/docs/haproxy/fastcgi/#section-10-3) pour les détails sur les limitations). Une seule application peut être définie à la fois par backend.

Notez qu'une fois une application FastCGI référencée pour un backend, selon la configuration, un traitement peut être effectué même si la requête n'est pas envoyée à un serveur FastCGI. Les règles permettant de définir des paramètres ou de transmettre des en-têtes à une application sont évaluées.

### 10.1.3. Exemple {#section-10-1-3}

```haproxy
frontend front-http
    mode http
    bind *:80

    use_backend back-dynamic if { path_reg ^/.+\.php(/.*)?$ }
    default_backend back-static

backend back-static
    mode http
    server www A.B.C.D:80

backend back-dynamic
    mode http
    use-fcgi-app php-fpm
    server php-fpm A.B.C.D:9000 proto fcgi

fcgi-app php-fpm
    log-stderr global
    option keep-conn

    docroot /var/www/my-app
    index index.php
    path-info ^(/.+\.php)(/.*)?$
```

## 10.2. Paramètres par défaut {#section-10-2}

Une application Responder FastCGI a le même objectif qu'un programme CGI/1.1. Selon la spécification CGI/1.1 (RFC3875), plusieurs variables doivent être transmises au script. HAProxy les définit donc, ainsi que d'autres variables couramment utilisées par les applications FastCGI. Toutes ces variables peuvent être surchargées, avec prudence toutefois.

```text
  +-------------------+-----------------------------------------------------+
  | AUTH_TYPE         | Indique le mécanisme éventuellement utilisé par     |
  |                   | HAProxy pour authentifier l'utilisateur. Seul le    |
  |                   | mécanisme d'authentification BASIC est pris en      |
  |                   | charge.                                             |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_LENGTH    | Contient la taille du corps du message joint à la   |
  |                   | requête. Seules les requêtes de taille connue sont  |
  |                   | donc considérées comme valides et envoyées à        |
  |                   | l'application.                                      |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_TYPE      | Contient le type du corps du message joint à la     |
  |                   | requête. Ce paramètre peut ne pas être défini.      |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | DOCUMENT_ROOT     | Contient la racine des documents sur l'hôte distant |
  |                   | sous laquelle le script doit être exécuté, définie  |
  |                   | dans la configuration de l'application.             |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | GATEWAY_INTERFACE | Contient le dialecte CGI utilisé par HAProxy pour   |
  |                   | communiquer avec l'application FastCGI. Sa valeur   |
  |                   | est "CGI/1.1".                                      |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_INFO         | Contient la portion de la hiérarchie du chemin URI  |
  |                   | qui suit la partie identifiant le script lui-même.  |
  |                   | La directive "path-info" doit être définie pour que |
  |                   | ce paramètre soit renseigné.                        |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_TRANSLATED   | Si PATH_INFO est défini, contient sa version        |
  |                   | traduite : la concaténation de DOCUMENT_ROOT et     |
  |                   | PATH_INFO. Si PATH_INFO n'est pas défini, ce        |
  |                   | paramètre ne l'est pas non plus.                    |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | QUERY_STRING      | Contient la chaîne de requête de la requête. Ce     |
  |                   | paramètre peut ne pas être défini.                  |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_ADDR       | Contient l'adresse réseau du client envoyant la     |
  |                   | requête.                                            |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_USER       | Contient la chaîne d'identification de              |
  |                   | l'utilisateur fournie par le client lors de son     |
  |                   | authentification.                                   |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_METHOD    | Contient la méthode que le script doit utiliser     |
  |                   | pour traiter la requête.                            |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_URI       | Contient l'URI de la requête.                       |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_FILENAME   | Contient le chemin absolu du script : la            |
  |                   | concaténation de DOCUMENT_ROOT et SCRIPT_NAME.      |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_NAME       | Contient le nom du script. Si la directive          |
  |                   | "path-info" est définie, il s'agit de la première   |
  |                   | partie de la hiérarchie du chemin URI, se terminant |
  |                   | par le nom du script. Sinon, il s'agit du chemin    |
  |                   | URI complet.                                        |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_NAME       | Contient le nom d'hôte du serveur auquel la requête |
  |                   | client est adressée : la valeur de l'en-tête "Host" |
  |                   | s'il est défini, sinon l'adresse de destination de  |
  |                   | la connexion côté client.                           |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PORT       | Contient le port TCP de destination de la connexion |
  |                   | côté client, c'est-à-dire le port auquel le client  |
  |                   | s'est connecté.                                     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PROTOCOL   | Contient le protocole de la requête.                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_SOFTWARE   | Contient la chaîne "HAProxy" suivie de la version   |
  |                   | actuelle de HAProxy.                                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | HTTPS             | Prend une valeur non vide ("on") si le script a été |
  |                   | interrogé via le protocole HTTPS.                   |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
```

## 10.3. Limitations {#section-10-3}

L’implémentation actuelle présente certaines limitations. La première concerne la manière dont certains en-têtes de requête sont masqués aux applications FastCGI. Ce masquage a lieu lors de l’analyse des en-têtes, du côté du backend, avant l’établissement de la connexion. À ce stade, HAProxy sait que le backend utilise une application FastCGI, mais il ne sait pas si la requête sera acheminée vers un serveur FastCGI ou non. Pour masquer les en-têtes de requête, il les supprime simplement du message HTX. Ainsi, si la requête est finalement acheminée vers un serveur HTTP, celui-ci ne les verra jamais. Pour cette raison, il est déconseillé de mixer des serveurs FastCGI et des serveurs HTTP sous le même backend.

De même, les règles « set-param » et « pass-header » sont évaluées lors de l'analyse des en-têtes de requête. L'évaluation est donc toujours effectuée, même si la requête est finalement acheminée vers un serveur HTTP.

À propos des règles « set-param », lorsqu'une règle est appliquée, un pseudo-en-tête est ajouté au message HTX.
Ainsi, de la même manière que pour les réécritures d'en-têtes HTTP, cela peut échouer si la mémoire tampon est pleine. Les règles
« set-param » peuvent entrer en concurrence avec les règles « http-request ».

Enfin, tous les paramètres FastCGI et les en-têtes HTTP sont envoyés dans un enregistrement unique FCGI_PARAM. Le codage de cet enregistrement doit être effectué en une seule passe, faute de quoi une erreur de traitement est renvoyée. Cela signifie que l’enregistrement FCGI_PARAM, une fois encodé, ne doit pas dépasser la taille d’un tampon. Toutefois, aucune réserve n’est à respecter ici.
