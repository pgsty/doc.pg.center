---
title: "Notas de versión"
weight: 190
icon: fa-solid fa-scroll
description: "Notas de versión cronológicas de Patroni e historial de cambios."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/releases.html"
---

<a id="releases"></a>

--------

## Versión 4.1.5 {#version-415}

Publicado el 2026-08-12

**Mejoras de compatibilidad**

- Compatibilidad con PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6 (Alexander Kukushkin)

  Añade el nuevo GUC `output_plugin_libraries`, que restringe los plugins de salida de la decodificación lógica.

**Mejoras**

- Registra los restablecimientos de conexión de la REST API en `DEBUG` en lugar de en `WARNING` (Kyle McLaren)

  Garantiza que las variantes comunes de «el cliente se fue a mitad de una escritura» se silencien sin afectar el manejo de los errores genuinos (no relacionados con la conexión).

**Correcciones de errores**

- Corrige la alineación de la validación de `thread_stack_size` (Sundong Kim)

  Corrige el valor `aligned` de `65535` a `65536` en la entrada del esquema de `thread_stack_size`. Anteriormente, `patroni --validate-config` rechazaba casi cualquier valor realista, incluido el valor predeterminado `524288` aplicado por el propio demonio.

- Permite que la validación de `synchronous_mode` acepte `'quorum'` y cadenas de tipo booleano (Eray Araz)

  Anteriormente, `patroni --validate-config` rechazaba valores de `synchronous_mode` como `quorum` y las cadenas booleanas al estilo de PostgreSQL que se aceptan en tiempo de ejecución.

## Versión 4.1.4 {#version-414}

Publicado el 2026-07-07

**Correcciones de errores**

- Comprueba la variable de entorno `NOTIFY_SOCKET` antes de usar el paquete `systemd` (Polina Bungina)

  Solo intenta importar y usar el paquete cuando la variable de entorno `NOTIFY_SOCKET` esté establecida, para evitar la excepción `FileNotFoundError: [Errno 2] No such file or directory`.

- Unifica la consulta `pg_replication_slots` (Polina Bungina)

  El manejo incorrecto de los valores `failover` y `synced` provocaba excepciones `KeyError` durante la eliminación de los slots de replicación lógica incorrectos.

- Considera los parámetros de autenticación específicos de la versión en la generación de la configuración (Polina Bungina)

  En el comando `patroni --generate-config`, elimina todos los parámetros de autenticación no aplicables que se habían recogido accidentalmente del entorno, según la versión obtenida de una conexión a PostgreSQL.

- Maneja `pg_rewind` mientras una instancia de PostgreSQL se inicia como standby (Alexander Kukushkin)

  Recurre a la información de `pg_controldata` cuando una instancia de PostgreSQL se está ejecutando pero aún no acepta conexiones.

- Corrige el tipo de la métrica de Prometheus para `patroni_postgres_timeline` (Huseyin Demir)

  Declara la métrica `patroni_postgres_timeline` como `gauge` en lugar de `counter`, ya que no siempre aumenta monótonamente (p. ej., puede restablecerse a 0 si una instancia de PostgreSQL no se está ejecutando).

- No detiene el watchdog hasta que los backends de cliente se hayan detenido por completo (Alexander Kukushkin)

  Anteriormente, si `primary_stop_timeout` era más corto que el tiempo de espera mínimo del watchdog y el tiempo de espera de la detención expiraba realmente, Patroni deshabilitaba el watchdog antes de que todos los backends de cliente hubieran terminado.

- Maneja el error de tiempo de espera de sentencia para la consulta de monitoreo (Alexander Kukushkin)

  En caso de error de tiempo de espera de sentencia, usa el rol almacenado en caché como alternativa para evitar degradar el primario. Además, establece forzosamente `pg_stat_statements.track` en `none` para la consulta de monitoreo, a fin de evitar llamadas costosas al GC de `pg_stat_statements`.

- Elimina los slots de replicación gestionados por Patroni con `wal_status=lost` (Alexander Kukushkin)

  Los slots de replicación con `wal_status=lost` ya no son utilizables. Patroni ahora eliminará dichos slots y los recreará si es necesario.

- Corrige la representación del rol en el error de validación de miembros de patronictl (Polina Bungina)

  Garantiza que se utilice la representación de cadena correcta en el mensaje de la excepción, evitando que los errores se formateen como `Error: No CtlPostgresqlRole.REPLICA among provided members`.

## Versión 4.1.3 {#version-413}

Publicado el 2026-05-05

**Mejoras de estabilidad**

- Maneja correctamente un error de Etcd mal etiquetado (Ants Aasma)

  Las versiones actuales de Etcd generan el error `Unknown` cuando se pierde el líder de Etcd mientras se actualiza la concesión. Patroni ahora anulará el código de error reportado a `Unavailable`.

**Correcciones de errores**

- Usa la versión del binario cuando el archivo `PG_VERSION` no existe (Polina Bungina)

  En algunos casos, por ejemplo al usar un bootstrap personalizado, el archivo `PG_VERSION` puede no estar presente en el directorio de datos. En ese caso, Patroni trataba la versión como 0.0, lo que causaba problemas con parte de la lógica específica de la versión. Con esta corrección, Patroni intentará obtener la versión del binario en dichos casos.

- Refactoriza la inicialización del logger para evitar la pérdida de mensajes de registro tempranos (Alexander Kukushkin)

  Crea `PatroniLogger` antes de cargar `Config` para capturar los mensajes de registro tempranos.

- Incluye `MONOTONIC_USEC` en la notificación `RELOADING=1` de systemd (Alexander Kukushkin)

  systemd 257+ requiere `MONOTONIC_USEC` junto con `RELOADING=1` para los servicios `Type=notify-reload`. Sin ello, `systemctl reload` se cuelga indefinidamente.

**Mejoras**

- Omite la recuperación ante fallos en modo usuario único cuando existe `backup_label` (Vadim Ponomarev)

  Omite la recuperación ante fallos en modo usuario único y deja que PostgreSQL la maneje durante el inicio normal al iniciar una réplica restaurada desde una copia de seguridad externa (sin usar un método de bootstrap personalizado).

- Advierte cuando se ejecuta bajo `systemd` sin el paquete `python-systemd` (Alexander Kukushkin)

  En lugar de registrar "systemd integration is not supported" al inicio, comprueba `NOTIFY_SOCKET` y solo advierte cuando realmente se está ejecutando bajo `systemd` sin el paquete `python-systemd` instalado.

## Versión 4.1.2 {#version-412}

Publicado el 2026-04-21

**Mejoras en el soporte de systemd**

- Añade soporte para el tipo de unidad `notify-reload` de systemd (Ronan Dunklau)

  Permite que `systemctl reload` espere hasta que Patroni haya procesado realmente la recarga de configuración, mediante el envío de las notificaciones `RELOADING=1` y `READY=1` a systemd.

- Envía la notificación `STOPPING=1` a systemd al apagarse (Alexander Kukushkin)

  Patroni ahora notifica correctamente a systemd que se está apagando, siguiendo el protocolo notify de systemd.

- No permite que PostgreSQL notifique a systemd (Alexander Kukushkin)

  Elimina `NotifyAccess=all` del archivo de unidad de systemd de ejemplo. Filtra `NOTIFY_SOCKET` del entorno al iniciar PostgreSQL para que no envíe `READY=1` ni `STOPPING=1` a systemd. Al tomar el control de un PostgreSQL que se inició antes que Patroni y que ya tiene `NOTIFY_SOCKET`, reafirma `READY=1` durante el apagado de PostgreSQL para contrarrestar su `STOPPING=1`.

## Versión 4.1.1 {#version-411}

Publicado el 2026-04-08

**Mejoras de estabilidad**

- Compatibilidad con los cambios en el threading de python 3.11+ (Alexander Kukushkin)

  Evita iniciar/detener hilos en tiempo de ejecución. Introduce grupos de hilos para la REST API y para ejecutar tareas asíncronas. Permite configurar `thread_pool_size` global y `restapi.thread_pool_size`.

- Compatibilidad con python 3.14 (Alexander Kukushkin)

  Ejecuta las pruebas contra python 3.14 y corrige problemas de compatibilidad.

- Compatibilidad con las correcciones de seguridad de Etcd en v3.6.9, v3.5.28 y v3.4.42 (Alexander Kukushkin)

  Estas versiones de Etcd abordaron CVEs y cambiaron el comportamiento de modo que la lectura de la topología del clúster y el mantenimiento de la concesión (keepalive) ya no estén permitidas sin autenticación. Patroni ahora lo maneja autenticándose en las rutas de descubrimiento de miembros y de mantenimiento de concesiones, reautenticándose ante fallos de autenticación y reintentando las solicitudes en consecuencia.

- Mejoras en el manejo de errores de Etcd3 (Alexander Kukushkin)

  Maneja respuestas JSON rotas, es flexible en la forma de analizar el error JSON y mejora el reporte de los errores internos de etcd.

**Correcciones de errores**

- Reintenta la actualización del líder ante un error `403` temporal de Kubernetes (Sophia Ruan, Alexander Kukushkin)

  Cuando la API de Kubernetes devuelve temporalmente `403 Permission Denied` (por ejemplo, durante problemas transitorios de RBAC), Patroni ahora verifica si el nodo actual todavía retiene el liderazgo y reintenta la actualización del líder dentro de `retry_timeout` en lugar de degradarse inmediatamente.

- Corrige un problema al renombrar el nodo líder en modo síncrono y en pausa (Alexander Kukushkin)

  La clave `/sync` no se actualizaba tras renombrar el nodo líder con reinicio de Patroni en pausa (sin reinicio de Postgres). Esto impedía que Patroni promoviera después del siguiente reinicio sin pausa.

- Activa la comprobación de `pg_rewind` cuando el mismo primario incrementó la línea de tiempo (Alexander Kukushkin)

  Dicho incremento de la línea de tiempo puede ocurrir como resultado de una recuperación ante fallos en modo usuario único más una promoción después de tomar la clave de líder, mientras otros nodos réplica están aislados del DCS. En este caso, los nodos réplica no activaban la máquina de estados de `pg_rewind` porque el líder y, por lo tanto, `primary_conninfo` no cambiaban.

- Escribe la contraseña de superusuario durante el bootstrap de `initdb` solo si no está vacía (Michael Banck)

  Escribir una contraseña vacía durante el bootstrap de `initdb` causaba problemas.

- Corrige un error con `failover_priority` cuando `synchronous_mode=on` (Alexander Kukushkin)

  Los valores de `tag.failover_priority` se ignoraban cuando `synchronous_node_count > 1`.

- Corrige un error en la comparación de contraseñas de `primary_conninfo` (Alexander Kukushkin)

  A partir de PostgreSQL 10, Patroni usa passfile en `primary_conninfo` y no actualizaba el passfile después de que la contraseña de replicación se actualizara en la configuración del archivo yaml con una recarga.

- No reinicia la réplica con la etiqueta `nofailover` en modo de pausa (Alexander Kukushkin)

  Patroni solía iniciar una réplica de PostgreSQL apagada manualmente en modo de pausa cuando tenía la etiqueta `nofailover` establecida en `true`.

- Corrige `check_recovery_conf()` cuando PostgreSQL está en estado de inicio (Alexander Kukushkin)

  Para PostgreSQL v12 y posteriores, `pg_settings` no puede consultarse mientras el servidor todavía se está iniciando y aún no acepta conexiones. Los parámetros de recuperación que faltan ahora se añaden al estado interno al escribir `postgresql.conf`. Además, se restaura la comprobación `Postgresql.is_starting()` en `Ha.is_healthiest_node()`.

- Valida las opciones de usuario en formato de diccionario para `initdb`/`basebackup` (m4rrypro)

  Cuando las opciones de `initdb` o `basebackup` se proporcionaban como un diccionario (en lugar de una lista), la validación de `option_is_allowed()` se omitía, lo que permitía usar opciones bloqueadas.

- Permite la compresión del lado del servidor para la opción `basebackup` (m4rrypro)

  La opción `compress` estaba completamente bloqueada para `basebackup`, pero desde PostgreSQL 15 la compresión del lado del servidor es útil y funciona de forma transparente con el formato plain. La compresión del lado del cliente sigue rechazándose.

- No recarga la configuración de PostgreSQL mientras se ejecuta un bootstrap personalizado (Alexander Kukushkin)

  El bootstrap personalizado puede ser complejo e implicar que PostgreSQL se inicie y se detenga varias veces. Las recargas de la configuración de PostgreSQL durante este proceso podían provocar un comportamiento inesperado.

- Comprueba que `postgresql.parameters` sea un diccionario (Alexander Kukushkin)

  Descarta la nueva configuración si `postgresql.parameters` no es un diccionario.

## Versión 4.1.0 {#version-410}

Publicado el 2025-09-23

**Nuevas funcionalidades**

- Añade soporte para el tipo de unidad "notify" de systemd (Ronan Dunklau)

  Sin un tipo de unidad notify, es posible iniciar Patroni e inmediatamente enviarle una señal SIGHUP mediante systemd, lo que en la práctica lo mata antes de que haya tenido tiempo de configurar sus manejadores de señales.

- Proporciona información de LSN/lag de recepción y reproducción en la API y en ctl (Polina Bungina)

  El endpoint `/cluster` de la REST API de Patroni y el comando `patronictl list` ahora proporcionan información del LSN de recepción, del LSN de reproducción, del lag de recepción y del lag de reproducción para cada miembro réplica.

- Garantiza una degradación limpia a clúster en espera (Polina Bungina)

  Garantiza que la introducción de la sección [standby_cluster](/es/patroni/standby_cluster#standby_cluster) en la configuración dinámica conduzca a una degradación limpia del clúster.

- Implementa los comandos `patronictl demote-cluster` y `promote-cluster` (Polina Bungina)

  Los nuevos comandos para la degradación y promoción del clúster se encargan tanto de la edición de la configuración dinámica como de la comprobación del estado del resultado.

- Implementa la etiqueta `sync_priority` (Polina Bungina)

  Este parámetro controla la prioridad que un miembro debería tener durante la selección de réplicas síncronas cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está establecido en `on`.

- Implementa la opción `--print` para `--validate-config` (Polina Bungina)

  Imprime la configuración local (incluidas las anulaciones de configuración del entorno) después de que se haya validado correctamente.

- Implementa `kubernetes.bootstrap_labels` (Polina Bungina)

  Esta función permite definir etiquetas que se asignarán al pod de un miembro cuando esté en el estado `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` o `creating replica`.

- Añade una opción de configuración para suprimir los registros de latido duplicados (Michael Morris)

  Si se establece en `true`, los registros de latido sucesivos que sean idénticos no se emitirán.

- Añade el atributo opcional `cluster_type` a los slots de replicación permanentes (Michael Banck)

  Esto permite establecer si un slot de replicación permanente concreto debe crearse siempre, o solo en un clúster primario o en espera.

- Hace configurable el encabezado HTTP Server (David Grierson)

  Introduce el parámetro de configuración `restapi.server_tokens` que permite restringir la información revelada en el encabezado HTTP Server.

- Implementa comprobaciones de readiness de la API para la replicación en los miembros réplica (Ants Aasma)

  La implementación anterior consideraba las réplicas listas tan pronto como PostgreSQL se iniciaba. Con este cambio, un pod de réplica solo se considera listo cuando PostgreSQL está replicando y no va demasiado retrasado respecto al líder.

**Mejoras**

- Reduce el nivel de registro del fallo de configuración del watchdog (Ants Aasma)

  Muestra la línea de registro `Could not activate Linux watchdog device` en el nivel de registro debug, a menos que el watchdog esté configurado en modo `required`. Anteriormente se mostraba en el nivel info.

- Aprovecha `written_lsn` y `latest_end_lsn` de `pg_stat_wal_receiver` (Alexander Kukushkin)

  Ahora se prefiere `written_lsn`, el LSN real de escritura, en lugar del devuelto por `pg_last_wal_receive_lsn()`, que de hecho es el LSN de vaciado a disco (flush). `latest_end_lsn` apunta al vaciado de WAL a disco en el host de origen. En el caso de un primario, permite un mejor cálculo del lag de reproducción, porque los valores almacenados en el DCS solo se actualizan cada `loop_wait` segundos.

- Evita interacciones con los slots creados con la opción `failover=true` (Alexander Kukushkin)

  Este cambio es necesario para que la función de conmutación por error de los slots lógicos sea completamente funcional.

- Añade el estado de PostgreSQL al endpoint `/metrics` de la REST API (Ivan Filianin)

  La información del estado de la instancia de PostgreSQL ahora está disponible en la salida en formato Prometheus del endpoint `/metrics` de la REST API.

--------

## Versión 4.0.7 {#version-407}

Publicado el 2025-09-22

**Nuevas funcionalidades**

- Añade soporte para PostgreSQL 18 RC1 (Alexander Kukushkin)

  Se ampliaron las reglas del validador de GUC. Patroni ahora maneja correctamente el nuevo worker de E/S en segundo plano.

**Correcciones de errores**

- Corrige un posible problema con la resolución de localhost a IPv6 en Windows (András Váczi)

  Al configurar `listen_addresses` en PostgreSQL, usar `0.0.0.0` o `127.0.0.1` restringirá la escucha solo a IPv4, excluyendo IPv6. Sin embargo, en sistemas Windows típicos, `localhost` a menudo se resuelve por defecto a la dirección IPv6 `::1`. Para garantizar la compatibilidad, Patroni ahora configura PostgreSQL para que escuche en `127.0.0.1`, en lugar de `localhost`, en sistemas Windows.

- Devuelve la configuración global solo cuando la clave `/config` existe en el DCS (Alexander Kukushkin)

  La REST API de Patroni devolvía una configuración vacía en lugar de generar un error si faltaba la clave `/config` en el DCS.

- Corrige el problema de que el modo a prueba de fallos no se activara en caso de indisponibilidad de Etcd (Alexander Kukushkin)

  Patroni no siempre manejaba correctamente las excepciones de `etcd3`, lo que provocaba que el modo a prueba de fallos no se activara.

- Corrige un interbloqueo por reentrada en el manejador de señales (Waynerv)

  Patroni ejecutándose en un contenedor Docker con `PID=1` en algunos casos especiales experimentaba un interbloqueo tras recibir `SIGCHLD`.

- Recrea un slot físico (permanente) cuando no reserva WAL (Israel Barth Rubio)

  Los slots de replicación físicos permanentes creados fuera del ámbito de Patroni sin reservar WALs provocaban un error `replication slot cannot be advanced`. Para evitarlo, Patroni ahora recrea dichos slots.

- Maneja correctamente los mensajes de cancelación de watch en `etcd3` (Alexander Kukushkin)

  Cuando `etcd3` envía un mensaje de cancelación al canal de watch, no cierra la conexión. Esto provoca que Patroni use datos obsoletos. Patroni ahora lo soluciona rompiendo el bucle de lectura de la respuesta fragmentada y cerrando la conexión por el lado de Patroni.

- Maneja el caso en que el socket de `HTTPConnection` está envuelto con `pyopenssl` (Alexander Kukushkin)

  Patroni no estaba usando correctamente las interfaces de `pyopenssl`, exigidas en `python-etcd`.

**Mejoras en la documentación**

- Mejora la guía para clústeres de 2 nodos (Nikolay Samokhvalov)

  Aclara el comportamiento durante la conmutación por error y los requisitos del DCS.

--------

## Versión 4.0.6 {#version-406}

Publicado el 2025-06-06

**Correcciones de errores**

- Corrige un error en la conmutación por error desde un líder con mayor prioridad (Alexander Kukushkin)

  Garantiza que Patroni ignore al antiguo líder con mayor prioridad cuando reporta el mismo `LSN` que el nodo actual.

- Corrige los permisos del archivo `postgresql.conf` creado fuera de `PGDATA` (Michael Banck)

  Respeta el valor de umask de todo el sistema al crear el archivo `postgresql.conf` fuera del directorio `PGDATA`.

- Corrige un error con el switchover en `synchronous_mode=quorum` (Alexander Kukushkin)

  No comprueba los requisitos de cuórum cuando se especifica un candidato.

- Ignora los nodos obsoletos de Etcd comparando el término del clúster (Alexander Kukushkin)

  Memoriza el último "raft_term" conocido del clúster de Etcd y, al ejecutar solicitudes de cliente, lo compara con el "raft_term" reportado por un nodo de Etcd.

- Actualiza los archivos de configuración de PostgreSQL al recibir `SIGHUP` (Alexander Kukushkin)

  Anteriormente, Patroni solo reemplazaba los archivos de configuración de PostgreSQL si se detectaba un cambio en la configuración global o local.

- Maneja correctamente la excepción `Unavailable` generada por `etcd3` (Alexander Kukushkin)

  Patroni solía reintentar dichas solicitudes en el mismo nodo `etcd3`, mientras que cambiar a otro nodo es una mejor estrategia.

- Mejora el manejo de las concesiones de `etcd3` (Alexander Kukushkin)

  Garantiza que Patroni renueve la concesión de `etcd3` al menos una vez por ciclo de HA.

- Vuelve a comprobar las anotaciones con el código de estado 409 al intentar adquirir el bloqueo de líder (Alexander Kukushkin)

  Implementa el mismo comportamiento que se aplicó a la lectura del objeto de líder en la versión 4.0.3 de Patroni.

- Considera `replay_lsn` al avanzar los slots (Polina Bungina)

  No intenta avanzar los slots en las réplicas más allá del `replay_lsn`. Además, avanza el slot a la posición `replay_lsn` si ya está más allá del `confirmed_flush_lsn` de este slot en la réplica, pero la réplica todavía no ha reproducido el `LSN` real en el que se encuentra este slot en el primario.

- Garantiza que se ejecute `CHECKPOINT` después de la promoción (Alexander Kukushkin)

  Era posible que la tarea de checkpoint no se restableciera al degradar porque `CHECKPOINT` aún no había terminado. Esto provocaba el uso de un `result` obsoleto cuando se activaba la siguiente promoción.

- Evita ejecutar la degradación «offline» de forma concurrente (Alexander Kukushkin)

  En caso de un apagado lento, podría ocurrir que el siguiente ciclo de latido vuelva a llegar al método de manejo de errores del DCS, lo que da como resultado la advertencia `AsyncExecutor is busy, demoting from the main thread` y el inicio de la degradación offline otra vez.

- Normaliza el valor de `data_dir` antes de renombrar el directorio de datos tras un fallo de inicialización (Waynerv)

  Evita que una barra diagonal final en el valor del parámetro `data_dir` rompa el proceso de renombrado después de un fallo de inicialización.

- Comprueba que `synchronous_standby_names` contenga el valor esperado (Alexander Kukushkin)

  Anteriormente, el mecanismo que implementaba la máquina de estados para la replicación síncrona sin cuórum no comprobaba el valor real de `synchronous_standby_names`, lo que provocaba que se usara un valor obsoleto de `synchronous_standby_names` cuando `pg_stat_replication` es un subconjunto de `synchronous_standby_names`.

--------

## Versión 4.0.5 {#version-405}

Publicado el 2025-02-20

**Mejoras de estabilidad**

- Compatibilidad con `python-json-logger>=3.1` (Alexander Kukushkin)

  Elimina las advertencias producidas por el uso de la antigua API.

- Compatibilidad con Python 3.13 (Alexander Kukushkin)

  Ejecuta las pruebas contra Python 3.13.

- Compatibilidad con `pyinstaller>=4.4` (Joe Jensen)

  Recurre al `iter_modules` predeterminado si el atributo `toc` de `pyinstaller` no está presente.

- Corrige problemas con el soporte de PostgreSQL 9.5 (Alexander Kukushkin)

  - Maneja correctamente el formato de salida de `pg_rewind`.
  - Considera que el formato de `synchronous_standby_names` no admite la especificación "num".

- Compatibilidad con los últimos cambios en `urlparse` (Alexander Kukushkin)

  `urlparse` ya no acepta múltiples hosts con el carácter `[]` en la URL. Para mitigar el problema, se pasa a los envoltorios nativos de `PQconninfoParse()` de `libpq` cuando es posible, y nuestra implementación se usa solo para versiones antiguas de `psycopg2` que están enlazadas con una versión desactualizada de `libpq`.

**Correcciones de errores**

- Muestra solo los miembros que se van a reiniciar en la confirmación de reinicio (András Váczi)

  Anteriormente, al ejecutar `patronictl restart <clustername> --pending`, la confirmación listaba todos los miembros, independientemente de si su reinicio estaba pendiente.

- Cancela los trabajos de larga duración al detener Patroni y elimina el directorio de datos ante un fallo del bootstrap de la réplica (Alexander Kukushkin)

  Anteriormente, Patroni podía detenerse durante el bootstrap de una réplica mientras `pg_basebackup` / `wal-g` / `pgBackRest` / `barman` o herramientas similares seguían ejecutándose.

- Maneja correctamente los nombres de clúster con una barra diagonal en `patronictl edit-config` (Antoni Mur)

  Reemplaza una barra diagonal en `cluster_name` por un guion bajo.

- Evita eliminar los slots físicos demasiado pronto (Alexander Kukushkin)

  Aplaza la eliminación de los slots de replicación físicos que contienen `xmin` después de una conmutación por error: en el nuevo primario, hasta que este miembro sea promovido; en las réplicas, hasta que haya un líder en el clúster.

- Maneja todas las excepciones generadas por subprocess en `controldata()` (Alexander Kukushkin)

  Patroni no manejaba correctamente todas las excepciones que posiblemente se generan al invocar la utilidad `pg_controldata`.

- Corrige un error por el que un slot del antiguo líder no se conservaba en la conmutación por error (Alexander Kukushkin)

  Evita depender falsamente de que los miembros estén presentes en el DCS, cuando en la conmutación por error la clave `/member` del antiguo líder expira exactamente al mismo tiempo.

- Corrige un par de errores en la máquina de estados de cuórum (Alexander Kukushkin)

  - Al evaluar si hay nodos sanos para una carrera por el liderazgo, antes de degradar debemos tener en cuenta los requisitos de cuórum. Sin ello, el antiguo líder puede acabar en recuperación rodeado de nodos asíncronos.
  - `QuorumStateResolver` no manejaba correctamente el caso en que un nodo réplica se unía y desconectaba rápidamente.

**Mejoras**

- Mejora el error ante un archivo de configuración vacío o que no sea un diccionario (Julian)

  Lanza una excepción más explícita al validar si el archivo de configuración de Patroni contiene un objeto `Mapping` válido.

--------

## Versión 4.0.4 {#version-404}

Publicado el 2024-11-22

**Mejoras de estabilidad**

- Añade compatibilidad con el módulo `py-consul` (Alexander Kukushkin)

  El módulo `python-consul` lleva mucho tiempo sin mantenimiento, mientras que `py-consul` es el reemplazo oficial. Se conserva la compatibilidad con versiones anteriores de python-consul.

- Añade compatibilidad con el módulo `prettytable>=3.12.0` (Alexander Kukushkin)

  Aborda las advertencias de obsolescencia.

- Compatibilidad con el módulo `ydiff==1.4.2` (Alexander Kukushkin)

  Corrige problemas de compatibilidad con la última versión, restringe la versión en `requirements.txt` e introduce una prueba de compatibilidad con la última versión.

**Correcciones de errores**

- Ejecuta el callback `on_role_change` después de una recuperación fallida del primario (Polina Bungina, Alexander Kukushkin)

  Además, ejecuta el callback `on_role_change` para un primario que no logró iniciarse tras un fallo, para aumentar las probabilidades de que el callback se ejecute, incluso si el posterior inicio como réplica falla.

- Corrige una fuga de hilos en `patronictl list -W` (Alexander Kukushkin)

  Almacena en caché el objeto de instancia del DCS para evitar la fuga de hilos.

- Garantiza que solo se escriban en la cadena de conexión los parámetros soportados (Alexander Kukushkin)

  Patroni solía pasar a la cadena de conexión parámetros introducidos en versiones más recientes, lo que había estado provocando errores de conexión.

--------

## Versión 4.0.3 {#version-403}

Publicado el 2024-10-18

**Correcciones de errores**

- Deshabilita `pgaudit` al crear usuarios para no exponer la contraseña (kviset)

  Patroni registraba las contraseñas de `superuser`, `replication` y `rewind` al crearlas cuando la extensión `pgaudit` estaba habilitada.

- Corrige un problema con configuraciones mixtas: primario con Patroni anterior a v4 y réplicas con v4+ (Alexander Kukushkin)

  Usa el `xlog_location` extraído de la clave `/members` en lugar de intentar obtener la posición del slot de un miembro desde la clave `/status` si la versión de Patroni que se ejecuta en el líder es anterior a 4.0.0. No hacerlo venía causando acumulación de WALs en las réplicas.

- No ignora los GUC válidos de PostgreSQL que no tienen validador en Patroni (Polina Bungina)

  Sigue comprobando contra `postgres --describe-config` si un GUC no tiene un validador de Patroni pero, de hecho, es un GUC válido.

**Mejoras**

- Vuelve a comprobar las anotaciones con el código de estado 409 al leer el objeto de líder en K8s (Alexander Kukushkin)

  Evita una actualización adicional si la solicitud `PATCH` fue cancelada por Patroni, mientras que la solicitud actualizó el destino con éxito.

- Añade soporte para la opción de conexión del lado cliente `sslnegotiation` (Alexander Kukushkin)

  `sslnegotiation` se añadió a la versión final de PostgreSQL 17.

--------

## Versión 4.0.2 {#version-402}

Publicado el 2024-09-17

**Correcciones de errores**

- Maneja las excepciones al descubrir los archivos de validación de la configuración (Alexander Kukushkin)

  Omite los directorios sobre los que Patroni no tiene permisos suficientes para realizar operaciones de listado.

- Garantiza que los slots de replicación físicos hot inactivos no retengan `xmin` (Alexander Kukushkin, Polina Bungina)

  Desde la versión 3.2.0 Patroni crea slots de replicación físicos para todos los miembros en las réplicas y los avanza periódicamente mediante la función `pg_replication_slot_advance()`. Sin embargo, si por cualquier motivo `hot_standby_feedback` está habilitado y el primario se degrada a réplica, los slots ahora inactivos tienen un valor `xmin` `NOT NULL` que se propaga de vuelta al nuevo primario. Esto provoca que el horizonte `xmin` no avance y que vacuum no pueda limpiar las tuplas muertas. Con esta corrección, Patroni recrea los slots de replicación físicos que deberían estar inactivos pero tienen un valor `xmin` `NOT NULL`.

- Corrige un `DCSError` no manejado durante la fase de inicio (Waynerv)

  Garantiza la conectividad con el DCS antes de intentar comprobar la unicidad del nombre del nodo.

- Incluye explícitamente los GUC de `CMDLINE_OPTIONS` al consultar `pg_settings` (Alexander Kukushkin)

  Garantiza que todos los GUC que se pasan al postmaster como parámetros de línea de comandos se restauren cuando Patroni se une a un standby en ejecución. Es el seguimiento del error corregido en Patroni 3.2.2.

- Corrige un error en la lógica de entrecomillado de `synchronous_standby_names` (Alexander Kukushkin)

  Según la documentación de PostgreSQL, las palabras clave `ANY` y `FIRST` deben ir entre comillas dobles, algo que Patroni no hacía antes.

- Corrige un problema de valor fuera de rango en la conexión keepalive (hadizamani021)

  Garantiza que el valor de la opción `keepalive` calculado a partir del `ttl` establecido no exceda el valor máximo permitido para la plataforma actual.

--------

## Versión 4.0.1 {#version-401}

Publicado el 2024-08-30

**Corrección de error**

- Patroni estaba creando slots de replicación innecesarios para sí mismo (Alexander Kukushkin)

  Ocurría si `name` contiene mayúsculas o caracteres especiales.

--------

## Versión 4.0.0 {#version-400}

Publicado el 2024-08-29

> [!WARNING]
> - Esta versión completa el trabajo de eliminar el término "master" en favor de "primary". Esto implica un par de cambios que rompen la compatibilidad; lee las notas de versión con atención. Actualizar a Patroni 4+ funcionará de forma fiable solo si ejecutas Patroni 3.1.0 o posterior. Actualizar desde una versión anterior directamente a 4+ es posible, pero puede provocar un comportamiento inesperado si el primario falla mientras el resto de los nodos ejecutan otras versiones de Patroni.

**Cambios incompatibles**

- Se introdujeron los siguientes cambios incompatibles al eliminar el término no inclusivo "master" del código de Patroni:
  - En Kubernetes, Patroni establecerá por defecto la etiqueta `role` en `primary`. Si deseas conservar el comportamiento antiguo y evitar tiempos de inactividad o migraciones complejas y prolongadas, puedes configurar los parámetros `kubernetes.leader_label_value` y `kubernetes.standby_leader_label_value` en `master`. Lee más [aquí](/es/patroni/kubernetes#kubernetes_role_values).
  - El rol de Patroni se escribe en el DCS como `primary` en lugar de `master`.
  - El rol de Patroni devuelto por la REST API de Patroni cambió de `master` a `primary`.
  - La REST API de Patroni ya no acepta `role=master` en las solicitudes a los endpoints `/switchover`, `/failover`, `/restart`.
  - El endpoint `/metrics` de la REST API ya no reportará la métrica `patroni_master`.
  - [patronictl](/es/patroni/patronictl#patronictl) ya no acepta la opción `--master` para ningún comando. Deben usarse en su lugar las opciones `--leader` o `--primary`.
  - La opción `no_master` en la configuración declarativa de los métodos personalizados de creación de réplicas ya no se trata como una opción especial; usa `no_leader` en su lugar.
  - El script `patroni_wale_restore` ya no acepta la opción `--no_master`.
  - El script `patroni_barman` ya no acepta la opción `--role=master`.
  - Todos los scripts de callback se ejecutan con la opción `role=primary` pasada en lugar de `role=master`.
- `patronictl failover` no acepta la opción `--leader`, obsoleta desde Patroni 3.2.0.
- Se eliminó la funcionalidad de creación de usuarios (sección de configuración `bootstrap.users`), obsoleta desde Patroni 3.2.0.

**Nuevas funcionalidades**

- Conmutación por error basada en cuórum (Ants Aasma, Alexander Kukushkin)

  Esta función implementa la replicación síncrona basada en cuórum (disponible desde PostgreSQL v10), que ayuda a reducir las latencias en el peor de los casos, incluso durante el funcionamiento normal, ya que una mayor latencia al replicar a un standby puede verse compensada por otros standbys. Patroni implementa salvaguardas adicionales para evitar cualquier pérdida de datos visible para el usuario, eligiendo un candidato para la conmutación por error basándose en la última transacción recibida.

- Registra las secundarias de Citus en `pg_dist_node` (Alexander Kukushkin)

  Patroni ahora mantiene en `pg_dist_node` la lista de nodos con `role==replica`, `state==running` y sin la [etiqueta](/es/patroni/config/yaml#tags_settings) `noloadbalance`.

- Retención configurable de los slots de replicación de los miembros (Alexander Kukushkin)

  Implementa soporte del parámetro de configuración global `member_slots_ttl`, que controla durante cuánto tiempo deben conservarse los slots de replicación de los miembros cuando la clave del miembro está ausente.

- Hace configurables los permisos de los archivos de registro creados por Patroni (Alexander Kukushkin)

  Permite establecer permisos específicos para los archivos de registro creados por Patroni. Si no se especifican, los permisos se establecen según el valor de `umask` actual.

- Compatibilidad con PostgreSQL 17 beta3 (Alexander Kukushkin)

  Se ampliaron las reglas del validador de GUC. Patroni maneja todos los nuevos backends auxiliares durante el apagado y establece `dbname` en `primary_conninfo`, como se requiere para la sincronización de los slots de replicación lógica.

- Implementa la opción `--ignore-listen-port` para la validación de la configuración de Patroni (Sahil Naphade)

  Permite ignorar los puertos ya enlazados al ejecutar `patroni --validate-config`.

**Mejoras**

- Hace configurable `wal_log_hints` (Paul_Kim)

  Permite evitar la sobrecarga de tener habilitada la configuración `wal_log_hints` cuando `use_pg_rewind` está establecido en `off`.

- Registra el comando `pg_basebackup` en el nivel `DEBUG` (Waynerv)

  Facilita la depuración de inicializaciones fallidas.

**Correcciones de errores**

- Avanza los slots permanentes de los nodos en cascada durante el modo a prueba de fallos (Alexander Kukushkin)

  Garantiza que los slots de las réplicas en cascada se avancen correctamente en el primario cuando se activa el modo a prueba de fallos. Se logra ampliando la respuesta de las réplicas a la solicitud `POST /failsafe` de la REST API con su `xlog_location`.

- No permite que el nodo actual sea elegido como síncrono (Alexander Kukushkin)

  Puede haber «algo» transmitiendo desde el nodo primario actual con un `application_name` que coincide con el nombre del primario actual. Patroni no manejaba correctamente esta situación, lo que podía terminar en que el primario fuera declarado como nodo síncrono y, en consecuencia, bloqueaba los switchovers.

- Ignora `restapi.allowlist_include_members` para POST /failsafe (Alexander Kukushkin)

- Mejora la validación de GUC (Polina Bungina)

  Debido a la validación adicional mediante la ejecución del comando `postgres --describe-config`, anteriormente no era posible establecer mediante la configuración de Patroni GUC que no estuvieran listados allí. Esta limitación se ha eliminado ahora.

- Añade una línea con `localhost` al archivo `.pgpass` cuando se detectan sockets unix (Alexander Kukushkin)

  Patroni añadirá una línea adicional al archivo `.pgpass` si el parámetro `host` especificado comienza con el carácter `/`. Esto permite cubrir un caso extremo en el que `host` coincide con la ruta del directorio de sockets predeterminado.

- Corrige problemas de registro (Waynerv)

  Define la URL de solicitud correcta en los registros del manejo del modo a prueba de fallos y corrige el orden de las marcas de tiempo en el registro de comprobación del postmaster.

--------

## Versión 3.3.2 {#version-332}

Publicado el 2024-07-11

**Correcciones de errores**

- Corrige el modo de replicación síncrona de Postgres puro (Israel Barth Rubio)

  Desde que se introdujo [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) en Patroni, la replicación síncrona de Postgres pura no funcionaba. Con esta corrección, Patroni establece el valor de `synchronous_standby_names` tal como lo configuró el usuario, si ese es el caso, cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está deshabilitado.

- Maneja la invalidación de slots lógicos en un standby (Polina Bungina)

  Desde PG16 los slots de replicación lógica en un standby pueden invalidarse debido al horizonte: a partir de ahora, Patroni fuerza la copia (es decir, la recreación) de los slots invalidados.

- Corrige una condición de carrera con el avance y la copia de slots lógicos (Alexander Kukushkin)

  Debido a este error, era posible que un slot de replicación lógica invalidado se copiara con reinicio de PostgreSQL más de una vez.

--------

## Versión 3.3.1 {#version-331}

Publicado el 2024-06-17

**Mejoras de estabilidad**

- Compatibilidad con Python 3.12 (Alexander Kukushkin)

  Maneja un nuevo atributo añadido a `logging.LogRecord`.

**Correcciones de errores**

- Corrige una recursión infinita en el manejo de las etiquetas `replicatefrom` (Alexander Kukushkin)

  Como parte de esta corrección, también mejora la comprobación `is_physical_slot()` y ajusta la documentación.

- Corrige el reporte incorrecto del rol en clústeres en espera (Alexander Kukushkin)

  `synchronous_standby_names` y la replicación síncrona solo funcionan en un nodo primario real y, en el caso de la replicación en cascada, simplemente las ignora Postgres. Antes de esta corrección, `patronictl list` y `GET /cluster` reportaban falsamente algunos nodos como síncronos.

- Corrige la disponibilidad del GUC `allow_in_place_tablespaces` (Polina Bungina)

  `allow_in_place_tablespaces` no solo se añadió a PostgreSQL 15, sino que también se retroportó a PostgreSQL 10-14.

--------

## Versión 3.3.0 {#version-330}

Publicado el 2024-04-04

> [!WARNING]
> Todas las versiones antiguas de Patroni no son compatibles con `ydiff>=1.3`.
>
> Existen las siguientes opciones para «arreglar» el problema:
>
> 1.  actualiza Patroni a la última versión
> 2.  instala `ydiff<1.3` después de instalar Patroni
> 3.  instala el módulo `cdiff`

**Nuevas funcionalidades**

- Añade la capacidad de pasar `auth_data` al cliente de Zookeeper (Aras Mumcuyan)

  Permite especificar las credenciales de autenticación a usar para la conexión.

- Añade un script contrib para la integración con `Barman` (Israel Barth Rubio)

  Proporciona una aplicación `patroni_barman` que permite realizar operaciones de `Barman` de forma remota y puede usarse como un método de bootstrap/réplica personalizado o como callback `on_role_change`. Consulta [aquí](/es/patroni/tools_integration#tools_integration) para más información.

- Soporta el formato de registro `JSON` (alisalemmi)

  Además de `plain` (predeterminado), Patroni ahora también soporta el formato de registro `json`. Requiere que la biblioteca `python-json-logger>=2.0.2` esté instalada.

- Muestra información de `pending_restart_reason` (Polina Bungina)

  Proporciona información extendida sobre los parámetros de PostgreSQL que provocaron que se estableciera el indicador `pending_restart`. Tanto `patronictl list` como el endpoint `/patroni` de la REST API ahora muestran los nombres de los parámetros y su «diff» como `pending_restart_reason`.

- Implementa la etiqueta `nostream` (Grigory Smolkin)

  Si la etiqueta `nostream` está establecida en `true`, el nodo no usará el protocolo de replicación para transmitir WAL, sino que dependerá de la recuperación desde el archivado (si `restore_command` está configurado). También deshabilita la copia y sincronización de los slots de replicación lógica permanentes en el propio nodo y en todas sus réplicas en cascada.

**Mejoras**

- Implementa la validación de la sección `log` (Alexander Kukushkin)

  Hasta ahora el validador no comprobaba la corrección de la configuración de registro proporcionada.

- Mejora el registro de los cambios de parámetros de PostgreSQL (Polina Bungina)

  Convierte los valores antiguos a un formato legible por humanos y registra información sobre la discrepancia entre `pg_controldata` y la configuración global de Patroni.

**Correcciones de errores**

- Filtra correctamente las opciones no permitidas de `pg_basebackup` (Israel Barth Rubio)

  Debido a un error, Patroni no filtraba correctamente las opciones no permitidas configuradas para el método de bootstrap de réplica `basebackup`, cuando se proporcionaban en el formato `- setting: value`.

- Corrige el manejo de errores de autenticación de `etcd3` (Alexander Kukushkin)

  Siempre reintenta una vez ante un error de autenticación de `etcd3` si la autenticación no se hizo justo antes de ejecutar la solicitud. Además, no reinicia los watchers al reautenticarse.

- Mejora la lógica de descubrimiento de los archivos del validador (Waynerv)

  Usa la biblioteca `importlib` para descubrir los archivos con los parámetros de configuración disponibles cuando sea posible (para Python 3.9+). Esta implementación es más estable y no rompe las distribuciones de Patroni basadas en archivos `zip`.

- Usa `target_session_attrs` solo cuando se especifican múltiples hosts en la sección [standby_cluster](/es/patroni/standby_cluster#standby_cluster) (Alexander Kukushkin)

  `target_session_attrs=read-write` ahora se añade al `primary_conninfo` en el nodo líder en espera solo cuando la sección `standby_cluster.host` contiene múltiples hosts separados por comas.

- Añade código de compatibilidad para la biblioteca `ydiff` versión 1.3+ (Alexander Kukushkin)

  Patroni depende de algunas API de `ydiff` que no son públicas, ya que se supone que es solo una herramienta de terminal y no un módulo de python. Lamentablemente, el cambio de API en 1.3 rompió las versiones antiguas de Patroni.

--------

## Versión 3.2.2 {#version-322}

Publicado el 2024-01-17

**Correcciones de errores**

- No permite que una réplica restaure la clave de inicialización cuando se ha borrado el DCS (Alexander Kukushkin)

  Ocurría en el método donde Patroni debía tomar el control de un clúster de PG independiente.

- Usa lectura consistente al obtener de Consul la clave sync recién actualizada (Alexander Kukushkin)

  Consul no proporciona ninguna interfaz para obtener inmediatamente el `ModifyIndex` de la clave que acabamos de actualizar; por lo tanto, tenemos que realizar una operación de lectura explícita. Dado que las lecturas obsoletas están permitidas por defecto, a veces obteníamos una versión desactualizada de la clave.

- Recarga la configuración de Postgres si un parámetro que requiere reinicio fue restablecido a su valor original (Polina Bungina)

  Anteriormente Patroni no actualizaba la configuración, sino que solo restablecía el `pending_restart`.

- Corrige la lógica invertida errónea del mensaje de confirmación al hacer una conmutación por error a un candidato asíncrono en modo síncrono (Polina Bungina)

  El problema existía solo en [patronictl](/es/patroni/patronictl#patronictl).

- Excluye al líder de los candidatos para la conmutación por error en [patronictl](/es/patroni/patronictl#patronictl) (Polina Bungina)

  Si el clúster está sano, hacer una conmutación por error a un líder existente no tiene efecto.

- Crea la base de datos y la extensión de Citus de forma idempotente (Alexander Kukushkin, Zhao Junwang)

  Permitirá crearlas en el script `post_bootstrap` si es necesario añadir más dependencias a la base de datos de Citus.

- No filtra la etiqueta `nofailover` contradictoria (Polina Bungina)

  La configuración `{nofailover: false, failover_priority: 0}` establecida en un nodo no le permitía participar en la carrera, cuando debería hacerlo, porque la etiqueta `nofailover` debe tener prioridad.

- Corrige un problema con PyInstaller congelado (Sophia Ruan)

  `freeze_support()` se llamaba después de `argparse` y, como resultado, Patroni no podía iniciar Postgres.

- Corrige un error en el generador de configuración para [patronictl](/es/patroni/patronictl#patronictl) y la configuración de [Citus](/es/patroni/citus#citus) (Israel Barth Rubio)

  Impedía que los parámetros de configuración de [patronictl](/es/patroni/patronictl#patronictl) y [Citus](/es/patroni/citus#citus) establecidos mediante variables de entorno se escribieran en la configuración generada.

- Restaura los GUC de recuperación y algunos parámetros gestionados por Patroni al unirse a un standby en ejecución (Alexander Kukushkin)

  Patroni no lograba reiniciar Postgres v12 y posteriores con un error sobre el `port` faltante en una de las estructuras internas.

- Correcciones en torno al indicador `pending_restart` (Polina Bungina)

  No expone `pending_restart` cuando se está en un bootstrap personalizado con `recovery_target_action = promote` o cuando alguien cambió `hot_standby` o `wal_log_hints` usando, por ejemplo, `ALTER SYSTEM`.

--------

## Versión 3.2.1 {#version-321}

Publicado el 2023-11-30

**Correcciones de errores**

- Limita los valores aceptados para el argumento `--format` en [patronictl](/es/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Solía aceptar cualquier cadena arbitraria y no producir salida si el valor no se reconocía.

- Verifica que los nodos réplica recibieron el LSN del checkpoint al apagarse antes de liberar la clave de líder (Alexander Kukushkin)

  Anteriormente, en algunos casos, usábamos el LSN del registro SWITCH al que sigue un CHECKPOINT (si el modo de archivado está habilitado). Como resultado, el antiguo primario a veces tenía que hacer `pg_rewind`, pero no habría pérdida de datos involucrada.

- Hace una solicitud HTTP real al realizar la comprobación de unicidad del nombre del nodo (Alexander Kukushkin)

  Al ejecutar Patroni en contenedores es posible que el tráfico se enrute mediante `docker-proxy`, que escucha en el puerto y acepta conexiones entrantes. Esto provocaba falsos positivos.

- Corrige el soporte de Citus con Etcd v2 (Alexander Kukushkin)

  Patroni no lograba desplegar un nuevo clúster de Citus con Etcd v2.

- Corrige el comportamiento de `pg_rewind` con Postgres v16+ (Alexander Kukushkin)

  El formato de los mensajes de error de `pg_waldump` cambió en v16, lo que provocaba que Patroni llamara a `pg_rewind` incluso cuando no era necesario.

- Corrige un error con el bootstrap personalizado (Alexander Kukushkin)

  Patroni aplicaba erróneamente el argumento `--command`, que es en sí mismo un comando de bootstrap.

- Corrige el problema con los endpoints de comprobación de estado de la REST API (Sophia Ruan)

  Había posibilidades de que, tras un reinicio de Postgres, devolviera el estado `unknown` para Postgres porque las conexiones no se cerraban correctamente.

- Almacena en caché los resultados de salida de `postgres --describe-config` (Waynerv)

  Se usan para determinar qué GUC están disponibles para validar la configuración de PostgreSQL y no esperamos que esta lista cambie mientras Patroni se está ejecutando.

--------

## Versión 3.2.0 {#version-320}

Publicado el 2023-10-25

**Aviso de obsolescencia**

- El soporte de `bootstrap.users` se eliminará en la versión 4.0.0. Si necesitas crear usuarios después de desplegar un clúster nuevo, usa para ello el hook `bootstrap.post_bootstrap`.

**Cambios incompatibles**

- Aplica la regla `loop_wait + 2*retry_timeout <= ttl` y fija en el código los valores mínimos posibles (Alexander Kukushkin)

  Valores mínimos: `loop_wait=2`, `retry_timeout=3`, `ttl=20`. En caso de que los valores sean más pequeños o violen la regla, se ajustan y se escribe una advertencia en los registros de Patroni.

**Nuevas funcionalidades**

- Prioridad de conmutación por error (Mark Pekala)

  Con la ayuda de `tags.failover_priority` ahora es posible hacer que un nodo sea más preferido durante la carrera por el liderazgo. Más detalles en la documentación (ref. etiquetas).

- Implementa `patroni --generate-config [--dsn DSN]` y `patroni --generate-sample-config` (Polina Bungina)

  Permite generar un archivo de configuración para el clúster de PostgreSQL en ejecución o un archivo de configuración de ejemplo para el nuevo clúster de Patroni.

- Usa una conexión dedicada a Postgres para la REST API de Patroni (Alexander Kukushkin)

  Ayuda a evitar el bloqueo del bucle de latido principal si el sistema está bajo carga.

- Enriquece algunos endpoints con el `name` del nodo (sskserk)

  Para el endpoint de monitoreo, `name` se añade junto al `scope`, y para el endpoint de métricas, `name` se añade a las etiquetas.

- Garantiza la distinción estricta entre conmutación por error y switchover (Polina Bungina)

  Es más preciso en los mensajes de registro y permite hacer una conmutación por error a un nodo asíncrono en un clúster síncrono sano.

- Hace que los slots de replicación físicos permanentes se comporten de forma similar a los slots lógicos permanentes (Alexander Kukushkin)

  Crea slots de replicación físicos permanentes en todos los nodos a los que se permite convertirse en líder y usa la función `pg_replication_slot_advance()` para avanzar el `restart_lsn` de los slots en los nodos standby.

- Añade la capacidad de especificar el espacio de nombres mediante el argumento `--dcs` en [patronictl](/es/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Puede ser útil si se usa [patronictl](/es/patroni/patronictl#patronictl) sin un archivo de configuración.

- Añade soporte para parámetros adicionales en la configuración del bootstrap personalizado (Israel Barth Rubio)

  Anteriormente solo era posible añadir argumentos personalizados al `command` y ahora se pueden listar como un mapeo.

**Mejoras**

- Establece el GUC `citus.local_hostname` al mismo valor que Patroni usa para conectarse a Postgres (Alexander Kukushkin)

  Hay casos en que Citus quiere tener una conexión al Postgres local. Por defecto usa `localhost`, que no siempre está disponible.

**Correcciones de errores**

- Ignora el ajuste [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) en un clúster en espera (Polina Bungina)

  Postgres no soporta la replicación síncrona en cascada y no ignorar [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) rompía un switchover en un clúster en espera.

- Maneja SIGCHLD para el callback `on_reload` (Alexander Kukushkin)

  No hacerlo da como resultado un proceso zombi, que solo se recoge cuando se ejecuta el siguiente `on_reload`.

- Maneja el error `AuthOldRevision` al trabajar con Etcd v3 (Alexander Kukushkin, Kenny Do)

  El error se genera si Etcd está configurado para usar JWT y cuando la base de datos de usuarios en Etcd se actualiza.

--------

## Versión 3.1.2 {#version-312}

Publicado el 2023-09-26

**Correcciones de errores**

- Corrige un error con las comprobaciones de `wal_keep_size` (Alexander Kukushkin)

  `wal_keep_size` es un GUC que normalmente tiene una unidad y Patroni no lograba convertir su valor a `int`. Como resultado, el valor de `bootstrap.dcs` no se escribía después en la clave `/config`.

- Detecta y resuelve inconsistencias entre la clave `/sync` y `synchronous_standby_names` (Alexander Kukushkin)

  Normalmente, Patroni actualiza `/sync` y `synchronous_standby_names` en un orden muy específico, pero en caso de un error o cuando alguien restableció manualmente `synchronous_standby_names`, Patroni entraba en un estado inconsistente. Como resultado, era posible que la conmutación por error ocurriera hacia un nodo asíncrono.

- Lee los valores de los GUC al unirse a un Postgres en ejecución (Alexander Kukushkin)

  Al reiniciarse en [pausa](/es/patroni/pause#pause), Patroni descartaba el GUC `synchronous_standby_names` del `postgresql.conf`. Para resolverlo y evitar problemas similares, Patroni leerá el valor del GUC si se está uniendo a un Postgres que ya está en ejecución.

- Silencia advertencias molestas al comprobar la unicidad del nodo (Alexander Kukushkin)

  Los mensajes `WARNING` los produce `urllib3` si Patroni se reinicia rápidamente.

--------

## Versión 3.1.1 {#version-311}

Publicado el 2023-09-20

**Correcciones de errores**

- Restablece el estado del modo a prueba de fallos al promover (ChenChangAo)

  Si un switchover/conmutación por error ocurría poco después de que se activara el modo a prueba de fallos, el primario recién promovido se degradaba a sí mismo cuando el modo a prueba de fallos se volvía inactivo.

- Silencia advertencias inútiles en [patronictl](/es/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Si [patronictl](/es/patroni/patronictl#patronictl) usa el mismo archivo patroni.yaml que Patroni y puede acceder al directorio `PGDATA`, podría haber estado mostrando advertencias molestas sobre valores incorrectos en la configuración global.

- Habilita explícitamente el modo síncrono para un caso extremo (Alexander Kukushkin)

  El modo síncrono en la práctica nunca se activaba si no hay réplicas transmitiendo desde el primario.

- Corrige un error con la validación de valores enteros `0` (Israel Barth Rubio)

  En la mayoría de los casos no causaba ningún problema, solo advertencias.

- No devuelve slots lógicos para el clúster en espera (Alexander Kukushkin)

  Patroni no puede crear slots de replicación lógica en el clúster en espera; por lo tanto, deben ignorarse si están definidos en la configuración global.

- Evita mostrar la docstring en la salida de `patronictl --help` (Israel Barth Rubio)

  El módulo `click` necesita recibir una pista especial para ello.

- Corrige un error con `kubernetes.standby_leader_label_value` (Alexander Kukushkin)

  Esta función en la práctica nunca funcionó.

- Devuelve el identificador de sistema del clúster a la salida de `patronictl list` (Polina Bungina)

  El problema se introdujo al implementar el soporte de Citus, donde necesitamos ocultar el identificador porque es diferente para el coordinador y para todos los workers.

- Sobrescribe el método `write_leader_optime` en la implementación de Kubernetes (Alexander Kukushkin)

  Se supone que el método escribe el LSN de apagado en el Endpoint/ConfigMap del líder cuando no hay réplicas sanas disponibles para convertirse en el nuevo primario.

- No inicia el postgres detenido en pausa (Alexander Kukushkin)

  Debido a una condición de carrera, Patroni asumía falsamente que el standby debía reiniciarse porque algunos parámetros de recuperación (`primary_conninfo` o similares) habían cambiado.

- Corrige un error en el comando `patronictl query` (Israel Barth Rubio)

  No funcionaba cuando solo se proporcionaba el argumento `-m` o cuando no se proporcionaba ni `-r` ni `-m`.

- Trata correctamente los parámetros enteros que se usan en la línea de comandos para iniciar postgres (Polina Bungina)

  Si los valores se suministran como cadenas y no se convierten a entero, daba como resultado un cálculo incorrecto de `max_prepared_transactions` a partir de `max_connections` para clústeres de Citus.

- No depende de `pg_stat_wal_receiver` al decidir sobre `pg_rewind` (Alexander Kukushkin)

  Podía ocurrir que el `received_tli` reportado por `pg_stat_wal_receiver` esté por delante de la línea de tiempo realmente reproducida, mientras que la línea de tiempo reportada por `IDENTIFY_SYSTEM` mediante la conexión de replicación siempre es correcta.

--------

## Versión 3.1.0 {#version-310}

Publicado el 2023-08-03

**Cambios incompatibles**

- Cambió la semántica de `restapi.keyfile` y `restapi.certfile` (Alexander Kukushkin)

  Anteriormente, Patroni usaba `restapi.keyfile` y `restapi.certfile` como certificados de cliente a modo de alternativa si no había parámetros de configuración respectivos en la sección `ctl`.

> [!WARNING]
> Si habilitaste la validación de certificados de cliente (`restapi.verify_client` está establecido en `required`), también **debes** proporcionar **certificados de cliente válidos** en `ctl.certfile`, `ctl.keyfile`, `ctl.keyfile_password`. Si no se proporcionan, Patroni no funcionará correctamente.

**Nuevas funcionalidades**

- Hace configurable la etiqueta de rol del Pod (Waynerv)

  Los valores podían personalizarse usando los parámetros `kubernetes.leader_label_value`, `kubernetes.follower_label_value` y `kubernetes.standby_leader_label_value`. Esta función será muy útil cuando cambiemos el rol `master` por el `primary`. Puedes leer más sobre la función y los pasos de migración [aquí](/es/patroni/kubernetes#kubernetes_role_values).

**Mejoras**

- Diversas mejoras de `patroni --validate-config` (Alexander Kukushkin)

  Mejora la validación de parámetros para las secciones de los diferentes DCS, `bootstrap.dcs`, `ctl`, `restapi` y [watchdog](/es/patroni/watchdog#watchdog).

- Inicia Postgres sin recuperación si falló durante la recuperación mientras Patroni se está ejecutando (Alexander Kukushkin)

  Puede reducir el tiempo de recuperación y ayudar a prevenir incrementos innecesarios de la línea de tiempo.

- Evita actualizaciones innecesarias de la clave `/status` (Alexander Kukushkin)

  Cuando no hay slots lógicos permanentes, Patroni actualizaba el `/status` en cada ciclo de latido incluso cuando el LSN en el primario no avanzaba.

- No permite que un primario obsoleto gane la carrera por el liderazgo (Alexander Kukushkin)

  Si Patroni se quedó colgado durante un tiempo significativo por falta de recursos, comprobará adicionalmente que ningún otro nodo haya promovido Postgres antes de adquirir el bloqueo de líder.

- Implementa la visibilidad de la validación de ciertos parámetros de PostgreSQL (Alexander Kukushkin, Feike Steenbergen)

  Si la validación de `max_connections`, `max_wal_senders`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_replication_slots` o `max_worker_processes` fallaba, Patroni usaba algún valor predeterminado razonable. Ahora, además de eso, también mostrará una advertencia.

- Establece permisos para los archivos y directorios creados en `PGDATA` (Alexander Kukushkin)

  Todos los archivos creados por Patroni tenían solo permisos de lectura/escritura para el propietario. Este comportamiento rompía las herramientas de copia de seguridad que se ejecutan bajo un usuario diferente y dependen de permisos de lectura de grupo. Ahora Patroni respeta los permisos de `PGDATA` y establece correctamente los permisos de todos los directorios y archivos que crea dentro de `PGDATA`.

**Correcciones de errores**

- Ejecuta `archive_command` a través del shell (Waynerv)

  Patroni podría archivar algunos segmentos de WAL antes de hacer la recuperación ante fallos en modo usuario único o antes de `pg_rewind`. Si archive_command contiene algunos operadores de shell, como `&&`, no funcionaba con Patroni.

- Corrige las comprobaciones de apagado en el switchover (Polina Bungina)

  Era posible que el candidato especificado todavía estuviera transmitiendo y no hubiera recibido el checkpoint de apagado, pero la clave de líder se eliminaba porque otros nodos estaban sanos.

- Corrige la comprobación «es primario» (Alexander Kukushkin)

  Durante la carrera por el liderazgo, las réplicas no podían reconocer que Postgres en el antiguo líder todavía se ejecuta como primario.

- Corrige `patronictl list` (Alexander Kukushkin)

  Faltaba el campo del nombre del clúster en los formatos de salida `tsv`, `json` y `yaml`.

- Corrige el comportamiento de `pg_rewind` después de la pausa (Alexander Kukushkin)

  Bajo ciertas condiciones, Patroni no podía reincorporar al clúster el falso primario con `pg_rewind` después de salir del modo de mantenimiento.

- Corrige un error en la implementación de Etcd v3 (Alexander Kukushkin)

  Invalida la caché KV interna si una actualización de clave usando el campo `create_revision`/`mod_revision` falla debido a una discrepancia de revisión.

- Corrige el comportamiento de las réplicas en el clúster en espera en pausa (Alexander Kukushkin)

  Cuando la clave de líder expira, las réplicas del clúster en espera no seguirán el nodo remoto, sino que mantendrán `primary_conninfo` tal como está.

--------

## Versión 3.0.4 {#version-304}

Publicado el 2023-07-13

**Nuevas funcionalidades**

- Hace visible el estado de replicación de los nodos standby (Alexander Kukushkin)

  Para PostgreSQL 9.6+, Patroni reportará el estado de replicación como `streaming` cuando el standby está transmitiendo desde el otro nodo, o `in archive recovery` cuando no hay conexión de replicación y `restore_command` está establecido. El estado es visible en las claves `member` del DCS, en la REST API y en la salida de `patronictl list`.

**Mejoras**

- Mejora los mensajes de error con Etcd v3 (Alexander Kukushkin)

  Cuando el clúster de Etcd v3 no era accesible, Patroni reportaba que no puede acceder a los endpoints `/v2`.

- Usa lectura de cuórum en [patronictl](/es/patroni/patronictl#patronictl) si es posible (Alexander Kukushkin)

  Los clústeres de Etcd o Consul podrían degradarse a solo lectura, pero desde el punto de vista de [patronictl](/es/patroni/patronictl#patronictl) todo estaba bien. Ahora fallará con el error.

- Previene el split-brain por nombres duplicados en la configuración (Mark Pekala)

  Al iniciar, Patroni comprobará si un nodo con el mismo nombre está registrado en el DCS e intentará consultar su REST API. Si la REST API es accesible, Patroni termina con un error. Ayudará a protegerse de los errores humanos.

- Inicia Postgres sin recuperación si falló mientras Patroni se está ejecutando (Alexander Kukushkin)

  Puede reducir el tiempo de recuperación y ayudar a evitar incrementos innecesarios de la línea de tiempo.

**Correcciones de errores**

- El certificado SSL de la REST API no se recargaba al recibir un SIGHUP (Israel Barth Rubio)

  La regresión se introdujo en 3.0.3.

- Corrige la validación de GUC enteros para parámetros como `max_connections` (Feike Steenbergen)

  A Patroni no le gustaban los valores numéricos entre comillas. La regresión se introdujo en 3.0.3.

- Corrige un problema con [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) (Alexander Kukushkin)

  Ejecuta `txid_current()` con `synchronous_commit=off` para que no espere accidentalmente por standbys síncronos ausentes cuando `synchronous_mode_strict` está habilitado.

--------

## Versión 3.0.3 {#version-303}

Publicado el 2023-06-22

**Nuevas funcionalidades**

- Compatibilidad con PostgreSQL 16 beta1 (Alexander Kukushkin)

  Amplía las reglas del validador de GUC.

- Hace extensible el validador de GUC de PostgreSQL (Israel Barth Rubio)

  Las reglas del validador se cargan desde archivos YAML ubicados en el directorio `patroni/postgresql/available_parameters/`. Los archivos se ordenan alfabéticamente y se aplican uno tras otro. Posibilita tener validadores personalizados para distribuciones de Postgres no estándar.

- Añade la opción `restapi.request_queue_size` (Andrey Zhidenkov, Aleksei Sukhov)

  Establece el tamaño de la cola de solicitudes para el socket TCP usado por la REST API de Patroni. Una vez que la cola está llena, las solicitudes posteriores reciben un error "Connection denied". El valor predeterminado es 5.

- Llama a `initdb` directamente al inicializar un clúster nuevo (Matt Baker)

  Anteriormente se llamaba mediante `pg_ctl`, lo que requería un entrecomillado especial de los parámetros pasados a `initdb`.

- Añade el hook before stop (Le Duane)

  El hook puede configurarse mediante `postgresql.before_stop` y se ejecuta justo antes de `pg_ctl stop`. El código de salida no afecta al proceso de apagado.

- Añade soporte para nombres de binarios de Postgres personalizados (Israel Barth Rubio, Polina Bungina)

  Al usar una distribución de Postgres personalizada, puede ocurrir que los binarios de Postgres se compilen con nombres diferentes a los usados por la distribución de Postgres de la comunidad. Los nombres de binarios personalizados pueden configurarse usando los ajustes de configuración `postgresql.bin_name.*` y las variables de entorno `PATRONI_POSTGRESQL_BIN_*`.

**Mejoras**

- Diversas mejoras de `patroni --validate-config` (Polina Bungina)

  - Hace opcional `bootstrap.initdb`. Solo es necesario para clústeres nuevos, pero `patroni --validate-config` se quejaba si faltaba en la configuración.
  - No falla con un error cuando `postgresql.bin_dir` está vacío o no está establecido. En su lugar, intenta primero encontrar los binarios de Postgres en el PATH predeterminado.
  - Hace opcional la sección `postgresql.authentication.rewind`. Si falta, Patroni usa el superusuario.

- Mejora el reporte de errores en [patronictl](/es/patroni/patronictl#patronictl) (Israel Barth Rubio)

  El símbolo `\n` se mostraba tal cual, en lugar del símbolo real de nueva línea.

**Correcciones de errores**

- Corrige un problema en el soporte de Citus (Alexander Kukushkin)

  Si la llamada a la REST API del worker promovido al coordinador fallaba durante un switchover, dejaba bloqueado durante un tiempo indefinido al grupo de Citus dado.

- Permite la URL `etcd3` en la opción `--dcs-url` de [patronictl](/es/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Si los usuarios intentaban pasar una URL `etcd3` a través de la opción `--dcs-url` de [patronictl](/es/patroni/patronictl#patronictl), se encontraban con una excepción.

--------

## Versión 3.0.2 {#version-302}

Publicado el 2023-03-24

> [!WARNING]
> La versión 3.0.2 eliminó el soporte de Python anterior a 3.6.

**Nuevas funcionalidades**

- Añade el estado de réplica standby síncrona al endpoint `/metrics` (Thomas von Dein, Alexander Kukushkin)

  Antes solo se reportaba `primary`/`standby_leader`/`replica`.

- Manejo amigable de `PAGER` en [patronictl](/es/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Hace configurable el paginador mediante la variable de entorno `PAGER`, que anula los valores predeterminados `less` y `more`.

- Hace configurable el código de estado HTTP reintentable de K8s (Alexander Kukushkin)

  En algunas plataformas gestionadas es posible obtener el código de estado `401 Unauthorized`, que a veces se resuelve después de unos pocos reintentos.

**Mejoras**

- Establece `hot_standby` en `off` durante el bootstrap personalizado solo si `recovery_target_action` está establecido en `promote` (Alexander Kukushkin)

  Era necesario para que `recovery_target_action=pause` funcionara correctamente.

- No permite que el callback `on_reload` termine con otros callbacks (Alexander Kukushkin)

  `on_start`/`on_stop`/`on_role_change` suelen usarse para añadir/eliminar la IP virtual y `on_reload` no debería interferir con ellos.

- Cambió a `IMDSFetcher` en el script de ejemplo del callback de aws (Polina Bungina)

  `IMDSv2` requiere un token para funcionar y `IMDSFetcher` lo maneja de forma transparente.

**Correcciones de errores**

- Corrige `patronictl switchover` en un clúster de Citus ejecutándose en Kubernetes (Lukáš Lalinský)

  No funcionaba para espacios de nombres diferentes de `default`.

- No escribe en `PGDATA` si no se conoce la versión principal (Alexander Kukushkin)

  Si justo después del inicio `PGDATA` estaba vacío (quizás aún no se había montado), Patroni hacía una suposición falsa sobre la versión de PostgreSQL y creaba falsamente el archivo `recovery.conf` aunque la versión principal real fuera v10+.

- Corrige un error con los metadatos de Citus después de una conmutación por error del coordinador (Alexander Kukushkin)

  La llamada a `citus_set_coordinator_host()` no provoca la sincronización de metadatos y el cambio era invisible en los nodos worker. El problema se resuelve cambiando a `citus_update_node()`.

- Usa los hosts de etcd listados en el archivo de configuración como alternativa cuando todos los nodos de etcd «fallaron» (Alexander Kukushkin)

  El clúster de etcd puede cambiar de topología con el tiempo y Patroni intenta seguirlo. Si en algún momento todos los nodos se volvían inalcanzables, Patroni usará una combinación de los nodos de la configuración más la última topología conocida al intentar reconectarse.

--------

## Versión 3.0.1 {#version-301}

Publicado el 2023-02-16

**Correcciones de errores**

- Pasa el nombre de rol correcto a un script de callback `on_role_change`. (Alexander Kukushkin, Polina Bungina)

  Patroni solía pasar erróneamente el rol `promoted` a un script de callback `on_role_change` al promover. El nombre de rol pasado volvió a ser `master`. Esta regresión se introdujo en 3.0.0.

--------

## Versión 3.0.0 {#version-300}

Publicado el 2023-01-30

Esta versión añade la integración con [Citus](https://www.citusdata.com) y hace posible sobrevivir a interrupciones temporales del DCS sin degradar el primario.

> [!WARNING]
> - La versión 3.0.0 es la última versión con soporte de Python 2.7. La próxima versión eliminará el soporte de versiones de Python anteriores a 3.7.
>
> - El soporte de RAFT está obsoleto. Haremos todo lo posible por mantenerlo, pero no ofrecemos ni garantía ni responsabilidad por posibles problemas.
> - Esta versión es el primer paso para eliminar "master" en favor de "primary". Actualizar a la siguiente versión principal funcionará de forma fiable solo si ejecutas al menos la 3.0.0.

**Nuevas funcionalidades**

- Modo a prueba de fallos del DCS (Alexander Kukushkin, Polina Bungina)

  Si la función está habilitada, permitirá que el clúster de Patroni sobreviva a interrupciones temporales del DCS. Puedes encontrar más detalles en la [documentación](/es/patroni/dcs_failsafe_mode#dcs_failsafe_mode).

- Soporte de Citus (Alexander Kukushkin, Polina Bungina, Jelte Fennema)

  Patroni permite el despliegue y la gestión sencillos de clústeres de [Citus](https://www.citusdata.com) con HA. Consulta la página [aquí](/es/patroni/citus#citus) para más información.

**Mejoras**

- Suprime los errores recurrentes al eliminar slots de replicación desconocidos pero activos (Michael Banck)

  Patroni seguirá escribiendo estos registros, pero solo en DEBUG.

- Ejecuta solo una consulta de monitoreo por ciclo de HA (Alexander Kukushkin)

  No era el caso si la replicación síncrona está habilitada.

- Conserva solo el último directorio de datos fallido (William Albertus Dembo)

  Si el bootstrap fallaba, Patroni solía renombrar la carpeta \$PGDATA con un sufijo de marca de tiempo. A partir de ahora el sufijo será `.failed` y si dicha carpeta existe, se elimina antes de renombrar.

- Mejora la comprobación de las conexiones de replicación síncrona (Alexander Kukushkin)

  Cuando se añade un nuevo host a `synchronous_standby_names`, se establecerá como síncrono en el DCS solo cuando haya logrado ponerse al día con el primario, además de `pg_stat_replication.sync_state = 'sync'`.

**Funcionalidad eliminada**

- Elimina `patronictl scaffold` (Alexander Kukushkin)

  La única razón de su existencia era una forma improvisada de ejecutar clústeres en espera.

--------

## Versión 2.1.7 {#version-217}

Publicado el 2023-01-04

**Correcciones de errores**

- Corrige pequeñas incompatibilidades con módulos de python antiguos (Alexander Kukushkin)

  Impedían compilar/ejecutar Patroni en Debian buster/Ubuntu bionic.

--------

## Versión 2.1.6 {#version-216}

Publicado el 2022-12-30

**Mejoras**

- Corrige excepciones molestas al cerrar el socket ssl (Alexander Kukushkin)

  HAProxy cierra las conexiones tan pronto como recibe el código de estado HTTP, sin dejar tiempo a Patroni para cerrar correctamente la conexión SSL.

- Ajusta el Dockerfile de ejemplo para arm64 (Polina Bungina)

  Elimina `amd64` y `x86_64` explícitos, no elimina `libnss_files.so.*`.

**Mejoras de seguridad**

- Aplica `search_path=pg_catalog` para las conexiones que no son de replicación (Alexander Kukushkin)

  Dado que Patroni depende en gran medida de conexiones de superusuario, queremos protegerlo de los posibles ataques llevados a cabo mediante funciones y/u operadores definidos por el usuario en el esquema `public` con el mismo nombre y firma que los objetos correspondientes en `pg_catalog`. Para ello, se aplica `search_path=pg_catalog` a todas las conexiones creadas por Patroni (excepto las conexiones de replicación).

- Evita que las contraseñas queden registradas en `pg_stat_statements` (Feike Steenbergen)

  Se logra estableciendo `pg_stat_statements.track_utility=off` al crear usuarios.

**Correcciones de errores**

- Declara `proxy_address` como opcional (Denis Laxalde)

  Ya que en la práctica es una opción no requerida.

- Mejora el comportamiento de la opción insecure (Alexander Kukushkin)

  La opción `insecure` de Ctl no funcionaba correctamente cuando se usaban certificados de cliente para las solicitudes a la REST API.

- Toma la configuración del watchdog de `bootstrap.dcs` cuando se inicializa el clúster nuevo (Matt Baker)

  Patroni solía configurar inicialmente el watchdog con valores predeterminados al inicializar un clúster nuevo, en lugar de tomar la configuración usada para inicializar el DCS.

- Corrige la forma en que se tratan las extensiones de archivo al buscar ejecutables en WIN32 (Martín Marqués)

  Solo añade `.exe` a un nombre de archivo si aún no tiene extensión.

- Corrige la configuración del TTL de Consul (Alexander Kukushkin)

  Usábamos `ttl/2.0` al establecer el valor en el HTTPClient, pero olvidamos multiplicar el valor actual por 2 en la propiedad de la clase. Esto daba como resultado un TTL de Consul desviado por un factor de 2.

**Funcionalidad eliminada**

- Elimina `patronictl configure` (Polina Bungina)

  Ya no hay necesidad de una creación separada de la configuración de [patronictl](/es/patroni/patronictl#patronictl).

--------

## Versión 2.1.5 {#version-215}

Publicado el 2022-11-28

Esta versión mejora la compatibilidad con PostgreSQL 15 y declara el soporte de Etcd v3 como listo para producción. Patroni sobre Raft permanece en Beta.

**Nuevas funcionalidades**

- Mejora `patroni --validate-config` (Denis Laxalde)

  Termina con el código 1 si la configuración no es válida e imprime los errores en stderr.

- No elimina los slots de replicación en pausa (Alexander Kukushkin)

  Patroni crea/elimina automáticamente los slots de replicación físicos cuando los miembros se unen al/dejan el clúster. En pausa, los slots ya no se eliminarán.

- Soporta el método de solicitud `HEAD` para los endpoints de monitoreo (Robert Cutajar)

  Si se usa en lugar de `GET`, Patroni devolverá solo el código de estado HTTP.

- Soporta las pruebas behave en Windows (Alexander Kukushkin)

  Emula el apagado elegante de Patroni (`SIGTERM`) en Windows introduciendo el nuevo endpoint de la REST API `POST /sigterm`.

- Presenta `postgresql.proxy_address` (Alexander Kukushkin)

  Se escribirá en la clave del miembro en el DCS como `proxy_url` y podría usarse/ser útil para el descubrimiento de servicios.

**Mejoras de estabilidad**

- Llama a `pg_replication_slot_advance()` desde un hilo (Alexander Kukushkin)

  En clústeres ocupados con muchos slots de replicación lógica, la llamada a `pg_replication_slot_advance()` afectaba el bucle principal de HA y podía provocar la expiración de la clave del miembro.

- Archiva los WAL que posiblemente falten antes de llamar a `pg_rewind` en el antiguo primario (Polina Bungina)

  Si el primario falló y estuvo caído durante un tiempo considerable, podrían faltar algunos archivos WAL en el archivado y en el nuevo primario. Existe la posibilidad de que `pg_rewind` eliminara estos archivos WAL del antiguo primario, haciendo imposible iniciarlo como standby. Al archivar los archivos WAL `ready` no solo mitigamos este problema, sino que en general mejoramos la experiencia de archivado continuo.

- Ignora los errores `403` al intentar crear el Service de Kubernetes (Nick Hudson, Polina Bungina)

  Patroni saturaba los registros con intentos fallidos de crear el servicio, que de hecho podría ya existir.

- Mejora la sonda de liveness (Alexander Kukushkin)

  La sonda de liveness comenzará a fallar si el bucle de latido se ejecuta durante más de `ttl` en el primario o `2*ttl` en la réplica. Eso nos permitirá usarla como alternativa al [watchdog](/es/patroni/watchdog#watchdog) en Kubernetes.

- Garantiza que solo el nodo síncrono intente tomar el bloqueo durante un switchover (Alexander Kukushkin, Polina Bungina)

  Anteriormente había una pequeña probabilidad de que un miembro asíncrono actualizado se convirtiera en líder si el switchover manual se realizaba sin especificar el destino.

- Evita la clonación mientras el bootstrap se está ejecutando (Ants Aasma)

  No permite que se active un método de creación de réplica que no requiere líder mientras el bootstrap del clúster se está ejecutando.

- Compatibilidad con kazoo-2.9.0 (Alexander Kukushkin)

  Dependiendo de la versión de python, el método `SequentialThreadingHandler.select()` puede generar excepciones `TypeError` e `IOError` si se llama a `select()` sobre el socket cerrado.

- Cierra explícitamente la conexión SSL antes de cerrar el socket (Alexander Kukushkin)

  No hacerlo daba como resultado errores `unexpected eof while reading` con OpenSSL 3.0.

- Compatibilidad con `prettytable>=2.2.0` (Alexander Kukushkin)

  Debido a los cambios en la API interna, el encabezado del nombre del clúster se mostraba en la línea incorrecta.

**Correcciones de errores**

- Maneja el token expirado para lease_grant de Etcd (monsterxx03)

  En caso de error, obtiene el nuevo token y reintenta la solicitud.

- Corrige un error en el endpoint `GET /read-only-sync` (Alexander Kukushkin)

  Se introdujo en la versión anterior y en la práctica nunca funcionó.

- Maneja el caso en que el almacenamiento del directorio de datos desapareció (Alexander Kukushkin)

  Patroni comprueba periódicamente que el PGDATA esté presente y no esté vacío, pero en caso de problemas con el almacenamiento, `os.listdir()` genera la excepción `OSError`, rompiendo el bucle de latido.

- Aplica `master_stop_timeout` al esperar que se cierren los backends de usuario (Alexander Kukushkin)

  Algo que parece un backend de usuario podría ser de hecho un worker en segundo plano (p. ej., el demonio de mantenimiento de Citus) que no logra detenerse.

- Acepta `*:<port>` para `postgresql.listen` (Denis Laxalde)

  `patroni --validate-config` se quejaba de que era inválido.

- Correcciones de tiempos de espera en Raft (Alexander Kukushkin)

  Cuando Patroni o patronictl se inician, intentan obtener la topología del clúster de Raft de los miembros conocidos. Estas llamadas se hacían sin los tiempos de espera adecuados.

- Actualiza forzosamente el servicio de consul si el token cambió (John A. Lotoski)

  No hacerlo da como resultado los errores "rpc error making call: rpc error making call: ACL not found".

--------

## Versión 2.1.4 {#version-214}

Publicado el 2022-06-01

**Nuevas funcionalidades**

- Mejora el comportamiento de `pg_rewind` en sistemas Debian/Ubuntu típicos (Gunnar "Nick" Bluth)

  En configuraciones de Postgres que mantienen `postgresql.conf` fuera del directorio de datos (p. ej., los paquetes de Ubuntu/Debian), `pg_rewind --restore-target-wal` no logra determinar el valor de `restore_command`.

- Permite establecer `TLSServerName` en las comprobaciones de servicio de Consul (Michael Gmelin)

  Útil cuando las comprobaciones se realizan por IP y el `node_name` de Consul no es un FQDN.

- Añade soporte de `ppc64le` en el watchdog (Jean-Michel Scheiwiler)

  Y corrige el soporte del watchdog en algunas plataformas que no son x86.

- Cambió el callback aws.py de `boto` a `boto3` (Alexander Kukushkin)

> `boto` 2.x está abandonado desde 2018 y falla con python 3.9.

- Refresca periódicamente el token de la cuenta de servicio en K8s (Haitao Li)

  Desde Kubernetes v1.21 los tokens de las cuentas de servicio expiran en 1 hora.

- Añade el endpoint de monitoreo `/read-only-sync` (Dennis4b)

  Es similar al `/read-only`, pero incluye solo réplicas síncronas.

**Mejoras de estabilidad**

- No copia el slot de replicación lógica a una réplica si hay una discrepancia de configuración en la configuración de decodificación lógica con el primario (Alexander Kukushkin)

  Una réplica ya no copiará un slot de replicación lógica del primario si el slot no coincide con las opciones de configuración `plugin` o `database`. Anteriormente, la comprobación de si el slot coincidía con esas opciones de configuración no se realizaba hasta después de que la réplica copiara el slot e iniciara con él, lo que provocaba reinicios innecesarios y repetidos.

- Manejo especial de los parámetros de configuración de recuperación para PostgreSQL v12+ (Alexander Kukushkin)

  Al iniciarse como réplica, Patroni debe poder actualizar `postgresql.conf` y reiniciar/recargar si la dirección del líder cambió, almacenando en caché los valores actuales de los parámetros en lugar de consultarlos en `pg_settings`.

- Mejor manejo de las direcciones IPv6 en los parámetros `postgresql.listen` (Alexander Kukushkin)

  Como el parámetro `listen` incluye un puerto, la gente intenta poner las direcciones IPv6 entre corchetes, que no se eliminaban correctamente cuando hay más de una IP en la lista.

- Usa las credenciales de `replication` al realizar la comprobación de divergencia solo en PostgreSQL v10 y anteriores (Alexander Kukushkin)

  Si `rewind` está habilitado, Patroni volverá a usar las credenciales de `superuser` o de `rewind` en versiones más recientes de Postgres.

**Correcciones de errores**

- Corrige la importación faltante de `dateutil.parser` (Wesley Mendes)

  Las pruebas no fallaban solo porque también se importaba desde otros módulos.

- Garantiza que la anotación `optime` sea una cadena (Sebastian Hasler)

  En ciertos casos Patroni intentaba pasarla como numérica.

- Mejor manejo de un intento fallido de `pg_rewind` (Alexander Kukushkin)

  Si el primario deja de estar disponible durante `pg_rewind`, `$PGDATA` quedará en un estado roto. A continuación, Patroni eliminará el directorio de datos incluso si la configuración no lo permite.

- No elimina las anotaciones `slots` del `ConfigMap`/`Endpoint` del líder cuando PostgreSQL no está listo (Alexander Kukushkin)

  Si no se pasa el valor de `slots`, la anotación mantendrá el valor actual.

- Maneja un problema de concurrencia con los watchers de la API de K8s (Alexander Kukushkin)

  Bajo ciertas condiciones (desconocidas), los watchers podrían quedar obsoletos; como resultado, el método `attempt_to_acquire_leader()` podía fallar con el código de estado HTTP 409. En ese caso restablecemos las conexiones de los watchers y reiniciamos desde cero.

--------

## Versión 2.1.3 {#version-213}

Publicado el 2022-02-18

**Nuevas funcionalidades**

- Añade soporte para claves TLS cifradas para [patronictl](/es/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Podía configurarse mediante `ctl.keyfile_password` o la variable de entorno `PATRONI_CTL_KEYFILE_PASSWORD`.

- Añade más métricas al endpoint /metrics (Alexandre Pereira)

  Concretamente, `patroni_pending_restart` y `patroni_is_paused`.

- Permite especificar múltiples hosts en la configuración del clúster en espera (Michael Banck)

  Si el clúster en espera replica desde el clúster de Patroni, puede ser bueno confiar en la conmutación por error del lado del cliente, disponible en `libpq` desde PostgreSQL v10. Es decir, el `primary_conninfo` en el líder en espera y `pg_rewind` estableciendo `target_session_attrs=read-write` en la cadena de conexión. El archivo `pgpass` se generará con múltiples líneas (una línea por host) y, en lugar de llamar a `CHECKPOINT` en los nodos del clúster primario, el clúster en espera esperará a que se actualice `pg_control`.

**Mejoras de estabilidad**

- Compatibilidad con `psycopg2` antiguos (Alexander Kukushkin)

  Por ejemplo, el `psycopg2` instalado desde los paquetes de Ubuntu 18.04 todavía no tiene la excepción `UndefinedFile`.

- Reinicia el watcher de `etcd3` si todos los nodos de Etcd no responden (Alexander Kukushkin)

  Si el watcher está vivo, el método `get_cluster()` sigue devolviendo información obsoleta incluso si todos los nodos de Etcd están fallando.

- No elimina el bloqueo de líder en el clúster en espera durante la pausa (Alexander Kukushkin)

  Anteriormente, el bloqueo lo mantenía solo el nodo que se ejecutaba como primario y no como líder en espera.

**Correcciones de errores**

- Corrige un error en el bootstrap del líder en espera (Alexander Kukushkin)

  Patroni consideraba el bootstrap como fallido si Postgres no comenzaba a aceptar conexiones después de 60 segundos. El error se introdujo en la versión 2.1.2.

- Corrige un error con la conmutación por error a un standby en cascada (Alexander Kukushkin)

  Al determinar qué slots debían crearse en el standby en cascada, olvidamos tener en cuenta que el líder podría estar ausente.

- Corrige pequeños problemas en el validador de configuración de Postgres (Alexander Kukushkin)

  Los parámetros enteros introducidos en PostgreSQL v14 no pasaban la validación porque los valores mínimos y máximos estaban entre comillas en validator.py

- Usa las credenciales de replicación al comprobar el estado del líder (Alexander Kukushkin)

  Podría ser que `remove_data_directory_on_diverged_timelines` esté establecido, pero que no haya `rewind_credentials` definidos y que el acceso de superusuario entre nodos no esté permitido.

- Corrige el error «puerto en uso» al reemplazar el certificado de la REST API (Ants Aasma)

  Al cambiar certificados había una condición de carrera con una solicitud de API concurrente. Si hay una activa durante el período de reemplazo, el reemplazo terminará con un error de puerto en uso y Patroni queda atrapado en un estado sin un servidor de API activo.

- Corrige un error en el bootstrap del clúster si las contraseñas contienen caracteres `%` (Bastien Wirtz)

  El método de bootstrap ejecuta el bloque `DO`, con todos los parámetros correctamente entrecomillados, pero al método `cursor.execute()` no le gustaba que se le pasara una lista vacía con parámetros.

- Corrige la excepción "AttributeError: no attribute 'leader'" (Hrvoje Milković)

  Podía ocurrir si el modo síncrono está habilitado y el contenido del DCS fue borrado.

- Corrige un error en la comprobación de divergencia de líneas de tiempo (Alexander Kukushkin)

  Patroni asumía falsamente que las líneas de tiempo habían divergido. Para pg_rewind no creaba ningún problema, pero si pg_rewind no está permitido y `remove_data_directory_on_diverged_timelines` está establecido, daba como resultado la reinicialización del antiguo líder.

--------

## Versión 2.1.2 {#version-212}

Publicado el 2021-12-03

**Nuevas funcionalidades**

- Compatibilidad con `psycopg>=3.0` (Alexander Kukushkin)

  Por defecto se prefiere `psycopg2`. `psycopg>=3.0` se usará solo si `psycopg2` no está disponible o su versión es demasiado antigua.

- Añade el campo `dcs_last_seen` a la REST API (Michael Banck)

  Este campo anota la última vez (como unix epoch) que un miembro del clúster se comunicó con éxito con el DCS. Es útil para identificar y/o analizar particiones de red.

- Libera el bloqueo de líder cuando `pg_controldata` reporta "shut down" (Alexander Kukushkin)

  Para resolver el problema del switchover/apagado lento en caso de que `archive_command` sea lento/falle, Patroni eliminará la clave de líder inmediatamente después de que `pg_controldata` comenzara a reportar el PGDATA como `shut down` limpiamente y de que verificara que hay al menos una réplica que recibió todos los cambios. Si no hay réplicas que cumplan esta condición, la clave de líder no se elimina y se conserva el comportamiento antiguo, es decir, Patroni seguirá actualizando el bloqueo.

- Añade soporte para el parámetro de conexión `sslcrldir` (Kostiantyn Nemchenko)

  El nuevo parámetro de conexión se introdujo en PostgreSQL v14.

- Permite establecer ACL para los ZNodes en Zookeeper (Alwyn Davis)

  Introduce una nueva opción de configuración `zookeeper.set_acls` para que Kazoo aplique una ACL predeterminada a cada ZNode que crea.

**Mejoras de estabilidad**

- Retrasa el siguiente intento de recuperación hasta el siguiente ciclo de HA (Alexander Kukushkin)

  Si Postgres falló por falta de espacio en disco (por ejemplo) y no logra iniciarse por ello, Patroni intentaba recuperarlo con demasiada insistencia, saturando los registros.

- Añade un registro antes de degradar, lo que puede llevar algún tiempo (Michael Banck)

  La degradación puede tardar algún tiempo en completarse y quizás no sea obvio mirando los registros qué está pasando exactamente.

- Mejora los mensajes de estado "I am" (Michael Banck)

  `no action. I am a secondary ({0})` vs `no action. I am ({0}), a secondary`

- Convierte a entero `wal_keep_segments` al convertir a `wal_keep_size` (Jorge Solórzano)

  Es posible especificar `wal_keep_segments` como una cadena en la [configuración dinámica](/es/patroni/config/dynamic#dynamic) global y, dado que Python es un lenguaje de tipado dinámico, la cadena simplemente se multiplicaba. Ejemplo: `wal_keep_segments: "100"` se convertía en `100100100100100100100100100100100100100100100100MB`.

- Permite el switchover solo a nodos síncronos cuando la replicación síncrona está habilitada (Alexander Kukushkin)

  Además, realiza la carrera por el liderazgo solo contra los nodos síncronos conocidos.

- Usa el rol almacenado en caché como alternativa cuando Postgres es lento (Alexander Kukushkin)

  En algunos casos extremos, Postgres podía ser tan lento que la consulta de monitoreo normal no terminaba en unos segundos. Que la excepción `statement_timeout` no se manejara correctamente podía llevar a una situación en la que Postgres no se degradaba a tiempo cuando la clave de líder expiraba o la actualización fallaba. En caso de tal excepción, Patroni usará el `role` almacenado en caché para determinar si Postgres se está ejecutando como primario.

- Evita actualizaciones innecesarias del ZNode del miembro (Alexander Kukushkin)

  Si ningún valor ha cambiado en los datos de los miembros, la actualización no debería ocurrir.

- Optimiza el checkpoint después de la promoción (Alexander Kukushkin)

  Evita hacer `CHECKPOINT` si la última línea de tiempo ya está almacenada en `pg_control`. Ayuda a evitar un `CHECKPOINT` innecesario justo después de inicializar el clúster nuevo con `initdb`.

- Prefiere miembros sin `nofailover` al elegir nodos síncronos (Alexander Kukushkin)

  Anteriormente, los nodos síncronos se seleccionaban solo en función del lag de replicación; por lo tanto, el nodo con la etiqueta `nofailover` tenía las mismas probabilidades de volverse síncrono que cualquier otro nodo. Ese comportamiento era confuso y peligroso a la vez, porque en caso de fallo del primario la conmutación por error no podía ocurrir automáticamente.

- Elimina los hosts duplicados de la caché de máquinas de etcd (Michael Banck)

  Las URLs de cliente anunciadas en el clúster de etcd podrían estar mal configuradas. Eliminar los duplicados en Patroni en este caso es una mejora sencilla y de bajo costo.

**Correcciones de errores**

- Omite los slots de replicación temporales al hacer la gestión de slots (Alexander Kukushkin)

  Desde v10, `pg_basebackup` crea un slot de replicación temporal para la transmisión de WAL y Patroni intentaba eliminarlo porque el nombre del slot parece desconocido. Para corregirlo, omitimos todos los slots temporales al consultar la vista `pg_replication_slots`.

- Garantiza que `pg_replication_slot_advance()` no exceda el tiempo de espera (Alexander Kukushkin)

  Patroni usaba el `statement_timeout` predeterminado en este caso y, una vez que la llamada fallaba, hay altísimas probabilidades de que nunca se recupere, lo que da como resultado un aumento del tamaño de `pg_wal` e hinchazón de `pg_catalog`.

- El `/status` no se actualizaba al degradar (Alexander Kukushkin)

  Después de degradar PostgreSQL, el antiguo líder actualiza el último LSN en el DCS. A partir de `2.1.0` se introdujo la nueva clave `/status`, pero el optime todavía se escribía en `/optime/leader`.

- Maneja las excepciones del DCS al degradar (Alexander Kukushkin)

  Al degradar el primario por un fallo en la actualización del bloqueo de líder, podía ocurrir que el DCS se caiga por completo y que la llamada `get_cluster()` genere una excepción. Al no manejarse correctamente, da como resultado que Postgres permanezca detenido hasta que el DCS se recupere.

- El `use_unix_socket_repl` no funcionaba en algunos casos (Alexander Kukushkin)

  Concretamente, si `postgresql.unix_socket_directories` no está establecido. En ese caso, se supone que Patroni usa el valor predeterminado de `libpq`.

- Corrige algunos problemas con la REST API de Patroni (Alexander Kukushkin)

  El `clusters_unlocked` a veces podía no estar definido, lo que daba como resultado excepciones en el endpoint `GET /metrics`. Además, el método de manejo de errores asumía que la tupla `connect_address` siempre tiene dos elementos, cuando de hecho podría haber más en el caso de IPv6.

- Espera a que el nodo recién promovido termine la recuperación antes de decidir hacer rewind (Alexander Kukushkin)

  Podía pasar algún tiempo antes de que ocurriera la promoción real y se creara la nueva línea de tiempo. Sin esperar, las réplicas podían llegar a la conclusión de que no se requiere rewind.

- Maneja líneas de tiempo faltantes en un archivo de historial al decidir hacer rewind (Alexander Kukushkin)

  Si la línea de tiempo actual de la réplica falta en el archivo de historial del primario, la réplica asumía falsamente que no se requiere rewind.

--------

## Versión 2.1.1 {#version-211}

Publicado el 2021-08-19

**Nuevas funcionalidades**

- Soporte para el sufijo de nombre SRV de ETCD (David Pavlicek)

  Etcd permite diferenciar entre múltiples clústeres de Etcd bajo el mismo dominio y a partir de ahora Patroni también lo soporta.

- Enriquece el historial con el nuevo líder (huiyalin525)

  Añade la nueva columna a la salida de `patronictl history`.

- Hace configurable el paquete de CA para la configuración de Kubernetes dentro del clúster (Aron Parsons)

  Por defecto, Patroni usa `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt` y esta nueva función permite especificar el `kubernetes.cacert` personalizado.

- Soporta el registro/desregistro dinámico como servicio de Consul y el cambio de etiquetas (Tommy Li)

  Anteriormente requería reiniciar Patroni.

**Correcciones de errores**

- Evita recargas innecesarias de la REST API (Alexander Kukushkin)

  La versión anterior añadió una función de recarga de los certificados de la REST API si cambiaban en el disco. Lamentablemente, la recarga ocurría incondicionalmente justo después del inicio.

- No resuelve los miembros del clúster cuando `etcd.use_proxies` está establecido (Alexander Kukushkin)

  Al iniciarse, Patroni comprueba la salud del clúster de Etcd consultando la lista de miembros. Además, también intentaba resolver sus nombres de host, lo que no es necesario cuando se trabaja con Etcd mediante proxy y causaba advertencias innecesarias.

- Omite las filas con valores NULL en `pg_stat_replication` (Alexander Kukushkin)

  Parece que la vista `pg_stat_replication` podía contener valores NULL en los campos `replay_lsn`, `flush_lsn` o `write_lsn` incluso cuando `state = 'streaming'`.

--------

## Versión 2.1.0 {#version-210}

Publicado el 2021-07-06

Esta versión añade compatibilidad con PostgreSQL v14, hace que los slots de replicación lógica sobrevivan a la conmutación por error/switchover, implementa el soporte de lista de permitidos (allowlist) para la REST API y también reduce el número de registros a una línea por latido.

**Nuevas funcionalidades**

- Compatibilidad con PostgreSQL v14 (Alexander Kukushkin)

  Reanuda la reproducción de WAL si Patroni no está en modo «pausa». Podría estar «en pausa» debido al cambio de ciertos parámetros como, por ejemplo, `max_connections` en el primario.

- Conmutación por error de slots lógicos (Alexander Kukushkin)

  Hace que los slots de replicación lógica sobrevivan a la conmutación por error/switchover en PostgreSQL v11+. El slot de replicación se copia del primario a la réplica con reinicio y más tarde se usa la función [pg_replication_slot_advance()](https://www.postgresql.org/docs/11/functions-admin.html#id-1.5.8.31.8.5.2.2.8.1.1) para avanzarlo. Como resultado, el slot ya existirá antes de la conmutación por error y no deberían perderse eventos, pero existe la posibilidad de que algunos eventos se entreguen más de una vez.

- Implementa la lista de permitidos (allowlist) para la REST API de Patroni (Alexander Kukushkin)

  Si está configurada, solo las IP que coincidan con las reglas podrán llamar a los endpoints no seguros. Además, es posible incluir automáticamente en la lista las IP de los miembros del clúster.

- Añade soporte de conexiones de replicación mediante socket unix (Mohamad El-Rifai)

  Anteriormente, Patroni usaba siempre TCP para la conexión de replicación, lo que podía causar algunos problemas con la verificación SSL. Usar sockets unix permite eximir al usuario de replicación de la verificación SSL.

- Comprobación de estado sobre etiquetas definidas por el usuario (Arman Jafari Tehrani)

  Junto con las [etiquetas predefinidas:](/es/patroni/config/yaml#tags_settings) es posible especificar cualquier número de etiquetas personalizadas que se vuelven visibles en la salida de `patronictl list` y en la REST API. A partir de ahora es posible usar etiquetas personalizadas en las comprobaciones de estado.

- Añade el endpoint `/metrics` de Prometheus (Mark Mercado, Michael Banck)

  El endpoint expone las mismas métricas que `/patroni`.

- Reduce la verbosidad de los registros de Patroni (Alexander Kukushkin)

  Cuando todo va bien, solo se escribirá una línea por cada ejecución del ciclo de HA.

**Cambios incompatibles**

- La antigua función de `permanent logical replication slots` ya no funcionará con PostgreSQL v10 y anteriores (Alexander Kukushkin)

  La estrategia de crear los slots lógicos después de realizar una promoción no puede garantizar que no se pierdan eventos lógicos y, por lo tanto, quedó deshabilitada.

- El endpoint `/leader` devuelve siempre 200 si el nodo retiene el bloqueo (Alexander Kukushkin)

  Promover el clúster en espera requiere actualizar las comprobaciones de estado del balanceador de carga, lo cual no es muy conveniente y es fácil de olvidar. Para resolverlo, cambiamos el comportamiento del endpoint de comprobación de estado `/leader`. Devolverá 200 sin tener en cuenta si el clúster es normal o el [standby_cluster](/es/patroni/standby_cluster#standby_cluster).

**Mejoras en el soporte de Raft**

- Soporte fiable del cifrado del tráfico de Raft (Alexander Kukushkin)

  Debido a los diferentes problemas en `PySyncObj`, el soporte del cifrado era muy inestable

- Maneja los problemas de DNS en la implementación de Raft (Alexander Kukushkin)

  Si `self_addr` y/o `partner_addrs` se configuran usando el nombre DNS en lugar de IP, `PySyncObj` en la práctica hacía la resolución solo una vez al crear el objeto. Esto causaba problemas cuando el mismo nodo volvía a estar en línea con una IP diferente.

**Mejoras de estabilidad**

- Compatibilidad con `psycopg2-2.9+` (Alexander Kukushkin)

  En `psycopg2`, el `autocommit = True` se ignora en el bloque `with connection`, lo que rompe las conexiones del protocolo de replicación.

- Corrige las ejecuciones excesivas del ciclo de HA con Zookeeper (Alexander Kukushkin)

  La actualización de los ZNodes de los miembros provocaba una reacción en cadena y daba como resultado la ejecución de los ciclos de HA varias veces seguidas.

- Recarga si el certificado de la REST API cambia en el disco (Michael Todorovic)

  Si el archivo del certificado de la REST API se actualizaba en el lugar, Patroni no realizaba una recarga.

- No crea el directorio de pgpass si se usa autenticación kerberos (Kostiantyn Nemchenko)

  Kerberos y la autenticación por contraseña son mutuamente excluyentes.

- Corrige pequeños problemas con el bootstrap personalizado (Alexander Kukushkin)

  Inicia Postgres con `hot_standby=off` solo cuando hacemos un PITR y lo reinicia después de que el PITR termine.

**Correcciones de errores**

- Compatibilidad con `kazoo-2.7+` (Alexander Kukushkin)

  Dado que Patroni maneja los reintentos por sí mismo, depende del comportamiento antiguo de `kazoo` en el que las solicitudes a un clúster de Zookeeper se descartan inmediatamente cuando no hay conexiones disponibles.

- Solicita explícitamente la versión del clúster de Etcd v3 cuando se sabe que nos conectamos mediante proxy (Alexander Kukushkin)

  Patroni trabaja con el clúster de Etcd v3 mediante gRPC-gateway y, dependiendo de la versión del clúster, deben usarse diferentes endpoints (`/v3`, `/v3beta` o `/v3alpha`). La versión se resolvía solo junto con la topología del clúster, pero esta última nunca se obtenía al conectarse mediante proxy.

--------

## Versión 2.0.2 {#version-202}

Publicado el 2021-02-22

**Nuevas funcionalidades**

- Capacidad de ignorar los slots de replicación gestionados externamente (James Coleman)

  Patroni intenta eliminar cualquier slot de replicación que no conoce, pero ciertamente hay casos en que los slots de replicación deben gestionarse externamente. A partir de ahora es posible configurar slots que no deben eliminarse.

- Añade soporte para la limitación de conjuntos de cifrado para la REST API (Gunnar "Nick" Bluth)

  Podía configurarse mediante `restapi.ciphers` o la variable de entorno `PATRONI_RESTAPI_CIPHERS`.

- Añade soporte para claves TLS cifradas para la REST API (Jonathan S. Katz)

  Podía configurarse mediante `restapi.keyfile_password` o la variable de entorno `PATRONI_RESTAPI_KEYFILE_PASSWORD`.

- Comparación en tiempo constante de las credenciales de autenticación de la REST API (Alex Brasetvik)

  Usa `hmac.compare_digest()` en lugar de `==`, que es vulnerable a ataques de temporización.

- Elige nodos síncronos en función del lag de replicación (Krishna Sarabu)

  Si el lag de replicación en el nodo síncrono comienza a exceder el umbral configurado, podría degradarse a asíncrono y/o ser reemplazado por el otro nodo. El comportamiento se controla con `maximum_lag_on_syncnode`.

**Mejoras de estabilidad**

- Inicia postgres con `hot_standby = off` al hacer un bootstrap personalizado (Igor Yanchenko)

  Durante un bootstrap personalizado, Patroni restaura el basebackup, inicia Postgres y espera a que termine la recuperación. Algunos parámetros de PostgreSQL en el standby no pueden ser menores que en el primario y, si el nuevo valor (restaurado del WAL) es mayor que el configurado, Postgres entra en pánico y se detiene. Para evitar tal comportamiento, haremos el bootstrap personalizado sin el modo `hot_standby`.

- Advierte al usuario si el watchdog requerido no está sano (Nicolas Thauvin)

  Cuando el dispositivo watchdog no es escribible o falta en el modo required, el miembro no puede ser promovido. Se añadió una advertencia para mostrar al usuario dónde buscar esta mala configuración.

- Mejor verbosidad para la recuperación en modo usuario único (Alexander Kukushkin)

  Si Patroni nota que PostgreSQL no se apagó limpiamente, en ciertos casos la recuperación ante fallos se ejecuta iniciando Postgres en modo usuario único. Podía ocurrir que la recuperación fallara (por ejemplo, por falta de espacio en disco) pero los errores se tragaban.

- Añade compatibilidad con el módulo `python-consul2` (Alexander Kukushkin, Wilfried Roset)

  El buen y viejo `python-consul` no recibe mantenimiento desde hace unos años; por lo tanto, alguien creó un fork con nuevas funciones y correcciones de errores.

- No usa `bypass_api_service` al ejecutar [patronictl](/es/patroni/patronictl#patronictl) (Alexander Kukushkin)

  Cuando un pod de K8s se ejecuta en un espacio de nombres que no es `default`, no necesariamente tiene permisos suficientes para consultar el endpoint de [kubernetes](/es/patroni/kubernetes#kubernetes). En ese caso, Patroni muestra la advertencia e ignora el ajuste `bypass_api_service`. En el caso de [patronictl](/es/patroni/patronictl#patronictl), la advertencia era un poco molesta.

- Crea `raft.data_dir` si no existe o garantiza que sea escribible (Mark Mercado)

  Mejora la facilidad de uso y la usabilidad.

**Correcciones de errores**

- No interrumpe el reinicio o la promoción si se pierde el bloqueo de líder en pausa (Alexander Kukushkin)

  En pausa está permitido ejecutar postgres como primario sin bloqueo.

- Corrige un problema con `shutdown_request()` en la REST API (Nicolas Limage)

  Para mejorar el manejo de las conexiones SSL y retrasar el handshake hasta que se inicie el hilo, Patroni sobrescribe algunos métodos en el `HTTPServer`. El método `shutdown_request()` fue olvidado.

- Corrige un problema con el tiempo de espera cuando se usa Zookeeper (Alexander Kukushkin)

  Había posibilidades de que Patroni durmiera hasta el doble de tiempo entre ejecuciones del código de HA.

- Corrige llamadas inválidas a `os.symlink()` al mover el directorio de datos tras un bootstrap fallido (Andrew L'Ecuyer)

  Si el bootstrap fallaba, Patroni renombra el directorio de datos, pg_wal y todos los tablespaces. Después actualiza los enlaces simbólicos para que el sistema de archivos permanezca consistente. La creación de los enlaces simbólicos fallaba porque los argumentos `src` y `dst` estaban intercambiados.

- Corrige un error en el método post_bootstrap() (Alexander Kukushkin)

  Si la contraseña de superusuario no estaba configurada, Patroni no lograba llamar al script `post_init` y, por lo tanto, todo el bootstrap fallaba.

- Corrige un problema con pg_rewind en el clúster en espera (Alexander Kukushkin)

  Si el nombre del superusuario es diferente de `postgres`, el `pg_rewind` en el clúster en espera fallaba porque la cadena de conexión no contenía el nombre de la base de datos.

- Termina solo si la autenticación con Etcd v3 falló explícitamente (Alexander Kukushkin)

  Al iniciar, Patroni realiza el descubrimiento de la topología del clúster de Etcd y se autentica si es necesario. Podía ocurrir que uno de los servidores de etcd no fuera accesible; Patroni intentaba autenticarse en ese servidor y fallaba, en lugar de reintentar con el siguiente nodo.

- Maneja el caso de que psutil cmdline() devuelva una lista vacía (Alexander Kukushkin)

  Los procesos zombis siguen siendo hijos del postmaster, pero no tienen cmdline()

- Trata la variable de entorno `PATRONI_KUBERNETES_USE_ENDPOINTS` como booleana (Alexander Kukushkin)

  No hacerlo hacía imposible deshabilitar `kubernetes.use_endpoints` mediante el entorno.

- Mejora el manejo de los errores de actualización concurrente de endpoints (Alexander Kukushkin)

  Patroni consultará explícitamente el objeto endpoint actual, verificará que el pod actual todavía retiene el bloqueo de líder y repetirá la actualización.

--------

## Versión 2.0.1 {#version-201}

Publicado el 2020-10-01

**Nuevas funcionalidades**

- Usa `more` como paginador en `patronictl edit-config` si `less` no está disponible (Pavel Golub)

  En Windows sería el `more.com`. Además, `cdiff` se cambió por `ydiff` en `requirements.txt`, pero [patronictl](/es/patroni/patronictl#patronictl) sigue soportando ambos por compatibilidad.

- Añade soporte de `bind_addr` y `password` de `raft` (Alexander Kukushkin)

  `raft.bind_addr` puede ser útil al ejecutarse detrás de un NAT. `raft.password` habilita el cifrado del tráfico (requiere el módulo `cryptography`).

- Añade soporte para el parámetro de conexión `sslpassword` (Kostiantyn Nemchenko)

  El parámetro de conexión se introdujo en PostgreSQL 13.

**Mejoras de estabilidad**

- Cambió el comportamiento en pausa (Alexander Kukushkin)

  1.  Patroni no llamará al método `bootstrap` si el directorio `PGDATA` falta/está vacío.
  2.  Patroni no terminará por una discrepancia de sysid en pausa, solo registrará una advertencia.
  3.  El nodo no intentará tomar la clave de líder en modo de pausa si Postgres se está ejecutando sin recuperación (aceptando escrituras) pero el sysid no coincide con la clave de inicialización.

- Aplica `master_start_timeout` al ejecutar la recuperación ante fallos (Alexander Kukushkin)

  Si Postgres falló en el nodo líder, Patroni hace una recuperación ante fallos iniciando Postgres en modo usuario único. Durante la recuperación ante fallos se actualiza el bloqueo de líder. Si la recuperación ante fallos no terminaba en `master_start_timeout` segundos, Patroni la detendrá forzosamente y liberará el bloqueo de líder.

- Elimina el extra `secure` de los requisitos de `urllib3` (Alexander Kukushkin)

  La única razón para añadirlo allí era la dependencia de `ipaddress` para python 2.7.

**Correcciones de errores**

- Corrige un error en `Kubernetes.update_leader()` (Alexander Kukushkin)

  Una excepción no manejada impedía degradar el primario cuando la actualización del objeto de líder fallaba.

- Corrige el colgado de [patronictl](/es/patroni/patronictl#patronictl) cuando se usa RAFT (Alexander Kukushkin)

  Al usar [patronictl](/es/patroni/patronictl#patronictl) con la configuración de Patroni, `self_addr` debería añadirse a los `partner_addrs`.

- Corrige un error en `get_guc_value()` (Alexander Kukushkin)

  Patroni no lograba obtener el valor de `restore_command` en PostgreSQL 12; por lo tanto, la obtención de los WAL faltantes para `pg_rewind` no funcionaba.

--------

## Versión 2.0.0 {#version-200}

Publicado el 2020-09-02

Esta versión mejora la compatibilidad con PostgreSQL 13, añade el soporte de múltiples standbys síncronos, tiene mejoras significativas en el manejo de `pg_rewind`, añade el soporte de Etcd v3 y de Patroni sobre RAFT puro (sin Etcd, Consul ni Zookeeper), y hace posible llamar opcionalmente al script `pre_promote` (aislamiento/fencing).

**Soporte de PostgreSQL 13**

- No dispara `on_reload` al promover a `standby_leader` en PostgreSQL 13+ (Alexander Kukushkin)

  Al promover a `standby_leader` cambiamos `primary_conninfo`, actualizamos el rol y recargamos Postgres. Dado que `on_role_change` y `on_reload` efectivamente se duplican entre sí, Patroni llamará solo a `on_role_change`.

- Añade soporte para los parámetros de conexión `gssencmode` y `channel_binding` (Alexander Kukushkin)

  PostgreSQL 12 introdujo el parámetro de conexión `gssencmode` y 13 el `channel_binding`, y ahora pueden usarse si están definidos en la sección `postgresql.authentication`.

- Maneja el cambio de nombre de `wal_keep_segments` a `wal_keep_size` (Alexander Kukushkin)

  En caso de mala configuración (`wal_keep_segments` en 13 y `wal_keep_size` en versiones anteriores), Patroni ajustará automáticamente la configuración.

- Usa `pg_rewind` con `--restore-target-wal` en 13 si es posible (Alexander Kukushkin)

  En PostgreSQL 13, Patroni comprueba si `restore_command` está configurado y le indica a `pg_rewind` que lo use.

**Nuevas funcionalidades**

- \[BETA\] Implementa el soporte de Patroni sobre RAFT puro (Alexander Kukushkin)

  Esto hace posible ejecutar Patroni sin dependencias de terceros, como Etcd, Consul o Zookeeper. Para HA tendrás que ejecutar tres nodos de Patroni o dos nodos con Patroni y un nodo con `patroni_raft_controller`. Para más información, consulta la [documentación](/es/patroni/config/yaml#raft_settings).

- \[BETA\] Implementa el soporte del protocolo de Etcd v3 mediante gRPC-gateway (Alexander Kukushkin)

  Etcd 3.0 se publicó hace más de cuatro años y Etcd 3.4 tiene v2 deshabilitado por defecto. También hay posibilidades de que v2 se elimine por completo de Etcd; por lo tanto, implementamos el soporte de Etcd v3 en Patroni. Para empezar a usarlo tienes que crear explícitamente la sección `etcd3` en el archivo de configuración de Patroni.

- Soporta múltiples standbys síncronos (Krishna Sarabu)

  Permite ejecutar un clúster con más de una réplica síncrona. El número máximo de réplicas síncronas se controla con el nuevo parámetro `synchronous_node_count`. Está establecido en 1 por defecto y no tiene efecto cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está establecido en `off`.

- Añade la posibilidad de llamar al script `pre_promote` (Sergey Dudoladov)

  A diferencia de los callbacks, el script `pre_promote` se llama de forma síncrona después de adquirir el bloqueo de líder, pero antes de promover Postgres. Si el script falla o termina con un código de salida distinto de cero, el nodo actual liberará el bloqueo de líder.

- Añade soporte para directorios de configuración (Floris van Nee)

  Los archivos YAML del directorio se cargan y aplican en orden alfabético.

- Validación avanzada de los parámetros de PostgreSQL (Alexander Kukushkin)

  En caso de que el parámetro específico no esté soportado por la versión actual de PostgreSQL o cuando su valor sea incorrecto, Patroni eliminará el parámetro por completo o intentará corregir el valor.

- Despierta el hilo principal cuando el checkpoint forzado después de la promoción se completa (Alexander Kukushkin)

  Las réplicas esperan la indicación del checkpoint mediante la clave del miembro del líder en el DCS. La clave normalmente se actualiza solo una vez por ciclo de HA. Sin despertar el hilo principal, las réplicas tendrán que esperar hasta `loop_wait` segundos más de lo necesario.

- Uso de la vista `pg_stat_wal_receiver` en 9.6+ (Alexander Kukushkin)

  La vista contiene valores actualizados de `primary_conninfo` y `primary_slot_name`, mientras que el contenido de `recovery.conf` podría estar obsoleto.

- Mejora el manejo de las direcciones IPv6 en el archivo de configuración de Patroni (Mateusz Kowalski)

  Se supone que la dirección IPv6 va entre corchetes, pero Patroni esperaba recibirla sin adornos. Ahora se soportan ambos formatos.

- Añade el parámetro de configuración `service_tags` de Consul (Robert Edström)

  Son útiles para el descubrimiento dinámico de servicios, por ejemplo por parte de balanceadores de carga.

- Implementa el soporte SSL para Zookeeper (Kostiantyn Nemchenko)

  Requiere `kazoo>=2.6.0`.

- Implementa la opción `no_params` para el método de bootstrap personalizado (Kostiantyn Nemchenko)

  Permite llamar a `wal-g`, `pgBackRest` y otras herramientas de copia de seguridad sin envolverlas en scripts de shell.

- Mueve el WAL y los tablespaces después de una inicialización fallida (Feike Steenbergen)

  Al hacer `reinit`, Patroni ya eliminaba no solo `PGDATA` sino también el directorio de WAL enlazado simbólicamente y los tablespaces. Ahora el método `move_data_directory()` hará un trabajo similar, es decir, renombrar el directorio de WAL y los tablespaces y actualizar los enlaces simbólicos en PGDATA.

**Mejoras en el soporte de pg_rewind**

- Mejora la comprobación de divergencia de líneas de tiempo (Alexander Kukushkin)

  No necesitamos hacer rewind cuando la posición reproducida en la réplica no está por delante del punto de conmutación (switchpoint) o cuando el final del registro de checkpoint en el antiguo primario es el mismo que el punto de conmutación. Para obtener el final del registro de checkpoint usamos `pg_waldump` y analizamos su salida.

- Intenta obtener los WAL faltantes si `pg_rewind` se queja de ello (Alexander Kukushkin)

  Podía ocurrir que el segmento de WAL requerido por `pg_rewind` ya no exista en el directorio `pg_wal` y que, por lo tanto, `pg_rewind` no pueda encontrar la ubicación del checkpoint antes del punto de divergencia. A partir de PostgreSQL 13, `pg_rewind` puede usar `restore_command` para obtener los WAL faltantes. Para versiones anteriores de PostgreSQL, Patroni analiza los errores de un intento fallido de rewind e intenta obtener el WAL faltante llamando al `restore_command` por su cuenta.

- Detecta una nueva línea de tiempo en el clúster en espera y activa el rewind/reinicialización si es necesario (Alexander Kukushkin)

  El [standby_cluster](/es/patroni/standby_cluster#standby_cluster) está desacoplado del clúster primario y, por lo tanto, no conoce de inmediato las elecciones de líder y los cambios de línea de tiempo. Para detectar el hecho, el `standby_leader` comprueba periódicamente si hay nuevos archivos de historial en `pg_wal`.

- Acorta y embellece la salida del registro de historial (Alexander Kukushkin)

  Cuando Patroni intenta determinar la necesidad de `pg_rewind`, podía escribir en el registro el contenido del archivo de historial del primario. El archivo de historial crece con cada conmutación por error/switchover y eventualmente empieza a ocupar demasiadas líneas, la mayoría de las cuales no son tan útiles. En lugar de mostrar los datos en bruto, Patroni mostrará solo 3 líneas antes de la línea de tiempo actual de la réplica y 2 líneas después.

**Mejoras en K8s**

- Se deshace del módulo de python [kubernetes](/es/patroni/kubernetes#kubernetes) (Alexander Kukushkin)

  El cliente oficial de kubernetes para python contiene mucho código autogenerado y, por lo tanto, es muy pesado. Patroni usa solo una pequeña fracción de los endpoints de la API de K8s e implementar el soporte para ellos no fue difícil.

- Hace posible omitir el servicio de [kubernetes](/es/patroni/kubernetes#kubernetes) (Alexander Kukushkin)

  Al ejecutarse en K8s, Patroni normalmente se comunica con la API de K8s mediante el servicio de [kubernetes](/es/patroni/kubernetes#kubernetes), cuya dirección se expone en la variable de entorno `KUBERNETES_SERVICE_HOST`. Como cualquier otro servicio, el servicio de [kubernetes](/es/patroni/kubernetes#kubernetes) lo maneja `kube-proxy`, que a su vez, dependiendo de la configuración, depende de un programa en espacio de usuario o de `iptables` para el enrutamiento del tráfico. Omitir el componente intermedio y conectarse directamente a los nodos master de K8s nos permite implementar una mejor estrategia de reintentos y mitigar los riesgos de degradar Postgres cuando los nodos master de K8s se actualizan.

- Sincroniza los ciclos de HA de todos los pods de un clúster de Patroni (Alexander Kukushkin)

  No hacerlo aumentaba el tiempo de detección de fallos de `ttl` a `ttl + loop_wait`.

- Rellena `references` y `nodename` en las direcciones de los subsets en K8s (Alexander Kukushkin)

  Algunos balanceadores de carga dependen de esta información.

- Corrige posibles condiciones de carrera en `update_leader()` (Alexander Kukushkin)

  La actualización concurrente del configmap o endpoint del líder que ocurre fuera de Patroni podría provocar que la llamada `update_leader()` falle. En ese caso, Patroni vuelve a comprobar que el nodo actual aún posea el bloqueo de líder y repite la actualización.

- No permite explícitamente aplicar patch a una configuración inexistente (Alexander Kukushkin)

  Para DCS distintos de [kubernetes](/es/patroni/kubernetes#kubernetes), la llamada PATCH falla con una excepción debido a que `cluster.config` es `None`, pero en Kubernetes estaba creando alegremente la anotación de configuración e impidiendo escribir la configuración de bootstrap después de que terminara el bootstrap.

- Corrige un error en la [pausa](/es/patroni/pause#pause) (Alexander Kukushkin)

  Las réplicas eliminaban `primary_conninfo` y reiniciaban Postgres cuando la clave de líder estaba ausente, pero no deberían hacer nada.

**Mejoras en la REST API**

- Aplaza el handshake TLS hasta que se haya iniciado el hilo de trabajo (Alexander Kukushkin, Ben Harris)

  Si el handshake TLS se hacía en el hilo de la API y el lado cliente no enviaba ningún dato, el hilo de la API quedaba bloqueado (con riesgo de DoS).

- Comprueba el `basic-auth` de forma independiente del certificado de cliente en la REST API (Alexander Kukushkin)

  Anteriormente solo se validaba el certificado de cliente. Hacer dos comprobaciones de forma independiente es un caso de uso absolutamente válido.

- Escribe un doble `CRLF` después de los encabezados HTTP de la solicitud `OPTIONS` (Sergey Burladyan)

  HAProxy estaba conforme con un solo `CRLF`, mientras que la comprobación de estado de Consul se quejaba de conexión rota y EOF inesperado.

- El `GET /cluster` mostraba información obsoleta de los miembros con Zookeeper (Alexander Kukushkin)

  El endpoint usaba la vista interna del clúster de Patroni. Para el propio Patroni no causaba ningún problema, pero cuando se expone al mundo exterior necesitamos mostrar información actualizada, especialmente el lag de replicación.

- Corrige las comprobaciones de estado para el clúster en espera (Alexander Kukushkin)

  El `GET /standby-leader` para un primario y el `GET /master` para un `standby_leader` respondían incorrectamente con 200.

- Implementa `DELETE /switchover` (Alexander Kukushkin)

  La llamada a la REST API elimina el switchover programado.

- Crea los endpoints `/readiness` y `/liveness` (Alexander Kukushkin)

  Podrían ser útiles para eliminar los pods «no sanos» de las direcciones de los subsets cuando el servicio de K8s se usa con selectores de etiquetas.

- Mejora las comprobaciones de estado `GET /replica` y `GET /async` de la REST API (Krishna Sarabu, Alexander Kukushkin)

  Las comprobaciones ahora soportan la palabra clave opcional `?lag=<max-lag>` y responderán con 200 solo si el lag es menor que el valor suministrado. Si dependes de esta función, ten en cuenta que la información sobre la posición del WAL en el líder se actualiza solo cada `loop_wait` segundos.

- Añade soporte para encabezados HTTP definidos por el usuario en la respuesta de la REST API (Yogesh Sharma)

  Esta función podría ser útil si las solicitudes se hacen desde un navegador.

**Mejoras en patronictl**

- No intenta llamar a un líder inexistente en `patronictl pause` (Alexander Kukushkin)

  Al pausar un clúster sin líder en K8s, [patronictl](/es/patroni/patronictl#patronictl) mostraba advertencias de que no se podía acceder al miembro "None".

- Maneja el caso en que falta el `conn_url` del miembro (Alexander Kukushkin)

  En K8s es posible que el pod no tenga las anotaciones necesarias porque Patroni aún no se está ejecutando. Esto hacía fallar a [patronictl](/es/patroni/patronictl#patronictl).

- Añade la capacidad de imprimir la topología del clúster en ASCII (Maxim Fedotov, Alexander Kukushkin)

  Es muy útil para obtener una visión general del clúster con replicación en cascada.

- Implementa `patronictl flush switchover` (Alexander Kukushkin)

  Antes de esto, `patronictl flush` solo soportaba la cancelación de reinicios programados.

**Correcciones de errores**

- Error de atributo durante el bootstrap del clúster con un PGDATA existente (Krishna Sarabu)

  Al intentar crear/actualizar la clave `/history`, Patroni accedía al objeto `ClusterConfig` que aún no se había creado en el DCS.

- Mejora el manejo de excepciones en Consul (Alexander Kukushkin)

  Una excepción no manejada en el método `touch_member()` provocaba el fallo de todo el proceso de Patroni.

- Aplica `synchronous_commit=local` para el script `post_init` (Alexander Kukushkin)

  Patroni ya lo hacía al crear usuarios (`replication`, `rewind`), pero pasarlo por alto en el caso de `post_init` fue un descuido. Como resultado, si el script no lo hacía internamente por sí mismo, el bootstrap en [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) no podía terminar.

- Aumenta el `maxsize` en el gestor de pool de Consul (ponvenkates)

  Con el `size=1` predeterminado se generaban algunas advertencias.

- Patroni reportaba erróneamente que Postgres se estaba ejecutando (Alexander Kukushkin)

  El estado no se actualizaba cuando, por ejemplo, Postgres fallaba debido a un error de falta de espacio en disco.

- Pone `*` en `pgpass` en lugar de valores faltantes o vacíos (Alexander Kukushkin)

  Si, por ejemplo, el `standby_cluster.port` no se especifica, el archivo `pgpass` se generaba incorrectamente.

- Omite la creación de slots de replicación físicos en el nodo líder con caracteres especiales (Krishna Sarabu)

  Parecía que Patroni estaba creando un slot inactivo (cuando `slots` está definido) para el nodo líder cuando el nombre contenía caracteres especiales como '-' (por ejemplo, "abc-us-1").

- Evita eliminar un `pg_hba.conf` inexistente en el bootstrap personalizado (Krishna Sarabu)

  Patroni fallaba si `pg_hba.conf` resultaba estar ubicado fuera del directorio `pgdata` después del bootstrap personalizado.

--------

## Versión 1.6.5 {#version-165}

Publicado el 2020-08-23

**Nuevas funcionalidades**

- Tiempo de espera de detención del master (Krishna Sarabu)

  El número de segundos que Patroni puede esperar al detener Postgres. Efectivo solo cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está habilitado. Cuando se establece en un valor mayor que 0 y [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está habilitado, Patroni envía `SIGKILL` al postmaster si la operación de detención se está ejecutando durante más del valor establecido por `master_stop_timeout`. Establece el valor según tu equilibrio entre durabilidad/disponibilidad. Si el parámetro no está establecido o está establecido en un valor no positivo, `master_stop_timeout` no tiene efecto.

- No crea un slot físico permanente con el nombre del primario (Alexander Kukushkin)

  Es un problema común que el primario recicle segmentos de WAL mientras la réplica está caída. Ahora tenemos una buena solución para clústeres estáticos, con un número fijo de nodos y nombres que nunca cambian. Solo necesitas listar los nombres de todos los nodos en `slots` para que el primario no elimine el slot cuando el nodo está caído (no registrado en el DCS).

- Primer borrador del validador de configuración (Igor Yanchenko)

  Usa `patroni --validate-config patroni.yaml` para validar la configuración de Patroni.

- Posibilidad de configurar la longitud máxima del historial de líneas de tiempo (Krishna Sarabu)

  Patroni escribe el historial de conmutaciones por error/switchovers en la clave `/history` del DCS. Con el tiempo el tamaño de esta clave se vuelve grande, pero en la mayoría de los casos solo las últimas líneas son interesantes. El parámetro `max_timelines_history` permite especificar el número máximo de elementos del historial de líneas de tiempo que se conservan en el DCS.

- Compatibilidad con Kazoo 2.7.0 (Danyal Prout)

  Algunos métodos no públicos de Kazoo cambiaron sus firmas, pero Patroni dependía de ellos.

**Mejoras en patronictl**

- Muestra las etiquetas de los miembros (Kostiantyn Nemchenko, Alexander Kukushkin)

  Las etiquetas se configuran individualmente para cada nodo y no había una forma sencilla de obtener una visión general de ellas

- Mejora la salida de los miembros (Alexander Kukushkin)

  El nombre redundante del clúster ya no se mostrará en cada línea, solo en el encabezado de la tabla.

``` bash
$ patronictl list
+ Cluster: batman (6813309862653668387) +---------+----+-----------+---------------------+
|    Member   |      Host      |  Role  |  State  | TL | Lag in MB | Tags                |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql0 | 127.0.0.1:5432 | Leader | running |  3 |           | clonefrom: true     |
|             |                |        |         |    |           | noloadbalance: true |
|             |                |        |         |    |           | nosync: true        |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql1 | 127.0.0.1:5433 |        | running |  3 |       0.0 |                     |
+-------------+----------------+--------+---------+----+-----------+---------------------+
```

- Falla si se especifica explícitamente un archivo de configuración pero no se encuentra (Kaarel Moppel)

  Anteriormente, [patronictl](/es/patroni/patronictl#patronictl) solo reportaba un mensaje `DEBUG`.

- Resuelve el problema de que un pod de K8s no inicializado rompiera patronictl (Alexander Kukushkin)

  Patroni depende de ciertas anotaciones del pod en K8s. Cuando uno de los pods de Patroni se está deteniendo o iniciando, todavía no hay una anotación válida y [patronictl](/es/patroni/patronictl#patronictl) fallaba con una excepción.

**Mejoras de estabilidad**

- Aplica una espera de 1 segundo si la llamada LIST al servidor de la API de K8s falla (Alexander Kukushkin)

  Es mayormente necesario para evitar saturar los registros, pero también ayuda a prevenir la inanición del hilo principal.

- Reintenta si la API de K8s devuelve el encabezado HTTP `retry-after` (Alexander Kukushkin)

  Si el servidor de la API de K8s está desbordado de solicitudes, podría pedir que se reintente.

- Limpia el entorno `KUBERNETES_` del postmaster (Feike Steenbergen)

  Las variables de entorno `KUBERNETES_` no son necesarias para PostgreSQL; sin embargo, tenerlas expuestas al postmaster también las expondrá a los backends y a los usuarios normales de la base de datos (usando pl/perl, por ejemplo).

- Limpia los tablespaces al reinicializar (Krishna Sarabu)

  Durante el reinit, Patroni eliminaba solo `PGDATA` y dejaba los directorios de tablespaces definidos por el usuario. Esto hace que Patroni entre en un bucle de reinit. La solución anterior para el problema era implementar el script de [bootstrap personalizado](/es/patroni/replica_bootstrap#custom_bootstrap).

- Ejecuta explícitamente `CHECKPOINT` después de que ocurre la promoción (Alexander Kukushkin)

  Ayuda a reducir el tiempo antes de que el nuevo primario sea utilizable para `pg_rewind`.

- Refresco inteligente de los miembros de Etcd (Alexander Kukushkin)

  En caso de que Patroni fallara en ejecutar una solicitud en todos los miembros del clúster de Etcd, Patroni volverá a comprobar los registros `A` o `SRV` por si cambiaron las IP/hosts antes de reintentar la próxima vez.

- Omite los valores faltantes de `pg_controldata` (Feike Steenbergen)

  Faltan valores al intentar usar binarios de una versión que no coincide con PGDATA. Patroni intentará iniciar Postgres de todos modos, y Postgres se quejará de que la versión principal no coincide y abortará con un error.

**Correcciones de errores**

- Deshabilita la verificación SSL para Consul cuando se requiere (Julien Riou)

  A partir de cierta versión de `urllib3`, `cert_reqs` debe establecerse explícitamente en `ssl.CERT_NONE` para deshabilitar efectivamente la verificación SSL.

- Evita abrir la conexión de replicación en cada ciclo del bucle de HA (Alexander Kukushkin)

  La regresión se introdujo en 1.6.4.

- Llama al callback `on_role_change` en un primario fallido (Alexander Kukushkin)

  En ciertos casos podía llevar a que la IP virtual permaneciera adjunta al antiguo primario. La regresión se introdujo en 1.4.5.

- Restablece el estado de rewind si postgres se inició después de un pg_rewind exitoso (Alexander Kukushkin)

  Como resultado de este error, Patroni iniciaba un postgres apagado manualmente en el modo de pausa.

- Convierte `recovery_min_apply_delay` a `ms` al comprobar `recovery.conf`

  Patroni reiniciaba indefinidamente la réplica si `recovery_min_apply_delay` estaba configurado en PostgreSQL anterior a 12.

- Compatibilidad con PyInstaller (Alexander Kukushkin)

  PyInstaller congela (empaqueta) aplicaciones de Python en ejecutables independientes. La compatibilidad se rompió cuando cambiamos al método `spawn` en lugar de `fork` para `multiprocessing`.

--------

## Versión 1.6.4 {#version-164}

Publicado el 2020-01-27

**Nuevas funcionalidades**

- Implementa la opción `--wait` para `patronictl reinit` (Igor Yanchenko)

  patronictl esperará a que `reinit` termine si se usa la opción `--wait`.

- Mejoras adicionales del soporte de Windows (Igor Yanchenko, Alexander Kukushkin)

  1.  Todos los scripts de shell que se usan para las pruebas de integración están reescritos en python
  2.  Se usará `pg_ctl kill` para detener postgres en sistemas no posix
  3.  No intenta usar sockets de dominio unix

**Mejoras de estabilidad**

- Garantiza que `unix_socket_directories` y `stats_temp_directory` existan (Igor Yanchenko)

  Al inicio de Patroni y Postgres, garantiza que `unix_socket_directories` y `stats_temp_directory` existan o intenta crearlos. Patroni terminará si falla al crearlos.

- Garantiza que `postgresql.pgpass` esté ubicado en un lugar donde Patroni tenga acceso de escritura (Igor Yanchenko)

  En caso de no tener acceso de escritura, Patroni terminará con una excepción.

- Deshabilita la comprobación `serfHealth` de Consul por defecto (Kostiantyn Nemchenko)

  Incluso en caso de pequeños problemas de red, el fallo de `serfHealth` provoca la invalidación de todas las sesiones asociadas con el nodo. Por lo tanto, la clave de líder se pierde mucho antes que `ttl`, lo que causa reinicios no deseados de las réplicas y quizás la degradación del primario.

- Configura los keepalives TCP para las conexiones a la API de K8s (Alexander Kukushkin)

  En caso de no recibir nada del socket después de TTL segundos, puede considerarse muerto.

- Evita el registro de contraseñas al crear usuarios (Alexander Kukushkin)

  Si la contraseña es rechazada o el registro está configurado como detallado o no está configurado en absoluto, podría ocurrir que la contraseña se escriba en los registros de postgres. Para evitarlo, Patroni cambiará `log_statement`, `log_min_duration_statement` y `log_min_error_statement` a algunos valores seguros antes de intentar crear/actualizar el usuario.

**Correcciones de errores**

- Usa el `restore_command` de la configuración de [standby_cluster](/es/patroni/standby_cluster#standby_cluster) en las réplicas en cascada (Alexander Kukushkin)

  El `standby_leader` ya lo hacía desde el principio en que existió la función. No hacer lo mismo en las réplicas podría impedir que se pongan al día con el líder en espera.

- Actualiza la línea de tiempo reportada por el clúster en espera (Alexander Kukushkin)

  En caso de cambio de línea de tiempo, el clúster en espera replicaba correctamente desde el primario, pero [patronictl](/es/patroni/patronictl#patronictl) reportaba la línea de tiempo antigua.

- Permite que ciertos parámetros de recuperación se definan en el custom_conf (Alexander Kukushkin)

  Al hacer la validación de los parámetros de recuperación en la réplica, Patroni omitirá `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command`, `recovery_min_apply_delay` y `restore_command` si no están definidos en la configuración de patroni sino en archivos distintos de `postgresql.auto.conf` o `postgresql.conf`.

- Mejora el manejo de los parámetros de postgresql con un punto en su nombre (Alexander Kukushkin)

  Dichos parámetros podrían estar definidos por extensiones donde la unidad no es necesariamente una cadena. Cambiar el valor podría requerir un reinicio (por ejemplo, `pg_stat_statements.max`).

- Mejora el manejo de excepciones durante el apagado (Alexander Kukushkin)

  Durante el apagado, Patroni intenta actualizar su estado en el DCS. Si el DCS es inaccesible, podría generarse una excepción. La falta de manejo de excepciones impedía que el hilo del logger se detuviera.

--------

## Versión 1.6.3 {#version-163}

Publicado el 2019-12-05

**Correcciones de errores**

- No expone la contraseña al ejecutar `pg_rewind` (Alexander Kukushkin)

  El error se introdujo en el [\#1301](https://github.com/patroni/patroni/pull/1301)

- Aplica los parámetros de conexión especificados en `postgresql.authentication` a `pg_basebackup` y a los métodos personalizados de creación de réplicas (Alexander Kukushkin)

  Estos dependían de una cadena de conexión tipo URL y, por lo tanto, los parámetros nunca se aplicaban.

--------

## Versión 1.6.2 {#version-162}

Publicado el 2019-12-05

**Nuevas funcionalidades**

- Implementa `patroni --version` (Igor Yanchenko)

  Imprime la versión actual de Patroni y termina.

- Establece el encabezado http `user-agent` para todas las solicitudes http (Alexander Kukushkin)

  Patroni se comunica con Consul, Etcd y la API de Kubernetes mediante el protocolo http. Tener un `user-agent` específicamente elaborado (ejemplo: `Patroni/1.6.2 Python/3.6.8 Linux`) puede ser útil para la depuración y el monitoreo.

- Hace posible configurar el nivel de registro para los tracebacks de excepciones (Igor Yanchenko)

  Si estableces `log.traceback_level=DEBUG`, los tracebacks serán visibles solo cuando `log.level=DEBUG`. El comportamiento predeterminado sigue siendo el mismo.

**Mejoras de estabilidad**

- Evita importar todos los módulos de DCS al buscar el módulo requerido por el archivo de configuración (Alexander Kukushkin)

  No hay necesidad de importar los módulos de Etcd, Consul y Kubernetes si solo necesitamos, por ejemplo, Zookeeper. Ayuda a reducir el uso de memoria y resuelve el problema de tener mensajes INFO `Failed to import smth`.

- Elimina el módulo `requests` de python de los requisitos explícitos (Alexander Kukushkin)

  No se usaba para nada crítico, pero causaba muchos problemas cuando se publicaba la nueva versión de `urllib3`.

- Mejora el manejo de `etcd.hosts` escrito como una cadena separada por comas en lugar de un array YAML (Igor Yanchenko)

  Anteriormente fallaba cuando se escribía en el formato `host1:port1, host2:port2` (el carácter de espacio después de la coma).

**Mejoras de usabilidad**

- No obliga a los usuarios a elegir miembros de una lista vacía en [patronictl](/es/patroni/patronictl#patronictl) (Igor Yanchenko)

  Si el usuario proporciona un nombre de clúster incorrecto, generaremos una excepción en lugar de pedir que elija un miembro de una lista vacía.

- Hace el mensaje de error más útil si la REST API no puede enlazarse (Igor Yanchenko)

  Para un usuario sin experiencia podría ser difícil averiguar qué está mal a partir del stacktrace de Python.

**Correcciones de errores**

- Corrige el cálculo de `wal_buffers` (Alexander Kukushkin)

  La unidad base se cambió de bloques de 8 kB a bytes en PostgreSQL 11.

- Usa `passfile` en `primary_conninfo` solo en PostgreSQL 10+ (Alexander Kukushkin)

  En versiones anteriores no hay garantía de que `passfile` funcione, a menos que esté instalada la última versión de `libpq`.

--------

## Versión 1.6.1 {#version-161}

Publicado el 2019-11-15

**Nuevas funcionalidades**

- Añade la variable de entorno `PATRONICTL_CONFIG_FILE` (msvechla)

  Permite configurar el argumento `--config-file` de [patronictl](/es/patroni/patronictl#patronictl) desde el entorno.

- Implementa `patronictl history` (Alexander Kukushkin)

  Muestra el historial de conmutaciones por error/switchovers.

- Pasa `-c statement_timeout=0` en `PGOPTIONS` al hacer `pg_rewind` (Alexander Kukushkin)

  Protege del caso en que `statement_timeout` en el servidor esté establecido en algún valor pequeño y una de las sentencias ejecutadas por pg_rewind sea cancelada.

- Permite valores más bajos para la configuración de PostgreSQL (Soulou)

  Patroni no permitía que algunos de los parámetros de configuración de PostgreSQL se establecieran por debajo de ciertos valores fijados en el código. Ahora los valores mínimos permitidos son más pequeños; los valores predeterminados no se han cambiado.

- Permite la autenticación basada en certificados (Jonathan S. Katz)

  Esta función habilita la autenticación basada en certificados para las cuentas de superusuario, replicación y rewind, y permite al usuario especificar el `sslmode` con el que desea conectarse.

- Usa el `passfile` en el `primary_conninfo` en lugar de la contraseña (Alexander Kukushkin)

  Permite evitar establecer permisos `600` en postgresql.conf

- Realiza `pg_ctl reload` independientemente de los cambios de configuración (Alexander Kukushkin)

  Es posible que algunos archivos de configuración no estén controlados por Patroni. Cuando alguien hace una recarga mediante la REST API o enviando SIGHUP al proceso de Patroni, lo habitual es esperar que Postgres también se recargue. Anteriormente esto no ocurría cuando no había cambios en la sección `postgresql` de la configuración de Patroni.

- Compara todos los parámetros de recuperación, no solo el `primary_conninfo` (Alexander Kukushkin)

  Anteriormente, el método `check_recovery_conf()` solo comprobaba si `primary_conninfo` había cambiado, sin tener nunca en cuenta todos los demás parámetros de recuperación.

- Hace posible aplicar algunos parámetros de recuperación sin reinicio (Alexander Kukushkin)

  A partir de PostgreSQL 12 los siguientes parámetros de recuperación pueden cambiarse sin reinicio: `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command` y `recovery_min_apply_delay`. En futuras versiones de Postgres esta lista se ampliará y Patroni lo soportará automáticamente.

- Hace posible cambiar `use_slots` en caliente (Alexander Kukushkin)

  Anteriormente requería reiniciar Patroni y eliminar los slots manualmente.

- Elimina solo las variables de entorno con prefijo `PATRONI_` al iniciar Postgres (Cody Coons)

  Resolverá muchos problemas al ejecutar diferentes Foreign Data Wrappers.

**Mejoras de estabilidad**

- Usa LIST + WATCH al trabajar con la API de K8s (Alexander Kukushkin)

  Permite recibir eficientemente los cambios de los objetos (pods, endpoints/configmaps) y ejerce menos estrés en los nodos master de K8s.

- Mejora el flujo de trabajo cuando PGDATA no está vacío durante el bootstrap (Alexander Kukushkin)

  Según el código fuente de `initdb`, podría considerar un PGDATA vacío cuando solo hay `lost+found` y `.dotfiles` en él. Ahora Patroni hace lo mismo. Si `PGDATA` resulta ser no vacío y, al mismo tiempo, no válido desde el punto de vista de `pg_controldata`, Patroni se quejará y terminará.

- Evita llamar al costoso `os.listdir()` en cada ciclo de HA (Alexander Kukushkin)

  Cuando el sistema está bajo estrés de E/S, `os.listdir()` podía tardar unos segundos (o incluso minutos) en ejecutarse, afectando gravemente el ciclo de HA de Patroni. Esto podía incluso provocar que la clave de líder desapareciera del DCS por falta de actualizaciones. Hay una forma mejor y menos costosa de comprobar que el PGDATA no está vacío. Ahora comprobamos la presencia del archivo `global/pg_control` en el PGDATA.

- Algunas mejoras en la infraestructura de registro (Alexander Kukushkin)

  Anteriormente existía la posibilidad de perder las últimas líneas de registro al apagarse porque el hilo de registro era un hilo `daemon`.

- Usa el método de inicio `spawn` de multiprocessing en python 3.4+ (Maciej Kowalczyk)

  Es un [problema](https://bugs.python.org/issue6721) conocido de Python que threading y multiprocessing no se lleven bien. Cambiar del método predeterminado `fork` a `spawn` es una solución recomendada. No hacerlo podía dar como resultado que el proceso de inicio del Postmaster se colgara y que Patroni reportara indefinidamente `INFO: restarting after failure in progress`, mientras Postgres en realidad estaba activo y funcionando.

**Mejoras en la REST API**

- Hace posible comprobar certificados de cliente en la REST API (Alexander Kukushkin)

  Si `verify_client` está establecido en `required`, Patroni comprobará los certificados de cliente para todas las llamadas a la REST API. Cuando está establecido en `optional`, los certificados de cliente se comprueban para todos los endpoints no seguros de la REST API.

- Devuelve el código de respuesta 503 para la solicitud de comprobación de estado `GET /replica` si Postgres no se está ejecutando (Alexander Anikin)

  Postgres podría pasar un tiempo significativo en recuperación antes de comenzar a aceptar conexiones de cliente.

- Implementa los endpoints `/history` y `/cluster` (Alexander Kukushkin)

  El endpoint `/history` muestra el contenido de la clave `history` del DCS. El endpoint `/cluster` muestra todos los miembros del clúster y cierta información de servicio como reinicios o switchovers pendientes y programados.

**Mejoras en el soporte de Etcd**

- Reintenta ante un error interno de RAFT de Etcd (Alexander Kukushkin)

  Cuando el nodo de Etcd se está apagando, envía `response code=300, data='etcdserver: server stopped'`, lo que provocaba que Patroni degradara el primario.

- No se rinde demasiado pronto con el reintento de solicitudes a Etcd (Alexander Kukushkin)

  Cuando había algunos problemas de red, Patroni agotaba rápidamente la lista de nodos de Etcd y se rendía sin usar todo el `retry_timeout`, lo que potencialmente daba como resultado la degradación del primario.

**Correcciones de errores**

- Deshabilita `synchronous_commit` al otorgar permisos de ejecución al usuario de `pg_rewind` (kremius)

  Si el bootstrap se hace con `synchronous_mode_strict: true`, la sentencia `GRANT EXECUTE` esperaba indefinidamente porque no había nodos standby síncronos disponibles.

- Corrige una fuga de memoria en python 3.7 (Alexander Kukushkin)

  Patroni usa `ThreadingMixIn` para procesar las solicitudes de la REST API y python 3.7 hizo que los hilos generados para cada solicitud no sean demonio por defecto.

- Corrige condiciones de carrera en acciones asíncronas (Alexander Kukushkin)

  Había una posibilidad de que `patronictl reinit --force` fuera sobrescrito por el intento de recuperar un Postgres detenido. Esto terminaba en una situación en la que Patroni intentaba iniciar Postgres mientras el basebackup se estaba ejecutando.

- Corrige una condición de carrera en el método `postmaster_start_time()` (Alexander Kukushkin)

  Si el método se ejecuta desde el hilo de la REST API, requiere que se cree un objeto cursor separado.

- Corrige el problema de no promover el standby síncrono que tenía un nombre que contenía letras mayúsculas (Alexander Kukushkin)

  Convertíamos el nombre a minúsculas porque Postgres hacía lo mismo al comparar el `application_name` con el valor en `synchronous_standby_names`.

- Mata a todos los hijos junto con el proceso del callback antes de iniciar el nuevo (Alexander Kukushkin)

  No hacerlo hace difícil implementar callbacks en bash y eventualmente puede llevar a la situación en que dos callbacks se estén ejecutando al mismo tiempo.

- Corrige el problema de 'start failed' (Alexander Kukushkin)

  Bajo ciertas condiciones, el estado de Postgres podía establecerse en 'start failed' a pesar de que Postgres estuviera activo y funcionando.

--------

## Versión 1.6.0 {#version-160}

Publicado el 2019-08-05

Esta versión añade compatibilidad con PostgreSQL 12, hace posible ejecutar pg_rewind sin superusuario en PostgreSQL 11 y posteriores, y habilita el soporte de IPv6.

**Nuevas funcionalidades**

- Psycopg2 fue eliminado de los requisitos y debe instalarse de forma independiente (Alexander Kukushkin)

  A partir de 2.8.0, `psycopg2` se dividió en dos paquetes diferentes, `psycopg2` y `psycopg2-binary`, que podían instalarse al mismo tiempo en el mismo lugar del sistema de archivos. Para disminuir el problema del infierno de dependencias, dejamos que el usuario elija cómo instalarlo. Hay algunas opciones disponibles; consulta la [documentación](/es/patroni/installation#psycopg2_install_options).

- Compatibilidad con PostgreSQL 12 (Alexander Kukushkin)

  A partir de PostgreSQL 12 ya no existe `recovery.conf` y todos los antiguos parámetros de recuperación se convierten en [GUC](https://www.enterprisedb.com/blog/what-guc-variable). Para protegerse de `ALTER SYSTEM SET primary_conninfo` o similar, Patroni analizará `postgresql.auto.conf` y eliminará de allí todos los parámetros de standby y de recuperación. La configuración de Patroni sigue siendo compatible con versiones anteriores. Por ejemplo, a pesar de que `restore_command` es un GUC, todavía se puede especificar en la sección `postgresql.recovery_conf.restore_command` y Patroni lo escribirá en `postgresql.conf` para PostgreSQL 12.

- Hace posible usar `pg_rewind` sin superusuario en PostgreSQL 11 y posteriores (Alexander Kukushkin)

  Si quieres usar esta función, define `username` y `password` en la sección `postgresql.authentication.rewind` del archivo de configuración de Patroni. Para un clúster ya existente tendrás que crear el usuario manualmente y concederle permisos sobre algunas funciones mediante `GRANT EXECUTE`. Puedes encontrar más detalles en la [documentación](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) de PostgreSQL.

- Hace una comparación inteligente de los valores real y deseado de `primary_conninfo` en las réplicas (Alexander Kukushkin)

  Puede ayudar a evitar el reinicio de la réplica cuando conviertes un clúster primario-standby ya existente en uno gestionado por Patroni

- Soporte de IPv6 (Alexander Kukushkin)

  Había dos problemas principales. El servicio de la REST API de Patroni escuchaba solo en `0.0.0.0` y las direcciones IP IPv6 usadas en `api_url` y `conn_url` no estaban correctamente entrecomilladas.

- Soporte de Kerberos (Ajith Vilas, Alexander Kukushkin)

  Hace posible usar autenticación Kerberos entre los nodos de Postgres en lugar de definir contraseñas en el archivo de configuración de Patroni

- Gestiona `pg_ident.conf` (Alexander Kukushkin)

  Esta funcionalidad funciona de forma similar a `pg_hba.conf`: si `postgresql.pg_ident` está definido en el archivo de configuración o en el DCS, Patroni escribirá su valor en `pg_ident.conf`; sin embargo, si `postgresql.parameters.ident_file` está definido, Patroni asumirá que `pg_ident` se gestiona desde fuera y no actualizará el archivo.

**Mejoras en la REST API**

- Añade el endpoint `/health` (Wilfried Roset)

  Devolverá el código de estado HTTP 200 solo si PostgreSQL se está ejecutando

- Añade los endpoints `/read-only` y `/read-write` (Julien Riou)

  El endpoint `/read-only` habilita lecturas balanceadas entre las réplicas y el primario. El endpoint `/read-write` es un alias de `/primary`, `/leader` y `/master`.

- Usa `SSLContext` para envolver el socket de la REST API (Julien Riou)

  El uso de `ssl.wrap_socket()` está obsoleto y todavía permitía protocolos pronto obsoletos como TLS 1.1.

**Mejoras en el registro**

- Registro en dos pasos (Alexander Kukushkin)

  Todos los mensajes de registro se escriben primero en una cola en memoria y luego se vacían de forma asíncrona a stderr o a un archivo desde un hilo separado. El tamaño máximo de la cola está limitado (configurable). Si se alcanza el límite, Patroni comenzará a perder registros, lo que sigue siendo mejor que bloquear el ciclo de HA.

- Habilita el registro de depuración para las llamadas GET/OPTIONS a la API junto con la latencia (Jan Tomsa)

  Ayudará a depurar las comprobaciones de estado realizadas por HAProxy, Consul u otras herramientas que deciden qué nodo es el primario/réplica.

- Registra las excepciones capturadas en Retry (Daniel Kucera)

  Registra la excepción final cuando se alcanza el número de intentos o el tiempo de espera. Con suerte ayudará a depurar algunos problemas cuando falla la comunicación con el DCS.

**Mejoras en patronictl**

- Mejora los diálogos para el switchover y el reinicio programados (Rafia Sabih)

  Anteriormente los diálogos no tenían en cuenta las acciones programadas y, por lo tanto, eran engañosos.

- Comprueba si el archivo de configuración existe (Wilfried Roset)

  Es explícito sobre el archivo de configuración cuando el nombre de archivo dado no existe, en lugar de ignorarlo silenciosamente (lo que puede llevar a malentendidos).

- Añade un valor de reserva para `EDITOR` (Wilfried Roset)

  Cuando la variable de entorno `EDITOR` no estaba definida, `patronictl edit-config` fallaba con `PatroniCtlException`. La nueva estrategia es probar `editor` y luego `vi`, que deberían estar disponibles en la mayoría de los sistemas.

**Mejoras en el soporte de Consul**

- Permite especificar el modo de consistencia de Consul (Jan Tomsa)

  Puedes leer más sobre el modo de consistencia [aquí](https://www.consul.io/api/features/consistency.html).

- Recarga la configuración de Consul al recibir SIGHUP (Cameron Daniel Kucera, Alexander Kukushkin)

  Es especialmente útil cuando alguien cambia el valor de `token`.

**Correcciones de errores**

- Corrige un caso extremo en la conmutación por error/switchover (Sharoon Thomas)

  La variable `scheduled_at` puede quedar sin definir si la REST API no es accesible y usamos el DCS como alternativa.

- Abre trust a localhost en `pg_hba.conf` durante el bootstrap personalizado (Alexander Kukushkin)

  Anteriormente estaba abierto solo a unix_socket, lo que causaba muchos errores: `FATAL:  no pg_hba.conf entry for replication connection from host "127.0.0.1", user "replicator"`

- Considera sano al nodo síncrono incluso cuando el antiguo líder está por delante (Alexander Kukushkin)

  Si el primario pierde el acceso al DCS, reinicia Postgres en modo de solo lectura, pero puede ocurrir que otros nodos todavía puedan acceder al antiguo primario mediante la REST API. Tal situación provocaba que el standby síncrono no promoviera porque el antiguo primario reportaba una posición de WAL por delante del standby síncrono.

- Correcciones de errores del clúster en espera (Alexander Kukushkin)

  Hace posible inicializar una réplica en un clúster en espera cuando el standby_leader no es accesible, junto con algunas otras correcciones menores.

--------

## Versión 1.5.6 {#version-156}

Publicado el 2019-08-03

**Nuevas funcionalidades**

- Soporta el trabajo con el clúster de etcd mediante un conjunto de proxies (Alexander Kukushkin)

  Puede ocurrir que el clúster de etcd no sea accesible directamente sino mediante un conjunto de proxies. En ese caso, Patroni no realizará el descubrimiento de la topología de etcd, sino simplemente un round-robin a través de los hosts proxy. El comportamiento se controla con `etcd.use_proxies`.

- Cambió el comportamiento de los callbacks cuando cambia el rol en el nodo (Alexander Kukushkin)

  Si el rol cambió de `master` o `standby_leader` a `replica`, o de `replica` a `standby_leader`, el callback `on_restart` ya no se llamará en favor del callback `on_role_change`.

- Cambia la forma en que iniciamos postgres (Alexander Kukushkin)

  Usa `multiprocessing.Process` en lugar de ejecutarse a sí mismo y `multiprocessing.Pipe` para transmitir el pid del postmaster al proceso de Patroni. Antes usábamos pipes, lo que dejaba el proceso postmaster con stdin cerrado.

**Correcciones de errores**

- Corrige el rol devuelto por la REST API para el líder en espera (Alexander Kukushkin)

  Devolvía incorrectamente `replica` en lugar de `standby_leader`

- Espera el fin del callback si no pudo ser terminado (Julien Tachoires)

  Patroni no tiene privilegios suficientes para terminar el script de callback que se ejecuta bajo `sudo`, lo que cancelaba el nuevo callback. Si el script en ejecución no pudo ser terminado, Patroni esperará a que termine y luego ejecutará el siguiente callback.

- Reduce el tiempo de bloqueo tomado por el método dcs.get_cluster (Alexander Kukushkin)

  Debido a que se retenía el bloqueo, la lentitud del DCS afectaba las comprobaciones de estado de la REST API, causando falsos positivos.

- Mejora la limpieza del PGDATA cuando `pg_wal`/`pg_xlog` es un enlace simbólico (Julien Tachoires)

  En ese caso, Patroni eliminará explícitamente los archivos del directorio de destino.

- Elimina el uso innecesario de os.path.relpath (Ants Aasma)

  Depende de poder resolver el directorio de trabajo, lo que fallará si Patroni se inicia en un directorio que luego se desvincula del sistema de archivos.

- No impone la versión de ssl al comunicarse con Etcd (Alexander Kukushkin)

  Por alguna razón desconocida, python3-etcd en debian y ubuntu no se basa en la última versión del paquete y, por lo tanto, impone TLSv1, que no está soportado por Etcd v3. Resolvimos este problema por el lado de Patroni.

--------

## Versión 1.5.5 {#version-155}

Publicado el 2019-02-15

Esta versión introduce la posibilidad de reinicializar automáticamente el antiguo master, mejora la salida de patronictl list y corrige varios errores.

**Nuevas funcionalidades**

- Añade soporte de las variables de entorno `PATRONI_ETCD_PROTOCOL`, `PATRONI_ETCD_USERNAME` y `PATRONI_ETCD_PASSWORD` (Étienne M)

  Antes solo era posible configurarlas en el archivo de configuración o como parte de `PATRONI_ETCD_URL`, lo cual no siempre es conveniente.

- Hace posible reinicializar automáticamente el antiguo master (Alexander Kukushkin)

  Si pg_rewind está deshabilitado o no puede usarse, el antiguo master podía fallar al iniciarse como nueva réplica debido a líneas de tiempo divergentes. En ese caso, la única forma de arreglarlo es borrar el directorio de datos y reinicializar. Este comportamiento podía cambiarse estableciendo `postgresql.remove_data_directory_on_diverged_timelines`. Cuando está establecido, Patroni borrará el directorio de datos y reinicializará automáticamente el antiguo master.

- Muestra información sobre las líneas de tiempo en patronictl list (Alexander Kukushkin)

  Ayuda a detectar réplicas obsoletas. Además, `Host` incluirá ':{port}' si el valor del puerto no es el predeterminado o hay más de un miembro ejecutándose en el mismo host.

- Crea un servicio headless asociado con el endpoint \$SCOPE-config (Alexander Kukushkin)

  El endpoint "config" mantiene información sobre la configuración de Patroni y Postgres de todo el clúster, el archivo de historial y, por último pero más importante, retiene la clave `initialize`. Cuando el nodo master de Kubernetes se reinicia o se actualiza, elimina los endpoints sin servicios. El servicio headless evitará que se elimine.

**Correcciones de errores**

- Ajusta el tiempo de espera de lectura para la consulta de bloqueo del watch del líder (Alexander Kukushkin)

  Según la documentación de Consul, el tiempo de espera real de respuesta se incrementa en una pequeña cantidad aleatoria de tiempo de espera adicional añadida al tiempo de espera máximo suministrado, para distribuir el momento de despertar de cualquier solicitud concurrente. Añade hasta `wait / 16` de tiempo adicional a la duración máxima. En nuestro caso añadimos `wait / 15` o 1 segundo, dependiendo de cuál sea mayor.

- Usa siempre replication=1 al conectarse mediante el protocolo de replicación a postgres (Alexander Kukushkin)

  A partir de Postgres 10, la línea en pg_hba.conf con database=replication no acepta conexiones con el parámetro replication=database.

- No escribe primary_conninfo en recovery.conf para un clúster en espera solo con WAL (Alexander Kukushkin)

  A pesar de no tener ni `host` ni `port` definidos en la configuración de [standby_cluster](/es/patroni/standby_cluster#standby_cluster), Patroni ponía el `primary_conninfo` en el `recovery.conf`, lo cual es inútil y generaba muchos errores.

--------

## Versión 1.5.4 {#version-154}

Publicado el 2019-01-15

Esta versión implementa un registro flexible y corrige varios errores.

**Nuevas funcionalidades**

- Mejoras en la infraestructura de registro (Alexander Kukushkin, Lucas Capistrant, Alexander Anikin)

  La configuración de registro podía configurarse no solo desde variables de entorno sino también desde el archivo de configuración de Patroni. Hace posible cambiar la configuración de registro en tiempo de ejecución actualizando la configuración y haciendo una recarga o enviando SIGHUP al proceso de Patroni. Por defecto, Patroni escribe los registros en stderr, pero ahora pasa a ser posible escribir los registros directamente en el archivo y rotarlos cuando alcanza un cierto tamaño. Además, se añadió soporte de formato de fecha personalizado y la posibilidad de ajustar finamente el nivel de registro para cada módulo de python.

- Hace posible tener en cuenta la línea de tiempo actual durante las elecciones de líder (Alexander Kukushkin)

  Podía ocurrir que el nodo se considere a sí mismo el más sano aunque actualmente no esté en la última línea de tiempo conocida. En algunos casos queremos evitar la promoción de tal nodo, lo que puede lograrse estableciendo el parámetro `check_timeline` en `true` (el comportamiento predeterminado no cambia).

- Relaja los requisitos sobre las credenciales de superusuario

  Libpq permite abrir conexiones sin especificar explícitamente ni el nombre de usuario ni la contraseña. Dependiendo de la situación, depende del archivo pgpass o del método de autenticación trust en pg_hba.conf. Dado que pg_rewind también usa libpq, funcionará de la misma manera.

- Implementa la posibilidad de configurar el registro del servicio de Consul y el intervalo de comprobación mediante variables de entorno (Alexander Kukushkin)

  El registro del servicio en Consul se añadió en la 1.5.0, pero hasta ahora solo era posible activarlo mediante patroni.yaml.

**Mejoras de estabilidad**

- Establece archive_mode en off durante el bootstrap personalizado (Alexander Kukushkin)

  Queremos evitar el archivado de WAL y archivos de historial hasta que el clúster sea completamente funcional. Realmente ayuda si el bootstrap personalizado involucra pg_upgrade.

- Aplica una espera de cinco segundos al cargar la configuración global al inicio (Alexander Kukushkin)

  Ayuda a evitar martillear el DCS cuando Patroni apenas se está iniciando.

- Reduce la cantidad de mensajes de error generados al apagarse (Alexander Kukushkin)

  Eran inofensivos pero bastante molestos y a veces alarmantes.

- Asegura explícitamente los permisos rw de recovery.conf en el momento de su creación (Lucas Capistrant)

  No queremos que nadie excepto el usuario patroni/postgres lea este archivo, porque contiene el usuario y la contraseña de replicación.

- Redirige las excepciones del HTTPServer al logger (Julien Riou)

  Por defecto, dichas excepciones se registraban en la salida estándar, mezclándose con los registros habituales.

**Correcciones de errores**

- Elimina la tubería de stderr a stdout en el proceso de pg_ctl (Cody Coons)

  Heredar stderr del proceso principal de Patroni permite ver todos los registros de Postgres junto con todos los registros de patroni. Esto es muy útil en un entorno de contenedores, ya que los registros de Patroni y Postgres pueden consumirse con herramientas estándar (docker logs, kubectl, etc.). Además, este cambio corrige un error por el cual Patroni no podía capturar el pid del postmaster cuando postgres escribía algunas advertencias en stderr.

- Establece el tiempo de espera de desregistro de la comprobación del servicio de Consul en formato de tiempo de Go (Pavel Kirillov)

  Sin la unidad de tiempo mencionada explícitamente, el registro fallaba.

- Relaja las comprobaciones de la configuración del clúster standby_cluster (Dmitry Dolgov, Alexander Kukushkin)

  Solo aceptaba cadenas como valores válidos y, por lo tanto, no era posible especificar el puerto como entero ni create_replica_methods como lista.

--------

## Versión 1.5.3 {#version-153}

Publicado el 2018-12-03

Versión de compatibilidad y corrección de errores.

- Mejora la estabilidad al ejecutarse con python3 contra zookeeper (Alexander Kukushkin)

  El cambio de `loop_wait` provocaba que Patroni se desconectara de zookeeper y nunca volviera a conectarse.

- Corrige la compatibilidad rota con postgres 9.3 (Alexander Kukushkin)

  Al abrir una conexión de replicación debemos especificar replication=1, porque 9.3 no entiende replication='database'

- Garantiza que refresquemos la sesión de Consul al menos una vez por ciclo de HA y mejora el manejo de las excepciones de sesiones de consul (Alexander Kukushkin)

  El reinicio del agente local de consul invalida todas las sesiones relacionadas con el nodo. No llamar al refresco de sesión a tiempo y no hacer un manejo adecuado de los errores de sesión provocaba la degradación del primario.

--------

## Versión 1.5.2 {#version-152}

Publicado el 2018-11-26

Versión de compatibilidad y corrección de errores.

- Compatibilidad con kazoo-2.6.0 (Alexander Kukushkin)

  Para asegurarse de que las solicitudes se realicen con un tiempo de espera apropiado, Patroni redefine el método create_connection del módulo python-kazoo. La última versión de kazoo cambió ligeramente la forma en que se llama al método create_connection.

- Corrige el fallo de Patroni cuando el clúster de Consul pierde al líder (Alexander Kukushkin)

  El fallo ocurría debido a una implementación incorrecta del método touch_member; debe devolver un booleano y no generar ninguna excepción.

--------

## Versión 1.5.1 {#version-151}

Publicado el 2018-11-01

Esta versión implementa el soporte de slots de replicación permanentes, añade soporte de pgBackRest y corrige varios errores.

**Nuevas funcionalidades**

- Slots de replicación permanentes (Alexander Kukushkin)

  Los slots de replicación permanentes se conservan en la conmutación por error/switchover; es decir, Patroni en el nuevo primario creará los slots de replicación configurados justo después de hacer la promoción. Los slots pueden configurarse con la ayuda de `patronictl edit-config`. La configuración inicial también puede hacerse en [bootstrap.dcs](/es/patroni/config/yaml#yaml).

- Añade soporte de pgbackrest (Yogesh Sharma)

  pgBackrest puede restaurar en la carpeta \$PGDATA existente; esto permite una restauración rápida, ya que se omiten los archivos que no han cambiado desde la última copia de seguridad. Para soportar esta función se ha introducido el nuevo parámetro `keep_data`. Consulta la sección [método de creación de réplicas](/es/patroni/replica_bootstrap#custom_replica_creation) para ejemplos adicionales.

**Correcciones de errores**

- Algunas correcciones de errores en el flujo de trabajo del «clúster en espera» (Alexander Kukushkin)

  Consulta <https://github.com/patroni/patroni/pull/823> para más detalles.

- Corrige la comprobación de estado de la REST API cuando la gestión del clúster está en pausa y el DCS no es accesible (Alexander Kukushkin)

  La regresión se introdujo en <https://github.com/patroni/patroni/commit/90cf930036a9d5249265af15d2b787ec7517cf57>

--------

## Versión 1.5.0 {#version-150}

Publicado el 2018-09-20

Esta versión permite que el clúster de HA de Patroni opere en modo standby, introduce soporte experimental para ejecutarse en Windows y proporciona un nuevo parámetro de configuración para registrar el servicio de PostgreSQL en Consul.

**Nuevas funcionalidades**

- Clúster en espera (Dmitry Dolgov)

  Uno o más nodos de Patroni pueden formar un clúster en espera que se ejecuta junto al primario (es decir, en otro centro de datos) y consta de nodos standby que replican desde el master del clúster primario. Todos los nodos de PostgreSQL del clúster en espera son réplicas; una de esas réplicas se elige a sí misma para replicar directamente desde el master remoto, mientras que las demás replican de ella en cascada. Puede encontrarse una descripción más detallada de esta función y algunos ejemplos de configuración [aquí](/es/patroni/standby_cluster#standby_cluster).

- Registra servicios en Consul (Pavel Kirillov, Alexander Kukushkin)

  Si el parámetro `register_service` de la [configuración](/es/patroni/config/yaml#consul_settings) de consul está habilitado, el nodo registrará un servicio con el nombre `scope` y la etiqueta `master`, `replica` o `standby-leader`.

- Soporte experimental de Windows (Pavel Golub)

  A partir de ahora es posible ejecutar Patroni en Windows, aunque el soporte de Windows es completamente nuevo y no ha recibido tantas pruebas en el mundo real como su contraparte de Linux. ¡Agradecemos tus comentarios!

**Mejoras en patronictl**

- Añade la opción patronictl -k/--insecure y soporte para el certificado de restapi (Wilfried Roset)

  En el pasado, si la REST API estaba protegida por certificados autofirmados, [patronictl](/es/patroni/patronictl#patronictl) fallaba al verificarlos. No había forma de deshabilitar esa verificación. Ahora es posible configurar [patronictl](/es/patroni/patronictl#patronictl) para omitir por completo la verificación del certificado o proporcionar los certificados de CA y de cliente en la sección [ctl:](/es/patroni/config/yaml#patronictl_settings) de la configuración.

- Excluye a los miembros con la etiqueta nofailover de la salida de patronictl switchover/failover (Alexander Anikin)

  Anteriormente, esos miembros se proponían incorrectamente como candidatos al realizar un switchover o conmutación por error interactivos mediante patronictl.

**Mejoras de estabilidad**

- Evita analizar las líneas de salida de pg_controldata que no son clave-valor (Alexander Anikin)

  Bajo ciertas circunstancias, pg_controldata emite líneas sin el carácter de dos puntos. Eso provocaría un error en el código de Patroni que analizaba la salida de pg_controldata, ocultando el problema real; a menudo dichas líneas se emiten en una advertencia mostrada por pg_controldata antes de la salida regular, es decir, cuando la versión principal del binario no coincide con la del directorio de datos de PostgreSQL.

- Añade el nombre del miembro al mensaje de error durante la elección de líder (Jan Mussler)

  Durante la elección de líder, Patroni se conecta a todos los miembros conocidos del clúster y solicita su estado. Dicho estado se escribe en el registro de Patroni e incluye el nombre del miembro. Anteriormente, si el miembro no era accesible, el mensaje de error no indicaba su nombre, conteniendo solo la URL.

- Reserva inmediatamente la posición de WAL al crear el slot de replicación (Alexander Kukushkin)

  A partir de 9.6, la función `pg_create_physical_replication_slot` proporciona un parámetro booleano adicional `immediately_reserve`. Cuando está establecido en `false`, que también es el valor predeterminado, el slot no reserva la posición de WAL hasta que recibe la primera conexión de cliente, perdiendo potencialmente algunos segmentos requeridos por el cliente en una ventana de tiempo entre la creación del slot y la conexión inicial del cliente.

- Corrige un error en la replicación síncrona estricta (Alexander Kukushkin)

  Al ejecutarse con `synchronous_mode_strict: true`, en algunos casos Patroni pone `*` en `synchronous_standby_names`, cambiando el estado de sincronización de la mayoría de las conexiones de replicación a `potential`. Anteriormente, Patroni no podía elegir un candidato síncrono en tales circunstancias, ya que solo consideraba aquellos con el estado `async`.

--------

## Versión 1.4.6 {#version-146}

Publicado el 2018-08-14

**Correcciones de errores y mejoras de estabilidad**

Esta versión corrige un problema crítico con el endpoint /master de la API de Patroni que devolvía 200 para el nodo no master. Es un problema de reporte, no un split-brain real, pero bajo ciertas circunstancias los clientes podrían ser dirigidos al nodo de solo lectura.

- Restablece el estado is_leader al degradar (Alexander Kukushkin, Oleksii Kliukin)

  Garantiza que el miembro degradado del clúster deje de responder con el código 200 en la llamada a la API /master.

- Añade el nuevo campo "cluster_unlocked" a la salida de la API (Dmitry Dolgov)

  Este campo indica si el clúster tiene el master en ejecución. Puede usarse cuando no es posible consultar ningún otro nodo salvo una de las réplicas.

--------

## Versión 1.4.5 {#version-145}

Publicado el 2018-08-03

**Nuevas funcionalidades**

- Mejora el registro al aplicar la nueva configuración de postgres (Don Seiler)

  Patroni registra los nombres y valores de los parámetros cambiados.

- Compatibilidad con Python 3.7 (Christoph Berg)

  async es una palabra reservada en python3.7

- Establece el estado en "stopped" en el DCS cuando se apaga un miembro (Tony Sorrentino)

  Esto muestra el estado del miembro como "stopped" en el comando "patronictl list".

- Mejora el mensaje registrado cuando un postmaster.pid obsoleto coincide con un proceso en ejecución (Ants Aasma)

  El anterior era más que confuso.

- Implementa la funcionalidad patronictl reload (Don Seiler)

  Antes de esto, solo era posible recargar la configuración llamando a la REST API o enviando la señal SIGHUP al proceso de Patroni.

- Toma y aplica algunos parámetros del controldata al iniciarse como réplica (Alexander Kukushkin)

  El valor de `max_connections` y de algunos otros parámetros establecidos en la configuración global puede ser menor que el realmente usado por el primario; cuando esto ocurre, la réplica no puede iniciarse y debe corregirse manualmente. Patroni ahora se encarga de ello leyendo y aplicando el valor de `pg_controldata`, iniciando postgres y estableciendo el indicador `pending_restart`.

- Si está establecido, usa LD_LIBRARY_PATH al iniciar postgres (Chris Fraser)

  Al iniciar Postgres, Patroni pasaba las variables de entorno PATH, LC_ALL y LANG si estaban establecidas. Ahora hace lo mismo con LD_LIBRARY_PATH. Debería ayudar si alguien instaló PostgreSQL en un lugar no estándar.

- Cambia el nombre de create_replica_method a create_replica_methods (Dmitry Dolgov)

  Para dejar claro que en realidad es un array. El nombre antiguo sigue soportado por compatibilidad con versiones anteriores.

**Correcciones de errores y mejoras de estabilidad**

- Corrige la condición para el inicio de la réplica debido a pg_rewind en estado de pausa (Oleksii Kliukin)

  Evita iniciar la réplica que ya había ejecutado pg_rewind antes.

- Responde 200 a la comprobación de estado del master solo si update_lock ha tenido éxito (Alexander Kukushkin)

  Evita que Patroni se reporte a sí mismo como master en el antiguo master (degradado) si el DCS está particionado.

- Corrige la compatibilidad con el nuevo módulo de consul (Alexander Kukushkin)

  A partir de v1.1.0, python-consul cambió la API interna y comenzó a usar `list` en lugar de `dict` para pasar los parámetros de consulta.

- Captura las excepciones del hilo de la REST API de Patroni durante el apagado (Alexander Kukushkin)

  Esas excepciones no capturadas mantenían PostgreSQL en ejecución al apagarse.

- Hace la recuperación ante fallos solo cuando Postgres se ejecuta como master (Alexander Kukushkin)

  Requiere que `pg_controldata` reporte 'in production', 'shutting down' o 'in crash recovery'. En todos los demás casos no es necesaria la recuperación ante fallos.

- Mejora el manejo de los errores de configuración (Henning Jacobs, Alexander Kukushkin)

  Es posible cambiar muchos parámetros en tiempo de ejecución (incluido `restapi.listen`) actualizando el archivo de configuración de Patroni y enviando SIGHUP al proceso de Patroni. Esta corrección elimina las excepciones oscuras del hilo de 'restapi' cuando algunos de los parámetros reciben valores inválidos.

--------

## Versión 1.4.4 {#version-144}

Publicado el 2018-05-22

**Mejoras de estabilidad**

- Corrige una condición de carrera en poll_failover_result (Alexander Kukushkin)

  No afectaba directamente ni a la conmutación por error ni al switchover, pero en algunos casos raros reportaba el éxito demasiado pronto, cuando el antiguo líder liberó el bloqueo, produciendo un mensaje 'Failed over to "None"' en lugar de 'Failed over to "desired-node"'.

- Trata los nombres de los parámetros de Postgres como insensibles a mayúsculas/minúsculas (Alexander Kukushkin)

  La mayoría de los parámetros de Postgres tienen nombres snake_case, pero hay tres excepciones a esta regla: DateStyle, IntervalStyle y TimeZone. Postgres acepta esos parámetros cuando se escriben con mayúsculas/minúsculas diferentes (p. ej. timezone = 'some/tzn'); sin embargo, Patroni no podía encontrar coincidencias insensibles a mayúsculas/minúsculas de esos nombres de parámetros en pg_settings y, como resultado, ignoraba dichos parámetros.

- Aborta el inicio si se adjunta a un postgres en ejecución y el clúster no está inicializado (Alexander Kukushkin)

  Patroni puede adjuntarse a una instancia de Postgres que ya está en ejecución. Es imprescindible empezar ejecutando Patroni en el nodo master antes de pasar a las réplicas.

- Corrige el comportamiento de patronictl scaffold (Alexander Kukushkin)

  Pasa un objeto dict a `touch_member` en lugar de una cadena codificada en JSON; la implementación del DCS se encargará de codificarlo.

- No degrada el master si falla la actualización de la clave de líder en pausa (Alexander Kukushkin)

  Durante el mantenimiento, un DCS puede comenzar a fallar en las solicitudes de escritura mientras sigue respondiendo a las de lectura. En ese caso, Patroni solía poner el nodo master de Postgres en modo de solo lectura tras fallar la actualización del bloqueo de líder en el DCS.

- Sincroniza los slots de replicación cuando Patroni nota un nuevo proceso postmaster (Alexander Kukushkin)

  Si Postgres se ha reiniciado, Patroni debe asegurarse de que la lista de slots de replicación coincida con sus expectativas.

- Verifica el sysid y sincroniza los slots de replicación después de salir de la pausa (Alexander Kukushkin)

  Durante el modo `maintenance` puede ocurrir que el directorio de datos haya sido completamente reescrito y, por lo tanto, tenemos que asegurarnos de que el `Database system identifier` todavía pertenezca a nuestro clúster y de que los slots de replicación estén sincronizados con las expectativas de Patroni.

- Corrige un posible fallo al iniciar un Postgres que no está en ejecución sobre un directorio de datos con el archivo de bloqueo del postmaster presente (Alexander Kukushkin)

  Detecta la reutilización de un PID del archivo de bloqueo del postmaster. Es más probable encontrarse con tal problema si ejecutas Patroni y Postgres en el contenedor de docker.

- Mejora la protección del DCS contra borrados accidentales (Alexander Kukushkin)

  Patroni tiene mucha lógica implementada para prevenir la conmutación por error en tal caso; también puede restaurar todas las claves; sin embargo, hasta este cambio, una eliminación accidental de la clave /config desactivaba el modo de pausa durante 1 ciclo del bucle de HA.

- No termina al encontrar un identificador de sistema inválido (Oleksii Kliukin)

  No termina cuando el identificador de sistema del clúster está vacío o no pasa la comprobación de validación. En ese caso, lo más probable es que el clúster necesite un reinit; menciónalo en el mensaje del resultado. Evita terminar Patroni, ya que de lo contrario el reinit no puede ocurrir.

**Compatibilidad con Kubernetes 1.10+**

- Añade una comprobación de subsets vacíos (Cody Coons)

  Kubernetes 1.10.0+ comenzó a devolver `Endpoints.subsets` establecido en `None` en lugar de `[]`.

**Mejoras en el bootstrap**

- Hace opcional la eliminación de recovery.conf (Brad Nicholson)

  Si `bootstrap.<custom_bootstrap_method_name>.keep_existing_recovery_conf` está definido y establecido en `True`, Patroni no eliminará el archivo `recovery.conf` existente. Esto es útil al inicializar desde una copia de seguridad con herramientas como pgBackRest que generan el `recovery.conf` apropiado por ti.

- Permite opciones para el método integrado basebackup (Oleksii Kliukin)

  Ahora es posible suministrar opciones al método integrado basebackup definiendo la sección `basebackup` en la configuración, de forma similar a como se definen para los métodos personalizados de creación de réplicas. La diferencia está en el formato aceptado por la sección `basebackup`: dado que pg_basebackup acepta tanto opciones `--key=value` como `--key`, el contenido de la sección puede ser un diccionario de pares clave-valor o una lista de diccionarios de un solo elemento o simplemente claves (para las opciones que no aceptan valores). Consulta la sección [método de creación de réplicas](/es/patroni/replica_bootstrap#custom_replica_creation) para ejemplos adicionales.

--------

## Versión 1.4.3 {#version-143}

Publicado el 2018-03-05

**Mejoras en el registro**

- Hace configurable el nivel de registro desde variables de entorno (Andy Newton, Keyvan Hedayati)

  `PATRONI_LOGLEVEL` - establece el nivel de registro general `PATRONI_REQUESTS_LOGLEVEL` - establece el nivel de registro para todas las solicitudes HTTP, p. ej. las llamadas a la API de Kubernetes. Consulta la [documentación de registro de Python](https://docs.python.org/3.6/library/logging.html#levels) para obtener los nombres de los niveles de registro posibles

**Mejoras de estabilidad y correcciones de errores**

- No redescubre la topología del clúster de etcd cuando el watch excede el tiempo de espera (Alexander Kukushkin)

  Si tenemos solo un host en la configuración de etcd y precisamente ese host no es accesible, Patroni iniciaba el descubrimiento de la topología del clúster sin tener nunca éxito. En lugar de eso, debería simplemente cambiar al siguiente nodo disponible.

- Escribe el contenido de bootstrap.pg_hba en un pg_hba.conf después del bootstrap personalizado (Alexander Kukushkin)

  Ahora se comporta de forma similar al bootstrap habitual con `initdb`

- El modo usuario único esperaba la entrada del usuario y nunca terminaba (Alexander Kukushkin)

  La regresión se introdujo en <https://github.com/patroni/patroni/pull/576>

--------

## Versión 1.4.2 {#version-142}

Publicado el 2018-01-30

**Mejoras en patronictl**

- Cambia el nombre de failover programado a switchover programado (Alexander Kukushkin)

  Las funciones de failover y switchover se separaron en la versión 1.4, pero `patronictl list` todavía reportaba `Scheduled failover` en lugar de `Scheduled switchover`.

- Muestra información sobre los reinicios pendientes (Alexander Kukushkin)

  Para aplicar algunos cambios de configuración a veces es necesario reiniciar postgres. Patroni ya daba una pista sobre ello en la REST API y al escribir el estado del nodo en el DCS, pero no había una forma sencilla de mostrarlo.

- Hace que show-config funcione con el cluster_name del archivo de configuración (Alexander Kukushkin)

  Funciona de forma similar al `patronictl edit-config`

**Mejoras de estabilidad**

- Evita llamar a pg_controldata durante el bootstrap (Alexander Kukushkin)

  Durante initdb o un bootstrap personalizado hay una ventana de tiempo en la que pgdata no está vacío pero pg_control aún no se ha escrito. En tal caso, la llamada a pg_controldata fallaba con mensajes de error.

- Maneja las excepciones generadas por psutil (Alexander Kukushkin)

  cmdline se lee y analiza cada vez que se llama al método `cmdline()`. Podía ocurrir que el proceso examinado ya hubiera desaparecido; en ese caso se genera `NoSuchProcess`.

**Mejoras en el soporte de Kubernetes**

- No se traga los errores de la API de k8s (Alexander Kukushkin)

  Una llamada a la API de Kubernetes podía fallar por diferentes motivos. En algunos casos dicha llamada debería reintentarse; en otros, deberíamos registrar el mensaje de error y la traza de la excepción. Este cambio ayudará a depurar problemas de permisos de Kubernetes.

- Actualiza el Dockerfile de ejemplo de Kubernetes para instalar Patroni desde la rama master (Maciej Szulik)

  Antes usaba `feature/k8s`, que quedó desactualizado.

- Añade el RBAC adecuado para ejecutar patroni en k8s (Maciej Szulik)

  Añade la cuenta de servicio (Service account) que se asigna a los pods del clúster, el rol que contiene solo los permisos necesarios y el rolebinding que conecta la cuenta de servicio con el Rol.

--------

## Versión 1.4.1 {#version-141}

Publicado el 2018-01-17

**Correcciones en patronictl**

- No muestra el líder actual en la lista sugerida de miembros a los que hacer la conmutación por error. (Alexander Kukushkin)

  patronictl failover podía seguir funcionando cuando hay líder en el clúster y debería excluirse de la lista de miembros a los que es posible hacer la conmutación por error.

- Hace que patronictl switchover sea compatible con la antigua API de Patroni (Alexander Kukushkin)

  En caso de que la llamada POST /switchover a la REST API haya fallado con el código de estado 501, lo hará una vez más, pero al endpoint /failover.

--------

## Versión 1.4 {#version-14}

Publicado el 2018-01-10

Esta versión añade soporte para usar Kubernetes como DCS, lo que permite ejecutar Patroni como un agente cloud-native en Kubernetes sin despliegues adicionales de Etcd, Zookeeper o Consul.

**Aviso de actualización**

Instalar Patroni mediante pip ya no traerá dependencias (como bibliotecas para Etcd, Zookeeper, Consul o Kubernetes, o soporte para AWS). Para habilitarlas hay que listarlas explícitamente en el comando pip install, por ejemplo `pip install 'patroni[etcd,kubernetes]'`.

**Soporte de Kubernetes**

Implementa un DCS basado en Kubernetes. Los metadatos de los endpoints se usan para almacenar la configuración y la clave de líder. El campo de metadatos dentro de la definición de los pods se usa para almacenar los datos relacionados con los miembros. Además de usar Endpoints, Patroni soporta ConfigMaps. Puedes encontrar más información sobre esta función en el [capítulo de Kubernetes de la documentación](/es/patroni/kubernetes#kubernetes)

**Mejoras de estabilidad**

- Extrae el proceso postmaster a un objeto separado (Ants Aasma)

  Este objeto identifica un proceso postmaster en ejecución mediante el pid y la hora de inicio, y simplifica la detección (y resolución) de situaciones en las que el postmaster se reinició a nuestras espaldas o en las que el directorio de postgres desapareció del sistema de archivos.

- Minimiza la cantidad de SELECT emitidos por Patroni en cada ciclo del bucle de HA (Alexander Kukushkin)

  En cada iteración del ciclo de HA, Patroni necesita conocer el estado de recuperación y la posición absoluta de WAL. A partir de ahora, Patroni ejecutará solo un único SELECT para obtener esta información, en lugar de dos en la réplica y tres en el master.

- Elimina la clave de líder al apagarse solo cuando tenemos el bloqueo (Ants Aasma)

  La eliminación incondicional generaba excepciones innecesarias y engañosas.

**Mejoras en patronictl**

- Añade el comando version a patronictl (Ants Aasma)

  Mostrará la versión de Patroni instalada y las versiones de las instancias de Patroni en ejecución (si se especifica el nombre del clúster).

- Hace opcional especificar el argumento cluster_name para algunos comandos de patronictl (Alexander Kukushkin, Ants Aasma)

  Funcionará si patronictl usa el archivo de configuración habitual de Patroni con el `scope` definido.

- Muestra información sobre el switchover programado y el modo de mantenimiento (Alexander Kukushkin)

  Antes de esto, era posible obtener esta información solo de los registros de Patroni o directamente del DCS.

- Mejora `patronictl reinit` (Alexander Kukushkin)

  A veces `patronictl reinit` se negaba a continuar cuando Patroni estaba ocupado con otras acciones, concretamente intentando iniciar postgres. [patronictl](/es/patroni/patronictl#patronictl) no proporcionaba ningún comando para cancelar tales acciones de larga duración, y la única solución (peligrosa) era eliminar un directorio de datos manualmente. La nueva implementación de `reinit` cancela forzosamente otras acciones de larga duración antes de proceder con el reinit.

- Implementa la opción `--wait` en `patronictl pause` y `patronictl resume` (Alexander Kukushkin)

  Hará que [patronictl](/es/patroni/patronictl#patronictl) espere hasta que la acción solicitada sea reconocida por todos los nodos del clúster. Dicho comportamiento se logra exponiendo el indicador de [pausa](/es/patroni/pause#pause) para cada nodo en el DCS y mediante la REST API.

- Cambia el nombre de `patronictl failover` a `patronictl switchover` (Alexander Kukushkin)

  El `failover` anterior en realidad solo era capaz de hacer un switchover; se negaba a continuar en un clúster sin líder.

- Altera el comportamiento de `patronictl failover` (Alexander Kukushkin)

  Funcionará incluso si no hay líder, pero en ese caso tendrás que especificar explícitamente un nodo que debería convertirse en el nuevo líder.

**Exponer información sobre la línea de tiempo y el historial**

- Expone la línea de tiempo actual en el DCS y mediante la API (Alexander Kukushkin)

  Almacena información sobre la línea de tiempo actual de cada miembro del clúster. Esta información es accesible mediante la API y se almacena en el DCS

- Almacena el historial de promociones en la clave /history del DCS (Alexander Kukushkin)

  Además, almacena el historial de líneas de tiempo enriquecido con la marca de tiempo de la promoción correspondiente en la clave /history del DCS y lo actualiza con cada promoción.

**Añade endpoints para obtener réplicas síncronas y asíncronas**

- Añade los nuevos endpoints /sync y /async (Alexander Kukushkin, Oleksii Kliukin)

> Dichos endpoints (también accesibles como /synchronous y /asynchronous) devuelven 200 solo para las réplicas síncronas y asíncronas respectivamente (excluyendo las marcadas con `noloadbalance`).

**Permite múltiples hosts para Etcd**

- Añade el nuevo parámetro `hosts` a la configuración de Etcd (Alexander Kukushkin)

  Este parámetro debe contener la lista inicial de hosts que se usará para descubrir y poblar la lista de los miembros del clúster etcd en ejecución. Si por algún motivo durante el trabajo esta lista de hosts descubiertos se agota (no hay hosts disponibles de esa lista), Patroni volverá a la lista inicial del parámetro `hosts`.

--------

## Versión 1.3.6 {#version-136}

Publicado el 2017-11-10

**Mejoras de estabilidad**

- Verifica la hora de inicio del proceso al comprobar si postgres se está ejecutando. (Ants Aasma)

  Después de un fallo que no limpia el postmaster.pid podría haber un nuevo proceso con el mismo pid, lo que da como resultado un falso positivo en is_running(), lo que llevará a todo tipo de malos comportamientos.

- Apaga postgresql antes del bootstrap cuando perdimos el directorio de datos (ainlolcat)

  Cuando el directorio de datos del master se elimina por la fuerza, el proceso de postgres puede seguir vivo por algún tiempo e impedir que la réplica creada en el lugar de ese antiguo master se inicie o replique. La corrección hace que Patroni almacene en caché el pid del postmaster y su hora de inicio y le permite terminar el postmaster antiguo en caso de que aún se esté ejecutando después de que se haya eliminado el directorio de datos correspondiente.

- Realiza la recuperación ante fallos en modo usuario único si muere el master de postgres (Alexander Kukushkin)

  No es seguro iniciar inmediatamente como standby y no es posible ejecutar `pg_rewind` si postgres no se ha apagado limpiamente. La recuperación ante fallos en modo usuario único solo entra en juego si `pg_rewind` está habilitado o si no hay master en ese momento.

**Mejoras en Consul**

- Hace posible proporcionar la configuración de datacenter para Consul (Vilius Okockis, Alexander Kukushkin)

  Antes de esto, Patroni siempre se comunicaba con el datacenter del host en el que se ejecuta.

- Envía siempre un token en el encabezado http X-Consul-Token (Alexander Kukushkin)

  Si `consul.token` está definido en la configuración de Patroni, lo enviaremos siempre en el encabezado http 'X-Consul-Token'. El módulo python-consul intenta ser «consistente» con la REST API de Consul, que no acepta el token como parámetro de consulta para la [API de sesión](https://www.consul.io/api/session.html), pero sigue funcionando con el encabezado 'X-Consul-Token'.

- Ajusta el TTL de la sesión si el valor suministrado es menor que el mínimo posible (Stas Fomin, Alexander Kukushkin)

  Podía ocurrir que el TTL proporcionado en la configuración de Patroni sea menor que el mínimo soportado por Consul. En ese caso, el agente de Consul falla al crear una nueva sesión. Sin una sesión, Patroni no puede crear las claves de miembro y de líder en el almacén KV de Consul, lo que da como resultado un clúster no sano.

**Otras mejoras**

- Define un formato de registro personalizado mediante la variable de entorno `PATRONI_LOGFORMAT` (Stas Fomin)

  Permite deshabilitar las marcas de tiempo y otros campos similares en los registros de Patroni si ya los añade el logger del sistema (generalmente cuando Patroni se ejecuta como servicio).

--------

## Versión 1.3.5 {#version-135}

Publicado el 2017-10-12

**Corrección de error**

- Establece el rol en 'uninitialized' si el directorio de datos fue eliminado (Alexander Kukushkin)

  Si el nodo se estaba ejecutando como master, impedía la conmutación por error.

**Mejora de estabilidad**

- Intenta ejecutar el postmaster en modo usuario único si intentamos y fallamos al iniciar postgres (Alexander Kukushkin)

  Normalmente tal problema ocurre cuando un nodo que se ejecutaba como master fue terminado y las líneas de tiempo divergieron. Si `recovery.conf` tiene definido `restore_command`, hay altísimas probabilidades de que postgres aborte el inicio y deje el controldata sin cambios. Hace imposible usar `pg_rewind`, que requiere un apagado limpio.

**Mejoras en Consul**

- Hace posible especificar comprobaciones de estado al crear la sesión (Alexander Kukushkin)

  Si no se especifican, Consul usará "serfHealth". Por un lado, esto permite la detección rápida de un master aislado; por otro, hace imposible que Patroni tolere pequeños retrasos de red.

**Corrección de error**

- Corrige el watchdog en Python 3 (Ants Aasma)

  Un malentendido de la interfaz de la llamada ioctl(). Si mutable=False, entonces fcntl.ioctl() en realidad devuelve el búfer arg de vuelta. Esto funcionaba accidentalmente en Python2 porque la comparación entre int y str no devolvía un error. El reporte de errores en realidad se hace generando IOError en Python2 y OSError en Python3.

--------

## Versión 1.3.4 {#version-134}

Publicado el 2017-09-08

**Diversas mejoras en Consul**

- Pasa el token de consul como encabezado (Andrew Colin Kissa)

  Los encabezados son ahora la forma preferida de pasar el token a la [API](https://www.consul.io/api/index.html#authentication) de consul.

- Configuración avanzada para Consul (Alexander Kukushkin)

  posibilidad de especificar `scheme`, `token`, certificados de cliente y de CA [detalles](/es/patroni/config/yaml#consul_settings).

- compatibilidad con python-consul-0.7.1 y posteriores (Alexander Kukushkin)

  el nuevo módulo python-consul cambió la firma de algunos métodos

- El mensaje "Could not take out TTL lock" nunca se registraba (Alexander Kukushkin)

  No es un error crítico, pero la falta de un registro adecuado complica la investigación en caso de problemas.

**Entrecomilla synchronous_standby_names usando quote_ident**

- Al escribir `synchronous_standby_names` en el `postgresql.conf`, su valor debe ir entrecomillado (Alexander Kukushkin)

  Si no se entrecomilla correctamente, PostgreSQL deshabilitará efectivamente la replicación síncrona y continuará funcionando.

**Diversas correcciones de errores en torno al estado de pausa, en su mayoría relacionadas con el watchdog** (Alexander Kukushkin)

- No envía keepalives si el watchdog no está activo
- Evita activar el watchdog en modo de pausa
- Establece el estado correcto de postgres en modo de pausa
- No intenta ejecutar consultas desde la API si postgres está detenido

--------

## Versión 1.3.3 {#version-133}

Publicado el 2017-08-04

**Correcciones de errores**

- la replicación síncrona se deshabilitaba poco después de la promoción incluso cuando synchronous_mode_strict estaba activado (Alexander Kukushkin)
- crea un archivo `pg_ident.conf` vacío si falta después de restaurar desde la copia de seguridad (Alexander Kukushkin)
- abre el acceso en `pg_hba.conf` a todas las bases de datos, no solo a postgres (Franco Bellagamba)

--------

## Versión 1.3.2 {#version-132}

Publicado el 2017-07-31

**Corrección de error**

- patronictl edit-config no funcionaba con ZooKeeper (Alexander Kukushkin)

--------

## Versión 1.3.1 {#version-131}

Publicado el 2017-07-28

**Corrección de error**

- la conmutación por error mediante la API estaba rota debido a un cambio en `_MemberStatus` (Alexander Kukushkin)

--------

## Versión 1.3 {#version-13}

Publicado el 2017-07-27

La versión 1.3 añade la posibilidad de bootstrap personalizado, mejora significativamente el soporte de pg_rewind, refuerza el soporte del modo síncrono, añade la edición de configuración a patronictl e implementa el soporte del watchdog en Linux. Además, es la primera versión que funciona correctamente con PostgreSQL 10.

**Aviso de actualización**

No hay problemas de compatibilidad conocidos con la nueva versión de Patroni. La configuración de la versión 1.2 debería funcionar sin ningún cambio. Es posible actualizar instalando los nuevos paquetes y reiniciando Patroni (lo que provocará el reinicio de PostgreSQL), o poniendo primero a Patroni en [modo de pausa](/es/patroni/pause#pause) y luego reiniciando Patroni en todos los nodos del clúster (Patroni en modo de pausa no intentará detener/iniciar PostgreSQL), saliendo del modo de pausa al final.

**Bootstrap personalizado**

- Hace configurable el proceso de bootstrap del clúster (Alexander Kukushkin)

  Permite scripts de bootstrap personalizados en lugar de `initdb` al inicializar el primer nodo del clúster. El comando de bootstrap recibe el nombre del clúster y la ruta al directorio de datos. El clúster resultante puede configurarse para realizar una recuperación, haciendo posible inicializar desde una copia de seguridad y hacer una recuperación a un punto en el tiempo. Consulta la [página de documentación](/es/patroni/replica_bootstrap#custom_bootstrap) para una descripción más detallada de esta función.

**Soporte de pg_rewind más inteligente**

- Decide si ejecutar pg_rewind observando las diferencias de líneas de tiempo respecto al master actual (Alexander Kukushkin)

  Anteriormente, Patroni tenía un conjunto fijo de condiciones para activar pg_rewind, concretamente al iniciar un antiguo master, al hacer un switchover al nodo designado para todos los demás nodos del clúster, o cuando hay una réplica con la etiqueta nofailover. Todos esos casos tienen en común la posibilidad de que alguna réplica esté por delante del nuevo master. En algunos casos, pg_rewind no hacía nada; en otros, no se ejecutaba cuando era necesario. En lugar de depender de esta lista limitada de reglas, se hace que Patroni compare las posiciones WAL del master y de la réplica (usando el protocolo de replicación por streaming) para decidir de forma fiable si la réplica necesita rewind.

**Modo de replicación síncrona estricto**

- Refuerza el soporte de la replicación síncrona añadiendo el modo estricto (James Sewell, Alexander Kukushkin)

  Normalmente, cuando [synchronous_mode](/es/patroni/replication_modes#synchronous_mode) está habilitado y no hay réplicas adjuntas al master, Patroni deshabilitará la replicación síncrona para mantener el master disponible para escrituras. La opción `synchronous_mode_strict` cambia eso: cuando está establecida, Patroni no deshabilitará la replicación síncrona ante la falta de réplicas, bloqueando efectivamente a todos los clientes que escriben datos en el master. Además de la garantía del modo síncrono de prevenir cualquier pérdida de datos debida a la conmutación por error automática, el modo estricto asegura que cada escritura quede almacenada de forma duradera en dos nodos o que no ocurra en absoluto si solo hay un nodo en el clúster.

**Edición de configuración con patronictl**

- Añade la edición de configuración a patronictl (Ants Aasma, Alexander Kukushkin)

  Añade a patronictl la capacidad de editar la configuración dinámica del clúster almacenada en el DCS. Soporta tanto especificar los parámetros/valores desde la línea de comandos, invocar el \$EDITOR, como aplicar la configuración desde el archivo yaml.

**Soporte de watchdog en Linux**

- Implementa el soporte del watchdog para Linux (Ants Aasma)

  Soporta el watchdog por software de Linux para reiniciar el nodo donde Patroni no se está ejecutando o no responde (p. ej., por alta carga). El watchdog por software de Linux reinicia el nodo que no responde. Es posible configurar el dispositivo watchdog a usar (`/dev/watchdog` por defecto) y el modo (on, automatic, off) desde la sección watchdog de la configuración de Patroni. Puedes obtener más información en la [documentación del watchdog](/es/patroni/watchdog#watchdog).

**Añade soporte para PostgreSQL 10**

- Patroni es compatible con todas las versiones beta de PostgreSQL 10 publicadas hasta ahora y esperamos que sea compatible con PostgreSQL 10 cuando se publique.

**Mejoras menores relacionadas con PostgreSQL**

- Define pg_hba.conf mediante el archivo de configuración de Patroni o la configuración dinámica en el DCS (Alexander Kukushkin)

  Permite definir el contenido de `pg_hba.conf` en la subsección `pg_hba` de la sección `postgresql` de la configuración. Esto simplifica la gestión de `pg_hba.conf` en múltiples nodos, ya que basta con definirlo una sola vez en el DCS en lugar de iniciar sesión en cada nodo, cambiarlo manualmente y recargar la configuración.

  Cuando se define, el contenido de esta sección reemplazará por completo el `pg_hba.conf` actual. Patroni lo ignora si el parámetro de PostgreSQL `hba_file` está establecido.

- Soporta la conexión mediante un socket UNIX al clúster de PostgreSQL local (Alexander Kukushkin)

  Añade la opción `use_unix_socket` a la sección `postgresql` de la configuración de Patroni. Cuando se establece en true y la opción `unix_socket_directories` de PostgreSQL no está vacía, permite a Patroni usar el primer valor de esta para conectarse al clúster de PostgreSQL local. Si `unix_socket_directories` no está definida, Patroni asumirá su valor predeterminado y omitirá por completo el parámetro `host` en la cadena de conexión de PostgreSQL.

- Soporta el cambio de las credenciales de superusuario y replicación al recargar (Alexander Kukushkin)

- Soporta el almacenamiento de los archivos de configuración fuera del directorio de datos de PostgreSQL (@jouir)

  Añade la nueva directiva de configuración `config_dir` de la configuración `postgresql`. Por defecto es el directorio de datos y debe ser escribible por Patroni.

**Correcciones de errores y mejoras de estabilidad**

- Maneja las excepciones EtcdEventIndexCleared y EtcdWatcherCleared (Alexander Kukushkin)

  Recuperación más rápida cuando la operación de watch es terminada por Etcd, evitando reintentos inútiles.

- Elimina el bucle de errores ante fallos de Etcd y reduce el spam en el registro (Ants Aasma)

  Evita el reintento inmediato y la emisión de trazas de pila en el registro en el segundo y posteriores fallos de conexión a Etcd.

- Exporta las variables de locale al bifurcar procesos de PostgreSQL (Oleksii Kliukin)

  Evita el error fatal `postmaster became multithreaded during startup` en locales que no son ingleses para PostgreSQL compilado con NLS.

- Comprobaciones adicionales al eliminar el slot de replicación (Alexander Kukushkin)

  En algunos casos, el WAL sender impide que Patroni elimine el slot de replicación.

- Trunca el nombre del slot de replicación a 63 (NAMEDATALEN - 1) caracteres para cumplir las reglas de nomenclatura de PostgreSQL (Nick Scott)

- Corrige una condición de carrera que daba como resultado conexiones extra abiertas al clúster de PostgreSQL desde Patroni (Alexander Kukushkin)

- Libera la clave de líder cuando el nodo se reinicia con un directorio de datos vacío (Alex Kerney)

- Establece el ejecutor asíncrono como ocupado al ejecutar el bootstrap sin líder (Alexander Kukushkin)

  No hacerlo podía dar como resultado errores que afirmaban que el nodo pertenecía a un clúster diferente, ya que Patroni continuaba con el funcionamiento normal mientras era inicializado por un método de bootstrap que no requiere que haya un líder en el clúster.

- Mejora el método de creación de réplicas con WAL-E (Joar Wandborg, Alexander Kukushkin).

  - Usa csv.DictReader al analizar el base backup de WAL-E, aceptando fechas ISO con fecha y hora separadas por espacio.
  - Soporta la obtención de la posición WAL actual desde la réplica para estimar la cantidad de WAL a restaurar. Anteriormente, el código solía llamar a funciones de información del sistema que solo estaban disponibles en el nodo master.

--------

## Versión 1.2 {#version-12}

Publicado el 2016-12-13

Esta versión introduce mejoras significativas en el manejo de la replicación síncrona, hace más fiables el proceso de inicio y la conmutación por error, añade soporte de PostgreSQL 9.6 y corrige un buen número de errores. Además, la documentación, incluidas estas notas de versión, se ha trasladado a [https://patroni.readthedocs.io](https://patroni.readthedocs.io).

**Replicación síncrona**

- Añade soporte de replicación síncrona. (Ants Aasma)

  Añade una nueva variable de configuración [synchronous_mode](/es/patroni/replication_modes#synchronous_mode). Cuando está habilitado, Patroni gestionará `synchronous_standby_names` para activar la replicación síncrona siempre que haya standbys sanos disponibles. Cuando el modo síncrono está habilitado, Patroni hará la conmutación por error automáticamente solo a un standby que estuviera replicando de forma síncrona en el momento del fallo del master. Esto significa efectivamente que ninguna transacción visible para el usuario se pierde en tal caso. Consulta la [documentación de la función](/es/patroni/replication_modes#synchronous_mode) para la descripción detallada y los detalles de implementación.

**Mejoras de fiabilidad**

- No intenta actualizar la posición del líder almacenada en la clave `leader optime` cuando PostgreSQL no está 100% sano. Degrada inmediatamente cuando la actualización de la clave de líder falla. (Alexander Kukushkin)

- Excluye los nodos no sanos de la lista de objetivos desde los que clonar la nueva réplica. (Alexander Kukushkin)

- Implementa una estrategia de reintento y tiempo de espera para Consul similar a como se hace para Etcd. (Alexander Kukushkin)

- Hace que `--dcs` y `--config-file` se apliquen a todas las opciones de [patronictl](/es/patroni/patronictl#patronictl). (Alexander Kukushkin)

- Escribe todos los parámetros de postgres en postgresql.conf. (Alexander Kukushkin)

  Permite iniciar PostgreSQL configurado por Patroni con solo `pg_ctl`.

- Evita excepciones cuando no hay usuarios en la configuración. (Kirill Pushkin)

- Permite pausar un clúster no sano. Antes de esta corrección, [patronictl](/es/patroni/patronictl#patronictl) se retiraba si el nodo en el que intenta ejecutar la pausa no está sano. (Alexander Kukushkin)

- Mejora la funcionalidad de watch del líder. (Alexander Kukushkin)

  Anteriormente, las réplicas siempre estaban vigilando la clave de líder (durmiendo hasta el tiempo de espera o hasta que la clave de líder cambiara). Con este cambio, solo vigilan cuando el PostgreSQL de la réplica está en el estado `running` y no cuando está detenido/iniciando o reiniciando PostgreSQL.

- Evita caer en condiciones de carrera al manejar SIGCHLD como PID 1. (Alexander Kukushkin)

  Anteriormente podía ocurrir una condición de carrera al ejecutarse dentro de contenedores Docker, ya que el mismo proceso dentro de Patroni tanto generaba nuevos procesos como manejaba el SIGCHLD de estos. Este cambio usa fork/execs para Patroni y deja que el proceso PID 1 original sea el responsable de manejar las señales de los hijos.

- Corrige la restauración con WAL-E. (Oleksii Kliukin)

  Anteriormente, la restauración con WAL-E usaba el indicador `no_master` para evitar consultar al master por completo, haciendo que Patroni eligiera siempre restaurar desde WAL en lugar de `pg_basebackup`. Este cambio lo revierte al significado original de `no_master`, es decir, la restauración de Patroni con WAL-E puede seleccionarse como método de replicación si el master no se está ejecutando. Esto último se comprueba examinando la cadena de conexión pasada al método. Además, hace que el mecanismo de reintento sea más robusto y maneja otros detalles.

- Implementa una caché de resolutor DNS asíncrona. (Alexander Kukushkin)

  Evita fallos cuando el DNS no está disponible temporalmente (por ejemplo, debido a un tráfico excesivo recibido por el nodo).

- Implementa el estado de inicio y el tiempo de espera de inicio del master. (Ants Aasma, Alexander Kukushkin)

  Anteriormente, `pg_ctl` esperaba un tiempo de espera y luego continuaba alegremente considerando que PostgreSQL se estaba ejecutando. Esto hacía que PostgreSQL apareciera en los listados como en ejecución cuando en realidad no lo estaba y causaba una condición de carrera que daba como resultado una conmutación por error, o una recuperación ante fallos, o una recuperación ante fallos interrumpida por una conmutación por error y un rewind perdido. Este cambio añade un parámetro `master_start_timeout` e introduce un nuevo estado para el bucle principal de HA: `starting`. Cuando `master_start_timeout` es 0, haremos la conmutación por error inmediatamente cuando el master falle, tan pronto como haya un candidato. De lo contrario, Patroni esperará después de intentar iniciar PostgreSQL en el master durante la duración del tiempo de espera; cuando expire, hará la conmutación por error si es posible. Las solicitudes manuales de conmutación por error se atenderán durante el fallo del master incluso antes de que expire el tiempo de espera.

  Introduce el parámetro `timeout` en el endpoint de la API `restart` y en [patronictl](/es/patroni/patronictl#patronictl). Cuando está establecido y el reinicio tarda más que el tiempo de espera, PostgreSQL se considera no sano y los otros nodos pasan a ser elegibles para tomar el bloqueo de líder.

- Corrige el comportamiento de `pg_rewind` en modo de pausa. (Ants Aasma)

  Evita un reinicio innecesario en modo de pausa cuando Patroni cree que necesita hacer rewind pero el rewind no es posible (es decir, `pg_rewind` no está presente). Recurre a los valores predeterminados de `libpq` para el `superuser` (usuario del SO predeterminado) si falta la autenticación de `superuser` en la sección de configuración de Patroni relacionada con `pg_rewind`.

- Serializa la ejecución de los callbacks. Termina el callback anterior del mismo tipo cuando el nuevo esté a punto de ejecutarse. Corrige el problema de generar procesos zombis al ejecutar callbacks. (Alexander Kukushkin)

- Evita promover un antiguo master cuando la clave de líder está establecida en el DCS pero la actualización de esta clave de líder falla. (Alexander Kukushkin)

  Esto evita el problema de que un master actual continúe conservando su rol cuando está particionado junto con la minoría de nodos en Etcd y otros DCS que permiten «lecturas inconsistentes».

**Varios**

- Añade la opción de configuración `post_init` en el bootstrap. (Alejandro Martínez)

  Patroni llamará al argumento de script de esta opción justo después de ejecutar `initdb` e iniciar PostgreSQL para un clúster nuevo. El script recibe una URL de conexión con `superuser`. Cuando se proporciona una contraseña, Patroni establece `PGPASSFILE` para apuntar al archivo `.pgpass` que contiene la contraseña. Si el script falla, la inicialización de Patroni también falla. Es útil para añadir nuevos usuarios o crear extensiones en el clúster nuevo.

- Implementa el soporte de PostgreSQL 9.6. (Alexander Kukushkin)

  Usa `wal_level = replica` como sinónimo de `hot_standby`, evitando el indicador pending_restart cuando cambia de uno a otro. (Alexander Kukushkin)

**Mejoras en la documentación**

- Añade un [diagrama del flujo de trabajo del bucle principal](https://raw.githubusercontent.com/patroni/patroni/master/docs/ha_loop_diagram.png) de Patroni. (Alejandro Martínez, Alexander Kukushkin)

- Mejora el README, añadiendo el chart de Helm y enlaces a las notas de versión. (Lauri Apple)

- Traslada la documentación de Patroni a `Read the Docs`. La documentación actualizada está disponible en [https://patroni.readthedocs.io](https://patroni.readthedocs.io). (Oleksii Kliukin)

  Hace que la documentación sea fácilmente visible desde diferentes dispositivos (incluidos los teléfonos inteligentes) y que se pueda buscar.

- Pasa el paquete al versionamiento semántico. (Oleksii Kliukin)

  Patroni seguirá el esquema de versiones mayor.menor.parche para evitar publicar una nueva versión menor por correcciones de errores pequeñas pero críticas. Solo publicaremos las notas de versión de la versión menor, que incluirá todos los parches.

--------

## Versión 1.1 {#version-11}

Publicado el 2016-09-07

Esta versión mejora la gestión del clúster de Patroni al incorporar el modo de pausa, mejora el mantenimiento con reinicios programados y condicionales, hace más resistente la interacción de Patroni con Etcd o Zookeeper y mejora enormemente patronictl.

**Aviso de actualización**

Al actualizar desde versiones anteriores a 1.0, lee acerca del cambio de credenciales y formato de configuración en las notas de versión de la 1.0.

**Modo de pausa**

- Introduce el modo de pausa para separar temporalmente a Patroni de la gestión de la instancia de PostgreSQL (Murat Kabilov, Alexander Kukushkin, Oleksii Kliukin).

  Anteriormente, había que enviar la señal SIGKILL a Patroni para detenerlo sin terminar PostgreSQL. El nuevo modo de pausa separa a Patroni de PostgreSQL en todo el clúster sin terminar Patroni. Es similar al modo de mantenimiento de Pacemaker. Patroni sigue siendo responsable de actualizar las claves de miembro y de líder en el DCS, pero no iniciará, detendrá ni reiniciará el servidor de PostgreSQL en el proceso. Hay algunas excepciones; por ejemplo, las conmutaciones por error, reinicializaciones y reinicios manuales siguen permitidos. Puedes leer [una descripción detallada de esta función](/es/patroni/pause#pause).

Además, patronictl soporta los nuevos comandos [pause](/es/patroni/pause#pause) y `resume` para activar/desactivar el modo de pausa.

**Reinicios programados y condicionales**

- Añade condiciones al comando de la API restart (Oleksii Kliukin)

  Este cambio mejora los reinicios de Patroni añadiendo un par de condiciones que pueden verificarse para hacer el reinicio. Entre las condiciones están reiniciar cuando el rol de PostgreSQL es master o réplica, comprobar el número de versión de PostgreSQL o reiniciar solo cuando es necesario reiniciar para aplicar cambios de configuración.

- Añade reinicios programados (Oleksii Kliukin)

  Ahora es posible programar un reinicio en el futuro. Solo se soporta un reinicio programado por nodo. Es posible limpiar el reinicio programado si ya no es necesario. Se soporta una combinación de reinicios programados y condicionales, haciendo posible, por ejemplo, programar actualizaciones menores de PostgreSQL por la noche, reiniciando solo las instancias que ejecutan la versión menor desactualizada sin añadir lógica específica de postgres a los scripts de administración.

- Añade soporte para reinicios condicionales y programados a patronictl (Murat Kabilov).

  patronictl restart soporta varias opciones nuevas. También está el comando patronictl flush para limpiar las acciones programadas.

**Interacción robusta con el DCS**

- Establece los tiempos de espera de Kazoo en función del loop_wait (Alexander Kukushkin)

  Originalmente, los valores de ping_timeout y connect_timeout se calculaban a partir del tiempo de espera de sesión negociado. El loop_wait de Patroni no se tenía en cuenta. Como resultado, un solo reintento podía tardar más que el tiempo de espera de sesión, forzando a Patroni a liberar el bloqueo y degradarse.

  Este cambio establece el ping y el connect timeout a la mitad del valor de loop_wait, acelerando la detección de problemas de conexión y dejando tiempo suficiente para reintentar el intento de conexión antes de perder el bloqueo.

- Actualiza la topología de Etcd solo después de que la solicitud original tenga éxito (Alexander Kukushkin)

  Aplaza la actualización de la topología de Etcd conocida por el cliente hasta después de la solicitud original. Al recuperar la topología del clúster, implementa los tiempos de espera de reintento en función del número conocido de nodos en el clúster de Etcd. Esto hace que nuestro cliente prefiera obtener los resultados de la solicitud a tener la lista actualizada de nodos.

  Ambos cambios hacen que las conexiones de Patroni al DCS sean más robustas frente a problemas de red.

**Patronictl, monitoreo y configuración**

- Devuelve información sobre las réplicas en streaming mediante la API (Feike Steenbergen)

  Anteriormente, no había una forma fiable de consultar a Patroni sobre instancias de PostgreSQL que fallan al transmitir cambios (por ejemplo, debido a problemas de conexión). Este cambio expone el contenido de pg_stat_replication mediante el endpoint /patroni.

- Añade el comando patronictl scaffold (Oleksii Kliukin)

  Añade un comando para crear la estructura del clúster en Etcd. El clúster se crea con el sysid y el líder especificados por el usuario, y tanto las claves de líder como las de miembro se hacen persistentes. Este comando es útil para crear las llamadas configuraciones sin master (master-less), donde un clúster de Patroni que consta solo de réplicas replica desde el nodo master externo que no conoce Patroni. Posteriormente, se puede eliminar la clave de líder, promoviendo uno de los nodos de Patroni y reemplazando el master original por el clúster de HA basado en Patroni.

- Añade la opción de configuración `bin_dir` para localizar los binarios de PostgreSQL (Ants Aasma)

  Es útil poder especificar la ubicación de los binarios de PostgreSQL explícitamente en las distribuciones de Linux que soportan instalar varias versiones de PostgreSQL al mismo tiempo.

- Permite que la ruta del archivo de configuración se anule usando `custom_conf` (Alejandro Martínez)

  Permite rutas de archivo de configuración personalizadas, que no serán gestionadas por Patroni, [detalles](/es/patroni/config/yaml#postgresql_settings).

**Correcciones de errores y mejoras de código**

- Hace que Patroni sea compatible con el nuevo esquema de versiones de PostgreSQL 10 y posteriores (Feike Steenbergen)

  Garantiza que Patroni entienda los números de versión de 2 dígitos al hacer reinicios condicionales basados en la versión de PostgreSQL.

- Usa pkgutil para encontrar los módulos de DCS (Alexander Kukushkin)

  Usa el módulo dedicado de python en lugar de recorrer directorios manualmente para encontrar los módulos de DCS.

- Llama siempre al callback on_start al iniciar Patroni (Alexander Kukushkin)

  Anteriormente, Patroni no llamaba a ningún callback al adjuntarse al nodo ya en ejecución con el rol correcto. Dado que los callbacks suelen usarse para enrutar conexiones de cliente, eso podía dar como resultado el fallo al registrar el nodo en ejecución en el esquema de enrutamiento de conexiones. Con esta corrección, Patroni llama al callback on_start incluso cuando se adjunta al nodo ya en ejecución.

- No elimina los slots de replicación activos (Murat Kabilov, Oleksii Kliukin)

  Evita eliminar los slots de replicación físicos activos en el master. PostgreSQL no puede eliminar dichos slots de todos modos. Este cambio hace posible ejecutar réplicas/consumidores no gestionados por Patroni en el master.

- Cierra las conexiones de Patroni durante el inicio de la instancia de PostgreSQL (Alexander Kukushkin)

  Fuerza a Patroni a cerrar todas las conexiones anteriores cuando se inicia el nodo de PostgreSQL. Evita la trampa de reutilizar conexiones anteriores si el postmaster fue terminado con SIGKILL.

- Reemplaza los caracteres inválidos al construir nombres de slot a partir de nombres de miembros (Ants Aasma)

  Garantiza que los nombres de standby que no cumplen las reglas de nomenclatura de slots no provoquen el fallo de la creación del slot y del inicio del standby. Reemplaza los guiones en los nombres de slot por guiones bajos y todos los demás caracteres no permitidos en nombres de slot por sus puntos de código unicode.

--------

## Versión 1.0 {#version-10}

Publicado el 2016-07-05

Esta versión introduce la configuración dinámica global que permite cambios dinámicos de los parámetros de configuración de PostgreSQL y Patroni para todo el clúster de HA. También entrega numerosas correcciones de errores.

**Aviso de actualización**

Al actualizar desde v0.90 o anterior, actualiza siempre todas las réplicas antes que el master. Dado que ya no almacenamos las credenciales de replicación en el DCS, una réplica antigua no podrá conectarse al nuevo master.

**Configuración dinámica**

- Implementa la configuración dinámica global (Alexander Kukushkin)

  Introduce el nuevo endpoint /config de la REST API para proporcionar parámetros de configuración de PostgreSQL y Patroni que deben establecerse globalmente para todo el clúster de HA (el master y todas las réplicas). Dichos parámetros se establecen en el DCS y en muchos casos pueden aplicarse sin interrumpir PostgreSQL ni Patroni. Patroni establece un indicador especial llamado "pending restart" visible mediante la API cuando algunos de los valores requieren el reinicio de PostgreSQL. En ese caso, el reinicio debe emitirse manualmente mediante la API.

  Un SIGHUP a Patroni o un POST a /reload harán que vuelva a leer el archivo de configuración.

  Consulta la [configuración de Patroni](/es/patroni/config#config) para conocer los detalles sobre qué parámetros pueden cambiarse y el orden de procesamiento de las diferentes fuentes de configuración.

  El formato del archivo de configuración *ha cambiado* desde la v0.90. Patroni sigue siendo compatible con los archivos de configuración antiguos, pero para aprovechar los parámetros de bootstrap hay que cambiarlo. Se recomienda a los usuarios actualizarlos consultando la [página de documentación de la configuración dinámica](/es/patroni/config/dynamic#dynamic).

**Configuración más flexible**\*

- Hace configurables la configuración de postgresql y el nombre de la base de datos a la que se conecta Patroni (Misja Hoebe)

  Introduce los parámetros de configuración `database` y `config_base_name`. Entre otras cosas, hace posible ejecutar Patroni con PipelineDB y otros forks de PostgreSQL.

- Implementa la posibilidad de configurar algunos parámetros de configuración de Patroni mediante el entorno (Alexander Kukushkin)

  Estos incluyen el scope, el nombre del nodo y el espacio de nombres, así como los secretos, y facilita ejecutar Patroni en un entorno dinámico, p. ej. Kubernetes. Consulta las [variables de entorno soportadas](/es/patroni/config/env#env) para más detalles.

- Actualiza el contenedor docker integrado de Patroni para aprovechar la configuración basada en el entorno (Feike Steenbergen).

- Añade soporte de Zookeeper a la imagen docker de Patroni (Alexander Kukushkin)

- Divide las opciones de configuración de Zookeeper y Exhibitor (Alexander Kukushkin)

- Hace que patronictl reutilice el código de Patroni para leer la configuración (Alexander Kukushkin)

  Esto permite a patronictl aprovechar la configuración basada en el entorno.

- Establece el nombre de aplicación al nombre del nodo en primary_conninfo (Alexander Kukushkin)

  Esto simplifica la identificación y configuración de la replicación síncrona para un nodo dado.

**Mejoras de estabilidad, seguridad y usabilidad**

- Restablece el sysid y no llama a pg_controldata cuando hay una restauración de copia de seguridad en progreso (Alexander Kukushkin)

  Este cambio reduce la cantidad de ruido generado por las comprobaciones de estado de la API de Patroni durante la prolongada inicialización de este nodo desde la copia de seguridad.

- Corrige un montón de casos extremos de pg_rewind (Alexander Kukushkin)

  Evita ejecutar pg_rewind si el clúster de origen no es el master.

  Además, evita eliminar el directorio de datos tras un rewind fallido, a menos que el nuevo parámetro *remove_data_directory_on_rewind_failure* esté establecido en true. Por defecto es false.

- Elimina las contraseñas de la cadena de conexión de replicación en el DCS (Alexander Kukushkin)

  Anteriormente, Patroni usaba siempre las credenciales de replicación de la URL de Postgres en el DCS. Esto ahora cambia para tomar las credenciales de la configuración de patroni. Los secretos (usuario y contraseña de replicación) ya no quedan expuestos en el DCS.

- Corrige la maquinaria asíncrona en torno a la llamada de degradación (Alexander Kukushkin)

  La degradación ahora se ejecuta totalmente de forma asíncrona sin bloquear las interacciones con el DCS.

- Hace que patronictl envíe siempre el encabezado de autorización si está configurado (Alexander Kukushkin)

  Esto permite a patronictl emitir solicitudes «protegidas», es decir, restart o reinitialize, cuando Patroni está configurado para requerir autorización en ellas.

- Maneja correctamente la excepción SystemExit (Alexander Kukushkin)

  Evita los problemas de que Patroni no se detenga correctamente al recibir el SIGTERM

- Plantillas de ejemplo de haproxy para confd (Alexander Kukushkin)

  Genera y cambia dinámicamente la configuración de haproxy a partir del estado de patroni en el DCS usando confd

- Mejora y reestructura la documentación para hacerla más amigable para los nuevos usuarios (Lauri Apple)

- La API debe reportar role=master durante pg_ctl stop (Alexander Kukushkin)

  Hace que las llamadas a los callbacks sean más fiables, particularmente en el caso de la detención del clúster. Además, introduce la opción `pg_ctl_timeout` para establecer el tiempo de espera de las llamadas de inicio, detención y reinicio mediante `pg_ctl`.

- Corrige la lógica de reintento en etcd (Alexander Kukushkin)

  Hace que los reintentos sean más predecibles y robustos.

- Hace que el código de Zookeeper sea más resistente a pequeños fallos de red (Alexander Kukushkin)

  Reduce los tiempos de espera de conexión para que los intentos de conexión a Zookeeper sean más frecuentes.

--------

## Versión 0.90 {#version-090}

Publicado el 2016-04-27

Esta versión añade soporte de Consul, incluye la nueva etiqueta *noloadbalance*, cambia el comportamiento de la etiqueta *clonefrom*, mejora el manejo de *pg_rewind* y mejora el programa de control *patronictl*.

**Soporte de Consul**

- Implementa el soporte de Consul (Alexander Kukushkin)

  Patroni se ejecuta contra Consul, además de Etcd y Zookeeper. Los parámetros de conexión pueden configurarse en el archivo YAML.

**Etiquetas nuevas y mejoradas**

- Implementa la etiqueta *noloadbalance* (Alexander Kukushkin)

  Esta etiqueta hace que Patroni devuelva siempre que la réplica no está disponible para el balanceador de carga.

- Cambia la implementación de la etiqueta *clonefrom* (Alexander Kukushkin)

  Anteriormente, había que suministrar un nombre de nodo al *clonefrom*, forzando a una réplica etiquetada a clonar desde el nodo específico. La nueva implementación convierte *clonefrom* en una etiqueta booleana: si está establecida en true, la réplica pasa a ser candidata para que otras réplicas clonen de ella. Cuando hay múltiples candidatos, las réplicas eligen uno al azar.

**Mejoras de estabilidad y seguridad**

- Numerosas mejoras de fiabilidad (Alexander Kukushkin)

  Elimina algunos mensajes de error espurios, mejora la estabilidad de la conmutación por error y aborda algunos casos extremos con la lectura de datos del DCS, el apagado, la degradación y la readjunción del antiguo líder.

- Mejora el script de sistema para evitar matar los hijos de Patroni al detenerse (Jan Keirse, Alexander Kukushkin)

  Anteriormente, al detener Patroni, *systemd* también enviaba una señal a PostgreSQL. Dado que Patroni también intentaba detener PostgreSQL por sí mismo, esto daba como resultado el envío de dos solicitudes de apagado diferentes (el smart shutdown, seguido del fast shutdown). Eso provocaba que las réplicas se desconectaran demasiado pronto y que un antiguo master no pudiera reincorporarse tras la degradación. Corrección de Jan con investigación previa de Alexander.

- Elimina algunos casos en los que el antiguo master no podía llamar a pg_rewind antes de reincorporarse como réplica (Oleksii Kliukin)

  Anteriormente, solo llamábamos a *pg_rewind* si el antiguo master había fallado. Esto se cambia para ejecutar siempre pg_rewind en el antiguo master mientras pg_rewind esté presente en el sistema. Esto corrige el caso en que el master se apaga antes de que las réplicas logren obtener los últimos cambios (es decir, durante el apagado "smart").

- Numerosas mejoras a las pruebas unitarias y de aceptación; en particular, habilita el soporte de Zookeeper y Consul (Alexander Kukushkin).

- Hace que Travis CI sea más rápido e implementa soporte para ejecutar pruebas contra Zookeeper (Exhibitor) y Consul (Alexander Kukushkin)

  Tanto las pruebas unitarias como las de aceptación se ejecutan automáticamente contra Etcd, Zookeeper y Consul en cada commit o pull-request.

- Limpia las variables de entorno antes de llamar a comandos de PostgreSQL desde Patroni (Feike Steenbergen)

  Esto evita la posibilidad de leer variables de entorno del sistema conectándose al clúster de PostgreSQL gestionado por Patroni.

**Cambios de configuración y control**

- Unifica la configuración de patronictl y Patroni (Feike Steenbergen)

  patronictl puede usar el mismo archivo de configuración que el propio Patroni.

- Habilita a Patroni para leer la configuración desde las variables de entorno (Oleksii Kliukin)

  Esto simplifica la generación automática de la configuración de Patroni, o la fusión de una única configuración a partir de diferentes fuentes.

- Incluye el identificador de sistema de la base de datos en la información devuelta por la API (Feike Steenbergen)

- Implementa *delete_cluster* para todos los DCS disponibles (Alexander Kukushkin)

  Habilita el soporte de DCS distintos de Etcd en patronictl.

--------

## Versión 0.80 {#version-080}

Publicado el 2016-03-14

Esta versión añade soporte de *replicación en cascada* y simplifica la gestión de Patroni mediante *conmutaciones por error programadas*. Pueden usarse versiones antiguas de Patroni (en particular, la 0.78) combinadas con esta para migrar a la nueva versión. Ten en cuenta que la conmutación por error programada y las funciones relacionadas con la replicación en cascada solo funcionarán con Patroni 0.80 y posteriores.

**Replicación en cascada**

> - Añade soporte de las etiquetas *replicatefrom* y *clonefrom* para el nodo de patroni (Oleksii Kliukin).
>
> La etiqueta *replicatefrom* permite que una réplica use un nodo arbitrario como fuente, no necesariamente el master. La *clonefrom* hace lo mismo para la copia de seguridad inicial. Juntas, permiten que Patroni soporte por completo la replicación en cascada.

- Añade soporte para ejecutar métodos de replicación para inicializar la réplica incluso sin una conexión de replicación en ejecución (Oleksii Kliukin).

> Esto es útil para crear réplicas a partir de instantáneas almacenadas en S3 o FTP. Un método de replicación que no requiere una conexión de replicación en ejecución debe suministrar *no_master: true* en la configuración yaml. Dichos scripts seguirán llamándose en orden si la conexión de replicación está presente.

**Mejoras en patronictl, API y DCS**

- Implementa conmutaciones por error programadas (Feike Steenbergen).

  Las conmutaciones por error pueden programarse para ocurrir en un momento futuro determinado, usando tanto patronictl como llamadas a la API.

- Añade soporte para los parámetros *dbuser* y *password* en patronictl (Feike Steenbergen).

- Añade la versión de PostgreSQL a la salida de la comprobación de estado (Feike Steenbergen).

- Mejora el soporte de Zookeeper en patronictl (Oleksandr Shulgin)

- Migra a python-etcd 0.4.3 (Alexander Kukushkin)

**Configuración**

- Añade un script de configuración de sistema de ejemplo para Patroni (Jan Keirse).
- Corrige el problema de que Patroni ignoraba el nombre de superusuario especificado en el archivo de configuración para las conexiones a la BD (Alexander Kukushkin).
- Corrige el manejo de CTRL-C creando un ID de sesión y un grupo de procesos separados para el postmaster lanzado por Patroni (Alexander Kukushkin).

**Pruebas**

- Añade pruebas de aceptación con *behave* para comprobar escenarios reales de ejecución de Patroni (Alexander Kukushkin, Oleksii Kliukin).

  Las pruebas pueden lanzarse manualmente usando el comando *behave*. También se lanzan automáticamente para los pull requests y después de los commits.

  Las notas de versión de algunas versiones más antiguas pueden encontrarse en la [página de github del proyecto](https://github.com/patroni/patroni/releases).
