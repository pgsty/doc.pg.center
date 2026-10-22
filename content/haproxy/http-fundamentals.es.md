---
title: "1. Un breve recordatorio sobre HTTP"
linkTitle: "1. Fundamentos de HTTP"
weight: 120
description: "Transacciones HTTP, solicitudes, respuestas, cabeceras y terminología del protocolo"
icon: fa-solid fa-globe
module: [HAPROXY]
categories: [Concepto]
aliases:
  - /haproxy/configuration/http-fundamentals/
  - /haproxy/configuration/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 1"
---

Este documento cubre el lenguaje de configuración tal como está implementado en la versión indicada anteriormente. No
proporciona ningún consejo, ejemplo o recomendación. Para ese tipo de documentación, consulta el
Manual de referencia o el Manual de arquitectura. Los capítulos numerados están ordenados en la barra lateral plana de HAProxy para una navegación directa.

Cuando HAProxy se ejecuta en modo HTTP, tanto la solicitud como la respuesta se analizan e indexan por completo, por lo que
resulta posible construir criterios de coincidencia sobre casi cualquier elemento presente en los
contenidos.

Sin embargo, es importante comprender cómo se forman las solicitudes y respuestas HTTP, y cómo las descompone
HAProxy. Así resultará más fácil escribir reglas correctas y depurar las configuraciones
existentes.

En primer lugar, HTTP está estandarizado por una serie de RFC que HAProxy sigue tan de cerca como es posible:

- RFC 9110: Semántica HTTP (explica el significado de los elementos del protocolo)
- RFC 9111: Almacenamiento en caché HTTP (explica las reglas a seguir para una caché HTTP)
- RFC 9112: HTTP/1.1 (representación, reglas de interoperabilidad, seguridad)
- RFC 9113: HTTP/2 (representación, reglas de interoperabilidad, seguridad)
- RFC 9114: HTTP/3 (representación, reglas de interoperabilidad, seguridad)

Además de estas, las RFC 8999 a 9002 especifican la capa de transporte QUIC utilizada por el protocolo HTTP/3.

## 1.1. El modelo de transacción HTTP {#section-1-1}

El protocolo HTTP está basado en transacciones. Esto significa que cada solicitud dará lugar a una y solo una
respuesta. Originalmente, con la versión 1.0 del protocolo, había una sola solicitud por conexión: se
establece una conexión TCP desde el cliente hacia el servidor, el cliente envía una solicitud por la
conexión, el servidor responde y la conexión se cierra. Una nueva solicitud implica entonces una nueva
conexión:

```text
[CON1] [REQ1] ... [RESP1] [CLO1] [CON2] [REQ2] ... [RESP2] [CLO2] ...
```

En este modo, a menudo llamado modo «HTTP close», hay tantos establecimientos de conexión como
transacciones HTTP. Dado que la conexión la cierra el servidor después de la respuesta, el
cliente no necesita conocer la longitud del contenido; considera que la respuesta está completa cuando la
conexión se cierra. Esto también significa que si algunas respuestas quedan truncadas debido a errores de red, el
cliente podría pensar erróneamente que una respuesta estaba completa, y esto solía provocar que a veces se
mostraran en pantalla imágenes truncadas.

Debido a la naturaleza transaccional del protocolo, fue posible mejorarlo para evitar cerrar una
conexión entre dos transacciones sucesivas. Sin embargo, en este modo es obligatorio que el
servidor indique la longitud del contenido de cada respuesta para que el cliente no espere indefinidamente.
Para ello se utiliza una cabecera especial: «Content-length». Este modo se llama modo «keep-alive», y
llegó con HTTP/1.1 (algunos agentes HTTP/1.0 lo soportan), y las conexiones que se reutilizan entre
solicitudes se denominan «conexiones persistentes»:

```text
[CON] [REQ1] ... [RESP1] [REQ2] ... [RESP2] [CLO] ...
```

Sus ventajas son una latencia reducida entre transacciones, menos potencia de procesamiento necesaria en el
lado del servidor y la capacidad de detectar una respuesta truncada. Generalmente es más rápido que el modo
close, pero no siempre, porque algunos clientes suelen limitar sus conexiones simultáneas a un valor
menor, y esto compensa en menor medida una conectividad de red deficiente. Además, algunos servidores tienen
que mantener la conexión viva durante mucho tiempo esperando una posible nueva solicitud y pueden sufrir un
uso de memoria elevado debido al alto número de conexiones, y cerrar demasiado rápido puede romper algunas
solicitudes que llegaron en el momento en que la conexión se cerró.

En este modo, el tamaño de la respuesta debe conocerse por adelantado, lo que no siempre es posible con
contenidos generados dinámicamente o comprimidos. Por este motivo se implementó otro modo, el
«modo chunked», en el que, en lugar de anunciar el tamaño total de una sola vez, el emisor solo
anuncia el tamaño del siguiente «fragmento» (chunk) de respuesta que ya tiene en un búfer, y puede terminar en
cualquier momento con un fragmento de tamaño cero. En este modo no se utiliza la cabecera Content-Length.

Otra mejora en las comunicaciones es el modo pipelining. Sigue utilizando keep-alive, pero el
cliente no espera la primera respuesta para enviar la segunda solicitud. Esto es útil para recuperar un
gran número de imágenes que componen una página:

```text
[CON] [REQ1] [REQ2] ... [RESP1] [RESP2] [CLO] ...
```

Esto puede obviamente reportar un beneficio enorme en el rendimiento, porque se elimina la latencia de red
entre solicitudes sucesivas. Muchos agentes HTTP no soportan correctamente el pipelining, dado que
no existe ninguna forma de asociar una respuesta con la solicitud correspondiente en HTTP. Por este motivo, es
obligatorio que el servidor responda en exactamente el mismo orden en que se recibieron las solicitudes. En la
práctica, tras varios intentos de diversos clientes por desplegarlo, ha sido totalmente abandonado por
su falta de fiabilidad en ciertos servidores. Pero es obligatorio que los servidores lo soporten.

La siguiente mejora es el modo multiplexado, tal como está implementado en HTTP/2 y HTTP/3. En este modo,
múltiples transacciones (es decir, pares solicitud-respuesta) se transmiten en paralelo sobre una única
conexión, y todas progresan a su propia velocidad, independientes entre sí. Con los protocolos
multiplexados se introdujo una nueva noción, la de «flujo» (stream), para representar estas comunicaciones
paralelas que ocurren sobre la misma conexión. A cada flujo generalmente se le asigna un identificador único
para una conexión dada, que utilizan ambos extremos para saber dónde entregar los datos. Es bastante común
que los clientes inicien muchos flujos en paralelo (hasta 100, a veces más) sobre una misma
conexión, y dejen que el servidor los ordene y responda en cualquier orden según la respuesta
disponible. El beneficio principal del modo multiplexado es que reduce significativamente el número de
recorridos de ida y vuelta y acelera el tiempo de carga de las páginas en redes de alta latencia. A veces se
nota en sitios que utilizan muchas imágenes, donde todas las imágenes parecen cargarse en paralelo.

Estos protocolos también han mejorado su eficiencia adoptando algunos mecanismos para comprimir los campos
de cabecera con el fin de reducir el número de bytes transmitidos, de modo que, sin las herramientas
adecuadas, no son realistamente manipulables a mano ni legibles a simple vista como lo era HTTP/1. Por este
motivo, diversos ejemplos de mensajes HTTP continúan representándose en la literatura (incluido este
documento) utilizando la sintaxis de HTTP/1 incluso para las versiones más recientes del protocolo.

HTTP/2 sufre algunas limitaciones de diseño, como que las pérdidas de paquetes afectan a todos los flujos a la
vez, y si un cliente tarda demasiado en recuperar un objeto (p. ej., si necesita almacenarlo en disco), puede
ralentizar su recuperación y hacer imposible durante ese tiempo acceder a los datos que quedan pendientes
detrás de él. Esto se denomina «bloqueo de cabecera de fila» (head of line blocking), «HoL blocking», o a
veces simplemente «HoL».

HTTP/3 está implementado sobre QUIC, que a su vez está implementado sobre UDP. QUIC resuelve el bloqueo de
cabecera de fila a nivel de transporte mediante flujos gestionados de forma independiente. En efecto, cuando
se produce una pérdida, un flujo afectado no compromete a los demás flujos, y todos ellos pueden accederse en
paralelo. QUIC también proporciona soporte de migración de conexiones, pero actualmente haproxy no lo
soporta.

Por defecto, HAProxy opera en modo keep-alive con respecto a las conexiones persistentes: para cada
conexión procesa cada solicitud y respuesta, y deja la conexión inactiva en ambos lados
entre el final de una respuesta y el inicio de una nueva solicitud. Cuando recibe conexiones HTTP/2
de un cliente, procesa todas las solicitudes en paralelo y deja la conexión inactiva, esperando
nuevas solicitudes, igual que si fuera una conexión HTTP keep-alive.

HAProxy soporta esencialmente 3 modos de conexión:

- keep alive: se procesan todas las solicitudes y respuestas, y las conexiones orientadas al cliente y al
  servidor se mantienen vivas para nuevas solicitudes. Este es el modo por defecto y se adapta a la web
  moderna y a los protocolos modernos (HTTP/2 y HTTP/3).

- server close: la conexión orientada al servidor se cierra después de la respuesta.

- close: la conexión se cierra activamente tras el final de la respuesta en ambos lados.

Además de esto, por defecto la conexión orientada al servidor es reutilizable por cualquier solicitud de
cualquier cliente, como lo exige la especificación del protocolo HTTP, de modo que cualquier información
relativa a un cliente específico debe transmitirse con cada solicitud si es necesario (p. ej., la dirección
de origen del cliente, etc.). Cuando se utiliza HTTP/2 con un servidor, por defecto HAProxy dedicará esta
conexión al mismo cliente para evitar el riesgo de bloqueo de cabecera de fila entre clientes.

## 1.2. Terminología {#section-1-2}

Dentro de HAProxy, la terminología ha evolucionado un poco a lo largo del tiempo para seguir las evoluciones del
protocolo HTTP y sus usos. Aunque originalmente no había una diferencia significativa entre una conexión,
una sesión, un flujo (stream) o una transacción, estos términos se aclararon con el tiempo para corresponder
estrechamente con lo que existe en las versiones modernas del protocolo HTTP, aunque algunos términos siguen
visibles en la configuración o en la interfaz de línea de comandos con fines de compatibilidad histórica.

Estas son algunas definiciones que se aplican a la versión actual de HAProxy:

- connection: una conexión es un único canal de comunicación bidireccional entre un agente remoto
  (cliente o servidor) y haproxy, en el nivel más bajo posible. Normalmente corresponde a un socket
  TCP establecido entre un par de IP y puertos. En el lado orientado al cliente, las conexiones son las
  primeras entidades que se instancian cuando un cliente se conecta a haproxy, y las reglas que se aplican a
  nivel de conexión son las primeras en aplicarse.

- session: una sesión añade cierta información de contexto asociada a una conexión. Esto incluye
  información específica de la capa de transporte (p. ej., claves TLS, etc.), o variables. Este término se ha
  utilizado durante mucho tiempo dentro de HAProxy para designar las comunicaciones HTTP/1.0 extremo a extremo
  entre dos puntas, y como tal sigue visible en el nombre de ciertos comandos de la CLI o estadísticas, a
  pesar de que hoy en día representa flujos, pero los mensajes de ayuda y las descripciones tratan de evitar
  cualquier ambigüedad. Sigue siendo válido en lo que respecta a la terminología a nivel de red (p. ej.,
  sesiones TCP dentro de los sistemas operativos o sesiones TCP a través de un cortafuegos), o para
  aplicaciones a nivel de usuario no HTTP (p. ej., una sesión de telnet o una sesión SSH). No debe confundirse
  con las «sesiones de aplicación», que se utilizan para almacenar un contexto completo de usuario en una
  cookie y deben enviarse siempre al mismo servidor.

- stream: un flujo corresponde exactamente a una comunicación bidireccional extremo a extremo a
  nivel de aplicación, donde pueden aplicarse análisis y transformaciones. En HTTP, contiene una
  única solicitud y su respuesta asociada, se instancia con la llegada de la solicitud y
  termina con el fin de la entrega de la respuesta. En este contexto existe una relación 1:1 entre
  dicho flujo y el flujo de un protocolo multiplexado. En las comunicaciones TCP hay un único
  flujo por conexión.

- transaction: una transacción es solo un par formado por una solicitud y la respuesta asociada. El término
  se utilizaba junto con las sesiones antes que los flujos, pero hoy en día existe una relación 1:1 entre
  una transacción y un flujo. Es esencialmente visible en el ámbito de las variables «txn», que es válido
  durante toda la transacción y, por tanto, durante todo el flujo.

- solicitud: designa el tráfico que fluye del cliente hacia el servidor. Se utiliza principalmente en
  HTTP para indicar dónde se realizan las operaciones. Este término también existe para las operaciones
  TCP para indicar dónde se procesan los datos. Las solicitudes suelen aparecer en los contadores como
  unidad de tráfico o de actividad. No siempre implican una respuesta (p. ej., por errores), pero dado que no
  existen respuestas espontáneas sin solicitudes, las solicitudes siguen siendo una métrica relevante de la
  actividad global. En TCP hay tantas solicitudes como conexiones.

- respuesta: designa el tráfico que fluye del servidor hacia el cliente, o a veces de HAProxy hacia el
  cliente, cuando HAProxy produce la respuesta por sí mismo (p. ej., una redirección HTTP).

- servicio: generalmente indica cierto procesamiento interno en HAProxy que no requiere un servidor, como
  la página de estadísticas, la caché o algo de código Lua para implementar una pequeña aplicación. Un
  servicio normalmente lee una solicitud, realiza algunas operaciones y produce una respuesta.

## 1.3. Solicitud HTTP {#section-1-3}

En primer lugar, consideremos esta solicitud HTTP:

```text
Número   Contenido
de línea
   1     GET /serv/login.php?lang=en&profile=2 HTTP/1.1
   2     Host: www.mydomain.com
   3     User-agent: my small browser
   4     Accept: image/jpeg, image/gif
   5     Accept: image/png
```

### 1.3.1. La línea de solicitud {#section-1-3-1}

La línea 1 es la «línea de solicitud». Siempre está compuesta por 3 campos:

- un método: GET
- una URI: /serv/login.php?lang=en&profile=2
- una etiqueta de versión: HTTP/1.1

Todos ellos están delimitados por lo que la norma llama LWS (espacios en blanco lineales), que comúnmente
son espacios, pero también pueden ser tabulaciones o saltos de línea/retornos de carro seguidos de
espacios/tabulaciones. El método en sí no puede contener ningún carácter de dos puntos («:») y está limitado
a letras alfabéticas. Todas esas diversas combinaciones hacen deseable que HAProxy realice la división por
sí mismo en lugar de dejar que el usuario escriba una expresión regular compleja o inexacta.

La URI en sí puede tener varias formas:

- Una «URI relativa»:

```text
  /serv/login.php?lang=en&profile=2

Es una URL completa sin la parte del host. Generalmente es lo que
reciben los servidores, los proxies inversos y los proxies transparentes.
```

- Una «URI absoluta», también llamada «URL»:

```text
  http://192.168.0.12:8080/serv/login.php?lang=en&profile=2

Está compuesta por un «esquema» (nombre de protocolo seguido de «://»), un
nombre o dirección de host, opcionalmente dos puntos («:») seguidos de un
número de puerto, y luego una URI relativa que comienza en la primera barra
(«/») después de la parte de la dirección. Generalmente es lo que reciben
los proxies, pero un servidor con soporte de HTTP/1.1 también debe aceptar
esta forma.
```

- una estrella («\*»): esta forma solo se acepta en asociación con el método OPTIONS y no es
  retransmisible. Se utiliza para consultar las capacidades de un siguiente salto.

- una combinación dirección:puerto: 192.168.0.12:80. Se utiliza con el método CONNECT, que sirve
  para establecer túneles TCP a través de proxies HTTP, generalmente para HTTPS, pero a veces también
  para otros protocolos.

En una URI relativa se identifican dos subpartes. La parte anterior al signo de interrogación se llama
«ruta» (path). Suele ser la ruta relativa a los objetos estáticos del servidor. La parte posterior al signo
de interrogación se llama «cadena de consulta» (query string). Se utiliza principalmente con solicitudes GET
enviadas a scripts dinámicos y es muy específica del lenguaje, el framework o la aplicación utilizados.

HTTP/2 y HTTP/3 no transmiten información de versión con la solicitud, por lo que se asume que la versión es
la misma que la del protocolo subyacente (es decir, «HTTP/2»). Además, estos protocolos no
envían la línea de solicitud como una sola parte, sino que la dividen en campos individuales llamados
«pseudo-cabeceras», cuyo nombre comienza por dos puntos, y que HAProxy reensambla convenientemente en una
línea de solicitud equivalente. Por este motivo, las líneas de solicitud que aparecen en los registros pueden
diferir ligeramente entre HTTP/1.x y HTTP/2 o HTTP/3.

### 1.3.2. Las cabeceras de solicitud {#section-1-3-2}

Las cabeceras comienzan en la segunda línea. Se componen de un nombre al principio de la línea,
seguido inmediatamente de un carácter de dos puntos («:»). Tradicionalmente se añade un LWS después de los
dos puntos, pero no es obligatorio. Después vienen los valores. Varias cabeceras idénticas pueden plegarse en
una sola línea, delimitando los valores con comas, siempre que se respete su orden. Esto se encuentra
comúnmente en el campo «Cookie:». Una cabecera puede abarcar varias líneas si las líneas
posteriores comienzan con un LWS. En el ejemplo de 1.3, las líneas 4 y 5 definen un total de 3 valores para
la cabecera «Accept:». Finalmente, todos los LWS al principio o al final de una cabecera se ignoran y no
forman parte del valor, según la especificación.

Contrariamente a una idea errónea común, los nombres de las cabeceras no distinguen mayúsculas de minúsculas,
y sus valores tampoco cuando hacen referencia a otros nombres de cabeceras (como la cabecera «Connection:»).
En HTTP/2 y HTTP/3, los nombres de las cabeceras se envían siempre en minúsculas, como puede verse al ejecutar
en modo de depuración. Internamente, todos los nombres de cabeceras se normalizan a minúsculas para que
HTTP/1.x y HTTP/2 o HTTP/3 utilicen exactamente la misma representación, y se envían tal cual al otro lado.
Esto explica por qué una solicitud HTTP/1.x escrita con notación camel case se entrega en minúsculas.

El final de las cabeceras lo indica la primera línea vacía. La gente suele decir que es un doble
salto de línea, lo cual no es exacto, aunque un doble salto de línea es una forma válida de línea vacía.

Afortunadamente, HAProxy se encarga de todas estas combinaciones complejas al indexar cabeceras, comprobar
valores y contarlos, de modo que no hay motivo para preocuparse por la forma en que puedan estar escritas,
pero es importante no acusar a una aplicación de tener errores si hace cosas inusuales pero válidas.

Nota importante:

```text
Como sugiere la RFC7231, HAProxy normaliza las cabeceras reemplazando los
saltos de línea en medio de las cabeceras por LWS para unir las cabeceras
multilínea. Esto es necesario para un análisis correcto y ayuda a los
analizadores HTTP menos capaces a funcionar correctamente y a no dejarse
engañar por construcciones tan complejas.
```

## 1.4. Respuesta HTTP {#section-1-4}

Una respuesta HTTP se parece mucho a una solicitud HTTP. Ambas se denominan mensajes HTTP. Consideremos
esta respuesta HTTP:

```text
Número   Contenido
de línea
   1     HTTP/1.1 200 OK
   2     Content-length: 350
   3     Content-Type: text/html
```

Como caso especial, HTTP soporta las llamadas «respuestas informativas» como códigos de estado 1xx. Estos
mensajes son especiales porque no transmiten ninguna parte de la respuesta; solo se utilizan como una especie
de mensaje de señalización para pedir, por ejemplo, a un cliente que continúe enviando su solicitud. En el
caso de una respuesta con estado 100, la información solicitada será transportada por el siguiente mensaje de
respuesta que no sea 100 tras la informativa. Esto implica que pueden enviarse varias respuestas a una sola
solicitud y que esto solo funciona cuando keep-alive está activado (los mensajes 1xx aparecieron en
HTTP/1.1). HAProxy gestiona estos mensajes y es capaz de reenviarlos y saltárselos correctamente, procesando
solo la siguiente respuesta que no sea 100. Como tales, estos mensajes ni se registran ni se transforman,
salvo indicación explícita en contrario. Los mensajes de estado 101 indican que el protocolo cambia en la
misma conexión y que HAProxy debe pasar a modo túnel, igual que si hubiera ocurrido un CONNECT. Entonces la
cabecera Upgrade contendría información adicional sobre el tipo de protocolo al que cambia la
conexión.

### 1.4.1. La línea de respuesta {#section-1-4-1}

La línea 1 es la «línea de respuesta». Siempre está compuesta por 3 campos:

- una etiqueta de versión: HTTP/1.1
- un código de estado: 200
- una razón: OK

El código de estado siempre tiene 3 dígitos. El primer dígito indica un estado general:

- 1xx = mensaje informativo que debe omitirse (p. ej. 100, 101)
- 2xx = OK, el contenido continúa a continuación (p. ej. 200, 206)
- 3xx = OK, no continúa contenido (p. ej. 302, 304)
- 4xx = error causado por el cliente (p. ej. 401, 403, 404)
- 5xx = error causado por el servidor (p. ej. 500, 502, 503)

Los códigos de estado mayores que 599 no deben emitirse en las comunicaciones, aunque ciertos agentes pueden
producirlos en los registros para informar de sus estados internos. Consulta la RFC9110 para el significado
detallado de todos estos códigos. HTTP/2 y posteriores no tienen etiqueta de versión y utilizan la
pseudo-cabecera «:status» para informar del código de estado.

El campo «reason» es solo una pista, pero los clientes no lo analizan. Puede encontrarse cualquier cosa,
aunque es práctica común respetar los mensajes bien establecidos. Puede componerse de una o de
varias palabras, como «OK», «Found» o «Authentication Required». No existe en HTTP/2 y
posteriores, ni se emite allí. Cuando una respuesta de HTTP/2 o posterior se transmite a un cliente HTTP/1,
HAProxy producirá un campo reason común que coincide con el código de estado.

HAProxy puede emitir por sí mismo los siguientes códigos de estado:

```text
Cód.  Cuándo / razón
 200  acceso a la página de estadísticas y al responder a solicitudes de monitorización
 301  al realizar una redirección, dependiendo del código configurado
 302  al realizar una redirección, dependiendo del código configurado
 303  al realizar una redirección, dependiendo del código configurado
 307  al realizar una redirección, dependiendo del código configurado
 308  al realizar una redirección, dependiendo del código configurado
 400  por una solicitud inválida o demasiado grande
 401  cuando se requiere autenticación para realizar la acción (al acceder
      a la página de estadísticas)
 403  cuando una solicitud está prohibida por una regla «http-request deny»
 404  cuando no se pudo encontrar el recurso solicitado
 408  cuando expira el tiempo de espera de la solicitud antes de que esta
      esté completa
 410  cuando el recurso solicitado ya no está disponible y no volverá a
      estar disponible
 413  cuando una solicitud HTTP/1.0 GET/HEAD/DELETE lleva una carga útil;
      ver también la opción «h1-accept-payload-with-any-method»
 500  cuando HAProxy encuentra un error interno irrecuperable, como un fallo
      de asignación de memoria, lo cual nunca debería ocurrir
 501 cuando HAProxy no puede atender una solicitud del cliente debido a una
     función no soportada
 502  cuando el servidor devuelve una respuesta vacía, inválida o incompleta,
      o cuando una regla «http-response deny» bloquea la respuesta.
 503  cuando ningún servidor estaba disponible para atender la solicitud, o
      en respuesta a solicitudes de monitorización que coinciden con la
      condición «monitor fail»
 504  cuando expira el tiempo de espera de la respuesta antes de que el
      servidor responda
```

Los códigos de error 4xx y 5xx anteriores pueden personalizarse (consulta «errorloc» en la [sección 4.2](/es/haproxy/proxies/#section-4-2)). Otros códigos de
estado pueden emitirse deliberadamente mediante acciones específicas (consulta, por ejemplo, las acciones «deny», «return» y «redirect»
en la [sección 4.3](/es/haproxy/proxies/#section-4-3)).

### 1.4.2. Las cabeceras de respuesta {#section-1-4-2}

Las cabeceras de respuesta funcionan exactamente igual que las cabeceras de solicitud, por lo que HAProxy utiliza la misma
función de análisis para ambas. Consulta el párrafo 1.3.2 para más detalles.
