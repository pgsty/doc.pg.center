---
title: "Documentación de pgBackRest 2.60.0"
linkTitle: pgBackRest
weight: 20
icon: fa-solid fa-couch
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
description: "Copias de seguridad y restauración fiables para PostgreSQL — documentación y referencia de pgBackRest."
module: [PGBACKREST]
categories: [Concepto]
upstream_source: pgbackrest
upstream_ref: v2.60.0
upstream_link: "https://pgbackrest.org/"
cascade:
  upstream_source: pgbackrest
  upstream_ref: v2.60.0
  type: docs
  module: [PGBACKREST]
---

--------

## Introducción {#introduction}

pgBackRest es una solución fiable de copia de seguridad y restauración para PostgreSQL que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

Este espejo de la documentación cubre pgBackRest [v2.60.0](https://github.com/pgbackrest/pgbackrest/releases/tag/release/2.60.0). Las notas de la versión están en la página de [versiones](/es/pgbackrest/release/).

La versión 2.60.0 añade un tratamiento configurable de los errores de sumas de control de páginas, la lectura anticipada de almacenes de objetos y GCS Workload Identity Federation. Ahora `restore` y `expire` se detienen de forma predeterminada ante sumas de control de páginas no válidas; consulta las [notas de la versión 2.60.0](/es/pgbackrest/release/#v2600-release-notes).

La versión 2.59.3 corrigió posibles subclaves de cifrado débiles y sales. La actualización no reemplaza las subclaves de stanza débiles existentes; consulta [Subclaves y sales de cifrado débiles](/es/pgbackrest/news/#weak-encryption) para las comprobaciones y la remediación.

¡Danos una estrella en [GitHub](https://github.com/pgbackrest/pgbackrest) si te gusta pgBackRest!


--------

## Novedades {#news}

**18 de octubre de 2026** - [Publicación de pgBackRest 2.60.0](/es/pgbackrest/news/#release-2-60-0)

**4 de octubre de 2026** - [Subclaves y sales de cifrado débiles](/es/pgbackrest/news/#weak-encryption)

**4 de octubre de 2026** - [Publicación de pgBackRest 2.59.3](/es/pgbackrest/news/#release-2-59-3)

**27 de septiembre de 2026** - [Publicación de pgBackRest 2.59.2](/es/pgbackrest/news/#release-2-59-2)


--------

## Patrocinadores {#sponsors}

pgBackRest no existiría sin patrocinio. Escribir funcionalidades nuevas, corregir bugs, revisar contribuciones, responder a las preguntas de la comunidad y el mantenimiento llevan todos una cantidad considerable de tiempo. Considera un [patrocinio](https://github.com/sponsors/dwsteele) si usas pgBackRest en tu empresa.

Nuestros patrocinadores: [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).

Estamos agradecidos con nuestros patrocinadores por invertir en infraestructura de código abierto que beneficia a toda la comunidad de PostgreSQL.

Patrocinadores anteriores: [Crunchy Data](https://crunchydata.com), [Resonate](https://resonate.com).


--------

## Funcionalidades {#features}


### Copia de seguridad y restauración en paralelo {#parallel-backup--restore}

La compresión suele ser el cuello de botella durante las operaciones de copia de seguridad, así que pgBackRest resuelve este problema con procesamiento en paralelo y algoritmos de compresión más eficientes como `lz4` y `zstd`.


### Operación local o remota {#local-or-remote-operation}

Un protocolo personalizado permite a pgBackRest hacer copias de seguridad, restaurar y archivar de forma local o remota mediante TLS/SSH con una configuración mínima. También se proporciona una interfaz para consultar PostgreSQL a través de la capa del protocolo, de modo que nunca se requiere acceso remoto a PostgreSQL, lo que mejora la seguridad.


### Múltiples repositorios {#multiple-repositories}

Los múltiples repositorios permiten, por ejemplo, un repositorio local con una retención mínima para restauraciones rápidas y un repositorio remoto con una retención más larga para redundancia y acceso en toda la empresa.


### Copia de seguridad desde un servidor en espera {#backup-from-standby}

Las copias de seguridad pueden realizarse desde un servidor en espera para reducir la carga del primario. Solo se copian del primario los pocos archivos que no se replican.


### Copias de seguridad completas, diferenciales e incrementales (a nivel de archivo o de bloque) {#full-differential--incremental-backups-at-file-or-block-level}

Se admiten copias de seguridad completas, diferenciales e incrementales. pgBackRest no es susceptible a los problemas de resolución de tiempo de `rsync`, lo que hace que las copias de seguridad diferenciales e incrementales sean seguras sin necesidad de calcular la suma de control de cada archivo. Las copias de seguridad a nivel de bloque ahorran espacio al copiar solo las partes de los archivos que han cambiado.


### Rotación de copias de seguridad y expiración del archivado {#backup-rotation--archive-expiration}

Se pueden establecer políticas de retención para las copias de seguridad completas y diferenciales para crear cobertura para cualquier periodo de tiempo. El archivado de WAL puede mantenerse para todas las copias de seguridad o estrictamente para las más recientes. En este último caso, el WAL necesario para hacer consistentes las copias de seguridad más antiguas se mantendrá en el archivado.


### Integridad de las copias de seguridad {#backup-integrity}

Se calculan sumas de control para cada archivo de la copia de seguridad y se vuelven a comprobar durante una restauración o una verificación. Después de que una copia de seguridad termina de copiar archivos, espera hasta que cada segmento WAL necesario para hacer consistente la copia de seguridad llegue al repositorio.

Las copias de seguridad del repositorio pueden almacenarse en el mismo formato que un clúster estándar de PostgreSQL (incluidos los tablespaces). Si la compresión está deshabilitada y los enlaces duros están habilitados, es posible tomar una instantánea de una copia de seguridad del repositorio y levantar directamente sobre la instantánea un clúster de PostgreSQL. Esto es ventajoso para bases de datos de escala de terabytes cuya restauración por la vía tradicional consume mucho tiempo.

Todas las operaciones utilizan fsync a nivel de archivo y de directorio para garantizar la durabilidad.


### Sumas de control de páginas {#page-checksums}

Si las sumas de control de páginas están habilitadas, pgBackRest validará las sumas de control de cada archivo que se copie durante una copia de seguridad. Todas las sumas de control de páginas se validan durante una copia de seguridad completa y las sumas de control de los archivos que han cambiado se validan durante las copias de seguridad diferenciales e incrementales.

De forma predeterminada, los fallos de validación no detienen la copia de seguridad, sino que se emiten advertencias a la consola y al archivo de registro con detalles de las páginas que han fallado. De forma predeterminada, restore notifica un error si la copia contiene sumas de control de páginas no válidas, y expire no permite que una copia con esos errores quede como la copia más antigua conservada.

Esta funcionalidad permite detectar temprano la corrupción a nivel de página, antes de que expiren las copias de seguridad que contienen copias válidas de los datos.


### Reanudación de copias de seguridad {#backup-resume}

Una copia de seguridad interrumpida puede reanudarse desde el punto donde se detuvo. Los archivos que ya se habían copiado se comparan con las sumas de control del manifiesto para garantizar la integridad. Dado que esta operación puede realizarse por completo en el host del repositorio, reduce la carga en el host de PostgreSQL y ahorra tiempo, ya que el cálculo de sumas de control es más rápido que comprimir y retransmitir datos.


### Compresión y sumas de control en streaming {#streaming-compression--checksums}

Los cálculos de compresión y de sumas de control se realizan en streaming mientras los archivos se copian al repositorio, ya sea que el repositorio esté ubicado local o remotamente.

Si el repositorio está en un host de repositorio, la compresión se realiza en el host de PostgreSQL y los archivos se transmiten en formato comprimido y simplemente se almacenan en el host del repositorio. Cuando la compresión está deshabilitada se utiliza un nivel inferior de compresión para hacer un uso eficiente del ancho de banda disponible manteniendo el coste de CPU al mínimo.


### Agrupación de archivos {#file-bundling}

Los archivos pequeños se agrupan en paquetes en el repositorio para crear menos archivos durante la copia de seguridad. Esto resulta especialmente eficaz en los almacenes de objetos.


### Restauración delta {#delta-restore}

El manifiesto contiene sumas de control para cada archivo de la copia de seguridad, de modo que durante una restauración es posible usar estas sumas de control para acelerar enormemente el procesamiento. En una restauración delta, los archivos que no estén presentes en la copia de seguridad se eliminan primero y luego se generan las sumas de control de los archivos restantes. Los archivos que coinciden con la copia de seguridad se dejan en su lugar y el resto de los archivos se restaura como de costumbre. El procesamiento en paralelo puede reducir drásticamente los tiempos de restauración.


### Envío y obtención de WAL en paralelo y asíncronos {#parallel-asynchronous-wal-push--get}

Se incluyen comandos dedicados para enviar (push) WAL al archivado y obtener (get) WAL del archivado. Ambos comandos admiten paralelismo para acelerar el procesamiento y se ejecutan de forma asíncrona para proporcionar el menor tiempo de respuesta posible a PostgreSQL.

El envío de WAL detecta automáticamente los segmentos WAL que se envían varias veces y los desduplica cuando el segmento es idéntico; de lo contrario, se genera un error. El envío asíncrono de WAL permite delegar la transferencia a otro proceso que comprime los segmentos WAL en paralelo para obtener el máximo rendimiento. Esto puede ser una funcionalidad crítica para bases de datos con un volumen de escritura extremadamente alto.

La obtención asíncrona de WAL mantiene una cola local de segmentos WAL descomprimidos y listos para reproducirse. Esto reduce el tiempo necesario para proporcionar WAL a PostgreSQL, lo que maximiza la velocidad de reproducción. Las conexiones y almacenamientos de mayor latencia (como S3) son los más beneficiados.

Los comandos de envío y obtención garantizan ambos que la base de datos y el repositorio coincidan comparando las versiones de PostgreSQL y los identificadores del sistema. Esto elimina prácticamente la posibilidad de configurar incorrectamente la ubicación del archivado de WAL.


### Soporte de tablespaces y enlaces {#tablespace--link-support}

Los tablespaces son totalmente compatibles y, al restaurar, los tablespaces pueden remapearse a cualquier ubicación. También es posible remapear todos los tablespaces a una sola ubicación con un único comando, lo cual es útil para restauraciones de desarrollo.

Los enlaces de archivos y directorios son compatibles para cualquier archivo o directorio del clúster de PostgreSQL. Al restaurar, es posible restaurar todos los enlaces a sus ubicaciones originales, remapear algunos o todos los enlaces, o restaurar algunos o todos los enlaces como archivos o directorios normales dentro del directorio del clúster.


### Soporte de S3, Azure, GCS y SFTP {#s3-azure-and-gcs-compatible-object-store-support}

Los repositorios de pgBackRest pueden ubicarse en almacenes de objetos compatibles con S3, Azure y GCS para permitir una capacidad y retención prácticamente ilimitadas. Los repositorios también pueden almacenarse en un servidor SFTP. En entornos de nube, las credenciales del almacén de objetos pueden obtenerse automáticamente mediante diversos métodos de autenticación.


### Cifrado {#encryption}

pgBackRest puede cifrar el repositorio para proteger las copias de seguridad estén donde estén almacenadas.


### Protección contra ransomware y malware {#ransomware--malware-protection}

Cuando el repositorio se almacena en almacenamiento de objetos con versionado, pgBackRest puede leer el repositorio tal como estaba en un punto en el tiempo. Si las copias de seguridad son eliminadas o corrompidas por accidente, malware o ransomware, puede usarse un tiempo objetivo para recuperar los datos desde antes de que ocurriera el daño.

El versionado es compatible con los almacenes de objetos compatibles con S3, Azure y GCS. El bloqueo de objetos para S3 y el borrado suave para GCS o Azure pueden proporcionar protección adicional contra manipulaciones.


### Compatibilidad con diez versiones de PostgreSQL {#compatibility-with-ten-versions-of-postgresql}

pgBackRest incluye soporte para diez versiones de PostgreSQL: las cinco versiones con soporte y las últimas cinco versiones EOL. Esto deja tiempo de sobra para actualizar a una versión con soporte.


--------

## Primeros pasos {#getting-started}

pgBackRest se esfuerza por ser fácil de configurar y operar:

- [Guías de usuario](/es/pgbackrest/user-guide/) para varios sistemas operativos y versiones de PostgreSQL.
- Páginas de comandos para las operaciones de línea de comandos: [backup](/es/pgbackrest/command/backup/), [restore](/es/pgbackrest/command/restore/), [check](/es/pgbackrest/command/check/) e [info](/es/pgbackrest/command/info/).
- [Referencia de configuración](/es/pgbackrest/configuration/) para crear configuraciones de pgBackRest.


--------

## Contribuciones {#contributions}

¡Las contribuciones a pgBackRest siempre son bienvenidas! Consulta nuestras [pautas de contribución](https://github.com/pgbackrest/pgbackrest/blob/main/CONTRIBUTING.md) para más detalles sobre cómo contribuir con funcionalidades, mejoras o incidencias.


--------

## Soporte {#support}

pgBackRest es completamente gratuito y de código abierto bajo la licencia [MIT](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE). Puedes usarlo con fines personales o comerciales sin restricción alguna. Los informes de bugs se toman muy en serio y se atenderán tan pronto como sea posible. Reporta los bugs [aquí](https://github.com/pgbackrest/pgbackrest/issues).

Crear una política robusta de recuperación ante desastres con estrategias adecuadas de replicación y copia de seguridad puede ser una tarea muy compleja y desalentadora. Puede que descubras que necesitas ayuda durante la fase de arquitectura y soporte continuo para garantizar que tu empresa siga funcionando sin problemas.

Nuestros [patrocinadores](#sponsors) ofrecen productos y servicios que incluyen soporte de pgBackRest y pueden ayudarte con tus necesidades de recuperación ante desastres.
