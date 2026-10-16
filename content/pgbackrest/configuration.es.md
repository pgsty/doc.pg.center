---
title: "Referencia de configuración"
linkTitle: "Configuración"
weight: 50
description: "Referencia completa de configuración de pgBackRest para todos los ajustes, incluidas las opciones de archivado, copia de seguridad, repositorio y almacenamiento en la nube."
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/configuration.html"
---

--------

## Introducción {#introduction}

pgBackRest puede usarse por completo con parámetros de línea de comandos, pero un archivo de configuración es más práctico para instalaciones complejas o que establecen muchas opciones. La ubicación predeterminada del archivo de configuración es `/etc/pgbackrest/pgbackrest.conf`. Si no existe ningún archivo en esa ubicación, se comprobará el antiguo predeterminado `/etc/pgbackrest.conf`.

Se usan los siguientes tipos de opción:

**Cadena**: Una cadena de texto, comúnmente un identificador, una contraseña, etc.

Ejemplo en línea de comandos: `--stanza=demo`<br/>Ejemplo en archivo de configuración: `repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**Ruta**: Se usa para identificar de forma única una ubicación en una estructura de directorios. Las rutas deben comenzar con /, no se permite el doble // y no se espera una / al final.

Ejemplo en línea de comandos: `--repo1-path=/var/lib/pgbackrest`<br/>Ejemplo en archivo de configuración: `repo1-path=/var/lib/pgbackrest`

**Booleano**: Activa o desactiva la opción. Solo y/n son valores de argumento válidos.

Ejemplos en línea de comandos: `--start-fast`, `--no-start-fast`, `--start-fast=y`, `--start-fast=n`<br/>Ejemplos en archivo de configuración: `start-fast=y`, `start-fast=n`

**Entero**: Se usa para puertos, recuentos de retención/reintento, procesos en paralelo permitidos, etc.

Ejemplo en línea de comandos: `--compress-level=3`<br/>Ejemplo en archivo de configuración: `pg1-port=5432`

**Tamaño**: Se usa para tamaños de búfer, uso de disco, etc. El tamaño puede especificarse en bytes (predeterminado) o en KiB, MiB, GiB, TiB o PiB, donde el multiplicador es una potencia de 1024. Por ejemplo, el valor insensible a mayúsculas/minúsculas 5GiB (o 5GB, 5g) puede usarse en lugar de 5368709120. No se permiten valores fraccionarios como 2.5GiB; usa 2560MiB en su lugar.

Ejemplo en línea de comandos: `--archive-get-queue-max=1GiB`<br/>Ejemplo en archivo de configuración: `buffer-size=2MiB`

**Tiempo**: Tiempo en segundos.

Ejemplo en línea de comandos: `--io-timeout=90`<br/>Ejemplo en archivo de configuración: `db-timeout=600`

**Lista**: La opción puede proporcionarse varias veces.

Ejemplo en línea de comandos: `--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`

Ejemplo en archivo de configuración, cada uno en su propia línea:

```ini
db-exclude=db1
db-exclude=db2
db-exclude=db5
```

**Clave/Valor**: La opción puede proporcionarse varias veces en la forma `key=value`.

Ejemplo en línea de comandos: `--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`

Ejemplo en archivo de configuración, cada uno en su propia línea:

```ini
tablespace-map=ts_01=/db/ts_01
tablespace-map=ts_02=/db/ts_02
```

--------

## Opciones de archivado {#archive-options}

La sección `archive` define opciones para los comandos `archive-push` y `archive-get`.

### Opción de archivado asíncrono (`--archive-async`) {#asynchronous-archiving-option---archive-async}

Envía/obtiene segmentos WAL de forma asíncrona.

Activa la operación asíncrona para los comandos `archive-push` y `archive-get`.

La operación asíncrona es más eficiente porque puede reutilizar conexiones y aprovechar el paralelismo. Consulta las opciones `spool-path`, `archive-get-queue-max` y `archive-push-queue-max` para obtener más información.

```text
default: n
example: archive-async=y
```

### Opción de tamaño máximo de la cola de archive-get (`--archive-get-queue-max`) {#maximum-archive-get-queue-size-option---archive-get-queue-max}

Tamaño máximo de la cola de archive-get de pgBackRest.

Especifica el tamaño máximo de la cola de `archive-get` cuando `archive-async` está activado. La cola se almacena en el `spool-path` y se utiliza para acelerar el suministro de WAL a PostgreSQL.

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### Opción de reintento de segmento WAL faltante (`--archive-missing-retry`) {#retry-missing-wal-segment-option---archive-missing-retry}

Reintentar segmento WAL faltante

Reintenta un segmento WAL que el comando `archive-get` reportó previamente como faltante cuando está en modo asíncrono. Esto evita que se utilicen notificaciones en la ruta de spool de una restauración anterior y que posiblemente provoquen un fallo de recuperación si no se ha alcanzado la consistencia.

Al desactivar esta opción, PostgreSQL puede reconocer con mayor fiabilidad cuándo se ha alcanzado el final del WAL en el archivado, lo que le permite conmutar a la replicación por streaming desde el primario. Con los reintentos activados, un flujo constante de WAL archivándose hará que PostgreSQL siga obteniendo WAL del archivado en lugar de conmutar al streaming.

Al desactivar esta opción es importante asegurarse de que la ruta de spool del stanza esté vacía. El comando `restore` lo hace automáticamente si la ruta de spool está configurada en el momento de la restauración. De lo contrario, es responsabilidad del usuario asegurarse de que la ruta de spool esté vacía.

```text
default: y
example: archive-missing-retry=n
```

### Opción de tamaño de lote de archive-push (`--archive-push-batch-size`) {#archive-push-batch-size-option---archive-push-batch-size}

Cantidad máxima de WAL a enviar por ejecución asíncrona.

En modo asíncrono, el proceso `archive-push` envía todos los segmentos WAL que estén listos en una sola ejecución. Dado que `archive-push-queue-max` solo se comprueba al inicio de cada ejecución, una ejecución que procesa un número muy grande de segmentos puede permitir que la cola crezca bien más allá del límite antes de que se vuelva a comprobar.

Esta opción limita la cantidad de WAL procesada por ejecución, de modo que el proceso termina y vuelve a ser lanzado por el siguiente `archive-push`, que recomprueba la cola. Los valores más bajos recomprueban la cola más a menudo a costa de lanzar el proceso asíncrono con más frecuencia. El valor se redondea hacia abajo a un número entero de segmentos WAL, pero siempre se procesa al menos un segmento.

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### Opción de tamaño máximo de la cola de archive-push (`--archive-push-queue-max`) {#maximum-archive-push-queue-size-option---archive-push-queue-max}

Tamaño máximo de la cola de archivado de PostgreSQL.

Una vez alcanzado el límite, ocurrirá lo siguiente:

- pgBackRest notificará a PostgreSQL que el WAL se archivó correctamente y luego **LO DESCARTARÁ**.
- Se emitirá una advertencia en el registro de PostgreSQL.

Si esto ocurre, el flujo del registro de archivado se interrumpirá y PITR no será posible más allá de ese punto. Será necesaria una nueva copia de seguridad para recuperar la capacidad completa de restauración.

En modo asíncrono, toda la cola se descartará para evitar que ráfagas de WAL pasen antes de que el límite de la cola se exceda de nuevo.

En modo asíncrono este límite solo se comprueba al inicio de cada ejecución de `archive-push`, por lo que la cola puede crecer más allá de él dentro de una sola ejecución. Reduce `archive-push-batch-size` para comprobar la cola con más frecuencia.

El propósito de esta función es evitar que el volumen de registros se llene, punto en el cual PostgreSQL se detendría por completo. Es mejor perder la copia de seguridad que hacer caer PostgreSQL.

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

Nombre obsoleto: archive-queue-max

### Opción de tiempo de espera de archivado (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

Tiempo de espera de archivado.

Establece el tiempo máximo, en segundos, de espera para que cada segmento WAL llegue al repositorio de archivado de pgBackRest. El tiempo de espera se aplica a los comandos `check` y `backup` mientras esperan que se archiven los segmentos WAL requeridos para la consistencia de la copia de seguridad.

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## Opciones de copia de seguridad {#backup-options}

La sección `backup` define ajustes relacionados con la copia de seguridad.

### Opción de anotación de copia de seguridad (`--annotation`) {#backup-annotation-option---annotation}

Anota la copia de seguridad con pares clave/valor definidos por el usuario.

Los usuarios pueden adjuntar pares clave/valor informativos a la copia de seguridad. Esta opción puede usarse varias veces para adjuntar múltiples anotaciones.

Las anotaciones se muestran en la salida de texto del comando `info` cuando se especifica una copia de seguridad con `--set` y siempre aparecen en la salida JSON.

```text
example: annotation=source="Sunday backup for website database"
```

### Opción de comprobación de archivado (`--archive-check`) {#check-archive-option---archive-check}

Comprueba que los segmentos WAL estén en el archivado antes de que se complete la copia de seguridad.

Comprueba que todos los segmentos WAL necesarios para que la copia de seguridad sea consistente estén presentes en el archivado de WAL. Es buena idea dejar el valor predeterminado a menos que uses otro método de archivado.

Esta opción debe estar activada si `archive-copy` está activado.

```text
default: y
example: archive-check=n
```

### Opción de copia de archivado (`--archive-copy`) {#copy-archive-option---archive-copy}

Copia en la copia de seguridad los segmentos WAL necesarios para la consistencia.

Esta opción, ligeramente paranoica, protege contra la corrupción en el archivado de segmentos WAL almacenando los segmentos WAL necesarios para la consistencia directamente en la copia de seguridad. Los segmentos WAL se siguen almacenando en el archivado, por lo que esta opción utilizará espacio adicional.

Es preferible que los comandos `archive-push` y `backup` tengan el mismo `compress-type` (p. ej., `lz4`) al usar esta opción. De lo contrario, los segmentos WAL tendrán que recomprimirse con el `compress-type` utilizado por la copia de seguridad, lo que puede ser bastante costoso dependiendo de cuánto WAL se haya generado durante la copia de seguridad.

Al restaurar, los segmentos WAL estarán presentes en `pg_xlog/pg_wal` y PostgreSQL los usará con preferencia a llamar al `restore_command`.

La opción `archive-check` debe estar activada si `archive-copy` está activado.

```text
default: n
example: archive-copy=y
```

### Opción de comprobación del modo de archivado (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

Comprueba el ajuste `archive_mode` de PostgreSQL.

Activada por defecto, esta opción no permite `archive_mode=always` en PostgreSQL.

Los segmentos WAL enviados desde un servidor standby podrían ser lógicamente iguales a los segmentos WAL enviados desde el primario pero tener sumas de comprobación diferentes. Se recomienda desactivar el archivado desde múltiples fuentes para evitar conflictos.

PRECAUCIÓN:

Si esta opción se desactiva, es crítico asegurarse de que solo un archivador esté escribiendo en el repositorio a través del comando `archive-push`.

```text
default: y
example: archive-mode-check=n
```

### Opción de copia de seguridad desde el standby (`--backup-standby`) {#backup-from-standby-option---backup-standby}

Copia de seguridad desde el clúster standby.

Activa la copia de seguridad desde el standby para reducir la carga en el clúster primario. Esta opción requiere que estén configurados tanto el host primario como el standby.

Se soportan los siguientes modos:

- `y` - El standby es obligatorio para la copia de seguridad.
- `prefer` - Copia de seguridad desde el standby si está disponible; de lo contrario, desde el primario.
- `n` - Copia de seguridad solo desde el primario.

```text
default: n
example: backup-standby=y
```

### Opción de sumas de comprobación de páginas (`--checksum-page`) {#page-checksums-option---checksum-page}

Valida las sumas de comprobación de las páginas de datos.

Indica a pgBackRest que valide todas las sumas de comprobación de las páginas de datos mientras se hace la copia de seguridad de un clúster. Esta opción se activa automáticamente cuando las sumas de comprobación de páginas de datos están activadas en el clúster.

Los fallos en la validación de sumas de comprobación no abortarán una copia de seguridad. Más bien, se emitirán advertencias en el registro (y en la consola con los ajustes predeterminados) y la lista de páginas no válidas se almacenará en el manifiesto de la copia de seguridad.

```text
example: checksum-page=n
```

### Opción de exclusión de rutas/archivos (`--exclude`) {#pathfile-exclusions-option---exclude}

Excluye rutas/archivos de la copia de seguridad.

Todas las exclusiones son relativas a `$PGDATA`. Si la exclusión termina con /, solo se excluirán los archivos del directorio especificado; p. ej., `--exclude=junk/` excluirá todos los archivos del directorio `$PGDATA/junk` pero incluirá el directorio en sí. Si la exclusión no termina con /, el archivo puede coincidir exactamente con la exclusión o coincidir añadiendo / a la exclusión; p. ej., `--exclude=junk` excluirá el directorio `$PGDATA/junk` y todos los archivos que contiene.

**Ten cuidado al usar esta función: es muy fácil excluir algo crítico que dejará la copia de seguridad inconsistente. ¡Asegúrate de probar tus restauraciones!**

Todos los archivos excluidos se registrarán en el nivel `info` junto con la regla de exclusión. Asegúrate de auditar la lista de archivos excluidos para comprobar que no se está excluyendo nada inesperado.

NOTA:

Las exclusiones no se respetan en las restauraciones delta. Cualquier archivo/directorio que haya sido excluido por la copia de seguridad será *eliminado* en la restauración delta.

Esta opción no debe usarse para excluir los registros de PostgreSQL de una copia de seguridad. Los registros pueden moverse fuera del directorio `PGDATA` usando el ajuste `log_directory` de PostgreSQL, lo que tiene el beneficio de permitir que los registros se conserven después de una restauración.

Pueden especificarse múltiples exclusiones en la línea de comandos o en un archivo de configuración.

```text
example: exclude=junk/
```

### Opción de expiración automática (`--expire-auto`) {#expire-auto-option---expire-auto}

Ejecuta automáticamente el comando `expire` después de una copia de seguridad exitosa.

El ajuste está activado por defecto. Ten cautela al desactivar esta opción, ya que hacerlo resultará en conservar todas las copias de seguridad y archivados indefinidamente, lo que podría hacer que tu repositorio se quede sin espacio. El comando `expire` tendrá que ejecutarse regularmente para evitar que esto ocurra.

Cuando `expire` se ejecuta automáticamente después de una copia de seguridad exitosa, usa la configuración del comando `backup`, por lo que las opciones establecidas solo en una sección de comando `expire` (p. ej., `[global:expire]`) no se aplican. Para aplicar configuración específica de `expire`, desactiva esta opción y ejecuta el comando `expire` por separado.

```text
default: y
example: expire-auto=y
```

### Opción de umbral de guardado del manifiesto (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

Umbral de guardado del manifiesto durante la copia de seguridad.

Define con qué frecuencia se guardará el manifiesto durante una copia de seguridad. Guardar el manifiesto es importante porque almacena las sumas de comprobación y permite que la función de reanudación funcione de manera eficiente. El umbral real utilizado es el 1% del tamaño de la copia de seguridad o `manifest-save-threshold`, el que sea mayor.

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### Opción de reanudación (`--resume`) {#resume-option---resume}

Permite reanudar una copia de seguridad fallida.

Define si la función de reanudación está activada. La reanudación puede reducir enormemente el tiempo necesario para ejecutar una copia de seguridad después de que una copia de seguridad anterior del mismo tipo haya fallado. Sin embargo, añade complejidad, por lo que puede ser conveniente desactivarla en entornos que no requieren la función.

```text
default: y
example: resume=n
```

### Opción de inicio rápido (`--start-fast`) {#start-fast-option---start-fast}

Fuerza un checkpoint para iniciar la copia de seguridad rápidamente.

Fuerza un checkpoint (pasando `y` al parámetro `fast` de la función de inicio de la copia de seguridad) para que la copia de seguridad comience de inmediato. De lo contrario, la copia de seguridad comenzará después del siguiente checkpoint regular.

```text
default: n
example: start-fast=y
```

--------

## Opciones generales {#general-options}

La sección `general` define opciones que son comunes a muchos comandos.

### Opción permitir ejecutar como root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Permite que el comando se ejecute como el usuario root.

Por defecto, solo el comando `restore` puede ejecutarse como usuario root, ya que está diseñado para gestionar cuidadosamente la propiedad de los archivos. Ejecutar otros comandos como root corre el riesgo de crear archivos (p. ej., en el repositorio) cuya propiedad es de root y que, por lo tanto, resultan inaccesibles para el usuario de PostgreSQL, lo que provoca que comandos posteriores fallen.

Activa esta opción para ejecutar un comando como root de todos modos. Sin embargo, es mucho mejor ejecutar pgBackRest como el usuario propietario del repositorio y del clúster de PostgreSQL.

```text
default: n
example: allow-root=y
```

### Opción de tamaño de búfer (`--buffer-size`) {#buffer-size-option---buffer-size}

Tamaño de búfer para operaciones de E/S.

Tamaño de búfer utilizado para copiar, comprimir, cifrar y otras operaciones. El número de búferes utilizados depende de las opciones y cada operación puede usar memoria adicional, p. ej., la compresión `gz` puede usar 256KiB de memoria adicional.

Los valores permitidos son `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` y `16MiB`.

```text
default: 1MiB
example: buffer-size=2MiB
```

### Opción de comando pgBackRest (`--cmd`) {#pgbackrest-command-option---cmd}

Comando de pgBackRest.

pgBackRest puede generar una cadena de comando, p. ej., cuando el comando `restore` genera el ajuste restore_command. En este caso se usará el comando utilizado para ejecutar el proceso de pgBackRest, a menos que se proporcione la opción `cmd`.

PRECAUCIÓN:

Envolver el comando de pgBackRest puede causar un comportamiento impredecible y no se recomienda.

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### Opción de comando de cliente SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Comando de cliente SSH.

Usa un comando de cliente SSH específico cuando se desee uno alternativo o el comando `ssh` no esté en $PATH.

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### Opción de compresión (`--compress`) {#compress-option---compress}

Usa compresión de archivos.

Los archivos de la copia de seguridad son compatibles con las herramientas de compresión de línea de comandos.

Esta opción está ahora obsoleta. Debe usarse en su lugar la opción `compress-type`.

```text
default: y
example: compress=n
```

### Opción de nivel de compresión (`--compress-level`) {#compress-level-option---compress-level}

Nivel de compresión de archivos.

Establece el nivel que se usará para la compresión de archivos cuando `compress-type` no sea igual a `none` o `compress=y` (obsoleto).

```text
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: compress-level=9
```

### Opción de nivel de compresión de red (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Nivel de compresión de red.

Establece el nivel de compresión de red cuando `compress-type=none` y el comando no se ejecuta en el mismo host que el repositorio. La compresión se usa para reducir el tráfico de red. Cuando `compress-type` no es igual a `none`, el ajuste `compress-level-network` se ignora y se usa `compress-level` en su lugar, de modo que el archivo solo se comprima una vez.

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### Opción de tipo de compresión (`--compress-type`) {#compress-type-option---compress-type}

Tipo de compresión de archivos.

Se soportan los siguientes tipos de compresión:

- `none` - sin compresión
- `bz2` - formato de compresión bzip2
- `gz` - formato de compresión gzip
- `lz4` - formato de compresión lz4 (no disponible en todas las plataformas)
- `zst` - formato de compresión Zstandard (no disponible en todas las plataformas)

```text
default: gz
example: compress-type=none
```

### Opción de tiempo de espera de la base de datos (`--db-timeout`) {#database-timeout-option---db-timeout}

Tiempo de espera de consultas a la base de datos.

Establece el tiempo de espera, en segundos, para las consultas a la base de datos. Esto incluye las funciones de inicio/parada de la copia de seguridad, cada una de las cuales puede tardar un tiempo considerable. Por ello, el tiempo de espera debe mantenerse alto a menos que sepas que estas funciones retornarán rápidamente (es decir, si has establecido `start-fast=y` y sabes que el clúster de bases de datos no generará muchos segmentos WAL durante la copia de seguridad).

NOTA:

La opción `db-timeout` debe ser menor que la opción `protocol-timeout`.

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### Opción delta (`--delta`) {#delta-option---delta}

Restaura o hace copia de seguridad usando sumas de comprobación.

Durante una restauración, por defecto, se espera que los directorios de datos y de tablespaces de PostgreSQL estén presentes pero vacíos. Esta opción realiza una restauración delta usando sumas de comprobación.

Durante una copia de seguridad, esta opción usará las sumas de comprobación en lugar de las marcas de tiempo para determinar si se copiarán los archivos.

```text
default: n
example: delta=y
```

### Opción de tiempo de espera de E/S (`--io-timeout`) {#io-timeout-option---io-timeout}

Tiempo de espera de E/S.

Tiempo de espera, en segundos, utilizado para las conexiones y las operaciones de lectura/escritura.

Ten en cuenta que la operación completa de lectura/escritura no necesita terminar dentro de este tiempo de espera, pero debe haber *algún* progreso, aunque sea un solo byte.

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### Opción de ruta de bloqueo (`--lock-path`) {#lock-path-option---lock-path}

Ruta donde se almacenan los archivos de bloqueo.

La ruta de bloqueo proporciona una ubicación para que pgBackRest cree archivos de bloqueo que eviten que se ejecuten concurrentemente operaciones en conflicto.

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### Opción de umask neutro (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Usa un umask neutro.

Establece el umask en 0000 para que los modos en el repositorio se creen de manera sensata. El modo de directorio predeterminado es 0750 y el modo de archivo predeterminado es 0640.

Para usar en su lugar el umask del usuario que ejecuta, especifica `neutral-umask=n` en el archivo de configuración o `--no-neutral-umask` en la línea de comandos.

```text
default: y
example: neutral-umask=n
```

### Opción de establecimiento de prioridad del proceso (`--priority`) {#set-process-priority-option---priority}

Establece la prioridad del proceso.

Define cuánta prioridad (es decir, cuánta «niceness») otorgará el planificador del kernel al proceso. Los valores positivos disminuyen la prioridad y los valores negativos la aumentan. En la mayoría de los casos, los procesos no tienen permiso para aumentar su prioridad.

```text
allowed: [-20, 19]
example: priority=19
```

### Opción de máximo de procesos (`--process-max`) {#process-maximum-option---process-max}

Procesos máximos a usar para comprimir/transferir.

Cada proceso realizará compresión y transferencia para que el comando se ejecute más rápido, pero no establezcas `process-max` tan alto que afecte al rendimiento de la base de datos.

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### Opción de tiempo de espera de protocolo (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Tiempo de espera de protocolo.

Establece el tiempo de espera, en segundos, que el proceso local o remoto esperará a que se reciba un nuevo mensaje en la capa de protocolo. Esto evita que los procesos esperen indefinidamente un mensaje.

NOTA:

La opción `protocol-timeout` debe ser mayor que la opción `db-timeout`.

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### Opción keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Activación de keep-alive.

Activa los mensajes keep-alive en las conexiones de socket.

```text
default: y
example: sck-keep-alive=n
```

### Opción de ruta de spool (`--spool-path`) {#spool-path-option---spool-path}

Ruta donde se almacenan los datos transitorios.

Esta ruta se usa para almacenar datos de los comandos asíncronos `archive-push` y `archive-get`.

El comando asíncrono `archive-push` escribe reconocimientos en la ruta de spool cuando ha almacenado WAL correctamente en el archivado (y errores en caso de fallo), de modo que el proceso en primer plano puede notificar rápidamente a PostgreSQL. Los archivos de reconocimiento son muy pequeños (cero bytes en caso de éxito y unos pocos cientos de bytes en caso de error).

El comando asíncrono `archive-get` pone en cola el WAL en la ruta de spool para poder suministrarlo muy rápidamente cuando PostgreSQL lo solicite. Mover archivos a PostgreSQL es más eficiente cuando la ruta de spool está en el mismo sistema de archivos que `pg_xlog`/`pg_wal`. Sin embargo, no se recomienda colocar la ruta de spool *dentro* del directorio `pg_xlog`/`pg_wal`, ya que esto puede causar problemas a las utilidades de PostgreSQL como `pg_rewind`.

Los datos almacenados en la ruta de spool no son estrictamente temporales, ya que pueden y deben sobrevivir a un reinicio. Sin embargo, la pérdida de los datos de la ruta de spool no es un problema. pgBackRest simplemente volverá a comprobar cada segmento WAL para asegurarse de que está archivado de forma segura para `archive-push` y reconstruirá la cola para `archive-get`.

La ruta de spool está pensada para estar ubicada en un sistema de archivos local compatible con Posix, no en un sistema de archivos remoto como NFS o CIFS.

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### Opción de recuento keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Recuento de keep-alive.

Especifica el número de mensajes keep-alive de TCP que pueden perderse antes de que la conexión se considere muerta.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPCNT`.

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### Opción de tiempo de inactividad de keep-alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Tiempo de inactividad de keep-alive.

Especifica la cantidad de tiempo (en segundos) sin actividad de red tras la cual el sistema operativo debería enviar un mensaje keep-alive de TCP.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPIDLE`.

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### Opción de intervalo de keep-alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Intervalo de tiempo de keep-alive.

Especifica la cantidad de tiempo (en segundos) tras la cual debería retransmitirse un mensaje keep-alive de TCP que no haya sido reconocido.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPINTVL`.

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### Opción de conjuntos de cifrado TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Conjuntos de cifrado TLSv1.2 permitidos.

Todas las conexiones TLS entre el cliente y el servidor de pgBackRest están cifradas. Por defecto, las conexiones a los almacenes de objetos (p. ej., S3) también están cifradas.

NOTA:

El nivel de seguridad mínimo absoluto para cualquier conexión de transporte es TLSv1.2.

Los conjuntos de cifrado aceptados pueden ajustarse si surge la necesidad. El ejemplo es una elección razonable a menos que tengas requisitos de seguridad específicos. Si no se establece (el predeterminado), se aplica el predeterminado de la librería OpenSSL subyacente.

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Opción de conjuntos de cifrado TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Conjuntos de cifrado TLSv1.3 permitidos.

Todas las conexiones TLS entre el cliente y el servidor de pgBackRest están cifradas. Por defecto, las conexiones a los almacenes de objetos (p. ej., S3) también están cifradas.

NOTA:

El nivel de seguridad mínimo absoluto para cualquier conexión de transporte es TLSv1.2.

Los conjuntos de cifrado aceptados pueden ajustarse si surge la necesidad. Si no se establece (el predeterminado), se aplica el predeterminado de la librería OpenSSL subyacente.

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## Opciones de registro {#log-options}

La sección `log` define ajustes relacionados con el registro.

PRECAUCIÓN:

El registro a nivel trace puede exponer secretos como claves y contraseñas. ¡Úsalo con cautela!

### Opción de nivel de registro en consola (`--log-level-console`) {#console-log-level-option---log-level-console}

Nivel para el registro en consola.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro en absoluto (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar info, advertencias y errores
- `detail` - Registrar detail, info, advertencias y errores
- `debug` - Registrar debug, detail, info, advertencias y errores
- `trace` - Registrar trace (depuración muy detallada), debug, info, advertencias y errores

```text
default: warn
example: log-level-console=error
```

### Opción de nivel de registro en archivo (`--log-level-file`) {#file-log-level-option---log-level-file}

Nivel para el registro en archivo.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro en absoluto (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar info, advertencias y errores
- `detail` - Registrar detail, info, advertencias y errores
- `debug` - Registrar debug, detail, info, advertencias y errores
- `trace` - Registrar trace (depuración muy detallada), debug, info, advertencias y errores

```text
default: info
example: log-level-file=debug
```

### Opción de nivel de registro en stderr (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

Nivel para el registro en stderr.

Especifica qué niveles de registro se enviarán a `stderr` en lugar de a `stdout` (especificado por `log-level-console`). La marca de tiempo y el proceso no se enviarán a `stderr`.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro en absoluto (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar info, advertencias y errores
- `detail` - Registrar detail, info, advertencias y errores
- `debug` - Registrar debug, detail, info, advertencias y errores
- `trace` - Registrar trace (depuración muy detallada), debug, info, advertencias y errores

```text
default: off
example: log-level-stderr=error
```

### Opción de ruta de registro (`--log-path`) {#log-path-option---log-path}

Ruta donde se almacenan los archivos de registro.

La ruta de registro proporciona una ubicación para que pgBackRest almacene archivos de registro. Ten en cuenta que si `log-level-file=off` no se requiere ninguna ruta de registro.

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### Opción de registro en subprocesos (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Activa el registro en subprocesos.

Activa el registro en archivo para cualquier subproceso creado por este proceso usando el nivel de registro especificado por `log-level-file`.

```text
default: n
example: log-subprocess=y
```

### Opción de marca de tiempo de registro (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activa la marca de tiempo en el registro.

Activa la marca de tiempo en el registro de consola y de archivo. Esta opción se desactiva en situaciones especiales, como al generar documentación.

```text
default: y
example: log-timestamp=n
```

--------

## Opciones del mantenedor {#maintainer-options}

Las opciones del mantenedor están destinadas a soportar los forks de PostgreSQL. El mantenedor del fork debería determinar los ajustes apropiados y luego comunicarlos a los usuarios del fork.

ADVERTENCIA:

El uso incorrecto de estas opciones puede provocar un comportamiento inesperado o corrupción de datos.

Es responsabilidad del mantenedor del fork probar pgBackRest con las opciones requeridas. pgBackRest no garantiza la compatibilidad con ningún fork.

### Opción de comprobación de cabeceras del WAL (`--archive-header-check`) {#check-wal-headers-option---archive-header-check}

Comprueba la versión/id de PostgreSQL en las cabeceras del WAL.

Activada por defecto, esta opción comprueba la cabecera del WAL contra la versión de PostgreSQL y el identificador del sistema para asegurarse de que el WAL se está copiando a la stanza correcta. Esto es adicional a comprobar `pg_control` contra la stanza y a verificar que el WAL se copia desde el mismo directorio de datos de PostgreSQL donde se encuentra `pg_control`.

Por lo tanto, desactivar esta comprobación es bastante seguro, pero solo debería hacerse cuando sea necesario, p. ej., si el WAL está cifrado.

```text
default: y
example: archive-header-check=n
```

### Opción de comprobación de cabeceras de página (`--page-header-check`) {#page-header-check-option---page-header-check}

Comprueba las cabeceras de página de PostgreSQL.

Activada por defecto, esta opción añade comprobaciones de cabeceras de página.

Desactivar esta opción debería evitarse excepto cuando sea necesario, p. ej., si las páginas están cifradas.

```text
default: y
example: page-header-check=n
```

### Opción forzar versión de PostgreSQL (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

Fuerza la versión de PostgreSQL.

La versión de PostgreSQL especificada se utilizará en lugar de la versión detectada automáticamente leyendo `pg_control` o las cabeceras del WAL. Esto es útil principalmente para forks de PostgreSQL o versiones de desarrollo donde esos valores son diferentes de la versión de lanzamiento. La versión reportada por PostgreSQL vía `server_version_num` debe coincidir con la versión forzada.

ADVERTENCIA:

Ten cautela al usar esta opción, porque `pg_control` y las cabeceras del WAL se seguirán leyendo con el formato esperado para la versión especificada, es decir, el formato de la versión oficial de código abierto de PostgreSQL. Si el fork o la versión de desarrollo cambia el formato de los campos de los que depende pgBackRest, esto provocará un comportamiento inesperado. En general, esta opción solo funcionará como se espera si el fork añade todos los miembros personalizados de las estructuras *después* de los miembros estándar de PostgreSQL.

```text
example: pg-version-force=15
```

--------

## Opciones del repositorio {#repository-options}

La sección `repository` define opciones usadas para configurar el repositorio.

**Indexación**: Todas las opciones `repo-` están indexadas para permitir configurar múltiples repositorios. Por ejemplo, un solo repositorio se configura con las opciones `repo1-path`, `repo1-host`, etc. Si hay más de un repositorio configurado y no se especifica la opción `--repo` para un comando, se actuará sobre los repositorios en orden de mayor prioridad (p. ej., repo1 y luego repo2).

Las opciones `repo-retention-*` definen cuánto tiempo se retendrán las copias de seguridad. La expiración solo ocurre cuando el recuento de copias de seguridad completas excede la retención permitida. En otras palabras, si `repo1-retention-full-type` está establecido en `count` (predeterminado) y `repo1-retention-full` en 2, debe haber 3 copias completas antes de que la más antigua expire. Si `repo1-retention-full-type` está establecido en `time`, entonces `repo1-retention-full` representa días, por lo que debe haber al menos ese número de días en copias completas antes de que pueda ocurrir la expiración. Asegúrate de tener siempre espacio suficiente para retención + 1 copias de seguridad.

### Opción de cuenta de repositorio de Azure (`--repo-azure-account`) {#azure-repository-account-option---repo-azure-account}

Cuenta del repositorio de Azure.

Cuenta de Azure usada para almacenar el repositorio.

```text
example: repo1-azure-account=pg-backup
```

### Opción de contenedor de repositorio de Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Contenedor del repositorio de Azure.

Contenedor de Azure usado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del contenedor estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por Azure también puedan almacenarse en el contenedor.

```text
example: repo1-azure-container=pg-backup
```

### Opción de endpoint de repositorio de Azure (`--repo-azure-endpoint`) {#azure-repository-endpoint-option---repo-azure-endpoint}

Endpoint del repositorio de Azure.

Endpoint usado para conectarse al servicio de blobs. El predeterminado generalmente es correcto, a menos que uses Azure Government.

Para configuraciones personalizadas o de prueba, las opciones `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` y `repo-storage-verify-tls` pueden ser útiles.

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### Opción de clave de repositorio de Azure (`--repo-azure-key`) {#azure-repository-key-option---repo-azure-key}

Clave del repositorio de Azure.

Una clave compartida o una firma de acceso compartido según la opción `repo-azure-key-type`.

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### Opción de tipo de clave de repositorio de Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Tipo de clave del repositorio de Azure.

Se soportan los siguientes tipos para la autorización:

- `shared` - Clave compartida
- `sas` - Firma de acceso compartido
- `auto` - Autoriza automáticamente usando identidades administradas de Azure

```text
default: shared
example: repo1-azure-key-type=sas
```

### Opción de estilo de URI de repositorio de Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Estilo de URI de Azure.

Se soportan los siguientes estilos de URI:

- `host` - Conecta al host `account.endpoint`.
- `path` - Conecta al host `endpoint` y antepone la cuenta a los URI.

```text
default: host
example: repo1-azure-uri-style=path
```

### Opción de copia de seguridad incremental por bloques (`--repo-block`) {#block-incremental-backup-option---repo-block}

Activa la copia de seguridad incremental por bloques.

La copia incremental por bloques permite copias de seguridad más granulares dividiendo los archivos en bloques que pueden respaldarse de forma independiente. Esto ahorra espacio en el repositorio y puede mejorar el rendimiento de la restauración delta, porque se pueden obtener bloques individuales sin leer el archivo completo del repositorio.

NOTA:

La opción `repo-bundle` debe estar activada antes de que pueda activarse `repo-block`.

El tamaño de bloque de un archivo se determina según el tamaño y la antigüedad del archivo. En general, los archivos más antiguos/grandes recibirán tamaños de bloque mayores. Si un archivo es suficientemente antiguo, no se respaldará usando bloques incrementales.

La copia incremental por bloques es más eficiente cuando está activada para todos los tipos de copia de seguridad, incluida la completa. Esto hace que la completa sea un poco más grande, pero las copias de seguridad diferenciales e incrementales posteriores pueden hacer uso de los mapas de bloques generados por la copia completa para ahorrar espacio.

```text
default: n
example: repo1-block=y
```

### Opción de paquetes del repositorio (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

Agrupa archivos en el repositorio.

Agrupa (combina) archivos más pequeños para reducir el número total de archivos escritos en el repositorio. Escribir menos archivos generalmente es más eficiente, especialmente en almacenes de objetos como S3. Además, los archivos de longitud cero no se almacenan (excepto en el manifiesto), lo que ahorra tiempo y espacio.

```text
default: n
example: repo1-bundle=y
```

### Opción de límite de paquetes del repositorio (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

Límite para paquetes de archivos.

Límite de tamaño para los archivos que se incluirán en paquetes. Los archivos más grandes que este tamaño se almacenarán por separado.

Los archivos agrupados en paquetes no pueden reutilizarse cuando se reanuda una copia de seguridad, por lo que esta opción controla los archivos que pueden reanudarse; es decir, valores más altos dan como resultado menos archivos reanudables.

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### Opción de tamaño de paquete del repositorio (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

Tamaño objetivo para los paquetes de archivos.

Define el tamaño objetivo de los archivos que se añadirán a un solo paquete. El tamaño del paquete sin comprimir puede ser tan grande como `repo-bundle-size` + `repo-bundle-limit`, así que no establezcas esta opción al tamaño máximo que permita tu sistema de archivos.

En general, no es buena idea establecer esta opción demasiado alto, porque los reintentos tendrán que rehacer el paquete completo.

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### Opción de frase de contraseña de cifrado del repositorio (`--repo-cipher-pass`) {#repository-cipher-passphrase-option---repo-cipher-pass}

Frase de contraseña de cifrado del repositorio.

Frase de contraseña usada para cifrar/descifrar archivos del repositorio.

NOTA:

Cuando se ejecuta sin la opción `stanza`, el comando `info` lee los ajustes de cifrado solo de la sección `global`. Si los ajustes de cifrado están configurados por stanza, ejecuta el comando `info` con la opción `stanza` para leer una stanza cifrada.

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### Opción de tipo de cifrado del repositorio (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Cifrado usado para cifrar el repositorio.

Se soportan los siguientes tipos de cifrado:

- `none` - El repositorio no está cifrado
- `aes-256-cbc` - Advanced Encryption Standard con longitud de clave de 256 bits

Ten en cuenta que el cifrado siempre se realiza en el lado del cliente, incluso si el tipo de repositorio (p. ej., S3) soporta cifrado.

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### Opción de bucket de repositorio de GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Bucket del repositorio de GCS.

Bucket de GCS usado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del bucket estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por GCS también puedan almacenarse en el bucket.

```text
example: repo1-gcs-bucket=/pg-backup
```

### Opción de endpoint de repositorio de GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Endpoint del repositorio de GCS.

Endpoint usado para conectarse al servicio de almacenamiento. Puede actualizarse para usar un servidor GCS local o un endpoint alternativo.

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### Opción de clave de repositorio de GCS (`--repo-gcs-key`) {#gcs-repository-key-option---repo-gcs-key}

Clave del repositorio de GCS.

Un token o un archivo de clave de servicio según la opción `repo-gcs-key-type`.

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### Opción de tipo de clave de repositorio de GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Tipo de clave del repositorio de GCS.

Se soportan los siguientes tipos para la autorización:

- `auto` - Autoriza usando la cuenta de servicio de la instancia.
- `service` - Cuenta de servicio desde una clave almacenada localmente.
- `token` - Para pruebas locales, p. ej., `fakegcs`.

Cuando `repo-gcs-key-type=service`, las credenciales se recargarán cuando se renueve el token de autenticación.

```text
default: service
example: repo1-gcs-key-type=auto
```

### Opción de ID de proyecto de GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

ID de proyecto de GCS.

ID de proyecto de GCS usado para determinar la facturación de las solicitudes.

```text
example: repo1-gcs-user-project=my-project
```

### Opción de enlaces duros del repositorio (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

Enlaza con enlaces duros los archivos entre copias de seguridad en el repositorio.

Activa la creación de enlaces duros de los archivos en las copias de seguridad diferenciales e incrementales hacia sus copias completas. Esto da la apariencia de que cada copia de seguridad es una copia completa a nivel del sistema de archivos. Sin embargo, ten cuidado, porque modificar archivos que están enlazados con enlaces duros puede afectar a todas las copias de seguridad del conjunto.

```text
default: n
example: repo1-hardlink=y
```

Nombre obsoleto: hardlink

### Opción de host del repositorio (`--repo-host`) {#repository-host-option---repo-host}

Host del repositorio cuando se opera de forma remota.

Al hacer copias de seguridad y archivar a un sistema de archivos montado localmente, este ajuste no es necesario.

```text
example: repo1-host=repo1.domain.com
```

Nombre obsoleto: backup-host

### Opción de archivo de autoridad de certificación del host del repositorio (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Archivo de autoridad de certificación del host del repositorio.

Usa un archivo de CA distinto del predeterminado del sistema para conectarse al host del repositorio.

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Opción de ruta de autoridad de certificación del host del repositorio (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Ruta de autoridad de certificación del host del repositorio.

Usa una ruta de CA distinta del predeterminado del sistema para conectarse al host del repositorio.

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### Opción de archivo de certificado del host del repositorio (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Archivo de certificado del host del repositorio.

Se envía al host del repositorio para demostrar la identidad del cliente.

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### Opción de comando del host del repositorio (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

Comando pgBackRest del host del repositorio.

Solo es necesario si la ruta al comando pgBackRest es diferente en los hosts local y del repositorio. Si no se define, el comando del host del repositorio se establecerá igual que el comando local.

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nombre obsoleto: backup-cmd

### Opción de configuración del host del repositorio (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

Archivo de configuración del host del repositorio de pgBackRest.

Establece la ubicación del archivo de configuración en el host del repositorio. Esto solo es necesario si el archivo de configuración del host del repositorio está en una ubicación diferente que el archivo de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nombre obsoleto: backup-config

### Opción de ruta de inclusión de configuración del host del repositorio (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Ruta de inclusión de configuración del host del repositorio de pgBackRest.

Establece la ubicación de la ruta de inclusión de configuración en el host del repositorio. Esto solo es necesario si la ruta de inclusión de configuración del host del repositorio está en una ubicación diferente que la ruta de inclusión de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Opción de ruta de configuración del host del repositorio (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

Ruta de configuración del host del repositorio de pgBackRest.

Establece la ubicación de la ruta de configuración en el host del repositorio. Esto solo es necesario si la ruta de configuración del host del repositorio está en una ubicación diferente que la ruta de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### Opción de archivo de clave del host del repositorio (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Archivo de clave del host del repositorio.

Demuestra que el certificado del cliente fue enviado por su propietario.

```text
example: repo1-host-key-file=/path/to/client.key
```

### Opción de puerto del host del repositorio (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Puerto del host del repositorio cuando `repo-host` está establecido.

Usa esta opción para especificar un puerto no predeterminado para el protocolo del host del repositorio.

NOTA:

Cuando `repo-host-type=ssh` no existe un valor predeterminado para `repo-host-port`. En este caso el puerto será el que esté configurado para el comando especificado por `cmd-ssh`.

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

Nombre obsoleto: backup-ssh-port

### Opción de tipo de protocolo del host del repositorio (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Tipo de protocolo del host del repositorio.

Se soportan los siguientes tipos de protocolo:

- `ssh` - Secure Shell.
- `tls` - servidor TLS de pgBackRest.

```text
default: ssh
example: repo1-host-type=tls
```

### Opción de usuario del host del repositorio (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Usuario del host del repositorio cuando `repo-host` está establecido.

Define el usuario que se usará para las operaciones en el host del repositorio. Preferiblemente no es el usuario `postgres`, sino algún otro usuario como `pgbackrest`. Si PostgreSQL se ejecuta en el host del repositorio, el usuario `postgres` puede colocarse en el grupo `pgbackrest` para que tenga permisos de lectura sobre el repositorio sin poder dañar el contenido accidentalmente.

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

Nombre obsoleto: backup-user

### Opción de ruta del repositorio (`--repo-path`) {#repository-path-option---repo-path}

Ruta donde se almacenan las copias de seguridad y el archivado.

El repositorio es donde pgBackRest almacena las copias de seguridad y archiva los segmentos WAL.

Puede ser difícil estimar de antemano cuánto espacio necesitarás. Lo mejor es hacer algunas copias de seguridad y luego registrar el tamaño de los distintos tipos de copia de seguridad (full/incr/diff) y medir la cantidad de WAL generada por día. Esto te dará una idea general del espacio que necesitarás, aunque por supuesto los requisitos probablemente cambien con el tiempo a medida que tu base de datos evolucione.

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### Opción de retención de archivado (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Cantidad de WAL continuo que se retendrá, medida en número de copias de seguridad.

NOTA:

Los segmentos WAL necesarios para que una copia de seguridad sea consistente siempre se retienen hasta que la copia de seguridad expira, independientemente de cómo esté configurada esta opción.

Si este valor no está establecido y `repo-retention-full-type` es `count` (predeterminado), el archivado a expirar tomará por defecto el valor de `repo-retention-full` (o `repo-retention-diff`) correspondiente a `repo-retention-archive-type` si este está establecido en `full` (o `diff`). Esto garantizará que el WAL solo expire para copias de seguridad que ya han expirado. Si `repo-retention-full-type` es `time`, este valor tomará por defecto la eliminación de los archivados anteriores a la copia completa más antigua que se retenga tras satisfacer el ajuste `repo-retention-full`.

Esta opción debe establecerse si `repo-retention-archive-type` está establecido en `incr`. Si el espacio en disco es escaso, este ajuste, junto con `repo-retention-archive-type`, puede usarse para expirar segmentos WAL de forma agresiva. Sin embargo, hacerlo anula la posibilidad de realizar PITR desde las copias de seguridad con WAL expirado y, por lo tanto, **no** se recomienda.

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

Nombre obsoleto: retention-archive

### Opción de tipo de retención de archivado (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Tipo de copia de seguridad para la retención de WAL.

Si se establece en `full`, pgBackRest conservará los registros del archivado para el número de copias completas definido por `repo-retention-archive`. Si se establece en `diff` (diferencial), pgBackRest conservará los registros del archivado para el número de copias completas y diferenciales definido por `repo-retention-archive`, lo que significa que si la última copia de seguridad realizada fue completa, contará como diferencial a efectos de la retención del repositorio. Si se establece en `incr` (incremental), pgBackRest conservará los registros del archivado para el número de copias completas, diferenciales e incrementales definido por `repo-retention-archive`. Se recomienda no cambiar este ajuste del valor predeterminado, que solo expirará WAL junto con la expiración de copias completas.

```text
default: full
example: repo1-retention-archive-type=diff
```

Nombre obsoleto: retention-archive-type

### Opción de retención diferencial (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Número de copias de seguridad diferenciales que se retendrán.

Cuando expira una copia de seguridad diferencial, todas las copias de seguridad incrementales asociadas a la copia diferencial también expirarán. Cuando no está definido, todas las copias de seguridad diferenciales se conservarán hasta que expiren las copias completas de las que dependen.

Ten en cuenta que las copias completas se incluyen en el recuento de copias de seguridad diferenciales a efectos de la expiración. Esto reduce ligeramente el número de copias de seguridad diferenciales que deben retenerse en la mayoría de los casos.

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

Nombre obsoleto: retention-diff

### Opción de retención de copias completas (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Recuento/tiempo de retención de copias completas.

Cuando expira una copia completa, todas las copias de seguridad diferenciales e incrementales asociadas a la copia completa también expirarán. Cuando la opción no está definida, se emitirá una advertencia. Si se desea una retención indefinida, establece la opción al valor máximo.

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

Nombre obsoleto: retention-full

### Opción de tipo de retención de copias completas (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Tipo de retención para las copias completas.

Determina si el ajuste `repo-retention-full` representa un periodo de tiempo (días) o un recuento de copias completas a conservar.

Si se establece en `time`, las copias completas más antiguas que `repo-retention-full` se eliminarán del repositorio si hay al menos otra copia de seguridad que sea igual o mayor que el ajuste `repo-retention-full`. Por ejemplo, si `repo-retention-full` es 30 (días) y hay 2 copias completas: una de 25 días y otra de 35 días, ninguna copia completa expirará, porque expirar la copia de 35 días dejaría solo la copia de 25 días, lo que violaría la política de retención de 30 días de tener al menos una copia de 30 días antes de que una más antigua pueda expirar. El WAL archivado más antiguo que la copia completa más antigua restante expirará automáticamente, a menos que `repo-retention-archive-type` y `repo-retention-archive` se establezcan explícitamente.

Si se establece en `count`, las copias completas que excedan `repo-retention-full` expirarán. Por ejemplo, si `repo-retention-full` es `4` y se completa una quinta copia completa, la copia completa más antigua expirará para mantener el recuento en 4.

Ten en cuenta que una copia de seguridad debe completarse con éxito antes de que se considere para la retención. Por ejemplo, si `repo-retention-full-type` es `count` y `repo-retention-full` es `2`, debe haber 3 copias completas terminadas antes de que la más antigua expire.

```text
default: count
example: repo1-retention-full-type=time
```

### Opción de retención del historial de copias de seguridad (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Días de manifiestos del historial de copias de seguridad que se retendrán.

Una copia del manifiesto de la copia de seguridad se almacena en la ruta `backup.history` cuando una copia de seguridad se completa. Por defecto, estos archivos nunca expiran, ya que son útiles para la minería de datos, p. ej., medir el crecimiento de las copias de seguridad y del WAL a lo largo del tiempo.

Establece `repo-retention-history` para definir el número de días de manifiestos del historial de copias de seguridad que se retendrán. Las copias de seguridad no expiradas siempre se conservan en el historial de copias de seguridad. Especifica `repo-retention-history=0` para conservar el historial de copias de seguridad solo para las copias de seguridad no expiradas.

Cuando expira el manifiesto del historial de una copia completa, todos los manifiestos del historial de las copias de seguridad diferenciales e incrementales asociadas a la copia completa también expiran.

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### Opción de bucket de repositorio de S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

Bucket del repositorio de S3.

Bucket de S3 usado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del bucket estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por AWS también puedan almacenarse en el bucket.

```text
example: repo1-s3-bucket=pg-backup
```

### Opción de endpoint de repositorio de S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

Endpoint del repositorio de S3.

El endpoint de AWS debería ser válido para la región seleccionada.

Para configuraciones personalizadas o de prueba, las opciones `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` y `repo-storage-verify-tls` pueden ser útiles.

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### Opción de clave de acceso de repositorio de S3 (`--repo-s3-key`) {#s3-repository-access-key-option---repo-s3-key}

Clave de acceso del repositorio de S3.

Clave de AWS usada para acceder a este bucket.

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### Opción de clave de acceso secreta de repositorio de S3 (`--repo-s3-key-secret`) {#s3-repository-secret-access-key-option---repo-s3-key-secret}

Clave de acceso secreta del repositorio de S3.

Clave secreta de AWS usada para acceder a este bucket.

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Opción de tipo de clave de repositorio de S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

Tipo de clave del repositorio de S3.

Se soportan los siguientes tipos:

- `shared` - Claves compartidas
- `auto` - Obtiene automáticamente credenciales temporales
- `web-id` - Obtiene automáticamente credenciales de identidad web
- `pod-id` - Obtiene automáticamente credenciales de identidad de pod de EKS
- `process` - Obtiene credenciales ejecutando un proceso

```text
default: shared
example: repo1-s3-key-type=auto
```

### Opción de ID de clave KMS de repositorio de S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

Clave KMS del repositorio de S3.

Activa el cifrado del lado del servidor de S3 usando la clave del servicio de gestión de claves de AWS especificada.

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Opción de comando de proceso de autenticación de S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Comando de proceso de autenticación de S3.

Comando (y argumentos opcionales) a ejecutar para obtener credenciales temporales de S3. La primera entrada de la lista es el comando y las entradas restantes se pasan como parámetros.

El proceso debe producir una salida JSON que contenga los campos `AccessKeyId`, `SecretAccessKey`, `SessionToken` y `Expiration`. Las credenciales se refrescarán automáticamente antes de la hora de expiración. Consulta [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) para obtener detalles del formato.

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### Opción de región de repositorio de S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

Región del repositorio de S3.

La región de AWS donde se creó el bucket.

```text
example: repo1-s3-region=us-east-1
```

### Opción de pago del solicitante del repositorio de S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Pago del solicitante del repositorio de S3.

Activa el pago del solicitante de S3.

```text
default: n
example: repo1-s3-requester-pays=n
```

### Opción de rol de repositorio de S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

Rol del repositorio de S3.

El nombre del rol de AWS (no el ARN completo) usado para obtener credenciales temporales cuando `repo-s3-key-type=auto`.

```text
example: repo1-s3-role=authrole
```

### Opción de servicio de repositorio de S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

Servicio de firma de S3.

El servicio de firma de S3 usado en la autenticación SigV4. Por defecto es `s3` para los endpoints de S3 estándar. Establécelo en `s3-outposts` cuando se use un endpoint de S3 Outposts.

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### Opción de clave de cliente SSE del repositorio de S3 (`--repo-s3-sse-customer-key`) {#s3-repository-sse-customer-key-option---repo-s3-sse-customer-key}

Clave de cliente SSE del repositorio de S3.

Activa el cifrado del lado del servidor de S3 usando la clave de cliente especificada.

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Opción de endpoint STS de repositorio de S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

Endpoint STS del repositorio de S3.

El endpoint STS usado para obtener credenciales temporales cuando `repo-s3-key-type=web-id` está configurado. Establécelo en un endpoint regional (p. ej., `sts.us-east-1.amazonaws.com`) para usar STS regional, lo que puede ser necesario para GovCloud, las regiones de China o para reducir la latencia.

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Opción de token de seguridad del repositorio de S3 (`--repo-s3-token`) {#s3-repository-security-token-option---repo-s3-token}

Token de seguridad del repositorio de S3.

Token de seguridad de AWS usado con credenciales temporales.

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### Opción de estilo de URI de repositorio de S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

Estilo de URI de S3.

Se soportan los siguientes estilos de URI:

- `host` - Conecta al host `bucket.endpoint`.
- `path` - Conecta al host `endpoint` y antepone el bucket a los URI.

```text
default: host
example: repo1-s3-uri-style=path
```

### Opción de host del repositorio SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

Host del repositorio SFTP.

El host SFTP que contiene el repositorio.

```text
example: repo1-sftp-host=sftprepo.domain
```

### Opción de huella del host del repositorio SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Huella del host del repositorio SFTP.

La generación de la huella del host del repositorio SFTP debería coincidir con `repo-sftp-host-key-hash-type`. Genera la huella mediante `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. Las claves de host de ssh normalmente se encuentran en el directorio `/etc/ssh`.

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Opción de tipo de comprobación de clave de host SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Tipo de comprobación de la clave de host SFTP.

Se soportan los siguientes tipos de comprobación de la clave de host SFTP:

- `strict` - pgBackRest nunca añadirá automáticamente claves de host al archivo ~/.ssh/known_hosts y se niega a conectarse a hosts cuya clave de host haya cambiado o no se encuentre en los archivos de hosts conocidos. Esta opción obliga al usuario a añadir manualmente todos los hosts nuevos.
- `accept-new` - pgBackRest añadirá automáticamente las nuevas claves de host al archivo de hosts conocidos del usuario, pero no permitirá conexiones a hosts con claves de host modificadas.
- `fingerprint` - pgBackRest comprobará la clave de host contra la huella especificada por la opción `repo-sftp-host-fingerprint`.
- `none` - no se realizará ninguna comprobación de la clave de host.

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### Opción de tipo de hash de clave de host del repositorio SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Tipo de hash de la clave de host del repositorio SFTP.

Tipo de hash de la clave de host del repositorio SFTP. Declara el tipo de hash que se usará para calcular el resumen de la clave de host del sistema remoto al iniciar SSH. Las versiones más recientes de `libssh2` soportan `sha256` además de md5 y sha1.

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### Opción de puerto del host del repositorio SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Puerto del host del repositorio SFTP.

Puerto del host del repositorio SFTP.

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### Opción de usuario del host del repositorio SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Usuario del host del repositorio SFTP.

Usuario en el host usado para almacenar el repositorio.

```text
example: repo1-sftp-host-user=pg-backup
```

### Opción de archivo de hosts conocidos SFTP (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Archivo de hosts conocidos SFTP.

Un archivo de hosts conocidos donde buscar una coincidencia de host SFTP durante la autenticación. Cuando no se especifica, pgBackRest buscará por defecto en `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` y `/etc/ssh/ssh_known_hosts2`. Si se configura con una o más rutas de archivo, pgBackRest buscará en ellas una coincidencia. Las rutas de archivo deben ser completas o comenzar por una tilde. La opción `repo-sftp-known-host` puede pasarse varias veces para especificar más de un archivo de hosts conocidos donde buscar. Para utilizar la comprobación del archivo de hosts conocidos, `repo-sftp-host-fingerprint` no debe especificarse. Consulta también la opción `repo-sftp-host-check-type`.

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Opción de archivo de clave privada del repositorio SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Archivo de clave privada SFTP.

Archivo de clave privada SFTP usado para la autenticación.

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Opción de frase de contraseña de clave privada del repositorio SFTP (`--repo-sftp-private-key-passphrase`) {#sftp-repository-private-key-passphrase-option---repo-sftp-private-key-passphrase}

Frase de contraseña de la clave privada SFTP.

Frase de contraseña usada para acceder a la clave privada. Esta es una función opcional al crear un par de claves pública/privada SSH.

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### Opción de archivo de clave pública del repositorio SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Archivo de clave pública SFTP.

Archivo de clave pública SFTP usado para la autenticación. Opcional si se compiló contra OpenSSL, obligatorio si se compiló contra una librería diferente.

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Opción de archivo de CA del almacenamiento del repositorio (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

Archivo de CA del almacenamiento del repositorio.

Usa un archivo de CA distinto del predeterminado del sistema para los certificados del almacenamiento (p. ej., S3, Azure).

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Nombres obsoletos: repo-azure-ca-file, repo-s3-ca-file

### Opción de ruta de CA TLS del almacenamiento del repositorio (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

Ruta de CA del almacenamiento del repositorio.

Usa una ruta de CA distinta del predeterminado del sistema para los certificados del almacenamiento (p. ej., S3, Azure).

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

Nombres obsoletos: repo-azure-ca-path, repo-s3-ca-path

### Opción de host de almacenamiento del repositorio (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Host de almacenamiento del repositorio.

Conecta a un host distinto del endpoint del almacenamiento (p. ej., S3, Azure). Esto se usa típicamente para pruebas.

```text
example: repo1-storage-host=127.0.0.1
```

Nombres obsoletos: repo-azure-host, repo-s3-host

### Opción de puerto de almacenamiento del repositorio (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Puerto de almacenamiento del repositorio.

Puerto a usar al conectarse al endpoint del almacenamiento (p. ej., S3, Azure) (o al host si se especifica).

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

Nombres obsoletos: repo-azure-port, repo-s3-port

### Opción de etiqueta de almacenamiento del repositorio (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Etiquetas del almacenamiento del repositorio.

Especifica etiquetas que se añadirán a los objetos cuando el repositorio sea un almacén de objetos (p. ej., S3). La opción puede repetirse para añadir múltiples etiquetas.

No existe en pgBackRest ninguna provisión para modificar estas etiquetas, así que asegúrate de establecerlas correctamente antes de ejecutar `stanza-create` para garantizar etiquetas uniformes en todo el repositorio.

```text
example: repo1-storage-tag=key1=value1
```

### Opción de tamaño de fragmento de subida del almacenamiento del repositorio (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Tamaño de fragmento de subida del almacenamiento del repositorio.

Los almacenes de objetos como S3 permiten subir archivos en fragmentos cuando el archivo es demasiado grande para almacenarse en memoria. Incluso si el archivo puede almacenarse en memoria, es más eficiente en memoria limitar la cantidad de memoria usada para las subidas.

Un tamaño de fragmento mayor generalmente conducirá a un mejor rendimiento, porque minimizará las solicitudes de subida y permitirá que más archivos se suban en una sola solicitud en lugar de en fragmentos. La desventaja es que el uso de memoria será mayor y, como el búfer de fragmento debe asignarse por proceso, valores de `process-max` más grandes provocarán que se consuma más memoria en total.

Ten en cuenta que los tamaños de fragmento válidos varían según el tipo de almacenamiento y la plataforma. Por ejemplo, AWS S3 tiene un tamaño mínimo de fragmento de 5MiB. La terminología del tamaño de fragmento varía según el tipo de almacenamiento, así que al buscar los valores mínimos/máximos usa «part size» para AWS S3, «chunk size» para GCS y «block size» para Azure.

Si un archivo es más grande que 1GiB (el tamaño máximo que PostgreSQL creará por defecto), el tamaño de fragmento se incrementará gradualmente hasta el máximo permitido para completar la subida del archivo.

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### Opción de verificación de certificado del almacenamiento del repositorio (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Verificación de certificado del almacenamiento del repositorio.

Esta opción proporciona la capacidad de activar/desactivar la verificación del certificado TLS del servidor de almacenamiento (p. ej., S3, Azure). La desactivación solo debería usarse para pruebas u otros escenarios donde un certificado haya sido autofirmado.

```text
default: y
example: repo1-storage-verify-tls=n
```

Nombres obsoletos: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Opción de enlaces simbólicos del repositorio (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Crea enlaces simbólicos dentro del repositorio.

Activa la creación de los enlaces simbólicos `latest` y de los tablespaces. Estos enlaces simbólicos son más útiles cuando se usan instantáneas para hacer una recuperación in situ en el repositorio, que es un caso de uso poco común.

Aunque esta función probablemente no sea útil para la gran mayoría de los usuarios, permanece activada por defecto por razones de compatibilidad. Sin embargo, puede ser útil desactivar los enlaces simbólicos para almacenamientos tipo Posix que no los soportan.

```text
default: y
example: repo1-symlink=n
```

### Opción de hora objetivo para el repositorio (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

Hora objetivo para el repositorio.

La hora objetivo define el tiempo que usan los comandos para leer un repositorio en almacenamiento versionado. Esto permite que el comando lea el repositorio tal como estaba en un punto en el tiempo, para recuperar datos que hayan sido eliminados o corrompidos por accidente del usuario o por malware.

El almacenamiento versionado está soportado por S3, GCS y Azure, pero en general no está activado por defecto. Además de activar el versionado, puede ser útil activar el bloqueo de objetos para S3 y el borrado suave para GCS o Azure.

Cuando se especifica la opción `repo-target-time`, la opción `repo` también debe proporcionarse. Es probable que no todos los tipos de repositorio soporten el versionado y, en general, tiene sentido apuntar a un solo repositorio para la recuperación.

Ten en cuenta que las comparaciones con la marca de tiempo del almacenamiento son <= que la marca de tiempo proporcionada y los milisegundos se truncan de la marca de tiempo cuando se proporciona.

```text
example: repo-target-time=2024-08-08 12:12:12+00
```

### Opción de tipo de repositorio (`--repo-type`) {#repository-type-option---repo-type}

Tipo de almacenamiento usado para el repositorio.

Se soportan los siguientes tipos de repositorio:

- `azure` - Azure Blob Storage Service
- `cifs` - Como `posix`, pero desactiva los enlaces y los fsync de directorio
- `gcs` - Google Cloud Storage
- `posix` - Sistemas de archivos compatibles con Posix
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

Cuando se usa un montaje NFS como repositorio `posix`, se aplican a pgBackRest las mismas reglas descritas en la documentación de PostgreSQL: [Creating a Database Cluster - File Systems](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```text
default: posix
example: repo1-type=cifs
```

--------

## Opciones de restauración {#restore-options}

La sección `restore` define ajustes usados para restaurar copias de seguridad.

### Opción de modo de archivado (`--archive-mode`) {#archive-mode-option---archive-mode}

Conserva o desactiva el archivado en el clúster restaurado.

Esta opción permite conservar o desactivar el archivado en un clúster restaurado. Esto es útil cuando el clúster debe promocionarse para hacer algún trabajo pero no está destinado a convertirse en el nuevo primario. En este caso no es buena idea enviar WAL desde el clúster al repositorio.

Se soportan los siguientes modos:

- `off` - desactiva el archivado estableciendo `archive_mode=off`.
- `preserve` - conserva el ajuste `archive_mode` actual.

**NOTA**: Esta opción no está disponible en PostgreSQL < 12.

```text
default: preserve
example: archive-mode=off
```

### Opción de exclusión de bases de datos (`--db-exclude`) {#exclude-database-option---db-exclude}

Restaura excluyendo las bases de datos especificadas.

Las bases de datos excluidas se restaurarán como archivos dispersos rellenados con ceros para ahorrar espacio, pero permitiendo que PostgreSQL realice la recuperación. Tras la recuperación, esas bases de datos no serán accesibles, pero pueden eliminarse con el comando `drop database`. La opción `--db-exclude` puede pasarse varias veces para especificar más de una base de datos a excluir.

Cuando se usa en combinación con la opción `--db-include`, `--db-exclude` solo se aplicará a las bases de datos del sistema estándar (`template0`, `template1` y `postgres`).

```text
example: db-exclude=db_main
```

### Opción de inclusión de bases de datos (`--db-include`) {#include-database-option---db-include}

Restaura solo las bases de datos especificadas.

Esta función permite que solo se restauren las bases de datos seleccionadas. Las bases de datos que no se incluyan específicamente se restaurarán como archivos dispersos rellenados con ceros para ahorrar espacio, pero permitiendo que PostgreSQL realice la recuperación. Tras la recuperación, las bases de datos que no se incluyeron no serán accesibles, pero pueden eliminarse con el comando `drop database`.

NOTA:

las bases de datos integradas (`template0`, `template1` y `postgres`) siempre se restauran a menos que se excluyan específicamente.

La opción `--db-include` puede pasarse varias veces para especificar más de una base de datos a incluir.

Consulta [Restaurar bases de datos seleccionadas](/es/pgbackrest/user-guide/#restore-selected-databases) para obtener información adicional y advertencias.

```text
example: db-include=db_main
```

### Opción de enlazar todo (`--link-all`) {#link-all-option---link-all}

Restaura todos los enlaces simbólicos.

Por defecto, los directorios y archivos enlazados simbólicamente se restauran como directorios y archivos normales en $PGDATA. Esto se debe a que puede no ser seguro restaurar los enlaces simbólicos a sus destinos originales en un sistema distinto de aquel donde se realizó la copia de seguridad original. Esta opción restaura todos los enlaces simbólicos tal como estaban en el sistema original donde se realizó la copia de seguridad.

```text
default: n
example: link-all=y
```

### Opción de mapeo de enlaces (`--link-map`) {#link-map-option---link-map}

Modifica el destino de un enlace simbólico.

Permite cambiar el archivo o la ruta de destino de un enlace simbólico al restaurar. Esto es útil para restaurar en sistemas que tienen una disposición de almacenamiento diferente a la del sistema original donde se generó la copia de seguridad.

```text
example: link-map=pg_xlog=/data/xlog
```

### Opción de recuperación (`--recovery-option`) {#recovery-option---recovery-option}

Establece una opción en `postgresql.auto.conf` o `recovery.conf`.

Consulta [Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html) para obtener detalles sobre las opciones de `postgresql.auto.conf` o `recovery.conf` (asegúrate de seleccionar tu versión de PostgreSQL). Esta opción puede usarse varias veces.

Para PostgreSQL >= 12, las opciones se escribirán en `postgresql.auto.conf`. Para todas las demás versiones, las opciones se escribirán en `recovery.conf`.

NOTA:

La opción `restore_command` se generará automáticamente, pero puede anularse con esta opción. Ten cuidado al especificar tu propio `restore_command`, ya que pgBackRest está diseñado para gestionarlo por ti. Las opciones de recuperación objetivo (recovery_target_name, recovery_target_time, etc.) son generadas automáticamente por pgBackRest y no deben establecerse con esta opción.

Dado que pgBackRest no inicia PostgreSQL después de escribir el archivo `postgresql.auto.conf` o `recovery.conf`, siempre es posible editar/comprobar `postgresql.auto.conf` o `recovery.conf` antes de reiniciar manualmente.

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### Opción de mapeo de tablespaces (`--tablespace-map`) {#tablespace-map-option---tablespace-map}

Restaura un tablespace en el directorio especificado.

Mueve un tablespace a una nueva ubicación durante la restauración. Esto es útil cuando las ubicaciones de los tablespaces no son las mismas en una réplica, o cuando un sistema actualizado tiene diferentes puntos de montaje.

Las ubicaciones de los tablespaces no se almacenan en pg_tablespace, así que mover tablespaces puede hacerse sin consecuencias. Sin embargo, mover un tablespace al `data_directory` no se recomienda y puede causar problemas. Para más información sobre cómo mover tablespaces, http://www.databasesoup.com/2013/11/moving-tablespaces.html es un buen recurso.

```text
example: tablespace-map=ts_01=/db/ts_01
```

### Opción de mapeo de todos los tablespaces (`--tablespace-map-all`) {#map-all-tablespaces-option---tablespace-map-all}

Restaura todos los tablespaces en el directorio especificado.

Por defecto, los tablespaces se restauran en sus ubicaciones originales. Este comportamiento puede modificarse para cada tablespace con la opción `tablespace-map`, pero a veces es preferible remapear todos los tablespaces a un nuevo directorio de una sola vez. Esto es particularmente útil para sistemas de desarrollo o de pruebas (staging) que pueden no tener la misma disposición de almacenamiento que el sistema original donde se generó la copia de seguridad.

La ruta especificada será la ruta principal usada para crear todos los tablespaces de la copia de seguridad.

PRECAUCIÓN:

Los tablespaces creados después de que comenzara la copia de seguridad no serán mapeados. Haz una nueva copia de seguridad después de crear un tablespace si se requiere el mapeo de tablespaces.

```text
example: tablespace-map-all=/data/tablespace
```

--------

## Opciones del servidor {#server-options}

La sección `server` define opciones usadas para configurar el servidor TLS.

### Opción de dirección del servidor TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

Dirección del servidor TLS.

Dirección IP en la que el servidor escuchará las solicitudes de los clientes.

```text
default: localhost
example: tls-server-address=*
```

### Opción de clientes autorizados del servidor TLS (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

Clientes autorizados del servidor TLS.

Los clientes se autorizan en el servidor verificando su certificado y comprobando el CN (Common Name) de su certificado contra una lista en el servidor configurada con la opción `tls-server-auth`.

Un CN de cliente puede autorizarse para tantas stanzas como sea necesario proporcionando una lista separada por comas a la opción `tls-server-auth`, o para todas las stanzas especificando `tls-server-auth=client-cn=*`. No pueden especificarse comodines para el CN del cliente.

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### Opción de autoridades de certificación del servidor TLS (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

Autoridades de certificación del servidor TLS.

Comprueba que los certificados de los clientes estén firmados por una autoridad de certificación de confianza.

```text
example: tls-server-ca-file=/path/to/server.ca
```

### Opción de certificado del servidor TLS (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

Archivo de certificado del servidor TLS.

Se envía al cliente para mostrar la identidad del servidor.

```text
example: tls-server-cert-file=/path/to/server.crt
```

### Opción de clave del servidor TLS (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

Archivo de clave del servidor TLS.

Demuestra que el certificado del servidor fue enviado por su propietario.

```text
example: tls-server-key-file=/path/to/server.key
```

### Opción de puerto del servidor TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

Puerto del servidor TLS.

Puerto en el que el servidor escuchará las solicitudes de los clientes.

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## Opciones de stanza {#stanza-options}

Una stanza define la configuración de copia de seguridad para un clúster de bases de datos PostgreSQL específico. La sección de la stanza debe definir la ruta del clúster de bases de datos y el host/usuario si el clúster de bases de datos es remoto. Además, cualquier sección de configuración global puede anularse para definir ajustes específicos de la stanza.

**Indexación**: Todas las opciones `pg-` están indexadas para permitir configurar múltiples hosts de PostgreSQL. Por ejemplo, un solo primario se configura con las opciones `pg1-path`, `pg1-port`, etc. Si se configura un standby, indexa las opciones `pg-` en el host del repositorio como `pg2-` (p. ej., pg2-host, pg2-path, etc).

### Opción de base de datos de PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

Base de datos de PostgreSQL.

El nombre de la base de datos usado al conectarse a PostgreSQL. El predeterminado suele ser el mejor, pero algunas instalaciones pueden no contener esta base de datos.

Ten en cuenta que, por razones de compatibilidad histórica, el ajuste de la variable de entorno `PGDATABASE` se ignorará.

```text
default: postgres
example: pg1-database=backupdb
```

### Opción de host de PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

Host de PostgreSQL para operar de forma remota.

Se usa para copias de seguridad donde el host de PostgreSQL es diferente del host del repositorio.

```text
example: pg1-host=db.domain.com
```

Nombre obsoleto: db-host

### Opción de archivo de autoridad de certificación del host de PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Archivo de autoridad de certificación del host de PostgreSQL.

Usa un archivo de CA distinto del predeterminado del sistema para conectarse al host de PostgreSQL.

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Opción de ruta de autoridad de certificación del host de PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Ruta de autoridad de certificación del host de PostgreSQL.

Usa una ruta de CA distinta del predeterminado del sistema para conectarse al host de PostgreSQL.

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### Opción de archivo de certificado del host de PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Archivo de certificado del host de PostgreSQL.

Se envía al host de PostgreSQL para demostrar la identidad del cliente.

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### Opción de comando del host de PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

Comando pgBackRest del host de PostgreSQL.

Solo es necesario si la ruta al comando pgBackRest es diferente en los hosts local y de PostgreSQL. Si no se define, el comando del host de PostgreSQL se establecerá igual que el comando local.

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nombre obsoleto: db-cmd

### Opción de configuración del host de PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

Archivo de configuración del host de bases de datos de pgBackRest.

Establece la ubicación del archivo de configuración en el host de PostgreSQL. Esto solo es necesario si el archivo de configuración del host de PostgreSQL está en una ubicación diferente que el archivo de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nombre obsoleto: db-config

### Opción de ruta de inclusión de configuración del host de PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Ruta de inclusión de configuración del host de bases de datos de pgBackRest.

Establece la ubicación de la ruta de inclusión de configuración en el host de PostgreSQL. Esto solo es necesario si la ruta de inclusión de configuración del host de PostgreSQL está en una ubicación diferente que la ruta de inclusión de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Opción de ruta de configuración del host de PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

Ruta de configuración del host de bases de datos de pgBackRest.

Establece la ubicación de la ruta de configuración en el host de PostgreSQL. Esto solo es necesario si la ruta de configuración del host de PostgreSQL está en una ubicación diferente que la ruta de configuración local.

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### Opción de archivo de clave del host de PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Archivo de clave del host de PostgreSQL.

Demuestra que el certificado del cliente fue enviado por su propietario.

```text
example: pg1-host-key-file=/path/to/client.key
```

### Opción de puerto del host de PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Puerto del host de PostgreSQL cuando `pg-host` está establecido.

Usa esta opción para especificar un puerto no predeterminado para el protocolo del host de PostgreSQL.

NOTA:

Cuando `pg-host-type=ssh` no existe un valor predeterminado para `pg-host-port`. En este caso el puerto será el que esté configurado para el comando especificado por `cmd-ssh`.

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

Nombre obsoleto: db-ssh-port

### Opción de tipo de protocolo del host de PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Tipo de protocolo del host de PostgreSQL.

Se soportan los siguientes tipos de protocolo:

- `ssh` - Secure Shell.
- `tls` - servidor TLS de pgBackRest.

```text
default: ssh
example: pg1-host-type=tls
```

### Opción de usuario del host de PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Usuario de inicio de sesión del host de PostgreSQL cuando `pg-host` está establecido.

Este usuario también será el propietario del proceso remoto de pgBackRest e iniciará las conexiones a PostgreSQL. Para que esto funcione correctamente, el usuario debería ser el propietario del clúster de bases de datos de PostgreSQL, que generalmente es `postgres`, el predeterminado.

```text
default: postgres
example: pg1-host-user=db_owner
```

Nombre obsoleto: db-user

### Opción de ruta de PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

Directorio de datos de PostgreSQL.

Debería ser el mismo que el `data_directory` reportado por PostgreSQL. Aunque este valor puede leerse de varios lugares, es prudente establecerlo en caso de que esos recursos no estén disponibles durante una restauración o un escenario de copia de seguridad sin conexión.

La opción `pg-path` se comprueba contra el valor reportado por PostgreSQL en cada copia de seguridad en línea, así que siempre debería estar actualizada.

```text
example: pg1-path=/data/db
```

Nombre obsoleto: db-path

### Opción de puerto de PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

Puerto de PostgreSQL.

Puerto en el que se ejecuta PostgreSQL. Esto normalmente no necesita especificarse, ya que la mayoría de los clústeres de PostgreSQL se ejecutan en el puerto predeterminado.

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

Nombre obsoleto: db-port

### Opción de ruta de socket de PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Ruta del socket unix de PostgreSQL.

El directorio del socket unix que se especificó cuando se inició PostgreSQL. pgBackRest buscará automáticamente en la ubicación estándar de tu sistema operativo, así que normalmente no hay necesidad de especificar este ajuste, a menos que el directorio del socket se haya modificado explícitamente con el ajuste `unix_socket_directories` en `postgresql.conf`.

```text
example: pg1-socket-path=/var/run/postgresql
```

Nombre obsoleto: db-socket-path

### Opción de usuario de base de datos de PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

Usuario de base de datos de PostgreSQL.

El nombre de usuario de base de datos usado al conectarse a PostgreSQL. Si no se especifica, pgBackRest se conectará con el usuario local del sistema operativo o `PGUSER`.

```text
example: pg1-user=backupuser
```
