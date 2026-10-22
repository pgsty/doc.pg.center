---
title: "11. Tablas de persistencia y pares"
linkTitle: "11. Tablas de persistencia y pares"
weight: 220
description: "Declaraciones de almacenamiento en tablas de persistencia y de replicación entre pares"
icon: fa-solid fa-table
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/stick-tables-and-peers/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 11"
---

Las tablas de persistencia en HAProxy son un mecanismo que permite asociar un cierto número de
informaciones y métricas con una clave de un tipo determinado, y esto durante una cierta duración
tras la última actualización. Esto puede verse como una línea de varias columnas en una tabla, donde
el número de línea viene definido por el valor de la clave, y las columnas representan todas
criterios distintos.

Las tablas de persistencia se diseñaron originalmente para almacenar información de persistencia
cliente-servidor con el fin de mantener sesiones persistentes entre estas entidades. Un cliente se
conectaba o enviaba una solicitud; este cliente se identificaba mediante un discriminador
(dirección de origen, cookie, parámetro de URL) y el servidor elegido se almacenaba en asociación
con este discriminador en una tabla de persistencia durante una duración configurable, de modo que
los accesos posteriores del mismo cliente pudieran dirigirse automáticamente al mismo servidor,
donde el cliente había creado su sesión de aplicación.

Hoy en día, las tablas de persistencia pueden almacenar más información que un simple número de
servidor: pueden almacenarse elementos como métricas de actividad relacionadas con un cliente
específico (números/tasas de solicitudes, números/tasas de conexiones, números/tasas de bytes,
etc.), así como algunos contadores de eventos arbitrarios («gpc», por «Contadores de Propósito
General») y algunas etiquetas para marcar a un cliente con ciertas características («gpt», por
«Etiqueta de Propósito General»).

Las tablas de persistencia pueden ser referenciadas por las directivas «stick», usadas para la
persistencia cliente-servidor, por las reglas «track-sc», usadas para describir qué clave rastrear
y en qué tabla con el fin de recopilar métricas, así como por una serie de funciones de extracción
de muestras y convertidores que pueden realizar una búsqueda inmediata de una clave dada para
obtener una métrica o un dato específico. El principio general es que las actualizaciones de las
tablas (gpt/gpc/métricas), así como las búsquedas de información de persistencia, refrescan la
entrada accedida y posponen su expiración, mientras que las meras búsquedas desde funciones de
extracción de muestras y convertidores solo extraen los datos sin posponer la expiración de la
entrada.

Para que el mecanismo escale y resista las recargas y conmutaciones por error de HAProxy, es
posible compartir las actualizaciones de las tablas de persistencia con otros nodos llamados
«pares» (peers) mediante el mecanismo «Peers» descrito en la [sección 11.2](/es/haproxy/stick-tables-and-peers/#section-11-2). Para ajustar finamente la
comunicación con los pares, también es posible decidir que algunas tablas solo reciban información
de los pares, o que las actualizaciones de los pares se reenvíen en cambio a una tabla diferente.

Finalmente, las tablas de persistencia pueden declararse en secciones de proxy (frontends,
backends) usando la palabra clave «stick-table», donde solo puede haber una por sección y donde
tomarán el nombre de esa sección, o en secciones peers con la palabra clave «table» seguida del
nombre de la tabla, lo que permite declarar múltiples tablas de persistencia en la misma sección
«peers». Si se necesitan varias tablas de persistencia, la solución recomendada suele ser declararlas
en una sección peers (en caso de que vayan a compartirse) o crear secciones backend adicionales,
cada una con solo la definición «stick-table».

## 11.1. Declaración de stick-table {#section-11-1}

La declaración de una tabla de persistencia en una sección de proxy («frontend», «backend»,
«listen») y en secciones «peers» es muy similar, con la diferencia de que la de la sección peers
exige un nombre obligatorio y no admite ninguna opción «peers».

En una sección «frontend», «backend» o «listen»:

stick-table type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only] [write-to
`<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`] [peers
`<peersect>`]

En una sección «peers»:

table `<name>` type `<type>` size `<size>` [expire `<expire>`] [nopurge] [recv-only]
[write-to `<wtable>`] [srvkey `<srvkey>`] [store `<data_type>`]\* [brates-factor `<factor>`]

Argumentos: (los obligatorios primero, luego ordenados alfabéticamente):

- type `<type>` Este argumento obligatorio define el tipo de clave como `<type>`, que normalmente
  es una sola palabra pero también puede tener sus propios argumentos:

  - ip Este tipo debería evitarse en favor de uno más explícito, como «ipv4» o «ipv6». Antes de la
    versión 3.2 era la única forma de configurar IPv4. En 3.2, «ip» es un alias de «ipv4», y se
    prefiere «ipv4». En una versión futura, «ip» corresponderá en cambio a «ipv6». Solo está
    pensado para facilitar la transición de las versiones anteriores a 3.2 a las posteriores a 3.2.

  - ipv4 Una tabla declarada con este tipo solo almacenará direcciones IPv4. Esta forma es muy
    compacta (unos 50 bytes por entrada) y permite búsquedas y almacenamientos de entradas muy
    rápidos con casi ningún coste adicional. Se usa principalmente para almacenar direcciones IP de
    origen de los clientes.

  - ipv6 Una tabla declarada con «type ipv6» solo almacenará direcciones IPv6. Esta forma es muy
    compacta (unos 60 bytes por entrada) y permite búsquedas y almacenamientos de entradas muy
    rápidos con casi ningún coste adicional. Se usa principalmente para almacenar direcciones IP de
    origen de los clientes.

  - integer Una tabla declarada con «type integer» almacenará enteros de 32bit que pueden
    representar, por ejemplo, un identificador de cliente encontrado en una solicitud.

  - string [len `<len>`] Una tabla declarada con «type string» almacenará subcadenas de hasta
    `<len>` caracteres. Si la cadena proporcionada por el extractor de patrones es más larga que
    `<len>`, se truncará antes de almacenarse. Durante la comparación, se compararán como máximo
    `<len>` caracteres entre la cadena de la tabla y el patrón extraído. Cuando no se especifica,
    la cadena queda automáticamente limitada a 32 caracteres. Aumentar la longitud puede tener un
    impacto no despreciable en el uso de memoria.

  - binary [len `<len>`] Una tabla declarada con «type binary» almacenará bloques binarios de
    `<len>` bytes. Si el bloque proporcionado por el extractor de patrones es más grande que
    `<len>`, se truncará antes de almacenarse. Si el bloque proporcionado por la expresión de
    muestra es más corto que `<len>`, se rellenará con 0. Cuando no se especifica, el bloque queda
    automáticamente limitado a 32 bytes. Aumentar la longitud puede tener un impacto no
    despreciable en el uso de memoria.

- size `<size>` Este argumento obligatorio define el número máximo de entradas que caben en la
  tabla como `<size>`. Este valor impacta directamente en el uso de memoria. Cuenta aproximadamente
  50 bytes por entrada, además del tamaño de la clave anterior, las métricas almacenadas
  opcionalmente y el tamaño de una cadena si la hay. El tamaño admite los sufijos «k», «m», «g»
  para los factores 2^10, 2^20 y 2^30.

- expire `<delay>` Define la duración máxima de una entrada en la tabla desde la última vez que se creó,
  se actualizó usando «track-sc» o coincidió al aplicar una regla «stick match» o «stick on». El retardo
  de expiración `<delay>` se define usando el formato de tiempo estándar, de forma similar a los
  diversos tiempos de espera, con milisegundos como valor predeterminado. La duración máxima es
  ligeramente superior a 24 días. Consulta la [sección 2.5](/es/haproxy/configuration-basics/#section-2-5) para más
  información. Si no se especifica este retardo, las sesiones no expiran automáticamente, pero las
  entradas más antiguas se eliminarán al crearse una nueva una vez que esté llena. Asegúrate de no
  usar el parámetro «nopurge» si no se especifica ningún retardo de expiración. Nota: los
  convertidores «table\_\*» realizan búsquedas pero no actualizan la expiración al tocarlos, ya que
  no requieren «track-sc».

- brates-factor `<factor>` Especifica un factor que se aplicará a la tasa de bytes de
  entrada/salida. En lugar de contar cada byte, se cuentan bloques de bytes. Internamente, las
  tasas se definen en contadores de 32 bits, lo que las limita a unos 4 mil millones por periodo.
  Usando este parámetro es posible tener tasas que superen este límite de 4G durante el periodo
  definido. El factor debe ser mayor que 0 y menor o igual que 1024.

- nopurge indica que nos negamos a purgar las entradas más antiguas cuando la tabla está llena.
  Cuando no se especifica y la tabla está llena cuando HAProxy quiere almacenar una entrada en
  ella, se vaciarán algunas de las entradas más antiguas para liberar algo de espacio para las
  nuevas. Este es el comportamiento deseado en la mayoría de los casos. En algunos casos
  específicos, será preferible rechazar entradas nuevas en lugar de purgar las antiguas. Puede ser
  el caso cuando la cantidad de datos a almacenar supera con mucho los límites del hardware y
  preferimos no ofrecer acceso a clientes nuevos antes que rechazar a los ya conectados. Al usar
  este parámetro, asegúrate de configurar correctamente el parámetro «expire» (consulta más arriba).

- recv-only indica que no tenemos la intención de usar la tabla para realizar actualizaciones en
  ella, sino que solo planeamos usar la tabla para recuperar datos de un par remoto que nos
  interesa. En efecto, el uso de esta palabra clave habilita la recuperación de valores
  exclusivamente locales como «conn_cur», que no se aprenden por defecto porque entrarían en
  conflicto con las actualizaciones locales realizadas en la tabla por el par local. El uso de esta
  opción solo es pertinente para tablas que no participan en reglas de rastreo ni en métodos que
  realicen operaciones de actualización en la tabla, o dicho más simple: tablas remotas que solo se
  usan para recuperar información.

- peers `<peersect>` Las entradas que se creen, actualicen o refresquen se enviarán a los pares de
  la sección `<peersect>` para su sincronización, y las claves aprendidas de los pares de esta
  sección también se insertarán o actualizarán en la tabla. Además, al arrancar, se puede intentar
  aprender entradas de una instancia anterior del proceso, designada como el «par local» mediante
  esta sección.

- srvkey `<srvkey>` Especifica cómo se identifica cada servidor a efectos de la tabla de
  persistencia. Los valores válidos son «name» y «addr». Si se indica «name», entonces el argumento
  `<name>` del servidor (puede ser generado por una plantilla). Si se indica «addr», el servidor se
  identifica por su dirección de red actual, incluido el puerto. «addr» es especialmente útil si
  usas descubrimiento de servicios para generar las direcciones de servidores con tablas de
  persistencia emparejadas y quieres usar de forma consistente el mismo host entre los pares para
  un token de persistencia.

- store `<data_type>` Se usa para almacenar información adicional en la tabla de persistencia.
  Puede ser usado por las ACL para controlar diversos criterios relacionados con la actividad del
  cliente que coincide con la tabla de persistencia. Por cada elemento que se especifique aquí, el
  tamaño de cada entrada se incrementará para que los datos adicionales quepan. Se pueden
  almacenar varios tipos de datos con una entrada. Se pueden especificar múltiples tipos de datos
  tras la palabra clave «store», como una lista separada por comas. Alternativamente, es posible
  repetir la palabra clave «store» seguida de uno o varios tipos de datos. Salvo el tipo
  «server_id», que se detecta y habilita automáticamente, todos los tipos de datos deben declararse
  explícitamente para almacenarse. Si una ACL referencia un tipo de datos que no está almacenado,
  la ACL simplemente no coincidirá. Algunos tipos de datos requieren un argumento que debe pasarse
  justo después del tipo, entre paréntesis. Consulta más abajo los tipos de datos soportados y sus
  argumentos.

- write-to `<wtable>` Especifica el nombre de otra tabla de persistencia donde se escribirán
  también las actualizaciones de los pares, además de en la tabla de origen. `<wtable>` debe ser
  del mismo tipo que la tabla que se está definiendo y tener la misma longitud de clave, y la tabla
  de origen no puede usarse a su vez como tabla de destino. Cada vez que se reciba una
  actualización de entrada en la tabla de origen a través de un par, HAProxy intentará refrescar
  la entrada relacionada de `<wtable>`. Si la entrada todavía no existe, se creará; de lo
  contrario, sus valores se actualizarán al igual que su temporizador. Ten en cuenta que solo los
  tipos que no participan en operaciones aritméticas, como server_id, server_key y gpt, se
  escribirán en `<wtable>` para evitar que los valores procesados de una tabla remota interfieran
  con las operaciones aritméticas realizadas en la tabla de destino local. (es decir: evitar que un
  contador acumulativo compartido crezca indefinidamente) Un uso común de esta opción es poder
  usar reglas de persistencia (para la persistencia de servidores) en una configuración de clúster
  de pares, porque las claves que coincidan se aprenderán de las tablas remotas.

Los tipos de datos que pueden asociarse a una entrada mediante la directiva «store» se listan a
continuación. Es importante tener en cuenta que los requisitos de memoria pueden ser importantes
al almacenar muchos tipos de datos. En efecto, almacenar todos los indicadores siguientes a la vez
en cada entrada puede requerir cientos de bytes por entrada, o cientos de MB para una tabla de 1
millón de entradas. Por esta razón, el tamaño de almacenamiento aproximado se indica más abajo
para cada tipo entre corchetes, después del argumento.

Argumentos:

- bytes_in_cnt [8 bytes] Es el contador de bytes del cliente al servidor. Es un entero de 64 bits
  positivo que cuenta el número acumulado de bytes recibidos de los clientes que coincidieron con
  esta entrada. Las cabeceras se incluyen en el recuento. Puede usarse para limitar el abuso de las
  funciones de subida en servidores de fotos o vídeos. Ten en cuenta que los valores se miden
  cuando los datos entran en haproxy, por lo que los recuentos no se ven afectados por la
  compresión.

- bytes_in_rate(`<period>`) [12 bytes] Es un contador de tasa sobre los bytes del cliente al
  servidor. Toma un parámetro entero `<period>` que indica en milisegundos la duración del periodo
  sobre el cual se mide la media. Informa de la tasa media de bytes entrantes durante ese periodo,
  en bytes por periodo. Puede usarse para detectar usuarios que suben demasiado y demasiado
  rápido. Atención: con subidas grandes, es posible que la cantidad de datos subidos se cuente una
  sola vez al finalizar, lo que provoca picos en la velocidad media de transferencia en lugar de
  una velocidad uniforme. Esto puede suavizarse parcialmente con «option contstats», aunque no es
  perfecto. Se recomienda el uso de bytes_in_cnt para una mejor equidad.

- bytes_out_cnt [8 bytes] Es el contador de bytes del servidor al cliente. Es un entero de 64 bits
  positivo que cuenta el número acumulado de bytes enviados a los clientes que coincidieron con
  esta entrada. Las cabeceras se incluyen en el recuento. Puede usarse para limitar el abuso de
  bots que descargan todo el sitio. Ten en cuenta que los valores se miden cuando los datos entran
  en haproxy, por lo que los recuentos no se ven afectados por la compresión.

- bytes_out_rate(`<period>`) [12 bytes] Es un contador de tasa sobre los bytes del servidor al
  cliente. Toma un parámetro entero `<period>` que indica en milisegundos la duración del periodo
  sobre el cual se mide la media. Informa de la tasa media de bytes salientes durante ese periodo,
  en bytes por periodo. Puede usarse para detectar usuarios que descargan demasiado y demasiado
  rápido. Atención: con transferencias grandes, es posible que la cantidad de datos transferidos se
  cuente una sola vez al finalizar, lo que provoca picos en la velocidad media de transferencia en
  lugar de una velocidad uniforme. Esto puede suavizarse parcialmente con «option contstats»,
  aunque todavía no es perfecto. Se recomienda el uso de bytes_out_cnt para una mejor equidad.

- conn_cnt [4 bytes] Es el Contador de Conexiones. Es un entero de 32 bits positivo que cuenta el
  número absoluto de conexiones recibidas de los clientes que coincidieron con esta entrada. No
  significa que las conexiones fueran aceptadas, solo que fueron recibidas.

- conn_cur [4 bytes] Es el contador de Conexiones Actuales. Es un entero de 32 bits positivo que
  almacena el número de conexiones simultáneas de la entrada. Se incrementa cuando una conexión
  entrante coincide con la entrada y se decrementa cuando la conexión se va. De este modo es
  posible conocer en todo momento el número exacto de conexiones simultáneas de una entrada. Este
  tipo no se aprende de otros pares por defecto, ya que no representaría nada dado que ignoraría el
  recuento local. Sin embargo, combinado con recv-only puede usarse para aprender el número de
  conexiones simultáneas vistas por los pares.

- conn_rate(`<period>`) [12 bytes] Es un contador de frecuencia de conexiones. Toma un parámetro
  entero `<period>` que indica en milisegundos la duración del periodo sobre el cual se mide la
  media. Informa de la tasa media de conexiones entrantes durante ese periodo, en conexiones por
  periodo. El resultado es un entero que puede compararse usando ACL. El que las conexiones se
  acepten o se rechacen no tiene ningún efecto en su medición.

- glitch_cnt [4 bytes] Es el contador de glitches del frontend. Es un entero de 32 bits positivo
  que cuenta el número acumulado de glitches reportados en una conexión del frontend. Los glitches
  corresponden a acciones inusuales o inesperadas (a nivel de protocolo) del cliente que podrían
  indicar un cliente muy defectuoso o posiblemente un atacante. Como tal, este contador puede
  ayudar a decidir cómo actuar con ellos en tal caso.

- glitch_rate(`<period>`) [12 bytes] Es un contador de frecuencia de glitches. Toma un parámetro
  entero `<period>` que indica en milisegundos la duración del periodo sobre el cual se mide la
  media. Informa de la tasa media de glitches del frontend durante ese periodo. Puede usarse para
  detectar clientes defectuosos o atacantes potenciales que realizan acciones poco comunes o
  inesperadas desde el punto de vista del protocolo, siempre que HAProxy los haya marcado como
  tales.

- gpc(`<nb>`) [4 \* `<nb>` bytes] Es un array de `<nb>` elementos de Contador de Propósito
  General. Es un array de enteros de 32 bits positivos que pueden usarse para contar cualquier
  cosa. La mayoría de las veces se usarán como contadores incrementales en algunas entradas, por
  ejemplo para señalar que se alcanzó un límite y desencadenar algunas acciones. Este array está
  limitado a un máximo de 100 elementos: gpc0 a gpc99, para garantizar que la construcción de un
  mensaje de actualización de par quepa en el búfer. Los usuarios deben tener en cuenta que una
  gran cantidad de contadores incrementará el tamaño de los datos y la carga de tráfico al usar el
  protocolo de pares, ya que todos los datos/contadores se envían cada vez que se actualiza
  cualquiera de ellos. Este data_type excluye el uso de los data_types heredados «gpc0» y «gpc1»
  en la misma tabla. Al usar el data_type de array «gpc», todas las funciones de extracción de
  muestras y acciones relacionadas con «gpc0» y «gpc1» se aplicarán a los dos primeros elementos de
  este array.

- gpc_rate(`<nb>`,`<period>`) [12 \* `<nb>` bytes] Es un array de tasas de incremento de
  Contadores de Propósito General durante un periodo. Estos elementos son enteros de 32 bits
  positivos que pueden usarse para cualquier cosa. Al igual que `<gpc>`, cuentan eventos, pero en
  lugar de mantener un número acumulado, mantienen la tasa a la que se incrementa el contador. La
  mayoría de las veces se usará para medir la frecuencia de ocurrencia de ciertos eventos (p. ej.,
  solicitudes a una URL específica). Este array está limitado a un máximo de 100 elementos:
  gpc_rate(100,`<period>`), lo que permite almacenar gpc0_rate a gpc99_rate, para garantizar que
  la construcción de un mensaje de actualización de par quepa en el búfer. El array no puede
  contener menos de 1 elemento: usa gpc_rate(1,`<period>`) si quieres almacenar solo la tasa del
  contador gpc0_rate. Los usuarios deben tener en cuenta que una gran cantidad de contadores
  incrementará el tamaño de los datos y la carga de tráfico al usar el protocolo de pares, ya que
  todos los datos/contadores se envían cada vez que se actualiza cualquiera de ellos. Este
  data_type excluye el uso de los data_types heredados «gpc0_rate» y «gpc1_rate» en la misma
  tabla. Al usar el data_type de array «gpc_rate», todas las extracciones y acciones relacionadas
  con «gpc0» y «gpc1» se aplicarán a los dos primeros elementos de este array.

- gpc0 [4 bytes] Es el primer Contador de Propósito General. Es un entero de 32 bits positivo que
  puede usarse para cualquier cosa. La mayoría de las veces se usará para poner una etiqueta
  especial en algunas entradas, por ejemplo para señalar que se detectó un comportamiento
  específico y debe conocerse para coincidencias futuras.

- gpc0_rate(`<period>`) [12 bytes] Es la tasa de incremento del primer Contador de Propósito
  General durante un periodo. Es un entero de 32 bits positivo que puede usarse para cualquier
  cosa. Al igual que `<gpc0>`, cuenta eventos, pero en lugar de mantener un número acumulado,
  mantiene la tasa a la que se incrementa el contador. La mayoría de las veces se usará para medir
  la frecuencia de ocurrencia de ciertos eventos (p. ej., solicitudes a una URL específica).

- gpc1 [4 bytes] Es el segundo Contador de Propósito General. Es un entero de 32 bits positivo
  que puede usarse para cualquier cosa. La mayoría de las veces se usará para poner una etiqueta
  especial en algunas entradas, por ejemplo para señalar que se detectó un comportamiento
  específico y debe conocerse para coincidencias futuras.

- gpc1_rate(`<period>`) [12 bytes] Es la tasa de incremento del segundo Contador de Propósito
  General durante un periodo. Es un entero de 32 bits positivo que puede usarse para cualquier
  cosa. Al igual que `<gpc1>`, cuenta eventos, pero en lugar de mantener un número acumulado,
  mantiene la tasa a la que se incrementa el contador. La mayoría de las veces se usará para medir
  la frecuencia de ocurrencia de ciertos eventos (p. ej., solicitudes a una URL específica).

- gpt(`<nb>`) [4 \* `<nb>` bytes] Es un array de `<nb>` elementos de Etiqueta de Propósito
  General. Es un array de enteros de 32 bits positivos que pueden usarse para cualquier cosa. La
  mayoría de las veces se usarán para poner etiquetas especiales en algunas entradas, por ejemplo
  para señalar que se detectó un comportamiento específico y debe conocerse para coincidencias
  futuras. Este array está limitado a un máximo de 100 elementos: gpt(100), lo que permite
  almacenar gpt0 a gpt99, para garantizar que la construcción de un mensaje de actualización de par
  quepa en el búfer. El array no puede contener menos de 1 elemento: usa gpt(1) si quieres
  almacenar solo la etiqueta gpt0. Los usuarios deben tener en cuenta que una gran cantidad de
  contadores incrementará el tamaño de los datos y la carga de tráfico al usar el protocolo de
  pares, ya que todos los datos/contadores se envían cada vez que se actualiza cualquiera de
  ellos. Este data_type excluye el uso del data_type heredado «gpt0» en la misma tabla. Al usar el
  data_type de array «gpt», todas las extracciones y acciones relacionadas con «gpt0» se aplicarán
  al primer elemento de este array.

- gpt0 [4 bytes] Es la primera Etiqueta de Propósito General. Es un entero de 32 bits positivo
  que puede usarse para cualquier cosa. La mayoría de las veces se usará para poner una etiqueta
  especial en algunas entradas, por ejemplo para señalar que se detectó un comportamiento
  específico y debe conocerse para coincidencias futuras.

- http_req_cnt [4 bytes] Es el Contador de solicitudes HTTP. Es un entero de 32 bits positivo que
  cuenta el número absoluto de solicitudes HTTP recibidas de los clientes que coincidieron con esta
  entrada. No importa si son solicitudes válidas o no. Ten en cuenta que esto es diferente de las
  sesiones cuando se usa keep-alive en el lado del cliente.

- http_req_rate(`<period>`) [12 bytes] Es un contador de frecuencia de solicitudes. Toma un
  parámetro entero `<period>` que indica en milisegundos la duración del periodo sobre el cual se
  mide la media. Informa de la tasa media de solicitudes HTTP durante ese periodo, en solicitudes
  por periodo. El resultado es un entero que puede compararse usando ACL. No importa si son
  solicitudes válidas o no. Ten en cuenta que esto es diferente de las sesiones cuando se usa
  keep-alive en el lado del cliente.

- http_err_cnt [4 bytes] Es el Contador de errores de solicitudes HTTP. Es un entero de 32 bits
  positivo que cuenta el número absoluto de errores de solicitudes HTTP inducidos por los clientes
  que coincidieron con esta entrada. Los errores se cuentan en las solicitudes inválidas y
  truncadas, así como en las solicitudes denegadas o retardadas (tarpitted) y en las
  autenticaciones fallidas. Si el servidor responde con un 4xx, la solicitud también se cuenta como
  error, ya que es un error provocado por el cliente (p. ej., un escaneo de vulnerabilidades).

- http_err_rate(`<period>`) [12 bytes] Es un contador de frecuencia de solicitudes HTTP. Toma un
  parámetro entero `<period>` que indica en milisegundos la duración del periodo sobre el cual se
  mide la media. Informa de la tasa media de errores de solicitudes HTTP durante ese periodo, en
  solicitudes por periodo (consulta http_err_cnt más arriba para saber qué se cuenta como error). El
  resultado es un entero que puede compararse usando ACL.

- http_fail_cnt [4 bytes] Es el Contador de fallos de respuestas HTTP. Es un entero de 32 bits
  positivo que cuenta el número absoluto de fallos de respuestas HTTP inducidos por los servidores
  que coincidieron con esta entrada. Los errores se cuentan en las respuestas inválidas y
  truncadas, así como en cualquier respuesta 5xx distinta de 501 o 505. Su objetivo es usarse
  combinado con la ruta o el URI para detectar fallos del servicio.

- http_fail_rate(`<period>`) [12 bytes] Es un contador de frecuencia de fallos de respuestas
  HTTP. Toma un parámetro entero `<period>` que indica en milisegundos la duración del periodo
  sobre el cual se mide la media. Informa de la tasa media de fallos de respuestas HTTP durante ese
  periodo, en solicitudes por periodo (consulta http_fail_cnt más arriba para saber qué se cuenta como
  fallo). El resultado es un entero que puede compararse usando ACL.

- server_id [4 bytes] Es un entero que contiene el ID numérico del servidor al que se asignó una
  solicitud. Lo usan las reglas «stick match», «stick store» y «stick on». Se habilita
  automáticamente cuando se referencia. Es importante entender que la persistencia basada en
  información aprendida tiene algunas limitaciones, incluido el hecho de que todas las asociaciones
  aprendidas se pierden al reiniciar, salvo que los pares estén correctamente configurados para
  transferir dicha información al reiniciar (recomendado). En general puede ser bueno como
  complemento de otros mecanismos de persistencia, pero no siempre como único mecanismo.

- sess_cnt [4 bytes] Es el Contador de Sesiones. Es un entero de 32 bits positivo que cuenta el
  número absoluto de sesiones recibidas de los clientes que coincidieron con esta entrada. Una
  sesión es una conexión que fue aceptada por las reglas de capa 4 («tcp-request connection»).

- sess_rate(`<period>`) [12 bytes] Es un contador de frecuencia de sesiones. Toma un parámetro
  entero `<period>` que indica en milisegundos la duración del periodo sobre el cual se mide la
  media. Informa de la tasa media de sesiones entrantes durante ese periodo, en sesiones por
  periodo. El resultado es un entero que puede compararse usando ACL.

Ejemplo:

```shell
# Keep track of counters of up to 1 million IP addresses over 5 minutes
# and store a general purpose counter and the average connection rate
# computed over a sliding window of 30 seconds.
stick-table type ip size 1m expire 5m store gpc0,conn_rate(30s)
```

Consulta también: «stick match», «stick on», «stick store-request», «track-sc», la [sección 2.5](/es/haproxy/configuration-basics/#section-2-5) sobre el
formato de tiempo, la [sección 11.2](/es/haproxy/stick-tables-and-peers/#section-11-2) sobre los pares, la [sección 9.7](/es/haproxy/filters/#section-9-7) sobre las limitaciones de
ancho de banda y la [sección 7](/es/haproxy/acls-and-samples/) sobre las ACL.

## 11.2. Declaración de peers {#section-11-2}

Es posible propagar entradas de cualquier tipo de datos en tablas de persistencia entre varias
instancias de HAProxy mediante conexiones TCP de forma multi-maestro. Cada instancia envía sus
actualizaciones e inserciones locales a los pares remotos. Los valores enviados sobrescriben los
remotos sin agregación.

Una excepción es el tipo de datos «conn_cur», que nunca se aprende de los pares por defecto, ya
que se supone que debe reflejar valores locales. Las versiones anteriores solían sincronizarlo por
defecto, lo que se sabía que provocaba valores negativos en configuraciones activo-activo y
valores siempre crecientes en las recargas o conmutaciones activo-pasivo, porque el valor local
reflejaría más conexiones de las presentes localmente. Sin embargo, hay algunas configuraciones
donde puede ser pertinente aprender este valor de los pares, por ejemplo cuando la tabla es una
tabla remota pasiva usada únicamente para aprender/monitorizar datos de ella sin depender de ella
para operaciones de escritura o actualizaciones. Para lograrlo, se puede añadir la palabra clave
«recv-only» en la declaración de la tabla. En cualquier caso, la información de «conn_cur» siempre
se envía para que los sistemas de monitorización puedan observarla.

Los intercambios interrumpidos se detectan automáticamente y se recuperan desde el último punto
conocido. Además, durante un reinicio suave, el proceso antiguo se conecta al nuevo usando una
conexión TCP de este tipo para enviar todas sus entradas antes de que el nuevo proceso intente
conectarse a otros pares. Esto garantiza una replicación muy rápida durante una recarga;
normalmente tarda una fracción de segundo incluso para tablas grandes.

Ten en cuenta que los ID de servidor se usan para identificar servidores de forma remota, por lo
que es importante que las configuraciones se parezcan o, al menos, que se fuercen los mismos ID en
cada servidor en todos los participantes.

<a id="entry-11-2-peers"></a>

**`peers <peersect>`**

```haproxy
peers <peersect>
```

Crea una nueva lista de pares con el nombre `<peersect>`. Es una sección independiente,
referenciada por una o más tablas de persistencia.

<a id="entry-11-2-bind"></a>

**`bind [<address>]:port [param*]`**

```haproxy
bind [<address>]:port [param*]
bind /<path> [param*]
```

Define los parámetros de enlace del par local de esta sección «peers». Estas líneas no están
soportadas junto con una línea «peer» en la misma sección «peers».

<a id="entry-11-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Desactiva una sección peers. Desactiva tanto la escucha como cualquier sincronización relacionada
con esta sección. Se proporciona para desactivar la sincronización de las tablas de persistencia
sin tener que comentar todas las referencias «peers».

<a id="entry-11-2-default-bind"></a>

**`default-bind [param*]`**

```haproxy
default-bind [param*]
```

Define los parámetros de enlace del par local, salvo su dirección.

<a id="entry-11-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Cambia las opciones predeterminadas de un servidor en una sección «peers».

Argumentos:

```text
<param*>  es una lista de parámetros para este servidor. La palabra clave
          «default-server» acepta un número importante de opciones y tiene
          una sección completa dedicada a ella. En una sección peers, se
          soportan los parámetros de transporte de una línea
          «default-server». Consulta la sección 5 para más detalles, y la
          palabra clave «server» más abajo en esta sección para algunas de
          las restricciones.
```

Consulta también: «server» y la [sección 5](/es/haproxy/bind-and-server-options/) sobre las opciones del servidor

<a id="entry-11-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Esto reactiva una sección peers que fue desactivada previamente mediante la palabra clave
«disabled».

<a id="entry-11-2-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

Las secciones «peers» soportan la misma palabra clave «log» que los proxies para registrar
información sobre el listener «peers». Consulta la opción «log» de los proxies para más detalles.

<a id="entry-11-2-peer"></a>

**`peer <peername> [<address>]:port [param*]`**

```haproxy
peer <peername> [<address>]:port [param*]
peer <peername> /<path> [param*]
```

Define un par dentro de una sección peers. Si `<peername>` se establece al nombre del par local
(por defecto el nombre de host, o forzado mediante la opción de línea de comandos «-L» o el ajuste
de configuración global «localpeer»), HAProxy escuchará conexiones entrantes del par remoto en la
dirección proporcionada. De lo contrario, la dirección define dónde conectarse para unirse al par
remoto, y `<peername>` se usa a nivel de protocolo para identificar y validar el par remoto en el
lado del servidor.

Durante un reinicio suave, la dirección del par local la usa la instancia antigua para conectarse
a la nueva e iniciar una replicación completa (proceso de enseñanza).

Es sumamente recomendable tener exactamente la misma declaración de pares en todos ellos y confiar
únicamente en el argumento de línea de comandos «-L» o en el ajuste de configuración global
«localpeer» para cambiar el nombre del par local. Esto facilita mantener archivos de configuración
coherentes en todos los pares.

Es posible que quieras referenciar algunas variables de entorno en el parámetro de dirección;
consulta la [sección 2.3](/es/haproxy/configuration-basics/#section-2-3) sobre variables de entorno.

Nota: la palabra clave «peer» puede sustituirse de forma transparente por la palabra clave
«server» (consulta la explicación de la palabra clave «server» más abajo).

<a id="entry-11-2-server"></a>

**`server <peername> [<address>:<port>] [param*]`**

```haproxy
server <peername> [<address>:<port>] [param*]
server <peername> [/<path>] [param*]
```

Como se mencionó anteriormente, la palabra clave «peer» puede sustituirse por la palabra clave
«server», con soporte de todos los parámetros «server» del párrafo 5.2 relacionados con los
ajustes de transporte. Si el par subyacente es local, el parámetro de dirección no debe estar
presente; debe proporcionarse en una línea «bind» (consulta la palabra clave «bind» de esta sección
«peers»).

Varios parámetros «server» son irrelevantes para las secciones «peers». Los pares por naturaleza
no soportan la resolución dinámica de nombres de host ni las comprobaciones de estado, por lo que
parámetros como «init_addr», «resolvers», «check», «agent-check» o «track» no están soportados. De
igual modo, no hay balanceo de carga ni persistencia, por lo que parámetros como «weight» o
«cookie» no tienen efecto.

Ejemplo:

```text
 # The old way.
 peers mypeers
     peer haproxy1 192.168.0.1:1024
     peer haproxy2 192.168.0.2:1024
     peer haproxy3 10.2.0.1:1024

 backend mybackend
     mode tcp
     balance roundrobin
     stick-table type ip size 20k peers mypeers
     stick on src

     server srv1 192.168.0.30:80
     server srv2 192.168.0.31:80

Ejemplo:
  peers mypeers
     bind 192.168.0.1:1024 ssl crt mycerts/pem
     default-server ssl verify none
     server haproxy1 #local peer
     server haproxy2 192.168.0.2:1024
     server haproxy3 10.2.0.1:1024
```

shards `<shards>`

En algunas configuraciones, puede quererse distribuir el contenido de la tabla de persistencia a
algunos pares en lugar de enviar todo el contenido de la tabla de persistencia a cada par declarado
en la sección «peers». En tales casos, «shards» especifica el número de pares implicados en esta
distribución del contenido de la tabla de persistencia. Consulta también el parámetro de servidor
«shard».

<a id="entry-11-2-table"></a>

**`table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}`**

```haproxy
table <tablename> type {ip | integer | string [len <length>] | binary [len <length>]}
```

      size `<size>` [expire `<expire>`] [write-to `<wtable>`] [nopurge] [store `<data_type>`]*
      [recv-only]

Configura una tabla de persistencia para la sección actual. Esta línea se analiza exactamente
igual que la palabra clave «stick-table» en otras secciones, salvo por el argumento «peers», que
aquí no es necesario, y con un primer parámetro obligatorio adicional para designar la tabla de
persistencia. Al contrario que en otras secciones, puede haber varias líneas «table» en las
secciones «peers» (consulta también la definición completa de las palabras clave «table» y
«stick-table» en la [sección 11.1](/es/haproxy/stick-tables-and-peers/#section-11-1) más arriba).

Ten presente también el hecho de que las secciones «peers» tienen sus propios espacios de nombres
de tablas de persistencia para evitar colisiones entre nombres de tablas de persistencia
idénticos en diferentes secciones «peers». Esto se gestiona internamente anteponiendo al nombre de cada tabla de persistencia el nombre
de su sección «peers» seguido de un carácter «/». Si
en otra parte del archivo de configuración tienes que referirte a tablas de persistencia
declaradas en secciones «peers», debes usar la versión con prefijo del nombre de la tabla de
persistencia, así:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 ...

frontend fe1
    tcp-request content track-sc0 src table mypeers/t1
```

Es también esta versión con prefijo de los nombres de las tablas de persistencia la que debe
usarse para referirse a las tablas de persistencia a través de la CLI.

Acerca del protocolo «peers», como solo los «peers» pertenecientes a la misma sección pueden
comunicarse entre sí, no hay necesidad de hacer tal distinción. Varias secciones «peers» pueden
declarar tablas de persistencia con el mismo nombre. Es la versión corta del nombre de la tabla de
persistencia la que se envía por la red. Solo hay un carácter «/» como prefijo para evitar
colisiones de nombres entre tablas de persistencia declaradas como backends y tablas de
persistencia declaradas en secciones «peers», como sigue en esta configuración extraña pero
soportada:

```text
peers mypeers
    peer A ...
    peer B ...
    table t1 type string size 10m store gpc0

backend t1
    stick-table type string size 10m store gpc0 peers mypeers
```

Aquí, la tabla «t1» declarada en la sección «mypeers» tiene «mypeers/t1» como nombre global. La
tabla «t1» declarada como backend tiene «t1» como nombre global. Pero a nivel del protocolo de
pares, la primera tabla se llama «/t1», y la segunda se llama de nuevo «t1».
