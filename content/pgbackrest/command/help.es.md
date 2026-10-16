---
title: "Comando de ayuda (help)"
linkTitle: "help"
weight: 70
description: "Referencia de las opciones y el comportamiento del comando `help` de pgBackRest."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

Se proporcionan tres niveles de ayuda. Si no se especifica ningún comando, se mostrará la ayuda general. Si se especifica un comando (p. ej., `pgbackrest help backup`), se mostrará una descripción completa del comando junto con una lista de las opciones válidas. Si se especifica una opción además de un comando (p. ej., `pgbackrest help backup type`), se mostrará una descripción completa de la opción tal como se aplica al comando.

## Opciones del comando {#command-options}

### Opción de mostrar la ayuda (`--help`) {#display-help-option---help}

Muestra la ayuda.

Muestra la ayuda incluso si no se especifica el comando `help` y prevalece sobre la opción `--version`.

```yaml
default: n
example: --help
```

### Opción de mostrar la versión (`--version`) {#display-version-option---version}

Muestra la versión.

Muestra la versión incluso si no se especifica el comando `version` o `help`.

```yaml
default: n
example: --version
```
