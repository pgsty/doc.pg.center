---
title: "Commande de sauvegarde (backup)"
linkTitle: "backup"
weight: 40
description: "Référence des options et du comportement de la commande pgBackRest `backup`."
icon: fa-solid fa-box-archive
module: [PGBACKREST]
categories: [Référence]
upstream_link: "https://pgbackrest.org/command.html#command-backup"
---

Lorsque plusieurs dépôts sont configurés, pgBackRest effectuera la sauvegarde vers le dépôt de priorité la plus élevée (par exemple `repo1`) sauf si l'option `--repo` est spécifiée.

pgBackRest ne dispose pas de planificateur intégré, il est donc préférable de l'exécuter depuis cron ou un autre mécanisme de planification.

Consultez [Effectuer une sauvegarde](/fr/pgbackrest/user-guide/#perform-a-backup) pour plus de détails et d'exemples.

## Options de commande {#command-options}

### Option d'annotation de sauvegarde (`--annotation`) {#backup-annotation-option---annotation}

Ajoutez des paires clé/valeur définies par l'utilisateur à la sauvegarde.

Les utilisateurs peuvent attacher des paires clé/valeur explicatives à la sauvegarde. Cette option peut être utilisée plusieurs fois pour attacher plusieurs annotations.

Les annotations sont produites par la sortie texte de la commande `info` lorsque une sauvegarde est spécifiée avec `--set`, et apparaissent toujours dans la sortie JSON.

```yaml
example: --annotation=source="Sunday backup for website database"
```

### Option de vérification de l'archive (`--archive-check`) {#check-archive-option---archive-check}

Vérifiez que les segments WAL sont présents dans l'archive avant la fin de la sauvegarde.

Vérifie que tous les segments WAL nécessaires pour rendre la sauvegarde cohérente sont présents dans l’archive WAL. Il est recommandé de laisser cette option par défaut, sauf si vous utilisez une autre méthode d’archivage.

Cette option doit être activée si `archive-copy` est activé.

```yaml
default: y
example: --no-archive-check
```

### Option de copie d'archive (`--archive-copy`) {#copy-archive-option---archive-copy}

Copiez les segments WAL nécessaires à la cohérence vers la sauvegarde.

Cette option, légèrement paranoïaque, protège contre les corruptions dans l’archive des segments WAL en stockant directement dans la sauvegarde les segments WAL nécessaires à la cohérence. Les segments WAL sont toujours stockés dans l’archive, donc cette option utilise un espace supplémentaire.

Il est préférable que les commandes `archive-push` et `backup` utilisent le même `compress-type` (par exemple `lz4`) lors de l'utilisation de cette option. Sinon, les segments WAL devront être récompressés avec le `compress-type` utilisé par la sauvegarde, ce qui peut s'avérer assez coûteux selon la quantité de WAL générée pendant la sauvegarde.

Lors d'une restauration, les segments WAL seront présents dans `pg_xlog/pg_wal` et PostgreSQL les utilisera en priorité plutôt que d'appeler `restore_command`.

L'option `archive-check` doit être activée si `archive-copy` est activé.

```yaml
default: n
example: --archive-copy
```

### Vérifier l'option Mode archive (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

Vérifiez le paramètre PostgreSQL `archive_mode`.

Activé par défaut, cette option interdit PostgreSQL `archive_mode=always`.

Les segments WAL poussés depuis un serveur de secours peuvent être logiquement identiques aux segments WAL poussés depuis le principal, mais présenter des sommes de contrôle différentes. Il est recommandé de désactiver l'archivage depuis plusieurs sources afin d'éviter les conflits.

AVERTISSEMENT :

Si cette option est désactivée, il est essentiel de s'assurer qu’un seul archivage écrit dans le dépôt via la commande `archive-push`.

```yaml
default: y
example: --no-archive-mode-check
```

### Option délai d'archivage (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

Délai d'attente de l'archive.

Définir le délai maximal, en secondes, d'attente pour chaque segment WAL afin qu'il atteigne le dépôt d'archive pgBackRest. Ce délai s'applique aux commandes `check` et `backup` lors de l'attente des segments WAL nécessaires à la cohérence de la sauvegarde.

```yaml
default: 1m
allowed: [100ms, 1d]
example: --archive-timeout=30
```

### Option de sauvegarde depuis une instance de secours (`--backup-standby`) {#backup-from-standby-option---backup-standby}

Sauvegarde à partir du cluster de secours.

Activez la sauvegarde depuis le serveur de secours afin de réduire la charge sur le cluster principal. Cette option nécessite que les hôtes principal et de secours soient configurés.

Les modes suivants sont pris en charge :

- `y` - un serveur standby est obligatoire pour la sauvegarde.
- `prefer` - effectuer la sauvegarde depuis le serveur standby s'il est disponible, sinon depuis le primaire.
- `n` - effectuer la sauvegarde uniquement depuis le primaire.

```yaml
default: n
example: --backup-standby=y
```

### Option sommes de contrôle (`--checksum-page`) {#page-checksums-option---checksum-page}

Valider les sommes de contrôle des pages de données.

Active la validation de toutes les sommes de contrôle des pages de données lors de la sauvegarde d'un cluster. Cette option est activée automatiquement lorsque les sommes de contrôle des pages de données sont activées sur le cluster.

Par défaut, les échecs de validation des sommes de contrôle n'interrompent pas une sauvegarde : des avertissements sont émis dans le journal (et sur la console avec les paramètres par défaut), et la liste des pages invalides est enregistrée dans le manifeste de sauvegarde. Définissez `checksum-page-error=y` pour interrompre la sauvegarde à la place.

```yaml
example: --no-checksum-page
```

### Option d’erreur en cas de sommes de contrôle de pages invalides (`--checksum-page-error`) {#error-on-invalid-page-checksums-option---checksum-page-error}

Signaler une erreur en cas de sommes de contrôle de pages invalides.

Lorsque cette option est activée avec `checksum-page`, un échec de validation des sommes de contrôle de pages interrompt la sauvegarde.

```yaml
default: n
example: --no-checksum-page-error
```

### Option d'exclusion de chemins/fichiers (`--exclude`) {#pathfile-exclusions-option---exclude}

Exclure les chemins ou fichiers de la sauvegarde.

Toutes les exclusions sont relatives à `$PGDATA`. Si l'exclusion se termine par /, seuls les fichiers du répertoire spécifié seront exclus, par exemple `--exclude=junk/` exclura tous les fichiers du répertoire `$PGDATA/junk` tout en conservant le répertoire lui-même. Si l'exclusion ne se termine pas par /, le fichier peut correspondre exactement à l'exclusion ou correspondre à l'exclusion suivie de /, par exemple `--exclude=junk` exclura le répertoire `$PGDATA/junk` ainsi que tous les fichiers qu'il contient.

**Faites attention à utiliser cette fonctionnalité — il est très facile d'exclure quelque chose de crucial qui rendra la sauvegarde inconsistante. Assurez-vous de tester vos restaurations !**

Tous les fichiers exclus seront journalisés au niveau `info` ainsi que la règle d'exclusion. Vérifiez soigneusement la liste des fichiers exclus afin de vous assurer qu'aucun fichier inattendu n'est exclu.

> **NOTE :** Les exclusions ne sont pas prises en compte lors d'une restauration delta. Tous les fichiers ou répertoires exclus lors de la sauvegarde seront *supprimés* lors d'une restauration delta.

Cette option ne doit pas être utilisée pour exclure les journaux PostgreSQL d'une sauvegarde. Les journaux peuvent être déplacés hors du répertoire `PGDATA` à l'aide de la configuration PostgreSQL `log_directory`, ce qui permet de conserver les journaux après une restauration.

Plusieurs exclusions peuvent être spécifiées en ligne de commande ou dans un fichier de configuration.

```yaml
example: --exclude=junk/
```

### Option d'expiration automatique (`--expire-auto`) {#expire-auto-option---expire-auto}

Exécuter automatiquement la commande `expire` après une sauvegarde réussie.

L’option est activée par défaut. Faites preuve de prudence en la désactivant, car cela entraînera le maintien indéfini de toutes les sauvegardes et archives, ce qui pourrait faire épuiser l’espace disponible dans le dépôt. La commande `expire` devra être exécutée régulièrement afin d’éviter ce problème.

Lorsque `expire` est exécuté automatiquement après une sauvegarde réussie, il utilise la configuration de la commande `backup`, de sorte que les options définies uniquement dans une section de commande `expire` (par exemple `[global:expire]`) ne sont pas prises en compte. Pour appliquer une configuration spécifique à `expire`, désactivez cette option et exécutez la commande `expire` séparément.

```yaml
default: y
example: --expire-auto
```

### Option de forçage (`--force`) {#force-option---force}

Forcer une sauvegarde hors ligne.

Lorsqu’il est utilisé avec `--no-start-stop`, une sauvegarde sera exécutée même si pgBackRest estime que PostgreSQL est en cours d’exécution. **Cette option doit être utilisée avec une extrême prudence, car elle risque fortement de produire une sauvegarde corrompue.**

Il existe certains scénarios où une sauvegarde peut toutefois être souhaitable dans ces conditions. Par exemple, si un serveur tombe en panne et que le volume du cluster de base de données ne peut être monté qu’en lecture seule, il serait judicieux de réaliser une sauvegarde même si `postmaster.pid` est présent. Dans ce cas, il serait préférable de revenir à la sauvegarde précédente et de rejouer les WAL, mais il se peut qu’une transaction très importante se trouve dans un segment WAL qui n’a pas été archivé.

```yaml
default: n
example: --force
```

### Option seuil d'enregistrement du manifeste (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

Seuil d'enregistrement du manifeste pendant la sauvegarde.

Définit la fréquence à laquelle le manifeste sera enregistré pendant une sauvegarde. Enregistrer le manifeste est important car il stocke les sommes de contrôle et permet au fonctionnement de la reprise d’être efficace. Le seuil réel utilisé est le plus élevé entre 1 % de la taille de la sauvegarde et `manifest-save-threshold`.

```yaml
default: 1GiB
allowed: [1B, 1TiB]
example: --manifest-save-threshold=8GiB
```

### Option en ligne (`--online`) {#online-option---online}

Effectuez une sauvegarde en ligne.

Spécifier --no-online empêche pgBackRest d'exécuter les fonctions de démarrage/arrêt de la sauvegarde sur le cluster de base de données. Pour que cela fonctionne, PostgreSQL doit être arrêté, et pgBackRest générera une erreur si ce n'est pas le cas.

Cette option a pour but de permettre les sauvegardes hors ligne. Le répertoire `pg_xlog`/`pg_wal` est copié tel quel et `archive-check` est automatiquement désactivé pour la sauvegarde.

```yaml
default: y
example: --no-online
```

### Option de reprise (`--resume`) {#resume-option---resume}

Permet la reprise d'une sauvegarde interrompue.

Définit si la fonction de reprise est activée. La reprise peut réduire considérablement le temps nécessaire pour exécuter une sauvegarde après un échec précédent de la même nature. Toutefois, elle ajoute de la complexité, aussi peut-il être souhaitable de la désactiver dans les environnements qui n'en ont pas besoin.

```yaml
default: y
example: --no-resume
```

### Option Démarrage rapide (`--start-fast`) {#start-fast-option---start-fast}

Forcer un checkpoint pour démarrer la sauvegarde plus rapidement.

Force un checkpoint (en passant `y` au paramètre `fast` de la fonction de démarrage de la sauvegarde) afin que la sauvegarde commence immédiatement. Sinon, la sauvegarde commencera après le prochain checkpoint régulier.

```yaml
default: n
example: --start-fast
```

### Option de type (`--type`) {#type-option---type}

Type de sauvegarde.

Les types de sauvegarde suivants sont pris en charge :

- `full` - tous les fichiers du cluster de base de données seront copiés et aucune dépendance avec les sauvegardes précédentes ne sera requise.
- `incr` - sauvegarde incrémentielle à partir de la dernière sauvegarde réussie.
- `diff` - semblable à une sauvegarde incrémentielle, mais toujours basée sur la dernière sauvegarde complète.

```yaml
default: incr
example: --type=full
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

### Option de commande pgBackRest (`--cmd`) {#pgbackrest-command-option---cmd}

Commande pgBackRest.

pgBackRest peut générer une chaîne de commande, par exemple lorsque la commande `restore` génère le paramètre restore_command. Dans ce cas, la commande utilisée pour exécuter le processus pgBackRest sera employée, sauf si l'option `cmd` est fournie.

AVERTISSEMENT :

Envelopper la commande pgBackRest peut entraîner un comportement imprévisible et n'est pas recommandé.

```yaml
default: [path of executed pgbackrest binary]
example: --cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### Option de commande client SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Commande cliente SSH.

Utilisez une commande cliente SSH spécifique lorsque vous souhaitez utiliser une alternative ou que la commande `ssh` n'est pas disponible dans $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Option de compression (`--compress`) {#compress-option---compress}

Utilisez la compression des fichiers.

Les fichiers de sauvegarde sont compatibles avec les outils de compression en ligne de commande.

Cette option est désormais obsolète. L'option `compress-type` doit être utilisée à la place.

```yaml
default: y
example: --no-compress
```

### Option niveau de compression (`--compress-level`) {#compress-level-option---compress-level}

Niveau de compression du fichier.

Définit le niveau à utiliser pour la compression des fichiers lorsque `compress-type` est différent de `none` ou `compress=y` (obsolète).

```yaml
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: --compress-level=9
```

### Option niveau de compression réseau (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Niveau de compression du réseau.

Définit le niveau de compression réseau lorsque `compress-type=none` et que la commande n'est pas exécutée sur le même hôte que le dépôt. La compression est utilisée pour réduire le trafic réseau. Lorsque `compress-type` est différent de `none`, le paramètre `compress-level-network` est ignoré et `compress-level` est utilisé à la place, afin que le fichier ne soit compressé qu'une seule fois.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### Option de type de compression (`--compress-type`) {#compress-type-option---compress-type}

Type de compression des fichiers.

Les types de compression suivants sont pris en charge :

- `none` - pas de compression
- `bz2` - format de compression bzip2
- `gz` - format de compression gzip
- `lz4` - format de compression lz4 (non disponible sur toutes les plates-formes)
- `zst` - format de compression Zstandard (non disponible sur toutes les plates-formes)

```yaml
default: gz
example: --compress-type=none
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

### Option de délai d'attente de la base de données (`--db-timeout`) {#database-timeout-option---db-timeout}

Délai d'attente des requêtes de base de données.

Définit le délai d'attente, en secondes, des requêtes effectuées contre la base de données. Cela inclut les fonctions de démarrage et d'arrêt de la sauvegarde, qui peuvent chacune prendre beaucoup de temps. En raison de cela, le délai d'attente doit être maintenu élevé, sauf si vous savez que ces fonctions retourneront rapidement (par exemple, si vous avez défini `start-fast=y` et que vous savez que le cluster de base de données ne générera pas beaucoup de segments WAL pendant la sauvegarde).

> **NOTE :** L'option `db-timeout` doit être inférieure à l'option `protocol-timeout`.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### Option Delta (`--delta`) {#delta-option---delta}

Restauration ou sauvegarde à l’aide de sommes de contrôle.

Lors d'une restauration, par défaut, les répertoires de données PostgreSQL et les répertoires de tablespace sont supposés exister mais être vides. Cette option effectue une restauration delta à l'aide des sommes de contrôle.

Pendant une sauvegarde, cette option utilisera les sommes de contrôle au lieu des horodatages pour déterminer si les fichiers seront copiés.

```yaml
default: n
example: --delta
```

### Option de délai d'attente d'E/S (`--io-timeout`) {#io-timeout-option---io-timeout}

Délai d'attente des E/S.

Délai d'attente, en secondes, utilisé pour les connexions et les opérations de lecture/écriture.

Notez que l'opération de lecture/écriture entière n'a pas besoin de se terminer dans ce délai d'attente, mais *une certaine* progression doit être réalisée, même si elle ne concerne qu'un seul octet.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Option Chemin verrou (`--lock-path`) {#lock-path-option---lock-path}

Chemin où les fichiers verrou sont stockés.

Le chemin de verrouillage fournit un emplacement où pgBackRest peut créer des fichiers de verrouillage afin d'empêcher l'exécution simultanée d'opérations en conflit.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
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

### Option de processus maximum (`--process-max`) {#process-maximum-option---process-max}

Nombre maximal de processus à utiliser pour la compression ou le transfert.

Chaque processus effectuera une compression et un transfert afin d'accélérer l'exécution de la commande, mais ne définissez pas `process-max` trop élevé afin de ne pas affecter les performances de la base de données.

```yaml
default: 1
allowed: [1, 999]
example: --process-max=4
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

### Option stanza (`--stanza`) {#stanza-option---stanza}

Définit la stanza.

Une stanza est la configuration d'un cluster de base de données PostgreSQL qui définit son emplacement, la manière dont il sera sauvegardé, les options d'archivage, etc. La plupart des serveurs de base de données n'ont qu'un seul cluster PostgreSQL et donc une seule stanza, tandis que les serveurs de sauvegarde ont une stanza pour chaque cluster de base de données à sauvegarder.

Il est tentant de nommer la stanza en fonction du cluster principal, mais un nom plus pertinent décrit les bases de données contenues dans le cluster. Étant donné que le nom de la stanza sera utilisé pour le principal et toutes les répliques, il est préférable de choisir un nom qui décrit la fonction réelle du cluster, par exemple app ou dw, plutôt que le nom local du cluster, comme main ou prod.

```yaml
example: --stanza=main
```

### Option de nombre de messages Keep Alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

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

### Option Suites de chiffrement TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Suites de chiffrement TLSv1.2 autorisées.

Toutes les connexions TLS entre le client pgBackRest et le serveur sont chiffrées. Par défaut, les connexions aux magasins d'objets (par exemple S3) sont également chiffrées.

> **NOTE :** Le niveau de sécurité minimal absolu pour toute connexion de transport est TLSv1.2.

Les suites de chiffrement acceptées peuvent être ajustées si nécessaire. L'exemple proposé constitue un choix raisonnable sauf si des exigences de sécurité spécifiques s'appliquent. Si non définies (valeur par défaut), la valeur par défaut de la bibliothèque OpenSSL sous-jacente s'applique.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Option Suites de chiffrement TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

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

## Options du mainteneur {#maintainer-options}

### Option de vérification de l’en-tête de page (`--page-header-check`) {#page-header-check-option---page-header-check}

Vérifier les en-têtes de page PostgreSQL.

Activé par défaut, cette option ajoute des vérifications d’en-tête de page.

Cette option doit être désactivée uniquement si nécessaire, par exemple si les pages sont chiffrées.

```yaml
default: y
example: --no-page-header-check
```

### Option de version PostgreSQL obligatoire (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

Forcer la version de PostgreSQL.

La version de PostgreSQL spécifiée sera utilisée à la place de la version détectée automatiquement en lisant `pg_control` ou les en-têtes WAL. Cela est principalement utile pour les forks de PostgreSQL ou les versions de développement où ces valeurs diffèrent de la version de publication. La version rapportée par PostgreSQL via `server_version_num` doit correspondre à la version forcée.

AVERTISSEMENT :

Faites preuve de prudence en utilisant cette option, car `pg_control` et les en-têtes WAL seront toujours lus selon le format attendu pour la version spécifiée, c'est-à-dire le format issu de la version open-source officielle de PostgreSQL. Si la version fork ou développée modifie le format des champs sur lesquels pgBackRest dépend, cela entraînera un comportement imprévu. En général, cette option ne fonctionnera correctement que si le fork ajoute tous les membres de structure personnalisés *après* les membres standard de PostgreSQL.

```yaml
example: --pg-version-force=15
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

Les types d'autorisation suivants sont pris en charge :

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

### Option de sauvegarde incrémentielle par bloc (`--repo-block`) {#block-incremental-backup-option---repo-block}

Activez la sauvegarde incrémentielle par bloc.

Le mode incrémentiel par bloc permet des sauvegardes plus granulaires en divisant les fichiers en blocs pouvant être sauvegardés indépendamment. Cela permet d'économiser de l'espace dans le dépôt et peut améliorer les performances de restauration delta, car des blocs individuels peuvent être récupérés sans devoir lire entièrement le fichier depuis le dépôt.

> **NOTE :** L'option `repo-bundle` doit être activée avant que `repo-block` ne puisse l'être.

La taille des blocs d’un fichier est déterminée en fonction de sa taille et de son âge. En général, les fichiers plus anciens ou plus volumineux reçoivent des tailles de blocs plus grandes. Si un fichier est suffisamment ancien, il ne sera pas sauvegardé en utilisant l’incrémentation par bloc.

La sauvegarde incrémentielle par bloc est optimale lorsqu'elle est activée pour toutes les catégories de sauvegarde, y compris les sauvegardes complètes. Cela rend la sauvegarde complète légèrement plus grande, mais permet aux sauvegardes différentielles et incrémentielles ultérieures d'utiliser les cartes de blocs générées par la sauvegarde complète afin de réduire l'espace utilisé.

```yaml
default: n
example: --repo1-block
```

### Option des paquets de dépôt (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

Fichiers du dépôt regroupés.

Regrouper les petits fichiers afin de réduire le nombre total de fichiers écrits dans le dépôt. Écrire moins de fichiers est généralement plus efficace, en particulier sur les magasins d'objets tels que S3. En outre, les fichiers vides ne sont pas stockés, sauf dans le manifeste, ce qui économise du temps et de l'espace.

```yaml
default: n
example: --repo1-bundle
```

### Option de limite du bundle de dépôt (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

Limite pour les paquets de fichiers.

Limite de taille pour les fichiers inclus dans les bundles. Les fichiers dont la taille dépasse cette limite seront stockés séparément.

Les fichiers intégrés ne peuvent pas être réutilisés lors d'une reprise d'une sauvegarde, donc cette option contrôle les fichiers pouvant être repris, c'est-à-dire que des valeurs plus élevées entraînent un nombre réduit de fichiers pouvant être repris.

```yaml
default: 2MiB
allowed: [8KiB, 1PiB]
example: --repo1-bundle-limit=10MiB
```

### Option taille du bundle de dépôt (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

Taille cible pour les paquets de fichiers.

Définit la taille cible des fichiers ajoutés à un seul lot. La taille du lot non compressé peut atteindre jusqu'à `repo-bundle-size` + `repo-bundle-limit`, donc ne définissez pas cette option à la taille maximale autorisée par votre système de fichiers.

En général, il n'est pas recommandé de définir cette option trop élevée, car les réessais devront répéter l'intégralité du lot.

```yaml
default: 20MiB
allowed: [1MiB, 1PiB]
example: --repo1-bundle-size=10MiB
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

### Option de bucket du dépôt GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Bucket du dépôt GCS.

Bucket GCS utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés à la racine du bucket en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par GCS dans le bucket.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### Option de point de terminaison du dépôt GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Point de terminaison du dépôt GCS.

Point de terminaison utilisé pour se connecter au service de stockage. Peut être mis à jour pour utiliser un serveur local GCS ou un point de terminaison alternatif.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### Type de clé du dépôt GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Type de clé du dépôt GCS.

Les types d'autorisation suivants sont pris en charge :

- `auto` - Autoriser à l'aide du compte de service de l'instance.
- `service` - Compte de service à partir d'une clé stockée localement.
- `token` - À utiliser pour les tests locaux, par exemple `fakegcs`.
- `web-id` - Autorisation à l'aide de Workload Identity Federation.

Lorsque `repo-gcs-key-type=service`, les identifiants seront rechargés lorsque le jeton d'authentification sera renouvelé.

Lorsque `repo-gcs-key-type=web-id`, l'option `repo-gcs-key` doit désigner un fichier d'identifiants de compte externe ; le jeton d'identité Web est rechargé lors du renouvellement du jeton d'authentification.

`service_account_impersonation_url` n'est pas pris en charge. Seul `credential_source.file` est pris en charge et, si `credential_source.format` est spécifié, son type doit être `text`.

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

### Option de lien dur pour le dépôt (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

Crée des liens durs entre les fichiers des sauvegardes dans le dépôt.

Activez le lien dur des fichiers dans les sauvegardes différentielles et incrémentielles vers leurs sauvegardes complètes. Cela donne l'illusion qu'au niveau du système de fichiers, chaque sauvegarde est une sauvegarde complète. Faites attention toutefois, car la modification de fichiers liés par lien dur peut affecter toutes les sauvegardes de l'ensemble.

```yaml
default: n
example: --repo1-hardlink
```

Nom obsolète : hardlink

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

### Option de rétention des archives (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Nombre de sauvegardes de WAL continu à conserver.

> **NOTE :** Les segments WAL nécessaires pour rendre une sauvegarde cohérente sont toujours conservés jusqu'à l'expiration de la sauvegarde, quelle que soit la configuration de cette option.

Si cette valeur n’est pas définie et que `repo-retention-full-type` est égal à `count` (valeur par défaut), alors l’archive à expirer sera par défaut celle correspondant à la valeur de `repo-retention-full` (ou `repo-retention-diff`) associée à `repo-retention-archive-type` si celle-ci est définie à `full` (ou `diff`). Cela garantira que les fichiers WAL ne seront supprimés que pour les sauvegardes déjà expirées. Si `repo-retention-full-type` est égal à `time`, alors cette valeur sera par défaut définie pour supprimer les archives antérieures à la plus ancienne sauvegarde complète conservée après avoir satisfait le paramètre `repo-retention-full`.

Cette option doit être définie si `repo-retention-archive-type` est réglé sur `incr`. Si l'espace disque est limité, ce paramètre, combiné à `repo-retention-archive-type`, peut être utilisé pour supprimer de manière agressive les segments WAL. Toutefois, cela annule la possibilité de réaliser une restauration à un instant donné à partir des sauvegardes ayant des segments WAL expirés, et n'est donc **pas** recommandé.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-archive=2
```

Nom obsolète : retention-archive

### Type de rétention des archives (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Type de sauvegarde pour la rétention de WAL.

Les types de sauvegarde suivants sont pris en charge :

- `full` - pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes défini par `repo-retention-archive`.
- `diff` - (différentiel) pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes et différentielles défini par `repo-retention-archive`, ce qui signifie qu'une sauvegarde complète prise en dernier sera comptée comme une sauvegarde différentielle pour l'application de la rétention du dépôt.
- `incr` - (incrémentielle) pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes, différentielles et incrémentielles défini par `repo-retention-archive`.

Il est recommandé de ne pas modifier cette option par rapport à sa valeur par défaut, qui n'expire les WAL que conjointement à l'expiration des sauvegardes complètes.

```yaml
default: full
example: --repo1-retention-archive-type=diff
```

Nom obsolète : retention-archive-type

### Option de rétention différentielle (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Nombre de sauvegardes différentielles à conserver.

Lorsqu'une sauvegarde différentielle expire, toutes les sauvegardes incrémentielles associées à cette sauvegarde différentielle expirent également. Si ce paramètre n'est pas défini, toutes les sauvegardes différentielles sont conservées jusqu'à l'expiration des sauvegardes complètes dont elles dépendent.

Notez que les sauvegardes complètes sont prises en compte dans le nombre de sauvegardes différentielles pour l'expiration. Cela réduit légèrement le nombre de sauvegardes différentielles à conserver dans la plupart des cas.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-diff=3
```

Nom obsolète : retention-diff

### Option de rétention complète (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Nombre ou durée de rétention des sauvegardes complètes.

Lorsqu'une sauvegarde complète expire, toutes les sauvegardes différentielles et incrémentielles associées à cette sauvegarde complète expirent également. Si l'option n'est pas définie, un avertissement est émis. Si une rétention indéfinie est souhaitée, définissez l'option à sa valeur maximale.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-full=2
```

Nom obsolète : retention-full

### Type d'option de rétention complète (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Type de rétention pour les sauvegardes complètes.

Détermine si le paramètre `repo-retention-full` représente une période de temps (en jours) ou un nombre de sauvegardes complètes à conserver.

Les types de rétention suivants sont pris en charge :

- `time` - les sauvegardes complètes dont l'âge dépasse `repo-retention-full` seront supprimées du dépôt si au moins une autre sauvegarde a un âge supérieur ou égal au nombre de jours défini par `repo-retention-full`. Par exemple, si `repo-retention-full` est égal à 30 (jours) et qu'il existe 2 sauvegardes complètes : l'une âgée de 25 jours et l'autre de 35 jours, aucune sauvegarde complète ne sera expirée, car la suppression de la sauvegarde âgée de 35 jours laisserait uniquement la sauvegarde âgée de 25 jours, ce qui violerait la politique de rétention de 30 jours exigeant qu'au moins une sauvegarde ait au moins 30 jours d'âge avant qu'une sauvegarde plus ancienne ne puisse être expirée. Les archives WAL plus anciennes que la plus ancienne sauvegarde complète restante seront automatiquement expirées, sauf si `repo-retention-archive-type` et `repo-retention-archive` sont explicitement définis.
- `count` - les sauvegardes complètes dont le nombre dépasse `repo-retention-full` seront supprimées. Par exemple, si `repo-retention-full` est égal à `4` et qu'une cinquième sauvegarde complète est effectuée, la sauvegarde complète la plus ancienne sera supprimée afin de maintenir le nombre à 4.

Notez qu'une sauvegarde ne sera prise en compte pour la rétention qu'après avoir été correctement terminée. Par exemple, si `repo-retention-full-type` est `count` et `repo-retention-full` est `2`, il doit y avoir 3 sauvegardes complètes avant que la plus ancienne ne soit supprimée.

```yaml
default: count
example: --repo1-retention-full-type=time
```

### Option de rétention de l'historique des sauvegardes (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Nombre de jours d'historique de sauvegarde à conserver.

Une copie du manifeste de sauvegarde est stockée dans le chemin `backup.history` une fois la sauvegarde terminée. Par défaut, ces fichiers ne sont jamais supprimés, car ils sont utiles pour l'analyse de données, par exemple pour mesurer l'évolution de la taille des sauvegardes et des fichiers WAL au fil du temps.

Définissez `repo-retention-history` pour préciser le nombre de jours de manifestes d'historique de sauvegarde à conserver. Les sauvegardes non expirées sont toujours conservées dans l'historique des sauvegardes. Spécifiez `repo-retention-history=0` pour ne conserver l'historique des sauvegardes que pour les sauvegardes non expirées.

Lorsqu'un manifeste d'historique de sauvegarde complète est expiré, tous les manifestes d'historique de sauvegardes différentielles et incrémentielles associés à cette sauvegarde complète expirent également.

```yaml
allowed: [0, 9999999]
example: --repo1-retention-history=365
```

### Option de bucket du dépôt S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

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

Les types d'autorisation suivants sont pris en charge :

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

Le service de signature S3 utilisé dans l'authentification SigV4. La valeur par défaut est `s3` pour les points de terminaison S3 standards. À définir sur `s3-outposts` lors de l'utilisation d'un point de terminaison S3 Outposts.

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

Définit le type de hachage utilisé pour calculer l'empreinte de la clé hôte du système distant au démarrage de SSH. Les valeurs autorisées sont `md5`, `sha1` et `sha256`, mais seules les versions récentes de `libssh2` prennent en charge `sha256`.

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

### Option de prélecture du stockage du dépôt (`--repo-storage-prefetch`) {#repository-storage-prefetch-option---repo-storage-prefetch}

Prélecture du stockage du dépôt.

Détermine le nombre de requêtes à anticiper lors de la lecture depuis un stockage objet, tel que S3. Il ne s'agit pas d'une véritable exécution concurrente, mais cela réduit la latence liée à l'envoi des requêtes.

Le nombre de requêtes ouvertes par lecture est supérieur d'une unité à la valeur de prélecture, car la lecture initiale ne peut pas être anticipée.

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### Option de lecture au-delà des données utiles du stockage du dépôt (`--repo-storage-read-over`) {#repository-storage-read-over-option---repo-storage-read-over}

Lecture au-delà des données utiles du stockage du dépôt.

Les bundles peuvent contenir des données inutiles à la restauration, par exemple des fichiers déjà présents. Cette option permet de passer ces données en poursuivant la lecture, sans lancer une nouvelle requête de lecture sur le stockage objet. C'est généralement plus rapide, car la latence d'une nouvelle requête de lecture est supérieure à celle de la poursuite d'une lecture en cours. C'est également moins coûteux pour la plupart des classes de stockage.

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

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

### Option de lien symbolique du dépôt (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Créez des liens symboliques dans le dépôt.

Active la création du `latest` et des liens symboliques de tablespace. Ces liens symboliques sont particulièrement utiles lors de la récupération in situ à l’aide de captures instantanées dans le dépôt, ce qui constitue un cas d’utilisation peu courant.

Bien que cette fonctionnalité soit probablement inutile pour la grande majorité des utilisateurs, elle reste activée par défaut pour des raisons de compatibilité avec les anciennes versions. Toutefois, il peut être utile de désactiver les liens symboliques pour les stockages de type Posix qui ne les prennent pas en charge.

```yaml
default: y
example: --no-repo1-symlink
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

## Options de stanza {#stanza-options}

### Option base de données PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

Base de données PostgreSQL.

Le nom de la base de données utilisé lors de la connexion à PostgreSQL. La valeur par défaut est généralement la meilleure option, mais certaines installations peuvent ne pas contenir cette base de données.

Notez que, pour des raisons historiques, le paramétrage de la variable d'environnement `PGDATABASE` sera ignoré.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### Option Hôte PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

Hôte PostgreSQL pour une opération à distance.

Utilisé pour les sauvegardes où l'hôte PostgreSQL est différent de l'hôte du dépôt.

```yaml
example: --pg1-host=db.domain.com
```

Nom obsolète : db-host

### Option Fichier de l'Autorité de certification du serveur PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Fichier de l'autorité de certification du serveur PostgreSQL.

Utilisez un fichier CA autre que celui par défaut du système pour vous connecter à l'hôte PostgreSQL.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option Chemin de l'Autorité de certification du serveur PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Chemin de l'autorité de certification du serveur PostgreSQL.

Utilisez un chemin de certificat d'autorité de certification (CA) autre que celui par défaut du système pour établir la connexion avec l'hôte PostgreSQL.

```yaml
example: --pg1-host-ca-path=/etc/pki/tls/certs
```

### Option Fichier de certificat d'hôte PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Fichier de certificat d'hôte PostgreSQL.

Envoyé à l'hôte PostgreSQL pour prouver l'identité du client.

```yaml
example: --pg1-host-cert-file=/path/to/client.crt
```

### Option de commande hôte PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

Commande pgBackRest de l'hôte PostgreSQL.

Requis uniquement si le chemin vers la commande pgBackRest est différent sur les hôtes locaux et PostgreSQL. Si ce n'est pas défini, la commande sur l'hôte PostgreSQL sera définie de la même manière que celle sur l'hôte local.

```yaml
default: [path of executed pgbackrest binary]
example: --pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nom obsolète : db-cmd

### Option de configuration hôte PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

Fichier de configuration du serveur de base de données pgBackRest.

Spécifie l'emplacement du fichier de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le fichier de configuration PostgreSQL est situé à un emplacement différent du fichier de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nom obsolète : db-config

### Chemin d'inclusion de la configuration hôte PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Chemin d'inclusion de configuration de l'hôte de base de données pgBackRest.

Définit l'emplacement du chemin d'inclusion de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le chemin d'inclusion de configuration PostgreSQL se trouve dans un emplacement différent du chemin d'inclusion de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option de chemin de configuration de l'hôte PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

Chemin de configuration de l'hôte de base de données pgBackRest.

Définit l'emplacement du chemin de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le chemin de configuration PostgreSQL se trouve dans un emplacement différent du chemin de configuration local.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --pg1-host-config-path=/conf/pgbackrest
```

### Option fichier clé hôte PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Fichier de clé hôte PostgreSQL.

Vérifie que le certificat client a été envoyé par le propriétaire.

```yaml
example: --pg1-host-key-file=/path/to/client.key
```

### Option Port hôte PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Port de l'hôte PostgreSQL lorsque `pg-host` est défini.

Utilisez cette option pour spécifier un port non par défaut pour le protocole d'hôte PostgreSQL.

> **NOTE :** Lorsque `pg-host-type=ssh`, il n'existe pas de valeur par défaut pour `pg-host-port`. Dans ce cas, le port sera celui configuré pour la commande spécifiée par `cmd-ssh`.

```yaml
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: --pg1-host-port=25
```

Nom obsolète : db-ssh-port

### Type de protocole d'hôte PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Type de protocole hôte PostgreSQL.

Les types de protocole suivants sont pris en charge :

- `ssh` - Shell sécurisé.
- `tls` - Serveur TLS pgBackRest.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### Option utilisateur hôte PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Utilisateur de connexion au serveur PostgreSQL lorsqu'`pg-host` est défini.

Cet utilisateur possédera également le processus pgBackRest distant et initiera les connexions à PostgreSQL. Pour que cela fonctionne correctement, l'utilisateur doit être le propriétaire du cluster de base de données PostgreSQL, ce qui correspond généralement à `postgres`, la valeur par défaut.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

Nom obsolète : db-user

### Option Chemin PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

Répertoire de données PostgreSQL.

Il doit être identique à la valeur `data_directory` rapportée par PostgreSQL. Même si cette valeur peut être lue à divers endroits, il est prudent de la définir afin de garantir sa disponibilité en cas de restauration ou de sauvegarde hors ligne.

L'option `pg-path` est vérifiée par rapport à la valeur rapportée par PostgreSQL à chaque sauvegarde en ligne, elle doit donc toujours être à jour.

```yaml
example: --pg1-path=/data/db
```

Nom obsolète : db-path

### Option de port PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

Port PostgreSQL.

Port sur lequel PostgreSQL est en cours d'exécution. Ce paramètre n'a généralement pas besoin d'être spécifié, car la plupart des clusters PostgreSQL s'exécutent sur le port par défaut.

```yaml
default: 5432
allowed: [0, 65535]
example: --pg1-port=6543
```

Nom obsolète : db-port

### Option Chemin du socket PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Chemin du socket Unix de PostgreSQL.

Répertoire du socket Unix spécifié lors du démarrage de PostgreSQL. pgBackRest recherche automatiquement dans l'emplacement standard de votre système d'exploitation, aussi il est généralement inutile de préciser ce paramètre, sauf si le répertoire du socket a été explicitement modifié à l'aide du paramètre `unix_socket_directories` dans `postgresql.conf`.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

Nom obsolète : db-socket-path

### Option utilisateur de base de données PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

Utilisateur de base de données PostgreSQL.

Le nom d'utilisateur de la base de données utilisé lors de la connexion à PostgreSQL. Si non spécifié, pgBackRest se connectera avec l'utilisateur système local ou `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
