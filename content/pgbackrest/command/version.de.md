---
title: "Versionsbefehl (version)"
linkTitle: "version"
weight: 200
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `version`."
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

Zeigt die installierte pgBackRest-Version an.

## Befehlsoptionen {#command-options}

### Ausgabeoption (`--output`) {#output-option---output}

Ausgabetyp.

Die folgenden Ausgabetypen werden unterstützt:

- `text` - Die installierte pgBackRest-Version als Text anzeigen.
- `num` - Die installierte pgBackRest-Version als Ganzzahl anzeigen.

```yaml
default: text
example: --output=num
```
