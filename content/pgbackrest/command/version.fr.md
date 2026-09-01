---
title: "Commande Version (version)"
linkTitle: "version"
weight: 200
description: "Référence des options et du comportement de la commande pgBackRest `version`."
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [Référence]
aliases: [/docs/pgbackrest/command/version/]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

Affiche la version de pgBackRest installée.

## Options de commande {#command-options}

### Option de sortie (`--output`) {#output-option---output}

Type de sortie.

Les types de sortie suivants sont pris en charge :

- `text` - Affiche la version installée de pgBackRest sous forme de texte.
- `num` - Affiche la version installée de pgBackRest sous forme d'entier.

```yaml
default: text
example: --output=num
```
