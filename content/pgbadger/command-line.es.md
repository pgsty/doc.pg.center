---
title: "Referencia de la línea de comandos"
linkTitle: "Línea de comandos"
weight: 30
description: "Sintaxis completa de los comandos de pgBadger, opciones, entrada remota, códigos de retorno y ejemplos"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Referencia]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## Uso y opciones {#usage-and-options}

Uso: pgbadger [options] logfile [...]

```text
Analizador de registros de PostgreSQL con informes y gráficos totalmente detallados.
```

Argumentos:

```text
logfile puede ser un solo archivo de registro, una lista de archivos o un
comando de shell que devuelva una lista de archivos. Si deseas pasar
contenido del registro desde stdin, usa - como nombre de archivo. Ten en
cuenta que la entrada desde stdin no funcionará con csvlog.
```

Opciones:

```text
-a | --average minutes : número de minutos para construir los gráficos de
                         promedios de consultas y conexiones. Por defecto: 5 minutos.
-A | --histo-average min: número de minutos para construir los gráficos de
                         histogramas de consultas. Por defecto: 60 minutos.
-b | --begin datetime  : fecha/hora de inicio de los datos que se van a
                         analizar en el registro (una marca de tiempo o una hora)
-c | --dbclient host   : informar solo de las entradas del host cliente
                         indicado.
-C | --nocomment       : eliminar de las consultas los comentarios como /* ... */.
-d | --dbname database : informar solo de las entradas de la base de datos
                         indicada.
-D | --dns-resolv      : las direcciones IP de los clientes se sustituyen por
                         su nombre DNS. Ten en cuenta que esto puede
                         ralentizar mucho pgBadger.
-e | --end datetime    : fecha/hora de fin de los datos que se van a analizar
                         en el registro (una marca de tiempo o una hora)
-E | --explode         : dividir el informe principal generando un informe
                         por base de datos. La información global no
                         relacionada con una base de datos se añade al
                         informe de la base postgres.
-f | --format logtype  : valores posibles: syslog, syslog2, stderr, jsonlog,
                         csv, pgbouncer, logplex, rds y redshift. Usar esta
                         opción cuando pgBadger no sea capaz de detectar el
                         formato del registro.
-G | --nograph         : deshabilitar los gráficos en la salida HTML. Están
                         activados por defecto.
-h | --help            : mostrar este mensaje y salir.
-H | --html-outdir path: directorio donde debe escribirse el informe HTML en
                         modo incremental; los archivos binarios permanecen
                         en el directorio definido con la opción -O, --outdir.
-i | --ident name      : nombre de programa usado como ident de syslog. Por
                         defecto: postgres
-I | --incremental     : usar el modo incremental; los informes se generarán
                         por días en un directorio separado. Debe definirse
                         --outdir.
-j | --jobs number     : número de tareas que se ejecutan a la vez para un
                         solo archivo de registro. Se ejecuta una sola por
                         defecto o al trabajar con el formato csvlog.
-J | --Jobs number     : número de archivos de registro que se analizan en
                         paralelo. Por defecto se procesa un archivo a la vez.
-l | --last-parsed file: permite el análisis incremental del registro
                         guardando la última fecha/hora y la última línea
                         analizadas. Útil si se quieren vigilar los errores
                         desde la última ejecución o si se desea un informe
                         por día con un registro que rota cada semana.
-L | --logfile-list file:archivo que contiene una lista de archivos de
                         registro que se van a analizar.
-m | --maxlength size  : longitud máxima de una consulta; se restringirá al
                         tamaño indicado. El tamaño de truncamiento por
                         defecto es 100000.
-M | --no-multiline    : no recopilar sentencias multilínea para evitar
                         contenido basura, especialmente en errores que
                         generan un informe enorme.
-N | --appname name    : informar solo de las entradas del nombre de
                         aplicación indicado
-o | --outfile filename: define el nombre del archivo de salida. Por defecto
                         depende del formato de salida: out.html, out.txt,
                         out.bin o out.json. Esta opción puede usarse varias
                         veces para producir varios formatos. Para usar la
                         salida json debe estar instalado el módulo Perl
                         JSON::XS; para volcar la salida a stdout, usar -
                         como nombre de archivo.
-O | --outdir path     : directorio donde deben guardarse los archivos de
                         salida.
-p | --prefix string   : el valor de tu log_line_prefix personalizado tal
                         como está definido en tu postgresql.conf. Solo debe
                         usarse si no se emplea uno de los prefijos estándar
                         especificados en la documentación de pgBadger, por
                         ejemplo si el prefijo incluye variables adicionales
                         como la IP del cliente o el nombre de la aplicación.
                         DEBE contener secuencias de escape de tiempo (%t,
                         %m o %n) y de procesos (%p o %c). Ver los ejemplos
                         a continuación.
-P | --no-prettify     : deshabilitar el formateador de embellecido de las
                         consultas SQL.
-q | --quiet           : no imprimir nada en stdout, ni siquiera una barra
                         de progreso.
-Q | --query-numbering : añadir la numeración de las consultas a la salida
                         al usar las opciones --dump-all-queries o
                         --normalized-only.
-r | --remote-host ip  : define el host donde ejecutar el comando cat sobre
                         el archivo de registro remoto para analizarlo
                         localmente.
-R | --retention N     : número de semanas que se conservan en modo
                         incremental. Por defecto: 0, deshabilitado. Se usa
                         para fijar el número de semanas que se conservan en
                         el directorio de salida. Los directorios de semanas
                         y días más antiguos se eliminan automáticamente.
-s | --sample number   : número de muestras de consultas que se almacenan.
                         Por defecto: 3.
-S | --select-only     : informar solo de las consultas SELECT.
-t | --top number      : número de consultas que se almacenan/muestran. Por
                         defecto: 20.
-T | --title string    : cambia el título de la página HTML del informe.
-u | --dbuser username : informar solo de las entradas del usuario indicado.
-U | --exclude-user username : excluye del informe las entradas del usuario
                         especificado. Puede usarse varias veces.
-v | --verbose         : activar el modo detallado o de depuración.
                         Deshabilitado por defecto.
-V | --version         : mostrar la versión de pgBadger y salir.
-w | --watch-mode      : informar solo de los errores, tal como podría
                         hacerlo logwatch.
-W | --wide-char       : codificar en UTF8 la salida HTML de las consultas
                         para evitar el mensaje de Perl
                         "Wide character in print".
-x | --extension       : formato de salida. Valores: text, html, bin o json.
                         Por defecto: html
-X | --extra-files     : en modo incremental, permite que pgBadger escriba
                         los archivos CSS y JS en el directorio de salida
                         como archivos separados.
-z | --zcat exec_path  : define la ruta completa del programa zcat. Usar
                         esta opción si zcat, bzcat o unzip no está en el
                         path.
-Z | --timezone +/-XX  : define el número de horas respecto a GMT de la zona
                         horaria. Usar esto para ajustar la fecha/hora en
                         los gráficos de JavaScript. El valor puede ser un
                         entero, p. ej. 2, o un decimal, p. ej. 2.5.
--anonymize            : ocultar todos los literales de las consultas, útil
                         para esconder datos confidenciales.
--charset              : se usa para fijar el juego de caracteres HTML que
                         se va a usar. Por defecto: utf-8.
--command CMD          : comando que se ejecuta para obtener entradas de
                         registro por stdin. pgBadger abrirá una tubería
                         hacia el comando y analizará las entradas generadas
                         por el comando.
--csv-separator        : se usa para fijar el separador de campos CSV, por
                         defecto: ,
--day-report YYYY-MM-DD: crea un informe HTML del día especificado. Requiere
                         los directorios de salida incremental y la
                         presencia de todos los archivos de datos binarios
                         necesarios
--disable-autovacuum   : no generar el informe de autovacuum.
--disable-checkpoint   : no generar el informe de checkpoint/restartpoint.
--disable-connection   : no generar el informe de conexiones.
--disable-error        : no generar el informe de errores.
--disable-hourly       : no generar el informe por horas.
--disable-lock         : no generar el informe de bloqueos.
--disable-query        : no generar los informes de consultas (las más
                         lentas, las más frecuentes, consultas por usuario,
                         por base de datos, ...).
--disable-session      : no generar el informe de sesiones.
--disable-temporary    : no generar el informe de temporales.
--disable-type         : no generar el informe de consultas por tipo, base
                         de datos o usuario.
--dump-all-queries     : volcar todas las consultas encontradas en el
                         archivo de registro, sustituyendo los parámetros de
                         enlace incluidos en las consultas en sus posiciones
                         de marcador respectivas.
--dump-raw-csv         : analizar el registro y volcar la información en
                         formato CSV. No se hace ningún procesamiento
                         posterior, sin informe.
--enable-checksum      : se usa para añadir una suma md5 bajo cada informe de
                         consulta.
--exclude-appname name : excluye del informe las entradas del nombre de
                         aplicación especificado.  Ejemplo: "pg_dump".
                         Puede usarse varias veces.
--exclude-client name  : excluye las entradas de registro de la IP de
                         cliente especificada. Puede usarse varias veces.
--exclude-db name      : excluye del informe las entradas de la base de
                         datos especificada. Ejemplo: "postgres". Puede
                         usarse varias veces.
--exclude-file filename: ruta del archivo que contiene cada regex que se
                         usará para excluir consultas del informe. Una regex
                         por línea.
--exclude-line regex   : excluye cualquier entrada de registro que coincida
                         con la regex indicada. Puede usarse varias veces.
--exclude-query regex  : cualquier consulta que coincida con la regex
                         indicada se excluirá del informe. Por ejemplo:
                         "^(VACUUM|COMMIT)". Puede usarse esta opción varias
                         veces.
--exclude-time  regex  : cualquier marca de tiempo que coincida con la regex
                         indicada se excluirá del informe. Por ejemplo:
                         "2013-04-12 .*". Puede usarse esta opción varias
                         veces.
--explain-url URL      : se usa para sobrescribir la URL de la herramienta
                         explain gráfica. Por defecto:
                         https://explain.depesz.com/
--histogram-query VAL  : usar límites personalizados para el histograma de
                        tiempos de consulta. Límites por defecto en
                        milisegundos:
                     0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: usar límites personalizados para el histograma de
                        tiempos de sesión. Límites por defecto en
                        milisegundos:
                     0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: ruta del archivo que contiene cada regex de las
                         consultas que se van a incluir del informe. Una
                         regex por línea.
--include-query regex  : cualquier consulta que no coincida con la regex
                         indicada se excluirá del informe. Puede usarse esta
                         opción varias veces. Por ejemplo: "(tbl1|tbl2)".
--include-pid PID      : informar solo de los eventos relacionados con el
                         pid de sesión (%p). Puede usarse varias veces.
--include-session ID   : informar solo de los eventos relacionados con el
                         id de sesión (%c). Puede usarse varias veces.
--include-time  regex  : solo las marcas de tiempo que coincidan con la
                         regex indicada se incluirán en el informe. Por
                         ejemplo: "2013-04-12 .*". Puede usarse esta opción
                         varias veces.
--iso-week-number      : en modo incremental, las semanas del calendario
                         empiezan en lunes y respetan el número de semana
                         ISO 8601, del 01 al 53, donde la semana 1 es la
                         primera semana que tiene al menos 4 días en el año
                         nuevo.
--keep-comments        : no eliminar los comentarios de las consultas
                         normalizadas. Puede ser útil si se quiere
                         distinguir entre consultas normalizadas iguales.
--journalctl command   : comando que se usará para sustituir el archivo de
                         registro de PostgreSQL por una llamada a
                         journalctl. Básicamente podría ser:
                            journalctl -u postgresql-9.5
--log-duration         : fuerza a pgBadger a asociar las entradas de
                         registro generadas tanto por log_duration = on
                         como por log_statement = 'all'
--log-timezone +/-XX   : define el número de horas respecto a GMT de la
                         zona horaria que debe usarse para ajustar la
                         fecha/hora leída del archivo de registro antes de
                         analizarla. Usar esta opción dificulta la búsqueda
                         en el registro por fecha/hora. El valor puede ser
                         un entero, p. ej. 2, o un decimal, p. ej. 2.5.
--month-report YYYY-MM : crea un informe HTML acumulativo del mes
                         especificado. Requiere los directorios de salida
                         incremental y la presencia de todos los archivos
                         de datos binarios necesarios
--noexplain            : no procesar las líneas generadas por auto_explain.
--no-fork              : no crear ningún proceso, con fines de depuración.
--no-process-info      : deshabilitar el cambio de título del proceso para
                         ayudar a identificar el proceso de pgbadger;
                         algunos sistemas no lo soportan.
--no-progressbar       : deshabilitar la barra de progreso.
--noreport             : no se creará ningún informe en modo incremental.
--no-week              : indica a pgbadger que no construya informes
                         semanales en modo incremental. Útil si requiere
                         demasiado tiempo.
--normalized-only      : volcar solo todas las consultas normalizadas a
                         out.txt
--pgbouncer-only       : mostrar solo los menús relacionados con PgBouncer
                         en la cabecera.
--pid-dir path         : define la ruta donde debe almacenarse el archivo
                         pid. Por defecto /tmp
--pid-file file        : define el nombre del archivo pid para gestionar la
                         ejecución concurrente de pgBadger. Por defecto:
                         pgbadger.pid
--pie-limit num        : los datos de sectores inferiores a num% se
                         mostrarán como una suma en su lugar.
--prettify-json        : se usa para embellecer la salida json.
--rebuild              : se usa para reconstruir todos los informes html en
                         los directorios de salida incremental donde haya
                         archivos de datos binarios.
--start-monday         : en modo incremental, las semanas del calendario
                         empiezan en domingo. Usar esta opción para que
                         empiecen en lunes.
--tempdir DIR          : define el directorio donde se escribirán los
                         archivos temporales. Por defecto:
                         File::Spec->tmpdir() || '/tmp'
```

pgBadger puede analizar un archivo de registro remoto mediante una conexión ssh sin
contraseña. Usa -r o --remote-host para indicar la dirección IP o el nombre de host.
También hay algunas opciones adicionales para controlar por completo la conexión ssh.

```text
--ssh-identity file      ruta del archivo de identidad que se va a usar.
--ssh-option  options    lista de opciones -o que se usarán para la
                         conexión ssh. Opciones siempre usadas:
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          puerto ssh que se usará para la conexión. Por
                         defecto: 22.
--ssh-program ssh        ruta del programa ssh que se va a usar. Por
                         defecto: ssh.
--ssh-timeout second     tiempo de espera del fallo de conexión ssh. Por
                         defecto: 10 segundos.
--ssh-user username      nombre de usuario de la conexión. Por defecto, el
                         usuario que ejecuta pgBadger.
```

`--ssh-sudo` antepone `sudo` a los comandos remotos de listado de archivos y de lectura del registro. El usuario SSH remoto debe poder ejecutar esos comandos mediante `sudo` sin un aviso interactivo.

El archivo de registro que se va a analizar también puede especificarse mediante un URI; los protocolos
admitidos son http[s] y [s]ftp. Se usará el comando curl para descargar el archivo, y el
archivo se analizará durante la descarga. El protocolo ssh también está admitido y usará
el comando ssh igual que en el uso con un host remoto. Consulta los ejemplos a continuación.

Códigos de retorno:

```text
0: en caso de éxito
1: terminación por error
2: si se ha interrumpido con ctr+c, por ejemplo
3: el archivo pid ya existe o no puede crearse
4: no se ha dado ningún archivo de registro en la línea de comandos
```

Ejemplos:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# Prefijo de línea de registro con salida de registro stderr
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# Prefijo de línea de registro con salida de registro syslog
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# Usar mis 8 CPU para analizar mi archivo de 10GB más rápido, mucho más rápido
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

Usa la notación URI para el archivo de registro remoto:

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

Puedes usar juntos un registro local de PostgreSQL y un archivo de registro remoto de pgbouncer para analizarlos:

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

Informar de los errores cada semana mediante una tarea de cron:

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

Generar un informe cada semana usando el comportamiento incremental:

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

Esto supone que tu archivo de registro y tu informe HTML también rotan cada semana.

O mejor aún, usa los informes incrementales generados automáticamente:

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

generará un informe por día y por semana.

En el modo incremental, también puedes indicar el número de semanas que se conservan en
los informes:

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Si tienes un pg_dump a las 23:00 y a las 13:00 cada día durante media hora, puedes
usar pgBadger de la siguiente manera para excluir estos períodos del informe:

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

Esta expresión excluye cada hora completa que coincida, incluido el tiempo fuera del volcado de media hora. Estrecha el patrón de minutos si solo debe excluirse el intervalo del volcado.

Esto ayudará a evitar tener sentencias COPY, como las que genera pg_dump, en la parte superior de
la lista de consultas más lentas. También puedes usar --exclude-appname "pg_dump" para
resolver este problema de una manera más sencilla.

También puedes analizar la salida de journalctl como si fuera un archivo de registro:

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

o, lo que es peor, llamarlo desde un host remoto:

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

no necesitas especificar ningún archivo de registro en la línea de comandos, pero si tienes otros
archivos de registro de PostgreSQL que analizar, puedes añadirlos como de costumbre.

Para reconstruir después todos los informes html incrementales, procede de la siguiente manera:

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

también actualizará todos los archivos de recursos (JS y CSS). Usa -E o --explode
si los informes se generaron con esta opción.

pgBadger también admite los registros de Heroku PostgreSQL con el formato logplex:

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

esto enviará el registro de Heroku PostgreSQL a pgbadger a través de stdin.

pgBadger puede detectar automáticamente los registros de RDS y cloudwatch de PostgreSQL con
el formato rds:

```text
pgbadger -f rds -o rds_out.html rds.log
```

Cada registro de CloudSQL Postgresql es un registro de PostgreSQL bastante normal, pero encapsulado
en formato JSON. pgBadger lo detecta automáticamente, pero en caso de que necesites forzar
el formato de registro, usa `jsonlog`:

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

Es lo mismo que ocurre con la extensión jsonlog: el formato json es diferente,
pero pgBadger puede analizar ambos formatos.

pgBadger también admite los registros producidos por el operador CloudNativePG de Postgres para Kubernetes:

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

Para crear un informe acumulativo de un mes, usa el comando:

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

esto añadirá un enlace al nombre del mes en la vista de calendario de los informes
incrementales para consultar el informe del mes de mayo de 2019.
Usa -E o --explode si los informes se generaron con esta opción.
