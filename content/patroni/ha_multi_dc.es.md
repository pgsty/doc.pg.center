---
title: "Alta disponibilidad en múltiples centros de datos"
weight: 170
icon: fa-solid fa-globe
description: "Patrones de alta disponibilidad en múltiples centros de datos con replicación de Patroni."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/ha_multi_dc.html"
---

<a id="ha_multi_dc"></a>
La alta disponibilidad de un clúster de PostgreSQL desplegado en múltiples centros de datos se basa en la replicación, que puede ser síncrona o asíncrona (consulta los [modos de replicación](/es/patroni/replication_modes#replication_modes)).

En ambos casos, es importante tener claros los siguientes conceptos:

- Postgres puede ejecutarse como primario o como líder en espera solo cuando es propietario de la clave de líder y puede actualizarla.
- Debes ejecutar un número impar de nodos de etcd, ZooKeeper o Consul: ¡3 o 5!

--------

## Replicación síncrona {#synchronous-replication}

Para tener un clúster de múltiples centros de datos que pueda tolerar automáticamente la caída de una zona, se requiere un mínimo de 3.

El diagrama de arquitectura sería el siguiente:

![imagen](/img/patroni/multi-dc-synchronous-replication.png)

Debemos desplegar un clúster de etcd, ZooKeeper o Consul entre los diferentes centros de datos, con un mínimo de 3 nodos, uno en cada zona.

En cuanto a postgres, debemos desplegar al menos 2 nodos, en centros de datos diferentes. Luego tienes que establecer `synchronous_mode: true` en la [configuración dinámica](/es/patroni/config/dynamic#dynamic) global.

Esto habilita la replicación síncrona y el nodo primario elegirá uno de los nodos como síncrono.

--------

## Replicación asíncrona {#asynchronous-replication}

Con solo dos centros de datos, es mejor tener dos clústeres de etcd independientes y ejecutar un [clúster en espera](/es/patroni/standby_cluster#standby_cluster) de Patroni en el segundo centro de datos. Si el primer sitio se cae, puedes promover MANUALMENTE el [standby_cluster](/es/patroni/standby_cluster#standby_cluster).

El diagrama de arquitectura sería el siguiente:

![imagen](/img/patroni/multi-dc-asynchronous-replication.png)

La promoción automática no es posible, porque DC2 nunca podrá determinar el estado de DC1.

No debes usar `pg_ctl promote` en este escenario; necesitas «promover manualmente» el clúster en buen estado eliminando la sección [standby_cluster](/es/patroni/standby_cluster#standby_cluster) de la [configuración dinámica](/es/patroni/config/dynamic#dynamic).

> [!WARNING]
> Si el clúster origen sigue en ejecución y promueves el clúster en espera, creas un split-brain.

En caso de que quieras volver al estado «inicial», solo hay dos formas de resolverlo:

- Vuelve a añadir la sección standby_cluster y esto desencadenará `pg_rewind`; sin embargo, para que `pg_rewind` funcione correctamente, el clúster debe inicializarse con `data page checksums` (opción `--data-checksums` de `initdb`) y/o `wal_log_hints` debe establecerse en `on`, pero todavía existe la posibilidad de que `pg_rewind` falle por otros factores.
- Reconstruye el clúster en espera desde cero.

Antes de promover el clúster en espera hay que asegurarse manualmente de que el clúster origen esté detenido (STONITH). Cuando DC1 se recupera, el clúster debe convertirse en un clúster en espera.

Antes de hacer eso, puedes examinar manualmente la base de datos y extraer todos los cambios que ocurrieron entre el momento en que la red entre DC1 y DC2 dejó de funcionar y el momento en que detuviste manualmente el clúster en DC1.

Una vez extraídos, también puedes aplicar manualmente estos cambios al clúster en DC2.
