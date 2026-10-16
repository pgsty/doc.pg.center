---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "Referencia de comandos para la configuración, sintaxis y subcomandos de patronictl."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
Patroni dispone de una interfaz de línea de comandos llamada [patronictl](/es/patroni/patronictl#patronictl), que se usa básicamente para interactuar con la REST API de Patroni y con el DCS. Está pensada para facilitar la realización de operaciones en el clúster y puede usarse fácilmente tanto por humanos como por scripts.

<a id="patronictl_configuration"></a>

--------

## Configuración {#configuration}

[patronictl](/es/patroni/patronictl#patronictl) usa 3 secciones de la configuración:

- **ctl**: cómo autenticarse contra la REST API de Patroni y cómo validar la identidad del servidor. Consulta los [ajustes de ctl](/es/patroni/config/yaml#patronictl_settings) para más detalles;
- **restapi**: cómo autenticarse contra la REST API de Patroni y cómo validar la identidad del servidor. Solo se usa si la configuración de `ctl` no es suficiente. A [patronictl](/es/patroni/patronictl#patronictl) le interesa principalmente la sección `restapi.authentication` (en caso de que falte `ctl.authentication`) y el ajuste `restapi.cafile` (en caso de que falte `ctl.cacert`). Consulta los [ajustes de la REST API](/es/patroni/config/yaml#restapi_settings) para más detalles;
- DCS (p. ej. **etcd**): cómo contactar y autenticarse contra el DCS usado por Patroni.

Esas opciones de configuración pueden provenir de variables de entorno o de un archivo de configuración. Busca las secciones anteriores en [Ajustes de configuración mediante variables de entorno](/es/patroni/config/env#env) o en [Ajustes de configuración YAML](/es/patroni/config/yaml#yaml) para entender cómo puedes establecer sus opciones mediante variables de entorno o mediante un archivo de configuración.

Si optas por usar variables de entorno, es un enfoque directo. Patronictl leerá las variables de entorno y usará sus valores.

Si optas por usar un archivo de configuración, tienes distintas maneras de indicar a [patronictl](/es/patroni/patronictl#patronictl) el archivo que se va a usar. De forma predeterminada, [patronictl](/es/patroni/patronictl#patronictl) intentará cargar un archivo de configuración llamado `patronictl.yaml`, que se espera encontrar en cualquiera de estas rutas, según tu sistema:

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (itinerante): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (no itinerante): `C:\Users\<user>\AppData\Local\patroni`

Puedes sobrescribir ese comportamiento de las siguientes formas:

- Estableciendo la variable de entorno `PATRONICTL_CONFIG_FILE` con la ruta a un archivo de configuración personalizado;
- Usando el argumento de línea de comandos `-c` / `--config-file` de [patronictl](/es/patroni/patronictl#patronictl) con la ruta a un archivo de configuración personalizado.

> [!NOTE]
> Si estás ejecutando [patronictl](/es/patroni/patronictl#patronictl) en el mismo host donde se ejecuta el demonio `patroni`, simplemente puedes usar el mismo archivo de configuración si contiene todas las secciones de configuración requeridas por [patronictl](/es/patroni/patronictl#patronictl).

<a id="patronictl_usage"></a>

--------

## Uso {#usage}

[patronictl](/es/patroni/patronictl#patronictl) expone varias operaciones útiles. Esta sección tiene como objetivo describir cada una de ellas.

Antes de entrar en cada uno de los subcomandos de [patronictl](/es/patroni/patronictl#patronictl), ten en cuenta que el propio [patronictl](/es/patroni/patronictl#patronictl) tiene los siguientes argumentos de línea de comandos:

`-c` / `--config-file`  
Como se explicó antes, se usa para proporcionar una ruta a un archivo de configuración para [patronictl](/es/patroni/patronictl#patronictl).

`-d` / `--dcs-url` / `--dcs`  
Proporciona una cadena de conexión al DCS usado por Patroni.

Este argumento puede usarse tanto para sobrescribir los ajustes de DCS y `namespace` de la configuración de [patronictl](/es/patroni/patronictl#patronictl), como para definirlos si faltan en la configuración.

El valor debe estar en el formato `DCS://HOST:PORT/NAMESPACE`, p. ej. `etcd3://localhost:2379/service` para conectarse a un etcd v3 que se ejecuta en `localhost` con el clúster de Patroni almacenado bajo el namespace `service`. Cualquier parte que falte en el valor del argumento se sustituirá por el valor presente en la configuración o por su valor predeterminado.

`-k` / `--insecure`  
Opción para omitir la validación del certificado SSL del servidor de la REST API.

Esta es la sinopsis para ejecutar un comando de [patronictl](/es/patroni/patronictl#patronictl):

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> Esta es la sintaxis de la sinopsis:
>
> - Las opciones entre corchetes son opcionales;
> - Las opciones entre llaves representan una operación de «elige una del conjunto»;
> - Las opciones con `[, ... ]` pueden especificarse varias veces;
> - Lo que está escrito en mayúsculas representa un literal al que se debe dar un valor.
>
> Usaremos esta misma sintaxis al describir los subcomandos de [patronictl](/es/patroni/patronictl#patronictl) en las siguientes subsecciones. Además, al describir los subcomandos en las siguientes subsecciones, la sinopsis de los comandos debe interpretarse como un reemplazo del `SUBCOMMAND` de la sinopsis anterior.

En las siguientes subsecciones encontrarás una descripción de cada comando implementado por [patronictl](/es/patroni/patronictl#patronictl). A modo de ejemplo, usaremos los archivos de configuración presentes en el repositorio de GitHub de Patroni (archivos `postgres0.yml`, `postgres1.yml` y `postgres2.yml`).

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### Sinopsis {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### Descripción {#description}

`patronictl demote-cluster` convierte un clúster regular de Patroni en un [clúster en espera](/es/patroni/standby_cluster#standby_cluster).

El comando modifica la configuración dinámica con una sección `standby_cluster` construida a partir de las opciones de conexión al primario remoto proporcionadas y, a continuación, espera hasta que el líder se esté ejecutando como líder en espera. Imprime la topología actual del clúster antes de cambiar la configuración y pide confirmación a menos que se use `--force`.

Debe especificarse al menos una de `--host`, `--port` o `--restore-command`.

<a id="patronictl_demote_cluster_parameters"></a>

#### Parámetros {#parameters}

`CLUSTER_NAME`: nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--host`: dirección del nodo remoto.

`--port`: puerto del nodo remoto.

`--restore-command`: comando para restaurar registros de WAL desde el primario remoto.

`--primary-slot-name`: nombre del slot de replicación del nodo remoto que se usará para la replicación.

`--force`: opción para omitir los avisos de confirmación al degradar el clúster.

Útil para scripts.

<a id="patronictl_demote_cluster_examples"></a>

#### Ejemplos {#examples}

Degradar el clúster a un clúster en espera que sigue el endpoint de un primario remoto:

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### Sinopsis {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### Descripción {#description-1}

`patronictl dsn` obtiene la cadena de conexión de un miembro del clúster de Patroni.

Si varios miembros coinciden con los parámetros de este comando, se elegirá uno de ellos, dando prioridad al nodo primario.

<a id="patronictl_dsn_parameters"></a>

#### Parámetros {#parameters-1}

`CLUSTER_NAME`: nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`-r` / `--role`  
Elige un miembro que tenga el rol dado.

El rol puede ser uno de:

- `leader`: el líder de un clúster regular de Patroni o de un clúster en espera de Patroni; o
- `primary`: el líder de un clúster regular de Patroni; o
- `standby-leader`: el líder de un clúster en espera de Patroni; o
- `replica`: una réplica de un clúster de Patroni; o
- `standby`: igual que `replica`; o
- `any`: cualquier rol. Igual que omitir este parámetro; o

`-m` / `--member`  
Elige un miembro del clúster con el nombre dado.

`MEMBER_NAME` es el nombre del miembro.

`--group`  
Elige un miembro que forme parte del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

<a id="patronictl_dsn_examples"></a>

#### Ejemplos {#examples-1}

Obtener el DSN del nodo primario:

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

Obtener el DSN del nodo llamado `postgresql1`:

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### Sinopsis {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### Descripción {#description-2}

`patronictl edit-config` cambia la configuración dinámica del clúster y actualiza el DCS con ella.

> [!NOTE]
> Cuando se invoca a través de una TTY, el comando intenta mostrar un diff de la configuración dinámica mediante un paginador. De forma predeterminada, intenta usar `less` o `more`. Si quieres un paginador distinto, establece la variable de entorno `PAGER` con el deseado.

<a id="patronictl_edit_config_parameters"></a>

#### Parámetros {#parameters-2}

`CLUSTER_NAME`: nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Cambia la configuración dinámica del grupo de Citus dado.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `citus.group`, si existe.

`CITUS_GROUP` es el ID del grupo de Citus.

`-q` / `--quiet`  
Opción para omitir la muestra del diff de la configuración.

`-s` / `--set`  
Establece una opción dada de la configuración dinámica con un valor dado.

`CONFIG` es el nombre de la ruta de configuración dinámica en el árbol YAML, con los niveles unidos por `.` .

`VALUE` es el valor de `CONFIG`. Si es `null`, entonces `CONFIG` se eliminará de la configuración dinámica.

`-p` / `--pg`  
Establece una opción dada de la configuración dinámica de Postgres con el valor dado.

Es esencialmente una abreviatura de `-s` / `--set` con `CONFIG` precedido de `postgresql.parameters.`.

`PG_CONFIG` es el nombre de la configuración de Postgres que se va a establecer.

`PG_VALUE` es el valor de `PG_CONFIG`. Si es `null`, entonces `PG_CONFIG` se eliminará de la configuración dinámica.

`--apply`  
Aplica la configuración dinámica del archivo dado.

Es similar a especificar múltiples opciones `-s` / `--set`, una por cada configuración de `CONFIG_FILE`.

`CONFIG_FILE` es la ruta a un archivo que contiene la configuración dinámica que se va a aplicar, en formato YAML. Usa `-` si quieres leer desde `stdin`.

`--replace`  
Sustituye la configuración dinámica del DCS por la configuración dinámica especificada en el archivo dado.

`CONFIG_FILE` es la ruta a un archivo que contiene la nueva configuración dinámica que entrará en vigor, en formato YAML. Usa `-` si quieres leer desde `stdin`.

`--force`  
Opción para omitir los avisos de confirmación al cambiar la configuración dinámica.

Útil para scripts.

<a id="patronictl_edit_config_examples"></a>

#### Ejemplos {#examples-2}

Cambiar el GUC de Postgres `max_connections`:

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

Cambiar los ajustes `loop_wait` y `ttl`:

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

Eliminar el ajuste `maximum_lag_on_failover` de la configuración dinámica:

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### Sinopsis {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### Descripción {#description-3}

`patronictl failover` realiza una conmutación por error manual en el clúster.

Está pensado para usarse cuando el clúster no está en buen estado, por ejemplo:

- No hay líder; o
- No hay ningún standby síncrono disponible en un clúster síncrono.

También permite conmutar a un nodo asíncrono si el modo síncrono está habilitado.

> [!NOTE]
> Nada te impide ejecutar `patronictl failover` en un clúster en buen estado. Sin embargo, en esos casos recomendamos usar `patronictl switchover`.

> [!WARNING]
> Disparar una conmutación por error puede provocar pérdida de datos dependiendo de lo actualizada que esté la réplica promovida en comparación con el primario.

<a id="patronictl_failover_parameters"></a>

#### Parámetros {#parameters-3}

`CLUSTER_NAME`: nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Realiza una conmutación por error en el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`--candidate`  
El nodo que se promoverá en la conmutación por error.

`CANDIDATE_NAME` es el nombre del nodo que se va a promover.

`--force`  
Opción para omitir los avisos de confirmación al realizar la conmutación por error.

Útil para scripts.

<a id="patronictl_failover_examples"></a>

#### Ejemplos {#examples-3}

Conmutar por error al nodo `postgresql2`:

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### Sinopsis {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### Descripción {#description-4}

`patronictl flush` descarta los eventos programados, si los hay.

<a id="patronictl_flush_parameters"></a>

#### Parámetros {#parameters-4}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`MEMBER_NAME`  
Descarta los eventos programados de los miembros de Patroni dados.

Pueden especificarse varios miembros. Si no se especifica ningún miembro, se consideran todos.

> [!NOTE]
> Solo se usa si se descartan eventos de reinicio programados.

`restart`  
Descarta eventos de reinicio programados.

`switchover`  
Descarta el evento de switchover programado.

`--group`  
Descarta los eventos programados del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-r` / `--role`  
Descarta los eventos programados de los miembros que tienen el rol dado.

El rol puede ser uno de:

- `leader`: el líder de un clúster regular de Patroni o de un clúster en espera de Patroni; o
- `primary`: el líder de un clúster regular de Patroni; o
- `standby-leader`: el líder de un clúster en espera de Patroni; o
- `replica`: una réplica de un clúster de Patroni; o
- `standby`: igual que `replica`; o
- `any`: cualquier rol. Igual que omitir este parámetro.

> [!NOTE]
> Solo se usa si se descartan eventos de reinicio programados.

`--force`  
Opción para omitir los avisos de confirmación al realizar el flush.

Útil para scripts.

<a id="patronictl_flush_examples"></a>

#### Ejemplos {#examples-4}

Descartar un evento de switchover programado:

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

Descartar el reinicio programado de todos los nodos standby:

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

Descartar el reinicio programado de los nodos `postgresql0` y `postgresql1`:

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### Sinopsis {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### Descripción {#description-5}

`patronictl history` muestra un historial de eventos de conmutación por error y de switchover del clúster, si los hay.

La siguiente información se incluye en la salida:

`TL`  
Línea de tiempo de Postgres en la que ocurrió el evento.

`LSN`  
LSN de Postgres en el que ocurrió el evento.

`Reason`  
Motivo obtenido del archivo `.history` de Postgres.

`Timestamp`  
Momento en que ocurrió el evento.

`New Leader`  
Miembro de Patroni que fue promovido durante el evento.

<a id="patronictl_history_parameters"></a>

#### Parámetros {#parameters-5}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Muestra el historial de eventos del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `citus.group`, si existe.

`-f` / `--format`  
Cómo formatear la lista de eventos en la salida.

El formato puede ser uno de:

- `pretty`: imprime el historial como una tabla bien formateada; o
- `tsv`: imprime el historial como información tabular, con columnas delimitadas por `\t`; o
- `json`: imprime el historial en formato JSON; o
- `yaml`: imprime el historial en formato YAML.

El valor predeterminado es `pretty`.

<a id="patronictl_history_examples"></a>

#### Ejemplos {#examples-5}

Mostrar el historial de eventos:

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

Mostrar el historial de eventos en formato YAML:

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### Sinopsis {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### Descripción {#description-6}

`patronictl list` muestra información sobre el clúster de Patroni y sus miembros.

La siguiente información se incluye en la salida:

`Cluster`  
Nombre del clúster de Patroni.

`Member`  
Nombre del miembro de Patroni.

`Host`  
Host donde se encuentra el miembro.

`Role`  
Rol actual del miembro.

Puede ser uno entre:

- `Leader`: el líder actual de un clúster regular de Patroni; o
- `Standby Leader`: el líder actual de un clúster en espera de Patroni; o
- `Sync Standby`: un standby síncrono de un clúster de Patroni con el modo síncrono habilitado; o
- `Replica`: un standby regular de un clúster de Patroni.

`State`  
Estado actual de Postgres en el miembro de Patroni.

Algunos ejemplos entre los estados posibles:

- `running`: si Postgres está actualmente levantado y en ejecución;
- `streaming`: si es una réplica y Postgres está actualmente transmitiendo WAL desde el nodo primario;
- `in archive recovery`: si es una réplica y Postgres está obteniendo actualmente WAL del archivado;
- `stopped`: si Postgres había sido apagado;
- `crashed`: si Postgres se ha caído.

`TL`  
Línea de tiempo actual de Postgres en el miembro de Patroni.

`Receive LSN`  
La última posición del write-ahead log recibida y sincronizada con el disco por la replicación en flujo del miembro (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Retraso de replicación entre la posición `Receive LSN` del miembro y su upstream, en MB.

`Replay LSN`  
La última posición del write-ahead log reproducida durante la recuperación del miembro (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Retraso de replicación entre la posición `Replay LSN` del miembro y su upstream, en MB.

Además de eso, la siguiente información puede incluirse en la salida:

`System identifier`  
Identificador de sistema de Postgres.

> [!NOTE]
> Se muestra en la cabecera de la tabla.
>
> Solo se muestra si el formato de salida es `pretty`.

`Group`  
ID del grupo de Citus.

> [!NOTE]
> Se muestra en la cabecera de la tabla.
>
> Solo se muestra si es un clúster de Citus.

`Pending restart`  
`*` indica que el nodo necesita un reinicio para que alguna configuración de Postgres surta efecto. Un valor vacío indica que el nodo no requiere un reinicio.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si:
>
> - Se imprime en formato `pretty` o `tsv` y con la salida extendida habilitada; o
> - El nodo requiere un reinicio.

`Scheduled restart`  
Marca de tiempo en la que se ha programado un reinicio para la instancia de Postgres gestionada por el miembro de Patroni. Un valor vacío indica que no hay ningún reinicio programado para el miembro.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si:
>
> - Se imprime en formato `pretty` o `tsv` y con la salida extendida habilitada; o
> - El nodo tiene un reinicio programado.

`Tags`  
Contiene las etiquetas establecidas para el miembro de Patroni. Un valor vacío indica que no se ha configurado ninguna etiqueta o que se han configurado con valores predeterminados.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si:
>
> - Se imprime en formato `pretty` o `tsv` y con la salida extendida habilitada; o
> - El nodo tiene alguna etiqueta personalizada, o alguna etiqueta predeterminada con valores no predeterminados.

`Scheduled switchover`  
Marca de tiempo en la que se ha programado un switchover para el clúster de Patroni, si lo hay.

> [!NOTE]
> Se muestra en el pie de la tabla.
>
> Solo se muestra si hay un switchover programado y el formato de salida es `pretty`.

`Maintenance mode`

> Si la monitorización del clúster está actualmente en pausa.
>
> > [!NOTE]
> > Se muestra en el pie de la tabla.
> >
> > Solo se muestra si el clúster está en pausa y el formato de salida es `pretty`.

<a id="patronictl_list_parameters"></a>

#### Parámetros {#parameters-6}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Muestra información sobre los miembros del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-e` / `--extended`  
Muestra información extendida.

Fuerza la muestra de los atributos `Pending restart`, `Scheduled restart` y `Tags`, incluso si su valor está vacío.

> [!NOTE]
> Solo se aplica a los formatos de salida `pretty` y `tsv`.

`-t` / `--timestamp`  
Imprime una marca de tiempo antes de imprimir la información sobre el clúster y sus miembros.

`-f` / `--format`  
Cómo formatear la lista de miembros del clúster en la salida.

El formato puede ser uno de:

- `pretty`: imprime los miembros del clúster como una tabla bien formateada; o
- `tsv`: imprime los miembros del clúster como información tabular, con columnas delimitadas por `\t`; o
- `json`: imprime los miembros del clúster en formato JSON; o
- `yaml`: imprime los miembros del clúster en formato YAML.

El valor predeterminado es `pretty`.

`-W`  
Refresca automáticamente la información cada 2 segundos.

`-w` / `--watch`  
Refresca automáticamente la información en el intervalo especificado.

`TIME` es el intervalo entre refrescos, en segundos.

<a id="patronictl_list_examples"></a>

#### Ejemplos {#examples-6}

Mostrar información sobre el clúster en formato pretty:

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

Mostrar información sobre el clúster en formato pretty con columnas extendidas:

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

Mostrar información sobre el clúster en formato YAML, con la marca de tiempo de ejecución:

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### Sinopsis {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### Descripción {#description-7}

`patronictl pause` pone temporalmente el clúster de Patroni en modo de mantenimiento y deshabilita la conmutación por error automática.

<a id="patronictl_pause_parameters"></a>

#### Parámetros {#parameters-7}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Pone en pausa el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `citus.group`, si existe.

`--wait`  
Espera hasta que todos los miembros de Patroni estén en pausa antes de devolver el control al invocador.

<a id="patronictl_pause_examples"></a>

#### Ejemplos {#examples-7}

Poner el clúster en modo de mantenimiento y esperar hasta que todos los nodos estén en pausa:

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### Sinopsis {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### Descripción {#description-8}

`patronictl promote-cluster` convierte un clúster en espera en un clúster regular de Patroni.

El comando elimina la sección `standby_cluster` de la configuración dinámica y espera hasta que el líder se esté ejecutando como primario. Imprime la topología actual del clúster antes de cambiar la configuración y pide confirmación a menos que se use `--force`.

<a id="patronictl_promote_cluster_parameters"></a>

#### Parámetros {#parameters-8}

`CLUSTER_NAME`: nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--force`: opción para omitir los avisos de confirmación al promover el clúster.

Útil para scripts.

<a id="patronictl_promote_cluster_examples"></a>

#### Ejemplos {#examples-8}

Promover el clúster en espera para que se ejecute como un clúster regular de Patroni:

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### Sinopsis {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### Descripción {#description-9}

`patronictl query` ejecuta un comando o un script SQL contra un miembro del clúster de Patroni.

<a id="patronictl_query_parameters"></a>

#### Parámetros {#parameters-9}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Consulta el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-r` / `--role`  
Elige un miembro que tenga el rol dado.

El rol puede ser uno de:

- `leader`: el líder de un clúster regular de Patroni o de un clúster en espera de Patroni; o
- `primary`: el líder de un clúster regular de Patroni; o
- `standby-leader`: el líder de un clúster en espera de Patroni; o
- `replica`: una réplica de un clúster de Patroni; o
- `standby`: igual que `replica`; o
- `any`: cualquier rol. Igual que omitir este parámetro.

`-m` / `--member`  
Elige un miembro que tenga el nombre dado.

`MEMBER_NAME` es el nombre del miembro que se va a elegir.

`-d` / `--dbname`  
Base de datos a la que conectarse para ejecutar la consulta.

`DBNAME` es el nombre de la base de datos. Si no se proporciona, el valor predeterminado es `USERNAME`.

`-U` / `--username`  
Usuario para conectarse a la base de datos.

`USERNAME` es el nombre del usuario. Si no se proporciona, el valor predeterminado es el usuario del sistema operativo que ejecuta `patronictl query`.

`--password`  
Pide la contraseña del usuario que se conecta.

Como Patroni usa `libpq`, como alternativa puedes crear un archivo `~/.pgpass` o establecer la variable de entorno `PGPASSWORD`.

`--format`  
Cómo formatear la salida de la consulta.

El formato puede ser uno de:

- `pretty`: imprime la salida de la consulta como una tabla bien formateada; o
- `tsv`: imprime la salida de la consulta como información tabular, con columnas delimitadas por `\t`; o
- `json`: imprime la salida de la consulta en formato JSON; o
- `yaml`: imprime la salida de la consulta en formato YAML.

El valor predeterminado es `tsv`.

`-f` / `--file`  
Usa un archivo como origen de los comandos para ejecutar consultas.

`FILE_NAME` es la ruta al archivo de origen.

`-c` / `--command`  
Ejecuta el comando SQL dado en la consulta.

`SQL_COMMAND` es el comando SQL que se va a ejecutar.

`--delimiter`  
El delimitador al imprimir información en formato `tsv`, o `\t` si se omite.

`-W`  
Vuelve a ejecutar automáticamente la consulta cada 2 segundos.

`-w` / `--watch`  
Vuelve a ejecutar automáticamente la consulta en el intervalo especificado.

`TIME` es el intervalo entre reejecuciones, en segundos.

<a id="patronictl_query_examples"></a>

#### Ejemplos {#examples-9}

Ejecutar un comando SQL como usuario `postgres` y pedir su contraseña:

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

Ejecutar un comando SQL como usuario `postgres` y tomar la contraseña de la variable de entorno de `libpq`:

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

Ejecutar un comando SQL e imprimir en formato `pretty` cada 2 segundos:

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

Ejecutar un comando SQL en la base de datos `test` e imprimir la salida en formato YAML:

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

Ejecutar un comando SQL en el miembro `postgresql2`:

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

Ejecutar un comando SQL en cualquiera de los standbys:

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### Sinopsis {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### Descripción {#description-10}

`patronictl reinit` reconstruye una instancia standby de Postgres gestionada por un miembro réplica del clúster de Patroni.

<a id="patronictl_reinit_parameters"></a>

#### Parámetros {#parameters-10}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`MEMBER_NAME`  
Nombre del miembro réplica para el que se reconstruirá la instancia de Postgres.

Pueden especificarse varios miembros réplica. Si no se especifica ningún miembro, el comando no hace nada.

`--group`  
Reconstruye un miembro réplica del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`--wait`  
Espera hasta que termine la reinicialización de los nodos standby de Postgres.

`--force`  
Opción para omitir los avisos de confirmación al reconstruir instancias standby de Postgres.

Útil para scripts.

`--from-leader`  
Opción para obtener el basebackup directamente del líder.

<a id="patronictl_reinit_examples"></a>

#### Ejemplos {#examples-10}

Solicitar la reconstrucción de todos los miembros réplica del clúster de Patroni y devolver inmediatamente el control al invocador:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

Solicitar la reconstrucción de `postgresql2` y esperar a que se complete:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

Solicitar la reconstrucción de `postgresql2` y obtener el basebackup directamente del líder:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### Sinopsis {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### Descripción {#description-11}

`patronictl reload` solicita una recarga de la configuración local de uno o más miembros de Patroni.

También dispara `pg_ctl reload` en la instancia de Postgres gestionada, incluso si nada ha cambiado.

<a id="patronictl_reload_parameters"></a>

#### Parámetros {#parameters-11}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`MEMBER_NAME`  
Solicita una recarga de la configuración local de los miembros de Patroni dados.

Pueden especificarse varios miembros. Si no se especifica ningún miembro, se consideran todos.

`--group`  
Solicita una recarga de los miembros del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-r` / `--role`  
Selecciona los miembros que tienen el rol dado.

El rol puede ser uno de:

- `leader`: el líder de un clúster regular de Patroni o de un clúster en espera de Patroni; o
- `primary`: el líder de un clúster regular de Patroni; o
- `standby-leader`: el líder de un clúster en espera de Patroni; o
- `replica`: una réplica de un clúster de Patroni; o
- `standby`: igual que `replica`; o
- `any`: cualquier rol. Igual que omitir este parámetro.

`--force`  
Opción para omitir los avisos de confirmación al solicitar una recarga de la configuración local.

Útil para scripts.

<a id="patronictl_reload_examples"></a>

#### Ejemplos {#examples-11}

Solicitar una recarga de la configuración local de todos los miembros del clúster de Patroni:

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### Sinopsis {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### Descripción {#description-12}

`patronictl remove` elimina del DCS la información del clúster.

Es una acción interactiva.

> [!WARNING]
> Esta operación destruirá la información del clúster de Patroni del DCS.

<a id="patronictl_remove_parameters"></a>

#### Parámetros {#parameters-12}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`--group`  
Elimina la información sobre el clúster de Patroni relacionada con el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-f` / `--format`  
Cómo formatear la lista de miembros en la salida al pedir la confirmación.

El formato puede ser uno de:

- `pretty`: imprime los miembros como una tabla bien formateada; o
- `tsv`: imprime los miembros como información tabular, con columnas delimitadas por `\t`; o
- `json`: imprime los miembros en formato JSON; o
- `yaml`: imprime los miembros en formato YAML.

El valor predeterminado es `pretty`.

<a id="patronictl_remove_examples"></a>

#### Ejemplos {#examples-12}

Eliminar del DCS la información sobre el clúster de Patroni `batman`:

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### Sinopsis {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### Descripción {#description-13}

`patronictl restart` solicita un reinicio de la instancia de Postgres gestionada por un miembro del clúster de Patroni.

El reinicio puede realizarse inmediatamente o programarse para más tarde.

<a id="patronictl_restart_parameters"></a>

#### Parámetros {#parameters-13}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`--group`  
Reinicia el clúster de Patroni relacionado con el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-r` / `--role`  
Elige los miembros que tienen el rol dado.

El rol puede ser uno de:

- `leader`: el líder de un clúster regular de Patroni o de un clúster en espera de Patroni; o
- `primary`: el líder de un clúster regular de Patroni; o
- `standby-leader`: el líder de un clúster en espera de Patroni; o
- `replica`: una réplica de un clúster de Patroni; o
- `standby`: igual que `replica`; o
- `any`: cualquier rol. Igual que omitir este parámetro.

`--any`  
Reinicia un único nodo aleatorio entre los que coinciden con los filtros dados.

`--pg-version`  
Selecciona solo los miembros cuya versión de la instancia de Postgres gestionada es anterior a la versión dada.

`PG_VERSION` es la versión de Postgres que se va a comparar.

`--pending`  
Selecciona solo los miembros marcados como `Pending restart`.

`--timeout`: aborta el reinicio si tarda más del tiempo de espera especificado y conmuta por error a una réplica si el problema está en el primario.

`TIMEOUT` es la cantidad de segundos que se esperarán antes de abortar el reinicio.

`--scheduled`  
Programa un reinicio para que ocurra en la marca de tiempo dada.

`TIMESTAMP` es la marca de tiempo en la que debería ocurrir el reinicio. Especifícala en un formato sin ambigüedad, preferiblemente con zona horaria. También puedes usar el literal `now` para que el reinicio se ejecute inmediatamente.

`--force`  
Opción para omitir los avisos de confirmación al solicitar las operaciones de reinicio.

Útil para scripts.

<a id="patronictl_restart_examples"></a>

#### Ejemplos {#examples-13}

Reiniciar inmediatamente todos los miembros del clúster:

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

Reiniciar inmediatamente un miembro aleatorio del clúster:

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

Programar un reinicio para que ocurra en `2023-09-13T18:00-03:00`:

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### Sinopsis {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### Descripción {#description-14}

`patronictl resume` saca el clúster de Patroni del modo de mantenimiento y vuelve a habilitar la conmutación por error automática.

<a id="patronictl_resume_parameters"></a>

#### Parámetros {#parameters-14}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Reanuda el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `citus.group`, si existe.

`--wait`  
Espera hasta que todos los miembros de Patroni estén fuera de pausa antes de devolver el control al invocador.

<a id="patronictl_resume_examples"></a>

#### Ejemplos {#examples-14}

Sacar el clúster del modo de mantenimiento:

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### Sinopsis {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### Descripción {#description-15}

`patronictl show-config` muestra la configuración dinámica del clúster que está almacenada en el DCS.

<a id="patronictl_show_config_parameters"></a>

#### Parámetros {#parameters-15}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Muestra la configuración dinámica del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `citus.group`, si existe.

<a id="patronictl_show_config_examples"></a>

#### Ejemplos {#examples-15}

Mostrar la configuración dinámica del clúster `batman`:

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### Sinopsis {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### Descripción {#description-16}

`patronictl switchover` realiza un switchover en el clúster.

Está pensado para usarse cuando el clúster está en buen estado, por ejemplo:

- Hay líder;
- Hay standbys síncronos disponibles en un clúster síncrono.

> [!NOTE]
> Si tu clúster no está en buen estado, quizá te interese `patronictl failover`.

<a id="patronictl_switchover_parameters"></a>

#### Parámetros {#parameters-16}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Realiza un switchover en el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`--leader` / `--primary`  
Indica quién es el líder que se degradará en el momento del switchover.

`LEADER_NAME` debe coincidir con el nombre del líder actual del clúster.

`--candidate`  
El nodo que se promoverá en el switchover y que tomará el rol de primario.

`CANDIDATE_NAME` es el nombre del nodo que se va a promover.

`--scheduled`  
Programa un switchover para que ocurra en la marca de tiempo dada.

`TIMESTAMP` es la marca de tiempo en la que debería ocurrir el switchover. Especifícala en un formato sin ambigüedad, preferiblemente con zona horaria. También puedes usar el literal `now` para que el switchover se ejecute inmediatamente.

`--force`  
Opción para omitir los avisos de confirmación al realizar el switchover.

Útil para scripts.

<a id="patronictl_switchover_examples"></a>

#### Ejemplos {#examples-16}

Hacer el switchover con el nodo `postgresql2`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

Programar un switchover entre `postgresql0` y `postgresql2` para que ocurra en `2023-09-13T18:00:00-03:00`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### Sinopsis {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### Descripción {#description-17}

`patronictl topology` muestra información sobre el clúster de Patroni y sus miembros con un enfoque de vista de árbol.

La siguiente información se incluye en la salida:

`Cluster`  
Nombre del clúster de Patroni.

> [!NOTE]
> Se muestra en la cabecera de la tabla.

`System identifier`  
Identificador de sistema de Postgres.

> [!NOTE]
> Se muestra en la cabecera de la tabla.

`Member`  
Nombre del miembro de Patroni.

> [!NOTE]
> La información de esta columna se muestra como una vista de árbol de los miembros en términos de conexiones de replicación.

`Host`  
Host donde se encuentra el miembro.

`Role`  
Rol actual del miembro.

Puede ser uno entre:

- `Leader`: el líder actual de un clúster regular de Patroni; o
- `Standby Leader`: el líder actual de un clúster en espera de Patroni; o
- `Sync Standby`: un standby síncrono de un clúster de Patroni con el modo síncrono habilitado; o
- `Replica`: un standby regular de un clúster de Patroni.

`State`  
Estado actual de Postgres en el miembro de Patroni.

Algunos ejemplos entre los estados posibles:

- `running`: si Postgres está actualmente levantado y en ejecución;
- `streaming`: si es una réplica y Postgres está actualmente transmitiendo WAL desde el nodo primario;
- `in archive recovery`: si es una réplica y Postgres está obteniendo actualmente WAL del archivado;
- `stopped`: si Postgres había sido apagado;
- `crashed`: si Postgres se ha caído.

`TL`  
Línea de tiempo actual de Postgres en el miembro de Patroni.

`Receive LSN`  
La última posición del write-ahead log recibida y sincronizada con el disco por la replicación en flujo del miembro (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Retraso de replicación entre la posición `Receive LSN` del miembro y su upstream, en MB.

`Replay LSN`  
La última posición del write-ahead log reproducida durante la recuperación del miembro (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Retraso de replicación entre la posición `Replay LSN` del miembro y su upstream, en MB.

Además de eso, la siguiente información puede incluirse en la salida:

`Group`  
ID del grupo de Citus.

> [!NOTE]
> Se muestra en la cabecera de la tabla.
>
> Solo se muestra si es un clúster de Citus.

`Pending restart`  
`*` indica que el nodo necesita un reinicio para que alguna configuración de Postgres surta efecto. Un valor vacío indica que el nodo no requiere un reinicio.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si el nodo requiere un reinicio.

`Scheduled restart`  
Marca de tiempo en la que se ha programado un reinicio para la instancia de Postgres gestionada por el miembro de Patroni. Un valor vacío indica que no hay ningún reinicio programado para el miembro.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si el nodo tiene un reinicio programado.

`Tags`  
Contiene las etiquetas establecidas para el miembro de Patroni. Un valor vacío indica que no se ha configurado ninguna etiqueta o que se han configurado con valores predeterminados.

> [!NOTE]
> Se muestra como un atributo de miembro.
>
> Se muestra si el nodo tiene alguna etiqueta personalizada, o alguna etiqueta predeterminada con valores no predeterminados.

`Scheduled switchover`  
Marca de tiempo en la que se ha programado un switchover para el clúster de Patroni, si lo hay.

> [!NOTE]
> Se muestra en el pie de la tabla.
>
> Solo se muestra si hay un switchover programado.

`Maintenance mode`

> Si la monitorización del clúster está actualmente en pausa.
>
> > [!NOTE]
> > Se muestra en el pie de la tabla.
> >
> > Solo se muestra si el clúster está en pausa.

<a id="patronictl_topology_parameters"></a>

#### Parámetros {#parameters-17}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

Si no se proporciona, [patronictl](/es/patroni/patronictl#patronictl) intentará obtenerlo de la configuración de `scope`, si existe.

`--group`  
Muestra información sobre los miembros del grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

`-W`  
Refresca automáticamente la información cada 2 segundos.

`-w` / `--watch`  
Refresca automáticamente la información en el intervalo especificado.

`TIME` es el intervalo entre refrescos, en segundos.

<a id="patronictl_topology_examples"></a>

#### Ejemplos {#examples-17}

Mostrar la topología del clúster `batman` -- `postgresql1` y `postgresql2` están replicando desde `postgresql0`:

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### Sinopsis {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### Descripción {#description-18}

`patronictl version` obtiene la versión de la aplicación [patronictl](/es/patroni/patronictl#patronictl). Además, también puede incluir información de versión sobre los clústeres de Patroni y sus miembros.

<a id="patronictl_version_parameters"></a>

#### Parámetros {#parameters-18}

`CLUSTER_NAME`  
Nombre del clúster de Patroni.

`MEMBER_NAME`  
Nombre del miembro del clúster de Patroni.

`--group`  
Considera un clúster de Patroni con el grupo de Citus dado.

`CITUS_GROUP` es el ID del grupo de Citus.

<a id="patronictl_version_examples"></a>

#### Ejemplos {#examples-18}

Obtener solo la versión de [patronictl](/es/patroni/patronictl#patronictl):

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

Obtener la versión de [patronictl](/es/patroni/patronictl#patronictl) y de todos los miembros del clúster `batman`:

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

Obtener la versión de [patronictl](/es/patroni/patronictl#patronictl) y de los miembros `postgresql1` y `postgresql2` del clúster `batman`:

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
