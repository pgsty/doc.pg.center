---
title: "Noticias"
linkTitle: "Noticias"
weight: 10
description: "Noticias oficiales del proyecto pgBackRest, anuncios de versiones y actualizaciones de mantenimiento."
icon: fa-solid fa-newspaper
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/news.html"
---

--------

## Publicación de pgBackRest 2.60.0 {#release-2-60-0}

**18 de octubre de 2026**

La comunidad de pgBackRest se complace en anunciar la publicación de [pgBackRest](https://pgbackrest.org) 2.60.0, la versión más reciente de la solución de copia de seguridad y restauración, fiable y fácil de usar, que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

pgBackRest admite un sólido conjunto de funcionalidades para gestionar tu infraestructura de copias de seguridad y recuperación, entre ellas: copia de seguridad/restauración en paralelo, copias de seguridad completas/diferenciales/incrementales, copia de seguridad incremental a nivel de bloque, múltiples repositorios, restauración delta, archivado asíncrono en paralelo, protección contra malware/ransomware, sumas de control por archivo, sumas de control de páginas (cuando están habilitadas) validadas durante la copia de seguridad, múltiples tipos de compresión, cifrado, reanudación de copias de seguridad parciales/fallidas, copia de seguridad desde un servidor en espera, soporte de tablespaces y enlaces, soporte de S3/Azure/GCS/SFTP, expiración de copias de seguridad, operación local/remota mediante SSH o TLS, configuración flexible y mucho más.

pgBackRest se puede instalar desde el [repositorio Yum de PostgreSQL](https://yum.postgresql.org) o el [repositorio APT de PostgreSQL](https://apt.postgresql.org), y también hay paquetes disponibles para muchas otras distribuciones. El código fuente se puede descargar desde [versiones](/es/pgbackrest/release/).

### Principales novedades y mejoras {#release-2-60-0-feature}

- Añadida la opción checksum-page-error para notificar un error ante sumas de control de páginas no válidas (Andrew Pogrebnoi)
- Soporte de GCS Workload Identity Federation (Adol Rodriguez)
- Lectura anticipada de múltiples archivos o rangos de almacenes de objetos (David Steele)
- Reducción de las solicitudes de mantenimiento de conexión a procesos remotos (David Steele)
- Reintento de subsolicitudes de lotes de Azure ausentes en la respuesta (David Steele)
- Reducción de las comprobaciones de manifiestos al reconstruir backup.info (David Steele)
- Soporte de compilación en illumos (Kalevi Kolttonen)
- Soporte de OpenSSL 4 (David Steele)
- Modernización del sitio web (David Steele, Jan Wieremjewicz)

Consulta las [notas de la versión 2.60.0](/es/pgbackrest/release/#v2600-release-notes) para ver otras funcionalidades y mejoras.

### Notas importantes {#release-2-60-0-note}

- Ahora la orden restore notifica un error y se detiene si algún archivo restaurado contiene una suma de control de página no válida. Esto deja el clúster incompleto e incapaz de iniciarse, por lo que hay que repetir la restauración. La orden expire ahora rechaza la expiración si la copia más antigua que se conservaría contiene errores de sumas de control, lo que también impide la expiración del archivado de ese repositorio. Establece checksum-page-error=n para emitir advertencias en lugar de errores.
- La compilación desde una copia de trabajo de Git requiere PyYAML en lugar de libyaml. El archivo tar de distribución incluye el código generado y no requiere ninguna de las dos bibliotecas.
- PostgreSQL 19rc1 está soportado por v2.59.2 y posteriores, incluida esta versión.

### Enlaces {#release-2-60-0-link}

- [Sitio web](/es/pgbackrest/)
- [Guías de usuario](/es/pgbackrest/user-guide/)
- [Notas de la versión](/es/pgbackrest/release/)

### Patrocinio {#release-2-60-0-sponsorship}

Esta versión fue posible gracias al generoso patrocinio de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).


--------

## Subclaves y sales de cifrado débiles {#weak-encryption}

**4 de octubre de 2026**

Las versiones de pgBackRest anteriores a 2.59.3 no comprobaban si se producía un error al generar datos aleatorios para el cifrado. Si OpenSSL no podía obtener datos aleatorios del sistema operativo, las subclaves de cifrado y las sales se generaban a partir de datos ya presentes en memoria y no se informaba de ningún error. Los repositorios sin cifrado no se ven afectados.

Este error debería ser poco frecuente. Entre las causas posibles se incluyen una política de sandbox o de seccomp que bloquee la llamada al sistema `getrandom()` y una configuración de OpenSSL no válida.

Las subclaves de `archive.info` y `backup.info` son la principal preocupación. Las genera `stanza-create` una sola vez y se usan durante toda la vida de la stanza, por lo que actualizar no reemplaza una subclave débil. Las subclaves y las sales débiles de las copias de seguridad se eliminan a medida que expiran las copias de seguridad y el WAL.

### Impacto {#weak-encryption-impact}

La subclave del WAL se almacena en `archive.info` y la subclave del manifiesto se almacena en `backup.info`. Una subclave débil es más fácil de adivinar que una subclave aleatoria, y una subclave adivinada descifra los archivos cifrados con ella sin `repo-cipher-pass`. Cuánto más fácil depende de lo que hubiera en memoria, lo cual varía según la plataforma y la compilación. Una subclave débil en `archive.info` expone todo el WAL del repositorio. Una subclave débil en `backup.info` expone todas las copias de seguridad, ya que los manifiestos están cifrados con ella y cada manifiesto almacena la subclave de los archivos de su copia de seguridad. Esto incluye el WAL y las copias de seguridad añadidos después de la actualización.

La subclave de los archivos de una copia de seguridad se genera para cada copia de seguridad completa y también la usan las copias de seguridad diferenciales e incrementales que se basan en ella. Una subclave de copia de seguridad débil expone los archivos de esas copias de seguridad.

Una sal débil no expone una subclave. Los archivos cifrados con la misma subclave y la misma sal usan la misma clave y el mismo IV, por lo que los datos idénticos de esos archivos producen datos cifrados idénticos. La sal se almacena sin cifrar al principio de cada archivo, y una sal débil puede contener hasta 8 bytes de datos que estuvieran previamente en memoria.

### Comprobar las subclaves {#weak-encryption-check-subkey}

Ejecuta lo siguiente en un host que tenga acceso al repositorio, con `STANZA` definido como el nombre de la stanza. Añade `--repo` a los comandos `pgbackrest` para comprobar un repositorio distinto del primero.

```bash
STANZA=demo

for file in archive/$STANZA/archive.info backup/$STANZA/backup.info; do
    for key in $(pgbackrest --stanza=$STANZA repo-get $file | grep '^cipher-pass=' | grep -oE '[A-Za-z0-9+/]{64}'); do
        echo "$(printf '%s' $key | base64 -d | od -An -v -tx1 | tr -s ' ' '\n' | grep -c '^00$') $file"
    done
done
```

La primera columna es el número de bytes cero de la subclave. Una subclave aleatoria tiene 6 o más bytes cero en menos de 1 de cada 25,000,000 casos, mientras que las subclaves débiles encontradas en las pruebas tenían 13 o más. Una subclave con 6 o más bytes cero debe considerarse débil.

### OpenSSL 1.0 {#weak-encryption-openssl-1-0}

Las versiones de pgBackRest anteriores a 2.53 podían compilarse con OpenSSL 1.0, que genera datos aleatorios a partir de un estado que no fue inicializado con datos aleatorios cuando no puede obtener datos aleatorios del sistema operativo. Las subclaves débiles generadas de esta forma no se pueden detectar con la comprobación anterior.

### Remediación {#weak-encryption-remediation}

- Actualiza a pgBackRest 2.59.3 o posterior, que informa de un error cuando no se pueden generar datos aleatorios.
- Si la subclave de `archive.info` o `backup.info` es débil, crea la stanza en un repositorio nuevo y conserva el repositorio antiguo solo mientras sean necesarias sus copias de seguridad.
- Considera hacer una nueva copia de seguridad completa después de actualizar, ya que las copias de seguridad diferenciales e incrementales usan la subclave de su copia de seguridad completa.
- Las subclaves y las sales débiles de las copias de seguridad se eliminan a medida que expiran las copias de seguridad y el WAL anteriores a la actualización. Las copias de seguridad con un periodo de retención largo las conservan hasta que expiran.


--------

## Publicación de pgBackRest 2.59.3 {#release-2-59-3}

**4 de octubre de 2026**

La comunidad de pgBackRest se complace en anunciar la publicación de [pgBackRest](https://pgbackrest.org) 2.59.3, la versión más reciente de la solución de copia de seguridad y restauración, fiable y fácil de usar, que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

pgBackRest admite un sólido conjunto de funcionalidades para gestionar tu infraestructura de copias de seguridad y recuperación, entre ellas: copia de seguridad/restauración en paralelo, copias de seguridad completas/diferenciales/incrementales, copia de seguridad incremental a nivel de bloque, múltiples repositorios, restauración delta, archivado asíncrono en paralelo, protección contra malware/ransomware, sumas de control por archivo, sumas de control de páginas (cuando están habilitadas) validadas durante la copia de seguridad, múltiples tipos de compresión, cifrado, reanudación de copias de seguridad parciales/fallidas, copia de seguridad desde un servidor en espera, soporte de tablespaces y enlaces, soporte de S3/Azure/GCS/SFTP, expiración de copias de seguridad, operación local/remota mediante SSH o TLS, configuración flexible y mucho más.

pgBackRest se puede instalar desde el [repositorio Yum de PostgreSQL](https://yum.postgresql.org) o el [repositorio APT de PostgreSQL](https://apt.postgresql.org), y también hay paquetes disponibles para muchas otras distribuciones. El código fuente se puede descargar desde [versiones](/es/pgbackrest/release/).

### Correcciones de bugs {#release-2-59-3-feature}

- Corregidas posibles subclaves de cifrado/sales débiles (j0uinim)
- Corregido un posible error de suma de control al cargar archivos de información y manifiestos cifrados (j0uinim)

Consulta las [notas de la versión 2.59.3](/es/pgbackrest/release/#v2593-release-notes) para ver correcciones y mejoras adicionales.

### Notas importantes {#release-2-59-3-note}

- En versiones anteriores era posible que se generaran subclaves de cifrado y sales débiles si se producía un error al acceder a los datos aleatorios del sistema. Consulta [Subclaves y sales de cifrado débiles](/es/pgbackrest/news/#weak-encryption) para obtener más información.

### Enlaces {#release-2-59-3-link}

- [Sitio web](/es/pgbackrest/)
- [Guías de usuario](/es/pgbackrest/user-guide/)
- [Notas de la versión](/es/pgbackrest/release/)

### Patrocinio {#release-2-59-3-sponsorship}

Esta versión fue posible gracias al generoso patrocinio de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).



--------

## Publicación de pgBackRest 2.59.2 {#release-2-59-2}

**27 de septiembre de 2026**

La comunidad de pgBackRest se complace en anunciar la publicación de [pgBackRest](https://pgbackrest.org) 2.59.2, la versión más reciente de la solución de copia de seguridad y restauración, fiable y fácil de usar, que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

pgBackRest admite un sólido conjunto de funcionalidades para gestionar tu infraestructura de copias de seguridad y recuperación, entre ellas: copia de seguridad/restauración en paralelo, copias de seguridad completas/diferenciales/incrementales, copia de seguridad incremental a nivel de bloque, múltiples repositorios, restauración delta, archivado asíncrono en paralelo, protección contra malware/ransomware, sumas de control por archivo, sumas de control de páginas (cuando están habilitadas) validadas durante la copia de seguridad, múltiples tipos de compresión, cifrado, reanudación de copias de seguridad parciales/fallidas, copia de seguridad desde un servidor en espera, soporte de tablespaces y enlaces, soporte de S3/Azure/GCS/SFTP, expiración de copias de seguridad, operación local/remota mediante SSH o TLS, configuración flexible y mucho más.

pgBackRest se puede instalar desde el [repositorio Yum de PostgreSQL](https://yum.postgresql.org) o el [repositorio APT de PostgreSQL](https://apt.postgresql.org), y también hay paquetes disponibles para muchas otras distribuciones. El código fuente se puede descargar desde [versiones](/es/pgbackrest/release/).

### Nuevas funcionalidades y correcciones de bugs {#release-2-59-2-feature}

- Compatibilidad con PostgreSQL 19beta4 (David Steele)
- Corregido un mapa de bloques vacío cuando un archivo se trunca a cero durante la copia de seguridad (David Steele)
- Deshabilitado el reintento de lectura cuando se pasan filtros al controlador (David Steele)
- Corregida la paginación del listado de versiones de S3 (David Steele)
- Establecido el encabezado de versión de Azure para la autenticación SAS (David Steele)
- Corregido que `archive-push` asíncrono se quede bloqueado con un archivo de historial de copias de seguridad de tamaño cero (Andrew Kroh)
- Corregido el comando `annotate` en un repositorio remoto cifrado (Douglas J Hunley)

Consulta las [notas de la versión 2.59.2](/es/pgbackrest/release/#v2592-release-notes) para ver correcciones y mejoras adicionales.

### Notas importantes {#release-2-59-2-note}

- PostgreSQL 19beta4 cambió los formatos de `pg_control` y de WAL, por lo que los clústeres y el WAL de una beta 19 anterior ya no se admiten. Los clústeres que ejecutan una beta anterior deben recrearse con 19beta4.

### Enlaces {#release-2-59-2-link}

- [Sitio web](/es/pgbackrest/)
- [Guías de usuario](/es/pgbackrest/user-guide/)
- [Notas de la versión](/es/pgbackrest/release/)

### Patrocinio {#release-2-59-2-sponsorship}

Esta versión fue posible gracias al generoso patrocinio de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).


--------

## Publicación de pgBackRest 2.59.1 {#release-2-59-1}

**17 de agosto de 2026**

La comunidad de pgBackRest se complace en anunciar la publicación de [pgBackRest](https://pgbackrest.org) 2.59.1, la versión más reciente de la solución de copia de seguridad y restauración, fiable y fácil de usar, que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

pgBackRest admite un sólido conjunto de funcionalidades para gestionar tu infraestructura de copias de seguridad y recuperación, entre ellas: copia de seguridad/restauración en paralelo, copias de seguridad completas/diferenciales/incrementales, copia de seguridad incremental a nivel de bloque, múltiples repositorios, restauración delta, archivado asíncrono en paralelo, protección contra malware/ransomware, sumas de control por archivo, sumas de control de páginas (cuando están habilitadas) validadas durante la copia de seguridad, múltiples tipos de compresión, cifrado, reanudación de copias de seguridad parciales/fallidas, copia de seguridad desde un servidor en espera, soporte de tablespaces y enlaces, soporte de S3/Azure/GCS/SFTP, expiración de copias de seguridad, operación local/remota mediante SSH o TLS, configuración flexible y mucho más.

pgBackRest se puede instalar desde el [repositorio Yum de PostgreSQL](https://yum.postgresql.org) o el [repositorio APT de PostgreSQL](https://apt.postgresql.org), y también hay paquetes disponibles para muchas otras distribuciones. El código fuente se puede descargar desde [versiones](/es/pgbackrest/release/).

### Nuevas funcionalidades y correcciones de bugs {#release-2-59-1-feature}

- Compatibilidad con PostgreSQL 19beta3 (Lardière Sébastien)
- Corregido un bloqueo cuando el búfer de fragmentos es más pequeño que el búfer de entrada (David Steele)
- Comparar una etiqueta de copia de seguridad nueva solo contra su propio conjunto basado en una copia de seguridad completa (David Steele)
- Corregidos los archivos fuente generados por GitHub a los que les faltaban archivos necesarios para compilar (David Steele)

Consulta las [notas de la versión 2.59.1](/es/pgbackrest/release/#v2591-release-notes) para ver correcciones y mejoras adicionales.

### Notas importantes {#release-2-59-1-note}

- PostgreSQL 19beta3 cambió el formato de WAL, por lo que el WAL archivado desde una beta anterior de PostgreSQL 19 ya no se puede leer. Los clústeres que ejecutan una beta anterior deben recrearse con 19beta3.

### Enlaces {#release-2-59-1-link}

- [Sitio web](/es/pgbackrest/)
- [Guías de usuario](/es/pgbackrest/user-guide/)
- [Notas de la versión](/es/pgbackrest/release/)

### Patrocinio {#release-2-59-1-sponsorship}

Esta versión fue posible gracias al generoso patrocinio de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).


--------

## Nuevo tarball de distribución {#distribution-tarball}

**20 de julio de 2026**

A partir de pgBackRest 2.59.0, cada versión incluye un tarball de distribución que hace más sencilla la compilación desde el código fuente. A diferencia de una copia de trabajo del repositorio git, el tarball incluye el código fuente generado y la documentación renderizada ya construidos, de modo que pgBackRest se compila e instala sin la generación de código ni las herramientas de documentación que requiere una copia de trabajo del repositorio.

El tarball contiene el código fuente de pgBackRest con el código pregenerado, la página de manual de referencia de comandos, la documentación HTML y una prueba de humo para verificar la compilación. Se compila con meson y ninja usando solo las bibliotecas habituales de pgBackRest.

El tarball se adjunta a cada versión como un recurso llamado `pgbackrest-{version}.tar.gz`, junto con una suma de control `.sha256sum` correspondiente. Descárgalo desde la página de [releases](https://github.com/pgbackrest/pgbackrest/releases) de GitHub y consulta el `README.md` del tarball para obtener las instrucciones de compilación y prueba.

Se anima a los empaquetadores a compilar a partir del tarball de distribución para evitar las herramientas de compilación adicionales que la generación de código y documentación requerirá en las versiones futuras.


--------

## Publicación de pgBackRest 2.59.0 {#release-2-59-0}

**20 de julio de 2026**

La comunidad de pgBackRest se complace en anunciar la publicación de [pgBackRest](https://pgbackrest.org) 2.59.0, la versión más reciente de la solución de copia de seguridad y restauración, fiable y fácil de usar, que escala sin problemas hasta las bases de datos y cargas de trabajo más grandes.

pgBackRest admite un sólido conjunto de funcionalidades para gestionar tu infraestructura de copias de seguridad y recuperación, entre ellas: copia de seguridad/restauración en paralelo, copias de seguridad completas/diferenciales/incrementales, copia de seguridad incremental a nivel de bloque, múltiples repositorios, restauración delta, archivado asíncrono en paralelo, protección contra malware/ransomware, sumas de control por archivo, sumas de control de páginas (cuando están habilitadas) validadas durante la copia de seguridad, múltiples tipos de compresión, cifrado, reanudación de copias de seguridad parciales/fallidas, copia de seguridad desde un servidor en espera, soporte de tablespaces y enlaces, soporte de S3/Azure/GCS/SFTP, expiración de copias de seguridad, operación local/remota mediante SSH o TLS, configuración flexible y mucho más.

pgBackRest se puede instalar desde el [repositorio Yum de PostgreSQL](https://yum.postgresql.org) o el [repositorio APT de PostgreSQL](https://apt.postgresql.org), y también hay paquetes disponibles para muchas otras distribuciones. El código fuente se puede descargar desde [versiones](/es/pgbackrest/release/).

### Funcionalidades y mejoras nuevas significativas {#feature}

- Compatibilidad con PostgreSQL 19 (David Steele)
- Añadir la opción `archive-expire-before` para limpiar el archivado de WAL (Stefan Fercot)
- Añadir soporte de S3 Outposts (Shiva Kumar Ambigi)
- Añadir la autenticación de S3 mediante un proceso (David Steele)
- Añadir caché de usuario/grupo para una construcción más rápida del manifiesto (Gunnar Lindholm)
- Reconectar el almacenamiento SFTP después de que el servidor descarte una conexión inactiva (David Steele)
- Añadir el progreso de copia de seguridad por repositorio a la salida del comando `info` (Will Morland)
- Añadir el borrado por lotes para el almacenamiento de Azure (David Steele)
- Añadir comprobaciones de `backup.info` al comando `verify` (Denis Garsh)
- Permitir la configuración del punto de conexión STS de S3 (Simon Gratton)
- Añadir la integración con systemd notify (Andrew Jackson)
- Error al ejecutar como root a menos que `allow-root` esté habilitado (David Steele)
- Salir de `archive-push` asíncrono ante el primer error (David Steele)

Consulta las [notas de la versión 2.59.0](/es/pgbackrest/release/#v2590-release-notes) para ver funcionalidades y mejoras adicionales.

### Notas importantes {#note}

- Por defecto, solo el comando `restore` puede ejecutarse como root. Usa `allow-root` para ejecutar otros comandos como root (aunque no se recomienda).
- Un nuevo tarball de distribución con la documentación, la página de manual y el código pregenerados se adjunta a cada versión para simplificar el empaquetado. Consulta [Nuevo tarball de distribución](#distribution-tarball) para obtener más información.
- Hay una nueva dependencia opcional de `libsystemd`.

### Enlaces {#link}

- [Sitio web](/es/pgbackrest/)
- [Guías de usuario](/es/pgbackrest/user-guide/)
- [Notas de la versión](/es/pgbackrest/release/)

### Patrocinio {#sponsorship}

Esta versión fue posible gracias al generoso patrocinio de [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) y [Data Egret](https://dataegret.com/).


--------

## ¡pgBackRest continuará! {#will-continue}

**18 de mayo de 2026**

¡Me complace anunciar que pgBackRest continuará! Durante las últimas semanas, una coalición de patrocinadores se ha unido para financiar el desarrollo continuo. Su apoyo significa que el proyecto ya no depende de un único patrocinador, lo que da a pgBackRest la estabilidad que necesita a largo plazo.

Quiero dar las gracias a cada uno de nuestros patrocinadores:

[Amazon Web Services](https://aws.amazon.com) proporciona recursos de computación en la nube a demanda a personas, empresas y gobiernos. Accede a potencia de cómputo, almacenamiento, bases de datos, aprendizaje automático y más de 200 servicios, pagando solo por lo que usas. Construido para crecer contigo, invirtiendo en las comunidades que compartimos.

[Supabase](https://supabase.com), una plataforma backend completa construida sobre PostgreSQL, permite a los desarrolladores crear y escalar aplicaciones rápidamente sin gestionar infraestructura. Incluye una base de datos Postgres, autenticación de usuarios, suscripciones en tiempo real, almacenamiento de archivos, funciones edge y funciones serverless, todo respaldado por una comunidad activa de código abierto.

[pgEdge](https://pgedge.com) es una plataforma Postgres de código abierto de clase empresarial para IA, alta disponibilidad y mucho más, con herramientas nativas de IA agéntica y banco de trabajo para DBA, supervisión y respuesta a incidentes, despliegue flexible y mantenimiento sin tiempo de inactividad. Escala desde un único nodo hasta una arquitectura multimáster activo-activo en la nube, en entornos locales o aislados.

[Tiger Data](https://tigerdata.com), los creadores de TimescaleDB, desarrolla la base de datos de código abierto de series temporales construida sobre PostgreSQL y opera Tiger Cloud, una plataforma gestionada para cargas de trabajo de series temporales, analíticas e IA. Tanto las opciones autogestionadas como las de la nube permiten a las organizaciones capturar, almacenar y analizar datos de series temporales a escala, desde el borde hasta despliegues centralizados en la nube.

[Percona](https://percona.com) es una empresa de software, soporte y servicios de bases de datos de código abierto centrada en ayudar a las organizaciones a mantener el control total sobre su infraestructura de datos. Ayudan a las empresas a ejecutar MySQL, PostgreSQL, MongoDB, Valkey y Redis de forma segura y eficiente mediante software de código abierto disponible libremente, soporte experto 24/7 y experiencia práctica en bases de datos.

[Eon.io](https://eon.io) es una infraestructura de nube inteligente para copias de seguridad, recuperación y gestión de datos que ayuda a los equipos a almacenar y acceder a las copias de seguridad de forma más eficiente, haciendo que los datos sean accesibles para flujos de trabajo de analíticas e IA. Ofrece recuperación rápida y granular y costes de almacenamiento significativamente más bajos para Postgres y cargas de trabajo intensivas en datos en todas las nubes, incluida la recuperación tras pérdidas accidentales de datos y regresiones de agentes de IA.

Estas organizaciones confían en pgBackRest para proporcionar recuperación ante desastres fiable para sus productos y clientes. Su inversión refleja el papel crítico que pgBackRest desempeña en el ecosistema de PostgreSQL, y su apoyo colectivo garantiza la sostenibilidad del proyecto a largo plazo.

Tengo muchas ganas de volver al trabajo. Hay funcionalidades y optimizaciones en camino que estoy deseando compartir en las próximas versiones. Gracias a nuestros patrocinadores por hacer esto posible, y gracias a la comunidad por su paciencia y apoyo durante esta transición.


--------

## Actualización de mantenimiento {#maintenance-update}

**4 de mayo de 2026**

Después de que anunciara que ya no mantengo pgBackRest, mi bandeja de entrada explotó. Tardé un tiempo en ordenar los mensajes — muchos de ellos eran buenos deseos y agradecimientos por mi trabajo a lo largo de los años.

Pero pronto surgió un patrón. Está claro que muchos usuarios de pgBackRest, especialmente aquellos que deben dar soporte a usuarios propios de pgBackRest, preferirían que el proyecto continuara conmigo como mantenedor principal. Nada me gustaría más, pero después de meses de búsqueda de financiación acababa de decidir que no iba a suceder.

Ahora la situación ha cambiado y parece prácticamente seguro que podré conseguir financiación suficiente para continuar el proyecto. Esta vez pgBackRest estará financiado por una coalición de patrocinadores, de modo que una única adquisición ya no afectará a mi capacidad para seguir trabajando en el proyecto. También deberíamos poder incorporar a otro mantenedor para distribuir la carga de trabajo y proporcionar continuidad en el futuro.

Sé que esto ha sido una conmoción y que hay mucha incertidumbre. Ten paciencia — la versión actual de pgBackRest funciona y no hay bugs críticos pendientes ni problemas de seguridad, así que no hay necesidad de hacer un fork del proyecto de inmediato.

Espero poder hacer un anuncio más definitivo antes de que termine la semana. Hasta entonces, mantente a la espera y ten por seguro que estamos trabajando activamente para revivir pgBackRest.


--------

## pgBackRest ya no se mantiene {#no-longer-maintained}

**27 de abril de 2026**

TL;DR: pgBackRest ya no se mantiene. Si haces un fork de pgBackRest, selecciona un nombre nuevo para tu proyecto.

Después de pensarlo mucho, he decidido dejar de trabajar en pgBackRest. No tomé esta decisión a la ligera. pgBackRest ha sido mi proyecto y mi pasión durante los últimos trece años y tuve la fortuna de contar con patrocinio corporativo durante gran parte de ese tiempo, pero también hubo muchas noches hasta tarde y fines de semana mientras trabajaba para hacer de pgBackRest el proyecto que es hoy, con la ayuda de numerosos colaboradores. Cada desarrollador de código abierto sabe exactamente a qué me refiero y cuánta de tu vida se dedica a un proyecto especial.

Desde que Crunchy Data fue vendida, he estado manteniendo pgBackRest y buscando un puesto que me permitiera continuar el trabajo, pero hasta ahora no he tenido éxito. Del mismo modo, mis esfuerzos por conseguir patrocinio también han quedado muy lejos de lo que necesito para que el proyecto sea viable.

Como cualquier otra persona, tengo que ganarme la vida, y la gama de puestos relacionados con pgBackRest es muy limitada. Ahora puedo considerar una variedad más amplia de oportunidades, pero estas no me dejarán tiempo para trabajar en pgBackRest, que requiere bastante tiempo para mantenimiento, corrección de bugs, revisión de PR, respuesta a issues, etc. Eso sin contar el tiempo para escribir funcionalidades nuevas, que es lo que de verdad me encanta hacer. En lugar de hacer el trabajo de forma deficiente y/o esporádica, creo que tiene más sentido hacer un alto definitivo.

Imagino que en algún momento se hará un fork de pgBackRest, pero será un proyecto nuevo con nuevos mantenedores, y estos tendrán que ganarse la confianza de la misma manera que lo hicimos nosotros.

Una vez más, muchas gracias a todos los colaboradores de pgBackRest a lo largo de los años. ¡Fue un placer trabajar con todos!
