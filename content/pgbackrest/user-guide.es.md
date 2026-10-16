---
title: "Guía de usuario (Debian/Ubuntu)"
linkTitle: "Guía de usuario (Deb)"
weight: 20
description: "Guía paso a paso de instalación y uso de pgBackRest para sistemas Debian y Ubuntu."
icon: fa-brands fa-ubuntu
module: [PGBACKREST]
categories: [Tutorial]
upstream_link: "https://pgbackrest.org/user-guide.html"
---

--------

## Introducción {#introduction}

Esta guía de usuario está pensada para seguirse de forma secuencial, de principio a fin — cada sección depende de la anterior. Por ejemplo, la sección [Restauración](#restore-1) depende de la configuración realizada en la sección [Inicio rápido](#quick-start). Una vez que pgBackRest está en funcionamiento, es posible saltar entre secciones, pero se recomienda seguir la guía de usuario en orden la primera vez.

Aunque los ejemplos de esta guía están orientados a Debian/Ubuntu y PostgreSQL 17, debería ser bastante fácil aplicarlos a cualquier distribución Unix y a cualquier versión de PostgreSQL. Los únicos comandos específicos del sistema operativo son los de crear, iniciar, detener y eliminar clústeres de PostgreSQL. Los comandos de pgBackRest serán los mismos en cualquier sistema Unix, aunque la ubicación del ejecutable puede variar. Aunque pgBackRest se esfuerza por funcionar de manera consistente entre las distintas versiones de PostgreSQL, hay diferencias sutiles entre versiones de PostgreSQL que pueden aparecer en esta guía al ilustrar ciertos ejemplos, p. ej. las rutas, los nombres de archivo y los parámetros de PostgreSQL.

La información de configuración y la documentación de PostgreSQL pueden encontrarse en el [Manual](http://www.postgresql.org/docs/17/static/index.html) de PostgreSQL.

En esta guía de usuario se adopta un enfoque algo novedoso para la documentación. Cada comando se ejecuta en una máquina virtual cuando la documentación se genera a partir de la fuente XML. Esto significa que puedes tener una confianza elevada en que los comandos funcionan correctamente en el orden presentado. La salida se captura y se muestra debajo del comando cuando resulta apropiado. Si la salida no se incluye, es porque se consideró que no era relevante o que distraía del hilo narrativo.

Todos los comandos están pensados para ejecutarse como un usuario sin privilegios que disponga de privilegios sudo tanto para el usuario `root` como para el usuario `postgres`. También es posible ejecutar los comandos directamente como sus usuarios respectivos sin modificación, y en ese caso se pueden omitir los comandos `sudo`.


--------

## Conceptos {#concepts}

Los siguientes conceptos se definen según su relevancia para pgBackRest, PostgreSQL y esta guía de usuario.


### Copia de seguridad {#backup}

Una copia de seguridad es una copia consistente de un clúster de bases de datos que puede restaurarse para recuperarse de un fallo de hardware, para realizar una recuperación en un punto en el tiempo (Point-In-Time Recovery) o para levantar un standby nuevo.

**Copia de seguridad completa**: pgBackRest copia todo el contenido del clúster de bases de datos a la copia de seguridad. La primera copia de seguridad del clúster de bases de datos siempre es una copia completa. pgBackRest siempre puede restaurar una copia de seguridad completa directamente. La copia completa no depende de ningún archivo externo a ella para garantizar su consistencia.

**Copia de seguridad diferencial**: pgBackRest copia únicamente aquellos archivos del clúster de bases de datos que han cambiado desde la última copia de seguridad completa. pgBackRest restaura una copia diferencial copiando todos los archivos de la copia diferencial elegida y los archivos sin cambios apropiados de la copia completa anterior. La ventaja de una copia diferencial es que requiere menos espacio en disco que una copia completa; sin embargo, tanto la copia diferencial como la copia completa deben ser válidas para poder restaurar la copia diferencial.

**Copia de seguridad incremental**: pgBackRest copia únicamente aquellos archivos del clúster de bases de datos que han cambiado desde la última copia de seguridad (que puede ser otra copia incremental, una copia diferencial o una copia completa). Dado que una copia incremental solo incluye los archivos modificados desde la copia anterior, por lo general es mucho más pequeña que una copia completa o diferencial. Al igual que la copia diferencial, la copia incremental depende de que otras copias de seguridad sean válidas para poder restaurarse. Dado que la copia incremental incluye solo los archivos modificados desde la última copia de seguridad, todas las copias incrementales previas hasta la diferencial anterior, la copia diferencial anterior y la copia completa anterior deben ser válidas para poder realizar la restauración de la copia incremental. Si no existe ninguna copia diferencial, entonces todas las copias incrementales previas hasta la anterior copia completa (que debe existir) y la propia copia completa deben ser válidas para poder restaurar la copia incremental.


### Restauración {#restore}

Una restauración consiste en copiar una copia de seguridad a un sistema donde se iniciará como un clúster de bases de datos en vivo. Una restauración necesita los archivos de la copia de seguridad y uno o más segmentos de WAL para funcionar correctamente.


### Registro de escritura anticipada (WAL) {#write-ahead-log-wal}

WAL es el mecanismo que PostgreSQL utiliza para asegurar que no se pierda ningún cambio confirmado. Las transacciones se escriben secuencialmente en el WAL y una transacción se considera confirmada cuando esas escrituras se vuelcan a disco. Después, un proceso en segundo plano escribe los cambios en los archivos principales del clúster de bases de datos (también conocido como el heap). En caso de caída, el WAL se reproduce para hacer que la base de datos quede consistente.

WAL es conceptualmente infinito, pero en la práctica se divide en archivos individuales de 16MB llamados segmentos. Los segmentos de WAL siguen la convención de nomenclatura `0000000100000A1E000000FE`, donde los primeros 8 dígitos hexadecimales representan la línea de tiempo y los siguientes 16 dígitos son el número de secuencia lógico (LSN).


### Cifrado {#encryption}

El cifrado es el proceso de convertir los datos en un formato irreconocible a menos que se proporcione la contraseña adecuada (también denominada frase de contraseña).

pgBackRest cifrará el repositorio a partir de una contraseña proporcionada por el usuario, impidiendo así el acceso no autorizado a los datos almacenados en el repositorio.


--------

## Actualización de pgBackRest {#upgrading-pgbackrest}



### Actualización de pgBackRest de v2.x a v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

Actualizar de v2.x a v2.y es sencillo. El formato del repositorio no ha cambiado, por lo que para la mayoría de las instalaciones basta con instalar los binarios de la nueva versión. También es posible volver a una versión anterior si no se han utilizado funciones nuevas que no estén soportadas por la versión más antigua.

IMPORTANTE:

Las versiones local y remota de pgBackRest deben coincidir exactamente, por lo que deberían actualizarse juntas. Si hay una discrepancia, el archivado de WAL y las copias de seguridad no funcionarán hasta que las versiones coincidan. En tal caso, se informará del siguiente error: `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.


--------

## Compilación {#build}

Instalar pgBackRest desde un paquete es preferible a compilarlo desde el código fuente. Consulta [Instalación](#installation) para obtener más información sobre los paquetes.

Al compilar desde el código fuente, es mejor usar un host de compilación en lugar de compilar en producción. Muchas de las herramientas necesarias para la compilación por lo general no deberían instalarse en producción. pgBackRest consta de un único ejecutable, por lo que es fácil copiarlo a un host nuevo una vez compilado.

build **⇒** Descargar la versión `2.59.3` de pgBackRest a la ruta `/build`

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** Instalar las dependencias de compilación

```bash
sudo apt-get install python3-distutils meson gcc libpq-dev libssl-dev libxml2-dev \
       pkg-config liblz4-dev libzstd-dev libbz2-dev libz-dev libssh2-1-dev libsystemd-dev
```

build **⇒** Configurar y compilar pgBackRest

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.59.3
ninja -C /build/pgbackrest
```

build **⇒** Ejecutar opcionalmente las pruebas de humo para verificar que pgBackRest se compiló correctamente

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               11.07s


       [filtered 7 lines of output]
```

--------

## Instalación {#installation}

Se crea un nuevo host llamado pg-primary para alojar el clúster de demostración y ejecutar los ejemplos de pgBackRest.

Instalar pgBackRest desde un paquete es preferible a compilarlo desde el código fuente. Al instalar desde un paquete, el resto de las instrucciones de esta sección generalmente no son necesarias, pero es posible que un paquete omita la creación de uno de los directorios o aplique permisos incorrectos. En ese caso, puede ser necesario crear directorios manualmente o actualizar los permisos.

Los paquetes de pgBackRest para Debian/Ubuntu están disponibles en [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si no se proporcionan paquetes para tu distribución/versión, puedes [compilar desde el código fuente](#build) y luego instalar manualmente como se muestra aquí.

pg-primary **⇒** Instalar dependencias

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-primary **⇒** Copiar el binario de pgBackRest desde el host de compilación

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest requiere directorios de registro y de configuración, además de un archivo de configuración.

pg-primary **⇒** Crear el archivo de configuración y los directorios de pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

pgBackRest debería estar ya correctamente instalado, pero es mejor comprobarlo. Si se pasó por alto alguna dependencia, obtendrás un error al ejecutar pgBackRest desde la línea de comandos.

pg-primary **⇒** Comprobar que la instalación funcionó

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.59.3 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## Inicio rápido {#quick-start}

La sección de inicio rápido cubrirá la configuración básica de pgBackRest y PostgreSQL e introducirá los comandos `backup`, `restore` e `info`.


### Configurar el clúster de demostración {#setup-demo-cluster}

Crear el clúster de demostración es opcional, pero se recomienda encarecidamente, especialmente a los usuarios nuevos, ya que los comandos de ejemplo de la guía de usuario hacen referencia al clúster de demostración; los ejemplos asumen que el clúster de demostración se ejecuta en el puerto predeterminado (es decir, 5432). El clúster no se iniciará hasta una sección posterior porque todavía queda configuración por hacer.

pg-primary **⇒** Crear el clúster de demostración

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 102:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

### Configurar la stanza del clúster {#configure-cluster-stanza}

Una stanza es la configuración de un clúster de bases de datos PostgreSQL que define dónde se ubica, cómo se harán las copias de seguridad, las opciones de archivado, etc. La mayoría de los servidores de bases de datos tendrán un solo clúster de bases de datos PostgreSQL y, por lo tanto, una sola stanza, mientras que los servidores de copias de seguridad tendrán una stanza por cada clúster de bases de datos que necesite copia de seguridad.

Es tentador nombrar la stanza según el clúster primario, pero un nombre mejor describe las bases de datos que contiene el clúster. Dado que el nombre de la stanza se usará para el primario y todas las réplicas, es más apropiado elegir un nombre que describa la función real del clúster, como app o dw, en lugar del nombre local del clúster, como main o prod.

El nombre «demo» describe con precisión el propósito de este clúster, de modo que también será un buen nombre de stanza.

pgBackRest necesita saber dónde se encuentra el directorio de datos base del clúster PostgreSQL. La ruta puede solicitarse directamente a PostgreSQL, pero en un escenario de recuperación el proceso de PostgreSQL no estará disponible. Durante las copias de seguridad, el valor proporcionado a pgBackRest se comparará con la ruta en la que PostgreSQL se está ejecutando y deben ser iguales, o de lo contrario la copia de seguridad devolverá un error. Asegúrate de que `pg-path` sea exactamente igual a data_directory tal como lo informa PostgreSQL.

Por defecto, Debian/Ubuntu almacena los clústeres en `/var/lib/postgresql/[version]/[cluster]`, por lo que es fácil determinar la ruta correcta para el directorio de datos.

Al crear el archivo `/etc/pgbackrest/pgbackrest.conf`, deben otorgarse privilegios de lectura al propietario de la base de datos (normalmente `postgres`).

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar el directorio de datos del clúster PostgreSQL

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo
```

Los archivos de configuración de pgBackRest siguen una convención similar a los archivos INI de Windows. Las secciones se denotan con texto entre corchetes y cada sección contiene pares clave/valor. Las líneas que comienzan con `#` se ignoran y pueden usarse como comentarios, pero no se admiten los comentarios al final de la línea a continuación de un valor en la misma línea. No se admite el uso de comillas y los espacios en blanco se recortan de las claves y de los valores. Las secciones se combinarán si aparecen más de una vez.

Hay varias formas de cargar los archivos de configuración de pgBackRest:

- `config` y `config-include-path` son los predeterminados: se cargará el archivo de configuración predeterminado, si existe, y se añadirán los archivos `*.conf` de la ruta de inclusión de configuración predeterminada, si existen.
- Se especifica la opción `config`: solo se cargará el archivo de configuración especificado y se espera que exista.
- Se especifica `config-include-path`: se cargarán los archivos `*.conf` de la ruta de inclusión de configuración y se exige que la ruta exista. El archivo de configuración predeterminado se cargará si existe. Si se desea cargar solo los archivos de la ruta de inclusión de configuración especificada, también puede pasarse la opción `--no-config`.
- Se especifican `config` y `config-include-path`: con los valores especificados por el usuario, se cargará el archivo de configuración y se añadirán los archivos `*.conf` de la ruta de inclusión de configuración. Se espera que los archivos existan.
- Se especifica `config-path`: este parámetro anulará la ruta base de la ubicación predeterminada del archivo de configuración y/o la ruta base del parámetro config-include-path predeterminado, salvo que la opción config y/o config-include-path se establezca explícitamente.

Los archivos se concatenan como si fueran un único archivo grande y cada archivo debe ser válido individualmente. Esto significa que las secciones deben especificarse en cada archivo donde se necesiten para almacenar un par clave/valor. El orden no importa, pero existe una precedencia basada en las secciones. La precedencia (de mayor a menor) es:

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

NOTA:

`--config`, `--config-include-path` y `--config-path` son opciones exclusivas de la línea de comandos.

pgBackRest también puede configurarse mediante variables de entorno (ejemplo más abajo); estas variables se aplican a comandos como [backup](/es/pgbackrest/command/backup/), [restore](/es/pgbackrest/command/restore/) y [archive-push](/es/pgbackrest/command/archive-push/).

pg-primary **⇒** Configurar `log-path` mediante el entorno

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.59.3 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### Crear el repositorio {#create-the-repository}

El repositorio es donde pgBackRest almacena las copias de seguridad y archiva los segmentos de WAL.

Puede ser difícil estimar por adelantado cuánto espacio necesitarás. Lo mejor es hacer algunas copias de seguridad, registrar el tamaño de los distintos tipos de copia (full/incr/diff) y medir la cantidad de WAL generada por día. Esto te dará una idea general del espacio que necesitarás, aunque por supuesto es probable que los requisitos cambien con el tiempo a medida que evolucione tu base de datos.

Para esta demostración, el repositorio se almacenará en el mismo host que el servidor PostgreSQL. Esta es la configuración más sencilla y resulta útil en los casos donde se emplea software de copia de seguridad tradicional para respaldar el host de la base de datos.

pg-primary **⇒** Crear el repositorio de pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

La ruta del repositorio debe configurarse para que pgBackRest sepa dónde encontrarla.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar la ruta del repositorio de pgBackRest

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest
```

También pueden configurarse varios repositorios. Consulta [Repositorios múltiples](#multiple-repositories) para más detalles.


### Configurar el archivado {#configure-archiving}

Hacer una copia de seguridad de un clúster PostgreSQL en ejecución requiere que el archivado de WAL esté habilitado. `%p` es la forma en que PostgreSQL especifica la ubicación del segmento de WAL que se va a archivar. Ten en cuenta que se creará *al menos* un segmento de WAL durante el proceso de copia de seguridad incluso si no se hacen escrituras explícitas en el clúster.

pg-primary:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurar los parámetros de archivado

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

El clúster PostgreSQL debe reiniciarse después de hacer estos cambios y antes de realizar una copia de seguridad.

pg-primary **⇒** Reiniciar el clúster de demostración

```bash
sudo pg_ctlcluster 17 demo restart
```

El parámetro `hot_standby` está habilitado por defecto y debería dejarse así en todos los clústeres. Cualquier clúster puede restaurarse más adelante como standby, por ejemplo, un primario que se reconstruye como standby tras una conmutación por error, y un standby no aceptará conexiones de solo lectura sin él.

Cuando se espera que el archivado de un segmento de WAL tarde más de 60 segundos (el valor predeterminado) en llegar al repositorio de pgBackRest, debería aumentarse la opción `archive-timeout` de pgBackRest. Ten en cuenta que esta opción no es lo mismo que la opción archive_timeout de PostgreSQL, que se usa para forzar el cambio de segmento de WAL; resulta útil para bases de datos con largos periodos de inactividad. Para obtener más información sobre la opción archive_timeout de PostgreSQL, consulta el [Write Ahead Log](https://www.postgresql.org/docs/current/static/runtime-config-wal.html) de PostgreSQL.

El comando `archive-push` puede configurarse con sus propias opciones. Por ejemplo, puede establecerse un nivel de compresión más bajo para acelerar el archivado sin afectar a la compresión usada para las copias de seguridad.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `archive-push` para usar un nivel de compresión más bajo

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

Esta técnica de configuración puede usarse con cualquier comando e incluso puede dirigirse a una stanza específica, p. ej. `demo:archive-push`.


### Configurar la retención {#configure-retention}

pgBackRest expira las copias de seguridad según las opciones de retención.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar la retención en 2 copias de seguridad completas

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

Puede encontrarse más información sobre la retención en la sección [Retención](#retention).


### Configurar el cifrado del repositorio {#configure-repository-encryption}

El repositorio se configurará con un tipo de cifrado y una clave para demostrar el cifrado. El cifrado siempre se realiza en el lado del cliente, incluso si el tipo de repositorio (p. ej. S3 u otro almacén de objetos) admite cifrado.

Es importante usar una frase de contraseña larga y aleatoria para la clave de cifrado. Una buena forma de generarla es ejecutar: `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar el cifrado del repositorio de pgBackRest

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

NOTA:

Los ajustes de cifrado se colocan en la sección `[global]`, más arriba, para que el comando `info` pueda leer todas las stanzas. Sin la opción `stanza`, el comando `info` lee los ajustes de cifrado solo de la sección `[global]`, por lo que los ajustes de cifrado configurados por stanza requieren la opción `stanza` para leer una stanza cifrada.

Una vez que el repositorio haya sido configurado y la stanza creada y comprobada, los ajustes de cifrado del repositorio no pueden cambiarse.


### Crear la stanza {#create-the-stanza}

Debe ejecutarse el comando `stanza-create` para inicializar la stanza. Se recomienda ejecutar el comando `check` después de `stanza-create` para asegurar que el archivado y las copias de seguridad estén correctamente configurados.

pg-primary **⇒** Crear la stanza y comprobar la configuración

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=415-9c2d1500 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### Comprobar la configuración {#check-the-configuration}

El comando `check` valida que pgBackRest y el parámetro archive_command estén configurados correctamente para el archivado y las copias de seguridad de la stanza especificada. Intentará comprobar todos los repositorios y bases de datos que estén configurados para el host en el que se ejecuta el comando. Detecta errores de configuración, particularmente en el archivado, que dan lugar a copias de seguridad incompletas porque los segmentos de WAL requeridos no llegaron al archivado. El comando puede ejecutarse en el host de PostgreSQL o en el del repositorio. El comando también puede ejecutarse en el host standby; sin embargo, dado que `pg_switch_xlog()`/`pg_switch_wal()` no puede ejecutarse en el standby, el comando solo probará la configuración del repositorio.

Ten en cuenta que se llama a `pg_create_restore_point('pgBackRest Archive Check')` y a `pg_switch_xlog()`/`pg_switch_wal()` para forzar a PostgreSQL a archivar un segmento de WAL.

pg-primary **⇒** Comprobar la configuración

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=424-7270037b --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000100000000/000000010000000000000001-e8eb01b8d8aaf321d368dc8edf5b559247841eb1.gz' on repo1
P00   INFO: check command end: completed successfully
```

### Ajuste del rendimiento {#performance-tuning}

pgBackRest tiene varias opciones de rendimiento que no están habilitadas por defecto para mantener la compatibilidad con versiones anteriores en el repositorio. Sin embargo, al crear un repositorio nuevo se recomiendan las siguientes opciones. También pueden usarse en un repositorio existente, con la salvedad de que las versiones anteriores de pgBackRest no podrán leer el repositorio. Esta incompatibilidad depende de cuándo se introdujo la función, como se indica en la lista siguiente.

- `compress-type` - determina el algoritmo de compresión usado por los comandos `backup` y `archive-push`. El valor predeterminado es `gz` (Gzip), pero se recomienda `zst` (Zstandard) porque es mucho más rápido y ofrece una compresión similar a `gz`. `zst` está soportado por la opción `compress-type` desde la [v2.27](/es/pgbackrest/release/#v227-release-notes). Consulta [Tipo de compresión](/es/pgbackrest/configuration/#compress-type-option---compress-type) para más detalles.
- `repo-bundle` - combina los archivos pequeños durante la copia de seguridad para ahorrar espacio y mejorar la velocidad de los comandos `backup` y `restore`, especialmente en almacenes de objetos como S3. La opción `repo-bundle` se introdujo en la [v2.39](/es/pgbackrest/release/#v239-release-notes). Consulta [Agrupación de archivos](#file-bundling) para más detalles.
- `repo-block` - almacena solo las porciones de los archivos que han cambiado en lugar del archivo completo durante una `backup` `diff`/`incr`. Esto ahorra espacio y aumenta la velocidad de la `backup`. La opción `repo-block` se introdujo en la [v2.46](/es/pgbackrest/release/#v246-release-notes), pero se recomienda al menos la [v2.52.1](/es/pgbackrest/release/#v2521-release-notes). Consulta [Incremental por bloques](#block-incremental) para más detalles.

Existen otras opciones de rendimiento que no están habilitadas por defecto porque requieren configuración adicional o porque el valor predeterminado es seguro (aunque no óptimo). Estas opciones están disponibles en todas las versiones v2 de pgBackRest.

- `process-max` - determina cuántos procesos se usarán para los comandos. El valor predeterminado es 1, que casi nunca es el valor apropiado. Cada comando usa `process-max` de forma distinta, así que consulta la documentación de cada comando para más detalles sobre su uso.
- `archive-async` - archiva los archivos de WAL al repositorio por lotes, lo que aumenta enormemente la velocidad de archivado. No está habilitada por defecto porque requiere que se cree una ruta de spool. Consulta [Archivado asíncrono](#asynchronous-archiving) para más detalles.
- `backup-standby` - realiza la copia de seguridad en un standby en lugar de en el primario para reducir la carga del primario. No está habilitada por defecto porque requiere configuración adicional y la presencia de uno o más hosts standby. Consulta [Copia de seguridad desde un standby](#backup-from-a-standby) para más detalles.


### Realizar una copia de seguridad {#perform-a-backup}

Por defecto, pgBackRest esperará el siguiente checkpoint programado con regularidad antes de iniciar una copia de seguridad. Dependiendo de los parámetros checkpoint_timeout y checkpoint_segments de PostgreSQL, puede pasar bastante tiempo antes de que se complete un checkpoint y de que la copia de seguridad pueda comenzar. En general, es mejor establecer `start-fast=y` para que la copia de seguridad comience de inmediato. Esto fuerza un checkpoint, pero dado que las copias de seguridad suelen ejecutarse una vez al día, un checkpoint adicional no debería tener un impacto notable en el rendimiento. Sin embargo, en clústeres muy cargados puede ser mejor pasar `--start-fast` en la línea de comandos cuando sea necesario.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar el inicio rápido de la copia de seguridad

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Para hacer una copia de seguridad del clúster PostgreSQL, ejecuta pgBackRest con el comando `backup`.

pg-primary **⇒** Hacer una copia de seguridad del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=451-67e8eca3 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-190624F
P00   INFO: full backup size = 22MB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=451-67e8eca3 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Por defecto, pgBackRest intentará hacer una copia de seguridad incremental. Sin embargo, una copia incremental debe basarse en una copia completa y, como no existía ninguna copia completa, pgBackRest hizo una copia completa en su lugar.

La opción `type` puede usarse para especificar una copia completa o diferencial.

pg-primary **⇒** Copia de seguridad diferencial del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-190624F_20261002-190626D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=477-af59c897 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Esta vez no hubo ninguna advertencia porque ya existía una copia de seguridad completa. Mientras que las copias incrementales pueden basarse en una copia completa *o* diferencial, las copias diferenciales deben basarse en una copia completa. Puede hacerse una copia completa ejecutando el comando `backup` con `--type=full`.

Durante una copia de seguridad en línea, pgBackRest espera a que se archiven los segmentos de WAL requeridos para la consistencia de la copia. Este tiempo de espera se rige por la opción `archive-timeout` de pgBackRest, cuyo valor predeterminado es 60 segundos. Si se sabe que el archivado de un segmento individual tarda más, debería aumentarse esta opción.


### Programar una copia de seguridad {#schedule-a-backup}

Las copias de seguridad pueden programarse con utilidades como cron.

En el siguiente ejemplo, se configuran dos tareas de cron para ejecutarse; las copias de seguridad completas están programadas para las 6:30 AM de todos los domingos y las copias diferenciales para las 6:30 AM de lunes a sábado. Si este crontab se instala por primera vez a mitad de semana, pgBackRest hará una copia de seguridad completa la primera vez que se ejecute la tarea diferencial, seguida al día siguiente de una copia diferencial.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

Una vez programadas las copias de seguridad, es importante configurar la retención para que las copias expiren según un calendario regular; consulta [Retención](#retention).


### Información de las copias de seguridad {#backup-information}

Usa el comando `info` para obtener información sobre las copias de seguridad.

pg-primary **⇒** Obtener información del clúster de demostración

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-190624F
            timestamp start/stop: 2026-10-02 19:06:24+00 / 2026-10-02 19:06:26+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 22MB, database backup size: 22MB
            repo1: backup set size: 2.9MB, backup size: 2.9MB

        diff backup: 20261002-190624F_20261002-190626D
            timestamp start/stop: 2026-10-02 19:06:26+00 / 2026-10-02 19:06:28+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 22MB, database backup size: 8.3KB
            repo1: backup set size: 2.9MB, backup size: 448B
            backup reference total: 1 full
```

El comando `info` opera sobre una stanza o sobre todas las stanzas. La salida de texto es la predeterminada y ofrece un resumen legible por humanos de las copias de seguridad de las stanzas solicitadas. Este formato está sujeto a cambios con cualquier versión.

Para una salida legible por máquinas, usa `--output=json`. La salida JSON contiene mucha más información que la salida de texto y se mantiene estable a menos que se encuentre un error.

Para acelerar la ejecución, limita la salida a solo la información de progreso especificando `--detail-level=progress`. Ten en cuenta que esto omite todas las comprobaciones excepto la disponibilidad de la stanza.

Cada stanza tiene su propia sección y es posible limitar la salida a una sola stanza con la opción `--stanza`. El «`status`» de la stanza da una indicación breve del estado de salud de la stanza. Si es «`ok`», pgBackRest funciona con normalidad. Si hay varios repositorios, un estado «`mixed`» indica que la stanza no está en un estado saludable en uno o más de los repositorios; en ese caso, el estado de la stanza se detallará por repositorio. Para los casos en que ocurra un error en un repositorio que no sea uno de los códigos de error conocidos, se usará el código de error «`other`» y se proporcionarán los detalles completos del error. El «`wal archive min/max`» muestra el WAL mínimo y máximo almacenado actualmente en el archivado y, en el caso de varios repositorios, se informará considerando todos los repositorios salvo que se establezca la opción `--repo`. Ten en cuenta que puede haber huecos debido a políticas de retención del archivado u otras razones.

Los mensajes «`backup/expire running`» y/o «`restore running`» aparecerán junto a la información de «`status`» si alguno de esos comandos se está ejecutando actualmente en el host. El progreso por repositorio también se informará en la salida de texto y se incluirá un array «`repo`» en la salida JSON.

Las copias de seguridad se muestran de la más antigua a la más reciente. La copia más antigua *siempre* será una copia completa (indicada con una `F` al final de la etiqueta), pero la más reciente puede ser completa, diferencial (termina con `D`) o incremental (termina con `I`).

El «`timestamp start/stop`» define el periodo de tiempo durante el cual se ejecutó la copia de seguridad. El «`timestamp stop`» puede usarse para determinar qué copia usar al realizar una recuperación en un punto en el tiempo. Puede encontrarse más información sobre la recuperación en un punto en el tiempo en la sección [Recuperación en un punto en el tiempo](#point-in-time-recovery).

El «`wal start/stop`» define el rango de WAL necesario para hacer que la base de datos sea consistente durante la restauración. El comando `backup` se asegurará de que este rango de WAL esté en el archivado antes de completarse.

El «`database size`» es el tamaño completo sin comprimir de la base de datos, mientras que «`database backup size`» es la cantidad de datos de la base de datos que realmente se van a respaldar (serán iguales en las copias completas).

El «`repo`» indica en qué repositorio reside esta copia de seguridad. El «`backup set size`» incluye todos los archivos de esta copia y de cualquier copia referenciada en el repositorio que sean necesarios para restaurar la base de datos desde esta copia, mientras que «`backup size`» incluye solo los archivos de esta copia (también serán iguales en las copias completas). Los tamaños de repositorio reflejan los tamaños comprimidos de los archivos si la compresión está habilitada en pgBackRest.

El «`backup reference total`» resume la lista de copias de seguridad adicionales que se requieren para restaurar esta copia. Usa la opción `--set` para mostrar la lista completa de referencias.


### Restaurar una copia de seguridad {#restore-a-backup}

Las copias de seguridad pueden protegerte de diversos escenarios de desastre, los más comunes son el fallo de hardware y la corrupción de datos. La forma más sencilla de simular una corrupción de datos es eliminar un archivo importante del clúster PostgreSQL.

pg-primary **⇒** Detener el clúster de demostración y eliminar el archivo `pg_control`

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres rm /var/lib/postgresql/17/demo/global/pg_control
```

Iniciar el clúster sin este archivo importante producirá un error.

pg-primary **⇒** Intentar iniciar el clúster de demostración corrupto

```bash
sudo pg_ctlcluster 17 demo start
```

```text
Error: /usr/lib/postgresql/17/bin/pg_ctl /usr/lib/postgresql/17/bin/pg_ctl start -D /var/lib/postgresql/17/demo -l /var/log/postgresql/postgresql-17-demo.log -s -o  -c config_file="/etc/postgresql/17/demo/postgresql.conf"  exited with status 1:
postgres: could not find the database system
Expected to find it in the directory "/var/lib/postgresql/17/demo",
but could not open file "/var/lib/postgresql/17/demo/global/pg_control": No such file or directory
Examine the log output.
```

Para restaurar una copia de seguridad del clúster PostgreSQL, ejecuta pgBackRest con el comando `restore`. El clúster debe estar detenido (en este caso ya está detenido) y deben eliminarse todos los archivos del directorio de datos de PostgreSQL.

pg-primary **⇒** Eliminar los archivos antiguos del clúster de demostración

```bash
sudo -u postgres find /var/lib/postgresql/17/demo -mindepth 1 -delete
```

pg-primary **⇒** Restaurar el clúster de demostración e iniciar PostgreSQL

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo pg_ctlcluster 17 demo start
```

Esta vez el clúster se inició correctamente porque la restauración reemplazó el archivo `pg_control` que faltaba.

Puede encontrarse más información sobre el comando `restore` en la sección [Restauración](#restore-1).


--------

## Supervisión {#monitoring}

La supervisión es una parte importante de cualquier sistema en producción. Hay muchas herramientas disponibles y pgBackRest puede supervisarse en cualquiera de ellas con un poco de trabajo.

pgBackRest puede emitir información sobre el repositorio en formato JSON, que incluye una lista de todas las copias de seguridad de cada stanza e información del archivado de WAL.


### En PostgreSQL {#in-postgresql}

El comando `COPY` de PostgreSQL permite cargar la información de pgBackRest en una tabla. El siguiente ejemplo encapsula esa lógica en una función que puede usarse para hacer consultas en tiempo real.

pg-primary **⇒** Cargar la función de información de pgBackRest para PostgreSQL

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

Ahora la función `monitor.pgbackrest_info()` puede usarse para determinar la hora de la última copia de seguridad correcta y el WAL archivado de una stanza.

pg-primary **⇒** Consultar la hora de la última copia de seguridad correcta y el WAL archivado

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 19:06:28+00 | 000000010000000000000005
(1 row)
```

### Uso de jq {#using-jq}

jq es una utilidad de línea de comandos que puede extraer datos de JSON con facilidad.

pg-primary **⇒** Instalar la utilidad jq

```bash
sudo apt-get install jq
```

Ahora jq puede usarse para consultar la hora de la última copia de seguridad correcta de una stanza.

pg-primary **⇒** Consultar la hora de la última copia de seguridad correcta

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .backup[-1] | .timestamp.stop'
```

```text
1790967988
```

O el último WAL archivado.

pg-primary **⇒** Consultar el último WAL archivado

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .archive[-1] | .max'
```

```text
"000000010000000000000005"
```

NOTA:

Esta sintaxis requiere jq v1.5.

NOTA:

jq puede redondear números grandes como los identificadores de sistema. Prueba tus consultas con cuidado.


--------

## Copia de seguridad {#backup-1}

Cuando se configuran varios repositorios, pgBackRest hará la copia de seguridad en el repositorio de mayor prioridad (p. ej. `repo1`) salvo que se especifique la opción `--repo`.

pgBackRest no incluye un planificador integrado, por lo que es mejor ejecutarlo desde cron u otro mecanismo de programación.

Consulta [Realizar una copia de seguridad](#perform-a-backup) para más detalles y ejemplos.


### Agrupación de archivos {#file-bundling}

Agrupar los archivos en el repositorio ahorra tiempo durante la copia de seguridad y algo de espacio en el repositorio. Esto es especialmente notorio cuando el repositorio se almacena en un almacén de objetos como S3 o en sistemas de archivos con tamaños de bloque grandes. El tiempo de creación por archivo en los almacenes de objetos es mayor y los archivos muy pequeños pueden costar tanto de almacenar como los archivos más grandes.

La función de agrupación de archivos se habilita con la opción `repo-bundle`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-bundle`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Una copia de seguridad completa sin agrupación de archivos tendrá más de 1000 archivos en la ruta de la copia, pero con la agrupación el número total de archivos se reduce considerablemente. Un beneficio adicional es que los archivos de longitud cero no se almacenan (excepto en el manifiesto), mientras que en una copia de seguridad normal cada archivo de longitud cero se almacena individualmente.

pg-primary **⇒** Realizar una copia de seguridad completa

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** Comprobar el total de archivos

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

Las opciones `repo-bundle-size` y `repo-bundle-limit` pueden usarse para el ajuste, aunque los valores predeterminados deberían ser óptimos en la mayoría de los casos.

Si bien la agrupación de archivos es por lo general más eficiente, la desventaja es que resulta más difícil recuperar archivos manualmente del repositorio. Puede no ser ideal para almacenamiento con deduplicación, ya que cada copia completa organizará los archivos en los paquetes de forma diferente. Por último, los paquetes de archivos no se pueden reanudar, así que ten cuidado de no establecer `repo-bundle-limit` demasiado alto.


### Incremental por bloques {#block-incremental}

Las copias de seguridad incrementales por bloques ahorran espacio almacenando solo las partes de un archivo que han cambiado desde la copia anterior, en lugar de almacenar el archivo completo.

La función de incremental por bloques se habilita con la opción `repo-block` y funciona mejor cuando está habilitada para todos los tipos de copia de seguridad. La agrupación de archivos también debe estar habilitada.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-block`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

### Anotaciones de las copias de seguridad {#backup-annotations}

Los usuarios pueden adjuntar pares clave/valor informativos a la copia de seguridad. Esta opción puede usarse varias veces para adjuntar varias anotaciones.

pg-primary **⇒** Realizar una copia de seguridad completa con anotaciones

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

Las anotaciones se muestran en la salida de texto del comando `info` cuando se especifica una copia de seguridad con `--set` y siempre aparecen en la salida JSON.

pg-primary **⇒** Obtener información del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-190643F
            timestamp start/stop: 2026-10-02 19:06:43+00 / 2026-10-02 19:06:44+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22MB, database backup size: 22MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                key: value
                source: demo backup
```

Las anotaciones incluidas con el comando `backup` pueden añadirse, modificarse o eliminarse después con el comando `annotate`.

pg-primary **⇒** Cambiar las anotaciones de la copia de seguridad

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-190643F
            timestamp start/stop: 2026-10-02 19:06:43+00 / 2026-10-02 19:06:44+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22MB, database backup size: 22MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## Retención {#retention}

En general, es mejor conservar tantas copias de seguridad como sea posible para disponer de una ventana mayor para la [recuperación en un punto en el tiempo](#point-in-time-recovery), pero también deben considerarse cuestiones prácticas como el espacio en disco. Las opciones de retención eliminan las copias de seguridad más antiguas cuando ya no son necesarias.

pgBackRest hace rotación de las copias de seguridad completas según el tipo de retención, que puede ser un conteo o un periodo de tiempo. Cuando se especifica un conteo, la expiración no se ocupa de cuándo se crearon las copias de seguridad, sino de cuántas deben conservarse. Las copias diferenciales se basan en conteo, pero siempre expirarán cuando expire la copia completa de la que dependen. Las copias incrementales no expiran de forma independiente por retención — siempre expiran junto con su copia completa o diferencial relacionada. Consulta las secciones [Retención de copias de seguridad completas](#full-backup-retention) y [Retención de copias de seguridad diferenciales](#differential-backup-retention) para más detalles y ejemplos.

Por defecto, el WAL archivado se conserva para las copias de seguridad que no han expirado; sin embargo, aunque no se recomienda, este calendario puede modificarse por repositorio con las opciones retention-archive. Consulta la sección [Retención del archivado](#archive-retention) para más detalles y ejemplos.

El comando `expire` se ejecuta automáticamente después de cada copia de seguridad correcta y también puede ejecutarlo el usuario. Cuando lo ejecuta el usuario, la expiración ocurrirá según lo definido por los ajustes de retención de cada repositorio configurado. Si se proporciona la opción `--repo`, la expiración ocurrirá solo en el repositorio especificado. El usuario también puede limitar la expiración a un conjunto de copias de seguridad específico con la opción `--set` y, salvo que se especifique la opción `--repo`, se buscará en todos los repositorios y se expirará cualquiera que coincida con los criterios del conjunto. Cabe señalar que el calendario de retención del archivado se comprobará y aplicará cada vez que se ejecute el comando `expire`.


### Retención de copias de seguridad completas {#full-backup-retention}

`repo1-retention-full-type` determina cómo se interpreta la opción `repo1-retention-full`; ya sea como el número de copias completas que deben conservarse o cuántos días deben conservarse las copias completas. Las copias nuevas deben completarse antes de que ocurra la expiración — esto significa que si `repo1-retention-full-type=count` y `repo1-retention-full=2`, habrá tres copias completas almacenadas antes de que expire la más antigua, o bien si `repo1-retention-full-type=time` y `repo1-retention-full=20`, debe existir una copia completa con al menos 20 días de antigüedad antes de que pueda ocurrir la expiración.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-retention-full`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

La copia de seguridad usa `repo1-retention-full=2`, pero actualmente solo hay una copia completa, por lo que la siguiente copia completa que se ejecute no expirará ninguna copia completa.

pg-primary **⇒** Realizar una copia de seguridad completa

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 975 lines of output]
P00   INFO: repo1: remove expired backup 20261002-190641F
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190643F, start = 000000020000000000000008
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

El archivado *sí* se expira porque se generaron segmentos de WAL antes de la copia de seguridad más antigua. Estos no sirven para la recuperación — solo los segmentos de WAL generados después de una copia de seguridad pueden usarse para recuperar esa copia.

pg-primary **⇒** Realizar una copia de seguridad completa

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-190643F
P00   INFO: repo1: remove expired backup 20261002-190643F
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000008, stop = 00000002000000000000000A
P00   INFO: expire command end: completed successfully
```

La copia de seguridad completa `20261002-190624F` ha expirado y la retención del archivado se basa en la `20261002-190646F`, que ahora es la copia completa más antigua.


### Retención de copias de seguridad diferenciales {#differential-backup-retention}

Establece `repo1-retention-diff` en el número de copias de seguridad diferenciales requeridas. Las diferenciales solo dependen de la copia completa anterior, por lo que es posible crear un conjunto «rotativo» de diferenciales para el último día o más. Esto permite restauraciones rápidas a puntos en el tiempo recientes, pero reduce el consumo general de espacio.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=1

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

La copia de seguridad usa `repo1-retention-diff=1`, así que habrá que hacer dos diferenciales antes de que expire una. Se añade una copia de seguridad incremental para demostrar la expiración incremental, que en este caso depende de la expiración de la diferencial.

pg-primary **⇒** Realizar copias de seguridad diferenciales e incrementales

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Ahora, hacer una copia de seguridad diferencial expirará las copias diferencial e incremental anteriores, dejando solo una copia diferencial.

pg-primary **⇒** Realizar una copia de seguridad diferencial

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=956-fb652d58 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-190648F_20261002-190650D, 20261002-190648F_20261002-190651I
P00   INFO: repo1: remove expired backup 20261002-190648F_20261002-190651I
P00   INFO: repo1: remove expired backup 20261002-190648F_20261002-190650D
P00   INFO: expire command end: completed successfully
```

### Retención del archivado {#archive-retention}

Aunque pgBackRest elimina automáticamente los segmentos de WAL archivados al expirar copias de seguridad (el comportamiento predeterminado expira el WAL de las copias completas según la opción `repo1-retention-full`), puede ser útil expirar el archivado de forma más agresiva para ahorrar espacio en disco. Ten en cuenta que las copias completas se tratan como copias diferenciales a efectos de la retención diferencial del archivado.

Expirar el archivado nunca eliminará segmentos de WAL que sean necesarios para hacer consistente una copia de seguridad. Sin embargo, dado que la recuperación en un punto en el tiempo (PITR) solo funciona sobre un flujo continuo de WAL, se debe tener cuidado al expirar el archivado de forma agresiva fuera del proceso normal de expiración de copias de seguridad. Para determinar qué se expirará sin expirar realmente nada, puede proporcionarse la opción `dry-run` en la línea de comandos junto con el comando `expire`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

pg-primary **⇒** Realizar una copia de seguridad diferencial

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261002-190648F_20261002-190654D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** Expirar el archivado

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=1037-f7b8ca1a --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190646F, start = 00000002000000000000000B, stop = 00000002000000000000000B
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F_20261002-190652D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F_20261002-190654D, start = 000000020000000000000016
P00   INFO: repo1: 17-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

La copia de seguridad diferencial `20261002-190648F_20261002-190652D` tiene segmentos de WAL archivados que deben conservarse para hacer consistentes las copias más antiguas, aunque no puedan reproducirse más hacia adelante con PITR. Los segmentos de WAL generados después de `20261002-190648F_20261002-190652D` pero antes de `20261002-190648F_20261002-190654D` se eliminan. Los segmentos de WAL generados después de la nueva copia de seguridad `20261002-190648F_20261002-190654D` permanecen y pueden usarse para PITR.

Dado que las copias completas se consideran copias diferenciales a efectos de la retención diferencial del archivado, si ahora se hace una copia completa con los mismos ajustes, solo se conservará el archivado de esa copia completa para PITR.


--------

## Restauración {#restore-1}

El comando restore usa por defecto la selección automática de la copia de seguridad más reciente del primer repositorio donde existan copias (consulta [Inicio rápido - Restaurar una copia de seguridad](#restore-a-backup)). El orden en que se comprueban los repositorios lo dicta el `pgbackrest.conf` (p. ej. repo1 se comprobará antes que repo2). Para seleccionar de un repositorio específico, puede pasarse la opción `--repo` (p. ej. `--repo=1`). Puede pasarse la opción `--set` si se desea una copia distinta de la más reciente.

Cuando se especifica un PITR con `--type=time` o `--type=lsn`, la hora objetivo o el LSN objetivo debe suministrarse con la opción `--target`. Si no se especifica `--set`, los repositorios configurados se comprueban en orden buscando una copia cuya hora de finalización sea anterior a la hora objetivo, o cuyo LSN de finalización sea menor o igual que el LSN objetivo. Si no se encuentra ninguna copia que coincida, pgBackRest lanza un error tanto para `--type=time` como para `--type=lsn`; no recurre a la copia más reciente. Para otros tipos de PITR, p. ej. `xid`, la opción `--set` debe proporcionarse si el objetivo es anterior a la copia más reciente. Consulta [Recuperación en un punto en el tiempo](#point-in-time-recovery) para más detalles y ejemplos.

Los slots de replicación no se incluyen por recomendación de PostgreSQL. Consulta [Copia de seguridad del directorio de datos](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) en la documentación de PostgreSQL para más información.

Las secciones siguientes presentan funciones adicionales del comando `restore`.


### Propiedad de los archivos {#file-ownership}

Si un `restore` se ejecuta como un usuario distinto de root (el escenario típico), todos los archivos restaurados pertenecerán al usuario/grupo que ejecuta pgBackRest. Si los archivos existentes no pertenecen al usuario/grupo que lo ejecuta, se producirá un error si la propiedad no puede actualizarse al usuario/grupo que lo ejecuta. En ese caso, la propiedad de los archivos deberá ser actualizada por un usuario con privilegios antes de reintentar la restauración.

Si un `restore` se ejecuta como el usuario `root`, pgBackRest intentará recrear la propiedad registrada en el manifiesto cuando se hizo la copia de seguridad. En el manifiesto solo se almacenan los **nombres** de usuario/grupo, por lo que los mismos nombres deben existir en el host de restauración para que esto funcione. Si el nombre de usuario/grupo no puede encontrarse localmente, se usará el usuario/grupo del directorio de datos de PostgreSQL y, por último, `root` si el usuario/grupo del directorio de datos no puede asignarse a un nombre.


### Opción delta {#delta-option}

[Restaurar una copia de seguridad](#restore-a-backup) en [Inicio rápido](#quick-start) requería limpiar el directorio del clúster de bases de datos antes de poder ejecutar el `restore`. La opción `delta` permite a pgBackRest determinar automáticamente qué archivos del directorio del clúster de bases de datos pueden conservarse y cuáles deben restaurarse desde la copia de seguridad — también *elimina* los archivos que no están presentes en el manifiesto de la copia, por lo que se deshará de los cambios divergentes. Esto se consigue calculando un hash criptográfico [SHA-1](https://en.wikipedia.org/wiki/SHA-1) para cada archivo del directorio del clúster de bases de datos. Si el hash `SHA-1` no coincide con el hash almacenado en la copia de seguridad, ese archivo se restaurará. Esta operación es muy eficiente cuando se combina con la opción `process-max`. Dado que el servidor PostgreSQL está apagado durante la restauración, puede usarse un número de procesos mayor que el que sería deseable durante una copia de seguridad con el servidor PostgreSQL en ejecución.

pg-primary **⇒** Detener el clúster de demostración y realizar una restauración delta

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/postgresql/17/demo' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/base/1/pg_internal.init'
       [filtered 769 lines of output]
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/113 - exists and matches backup (bundle 20261002-190648F/1/2665832, 8KB, 88.00%) checksum 1cd643347b87a472ff001ae124e4b532ce998d2f
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/112 - exists and matches backup (bundle 20261002-190648F/1/2665920, 8KB, 88.03%) checksum 2cbd5cf8fb22ef627eb539776c5ec7457bdb2890
P01 DETAIL: restore file /var/lib/postgresql/17/demo/PG_VERSION - exists and matches backup (bundle 20261002-190648F/1/2666008, 3B, 88.03%) checksum ad48103e4fc71796e9708cafc43adeed0d1076b7
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/5/2608_fsm - exists and matches backup (bundle 20261002-190648F/1/2666032, 24KB, 88.14%) checksum e807fe622bbfccc5e9ad7f453ecb4f0eaccb75e2
P01 DETAIL: restore file /var/lib/postgresql/17/demo/postgresql.auto.conf - exists and matches backup (bundle 20261002-190648F/1/2666272, 229B, 88.14%) checksum e1b0002d9a33d70466c5a348f4e0c1f1f80639f6
       [filtered 233 lines of output]
```

pg-primary **⇒** Reiniciar PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

### Restaurar bases de datos seleccionadas {#restore-selected-databases}

Puede haber casos en los que sea deseable restaurar de forma selectiva bases de datos específicas de una copia de seguridad del clúster. Esto puede hacerse por motivos de rendimiento o para mover bases de datos seleccionadas a una máquina que no tiene espacio suficiente para restaurar la copia completa del clúster.

Para demostrar esta función se crean dos bases de datos: test1 y test2.

pg-primary **⇒** Crear dos bases de datos de prueba

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

Cada base de datos de prueba se poblará con tablas y datos para demostrar que la recuperación funciona con la restauración selectiva.

pg-primary **⇒** Crear una tabla de prueba en cada base de datos

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

Se ejecuta una copia de seguridad nueva para que pgBackRest conozca las nuevas bases de datos.

pg-primary **⇒** Realizar una copia de seguridad

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Una de las principales razones para usar la restauración selectiva es ahorrar espacio. Aquí se muestra el tamaño de la base de datos test1 para poder compararlo con la utilización del disco después de una restauración selectiva.

pg-primary **⇒** Mostrar el espacio usado por la base de datos test1

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
7.4M	/var/lib/postgresql/17/demo/base/32768
```

Si no se conoce la base de datos a restaurar, usa la opción `set` del comando `info` para descubrir las bases de datos que forman parte del conjunto de copia de seguridad.

pg-primary **⇒** Mostrar la lista de bases de datos de la copia de seguridad

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-190648F_20261002-190702I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 1.9MB
            backup reference list: 20261002-190648F, 20261002-190648F_20261002-190654D
            database list: postgres (5), test1 (32768), test2 (32769)
```

Detén el clúster y restaura solo la base de datos test2. Las bases de datos integradas (`template0`, `template1` y `postgres`) siempre se restauran.

ADVERTENCIA:

La recuperación puede fallar con un error salvo que se especifique `--type=immediate`. Esto se debe a que, una vez alcanzada la consistencia, PostgreSQL marcará como errores las páginas rellenadas con ceros incluso para una escritura de página completa. Para PostgreSQL ≥ 13 puede usarse el parámetro ignore_invalid_pages para ignorar las páginas no válidas. En este caso es importante comprobar los registros después de la recuperación para asegurar que no se haya informado de ninguna página no válida en las bases de datos seleccionadas.

pg-primary **⇒** Restaurar desde la última copia de seguridad incluyendo solo la base de datos test2

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

Una vez completada la recuperación, la base de datos test2 contendrá todas las tablas y datos creados previamente.

pg-primary **⇒** Demostrar que la base de datos test2 se recuperó

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

La base de datos test1, a pesar de recuperarse correctamente, no es accesible. Esto se debe a que toda la base de datos se restauró como archivos dispersos rellenados con ceros. PostgreSQL puede aplicar WAL con éxito sobre los archivos rellenados con ceros, pero la base de datos en su conjunto no será válida porque los archivos clave no contienen datos. Esto es intencional, para impedir que la base de datos se use por accidente cuando podría contener datos parciales aplicados durante la reproducción del WAL.

pg-primary **⇒** Intentar conectarse a la base de datos test1 producirá un error

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

Dado que la base de datos test1 se restaura con archivos dispersos rellenados con ceros, solo requerirá tanto espacio como la cantidad de WAL que se escriba durante la recuperación. Si bien la cantidad de WAL generada durante una copia de seguridad y aplicada durante la recuperación puede ser significativa, por lo general será una pequeña fracción del tamaño total de la base de datos, especialmente para bases de datos grandes, donde esta función tiene más probabilidades de resultar útil.

Está claro que la base de datos test1 usa mucho menos espacio en disco durante la restauración selectiva del que habría usado si se hubiera restaurado la base de datos completa.

pg-primary **⇒** Mostrar el espacio usado por la base de datos test1 después de la recuperación

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
8.0K	/var/lib/postgresql/17/demo/base/32768
```

En este punto, la única acción que puede realizarse sobre la base de datos test1 no válida es `drop database`. pgBackRest no elimina la base de datos automáticamente, ya que esto no puede hacerse hasta que la recuperación se complete y el clúster sea accesible.

pg-primary **⇒** Eliminar la base de datos test1

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

Ahora que la base de datos test1 no válida ha sido eliminada, solo quedan la base de datos test2 y las bases de datos integradas.

pg-primary **⇒** Listar las bases de datos restantes

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
     4 | template0
     5 | postgres
 32769 | test2
(4 rows)
```

--------

## Recuperación en un punto en el tiempo {#point-in-time-recovery}

[Restaurar una copia de seguridad](#restore-a-backup) en [Inicio rápido](#quick-start) realizó la recuperación predeterminada, que consiste en reproducir el WAL hasta el final del flujo. En caso de un fallo de hardware esta suele ser la mejor opción, pero para escenarios de corrupción de datos (ya sean de origen de la máquina o humano) la recuperación en un punto en el tiempo (PITR) suele ser más apropiada.

La recuperación en un punto en el tiempo (PITR) permite reproducir el WAL desde una copia de seguridad hasta un lsn, una hora, un id de transacción o un punto de recuperación especificados. Para los escenarios de recuperación comunes, la recuperación basada en el tiempo es posiblemente la más útil. Un escenario de recuperación típico es restaurar una tabla que se eliminó por accidente o datos que se borraron por accidente. Recuperar una tabla eliminada es más llamativo, así que ese es el ejemplo que se da aquí, pero los datos borrados se recuperarían exactamente de la misma manera.

pg-primary **⇒** Crear una tabla con datos muy importantes

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Es importante representar la hora tal como la calcula PostgreSQL e incluir los desplazamientos de zona horaria. Esto reduce la posibilidad de conversiones de zona horaria no deseadas y de un resultado de recuperación inesperado.

pg-primary **⇒** Obtener la hora de PostgreSQL

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 19:07:12.060959+00
```

Ahora que se ha registrado la hora, se elimina la tabla. En la práctica, encontrar la hora exacta en que se eliminó la tabla es mucho más difícil que en este ejemplo. Puede que no sea posible encontrar la hora exacta, pero algo de trabajo forense debería acercarte lo suficiente.

pg-primary **⇒** Eliminar la tabla importante

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

Si se selecciona la copia de seguridad incorrecta para restaurar, la recuperación hasta el objetivo de hora requerido fallará. Para demostrarlo, se hace una nueva copia de seguridad incremental donde `important_table` no existe.

pg-primary **⇒** Realizar una copia de seguridad incremental

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-190648F_20261002-190713I
            timestamp start/stop: 2026-10-02 19:07:13+00 / 2026-10-02 19:07:14+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

No será posible recuperar la tabla perdida desde esta copia de seguridad, ya que PostgreSQL solo puede reproducir hacia adelante, no hacia atrás.

pg-primary **⇒** Intentar la recuperación desde una copia de seguridad incorrecta

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-190648F_20261002-190713I --target-timeline=current \
       --type=time "--target=2026-10-02 19:07:12.060959+00" --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

```text
       [filtered 13 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000120 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.03 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 1437) exited with exit code 1
LOG:  terminating any other active server processes
       [filtered 3 lines of output]
```

Un método fiable es permitir que pgBackRest seleccione automáticamente una copia de seguridad capaz de recuperar hasta el objetivo de hora, es decir, una copia que haya finalizado antes de la hora especificada.

NOTA:

pgBackRest no puede seleccionar automáticamente una copia de seguridad cuando el tipo de restauración es `xid` o `name`.

pg-primary **⇒** Restaurar el clúster de demostración a `2026-10-02 19:07:12.060959+00`

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 19:07:12.060959+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 19:07:12.060959+00'
recovery_target_action = 'promote'
```

pgBackRest ha generado los ajustes de recuperación en `postgresql.auto.conf`, de modo que PostgreSQL puede iniciarse de inmediato. `%f` es la forma en que PostgreSQL especifica el segmento de WAL que necesita y `%p` es la ubicación donde debe copiarse. Una vez que PostgreSQL termine la recuperación, la tabla existirá de nuevo y podrá consultarse.

pg-primary **⇒** Iniciar PostgreSQL y comprobar que la tabla importante existe

```bash
sudo pg_ctlcluster 17 demo start
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

El registro de PostgreSQL también contiene información valiosa. Indicará la hora y la transacción donde se detuvo la recuperación y también dará la hora de la última transacción aplicada.

pg-primary **⇒** Examinar la salida del registro de PostgreSQL

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 7 lines of output]
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
LOG:  starting point-in-time recovery to 2026-10-02 19:07:12.060959+00
LOG:  restored log file "00000003.history" from archive
LOG:  redo starts at 0/19000028
       [filtered 2 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "00000004000000000000001A" from archive
LOG:  recovery stopping before commit of transaction 748, time 2026-10-02 19:07:13.389359+00
LOG:  redo done at 0/1901CC00 system usage: CPU: user: 0.00 s, system: 0.01 s, elapsed: 0.07 s
LOG:  last completed transaction was at log time 2026-10-02 19:07:10.778316+00
LOG:  restored log file "000000040000000000000019" from archive
LOG:  selected new timeline ID: 5
       [filtered 5 lines of output]
```

--------

## Eliminar una stanza {#delete-a-stanza}

El comando `stanza-delete` elimina los datos del repositorio asociados a una stanza.

ADVERTENCIA:

Usa este comando con precaución — eliminará permanentemente todas las copias de seguridad y todos los archivados del repositorio de pgBackRest para la stanza especificada.

Para eliminar una stanza:

- Apaga el clúster PostgreSQL asociado a la stanza (o usa --force para omitirlo).
- Ejecuta el comando `stop` en el host donde se ejecutará el comando `stanza-delete`.
- Ejecuta el comando `stanza-delete`.

Una vez que el comando se complete con éxito, es responsabilidad del usuario eliminar la stanza de todos los archivos de configuración de pgBackRest y/o variables de entorno.

Una stanza solo puede eliminarse de un repositorio a la vez. Para eliminar la stanza de varios repositorios, repite el comando `stanza-delete` para cada repositorio especificando la opción `--repo`.

pg-primary **⇒** Detener el clúster PostgreSQL que se va a eliminar

```bash
sudo pg_ctlcluster 17 demo stop
```

pg-primary **⇒** Detener pgBackRest para la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=1568-4c984637 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** Eliminar la stanza de un repositorio

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=1576-48368d9e --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## Repositorios múltiples {#multiple-repositories}

Pueden configurarse varios repositorios como se demuestra en [Soporte de S3](#s3-compatible-object-store-support). Un beneficio potencial es la posibilidad de tener un repositorio local para restauraciones rápidas y un repositorio remoto para redundancia.

Algunos comandos, p. ej. [`stanza-create`](/es/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/es/pgbackrest/command/stanza-upgrade/), funcionarán automáticamente con todos los repositorios configurados, mientras que otros, p. ej. [`stanza-delete`](/es/pgbackrest/command/stanza-delete/), requerirán que se especifique un repositorio usando la opción `repo`.

Ten en cuenta que la opción `repo` no es necesaria cuando solo está configurado `repo1`, para mantener la compatibilidad con versiones anteriores. Sin embargo, la opción `repo` *sí* es necesaria cuando un solo repositorio está configurado como, p. ej., `repo2`. Esto es para evitar que los comandos se rompan si más adelante se añade un repositorio nuevo.

El comando `archive-push` siempre enviará WAL al archivado en todos los repositorios configurados. Cuando un repositorio no puede alcanzarse, el WAL seguirá enviándose a los demás repositorios. Sin embargo, para que esto funcione con eficacia, debe habilitarse `archive-async=y`; de lo contrario, los demás repositorios solo podrán adelantarse en un segmento de WAL al repositorio inalcanzable. Ten en cuenta también que si el WAL no puede enviarse a ningún repositorio, PostgreSQL no lo eliminará del directorio `pg_wal`, lo que puede provocar que el volumen se quede sin espacio.

Las copias de seguridad deben programarse individualmente para cada repositorio. En muchos casos esto es deseable, ya que los tipos de copia de seguridad y la retención variarán según el repositorio. Asimismo, las restauraciones deben especificar un repositorio. En general, es mejor especificar para las restauraciones un repositorio con baja latencia/costo, incluso si eso implica más tiempo de recuperación. Solo las pruebas de restauración pueden determinar qué repositorio será el más eficiente.


--------

## Soporte de almacenes de objetos compatibles con Azure {#azure-compatible-object-store-support}

pgBackRest admite ubicar repositorios en almacenes de objetos compatibles con Azure. El contenedor usado para almacenar el repositorio debe crearse por adelantado — pgBackRest no lo hará automáticamente. El repositorio puede ubicarse en la raíz del contenedor (`/`), pero por lo general es mejor colocarlo en una subruta para que los registros del almacén de objetos u otros datos puedan almacenarse también en el contenedor sin conflictos.

ADVERTENCIA:

No habilites el «espacio de nombres jerárquico» («hierarchical namespace»), ya que esto provocará errores durante la expiración.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar Azure

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

start-fast=y



[global:archive-push]

compress-level=3
```

Se pueden usar firmas de acceso compartido estableciendo la opción `repo2-azure-key-type` en `sas` y la opción `repo2-azure-key` en el token de firma de acceso compartido.

Los comandos se ejecutan exactamente igual que si el repositorio estuviera almacenado en un disco local.

pg-primary **⇒** Crear la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1657-1f40c982 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

El tiempo de creación de archivos en Azure es relativamente lento, por lo que el rendimiento de `backup`/`restore` mejora habilitando la [agrupación de archivos](#file-bundling).

pg-primary **⇒** Hacer una copia de seguridad del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1666-1ab08562 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-190727F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1666-1ab08562 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## Soporte de almacenes de objetos compatibles con S3 {#s3-compatible-object-store-support}

pgBackRest admite ubicar repositorios en almacenes de objetos compatibles con S3. El bucket usado para almacenar el repositorio debe crearse por adelantado — pgBackRest no lo hará automáticamente. El repositorio puede ubicarse en la raíz del bucket (`/`), pero por lo general es mejor colocarlo en una subruta para que los registros del almacén de objetos u otros datos puedan almacenarse también en el bucket sin conflictos.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar S3

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

start-fast=y



[global:archive-push]

compress-level=3
```

NOTA:

La región y el endpoint deberán configurarse según el lugar donde se encuentre el bucket. Los valores indicados aquí corresponden a la región `us-east-1`.

Debería crearse un rol para ejecutar pgBackRest y los permisos del bucket deberían establecerse de la forma más restrictiva posible. Si el rol está asociado a una instancia en AWS, pgBackRest recuperará automáticamente credenciales temporales cuando `repo3-s3-key-type=auto`, lo que significa que las claves no necesitan establecerse explícitamente en `/etc/pgbackrest/pgbackrest.conf`.

Esta política de ejemplo de Amazon S3 restringirá todas las lecturas y escrituras al bucket y a la ruta del repositorio.

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

Los comandos se ejecutan exactamente igual que si el repositorio estuviera almacenado en un disco local.

pg-primary **⇒** Crear la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

El tiempo de creación de archivos en S3 es relativamente lento, por lo que el rendimiento de `backup`/`restore` mejora habilitando la [agrupación de archivos](#file-bundling).

pg-primary **⇒** Hacer una copia de seguridad del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1767-6031c435 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-190741F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1767-6031c435 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## Soporte de SFTP {#sftp-support}

pgBackRest admite ubicar repositorios en hosts SFTP. La transferencia de archivos por SFTP es relativamente lenta, por lo que los comandos se benefician de aumentar `process-max` para paralelizar la transferencia de archivos.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar SFTP

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

Al utilizar SFTP, si libssh2 está compilado contra OpenSSH, entonces `repo4-sftp-public-key-file` es opcional.

pg-primary **⇒** Generar el par de claves SSH para la copia de seguridad SFTP

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** Copiar la clave pública de copia de seguridad SFTP de pg-primary a sftp-server

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

Los comandos se ejecutan exactamente igual que si el repositorio estuviera almacenado en un disco local.

pg-primary **⇒** Añadir la huella de sftp-server al archivo known_hosts dado que `repo4-sftp-host-key-check-type` tiene el valor predeterminado «strict»

```bash
ssh-keyscan -H sftp-server >> /var/lib/postgresql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** Crear la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** Hacer una copia de seguridad del clúster de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1859-efaa8e87 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-190759F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1859-efaa8e87 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## Soporte de almacenes de objetos compatibles con GCS {#gcs-compatible-object-store-support}

pgBackRest admite ubicar repositorios en almacenes de objetos compatibles con GCS. El bucket usado para almacenar el repositorio debe crearse por adelantado — pgBackRest no lo hará automáticamente. El repositorio puede ubicarse en la raíz del bucket (`/`), pero por lo general es mejor colocarlo en una subruta para que los registros del almacén de objetos u otros datos puedan almacenarse también en el bucket sin conflictos.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar GCS

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

repo5-gcs-bucket=demo-bucket

repo5-gcs-key=/etc/pgbackrest/gcs-key.json

repo5-path=/demo-repo

repo5-type=gcs

start-fast=y



[global:archive-push]

compress-level=3
```

Al ejecutar en GCE, establece `repo5-gcs-key-type=auto` para autenticarse automáticamente usando la cuenta de servicio de la instancia.

Los comandos se ejecutan exactamente igual que si el repositorio estuviera almacenado en un disco local.

El tiempo de creación de archivos en GCS es relativamente lento, por lo que el rendimiento de `backup`/`restore` mejora habilitando la [agrupación de archivos](#file-bundling).


--------

## Hora objetivo para el repositorio {#target-time-for-repository}

La hora objetivo define la hora que usan los comandos para leer un repositorio en almacenamiento con versiones. Esto permite que el comando lea el repositorio tal como estaba en un punto en el tiempo, para así recuperar datos que hayan sido eliminados o corrompidos por accidente del usuario o por malware.

El almacenamiento con versiones está soportado por S3, GCS y Azure, pero por lo general no está habilitado por defecto. Además de habilitar el versionado, puede ser útil habilitar el bloqueo de objetos para S3 y el borrado suave (soft delete) para GCS o Azure.

Cuando se especifica la opción `repo-target-time`, también debe proporcionarse la opción `repo`. Es probable que no todos los tipos de repositorio admitan el versionado y, en general, tiene sentido fijar como objetivo un único repositorio para la recuperación.

Ten en cuenta que las comparaciones con la marca de tiempo del almacenamiento son <= a la marca de tiempo proporcionada y que los milisegundos se truncan de la marca de tiempo cuando se proporciona.

Para demostrar esta función se elimina la stanza `demo` del repositorio S3.

pg-primary **⇒** Eliminar la stanza del repositorio S3

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

Una vez eliminada la stanza, el comando `info` mostrará el repositorio en estado de error.

pg-primary **⇒** Error en info

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

Sin embargo, dado que el almacenamiento tiene versiones, es posible mirar el repositorio en un momento anterior a la eliminación de la stanza. Encontrar la hora objetivo puede ser complicado según la situación, pero en este caso la hora en que se eliminó la stanza puede determinarse comprobando cuándo se eliminó `backup.info`.

pg-primary **⇒** Listar las versiones de `backup.info` en el bucket

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
-----------------------------------------------------------------------------
|                            ListObjectVersions                             |
+--------+----------------------------+-------------------------------------+
| Action |         Modified           |               Object                |
+--------+----------------------------+-------------------------------------+
|  PUT   |  2026-10-02T19:07:41.474Z  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T19:07:56.815Z  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T19:08:04.878Z  |  demo-repo/backup/demo/backup.info  |
+--------+----------------------------+-------------------------------------+
```

Ahora puede ejecutarse el comando `info` con una hora objetivo que mostrará el repositorio antes de su eliminación.

pg-primary **⇒** Info con hora objetivo

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 19:07:57+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (17): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-190741F
            timestamp start/stop: 2026-10-02 19:07:41+00 / 2026-10-02 19:07:56+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 3.8MB, backup size: 3.8MB
```

Si el comando `info` muestra la copia de seguridad requerida, esta puede restaurarse usando la misma hora objetivo.

pg-primary **⇒** Restaurar con hora objetivo

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 19:07:57+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=1953-a0a01a5a --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 19:07:57+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-190741F, recovery will start at 2026-10-02 19:07:41
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00   INFO: write updated /var/lib/postgresql/17/demo/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo pg_ctlcluster 17 demo start
```

--------

## Host de repositorio dedicado {#dedicated-repository-host}

La configuración descrita en [Inicio rápido](#quick-start) es adecuada para instalaciones sencillas, pero para configuraciones empresariales es más típico tener un host de repositorio dedicado donde se almacenan las copias de seguridad y los archivos del archivado de WAL. Esto separa las copias de seguridad y el archivado de WAL del servidor de bases de datos, de modo que los fallos del host de bases de datos tienen menos impacto. Sigue siendo buena idea emplear software de copia de seguridad tradicional para respaldar el host del repositorio.

En los hosts de PostgreSQL, se exige que `pg1-path` sea la ruta del clúster PostgreSQL local y no debería configurarse ningún `pg1-host`. Al configurar un host de repositorio, el archivo de configuración de pgbackrest debe tener la opción `pg-host` configurada para conectarse a los hosts primario y standby (si existe). El host del repositorio tiene la única configuración de pgbackrest que debería conocer más de un host PostgreSQL. El orden no importa, p. ej. pg1-path/pg1-host, pg2-path/pg2-host pueden ser primario o standby.


### Instalación {#installation-1}

Se crea un nuevo host llamado repository para almacenar las copias de seguridad del clúster.

NOTA:

La versión de pgBackRest instalada en el host del repositorio debe coincidir exactamente con la versión instalada en el host de PostgreSQL.

Se crea el usuario `pgbackrest` como propietario del repositorio de pgBackRest. Cualquier usuario puede ser propietario del repositorio, pero es mejor no usar `postgres` (si existe) para evitar confusiones.

NOTA:

Cuando pgBackRest se instala desde un paquete, puede proporcionarse una configuración de logrotate como `/etc/logrotate.d/pgbackrest` que rota los registros como un usuario específico mediante la directiva `su` (p. ej. `su postgres postgres`). Dado que los archivos en `/var/log/pgbackrest` pertenecen al usuario que ejecuta pgBackRest (aquí `pgbackrest`), la directiva `su` debe actualizarse para que coincida con este usuario, o de lo contrario logrotate fallará con un error de permisos.

repository **⇒** Crear el usuario `pgbackrest`

```bash
sudo adduser --disabled-password --gecos "" pgbackrest
```

Instalar pgBackRest desde un paquete es preferible a compilarlo desde el código fuente. Al instalar desde un paquete, el resto de las instrucciones de esta sección generalmente no son necesarias, pero es posible que un paquete omita la creación de uno de los directorios o aplique permisos incorrectos. En ese caso, puede ser necesario crear directorios manualmente o actualizar los permisos.

Los paquetes de pgBackRest para Debian/Ubuntu están disponibles en [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si no se proporcionan paquetes para tu distribución/versión, puedes [compilar desde el código fuente](#build) y luego instalar manualmente como se muestra aquí.

repository **⇒** Instalar dependencias

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

repository **⇒** Copiar el binario de pgBackRest desde el host de compilación

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest requiere directorios de registro y de configuración, además de un archivo de configuración.

repository **⇒** Crear el archivo de configuración y los directorios de pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

repository **⇒** Crear el repositorio de pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### Configurar SSH sin contraseña {#setup-passwordless-ssh}

pgBackRest puede usar SSH sin contraseña para habilitar la comunicación entre los hosts. También es posible usar TLS; consulta [Configurar TLS](/es/pgbackrest/user-guide-rhel/#configuration).

repository **⇒** Crear el par de claves del host repository

```bash
sudo -u pgbackrest mkdir -m 750 /home/pgbackrest/.ssh
sudo -u pgbackrest ssh-keygen -f /home/pgbackrest/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

pg-primary **⇒** Crear el par de claves del host pg-primary

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Intercambia las claves entre repository y pg-primary.

repository **⇒** Copiar la clave pública de pg-primary a repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-primary **⇒** Copiar la clave pública de repository a pg-primary

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Comprueba que puedan establecerse conexiones de repository a pg-primary y viceversa.

repository **⇒** Probar la conexión de repository a pg-primary

```bash
sudo -u pgbackrest ssh postgres@pg-primary
```

pg-primary **⇒** Probar la conexión de pg-primary a repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

NOTA:

ssh se ha configurado para permitir que solo se ejecute pgBackRest mediante ssh sin contraseña. Esto mejora la seguridad en caso de que una de las cuentas de servicio sea comprometida.


### Configuración {#configuration}

El host del repositorio debe configurarse con el host/usuario de pg-primary y la ruta de la base de datos. El primario se configurará como `pg1` para permitir añadir un standby más adelante.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `pg1-host`/`pg1-host-user` y `pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

El host de la base de datos debe configurarse con el host/usuario del repositorio. El valor predeterminado de la opción `repo1-host-user` es `pgbackrest`. Si el usuario `postgres` hace restauraciones en el host del repositorio, es mejor no permitir también que el usuario `postgres` haga copias de seguridad. Sin embargo, el usuario `postgres` puede leer el repositorio directamente si está en el mismo grupo que el usuario `pgbackrest`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `repo1-host`/`repo1-host-user`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

La configuración de PostgreSQL puede encontrarse en la sección [Configurar el archivado](#configure-archiving).

Los comandos se ejecutan igual que en una configuración de un solo host, excepto que algunos comandos como `backup` y `expire` se ejecutan desde el host del repositorio en lugar del host de la base de datos.


### Crear y comprobar la stanza {#create-and-check-stanza}

Crea la stanza en el repositorio nuevo.

repository **⇒** Crear la stanza

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

Comprueba que la configuración sea correcta tanto en el host de la base de datos como en el del repositorio. Puede encontrarse más información sobre el comando `check` en [Comprobar la configuración](#check-the-configuration).

pg-primary **⇒** Comprobar la configuración

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

repository **⇒** Comprobar la configuración

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### Realizar una copia de seguridad {#perform-a-backup-1}

Para hacer una copia de seguridad del clúster PostgreSQL, ejecuta pgBackRest con el comando `backup` en el host del repositorio.

repository **⇒** Hacer una copia de seguridad del clúster de demostración

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

Dado que se creó un repositorio nuevo en el host del repositorio, se emitió la advertencia sobre el cambio de la copia de seguridad incremental a una copia completa.


### Restaurar una copia de seguridad {#restore-a-backup-1}

Para realizar una restauración del clúster PostgreSQL, ejecuta pgBackRest con el comando `restore` en el host de la base de datos.

pg-primary **⇒** Detener el clúster de demostración, restaurar y reiniciar PostgreSQL

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo pg_ctlcluster 17 demo start
```

--------

## Copia de seguridad / restauración en paralelo {#parallel-backup--restore}

pgBackRest ofrece procesamiento en paralelo para mejorar el rendimiento de la compresión y la transferencia. El número de procesos que se usarán para esta función se establece con la opción `--process-max`.

Por lo general, es mejor no usar más del 25% de las CPU disponibles para el comando `backup`. Las copias de seguridad no tienen que ejecutarse tan rápido siempre que se hagan con regularidad, y el proceso de copia de seguridad no debería afectar al rendimiento de la base de datos, si es posible evitarlo.

El comando restore puede y debe usar todas las CPU disponibles, porque durante una restauración el clúster PostgreSQL está apagado y por lo general no hay otro trabajo importante en el host. Si el host contiene varios clústeres, esto debería tenerse en cuenta al establecer el paralelismo de la restauración.

repository **⇒** Realizar una copia de seguridad con un solo proceso

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar pgBackRest para usar múltiples procesos de `backup`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

repository **⇒** Realizar una copia de seguridad con múltiples procesos

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** Obtener información de la copia de seguridad del clúster de demostración

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (17): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-190844F
            timestamp start/stop: 2026-10-02 19:08:44+00 / 2026-10-02 19:08:48+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 29.2MB, database backup size: 29.2MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB

        full backup: 20261002-190850F
            timestamp start/stop: 2026-10-02 19:08:50+00 / 2026-10-02 19:08:52+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 29.2MB, database backup size: 29.2MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB
```

El rendimiento de la última copia de seguridad debería mejorar usando múltiples procesos. Para copias de seguridad muy pequeñas la diferencia puede no ser muy evidente, pero a medida que aumenta el tamaño de la base de datos, también lo harán los ahorros de tiempo.


--------

## Inicio y detención {#starting-and-stopping}

Si un standby se promueve para pruebas, o si un clúster de prueba se restaura desde una copia de seguridad de producción, es buena idea impedir que esos clústeres escriban en los repositorios de pgBackRest. Esto puede lograrse con el comando `stop`.

Los comandos que escriben y quedan bloqueados por `stop` son: `archive-push`, `backup`, `expire`, `stanza-create` y `stanza-upgrade`. Ten en cuenta que `stanza-delete` es una excepción a esta regla (consulta [Eliminar una stanza](#delete-a-stanza) para más detalles).

pg-primary **⇒** Detener los comandos de escritura de pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

Los nuevos comandos de escritura de pgBackRest ya no se ejecutarán.

repository **⇒** Intentar hacer una copia de seguridad

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

Especifica la opción `--force` para terminar cualquier comando de escritura de pgBackRest que esté actualmente en ejecución. Esto incluye el archive-get asíncrono (aunque volverá a ejecutarse si PostgreSQL lo requiere). Si pgBackRest ya está detenido, detenerlo de nuevo generará una advertencia.

pg-primary **⇒** Detener de nuevo los servicios de pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

Inicia de nuevo los comandos de escritura de pgBackRest con el comando `start`. Los comandos de escritura que estaban en curso antes de la detención no se reiniciarán automáticamente, pero ahora sí se les permite iniciarse.

pg-primary **⇒** Iniciar los comandos de escritura de pgBackRest

```bash
sudo -u postgres pgbackrest start
```

También es posible detener pgBackRest para una sola stanza.

pg-primary **⇒** Detener los comandos de escritura de pgBackRest para la stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

Los nuevos comandos de escritura de pgBackRest para la stanza especificada ya no se ejecutarán.

repository **⇒** Intentar hacer una copia de seguridad

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

La stanza también debe especificarse al iniciar los comandos de escritura de pgBackRest para una sola stanza.

pg-primary **⇒** Iniciar los comandos de escritura de pgBackRest para la stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## Replicación {#replication}

La replicación permite crear múltiples copias de un clúster PostgreSQL (llamadas standbys) a partir de un único primario. Los standbys son útiles para balancear las lecturas y para proporcionar redundancia en caso de que falle el host primario.


### Instalación {#installation-2}

Se crea un nuevo host llamado pg-standby para ejecutar el standby.

Instalar pgBackRest desde un paquete es preferible a compilarlo desde el código fuente. Al instalar desde un paquete, el resto de las instrucciones de esta sección generalmente no son necesarias, pero es posible que un paquete omita la creación de uno de los directorios o aplique permisos incorrectos. En ese caso, puede ser necesario crear directorios manualmente o actualizar los permisos.

Los paquetes de pgBackRest para Debian/Ubuntu están disponibles en [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si no se proporcionan paquetes para tu distribución/versión, puedes [compilar desde el código fuente](#build) y luego instalar manualmente como se muestra aquí.

pg-standby **⇒** Instalar dependencias

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-standby **⇒** Copiar el binario de pgBackRest desde el host de compilación

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest requiere directorios de registro y de configuración, además de un archivo de configuración.

pg-standby **⇒** Crear el archivo de configuración y los directorios de pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Configurar SSH sin contraseña {#setup-passwordless-ssh-1}

pgBackRest puede usar SSH sin contraseña para habilitar la comunicación entre los hosts. También es posible usar TLS; consulta [Configurar TLS](/es/pgbackrest/user-guide-rhel/#configuration).

pg-standby **⇒** Crear el par de claves del host pg-standby

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Intercambia las claves entre repository y pg-standby.

repository **⇒** Copiar la clave pública de pg-standby a repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-standby cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-standby **⇒** Copiar la clave pública de repository a pg-standby

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Comprueba que puedan establecerse conexiones de repository a pg-standby y viceversa.

repository **⇒** Probar la conexión de repository a pg-standby

```bash
sudo -u pgbackrest ssh postgres@pg-standby
```

pg-standby **⇒** Probar la conexión de pg-standby a repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

### Standby en caliente {#hot-standby}

Un standby en caliente realiza la replicación usando el archivado de WAL y permite consultas de solo lectura.

La configuración de pgBackRest es muy similar a la de pg-primary, excepto que se usará el tipo de recuperación `standby` para mantener el clúster en modo recuperación cuando se alcance el final del flujo de WAL.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar pgBackRest en el standby

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

El clúster de demostración debe crearse (aunque se sobrescribirá al restaurar) para poder crear los archivos de configuración de PostgreSQL.

pg-standby **⇒** Crear el clúster de demostración

```bash
sudo pg_createcluster 17 demo
```

Ahora puede crearse el standby con el comando `restore`.

IMPORTANTE:

Si se pretende promover el clúster sin que se convierta en el nuevo primario (p. ej. para informes o pruebas), usa `--archive-mode=off` o establece archive_mode=off en `postgresql.conf` para deshabilitar el archivado. Si el archivado no se deshabilita, el repositorio puede contaminarse con WAL que puede dificultar las restauraciones.

pg-standby **⇒** Restaurar el clúster standby de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:30
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:56
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_time = '2026-10-02 19:07:12.060959+00'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:10
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 19:07:57+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:37
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:09:08
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

La configuración es por si el standby se promueve a primario.

pg-standby:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurar PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

pg-standby **⇒** Iniciar PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

El registro de PostgreSQL da información valiosa sobre la recuperación. Observa en especial que el clúster ha entrado en modo standby y está listo para aceptar conexiones de solo lectura.

pg-standby **⇒** Examinar la salida del registro de PostgreSQL en busca de mensajes que indiquen éxito

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 6 lines of output]
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
LOG:  entering standby mode
LOG:  redo starts at 0/24000028
LOG:  restored log file "000000070000000000000025" from archive
       [filtered 3 lines of output]
```

Una forma sencilla de comprobar que la replicación está correctamente configurada es crear una tabla en pg-primary.

pg-primary **⇒** Crear una tabla nueva en el primario

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Y luego consultar la misma tabla en pg-standby.

pg-standby **⇒** Consultar la tabla nueva en el standby

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

Entonces, ¿qué salió mal? Dado que PostgreSQL obtiene segmentos de WAL del archivado para realizar la replicación, los cambios no se verán en el standby hasta que el segmento de WAL que los contiene se envíe desde pg-primary.

Esto puede hacerse manualmente llamando a `pg_switch_wal()`, que envía el segmento de WAL actual al archivado (se crea un segmento de WAL nuevo para contener los cambios posteriores).

pg-primary **⇒** Llamar a `pg_switch_wal()`

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/26019600    | 2026-10-02 19:09:16.993398+00
(1 row)
```

Ahora, tras un breve retardo, la tabla aparecerá en pg-standby.

pg-standby **⇒** Ahora la tabla nueva existe en el standby (puede requerir algunos reintentos)

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:09:22.793715+00
(1 row)
```

Comprueba la configuración del standby para el acceso al repositorio.

pg-standby **⇒** Comprobar la configuración

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=654-6b53cbe6 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### Replicación por streaming {#streaming-replication}

En lugar de depender únicamente del archivado de WAL, la replicación por streaming establece una conexión directa con el primario y aplica los cambios tan pronto como se hacen en el primario. Esto resulta en mucho menos desfase entre el primario y el standby.

La replicación por streaming requiere un usuario con el privilegio de replicación.

pg-primary **⇒** Crear el usuario de replicación

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

El archivo `pg_hba.conf` debe actualizarse para permitir que el standby se conecte como el usuario de replicación. Asegúrate de reemplazar la dirección IP siguiente con la dirección IP real de tu pg-standby. Se requerirá una recarga después de modificar el archivo `pg_hba.conf`.

pg-primary **⇒** Crear la entrada de `pg_hba.conf` para el usuario de replicación

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /etc/postgresql/17/demo/pg_hba.conf'
sudo pg_ctlcluster 17 demo reload
```

El standby necesita saber cómo contactar con el primario, por lo que el parámetro primary_conninfo se configurará en pgBackRest.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Establecer primary_conninfo

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository
```

Es posible configurar una contraseña en el parámetro primary_conninfo, pero usar un archivo `.pgpass` es más flexible y seguro.

pg-standby **⇒** Configurar la contraseña de replicación en el archivo `.pgpass`

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/postgresql/.pgpass'
sudo -u postgres chmod 600 /var/lib/postgresql/.pgpass
```

Ahora puede crearse el standby con el comando `restore`.

pg-standby **⇒** Detener PostgreSQL y restaurar el clúster standby de demostración

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:30
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:56
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_time = '2026-10-02 19:07:12.060959+00'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:10
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 19:07:57+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:37
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:09:25
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

NOTA:

El parámetro primary_conninfo se ha escrito en el archivo `postgresql.auto.conf` porque se configuró como `recovery-option` en `pgbackrest.conf`. La opción `--type=preserve` puede usarse con el `restore` para dejar el archivo `postgresql.auto.conf` existente en su lugar si se prefiere ese comportamiento.

pg-standby **⇒** Iniciar PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

El registro de PostgreSQL confirmará que la replicación por streaming ha comenzado.

pg-standby **⇒** Examinar la salida del registro de PostgreSQL en busca de mensajes que indiquen éxito

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 13 lines of output]
LOG:  consistent recovery state reached at 0/25000050
LOG:  database system is ready to accept read-only connections
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

Ahora, cuando se crea una tabla en pg-primary, aparecerá en pg-standby rápidamente y sin necesidad de llamar a `pg_switch_wal()`.

pg-primary **⇒** Crear una tabla nueva en el primario

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:09:32.302145+00
(1 row)
```

pg-standby **⇒** Consultar la tabla en el standby

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:09:32.491307+00
(1 row)
```

--------

## Stanzas múltiples {#multiple-stanzas}

pgBackRest admite múltiples stanzas. El uso más común es compartir un host de repositorio entre varias stanzas.


### Instalación {#installation-3}

Se crea un nuevo host llamado pg-alt para ejecutar el nuevo primario.

Instalar pgBackRest desde un paquete es preferible a compilarlo desde el código fuente. Al instalar desde un paquete, el resto de las instrucciones de esta sección generalmente no son necesarias, pero es posible que un paquete omita la creación de uno de los directorios o aplique permisos incorrectos. En ese caso, puede ser necesario crear directorios manualmente o actualizar los permisos.

Los paquetes de pgBackRest para Debian/Ubuntu están disponibles en [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

Si no se proporcionan paquetes para tu distribución/versión, puedes [compilar desde el código fuente](#build) y luego instalar manualmente como se muestra aquí.

pg-alt **⇒** Instalar dependencias

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-alt **⇒** Copiar el binario de pgBackRest desde el host de compilación

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest requiere directorios de registro y de configuración, además de un archivo de configuración.

pg-alt **⇒** Crear el archivo de configuración y los directorios de pgBackRest

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Configurar SSH sin contraseña {#setup-passwordless-ssh-2}

pgBackRest puede usar SSH sin contraseña para habilitar la comunicación entre los hosts. También es posible usar TLS; consulta [Configurar TLS](/es/pgbackrest/user-guide-rhel/#configuration).

pg-alt **⇒** Crear el par de claves del host pg-alt

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

Intercambia las claves entre repository y pg-alt.

repository **⇒** Copiar la clave pública de pg-alt a repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-alt cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-alt **⇒** Copiar la clave pública de repository a pg-alt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

Comprueba que puedan establecerse conexiones de repository a pg-alt y viceversa.

repository **⇒** Probar la conexión de repository a pg-alt

```bash
sudo -u pgbackrest ssh postgres@pg-alt
```

pg-alt **⇒** Probar la conexión de pg-alt a repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

### Configuración {#configuration-1}

La configuración de pgBackRest es casi idéntica a la de pg-primary, excepto que se usará la stanza `demo-alt`, de modo que las copias de seguridad y el archivado se almacenarán en una ubicación separada.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar pgBackRest en el nuevo primario

```ini
[demo-alt]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `pg1-host`/`pg1-host-user` y `pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

### Configurar el clúster de demostración {#setup-demo-cluster-1}

pg-alt **⇒** Crear el clúster de demostración

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 102:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

pg-alt:`/etc/postgresql/17/demo/postgresql.conf` **⇒** Configurar los parámetros de PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on
```

pg-alt **⇒** Iniciar el clúster de demostración

```bash
sudo pg_ctlcluster 17 demo restart
```

### Crear la stanza y comprobar la configuración {#create-the-stanza-and-check-configuration}

Debe ejecutarse el comando `stanza-create` para inicializar la stanza. Se recomienda ejecutar el comando `check` después de `stanza-create` para asegurar que el archivado y las copias de seguridad estén correctamente configurados.

pg-alt **⇒** Crear la stanza y comprobar la configuración

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=386-f644abb9 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=396-8c7be3ca --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000001-ef9bc7e061e42fae1596a4f23d34fdb78ee324d0.gz' on repo1
P00   INFO: check command end: completed successfully
```

Si el comando `check` se ejecuta desde el host del repositorio, se comprobarán todas las stanzas.

repository **⇒** Comprobar la configuración de todas las stanzas

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1284-38748c52 --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/000000070000000000000027-f89bb62652ecba95477379768079564b0243a0d3.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000002-de2b6314bf64b956ede5fad9e01f3d5f0200faff.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## Archivado asíncrono {#asynchronous-archiving}

El archivado asíncrono se habilita con la opción `archive-async`. Esta opción habilita la operación asíncrona tanto para el comando `archive-push` como para el `archive-get`.

Se requiere una ruta de spool. Los comandos almacenarán aquí datos transitorios, pero cada comando funciona de forma bastante diferente, por lo que el uso de la ruta de spool se describe en detalle en cada sección.

pg-primary **⇒** Crear el directorio de spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** Crear el directorio de spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

La ruta de spool debe configurarse y el archivado asíncrono habilitarse. El archivado asíncrono aporta automáticamente algún beneficio al reducir el número de conexiones al almacenamiento remoto, pero establecer `process-max` puede mejorar drásticamente el rendimiento al paralelizar las operaciones. Asegúrate de no establecer `process-max` tan alto que afecte a las operaciones normales de la base de datos.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar la ruta de spool y el archivado asíncrono

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar la ruta de spool y el archivado asíncrono

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

NOTA:

`process-max` se configura usando secciones de comando para que la opción no sea usada por backup y restore. Esto también permite valores diferentes para `archive-push` y `archive-get`.

Para fines de demostración, se romperá la replicación por streaming para forzar a PostgreSQL a obtener WAL usando restore_command.

pg-primary **⇒** Romper la replicación por streaming cambiando la contraseña de replicación

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** Reiniciar el standby para romper la conexión

```bash
sudo pg_ctlcluster 17 demo restart
```

### Envío al archivado {#archive-push}

El comando `archive-push` asíncrono descarga el archivado de WAL en un proceso (o procesos) separado para mejorar el rendimiento. Funciona «mirando hacia adelante» para ver qué segmentos de WAL están listos para archivarse más allá de la solicitud que PostgreSQL está haciendo actualmente mediante el `archive_command`. Los segmentos de WAL se transfieren al archivado directamente desde el directorio `pg_xlog`/`pg_wal` y el `archive_command` solo devuelve éxito cuando el segmento de WAL se ha almacenado de forma segura en el archivado.

La ruta de spool contiene el estado actual del archivado de WAL. Los archivos de estado escritos en el directorio de spool suelen tener longitud cero y deberían consumir una cantidad mínima de espacio (unos pocos MB como máximo) y muy poca E/S. Toda la información de este directorio puede recrearse, por lo que no es necesario conservar el directorio de spool si el clúster se mueve a hardware nuevo.

IMPORTANTE:

En la implementación original del archivado asíncrono, los segmentos de WAL se copiaban al directorio de spool antes de la compresión y la transferencia. La nueva implementación copia el WAL directamente desde el directorio `pg_xlog`. Si se utilizó el archivado asíncrono en la v1.12 o anteriores, lee cuidadosamente las notas de la versión v1.13 antes de actualizar.

El archivo `[stanza]-archive-push-async.log` puede usarse para supervisar la actividad del proceso asíncrono. Una buena forma de probarlo es enviar rápidamente varios segmentos de WAL.

pg-primary **⇒** Probar el archivado asíncrono en paralelo

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=2590-c51c0441 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/00000007000000000000002D-1ed494e7471557cb0563baa2af44d9e1252e424f.gz' on repo1
P00   INFO: check command end: completed successfully
```

Ahora el archivo de registro contendrá actividad asíncrona y en paralelo.

pg-primary **⇒** Comprobar los resultados en el registro

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2576-267f2388 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2594-5115f5d8 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00   INFO: archive-push:async command end: completed successfully
```

### Obtención desde el archivado {#archive-get}

El comando `archive-get` asíncrono mantiene una cola local de WAL para mejorar el rendimiento. Si no se encuentra un segmento de WAL en la cola, se obtiene del repositorio junto con suficiente WAL consecutivo para llenar la cola. El tamaño máximo de la cola lo define `archive-get-queue-max`. Siempre que la cola esté menos de la mitad llena, se obtendrá más WAL para llenarla.

La operación asíncrona es más útil en entornos que generan mucho WAL o que tienen una conexión de alta latencia al almacenamiento del repositorio (es decir, S3 u otros almacenes de objetos). En el caso de una conexión de alta latencia, puede ser buena idea aumentar `process-max`.

El archivo `[stanza]-archive-get-async.log` puede usarse para supervisar la actividad del proceso asíncrono.

pg-standby **⇒** Comprobar los resultados en el registro

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=871-5afe1731 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P02 DETAIL: found 000000070000000000000025 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000024 in the repo1: 17-1 archive
P02 DETAIL: found 000000070000000000000026 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000027 in the repo1: 17-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00   INFO: archive-get:async command end: completed successfully
       [filtered 14 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=924-87ccaa43 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P02 DETAIL: found 000000070000000000000029 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000028 in the repo1: 17-1 archive
P02 DETAIL: found 00000007000000000000002A in the repo1: 17-1 archive
P01 DETAIL: found 00000007000000000000002B in the repo1: 17-1 archive
P02 DETAIL: found 00000007000000000000002C in the repo1: 17-1 archive
P01 DETAIL: found 00000007000000000000002D in the repo1: 17-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00   INFO: archive-get:async command end: completed successfully
       [filtered 15 lines of output]
```

pg-primary **⇒** Reparar la replicación por streaming cambiando la contraseña de replicación

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## Copia de seguridad desde un standby {#backup-from-a-standby}

pgBackRest puede hacer copias de seguridad en un standby en lugar de en el primario. Las copias de seguridad desde standby requieren que el host pg-standby esté configurado y la opción `backup-standby` habilitada. Si se configura más de un standby, se usará para la copia de seguridad el primer standby en ejecución que se encuentre.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Configurar `pg2-host`/`pg2-host-user` y `pg2-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/17/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

Se requieren tanto la base de datos primaria como la standby para hacer la copia de seguridad, aunque la gran mayoría de los archivos se copiarán desde el standby para reducir la carga del primario. Los hosts de bases de datos pueden configurarse en cualquier orden. pgBackRest determinará automáticamente cuál es el primario y cuál el standby.

repository **⇒** Hacer una copia de seguridad del clúster de demostración desde pg2

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P03 DETAIL: backup file pg-standby:/var/lib/postgresql/17/demo/base/5/2658 (128KB, 8.47%) checksum 6bcdcabc7aaf3e4919655612f77833a1612baf01
P01 DETAIL: backup file pg-primary:/var/lib/postgresql/17/demo/global/pg_control (8KB, 8.99%) checksum aa003dff0afea4b06a88d00138da8e948a563345
P04 DETAIL: backup file pg-standby:/var/lib/postgresql/17/demo/base/5/1247 (120KB, 16.93%) checksum fa2fb6657bf9785e320a8a5516851de78d7a7a33
P01 DETAIL: match file from prior backup pg-primary:/var/lib/postgresql/17/demo/pg_logical/replorigin_checkpoint (8B, 16.93%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1277 lines of output]
```

Esta copia de seguridad incremental muestra que la mayoría de los archivos se copian desde el host pg-standby y solo unos pocos se copian desde el host pg-primary.

pgBackRest crea una copia de seguridad desde standby idéntica a una copia realizada en el primario. Lo hace iniciando/deteniendo la copia de seguridad en el host pg-primary, copiando solo los archivos que están replicados desde el host pg-standby y copiando luego los pocos archivos restantes desde el host pg-primary. Esto significa que los registros y las estadísticas de la base de datos primaria se incluirán en la copia de seguridad.


--------

## Actualización de PostgreSQL {#upgrading-postgresql}

Inmediatamente después de actualizar PostgreSQL a una nueva versión principal, el `pg-path` de todas las configuraciones de pgBackRest debe establecerse en la nueva ubicación de la base de datos y ejecutarse el comando `stanza-upgrade`. Si hay más de un repositorio configurado en el host, la stanza se actualizará en cada uno. Si la base de datos está fuera de línea, usa la opción `--no-online`.

Las instrucciones siguientes no pretenden ser una guía exhaustiva para actualizar PostgreSQL; más bien describen el proceso general para actualizar un primario y un standby con la intención de demostrar los pasos necesarios para reconfigurar pgBackRest. Se recomienda hacer una copia de seguridad antes de actualizar.

pg-primary **⇒** Detener el clúster antiguo

```bash
sudo pg_ctlcluster 17 demo stop
```

Detén el clúster antiguo en el standby, ya que se restaurará desde el clúster recién actualizado.

pg-standby **⇒** Detener el clúster antiguo

```bash
sudo pg_ctlcluster 17 demo stop
```

Crea el clúster nuevo y realiza la actualización.

pg-primary **⇒** Crear el clúster nuevo y realizar la actualización

```bash
sudo -u postgres /usr/lib/postgresql/18/bin/initdb \
       -D /var/lib/postgresql/18/demo -k -A peer
sudo pg_createcluster 18 demo
sudo -u postgres sh -c 'cd /var/lib/postgresql && \
       /usr/lib/postgresql/18/bin/pg_upgrade \
       --old-bindir=/usr/lib/postgresql/17/bin \
       --new-bindir=/usr/lib/postgresql/18/bin \
       --old-datadir=/var/lib/postgresql/17/demo \
       --new-datadir=/var/lib/postgresql/18/demo \
       --old-options=" -c config_file=/etc/postgresql/17/demo/postgresql.conf" \
       --new-options=" -c config_file=/etc/postgresql/18/demo/postgresql.conf"'
```

```text
       [filtered 44 lines of output]
Checking for extension updates                                ok
Upgrade Complete
----------------
Some statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

Configura los ajustes y el puerto del clúster nuevo.

pg-primary:`/etc/postgresql/18/demo/postgresql.conf` **⇒** Configurar PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

Actualiza la configuración de pgBackRest en todos los sistemas para que apunte al clúster nuevo.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Actualizar el `pg1-path`

```ini
[demo]

pg1-path=/var/lib/postgresql/18/demo



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Actualizar el `pg-path`

```ini
[demo]

pg1-path=/var/lib/postgresql/18/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Actualizar `pg1-path` y `pg2-path`, deshabilitar la copia de seguridad desde standby

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/18/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/18/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

pg-primary **⇒** Copiar la configuración hba

```bash
sudo cp /etc/postgresql/17/demo/pg_hba.conf \
       /etc/postgresql/18/demo/pg_hba.conf
```

Antes de iniciar el clúster nuevo, debe ejecutarse el comando `stanza-upgrade`.

pg-primary **⇒** Actualizar la stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=3025-70610f0d --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/postgresql/18/demo --repo1-host=repository --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

Inicia el clúster nuevo y confirma que se haya instalado correctamente.

pg-primary **⇒** Iniciar el clúster nuevo

```bash
sudo pg_ctlcluster 18 demo start
```

Prueba la configuración usando el comando `check`.

pg-primary **⇒** Comprobar la configuración

```bash
sudo pg_lsclusters
sudo -u postgres pgbackrest --stanza=demo check
```

Elimina el clúster antiguo.

pg-primary **⇒** Eliminar el clúster antiguo

```bash
sudo pg_dropcluster 17 demo
```

Instala los binarios de PostgreSQL nuevos en el standby y crea el clúster.

pg-standby **⇒** Eliminar el clúster antiguo y crear el clúster nuevo

```bash
sudo pg_dropcluster 17 demo
sudo pg_createcluster 18 demo
```

Ejecuta el `check` en el host del repositorio. La advertencia sobre que el standby está apagado es de esperar, ya que el clúster standby está apagado. Ejecutar este comando demuestra que el servidor del repositorio conoce el standby y está correctamente configurado para el servidor primario.

repository **⇒** Comprobar la configuración

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 ssh protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

Ejecuta una copia de seguridad completa en el clúster nuevo y luego restaura el standby desde la copia. El tipo de copia de seguridad se cambiará automáticamente a `full` si se solicita `incr` o `diff`.

repository **⇒** Ejecutar una copia de seguridad completa

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** Restaurar el clúster standby de demostración

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
```

pg-standby **⇒** Iniciar PostgreSQL y comprobar la configuración de pgBackRest

```bash
sudo pg_ctlcluster 18 demo start
sudo -u postgres pgbackrest --stanza=demo check
```

La copia de seguridad desde standby puede habilitarse ahora que el standby está restaurado.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Volver a habilitar la copia de seguridad desde standby

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/18/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/18/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```
