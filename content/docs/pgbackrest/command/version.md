---
title: "Version Command (version)"
linkTitle: "version"
weight: 200
description: "Reference for pgBackRest `version` command options and behavior."
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [Reference]
---

> Source: [pgBackRest Command Docs: version](https://pgbackrest.org/command.html#command-version)

Displays installed pgBackRest version.

## Command Options

### Output Option (`--output`)

Output type.

The following output types are supported:

- `text` - Display the installed pgBackRest version as text.
- `num` - Display the installed pgBackRest version as an integer.

```yaml
default: text
example: --output=num
```
