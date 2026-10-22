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

Los números de versión de pgBackRest constan de tres partes: principal, secundaria y parche. Una versión principal *puede* romper la compatibilidad con la versión principal anterior, pero las versiones v2 son totalmente compatibles con los repositorios v1 y aceptarán todas las opciones v1. Las versiones secundarias pueden incluir correcciones de errores y funcionalidades, pero no cambian el formato del repositorio y procuran evitar cambios en las opciones y en los nombres. Las versiones de parche contienen correcciones de errores para la versión secundaria más reciente.

Las versiones con funcionalidades están programadas para el tercer lunes de enero, abril, julio y octubre. Las versiones de parche están programadas para el tercer lunes de los demás meses, según sea necesario.

La documentación de la versión v1 puede encontrarse [aquí](https://pgbackrest.org/1).

Las notas de una versión también pueden contener «Notas adicionales», pero los cambios en esa sección afectan únicamente a la documentación o a la suite de pruebas y no tienen impacto directo en el código base de pgBackRest.

--------

## Versión estable documentada {#current-stable-release}

Este espejo cubre la v2.60.0. Consulta el [historial de versiones original](https://pgbackrest.org/release.html) para las versiones más recientes.

### Notas de la versión v2.60.0 {#v2600-release-notes}

*Errores de suma de verificación de páginas y lectura anticipada de almacenes de objetos*

*Publicada el 18 de octubre de 2026*

**NOTA IMPORTANTE**: El comando `restore` ahora notificará un error y se detendrá si algún archivo restaurado contiene una suma de verificación de página no válida. Esto deja el clúster incompleto e incapaz de arrancar, por lo que es necesario repetir la restauración. El comando `expire` ahora se negará a ejecutar la caducidad si la copia de seguridad más antigua que se conservaría contiene errores de suma de verificación, lo que también impide caducar el archivo WAL en ese repositorio. Establece `checksum-page-error=n` para emitir advertencias en lugar de errores.

**Funcionalidades:**

- Añadida la opción `checksum-page-error` para generar un error cuando las sumas de verificación de páginas no sean válidas. (*Contribución de Andrew Pogrebnoi. Revisado por Douglas J Hunley, David Steele, Greg Sabino Mullane, Stefan Fercot. Sugerido por Greg Sabino Mullane.*)

  Esta opción se aplica a los comandos `backup`, `restore` y `expire`. Por defecto, `backup` emite una advertencia por archivo, como antes, y ahora también informa del número total de advertencias de suma de verificación al finalizar la copia. Los comandos `restore` y `expire` generan un error por defecto. Anteriormente, `restore` no notificaba en absoluto las sumas de verificación de páginas no válidas.

  Incidencia [#2687](https://github.com/pgbackrest/pgbackrest/issues/2687); Solicitud de incorporación [#2833](https://github.com/pgbackrest/pgbackrest/pull/2833); Commit [`d7f54b2`](https://github.com/pgbackrest/pgbackrest/commit/d7f54b2245c8a9467e9a811c65626fe77739376b)
- Soporte de Workload Identity Federation de GCS. (*Contribución de Adol Rodriguez. Revisado por Douglas J Hunley, David Steele.*)

  Establece `repo-gcs-key-type=web-id` y configura `repo-gcs-key` con un archivo de credenciales de cuenta externa, por ejemplo, uno generado por `gcloud iam workload-identity-pools create-cred-config`. El token de identidad web se intercambia por un token de acceso sin una clave de cuenta de servicio. El archivo del token se vuelve a cargar en cada intercambio para recoger los tokens rotados, como los tokens proyectados de cuentas de servicio de Kubernetes. No se admite la suplantación de cuentas de servicio.

  Incidencia [#2838](https://github.com/pgbackrest/pgbackrest/issues/2838); Solicitud de incorporación [#2839](https://github.com/pgbackrest/pgbackrest/pull/2839); Commit [`1d217e6`](https://github.com/pgbackrest/pgbackrest/commit/1d217e626301118ae2c1e7be39a6a4affa86e501)
- Lectura anticipada de varios archivos o rangos desde almacenes de objetos. (*Revisado por Andrew Pogrebnoi, Douglas J Hunley.*)

  Las solicitudes se ponen en cola por delante de la lectura actual para que avancen mientras se lee, y los pequeños huecos entre archivos se leen de paso en vez de iniciar una nueva solicitud. `Restore` lo utiliza para leer archivos agrupados y mapas incrementales por bloques, y `backup` para leer los mapas incrementales por bloques de la copia anterior. `repo-storage-prefetch` (valor predeterminado 3) establece cuántas solicitudes se ponen en cola y `repo-storage-read-over` (valor predeterminado 64KiB) fija el tamaño máximo del hueco que se lee de paso.

  [`e63dec3`](https://github.com/pgbackrest/pgbackrest/commit/e63dec323b9e79513638b9858e4ad13b6072d060) Lectura anticipada de varios archivos o rangos desde almacenes de objetos.; Solicitud de incorporación [#2783](https://github.com/pgbackrest/pgbackrest/pull/2783)

  [`5ae4015`](https://github.com/pgbackrest/pgbackrest/commit/5ae4015d37081eba4259f4de379a9d160236de0e) Agrupar las lecturas de mapas incrementales por bloques anteriores durante la copia de seguridad.; Solicitud de incorporación [#2816](https://github.com/pgbackrest/pgbackrest/pull/2816)

**Mejoras:**

- Reducir las solicitudes keep-alive a los procesos remotos. (*Revisado por Douglas J Hunley.*)

  Antes se enviaba un keep-alive a cada remoto cada vez que terminaba un trabajo en `archive-push` y `backup`, incluso si acababa de enviársele una solicitud. Ahora solo se envía un keep-alive cuando no se ha enviado ninguna solicitud al remoto durante 30 segundos.

  Commit [`f652261`](https://github.com/pgbackrest/pgbackrest/commit/f652261d32a4ffba98e7da26a41ef4ef1cd08da3)
- Reintentar las subsolicitudes de lote de Azure ausentes de la respuesta. (*Revisado por Douglas J Hunley.*)

  Cuando falla una eliminación por lotes en Azure, este puede devolver una sola respuesta para todo el lote. Las subsolicitudes sin respuesta se consideraban completadas, por lo que solo se eliminaba un archivo por lote aunque el comando informase de éxito. Ahora se reintentan las subsolicitudes sin respuesta.

  Incidencia [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Solicitud de incorporación [#2849](https://github.com/pgbackrest/pgbackrest/pull/2849); Commit [`567a245`](https://github.com/pgbackrest/pgbackrest/commit/567a2451244e0e7a4c54e41880fac1a007b49930)
- Reducir las comprobaciones de manifiestos al reconstruir `backup.info`. (*Revisado por Douglas J Hunley. Sugerido por todeb.*)

  Los comandos `backup`, `expire` y `annotate` ya no buscan un `backup.manifest` cuando el listado del repositorio indica que la ruta de la copia no existe, o cuando una copia diferencial o incremental pertenece a un conjunto de copia completa que no figura en `backup.info`. Cada comprobación supone una solicitud, por lo que, en un almacén de objetos, la búsqueda de un manifiesto inexistente se registra como un 404.

  Incidencia [#2769](https://github.com/pgbackrest/pgbackrest/issues/2769); Solicitud de incorporación [#2825](https://github.com/pgbackrest/pgbackrest/pull/2825); Commit [`0d3c340`](https://github.com/pgbackrest/pgbackrest/commit/0d3c340087bfb97263c29a8fd681cf079071236b)
- Usar el tamaño original para decidir si un archivo debe agruparse. (*Revisado por Douglas J Hunley.*)

  Antes se usaba el tamaño del archivo incremental por bloques de la copia anterior para decidir si agruparlo, por lo que un archivo que había crecido por encima de `repo-bundle-limit` podía seguir almacenándose en un grupo. Ahora se utiliza el tamaño actual del archivo.

  Solicitud de incorporación [#2843](https://github.com/pgbackrest/pgbackrest/pull/2843); Commit [`340d58b`](https://github.com/pgbackrest/pgbackrest/commit/340d58bb49d6c88a002a0d23830fd37be155cc21)
- Añadir contexto a los errores de lectura del mapa de bloques durante la copia de seguridad. (*Revisado por Stefan Fercot, Douglas J Hunley.*)

  Un error al leer el mapa de bloques de una copia anterior ahora indica el archivo, la ruta del repositorio, el desplazamiento y el tamaño del mapa. Si una lectura devuelve menos bytes de los esperados, se informa de ello en lugar de notificar un error de análisis.

  [`bc91688`](https://github.com/pgbackrest/pgbackrest/commit/bc91688c4cf18fa6a36ec65441784533d5e6bdd5) Añadir contexto a los errores de lectura del mapa de bloques durante la copia de seguridad.; Incidencia [#2489](https://github.com/pgbackrest/pgbackrest/issues/2489); Incidencia [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Solicitud de incorporación [#2830](https://github.com/pgbackrest/pgbackrest/pull/2830)

  [`f46bfaf`](https://github.com/pgbackrest/pgbackrest/commit/f46bfafdd53dd0031a320fa95b08568263901ff3) Corregir el nombre de la opción en los errores de mapas incrementales por bloques.
- Convertir `current_timestamp` a `text` en la etiqueta de inicio de la copia de seguridad. (*Contribución de Tiago Corcelli de Oliveira. Revisado por David Steele.*)

  Una conversión implícita definida por el usuario de `timestamptz` a `text` hacía que la copia de seguridad fallara con "operator is not unique: unknown || timestamp with time zone". El texto de la etiqueta no cambia.

  Incidencia [#2873](https://github.com/pgbackrest/pgbackrest/issues/2873); Commit [`86936e1`](https://github.com/pgbackrest/pgbackrest/commit/86936e1fa60b10b7592eaac09283c4bb5991265d)
- Soporte de compilación en illumos. (*Contribución de Kalevi Kolttonen. Revisado por Douglas J Hunley, David Steele.*)

  Se ha añadido un trabajo de OmniOS a CI. Solaris también podría funcionar, pero no se ha probado.

  Solicitud de incorporación [#2870](https://github.com/pgbackrest/pgbackrest/pull/2870); Commit [`ad72e58`](https://github.com/pgbackrest/pgbackrest/commit/ad72e5815f3cf9c0c6170dcbe04ef9c41762d3d9)
- Soporte de OpenSSL 4. (*Revisado por Douglas J Hunley.*)

  La compilación con OpenSSL 4 fallaba porque `X509_get_subject_name()` ahora devuelve un nombre `const`.

  Commit [`a729ac8`](https://github.com/pgbackrest/pgbackrest/commit/a729ac881f48225622151841e80146f7a3a4bce6)
- Corregir las compilaciones con clang. (*Revisado por Douglas J Hunley.*)

  En Linux, gcc instala `libbacktrace.a` en una ubicación donde clang también la busca, pero instala `backtrace.h` donde solo gcc puede encontrarla. La compilación con clang encontraba la biblioteca y luego fallaba al compilar. Ahora la biblioteca solo se utiliza si se encuentra su encabezado. También se corrigen los tipos de retorno que clang señala como conversiones de estrechamiento en las compilaciones de depuración.

  [`84b031a`](https://github.com/pgbackrest/pgbackrest/commit/84b031af68fe6a30b4150ec6c903cc8c1781fc05) Exigir el encabezado al comprobar libbacktrace.

  [`195e66b`](https://github.com/pgbackrest/pgbackrest/commit/195e66bafd89da511fb0d48e6e053176104c47c7) Devolver el tipo declarado en las funciones que devuelven una enumeración basada en StringId.

  [`d9e5e14`](https://github.com/pgbackrest/pgbackrest/commit/d9e5e14e93f460d62930f58dd4dd5bbc2a9f3a85) Devolver bool desde una función declarada para devolver bool.
- Migrar la generación de código de C a Python.

  Durante la compilación, una herramienta de Python genera código a partir de las declaraciones de opciones, errores, ayuda y PostgreSQL, en lugar de una herramienta de C que había que compilar primero. Compilar desde una copia de trabajo de git requiere PyYAML en lugar de libyaml. El archivo tar de la versión incluye el código generado y no requiere ninguno de los dos.

  Commit [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e)

**Mejoras en la documentación:**

- Modernizar el sitio web. Un agradecimiento especial a Jan por el logo tan ingenioso (y divertido). (*Contribución de David Steele, Jan Wieremjewicz. Revisado por Steve Atkins, Kai Wagner, Douglas J Hunley, Nikolaos Stamatopoulos, Matt Hudson, Stefan Fercot.*)

  El sitio web tiene un nuevo diseño con temas claro y oscuro y una disposición que funciona en teléfonos. Las páginas con índice lo muestran junto al texto y señalan la sección que se está leyendo. Los comandos y archivos de configuración se pueden copiar con un botón, los archivos de configuración marcan las líneas que cambia cada sección y las notas de versión se pueden desplegar para mostrar más detalles.

  [`5bc14b5`](https://github.com/pgbackrest/pgbackrest/commit/5bc14b581a054ab3dc9cd633954a689acc99a58f) Acortar y aclarar los títulos de la documentación.

  [`b668d71`](https://github.com/pgbackrest/pgbackrest/commit/b668d71f22489cbd4d5e120e7e6e73be0ca9e167) Mover los patrocinadores más abajo en la página principal y acortar la petición de apoyo.

  [`60b85c5`](https://github.com/pgbackrest/pgbackrest/commit/60b85c58d98dd65d47747e6355f47c934cd6b430) Modernizar el sitio web.

  [`ab8df23`](https://github.com/pgbackrest/pgbackrest/commit/ab8df23807cc4c11768ef40196bcade70ebec23a) Mostrar una tarjeta en lugar del logo cuando se publica un enlace.

  [`76ae494`](https://github.com/pgbackrest/pgbackrest/commit/76ae49456c7dace20bbd6f17e8acdfd36bf03a46) Eliminar el índice de la página de versiones y reducir el espacio alrededor de la fecha.

  [`3e86c71`](https://github.com/pgbackrest/pgbackrest/commit/3e86c71f5546c86941f35d5be3a7fdcd98af3cca) Enlazar las opciones en lugar de repetirlas en la referencia de comandos.

  [`dc3af7b`](https://github.com/pgbackrest/pgbackrest/commit/dc3af7b2aee5778dbe9200e31d5a2f95ecae5777) Aclarar los títulos de los comandos en la referencia de comandos.

  [`078d52c`](https://github.com/pgbackrest/pgbackrest/commit/078d52c5768bb67989624b5418fdd687fab9e485) Marcar las líneas que cambia una sección en un archivo de configuración.

  [`bd33623`](https://github.com/pgbackrest/pgbackrest/commit/bd33623ba945ed251e2a6704cea14a81d51c2c9e) Marcar la salida de un comando del mismo modo que un archivo de configuración.

  [`578fc2d`](https://github.com/pgbackrest/pgbackrest/commit/578fc2de14a6a739401fd58b9a232cf587c52fb4) Permitir copiar un comando además de un archivo de configuración.

  [`1fb93f9`](https://github.com/pgbackrest/pgbackrest/commit/1fb93f92725124d6afa8953b7c7243aee92fcaf5) Generar un error cuando una sección de configuración no cambia nada visible para el lector.

  [`2f3b2f2`](https://github.com/pgbackrest/pgbackrest/commit/2f3b2f22a30a35340549d42b09d5aaa58d9dfe61) Convertir el logo del sitio en un enlace a la página principal.

  [`8f902c6`](https://github.com/pgbackrest/pgbackrest/commit/8f902c66609c0bf1de6720e60552adde515209cd) Acelerar la compilación de la documentación.

  [`b56b6ab`](https://github.com/pgbackrest/pgbackrest/commit/b56b6ab4d24ff6298b95b415b3115591e311de20) Mostrar automáticamente las noticias más recientes en la página principal.

  [`5b8987d`](https://github.com/pgbackrest/pgbackrest/commit/5b8987da0bb24fc3979fb764ccbde82b7b0e9500) Mostrar los ejemplos de tipos de opciones como bloques de código en la referencia.

  [`b5d5274`](https://github.com/pgbackrest/pgbackrest/commit/b5d527471444f90df5529f15726b3d33065f9829) Desplazar el menú horizontalmente en lugar de dejar que se parta en líneas fuera de la vista.

  [`9ae2c32`](https://github.com/pgbackrest/pgbackrest/commit/9ae2c32a35f56f53f299e8c04f004ed3386b95e4) Resaltar la página actual en el menú en lugar de omitirla.

  [`b8da5b0`](https://github.com/pgbackrest/pgbackrest/commit/b8da5b061d0f9c5d1cc01e936dc65cbdd9f70be7) Añadir versiones a los enlaces de estilos y scripts para volver a descargarlos cuando la caché esté obsoleta.

  [`ec57431`](https://github.com/pgbackrest/pgbackrest/commit/ec57431aa88860b9058d971b938afb5e35a142c7) Saltar directamente a una sección en lugar de desplazarse suavemente hasta ella.

  [`46babed`](https://github.com/pgbackrest/pgbackrest/commit/46babedaed8429026efa4592d93a8d9876acad0b) Difuminar el extremo por el que continúa el menú en lugar de cortarlo bruscamente.

  [`17de501`](https://github.com/pgbackrest/pgbackrest/commit/17de50192b7e40d7517a4079451e93da5c39b3f3) Colocar la barra de un encabezado section2 debajo del título en lugar de a su lado.

  [`940f431`](https://github.com/pgbackrest/pgbackrest/commit/940f4311375dda3caabdc0bdd01c36bedf43d46f) Centrar el título de la página junto al logo y alinearlo a la izquierda cuando ocupe varias líneas.

  [`050ca9e`](https://github.com/pgbackrest/pgbackrest/commit/050ca9e354421530ba4282d95dead90e31d6dc2a) Añadir detalles desplegables a las notas de versión.

  [`bd8f99b`](https://github.com/pgbackrest/pgbackrest/commit/bd8f99be00cd4b03a1b234bf7fbaa39f406c0c44) Añadir detalles a las notas de las versiones v2.33 a v2.60.

  [`28a1e3d`](https://github.com/pgbackrest/pgbackrest/commit/28a1e3d6278992e0a347aab19248abdcddefd491) Ajustar el estilo de las palabras clave en el modo claro.

  [`1911f5f`](https://github.com/pgbackrest/pgbackrest/commit/1911f5f1744ff4bfee528d95e37a0a8d9b77d6b3) Limitar el historial de notas de versión al momento de la integración en el CI del proyecto original.
- Documentar el calendario de versiones.

  Las versiones con funcionalidades están programadas para el tercer lunes de enero, abril, julio y octubre. Las versiones de parche están programadas para el tercer lunes de los demás meses, según sea necesario. La introducción de las notas de versión también describe las partes principal, secundaria y parche del número de versión.

  [`9bca69a`](https://github.com/pgbackrest/pgbackrest/commit/9bca69a591abcee0623ff910d0db3e27008cfc25) Documentar el calendario de versiones.

  [`c179f3f`](https://github.com/pgbackrest/pgbackrest/commit/c179f3f7d6d6b1963d9d3b98b981786ef9546022) Actualizar la numeración de versiones en la introducción de las notas de versión.
- Migrar las herramientas de documentación de C y Perl a Python.

  La documentación se compila con `doc/doc.py` en lugar de una herramienta de C ejecutada por `doc/doc.pl`, y ya no se necesita Perl para compilarla.

  [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e) Migrar el código de compilación y documentación de C a Python.

  [`fa3d197`](https://github.com/pgbackrest/pgbackrest/commit/fa3d1979b77d6252642c64d708a951914e0a0ac2) Migrar el código de documentación restante de Perl a Python.

**Mejoras en la suite de pruebas:**

- Migrar el arnés de pruebas de C y Perl a Python.

  Las pruebas se ejecutan con `test/test.py` en lugar de `test/test.pl`. Los contenedores de pruebas y los ejecutores de CI ya no requieren Perl, y el arnés está cubierto por pruebas.

  [`163e5ba`](https://github.com/pgbackrest/pgbackrest/commit/163e5ba0f9ff72ec730f0b35ddac0e5d68ece531) Migrar el arnés de pruebas de C a Python.

  [`e25c662`](https://github.com/pgbackrest/pgbackrest/commit/e25c6621e8427e862e4ce0196d059ab651bb276d) Migrar el resto del arnés de pruebas de Perl a Python.
- Añadir un trabajo de Fil-C a CI.

  Fil-C es una implementación de C con seguridad de memoria que comprueba cada acceso a punteros. Detectó dos lecturas fuera de límites que gcc, clang y Valgrind no habían detectado. Un nuevo flujo de trabajo también compila y prueba en el ejecutor de CI con gcc y clang, con y sin las bibliotecas opcionales.

  [`f32a5d5`](https://github.com/pgbackrest/pgbackrest/commit/f32a5d5543c4dc547006629bdb2dd52d3edb9205) Añadir un flujo de trabajo para compilar y probar en el ejecutor sin un contenedor.

  [`12396fb`](https://github.com/pgbackrest/pgbackrest/commit/12396fb353bc4aa10c3739b826189e421732adf5) Añadir un trabajo de Fil-C al flujo de compilación.

  [`908a11a`](https://github.com/pgbackrest/pgbackrest/commit/908a11a841e85d4e66e4aa551380b52aabfe606f) Usar la distribución de Fil-C tal cual, ahora que incluye todas las bibliotecas necesarias.
- Añadir pruebas de fuzzing para los lectores de `JSON`, `Ini` y `Pack`.

  Los lectores se someten a fuzzing con libFuzzer, AddressSanitizer y UndefinedBehaviorSanitizer en CI. El fuzzing encontró varios errores al leer entradas no válidas; por ejemplo, los arrays JSON muy anidados en un archivo de información o en una respuesta del almacén de objetos podían desbordar la pila de contextos de memoria.

  Commit [`4c65010`](https://github.com/pgbackrest/pgbackrest/commit/4c65010e7d28ea68571732fb275d91266a97ad80)
- Permitir nombres de usuario de pruebas que adduser rechaza en Debian. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  El contenedor de pruebas se construye con el mismo nombre de usuario que el usuario del host. El comando `adduser` de Debian rechaza los nombres que contienen un punto, como `first.last`, por lo que la construcción del contenedor fallaba en imágenes basadas en Debian para esos usuarios.

  Incidencia [#2858](https://github.com/pgbackrest/pgbackrest/issues/2858); Solicitud de incorporación [#2859](https://github.com/pgbackrest/pgbackrest/pull/2859); Commit [`ce19dae`](https://github.com/pgbackrest/pgbackrest/commit/ce19dae6a2d6ab3665374ead04c270fd45d563fb)


--------

## Versiones estables {#stable-releases}

### Notas de la versión v2.59.3 {#v2593-release-notes}

*Error de subclaves de cifrado débiles*

*Publicada el 4 de octubre de 2026*

**NOTA IMPORTANTE**: En versiones anteriores era posible que se generaran subclaves y sales de cifrado débiles si se producía un error al acceder a los datos aleatorios del sistema. Consulta [Subclaves y sales de cifrado débiles](/es/pgbackrest/news/#weak-encryption) para obtener más información.

**Correcciones de errores:**

- Corregido un posible error de suma de verificación al cargar los archivos de información y manifiesto cifrados. (*Corregido por j0uinim. Revisado por David Steele.*)

  Al cargar un archivo de información o manifiesto cifrado de gran tamaño podían perderse sus últimas líneas, lo que provocaba un fallo de la suma de verificación. Las líneas perdidas debían caber en el último bloque de cifrado, por lo que es poco probable en la práctica.

  Incidencia [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Solicitud de incorporación [#2868](https://github.com/pgbackrest/pgbackrest/pull/2868); Commit [`2def063`](https://github.com/pgbackrest/pgbackrest/commit/2def063e06c6f0b7e137309c7ed0d7631a42f6cf)
- Corregida la posible generación de subclaves/sales de cifrado débiles. (*Corregido por j0uinim. Revisado por David Steele, Stefan Fercot, Douglas J Hunley.*)

  Cuando OpenSSL no podía obtener datos aleatorios del sistema operativo, se ignoraba el fallo y se generaban subclaves y sales a partir de memoria que no contenía datos aleatorios. Ahora se informa de un error.

  Incidencia [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); Solicitud de incorporación [#2867](https://github.com/pgbackrest/pgbackrest/pull/2867); Commit [`47ed78f`](https://github.com/pgbackrest/pgbackrest/commit/47ed78f8d54a44466a872852939edc0273172bf1)

### Notas de la versión v2.59.2 {#v2592-release-notes}

*Soporte de PostgreSQL 19beta4*

*Publicada el 27 de septiembre de 2026*

**Correcciones de errores:**

- Corregido un mapa de bloques vacío cuando un archivo se trunca a cero durante la copia de seguridad. (*Revisado por Douglas J Hunley. Reportado por JPCOSTA78.*)

  Un archivo incremental por bloques mayor que `repo-bundle-limit` que PostgreSQL truncaba a cero durante una copia se almacenaba como un mapa de bloques sin bloques. Todas las copias posteriores que lo referenciaban fallaban con "unexpected eof" hasta la siguiente copia completa.

  Incidencia [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); Solicitud de incorporación [#2842](https://github.com/pgbackrest/pgbackrest/pull/2842); Commit [`572d163`](https://github.com/pgbackrest/pgbackrest/commit/572d1631026d5f10915634592b547f3439b7a291)
- Desactivado el reintento de lectura cuando se pasan filtros al controlador. (*Revisado por Douglas J Hunley. Reportado por megamaced.*)

  El reintento de una lectura de un repositorio en un almacén de objetos, accedido a través de un host de repositorio, provocaba un fallo del proceso. El cliente ya no reintenta estas lecturas. El host de repositorio sigue reintentando su lectura del almacén de objetos.

  Incidencia [#2845](https://github.com/pgbackrest/pgbackrest/issues/2845); Solicitud de incorporación [#2846](https://github.com/pgbackrest/pgbackrest/pull/2846); Commit [`c6eca28`](https://github.com/pgbackrest/pgbackrest/commit/c6eca28ff8e551bd2e76f0c91b1a70ddee60b35e)
- Corregida la paginación del listado de versiones de S3. (*Revisado por Douglas J Hunley, guruguruguru. Reportado por guruguruguru.*)

  La lectura de un repositorio en un momento determinado mediante `repo-target-time` fallaba con "unable to find child 'NextContinuationToken'" cuando se listaban más de mil versiones bajo un prefijo.

  Incidencia [#2854](https://github.com/pgbackrest/pgbackrest/issues/2854); Solicitud de incorporación [#2855](https://github.com/pgbackrest/pgbackrest/pull/2855); Commit [`6f0490d`](https://github.com/pgbackrest/pgbackrest/commit/6f0490dd29f0c756e6766fd9be023805540815fc)
- Establecido el encabezado de versión de Azure para la autenticación `SAS`. (*Revisado por Douglas J Hunley. Reportado por Florian Helmberger.*)

  Las eliminaciones por lotes requieren el encabezado de versión, por lo que con autenticación `SAS` se rechazaban todos los lotes. El rechazo parecía corresponder a un único archivo fallido y el resto del lote no se eliminaba, mientras `expire` informaba de éxito, dejando copias caducadas y WAL en el repositorio.

  Incidencia [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); Solicitud de incorporación [#2848](https://github.com/pgbackrest/pgbackrest/pull/2848); Commit [`ea3293b`](https://github.com/pgbackrest/pgbackrest/commit/ea3293be75c86b5e6c9ca4158b5ebe2a3224f76f)
- Corregido el bloqueo de `archive-push` asincrónico por un archivo de historial de copias de seguridad de tamaño cero. (*Corregido por Andrew Kroh. Revisado por David Steele, Douglas J Hunley.*)

  Un archivo de historial de copias de seguridad de tamaño cero, por ejemplo en un clúster copiado de una instantánea de almacenamiento, hacía fallar todas las ejecuciones asincrónicas de `archive-push`, por lo que no se archivaba ningún WAL. Ahora `archive-push-batch-size` se convierte a un número de segmentos usando el tamaño del primer segmento WAL listo.

  Incidencia [#2856](https://github.com/pgbackrest/pgbackrest/issues/2856); Solicitud de incorporación [#2857](https://github.com/pgbackrest/pgbackrest/pull/2857); Commit [`12b1b3c`](https://github.com/pgbackrest/pgbackrest/commit/12b1b3cf58caee7b04ed788eee221726f5caa155)
- Corregido el comando `annotate` en un repositorio remoto cifrado. (*Corregido por Douglas J Hunley. Revisado por David Steele.*)

  Cuando el repositorio estaba cifrado y el cifrado solo se configuraba en el host de repositorio, `annotate` no podía cargar `backup.info`.

  Commit [`497ad5a`](https://github.com/pgbackrest/pgbackrest/commit/497ad5aee0c654611d2ad4185958727e1341dd8c)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta4/rc1.

  PostgreSQL 19beta4 revirtió los cambios de sumas de verificación de páginas en línea, por lo que su versión vuelve a estar limitada a 0 y 1. También cambió la versión de `pg_control` y el número mágico de las páginas WAL.

  Commit [`89eae83`](https://github.com/pgbackrest/pgbackrest/commit/89eae839d5ca79591aaea8157f437688c3b53df4)

### Notas de la versión v2.59.1 {#v2591-release-notes}

*Soporte de PostgreSQL 19beta3*

*Publicada el 17 de agosto de 2026*

**Correcciones de errores:**

- Corregido el bloqueo cuando el búfer de fragmentos es más pequeño que el búfer de entrada. (*Revisado por Andrew Pogrebnoi, Douglas J Hunley. Reportado por crajac66.*)

  Una carga multiparte a S3, GCS o Azure podía entrar en un bucle infinito si el búfer de fragmentos era menor que el de entrada, por ejemplo después de aumentar el tamaño del fragmento durante la carga. Ahora el búfer de fragmentos siempre tiene capacidad suficiente para contener el de entrada.

  Incidencia [#2818](https://github.com/pgbackrest/pgbackrest/issues/2818); Solicitud de incorporación [#2819](https://github.com/pgbackrest/pgbackrest/pull/2819); Commit [`a53e470`](https://github.com/pgbackrest/pgbackrest/commit/a53e470eca258c2db088af55be307403c8f43b7a)
- Comparar una etiqueta de copia de seguridad nueva solo contra su propio conjunto basado en una copia de seguridad completa. (*Revisado por Douglas J Hunley. Reportado por Anton Glushakov.*)

  Algunos almacenes de objetos, como MinIO con bloqueo de objetos o SeaweedFS, siguen listando un prefijo después de borrar todo su contenido, por lo que una copia completa eliminada podía seguir apareciendo en el repositorio. Todas las copias diferenciales e incrementales posteriores fallaban entonces con "new backup label ... is not later than latest backup label ...". Ahora una etiqueta nueva solo se compara con las copias de su propio conjunto de copia completa.

  Incidencia [#2792](https://github.com/pgbackrest/pgbackrest/issues/2792); Solicitud de incorporación [#2824](https://github.com/pgbackrest/pgbackrest/pull/2824); Commit [`d01f77e`](https://github.com/pgbackrest/pgbackrest/commit/d01f77e8237f5d008bb7782c18ced12cd6d1971a)
- Corregidos los archivos fuente generados por GitHub a los que les faltaban archivos necesarios para compilar. (*Reportado por aardvarkzed.*)

  Los archivos de fuentes que GitHub genera para una versión no incluían las herramientas de generación de código ni sus archivos de entrada, por lo que no podían compilarse. Ahora solo se recorta el archivo tar de distribución.

  Incidencia [#2821](https://github.com/pgbackrest/pgbackrest/issues/2821); Commit [`163670a`](https://github.com/pgbackrest/pgbackrest/commit/163670a4eeede6d2d170b5d1f55c5ba0b66ba564)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta3. (*Contribución de Lardière Sébastien. Revisado por David Steele.*)

  PostgreSQL 19beta3 cambió el número mágico de las páginas WAL.

  Commit [`5cbc256`](https://github.com/pgbackrest/pgbackrest/commit/5cbc256bf37a44fa478d73a12a2e5b2d84fa6337)

**Mejoras en la documentación:**

- Documentar la excepción para los puntos en los nombres de bucket de S3 cuando `repo-s3-uri-style=path`.

  Con `repo-s3-uri-style=path`, el bucket forma parte de la ruta en lugar del nombre del host, por lo que los puntos en su nombre no provocan una discrepancia con el nombre de host del certificado.

  Commit [`bbdc4b9`](https://github.com/pgbackrest/pgbackrest/commit/bbdc4b9217a0e66f6a01c05f4edc04282cffb3fc)
- Eliminada la configuración explícita de `hot_standby` de la guía de usuario.

  `hot_standby` está activado por defecto desde PostgreSQL 10. La guía de inicio rápido ahora señala que un servidor en espera no acepta conexiones de solo lectura sin él.

  Commit [`cda454d`](https://github.com/pgbackrest/pgbackrest/commit/cda454d4bac0c0412230a0b41513659a7d0d4205)

### Notas de la versión v2.59.0 {#v2590-release-notes}

*Soporte de PostgreSQL 19beta2*

*Publicada el 20 de julio de 2026*

**NOTA PARA EMPAQUETADORES**: Hay disponible un nuevo archivo tar de distribución que simplifica la compilación al proporcionar documentación HTML, página de manual y código ya generados. Se adjunta a cada versión como un recurso con el nombre `pgbackrest-{version}.tar.gz`. Consulta el `README.md` incluido para más detalles. Utiliza el nuevo archivo tar de distribución para evitar las herramientas de compilación adicionales que se necesitarán para generar código en futuras versiones. Consulta [Nuevo archivo tar de distribución](/es/pgbackrest/news/#distribution-tarball) para más información.<br/> <br/> **NOTA PARA EMPAQUETADORES**: Hay una nueva dependencia opcional de `libsystemd`.<br/> <br/> **NOTA IMPORTANTE**: A partir de esta versión, por defecto solo el comando `restore` puede ejecutarse como root. Utiliza `allow-root` para ejecutar otros comandos como root, aunque no se recomienda.

**Correcciones de errores:**

- Corregir que `expire` elimine una copia de seguridad en curso en otro host. (*Revisado por Douglas J Hunley. Reportado por Dmitrii.*)

  Una copia no se añade a `backup.info` hasta que termina. Por ello, si `expire` se ejecutaba en un host mientras otro realizaba una copia, por ejemplo `expire` en un servidor en espera mientras se copiaba el primario, se eliminaba la copia en curso. La caducidad ya no elimina la copia más reciente si está en curso o se puede reanudar.

  Incidencia [#2622](https://github.com/pgbackrest/pgbackrest/issues/2622); Solicitud de incorporación [#2797](https://github.com/pgbackrest/pgbackrest/pull/2797); Commit [`aa0e215`](https://github.com/pgbackrest/pgbackrest/commit/aa0e215019f50f92a8f0c97f907affc1d3bf86c4)
- Corregir que `archive-push-queue-max` no se aplique cuando un archivo WAL provoca un error. (*Revisado por Stefan Fercot. Reportado por vut12.*)

  En modo asincrónico, la cola se medía según el WAL que quedaba por enviar. Si un archivo WAL fallaba repetidamente, los posteriores se enviaban y dejaban de contarse aunque permanecieran en `pg_wal`. Así, nunca se alcanzaba el límite de la cola y `pg_wal` podía llenar el disco. Ahora la cola se mide con todo el WAL que PostgreSQL está esperando archivar, como en el modo sincrónico.

  Incidencia [#2629](https://github.com/pgbackrest/pgbackrest/issues/2629); Solicitud de incorporación [#2799](https://github.com/pgbackrest/pgbackrest/pull/2799); Commit [`7fe3636`](https://github.com/pgbackrest/pgbackrest/commit/7fe363658639bbc2f70e53496fa6da4acb9e481e)
- Corregir el fallo de `archive-get` asincrónico durante una recuperación a través de un cambio de línea de tiempo. (*Revisado por Douglas J Hunley. Reportado por Jimmy Yih.*)

  Dos procesos asincrónicos podían competir por el bloqueo de archivado y el que perdía terminaba antes de obtener el segmento para el que se había iniciado. El `archive-get` que lo había iniciado esperaba entonces hasta `archive-timeout` y devolvía un error para un segmento existente, lo que podía finalizar la recuperación antes de tiempo, especialmente al cambiar de línea temporal. Ahora se obtiene el segmento directamente cuando no está en ejecución el proceso asincrónico que debería obtenerlo.

  Incidencia [#2423](https://github.com/pgbackrest/pgbackrest/issues/2423); Solicitud de incorporación [#2806](https://github.com/pgbackrest/pgbackrest/pull/2806); Commit [`baed942`](https://github.com/pgbackrest/pgbackrest/commit/baed942af0d61fcf3c2cb1f7d1bf1d6fe5bb6df9)
- Corregir un posible desbordamiento de búfer en el módulo de errores. (*Corregido por Christophe Pettus. Revisado por David Steele.*)

  Una traza de pila demasiado larga para su búfer no se terminaba y podía leerse más allá de su final. Asimismo, un mensaje de error demasiado largo podía escribir más allá del búfer al añadirle un error del sistema. Ambos casos requieren un mensaje inusualmente largo.

  [`7fd8bc8`](https://github.com/pgbackrest/pgbackrest/commit/7fd8bc89a15cb039111aa85fd37f9dc68f7c4d6d) Corregir un posible desbordamiento de búfer en el módulo de errores.

  [`5ca98ab`](https://github.com/pgbackrest/pgbackrest/commit/5ca98abc91f823ef97ff6a1e77d65727d1259218) Usar todo el búfer al dar formato a los mensajes de error.

  [`3a71dc8`](https://github.com/pgbackrest/pgbackrest/commit/3a71dc839a89b83f592c1d5813c068bcded1b6bc) Evitar escrituras fuera de límites en el búfer de errores con mensajes demasiado largos.
- Corregir un use-after-free del cliente de protocolo paralelo. (*Revisado por Douglas J Hunley. Reportado por Georgy Shelkovy.*)

  Un cliente que se quedaba sin trabajo se liberaba, pero permanecía en la lista de clientes y volvía a liberarse en una llamada posterior. Con registros de depuración o traza, esto leía memoria ya liberada y podía provocar un fallo del proceso, por ejemplo en una copia paralela con `log-level-file=trace`.

  Incidencia [#2754](https://github.com/pgbackrest/pgbackrest/issues/2754); Solicitud de incorporación [#2804](https://github.com/pgbackrest/pgbackrest/pull/2804); Commit [`31432ed`](https://github.com/pgbackrest/pgbackrest/commit/31432ed3977302b5e183f2b592d85afb521b4f55)
- Corregir un desbordamiento del heap cuando se configura una opción pg sin pg1. (*Revisado por Douglas J Hunley. Reportado por Naveen.*)

  Si se configuraban opciones `pg` para otros índices sin `pg1-path`, como `pg2-path` y `pg3-path`, se sobrescribía el mapa de índices. Esto corrompía el heap en musl, por ejemplo en Alpine, y provocaba un fallo de segmentación. También se perdía el `pg-path` con el número más alto.

  Incidencia [#1768](https://github.com/pgbackrest/pgbackrest/issues/1768); Solicitud de incorporación [#2796](https://github.com/pgbackrest/pgbackrest/pull/2796); Commit [`2d767de`](https://github.com/pgbackrest/pgbackrest/commit/2d767de3c59cf5570639e75755dc73c626fb99e1)
- Corregir el fallo cuando llega una señal durante la salida en musl 1.2.6.

  musl 1.2.6, por ejemplo en Alpine 3.24, falla si se llama a `exit()` cuando ya hay una salida en curso. Esto ocurría al llegar una señal durante la salida, por ejemplo cuando `server` terminaba un proceso hijo que ya estaba saliendo. Ahora se ignoran las señales que llegan durante la salida.

  Commit [`e166a33`](https://github.com/pgbackrest/pgbackrest/commit/e166a33f48a00192c09b0f1cea3465243c03d1f1)

**Funcionalidades:**

- Soporte de PostgreSQL 19beta1/beta2. (*Revisado por Stefan Fercot.*)

  Se añade soporte de PostgreSQL 19beta1/beta2. PostgreSQL 19 puede activar y desactivar las sumas de verificación de páginas en línea, y estas no se validan mientras cualquiera de las dos operaciones esté en curso.

  [`bc6d399`](https://github.com/pgbackrest/pgbackrest/commit/bc6d399a6a160f5fa41dd3a98ae046dff66e56a8) Soporte de PostgreSQL 19beta1.; Solicitud de incorporación [#2779](https://github.com/pgbackrest/pgbackrest/pull/2779)

  [`2777395`](https://github.com/pgbackrest/pgbackrest/commit/2777395dacc35aec51572d3e75c621725e2f9d9c) Soporte de PostgreSQL 19beta2.
- Añadir la opción `archive-expire-before` para limpiar el archivado de WAL. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  La opción `archive-expire-before` de `expire` elimina del archivo WAL los segmentos anteriores al indicado, pero nunca los que necesita una copia conservada. Puede limpiar el archivo desde el punto de reinicio de un servidor en espera mediante `archive_cleanup_command`, en lugar de `pg_archivecleanup`, que no conoce la política de retención.

  [`6cd692b`](https://github.com/pgbackrest/pgbackrest/commit/6cd692b1b321faf544ee3a9b1f503fd48007d7c7) Extraer la caducidad de WAL a expireArchiveId().

  [`4945139`](https://github.com/pgbackrest/pgbackrest/commit/4945139392c21f197f2e307abc3c89b5548cef8d) Añadir la opción `archive-expire-before` para limpiar el archivado de WAL.; Solicitud de incorporación [#2801](https://github.com/pgbackrest/pgbackrest/pull/2801)
- Añadir la eliminación por lotes para el almacenamiento Azure. (*Revisado por Douglas J Hunley, Crispy.*)

  Los archivos se eliminan mediante Azure Blob Batch API, hasta 256 por solicitud, en lugar de una solicitud por archivo. Esto acelera `expire` y otros comandos que eliminan archivos del repositorio.

  Solicitud de incorporación [#2786](https://github.com/pgbackrest/pgbackrest/pull/2786); Commit [`ffa325b`](https://github.com/pgbackrest/pgbackrest/commit/ffa325b8a44c1e9e44dc038bbcc8aece6f312a90)
- Añadir soporte para S3 Outposts. (*Contribución de Shiva Kumar Ambigi. Revisado por David Steele, Roberto Mello.*)

  Establece `repo-s3-service=s3-outposts` al utilizar un endpoint de S3 Outposts. La opción define el nombre del servicio utilizado para firmar las solicitudes y su valor predeterminado es `s3`.

  Solicitud de incorporación [#2762](https://github.com/pgbackrest/pgbackrest/pull/2762); Commit [`6c51800`](https://github.com/pgbackrest/pgbackrest/commit/6c518001c24ad2405eaf750d358f69703322a221)
- Añadir la autenticación de S3 mediante un proceso. (*Revisado por Andrew Charlton. Sugerido por Andrew Charlton.*)

  Establece `repo-s3-key-type=process` y configura `repo-s3-process-cmd` con un comando que emita credenciales temporales en el formato JSON del proveedor de credenciales mediante proceso de AWS. Las credenciales se renuevan antes de caducar.

  Solicitud de incorporación [#2778](https://github.com/pgbackrest/pgbackrest/pull/2778); Commit [`b5a578a`](https://github.com/pgbackrest/pgbackrest/commit/b5a578a5c2c88d53fca0ee8cfbfb8ee662ce7e48)
- Proporcionar un archivo tar de distribución con el código y la documentación generados.

  El archivo tar incluye el código generado, la página de manual y la documentación HTML ya renderizadas, por lo que se puede compilar e instalar sin las herramientas de generación de código y documentación, incluida `libyaml`.

  Commit [`8fcfef5`](https://github.com/pgbackrest/pgbackrest/commit/8fcfef5d8732055f9bc8e50224d5b7a988512e61)

**Mejoras:**

- Reconectar el almacenamiento SFTP después de que el servidor cierre una conexión inactiva. (*Revisado por Stefan Fercot. Sugerido por mustafa0x, tisserat.*)

  Los servidores SFTP y los cortafuegos pueden cerrar una conexión inactiva durante cierto tiempo, como la conexión de lectura del repositorio durante la fase de copia de una copia de seguridad, y el siguiente uso fallaba con un error de socket. Ahora se vuelve a abrir la conexión cerrada y se reintenta la operación una vez.

  [`d72bea9`](https://github.com/pgbackrest/pgbackrest/commit/d72bea9fe7c3975fc6832a51b0b0c1c041c467d2) Obtener la sesión libssh2 del almacenamiento en los objetos de lectura y escritura SFTP.

  [`a31febf`](https://github.com/pgbackrest/pgbackrest/commit/a31febfbd9ba639589fe57e4083ae9358b1306a4) Reconectar el almacenamiento SFTP después de que el servidor cierre una conexión inactiva.; Incidencia [#2739](https://github.com/pgbackrest/pgbackrest/issues/2739); Incidencia [#2772](https://github.com/pgbackrest/pgbackrest/issues/2772); Solicitud de incorporación [#2793](https://github.com/pgbackrest/pgbackrest/pull/2793)
- Añadir caché de usuario/grupo para una construcción más rápida del manifiesto. (*Contribución de Gunnar Lindholm. Revisado por David Steele.*)

  Cuando los nombres de usuario y grupo se resuelven mediante un servicio remoto, como sssd o LDAP, cada consulta requiere un viaje de ida y vuelta. Esto dominaba el tiempo de creación del manifiesto en clústeres con millones de archivos. Ahora se almacenan en caché los nombres de usuario y grupo.

  Solicitud de incorporación [#2773](https://github.com/pgbackrest/pgbackrest/pull/2773); Commit [`1e6d23f`](https://github.com/pgbackrest/pgbackrest/commit/1e6d23fea72ac9c599f8b62a2e0a3de02d0d08d0)
- Añadir el progreso de copia de seguridad por repositorio a la salida del comando `info`. (*Contribución de Will Morland. Revisado por David Steele, Stefan Fercot.*)

  Cuando se ejecutan copias en varios repositorios a la vez, `info` ahora informa del progreso de cada repositorio además del progreso global. La salida JSON contiene un array `repo` por cada bloqueo de copia de seguridad.

  Incidencia [#2736](https://github.com/pgbackrest/pgbackrest/issues/2736); Solicitud de incorporación [#2740](https://github.com/pgbackrest/pgbackrest/pull/2740); Commit [`77312b3`](https://github.com/pgbackrest/pgbackrest/commit/77312b33ba913132b33401d862c2e354f323c786)
- Añadir comprobaciones de `backup.info` al comando `verify`. (*Contribución de Denis Garsh. Revisado por David Steele, Douglas J Hunley.*)

  El comando `verify` ahora advierte cuando una copia del repositorio no figura en `backup.info` y cuando una copia de `backup.info` no está en el repositorio. Una copia ausente se informa como un manifiesto que falta.

  Incidencia [#2723](https://github.com/pgbackrest/pgbackrest/issues/2723); Solicitud de incorporación [#2752](https://github.com/pgbackrest/pgbackrest/pull/2752); Commit [`7f82fb6`](https://github.com/pgbackrest/pgbackrest/commit/7f82fb6635c1e3e9dd285d53076e9aee3fbf1ca2)
- Permitir configurar el endpoint STS de S3. (*Contribución de Simon Gratton. Revisado por David Steele.*)

  Establece `repo-s3-sts-host` para usar un endpoint regional de STS con `repo-s3-key-type=web-id`, por ejemplo `sts.eu-central-2.amazonaws.com`. Las regiones de AWS que requieren activación no aceptan credenciales del endpoint global, que sigue siendo el predeterminado.

  Incidencia [#2791](https://github.com/pgbackrest/pgbackrest/issues/2791); Solicitud de incorporación [#2798](https://github.com/pgbackrest/pgbackrest/pull/2798); Commit [`11f5582`](https://github.com/pgbackrest/pgbackrest/commit/11f5582dfe696187cab1f15d08f649a5117730b3)
- Añadir `archive-push-batch-size` para limitar el WAL enviado por ejecución asincrónica. (*Revisado por Stefan Fercot.*)

  En modo asincrónico, `archive-push-queue-max` solo se comprueba al inicio de una ejecución, por lo que al procesar un gran atraso la cola podía crecer muy por encima del límite. `archive-push-batch-size` (valor predeterminado 16GiB) limita el WAL enviado por ejecución para volver a comprobar la cola antes.

  Solicitud de incorporación [#2803](https://github.com/pgbackrest/pgbackrest/pull/2803); Commit [`34a035f`](https://github.com/pgbackrest/pgbackrest/commit/34a035f4d62f06822c1f60f72a605762cc1ad79c)
- Salir de `archive-push` asincrónico en el primer error. (*Revisado por Stefan Fercot. Sugerido por Lardière Sébastien.*)

  Cuando el repositorio no estaba disponible, el proceso asincrónico seguía intentando enviar cada segmento WAL listo. La ejecución podía durar lo suficiente para llenar `pg_wal` antes de volver a comprobar `archive-push-queue-max`. Ahora termina tras el primer error, una vez finalizados los trabajos en curso.

  Incidencia [#1848](https://github.com/pgbackrest/pgbackrest/issues/1848); Solicitud de incorporación [#2802](https://github.com/pgbackrest/pgbackrest/pull/2802); Commit [`a0c1435`](https://github.com/pgbackrest/pgbackrest/commit/a0c14359392e283d88f72e7f9f815d9e78ddfb10)
- Reforzar el análisis de respuestas HTTP por fragmentos. (*Contribución de Shubham. Revisado por David Steele.*)

  Ahora se aceptan extensiones de fragmentos y campos finales, `transfer-encoding` se compara sin distinguir mayúsculas de minúsculas y se rechaza una respuesta que incluya tanto `transfer-encoding` como `content-length`.

  Solicitud de incorporación [#2785](https://github.com/pgbackrest/pgbackrest/pull/2785); Commit [`34bba82`](https://github.com/pgbackrest/pgbackrest/commit/34bba828c6ba97579d65c2199c02d94bf31257a5)
- Generar un error al ejecutar como root a menos que `allow-root` esté habilitado. (*Revisado por Douglas J Hunley.*)

  Ejecutar como root un comando distinto de `restore` podía crear archivos en el repositorio, como `backup.info`, a los que el usuario de PostgreSQL no podía acceder. `allow-root` está desactivado por defecto para todos los comandos excepto `restore`, y la comprobación también se aplica en los hosts remotos.

  Incidencia [#1693](https://github.com/pgbackrest/pgbackrest/issues/1693); Solicitud de incorporación [#2812](https://github.com/pgbackrest/pgbackrest/pull/2812); Commit [`0daf53d`](https://github.com/pgbackrest/pgbackrest/commit/0daf53da03fb179b5771b6aaa559f9e0cc5842bb)
- Menos búsquedas binarias al construir el manifiesto. (*Contribución de Gunnar Lindholm. Revisado por David Steele.*)

  Al crear el manifiesto de una copia diferencial o incremental se buscaba tres veces cada archivo en el manifiesto anterior. Ahora solo se busca una vez, lo que ahorra millones de búsquedas en clústeres con millones de archivos.

  Solicitud de incorporación [#2774](https://github.com/pgbackrest/pgbackrest/pull/2774); Commit [`f1ef629`](https://github.com/pgbackrest/pgbackrest/commit/f1ef62956adabf305a7e959477ea1bb668fd8d65)
- Mejorar el rendimiento de seek durante la restauración delta incremental por bloques. (*Revisado por David Christensen, Douglas J Hunley.*)

  Durante una restauración delta incremental por bloques se hacía un posicionamiento y un vaciado del búfer de escritura por cada bloque escrito, que a menudo era de 8KiB. Ahora se lleva un seguimiento de la posición del archivo y solo se posiciona y vacía cuando es necesario.

  Solicitud de incorporación [#2732](https://github.com/pgbackrest/pgbackrest/pull/2732); Commit [`b908d5e`](https://github.com/pgbackrest/pgbackrest/commit/b908d5e2c5b37ef968f19e2c40a1001e19e5b87f)
- Agrupar los archivos de la copia de seguridad en orden en lugar de explorar buscando un mejor ajuste. (*Revisado por Stefan Fercot.*)

  Antes se omitía un archivo que haría superar `repo-bundle-size` y se elegía otro más pequeño de la cola. Ahora se añaden los archivos en orden y se cierra el grupo cuando alcanza `repo-bundle-size`, por lo que puede exceder ese tamaño hasta en `repo-bundle-limit`.

  Solicitud de incorporación [#2794](https://github.com/pgbackrest/pgbackrest/pull/2794); Commit [`253dbc3`](https://github.com/pgbackrest/pgbackrest/commit/253dbc3f03e5581c98bb97b252dc77b8defd3693)
- Reportar el error subyacente cuando una consulta no se completa. (*Revisado por Andrew Pogrebnoi. Sugerido por Marco Fontana.*)

  Si se perdía la conexión después de recibir el primer resultado de una consulta, por ejemplo bajo carga, se notificaba el error genérico "NULL result required to complete request". Ahora se informa del error de PostgreSQL, con indicaciones sobre conexiones perdidas y valores demasiado agresivos de `idle_session_timeout` e `idle_in_transaction_session_timeout`.

  Incidencia [#2789](https://github.com/pgbackrest/pgbackrest/issues/2789); Solicitud de incorporación [#2790](https://github.com/pgbackrest/pgbackrest/pull/2790); Commit [`23e966c`](https://github.com/pgbackrest/pgbackrest/commit/23e966cd8f17a8cd446b04901d0ae66ebf4118ee)
- Reportar el error real cuando falla una solicitud de credenciales de S3. (*Revisado por Douglas J Hunley. Sugerido por Mitchell Grice.*)

  Un error de AWS en una solicitud de credenciales `web-id` o `pod-id` se notificaba como un fallo al analizar la respuesta. Ahora se informa del error devuelto por AWS y se ocultan los tokens al registrar la solicitud.

  Incidencia [#1997](https://github.com/pgbackrest/pgbackrest/issues/1997); Solicitud de incorporación [#2808](https://github.com/pgbackrest/pgbackrest/pull/2808); Commit [`b0c57c2`](https://github.com/pgbackrest/pgbackrest/commit/b0c57c280d727e743b72a6d86e2c3e413307e44b)
- Reportar los errores de la ruta de spool de `archive-push` al registro de PostgreSQL. (*Revisado por Douglas J Hunley. Sugerido por Don Seiler.*)

  Si no se podía crear la ruta del spool asincrónico, por ejemplo por falta de permisos, el error no podía escribirse en el spool y `archive-push` fallaba con un tiempo de espera genérico que remitía al registro asincrónico. Ahora la ruta del spool se crea antes de iniciar el proceso asincrónico, de modo que el error aparece en el registro de PostgreSQL.

  Incidencia [#1408](https://github.com/pgbackrest/pgbackrest/issues/1408); Solicitud de incorporación [#2810](https://github.com/pgbackrest/pgbackrest/pull/2810); Commit [`7b0159c`](https://github.com/pgbackrest/pgbackrest/commit/7b0159c7dfd69763b63b1385fd564c18a4a5c1bc)
- Sugerir que pgBackRest puede estar desactualizado cuando no se soporta una versión.

  Cuando pgBackRest no reconoce una versión de PostgreSQL, por ejemplo al leer la copia de un clúster más reciente con un pgBackRest antiguo en el host de restauración, el error ahora sugiere que quizá sea necesario actualizar pgBackRest en todos los hosts. La versión se muestra en su forma habitual, por ejemplo 13 en lugar de 130000.

  Commit [`d4f697e`](https://github.com/pgbackrest/pgbackrest/commit/d4f697ebce705f9439798f970103fd38f829dfff)
- Añadir integración de notificaciones de systemd. (*Contribución de Andrew Jackson. Revisado por David Steele.*)

  Cuando se compila con `libsystemd`, el comando `server` avisa a systemd cuando está listo para aceptar conexiones y cuando se detiene, como hacen PostgreSQL y PgBouncer.

  Incidencia [#2757](https://github.com/pgbackrest/pgbackrest/issues/2757); Solicitud de incorporación [#2760](https://github.com/pgbackrest/pgbackrest/pull/2760); Commit [`742fff1`](https://github.com/pgbackrest/pgbackrest/commit/742fff174a3f5baaed932afa284334ca2aa1be82)
- Suprimir los errores `unused parameter` en los sondeos del compilador de meson. (*Contribución de Jörg Plate. Revisado por David Steele.*)

  Las comprobaciones del compilador de meson declaraban parámetros de `main()` que no utilizaban, lo que hacía fallar las comprobaciones cuando las advertencias por parámetros sin usar se trataban como errores.

  Incidencia [#2724](https://github.com/pgbackrest/pgbackrest/issues/2724); Commit [`d4465bd`](https://github.com/pgbackrest/pgbackrest/commit/d4465bd6f78d6d58d18ebedbe8f63b55d0ae2508)
- C11 es ahora el estándar mínimo de C. (*Revisado por Mohammad Ali Nazir Kosar.*)

  Solicitud de incorporación [#2738](https://github.com/pgbackrest/pgbackrest/pull/2738); Commit [`3a6c671`](https://github.com/pgbackrest/pgbackrest/commit/3a6c67183cd9c6a12c24f0d978ef5e501b7c3fcf)

**Mejoras en la documentación:**

- Hacer interna la opción `stanza` para los comandos `repo-*`. (*Revisado por Stefan Fercot.*)

  La opción `stanza` solo afecta a los comandos `repo-*` con constantes de rutas de almacenamiento no documentadas, por lo que la documentación daba a entender un efecto que no tenía. La opción ya no se documenta para estos comandos y sigue funcionando como antes.

  Incidencia [#2735](https://github.com/pgbackrest/pgbackrest/issues/2735); Commit [`3e9eabd`](https://github.com/pgbackrest/pgbackrest/commit/3e9eabd8a5551cdaeb6bc78a52f000eaf239defb)
- Documentar que info lee la configuración de cifrado de la sección global. (*Revisado por Stefan Fercot. Sugerido por Ron Johnson.*)

  Cuando se ejecuta sin `stanza`, el comando `info` solo lee los ajustes de cifrado de la sección global, por lo que los configurados para una stanza requieren indicar `stanza`.

  Incidencia [#1407](https://github.com/pgbackrest/pgbackrest/issues/1407); Solicitud de incorporación [#2805](https://github.com/pgbackrest/pgbackrest/pull/2805); Commit [`2137bda`](https://github.com/pgbackrest/pgbackrest/commit/2137bda1a5a1ad890d0137feffe8491102041af3)
- Documentar que `expire-auto` usa la configuración del comando `backup`. (*Revisado por Stefan Fercot. Sugerido por Lardière Sébastien.*)

  La caducidad automática tras una copia usa la configuración del comando `backup`, por lo que no se aplican las opciones definidas solo para `expire`. Desactiva `expire-auto` y ejecuta `expire` por separado cuando necesite su propia configuración.

  Incidencia [#1874](https://github.com/pgbackrest/pgbackrest/issues/1874); Solicitud de incorporación [#2807](https://github.com/pgbackrest/pgbackrest/pull/2807); Commit [`cf847f9`](https://github.com/pgbackrest/pgbackrest/commit/cf847f94cd7ab6517ec1abb30075fb53dc75d5f8)
- Documentar el ajuste de la directiva `su` de logrotate para un usuario dedicado. (*Revisado por Douglas J Hunley. Sugerido por lkanbus.*)

  Los paquetes pueden instalar una configuración de logrotate que rote los registros como el usuario `postgres`. Si un usuario dedicado es propietario del repositorio y de los registros, hay que cambiar la directiva `su` a ese usuario; de lo contrario, la rotación falla con un error de permisos.

  Incidencia [#2737](https://github.com/pgbackrest/pgbackrest/issues/2737); Solicitud de incorporación [#2809](https://github.com/pgbackrest/pgbackrest/pull/2809); Commit [`bde2c50`](https://github.com/pgbackrest/pgbackrest/commit/bde2c509c923fbe2844c10b0f95c55973378d2ae)
- Documentar que los comentarios al final de línea no están soportados en los archivos de configuración. (*Revisado por Douglas J Hunley. Sugerido por Alex Richman.*)

  Los comentarios al final de una línea nunca se han admitido, aunque parezcan funcionar con algunas opciones. Solo se admiten comentarios en una línea propia.

  Incidencia [#1633](https://github.com/pgbackrest/pgbackrest/issues/1633); Solicitud de incorporación [#2811](https://github.com/pgbackrest/pgbackrest/pull/2811); Commit [`8571799`](https://github.com/pgbackrest/pgbackrest/commit/85717992cadbfdabc571fb23914b62b08c7f6f44)

**Mejoras en la suite de pruebas:**

- Corregir conflictos de grupos de Alpine en los contenedores de CI. (*Contribución de Artur Zakirov. Revisado por David Steele.*)

  Ahora se manejan las entradas de grupo con miembros al renombrar el grupo de pruebas, y el grupo de Alpine solo se crea si todavía no existe.

  Solicitud de incorporación [#2784](https://github.com/pgbackrest/pgbackrest/pull/2784); Commit [`760dd8d`](https://github.com/pgbackrest/pgbackrest/commit/760dd8db69e7c6e5cbb9c5b7e2067b6813cf4497)

### Notas de la versión v2.58.0 {#v2580-release-notes}

*Mejoras en el almacenamiento de objetos*

*Publicada el 19 de enero de 2026*

**NOTA IMPORTANTE**: Los valores mínimos de la opción `repo-storage-upload-chunk-size` han aumentado. Ahora representan el mínimo permitido por los proveedores.

**Correcciones de errores:**

- Corregir un interbloqueo debido al registro en el manejador de señales. (*Corregido por Maxim Michkov. Revisado por David Steele.*)

  Una señal que llegara mientras `gmtime_r()` mantenía un bloqueo, como el SIGTERM enviado por `stop` con `--force`, podía provocar un interbloqueo cuando el manejador escribía en el registro. Ahora el manejador solo registra mediante funciones seguras para señales asincrónicas.

  Incidencia [#2710](https://github.com/pgbackrest/pgbackrest/issues/2710); Solicitud de incorporación [#2715](https://github.com/pgbackrest/pgbackrest/pull/2715); Commit [`e13c462`](https://github.com/pgbackrest/pgbackrest/commit/e13c462908c6ee25f8795b5d1373981549d4d5cf)

**Funcionalidades:**

- Soporte de HTTP para S3, GCS y Azure. (*Contribución de Will Morland. Revisado por David Steele.*)

  Ahora un endpoint de almacén de objetos puede comenzar por `http://` para conectarse sin TLS. Si el endpoint no indica un protocolo, se sigue utilizando HTTPS.

  Incidencia [#2340](https://github.com/pgbackrest/pgbackrest/issues/2340); Solicitud de incorporación [#2703](https://github.com/pgbackrest/pgbackrest/pull/2703); Commit [`2398dd4`](https://github.com/pgbackrest/pgbackrest/commit/2398dd4d432d312b3641e9fbbcbe0487ad43112d)
- Permitir la expiración de la copia de seguridad completa más antigua independientemente de la retención actual. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Ron Johnson.*)

  La opción `--oldest` de `expire` hace caducar la copia completa más antigua y las que dependen de ella independientemente de la retención configurada, por ejemplo cuando el repositorio se queda sin espacio. También caduca el WAL anterior a la copia completa más antigua que quede.

  Incidencia [#2666](https://github.com/pgbackrest/pgbackrest/issues/2666); Solicitud de incorporación [#2709](https://github.com/pgbackrest/pgbackrest/pull/2709); Commit [`bf2b276`](https://github.com/pgbackrest/pgbackrest/commit/bf2b276dc011464b13039630870934fd42ca473c)
- Soporte para identidades administradas de Azure. (*Contribución de Moiz Ibrar, Matthew Mols. Revisado por David Steele.*)

  Establece `repo-azure-key-type=auto` para obtener las credenciales automáticamente mediante identidades administradas en lugar de configurarlas. Las credenciales se renuevan antes de caducar.

  Incidencia [#2023](https://github.com/pgbackrest/pgbackrest/issues/2023); Solicitud de incorporación [#2712](https://github.com/pgbackrest/pgbackrest/pull/2712); Commit [`38f14d7`](https://github.com/pgbackrest/pgbackrest/commit/38f14d73b6a62d06e1ead7942e49a2bb2ae90dab)
- Soporte ***experimental*** de la identidad de pod de S3 EKS. (*Contribución de Pierre BOUTELOUP. Revisado por David Steele.*)

  Establece `repo-s3-key-type=pod-id` para obtener las credenciales automáticamente mediante la identidad de pods de EKS en lugar de configurarlas. Las credenciales se renuevan antes de caducar.

  Incidencia [#2718](https://github.com/pgbackrest/pgbackrest/issues/2718); Solicitud de incorporación [#2719](https://github.com/pgbackrest/pgbackrest/pull/2719); Commit [`79544f6`](https://github.com/pgbackrest/pgbackrest/commit/79544f64a3ce198f4685f923739def997fcafbce)
- Permitir la configuración de suites de cifrado TLS. (*Contribución de Gunnar "Nick" Bluth. Revisado por David Steele.*)

  Configura `tls-cipher-12` para TLS 1.2 y `tls-cipher-13` para TLS 1.3, por ejemplo por requisitos de cumplimiento. Las suites de cifrado se aplican a todas las conexiones que establece un proceso.

  [`fbc607a`](https://github.com/pgbackrest/pgbackrest/commit/fbc607a48b1fb4ae65c9f2691c44453f02aef2b8) Permitir la configuración de suites de cifrado TLS.; Incidencia [#2697](https://github.com/pgbackrest/pgbackrest/issues/2697); Solicitud de incorporación [#2700](https://github.com/pgbackrest/pgbackrest/pull/2700)

  [`91ad655`](https://github.com/pgbackrest/pgbackrest/commit/91ad65537f55aa3825b6c7b626a9e1b7cbb1ad4c) Corregir la inestabilidad de la prueba unitaria common/io-tls añadida en fbc607a4.
- Permitir establecer la prioridad del proceso. (*Revisado por Douglas J Hunley.*)

  `priority` establece la prioridad de planificación de los procesos pgBackRest entre -20 y 19, como `nice`. Un valor mayor reduce la probabilidad de que pgBackRest interfiera con PostgreSQL.

  Solicitud de incorporación [#2693](https://github.com/pgbackrest/pgbackrest/pull/2693); Commit [`0fc7e96`](https://github.com/pgbackrest/pgbackrest/commit/0fc7e96f5addb01e7f6f3585e37d209cc17dd956)

**Mejoras:**

- Permitir puntos en los nombres de bucket de S3 cuando se usan URI con estilo de ruta. (*Contribución de Joakim Hindersson. Revisado por David Steele.*)

  Los puntos en el nombre de un bucket solo causan discrepancias con el nombre de host del certificado en las URI de estilo host. Por ello, ahora se permiten con `repo-s3-uri-style=path`, que utilizan la mayoría de los servicios S3 autogestionados.

  Solicitud de incorporación [#2713](https://github.com/pgbackrest/pgbackrest/pull/2713); Commit [`3fdb4a1`](https://github.com/pgbackrest/pgbackrest/commit/3fdb4a1ea00b442aca5fc714818d293d57490386)
- Requerir TLS >= 1.2 a menos que la verificación esté deshabilitada. (*Revisado por Douglas J Hunley, Gunnar "Nick" Bluth.*)

  TLS 1.0 y 1.1 están obsoletos desde 2021. La verificación siempre está activada en las conexiones entre hosts pgBackRest. Si se desactiva para un almacén de objetos con `repo-storage-verify-tls`, por ejemplo para un certificado autofirmado, se permiten todas las versiones del protocolo.

  Solicitud de incorporación [#2720](https://github.com/pgbackrest/pgbackrest/pull/2720); Commit [`5b4b20a`](https://github.com/pgbackrest/pgbackrest/commit/5b4b20a8d7d17c2bffe106595310853e3f3a9604)
- Dimensionar dinámicamente los fragmentos de S3/GCS/Azure para cargas grandes. (*Revisado por Douglas J Hunley. Sugerido por Timothée Peignier.*)

  El número de fragmentos por carga es limitado, por lo que con el valor predeterminado de `repo-storage-upload-chunk-size` el archivo máximo era de 50GiB en S3, 40GiB en GCS y 200GiB en Azure. Ahora el tamaño del fragmento aumenta durante la carga, permitiendo archivos de hasta 5TiB en S3 y GCS y 45TiB en Azure.

  Incidencia [#2679](https://github.com/pgbackrest/pgbackrest/issues/2679); Solicitud de incorporación [#2701](https://github.com/pgbackrest/pgbackrest/pull/2701); Commit [`86554fa`](https://github.com/pgbackrest/pgbackrest/commit/86554faa707292855c2776a0c70b5e212b1e3945)
- Optimizar el tamaño de fragmento de S3/GCS/Azure para archivos pequeños. (*Revisado por Douglas J Hunley.*)

  Antes se reservaba todo el búfer del fragmento al abrir un archivo, aunque muchos archivos son menores que un fragmento. Ahora el búfer crece conforme llegan los datos, ahorrando memoria al cargar archivos pequeños.

  Solicitud de incorporación [#2705](https://github.com/pgbackrest/pgbackrest/pull/2705); Commit [`28bfa20`](https://github.com/pgbackrest/pgbackrest/commit/28bfa20ba3b860f72ba7ab6c018e37ada99e2109)
- Eliminar el soporte de PostgreSQL `9.5`. (*Revisado por Douglas J Hunley.*)

  PostgreSQL 9.5 deja de estar soportado, de acuerdo con la política de admitir cinco versiones de PostgreSQL que hayan llegado al final de su vida útil.

  Solicitud de incorporación [#2692](https://github.com/pgbackrest/pgbackrest/pull/2692); Commit [`5171e8b`](https://github.com/pgbackrest/pgbackrest/commit/5171e8bde31b9711c9c5b4ccc5170b61c5235548)
- Mejorar el registro del valor por defecto de opciones con una dependencia sin resolver. (*Revisado por Stefan Fercot.*)

  Una opción del archivo de configuración se registraba al iniciar un comando aunque no se resolviera su dependencia y se usara su valor predeterminado. Ahora no se registra en ese caso.

  Incidencia [#2707](https://github.com/pgbackrest/pgbackrest/issues/2707); Solicitud de incorporación [#2708](https://github.com/pgbackrest/pgbackrest/pull/2708); Commit [`38ac638`](https://github.com/pgbackrest/pgbackrest/commit/38ac6387cbbfc6f78a686de657e5a4de4ed59295)

**Mejoras en la documentación:**

- Eliminar la configuración explícita de `max_wal_senders`/`wal_level` de la guía de usuario. (*Sugerido por Jamie Nguyen.*)

  Desde PostgreSQL 10, `max_wal_senders` y `wal_level` tienen por defecto los valores que requiere la guía de usuario.

  Incidencia [#2699](https://github.com/pgbackrest/pgbackrest/issues/2699); Commit [`bce97d3`](https://github.com/pgbackrest/pgbackrest/commit/bce97d3ea80675b8eab3dbf692e8bc8f077f30c7)
- Aclarar que el agrupamiento es útil para sistemas de archivos con tamaños de bloque grandes. (*Sugerido por Ron Johnson.*)

  La agrupación ahorra espacio en sistemas de archivos con bloques grandes, donde cada archivo pequeño ocupa un bloque completo.

  Incidencia [#2706](https://github.com/pgbackrest/pgbackrest/issues/2706); Commit [`a7e5f28`](https://github.com/pgbackrest/pgbackrest/commit/a7e5f28511c27f2504a873db26803b26a84df8f1)

### Notas de la versión v2.57.0 {#v2570-release-notes}

*Supresión de enlaces simbólicos del repositorio*

*Publicada el 18 de octubre de 2025*

**Correcciones de errores:**

- Desanidar los tiempos de espera de HTTP/TLS/socket. (*Revisado por David Christensen.*)

  Una conexión de socket fallida también se reintentaba en las capas TLS y HTTP, de modo que, con `io-timeout` en su valor predeterminado de 60 segundos, la conexión tardaba nueve minutos en agotar el tiempo de espera. Ahora cada capa solo reintenta sus propios fallos.

  Incidencia [#2654](https://github.com/pgbackrest/pgbackrest/issues/2654); Solicitud de incorporación [#2662](https://github.com/pgbackrest/pgbackrest/pull/2662); Commit [`9c7f064`](https://github.com/pgbackrest/pgbackrest/commit/9c7f0648648e651d82918e5dbfc3d511abee3298)
- Corregir un posible segfault en el mensaje de error de la suma de verificación de páginas. (*Corregido por Zsolt Parragi. Revisado por David Steele.*)

  El mensaje de error de sumas de verificación de páginas no válidas utilizaba una cadena fuera de ámbito, lo que podía registrar basura o provocar un fallo. Era especialmente probable con pg_tde, ya que todos los archivos cifrados fallan la comprobación de páginas.

  Solicitud de incorporación [#2675](https://github.com/pgbackrest/pgbackrest/pull/2675); Commit [`adc5e5b`](https://github.com/pgbackrest/pgbackrest/commit/adc5e5b23b9b544745724a7eaa0461b88b691e36)
- Corregir un posible fallo de segmentación en los mensajes de reanudación de copias.

  El mensaje que explica por qué no se puede reanudar una copia utilizaba una cadena fuera de ámbito, lo que podía registrar basura o provocar un fallo.

  Commit [`c1c40a4`](https://github.com/pgbackrest/pgbackrest/commit/c1c40a4a851efe98be83aca2044c02fd1c7fb2ae)

**Funcionalidades:**

- Añadir la opción `repo-symlink` para suprimir la creación de enlaces simbólicos del repositorio. (*Revisado por Douglas J Hunley. Sugerido por Ron Johnson.*)

  Algunos sistemas de archivos compatibles con Posix en los demás aspectos no admiten enlaces simbólicos. Establece `repo-symlink=n` para evitar crear los enlaces `latest` y de espacios de tablas en el repositorio.

  Incidencia [#2673](https://github.com/pgbackrest/pgbackrest/issues/2673); Solicitud de incorporación [#2674](https://github.com/pgbackrest/pgbackrest/pull/2674); Commit [`bfd9790`](https://github.com/pgbackrest/pgbackrest/commit/bfd97907311a25ed239798691cff52cf73acdb83)

**Mejoras:**

- Añadir reintentos HTTP para los errores 408 y 429. (*Revisado por David Christensen.*)

  Ahora se reintentan los errores HTTP 408 (Request Timeout) y 429 (Too Many Requests). Los errores 429 son frecuentes en Cloudflare R2.

  Solicitud de incorporación [#2661](https://github.com/pgbackrest/pgbackrest/pull/2661); Commit [`8733900`](https://github.com/pgbackrest/pgbackrest/commit/87339004e59c03d2a03a6ceb8426202346849c37)

### Notas de la versión v2.56.0 {#v2560-release-notes}

*Mejoras en la información de progreso*

*Publicada el 21 de julio de 2025*

**Correcciones de errores:**

- Corregir un problema con la expiración ad hoc cuando no hay copias de seguridad en un repositorio. (*Revisado por Stefan Fercot. Reportado por Anup Gupta.*)

  La caducidad puntual fallaba con "cannot get index 0 from list with 0 value(s)" cuando el repositorio no tenía copias de seguridad.

  Incidencia [#2645](https://github.com/pgbackrest/pgbackrest/issues/2645); Solicitud de incorporación [#2646](https://github.com/pgbackrest/pgbackrest/pull/2646); Commit [`638815b`](https://github.com/pgbackrest/pgbackrest/commit/638815b4cde1ba1322516e256742c51676af66f0)

**Funcionalidades:**

- Añadir el progreso de restauración a la salida del comando `info`. (*Contribución de Denis Garsh, Maxim Michkov. Revisado por David Steele.*)

  El comando `restore` ahora registra su progreso, que `info` muestra junto al de las copias de seguridad. Además, el comando `stop` ya no termina una restauración.

  Incidencia [#2546](https://github.com/pgbackrest/pgbackrest/issues/2546); Solicitud de incorporación [#2652](https://github.com/pgbackrest/pgbackrest/pull/2652); Commit [`8cdd9ce`](https://github.com/pgbackrest/pgbackrest/commit/8cdd9ce1c4ab6cca508932a41a3013374d7547ef)
- Añadir un nivel de detalle de solo progreso para la salida del comando `info`. (*Contribución de Denis Garsh. Revisado por David Steele, Stefan Fercot.*)

  Establece `--detail-level=progress` para mostrar solo el progreso. Es más rápido porque no se lee el repositorio. El valor predeterminado es `full`.

  Solicitud de incorporación [#2550](https://github.com/pgbackrest/pgbackrest/pull/2550); Commit [`2706168`](https://github.com/pgbackrest/pgbackrest/commit/2706168f609af544b0453d384c7fb620626fc205)

**Mejoras:**

- Reintentar lecturas fallidas en almacenes de objetos. (*Revisado por David Christensen.*)

  Una lectura de un almacén de objetos que fallaba después de iniciarse era un error fatal y podía obligar a reiniciar un trabajo costoso, por ejemplo durante una restauración. Ahora se reintenta desde el punto donde se interrumpió.

  Solicitud de incorporación [#2642](https://github.com/pgbackrest/pgbackrest/pull/2642); Commit [`5e14692`](https://github.com/pgbackrest/pgbackrest/commit/5e14692588b9fd8a566c9a1795c866ba2e83eebd)
- Corregir los valores por defecto en la ayuda de línea de comandos. (*Revisado por David Christensen, Chris Bandy.*)

  Cuando una opción tiene varios valores predeterminados, como `repo-storage-upload-chunk-size` con repositorios S3 y Azure, la lista de opciones muestra `<multi>` y la ayuda de la opción enumera cada valor. No se muestran valores predeterminados para las opciones que no sean válidas en la configuración actual.

  Solicitud de incorporación [#2625](https://github.com/pgbackrest/pgbackrest/pull/2625); Commit [`8737cad`](https://github.com/pgbackrest/pgbackrest/commit/8737cad566974c37529595715ecdc06571420752)

**Mejoras en la documentación:**

- Describir los valores discretos de las opciones en una lista donde corresponda. (*Contribución de Anton Kurochkin. Revisado por David Steele.*)

  Los valores de opciones como `output` para `verify` y `version` ahora se describen mediante una lista, como en las demás opciones.

  Solicitud de incorporación [#2638](https://github.com/pgbackrest/pgbackrest/pull/2638); Commit [`2e76e9f`](https://github.com/pgbackrest/pgbackrest/commit/2e76e9fc699d22286f6bf05fddc271d8fa22523e)
- Corregir «menor que» en la salida de ayuda de la opción `archive-mode`. (*Contribución de Anton Kurochkin. Revisado por David Steele.*)

  Solicitud de incorporación [#2633](https://github.com/pgbackrest/pgbackrest/pull/2633); Commit [`cb67322`](https://github.com/pgbackrest/pgbackrest/commit/cb673225e90604a8865ce30c188d15661f945e5e)

### Notas de la versión v2.55.1 {#v2551-release-notes}

*Correcciones de errores*

*Publicada el 5 de mayo de 2025*

**Correcciones de errores:**

- Revertir «calcular content-md5 en S3 solo cuando sea necesario». (*Revisado por David Christensen. Reportado por Frank Brendel.*)

  S3 exige `content-md5` o una suma `x-amz-content-*` al cargar con el bloqueo de objetos activado, y Scality no aceptaba las sumas alternativas, por lo que las cargas fallaban. Se vuelve a calcular `content-md5` para todas las solicitudes con contenido.

  Incidencia [#2613](https://github.com/pgbackrest/pgbackrest/issues/2613); Solicitud de incorporación [#2615](https://github.com/pgbackrest/pgbackrest/pull/2615); Commit [`8bbb982`](https://github.com/pgbackrest/pgbackrest/commit/8bbb98243566bfa052f6aacfd1bd3a6acd770e40)
- Corregir la comprobación de los límites inferiores de las claves de opción. (*Revisado por David Christensen, Wolfgang Walther. Reportado por Wolfgang Walther.*)

  Una opción indexada con clave 0, como `pg0-path`, provocaba un fallo de segmentación. Ahora se notifica un error.

  Incidencia [#2610](https://github.com/pgbackrest/pgbackrest/issues/2610); Solicitud de incorporación [#2611](https://github.com/pgbackrest/pgbackrest/pull/2611); Commit [`5e01098`](https://github.com/pgbackrest/pgbackrest/commit/5e01098617a3803067b153be2d41e023cd4d95e4)

### Notas de la versión v2.55.0 {#v2550-release-notes}

*Mejoras de verificación y soporte de PostgreSQL 18*

*Publicada el 21 de abril de 2025*

**Correcciones de errores:**

- Corregir un problema de restauración incremental por bloques en un repositorio no predeterminado. (*Revisado por David Christensen. Probado por Aleksander Łukasz. Reportado por Aleksander Łukasz.*)

  Cuando la copia restaurada usaba incrementales por bloques y no estaba en el repositorio de menor número, se leía parte de sus datos incrementales desde ese repositorio de menor número. Configurar `repo` permitía evitar el problema.

  Incidencia [#2577](https://github.com/pgbackrest/pgbackrest/issues/2577); Solicitud de incorporación [#2579](https://github.com/pgbackrest/pgbackrest/pull/2579); Commit [`5d2c67c`](https://github.com/pgbackrest/pgbackrest/commit/5d2c67c3c6975ea3ed08c7425f6e410ae378913f)
- No establecer `recovery_target_timeline=current` para PostgreSQL < 12. (*Revisado por Stefan Fercot.*)

  Antes de PostgreSQL 12, establecer explícitamente `recovery_target_timeline` en `current` se comporta como `latest`, aunque `current` sea el valor predeterminado. Ahora se omite este ajuste de `recovery.conf` si está en `current` para esas versiones.

  Solicitud de incorporación [#2533](https://github.com/pgbackrest/pgbackrest/pull/2533); Commit [`6fbb28f`](https://github.com/pgbackrest/pgbackrest/commit/6fbb28fa2d615576be78376c7f539921f6b8bc6a)
- Corregir el registro del rango de archivado en expire. (*Revisado por Stefan Fercot. Reportado por Aleš Zelený.*)

  Solo se registraba la última ruta de archivo eliminada como inicio del rango, por lo que el registro parecía indicar que habían caducado muchos menos archivos de los reales.

  Incidencia [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Solicitud de incorporación [#2554](https://github.com/pgbackrest/pgbackrest/pull/2554); Commit [`47f050f`](https://github.com/pgbackrest/pgbackrest/commit/47f050f8fd816e57326d881f4253d8a13c0f8da6)
- Corregir el reporte de errores para consultas sin resultados. (*Revisado por Stefan Fercot. Reportado por Susantha Bathige.*)

  Un error de una consulta que no debía devolver resultados se notificaba como un resultado inesperado en lugar de como el error.

  Solicitud de incorporación [#2539](https://github.com/pgbackrest/pgbackrest/pull/2539); Commit [`d5cefb7`](https://github.com/pgbackrest/pgbackrest/commit/d5cefb7290c34c64a2b9aa89ff04a718df4ec18b)

**Funcionalidades:**

- Verificar la línea de tiempo objetivo de recuperación. (*Revisado por Stefan Fercot.*)

  Una copia que no podía seguir la línea temporal de destino, por ejemplo creada después de promover un servidor en espera y bifurcar la nueva línea temporal, solo fallaba al comenzar la recuperación, con un error de PostgreSQL difícil de interpretar. Ahora se comprueba la línea temporal con los archivos de historial antes de iniciar la restauración.

  Solicitud de incorporación [#2534](https://github.com/pgbackrest/pgbackrest/pull/2534); Commit [`922e9f0`](https://github.com/pgbackrest/pgbackrest/commit/922e9f0775c39b64e009251a6bec8ef9b83c190f)
- Permitir la verificación de una copia de seguridad especificada. (*Contribución de Maxim Michkov. Revisado por David Steele.*)

  La opción `--set` de `verify` verifica únicamente la copia indicada y el WAL necesario para hacerla coherente.

  Incidencia [#2419](https://github.com/pgbackrest/pgbackrest/issues/2419); Solicitud de incorporación [#2544](https://github.com/pgbackrest/pgbackrest/pull/2544); Commit [`e4def88`](https://github.com/pgbackrest/pgbackrest/commit/e4def8845eb5c3fe9fb8cc44d9f64766cfb348c2)
- Añadir soporte para requester pays de S3/GCS. (*Contribución de Timothée Peignier. Revisado por David Steele.*)

  Establece `repo-s3-requester-pays` o `repo-gcs-user-project` para facturar al solicitante en lugar de al propietario del bucket, por ejemplo para que un servicio alojado dé acceso a sus clientes a sus propias copias.

  [`4db0263`](https://github.com/pgbackrest/pgbackrest/commit/4db0263fd63274a8168eb4de17b320d2f86251a2) Añadir soporte del pago por el solicitante en S3.; Solicitud de incorporación [#2560](https://github.com/pgbackrest/pgbackrest/pull/2560)

  [`814bf48`](https://github.com/pgbackrest/pgbackrest/commit/814bf487c3955e877d226faaa22324d3c79863b2) Añadir soporte del pago por el solicitante en GCS.; Solicitud de incorporación [#2557](https://github.com/pgbackrest/pgbackrest/pull/2557)
- Soporte de PostgreSQL 18. (*Revisado por Stefan Fercot.*)

  Esta versión se publicó antes de que PostgreSQL 18 tuviera una beta, por lo que el soporte era inicialmente experimental. No hubo cambios que afectaran a pgBackRest antes de PostgreSQL 18.0.

  Solicitud de incorporación [#2603](https://github.com/pgbackrest/pgbackrest/pull/2603); Commit [`565d2e0`](https://github.com/pgbackrest/pgbackrest/commit/565d2e0c47cd21df890a40b3a94a8c865bed76d9)
- Permitir conexiones a PostgreSQL en sockets de dominio abstractos. (*Probado por Chris Bandy. Sugerido por Chris Bandy.*)

  `pg-socket-path` ya no tiene que ser una ruta absoluta, por lo que puede indicar un socket de dominio abstracto. libpq informa si la ruta no es válida.

  Incidencia [#2529](https://github.com/pgbackrest/pgbackrest/issues/2529); Solicitud de incorporación [#2535](https://github.com/pgbackrest/pgbackrest/pull/2535); Commit [`68f22ae`](https://github.com/pgbackrest/pgbackrest/commit/68f22aea6665b9dcbe76dbfaa731f37187e1ce20)
- Añadir salida numérica al comando `version`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Establece `--output=num` para mostrar la versión como un número, por ejemplo 2055000, lo que facilita compararla.

  Incidencia [#2410](https://github.com/pgbackrest/pgbackrest/issues/2410); Solicitud de incorporación [#2526](https://github.com/pgbackrest/pgbackrest/pull/2526); Commit [`750a051`](https://github.com/pgbackrest/pgbackrest/commit/750a051b7aeccc3dd7ae9c07af2c73cb25057de9)

**Mejoras:**

- Permitir que el comando backup opere en repositorios remotos. (*Revisado por Stefan Fercot.*)

  Ahora `backup` puede ejecutarse en un host cuyo repositorio sea remoto, lo que permite más flexibilidad al elegir dónde ejecutar las copias.

  [`4a94b6b`](https://github.com/pgbackrest/pgbackrest/commit/4a94b6bef9108ab775c0070571a1fb7dd8883eeb) Refactorizar el ayudante del protocolo.

  [`931435c`](https://github.com/pgbackrest/pgbackrest/commit/931435c0177ded2189903385d520d5c8819c4f5e) Permitir que el comando backup opere en repositorios remotos.; Solicitud de incorporación [#2512](https://github.com/pgbackrest/pgbackrest/pull/2512)
- Usar lz4 para la compresión del protocolo. (*Revisado por Stefan Fercot.*)

  lz4 comprime mucho más rápido que gz y ofrece tasas similares en los niveles bajos usados para comprimir el protocolo. Establecer `compress-level-network=0` ya no desactiva la compresión del protocolo.

  [`0577b03`](https://github.com/pgbackrest/pgbackrest/commit/0577b0301689bc19d49c4081cc652971de5da8cf) Usar lz4 para la compresión del protocolo.; Solicitud de incorporación [#2488](https://github.com/pgbackrest/pgbackrest/pull/2488)

  [`5c8296d`](https://github.com/pgbackrest/pgbackrest/commit/5c8296df066564be35d3936610ebff1c332f38da) Eliminar de la documentación la referencia a desactivar la compresión de red.
- Calcular `content-md5` en S3 solo cuando sea necesario. (*Revisado por David Christensen.*)

  Para ahorrar CPU al cargar archivos, el encabezado `content-md5` solo se calcula para las solicitudes de eliminación por lotes, que lo requieren. Este cambio se revirtió en v2.55.1.

  Solicitud de incorporación [#2592](https://github.com/pgbackrest/pgbackrest/pull/2592); Commit [`20bfd14`](https://github.com/pgbackrest/pgbackrest/commit/20bfd14b73ad6d75b6fb1169565b18dcfa183c9b)
- Advertir cuando se sobrescribe el valor de una opción multi-clave. (*Revisado por David Christensen, Stefan Fercot.*)

  Las opciones con pares clave/valor, como `recovery-option`, sobrescribían silenciosamente un valor al repetir su clave. Ahora se registra una advertencia.

  Incidencia [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Solicitud de incorporación [#2594](https://github.com/pgbackrest/pgbackrest/pull/2594); Commit [`cab4d6f`](https://github.com/pgbackrest/pgbackrest/commit/cab4d6fd5c775d6e1a9cd9889d825eee667b5322)
- Añadir registro de detalle para la ruta de archivado expirada. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  La eliminación de muchos archivos de archivado podía parecer un bloqueo. Ahora un mensaje de nivel detail muestra el progreso.

  [`4dcfa9e`](https://github.com/pgbackrest/pgbackrest/commit/4dcfa9ef59c5e75c6c0ee83390c64b9a3d4af1fc) Añadir registro de nivel detail a la prueba de caducidad.

  [`2155a12`](https://github.com/pgbackrest/pgbackrest/commit/2155a12a3d861645de5618518350f90962fbc26d) Añadir registro de detalle para la ruta de archivado expirada.; Incidencia [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); Solicitud de incorporación [#2559](https://github.com/pgbackrest/pgbackrest/pull/2559)
- Eliminar el soporte de PostgreSQL `9.4`. (*Revisado por Stefan Fercot.*)

  PostgreSQL 9.4 deja de estar soportado conforme a la política de admitir cinco versiones de PostgreSQL que hayan llegado al final de su vida útil. Todavía se pueden caducar copias de clústeres 9.4.

  Solicitud de incorporación [#2472](https://github.com/pgbackrest/pgbackrest/pull/2472); Commit [`48f511d`](https://github.com/pgbackrest/pgbackrest/commit/48f511dad339ef9357e00f7bd8e2bf4b7c800dd4)
- Eliminar la compilación con autoconf/make. (*Revisado por David Christensen.*)

  v2.54.0 fue la última versión compatible con la compilación mediante autoconf/make. Utiliza meson para compilar.

  Solicitud de incorporación [#2470](https://github.com/pgbackrest/pgbackrest/pull/2470); Commit [`89c9bab`](https://github.com/pgbackrest/pgbackrest/commit/89c9baba72fc99616083a7adc4be2c3e2bf9e4dd)

**Mejoras en la documentación:**

- Corregir la documentación sobre cómo especificar varias stanzas con `tls-server-auth`. (*Revisado por David Christensen, Stefan Fercot. Sugerido por Terry MacAndrew.*)

  Para indicar varias stanzas en `tls-server-auth` se utiliza una lista separada por comas. La documentación decía que se repitiera la opción.

  Incidencia [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); Solicitud de incorporación [#2595](https://github.com/pgbackrest/pgbackrest/pull/2595); Commit [`53a45d2`](https://github.com/pgbackrest/pgbackrest/commit/53a45d25c3e60e5067010b2676f5d6216638fbe3)
- Aclarar la expiración de copias de seguridad incrementales. (*Revisado por Stefan Fercot.*)

  La documentación daba a entender que las copias incrementales caducaban por cantidad. Ahora explica cómo caducan y que las copias completas cuentan como diferenciales para la retención diferencial.

  Solicitud de incorporación [#2601](https://github.com/pgbackrest/pgbackrest/pull/2601); Commit [`8bdba74`](https://github.com/pgbackrest/pgbackrest/commit/8bdba747981e8805a9bf355050f70cdf19e9babc)
- Aclarar el requisito de que las versiones local/remota de pgBackRest coincidan. (*Contribución de Greg Clough. Revisado por David Steele.*)

  Incidencia [#2540](https://github.com/pgbackrest/pgbackrest/issues/2540); Solicitud de incorporación [#2541](https://github.com/pgbackrest/pgbackrest/pull/2541); Commit [`82299eb`](https://github.com/pgbackrest/pgbackrest/commit/82299eb4cd997524eeddef170ad99669ed6651cf)
- Añadir una pregunta frecuente sobre cómo exportar un clúster autocontenido. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Las preguntas frecuentes explican cómo crear una exportación autosuficiente de un clúster con una copia realizada con `--archive-copy` y restaurada con `--type=none`.

  Solicitud de incorporación [#2605](https://github.com/pgbackrest/pgbackrest/pull/2605); Commit [`9386920`](https://github.com/pgbackrest/pgbackrest/commit/9386920b79971347c6c57589190bf09b591d8b4d)
- Advertir sobre `--tablespace-map-all` respecto a la creación de tablespaces. (*Revisado por Stefan Fercot, Christophe Courtois. Sugerido por Christophe Courtois.*)

  Un espacio de tablas creado después de iniciar la copia no figura en el manifiesto, por lo que `tablespace-map-all` no puede asignarle una ruta.

  Solicitud de incorporación [#2538](https://github.com/pgbackrest/pgbackrest/pull/2538); Commit [`e625ed8`](https://github.com/pgbackrest/pgbackrest/commit/e625ed8be2228cb99c3801f9d1776909a2201c5a)
- Aclarar el comportamiento de `--repo-retention-full-type`. (*Revisado por Antoine Beaupré. Sugerido por Antoine Beaupré.*)

  Incidencia [#2562](https://github.com/pgbackrest/pgbackrest/issues/2562); Solicitud de incorporación [#2583](https://github.com/pgbackrest/pgbackrest/pull/2583); Commit [`84eb9a7`](https://github.com/pgbackrest/pgbackrest/commit/84eb9a742dcf75f071e011946263dedaa985099e)
- Cambiar la recomendación de `--process-max` para almacenes de objetos a `--repo-bundle`. (*Revisado por Stefan Fercot.*)

  En almacenes de objetos, `repo-bundle` reduce el tiempo de creación de archivos mucho más que `process-max`, porque se crean menos archivos.

  Solicitud de incorporación [#2542](https://github.com/pgbackrest/pgbackrest/pull/2542); Commit [`aa7210a`](https://github.com/pgbackrest/pgbackrest/commit/aa7210a1830825e0a3e6b6740937357341127a6f)
- Actualizar `unix_socket_directory` a `unix_socket_directories`. (*Contribución de hyunkyu han. Revisado por David Steele.*)

  `unix_socket_directory` no es válido desde PostgreSQL 9.2, por lo que solo se documenta `unix_socket_directories`.

  Incidencia [#2589](https://github.com/pgbackrest/pgbackrest/issues/2589); Commit [`b28ae98`](https://github.com/pgbackrest/pgbackrest/commit/b28ae98cec7ae7e881e6476c1cba1ba7e1abc358)
- Recomendar no colocar `spool-path` dentro de `pg_xlog`/`pg_wal`. (*Revisado por Martín Marqués, Don Seiler. Sugerido por Martín Marqués.*)

  Una ruta de spool dentro de `pg_xlog` o `pg_wal` puede causar problemas a herramientas de PostgreSQL como `pg_rewind`.

  Solicitud de incorporación [#2600](https://github.com/pgbackrest/pgbackrest/pull/2600); Commit [`dd3a7d9`](https://github.com/pgbackrest/pgbackrest/commit/dd3a7d99a78d0d604967d90e8a8dbf8915432896)

### Notas de la versión v2.54.2 {#v2542-release-notes}

*Corrección de error*

*Publicada el 20 de enero de 2025*

**Correcciones de errores:**

- Corregir un problema tras deshabilitar el agrupamiento con el incremental por bloques habilitado. (*Revisado por David Christensen.*)

  Si se desactivaba la agrupación después de realizar copias con agrupación e incrementales por bloques, no podían leerse las copias anteriores. Ahora se conserva el ajuste necesario para leerlas.

  Solicitud de incorporación [#2511](https://github.com/pgbackrest/pgbackrest/pull/2511); Commit [`dbc6f28`](https://github.com/pgbackrest/pgbackrest/commit/dbc6f2875356ec16cf4883830a0d7b00204752ee)

**Mejoras en la documentación:**

- Aclarar el comportamiento de múltiples archivos de configuración. (*Revisado por Paul Bierly. Sugerido por Paul Bierly.*)

  Cada archivo de configuración debe ser válido por sí mismo, por lo que hay que declarar la sección en cada archivo que establezca opciones en ella. La documentación también señala que no se admiten comillas, se recortan los espacios en claves y valores y se combinan las secciones repetidas.

  Commit [`5da2df4`](https://github.com/pgbackrest/pgbackrest/commit/5da2df4a933f04d5fb9a3b6c7c59529f3afa805b)

### Notas de la versión v2.54.1 {#v2541-release-notes}

*Corrección de error*

*Publicada el 16 de diciembre de 2024*

**Correcciones de errores:**

- Corregir un problema por el que los comandos `version`/`help` intentaban cargar `pgbackrest.conf`. (*Revisado por Stefan Fercot. Reportado por Bradford Boyle, Julian.*)

  En v2.54.0, los comandos `version` y `help` cargaban `pgbackrest.conf` y fallaban si no podían leerlo o analizarlo.

  Incidencia [#2476](https://github.com/pgbackrest/pgbackrest/issues/2476); Solicitud de incorporación [#2477](https://github.com/pgbackrest/pgbackrest/pull/2477); Commit [`8d69118`](https://github.com/pgbackrest/pgbackrest/commit/8d6911898afd75c586ef70c6d8559b1e5959a155)

**Mejoras en la suite de pruebas:**

- Estabilizar el archivado asincrónico en las pruebas de integración. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)

  Un `archive-get` asincrónico que quedaba ejecutándose tras una prueba de integración podía escribir un error en la cola de la siguiente prueba y hacer fallar su recuperación.

  Incidencia [#2463](https://github.com/pgbackrest/pgbackrest/issues/2463); Solicitud de incorporación [#2481](https://github.com/pgbackrest/pgbackrest/pull/2481); Commit [`b90ce9e`](https://github.com/pgbackrest/pgbackrest/commit/b90ce9eb8c7cd9e9b131477a377249a3d3fda181)

### Notas de la versión v2.54.0 {#v2540-release-notes}

*Tiempo objetivo para el almacenamiento con versionado*

*Publicada el 21 de octubre de 2024*

**NOTA PARA EMPAQUETADORES**: Esta es la última versión de funcionalidades que soporta la compilación con autoconf/make. Migra a meson si aún no lo has hecho. Las versiones de parche 2.54.X (si las hay) seguirán soportando autoconf/make.

**Correcciones de errores:**

- Corregir el rendimiento de las consultas de PostgreSQL para conjuntos de datos grandes. (*Corregido por Thibault Vincent, David Steele. Revisado por David Christensen. Probado por Antoine Millet. Reportado por Antoine Millet.*)

  La lógica de tiempo de espera de las consultas retrasaba la lectura de resultados, lo que podía hacer que una consulta con un resultado grande tardara hasta `db-timeout`. Ahora se leen los resultados en cuanto están disponibles.

  [`6ac4e8d`](https://github.com/pgbackrest/pgbackrest/commit/6ac4e8dd78f16e93300f7747c4bc8fa8e1a0558b) Mover el shim del módulo fd a la prueba del módulo io.

  [`77ae753`](https://github.com/pgbackrest/pgbackrest/commit/77ae753ef59bd40b9867be21e8519093786c3b85) Permitir ejecutar el shim de fdReady() una sola vez con un valor de retorno determinado.

  [`33fa396`](https://github.com/pgbackrest/pgbackrest/commit/33fa3965616b1432e5d1d59c489302fa4891a39e) Refactorizar el objeto Wait para exponer la espera restante mediante waitRemains().

  [`c8ccaaa`](https://github.com/pgbackrest/pgbackrest/commit/c8ccaaa755993e3fd5e87148bd0a991acb3050c3) Corregir el rendimiento de las consultas de PostgreSQL para conjuntos de datos grandes.; Incidencia [#2458](https://github.com/pgbackrest/pgbackrest/issues/2458); Solicitud de incorporación [#2459](https://github.com/pgbackrest/pgbackrest/pull/2459)

**Funcionalidades:**

- Permitir que los repositorios en almacenamiento con versionado se lean en un tiempo objetivo. (*Revisado por Stefan Fercot, David Christensen.*)

  Los comandos `archive-get`, `info`, `repo-get`, `repo-ls`, `restore` y `verify` pueden leer un repositorio en almacenamiento Azure, GCS o S3 con versiones tal como estaba en `repo-target-time`. Esto permite recuperarse incluso si el repositorio se ha eliminado o corrompido, accidentalmente o de forma maliciosa.

  Solicitud de incorporación [#2404](https://github.com/pgbackrest/pgbackrest/pull/2404); Commit [`b19134d`](https://github.com/pgbackrest/pgbackrest/commit/b19134dccd5d0dab87b5d45b443f481df00370b1)
- Permitir que una copia de seguridad desde réplica solicitada continúe sin réplica. (*Revisado por Stefan Fercot.*)

  Establece `backup-standby=prefer` para copiar desde un servidor en espera cuando esté disponible y, en caso contrario, desde el primario. Esto no resuelve el caso en que el servidor en espera responde pero no logra sincronizarse con el primario después de iniciar la copia.

  Solicitud de incorporación [#2378](https://github.com/pgbackrest/pgbackrest/pull/2378); Commit [`a42629f`](https://github.com/pgbackrest/pgbackrest/commit/a42629f87ab70ffaee8d1241eb50c5ea7154a87d)

**Mejoras:**

- Resumir la lista de referencias de la copia de seguridad en la salida de texto del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  La lista de referencias de una copia puede ser muy larga, por lo que la salida de texto de `info` ahora la resume. Se muestra completa al indicar `--set`.

  Solicitud de incorporación [#2399](https://github.com/pgbackrest/pgbackrest/pull/2399); Commit [`b306f83`](https://github.com/pgbackrest/pgbackrest/commit/b306f83493cc859ad15c8f175fc6db2321b79340)
- Refrescar el token web-id en cada autenticación de S3. (*Contribución de Brent Graveland. Revisado por David Steele.*)

  El archivo de token indicado por `AWS_WEB_IDENTITY_TOKEN_FILE` solo se leía al iniciar, por lo que el token podía caducar durante una operación larga. Ahora se lee en cada autenticación.

  Incidencia [#2428](https://github.com/pgbackrest/pgbackrest/issues/2428); Solicitud de incorporación [#2429](https://github.com/pgbackrest/pgbackrest/pull/2429); Commit [`95a4b9e`](https://github.com/pgbackrest/pgbackrest/commit/95a4b9e10a3f7a26ebaae22fc6abd79cee14189a)
- Mostrar correctamente los valores actuales de las opciones indexadas en la ayuda. (*Revisado por David Christensen.*)

  El valor actual mostrado para una opción indexada siempre era el del primer índice, por ejemplo `pg1-path`. Ahora la ayuda enumera el valor de cada índice y la lista de opciones muestra `<multi>` cuando hay más de uno.

  Solicitud de incorporación [#2453](https://github.com/pgbackrest/pgbackrest/pull/2453); Commit [`b3ca2e3`](https://github.com/pgbackrest/pgbackrest/commit/b3ca2e34823b28862d999f87c4d7346707952a5b)
- Guardar `backup.info` solo cuando el contenido haya cambiado. (*Revisado por Stefan Fercot.*)

  `expire` guardaba `backup.info` aunque no hubiera cambiado. Reducir las escrituras también facilita elegir un momento de destino en almacenamiento con versiones.

  Solicitud de incorporación [#2403](https://github.com/pgbackrest/pgbackrest/pull/2403); Commit [`b454b9e`](https://github.com/pgbackrest/pgbackrest/commit/b454b9e403526b1f352df964d9206c27d2397df3)
- Eliminar la limitación de lectura de archivos en paralelo durante la restauración. (*Revisado por David Christensen.*)

  El protocolo solo podía leer o escribir un archivo a la vez en un remoto, por lo que una restauración leía los archivos del repositorio de uno en uno. Ahora se pueden multiplexar los comandos del protocolo y leer varios archivos a la vez, por ejemplo un grupo y los datos incrementales por bloques de uno de sus archivos.

  [`df8cbc9`](https://github.com/pgbackrest/pgbackrest/commit/df8cbc91c348bc2f746767c87ac5626460fb6f39) Multiplexación de comandos del protocolo.; Solicitud de incorporación [#2108](https://github.com/pgbackrest/pgbackrest/pull/2108)

  [`46c1297`](https://github.com/pgbackrest/pgbackrest/commit/46c1297be344909e900be596a865064233da9f87) Eliminar la limitación de lectura de archivos en paralelo durante la restauración.; Solicitud de incorporación [#2436](https://github.com/pgbackrest/pgbackrest/pull/2436)
- Mejorar los mensajes de error de SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Los errores SFTP solo se notificaban como números. Ahora incluyen una descripción.

  Solicitud de incorporación [#2439](https://github.com/pgbackrest/pgbackrest/pull/2439); Commit [`70bda2c`](https://github.com/pgbackrest/pgbackrest/commit/70bda2cfb21130eb589a87cb419fb5f22a71c78a)

**Funcionalidades de la documentación:**

- Añadir una sección de ajuste de rendimiento a la guía de usuario. (*Revisado por Stefan Fercot.*)

  Las opciones que suelen mejorar el rendimiento estaban dispersas por la documentación. La guía de inicio rápido ahora incluye una sección que las enumera.

  Solicitud de incorporación [#2446](https://github.com/pgbackrest/pgbackrest/pull/2446); Commit [`278319e`](https://github.com/pgbackrest/pgbackrest/commit/278319eba3444070123d3f0f277be9234604d937)

**Mejoras en la documentación:**

- Aclarar el origen de `data_directory`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Matthias.*)

  `pg-path` debe coincidir con el `data_directory` que informa PostgreSQL, que puede diferir del valor de `postgresql.conf`.

  Incidencia [#2464](https://github.com/pgbackrest/pgbackrest/issues/2464); Solicitud de incorporación [#2467](https://github.com/pgbackrest/pgbackrest/pull/2467); Commit [`9ba2db0`](https://github.com/pgbackrest/pgbackrest/commit/9ba2db017348d304f96ce89592fc01f29197e136)
- Mejor lógica para decidir cuándo un resumen debe ir en minúsculas. (*Sugerido por Daniel Westermann.*)

  Los resúmenes que comienzan por un nombre propio o una sigla, como PostgreSQL, ya no se convierten a minúsculas en la documentación.

  Incidencia [#2462](https://github.com/pgbackrest/pgbackrest/issues/2462); Commit [`eb2f279`](https://github.com/pgbackrest/pgbackrest/commit/eb2f279a2998d1ed893c5d8984590ab4997a5f32)

### Notas de la versión v2.53.1 {#v2531-release-notes}

*Soporte de PostgreSQL 17*

*Publicada el 19 de agosto de 2024*

**Correcciones de errores:**

- Corregir los permisos cuando `restore` se ejecuta como usuario root. (*Revisado por Stefan Fercot. Reportado por Will M.*)

  Al ejecutar `restore` como root, `pg_control` quedaba propiedad de root. La restauración como root también fallaba si no existía la ruta base.

  Incidencia [#2407](https://github.com/pgbackrest/pgbackrest/issues/2407); Solicitud de incorporación [#2416](https://github.com/pgbackrest/pgbackrest/pull/2416); Commit [`7bd8da4`](https://github.com/pgbackrest/pgbackrest/commit/7bd8da4eecb0ce1461854414b727606a5e884edf)
- Corregir un segfault en errores de conexión diferidos. (*Revisado por David Christensen. Reportado por Anton Glushakov.*)

  Un error de conexión cuya notificación se retrasaba hasta una espera posterior podía provocar un fallo de segmentación.

  Incidencia [#2420](https://github.com/pgbackrest/pgbackrest/issues/2420); Solicitud de incorporación [#2422](https://github.com/pgbackrest/pgbackrest/pull/2422); Commit [`377ba06`](https://github.com/pgbackrest/pgbackrest/commit/377ba062ac81867dca6197265688deb0111ae81a)
- Omitir la comprobación de duplicados del repositorio local para SFTP. (*Corregido por Reid Thompson. Revisado por David Steele. Reportado por Anton Kurochkin.*)

  La comprobación de repositorios locales configurados más de una vez también se aplicaba a los repositorios SFTP, que nunca son locales.

  Incidencia [#2418](https://github.com/pgbackrest/pgbackrest/issues/2418); Solicitud de incorporación [#2421](https://github.com/pgbackrest/pgbackrest/pull/2421); Commit [`9840304`](https://github.com/pgbackrest/pgbackrest/commit/98403046ed6af4c54fa2f572ecf9c211f94b67db)

**Mejoras:**

- Soporte de PostgreSQL 17.

  PostgreSQL 17beta3 cambió los formatos de control y WAL, algo inusual en una beta.

  Commit [`189d15d`](https://github.com/pgbackrest/pgbackrest/commit/189d15d1a640e31aac5ffbbd0fb06eb9eed8b576)

### Notas de la versión v2.53 {#v253-release-notes}

*Copias de seguridad concurrentes*

*Publicada el 22 de julio de 2024*

**NOTA IMPORTANTE**: El valor predeterminado de `log-level-stderr` cambia de `warn` a `off`. Esto facilita capturar los errores cuando solo se redirige `stdout`. Para conservar el comportamiento anterior, establece `log-level-stderr=warn`.<br/> <br/> **NOTA PARA EMPAQUETADORES**: La compilación con meson ahora requiere la biblioteca lz4.<br/> <br/> **NOTA PARA EMPAQUETADORES**: La compilación con meson ahora requiere que el compilador admita `__builtin_clzl()` y `__builtin_bswap64()`.

**Correcciones de errores:**

- Corregir el fallo de renombrado SFTP cuando el archivo ya existe. (*Corregido por Reid Thompson. Revisado por David Steele. Reportado por ahmed112212.*)

  Algunos servidores SFTP notifican que un archivo ya existe mediante un error que no se manejaba, por lo que fallaba renombrar un archivo sobre otro existente.

  Incidencia [#2376](https://github.com/pgbackrest/pgbackrest/issues/2376); Solicitud de incorporación [#2377](https://github.com/pgbackrest/pgbackrest/pull/2377); Commit [`d6f0bf8`](https://github.com/pgbackrest/pgbackrest/commit/d6f0bf88af8b39492aa8e20c09bdf30260e2eb2f)

**Funcionalidades:**

- Permitir que las copias de seguridad se ejecuten concurrentemente en repositorios diferentes. (*Revisado por Reid Thompson, Stefan Fercot.*)

  Ahora se pueden realizar copias de una misma stanza al mismo tiempo en distintos repositorios, ya que los bloqueos se aplican por stanza y repositorio en lugar de solo por stanza. No es posible con PostgreSQL <= 9.5.

  [`270dce4`](https://github.com/pgbackrest/pgbackrest/commit/270dce41b6fff0d0ad0769b0ea5df0011140f0b9) Refactorizar el módulo de bloqueos.; Solicitud de incorporación [#2371](https://github.com/pgbackrest/pgbackrest/pull/2371)

  [`cfb8aa2`](https://github.com/pgbackrest/pgbackrest/commit/cfb8aa202ee972579697db2cc8d5d8ef111f0022) Añadir bloqueos remotos para los comandos de stanza omitidos en 31c7824a.

  [`edd6163`](https://github.com/pgbackrest/pgbackrest/commit/edd61636a98d193b7c0634b5a4444527132959e0) Permitir que las copias de seguridad se ejecuten concurrentemente en repositorios diferentes.; Solicitud de incorporación [#2389](https://github.com/pgbackrest/pgbackrest/pull/2389)
- Soportar SAN basados en IP para la validación de certificados TLS. (*Contribución de David Christensen. Revisado por David Steele.*)

  Ahora se validan los certificados con una dirección IP como nombre alternativo del sujeto, por ejemplo `IP:1.2.3.4`. Las direcciones IPv4 e IPv6 deben coincidir exactamente.

  Incidencia [#1977](https://github.com/pgbackrest/pgbackrest/issues/1977); Solicitud de incorporación [#2047](https://github.com/pgbackrest/pgbackrest/pull/2047); Commit [`dfb620b`](https://github.com/pgbackrest/pgbackrest/commit/dfb620b0b8cf884ca486b413f4cd162e258b2fc5)

**Mejoras:**

- Establecer por defecto la opción `log-level-stderr` en `off`. (*Revisado por Greg Sabino Mullane, Stefan Fercot.*)

  Las advertencias y errores escritos en stderr a menudo se perdían al redirigir solo stdout para recoger registros. Un `log-level-stderr` establecido explícitamente no se ve afectado.

  Solicitud de incorporación [#2379](https://github.com/pgbackrest/pgbackrest/pull/2379); Commit [`7d54073`](https://github.com/pgbackrest/pgbackrest/commit/7d540730941994d3cb630c695e9f672e047d8e7f)
- Permitir tamaños de segmento WAL alternativos para PostgreSQL ≤ 10. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)

  PostgreSQL <= 10 puede compilarse con otro tamaño de segmento WAL, y derivados como Greenplum lo establecen mediante `initdb`.

  Solicitud de incorporación [#2303](https://github.com/pgbackrest/pgbackrest/pull/2303); Commit [`4ac3b82`](https://github.com/pgbackrest/pgbackrest/commit/4ac3b82c99ff3bd48d2cc74651a47ce072ac0022)
- Añadir una sugerencia para revisar el registro de autorización de SFTP. (*Contribución de Vitalii Zurian. Revisado por Reid Thompson, David Steele.*)

  Cuando falla la autenticación SFTP, el error ahora indica que el registro de autorización del servidor puede contener más detalles.

  Incidencia [#2381](https://github.com/pgbackrest/pgbackrest/issues/2381); Solicitud de incorporación [#2385](https://github.com/pgbackrest/pgbackrest/pull/2385); Commit [`ccae609`](https://github.com/pgbackrest/pgbackrest/commit/ccae60940241b30e8bc3e405936b6ba68857930c)
- Mostrar los valores predeterminados y permitidos de las opciones de tiempo con unidades adecuadas.

  Los valores predeterminados y permitidos de tiempo se mostraban en segundos, lo que dificultaba leer valores grandes. Ya no se permiten segundos fraccionarios, por lo que un valor como `archive-timeout=0.5` debe escribirse como `archive-timeout=500ms`.

  Commit [`3a2266f`](https://github.com/pgbackrest/pgbackrest/commit/3a2266f327c340ff1133a6a2398429c844b5755d)
- Exigir OpenSSL >= 1.1.1.

  Commit [`cf8625d`](https://github.com/pgbackrest/pgbackrest/commit/cf8625d24bd953ad1ed448c32b937584009e5b6b)

**Mejoras en la documentación:**

- Aclarar el comportamiento multi-repositorio de `archive-push`. (*Revisado por Stefan Fercot.*)

  Si un repositorio falla, `archive-push` no puede avanzar con los demás a menos que esté activado `archive-async`.

  Solicitud de incorporación [#2398](https://github.com/pgbackrest/pgbackrest/pull/2398); Commit [`ec3e387`](https://github.com/pgbackrest/pgbackrest/commit/ec3e387bb73826c30b32bf0221acb2d56f23f1c5)

### Notas de la versión v2.52.1 {#v2521-release-notes}

*Corrección de error*

*Publicada el 25 de junio de 2024*

**Correcciones de errores:**

- Corregir un problema con archivos más grandes en la réplica que en el primario. (*Revisado por Stefan Fercot. Reportado por Nicolas Lassimonne.*)

  Con incrementales por bloques, si el tamaño de un archivo difería entre el primario y el servidor en espera durante una copia desde este último, la siguiente copia diferencial o incremental guardaba el tamaño del primario. La copia posterior fallaba con "repo size must be > 0".

  [`83aaa86`](https://github.com/pgbackrest/pgbackrest/commit/83aaa868ef396348bf96589457f13c1805b25cb6) Añadir pruebas unitarias de copias desde un servidor en espera con incrementales por bloques.

  [`aabc122`](https://github.com/pgbackrest/pgbackrest/commit/aabc122021a582e9d0193f978cf710cff95c2bee) Corregir un problema con archivos más grandes en la réplica que en el primario.; Incidencia [#2358](https://github.com/pgbackrest/pgbackrest/issues/2358); Solicitud de incorporación [#2367](https://github.com/pgbackrest/pgbackrest/pull/2367)

### Notas de la versión v2.52 {#v252-release-notes}

*Soporte de PostgreSQL 17beta1*

*Publicada el 27 de mayo de 2024*

**NOTA PARA EMPAQUETADORES**: El sistema de compilación de pgBackRest ahora es meson. La compilación con autoconf/make no recibirá nuevas funcionalidades y se eliminará después de algunas versiones.

**Funcionalidades:**

- Añadir soporte de eliminación por lotes de GCS. (*Revisado por Reid Thompson.*)

  Los archivos se eliminan mediante solicitudes por lotes en lugar de una por archivo, lo que acelera `expire` y otros comandos que eliminan archivos del repositorio.

  Solicitud de incorporación [#2326](https://github.com/pgbackrest/pgbackrest/pull/2326); Commit [`76bcb74`](https://github.com/pgbackrest/pgbackrest/commit/76bcb740b66f64804dbbf5a2a6be6407f9cec376)
- Soporte de cifrado `SSE-C` de S3. (*Revisado por Tim Jones. Sugerido por Tim Jones.*)

  Establece `repo-s3-sse-customer-key` para que S3 cifre los datos con la clave proporcionada después de transferirlos. No es tan seguro como cifrarlos antes de transmitirlos mediante `repo-cipher-type`.

  Incidencia [#2279](https://github.com/pgbackrest/pgbackrest/issues/2279); Solicitud de incorporación [#2282](https://github.com/pgbackrest/pgbackrest/pull/2282); Commit [`57731b6`](https://github.com/pgbackrest/pgbackrest/commit/57731b6cd261c732041aacc094429ab02ca13418)
- Soporte de PostgreSQL 17beta1. (*Revisado por Stefan Fercot.*)

  Se añaden la versión de catálogo y el número mágico WAL de PostgreSQL 17.

  Solicitud de incorporación [#2328](https://github.com/pgbackrest/pgbackrest/pull/2328); Commit [`fb22f04`](https://github.com/pgbackrest/pgbackrest/commit/fb22f04555fecfa143354372ec3543ab186c131d)

**Mejoras:**

- Permitir la deshabilitación explícita de dependencias opcionales en las compilaciones con meson. (*Contribución de Michael Schout. Revisado por David Steele.*)

  En la compilación con meson se puede desactivar una función opcional aunque su biblioteca esté instalada, como requieren algunas plataformas, por ejemplo FreeBSD. Por defecto, se activa si se encuentra su biblioteca.

  Solicitud de incorporación [#2321](https://github.com/pgbackrest/pgbackrest/pull/2321); Commit [`7b95fd3`](https://github.com/pgbackrest/pgbackrest/commit/7b95fd3bd29346e7325aa161bfee45efd71e22eb)
- Buscar dinámicamente python en la compilación con meson. (*Contribución de Michael Schout. Revisado por David Steele.*)

  La compilación con meson ahora localiza Python en lugar de exigir un ejecutable `python3` en la ruta, por ejemplo cuando solo está instalado `python3.9`. La versión mínima de meson pasa a ser 0.47.

  [`55e9969`](https://github.com/pgbackrest/pgbackrest/commit/55e996912aa57d39ea21f5dc905b7acabe93b0f8) Actualizar la versión mínima de meson a 0.47.

  [`e00e33b`](https://github.com/pgbackrest/pgbackrest/commit/e00e33b52856a63e82552ccc12df235d1a7f6f17) Buscar dinámicamente python en la compilación con meson.; Solicitud de incorporación [#2338](https://github.com/pgbackrest/pgbackrest/pull/2338)
- Marcar el objetivo de compilación `pgbackrest` en meson como instalable. (*Contribución de Bradford Boyle. Revisado por David Steele.*)

  Solicitud de incorporación [#2312](https://github.com/pgbackrest/pgbackrest/pull/2312); Commit [`7877983`](https://github.com/pgbackrest/pgbackrest/commit/7877983acb3b1a27e900f7e7aea89cb7b29a817d)

**Mejoras en la documentación:**

- Actualizar la documentación de `start`/`stop` para reflejar la funcionalidad real. (*Revisado por Stefan Fercot.*)

  Incidencia [#2325](https://github.com/pgbackrest/pgbackrest/issues/2325); Incidencia [#2334](https://github.com/pgbackrest/pgbackrest/issues/2334); Solicitud de incorporación [#2352](https://github.com/pgbackrest/pgbackrest/pull/2352); Commit [`b6ac11b`](https://github.com/pgbackrest/pgbackrest/commit/b6ac11beec920fe978994c0d018c380477199ca8)

### Notas de la versión v2.51 {#v251-release-notes}

*Sistema de compilación Meson*

*Publicada el 25 de marzo de 2024*

**Correcciones de errores:**

- Omitir archivos de longitud cero para la restauración delta incremental por bloques. (*Revisado por Sebastian Krause, René Højbjerg Larsen. Reportado por Sebastian Krause.*)

  Un archivo existente de longitud cero hacía fallar una restauración delta incremental por bloques en el filtro de sumas de bloques. Ahora se omiten estos archivos, ya que no tienen contenido reutilizable.

  Incidencia [#2271](https://github.com/pgbackrest/pgbackrest/issues/2271); Solicitud de incorporación [#2272](https://github.com/pgbackrest/pgbackrest/pull/2272); Commit [`f7a7ab1`](https://github.com/pgbackrest/pgbackrest/commit/f7a7ab16c9652179945717ebf9b68af3aa8a0b0e)
- Corregir una regresión de rendimiento en el listado de almacenamiento. (*Revisado por Stephen Frost. Reportado por Maksym Boguk.*)

  Listar una ruta solicitaba información detallada de cada archivo, lo que podía ser lento, por ejemplo en almacenes de objetos. Ahora solo se pide la información necesaria para el listado.

  Incidencia [#2275](https://github.com/pgbackrest/pgbackrest/issues/2275); Solicitud de incorporación [#2276](https://github.com/pgbackrest/pgbackrest/pull/2276); Commit [`e00bfe2`](https://github.com/pgbackrest/pgbackrest/commit/e00bfe2d2c3f124b2883e3c2d169a2ce506a1e98)
- Corregir el registro de progreso cuando el tamaño del archivo cambia durante la copia de seguridad. (*Revisado por Stephen Frost. Reportado por samkingno.*)

  Incidencia [#2298](https://github.com/pgbackrest/pgbackrest/issues/2298); Solicitud de incorporación [#2304](https://github.com/pgbackrest/pgbackrest/pull/2304); Commit [`76956e7`](https://github.com/pgbackrest/pgbackrest/commit/76956e71cfa3044867213bd65a6f22e96120c108)

**Mejoras:**

- Soporte mejorado para conexiones dual stack. (*Revisado por Stephen Frost. Sugerido por Timothée Peignier.*)

  Cuando un nombre de host resuelve a varias direcciones, como IPv4 e IPv6, se prueba la siguiente una vez que la anterior ha tenido un tiempo razonable para conectar, siguiendo el enfoque «happy eyeballs» de RFC 8305. Un intento que ni falla ni conecta ya no consume todo el tiempo disponible.

  Incidencia [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Solicitud de incorporación [#2235](https://github.com/pgbackrest/pgbackrest/pull/2235); Commit [`7448fde`](https://github.com/pgbackrest/pgbackrest/commit/7448fde157c6d22f57b90c0cef11957b0aadf4b3)
- Hacer de meson el sistema de compilación principal. (*Revisado por Stephen Frost.*)

  Ahora se usa meson para las pruebas y para compilar la documentación. Las funciones que no se usan fuera de su módulo pasan a estar ocultas, lo que reduce el tamaño del binario.

  [`e3d9df3`](https://github.com/pgbackrest/pgbackrest/commit/e3d9df3ae9669ee5749b970d59f8afeb20fd3d9d) Hacer de meson el sistema de compilación principal.; Solicitud de incorporación [#2264](https://github.com/pgbackrest/pgbackrest/pull/2264)

  [`f287178`](https://github.com/pgbackrest/pgbackrest/commit/f287178b705cc90aa887d66c932e2a223029649b) Establecer la visibilidad de funciones y variables como hidden.; Solicitud de incorporación [#2265](https://github.com/pgbackrest/pgbackrest/pull/2265)
- Detectar archivos que no han cambiado durante una copia de seguridad incremental no delta. (*Revisado por Stephen Frost.*)

  Durante una copia diferencial o incremental sin delta, un archivo que cabe en un búfer, o cualquier archivo incremental por bloques, se compara con el de la copia anterior y, si no ha cambiado, se referencia en lugar de almacenarse.

  Solicitud de incorporación [#2257](https://github.com/pgbackrest/pgbackrest/pull/2257); Commit [`9d91d1b`](https://github.com/pgbackrest/pgbackrest/commit/9d91d1b2f817b543fc8d970af56d1442c325ed7c)
- Evitar una recuperación inválida cuando se elimina `backup_label`. (*Revisado por Stephen Frost.*)

  Si se elimina `backup_label` de un clúster restaurado, PostgreSQL usa el punto de control de `pg_control` para la recuperación tras un fallo, lo que casi siempre corrompe el clúster. Ahora la restauración invalida el punto de control de `pg_control` para que la recuperación falle en su lugar. `pg_controldata` lo muestra como `0/DEAD`.

  Solicitud de incorporación [#2232](https://github.com/pgbackrest/pgbackrest/pull/2232); Commit [`e634fd8`](https://github.com/pgbackrest/pgbackrest/commit/e634fd85cedc1ae3aef7c4fa2556d7d73d05cb8a)
- Mejorar el manejo de la cola de segmentos WAL de `archive-push`. (*Revisado por Stephen Frost.*)

  Antes se leía el tamaño de cada segmento WAL para medir la cola. Ahora se usa el tamaño del primer segmento para todos.

  Solicitud de incorporación [#2277](https://github.com/pgbackrest/pgbackrest/pull/2277); Commit [`cf17515`](https://github.com/pgbackrest/pgbackrest/commit/cf17515e409440eecfb04bf7186790d8baa8ab12)
- Limitar la funcionalidad de reanudación a las copias de seguridad completas. (*Revisado por Stephen Frost, Stefan Fercot.*)

  La reanudación no funcionaba correctamente para copias diferenciales e incrementales delta y es probable que un archivo modificado desde la copia anterior vuelva a cambiar antes de reanudar. Ahora solo se reanudan las copias completas.

  Solicitud de incorporación [#2268](https://github.com/pgbackrest/pgbackrest/pull/2268); Commit [`dddcbcd`](https://github.com/pgbackrest/pgbackrest/commit/dddcbcd8e9a1cae578b0cc5bb2d1aa768330f3c5)
- Actualizar la funcionalidad de reanudación para el incremental por bloques. (*Revisado por Stephen Frost.*)

  La reanudación eliminaba los archivos incrementales por bloques, por lo que funcionaba pero volvía a copiarlos todos. Ahora se conservan al reanudar.

  Solicitud de incorporación [#2296](https://github.com/pgbackrest/pgbackrest/pull/2296); Commit [`ff47450`](https://github.com/pgbackrest/pgbackrest/commit/ff47450402fde5ebc64a08d31791551bee52200e)
- Permitir `--version` y `--help` para versión y ayuda. (*Revisado por Greg Sabino Mullane. Sugerido por Greg Sabino Mullane.*)

  `--version` y `--help` ahora funcionan como en la mayoría de programas. Utiliza `help` para consultar un comando u opción concretos.

  Solicitud de incorporación [#2263](https://github.com/pgbackrest/pgbackrest/pull/2263); Commit [`68db307`](https://github.com/pgbackrest/pgbackrest/commit/68db3075d7ac4a48377967ad54e45b95b9ee6c61)
- Añadir un backtrace detallado a la compilación con autoconf/make. (*Revisado por Stephen Frost.*)

  Las trazas de errores de la compilación autoconf/make ahora incluyen detalles de libbacktrace, que según las pruebas de rendimiento no tienen un coste apreciable.

  Solicitud de incorporación [#1970](https://github.com/pgbackrest/pgbackrest/pull/1970); Commit [`676700d`](https://github.com/pgbackrest/pgbackrest/commit/676700d8ca6f2e0e0ab8123aa9606c8ec7aa81ae)

**Mejoras en la documentación:**

- Actualizar las referencias a `recovery.conf`. (*Revisado por Stefan Fercot. Sugerido por Stephen Frost.*)

  Las referencias a `recovery.conf` ahora también incluyen `postgresql.auto.conf`, usado por las versiones recientes de PostgreSQL.

  Solicitud de incorporación [#2281](https://github.com/pgbackrest/pgbackrest/pull/2281); Commit [`6835178`](https://github.com/pgbackrest/pgbackrest/commit/68351785f6816a23526900db595557cf6e3a0056)

### Notas de la versión v2.50 {#v250-release-notes}

*Mejoras de rendimiento y correcciones de errores*

*Publicada el 22 de enero de 2024*

**Correcciones de errores:**

- Corregir una lectura corta en la restauración incremental por bloques. (*Revisado por Stephen Frost. Probado por Brent Graveland. Reportado por Adol Rodriguez, Brent Graveland.*)

  Un superbloque comprimido puede terminar con bytes innecesarios para descomprimirlo pero que marcan el final de los datos. Según cómo coincidiera el búfer con los datos, esos bytes no se leían y la restauración fallaba.

  Incidencia [#2215](https://github.com/pgbackrest/pgbackrest/issues/2215); Incidencia [#2238](https://github.com/pgbackrest/pgbackrest/issues/2238); Solicitud de incorporación [#2256](https://github.com/pgbackrest/pgbackrest/pull/2256); Commit [`f4a4af2`](https://github.com/pgbackrest/pgbackrest/commit/f4a4af299bee93ab7dde599ccdb35becc1c2afad)
- Corregir un desbordamiento que suprimía el progreso de la copia de seguridad en la salida de `info`. (*Corregido por Robert Donovan. Revisado por Joe Wildish.*)

  Los tamaños del archivo de bloqueo se leían como valores de 32 bits, por lo que `info` no informaba del progreso de copias mayores de 4GiB.

  Incidencia [#2251](https://github.com/pgbackrest/pgbackrest/issues/2251); Solicitud de incorporación [#2252](https://github.com/pgbackrest/pgbackrest/pull/2252); Commit [`25f1489`](https://github.com/pgbackrest/pgbackrest/commit/25f14898babf4ad78baef3e8343933a863633975)

**Mejoras:**

- Preservar archivos parciales durante la restauración delta incremental por bloques. (*Revisado por Stephen Frost.*)

  En una restauración delta incremental por bloques no se conservaba un archivo menor de lo esperado, aunque sus bloques fueran reutilizables, por ejemplo al reintentar una restauración fallida o restaurar sobre un archivo más pequeño.

  Solicitud de incorporación [#2254](https://github.com/pgbackrest/pgbackrest/pull/2254); Commit [`a42614e`](https://github.com/pgbackrest/pgbackrest/commit/a42614e8f3a9e6871c16331f01c2cd765ab181aa)
- Añadir soporte para tamaños de página alternativos en tiempo de compilación. (*Contribución de Viktor Kurilko. Revisado por David Steele.*)

  PostgreSQL puede compilarse con otro tamaño de página, por ejemplo 4096, y derivados como Greenplum lo hacen.

  Solicitud de incorporación [#2197](https://github.com/pgbackrest/pgbackrest/pull/2197); Commit [`89d5278`](https://github.com/pgbackrest/pgbackrest/commit/89d5278b74ab0d880345575d7ac4c239cd1fce54)
- Omitir archivos truncados durante la copia de seguridad al agrupar. (*Contribución de Georgy Shelkovy. Revisado por David Steele.*)

  Un archivo truncado a cero después de asignarlo a un grupo seguía almacenándose en él y fallaba una aserción en compilaciones de depuración. Ahora se omiten estos archivos.

  [`02eea55`](https://github.com/pgbackrest/pgbackrest/commit/02eea555c7169e99892fdbc8ce7cc1ee59f50509) Omitir archivos truncados durante la copia de seguridad al agrupar.; Solicitud de incorporación [#2227](https://github.com/pgbackrest/pgbackrest/pull/2227)

  [`c879509`](https://github.com/pgbackrest/pgbackrest/commit/c8795094d418802a0e24d4d19da66973c71b00e5) Permitir que backupFile() devuelva búferes de sumas de verificación const.

  [`9049fec`](https://github.com/pgbackrest/pgbackrest/commit/9049fec2c02c4110e16ffdff7b56f83d8ff32b4a) Refactorizar la omisión de archivos truncados durante la copia al agruparlos.

  Desarrollo en [v2.49](#v249-release-notes):

  [`337da35`](https://github.com/pgbackrest/pgbackrest/commit/337da35ab278e058ec4cdffeb4319f1a1e2cb0df) Añadir una prueba del comportamiento de archivos agrupados truncados durante la copia.
- Mejorar los mensajes de error del almacenamiento SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Solicitud de incorporación [#2249](https://github.com/pgbackrest/pgbackrest/pull/2249); Commit [`7c17eec`](https://github.com/pgbackrest/pgbackrest/commit/7c17eec3db455d3e8e660f4f8247b6975517648f)

### Notas de la versión v2.49 {#v249-release-notes}

*Eliminación del soporte de PostgreSQL 9.3*

*Publicada el 27 de noviembre de 2023*

**Correcciones de errores:**

- Corregir una regresión en los reintentos. (*Revisado por Stephen Frost. Reportado por Norman Adkins, Tanel Suurhans, Jordan English, Timothée Peignier.*)

  v2.48 eliminó el reintento cuando una operación agotaba todo su tiempo de espera, por lo que el agotamiento se convertía en error, por ejemplo al esperar que un socket de un almacén de objetos pudiera escribirse. Ahora se hacen dos reintentos incluso tras agotar el tiempo.

  [`3c116e1`](https://github.com/pgbackrest/pgbackrest/commit/3c116e1829a0df62aaf50ce241c63d829eb438e0) Eliminar un encabezado sin uso.

  [`fa5b2d4`](https://github.com/pgbackrest/pgbackrest/commit/fa5b2d44ad9f7591517eecaaaaeb07e9500dd51c) Corregir una regresión en los reintentos.; Incidencia [#2200](https://github.com/pgbackrest/pgbackrest/issues/2200); Incidencia [#2214](https://github.com/pgbackrest/pgbackrest/issues/2214); Solicitud de incorporación [#2221](https://github.com/pgbackrest/pgbackrest/pull/2221)
- Corregir la eliminación recursiva de rutas en el controlador de almacenamiento SFTP. (*Corregido por Reid Thompson. Revisado por Stephen Frost. Reportado por Luc.*)

  Algunos servidores SFTP devuelven permiso denegado en lugar de un fallo al desvincular un directorio como archivo, por lo que la eliminación recursiva de rutas fallaba en ellos.

  Incidencia [#2219](https://github.com/pgbackrest/pgbackrest/issues/2219); Solicitud de incorporación [#2226](https://github.com/pgbackrest/pgbackrest/pull/2226); Commit [`c4dc466`](https://github.com/pgbackrest/pgbackrest/commit/c4dc4665f88e9d67a3b66f44cd59d6dd4bb5107f)

**Mejoras:**

- Eliminar el soporte de PostgreSQL `9.3`. (*Revisado por Stephen Frost.*)

  PostgreSQL 9.3 deja de estar soportado conforme a la política de admitir cinco versiones de PostgreSQL que hayan llegado al final de su vida útil.

  Solicitud de incorporación [#2220](https://github.com/pgbackrest/pgbackrest/pull/2220); Commit [`dcf0781`](https://github.com/pgbackrest/pgbackrest/commit/dcf078198761a2cfe9be6b4c7f4b4fb07ef53cbf)

**Funcionalidades de la documentación:**

- Documentar las opciones del mantenedor. (*Revisado por Stefan Fercot.*)

  Las opciones para mantenedores ahora se documentan en su propia sección con las precauciones de uso, y `pg-version-force` deja de ser interna.

  Solicitud de incorporación [#2202](https://github.com/pgbackrest/pgbackrest/pull/2202); Commit [`21c8c8a`](https://github.com/pgbackrest/pgbackrest/commit/21c8c8a66cb06eba714bfa41bed7239af3d14f08)
- Actualizar la documentación de recuperación en un punto en el tiempo para PostgreSQL >= 13.

  Desde PostgreSQL 13, la recuperación da error si no se alcanza el objetivo. La sección de recuperación a un punto en el tiempo ahora funciona tanto con PostgreSQL 13 y posteriores como con versiones anteriores.

  Commit [`eb69e2e`](https://github.com/pgbackrest/pgbackrest/commit/eb69e2ee6339047f0145b751437ac2bec82bb5ab)

**Mejoras en la suite de pruebas:**

- Permitir que la prueba unitaria `config/load` se ejecute sin `libssh2` instalado. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Wu Ning.*)

  Incidencia [#2193](https://github.com/pgbackrest/pgbackrest/issues/2193); Solicitud de incorporación [#2194](https://github.com/pgbackrest/pgbackrest/pull/2194); Commit [`e2b734e`](https://github.com/pgbackrest/pgbackrest/commit/e2b734eff97e3fac32895b799cc32126013aae27)

### Notas de la versión v2.48 {#v248-release-notes}

*Etiquetas de almacenamiento del repositorio*

*Publicada el 25 de septiembre de 2023*

**Correcciones de errores:**

- Corregir un problema al restaurar incremental por bloques sin una lista de bloques. (*Revisado por Stephen Frost. Probado por Burak Yurdakul. Reportado por Burak Yurdakul.*)

  Un mapa sin bloques, escrito cuando cambia la marca de tiempo de un archivo pero no su contenido, no se descifraba si seguía a un archivo guardado sin incrementales por bloques en la misma lectura de grupo. Con suficientes archivos afectados se agotaban los reintentos y fallaba la restauración.

  Incidencia [#2182](https://github.com/pgbackrest/pgbackrest/issues/2182); Solicitud de incorporación [#2184](https://github.com/pgbackrest/pgbackrest/pull/2184); Commit [`31de127`](https://github.com/pgbackrest/pgbackrest/commit/31de127cf42438b1fac04c161c47264aa1fb1060)

**Funcionalidades:**

- Añadir la opción `--repo-storage-tag` para crear etiquetas de objetos. (*Revisado por Stephen Frost, Stefan Fercot, Timothée Peignier.*)

  Establece `repo-storage-tag` para añadir etiquetas a los objetos escritos en un repositorio S3, GCS o Azure. Las etiquetas se configuran por repositorio.

  Incidencia [#2150](https://github.com/pgbackrest/pgbackrest/issues/2150); Solicitud de incorporación [#2159](https://github.com/pgbackrest/pgbackrest/pull/2159); Commit [`1b4e0cc`](https://github.com/pgbackrest/pgbackrest/commit/1b4e0cce5f3ff5ea3ee0b889e6d4ce4de1430b04)
- Añadir comprobación de known hosts para el controlador de almacenamiento SFTP. (*Contribución de Reid Thompson. Revisado por Stephen Frost, David Steele.*)

  Ahora las claves de host SFTP se comprueban por defecto contra los archivos de hosts conocidos, es decir, `repo-sftp-host-key-check-type=strict`. Establece `repo-sftp-host-key-check-type=accept-new` para añadir hosts nuevos automáticamente o `repo-sftp-host-key-check-type=none` para omitir la comprobación como antes.

  Solicitud de incorporación [#2125](https://github.com/pgbackrest/pgbackrest/pull/2125); Commit [`ce9ba0f`](https://github.com/pgbackrest/pgbackrest/commit/ce9ba0fadee652d409488bee701ea6a51cafec75)
- Soporte para conexiones dual stack. (*Revisado por Stephen Frost.*)

  Ahora se prueba sucesivamente cada dirección a la que resuelve un host, por ejemplo una IPv6 sin ruta al host seguida de una IPv4, hasta conectar o agotar el tiempo. Los errores de reintento repetidos también se resumen en los mensajes.

  [`5314dbf`](https://github.com/pgbackrest/pgbackrest/commit/5314dbffc761bc7507db02693f2421c1578efe10) Ajustar el objeto Wait para mejorar su precisión cuando está anidado.

  [`c180513`](https://github.com/pgbackrest/pgbackrest/commit/c1805134b370f0c5c54c40a2df8978599328784f) Agrupar los errores de reintentos en la salida de ErrorRetry.

  [`edbd520`](https://github.com/pgbackrest/pgbackrest/commit/edbd520c81f5d437963aaf42d1c79b2c51d01665) Refactorizar la búsqueda de la lista de direcciones para incluir todas las devueltas.; Solicitud de incorporación [#2174](https://github.com/pgbackrest/pgbackrest/pull/2174)

  [`39bb8a0`](https://github.com/pgbackrest/pgbackrest/commit/39bb8a0d3a96eef63219dff262a9306a4f59dae9) Soporte para conexiones dual stack.; Incidencia [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); Solicitud de incorporación [#2175](https://github.com/pgbackrest/pgbackrest/pull/2175)
- Añadir el tamaño completado/total de la copia de seguridad a la salida JSON del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  La salida JSON de `info` ahora incluye el tamaño completado y total de una copia en curso, permitiendo supervisar su progreso desde otros programas.

  Incidencia [#2007](https://github.com/pgbackrest/pgbackrest/issues/2007); Solicitud de incorporación [#2141](https://github.com/pgbackrest/pgbackrest/pull/2141); Commit [`e3fcd8c`](https://github.com/pgbackrest/pgbackrest/commit/e3fcd8cd9e0be42a32fc4cbd2ae3db2c072eabcd)

**Mejoras:**

- Comando check multi-stanza. (*Revisado por Stephen Frost.*)

  Si no se indica `stanza`, `check` ahora comprueba todas las stanzas de la configuración.

  Solicitud de incorporación [#2057](https://github.com/pgbackrest/pgbackrest/pull/2057); Commit [`1141dc2`](https://github.com/pgbackrest/pgbackrest/commit/1141dc20708cf0c68296f83e74c872a7db9c2bd9)
- Reintentar lecturas de `pg_control` hasta que la suma de verificación sea válida. (*Revisado por Stefan Fercot, Stephen Frost.*)

  En algunos sistemas de archivos, como ext4, leer `pg_control` durante una escritura simultánea puede devolver datos parcialmente escritos. Ahora se reintenta la lectura hasta que la suma de verificación sea válida.

  Solicitud de incorporación [#2131](https://github.com/pgbackrest/pgbackrest/pull/2131); Commit [`f42d927`](https://github.com/pgbackrest/pgbackrest/commit/f42d927d2dcd58cf5a80d68eaf6888bcf2c67a4b)
- Optimizar la comprobación del segmento WAL después de una copia de seguridad exitosa. (*Revisado por Stephen Frost.*)

  La comprobación de segmentos WAL tras una copia listaba el almacenamiento una vez por segmento. Ahora cada directorio WAL se lista una sola vez y se reutiliza la lista.

  Solicitud de incorporación [#2169](https://github.com/pgbackrest/pgbackrest/pull/2169); Commit [`9d3a605`](https://github.com/pgbackrest/pgbackrest/commit/9d3a605900644059ff0e030d71a818b3965eb031)
- Mejorar el rendimiento multiparte de GCS. (*Revisado por Reid Thompson.*)

  Ahora los fragmentos de una carga multiparte se suben en cuanto están disponibles.

  Solicitud de incorporación [#2162](https://github.com/pgbackrest/pgbackrest/pull/2162); Commit [`6cb9c40`](https://github.com/pgbackrest/pgbackrest/commit/6cb9c40fb8ea18e6572bf3f6e44bbb1d8f922682)
- Permitir que el comando `archive-get` se ejecute cuando la stanza está detenida. (*Revisado por Tom Swartz, David Christensen, Reid Thompson.*)

  Como `archive-get` no escribe en el repositorio, ahora puede ejecutarse mientras la stanza está detenida, al igual que `restore`.

  Commit [`fbd992a`](https://github.com/pgbackrest/pgbackrest/commit/fbd992adc7b18db5e70774d675c160c8c8e2f031)
- Aceptar la virgulilla inicial en las rutas de las claves públicas/privadas SFTP. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Las rutas de `repo-sftp-private-key-file` y `repo-sftp-public-key-file` ahora pueden comenzar por `~`, tal como se documenta.

  Solicitud de incorporación [#2136](https://github.com/pgbackrest/pgbackrest/pull/2136); Commit [`eb32d6d`](https://github.com/pgbackrest/pgbackrest/commit/eb32d6de5e1575a37efb166abbf7df400d93352e)
- Recargar las credenciales de GCS antes de renovar el token de autenticación. (*Revisado por Stephen Frost. Sugerido por Daniel Farina.*)

  Ahora se vuelve a leer el archivo de clave de servicio antes de renovar el token, permitiendo sustituir la clave mientras se ejecuta un comando.

  Solicitud de incorporación [#2072](https://github.com/pgbackrest/pgbackrest/pull/2072); Commit [`995a8e9`](https://github.com/pgbackrest/pgbackrest/commit/995a8e96691d23eaf3914a425669f89deb3ce002)

**Correcciones de errores en la documentación:**

- Corregir el ejemplo de la referencia de configuración para la opción `tls-server-address`. (*Corregido por Hartmut Goebel. Revisado por David Steele.*)

  El ejemplo `::*` no era válido. Usa `*` para IPv4 o `::` para IPv6.

  Solicitud de incorporación [#2165](https://github.com/pgbackrest/pgbackrest/pull/2165); Commit [`43524a4`](https://github.com/pgbackrest/pgbackrest/commit/43524a47a4c6a847f76514812f94b87cb7af4c05)
- Corregir el ejemplo de la referencia de comandos para la opción `filter`.

  Commit [`cb3ff6e`](https://github.com/pgbackrest/pgbackrest/commit/cb3ff6ed4336af9e4c0643d8224d5bc3d790a655)

**Mejoras en la suite de pruebas:**

- Permitir que la prueba unitaria `storage/sftp` se ejecute sin `libssh2` instalado. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Wu Ning.*)

  Incidencia [#2163](https://github.com/pgbackrest/pgbackrest/issues/2163); Solicitud de incorporación [#2177](https://github.com/pgbackrest/pgbackrest/pull/2177); Commit [`c3c0834`](https://github.com/pgbackrest/pgbackrest/commit/c3c0834e170196a1241a368779162fcca65f9ad5)

### Notas de la versión v2.47 {#v247-release-notes}

*Mejoras de rendimiento y correcciones de errores*

*Publicada el 24 de julio de 2023*

**Correcciones de errores:**

- Preservar la información del incremental por bloques en el manifiesto durante una copia de seguridad delta. (*Revisado por Stephen Frost. Reportado por Francisco Miguel Biete Banon.*)

  Si un archivo cambiaba de modo que no usaría incrementales por bloques de ser nuevo, por ejemplo al reducirse por debajo del límite o retroceder mucho su marca de tiempo, perdía la información incremental por bloques del manifiesto de una copia delta, aunque todavía pudiera referenciarse a la copia anterior.

  [`1d42aed`](https://github.com/pgbackrest/pgbackrest/commit/1d42aed152563fff6ec70c517d86eb39158b3f20) Mejorar la validación de archivos referenciados en la prueba unitaria command/backup.

  [`4c27d74`](https://github.com/pgbackrest/pgbackrest/commit/4c27d74bbd3a44d8ab1af140277d3cd8302060c2) Preservar la información del incremental por bloques en el manifiesto durante una copia de seguridad delta.; Incidencia [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Solicitud de incorporación [#2123](https://github.com/pgbackrest/pgbackrest/pull/2123)
- Corregir los nombres de archivo del incremental por bloques en el comando `verify`. (*Revisado por Reid Thompson. Reportado por Francisco Miguel Biete Banon.*)

  `verify` utilizaba la extensión de compresión en lugar de `.pgbi` para archivos incrementales por bloques fuera de un grupo, por lo que no podía encontrarlos.

  Incidencia [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); Solicitud de incorporación [#2120](https://github.com/pgbackrest/pgbackrest/pull/2120); Commit [`cdb7e26`](https://github.com/pgbackrest/pgbackrest/commit/cdb7e26350822b55c00771d6d575242b1202e741)
- Corregir una copia de seguridad delta automática espuria en una copia desde réplica. (*Revisado por Stephen Frost. Reportado por krmozejko, Don Seiler.*)

  Los tamaños de archivo pueden diferir entre el servidor en espera y el primario, por ejemplo en los mapas de espacio libre. La siguiente copia incremental podía detectar un cambio de tamaño en el primario y pasar a un delta por suma de verificación, mucho más lento. Ahora se conserva el tamaño original en el manifiesto y se usa para comparar.

  Incidencia [#2020](https://github.com/pgbackrest/pgbackrest/issues/2020); Solicitud de incorporación [#2124](https://github.com/pgbackrest/pgbackrest/pull/2124); Commit [`5ed6f8d`](https://github.com/pgbackrest/pgbackrest/commit/5ed6f8df1487174985c42d6e13c367d70c2d8b8a)
- Omitir `recovery.signal` para PostgreSQL >= 12 cuando la recuperación es `type=none`. (*Revisado por Stefan Fercot. Reportado por T.Anastacio.*)

  Con `type=none`, ya no se escribe `recovery.signal` para PostgreSQL >= 12, igualando el comportamiento de versiones anteriores.

  Incidencia [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Solicitud de incorporación [#2070](https://github.com/pgbackrest/pgbackrest/pull/2070); Commit [`9cceed6`](https://github.com/pgbackrest/pgbackrest/commit/9cceed6ac4a32c14a797eba89a4ad1dc06d89d80)
- Corregir la generación de etiquetas únicas para copias de seguridad diff/incr. (*Corregido por Andrey Sokolov. Revisado por David Steele.*)

  Con al menos dos copias completas y la más reciente caducada, una copia diferencial o incremental fallaba como si el reloj hubiera retrocedido, porque su etiqueta se comparaba con la de la copia completa caducada.

  Incidencia [#1873](https://github.com/pgbackrest/pgbackrest/issues/1873); Solicitud de incorporación [#2104](https://github.com/pgbackrest/pgbackrest/pull/2104); Commit [`0ac0934`](https://github.com/pgbackrest/pgbackrest/commit/0ac09344dc17fb54e250705ce49399b86329bb3d)
- Corregir la expiración de archivado basada en tiempo cuando no expira ninguna copia de seguridad. (*Revisado por Stefan Fercot.*)

  Si se cumplía la retención temporal pero no caducaba ninguna copia, tampoco caducaba el archivo WAL y se registraba "time-based archive retention not met". Hacía falta una copia más para caducar el WAL anterior.

  Incidencia [#2103](https://github.com/pgbackrest/pgbackrest/issues/2103); Solicitud de incorporación [#2109](https://github.com/pgbackrest/pgbackrest/pull/2109); Commit [`762498f`](https://github.com/pgbackrest/pgbackrest/commit/762498f4cd5f1425db4c176fc707926d62cc7c04)

**Mejoras:**

- Mejorar el rendimiento del controlador de almacenamiento SFTP. (*Contribución de Stephen Frost, Reid Thompson. Revisado por David Steele.*)

  El controlador SFTP esperaba un tiempo fijo cuando libssh2 no podía continuar. Ahora espera hasta que el socket se pueda leer o escribir.

  [`e280ed9`](https://github.com/pgbackrest/pgbackrest/commit/e280ed9098a6f5da9bdabb541e9c69d4f24ffcf2) Hacer más coherente el manejo de códigos de resultado en storage/sftp.

  [`125676a`](https://github.com/pgbackrest/pgbackrest/commit/125676ae0e98d3730d2dc0d47e37ca1df145d044) Limpiar la inicialización y el handshake de storageSftpNew().

  [`28b6b2d`](https://github.com/pgbackrest/pgbackrest/commit/28b6b2d4659d78ce67c1bd3104d96e5705d955c9) Mejorar el rendimiento del controlador de almacenamiento SFTP.; Solicitud de incorporación [#2089](https://github.com/pgbackrest/pgbackrest/pull/2089)
- Añadir el desplazamiento de zona horaria a la salida de fecha/hora del comando `info`. (*Revisado por Stefan Fercot, Philip Hurst. Sugerido por Philip Hurst.*)

  Las marcas de tiempo de `info` ahora incluyen el desplazamiento de zona horaria, por lo que se pueden usar directamente como objetivo de recuperación, por ejemplo con `--target`.

  [`9efd5cd`](https://github.com/pgbackrest/pgbackrest/commit/9efd5cd0bb40c5dc2fcac2e21c9b62e554b94db6) Añadir el desplazamiento de zona horaria a la salida de fecha/hora del comando `info`.; Incidencia [#2093](https://github.com/pgbackrest/pgbackrest/issues/2093); Solicitud de incorporación [#2095](https://github.com/pgbackrest/pgbackrest/pull/2095)

  [`aa229a1`](https://github.com/pgbackrest/pgbackrest/commit/aa229a1deef3afeebb66db1443b19e24559adf96) Modificar las conversiones de time_t según las observaciones de Coverity.
- Centralizar el manejo de errores para funcionalidades no soportadas. (*Revisado por Stefan Fercot.*)

  Los errores de funciones no compiladas, como lz4, ahora son más detallados y coherentes. Indicar almacenamiento SFTP sin haberlo compilado ya no provoca un fallo de aserción.

  [`de46276`](https://github.com/pgbackrest/pgbackrest/commit/de46276bf60b8a2181621b123d1a99e56808a089) Refactorizar el procesamiento de listas de permitidos en config/parse.

  [`36ff81d`](https://github.com/pgbackrest/pgbackrest/commit/36ff81dc6ff7e98e40c0c05a4a343a71b91b1678) Centralizar el manejo de errores para funcionalidades no soportadas.; Solicitud de incorporación [#2075](https://github.com/pgbackrest/pgbackrest/pull/2075)

**Mejoras en la documentación:**

- Aclarar la preferencia por instalar desde paquetes en la guía de usuario. (*Revisado por Stefan Fercot. Sugerido por dr-kd.*)

  Solicitud de incorporación [#2090](https://github.com/pgbackrest/pgbackrest/pull/2090); Commit [`a36f480`](https://github.com/pgbackrest/pgbackrest/commit/a36f480c85c7add6fdf0e5517748d740e3a7b424)

### Notas de la versión v2.46 {#v246-release-notes}

*Copia de seguridad incremental por bloques y almacenamiento SFTP*

*Publicada el 22 de mayo de 2023*

**Funcionalidades:**

- Copia de seguridad incremental por bloques. (*Revisado por John Morris, Stephen Frost, Stefan Fercot.*)

  Los incrementales por bloques solo almacenan las partes del archivo que cambiaron desde la copia anterior, ahorrando espacio y tiempo en copias diferenciales e incrementales de archivos grandes. Se activan con `repo-block`, que requiere `repo-bundle`.

  [`dd4e526`](https://github.com/pgbackrest/pgbackrest/commit/dd4e52679ecdc43539bd038b5aa9bd4ff9055cbf) Eliminar la división en fragmentos y los números de bloque de la lista incremental de bloques.; Solicitud de incorporación [#2029](https://github.com/pgbackrest/pgbackrest/pull/2029)

  [`822f2a5`](https://github.com/pgbackrest/pgbackrest/commit/822f2a584260a012b833455a7a2bd1c8487e3010) Finalizar la función de incrementales por bloques.; Solicitud de incorporación [#2053](https://github.com/pgbackrest/pgbackrest/pull/2053)
- Soporte de SFTP para el almacenamiento del repositorio. (*Contribución de Reid Thompson. Revisado por Stephen Frost, David Steele.*)

  Establece `repo-type=sftp` y `repo-sftp-host` para almacenar el repositorio en un servidor SFTP.

  Solicitud de incorporación [#1959](https://github.com/pgbackrest/pgbackrest/pull/1959); Commit [`87087fa`](https://github.com/pgbackrest/pgbackrest/commit/87087fac231d2110160b3219daee3f9fb91aec02)

  Desarrollo en [v2.42](#v242-release-notes):

  [`01b81f9`](https://github.com/pgbackrest/pgbackrest/commit/01b81f9d374701eb489dd1888bcba25fb5d6df84) Mover la creación de enlaces a la interfaz de almacenamiento.; Solicitud de incorporación [#1879](https://github.com/pgbackrest/pgbackrest/pull/1879)
- Soporte de PostgreSQL 16. (*Revisado por Stefan Fercot.*)

  Se añaden la versión de catálogo y el número mágico WAL de PostgreSQL 16.

  Solicitud de incorporación [#2051](https://github.com/pgbackrest/pgbackrest/pull/2051); Commit [`3fc3690`](https://github.com/pgbackrest/pgbackrest/commit/3fc3690dd77ef5fa032abb006558184164db53ec)

**Mejoras:**

- Permitir omitir las comprobaciones del encabezado de página. (*Revisado por David Christensen. Sugerido por David Christensen.*)

  Las comprobaciones de cabecera realizadas al verificar las sumas de páginas pueden notificar falsos errores en páginas cifradas. Establece `page-header-check=n` para omitirlas. Están activadas por defecto.

  Solicitud de incorporación [#2045](https://github.com/pgbackrest/pgbackrest/pull/2045); Commit [`f5e6bc2`](https://github.com/pgbackrest/pgbackrest/commit/f5e6bc26983396ec51c6579aade37db39807f3a5)
- Evitar `chown()` en los archivos de recuperación durante la restauración. (*Revisado por Stefan Fercot, Marcelo Henrique Neppel. Sugerido por Marcelo Henrique Neppel.*)

  La restauración omitía `chown()` para archivos restaurados que ya tenían el propietario correcto, pero no para los archivos de recuperación que escribía. Ahora el controlador Posix también omite `chown()` si el propietario ya es correcto.

  Incidencia [#2036](https://github.com/pgbackrest/pgbackrest/issues/2036); Solicitud de incorporación [#2038](https://github.com/pgbackrest/pgbackrest/pull/2038); Commit [`3ff88ff`](https://github.com/pgbackrest/pgbackrest/commit/3ff88ffbb495fd669e9a361478e60192930ee0a1)
- Añadir detalle de reintento de error para los reintentos HTTP.

  Un error tras reintentos HTTP ahora informa del número de reintentos y del tiempo transcurrido.

  [`801e396`](https://github.com/pgbackrest/pgbackrest/commit/801e396dace2a4d9f4125ef0e751c90dc0cc644a) Mover los módulos de errores al directorio common/error.

  [`df419b3`](https://github.com/pgbackrest/pgbackrest/commit/df419b34b55a15a902ff5cc1912aaebc7e023738) Mejorar los mensajes de error de reintentos.

  [`f33e1cf`](https://github.com/pgbackrest/pgbackrest/commit/f33e1cfb1600643820a1ae76bdeb15c62ac1fcc7) Añadir detalle de reintento de error para los reintentos HTTP.

**Mejoras en la documentación:**

- Añadir una advertencia sobre el uso de la recuperación `type=none`. (*Revisado por Stefan Fercot.*)

  La recuperación con `type=none` no incrementa la línea temporal al finalizar. Esto puede hacer que PostgreSQL intente archivar WAL duplicado, que se rechace y llene el disco, o que herramientas como `pg_rewind` fallen o corrompan el clúster. Ahora la documentación advierte sobre ello.

  Incidencia [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); Solicitud de incorporación [#2069](https://github.com/pgbackrest/pgbackrest/pull/2069); Commit [`a28b72c`](https://github.com/pgbackrest/pgbackrest/commit/a28b72c62431bcf9df02791219d9d6f5d0e60b54)
- Añadir una nota sobre la ejecución de `stanza-create` en repositorios ya creados.

  Se omiten las stanzas que ya existen, por lo que es seguro repetir `stanza-create`, por ejemplo tras configurar un repositorio nuevo.

  Commit [`0c1f823`](https://github.com/pgbackrest/pgbackrest/commit/0c1f823e7a3abf1cadb44de3832ec1ddb2da7ec8)

### Notas de la versión v2.45 {#v245-release-notes}

*Copia de seguridad incremental por bloques (BETA)*

*Publicada el 20 de marzo de 2023*

**Correcciones de errores:**

- Omitir por defecto la escritura de `recovery.signal` para restauraciones de copias de seguridad sin conexión. (*Revisado por Stefan Fercot. Reportado por Marcel Borger.*)

  En PostgreSQL >= 12, `recovery.signal` impide arrancar si la copia se hizo sin conexión con `wal_level=minimal`. Ahora se omite ese archivo al restaurar copias sin conexión, salvo que se establezca `type` explícitamente, por ejemplo para recuperar a un punto en el tiempo una copia sin conexión con un `wal_level` mayor.

  [`0818601`](https://github.com/pgbackrest/pgbackrest/commit/0818601c055724bde3b97d4b02d3a38b0a53899a) Establecer el indicador online del manifiesto en las pruebas unitarias command/restore.

  [`2fa7e53`](https://github.com/pgbackrest/pgbackrest/commit/2fa7e53c5d4b5a5fd79f62d39763746727a5b9be) Omitir por defecto la escritura de `recovery.signal` para restauraciones de copias de seguridad sin conexión.; Incidencia [#2018](https://github.com/pgbackrest/pgbackrest/issues/2018); Solicitud de incorporación [#2019](https://github.com/pgbackrest/pgbackrest/pull/2019)

**Funcionalidades:**

- Copia de seguridad incremental por bloques (BETA). (*Revisado por John Morris, Stephen Frost, Stefan Fercot.*)

  Los incrementales por bloques solo almacenan las partes modificadas desde la copia anterior en lugar del archivo completo. Se activan con `repo-block`, que requiere `repo-bundle`. La función está en beta y también requiere la opción `beta`. No la uses en producción: el formato en disco cambiará antes de la versión definitiva.

  [`089fae0`](https://github.com/pgbackrest/pgbackrest/commit/089fae035bf0a9778fff0527ea3cbb113625a403) Añadir incrementales por bloques a la salida de la prueba real/all.

  [`3feed38`](https://github.com/pgbackrest/pgbackrest/commit/3feed389a2199454db68e446851323498b45db20) Mejorar el manejo del fin de archivo en IoChunkedRead.

  [`d520816`](https://github.com/pgbackrest/pgbackrest/commit/d520816acf9ecb01ef805cecbc9de7e8d0a9f468) Eliminar la lista de parámetros de deltaMapNew().

  [`779efe0`](https://github.com/pgbackrest/pgbackrest/commit/779efe0d7a54340141e01597279e9ab1d0bd0773) Declarar de forma coherente el tamaño incremental por bloques como size_t.

  [`dffc933`](https://github.com/pgbackrest/pgbackrest/commit/dffc933384e4327e2fd52868dd19668ed9d3ed91) Renombrar DeltaMap como BlockHash.

  [`a9867cb`](https://github.com/pgbackrest/pgbackrest/commit/a9867cb0b8e8d7abcac9b18b76e3e490c265f3cb) Añadir las opciones repo-block-age-map y repo-block-size-map.

  [`16ac5ee`](https://github.com/pgbackrest/pgbackrest/commit/16ac5ee8d3b926464cd27e8f064579f1e7935f4c) Renombrar las claves del manifiesto incremental por bloques.

  [`da91858`](https://github.com/pgbackrest/pgbackrest/commit/da9185870222057b97365f5db0acf797f959ec5e) Añadir un formato raw opcional para los tipos de compresión.

  [`7e5adc0`](https://github.com/pgbackrest/pgbackrest/commit/7e5adc03594a3b7a975001e80902a51df3ddd577) Usar compresión y cifrado raw para la agrupación y las copias incrementales por bloques.

  [`8b5153a`](https://github.com/pgbackrest/pgbackrest/commit/8b5153ad210011812c8fe6db2f2ed829a5aa543a) Superbloques de copias incrementales a nivel de bloque.; Solicitud de incorporación [#1996](https://github.com/pgbackrest/pgbackrest/pull/1996)

  [`210bed4`](https://github.com/pgbackrest/pgbackrest/commit/210bed4511ae5523b170eb193b877346d787140d) Usar xxHash en lugar de SHA-1 para las sumas de verificación incrementales por bloques.

  [`6252c0e`](https://github.com/pgbackrest/pgbackrest/commit/6252c0e4485caee362edec13302a5f735a69bff4) Excluir el tamaño del conjunto de copia de info para las copias incrementales por bloques.

  [`1119a53`](https://github.com/pgbackrest/pgbackrest/commit/1119a5353911d6d326edac325f530bb796a806ae) Renombrar BlockHash como BlockChecksum.

  [`6b409d0`](https://github.com/pgbackrest/pgbackrest/commit/6b409d049eb935146f7996b75b97744b75c411a9) Actualizar los valores predeterminados de tamaño de bloque y superbloque según las pruebas.

  [`1281a6e`](https://github.com/pgbackrest/pgbackrest/commit/1281a6eaf8552232c8c9af4d7fc15c082a7794d9) Garantizar que no haya continuaciones cuando el tamaño de bloque sea igual al de superbloque.

  [`5c1f78d`](https://github.com/pgbackrest/pgbackrest/commit/5c1f78d4dd62c37218285d13b09a9450eb3a588e) Corregir una errata en blockIncrProcess().

  [`c30d3e4`](https://github.com/pgbackrest/pgbackrest/commit/c30d3e439b77d544477e289606d30d0c8ffe301f) Correcciones y mejoras del mapa incremental por bloques.; Solicitud de incorporación [#2026](https://github.com/pgbackrest/pgbackrest/pull/2026)

  [`24f7252`](https://github.com/pgbackrest/pgbackrest/commit/24f725212d0c1dedc0f34fe4e939e481585ff697) Añadir la infraestructura para funciones beta.

  [`04d224b`](https://github.com/pgbackrest/pgbackrest/commit/04d224b88e73194ff1c6497dbecaaff392008dfe) Añadir la función beta y documentación para copias incrementales por bloques.

  Desarrollo en [v2.44](#v244-release-notes):

  [`912eec6`](https://github.com/pgbackrest/pgbackrest/commit/912eec63bb971c10a545e582f628c982f4e00005) Copia incremental a nivel de bloque.; Incidencia [#959](https://github.com/pgbackrest/pgbackrest/issues/959); Incidencia [#1806](https://github.com/pgbackrest/pgbackrest/issues/1806); Incidencia [#1913](https://github.com/pgbackrest/pgbackrest/issues/1913); Solicitud de incorporación [#1916](https://github.com/pgbackrest/pgbackrest/pull/1916)

  Desarrollo en [v2.42](#v242-release-notes):

  [`1ea6a41`](https://github.com/pgbackrest/pgbackrest/commit/1ea6a4142e47e2e0b56911ad1f028dfcddc5fd64) Mejorar las actualizaciones del archivo de manifiesto.; Solicitud de incorporación [#1888](https://github.com/pgbackrest/pgbackrest/pull/1888)

  [`c647bcb`](https://github.com/pgbackrest/pgbackrest/commit/c647bcb50954f623d29104cdb8a1457ed8e94579) Añadir indicadores al manifiesto para el procesamiento de archivos durante la copia.; Solicitud de incorporación [#1889](https://github.com/pgbackrest/pgbackrest/pull/1889)

  [`102ce5d`](https://github.com/pgbackrest/pgbackrest/commit/102ce5dee47e8d9a8d2eeaf2b2cc2bac105914ef) Añadir una lista persistente de referencias al manifiesto.; Solicitud de incorporación [#1890](https://github.com/pgbackrest/pgbackrest/pull/1890)

  [`ac99201`](https://github.com/pgbackrest/pgbackrest/commit/ac99201c0ebde616279214e600e49fdf506f7469) Añadir bufferSize a cvtUInt64FromVarInt128() para limitar más las lecturas.

  [`5602f17`](https://github.com/pgbackrest/pgbackrest/commit/5602f179a177a8513b96c762590829c012c28175) Añadir codificación y decodificación varint-128 a IoRead/IoWrite.; Solicitud de incorporación [#1891](https://github.com/pgbackrest/pgbackrest/pull/1891)

  [`352cbf1`](https://github.com/pgbackrest/pgbackrest/commit/352cbf1d5738a720292b5067051a05efc2b9a8ac) Cambiar los booleanos de ManifestFile a campos de bits.

  [`e7e106f`](https://github.com/pgbackrest/pgbackrest/commit/e7e106f781be01027d4829b258902549eb36eb7b) Usar almacenamiento de solo lectura para calcular la suma de verificación en restoreFile().

  [`909be41`](https://github.com/pgbackrest/pgbackrest/commit/909be412f8ad0d87f23ce2a2dbca94c3e0732f9f) Intercambiar las pruebas unitarias command/backup y command/restore.

  [`1730ef4`](https://github.com/pgbackrest/pgbackrest/commit/1730ef4ac3d88137bd218e6128b0107a8bf2c121) Añadir el indicador noTruncate a storageNewWriteP().; Solicitud de incorporación [#1898](https://github.com/pgbackrest/pgbackrest/pull/1898)

  [`fee38c2`](https://github.com/pgbackrest/pgbackrest/commit/fee38c2c7cc3ae318bf0d3b50fe23c22900c2311) Pasar los filtros al almacenamiento remoto como un array de manejadores.

  [`5fceee8`](https://github.com/pgbackrest/pgbackrest/commit/5fceee88a9439460bf24082f275ec2e695cc6bf6) Añadir backupFileRepoPathP().

  [`221db61`](https://github.com/pgbackrest/pgbackrest/commit/221db610d2a054ed00ad27377663941abfb9fb98) Acortar los nombres de la matriz de pruebas de integración real/all.

  [`c9db7bc`](https://github.com/pgbackrest/pgbackrest/commit/c9db7bc274211820030c4ab6ab8c70c1b1896254) Actualizar cipherBlockNew() para permitir parámetros opcionales.

  [`58b3c91`](https://github.com/pgbackrest/pgbackrest/commit/58b3c91babc6af9e003e5ef09bf99becf8a6f827) Añadir un modo raw a CipherBlock para ahorrar espacio.

**Mejoras:**

- Mantener solo un índice de grupo con todos los valores por defecto. (*Revisado por Stefan Fercot.*)

  Una opción no aplicable, como `repo2-s3-key` si `repo2-type` no es `s3`, podía añadir un repositorio fantasma con solo valores predeterminados. Ahora se eliminan los índices de repositorio y PostgreSQL que solo tengan valores predeterminados, salvo que no quede ningún otro índice.

  Solicitud de incorporación [#2011](https://github.com/pgbackrest/pgbackrest/pull/2011); Commit [`1648c13`](https://github.com/pgbackrest/pgbackrest/commit/1648c133d6bc1ffd0682ae6219934d00295aa580)

**Mejoras en la documentación:**

- Añadir instrucciones explícitas para actualizar entre versiones `2.x`. (*Contribución de Christophe Courtois. Revisado por David Steele.*)

  Una nueva sección de la guía explica que para actualizar entre versiones `2.x` solo hay que instalar los nuevos binarios. También se puede volver a una versión anterior si no se han usado funciones que esta no admita.

  Incidencia [#1774](https://github.com/pgbackrest/pgbackrest/issues/1774); Solicitud de incorporación [#1993](https://github.com/pgbackrest/pgbackrest/pull/1993); Commit [`15d5dcd`](https://github.com/pgbackrest/pgbackrest/commit/15d5dcdd3bb387aab28bbe7262011c38c7d6d22c)
- Eliminar las referencias a SSH que quedaron obsoletas cuando se introdujo TLS.

  La ayuda de `repo-host`, `pg-host` y sus opciones de puerto ya no presenta SSH como el único protocolo remoto. También se eliminaron los detalles de compresión SSH.

  Commit [`c5907a2`](https://github.com/pgbackrest/pgbackrest/commit/c5907a2e7193ca8f79cf56dca23e0df118e686c3)

### Notas de la versión v2.44 {#v244-release-notes}

*Eliminación del soporte de PostgreSQL 9.0/9.1/9.2*

*Publicada el 30 de enero de 2023*

**Mejoras:**

- Eliminar el soporte de PostgreSQL `9.0`/`9.1`/`9.2`. (*Revisado por Stefan Fercot.*)

  pgBackRest ahora admite diez versiones de PostgreSQL: las cinco con soporte y las cinco últimas que llegaron al final de su vida útil. A partir de PostgreSQL 15, quedan excluidas `9.0`, `9.1` y `9.2`.

  Solicitud de incorporación [#1941](https://github.com/pgbackrest/pgbackrest/pull/1941); Commit [`77c721e`](https://github.com/pgbackrest/pgbackrest/commit/77c721eb635c6d757d2d5ed6f2ffc083720c10a7)
- Mostrar errores al restaurar cuando ninguna copia de seguridad coincide con la versión actual de PostgreSQL. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Soulou.*)

  Tras un `stanza-upgrade` sin una copia nueva, la restauración usaba la última copia, creada con la versión anterior de PostgreSQL. Las réplicas construidas así podían fallar. Ahora se genera un error en este caso salvo que se indique `set` o `type=time`/`type=lsn`.

  Incidencia [#1942](https://github.com/pgbackrest/pgbackrest/issues/1942); Solicitud de incorporación [#1967](https://github.com/pgbackrest/pgbackrest/pull/1967); Commit [`b9be4fa`](https://github.com/pgbackrest/pgbackrest/commit/b9be4fa54039e2c79fad0dc1552c7ffaf883004c)
- Añadir comprobación de rango para `compress-level` según cada `compress-type`. (*Revisado por Stefan Fercot. Sugerido por gkleen, ViperRu.*)

  El rango de `compress-level` era `0-9` para todos los `compress-type`. Es el rango de `gz`, pero solo una parte del permitido por `lz4` y `zst`. Ahora cada tipo tiene su propio rango, como `-7` a `22` para `zst`.

  Incidencia [#1216](https://github.com/pgbackrest/pgbackrest/issues/1216); Incidencia [#1931](https://github.com/pgbackrest/pgbackrest/issues/1931); Solicitud de incorporación [#1962](https://github.com/pgbackrest/pgbackrest/pull/1962); Commit [`44da314`](https://github.com/pgbackrest/pgbackrest/commit/44da314adb2b63f96b1d571f822e91a0e412e984)

**Mejoras en la documentación:**

- Añadir una advertencia sobre habilitar el «espacio de nombres jerárquico» en el almacenamiento de Azure. (*Revisado por Stefan Fercot. Sugerido por Vojtech Galda, Pluggi, asjonos.*)

  Con el «espacio de nombres jerárquico» activado, Azure exige eliminar los directorios por separado y `expire` falla. La guía ahora advierte que no debe activarse.

  Incidencia [#1770](https://github.com/pgbackrest/pgbackrest/issues/1770); Solicitud de incorporación [#1980](https://github.com/pgbackrest/pgbackrest/pull/1980); Commit [`3aea997`](https://github.com/pgbackrest/pgbackrest/commit/3aea997df5ace85251d0579ccbe13fa938f587ee)
- Añadir un reemplazo para los saltos de línea en el ejemplo de monitoreo. (*Revisado por Stefan Fercot. Sugerido por rudonx, gmustdie, Ivan Shelestov.*)

  El ejemplo de supervisión fallaba si la salida de `info` contenía un salto de línea, como en algunos errores, porque `COPY` convierte `\n` en un salto que `jsonb` rechaza. Ahora el ejemplo sustituye los saltos antes de convertir a `jsonb`.

  Incidencia [#1910](https://github.com/pgbackrest/pgbackrest/issues/1910); Solicitud de incorporación [#1963](https://github.com/pgbackrest/pgbackrest/pull/1963); Commit [`ae258f6`](https://github.com/pgbackrest/pgbackrest/commit/ae258f604e634f1d2a760ffdb92dd359fd1129bb)
- Aclarar el comportamiento de `target-action` en varias versiones de PostgreSQL. (*Contribución de Chris Bandy. Revisado por David Steele, Anton Kurochkin, Stefan Fercot. Sugerido por Anton Kurochkin, Chris Bandy.*)

  El efecto de `pause` depende de `hot_standby` y de la versión de PostgreSQL. Con `hot_standby=off`, `pause` actúa como `shutdown` en PostgreSQL >= 12 y como `promote` en versiones anteriores.

  Incidencia [#987](https://github.com/pgbackrest/pgbackrest/issues/987); Incidencia [#1314](https://github.com/pgbackrest/pgbackrest/issues/1314); Solicitud de incorporación [#1960](https://github.com/pgbackrest/pgbackrest/pull/1960); Commit [`84a3ff8`](https://github.com/pgbackrest/pgbackrest/commit/84a3ff8b7ac1243c0b47c6585697f4fcf3c12065)
- Actualizaciones y aclaraciones a la página de índice. (*Revisado por Stefan Fercot.*)

  La sección que afirmaba que otras soluciones de copia no admitían procesamiento paralelo ya no era correcta y se reformuló. Otras secciones se actualizaron para usar términos actuales y mejorar la claridad.

  Solicitud de incorporación [#1966](https://github.com/pgbackrest/pgbackrest/pull/1966); Commit [`36ee30d`](https://github.com/pgbackrest/pgbackrest/commit/36ee30d118ce6cc7720653a3d3a49a06c655c463)
- Añadir el modo oscuro al sitio web. (*Sugerido por Stephen Frost.*)

  El sitio utiliza colores oscuros cuando el navegador prefiere un esquema oscuro.

  Commit [`ed818b3`](https://github.com/pgbackrest/pgbackrest/commit/ed818b31867c640d72ef829dd36cd0a7feff12df)

### Notas de la versión v2.43 {#v243-release-notes}

*Corrección de error*

*Publicada el 28 de noviembre de 2022*

**Correcciones de errores:**

- Corregir una referencia faltante en la copia de seguridad diff/incr. (*Revisado por Stefan Fercot. Reportado por Marcel Borger, ulfedf, jaymefSO.*)

  En v2.42, una copia diferencial o incremental fallaba con "unable to find '...' in string list" si la copia anterior se había creado con una versión previa. Ahora la lista de referencias de un manifiesto antiguo incluye la etiqueta de la propia copia.

  [`28f6604`](https://github.com/pgbackrest/pgbackrest/commit/28f660482aa5abb97850a9d7c89c2e5e9f23a4c9) Mover la prueba manifestBackupLabelSet() en la unidad info/manifest.

  [`c4bf775`](https://github.com/pgbackrest/pgbackrest/commit/c4bf775099c85e3cd081f9c1ce35efd4c71d9161) Corregir una referencia faltante en la copia de seguridad diff/incr.; Incidencia [#1933](https://github.com/pgbackrest/pgbackrest/issues/1933); Solicitud de incorporación [#1935](https://github.com/pgbackrest/pgbackrest/pull/1935)

**Mejoras:**

- Añadir una sugerencia cuando se especifica una opción sin índice. (*Revisado por Stefan Fercot.*)

  Una opción que requiere índice, como `repo-storage-ca-file`, ahora da error con una indicación del nombre indexado, como `repo1-storage-ca-file`. Las opciones obsoletas también muestran una indicación con su nombre actual.

  Incidencia [#1925](https://github.com/pgbackrest/pgbackrest/issues/1925); Solicitud de incorporación [#1929](https://github.com/pgbackrest/pgbackrest/pull/1929); Commit [`3f363cb`](https://github.com/pgbackrest/pgbackrest/commit/3f363cb3aed1a7c6836ee6c32eae600129a6f6b8)

### Notas de la versión v2.42 {#v242-release-notes}

*Correcciones de errores*

*Publicada el 22 de noviembre de 2022*

**Correcciones de errores:**

- Corregir una fuga de memoria en `backup`/`restore` de agrupamientos de archivos. (*Revisado por John Morris. Probado por Oscar. Reportado por Oscar.*)

  La restauración no liberaba algunos objetos de E/S de archivos agrupados hasta restaurar todos los del grupo. Con muchos archivos pequeños, la memoria crecía hasta fallar con "unable to allocate". La reanudación de copias tenía una fuga similar, de menor tamaño.

  Incidencia [#1877](https://github.com/pgbackrest/pgbackrest/issues/1877); Solicitud de incorporación [#1878](https://github.com/pgbackrest/pgbackrest/pull/1878); Commit [`cd8db7d`](https://github.com/pgbackrest/pgbackrest/commit/cd8db7d9e53e041ad6fb31f2f015541c1d24abc2)
- Corregir un error de protocolo en una lectura corta de un archivo remoto. (*Revisado por Stephen Frost.*)

  Una lectura remota que terminaba antes de tiempo o fallaba dejaba el protocolo en un estado incorrecto. El siguiente comando fallaba con "client state is 'data-get' but expected 'idle'" y se perdía el error original. Ahora se lee el resto del archivo al cerrarlo.

  [`ea162e8`](https://github.com/pgbackrest/pgbackrest/commit/ea162e821634919b7c839e866b99bf82010dbacc) Mover storageReadRemoteOpen() en el módulo storage/remote/read.

  [`7967c75`](https://github.com/pgbackrest/pgbackrest/commit/7967c750d83466d030081e9deb1d70a1ba240271) Corregir un error de protocolo en una lectura corta de un archivo remoto.; Solicitud de incorporación [#1900](https://github.com/pgbackrest/pgbackrest/pull/1900)

**Mejoras:**

- No almacenar referencias de archivos de longitud cero al agrupar. (*Revisado por Stefan Fercot.*)

  Las copias diferenciales e incrementales agrupadas guardaban referencias a copias anteriores para archivos de longitud cero, que no se almacenan en ninguna copia. La referencia se ignoraba al restaurar, pero ocupaba espacio en el manifiesto.

  Solicitud de incorporación [#1887](https://github.com/pgbackrest/pgbackrest/pull/1887); Commit [`f981fb4`](https://github.com/pgbackrest/pgbackrest/commit/f981fb45d9931e597afec764e13b1a53d8365d25)
- Usar descripciones más genéricas para `pg_start_backup()`/`pg_stop_backup()`. (*Revisado por Greg Sabino Mullane, David Christensen. Sugerido por Greg Sabino Mullane.*)

  PostgreSQL 15 renombró estas funciones a `pg_backup_start()`/`pg_backup_stop()`. Los registros y la documentación ahora usan descripciones independientes de la versión de PostgreSQL.

  Solicitud de incorporación [#1901](https://github.com/pgbackrest/pgbackrest/pull/1901); Commit [`ddd966c`](https://github.com/pgbackrest/pgbackrest/commit/ddd966cadc30440a81100144204d4084a0f2ac3a)

**Mejoras en la suite de pruebas:**

- Actualizar la opción `--psql-bin` de `test.pl` para que coincida con la ayuda de línea de comandos. (*Contribución de Koshi Shibagaki. Revisado por David Steele.*)

  La ayuda mostraba `--psql-bin`, pero la opción se llamaba `--pgsql-bin`. Ahora tiene el nombre que mostraba la ayuda.

  Solicitud de incorporación [#1920](https://github.com/pgbackrest/pgbackrest/pull/1920); Commit [`3ad5884`](https://github.com/pgbackrest/pgbackrest/commit/3ad588443b452e04f3abcc107e825dc47e078103)

### Notas de la versión v2.41 {#v241-release-notes}

*Anotaciones de copias de seguridad*

*Publicada el 19 de septiembre de 2022*

**Correcciones de errores:**

- Corregir la expiración de tiempo incorrecta que se usaba para repositorios no predeterminados. (*Revisado por Stefan Fercot. Reportado por Adam Brusselback.*)

  Al ejecutar `expire` sin `repo`, se leía el `repo-retention-full` temporal de todos los repositorios desde el de menor número. Ahora cada repositorio usa su propio valor.

  Incidencia [#1852](https://github.com/pgbackrest/pgbackrest/issues/1852); Solicitud de incorporación [#1854](https://github.com/pgbackrest/pgbackrest/pull/1854); Commit [`eda7f81`](https://github.com/pgbackrest/pgbackrest/commit/eda7f81ee4fd6818ce458768144fc3fc1e1f0f21)
- Corregir un problema al listar directorios recursivamente con un filtro. (*Revisado por Stephen Frost. Reportado por Efremov Egor.*)

  `repo-ls` con `recurse` y `filter` podía fallar por doble liberación o fallo de segmentación si la última entrada de un directorio era otro directorio con contenido. La lista del padre se liberaba antes de procesar las entradas de sus subdirectorios.

  Incidencia [#1870](https://github.com/pgbackrest/pgbackrest/issues/1870); Solicitud de incorporación [#1871](https://github.com/pgbackrest/pgbackrest/pull/1871); Commit [`c39c9f2`](https://github.com/pgbackrest/pgbackrest/commit/c39c9f220ed328b4175d912e109697b726e9ea9b)

**Funcionalidades:**

- Anotaciones clave/valor para copias de seguridad. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Adam Berlin.*)

  Añade anotaciones clave/valor a una copia con `annotation` de `backup` y después agrégalas, modifícalas o elimínalas con el nuevo comando `annotate`. `info` las muestra en texto cuando se indica `set` y siempre las incluye en JSON.

  Incidencia [#1709](https://github.com/pgbackrest/pgbackrest/issues/1709); Solicitud de incorporación [#1724](https://github.com/pgbackrest/pgbackrest/pull/1724); Commit [`381fd0a`](https://github.com/pgbackrest/pgbackrest/commit/381fd0a5a4de61624615b150ba98beeafac31f7e)

**Mejoras:**

- Soportar `--set` en la salida JSON del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Anton Kurochkin.*)

  Con `set`, la salida JSON de `info` ahora incluye los detalles que ya mostraba el texto, como las listas de errores y espacios de tablas.

  Incidencia [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Solicitud de incorporación [#1501](https://github.com/pgbackrest/pgbackrest/pull/1501); Commit [`db75ffd`](https://github.com/pgbackrest/pgbackrest/commit/db75ffd27037d690a11eb02902f929250fe2bf5b)
- Permitir configurar el tamaño de fragmento de carga para almacenes de objetos. (*Revisado por Stefan Fercot. Sugerido por Anton Glushakov.*)

  Establece `repo-storage-upload-chunk-size` para cambiar el tamaño de cada fragmento de carga en S3, GCS o Azure. Los fragmentos mayores pueden mejorar el rendimiento, pero consumen más memoria. Los valores predeterminados no cambian.

  [`ff1188f`](https://github.com/pgbackrest/pgbackrest/commit/ff1188f92dfc9e8f6d4aeca8b71a9886f24f58b4) Permitir la etiqueta quote en la ayuda de línea de comandos.

  [`b05d31f`](https://github.com/pgbackrest/pgbackrest/commit/b05d31f531b55b747175cf94c963f95574c54d2b) Permitir configurar el tamaño de fragmento de carga para almacenes de objetos.; Incidencia [#1843](https://github.com/pgbackrest/pgbackrest/issues/1843); Solicitud de incorporación [#1847](https://github.com/pgbackrest/pgbackrest/pull/1847)
- Actualizar las marcas de tiempo de archive.info después de una copia de seguridad exitosa. (*Revisado por Stefan Fercot. Sugerido por Alex Richman.*)

  `archive.info` y su copia solo se escribían con `stanza-create` y `stanza-upgrade`, y una política de ciclo de vida que caducara archivos antiguos podía eliminarlos. Ahora se actualizan sus marcas de tiempo tras cada copia correcta.

  Incidencia [#1853](https://github.com/pgbackrest/pgbackrest/issues/1853); Solicitud de incorporación [#1855](https://github.com/pgbackrest/pgbackrest/pull/1855); Commit [`3b5df1e`](https://github.com/pgbackrest/pgbackrest/commit/3b5df1e089234d425dd225f8c1976755dc947c8a)
- Mover la comprobación de línea de tiempo de la réplica después del checkpoint. (*Revisado por Stefan Fercot. Probado por Keith Fiske. Sugerido por Keith Fiske.*)

  La comprobación de la línea temporal del servidor en espera usaba el `pg_control` anterior al inicio de la copia. Justo después de una promoción, `pg_control` podía no contener aún la nueva línea temporal y la copia fallaba con "standby is on timeline ... but expected ...". Ahora se comprueba después del punto de control.

  Incidencia [#1816](https://github.com/pgbackrest/pgbackrest/issues/1816); Solicitud de incorporación [#1819](https://github.com/pgbackrest/pgbackrest/pull/1819); Commit [`c267ba5`](https://github.com/pgbackrest/pgbackrest/commit/c267ba51b1778b5872f4ee928a9614545d743f3f)
- Mejorar el mensaje de advertencia al reanudar una copia de seguridad. (*Sugerido por Cynthia Shang.*)

  La advertencia parecía exigir una intervención del usuario. Ahora indica que se eliminarán los archivos no válidos y después se reanudará la copia.

  Commit [`cbbe93f`](https://github.com/pgbackrest/pgbackrest/commit/cbbe93f592d8097393c5ffe214f0a8c5fb0549c1)

**Mejoras en la documentación:**

- Añadir la ruta absoluta de `kill` en `pgbackrest.service`. (*Sugerido por Don Seiler.*)

  El ejemplo de `pgbackrest.service` ahora utiliza `/bin/kill` en `ExecReload`. Las versiones antiguas de systemd requieren una ruta absoluta.

  Commit [`e9ff524`](https://github.com/pgbackrest/pgbackrest/commit/e9ff5248039eedb25da2fee550ec64fcebbc51c7)

### Notas de la versión v2.40 {#v240-release-notes}

*Soporte de OpenSSL 3*

*Publicada el 18 de julio de 2022*

**NOTA PARA EMPAQUETADORES**: Se ha añadido una compilación experimental con meson, pero los empaquetadores deberían seguir usando la compilación con autoconf/make en el futuro previsible.

**Mejoras:**

- Soporte de OpenSSL 3. (*Revisado por Stephen Frost.*)

  pgBackRest ahora compila con OpenSSL 3. Se suprimen las advertencias de obsolescencia y se detecta un EOF inesperado con los códigos de error que informa OpenSSL 3.

  Solicitud de incorporación [#1767](https://github.com/pgbackrest/pgbackrest/pull/1767); Commit [`08242ee`](https://github.com/pgbackrest/pgbackrest/commit/08242ee6ac93b9eb9c05cc39e3db15bbafb9052c)
- Crear una instantánea al listar el contenido de una ruta. (*Revisado por John Morris, Stephen Frost.*)

  Un listado sin ordenar leía las entradas mientras las procesaba. Si se borraban archivos durante el listado, algunos sistemas de archivos omitían otros que aún existían y no se podía eliminar la ruta. Ahora los listados siempre usan una instantánea de la ruta.

  [`61ca9b5`](https://github.com/pgbackrest/pgbackrest/commit/61ca9b58a000aa8789ef3267682519bdb15e8a6b) Sustituir hrnStorageInfoListCallback() por TEST_STORAGE_LIST() en las pruebas.

  [`1c0bf0b`](https://github.com/pgbackrest/pgbackrest/commit/1c0bf0b15da8c0d15cc639851ff1d1bd05b51d06) Reordenar las comprobaciones de usuario y grupo null en el protocolo remoto y añadir pruebas.

  [`72960bb`](https://github.com/pgbackrest/pgbackrest/commit/72960bbf179b4e8051bd4fc50be57d95159e9e13) Renombrar strTrunc() como strTruncIdx() y añadir strTrunc().

  [`75623d4`](https://github.com/pgbackrest/pgbackrest/commit/75623d4583bfdaccb3a19b935fd04d744b363923) Crear una instantánea al listar el contenido de una ruta.; Incidencia [#1754](https://github.com/pgbackrest/pgbackrest/issues/1754); Solicitud de incorporación [#1805](https://github.com/pgbackrest/pgbackrest/pull/1805)
- Forzar `target-timeline=current` cuando la restauración es `type=immediate`. (*Revisado por Stephen Frost.*)

  En PostgreSQL >= 12, la línea temporal de destino predeterminada es `latest`, y la recuperación podía fallar si no era alcanzable desde la copia. Como `type=immediate` no cambia de línea temporal, ahora establece el destino en `current`.

  Solicitud de incorporación [#1814](https://github.com/pgbackrest/pgbackrest/pull/1814); Commit [`364af16`](https://github.com/pgbackrest/pgbackrest/commit/364af1635d40431276cc6fd87d6ddd689b611e09)
- Truncar archivos durante `restore` delta cuando son más grandes de lo esperado. (*Revisado por Stephen Frost.*)

  La restauración delta copiaba un archivo del repositorio si su tamaño difería del manifiesto. Ahora se trunca un archivo mayor al tamaño del manifiesto y solo se copia si no coincide su suma de verificación. Ya no se copian archivos a los que solo se ha añadido contenido, como registros.

  Solicitud de incorporación [#1758](https://github.com/pgbackrest/pgbackrest/pull/1758); Commit [`7ec51e7`](https://github.com/pgbackrest/pgbackrest/commit/7ec51e7e6279ea576ad3b4b5c2ea1fc389d08ab5)
- Desactivar el guardado incremental del manifiesto cuando `resume=n`. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Durante una copia se guarda periódicamente el manifiesto para poder reanudar. Ahora se omiten estas escrituras con `resume=n`.

  Solicitud de incorporación [#1760](https://github.com/pgbackrest/pgbackrest/pull/1760); Commit [`60d70fa`](https://github.com/pgbackrest/pgbackrest/commit/60d70fa66fc3f709914f40dd088bac1b467001f2)
- Establecer el porcentaje completado de la copia de seguridad en cero antes de iniciar la copia. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  El progreso de una copia no se mostraba hasta copiar el primer archivo. Ahora se establece en cero al comenzar a copiar.

  Solicitud de incorporación [#1759](https://github.com/pgbackrest/pgbackrest/pull/1759); Commit [`38ad283`](https://github.com/pgbackrest/pgbackrest/commit/38ad2838d553febae1b7fe0244d942dfaa9cf548)
- Usar la bandera `IsTruncated` de S3 para determinar la continuación del listado. (*Revisado por John Morris. Probado por Soulou. Sugerido por Christian Montagne.*)

  Las versiones recientes de Scality envían un `NextContinuationToken` vacío cuando una lista no está truncada, causando un bucle infinito. Ahora `IsTruncated` determina si continúa, y la ausencia de token o un token vacío en una lista truncada es un error.

  Incidencia [#1748](https://github.com/pgbackrest/pgbackrest/issues/1748); Solicitud de incorporación [#1783](https://github.com/pgbackrest/pgbackrest/pull/1783); Commit [`845d82f`](https://github.com/pgbackrest/pgbackrest/commit/845d82f6825d4101e6a465a435ef056ff6ec15a2)

**Correcciones de errores en la documentación:**

- Omitir las opciones internas en la referencia de configuración. (*Reportado por Francisco Miguel Biete Banon.*)

  Las opciones internas solo para algunos comandos aparecían en la referencia de configuración. La ayuda de línea de comandos no se veía afectada.

  Commit [`2643050`](https://github.com/pgbackrest/pgbackrest/commit/2643050be0dc4b7363c434f58373919bd6fdac68)

**Mejoras en la documentación:**

- Añadir un enlace a la configuración de PostgreSQL en la sección del host del repositorio. (*Revisado por Stefan Fercot. Sugerido por Julien Cigar.*)

  Solicitud de incorporación [#1809](https://github.com/pgbackrest/pgbackrest/pull/1809); Commit [`74a4ac8`](https://github.com/pgbackrest/pgbackrest/commit/74a4ac801db921f7b11b63b9f927228c6a6af861)

**Mejoras en la suite de pruebas:**

- Añadir compilación experimental con Meson. (*Revisado por Eli Schwartz, Sam Bassaly.*)

  Meson tiene una sintaxis más sencilla y mejor rendimiento que autoconf/make. Se utiliza para generar código y compilar pruebas, y da error en cualquier compilación que no sea de depuración. Los empaquetadores deben seguir utilizando autoconf/make.

  [`2feaaea`](https://github.com/pgbackrest/pgbackrest/commit/2feaaeaac803d6c0193477b56dbeb622fd991156) Añadir la extensión .inc a los archivos C incluidos en otros archivos C.

  [`b8fc20d`](https://github.com/pgbackrest/pgbackrest/commit/b8fc20d5b8e7ca003ff39f29ea6e3ba57653f55c) Añadir compilación experimental con Meson.; Solicitud de incorporación [#1765](https://github.com/pgbackrest/pgbackrest/pull/1765)

  [`665da12`](https://github.com/pgbackrest/pgbackrest/commit/665da12ae7f519077512e60ce3a5ec6c6a9997fd) Hacer más general el comentario de include en meson.build.

  [`9fd85a1`](https://github.com/pgbackrest/pgbackrest/commit/9fd85a104ad56061b028afd9057ce8c1d636d3dd) Desactivar meson para las compilaciones que no sean de depuración.

  [`59f148b`](https://github.com/pgbackrest/pgbackrest/commit/59f148bf6ea8c090d4d65ce5b135a71501e8ae22) Generar -fmacro-prefix-map para eliminar la ruta relativa de __FILE__.

  [`0eccbc8`](https://github.com/pgbackrest/pgbackrest/commit/0eccbc8bf47073ab8ec1f13fed9865d0bd7c3635) La compilación con Meson funciona en la versión 0.45.
- Permitir pasar cualquier ruta a la opción `--test-path`. (*Contribución de Andrey Sokolov. Revisado por David Steele.*)

  Solicitud de incorporación [#1764](https://github.com/pgbackrest/pgbackrest/pull/1764); Commit [`29b2a54`](https://github.com/pgbackrest/pgbackrest/commit/29b2a54fcc74457af5c63ffb505c5fbb24bb2ade)
- Corregir un error de compilación cuando `DEBUG_EXEC_TIME` se define sin `DEBUG`. (*Contribución de Andrey Sokolov. Revisado por David Steele.*)

  Sin `DEBUG`, el `ASSERT()` que usaba la hora de inicio desaparecía al expandirse y la variable sin uso provocaba un error de compilación. Ahora se usa `CHECK()`.

  Solicitud de incorporación [#1775](https://github.com/pgbackrest/pgbackrest/pull/1775); Commit [`1a00ab1`](https://github.com/pgbackrest/pgbackrest/commit/1a00ab10033e9ac6e6f797627567e8b91e143432)

### Notas de la versión v2.39 {#v239-release-notes}

*Verify y agrupamiento de archivos*

*Publicada el 16 de mayo de 2022*

**Correcciones de errores:**

- Corregir un error lanzado desde `FINALLY()` que causaba un bucle infinito. (*Revisado por Stephen Frost.*)

  Un error lanzado en un bloque `FINALLY()` devolvía el control al mismo bloque, donde probablemente volvía a lanzarse y causaba un bucle infinito. Ahora `FINALLY()` solo se ejecuta una vez.

  [`9a271e9`](https://github.com/pgbackrest/pgbackrest/commit/9a271e925c6239fbd3577f9827c34940e7e43ae4) Corregir un error lanzado desde `FINALLY()` que causaba un bucle infinito.; Solicitud de incorporación [#1732](https://github.com/pgbackrest/pgbackrest/pull/1732)

  [`ef4c4ab`](https://github.com/pgbackrest/pgbackrest/commit/ef4c4ab8525f81c9ed22c7e82ed12096e81703c5) Usar una variable en lugar de una función para seguir el estado de FINALLY().; Solicitud de incorporación [#1744](https://github.com/pgbackrest/pgbackrest/pull/1744)
- Generar error en todos los fallos de bloqueo excepto cuando otro proceso mantiene el bloqueo. (*Revisado por Reid Thompson. Probado por Geir Råness. Reportado por Geir Råness.*)

  `archive-get`/`archive-push` no daban error si no podían adquirir el bloqueo por otra causa, como permisos, y no iniciaban el proceso asincrónico. El usuario recibía un fallo genérico y no había registro asincrónico. Ahora esas situaciones son errores.

  Incidencia [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Solicitud de incorporación [#1730](https://github.com/pgbackrest/pgbackrest/pull/1730); Commit [`9629908`](https://github.com/pgbackrest/pgbackrest/commit/962990869454b15db058f4037dbc0b1b611fc95e)

**Funcionalidades:**

- Agrupamiento de archivos de la copia de seguridad para mejorar el soporte de archivos pequeños. (*Revisado por Reid Thompson, Stefan Fercot, Chris Bandy.*)

  La agrupación almacena juntos los archivos pequeños para ahorrar tiempo y espacio al copiar, especialmente en almacenes de objetos donde crear cada archivo es costoso. Se activa con `repo-bundle` y se ajusta con `repo-bundle-size` y `repo-bundle-limit`. La restauración lee los archivos contiguos de un grupo en una sola lectura.

  [`4d2fef1`](https://github.com/pgbackrest/pgbackrest/commit/4d2fef1c37d357965f0ffb9af0d7489f3be1371b) Eliminar una prueba redundante de restoreFile() y mejorar la cobertura.

  [`5141370`](https://github.com/pgbackrest/pgbackrest/commit/514137040e60e8fff0e7f42f43b493113abae5ff) Añadir el parámetro limit a ioCopyP().

  [`dca6da8`](https://github.com/pgbackrest/pgbackrest/commit/dca6da86bfe84a0cda004df1140d125db1630c90) Optimizar restore para la agrupación de archivos.; Incidencia [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Solicitud de incorporación [#1683](https://github.com/pgbackrest/pgbackrest/pull/1683)

  [`0054677`](https://github.com/pgbackrest/pgbackrest/commit/0054677147121967889ead7feab0959fb19e39a6) Añadir registro de grupos al comando backup.

  [`3f66f42`](https://github.com/pgbackrest/pgbackrest/commit/3f66f42ef9605a83c356e4c6eb3ef47bcb12c30d) Renombrar las opciones bundle-* a repo-bundle-*.; Solicitud de incorporación [#1694](https://github.com/pgbackrest/pgbackrest/pull/1694)

  [`fe9fd2f`](https://github.com/pgbackrest/pgbackrest/commit/fe9fd2ff2d778b86c0df159aabe7644f18f6479f) Desactivar repo-hardlink cuando esté activado repo-bundle.

  [`424008d`](https://github.com/pgbackrest/pgbackrest/commit/424008d293661dfb1a167cfec2697def48057447) Permitir archivos que pasan a longitud cero después de crear el manifiesto de copia.

  [`f405fc6`](https://github.com/pgbackrest/pgbackrest/commit/f405fc6ae281eebf4d61abb39963a9830fe2fa2f) Documentación de la agrupación de archivos de copia.; Solicitud de incorporación [#1740](https://github.com/pgbackrest/pgbackrest/pull/1740)

  Desarrollo en [v2.38](#v238-release-notes):

  [`a79034a`](https://github.com/pgbackrest/pgbackrest/commit/a79034ae2f6a8ec66b84c62ab6cd4042d2c1a249) Añadir rangos de lectura a todos los controladores de almacenamiento.; Solicitud de incorporación [#1619](https://github.com/pgbackrest/pgbackrest/pull/1619)

  [`b791f1c`](https://github.com/pgbackrest/pgbackrest/commit/b791f1c82f53fa16866837d4544b58243c682f7f) Implementar la asignación de propietario al restaurar sin modificar los datos internos del manifiesto.

  [`f84909f`](https://github.com/pgbackrest/pgbackrest/commit/f84909f85f7dfb202ac812c67665cc590a5acad4) Corregir el manejo del desplazamiento de lectura Posix tras un error.

  [`4ca0590`](https://github.com/pgbackrest/pgbackrest/commit/4ca0590a51a665535fbba903b8f55e10557b606a) Refactorizar backupProcessQueue() para usar la estructura BackupJobData.

  [`16559d9`](https://github.com/pgbackrest/pgbackrest/commit/16559d9e421c66596d21b047c8afe1b2c96ccd82) Usar la constante PG_FILE_POSTMTRPID donde corresponda.

  [`8c062e1`](https://github.com/pgbackrest/pgbackrest/commit/8c062e1af824c3dc80ff94b3df8d433f95e88d0f) Eliminar el indicador primary del manifiesto.; Solicitud de incorporación [#1630](https://github.com/pgbackrest/pgbackrest/pull/1630)

  [`b0db4b8`](https://github.com/pgbackrest/pgbackrest/commit/b0db4b8ff00db913cb69308017a56155d6070830) Simplificar el modo de la ruta base en las pruebas de integración mock/all.

  [`4a73a02`](https://github.com/pgbackrest/pgbackrest/commit/4a73a0286387f3f2185f3f193f9c20ed0d7d926d) Simplificar los valores predeterminados del manifiesto.; Solicitud de incorporación [#1631](https://github.com/pgbackrest/pgbackrest/pull/1631)

  [`575ae77`](https://github.com/pgbackrest/pgbackrest/commit/575ae77c0dee12b932469d479b2e45dbaf389737) Convertir varNewUInt64() a VARUINT64() donde sea posible en el manifiesto.

  [`61ce586`](https://github.com/pgbackrest/pgbackrest/commit/61ce58692f3092b72833b6e9ee87037f45b3b702) Empaquetar las estructuras de archivos del manifiesto para ahorrar memoria.; Solicitud de incorporación [#1626](https://github.com/pgbackrest/pgbackrest/pull/1626)

  [`ca13f11`](https://github.com/pgbackrest/pgbackrest/commit/ca13f11b4a3858587c7055b0b2b4a8b396dd8451) Optimizar jsonFromStrInternal().

  [`e4df5b7`](https://github.com/pgbackrest/pgbackrest/commit/e4df5b7d3846134832b9315e22786f679d63a46b) Simplificar los valores predeterminados de archivos del manifiesto.; Solicitud de incorporación [#1632](https://github.com/pgbackrest/pgbackrest/pull/1632)

  [`7dd657b`](https://github.com/pgbackrest/pgbackrest/commit/7dd657b7dd163ded9fbf7caef37eea7e08bc5a37) Simplificar la construcción de nombres de archivo en command/verify.

  [`34d6495`](https://github.com/pgbackrest/pgbackrest/commit/34d649579eb3bd1530aa99f0ed1879e7d3125424) Agrupar archivos en el repositorio durante la copia.; Incidencia [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Solicitud de incorporación [#1655](https://github.com/pgbackrest/pgbackrest/pull/1655)

  [`efc09db`](https://github.com/pgbackrest/pgbackrest/commit/efc09db7b9ece6e7b7f92538d56d6ab7b9798f8f) Limitar los archivos que pueden agruparse.; Incidencia [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); Solicitud de incorporación [#1662](https://github.com/pgbackrest/pgbackrest/pull/1662)

  [`e6e1122`](https://github.com/pgbackrest/pgbackrest/commit/e6e1122dbcf5e667d683295f7e7e45de4bbf56bd) Pasar el archivo por referencia en manifestFileAdd().
- Comando verify para validar el contenido de un repositorio. (*Contribución de Cynthia Shang, Reid Thompson. Revisado por David Steele, Stefan Fercot.*)

  `verify` comprueba que las copias y el WAL del repositorio sean válidos. Establece `output=text` para imprimir los resultados y `verbose` para incluir lo verificado correctamente además de los errores.

  Solicitud de incorporación [#1607](https://github.com/pgbackrest/pgbackrest/pull/1607); Commit [`65d22e4`](https://github.com/pgbackrest/pgbackrest/commit/65d22e43257d46ff6523ffbdb3af59e30deeaea5)
- Soporte de PostgreSQL 15. (*Revisado por Stefan Fercot.*)

  PostgreSQL 15 elimina la copia exclusiva, renombra las funciones de inicio y fin de copia y suprime `pg_database.datlastsysoid`, que pgBackRest ya no utiliza.

  [`692fe49`](https://github.com/pgbackrest/pgbackrest/commit/692fe496bdb5fa6dcffeb9f85b6188ceb1df707a) Eliminar la dependencia de pg_database.datlastsysoid.; Solicitud de incorporación [#1735](https://github.com/pgbackrest/pgbackrest/pull/1735)

  [`20782c8`](https://github.com/pgbackrest/pgbackrest/commit/20782c88bc8d0842d547bd5f4fecdb292e69d1f7) Soporte de PostgreSQL 15.; Solicitud de incorporación [#1736](https://github.com/pgbackrest/pgbackrest/pull/1736)
- Mostrar el porcentaje completado de la copia de seguridad en la salida de `info`. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  `info` muestra el porcentaje completado de una copia en el host donde se ejecuta. En JSON se expresa como un entero: el porcentaje multiplicado por 100.

  [`d9088b2`](https://github.com/pgbackrest/pgbackrest/commit/d9088b2e2b16a89d29b967187a547976f96061fc) Mostrar el porcentaje completado de la copia de seguridad en la salida de `info`.; Incidencia [#1490](https://github.com/pgbackrest/pgbackrest/issues/1490); Solicitud de incorporación [#1621](https://github.com/pgbackrest/pgbackrest/pull/1621)

  [`a6b1adb`](https://github.com/pgbackrest/pgbackrest/commit/a6b1adb5fd533b4b9aca29646c8acf647d872959) Eliminar un salto de línea sobrante al escribir un archivo de bloqueo.

  Desarrollo en [v2.38](#v238-release-notes):

  [`22734eb`](https://github.com/pgbackrest/pgbackrest/commit/22734eb376b3183924cb7794f9111c1eeb5d92d6) Añadir ioBufferReadNewOpen() e ioBufferWriteNewOpen().

  [`9b2f10d`](https://github.com/pgbackrest/pgbackrest/commit/9b2f10dbb49a8b869cef2c419d9957ed4c550016) Refactorizar el código de bloqueos.; Solicitud de incorporación [#1643](https://github.com/pgbackrest/pgbackrest/pull/1643)
- Autoselección de la copia de seguridad para el comando `restore` con `--type=lsn`. (*Contribución de Reid Thompson. Revisado por Stefan Fercot, David Steele.*)

  Con `type=lsn`, la restauración ahora selecciona la copia más reciente que terminó en el LSN `target` o antes.

  [`08d9e26`](https://github.com/pgbackrest/pgbackrest/commit/08d9e269c6f03e7797584e90c53eb0743b787f60) Refactorizar la comprobación del tipo de destino en restore para mayor claridad.

  [`d8d4132`](https://github.com/pgbackrest/pgbackrest/commit/d8d4132118edd7f93a5b221478c85c2d213c39dd) Autoselección de la copia de seguridad para el comando `restore` con `--type=lsn`.; Solicitud de incorporación [#1706](https://github.com/pgbackrest/pgbackrest/pull/1706)

  [`ea4d73f`](https://github.com/pgbackrest/pgbackrest/commit/ea4d73f375558c237fce696f20c19d1efef00bc1) Corregir el orden del campo backup-lsn-stop en la prueba unitaria command/restore.
- Suprimir la advertencia de WAL existente cuando `archive-mode-check` está deshabilitado. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Con `archive-mode-check=n` y envío de WAL desde varios hosts, es normal que ya exista en el archivo un WAL con la misma suma de verificación, por lo que ya no se avisa. Una suma distinta sigue siendo un error.

  Solicitud de incorporación [#1711](https://github.com/pgbackrest/pgbackrest/pull/1711); Commit [`aad7171`](https://github.com/pgbackrest/pgbackrest/commit/aad7171940afdb221a03825bee6eb2f1827289f1)
- Añadir soporte de AWS IMDSv2. (*Contribución de Nuno Pires. Revisado por David Steele.*)

  IMDSv2 protege los metadatos de instancia que proporcionan credenciales para `repo-s3-key-type=auto`. pgBackRest recurre a IMDSv1 si falla la solicitud del token IMDSv2.

  Incidencia [#1685](https://github.com/pgbackrest/pgbackrest/issues/1685); Solicitud de incorporación [#1691](https://github.com/pgbackrest/pgbackrest/pull/1691); Commit [`21cef09`](https://github.com/pgbackrest/pgbackrest/commit/21cef09dfd03c313531dc66ba9556164ae2835ab)

**Mejoras:**

- Permitir cambiar la opción `repo-hardlink` después de una copia de seguridad completa. (*Revisado por Reid Thompson.*)

  Cambiar `repo-hardlink` requería una copia completa nueva. Ahora se puede cambiar en cualquier momento, por ejemplo para desactivarlo al agrupar archivos.

  Solicitud de incorporación [#1699](https://github.com/pgbackrest/pgbackrest/pull/1699); Commit [`7afaac0`](https://github.com/pgbackrest/pgbackrest/commit/7afaac0a3d0e43e5598d1abf548559dbe6329363)
- Aumentar la precisión del registro de porcentaje completado para `backup` y `restore`. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Ahora se registra el porcentaje con centésimas, lo que permite actualizaciones más frecuentes en copias y restauraciones grandes.

  Solicitud de incorporación [#1679](https://github.com/pgbackrest/pgbackrest/pull/1679); Commit [`330e199`](https://github.com/pgbackrest/pgbackrest/commit/330e19900ee3415d920680cf6e6856bf5e8e9a69)
- Mejorar la validación de rutas para los comandos `repo-*`. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Una ruta no puede contener `//`, se elimina una `/` final y una ruta absoluta debe estar dentro de la ruta del repositorio.

  [`5ae84d5`](https://github.com/pgbackrest/pgbackrest/commit/5ae84d5e474e95dcc00c174aa5111815a5a70ba5) Mejorar la validación de rutas para los comandos `repo-*`.; Solicitud de incorporación [#1697](https://github.com/pgbackrest/pgbackrest/pull/1697)

  [`19dd015`](https://github.com/pgbackrest/pgbackrest/commit/19dd015d589ed3efd31a2a238249a150fb3748c1) Corregir problemas en la validación mejorada de rutas de los comandos repo-*.; Solicitud de incorporación [#1751](https://github.com/pgbackrest/pgbackrest/pull/1751)
- Mejorar el comando `stop` para que respete la opción `stanza`. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por ragaoua.*)

  `stop` con `force` y `stanza` ahora solo termina los procesos que mantienen bloqueos de esa stanza. Antes terminaba los de todas las stanzas.

  Incidencia [#1608](https://github.com/pgbackrest/pgbackrest/issues/1608); Solicitud de incorporación [#1676](https://github.com/pgbackrest/pgbackrest/pull/1676); Commit [`f7ab002`](https://github.com/pgbackrest/pgbackrest/commit/f7ab002aa74dd2ca277123f7500018ae68a04c74)
- Mejorar el mensaje de error para `repo-azure-key` inválido. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Seth Daniel.*)

  Con `repo-azure-key-type=shared`, ahora se comprueba que `repo-azure-key` sea base64 válido.

  Incidencia [#1686](https://github.com/pgbackrest/pgbackrest/issues/1686); Solicitud de incorporación [#1688](https://github.com/pgbackrest/pgbackrest/pull/1688); Commit [`7c9208b`](https://github.com/pgbackrest/pgbackrest/commit/7c9208ba856a71833dc7d8f1cf8cb2b4bb4b7414)
- Añadir una sugerencia para revisar el registro ante un error asincrónico de `archive-get`/`archive-push`. (*Revisado por Reid Thompson.*)

  Si el proceso asincrónico no puede escribir sus archivos de estado, `archive-get`/`archive-push` agotan el tiempo con un error genérico. Ahora se añade una indicación con la ruta del registro asincrónico, que contiene el error real.

  Incidencia [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`03c71aa`](https://github.com/pgbackrest/pgbackrest/commit/03c71aa606bc0dc89303b3907e7fcbd83ace79d6)
- Añadir `ClockError` para desfases de reloj y cambios de zona horaria inesperados. (*Revisado por Greg Sabino Mullane, Stefan Fercot. Sugerido por Greg Sabino Mullane.*)

  Solicitud de incorporación [#1739](https://github.com/pgbackrest/pgbackrest/pull/1739); Commit [`5f8c9cd`](https://github.com/pgbackrest/pgbackrest/commit/5f8c9cd66a1b39a47acaddfbc3cf443ae8057519)
- Quitar las extensiones del manifiesto de historial antes de mostrarlo en un mensaje de error. (*Revisado por Stefan Fercot.*)

  Si una etiqueta nueva no era posterior a la última del historial, el error mostraba el nombre del manifiesto histórico, por ejemplo `20220504-222042F_20220504-222141I.manifest.gz`. Ahora solo muestra la etiqueta.

  Solicitud de incorporación [#1738](https://github.com/pgbackrest/pgbackrest/pull/1738); Commit [`b6bfd9f`](https://github.com/pgbackrest/pgbackrest/commit/b6bfd9f99d74b1f5e631cf6462b68342589d2b80)
- Añadir usuario:grupo al error de permisos de bloqueo. (*Revisado por Reid Thompson.*)

  Incidencia [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); Commit [`0055fa4`](https://github.com/pgbackrest/pgbackrest/commit/0055fa40fee2636fed88699f52e9e67cd2803f71)
- Añadir una indicación cuando no se encuentra el clúster primario.

  El error "unable to find primary cluster" ahora incluye una indicación para comprobar si todos los clústeres disponibles están en recuperación.

  Commit [`46b7b72`](https://github.com/pgbackrest/pgbackrest/commit/46b7b7287446d0bb5ed0963fd01c51fb2b08893f)

**Correcciones de errores en la documentación:**

- Corregir una referencia incorrecta a `stanza-update` en la guía de usuario. (*Corregido por Abubakar Mohammed. Revisado por David Steele.*)

  Commit [`3dd7960`](https://github.com/pgbackrest/pgbackrest/commit/3dd796045160c4d4dbf70ec2800ad483867629f1)
- Corregir el ejemplo de la opción `repo-gcs-key-type` en la referencia de configuración. (*Revisado por Reid Thompson.*)

  El ejemplo era `none`, que no es válido. Ahora es `auto`.

  Commit [`166039c`](https://github.com/pgbackrest/pgbackrest/commit/166039c0da1875581a08d41ab8a44adf95fa6db1)
- Corregir el ejemplo de `tls-server-auth` y añadir aclaraciones. (*Revisado por Reid Thompson.*)

  Faltaba el CN del cliente en el ejemplo, que ahora es `client-cn=stanza1`. La ayuda también indica que el CN del cliente no admite comodines.

  Commit [`c222ce1`](https://github.com/pgbackrest/pgbackrest/commit/c222ce1a5f6f813188b7e87a3838d6dce656e0ff)

**Mejoras en la documentación:**

- Simplificar los mensajes sobre las versiones soportadas en la documentación. (*Revisado por Stefan Fercot, Reid Thompson, Greg Sabino Mullane.*)

  Las guías indicaban rangos de versiones de PostgreSQL que daban a entender que otras no se admitían, como PostgreSQL 12 en RHEL. Se eliminaron los rangos y la introducción ahora explica qué versiones cubren las guías.

  Solicitud de incorporación [#1742](https://github.com/pgbackrest/pgbackrest/pull/1742); Commit [`eefa0b1`](https://github.com/pgbackrest/pgbackrest/commit/eefa0b161a6a02b7843e18455443a4bce41cd4b9)
- Añadir descripciones de tipo de opción. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  La referencia de configuración ahora describe cada tipo de opción, como las unidades de tamaño, en lugar de repetirlo para cada opción.

  Solicitud de incorporación [#1747](https://github.com/pgbackrest/pgbackrest/pull/1747); Commit [`a913113`](https://github.com/pgbackrest/pgbackrest/commit/a913113fda5886ffd2ff136cdd52a3f469eca026)
- Añadir una pregunta frecuente sobre los tipos de copia de seguridad y la velocidad de restauración. (*Contribución de David Christensen. Revisado por Reid Thompson.*)

  Una nueva pregunta frecuente explica que el tipo de copia solo afecta a la copia y no a la velocidad de restauración.

  Solicitud de incorporación [#1731](https://github.com/pgbackrest/pgbackrest/pull/1731); Commit [`50d409a`](https://github.com/pgbackrest/pgbackrest/commit/50d409a812be577f2c296f3d6096cf97fab049ff)
- Documentar la rama base requerida para los pull requests. (*Contribución de David Christensen. Revisado por Reid Thompson.*)

  La guía de contribución ahora indica que las solicitudes de incorporación deben basarse en la rama `integration`.

  Solicitud de incorporación [#1733](https://github.com/pgbackrest/pgbackrest/pull/1733); Commit [`cc5b061`](https://github.com/pgbackrest/pgbackrest/commit/cc5b0614894e1b5ef78f1ceba3bc8e4760a40a24)

### Notas de la versión v2.38 {#v238-release-notes}

*Correcciones y mejoras menores*

*Publicada el 6 de marzo de 2022*

**NOTA IMPORTANTE**: El tamaño del repositorio reportado por el comando `info` ahora se basa enteramente en lo que pgBackRest ha escrito en el almacenamiento. Anteriormente, en ciertos casos, pgBackRest podía detectar si el almacenamiento aplicaba compresión adicional, pero esto ya no está soportado.

**Correcciones de errores:**

- Reintentar errores en la eliminación por lotes de archivos en S3. (*Revisado por Reid Thompson. Reportado por Alex Richman.*)

  Se reintentaban los fallos de una eliminación por lotes, pero no los errores de archivos individuales, y pgBackRest podía terminar durante la caducidad o al eliminar una copia no reanudable. Ahora los archivos que fallan se eliminan individualmente con los reintentos HTTP habituales.

  Incidencia [#1650](https://github.com/pgbackrest/pgbackrest/issues/1650); Solicitud de incorporación [#1653](https://github.com/pgbackrest/pgbackrest/pull/1653); Commit [`551e5bc`](https://github.com/pgbackrest/pgbackrest/commit/551e5bc6f67c91cf1e11da0cefe24f9650353adc)
- Permitir la coincidencia sin distinción entre mayúsculas y minúsculas de los valores del encabezado HTTP `connection`. (*Revisado por Reid Thompson. Reportado por Rémi Vidier.*)

  La especificación HTTP permite cualquier combinación de mayúsculas y minúsculas en los valores de `connection`, por ejemplo `Close`.

  Incidencia [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Solicitud de incorporación [#1675](https://github.com/pgbackrest/pgbackrest/pull/1675); Commit [`b33cabe`](https://github.com/pgbackrest/pgbackrest/commit/b33cabe08c33e29eb8aef65dd46b2c1f3cf2d186)

**Funcionalidades:**

- Añadir soporte para el cifrado del lado del servidor de AWS S3 con KMS. (*Contribución de Christoph Berg. Revisado por David Steele. Probado por Tharindu Amila.*)

  Establece `repo-s3-kms-key-id` para cifrar objetos con una clave administrada por AWS KMS.

  Incidencia [#1430](https://github.com/pgbackrest/pgbackrest/issues/1430); Solicitud de incorporación [#1567](https://github.com/pgbackrest/pgbackrest/pull/1567); Commit [`3097acd`](https://github.com/pgbackrest/pgbackrest/commit/3097acd73a21b630aa5352be57a82b031930f96b)
- Añadir la opción `archive-missing-retry`. (*Revisado por Stefan Fercot.*)

  Por defecto, `archive-get` reintenta un segmento WAL ya notificado como ausente, ignorando así avisos de ausencia dejados en el spool por una restauración anterior. Con `archive-missing-retry=n`, PostgreSQL puede detectar el final del archivo y pasar a streaming aunque se siga archivando WAL. En ese caso, el spool debe estar vacío al comenzar la recuperación.

  Solicitud de incorporación [#1642](https://github.com/pgbackrest/pgbackrest/pull/1642); Commit [`10038db`](https://github.com/pgbackrest/pgbackrest/commit/10038db9c9f2b4753c3821e0b246fa8626527184)
- Añadir un filtro por tipo de copia de seguridad al comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Establece `type` para mostrar solo copias de ese tipo, por ejemplo `type=full`.

  Incidencia [#600](https://github.com/pgbackrest/pgbackrest/issues/600); Solicitud de incorporación [#1651](https://github.com/pgbackrest/pgbackrest/pull/1651); Commit [`b26097f`](https://github.com/pgbackrest/pgbackrest/commit/b26097f8d8a7e2af6e9a21576994cbb47110c6f4)

**Mejoras:**

- Reintentar ante un fallo de validación de páginas durante `backup`. (*Revisado por Stephen Frost, David Christensen.*)

  Ahora se vuelve a leer una página que falla la suma de verificación y solo se informa de error si no ha cambiado. Una página modificada está siendo escrita por PostgreSQL y el WAL contiene una imagen completa de ella. Ahora se comprueba que las páginas cero contengan únicamente ceros, en lugar de comprobar solo el campo `pd_upper`.

  [`b489707`](https://github.com/pgbackrest/pgbackrest/commit/b4897077937ee4571ba719276a44d5db0a75510e) Mover las pruebas command/backup-common al módulo command/backup.

  [`9eec98c`](https://github.com/pgbackrest/pgbackrest/commit/9eec98c61302121134d2067326dbd2cd0f2f0b9c) Reintentar al fallar la validación de sumas de páginas durante la copia.; Incidencia [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Solicitud de incorporación [#1667](https://github.com/pgbackrest/pgbackrest/pull/1667)

  [`53f1b25`](https://github.com/pgbackrest/pgbackrest/commit/53f1b2520434221c01caf92e052403a28c455c1b) Mejorar la validación de páginas cero.; Incidencia [#952](https://github.com/pgbackrest/pgbackrest/issues/952); Solicitud de incorporación [#1669](https://github.com/pgbackrest/pgbackrest/pull/1669)
- Manejar servidores TLS que no cierran las conexiones de forma limpia. (*Revisado por David Christensen, Stephen Frost. Probado por Rémi Vidier.*)

  Algunos servidores cierran el socket en lugar de la conexión TLS. Si una respuesta no tiene longitud de contenido ni codificación por fragmentos y se puede analizar su contenido, ahora se trata el cierre como EOF. Esos servidores dejaron de funcionar en v2.35.

  Incidencia [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); Solicitud de incorporación [#1677](https://github.com/pgbackrest/pgbackrest/pull/1677); Commit [`59a5373`](https://github.com/pgbackrest/pgbackrest/commit/59a5373cf85e4ad0057b592bfe855495384dfcbd)
- Añadir los LSN de la copia de seguridad a la salida del comando `info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Los LSN de inicio y fin de una copia se muestran con `set` y en JSON para su uso en recuperaciones a un punto en el tiempo basadas en LSN.

  Solicitud de incorporación [#1610](https://github.com/pgbackrest/pgbackrest/pull/1610); Commit [`d866dd5`](https://github.com/pgbackrest/pgbackrest/commit/d866dd5c297dc046581134a108032cf9694cae0e)
- Quitar automáticamente las barras finales de las rutas de `repo-ls`. (*Contribución de David Christensen. Revisado por David Steele.*)

  Una barra final en la ruta hacía que `repo-ls` no mostrara contenido con algunos tipos de almacenamiento de repositorio.

  Solicitud de incorporación [#1673](https://github.com/pgbackrest/pgbackrest/pull/1673); Commit [`6320712`](https://github.com/pgbackrest/pgbackrest/commit/632071232344a1160ef932d6e0d65eb3149ed226)
- No reintentar errores fatales. (*Revisado por Reid Thompson.*)

  Reintentar errores fatales, especialmente de memoria insuficiente, puede causar bloqueos. Ahora los errores de aserción y memoria se notifican sin reintentarlos.

  [`8573a2d`](https://github.com/pgbackrest/pgbackrest/commit/8573a2df14d0bfd5578333b68147cc12c93c6f96) Mejorar la prueba de errores del módulo de protocolo para protocolClientFree().

  [`8d0cce6`](https://github.com/pgbackrest/pgbackrest/commit/8d0cce66f83abc1ff02a985ec3f0d7e285c09d72) Usar un error normal en la prueba de reintento de errores del protocolo.

  [`8046f06`](https://github.com/pgbackrest/pgbackrest/commit/8046f0630715015d5adcced570c54e9a183c0e73) No reintentar errores fatales.; Solicitud de incorporación [#1658](https://github.com/pgbackrest/pgbackrest/pull/1658)
- Eliminar el soporte de PostgreSQL `8.3`/`8.4`. (*Revisado por Reid Thompson, Stefan Fercot.*)

  No hay indicios de que estas versiones sigan usándose y mantenerlas consume tiempo de desarrollo y pruebas. Utiliza una versión anterior de pgBackRest para copiarlas o migrar desde ellas.

  Solicitud de incorporación [#1611](https://github.com/pgbackrest/pgbackrest/pull/1611); Commit [`bb4b30d`](https://github.com/pgbackrest/pgbackrest/commit/bb4b30ddd3f80c246c565eb4769efc82b9509648)
- Eliminar la lógica que intentaba determinar compresión adicional del sistema de archivos. (*Revisado por Reid Thompson, Stefan Fercot.*)

  Después de copiar un archivo se comprobaba su tamaño en disco para detectar compresión del sistema de archivos, como ZFS. No estaba probado, era lento con muchos archivos pequeños e impedía la agrupación. Ahora el tamaño del repositorio en `info` es lo que escribió pgBackRest.

  Solicitud de incorporación [#1652](https://github.com/pgbackrest/pgbackrest/pull/1652); Commit [`cb630ff`](https://github.com/pgbackrest/pgbackrest/commit/cb630ffe3b5c819b5e97ac11d5974000bd44d632)

**Correcciones de errores en la documentación:**

- Mover las opciones `repo` de la documentación de TLS a la sección `global`. (*Reportado por Anton Kurochkin.*)

  La guía establecía estas opciones en la sección de stanza, lo que funciona en algunos casos pero no es la práctica recomendada.

  Commit [`53de3e3`](https://github.com/pgbackrest/pgbackrest/commit/53de3e3aeb71f8209f56167941df35bbfcb7cdc9)
- Eliminar la opción `backup-standby` sin uso de los comandos de stanza. (*Reportado por Stefan Fercot.*)

  `stanza-create` y `stanza-upgrade` enumeraban `backup-standby` en la referencia y la ayuda, pero no lo utilizaban.

  Commit [`5cbb4a3`](https://github.com/pgbackrest/pgbackrest/commit/5cbb4a3e6b13598b90cae46fad28c31604f9f094)
- Corregir erratas en la ayuda y las notas de versión. (*Corregido por Daniel Gustafsson. Revisado por David Steele.*)

  [`cacfdd9`](https://github.com/pgbackrest/pgbackrest/commit/cacfdd94d74307285b1b590ec0977d7db3142d0d) Corregir erratas en la ayuda y las notas de versión.; Solicitud de incorporación [#1671](https://github.com/pgbackrest/pgbackrest/pull/1671)

  [`5c332a0`](https://github.com/pgbackrest/pgbackrest/commit/5c332a0b100d5a5180b3d95bd90d4d7b521b42db) Corregir la atribución de las notas de versión de cacfdd94 y f798458e.

**Mejoras en la documentación:**

- Añadir una comprobación de vitalidad a la configuración del servicio systemd. (*Sugerido por Yogesh Sharma.*)

  El ejemplo de `pgbackrest.service` ahora comprueba poco después del inicio que el servidor sigue activo. Antes no se informaba del error al fallar el arranque mientras systemd reintentaba en segundo plano.

  Commit [`f1bdf3e`](https://github.com/pgbackrest/pgbackrest/commit/f1bdf3e04b07dc9a2eaa1fdbe5278cc18371e868)
- Añadir una pregunta frecuente que explica el sufijo del archivado de WAL. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  El sufijo de un archivo WAL en el repositorio es su suma SHA1, utilizada para verificarlo. No se puede omitir.

  Incidencia [#1485](https://github.com/pgbackrest/pgbackrest/issues/1485); Incidencia [#1663](https://github.com/pgbackrest/pgbackrest/issues/1663); Solicitud de incorporación [#1664](https://github.com/pgbackrest/pgbackrest/pull/1664); Commit [`98d525d`](https://github.com/pgbackrest/pgbackrest/commit/98d525dba43ba259ff7989746b8e5be3382c189d)
- Señalar que los slots de replicación no se restauran. (*Contribución de Reid Thompson. Revisado por David Steele, Stefan Fercot. Sugerido por Christophe Courtois.*)

  Incidencia [#1585](https://github.com/pgbackrest/pgbackrest/issues/1585); Solicitud de incorporación [#1601](https://github.com/pgbackrest/pgbackrest/pull/1601); Commit [`a82f017`](https://github.com/pgbackrest/pgbackrest/commit/a82f0179cdd5742e5c5b1e0bdfd23166753fdb38)

### Notas de la versión v2.37 {#v237-release-notes}

*Servidor TLS*

*Publicada el 3 de enero de 2022*

**NOTA IMPORTANTE**: Si el comando `restore` no puede encontrar una copia de seguridad que coincida con un tiempo objetivo especificado, se lanzará un error, mientras que antes se registraba una advertencia.

**Correcciones de errores:**

- Corregir el mapeo de enlaces delta de `restore` cuando la ruta/el archivo ya existe. (*Revisado por Reid Thompson. Reportado por Younes Alhroub.*)

  Si `link-map` o `link-all` asignaban un enlace a una ruta o archivo existente, la restauración delta lo dejaba en su lugar. Ahora se sustituye por el enlace.

  Incidencia [#1588](https://github.com/pgbackrest/pgbackrest/issues/1588); Solicitud de incorporación [#1589](https://github.com/pgbackrest/pgbackrest/pull/1589); Commit [`a73fe4e`](https://github.com/pgbackrest/pgbackrest/commit/a73fe4eb966f9685f6e4179c397a10c1e7f15f19)
- Corregir una fuga de sockets en los reintentos de conexión. (*Revisado por Reid Thompson. Reportado por James Coleman.*)

  En compilaciones optimizadas no se cerraba el socket de un intento de conexión fallido, por lo que cada reintento filtraba un socket.

  Incidencia [#1593](https://github.com/pgbackrest/pgbackrest/issues/1593); Solicitud de incorporación [#1594](https://github.com/pgbackrest/pgbackrest/pull/1594); Commit [`615bdff`](https://github.com/pgbackrest/pgbackrest/commit/615bdff4030a31bfedfe7df04676e3948ec9c2c0)

**Funcionalidades:**

- Añadir un servidor TLS. (*Revisado por Stephen Frost, Reid Thompson. Probado por Andrew L'Ecuyer.*)

  El comando `server` inicia un servidor TLS que puede sustituir a SSH para acceder a hosts de repositorio y PostgreSQL. Configura `repo-host-type=tls` o `pg-host-type=tls` en el cliente y usa `tls-server-*` para los certificados y la autorización. `SIGHUP` recarga la configuración y `SIGTERM` detiene el servidor.

  [`2d963ce`](https://github.com/pgbackrest/pgbackrest/commit/2d963ce9471808172f879916c3f3accc35f14d56) Renombrar el comando server-start como server.

  [`7b3ea88`](https://github.com/pgbackrest/pgbackrest/commit/7b3ea883c7c010aafbeb14d150d073a113b703e4) Añadir el manejo de SIGTERM y SIGHUP al servidor TLS.; Solicitud de incorporación [#1572](https://github.com/pgbackrest/pgbackrest/pull/1572)

  [`f06101d`](https://github.com/pgbackrest/pgbackrest/commit/f06101de77a980c7e4115762f2fc301280aa4127) Añadir documentación del servidor TLS.; Solicitud de incorporación [#1597](https://github.com/pgbackrest/pgbackrest/pull/1597)

  Desarrollo en [v2.36](#v236-release-notes):

  [`ccc255d`](https://github.com/pgbackrest/pgbackrest/commit/ccc255d3e05d8ce2b6ac251d1498f71b04098a86) Añadir un servidor TLS.; Solicitud de incorporación [#1504](https://github.com/pgbackrest/pgbackrest/pull/1504)

  [`13d4559`](https://github.com/pgbackrest/pgbackrest/commit/13d4559708819787ad05be6f37ec0badb0eccae5) Comprobar el valor de retorno de getsockopt().

  Desarrollo en [v2.35](#v235-release-notes):

  [`947c7a8`](https://github.com/pgbackrest/pgbackrest/commit/947c7a84cb37d09ab925785ca7670c970e32b8a3) Refactorizar cmdLocal()/cmdRemote() para aceptar un objeto ProtocolServer.

  [`0999de0`](https://github.com/pgbackrest/pgbackrest/commit/0999de0279fabf35af80396a9a8d35546ec02d53) Mover noop de protocolClientNew() a la inicialización local/remote.
- Añadir la opción `--cmd`. (*Contribución de Reid Thompson. Revisado por Stefan Fercot, David Steele. Sugerido por Virgile CREVON.*)

  Establece `cmd` con el ejecutable pgBackRest que debe usarse en los comandos que escribe, como `restore_command` en `recovery.conf`.

  Incidencia [#1537](https://github.com/pgbackrest/pgbackrest/issues/1537); Solicitud de incorporación [#1540](https://github.com/pgbackrest/pgbackrest/pull/1540); Commit [`2a57647`](https://github.com/pgbackrest/pgbackrest/commit/2a576477b316238473525e56bc8fc8ea5790455f)

**Mejoras:**

- Comprobar el archivado inmediatamente después de iniciar la copia de seguridad. (*Revisado por Reid Thompson, David Christensen.*)

  Una copia solo fallaba por falta de archivado WAL después de copiar todos los archivos. Ahora se comprueba el archivo justo al iniciar. En sistemas inactivos se crea un punto de restauración para cambiar de segmento WAL.

  Incidencia [#152](https://github.com/pgbackrest/pgbackrest/issues/152); Solicitud de incorporación [#1570](https://github.com/pgbackrest/pgbackrest/pull/1570); Commit [`1f14f45`](https://github.com/pgbackrest/pgbackrest/commit/1f14f45dfb0d1677a695719381cbd5a8a3c6c986)
- Añadir comprobaciones de línea de tiempo y de checkpoint a la copia de seguridad. (*Revisado por Stefan Fercot, Reid Thompson.*)

  La copia ahora comprueba que `pg_control` contiene el punto de control y la línea temporal del inicio, y que el servidor en espera sigue al primario: está en la misma línea temporal y su punto de control no es posterior al de la copia.

  Solicitud de incorporación [#1581](https://github.com/pgbackrest/pgbackrest/pull/1581); Commit [`49145d7`](https://github.com/pgbackrest/pgbackrest/commit/49145d72bac16498cdbf5eeb3cd6128ea0be0667)
- Comprobar que los clústeres están vivos y correctamente configurados durante una copia de seguridad. (*Revisado por Stefan Fercot.*)

  Ahora una copia falla en cuanto se detiene un clúster o se promueve el servidor en espera. Antes solo se detectaba el primario detenido al final y no se detectaba la promoción del servidor en espera.

  Solicitud de incorporación [#1584](https://github.com/pgbackrest/pgbackrest/pull/1584); Commit [`bd2ba80`](https://github.com/pgbackrest/pgbackrest/commit/bd2ba802db11c505ec69943fa81b2b379073fbf4)
- Generar un error cuando `restore` no puede encontrar una copia de seguridad que coincida con el tiempo objetivo. (*Revisado por Reid Thompson, Douglas J Hunley. Sugerido por Douglas J Hunley.*)

  Antes era una advertencia fácil de pasar por alto, y podía perderse mucho tiempo restaurando una copia incapaz de alcanzar el objetivo.

  Incidencia [#1582](https://github.com/pgbackrest/pgbackrest/issues/1582); Solicitud de incorporación [#1586](https://github.com/pgbackrest/pgbackrest/pull/1586); Commit [`be4ac39`](https://github.com/pgbackrest/pgbackrest/commit/be4ac3923cb77873da298a30aca5d847b3c635af)
- Analizar protocolo/puerto en los endpoints de S3/Azure. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  `repo-s3-endpoint`, `repo-azure-endpoint` y `repo-storage-host` ahora pueden incluir protocolo y puerto, por ejemplo `https://host:9000`.

  Incidencia [#1560](https://github.com/pgbackrest/pgbackrest/issues/1560); Solicitud de incorporación [#1591](https://github.com/pgbackrest/pgbackrest/pull/1591); Commit [`6a12458`](https://github.com/pgbackrest/pgbackrest/commit/6a12458440168f13cb05d70f36ea54b1860e390c)
- Añadir una advertencia cuando `checkpoint_timeout` excede `db-timeout`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Con `start-fast=n`, una copia puede agotar el tiempo esperando el punto de control si `checkpoint_timeout` supera `db-timeout`. Ahora se advierte en ese caso.

  Solicitud de incorporación [#1564](https://github.com/pgbackrest/pgbackrest/pull/1564); Commit [`6723305`](https://github.com/pgbackrest/pgbackrest/commit/672330593789f07aaad90bbafcd2597cbc602686)
- Añadir el verbo a la salida de errores HTTP. (*Contribución de Christoph Berg. Revisado por David Steele.*)

  Solicitud de incorporación [#1566](https://github.com/pgbackrest/pgbackrest/pull/1566); Commit [`c38e2d3`](https://github.com/pgbackrest/pgbackrest/commit/c38e2d31709804eb4b9125a15ad84c8fc813f366)
- Permitir argumentos y/n para opciones booleanas de línea de comandos. (*Contribución de Reid Thompson. Revisado por David Steele.*)

  Solicitud de incorporación [#1571](https://github.com/pgbackrest/pgbackrest/pull/1571); Commit [`1a0560d`](https://github.com/pgbackrest/pgbackrest/commit/1a0560d363d28737befb8c222647783d4fc2ca29)
- Hacer que el registro del tamaño de la copia de seguridad coincida exactamente con la salida del comando `info`. (*Contribución de Reid Thompson. Revisado por David Steele. Sugerido por Mahomed Hussein.*)

  El tamaño registrado de la copia ahora solo incluye los archivos copiados, más `backup_label` y `tablespace_map`. Antes, por ejemplo tras un cambio de primario, una copia incremental registraba el tamaño de todos los archivos comprobados.

  [`6e63576`](https://github.com/pgbackrest/pgbackrest/commit/6e635764a66278d5a8c2b4d30b23063bc3923067) Hacer coincidir el tamaño de la copia registrado en el log con el informado por info.; Incidencia [#766](https://github.com/pgbackrest/pgbackrest/issues/766); Solicitud de incorporación [#1562](https://github.com/pgbackrest/pgbackrest/pull/1562)

  [`afe77e7`](https://github.com/pgbackrest/pgbackrest/commit/afe77e76e0adf948138d797e227a6f4c7d47c2eb) Actualizar el colaborador de 6e635764.

  [`1e77fc3`](https://github.com/pgbackrest/pgbackrest/commit/1e77fc3d75490b7a1b6a0b31be9298c995ec672f) Incluir los tamaños de backup_label y tablespace_map en el registro.; Solicitud de incorporación [#1568](https://github.com/pgbackrest/pgbackrest/pull/1568)

  [`a3d7a23`](https://github.com/pgbackrest/pgbackrest/commit/a3d7a23a9d90611a3d31947598fbea240b250710) Usar infoBackupDataByLabel() para registrar el tamaño de la copia.; Solicitud de incorporación [#1573](https://github.com/pgbackrest/pgbackrest/pull/1573)

  [`dcb4f09`](https://github.com/pgbackrest/pgbackrest/commit/dcb4f09d8315e92c0877b589f3fa9b7f0fa65f93) Revertir los cambios en backupFilePut() de 1e77fc3d.

**Mejoras en la documentación:**

- Mostrar los valores por defecto y permitidos de las opciones de tamaño con las unidades apropiadas. (*Revisado por Reid Thompson.*)

  [`cff961e`](https://github.com/pgbackrest/pgbackrest/commit/cff961ede7e41fa8035ffe7451a22eb5ea0e46c1) Centralizar la construcción de listas de valores al renderizar la configuración.

  [`038abaa`](https://github.com/pgbackrest/pgbackrest/commit/038abaa71d816cc87b382bd81d3df62ddec9455a) Mostrar los valores por defecto y permitidos de las opciones de tamaño con las unidades apropiadas.; Solicitud de incorporación [#1557](https://github.com/pgbackrest/pgbackrest/pull/1557)
- Corregir erratas y mejorar la documentación de la opción `tablespace-map-all`. (*Revisado por Reid Thompson. Sugerido por Reid Thompson.*)

  Commit [`df89eff`](https://github.com/pgbackrest/pgbackrest/commit/df89eff429e9b8fbc68d9e9895badf9719fd31d2)
- Eliminar una afirmación obsoleta sobre el futuro soporte de múltiples repositorios. (*Sugerido por David Christensen.*)

  La documentación decía que solo se permitía un repositorio, pero se admiten varios desde v2.33.

  Commit [`dea7524`](https://github.com/pgbackrest/pgbackrest/commit/dea752477ab8e812cdbd717eb2091baf3f5d0906)

### Notas de la versión v2.36 {#v236-release-notes}

*Correcciones y mejoras menores*

*Publicada el 1 de noviembre de 2021*

**Correcciones de errores:**

- Permitir «global» como prefijo de stanza. (*Revisado por Stefan Fercot. Reportado por Younes Alhroub.*)

  Se rechazaban los nombres de stanza que comenzaban por `global`, como `global_stanza`, porque el analizador los trataba como una sección global.

  Incidencia [#1524](https://github.com/pgbackrest/pgbackrest/issues/1524); Solicitud de incorporación [#1525](https://github.com/pgbackrest/pgbackrest/pull/1525); Commit [`498902e`](https://github.com/pgbackrest/pgbackrest/commit/498902e885c9d7a44648ccc01b20454094d5b742)
- Corregir un segfault con un archivo de clave GCS inválido. (*Revisado por Stephen Frost. Reportado por Henrik Feldt.*)

  Un archivo de clave GCS sin el correo del cliente, la clave privada o el URI del token provocaba un fallo de segmentación. Ahora genera un error.

  Incidencia [#1536](https://github.com/pgbackrest/pgbackrest/issues/1536); Commit [`2cea005`](https://github.com/pgbackrest/pgbackrest/commit/2cea005f740d640290a9948595f5933833e30e7d)

**Mejoras:**

- Permitir que la opción `link-map` cree enlaces nuevos. (*Revisado por Don Seiler, Stefan Fercot, Chris Bandy. Sugerido por Don Seiler.*)

  `link-map` solo podía reasignar enlaces existentes en la copia. Ahora puede crear un enlace nuevo para cualquier ruta o archivo de ella.

  [`d89a677`](https://github.com/pgbackrest/pgbackrest/commit/d89a67776cfbb7b3047dbe297cc0c768e5c670e8) Refactorizar las pruebas de restoreManifestMap() en command/restore.

  [`cf1a575`](https://github.com/pgbackrest/pgbackrest/commit/cf1a57518fe3230886509f59fcec9c9a81e6513c) Refactorizar restoreManifestMap() para que se guíe por link-map.

  [`68c5f3e`](https://github.com/pgbackrest/pgbackrest/commit/68c5f3eaf18fc9bd10fde15a323890bcdcbf4534) Permitir que la opción `link-map` cree enlaces nuevos.; Incidencia [#1409](https://github.com/pgbackrest/pgbackrest/issues/1409); Solicitud de incorporación [#1520](https://github.com/pgbackrest/pgbackrest/pull/1520)
- Aumentar a 256 el índice máximo permitido para las opciones `pg`/`repo`. (*Revisado por Cynthia Shang.*)

  El índice máximo era 8 para las opciones `pg` y 4 para las `repo`. Ahora ambos son 256, por ejemplo `pg256-path`.

  [`02b06aa`](https://github.com/pgbackrest/pgbackrest/commit/02b06aa4957cf3fe64ceb7a44cc1893bff12fe99) Aumentar a 256 el índice máximo permitido para las opciones `pg`/`repo`.; Solicitud de incorporación [#1481](https://github.com/pgbackrest/pgbackrest/pull/1481)

  [`71047a9`](https://github.com/pgbackrest/pgbackrest/commit/71047a9d6d1eea71b3fbd430983541a54049cc69) Usar strncpy() para limitar los caracteres copiados a optionName.
- Añadir autenticación `WebIdentity` para AWS S3. (*Revisado por James Callahan, Reid Thompson, Andrew L'Ecuyer. Probado por Benjamin Blattberg.*)

  Establece `repo-s3-key-type=web-id` para obtener credenciales automáticamente en un entorno EKS.

  [`cfd8233`](https://github.com/pgbackrest/pgbackrest/commit/cfd823355af2ac99f30c5e1393a121c6dbf622b7) Refactorizar el controlador S3 para métodos de autenticación adicionales.

  [`3879bc6`](https://github.com/pgbackrest/pgbackrest/commit/3879bc69b888daa04d2ca98a2d1219cf22519ddc) Añadir autenticación `WebIdentity` para AWS S3.; Incidencia [#1203](https://github.com/pgbackrest/pgbackrest/issues/1203); Solicitud de incorporación [#1527](https://github.com/pgbackrest/pgbackrest/pull/1527)

  [`1152f7a`](https://github.com/pgbackrest/pgbackrest/commit/1152f7a7d64e69eed1d9e74b48a308f6c742c28a) Corregir parámetros discordantes en la llamada a tlsClientNew().
- Añadir la opción `repo-azure-uri-style`.

  Establece `repo-azure-uri-style` en `host` (predeterminado) o `path` para elegir el estilo de URI de Azure. Azurite usa URI de estilo host si el endpoint parece un nombre de host de varias partes.

  Commit [`096829b`](https://github.com/pgbackrest/pgbackrest/commit/096829b3b257444162417662612e80d8cb2ac6ec)
- Reportar los errores de validación de archivos de la copia de seguridad en `backup.info`. (*Contribución de Stefan Fercot. Revisado por David Steele.*)

  Los errores detectados al copiar, como sumas de páginas no válidas, solo se mostraban con `info` y `set`. Ahora un indicador en `backup.info` señala en texto y JSON que la copia contiene errores. Los detalles siguen requiriendo `set`.

  Incidencia [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); Solicitud de incorporación [#1508](https://github.com/pgbackrest/pgbackrest/pull/1508); Commit [`34f7873`](https://github.com/pgbackrest/pgbackrest/commit/34f78734325743b4e34cb39224852e6debf49750)
- Añadir la hora de inicio de la recuperación al registro de restauración de copias de seguridad en línea. (*Revisado por Tom Swartz, Stefan Fercot. Sugerido por Tom Swartz.*)

  La restauración ahora registra la hora desde la que comenzará la recuperación, indicando cuánto WAL deberá reproducirse.

  Incidencia [#1507](https://github.com/pgbackrest/pgbackrest/issues/1507); Solicitud de incorporación [#1518](https://github.com/pgbackrest/pgbackrest/pull/1518); Commit [`9e79f0e`](https://github.com/pgbackrest/pgbackrest/commit/9e79f0e64b661e944ce2b3897c366feea1544ac2)
- Reportar el error original y los reintentos ante un fallo de un trabajo local. (*Revisado por Stefan Fercot.*)

  Si un trabajo local falla tras reintentarlo, ahora se informa del primer error con su traza, seguido de los errores de reintento. Antes solo se notificaba el último, a menudo un fallo en cascada como la pérdida de sincronización del protocolo.

  [`136d309`](https://github.com/pgbackrest/pgbackrest/commit/136d309dd4bc1ada9f3d775f036b62292fda390b) Permitir especificar la traza de pila para errorInternalThrow().

  [`ae40ed6`](https://github.com/pgbackrest/pgbackrest/commit/ae40ed6ec9cf77e577518b128518a5763767f589) Añadir el parámetro jobRetry a HRN_CFG_LOAD().

  [`6af827c`](https://github.com/pgbackrest/pgbackrest/commit/6af827cbb1e78cd4c5d649ed4cb24c49a7204b8f) Reportar el error original y los reintentos ante un fallo de un trabajo local.; Solicitud de incorporación [#1521](https://github.com/pgbackrest/pgbackrest/pull/1521)
- Renombrar «page checksum error» a «error list» en la salida de texto de info. (*Revisado por Stefan Fercot.*)

  La etiqueta de texto de `info` pasa de "page checksum error" a "error list", ya que un archivo puede tener un error de alineación en vez de suma de página.

  Solicitud de incorporación [#1519](https://github.com/pgbackrest/pgbackrest/pull/1519); Commit [`9346895`](https://github.com/pgbackrest/pgbackrest/commit/9346895f5b61627b50d431f09447e08d8a50caa8)
- Añadir sugerencias al mensaje de tiempo de espera agotado de la reproducción de la réplica. (*Revisado por Cynthia Shang, Stefan Fercot. Sugerido por Leigh Downs.*)

  El tiempo de espera agotado al esperar la reproducción del servidor en espera ahora sugiere comprobar la replicación y desactivar `backup-standby` para copiar desde el primario.

  Incidencia [#1434](https://github.com/pgbackrest/pgbackrest/issues/1434); Commit [`b7ef12a`](https://github.com/pgbackrest/pgbackrest/commit/b7ef12a76f219881d0b24c715592af96fe5c9b8f)

**Correcciones de errores en la documentación:**

- Corregir un nombre de host erróneo en la guía. (*Corregido por Reid Thompson. Revisado por David Steele.*)

  La configuración de replicación usaba en `pg_hba.conf` la IP de pg-primary en lugar de la de pg-standby.

  Solicitud de incorporación [#1544](https://github.com/pgbackrest/pgbackrest/pull/1544); Commit [`1cb8ae1`](https://github.com/pgbackrest/pgbackrest/commit/1cb8ae15de5b4276682bdd9825ca97012cd43855)

**Mejoras en la documentación:**

- Mejorar la documentación de opciones.

  La ayuda de `buffer-size` ahora describe todas las operaciones que lo usan; las descripciones de `cmd-ssh`, `repo-host-cmd` y `pg-host-cmd` son coherentes, y `archive-header-check` pasa a la sección de archivado de la referencia.

  [`3763624`](https://github.com/pgbackrest/pgbackrest/commit/376362475e3b3b13b70313d9002d4ff8b25b4b40) Mover archive-header-check a la sección de referencia de archivado.

  [`e1f6c06`](https://github.com/pgbackrest/pgbackrest/commit/e1f6c066b3da11fd21b1155c90370c3fa2da06b7) Mejorar la documentación de buffer-size.

  [`fa564ee`](https://github.com/pgbackrest/pgbackrest/commit/fa564ee1969229b5cf60d2479d8ace85325f4db3) Mejorar la documentación de cmd-ssh, repo-host-cmd y pg-host-cmd.

### Notas de la versión v2.35 {#v235-release-notes}

*Protocolo binario*

*Publicada el 23 de agosto de 2021*

**NOTA IMPORTANTE**: El nivel de registro para los archivos copiados en los comandos `backup`/`restore` se ha cambiado a `detail`. Esto hace que el nivel de registro `info` sea menos ruidoso, pero si estos mensajes son necesarios, establece el nivel de registro de los comandos `backup`/`restore` en `detail`

**Correcciones de errores:**

- Detectar errores en la finalización de subidas multiparte de S3. (*Revisado por Cynthia Shang. Probado por Marco Montagna. Reportado por Marco Montagna, Lev Kokotov, Anderson A. Mallmann.*)

  La finalización de una carga multiparte puede fallar aunque S3 devuelva éxito HTTP. Ahora una respuesta sin `ETag` se considera un fallo y se reintenta el trabajo.

  [`8e1807c`](https://github.com/pgbackrest/pgbackrest/commit/8e1807cdbe08a6e059ff79220247cf4b3c058979) Detectar errores en la finalización de subidas multiparte de S3.; Incidencia [#1116](https://github.com/pgbackrest/pgbackrest/issues/1116); Incidencia [#1290](https://github.com/pgbackrest/pgbackrest/issues/1290); Incidencia [#1433](https://github.com/pgbackrest/pgbackrest/issues/1433); Solicitud de incorporación [#1438](https://github.com/pgbackrest/pgbackrest/pull/1438)

  [`25508a4`](https://github.com/pgbackrest/pgbackrest/commit/25508a48e0d3b0a3eabc6d1fe858b9c3dc12dc86) Añadir colaboradores omitidos en 8e187cdb.
- Corregir la detección de enlaces simbólicos circulares. (*Revisado por Stefan Fercot. Reportado por Rohit Raveendran.*)

  Se seguían los enlaces antes de comprobarlos, y un enlace circular provocaba recursión infinita y un fallo al crear el manifiesto.

  Incidencia [#1447](https://github.com/pgbackrest/pgbackrest/issues/1447); Solicitud de incorporación [#1452](https://github.com/pgbackrest/pgbackrest/pull/1452); Commit [`43b8746`](https://github.com/pgbackrest/pgbackrest/commit/43b874628c86ec4fe297dbd5cab5bd3f62b8639b)
- Pasar al remoto solo las opciones `repo` seleccionadas. (*Revisado por David Christensen, Cynthia Shang. Reportado por Greg Sabino Mullane, David Christensen.*)

  Las opciones de otros repositorios podían causar conflictos en el remoto, que utiliza exactamente un repositorio.

  Solicitud de incorporación [#1480](https://github.com/pgbackrest/pgbackrest/pull/1480); Commit [`935de1e`](https://github.com/pgbackrest/pgbackrest/commit/935de1e7a06d60415c16cad137875b49346337c6)

**Mejoras:**

- Protocolo binario. (*Revisado por Cynthia Shang.*)

  Los procesos locales y remotos ahora se comunican mediante el formato binario pack en vez de JSON. Los packs son más compactos, rápidos de generar y analizar y tienen tipos estrictos. Cada mensaje se escribe en un solo lugar, reduciendo el riesgo de dejar el protocolo en mal estado tras un error, y no hay límite de tamaño.

  [`6a1c033`](https://github.com/pgbackrest/pgbackrest/commit/6a1c0337ddee9900dda58b7d2fa74d82c0586ed2) Protocolo binario.; Solicitud de incorporación [#1424](https://github.com/pgbackrest/pgbackrest/pull/1424)

  [`2d5cbfc`](https://github.com/pgbackrest/pgbackrest/commit/2d5cbfc73142fa99df609aa23b64db5342e73c88) Corregir fugas de memoria introducidas por el protocolo binario en 6a1c0337.

  [`f716cb6`](https://github.com/pgbackrest/pgbackrest/commit/f716cb6f4f9765baa03f71b5563786d79d9f04a2) Corregir el uso de memoria liberada introducido por el protocolo binario en 6a1c0337.

  [`4fb6384`](https://github.com/pgbackrest/pgbackrest/commit/4fb6384f10f6cd26c422ab9b24feb5ae0ebeeee9) Corregir más fugas de memoria introducidas por el protocolo binario en 6a1c0337.
- Crear automáticamente el directorio de datos en `restore`. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Chris Bandy.*)

  Una comprobación migrada de Perl impedía crear el directorio de datos al restaurar.

  Incidencia [#1445](https://github.com/pgbackrest/pgbackrest/issues/1445); Solicitud de incorporación [#1454](https://github.com/pgbackrest/pgbackrest/pull/1454); Commit [`056a307`](https://github.com/pgbackrest/pgbackrest/commit/056a3070e0dba299389c7b5049878d40dd91ec9a)
- Permitir `restore` `--type=lsn`. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang. Sugerido por James Coleman.*)

  Establece `type=lsn` y un LSN en `target` para recuperar hasta ese LSN en PostgreSQL >= 10.

  Incidencia [#1339](https://github.com/pgbackrest/pgbackrest/issues/1339); Solicitud de incorporación [#1462](https://github.com/pgbackrest/pgbackrest/pull/1462); Commit [`563d117`](https://github.com/pgbackrest/pgbackrest/commit/563d117967ab9770f9f646c6186d0bc37121611f)
- Cambiar a detail el nivel de registro de archivos copiados de `backup`/`restore`. (*Revisado por Stefan Fercot. Sugerido por Jens Wilke.*)

  Esto reduce el ruido del nivel de registro `info`. Establece `detail` para ver cada archivo copiado.

  Incidencia [#1277](https://github.com/pgbackrest/pgbackrest/issues/1277); Solicitud de incorporación [#1455](https://github.com/pgbackrest/pgbackrest/pull/1455); Commit [`849ab34`](https://github.com/pgbackrest/pgbackrest/commit/849ab343aa10d66fbbd27cad407eff981c186d06)
- Iterar mientras se espera que el LSN del checkpoint alcance el LSN de reproducción. (*Contribución de Stefan Fercot. Revisado por David Steele. Sugerido por Fatih Mencutekin.*)

  En un servidor en espera, el LSN del punto de control puede ir ligeramente por detrás del de reproducción hasta actualizar `pg_control`. Ahora la copia sigue comprobándolo en lugar de fallar.

  Incidencia [#1450](https://github.com/pgbackrest/pgbackrest/issues/1450); Solicitud de incorporación [#1460](https://github.com/pgbackrest/pgbackrest/pull/1460); Commit [`8fac1ac`](https://github.com/pgbackrest/pgbackrest/commit/8fac1ac50d28557d162fbb251fbbdcc3c9fb950c)
- Registrar el total de archivos de `backup` y el total de tamaño/archivos de `restore`. (*Revisado por Cynthia Shang.*)

  Ahora el tamaño se registra al final de la copia e incluye archivos añadidos al manifiesto tras la copia principal, como `backup_label` y WAL. La restauración también registra su tamaño y total de archivos.

  Solicitud de incorporación [#1489](https://github.com/pgbackrest/pgbackrest/pull/1489); Commit [`a0bdfa4`](https://github.com/pgbackrest/pgbackrest/commit/a0bdfa436c9e1c2723be905ebe5cef7809a26244)

**Correcciones de errores en la documentación:**

- Corregir nombres de host incorrectos en la guía de usuario. (*Revisado por Stefan Fercot. Reportado por Greg Sabino Mullane.*)

  Algunos ejemplos mostraban `pg1` en vez del nombre del host, y el bloque de instalación instalaba paquetes en el host de compilación independientemente del host indicado.

  Solicitud de incorporación [#1479](https://github.com/pgbackrest/pgbackrest/pull/1479); Commit [`155ef85`](https://github.com/pgbackrest/pgbackrest/commit/155ef85013088a1150a4c15b04af36420d06e9c3)

**Mejoras en la documentación:**

- Actualizar la documentación de contribución y añadir una plantilla de pull request. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  La guía de contribución ahora incluye índice y secciones para interpretar las pruebas y enviar solicitudes de incorporación. GitHub muestra una plantilla para nuevas solicitudes.

  [`e3d05e2`](https://github.com/pgbackrest/pgbackrest/commit/e3d05e2b4aa80149219b6d49a3136b34fa268127) Actualizar la documentación de contribución y añadir una plantilla de pull request.; Solicitud de incorporación [#1469](https://github.com/pgbackrest/pgbackrest/pull/1469)

  [`71b654f`](https://github.com/pgbackrest/pgbackrest/commit/71b654fc29497319862fe01c3917bbc353cc6dd9) Corregir enlaces y actualizar el ejemplo de proceso hijo.; Solicitud de incorporación [#1487](https://github.com/pgbackrest/pgbackrest/pull/1487)
- Reordenar la documentación de copias de seguridad en la guía de usuario. (*Revisado por Cynthia Shang.*)

  Las secciones «Opción de inicio rápido» y «Tiempo de espera de archivado» pasan a «Inicio rápido - Realizar una copia». Se elimina «Opción de parada automática», aplicable solo a PostgreSQL <= 9.6.

  Solicitud de incorporación [#1488](https://github.com/pgbackrest/pgbackrest/pull/1488); Commit [`6ab18dc`](https://github.com/pgbackrest/pgbackrest/commit/6ab18dc0fa42885aea8eb9405ab0a943c2d49a71)
- Aclarar el comportamiento de `--type` de `restore` en la referencia de comandos. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  La referencia ahora indica que hay que especificar `set` si el objetivo es anterior a la última copia y `type` no es `time`.

  Commit [`a6691c6`](https://github.com/pgbackrest/pgbackrest/commit/a6691c6f615f90195aeb6c1c6657a6afd79a10d3)
- Corregir erratas en la documentación y los comentarios. (*Contribución de Eric Radman. Revisado por David Steele.*)

  Solicitud de incorporación [#1446](https://github.com/pgbackrest/pgbackrest/pull/1446); Commit [`23bdc3d`](https://github.com/pgbackrest/pgbackrest/commit/23bdc3deb62a622713064df3b0777110ebba8723)

**Mejoras en la suite de pruebas:**

- Añadir una comprobación de que la ruta de pruebas esté dentro de la ruta del repositorio. (*Revisado por Greg Sabino Mullane. Sugerido por Greg Sabino Mullane.*)

  Una ruta de pruebas dentro del repositorio causaba fallos extraños porque el repositorio se copia en ella. Ahora `test.pl` da error en ese caso.

  Incidencia [#1472](https://github.com/pgbackrest/pgbackrest/issues/1472); Solicitud de incorporación [#1474](https://github.com/pgbackrest/pgbackrest/pull/1474); Commit [`e32f9e1`](https://github.com/pgbackrest/pgbackrest/commit/e32f9e146b11389e3d16feba9665360b73737d66)
- Añadir análisis de código estático con CodeQL. (*Revisado por Cynthia Shang.*)

  CodeQL ahora se ejecuta en CI. Se corrigieron los problemas detectados; por ejemplo, `gmtime()`/`localtime()` se sustituyeron por `gmtime_r()`/`localtime_r()`.

  Solicitud de incorporación [#1457](https://github.com/pgbackrest/pgbackrest/pull/1457); Commit [`3c8819e`](https://github.com/pgbackrest/pgbackrest/commit/3c8819e10f9eff89195566e7e02f349373f5c4c7)
- Actualizar las pruebas para usar patrones estándar. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  [`3f9fbc3`](https://github.com/pgbackrest/pgbackrest/commit/3f9fbc3c24eab48e7ae2871484ea01273049e601) Adaptar la prueba command/expire a los patrones estándar.; Solicitud de incorporación [#1420](https://github.com/pgbackrest/pgbackrest/pull/1420)

  [`03021c6`](https://github.com/pgbackrest/pgbackrest/commit/03021c6a17f1374e84ef42614fa1dd2a6be4b64d) Adaptar la prueba command/stanza a los patrones estándar.; Solicitud de incorporación [#1426](https://github.com/pgbackrest/pgbackrest/pull/1426)

  [`8dd882b`](https://github.com/pgbackrest/pgbackrest/commit/8dd882badee76b038dc8b494a1112eb3e18ef678) Adaptar la prueba info/infoArchive a los patrones estándar.; Solicitud de incorporación [#1436](https://github.com/pgbackrest/pgbackrest/pull/1436)

  [`ff95edd`](https://github.com/pgbackrest/pgbackrest/commit/ff95eddc369597c76a9ea70ffbada493ed4d1951) Adaptar la prueba command/verify a los patrones estándar.; Solicitud de incorporación [#1435](https://github.com/pgbackrest/pgbackrest/pull/1435)

  [`17c9ed0`](https://github.com/pgbackrest/pgbackrest/commit/17c9ed0ef0380fb14fba9a5299b6618ca8c92c2e) Adaptar la prueba command/info a los patrones estándar.; Solicitud de incorporación [#1432](https://github.com/pgbackrest/pgbackrest/pull/1432)

  [`bffb43e`](https://github.com/pgbackrest/pgbackrest/commit/bffb43ea3fe00f445a2fc3c44a07f105cee65b4b) Adaptar la prueba command/check a los patrones estándar.; Solicitud de incorporación [#1431](https://github.com/pgbackrest/pgbackrest/pull/1431)

  [`fb2d111`](https://github.com/pgbackrest/pgbackrest/commit/fb2d111dcd75021313a64a348959482339bf7f2a) Adaptar la prueba info/infoBackup a los patrones estándar.; Solicitud de incorporación [#1437](https://github.com/pgbackrest/pgbackrest/pull/1437)

  [`065a8c8`](https://github.com/pgbackrest/pgbackrest/commit/065a8c8454d2acdd72c0c71a24d6b8bc09669e18) Sustituir defines por constantes de cadena en las pruebas unitarias.; Solicitud de incorporación [#1440](https://github.com/pgbackrest/pgbackrest/pull/1440)

  [`c620811`](https://github.com/pgbackrest/pgbackrest/commit/c6208113bfce9d637ca3fd0b35ab28a819c1a83e) Añadir el parámetro timeModified a la macro HRN_STORAGE_PUT().

  [`6a90d46`](https://github.com/pgbackrest/pgbackrest/commit/6a90d469094ee2697ae4c932349756a54136799d) Adaptar la prueba info/manifest a los patrones estándar.; Solicitud de incorporación [#1444](https://github.com/pgbackrest/pgbackrest/pull/1444)

  [`62e8d97`](https://github.com/pgbackrest/pgbackrest/commit/62e8d97af03e7628d5710b17aad1cc31f83d7e69) Adaptar las pruebas command/archive a los patrones estándar.; Solicitud de incorporación [#1449](https://github.com/pgbackrest/pgbackrest/pull/1449)

  [`8bb0b28`](https://github.com/pgbackrest/pgbackrest/commit/8bb0b28455d59ef884eab7ab25a91f988adbab81) Adaptar las pruebas command/control y command/command a los patrones estándar.; Solicitud de incorporación [#1456](https://github.com/pgbackrest/pgbackrest/pull/1456)

  [`f2ec4e0`](https://github.com/pgbackrest/pgbackrest/commit/f2ec4e00a4c4c388a8f1b094381fd566a3dc9aa7) Añadir parámetros de cifrado a la macro TEST_STORAGE_GET().

  [`4ad0bbd`](https://github.com/pgbackrest/pgbackrest/commit/4ad0bbda53b34688146f14d130cf0e53c8dd650f) Adaptar las pruebas command/backup a los patrones estándar.; Solicitud de incorporación [#1463](https://github.com/pgbackrest/pgbackrest/pull/1463)

  [`117ffe8`](https://github.com/pgbackrest/pgbackrest/commit/117ffe88965fd60ce3dcb328e9d28503870af05a) Adaptar las pruebas command/help a los patrones estándar.; Solicitud de incorporación [#1464](https://github.com/pgbackrest/pgbackrest/pull/1464)

  [`ebe5848`](https://github.com/pgbackrest/pgbackrest/commit/ebe5848494d4e37a9c86f1fafb5b3453c1f425a6) Adaptar las pruebas command/local y command/remote a los patrones estándar.; Solicitud de incorporación [#1466](https://github.com/pgbackrest/pgbackrest/pull/1466)

  [`a6cdf5b`](https://github.com/pgbackrest/pgbackrest/commit/a6cdf5b22f0eed53f33bbd84478af0542c81af7d) Adaptar la prueba command/repo a los patrones estándar.; Solicitud de incorporación [#1467](https://github.com/pgbackrest/pgbackrest/pull/1467)

  [`4992508`](https://github.com/pgbackrest/pgbackrest/commit/49925087644c76df005828eb27c24f503a09b20b) Adaptar la prueba command/restore a los patrones estándar.; Solicitud de incorporación [#1468](https://github.com/pgbackrest/pgbackrest/pull/1468)

  [`4c9ddf5`](https://github.com/pgbackrest/pgbackrest/commit/4c9ddf5ef25d0f441e20e918f57c1ec79218cfdb) Adaptar las pruebas storage a los patrones estándar.; Solicitud de incorporación [#1470](https://github.com/pgbackrest/pgbackrest/pull/1470)

  [`eeaab6a`](https://github.com/pgbackrest/pgbackrest/commit/eeaab6a3d192fc788c0f74aadbf4b3de5da52531) Adaptar las pruebas config, excepto parse, a los patrones estándar.; Solicitud de incorporación [#1473](https://github.com/pgbackrest/pgbackrest/pull/1473)

  [`f653b59`](https://github.com/pgbackrest/pgbackrest/commit/f653b59664e757a0e3da63cc8462deafe2d9e0ef) Adaptar la prueba db/db a los patrones estándar.; Solicitud de incorporación [#1486](https://github.com/pgbackrest/pgbackrest/pull/1486)

  [`e17865a`](https://github.com/pgbackrest/pgbackrest/commit/e17865a03a5451b82a101557d400ff223d104383) Adaptar la prueba protocol/protocol a los patrones estándar.; Solicitud de incorporación [#1491](https://github.com/pgbackrest/pgbackrest/pull/1491)

  [`eca2fc6`](https://github.com/pgbackrest/pgbackrest/commit/eca2fc69589cd44f7c1a43206553984adde5cfb1) Adaptar la prueba config/parse a los patrones estándar.; Solicitud de incorporación [#1492](https://github.com/pgbackrest/pgbackrest/pull/1492)

### Notas de la versión v2.34 {#v234-release-notes}

*Soporte de PostgreSQL 14*

*Publicada el 7 de junio de 2021*

**Correcciones de errores:**

- Corregir problemas con archivos de spool remanentes de un `restore` anterior. (*Revisado por Cynthia Shang, Stefan Fercot. Probado por Floris van Nee. Reportado por Floris van Nee.*)

  Una notificación dejada en el spool por una restauración previa podía hacer que `archive-get` informara de un segmento WAL ausente. Si se encuentra en la primera comprobación, ahora se elimina y se vuelve a ejecutar el proceso asincrónico. Si este no responde, se informa de un error en lugar de indicar que falta el WAL.

  Incidencia [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Solicitud de incorporación [#1371](https://github.com/pgbackrest/pgbackrest/pull/1371); Commit [`f45e76f`](https://github.com/pgbackrest/pgbackrest/commit/f45e76fa2e8ce0f62317a74fdd51083d52659cd5)
- Corregir un problema al comprobar enlaces con grandes cantidades de tablespaces. (*Revisado por Cynthia Shang. Probado por Avinash Vallarapu. Reportado por Avinash Vallarapu.*)

  La comprobación de enlaces consumía mucha memoria con numerosos espacios de tablas y podía fallar. La nueva es mucho más rápida, usa mucha menos memoria y también detecta enlaces de archivo duplicados.

  Incidencia [#1354](https://github.com/pgbackrest/pgbackrest/issues/1354); Solicitud de incorporación [#1356](https://github.com/pgbackrest/pgbackrest/pull/1356); Commit [`eba013b`](https://github.com/pgbackrest/pgbackrest/commit/eba013b49b850e53d59795ac6358fcb3381048a3)
- Liberar los remotos que ya no se necesitan para que no agoten su tiempo de espera durante `restore`. (*Revisado por Cynthia Shang. Reportado por Francisco Miguel Biete Banon.*)

  Las conexiones remotas se mantenían durante toda la restauración y podían caducar, generando una advertencia inocua pero desconcertante al terminar una restauración larga. Ahora se cierran tras cargar el manifiesto.

  Incidencia [#1368](https://github.com/pgbackrest/pgbackrest/issues/1368); Solicitud de incorporación [#1374](https://github.com/pgbackrest/pgbackrest/pull/1374); Commit [`06fa185`](https://github.com/pgbackrest/pgbackrest/commit/06fa18582a405417c8ab4ba667cb01a13a5c3103)
- Corregir `help` cuando una opción válida es inválida para el comando especificado. (*Revisado por Stefan Fercot. Reportado por Cynthia Shang.*)

  `help` provocaba un fallo de segmentación al consultar una opción no válida para el comando.

  Solicitud de incorporación [#1375](https://github.com/pgbackrest/pgbackrest/pull/1375); Commit [`45f8355`](https://github.com/pgbackrest/pgbackrest/commit/45f83558ea862c6f496a27b886e1160e6303bbe8)

**Funcionalidades:**

- Añadir soporte de PostgreSQL 14. (*Revisado por Cynthia Shang.*)

  PostgreSQL 14 no requiere cambios de código respecto a PostgreSQL 13. Ahora la versión de catálogo puede cambiar durante las betas y RC de PostgreSQL sin exigir una nueva versión de pgBackRest.

  Solicitud de incorporación [#1413](https://github.com/pgbackrest/pgbackrest/pull/1413); Commit [`2452c4d`](https://github.com/pgbackrest/pgbackrest/commit/2452c4d5a4c230b8e3c33d3bddf69e56dfbec284)
- Añadir autenticación automática de GCS para instancias de GCE. (*Revisado por Jan Wieck. Probado por Daniel Farina.*)

  Establece `repo-gcs-key-type=auto` para obtener el token de autenticación de los metadatos de una instancia GCE.

  [`7b71604`](https://github.com/pgbackrest/pgbackrest/commit/7b71604defa02d5ed9b7aa3407961cb59a52cc45) Usar una variable existente para el puerto del servidor de pruebas GCS.

  [`26fefa6`](https://github.com/pgbackrest/pgbackrest/commit/26fefa6aeeae90bbb572ea57b605fb8fe526f1a0) Separar el análisis de respuestas de tokens GCS en otra función.

  [`9af0331`](https://github.com/pgbackrest/pgbackrest/commit/9af033194abc4b1cd3f06c3a97fff71c966c3827) Añadir autenticación automática de GCS para instancias de GCE.; Solicitud de incorporación [#1395](https://github.com/pgbackrest/pgbackrest/pull/1395)
- Añadir la opción `repo-retention-history` para expirar el historial de copias de seguridad. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang, David Steele.*)

  Configura cuántos días conservar el historial. Por defecto se conserva todo, y nunca caduca el historial de copias que aún están en el repositorio. Al caducar el manifiesto de una copia completa, también caducan los de sus copias diferenciales e incrementales.

  Solicitud de incorporación [#1389](https://github.com/pgbackrest/pgbackrest/pull/1389); Commit [`5b332b2`](https://github.com/pgbackrest/pgbackrest/commit/5b332b22b508d896abb64fa6abe26c78c83a29bc)
- Añadir la opción `db-exclude`. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang.*)

  La restauración excluye las bases indicadas escribiéndolas como archivos dispersos llenos de ceros. PostgreSQL puede completar la recuperación y después se pueden eliminar esas bases. Con `db-include`, `db-exclude` solo se aplica a las bases del sistema `template0`, `template1` y `postgres`.

  Incidencia [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Solicitud de incorporación [#1337](https://github.com/pgbackrest/pgbackrest/pull/1337); Commit [`292f836`](https://github.com/pgbackrest/pgbackrest/commit/292f836f1243e51d102bb4be202e7b21a7a386b1)

**Mejoras:**

- Cambiar el registro de la expiración del archivado del nivel detail al nivel info. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  Solicitud de incorporación [#1416](https://github.com/pgbackrest/pgbackrest/pull/1416); Commit [`aceb956`](https://github.com/pgbackrest/pgbackrest/commit/aceb956815a87f0c19ea171de25d2c3842a6d806)
- Eliminar la ruta de spool del archivado de la stanza en `restore`. (*Revisado por Cynthia Shang, Stefan Fercot.*)

  Los archivos del spool podían interferir con el clúster nuevo; por ejemplo, confirmaciones antiguas de `archive-push` podían hacer que se omitiera archivar WAL.

  Incidencia [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); Solicitud de incorporación [#1386](https://github.com/pgbackrest/pgbackrest/pull/1386); Commit [`320c6e1`](https://github.com/pgbackrest/pgbackrest/commit/320c6e1aad2cc9a8dabecb2bc91a9b34464de6ec)
- No escribir archivos atómicamente ni sincronizar rutas durante la copia de `backup`. (*Revisado por Stephen Frost, Stefan Fercot, Cynthia Shang.*)

  No hacen falta escrituras atómicas, porque al reanudar una copia fallida se verifican las sumas y al finalizar se sincronizan todas las rutas.

  Solicitud de incorporación [#1373](https://github.com/pgbackrest/pgbackrest/pull/1373); Commit [`aa72c19`](https://github.com/pgbackrest/pgbackrest/commit/aa72c19a831fb0dd15a50a003fbaad427f335353)

**Mejoras en la documentación:**

- Actualizar la documentación de contribución. (*Contribución de Cynthia Shang. Revisado por David Steele, Stefan Fercot.*)

  La guía de contribución incluye más ejemplos para escribir código, añadir opciones y realizar pruebas.

  Solicitud de incorporación [#1400](https://github.com/pgbackrest/pgbackrest/pull/1400); Commit [`68faf14`](https://github.com/pgbackrest/pgbackrest/commit/68faf1482a42ea14f5b00a91e19bd5aedec275b8)
- Consolidar la guía de usuario de RHEL/CentOS en un único documento. (*Revisado por Cynthia Shang.*)

  La segunda guía existía principalmente para documentar `stop-auto` en PostgreSQL <= 9.5, ya sin soporte. La opción sigue documentada en la referencia.

  Solicitud de incorporación [#1405](https://github.com/pgbackrest/pgbackrest/pull/1405); Commit [`ccac75e`](https://github.com/pgbackrest/pgbackrest/commit/ccac75e7de8754b39bb691ff8830a2839ea7a285)
- Aclarar que `repo-s3-role` no es un `ARN`. (*Contribución de Isaac Yuen. Revisado por David Steele.*)

  Solicitud de incorporación [#1365](https://github.com/pgbackrest/pgbackrest/pull/1365); Commit [`5bf1606`](https://github.com/pgbackrest/pgbackrest/commit/5bf160643b53699a28a8f0920c36d6ded767d249)

### Notas de la versión v2.33 {#v233-release-notes}

*Soporte de múltiples repositorios y de GCS*

*Publicada el 5 de abril de 2021*

**Correcciones de errores:**

- Corregir advertencias de opciones que rompían `archive-get`/`archive-push` asincrónicos. (*Revisado por Cynthia Shang. Reportado por Lev Kokotov.*)

  Una advertencia de opción del proceso asincrónico se escribía en stdout cerrado y abortaba el proceso. Al poder diferir las opciones válidas del rol asincrónico y el predeterminado, esto ocurría más a menudo. Ahora solo se registran esas advertencias para el rol predeterminado.

  Incidencia [#1299](https://github.com/pgbackrest/pgbackrest/issues/1299); Solicitud de incorporación [#1301](https://github.com/pgbackrest/pgbackrest/pull/1301); Commit [`3837e61`](https://github.com/pgbackrest/pgbackrest/commit/3837e61a7504b1e211e4b3a70cbe97343c1cf2e6)
- Corregir una fuga de memoria en la copia de seguridad durante la copia del archivado. (*Revisado por Cynthia Shang. Reportado por Christian ROUX, Efremov Egor.*)

  Copiar WAL a la copia mediante `archive-copy` filtraba memoria, sobre todo si había que recomprimirlo.

  Incidencia [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Commit [`778adbf`](https://github.com/pgbackrest/pgbackrest/commit/778adbf19f71ceb90071f01197bf189d59b14df0)
- Corregir un desbordamiento de pila en la generación de frases de contraseña de cifrado. (*Revisado por Cynthia Shang. Reportado por bsiara.*)

  El búfer de la frase de contraseña generada no tenía espacio para el cero final. Se detectó en arm64 con musl libc.

  Incidencia [#1294](https://github.com/pgbackrest/pgbackrest/issues/1294); Solicitud de incorporación [#1295](https://github.com/pgbackrest/pgbackrest/pull/1295); Commit [`d29855b`](https://github.com/pgbackrest/pgbackrest/commit/d29855bd0bf8b957fa8c06445d22e425c443a704)
- Corregir `repo-ls` `/` en repositorios S3. (*Revisado por Cynthia Shang. Reportado por Lesovsky Alexey.*)

  S3 notificaba `/` como un archivo sin los encabezados esperados, causando un error. Ahora `/` se informa como inexistente en almacenamiento que no admite rutas.

  Incidencia [#1317](https://github.com/pgbackrest/pgbackrest/issues/1317); Solicitud de incorporación [#1336](https://github.com/pgbackrest/pgbackrest/pull/1336); Commit [`b1d945e`](https://github.com/pgbackrest/pgbackrest/commit/b1d945ebb774c25676155af439b0558e8582bbe5)

**Funcionalidades:**

- Soporte de múltiples repositorios. (*Contribución de Cynthia Shang, David Steele. Revisado por Stefan Fercot, Stephen Frost.*)

  Se pueden configurar hasta cuatro repositorios, por ejemplo uno local para restaurar rápido y otro remoto para redundancia. `archive-push` envía WAL a todos y las copias se programan para cada repositorio. Algunos comandos trabajan con todos; otros requieren `repo`. No hace falta `repo` si solo está configurado `repo1`.

  [`3408f1e`](https://github.com/pgbackrest/pgbackrest/commit/3408f1ee2ee3f774699a15de045e0afe3eaf9a26) Mejorar el soporte de varios repositorios en expire.; Solicitud de incorporación [#1289](https://github.com/pgbackrest/pgbackrest/pull/1289)

  [`e28f6f1`](https://github.com/pgbackrest/pgbackrest/commit/e28f6f11e97a80e9c1adf1a6eaeeabbfc991914f) Expire continúa si se produce un error al procesar un repositorio.; Solicitud de incorporación [#1308](https://github.com/pgbackrest/pgbackrest/pull/1308)

  [`bec3e20`](https://github.com/pgbackrest/pgbackrest/commit/bec3e20b2cb061ef0413df24234ebe246ea53063) Añadir soporte de varios repositorios a archive-get.; Solicitud de incorporación [#1292](https://github.com/pgbackrest/pgbackrest/pull/1292)

  [`118d9e6`](https://github.com/pgbackrest/pgbackrest/commit/118d9e64fea71c2e049b52802e55f72f5793871b) Mejorar el soporte de varios repositorios en restore.; Solicitud de incorporación [#1300](https://github.com/pgbackrest/pgbackrest/pull/1300)

  [`065b2ff`](https://github.com/pgbackrest/pgbackrest/commit/065b2ff2300a9f06a8c32621fac521451ca942bd) Refactorizar repoMin/Max del comando info.

  [`0ddc038`](https://github.com/pgbackrest/pgbackrest/commit/0ddc0380ff408f9ed6e8bcd4d328df500681ce77) Eliminar el repo predeterminado de restore de las pruebas de integración.

  [`13dc8e6`](https://github.com/pgbackrest/pgbackrest/commit/13dc8e68d74fa9e06180e67b7e59994767b4a34d) Hacer opcional --repo para backup.; Solicitud de incorporación [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`a1280c4`](https://github.com/pgbackrest/pgbackrest/commit/a1280c41e530500e5bbde73a900683f6db207686) Refactorizar las advertencias de archive-push para que funcionen como las de archive-get.

  [`3b8f0ef`](https://github.com/pgbackrest/pgbackrest/commit/3b8f0ef7ae8a81ae969934fff4ad3da299454b24) Añadir tolerancia a fallos de escritura a archive-push.; Solicitud de incorporación [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`95063f6`](https://github.com/pgbackrest/pgbackrest/commit/95063f6812279cd59380fd72e16e67b631582bd0) Hacer opcional --repo para los comandos restantes salvo stanza-delete.

  [`1dbb3bf`](https://github.com/pgbackrest/pgbackrest/commit/1dbb3bf50b94dcc9d53dfe1e5ad57a17bd6d38e8) Soporte de múltiples repositorios.; Solicitud de incorporación [#1227](https://github.com/pgbackrest/pgbackrest/pull/1227)

  [`31c7824`](https://github.com/pgbackrest/pgbackrest/commit/31c7824a4d84cbf5a0ba0938f4caa546fa67af0a) Permitir ejecutar remotamente los comandos stanza-*.; Solicitud de incorporación [#1326](https://github.com/pgbackrest/pgbackrest/pull/1326)

  [`2789d3b`](https://github.com/pgbackrest/pgbackrest/commit/2789d3b6206c4de9299a3bc459e04cdab793abc9) Mejorar la tolerancia a fallos de info.; Solicitud de incorporación [#1342](https://github.com/pgbackrest/pgbackrest/pull/1342)

  [`01b8e22`](https://github.com/pgbackrest/pgbackrest/commit/01b8e2258f6efa5386665c33cb5c267c154376fb) Mejorar la tolerancia a fallos de archive-push.; Solicitud de incorporación [#1343](https://github.com/pgbackrest/pgbackrest/pull/1343)
- Soporte de GCS para el almacenamiento del repositorio. (*Revisado por Cynthia Shang. Probado por Daniel Farina.*)

  Establece `repo-type=gcs` para almacenar el repositorio en GCS o en un almacén compatible.

  [`dcb79ab`](https://github.com/pgbackrest/pgbackrest/commit/dcb79ab8fb18c63c2d56ecacd9d680b999ea044b) Decodificar los caracteres escapados con \u en JSON.

  [`1b4b353`](https://github.com/pgbackrest/pgbackrest/commit/1b4b3538cc218f66ed1e903c3caeade4b0ab1120) Renombrar uri como path donde corresponda en los módulos HTTP y de almacenamiento.

  [`66a4ff4`](https://github.com/pgbackrest/pgbackrest/commit/66a4ff496afe63305cb1a437bcb52d1efc11edf7) Codificar la ruta antes de pasarla a HttpRequest.

  [`d485609`](https://github.com/pgbackrest/pgbackrest/commit/d4856096587c72daee76f8ad8408db677a16d6dd) Añadir strNewEncode(), strCatEncode() y bufNewDecode().

  [`abcbe0f`](https://github.com/pgbackrest/pgbackrest/commit/abcbe0f9c1804ecb1b93b811cfb0a362c17e1b85) Combinar los archivos del módulo encode en uno solo.

  [`edab2a0`](https://github.com/pgbackrest/pgbackrest/commit/edab2a0b89eabc5fd5ba6e795d938670bd5d3105) Usar switch en lugar de if-else para los tipos de codificación.

  [`f6c3262`](https://github.com/pgbackrest/pgbackrest/commit/f6c3262861252b24e7e0cffd6d67e0c5e3291f3e) No exponer las funciones valid/validate del módulo encode.

  [`a1f4fd3`](https://github.com/pgbackrest/pgbackrest/commit/a1f4fd32a1790e569ccae3598cd9648bb25d13b6) Añadir ASSERT_MSG().

  [`00b60e5`](https://github.com/pgbackrest/pgbackrest/commit/00b60e564eef13f8adba0ab867fcde2c352669d6) Añadir codificación base64url.

  [`54c4eb0`](https://github.com/pgbackrest/pgbackrest/commit/54c4eb0c10758879b4bf2b96efd2a1523ecccc21) Permitir escribir en los objetos de almacenamiento remoto.

  [`088662d`](https://github.com/pgbackrest/pgbackrest/commit/088662d986288843d1bfd118b724091c93df4569) Soporte de GCS para el almacenamiento del repositorio.; Incidencia [#631](https://github.com/pgbackrest/pgbackrest/issues/631); Incidencia [#743](https://github.com/pgbackrest/pgbackrest/issues/743); Solicitud de incorporación [#1320](https://github.com/pgbackrest/pgbackrest/pull/1320)
- Añadir la opción `archive-header-check`. (*Revisado por Stephen Frost, Cynthia Shang. Sugerido por Hans-Jürgen Schönig.*)

  Se comprueba la cabecera WAL con la versión y el identificador del sistema PostgreSQL para enviarlo a la stanza correcta. La comprobación está activada por defecto y puede desactivarse si es necesario, por ejemplo para WAL cifrado.

  Solicitud de incorporación [#1298](https://github.com/pgbackrest/pgbackrest/pull/1298); Commit [`b6106f3`](https://github.com/pgbackrest/pgbackrest/commit/b6106f3c1f586b410c50c9da8dcea583cc157423)

**Mejoras:**

- Incluir las bases de datos del sistema recreadas durante la restauración selectiva. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang.*)

  Una base del sistema (`template0`, `template1` o `postgres`) recreada tiene un OID que la hace parecer una base de usuario. Ahora se restauran siempre, independientemente del OID.

  Incidencia [#986](https://github.com/pgbackrest/pgbackrest/issues/986); Solicitud de incorporación [#1307](https://github.com/pgbackrest/pgbackrest/pull/1307); Commit [`6942ff5`](https://github.com/pgbackrest/pgbackrest/commit/6942ff569dd950a5146faa0bebfee69e241c4179)
- Excluir `content-length` de los encabezados firmados de S3. (*Revisado por Cynthia Shang. Sugerido por Brian P Bockelman.*)

  Algunos proxies modifican `content-length`, lo que hacía fallar la autenticación si ese encabezado estaba firmado.

  Incidencia [#1340](https://github.com/pgbackrest/pgbackrest/issues/1340); Solicitud de incorporación [#1341](https://github.com/pgbackrest/pgbackrest/pull/1341); Commit [`7d7ac0e`](https://github.com/pgbackrest/pgbackrest/commit/7d7ac0e0eb63a02bbc1dd8bd8fc89c6008c740f8)
- Consolidar las opciones de almacenamiento del repositorio menos utilizadas. (*Revisado por Cynthia Shang.*)

  Las opciones de CA, host, puerto y verificación TLS de S3 y Azure se renombran a `repo-storage-*`; por ejemplo, `repo1-s3-host` pasa a `repo1-storage-host`. Se siguen aceptando los nombres antiguos.

  Solicitud de incorporación [#1321](https://github.com/pgbackrest/pgbackrest/pull/1321); Commit [`d1aa765`](https://github.com/pgbackrest/pgbackrest/commit/d1aa765a9d5f290738c1de00c5ea99d5f6056ba5)
- Permitir un valor por defecto personalizado de `config-path` con `./configure --with-configdir`. (*Contribución de Michael Schout. Revisado por David Steele.*)

  Los empaquetadores pueden cambiar el valor predeterminado de `config-path` al compilar. Sin la opción, sigue siendo `/etc/pgbackrest`.

  [`6a717e0`](https://github.com/pgbackrest/pgbackrest/commit/6a717e032f1309ddc9dc955042b5e2ac2bc7324d) Establecer la ruta de configuración en el script configure.

  [`9243962`](https://github.com/pgbackrest/pgbackrest/commit/9243962b9504787c6f4af42318af6dc27094136d) Permitir un valor por defecto personalizado de `config-path` con `./configure --with-configdir`.; Incidencia [#1251](https://github.com/pgbackrest/pgbackrest/issues/1251); Incidencia [#1293](https://github.com/pgbackrest/pgbackrest/issues/1293); Solicitud de incorporación [#1255](https://github.com/pgbackrest/pgbackrest/pull/1255)
- Registrar la copia del archivado durante `backup`. (*Revisado por Cynthia Shang, Stefan Fercot.*)

  Incidencia [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Solicitud de incorporación [#1328](https://github.com/pgbackrest/pgbackrest/pull/1328); Commit [`c862e96`](https://github.com/pgbackrest/pgbackrest/commit/c862e9654aff198167efeb897957bf93c1afe453)

**Mejoras en la documentación:**

- Actualizar la referencia para incluir enlaces a los ejemplos de la guía de usuario. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  La referencia de comandos ahora enlaza a ejemplos de la guía y aclara algunas descripciones, como `set` para `expire`.

  Solicitud de incorporación [#1353](https://github.com/pgbackrest/pgbackrest/pull/1353); Commit [`d372dd6`](https://github.com/pgbackrest/pgbackrest/commit/d372dd652c9a01b72444998d87f0f44464676803)
- Actualizar la documentación de restauración selectiva con advertencias. (*Revisado por Cynthia Shang, Stefan Fercot.*)

  La recuperación puede fallar si no se indica `type=immediate`, porque PostgreSQL considera errores las páginas de ceros tras alcanzar la coherencia. En PostgreSQL >= 13 se puede usar `ignore_invalid_pages`, pero hay que revisar el registro en busca de páginas no válidas en las bases seleccionadas.

  Incidencia [#796](https://github.com/pgbackrest/pgbackrest/issues/796); Solicitud de incorporación [#1329](https://github.com/pgbackrest/pgbackrest/pull/1329); Commit [`92d12cc`](https://github.com/pgbackrest/pgbackrest/commit/92d12ccb9bd0787e30441794e2a2a4d4a4e0fe9c)
- Añadir una aclaración de `compress-type` a la documentación de `archive-copy`. (*Revisado por Cynthia Shang, Stefan Fercot.*)

  Si `archive-push` y `backup` usan distintos `compress-type`, hay que recomprimir el WAL, lo que puede resultar costoso.

  Incidencia [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); Solicitud de incorporación [#1327](https://github.com/pgbackrest/pgbackrest/pull/1327); Commit [`9506ffa`](https://github.com/pgbackrest/pgbackrest/commit/9506ffae39dd86d2c5454511026f1249097d96a2)
- Añadir los valores por defecto de `compress-level` según el valor de `compress-type`. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  Los valores predeterminados son 9 para `bz2`, 6 para `gz`, 1 para `lz4` y 3 para `zst`.

  Incidencia [#1242](https://github.com/pgbackrest/pgbackrest/issues/1242); Solicitud de incorporación [#1346](https://github.com/pgbackrest/pgbackrest/pull/1346); Commit [`3e20608`](https://github.com/pgbackrest/pgbackrest/commit/3e206088e79c4a73a20b8f2fda1706c6b95fa188)
- Añadir una nota sobre que los ajustes de NFS requeridos son los mismos que los de PostgreSQL. (*Contribución de Cynthia Shang. Revisado por David Steele.*)

  Incidencia [#871](https://github.com/pgbackrest/pgbackrest/issues/871); Solicitud de incorporación [#1347](https://github.com/pgbackrest/pgbackrest/pull/1347); Commit [`7598762`](https://github.com/pgbackrest/pgbackrest/commit/75987621fab5f57d0e95b42eabd301731587c438)

### Notas de la versión v2.32 {#v232-release-notes}

*Comandos de repositorio*

*Publicada el 8 de febrero de 2021*

**Correcciones de errores:**

- Corregir la reanudación tras la eliminación parcial de una copia de seguridad por una reanudación anterior. (*Revisado por Cynthia Shang. Reportado por Tom Swartz.*)

**Funcionalidades:**

- Añadir el comando `repo-ls`. (*Revisado por Cynthia Shang. Probado por Stefan Fercot.*)
- Añadir el comando `repo-get`. (*Contribución de Stefan Fercot, David Steele. Revisado por Cynthia Shang.*)
- Añadir la opción `archive-mode-check`. (*Contribución de Stefan Fercot. Revisado por David Steele. Probado por Michael Banck.*)

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
- Añadir la opción `repo-azure-endpoint`. (*Revisado por Cynthia Shang. Probado por Brian Peterson. Sugerido por Brian Peterson.*)
- Añadir la opción `pg-database`. (*Revisado por Cynthia Shang.*)

**Mejoras:**

- Mejorar la salida del comando `info` cuando se especifica una stanza que no existe. (*Contribución de Stefan Fercot. Revisado por Cynthia Shang, David Steele. Sugerido por uspen.*)
- Mejorar el rendimiento de las listas extensas de archivos en los comandos `backup`/`restore`. (*Revisado por Cynthia Shang. Probado por Oscar.*)
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

- Obtener automáticamente credenciales S3 temporales en instancias de AWS. (*Contribución de David Steele, Stephen Frost. Revisado por Cynthia Shang, Aleš Zelený, Jeanette Bromage. Probado por David Youatt.*)
- Añadir la opción `archive-mode` para deshabilitar el archivado en la restauración. (*Revisado por Stephen Frost. Sugerido por Stephen Frost.*)

**Mejoras:**

- Soporte de PostgreSQL 13 beta3. Los cambios en las versiones de control/catálogo/WAL en betas posteriores pueden romper la compatibilidad, pero pgBackRest se actualizará con cada versión para mantener el ritmo.
- `list`/`remove` asincrónicos para el almacenamiento S3/Azure. (*Revisado por Cynthia Shang, Stephen Frost.*)
- Mejorar el uso de memoria de la detección de relaciones unlogged en la construcción del manifiesto. (*Revisado por Cynthia Shang, Stephen Frost, Oscar. Probado por Brad Nicholson. Sugerido por Oscar, Brad Nicholson.*)
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

- Soporte de Azure para el almacenamiento del repositorio. (*Revisado por Cynthia Shang. Probado por Don Seiler.*)
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

- Implementación de TLS no bloqueante. (*Revisado por Cynthia Shang, Stephen Frost. Probado por Slava Moudry.*)
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
