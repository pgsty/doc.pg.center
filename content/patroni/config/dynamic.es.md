---
title: "Ajustes de configuración dinámica"
linkTitle: "Configuración dinámica"
weight: 10
icon: fa-solid fa-sliders
description: "Ajustes de configuración dinámica almacenados en el DCS y aplicados a todo el clúster."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/dynamic_configuration.html"
---

<a id="dynamic"></a>
La configuración dinámica se almacena en el DCS (Distributed Configuration Store) y se aplica en todos los nodos del clúster.

Para cambiar la configuración dinámica puedes utilizar la herramienta [patronictl_edit_config](/es/patroni/patronictl#patronictl_edit_config) o la [REST API](/es/patroni/rest_api#rest_api) de Patroni.

- **loop_wait**: el número de segundos que el bucle dormirá. Valor predeterminado: 10, valor mínimo posible: 1
- **ttl**: el TTL para adquirir el bloqueo de líder (en segundos). Piénsalo como el tiempo transcurrido antes del inicio del proceso automático de conmutación por error. Valor predeterminado: 30, valor mínimo posible: 20
- **retry_timeout**: tiempo de espera para los reintentos de operaciones del DCS y de PostgreSQL (en segundos). Los problemas del DCS o de la red más cortos que esto no provocarán que Patroni degrade al líder. Valor predeterminado: 10, valor mínimo posible: 3

> [!WARNING]
> al cambiar los valores de **loop_wait**, **retry_timeout** o **ttl** debes seguir la regla:
>
> ```python
> loop_wait + 2 * retry_timeout <= ttl
> ```

- **maximum_lag_on_failover**: el máximo de bytes de retraso que puede tener una réplica para poder participar en la elección de líder.
- **primary_race_backoff**: pospone la carrera por el liderazgo en los nodos en espera `primary_race_backoff` segundos si la replicación de WAL desde el primario sigue avanzando. Permite minimizar las conmutaciones por error innecesarias causadas por un Patroni que deja de responder brevemente. Valor predeterminado: 0 (desactivado).
- **maximum_lag_on_syncnode**: el máximo de bytes de retraso que puede tener una réplica síncrona antes de que se considere un candidato no sano y sea sustituida por una réplica asíncrona sana. Patroni utiliza el lsn máximo de las réplicas si hay más de una réplica; de lo contrario, utilizará el LSN actual del WAL del líder. El valor predeterminado es -1; Patroni no tomará medidas para sustituir a una réplica síncrona no sana cuando el valor esté establecido en 0 o menos. Establece el valor lo suficientemente alto para que Patroni no sustituya a la réplica síncrona con frecuencia durante volúmenes de transacciones altos.
- **max_timelines_history**: número máximo de elementos del historial de líneas de tiempo que se conservan en el DCS. Valor predeterminado: 0. Cuando se establece en 0, se conserva el historial completo en el DCS.
- **primary_start_timeout**: el tiempo durante el cual se permite que un primario se recupere de fallos antes de que se dispare la conmutación por error (en segundos). El valor predeterminado es 300 segundos. Cuando se establece en 0, la conmutación por error se realiza inmediatamente después de detectar una caída, si es posible. Al utilizar replicación asíncrona, una conmutación por error puede causar transacciones perdidas. El peor caso de tiempo de conmutación por error ante un fallo del primario es: loop_wait + primary_start_timeout + loop_wait, excepto si primary_start_timeout es cero, en cuyo caso es solo loop_wait. Establece el valor según tu equilibrio entre durabilidad/disponibilidad.
- **primary_stop_timeout**: el número de segundos que Patroni puede esperar al detener Postgres y efectivo solo cuando synchronous_mode está habilitado. Cuando se establece en \> 0 y synchronous_mode está habilitado, Patroni envía SIGKILL al postmaster si la operación de detención se está ejecutando durante más tiempo que el valor establecido por primary_stop_timeout. Establece el valor según tu equilibrio entre durabilidad/disponibilidad. Si el parámetro no está establecido o está establecido en \<= 0, primary_stop_timeout no se aplica.
- **synchronous_mode**: activa el modo de replicación síncrona. Valores posibles: `off`, `on`, `quorum`. En este modo el líder se encarga de la gestión de `synchronous_standby_names`, y solo el último líder conocido, o una de las réplicas síncronas, puede participar en la carrera por el liderazgo. El modo síncrono garantiza que las transacciones confirmadas con éxito no se pierdan en una conmutación por error, a costa de perder disponibilidad de escritura cuando Patroni no puede garantizar la durabilidad de las transacciones. Consulta la [documentación de los modos de replicación](/es/patroni/replication_modes#replication_modes) para más detalles.
- **synchronous_mode_strict**: evita desactivar la replicación síncrona si no hay réplicas síncronas disponibles, bloqueando todas las escrituras de clientes al primario. En el modo síncrono basado en prioridades (`synchronous_mode: on`), Patroni 4.1.5 establece `synchronous_standby_names` en `*` cuando no hay disponible un nodo en espera síncrono adecuado. Consulta la [documentación de los modos de replicación](/es/patroni/replication_modes#replication_modes) para más detalles.
- **synchronous_node_count**: si [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está habilitado, este parámetro lo utiliza Patroni para gestionar el número preciso de instancias en espera síncronas y ajusta el estado en el DCS y el parámetro `synchronous_standby_names` en PostgreSQL a medida que los miembros se unen y se van. Si el parámetro se establece en un valor superior al número de nodos elegibles, se ajustará automáticamente. El valor predeterminado es `1`.
- **failsafe_mode**: habilita el [modo a prueba de fallos del DCS](/es/patroni/dcs_failsafe_mode#dcs_failsafe_mode). El valor predeterminado es `false`.
- **postgresql**:
  - **use_pg_rewind**: si se utiliza pg_rewind o no. El valor predeterminado es `false`. Ten en cuenta que el clúster debe inicializarse con `data page checksums` (opción `--data-checksums` para `initdb`) y/o `wal_log_hints` debe establecerse en `on`, o de lo contrario `pg_rewind` no funcionará.
  - **use_slots**: si se utilizan slots de replicación o no. El valor predeterminado es `true` en PostgreSQL 9.4+.
  - **recovery_conf**: ajustes de configuración adicionales escritos en recovery.conf al configurar la réplica. Ya no existe recovery.conf en PostgreSQL 12, pero puedes continuar usando esta sección, porque Patroni la gestiona de forma transparente.
  - **parameters**: parámetros de configuración (GUC) para Postgres en formato `{max_connections: 100, wal_level: "replica", max_wal_senders: 10, wal_log_hints: "on"}`. Muchos de ellos son necesarios para que la replicación funcione.
  - **parameters_primary**: (opcional) sobrescrituras de parámetros específicas del rol para el primario. Estos valores se combinan con **parameters** y lo sobrescriben.
  - **parameters_replica**: (opcional) sobrescrituras de parámetros específicas del rol para la réplica. Estos valores se combinan con **parameters** y lo sobrescriben.
  - **parameters_standby_leader**: (opcional) sobrescrituras de parámetros específicas del rol para standby_leader. Estos valores se combinan con **parameters** y lo sobrescriben.
  - **pg_hba**: lista de líneas que Patroni utilizará para generar `pg_hba.conf`. Patroni ignora este parámetro si el parámetro de PostgreSQL `hba_file` está establecido en un valor no predeterminado.
    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: se requiere una línea como esta para la replicación.
  - **pg_hba_primary**: (opcional) entradas pg_hba específicas del rol para el primario. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.
  - **pg_hba_replica**: (opcional) entradas pg_hba específicas del rol para la réplica. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.
  - **pg_hba_standby_leader**: (opcional) entradas pg_hba específicas del rol para standby_leader. Estas reemplazan completamente a **pg_hba** (sin combinación). Si no se definen, se utiliza **pg_hba**.
  - **pg_ident**: lista de líneas que Patroni utilizará para generar `pg_ident.conf`. Patroni ignora este parámetro si el parámetro de PostgreSQL `ident_file` está establecido en un valor no predeterminado.
    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (opcional) entradas pg_ident específicas del rol para el primario. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.
  - **pg_ident_replica**: (opcional) entradas pg_ident específicas del rol para la réplica. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.
  - **pg_ident_standby_leader**: (opcional) entradas pg_ident específicas del rol para standby_leader. Estas reemplazan completamente a **pg_ident** (sin combinación). Si no se definen, se utiliza **pg_ident**.
- **standby_cluster**: si esta sección está definida, queremos arrancar un clúster en espera.
  - **host**: una dirección del nodo remoto
  - **port**: un puerto del nodo remoto
  - **primary_slot_name**: qué slot del nodo remoto utilizar para la replicación. Este parámetro es opcional; el valor predeterminado se deriva del nombre de la instancia (ver la función `slot_name_from_member_name`).
  - **create_replica_methods**: una lista ordenada de métodos que pueden usarse para arrancar el líder en espera desde el primario remoto; puede ser diferente de la lista definida en [postgresql_settings](/es/patroni/config/yaml#postgresql_settings)
  - **restore_command**: comando para restaurar registros WAL desde el primario remoto a los nodos de un clúster en espera; puede ser diferente de la lista definida en [postgresql_settings](/es/patroni/config/yaml#postgresql_settings)
  - **archive_cleanup_command**: comando de limpieza para el líder en espera
  - **recovery_min_apply_delay**: cuánto esperar antes de aplicar realmente los registros WAL en un líder en espera
- **member_slots_ttl**: tiempo de retención de los slots de replicación físicos para las réplicas cuando se apagan. Valor predeterminado: `30min`. Establécelo en `0` si quieres mantener el comportamiento antiguo (cuando la clave del miembro expira del DCS, el slot se elimina inmediatamente). La función solo funciona a partir de PostgreSQL 11.
- **slots**: define slots de replicación permanentes. Estos slots se conservarán durante un switchover/conmutación por error. Los slots permanentes que no existan serán creados por Patroni. Con PostgreSQL 11 en adelante, los slots físicos permanentes se crean en todos los nodos y su posición se avanza cada **loop_wait** segundos. Para versiones de PostgreSQL anteriores a 11, los slots de replicación físicos permanentes se mantienen solo en el primario actual. Los slots lógicos se copian del primario a un nodo en espera con el reinicio y, después de eso, su posición se avanza cada **loop_wait** segundos (si es necesario). La copia de los archivos de slots lógicos se realiza mediante conexión `libpq` y utilizando credenciales de rewind o de superusuario (ver la sección **postgresql.authentication**). Siempre existe la posibilidad de que la posición del slot lógico en la réplica esté un poco por detrás del antiguo primario; por lo tanto, la aplicación debería estar preparada para que algunos mensajes puedan recibirse por segunda vez después de la conmutación por error. La forma más fácil de hacerlo es rastrear `confirmed_flush_lsn`. Habilitar los slots de replicación permanentes requiere que **postgresql.use_slots** esté establecido en `true`. Si hay slots de replicación lógicos permanentes definidos, Patroni habilitará automáticamente `hot_standby_feedback`. Dado que la conmutación por error de los slots de replicación lógicos no es segura en PostgreSQL 9.6 y anteriores, y a la versión 10 de PostgreSQL le faltan algunas funciones importantes, la función solo funciona con PostgreSQL 11+.
  - **my_slot_name**: el nombre del slot de replicación permanente. Si el nombre del slot permanente coincide con el nombre del nodo actual, no se creará en este nodo. Si añades un slot de replicación físico permanente cuyo nombre coincide con el nombre de un miembro de Patroni, Patroni garantizará que el slot creado no se elimine incluso si el miembro correspondiente deja de responder, situación que normalmente resultaría en la eliminación del slot por parte de Patroni. Aunque esto puede ser útil en algunas situaciones, como cuando quieres que los slots de replicación utilizados por los miembros persistan durante fallos temporales o al importar miembros existentes a un nuevo clúster de Patroni (ver [Convertir una instancia independiente en un clúster de Patroni](/es/patroni/existing_data#existing_data) para más detalles), el operador debe tener cuidado de que estos conflictos de nombres no persistan en el DCS cuando el slot ya no sea necesario, debido a su efecto en el funcionamiento normal de Patroni.
    - **type**: tipo de slot. Puede ser `physical` o `logical`. Si el slot es lógico, tienes que definir adicionalmente `database` y `plugin`. Si el slot es físico, puedes definir opcionalmente `cluster_type`.
    - **database**: el nombre de la base de datos donde deben crearse los slots lógicos.
    - **plugin**: el nombre del plugin para el slot lógico.
    - **cluster_type**: el tipo de clúster (`primary` o `standby`) en el que el slot solo debe crearse; de lo contrario, no se creará o un slot ya existente será eliminado.
- **ignore_slots**: lista de conjuntos de propiedades de slots de replicación para los cuales Patroni debería ignorar los slots coincidentes. Esta configuración/función/etc. es útil cuando algunos slots de replicación se gestionan fuera de Patroni. Cualquier subconjunto de propiedades coincidentes hará que se ignore un slot.
  - **name**: el nombre del slot de replicación.
  - **type**: tipo de slot. Puede ser `physical` o `logical`. Si el slot es lógico, puedes definir adicionalmente `database` y/o `plugin`.
  - **database**: el nombre de la base de datos (al coincidir con un slot `logical`).
  - **plugin**: el plugin de decodificación lógica (al coincidir con un slot `logical`).

Nota: **slots** es un hashmap mientras que **ignore_slots** es un array. Por ejemplo:

```yaml
slots:
  permanent_logical_slot_name:
    type: logical
    database: my_db
    plugin: test_decoding
  permanent_physical_slot_name:
    type: physical
  ...
ignore_slots:
  - name: ignored_logical_slot_name
    type: logical
    database: my_db
    plugin: test_decoding
  - name: ignored_physical_slot_name
    type: physical
  ...
```

Nota: Al ejecutar PostgreSQL v11 o más reciente, Patroni mantiene slots de replicación físicos en todos los nodos que potencialmente podrían convertirse en líder, de modo que los nodos réplica mantienen reservados segmentos WAL si otros nodos potencialmente los necesitan. En caso de que el nodo esté ausente y su clave de miembro en el DCS expire, el slot de replicación correspondiente se elimina tras `member_slots_ttl` (el valor predeterminado es `30min`). Puedes aumentar o disminuir la retención según tus necesidades. Alternativamente, si la topología de tu clúster es estática (número fijo de nodos que nunca cambian de nombre) puedes configurar slots de replicación físicos permanentes con nombres correspondientes a los nombres de los nodos para evitar la eliminación de slots y el reciclaje de archivos WAL mientras la réplica está temporalmente caída:

```yaml
slots:
  node_name1:
    type: physical
  node_name2:
    type: physical
  node_name3:
    type: physical
  ...
```

> [!WARNING]
> Los slots de replicación permanentes se sincronizan solo desde el `primary`/`standby_leader` hacia los nodos réplica. Eso significa que se supone que las aplicaciones los utilizan solo desde el nodo líder. Utilizarlos en nodos réplica provocará un crecimiento indefinido de `pg_wal` en todos los demás nodos del clúster. Una excepción a esa regla son los slots físicos que coinciden con los nombres de los miembros de Patroni (creados y mantenidos por Patroni). Estos se sincronizarán entre todos los nodos, ya que se utilizan para la replicación entre ellos.

> [!WARNING]
> Establecer la etiqueta `nostream` en un nodo en espera desactiva la copia y sincronización de los slots de replicación lógicos permanentes en el propio nodo y en todas sus réplicas en cascada, si las hay.
