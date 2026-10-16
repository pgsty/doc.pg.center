---
title: "Registro de cambios"
weight: 70
description: "Historial de versiones y notas de publicación de PgBouncer"
icon: fa-solid fa-scroll
module: [PGBOUNCER]
categories: [Referencia]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/NEWS.md"
---

--------

## PgBouncer 1.26.x {#pgbouncer-126x}

**2026-09-23  -  PgBouncer 1.26.0  -  « Ignora todos los search_path anteriores »**

- Seguridad
    * Corrección de CVE-2026-19888: PgBouncer anterior a 1.26.0 no comprobaba que el client-final-message de SCRAM contuviera un nonce. Un atacante remoto no autenticado podía provocar la caída de PgBouncer enviando un client-final-message sin él. Esto también se aplica a los usuarios que no existen, porque PgBouncer ejecuta para ellos un intercambio SCRAM simulado. Este error existe desde que se añadió la compatibilidad con SCRAM en PgBouncer 1.11.0.
    * Corrección de CVE-2026-6668: un desbordamiento de enteros en la lógica de crecimiento del búfer de paquetes de PgBouncer anterior a 1.26.0 podía hacer que PgBouncer quedara bloqueado en un bucle infinito. Para ello era necesario enviar una gran cantidad de datos a un solo búfer de paquetes, algo posible sin autenticarse primero cuando `max_packet_size` se deja en su valor predeterminado. Como PgBouncer es de un solo hilo, este bloqueo impedía que atendiera a cualquier cliente hasta que el proceso fuera terminado.
    * Corrección de CVE-2026-6669: PgBouncer anterior a 1.26.0 no limitaba el número de iteraciones SCRAM que aceptaba de un servidor. Un servidor PostgreSQL malicioso o comprometido podía hacer que PgBouncer realizara una cantidad ilimitada de trabajo durante un solo inicio de sesión, impidiéndole mientras tanto atender a todos los demás clientes y bases de datos. El número de iteraciones debe ser ahora de 1000000 como máximo.
- Funcionalidades
    * Realiza un seguimiento de todos los parámetros que PostgreSQL comunica por defecto. Esto significa, sobre todo, que `search_path` (en PostgreSQL 18 y posteriores) y `default_transaction_read_only` (en PostgreSQL 14 y posteriores) ahora se siguen por defecto. Antes, un cliente que ejecutara `SET search_path` o `SET default_transaction_read_only = true` en modo de agrupación por transacciones podía afectar a otros clientes que después usaran la misma conexión de servidor. ([#1580], [#1573])
    * Añade el parámetro `pool_idle_timeout` para limpiar pools que lleven un tiempo sin usarse. Esto es útil en configuraciones con muchos usuarios distintos que se conectan con poca frecuencia. Sin este parámetro activado, el número de pools crece sin límite en ese tipo de configuraciones. El parámetro está desactivado por defecto, porque eliminar un pool también pierde sus estadísticas. ([#1491])
    * Permite configurar `query_wait_timeout` por usuario y por base de datos. ([#1449])
    * Añade la estadística `client_login_count` a `SHOW STATS`, que cuenta los inicios de sesión de clientes correctos. Esto permite detectar clientes que renuevan conexiones constantemente. ([#1457])
    * Envía a los clientes mensajes `ParameterStatus` específicos de PgBouncer al iniciar sesión: `pgbouncer.version`, `pgbouncer.pool_mode` y `pgbouncer.max_prepared_statements`. Esto permite a los clientes y a los controladores detectar que están conectados a través de PgBouncer y adaptar su comportamiento en consecuencia. ([#1490])
    * Añade el parámetro `login_notify_message`. Cuando está definido, su valor se envía a los clientes como mensaje NOTICE después de iniciar sesión. Puede usarse para dejar claro a los clientes que están conectados a través de PgBouncer y no directamente a PostgreSQL. ([#1488])
    * Añade compatibilidad con la compilación de PgBouncer con meson, incluida una compilación para Windows usando el entorno UCRT64. Las compilaciones con Autoconf siguen siendo compatibles. ([#1524], [#1426], [#1568], [#1585], [#1602], [#1607])
    * Añade un logotipo. ([#1609])
- Cambios
    * Elimina la funcionalidad obsoleta de reinicio en línea (`-R`, también conocida como toma de control), junto con los comandos de administración `SHOW FDS` y `SUSPEND`, que solo existían para admitirla. Usa en su lugar [reinicios sucesivos con `so_reuseport`][rolling-restart-docs]. ([#1581])
    * Aumenta la longitud máxima de las contraseñas a 65535 bytes, igualando a libpq. ([#1310], [#1520])
    * Trata un nombre de usuario `NULL` devuelto por `auth_query` igual que la ausencia de filas, en lugar de tratarlo como un error. ([#1569])
    * Acepta `SET extra_float_digits` en la base de datos de administración, que los controladores JDBC de PostgreSQL más recientes envían durante la configuración de la conexión. ([#1550])
    * Permite que `mkauth.py` escriba en stdout pasando `-` como archivo de salida. ([#1514])
    * Deja de registrar errores ruidosos por EOF inesperado de los clientes cuando se compila contra OpenSSL 3. ([#1507])
    * Incluye el error del sistema subyacente en los mensajes de error TLS cuando se compila contra OpenSSL 3. ([#1492])
    * Requiere un compilador C11. ([#1417])
    * Registra qué límite provocó el desalojo de una conexión de servidor. El motivo de desconexión es ahora `evicted for max_db_connections`, `evicted for pool_size` o `evicted for max_user_connections` en lugar del simple `evicted`. ([#1597])
- Correcciones
    * Corrige el agotamiento del pool causado por mensajes `COPY` tardíos en modo de agrupación por transacciones. Esto también hace que `COPY` funcione fuera de una transacción explícita en modo de agrupación por transacciones. ([#1471])
    * Corrige los fallos de autenticación LDAP con DN largos aumentando la longitud máxima de las URL LDAP. ([#1497])
    * Corrige la corrupción por pass-through SCRAM de las credenciales en caché de un usuario forzado, lo que provocaba fallos de inicio de sesión en el servidor, con el servidor real rechazando la prueba SCRAM. ([#1612])
    * Corrige el fallo del pass-through SCRAM con secretos SCRAM almacenados tras una reconexión al servidor, con el error "password is SCRAM secret but client authentication did not provide SCRAM keys". ([#1504], error introducido en la versión 1.25.1)
    * Corrige una caída por use-after-free cuando un cliente de replicación se desconecta mientras su conexión de servidor sigue iniciando sesión. ([#1577])
    * Corrige el desalojo de conexiones de servidor inactivas para clientes de replicación cuando el pool está lleno. Antes, un solo cliente de replicación podía desalojar todos los servidores inactivos del pool en lugar de solo uno, y no se producía desalojo alguno cuando el pool contenía más servidores que `pool_size` debido al pool de reserva o a solicitudes de cancelación. ([#1597])
    * Corrige las conexiones TLS estancadas cuando un paquete cruza el límite del búfer de paquetes, por ejemplo un `SET application_name` con un valor largo. ([#1531])
    * Corrige el envío en orden incorrecto de las respuestas de instrucciones preparadas cuando un lote mezcla mensajes `Parse` y `Close` sin un `Sync` entre ellos. ([#1555])
    * Corrige el comportamiento incorrecto cuando un cliente define en su paquete de inicio parámetros listados en `track_extra_parameters` que el servidor no comunica. ([#1576])
    * Corrige los fallos de inicio de sesión cuando el servidor reparte sus paquetes de inicio de sesión entre varios paquetes TCP, por ejemplo cuando hay otro proxy entre PgBouncer y PostgreSQL. ([#1446])
    * Corrige el cierre de conexiones por `query_timeout` cuando no había ninguna consulta en curso. ([#1395])
    * Corrige el envío de un mensaje `NegotiateProtocolVersion` duplicado cuando no había ningún servidor disponible de inmediato. ([#1460])
    * Corrige que la columna `pool_size` de `SHOW USERS` mostrara un valor para usuarios que no tienen ninguno configurado. ([#1489])
    * Corrige el mensaje de error del comando de administración `ENABLE`. ([#1308])
    * Corrige la compilación contra futuras versiones de OpenSSL que hacen opaca a `struct asn1_string_st`. ([#1440])
    * Impide que el compilador optimice y elimine el borrado de datos criptográficos sensibles de la pila. ([#1508])
    * Corrige el enlazado de `pgbevent.dll` con clang en Windows. ([#1571])
    * Corrige las rutas de los archivos del nivel raíz en el archivo tar de la versión, que se almacenaban como `pgbouncer-X.Y.Z/./configure` en lugar de `pgbouncer-X.Y.Z/configure`. ([#1549])
    * Corrige una fuga de memoria al leer `track_extra_parameters` de la configuración. ([#1510])
    * Corrige una fuga de memoria por cada paquete de inicio que contuviera un parámetro de extensión de protocolo (prefijo `_pq_.`), que podía ser provocada por clientes no autenticados. ([#1540])

[rolling-restart-docs]: /es/pgbouncer/usage/#shutdown-wait_for_clients
[#1308]: https://github.com/pgbouncer/pgbouncer/pull/1308
[#1310]: https://github.com/pgbouncer/pgbouncer/pull/1310
[#1395]: https://github.com/pgbouncer/pgbouncer/pull/1395
[#1417]: https://github.com/pgbouncer/pgbouncer/pull/1417
[#1426]: https://github.com/pgbouncer/pgbouncer/pull/1426
[#1440]: https://github.com/pgbouncer/pgbouncer/pull/1440
[#1446]: https://github.com/pgbouncer/pgbouncer/pull/1446
[#1449]: https://github.com/pgbouncer/pgbouncer/pull/1449
[#1457]: https://github.com/pgbouncer/pgbouncer/pull/1457
[#1460]: https://github.com/pgbouncer/pgbouncer/pull/1460
[#1471]: https://github.com/pgbouncer/pgbouncer/pull/1471
[#1488]: https://github.com/pgbouncer/pgbouncer/pull/1488
[#1489]: https://github.com/pgbouncer/pgbouncer/pull/1489
[#1490]: https://github.com/pgbouncer/pgbouncer/pull/1490
[#1491]: https://github.com/pgbouncer/pgbouncer/pull/1491
[#1492]: https://github.com/pgbouncer/pgbouncer/pull/1492
[#1497]: https://github.com/pgbouncer/pgbouncer/pull/1497
[#1504]: https://github.com/pgbouncer/pgbouncer/pull/1504
[#1507]: https://github.com/pgbouncer/pgbouncer/pull/1507
[#1508]: https://github.com/pgbouncer/pgbouncer/pull/1508
[#1510]: https://github.com/pgbouncer/pgbouncer/pull/1510
[#1514]: https://github.com/pgbouncer/pgbouncer/pull/1514
[#1520]: https://github.com/pgbouncer/pgbouncer/pull/1520
[#1524]: https://github.com/pgbouncer/pgbouncer/pull/1524
[#1531]: https://github.com/pgbouncer/pgbouncer/pull/1531
[#1540]: https://github.com/pgbouncer/pgbouncer/pull/1540
[#1549]: https://github.com/pgbouncer/pgbouncer/pull/1549
[#1550]: https://github.com/pgbouncer/pgbouncer/pull/1550
[#1555]: https://github.com/pgbouncer/pgbouncer/pull/1555
[#1568]: https://github.com/pgbouncer/pgbouncer/pull/1568
[#1569]: https://github.com/pgbouncer/pgbouncer/pull/1569
[#1571]: https://github.com/pgbouncer/pgbouncer/pull/1571
[#1573]: https://github.com/pgbouncer/pgbouncer/pull/1573
[#1576]: https://github.com/pgbouncer/pgbouncer/pull/1576
[#1577]: https://github.com/pgbouncer/pgbouncer/pull/1577
[#1580]: https://github.com/pgbouncer/pgbouncer/pull/1580
[#1581]: https://github.com/pgbouncer/pgbouncer/pull/1581
[#1585]: https://github.com/pgbouncer/pgbouncer/pull/1585
[#1597]: https://github.com/pgbouncer/pgbouncer/pull/1597
[#1602]: https://github.com/pgbouncer/pgbouncer/pull/1602
[#1607]: https://github.com/pgbouncer/pgbouncer/pull/1607
[#1609]: https://github.com/pgbouncer/pgbouncer/pull/1609
[#1612]: https://github.com/pgbouncer/pgbouncer/pull/1612

--------

## PgBouncer 1.25.x {#pgbouncer-125x}

**2026-05-08  -  PgBouncer 1.25.2  -  « Un toque humano con un giro inesperado en una carrera por el título llena de incertidumbres »**

- Seguridad
  * Corrección de CVE-2026-6664: un desbordamiento de enteros en el código de análisis de paquetes de red de PgBouncer anterior a 1.25.2 omite una comprobación de límites y puede provocar una caída. Un atacante remoto no autenticado puede provocar la caída de PgBouncer con un paquete de autenticación SCRAM malformado.
  * Corrección de CVE-2026-6665: el código SCRAM de PgBouncer anterior a 1.25.2 no comprobaba correctamente el valor de retorno de `strlcat()` al construir el contenido del client-final-message de SCRAM. Un backend malicioso que envíe un server-final-message de SCRAM con un nonce largo puede provocar un desbordamiento de pila.
  * Corrección de CVE-2026-6666: una posible referencia a puntero nulo en PgBouncer anterior a 1.25.2 podía provocar una caída si un servidor enviaba una respuesta de error sin campo SQLSTATE.
  * Corrección de CVE-2026-6667: PgBouncer anterior a 1.25.2 no realizaba una comprobación de autorización adecuada para el comando de administración `KILL_CLIENT`. Todos los usuarios con acceso a la consola de administración, que a su vez requiere autorización, podían ejecutar este comando. Solo debería permitirse a los usuarios listados en el parámetro `admin_users`.

- Correcciones
  * Aclara la documentación del parámetro `default_pool_size`.
  * Corrige la documentación de `client_tls13_ciphers` y `server_tls13_ciphers`.

**2025-12-03  -  PgBouncer 1.25.1  -  « Corrigiendo un montón de errores antes de Navidad »**

- Seguridad
  * Corrección de CVE-2025-12819: antes de esta versión, un atacante no autenticado podía ejecutar SQL arbitrario durante la autenticación proporcionando un parámetro search_path malicioso en el StartupMessage. Los sistemas que presenten TODAS las configuraciones siguientes son vulnerables:

    1. `track_extra_parameters` incluye search_path (configuración no predeterminada, probablemente configurada solo en entornos que involucran a Citus o PostgreSQL 18)
    2. `auth_user` está definido con una cadena no vacía (configuración no predeterminada)
    3. `auth_query` está configurado sin nombres de objetos totalmente calificados (configuración predeterminada, el operador < no está calificado por esquema)

- Correcciones
    - Corrige errores con la autenticación SCRAM ad hoc tras reconectar con el servidor ([#1432], introducido en la versión 1.25.0)
    - Añade las definiciones de tipos (typedefs) faltantes para arquitecturas exóticas sin soporte SIMD ([#1414], introducido en la versión 1.25.0)
    - Elimina el aviso ruidoso en el registro cuando el cliente cierra la conexión antes de enviar datos ([#1420], introducido en la versión 1.25.0)
    - Evita una posible desreferencia de puntero NULL ([#1423], introducido en la versión 1.25.0)
    - Corrige una posible fuga de memoria ([#1422], introducido en la versión 1.25.0)
    - Corrige el análisis de los mensajes del servidor en SCRAM ([#1431], introducido en la versión 1.25.0)

[#1414]: https://github.com/pgbouncer/pgbouncer/pull/1414
[#1420]: https://github.com/pgbouncer/pgbouncer/pull/1420
[#1422]: https://github.com/pgbouncer/pgbouncer/pull/1422
[#1423]: https://github.com/pgbouncer/pgbouncer/pull/1423
[#1431]: https://github.com/pgbouncer/pgbouncer/pull/1431
[#1432]: https://github.com/pgbouncer/pgbouncer/pull/1432

**2025-11-09  -  PgBouncer 1.25.0  -  « La versión con soporte de LDAP »**

- Funcionalidades
    * ¡Añade autenticación LDAP! Puede configurarse mediante un archivo HBA o mediante `auth_ldap_options`. ([#731])
    * Añade compatibilidad con conexiones TLS directas del lado del cliente. Esto permite a los clientes usar el establecimiento de conexiones TLS más rápido que se introdujo en PostgreSQL 17. PgBouncer (todavía) no puede conectarse a servidores PostgreSQL usando este establecimiento de conexión más rápido. ([#1359])
    * Añade el estado idle a `SHOW CLIENTS`. ([#1191])
    * Añade el parámetro `transaction_timeout`, tanto globalmente como a nivel de usuario. ([#1242])
    * Envía un mensaje NOTICE al cliente si permanece en cola más de 5 segundos sin recibir una conexión. Esta duración puede cambiarse o desactivarse con `query_wait_notify`. ([#1264])
    * Añade el parámetro `scram_iterations` para permitir a los operadores intercambiar seguridad por velocidad de autenticación ([#1339])
    * Añade `client_tls13_ciphers` y `server_tls13_ciphers` para elegir qué suites de cifrado TLSv1.3 activar. ([#1352])
- Cambios
    * Mejora considerablemente el rendimiento de la autenticación SCRAM ad hoc. ([#1338])
    * Permite que `KILL` no reciba ninguna base de datos, lo que ahora significa `KILL` en todas las bases de datos. ([#1317])
    * La consulta de comprobación de estado envía por defecto una consulta vacía en lugar de `SELECT 1`. ([#1233])
    * Registra como aviso que la cola PAM está llena. Esto facilita encontrar la causa de las consultas lentas que esta provoca. ([#1297])
    * El comando `RELOAD` ahora informa de cualquier error ocurrido durante la recarga. ([#1231])
    * Habilita el acceso al socket UNIX de PgBouncer durante el apagado para conexiones de administración. Esto facilita que un operador averigüe por qué un proceso de PgBouncer no se está apagando y/o ejecute manualmente `KILL_CLIENT` para conexiones atascadas. ([#1305])
    * Cambia `mkauth.py` para que ya no añada un tercer campo obsoleto ([#1365])
    * Mejora los mensajes `FATAL` en las funciones `disconnect_client` y `disconnect_server`. ([#1382])
    * Deja de usar la función obsoleta de OpenSSL `EVP_PKEY_get0_EC_KEY`. Esto podía causar problemas con ciertas implementaciones FIPS. ([#1384])
- Correcciones
    * Corrige una caída relacionada con contraseñas largas (1024 caracteres o más). ([#1215])
    * Corrige las conexiones multihost cuando se usa `server_tls_sslmode=verify-full`. ([#1303])
    * Corrige un error `FATAL` poco frecuente al reenviar solicitudes de cancelación. ([#1383])
    * Corrige la ordenación de parámetros en `SHOW CONFIG`. ([#1403])
    * Endurece el análisis del paquete de inicio. ([#1407])

[#731]: https://github.com/pgbouncer/pgbouncer/pull/731
[#1191]: https://github.com/pgbouncer/pgbouncer/pull/1191
[#1215]: https://github.com/pgbouncer/pgbouncer/pull/1215
[#1231]: https://github.com/pgbouncer/pgbouncer/pull/1231
[#1233]: https://github.com/pgbouncer/pgbouncer/pull/1233
[#1242]: https://github.com/pgbouncer/pgbouncer/pull/1242
[#1264]: https://github.com/pgbouncer/pgbouncer/pull/1264
[#1297]: https://github.com/pgbouncer/pgbouncer/pull/1297
[#1303]: https://github.com/pgbouncer/pgbouncer/pull/1303
[#1305]: https://github.com/pgbouncer/pgbouncer/pull/1305
[#1317]: https://github.com/pgbouncer/pgbouncer/pull/1317
[#1338]: https://github.com/pgbouncer/pgbouncer/pull/1338
[#1339]: https://github.com/pgbouncer/pgbouncer/pull/1339
[#1352]: https://github.com/pgbouncer/pgbouncer/pull/1352
[#1359]: https://github.com/pgbouncer/pgbouncer/pull/1359
[#1365]: https://github.com/pgbouncer/pgbouncer/pull/1365
[#1382]: https://github.com/pgbouncer/pgbouncer/pull/1382
[#1383]: https://github.com/pgbouncer/pgbouncer/pull/1383
[#1384]: https://github.com/pgbouncer/pgbouncer/pull/1384
[#1403]: https://github.com/pgbouncer/pgbouncer/pull/1403
[#1407]: https://github.com/pgbouncer/pgbouncer/pull/1407

--------

## PgBouncer 1.24.x {#pgbouncer-124x}

**2025-04-16  -  PgBouncer 1.24.1  -  « CVE-2025-2291 VALID UNTIL ayer »**

- Seguridad
  * Corrección de CVE-2025-2291: anteriormente, PgBouncer no tenía en cuenta la cláusula
    VALID UNTIL de la contraseña de un usuario al consultar los hashes de contraseñas
    mediante su auth_query. Por tanto, si PgBouncer se usaba como proxy transparente
    delante de Postgres, podía permitir contraseñas que ya habían expirado. Para
    resolver este problema, la auth_query predeterminada y los ejemplos de funciones
    auth_query personalizadas de la documentación se han cambiado para tener en
    cuenta VALID UNTIL. Si usas una auth_query personalizada, debes actualizarla
    en consecuencia. Si usas la auth_query predeterminada, puedes actualizar a
    PgBouncer 1.24.1 o cambiar tu configuración para usar la nueva auth_query
    predeterminada en una versión anterior de PgBouncer.

- Correcciones
  * Corrige la compatibilidad con PAM revirtiendo la compatibilidad de autenticación `pam` en el archivo HBA. ([#1291]) (error introducido en la versión 1.24.0)
  * Corrige un error al decrementar el número de conexiones de usuario. Esto estaba incluido en la etiqueta de 1.24.0 en GitHub, pero el archivo tar de la versión no contenía esta corrección.  ([#1238]) (error introducido en la versión 1.24.0)
  * Añade `test_load_balance_hosts.py` al archivo tar. ([#1282])
  * Corrige problemas con las pruebas para que los empaquetadores de Debian puedan ejecutarlas. ([#1266], [#1250])

- Documentación
  * Actualiza el ejemplo de `auth_query` para definir un `search_path` seguro. ([#1245])

[#1238]: https://github.com/pgbouncer/pgbouncer/pull/1238
[#1291]: https://github.com/pgbouncer/pgbouncer/pull/1291
[#1282]: https://github.com/pgbouncer/pgbouncer/pull/1282
[#1266]: https://github.com/pgbouncer/pgbouncer/pull/1266
[#1250]: https://github.com/pgbouncer/pgbouncer/pull/1250
[#1245]: https://github.com/pgbouncer/pgbouncer/pull/1245

**2025-01-10  -  PgBouncer 1.24.0  -  « Año nuevo, bouncer nuevo »**

- Funcionalidades
  * Añade compatibilidad con `Type=notify-reload` para systemd. Esto requiere systemd
    versión 253 o posterior. ([#1148])
  * Añade el comando `KILL_CLIENT` a la consola de administración. Esto permite terminar
    una conexión de cliente por la fuerza. ([#1147])
  * Añade el parámetro `max_user_client_connections`, tanto globalmente como a nivel de usuario. ([#1137])
  * Añade el parámetro `max_db_client_connections`, tanto globalmente como a nivel de base de datos. ([#1138])
  * Añade el contador `current_client_connections` a la salida de `SHOW USERS` y `SHOW DATABASES`. ([#1137], [#1138])
  * Añade el parámetro `load_balance_hosts`, para admitir **no** hacer balanceo de carga entre hosts. ([#736])
  * Expone contadores de uso de instrucciones preparadas en `SHOW STATS`. ([#1192])
  * Añade el parámetro `client_idle_timeout`. ([#1189])
  * Añade `query_timeout` y `reserve_pool_size` a nivel de usuario. ([#1180], [#1228])
  * Activa la compatibilidad de autenticación `pam` en el archivo HBA. ([#326])

- Cambios
  * No recicla conexiones en RELOAD si la configuración TLS no ha cambiado. Antes,
    si tenías conexiones TLS, todas se reciclaban en RELOAD, lo que podía
    causar una degradación del rendimiento temporal pero grave. Ahora esto solo
    ocurre cuando la configuración TLS cambia realmente. ([#1157])
  * Activa por defecto la compatibilidad con instrucciones preparadas; `max_prepared_statements`
    ahora está fijado en 200 por defecto. Este cambio en los valores predeterminados
    solo debería afectar a los clientes que realmente usan instrucciones preparadas.
    Si usas instrucciones preparadas, se recomienda leer sobre las limitaciones de la
    compatibilidad con instrucciones preparadas en [nuestra documentación][prepared-docs] ([#1144])
  * Los sockets/clientes/servidores ahora pueden identificarse por un ID único en la
    salida de administración. Antes podían identificarse por su puntero, pero estos
    solían ser reutilizados por nuevos clientes tras la desconexión. ([#1172])
  * Error más claro para un pidfile vacío. ([#1195])
  * Devuelve el error original al cliente en caso de fallo de `server_login_retry`. ([#1152])
  * Registra el error original del servidor en caso de error de `auth_query`. ([#1187])
  * Definir `default_pool_size` en 0 significa tamaño ilimitado. ([#1227])
  * Cambia el nombre del parámetro `reserve_pool` para bases de datos a
    `reserve_pool_size`. El nombre anterior sigue siendo un alias del nombre nuevo.
    ([#1232])

- Correcciones
  * Gestiona mejor varios casos de error improbables, como errores de OOM. Estos
    antes podían provocar caídas o fugas de memoria. ([#1108], [#1101], [#1099], [#1169], [#1202])
  * Corrige el valor predeterminado de `server_tls_sslmode` en el archivo de configuración de ejemplo. ([#1133])
  * Elimina la mención en la documentación de un alias no válido para `server_tls_protocols`. ([#1155])
  * Corrige un error al usar `auth_query` y conexiones de replicación a la vez. Este
    error provocaba fallos de conexión en ese tipo de configuraciones. ([#1166])
  * Ignora las solicitudes de cancelación del cliente mientras PgBouncer configura un parámetro del servidor. ([#298])

[prepared-docs]: /es/pgbouncer/config/#max_prepared_statements

[#1148]: https://github.com/pgbouncer/pgbouncer/pull/1148
[#1147]: https://github.com/pgbouncer/pgbouncer/pull/1147
[#1137]: https://github.com/pgbouncer/pgbouncer/pull/1137
[#1138]: https://github.com/pgbouncer/pgbouncer/pull/1138
[#736]: https://github.com/pgbouncer/pgbouncer/pull/736
[#1192]: https://github.com/pgbouncer/pgbouncer/pull/1192
[#1189]: https://github.com/pgbouncer/pgbouncer/pull/1189
[#1180]: https://github.com/pgbouncer/pgbouncer/pull/1180
[#1228]: https://github.com/pgbouncer/pgbouncer/pull/1228
[#326]: https://github.com/pgbouncer/pgbouncer/pull/326
[#1157]: https://github.com/pgbouncer/pgbouncer/pull/1157
[#1144]: https://github.com/pgbouncer/pgbouncer/pull/1144
[#1172]: https://github.com/pgbouncer/pgbouncer/pull/1172
[#1195]: https://github.com/pgbouncer/pgbouncer/pull/1195
[#1152]: https://github.com/pgbouncer/pgbouncer/pull/1152
[#1187]: https://github.com/pgbouncer/pgbouncer/pull/1187
[#1227]: https://github.com/pgbouncer/pgbouncer/pull/1227
[#1232]: https://github.com/pgbouncer/pgbouncer/pull/1232
[#1108]: https://github.com/pgbouncer/pgbouncer/pull/1108
[#1101]: https://github.com/pgbouncer/pgbouncer/pull/1101
[#1099]: https://github.com/pgbouncer/pgbouncer/pull/1099
[#1169]: https://github.com/pgbouncer/pgbouncer/pull/1169
[#1202]: https://github.com/pgbouncer/pgbouncer/pull/1202
[#1133]: https://github.com/pgbouncer/pgbouncer/pull/1133
[#1155]: https://github.com/pgbouncer/pgbouncer/pull/1155
[#1166]: https://github.com/pgbouncer/pgbouncer/pull/1166
[#298]: https://github.com/pgbouncer/pgbouncer/pull/298

--------

## PgBouncer 1.23.x {#pgbouncer-123x}

**2024-08-02  -  PgBouncer 1.23.1  -  « Todo queda en orden »**

- Correcciones
  * Corrige un posible fallo de segmentación después de que PgBouncer recargue su
    configuración. ([#1105]) (error introducido en la versión 1.23.0)
  * Corrige todas las caídas conocidas de put_in_order. ([#1120])
    (las nuevas caídas se introdujeron en la versión 1.23.0)
  * Añade al archivo tar de la versión los archivos faltantes necesarios para las pruebas.
    ([#1124]) (la ausencia de archivos se introdujo en la versión 1.23.0)

[#1120]: https://github.com/pgbouncer/pgbouncer/pull/1120
[#1105]: https://github.com/pgbouncer/pgbouncer/pull/1105
[#1124]: https://github.com/pgbouncer/pgbouncer/pull/1124

**2024-07-03  -  PgBouncer 1.23.0  -  « Hacia los nuevos comienzos »**

- Funcionalidades
  * Añade compatibilidad con reinicios sucesivos. SIGTERM ya no provoca el apagado
    inmediato del proceso de PgBouncer. Ahora realiza un «apagado súper seguro»:
    espera a que todos los clientes se desconecten antes de apagarse. El nuevo
    comportamiento de SIGTERM permite reinicios sucesivos de varios procesos de
    PgBouncer tras un balanceador de carga, o escuchando en el mismo puerto
    usando `so_reuseport`.
    Esto es un **cambio incompatible menor**. Si dependías del comportamiento antiguo
    de SIGTERM en tu Dockerfile o en tu archivo de servicio de Systemd, ahora deberías usar SIGQUIT.
    ([#902])
  * Añade compatibilidad con mapas de nombres de usuario para los métodos de autenticación
    `cert` y `peer`. Esta funcionalidad aporta la flexibilidad de que el usuario que
    inicia la conexión no tiene que ser el usuario de la base de datos. La compatibilidad
    de PgBouncer con los mapas de nombres de usuario funciona de forma muy similar a
    postgres, con las excepciones enumeradas en la documentación. ([#996])
  * Añade compatibilidad con conexiones de replicación a través de PgBouncer. ([#876])

- Cambios
  * Mejora la salida de `SHOW USERS` listando las conexiones. ([#1040])
  * Permite la configuración de `pool_size` por usuario. ([#1049])
  * Permite la configuración de `server_lifetime` por base de datos. ([#1057])
  * Añade compatibilidad con el listado de usuarios creados dinámicamente en la salida de `SHOW USERS`. ([#1052])
  * Añade compatibilidad con el tipo de dirección `all` en la configuración hba. ([#1078])
  * Añade compatibilidad con el reinicio automático al usar systemd. ([#1080])
  * Aumenta el requisito de versión mínima de c-ares a 1.9.0 ([#1076])

- Correcciones
  * Corrige problemas al manejar paquetes de inicio grandes y parciales. ([#1058])
  * Añade compatibilidad con el formato `--config=value` en el parámetro de inicio options. ([#1064])
  * Corrige el cálculo de la métrica `avg_wait_time`. ([#727])
  * Añade compatibilidad con la negociación de la versión del protocolo de postgres con el cliente. ([#1007])
  * Añade solicitud pendiente para `auth_query`. ([#1034])
  * Múltiples mejoras en la documentación y en el CI.

[#996]: https://github.com/pgbouncer/pgbouncer/pull/996
[#1040]: https://github.com/pgbouncer/pgbouncer/pull/1040
[#1049]: https://github.com/pgbouncer/pgbouncer/pull/1049
[#1057]: https://github.com/pgbouncer/pgbouncer/pull/1057
[#1052]: https://github.com/pgbouncer/pgbouncer/pull/1052
[#1058]: https://github.com/pgbouncer/pgbouncer/pull/1058
[#1007]: https://github.com/pgbouncer/pgbouncer/pull/1007
[#876]: https://github.com/pgbouncer/pgbouncer/pull/876
[#902]: https://github.com/pgbouncer/pgbouncer/pull/902
[#1064]: https://github.com/pgbouncer/pgbouncer/pull/1064
[#1078]: https://github.com/pgbouncer/pgbouncer/pull/1078
[#1080]: https://github.com/pgbouncer/pgbouncer/pull/1080
[#727]: https://github.com/pgbouncer/pgbouncer/pull/727
[#1076]: https://github.com/pgbouncer/pgbouncer/pull/1076
[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034

--------

## PgBouncer 1.22.x {#pgbouncer-122x}

**2024-03-04  -  PgBouncer 1.22.1  -  « Es verano en Bangalore »**

- Correcciones
  * Corrige problemas causados por algunos clientes que usan consultas
    `COPY FROM STDIN`. Dichas consultas podían introducir fugas de
    memoria, regresiones de rendimiento y un comportamiento incorrecto
    de las instrucciones preparadas. ([#1025])
    (error introducido en la versión 1.21.0)
  * Añade las pruebas faltantes al archivo tar de la versión ([#1026])
    (la ausencia de pruebas se introdujo en las versiones 1.19.0 y 1.21.0)

[#1025]: https://github.com/pgbouncer/pgbouncer/pull/1025
[#1026]: https://github.com/pgbouncer/pgbouncer/pull/1026

**2024-01-31  -  PgBouncer 1.22.0  -  « DEALLOCATE ALL »**

- Funcionalidades
  * Añade compatibilidad con `DEALLOCATE ALL` y `DISCARD ALL` cuando
    `max_prepared_statements` está definido en un valor distinto de cero (`DEALLOCATE`
    normal sigue sin ser compatible) ([#972])
  * Permite configurar `auth_query` por base de datos ([#979])

- Cambios
  * Mejora la configuración del archivo de unidad de systemd recomendado ([#983])
  * Hace que la lógica de fallo rápido gestione todos los escenarios en los que ya
    no existen conexiones operativas a la base de datos y no puede establecerse ninguna ([#998])
  * Múltiples mejoras en la documentación

- Correcciones
  * Corrige un problema en PG14+ por el que PgBouncer enviaba
    `SET DateStyle='ISO'` en cada transacción ([#879])
  * Corrige el manejo de un `application_name` vacío ([#999])
  * Corrige la compilación en Windows con OpenSSL 3.2.0 ([#1009])

[#972]: https://github.com/pgbouncer/pgbouncer/pull/972
[#979]: https://github.com/pgbouncer/pgbouncer/pull/979
[#983]: https://github.com/pgbouncer/pgbouncer/pull/983
[#998]: https://github.com/pgbouncer/pgbouncer/pull/998
[#879]: https://github.com/pgbouncer/pgbouncer/pull/879
[#999]: https://github.com/pgbouncer/pgbouncer/pull/999
[#1009]: https://github.com/pgbouncer/pgbouncer/pull/1009

--------

## PgBouncer 1.21.x {#pgbouncer-121x}

**2023-10-16  -  PgBouncer 1.21.0  -  « La versión con las instrucciones preparadas »**

- Funcionalidades
  * ¡Añade compatibilidad con instrucciones preparadas con nombre a nivel de protocolo!
    Probablemente sea una de las funcionalidades más solicitadas de PgBouncer.
    Usar instrucciones preparadas junto con PgBouncer puede reducir mucho la carga de
    CPU de tu sistema (tanto del lado de PgBouncer como del lado de PostgreSQL). En
    pruebas sintéticas, esta funcionalidad llegó a aumentar el rendimiento de las
    consultas en cualquier punto entre el 15% y el 250%, dependiendo de la carga de
    trabajo. Para beneficiarte de esta nueva funcionalidad tienes que cambiar el
    nuevo parámetro `max_prepared_statements` a un valor distinto de cero
    (el valor exacto depende de tu carga de trabajo, pero 100 es probablemente
    razonable).
    Consulta [la documentación de
    `max_prepared_statements`](/es/pgbouncer/config/#max_prepared_statements)
    para ver en detalle cómo funciona la funcionalidad, sus limitaciones y cómo
    ajustar el valor. Después de eso, asegúrate de que tu biblioteca
    cliente realmente use instrucciones preparadas. Cómo hacerlo difiere en cada cliente,
    así que deberías consultar la documentación del cliente que uses. Esta funcionalidad
    se ha probado a fondo antes de publicarla, pero es muy posible que existan
    problemas de rendimiento o errores debido a la complejidad de la funcionalidad. Si
    encuentras alguno, repórtalo. ([#845])

- Cambios
  * Mejora la seguridad de la configuración de OpenSSL; los valores predeterminados
    usados estaban MUY desactualizados. Con esta versión, los valores predeterminados
    son ahora los mismos que los de OpenSSL del sistema que ejecuta PgBouncer. ([#948] & [libusual/#41])
  * PgBouncer ahora usa OpenSSL para calcular hashes MD5 cuando es posible. Esto es
    necesario para usar PgBouncer de forma conforme a FIPS. ([#949])
  * Mantiene `min_pool_size` para pools con un usuario forzado incluso si no hay clientes
    conectados a PgBouncer ([#947])
  * La forma en que PgBouncer codifica un `peer_id` en el token de cancelación ha
    cambiado; esto significa que el peering entre distintas versiones de PgBouncer
    no funcionará si no todas están del mismo lado del límite de la versión
    v1.21.0. ([#945])

- Correcciones
  * Corrige una caída con el mensaje de error: "FATAL in function client\_proto(): bad
    client state: 6/7" ([#928]) (error introducido en la versión 1.18.0)
  * Corrige una caída con el mensaje de error: "FATAL in function server\_proto(): server in
    bad state: 11" ([#927]) (error introducido en la versión 1.18.0)
  * Reduce el nivel de registro del envío de cancelaciones ([#903])
  * Corrige el prefijo de registro de slog para los peers ([#922])
  * Corrige erratas en la documentación ([#932])
  * Corrige errores señalados por el analizador estático ([#943])
  * No termina a todos los clientes en espera ante errores FATAL temporales durante el inicio de sesión ([#946])
  * Usa la base de datos automática cuando la base de datos en `auth_dbname` no está configurada explícitamente
    ([#921])

- Limpieza
  * Elimina la compatibilidad con udns ([#938])

[#845]: https://github.com/pgbouncer/pgbouncer/pull/845
[#948]: https://github.com/pgbouncer/pgbouncer/pull/948
[#949]: https://github.com/pgbouncer/pgbouncer/pull/949
[#947]: https://github.com/pgbouncer/pgbouncer/pull/947
[#945]: https://github.com/pgbouncer/pgbouncer/pull/945
[#903]: https://github.com/pgbouncer/pgbouncer/pull/903
[#922]: https://github.com/pgbouncer/pgbouncer/pull/922
[#932]: https://github.com/pgbouncer/pgbouncer/pull/932
[#928]: https://github.com/pgbouncer/pgbouncer/pull/928
[#927]: https://github.com/pgbouncer/pgbouncer/pull/927
[#943]: https://github.com/pgbouncer/pgbouncer/pull/943
[#946]: https://github.com/pgbouncer/pgbouncer/pull/946
[#921]: https://github.com/pgbouncer/pgbouncer/pull/921
[#938]: https://github.com/pgbouncer/pgbouncer/pull/938
[libusual/#41]: https://github.com/libusual/libusual/pull/41

--------

## PgBouncer 1.20.x {#pgbouncer-120x}

**2023-08-09  -  PgBouncer 1.20.1  -  « Opciones opcionales »**

- Correcciones
  * Corrige una regresión por la que poner `options` dentro de `ignore_startup_parameters`
    ya no ignoraba los parámetros desconocidos dentro del parámetro de inicio
    `options`. ([#908]) (la regresión se introdujo en la versión 1.20.0)
  * Corrige una errata confusa en la documentación ([#917])

[#908]: https://github.com/pgbouncer/pgbouncer/pull/908
[#917]: https://github.com/pgbouncer/pgbouncer/pull/917

**2023-07-20  -  PgBouncer 1.20.0  -  « Aquí va un nombre gracioso »**

- Deprecaciones
  * La opción de reinicio en línea ahora se considera obsoleta. La funcionalidad ha
    recibido muy poca atención en los últimos años. Hay varios problemas conocidos
    con ella y las funcionalidades añadidas recientemente a menudo no la admiten. El
    método recomendado hoy en día para hacer reinicios en línea es usar la funcionalidad
    `so_reuseport` y `peers`. Así puedes tener varios procesos de PgBouncer
    distintos ejecutándose en el mismo puerto. Luego, reiniciando esos procesos
    uno a uno, puedes asegurarte de que siempre haya un proceso de PgBouncer
    escuchando en el puerto deseado. ([#894])

- Funcionalidades
  * Introduce `track_extra_parameters`, que permite seguir más parámetros en
    modo de agrupación por transacciones. Antes, PgBouncer solo seguía
    `application_name`, `DateStyle`, `TimeZone` y
    `standard_conforming_strings`. Ahora PgBouncer también sigue `IntervalStyle` por
    defecto. Y cambiando `track_extra_parameters` puedes seguir aún más
    parámetros, pero solo [los que PostgreSQL comunica de vuelta al
    cliente][guc_report]. Si usas Citus 12.0+, Citus se asegurará
    de que PostgreSQL también comunique `search_path` de vuelta al cliente. Así que si usas
    Citus, puedes añadir `search_path` al parámetro `track_extra_parameters`.
    ([#867])
  * Reenvía el SQLSTATE en la fase de autenticación. Esto permite detectar
    que la base de datos no existe, algo que hace Npgsql (un proveedor de datos .NET
    para PostgreSQL). ([#814])
  * Cambia el valor predeterminado de `server_tls_sslmode` a `prefer`. ([#866])
  * Añade compatibilidad con el parámetro de inicio `options`. Esto permite usar [la
    variable de entorno `PGOPTIONS` que conocen `psql` y
    `libpq`][pgoptions]. Con esta variable puedes definir cualquier parámetro de PostgreSQL
    al inicio. Esto solo funciona para los parámetros de PostgreSQL que PgBouncer
    sigue a través de `track_extra_parameters`. ([#878])

- Correcciones
  * No se cae cuando la base de datos de administración `pgbouncer` se usa como
    auth_dbname. Sigue sin ser compatible, pero ahora esto da un error claro en lugar de caerse.
    ([#817])
  * Corrige el nombre de `peer_cache` en `SHOW MEM`. Antes aparecía
    incorrectamente como `db_cache`. ([#864])
  * Corrige la confusión de origen/destino en el registro. PgBouncer registraba una IP
    de origen cuando pretendía registrar la IP de destino. ([#880])
  * Solo registra las conexiones de administración por sockets unix cuando `log_connections`
    está definido en `1`. ([#883])

[guc_report]: https://www.postgresql.org/docs/15/protocol-flow.html#PROTOCOL-ASYNC
[pgoptions]: https://www.postgresql.org/docs/current/config-setting.html#id-1.6.7.4.5
[#867]: https://github.com/pgbouncer/pgbouncer/pull/867
[#814]: https://github.com/pgbouncer/pgbouncer/pull/814
[#866]: https://github.com/pgbouncer/pgbouncer/pull/866
[#878]: https://github.com/pgbouncer/pgbouncer/pull/878
[#817]: https://github.com/pgbouncer/pgbouncer/pull/817
[#864]: https://github.com/pgbouncer/pgbouncer/pull/864
[#880]: https://github.com/pgbouncer/pgbouncer/pull/880
[#883]: https://github.com/pgbouncer/pgbouncer/pull/883
[#894]: https://github.com/pgbouncer/pgbouncer/pull/894

--------

## PgBouncer 1.19.x {#pgbouncer-119x}

**2023-05-31  -  PgBouncer 1.19.1  -  « Primavera soleada »**

Esta es una versión menor que corrige algunos errores introducidos recientemente:

- Correcciones
  * Corrige: FATAL in function disconnect_client(): bad client state: 0 ([#846])
    (error introducido en la versión 1.18.0)
  * Corrige: FATAL in function server_proto(): server in bad state: 14 ([#849])
    (error introducido en la versión 1.18.0)
  * Añade al archivo tar de la versión los archivos necesarios para ejecutar las pruebas basadas en python ([#852])
    (las nuevas pruebas se introdujeron en la versión 1.19.0)

[#846]: https://github.com/pgbouncer/pgbouncer/pull/846
[#849]: https://github.com/pgbouncer/pgbouncer/pull/849
[#852]: https://github.com/pgbouncer/pgbouncer/pull/852

**2023-05-04  -  PgBouncer 1.19.0  -  « A la antigua, generado por humanos »**

- Funcionalidades
  * Añade la opción `auth_dbname`, que especifica en qué base de datos
    ejecutar la `auth_query`. ([#764])
  * Añade el comando `SHOW STATE`, que muestra si PgBouncer está
    activo, en pausa o suspendido. ([#528])
  * Añade compatibilidad con el peering entre procesos de PgBouncer.  Esto permite
    configurar PgBouncer de modo que las solicitudes de cancelación sigan
    funcionando cuando varios procesos de PgBouncer distintos están tras un
    único balanceador de carga. ([#666])
  * Añade un parámetro dedicado `cancel_wait_timeout`, que determina
    tras cuánto tiempo renunciar a reenviar una solicitud de cancelación.  El valor
    predeterminado es 10 segundos. ([#833])
  * Nuevo marco de pruebas ([#792])

- Correcciones
  * Corrige una posible fuga de memoria ante un fallo del handshake TLS. ([#796])
  * Da mensajes de error más precisos para las opciones de línea de comandos
    no compatibles en Windows. ([#620])
  * Corrige la llamada a `disconnect_server` sobre un servidor en estado
    `BEING_CANCELED`. ([#815]) (introducido en la versión 1.18.0)
  * No sale con un estado distinto de cero cuando se recibe un
    `SIGTERM`. ([#834])
  * Falla de forma contundente durante el inicio cuando no se pudo crear un socket en
    `unix_socket_dir`. ([#830])
  * Falla de forma contundente durante el inicio cuando no se pudo escuchar en
    ninguna de las direcciones de `listen_addr`. ([#838])
  * Da más mensajes de aviso con más información cuando
    falla `sbuf_connect`.  Esto es especialmente útil cuando falla la
    creación de sockets Unix. ([#837])

- Limpiezas
  * Varias actualizaciones del CI para mejorar el rendimiento
  * Se eliminó AppVeyor

[#528]: https://github.com/pgbouncer/pgbouncer/issues/528
[#620]: https://github.com/pgbouncer/pgbouncer/pull/620
[#666]: https://github.com/pgbouncer/pgbouncer/pull/666
[#764]: https://github.com/pgbouncer/pgbouncer/pull/764
[#792]: https://github.com/pgbouncer/pgbouncer/pull/792
[#796]: https://github.com/pgbouncer/pgbouncer/pull/796
[#815]: https://github.com/pgbouncer/pgbouncer/pull/815
[#830]: https://github.com/pgbouncer/pgbouncer/pull/830
[#833]: https://github.com/pgbouncer/pgbouncer/pull/833
[#834]: https://github.com/pgbouncer/pgbouncer/pull/834
[#837]: https://github.com/pgbouncer/pgbouncer/pull/837
[#838]: https://github.com/pgbouncer/pgbouncer/pull/838

--------

## PgBouncer 1.18.x {#pgbouncer-118x}

**2022-12-12  -  PgBouncer 1.18.0  -  « Sin misterio real »**

- Funcionalidades
  * Añade `application_name` a la salida de `SHOW CLIENTS`/`SERVERS`/`SOCKETS`
    ([#449](https://github.com/pgbouncer/pgbouncer/pull/449))
  * Añade información sobre solicitudes de cancelación a la salida de `SHOW CLIENTS`/`SERVERS`/`POOLS`
    ([#782](https://github.com/pgbouncer/pgbouncer/pull/782))

- Correcciones
  * Hace fallar la operación `sbuf_send_pending` si el socket de destino está cerrado
    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))
  * Corrige algunas caídas posibles
    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),
    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))
  * Corrección del error de desbordamiento en la funcionalidad de lista de hosts separados
    por comas, que provocaba que la conexión se redirigiera al socket Unix
    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))
  * No desaloja conexiones para alcanzar `min_pool_size`
    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))
  * Corrige `SHOW HELP` con PostgreSQL 15
    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))
  * Corrige una condición de carrera en el manejo de la cancelación de consultas.  Era posible
    que una cancelación de consulta de un cliente cancelara la consulta de
    otro.  Esto podía ocurrir cuando PgBouncer recibía una solicitud
    de cancelación cuando la consulta que debía cancelar ya había
    terminado por sí misma.
    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))

- Limpiezas
  * Varias actualizaciones del CI

--------

## PgBouncer 1.17.x {#pgbouncer-117x}

**2022-03-23  -  PgBouncer 1.17.0  -  « Se ha trazado una línea »**

- Funcionalidades
  * Una definición de base de datos puede especificar una lista de hosts separados
    por comas. Los hosts se conectarán de forma round-robin.
  * Al conectarse a una base de datos inexistente, el error ("no such
    database") ahora se informa después de la autenticación.  Esto evita
    que clientes no autenticados sondeen qué bases de datos existen.  (Esto
    es similar al cambio de la versión 1.15.0 de informar de usuarios
    inexistentes después de la autenticación.)
  * No envía errores de desconexión del servidor al cliente antes del inicio de
    sesión.  Esto podía revelar información no del todo pública, como
    detalles de configuración, a un cliente que aún no ha iniciado sesión.
  * Aumenta de nuevo la longitud máxima de las contraseñas.  Aparentemente,
    el último aumento no bastó durante mucho tiempo.
  * Elimina la recarga automática del `auth_file`.  El `auth_file` ahora
    se vuelve a leer solo al recargar el archivo de configuración, ya no
    automáticamente en cuanto cambia.
  * La compilación de Windows ahora incluye un archivo de recursos con
    información de versión.
  * Las compilaciones de Windows creadas en el CI ahora están enlazadas
    estáticamente, de modo que pueden usarse directamente sin requerir
    dependencias.

- Correcciones
  * Se ha corregido la compatibilidad con OpenSSL 3.  Las versiones anteriores se caían.
  * No aplica el fast-fail en el momento de la conexión.  Esto es parte del
    cambio mencionado anteriormente de no informar de errores del servidor antes
    de la autenticación.  También corrige una situación particular con la
    autenticación pass-through SCRAM, en la que necesitamos permitir el
    intercambio de autenticación del lado del cliente para poder reparar la
    conexión del lado del servidor reautenticando.  El mecanismo de
    fast-fail sigue aplicándose justo después de la autenticación, de modo que el
    comportamiento efectivo observado será el mismo en la mayoría de las situaciones.
  * Cambia `auth_type` en el `pgbouncer.ini` de ejemplo a `md5` para coincidir
    con el valor predeterminado integrado.  Algunos despliegan este archivo como
    archivo de configuración predeterminado, así que comprueba si esta configuración
    cambiada sigue teniendo sentido para ti.
  * Corrige una caída al salir en compilaciones con asserts activados.
  * Mejora la documentación y el comportamiento de `tcp_defer_accept`.  La
    documentación era incorrecta y engañosa sobre el valor predeterminado.  En
    algunos casos, el valor incorrecto se mostraba en "show config".  Además, si
    está definido pero no es compatible, da un error en lugar de ignorarlo, de
    forma similar a como se manejan otras opciones de socket específicas de la
    plataforma.
  * Corrige la compilación con c-ares en Windows.  Ahora se requiere
    c-ares >=1.18.0 en Windows.

- Limpiezas
  * Se han limpiado la mayoría de los avisos de obsolescencia de Autoconf >=2.70.
    Las versiones anteriores de Autoconf siguen siendo compatibles.
  * El uso de Cirrus CI se ha ampliado a más plataformas.
  * Se ha eliminado la compatibilidad con Travis CI.
  * Actualiza las ubicaciones donde buscar el archivo de CA raíz predeterminado,
    para cubrir más plataformas, como Fedora/RHEL/CentOS.
  * Los scripts de Python ahora usan todos `python3` por defecto.  La
    compatibilidad con Python 2 ya no se mantiene.
  * Los scripts de la suite de pruebas usan `command -v` en lugar de `which`,
    que está obsoleto.
  * Varios mensajes de error se han reformulado para dejar más claro a qué
    comando o parámetro de configuración se refieren.
  * Los scripts de la suite de pruebas ya no requieren GNU sed.
  * `make check` ahora funciona en Windows (pero todavía no la suite de
    pruebas SSL).
  * Documenta que la consola de administración solo es compatible con el
    protocolo de consulta simple, y da mejores mensajes de error al respecto.

--------

## PgBouncer 1.16.x {#pgbouncer-116x}

**2021-11-11  -  PgBouncer 1.16.1  -  « Prueba de profundidad contra eficiencia silenciosa »**

Esta es una versión menor con una corrección de seguridad.

* Hace que PgBouncer actuando como servidor rechace datos superfluos tras un
  handshake de cifrado SSL o GSS.

  Un hombre en el medio (man-in-the-middle) con la capacidad de inyectar datos
  en la conexión TCP podría introducir datos en texto claro al inicio de una
  sesión de base de datos supuestamente protegida por cifrado.  Esto podría
  aprovecharse para enviar comandos SQL falsificados al servidor, aunque eso solo
  funcionaría si PgBouncer no exigiera ningún dato de autenticación.
  (Sin embargo, una configuración de PgBouncer que dependa de la autenticación
  por certificado SSL bien podría no hacerlo.)  (CVE-2021-3935)

**2021-08-09  -  PgBouncer 1.16.0  -  « Ahuyentó a un jaguar »**

- Funcionalidades
  * Admite la recarga en caliente de la configuración TLS.  Cuando se recarga
    el archivo de configuración, los cambios en la configuración TLS surten
    efecto automáticamente.
  * Añade compatibilidad con sockets de dominio Unix abstractos.  Prefija una
    ruta de socket de dominio Unix con `@` para usar un socket en el espacio
    de nombres abstracto.  Esto coincide con la funcionalidad correspondiente
    de PostgreSQL 14.
  * Las longitudes máximas de las contraseñas y de los nombres de usuario se
    han aumentado a 996 y 128, respectivamente.  Varios servicios en la nube
    lo requieren.
  * El tamaño mínimo del pool ahora puede definirse por base de datos, de
    forma similar al tamaño normal del pool y al tamaño del pool de reserva.
  * El número de cancelaciones de consultas pendientes se muestra en `SHOW
    POOLS`.

- Correcciones
  * El análisis de la configuración ahora tiene un manejo de errores más
    estricto en muchos lugares.  Donde antes podía registrar un error y
    continuar, esos errores de configuración ahora provocan fallos de
    inicio.  Esto es lo que siempre debería haber ocurrido, pero parte del
    código no lo hacía bien.  Algunos usuarios podrían descubrir que sus
    configuraciones han sido defectuosas todo el tiempo y dejarán de
    funcionar.
  * Se ha corregido el manejo de la cancelación de consultas.  Bajo algunas
    circunstancias, las solicitudes de cancelación parecían quedarse
    atascadas durante mucho tiempo.  Esto ya no debería ocurrir.  De hecho,
    las solicitudes de cancelación ahora pueden superar el tamaño del pool
    en un factor de dos, así que realmente no deberían volverse a atascar.
    ([#542](https://github.com/pgbouncer/pgbouncer/pull/542),
    [#543](https://github.com/pgbouncer/pgbouncer/pull/543))
  * Se ha corregido el uso mixto de md5 y scram vía hba.
  * Se ha corregido la compilación con c-ares en Windows.
  * Se han corregido los temidos mensajes "FIXME: query end, but query_start == 0".
    Ahora sabemos por qué ocurrían, y no deberías volver a verlos.
    ([#565](https://github.com/pgbouncer/pgbouncer/pull/565))
  * Corrige la recarga de `default_pool_size`, `min_pool_size` y
    `reserve_pool_size`.  Recargar estos parámetros antes no funcionaba.

- Limpiezas
  * Ahora
    [se usa](https://cirrus-ci.com/github/pgbouncer/pgbouncer) Cirrus CI
    en lugar de Travis CI.
  * Como de costumbre, se han añadido muchas pruebas.
  * El mensaje de registro "unclean server" se ha aclarado un poco.  Ahora
    dice "client disconnect while server was not ready" o "client disconnect
    before everything was sent to the server".  El primero puede ocurrir si
    la conexión del cliente se cierra cuando el servidor tiene un bloque de
    transacción abierto, lo que confundía a algunos usuarios.
  * Ya no puedes usar "pgbouncer" como nombre de base de datos.  Este nombre
    está reservado para la consola de administración, y usarlo como nombre
    normal de base de datos nunca funcionó realmente bien.  Ahora está
    explícitamente prohibido.
  * Los errores enviados a los clientes antes de cerrar la conexión ahora se
    etiquetan como FATAL en lugar de solo ERROR.  De lo contrario, algunos
    clientes se confundían.
    ([#564](https://github.com/pgbouncer/pgbouncer/pull/564))
  * Corrige avisos del compilador con GCC 11.
    ([#623](https://github.com/pgbouncer/pgbouncer/issues/623))

--------

## PgBouncer 1.15.x {#pgbouncer-115x}

**2020-11-19  -  PgBouncer 1.15.0  -  « Todavía tengo una maleta en Berlín »**

- Funcionalidades
  * Mejora la notificación de fallos de autenticación.  Los mensajes de fallo
    de autenticación enviados al cliente ahora solo indican que la autenticación
    falló, sin dar más detalles.  Los detalles están disponibles en el registro
    de PgBouncer.  Además, si el usuario solicitado no existe, la autenticación
    se procesa hasta el final y dará como resultado el mismo mensaje de fallo
    genérico.  Todo esto evita que los clientes sondeen la instancia de
    PgBouncer en busca de nombres de usuario y otra información relacionada
    con la autenticación.  Esto es similar a cómo se comporta PostgreSQL.
  * No registra nada si el cliente se desconecta inmediatamente.  Esto evita
    el spam en el registro cuando los sistemas de monitorización solo abren
    una conexión TCP/IP pero no envían nada antes de desconectarse.
  * Usa el diario (journal) de systemd para el registro cuando esté en uso.
    Cuando detectamos que stderr va al diario de systemd, usamos funciones
    nativas de systemd para la salida del registro.  Esto evita duplicar la impresión
    de la marca de tiempo y del pid, haciendo así el registro algo más
    limpio.  Además, esto añade metadatos como la severidad a los registros,
    de modo que si el diario se envía a syslog, los mensajes llevan
    metadatos útiles adjuntos.
  * Un subconjunto de la suite de pruebas ahora puede ejecutarse en Windows.
  * `SHOW CONFIG` ahora también muestra los valores predeterminados de los
    parámetros.

- Correcciones
  * Corrige la opción `so_reuseport` en FreeBSD.  El código original de
    PgBouncer 1.12.0 en realidad no funcionaba en FreeBSD.
    ([#504](https://github.com/pgbouncer/pgbouncer/pull/504))
  * Repara la compilación en sistemas con versiones antiguas de systemd.  Esto
    se rompió en 1.14.0.
    ([#505](https://github.com/pgbouncer/pgbouncer/issues/505))
  * Se ha reparado el objetivo del makefile para construir paquetes zip con
    binarios de Windows.
  * Las opciones largas de línea de comandos ahora también funcionan en
    Windows.
  * Corrige el comportamiento del parámetro global `auth_user`.  El
    comportamiento antiguo era confuso y frágil, ya que dependía del orden en
    el archivo de configuración.  Esto ya no ocurre.
    ([#391](https://github.com/pgbouncer/pgbouncer/issues/391),
    [#393](https://github.com/pgbouncer/pgbouncer/issues/393))

- Limpiezas
  * Mejora la estabilidad y portabilidad de las pruebas.
  * Moderniza el código relacionado con Autoconf.
  * Desactiva los avisos de obsolescencia del compilador procedentes de
    OpenSSL 3.0.0.

--------

## PgBouncer 1.14.x {#pgbouncer-114x}

**2020-06-11  -  PgBouncer 1.14.0  -  « La magia redescubierta »**

- Funcionalidades
  * Añade pass-through de autenticación SCRAM.  Esto permite usar secretos
    SCRAM cifrados en PgBouncer (ya sea en `userlist.txt` o desde
    `auth_query`) para iniciar sesión en los servidores.
  * Añade compatibilidad con la activación de sockets de systemd.  Esto es
    especialmente útil para dejar que systemd gestione la creación de los
    sockets de dominio Unix en sistemas donde el acceso a
    `/var/run/postgresql` está restringido.
  * Añade compatibilidad con sockets de dominio Unix en Windows.

- Limpiezas
  * Añade un archivo de configuración de ejemplo alternativo más pequeño,
    `pgbouncer-minimal.ini`, para pruebas o despliegue.

--------

## PgBouncer 1.13.x {#pgbouncer-113x}

**2020-04-27  -  PgBouncer 1.13.0  -  « Mi juego favorito »**

- Funcionalidades
  * Añade el parámetro de configuración `tcp_user_timeout`, para definir la
    opción de socket correspondiente.
  * `client_tls_protocols` y `server_tls_protocols` ahora tienen el valor
    predeterminado `secure`, lo que significa que solo TLS 1.2 y TLS 1.3
    están activados.  Las versiones anteriores siguen siendo compatibles,
    simplemente no se activan por defecto.
  * Añade compatibilidad con las notificaciones de servicio de systemd.  Por
    ahora, esto permite usar unidades de servicio `Type=notify`.  Hay más
    integraciones previstas para versiones futuras.

- Correcciones
  * Corrige los mensajes de registro multilínea
    ([libusual #24](https://github.com/libusual/libusual/pull/24))
  * Maneja correctamente los nombres de usuario nulos devueltos por
    `auth_query`
    ([#340](https://github.com/pgbouncer/pgbouncer/pull/340))

- Limpiezas
  * Se han eliminado los archivos de empaquetado de Debian bajo `debian`.  Se
    recomienda usar los paquetes de https://apt.postgresql.org/.
  * Numerosas correcciones y mejoras en la suite de pruebas
  * Las pruebas ya no intentan usar sudo por defecto.  Ahora puede activarse
    explícitamente definiendo la variable de entorno
    `USE_SUDO`.
  * El uso de la API de libevent se actualizó para usar interfaces de estilo
    versión 2 y dejar de usar interfaces obsoletas de la versión 1.

--------

## PgBouncer 1.12.x {#pgbouncer-112x}

**2019-10-17  -  PgBouncer 1.12.0  -  « Se trata de aprender y mejorar »**

Esta versión contiene una variedad de pequeñas mejoras y correcciones.

- Funcionalidades
  * Añade un parámetro para activar la opción de socket `SO_REUSEPORT`.  En
    algunos sistemas operativos, esto permite ejecutar varias instancias de
    PgBouncer en el mismo host escuchando en el mismo puerto y dejar que el
    núcleo distribuya las conexiones automáticamente.
  * Añade un parámetro para usar un archivo `resolv.conf` separado del
    sistema operativo.  Esto permite definir servidores DNS personalizados y
    quizá otras opciones de DNS.
  * Envía la salida de `SHOW VERSION` como una fila de resultado normal en
    lugar de un mensaje NOTICE.  Esto facilita su consumo y es consistente
    con otros comandos `SHOW`.

- Correcciones
  * Envía las columnas de estadísticas como `numeric` en lugar de `bigint`.
    Esto evita que algunas bibliotecas cliente fallen con valores que
    desbordan el rango de `bigint`.
    ([#360](https://github.com/pgbouncer/pgbouncer/pull/360),
    [#401](https://github.com/pgbouncer/pgbouncer/pull/401))
  * Corrige un problema con usuarios PAM que perdían su
    contraseña. ([#285](https://github.com/pgbouncer/pgbouncer/issues/285))
  * Acepta clientes con channel binding SCRAM activado.  Antes, un
    cliente con soporte de channel binding (es decir, PostgreSQL 11+)
    obtenía un fallo de conexión al conectarse a PgBouncer en ciertas
    situaciones.  (PgBouncer no es compatible con channel binding.  Este
    cambio solo corrige el soporte para los clientes que lo ofrecen.)
  * Corrige la compilación con versiones más recientes de musl-libc (usada
    por Alpine Linux).

- Limpiezas
  * Añade el objetivo `make check`.  Esto permite ejecutar todas las pruebas
    con un solo comando.
  * Elimina las referencias a la wiki de PostgreSQL.  Toda la información
    está ahora en la documentación de PgBouncer o en el sitio web.
  * Elimina la compatibilidad con Libevent versión 1.x.  Ahora se requiere
    Libevent 2.x.  Libevent ahora se detecta usando pkg-config.
  * Corrige avisos del compilador en macOS y Windows.  La compilación en
    estas plataformas debería estar ahora libre de avisos.
  * Corrige algunos avisos de LLVM scan-build.

--------

## PgBouncer 1.11.x {#pgbouncer-111x}

**2019-08-27  -  PgBouncer 1.11.0  -  « Instinto de grandeza »**

- Funcionalidades
  * Añade compatibilidad con la autenticación SCRAM para clientes y
    servidores.  Se añade un nuevo tipo de autenticación
    `scram-sha-256`.
  * Maneja `auth_type=password` cuando la contraseña almacenada es md5, como
    lo haría un servidor
    PostgreSQL. ([#129](https://github.com/pgbouncer/pgbouncer/pull/129))
  * Añade la opción `log_stats` para desactivar la impresión de estadísticas
    en el registro. ([#287](https://github.com/pgbouncer/pgbouncer/pull/287))
  * Añade la zona horaria a las marcas de tiempo del registro.
  * Pone el PID entre [corchetes] en el prefijo del registro.
- Correcciones
  * Corrige la prueba de configure de OpenSSL al ejecutarse contra OpenSSL
    más reciente con `-Werror`.
  * Corrige el cálculo del tiempo de espera con `auth_user`.  Esto provocaba
    una caída o informaba de valores basura para el tiempo de
    espera. ([#393](https://github.com/pgbouncer/pgbouncer/pull/393))
  * Maneja el paquete GSSENCRequest, añadido en PostgreSQL 12.  Por ahora no
    hace nada, pero evita mensajes de error confusos sobre "bad packet
    header".
- Limpiezas
  * Muchas mejoras en la suite de pruebas y varias pruebas nuevas
  * Corrige varios avisos del compilador en Windows.
  * Amplía la documentación de la sección `[users]` y la añade al archivo de
    configuración de
    ejemplo. ([#330](https://github.com/pgbouncer/pgbouncer/pull/330))

--------

## PgBouncer 1.10.x {#pgbouncer-110x}

**2019-07-01  -  PgBouncer 1.10.0  -  « Miedo al mundo »**

- Funcionalidades
  * Añade compatibilidad con activar y desactivar TLS 1.3.  (TLS 1.3 ya era
    compatible, dependiendo de la biblioteca OpenSSL, pero ahora los
    parámetros de configuración para elegir las versiones del protocolo TLS
    también lo admiten.)
- Correcciones
  * Corrige la compatibilidad con TLS 1.3.  Estaba rota con OpenSSL 1.1.1 y
    1.1.1a (pero no antes ni después).
  * Corrige una caída poco frecuente en `SHOW FDS`
    ([#311](https://github.com/pgbouncer/pgbouncer/issues/311)).
  * Corrige un problema que podía llevar a un tiempo de inactividad
    prolongado si llegan muchas solicitudes de cancelación
    ([#329](https://github.com/pgbouncer/pgbouncer/issues/329)).
  * Evita "unexpected response from login query" tras un reload de
    postgres
    ([#220](https://github.com/pgbouncer/pgbouncer/issues/220)).
  * Corrige el cálculo de `idle_transaction_timeout`
    ([#125](https://github.com/pgbouncer/pgbouncer/issues/125)).  El error
    provocaba tiempos de espera prematuros en situaciones específicas.
- Limpiezas
  * Hace más precisos varios mensajes de registro y de error.
  * Corrige problemas encontrados por Coverity (ninguno tenía un impacto
    significativo en la práctica).
  * Mejora y documenta todos los scripts de pruebas.
  * Añade comandos SHOW adicionales a la documentación.
  * Convierte la documentación de rst a Markdown.
  * Los scripts de Python del árbol de fuentes ahora son todos compatibles
    con Python 3.

--------

## PgBouncer 1.9.x {#pgbouncer-19x}

**2018-08-13  -  PgBouncer 1.9.0  -  « Supervivencia en el caos »**

- Funcionalidades
  * Comando RECONNECT
  * Comando WAIT_CLOSE
  * Cierre rápido: desconecta de inmediato un servidor en modo de pool por
    sesiones si está en modo "close_needed" (reconexión).
  * Añade la columna close_needed a SHOW SERVERS
- Correcciones
  * Evita un double-free en parse_filename
  * Evita una desreferencia de puntero NULL en parse_line
- Limpiezas
  * Porta mkauth.py a Python 3
  * Mejora la documentación de las señales
  * Mejora la documentación de inicio rápido
  * Documenta el comando SET
  * Corrige la lista de software requerido
  * Corrige los avisos -Wimplicit-fallthrough
  * Añade la documentación faltante de varios campos de SHOW
  * Documenta el comportamiento de reconexión ante reload y cambios de DNS
  * Documenta que KILL requiere RESUME después
  * Aclara la documentación de server_lifetime
  * Correcciones de erratas y mayúsculas en mensajes y documentación
  * Corrige la invocación de psql en las pruebas
  * Otras mejoras diversas en la configuración de pruebas

--------

## PgBouncer 1.8.x {#pgbouncer-18x}

**2017-12-20  -  PgBouncer 1.8.1  -  « Mentalidad de ground-and-pound »**

- Correcciones
  * Incluye el archivo `include/pam.h` en el archivo tar de distribución.  Esto
    impedía por completo la compilación del archivo tar de 1.8.

**2017-12-19  -  PgBouncer 1.8  -  « Confiado al timón »**

- Funcionalidades
  * Admite la autenticación PAM.  (Actívala con `--with-pam`.)
  * Añade los campos `paused` y `disabled` a la salida de `SHOW DATABASES`.
  * Añade el campo `maxwait_us` a la salida de `SHOW POOLS`.
  * Añade los campos `wait` y `wait_us` a la salida de los comandos `SHOW`.
  * Añade los nuevos comandos `SHOW STATS_TOTALS` y `SHOW STATS_AVERAGES`.
  * Sigue consultas y transacciones por separado en `SHOW STATS`.  Los
    campos `total_requests`, `avg_req` y
    `avg_query` se han sustituido por campos nuevos.
  * Añade `wait_time` a `SHOW STATS`.
- Correcciones
  * El libusual actualizado es compatible con OpenSSL 1.1.
  * No intenta usar TLS en sockets Unix.
  * Al analizar `pg_hba.conf`, sigue analizando tras las líneas erróneas en
    lugar de rechazar el archivo completo.
    ([#118](https://github.com/pgbouncer/pgbouncer/issues/118))
  * Varias otras correcciones del análisis de hba.
  * Corrige una condición de carrera al cancelar una consulta.
    ([#141](https://github.com/pgbouncer/pgbouncer/issues/141))
- Limpiezas
  * El parámetro `auth_user` ahora también se permite globalmente, no solo
    por base de datos.
    ([#142](https://github.com/pgbouncer/pgbouncer/issues/142))
  * Define la codificación de cliente y servidor de la consola en `UTF8`.

--------

## PgBouncer 1.7.x {#pgbouncer-17x}

**2016-02-26  -  PgBouncer 1.7.2  -  « Por fin en vuelo »**

- Correcciones
  * Corrige una caída al eliminar un pidfile obsoleto.  Problema introducido
    en 1.7.1.
  * Desactiva la limpieza: rompe la toma de control y no es útil
    para cargas de producción.  Problema introducido en 1.7.1.
  * Tras la toma de control, espera a que el pidfile desaparezca antes de
    arrancar.  El apagado lento debido a la limpieza de memoria expuso una
    condición de carrera existente.
    ([#113](https://github.com/pgbouncer/pgbouncer/issues/113))
- Limpiezas
  * Hace la compilación reproducible eliminando el manejo de DBGVER.
    ([#112](https://github.com/pgbouncer/pgbouncer/issues/112))
  * Antimake: ordena la lista de archivos de $(wildcard); el gmake más
    reciente ya no la ordena.
    ([#111](https://github.com/pgbouncer/pgbouncer/issues/111))
  * Muestra la versión de libssl en el registro.
  * deb: activa el endurecimiento completo.

**2016-02-18  -  PgBouncer 1.7.1  -  « Reenvía a cinco amigos o si no... »**

AVISO: desde la versión 1.7, `server_reset_query` no se ejecuta cuando
la base de datos está en modo de agrupación por transacciones.  Parece que
esto no se destacó lo suficiente en el anuncio de 1.7.  Si tus aplicaciones
dependen de que eso ocurra, usa `server_reset_query_always` para restaurar
el comportamiento anterior.

Por lo demás, el trabajo principal de esta versión fue rastrear una fuga de
memoria relacionada con TLS, que resultó no existir.  En su lugar, hay una
compilación de libssl en Debian/wheezy con 600k de sobrecoste por conexión
(sin fugas) en lugar de los 20-30k esperados.  Algo que conviene vigilar
al usar TLS.

- Correcciones
  * TLS: cambia el nombre del sslmode "disabled" a "disable", que es lo que
    usa PostgreSQL.
  * TLS: `client_tls_sslmode=verify-ca/-full` ahora rechaza
    conexiones sin certificado de cliente.
    ([#104](https://github.com/pgbouncer/pgbouncer/issues/104))
  * TLS: `client_tls_sslmode=allow/require` sí validan el
    certificado de cliente si se envía.  Antes dejaban la validación del
    certificado sin configurar, de modo que las conexiones con certificado
    de cliente fallaban.
    ([#105](https://github.com/pgbouncer/pgbouncer/issues/105))
  * Corrige una fuga de memoria al liberar una base de datos.
  * Corrige una posible fuga de memoria en tls_handshake().
  * Corrige el manejo de EOF en tls_handshake().
  * Corrige un memset demasiado pequeño en el compat de asn1_time_parse.
  * Corrige la compilación sin TLS (`--without-openssl`).
    ([#101](https://github.com/pgbouncer/pgbouncer/issues/101))
  * Corrige varios problemas con la compilación de Windows.
    ([#100](https://github.com/pgbouncer/pgbouncer/issues/100))
- Limpiezas
  * TLS: usa SSL_MODE_RELEASE_BUFFERS para disminuir el uso de memoria
    de las conexiones inactivas.
  * Limpia la memoria asignada al salir.  Ayuda a ejecutar comprobadores
    de fugas de memoria.
  * Mejora la documentación de `server_reset_query`.
    ([#110](https://github.com/pgbouncer/pgbouncer/issues/110))
  * Añade opciones TLS al archivo de configuración de ejemplo.

**2015-12-18  -  PgBouncer 1.7  -  « Los colores varían tras la resurrección »**

- Funcionalidades
  * Admite conexiones TLS.  Se usa OpenSSL/LibreSSL
    como implementación de backend.
  * Admite la autenticación mediante certificado de cliente TLS.
  * Admite la autenticación "peer" en sockets Unix.
  * Admite archivo de control de acceso basado en hosts, como el
    [pg_hba.conf](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
    de Postgres.  Esto permite configurar TLS para las conexiones de red y
    autenticación "peer" para las conexiones locales.
- Limpiezas
  * Define `query_wait_timeout` en 120s por defecto.  El valor predeterminado
    actual (0) provoca una cola infinita, lo cual no es útil.  Eso
    significa que si un cliente tiene una consulta pendiente y no se le ha
    asignado una conexión de servidor, la conexión del cliente se
    descartará.
  * Desactiva `server_reset_query_always` por defecto.  Ahora la consulta
    de reinicio se usa solo en pools que están en modo de sesiones.
  * Aumenta pkt_buf a 4096 bytes.  Mejora el rendimiento con TLS.
    El comportamiento probablemente dependa de la carga, pero debería ser
    seguro hacerlo, ya que desde v1.2 los búferes de paquetes están separados
    de las conexiones y se usan perezosamente desde el pool.
  * Admite el conteo de paquetes ReadyForQuery esperados en pipelining.
    Esto evita liberar el servidor demasiado pronto.  Corrige
    [#52](https://github.com/pgbouncer/pgbouncer/issues/52).
  * Lógica de sbuf_loopcnt mejorada: se garantiza que el socket se reprocese
    incluso si no hay eventos del socket.
    Necesario para TLS, ya que tiene su propio búfer.
  * Adapta las pruebas del sistema para funcionar con BSD y MacOS modernos.
    (Eric Radman)
  * Elimina la autenticación **crypt**.  Es obsoleta y PostgreSQL no la
    admite desde 8.4.
  * Corrige la opción de configure simple "--with-cares": sin argumento
    estaba rota.

--------

## PgBouncer 1.6.x {#pgbouncer-16x}

**2015-09-03  -  PgBouncer 1.6.1  -  « El público del estudio lo aprueba »**

- Funcionalidades
  * Nuevo parámetro: `server_reset_query_always`.  Cuando se define,
    desactiva el uso de `server_reset_query` en pools que no son de
    sesiones.  PgBouncer introduce pool_mode por pool, pero la agrupación
    por sesiones y la agrupación por transacciones no deberían usar la
    misma consulta de reinicio.  De hecho, la agrupación por transacciones
    no debería usar ninguna consulta de reinicio.

    Está activado en 1.6.x, pero se desactivará en 1.7.

- Correcciones
  * [SEGURIDAD]  Elimina la asignación no válida de `auth_user`. (#69)
    Cuando `auth_user` está definido y el cliente solicita un nombre de
    usuario inexistente, el cliente iniciará sesión como `auth_user`.  Nada
    bueno.

    [CVE-2015-6817](https://access.redhat.com/security/cve/cve-2015-6817)

  * Omite NoticeResponse en handle_auth_response.  De lo contrario, los
    niveles de registro detallados en el servidor provocan fallos de inicio
    de sesión.

  * consola: rellena `auth_user` cuando auth_type=any.  De lo contrario,
    el registro puede caerse (#67).

  * Varias correcciones de portabilidad (OpenBSD, Solaris, OSX).

**2015-08-01  -  PgBouncer 1.6  -  « Zombis del futuro »**

- Funcionalidades

  * Carga el hash de la contraseña del usuario desde la base de datos
    postgres.  Nuevos parámetros:

    auth_user
        usuario con el que conectarse a la misma base de datos y obtener información del usuario.
        También puede definirse por base de datos.

    auth_query
        Consulta SQL que se ejecuta con auth_user.
        Predeterminado: "SELECT usename, passwd FROM pg_shadow WHERE usename=$1"

    (Cody Cutrer)

  * El modo de agrupación puede configurarse tanto por base de datos como
    por usuario.
    (Cody Cutrer)

  * Límites de conexiones por base de datos y por usuario:
    max_db_connections y max_user_connections.
    (Cody Cutrer / Pavel Stehule)

  * Añade los comandos DISABLE/ENABLE para evitar nuevas conexiones.
    (William Grant)

  * Nuevo backend de DNS: c-ares.  El único backend de DNS que admite todas
    las funcionalidades interesantes:  /etc/hosts con actualización, búsqueda
    SOA, respuestas grandes (vía TCP/EDNS+UDP), IPv6.  Es el backend preferido
    ahora, y probablemente será el **único** backend en el futuro,
    ya que no tiene sentido mantener un zoológico de bibliotecas inadecuadas.

    SNAFU: las versiones de c-ares <= 1.10 tienen un error que rompe el
    soporte de CNAME-s cuando IPv6 ha sido activado.  (Corregido en
    upstream.)  Como solución, c-ares <= 1.10 se usa solo con IPv4.  Así que
    PgBouncer abandonará los demás backends
    solo cuando c-ares >1.10 (todavía sin publicar) haya estado disponible
    algún tiempo...

  * Muestra remote_pid en SHOW CLIENTS/SERVERS.  Disponible para los clientes
    que se conectan por sockets unix y para servidores tanto por tcp como
    por socket unix.  En el caso de un servidor tcp, el pid se toma de la
    clave de cancelación.

  * Añade un parámetro de configuración separado (dns_nxdomain_ttl) para
    controlar el caché negativo de DNS.
    (Cody Cutrer)

  * Añade la dirección IP y el puerto del host del cliente a
    application_name.  Esto se activa con el parámetro de configuración
    application_name_add_host, que por defecto está en 'off'.
    (Andrew Dunstan)

  * Los archivos de configuración tienen la directiva '%include FILENAME'
    para permitir dividir la configuración en varios archivos.
    (Andrew Dunstan)

- Limpiezas

  * log: envuelve la dirección ipv6 con []
  * log: al conectar con el servidor, muestra la ip y el puerto locales
  * win32: usa el estilo gnu para los argumentos largos: --foo
  * Permite números en el nombre de host; siempre intenta analizar con
    inet_pton
  * Corrige deallocate_all() en las preguntas frecuentes
  * Corrige una palabra clave incorrecta en el archivo de configuración de
    ejemplo
    (Magnus Hagander)
  * Permite comentarios (con ';') en los archivos de autenticación.
    (Guillaume Aubert)
  * Corrige errores ortográficos en mensajes de registro y comentarios.
    (Dmitriy Olshevskiy)

- Correcciones

  * corrige el lanzamiento de nuevas conexiones durante el mantenimiento
    (Cody Cutrer)
  * no carga el archivo de autenticación dos veces al arrancar
    (Cody Cutrer)
  * Invalidación correcta para las autodbs
  * ipv6: define IPV6_V6ONLY en el socket de escucha.
  * win32: no define SO_REUSEADDR en el socket de escucha.
  * Corrige el memcpy de direcciones IPv6
  * Corrige la cancelación de clientes en espera.
    (Mathieu Fenniak)
  * Pequeña corrección de un error: hay que comprobar el resultado de calloc
    (Heikki Linnakangas)
  * Añade un salto de línea al final del archivo de PID
    (Peter Eisentraut)
  * No permite nuevas conexiones de servidor cuando se emitió PAUSE <db>.
    (Petr Jelinek)
  * Corrige el 'bad packet' durante el inicio de sesión cuando la cabecera
    llega con retraso.
    (Michał Trojnara, Marko Kreen)
  * Corrige errores detectados por Coverity.
    (Euler Taveira)
  * Desactiva server_idle_timeout cuando el número de servidores baja de
    min_pool (#60)
    (Marko Kreen)

--------

## PgBouncer 1.5.x {#pgbouncer-15x}

**2015-04-09  -  PgBouncer 1.5.5  -  « Hazte el muerto para ganar »**

- Correcciones
  * Corrige una caída remota: un orden de paquetes no válido provoca la
    búsqueda de un puntero NULL.  No explotable, solo DoS.

**2012-11-28  -  PgBouncer 1.5.4  -  « Sin fugas, entrenamiento para ir al baño con éxito »**

- Correcciones
  * DNS: corrige una fuga de memoria en el backend getaddrinfo_a().
  * DNS: corrige una fuga de memoria en el backend udns.
  * DNS: corrige el cálculo de estadísticas.
  * DNS: mejora el manejo de mensajes de error para getaddrinfo_a().
  * Corrige la compilación en win32.
  * Corrige la comprobación de soporte de dependencias del compilador en
    configure.
  * Algunas correcciones en la documentación.

**2012-09-12  -  PgBouncer 1.5.3  -  « Tostadora cuántica »**

- Corrección crítica

  * Los nombres de base de datos demasiado largos pueden provocar una
    caída, que es desencadenable de forma remota si las autodbs están
    activadas.

    Las comprobaciones originales asumían que todos los nombres venían de
    archivos de configuración, por lo que usar fatal() estaba bien, pero
    cuando las autodbs están activadas
    - mediante '*' en la sección [databases] - el nombre de la base de datos
    puede venir de la red, haciendo así
    posible un apagado remoto.

    [CVE-2012-4575](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-4575)

- Funcionalidades menores

  * max_packet_size: parámetro de configuración para ajustar el tamaño
    máximo de paquete que se permite pasar.  El valor predeterminado se
    mantiene igual: (2G-1), pero ahora puede hacerse más pequeño.
  * En caso de cabecera de paquete no analizable, mostrarla en hexadecimal
    en el registro y en el mensaje de error.

- Correcciones

  * AntiMake: usaba $(relpath) y $(abspath) para manipular nombres de
    rutas, pero el resultado era un fallo de compilación cuando la ruta del
    árbol de fuentes contenía enlaces simbólicos.  El código ahora se ha
    cambiado para trabajar solo con cadenas simples.
  * consola: ahora SET puede usarse para definir valores de cadena vacía.
  * config.txt: mostrar que todos los tiempos de espera pueden definirse
    en decimales.  Es una funcionalidad bien escondida introducida en 1.4.

**2012-05-29  -  PgBouncer 1.5.2  -  « No mastiques, solo traga »**

- Correcciones
  * Debido a un error, reserve_pool_timeout se tomaba en microsegundos,
    no en segundos, activando efectivamente el pool de reserva
    inmediatamente cuando el pool se llenaba.  Ahora se usa como segundos,
    como se pretendía.
    (Advertido por Keyur Govande)

**2012-04-17  -  PgBouncer 1.5.1  -  « ¿Anular, Reintentar, Omitir? »**

- Funcionalidades
  * Parámetros para ajustar los permisos del socket unix:
    unix_socket_mode=0777, unix_socket_group=''.
- Correcciones
  * Permite la cadena vacía para la variable del lado del servidor; esto es
    necesario para que "application_name" funcione correctamente, ya que es
    el único parámetro que no tiene un valor predeterminado del lado del
    servidor.
  * Si la cadena de conexión cambia, exige la actualización de los
    parámetros del servidor.  Antes PgBouncer continuaba con los parámetros
    antiguos, lo que se rompe en caso de una actualización de Postgres.
  * Si cambia la cadena de conexión de una autodb, descarta las conexiones
    antiguas.
  * cf_setint: usa strtol() en lugar de atoi() para analizar parámetros de
    configuración enteros.  Permite hex, octal y mejor detección de errores.
  * Usa sigqueue() para detectar la existencia de union sigval: corrige
    la compilación en HPUX.
  * Elimina el comando 'git' del Makefile: lanza errores aleatorios
    en caso de una compilación a partir del tarball simple.
  * Documenta el parámetro stats_period.  Ajusta el período de la
    salida de estadísticas.
  * Requiere Asciidoc >= 8.4; parece que la documentación ya no es
    compatible con versiones anteriores.
  * Deja de reintentar ante EINTR de close().

**2012-01-05  -  PgBouncer 1.5  -  « Rebotando clientes satisfechos desde 2007 »**

Si usas más de 8 IP detrás de un nombre DNS, ahora necesitas
usar el protocolo EDNS0 para consultar.  Solo los backends
getaddrinfo_a()/getaddrinfo() y UDNS lo admiten; libevent 1.x/2.x no.
Para activarlo en libc, añade 'options edns0' a /etc/resolv.conf.

Se requiere GNU Make 3.81+ para compilar.

- Funcionalidades
  * Detecta cambios en las respuestas DNS e invalida las conexiones a IP
    que ya no estén presentes en la última respuesta.
    (Petr Jelinek)
  * Invalidación de nombres de host basada en el número de serie de la
    zona DNS.  Cuando la opción dns_zone_check_period está definida, se
    consultará el SOA de todas las zonas DNS y, cuando el número de serie
    haya cambiado, se consultarán todos los nombres de host.  Esto es
    necesario para obtener una invalidación de conexiones determinista,
    porque la invalidación en la búsqueda es inútil cuando no se realizan
    búsquedas.  Funciona solo con el nuevo backend UDNS.
  * Nuevos comandos SHOW DNS_HOSTS y SHOW DNS_ZONES para examinar la
    caché de DNS.
  * Nuevo parámetro: min_pool_size; evita descartar todas las conexiones
    cuando no hay carga.
    (Filip Rembiałkowski)
  * idle_in_transaction_timeout: termina la transacción si está inactiva
    demasiado tiempo.  No definido por defecto.
  * Nuevo backend libudns para las búsquedas DNS.  Con más funcionalidades
    que evdns.  Usa --with-udns para activarlo.  Todavía no funciona con
    IPv6.
  * Comando KILL, para terminar de inmediato todas las conexiones de una
    base de datos.
    (Michael Tharp)
  * Pasa al sistema de compilación Antimake para tener Makefiles de mejor
    aspecto.  Ahora se requiere GNU Make 3.81+ para compilar.
- Correcciones
  * DNS ahora funciona con nombres de host IPv6.
  * No cambia el estado de la conexión cuando llega un NOTIFY del
    servidor.
  * Varias correcciones en la documentación.
    (Dan McGee)
  * Consola: admite el entrecomillado de identificadores con "".  Al
    principio no teníamos ningún comando que tomara nombres de bases de
    datos, así que no hacía falta entrecomillado.
  * Consola: permite números al inicio de la expresión regular de
    palabra.  Intentar usar un analizador estricto complica demasiado las
    cosas aquí.
  * No expira las BD automáticas que están en pausa.
    (Michael Tharp)
  * Crea bases de datos automáticas según haga falta al ejecutar PAUSE.
    (Michael Tharp)
  * Corrige el mensaje de registro incorrecto emitido por el comando
    RESUME.
    (Peter Eisentraut)
  * Cuando user= sin password= está en la cadena de conexión de la base
    de datos, la contraseña se tomará de userlist.
  * Analiza '*' correctamente en el código de toma de control.
  * autogen.sh: funciona con autoconf/automake antiguos.
  * Corrige la caída de run-as-service en win32 debida a un basename()
    defectuoso del runtime mingw/msvc.  Ahora siempre se usa el basename()
    de compat.

--------

## PgBouncer 1.4.x {#pgbouncer-14x}

**2011-06-16  -  PgBouncer 1.4.2  -  « Algoritmo de golpear primero »**

Sistemas operativos afectados: \*BSD, Solaris, Win32.

- Correcciones de portabilidad
  * Da los CFLAGS al enlazador.  Necesario cuando se usa el fallback
    getaddrinfo_a() basado en pthread.
  * lib/find_modules.sh: sustituye split() por index()+substr().
    Esto debería hacerlo funcionar con AWK antiguos.
  * <usual/endian.h>: ignora las definiciones htoX/Xtoh del sistema.  Puede
    que solo haya un subconjunto de macros definidas.
  * <usual/signal.h>: separa el sigval de compat del sigevent de compat
  * <usual/socket.h>: incluye <sys/uio.h> para obtener iovec
  * <usual/time.h>: mejor autodetección de funciones en win32
  * <usual/base_win32.h>: elimina la declaración duplicada de
    sigval/sigevent

**2011-04-01  -  PgBouncer 1.4.1  -  « Todo era un acto »**

- Funcionalidades

  * Admite escucha/conexión para direcciones IPv6.
    (Hannu Krosing)
  * Varias direcciones de escucha en 'listen_addr'.  Por cada una se llama
    a getaddrinfo(), así que también pueden usarse nombres.
  * consola: envía la versión de PgBouncer como 'server_version' al
    cliente.

- Correcciones importantes

  * Desactiva getaddrinfo_a() en glibc < 2.9, ya que se cae en versiones
    anteriores.

    Sistemas operativos afectados notables: RHEL/CentOS 5.x (glibc 2.5),
    Ubuntu 8.04 (glibc 2.7).  También Debian/lenny (glibc 2.7), que tiene un
    getaddrinfo_a() que no se cae, pero no tenemos una buena forma de
    detectarlo.

    Usa libevent 2.x en esos sistemas operativos; el fallback
    getaddrinfo_a() no está pensado para sistemas de producción.  Y lee la
    nueva sección 'DNS lookup support' del README para ver cómo se elige el
    backend de DNS.

    (Hubert Depesz Lubaczewski, Dominique Hermsdorff, David Sommerseth)

  * Por defecto usa --enable-evdns si se usa libevent 2.x.

  * Activa tcp_keepalive por defecto, ya que eso también lo hace
    Postgres.
    (Hubert Depesz Lubaczewski)

  * Define el server_reset_query predeterminado en DISCARD ALL para ser
    compatible con Postgres por defecto.

  * win32: corrige caídas con una dirección de socket unix NULL.
    (Hiroshi Saito)

  * Corrige la limpieza de las autodb: el código antiguo de limpieza
    confundía bases de datos y pools: en cuanto se encontraba un pool
    vacío, la base de datos se marcaba como 'idle', potencialmente
    terminando más tarde una base de datos con usuarios activos.

    Reported-By: Hubert Depesz Lubaczewski

- Correcciones

  * Hace no bloqueante el getaddrinfo_a() de compat, usando un único hilo
    en paralelo para hacer las búsquedas.
  * Activa la compilación con pthread si se usa el getaddrinfo_a de
    compat.
  * release_server olvidaba definir ->last_lifetime_disconnect en una
    desconexión por tiempo de vida.
    (Emmanuel Courreges)
  * win32: corrige el archivo de autenticación con finales de línea DOS:
    load_file() no tenía en cuenta la reducción del archivo al
    cargarlo.
    (Rich Schaaf)
  * <usual/endian.h>: añade detección de autoconf para las funciones
    enc/dec, de modo que no cree conflictos en BSD.
    (James Pye)
  * No se cae cuando el archivo de configuración no existe.
    (Lou Picciano)
  * No se cae ante un fallo de búsqueda DNS cuando se registra en nivel
    de ruido (-v -v).
    (Hubert Depesz Lubaczewski, Dominique Hermsdorff)
  * Usa comillas inversas en lugar de $(cmd) en find_modules.sh para
    hacerlo más portable.
    (Lou Picciano)
  * Usa 'awk' en lugar de 'sed' en find_modules.sh para hacerlo más
    portable.
    (Giorgio Valoti)
  * Registra información del backend DNS asíncrono activo al arrancar.
  * Corrige --disable-evdns para que signifique 'no' en lugar de
    'yes'.
  * Menciona en la documentación que -R requiere unix_socket_dir.
  * Trata server_reset_query en faq.txt.
  * Restaura el memset perdido en el asignador slab
  * Varias correcciones de portabilidad menores en libusual.

**2011-01-11  -  PgBouncer 1.4  -  « Código gore »**

- Funcionalidades

  * Búsqueda DNS asíncrona: en lugar de resolver los nombres de host al
    recargar, los nombres ahora se resuelven al conectar, con caché
    configurable.  (Véase el parámetro dns_max_ttl.)

    Por defecto usa getaddrinfo_a() (glibc) como backend; si no existe,
    getaddrinfo_a() se emula mediante un getaddrinfo() bloqueante (!).

    Cuando se pasa el argumento --enable-evdns a configure, se usa evdns
    de libevent como backend.  No se usa por defecto, porque libevent
    1.3/1.4 contiene una implementación con errores.  Solo el evdns de
    libevent 2.0 parece correcto.

  * Nueva variable de configuración: syslog_ident, para ajustar el nombre
    de syslog.

  * Soporte adecuado del parámetro de inicio `application_name`.

  * Opciones largas de línea de comandos (Guillaume Lelarge)

  * Correcciones de portabilidad para Solaris (Hubert Depesz Lubaczewski)

  * Nueva variable de configuración: disable_pqexec.  Los entornos
    altamente paranoicos pueden desactivar con ello el protocolo de
    consulta simple.  Requiere aplicaciones que usen solo el protocolo de
    consulta extendida.

  * Compatibilidad con Postgres: si el nombre de la base de datos está
    vacío en el paquete de inicio, usa el nombre de usuario como base de
    datos.

- Correcciones

  * Los parámetros de servidor DateStyle y TimeZone necesitan usar
    mayúsculas y minúsculas exactas.
  * Consola: envía al cliente los parámetros de servidor datetime, timezone
    y stdstr.

- Limpiezas internas

  * Usa la biblioteca libusual para las funciones utilitarias de bajo
    nivel.
  * Elimina el límite de longitud fija de los parámetros del servidor.

--------

## PgBouncer 1.3.x {#pgbouncer-13x}

**2010-09-09  -  PgBouncer 1.3.4  -  « El bouncer siempre tiene razón »**

- Correcciones
  * Aplica la lógica de fallo rápido en el momento de la conexión.  Así,
    si el servidor está fallando, los clientes reciben un error al
    conectar.
  * No marca las bases de datos generadas automáticamente para
    comprobación al recargar; de lo contrario se terminan, porque no
    existen en la configuración.
  * Ignora el parámetro application_name por defecto.  Esto evita que
    todos los usuarios de Postgres 9.0 tengan que añadirlo ellos mismos a
    ignore_startup_parameters=.
  * Corrige el entrecomillado de pg_auth.  Allí no se usa '\'.
  * Mejor notificación de errores en la consola: muestra al usuario la
    consulta entrante.
  * Admite sistemas operativos (OpenBSD) donde tv_sec no es time_t.
  * Evita avisos demasiado ruidosos en gcc 4.5.

**2010-05-10  -  PgBouncer 1.3.3  -  « NSFW »**

- Mejoras
  * Hace configurable el argumento de listen(2): listen_backlog.  Esto es
    útil en sistemas operativos donde el máximo permitido por el sistema es
    configurable.
  * Mejora los mensajes de desconexión para mostrar qué nombre de usuario
    o de base de datos provocó el fallo del inicio de sesión.
- Correcciones
  * Traslada la lógica de relanzamiento del fallo rápido.  La antigua era
    molesta en el caso de bases de datos o usuarios permanentemente rotos,
    al intentar reintentar aunque no hubiera clientes que quisieran iniciar
    sesión.
  * Hace que las funciones de registro conserven el errno antiguo; de lo
    contrario, pgbouncer puede comportarse de forma extraña con niveles de
    registro altos y problemas de registro.
  * Aumenta el tamaño de varios búferes relacionados con el inicio para
    manejar el inicio más ruidoso de EDB.
  * Detecta una solicitud de inicio con protocolo V2 y da un motivo claro
    de desconexión.

**2010-03-15  -  PgBouncer 1.3.2  -  « Bala boomerang »**

- Correcciones

  * Nueva variable de configuración 'query_wait_timeout'.  Si el cliente
    no obtiene una conexión de servidor en ese número de segundos, se
    terminará.

  * Si no hay conexión de servidor en el pool y la última conexión falló,
    no pone las conexiones de cliente en espera, sino que envía un error de
    inmediato.

    Esto, junto con la corrección anterior, evita estancamientos
    innecesarios si una base de datos ha caído.

  * Sigue el estado de libevent en sbuf.c para evitar un event_del()
    doble.  Aunque normalmente es seguro, no parece funcionar al 100%.
    Ahora deberíamos saber siempre si se ha llamado o no.

  * Desactiva el mantenimiento durante SUSPEND.  De lo contrario, con
    tiempos de espera cortos, el bouncer antiguo podía cerrar algunas
    conexiones después de enviarlas.

  * Aplica client_login_timeout a los clientes que esperan el paquete de
    bienvenida (primera conexión de servidor).  De lo contrario pueden
    quedarse esperando indefinidamente, salvo que haya un query_timeout
    definido.

  * win32: añade los modificadores -U/-P a -regservice para que el usuario
    elija la cuenta bajo la que ejecutar el servicio.  La antigua elección
    automática entre Local Service y Local System no era lo bastante
    fiable.

  * consola: elimina el \0 del final de las columnas de texto.  Era
    difícil de notar, porque los clientes en C estaban conformes con ello.

  * Mejoras en la documentación.  (Greg Sabino Mullane)

  * Aclara algunos mensajes de registro relacionados con el inicio de
    sesión.

  * Cambia el nivel de registro de los errores enviados por el pooler
    (normalmente al desconectar) de INFO a WARNING, ya que señalan
    problemas.

  * Cambia el mensaje de registro de query_timeout a "query timeout".

**2009-07-06  -  PgBouncer 1.3.1  -  « Ahora cumple plenamente los requisitos de vigilancia de la NSA »**

- Correcciones
  * Corrige un problema con sbuf_loopcnt que podía dejar colgadas las
    conexiones.  Si la longitud de la consulta o del resultado está cerca
    de un múltiplo de (pktlen*sbuf_loopcnt) [10k por defecto], podía
    quedarse esperando más datos que no aparecerán.
  * Hace inmediata la reconfiguración de la base de datos.  Actualmente
    las conexiones antiguas podían reutilizarse tras un SIGHUP.
  * Corrige SHOW DATABASES, que estaba roto por una adición de columna.
  * El acceso a la consola estaba desactivado con "auth_type=any", ya que
    pgbouncer descartaba el nombre de usuario.  Corrección: si
    "auth_type=any", permite que cualquier usuario entre a la consola como
    administrador.
  * Corrige la macro CUSTOM_ALIGN defectuosa.  Por suerte no se usa si el
    sistema operativo ya define la macro ALIGN, así que parece que el
    error no ha ocurrido en entornos reales.
  * win32: llama a WSAStartup() siempre, no solo en modo demonio,
    ya que el análisis de la configuración quiere resolver hosts.
  * win32: pone comillas alrededor del nombre del archivo de configuración
    en la línea de comandos del servicio para permitir espacios en las
    rutas.  La ruta del ejecutable no parece necesitarlo debido a alguna
    magia de win32.
  * Añade STATS al texto de SHOW HELP.
  * doc/usage.txt: las unidades de tiempo en los resultados de la consola
    están en microsegundos, no en milisegundos.

**2009-02-18  -  PgBouncer 1.3 -  « Nuevo golpe final Ki-Smash »**

- Funcionalidades

  * La IANA ha asignado el puerto 6432 como puerto oficial de
    PgBouncer.  Por tanto, el número de puerto predeterminado ha cambiado a
    6432.  Los usuarios individuales existentes no necesitan cambiarlo,
    pero si distribuyes paquetes de PgBouncer, cambia por favor el valor
    predeterminado del paquete al puerto oficial.

  * Creación dinámica de bases de datos (David Galoyan)

    Ahora puedes definir una base de datos con el nombre "*".  Si se
    define, su cadena de conexión se usará para todas las bases de datos
    sin definir.  Útil sobre todo para entornos de prueba /
    desarrollo.

  * Soporte de Windows (Hiroshi Saito)

    PgBouncer ahora funciona en Windows 2000+.  El uso de la línea de
    comandos sigue igual, excepto que no puede ejecutarse como demonio ni
    hacer reinicio en línea.  Para ejecutarlo como servicio, define el
    parámetro service_name en la configuración.  Entonces:

        > pgbouncer.exe config.ini -regservice
        > net start SERVICE_NAME

    Para detener y desregistrar:

        > net stop SERVICE_NAME
        > pgbouncer.exe config.ini -unregservice

    Para usar el registro de eventos de Windows, primero hay que
    registrar la DLL de eventos:

        > regsvr32 pgbevent.dll

    Después puedes definir "syslog = 1" en la configuración.

- Funcionalidades menores

  * Los nombres de bases de datos en el archivo de configuración ahora
    pueden entrecomillarse con el entrecomillado estándar de identificadores
    SQL, para permitir caracteres no estándar en los nombres de las bases
    de datos.

  * Nuevos parámetros ajustables: 'reserve_pool_size' y
    'reserve_pool_timeout'.  En caso de que haya clientes en el pool que
    hayan esperado más de 'reserve_pool_timeout' segundos,
    'reserve_pool_size' especifica el número de conexiones que pueden
    añadirse al pool.  También puede fijarse por pool con la variable de
    conexión 'reserve_pool'.

  * Nuevo parámetro ajustable 'sbuf_loopcnt' para limitar el tiempo
    dedicado a un socket.

    En algunas situaciones —p. ej. servidor SMP, Postgres local y red
    rápida— pgbouncer puede ejecutar el bucle recv()->send() muchas veces
    sin bloquearse en ningún lado.  Pero eso significa que otras conexiones
    se estancarán durante mucho tiempo.  Para hacer el procesamiento más
    justo, limita las veces de hacer recv()->send() en un socket.  Si el
    contador alcanza el límite, simplemente procede a procesar otros
    sockets.  El procesamiento de ese socket se reanudará en el siguiente
    bucle de eventos.

    Gracias a Alexander Schöcke por el informe y las pruebas.

  * La autenticación crypt() ahora es opcional, ya que se eliminó de
    Postgres.  Si el sistema operativo no la proporciona, pgbouncer
    funciona bien sin ella.

  * Añade milisegundos a las marcas de tiempo del registro.

  * Sustituye la antigua implementación de MD5 por una más compacta.

  * Actualiza la licencia ISC con la aclaración de la FSF.

- Correcciones

  * En caso de que event_del() informe de un fallo, simplemente procede
    con la limpieza.  Antes pgbouncer lo reintentaba, por si el fallo se
    debía a ENOMEM.  Pero esto causó inundaciones de registro con
    repeticiones infinitas, así que parece que a libevent no le gusta.

    Por qué event_del() informa de fallo la primera vez sigue siendo un
    misterio.

  * --enable-debug ahora solo activa o desactiva si la información de
    depuración se elimina del binario.  Ya no juega con
    -fomit-frame-pointer, ya que es peligroso.

  * Corrige el orden de los include, ya que de lo contrario los include
    del sistema podían llegar antes que los internos.  Era un problema
    para el nuevo archivo de include md5.h.

  * Incluye el archivo COPYRIGHT en el .tgz...

--------

## PgBouncer 1.2.x {#pgbouncer-12x}

**2008-08-08  -  PgBouncer 1.2.3  -  « Bytes cuidadosamente seleccionados »**

- Correcciones
  * Desactiva el código SO_ACCEPTFILTER para los BSD, que no
    funcionaba.
  * Incluye el etc/userlist.txt de ejemplo en el tgz.
  * Usa '$(MAKE)' en lugar de 'make' para la recursión (Jørgen Austvik)
  * Define _GNU_SOURCE, ya que glibc es inútil sin ello.
  * Deja que libevent 1.1 pase la prueba de enlazado para poder informar
    luego "1.3b+ needed"
  * Detecta el pidfile obsoleto y lo elimina.

Gracias a Devrim GÜNDÜZ y Bjoern Metzdorf por los informes de problemas y
las pruebas.

**2008-08-06  -  PgBouncer 1.2.2  -  « Con bolsa de vómito incluida »**

- Correcciones
  * Elimina 'drop_on_error': era una mala idea.  Se añadió como solución al
    comportamiento roto de la caché de planes en Postgres, pero puede
    causar daño en el caso común de que algunas consultas devuelvan siempre
    error.

**2008-08-04  -  PgBouncer 1.2.1  -  « Impermeable »**

- Funcionalidades
  * Nuevo parámetro 'drop_on_error': si el servidor lanza un error, la
    conexión no se reutilizará, sino que se descartará cuando el cliente
    termine con ella.  Esto es necesario para refrescar la caché de
    planes.  El refresco automático no funciona ni siquiera en 8.3.
    Por defecto es 1.
- Correcciones
  * SHOW SOCKETS/CLIENTS/SERVERS: no se cae si el socket no tiene
    búfer.
  * Corrige el bucle infinito en SUSPEND si se dispara
    suspend_timeout.
- Limpiezas menores
  * Usa <sys/uio.h> para 'struct iovec'.
  * Cancela el apagado (de SIGINT) en RESUME/SIGUSR2; de lo contrario se
    disparará en el siguiente PAUSE.
  * Mensaje de registro adecuado si se cancela una operación de
    consola.

**2008-07-29  -  PgBouncer 1.2  -  « Flauta mágica ordinaria »**

PgBouncer 1.2 ahora requiere libevent versión 1.3b o más reciente.
Las versiones anteriores de libevent se caen con el nuevo código de
reinicio.

- Funcionalidades

  * Opción de línea de comandos (-u) y parámetro de configuración (user=)
    para admitir el cambio de usuario al arrancar.  Además, ahora
    pgbouncer se niega a ejecutarse como root.

    (Jacob Coby)

  * Texto de uso más descriptivo (-h).  (Jacob Coby)

  * Nueva opción de base de datos: connect_query, para permitir ejecutar
    una consulta en las conexiones nuevas antes de ponerlas en uso.

    (Teodor Sigaev)

  * Nueva variable de configuración 'ignore_startup_parameters' para
    permitir e ignorar parámetros extra en el paquete de inicio.  Por
    defecto solo se permiten 'database' y 'user'; todos los demás lanzan
    error.  Esto es necesario para tolerar el JDBC demasiado entusiasta
    que quiere definir incondicionalmente 'extra_float_digits=2' en el
    paquete de inicio.

  * Registro en syslog: nuevos parámetros syslog=0/1 y
    syslog_facility=daemon/user/local0.

  * Reinicio en línea menos atemorizante (-R)

    - Mueve la carga de FD antes del fork, de modo que registre en la
      consola y pueda cancelarse con ^C

    - Mantiene SHUTDOWN después del fork, para que ^C sea seguro

    - Se intenta un connect() al socket unix para ver si alguien está
      escuchando.  Ahora -R puede usarse incluso cuando no había proceso
      previo en ejecución.  Si hay proceso previo, pero no se usa -R, el
      arranque falla.

  * Nuevos comandos de consola:

    - SHOW TOTALS, que muestra un resumen de estadísticas (como va al
      registro) más el uso de memoria.

    - SHOW ACTIVE_SOCKETS: como show sockets, pero filtra solo las
      activas.

- Funcionalidades menos visibles

  * suspend_timeout: descarta conexiones estancadas e inicios de sesión
    largos.  Esto aporta seguridad adicional al reinicio.

  * Cuando la base de datos remota lanza un error al iniciar sesión,
    notifica a los clientes.

  * Eliminar una base de datos de la configuración y recargar funciona:
    todas las conexiones se terminan y la base de datos se elimina.

  * Falsifica algunos parámetros en los comandos SHOW/SET de la consola
    para parecerse más a Postgres.  Eso era necesario para permitir que
    psycopg se conectara a la consola.
    (client_encoding/default_transaction_isolation/datestyle/timezone)

  * Hace que server_lifetime=0 desconecte la conexión de servidor
    inmediatamente después del primer uso.  Antes, "0" hacía que
    PgBouncer ignorara la edad del servidor.  Como este comportamiento no
    estaba documentado, no debería haber usuarios que dependan de él.

  * Mejoras internas:

    - Los búferes de paquetes se asignan perezosamente y se reutilizan.
      Esto debería reducir enormemente el uso de memoria.  Esto también
      hace realista usar un pktbuf grande con muchas conexiones.

    - Muchas mejoras en el manejo de errores; PgBouncer ahora debería
      sobrevivir con elegancia a situaciones de OOM.

    - Usa el asignador slab para la gestión de memoria.

    - Muchas limpiezas de código.

- Correcciones

  * Solo se emitía un único accept() por bucle de eventos, lo que podía
    causar acumulación de conexiones al haber un alto número de intentos
    de conexión.  Ahora el socket de escucha siempre se vacía por
    completo, lo que debería corregirlo.
  * Maneja EINTR de connect().
  * Hace compatible configure.ac con autoconf 2.59.
  * Correcciones de compatibilidad con Solaris (Magne Mæhre)

--------

## PgBouncer 1.1.x {#pgbouncer-11x}

**2007-12-10  -  PgBouncer 1.1.2  -  « El martillo »**

- Funcionalidades
  * Las desconexiones por server_lifetime ahora están separadas por
    (server_lifetime / pool_size) segundos.  Esto evita que pgbouncer
    provoque inundaciones de reconexiones.
- Correcciones
  * Problemas de la actualización en línea de 1.0 -> 1.1:
    - 1.0 no sigue los parámetros del servidor, así que permanecen NULL,
      pero 1.1 no lo esperaba y se caía.
    - Si los parámetros del servidor son desconocidos, pero los del
      cliente están definidos, emitir un SET para ellos, en lugar de
      quejarse.
  * Elimina las instrucciones de depuración temporales que se dejaron
    accidentalmente en el código a nivel INFO, por lo que contaminaban los
    registros.
  * Arregla de nuevo debian/changelog
- Limpieza
  * reordena los campos del struct SBuf para obtener mejor alineación del
    búfer.

**2007-10-26  -  PgBouncer 1.1.1  -  « Abeja bailarina de breakdance »**

- Correcciones
  * La caché de parámetros del servidor podía quedar sin inicializar, lo
    que causaba un SET innecesario de ellos.  Esto causaba problemas en
    8.1, que no permite tocar standard_conforming_strings.
    (Gracias a Dimitri Fontaine por el informe y las pruebas.)
  * Algunas correcciones en la documentación.
  * Incluye doc/fixman.py en el .tgz.

**2007-10-09  -  PgBouncer 1.1  -  « Caja de herramientas de sombrero loco »**

- Funcionalidades

  * Mantiene un seguimiento de los siguientes parámetros del servidor:

        client_encoding  datestyle, timezone, standard_conforming_strings

  * Mejoras en la cadena de conexión de la base de datos:

    - Acepta nombre de host en host=
    - Acepta una ubicación personalizada de socket unix en host=
    - Acepta valores entrecomillados: password=' asd''foo'

  * Nueva variable de configuración: server_reset_query, para enviarse
    inmediatamente después de la liberación
  * Nueva variable de configuración: server_round_robin, para alternar
    entre LIFO y RR.
  * El paquete de cancelación dirigido a una conexión inactiva ya no la
    descarta.
  * La cancelación con ^C desde psql funciona para SUSPEND / PAUSE.
  * Imprime los límites de FD al arrancar.
  * Al suspender, intenta alcanzar el límite de paquete lo antes
    posible.
  * Añade 'timezone' a los parámetros de base de datos.
  * Usa un fd de archivo de registro de larga vida.  Reabierto en SIGHUP /
    RELOAD;
  * Información del punto de conexión local en SHOW
    SERVERS/CLIENTS/SOCKETS.

- Limpieza de código

  * Más mensajes de registro de depuración incluyen información del
    socket.
  * Eliminación de números mágicos y limpieza de mensajes de error.
    (David Fetter)
  * Struct contenedor para la información del paquete actual.  Elimina
    mucha complejidad.

- Correcciones

  * Detecta mejor las cabeceras de paquetes no válidas.
  * La comprobación de modificación del auth_file estaba rota, lo que
    hacía que pgbouncer lo recargara con demasiada frecuencia.

--------

## PgBouncer 1.0.x {#pgbouncer-10x}

**2007-06-18  -  PgBouncer 1.0.8  -  « Jutsu de la pala no muerta »**

- Correcciones
  * Corrige una caída en el manejo del paquete de cancelación. (^C desde
    psql)
- Funcionalidades
  * PAUSE <db>; RESUME <db>; ya funciona.
  * Limpieza del análisis de los comandos de consola.
  * Desactiva la costosa comprobación assert de pertenencia a una lista.

**2007-04-19  -  PgBouncer 1.0.7  -  « Con vitaminas de la A a la Z »**

- Correcciones
  * El envío de varios paquetes de error/aviso con send() bloqueándose
    entre ellos disparaba una aserción.  Se corrige eliminando por completo
    la lógica de volcado.  Como PgBouncer no almacena activamente nada en
    búfer, esta lógica no es necesaria.  Era un remanente de la época en
    que el buffering se empujaba al núcleo con MSG_MORE.
  * Además, evita llamar a la lógica de recv() cuando se desbloquea el
    envío.
  * El código de búsqueda en lista para admin_users y stats_users
    manejaba mal las coincidencias parciales.  Se corrige.
  * Estandariza la búsqueda del UID del par del socket UNIX a
    getpeereid().

**2007-04-12  -  PgBouncer 1.0.6  -  « Dosis diaria »**

- Correcciones
  * La corrección «Desactiva el mantenimiento durante la toma de control» podía
    desactivar el mantenimiento por completo.  Se corrige.
  * Corrección de compilación para FreeBSD: allí <sys/ucred.h> requiere
    <sys/param.h>.
    Gracias a Robert Gogolok por el informe.

**2007-04-11  -  PgBouncer 1.0.5  -  « Suficiente por hoy »**

- Correcciones
  * Corrige errores del reinicio en línea:
    - Define ->ready para los servidores inactivos.
    - Elimina el código obsoleto de use_client_socket()
    - Desactiva el mantenimiento durante la toma de control.

**2007-04-11  -  PgBouncer 1.0.4  -  « El último error "último" »**

- Correcciones
  * Un Notice de un servidor inactivo marcaba el servidor como dirty.
    release_server() no lo esperaba.  Se corrige descartándolos.

**2007-04-11  -  PgBouncer 1.0.3  -  « Fork intrépido »**

- Correcciones
  * Faltaba algo de manejo de errores en la ruta de inicio de sesión, de
    modo que una conexión moribunda ahí podía disparar asserts.
  * Limpieza de los asserts en sbuf.c para detectar problemas antes.
  * Crea un core cuando se dispara Assert().

- Novedades
  * Nuevas variables de configuración: log_connections,
    log_disconnections y log_pooler_errors para activar/desactivar el
    ruido.
  * Variable de configuración: client_login_timeout, para terminar
    conexiones muertas en la fase de inicio de sesión que podían estancar
    SUSPEND y, por tanto, el reinicio en línea.

**2007-03-28  -  PgBouncer 1.0.2  -  « Cuchara supersónica »**

- Correcciones
  * libevent puede informar de un evento eliminado dentro del mismo
    bucle.  Evita la reutilización del socket durante un bucle.
  * release_server() desde disconnect_client() no comprobaba si el paquete
    se había enviado realmente.

**2007-03-15  -  PgBouncer 1.0.1  -  « Tecnología alienígena »**

- Correcciones
  * El uso mixto de tiempo cacheado y no cacheado, más el typedef usec_t
    sin signo, creaba errores espurios de query_timeout.
  * Corrige el caso raro en que un socket despertado de la espera de
    envío podía quedarse estancado.
  * Encolamiento más justo de las conexiones de servidor.  Antes, una
    consulta nueva podía obtener una conexión de servidor antes que una
    más antigua.
  * Retrasa la liberación del servidor hasta que se garantice que todo se
    ha enviado.

- Funcionalidades
  * Comando SHOW SOCKETS para tener información detallada del estado.
  * Pone el puntero PgSocket en el registro, para ayudar a rastrear una
    conexión.
  * En la consola, permite SELECT en lugar de SHOW.
  * Varias limpiezas de código.

**2007-03-13  -  PgBouncer 1.0  -  « BMW tuneado »**

- Primer lanzamiento público.
