---
title: "Commande d'arrêt (stop)"
linkTitle: "stop"
weight: 180
description: "Référence des options et du comportement de la commande pgBackRest `stop`."
icon: fa-solid fa-stop
module: [PGBACKREST]
categories: [Référence]
aliases: [/pgbackrest/command/stop/]
upstream_link: "https://pgbackrest.org/command.html#command-stop"
---

N'autorise aucun nouveau processus pgBackRest à s'exécuter. Par défaut, les processus en cours d'exécution sont autorisés à se terminer correctement. Utilisez l'option `--force` pour terminer les processus en cours.

Les processus pgBackRest retourneront une erreur s’ils sont exécutés après la fin de la commande d’arrêt. Consultez [Démarrage et arrêt](/fr/docs/pgbackrest/user-guide/#starting-and-stopping) pour plus d’informations et d’exemples.

## Options de commande {#command-options}

### Option de forçage (`--force`) {#force-option---force}

Forcer l’arrêt de tous les processus pgBackRest.

Cette option enverra des signaux TERM à tous les processus pgBackRest en cours d'exécution afin d'effectuer une fermeture correcte mais immédiate. Notez qu'elle arrêtera également les processus lancés depuis un autre système mais dont les processus distants s'exécutent sur le système actuel. Par exemple, si une sauvegarde a été lancée depuis le serveur de sauvegarde, l'exécution de `stop --force` sur le serveur de base de données arrêtera le processus de sauvegarde sur le serveur de sauvegarde.

```yaml
default: n
example: --force
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

### Option stanza (`--stanza`) {#stanza-option---stanza}

Définit la stanza.

Une stanza est la configuration d'un cluster de base de données PostgreSQL qui définit son emplacement, la manière dont il sera sauvegardé, les options d'archivage, etc. La plupart des serveurs de base de données n'ont qu'un seul cluster PostgreSQL et donc une seule stanza, tandis que les serveurs de sauvegarde ont une stanza pour chaque cluster de base de données à sauvegarder.

Il est tentant de nommer la stanza en fonction du cluster principal, mais un nom plus pertinent décrit les bases de données contenues dans le cluster. Étant donné que le nom de la stanza sera utilisé pour le principal et toutes les répliques, il est préférable de choisir un nom qui décrit la fonction réelle du cluster, par exemple app ou dw, plutôt que le nom local du cluster, comme main ou prod.

```yaml
example: --stanza=main
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
