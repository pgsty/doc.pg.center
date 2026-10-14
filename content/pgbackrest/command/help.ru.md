---
title: "Команда справки (help)"
linkTitle: "help"
weight: 70
description: "Справочник по параметрам и поведению команды pgBackRest `help`."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Справочник]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

Предоставляется три уровня справки. Если команда не указана, выводится общая справка. Если указана команда (например, `pgbackrest help backup`), выводится её полное описание со списком допустимых параметров. Если вместе с командой указан параметр (например, `pgbackrest help backup type`), выводится полное описание этого параметра применительно к команде.

## Параметры команды {#command-options}

### Параметр вывода справки (`--help`) {#display-help-option---help}

Вывод справки.

Выводит справку, даже если команда `help` не указана, и переопределяет параметр `--version`.

```yaml
default: n
example: --help
```

### Параметр вывода версии (`--version`) {#display-version-option---version}

Вывод версии.

Отображает версию, даже если не указаны команды `version` или `help`.

```yaml
default: n
example: --version
```
