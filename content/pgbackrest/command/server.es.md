---
title: "Comando de servidor (server)"
linkTitle: "server"
weight: 120
description: "Referencia de las opciones y el comportamiento del comando `server` de pgBackRest."
icon: fa-solid fa-server
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/command.html#command-server"
---

El servidor de pgBackRest permite el acceso a hosts remotos sin utilizar el protocolo SSH.

## Opciones del comando {#command-options}

### Opción de dirección del servidor TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

Dirección del servidor TLS.

Dirección IP en la que el servidor escuchará las solicitudes de los clientes.

```yaml
default: localhost
example: --tls-server-address=*
```

### Opción de clientes autorizados del servidor TLS (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

Clientes autorizados del servidor TLS.

Los clientes se autorizan en el servidor verificando su certificado y comprobando el CN (Common Name) de su certificado contra una lista en el servidor configurada con la opción `tls-server-auth`.

Un CN de cliente puede autorizarse para tantos stanzas como sea necesario proporcionando una lista separada por comas a la opción `tls-server-auth`, o para todos los stanzas especificando `tls-server-auth=client-cn=*`. No se pueden especificar comodines para el CN del cliente.

```yaml
example: --tls-server-auth=client-cn=stanza1,stanza2
```

### Opción de autoridades de certificación del servidor TLS (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

Autoridades de certificación del servidor TLS.

Comprueba que los certificados de los clientes estén firmados por una autoridad de certificación de confianza.

```yaml
example: --tls-server-ca-file=/path/to/server.ca
```

### Opción de certificado del servidor TLS (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

Archivo de certificado del servidor TLS.

Se envía al cliente para mostrar la identidad del servidor.

```yaml
example: --tls-server-cert-file=/path/to/server.crt
```

### Opción de clave del servidor TLS (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

Archivo de clave del servidor TLS.

Demuestra que el certificado del servidor fue enviado por su propietario.

```yaml
example: --tls-server-key-file=/path/to/server.key
```

### Opción de puerto del servidor TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

Puerto del servidor TLS.

Puerto en el que el servidor escuchará las solicitudes de los clientes.

```yaml
default: 8432
allowed: [1, 65535]
example: --tls-server-port=8000
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

### Opción de tiempo de espera de E/S (`--io-timeout`) {#io-timeout-option---io-timeout}

Tiempo de espera de E/S.

Tiempo de espera, en segundos, utilizado para conexiones y operaciones de lectura/escritura.

Ten en cuenta que la operación de lectura/escritura completa no necesita terminar dentro de este tiempo de espera, pero debe haber *algún* progreso, aunque sea un solo byte.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
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

### Opción de nivel de registro en error estándar (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

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

### Opción de marca de tiempo del registro (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Activa la marca de tiempo en el registro.

Activa la marca de tiempo en el registro de consola y de archivo. Esta opción se desactiva en situaciones especiales, como la generación de documentación.

```yaml
default: y
example: --no-log-timestamp
```
