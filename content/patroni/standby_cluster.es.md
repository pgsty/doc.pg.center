---
title: "Clúster en espera"
weight: 80
icon: fa-solid fa-clone
description: "Configuración, comportamiento y replicación desde un primario remoto del clúster en espera."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/standby_cluster.html"
---

<a id="standby_cluster"></a>
Patroni también admite ejecutar replicación en cascada hacia un centro de datos (región) remoto mediante una función denominada «standby cluster» (clúster en espera). Este tipo de clústeres tiene:

- un «líder en espera», que se comporta prácticamente como un líder de clúster normal, excepto en que replica desde un nodo remoto.
- réplicas en cascada, que replican desde el líder en espera.

El líder en espera mantiene y actualiza un bloqueo de líder en el DCS. Si el bloqueo de líder expira, las réplicas en cascada realizarán una elección para elegir otro líder entre los nodos en espera.

No hay ninguna otra relación entre el clúster en espera y el clúster primario del que replica; en particular, no deben compartir el mismo ámbito (scope) del DCS si usan el mismo DCS. No saben nada el uno del otro aparte de la información de replicación. Además, el clúster en espera no se muestra en la salida de [patronictl_list](/es/patroni/patronictl#patronictl_list) o [patronictl_topology](/es/patroni/patronictl#patronictl_topology) en el clúster primario.

Por flexibilidad, puedes especificar los métodos de creación de una réplica y de recuperación de registros WAL cuando un clúster está en el «modo en espera» proporcionando la clave [create_replica_methods](/es/patroni/replica_bootstrap#custom_replica_creation) en la sección [standby_cluster](/es/patroni/standby_cluster#standby_cluster). Esto es distinto de la creación de réplicas cuando el clúster está desvinculado y funciona como un clúster normal, lo cual se controla mediante `create_replica_methods` en la sección `postgresql`. Tanto los `create_replica_methods` de «espera» como los «normales» hacen referencia a claves de la sección `postgresql`.

Para configurar un clúster de este tipo necesitas especificar la sección [standby_cluster](/es/patroni/standby_cluster#standby_cluster) en una configuración de patroni:

```yaml
bootstrap:
    dcs:
        standby_cluster:
            host: 1.2.3.4
            port: 5432
            primary_slot_name: patroni
            create_replica_methods:
            - basebackup
```

Ten en cuenta que estas opciones se aplicarán solo una vez durante el bootstrap del clúster y que la única forma de cambiarlas después es a través del DCS.

Patroni espera encontrar `postgresql.conf` o `postgresql.conf.backup` en el PGDATA del primario remoto y no arrancará si no lo encuentra después de un basebackup. Si el primario remoto mantiene su `postgresql.conf` en otro lugar, es tu responsabilidad copiarlo al PGDATA.

Si usas slots de replicación en el clúster en espera, también debes crear el slot de replicación correspondiente en el clúster primario. La implementación del clúster en espera no lo hará automáticamente. Puedes usar la funcionalidad de slots de replicación permanentes de Patroni en el clúster primario para mantener un slot de replicación con el mismo nombre que `primary_slot_name`, o su valor predeterminado si no se proporciona `primary_slot_name`.

En caso de que el sitio remoto no proporcione un único endpoint que conecte con un primario, se pueden listar todos los hosts del clúster de origen en la sección `standby_cluster.host`. Cuando `standby_cluster.host` contiene varios hosts separados por comas, Patroni hará:

- añadir `target_session_attrs=read-write` al `primary_conninfo` en el nodo líder en espera.
- usar `target_session_attrs=read-write` al intentar determinar si es necesario ejecutar `pg_rewind` o al ejecutar `pg_rewind` en todos los nodos del clúster en espera.
- Es importante tener en cuenta que, para que `pg_rewind` funcione correctamente, el clúster debe haberse inicializado con `data page checksums` (opción `--data-checksums` de `initdb`) y/o `wal_log_hints` debe estar establecido en `on`. De lo contrario, `pg_rewind` no funcionará correctamente.

También existe la posibilidad de replicar el clúster en espera desde otro clúster en espera o desde un miembro en espera del clúster primario: para ello necesitas definir un único host en la sección `standby_cluster.host`. Sin embargo, debes saber que en este caso `pg_rewind` no podrá ejecutarse en el clúster en espera.

> [!WARNING]
> Los nombres de los miembros (el campo `name` en la configuración de Patroni de cada nodo) deben ser únicos en todo el clúster primario y en todos los clústeres en espera conectados a él.
>
> Patroni establece `synchronous_standby_names` en el primario usando nombres de miembros, que también se convierten en el `application_name` de cada conexión de replicación en `pg_stat_replication`. Si un nodo de un clúster en espera comparte el mismo nombre que un miembro del clúster primario, PostgreSQL verá dos conexiones con valores idénticos de `application_name`. Esta ambigüedad puede hacer que PostgreSQL satisfaga el requisito de replicación síncrona usando la conexión del clúster en espera en lugar del miembro previsto del clúster primario, llevando a PostgreSQL a reconocer transacciones prematuramente como confirmadas sincrónicamente cuando no son duraderas en el nodo en espera correcto.
>
> Este es un fallo silencioso: la replicación continúa y no se registra ningún error, pero el clúster opera efectivamente sin una réplica síncrona válida, lo que supone un escenario potencial de pérdida de datos si el primario falla.
