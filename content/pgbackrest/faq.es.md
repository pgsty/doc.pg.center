---
title: "Preguntas frecuentes"
linkTitle: "FAQ"
weight: 70
description: "Preguntas frecuentes sobre copias de seguridad, restauración, configuración y solución de problemas con pgBackRest."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/faq.html"
---

--------

## Introducción {#introduction}

Las preguntas frecuentes tienen como objetivo proporcionar detalles sobre preguntas específicas que pueden o no estar cubiertas en la guía de usuario, la configuración o la referencia de comandos. Si no encuentras aquí detalles para tu problema específico, recuerda que la [lista de problemas en GitHub](https://github.com/pgbackrest/pgbackrest/issues) también es un recurso valioso.


--------

## ¿Qué hago si obtengo el error «could not find WAL segment»? {#what-if-i-get-the-could-not-find-wal-segment-error}

La causa de este error puede deberse a muchos problemas diferentes, algunos de los cuales pueden ser:

- un `archive_command` mal configurado
- archivos de configuración de pgBackRest mal configurados
- un problema de red o de permisos
- un problema de configuración de un producto de terceros (p. ej., S3, Swift o Minio)
- una gran cantidad de WAL en cola pendiente de archivarse

Es aconsejable:

- comprobar el `archive_command` en PostgreSQL
- comprobar los ajustes de configuración de pgBackRest en cada host (p. ej., los ajustes `pg*` se establecen en el host del repositorio y los ajustes `repo*` en el host de pg)
- ejecutar el comando `check` con `--archive-timeout` establecido a un valor más alto que el del archivo de configuración de pgBackRest (o el predeterminado) para ver si la cola de WAL necesita más tiempo para vaciarse. Si el sistema genera mucho WAL, considera configurar el [archivado asíncrono](/es/pgbackrest/user-guide/#asynchronous-archiving)


--------

## ¿Cómo purgo manualmente un conjunto de copia de seguridad? {#how-do-i-manually-purge-a-backup-set}

Un conjunto de copia de seguridad completa puede expirarse usando la opción `--set`, como se explica en [Referencia de comandos: Expire](/es/pgbackrest/command/expire/).


--------

## ¿Cómo puedo configurar las opciones de forma independiente para cada comando? {#how-can-i-configure-options-independently-for-each-command}

pgBackRest tiene la capacidad de establecer opciones de forma independiente en el archivo de configuración para cada comando. [Configurar la stanza del clúster](/es/pgbackrest/user-guide/#configure-cluster-stanza) describe esta función, así como la precedencia de las opciones.

Por ejemplo, la opción `process-max` puede optimizarse para cada comando:

```ini
[global]
# used where not overridden
process-max=2

[global:backup]
# more cores for backup
process-max=4

[global:restore]
# all the cores for restore
process-max=8

[global:archive-push]
# more cores for archive-push
process-max=3

[global:archive-get]
# fewer cores for archive-get
process-max=1
```


--------

## ¿Puedo usar puntos (.) en el nombre de mi bucket de S3? {#can-i-use-dots-periods-in-my-s3-bucket-name}

RFC-2818 no permite que los comodines coincidan con un punto (.), por lo que los nombres de bucket de S3 no deben contener puntos. Si hay puntos en el nombre del bucket de S3, ocurrirá un error como «unable to find hostname 'my.backup.bucket.s3.amazonaws.com' in certificate common name or subject alternative names».

La excepción es `repo-s3-uri-style=path`, que antepone el bucket al URI en lugar del host. Como el bucket no forma parte del nombre del host, el certificado se coteja únicamente con el endpoint y los puntos en el nombre del bucket no son un problema. Ten en cuenta que los URI de estilo path no son compatibles con todos los almacenes de objetos compatibles con S3.


--------

## ¿Dónde puedo encontrar paquetes de versiones antiguas de pgBackRest? {#where-can-i-find-packages-for-older-versions-of-pgbackrest}

El repositorio [apt.postgresql.org](https://apt.postgresql.org) mantiene un [archivo de versiones antiguas](https://apt-archive.postgresql.org). Debian también mantiene [instantáneas](https://snapshot.debian.org/binary/pgbackrest/) de todas las compilaciones de prueba.


--------

## ¿Por qué falla un intento de copia de seguridad cuando `backup-standby=y` y la base de datos standby está caída? {#why-does-a-backup-attempt-fail-when-backup-standbyy-and-the-standby-database-is-down}

Configurar la copia de seguridad desde el standby generalmente tiene como objetivo reducir la carga en el primario, por lo que pasar las copias de seguridad al primario cuando el standby está caído a menudo va contra el propósito. No se recomienda poner más carga en el primario en una situación en la que ya hay fallos en el sistema. Las copias de seguridad no son críticas siempre que tengas una bastante reciente — lo importante es mantenerse al día con el archivado de WAL. Hay tiempo de sobra para hacer una copia de seguridad cuando el sistema vuelva a estar estable.

Si realmente necesitas una copia de seguridad, la solución es tener más standbys o eliminar `backup-standby`. Esto puede anularse en la línea de comandos con `--no-backup-standby`, por lo que no hay necesidad de reconfigurar para una copia de seguridad puntual.


--------

## ¿Debo configurar mi repositorio en un host standby? {#should-i-setup-my-repository-on-a-standby-host}

No. Cuando las bases de datos primaria y standby están configuradas, los archivos de configuración de pgBackRest deben ser simétricos para manejar las conmutaciones por error sin problemas. Si no lo son, será necesario cambiar las configuraciones en una conmutación por error o podrían surgir más problemas.

Consulta la sección [Host de repositorio dedicado](/es/pgbackrest/user-guide/#dedicated-repository-host) de la guía de usuario para obtener más información.


--------

## La recuperación a un punto en el tiempo basada en el tiempo no parece funcionar, ¿por qué? {#time-based-point-in-time-recovery-does-not-appear-to-work-why}

El error más común al usar la recuperación a un punto en el tiempo basada en el tiempo es elegir una copia de seguridad que se completó después de la hora objetivo. Con `--type=time`, si no se especifica la opción `--set`, pgBackRest busca en los repositorios configurados una copia de seguridad que se hubiera completado antes de la hora especificada por `--target=`. Si no se encuentra una copia de seguridad adecuada, pgBackRest lanza un error en lugar de restaurar la copia de seguridad más reciente. Una copia de seguridad completada después de la hora objetivo no puede usarse para alcanzar ese objetivo anterior reproduciendo el WAL.

Para usar la opción `--set`, elige un conjunto de copia de seguridad ejecutando el comando `info` y localizando la copia de seguridad con una marca de tiempo de detención anterior a la hora objetivo. Luego, al ejecutar la restauración, especifica la opción `--set=BACKUP_LABEL` donde `BACKUP_LABEL` es el conjunto de copia de seguridad elegido.

Consulta la sección [Recuperación a un punto en el tiempo](/es/pgbackrest/user-guide/#point-in-time-recovery) de la guía de usuario para obtener más información.


--------

## ¿Qué significa el sufijo del archivado de WAL? {#what-does-the-wal-archive-suffix-mean}

El sufijo es la suma de comprobación SHA1 que se usa para verificar la integridad del archivo. No hay forma de omitirlo.


--------

## ¿Tarda más la restauración de tipos de copia de seguridad específicos (completa, diferencial, incremental)? {#does-it-take-longer-to-restore-specific-backup-types-full-differential-incremental}

Los distintos tipos de copia de seguridad requieren el mismo tiempo de restauración. La restauración recupera los archivos basándose en el manifiesto de la copia de seguridad, que puede hacer referencia a archivos de una copia de seguridad anterior en el caso de las copias incrementales o diferenciales. Aunque podría haber diferencias en el tiempo empleado en *hacer* una copia de seguridad determinada (dependiendo del tipo de copia de seguridad), el tamaño de la base de datos determina el tiempo de restauración (siendo iguales la E/S de disco, la E/S de red, etc.).


--------

## ¿Cómo puedo exportar una copia de seguridad para usarla en un entorno aislado de la red? {#how-can-i-export-a-backup-for-use-in-a-network-isolated-environment}

pgBackRest usa el repositorio no solo para almacenar copias de seguridad y el archivado de WAL, sino también para mantener los metadatos esenciales requeridos por funciones como la compresión, el cifrado y la agrupación de archivos. Debido a esto, simplemente copiar una copia de seguridad junto con un subconjunto de archivos WAL generalmente no funcionará, a menos que se cumplan condiciones muy específicas y restrictivas.

Sin embargo, existe una solución alternativa si tu objetivo es crear una exportación autónoma de una base de datos que puedas transferir (p. ej., por USB). Puedes hacer una copia de seguridad con la opción [`--archive-copy`](/es/pgbackrest/command/backup/#copy-archive-option---archive-copy) activada para asegurarte de que los segmentos WAL necesarios se almacenen junto con la copia de seguridad. Luego, restaura usando [`--type=none`](/es/pgbackrest/command/restore/#type-option---type) `--pg1-path=/your/target/path`. Esto produce un directorio de datos de PostgreSQL restaurado con todos los archivos WAL requeridos ya colocados en `pg_wal`, similar a lo que crearía `pg_basebackup`.

Luego puedes copiar este directorio a otro sistema y PostgreSQL debería poder recuperarse a partir de él sin necesidad de acceder al repositorio de pgBackRest.

Ten en cuenta que la recuperación de esta copia de seguridad no producirá un cambio de timeline, lo que significa que este clúster no debe enviar WAL al repositorio original del cual fue exportado. Si el nuevo clúster está en un entorno aislado de la red, esto no debería ser un problema.
