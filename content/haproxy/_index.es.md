---
title: "Documentación de HAProxy 3.4.6-66"
linkTitle: HAProxy
weight: 50
description: "Edición Markdown completa en español de las guías de inicio, configuración y gestión de HAProxy 3.4"
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [Referencia]
upstream_source: haproxy
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy
  type: docs
  module: [HAPROXY]
---

**HAProxy** es un proxy inverso gratuito, rápido y fiable para la alta disponibilidad, el balanceo de carga TCP y
HTTP, y la gestión del tráfico de aplicaciones. Este componente contiene la traducción completa al español de
los tres manuales principales de HAProxy 3.4, reorganizada como una secuencia de lectura plana en Markdown para OINK.

Esta edición sigue los manuales oficiales en inglés de la rama de mantenimiento en la instantánea `3.4.6-66`.
La última versión estable es `3.4.6` (`v3.4.6`); la instantánea incluye cambios de documentación realizados
después de esa versión. Su fuente exacta es el commit
[`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8).

## Elige un manual {#choose-a-manual}

- [Guía de inicio](/es/haproxy/load-balancing/) — 9 temas sobre conceptos de balanceo de carga, arquitectura de HAProxy, funcionalidades, dimensionamiento, versiones y ecosistema.
- [Manual de configuración](/es/haproxy/http-fundamentals/) — 12 capítulos que cubren proxies, ACL, muestras, registro, filtros y cada familia de opciones.
- [Guía de gestión](/es/haproxy/prerequisites/) — 13 capítulos sobre arranque, recargas, recursos, registro, estadísticas, CLI en tiempo de ejecución, depuración y seguridad.
{.cards}

## Cobertura de la edición {#edition-coverage}

| Manual | Fuente upstream | Organización local |
| --- | ---: | ---: |
| Guía de inicio | 1,695 líneas | 9 páginas planas de temas |
| Manual de configuración | 33,216 líneas | 12 páginas planas de capítulos |
| Guía de gestión | 5,305 líneas | 13 páginas planas de capítulos |

Las 34 páginas de lectura se encuentran directamente bajo la raíz del componente HAProxy. Tres marcadores divisores
sin enlaces separan los manuales en la barra lateral sin añadir niveles de directorio ni paradas de paginación.

Los manuales originales completos están disponibles en la revisión upstream fija enlazada más arriba. El
[aviso de licencia upstream](/third_party/haproxy/LICENSE) y el [texto GPLv2](/third_party/haproxy/GPL-2.0) se
publican junto a los manuales. Existe una edición complementaria revisada en chino simplificado disponible para
cada página.
