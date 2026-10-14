---
title: "Commande de listage du contenu du dépôt (repo-ls)"
linkTitle: "repo-ls"
weight: 100
description: "Référence des options et du comportement de la commande pgBackRest `repo-ls`."
icon: fa-solid fa-list
module: [PGBACKREST]
categories: [Référence]
upstream_link: "https://pgbackrest.org/command.html#command-repo-ls"
---

Similaire à la commande unix `ls` mais fonctionne sur tout type de dépôt pris en charge. Cette commande accepte un chemin, absolu ou relatif par rapport au chemin du dépôt défini par l'option `--repo-path`, et est principalement destinée à l'administration, l'investigation et les tests. Elle n'est pas obligatoire dans une configuration pgBackRest normale.

La sortie texte par défaut affiche un nom de fichier par ligne. La sortie JSON est disponible en spécifiant `--output=json`.

Si plusieurs dépôts sont configurés, la commande utilise par défaut le dépôt de priorité la plus élevée (par exemple `repo1`) sauf si l'option `--repo` est spécifiée.

## Options de commande {#command-options}

### Option de filtrage de sortie (`--filter`) {#filter-output-option---filter}

Filtrer la sortie avec une expression régulière.

Le filtre est appliqué aux noms de fichier/chemin avant leur sortie.

```yaml
example: --filter="(F|D|I)$"
```

### Option de sortie (`--output`) {#output-option---output}

Format de sortie.

Les types de sortie suivants sont pris en charge :

- `text` - Liste simple contenant un nom de fichier/lien/chemin par ligne.
- `json` - Informations détaillées sur les fichiers/liens/chemins au format JSON.

Au format JSON, les champs disponibles sont :

- `name` - nom de fichier/lien/chemin (et chemin partiel en cas de récursion).
- `type` - `file`, `path` ou `link`.
- `size` - taille en octets (fichiers uniquement).
- `time` - horodatage de dernière modification (fichiers uniquement).
- `destination` - destination du lien (liens uniquement).

```yaml
default: text
example: --output=json
```

### Option parcours des sous-répertoires (`--recurse`) {#recurse-subpaths-option---recurse}

Inclure tous les sous-chemins dans la sortie.

Tous les sous-chemins et leurs fichiers seront inclus dans la sortie.

```yaml
default: n
example: --recurse
```

### Option de tri de la sortie (`--sort`) {#sort-output-option---sort}

Trier la sortie par ordre croissant, décroissant ou aucun.

Les types de tri suivants sont pris en charge :

- `asc` - tri croissant.
- `desc` - tri décroissant.
- `none` - pas de tri.

```yaml
default: asc
example: --sort=desc
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

### Option de commande client SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Commande cliente SSH.

Utilisez une commande cliente SSH spécifique lorsque vous souhaitez utiliser une alternative ou que la commande `ssh` n'est pas disponible dans $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Option niveau de compression réseau (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Niveau de compression du réseau.

Définit le niveau de compression réseau lorsque `compress-type=none` et que la commande n'est pas exécutée sur le même hôte que le dépôt. La compression est utilisée pour réduire le trafic réseau. Lorsque `compress-type` est différent de `none`, le paramètre `compress-level-network` est ignoré et `compress-level` est utilisé à la place, afin que le fichier ne soit compressé qu'une seule fois.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
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

### Option de masque neutre (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Utilisez un umask neutre.

Définit le umask à 0000 afin que les modes du dépôt soient créés de manière cohérente. Le mode par défaut du répertoire est 0750 et le mode par défaut du fichier est 0640.

Pour utiliser le umask de l'utilisateur en cours, spécifiez `neutral-umask=n` dans le fichier de configuration ou `--no-neutral-umask` en ligne de commande.

```yaml
default: y
example: --no-neutral-umask
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

### Option de journalisation des sous-processus (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Activer la journalisation dans les sous-processus.

Activez la journalisation des fichiers pour tout sous-processus créé par ce processus, en utilisant le niveau de journalisation spécifié par `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### Option de timestamp de journal (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activer les horodatages dans la journalisation.

Active l’horodatage dans la journalisation console et fichier. Cette option est désactivée dans des situations spéciales, telles que la génération de documentation.

```yaml
default: y
example: --no-log-timestamp
```

## Options du dépôt {#repository-options}

### Définir l'option dépôt (`--repo`) {#set-repository-option---repo}

Définir le dépôt.

Spécifiez le dépôt sur lequel une commande doit s'opérer.

Par exemple, cette option peut être utilisée pour effectuer une restauration à partir d’un dépôt spécifique, plutôt que de laisser pgBackRest choisir.

```yaml
allowed: [1, 256]
example: --repo=1
```

### Option de conteneur de dépôt Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Conteneur de dépôt Azure.

Conteneur Azure utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés dans la racine du conteneur en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par Azure dans le conteneur.

```yaml
example: --repo1-azure-container=pg-backup
```

### Type de clé du dépôt Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Type de clé du dépôt Azure.

Les types suivants sont pris en charge pour l'autorisation :

- `shared` - Clé partagée
- `sas` - Signature d'accès partagé
- `auto` - Autorisation automatique à l'aide d'identités managées Azure

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### Option de style d'URI de dépôt Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Style URI Azure.

Les styles d'URI suivants sont pris en charge :

- `host` - Se connecter à l'hôte `account.endpoint`.
- `path` - Se connecter à l'hôte `endpoint` et préfixer le compte aux URI.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### Type de chiffrement du dépôt (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Chiffrement utilisé pour chiffrer le dépôt.

Les types de chiffrement suivants sont pris en charge :

- `none` - Le dépôt n'est pas chiffré
- `aes-256-cbc` - Advanced Encryption Standard avec une longueur de clé de 256 bits

Notez que le chiffrement est toujours effectué côté client, même si le type de dépôt (par exemple S3) prend en charge le chiffrement.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### Option de bac de dépôt GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Bucket du dépôt GCS.

Bucket GCS utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés à la racine du bucket en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par GCS dans le bucket.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### Option de point de terminaison du dépôt GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Point de terminaison du dépôt GCS.

Point d'accès utilisé pour se connecter au service de stockage. Peut être mis à jour pour utiliser un serveur local GCS ou un point d'accès alternatif.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### Type de clé du dépôt GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Type de clé du dépôt GCS.

Les types suivants sont pris en charge pour l'autorisation :

- `auto` - Autoriser à l'aide du compte de service de l'instance.
- `service` - Compte de service à partir d'une clé stockée localement.
- `token` - À utiliser pour les tests locaux, par exemple `fakegcs`.

Lorsque `repo-gcs-key-type=service`, les identifiants seront rechargés lorsque le jeton d'authentification sera renouvelé.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### Option ID du projet du dépôt GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

Identifiant du projet GCS.

ID du projet GCS utilisé pour déterminer la facturation des requêtes.

```yaml
example: --repo1-gcs-user-project=my-project
```

### Option hôte du dépôt (`--repo-host`) {#repository-host-option---repo-host}

Hôte du dépôt lors de l'opération à distance.

Lors de la sauvegarde et de l'archivage vers un système de fichiers monté localement, ce paramètre n'est pas requis.

```yaml
example: --repo1-host=repo1.domain.com
```

Nom obsolète : backup-host

### Option du fichier de l'autorité de certification hôte du dépôt (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Fichier de l'autorité de certification du serveur de dépôt.

Utilisez un fichier CA autre que celui par défaut du système pour vous connecter à l'hôte du dépôt.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option Chemin de l'autorité de certification du dépôt (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Chemin de l'autorité de certification du serveur de dépôt.

Utilisez un chemin de certificat d'autorité (CA) autre que celui par défaut du système pour établir la connexion avec l'hôte du dépôt.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### Option de fichier de certificat d'hôte du dépôt (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Fichier de certificat d'hôte du dépôt.

Envoyé à l'hôte du dépôt pour prouver l'identité du client.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### Option de commande hôte du dépôt (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

Commande pgBackRest de l'hôte du dépôt.

Requis uniquement si le chemin vers la commande pgBackRest est différent sur les hôtes local et de dépôt. Si non défini, la commande de dépôt sera définie de la même manière que celle de l'hôte local.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nom obsolète : backup-cmd

### Option de configuration de l'hôte du dépôt (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

Fichier de configuration du serveur de dépôt pgBackRest.

Spécifie l'emplacement du fichier de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le fichier de configuration de l'hôte du dépôt se trouve dans un emplacement différent du fichier de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nom obsolète : backup-config

### Option de chemin d'inclusion de configuration d'hôte de dépôt (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Chemin d'inclusion de configuration de l'hôte du dépôt pgBackRest.

Définit l'emplacement du chemin d'inclusion de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le chemin d'inclusion de configuration de l'hôte du dépôt est différent du chemin d'inclusion de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Chemin de configuration de l'hôte du dépôt (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

Chemin de configuration du serveur de dépôt pgBackRest.

Définit l'emplacement du chemin de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le chemin de configuration de l'hôte du dépôt est différent du chemin de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### Option de fichier de clé hôte du dépôt (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Fichier de clé hôte du dépôt.

Vérifie que le certificat client a été envoyé par le propriétaire.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### Option de port hôte du dépôt (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Port de l'hôte du dépôt lorsque `repo-host` est défini.

Utilisez cette option pour spécifier un port non par défaut pour le protocole du serveur du dépôt.

> **NOTE :** Lorsque `repo-host-type=ssh`, il n'existe pas de valeur par défaut pour `repo-host-port`. Dans ce cas, le port sera celui configuré pour la commande spécifiée par `cmd-ssh`.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

Nom obsolète : backup-ssh-port

### Type de protocole d'hôte de dépôt (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Type de protocole d'hôte de dépôt.

Les types de protocole suivants sont pris en charge :

- `ssh` - Shell sécurisé.
- `tls` - Serveur TLS pgBackRest.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### Option d'utilisateur hôte de dépôt (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Utilisateur hôte du dépôt lorsque `repo-host` est défini.

Définit l'utilisateur utilisé pour les opérations sur l'hôte du dépôt. Il est préférable que ce ne soit pas l'utilisateur `postgres`, mais plutôt un autre utilisateur tel que `pgbackrest`. Si PostgreSQL s'exécute sur l'hôte du dépôt, l'utilisateur `postgres` peut être ajouté au groupe `pgbackrest` afin d'avoir des permissions de lecture sur le dépôt sans pouvoir accidentellement le modifier.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

Nom obsolète : backup-user

### Option Chemin du dépôt (`--repo-path`) {#repository-path-option---repo-path}

Chemin où les sauvegardes et l'archive sont stockées.

Le dépôt est l'emplacement où pgBackRest stocke les sauvegardes et les archives des segments WAL.

Il peut être difficile de prévoir à l’avance l’espace nécessaire. La meilleure approche consiste à effectuer quelques sauvegardes, puis à noter la taille des différents types de sauvegardes (pleines, incrémentielles, différentielles) et à mesurer la quantité de WAL générée par jour. Cela vous donnera une idée générale de l’espace requis, bien que les besoins évoluent probablement au fil du temps avec l’évolution de votre base de données.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### Option de bac de dépôt S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

Bucket du dépôt S3.

Bucket S3 utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés à la racine du bucket en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par AWS dans le bucket.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### Option de point de terminaison du dépôt S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

Point de terminaison du dépôt S3.

Le point de terminaison AWS doit être valide pour la région sélectionnée.

Pour les configurations personnalisées ou les tests, les options `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, et `repo-storage-verify-tls` peuvent être utiles.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### Type de clé du dépôt S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

Type de clé pour le dépôt S3.

Les types suivants sont pris en charge :

- `shared` - Clés partagées
- `auto` - Récupérer automatiquement les identifiants temporaires
- `web-id` - Récupérer automatiquement les identifiants d'identité web
- `pod-id` - Récupérer automatiquement les identifiants d'identité de pod EKS
- `process` - Récupérer les identifiants en exécutant un processus

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### Option ID de clé KMS pour dépôt S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

Clé KMS du dépôt S3.

Active le chiffrement côté serveur S3 en utilisant la clé du service de gestion des clés AWS spécifiée.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option de commande du processus d'authentification S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Commande du processus d'authentification S3.

Commande (et arguments facultatifs) à exécuter pour récupérer les identifiants temporaires S3. Le premier élément de la liste est la commande, les éléments suivants sont passés en tant que paramètres.

Le processus doit produire un JSON contenant les champs `AccessKeyId`, `SecretAccessKey`, `SessionToken` et `Expiration`. Les identifiants seront automatiquement actualisés avant l'expiration. Voir [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) pour les détails du format.

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### Option de région du dépôt S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

Région du dépôt S3.

La région AWS où le bucket a été créé.

```yaml
example: --repo1-s3-region=us-east-1
```

### Option Requesteur Payant pour le dépôt S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Paiement par le demandeur pour le dépôt S3.

Active le paiement par le demandeur S3.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### Option de rôle du dépôt S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

Rôle du dépôt S3.

Le nom du rôle AWS (pas le nom ARN complet) utilisé pour récupérer les identifiants temporaires lorsque `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### Option de service de dépôt S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

Service de signature S3.

Le service de signature S3 utilisé dans l'authentification SigV4. La valeur par défaut est `s3` pour les points d'accès S3 standards. À définir sur `s3-outposts` lors de l'utilisation d'un point d'accès S3 Outposts.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### Option de point de terminaison STS du dépôt S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

Point de terminaison STS du dépôt S3.

Point de terminaison STS utilisé pour récupérer des identifiants temporaires lorsque `repo-s3-key-type=web-id` est configuré. Définissez-le sur un point de terminaison régional (par exemple `sts.us-east-1.amazonaws.com`) pour utiliser STS régional, ce qui peut être nécessaire pour les régions GovCloud, Chine, ou pour réduire la latence.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Option de style d'URI de dépôt S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

Style d'URI S3.

Les styles d'URI suivants sont pris en charge :

- `host` - Se connecter à l'hôte `bucket.endpoint`.
- `path` - Se connecter à l'hôte `endpoint` et préfixer les URI par le bucket.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### Option hôte du dépôt SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

Hôte du dépôt SFTP.

Hôte SFTP contenant le dépôt.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### Fingerprint de l'hôte du dépôt SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Empreinte du serveur hôte du dépôt SFTP.

La génération de l'empreinte d'hôte du dépôt SFTP doit correspondre à `repo-sftp-host-key-hash-type`. Générez l'empreinte via `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. Les clés d'hôte SSH se trouvent normalement dans le répertoire `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Type d'option de vérification de la clé hôte SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Type de vérification de la clé hôte SFTP.

Les types de vérification de clé d'hôte SFTP suivants sont pris en charge :

- `strict` - pgBackRest n’ajoutera jamais automatiquement les clés d’hôte au fichier ~/.ssh/known_hosts, et refusera de se connecter aux hôtes dont la clé d’hôte a changé ou n’est pas trouvée dans les fichiers known hosts. Cette option oblige l’utilisateur à ajouter manuellement tous les nouveaux hôtes.
- `accept-new` - pgBackRest ajoutera automatiquement les nouvelles clés d’hôte au fichier known hosts de l’utilisateur, mais n’autorisera pas les connexions aux hôtes dont la clé d’hôte a changé.
- `fingerprint` - pgBackRest vérifiera la clé d’hôte contre l’empreinte spécifiée par l’option `repo-sftp-host-fingerprint`.
- `none` - aucune vérification de clé d’hôte ne sera effectuée.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### Type de hachage de la clé hôte du dépôt SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Type de hachage de la clé d'hôte du dépôt SFTP.

Type de hachage de la clé hôte du dépôt SFTP. Déclare le type de hachage à utiliser pour calculer le hachage de la clé hôte du système distant au démarrage SSH. Les versions plus récentes de `libssh2` prennent en charge `sha256` en plus de md5 et sha1.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### Option de port hôte du dépôt SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Port hôte du dépôt SFTP.

Port hôte du dépôt SFTP.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### Option utilisateur hôte dépôt SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Utilisateur hôte du dépôt SFTP.

Utilisateur sur l'hôte utilisé pour stocker le dépôt.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### Option fichier Hôtes SFTP connus (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Fichier d'hôtes SFTP connus.

Fichier known hosts à consulter pour rechercher une correspondance avec un hôte SFTP lors de l'authentification. Si non spécifié, pgBackRest recherchera par défaut dans `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` et `/etc/ssh/ssh_known_hosts2`. Si configuré avec un ou plusieurs chemins de fichier, pgBackRest recherchera dans ces fichiers une correspondance. Les chemins de fichier doivent être complets ou commencer par un tilde. L'option `repo-sftp-known-host` peut être spécifiée plusieurs fois pour indiquer plusieurs fichiers known hosts à consulter. Pour utiliser la vérification du fichier known hosts, l'option `repo-sftp-host-fingerprint` ne doit pas être définie. Voir également l'option `repo-sftp-host-check-type`.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Option fichier de clé privée du dépôt SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Fichier de clé privée SFTP.

Fichier de clé privée SFTP utilisé pour l'authentification.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Option de fichier de clé publique du dépôt SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Fichier de clé publique SFTP.

Fichier de clé publique SFTP utilisé pour l'authentification. Facultatif si compilé contre OpenSSL, obligatoire si compilé contre une autre bibliothèque.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Option du fichier CA du dépôt de stockage (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

Fichier de certificat d'autorité de certification pour le dépôt.

Utilisez un fichier CA autre que celui par défaut du système pour les certificats du stockage (par exemple, S3, Azure).

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Noms obsolètes : repo-azure-ca-file, repo-s3-ca-file

### Option de chemin du certificat CA TLS pour le dépôt (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

Chemin du certificat d'autorité de certification du dépôt.

Utilisez un chemin de certificat d'autorité de certification (CA) autre que celui par défaut du système pour les certificats du stockage (par exemple, S3, Azure).

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

Noms obsolètes : repo-azure-ca-path, repo-s3-ca-path

### Option hôte de stockage du dépôt (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Hôte de stockage du dépôt.

Se connecter à un hôte autre que le point de terminaison de stockage (par exemple S3, Azure). Cela est généralement utilisé pour les tests.

```yaml
example: --repo1-storage-host=127.0.0.1
```

Noms obsolètes : repo-azure-host, repo-s3-host

### Option de port du stockage du dépôt (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Port du stockage du dépôt.

Port à utiliser lors de la connexion au point de terminaison du stockage (par exemple S3, Azure) ou à l'hôte (le cas échéant).

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

Noms obsolètes : repo-azure-port, repo-s3-port

### Option d'étiquette de stockage du dépôt (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Étiquette(s) de stockage du dépôt.

Spécifiez les balises à ajouter aux objets lorsque le dépôt est un magasin d'objets (par exemple, S3). L'option peut être répétée pour ajouter plusieurs balises.

Il n'existe aucune fonctionnalité dans pgBackRest permettant de modifier ces balises ; veillez donc à les définir correctement avant d'exécuter `stanza-create` afin d'assurer une cohérence des balises dans l'ensemble du dépôt.

```yaml
example: --repo1-storage-tag=key1=value1
```

### Option de taille de morceau de téléversement vers le dépôt (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Taille du morceau de téléversement vers le dépôt.

Les magasins d’objets tels que S3 permettent de téléverser des fichiers par morceaux lorsque le fichier est trop volumineux pour être stocké en mémoire. Même si le fichier peut être stocké en mémoire, il est plus efficace en mémoire de limiter la quantité de mémoire utilisée pour les téléversements.

Une taille de morceau plus élevée entraîne généralement de meilleures performances, car elle réduit le nombre de requêtes de téléversement et permet de téléverser plus de fichiers en une seule requête plutôt qu’en morceaux. Le désavantage est que la consommation mémoire sera plus élevée, et comme la mémoire tampon de morceau doit être allouée par processus, des valeurs plus élevées de `process-max` entraînent une consommation mémoire globale plus importante.

Notez que les tailles de morceau valides varient selon le type de stockage et la plateforme. Par exemple, AWS S3 impose une taille minimale de morceau de 5MiB. La terminologie relative à la taille du morceau varie selon le type de stockage ; utilisez donc « part size » pour AWS S3, « chunk size » pour GCS et « block size » pour Azure lorsque vous recherchez les valeurs minimales ou maximales.

Si un fichier est plus grand que 1GiB (la taille maximale que PostgreSQL crée par défaut), la taille de morceau sera augmentée progressivement jusqu'à la valeur maximale autorisée afin de terminer le téléversement du fichier.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### Option de vérification du certificat de stockage du dépôt (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Vérification du certificat du dépôt de stockage.

Cette option permet d’activer/désactiver la vérification du certificat TLS du serveur de stockage (par exemple, S3, Azure). La désactivation ne doit être utilisée que pour des tests ou d’autres scénarios où un certificat a été auto-signé.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

Noms obsolètes : repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Heure cible pour l'option dépôt (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

Heure cible pour le dépôt.

Le temps cible définit l'instant auquel les commandes lisent un dépôt sur un stockage versionné. Cela permet à la commande de lire le dépôt tel qu'il était à un instant donné, afin de récupérer des données supprimées ou corrompues par une erreur utilisateur ou un logiciel malveillant.

Le stockage versionné est pris en charge par S3, GCS et Azure, mais il est généralement désactivé par défaut. En plus d’activer le versioning, il peut être utile d’activer le verrouillage d’objets pour S3 et la suppression réversible pour GCS ou Azure.

Lorsque l'option `repo-target-time` est spécifiée, l'option `repo` doit également être fournie. Il est probable que tous les types de dépôt ne prennent pas en charge le versioning, et il est généralement préférable de cibler un seul dépôt pour la récupération.

Notez que les comparaisons avec l'horodatage de stockage sont <= à l'horodatage fourni et que les millisecondes sont tronquées de l'horodatage lorsqu'elles sont fournies.

```yaml
example: --repo-target-time=2024-08-08 12:12:12+00
```

### Option de type de dépôt (`--repo-type`) {#repository-type-option---repo-type}

Type de stockage utilisé pour le dépôt.

Les types de dépôt suivants sont pris en charge :

- `azure` - Service de stockage Blob Azure
- `cifs` - Comme `posix`, mais désactive les liens et les fsyncs de répertoire
- `gcs` - Google Cloud Storage
- `posix` - Systèmes de fichiers conformes à Posix
- `s3` - AWS Simple Storage Service
- `sftp` - Protocole de transfert de fichiers sécurisé

Lorsqu’un montage NFS est utilisé comme dépôt `posix`, les mêmes règles s’appliquent à pgBackRest qu’indiquées dans la documentation PostgreSQL : [Création d’un cluster de base de données - Systèmes de fichiers](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```yaml
default: posix
example: --repo1-type=cifs
```
