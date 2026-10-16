---
title: Plataformas compatibles
weight: 4800
description: Soporte de etcd para arquitecturas y sistemas operativos habituales
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/supported-platform.md"
---

## Niveles de soporte {#support-tiers}

etcd se ejecuta en diferentes plataformas, pero las garantías que ofrece dependen del
nivel de soporte de la plataforma:

- **Nivel 1**: con soporte total por parte de los [mantenedores de etcd][etcd maintainers]; se garantiza que etcd
  pasa todas las pruebas, incluidas las pruebas funcionales y de robustez.
- **Nivel 2**: se garantiza que etcd pasa las pruebas de integración y de extremo a extremo, pero
  no necesariamente las pruebas funcionales o de robustez.
- **Nivel 3**: se garantiza que etcd compila, puede estar probado ligeramente (o no), y
  por lo tanto debe considerarse _inestable_.

## Soporte actual {#current-support}

La siguiente tabla enumera las plataformas actualmente compatibles y su nivel de soporte
correspondiente en etcd:

| Arquitectura | Sistema operativo | Nivel de soporte |      Mantenedores     |
|:------------:|:-----------------:|:----------------:|:---------------------:|
| AMD64        | Linux             |      1           | [mantenedores de etcd][etcd maintainers] |
| ARM64        | Linux             |      1           | [mantenedores de etcd][etcd maintainers] |
| AMD64        | Darwin            |      3           |                       |
| ARM64        | Darwin            |      3           |                       |
| AMD64        | Windows           |      3           |                       |
| ppc64le      | Linux             |      3           |                       |
| s390x        | Linux             |      3           |                       |

Las plataformas no listadas no son compatibles.

## Soporte para una nueva plataforma {#supporting-a-new-platform}

¿Quieres contribuir a etcd como mantenedor «oficial» de una nueva plataforma? Además
de comprometerte a dar soporte a la plataforma, debes configurar la integración continua
(CI) de etcd de manera que cumpla los siguientes requisitos, según el nivel
de soporte:

| Integración continua de etcd           | Nivel 1  | Nivel 2  | Nivel 3  |
|---------------------------------------|:-------:|:-------:|:-------:|
| La compilación pasa                   | &check; | &check; | &check; |
| Las pruebas unitarias pasan           | &check; | &check; |         |
| Las pruebas de integración y de extremo a extremo pasan | &check; | &check; |         |
| Las pruebas de robustez pasan         | &check; |         |         |

Para ver un ejemplo de configuración de una CI de nivel 2 para ARM64, consulta la [PR de etcd #12928][etcd PR #12928].

## Plataformas no compatibles {#unsupported-platforms}

Para evitar ejecutar inadvertidamente un servidor de etcd en una plataforma no compatible, etcd
muestra un mensaje de advertencia y sale inmediatamente a menos que la variable de entorno
`ETCD_UNSUPPORTED_ARCH` esté establecida en la arquitectura de destino.

> [!WARNING]
> **Sistemas de 32 bits**
>   etcd tiene **problemas conocidos** en sistemas de 32 bits debido a un error en el runtime de Go.
>   Para más información, consulta el [issue de Go #599][go-issue] y la [nota sobre el error del paquete
>   atomic][go-atomic].
>
>   [go-atomic]: https://golang.org/pkg/sync/atomic/#pkg-note-BUG
>   [go-issue]: https://github.com/golang/go/issues/599

[etcd maintainers]: https://github.com/etcd-io/etcd/blob/main/OWNERS
[etcd PR #12928]: https://github.com/etcd-io/etcd/pull/12928
