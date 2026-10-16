---
title: "Notas de la versión"
linkTitle: "Versiones"
weight: 60
description: "Historial de versiones de pgBackRest con un registro de cambios detallado para cada versión."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [Referencia]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## Introducción {#introduction}

Los números de versión de pgBackRest constan de dos partes: principal y secundaria. Una versión principal *puede* romper la compatibilidad con la versión principal anterior, pero las versiones v2 son totalmente compatibles con los repositorios v1 y aceptarán todas las opciones v1. Las versiones secundarias pueden incluir correcciones de errores y funcionalidades, pero no cambian el formato del repositorio y procuran evitar cambios en las opciones y en los nombres. La documentación de la versión v1 puede encontrarse [aquí](https://pgbackrest.org/1). Las notas de una versión también pueden contener «Notas adicionales», pero los cambios en esa sección afectan únicamente a la documentación o a la suite de pruebas y no tienen impacto directo en el código base de pgBackRest.


--------

## Versión estable documentada {#current-stable-release}

Este espejo cubre la v2.59.3. Consulta el [historial de versiones original](https://pgbackrest.org/release.html) para las versiones más recientes.

### Notas de la versión v2.59.3 {#v2593-release-notes}

*Error de subclaves de cifrado débiles*

*Publicada el 4 de octubre de 2026*

**NOTA IMPORTANTE**: En versiones anteriores era posible que se generaran subclaves y sales de cifrado débiles si se producía un error al acceder a los datos aleatorios del sistema. Consulta [Subclaves y sales de cifrado débiles](/es/pgbackrest/news/#weak-encryption) para obtener más información.

**Correcciones de errores:**

- Corregido un posible error de suma de verificación al cargar los archivos de información y manifiesto cifrados. (*Corregido por j0uinim. Revisado por David Steele.*)
- Corregida la posible generación de subclaves/sales de cifrado débiles. (*Corregido por j0uinim. Revisado por David Steele, Stefan Fercot, Douglas J Hunley.*)


--------

## Versiones estables {#stable-releases}


### Notas de la versión v2.59.2 {#v2592-release-notes}

*Soporte de PostgreSQL 19beta4*

*Publicada el 27 de septiembre de 2026*

**Correcciones de errores:**

- Corregido un mapa de bloques vacío cuando un archivo se trunca a cero durante la copia de seguridad. (*Revisado por Douglas J Hunley. Reportado por JPCOSTA78.*)
- Desactivado el reintento de lectura cuando se pasan filtros al controlador. (*Revisado por Douglas J Hunley. Reportado por megamaced.*)
- Corregida la paginación del listado de versiones de S3. (*Revisado por Douglas J Hunley, guruguruguru. Reportado por guruguruguru.*)
- Establecido el encabezado de versión de Azure para la autenticación SAS. (*Revisado por Douglas J Hunley. Reportado por Florian Helmberger.*)
- Corregido el bloqueo de `archive-push` asincrónico por un archivo de historial de copias de seguridad de tamaño cero. (*Corregido por Andrew Kroh. Revisado por David Steele, Douglas J Hunley.*)
- Corregido el comando `annotate` en un repositorio remoto cifrado. (*Corregido por Douglas J Hunley. Revisado por David Steele.*)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta4.



### Notas de la versión v2.59.1 {#v2591-release-notes}

*Soporte de PostgreSQL 19beta3*

*Publicada el 17 de agosto de 2026*

**Correcciones de errores:**

- Corregido el bloqueo cuando el búfer de fragmentos es más pequeño que el búfer de entrada. (*Revisado por Andrew Pogrebnoi, Douglas J Hunley. Reportado por crajac66.*)
- Comparar una etiqueta de copia de seguridad nueva solo contra su propio conjunto basado en una copia de seguridad completa. (*Revisado por Douglas J Hunley. Reportado por Anton Glushakov.*)
- Corregidos los archivos fuente generados por GitHub a los que les faltaban archivos necesarios para compilar. (*Reportado por aardvarkzed.*)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta3. (*Contribución de Lardière Sébastien. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Documentar la excepción para los puntos en los nombres de bucket de S3 cuando `repo-s3-uri-style=path`.
- Eliminada la configuración explícita de `hot_standby` de la guía de usuario.


### Notas de la versión v2.59.0 {#v2590-release-notes}

*Soporte de PostgreSQL 19beta2*

*Publicada el 20 de julio de 2026*

**NOTA PARA EMPAQUETADORES**: Hay disponible un nuevo tarball de distribución que simplifica el proceso de compilación al proporcionar documentación HTML pregenerada, página de manual y código. El tarball se adjunta a cada versión como un recurso y se llama `pgbackrest-{version}.tar.gz`. Consulta el `README.md` del tarball para más detalles. Usa el nuevo tarball de distribución para evitar las herramientas de compilación adicionales que se requerirán para generar código en versiones futuras. Consulta [Nuevo tarball de distribución](/es/pgbackrest/news/#distribution-tarball) para obtener más información. **NOTA PARA EMPAQUETADORES**: Ahora existe una nueva dependencia opcional de `libsystemd`. **NOTA IMPORTANTE**: A partir de esta versión, por defecto solo el comando `restore` puede ejecutarse como root. Usa `allow-root` para ejecutar otros comandos como root (aunque no se recomienda).

**Correcciones de errores:**

- Corregir que `expire` elimine una copia de seguridad en curso en otro host. (*Revisado por Douglas J Hunley. Reportado por Dmitrii.*)
- Corregir que `archive-push-queue-max` no se aplique cuando un archivo WAL provoca un error. (*Revisado por Stefan Fercot. Reportado por vut12.*)
- Corregir el fallo de `archive-get` asincrónico durante una recuperación a través de un cambio de línea de tiempo. (*Revisado por Douglas J Hunley. Reportado por Jimmy Yih.*)
- Corregir un posible desbordamiento de búfer en el módulo de errores. (*Corregido por Christophe Pettus. Revisado por David Steele.*)
- Corregir un use-after-free del cliente de protocolo paralelo. (*Revisado por Douglas J Hunley. Reportado por Georgy Shelkovy.*)
- Corregir un desbordamiento del heap cuando se configura una opción pg sin pg1. (*Revisado por Douglas J Hunley. Reportado por Naveen.*)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta2. (*Revisado por Stefan Fercot.*)
- Añadir la opción `archive-expire-before` para limpiar el archivado de WAL. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Añadir la eliminación por lotes para el almacenamiento Azure. (*Revisado por Douglas J Hunley, Crispy.*)
- Añadir soporte para S3 Outposts. (*Contribución de Shiva Kumar Ambigi. Revisado por David Steele, Roberto Mello.*)
- Añadir la autenticación de S3 mediante un proceso. (*Revisado por Andrew Charlton. Sugerido por Andrew Charlton.*)

**Mejoras:**

- Reconectar el almacenamiento SFTP después de que el servidor cierre una conexión inactiva. (*Revisado por Stefan Fercot. Sugerido por mustafa0x, tisserat.*)
- Añadir caché de usuario/grupo para una construcción más rápida del manifiesto. (*Contribución de Gunnar Lindholm. Revisado por David Steele.*)
- Añadir el progreso de copia de seguridad por repositorio a la salida del comando `info`. (*Contribución de Will Morland. Revisado por David Steele, Stefan Fercot.*)
- Añadir comprobaciones de `backup.info` al comando `verify`. (*Contribución de Denis Garsh. Revisado por David Steele, Douglas J Hunley.*)
- Permitir configurar el endpoint STS de S3. (*Contribución de Simon Gratton. Revisado por David Steele.*)
- Añadir `archive-push-batch-size` para limitar el WAL enviado por ejecución asincrónica. (*Revisado por Stefan Fercot.*)
- Salir de `archive-push` asincrónico en el primer error. (*Revisado por Stefan Fercot. Sugerido por Lardière Sébastien.*)
- Reforzar el análisis de respuestas HTTP por fragmentos. (*Contribución de Shubham. Revisado por David Steele.*)
- Generar un error al ejecutar como root a menos que `allow-root` esté habilitado. (*Revisado por Douglas J Hunley.*)
- Menos búsquedas binarias al construir el manifiesto. (*Contribución de Gunnar Lindholm. Revisado por David Steele.*)
- Mejorar el rendimiento de seek durante la restauración delta incremental por bloques. (*Revisado por David Christensen, Douglas J Hunley.*)
- Agrupar los archivos de la copia de seguridad en orden en lugar de explorar buscando un mejor ajuste. (*Revisado por Stefan Fercot.*)
- Reportar el error subyacente cuando una consulta no se completa. (*Revisado por Andrew Pogrebnoi. Sugerido por Marco Fontana.*)
- Reportar el error real cuando falla una solicitud de credenciales de S3. (*Revisado por Douglas J Hunley. Sugerido por Mitchell Grice.*)
- Reportar los errores de la ruta de spool de `archive-push` al registro de PostgreSQL. (*Revisado por Douglas J Hunley. Sugerido por Don Seiler.*)
- Sugerir que pgBackRest puede estar desactualizado cuando no se soporta una versión.
- Añadir integración de notificaciones de systemd. (*Contribución de Andrew Jackson. Revisado por David Steele.*)
- Suprimir los errores `unused parameter` en los sondeos del compilador de meson. (*Contribución de Jörg Plate. Revisado por David Steele.*)
- C11 es ahora el estándar mínimo de C. (*Revisado por Mohammad Ali Nazir Kosar.*)

**Mejoras en la documentación:**

- Hacer interna la opción `stanza` para los comandos `repo-*`. (*Revisado por Stefan Fercot.*)
- Documentar que info lee la configuración de cifrado de la sección global. (*Revisado por Stefan Fercot. Sugerido por Ron Johnson.*)
- Documentar que `expire-auto` usa la configuración del comando `backup`. (*Revisado por Stefan Fercot. Sugerido por Lardière Sébastien.*)
- Documentar el ajuste de la directiva `su` de logrotate para un usuario dedicado. (*Revisado por Douglas J Hunley. Sugerido por lkanbus.*)
- Documentar que los comentarios al final de línea no están soportados en los archivos de configuración. (*Revisado por Douglas J Hunley. Sugerido por Alex Richman.*)

**Mejoras en la suite de pruebas:**

- Corregir conflictos de grupos de Alpine en los contenedores de CI. (*Contribución de Artur Zakirov. Revisado por David Steele.*)


### Notas de la versión v2.58.0 {#v2580-release-notes}

*Mejoras en el almacenamiento de objetos*

*Publicada el 19 de enero de 2026*

**NOTA IMPORTANTE**: Los valores mínimos de la opción `repo-storage-upload-chunk-size` han aumentado. Ahora representan el mínimo permitido por los proveedores.

**Correcciones de errores:**

- Corregir un interbloqueo debido al registro en el manejador de señales. (*Corregido por Maxim Michkov. Revisado por David Steele.*)

**Funcionalidades:**

- Soporte de HTTP para S3, GCS y Azure. (*Contribución de Will Morland. Revisado por David Steele.*)
- Permitir la expiración de la copia de seguridad completa más antigua independientemente de la retención actual. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Ron Johnson.*)
- Soporte para identidades administradas de Azure. (*Contribución de Moiz Ibrar, Matthew Mols. Revisado por David Steele.*)
- Soporte ***experimental*** de la identidad de pod de S3 EKS. (*Contribución de Pierre BOUTELOUP. Revisado por David Steele.*)
- Permitir la configuración de suites de cifrado TLS. (*Contribución de Gunnar "Nick" Bluth. Revisado por David Steele.*)
- Permitir establecer la prioridad del proceso. (*Revisado por Douglas J Hunley.*)

**Mejoras:**

- Permitir puntos en los nombres de bucket de S3 cuando se usan URI con estilo de ruta. (*Contribución de Joakim Hindersson. Revisado por David Steele.*)
- Requerir TLS >= 1.2 a menos que la verificación esté deshabilitada. (*Revisado por Douglas J Hunley, Gunnar "Nick" Bluth.*)
- Dimensionar dinámicamente los fragmentos de S3/GCS/Azure para cargas grandes. (*Revisado por Douglas J Hunley. Sugerido por Timothée Peignier.*)
- Optimizar el tamaño de fragmento de S3/GCS/Azure para archivos pequeños. (*Revisado por Douglas J Hunley.*)
- Eliminar el soporte de PostgreSQL `9.5`. (*Revisado por Douglas J Hunley.*)
- Mejorar el registro del valor por defecto de opciones con una dependencia sin resolver. (*Revisado por Stefan Fercot.*)

**Mejoras en la documentación:**

- Eliminar la configuración explícita de `max_wal_senders`/`wal_level` de la guía de usuario. (*Sugerido por Jamie Nguyen.*)
- Aclarar que el agrupamiento es útil para sistemas de archivos con tamaños de bloque grandes. (*Sugerido por Ron Johnson.*)


### Notas de la versión v2.57.0 {#v2570-release-notes}

*Supresión de enlaces simbólicos del repositorio*

*Publicada el 18 de octubre de 2025*

**Correcciones de errores:**

- Desanidar los tiempos de espera de HTTP/TLS/socket. (*Revisado por David Christensen.*)
- Corregir un posible segfault en el mensaje de error de la suma de verificación de páginas. (*Corregido por Zsolt Parragi. Revisado por David Steele.*)

**Funcionalidades:**

- Añadir la opción `repo-symlink` para suprimir la creación de enlaces simbólicos del repositorio. (*Revisado por Douglas J Hunley. Sugerido por Ron Johnson.*)

**Mejoras:**

- Añadir reintentos HTTP para los errores 408 y 429. (*Revisado por David Christensen.*)


### Notas de la versión v2.56.0 {#v2560-release-notes}

*Mejoras en la información de progreso*

*Publicada el 21 de julio de 2025*

**Correcciones de errores:**

- Corregir un problema con la expiración ad hoc cuando no hay copias de seguridad en un repositorio. (*Revisado por Stefan Fercot. Reportado por Anup Gupta.*)

**Funcionalidades:**

- Añadir el progreso de restauración a la salida del comando `info`. (*Contribución de Denis Garsh, Maxim Michkov. Revisado por David Steele.*)
- Añadir un nivel de detalle de solo progreso para la salida del comando `info`. (*Contribución de Denis Garsh. Revisado por David Steele, Stefan Fercot.*)

**Mejoras:**

- Reintentar lecturas fallidas en almacenes de objetos. (*Revisado por David Christensen.*)
- Corregir los valores por defecto en la ayuda de línea de comandos. (*Revisado por David Christensen, Chris Bandy.*)

**Mejoras en la documentación:**

- Describir los valores discretos de las opciones en una lista donde corresponda. (*Contribución de Anton Kurochkin. Revisado por David Steele.*)
- Corregir «menor que» en la salida de ayuda de la opción `archive-mode`. (*Contribución de Anton Kurochkin. Revisado por David Steele.*)


### Notas de la versión v2.55.1 {#v2551-release-notes}

*Correcciones de errores*

*Publicada el 5 de mayo de 2025*

**Correcciones de errores:**

- Revertir «calcular content-md5 en S3 solo cuando sea necesario». (*Revisado por David Christensen. Reportado por Frank Brendel.*)
- Corregir la comprobación de los límites inferiores de las claves de opción. (*Revisado por David Christensen, Wolfgang Walther. Reportado por Wolfgang Walther.*)


### Notas de la versión v2.55.0 {#v2550-release-notes}

*Mejoras de verificación y soporte de PostgreSQL 18*

*Publicada el 21 de abril de 2025*

**Correcciones de errores:**

- Corregir un problema de restauración incremental por bloques en un repositorio no predeterminado. (*Revisado por David Christensen, Aleksander Łukasz. Reportado por Aleksander Łukasz.*)
- No establecer `recovery_target_timeline=current` para PostgreSQL < 12. (*Revisado por Stefan Fercot.*)
- Corregir el registro del rango de archivado en expire. (*Revisado por Stefan Fercot. Reportado por Aleš Zelený.*)
- Corregir el reporte de errores para consultas sin resultados. (*Revisado por Stefan Fercot. Reportado por Susantha Bathige.*)

**Funcionalidades:**

- Verificar la línea de tiempo objetivo de recuperación. (*Revisado por Stefan Fercot.*)
- Permitir la verificación de una copia de seguridad especificada. (*Contribución de Maxim Michkov. Revisado por David Steele.*)
- Añadir soporte para requester pays de S3/GCS. (*Contribución de Timothée Peignier. Revisado por David Steele.*)
- Soporte de PostgreSQL 18. (*Revisado por Stefan Fercot.*)
- Permitir conexiones a PostgreSQL en sockets de dominio abstractos. (*Revisado por Chris Bandy. Sugerido por Chris Bandy.*)
- Añadir salida numérica al comando `version`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

**Mejoras:**

- Permitir que el comando backup opere en repositorios remotos. (*Revisado por Stefan Fercot.*)
- Usar lz4 para la compresión del protocolo. (*Revisado por Stefan Fercot.*)
- Calcular `content-md5` en S3 solo cuando sea necesario. (*Revisado por David Christensen.*)
- Advertir cuando se sobrescribe el valor de una opción multi-clave. (*Revisado por David Christensen, Stefan Fercot.*)
- Añadir registro de detalle para la ruta de archivado expirada. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Eliminar el soporte de PostgreSQL `9.4`. (*Revisado por Stefan Fercot.*)
- Eliminar la compilación con autoconf/make. (*Revisado por David Christensen.*)

**Mejoras en la documentación:**

- Corregir la documentación sobre cómo especificar varias stanzas con `tls-server-auth`. (*Revisado por David Christensen, Stefan Fercot. Sugerido por Terry MacAndrew.*)
- Aclarar la expiración de copias de seguridad incrementales. (*Revisado por Stefan Fercot.*)
- Aclarar el requisito de que las versiones local/remota de pgBackRest coincidan. (*Contribución de Greg Clough. Revisado por David Steele.*)
- Añadir una pregunta frecuente sobre cómo exportar un clúster autocontenido. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Advertir sobre `--tablespace-map-all` respecto a la creación de tablespaces. (*Revisado por Stefan Fercot, Christophe Courtois. Sugerido por Christophe Courtois.*)
- Aclarar el comportamiento de `--repo-retention-full-type`. (*Revisado por Antoine Beaupré. Sugerido por Antoine Beaupré.*)
- Cambiar la recomendación de `--process-max` para almacenes de objetos a `--repo-bundle`. (*Revisado por Stefan Fercot.*)
- Actualizar `unix_socket_directory` a `unix_socket_directories`. (*Contribución de hyunkyu han. Revisado por David Steele.*)
- Recomendar no colocar `spool-path` dentro de `pg_xlog`/`pg_wal`. (*Revisado por Martín Marqués, Don Seiler. Sugerido por Martín Marqués.*)


### Notas de la versión v2.54.2 {#v2542-release-notes}

*Corrección de error*

*Publicada el 20 de enero de 2025*

**Correcciones de errores:**

- Corregir un problema tras deshabilitar el agrupamiento con el incremental por bloques habilitado. (*Revisado por David Christensen.*)

**Mejoras en la documentación:**

- Aclarar el comportamiento de múltiples archivos de configuración. (*Revisado por Paul Bierly. Sugerido por Paul Bierly.*)


### Notas de la versión v2.54.1 {#v2541-release-notes}

*Corrección de error*

*Publicada el 16 de diciembre de 2024*

**Correcciones de errores:**

- Corregir un problema por el que los comandos `version`/`help` intentaban cargar `pgbackrest.conf`. (*Revisado por Stefan Fercot. Reportado por Bradford Boyle, Julian.*)

**Mejoras en la suite de pruebas:**

- Estabilizar el archivado asincrónico en las pruebas de integración. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)


### Notas de la versión v2.54.0 {#v2540-release-notes}

*Tiempo objetivo para el almacenamiento con versionado*

*Publicada el 21 de octubre de 2024*

**NOTA PARA EMPAQUETADORES**: Esta es la última versión de funcionalidades que soporta la compilación con autoconf/make. Migra a meson si aún no lo has hecho. Las versiones de parche 2.54.X (si las hay) seguirán soportando autoconf/make.

**Correcciones de errores:**

- Corregir el rendimiento de las consultas de PostgreSQL para conjuntos de datos grandes. (*Corregido por Thibault Vincent, David Steele. Revisado por David Christensen, Antoine Millet. Reportado por Antoine Millet.*)

**Funcionalidades:**

- Permitir que los repositorios en almacenamiento con versionado se lean en un tiempo objetivo. (*Revisado por Stefan Fercot, David Christensen.*)
- Permitir que una copia de seguridad desde réplica solicitada continúe sin réplica. (*Revisado por Stefan Fercot.*)

**Mejoras:**

- Resumir la lista de referencias de la copia de seguridad en la salida de texto del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Refrescar el token web-id en cada autenticación de S3. (*Contribución de Brent Graveland. Revisado por David Steele.*)
- Mostrar correctamente los valores actuales de las opciones indexadas en la ayuda. (*Revisado por David Christensen.*)
- Guardar `backup.info` solo cuando el contenido haya cambiado. (*Revisado por Stefan Fercot.*)
- Eliminar la limitación de lectura de archivos en paralelo durante la restauración. (*Revisado por David Christensen.*)
- Mejorar los mensajes de error de SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)

**Funcionalidades de la documentación:**

- Añadir una sección de ajuste de rendimiento a la guía de usuario. (*Revisado por Stefan Fercot.*)

**Mejoras en la documentación:**

- Aclarar el origen de `data_directory`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Matthias.*)
- Mejor lógica para decidir cuándo un resumen debe ir en minúsculas. (*Sugerido por Daniel Westermann.*)


### Notas de la versión v2.53.1 {#v2531-release-notes}

*Soporte de PostgreSQL 17*

*Publicada el 19 de agosto de 2024*

**Correcciones de errores:**

- Corregir los permisos cuando `restore` se ejecuta como usuario root. (*Revisado por Stefan Fercot. Reportado por Will M.*)
- Corregir un segfault en errores de conexión diferidos. (*Revisado por David Christensen. Reportado por Anton Glushakov.*)
- Omitir la comprobación de duplicados del repositorio local para SFTP. (*Corregido por Reid Thompson. Revisado por David Steele. Reportado por Anton Kurochkin.*)

**Mejoras:**

- Soporte de PostgreSQL 17.


### Notas de la versión v2.53 {#v253-release-notes}

*Copias de seguridad concurrentes*

*Publicada el 22 de julio de 2024*

**NOTA IMPORTANTE**: El valor por defecto de la opción `log-level-stderr` ha cambiado de `warn` a `off`. Esto facilita capturar errores cuando solo se redirige `stdout`. Para conservar el comportamiento anterior, establece `log-level-stderr=warn`. **NOTA PARA EMPAQUETADORES**: La biblioteca lz4 ahora es requerida por la compilación con meson. **NOTA PARA EMPAQUETADORES**: El soporte del compilador para `__builtin_clzl()` y `__builtin_bswap64()` ahora es requerido por la compilación con meson.

**Correcciones de errores:**

- Corregir el fallo de renombrado SFTP cuando el archivo ya existe. (*Corregido por Reid Thompson. Revisado por David Steele. Reportado por ahmed112212.*)

**Funcionalidades:**

- Permitir que las copias de seguridad se ejecuten concurrentemente en repositorios diferentes. (*Revisado por Reid Thompson, Stefan Fercot.*)
- Soportar SAN basados en IP para la validación de certificados TLS. (*Contribución de David Christensen. Revisado por David Steele.*)

**Mejoras:**

- Establecer por defecto la opción `log-level-stderr` en `off`. (*Revisado por Greg Sabino Mullane, Stefan Fercot.*)
- Permitir tamaños de segmento WAL alternativos para PostgreSQL ≤ 10. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)
- Añadir una sugerencia para revisar el registro de autorización de SFTP. (*Contribución de Vitalii Zurian. Revisado por Reid Thompson, David Steele.*)

**Mejoras en la documentación:**

- Aclarar el comportamiento multi-repositorio de `archive-push`. (*Revisado por Stefan Fercot.*)


### Notas de la versión v2.52.1 {#v2521-release-notes}

*Corrección de error*

*Publicada el 25 de junio de 2024*

**Correcciones de errores:**

- Corregir un problema con archivos más grandes en la réplica que en el primario. (*Revisado por Stefan Fercot. Reportado por Nicolas Lassimonne.*)


### Notas de la versión v2.52 {#v252-release-notes}

*Soporte de PostgreSQL 17beta1*

*Publicada el 27 de mayo de 2024*

**NOTA PARA EMPAQUETADORES**: El sistema de compilación de pgBackRest ahora es meson. La compilación con autoconf/make no recibirá nuevas funcionalidades y se eliminará después de algunas versiones.

**Funcionalidades:**

- Añadir soporte de eliminación por lotes de GCS. (*Revisado por Reid Thompson.*)
- Soporte de cifrado `SSE-C` de S3. (*Revisado por Tim Jones. Sugerido por Tim Jones.*)
- Soporte de PostgreSQL 17beta1. (*Revisado por Stefan Fercot.*)

**Mejoras:**

- Permitir la deshabilitación explícita de dependencias opcionales en las compilaciones con meson. (*Contribución de Michael Schout. Revisado por David Steele.*)
- Buscar dinámicamente python en la compilación con meson. (*Contribución de Michael Schout. Revisado por David Steele.*)
- Marcar el objetivo de compilación `pgbackrest` en meson como instalable. (*Contribución de Bradford Boyle. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Actualizar la documentación de `start`/`stop` para reflejar la funcionalidad real. (*Revisado por Stefan Fercot.*)


### Notas de la versión v2.51 {#v251-release-notes}

*Sistema de compilación Meson*

*Publicada el 25 de marzo de 2024*

**Correcciones de errores:**

- Omitir archivos de longitud cero para la restauración delta incremental por bloques. (*Revisado por Sebastian Krause, René Højbjerg Larsen. Reportado por Sebastian Krause.*)
- Corregir una regresión de rendimiento en el listado de almacenamiento. (*Revisado por Stephen Frost. Reportado por Maksym Boguk.*)
- Corregir el registro de progreso cuando el tamaño del archivo cambia durante la copia de seguridad. (*Revisado por Stephen Frost. Reportado por samkingno.*)

**Mejoras:**

- Soporte mejorado para conexiones dual stack. (*Revisado por Stephen Frost. Sugerido por Timothée Peignier.*)
- Hacer de meson el sistema de compilación principal. (*Revisado por Stephen Frost.*)
- Detectar archivos que no han cambiado durante una copia de seguridad incremental no delta. (*Revisado por Stephen Frost.*)
- Evitar una recuperación inválida cuando se elimina `backup_label`. (*Revisado por Stephen Frost.*)
- Mejorar el manejo de la cola de segmentos WAL de `archive-push`. (*Revisado por Stephen Frost.*)
- Limitar la funcionalidad de reanudación a las copias de seguridad completas. (*Revisado por Stephen Frost, Stefan Fercot.*)
- Actualizar la funcionalidad de reanudación para el incremental por bloques. (*Revisado por Stephen Frost.*)
- Permitir `--version` y `--help` para versión y ayuda. (*Revisado por Greg Sabino Mullane. Sugerido por Greg Sabino Mullane.*)
- Añadir un backtrace detallado a la compilación con autoconf/make. (*Revisado por Stephen Frost.*)

**Mejoras en la documentación:**

- Actualizar las referencias a `recovery.conf`. (*Revisado por Stefan Fercot. Sugerido por Stephen Frost.*)


### Notas de la versión v2.50 {#v250-release-notes}

*Mejoras de rendimiento y correcciones de errores*

*Publicada el 22 de enero de 2024*

**Correcciones de errores:**

- Corregir una lectura corta en la restauración incremental por bloques. (*Revisado por Stephen Frost, Brent Graveland. Reportado por Adol Rodriguez, Brent Graveland.*)
- Corregir un desbordamiento que suprimía el progreso de la copia de seguridad en la salida de `info`. (*Corregido por Robert Donovan. Revisado por Joe Wildish.*)

**Mejoras:**

- Preservar archivos parciales durante la restauración delta incremental por bloques. (*Revisado por Stephen Frost.*)
- Añadir soporte para tamaños de página alternativos en tiempo de compilación. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)
- Omitir archivos truncados durante la copia de seguridad al agrupar. (*Contribución de Georgy Shelkovy. Revisado por David Steele.*)
- Mejorar los mensajes de error del almacenamiento SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)


### Notas de la versión v2.49 {#v249-release-notes}

*Eliminación del soporte de PostgreSQL 9.3*

*Publicada el 27 de noviembre de 2023*

**Correcciones de errores:**

- Corregir una regresión en los reintentos. (*Revisado por Stephen Frost. Reportado por Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)
- Corregir la eliminación recursiva de rutas en el controlador de almacenamiento SFTP. (*Corregido por Reid Thompson. Revisado por Stephen Frost. Reportado por Luc.*)

**Mejoras:**

- Eliminar el soporte de PostgreSQL `9.3`. (*Revisado por Stephen Frost.*)

**Funcionalidades de la documentación:**

- Documentar las opciones del mantenedor. (*Revisado por Stefan Fercot.*)
- Actualizar la documentación de recuperación en un punto en el tiempo para PostgreSQL >= 13.

**Mejoras en la suite de pruebas:**

- Permitir que la prueba unitaria `config/load` se ejecute sin `libssh2` instalado. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Wu Ning.*)


### Notas de la versión v2.48 {#v248-release-notes}

*Etiquetas de almacenamiento del repositorio*

*Publicada el 25 de septiembre de 2023*

**Correcciones de errores:**

- Corregir un problema al restaurar incremental por bloques sin una lista de bloques. (*Revisado por Stephen Frost, Burak Yurdakul. Reportado por Burak Yurdakul.*)

**Funcionalidades:**

- Añadir la opción `--repo-storage-tag` para crear etiquetas de objetos. (*Revisado por Stephen Frost, Stefan Fercot, Timothée Peignier.*)
- Añadir comprobación de known hosts para el controlador de almacenamiento SFTP. (*Contribución de Reid Thompson. Revisado por Stephen Frost, David Steele.*)
- Soporte para conexiones dual stack. (*Revisado por Stephen Frost.*)
- Añadir el tamaño completado/total de la copia de seguridad a la salida JSON del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

**Mejoras:**

- Comando check multi-stanza. (*Revisado por Stephen Frost.*)
- Reintentar lecturas de `pg_control` hasta que la suma de verificación sea válida. (*Revisado por Stefan Fercot, Stephen Frost.*)
- Optimizar la comprobación del segmento WAL después de una copia de seguridad exitosa. (*Revisado por Stephen Frost.*)
- Mejorar el rendimiento multiparte de GCS. (*Revisado por Reid Thompson.*)
- Permitir que el comando `archive-get` se ejecute cuando la stanza está detenida. (*Revisado por Tom Swartz, David Christensen, Reid Thompson.*)
- Aceptar la virgulilla inicial en las rutas de las claves públicas/privadas SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Recargar las credenciales de GCS antes de renovar el token de autenticación. (*Revisado por Stephen Frost. Sugerido por Daniel Farina.*)

**Correcciones de errores en la documentación:**

- Corregir el ejemplo de la referencia de configuración para la opción `tls-server-address`. (*Corregido por Hartmut Goebel. Revisado por David Steele.*)
- Corregir el ejemplo de la referencia de comandos para la opción `filter`.

**Mejoras en la suite de pruebas:**

- Permitir que la prueba unitaria `storage/sftp` se ejecute sin `libssh2` instalado. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Wu Ning.*)


### Notas de la versión v2.47 {#v247-release-notes}

*Mejoras de rendimiento y correcciones de errores*

*Publicada el 24 de julio de 2023*

**Correcciones de errores:**

- Preservar la información del incremental por bloques en el manifiesto durante una copia de seguridad delta. (*Revisado por Stephen Frost. Reportado por Francisco Miguel Biete Banon.*)
- Corregir los nombres de archivo del incremental por bloques en el comando `verify`. (*Revisado por Reid Thompson. Reportado por Francisco Miguel Biete Banon.*)
- Corregir una copia de seguridad delta automática espuria en una copia desde réplica. (*Revisado por Stephen Frost. Reportado por krmozejko, Don Seiler.*)
- Omitir `recovery.signal` para PostgreSQL >= 12 cuando la recuperación es `type=none`. (*Revisado por Stefan Fercot. Reportado por T.Anastacio.*)
- Corregir la generación de etiquetas únicas para copias de seguridad diff/incr. (*Corregido por Andrey Sokolov. Revisado por David Steele.*)
- Corregir la expiración de archivado basada en tiempo cuando no expira ninguna copia de seguridad. (*Revisado por Stefan Fercot.*)

**Mejoras:**

- Mejorar el rendimiento del controlador de almacenamiento SFTP. (*Contribución de Stephen Frost, Reid Thompson. Revisado por David Steele.*)
- Añadir el desplazamiento de zona horaria a la salida de fecha/hora del comando `info`. (*Revisado por Stefan Fercot, Philip Hurst. Sugerido por Philip Hurst.*)
- Centralizar el manejo de errores para funcionalidades no soportadas. (*Revisado por Stefan Fercot.*)

**Mejoras en la documentación:**

- Aclarar la preferencia por instalar desde paquetes en la guía de usuario. (*Revisado por Stefan Fercot. Sugerido por dr-kd.*)


### Notas de la versión v2.46 {#v246-release-notes}

*Copia de seguridad incremental por bloques y almacenamiento SFTP*

*Publicada el 22 de mayo de 2023*

**Funcionalidades:**

- Copia de seguridad incremental por bloques. (*Revisado por John Morris, Stephen Frost, Stefan Fercot.*)
- Soporte de SFTP para el almacenamiento del repositorio. (*Contribución de Reid Thompson. Revisado por Stephen Frost, David Steele.*)
- Soporte de PostgreSQL 16. (*Revisado por Stefan Fercot.*)

**Mejoras:**

- Permitir omitir las comprobaciones del encabezado de página. (*Revisado por David Christensen. Sugerido por David Christensen.*)
- Evitar `chown()` en los archivos de recuperación durante la restauración. (*Revisado por Stefan Fercot, Marcelo Henrique Neppel. Sugerido por Marcelo Henrique Neppel.*)
- Añadir detalle de reintento de error para los reintentos HTTP.

**Mejoras en la documentación:**

- Añadir una advertencia sobre el uso de la recuperación `type=none`. (*Revisado por Stefan Fercot.*)
- Añadir una nota sobre la ejecución de `stanza-create` en repositorios ya creados.


### Notas de la versión v2.45 {#v245-release-notes}

*Copia de seguridad incremental por bloques (BETA)*

*Publicada el 20 de marzo de 2023*

**Correcciones de errores:**

- Omitir por defecto la escritura de `recovery.signal` para restauraciones de copias de seguridad sin conexión. (*Revisado por Stefan Fercot. Reportado por Marcel Borger.*)

**Funcionalidades:**

- Copia de seguridad incremental por bloques (BETA). (*Revisado por John Morris, Stephen Frost, Stefan Fercot.*)

**Mejoras:**

- Mantener solo un índice de grupo con todos los valores por defecto. (*Revisado por Stefan Fercot.*)

**Mejoras en la documentación:**

- Añadir instrucciones explícitas para actualizar entre versiones `2.x`. (*Contribución de Christophe Courtois. Revisado por David Steele.*)
- Eliminar las referencias a SSH que quedaron obsoletas cuando se introdujo TLS.


### Notas de la versión v2.44 {#v244-release-notes}

*Eliminación del soporte de PostgreSQL 9.0/9.1/9.2*

*Publicada el 30 de enero de 2023*

**Mejoras:**

- Eliminar el soporte de PostgreSQL `9.0`/`9.1`/`9.2`. (*Revisado por Stefan Fercot.*)
- Mostrar errores al restaurar cuando ninguna copia de seguridad coincide con la versión actual de PostgreSQL. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Soulou.*)
- Añadir comprobación de rango para `compress-level` según cada `compress-type`. (*Revisado por Stefan Fercot. Sugerido por gkleen, ViperRu.*)

**Mejoras en la documentación:**

- Añadir una advertencia sobre habilitar el «espacio de nombres jerárquico» en el almacenamiento de Azure. (*Revisado por Stefan Fercot. Sugerido por Vojtech Galda, Pluggi, asjonos.*)
- Añadir un reemplazo para los saltos de línea en el ejemplo de monitoreo. (*Revisado por Stefan Fercot. Sugerido por rudonx, gmustdie, Ivan Shelestov.*)
- Aclarar el comportamiento de `target-action` en varias versiones de PostgreSQL. (*Contribución de Chris Bandy. Revisado por David Steele, Anton Kurochkin, Stefan Fercot. Sugerido por Anton Kurochkin, Chris Bandy.*)
- Actualizaciones y aclaraciones a la página de índice. (*Revisado por Stefan Fercot.*)
- Añadir el modo oscuro al sitio web. (*Sugerido por Stephen Frost.*)


### Notas de la versión v2.43 {#v243-release-notes}

*Corrección de error*

*Publicada el 28 de noviembre de 2022*

**Correcciones de errores:**

- Corregir una referencia faltante en la copia de seguridad diff/incr. (*Revisado por Stefan Fercot. Reportado por Marcel Borger, ulfedf, jaymefSO.*)

**Mejoras:**

- Añadir una sugerencia cuando se especifica una opción sin índice. (*Revisado por Stefan Fercot.*)


### Notas de la versión v2.42 {#v242-release-notes}

*Correcciones de errores*

*Publicada el 22 de noviembre de 2022*

**Correcciones de errores:**

- Corregir una fuga de memoria en `backup`/`restore` de agrupamientos de archivos. (*Revisado por John Morris, Oscar. Reportado por Oscar.*)
- Corregir un error de protocolo en una lectura corta de un archivo remoto. (*Revisado por Stephen Frost.*)

**Mejoras:**

- No almacenar referencias de archivos de longitud cero al agrupar. (*Revisado por Stefan Fercot.*)
- Usar descripciones más genéricas para `pg_start_backup()`/`pg_stop_backup()`. (*Revisado por Greg Sabino Mullane, David Christensen. Sugerido por Greg Sabino Mullane.*)

**Mejoras en la suite de pruebas:**

- Actualizar la opción `--psql-bin` de `test.pl` para que coincida con la ayuda de línea de comandos. (*Contribución de Koshi Shibagaki. Revisado por David Steele.*)


### Notas de la versión v2.41 {#v241-release-notes}

*Anotaciones de copias de seguridad*

*Publicada el 19 de septiembre de 2022*

**Correcciones de errores:**

- Corregir la expiración de tiempo incorrecta que se usaba para repositorios no predeterminados. (*Revisado por Stefan Fercot. Reportado por Adam Brusselback.*)
- Corregir un problema al listar directorios recursivamente con un filtro. (*Revisado por Stephen Frost. Reportado por Efremov Egor.*)

**Funcionalidades:**

- Anotaciones clave/valor para copias de seguridad. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Adam Berlin.*)

**Mejoras:**

- Soportar `--set` en la salida JSON del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Anton Kurochkin.*)
- Permitir configurar el tamaño de fragmento de carga para almacenes de objetos. (*Revisado por Stefan Fercot. Sugerido por Anton Glushakov.*)
- Actualizar las marcas de tiempo de archive.info después de una copia de seguridad exitosa. (*Revisado por Stefan Fercot. Sugerido por Alex Richman.*)
- Mover la comprobación de línea de tiempo de la réplica después del checkpoint. (*Revisado por Stefan Fercot, Keith Fiske. Sugerido por Keith Fiske.*)
- Mejorar el mensaje de advertencia al reanudar una copia de seguridad. (*Sugerido por Cynthia Shang.*)

**Mejoras en la documentación:**

- Añadir la ruta absoluta de `kill` en `pgbackrest.service`. (*Sugerido por Don Seiler.*)


### Notas de la versión v2.40 {#v240-release-notes}

*Soporte de OpenSSL 3*

*Publicada el 18 de julio de 2022*

**NOTA PARA EMPAQUETADORES**: Se ha añadido una compilación experimental con meson, pero los empaquetadores deberían seguir usando la compilación con autoconf/make en el futuro previsible.

**Mejoras:**

- Soporte de OpenSSL 3. (*Revisado por Stephen Frost.*)
- Crear una instantánea al listar el contenido de una ruta. (*Revisado por John Morris, Stephen Frost.*)
- Forzar `target-timeline=current` cuando la restauración es `type=immediate`. (*Revisado por Stephen Frost.*)
- Truncar archivos durante `restore` delta cuando son más grandes de lo esperado. (*Revisado por Stephen Frost.*)
- Desactivar el guardado incremental del manifiesto cuando `resume=n`. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Establecer el porcentaje completado de la copia de seguridad en cero antes de iniciar la copia. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Usar la bandera `IsTruncated` de S3 para determinar la continuación del listado. (*Revisado por John Morris, Soulou. Sugerido por Christian Montagne.*)

**Correcciones de errores en la documentación:**

- Omitir las opciones internas en la referencia de configuración. (*Reportado por Francisco Miguel Biete Banon.*)

**Mejoras en la documentación:**

- Añadir un enlace a la configuración de PostgreSQL en la sección del host del repositorio. (*Revisado por Stefan Fercot. Sugerido por Julien Cigar.*)

**Mejoras en la suite de pruebas:**

- Añadir compilación experimental con Meson. (*Revisado por Eli Schwartz, Sam Bassaly.*)
- Permitir pasar cualquier ruta a la opción `--test-path`. (*Contribución de Andrey Sokolov. Revisado por David Steele.*)
- Corregir un error de compilación cuando `DEBUG_EXEC_TIME` se define sin `DEBUG`. (*Contribución de Andrey Sokolov. Revisado por David Steele.*)


### Notas de la versión v2.39 {#v239-release-notes}

*Verify y agrupamiento de archivos*

*Publicada el 16 de mayo de 2022*

**Correcciones de errores:**

- Corregir un error lanzado desde `FINALLY()` que causaba un bucle infinito. (*Revisado por Stephen Frost.*)
- Generar error en todos los fallos de bloqueo excepto cuando otro proceso mantiene el bloqueo. (*Revisado por Reid Thompson, Geir Råness. Reportado por Geir Råness.*)

**Funcionalidades:**

- Agrupamiento de archivos de la copia de seguridad para mejorar el soporte de archivos pequeños. (*Revisado por Reid Thompson, Stefan Fercot, Chris Bandy.*)
- Comando verify para validar el contenido de un repositorio. (*Contribución de Cynthia Shang, Reid Thompson. Revisado por David Steele, Stefan Fercot.*)
- Soporte de PostgreSQL 15. (*Revisado por Stefan Fercot.*)
- Mostrar el porcentaje completado de la copia de seguridad en la salida de `info`. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Autoselección de la copia de seguridad para el comando `restore` con `--type=lsn`. (*Contribución de Reid Thompson. Revisado por Stefan Fercot, David Steele.*)
- Suprimir la advertencia de WAL existente cuando `archive-mode-check` está deshabilitado. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Añadir soporte de AWS IMDSv2. (*Contribución de Nuno Pires. Revisado por David Steele.*)

**Mejoras:**

- Permitir cambiar la opción `repo-hardlink` después de una copia de seguridad completa. (*Revisado por Reid Thompson.*)
- Aumentar la precisión del registro de porcentaje completado para `backup` y `restore`. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Mejorar la validación de rutas para los comandos `repo-*`. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Mejorar el comando `stop` para que respete la opción `stanza`. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por ragaoua.*)
- Mejorar el mensaje de error para `repo-azure-key` inválido. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Seth Daniel.*)
- Añadir una sugerencia para revisar el registro ante un error asincrónico de `archive-get`/`archive-push`. (*Revisado por Reid Thompson.*)
- Añadir `ClockError` para desfases de reloj y cambios de zona horaria inesperados. (*Revisado por Greg Sabino Mullane, Stefan Fercot. Sugerido por Greg Sabino Mullane.*)
- Quitar las extensiones del manifiesto de historial antes de mostrarlo en un mensaje de error. (*Revisado por Stefan Fercot.*)
- Añadir usuario:grupo al error de permisos de bloqueo. (*Revisado por Reid Thompson.*)

**Correcciones de errores en la documentación:**

- Corregir una referencia incorrecta a `stanza-update` en la guía de usuario. (*Corregido por Abubakar Mohammed. Revisado por David Steele.*)
- Corregir el ejemplo de la opción `repo-gcs-key-type` en la referencia de configuración. (*Revisado por Reid Thompson.*)
- Corregir el ejemplo de `tls-server-auth` y añadir aclaraciones. (*Revisado por Reid Thompson.*)

**Mejoras en la documentación:**

- Simplificar los mensajes sobre las versiones soportadas en la documentación. (*Revisado por Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)
- Añadir descripciones de tipo de opción. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Añadir una pregunta frecuente sobre los tipos de copia de seguridad y la velocidad de restauración. (*Contribución de David Christensen. Revisado por Reid Thompson.*)
- Documentar la rama base requerida para los pull requests. (*Contribución de David Christensen. Revisado por Reid Thompson.*)


### Notas de la versión v2.38 {#v238-release-notes}

*Correcciones y mejoras menores*

*Publicada el 6 de marzo de 2022*

**NOTA IMPORTANTE**: El tamaño del repositorio reportado por el comando `info` ahora se basa enteramente en lo que pgBackRest ha escrito en el almacenamiento. Anteriormente, en ciertos casos, pgBackRest podía detectar si el almacenamiento aplicaba compresión adicional, pero esto ya no está soportado.

**Correcciones de errores:**

- Reintentar errores en la eliminación por lotes de archivos en S3. (*Revisado por Reid Thompson. Reportado por Alex Richman.*)
- Permitir la coincidencia sin distinción entre mayúsculas y minúsculas de los valores del encabezado HTTP `connection`. (*Revisado por Reid Thompson. Reportado por Rémi Vidier.*)

**Funcionalidades:**

- Añadir soporte para el cifrado del lado del servidor de AWS S3 con KMS. (*Contribución de Christoph Berg. Revisado por David Steele, Tharindu Amila.*)
- Añadir la opción `archive-missing-retry`. (*Revisado por Stefan Fercot.*)
- Añadir un filtro por tipo de copia de seguridad al comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

**Mejoras:**

- Reintentar ante un fallo de validación de páginas durante `backup`. (*Revisado por Stephen Frost, David Christensen.*)
- Manejar servidores TLS que no cierran las conexiones de forma limpia. (*Revisado por Rémi Vidier, David Christensen, Stephen Frost.*)
- Añadir los LSN de la copia de seguridad a la salida del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Quitar automáticamente las barras finales de las rutas de `repo-ls`. (*Contribución de David Christensen. Revisado por David Steele.*)
- No reintentar errores fatales. (*Revisado por Reid Thompson.*)
- Eliminar el soporte de PostgreSQL `8.3`/`8.4`. (*Revisado por Reid Thompson, Stefan Fercot.*)
- Eliminar la lógica que intentaba determinar compresión adicional del sistema de archivos. (*Revisado por Reid Thompson, Stefan Fercot.*)

**Correcciones de errores en la documentación:**

- Mover las opciones `repo` de la documentación de TLS a la sección `global`. (*Reportado por Anton Kurochkin.*)
- Eliminar la opción `backup-standby` sin uso de los comandos de stanza. (*Reportado por Stefan Fercot.*)
- Corregir erratas en la ayuda y las notas de versión. (*Corregido por Daniel Gustafsson. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Añadir una comprobación de vitalidad a la configuración del servicio systemd. (*Sugerido por Yogesh Sharma.*)
- Añadir una pregunta frecuente que explica el sufijo del archivado de WAL. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Señalar que los slots de replicación no se restauran. (*Contribución de Reid Thompson. Revisado por David Steele, Stefan Fercot. Sugerido por Christophe Courtois.*)


### Notas de la versión v2.37 {#v237-release-notes}

*Servidor TLS*

*Publicada el 3 de enero de 2022*

**NOTA IMPORTANTE**: Si el comando `restore` no puede encontrar una copia de seguridad que coincida con un tiempo objetivo especificado, se lanzará un error, mientras que antes se registraba una advertencia.

**Correcciones de errores:**

- Corregir el mapeo de enlaces delta de `restore` cuando la ruta/el archivo ya existe. (*Revisado por Reid Thompson. Reportado por Younes Alhroub.*)
- Corregir una fuga de sockets en los reintentos de conexión. (*Revisado por Reid Thompson. Reportado por James Coleman.*)

**Funcionalidades:**

- Añadir un servidor TLS. (*Revisado por Stephen Frost, Reid Thompson, Andrew L'Ecuyer.*)
- Añadir la opción `--cmd`. (*Contribución de Reid Thompson. Revisado por Stefan Fercot, David Steele. Sugerido por Virgile CREVON.*)

**Mejoras:**

- Comprobar el archivado inmediatamente después de iniciar la copia de seguridad. (*Revisado por Reid Thompson, David Christensen.*)
- Añadir comprobaciones de línea de tiempo y de checkpoint a la copia de seguridad. (*Revisado por Stefan Fercot, Reid Thompson.*)
- Comprobar que los clústeres están vivos y correctamente configurados durante una copia de seguridad. (*Revisado por Stefan Fercot.*)
- Generar un error cuando `restore` no puede encontrar una copia de seguridad que coincida con el tiempo objetivo. (*Revisado por Reid Thompson, Douglas J Hunley. Sugerido por Douglas J Hunley.*)
- Analizar protocolo/puerto en los endpoints de S3/Azure. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Añadir una advertencia cuando checkpoint_timeout excede `db-timeout`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Añadir el verbo a la salida de errores HTTP. (*Contribución de Christoph Berg. Revisado por David Steele.*)
- Permitir argumentos y/n para opciones booleanas de línea de comandos. (*Contribución de Reid Thompson. Revisado por David Steele.*)
- Hacer que el registro del tamaño de la copia de seguridad coincida exactamente con la salida del comando `info`. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Mahomed Hussein.*)

**Mejoras en la documentación:**

- Mostrar los valores por defecto y permitidos de las opciones de tamaño con las unidades apropiadas. (*Revisado por Reid Thompson.*)
- Corregir erratas y mejorar la documentación de la opción `tablespace-map-all`. (*Revisado por Reid Thompson. Sugerido por Reid Thompson.*)
- Eliminar una afirmación obsoleta sobre el futuro soporte de múltiples repositorios. (*Sugerido por David Christensen.*)


### Notas de la versión v2.36 {#v236-release-notes}

*Correcciones y mejoras menores*

*Publicada el 1 de noviembre de 2021*

**Correcciones de errores:**

- Permitir «global» como prefijo de stanza. (*Revisado por Stefan Fercot. Reportado por Younes Alhroub.*)
- Corregir un segfault con un archivo de clave GCS inválido. (*Revisado por Stephen Frost. Reportado por Henrik Feldt.*)

**Mejoras:**

- Permitir que la opción `link-map` cree enlaces nuevos. (*Revisado por Don Seiler, Stefan Fercot, Chris Bandy. Sugerido por Don Seiler.*)
- Aumentar a 256 el índice máximo permitido para las opciones `pg`/`repo`. (*Revisado por Cynthia Shang.*)
- Añadir autenticación `WebIdentity` para AWS S3. (*Revisado por James Callahan, Reid Thompson, Benjamin Blattberg, Andrew L'Ecuyer.*)
- Reportar los errores de validación de archivos de la copia de seguridad en `backup.info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Añadir la hora de inicio de la recuperación al registro de restauración de copias de seguridad en línea. (*Revisado por Tom Swartz, Stefan Fercot. Sugerido por Tom Swartz.*)
- Reportar el error original y los reintentos ante un fallo de un trabajo local. (*Revisado por Stefan Fercot.*)
- Renombrar «page checksum error» a «error list» en la salida de texto de info. (*Revisado por Stefan Fercot.*)
- Añadir sugerencias al mensaje de tiempo de espera agotado de la reproducción de la réplica. (*Revisado por Cynthia Shang, Stefan Fercot. Sugerido por Leigh Downs.*)


### Notas de la versión v2.35 {#v235-release-notes}

*Protocolo binario*

*Publicada el 23 de agosto de 2021*

**NOTA IMPORTANTE**: El nivel de registro para los archivos copiados en los comandos `backup`/`restore` se ha cambiado a `detail`. Esto hace que el nivel de registro `info` sea menos ruidoso, pero si estos mensajes son necesarios, establece el nivel de registro de los comandos `backup`/`restore` en `detail`

**Correcciones de errores:**

- Detectar errores en la finalización de subidas multiparte de S3. (*Revisado por Cynthia Shang, Marco Montagna. Reportado por Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)
- Corregir la detección de enlaces simbólicos circulares. (*Revisado por Stefan Fercot. Reportado por Rohit Raveendran.*)
- Pasar al remoto solo las opciones `repo` seleccionadas. (*Revisado por David Christensen, Cynthia Shang. Reportado por Greg Sabino Mullane, David Christensen.*)

**Mejoras:**

- Protocolo binario. (*Revisado por Cynthia Shang.*)
- Crear automáticamente el directorio de datos en `restore`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Chris Bandy.*)
- Permitir `restore` `--type=lsn`. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang. Sugerido por James Coleman.*)
- Cambiar a detail el nivel de registro de archivos copiados de `backup`/`restore`. (*Revisado por Stefan Fercot. Sugerido por Jens Wilke.*)
- Iterar mientras se espera que el LSN del checkpoint alcance el LSN de reproducción. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Fatih Mencutekin.*)
- Registrar el total de archivos de `backup` y el total de tamaño/archivos de `restore`. (*Revisado por Cynthia Shang.*)

**Correcciones de errores en la documentación:**

- Corregir nombres de host incorrectos en la guía de usuario. (*Revisado por Stefan Fercot. Reportado por Greg Sabino Mullane.*)

**Mejoras en la documentación:**

- Actualizar la documentación de contribución y añadir una plantilla de pull request. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Reordenar la documentación de copias de seguridad en la guía de usuario. (*Revisado por Cynthia Shang.*)
- Aclarar el comportamiento de `--type` de `restore` en la referencia de comandos. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Corregir erratas en la documentación y los comentarios. (*Contribución de Eric Radman. Revisado por David Steele.*)

**Mejoras en la suite de pruebas:**

- Añadir una comprobación de que la ruta de pruebas esté dentro de la ruta del repositorio. (*Revisado por Greg Sabino Mullane. Sugerido por Greg Sabino Mullane.*)
- Añadir análisis de código estático con CodeQL. (*Revisado por Cynthia Shang.*)
- Actualizar las pruebas para usar patrones estándar. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.34 {#v234-release-notes}

*Soporte de PostgreSQL 14*

*Publicada el 7 de junio de 2021*

**Correcciones de errores:**

- Corregir problemas con archivos de spool remanentes de un `restore` anterior. (*Revisado por Cynthia Shang, Stefan Fercot, Floris van Nee. Reportado por Floris van Nee.*)
- Corregir un problema al comprobar enlaces con grandes cantidades de tablespaces. (*Revisado por Cynthia Shang, Avinash Vallarapu. Reportado por Avinash Vallarapu.*)
- Liberar los remotos que ya no se necesitan para que no agoten su tiempo de espera durante `restore`. (*Revisado por Cynthia Shang. Reportado por Francisco Miguel Biete Banon.*)
- Corregir `help` cuando una opción válida es inválida para el comando especificado. (*Revisado por Stefan Fercot. Reportado por Cynthia Shang.*)

**Funcionalidades:**

- Añadir soporte de PostgreSQL 14. (*Revisado por Cynthia Shang.*)
- Añadir autenticación automática de GCS para instancias de GCE. (*Revisado por Jan Wieck, Daniel Farina.*)
- Añadir la opción `repo-retention-history` para expirar el historial de copias de seguridad. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang, David Steele.*)
- Añadir la opción `db-exclude`. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang.*)

**Mejoras:**

- Cambiar el registro de la expiración del archivado del nivel detail al nivel info. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Eliminar la ruta de spool del archivado de la stanza en `restore`. (*Revisado por Cynthia Shang, Stefan Fercot.*)
- No escribir archivos atómicamente ni sincronizar rutas durante la copia de `backup`. (*Revisado por Stephen Frost, Stefan Fercot, Cynthia Shang.*)

**Mejoras en la documentación:**

- Actualizar la documentación de contribución. (*Contribución de Cynthia Shang. Revisado por David Steele, Stefan Fercot.*)
- Consolidar la guía de usuario de RHEL/CentOS en un único documento. (*Revisado por Cynthia Shang.*)
- Aclarar que `repo-s3-role` no es un `ARN`. (*Contribución de Isaac Yuen. Revisado por David Steele.*)


### Notas de la versión v2.33 {#v233-release-notes}

*Soporte de múltiples repositorios y de GCS*

*Publicada el 5 de abril de 2021*

**Correcciones de errores:**

- Corregir advertencias de opciones que rompían `archive-get`/`archive-push` asincrónicos. (*Revisado por Cynthia Shang. Reportado por Lev Kokotov.*)
- Corregir una fuga de memoria en la copia de seguridad durante la copia del archivado. (*Revisado por Cynthia Shang. Reportado por Christian ROUX, Efremov Egor.*)
- Corregir un desbordamiento de pila en la generación de frases de contraseña de cifrado. (*Revisado por Cynthia Shang. Reportado por bsiara.*)
- Corregir `repo-ls` `/` en repositorios S3. (*Revisado por Cynthia Shang. Reportado por Lesovsky Alexey.*)

**Funcionalidades:**

- Soporte de múltiples repositorios. (*Contribución de Cynthia Shang, David Steele. Revisado por Stefan Fercot, Stephen Frost.*)
- Soporte de GCS para el almacenamiento del repositorio. (*Revisado por Cynthia Shang, Daniel Farina.*)
- Añadir la opción `archive-header-check`. (*Revisado por Stephen Frost, Cynthia Shang. Sugerido por Hans-Jürgen Schönig.*)

**Mejoras:**

- Incluir las bases de datos del sistema recreadas durante la restauración selectiva. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang.*)
- Excluir `content-length` de los encabezados firmados de S3. (*Revisado por Cynthia Shang. Sugerido por Brian P Bockelman.*)
- Consolidar las opciones de almacenamiento del repositorio menos utilizadas. (*Revisado por Cynthia Shang.*)
- Permitir un valor por defecto personalizado de `config-path` con `./configure --with-configdir`. (*Contribución de Michael Schout. Revisado por David Steele.*)
- Registrar la copia del archivado durante `backup`. (*Revisado por Cynthia Shang, Stefan Fercot.*)

**Mejoras en la documentación:**

- Actualizar la referencia para incluir enlaces a los ejemplos de la guía de usuario. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Actualizar la documentación de restauración selectiva con advertencias. (*Revisado por Cynthia Shang, Stefan Fercot.*)
- Añadir una aclaración de `compress-type` a la documentación de `archive-copy`. (*Revisado por Cynthia Shang, Stefan Fercot.*)
- Añadir los valores por defecto de `compress-level` según el valor de `compress-type`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadir una nota sobre que los ajustes de NFS requeridos son los mismos que los de PostgreSQL. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.32 {#v232-release-notes}

*Comandos de repositorio*

*Publicada el 8 de febrero de 2021*

**Correcciones de errores:**

- Corregir la reanudación tras la eliminación parcial de una copia de seguridad por una reanudación anterior. (*Revisado por Cynthia Shang. Reportado por Tom Swartz.*)

**Funcionalidades:**

- Añadir el comando `repo-ls`. (*Revisado por Cynthia Shang, Stefan Fercot.*)
- Añadir el comando `repo-get`. (*Contribución de Stefan Fercot, David Steele. Revisado por Cynthia Shang.*)
- Añadir la opción `archive-mode-check`. (*Contribución de Stefan Fercot. Revisado por David Steele, Michael Banck.*)

**Mejoras:**

- Mejorar el rendimiento de `archive-get`. (*Revisado por Cynthia Shang.*)

**Mejoras en la documentación:**

- Mejorar la documentación del comando `expire`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.31 {#v231-release-notes}

*Correcciones y mejoras menores*

*Publicada el 7 de diciembre de 2020*

**Correcciones de errores:**

- Permitir `[`, `#` y `space` como primer carácter en los nombres de las bases de datos. (*Revisado por Stefan Fercot, Cynthia Shang. Reportado por Jefferson Alexandre.*)
- Crear `standby.signal` solo en PostgreSQL 12 cuando el tipo de `restore` es `standby`. (*Corregido por Stefan Fercot. Revisado por David Steele. Reportado por Keith Fiske.*)

**Funcionalidades:**

- Expirar los archivos de historial. (*Contribución de Stefan Fercot. Revisado por David Steele.*)
- Reportar errores de suma de verificación de páginas en la salida `text` del comando `info`. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang.*)
- Añadir la opción `repo-azure-endpoint`. (*Revisado por Cynthia Shang, Brian Peterson. Sugerido por Brian Peterson.*)
- Añadir la opción `pg-database`. (*Revisado por Cynthia Shang.*)

**Mejoras:**

- Mejorar la salida del comando `info` cuando se especifica una stanza que no existe. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang, David Steele. Sugerido por uspen.*)
- Mejorar el rendimiento de las listas extensas de archivos en los comandos `backup`/`restore`. (*Revisado por Cynthia Shang, Oscar.*)
- Añadir reintentos a la espera de PostgreSQL al iniciar una copia de seguridad. (*Revisado por Cynthia Shang. Sugerido por Vitaliy Kukharik.*)

**Mejoras en la documentación:**

- Reemplazar la documentación de RHEL/CentOS 6 por la de RHEL/CentOS 8.


### Notas de la versión v2.30 {#v230-release-notes}

*Soporte de PostgreSQL 13*

*Publicada el 5 de octubre de 2020*

**Correcciones de errores:**

- Generar un error con sugerencias cuando el usuario de la copia de seguridad no puede leer `pg_settings`. (*Revisado por Stefan Fercot, Cynthia Shang. Reportado por Mohamed Insaf K.*)

**Funcionalidades:**

- Soporte de PostgreSQL 13. (*Revisado por Cynthia Shang.*)

**Mejoras:**

- Mejorar la identificación de la versión de PostgreSQL. (*Revisado por Cynthia Shang, Stephen Frost.*)
- Mejorar el mensaje de error del directorio de trabajo. (*Revisado por Stefan Fercot.*)
- Añadir una sugerencia sobre iniciar la stanza cuando no se encuentra un segmento WAL. (*Contribución de David Christensen. Revisado por David Steele.*)
- Añadir una sugerencia para la discrepancia de versión del protocolo. (*Revisado por Cynthia Shang. Sugerido por loop-evgeny.*)

**Mejoras en la documentación:**

- Añadir una nota de que las versiones de pgBackRest deben coincidir cuando se ejecutan de forma remota. (*Revisado por Cynthia Shang. Sugerido por loop-evgeny.*)
- Mover el texto del comando info a la referencia y enlazar a la guía de usuario. (*Revisado por Cynthia Shang. Sugerido por Christophe Courtois.*)
- Actualizar la ruta del repositorio yum para la guía de usuario de CentOS/RHEL. (*Contribución de Heath Lord. Revisado por David Steele.*)


### Notas de la versión v2.29 {#v229-release-notes}

*Credenciales S3 automáticas en AWS*

*Publicada el 31 de agosto de 2020*

**Correcciones de errores:**

- Suprimir los errores al cerrar los procesos `local`/`remote`. Dado que el comando ha finalizado, es contraproducente lanzar un error, pero aun así se **advierte** para indicar que ocurrió algo inusual. (*Revisado por Cynthia Shang. Reportado por argdenis.*)
- Corregir un problema con el carácter `=` en nombres de archivos o bases de datos. (*Revisado por Bastian Wegge, Cynthia Shang. Reportado por Brad Nicholson, Bastian Wegge.*)

**Funcionalidades:**

- Obtener automáticamente credenciales S3 temporales en instancias de AWS. (*Contribución de David Steele, Stephen Frost. Revisado por Cynthia Shang, David Youatt, Aleš Zelený, Jeanette Bromage.*)
- Añadir la opción `archive-mode` para deshabilitar el archivado en la restauración. (*Revisado por Stephen Frost. Sugerido por Stephen Frost.*)

**Mejoras:**

- Soporte de PostgreSQL 13 beta3. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.
- `list`/`remove` asincrónicos para el almacenamiento S3/Azure. (*Revisado por Cynthia Shang, Stephen Frost.*)
- Mejorar el uso de memoria de la detección de relaciones unlogged en la construcción del manifiesto. (*Revisado por Cynthia Shang, Stephen Frost, Brad Nicholson, Oscar. Sugerido por Oscar, Brad Nicholson.*)
- Cerrar proactivamente los descriptores de archivo tras bifurcar el proceso asincrónico. (*Revisado por Stephen Frost, Cynthia Shang.*)
- Retrasar el cierre de la conexión remota de la copia de seguridad hasta después de la comprobación del archivado. (*Contribución de Floris van Nee. Revisado por David Steele.*)
- Mejorar la salida de error detallada. (*Revisado por Cynthia Shang.*)
- Mejorar el reporte de errores de TLS. (*Revisado por Cynthia Shang, Stephen Frost.*)

**Correcciones de errores en la documentación:**

- Añadir `none` a la referencia de la opción `compress-type` y corregir el ejemplo. (*Reportado por Ugo Bellavance, Don Seiler.*)
- Añadir el tipo `azure` faltante en la referencia de la opción `repo-type`. (*Corregido por Don Seiler. Revisado por David Steele.*)
- Corregir una errata en la referencia de la opción `repo-cipher-type`. (*Corregido por Don Seiler. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Aclarar que `expire` debe ejecutarse regularmente cuando `expire-auto` está deshabilitado. (*Revisado por Douglas J Hunley. Sugerido por Douglas J Hunley.*)


### Notas de la versión v2.28 {#v228-release-notes}

*Almacenamiento de repositorio en Azure*

*Publicada el 20 de julio de 2020*

**Correcciones de errores:**

- Corregir que `restore` `--force` se comportara como `--force --delta`. Esto hacía que `restore` reemplazara archivos según marca de tiempo y tamaño en lugar de sobrescribirlos, lo que significaba que algunos archivos que debían haberse actualizado quedaban sin cambios. `restore` normal y `restore` `--delta` no estaban afectados por este problema. (*Revisado por Cynthia Shang.*)

**Funcionalidades:**

- Soporte de Azure para el almacenamiento del repositorio. (*Revisado por Cynthia Shang, Don Seiler.*)
- Añadir la opción `expire-auto`. Esto permite deshabilitar la expiración automática después de una copia de seguridad exitosa. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang, David Steele.*)

**Mejoras:**

- Subida multiparte asincrónica de S3. (*Revisado por Stephen Frost.*)
- Reintento automático para `backup`, `restore`, `archive-get` y `archive-push`. (*Revisado por Cynthia Shang.*)
- Deshabilitar el paralelismo de consultas en las sesiones de PostgreSQL usadas para el control de la copia de seguridad. (*Revisado por Stefan Fercot.*)
- Soporte de PostgreSQL 13 beta2. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.
- Mejorar el manejo de estados de respuesta HTTP inválidos. (*Revisado por Cynthia Shang.*)
- Mejorar el error cuando falta la opción `pg1-path` para el comando `archive-get`. (*Revisado por Cynthia Shang.*)
- Añadir una sugerencia cuando el delta de suma de verificación se habilita después de un cambio de línea de tiempo. (*Revisado por Matt Bunter, Cynthia Shang.*)
- Usar PostgreSQL en lugar de `postmaster` donde corresponda. (*Revisado por Cynthia Shang.*)

**Correcciones de errores en la documentación:**

- Corregir un ejemplo incorrecto de la opción `repo-retention-full-type`. (*Reportado por Höseyin Sönmez.*)
- Eliminar los comandos internos de las referencias de comandos HTML y de manual. (*Reportado por Cynthia Shang.*)

**Mejoras en la documentación:**

- Actualizar las versiones de PostgreSQL usadas para construir las guías de usuario. También se añaden rangos de versiones para indicar que una guía de usuario es precisa para un rango de versiones de PostgreSQL aunque se haya construido para una versión específica. (*Revisado por Stephen Frost.*)
- Actualizar la pregunta frecuente sobre cómo expirar un conjunto de copias de seguridad específico. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Actualizar la pregunta frecuente para aclarar el comportamiento predeterminado de PITR. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.27 {#v227-release-notes}

*Mejoras de expiración y controladores de compresión*

*Publicada el 26 de mayo de 2020*

**Correcciones de errores:**

- Corregir un problema al comprobar si los enlaces de archivos están contenidos en los enlaces de rutas. (*Revisado por Cynthia Shang. Reportado por Christophe Cavallié.*)
- Permitir que `pg-path1` sea opcional para `archive-push` sincrónico. (*Revisado por Cynthia Shang. Reportado por Jerome Peng.*)
- El comando `expire` ahora comprueba si hay un archivo de parada. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Manejar la frase de razón faltante en respuestas HTTP. (*Revisado por Cynthia Shang. Reportado por Tenuun.*)
- Aumentar el tamaño del búfer para el vaciado de la compresión lz4. (*Revisado por Cynthia Shang. Reportado por Eric Radman.*)
- Ignorar las opciones `pg-host*` y `repo-host*` para el comando `remote`. (*Revisado por Cynthia Shang. Reportado por Pavel Suderevsky.*)
- Corregir opciones `pg1-*` posiblemente faltantes para el comando `remote`. (*Revisado por Cynthia Shang. Reportado por Andrew L'Ecuyer.*)

**Funcionalidades:**

- Retención basada en tiempo para copias de seguridad completas. La opción `--repo-retention-full-type` permite la retención de copias de seguridad completas con base en un período de tiempo, especificado en días. (*Contribución de Cynthia Shang, Pierre Ducroquet. Revisado por David Steele.*)
- Expiración ad hoc de copias de seguridad. Permite al usuario eliminar una copia de seguridad especificada sin importar la configuración de retención. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Soporte de compresión Zstandard. Ten en cuenta que establecer `compress-type=zst` hará que las nuevas copias de seguridad y el archivado sean incompatibles (irrestaurables) con versiones anteriores de pgBackRest. (*Revisado por Cynthia Shang.*)
- Soporte de compresión bzip2. Ten en cuenta que establecer `compress-type=bz2` hará que las nuevas copias de seguridad y el archivado sean incompatibles (irrestaurables) con versiones anteriores de pgBackRest. (*Contribución de Stephen Frost. Revisado por David Steele, Cynthia Shang.*)
- Añadir el estado de ejecución de `backup`/`expire` al comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

**Mejoras:**

- Expirar el archivado de WAL solo cuando se cumple el umbral de `repo-retention-archive`. El WAL anterior a la primera copia de seguridad completa previamente se expiraba después de la primera copia completa. Ahora se preserva según la configuración de retención. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadir una implementación local de MD5 para que S3 funcione cuando FIPS está habilitado. (*Revisado por Cynthia Shang, Stephen Frost. Sugerido por Brian Almeida, John Kelly.*)
- Soporte de PostgreSQL 13 beta1. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo. (*Revisado por Cynthia Shang.*)
- Reducir el valor por defecto de `buffer-size` a `1MiB`. (*Revisado por Stephen Frost.*)
- Lanzar un error amigable si `expire` no se ejecuta en el host del repositorio. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.26 {#v226-release-notes}

*TLS no bloqueante*

*Publicada el 20 de abril de 2020*

**Correcciones de errores:**

- Eliminar la subexpresión vacía de la expresión regular del manifiesto. MacOS no estaba conforme con esto, aunque otras plataformas parecían funcionar bien. (*Corregido por David Raftis. Revisado por David Steele.*)

**Mejoras:**

- Implementación de TLS no bloqueante. (*Revisado por Slava Moudry, Cynthia Shang, Stephen Frost.*)
- Limitar el tamaño de copia de la copia de seguridad solo para archivos registrados en WAL. El comportamiento anterior podía llevar a que `postgresql.conf` o `postgresql.auto.conf` quedaran truncados en la copia de seguridad. (*Revisado por Cynthia Shang.*)
- Las opciones keep-alive de TCP son configurables. (*Sugerido por Marc Cousin.*)
- Añadir la opción `io-timeout`. (*Revisado por Cynthia Shang.*)


### Notas de la versión v2.25 {#v225-release-notes}

*Soporte de compresión LZ4*

*Publicada el 26 de marzo de 2020*

**Funcionalidades:**

- Añadir soporte de compresión lz4. Ten en cuenta que establecer `compress-type=lz4` hará que las nuevas copias de seguridad y el archivado sean incompatibles (irrestaurables) con versiones anteriores de pgBackRest. (*Revisado por Cynthia Shang.*)
- Añadir la opción `--dry-run` al comando `expire`. Usa dry-run para ver qué copias de seguridad/archivado eliminaría el comando `expire` sin eliminar nada realmente. (*Contribución de Cynthia Shang, Luca Ferrari. Revisado por David Steele. Sugerido por Marc Cousin.*)

**Mejoras:**

- Mejorar el rendimiento de la construcción remota del manifiesto. (*Sugerido por Jens Wilke.*)
- Corregir la detección de las opciones de keepalive en Linux. (*Contribución de Marc Cousin. Revisado por David Steele.*)
- Añadir la detección de host a configure para establecer correctamente las banderas de estándares. (*Contribución de Marc Cousin. Revisado por David Steele.*)
- Eliminar las opciones `compress`/`compress-level` de los comandos donde no se usan. Estos comandos (p. ej. `restore`, `archive-get`) nunca usaron las opciones de compresión pero permitían pasarlas en la línea de comandos. Ahora darán error cuando estas opciones se pasen en la línea de comandos. Si ocurren estos errores, elimina las opciones sin uso. (*Revisado por Cynthia Shang.*)
- Limitar el tamaño de copia de los archivos de la copia de seguridad al tamaño reportado al inicio de la copia. Si un archivo crece durante la copia de seguridad, será reconstruido por la reproducción de WAL durante la recuperación, de modo que no es necesario copiar los datos adicionales. (*Revisado por Cynthia Shang.*)


### Notas de la versión v2.24 {#v224-release-notes}

*Autoselección del conjunto de copias de seguridad para un tiempo objetivo*

*Publicada el 25 de febrero de 2020*

**Correcciones de errores:**

- Evitar procesos zombi en los comandos de archivado asincrónicos. (*Revisado por Stephen Frost. Reportado por Adam Brusselback, ejberdecia.*)
- Generar un error cuando `archive-get`/`archive-push`/`restore` no se ejecutan en un host de PostgreSQL. (*Revisado por Stephen Frost. Reportado por Jesper St John.*)
- Leer el contenido HTTP hasta eof cuando no se especifica tamaño/codificación. (*Revisado por Cynthia Shang. Reportado por Christian ROUX.*)
- Corregir la reanudación cuando la copia de seguridad reanudable fue creada por Perl. En este caso la copia reanudable debería ignorarse, pero el código en C no podía cargar el manifiesto parcial escrito por Perl porque el formato difiere ligeramente. Se añaden validaciones para detectar este caso y continuar de forma limpia. (*Reportado por Kacey Holston.*)

**Funcionalidades:**

- Autoseleccionar el conjunto de copias de seguridad en la restauración cuando se especifica un tiempo objetivo. La autoselección se realiza solo cuando no se especifica `--set`. Si no se puede encontrar un conjunto de copias de seguridad para el tiempo objetivo dado, se usará el conjunto más reciente (predeterminado). (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras:**

- Omitir el archivo temporal `pg_internal.init` durante la copia de seguridad. (*Revisado por Cynthia Shang. Sugerido por Michael Paquier.*)
- Añadir más validaciones al manifiesto en `backup`. (*Revisado por Cynthia Shang.*)

**Mejoras en la documentación:**

- Impedir que lock-bot añada comentarios a los issues bloqueados. (*Sugerido por Christoph Berg.*)


### Notas de la versión v2.23 {#v223-release-notes}

*Corrección de error*

*Publicada el 27 de enero de 2020*

**Correcciones de errores:**

- Corregir archivos faltantes que corrompían el manifiesto. Si PostgreSQL eliminaba un archivo durante la copia de seguridad (o faltaba en la réplica), el siguiente archivo podía no copiarse ni actualizarse en el manifiesto. Si esto ocurría, la copia de seguridad daba error al restaurarse. (*Revisado por Cynthia Shang. Reportado por Vitaliy Kukharik.*)

**Mejoras:**

- Usar `pkg-config` en lugar de `xml2-config` para las opciones de compilación de libxml2. (*Contribución de David Steele, Adrian Vondendriesch.*)
- Validar que las sumas de verificación estén establecidas en el manifiesto en `backup`/`restore`. (*Revisado por Cynthia Shang.*)


### Notas de la versión v2.22 {#v222-release-notes}

*Corrección de error*

*Publicada el 21 de enero de 2020*

**Correcciones de errores:**

- Corregir un error en la conversión de línea de tiempo. La línea de tiempo es necesaria para verificar los segmentos WAL en el archivado después de una copia de seguridad. La conversión se realizaba en base `10` en lugar de `16`, lo que provocaba errores cuando la línea de tiempo era ≥ `0xA`. (*Reportado por Lukas Ertl, Eric Veldhuyzen.*)


### Notas de la versión v2.21 {#v221-release-notes}

*Migración a C completada*

*Publicada el 15 de enero de 2020*

**Correcciones de errores:**

- Corregir opciones que eran ignoradas por los comandos asincrónicos. Los procesos `archive-get`/`archive-push` asincrónicos no cargaban las opciones configuradas en las secciones de configuración de comandos, p. ej. `[global:archive-get]`. (*Revisado por Cynthia Shang. Reportado por Urs Kramer.*)
- Corregir el manejo de `\` en los nombres de archivo. `\` no se estaba escapando correctamente al calcular la suma de verificación del manifiesto, lo que impedía cargar el manifiesto. Dado que las apariciones de `\` en nombres de archivos del clúster deberían ser raras o inexistentes, esto no parece ser un problema grave en el mundo real.

**Funcionalidades:**

- pgBackRest ahora es C puro.
- Añadir la opción `pg-user`. Especifica el nombre de usuario de la base de datos al conectarse a PostgreSQL. Si no se especifica, pgBackRest se conectará con el usuario local del SO o `PGUSER`, que era el comportamiento anterior. (*Contribución de Mike Palmiotto. Revisado por David Steele.*)
- Permitir URI con estilo de ruta en el controlador S3.

**Mejoras:**

- El comando `backup` está implementado enteramente en C. (*Revisado por Cynthia Shang.*)


### Notas de la versión v2.20 {#v220-release-notes}

*Correcciones de errores*

*Publicada el 12 de diciembre de 2019*

**Correcciones de errores:**

- Corregir archive-push/archive-get cuando `PGDATA` es un enlace simbólico. Estos comandos intentaban usar `cwd()` como `PGDATA`, pero esto podía no coincidir con la ruta configurada en pgBackRest si `PGDATA` era un enlace simbólico. Si `cwd()` no coincide con la ruta de pgBackRest, entonces se hace `chdir()` a la ruta y se comprueba que el siguiente `cwd()` coincida con el resultado de la primera llamada. (*Reportado por Stephen Frost, Milosz Suchy.*)
- Corregir la lista de referencias cuando `backup.info` se reconstruye en el comando `expire`. Dado que el comando `backup` todavía usa la versión Perl de la reconstrucción, este problema no se manifestará a menos que **1)** falte una copia de seguridad en `backup.info` y **2)** el comando `expire` se ejecute directamente en lugar de ejecutarse después de `backup` como es habitual. Esta improbable combinación de eventos hace que probablemente no sea un problema en el mundo real.
- Corregir un segfault ante un EOF inesperado en la descompresión gzip. (*Reportado por Stephen Frost.*)


### Notas de la versión v2.19 {#v219-release-notes}

*Migraciones a C y correcciones de errores*

*Publicada el 12 de noviembre de 2019*

**Correcciones de errores:**

- Corregir el tiempo de espera agotado del remoto en la restauración delta. Al realizar una restauración delta en un clúster prácticamente sin cambios, el remoto podía agotar su tiempo de espera si no se recuperaban archivos del repositorio dentro de `protocol-timeout`. Se añaden keep-alives para evitar el tiempo de espera agotado del remoto. (*Reportado por James Sewell, Jens Wilke.*)
- Corregir el manejo de encabezados HTTP repetidos. Cuando los encabezados HTTP se repiten, deberían considerarse equivalentes a un único encabezado separado por comas en lugar de generar un error, que era el comportamiento anterior. (*Reportado por donicrosby.*)

**Mejoras:**

- La salida JSON del comando `info` ya no se imprime con formato. Los sistemas de monitoreo pueden ingerir el JSON más fácilmente sin saltos de línea. Herramientas externas como `jq` pueden usarse para darle formato si se desea. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- El comando `check` está implementado enteramente en C. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Documentar cómo contribuir a pgBackRest. (*Contribución de Cynthia Shang, David Steele.*)
- Documentar la versión máxima para la opción `auto-stop`. (*Contribución de Brad Nicholson. Revisado por David Steele.*)

**Mejoras en la suite de pruebas:**

- Corregir que se use la ruta de pruebas de contenedor cuando `--vm=none`. (*Sugerido por Stephen Frost.*)
- Corregir una zona horaria no coincidente en la prueba expect. (*Sugerido por Stephen Frost.*)
- No autogenerar el código libc embebido por defecto. (*Sugerido por Stephen Frost.*)


### Notas de la versión v2.18 {#v218-release-notes}

*Soporte de PostgreSQL 12*

*Publicada el 1 de octubre de 2019*

**Funcionalidades:**

- Soporte de PostgreSQL 12.
- Añadir la opción `set` del comando `info` para una salida de texto detallada. Los detalles adicionales incluyen las bases de datos que pueden usarse para la restauración selectiva y una lista de tablespaces y enlaces simbólicos con sus destinos predeterminados. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Stephen Frost, ejberdecia.*)
- Añadir el tipo de restauración `standby`. Este tipo de restauración añade automáticamente standby_mode=on a recovery.conf para PostgreSQL < 12 y crea `standby.signal` para PostgreSQL ≥ 12, creando una interfaz común entre versiones de PostgreSQL. (*Revisado por Cynthia Shang.*)

**Mejoras:**

- El comando `restore` está implementado enteramente en C. (*Revisado por Cynthia Shang.*)

**Mejoras en la documentación:**

- Documentar la relación entre `db-timeout` y `protocol-timeout`. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por James Chanco Jr.*)
- Añadir aclaraciones a la documentación sobre los repositorios en réplicas. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadir una pregunta frecuente sobre la recuperación en un punto en el tiempo basada en tiempo. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v2.17 {#v217-release-notes}

*Migraciones a C y correcciones de errores*

*Publicada el 3 de septiembre de 2019*

**Correcciones de errores:**

- Mejorar la construcción lenta del manifiesto para cantidades muy grandes de tablas/segmentos. (*Reportado por Jens Wilke.*)
- Corregir las exclusiones de archivos especiales. (*Reportado por CluelessTechnologist, Janis Puris, Rachid Broum.*)

**Mejoras:**

- Los comandos `stanza-create/update/delete` están implementados enteramente en C. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Los comandos `start`/`stop` están implementados enteramente en C. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Crear directorios/archivos de registro con modo `0750`/`0640`. (*Sugerido por Damiano Albani.*)

**Correcciones de errores en la documentación:**

- Corregir que se instalara el paquete `yum.p.o` cuando se especificaba un paquete personalizado. (*Reportado por Joe Ayers, John Harvey.*)

**Mejoras en la documentación:**

- Compilar pgBackRest como un usuario sin privilegios. (*Sugerido por Laurenz Albe.*)


### Notas de la versión v2.16 {#v216-release-notes}

*Migraciones a C y correcciones de errores*

*Publicada el 5 de agosto de 2019*

**Correcciones de errores:**

- Reintentar los errores `RequestTimeTooSkewed` de S3 en lugar de terminar inmediatamente. (*Reportado por sean0101n, Tim Garton, Jesper St John, Aleš Zelený.*)
- Corregir el manejo incorrecto de la respuesta `transfer-encoding` a una solicitud `HEAD`. (*Reportado por Pavel Suderevsky.*)
- Corregir violaciones de ámbito expuestas por optimizaciones en gcc 9. (*Reportado por Christian Lange, Ned T. Crigler.*)

**Funcionalidades:**

- Añadir la opción `repo-s3-port` para establecer un puerto de servicio S3 no estándar.

**Mejoras:**

- El comando `local` para `backup` está implementado enteramente en C. (*Contribución de David Steele, Cynthia Shang.*)
- El comando `check` está implementado parcialmente en C. (*Revisado por Cynthia Shang.*)


### Notas de la versión v2.15 {#v215-release-notes}

*Implementación en C de expire*

*Publicada el 25 de junio de 2019*

**Correcciones de errores:**

- Corregir la retención del archivado que expiraba de forma demasiado agresiva. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Mohamad El-Rifai.*)

**Mejoras:**

- El comando `expire` está implementado enteramente en C. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- El comando `local` para restore está implementado enteramente en C.
- Eliminar el usuario de PostgreSQL codificado de forma fija para que `$PGUSER` funcione. (*Sugerido por Julian Zhang, Janis Puris.*)
- Respetar la opción `--prefix` de configure. (*Sugerido por Daniel Westermann.*)
- Renombrar la opción `repo-s3-verify-ssl` a `repo-s3-verify-tls`. Se prefiere el nombre nuevo porque pgBackRest no soporta ninguna versión del protocolo SSL (todas se consideran inseguras). El nombre antiguo seguirá aceptándose.

**Mejoras en la documentación:**

- Añadir preguntas frecuentes a la documentación. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Usar `wal_level=replica` en la documentación para PostgreSQL ≥ 9.6. (*Sugerido por Patrick McLaughlin.*)


### Notas de la versión v2.14 {#v214-release-notes}

*Corrección de error y mejoras*

*Publicada el 20 de mayo de 2019*

**Correcciones de errores:**

- Corregir un segfault cuando `process-max` > 8 para `archive-push`/`archive-get`. (*Reportado por Jens Wilke.*)

**Mejoras:**

- Omitir las comprobaciones de la base de datos cuando se ejecuta `stanza-delete` con `force`. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por hatifnatt.*)
- Añadir el script `configure` para mejorar el soporte multiplataforma.

**Funcionalidades de la documentación:**

- Añadir guías de usuario para CentOS/RHEL 6/7.


### Notas de la versión v2.13 {#v213-release-notes}

*Correcciones de errores*

*Publicada el 18 de abril de 2019*

**Correcciones de errores:**

- Corregir lecturas de longitud cero que causaban problemas a los filtros de E/S que no las esperaban. (*Reportado por brunre01, Jens Wilke, Tomasz Kontusz, guruguruguru.*)
- Corregir la fiabilidad del reporte de errores de los procesos `local`/`remote`.
- Corregir los mensajes de error de Posix/CIFS que reportaban el nombre de archivo incorrecto en write/sync/close.


### Notas de la versión v2.12 {#v212-release-notes}

*Implementación en C de archive push*

*Publicada el 11 de abril de 2019*

**NOTA IMPORTANTE**: La nueva implementación de TLS/SSL prohíbe los puntos en los nombres de bucket de S3 según el RFC-2818. Esta corrección de seguridad es necesaria para una verificación de nombres de host conforme a la norma.

**Correcciones de errores:**

- Corregir problemas cuando una opción de ruta termina en /. (*Reportado por Marc Cousin.*)
- Corregir problemas cuando se establece `log-level-file=off` para el comando `archive-get`. (*Reportado por Brad Nicholson.*)
- Corregir el código C para reconocer el formato de opción `host:port` como lo hace Perl. (*Reportado por Kyle Nevins.*)
- Corregir problemas con las opciones de registro de los comandos `remote`/`local`.

**Mejoras:**

- El comando `archive-push` está implementado enteramente en C.
- Aumentar el límite de `process-max` a `999`. (*Sugerido por Rakshitha-BR.*)
- Mejorar el mensaje de error cuando un nombre de bucket de S3 contiene puntos.

**Mejoras en la documentación:**

- Aclarar que los almacenes de objetos compatibles con S3 están soportados. (*Sugerido por Magnus Hagander.*)


### Notas de la versión v2.11 {#v211-release-notes}

*Implementación en C de archive get*

*Publicada el 11 de marzo de 2019*

**Correcciones de errores:**

- Corregir posibles segmentos WAL truncados cuando ocurre un error a mitad de una escritura. (*Reportado por blogh.*)
- Corregir que al comando info le faltara el mínimo/máximo de WAL cuando se especifica una stanza. (*Corregido por Stefan Fercot. Revisado por David Steele.*)
- Corregir un JSON no conforme para las opciones pasadas de C a Perl. (*Reportado por Leo Khomenko.*)

**Mejoras:**

- El comando `archive-get` está implementado enteramente en C.
- Habilitar keep-alive de socket en versiones antiguas de Perl. (*Contribución de Marc Cousin. Revisado por David Steele.*)
- Generar error cuando se pasan parámetros a un comando que no acepta parámetros. (*Sugerido por Jason O'Donnell.*)
- Añadir sugerencias cuando no se puede encontrar un segmento WAL en el archivado. (*Sugerido por Hans-Jürgen Schönig.*)
- Mejorar el error cuando no se puede encontrar el nombre de host en un certificado. (*Sugerido por James Badger.*)
- Añadir opciones adicionales a `backup.manifest` para fines de depuración. (*Contribución de blogh. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Actualizar la versión predeterminada de la documentación a PostgreSQL 10.


### Notas de la versión v2.10 {#v210-release-notes}

*Correcciones de errores*

*Publicada el 9 de febrero de 2019*

**Correcciones de errores:**

- Añadir el método del controlador S3 no implementado requerido por `archive-get`. (*Reportado por mibiio.*)
- Corregir la comprobación de `pg-path` configurado incorrectamente. (*Reportado por James Chanco Jr.*)


### Notas de la versión v2.09 {#v209-release-notes}

*Mejoras menores y correcciones de errores*

*Publicada el 30 de enero de 2019*

**Correcciones de errores:**

- Corregir un problema con múltiples archivos de estado asincrónicos que causaba un error grave. (*Reportado por Vidhya Gurumoorthi, Joe Ayers, Douglas J Hunley.*)

**Mejoras:**

- El comando `info` está implementado enteramente en C. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Simplificar el mensaje de texto del comando `info` cuando no hay stanzas. Se reemplaza la ruta del repositorio por «the repository».
- Añadir la bandera `_DARWIN_C_SOURCE` al Makefile para compilaciones en MacOS. (*Contribución de Douglas J Hunley. Revisado por David Steele.*)
- Actualizar la búsqueda de direcciones en el cliente TLS de C para usar métodos modernos. (*Sugerido por Bruno Friedmann.*)
- Incluir el encabezado conforme a Posix para `strcasecmp()` y `fd_set`. (*Sugerido por ucando.*)

**Correcciones de errores en la documentación:**

- Corregir la ruta de repositorio codificada de forma fija. (*Reportado por Heath Lord.*)

**Mejoras en la documentación:**

- Aclarar que el cifrado siempre se realiza del lado del cliente. (*Sugerido por Bruce Burdick.*)
- Añadir ejemplos para construir un host de documentación.
- Permitir `if` en variables, listas y elementos de lista del manifiesto.


### Notas de la versión v2.08 {#v208-release-notes}

*Mejoras menores y correcciones de errores*

*Publicada el 2 de enero de 2019*

**Correcciones de errores:**

- Eliminar la solicitud de información del objeto S3 justo después de subirlo. (*Reportado por Matt Kunkel.*)
- Corregir `archive-get-queue-max` para que sea de tipo `size`. (*Reportado por Ronan Dunklau.*)
- Añadir un mensaje de error cuando el `uid`/`gid` del usuario actual no se mapea a un nombre. (*Reportado por Camilo Aguilar.*)
- Generar error cuando se especifica `--target-action=shutdown` para PostgreSQL < 9.5.

**Mejoras:**

- Establecer keepalives de TCP en las conexiones S3. (*Sugerido por Ronan Dunklau.*)
- Reordenar la salida de texto del comando `info` para que la copia de seguridad más reciente se muestre al final. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Ryan Lambert.*)
- Cambiar la propiedad de los archivos solo cuando sea necesario.
- Censurar el encabezado `authentication` al lanzar errores de S3. (*Sugerido por Brad Nicholson.*)

**Mejoras en la documentación:**

- Aclarar cuándo `target-action` es efectivo y el soporte de versiones de PostgreSQL. (*Sugerido por Keith Fiske.*)
- Aclarar que la región/el endpoint deben configurarse correctamente para el bucket. (*Sugerido por Pritam Barhate.*)
- Añadir documentación para construir la documentación.


### Notas de la versión v2.07 {#v207-release-notes}

*Delta de suma de verificación automático para copias de seguridad*

*Publicada el 16 de noviembre de 2018*

**Correcciones de errores:**

- Corregir un problema por el que `archive-push-queue-max` no se respetaba ante un error de conexión. (*Reportado por Lardière Sébastien.*)
- Corregir el tamaño estático de segmento WAL usado para determinar si se ha excedido `archive-push-queue-max`.
- Corregir un error tras un fallo de apertura del archivo de registro cuando el procesamiento debería continuar. (*Reportado por vthriller.*)

**Funcionalidades:**

- Habilitar automáticamente el delta de suma de verificación de la copia de seguridad cuando se detectan anomalías (p. ej. un cambio de línea de tiempo). (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras:**

- Reintentar todos los errores `5xx` de S3 en lugar de solo los errores internos `500`. (*Sugerido por Craig A. James.*)


### Notas de la versión v2.06 {#v206-release-notes}

*Copia de seguridad con delta de suma de verificación y soporte de PostgreSQL 11*

*Publicada el 15 de octubre de 2018*

**Correcciones de errores:**

- Corregir la codificación URI faltante en el controlador S3. (*Reportado por Dan Farrell.*)
- Corregir el mensaje de error incorrecto para opciones duplicadas en archivos de configuración. (*Reportado por Jesper St John.*)
- Corregir el reporte incorrecto del retorno de error en el registro de `info`. Un código de retorno 1 de `archive-get` se registraba como mensaje de error a nivel `info`, pero por lo demás funcionaba correctamente.

**Funcionalidades:**

- Añadir delta de suma de verificación para copias de seguridad incrementales. Las copias con delta de suma de verificación usan sumas de verificación en lugar de marcas de tiempo para determinar si los archivos han cambiado. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Soporte de PostgreSQL 11, incluido el tamaño de segmento WAL configurable.

**Mejoras:**

- Ignorar todos los archivos en un directorio de tablespace enlazado excepto el subdirectorio de la versión actual de PostgreSQL. Anteriormente se generaba un error si había otros archivos presentes que no pertenecieran al usuario de PostgreSQL.
- Mejorar el comando `info` para mostrar el tipo de cifrado de la stanza. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Douglas J Hunley.*)
- Mejorar el soporte de caracteres especiales en nombres de archivo.
- Permitir que la opción `delta` se especifique en el archivo de configuración de pgBackRest. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Usar `command` en `authorized_hosts` para mejorar la seguridad de SSH. (*Sugerido por Stephen Frost, Magnus Hagander.*)
- Listar los valores permitidos de la opción `buffer-size` en la referencia de configuración. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Stéphane Schildknecht.*)


### Notas de la versión v2.05 {#v205-release-notes}

*Opciones por variables de entorno y exclusión de relaciones temporales y unlogged*

*Publicada el 31 de agosto de 2018*

**Correcciones de errores:**

- Corregir un problema por el que los enlaces *relativos* en `$PGDATA` podían almacenarse en la copia de seguridad con la ruta incorrecta. Este problema no afectaba a los enlaces absolutos y los enlaces relativos de tablespaces eran detectados por otras comprobaciones. (*Reportado por Cynthia Shang.*)
- Eliminar la opción `online` implementada de forma incompleta del comando `check`. La operación sin conexión va contra el propósito de este comando, que es comprobar si el archivado y las copias de seguridad funcionan correctamente. (*Reportado por Jason O'Donnell.*)
- Corregir un problema por el que los errores generados en C no se registraban cuando se los llamaba desde Perl. pgBackRest terminaba correctamente con el código de error correcto, pero carecía de un mensaje de error para ayudar en la depuración. (*Reportado por Douglas J Hunley.*)
- Corregir un problema cuando una opción booleana (p. ej. `delta`) se especificaba más de una vez. (*Reportado por Yogesh Sharma.*)

**Funcionalidades:**

- Permitir que cualquier opción se establezca en una variable de entorno. Esto incluye opciones que antes solo podían especificarse en la línea de comandos, p. ej. `stanza`, y opciones secretas que no podían especificarse en la línea de comandos, p. ej. `repo1-s3-key-secret`.
- Excluir de la copia de seguridad los archivos de relaciones temporales y unlogged (tablas/índices). Implementado con la misma lógica que los parches que añadieron esta funcionalidad a PostgreSQL, [8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25) y [920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f). La exclusión de relaciones temporales está habilitada en PostgreSQL ≥ `9.0`. La exclusión de relaciones unlogged está habilitada en PostgreSQL ≥ `9.1`, donde se introdujo la funcionalidad. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Permitir excluir de una copia de seguridad directorios y/o archivos arbitrarios. El mal uso de esta funcionalidad puede llevar a copias de seguridad inconsistentes, así que lee cuidadosamente la documentación de `--exclude` antes de usarla. (*Revisado por Cynthia Shang.*)
- Añadir la opción `log-subprocess` para permitir el registro a archivo de los subprocesos `local` y `remote`.
- Soporte de PostgreSQL 11 Beta 3.

**Mejoras:**

- Permitir que los archivos de tamaño cero en el manifiesto de la copia de seguridad referencien un manifiesto anterior sin importar el delta de marca de tiempo. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Mejorar el rendimiento asincrónico de `archive-get`/`archive-push` comprobando directamente los archivos de estado. (*Contribución de Stephen Frost. Revisado por David Steele.*)
- Mejorar el mensaje de error cuando a un comando le falta la opción `stanza`. (*Sugerido por Sarah Conway.*)

**Correcciones de errores en la documentación:**

- Corregir un nivel de registro inválido en la referencia de la opción `log-path`. (*Reportado por Camilo Aguilar.*)

**Mejoras en la documentación:**

- Dejar de intentar ordenar los colaboradores en `release.xml` por apellido/nombre. Los nombres de los colaboradores siempre se han presentado en las notas de versión exactamente como se dieron, pero intentábamos asignar ID internos basados en apellido/nombre, lo que puede ser difícil de determinar y en última instancia no tiene sentido. Inspirado en la charla de Christophe en PostgresOpen 2017, «Human Beings Do Not Have a Primary Key». (*Sugerido por Christophe Pettus.*)

**Mejoras en la suite de pruebas:**

- Generar error si la compilación de LibC se realiza fuera del entorno de pruebas. LibC ya no es necesaria para las compilaciones de producción.


### Notas de la versión v2.04 {#v204-release-notes}

*Corrección crítica para la reanudación de copias de seguridad*

*Publicada el 5 de julio de 2018*

**NOTA IMPORTANTE**: Esta versión corrige un error crítico en la funcionalidad de reanudación de copias de seguridad. Todas las copias reanudadas anteriores a esta versión deben considerarse inconsistentes. Una copia de seguridad se reanudará después de que falle una copia anterior, a menos que se haya especificado `resume=n`. Puede identificarse una copia reanudada comprobando en el registro de la copia el mensaje «aborted backup of same type exists, will be cleaned to remove invalid files and resumed». Si el mensaje existe, no uses esa copia de seguridad ni ninguna del mismo conjunto para una restauración, y revisa los registros de restauración para ver si se restauró una copia reanudada. Si es así, puede haber datos inconsistentes en el clúster.

**Correcciones de errores:**

- Corregir el error crítico en la reanudación que producía copias de seguridad inconsistentes. Una regresión en `v0.82` eliminó la comparación de marcas de tiempo al decidir qué archivos de la copia abortada conservar al reanudar. Consulta la nota anterior para más detalles. (*Reportado por David Youatt, Yogesh Sharma, Stephen Frost.*)
- Corregir un error en la restauración selectiva cuando solo existe una base de datos de usuario en el clúster. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Nj Baliyan.*)
- Corregir el formato de marca de tiempo ISO-8601 no conforme en los encabezados de autorización de S3. AWS y algunas pasarelas toleraban un espacio en lugar de horas con ceros a la izquierda, mientras que otras no. (*Corregido por Andrew Schwartz. Revisado por David Steele.*)

**Funcionalidades:**

- Soporte de PostgreSQL 11 Beta 2.

**Mejoras:**

- Mejorar el cliente HTTP para establecer `content-length` en 0 cuando el servidor no lo especifica. S3 (y las pasarelas) siempre establecen `content-length` o `transfer-encoding`, pero `HTTP 1.1` no lo requiere y los proxies (p. ej. HAProxy) pueden no incluir ninguno. (*Sugerido por Adam K. Sumner.*)
- Establecer `search_path = 'pg_catalog'` en las conexiones a PostgreSQL. (*Sugerido por Stephen Frost.*)

**Mejoras en la documentación:**

- Crear una nueva sección que describa la compilación de pgBackRest y compilar en un host separado.
- Añadir una política S3 de ejemplo para restringir los privilegios del bucket. (*Sugerido por Douglas J Hunley, Jason O'Donnell.*)


### Notas de la versión v2.03 {#v203-release-notes}

*Un único ejecutable para desplegar*

*Publicada el 22 de mayo de 2018*

**Correcciones de errores:**

- Corregir un posible desbordamiento de búfer en el manejo de mensajes de error. (*Reportado por Lætitia.*)
- Corregir que se tomara el bloqueo de escritura del archivado para el comando `archive-get` sincrónico. (*Reportado por uspen.*)

**Mejoras:**

- Incrustar las funciones C exportadas y los módulos Perl directamente en el ejecutable de pgBackRest.
- Usar `time_t` en lugar de `__time_t` para mejor portabilidad. (*Sugerido por Nick Floersch.*)
- Imprimir el tiempo total de ejecución en milisegundos al final del comando.


### Notas de la versión v2.02 {#v202-release-notes}

*Archive-get asincrónico paralelo e includes de configuración*

*Publicada el 6 de mayo de 2018*

**Correcciones de errores:**

- Corregir sincronizaciones de directorios que se ejecutaban recursivamente cuando solo debería sincronizarse el directorio especificado. (*Reportado por Craig A. James.*)
- Corregir que `archive-copy` lanzara el error «path not found» para copias de seguridad incr/diff. (*Reportado por yummyliu, Vitaliy Kukharik.*)
- Corregir un fallo en la construcción del manifiesto cuando dos o más archivos en `PGDATA` están enlazados al mismo directorio. (*Reportado por Vitaliy Kukharik.*)
- Corregir el fallo de la restauración delta cuando falta un archivo enlazado.
- Corregir la renderización de las opciones clave/valor y de lista en la ayuda. (*Reportado por Clinton Adams.*)

**Funcionalidades:**

- Añadir `archive-get` asincrónico y paralelo. Esta funcionalidad mantiene una cola de segmentos WAL para ayudar a reducir la latencia cuando PostgreSQL solicita un segmento WAL con restore_command.
- Añadir soporte para archivos de configuración adicionales de pgBackRest. El directorio se especifica con la opción `--config-include-path`. Se añade la opción `--config-path` para sobrescribir la ruta base por defecto de las opciones `--config` y `--config-include-path`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadir la opción `repo-s3-token` para permitir configurar tokens de credenciales temporales. pgBackRest actualmente no tiene forma de solicitar credenciales nuevas, por lo que todo el comando (p. ej. `backup`, `restore`) debe completarse antes de que las credenciales expiren. (*Contribución de Yogesh Sharma. Revisado por David Steele.*)

**Mejoras:**

- Actualizar las opciones `archive-push-queue-max`, `manifest-save-threshold` y `buffer-size` para aceptar valores en `KB`, `MB`, `GB`, `TB` o `PB`, donde el multiplicador es una potencia de `1024`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Hacer más eficiente la sincronización de rutas de la copia de seguridad/restauración. Explorar todo el directorio puede ser muy costoso si hay muchas tablas pequeñas. El manifiesto de la copia de seguridad contiene la lista de rutas, así que úsala para realizar las sincronizaciones en lugar de explorar la ruta de la copia de seguridad/restauración.
- Mostrar los parámetros del comando además de las opciones del comando en el mensaje inicial de registro de nivel info.
- Renombrar la opción archive-queue-max a archive-push-queue-max. Esto es consistente con la nueva opción `archive-get-queue-max`. El nombre antiguo de la opción seguirá aceptándose.

**Correcciones de errores en la documentación:**

- Actualizar la documentación con el soporte y las advertencias de 32 bits. El soporte de 32 bits se añadió en la v1.26. (*Reportado por Viorel Tabara.*)

**Mejoras en la documentación:**

- Añadir ejemplos de monitoreo usando PostgreSQL y jq. (*Sugerido por Stephen Frost, Brian Faherty.*)
- Añadir un ejemplo de uso de secciones de comandos a la configuración de archivado. (*Sugerido por Christophe Courtois.*)
- Eliminar la documentación que describía `info --output=json` como experimental.
- Actualizar la descripción desactualizada de la opción `spool-path`.

**Funcionalidades de la suite de pruebas:**

- Usar lcov para el reporte de cobertura de las pruebas unitarias de C. Se cambió desde Devel::Cover porque no reportaba la cobertura de ramas para los reportes convertidos desde gcov. Una cobertura de ramas incompleta de un módulo ahora genera un error. La cobertura de las pruebas unitarias no se muestra en el reporte a menos que esté incompleta en la cobertura de sentencias o de ramas.


### Notas de la versión v2.01 {#v201-release-notes}

*Correcciones y mejoras menores*

*Publicada el 19 de marzo de 2018*

**Correcciones de errores:**

- Corregir que las opciones `--target-action` y `--recovery-option` se reportaran como inválidas al restaurar con `--type=immediate`. (*Reportado por Brad Nicholson.*)
- Generar error inmediatamente cuando se pasa una opción segura (p. ej. `repo1-s3-key`) en la línea de comandos. Dado que pgBackRest no pasaba las opciones seguras a los subprocesos, se lanzaba un error oscuro. El nuevo error es mucho más claro y proporciona sugerencias sobre cómo solucionar el problema. Se actualiza la documentación de comandos para omitir las opciones seguras que no pueden especificarse en la línea de comandos. (*Reportado por Brad Nicholson.*)
- Corregir un problema al pasar `--no-config` a Perl embebido. (*Reportado por Ibrahim Edib Kokdemir.*)
- Corregir un problema por el que especificar `log-level-stderr` > `warn` hacía que un proceso `local`/`remote` terminara con error por haber salida en stderr cuando no se esperaba ninguna. El valor máximo para un proceso `local`/`remote` es ahora `error`, ya que no hay razón para que estos procesos emitan advertencias. (*Reportado por Clinton Adams.*)
- Corregir la prueba de manifiesto en el comando `check` cuando hay tablespaces. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Thomas Flatley.*)

**Mejoras:**

- Generar error cuando se establecen múltiples argumentos en el archivo de configuración para una opción que no acepta múltiples argumentos. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Eliminar los comandos sudo superfluos de `src/Makefile`. (*Contribución de Adrian Vondendriesch. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Mostrar el índice en los ejemplos de las opciones indexadas, es decir, `repo-*`, `pg-*`. (*Sugerido por Stephen Frost.*)
- Simplificar la tabla de contenido de la página de comandos listando solo los comandos. (*Sugerido por Stephen Frost.*)
- Eliminar las referencias a que la biblioteca C era opcional.

**Funcionalidades de la suite de pruebas:**

- Añadir compilaciones de paquetes para CentOS/RHEL.
- Usar clang para el análisis de código estático. Inicialmente no se encontró nada excepto algunas funciones que deberían haberse marcado como `__noreturn__`.


### Notas de la versión v2.00 {#v200-release-notes}

*Mejoras de rendimiento para archive push*

*Publicada el 23 de febrero de 2018*

**Funcionalidades:**

- El comando `archive-push` está ahora codificado parcialmente en C, lo que permite que el `archive_command` de PostgreSQL se ejecute significativamente más rápido al procesar los mensajes de estado del proceso de archivado asincrónico. (*Revisado por Cynthia Shang.*)

**Mejoras:**

- Mejorar el comando `check` para verificar que el manifiesto de la copia de seguridad puede construirse. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Mejorar el rendimiento del cliente HTTPS. El almacenamiento en búfer ahora tiene en cuenta los bytes `pending` del socket (cuando están presentes) en lugar de depender enteramente de `select()`. En algunos casos, los últimos bytes no se volcaban hasta que se cerraba la conexión.
- Mejorar el rendimiento del borrado en S3. La constante `S3_BATCH_MAX` había sido reemplazada por un valor fijo de 2, probablemente durante las pruebas.
- Permitir que cualquier opción no exclusiva de línea de comandos se restablezca a su valor por defecto en la línea de comandos. Esto permite restablecer a su valor por defecto las opciones de `pgbackrest.conf`, lo que reduce la necesidad de escribir nuevos archivos de configuración para necesidades específicas.
- La biblioteca de C ahora es requerida. Esto elimina la carga condicional y facilita el desarrollo de nuevas funcionalidades de la biblioteca.
- El ejecutable `pgbackrest` es ahora un binario de C en lugar de Perl. Esto permite que ciertos comandos críticos en el tiempo (como `archive-push` asincrónico) se ejecuten más rápido.
- Renombrar las opciones `db-*` a `pg-*` y las opciones `backup-*` a `repo-*` para mejorar la consistencia. Las opciones `repo-*` ahora están indexadas, aunque actualmente solo se permite una.

**Funcionalidades de la documentación:**

- Todos los clústeres de la documentación se inicializan con sumas de verificación.

**Mejoras en la documentación:**

- Listar los nombres de opciones obsoletos en la documentación y la ayuda de línea de comandos.
- Aclarar que los buckets de S3 deben ser creados por el usuario. (*Sugerido por David Youatt.*)


### Notas de la versión v1.29 {#v129-release-notes}

*Corrección crítica para la reanudación de copias de seguridad*

*Publicada el 5 de julio de 2018*

**NOTA IMPORTANTE**: Esta versión corrige un error crítico en la funcionalidad de reanudación de copias de seguridad. Todas las copias reanudadas anteriores a esta versión deben considerarse inconsistentes. Una copia de seguridad se reanudará después de que falle una copia anterior, a menos que se haya especificado `resume=n`. Puede identificarse una copia reanudada comprobando en el registro de la copia el mensaje «aborted backup of same type exists, will be cleaned to remove invalid files and resumed». Si el mensaje existe, no uses esa copia de seguridad ni ninguna del mismo conjunto para una restauración, y revisa los registros de restauración para ver si se restauró una copia reanudada. Si es así, puede haber datos inconsistentes en el clúster.

**Correcciones de errores:**

- Corregir el error crítico en la reanudación que producía copias de seguridad inconsistentes. Una regresión en `v0.82` eliminó la comparación de marcas de tiempo al decidir qué archivos de la copia abortada conservar al reanudar. Consulta la nota anterior para más detalles. (*Reportado por David Youatt, Yogesh Sharma, Stephen Frost.*)
- Corregir el formato de marca de tiempo ISO-8601 no conforme en los encabezados de autorización de S3. AWS y algunas pasarelas toleraban un espacio en lugar de horas con ceros a la izquierda, mientras que otras no. (*Corregido por Andrew Schwartz. Revisado por David Steele.*)
- Corregir sincronizaciones de directorios que se ejecutaban recursivamente cuando solo debería sincronizarse el directorio especificado. (*Reportado por Craig A. James.*)
- Corregir que las opciones `--target-action` y `--recovery-option` se reportaran como inválidas al restaurar con `--type=immediate`. (*Reportado por Brad Nicholson.*)
- Corregir que `archive-copy` lanzara el error «path not found» para copias de seguridad incr/diff. (*Reportado por yummyliu, Vitaliy Kukharik.*)
- Corregir un fallo en la construcción del manifiesto cuando dos o más archivos en `PGDATA` estaban enlazados al mismo directorio. (*Reportado por Vitaliy Kukharik.*)
- Corregir el fallo de la restauración delta cuando faltaba un archivo enlazado.
- Corregir un error en la restauración selectiva cuando solo existe una base de datos de usuario en el clúster. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Nj Baliyan.*)

**Mejoras:**

- Mejorar el cliente HTTP para establecer `content-length` en 0 cuando el servidor no lo especifica. S3 (y las pasarelas) siempre establecen `content-length` o `transfer-encoding`, pero `HTTP 1.1` no lo requiere y los proxies (p. ej. HAProxy) pueden no incluir ninguno. (*Sugerido por Adam K. Sumner.*)
- Mejorar el rendimiento del cliente HTTPS. El almacenamiento en búfer ahora tiene en cuenta los bytes `pending` del socket (cuando están presentes) en lugar de depender enteramente de `select()`. En algunos casos, los últimos bytes no se volcaban hasta que se cerraba la conexión.
- Mejorar el rendimiento del borrado en S3. La constante `S3_BATCH_MAX` había sido reemplazada por un valor fijo de 2, probablemente durante las pruebas.
- Hacer más eficiente la sincronización de rutas de la copia de seguridad/restauración. Explorar todo el directorio puede ser muy costoso si hay muchas tablas pequeñas. El manifiesto de la copia de seguridad contiene la lista de rutas, así que úsala para realizar las sincronizaciones en lugar de explorar la ruta de la copia de seguridad/restauración. Eliminar la funcionalidad de sincronización recursiva de rutas dado que ya no se usa.

**Correcciones de errores en la documentación:**

- Actualizar la documentación con el soporte y las advertencias de 32 bits. El soporte de 32 bits se añadió en la v1.26. (*Reportado por Viorel Tabara.*)

**Mejoras en la documentación:**

- Aclarar que los buckets de S3 deben ser creados por el usuario. (*Sugerido por David Youatt.*)
- Actualizar la descripción desactualizada de la opción `spool-path`.


### Notas de la versión v1.28 {#v128-release-notes}

*Eliminación de stanza*

*Publicada el 1 de febrero de 2018*

**Correcciones de errores:**

- Corregida la imposibilidad de restaurar una única base de datos contenida en un tablespace usando --db-include. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Chiranjeevi Ravilla.*)
- Asegurar que se seleccione el `db-id` más reciente al emparejar `archive.info` con `backup.info`. Esto proporciona el emparejamiento correcto en caso de que haya duplicados de `system-id` y `db-version` (p. ej. tras revertir un `pg_upgrade`). (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Adam K. Sumner.*)
- Corregido un mensaje de error excesivamente verborréico al reportar un comando inválido. (*Reportado por Jason O'Donnell.*)

**Funcionalidades:**

- Añadir el comando `stanza-delete` para limpiar stanzas sin uso. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Magnus Hagander.*)

**Mejoras:**

- Mejorar el comando `stanza-create` para que no dé error cuando la stanza ya existe. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Actualizar la documentación de `stanza-create --force` para instar a la precaución al usarla. (*Sugerido por Jason O'Donnell.*)


### Notas de la versión v1.27 {#v127-release-notes}

*Correcciones de errores y documentación*

*Publicada el 19 de diciembre de 2017*

**Correcciones de errores:**

- Corregido un problema que suprimía los errores de localidad para `backup` y `restore`. Cuando hay un host de copia de seguridad presente, las copias solo deberían permitirse en el host de copia de seguridad y las restauraciones solo deberían permitirse en el host de la base de datos, a menos que se cree una configuración alternativa que ignore el host remoto. (*Reportado por Lardière Sébastien.*)
- Corregido un problema por el que el WAL no expiraba en PostgreSQL 10. Esto fue causado por una expresión regular defectuosa que esperaba que todas las versiones principales de PostgreSQL fueran X.X. (*Reportado por Adam Brusselback.*)
- Corregido un problema por el que la opción `--no-config` no se pasaba a los procesos hijos. Esto significaba que los procesos hijos aún leerían el archivo de configuración local y podrían causar comportamientos inesperados.
- Corregido el comando `info` para eliminar la salida `"db (prior)"` si no existen copias de seguridad ni archivados para una versión anterior del clúster. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Stephen Frost.*)

**Funcionalidades de la documentación:**

- Documentar la relación entre las opciones `archive-copy` y `archive-check`. (*Sugerido por Markus Nullmeier.*)
- Mejorar la documentación de referencia de `archive-copy`.


### Notas de la versión v1.26 {#v126-release-notes}

*Cifrado del repositorio*

*Publicada el 21 de noviembre de 2017*

**Correcciones de errores:**

- Corregido un problema que podía hacer fallar la copia de manifiestos grandes durante la restauración. (*Reportado por Craig A. James.*)
- Corregido el desplazamiento WAL incorrecto para arquitecturas de 32 bits. (*Corregido por Javier Wilson. Revisado por David Steele.*)
- Corregido un problema al recuperar WAL para versiones antiguas de la base de datos. Después de un `stanza-upgrade` debería seguir siendo posible restaurar copias de seguridad de la versión anterior y realizar la recuperación con `archive-get`. Sin embargo, archive-get solo comprobaba la versión/id de base de datos más reciente y fallaba. También se limpian algunos problemas cuando la misma versión/id de base de datos aparece varias veces en el historial. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Clinton Adams.*)
- Corregido un problema con la correcta aplicación de grupos inválidos de la copia de seguridad en la restauración. Si la copia de seguridad no puede mapear un grupo a un nombre, almacena el grupo en el manifiesto como `false` y luego usa el propietario de $PGDATA para establecer el grupo durante la restauración o, en su defecto, el grupo del usuario actual. Esta lógica no funcionaba correctamente porque el grupo seleccionado sobrescribía al usuario en la restauración, dejando el grupo sin definir y el usuario incorrectamente establecido como el grupo. (*Reportado por Jeff McCormick.*)
- Corregido un problema al pasar parámetros a los remotos. Cuando se especificaba más de una db, la ruta, el puerto y la ruta de socket de la db1 se pasaban sin importar a qué db se estuviera dirigiendo realmente. (*Reportado por uspen.*)

**Funcionalidades:**

- Soporte de cifrado del repositorio. (*Contribución de Cynthia Shang, David Steele.*)

**Mejoras:**

- Deshabilitar el filtro gzip cuando `--compress-level-network=0`. El filtro se usaba con el nivel de compresión establecido en 0, lo que añadía sobrecarga sin ningún beneficio.
- Mejora del rendimiento de descompresión del filtro gzip.

**Funcionalidades de la documentación:**

- Añadir una plantilla para mejorar la información inicial recopilada para los reportes de issues. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Aclarar el uso de la opción `archive-timeout` y describir en qué se diferencia del ajuste archive_timeout de PostgreSQL. (*Contribución de Cynthia Shang. Revisado por David Steele. Sugerido por Keith Fiske.*)

**Funcionalidades de la suite de pruebas:**

- Pruebas automatizadas para la arquitectura i386/i686 de 32 bits.


### Notas de la versión v1.25 {#v125-release-notes}

*Mejoras de rendimiento de S3*

*Publicada el 24 de octubre de 2017*

**Correcciones de errores:**

- Corregir que se ignoraran los ajustes personalizados de la opción `compress-level`. (*Reportado por Jens Wilke.*)
- Eliminar el error cuando se detectan líneas de tiempo superpuestas. Las líneas de tiempo superpuestas son válidas en muchos escenarios de recuperación en un punto en el tiempo (PITR). (*Reportado por blogh.*)
- Corregir casos donde `database-id` no se renderizaba como entero en la salida JSON de info. (*Corregido por Cynthia Shang. Revisado por David Steele. Reportado por Jason O'Donnell.*)

**Funcionalidades:**

- Mejorar el rendimiento de las solicitudes de listado en S3. Cualquier porción literal inicial de una expresión de filtro se usa para generar un prefijo de búsqueda, lo que a menudo ayuda a mantener la solicitud lo suficientemente pequeña para evitar la limitación de tasa. (*Sugerido por Mihail Shvein.*)

**Funcionalidades de la suite de pruebas:**

- Añadir pruebas de rendimiento de E/S.


### Notas de la versión v1.24 {#v124-release-notes}

*Nuevas exclusiones de copia de seguridad*

*Publicada el 28 de septiembre de 2017*

**Correcciones de errores:**

- Corregido un problema por el que se emitían advertencias en lugar de mensajes de registro de menor prioridad durante la inicialización de la copia de seguridad desde réplica. (*Reportado por uspen.*)
- Corregido un problema por el que algunas opciones `db-*` (p. ej. `db-port`) no se pasaban a los remotos. (*Reportado por uspen.*)

**Funcionalidades:**

- Excluir de la copia de seguridad el contenido de `pg_snapshots`, `pg_serial`, `pg_notify` y `pg_dynshmem` ya que se reconstruyen al iniciar.
- Excluir de la copia de seguridad los archivos `pg_internal.init` ya que se reconstruyen al iniciar.

**Mejoras:**

- Abrir el archivo de registro después de que el proceso asincrónico esté completamente separado del proceso principal para evitar que el proceso principal también registre en el archivo. (*Sugerido por Jens Wilke.*)

**Funcionalidades de la documentación:**

- Añadir configuración SSH sin contraseña.

**Mejoras en la documentación:**

- Renombrar master a primary en la documentación para alinearse con la convención de PostgreSQL.


### Notas de la versión v1.23 {#v123-release-notes}

*Múltiples réplicas y soporte de PostgreSQL 10*

*Publicada el 3 de septiembre de 2017*

**Correcciones de errores:**

- Corregido un problema que podía causar que la compresión abortara en archivos en crecimiento. (*Reportado por Jesper St John, Aleksandr Rogozin.*)
- Corregido un problema por el que los keep-alives no se enviaban al remoto desde el proceso local. (*Reportado por William Cox.*)

**Funcionalidades:**

- Se pueden configurar hasta siete réplicas para la copia de seguridad desde réplica. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Soporte de PostgreSQL 10.
- Permitir `content-length` (además de la codificación por fragmentos) al leer datos XML para mejorar la compatibilidad con pasarelas S3 de terceros. (*Sugerido por Victor Gdalevich.*)

**Mejoras:**

- Aumentar el tiempo de espera HTTP para S3.
- Añadir reintentos HTTP para blindarse contra errores de red S3 transitorios.

**Correcciones de errores en la documentación:**

- Corregida la generación de documentos para incluir resúmenes de sección en la página de configuración. (*Corregido por Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.22 {#v122-release-notes}

*Reintento de S3 corregido*

*Publicada el 9 de agosto de 2017*

**Correcciones de errores:**

- Corregido un problema de autenticación en el reintento de S3.


### Notas de la versión v1.21 {#v121-release-notes}

*Salida de info mejorada y opción de puerto SSH*

*Publicada el 8 de agosto de 2017*

**Correcciones de errores:**

- El directorio `archive_status` ahora se recrea en la restauración para dar soporte a PostgreSQL 8.3, que no lo recrea automáticamente como lo hacen las versiones más recientes. (*Reportado por Stephen Frost.*)
- Corregido un problema que podía hacer que el directorio de archivado vacío de una versión antigua de PostgreSQL quedara atrás después de un `stanza-upgrade`. (*Corregido por Cynthia Shang. Revisado por David Steele.*)

**Funcionalidades:**

- Modificado el comando `info` (tanto en salida de texto como JSON) para mostrar el ID de archivado y el WAL mínimo/máximo actualmente presente en el archivado para la versión actual y, si existe, la anterior del clúster de bases de datos. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadidas las opciones `--backup-ssh-port` y `--db-ssh-port` para soportar puertos SSH no predeterminados. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras:**

- Reintentar cuando S3 devuelve un error interno (500).

**Correcciones de errores en la documentación:**

- Corregir la descripción de `--online` según el contexto del comando.

**Funcionalidades de la documentación:**

- Añadir la creación de `/etc/pgbackrest.conf` a las instrucciones de instalación manual.

**Mejoras en la documentación:**

- Mover las opciones de repositorio a una sección separada en la ayuda de comandos/línea de comandos. (*Sugerido por Stephen Frost.*)


### Notas de la versión v1.20 {#v120-release-notes}

*Corrección crítica de error para 8.3/8.4*

*Publicada el 27 de junio de 2017*

**NOTA IMPORTANTE**: Las instalaciones de PostgreSQL 8.3 y 8.4 que utilizan tablespaces deberían actualizar de inmediato desde cualquier versión v1 y ejecutar una copia de seguridad completa. Un error impedía que se respaldaran los tablespaces únicamente en estas versiones. PostgreSQL ≥ 9.0 no está afectado.

**Correcciones de errores:**

- Corregido un problema que impedía respaldar los tablespaces en PostgreSQL ≤ 8.4.
- Corregida una bandera faltante en la compilación de la biblioteca C que producía un binario incompatible en sistemas de 32 bits. (*Reportado por Adrian Vondendriesch.*)

**Funcionalidades:**

- Añadir las opciones `s3-repo-ca-path` y `s3-repo-ca-file` para dar cabida a sistemas donde `IO::Socket::SSL` no encuentra automáticamente las CA, es decir, RHEL7, o para cargar CA personalizadas. (*Sugerido por Scott Frazer.*)

**Funcionalidades de la suite de pruebas:**

- Añadir compilaciones de documentación a CI.


### Notas de la versión v1.19 {#v119-release-notes}

*Soporte de S3*

*Publicada el 12 de junio de 2017*

**Correcciones de errores:**

- Corregido el comando `info` para que el mínimo/máximo del archivado de WAL mostrado corresponda a la versión actual de la base de datos. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Corregido el comando `backup` para que la opción `backup-standby` se restablezca (y la copia de seguridad continúe en el primario) si la réplica no está configurada y/o no es accesible. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Corregidas las advertencias de configuración generadas desde un proceso remoto que causaban errores en el proceso maestro. (*Corregido por Cynthia Shang. Revisado por David Steele.*)

**Funcionalidades:**

- Soporte de repositorio en Amazon S3. (*Revisado por Cynthia Shang.*)

**Correcciones de errores en la documentación:**

- Cambiada la opción inválida `max-archive-mb` en la referencia de configuración por `archive-queue-max`.
- Corregido el `sudo` faltante en la sección de instalación. (*Corregido por Lætitia. Revisado por David Steele.*)


### Notas de la versión v1.18 {#v118-release-notes}

*Actualización de stanza, refactorización y mejoras de bloqueo*

*Publicada el 12 de abril de 2017*

**Correcciones de errores:**

- Corregido un problema por el que operaciones de solo lectura que usaban procesos de trabajo locales (es decir, `restore`) creaban bloqueos de escritura que podían interferir con `archive-push` paralelo. (*Reportado por Jens Wilke.*)

**Funcionalidades:**

- Añadido el comando stanza-upgrade para proporcionar un mecanismo de actualización de una stanza tras actualizar a una nueva versión principal de PostgreSQL. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadida la validación de `pgbackrest.conf` para mostrar advertencias si las opciones no son válidas o no están en la sección correcta. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras:**

- Simplificar el esquema de bloqueo. Ahora, solo el proceso maestro mantendrá bloqueos de escritura (para los comandos `archive-push` y `backup`) y no todos los procesos de trabajo locales y remotos como antes.
- No establecer las marcas de tiempo de los archivos en los directorios de copia de seguridad para que coincidan con las del directorio del clúster. Esto se hizo originalmente para permitir la reanudación de copias de seguridad, pero ese proceso ahora está implementado con sumas de verificación.
- Mejorado el mensaje de error cuando el comando `restore` detecta la presencia de `postmaster.pid`. (*Sugerido por Yogesh Sharma.*)
- Renumerar los códigos de retorno entre 25 y 125 para evitar que PostgreSQL interprete algunos como excepciones de señal fatal. (*Sugerido por Yogesh Sharma.*)


### Notas de la versión v1.17 {#v117-release-notes}

*Corrección de error de suma de verificación de páginas*

*Publicada el 13 de marzo de 2017*

**Correcciones de errores:**

- Corregido un problema por el que las páginas recién inicializadas (pero sin usar) causaban advertencias de suma de verificación de páginas. (*Reportado por Stephen Frost.*)


### Notas de la versión v1.16 {#v116-release-notes}

*Mejoras de suma de verificación de páginas, CI y pruebas de paquetes*

*Publicada el 2 de marzo de 2017*

**Correcciones de errores:**

- Corregido un problema por el que las tablas de más de 1GB reportaban advertencias de suma de verificación de páginas después del primer segmento. (*Reportado por Stephen Frost.*)
- Corregido un problema por el que las bases de datos creadas con un tablespace no predeterminado generaban advertencias falsas sobre que `pg_filenode.map` y `pg_internal.init` no estaban alineados a página. (*Reportado por blogh.*)

**Funcionalidades de la suite de pruebas:**

- Integración continua usando `travis-ci`.
- Compilaciones automatizadas de paquetes Debian para todas las distribuciones soportadas.


### Notas de la versión v1.15 {#v115-release-notes}

*Refactorización y correcciones de errores*

*Publicada el 13 de febrero de 2017*

**Correcciones de errores:**

- Corregida una regresión introducida en v1.13 que podía causar fallos en las copias de seguridad si se eliminaban archivos (p. ej. tablas borradas) mientras se construía el manifiesto. (*Reportado por Navid Golpayegani.*)


### Notas de la versión v1.14 {#v114-release-notes}

*Refactorización y correcciones de errores*

*Publicada el 13 de febrero de 2017*

**Correcciones de errores:**

- Corregido un problema por el que un error de archive-push no se reintentaba y en su lugar devolvía errores a PostgreSQL indefinidamente (a menos que el archivo `.error` se eliminara manualmente). (*Reportado por Jens Wilke.*)
- Corregida una condición de carrera en el archivado paralelo donde la creación de nuevas rutas generaba un error cuando múltiples procesos intentaban hacerlo al mismo tiempo. (*Reportado por Jens Wilke.*)

**Mejoras:**

- Mejorado el rendimiento del `wal archive min/max` proporcionado por el comando `info`. (*Sugerido por Jens Wilke.*)

**Funcionalidades de la documentación:**

- Actualizada la documentación del archivado asincrónico para describir con mayor precisión cómo funciona el nuevo método y en qué se diferencia del antiguo. (*Sugerido por Jens Wilke.*)


### Notas de la versión v1.13 {#v113-release-notes}

*Archivado paralelo, stanza-create, info y check mejorados*

*Publicada el 5 de febrero de 2017*

**NOTA IMPORTANTE**: La nueva implementación del archivado asincrónico ya no copia el WAL a una cola separada. Si queda WAL en la cola antigua después de actualizar a `1.13`, será abandonado y **no** se enviará al repositorio. Para evitar este resultado, detén el archivado estableciendo `archive_command = false`. A continuación, vacía la cola asincrónica ejecutando `pgbackrest --stanza=[stanza-name] archive-push` y espera a que el proceso se complete. Comprueba que la cola en `[spool-path]/archive/[stanza-name]/out` esté vacía. Finalmente, instala `1.13` y restaura el `archive_command` original. **NOTA IMPORTANTE**: El comando `stanza-create` ya no es opcional y debe ejecutarse antes de que se puedan realizar copias de seguridad o archivado en una stanza **nueva**. Las stanzas preexistentes no requieren que se ejecute `stanza-create`.

**Correcciones de errores:**

- Corregida una asignación const que generaba una advertencia del compilador en la biblioteca C. (*Corregido por Adrian Vondendriesch. Revisado por David Steele.*)
- Corregidas algunas sincronizaciones de directorios que se pasaron por alto para la opción `--repo-sync`.
- Corregido un problema por el que un usuario/grupo faltante en la restauración podía causar un error de «uninitialized value» en `File->owner()`. (*Reportado por Leonardo GG Avellar.*)
- Corregido un problema por el que los errores de discrepancia de protocolo no mostraban el valor esperado.
- Corregido un mensaje de registro espurio de `archive-get` que indicaba que un código de salida 1 era una terminación anormal.

**Funcionalidades:**

- Implementación mejorada y multiproceso del archivado asincrónico.
- Mejorado el comando `stanza-create` para que pueda reparar repositorios rotos en la mayoría de los casos y sea lo suficientemente robusto para hacerse obligatorio. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Mejorado el comando `check` para ejecutarse en una réplica, aunque solo se hacen comprobaciones básicas porque `pg_switch_xlog()` no puede ejecutarse en una réplica. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadidos los rangos de WAL de archivado y de copia de seguridad al comando `info`.
- Añadida una advertencia para actualizar `pg_tablespace.spclocation` al remapear tablespaces en PostgreSQL < 9.2. (*Contribución de blogh. Revisado por David Steele.*)
- Eliminar los requisitos de bloqueo remoto para los comandos `archive-get`, `restore`, `info` y `check` ya que son operaciones de solo lectura. (*Sugerido por Michael Vitale.*)

**Mejoras:**

- El banner del archivo de registro no se emite hasta que se escribe la primera entrada de registro. (*Sugerido por Jens Wilke.*)
- Reducida la probabilidad de que las páginas escritas parcialmente causen un falso positivo en las sumas de verificación de páginas filtrando por el LSN de inicio de la copia de seguridad.
- Eliminar la optimización específica de Intel de las banderas de compilación de la biblioteca C. (*Contribución de Adrian Vondendriesch. Revisado por David Steele.*)
- Eliminar la opción `--lock`. Esta opción se introdujo antes de que el directorio de bloqueo pudiera ubicarse fuera del repositorio y ahora es obsoleta.
- Añadida la opción `--log-timestamp` para permitir suprimir las marcas de tiempo en el registro. Se usa principalmente para evitar filtros en la documentación automatizada.
- Devolver el código de error apropiado cuando no se pueda convertir una ruta relativa en una ruta absoluta. (*Sugerido por Yogesh Sharma.*)

**Funcionalidades de la documentación:**

- Añadida documentación a la guía de usuario para la opción `process-max`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.12 {#v112-release-notes}

*Sumas de verificación de páginas, configuración y correcciones de errores*

*Publicada el 12 de diciembre de 2016*

**NOTA IMPORTANTE**: En versiones anteriores era posible especificar en la línea de comandos opciones que eran inválidas para el comando actual sin obtener un error. Ahora se generará un error para las opciones inválidas, por lo que es importante revisar cuidadosamente las opciones de línea de comandos en tu entorno para prevenir interrupciones.

**Correcciones de errores:**

- Corregido un problema por el que se podían proporcionar en la línea de comandos opciones inválidas para el comando especificado sin generar un error. Las opciones se ignoraban y no causaban ningún cambio de comportamiento, pero sí generaban algo de confusión. Las opciones inválidas ahora generarán un error. (*Reportado por Nikhilchandra Kulkarni.*)
- Corregido un problema por el que no se creaban los enlaces simbólicos internos para los tablespaces en el repositorio. Este problema solo era visible al intentar levantar clústeres en el lugar manualmente usando instantáneas del sistema de archivos y no afectaba a la copia de seguridad y restauración normales.
- Corregido un problema que impedía que los errores se mostraran por consola antes de que el sistema de registro se inicializara, es decir, durante el análisis de opciones. Los códigos de error se seguían devolviendo con precisión, por lo que esto no habría hecho parecer que un proceso tuvo éxito cuando no fue así. (*Reportado por Adrian Vondendriesch.*)
- Corregido un problema por el que la opción `db-port` especificada en el servidor de copia de seguridad no se pasaba correctamente al remoto a menos que fuera de la primera base de datos configurada. (*Reportado por Michael Vitale.*)

**Funcionalidades:**

- Añadida la opción `--checksum-page` para permitir que pgBackRest valide las sumas de verificación de páginas en los archivos de datos cuando las sumas de verificación están habilitadas en PostgreSQL >= 9.3. Ten en cuenta que esta funcionalidad requiere una biblioteca C que puede que inicialmente no esté disponible en los paquetes del sistema operativo. La opción se habilitará automáticamente cuando la biblioteca esté presente y las sumas de verificación estén habilitadas en el clúster. (*Sugerido por Stephen Frost.*)
- Añadida la opción `--repo-link` para permitir suprimir los enlaces simbólicos internos cuando el repositorio se encuentra en un sistema de archivos que no soporta enlaces simbólicos. Esto no afecta ninguna funcionalidad de pgBackRest, pero el enlace de conveniencia `latest` no se creará, y tampoco los enlaces simbólicos internos de tablespaces, lo que afectará la capacidad de levantar clústeres en el lugar manualmente usando instantáneas del sistema de archivos.
- Añadida la opción `--repo-sync` para permitir deshabilitar las sincronizaciones de directorios en el repositorio para sistemas de archivos que no las soportan, p. ej. NTFS.
- Añadida una entrada de registro predecible para señalar que un comando ha finalizado con éxito. Por ejemplo, una copia de seguridad termina con éxito con: `INFO: backup command end: completed successfully`. (*Sugerido por Jens Wilke.*)

**Mejoras:**

- Por simplicidad, el archivo `pg_control` ahora se copia junto con el resto de los archivos en lugar de por sí solo al final del proceso. El comando `backup` no requiere este comportamiento y `restore` copia a un archivo temporal que se renombra al final de la restauración.

**Correcciones de errores en la documentación:**

- Corregido un problema que suprimía excepciones en las compilaciones PDF.
- Corregida una regresión en los enlaces de sección introducida en v1.10.

**Funcionalidades de la documentación:**

- Añadida la retención a la sección de inicio rápido.


### Notas de la versión v1.11 {#v111-release-notes}

*Corrección para la eficiencia del archivado asincrónico*

*Publicada el 17 de noviembre de 2016*

**Correcciones de errores:**

- Corregido un problema por el que el archivado asincrónico transfería un archivo por ejecución en lugar de transferir archivos por lotes. Esta regresión fue introducida en v1.09 y afectó únicamente a la eficiencia; todos los segmentos WAL se archivaron correctamente en modo asincrónico. (*Reportado por Stephen Frost.*)


### Notas de la versión v1.10 {#v110-release-notes}

*Creación de stanzas y correcciones menores*

*Publicada el 8 de noviembre de 2016*

**Correcciones de errores:**

- Corregido un problema por el que una copia de seguridad podía dar error si no se hicieron cambios a una base de datos entre copias y solo cambió `pg_control`.
- Corregido un problema por el que rutas de tablespaces con el mismo prefijo causaban un error de enlace inválido. (*Reportado por Nikhilchandra Kulkarni.*)

**Funcionalidades:**

- Añadido el comando `stanza-create` para formalizar la creación de stanzas en el repositorio. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras:**

- Eliminadas las directivas `use lib` superfluas de los módulos Perl. (*Sugerido por Devrim Gündüz.*)


### Notas de la versión v1.09 {#v109-release-notes}

*Soporte de 9.6, configurabilidad y correcciones de errores*

*Publicada el 10 de octubre de 2016*

**Correcciones de errores:**

- Corregido el comando `check` para evitar que se registre un mensaje de error si el directorio de copia de seguridad no existe. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Corregido el mensaje de error para mostrar correctamente el comando de archivado cuando se detecta un comando de archivado inválido. (*Reportado por Jason O'Donnell.*)
- Corregido un problema por el que el archivador asincrónico no se iniciaría si `archive-push` no tenía espacio suficiente para poner en cola un nuevo segmento WAL. Esto significaba que la cola nunca se vaciaría sin intervención manual (como llamar a `archive-push` directamente). PostgreSQL ahora recibe errores cuando no hay espacio suficiente para almacenar nuevos segmentos WAL, pero el proceso asincrónico se seguirá iniciando para que el espacio se libere eventualmente. (*Reportado por Jens Wilke.*)
- Corregido un tiempo de espera agotado del remoto que ocurría cuando un proceso local generaba sumas de verificación (durante una reanudación o restauración) pero no copiaba archivos, lo que permitía que el remoto quedara inactivo. (*Reportado por Jens Wilke.*)

**Funcionalidades:**

- Las copias de seguridad no exclusivas se usarán automáticamente en PostgreSQL 9.6.
- Añadida la opción `cmd-ssh` para permitir especificar el cliente ssh. (*Sugerido por Jens Wilke.*)
- Añadida la opción `log-level-stderr` para controlar si los mensajes de registro de consola se envían a `stderr` o a `stdout`. Por defecto está establecida en `warn`, lo que representa un cambio de comportamiento respecto a versiones anteriores, aunque puede ser más intuitivo. Establecer `log-level-stderr=off` conservará el comportamiento antiguo. (*Sugerido por Sascha Biberhofer.*)
- Establecer `application_name` en `"pgBackRest [command]"` para las conexiones a la base de datos. (*Sugerido por Jens Wilke.*)
- Comprobar que archive_mode está habilitado cuando la opción `archive-check` está habilitada.

**Mejoras:**

- Aclarado el mensaje de error cuando no se puede adquirir el bloqueo consultivo de pgBackRest para dejar claro que no es un bloqueo de copia de seguridad de PostgreSQL. (*Sugerido por Jens Wilke.*)
- Número de versión de pgBackRest incluido en la salida de registro INFO de inicio de comando.
- ID de proceso registrado en la salida de registro INFO de inicio/parada del proceso local.

**Funcionalidades de la documentación:**

- Añadida la documentación de la opción `archive-timeout` a la guía de usuario. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.08 {#v108-release-notes}

*Correcciones de errores y mejoras de registro*

*Publicada el 14 de septiembre de 2016*

**Correcciones de errores:**

- Corregido un problema por el que los procesos locales no se desconectaban al completarse y podían agotar su tiempo de espera más tarde. (*Reportado por Todd Vernick.*)
- Corregido un problema por el que la capa de protocolo podía agotar su tiempo de espera mientras esperaba que llegaran segmentos WAL al archivado. (*Reportado por Todd Vernick.*)

**Mejoras:**

- Almacenar en caché la salida del registro de archivo hasta que se cree el archivo para generar un registro más completo.


### Notas de la versión v1.07 {#v107-release-notes}

*Conversión de hilos a procesos y correcciones de errores*

*Publicada el 7 de septiembre de 2016*

**Correcciones de errores:**

- Corregido un problema por el que los tablespaces se copiaban desde el primario durante una copia de seguridad desde réplica.
- Corregido el comando `check` para que la información de la copia de seguridad se compruebe remotamente y no solo localmente. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Corregido un problema por el que `retention-archive` no se establecía automáticamente cuando `retention-archive-type=diff`, lo que resultaba en una expiración del archivado menos agresiva de lo previsto. (*Corregido por Cynthia Shang. Revisado por David Steele.*)

**Funcionalidades:**

- Convertidos los hilos de Perl a procesos para mejorar la compatibilidad y el rendimiento.
- Excluir el contenido del directorio `$PGDATA/pg_replslot` para que los slots de replicación del primario no formen parte de la copia de seguridad.
- Los ajustes `archive-start` y `archive-stop` ahora se completan en `backup.manifest` incluso cuando `archive-check=n`. (*Sugerido por Jens Wilke.*)
- Advertencias adicionales cuando los ajustes de retención del archivado pueden no tener el efecto previsto o permitirían una retención indefinida. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Soporte experimental para copias de seguridad no exclusivas en PostgreSQL 9.6 rc1. Los cambios en las versiones de control/catálogo/WAL en candidatos de versión posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.

**Correcciones de errores en la documentación:**

- Corregidos problemas menores de reproducibilidad de la documentación relacionados con rutas de binarios.

**Funcionalidades de la documentación:**

- Documentación para la retención del archivado. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.06 {#v106-release-notes}

*Copia de seguridad desde una réplica y correcciones de errores*

*Publicada el 25 de agosto de 2016*

**Correcciones de errores:**

- Corregido un problema por el que un enlace de tablespace que referenciaba a otro enlace no producía un error, sino que omitía el tablespace por completo. (*Reportado por Michael Vitale.*)
- Corregido un problema por el que las opciones que no deberían permitir múltiples valores podían especificarse varias veces en `pgbackrest.conf` sin que se generara un error. (*Reportado por Michael Vitale.*)
- Corregido un problema por el que la opción `protocol-timeout` no se aumentaba automáticamente cuando se aumentaba la opción `db-timeout`. (*Reportado por Todd Vernick.*)

**Funcionalidades:**

- Copia de seguridad desde un clúster réplica. Aún se requiere una conexión al clúster primario para iniciar/detener la copia de seguridad y copiar los archivos que no se replican, pero la gran mayoría de los archivos se copian desde la réplica para reducir la carga en el primario.
- Configuración más flexible para las bases de datos. El maestro y la réplica pueden configurarse ambos en el servidor de copia de seguridad y pgBackRest determinará automáticamente cuál es el primario. Esto significa que no se requieren cambios de configuración para la copia de seguridad tras una conmutación por error de primario a réplica cuando se usa un servidor de copia de seguridad separado.
- Excluir durante la copia de seguridad los directorios que PostgreSQL limpia, recrea o pone a cero al iniciar. Estos incluyen `pgsql_tmp` y `pg_stat_tmp`. El archivo `postgresql.auto.conf.tmp` ahora se excluye además de los archivos que ya estaban excluidos: `backup_label.old`, `postmaster.opts`, `postmaster.pid`, `recovery.conf`, `recovery.done`.
- Soporte experimental para copias de seguridad no exclusivas en PostgreSQL 9.6 beta4. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.

**Mejoras:**

- Mejorar el mensaje de error para enlaces que referencian enlaces en la construcción del manifiesto.
- Añadidas sugerencias al mensaje de error cuando se detectan rutas relativas en `archive-push` o `archive-get`.
- Mejorar los mensajes de registro de la copia de seguridad para indicar desde qué host se están copiando los archivos.


### Notas de la versión v1.05 {#v105-release-notes}

*Corrección para la comprobación de enlaces de tablespaces*

*Publicada el 9 de agosto de 2016*

**Correcciones de errores:**

- Corregido un problema por el que las rutas de tablespaces que tenían $PGDATA como subcadena se identificaban como subdirectorios de $PGDATA incluso cuando no lo eran. También se endureció un poco la comprobación de rutas relativas. (*Reportado por Chris Fort.*)

**Funcionalidades de la documentación:**

- Añadida documentación para programar copias de seguridad con cron. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

**Mejoras en la documentación:**

- Movido el backlog del sitio web de pgBackRest al wiki del repositorio de GitHub. (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.04 {#v104-release-notes}

*Varias correcciones de errores*

*Publicada el 30 de julio de 2016*

**Correcciones de errores:**

- Corregido un problema por el que se creaba un remoto superfluo que hacía que la copia de seguridad/restauración con hilos pudiera agotar el tiempo de espera y/o lanzar un conflicto de bloqueo. (*Reportado por Michael Vitale.*)
- Corregido un problema por el que db-path no era requerido para el comando `check`, de modo que se lanzaba un assert cuando faltaba en lugar de un mensaje de error cortés. (*Reportado por Michael Vitale.*)
- Corregido el comando `check` para lanzar un error cuando la versión/id de la base de datos no coincide con la del archivado. (*Corregido por Cynthia Shang. Revisado por David Steele.*)
- Corregido un problema por el que un remoto podía intentar iniciar su propio remoto cuando la opción `backup-host` no estaba presente en `pgbackrest.conf` en el servidor de bases de datos. (*Reportado por Lardière Sébastien.*)
- Corregido un problema por el que el contenido de `pg_xlog` se respaldaba si el directorio era un enlace simbólico. Esto no causaba problemas durante la restauración, pero era un desperdicio de espacio.
- Corregida una llamada inválida a `log()` en las rutinas de bloqueo.

**Funcionalidades:**

- Soporte experimental para copias de seguridad no exclusivas en PostgreSQL 9.6 beta3. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.

**Mejoras:**

- Suprimir los banners en las conexiones del protocolo SSH.
- Mejorados los mensajes de error remotos para identificar el host donde se generó el error.
- Todos los tipos de remotos ahora toman bloqueos. Las excepciones datan de cuando el arnés de pruebas y pgBackRest se ejecutaban en la misma VM y ya no aplican.

**Funcionalidades de la documentación:**

- Añadida una aclaración sobre por qué el valor por defecto de la opción `backrest-user` es `backrest`. (*Sugerido por Michael Vitale.*)
- Actualizada la información sobre la disponibilidad de paquetes en las plataformas soportadas. (*Sugerido por Michael Vitale.*)


### Notas de la versión v1.03 {#v103-release-notes}

*Comando check y correcciones de errores*

*Publicada el 2 de julio de 2016*

**Correcciones de errores:**

- Corregido un problema por el que los `keep-alives` podían verse desplazados por muchos archivos pequeños durante `backup` multihilo. También estaban completamente ausentes de la reanudación de `backup` mono/multihilo y del cálculo de sumas de verificación de `restore`. (*Reportado por Janice Parkinson, Chris Barber.*)
- Corregido un problema por el que el comando `expire` se negaba a ejecutarse cuando se lo llamaba explícitamente desde la línea de comandos si la opción `db-host` estaba establecida. Esto no era un problema cuando `expire` se ejecutaba automáticamente después de un `backup` (*Reportado por Chris Barber.*)
- Corregido un problema por el que se ejecutaba validación sobre archive_command incluso cuando la opción `archive-check` estaba deshabilitada.

**Funcionalidades:**

- Añadido el comando `check` para validar que pgBackRest está configurado correctamente para el archivado y las copias de seguridad. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Añadida la opción `protocol-timeout`. Anteriormente `protocol-timeout` se establecía como `db-timeout` + 30 segundos.
- El fallo al apagar los remotos al final de la copia de seguridad ya no lanza una excepción. En su lugar se genera una advertencia que recomienda un `protocol-timeout` mayor.
- Soporte experimental para copias de seguridad no exclusivas en PostgreSQL 9.6 beta2. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.

**Mejoras:**

- Mejorado el manejo de usuarios/grupos capturados durante la copia de seguridad que no existen en el host de restauración. También se maneja explícitamente el caso en que el usuario/grupo no está mapeado a un nombre.
- El manejo de opciones ahora es mucho más estricto. Anteriormente era posible que un comando usara una opción que no le estaba explícitamente asignada. Esto era especialmente cierto para las opciones `backup-host` y `db-host`, que se usan para determinar la localidad.

**Mejoras en la documentación:**

- Permitir que se use una fecha estática para la documentación a fin de generar compilaciones reproducibles. (*Sugerido por Adrian Vondendriesch.*)
- Añadida documentación sobre el archivado asincrónico a la guía de usuario. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- La ubicación de instalación recomendada para los módulos de pgBackRest ahora es `/usr/share/perl5` ya que `/usr/lib/perl5` fue eliminada de la ruta de búsqueda en versiones más nuevas de Perl.
- Añadidas instrucciones para eliminar versiones anteriores de pgBackRest.


### Notas de la versión v1.02 {#v102-release-notes}

*Corrección para Perl 5.22*

*Publicada el 2 de junio de 2016*

**Correcciones de errores:**

- Corregir el uso de sprintf() debido a nuevas restricciones en Perl 5.22. Ya no se permiten parámetros no referenciados en la cadena de formato. (*Corregido por Adrian Vondendriesch. Revisado por David Steele.*)

**Correcciones de errores en la documentación:**

- Corregida una sintaxis que no era compatible con Perl 5.2X. (*Corregido por Christoph Berg, Adrian Vondendriesch. Revisado por David Steele.*)
- Corregidas las rutas absolutas que se usaban para el logo del PDF. (*Reportado por Adrian Vondendriesch.*)

**Funcionalidades de la documentación:**

- Las notas de versión ahora se dividen en secciones para que los errores, las funcionalidades y las refactorizaciones estén claramente delimitados. Se ha añadido una sección «Notas adicionales» para los cambios en la documentación y la suite de pruebas que no afectan al código principal.
- Añadida la generación de páginas de manual. (*Contribución de Adrian Vondendriesch, David Steele.*)
- El registro de cambios fue la última pieza de la documentación en renderizarse solo en Markdown. Se escribió un conversor para que el documento pueda producirse con los renderizadores estándar. El registro de cambios ahora estará ubicado en el sitio web y ha sido renombrado a «Releases». (*Contribución de Cynthia Shang. Revisado por David Steele.*)


### Notas de la versión v1.01 {#v101-release-notes}

*Info mejorado, restauración selectiva y soporte de 9.6*

*Publicada el 17 de mayo de 2016*

**Funcionalidades:**

- Mejorada la salida de texto del comando `info` para incluir marcas de tiempo, tamaños y la lista de referencias de todas las copias de seguridad. (*Contribución de Cynthia Shang. Revisado por David Steele.*)
- Permitir la restauración selectiva de bases de datos desde una copia de seguridad del clúster. Esta funcionalidad puede generar grandes ahorros de espacio y tiempo cuando solo se restauran bases de datos específicas. Las bases de datos no restauradas no serán accesibles, pero deben eliminarse manualmente antes de que se quiten del catálogo compartido. (*Revisado por Cynthia Shang, Greg Smith, Stephen Frost. Sugerido por Stephen Frost.*)
- Soporte experimental para copias de seguridad no exclusivas en PostgreSQL 9.6 beta1. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo. (*Revisado por Cynthia Shang.*)


### Notas de la versión v1.00 {#v100-release-notes}

*Nuevo formato de repositorio y esquema de configuración, soporte de enlaces*

*Publicada el 14 de abril de 2016*

**NOTA IMPORTANTE**: Esta versión «flag day» rompe la compatibilidad con versiones anteriores de pgBackRest. El formato del manifiesto, la estructura en disco, el esquema de configuración y los nombres de ejecutable/ruta han cambiado. Debes crear un repositorio nuevo para almacenar las copias de seguridad de esta versión de pgBackRest y conservar tu repositorio anterior por un tiempo en caso de que necesites hacer una restauración. Las restauraciones desde el repositorio anterior requerirán la versión anterior de pgBackRest, pero debido a los cambios de nombre es posible tener instalados `1.00` y una versión anterior de pgBackRest al mismo tiempo. Consulta las notas siguientes para obtener información más detallada sobre lo que ha cambiado.

**Funcionalidades:**

- Implementado un nuevo esquema de configuración que debería ser mucho más simple de usar. Consulta la guía de usuario y la referencia de configuración para más detalles, pero para una configuración simple ahora todas las opciones pueden colocarse en la sección de la `stanza`. Las opciones compartidas entre stanzas pueden colocarse en la sección `[global]`. Las configuraciones más complejas aún pueden hacer uso de secciones de comandos, aunque esto debería ser un caso de uso raro. (*Sugerido por Michael Renner.*)
- La opción `repo-path` ahora siempre se refiere al repositorio donde se almacenan las copias de seguridad y el archivado, sea local o remoto, por lo que la opción `repo-remote-path` ha sido eliminada. La nueva opción `spool-path` puede usarse para definir una ubicación para poner en cola segmentos WAL al archivar asincrónicamente. Ya no se requiere un repositorio local.
- El nombre del archivo de configuración por defecto ahora es `pgbackrest.conf` en lugar de `pg_backrest.conf`. Esto se hizo por consistencia con otros cambios de nomenclatura, pero también para evitar que los archivos de configuración antiguos se carguen accidentalmente al migrar a `1.00`. (*Sugerido por Michael Renner, Stephen Frost.*)
- El nombre del repositorio por defecto se cambió de `/var/lib/backup` a `/var/lib/pgbackrest`. (*Sugerido por Michael Renner, Stephen Frost.*)
- Los archivos de bloqueo ahora se almacenan por defecto en `/tmp/pgbackrest`. Hoy en día `/run/pgbackrest` es la ubicación preferida, pero eso requeriría scripts de init que no forman parte de esta versión. La opción `lock-path` puede usarse para configurar el directorio de bloqueo.
- Los archivos de registro ahora se almacenan por defecto en `/var/log/pgbackrest` y ya no tienen la fecha añadida, de modo que pueden gestionarse con `logrotate`. La opción `log-path` puede usarse para configurar el directorio de registro. (*Sugerido por Stephen Frost.*)
- El nombre del archivo ejecutable cambió de `pg_backrest` a `pgbackrest`. (*Sugerido por Michael Renner, Stephen Frost.*)
- Todos los archivos y directorios enlazados desde PGDATA ahora se incluyen en la copia de seguridad. Por defecto, los enlaces se restaurarán directamente en PGDATA como archivos o directorios. La opción `--link-all` puede usarse para restaurar todos los enlaces a sus ubicaciones originales. La opción `--link-map` puede usarse para remapear un enlace a una nueva ubicación.
- Eliminada la opción `--tablespace` y reemplazada por la opción `--tablespace-map-all`, que debería indicar su función con mayor claridad.
- Añadido el nivel de registro `detail`, que mostrará más información que `info` sin ser tan verboso como `debug`.


--------

## Versiones previas a la estabilización {#pre-stable-releases}


### Notas de la versión v0.92 {#v092-release-notes}

*Corrección de la ruta de repositorio en la línea de comandos*

*Publicada el 6 de abril de 2016*

**Correcciones de errores:**

- Corregido un problema por el que el proceso maestro pasaba `--repo-remote-path` en lugar de `--repo-path` al remoto, causando que los archivos de bloqueo se crearan en el directorio de repositorio por defecto (`/var/lib/backup`), generalmente terminando en fallo. Esto solo era un problema cuando `--repo-remote-path` se definía en la línea de comandos en lugar de en `pg_backrest.conf`. (*Reportado por Jan Wieck.*)


### Notas de la versión v0.91 {#v091-release-notes}

*Corrección de error de tablespaces y mejoras menores*

*Publicada el 22 de marzo de 2016*

**CORRECCIÓN IMPORTANTE DE ERROR PARA TABLESPACES**: Un cambio en el formato del repositorio se introdujo accidentalmente en 0.90, lo que significa que la copia de seguridad en disco ya no era un clúster de PostgreSQL válido cuando la copia contenía tablespaces. Esto solo afectó a los usuarios que copiaban directamente las copias de seguridad para restaurar clústeres de PostgreSQL en lugar de usar el comando restore. Sin embargo, la corrección rompe la compatibilidad con copias de seguridad antiguas que contienen tablespaces, sin importar cómo se estén restaurando (pgBackRest lanzará errores y se negará a restaurar). Deben tomarse nuevas copias de seguridad completas inmediatamente después de instalar la versión 0.91 para cualquier clúster que contenga tablespaces. Si es necesario restaurar copias de seguridad antiguas, usa una versión de pgBackRest que coincida con la versión de la copia de seguridad.

**Correcciones de errores:**

- Corregida la incompatibilidad de repositorio introducida en pgBackRest 0.90. (*Reportado por Evan Benoit.*)

**Funcionalidades:**

- Copiar `global/pg_control` al final durante las copias de seguridad.
- Escribir los archivos `.info` y `.manifest` en temporales antes de moverlos a sus ubicaciones finales y aplicar fsync.
- Renombrar la opción `--no-start-stop` a `--no-online`.

**Funcionalidades de la suite de pruebas:**

- Análisis estático de código fuente usando Perl-Critic; actualmente pasa en el nivel gentle.


### Notas de la versión v0.90 {#v090-release-notes}

*Soporte de 9.5, varias mejoras y correcciones menores de errores*

*Publicada el 7 de febrero de 2016*

**Correcciones de errores:**

- Corregido un problema por el que especificar `--no-archive-check` lanzaba un error de configuración. (*Reportado por Jason O'Donnell.*)
- Corregido un problema por el que un archivo WAL temporal remanente tras un fallo del sistema ocurrido en un momento preciso podía hacer fallar el siguiente `archive-push`.
- La opción `retention-archive` ahora puede establecerse con seguridad a un valor menor que la retención de copias de seguridad (`retention-full` o `retention-diff`) sin especificar también `archive-copy=n`. El WAL requerido para que las copias de seguridad que quedan fuera de la retención de archivado sean consistentes se preservará en el archivado. Sin embargo, en este caso la PITR no será posible para las copias de seguridad que quedan fuera de la retención de archivado.

**Funcionalidades:**

- Al respaldar y restaurar tablespaces, pgBackRest solo opera en el subdirectorio creado para la versión de PostgreSQL contra la que se ejecuta. Dado que múltiples versiones pueden convivir en un tablespace (especialmente durante una actualización binaria), esto evita que se copien demasiados archivos durante una copia de seguridad y que otras versiones sean borradas durante una restauración. Esto solo aplica a PostgreSQL >= 9.0; las versiones anteriores de PostgreSQL no podían compartir un directorio de tablespace.
- Generar un error cuando `archive-check=y` pero `archive_command` no ejecuta `pg_backrest`. (*Contribución de Jason O'Donnell. Revisado por David Steele.*)
- Mejorado el mensaje de error cuando `repo-path` o `repo-remote-path` no existe.
- Añadidas comprobaciones para las opciones de restauración `--delta` y `--force` para asegurar que el destino sea un directorio $PGDATA válido. pgBackRest comprobará la presencia de `PG_VERSION` o `backup.manifest` (remanente de una restauración abortada). Si no se encuentra ninguno de los dos archivos, `--delta` y `--force` se deshabilitarán, pero la restauración continuará a menos que haya archivos en el directorio $PGDATA (o en cualquier directorio de tablespace), en cuyo caso la operación se abortará.
- Cuando se usa restore `--set=latest` (el valor por defecto), la copia de seguridad restaurada realmente se mostrará en el registro.
- Soporte para segmentos WAL parciales de PostgreSQL 9.5 y el ajuste `recovery_target_action`. El ajuste `archive_mode = 'always'` aún no está soportado.
- Soporte para el ajuste de recuperación `recovery_target = 'immediate'` introducido en PostgreSQL 9.4.
- Se han añadido las siguientes comprobaciones de tablespaces: rutas o archivos en pg_tblspc, enlaces relativos en pg_tblspc, tablespaces en $PGDATA. Las tres generarán errores.


### Notas de la versión v0.89 {#v089-release-notes}

*Corrección de tiempo de espera y restauración en repositorios de solo lectura*

*Publicada el 24 de diciembre de 2015*

**Correcciones de errores:**

- Corregido un problema por el que las copias de seguridad/restauraciones de larga duración agotaban el tiempo de espera cuando eran remotas y con hilos. Ahora se usan keepalives para asegurar que el remoto del proceso principal no agote su tiempo de espera mientras los remotos de los hilos hacen todo el trabajo. El mensaje de error para los tiempos de espera agotados también se mejoró para facilitar la depuración. (*Reportado por Stephen Frost.*)

**Funcionalidades:**

- Permitir que las restauraciones se realicen en un repositorio de solo lectura usando `--no-lock` y `--log-level-file=off`. La opción `--no-lock` solo puede usarse con restauraciones.


### Notas de la versión v0.88 {#v088-release-notes}

*Documentación y correcciones menores de errores*

*Publicada el 22 de noviembre de 2015*

**Correcciones de errores:**

- Corregido un problema por el que los comandos `start`/`stop` requerían la opción `--config`. (*Reportado por Dmitry Didovicher.*)
- Corregido un problema por el que los archivos de registro se sobrescribían en lugar de añadirse. (*Reportado por Stephen Frost, Dmitry Didovicher.*)
- Corregido un problema por el que `backup-user` no era opcional.

**Funcionalidades:**

- Ya no se crean enlaces simbólicos en los directorios de copia de seguridad del repositorio. Estos enlaces simbólicos podían apuntar prácticamente a cualquier parte y ser potencialmente peligrosos. Los enlaces simbólicos todavía se recrean durante una restauración. (*Sugerido por Stephen Frost.*)
- Añadidos mejores mensajes para la expiración de copias de seguridad. Las expiraciones de copias de seguridad completas y diferenciales se registran en una sola línea junto con una lista de todas las copias dependientes expiradas.
- La retención del archivado se establece automáticamente a la retención de copias de seguridad completas si no se configura explícitamente.

**Funcionalidades de la documentación:**

- Añadida documentación en la guía de usuario para restauraciones delta, expiración, hosts dedicados de copia de seguridad, inicio y detención de pgBackRest, y replicación.


### Notas de la versión v0.87 {#v087-release-notes}

*Sitio web y guía de usuario*

*Publicada el 28 de octubre de 2015*

**Funcionalidades:**

- Los archivos `backup_label.old` y `recovery.done` ahora se excluyen de las copias de seguridad.

**Funcionalidades de la documentación:**

- Añadida una nueva guía de usuario que cubre lo básico de pgBackRest y algunos temas avanzados incluyendo PITR. Queda mucho por venir, pero es un comienzo. (*Contribución de David Steele, Stephen Frost. Revisado por Michael Renner, Cynthia Shang, Eric Radman, Dmitry Didovicher.*)


### Notas de la versión v0.85 {#v085-release-notes}

*Comandos start/stop y correcciones menores de errores*

*Publicada el 8 de octubre de 2015*

**Correcciones de errores:**

- Corregido un problema por el que podía devolverse un error después de una copia de seguridad o restauración completamente exitosa.
- Corregido un problema por el que una reanudación fallaría si quedaban archivos temporales en el directorio raíz de la copia de seguridad cuando la copia fallaba. Este escenario era probable si el proceso de copia de seguridad terminaba abruptamente durante la fase de copia.

**Funcionalidades:**

- Añadidos los comandos `stop` y `start` para evitar que se ejecuten procesos de pgBackRest en un sistema donde PostgreSQL está apagado o el sistema necesita ponerse en reposo por alguna otra razón.
- Soporte experimental para PostgreSQL 9.5 beta1. Esto puede romperse cuando cambie la versión de control o el número mágico del WAL en versiones futuras, pero se actualizará en cada versión de pgBackRest para mantener el ritmo. Todas las pruebas de regresión pasan excepto las pruebas de `--target-resume` (esta funcionalidad ha cambiado en 9.5) y aún no hay pruebas para segmentos WAL `.partial`.


### Notas de la versión v0.82 {#v082-release-notes}

*Refactorización, ayuda de línea de comandos y correcciones menores de errores*

*Publicada el 14 de septiembre de 2015*

**Correcciones de errores:**

- Corregido un problema por el que las copias de seguridad comprimidas reanudadas no preservaban los archivos existentes.
- Corregido un problema por el que la reanudación y las copias incr/diff no aseguraban que la copia de seguridad anterior tuviera los mismos ajustes de compresión y de enlace duro.
- Corregido un problema por el que una copia de seguridad en frío usando `--no-start-stop` podía iniciarse en un clúster de PostgreSQL en ejecución sin especificar `--force`.
- Corregido un problema por el que se podía iniciar un hilo incluso cuando no se solicitó ninguno.
- Corregido un problema por el que el número de versión de pgBackRest no se actualizaba en `backup.info` y `archive.info` después de una actualización/degradación.
- Corregido un problema por el que el comando `info` lanzaba una excepción cuando el repositorio no contenía stanzas. (*Reportado por Stephen Frost.*)
- Corregido un problema por el que los NOTICE de `pg_stop_backup()` de PostgreSQL se enviaban a `stderr`. (*Reportado por Stephen Frost.*)

**Funcionalidades:**

- Soporte experimental para PostgreSQL 9.5 alpha2. Esto puede romperse cuando cambie la versión de control o el número mágico del WAL en versiones futuras, pero se actualizará en cada versión de pgBackRest para mantener el ritmo. Todas las pruebas de regresión pasan excepto las pruebas de `--target-resume` (esta funcionalidad ha cambiado en 9.5) y aún no hay pruebas para segmentos WAL `.partial`.

**Mejoras:**

- Renombrada la opción y sección `recovery-setting` a `recovery-option` para ser más consistente con las convenciones de nomenclatura de pgBackRest.
- Añadida la carga dinámica de módulos para acelerar los comandos, especialmente el archivado asincrónico.

**Funcionalidades de la documentación:**

- La ayuda de línea de comandos ahora se extrae de la misma fuente XML que se usa para el resto de la documentación e incluye mucho más detalle.


### Notas de la versión v0.80 {#v080-release-notes}

*Soporte de DBI, estabilidad y funcionalidades de conveniencia*

*Publicada el 9 de agosto de 2015*

**Correcciones de errores:**

- Corregido un problema que hacía que la marca de tiempo formateada tanto de la copia más antigua como de la más nueva se reportara como la hora actual por el comando `info`. Solo la salida `text` estaba afectada; la salida `json` reportaba los valores de epoch correctos. (*Reportado por Michael Renner.*)
- Corregido un problema de protocolo que impedía que los errores de ssh (especialmente en la conexión) se registraran.

**Funcionalidades:**

- El repositorio ahora se crea y actualiza con modos de directorio y de archivo consistentes. Por defecto, `umask` se establece en `0000`, pero esto puede deshabilitarse con el ajuste `neutral-umask`. (*Sugerido por Cynthia Shang.*)
- Añadida la opción `stop-auto` para permitir que las copias de seguridad fallidas se detengan automáticamente cuando comienza una nueva copia.
- Añadida la opción `db-timeout` para limitar el tiempo que pgBackRest esperará a que `pg_start_backup()` y `pg_stop_backup()` devuelvan.
- Eliminar el archivo `pg_control` al comienzo de la restauración y copiarlo de vuelta al final. Esto evita la posibilidad de que PostgreSQL arranque un clúster restaurado parcialmente.
- Añadidas comprobaciones para asegurar que el ajuste `db-path` es consistente con `db-port`, comparando el `data_directory` reportado por el clúster contra el ajuste `db-path` y la versión reportada por el clúster contra el valor leído de `pg_control`. Se comprueba que el ajuste `db-socket-path` sea una ruta absoluta.
- Soporte experimental para PostgreSQL 9.5 alpha1. Esto puede romperse cuando cambie la versión de control o el número mágico del WAL en versiones futuras, pero se actualizará en cada versión de pgBackRest para mantener el ritmo. Todas las pruebas de regresión pasan excepto las pruebas de `--target-resume` (esta funcionalidad ha cambiado en 9.5) y aún no hay pruebas para segmentos WAL `.partial`.

**Mejoras:**

- Ahora se usa `DBI` y `DBD::Pg` de Perl para las conexiones a PostgreSQL en lugar de `psql`. Los ajustes `cmd-psql` y `cmd-psql-option` han sido eliminados y reemplazados por `db-port` y `db-socket-path`. Sigue las instrucciones de la guía de instalación para instalar `DBD::Pg` en tu sistema operativo.

**Funcionalidades de la suite de pruebas:**

- Añadidas configuraciones de prueba con vagrant para Ubuntu 14.04 y CentOS 7.


### Notas de la versión v0.78 {#v078-release-notes}

*Eliminación de dependencias de CPAN, mejoras de estabilidad*

*Publicada el 13 de julio de 2015*

**Mejoras:**

- Eliminada la dependencia de paquetes de CPAN para la operación multihilo. Aunque actualizar los paquetes `threads` y `Thread::Queue` podría no ser mala idea, ya no es necesario.
- Modificado el retroceso de espera para usar una secuencia de Fibonacci en lugar de geométrica. Esto hará que el tiempo de espera crezca de manera menos agresiva dando aún valores razonables.

**Funcionalidades de la suite de pruebas:**

- Añadidas configuraciones de prueba con vagrant para Ubuntu 12.04 y CentOS 6.


### Notas de la versión v0.77 {#v077-release-notes}

*Soporte de CentOS/RHEL 6 y mejoras de protocolo*

*Publicada el 30 de junio de 2015*

**Funcionalidades:**

- Añadidas sincronizaciones de archivos y directorios al objeto `File` para mayor seguridad durante la copia de seguridad/restauración y el archivado. (*Sugerido por Andres Freund.*)
- Añadido soporte para Perl 5.10.1 y OpenSSH 5.3, que son los valores por defecto para CentOS/RHEL 6. (*Sugerido por Eric Radman.*)
- Mejorado el mensaje de error cuando la copia de seguridad se ejecuta sin `archive_command` establecido y sin especificar `--no-archive-check`. (*Sugerido por Eric Radman.*)


### Notas de la versión v0.75 {#v075-release-notes}

*Nuevo formato de repositorio, comando info y soporte experimental de 9.5*

*Publicada el 14 de junio de 2015*

**NOTA IMPORTANTE**: Esta versión «flag day» rompe la compatibilidad con versiones anteriores de pgBackRest. El formato del manifiesto, la estructura en disco y los nombres de los binarios han cambiado. Debes crear un repositorio nuevo para almacenar las copias de seguridad de esta versión de pgBackRest y conservar tu repositorio anterior por un tiempo en caso de que necesites hacer una restauración. El archivo `pg_backrest.conf` no ha cambiado, pero deberás cambiar cualquier referencia a `pg_backrest.pl` en cron (u otros lugares) por `pg_backrest` (sin la extensión `.pl`).

**Funcionalidades:**

- Añadido el comando `info`.
- El registro ahora usa salida sin búfer. Esto debería hacer menos caóticos los archivos de registro que están siendo escritos por múltiples hilos. (*Sugerido por Michael Renner.*)
- Soporte experimental para PostgreSQL 9.5. Esto puede romperse cuando cambien la versión de control o el número mágico del WAL, pero se actualizará en cada versión.

**Mejoras:**

- Ordenación de archivos más eficiente para `backup`. Los archivos se copian en orden descendente de tamaño para que un solo hilo no termine copiando un archivo grande al final. Esto ya había sido implementado para `restore`.


### Notas de la versión v0.70 {#v070-release-notes}

*Mejoras de estabilidad para el archivado, registro y ayuda mejorados*

*Publicada el 1 de junio de 2015*

**Correcciones de errores:**

- Corregido un problema por el que `archive-copy` fallaba en una copia de seguridad incr/diff cuando `hardlink=n`. En este caso, la ruta `pg_xlog` aún no existe y debe crearse. (*Reportado por Michael Renner.*)
- Corregido un problema en el archivado asincrónico por el que `archive-push` no devolvía correctamente 0 cuando se alcanzaba `archive-max-mb`; se movió la comprobación asincrónica después de la transferencia para evitar tener que eliminar el archivo de parada dos veces. También se añadieron pruebas unitarias para este caso y se mejoraron los mensajes de error para que quede más claro para el usuario qué salió mal. (*Reportado por Michael Renner.*)
- Corregido un problema de bloqueo que podía permitir múltiples operaciones del mismo tipo contra una sola stanza. Esto parecía benigno en términos de integridad de datos, pero causaba errores espurios durante el archivado y podía llevar a errores en la copia de seguridad/restauración. (*Reportado por Michael Renner.*)

**Funcionalidades:**

- Permitir que se archiven segmentos WAL duplicados cuando la suma de verificación coincide. Esto es necesario para algunos escenarios de recuperación.
- Permitir comentarios/deshabilitación en `pg_backrest.conf` usando el carácter `#`. Solo se respetan los caracteres `#` en el primer carácter de la línea. (*Sugerido por Michael Renner.*)
- Mejor registro antes de `pg_start_backup()` para dejar claro cuando la copia de seguridad está esperando un checkpoint. (*Sugerido por Michael Renner.*)
- Varias correcciones de comportamiento y registro de comandos. (*Revisado por Michael Renner. Sugerido por Michael Renner.*)

**Mejoras:**

- Reemplazado el módulo `JSON` por `JSON::PP`, que viene con Perl core.

**Correcciones de errores en la documentación:**

- Varias correcciones de la ayuda. (*Revisado por Michael Renner. Reportado por Michael Renner.*)


### Notas de la versión v0.65 {#v065-release-notes}

*Reanudación y registro de restauración mejorados, restauraciones compactas*

*Publicada el 11 de mayo de 2015*

**Correcciones de errores:**

- Corregido un problema por el que no se escribía una ruta absoluta en `recovery.conf` cuando la restauración se ejecutaba con una ruta relativa.

**Funcionalidades:**

- Mejor soporte de reanudación. Se comprueba que los archivos reanudados no hayan sido modificados y el manifiesto se guarda más a menudo para preservar las sumas de verificación a medida que avanza la copia de seguridad. Más pruebas unitarias para verificar cada caso de reanudación.
- La reanudación ahora es opcional. Usa el ajuste `resume` o `--no-resume` desde la línea de comandos para deshabilitarla.
- Más mensajes de nivel info durante la restauración. Anteriormente, la mayoría de los mensajes de restauración eran de nivel debug, así que no se mostraba mucho en el registro.
- Añadido el ajuste `tablespace` para permitir que los tablespaces se restauren en la ruta `pg_tblspc`. Esto produce restauraciones compactas que son convenientes para desarrollo, staging, etc. Actualmente estas restauraciones no pueden respaldarse, ya que pgBackRest espera solo enlaces en la ruta `pg_tblspc`.


### Notas de la versión v0.61 {#v061-release-notes}

*Corrección para destino remoto sin compresión*

*Publicada el 21 de abril de 2015*

**Correcciones de errores:**

- Corregido un error de almacenamiento en búfer que podía ocurrir en archivos grandes y altamente compresibles al copiar a un destino remoto sin compresión. El error se detectó en el código de descompresión y resultaba en una copia de seguridad fallida en lugar de corrupción, por lo que no debería afectar a las copias exitosas hechas con versiones anteriores.


### Notas de la versión v0.60 {#v060-release-notes}

*Mejor soporte de versiones y mejoras de WAL*

*Publicada el 19 de abril de 2015*

**Correcciones de errores:**

- Ahora se genera un error al enviar WAL duplicado. Esto funcionaba antes solo si las sumas de verificación estaban deshabilitadas.

**Funcionalidades:**

- Los identificadores de sistema de bases de datos se usan para asegurar que todo el WAL de un archivado corresponda al mismo sistema. Esto debería ayudar a prevenir configuraciones erróneas que envían WAL de múltiples clústeres al mismo archivado.

**Funcionalidades de la suite de pruebas:**

- Pruebas de regresión que funcionan hasta PostgreSQL 8.3.


### Notas de la versión v0.50 {#v050-release-notes}

*Restauración y mucho más*

*Publicada el 25 de marzo de 2015*

**Correcciones de errores:**

- Corregidas las sumas de verificación rotas y ahora funcionan con copias de seguridad normales y reanudadas. Finalmente se comprendió que las sumas de verificación y los deltas de sumas de verificación deberían separarse funcionalmente, y esto simplificó varias cosas. Se ha creado el issue #28 para los deltas de sumas de verificación.
- Corregido un problema por el que una copia de seguridad podía reanudarse desde una copia abortada que no tenía el mismo tipo y copia anterior.

**Funcionalidades:**

- Añadida la funcionalidad de restauración.
- Ahora todas las opciones pueden establecerse en la línea de comandos, lo que hace opcional a `pg_backrest.conf`.
- La des/compresión ahora se realiza sin hilos y la suma de verificación/tamaño se calcula en flujo. Eso significa que las sumas de verificación de archivos ya no son opcionales.
- Añadida la opción `--no-start-stop` para permitir copias de seguridad cuando Postgres está apagado. Si `postmaster.pid` está presente, entonces se requiere `--force` para que la copia se ejecute (aunque si Postgres está en ejecución, probablemente se creará una copia de seguridad inconsistente). Esta opción se añadió principalmente con el propósito de las pruebas unitarias, pero también puede haber aplicaciones en el mundo real.
- Suma de verificación para `backup.manifest` que permite detectar un manifiesto corrupto/modificado.
- El enlace `latest` siempre apunta a la última copia de seguridad. Se ha añadido por conveniencia y para hacer las restauraciones más simples.

**Funcionalidades de la suite de pruebas:**

- Pruebas unitarias más completas en todas las áreas.


### Notas de la versión v0.30 {#v030-release-notes}

*Reestructuración del núcleo y pruebas unitarias*

*Publicada el 5 de octubre de 2014*

**Funcionalidades de la documentación:**

- Añadida la muy necesaria documentación

**Funcionalidades de la suite de pruebas:**

- Pruebas unitarias bastante completas para todas las operaciones básicas. Seguro que queda más trabajo por hacer aquí, pero siempre hay más trabajo por hacer en pruebas unitarias.


### Notas de la versión v0.19 {#v019-release-notes}

*Reporte/manejo de errores mejorado*

*Publicada el 13 de mayo de 2014*

**Correcciones de errores:**

- Encontrado y eliminado un error desagradable por el que `file_copy()` tenía por defecto ignorar los errores. También había un problema en `file_exists()` que hacía que la prueba fallara cuando el archivo realmente existía. Juntos podrían haber resultado en una copia de seguridad corrupta sin errores, aunque es muy improbable.


### Notas de la versión v0.18 {#v018-release-notes}

*Devolución de error suave cuando falta el archivo del archivado*

*Publicada el 13 de abril de 2014*

**Correcciones de errores:**

- El comando `archive-get` ahora devuelve un 1 cuando falta el archivo del archivado para diferenciarlo de los errores graves (fallo de conexión ssh, error de copia de archivo, etc.). Esto permite que PostgreSQL sepa que el flujo de archivado ha terminado normalmente. Sin embargo, esto no tiene en cuenta posibles huecos en el flujo de archivado. (*Reportado por Stephen Frost.*)


### Notas de la versión v0.17 {#v017-release-notes}

*Advertencia cuando no se pueden eliminar directorios de archivado*

*Publicada el 3 de abril de 2014*

**Correcciones de errores:**

- Si un directorio de archivado que debería estar vacío no podía eliminarse, backrest lanzaba un error. Viene una buena corrección para eso, pero por el momento se ha cambiado a una advertencia para que el procesamiento pueda continuar. Esto impactaba las copias de seguridad, ya que a veces el archivo final del archivado no se enviaba si el primer archivo del archivado había estado en un directorio diferente (más algo de mala suerte).


### Notas de la versión v0.16 {#v016-release-notes}

*RequestTTY=yes para sesiones SSH*

*Publicada el 1 de abril de 2014*

**Correcciones de errores:**

- Añadido `RequestTTY=yes` a las sesiones ssh. Se espera que esto evite bloqueos aleatorios.


### Notas de la versión v0.15 {#v015-release-notes}

*Añadido archive-get*

*Publicada el 29 de marzo de 2014*

**Funcionalidades:**

- Añadida la funcionalidad `archive-get` para ayudar en las restauraciones.
- Añadida una opción para forzar un checkpoint al iniciar la copia de seguridad, `start-fast=y`.


### Notas de la versión v0.11 {#v011-release-notes}

*Correcciones menores*

*Publicada el 26 de marzo de 2014*

**Correcciones de errores:**

- Eliminada la opción `master_stderr_discard` en las conexiones SSH de la base de datos. Ha habido bloqueos ocasionales y podrían estar relacionados con problemas vistos originalmente en el código de archivos. (*Reportado por Stephen Frost.*)
- Cambiados los conflictos de archivos de bloqueo en los comandos `backup` y `expire` a `ERROR`. Estaban establecidos en `DEBUG` debido a un copiar y pegar de los bloqueos de archivado.


### Notas de la versión v0.10 {#v010-release-notes}

*La copia de seguridad y el archivado son funcionales*

*Publicada el 5 de marzo de 2014*

**Funcionalidades:**

- Sin funcionalidad de restauración, pero los directorios de copia de seguridad son directorios de datos de PostgreSQL consistentes. Deberás descomprimir los archivos o desactivar la compresión en la copia de seguridad. Las copias sin compresión en un sistema de archivos ZFS (o similar) son una buena opción porque las copias pueden restaurarse localmente mediante una instantánea para crear copias lógicas o hacer recuperación puntual de datos.
- El archivado es de un solo hilo. Esto no ha planteado un problema en nuestras bases de datos de múltiples terabytes con alto volumen de escritura. Se recomienda un volumen de WAL grande o usar la opción asincrónica con un volumen grande cercano.
- Las copias de seguridad son multihilo, pero la biblioteca `Net::OpenSSH` no parece ser 100% segura para hilos, así que muy ocasionalmente se bloqueará en un hilo. Hay un tiempo de espera global del proceso que resuelve este problema matando el proceso. Sí, muy feo.
- Las sumas de verificación se pierden en cualquier copia de seguridad reanudada. Solo la copia final registrará la suma de verificación en reanudaciones múltiples. Las sumas de verificación de copias anteriores se registran correctamente y una copia de seguridad completa lo restablece todo.
- El `backup.manifest` se está escribiendo como `Storable` porque `Config::IniFile` no parece manejar bien los archivos grandes. Definitivamente nos gustaría guardarlos como texto legible por humanos.

**Funcionalidades de la documentación:**

- Absolutamente sin documentación (fuera del código). Bueno, exceptuando estas notas de versión.
