---
title: "Commande serveur (server)"
linkTitle: "server"
weight: 120
description: "Référence des options et du comportement de la commande pgBackRest `server`."
icon: fa-solid fa-server
module: [PGBACKREST]
categories: [Référence]
upstream_link: "https://pgbackrest.org/command.html#command-server"
---

Le serveur pgBackRest permet d'accéder aux hôtes distants sans utiliser le protocole SSH.

## Options de commande {#command-options}

### Option d'adresse serveur TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

Adresse du serveur TLS.

Adresse IP sur laquelle le serveur écoute les requêtes clients.

```yaml
default: localhost
example: --tls-server-address=*
```

### Option Clients autorisés du serveur TLS (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

Clients autorisés du serveur TLS.

Les clients sont autorisés sur le serveur en vérifiant leur certificat et en comparant leur CN (Nom commun) au moyen d'une liste configurée sur le serveur via l'option `tls-server-auth`.

Un client CN peut être autorisé pour autant de stanzas que nécessaire en fournissant une liste séparée par des virgules à l'option `tls-server-auth` ou pour toutes les stanzas en spécifiant `tls-server-auth=client-cn=*`. Les caractères génériques ne peuvent pas être utilisés pour le CN du client.

```yaml
example: --tls-server-auth=client-cn=stanza1,stanza2
```

### Option Autorités de certification du serveur TLS (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

Autorités de certification du certificat serveur TLS.

Vérifie que les certificats client sont signés par une autorité de certification de confiance.

```yaml
example: --tls-server-ca-file=/path/to/server.ca
```

### Option de certificat serveur TLS (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

Fichier de certificat serveur TLS.

Envoyé au client pour indiquer l'identité du serveur.

```yaml
example: --tls-server-cert-file=/path/to/server.crt
```

### Option de clé de serveur TLS (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

Fichier de clé du serveur TLS.

Vérifie que le certificat serveur a été envoyé par son propriétaire.

```yaml
example: --tls-server-key-file=/path/to/server.key
```

### Option de port serveur TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

Port du serveur TLS.

Port sur lequel le serveur écoute les requêtes clients.

```yaml
default: 8432
allowed: [1, 65535]
example: --tls-server-port=8000
```

## Options générales {#general-options}

### Autoriser l'exécution en tant qu'utilisateur root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Permettre à la commande de s'exécuter en tant qu'utilisateur root.

Par défaut, seule la commande `restore` peut être exécutée en tant qu'utilisateur root, car elle est conçue pour gérer soigneusement les propriétés des fichiers. Exécuter d'autres commandes en tant que root risque de créer des fichiers (par exemple dans le dépôt) dont le propriétaire est root, rendant ces fichiers inaccessibles à l'utilisateur PostgreSQL, ce qui entraîne l'échec des commandes ultérieures.

Activez cette option pour exécuter une commande en tant qu'utilisateur root malgré tout. Toutefois, il est bien préférable d'exécuter pgBackRest en tant qu'utilisateur propriétaire du dépôt et du cluster PostgreSQL.

```yaml
default: n
example: --allow-root
```

### Option Taille tampon (`--buffer-size`) {#buffer-size-option---buffer-size}

Taille du tampon pour les opérations d'E/S.

Taille de tampon utilisée pour les opérations de copie, de compression, de chiffrement et autres. Le nombre de tampons utilisés dépend des options, et chaque opération peut utiliser une mémoire supplémentaire, par exemple, la compression `gz` peut utiliser jusqu'à 256KiB de mémoire supplémentaire.

Les valeurs autorisées sont `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` et `16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### Option de configuration (`--config`) {#config-option---config}

Fichier de configuration pgBackRest.

Utilisez cette option pour spécifier un fichier de configuration différent du fichier par défaut.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### Option Chemin d'inclusion de configuration (`--config-include-path`) {#config-include-path-option---config-include-path}

Chemin vers les fichiers de configuration supplémentaires de pgBackRest.

Les fichiers de configuration se trouvant dans l'emplacement spécifié et ayant l'extension `.conf` seront concaténés au fichier de configuration de pgBackRest, ce qui donne un seul fichier de configuration.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### Option de chemin de configuration (`--config-path`) {#config-path-option---config-path}

Chemin de base des fichiers de configuration de pgBackRest.

Ce paramètre est utilisé pour remplacer le chemin de base par défaut pour les options `--config` et `--config-include-path`, sauf si ces dernières sont explicitement définies en ligne de commande.

Par exemple, passer uniquement `--config-path=/conf/pgbackrest` fait que la valeur par défaut de `--config` est définie à `/conf/pgbackrest/pgbackrest.conf` et que la valeur par défaut de `--config-include-path` est définie à `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### Option d'expiration I/O (`--io-timeout`) {#io-timeout-option---io-timeout}

Délai d'attente d'E/S.

Délai d'attente, en secondes, utilisé pour les connexions et les opérations de lecture/écriture.

Notez que l'opération de lecture/écriture entière n'a pas besoin de se terminer dans ce délai d'attente, mais *une certaine* progression doit être réalisée, même si elle ne concerne qu'un seul octet.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Définir l'option de priorité du processus (`--priority`) {#set-process-priority-option---priority}

Définir la priorité du processus.

Définit la priorité (c’est-à-dire la valeur de niceness) accordée au processus par l’ordonnanceur du noyau. Les valeurs positives réduisent la priorité, tandis que les valeurs négatives l’augmentent. Dans la plupart des cas, les processus ne disposent pas des autorisations nécessaires pour augmenter leur priorité.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Option délai d'attente du protocole (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Délai d'attente du protocole.

Définit le délai d'attente, en secondes, durant lequel le processus local ou distant attend qu'un nouveau message soit reçu au niveau du protocole. Cela empêche les processus de rester bloqués indéfiniment en attente d'un message.

> **NOTE :** L'option `protocol-timeout` doit être supérieure à l'option `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### Option Keep Alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Activation du keep-alive.

Active les messages keep-alive sur les connexions socket.

```yaml
default: y
example: --no-sck-keep-alive
```

### Option de nombre de connexions Keep Alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Nombre de maintien de connexion.

Spécifie le nombre de messages TCP keep-alive pouvant être perdus avant que la connexion ne soit considérée comme inactive.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPCNT`.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### Option d'idle Keep Alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Délai d'inactivité pour le maintien de la connexion.

Spécifie la durée (en secondes) pendant laquelle aucune activité réseau ne se produit, après laquelle le système d'exploitation doit envoyer un message de maintien de connexion TCP.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPIDLE`.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### Option Intervalle Keep Alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Intervalle de temps pour le maintien de la connexion active.

Spécifie la durée (en secondes) après laquelle un message TCP keep-alive non reconnu doit être renvoyé.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPINTVL`.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### Suites de chiffrement TLSv1.2 Option (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Suites de chiffrement TLSv1.2 autorisées.

Toutes les connexions TLS entre le client pgBackRest et le serveur sont chiffrées. Par défaut, les connexions aux magasins d'objets (par exemple S3) sont également chiffrées.

> **NOTE :** Le niveau de sécurité minimal absolu pour toute connexion de transport est TLSv1.2.

Les suites de chiffrement acceptées peuvent être ajustées si nécessaire. L'exemple proposé constitue un choix raisonnable sauf si des exigences de sécurité spécifiques s'appliquent. Si non définies (valeur par défaut), la valeur par défaut de la bibliothèque OpenSSL sous-jacente s'applique.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Suites de chiffrement TLSv1.3 Option (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Suites de chiffrement TLSv1.3 autorisées.

Toutes les connexions TLS entre le client pgBackRest et le serveur sont chiffrées. Par défaut, les connexions aux magasins d'objets (par exemple S3) sont également chiffrées.

> **NOTE :** Le niveau de sécurité minimal absolu pour toute connexion de transport est TLSv1.2.

Les suites de chiffrement acceptées peuvent être ajustées si nécessaire. Si non définies (valeur par défaut), la valeur par défaut de la bibliothèque OpenSSL sous-jacente s'applique.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## Options de journalisation {#log-options}

### Niveau de journalisation de la console (`--log-level-console`) {#console-log-level-option---log-level-console}

Niveau de journalisation pour la console.

Les niveaux de journalisation suivants sont pris en charge :

- `off` - Aucune journalisation (non recommandé)
- `error` - Journaliser uniquement les erreurs
- `warn` - Journaliser les avertissements et les erreurs
- `info` - Journaliser les informations, les avertissements et les erreurs
- `detail` - Journaliser les détails, les informations, les avertissements et les erreurs
- `debug` - Journaliser le débogage, les détails, les informations, les avertissements et les erreurs
- `trace` - Journaliser les traces (débogage très détaillé), le débogage, les informations, les avertissements et les erreurs

```yaml
default: warn
example: --log-level-console=error
```

### Niveau de journalisation du fichier (`--log-level-file`) {#file-log-level-option---log-level-file}

Niveau de journalisation des fichiers.

Les niveaux de journalisation suivants sont pris en charge :

- `off` - Aucune journalisation (non recommandé)
- `error` - Journaliser uniquement les erreurs
- `warn` - Journaliser les avertissements et les erreurs
- `info` - Journaliser les informations, les avertissements et les erreurs
- `detail` - Journaliser les détails, les informations, les avertissements et les erreurs
- `debug` - Journaliser le débogage, les détails, les informations, les avertissements et les erreurs
- `trace` - Journaliser les traces (débogage très détaillé), le débogage, les informations, les avertissements et les erreurs

```yaml
default: info
example: --log-level-file=debug
```

### Niveau de journalisation des erreurs standard (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

Niveau de journalisation pour stderr.

Spécifie les niveaux de journalisation qui seront envoyés vers `stderr` plutôt que vers `stdout` (spécifié par `log-level-console`). L'horodatage et le processus ne seront pas envoyés vers `stderr`.

Les niveaux de journalisation suivants sont pris en charge :

- `off` - Aucune journalisation (non recommandé)
- `error` - Journaliser uniquement les erreurs
- `warn` - Journaliser les avertissements et les erreurs
- `info` - Journaliser les informations, les avertissements et les erreurs
- `detail` - Journaliser les détails, les informations, les avertissements et les erreurs
- `debug` - Journaliser le débogage, les détails, les informations, les avertissements et les erreurs
- `trace` - Journaliser les traces (débogage très détaillé), le débogage, les informations, les avertissements et les erreurs

```yaml
default: off
example: --log-level-stderr=error
```

### Option Chemin Journal (`--log-path`) {#log-path-option---log-path}

Chemin où les fichiers de journalisation sont stockés.

Le chemin de journalisation fournit un emplacement où pgBackRest peut stocker les fichiers de journalisation. Notez que si `log-level-file=off`, aucun chemin de journalisation n'est requis.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### Option de timestamp de journal (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activer les horodatages dans la journalisation.

Active l’horodatage dans la journalisation console et fichier. Cette option est désactivée dans des situations spéciales, telles que la génération de documentation.

```yaml
default: y
example: --no-log-timestamp
```
