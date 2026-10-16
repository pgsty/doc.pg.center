---
title: "Imágenes de réplicas y bootstrap"
linkTitle: "Bootstrap de réplicas"
weight: 60
icon: fa-solid fa-boxes-stacked
description: "Imágenes de réplicas, bootstrap y flujos de trabajo de creación de réplicas personalizadas."
module: [PATRONI]
categories: [Tarea]
upstream_link: "https://patroni.readthedocs.io/en/latest/replica_bootstrap.html"
---

<a id="replica_imaging_and_bootstrap"></a>
Patroni permite personalizar la creación de una réplica nueva. También admite definir qué sucede cuando se hace el bootstrap del nuevo clúster vacío. La distinción entre ambos está bien definida: Patroni crea réplicas solo si la clave `initialize` está presente en el DCS para el clúster. Si no hay clave `initialize`, Patroni invoca el bootstrap exclusivamente en el primer nodo que toma el bloqueo de la clave initialize.

<a id="custom_bootstrap"></a>

--------

## Bootstrap {#bootstrap}

PostgreSQL proporciona el comando `initdb` para inicializar un clúster nuevo y Patroni lo ejecuta de forma predeterminada. En ciertos casos, en particular al crear un clúster nuevo como copia de uno existente, es necesario reemplazar el método integrado por acciones personalizadas. Patroni admite la ejecución de scripts definidos por el usuario para hacer el bootstrap de clústeres nuevos, suministrándoles algunos argumentos requeridos, es decir, el nombre del clúster y la ruta al directorio de datos. Esto se configura en la sección `bootstrap` de la configuración de Patroni. Por ejemplo:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script> [param1 [, ...]]
        keep_existing_recovery_conf: False
        no_params: False
        recovery_conf:
            recovery_target_action: promote
            recovery_target_timeline: latest
            restore_command: <method_specific_restore_command>
```

Cada método de bootstrap personalizado debe tener el nombre indicado por el ajuste `method` y definir un `command` en la sección que lleva ese nombre. Existe un método especial `initdb` para invocar el comportamiento predeterminado; en ese caso el parámetro `method` puede omitirse por completo. El `command` puede usar una ruta absoluta, una ruta relativa al directorio de trabajo de Patroni o un nombre de comando disponible en `PATH`. Además de los parámetros fijos definidos en los archivos de configuración, Patroni suministra dos parámetros específicos del clúster:

`--scope`  
Nombre del clúster sobre el que se hará el bootstrap

`--datadir`  
Ruta al directorio de datos de la instancia del clúster sobre la que se hará el bootstrap

El paso de estas dos flags adicionales puede deshabilitarse estableciendo el parámetro especial `no_params` en `True`.

Si el script de bootstrap devuelve `0`, Patroni intenta configurar e iniciar la instancia de PostgreSQL producida por este. Si alguno de los pasos intermedios falla, o el script devuelve un valor distinto de cero, Patroni asume que el bootstrap ha fallado, realiza su propia limpieza y libera el bloqueo initialize para darle a otro nodo la oportunidad de hacer el bootstrap.

Si se define un bloque `recovery_conf` en la misma sección que el método de bootstrap personalizado, Patroni generará un `recovery.conf` antes de iniciar la instancia recién inicializada (o establecerá los ajustes de recuperación en la configuración de Postgres si se ejecuta PostgreSQL \>= 12). Normalmente, dicha configuración de recuperación debe contener al menos uno de los parámetros `recovery_target_*`, junto con `recovery_target_action` establecido en `promote`.

Si `keep_existing_recovery_conf` está definido y establecido en `True`, Patroni no eliminará el archivo `recovery.conf` existente si este existe (PostgreSQL \<= 11). De igual manera, en ese caso Patroni no eliminará el `recovery.signal` o el `standby.signal` existente si alguno existe, ni sobrescribirá los ajustes de recuperación configurados (PostgreSQL \>= 12). Esto es útil al hacer el bootstrap desde una copia de seguridad con herramientas como pgBackRest que generan por ti la configuración de recuperación adecuada.

Además de eso, cualquier par clave/valor adicional indicado en la configuración del método de bootstrap personalizado se pasará como argumentos al `command` en el formato `--name=value`. Por ejemplo:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script>
        arg1: value1
        arg2: value2
```

Hace que el `command` configurado se invoque también con los argumentos de línea de comandos `--arg1=value1 --arg2=value2`.

> [!NOTE]
> Los métodos de bootstrap ni se encadenan entre sí ni recurren al predeterminado en caso de que el principal falle

Como ejemplo, puedes hacer el bootstrap de un clúster nuevo de Patroni desde una copia de seguridad de Barman con una configuración como esta:

```yaml
bootstrap:
    method: barman
    barman:
        keep_existing_recovery_conf: true
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
```

> [!NOTE]
> `patroni_barman recover` requiere que tengas tanto Barman como `pg-backup-api` configurados en el host de Barman, de modo que pueda ejecutar un `barman recover` remoto a través de la API de copia de seguridad. El ejemplo anterior usa un subconjunto de los parámetros disponibles. Puedes obtener más información ejecutando `patroni_barman recover --help`.

<a id="custom_replica_creation"></a>

--------

## Construcción de réplicas {#building-replicas}

Patroni utiliza el contrastado y probado `pg_basebackup` para crear réplicas nuevas. Requiere una instancia de PostgreSQL de origen en ejecución y no proporciona limpieza integrada para los archivos de copia de seguridad obsoletos. Algunas personas prefieren otras soluciones de copia de seguridad, como `WAL-E`, `pgBackRest`, `Barman` y otras, o simplemente escriben sus propios scripts. Para acomodar todos estos casos de uso, Patroni admite la ejecución de scripts personalizados para clonar una réplica nueva. Estos se configuran en el bloque de configuración `postgresql`:

```yaml
postgresql:
    create_replica_methods:
        - <method name>
    <method name>:
        command: <command name>
        keep_data: True
        no_params: True
        no_leader: 1
```

ejemplo: wal_e

```yaml
postgresql:
    create_replica_methods:
        - wal_e
        - basebackup
    wal_e:
        command: patroni_wale_restore
        no_leader: 1
        envdir: '{{WALE_ENV_DIR}}'
        use_iam: 1
    basebackup:
        max-rate: '100M'
```

ejemplo: pgbackrest

```yaml
postgresql:
    create_replica_methods:
        - pgbackrest
        - basebackup
    pgbackrest:
        command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
        keep_data: True
        no_params: True
    basebackup:
        max-rate: '100M'
```

ejemplo: Barman

```yaml
postgresql:
    create_replica_methods:
        - barman
        - basebackup
    barman:
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
    basebackup:
        max-rate: '100M'
```

> [!NOTE]
> `patroni_barman recover` requiere que tengas tanto Barman como `pg-backup-api` configurados en el host de Barman, de modo que pueda ejecutar un `barman recover` remoto a través de la API de copia de seguridad. El ejemplo anterior usa un subconjunto de los parámetros disponibles. Puedes obtener más información ejecutando `patroni_barman recover --help`.

El `create_replica_methods` define los métodos disponibles de creación de réplicas y el orden de su ejecución. Patroni se detendrá en el primero que devuelva 0. Cada método debe definir una sección separada en el archivo de configuración, indicando el comando a ejecutar y cualquier parámetro personalizado que deba pasarse a ese comando. Todos los parámetros se pasarán en un formato `--name=value`. Además de los parámetros definidos por el usuario, Patroni suministra un par de parámetros específicos del clúster:

`--scope`  
A qué clúster pertenece esta réplica

`--datadir`  
Ruta al directorio de datos de la réplica

`--role`  
Siempre 'replica'

`--connstring`  
Cadena de conexión para conectarse al miembro del clúster del que clonar (el primario u otra réplica). El usuario de la cadena de conexión puede ejecutar SQL y comandos del protocolo de replicación.

Un parámetro especial `no_leader`, cuando está habilitado, permite a Patroni invocar el método de creación de réplicas incluso si no hay un líder ni réplicas en ejecución. En ese caso, se pasará una cadena vacía como cadena de conexión. Esto es útil para restaurar desde la copia de seguridad binaria el clúster que estaba en ejecución anteriormente.

Un parámetro especial `keep_data`, cuando está habilitado, indicará a Patroni que no limpie la carpeta PGDATA antes de llamar a restore.

Un parámetro especial `no_params`, cuando está habilitado, desactiva la adición automática de parámetros específicos del clúster al comando personalizado. Los parámetros definidos por el usuario se siguen pasando.

El método `basebackup` es un caso especial: se usará si `create_replica_methods` está vacío, aunque es posible listarlo explícitamente entre los métodos de `create_replica_methods`. Este método inicializa una réplica nueva con `pg_basebackup`; la copia de seguridad base se toma del líder, salvo que haya réplicas con la etiqueta `clonefrom`, en cuyo caso una de esas réplicas se usará como origen para pg_basebackup. Funciona sin ninguna configuración; sin embargo, es posible especificar una sección de configuración `basebackup`. Se aplican las mismas reglas que con la configuración de los otros métodos, a saber: allí solo deben especificarse opciones largas (con --). Patroni no acepta sobrescrituras de conexión ni opciones que produzcan copias de seguridad en formato tar o comprimidas por el cliente. En PostgreSQL 15 y posteriores, la compresión del lado del servidor se admite con `compress: server-gzip` o `compress: server-zstd`. Patroni filtra las opciones que controla y los ajustes de compresión distintos de la compresión del lado del servidor, pero no realiza una validación completa de todos los nombres y valores de las opciones. Ten en cuenta también que, en caso de usarse enlaces simbólicos para la carpeta de WAL, es responsabilidad del usuario especificar como opción la ruta `--waldir` correcta, de modo que el enlace simbólico se conserve después de la construcción o reinicialización de la réplica. Esta opción, sin embargo, solo se admite desde la v10.

Puedes especificar los parámetros de basebackup como un mapa (pares clave-valor) o como una lista de elementos, donde cada elemento puede ser un par clave-valor o una clave única (para opciones que no reciben ningún valor, por ejemplo `--verbose`). Considera estos 2 ejemplos:

```yaml
postgresql:
    basebackup:
        max-rate: '100M'
        checkpoint: 'fast'
```

y

```yaml
postgresql:
    basebackup:
        - verbose
        - max-rate: '100M'
        - waldir: /pg-wal-mount/external-waldir
```

Si todos los métodos de creación de réplicas fallan, Patroni volverá a intentar todos los métodos en orden durante el siguiente ciclo del bucle de eventos.
