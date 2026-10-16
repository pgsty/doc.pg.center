---
title: "Configuración: pgbouncer.ini"
linkTitle: "Configuración"
weight: 20
description: "Referencia del archivo de configuración de PgBouncer (pgbouncer.ini)"
icon: fa-solid fa-code
module: [PGBOUNCER]
categories: [Referencia]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/doc/config.md"
---

--------

## Descripción {#description}

El archivo de configuración está en formato «ini». Los nombres de las secciones van entre `[` y `]`. Las líneas que comienzan con `;` o `#` se toman como comentarios y se ignoran. Los caracteres `;` y `#` no se reconocen como especiales cuando aparecen más adelante en la línea.

--------

## Parámetros genéricos {#generic-settings}

### logfile {#logfile}

Especifica el archivo de registro. Para demonizar (`-d`), se debe establecer este parámetro o `syslog`.

El archivo de registro se mantiene abierto, así que después de una rotación se debe ejecutar `kill -HUP` o `RELOAD;` en la consola. En Windows, el servicio debe detenerse e iniciarse.

Ten en cuenta que establecer `logfile` no desactiva por sí solo el registro en stderr. Usa para ello la opción de línea de comandos `-q` o `-d`.

Predeterminado: sin establecer

### pidfile {#pidfile}

Especifica el archivo de PID. Sin `pidfile` establecido, no se permite la demonización (`-d`).

Predeterminado: sin establecer

### listen_addr {#listen_addr}

Especifica una lista (separada por comas) de direcciones en las que escuchar conexiones TCP. También puedes usar `*`, que significa «escuchar en todas las direcciones». Cuando no está establecido, solo se aceptan conexiones mediante socket Unix.

Las direcciones pueden especificarse numéricamente (IPv4/IPv6) o por nombre.

Predeterminado: sin establecer

### listen_port {#listen_port}

Puerto en el que escuchar. Se aplica tanto a sockets TCP como a sockets Unix.

Predeterminado: 6432

### unix_socket_dir {#unix_socket_dir}

Especifica la ubicación de los sockets Unix. Se aplica tanto al socket de escucha como a las conexiones de servidor. Si se establece como cadena vacía, los sockets Unix se desactivan. Un valor que comienza con `@` especifica que se debe crear un socket Unix en el espacio de nombres abstracto (actualmente compatible con Linux y Windows).

Predeterminado: `/tmp` (vacío en Windows)

### unix_socket_mode {#unix_socket_mode}

Modo del sistema de archivos para el socket Unix. Se ignora para sockets en el espacio de nombres abstracto. No es compatible con Windows.

Predeterminado: 0777

### unix_socket_group {#unix_socket_group}

Nombre de grupo a usar para el socket Unix. Se ignora para sockets en el espacio de nombres abstracto. No es compatible con Windows.

Predeterminado: sin establecer

### user {#user}

Si se establece, especifica el usuario de Unix al que cambiar después del arranque. Funciona solo si PgBouncer se inicia como root o si ya se está ejecutando como el usuario indicado. No es compatible con Windows.

Predeterminado: sin establecer

### pool_mode {#pool_mode}

Especifica cuándo puede una conexión de servidor ser reutilizada por otros clientes.

- **`session`**: El servidor se devuelve al pool después de que el cliente se desconecta. Predeterminado.
- **`transaction`**: El servidor se devuelve al pool después de que termina la transacción.
- **`statement`**: El servidor se devuelve al pool después de que termina la consulta. Las transacciones que abarcan múltiples instrucciones no están permitidas en este modo.

### max_client_conn {#max_client_conn}

Número máximo de conexiones de cliente permitidas.

Cuando se aumenta este parámetro, puede que también haya que aumentar los límites de descriptores de archivo del sistema operativo. Ten en cuenta que el número de descriptores de archivo potencialmente usados es mayor que `max_client_conn`. Si cada usuario se conecta al servidor con su propio nombre de usuario, el máximo teórico usado es:

```text
max_client_conn + (max pool_size * total databases * total users)
```

Si se especifica un usuario de base de datos en la cadena de conexión (todos los usuarios se conectan con el mismo nombre de usuario), el máximo teórico es:

```text
max_client_conn + (max pool_size * total databases)
```

El máximo teórico nunca debería alcanzarse, salvo que alguien elabore deliberadamente una carga especial para ello. Aun así, esto significa que debes fijar el número de descriptores de archivo en un valor prudentemente alto.

Busca `ulimit` en la página de manual de tu shell favorito. Nota: `ulimit` no se aplica en un entorno Windows.

Predeterminado: 100

### default_pool_size {#default_pool_size}

El número máximo de conexiones de servidor permitidas por par usuario/base de datos. Puede sobrescribirse con `pool_size` en la configuración por base de datos y por usuario; este es el valor predeterminado que se usa si no se especifica un `pool_size` específico para una base de datos o usuario dados.

Predeterminado: 20

### min_pool_size {#min_pool_size}

Añade más conexiones de servidor al pool si está por debajo de este número. Mejora el comportamiento cuando la carga normal regresa de repente tras un período de inactividad total. El valor queda efectivamente limitado al tamaño del pool.

Solo se aplica a los pools en los que al menos una de las siguientes condiciones es cierta:

* la entrada de la sección `[databases]` para el pool tiene un valor establecido para la clave `user` (también conocido como usuario forzado)
* hay al menos un cliente conectado al pool

Predeterminado: 0 (desactivado)

### reserve_pool_size {#reserve_pool_size}

Cuántas conexiones adicionales permitir a un pool (ver `reserve_pool_timeout`). 0 desactiva.

Predeterminado: 0 (desactivado)

### reserve_pool_timeout {#reserve_pool_timeout}

Si un cliente no ha sido atendido en este tiempo, se usan conexiones adicionales del pool de reserva. 0 desactiva. [segundos]

Predeterminado: 5.0

### max_db_connections {#max_db_connections}

No permitir más que este número de conexiones de servidor por base de datos (independientemente del usuario). Esto considera la base de datos de PgBouncer a la que se ha conectado el cliente, no la base de datos de PostgreSQL de la conexión saliente.

Esto también puede establecerse por base de datos en la sección `[databases]`.

Ten en cuenta que al alcanzar el límite, cerrar una conexión de cliente a un pool no permitirá de inmediato establecer una conexión de servidor para otro pool, porque la conexión de servidor del primer pool sigue abierta. Una vez que la conexión de servidor se cierra (por tiempo de espera de inactividad), se abrirá inmediatamente una nueva conexión de servidor para el pool en espera.

Predeterminado: 0 (sin límite)

### max_db_client_connections {#max_db_client_connections}

No permitir más que este número de conexiones de cliente a PgBouncer por base de datos (independientemente del usuario). Esto considera la base de datos de PgBouncer a la que se ha conectado el cliente, no la base de datos de PostgreSQL de la conexión saliente.

Esto debería establecerse en un número mayor o igual que max_db_connections. La diferencia entre ambos números puede considerarse como cuántas conexiones a una base de datos dada pueden estar en la cola mientras esperan a que terminen las conexiones activas.

Esto también puede establecerse por base de datos en la sección `[databases]`.

Predeterminado: 0 (sin límite)

### max_user_connections {#max_user_connections}

No permitir más que este número de conexiones de servidor por usuario (independientemente de la base de datos). Esto considera el usuario de PgBouncer que está asociado a un pool, que es el usuario especificado para la conexión de servidor o, en su defecto, el usuario con el que se ha conectado el cliente.

Esto también puede establecerse por usuario en la sección `[users]`.

Ten en cuenta que al alcanzar el límite, cerrar una conexión de cliente a un pool no permitirá de inmediato establecer una conexión de servidor para otro pool, porque la conexión de servidor del primer pool sigue abierta. Una vez que la conexión de servidor se cierra (por tiempo de espera de inactividad), se abrirá inmediatamente una nueva conexión de servidor para el pool en espera.

Predeterminado: 0 (sin límite)

### max_user_client_connections {#max_user_client_connections}

No permitir más que este número de conexiones de cliente por usuario (independientemente de la base de datos). Este valor debería establecerse en un número mayor que max_user_connections. La diferencia entre max_user_connections y max_user_client_connections puede conceptualizarse como el tamaño máximo de la cola para el usuario.

Esto también puede establecerse por usuario en la sección `[users]`.

Predeterminado: 0 (sin límite)

### server_round_robin {#server_round_robin}

De forma predeterminada, PgBouncer reutiliza las conexiones de servidor de manera LIFO (última en entrar, primera en salir), de modo que pocas conexiones reciben la mayor parte de la carga. Esto ofrece el mejor rendimiento si tienes un único servidor sirviendo una base de datos. Pero si hay un sistema round-robin detrás de una dirección de base de datos (TCP, DNS o lista de hosts), entonces es mejor que PgBouncer también use las conexiones de esa manera, logrando así una carga uniforme.

Predeterminado: 0

### track_extra_parameters {#track_extra_parameters}

De forma predeterminada, PgBouncer rastrea todos los parámetros que Postgres reporta al cliente y que el cliente puede cambiar:

- `application_name`
- `client_encoding`
- `DateStyle`
- `default_transaction_read_only`
- `IntervalStyle`
- `scram_iterations` (desde la versión 16 de PostgreSQL)
- `search_path` (desde la versión 18 de PostgreSQL)
- `session_authorization`
- `standard_conforming_strings`
- `TimeZone`

Para permitir que se rastreen otros parámetros, pueden especificarse aquí, de modo que PgBouncer sepa que deben mantenerse en la caché de variables del cliente y restaurarse en el servidor cada vez que el cliente se active.

Si necesitas especificar múltiples valores, usa una lista separada por comas (p. ej. `some_extension.setting, other_extension.setting`)

Nota: La mayoría de los parámetros no pueden rastrearse por completo de esta forma. PgBouncer solo se entera de los cambios hechos con `SET` para los parámetros que Postgres reporta al cliente. Postgres tiene [una lista oficial de parámetros que reporta al cliente](https://www.postgresql.org/docs/current/protocol-flow.html#PROTOCOL-ASYNC). Sin embargo, las extensiones de Postgres pueden cambiar esta lista: pueden añadir parámetros propios que también reportan, y pueden empezar a reportar parámetros ya existentes que Postgres no reporta. En particular, Citus 12.0+ hace que Postgres también reporte `search_path`. Algunos de los parámetros que se rastrean de forma predeterminada también solo los reportan las versiones más recientes de Postgres: `default_transaction_read_only` desde Postgres 14, `scram_iterations` desde Postgres 16 y `search_path` desde Postgres 18.

Para un parámetro rastreado que Postgres no reporta (p. ej. `search_path` en versiones de Postgres anteriores a la 18), PgBouncer solo conoce el valor que un cliente especificó en su paquete de arranque (o en el parámetro de arranque `options`). Ese valor se aplica a la conexión de servidor cada vez que el cliente se activa, y el parámetro se restablece a su valor predeterminado para los clientes que no lo especificaron. Los cambios hechos con `SET` después de conectarse no se rastrean para tales parámetros, por lo que se filtran a otros clientes que comparten la conexión de servidor, a menos que se use `server_reset_query_always`.

El protocolo de Postgres permite especificar ajustes de parámetros, tanto directamente como un parámetro en el paquete de arranque, como dentro del [paquete de arranque `options`][options-startup]. `track_extra_parameters` admite los parámetros especificados mediante ambos métodos. Sin embargo, no es posible incluir `options` mismo en `track_extra_parameters`, solo los parámetros contenidos en `options`.

Predeterminado: vacío

### ignore_startup_parameters {#ignore_startup_parameters}

De forma predeterminada, PgBouncer solo permite en los paquetes de arranque los parámetros de los que puede hacer seguimiento (ver `track_extra_parameters` para la lista). Todos los demás parámetros provocarán un error. Para permitir otros parámetros, pueden especificarse aquí, de modo que PgBouncer sepa que los gestiona el administrador y pueda ignorarlos.

Si necesitas especificar múltiples valores, usa una lista separada por comas (p. ej. `options,extra_float_digits`)

El protocolo de Postgres permite especificar ajustes de parámetros, tanto directamente como un parámetro en el paquete de arranque, como dentro del [paquete de arranque `options`][options-startup]. `ignore_startup_parameters` admite los parámetros especificados mediante ambos métodos. Es incluso posible incluir `options` mismo en `ignore_startup_parameters`, lo que hace que se ignoren los parámetros desconocidos contenidos dentro de `options`.

[options-startup]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-OPTIONS

Predeterminado: vacío

### peer_id {#peer_id}

El id de par usado para identificar este proceso de PgBouncer en un grupo de procesos de PgBouncer emparejados entre sí. El valor de `peer_id` debería ser único dentro de un grupo de procesos de PgBouncer emparejados. Cuando se establece en 0, el emparejamiento de PgBouncer está desactivado. Consulta la documentación de la sección `[peers]` para más información. El valor máximo que puede usarse para `peer_id` es 16383.

Predeterminado: 0

### disable_pqexec {#disable_pqexec}

Desactiva el protocolo Simple Query (PQexec). A diferencia del protocolo Extended Query, Simple Query permite múltiples consultas en un paquete, lo que posibilita ciertas clases de ataques de inyección SQL. Desactivarlo puede mejorar la seguridad. Obviamente, esto significa que solo los clientes que usen exclusivamente el protocolo Extended Query seguirán funcionando.

Predeterminado: 0

### application_name_add_host {#application_name_add_host}

Añade la dirección y el puerto del host del cliente al ajuste del nombre de aplicación establecido al inicio de la conexión. Esto ayuda a identificar el origen de las consultas defectuosas, etc. Esta lógica solo se aplica al inicio de una conexión. Si `application_name` se cambia más tarde con `SET`, PgBouncer no lo vuelve a cambiar.

Predeterminado: 0

### conffile {#conffile}

Muestra la ubicación del archivo de configuración actual. Cambiarlo hará que PgBouncer use otro archivo de configuración en el próximo `RELOAD` / `SIGHUP`.

Predeterminado: archivo de la línea de comandos

### service_name {#service_name}

Se usa en el registro del servicio de win32.

Predeterminado: `pgbouncer`

### job_name {#job_name}

Alias de `service_name`.

### stats_period {#stats_period}

Establece con qué frecuencia se actualizan los promedios mostrados en varios comandos `SHOW` y con qué frecuencia se escriben las estadísticas agregadas en el registro (pero ver `log_stats`). [segundos]

Predeterminado: 60

### max_prepared_statements {#max_prepared_statements}

Cuando se establece en un valor distinto de cero, PgBouncer rastrea en los modos de agrupación de transacciones y de instrucciones los comandos relacionados con instrucciones preparadas con nombre a nivel de protocolo enviados por el cliente. PgBouncer se asegura de que cualquier instrucción preparada por un cliente esté disponible en la conexión de servidor subyacente. Incluso cuando la instrucción fue preparada originalmente en otra conexión de servidor.

PgBouncer examina internamente todas las consultas que los clientes envían como instrucción preparada, y asigna a cada cadena de consulta única un nombre interno con el formato `PGBOUNCER_{unique_id}`. Si la misma cadena de consulta se prepara varias veces (posiblemente por clientes diferentes), esas consultas comparten el mismo nombre interno. PgBouncer solo prepara la instrucción en el servidor PostgreSQL real usando el nombre interno (por tanto, no el nombre proporcionado por el cliente). PgBouncer lleva un registro del nombre que el cliente dio a cada instrucción preparada. Luego reescribe cada comando que usa una instrucción preparada sustituyendo el nombre del lado del cliente por el nombre interno (p. ej., sustituyendo `my_prepared_statement` por `PGBOUNCER_123`) antes de reenviar ese comando al servidor. Más importante aún, si la instrucción preparada que el cliente quiere ejecutar aún no está preparada en el servidor (p. ej., porque ahora hay un servidor diferente asignado al cliente que cuando el cliente preparó la instrucción), entonces PgBouncer prepara la instrucción de forma transparente antes de ejecutarla.

Nota: Este rastreo y reescritura de los comandos de instrucciones preparadas no funciona para los comandos de instrucciones preparadas a nivel SQL, por lo que `PREPARE`, `EXECUTE` y `DEALLOCATE` se reenvían directamente a Postgres. La excepción a esta regla son los comandos `DEALLOCATE ALL` y `DISCARD ALL`; estos sí funcionan como se espera y limpiarán las instrucciones preparadas que PgBouncer rastreó para el cliente que envía este comando.

El valor real de este parámetro controla el número de instrucciones preparadas que se mantienen activas en una caché LRU en una única conexión de servidor. Cuando el parámetro se establece en 0, el soporte de instrucciones preparadas para la agrupación de transacciones y de instrucciones queda desactivado. Para obtener el mejor rendimiento, debes intentar asegurarte de que este parámetro sea mayor que la cantidad de instrucciones preparadas de uso común en tu aplicación. Ten en cuenta que cuanto mayor sea este valor, mayor será la huella de memoria de cada conexión de PgBouncer en tu servidor PostgreSQL, porque mantendrá más consultas preparadas en esas conexiones. También aumenta la huella de memoria del propio PgBouncer, porque ahora necesita llevar un registro de las cadenas de consulta.

El impacto en el uso de memoria de PgBouncer no es tan grande, eso sí:

- Cada consulta única se almacena una sola vez en una caché global de consultas.
- Cada conexión de cliente mantiene un búfer que usa para reescribir paquetes. Este es, como máximo, 4 veces el tamaño de `pkt_buf`. Este límite, sin embargo, muchas veces no se alcanza; solo ocurre cuando las consultas de tus instrucciones preparadas tienen entre 2 y 4 veces el tamaño de `pkt_buf`.

Así que si consideras lo siguiente como un escenario de ejemplo:

- Hay 1000 clientes activos
- Los clientes preparan 200 consultas únicas
- El tamaño promedio de una consulta es de 5kB
- El parámetro `pkt_buf` está establecido en el valor predeterminado de 4096 (4kB)

Entonces, PgBouncer necesita como máximo la siguiente cantidad de memoria para gestionar estas instrucciones preparadas:

```text
200 x 5kB + 1000 x 4 x 4kB = ~17MB of memory.
```

El rastreo de instrucciones preparadas no solo conlleva un coste de memoria, sino también un mayor uso de CPU, porque PgBouncer necesita inspeccionar y reescribir las consultas. Varias instancias de PgBouncer pueden escuchar en el mismo puerto para usar más de un núcleo para el procesamiento; consulta [la documentación de la opción `so_reuseport`](#so_reuseport) para más detalles.

Pero, por supuesto, las instrucciones preparadas también aportan beneficios de rendimiento. Igual que al conectarse directamente a PostgreSQL, al preparar una consulta que se ejecuta muchas veces se reduce la cantidad total de análisis y planificación que hay que hacer. La forma en que PgBouncer rastrea las instrucciones preparadas es especialmente beneficiosa para el rendimiento cuando múltiples clientes preparan las mismas consultas. Porque las conexiones de cliente reutilizan automáticamente una instrucción preparada en una conexión de servidor, aunque haya sido preparada por otro cliente. Como ejemplo, si tienes un `pool_size` de 20 y tienes 100 clientes que preparan todos exactamente la misma consulta, la consulta se prepara (y por tanto se analiza) solo 20 veces en el servidor PostgreSQL.

La reutilización de instrucciones preparadas tiene un inconveniente. Si los tipos de retorno o de argumento de una instrucción preparada cambian entre ejecuciones, PostgreSQL actualmente lanza un error como:

```text
ERROR:  cached plan must not change result type
```

Puedes evitar tales errores evitando que múltiples clientes usen exactamente la misma cadena de consulta en una instrucción preparada pero esperando tipos de argumento o de resultado diferentes. Una de las formas más comunes de toparse con este problema es durante una migración DDL en la que añades una columna nueva o cambias el tipo de una columna en una tabla existente. En esos casos puedes ejecutar `RECONNECT` en la consola de administración de PgBouncer después de hacer la migración para forzar una nueva preparación de la consulta y hacer desaparecer el error.

Predeterminado: 200

### scram_iterations {#scram_iterations}

El número de iteraciones de cálculo que se realizarán al calcular el hash de una contraseña usando SCRAM-SHA-256. Un número mayor de iteraciones proporciona protección adicional contra ataques de fuerza bruta sobre las contraseñas almacenadas, pero hace la autenticación más lenta.

Predeterminado: 4096

--------

## Parámetros de autenticación {#authentication-settings}

PgBouncer gestiona su propia autenticación de clientes y tiene su propia base de datos de usuarios. Estos parámetros la controlan.

### auth_type {#auth_type}

Cómo autenticar a los usuarios.

- **`cert`**: El cliente debe conectarse mediante una conexión TLS con un certificado de cliente válido. El nombre de usuario se toma entonces del campo CommonName del certificado.
- **`md5`**: Usa comprobación de contraseña basada en MD5. Este es el método de autenticación predeterminado. `auth_file` puede contener tanto contraseñas con hash MD5 como en texto plano. Si `md5` está configurado y un usuario tiene un secreto SCRAM, entonces se usa automáticamente la autenticación SCRAM en su lugar.
- **`scram-sha-256`**: Usa comprobación de contraseña con SCRAM-SHA-256. `auth_file` debe contener secretos SCRAM o contraseñas en texto plano.
- **`plain`**: La contraseña en texto claro se envía por el canal. Obsoleto.
- **`trust`**: No se realiza ninguna autenticación. El nombre de usuario debe seguir existiendo en `auth_file`.
- **`any`**: Como el método `trust`, pero el nombre de usuario dado se ignora. Requiere que todas las bases de datos estén configuradas para iniciar sesión como un usuario específico. Además, la base de datos de la consola permite que cualquier usuario inicie sesión como usuario de estadísticas; los usuarios listados en `admin_users` reciben privilegios de administrador.
- **`hba`**: El tipo de autenticación real se carga desde `auth_hba_file`. Esto permite diferentes métodos de autenticación para diferentes rutas de acceso; por ejemplo: las conexiones mediante socket Unix usan el método de autenticación `peer`, las conexiones por TCP deben usar TLS.
- **`ldap`**: Los usuarios se autentican contra un servidor LDAP, igual que en PostgreSQL (ver <https://www.postgresql.org/docs/current/auth-ldap.html> para más detalles). Las opciones de conexión LDAP se configuran mediante el parámetro `auth_ldap_options`, o alternativamente en el `auth_hba_file`.
- **`pam`**: Se usa PAM para autenticar a los usuarios; `auth_file` se ignora. Este método no es compatible con bases de datos que usan la opción `auth_user`. El nombre del servicio reportado a PAM es "pgbouncer". `pam` no es compatible con el archivo de configuración HBA.

### auth_hba_file {#auth_hba_file}

Archivo de configuración HBA a usar cuando `auth_type` es `hba`. Consulta la sección [Formato del archivo HBA](#hba-file-format) más abajo para conocer los detalles.

Predeterminado: sin establecer

### auth_ident_file {#auth_ident_file}

Archivo de mapeo de identidades a usar cuando `auth_type` es `hba` y se va a definir un mapeo de usuarios. Consulta la sección [Formato del archivo de mapeo de identidades](#ident-map-file-format) más abajo para conocer los detalles.

Predeterminado: sin establecer

### auth_file {#auth_file}

El nombre del archivo del que cargar nombres de usuario y contraseñas. Consulta la sección [Formato del archivo de autenticación](#authentication-file-format) más abajo para conocer los detalles.

La mayoría de los tipos de autenticación (ver arriba) requieren que se establezca `auth_file` o `auth_user`; de lo contrario no habría usuarios definidos.

Predeterminado: sin establecer

### auth_user {#auth_user}

Si `auth_user` está establecido, cualquier usuario no especificado en `auth_file` se consultará mediante la consulta `auth_query` sobre `pg_authid` en la base de datos, usando `auth_user`. La contraseña de `auth_user` se tomará de `auth_file`. (Si `auth_user` no requiere contraseña, entonces no hace falta que esté definido en `auth_file`.)

El acceso directo a `pg_authid` requiere derechos de administrador. Es preferible usar un usuario que no sea superusuario y que llame a una función SECURITY DEFINER en su lugar.

Predeterminado: sin establecer

### auth_query {#auth_query}

Consulta para cargar la contraseña del usuario desde la base de datos.

El acceso directo a `pg_authid` requiere derechos de administrador. Es preferible usar un usuario que no sea superusuario y que llame a una función SECURITY DEFINER en su lugar.

Ten en cuenta que la consulta se ejecuta dentro de la base de datos de destino. Por tanto, si se usa una función, debe estar instalada en cada base de datos.

La consulta debe devolver dos columnas, el nombre de usuario y la contraseña (con el cifrado/hash apropiado). Para reportar que el usuario no existe, devuelve cero filas o una fila con un valor nulo para el usuario. (La consulta predeterminada de abajo no devuelve filas para un usuario inexistente. La variante con el valor nulo es útil cuando la consulta llama a una función que devuelve un registro, como en el ejemplo mostrado en [Ejemplos](#examples) más abajo.) Un valor nulo en la columna de la contraseña significa que el usuario existe pero no hay contraseña disponible para él, de modo que no se aceptará ninguna contraseña que ofrezca el cliente.

Predeterminado: `SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END FROM pg_authid WHERE rolname=$1 AND rolcanlogin`

### auth_dbname {#auth_dbname}

Nombre de la base de datos en la sección `[databases]` que se usará con fines de autenticación. Esta opción puede ser global o sobrescribirse en la cadena de conexión si se especifica este parámetro.

### auth_ldap_options {#auth_ldap_options}

Opciones de conexión LDAP a usar si `auth_type` es `ldap`. (No se usan si la autenticación está configurada vía `auth_hba_file`.) Ejemplo:

```ini
auth_ldap_options = ldapurl="ldap://127.0.0.1:12345/dc=example,dc=net?uid?sub"
```

--------

## Parámetros de registro {#log-settings}

### syslog {#syslog}

Activa o desactiva syslog. En Windows, se usa el registro de eventos en su lugar.

Predeterminado: 0

### syslog_ident {#syslog_ident}

Con qué nombre enviar los registros a syslog.

Predeterminado: `pgbouncer` (nombre del programa)

### syslog_facility {#syslog_facility}

Con qué facility enviar los registros a syslog. Posibilidades: `auth`, `authpriv`, `daemon`, `user`, `local0-7`.

Predeterminado: `daemon`

### log_connections {#log_connections}

Registra los inicios de sesión correctos.

Predeterminado: 1

### log_disconnections {#log_disconnections}

Registra las desconexiones con sus motivos.

Predeterminado: 1

### log_pooler_errors {#log_pooler_errors}

Registra los mensajes de error que el pooler envía a los clientes.

Predeterminado: 1

### log_stats {#log_stats}

Escribe las estadísticas agregadas en el registro cada `stats_period`. Esto puede desactivarse si se usan herramientas externas de monitorización para obtener los mismos datos de los comandos `SHOW`.

Predeterminado: 1

### verbose {#verbose}

Aumenta el nivel de detalle. Refleja la opción `-v` de la línea de comandos. Por ejemplo, usar `-v -v` en la línea de comandos equivale a `verbose=2`. 3 es el nivel de detalle más alto actualmente soportado.

Predeterminado: 0

--------

## Control de acceso a la consola {#console-access-control}

### admin_users {#admin_users}

Lista separada por comas de usuarios de base de datos a los que se permite conectarse y ejecutar todos los comandos en la consola. Con `auth_type=any`, esta lista sigue determinando quién recibe privilegios de administrador; otros usuarios pueden iniciar sesión como usuarios de estadísticas. Ver las [comprobaciones de acceso a la consola de la versión 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/admin.c#L1572-L1609).

Predeterminado: vacío

### stats_users {#stats_users}

Lista separada por comas de usuarios de base de datos a los que se permite conectarse y ejecutar consultas de solo lectura en la consola. Es decir, todos los comandos `SHOW`.

Predeterminado: vacío

--------

## Comprobaciones de estado de las conexiones, tiempos de espera {#connection-sanity-checks-timeouts}

### server_reset_query {#server_reset_query}

Consulta enviada al servidor al liberar la conexión, antes de hacerla disponible para otros clientes. En ese momento no hay ninguna transacción en curso, por lo que el valor no debe incluir `ABORT` ni `ROLLBACK`.

La consulta se supone que limpia cualquier cambio hecho a la sesión de la base de datos para que el siguiente cliente reciba la conexión en un estado bien definido. El valor predeterminado es `DISCARD ALL`, que lo limpia todo, pero eso deja al siguiente cliente sin estado pre-cacheado. Puede hacerse más ligero, p. ej. `DEALLOCATE ALL` para solo descartar las instrucciones preparadas, si la aplicación no se rompe cuando se conserva algún estado.

Cuando se usa la agrupación de transacciones, no se usa `server_reset_query`, porque en ese modo los clientes no deben usar ninguna característica basada en sesión, dado que cada transacción acaba en una conexión diferente y por tanto obtiene un estado de sesión diferente.

Predeterminado: `DISCARD ALL`

### server_reset_query_always {#server_reset_query_always}

Si `server_reset_query` debe ejecutarse en todos los modos de agrupación. Cuando este parámetro está desactivado (predeterminado), `server_reset_query` se ejecutará solo en pools que estén en modo de agrupación de sesiones. Las conexiones en modo de agrupación de transacciones no deberían necesitar ninguna consulta de restablecimiento.

Este parámetro es para sortear configuraciones rotas que ejecutan aplicaciones que usan características de sesión sobre un PgBouncer con agrupación de transacciones. Convierte el fallo no determinista en fallo determinista: los clientes siempre pierden su estado después de cada transacción.

Predeterminado: 0

### server_check_delay {#server_check_delay}

Cuánto tiempo mantener disponibles las conexiones liberadas para su reutilización inmediata, sin ejecutar `server_check_query` sobre ellas. Si es 0, la comprobación se ejecuta siempre.

Predeterminado: 30.0

### server_check_query {#server_check_query}

Consulta simple que no hace nada, para comprobar si la conexión de servidor está viva.

Si es una cadena vacía, la comprobación de estado se desactiva.

Si es `<empty>`, se envía una consulta vacía como comprobación de estado.

Predeterminado: `<empty>`

### server_fast_close {#server_fast_close}

Desconecta un servidor en modo de agrupación de sesiones inmediatamente o al final de la transacción actual si está en modo "close_needed" (establecido por `RECONNECT`, un `RELOAD` que cambia los ajustes de conexión, o un cambio de DNS), en lugar de esperar al fin de la sesión. En modo de agrupación de instrucciones o transacciones, esto no tiene efecto, ya que ese es el comportamiento predeterminado allí.

Si debido a este parámetro una conexión de servidor se cierra antes del final de la sesión del cliente, la conexión del cliente también se cierra. Esto asegura que el cliente note que la sesión ha sido interrumpida.

Este parámetro hace que los cambios de configuración de conexiones surtan efecto antes si se usan la agrupación de sesiones y sesiones de larga duración. El inconveniente es que las sesiones de cliente pueden verse interrumpidas por un cambio de configuración, por lo que las aplicaciones cliente necesitarán lógica para reconectarse y restablecer el estado de la sesión. Pero ten en cuenta que no se perderá ninguna transacción, porque las transacciones en ejecución no se interrumpen, solo las sesiones inactivas.

Predeterminado: 0

### server_lifetime {#server_lifetime}

El pooler cerrará una conexión de servidor no usada (no vinculada actualmente a ninguna conexión de cliente) que haya estado conectada durante más tiempo que este. Establecerlo en 0 significa que la conexión se usará solo una vez y luego se cerrará. [segundos]

Esto también puede establecerse por base de datos en la sección `[databases]`.

Predeterminado: 3600.0

### server_idle_timeout {#server_idle_timeout}

Si una conexión de servidor ha estado inactiva más que este número de segundos, se cerrará. Si es 0, este tiempo de espera está desactivado. [segundos]

Predeterminado: 600.0

### server_connect_timeout {#server_connect_timeout}

Si la conexión y el inicio de sesión no terminan en este tiempo, la conexión se cerrará. [segundos]

Predeterminado: 15.0

### server_login_retry {#server_login_retry}

Si el inicio de sesión en el servidor falló, por un fallo de conexión o de autenticación, el pooler espera este tiempo antes de reintentar la conexión. Durante el intervalo de espera, los nuevos clientes que intenten conectarse al servidor que falla recibirán un error inmediatamente, sin otro intento de conexión. [segundos]

El propósito de este comportamiento es que los clientes no se pongan en cola innecesariamente esperando a que una conexión de servidor esté disponible si el servidor no funciona. Sin embargo, también significa que si un servidor falla momentáneamente, por ejemplo durante un reinicio o si la configuración era errónea, tomará al menos este tiempo hasta que el pooler considere conectarse a él de nuevo. Los eventos planificados, como los reinicios, deberían gestionarse normalmente con el comando `PAUSE` para evitar esto.

Predeterminado: 15.0

### client_login_timeout {#client_login_timeout}

Si un cliente se conecta pero no consigue iniciar sesión en este tiempo, será desconectado. [segundos]

Predeterminado: 60.0

### autodb_idle_timeout {#autodb_idle_timeout}

Si los pools de bases de datos creados automáticamente (vía `*`) no se han usado durante este número de segundos, se liberan. El aspecto negativo de ello es que sus estadísticas también se olvidan. [segundos]

Predeterminado: 3600.0

### pool_idle_timeout {#pool_idle_timeout}

Si un pool (un par específico base de datos/usuario) no ha tenido conexiones de cliente ni conexiones de servidor durante este número de segundos, se libera. Esto es similar a `autodb_idle_timeout`, pero libera pools individuales en lugar de bases de datos automáticas completas. Ten en cuenta que, a diferencia de `server_idle_timeout` (que cierra las conexiones de servidor inactivas pero conserva el pool), esto libera el pool completo, y solo cuando está completamente vacío.

Como con `autodb_idle_timeout`, el aspecto negativo es que las estadísticas de un pool liberado se olvidan. Como los totales por base de datos en `SHOW STATS` son la suma de los pools existentes actualmente, liberar un pool hace que esos totales disminuyan, lo que los sistemas de monitorización pueden malinterpretar como un reinicio de contador. Por esa razón esto está desactivado de forma predeterminada. 0 desactiva. [segundos]

Predeterminado: 0 (desactivado)

### dns_max_ttl {#dns_max_ttl}

Cuánto tiempo pueden almacenarse en caché las búsquedas de DNS. El TTL real del DNS se ignora. [segundos]

Predeterminado: 15.0

### dns_nxdomain_ttl {#dns_nxdomain_ttl}

Cuánto tiempo pueden almacenarse en caché los errores de DNS y las búsquedas DNS de NXDOMAIN. [segundos]

Predeterminado: 15.0

### dns_zone_check_period {#dns_zone_check_period}

Periodo para comprobar si el número de serie de una zona ha cambiado.

PgBouncer puede recolectar zonas DNS a partir de los nombres de host (todo lo que sigue al primer punto) y luego comprobar periódicamente si cambia el número de serie de la zona. Si nota cambios, todos los nombres de host bajo esa zona se vuelven a resolver. Si la IP de algún host cambia, sus conexiones quedan invalidadas.

Funciona solo con el backend c-ares (opción de `configure` `--with-cares`).

Predeterminado: 0.0 (desactivado)

### resolv_conf {#resolv_conf}

La ubicación de un archivo `resolv.conf` personalizado. Esto permite especificar servidores DNS personalizados y quizás otras opciones de resolución de nombres, independientemente de la configuración global del sistema operativo.

Requiere el backend evdns (>= 2.0.3) o c-ares (>= 1.15.0).

El análisis del archivo lo hace la biblioteca del backend de DNS, no PgBouncer, así que consulta la documentación de la biblioteca para conocer los detalles de la sintaxis y las directivas permitidas.

Predeterminado: vacío (usar los valores predeterminados del sistema operativo)

### query_wait_notify {#query_wait_notify}

Tiempo durante el que un cliente estará en cola antes de que PgBouncer envíe un mensaje de notificación de que está siendo puesto en cola. [segundos]

Un valor de 0 desactiva este mensaje de notificación.

Predeterminado: 5

### login_notify_message {#login_notify_message}

Mensaje de notificación de bienvenida que se envía al cliente después de un inicio de sesión correcto. Puede usarse para asegurar que los clientes entienden que se están conectando a pgbouncer en lugar de directamente a postgres.

Predeterminado: vacío (no se envía mensaje de bienvenida)

--------

## Parámetros TLS {#tls-settings}

Si se cambia el contenido de cualquiera de los archivos de certificado o de clave sin cambiar el nombre de archivo del ajuste en la configuración, el nuevo contenido de los archivos se usará para las conexiones nuevas después de un RELOAD. Las conexiones existentes, sin embargo, no se cerrarán. Si por motivos de seguridad es necesario que todas las conexiones empiecen a usar los nuevos archivos cuanto antes, se recomienda ejecutar RECONNECT después del RELOAD.

Cambiar cualquier parámetro TLS provocará un RECONNECT automático por motivos de seguridad.

### client_tls_sslmode {#client_tls_sslmode}

Modo TLS a usar para las conexiones de los clientes. Las conexiones TLS están desactivadas de forma predeterminada. Cuando se activan, `client_tls_key_file` y `client_tls_cert_file` también deben configurarse para establecer la clave y el certificado que PgBouncer usa para aceptar conexiones de cliente. El formato de archivo de certificado más común utilizable por PgBouncer es PEM.

- **`disable`**: TCP simple. Si el cliente solicita TLS, se ignora. Predeterminado.
- **`allow`**: Si el cliente solicita TLS, se usa. Si no, se usa TCP simple. Si el cliente presenta un certificado de cliente, no se valida.
- **`prefer`**: Igual que `allow`.
- **`require`**: El cliente debe usar TLS. Si no, se rechaza la conexión del cliente. Si el cliente presenta un certificado de cliente, no se valida.
- **`verify-ca`**: El cliente debe usar TLS con un certificado de cliente válido.
- **`verify-full`**: Igual que `verify-ca`.

### client_tls_key_file {#client_tls_key_file}

Clave privada para que PgBouncer acepte conexiones de cliente.

Predeterminado: sin establecer

### client_tls_cert_file {#client_tls_cert_file}

Certificado para la clave privada. Los clientes pueden validarlo.

Predeterminado: sin establecer

### client_tls_ca_file {#client_tls_ca_file}

Archivo de certificado raíz para validar los certificados de cliente.

Predeterminado: sin establecer

### client_tls_protocols {#client_tls_protocols}

Qué versiones del protocolo TLS están permitidas. Valores permitidos: `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Atajos: `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3).

Predeterminado: `secure`

### client_tls_ciphers {#client_tls_ciphers}

Cifrados TLS permitidos, en sintaxis OpenSSL. Atajos:

- `default`/`secure`/`fast`/`normal` (todos estos usan los valores predeterminados de OpenSSL de todo el sistema)
- `all` (activa todos los cifrados, no recomendado)

Solo se ven afectadas las conexiones que usan la versión 1.2 de TLS o inferior. Para la versión 1.3 ver `client_tls13_ciphers` más abajo.

Predeterminado: `default`

### client_tls13_ciphers {#client_tls13_ciphers}

Cifrados TLS v1.3 permitidos. Cuando está vacío, se usará el valor de `client_tls_ciphers`. Valores permitidos:

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Solo se ven afectadas las conexiones que usan la versión 1.3 de TLS o superior. Para la versión 1.2 e inferior ver `client_tls_ciphers`.

Predeterminado: `<empty>`

### client_tls_ecdhcurve {#client_tls_ecdhcurve}

Nombre de la curva elíptica a usar para los intercambios de claves ECDH.

Valores permitidos: `none` (DH está desactivado), `auto` (ECDH de 256 bits), nombre de curva

Predeterminado: `auto`

### client_tls_dheparams {#client_tls_dheparams}

Tipo de intercambio de claves DHE.

Valores permitidos: `none` (DH está desactivado), `auto` (DH de 2048 bits), `legacy` (DH de 1024 bits)

Predeterminado: `auto`

### server_tls_sslmode {#server_tls_sslmode}

Modo TLS a usar para las conexiones a servidores PostgreSQL. El modo predeterminado es `prefer`.

- **`disable`**: TCP simple. Ni siquiera se solicita TLS al servidor.
- **`allow`**: Se comporta como `prefer`: primero solicita TLS y recurre al TCP simple si el servidor rechaza TLS. El certificado del servidor no se valida.
- **`prefer`**: La conexión TLS siempre se solicita primero a PostgreSQL. Si se rechaza, la conexión se establecerá mediante TCP simple. El certificado del servidor no se valida. Predeterminado.
- **`require`**: La conexión debe ir sobre TLS. Si el servidor la rechaza, no se intenta TCP simple. El certificado del servidor no se valida.
- **`verify-ca`**: La conexión debe ir sobre TLS y el certificado del servidor debe ser válido según `server_tls_ca_file`. El nombre de host del servidor no se comprueba contra el certificado.
- **`verify-full`**: La conexión debe ir sobre TLS y el certificado del servidor debe ser válido según `server_tls_ca_file`. El nombre de host del servidor debe coincidir con la información del certificado.

### server_tls_ca_file {#server_tls_ca_file}

Archivo de certificado raíz para validar los certificados de los servidores PostgreSQL.

Predeterminado: sin establecer

### server_tls_key_file {#server_tls_key_file}

Clave privada para que PgBouncer se autentique ante el servidor PostgreSQL.

Predeterminado: sin establecer

### server_tls_cert_file {#server_tls_cert_file}

Certificado para la clave privada. El servidor PostgreSQL puede validarlo.

Predeterminado: sin establecer

### server_tls_protocols {#server_tls_protocols}

Qué versiones del protocolo TLS están permitidas. Valores permitidos: `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Atajos: `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3), `legacy` (todas).

Predeterminado: `secure`

### server_tls_ciphers {#server_tls_ciphers}

Cifrados TLS permitidos, en sintaxis OpenSSL. Atajos:

- `default`/`secure`/`fast`/`normal` (todos estos usan los valores predeterminados de OpenSSL de todo el sistema)
- `all` (activa todos los cifrados, no recomendado)

Solo se ven afectadas las conexiones que usan la versión 1.2 de TLS o inferior. Para la versión 1.3 ver `server_tls13_ciphers` más abajo.

Predeterminado: `default`

### server_tls13_ciphers {#server_tls13_ciphers}

Cifrados TLS v1.3 permitidos. Cuando está vacío, se usará el valor de `server_tls_ciphers`. Valores permitidos:

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Solo se ven afectadas las conexiones que usan la versión 1.3 de TLS o superior. Para la versión 1.2 e inferior ver `server_tls_ciphers`.

Predeterminado: `<empty>`

--------

## Tiempos de espera peligrosos {#dangerous-timeouts}

Establecer los siguientes tiempos de espera puede provocar errores inesperados.

### query_timeout {#query_timeout}

Las consultas que se ejecutan más tiempo que eso se cancelan. Esto debería usarse solo con un `statement_timeout` del lado del servidor ligeramente menor, para aplicar solo a problemas de red. [segundos]

Predeterminado: 0.0 (desactivado)

### query_wait_timeout {#query_wait_timeout}

Tiempo máximo que se permite a las consultas esperar su ejecución. Si la consulta no se asigna a un servidor durante ese tiempo, el cliente es desconectado. 0 desactiva. Si esto está desactivado, los clientes se pondrán en cola indefinidamente. [segundos]

Este parámetro se usa para evitar que los servidores que no responden acaparen conexiones. También ayuda cuando el servidor está caído o rechaza conexiones por cualquier motivo.

Este parámetro también puede configurarse por base de datos y por usuario. La precedencia es usuario, luego base de datos, luego global. Un 0 explícito en el nivel seleccionado desactiva este tiempo de espera. Ver el [código de selección de tiempo de espera de la versión 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/janitor.c#L328-L336).

Predeterminado: 120.0

### cancel_wait_timeout {#cancel_wait_timeout}

Tiempo máximo que se permite a las peticiones de cancelación esperar su ejecución. Si la petición de cancelación no se asigna a un servidor durante ese tiempo, el cliente es desconectado. 0 desactiva. Si esto está desactivado, las peticiones de cancelación se pondrán en cola indefinidamente. [segundos]

Este parámetro se usa para evitar que un cliente se bloquee cuando no se puede reenviar una cancelación debido a que el servidor está caído.

Predeterminado: 10.0

### client_idle_timeout {#client_idle_timeout}

Las conexiones de cliente inactivas durante más de este número de segundos se cierran. Esto debería ser mayor que los ajustes de tiempo de vida de las conexiones del lado del cliente, y usarse solo para problemas de red. [segundos]

Predeterminado: 0.0 (desactivado)

### idle_transaction_timeout {#idle_transaction_timeout}

Si un cliente ha estado en estado "idle in transaction" durante más tiempo, será desconectado. [segundos]

Predeterminado: 0.0 (desactivado)

### transaction_timeout {#transaction_timeout}

Si un cliente ha estado en estado "in transaction" durante más tiempo, será desconectado. [segundos]

Predeterminado: 0.0 (desactivado)

--------

## Parámetros de red de bajo nivel {#low-level-network-settings}

### pkt_buf {#pkt_buf}

Tamaño del búfer interno para los paquetes. Afecta al tamaño de los paquetes TCP enviados y al uso general de memoria. Los paquetes reales de libpq pueden ser mayores que esto, así que no hay necesidad de establecerlo grande.

Predeterminado: 4096

### max_packet_size {#max_packet_size}

Tamaño máximo de los paquetes de PostgreSQL que PgBouncer deja pasar. Un paquete es una consulta o una fila del conjunto de resultados. El conjunto de resultados completo puede ser mayor.

Predeterminado: 2147483647

### listen_backlog {#listen_backlog}

Argumento backlog para `listen(2)`. Determina cuántos intentos de conexión nuevos sin responder se mantienen en la cola. Cuando la cola está llena, las nuevas conexiones adicionales se descartan.

Predeterminado: 128

### sbuf_loopcnt {#sbuf_loopcnt}

Cuántas veces procesar datos en una conexión antes de continuar. Sin este límite, una conexión con un conjunto de resultados grande puede detener PgBouncer durante mucho tiempo. Un bucle procesa una cantidad de datos equivalente a un `pkt_buf`. 0 significa sin límite.

Predeterminado: 5

### so_reuseport {#so_reuseport}

Especifica si establecer la opción de socket `SO_REUSEPORT` en los sockets de escucha TCP. En algunos sistemas operativos, esto permite ejecutar múltiples instancias de PgBouncer en el mismo host escuchando en el mismo puerto y haciendo que el kernel distribuya las conexiones automáticamente. Esta opción es una forma de lograr que PgBouncer use más núcleos de CPU. (PgBouncer es monohilo y usa un núcleo de CPU por instancia.)

El comportamiento en detalle depende del kernel del sistema operativo. A la fecha de redacción de este documento, este parámetro tiene el efecto deseado en (versiones suficientemente recientes de) Linux, DragonFlyBSD y FreeBSD. (En FreeBSD, aplica en su lugar la opción de socket `SO_REUSEPORT_LB`.) Algunos otros sistemas operativos son compatibles con la opción de socket, pero no tendrá el efecto deseado: permitirá que múltiples procesos se enlacen al mismo puerto, pero solo uno de ellos recibirá las conexiones. Consulta la documentación de `setsockopt()` de tu sistema operativo para más detalles.

En sistemas que no son compatibles en absoluto con la opción de socket, activar este parámetro provocará un error.

Cada instancia de PgBouncer en el mismo host necesita ajustes diferentes al menos para `unix_socket_dir` y `pidfile`, así como para `logfile` si se usa. Ten en cuenta también que si usas esta opción, ya no podrás conectarte a una instancia específica de PgBouncer vía TCP/IP, lo que podría tener implicaciones para la monitorización y la recolección de métricas.

Para asegurarte de que las cancelaciones de consultas sigan funcionando, deberías configurar el emparejamiento de PgBouncer entre los diferentes procesos de PgBouncer. Para más detalles, consulta la documentación de la opción de configuración `peer_id` y de la sección de configuración `peers`. También hay un ejemplo que usa el emparejamiento y `so_reuseport` en la sección de ejemplos de esta documentación.

Predeterminado: 0

### tcp_defer_accept {#tcp_defer_accept}

Establece la opción de socket `TCP_DEFER_ACCEPT`; ver `man 7 tcp` para más detalles. (Es una opción booleana: 1 significa activada. El valor real establecido si se activa está actualmente fijado en el código a 45 segundos.)

Actualmente esto solo es compatible con Linux.

Predeterminado: 1 en Linux, de lo contrario 0

### tcp_socket_buffer {#tcp_socket_buffer}

Predeterminado: sin establecer

### tcp_keepalive {#tcp_keepalive}

Activa el keepalive básico con los valores predeterminados del sistema operativo.

En Linux, los valores predeterminados del sistema son `tcp_keepidle=7200`, `tcp_keepintvl=75`, `tcp_keepcnt=9`. Probablemente sean similares en otros sistemas operativos.

Predeterminado: 1

### tcp_keepcnt {#tcp_keepcnt}

Predeterminado: sin establecer

### tcp_keepidle {#tcp_keepidle}

Predeterminado: sin establecer

### tcp_keepintvl {#tcp_keepintvl}

Predeterminado: sin establecer

### tcp_user_timeout {#tcp_user_timeout}

Establece la opción de socket `TCP_USER_TIMEOUT`. Esto especifica la cantidad máxima de tiempo en milisegundos que los datos transmitidos pueden permanecer sin reconocer antes de que la conexión TCP se cierre por la fuerza. Si se establece en 0, se usa el valor predeterminado del sistema operativo.

Actualmente esto solo es compatible con Linux.

Predeterminado: 0

--------

## Sección [databases] {#section-databases}

La sección `[databases]` define los nombres de las bases de datos a las que los clientes de PgBouncer pueden conectarse y especifica hacia dónde se enrutarán esas conexiones. La sección contiene líneas clave=valor como

```ini
dbname = connection string
```

donde la clave se tomará como un nombre de base de datos y el valor como una cadena de conexión, compuesta de pares clave=valor de parámetros de conexión, descritos más abajo (similar a libpq, pero no se usa libpq como tal y el conjunto de características disponibles es diferente). Ejemplo:

```ini
foodb = host=host1.example.com port=5432
bardb = host=localhost dbname=bazdb
```

El nombre de la base de datos puede contener los caracteres `_0-9A-Za-z` sin entrecomillarlo. Los nombres que contienen otros caracteres deben entrecomillarse con el entrecomillado estándar de identificadores SQL: comillas dobles, usando `""` para una única instancia de una comilla doble.

El nombre de base de datos `pgbouncer` está reservado para la consola de administración y no puede usarse como clave aquí.

`*` actúa como base de datos de reserva (fallback): si el nombre exacto no existe, su valor se toma como cadena de conexión para la base de datos solicitada. Por ejemplo, si hay una entrada (y no hay otras entradas que la sobrescriban)

```ini
* = host=foo
```

entonces una conexión a PgBouncer que especifique una base de datos `bar` se comportará efectivamente como si una entrada

```ini
bar = host=foo dbname=bar
```

existiera (aprovechando que el valor predeterminado de `dbname` es el nombre de la base de datos del lado del cliente; ver más abajo).

Tales entradas de base de datos creadas automáticamente se limpian si permanecen inactivas más tiempo que el especificado por el parámetro `autodb_idle_timeout`.

### dbname {#dbname}

Nombre de la base de datos de destino.

Predeterminado: el mismo que el nombre de la base de datos del lado del cliente

### host {#host}

Nombre de host o dirección IP a la que conectarse. Los nombres de host se resuelven en el momento de la conexión; el resultado se almacena en caché según el parámetro `dns_max_ttl`. Cuando la resolución de un nombre de host cambia, las conexiones de servidor existentes se cierran automáticamente al liberarse (de acuerdo con el modo de agrupación), y las nuevas conexiones de servidor usan de inmediato la nueva resolución. Si DNS devuelve varios resultados, se usan de forma round-robin.

Si el valor comienza con `/`, se usa un socket Unix en el espacio de nombres del sistema de archivos. Si el valor comienza con `@`, se usa un socket Unix en el espacio de nombres abstracto.

Puede especificarse una lista de nombres de host o direcciones separada por comas. En ese caso, las conexiones se hacen de forma round-robin. (Si una lista de hosts contiene nombres de host que a su vez se resuelven vía DNS a múltiples direcciones, los sistemas round-robin operan de forma independiente. Esto es una dependencia de la implementación que está sujeta a cambios.) Ten en cuenta que en una lista, todos los hosts deben estar disponibles en todo momento: no existen mecanismos para saltarse los hosts inaccesibles ni para seleccionar solo los hosts disponibles de una lista o similar. (Esto es diferente de lo que significa una lista de hosts en libpq.) Ten en cuenta también que esto solo afecta a cómo se eligen los destinos de las conexiones nuevas. Ver también el ajuste `server_round_robin` para saber cómo se asignan los clientes a las conexiones de servidor ya establecidas.

Ejemplos:

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/postgresql
host=192.168.0.1,192.168.0.2,192.168.0.3
```

Predeterminado: sin establecer, lo que significa usar un socket Unix

### port {#port}

Predeterminado: 5432

### user {#user-1}

Si se establece `user=`, todas las conexiones a la base de datos de destino se harán con el usuario especificado, lo que significa que habrá un solo pool para esta base de datos.

De lo contrario, PgBouncer inicia sesión en la base de datos de destino con el nombre de usuario del cliente, lo que significa que habrá un pool por usuario.

### password {#password}

Si no se especifica aquí ninguna contraseña, se usará la contraseña del `auth_file` para el usuario especificado arriba. Las formas dinámicas de descubrimiento de contraseñas como `auth_query` no son compatibles actualmente.

### auth_user {#auth_user-1}

Sobrescribe el ajuste global `auth_user`, si se especifica.

### auth_query {#auth_query-1}

Sobrescribe el ajuste global `auth_query`, si se especifica. La instrucción SQL completa debe ir entre comillas simples.

### auth_dbname {#auth_dbname-1}

Sobrescribe el ajuste global `auth_dbname`, si se especifica.

### pool_size {#pool_size}

Establece el tamaño máximo de los pools para esta base de datos. Si no se establece, se usa `default_pool_size`.

### min_pool_size {#min_pool_size-1}

Establece el tamaño mínimo del pool para esta base de datos. Si no se establece, se usa el `min_pool_size` global.

Solo se aplica si al menos una de las siguientes condiciones es cierta:

* esta entrada de la sección `[databases]` tiene un valor establecido para la clave `user` (también conocido como usuario forzado)
* hay al menos un cliente conectado al pool

### reserve_pool_size {#reserve_pool_size-1}

Establece conexiones adicionales para esta base de datos. Si no se establece, se usa el `reserve_pool_size` global. Por razones de compatibilidad con versiones anteriores, `reserve_pool` es un alias de esta opción.

### connect_query {#connect_query}

Consulta que se ejecutará después de establecer una conexión, pero antes de permitir que cualquier cliente use la conexión. Si la consulta provoca errores, se registran pero por lo demás se ignoran.

### pool_mode {#pool_mode-1}

Establece el modo de agrupación específico de esta base de datos. Si no se establece, se usa el `pool_mode` predeterminado.

### query_wait_timeout {#query_wait_timeout-1}

Tiempo máximo que se permite a las consultas esperar su ejecución. 0 desactiva. Omite este ajuste para heredar el valor predeterminado aplicable. [segundos]

Ver la descripción del ajuste global `query_wait_timeout` para más detalles.

Un `query_wait_timeout` a nivel de usuario sobrescribe este ajuste de base de datos. Si no se establece ninguno, se usa el `query_wait_timeout` global.

### load_balance_hosts {#load_balance_hosts}

Cuando se especifica una lista separada por comas en `host`, `load_balance_hosts` controla qué entrada se elige para una conexión nueva.

Nota: Este parámetro actualmente solo controla el comportamiento del balanceo de carga cuando se proporcionan múltiples hosts en la cadena de conexión, pero no cuando el registro DNS de un único host referencia múltiples direcciones IP. Esta es una característica faltante, por lo que en una versión futura este parámetro podría pasar a controlar ambos métodos de balanceo de carga.

- **`round-robin`**: Un nuevo intento de conexión elige la siguiente entrada de host de la lista.
- **`disable`**: Una conexión nueva sigue usando la misma entrada de host hasta que una conexión falla, tras lo cual se elige la siguiente entrada de host.

Se recomienda establecer `server_login_retry` por debajo del valor predeterminado para asegurar reintentos rápidos cuando hay múltiples hosts disponibles.

Predeterminado: `round-robin`

### max_db_connections {#max_db_connections-1}

Configura un máximo de conexiones de servidor para toda la base de datos (es decir, todos los pools de la base de datos no tendrán más que este número de conexiones de servidor).

### max_db_client_connections {#max_db_client_connections-1}

Configura un máximo de conexiones de cliente para toda la base de datos. Debería usarse junto con `max_client_conn` para limitar el número de conexiones que PgBouncer puede aceptar.

### server_lifetime {#server_lifetime-1}

Configura el `server_lifetime` por base de datos. Si no se establece, la base de datos recurrirá al valor configurado a nivel de instancia para `server_lifetime`.

### client_encoding {#client_encoding}

Solicita un `client_encoding` específico al servidor.

### datestyle {#datestyle}

Solicita un `datestyle` específico al servidor.

### timezone {#timezone}

Solicita un `timezone` específico al servidor.

--------

## Sección [users] {#section-users}

Esta sección contiene líneas clave=valor como

```ini
user1 = settings
```

donde la clave se tomará como un nombre de usuario y el valor como una lista de pares clave=valor de ajustes de configuración específicos de este usuario. Ejemplo:

```ini
user1 = pool_mode=session
```

Solo unos pocos ajustes están disponibles aquí.

Ten en cuenta que cuando `auth_file` está configurado, si un usuario está definido en esta sección pero no está listado en `auth_file`, PgBouncer intentará usar `auth_query` para encontrar una contraseña para ese usuario si `auth_user` está establecido. Si `auth_user` no está establecido, PgBouncer fingirá que el usuario existe y no devolverá mensajes de "no such user" al cliente, pero tampoco aceptará ninguna contraseña proporcionada.

### pool_size {#pool_size-1}

Establece el tamaño máximo de los pools para todas las conexiones de este usuario. Si no se establece, se usa la base de datos o `default_pool_size`.

### reserve_pool_size {#reserve_pool_size-2}

Establece el número de conexiones adicionales que permitir a un pool para este usuario. Si no se establece, se usa la configuración de la base de datos o el `reserve_pool_size` global.

### pool_mode {#pool_mode-2}

Establece el modo de agrupación que se usará para todas las conexiones de este usuario. Si no se establece, se usa la base de datos o el `pool_mode` predeterminado.

### max_user_connections {#max_user_connections-1}

Configura un máximo de conexiones de servidor para el usuario (es decir, todos los pools con este usuario no tendrán más que este número de conexiones de servidor).

### query_timeout {#query_timeout-1}

Establece el número máximo de segundos que una consulta de un usuario puede ejecutarse. Si se establece, este tiempo de espera sobrescribe el `query_timeout` a nivel de servidor descrito anteriormente.

### query_wait_timeout {#query_wait_timeout-2}

Tiempo máximo que se permite a las consultas esperar su ejecución. 0 desactiva. Omite este ajuste para heredar el valor predeterminado aplicable. [segundos]

Ver la descripción del ajuste global `query_wait_timeout` para más detalles.

Este ajuste sobrescribe tanto el `query_wait_timeout` de la base de datos como el global. Si no se establece, se usa el ajuste de la base de datos, recurriendo al valor global.

### idle_transaction_timeout {#idle_transaction_timeout-1}

Establece el número máximo de segundos que un usuario puede tener abierta una transacción inactiva. Si se establece, este tiempo de espera sobrescribe el `idle_transaction_timeout` a nivel de servidor descrito anteriormente.

### transaction_timeout {#transaction_timeout-1}

Establece el número máximo de segundos que un usuario puede tener abierta una transacción. Si se establece, este tiempo de espera sobrescribe el `transaction_timeout` a nivel de servidor descrito anteriormente.

### client_idle_timeout {#client_idle_timeout-1}

Establece la cantidad máxima de tiempo en segundos que se permite a un cliente estar conectado de forma inactiva a la instancia de PgBouncer. Si se establece, este tiempo de espera sobrescribe el `client_idle_timeout` a nivel de servidor descrito anteriormente.

Ten en cuenta que este es un tiempo de espera potencialmente peligroso.

### max_user_client_connections {#max_user_client_connections-1}

Configura un máximo de conexiones de cliente para el usuario. Es el equivalente por usuario del ajuste `max_client_conn`.

--------

## Sección [peers] {#section-peers}

La sección `[peers]` define los pares a los que PgBouncer puede reenviar peticiones de cancelación y hacia dónde se enrutarán esas peticiones de cancelación.

Los procesos de PgBouncer pueden emparejarse en un grupo definiendo un valor `peer_id` y una sección `[peers]` en las configuraciones de todos los procesos de PgBouncer. Estos procesos de PgBouncer pueden entonces reenviar las peticiones de cancelación al proceso que recibió la consulta que se está cancelando. Esto es necesario para que las cancelaciones funcionen cuando múltiples procesos de PgBouncer (posiblemente en servidores diferentes) están detrás del mismo balanceador de carga TCP. Las peticiones de cancelación se envían por conexiones TCP diferentes de la consulta que están cancelando, así que un balanceador de carga TCP podría enviar la conexión de la petición de cancelación a un proceso distinto del previsto. Al emparejarlos, estas peticiones de cancelación acaban llegando al proceso correcto. En esta [grabación de una charla de conferencia][cancel-problem-video] se ofrece una explicación más detallada.

[cancel-problem-video]: https://www.youtube.com/watch?v=X-nCHcZ6vQU

La sección contiene líneas clave=valor como

```ini
peer_id = connection string
```

Donde la clave se tomará como un `peer_id` y el valor como una cadena de conexión, compuesta de pares clave=valor de parámetros de conexión, descritos más abajo (similar a libpq, pero no se usa libpq como tal y el conjunto de características disponibles es diferente). Ejemplo:

```ini
1 = host=host1.example.com
2 = host=/tmp/pgbouncer-2  port=5555
```

Nota 1: Para que el emparejamiento funcione, el `peer_id` de cada proceso de PgBouncer del grupo debe ser único dentro del grupo emparejado. Y la sección `[peers]` debería contener entradas para cada uno de esos ids de par. En la sección de ejemplos de esta documentación se puede encontrar un ejemplo. Sí **se permite**, aunque no es necesario, que la sección `[peers]` contenga el `peer_id` del PgBouncer al que corresponde la configuración. Dicha entrada se ignorará, pero permitirlo simplifica la gestión de la configuración: exactamente la misma sección `[peers]` puede usarse en múltiples configuraciones.

Nota 2: El emparejamiento entre versiones es compatible siempre que todos los pares estén en el mismo lado del límite de la versión v1.21.0. En v1.21.0 se hicieron algunos cambios rupturistas en la forma en que codificamos los tokens de cancelación, que los hicieron incompatibles con los creados por versiones anteriores.

### host {#host-1}

Nombre de host o dirección IP a la que conectarse. Los nombres de host se resuelven en el momento de la conexión; el resultado se almacena en caché según el parámetro `dns_max_ttl`. Si DNS devuelve varios resultados, se usan de forma round-robin. Pero en general no se recomienda usar un nombre de host que se resuelva a múltiples IP, porque entonces la petición de cancelación podría aún reenviarse al nodo equivocado y tendría que reenviarse de nuevo (lo que solo se permite hasta tres veces).

Si el valor comienza con `/`, se usa un socket Unix en el espacio de nombres del sistema de archivos. Si el valor comienza con `@`, se usa un socket Unix en el espacio de nombres abstracto.

Ejemplos:

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/pgbouncer-1
```

### port {#port-1}

Predeterminado: 6432

### pool_size {#pool_size-2}

Establece el número máximo de peticiones de cancelación que pueden estar en vuelo hacia el par al mismo tiempo. Es bastante normal que las peticiones de cancelación lleguen en ráfagas, p. ej. cuando el servidor Postgres subyacente es lento o está caído. Por eso es importante que `pool_size` no sea tan bajo que no pueda manejar estas ráfagas.

Si no se establece, se usa `default_pool_size`.

--------

## Directiva de inclusión {#include-directive}

El archivo de configuración de PgBouncer puede contener directivas de inclusión, que especifican otro archivo de configuración que leer y procesar. Esto permite dividir el archivo de configuración en partes físicamente separadas. Las directivas de inclusión se ven así:

```ini
%include filename
```

Si el nombre de archivo no es una ruta absoluta, se toma como relativa al directorio de trabajo actual.

--------

## Formato del archivo de autenticación {#authentication-file-format}

Esta sección describe el formato del archivo especificado por el ajuste `auth_file`. Es un archivo de texto con el siguiente formato:

```text
"username1" "password" ...
"username2" "md5abcdef012342345" ...
"username2" "SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>"
```

Debe haber al menos 2 campos, rodeados de comillas dobles. El primer campo es el nombre de usuario y el segundo es una contraseña en texto plano, una contraseña con hash MD5 o un secreto SCRAM. PgBouncer ignora el resto de la línea. Las comillas dobles en el valor de un campo pueden escaparse escribiendo dos comillas dobles.

Formato de contraseña con hash MD5 de PostgreSQL:

```text
"md5" + md5(password + username)
```

Así, el usuario `admin` con la contraseña `1234` tendrá la contraseña con hash MD5 `md545f2603610af569b6155c45067268c6b`.

Formato del secreto SCRAM de PostgreSQL:

```text
SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>
```

Consulta la documentación de PostgreSQL y el RFC 5803 para más detalles sobre esto.

Las contraseñas o secretos almacenados en el archivo de autenticación sirven para dos propósitos. Primero, se usan para verificar las contraseñas de las conexiones de cliente entrantes, si se configura un método de autenticación basado en contraseña. Segundo, se usan como contraseñas para las conexiones salientes al servidor backend, si el servidor backend requiere autenticación basada en contraseña (a menos que la contraseña se especifique directamente en la cadena de conexión de la base de datos).

### Limitaciones {#limitations}

Si la contraseña se almacena en texto plano, puede usarse para cualquier autenticación basada en contraseña usada en el servidor backend: texto plano, MD5 o SCRAM (ver <https://www.postgresql.org/docs/current/auth-password.html> para más detalles).

Las contraseñas con hash MD5 pueden usarse si el servidor backend usa autenticación MD5 (o si usuarios específicos tienen contraseñas con hash MD5).

Los secretos SCRAM solo pueden usarse para iniciar sesión en un servidor si la autenticación del cliente también usa SCRAM, la definición de la base de datos de PgBouncer no especifica un nombre de usuario, y los secretos SCRAM son idénticos en PgBouncer y en el servidor PostgreSQL (mismo salt y mismas iteraciones, no meramente la misma contraseña). Esto se debe a una propiedad de seguridad inherente a SCRAM: el secreto SCRAM almacenado no puede usarse por sí solo para derivar credenciales de inicio de sesión.

El archivo de autenticación puede escribirse a mano, pero también es útil generarlo a partir de otra lista de usuarios y contraseñas. Ver `./etc/mkauth.py` para un script de ejemplo que genera el archivo de autenticación a partir de la tabla del sistema `pg_authid`. Alternativamente, usa `auth_query` en lugar de `auth_file` para evitar tener que mantener un archivo de autenticación separado.

### Nota sobre los servidores gestionados {#note-on-managed-servers}

Si el servidor backend está configurado para usar autenticación de contraseña SCRAM, PgBouncer no puede autenticarse con éxito si no conoce a) la contraseña del usuario en texto plano o b) el secreto SCRAM correspondiente.

Algunos proveedores de nube (p. ej. AWS RDS) prohíben el acceso a las tablas del sistema sensibles de PostgreSQL para obtener contraseñas. Incluso para el usuario con más privilegios (p. ej. miembro de `rds_superuser`), `select * from pg_authid` devuelve el `ERROR: permission denied for table pg_authid`. Ese es un comportamiento conocido ([blog](https://aws.amazon.com/blogs/database/best-practices-for-migrating-postgresql-databases-to-amazon-rds-and-amazon-aurora/)).

Por tanto, obtener un secreto SCRAM existente una vez que se ha almacenado en un servidor gestionado es imposible, lo que hace difícil configurar PgBouncer para usar el mismo secreto SCRAM. Sin embargo, el secreto SCRAM todavía puede configurarse y usarse en ambos lados mediante el siguiente truco:

Genera un secreto SCRAM para una contraseña arbitraria con una herramienta capaz de imprimir el secreto. Por ejemplo, `psql --echo-hidden` y el comando `\password` imprimen el secreto SCRAM en la consola antes de enviarlo al servidor.

```bash
$ psql --echo-hidden <connection_string>
postgres=# \password <role_name>
Enter new password for user "<role_name>":
Enter it again:
********* QUERY **********
ALTER USER <role_name> PASSWORD 'SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>'
**************************
```

Anota el secreto SCRAM de la QUERY y establécelo en el `userlist.txt` de PgBouncer.

Si usaste una herramienta distinta de `psql --echo-hidden`, entonces necesitas establecer también el secreto SCRAM en el servidor (puedes usar `ALTER ROLE <role_name> PASSWORD '<scram_secret>'` para ello).

--------

## Formato del archivo HBA {#hba-file-format}

La ubicación del archivo HBA la especifica el ajuste `auth_hba_file`. Solo se usa si `auth_type` está establecido en `hba`.

El archivo sigue el formato del archivo `pg_hba.conf` de PostgreSQL (ver <https://www.postgresql.org/docs/current/auth-pg-hba-conf.html>).

* Tipos de registro compatibles: `local`, `host`, `hostssl`, `hostnossl`.
* Campo de base de datos: admite `all`, `replication`, `sameuser`, `@file`, múltiples nombres. No compatible: `samerole`, `samegroup`.
* Campo de nombre de usuario: admite `all`, `@file`, múltiples nombres. No compatible: `+groupname`.
* Campo de dirección: admite `all`, IPv4, IPv6. No compatible: `samehost`, `samenet`, nombres DNS, prefijos de dominio.
* Campo de método de autenticación: solo se admiten los métodos compatibles con `auth_type` de PgBouncer, más `peer` y `reject`, pero excepto `any` y `pam`, que solo funcionan globalmente.
* El parámetro de mapeo de nombres de usuario (`map=`) es compatible cuando `auth_type` es `cert` o `peer`.

--------

## Formato del archivo de mapeo de identidades {#ident-map-file-format}

La ubicación del archivo de mapeo de identidades la especifica el ajuste `auth_ident_file`. Solo se carga si `auth_type` está establecido en `hba`.

El formato del archivo es una variación simplificada del archivo de mapeo de identidades de PostgreSQL (ver <https://www.postgresql.org/docs/current/auth-username-maps.html>).

* Solo se admiten líneas de la forma `map-name system-username database-username`.
* No hay soporte para incluir archivos/directorios.
* Campo system-username: no compatible: expresiones regulares.
* Campo database-username: admite `all` o un único nombre de usuario de Postgres. No compatible: `+groupname`, expresiones regulares.

--------

## Ejemplos {#examples}

Ejemplo de configuración pequeño:

```ini
[databases]
template1 = host=localhost dbname=template1 auth_user=someuser

[pgbouncer]
pool_mode = session
listen_port = 6432
listen_addr = localhost
auth_type = md5
auth_file = users.txt
logfile = pgbouncer.log
pidfile = pgbouncer.pid
admin_users = someuser
stats_users = stat_collector
```

Ejemplos de bases de datos:

```ini
[databases]

; foodb over Unix socket
foodb =

; redirect bardb to bazdb on localhost
bardb = host=localhost dbname=bazdb

; access to destination database will go with single user
forcedb = host=localhost port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO
```

Ejemplo de una función segura para `auth_query`:

```sql
CREATE OR REPLACE FUNCTION pgbouncer.user_lookup(in i_username text, out uname text, out phash text)
RETURNS record AS $$
BEGIN
    SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END
    FROM pg_authid
    WHERE rolname=i_username AND rolcanlogin
    INTO uname, phash;
    RETURN;
END;
$$ LANGUAGE plpgsql
   SECURITY DEFINER
   -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
   SET search_path = pg_catalog, pg_temp;
REVOKE ALL ON FUNCTION pgbouncer.user_lookup(text) FROM public, pgbouncer;
GRANT EXECUTE ON FUNCTION pgbouncer.user_lookup(text) TO pgbouncer;
```

Ejemplos de configuraciones para 2 procesos de PgBouncer emparejados con el fin de crear una configuración de PgBouncer multinúcleo usando `so_reuseport`. La configuración del primer proceso:

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
unix_socket_dir=/tmp/pgbouncer1
peer_id=1
```

La configuración del segundo proceso:

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
; only unix_socket_dir and peer_id are different
unix_socket_dir=/tmp/pgbouncer2
peer_id=2
```

--------

## Véase también {#see-also}

pgbouncer(1) - página de manual sobre el uso general y los comandos de la consola

<https://www.pgbouncer.org/>
