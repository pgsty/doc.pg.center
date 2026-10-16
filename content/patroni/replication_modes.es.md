---
title: "Modos de replicación"
weight: 70
icon: fa-solid fa-share-nodes
description: "Modos de replicación asíncrona y síncrona gestionados por Patroni."
module: [PATRONI]
categories: [Concepto]
upstream_link: "https://patroni.readthedocs.io/en/latest/replication_modes.html"
---

<a id="replication_modes"></a>
Patroni utiliza la replicación por streaming de PostgreSQL. Para más información sobre la replicación por streaming, consulta la [documentación de Postgres](http://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION). De forma predeterminada, Patroni configura PostgreSQL para la replicación asíncrona. La elección de tu esquema de replicación depende de tus consideraciones de negocio. Investiga tanto la replicación asíncrona como la síncrona, así como otras soluciones de alta disponibilidad, para determinar cuál es la mejor solución para ti.

--------

## Durabilidad del modo asíncrono {#asynchronous-mode-durability}

En el modo asíncrono, el clúster puede perder algunas transacciones confirmadas para garantizar la disponibilidad. Cuando el servidor primario falla o deja de estar disponible por cualquier otro motivo, Patroni promoverá automáticamente a primario un nodo en espera suficientemente saludable. Las transacciones que no se hayan replicado a ese nodo en espera permanecen en una «línea de tiempo bifurcada» en el primario y son, en la práctica, irrecuperables[^1].

La cantidad de transacciones que pueden perderse se controla mediante el parámetro `maximum_lag_on_failover`. Como la posición del registro de transacciones del primario no se muestrea en tiempo real, en realidad la cantidad de datos perdidos en una conmutación por error está limitada, en el peor de los casos, a `maximum_lag_on_failover` bytes de registro de transacciones más la cantidad escrita en los últimos `ttl` segundos (`loop_wait`/2 segundos en el caso promedio). Sin embargo, el retraso de replicación típico en estado estable está muy por debajo de un segundo.

De forma predeterminada, al ejecutar las elecciones de líder, Patroni no tiene en cuenta la línea de tiempo actual de las réplicas, lo que en algunos casos podría ser un comportamiento indeseable. Establecer `check_timeline` en `true` impide que un nodo cuya línea de tiempo sea más antigua que la última línea de tiempo conocida del clúster, o que no pueda determinarse, se convierta en el nuevo líder.

--------

## Replicación síncrona de PostgreSQL {#postgresql-synchronous-replication}

Puedes usar la [replicación síncrona](http://www.postgresql.org/docs/current/static/warm-standby.html#SYNCHRONOUS-REPLICATION) de Postgres con Patroni. La replicación síncrona garantiza la consistencia en todo el clúster al confirmar que las escrituras se han guardado en un secundario antes de responder con éxito al cliente que se conecta. El costo de la replicación síncrona: mayor latencia y menor rendimiento en las escrituras. Este rendimiento se ve afectado por el rendimiento de la red.

En entornos de centro de datos alojados (como AWS, Rackspace o cualquier red que no controles), la replicación síncrona incrementa significativamente la variabilidad del rendimiento de escritura. Si las réplicas dejan de ser accesibles desde el líder, el líder pasa a ser efectivamente de solo lectura.

Para habilitar una prueba sencilla de replicación síncrona, añade las siguientes líneas a la sección `parameters` de tus archivos de configuración YAML:

```yaml
synchronous_commit: "on"
synchronous_standby_names: "*"
```

Al usar la replicación síncrona de PostgreSQL, usa al menos tres nodos de datos de Postgres para garantizar la disponibilidad de escritura si un host falla.

Usar la replicación síncrona de PostgreSQL no garantiza cero transacciones perdidas en todas las circunstancias. Cuando el primario y el secundario que actualmente actúa como réplica síncrona fallan simultáneamente, se promoverá un tercer nodo que podría no contener todas las transacciones.

<a id="synchronous_mode"></a>

--------

## Modo síncrono {#synchronous-mode}

Para casos de uso en los que no es permisible perder transacciones confirmadas puedes activar el [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) de Patroni. Cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está activado, Patroni no promoverá un nodo en espera salvo que tenga la certeza de que este contiene todas las transacciones que pudieron haber devuelto al cliente un estado de confirmación exitosa[^2]. Esto significa que el sistema puede no estar disponible para escrituras aunque algunos servidores sí lo estén. Los administradores del sistema pueden seguir usando comandos de conmutación por error manuales para promover un nodo en espera incluso si esto resulta en pérdida de transacciones.

Activar [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) no garantiza la durabilidad multinodo de las confirmaciones en todas las circunstancias. Cuando no hay disponible un nodo en espera adecuado, el servidor primario seguirá aceptando escrituras, pero no garantiza su replicación. Cuando el primario falla en este modo, no se promoverá ningún nodo en espera. Cuando el host que solía ser el primario regresa, será promovido automáticamente, salvo que el administrador del sistema haya realizado una conmutación por error manual. Este comportamiento hace que el modo síncrono sea utilizable con clústeres de 2 nodos.

Cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está activado, el modo estricto está deshabilitado y la única réplica síncrona se cae, las confirmaciones se bloquean hasta que la siguiente iteración de Patroni se ejecute y cambie el primario al modo autónomo (peor caso de retraso para las escrituras `ttl` segundos, caso promedio `loop_wait`/2 segundos). El apagado o reinicio manual de un nodo en espera no provocará una interrupción del servicio de confirmaciones. El nodo en espera avisará al primario para liberarse de sus funciones de réplica síncrona antes de que se inicie el apagado de PostgreSQL.

Cuando es absolutamente necesario garantizar que cada escritura se almacene de forma duradera en al menos dos nodos, habilita `synchronous_mode_strict` además del [synchronous_mode](/es/patroni/replication_modes#synchronous_mode). Este parámetro impide que Patroni desactive la replicación síncrona en el primario cuando no hay candidatos disponibles como réplicas síncronas. Las confirmaciones síncronas se bloquean hasta que haya una réplica síncrona disponible; las transacciones que usan valores de `synchronous_commit` iguales a `off` o `local` evitan esta espera.

En el modo síncrono basado en prioridades (`synchronous_mode: on`), cuando el modo estricto está habilitado y no hay disponible un nodo en espera síncrono adecuado, Patroni 4.1.5 establece `synchronous_standby_names` en `*` y emite la advertencia `"No standbys available!"`. Esto mantiene las confirmaciones a la espera de una réplica síncrona. El comodín no restringe los reconocimientos a los nombres de miembros registrados previamente en `/sync`.

Patroni excluye a un nodo en espera de su selección de réplica síncrona cuando la etiqueta `nosync` está establecida en true. Se recomienda establecerlo para nodos en espera que están detrás de conexiones de red lentas y que provocarían degradación del rendimiento al convertirse en réplica síncrona. Establecer la etiqueta `nostream` en true también tendrá el mismo efecto.

El modo síncrono puede activarse y desactivarse usando el comando `patronictl edit-config` o a través de la interfaz REST de Patroni. Consulta la [configuración dinámica](/es/patroni/config/dynamic#dynamic) para las instrucciones.

Nota: Debido a la forma en que la replicación síncrona está implementada en PostgreSQL, todavía es posible perder transacciones incluso usando `synchronous_mode_strict`. Si el backend de PostgreSQL es cancelado mientras espera reconocer la replicación (por ejemplo, por una solicitud de cancelación tras el timeout de un cliente, o por un fallo del backend), los cambios de la transacción se vuelven visibles para otros backends. Esos cambios aún no están replicados y pueden perderse en caso de promoción de un nodo en espera.

--------

## Factor de replicación síncrona {#synchronous-replication-factor}

El parámetro `synchronous_node_count` lo utiliza Patroni para gestionar el número de bases de datos en espera síncronas. Está establecido en `1` por defecto. No tiene ningún efecto cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está establecido en `off`. Cuando está habilitado, Patroni gestiona el número exacto de bases de datos en espera síncronas con base en el parámetro `synchronous_node_count` y ajusta el estado en el DCS y `synchronous_standby_names` en PostgreSQL a medida que los miembros se unen y se van. Patroni puede usar menos réplicas síncronas que las solicitadas cuando haya menos nodos elegibles disponibles; sin embargo, en el modo de cuórum estricto las confirmaciones siguen esperando el número configurado de reconocimientos de nodos en espera.

--------

## Retraso máximo en el nodo síncrono {#maximum-lag-on-synchronous-node}

De forma predeterminada, Patroni se mantiene en los nodos declarados como `synchronous`, según la vista `pg_stat_replication`, incluso cuando hay otros nodos por delante de él. Esto se hace para minimizar los cambios de `synchronous_standby_names`. Para cambiar este comportamiento se puede usar el parámetro `maximum_lag_on_syncnode`. Controla cuánto retraso puede tener la réplica para seguir considerándose «síncrona».

Patroni utiliza el LSN máximo de las réplicas si hay más de un nodo en espera; de lo contrario usará el LSN actual del WAL del líder. El valor predeterminado es `-1`, y Patroni no tomará medidas para reemplazar un nodo en espera síncrono en mal estado cuando el valor esté establecido en `0` o menos. Establece el valor lo suficientemente alto para que Patroni no intercambie las réplicas síncronas con frecuencia durante volúmenes altos de transacciones.

--------

## Implementación del modo síncrono {#synchronous-mode-implementation}

En el modo síncrono, Patroni mantiene el estado de sincronización en el DCS (clave `/sync`), que contiene el último primario y las bases de datos en espera síncronas actuales. Este estado se actualiza con estrictas restricciones de ordenación para garantizar los siguientes invariantes:

- Un nodo debe marcarse como el último líder siempre que pueda aceptar transacciones de escritura. Una caída de Patroni o que PostgreSQL no se apague pueden provocar violaciones de este invariante.
- Un nodo debe estar establecido como nodo en espera síncrono en PostgreSQL mientras esté publicado como nodo en espera síncrono en la clave `/sync` del DCS.
- Un nodo que no es el líder ni la réplica síncrona actual no tiene permitido promoverse automáticamente.

Para un conjunto no vacío de nodos en espera síncronos, Patroni asigna uno o más nodos en espera síncronos a `synchronous_standby_names`, con base en `synchronous_node_count`.

En cada iteración del bucle de HA, Patroni reevalúa la elección de los nodos en espera síncronos. Si la lista actual de nodos en espera síncronos está conectada y no ha solicitado que se elimine su estado síncrono, se mantiene la selección. De lo contrario, se eligen los miembros del clúster disponibles para la sincronización que estén más avanzados en la replicación.

### Ejemplo: {#example}

#### Clave `/config` en el DCS {#config-key-in-dcs}

```yaml
synchronous_mode: on
synchronous_node_count: 2
...
```

#### Clave `/sync` en el DCS {#sync-key-in-dcs}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2"
}
```

#### postgresql.conf {#postgresqlconf}

```ini
synchronous_standby_names = 'FIRST 2 (node1,node2)'
```

En los ejemplos anteriores, solo se sabe que los nodos `node1` y `node2` son síncronos y que tienen permitido promoverse automáticamente si el primario (`node0`) falla.

<a id="quorum_mode"></a>

--------

## Modo de confirmación por cuórum {#quorum-commit-mode}

A partir de PostgreSQL v10, Patroni admite la replicación síncrona basada en cuórum.

En este modo, Patroni mantiene el estado de sincronización en el DCS, que contiene el último primario conocido, el número de nodos requeridos para el cuórum y los nodos actualmente elegibles para votar en el cuórum. En estado estable, los nodos que votan en el cuórum son el líder y todos los nodos en espera síncronos. Este estado se actualiza con estrictas restricciones de ordenación, con respecto a la promoción de nodos y a `synchronous_standby_names`, para garantizar que en todo momento cualquier subconjunto de votantes que pueda alcanzar el cuórum incluya al menos un nodo con la última confirmación exitosa.

En cada iteración del bucle de HA, Patroni reevalúa las elecciones de nodos en espera síncronos y el cuórum, en función de la disponibilidad de los nodos y de la configuración solicitada del clúster. En versiones de PostgreSQL superiores a la 9.6, todos los nodos elegibles se añaden como nodos en espera síncronos tan pronto como su replicación alcanza al líder.

La confirmación por cuórum ayuda a reducir las latencias del peor de los casos, incluso durante el funcionamiento normal, ya que una latencia mayor al replicar hacia un nodo en espera puede verse compensada por otros nodos en espera.

El modo síncrono basado en cuórum puede habilitarse estableciendo [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) en `quorum` usando el comando `patronictl edit-config` o a través de la interfaz REST de Patroni. Consulta la [configuración dinámica](/es/patroni/config/dynamic#dynamic) para las instrucciones.

Otros parámetros, como `synchronous_node_count`, `maximum_lag_on_syncnode` y `synchronous_mode_strict`, siguen funcionando de la misma manera que con `synchronous_mode=on`.

En el modo de confirmación por cuórum, cuando el conjunto de nodos en espera síncronos está vacío y el modo estricto requiere `N` reconocimientos de nodos en espera, Patroni 4.1.5 establece `synchronous_standby_names` en `ANY N (*)`.

### Ejemplo: {#example-1}

#### Clave `/config` en el DCS {#config-key-in-dcs-1}

```yaml
synchronous_mode: quorum
synchronous_node_count: 2
...
```

#### Clave `/sync` en el DCS {#sync-key-in-dcs-1}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2,node3",
    "quorum": 1
}
```

#### postgresql.conf {#postgresqlconf-1}

```ini
synchronous_standby_names = 'ANY 2 (node1,node2,node3)'
```

Si el primario (`node0`) fallara, en el ejemplo anterior dos de los nodos `node1`, `node2`, `node3` habrán recibido la última transacción, pero no sabemos cuáles. Para averiguar si el nodo `node1` ha recibido la última transacción, necesitamos comparar su LSN con el LSN de **al menos** un nodo (`quorum=1` en la clave `/sync`) entre `node2` y `node3`. Si `node1` no va por detrás de al menos uno de ellos, podemos garantizar que no habrá pérdida de datos visible para el usuario si `node1` es promovido.

[^1]: Los datos siguen ahí, pero recuperarlos requiere un esfuerzo de recuperación manual por parte de especialistas en recuperación de datos. Cuando se permite a Patroni hacer rewind con `use_pg_rewind`, la línea de tiempo bifurcada se borrará automáticamente para reincorporar al clúster el primario fallido. Sin embargo, para que `use_pg_rewind` funcione correctamente, el clúster debe haberse inicializado con `data page checksums` (opción `--data-checksums` de `initdb`) y/o `wal_log_hints` debe estar establecido en `on`.

[^2]: Los clientes pueden cambiar el comportamiento por transacción usando el ajuste `synchronous_commit` de PostgreSQL. Las transacciones con valores de `synchronous_commit` iguales a `off` y `local` pueden perderse en una conmutación por error, pero no serán bloqueadas por retrasos de replicación.
