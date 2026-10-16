---
title: "Informes de ejemplo"
linkTitle: "Informes de ejemplo"
weight: 80
description: "Abre informes de pgBadger completos, solo de errores e incrementales"
search_keywords: [--anonymize, anonymize]
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [Referencia]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

El contenido de ejemplo fue generado por pgBadger 11.8 en mayo de 2022. La navegación de los informes, los gráficos, los estilos y los scripts están disponibles sin conexión.

| Ejemplo | Qué demuestra | Copia local |
|---|---|---|
| Informe completo | Actividad de PostgreSQL junto con estadísticas de PgBouncer | [Abrir el informe completo](/third_party/pgbadger/examples/sample.html) |
| Informe incremental | Índice de calendario, agregación semanal y páginas diarias | [Abrir el índice incremental](/third_party/pgbadger/examples/report/index.html) |
| Errores y eventos | Un informe restringido a errores y eventos operativos | [Abrir el informe de errores](/third_party/pgbadger/examples/errors.html) |

## Informe completo {#complete-report}

El informe completo es un documento HTML autónomo. Usa su navegación superior para examinar las estadísticas globales, las consultas, las sesiones, las conexiones, los archivos temporales, los checkpoints, la actividad de autovacuum, los bloqueos y los gráficos específicos de PgBouncer.

Los datos son un conjunto de demostración, no una referencia comparativa actual. Los valores, las versiones de PostgreSQL y la interfaz de pgBadger incrustada reflejan la fecha de generación del informe.

## Jerarquía incremental {#incremental-hierarchy}

El ejemplo incremental conserva la estructura completa de enlaces:

```text
report/
├── index.html
├── 2012/
│   ├── week-49/index.html
│   ├── week-50/index.html
│   └── 12/06 … 12/index.html
└── 11/
    ├── pgbadger.min.css
    ├── pgbadger.min.js
    └── recursos de gráficos y de interfaz empaquetados
```

El índice superior enlaza a dos informes semanales y siete informes diarios. Mover solo `index.html` rompe sus enlaces relativos; mantén el árbol de directorios completo junto.

## Seguridad y privacidad {#security-and-privacy}

Los informes reales pueden exponer texto SQL, valores de enlace, nombres de bases de datos y de usuarios, nombres de aplicaciones, direcciones de clientes, detalles de errores y patrones de carga. Antes de publicar un informe:

- usa `--anonymize` cuando no se necesiten los literales;
- aplica filtros de inclusión/exclusión antes de generar el informe;
- inspecciona el HTML final o los datos exportados, no solo la línea de comandos;
- protege la ubicación del informe con el mismo cuidado que los registros operativos.
