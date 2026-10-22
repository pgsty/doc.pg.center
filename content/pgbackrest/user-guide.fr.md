---
title: "Guide utilisateur (Debian/Ubuntu)"
linkTitle: "Guide utilisateur (Deb)"
weight: 20
description: "Guide pas à pas d'installation et d'utilisation de pgBackRest pour les systèmes Debian et Ubuntu."
icon: fa-brands fa-ubuntu
module: [PGBACKREST]
categories: [Tutoriel]
upstream_link: "https://pgbackrest.org/user-guide.html"
---

--------

## Introduction {#introduction}

Ce guide utilisateur est conçu pour être suivi séquentiellement, du début à la fin — chaque section dépend de la précédente. Par exemple, la section [Restauration](#restore-1) repose sur la configuration effectuée dans la section [Démarrage rapide](#quick-start). Une fois pgBackRest en fonctionnement, il est possible de sauter des sections, mais il est recommandé de suivre le guide dans l’ordre lors de la première utilisation.

Bien que les exemples de ce guide soient destinés à Debian/Ubuntu et à PostgreSQL 17, il devrait être relativement facile de les appliquer à toute distribution Unix et toute version de PostgreSQL. Les seules commandes spécifiques au système d'exploitation sont celles permettant de créer, démarrer, arrêter et supprimer des clusters PostgreSQL. Les commandes pgBackRest seront identiques sur tout système Unix, bien que l'emplacement de l'exécutable puisse varier. Bien que pgBackRest cherche à fonctionner de manière cohérente sur les différentes versions de PostgreSQL, certaines différences subtiles entre versions de PostgreSQL peuvent apparaître dans ce guide lors de l'illustration de certains exemples, par exemple les chemins ou noms de fichiers de PostgreSQL, ainsi que les paramètres.

Les informations de configuration et la documentation pour PostgreSQL sont disponibles dans le [Manuel](http://www.postgresql.org/docs/17/static/index.html) de PostgreSQL.

Une approche quelque peu originale est adoptée pour la documentation dans ce guide utilisateur. Chaque commande est exécutée sur une machine virtuelle au moment où la documentation est générée à partir de la source XML. Cela signifie que vous pouvez avoir une confiance élevée quant au bon fonctionnement des commandes, dans l’ordre présenté. La sortie est capturée et affichée sous la commande lorsque cela est pertinent. Si la sortie n’est pas incluse, c’est parce qu’elle a été jugée sans intérêt ou qu’elle aurait pu distraire du récit.

Toutes les commandes doivent être exécutées en tant qu'utilisateur non privilégié disposant des droits sudo pour les utilisateurs `root` et `postgres`. Il est également possible d'exécuter les commandes directement en tant que leurs utilisateurs respectifs sans modification, auquel cas les commandes `sudo` peuvent être omises.


--------

## Concepts {#concepts}

Les concepts suivants sont définis en tant qu'ils sont pertinents pour pgBackRest, PostgreSQL et ce guide utilisateur.


### Sauvegarde {#backup}

Une sauvegarde est une copie cohérente d'un cluster de base de données pouvant être restaurée pour récupérer après une panne matérielle, effectuer une restauration à un instant donné ou mettre en place un serveur secondaire nouveau.

**Sauvegarde complète** : pgBackRest copie l’intégralité du contenu du cluster de base de données vers la sauvegarde. La première sauvegarde du cluster de base de données est toujours une sauvegarde complète. pgBackRest est toujours en mesure de restaurer directement une sauvegarde complète. La sauvegarde complète ne dépend d’aucun fichier en dehors d’elle-même pour assurer sa cohérence.

**Sauvegarde différentielle** : pgBackRest copie uniquement les fichiers du cluster de base de données modifiés depuis la dernière sauvegarde complète. Pour restaurer une sauvegarde différentielle, pgBackRest copie tous les fichiers de celle-ci ainsi que les fichiers inchangés requis de la sauvegarde complète précédente. Une sauvegarde différentielle occupe moins d'espace disque qu'une sauvegarde complète, mais elle et la sauvegarde complète doivent chacune être valides pour permettre la restauration.

**Sauvegarde incrémentielle** : pgBackRest copie uniquement les fichiers du cluster de base de données ayant changé depuis la dernière sauvegarde (qui peut être une autre sauvegarde incrémentielle, une sauvegarde différentielle ou une sauvegarde complète). Comme une sauvegarde incrémentielle ne comprend que les fichiers modifiés depuis la sauvegarde précédente, elle est généralement bien plus petite que les sauvegardes complètes ou différentielles. Comme pour la sauvegarde différentielle, la sauvegarde incrémentielle dépend d'autres sauvegardes pour être valide lors d'une restauration. Étant donné qu'une sauvegarde incrémentielle ne contient que les fichiers modifiés depuis la dernière sauvegarde, toutes les sauvegardes incrémentielles antérieures jusqu'à la dernière sauvegarde différentielle, la dernière sauvegarde différentielle et la dernière sauvegarde complète doivent être valides afin de pouvoir restaurer la sauvegarde incrémentielle. Si aucune sauvegarde différentielle n'existe, alors toutes les sauvegardes incrémentielles antérieures jusqu'à la dernière sauvegarde complète, qui doit exister, ainsi que la sauvegarde complète elle-même doivent être valides pour restaurer la sauvegarde incrémentielle.


### Restauration {#restore}

Une restauration est l'opération de copie d'une sauvegarde sur un système où elle sera lancée en tant que cluster de base de données en cours d'exécution. Une restauration nécessite les fichiers de sauvegarde et un ou plusieurs segments WAL afin de fonctionner correctement.


### Journaux d'écriture anticipée (WAL) {#write-ahead-log-wal}

Le WAL est le mécanisme utilisé par PostgreSQL pour garantir qu'aucun changement validé n'est perdu. Les transactions sont écrites séquentiellement dans le WAL, et une transaction est considérée comme validée lorsque ces écritures sont écrites sur le disque. Par la suite, un processus en arrière-plan écrit les modifications dans les fichiers du cluster de base de données principal (également appelés heap). En cas de panne, le WAL est rejoué afin de rendre la base de données cohérente.

Les journaux d'écriture (WAL) sont conceptuellement infinis, mais en pratique ils sont divisés en fichiers individuels de 16 Mo appelés segments. Les segments WAL suivent la convention de nommage `0000000100000A1E000000FE`, où les 8 premiers chiffres hexadécimaux représentent la timeline et les 16 chiffres suivants constituent le numéro de séquence logique (LSN).


### Chiffrement {#encryption}

Le chiffrement est le processus de conversion des données dans un format illisible à moins qu'un mot de passe approprié (appelé également phrase secrète) ne soit fourni.

pgBackRest chiffrera le dépôt en fonction d’un mot de passe fourni par l’utilisateur, empêchant ainsi tout accès non autorisé aux données stockées dans le dépôt.


--------

## Mise à jour de pgBackRest {#upgrading-pgbackrest}



### Mise à jour de pgBackRest de la version v2.x à la v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

La mise à niveau depuis la version v2.x vers la version v2.y est directe. Le format du dépôt n’a pas changé, aussi, pour la plupart des installations, il s’agit simplement d’installer les binaires de la nouvelle version. Il est également possible de revenir à une version antérieure si vous n’avez pas utilisé de fonctionnalités nouvelles non prises en charge par la version plus ancienne.

IMPORTANT :

Les versions locales et distantes de pgBackRest doivent correspondre exactement, elles doivent donc être mises à jour ensemble. En cas de désaccord, l'archivage des WAL et les sauvegardes ne fonctionneront pas jusqu'à ce que les versions soient synchronisées. Dans ce cas, l'erreur suivante sera signalée : `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.


--------

## Construction {#build}

Installer pgBackRest à partir d'un paquet est préférable à la compilation à partir des sources. Consultez [Installation](#installation) pour plus d'informations sur les paquets.

Lors de la compilation à partir des sources, il est préférable d'utiliser une machine de compilation plutôt que de compiler directement sur la production. La plupart des outils nécessaires à la compilation ne devraient généralement pas être installés en production. pgBackRest se compose d'un seul exécutable, ce qui facilite sa copie sur une nouvelle machine une fois compilé.

build **⇒** Télécharger la version `2.60.0` de pgBackRest vers le chemin `/build`

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.60.0/pgbackrest-2.60.0.tar.gz | \
       tar zx -C /build
```

build **⇒** Installer les dépendances de compilation

```bash
sudo apt-get install meson gcc libpq-dev libssl-dev libxml2-dev pkg-config \
       liblz4-dev libzstd-dev libbz2-dev libz-dev libssh2-1-dev libsystemd-dev
```

build **⇒** Configurer et compiler pgBackRest

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.60.0
ninja -C /build/pgbackrest
```

build **⇒** Exécuter éventuellement des tests de fumée pour vérifier que pgBackRest a été correctement construit

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               10.21s

Ok:                 1
       [filtered 6 lines of output]
```

--------

## Installation {#installation}

Un nouvel hôte nommé pg-primary est créé pour contenir le cluster de démonstration et exécuter les exemples pgBackRest.

Installer pgBackRest à partir d’un paquet est préférable à la compilation à partir des sources. Lors de l’installation à partir d’un paquet, les autres instructions de cette section sont généralement inutiles, mais il se peut qu’un paquet omette de créer un répertoire ou applique des permissions incorrectes. Dans ce cas, il peut être nécessaire de créer manuellement les répertoires ou de mettre à jour les permissions.

Les paquets Debian/Ubuntu pour pgBackRest sont disponibles sur [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si des paquets ne sont pas fournis pour votre distribution/version, vous pouvez [compiler à partir des sources](#build) puis procéder à l'installation manuelle comme indiqué ici.

pg-primary **⇒** Installer les dépendances

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-primary **⇒** Copier le binaire pgBackRest depuis l'hôte de compilation

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest nécessite des répertoires pour les journaux et la configuration, ainsi qu'un fichier de configuration.

pg-primary **⇒** Créer le fichier de configuration et les répertoires pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

pgBackRest doit maintenant être correctement installé, mais il est préférable de le vérifier. Si des dépendances ont été omises, une erreur sera générée lors de l'exécution de pgBackRest en ligne de commande.

pg-primary **⇒** Vérifiez que l'installation s'est déroulée correctement

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.60.0 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## Démarrage rapide {#quick-start}

La section Démarrage rapide abordera la configuration basique de pgBackRest et de PostgreSQL, et présentera les commandes `backup`, `restore` et `info`.


### Configurer un cluster de démonstration {#setup-demo-cluster}

La création du cluster de démonstration est facultative mais fortement recommandée, en particulier pour les nouveaux utilisateurs, car les commandes d'exemple du guide utilisateur font référence au cluster de démonstration ; les exemples supposent que le cluster de démonstration s'exécute sur le port par défaut (c’est-à-dire 5432). Le cluster ne sera pas lancé avant une section ultérieure, car il reste encore certaines configurations à effectuer.

pg-primary **⇒** Créer le cluster de démonstration

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 101:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

### Configurer une stanza de cluster {#configure-cluster-stanza}

Une stanza est la configuration d'un cluster de base de données PostgreSQL qui définit son emplacement, la manière dont il sera sauvegardé, les options d'archivage, etc. La plupart des serveurs de base de données n'ont qu'un seul cluster PostgreSQL et donc une seule stanza, tandis que les serveurs de sauvegarde ont une stanza pour chaque cluster de base de données à sauvegarder.

Il est tentant de nommer la stanza en fonction du cluster principal, mais un nom plus pertinent décrit les bases de données contenues dans le cluster. Étant donné que le nom de la stanza sera utilisé pour le principal et toutes les répliques, il est préférable de choisir un nom qui décrit la fonction réelle du cluster, par exemple app ou dw, plutôt que le nom local du cluster, comme main ou prod.

Le nom « demo » décrit avec précision le but de ce cluster, ce qui en fait également un bon nom de stanza.

pgBackRest doit connaître l'emplacement du répertoire de données de base du cluster PostgreSQL. Le chemin peut être demandé directement à PostgreSQL, mais dans un scénario de récupération, le processus PostgreSQL ne sera pas disponible. Lors des sauvegardes, la valeur fournie à pgBackRest sera comparée au chemin sur lequel PostgreSQL est en cours d'exécution, et elles doivent être identiques, sinon la sauvegarde retournera une erreur. Assurez-vous que `pg-path` est exactement égal à la valeur data_directory rapportée par PostgreSQL.

Par défaut, Debian/Ubuntu stocke les clusters dans `/var/lib/postgresql/[version]/[cluster]`, ce qui facilite la détermination du chemin correct du répertoire de données.

Lors de la création du fichier `/etc/pgbackrest/pgbackrest.conf`, le propriétaire de la base de données (généralement `postgres`) doit être autorisé en lecture.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer le répertoire de données du cluster PostgreSQL

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo
```

Les fichiers de configuration de pgBackRest suivent une convention semblable à celle des fichiers INI sous Windows. Les sections sont indiquées par du texte entre crochets, et les paires clé/valeur sont contenues dans chaque section. Les lignes commençant par `#` sont ignorées et peuvent être utilisées comme commentaires, mais les commentaires en fin de ligne suivant une valeur sur la même ligne ne sont pas pris en charge. Les guillemets ne sont pas pris en charge, et les espaces sont supprimés des clés et des valeurs. Les sections seront fusionnées si elles apparaissent plus d'une fois.

Il existe plusieurs façons de charger les fichiers de configuration de pgBackRest :

- `config` et `config-include-path` sont par défaut : le fichier de configuration par défaut sera chargé, s'il existe, et les fichiers `*.conf` dans le chemin d'inclusion de configuration par défaut seront ajoutés, s'ils existent.
- `config` est spécifié : seul le fichier de configuration indiqué sera chargé et doit exister.
- `config-include-path` est spécifié : les fichiers `*.conf` dans le chemin d'inclusion de configuration seront chargés et le chemin doit exister. Le fichier de configuration par défaut sera chargé s'il existe. Si l'on souhaite charger uniquement les fichiers dans le chemin d'inclusion de configuration spécifié, l'option `--no-config` peut également être passée.
- `config` et `config-include-path` sont spécifiés : en utilisant les valeurs spécifiées par l'utilisateur, le fichier de configuration sera chargé et les fichiers `*.conf` dans le chemin d'inclusion de configuration seront ajoutés. Les fichiers doivent exister.
- `config-path` est spécifié : ce paramètre remplacera le chemin de base pour l'emplacement par défaut du fichier de configuration et/ou le chemin de base du paramètre de chemin d'inclusion de configuration par défaut, sauf si l'option config et/ou config-include-path est explicitement définie.

Les fichiers sont concaténés comme s’ils formaient un seul grand fichier, et chaque fichier doit être valide individuellement. Cela signifie que les sections doivent être spécifiées dans chaque fichier là où elles sont nécessaires pour stocker une paire clé/valeur. L’ordre n’a pas d’importance, mais une priorité s’applique selon les sections. La priorité (de la plus élevée à la plus faible) est :

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

NOTE :

`--config`, `--config-include-path` et `--config-path` sont des options uniquement disponibles en ligne de commande.

pgBackRest peut également être configuré à l’aide de variables d’environnement (exemple ci-dessous) ; ces variables s’appliquent aux commandes telles que [backup](/fr/pgbackrest/command/backup/), [restore](/fr/pgbackrest/command/restore/) et [archive-push](/fr/pgbackrest/command/archive-push/).

pg-primary **⇒** Configurer `log-path` en utilisant l'environnement

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.60.0 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### Créer le dépôt {#create-the-repository}

Le dépôt est l'emplacement où pgBackRest stocke les sauvegardes et les archives des segments WAL.

Il peut être difficile de prévoir à l’avance l’espace nécessaire. La meilleure approche consiste à effectuer quelques sauvegardes, puis à noter la taille des différents types de sauvegardes (pleines, incrémentielles, différentielles) et à mesurer la quantité de WAL générée par jour. Cela vous donnera une idée générale de l’espace requis, bien que les besoins évoluent probablement au fil du temps avec l’évolution de votre base de données.

Pour cette démonstration, le dépôt sera stocké sur le même hôte que le serveur PostgreSQL. Il s'agit de la configuration la plus simple et elle est utile dans les cas où un logiciel de sauvegarde traditionnel est utilisé pour sauvegarder l'hôte de la base de données.

pg-primary **⇒** Créer le dépôt pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

Le chemin du dépôt doit être configuré afin que pgBackRest sache où le trouver.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez le chemin du dépôt pgBackRest

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-path=/var/lib/pgbackrest
```

Plusieurs dépôts peuvent également être configurés. Consultez [Dépôts multiples](#multiple-repositories) pour plus de détails.


### Configurer la sauvegarde archivée {#configure-archiving}

La sauvegarde d'un cluster PostgreSQL en cours d'exécution nécessite que l'archivage du WAL soit activé. `%p` est le mécanisme utilisé par PostgreSQL pour spécifier l'emplacement du segment WAL à archiver. Notez qu'au moins un segment WAL sera créé pendant le processus de sauvegarde, même si aucune écriture explicite n'est effectuée sur le cluster.

pg-primary:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurez les paramètres d'archive

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

Le cluster PostgreSQL doit être redémarré après avoir apporté ces modifications et avant d'effectuer une sauvegarde.

pg-primary **⇒** Redémarrer le cluster de démonstration

```bash
sudo pg_ctlcluster 17 demo restart
```

Le paramètre `hot_standby` est activé par défaut et doit rester ainsi sur chaque cluster. Un cluster peut être restauré ultérieurement en réplica, par exemple un principal reconstruit en réplica après une bascule, et un réplica n'acceptera pas de connexions en lecture seule sans ce paramètre.

Lorsqu’il est prévu qu’un segment WAL mette plus de 60 secondes (valeur par défaut) à atteindre le dépôt pgBackRest, l’option `archive-timeout` de pgBackRest doit être augmentée. Notez que cette option n’est pas identique à l’option archive_timeout de PostgreSQL, qui est utilisée pour forcer un basculement de segment WAL ; elle est utile pour les bases de données présentant des périodes prolongées d’inactivité. Pour plus d’informations sur l’option archive_timeout de PostgreSQL, consultez PostgreSQL [Write Ahead Log](https://www.postgresql.org/docs/current/static/runtime-config-wal.html).

La commande `archive-push` peut être configurée avec ses propres options. Par exemple, un niveau de compression plus faible peut être défini afin d'accélérer l'archivage sans affecter le niveau de compression utilisé pour les sauvegardes.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `archive-push` pour utiliser un niveau de compression plus faible

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-path=/var/lib/pgbackrest

[global:archive-push]
compress-level=3
```

Cette configuration technique peut être utilisée pour toute commande et peut même cibler une stanza spécifique, par exemple `demo:archive-push`.


### Configurer la rétention {#configure-retention}

pgBackRest expire les sauvegardes en fonction des options de rétention.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez la rétention à 2 sauvegardes complètes

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2

[global:archive-push]
compress-level=3
```

Plus d'informations sur la rétention sont disponibles dans la section [Retention](#retention).


### Configurer le chiffrement du dépôt {#configure-repository-encryption}

Le dépôt sera configuré avec un type de chiffrement et une clé afin de démontrer le chiffrement. Le chiffrement est toujours effectué côté client, même si le type de dépôt (par exemple S3 ou autre magasin d'objets) prend en charge le chiffrement.

Il est important d'utiliser une phrase secrète longue et aléatoire pour la clé de chiffrement. Une bonne manière de la générer consiste à exécuter : `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez le chiffrement du dépôt pgBackRest

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2

[global:archive-push]
compress-level=3
```

NOTE :

Les paramètres de chiffrement sont placés dans la section `[global]`, ci-dessus, afin que la commande `info` puisse lire toutes les stanzas. Sans l'option `stanza`, la commande `info` ne lit les paramètres de chiffrement que dans la section `[global]`, de sorte que les paramètres de chiffrement configurés par stanza nécessitent l'option `stanza` pour lire une stanza chiffrée.

Une fois que le dépôt a été configuré et que le stanza a été créé et vérifié, les paramètres de chiffrement du dépôt ne peuvent pas être modifiés.


### Créer la stanza {#create-the-stanza}

La commande `stanza-create` doit être exécutée pour initialiser la stanza. Il est recommandé d'exécuter la commande `check` après `stanza-create` afin de vérifier que l'archivage et les sauvegardes sont correctement configurés.

pg-primary **⇒** Créer la stanza et vérifier la configuration

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.60.0: --exec-id=417-1e9f3ac1 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### Vérifier la configuration {#check-the-configuration}

La commande `check` vérifie que pgBackRest et le paramètre archive_command sont correctement configurés pour l'archivage et les sauvegardes du stanza spécifié. Elle tente de vérifier tous les dépôts et bases de données configurés pour l'hôte sur lequel la commande est exécutée. Elle détecte les mauvaises configurations, en particulier celles relatives à l'archivage, qui entraînent des sauvegardes incomplètes car des segments WAL requis n'ont pas atteint l'archive. La commande peut être exécutée sur l'hôte PostgreSQL ou sur l'hôte dépôt. Elle peut également être exécutée sur l'hôte de secours, toutefois, comme les opérations `pg_switch_xlog()`/`pg_switch_wal()` ne peuvent pas être effectuées sur l'hôte de secours, la commande ne testera que la configuration du dépôt.

Notez que `pg_create_restore_point('pgBackRest Archive Check')` et `pg_switch_xlog()`/`pg_switch_wal()` sont appelés pour forcer PostgreSQL à archiver un segment WAL.

pg-primary **⇒** Vérifier la configuration

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.60.0: --exec-id=426-0731b746 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000100000000/000000010000000000000001-33f92705c1adbff8d478e7083380b65fcb876f1c.gz' on repo1
P00   INFO: check command end: completed successfully
```

### Optimisation des performances {#performance-tuning}

pgBackRest dispose de plusieurs options de performance qui ne sont pas activées par défaut afin de préserver la compatibilité descendante du dépôt. Toutefois, lors de la création d’un nouveau dépôt, les options suivantes sont recommandées. Elles peuvent également être utilisées sur un dépôt existant, à condition de noter que les versions plus anciennes de pgBackRest ne seront pas en mesure de lire le dépôt. Cette incompatibilité dépend de la date d’introduction de la fonctionnalité, comme indiqué dans la liste ci-dessous.

- `compress-type` - détermine l'algorithme de compression utilisé par les commandes `backup` et `archive-push`. La valeur par défaut est `gz` (Gzip), mais `zst` (Zstandard) est recommandé car il est bien plus rapide et offre une compression similaire à `gz`. `zst` est pris en charge par l'option `compress-type` depuis [v2.27](/fr/pgbackrest/release/#v227-release-notes). Voir [Type de compression](/fr/pgbackrest/configuration/#compress-type-option---compress-type) pour plus de détails.
- `repo-bundle` - combine les petits fichiers lors de la sauvegarde afin de économiser de l'espace et d'améliorer la vitesse des commandes `backup` et `restore`, notamment sur des magasins d'objets tels que S3. L'option `repo-bundle` a été introduite dans [v2.39](/fr/pgbackrest/release/#v239-release-notes). Voir [Regroupement de fichiers](#file-bundling) pour plus de détails.
- `repo-block` - stocke uniquement les parties des fichiers qui ont changé plutôt que le fichier entier lors des `diff`/`incr` `backup`. Cela permet d'économiser de l'espace et d'accroître la vitesse de la `backup`. L'option `repo-block` a été introduite dans [v2.46](/fr/pgbackrest/release/#v246-release-notes), mais une version d'au moins [v2.52.1](/fr/pgbackrest/release/#v2521-release-notes) est recommandée. Voir [Incrémentation par bloc](#block-incremental) pour plus de détails.

D'autres options de performance ne sont pas activées par défaut car elles nécessitent une configuration supplémentaire ou car la valeur par défaut est sûre (mais non optimale). Ces options sont disponibles dans toutes les versions v2 de pgBackRest.

- `process-max` - détermine le nombre de processus utilisés pour les commandes. La valeur par défaut est 1, qui est presque jamais appropriée. Chaque commande utilise `process-max` de manière différente ; reportez-vous à la documentation de chaque commande pour plus de détails sur son utilisation.
- `archive-async` - archive les fichiers WAL dans le dépôt par lots, ce qui accroît considérablement la vitesse d'archivage. Il n'est pas activé par défaut car il nécessite la création d'un chemin de spool. Consultez [Archivage asynchrone](#asynchronous-archiving) pour plus de détails.
- `backup-standby` - effectue la sauvegarde sur une instance secondaire plutôt que sur l'instance principale afin de réduire la charge sur cette dernière. Il n'est pas activé par défaut car il nécessite une configuration supplémentaire et la présence d'une ou plusieurs instances secondaires. Consultez [Sauvegarde depuis une instance secondaire](#backup-from-a-standby) pour plus de détails.


### Effectuer une sauvegarde {#perform-a-backup}

Par défaut, pgBackRest attend la prochaine vérification planifiée avant de démarrer une sauvegarde. Selon les paramètres checkpoint_timeout et checkpoint_segments dans PostgreSQL, il peut s’écouler assez de temps avant qu’une vérification ne soit terminée et que la sauvegarde puisse commencer. En général, il est préférable de définir `start-fast=y` afin que la sauvegarde démarre immédiatement. Cela force une vérification, mais comme les sauvegardes sont généralement exécutées une fois par jour, une vérification supplémentaire n’a pas d’impact notable sur les performances. Toutefois, sur des clusters très chargés, il peut être préférable de passer `--start-fast` en ligne de commande au besoin.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer le démarrage rapide de la sauvegarde

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y

[global:archive-push]
compress-level=3
```

Pour effectuer une sauvegarde du cluster PostgreSQL, exécutez pgBackRest avec la commande `backup`.

pg-primary **⇒** Effectuer une sauvegarde du cluster de démonstration

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.60.0: --exec-id=453-1927d312 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261015-070743F
P00   INFO: full backup size = 22.1MB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=453-1927d312 --log-level-console=info --no-log-timestamp --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Par défaut, pgBackRest tente d'exécuter une sauvegarde incrémentielle. Toutefois, une sauvegarde incrémentielle doit être basée sur une sauvegarde complète, et comme aucune sauvegarde complète n'existait, pgBackRest a exécuté une sauvegarde complète à la place.

L'option `type` peut être utilisée pour spécifier une sauvegarde complète ou une sauvegarde différentielle.

pg-primary **⇒** Sauvegarde différentielle du cluster demo

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261015-070743F_20261015-070745D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=480-1ccf1661 --log-level-console=info --no-log-timestamp --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Cette fois-ci, aucun avertissement n’a été affiché car une sauvegarde complète existait déjà. Bien qu’une sauvegarde incrémentielle puisse être basée sur une sauvegarde complète *ou* une sauvegarde différentielle, une sauvegarde différentielle doit obligatoirement être basée sur une sauvegarde complète. Une sauvegarde complète peut être effectuée en exécutant la commande `backup` avec `--type=full`.

Pendant une sauvegarde en ligne, pgBackRest attend que les segments WAL nécessaires à la cohérence de la sauvegarde soient archivés. Cette durée d'attente est régulée par l'option pgBackRest `archive-timeout` qui vaut 60 secondes par défaut. Si l'archivage d'un segment individuel est connu pour prendre plus de temps, cette option doit être augmentée.


### Planifier une sauvegarde {#schedule-a-backup}

Les sauvegardes peuvent être planifiées à l'aide d'utilitaires tels que cron.

Dans l'exemple suivant, deux tâches cron sont configurées pour s'exécuter ; les sauvegardes complètes sont planifiées à 6 h 30 tous les dimanches, tandis que les sauvegardes différentielles sont planifiées à 6 h 30 du lundi au samedi. Si ce fichier crontab est installé pour la première fois en milieu de semaine, pgBackRest exécutera une sauvegarde complète lors de la première exécution de la tâche différentielle, suivie d'une sauvegarde différentielle le lendemain.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

Une fois les sauvegardes planifiées, il est important de configurer la rétention afin que les sauvegardes soient expirées selon un calendrier régulier, voir [Retention](#retention).


### Informations de sauvegarde {#backup-information}

Utilisez la commande `info` pour obtenir des informations sur les sauvegardes.

pg-primary **⇒** Obtenir les informations sur le cluster de démonstration

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000010000000000000001/000000010000000000000005

        full backup: 20261015-070743F
            timestamp start/stop: 2026-10-15 07:07:43+00 / 2026-10-15 07:07:45+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 22.1MB, database backup size: 22.1MB
            repo1: backup set size: 2.9MB, backup size: 2.9MB

        diff backup: 20261015-070743F_20261015-070745D
            timestamp start/stop: 2026-10-15 07:07:45+00 / 2026-10-15 07:07:46+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 22.1MB, database backup size: 8.3KB
            repo1: backup set size: 2.9MB, backup size: 448B
            backup reference total: 1 full
```

La commande `info` s'applique à une seule stanza ou à toutes les stanzas. La sortie texte est la valeur par défaut et fournit un résumé lisible par l'humain des sauvegardes pour la ou les stanzas demandées. Ce format peut évoluer à tout moment dans une version.

Pour une sortie lisible par machine, utilisez `--output=json`. La sortie JSON contient bien plus d'informations que la sortie texte et est maintenue stable, sauf en cas de bug.

Pour accélérer l'exécution, restreindre la sortie à l'information de progression uniquement en spécifiant `--detail-level=progress`. Notez que cela ignore toutes les vérifications sauf la disponibilité de la stanza.

Chaque stanza dispose d'une section distincte et il est possible de limiter la sortie à une seule stanza à l'aide de l'option `--stanza`. La stanza '`status`' indique brièvement l'état de santé de la stanza. Si cette valeur est '`ok`', pgBackRest fonctionne normalement. Si plusieurs dépôts sont configurés, une valeur de '`mixed`' indique que la stanza n'est pas dans un état sain sur un ou plusieurs dépôts ; dans ce cas, l'état de la stanza sera détaillé par dépôt. Dans les cas où une erreur s'est produite sur un dépôt sans correspondre à un code d'erreur connu, un code d'erreur de '`other`' sera utilisé et les détails complets de l'erreur seront fournis. La '`wal archive min/max`' affiche le WAL minimum et maximum actuellement stockés dans l'archive et, dans le cas de plusieurs dépôts, sera rapportée sur l'ensemble des dépôts sauf si l'option `--repo` est définie. Notez qu'il peut y avoir des lacunes dues aux politiques de rétention des archives ou à d'autres raisons.

Les messages '`backup/expire running`' et/ou '`restore running`' s'affichent aux côtés des informations '`status`' si l'une quelconque de ces commandes est actuellement en cours d'exécution sur l'hôte. La progression par répertoire sera également indiquée dans la sortie texte, et un tableau '`repo`' sera inclus dans la sortie JSON.

Les sauvegardes sont affichées du plus ancien au plus récent. La sauvegarde la plus ancienne sera *toujours* une sauvegarde complète (indiquée par un `F` à la fin de l'étiquette), mais la sauvegarde la plus récente peut être complète, différentielle (se terminant par `D`) ou incrémentielle (se terminant par `I`).

Le '`timestamp start/stop`' définit la période pendant laquelle la sauvegarde a été exécutée. Le '`timestamp stop`' peut être utilisé pour déterminer la sauvegarde à utiliser lors d'une restauration à un instant donné. Plus d'informations sur la restauration à un instant donné sont disponibles dans la section [Restauration à un instant donné](#point-in-time-recovery).

Le '`wal start/stop`' définit la plage de WAL nécessaire pour rendre la base de données cohérente lors d'une restauration. La commande `backup` s'assurera que cette plage de WAL se trouve dans l'archive avant de se terminer.

La '`database size`' correspond à la taille totale non compressée de la base de données, tandis que la '`database backup size`' représente la quantité de données à sauvegarder réellement ; elles sont identiques pour les sauvegardes complètes.

Le '`repo`' indique dans quel dépôt se trouve cette sauvegarde. Le '`backup set size`' inclut tous les fichiers de cette sauvegarde ainsi que toutes les sauvegardes référencées dans le dépôt nécessaires à la restauration de la base de données à partir de cette sauvegarde, tandis que le '`backup size`' inclut uniquement les fichiers de cette sauvegarde (ceux-ci seront également identiques pour les sauvegardes complètes). Les tailles des dépôts reflètent les tailles des fichiers compressés si la compression est activée dans pgBackRest.

Le '`backup reference total`' résume la liste des sauvegardes supplémentaires nécessaires pour effectuer la restauration de cette sauvegarde. Utilisez l'option `--set` pour afficher la liste complète de référence.


### Restaurer une sauvegarde {#restore-a-backup}

Les sauvegardes peuvent vous protéger contre plusieurs scénarios de catastrophe, dont les plus fréquents sont les pannes matérielles et la corruption des données. La méthode la plus simple pour simuler une corruption de données consiste à supprimer un fichier important du cluster PostgreSQL.

pg-primary **⇒** Arrêtez le cluster de démonstration et supprimez le fichier `pg_control`

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres rm /var/lib/postgresql/17/demo/global/pg_control
```

Le démarrage du cluster sans ce fichier important entraînera une erreur.

pg-primary **⇒** Tentative de démarrage du cluster démo corrompu

```bash
sudo pg_ctlcluster 17 demo start
```

```text
Error: /usr/lib/postgresql/17/bin/pg_ctl /usr/lib/postgresql/17/bin/pg_ctl start -D /var/lib/postgresql/17/demo -l /var/log/postgresql/postgresql-17-demo.log -s -o  -c config_file="/etc/postgresql/17/demo/postgresql.conf"  exited with status 1:
postgres: could not find the database system
Expected to find it in the directory "/var/lib/postgresql/17/demo",
but could not open file "/var/lib/postgresql/17/demo/global/pg_control": No such file or directory
       [filtered 2 lines of output]
```

Pour restaurer une sauvegarde du cluster PostgreSQL, exécutez pgBackRest avec la commande `restore`. Le cluster doit être arrêté (dans ce cas, il est déjà arrêté) et tous les fichiers doivent être supprimés du répertoire de données PostgreSQL.

pg-primary **⇒** Supprimer les anciens fichiers du cluster de démonstration

```bash
sudo -u postgres find /var/lib/postgresql/17/demo -mindepth 1 -delete
```

pg-primary **⇒** Effectuer la restauration du cluster de démonstration et démarrer PostgreSQL

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo pg_ctlcluster 17 demo start
```

Cette fois, le cluster a démarré correctement car la restauration a remplacé le fichier `pg_control` manquant.

Plus d'informations sur la commande `restore` sont disponibles dans la section [Restauration](#restore-1).


--------

## Surveillance {#monitoring}

La surveillance est une composante essentielle de tout système de production. De nombreux outils sont disponibles, et pgBackRest peut être surveillé sur l’un d’entre eux avec un peu d’effort.

pgBackRest peut produire des informations sur le dépôt au format JSON, qui inclut la liste de toutes les sauvegardes pour chaque stanza ainsi que les informations sur l'archive WAL.


### En PostgreSQL {#in-postgresql}

La commande PostgreSQL `COPY` permet de charger les informations de pgBackRest dans une table. L'exemple suivant encapsule cette logique dans une fonction pouvant être utilisée pour effectuer des requêtes en temps réel.

pg-primary **⇒** Charger la fonction d'information pgBackRest pour PostgreSQL

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

À présent, la fonction `monitor.pgbackrest_info()` peut être utilisée pour déterminer l’heure de la dernière sauvegarde réussie et le WAL archivé pour une stanza.

pg-primary **⇒** Interroger l'heure de la dernière sauvegarde réussie et des journaux WAL archivés

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-15 07:07:46+00 | 000000010000000000000005
(1 row)
```

### Utilisation de jq {#using-jq}

jq est un utilitaire en ligne de commande permettant d'extraire facilement des données depuis des fichiers JSON.

pg-primary **⇒** Installer l'utilitaire jq

```bash
sudo apt-get install jq
```

À présent, jq peut être utilisé pour interroger l'heure de la dernière sauvegarde réussie pour un stanza.

pg-primary **⇒** Requête le moment de la dernière sauvegarde réussie

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .backup[-1] | .timestamp.stop'
```

```text
1792048066
```

Ou le dernier WAL archivé.

pg-primary **⇒** Requête du dernier WAL archivé

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .archive[-1] | .max'
```

```text
"000000010000000000000005"
```

NOTE :

Cette syntaxe nécessite jq v1.5.

NOTE :

jq peut arrondir des nombres élevés tels que les identifiants système. Testez vos requêtes avec soin.


--------

## Sauvegarde {#backup-1}

Lorsque plusieurs dépôts sont configurés, pgBackRest effectuera la sauvegarde vers le dépôt de priorité la plus élevée (par exemple `repo1`) sauf si l'option `--repo` est spécifiée.

pgBackRest ne dispose pas de planificateur intégré, il est donc préférable de l'exécuter depuis cron ou un autre mécanisme de planification.

Consultez [Effectuer une sauvegarde](#perform-a-backup) pour plus de détails et d'exemples.


### Regroupement de fichiers {#file-bundling}

Regrouper les fichiers dans le dépôt permet de gagner du temps lors de la sauvegarde et de libérer de l’espace dans le dépôt. Cet avantage est particulièrement marqué lorsque le dépôt est stocké sur un magasin d’objets comme S3 ou sur des systèmes de fichiers à grandes tailles de bloc. Le temps de création par fichier est plus élevé sur les magasins d’objets, et des fichiers très petits peuvent coûter autant à stocker qu’un fichier plus volumineux.

La fonctionnalité de regroupement de fichiers est activée avec l'option `repo-bundle`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `repo1-bundle`

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y

[global:archive-push]
compress-level=3
```

Une sauvegarde complète sans regroupement de fichiers comportera plus de 1000 fichiers dans le chemin de sauvegarde, mais avec le regroupement, le nombre total de fichiers est fortement réduit. Un avantage supplémentaire est que les fichiers de taille nulle ne sont pas stockés (sauf dans le manifeste), contrairement à une sauvegarde normale où chaque fichier de taille nulle est stocké individuellement.

pg-primary **⇒** Effectuer une sauvegarde complète

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** Vérifier le total des fichiers

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

Les options `repo-bundle-size` et `repo-bundle-limit` peuvent être utilisées pour le réglage, bien que les valeurs par défaut soient optimales dans la plupart des cas.

Bien que le regroupement de fichiers soit généralement plus efficace, le désavantage réside dans la difficulté d'accès manuel aux fichiers depuis le dépôt. Il peut ne pas être adapté aux stockages à déduplication, car chaque sauvegarde complète organise les fichiers dans les paquets de manière différente. Enfin, les paquets de fichiers ne peuvent pas être repris, veillez donc à ne pas définir `repo-bundle-limit` trop élevé.


### Incrémentation par bloc {#block-incremental}

Les sauvegardes incrémentielles par bloc économisent de l’espace en ne stockant que les parties d’un fichier modifiées depuis la sauvegarde précédente, plutôt que le fichier entier.

La fonctionnalité de sauvegarde incrémentielle par bloc est activée avec l'option `repo-block` et fonctionne de manière optimale lorsqu'elle est activée pour tous les types de sauvegarde. Le regroupement des fichiers doit également être activé.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `repo1-block`

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y

[global:archive-push]
compress-level=3
```

### Annotations de sauvegarde {#backup-annotations}

Les utilisateurs peuvent attacher des paires clé/valeur explicatives à la sauvegarde. Cette option peut être utilisée plusieurs fois pour attacher plusieurs annotations.

pg-primary **⇒** Effectuer une sauvegarde complète avec annotations

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

Les annotations sont produites par la sortie texte de la commande `info` lorsque une sauvegarde est spécifiée avec `--set`, et apparaissent toujours dans la sortie JSON.

pg-primary **⇒** Obtenir les informations sur le cluster de démonstration

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261015-070756F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261015-070756F
            timestamp start/stop: 2026-10-15 07:07:56+00 / 2026-10-15 07:07:57+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22.1MB, database backup size: 22.1MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                key: value
                source: demo backup
```

Les annotations incluses avec la commande `backup` peuvent être ajoutées, modifiées ou supprimées ultérieurement à l'aide de la commande `annotate`.

pg-primary **⇒** Modifier les annotations de sauvegarde

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261015-070756F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261015-070756F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261015-070756F
            timestamp start/stop: 2026-10-15 07:07:56+00 / 2026-10-15 07:07:57+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22.1MB, database backup size: 22.1MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## Rétention {#retention}

En général, il est préférable de conserver autant de sauvegardes que possible afin de disposer d'une fenêtre plus étendue pour la [restauration à un instant donné](#point-in-time-recovery), mais des contraintes pratiques telles que l'espace disque doivent également être prises en compte. Les options de rétention suppriment automatiquement les sauvegardes anciennes une fois qu'elles ne sont plus nécessaires.

pgBackRest effectue la rotation des sauvegardes complètes selon le type de rétention, qui peut être défini par un nombre ou une période de temps. Lorsqu’un nombre est spécifié, l’expiration n’est pas liée à la date de création des sauvegardes, mais au nombre de sauvegardes à conserver. Les sauvegardes différentielles sont basées sur un nombre, mais sont toujours expirées lorsque la sauvegarde complète dont elles dépendent l’est. Les sauvegardes incrémentielles ne sont pas expirées indépendamment par rétention — elles sont toujours expirées en même temps que leur sauvegarde complète ou différentielle associée. Pour plus de détails et des exemples, reportez-vous aux sections [Rétention des sauvegardes complètes](#full-backup-retention) et [Rétention des sauvegardes différentielles](#differential-backup-retention).

L'archive WAL est conservée par défaut pour les sauvegardes n'ayant pas expiré, mais, bien que non recommandé, ce délai peut être modifié par dépôt à l'aide de l'option retention-archive. Voir la section [Rétention des archives](#archive-retention) pour les détails et exemples.

La commande `expire` s'exécute automatiquement après chaque sauvegarde réussie et peut également être exécutée par l'utilisateur. Lorsqu'elle est exécutée par l'utilisateur, l'expiration s'effectue selon les paramètres de rétention définis pour chaque dépôt configuré. Si l'option `--repo` est fournie, l'expiration s'applique uniquement au dépôt spécifié. L'expiration peut également être limitée par l'utilisateur à un jeu de sauvegarde spécifique à l'aide de l'option `--set`, et, sauf si l'option `--repo` est spécifiée, tous les dépôts seront recherchés et tous ceux correspondant aux critères seront supprimés. Il convient de noter que la planification de rétention des archives sera vérifiée et appliquée chaque fois que la commande `expire` est exécutée.


### Rétention des sauvegardes complètes {#full-backup-retention}

L'option `repo1-retention-full-type` détermine la manière dont l'option `repo1-retention-full` est interprétée : soit comme le nombre de sauvegardes complètes à conserver, soit comme le nombre de jours pendant lesquels conserver les sauvegardes complètes. Une nouvelle sauvegarde doit être terminée avant qu'une expiration ne puisse se produire — cela signifie que si `repo1-retention-full-type=count` et `repo1-retention-full=2`, alors trois sauvegardes complètes seront conservées avant que la plus ancienne ne soit supprimée, ou que si `repo1-retention-full-type=time` et `repo1-retention-full=20`, alors une sauvegarde complète d'au moins 20 jours d'âge doit exister avant qu'une expiration ne puisse avoir lieu.

`repo1-retention-full=2` a été défini dans [Configurer la rétention](#configure-retention), mais il n'existe actuellement qu'une seule sauvegarde complète ; la prochaine sauvegarde complète n'expirera donc aucune sauvegarde complète.

pg-primary **⇒** Effectuer une sauvegarde complète

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 975 lines of output]
P00   INFO: repo1: remove expired backup 20261015-070753F
P00 DETAIL: repo1: 17-1 archive retention on backup 20261015-070756F, start = 000000020000000000000008
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

L'archive *est* expirée car des segments WAL ont été générés avant la sauvegarde la plus ancienne. Ces segments ne sont pas utiles pour la récupération — seuls les segments WAL générés après une sauvegarde peuvent être utilisés pour récupérer cette sauvegarde.

pg-primary **⇒** Effectuer une sauvegarde complète

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261015-070756F
P00   INFO: repo1: remove expired backup 20261015-070756F
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000008, stop = 000000020000000000000009
P00   INFO: expire command end: completed successfully
```

La sauvegarde complète `20261015-070743F` a expiré et la rétention des archives est basée sur `20261015-070758F`, qui est désormais la sauvegarde complète la plus ancienne.


### Rétention des sauvegardes différentielles {#differential-backup-retention}

Définissez `repo1-retention-diff` sur le nombre de sauvegardes différentielles requises. Les sauvegardes différentielles ne dépendent que de la dernière sauvegarde complète, il est donc possible de créer un ensemble « en rouleau » de sauvegardes différentielles pour la dernière journée ou plus. Cela permet des restaurations rapides à des points récents dans le temps tout en réduisant la consommation globale d'espace.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `repo1-retention-diff`

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=1
repo1-retention-full=2
start-fast=y

[global:archive-push]
compress-level=3
```

Avec `repo1-retention-diff=1`, deux sauvegardes différentielles doivent être effectuées avant que l'une d'elles n'expire. Une sauvegarde incrémentielle est ajoutée pour illustrer l'expiration incrémentielle, qui dépend ici de l'expiration de la sauvegarde différentielle.

pg-primary **⇒** Effectuer des sauvegardes différentielles et incrémentielles

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Effectuer maintenant une sauvegarde différentielle expire les sauvegardes différentielles et incrémentielles précédentes, ne laissant ainsi qu'une seule sauvegarde différentielle.

pg-primary **⇒** Effectuer une sauvegarde différentielle

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=945-4ca6fd47 --log-level-console=info --no-log-timestamp --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261015-070800F_20261015-070802D, 20261015-070800F_20261015-070803I
P00   INFO: repo1: remove expired backup 20261015-070800F_20261015-070803I
P00   INFO: repo1: remove expired backup 20261015-070800F_20261015-070802D
P00   INFO: expire command end: completed successfully
```

### Rétention des archives {#archive-retention}

Bien que pgBackRest supprime automatiquement les segments WAL archivés lors de l’expiration des sauvegardes (le comportement par défaut expire les WAL des sauvegardes complètes en fonction de l’option `repo1-retention-full`), il peut être utile d’expirer l’archive de manière plus agressive afin de libérer de l’espace disque. Notez que les sauvegardes complètes sont traitées comme des sauvegardes différentielles pour l’application de la rétention des archives différentielles.

L’expiration de l’archive ne supprimera jamais les segments WAL nécessaires à la cohérence d’une sauvegarde. Toutefois, comme la récupération à un point donné (PITR) ne fonctionne qu’avec un flux WAL continu, une attention particulière doit être portée lors de l’expiration agressive de l’archive en dehors du processus normal d’expiration des sauvegardes. Pour déterminer quels éléments seront supprimés sans effectuer réellement l’expiration, l’option `dry-run` peut être fournie en ligne de commande avec la commande `expire`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `repo1-retention-diff`

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=2
repo1-retention-full=2
start-fast=y

[global:archive-push]
compress-level=3
```

pg-primary **⇒** Effectuer une sauvegarde différentielle

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261015-070800F_20261015-070805D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** Expire archive

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.60.0: --exec-id=1026-cfe5c422 --log-level-console=detail --no-log-timestamp --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 17-1 archive retention on backup 20261015-070758F, start = 00000002000000000000000A, stop = 00000002000000000000000B
P00 DETAIL: repo1: 17-1 archive retention on backup 20261015-070800F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 17-1 archive retention on backup 20261015-070800F_20261015-070804D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 17-1 archive retention on backup 20261015-070800F_20261015-070805D, start = 000000020000000000000016
P00   INFO: repo1: 17-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

La sauvegarde différentielle `20261015-070800F_20261015-070804D` contient des segments WAL qui doivent être conservés pour assurer la cohérence des sauvegardes plus anciennes, même si elles ne peuvent plus être restaurées ultérieurement avec une récupération à un point précis (PITR). Les segments WAL générés après `20261015-070800F_20261015-070804D` mais avant `20261015-070800F_20261015-070805D` sont supprimés. Les segments WAL générés après la nouvelle sauvegarde `20261015-070800F_20261015-070805D` sont conservés et peuvent être utilisés pour une récupération à un point précis (PITR).

Étant donné que les sauvegardes complètes sont considérées comme des sauvegardes différentielles afin de déterminer la rétention des archives différentielles, si une sauvegarde complète est désormais effectuée avec les mêmes paramètres, seule l’archive correspondante à cette sauvegarde complète est conservée pour la récupération à un instant donné.


--------

## Restauration {#restore-1}

La commande de restauration sélectionne automatiquement la dernière sauvegarde du premier dépôt où des sauvegardes existent (voir [Démarrage rapide - Restaurer une sauvegarde](#restore-a-backup)). L'ordre dans lequel les dépôts sont vérifiés est déterminé par le paramètre `pgbackrest.conf` (par exemple, repo1 sera vérifié avant repo2). Pour sélectionner un dépôt spécifique, l'option `--repo` peut être utilisée (par exemple, `--repo=1`). L'option `--set` peut être utilisée si une sauvegarde autre que la plus récente est souhaitée.

Lors d'une PITR avec `--type=time` ou `--type=lsn`, l'heure ou le LSN cible doit être fourni avec l'option `--target`. Si `--set` n'est pas spécifié, les dépôts configurés sont examinés dans l'ordre pour trouver une sauvegarde dont l'heure de fin précède l'heure cible, ou dont le LSN de fin est inférieur ou égal au LSN cible. Si aucune sauvegarde ne correspond, pgBackRest signale une erreur aussi bien pour `--type=time` que pour `--type=lsn` ; il ne se rabat pas sur la sauvegarde la plus récente. Pour les autres types de PITR, par exemple `xid`, l'option `--set` doit être fournie si la cible est antérieure à la sauvegarde la plus récente. Consultez [Restauration à un instant donné](#point-in-time-recovery) pour plus de détails et d'exemples.

Les slots de réplication ne sont pas inclus, conformément à la recommandation de PostgreSQL. Consultez [Sauvegarde du répertoire de données](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) dans la documentation PostgreSQL pour plus d'informations.

Les sections suivantes présentent des fonctionnalités supplémentaires de la commande `restore`.


### Propriétaire du fichier {#file-ownership}

Si un `restore` est exécuté en tant qu'utilisateur non privilégié (scénario typique), tous les fichiers restaurés appartiendront à l'utilisateur/groupe exécutant pgBackRest. Si des fichiers existants ne sont pas possédés par l'utilisateur/groupe exécutant, une erreur se produira si la propriété ne peut pas être mise à jour pour correspondre à l'utilisateur/groupe exécutant. Dans ce cas, la propriété des fichiers devra être mise à jour par un utilisateur ayant des privilèges avant de pouvoir réessayer la restauration.

Si un `restore` est exécuté en tant qu'utilisateur `root`, pgBackRest tentera de recréer la propriété enregistrée dans le manifeste au moment de la sauvegarde. Seuls les **noms** d'utilisateur/groupe sont stockés dans le manifeste, donc les mêmes noms doivent exister sur l'hôte de restauration pour que cela fonctionne. Si le nom d'utilisateur/groupe ne peut pas être trouvé localement, l'utilisateur/groupe du répertoire de données PostgreSQL sera utilisé, puis `root` si l'utilisateur/groupe du répertoire de données ne peut pas être mappé à un nom.


### Option Delta {#delta-option}

[Restaurer une sauvegarde](#restore-a-backup) dans [Démarrage rapide](#quick-start) nécessite que le répertoire du cluster de base de données soit nettoyé avant que la commande `restore` puisse être effectuée. L'option `delta` permet à pgBackRest de déterminer automatiquement quels fichiers du répertoire du cluster de base de données peuvent être conservés et quels fichiers doivent être restaurés à partir de la sauvegarde — elle supprime également les fichiers absents du manifeste de sauvegarde, ce qui permet d'éliminer les modifications divergentes. Cette opération est réalisée en calculant un hachage cryptographique [SHA-1](https://en.wikipedia.org/wiki/SHA-1) pour chaque fichier du répertoire du cluster de base de données. Si le hachage `SHA-1` ne correspond pas au hachage stocké dans la sauvegarde, ce fichier sera restauré. Cette opération est particulièrement efficace lorsqu'elle est combinée avec l'option `process-max`. Comme le serveur PostgreSQL est arrêté pendant la restauration, un plus grand nombre de processus peut être utilisé que lors d'une sauvegarde, où le serveur PostgreSQL est en cours d'exécution.

pg-primary **⇒** Arrêtez le cluster de démonstration, effectuez une restauration delta

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/postgresql/17/demo' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/base/1/pg_internal.init'
       [filtered 383 lines of output]
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/1255 - exists and matches backup (bundle 20261015-070800F/1/2464720, 792KB, 73.62%) checksum 7be9b18ae9e21c9583e5c9c35b662ce530a92e14
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/4/1255 - exists and matches backup (bundle 20261015-070800F/1/2568896, 792KB, 77.13%) checksum 7be9b18ae9e21c9583e5c9c35b662ce530a92e14
P01 DETAIL: restore file /var/lib/postgresql/17/demo/PG_VERSION - exists and matches backup (bundle 20261015-070800F/1/2673072, 3B, 77.13%) checksum ad48103e4fc71796e9708cafc43adeed0d1076b7
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/PG_VERSION - exists and matches backup (bundle 20261015-070800F/1/2673096, 3B, 77.13%) checksum ad48103e4fc71796e9708cafc43adeed0d1076b7
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/4/PG_VERSION - exists and matches backup (bundle 20261015-070800F/1/2673120, 3B, 77.13%) checksum ad48103e4fc71796e9708cafc43adeed0d1076b7
       [filtered 619 lines of output]
```

pg-primary **⇒** Redémarrer PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

### Restauration des bases de données sélectionnées {#restore-selected-databases}

Il peut arriver que l'on souhaite restaurer sélectivement des bases de données spécifiques à partir d'une sauvegarde de cluster. Cela peut être utile pour des raisons de performance ou pour déplacer des bases sélectionnées vers une machine qui ne dispose pas d'espace suffisant pour restaurer l'intégralité de la sauvegarde du cluster.

Pour démontrer cette fonctionnalité, deux bases de données sont créées : test1 et test2.

pg-primary **⇒** Créer deux bases de données de test

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

Chaque base de données de test sera initialisée avec des tables et des données afin de démontrer que la restauration sélective fonctionne.

pg-primary **⇒** Créer une table de test dans chaque base de données

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

Une nouvelle sauvegarde est exécutée afin que pgBackRest prenne connaissance des nouvelles bases de données.

pg-primary **⇒** Effectuer une sauvegarde

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

L'une des principales raisons d'utiliser une restauration sélective est de conserver de l'espace. La taille de la base de données test1 est indiquée ici afin de pouvoir la comparer à l'utilisation du disque après une restauration sélective.

pg-primary **⇒** Afficher l'espace utilisé par la base test1

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
7.4M    /var/lib/postgresql/17/demo/base/32768
```

Si la base de données à restaurer n'est pas connue, utilisez l'option `info` de la commande `set` pour découvrir les bases de données faisant partie de l'ensemble de sauvegarde.

pg-primary **⇒** Afficher la liste des bases de données pour la sauvegarde

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261015-070800F_20261015-070809I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 1.9MB
            backup reference list: 20261015-070800F, 20261015-070800F_20261015-070805D
            database list: postgres (5), test1 (32768), test2 (32769)
```

Arrêtez le cluster et effectuez une restauration uniquement de la base test2. Les bases de données intégrées (`template0`, `template1` et `postgres`) sont toujours restaurées.

AVERTISSEMENT :

La récupération peut échouer sauf si `--type=immediate` est spécifié. Cela est dû au fait qu'une fois la cohérence atteinte, PostgreSQL signale les pages nulles comme des erreurs, même pour une écriture complète de page. Pour PostgreSQL ≥ 13, le paramètre ignore_invalid_pages peut être utilisé pour ignorer les pages non valides. Dans ce cas, il est important de vérifier les journaux après la récupération afin de s'assurer qu'aucune page non valide n'a été signalée dans les bases de données sélectionnées.

pg-primary **⇒** Restauration à partir de la dernière sauvegarde, incluant uniquement la base test2

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

Une fois la récupération terminée, la base de données test2 contiendra toutes les tables et les données précédemment créées.

pg-primary **⇒** Démontrer que la base de données test2 a été restaurée

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

La base de données test1, malgré une récupération réussie, n'est pas accessible. Cela est dû au fait que la base entière a été restaurée sous forme de fichiers creux initialisés à zéro. PostgreSQL peut appliquer correctement le WAL sur ces fichiers initialisés à zéro, mais la base de données dans son ensemble ne sera pas valide, car certains fichiers clés ne contiennent aucune donnée. Cette situation est volontaire, afin d'éviter que la base de données ne soit utilisée accidentellement alors qu'elle pourrait contenir des données partielles appliquées pendant la relecture du WAL.

pg-primary **⇒** Tenter de se connecter à la base de données test1 produira une erreur

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

Étant donné que la base de données test1 est restaurée avec des fichiers épars et initialisés à zéro, elle n'utilisera que l'espace nécessaire à la quantité de WAL écrite pendant la récupération. Bien que la quantité de WAL générée lors d'une sauvegarde et appliquée lors de la récupération puisse être importante, elle représente généralement une fraction réduite de la taille totale de la base de données, en particulier pour les grandes bases de données où cette fonctionnalité est le plus susceptible d'être utile.

Il est clair que la base de données test1 utilise bien moins d'espace disque lors d'une restauration sélective que si toute la base de données avait été restaurée.

pg-primary **⇒** Afficher l'espace utilisé par la base de données test1 après la récupération

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
8.0K    /var/lib/postgresql/17/demo/base/32768
```

À ce stade, la seule action pouvant être entreprise sur la base test1 invalide est `drop database`. pgBackRest ne supprime pas automatiquement la base de données, car cela n'est pas possible tant que la récupération n'est pas terminée et que le cluster n'est pas accessible.

pg-primary **⇒** Supprimer la base de données test1

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

À présent que la base de données test1 invalide a été supprimée, seules les bases de données test2 et les bases intégrées restent.

pg-primary **⇒** Liste des bases de données restantes

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
     4 | template0
     5 | postgres
 32769 | test2
(4 rows)
```

--------

## Restauration à un instant donné {#point-in-time-recovery}

[Restaurer une sauvegarde](#restore-a-backup) dans [Démarrage rapide](#quick-start) a effectué une récupération par défaut, qui consiste à rejouer toutes les transactions jusqu'à la fin du flux WAL. En cas de panne matérielle, il s'agit généralement du choix optimal, mais en cas de corruption des données (qu'elle soit due à une panne matérielle ou humaine), la restauration à un instant donné (PITR) est souvent plus appropriée.

La restauration à un instant donné (PITR) permet de rejouer les journaux d'écriture (WAL) à partir d'une sauvegarde jusqu'à un LSN, une heure, un identifiant de transaction ou un point de récupération spécifié. Pour les scénarios de récupération courants, la récupération basée sur le temps est sans doute la plus utile. Un scénario de récupération typique consiste à restaurer une table supprimée par erreur ou des données supprimées par erreur. La récupération d'une table supprimée est plus spectaculaire, aussi est-elle prise comme exemple ici, mais les données supprimées seraient récupérées exactement de la même manière.

pg-primary **⇒** Créer une table avec des données très importantes

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Il est important de représenter l’heure selon le calcul de PostgreSQL et d’inclure les décalages de fuseau horaire. Cela réduit la possibilité de conversions de fuseau horaire non souhaitées et d’un résultat de récupération inattendu.

pg-primary **⇒** Obtenir l'heure depuis PostgreSQL

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-15 07:08:16.882666+00
```

À présent que l'heure a été enregistrée, la table est supprimée. En pratique, déterminer l'heure exacte à laquelle la table a été supprimée est bien plus difficile qu'à l'exemple présenté. Il se peut qu'il ne soit pas possible de déterminer l'heure exacte, mais une analyse forensique devrait toutefois pouvoir s'en approcher.

pg-primary **⇒** Supprimer la table importante

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

Si la mauvaise sauvegarde est sélectionnée pour la restauration, la récupération jusqu'à la cible de temps requise échouera. Pour illustrer ce cas, une nouvelle sauvegarde incrémentielle est effectuée alors que `important_table` n'existe pas.

pg-primary **⇒** Effectuer une sauvegarde incrémentielle

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261015-070800F_20261015-070818I
            timestamp start/stop: 2026-10-15 07:08:18+00 / 2026-10-15 07:08:19+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

Il ne sera pas possible de récupérer la table perdue à partir de cette sauvegarde, car PostgreSQL ne peut avancer que vers l'avant, pas vers l'arrière.

pg-primary **⇒** Tentative de récupération à partir d'une sauvegarde incorrecte

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261015-070800F_20261015-070818I --target-timeline=current \
       --type=time "--target=2026-10-15 07:08:16.882666+00" --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

```text
       [filtered 13 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000120 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.02 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 1433) exited with exit code 1
LOG:  terminating any other active server processes
       [filtered 4 lines of output]
```

Une méthode fiable consiste à autoriser pgBackRest à sélectionner automatiquement une sauvegarde pouvant être restaurée jusqu'à l'instant cible, c'est-à-dire une sauvegarde terminée avant l'instant spécifié.

NOTE :

pgBackRest ne peut pas sélectionner automatiquement une sauvegarde lorsque le type de restauration est `xid` ou `name`.

pg-primary **⇒** Effectuer la restauration du cluster de démonstration sur `2026-10-15 07:08:16.882666+00`

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-15 07:08:16.882666+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-15 07:08:20
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-15 07:08:16.882666+00'
recovery_target_action = 'promote'
```

pgBackRest a généré les paramètres de récupération dans `postgresql.auto.conf` afin que PostgreSQL puisse être démarré immédiatement. `%f` est le moyen par lequel PostgreSQL indique le segment WAL dont il a besoin, et `%p` est l'emplacement où il doit être copié. Une fois la récupération de PostgreSQL terminée, la table existera à nouveau et pourra être interrogée.

pg-primary **⇒** Démarrer PostgreSQL et vérifier que la table importante existe

```bash
sudo pg_ctlcluster 17 demo start
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

Le journal PostgreSQL contient également des informations précieuses. Il indique l'heure et la transaction où la récupération s'est arrêtée, ainsi que l'heure de la dernière transaction appliquée.

pg-primary **⇒** Examinez la sortie des journaux PostgreSQL

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 7 lines of output]
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
LOG:  starting point-in-time recovery to 2026-10-15 07:08:16.882666+00
LOG:  restored log file "00000003.history" from archive
LOG:  redo starts at 0/19000028
       [filtered 2 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "00000004000000000000001A" from archive
LOG:  recovery stopping before commit of transaction 748, time 2026-10-15 07:08:18.066935+00
LOG:  redo done at 0/1901CC00 system usage: CPU: user: 0.00 s, system: 0.01 s, elapsed: 0.05 s
LOG:  last completed transaction was at log time 2026-10-15 07:08:15.697241+00
LOG:  restored log file "000000040000000000000019" from archive
LOG:  selected new timeline ID: 5
       [filtered 4 lines of output]
```

--------

## Supprimer une stanza {#delete-a-stanza}

La commande `stanza-delete` supprime les données du dépôt associées à un stanza.

AVERTISSEMENT :

Utilisez cette commande avec précaution — elle supprimera définitivement toutes les sauvegardes et archives du dépôt pgBackRest pour le stanza spécifié.

Pour supprimer une stanza :

-  Arrêtez le cluster PostgreSQL associé à la stanza (ou utilisez --force pour l'ignorer).
-  Exécutez la commande `stop` sur l'hôte où la commande `stanza-delete` sera exécutée.
-  Exécutez la commande `stanza-delete`.

Une fois la commande exécutée avec succès, il incombe à l'utilisateur de supprimer la stanza de tous les fichiers de configuration pgBackRest et/ou des variables d'environnement.

Un stanza ne peut être supprimé que d’un dépôt à la fois. Pour supprimer le stanza de plusieurs dépôts, répétez la commande `stanza-delete` pour chaque dépôt tout en spécifiant l’option `--repo`.

pg-primary **⇒** Arrêtez le cluster PostgreSQL à supprimer

```bash
sudo pg_ctlcluster 17 demo stop
```

pg-primary **⇒** Arrêtez pgBackRest pour la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.60.0: --exec-id=1568-be450376 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** Supprimer le stanza depuis un dépôt

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.60.0: --exec-id=1576-579aad05 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=1 --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## Dépôts multiples {#multiple-repositories}

Plusieurs dépôts peuvent être configurés, comme illustré dans [Prise en charge S3](#s3-compatible-object-store-support). Un avantage potentiel est la possibilité de disposer d’un dépôt local pour des restaurations rapides et d’un dépôt distant pour la redondance.

Certaines commandes, par exemple [`stanza-create`](/fr/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/fr/pgbackrest/command/stanza-upgrade/), fonctionnent automatiquement avec tous les dépôts configurés, tandis que d'autres, par exemple [`stanza-delete`](/fr/pgbackrest/command/stanza-delete/), nécessitent la spécification d'un dépôt à l'aide de l'option `repo`.

Notez que l'option `repo` n'est pas obligatoire lorsqu'uniquement `repo1` est configuré, afin de préserver la compatibilité descendante. Toutefois, l'option `repo` *est* obligatoire lorsqu'un seul dépôt est configuré, par exemple `repo2`. Ceci vise à éviter la rupture de commande en cas d'ajout ultérieur d'un nouveau dépôt.

La commande `archive-push` poussera toujours les journaux WAL vers l’archive dans tous les dépôts configurés. Si un dépôt n’est pas accessible, les journaux WAL seront tout de même poussés vers les autres dépôts. Toutefois, pour que cela fonctionne efficacement, `archive-async=y` doit être activé ; sinon, les autres dépôts ne pourront avancer que d’un segment WAL par rapport au dépôt inatteignable. Notez également qu’en cas d’impossibilité de pousser les journaux WAL vers n’importe quel dépôt, PostgreSQL ne supprimera pas ces journaux du répertoire `pg_wal`, ce qui peut entraîner la saturation du volume.

Les sauvegardes doivent être planifiées individuellement pour chaque dépôt. Dans de nombreuses situations, cela est souhaitable car les types de sauvegarde et la rétention varient d’un dépôt à l’autre. De même, les restaurations doivent préciser un dépôt. Il est généralement préférable de spécifier un dépôt à faible latence/coût, même si cela implique un temps de récupération plus long. Seule une vérification par test de restauration permettra de déterminer quel dépôt sera le plus efficace.


--------

## Prise en charge du magasin d'objets compatible Azure {#azure-compatible-object-store-support}

pgBackRest prend en charge la localisation des dépôts dans des magasins d'objets compatibles Azure. Le conteneur utilisé pour stocker le dépôt doit être créé à l'avance — pgBackRest ne le fera pas automatiquement. Le dépôt peut être situé à la racine du conteneur (`/`), mais il est généralement préférable de le placer dans un sous-chemin afin de pouvoir stocker également des journaux ou d'autres données dans le conteneur sans conflit.

AVERTISSEMENT :

N'activez pas l'« espace de noms hiérarchique » car cela provoquera des erreurs lors de l'expiration.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez Azure

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=2
repo1-retention-full=2
repo2-azure-account=pgbackrest
repo2-azure-container=demo-container
repo2-azure-key=YXpLZXk=
repo2-path=/demo-repo
repo2-retention-full=4
repo2-type=azure
start-fast=y

[global:archive-push]
compress-level=3
```

Les signatures d'accès partagé peuvent être utilisées en définissant l'option `repo2-azure-key-type` sur `sas` et l'option `repo2-azure-key` sur le jeton de signature d'accès partagé.

Les commandes sont exécutées exactement comme si le dépôt était stocké sur un disque local.

pg-primary **⇒** Créer la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.60.0: --exec-id=1669-276a1ddb --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

Le temps de création de fichier dans Azure est relativement lent, aussi la performance de `backup`/`restore` est améliorée en activant le [regroupement de fichiers](#file-bundling).

pg-primary **⇒** Effectuer une sauvegarde du cluster de démonstration

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.60.0: --exec-id=1678-229e5c4c --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=2 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-block --repo1-bundle --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261015-070828F
P00   INFO: full backup size = 29.3MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=1678-229e5c4c --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## Prise en charge du stockage d'objets compatible S3 {#s3-compatible-object-store-support}

pgBackRest prend en charge le positionnement des dépôts dans des magasins d'objets compatibles S3. Le bac utilisé pour stocker le dépôt doit être créé à l'avance — pgBackRest ne le fera pas automatiquement. Le dépôt peut être placé à la racine du bac (`/`), mais il est généralement préférable de le situer dans un sous-répertoire afin de pouvoir stocker également des journaux ou d'autres données dans le bac sans conflit.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez S3

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=2
repo1-retention-full=2
repo2-azure-account=pgbackrest
repo2-azure-container=demo-container
repo2-azure-key=YXpLZXk=
repo2-path=/demo-repo
repo2-retention-full=4
repo2-type=azure
repo3-path=/demo-repo
repo3-retention-full=4
repo3-s3-bucket=demo-bucket
repo3-s3-endpoint=s3.us-east-1.amazonaws.com
repo3-s3-key=accessKey1
repo3-s3-key-secret=verySecretKey1
repo3-s3-region=us-east-1
repo3-type=s3
start-fast=y

[global:archive-push]
compress-level=3
```

NOTE :

La région et le point de terminaison devront être configurés selon l'emplacement du bac. Les valeurs indiquées ici correspondent à la région `us-east-1`.

Un rôle doit être créé pour exécuter pgBackRest et les autorisations du bac doivent être définies aussi restrictivement que possible. Si le rôle est associé à une instance dans AWS, pgBackRest récupérera automatiquement des identifiants temporaires lorsque `repo3-s3-key-type=auto`, ce qui signifie que les clés n’ont pas besoin d’être explicitement définies dans `/etc/pgbackrest/pgbackrest.conf`.

Politique Amazon S3 d'exemple qui restreint toutes les lectures et écritures au bac et au chemin du dépôt.

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

Les commandes sont exécutées exactement comme si le dépôt était stocké sur un disque local.

pg-primary **⇒** Créer la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

Le temps de création de fichier dans S3 est relativement lent, aussi la performance de `backup`/`restore` est améliorée en activant le [regroupement de fichiers](#file-bundling).

pg-primary **⇒** Effectuer une sauvegarde du cluster de démonstration

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.60.0: --exec-id=1886-57ff5545 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=3 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-block --repo1-bundle --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key= --repo3-s3-key-secret= --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261015-070845F
P00   INFO: full backup size = 29.3MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=1886-57ff5545 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key= --repo3-s3-key-secret= --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## Prise en charge SFTP {#sftp-support}

pgBackRest prend en charge la localisation des dépôts sur des hôtes SFTP. Le transfert de fichiers SFTP est relativement lent, aussi les commandes bénéficient-elles d'une augmentation de `process-max` afin de paralléliser le transfert de fichiers.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez SFTP

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
process-max=4
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=2
repo1-retention-full=2
repo2-azure-account=pgbackrest
repo2-azure-container=demo-container
repo2-azure-key=YXpLZXk=
repo2-path=/demo-repo
repo2-retention-full=4
repo2-type=azure
repo3-path=/demo-repo
repo3-retention-full=4
repo3-s3-bucket=demo-bucket
repo3-s3-endpoint=s3.us-east-1.amazonaws.com
repo3-s3-key=accessKey1
repo3-s3-key-secret=verySecretKey1
repo3-s3-region=us-east-1
repo3-type=s3
repo4-bundle=y
repo4-path=/demo-repo
repo4-sftp-host=sftp-server
repo4-sftp-host-key-hash-type=sha1
repo4-sftp-host-user=pgbackrest
repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp
repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub
repo4-type=sftp
start-fast=y

[global:archive-push]
compress-level=3
```

Lors de l'utilisation de SFTP, si libssh2 est compilé contre OpenSSH, `repo4-sftp-public-key-file` est facultatif.

pg-primary **⇒** Générer une paire de clés SSH pour la sauvegarde SFTP

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** Copier la clé publique de sauvegarde SFTP de pg-primary sur sftp-server

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

Les commandes sont exécutées exactement comme si le dépôt était stocké sur un disque local.

pg-primary **⇒** Ajouter l'empreinte du serveur SFTP au fichier known_hosts, car `repo4-sftp-host-key-check-type` est par défaut défini sur « strict »

```bash
ssh-keyscan -H sftp-server >> /var/lib/postgresql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** Créer la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** Effectuer une sauvegarde du cluster de démonstration

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.60.0: --exec-id=1973-b6b04e3d --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=4 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key= --repo3-s3-key-secret= --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261015-070853F
P00   INFO: full backup size = 29.3MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.60.0: --exec-id=1973-b6b04e3d --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key= --repo3-s3-key-secret= --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## Prise en charge du stockage d'objets compatible GCS {#gcs-compatible-object-store-support}

pgBackRest prend en charge la localisation des dépôts dans des magasins d'objets compatibles GCS. Le conteneur utilisé pour stocker le dépôt doit être créé à l'avance — pgBackRest ne le fera pas automatiquement. Le dépôt peut être situé à la racine du conteneur (`/`), mais il est généralement préférable de le placer dans un sous-répertoire afin de pouvoir stocker également des journaux ou d'autres données dans le conteneur sans conflit.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez le GCS

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
process-max=4
repo1-block=y
repo1-bundle=y
repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
repo1-cipher-type=aes-256-cbc
repo1-path=/var/lib/pgbackrest
repo1-retention-diff=2
repo1-retention-full=2
repo2-azure-account=pgbackrest
repo2-azure-container=demo-container
repo2-azure-key=YXpLZXk=
repo2-path=/demo-repo
repo2-retention-full=4
repo2-type=azure
repo3-path=/demo-repo
repo3-retention-full=4
repo3-s3-bucket=demo-bucket
repo3-s3-endpoint=s3.us-east-1.amazonaws.com
repo3-s3-key=accessKey1
repo3-s3-key-secret=verySecretKey1
repo3-s3-region=us-east-1
repo3-type=s3
repo4-bundle=y
repo4-path=/demo-repo
repo4-sftp-host=sftp-server
repo4-sftp-host-key-hash-type=sha1
repo4-sftp-host-user=pgbackrest
repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp
repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub
repo4-type=sftp
repo5-gcs-bucket=demo-bucket
repo5-gcs-key=/etc/pgbackrest/gcs-key.json
repo5-path=/demo-repo
repo5-type=gcs
start-fast=y

[global:archive-push]
compress-level=3
```

Lors de l'exécution sur GCE, définissez `repo5-gcs-key-type=auto` pour authentifier automatiquement à l'aide du compte de service de l'instance.

Les commandes sont exécutées exactement comme si le dépôt était stocké sur un disque local.

Le temps de création de fichier dans GCS est relativement lent, aussi la performance de `backup`/`restore` est améliorée en activant le [regroupement de fichiers](#file-bundling).


--------

## Heure cible pour le dépôt {#target-time-for-repository}

Le temps cible définit l'instant auquel les commandes lisent un dépôt sur un stockage versionné. Cela permet à la commande de lire le dépôt tel qu'il était à un instant donné, afin de récupérer des données supprimées ou corrompues par une erreur utilisateur ou un logiciel malveillant.

Le stockage versionné est pris en charge par S3, GCS et Azure, mais il est généralement désactivé par défaut. En plus d’activer le versioning, il peut être utile d’activer le verrouillage d’objets pour S3, ou la suppression réversible pour GCS ou Azure.

Lorsque l'option `repo-target-time` est spécifiée, l'option `repo` doit également être fournie. Il est probable que tous les types de dépôt ne prennent pas en charge le versioning, et il est généralement préférable de cibler un seul dépôt pour la récupération.

Notez que les comparaisons avec l'horodatage de stockage sont <= à l'horodatage fourni et que les millisecondes sont tronquées de l'horodatage lorsqu'elles sont fournies.

Pour démontrer cette fonctionnalité, la stanza `demo` dans le dépôt S3 est supprimée.

pg-primary **⇒** Supprimer le stanza dans le dépôt S3

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

Une fois le stanza supprimé, la commande `info` affichera le dépôt dans un état d'erreur.

pg-primary **⇒** Erreur lors de la commande `info`

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

Toutefois, comme le stockage est versionné, il est possible d'examiner le dépôt à une époque antérieure à la suppression du stanza. Trouver l'instant cible peut s'avérer délicat selon la situation, mais dans ce cas, l'instant de suppression du stanza peut être déterminé en vérifiant quand `backup.info` a été supprimé.

pg-primary **⇒** Répertorier les versions de `backup.info` dans le bac

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
------------------------------------------------------------------------------
|                             ListObjectVersions                             |
+--------+-----------------------------+-------------------------------------+
| Action |          Modified           |               Object                |
+--------+-----------------------------+-------------------------------------+
|  PUT   |  2026-10-15T07:08:45+00:00  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-15T07:08:49+00:00  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-15T07:08:58+00:00  |  demo-repo/backup/demo/backup.info  |
+--------+-----------------------------+-------------------------------------+
```

À présent, la commande `info` peut être exécutée avec une heure cible afin d’afficher le dépôt avant sa suppression.

pg-primary **⇒** Information avec heure cible

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-15 07:08:49+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (17): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261015-070845F
            timestamp start/stop: 2026-10-15 07:08:45+00 / 2026-10-15 07:08:49+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 3.8MB, backup size: 3.8MB
```

Si la sauvegarde requise est indiquée par la commande `info`, elle peut être restaurée en utilisant le même instant cible.

pg-primary **⇒** Restauration avec heure cible

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-15 07:08:49+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.60.0: --delta --exec-id=2085-6787dc85 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=3 --repo2-azure-account= --repo2-azure-container=demo-container --repo2-azure-key= --repo1-cipher-pass= --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key= --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key= --repo3-s3-key-secret= --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-15 07:08:49+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261015-070845F, recovery will start at 2026-10-15 07:08:45
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00   INFO: write updated /var/lib/postgresql/17/demo/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo pg_ctlcluster 17 demo start
```

--------

## Hôte dédié au dépôt {#dedicated-repository-host}

La configuration décrite dans [Démarrage rapide](#quick-start) convient aux installations simples, mais pour les configurations d'entreprise, il est plus courant d'avoir un hôte dédié au dépôt, où sont stockées les sauvegardes et les fichiers d'archive WAL. Cette approche sépare les sauvegardes et l'archive WAL du serveur de base de données, de sorte que les défaillances de l'hôte de base de données aient un impact moindre. Il est toutefois recommandé d'utiliser un logiciel de sauvegarde traditionnel pour sauvegarder l'hôte du dépôt.

Sur les hôtes PostgreSQL, `pg1-path` doit être le chemin du cluster PostgreSQL local et aucune configuration `pg1-host` ne doit être définie. Lors de la configuration d’un hôte de dépôt, le fichier de configuration pgBackRest doit inclure l’option `pg-host` pour se connecter aux hôtes principaux et secondaires (le cas échéant). L’hôte de dépôt est le seul qui doit disposer d’une configuration pgBackRest connaissant plusieurs hôtes PostgreSQL. L’ordre n’a pas d’importance, par exemple pg1-path/pg1-host, pg2-path/pg2-host peut correspondre à un hôte principal ou secondaire.


### Installation {#installation-1}

Un nouvel hôte nommé repository est créé pour stocker les sauvegardes du cluster.

NOTE :

La version de pgBackRest installée sur l'hôte du dépôt doit correspondre exactement à la version installée sur l'hôte PostgreSQL.

L'utilisateur `pgbackrest` est créé pour posséder le dépôt pgBackRest. Tout utilisateur peut posséder le dépôt, mais il est préférable de ne pas utiliser `postgres` (le cas échéant) afin d'éviter toute confusion.

NOTE :

Lorsque pgBackRest est installé à partir d'un paquet, une configuration logrotate telle que `/etc/logrotate.d/pgbackrest` peut être fournie, qui effectue la rotation des journaux en tant qu'utilisateur spécifique via la directive `su` (par exemple `su postgres postgres`). Étant donné que les fichiers dans `/var/log/pgbackrest` sont possédés par l'utilisateur exécutant pgBackRest (ici `pgbackrest`), la directive `su` doit être mise à jour pour correspondre à cet utilisateur, sinon logrotate échouera avec une erreur de permission.

dépôt **⇒** Créer l'utilisateur `pgbackrest`

```bash
sudo adduser --disabled-password --gecos "" pgbackrest
```

Installer pgBackRest à partir d’un paquet est préférable à la compilation à partir des sources. Lors de l’installation à partir d’un paquet, les autres instructions de cette section sont généralement inutiles, mais il se peut qu’un paquet omette de créer un répertoire ou applique des permissions incorrectes. Dans ce cas, il peut être nécessaire de créer manuellement les répertoires ou de mettre à jour les permissions.

Les paquets Debian/Ubuntu pour pgBackRest sont disponibles sur [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si des paquets ne sont pas fournis pour votre distribution/version, vous pouvez [compiler à partir des sources](#build) puis procéder à l'installation manuelle comme indiqué ici.

dépôt **⇒** Installer les dépendances

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

dépôt **⇒** Copier le binaire pgBackRest depuis l'hôte de compilation

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest nécessite des répertoires pour les journaux et la configuration, ainsi qu'un fichier de configuration.

dépôt **⇒** Créer le fichier de configuration pgBackRest et les répertoires

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

dépôt **⇒** Créer le dépôt pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### Configuration d'un accès SSH sans mot de passe {#setup-passwordless-ssh}

pgBackRest peut utiliser SSH sans mot de passe pour permettre la communication entre les hôtes. Il est également possible d'utiliser TLS, voir [Configurer TLS](/fr/pgbackrest/user-guide-rhel/#configuration).

dépôt **⇒** Créer une paire de clés pour l'hôte du dépôt

```bash
sudo -u pgbackrest mkdir -m 750 /home/pgbackrest/.ssh
sudo -u pgbackrest ssh-keygen -f /home/pgbackrest/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

pg-primary **⇒** Créer une paire de clés pour l'hôte pg-primary

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Échanger les clés entre le dépôt et pg-primary.

dépôt **⇒** Copiez la clé publique pg-primary vers le dépôt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-primary **⇒** Copier la clé publique du dépôt sur pg-primary

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Testez que les connexions peuvent être établies depuis le dépôt vers pg-primary et inversement.

dépôt **⇒** Tester la connexion depuis le dépôt vers pg-primary

```bash
sudo -u pgbackrest ssh postgres@pg-primary
```

pg-primary **⇒** Tester la connexion depuis pg-primary vers le dépôt

```bash
sudo -u postgres ssh pgbackrest@repository
```

NOTE :

ssh a été configuré pour autoriser uniquement l'exécution de pgBackRest via ssh sans mot de passe. Cela renforce la sécurité en cas de compromission d'un compte de service.


### Configuration {#configuration}

L'hôte du dépôt doit être configuré avec l'hôte/utilisateur principal et le chemin de la base de données. Le principal sera configuré en tant que `pg1` afin de permettre l'ajout ultérieur d'un serveur de secours.

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez `pg1-host`/`pg1-host-user` et `pg1-path`

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/17/demo

[global]
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

L'hôte de base de données doit être configuré avec l'hôte/utilisateur du dépôt. La valeur par défaut de l'option `repo1-host-user` est `pgbackrest`. Si l'utilisateur `postgres` effectue des restaurations sur l'hôte du dépôt, il est préférable de ne pas autoriser également l'utilisateur `postgres` à effectuer des sauvegardes. Toutefois, l'utilisateur `postgres` peut lire directement le dépôt s'il appartient au même groupe que l'utilisateur `pgbackrest`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurer `repo1-host`/`repo1-host-user`

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
log-level-file=detail
repo1-host=repository
```

La configuration de PostgreSQL peut être trouvée dans la section [Configurer la sauvegarde archivée](#configure-archiving).

Les commandes sont exécutées de la même manière qu’avec une configuration à hôte unique, à ceci près que certaines commandes, telles que `backup` et `expire`, sont exécutées depuis l’hôte du dépôt plutôt que depuis l’hôte de la base de données.


### Créer et vérifier une stanza {#create-and-check-stanza}

Créez le stanza dans le nouveau dépôt.

dépôt **⇒** Créer le stanza

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

Vérifiez que la configuration est correcte sur les hôtes de base de données et de dépôt. Plus d'informations sur la commande `check` sont disponibles dans [Vérifier la configuration](#check-the-configuration).

pg-primary **⇒** Vérifier la configuration

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

dépôt **⇒** Vérifiez la configuration

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### Effectuer une sauvegarde {#perform-a-backup-1}

Pour effectuer une sauvegarde du cluster PostgreSQL, exécutez pgBackRest avec la commande `backup` sur l'hôte du dépôt.

dépôt **⇒** Sauvegarder le cluster de démonstration

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

Depuis la création d’un nouveau dépôt sur l’hôte du dépôt, l’avertissement indiquant que la sauvegarde incrémentielle passe à une sauvegarde complète a été émis.


### Restaurer une sauvegarde {#restore-a-backup-1}

Pour effectuer une restauration du cluster PostgreSQL, exécutez pgBackRest avec la commande `restore` sur l'hôte de la base de données.

pg-primary **⇒** Arrêtez le cluster de démonstration, effectuez une restauration, puis redémarrez PostgreSQL

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo pg_ctlcluster 17 demo start
```

--------

## Sauvegarde / Restauration parallèle {#parallel-backup--restore}

pgBackRest propose un traitement parallèle afin d'améliorer les performances de compression et de transfert. Le nombre de processus à utiliser pour cette fonctionnalité est défini à l'aide de l'option `--process-max`.

Il est généralement préférable de ne pas utiliser plus de 25 % des processeurs disponibles pour la commande `backup`. Les sauvegardes n'ont pas besoin de s'exécuter aussi rapidement, à condition d'être effectuées régulièrement, et le processus de sauvegarde ne doit pas impacter les performances de la base de données, si possible.

La commande de restauration peut et doit utiliser tous les processeurs disponibles, car pendant une restauration le cluster PostgreSQL est arrêté et il n’y a généralement aucune autre tâche importante en cours sur l’hôte. Si l’hôte contient plusieurs clusters, cela doit être pris en compte lors de la configuration de la parallélisation de la restauration.

dépôt **⇒** Effectuer une sauvegarde avec un seul processus

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez pgBackRest pour utiliser plusieurs processus `backup`

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/17/demo

[global]
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

dépôt **⇒** Effectuer une sauvegarde avec plusieurs processus

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

dépôt **⇒** Obtenir les informations de sauvegarde pour le cluster de démonstration

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (17): 000000070000000000000023/000000070000000000000025

        full backup: 20261015-070929F
            timestamp start/stop: 2026-10-15 07:09:29+00 / 2026-10-15 07:09:33+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 29.3MB, database backup size: 29.3MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB

        full backup: 20261015-070934F
            timestamp start/stop: 2026-10-15 07:09:34+00 / 2026-10-15 07:09:36+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 29.3MB, database backup size: 29.3MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB
```

La performance de la dernière sauvegarde devrait être améliorée en utilisant plusieurs processus. Pour des sauvegardes très petites, la différence peut ne pas être très marquée, mais à mesure que la taille de la base de données augmente, les gains de temps deviennent plus importants.


--------

## Démarrage et arrêt {#starting-and-stopping}

Si un serveur de secours est promu à des fins de test, ou si un cluster de test est restauré à partir d'une sauvegarde de production, il est recommandé de bloquer l'écriture de ces clusters dans les dépôts pgBackRest. Cette mesure peut être mise en œuvre à l'aide de la commande `stop`.

Les commandes qui écrivent et sont bloquées par `stop` sont : `archive-push`, `backup`, `expire`, `stanza-create` et `stanza-upgrade`. Notez que `stanza-delete` est une exception à cette règle (voir [Supprimer une stanza](#delete-a-stanza) pour plus de détails).

pg-primary **⇒** Arrêt des commandes d'écriture pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

Les nouvelles commandes d'écriture pgBackRest ne s'exécuteront plus.

dépôt **⇒** Tentative de sauvegarde

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

Spécifiez l'option `--force` pour interrompre toute commande d'écriture pgBackRest en cours d'exécution. Cela inclut l'archive-get asynchrone (même si elle redémarre si PostgreSQL en a besoin). Si pgBackRest est déjà arrêté, un nouvel arrêt générera un avertissement.

pg-primary **⇒** Arrêtez à nouveau les services pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

Redémarrez les commandes d'écriture pgBackRest à l'aide de la commande `start`. Les commandes d'écriture en cours avant l'arrêt ne reprendront pas automatiquement, mais elles sont désormais autorisées à redémarrer.

pg-primary **⇒** Démarrer les commandes d'écriture pgBackRest

```bash
sudo -u postgres pgbackrest start
```

Il est également possible d'arrêter pgBackRest pour une seule stanza.

pg-primary **⇒** Arrête les commandes d'écriture pgBackRest pour la stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

Les nouvelles commandes d'écriture pgBackRest pour la stanza spécifiée ne s'exécuteront plus.

dépôt **⇒** Tentative de sauvegarde

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

La stanza doit également être précisée lors du lancement des commandes d'écriture pgBackRest pour une seule stanza.

pg-primary **⇒** Démarrer les commandes d'écriture pgBackRest pour la stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## Réplication {#replication}

La réplication permet de créer plusieurs copies d'un cluster PostgreSQL (appelées réplicas) à partir d'un seul hôte principal. Les réplicas sont utiles pour équilibrer les lectures et assurer une redondance en cas de défaillance de l'hôte principal.


### Installation {#installation-2}

Un nouvel hôte nommé pg-standby est créé pour exécuter le serveur de secours.

Installer pgBackRest à partir d’un paquet est préférable à la compilation à partir des sources. Lors de l’installation à partir d’un paquet, les autres instructions de cette section sont généralement inutiles, mais il se peut qu’un paquet omette de créer un répertoire ou applique des permissions incorrectes. Dans ce cas, il peut être nécessaire de créer manuellement les répertoires ou de mettre à jour les permissions.

Les paquets Debian/Ubuntu pour pgBackRest sont disponibles sur [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si des paquets ne sont pas fournis pour votre distribution/version, vous pouvez [compiler à partir des sources](#build) puis procéder à l'installation manuelle comme indiqué ici.

pg-standby **⇒** Installer les dépendances

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-standby **⇒** Copier le binaire pgBackRest depuis l'hôte de compilation

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest nécessite des répertoires pour les journaux et la configuration, ainsi qu'un fichier de configuration.

pg-standby **⇒** Créer le fichier de configuration et les répertoires pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Configuration d'un accès SSH sans mot de passe {#setup-passwordless-ssh-1}

pgBackRest peut utiliser SSH sans mot de passe pour permettre la communication entre les hôtes. Il est également possible d'utiliser TLS, voir [Configurer TLS](/fr/pgbackrest/user-guide-rhel/#configuration).

pg-standby **⇒** Créer une paire de clés hôte pg-standby

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Échanger les clés entre le dépôt et pg-standby.

dépôt **⇒** Copiez la clé publique pg-standby sur le dépôt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-standby cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-standby **⇒** Copier la clé publique du dépôt sur pg-standby

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Testez que les connexions peuvent être établies depuis le dépôt vers pg-standby et réciproquement.

dépôt **⇒** Tester la connexion depuis le dépôt vers pg-standby

```bash
sudo -u pgbackrest ssh postgres@pg-standby
```

pg-standby **⇒** Tester la connexion depuis pg-standby vers le dépôt

```bash
sudo -u postgres ssh pgbackrest@repository
```

### Standby chaud {#hot-standby}

Un serveur de secours actif effectue la réplication à l’aide de l’archive WAL et autorise les requêtes en lecture seule.

La configuration de pgBackRest est très similaire à celle de pg-primary, sauf que le type de récupération `standby` sera utilisé pour maintenir le cluster en mode récupération lorsque la fin du flux WAL aura été atteinte.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez pgBackRest sur le serveur de secours

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
log-level-file=detail
repo1-host=repository
```

Le cluster de démonstration doit être créé (même s'il sera écrasé lors de la restauration) afin de générer les fichiers de configuration PostgreSQL.

pg-standby **⇒** Créer un cluster de démonstration

```bash
sudo pg_createcluster 17 demo
```

À présent, le serveur de secours peut être créé avec la commande `restore`.

IMPORTANT :

Si le cluster doit être promu sans devenir le nouveau principal (par exemple pour des rapports ou des tests), utilisez `--archive-mode=off` ou définissez archive_mode=off dans `postgresql.conf` afin de désactiver l'archivage. Si l'archivage n'est pas désactivé, le dépôt risque d'être pollué par des WAL qui peuvent compliquer les restaurations.

pg-standby **⇒** Effectuer la restauration du cluster de secours démo

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:07:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:08:06
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:08:20
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-15 07:09:02 # recovery_target_time = '2026-10-15 07:08:16.882666+00'
# Removed by pgBackRest restore on 2026-10-15 07:09:02 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:09:02
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-15 07:08:49+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:09:24
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:09:49
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

La configuration est en cas de promotion du serveur de secours en serveur principal.

pg-standby:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurez PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

pg-standby **⇒** Démarrer PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

Le journal PostgreSQL fournit des informations précieuses sur la récupération. Notez notamment que le cluster est passé en mode standby et est prêt à accepter des connexions en lecture seule.

pg-standby **⇒** Examinez la sortie du journal PostgreSQL pour les messages indiquant une réussite

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 6 lines of output]
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
LOG:  entering standby mode
LOG:  redo starts at 0/24000028
LOG:  restored log file "000000070000000000000025" from archive
       [filtered 3 lines of output]
```

Une façon simple de vérifier que la réplication est correctement configurée consiste à créer une table sur pg-primary.

pg-primary **⇒** Créer une nouvelle table sur le serveur primaire

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Ensuite, interrogez la même table sur pg-standby.

pg-standby **⇒** Interroger une nouvelle table sur le serveur de secours

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

Qu'est-ce qui s'est mal passé ? Puisque PostgreSQL extrait les segments WAL de l'archive pour effectuer la réplication, les modifications ne seront pas visibles sur le serveur de secours tant que le segment WAL contenant ces modifications n'aura pas été transféré depuis pg-primary.

Cela peut être effectué manuellement en appelant `pg_switch_wal()`, ce qui transfère le segment WAL actuel vers l’archive (un nouveau segment WAL est créé pour contenir les modifications ultérieures).

pg-primary **⇒** Appel à `pg_switch_wal()`

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/260195C8    | 2026-10-15 07:09:54.192224+00
(1 row)
```

À présent, après un court délai, la table apparaîtra sur pg-standby.

pg-standby **⇒** La nouvelle table existe désormais sur le serveur de secours (peut nécessiter plusieurs tentatives)

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-15 07:09:58.574123+00
(1 row)
```

Vérifiez la configuration du serveur de secours pour accéder au dépôt.

pg-standby **⇒** Vérifier la configuration

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.60.0: --exec-id=527-f4cba4de --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### Réplication en streaming {#streaming-replication}

Au lieu de se fier uniquement à l’archive WAL, la réplication en streaming établit une connexion directe avec le principal et applique les modifications dès qu’elles sont effectuées sur ce dernier. Cela réduit considérablement le délai de latence entre le principal et le secondaire.

La réplication en streaming nécessite un utilisateur disposant du privilège de réplication.

pg-primary **⇒** Créer un utilisateur de réplication

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

Le fichier `pg_hba.conf` doit être mis à jour pour autoriser le serveur de secours à se connecter en tant qu'utilisateur de réplication. Veillez à remplacer l'adresse IP ci-dessous par l'adresse IP réelle de votre serveur pg-standby. Un rechargement sera nécessaire après la modification du fichier `pg_hba.conf`.

pg-primary **⇒** Créer une entrée `pg_hba.conf` pour l'utilisateur de réplication

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /etc/postgresql/17/demo/pg_hba.conf'
sudo pg_ctlcluster 17 demo reload
```

Le serveur de secours doit savoir comment contacter le serveur principal, donc le paramètre primary_conninfo sera configuré dans pgBackRest.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Définir primary_conninfo

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo
recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator

[global]
log-level-file=detail
repo1-host=repository
```

Il est possible de configurer un mot de passe dans le paramètre primary_conninfo, mais utiliser un fichier `.pgpass` est plus flexible et plus sécurisé.

pg-standby **⇒** Configurez le mot de passe de réplication dans le fichier `.pgpass`.

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/postgresql/.pgpass'
sudo -u postgres chmod 600 /var/lib/postgresql/.pgpass
```

À présent, le serveur de secours peut être créé avec la commande `restore`.

pg-standby **⇒** Arrêtez PostgreSQL et effectuez la restauration du cluster de secours démo

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:07:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:08:06
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:08:20
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-15 07:09:02 # recovery_target_time = '2026-10-15 07:08:16.882666+00'
# Removed by pgBackRest restore on 2026-10-15 07:09:02 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:09:02
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-15 07:08:49+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:09:24
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-15 07:10:01
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

NOTE :

Le paramètre primary_conninfo a été écrit dans le fichier `postgresql.auto.conf` car il a été configuré en tant que `recovery-option` dans `pgbackrest.conf`. L'option `--type=preserve` peut être utilisée avec `restore` pour laisser le fichier `postgresql.auto.conf` existant inchangé si ce comportement est préféré.

pg-standby **⇒** Démarrer PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

Le journal PostgreSQL confirmera que la réplication en flux a commencé.

pg-standby **⇒** Examinez la sortie du journal PostgreSQL pour les messages indiquant une réussite

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 13 lines of output]
LOG:  consistent recovery state reached at 0/25000050
LOG:  database system is ready to accept read-only connections
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

Désormais, lorsque vous créerez une table sur pg-primary, elle apparaîtra sur pg-standby rapidement et sans avoir à appeler `pg_switch_wal()`.

pg-primary **⇒** Créer une nouvelle table sur le serveur primaire

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-15 07:10:05.777744+00
(1 row)
```

pg-standby **⇒** Interroger une table sur le serveur de secours

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-15 07:10:05.882375+00
(1 row)
```

--------

## Stanzas multiples {#multiple-stanzas}

pgBackRest prend en charge plusieurs stanzas. L'utilisation la plus courante consiste à partager un hôte de dépôt entre plusieurs stanzas.


### Installation {#installation-3}

Un nouvel hôte nommé pg-alt est créé pour exécuter le nouveau primaire.

Installer pgBackRest à partir d’un paquet est préférable à la compilation à partir des sources. Lors de l’installation à partir d’un paquet, les autres instructions de cette section sont généralement inutiles, mais il se peut qu’un paquet omette de créer un répertoire ou applique des permissions incorrectes. Dans ce cas, il peut être nécessaire de créer manuellement les répertoires ou de mettre à jour les permissions.

Les paquets Debian/Ubuntu pour pgBackRest sont disponibles sur [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si des paquets ne sont pas fournis pour votre distribution/version, vous pouvez [compiler à partir des sources](#build) puis procéder à l'installation manuelle comme indiqué ici.

pg-alt **⇒** Installer les dépendances

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-alt **⇒** Copier le binaire pgBackRest depuis l'hôte de compilation

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest nécessite des répertoires pour les journaux et la configuration, ainsi qu'un fichier de configuration.

pg-alt **⇒** Créer le fichier de configuration et les répertoires pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Configuration d'un accès SSH sans mot de passe {#setup-passwordless-ssh-2}

pgBackRest peut utiliser SSH sans mot de passe pour permettre la communication entre les hôtes. Il est également possible d'utiliser TLS, voir [Configurer TLS](/fr/pgbackrest/user-guide-rhel/#configuration).

pg-alt **⇒** Créer une paire de clés hôte pg-alt

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Échanger les clés entre le dépôt et pg-alt.

dépôt **⇒** Copiez la clé publique pg-alt vers le dépôt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-alt cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-alt **⇒** Copier la clé publique du dépôt sur pg-alt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Testez que les connexions peuvent être établies depuis le dépôt vers pg-alt et réciproquement.

dépôt **⇒** Tester la connexion depuis le dépôt vers pg-alt

```bash
sudo -u pgbackrest ssh postgres@pg-alt
```

pg-alt **⇒** Tester la connexion depuis pg-alt vers le dépôt

```bash
sudo -u postgres ssh pgbackrest@repository
```

### Configuration {#configuration-1}

La configuration de pgBackRest est presque identique à celle de pg-primary, sauf que la stanza `demo-alt` sera utilisée, de sorte que les sauvegardes et l'archive seront stockées dans un emplacement séparé.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez pgBackRest sur le nouveau serveur primaire

```ini
[demo-alt]
pg1-path=/var/lib/postgresql/17/demo

[global]
log-level-file=detail
repo1-host=repository
```

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez `pg1-host`/`pg1-host-user` et `pg1-path`

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/17/demo

[demo-alt]
pg1-host=pg-alt
pg1-path=/var/lib/postgresql/17/demo

[global]
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

### Configurer un cluster de démonstration {#setup-demo-cluster-1}

pg-alt **⇒** Créer le cluster de démonstration

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 101:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

pg-alt:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurer les paramètres PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'
archive_mode = on
```

pg-alt **⇒** Démarrer le cluster de démonstration

```bash
sudo pg_ctlcluster 17 demo restart
```

### Créer la stanza et vérifier la configuration {#create-the-stanza-and-check-configuration}

La commande `stanza-create` doit être exécutée pour initialiser la stanza. Il est recommandé d'exécuter la commande `check` après `stanza-create` afin de vérifier que l'archivage et les sauvegardes sont correctement configurés.

pg-alt **⇒** Créer la stanza et vérifier la configuration

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.60.0: --exec-id=383-926d83c6 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.60.0: --exec-id=393-ca3e0098 --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000001-42e768a79e0022564a2c378e7beb646154378858.gz' on repo1
P00   INFO: check command end: completed successfully
```

Si la commande `check` est exécutée depuis l'hôte du dépôt, tous les stanzas seront vérifiés.

dépôt **⇒** Vérifiez la configuration de tous les stanzas

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.60.0: --exec-id=1261-3d28e169 --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/000000070000000000000027-7a7e51240e75814494d1baf706cd0ccbc34e0a20.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000002-eb6548b6d19132f0460998587116870ef72ae694.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## Archivage asynchrone {#asynchronous-archiving}

L'archivage asynchrone est activé avec l'option `archive-async`. Cette option permet une opération asynchrone pour les commandes `archive-push` et `archive-get`.

Un chemin de tampon est requis. Les commandes stockeront les données temporaires ici, mais chaque commande fonctionne de manière assez différente ; l'utilisation du chemin de tampon est donc décrite en détail dans chaque section.

pg-primary **⇒** Créer le répertoire de file d'attente

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** Créer le répertoire de tampon

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

Le chemin d’attente doit être configuré et l’archivage asynchrone activé. L’archivage asynchrone apporte automatiquement certains avantages en réduisant le nombre de connexions établies vers le stockage distant, mais la configuration de `process-max` peut améliorer considérablement les performances en parallélisant les opérations. Veillez à ne pas définir `process-max` trop élevé afin de ne pas affecter les opérations normales de la base de données.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez le chemin de spool et l'archivage asynchrone

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo

[global]
archive-async=y
log-level-file=detail
repo1-host=repository
spool-path=/var/spool/pgbackrest

[global:archive-get]
process-max=2

[global:archive-push]
process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez le chemin de spool et l'archivage asynchrone

```ini
[demo]
pg1-path=/var/lib/postgresql/17/demo
recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator

[global]
archive-async=y
log-level-file=detail
repo1-host=repository
spool-path=/var/spool/pgbackrest

[global:archive-get]
process-max=2

[global:archive-push]
process-max=2
```

NOTE :

`process-max` est configuré à l'aide de sections de commande afin que l'option ne soit pas utilisée lors de la sauvegarde ni de la restauration. Cela permet également d'attribuer des valeurs différentes à `archive-push` et `archive-get`.

À des fins de démonstration, la réplication en streaming sera interrompue afin de forcer PostgreSQL à récupérer les WAL à l’aide de la commande restore_command.

pg-primary **⇒** Interrompre la réplication en continu en modifiant le mot de passe de réplication

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** Redémarrer le serveur de secours pour interrompre la connexion

```bash
sudo pg_ctlcluster 17 demo restart
```

### Archivage push {#archive-push}

La commande asynchrone `archive-push` déplace l'archivage des WAL vers un processus (ou plusieurs processus) distinct pour améliorer le débit. Elle fonctionne en « regardant à l'avance » pour déterminer quels segments WAL sont prêts à être archivés, au-delà de la demande actuelle de PostgreSQL via le `archive_command`. Les segments WAL sont transférés directement depuis le répertoire `pg_xlog`/`pg_wal` et la réussite n'est retournée par le `archive_command` que lorsque le segment WAL a été stocké en toute sécurité dans l'archive.

Le répertoire de stockage temporaire contient l'état actuel de l'archivage des WAL. Les fichiers d'état écrits dans le répertoire de stockage temporaire sont généralement de taille nulle et doivent consommer une quantité négligeable d'espace (au plus quelques mégaoctets) et très peu d'E/S. Toutes les informations contenues dans ce répertoire peuvent être régénérées, aussi n'est-il pas nécessaire de préserver le répertoire de stockage temporaire si le cluster est déplacé vers de nouveaux matériels.

IMPORTANT :

Dans l’implémentation originale de l’archivage asynchrone, les segments WAL étaient copiés dans le répertoire tampon avant compression et transfert. La nouvelle implémentation copie directement les segments WAL depuis le répertoire `pg_xlog`. Si l’archivage asynchrone était utilisé dans la version 1.12 ou antérieure, lisez attentivement les notes de publication de la version 1.13 avant de procéder à la mise à jour.

Le fichier `[stanza]-archive-push-async.log` peut être utilisé pour surveiller l'activité du processus asynchrone. Une bonne manière de tester cela consiste à envoyer rapidement un nombre important de segments WAL.

pg-primary **⇒** Test de l'archivage asynchrone parallèle

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.60.0: --exec-id=2721-c7d903d7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/00000007000000000000002D-0d4c29773b9d645c758b34c45433b612863e0611.gz' on repo1
P00   INFO: check command end: completed successfully
```

Le fichier journal contiendra désormais une activité parallèle et asynchrone.

pg-primary **⇒** Vérifier les résultats dans le journal

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.60.0: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2710-237a82c1 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.60.0: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2728-64e54d04 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
```

### Récupération d'archive {#archive-get}

La commande asynchrone `archive-get` maintient une file locale de WAL afin d'améliorer le débit. Si un segment de WAL n'est pas présent dans la file, il est récupéré à partir du dépôt, accompagné de suffisamment de segments de WAL consécutifs pour remplir la file. La taille maximale de la file est définie par `archive-get-queue-max`. Chaque fois que la file est à moins de la moitié pleine, davantage de WAL est récupéré afin de la remplir.

L'opération asynchrone est particulièrement utile dans les environnements qui génèrent beaucoup de WAL ou qui disposent d'une connexion à haute latence avec le stockage du dépôt (par exemple, S3 ou d'autres magasins d'objets). Dans le cas d'une connexion à haute latence, il peut être pertinent d'augmenter `process-max`.

Le fichier `[stanza]-archive-get-async.log` peut être utilisé pour surveiller l'activité du processus asynchrone.

pg-standby **⇒** Vérifier les résultats dans le journal

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.60.0: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=738-f822f931 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P02 DETAIL: found 000000070000000000000025 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000024 in the repo1: 17-1 archive
P02 DETAIL: found 000000070000000000000026 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000027 in the repo1: 17-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00   INFO: archive-get:async command end: completed successfully
       [filtered 11 lines of output]
```

pg-primary **⇒** Corriger la réplication en streaming en modifiant le mot de passe de réplication

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## Sauvegarde à partir d'un serveur de secours {#backup-from-a-standby}

pgBackRest peut effectuer des sauvegardes sur une instance de secours au lieu du serveur principal. Les sauvegardes sur instance de secours nécessitent que l'hôte pg-standby soit configuré et que l'option `backup-standby` soit activée. Si plusieurs instances de secours sont configurées, la première instance de secours en cours d'exécution trouvée sera utilisée pour la sauvegarde.

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Configurez `pg2-host`/`pg2-host-user` et `pg2-path`

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/17/demo
pg2-host=pg-standby
pg2-path=/var/lib/postgresql/17/demo

[demo-alt]
pg1-host=pg-alt
pg1-path=/var/lib/postgresql/17/demo

[global]
backup-standby=y
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

La base primaire comme la base standby sont nécessaires pour effectuer la sauvegarde, bien que l'immense majorité des fichiers soient copiés depuis le standby afin de réduire la charge du primaire. Les hôtes de base de données peuvent être configurés dans n'importe quel ordre ; pgBackRest détermine automatiquement lequel est primaire et lequel est standby.

dépôt **⇒** Effectuer une sauvegarde du cluster de démonstration depuis pg2

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P01 DETAIL: backup file pg-primary:/var/lib/postgresql/17/demo/global/pg_control (8KB, 0.53%) checksum 8904c4227b3209010e9fa7a5826fc8691fb9a317
P01 DETAIL: match file from prior backup pg-primary:/var/lib/postgresql/17/demo/pg_logical/replorigin_checkpoint (8B, 0.53%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
P02 DETAIL: backup file pg-standby:/var/lib/postgresql/17/demo/base/5/1249 (448KB, 30.16%) checksum bcc99e003ab9acafa9dcae4abf14879526f8658f
       [filtered 1278 lines of output]
```

Cette sauvegarde incrémentielle montre que la majeure partie des fichiers provient de l'hôte pg-standby et qu'un petit nombre provient de l'hôte pg-primary.

pgBackRest crée une sauvegarde depuis un serveur de secours identique à celle effectuée sur le serveur principal. Il procède en lançant/arrêtant la sauvegarde sur l'hôte pg-primary, en copiant uniquement les fichiers répliqués depuis l'hôte pg-standby, puis en copiant les quelques fichiers restants depuis l'hôte pg-primary. Cela signifie que les journaux et les statistiques de la base de données principale seront inclus dans la sauvegarde.


--------

## Mise à jour de PostgreSQL {#upgrading-postgresql}

Immédiatement après la mise à niveau de PostgreSQL vers une nouvelle version majeure, le `pg-path` de toutes les configurations pgBackRest doit être défini sur le nouvel emplacement de la base de données, puis la commande `stanza-upgrade` doit être exécutée. Si plusieurs dépôts sont configurés sur l'hôte, le stanza sera mis à niveau sur chacun. Si la base de données est hors ligne, utilisez l'option `--no-online`.

Les instructions suivantes ne constituent pas un guide complet de mise à jour de PostgreSQL, mais décrivent le processus général de mise à jour d’un nœud principal et d’un nœud secondaire, dans le but de démontrer les étapes nécessaires à la reconfiguration de pgBackRest. Il est recommandé de prendre une sauvegarde avant la mise à jour.

pg-primary **⇒** Arrêt de l'ancien cluster

```bash
sudo pg_ctlcluster 17 demo stop
```

Arrêtez l'ancien cluster sur le serveur de secours, car il sera restauré à partir du cluster nouvellement mis à jour.

pg-standby **⇒** Arrêter l'ancien cluster

```bash
sudo pg_ctlcluster 17 demo stop
```

Créez le nouveau cluster et effectuez la mise à jour.

pg-primary **⇒** Créer un nouveau cluster et effectuer la mise à jour

```bash
sudo -u postgres /usr/lib/postgresql/18/bin/initdb \
       -D /var/lib/postgresql/18/demo -k -A peer
sudo pg_createcluster 18 demo
sudo -u postgres sh -c 'cd /var/lib/postgresql && \
       /usr/lib/postgresql/18/bin/pg_upgrade \
       --old-bindir=/usr/lib/postgresql/17/bin \
       --new-bindir=/usr/lib/postgresql/18/bin \
       --old-datadir=/var/lib/postgresql/17/demo \
       --new-datadir=/var/lib/postgresql/18/demo \
       --old-options=" -c config_file=/etc/postgresql/17/demo/postgresql.conf" \
       --new-options=" -c config_file=/etc/postgresql/18/demo/postgresql.conf"'
```

```text
       [filtered 44 lines of output]
Checking for extension updates                                ok

Upgrade Complete
----------------
Some statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

Configurez les paramètres du nouveau cluster et le port.

pg-primary:`/etc/postgresql/18/demo/postgresql.conf` **⇒** Configurez PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'
archive_mode = on
```

Mettez à jour la configuration de pgBackRest sur tous les systèmes pour qu’elle pointe vers le nouveau cluster.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Mettre à jour `pg1-path`

```ini
[demo]
pg1-path=/var/lib/postgresql/18/demo

[global]
archive-async=y
log-level-file=detail
repo1-host=repository
spool-path=/var/spool/pgbackrest

[global:archive-get]
process-max=2

[global:archive-push]
process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Mettre à jour `pg-path`

```ini
[demo]
pg1-path=/var/lib/postgresql/18/demo
recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator

[global]
archive-async=y
log-level-file=detail
repo1-host=repository
spool-path=/var/spool/pgbackrest

[global:archive-get]
process-max=2

[global:archive-push]
process-max=2
```

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Mettre à jour `pg1-path` et `pg2-path`, désactiver la sauvegarde depuis le serveur de secours

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/18/demo
pg2-host=pg-standby
pg2-path=/var/lib/postgresql/18/demo

[demo-alt]
pg1-host=pg-alt
pg1-path=/var/lib/postgresql/17/demo

[global]
backup-standby=n
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```

pg-primary **⇒** Copie de la configuration HBA

```bash
sudo cp /etc/postgresql/17/demo/pg_hba.conf \
       /etc/postgresql/18/demo/pg_hba.conf
```

Avant de démarrer le nouveau cluster, la commande `stanza-upgrade` doit être exécutée.

pg-primary **⇒** Mettre à jour la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.60.0: --exec-id=3148-2038b641 --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/postgresql/18/demo --repo1-host=repository --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

Démarrer le nouveau cluster et confirmer qu'il est correctement installé.

pg-primary **⇒** Démarrer un nouveau cluster

```bash
sudo pg_ctlcluster 18 demo start
```

Testez la configuration à l'aide de la commande `check`.

pg-primary **⇒** Vérifier la configuration

```bash
sudo pg_lsclusters
sudo -u postgres pgbackrest --stanza=demo check
```

Supprimez l'ancien cluster.

pg-primary **⇒** Supprimer l'ancien cluster

```bash
sudo pg_dropcluster 17 demo
```

Installez les nouveaux binaires PostgreSQL sur le serveur de secours et créez le cluster.

pg-standby **⇒** Supprimer l'ancien cluster et créer le nouveau cluster

```bash
sudo pg_dropcluster 17 demo
sudo pg_createcluster 18 demo
```

Exécutez `check` sur l'hôte du dépôt. L'avertissement concernant l'arrêt du serveur secondaire est attendu, car le cluster secondaire est arrêté. L'exécution de cette commande montre que le serveur de dépôt est conscient de la présence du serveur secondaire et est correctement configuré pour le serveur principal.

dépôt **⇒** Vérifier la configuration

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 ssh protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

Effectuez une sauvegarde complète sur le cluster nouvellement configuré, puis restaurez le serveur de secours à partir de cette sauvegarde. Le type de sauvegarde sera automatiquement modifié en `full` si `incr` ou `diff` est demandé.

dépôt **⇒** Exécuter une sauvegarde complète

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** Effectuer la restauration du cluster de secours démo

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
```

pg-standby **⇒** Démarrer PostgreSQL et vérifier la configuration de pgBackRest

```bash
sudo pg_ctlcluster 18 demo start
sudo -u postgres pgbackrest --stanza=demo check
```

La sauvegarde depuis un serveur de secours peut maintenant être activée, puisque le serveur de secours est restauré.

dépôt : `/etc/pgbackrest/pgbackrest.conf` **⇒** Réactiver la sauvegarde depuis le serveur secondaire

```ini
[demo]
pg1-host=pg-primary
pg1-path=/var/lib/postgresql/18/demo
pg2-host=pg-standby
pg2-path=/var/lib/postgresql/18/demo

[demo-alt]
pg1-host=pg-alt
pg1-path=/var/lib/postgresql/17/demo

[global]
backup-standby=y
process-max=3
repo1-path=/var/lib/pgbackrest
repo1-retention-full=2
start-fast=y
```
