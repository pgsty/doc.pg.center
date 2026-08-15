---
title: "Help Command (help)"
linkTitle: "help"
weight: 70
description: "Reference for pgBackRest `help` command options and behavior."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Reference]
---

> Source: [pgBackRest Command Docs: help](https://pgbackrest.org/command.html#command-help)

Three levels of help are provided. If no command is specified then general help will be displayed. If a command is specified (e.g. `pgbackrest help backup`) then a full description of the command will be displayed along with a list of valid options. If an option is specified in addition to a command (e.g. `pgbackrest help backup type`) then a full description of the option as it applies to the command will be displayed.

## Command Options

### Display Help Option (`--help`)

Display help.

Displays help even if the `help` command is not specified and overrides the `--version` option.

```yaml
default: n
example: --help
```

### Display Version Option (`--version`)

Display version.

Displays version even if the `version` or `help` command is not specified.

```yaml
default: n
example: --version
```
