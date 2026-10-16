---
title: "Comando de versión (version)"
linkTitle: "version"
weight: 200
description: "Referencia de las opciones y el comportamiento del comando `version` de pgBackRest."
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

Muestra la versión instalada de pgBackRest.

## Opciones del comando {#command-options}

### Opción de salida (`--output`) {#output-option---output}

Tipo de salida.

Se soportan los siguientes tipos de salida:

- `text` - Muestra la versión instalada de pgBackRest como texto.
- `num` - Muestra la versión instalada de pgBackRest como un número entero.

```yaml
default: text
example: --output=num
```
