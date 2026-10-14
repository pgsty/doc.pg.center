---
title: "Hilfebefehl (help)"
linkTitle: "help"
weight: 70
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `help`."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

Die Hilfe ist in drei Ebenen gegliedert. Ohne Angabe eines Befehls wird die allgemeine Hilfe angezeigt. Wird ein Befehl angegeben (z. B. `pgbackrest help backup`), erscheint eine vollständige Beschreibung des Befehls mit einer Liste der zulässigen Optionen. Wird zusätzlich eine Option angegeben (z. B. `pgbackrest help backup type`), erscheint eine vollständige Beschreibung dieser Option für den jeweiligen Befehl.

## Befehlsoptionen {#command-options}

### Option zur Anzeige der Hilfe (`--help`) {#display-help-option---help}

Hilfe anzeigen.

Zeigt die Hilfe auch dann an, wenn der Befehl `help` nicht angegeben wurde, und hat Vorrang vor der Option `--version`.

```yaml
default: n
example: --help
```

### Option zur Anzeige der Version (`--version`) {#display-version-option---version}

Version anzeigen.

Zeigt die Version auch dann an, wenn weder der Befehl `version` noch `help` angegeben wurde.

```yaml
default: n
example: --version
```
