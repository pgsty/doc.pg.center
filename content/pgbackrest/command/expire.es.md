---
title: "Comando de expiración (expire)"
linkTitle: "expire"
weight: 60
description: "Referencia de las opciones y el comportamiento del comando `expire` de pgBackRest."
icon: fa-solid fa-hourglass-end
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/command.html#command-expire"
---

pgBackRest realiza la rotación de copias completas según el tipo de retención, que puede ser un recuento o un periodo de tiempo. Cuando se especifica un recuento, la expiración no se ocupa de cuándo se crearon las copias de seguridad, sino de cuántas deben conservarse. Las copias de seguridad diferenciales se basan en recuento, pero siempre expirarán cuando expire la copia completa de la que dependen. Las copias de seguridad incrementales no expiran por retención de forma independiente — siempre expiran junto con su copia completa o diferencial relacionada. Consulta las secciones [Retención de copias completas](/es/pgbackrest/user-guide/#full-backup-retention) y [Retención de copias diferenciales](/es/pgbackrest/user-guide/#differential-backup-retention) para obtener detalles y ejemplos.

Por defecto, el WAL archivado se conserva para las copias de seguridad que no han expirado; sin embargo, aunque no se recomienda, esta pauta puede modificarse por repositorio con las opciones retention-archive. Consulta la sección [Retención del archivado](/es/pgbackrest/user-guide/#archive-retention) para obtener detalles y ejemplos.

El comando `expire` se ejecuta automáticamente después de cada copia de seguridad exitosa y también puede ser ejecutado por el usuario. Cuando lo ejecuta el usuario, la expiración ocurrirá según lo definido por los ajustes de retención de cada repositorio configurado. Si se proporciona la opción `--repo`, la expiración ocurrirá solo en el repositorio especificado. El usuario también puede limitar la expiración a un conjunto de copia de seguridad específico con la opción `--set` y, a menos que se especifique la opción `--repo`, se buscará en todos los repositorios y se expirará cualquiera que coincida con los criterios del conjunto. Cabe destacar que la pauta de retención del archivado se comprobará y se aplicará cada vez que se ejecute el comando `expire`.

## Opciones del comando {#command-options}

### Opción de expiración del archivado anterior (`--archive-expire-before`) {#expire-archive-before-option---archive-expire-before}

Elimina el archivado de WAL anterior al segmento WAL especificado.

Elimina los segmentos WAL anteriores al segmento especificado, pero solo aquellos que no son requeridos por una copia de seguridad retenida, es decir, segmentos más antiguos que el conjunto de copia de seguridad más antiguo que se retiene, o cualquier segmento cuando el repositorio no contiene ninguna copia de seguridad. El segmento especificado y todo lo posterior a él se conservan. Esto refleja el valor que PostgreSQL pasa a archive_cleanup_command como `%r`.

Esta opción está destinada principalmente a repositorios de solo archivado donde no se almacenan copias de seguridad. También puede usarse para recuperar espacio del archivado de WAL antes de la primera copia de seguridad, cuando aún no se ha cumplido la retención de copias completas para disparar la expiración del archivado.

```yaml
example: --archive-expire-before=000000010000000000000010
```

### Opción de error ante sumas de comprobación de páginas no válidas (`--checksum-page-error`) {#error-on-invalid-page-checksums-option---checksum-page-error}

Notificar un error ante sumas de comprobación de páginas no válidas.

Si está activada y la copia más antigua que se conservaría contiene errores en las sumas de comprobación, la orden `expire` termina con un error antes de realizar cualquier cambio. Si está desactivada, `expire` continúa y emite una advertencia si la copia más antigua conservada contiene esos errores.

Si se utiliza `--set`, `expire` continúa aunque esta opción esté activada. Se emite una advertencia si la copia más antigua conservada contiene errores en las sumas de comprobación.

```yaml
default: y
example: --no-checksum-page-error
```

### Opción de la más antigua (`--oldest`) {#oldest-option---oldest}

Expira el conjunto de copia de seguridad elegible más antiguo.

Expira el conjunto de copia completa más antiguo que pueda eliminarse (lo que significa que permanece al menos una copia completa más reciente). Esto es equivalente a reducir manualmente la retención en uno, pero calculado automáticamente. Todas las copias de seguridad relacionadas con el conjunto de copia completa expirado (diferenciales e incrementales) también expiran.

Cuando se usa, la retención del archivado también se ajusta temporalmente para que el WAL de las copias de seguridad expiradas pueda eliminarse en la misma ejecución.

Si está configurada la retención de copias completas basada en tiempo (usando `--repo-retention-full-type=time`), entonces `--oldest` usa la expiración basada en recuento para esta ejecución.

ADVERTENCIA:

Esta opción no puede combinarse con `--set`.

```yaml
default: n
example: --oldest
```

### Opción de conjunto (`--set`) {#set-option---set}

Conjunto de copia de seguridad a expirar.

El conjunto de copia de seguridad especificado (es decir, la etiqueta de copia de seguridad proporcionada y todas sus copias de seguridad dependientes, si las hay) expirará independientemente de las reglas de retención de copias de seguridad, excepto que debe permanecer al menos una copia completa en el repositorio.

ADVERTENCIA:

Usa esta opción con extrema precaución — eliminará permanentemente del repositorio de pgBackRest todas las copias de seguridad y archivados que no se requieran para hacer consistente una copia de seguridad, correspondientes al conjunto de copia de seguridad especificado. Este proceso puede anular la capacidad de realizar una PITR. Si las opciones `--repo-retention-full` y/o `--repo-retention-archive` están configuradas, se recomienda anularlas estableciendo sus valores al máximo mientras se realiza la expiración ad hoc, con el fin de evitar una expiración no intencionada de los archivados.

```yaml
example: --set=20150131-153358F_20150131-153401I
```

## Opciones generales {#general-options}

### Opción permitir ejecutar como root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Permite que el comando se ejecute como el usuario root.

Por defecto, solo el comando `restore` puede ejecutarse como usuario root, ya que está diseñado para gestionar cuidadosamente la propiedad de los archivos. Ejecutar otros comandos como root corre el riesgo de crear archivos (p. ej., en el repositorio) cuya propiedad es de root y que, por lo tanto, resultan inaccesibles para el usuario de PostgreSQL, lo que provoca que comandos posteriores fallen.

Activa esta opción para ejecutar un comando como root de todos modos. Sin embargo, es mucho mejor ejecutar pgBackRest como el usuario propietario del repositorio y del clúster de PostgreSQL.

```yaml
default: n
example: --allow-root
```

### Opción de tamaño de búfer (`--buffer-size`) {#buffer-size-option---buffer-size}

Tamaño de búfer para operaciones de E/S.

Tamaño de búfer utilizado para copiar, comprimir, cifrar y otras operaciones. El número de búferes utilizados depende de las opciones y cada operación puede usar memoria adicional, por ejemplo, la compresión `gz` puede usar 256KiB de memoria adicional.

Los valores permitidos son `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` y `16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### Opción de comando de cliente SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

Comando del cliente SSH.

Usa un comando de cliente SSH específico cuando se desee uno alternativo o cuando el comando `ssh` no esté en $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Opción de nivel de compresión de red (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Nivel de compresión de red.

Establece el nivel de compresión de red cuando `compress-type=none` y el comando no se ejecuta en el mismo host que el repositorio. La compresión se utiliza para reducir el tráfico de red. Cuando `compress-type` no es igual a `none`, el ajuste `compress-level-network` se ignora y en su lugar se usa `compress-level`, de modo que el archivo solo se comprime una vez.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### Opción de configuración (`--config`) {#config-option---config}

Archivo de configuración de pgBackRest.

Usa esta opción para especificar un archivo de configuración diferente al predeterminado.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### Opción de ruta de inclusión de configuración (`--config-include-path`) {#config-include-path-option---config-include-path}

Ruta a archivos de configuración adicionales de pgBackRest.

Los archivos de configuración existentes en la ubicación especificada con extensión `.conf` se concatenarán con el archivo de configuración de pgBackRest, dando como resultado un único archivo de configuración.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### Opción de ruta de configuración (`--config-path`) {#config-path-option---config-path}

Ruta base de los archivos de configuración de pgBackRest.

Este ajuste se utiliza para anular la ruta base predeterminada de las opciones `--config` y `--config-include-path`, a menos que se establezcan explícitamente en la línea de comandos.

Por ejemplo, pasar solo `--config-path=/conf/pgbackrest` hace que el valor predeterminado de `--config` se establezca en `/conf/pgbackrest/pgbackrest.conf` y el de `--config-include-path` en `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### Opción de simulación (`--dry-run`) {#dry-run-option---dry-run}

Ejecuta una simulación del comando.

La opción `--dry-run` es una opción disponible solo en la línea de comandos y puede pasarse cuando se desee determinar qué modificaciones hará el comando sin que este haga realmente ninguna modificación.

```yaml
default: n
example: --dry-run
```

### Opción de tiempo de espera de E/S (`--io-timeout`) {#io-timeout-option---io-timeout}

Tiempo de espera de E/S.

Tiempo de espera, en segundos, utilizado para conexiones y operaciones de lectura/escritura.

Ten en cuenta que la operación de lectura/escritura completa no necesita terminar dentro de este tiempo de espera, pero debe haber *algún* progreso, aunque sea un solo byte.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Opción de ruta de bloqueo (`--lock-path`) {#lock-path-option---lock-path}

Ruta donde se almacenan los archivos de bloqueo.

La ruta de bloqueo proporciona una ubicación para que pgBackRest cree archivos de bloqueo que evitan que operaciones conflictivas se ejecuten concurrentemente.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### Opción de umask neutro (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Usa un umask neutro.

Establece el umask en 0000 para que los modos en el repositorio se creen de forma razonable. El modo de directorio predeterminado es 0750 y el modo de archivo predeterminado es 0640.

Para usar en su lugar el umask del usuario que ejecuta, especifica `neutral-umask=n` en el archivo de configuración o `--no-neutral-umask` en la línea de comandos.

```yaml
default: y
example: --no-neutral-umask
```

### Opción de establecimiento de prioridad del proceso (`--priority`) {#set-process-priority-option---priority}

Establece la prioridad del proceso.

Define cuánta prioridad (es decir, cuánta «niceness») otorgará el planificador del kernel al proceso. Los valores positivos disminuyen la prioridad y los valores negativos la aumentan. En la mayoría de los casos, los procesos no tienen permiso para aumentar su prioridad.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Opción de tiempo de espera de protocolo (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Tiempo de espera de protocolo.

Establece el tiempo de espera, en segundos, que el proceso local o remoto esperará a que se reciba un nuevo mensaje en la capa de protocolo. Esto evita que los procesos esperen indefinidamente un mensaje.

> **NOTA:** La opción `protocol-timeout` debe ser mayor que la opción `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### Opción keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Activación de keep-alive.

Activa los mensajes keep-alive en conexiones de socket.

```yaml
default: y
example: --no-sck-keep-alive
```

### Opción de stanza (`--stanza`) {#stanza-option---stanza}

Define el stanza.

Un stanza es la configuración de un clúster de bases de datos de PostgreSQL que define dónde se encuentra, cómo se hará la copia de seguridad, las opciones de archivado, etc. La mayoría de los servidores de bases de datos tendrán solo un clúster de bases de datos de PostgreSQL y, por lo tanto, un solo stanza, mientras que los servidores de copias de seguridad tendrán un stanza por cada clúster de bases de datos del que haya que hacer copia de seguridad.

Es tentador nombrar el stanza como el clúster primario, pero un mejor nombre describe las bases de datos contenidas en el clúster. Como el nombre del stanza se usará para el primario y todas las réplicas, es más apropiado elegir un nombre que describa la función real del clúster, como app o dw, en lugar del nombre local del clúster, como main o prod.

```yaml
example: --stanza=main
```

### Opción de recuento keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Recuento de keep-alive.

Especifica el número de mensajes keep-alive de TCP que pueden perderse antes de que la conexión se considere muerta.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPCNT`.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### Opción de tiempo de inactividad de keep-alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Tiempo de inactividad de keep-alive.

Especifica la cantidad de tiempo (en segundos) sin actividad de red tras el cual el sistema operativo debería enviar un mensaje keep-alive de TCP.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPIDLE`.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### Opción de intervalo de keep-alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Tiempo de intervalo de keep-alive.

Especifica la cantidad de tiempo (en segundos) tras el cual debe retransmitirse un mensaje keep-alive de TCP que no haya sido reconocido.

Esta opción está disponible en sistemas que soportan la opción de socket `TCP_KEEPINTVL`.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### Opción de conjuntos de cifrado TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Conjuntos de cifrado TLSv1.2 permitidos.

Todas las conexiones TLS entre el cliente y el servidor de pgBackRest están cifradas. Por defecto, las conexiones a almacenes de objetos (p. ej., S3) también están cifradas.

> **NOTA:** El nivel de seguridad mínimo absoluto para cualquier conexión de transporte es TLSv1.2.

Los conjuntos de cifrado aceptados pueden ajustarse si surge la necesidad. El ejemplo es una opción razonable a menos que tengas requisitos de seguridad específicos. Si no se establece (el comportamiento predeterminado), se aplica el valor predeterminado de la biblioteca OpenSSL subyacente.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Opción de conjuntos de cifrado TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Conjuntos de cifrado TLSv1.3 permitidos.

Todas las conexiones TLS entre el cliente y el servidor de pgBackRest están cifradas. Por defecto, las conexiones a almacenes de objetos (p. ej., S3) también están cifradas.

> **NOTA:** El nivel de seguridad mínimo absoluto para cualquier conexión de transporte es TLSv1.2.

Los conjuntos de cifrado aceptados pueden ajustarse si surge la necesidad. Si no se establece (el comportamiento predeterminado), se aplica el valor predeterminado de la biblioteca OpenSSL subyacente.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## Opciones de registro {#log-options}

### Opción de nivel de registro en consola (`--log-level-console`) {#console-log-level-option---log-level-console}

Nivel para el registro en consola.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro alguno (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar información, advertencias y errores
- `detail` - Registrar detalle, información, advertencias y errores
- `debug` - Registrar depuración, detalle, información, advertencias y errores
- `trace` - Registrar traza (depuración muy detallada), depuración, información, advertencias y errores

```yaml
default: warn
example: --log-level-console=error
```

### Opción de nivel de registro en archivo (`--log-level-file`) {#file-log-level-option---log-level-file}

Nivel para el registro en archivo.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro alguno (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar información, advertencias y errores
- `detail` - Registrar detalle, información, advertencias y errores
- `debug` - Registrar depuración, detalle, información, advertencias y errores
- `trace` - Registrar traza (depuración muy detallada), depuración, información, advertencias y errores

```yaml
default: info
example: --log-level-file=debug
```

### Opción de nivel de registro en stderr (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

Nivel para el registro en stderr.

Especifica qué niveles de registro se enviarán a `stderr` en lugar de a `stdout` (especificado por `log-level-console`). La marca de tiempo y el proceso no se enviarán a `stderr`.

Se soportan los siguientes niveles de registro:

- `off` - Sin registro alguno (no recomendado)
- `error` - Registrar solo errores
- `warn` - Registrar advertencias y errores
- `info` - Registrar información, advertencias y errores
- `detail` - Registrar detalle, información, advertencias y errores
- `debug` - Registrar depuración, detalle, información, advertencias y errores
- `trace` - Registrar traza (depuración muy detallada), depuración, información, advertencias y errores

```yaml
default: off
example: --log-level-stderr=error
```

### Opción de ruta de registro (`--log-path`) {#log-path-option---log-path}

Ruta donde se almacenan los archivos de registro.

La ruta de registro proporciona una ubicación para que pgBackRest almacene archivos de registro. Ten en cuenta que si `log-level-file=off` no se requiere ninguna ruta de registro.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### Opción de registro en subprocesos (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Activa el registro en subprocesos.

Activa el registro en archivo para cualquier subproceso creado por este proceso usando el nivel de registro especificado por `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### Opción de marca de tiempo de registro (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activa la marca de tiempo en el registro.

Activa la marca de tiempo en el registro de consola y de archivo. Esta opción se desactiva en situaciones especiales, como la generación de documentación.

```yaml
default: y
example: --no-log-timestamp
```

## Opciones del repositorio {#repository-options}

### Opción de establecimiento de repositorio (`--repo`) {#set-repository-option---repo}

Establece el repositorio.

Establece el repositorio sobre el que operará un comando.

Por ejemplo, esta opción puede usarse para realizar una restauración desde un repositorio específico, en lugar de dejar que pgBackRest elija.

```yaml
allowed: [1, 256]
example: --repo=1
```

### Opción de contenedor de repositorio de Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Contenedor de repositorio de Azure.

Contenedor de Azure utilizado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del contenedor estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por Azure también puedan almacenarse en el contenedor.

```yaml
example: --repo1-azure-container=pg-backup
```

### Opción de tipo de clave de repositorio de Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Tipo de clave del repositorio de Azure.

Se admiten los siguientes tipos de autorización:

- `shared` - Clave compartida
- `sas` - Firma de acceso compartido
- `auto` - Autorizar automáticamente usando identidades administradas de Azure

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### Opción de estilo de URI de repositorio de Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Estilo de URI de Azure.

Se soportan los siguientes estilos de URI:

- `host` - Conectar al host `account.endpoint`.
- `path` - Conectar al host `endpoint` y anteponer la cuenta a los URI.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### Opción de tipo de cifrado del repositorio (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Cifrado utilizado para cifrar el repositorio.

Se soportan los siguientes tipos de cifrado:

- `none` - El repositorio no está cifrado
- `aes-256-cbc` - Advanced Encryption Standard con longitud de clave de 256 bits

Ten en cuenta que el cifrado siempre se realiza en el lado del cliente, incluso si el tipo de repositorio (p. ej., S3) soporta cifrado.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### Opción de bucket de repositorio de GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

Bucket de repositorio de GCS.

Bucket de GCS utilizado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del bucket estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por GCS también puedan almacenarse en el bucket.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### Opción de endpoint de repositorio de GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

Endpoint del repositorio de GCS.

Endpoint utilizado para conectarse al servicio de almacenamiento. Puede actualizarse para usar un servidor GCS local o un endpoint alternativo.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### Opción de tipo de clave de repositorio de GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

Tipo de clave del repositorio de GCS.

Se admiten los siguientes tipos de autorización:

- `auto` - Autorizar usando la cuenta de servicio de la instancia.
- `service` - Cuenta de servicio desde una clave almacenada localmente.
- `token` - Para pruebas locales, p. ej., `fakegcs`.
- `web-id` - Autorización mediante Workload Identity Federation.

Cuando `repo-gcs-key-type=service`, las credenciales se recargarán cuando se renueve el token de autenticación.

Cuando `repo-gcs-key-type=web-id`, la opción `repo-gcs-key` debe indicar un archivo de credenciales de una cuenta externa. El token de identidad web se vuelve a cargar al renovar el token de autenticación.

No se admite `service_account_impersonation_url`. Solo se admite `credential_source.file` y, si se especifica `credential_source.format`, el tipo debe ser `text`.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### Opción de ID de proyecto de GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

ID de proyecto de GCS.

ID de proyecto de GCS utilizado para determinar la facturación de solicitudes.

```yaml
example: --repo1-gcs-user-project=my-project
```

### Opción de host del repositorio (`--repo-host`) {#repository-host-option---repo-host}

Host del repositorio cuando se opera de forma remota.

Cuando se hacen copias de seguridad y se archiva a un sistema de archivos montado localmente, este ajuste no es necesario.

```yaml
example: --repo1-host=repo1.domain.com
```

Nombre obsoleto: backup-host

### Opción de archivo de autoridad de certificación del host del repositorio (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Archivo de autoridad de certificación del host del repositorio.

Usa un archivo de CA distinto del predeterminado del sistema para conectarse al host del repositorio.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Opción de ruta de autoridad de certificación del host del repositorio (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Ruta de autoridad de certificación del host del repositorio.

Usa una ruta de CA distinta de la predeterminada del sistema para conectarse al host del repositorio.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### Opción de archivo de certificado del host del repositorio (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Archivo de certificado del host del repositorio.

Se envía al host del repositorio para demostrar la identidad del cliente.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### Opción de comando del host del repositorio (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

Comando pgBackRest del host del repositorio.

Solo es necesario si la ruta al comando pgBackRest es diferente en el host local y en el del repositorio. Si no se define, el comando del host del repositorio se establecerá igual que el comando local.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Nombre obsoleto: backup-cmd

### Opción de configuración del host del repositorio (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

Archivo de configuración del host del repositorio de pgBackRest.

Establece la ubicación del archivo de configuración en el host del repositorio. Solo es necesario si el archivo de configuración del host del repositorio está en una ubicación diferente a la del archivo de configuración local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Nombre obsoleto: backup-config

### Opción de ruta de inclusión de configuración del host del repositorio (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Ruta de inclusión de configuración del host del repositorio de pgBackRest.

Establece la ubicación de la ruta de inclusión de configuración en el host del repositorio. Solo es necesario si la ruta de inclusión de configuración del host del repositorio está en una ubicación diferente a la ruta de inclusión de configuración local.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Opción de ruta de configuración del host del repositorio (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

Ruta de configuración del host del repositorio de pgBackRest.

Establece la ubicación de la ruta de configuración en el host del repositorio. Solo es necesario si la ruta de configuración del host del repositorio está en una ubicación diferente a la ruta de configuración local.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### Opción de archivo de clave del host del repositorio (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Archivo de clave del host del repositorio.

Demuestra que el certificado del cliente fue enviado por su propietario.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### Opción de puerto del host del repositorio (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Puerto del host del repositorio cuando `repo-host` está establecido.

Usa esta opción para especificar un puerto no predeterminado para el protocolo del host del repositorio.

> **NOTA:** Cuando `repo-host-type=ssh` no existe un valor predeterminado para `repo-host-port`. En este caso, el puerto será el que esté configurado para el comando especificado por `cmd-ssh`.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

Nombre obsoleto: backup-ssh-port

### Opción de tipo de protocolo del host del repositorio (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Tipo de protocolo del host del repositorio.

Se soportan los siguientes tipos de protocolo:

- `ssh` - Secure Shell.
- `tls` - Servidor TLS de pgBackRest.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### Opción de usuario del host del repositorio (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Usuario del host del repositorio cuando `repo-host` está establecido.

Define el usuario que se utilizará para las operaciones en el host del repositorio. Preferiblemente no es el usuario `postgres`, sino algún otro usuario como `pgbackrest`. Si PostgreSQL se ejecuta en el host del repositorio, el usuario `postgres` puede colocarse en el grupo `pgbackrest` para que tenga permisos de lectura sobre el repositorio sin poder dañar el contenido accidentalmente.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

Nombre obsoleto: backup-user

### Opción de ruta del repositorio (`--repo-path`) {#repository-path-option---repo-path}

Ruta donde se almacenan las copias de seguridad y el archivado.

El repositorio es donde pgBackRest almacena las copias de seguridad y archiva los segmentos WAL.

Puede ser difícil estimar por adelantado cuánto espacio necesitarás. Lo mejor es hacer algunas copias de seguridad y luego registrar el tamaño de los diferentes tipos de copias de seguridad (full/incr/diff) y medir la cantidad de WAL generada por día. Esto te dará una idea general del espacio que necesitarás, aunque por supuesto los requisitos probablemente cambien con el tiempo a medida que tu base de datos evolucione.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### Opción de retención de archivado (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Cantidad de WAL continuo que se retendrá, medida en número de copias de seguridad.

> **NOTA:** Los segmentos WAL necesarios para que una copia de seguridad sea consistente siempre se retienen hasta que la copia de seguridad expira, independientemente de cómo esté configurada esta opción.

Si este valor no está establecido y `repo-retention-full-type` es `count` (predeterminado), el archivado a expirar tomará por defecto el valor de `repo-retention-full` (o `repo-retention-diff`) correspondiente a `repo-retention-archive-type` si este está establecido en `full` (o `diff`). Esto garantizará que el WAL solo expire para copias de seguridad que ya han expirado. Si `repo-retention-full-type` es `time`, este valor tomará por defecto la eliminación de los archivados anteriores a la copia completa más antigua que se retenga tras satisfacer el ajuste `repo-retention-full`.

Esta opción debe establecerse si `repo-retention-archive-type` está establecido en `incr`. Si el espacio en disco es escaso, este ajuste, junto con `repo-retention-archive-type`, puede usarse para expirar segmentos WAL de forma agresiva. Sin embargo, hacerlo anula la posibilidad de realizar PITR desde las copias de seguridad con WAL expirado y, por lo tanto, **no** se recomienda.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-archive=2
```

Nombre obsoleto: retention-archive

### Opción de tipo de retención de archivado (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Tipo de copia de seguridad para la retención de WAL.

Se admiten los siguientes tipos de copia de seguridad:

- `full` - pgBackRest conservará los registros del archivado para el número de copias completas definido por `repo-retention-archive`.
- `diff` - (diferencial) pgBackRest conservará los registros del archivado para el número de copias completas y diferenciales definido por `repo-retention-archive`, lo que significa que si la última copia de seguridad realizada fue completa, contará como diferencial a efectos de la retención del repositorio.
- `incr` - (incremental) pgBackRest conservará los registros del archivado para el número de copias completas, diferenciales e incrementales definido por `repo-retention-archive`.

Se recomienda no cambiar este ajuste del valor predeterminado, que solo expirará WAL junto con la expiración de copias completas.

```yaml
default: full
example: --repo1-retention-archive-type=diff
```

Nombre obsoleto: retention-archive-type

### Opción de retención diferencial (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Número de copias de seguridad diferenciales que se retendrán.

Cuando expira una copia de seguridad diferencial, todas las copias de seguridad incrementales asociadas a la copia diferencial también expirarán. Cuando no está definido, todas las copias de seguridad diferenciales se conservarán hasta que expiren las copias completas de las que dependen.

Ten en cuenta que las copias completas se incluyen en el recuento de copias de seguridad diferenciales a efectos de la expiración. Esto reduce ligeramente el número de copias de seguridad diferenciales que deben retenerse en la mayoría de los casos.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-diff=3
```

Nombre obsoleto: retention-diff

### Opción de retención de copias completas (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Recuento/tiempo de retención de copias completas.

Cuando expira una copia completa, todas las copias de seguridad diferenciales e incrementales asociadas a la copia completa también expirarán. Cuando la opción no está definida, se emitirá una advertencia. Si se desea una retención indefinida, establece la opción al valor máximo.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-full=2
```

Nombre obsoleto: retention-full

### Opción de tipo de retención de copias completas (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Tipo de retención de las copias completas.

Determina si el ajuste `repo-retention-full` representa un periodo de tiempo (días) o un recuento de copias completas a conservar.

Se admiten los siguientes tipos de retención:

- `time` - las copias completas más antiguas que `repo-retention-full` se eliminarán del repositorio si hay al menos otra copia de seguridad que sea igual o mayor que el ajuste `repo-retention-full`. Por ejemplo, si `repo-retention-full` es 30 (días) y hay 2 copias completas: una de 25 días y otra de 35 días, ninguna copia completa expirará, porque expirar la copia de 35 días dejaría solo la copia de 25 días, lo que violaría la política de retención de 30 días de tener al menos una copia de 30 días antes de que una más antigua pueda expirar. El WAL archivado más antiguo que la copia completa más antigua restante expirará automáticamente, a menos que `repo-retention-archive-type` y `repo-retention-archive` se establezcan explícitamente.
- `count` - las copias completas que excedan `repo-retention-full` expirarán. Por ejemplo, si `repo-retention-full` es `4` y se completa una quinta copia completa, la copia completa más antigua expirará para mantener el recuento en 4.

Ten en cuenta que una copia de seguridad debe completarse exitosamente antes de que se considere para la retención. Por ejemplo, si `repo-retention-full-type` es `count` y `repo-retention-full` es `2`, debe haber 3 copias completas completadas antes de que la más antigua se expire.

```yaml
default: count
example: --repo1-retention-full-type=time
```

### Opción de retención del historial de copias de seguridad (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Días de manifiestos del historial de copias de seguridad que se retendrán.

Una copia del manifiesto de la copia de seguridad se almacena en la ruta `backup.history` cuando una copia de seguridad se completa. Por defecto, estos archivos nunca expiran ya que son útiles para la minería de datos, p. ej., para medir el crecimiento de las copias de seguridad y del WAL a lo largo del tiempo.

Establece `repo-retention-history` para definir el número de días de manifiestos del historial de copias de seguridad que se retendrán. Las copias de seguridad no expiradas siempre se conservan en el historial de copias de seguridad. Especifica `repo-retention-history=0` para conservar el historial de copias de seguridad solo para las copias no expiradas.

Cuando expira un manifiesto del historial de una copia completa, todos los manifiestos del historial de copias de seguridad diferenciales e incrementales asociados a la copia completa también expiran.

```yaml
allowed: [0, 9999999]
example: --repo1-retention-history=365
```

### Opción de bucket de repositorio de S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

Bucket de repositorio de S3.

Bucket de S3 utilizado para almacenar el repositorio.

Los repositorios de pgBackRest pueden almacenarse en la raíz del bucket estableciendo `repo-path=/`, pero normalmente es mejor especificar un prefijo, como `/repo`, para que los registros y otro contenido generado por AWS también puedan almacenarse en el bucket.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### Opción de endpoint de repositorio de S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

Endpoint del repositorio de S3.

El endpoint de AWS debe ser válido para la región seleccionada.

Para configuraciones personalizadas o de prueba, las opciones `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` y `repo-storage-verify-tls` pueden ser útiles.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### Opción de tipo de clave de repositorio de S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

Tipo de clave del repositorio de S3.

Se admiten los siguientes tipos de autorización:

- `shared` - Claves compartidas
- `auto` - Obtener automáticamente credenciales temporales
- `web-id` - Obtener automáticamente credenciales de identidad web
- `pod-id` - Obtener automáticamente credenciales de identidad de pod de EKS
- `process` - Obtener credenciales ejecutando un proceso

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### Opción de ID de clave KMS de repositorio de S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

Clave KMS del repositorio de S3.

Activa el cifrado en el lado del servidor de S3 usando la clave especificada del servicio de gestión de claves de AWS.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Opción de comando de proceso de autenticación de S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Comando de proceso de autenticación de S3.

Comando (y argumentos opcionales) a ejecutar para obtener credenciales temporales de S3. La primera entrada de la lista es el comando y las entradas restantes se pasan como parámetros.

El proceso debe generar una salida JSON que contenga los campos `AccessKeyId`, `SecretAccessKey`, `SessionToken` y `Expiration`. Las credenciales se actualizarán automáticamente antes del tiempo de expiración. Consulta [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) para obtener detalles del formato.

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### Opción de región de repositorio de S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

Región del repositorio de S3.

La región de AWS donde se creó el bucket.

```yaml
example: --repo1-s3-region=us-east-1
```

### Opción de pago del solicitante del repositorio de S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Pago del solicitante del repositorio de S3.

Activa el pago del solicitante de S3.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### Opción de rol de repositorio de S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

Rol del repositorio de S3.

El nombre del rol de AWS (no el ARN completo) utilizado para obtener credenciales temporales cuando `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### Opción de servicio de repositorio de S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

Servicio de firma de S3.

El servicio de firma de S3 utilizado en la autenticación SigV4. Por defecto es `s3` para los endpoints S3 estándar. Establécelo en `s3-outposts` cuando se use un endpoint de S3 Outposts.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### Opción de endpoint STS de repositorio de S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

Endpoint STS del repositorio de S3.

El endpoint de STS utilizado para obtener credenciales temporales cuando se configura `repo-s3-key-type=web-id`. Establécelo en un endpoint regional (p. ej., `sts.us-east-1.amazonaws.com`) para usar STS regional, lo que puede ser necesario para GovCloud, las regiones de China, o para reducir la latencia.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Opción de estilo de URI de repositorio de S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

Estilo de URI de S3.

Se soportan los siguientes estilos de URI:

- `host` - Conectar al host `bucket.endpoint`.
- `path` - Conectar al host `endpoint` y anteponer el bucket a los URI.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### Opción de host del repositorio SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

Host del repositorio SFTP.

El host SFTP que contiene el repositorio.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### Opción de huella del host del repositorio SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Huella del host del repositorio SFTP.

La generación de la huella del host del repositorio SFTP debe coincidir con `repo-sftp-host-key-hash-type`. Genera la huella mediante `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. Las claves de host de ssh se encuentran normalmente en el directorio `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Opción de tipo de comprobación de clave de host SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Tipo de comprobación de clave de host SFTP.

Se soportan los siguientes tipos de comprobación de clave de host SFTP:

- `strict` - pgBackRest nunca añadirá claves de host automáticamente al archivo ~/.ssh/known_hosts y se niega a conectarse a hosts cuya clave de host haya cambiado o no se encuentre en los archivos de hosts conocidos. Esta opción obliga al usuario a añadir manualmente todos los hosts nuevos.
- `accept-new` - pgBackRest añadirá automáticamente nuevas claves de host al archivo de hosts conocidos del usuario, pero no permitirá conexiones a hosts con claves de host modificadas.
- `fingerprint` - pgBackRest comprobará la clave de host contra la huella especificada por la opción `repo-sftp-host-fingerprint`.
- `none` - no se realizará ninguna comprobación de clave de host.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### Opción de tipo de hash de clave de host del repositorio SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Tipo de hash de clave de host del repositorio SFTP.

Declara el tipo de hash que se usa para calcular el resumen de la clave de host del sistema remoto al iniciar SSH. Los valores permitidos son `md5`, `sha1` y `sha256`, aunque solo las versiones más recientes de `libssh2` admiten `sha256`.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### Opción de puerto del host del repositorio SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Puerto del host del repositorio SFTP.

Puerto del host del repositorio SFTP.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### Opción de usuario del host del repositorio SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Usuario del host del repositorio SFTP.

Usuario en el host utilizado para almacenar el repositorio.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### Opción de archivo de hosts conocidos SFTP (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Archivo de hosts conocidos SFTP.

Un archivo de hosts conocidos para buscar una coincidencia de host SFTP durante la autenticación. Si no se especifica, pgBackRest buscará por defecto en `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` y `/etc/ssh/ssh_known_hosts2`. Si se configura con una o más rutas de archivos, pgBackRest buscará en ellas una coincidencia. Las rutas de archivos deben ser rutas completas o rutas que comiencen por una virgulilla (~). La opción `repo-sftp-known-host` puede pasarse varias veces para especificar más de un archivo de hosts conocidos en el que buscar. Para utilizar la comprobación del archivo de hosts conocidos no debe especificarse `repo-sftp-host-fingerprint`. Consulta también la opción `repo-sftp-host-check-type`.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Opción de archivo de clave privada del repositorio SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Archivo de clave privada SFTP.

Archivo de clave privada SFTP utilizado para la autenticación.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Opción de archivo de clave pública del repositorio SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Archivo de clave pública SFTP.

Archivo de clave pública SFTP utilizado para la autenticación. Es opcional si se compiló contra OpenSSL y obligatorio si se compiló contra una biblioteca diferente.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Opción de archivo de CA del almacenamiento del repositorio (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

Archivo de CA del almacenamiento del repositorio.

Usa un archivo de CA distinto del predeterminado del sistema para los certificados del almacenamiento (p. ej., S3, Azure).

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Nombres obsoletos: repo-azure-ca-file, repo-s3-ca-file

### Opción de ruta de CA TLS del almacenamiento del repositorio (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

Ruta de CA del almacenamiento del repositorio.

Usa una ruta de CA distinta de la predeterminada del sistema para los certificados del almacenamiento (p. ej., S3, Azure).

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

Nombres obsoletos: repo-azure-ca-path, repo-s3-ca-path

### Opción de host de almacenamiento del repositorio (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Host de almacenamiento del repositorio.

Conéctate a un host distinto del endpoint del almacenamiento (p. ej., S3, Azure). Esto se utiliza normalmente para pruebas.

```yaml
example: --repo1-storage-host=127.0.0.1
```

Nombres obsoletos: repo-azure-host, repo-s3-host

### Opción de puerto de almacenamiento del repositorio (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Puerto de almacenamiento del repositorio.

Puerto a utilizar al conectarse al endpoint del almacenamiento (p. ej., S3, Azure) (o al host si se especificó).

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

Nombres obsoletos: repo-azure-port, repo-s3-port

### Opción de lectura anticipada del almacenamiento del repositorio (`--repo-storage-prefetch`) {#repository-storage-prefetch-option---repo-storage-prefetch}

Lectura anticipada del almacenamiento del repositorio.

Determina el número de solicitudes que se envían por adelantado al leer de almacenes de objetos, como S3. No es concurrencia real, pero reduce la latencia asociada al envío de solicitudes.

El número de solicitudes abiertas por lectura es uno mayor que el valor de lectura anticipada, ya que la lectura inicial no puede anticiparse.

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### Opción de lectura continua sobre datos innecesarios del almacenamiento del repositorio (`--repo-storage-read-over`) {#repository-storage-read-over-option---repo-storage-read-over}

Lectura continua sobre datos innecesarios del almacenamiento del repositorio.

Los paquetes pueden contener datos que no se necesitan durante la restauración, por ejemplo archivos que ya existen. Esta opción omite esos datos continuando la lectura, sin iniciar una nueva solicitud al almacén de objetos. Suele ser más rápido, ya que la latencia de las nuevas solicitudes de lectura es mayor que la de continuar una lectura en curso. También es menos costoso para la mayoría de las clases de almacenamiento.

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

### Opción de etiqueta de almacenamiento del repositorio (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Etiqueta(s) de almacenamiento del repositorio.

Especifica etiquetas que se añadirán a los objetos cuando el repositorio sea un almacén de objetos (p. ej., S3). La opción puede repetirse para añadir múltiples etiquetas.

pgBackRest no ofrece ninguna forma de modificar estas etiquetas, así que asegúrate de establecerlas correctamente antes de ejecutar `stanza-create` para garantizar etiquetas uniformes en todo el repositorio.

```yaml
example: --repo1-storage-tag=key1=value1
```

### Opción de tamaño de fragmento de subida del almacenamiento del repositorio (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Tamaño de fragmento de subida del almacenamiento del repositorio.

Los almacenes de objetos como S3 permiten subir archivos en fragmentos cuando el archivo es demasiado grande para guardarse en memoria. Aunque el archivo pueda guardarse en memoria, es más eficiente limitar la cantidad de memoria utilizada para las subidas.

Un tamaño de fragmento mayor generalmente dará mejor rendimiento porque minimizará las solicitudes de subida y permitirá subir más archivos en una sola solicitud en lugar de en fragmentos. La desventaja es que el uso de memoria será mayor y, como el búfer de fragmentos debe asignarse por proceso, valores más altos de `process-max` provocarán un mayor consumo de memoria en general.

Ten en cuenta que los tamaños de fragmento válidos varían según el tipo de almacenamiento y la plataforma. Por ejemplo, AWS S3 tiene un tamaño de fragmento mínimo de 5MiB. La terminología para el tamaño de fragmento varía según el tipo de almacenamiento, así que al buscar los valores mínimo/máximo usa «part size» para AWS S3, «chunk size» para GCS y «block size» para Azure.

Si un archivo es mayor de 1GiB (el tamaño máximo que PostgreSQL creará por defecto), el tamaño de fragmento se incrementará gradualmente hasta el máximo permitido para completar la subida del archivo.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### Opción de verificación de certificado del almacenamiento del repositorio (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Verificación del certificado del almacenamiento del repositorio.

Esta opción ofrece la posibilidad de activar/desactivar la verificación del certificado TLS del servidor de almacenamiento (p. ej., S3, Azure). La desactivación solo debería usarse para pruebas u otros escenarios donde un certificado haya sido autofirmado.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

Nombres obsoletos: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Opción de enlaces simbólicos del repositorio (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Crea enlaces simbólicos dentro del repositorio.

Activa la creación de los enlaces simbólicos `latest` y de tablespaces. Estos enlaces simbólicos son más útiles cuando se usan instantáneas para hacer una recuperación in situ en el repositorio, que es un caso de uso poco común.

Aunque es probable que esta función no sea útil para la gran mayoría de los usuarios, permanece activada por defecto por razones de compatibilidad con versiones anteriores. Sin embargo, puede ser útil desactivar los enlaces simbólicos para almacenamientos tipo Posix que no los soportan.

```yaml
default: y
example: --no-repo1-symlink
```

### Opción de tipo de repositorio (`--repo-type`) {#repository-type-option---repo-type}

Tipo de almacenamiento utilizado para el repositorio.

Se soportan los siguientes tipos de repositorio:

- `azure` - Azure Blob Storage Service
- `cifs` - Como `posix`, pero desactiva los enlaces y los fsync de directorios
- `gcs` - Google Cloud Storage
- `posix` - Sistemas de archivos compatibles con Posix
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

Cuando se utiliza un montaje NFS como repositorio `posix`, se aplican a pgBackRest las mismas reglas descritas en la documentación de PostgreSQL: [Creación de un clúster de bases de datos - Sistemas de archivos](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```yaml
default: posix
example: --repo1-type=cifs
```
