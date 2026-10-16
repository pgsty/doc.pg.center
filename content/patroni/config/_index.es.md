---
title: "Configuración de Patroni"
weight: 30
icon: fa-solid fa-code
description: "Modelo de configuración de Patroni, reglas de precedencia y herramientas de validación."
sidebar_expanded: true
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/patroni_configuration.html"
---

<a id="config"></a>
Hay 3 tipos de configuración de Patroni:

- [Configuración dinámica](/es/patroni/config/dynamic#dynamic) global.  
  Estas opciones se almacenan en el DCS (Distributed Configuration Store) y se aplican en todos los nodos del clúster. La configuración dinámica puede establecerse en cualquier momento utilizando la herramienta [patronictl_edit_config](/es/patroni/patronictl#patronictl_edit_config) o la [REST API](/es/patroni/rest_api#rest_api) de Patroni. Si las opciones modificadas no forman parte de la configuración de arranque, se aplican de forma asíncrona (en el siguiente ciclo de activación) a cada nodo, que posteriormente se recarga. Si el nodo requiere un reinicio para aplicar la configuración (para [parámetros de PostgreSQL](https://www.postgresql.org/docs/current/view-pg-settings.html) con contexto postmaster, si sus valores han cambiado), se establece un indicador especial `pending_restart` en el JSON members.data. Además, el estado del nodo lo indica mostrando `"restart_pending": true`.

- [Archivo de configuración](/es/patroni/config/yaml#yaml) local (patroni.yml).  
  Estas opciones se definen en el archivo de configuración y tienen precedencia sobre la configuración dinámica. `patroni.yml` puede modificarse y recargarse en tiempo de ejecución (sin reiniciar Patroni) enviando SIGHUP al proceso de Patroni, realizando una solicitud `POST /reload` a la REST-API o ejecutando [patronictl_reload](/es/patroni/patronictl#patronictl_reload). La configuración local puede ser un único archivo YAML o un directorio. Cuando es un directorio, todos los archivos YAML de ese directorio se cargan uno por uno en orden alfabético. En caso de que una clave esté definida en varios archivos, la aparición en el último archivo tiene precedencia.

- [Configuración por entorno](/es/patroni/config/env#env).  
  Es posible establecer/sobrescribir algunos de los parámetros de configuración «local» con variables de entorno. La configuración por entorno es muy útil cuando se ejecuta en un entorno dinámico y no se conocen algunos parámetros por adelantado (por ejemplo, no es posible conocer tu dirección IP externa cuando se ejecuta dentro de `docker`).

<a id="important_configuration_rules"></a>

--------

## Reglas importantes {#important-rules}

### Parámetros de PostgreSQL controlados por Patroni {#postgresql-parameters-controlled-by-patroni}

Algunos de los parámetros de PostgreSQL **deben tener los mismos valores en el primario y en las réplicas**. Para aquellos, **los valores establecidos en los archivos locales de configuración de patroni o mediante las variables de entorno no tienen efecto**. Para alterar o establecer sus valores se debe cambiar la configuración compartida en el DCS. A continuación se muestra la lista real de tales parámetros junto con los valores predeterminados y mínimos:

- **max_connections**: valor predeterminado 100, valor mínimo 25
- **max_locks_per_transaction**: valor predeterminado 64, valor mínimo 32
- **max_worker_processes**: valor predeterminado 8, valor mínimo 2
- **max_prepared_transactions**: valor predeterminado 0, valor mínimo 0
- **wal_level**: valor predeterminado hot_standby, valores aceptados: hot_standby, replica, logical
- **track_commit_timestamp**: valor predeterminado off

Para los parámetros siguientes, PostgreSQL no requiere valores iguales entre el primario y todas las réplicas. Sin embargo, considerando la posibilidad de que una réplica se convierta en el primario en cualquier momento, en realidad no tiene sentido establecerlos de forma diferente; por lo tanto, **Patroni restringe el establecimiento de sus valores a la** [configuración dinámica](/es/patroni/config/dynamic#dynamic).

- **max_wal_senders**: valor predeterminado 10, valor mínimo 3
- **max_replication_slots**: valor predeterminado 10, valor mínimo 4
- **wal_keep_segments**: valor predeterminado 8, valor mínimo 1
- **wal_keep_size**: valor predeterminado 128MB, valor mínimo 16MB
- **wal_log_hints**: on

Estos parámetros se validan para garantizar que sean razonables o que cumplan un valor mínimo.

Hay algunos otros parámetros de Postgres controlados por Patroni:

- **listen_addresses** - se establece desde `postgresql.listen` o desde la variable de entorno `PATRONI_POSTGRESQL_LISTEN`
- **port** - se establece desde `postgresql.listen` o desde la variable de entorno `PATRONI_POSTGRESQL_LISTEN`
- **cluster_name** - se establece desde `scope` o desde la variable de entorno `PATRONI_SCOPE`
- **hot_standby: on**

Para estar del lado seguro, los parámetros de las listas anteriores se escriben en `postgresql.conf` y se pasan como una lista de argumentos al `postgres`, lo que les da la máxima precedencia (excepto `wal_keep_segments` y `wal_keep_size`), incluso por encima de [ALTER SYSTEM](https://www.postgresql.org/docs/current/static/sql-altersystem.html)

También hay algunos parámetros como **postgresql.listen**, **postgresql.data_dir** que **solo pueden establecerse localmente**, es decir, en el [archivo de configuración](/es/patroni/config/yaml#yaml) de Patroni o mediante la variable de [configuración](/es/patroni/config/env#env) por entorno. En la mayoría de los casos la configuración local sobrescribirá la configuración dinámica.

Al aplicar las opciones de configuración local o dinámica, se realizan las siguientes acciones:

- El nodo primero comprueba si hay un archivo `postgresql.base.conf` o si el parámetro `custom_conf` está establecido.
- Si el parámetro `custom_conf` está establecido, el archivo que especifica se utiliza como configuración base, ignorando `postgresql.base.conf` y `postgresql.conf`.
- Si el parámetro `custom_conf` no está establecido y existe `postgresql.base.conf`, este contiene la configuración «original» renombrada y se utiliza como configuración base.
- Si no hay `custom_conf` ni `postgresql.base.conf`, el `postgresql.conf` original se renombra a `postgresql.base.conf` y se utiliza como configuración base.
- Las opciones dinámicas (con las excepciones anteriores) se vuelcan en `postgresql.conf` y se establece un include en `postgresql.conf` hacia la configuración base (ya sea `postgresql.base.conf` o el archivo en `custom_conf`). Por lo tanto, podríamos aplicar nuevas opciones sin volver a leer el archivo de configuración para comprobar si el include está presente o no.
- Algunos parámetros esenciales para que Patroni gestione el clúster se sobrescriben mediante la línea de comandos.
- Si se cambia una opción que requiere reinicio (debemos mirar el contexto en pg_settings y los valores reales de esas opciones), se establece un indicador pending_restart en ese nodo. Este indicador se restablece en cualquier reinicio.

Los parámetros se aplicarían en el siguiente orden (los de tiempo de ejecución reciben la máxima prioridad):

1.  cargar parámetros del archivo `postgresql.base.conf` (o de un archivo `custom_conf`, si está establecido)
2.  cargar parámetros del archivo `postgresql.conf`
3.  cargar parámetros del archivo `postgresql.auto.conf`
4.  parámetro en tiempo de ejecución mediante `-o --name=value`

Esto permite la configuración de todos los nodos (2), la configuración de un nodo específico mediante `ALTER SYSTEM` (3) y garantiza que los parámetros esenciales para la ejecución de Patroni se impongan (4), además de dejar margen para herramientas de configuración que gestionan `postgresql.conf` directamente sin involucrar a Patroni (1).

<a id="shared_memory_gucs"></a>

### Parámetros de PostgreSQL que afectan a la memoria compartida {#postgresql-parameters-that-touch-shared-memory}

PostgreSQL tiene algunos parámetros que determinan el tamaño de la memoria compartida utilizada por ellos:

- **max_connections**
- **max_prepared_transactions**
- **max_locks_per_transaction**
- **max_wal_senders**
- **max_worker_processes**

Cambiar estos parámetros requiere un reinicio de PostgreSQL para que surtan efecto, y sus estructuras de memoria compartida no pueden ser más pequeñas en los nodos en espera que en el nodo primario.

Como se explicó antes, Patroni restringe el cambio de sus valores mediante la [configuración dinámica](/es/patroni/config/dynamic#dynamic), lo que normalmente consiste en:

1.  Aplicar cambios mediante [patronictl_edit_config](/es/patroni/patronictl#patronictl_edit_config) (o mediante el endpoint `/config` de la REST API)
2.  Reiniciar nodos mediante [patronictl_restart](/es/patroni/patronictl#patronictl_restart) (o mediante el endpoint `/restart` de la REST API)

**Nota:** ten en cuenta que deberías realizar un reinicio de los nodos de PostgreSQL mediante el comando [patronictl_restart](/es/patroni/patronictl#patronictl_restart), o mediante el endpoint `/restart` de la REST API. Un intento de reiniciar PostgreSQL reiniciando el demonio de Patroni, por ejemplo ejecutando `systemctl restart patroni`, puede provocar una conmutación por error en el clúster, si estás reiniciando el nodo primario.

Sin embargo, como esos ajustes gestionan memoria compartida, se debe tener un cuidado adicional al reiniciar los nodos:

- Si quieres **aumentar** el valor de cualquiera de esos ajustes:

  > 1.  Reinicia primero todos los nodos en espera
  > 2.  Reinicia el primario después

- Si quieres **disminuir** el valor de cualquiera de esos ajustes:

  > 1.  Reinicia primero el primario
  > 2.  Reinicia todos los nodos en espera después

**Nota:** si intentas reiniciar todos los nodos de una sola vez después de **disminuir** el valor de cualquiera de esos ajustes, Patroni ignorará el cambio y reiniciará el nodo en espera con el valor original del ajuste, lo que requerirá que reinicies los nodos en espera de nuevo más tarde. Patroni hace eso para evitar que el nodo en espera entre en un bucle de caídas infinito, porque PostgreSQL termina con un mensaje `FATAL` si intentas establecer cualquiera de esos parámetros en un valor inferior al visible en `pg_controldata` en el nodo en espera. En otras palabras, solo podemos disminuir el ajuste en el nodo en espera una vez que su `pg_controldata` esté actualizado respecto al primario en lo referente a estos cambios en el primario.

Más información al respecto puede encontrarse en la [visión general para el administrador de PostgreSQL](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN).

### Parámetros de configuración de Patroni {#patroni-configuration-parameters}

Además, las siguientes opciones de configuración de Patroni **solo pueden cambiarse dinámicamente**:

- **ttl**: 30
- **loop_wait**: 10
- **retry_timeout**: 10
- **maximum_lag_on_failover**: 1048576
- **max_timelines_history**: 0
- **check_timeline**: false
- **postgresql.use_slots**: true

Al cambiar estas opciones, Patroni leerá la sección correspondiente de la configuración almacenada en el DCS y cambiará sus valores en tiempo de ejecución.

Los nodos de Patroni guardan la configuración del DCS en disco después de cada cambio de configuración, en el archivo `patroni.dynamic.json` ubicado en el directorio de datos de Postgres. Solo el líder puede restaurar estas opciones desde el volcado en disco si están completamente ausentes del DCS o si no son válidas.

<a id="validate_generate_config"></a>

--------

## Generación y validación de la configuración {#configuration-generation-and-validation}

Patroni proporciona interfaces de línea de comandos para la generación y validación de una [configuración local](/es/patroni/config/yaml#yaml) de Patroni. Utilizando el ejecutable `patroni` puedes:

- Crear una configuración local de ejemplo de Patroni;
- Crear un archivo de configuración de Patroni para la instancia de PostgreSQL que se ejecuta localmente (por ejemplo, como paso de preparación para la [integración de Patroni](/es/patroni/existing_data#existing_data));
- Validar un archivo de configuración de Patroni dado.

<a id="generate_sample_config"></a>

### Configuración de ejemplo de Patroni {#sample-patroni-configuration}

```text
patroni --generate-sample-config [configfile]
```

#### Descripción {#description}

Genera un archivo de configuración de ejemplo de Patroni en formato `yaml`. Los valores de los parámetros se definen mediante la [configuración por entorno](/es/patroni/config/env#env); de lo contrario, si no están establecidos, los valores predeterminados utilizados en Patroni o la cadena `#FIXME` para los valores que el usuario debería definir más tarde.

Algunos valores predeterminados se definen en función de la configuración local:

> - **postgresql.listen**: la dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `5432`.
> - **postgresql.connect_address**: la dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `5432`.
> - **postgresql.authentication.rewind**: solo se define si la versión de PostgreSQL puede determinarse a partir del binario y la versión es 11 o posterior.
> - **restapi.listen**: dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `8008`.
> - **restapi.connect_address**: dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `8008`.

#### Parámetros {#parameters}

`configfile` - ruta completa del archivo de configuración utilizado para almacenar el resultado. Si no se proporciona, el resultado se envía a `stdout`.

<a id="generate_config"></a>

### Configuración de Patroni para una instancia en ejecución {#patroni-configuration-for-a-running-instance}

```text
patroni --generate-config [--dsn DSN] [configfile]
```

#### Descripción {#description-1}

Genera una configuración de Patroni en formato `yaml` para la instancia de PostgreSQL que se ejecuta localmente. Para la conexión a PostgreSQL se utilizará el DSN proporcionado (tiene precedencia) o las [variables de entorno](https://www.postgresql.org/docs/current/libpq-envars.html) de PostgreSQL. Si no se proporciona la contraseña, debería introducirse mediante un prompt.

Todos los GUC no internos definidos en la instancia de Postgres de origen, independientemente de si se establecieron mediante un archivo de configuración, mediante la línea de comandos del postmaster o mediante variables de entorno, se utilizarán como fuente de los siguientes parámetros de configuración de Patroni:

> - **scope**: valor del GUC `cluster_name`;
> - **postgresql.listen**: valores de los GUC `listen_addresses` y `port`;
> - **postgresql.data_dir**: valor del GUC `data_directory`;
> - **postgresql.parameters**: valores de los GUC `archive_command`, `restore_command`, `archive_cleanup_command`, `recovery_end_command`, `ssl_passphrase_command`, `hba_file`, `ident_file`, `config_file`;
> - **bootstrap.dcs**: todos los demás GUC de PostgreSQL recopilados.

Si `scope`, `postgresql.listen` o `postgresql.data_dir` no están establecidos desde los GUC de Postgres, se utiliza el valor respectivo de la [configuración por entorno](/es/patroni/config/env#env).

Otras reglas aplicadas para la definición de los valores:

> - **name**: valor de la variable de entorno `PATRONI_NAME` si está establecida; de lo contrario, el nombre de host de la máquina actual.
> - **postgresql.bin_dir**: ruta a los binarios de Postgres recopilada de la instancia en ejecución.
> - **postgresql.connect_address**: la dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto utilizado para la conexión a la instancia o el valor del GUC `port`.
> - **postgresql.authentication.superuser**: la configuración utilizada para la conexión a la instancia;
> - **postgresql.pg_hba**: las líneas recopiladas del `hba_file` de la instancia de origen.
> - **postgresql.pg_ident**: las líneas recopiladas del `ident_file` de la instancia de origen.
> - **restapi.listen**: dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `8008`.
> - **restapi.connect_address**: dirección IP resuelta por `getaddrinfo` a partir del nombre de host de la máquina actual devuelto por `gethostname` y el puerto estándar `8008`.

Otros parámetros definidos mediante la [configuración por entorno](/es/patroni/config/env#env) también se incluyen en la configuración.

#### Parámetros {#parameters-1}

`configfile`  
Ruta completa del archivo de configuración utilizado para almacenar el resultado. Si no se proporciona, el resultado se envía a `stdout`.

`dsn`  
Cadena DSN opcional para la instancia local de PostgreSQL de la que obtener los valores de los GUC.

### Validar la configuración de Patroni {#validate-patroni-configuration}

```text
patroni --validate-config [configfile] [--ignore-listen-port | -i]
```

#### Descripción {#description-2}

Valida la configuración de Patroni dada e imprime la información sobre las comprobaciones fallidas.

#### Parámetros {#parameters-2}

`configfile`  
Ruta completa del archivo de configuración a comprobar. Si no se da o el archivo no existe, intentará leer desde la variable de entorno `PATRONI_CONFIGURATION` o, si no está establecida, desde las [variables de entorno de Patroni](/es/patroni/config/env#env).

`--ignore-listen-port | -i`  
Flag opcional para ignorar los fallos de vinculación de los puertos `listen` que ya están en uso al validar el `configfile`.

`--print | -p`  
Flag opcional para imprimir la configuración local (incluidas las sobrescrituras de la configuración por entorno) después de que se haya validado con éxito.
