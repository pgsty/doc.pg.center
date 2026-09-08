---
title: "Команда справки (help)"
linkTitle: "help"
weight: 70
description: "Справочник по параметрам и поведению команды pgBackRest `help`."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Справочник]
aliases: [/docs/pgbackrest/command/help/]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

Предоставляется три уровня справки. Если команда не указана, будет отображена общая справка. Если указана команда (e.g. `pgbackrest help backup`), будет отображено полное описание команды вместе со списком допустимых параметров. Если указать параметр вместе с командой (e.g. `pgbackrest help backup type`), будет отображено полное описание параметра применительно к команде.

## Опции команды {#command-options}

### Показать сведения о параметре помощи (`--help`) {#display-help-option---help}

Показать справку.

Отображает справку даже если команда `help` не указана и переопределяет опцию `--version`.

```yaml
default: n
example: --help
```

### Параметр отображения версии (`--version`) {#display-version-option---version}

Показать версию.

Отображает версию даже если не указаны команды `version` или `help`.

```yaml
default: n
example: --version
```
