---
title: "Команда версии (version)"
linkTitle: "version"
weight: 200
description: "Справочник по параметрам и поведению команды pgBackRest `version`"
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [Справочник]
aliases: [/docs/pgbackrest/command/version/]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

Отображает установленную версию pgBackRest.

## Опции команды {#command-options}

### Параметр вывода (`--output`) {#output-option---output}

Тип вывода.

Поддерживаются следующие типы вывода:

- `text` — Отображает установленную версию pgBackRest в виде текста.  
- `num` — Отображает установленную версию pgBackRest в виде целого числа.

```yaml
default: text
example: --output=num
```
