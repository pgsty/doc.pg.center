---
title: "Uso: comando pgbouncer"
linkTitle: "Uso"
weight: 30
description: "Uso de la línea de comandos de PgBouncer y consola de administración"
icon: fa-solid fa-bell-concierge
module: [PGBOUNCER]
categories: [Tarea]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/doc/usage.md"
---

--------

## Sinopsis {#synopsis}

    pgbouncer [-d][-v][-u user] <pgbouncer.ini>
    pgbouncer -V|-h

En Windows, las opciones son:

    pgbouncer.exe [-v][-u user] <pgbouncer.ini>
    pgbouncer.exe -V|-h

Opciones adicionales para configurar un servicio de Windows:

    pgbouncer.exe --regservice   <pgbouncer.ini>
    pgbouncer.exe --unregservice <pgbouncer.ini>

--------

## Descripción {#description}

**pgbouncer** es un pooler de conexiones de PostgreSQL. Cualquier aplicación
de destino puede conectarse a **pgbouncer** como si fuera un servidor
PostgreSQL, y **pgbouncer** creará una conexión al servidor real, o bien
reutilizará una de sus conexiones existentes.

El objetivo de **pgbouncer** es reducir el impacto en el rendimiento que
supone abrir nuevas conexiones a PostgreSQL.

Para no comprometer la semántica de las transacciones al agrupar
conexiones, **pgbouncer** admite varios tipos de agrupación al rotar
las conexiones:

Agrupación de sesiones

:   El método más cortés. Cuando un cliente se conecta, se le asignará
    una conexión al servidor durante todo el tiempo que el cliente permanezca
    conectado. Cuando el cliente se desconecta, la conexión al servidor
    se devolverá al pool. Este es el método predeterminado.

Agrupación de transacciones

:   Una conexión al servidor se asigna a un cliente únicamente durante
    una transacción. Cuando PgBouncer detecta que la transacción ha
    terminado, la conexión al servidor se devolverá al pool.

Agrupación de instrucciones

:   El método más agresivo. La conexión al servidor se devolverá al pool
    inmediatamente después de que se complete una consulta. Las transacciones
    de varias instrucciones no están permitidas en este modo, ya que se romperían.

La interfaz de administración de **pgbouncer** consiste en una serie de
comandos `SHOW` nuevos, disponibles al conectarse a una base de datos
«virtual» especial: **pgbouncer**.

Desde la versión 1.26.0, PgBouncer envía a los clientes, al iniciar sesión,
los valores `ParameterStatus` `pgbouncer.version`,
`pgbouncer.pool_mode` y `pgbouncer.max_prepared_statements`. Los
controladores pueden usar estos valores para detectar PgBouncer y adaptar
su comportamiento. El parámetro opcional
[`login_notify_message`](/es/pgbouncer/config/#login_notify_message)
envía un NOTICE de bienvenida tras un inicio de sesión correcto.

--------

## Inicio rápido {#quick-start}

La configuración y el uso básicos son los siguientes.

1. Crea un archivo pgbouncer.ini. Los detalles están en **pgbouncer(5)**. Ejemplo sencillo:

        [databases]
        template1 = host=localhost port=5432 dbname=template1

        [pgbouncer]
        listen_port = 6432
        listen_addr = localhost
        auth_type = md5
        auth_file = userlist.txt
        logfile = pgbouncer.log
        pidfile = pgbouncer.pid
        admin_users = someuser

2. Crea un archivo `userlist.txt` que contenga los usuarios permitidos:

        "someuser" "same_password_as_in_server"

3. Inicia **pgbouncer**:

        $ pgbouncer -d pgbouncer.ini

4. Haz que tu aplicación (o el cliente **psql**) se conecte a
   **pgbouncer** en lugar de directamente al servidor PostgreSQL:

        $ psql -p 6432 -U someuser template1

5. Administra **pgbouncer** conectándote a la base de datos de administración
   especial **pgbouncer** y ejecutando `SHOW HELP;` para comenzar:

        $ psql -p 6432 -U someuser pgbouncer
        pgbouncer=# SHOW HELP;
        NOTICE:  Console usage
        DETAIL:
          SHOW [HELP|CONFIG|DATABASES|POOLS|CLIENTS|SERVERS|SOCKETS|LISTS|VERSION|...]
          SET key = arg
          RELOAD
          PAUSE
          RESUME
          SHUTDOWN
          [...]

6. Si has hecho cambios en el archivo pgbouncer.ini, puedes recargarlo con:

        pgbouncer=# RELOAD;

--------

## Opciones de línea de comandos {#command-line-switches}

`-d`, `--daemon`
:   Ejecutar en segundo plano. Sin esta opción, el proceso se ejecutará en
    primer plano.

    En modo demonio, es necesario definir `pidfile`, así como `logfile` o
    `syslog`. No se escribirá ningún mensaje de registro en stderr después
    de pasar a segundo plano.

    Nota: No funciona en Windows; **pgbouncer** debe ejecutarse allí como
    un servicio.

`-u` _USERNAME_, `--user=` _USERNAME_
:   Cambia al usuario indicado al iniciar.

`-v`, `--verbose`
:   Aumenta el nivel de detalle. Se puede usar varias veces.

`-q`, `--quiet`
:   Modo silencioso: no registra en stderr. Esto no afecta a la verbosidad
    del registro, solo a que no se use stderr.
    Para su uso en scripts de init.d.

`-V`, `--version`
:   Muestra la versión.

`-h`, `--help`
:   Muestra una ayuda breve.

`--regservice`
:   Win32: Registra PgBouncer para ejecutarse como servicio de Windows.
    El valor del parámetro de configuración **service_name** se usa como
    nombre bajo el cual registrar.

`--unregservice`
:   Win32: Elimina el registro del servicio de Windows.

--------

## Consola de administración {#admin-console}

La consola está disponible conectándose de la forma habitual a la
base de datos **pgbouncer**:

    $ psql -p 6432 pgbouncer

Solo los usuarios listados en los parámetros de configuración **admin_users** o **stats_users**
pueden iniciar sesión en la consola. (Excepto cuando `auth_type=any`; en ese caso,
cualquier usuario puede entrar como stats_user).

Además, el nombre de usuario **pgbouncer** puede iniciar sesión sin contraseña,
si el inicio de sesión se realiza mediante el socket Unix y el cliente tiene
el mismo UID de usuario Unix que el proceso en ejecución.

Actualmente, la consola de administración solo admite el protocolo de consulta
simple. Algunos controladores usan el protocolo de consulta extendida para todos
los comandos; estos controladores no funcionarán para esto.

### Comandos de visualización {#show-commands}

Los comandos **SHOW** muestran información. Cada comando se describe a continuación.

#### SHOW STATS {#show-stats}

Muestra estadísticas. En este comando y en los relacionados, las cifras totales
son desde el inicio del proceso, y los promedios se actualizan cada `stats_period`.

database
:   Las estadísticas se presentan por base de datos.

total_xact_count
:   Número total de transacciones SQL agrupadas por **pgbouncer**.

total_query_count
:   Número total de comandos SQL agrupados por **pgbouncer**.

total_server_assignment_count
:   Número total de veces que se asignó un servidor a un cliente.

total_received
:   Volumen total en bytes del tráfico de red recibido por **pgbouncer**.

total_sent
:   Volumen total en bytes del tráfico de red enviado por **pgbouncer**.

total_xact_time
:   Número total de microsegundos que **pgbouncer** pasó conectado
    a PostgreSQL en una transacción, ya sea inactivo en una transacción o
    ejecutando consultas.

total_query_time
:   Número total de microsegundos que **pgbouncer** pasó conectado
    activamente a PostgreSQL, ejecutando consultas.

total_wait_time
:   Tiempo que los clientes pasan esperando un servidor, en microsegundos. Se
    actualiza cuando a una conexión de cliente se le asigna una conexión de backend.

total_client_parse_count
:   Número total de instrucciones preparadas creadas por los clientes. Solo aplicable
    en el modo de seguimiento de instrucciones preparadas con nombre, véase `max_prepared_statements`.

total_server_parse_count
:   Número total de instrucciones preparadas creadas por **pgbouncer** en un servidor. Solo
    aplicable en el modo de seguimiento de instrucciones preparadas con nombre, véase `max_prepared_statements`.

total_bind_count
:   Número total de instrucciones preparadas dejadas listas para su ejecución por los clientes y
    reenviadas a PostgreSQL por **pgbouncer**. Solo aplicable en el modo de seguimiento de
    instrucciones preparadas con nombre, véase `max_prepared_statements`.

total_client_login_count
:   Número total de inicios de sesión de clientes correctos.

avg_xact_count
:   Promedio de transacciones por segundo en el último período de estadísticas.

avg_query_count
:   Promedio de consultas por segundo en el último período de estadísticas.

avg_server_assignment_count
:   Promedio de veces por segundo que se asignó un servidor a un cliente en el
    último período de estadísticas.

avg_recv
:   Promedio de bytes recibidos (de los clientes) por segundo.

avg_sent
:   Promedio de bytes enviados (a los clientes) por segundo.

avg_xact_time
:   Duración promedio de las transacciones, en microsegundos.

avg_query_time
:   Duración promedio de las consultas, en microsegundos.

avg_wait_time
:   Tiempo que los clientes pasan esperando un servidor, en microsegundos (promedio
    de los tiempos de espera de los clientes a los que se asignó un backend durante
    el `stats_period` actual).

avg_client_parse_count
:   Promedio de instrucciones preparadas creadas por los clientes por segundo. Solo aplicable
    en el modo de seguimiento de instrucciones preparadas con nombre, véase `max_prepared_statements`.

avg_server_parse_count
:   Promedio de instrucciones preparadas creadas por **pgbouncer** en un servidor por segundo. Solo
    aplicable en el modo de seguimiento de instrucciones preparadas con nombre, véase `max_prepared_statements`.

avg_bind_count
:   Promedio de instrucciones preparadas por segundo dejadas listas para su ejecución por los clientes
    y reenviadas a PostgreSQL por **pgbouncer**. Solo aplicable en el modo de seguimiento de
    instrucciones preparadas con nombre, véase `max_prepared_statements`.

avg_client_login_count
:   Promedio de inicios de sesión de clientes correctos por segundo.

#### SHOW STATS_TOTALS {#show-stats_totals}

Muestra estadísticas acumulativas por base de datos correspondientes a los campos **total_** de **SHOW STATS**. Los nombres de las columnas de salida omiten el prefijo **total_**; por ejemplo, **total_query_count** se llama **query_count**.


#### SHOW STATS_AVERAGES {#show-stats_averages}

Subconjunto de **SHOW STATS** que muestra los valores promedio (**avg_**).

#### SHOW TOTALS {#show-totals}

Como **SHOW STATS**, pero agregado entre todas las bases de datos.

#### SHOW SERVERS {#show-servers}

type
:   S, de servidor.

user
:   Nombre de usuario que **pgbouncer** usa para conectarse al servidor.

database
:   Nombre de la base de datos.

replication
:   Si la conexión del servidor usa replicación. Puede ser **none**, **logical** o **physical**.

state
:   Estado de la conexión al servidor de PgBouncer, uno de: **active**,
    **idle**, **used**, **tested**, **new**, **active_cancel**,
    **being_canceled**.

addr
:   Dirección IP del servidor PostgreSQL.

port
:   Puerto del servidor PostgreSQL.

local_addr
:   Dirección de inicio de la conexión en la máquina local.

local_port
:   Puerto de inicio de la conexión en la máquina local.

connect_time
:   Cuándo se realizó la conexión.

request_time
:   Cuándo se emitió la última solicitud.

wait
:   No se usa para conexiones de servidor.

wait_us
:   No se usa para conexiones de servidor.

close_needed
:   1 si la conexión se cerrará lo antes posible,
    porque una recarga del archivo de configuración o una actualización de DNS
    cambió la información de la conexión o porque se emitió **RECONNECT**.

ptr
:   Dirección del objeto interno de esta conexión.

link
:   Dirección de la conexión de cliente con la que el servidor está emparejado.

remote_pid
:   PID del proceso del servidor de backend. Si la conexión se realiza mediante
    un socket Unix y el sistema operativo admite obtener información del ID de
    proceso, su PID del sistema operativo. De lo contrario, se extrae del paquete
    de cancelación que envió el servidor, que debería ser el PID si el servidor
    es PostgreSQL, pero es un número aleatorio si el servidor es otro PgBouncer.

tls
:   Una cadena con información de la conexión TLS, o vacía si no se usa TLS.

application_name
:   Una cadena que contiene el `application_name` definido en la conexión de
    cliente vinculada, o vacía si no está definido o si no hay conexión vinculada.

prepared_statements
:  La cantidad de instrucciones preparadas que están preparadas en el servidor. Este
   número está limitado por el parámetro `max_prepared_statements`.

id
:   ID único del servidor.


#### SHOW CLIENTS {#show-clients}

type
:   C, de cliente.

user
:   Usuario con el que se conectó el cliente.

database
:   Nombre de la base de datos.

replication
:   Si la conexión del cliente usa replicación. Puede ser **none**, **logical** o **physical**.

state
:   Estado de la conexión del cliente, uno de: **active** (conexiones de cliente
    que están vinculadas a conexiones de servidor), **idle** (conexiones de cliente
    sin consultas pendientes de procesar), **waiting**,
    **active_cancel_req** o **waiting_cancel_req**.

addr
:   Dirección IP del cliente.

port
:   Puerto de origen del cliente.

local_addr
:   Dirección final de la conexión en la máquina local.

local_port
:   Puerto final de la conexión en la máquina local.

connect_time
:   Marca de tiempo de la conexión.

request_time
:   Marca de tiempo de la última solicitud del cliente.

wait
:   Tiempo de espera actual en segundos.

wait_us
:   Parte de microsegundos del tiempo de espera actual.

close_needed
:   no se usa para clientes

ptr
:   Dirección del objeto interno de esta conexión.

link
:   Dirección de la conexión de servidor con la que el cliente está emparejado.

remote_pid
:   ID del proceso, en caso de que el cliente se conecte mediante un socket Unix
    y el sistema operativo admita obtenerlo.

tls
:   Una cadena con información de la conexión TLS, o vacía si no se usa TLS.

application_name
:   Una cadena que contiene el `application_name` definido por el cliente
    para esta conexión, o vacía si no se definió.

prepared_statements
:  La cantidad de instrucciones preparadas que el cliente ha preparado

id
:   ID único del cliente.

#### SHOW POOLS {#show-pools}

Se crea una nueva entrada de pool por cada par (base de datos, usuario).

database
:   Nombre de la base de datos.

user
:   Nombre de usuario.

cl_active
:   Conexiones de cliente que están vinculadas a conexiones de servidor o que están inactivas sin consultas pendientes de procesar.

cl_waiting
:   Conexiones de cliente que han enviado consultas pero que todavía no han obtenido una conexión de servidor.

cl_active_cancel_req
:   Conexiones de cliente que han reenviado cancelaciones de consultas al servidor y
    esperan la respuesta del servidor.

cl_waiting_cancel_req
:   Conexiones de cliente que todavía no han reenviado cancelaciones de consultas al servidor.

sv_active
:   Conexiones de servidor que están vinculadas a un cliente.

sv_active_cancel
:   Conexiones de servidor que actualmente están reenviando una solicitud de cancelación.

sv_being_canceled
:   Servidores que normalmente podrían pasar a estar inactivos, pero que esperan
    para hacerlo hasta que se completen todas las solicitudes de cancelación en
    curso que se enviaron para cancelar una consulta en este servidor.

sv_idle
:   Conexiones de servidor que no se usan y que están disponibles de inmediato para consultas de clientes.

sv_used
:   Conexiones de servidor que han estado inactivas durante más de `server_check_delay`,
    por lo que necesitan que se ejecute `server_check_query` en ellas antes de poder usarse de nuevo.

sv_tested
:   Conexiones de servidor que actualmente están ejecutando `server_reset_query`
    o `server_check_query`.

sv_login
:   Conexiones de servidor que actualmente están en proceso de iniciar sesión.

maxwait
:   Cuánto tiempo ha esperado el primer cliente (el más antiguo) de la cola, en segundos.
    Si este valor empieza a aumentar, el pool actual de servidores no atiende
    las solicitudes con la suficiente rapidez. La razón puede ser un servidor
    sobrecargado o simplemente un valor de **pool_size** demasiado pequeño.

maxwait_us
:   Parte de microsegundos del tiempo de espera máximo.

pool_mode
:   El modo de agrupación en uso.

load_balance_hosts
:   El load_balance_hosts en uso si el host del pool contiene una lista separada por comas.

#### SHOW PEER_POOLS {#show-peer_pools}

Se crea una nueva entrada de peer_pool por cada peer configurado.

peer_id
:   ID de la entrada del peer configurado.

cl_active_cancel_req
:   Conexiones de cliente que han reenviado cancelaciones de consultas al servidor y
    esperan la respuesta del servidor.

cl_waiting_cancel_req
:   Conexiones de cliente que todavía no han reenviado cancelaciones de consultas al servidor.

sv_active_cancel
:   Conexiones de servidor que actualmente están reenviando una solicitud de cancelación.

sv_login
:   Conexiones de servidor que actualmente están en proceso de iniciar sesión.

#### SHOW LISTS {#show-lists}

Muestra las siguientes listas internas y sus recuentos de elementos, con una lista por fila en las columnas **list** e **items**.

databases
:   Recuento de bases de datos.

users
:   Recuento de usuarios.

peers
:   Número de peers configurados.

pools
:   Recuento de pools.

peer_pools
:   Número de pools de peers.

free_clients
:   Recuento de clientes libres. Son clientes que están desconectados, pero
    PgBouncer conserva la memoria que se asignó para ellos, de modo que pueda
    reutilizarse para clientes futuros y así evitar asignaciones.

used_clients
:   Recuento de clientes en uso.

login_clients
:   Recuento de clientes en estado **login**.

free_servers
:   Recuento de servidores libres. Son servidores que están desconectados, pero
    PgBouncer conserva la memoria que se asignó para ellos, de modo que pueda
    reutilizarse para servidores futuros y así evitar asignaciones.

used_servers
:   Recuento de servidores en uso.

dns_names
:   Recuento de nombres de DNS en la caché.

dns_zones
:   Recuento de zonas de DNS en la caché.

dns_queries
:   Recuento de consultas de DNS en curso.

dns_pending
:   no se usa

#### SHOW USERS {#show-users}

name
:   El nombre de usuario

pool_size
:   El valor de pool_size específico del usuario, o una cadena vacía si no está definido.

reserve_pool_size
:   El valor de reserve_pool_size específico del usuario, o una cadena vacía si no está definido.

pool_mode
:   El pool_mode específico del usuario, o NULL si no está definido.

max_user_connections
:   El parámetro max_user_connections del usuario. Si este parámetro no está definido
    para este usuario en concreto, se mostrará el valor predeterminado.

current_connections
:   Número actual de conexiones de servidor que este usuario tiene abiertas hacia todos los servidores.

max_user_client_connections
:   El parámetro max_user_client_connections del usuario. Si este parámetro no está definido
    para este usuario en concreto, se mostrará el valor predeterminado.

current_client_connections
:   Número actual de conexiones de cliente que este usuario tiene abiertas hacia PgBouncer.

#### SHOW DATABASES {#show-databases}

name
:   Nombre de la entrada de base de datos configurada.

host
:   Host al que se conecta PgBouncer.

port
:   Puerto al que se conecta PgBouncer.

database
:   Nombre real de la base de datos a la que se conecta PgBouncer.

force_user
:   Cuando el usuario forma parte de la cadena de conexión, la conexión entre
    PgBouncer y PostgreSQL se fuerza al usuario indicado, sea cual sea el
    usuario del cliente.

pool_size
:   Número máximo de conexiones de servidor.

min_pool_size
:   Número mínimo de conexiones de servidor.

reserve_pool_size
:   Número máximo de conexiones adicionales para esta base de datos.

server_lifetime
:   La duración máxima de una conexión de servidor para esta base de datos

pool_mode
:   El pool_mode específico de la base de datos, o NULL si se usará el predeterminado.

load_balance_hosts
:   El load_balance_hosts de la base de datos si el host contiene una lista separada por comas.

max_connections
:   Número máximo de conexiones de servidor permitidas para esta base de datos, según lo
    definido por **max_db_connections**, ya sea globalmente o por base de datos.

current_connections
:   Número actual de conexiones de servidor para esta base de datos.

max_client_connections
:   Número máximo de conexiones de cliente permitidas para esta base de datos, según lo definido por max_db_client_connections globalmente o por base de datos.

current_client_connections
:   Número actual de conexiones de cliente para esta base de datos.

paused
:   1 si esta base de datos está actualmente en pausa, 0 en caso contrario.

disabled
:   1 si esta base de datos está actualmente deshabilitada, 0 en caso contrario.

#### SHOW PEERS {#show-peers}

peer_id
:   ID de la entrada del peer configurado.

host
:   Host al que se conecta PgBouncer.

port
:   Puerto al que se conecta PgBouncer.

pool_size
:   Número máximo de conexiones de servidor que pueden establecerse hacia este peer

#### SHOW SOCKETS, SHOW ACTIVE_SOCKETS {#show-sockets-show-active_sockets}

Muestra información de bajo nivel sobre los sockets o solo los sockets activos.
Esto incluye la información mostrada en **SHOW CLIENTS** y **SHOW SERVERS**, así como otra información de aún más bajo nivel.

#### SHOW CONFIG {#show-config}

Muestra los parámetros de configuración actuales, uno por fila, con las
siguientes columnas:

key
:   Nombre de la variable de configuración

value
:   Valor de configuración

default
:   Valor predeterminado de configuración

changeable
:   **yes** o **no**; indica si la variable puede cambiarse en ejecución.
    Si es **no**, la variable solo puede cambiarse en el arranque. Usa
    **SET** para cambiar una variable en tiempo de ejecución.

#### SHOW MEM {#show-mem}

Muestra información de bajo nivel sobre los tamaños actuales de varias
asignaciones de memoria internas. La información presentada puede cambiar.

#### SHOW DNS_HOSTS {#show-dns_hosts}

Muestra los nombres de host en la caché de DNS.

hostname
:   Nombre de host.

ttl
:   Cuántos segundos faltan para la siguiente resolución.

addrs
:   Lista de direcciones separada por comas.

#### SHOW DNS_ZONES {#show-dns_zones}

Muestra las zonas de DNS en la caché.

zonename
:   Nombre de la zona.

serial
:   Número de serie actual.

count
:   Nombres de host que pertenecen a esta zona.


#### SHOW VERSION {#show-version}

Muestra la cadena de versión de PgBouncer.

#### SHOW STATE {#show-state}

Muestra los estados de PgBouncer. Los estados actuales son active y paused.

### Comandos de control del proceso {#process-controlling-commands}

#### PAUSE [db] {#pause-db}

PgBouncer intenta desconectarse de todos los servidores. Para desconectar cada conexión
de servidor, espera a que esa conexión de servidor se libere según el modo de agrupación
del pool de servidores (en el modo de agrupación por transacciones, la transacción debe
completarse; en el modo por instrucciones, la instrucción debe completarse; y en el modo de
agrupación por sesiones, el cliente debe desconectarse).
El comando no volverá antes de que se hayan desconectado todas las conexiones de servidor.
Para usar en el momento del reinicio de la base de datos.

Si se indica un nombre de base de datos, solo se pausará esa base de datos.

Las nuevas conexiones de cliente a una base de datos en pausa esperarán hasta que
se llame a **RESUME**.

#### DISABLE db {#disable-db}

Rechaza todas las nuevas conexiones de cliente en la base de datos indicada.

#### ENABLE db {#enable-db}

Permite nuevas conexiones de cliente después de un comando **DISABLE** previo.

#### RECONNECT [db] {#reconnect-db}

Cierra cada conexión de servidor abierta de la base de datos indicada, o de todas
las bases de datos, después de que se libere (según el modo de agrupación), incluso
si su duración aún no ha expirado. Se pueden establecer nuevas conexiones de
servidor de inmediato y se conectarán según sea necesario de acuerdo con los
parámetros de tamaño del pool.

Este comando es útil cuando la configuración de las conexiones al servidor ha
cambiado, por ejemplo para realizar una conmutación gradual a un servidor nuevo.
*No* es necesario ejecutar este comando cuando la cadena de conexión de
pgbouncer.ini se ha cambiado y recargado (véase **RELOAD**) o cuando la
resolución DNS ha cambiado, porque entonces se ejecutará automáticamente el
equivalente de este comando. Este comando solo es necesario si algo situado
por debajo de PgBouncer enruta las conexiones.

Después de ejecutar este comando, podría haber un período prolongado en el que
algunas conexiones de servidor vayan a un destino antiguo y algunas conexiones
de servidor vayan a un destino nuevo. Esto probablemente solo tenga sentido
al cambiar tráfico de solo lectura entre réplicas de solo lectura, o al cambiar
entre nodos de una configuración de replicación multimáster. Si todas las
conexiones deben cambiarse al mismo tiempo, se recomienda usar **PAUSE**. Para
cerrar conexiones de servidor sin esperar (por ejemplo, en escenarios de
conmutación por error de emergencia en lugar de conmutación gradual),
considera también **KILL**.

#### KILL [db] {#kill-db}

Cierra de inmediato todas las conexiones de cliente y de servidor en la base de datos indicada
o en todas las bases de datos, excluyendo la base de datos de administración.

Las nuevas conexiones de cliente a una base de datos afectada por KILL esperarán hasta
que se llame a **RESUME**.

#### KILL_CLIENT id {#kill_client-id}

Termina de inmediato la conexión de cliente especificada junto con cualquier conexión
de servidor del cliente indicado. El cliente que se va a terminar se identifica
por el valor `id`, que puede encontrarse con el comando `SHOW CLIENTS`.

Un comando de ejemplo tendrá un aspecto similar a `KILL_CLIENT 1234`.

#### RESUME [db] {#resume-db}

Reanuda el trabajo tras un comando **KILL** o **PAUSE** previo.

#### SHUTDOWN {#shutdown}

El proceso de PgBouncer terminará.

#### SHUTDOWN WAIT_FOR_SERVERS {#shutdown-wait_for_servers}

Deja de aceptar nuevas conexiones y se apaga después de que se liberen todos los servidores.
Esto es básicamente lo mismo que emitir **PAUSE** y **SHUTDOWN**, salvo que
también deja de aceptar nuevas conexiones mientras espera el **PAUSE**, además
de desconectar de inmediato a los clientes que están esperando recibir una conexión
de servidor. Ten en cuenta que los sockets UNIX permanecerán abiertos durante el apagado,
pero solo aceptarán conexiones a la consola de administración de PgBouncer.

#### SHUTDOWN WAIT_FOR_CLIENTS {#shutdown-wait_for_clients}

Deja de aceptar nuevas conexiones y apaga el proceso una vez que todos los clientes
existentes se hayan desconectado. Ten en cuenta que los sockets UNIX permanecerán
abiertos durante el apagado, pero solo aceptarán conexiones a la consola de
administración de pgbouncer. Este comando puede usarse para hacer un reinicio
progresivo sin tiempo de inactividad de dos procesos de PgBouncer mediante el
siguiente procedimiento:

1. Ejecuta dos o más procesos de PgBouncer en el mismo puerto usando
   `so_reuseport` (se recomienda [configurar el emparejamiento](/es/pgbouncer/config/#section-peers),
   pero no es obligatorio). Para lograr un tiempo de inactividad cero al
   reiniciar, reiniciaremos estos procesos uno por uno, dejando los demás
   en ejecución para aceptar conexiones mientras uno se reinicia.
2. Elige un proceso para reiniciar primero; llamémoslo A.
3. Ejecuta `SHUTDOWN WAIT_FOR_CLIENTS` (o envía `SIGTERM`) al proceso A.
4. Haz que todos los clientes se reconecten. Posiblemente esperando un tiempo
   hasta que el pooler del lado del cliente provoque reconexiones debido a su
   `server_idle_timeout` (o una configuración similar). O, si no se usa ningún
   pooler del lado del cliente, posiblemente reiniciando los clientes. Una vez
   que todos los clientes se hayan reconectado, el proceso A terminará
   automáticamente, porque ya no hay clientes conectados a él.
5. Inicia el proceso A de nuevo.
6. Repite los pasos 3, 4 y 5 para cada uno de los procesos restantes, uno por uno,
   hasta que hayas reiniciado todos los procesos.


#### RELOAD {#reload}

El proceso de PgBouncer recargará sus archivos de configuración y actualizará
los parámetros que se pueden cambiar. Esto incluye el archivo de configuración
principal, así como los archivos especificados por los parámetros `auth_file` y
`auth_hba_file`.

PgBouncer detecta cuando una recarga de un archivo de configuración cambia
los parámetros de conexión de una definición de base de datos. Una conexión
de servidor existente al destino antiguo se cerrará la próxima vez que se
libere la conexión de servidor (según el modo de agrupación), y las nuevas
conexiones de servidor usarán de inmediato los parámetros de conexión
actualizados.

#### WAIT_CLOSE [db] {#wait_close-db}

Espera hasta que todas las conexiones de servidor, ya sea de la base de datos especificada o
de todas las bases de datos, hayan salido del estado «close_needed» (véase **SHOW SERVERS**). Se puede llamar después de un **RECONNECT** o **RELOAD** para
esperar hasta que el cambio de configuración respectivo se haya activado por
completo, por ejemplo en scripts de conmutación.

### Otros comandos {#other-commands}

#### SET key = arg {#set-key--arg}

Cambia un parámetro de configuración (véase también **SHOW CONFIG**). Por ejemplo:

    SET log_connections = 1;
    SET server_check_query = 'select 2';

(Ten en cuenta que este comando se ejecuta en la consola de administración de PgBouncer
y define parámetros de PgBouncer. Un comando **SET** ejecutado en otra base de datos se
pasará al backend de PostgreSQL como cualquier otro comando SQL.)

### Señales {#signals}

SIGHUP
:   Recarga la configuración. Equivale a emitir el comando **RELOAD** en la consola.

SIGTERM
:   Apagado súper seguro. Espera a que todos los clientes existentes se desconecten, pero no
    acepta nuevas conexiones. Equivale a emitir **SHUTDOWN WAIT_FOR_CLIENTS**
    en la consola. Si se recibe esta señal cuando ya hay un apagado en curso,
    se desencadena un «apagado inmediato» en lugar de un «apagado súper seguro». En
    versiones de PgBouncer anteriores a 1.23.0, esta señal provocaba un «apagado
    inmediato».

SIGINT
:   Apagado seguro. Equivale a emitir **SHUTDOWN WAIT_FOR_SERVERS** en la consola.
    Si se recibe esta señal cuando ya hay un apagado en curso,
    se desencadena un «apagado inmediato» en lugar de un «apagado seguro».

SIGQUIT
:   Apagado inmediato. Equivale a emitir **SHUTDOWN** en la consola.

SIGUSR1
:   Equivale a emitir **PAUSE** en la consola.

SIGUSR2
:   Equivale a emitir **RESUME** en la consola.

### Parámetros de Libevent {#libevent-settings}

De la documentación de Libevent:

> Es posible deshabilitar la compatibilidad con epoll, kqueue, devpoll, poll
> o select estableciendo la variable de entorno EVENT_NOEPOLL,
> EVENT_NOKQUEUE, EVENT_NODEVPOLL, EVENT_NOPOLL o EVENT_NOSELECT,
> respectivamente.
>
> Al establecer la variable de entorno EVENT_SHOW_METHOD, libevent
> muestra el método de notificación del kernel que utiliza.

--------

## Véase también {#see-also}

pgbouncer(5) - página del manual con las descripciones de los parámetros de configuración

<https://www.pgbouncer.org/>
