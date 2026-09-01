---
title: "Commande d'aide (help)"
linkTitle: "help"
weight: 70
description: "Référence des options et du comportement de la commande pgBackRest `help`."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Référence]
aliases: [/docs/pgbackrest/command/help/]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

Trois niveaux d’aide sont proposés. Si aucune commande n’est spécifiée, une aide générale sera affichée. Si une commande est précisée (par exemple `pgbackrest help backup`), une description complète de la commande sera affichée, accompagnée d’une liste des options valides. Si une option est précisée en plus d’une commande (par exemple `pgbackrest help backup type`), une description complète de l’option telle qu’elle s’applique à la commande sera affichée.

## Options de commande {#command-options}

### Afficher l’option d’aide (`--help`) {#display-help-option---help}

Affiche l’aide.

Affiche l’aide même si la commande `help` n’est pas précisée et ignore l’option `--version`.

```yaml
default: n
example: --help
```

### Option d'affichage de la version (`--version`) {#display-version-option---version}

Afficher la version.

Affiche la version même si la commande `version` ou `help` n'est pas précisée.

```yaml
default: n
example: --version
```
