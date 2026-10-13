---
title: "Référence de configuration"
linkTitle: "Configuration"
weight: 50
description: "Référence complète de configuration pgBackRest pour toutes les options, y compris l'archive, la sauvegarde, le dépôt et les options de stockage cloud."
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [Référence]
aliases: [/pgbackrest/configuration/]
upstream_link: "https://pgbackrest.org/configuration.html"
---

--------

## Introduction {#introduction}

pgBackRest peut être utilisé entièrement à l’aide de paramètres en ligne de commande, mais un fichier de configuration est plus pratique pour les installations complexes ou celles qui définissent de nombreux paramètres. L'emplacement par défaut du fichier de configuration est `/etc/pgbackrest/pgbackrest.conf`. Si aucun fichier n'existe à cet emplacement, l'ancien emplacement par défaut de `/etc/pgbackrest.conf` sera vérifié.

Les types d'option suivants sont utilisés :

**Chaîne** : Une chaîne de texte, couramment utilisée comme identifiant, mot de passe, etc.

Exemple de ligne de commande : `--stanza=demo`<br/> Exemple de fichier de configuration : `repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**Chemin** : Utilisé pour identifier de manière unique un emplacement dans une structure de répertoires. Les chemins doivent commencer par /, la double occurrence de // n'est pas autorisée, et aucun / final n'est attendu.

Exemple de ligne de commande : `--repo1-path=/var/lib/pgbackrest`<br/> Exemple de fichier de configuration : `repo1-path=/var/lib/pgbackrest`

**Booléen** : Active ou désactive l'option. Seules les valeurs y/n sont autorisées.

Exemples de ligne de commande : `--start-fast`, `--no-start-fast`, `--start-fast=y`, `--start-fast=n`<br/>Exemples de fichier de configuration : `start-fast=y`, `start-fast=n`

**Entier** : Utilisé pour les ports, les nombres de rétention ou de réessais, le nombre de processus parallèles autorisés, etc.

Exemple de ligne de commande : `--compress-level=3`<br/> Exemple de fichier de configuration : `pg1-port=5432`

**Taille** : Utilisée pour les tailles de tampon, l'utilisation du disque, etc. La taille peut être spécifiée en octets (par défaut) ou en KiB, MiB, GiB, TiB ou PiB, où le multiplicateur est une puissance de 1024. Par exemple, la valeur insensible à la casse 5GiB (ou 5GB, 5g) peut être utilisée à la place de 5368709120. Les valeurs fractionnaires telles que 2.5GiB ne sont pas autorisées ; utilisez 2560MiB à la place.

Exemple de ligne de commande : `--archive-get-queue-max=1GiB`<br/>Exemple de fichier de configuration : `buffer-size=2MiB`

**Temps** : Durée en secondes.

Exemple de ligne de commande : `--io-timeout=90`<br/> Exemple de fichier de configuration : `db-timeout=600`

**Liste** : L'option peut être fournie plusieurs fois.

Exemple de ligne de commande : `--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`

Exemple de fichier de configuration, chacun sur sa propre ligne :

```ini
db-exclude=db1
db-exclude=db2
db-exclude=db5
```

**Clé/Valeur** : L'option peut être fournie plusieurs fois au format `key=value`.

Exemple de ligne de commande : `--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`

Exemple de fichier de configuration, chacun sur sa propre ligne :

```ini
tablespace-map=ts_01=/db/ts_01
tablespace-map=ts_02=/db/ts_02
```

--------

## Options d'archive {#archive-options}

La section `archive` définit les options pour les commandes `archive-push` et `archive-get`.

### Option d'archivage asynchrone (`--archive-async`) {#asynchronous-archiving-option---archive-async}

Envoyer/récupérer les segments WAL de manière asynchrone.

Active l'exécution asynchrone pour les commandes `archive-push` et `archive-get`.

L'opération asynchrone est plus efficace car elle permet de réutiliser les connexions et de tirer parti de la parallélisation. Consultez les options `spool-path`, `archive-get-queue-max` et `archive-push-queue-max` pour plus d'informations.

```text
default: n
example: archive-async=y
```

### Taille maximale de la file d'attente de récupération d'archive (`--archive-get-queue-max`) {#maximum-archive-get-queue-size-option---archive-get-queue-max}

Taille maximale de la file d'attente archive-get de pgBackRest.

Spécifie la taille maximale de la file d’attente `archive-get` lorsque `archive-async` est activé. La file est stockée dans `spool-path` et sert à accélérer la fourniture des WAL à PostgreSQL.

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### Option de réessai du segment WAL manquant (`--archive-missing-retry`) {#retry-missing-wal-segment-option---archive-missing-retry}

Réessayer le segment WAL manquant

Réessayer un segment WAL précédemment signalé comme manquant par la commande `archive-get` en mode asynchrone. Cela empêche l'utilisation de notifications provenant d'une restauration antérieure dans le chemin de spool, qui pourrait entraîner une défaillance de récupération si la cohérence n'a pas été atteinte.

Désactiver cette option permet à PostgreSQL de reconnaître plus fiablement l’arrivée à la fin du WAL dans l’archive, ce qui permet de passer au streaming depuis le principal. Avec les réessais activés, un flux continu de WAL archivé fait que PostgreSQL continue de récupérer le WAL depuis l’archive au lieu de basculer vers le streaming.

Lorsque cette option est désactivée, il est important de s'assurer que le chemin de spool de la stanza est vide. La commande `restore` effectue automatiquement cette opération si le chemin de spool est configuré au moment de la restauration. Sinon, il incombe à l'utilisateur de s'assurer que le chemin de spool est vide.

```text
default: y
example: archive-missing-retry=n
```

### Option taille de lot de poussée d'archive (`--archive-push-batch-size`) {#archive-push-batch-size-option---archive-push-batch-size}

Quantité maximale de WAL à transférer par exécution asynchrone.

En mode asynchrone, le processus `archive-push` transmet tous les segments WAL prêts en une seule exécution. Comme `archive-push-queue-max` n'est vérifié qu'au début de chaque exécution, une exécution traitant un très grand nombre de segments peut faire croître la file d'attente bien au-delà de la limite avant qu'elle ne soit à nouveau vérifiée.

Cette option limite la quantité de WAL traitée par exécution, afin que le processus se termine et soit relancé par le prochain `archive-push`, qui vérifie à nouveau la file d'attente. Des valeurs plus faibles entraînent une vérification plus fréquente de la file d'attente, au prix d'un démarrage plus fréquent du processus asynchrone. La valeur est arrondie vers le bas à un nombre entier de segments WAL, mais au moins un segment est toujours traité.

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### Taille maximale de la file d'attente d'archivage en écriture (`--archive-push-queue-max`) {#maximum-archive-push-queue-size-option---archive-push-queue-max}

Taille maximale de la file d'attente d'archive PostgreSQL.

Une fois la limite atteinte, les actions suivantes se produiront :

- pgBackRest notifiera PostgreSQL que le WAL a été correctement archivé, puis **LE SUPPRIMERA**.
- Un avertissement sera affiché dans le journal de PostgreSQL.

Si cela se produit, le flux des journaux d'archive sera interrompu et la restauration à un point précis (PITR) ne sera plus possible au-delà de ce point. Une nouvelle sauvegarde sera nécessaire pour rétablir la capacité de restauration complète.

En mode asynchrone, toute la file d’attente sera supprimée afin d’éviter que des segments de WAL ne passent avant que la limite de file ne soit à nouveau dépassée.

En mode asynchrone, cette limite n’est vérifiée qu’au démarrage de chaque exécution de `archive-push`, de sorte que la file d’attente puisse dépasser cette limite au cours d’une même exécution. Réduisez `archive-push-batch-size` afin de vérifier la file d’attente plus fréquemment.

Ce mécanisme a pour but d'éviter que le volume de journalisation ne soit saturé, ce qui fermerait complètement PostgreSQL. Il est préférable de perdre une sauvegarde que de faire tomber PostgreSQL.

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

Nom obsolète : archive-queue-max

### Option délai d'archivage (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

Délai d'attente de l'archive.

Définir le délai maximal, en secondes, d'attente pour chaque segment WAL afin qu'il atteigne le dépôt d'archive pgBackRest. Ce délai s'applique aux commandes `check` et `backup` lors de l'attente des segments WAL nécessaires à la cohérence de la sauvegarde.

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## Options de sauvegarde {#backup-options}

La section `backup` définit les paramètres liés à la sauvegarde.

### Option d'annotation de sauvegarde (`--annotation`) {#backup-annotation-option---annotation}

Ajoutez des paires clé/valeur définies par l'utilisateur à la sauvegarde.

Les utilisateurs peuvent attacher des paires clé/valeur explicatives à la sauvegarde. Cette option peut être utilisée plusieurs fois pour attacher plusieurs annotations.

Les annotations sont produites par la sortie texte de la commande `info` lorsqu'une sauvegarde est spécifiée avec `--set`, et apparaissent toujours dans la sortie JSON.

```text
example: annotation=source="Sunday backup for website database"
```

### Option de vérification de l'archive (`--archive-check`) {#check-archive-option---archive-check}

Vérifiez que les segments WAL sont présents dans l'archive avant la fin de la sauvegarde.

Vérifie que tous les segments WAL nécessaires pour rendre la sauvegarde cohérente sont présents dans l’archive WAL. Il est recommandé de laisser cette option par défaut, sauf si vous utilisez une autre méthode d’archivage.

Cette option doit être activée si `archive-copy` est activé.

```text
default: y
example: archive-check=n
```

### Option de copie d'archive (`--archive-copy`) {#copy-archive-option---archive-copy}

Copiez les segments WAL nécessaires à la cohérence vers la sauvegarde.

Cette option, légèrement paranoïaque, protège contre la corruption dans l’archive des segments WAL en stockant directement dans la sauvegarde les segments WAL nécessaires à la cohérence. Les segments WAL sont toujours stockés dans l’archive, donc cette option utilise un espace supplémentaire.

Il est préférable que les commandes `archive-push` et `backup` utilisent le même `compress-type` (par exemple `lz4`) lors de l'utilisation de cette option. Sinon, les segments WAL devront être récompressés avec le `compress-type` utilisé par la sauvegarde, ce qui peut s'avérer assez coûteux selon la quantité de WAL générée pendant la sauvegarde.

Lors d'une restauration, les segments WAL seront présents dans `pg_xlog/pg_wal` et PostgreSQL les utilisera en priorité plutôt que d'appeler `restore_command`.

L'option `archive-check` doit être activée si `archive-copy` est activé.

```text
default: n
example: archive-copy=y
```

### Vérifier l'option Mode archive (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

Vérifiez le paramètre PostgreSQL `archive_mode`.

Activée par défaut, cette option interdit le paramètre PostgreSQL `archive_mode=always`.

Les segments WAL poussés depuis un serveur de secours peuvent être logiquement identiques aux segments WAL poussés depuis le principal, mais présenter des sommes de contrôle différentes. Il est recommandé de désactiver l'archivage depuis plusieurs sources afin d'éviter les conflits.

AVERTISSEMENT :

Si cette option est désactivée, il est essentiel de s'assurer qu’un seul processus d’archivage écrit dans le dépôt via la commande `archive-push`.

```text
default: y
example: archive-mode-check=n
```

### Option de sauvegarde depuis une instance de secours (`--backup-standby`) {#backup-from-standby-option---backup-standby}

Sauvegarde à partir du cluster de secours.

Activez la sauvegarde depuis le serveur de secours afin de réduire la charge sur le cluster principal. Cette option nécessite que les hôtes principal et de secours soient configurés.

Les modes suivants sont pris en charge :

- `y` - un serveur de secours est obligatoire pour la sauvegarde.
- `prefer` - effectuer la sauvegarde depuis le serveur de secours s'il est disponible, sinon depuis le principal.
- `n` - effectuer la sauvegarde uniquement depuis le principal.

```text
default: n
example: backup-standby=y
```

### Option sommes de contrôle (`--checksum-page`) {#page-checksums-option---checksum-page}

Valider les sommes de contrôle des pages de données.

Active la validation de toutes les sommes de contrôle des pages de données lors de la sauvegarde d'un cluster. Cette option est activée automatiquement lorsque les sommes de contrôle des pages de données sont activées sur le cluster.

Les échecs de validation de la somme de contrôle n'interrompent pas une sauvegarde. En revanche, des avertissements sont émis dans le journal (et sur la console avec les paramètres par défaut) et la liste des pages invalides est stockée dans le manifeste de sauvegarde.

```text
example: checksum-page=n
```

### Option d'exclusion de chemins/fichiers (`--exclude`) {#pathfile-exclusions-option---exclude}

Exclure les chemins ou fichiers de la sauvegarde.

Toutes les exclusions sont relatives à `$PGDATA`. Si l'exclusion se termine par /, seuls les fichiers du répertoire spécifié seront exclus, par exemple `--exclude=junk/` exclura tous les fichiers du répertoire `$PGDATA/junk` tout en conservant le répertoire lui-même. Si l'exclusion ne se termine pas par /, le fichier peut correspondre exactement à l'exclusion ou correspondre à l'exclusion suivie de /, par exemple `--exclude=junk` exclura le répertoire `$PGDATA/junk` ainsi que tous les fichiers qu'il contient.

**Faites attention à utiliser cette fonctionnalité — il est très facile d'exclure quelque chose de crucial qui rendra la sauvegarde inconsistante. Assurez-vous de tester vos restaurations !**

Tous les fichiers exclus seront journalisés au niveau `info` ainsi que la règle d'exclusion. Vérifiez soigneusement la liste des fichiers exclus afin de vous assurer qu'aucun fichier inattendu n'est exclu.

NOTE :

Les exclusions ne sont pas prises en compte lors d'une restauration delta. Tous les fichiers/répertoires exclus lors de la sauvegarde seront *supprimés* lors de la restauration delta.

Cette option ne doit pas être utilisée pour exclure les journaux PostgreSQL d'une sauvegarde. Les journaux peuvent être déplacés hors du répertoire `PGDATA` à l'aide de la configuration PostgreSQL `log_directory`, ce qui permet de conserver les journaux après une restauration.

Plusieurs exclusions peuvent être spécifiées en ligne de commande ou dans un fichier de configuration.

```text
example: exclude=junk/
```

### Option d'expiration automatique (`--expire-auto`) {#expire-auto-option---expire-auto}

Exécuter automatiquement la commande `expire` après une sauvegarde réussie.

L’option est activée par défaut. Faites preuve de prudence en la désactivant, car cela entraînera le maintien indéfini de toutes les sauvegardes et archives, ce qui pourrait épuiser l’espace disponible dans le dépôt. La commande `expire` devra être exécutée régulièrement afin d’éviter ce problème.

Lorsque `expire` est exécuté automatiquement après une sauvegarde réussie, il utilise la configuration de la commande `backup`, de sorte que les options définies uniquement dans une section de commande `expire` (par exemple `[global:expire]`) ne sont pas prises en compte. Pour appliquer une configuration spécifique à `expire`, désactivez cette option et exécutez la commande `expire` séparément.

```text
default: y
example: expire-auto=y
```

### Option seuil d'enregistrement du manifeste (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

Seuil de sauvegarde manifeste pendant la sauvegarde.

Définit la fréquence à laquelle le manifeste sera enregistré pendant une sauvegarde. Enregistrer le manifeste est important car il stocke les sommes de contrôle et permet au fonctionnement de la reprise d’être efficace. Le seuil réel utilisé est le plus élevé entre 1 % de la taille de la sauvegarde et `manifest-save-threshold`.

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### Option de reprise (`--resume`) {#resume-option---resume}

Permet la reprise d'une sauvegarde interrompue.

Définit si la fonction de reprise est activée. La reprise peut réduire considérablement le temps nécessaire pour exécuter une sauvegarde après l'échec d'une sauvegarde précédente du même type. Toutefois, elle ajoute de la complexité, aussi peut-il être souhaitable de la désactiver dans les environnements qui n'en ont pas besoin.

```text
default: y
example: resume=n
```

### Option Démarrage rapide (`--start-fast`) {#start-fast-option---start-fast}

Forcer un checkpoint pour démarrer la sauvegarde plus rapidement.

Force un checkpoint (en passant `y` au paramètre `fast` de la fonction de démarrage de la sauvegarde) afin que la sauvegarde commence immédiatement. Sinon, la sauvegarde commencera après le prochain checkpoint régulier.

```text
default: n
example: start-fast=y
```

--------

## Options générales {#general-options}

La section `general` définit les options communes à de nombreuses commandes.

### Autoriser l'exécution en tant qu'utilisateur root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Permettre à la commande de s'exécuter en tant qu'utilisateur root.

Par défaut, seule la commande `restore` peut être exécutée en tant qu'utilisateur root, car elle est conçue pour gérer soigneusement la propriété des fichiers. Exécuter d'autres commandes en tant que root risque de créer des fichiers (par exemple dans le dépôt) dont le propriétaire est root, rendant ces fichiers inaccessibles à l'utilisateur PostgreSQL, ce qui entraîne l'échec des commandes ultérieures.

Activez cette option pour exécuter une commande en tant qu'utilisateur root malgré tout. Toutefois, il est bien préférable d'exécuter pgBackRest en tant qu'utilisateur propriétaire du dépôt et du cluster PostgreSQL.

```text
default: n
example: allow-root=y
```

### Option Taille tampon (`--buffer-size`) {#buffer-size-option---buffer-size}

Taille du tampon pour les opérations d'E/S.

Taille de tampon utilisée pour les opérations de copie, de compression, de chiffrement et autres. Le nombre de tampons utilisés dépend des options, et chaque opération peut utiliser une mémoire supplémentaire, par exemple, la compression `gz` peut utiliser 256KiB de mémoire supplémentaire.

Les valeurs autorisées sont `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` et `16MiB`.

```text
default: 1MiB
example: buffer-size=2MiB
```

### Option de commande pgBackRest (`--cmd`) {#pgbackrest-command-option---cmd}

Commande pgBackRest.

pgBackRest peut générer une chaîne de commande, par exemple lorsque la commande `restore` génère le paramètre restore_command. Dans ce cas, la commande utilisée pour exécuter le processus pgBackRest sera employée, sauf si l'option `cmd` est fournie.

AVERTISSEMENT :

Envelopper la commande pgBackRest peut entraîner un comportement imprévisible et n'est pas recommandé.

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### Option de commande client SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Commande cliente SSH.

Utilisez une commande cliente SSH spécifique lorsque vous souhaitez utiliser une alternative ou que la commande `ssh` n'est pas disponible dans $PATH.

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### Option de compression (`--compress`) {#compress-option---compress}

Utilisez la compression des fichiers.

Les fichiers de sauvegarde sont compatibles avec les outils de compression en ligne de commande.

Cette option est désormais obsolète. L'option `compress-type` devrait être utilisée à la place.

```text
default: y
example: compress=n
```

### Option niveau de compression (`--compress-level`) {#compress-level-option---compress-level}

Niveau de compression du fichier.

Définit le niveau à utiliser pour la compression des fichiers lorsque `compress-type` est différent de `none` ou `compress=y` (obsolète).

```text
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

example: compress-level=9
```

### Option niveau de compression réseau (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Niveau de compression du réseau.

Définit le niveau de compression réseau lorsque `compress-type=none` et que la commande n'est pas exécutée sur le même hôte que le dépôt. La compression est utilisée pour réduire le trafic réseau. Lorsque `compress-type` est différent de `none`, le paramètre `compress-level-network` est ignoré et `compress-level` est utilisé à la place, afin que le fichier ne soit compressé qu'une seule fois.

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### Option de type de compression (`--compress-type`) {#compress-type-option---compress-type}

Type de compression des fichiers.

Les types de compression suivants sont pris en charge :

- `none` - pas de compression
- `bz2` - format de compression bzip2
- `gz` - format de compression gzip
- `lz4` - format de compression lz4 (non disponible sur toutes les plates-formes)
- `zst` - format de compression Zstandard (non disponible sur toutes les plates-formes)

```text
default: gz
example: compress-type=none
```

### Option de délai d'attente de la base de données (`--db-timeout`) {#database-timeout-option---db-timeout}

Délai d'attente des requêtes de base de données.

Définit le délai d'attente, en secondes, des requêtes effectuées contre la base de données. Cela inclut les fonctions de démarrage et d'arrêt de la sauvegarde, qui peuvent chacune prendre beaucoup de temps. En raison de cela, le délai d'attente doit être maintenu élevé, sauf si vous savez que ces fonctions retourneront rapidement (par exemple, si vous avez défini `start-fast=y` et que vous savez que le cluster de base de données ne générera pas beaucoup de segments WAL pendant la sauvegarde).

NOTE :

L'option `db-timeout` doit être inférieure à l'option `protocol-timeout`.

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### Option Delta (`--delta`) {#delta-option---delta}

Restauration ou sauvegarde à l’aide de sommes de contrôle.

Lors d'une restauration, par défaut, les répertoires de données PostgreSQL et les répertoires de tablespace sont supposés exister mais être vides. Cette option effectue une restauration delta à l'aide des sommes de contrôle.

Pendant une sauvegarde, cette option utilisera les sommes de contrôle au lieu des horodatages pour déterminer si les fichiers seront copiés.

```text
default: n
example: delta=y
```

### Option d'expiration I/O (`--io-timeout`) {#io-timeout-option---io-timeout}

Délai d'attente d'E/S.

Délai d'attente, en secondes, utilisé pour les connexions et les opérations de lecture/écriture.

Notez que l'opération de lecture/écriture entière n'a pas besoin de se terminer dans ce délai d'attente, mais *une certaine* progression doit être réalisée, même si elle ne concerne qu'un seul octet.

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### Option Chemin verrou (`--lock-path`) {#lock-path-option---lock-path}

Chemin où les fichiers verrou sont stockés.

Le chemin de verrouillage fournit un emplacement où pgBackRest peut créer des fichiers de verrouillage afin d'empêcher l'exécution simultanée d'opérations en conflit.

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### Option de masque neutre (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Utilisez un umask neutre.

Définit le umask à 0000 afin que les modes du dépôt soient créés de manière cohérente. Le mode par défaut du répertoire est 0750 et le mode par défaut du fichier est 0640.

Pour utiliser le umask de l'utilisateur en cours, spécifiez `neutral-umask=n` dans le fichier de configuration ou `--no-neutral-umask` en ligne de commande.

```text
default: y
example: neutral-umask=n
```

### Définir l'option de priorité du processus (`--priority`) {#set-process-priority-option---priority}

Définir la priorité du processus.

Définit la priorité (c’est-à-dire la valeur de niceness) accordée au processus par l’ordonnanceur du noyau. Les valeurs positives réduisent la priorité, tandis que les valeurs négatives l’augmentent. Dans la plupart des cas, les processus ne disposent pas des autorisations nécessaires pour augmenter leur priorité.

```text
allowed: [-20, 19]
example: priority=19
```

### Option de processus maximum (`--process-max`) {#process-maximum-option---process-max}

Nombre maximal de processus à utiliser pour la compression ou le transfert.

Chaque processus effectuera une compression et un transfert afin d'accélérer l'exécution de la commande, mais ne définissez pas `process-max` trop élevé afin de ne pas affecter les performances de la base de données.

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### Option délai d'attente du protocole (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Délai d'attente du protocole.

Définit le délai d'attente, en secondes, durant lequel le processus local ou distant attend qu'un nouveau message soit reçu au niveau du protocole. Cela empêche les processus de rester bloqués indéfiniment en attente d'un message.

NOTE :

L'option `protocol-timeout` doit être supérieure à l'option `db-timeout`.

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### Option Keep Alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Activation du keep-alive.

Active les messages keep-alive sur les connexions socket.

```text
default: y
example: sck-keep-alive=n
```

### Option Chemin de spool (`--spool-path`) {#spool-path-option---spool-path}

Chemin où les données transitoires sont stockées.

Ce chemin est utilisé pour stocker les données de la commande asynchrone `archive-push` et `archive-get`.

La commande asynchrone `archive-push` écrit des accusés de réception dans le répertoire de spool après avoir correctement stocké le WAL dans l'archive, ou une erreur en cas d'échec, afin que le processus au premier plan puisse informer rapidement PostgreSQL. Ces fichiers sont très petits : vides en cas de succès et de quelques centaines d'octets en cas d'erreur.

La commande asynchrone `archive-get` met en file d'attente les fichiers WAL dans le répertoire de spool afin de pouvoir les fournir très rapidement lorsque PostgreSQL les demande. Le déplacement des fichiers vers PostgreSQL est le plus efficace lorsque le répertoire de spool se trouve sur le même système de fichiers que `pg_xlog`/`pg_wal`. Toutefois, il n'est pas recommandé de placer le répertoire de spool *à l'intérieur* du répertoire `pg_xlog`/`pg_wal`, car cela pourrait entraîner des problèmes pour les utilitaires PostgreSQL tels que `pg_rewind`.

Les données stockées dans le chemin de spool ne sont pas strictement temporaires, car elles peuvent et doivent survivre à un redémarrage. Toutefois, leur perte n’est pas problématique. pgBackRest vérifiera simplement chaque segment WAL afin de s’assurer qu’il est correctement archivé pour `archive-push` et reconstruira la file d’attente pour `archive-get`.

Le chemin de spool est censé être situé sur un système de fichiers local compatible Posix, et non sur un système de fichiers distant tel que NFS ou CIFS.

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### Option de nombre de messages keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Nombre de messages keep-alive.

Spécifie le nombre de messages TCP keep-alive pouvant être perdus avant que la connexion ne soit considérée comme inactive.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPCNT`.

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### Option d'idle Keep Alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Délai d'inactivité pour le maintien de la connexion.

Spécifie la durée (en secondes) pendant laquelle aucune activité réseau ne se produit, après laquelle le système d'exploitation doit envoyer un message de maintien de connexion TCP.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPIDLE`.

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### Option Intervalle Keep Alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Intervalle de temps pour le maintien de la connexion active.

Spécifie la durée (en secondes) après laquelle un message TCP keep-alive non reconnu doit être renvoyé.

Cette option est disponible sur les systèmes qui prennent en charge l'option de socket `TCP_KEEPINTVL`.

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### Suites de chiffrement TLSv1.2 Option (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Suites de chiffrement TLSv1.2 autorisées.

Toutes les connexions TLS entre le client pgBackRest et le serveur sont chiffrées. Par défaut, les connexions aux magasins d'objets (par exemple S3) sont également chiffrées.

NOTE :

Le niveau de sécurité minimal absolu pour toute connexion de transport est TLSv1.2.

Les suites de chiffrement acceptées peuvent être ajustées si nécessaire. L'exemple proposé constitue un choix raisonnable sauf si des exigences de sécurité spécifiques s'appliquent. Si non définies (valeur par défaut), la valeur par défaut de la bibliothèque OpenSSL sous-jacente s'applique.

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Suites de chiffrement TLSv1.3 Option (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Suites de chiffrement TLSv1.3 autorisées.

Toutes les connexions TLS entre le client pgBackRest et le serveur sont chiffrées. Par défaut, les connexions aux magasins d'objets (par exemple S3) sont également chiffrées.

NOTE :

Le niveau de sécurité minimal absolu pour toute connexion de transport est TLSv1.2.

Les suites de chiffrement acceptées peuvent être ajustées si nécessaire. Si non définies (valeur par défaut), la valeur par défaut de la bibliothèque OpenSSL sous-jacente s'applique.

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## Options de journalisation {#log-options}

La section `log` définit les paramètres liés à la journalisation.

AVERTISSEMENT :

La journalisation au niveau trace peut exposer des secrets tels que des clés et des mots de passe. Utilisez avec précaution !

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

```text
default: warn
example: log-level-console=error
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

```text
default: info
example: log-level-file=debug
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

```text
default: off
example: log-level-stderr=error
```

### Option Chemin Journal (`--log-path`) {#log-path-option---log-path}

Chemin où les fichiers de journalisation sont stockés.

Le chemin de journalisation fournit un emplacement où pgBackRest peut stocker les fichiers de journalisation. Notez que si `log-level-file=off`, aucun chemin de journalisation n'est requis.

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### Option de journalisation des sous-processus (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Activer la journalisation dans les sous-processus.

Activez la journalisation des fichiers pour tout sous-processus créé par ce processus, en utilisant le niveau de journalisation spécifié par `log-level-file`.

```text
default: n
example: log-subprocess=y
```

### Option d'horodatage des journaux (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activer les horodatages dans la journalisation.

Active l’horodatage dans la journalisation console et fichier. Cette option est désactivée dans des situations spéciales, telles que la génération de documentation.

```text
default: y
example: log-timestamp=n
```

--------

## Options du mainteneur {#maintainer-options}

Les options du mainteneur sont destinées à prendre en charge les forks de PostgreSQL. Les paramètres appropriés doivent être déterminés par le mainteneur du fork, puis communiqués aux utilisateurs du fork.

AVERTISSEMENT :

Une utilisation incorrecte de ces options peut entraîner un comportement imprévu ou une corruption des données.

Il incombe au mainteneur du fork de tester pgBackRest avec les options requises. pgBackRest ne garantit la compatibilité avec aucun fork.

### Option de vérification des en-têtes WAL (`--archive-header-check`) {#check-wal-headers-option---archive-header-check}

Vérifier la version/id de PostgreSQL dans les en-têtes WAL.

Activée par défaut, cette option vérifie l’en-tête WAL contre la version de PostgreSQL et l’identifiant système afin de s’assurer que le WAL est copié dans la bonne stanza. Cela s’ajoute à la vérification de `pg_control` par rapport à la stanza et à la vérification que le WAL est copié à partir du même répertoire de données PostgreSQL où se trouve `pg_control`.

Par conséquent, désactiver cette vérification est relativement sûr, mais ne doit être effectué que lorsque c'est nécessaire, par exemple si le WAL est chiffré.

```text
default: y
example: archive-header-check=n
```

### Option de vérification de l’en-tête de page (`--page-header-check`) {#page-header-check-option---page-header-check}

Vérifier les en-têtes de page PostgreSQL.

Activée par défaut, cette option ajoute des vérifications d’en-tête de page.

La désactivation de cette option devrait être évitée sauf nécessité, par exemple si les pages sont chiffrées.

```text
default: y
example: page-header-check=n
```

### Option de version PostgreSQL obligatoire (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

Forcer la version de PostgreSQL.

La version de PostgreSQL spécifiée sera utilisée à la place de la version détectée automatiquement en lisant `pg_control` ou les en-têtes WAL. Cela est principalement utile pour les forks de PostgreSQL ou les versions de développement où ces valeurs diffèrent de la version de publication. La version rapportée par PostgreSQL via `server_version_num` doit correspondre à la version forcée.

AVERTISSEMENT :

Faites preuve de prudence en utilisant cette option, car `pg_control` et les en-têtes WAL seront toujours lus selon le format attendu pour la version spécifiée, c'est-à-dire le format issu de la version open-source officielle de PostgreSQL. Si la version fork ou développée modifie le format des champs sur lesquels pgBackRest dépend, cela entraînera un comportement imprévu. En général, cette option ne fonctionnera correctement que si le fork ajoute tous les membres de structure personnalisés *après* les membres standard de PostgreSQL.

```text
example: pg-version-force=15
```

--------

## Options du dépôt {#repository-options}

La section `repository` définit les options utilisées pour configurer le dépôt.

**Indexation** : Toutes les options `repo-` sont indexées afin de permettre la configuration de plusieurs dépôts. Par exemple, un seul dépôt est configuré à l’aide des options `repo1-path`, `repo1-host`, etc. Si plusieurs dépôts sont configurés et que l’option `--repo` n’est pas précisée pour une commande, les dépôts seront traités dans l’ordre de priorité décroissante (par exemple, repo1 puis repo2).

Les options `repo-retention-*` définissent la durée de rétention des sauvegardes. L'expiration n'a lieu qu'après que le nombre de sauvegardes complètes dépasse la rétention autorisée. Autrement dit, si `repo1-retention-full-type` est défini sur `count` (valeur par défaut) et que `repo1-retention-full` est défini sur 2, il doit y avoir 3 sauvegardes complètes avant que la plus ancienne ne soit expirée. Si `repo1-retention-full-type` est défini sur `time`, alors `repo1-retention-full` représente des jours, et il doit y avoir au moins autant de jours de sauvegardes complètes avant qu'une expiration ne puisse avoir lieu. Veillez toujours à disposer d'espace suffisant pour la rétention + 1 sauvegarde.

### Option de compte de dépôt Azure (`--repo-azure-account`) {#azure-repository-account-option---repo-azure-account}

Compte de dépôt Azure.

Compte Azure utilisé pour stocker le dépôt.

```text
example: repo1-azure-account=pg-backup
```

### Option de conteneur de dépôt Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Conteneur de dépôt Azure.

Conteneur Azure utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés dans la racine du conteneur en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par Azure dans le conteneur.

```text
example: repo1-azure-container=pg-backup
```

### Option de point de terminaison de dépôt Azure (`--repo-azure-endpoint`) {#azure-repository-endpoint-option---repo-azure-endpoint}

Point de terminaison du dépôt Azure.

Point de terminaison utilisé pour se connecter au service blob. La valeur par défaut est généralement correcte, sauf si vous utilisez Azure Government.

Pour les configurations personnalisées ou les tests, les options `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, et `repo-storage-verify-tls` peuvent être utiles.

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### Option de clé de dépôt Azure (`--repo-azure-key`) {#azure-repository-key-option---repo-azure-key}

Clé de dépôt Azure.

Une clé partagée ou une signature d'accès partagé, selon l'option `repo-azure-key-type`.

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### Type de clé du dépôt Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Type de clé du dépôt Azure.

Les types suivants sont pris en charge pour l'autorisation :

- `shared` - Clé partagée
- `sas` - Signature d'accès partagé
- `auto` - Autorisation automatique à l'aide d'identités managées Azure

```text
default: shared
example: repo1-azure-key-type=sas
```

### Option de style d'URI de dépôt Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Style URI Azure.

Les styles d'URI suivants sont pris en charge :

- `host` - Se connecter à l'hôte `account.endpoint`.
- `path` - Se connecter à l'hôte `endpoint` et préfixer le compte aux URI.

```text
default: host
example: repo1-azure-uri-style=path
```

### Option de sauvegarde incrémentielle par bloc (`--repo-block`) {#block-incremental-backup-option---repo-block}

Activez la sauvegarde incrémentielle par bloc.

Le mode incrémentiel par bloc permet des sauvegardes plus granulaires en divisant les fichiers en blocs pouvant être sauvegardés indépendamment. Cela permet d'économiser de l'espace dans le dépôt et peut améliorer les performances de restauration delta, car des blocs individuels peuvent être récupérés sans devoir lire entièrement le fichier depuis le dépôt.

NOTE :

L'option `repo-bundle` doit être activée avant que `repo-block` ne puisse l'être.

La taille des blocs d’un fichier est déterminée en fonction de sa taille et de son âge. En général, les fichiers plus anciens ou plus volumineux reçoivent des tailles de blocs plus grandes. Si un fichier est suffisamment ancien, il ne sera pas sauvegardé en utilisant l’incrémentation par bloc.

La sauvegarde incrémentielle par bloc est optimale lorsqu'elle est activée pour toutes les catégories de sauvegarde, y compris les sauvegardes complètes. Cela rend la sauvegarde complète légèrement plus grande, mais permet aux sauvegardes différentielles et incrémentielles ultérieures d'utiliser les cartes de blocs générées par la sauvegarde complète afin de réduire l'espace utilisé.

```text
default: n
example: repo1-block=y
```

### Option des paquets de dépôt (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

Regrouper les fichiers dans le dépôt.

Regrouper les petits fichiers afin de réduire le nombre total de fichiers écrits dans le dépôt. Écrire moins de fichiers est généralement plus efficace, en particulier sur les magasins d'objets tels que S3. En outre, les fichiers vides ne sont pas stockés, sauf dans le manifeste, ce qui économise du temps et de l'espace.

```text
default: n
example: repo1-bundle=y
```

### Option de limite du bundle de dépôt (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

Limite pour les paquets de fichiers.

Limite de taille pour les fichiers inclus dans les bundles. Les fichiers dont la taille dépasse cette limite seront stockés séparément.

Les fichiers intégrés ne peuvent pas être réutilisés lors d'une reprise d'une sauvegarde, donc cette option contrôle les fichiers pouvant être repris, c'est-à-dire que des valeurs plus élevées entraînent un nombre réduit de fichiers repris.

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### Option taille du bundle de dépôt (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

Taille cible pour les paquets de fichiers.

Définit la taille cible des fichiers ajoutés à un seul lot. La taille du lot non compressé peut atteindre `repo-bundle-size` + `repo-bundle-limit`, donc ne définissez pas cette option à la taille maximale autorisée par votre système de fichiers.

En général, il n'est pas recommandé de définir cette option trop élevée, car les réessais devront répéter l'intégralité du lot.

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### Option de phrase de passe du chiffrement du dépôt (`--repo-cipher-pass`) {#repository-cipher-passphrase-option---repo-cipher-pass}

Phrase de passe du chiffrement du dépôt.

Phrase de passe utilisée pour chiffrer/déchiffrer les fichiers du dépôt.

NOTE :

Lorsqu’elle est exécutée sans l’option `stanza`, la commande `info` lit les paramètres de chiffrement uniquement dans la section `global`. Si les paramètres de chiffrement sont configurés par stanza, exécutez la commande `info` avec l’option `stanza` pour lire une stanza chiffrée.

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### Type de chiffrement du dépôt (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Chiffrement utilisé pour chiffrer le dépôt.

Les types de chiffrement suivants sont pris en charge :

- `none` - Le dépôt n'est pas chiffré
- `aes-256-cbc` - Advanced Encryption Standard avec une longueur de clé de 256 bits

Notez que le chiffrement est toujours effectué côté client, même si le type de dépôt (par exemple S3) prend en charge le chiffrement.

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### Option de bucket de dépôt GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Bucket de dépôt GCS.

Bucket GCS utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés à la racine du bucket en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par GCS dans le bucket.

```text
example: repo1-gcs-bucket=/pg-backup
```

### Option de point de terminaison du dépôt GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Point de terminaison du dépôt GCS.

Point de terminaison utilisé pour se connecter au service de stockage. Peut être mis à jour pour utiliser un serveur local GCS ou un point d'accès alternatif.

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### Option de clé de dépôt GCS (`--repo-gcs-key`) {#gcs-repository-key-option---repo-gcs-key}

Clé du dépôt GCS.

Un jeton ou un fichier de clé de service, selon l'option `repo-gcs-key-type`.

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### Type de clé du dépôt GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Type de clé du dépôt GCS.

Les types suivants sont pris en charge pour l'autorisation :

- `auto` - Autoriser à l'aide du compte de service de l'instance.
- `service` - Compte de service à partir d'une clé stockée localement.
- `token` - À utiliser pour les tests locaux, par exemple `fakegcs`.

Lorsque `repo-gcs-key-type=service`, les identifiants seront rechargés lorsque le jeton d'authentification sera renouvelé.

```text
default: service
example: repo1-gcs-key-type=auto
```

### Option ID du projet du dépôt GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

Identifiant du projet GCS.

ID du projet GCS utilisé pour déterminer la facturation des requêtes.

```text
example: repo1-gcs-user-project=my-project
```

### Option de lien dur pour le dépôt (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

Crée des liens durs entre les fichiers des sauvegardes dans le dépôt.

Activez le lien dur des fichiers dans les sauvegardes différentielles et incrémentielles vers leurs sauvegardes complètes. Cela donne l'illusion qu'au niveau du système de fichiers, chaque sauvegarde est une sauvegarde complète. Faites attention toutefois, car la modification de fichiers liés par lien dur peut affecter toutes les sauvegardes de l'ensemble.

```text
default: n
example: repo1-hardlink=y
```

Nom obsolète : hardlink

### Option hôte du dépôt (`--repo-host`) {#repository-host-option---repo-host}

Hôte du dépôt lors de l'opération à distance.

Lors de la sauvegarde et de l'archivage vers un système de fichiers monté localement, ce paramètre n'est pas requis.

```text
example: repo1-host=repo1.domain.com
```

Nom obsolète : backup-host

### Option du fichier de l'autorité de certification hôte du dépôt (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Fichier de l'autorité de certification du serveur de dépôt.

Utilisez un fichier CA autre que celui par défaut du système pour vous connecter à l'hôte du dépôt.

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option Chemin de l'autorité de certification du dépôt (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Chemin de l'autorité de certification du serveur de dépôt.

Utilisez un chemin de certificat d'autorité (CA) autre que celui par défaut du système pour établir la connexion avec l'hôte du dépôt.

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### Option de fichier de certificat d'hôte du dépôt (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Fichier de certificat d'hôte du dépôt.

Envoyé à l'hôte du dépôt pour prouver l'identité du client.

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### Option de commande hôte du dépôt (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

Commande pgBackRest de l'hôte du dépôt.

Requis uniquement si le chemin vers la commande pgBackRest est différent sur les hôtes local et de dépôt. Si non défini, la commande de dépôt sera définie de la même manière que celle de l'hôte local.

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nom obsolète : backup-cmd

### Option de configuration de l'hôte du dépôt (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

Fichier de configuration du serveur de dépôt pgBackRest.

Spécifie l'emplacement du fichier de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le fichier de configuration de l'hôte du dépôt se trouve dans un emplacement différent du fichier de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nom obsolète : backup-config

### Option de chemin d'inclusion de configuration d'hôte de dépôt (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Chemin d'inclusion de la configuration de l'hôte du dépôt pgBackRest.

Définit l'emplacement du chemin d'inclusion de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le chemin d'inclusion de configuration de l'hôte du dépôt est différent du chemin d'inclusion de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Chemin de configuration de l'hôte du dépôt (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

Chemin de configuration du serveur de dépôt pgBackRest.

Définit l'emplacement du chemin de configuration sur l'hôte du dépôt. Cette option est nécessaire uniquement si le chemin de configuration de l'hôte du dépôt est différent du chemin de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### Option de fichier de clé hôte du dépôt (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Fichier de clé hôte du dépôt.

Vérifie que le certificat client a été envoyé par le propriétaire.

```text
example: repo1-host-key-file=/path/to/client.key
```

### Option de port hôte du dépôt (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Port de l'hôte du dépôt lorsque `repo-host` est défini.

Utilisez cette option pour spécifier un port non par défaut pour le protocole du serveur du dépôt.

NOTE :

Lorsque `repo-host-type=ssh`, il n'existe pas de valeur par défaut pour `repo-host-port`. Dans ce cas, le port sera celui configuré pour la commande spécifiée par `cmd-ssh`.

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

Nom obsolète : backup-ssh-port

### Type de protocole d'hôte de dépôt (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Type de protocole d'hôte de dépôt.

Les types de protocole suivants sont pris en charge :

- `ssh` - Shell sécurisé.
- `tls` - Serveur TLS pgBackRest.

```text
default: ssh
example: repo1-host-type=tls
```

### Option d'utilisateur hôte de dépôt (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Utilisateur hôte du dépôt lorsque `repo-host` est défini.

Définit l'utilisateur utilisé pour les opérations sur l'hôte du dépôt. Il est préférable que ce ne soit pas l'utilisateur `postgres`, mais plutôt un autre utilisateur tel que `pgbackrest`. Si PostgreSQL s'exécute sur l'hôte du dépôt, l'utilisateur `postgres` peut être ajouté au groupe `pgbackrest` afin d'avoir des permissions de lecture sur le dépôt sans pouvoir accidentellement le modifier.

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

Nom obsolète : backup-user

### Option Chemin du dépôt (`--repo-path`) {#repository-path-option---repo-path}

Chemin où les sauvegardes et l'archive sont stockées.

Le dépôt est l'emplacement où pgBackRest stocke les sauvegardes et les archives des segments WAL.

Il peut être difficile de prévoir à l’avance l’espace nécessaire. La meilleure approche consiste à effectuer quelques sauvegardes, puis à noter la taille des différents types de sauvegardes (pleines, incrémentielles, différentielles) et à mesurer la quantité de WAL générée par jour. Cela vous donnera une idée générale de l’espace requis, bien que les besoins évoluent probablement au fil du temps avec l’évolution de votre base de données.

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### Option de rétention des archives (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Nombre de sauvegardes couvertes par le WAL continu à conserver.

NOTE :

Les segments WAL nécessaires pour rendre une sauvegarde cohérente sont toujours conservés jusqu'à l'expiration de la sauvegarde, quelle que soit la configuration de cette option.

Si cette valeur n’est pas définie et que `repo-retention-full-type` est égal à `count` (valeur par défaut), alors l’archive à expirer sera par défaut celle correspondant à la valeur de `repo-retention-full` (ou `repo-retention-diff`) associée à `repo-retention-archive-type` si celle-ci est définie à `full` (ou `diff`). Cela garantira que les fichiers WAL ne seront supprimés que pour les sauvegardes déjà expirées. Si `repo-retention-full-type` est égal à `time`, alors cette valeur sera par défaut définie pour supprimer les archives antérieures à la plus ancienne sauvegarde complète conservée après avoir satisfait le paramètre `repo-retention-full`.

Cette option doit être définie si `repo-retention-archive-type` est réglé sur `incr`. Si l'espace disque est limité, ce paramètre, combiné à `repo-retention-archive-type`, peut être utilisé pour supprimer de manière agressive les segments WAL. Toutefois, cela annule la possibilité de réaliser une restauration à un instant donné à partir des sauvegardes ayant des segments WAL expirés, et n'est donc **pas** recommandé.

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

Nom obsolète : retention-archive

### Type de rétention des archives (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Type de sauvegarde pour la rétention de WAL.

Si défini sur `full`, pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes défini par `repo-retention-archive`. Si défini sur `diff` (différentiel), pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes et différentielles défini par `repo-retention-archive`, ce qui signifie qu'une sauvegarde complète prise en dernier sera comptée comme une sauvegarde différentielle pour l'application de la rétention du dépôt. Si défini sur `incr` (incrémentielle), pgBackRest conservera les journaux d'archive pendant le nombre de sauvegardes complètes, différentielles et incrémentielles défini par `repo-retention-archive`. Il est recommandé de ne pas modifier cette option par rapport à sa valeur par défaut, qui n'expire les WAL que conjointement à l'expiration des sauvegardes complètes.

```text
default: full
example: repo1-retention-archive-type=diff
```

Nom obsolète : retention-archive-type

### Option de rétention différentielle (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Nombre de sauvegardes différentielles à conserver.

Lorsqu'une sauvegarde différentielle expire, toutes les sauvegardes incrémentielles associées à cette sauvegarde différentielle expirent également. Si ce paramètre n'est pas défini, toutes les sauvegardes différentielles sont conservées jusqu'à l'expiration des sauvegardes complètes dont elles dépendent.

Notez que les sauvegardes complètes sont prises en compte dans le nombre de sauvegardes différentielles pour l'expiration. Cela réduit légèrement le nombre de sauvegardes différentielles à conserver dans la plupart des cas.

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

Nom obsolète : retention-diff

### Option de rétention complète (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Nombre ou durée de rétention des sauvegardes complètes.

Lorsqu'une sauvegarde complète expire, toutes les sauvegardes différentielles et incrémentielles associées à cette sauvegarde complète expirent également. Si l'option n'est pas définie, un avertissement est émis. Si une rétention indéfinie est souhaitée, définissez l'option à sa valeur maximale.

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

Nom obsolète : retention-full

### Type d'option de rétention complète (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Type de rétention pour les sauvegardes complètes.

Détermine si le paramètre `repo-retention-full` représente une période de temps (en jours) ou un nombre de sauvegardes complètes à conserver.

Si la valeur est définie à `time`, les sauvegardes complètes dont l'âge dépasse `repo-retention-full` seront supprimées du dépôt si au moins une autre sauvegarde a un âge supérieur ou égal au nombre de jours défini par `repo-retention-full`. Par exemple, si `repo-retention-full` est égal à 30 (jours) et qu'il existe 2 sauvegardes complètes : l'une âgée de 25 jours et l'autre de 35 jours, aucune sauvegarde complète ne sera expirée, car la suppression de la sauvegarde âgée de 35 jours laisserait uniquement la sauvegarde âgée de 25 jours, ce qui violerait la politique de rétention de 30 jours exigeant qu'au moins une sauvegarde ait au moins 30 jours d'âge avant qu'une sauvegarde plus ancienne ne puisse être expirée. Les archives WAL plus anciennes que la plus ancienne sauvegarde complète restante seront automatiquement expirées, sauf si `repo-retention-archive-type` et `repo-retention-archive` sont explicitement définis.

Si la valeur est définie à `count`, les sauvegardes complètes dont le nombre dépasse `repo-retention-full` seront supprimées. Par exemple, si `repo-retention-full` est égal à `4` et qu'une cinquième sauvegarde complète est effectuée, la sauvegarde complète la plus ancienne sera supprimée afin de maintenir le nombre à 4.

Notez qu'une sauvegarde ne sera prise en compte pour la rétention qu'après avoir été correctement terminée. Par exemple, si `repo-retention-full-type` est `count` et `repo-retention-full` est `2`, il doit y avoir 3 sauvegardes complètes avant que la plus ancienne ne soit supprimée.

```text
default: count
example: repo1-retention-full-type=time
```

### Option de rétention de l'historique des sauvegardes (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Nombre de jours d'historique de sauvegarde à conserver.

Une copie du manifeste de sauvegarde est stockée dans le chemin `backup.history` une fois la sauvegarde terminée. Par défaut, ces fichiers ne sont jamais supprimés, car ils sont utiles pour l'analyse de données, par exemple pour mesurer l'évolution de la taille des sauvegardes et des fichiers WAL au fil du temps.

Définissez `repo-retention-history` pour préciser le nombre de jours de manifestes d'historique de sauvegarde à conserver. Les sauvegardes non expirées sont toujours conservées dans l'historique des sauvegardes. Spécifiez `repo-retention-history=0` pour ne conserver l'historique des sauvegardes que pour les sauvegardes non expirées.

Lorsqu'un manifeste d'historique de sauvegarde complète est expiré, tous les manifestes d'historique de sauvegardes différentielles et incrémentielles associés à cette sauvegarde complète expirent également.

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### Option de bucket de dépôt S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

Bucket de dépôt S3.

Bucket S3 utilisé pour stocker le dépôt.

Les dépôts pgBackRest peuvent être stockés à la racine du bucket en définissant `repo-path=/`, mais il est généralement préférable de préciser un préfixe, tel que `/repo`, afin de pouvoir également stocker les journaux et d'autres contenus générés par AWS dans le bucket.

```text
example: repo1-s3-bucket=pg-backup
```

### Option de point de terminaison du dépôt S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

Point de terminaison du dépôt S3.

Le point de terminaison AWS doit être valide pour la région sélectionnée.

Pour les configurations personnalisées ou les tests, les options `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, et `repo-storage-verify-tls` peuvent être utiles.

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### Option de clé d'accès au dépôt S3 (`--repo-s3-key`) {#s3-repository-access-key-option---repo-s3-key}

Clé d'accès au dépôt S3.

Clé AWS utilisée pour accéder à ce bucket.

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### Clé secrète d'accès au dépôt S3 (`--repo-s3-key-secret`) {#s3-repository-secret-access-key-option---repo-s3-key-secret}

Clé secrète d'accès au dépôt S3.

Clé secrète AWS utilisée pour accéder à ce bucket.

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Type de clé du dépôt S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

Type de clé pour le dépôt S3.

Les types suivants sont pris en charge :

- `shared` - Clés partagées
- `auto` - Récupérer automatiquement les identifiants temporaires
- `web-id` - Récupérer automatiquement les identifiants d'identité web
- `pod-id` - Récupérer automatiquement les identifiants d'identité de pod EKS
- `process` - Récupérer les identifiants en exécutant un processus

```text
default: shared
example: repo1-s3-key-type=auto
```

### Option ID de clé KMS pour dépôt S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

Clé KMS du dépôt S3.

Active le chiffrement côté serveur S3 en utilisant la clé du service de gestion des clés AWS spécifiée.

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option de commande du processus d'authentification S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Commande du processus d'authentification S3.

Commande (et arguments facultatifs) à exécuter pour récupérer les identifiants temporaires S3. Le premier élément de la liste est la commande, les éléments suivants sont passés en tant que paramètres.

Le processus doit produire un JSON contenant les champs `AccessKeyId`, `SecretAccessKey`, `SessionToken` et `Expiration`. Les identifiants seront automatiquement actualisés avant l'expiration. Voir [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) pour les détails du format.

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### Option de région du dépôt S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

Région du dépôt S3.

La région AWS où le bucket a été créé.

```text
example: repo1-s3-region=us-east-1
```

### Option Requesteur Payant pour le dépôt S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Dépôt S3 avec paiement par le demandeur.

Active le paiement par le demandeur S3.

```text
default: n
example: repo1-s3-requester-pays=n
```

### Option de rôle du dépôt S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

Rôle du dépôt S3.

Le nom du rôle AWS (pas le nom ARN complet) utilisé pour récupérer les identifiants temporaires lorsque `repo-s3-key-type=auto`.

```text
example: repo1-s3-role=authrole
```

### Option de service de dépôt S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

Service de signature S3.

Le service de signature S3 utilisé dans l'authentification SigV4. La valeur par défaut est `s3` pour les points de terminaison S3 standards. À définir sur `s3-outposts` lors de l'utilisation d'un point de terminaison S3 Outposts.

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### Option de clé SSE du dépôt S3 (`--repo-s3-sse-customer-key`) {#s3-repository-sse-customer-key-option---repo-s3-sse-customer-key}

Clé SSE du client pour le dépôt S3.

Active le chiffrement côté serveur S3 en utilisant la clé cliente spécifiée.

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option de point de terminaison STS du dépôt S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

Point de terminaison STS du dépôt S3.

Point de terminaison STS utilisé pour récupérer des identifiants temporaires lorsque `repo-s3-key-type=web-id` est configuré. Définissez-le sur un point de terminaison régional (par exemple `sts.us-east-1.amazonaws.com`) pour utiliser STS régional, ce qui peut être nécessaire pour les régions GovCloud, Chine, ou pour réduire la latence.

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Option de jeton de sécurité du dépôt S3 (`--repo-s3-token`) {#s3-repository-security-token-option---repo-s3-token}

Jeton de sécurité du dépôt S3.

Jeton de sécurité AWS utilisé avec des identifiants temporaires.

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### Option de style d'URI de dépôt S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

Style d'URI S3.

Les styles d'URI suivants sont pris en charge :

- `host` - Se connecter à l'hôte `bucket.endpoint`.
- `path` - Se connecter à l'hôte `endpoint` et préfixer les URI par le bucket.

```text
default: host
example: repo1-s3-uri-style=path
```

### Option hôte du dépôt SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

Hôte du dépôt SFTP.

Hôte SFTP contenant le dépôt.

```text
example: repo1-sftp-host=sftprepo.domain
```

### Fingerprint de l'hôte du dépôt SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Empreinte de l'hôte du dépôt SFTP.

La génération de l'empreinte d'hôte du dépôt SFTP doit correspondre à `repo-sftp-host-key-hash-type`. Générez l'empreinte via `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. Les clés d'hôte SSH se trouvent normalement dans le répertoire `/etc/ssh`.

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Type d'option de vérification de la clé hôte SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Type de vérification de la clé hôte SFTP.

Les types de vérification de clé d'hôte SFTP suivants sont pris en charge :

- `strict` - pgBackRest n’ajoutera jamais automatiquement les clés d’hôte au fichier ~/.ssh/known_hosts, et refusera de se connecter aux hôtes dont la clé d’hôte a changé ou n’est pas trouvée dans les fichiers known hosts. Cette option oblige l’utilisateur à ajouter manuellement tous les nouveaux hôtes.
- `accept-new` - pgBackRest ajoutera automatiquement les nouvelles clés d’hôte au fichier known hosts de l’utilisateur, mais n’autorisera pas les connexions aux hôtes dont la clé d’hôte a changé.
- `fingerprint` - pgBackRest vérifiera la clé d’hôte contre l’empreinte spécifiée par l’option `repo-sftp-host-fingerprint`.
- `none` - aucune vérification de clé d’hôte ne sera effectuée.

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### Type de hachage de la clé hôte du dépôt SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Type de hachage de la clé d'hôte du dépôt SFTP.

Type de hachage de la clé hôte du dépôt SFTP. Déclare le type de hachage à utiliser pour calculer le hachage de la clé hôte du système distant au démarrage SSH. Les versions plus récentes de `libssh2` prennent en charge `sha256` en plus de md5 et sha1.

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### Option de port hôte du dépôt SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Port hôte du dépôt SFTP.

Port hôte du dépôt SFTP.

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### Option utilisateur hôte dépôt SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Utilisateur hôte du dépôt SFTP.

Utilisateur sur l'hôte utilisé pour stocker le dépôt.

```text
example: repo1-sftp-host-user=pg-backup
```

### Option fichier Hôtes SFTP connus (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Fichier d'hôtes SFTP connus.

Fichier known hosts à consulter pour rechercher une correspondance avec un hôte SFTP lors de l'authentification. Si non spécifié, pgBackRest recherchera par défaut dans `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` et `/etc/ssh/ssh_known_hosts2`. Si configuré avec un ou plusieurs chemins de fichier, pgBackRest recherchera dans ces fichiers une correspondance. Les chemins de fichier doivent être complets ou commencer par un tilde. L'option `repo-sftp-known-host` peut être spécifiée plusieurs fois pour indiquer plusieurs fichiers known hosts à consulter. Pour utiliser la vérification du fichier known hosts, l'option `repo-sftp-host-fingerprint` ne doit pas être définie. Voir également l'option `repo-sftp-host-check-type`.

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Option fichier de clé privée du dépôt SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Fichier de clé privée SFTP.

Fichier de clé privée SFTP utilisé pour l'authentification.

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Option de phrase de passe de clé privée du dépôt SFTP (`--repo-sftp-private-key-passphrase`) {#sftp-repository-private-key-passphrase-option---repo-sftp-private-key-passphrase}

Phrase de passe de la clé privée SFTP.

Phrase de passe utilisée pour accéder à la clé privée. Il s'agit d'une fonctionnalité facultative lors de la création d'une paire de clés SSH publique/privée.

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### Option de fichier de clé publique du dépôt SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Fichier de clé publique SFTP.

Fichier de clé publique SFTP utilisé pour l'authentification. Facultatif si compilé contre OpenSSL, obligatoire si compilé contre une autre bibliothèque.

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Option du fichier CA du dépôt de stockage (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

Fichier CA du stockage du dépôt.

Utilisez un fichier CA autre que celui par défaut du système pour les certificats du stockage (par exemple, S3, Azure).

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Noms obsolètes : repo-azure-ca-file, repo-s3-ca-file

### Option de chemin du certificat CA TLS pour le dépôt (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

Chemin CA du stockage du dépôt.

Utilisez un chemin de certificat d'autorité de certification (CA) autre que celui par défaut du système pour les certificats du stockage (par exemple, S3, Azure).

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

Noms obsolètes : repo-azure-ca-path, repo-s3-ca-path

### Option hôte de stockage du dépôt (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Hôte de stockage du dépôt.

Se connecter à un hôte autre que le point de terminaison de stockage (par exemple S3, Azure). Cela est généralement utilisé pour les tests.

```text
example: repo1-storage-host=127.0.0.1
```

Noms obsolètes : repo-azure-host, repo-s3-host

### Option de port du stockage du dépôt (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Port du stockage du dépôt.

Port à utiliser lors de la connexion au point de terminaison du stockage (par exemple S3, Azure) ou à l'hôte (le cas échéant).

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

Noms obsolètes : repo-azure-port, repo-s3-port

### Option d'étiquette de stockage du dépôt (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Étiquette(s) de stockage du dépôt.

Spécifiez les balises à ajouter aux objets lorsque le dépôt est un magasin d'objets (par exemple, S3). L'option peut être répétée pour ajouter plusieurs balises.

Il n'existe aucune fonctionnalité dans pgBackRest permettant de modifier ces balises ; veillez donc à les définir correctement avant d'exécuter `stanza-create` afin d'assurer une cohérence des balises dans l'ensemble du dépôt.

```text
example: repo1-storage-tag=key1=value1
```

### Option de taille de morceau de téléversement vers le dépôt (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Taille du morceau de téléversement vers le dépôt.

Les magasins d’objets tels que S3 permettent de téléverser des fichiers par morceaux lorsque le fichier est trop volumineux pour être stocké en mémoire. Même si le fichier peut être stocké en mémoire, il est plus efficace en mémoire de limiter la quantité de mémoire utilisée pour les téléversements.

Une taille de morceau plus élevée entraîne généralement de meilleures performances, car elle réduit le nombre de requêtes de téléversement et permet de téléverser plus de fichiers en une seule requête plutôt qu’en morceaux. Le désavantage est que la consommation mémoire sera plus élevée, et comme la mémoire tampon de morceau doit être allouée par processus, des valeurs plus élevées de `process-max` entraînent une consommation mémoire globale plus importante.

Notez que les tailles de morceau valides varient selon le type de stockage et la plateforme. Par exemple, AWS S3 impose une taille minimale de morceau de 5MiB. La terminologie relative à la taille du morceau varie selon le type de stockage ; utilisez donc « part size » pour AWS S3, « chunk size » pour GCS et « block size » pour Azure lorsque vous recherchez les valeurs minimales ou maximales.

Si un fichier est plus grand que 1GiB (la taille maximale que PostgreSQL crée par défaut), la taille de morceau sera augmentée progressivement jusqu'à la valeur maximale autorisée afin de terminer le téléversement du fichier.

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### Option de vérification du certificat de stockage du dépôt (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Vérification du certificat du dépôt de stockage.

Cette option permet d’activer/désactiver la vérification du certificat TLS du serveur de stockage (par exemple, S3, Azure). La désactivation ne doit être utilisée que pour des tests ou d’autres scénarios où un certificat a été auto-signé.

```text
default: y
example: repo1-storage-verify-tls=n
```

Noms obsolètes : repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Option de lien symbolique du dépôt (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Créez des liens symboliques dans le dépôt.

Active la création du `latest` et des liens symboliques de tablespace. Ces liens symboliques sont particulièrement utiles lors de la récupération in situ à l’aide de captures instantanées dans le dépôt, ce qui constitue un cas d’utilisation peu courant.

Bien que cette fonctionnalité soit probablement inutile pour la grande majorité des utilisateurs, elle reste activée par défaut pour des raisons de compatibilité avec les anciennes versions. Toutefois, il peut être utile de désactiver les liens symboliques pour les stockages de type Posix qui ne les prennent pas en charge.

```text
default: y
example: repo1-symlink=n
```

### Heure cible pour l'option dépôt (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

Heure cible pour le dépôt.

Le temps cible définit l'instant auquel les commandes lisent un dépôt sur un stockage versionné. Cela permet à la commande de lire le dépôt tel qu'il était à un instant donné, afin de récupérer des données supprimées ou corrompues par une erreur utilisateur ou un logiciel malveillant.

Le stockage versionné est pris en charge par S3, GCS et Azure, mais il est généralement désactivé par défaut. En plus d’activer le versioning, il peut être utile d’activer le verrouillage d’objets pour S3, ou la suppression réversible pour GCS ou Azure.

Lorsque l'option `repo-target-time` est spécifiée, l'option `repo` doit également être fournie. Il est probable que tous les types de dépôt ne prennent pas en charge le versioning, et il est généralement préférable de cibler un seul dépôt pour la récupération.

Notez que les comparaisons avec l'horodatage de stockage sont <= à l'horodatage fourni et que les millisecondes sont tronquées de l'horodatage lorsqu'elles sont fournies.

```text
example: repo-target-time=2024-08-08 12:12:12+00
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

Lorsqu’un montage NFS est utilisé comme dépôt `posix`, les mêmes règles s’appliquent à pgBackRest que celles décrites dans la documentation PostgreSQL : [Création d’un cluster de base de données - Systèmes de fichiers](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```text
default: posix
example: repo1-type=cifs
```

--------

## Options de restauration {#restore-options}

La section `restore` définit les paramètres utilisés pour la restauration des sauvegardes.

### Option Mode archive (`--archive-mode`) {#archive-mode-option---archive-mode}

Conserver ou désactiver l'archivage sur le cluster restauré.

Cette option permet de conserver ou de désactiver l'archivage sur un cluster restauré. Cela est utile lorsque le cluster doit être promu pour effectuer certaines opérations, mais n'est pas destiné à devenir le nouveau principal. Dans ce cas, il n'est pas recommandé d'envoyer les WAL depuis le cluster vers le dépôt.

Les modes suivants sont pris en charge :

- `off` - désactiver l'archivage en définissant `archive_mode=off`.
- `preserve` - conserver le paramètre `archive_mode` actuel.

**NOTE** : Cette option n'est pas disponible sous PostgreSQL < 12.

```text
default: preserve
example: archive-mode=off
```

### Option d'exclusion de base de données (`--db-exclude`) {#exclude-database-option---db-exclude}

Restauration en excluant les bases de données spécifiées.

Les bases de données exclues seront restaurées sous forme de fichiers creux, initialisés à zéro, afin d'économiser de l'espace, tout en permettant à PostgreSQL de réaliser la récupération. Après la récupération, ces bases de données ne seront pas accessibles, mais pourront être supprimées à l'aide de la commande `drop database`. L'option `--db-exclude` peut être spécifiée plusieurs fois afin de préciser plusieurs bases de données à exclure.

Lorsqu'elle est utilisée en combinaison avec l'option `--db-include`, `--db-exclude` ne s'applique qu'aux bases de données système standard (`template0`, `template1`, et `postgres`).

```text
example: db-exclude=db_main
```

### Option base de données incluse (`--db-include`) {#include-database-option---db-include}

Restauration uniquement des bases de données spécifiées.

Cette fonctionnalité permet de ne restaurer que les bases de données sélectionnées. Les bases de données non spécifiquement incluses seront restaurées sous forme de fichiers creux, initialisés à zéro, afin d'économiser de l'espace, tout en permettant à PostgreSQL de réaliser la récupération. Après la récupération, les bases de données non incluses ne seront pas accessibles, mais peuvent être supprimées à l’aide de la commande `drop database`.

NOTE :

Les bases de données intégrées (`template0`, `template1` et `postgres`) sont toujours restaurées, sauf exclusion explicite.

L'option `--db-include` peut être passée plusieurs fois pour spécifier plus d'une base de données à inclure.

Voir [Restauration de bases de données sélectionnées](/fr/docs/pgbackrest/user-guide/#restore-selected-databases) pour plus d'informations et de précautions.

```text
example: db-include=db_main
```

### Option Lier tout (`--link-all`) {#link-all-option---link-all}

Restaurez tous les liens symboliques.

Par défaut, les répertoires et fichiers liés par des liens symboliques sont restaurés en tant que répertoires et fichiers normaux dans $PGDATA. Cela est dû au fait qu’il peut ne pas être sécurisé de restaurer les liens symboliques vers leurs destinations d’origine sur un système différent de celui où la sauvegarde d’origine a été effectuée. Cette option restaure tous les liens symboliques exactement comme ils étaient sur le système d’origine où la sauvegarde a été effectuée.

```text
default: n
example: link-all=y
```

### Option de carte de lien (`--link-map`) {#link-map-option---link-map}

Modifier la destination d'un lien symbolique.

Permet de modifier le fichier ou le chemin de destination d'un lien symbolique lors d'une restauration. Cela est utile pour restaurer sur des systèmes ayant une disposition de stockage différente de celle du système d'origine où la sauvegarde a été générée.

```text
example: link-map=pg_xlog=/data/xlog
```

### Option de récupération (`--recovery-option`) {#recovery-option---recovery-option}

Définissez une option dans `postgresql.auto.conf` ou `recovery.conf`.

Consultez [Configuration du serveur](https://www.postgresql.org/docs/current/runtime-config.html) pour obtenir les détails sur les options `postgresql.auto.conf` ou `recovery.conf` (assurez-vous de sélectionner votre version de PostgreSQL). Cette option peut être utilisée plusieurs fois.

Pour PostgreSQL >= 12, les options seront écrites dans `postgresql.auto.conf`. Pour toutes les autres versions, les options seront écrites dans `recovery.conf`.

NOTE :

L'option `restore_command` sera générée automatiquement, mais peut être remplacée par cette option. Prenez garde à spécifier votre propre `restore_command`, car pgBackRest est conçu pour gérer cela à votre place. Les options de récupération cible (recovery_target_name, recovery_target_time, etc.) sont générées automatiquement par pgBackRest et ne doivent pas être définies avec cette option.

Comme pgBackRest ne démarre pas PostgreSQL après avoir écrit le fichier `postgresql.auto.conf` ou `recovery.conf`, il est toujours possible d’éditer/vérifier `postgresql.auto.conf` ou `recovery.conf` avant de redémarrer manuellement.

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### Option de carte des espaces de table (`--tablespace-map`) {#tablespace-map-option---tablespace-map}

Restaurez un tablespace dans le répertoire spécifié.

Déplace un tablespace vers un nouvel emplacement pendant la restauration. Cela est utile lorsque les emplacements des tablespaces ne sont pas identiques sur un réplica, ou qu’un système mis à jour dispose de points de montage différents.

Les emplacements des tablespaces ne sont pas stockés dans pg_tablespace, aussi peut-on les déplacer sans risque. Toutefois, déplacer un tablespace vers `data_directory` n'est pas recommandé et peut entraîner des problèmes. Pour en savoir plus sur le déplacement des tablespaces, http://www.databasesoup.com/2013/11/moving-tablespaces.html constitue une bonne ressource.

```text
example: tablespace-map=ts_01=/db/ts_01
```

### Option de mappage de tous les espaces de table (`--tablespace-map-all`) {#map-all-tablespaces-option---tablespace-map-all}

Restaurez tous les tablespace dans le répertoire spécifié.

Les espaces de table sont restaurés dans leurs emplacements d'origine par défaut. Ce comportement peut être modifié pour chaque espace de table grâce à l'option `tablespace-map`, mais il peut parfois être préférable de rediriger tous les espaces de table vers un nouveau répertoire d’un coup. Cela est particulièrement utile pour les systèmes de développement ou de préproduction qui peuvent ne pas avoir la même disposition de stockage que le système d’origine où la sauvegarde a été générée.

Le chemin spécifié sera le chemin parent utilisé pour créer tous les espaces de table dans la sauvegarde.

AVERTISSEMENT :

Les espaces de table créés après le début de la sauvegarde ne seront pas mappés. Effectuez une nouvelle sauvegarde après la création d'un espace de table si le mappage est requis.

```text
example: tablespace-map-all=/data/tablespace
```

--------

## Options serveur {#server-options}

La section `server` définit les options utilisées pour configurer le serveur TLS.

### Option d'adresse serveur TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

Adresse du serveur TLS.

Adresse IP sur laquelle le serveur écoute les requêtes clients.

```text
default: localhost
example: tls-server-address=*
```

### Option Clients autorisés du serveur TLS (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

Clients autorisés du serveur TLS.

Les clients sont autorisés sur le serveur en vérifiant leur certificat et en comparant leur CN (Nom commun) au moyen d'une liste configurée sur le serveur via l'option `tls-server-auth`.

Un client CN peut être autorisé pour autant de stanzas que nécessaire en fournissant une liste séparée par des virgules à l'option `tls-server-auth` ou pour toutes les stanzas en spécifiant `tls-server-auth=client-cn=*`. Les caractères génériques ne peuvent pas être utilisés pour le CN du client.

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### Option Autorités de certification du serveur TLS (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

Autorités de certification du certificat serveur TLS.

Vérifie que les certificats client sont signés par une autorité de certification de confiance.

```text
example: tls-server-ca-file=/path/to/server.ca
```

### Option de certificat serveur TLS (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

Fichier de certificat serveur TLS.

Envoyé au client pour indiquer l'identité du serveur.

```text
example: tls-server-cert-file=/path/to/server.crt
```

### Option de clé de serveur TLS (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

Fichier de clé du serveur TLS.

Vérifie que le certificat serveur a été envoyé par son propriétaire.

```text
example: tls-server-key-file=/path/to/server.key
```

### Option de port serveur TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

Port du serveur TLS.

Port sur lequel le serveur écoute les requêtes clients.

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## Options de stanza {#stanza-options}

Un stanza définit la configuration de sauvegarde pour un cluster de base de données PostgreSQL spécifique. La section stanza doit définir le chemin du cluster de base de données et l'hôte/utilisateur si le cluster de base de données est distant. En outre, toute section de configuration globale peut être remplacée afin de définir des paramètres spécifiques au stanza.

**Indexation** : Toutes les options `pg-` sont indexées afin de permettre la configuration de plusieurs hôtes PostgreSQL. Par exemple, un hôte principal unique est configuré à l'aide des options `pg1-path`, `pg1-port`, etc. Si un serveur de secours est configuré, indexez les options `pg-` sur l'hôte du dépôt sous la forme `pg2-` (par exemple, pg2-host, pg2-path, etc.).

### Option base de données PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

Base de données PostgreSQL.

Le nom de la base de données utilisé lors de la connexion à PostgreSQL. La valeur par défaut est généralement la meilleure option, mais certaines installations peuvent ne pas contenir cette base de données.

Notez que, pour des raisons historiques, le paramétrage de la variable d'environnement `PGDATABASE` sera ignoré.

```text
default: postgres
example: pg1-database=backupdb
```

### Option Hôte PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

Hôte PostgreSQL pour une opération à distance.

Utilisé pour les sauvegardes où l'hôte PostgreSQL est différent de l'hôte du dépôt.

```text
example: pg1-host=db.domain.com
```

Nom obsolète : db-host

### Option Fichier de l'Autorité de certification du serveur PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Fichier de l'autorité de certification du serveur PostgreSQL.

Utilisez un fichier CA autre que celui par défaut du système pour vous connecter à l'hôte PostgreSQL.

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option Chemin de l'Autorité de certification du serveur PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Chemin de l'autorité de certification du serveur PostgreSQL.

Utilisez un chemin de certificat d'autorité de certification (CA) autre que celui par défaut du système pour établir la connexion avec l'hôte PostgreSQL.

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### Option Fichier de certificat d'hôte PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Fichier de certificat d'hôte PostgreSQL.

Envoyé à l'hôte PostgreSQL pour prouver l'identité du client.

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### Option de commande hôte PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

Commande pgBackRest de l'hôte PostgreSQL.

Requis uniquement si le chemin vers la commande pgBackRest est différent sur les hôtes locaux et PostgreSQL. Si ce n'est pas défini, la commande sur l'hôte PostgreSQL sera définie de la même manière que celle sur l'hôte local.

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nom obsolète : db-cmd

### Option de configuration hôte PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

Fichier de configuration de l'hôte de base de données pgBackRest.

Spécifie l'emplacement du fichier de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le fichier de configuration PostgreSQL est situé à un emplacement différent du fichier de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nom obsolète : db-config

### Chemin d'inclusion de la configuration hôte PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Chemin d'inclusion de la configuration de l'hôte de base de données pgBackRest.

Définit l'emplacement du chemin d'inclusion de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le chemin d'inclusion de configuration PostgreSQL se trouve dans un emplacement différent du chemin d'inclusion de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option de chemin de configuration de l'hôte PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

Chemin de configuration de l'hôte de base de données pgBackRest.

Définit l'emplacement du chemin de configuration sur l'hôte PostgreSQL. Cette option est nécessaire uniquement si le chemin de configuration PostgreSQL se trouve dans un emplacement différent du chemin de configuration local.

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### Option fichier clé hôte PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Fichier de clé hôte PostgreSQL.

Vérifie que le certificat client a été envoyé par le propriétaire.

```text
example: pg1-host-key-file=/path/to/client.key
```

### Option Port hôte PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Port de l'hôte PostgreSQL lorsque `pg-host` est défini.

Utilisez cette option pour spécifier un port non par défaut pour le protocole d'hôte PostgreSQL.

NOTE :

Lorsque `pg-host-type=ssh`, il n'existe pas de valeur par défaut pour `pg-host-port`. Dans ce cas, le port sera celui configuré pour la commande spécifiée par `cmd-ssh`.

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

Nom obsolète : db-ssh-port

### Type de protocole d'hôte PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Type de protocole hôte PostgreSQL.

Les types de protocole suivants sont pris en charge :

- `ssh` - Shell sécurisé.
- `tls` - Serveur TLS pgBackRest.

```text
default: ssh
example: pg1-host-type=tls
```

### Option utilisateur hôte PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Utilisateur de connexion à l'hôte PostgreSQL lorsqu'`pg-host` est défini.

Cet utilisateur possédera également le processus pgBackRest distant et initiera les connexions à PostgreSQL. Pour que cela fonctionne correctement, l'utilisateur doit être le propriétaire du cluster de base de données PostgreSQL, ce qui correspond généralement à `postgres`, la valeur par défaut.

```text
default: postgres
example: pg1-host-user=db_owner
```

Nom obsolète : db-user

### Option Chemin PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

Répertoire de données PostgreSQL.

Il doit être identique à la valeur `data_directory` rapportée par PostgreSQL. Même si cette valeur peut être lue à divers endroits, il est prudent de la définir afin de garantir sa disponibilité en cas de restauration ou de sauvegarde hors ligne.

L'option `pg-path` est vérifiée par rapport à la valeur rapportée par PostgreSQL à chaque sauvegarde en ligne, elle doit donc toujours être à jour.

```text
example: pg1-path=/data/db
```

Nom obsolète : db-path

### Option de port PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

Port PostgreSQL.

Port sur lequel PostgreSQL est en cours d'exécution. Ce paramètre n'a généralement pas besoin d'être spécifié, car la plupart des clusters PostgreSQL s'exécutent sur le port par défaut.

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

Nom obsolète : db-port

### Option Chemin du socket PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Chemin du socket Unix de PostgreSQL.

Répertoire du socket Unix spécifié lors du démarrage de PostgreSQL. pgBackRest recherche automatiquement dans l'emplacement standard de votre système d'exploitation, aussi il est généralement inutile de préciser ce paramètre, sauf si le répertoire du socket a été explicitement modifié à l'aide du paramètre `unix_socket_directories` dans `postgresql.conf`.

```text
example: pg1-socket-path=/var/run/postgresql
```

Nom obsolète : db-socket-path

### Option utilisateur de base de données PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

Utilisateur de base de données PostgreSQL.

Le nom d'utilisateur de la base de données utilisé lors de la connexion à PostgreSQL. Si non spécifié, pgBackRest se connectera avec l'utilisateur système local ou `PGUSER`.

```text
example: pg1-user=backupuser
```
