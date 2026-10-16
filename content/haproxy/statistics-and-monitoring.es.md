---
title: "9. Estadísticas y monitorización"
linkTitle: "9. Estadísticas y monitorización"
weight: 330
description: "Estadísticas CSV y tipadas, comandos CLI en tiempo de ejecución, CLI maestra y archivos de estadísticas"
icon: fa-solid fa-chart-line
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/management/statistics-and-monitoring/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

Es posible consultar a HAProxy sobre su estado. El mecanismo más utilizado es la página HTTP de
estadísticas. Esta página también expone un formato de salida CSV alternativo para herramientas de
monitorización. El mismo formato se proporciona en el socket Unix.

Las estadísticas se agrupan en categorías denominadas dominios, que corresponden a los múltiples
componentes de HAProxy. Hay dos dominios disponibles: proxy y resolvers. Si no se especifica
ninguno, se selecciona el dominio proxy. Ten en cuenta que en la página HTTP solo se muestran las
estadísticas del proxy.

## 9.1. Formato CSV {#section-9-1}

Las estadísticas pueden consultarse desde el socket Unix o desde la página HTTP. Ambos medios
proporcionan un formato CSV cuyos campos se describen a continuación. La primera línea comienza
con una almohadilla ('#') y tiene una palabra por campo delimitado por comas que representa el
título de la columna. Todas las demás líneas, a partir de la segunda, utilizan un formato CSV
clásico que emplea la coma como delimitador y la comilla doble ('"') como delimitador de texto
opcional, pero solo si el texto encerrado es ambiguo (si contiene una comilla o una coma). El
carácter de comilla doble ('"') en el texto se duplica ('""'), que es el formato que la mayoría
de las herramientas reconocen. No insertes ninguna columna antes de estas para no romper las
herramientas que utilizan posiciones de columnas codificadas de forma fija.

Para las estadísticas de proxy, después de cada nombre de campo se especifican entre corchetes los
tipos que pueden tener un valor para ese campo. Los tipos son L (Listeners), F (Frontends), B
(Backends) y S (Servers). Existe un conjunto fijo de campos estáticos que están siempre disponibles
en el mismo orden. Una columna que contiene el carácter '-' delimita el final de los campos
estáticos; después de ella no se garantiza la presencia ni el orden de los campos.

A continuación se muestra la lista de campos estáticos utilizando el dominio de estadísticas de
proxy:

```text
 0. pxname [LFBS]: nombre del proxy
 1. svname [LFBS]: nombre del servicio (FRONTEND para un frontend, BACKEND para un
    backend, cualquier nombre para servidor/escucha)
 2. qcur [..BS]: peticiones actualmente en cola. Para el backend, informa del
    número de peticiones en cola sin servidor asignado.
 3. qmax [..BS]: valor máximo de qcur
 4. scur [LFBS]: sesiones actuales
 5. smax [LFBS]: número máximo de sesiones
 6. slim [LFBS]: límite de sesiones configurado
 7. stot [LFBS]: número acumulado de sesiones
 8. bin [LFBS]: bytes entrantes
 9. bout [LFBS]: bytes salientes
10. dreq [LFB.]: peticiones rechazadas por motivos de seguridad.
    - En tcp, es porque coincidió una regla tcp-request content.
    - En http, es porque coincidió una regla http-request o tarpit.
11. dresp [LFBS]: respuestas rechazadas por motivos de seguridad.
    - En http, es porque coincidió una regla http-request o
      "option checkcache".
12. ereq [LF..]: errores de petición. Algunas de las causas posibles son:
    - interrupción temprana del cliente, antes de que la petición se haya enviado.
    - error de lectura del cliente
    - timeout del cliente
    - el cliente cerró la conexión
    - diversas peticiones erróneas del cliente.
    - la petición fue sometida a tarpit.
13. econ [..BS]: número de peticiones que encontraron un error al intentar
    conectarse a un servidor del backend. La estadística del backend es la suma
    de la estadística de todos los servidores de ese backend, más los errores
    de conexión no asociados a un servidor en particular (por ejemplo, que el
    backend no tenga servidores activos).
14. eresp [..BS]: errores de respuesta. srv_abrt también se cuenta aquí.
    Otros errores son:
    - error de escritura en el socket del cliente (no se cuenta para la
      estadística del servidor)
    - fallo al aplicar filtros a la respuesta.
15. wretr [..BS]: número de veces que se reintentó una conexión a un servidor.
16. wredis [..BS]: número de veces que una petición fue reenviada a otro
    servidor. El valor del servidor cuenta el número de veces que se dejó
    de usar ese servidor.
17. status [LFBS]: estado (UP/DOWN/NOLB/MAINT/MAINT(via)/MAINT(resolution)...)
18. weight [..BS]: peso efectivo total (backend), peso efectivo (servidor)
19. act [..BS]: número de servidores activos (backend), el servidor está activo (servidor)
20. bck [..BS]: número de servidores de respaldo (backend), el servidor es de respaldo (servidor)
21. chkfail [...S]: número de comprobaciones fallidas. (Solo cuenta las comprobaciones
    fallidas cuando el servidor está disponible.)
22. chkdown [..BS]: número de transiciones UP->DOWN. El contador del backend
    cuenta las transiciones a todo el backend caído, en lugar de la suma de
    los contadores de cada servidor.
23. lastchg [..BS]: número de segundos desde la última transición UP<->DOWN
24. downtime [..BS]: tiempo de inactividad total (en segundos). El valor para el
    backend es el tiempo de inactividad de todo el backend, no la suma de los
    tiempos de inactividad de los servidores.
25. qlimit [...S]: maxqueue configurado para el servidor, o nada si el
    valor es 0 (por defecto, es decir, sin límite)
26. pid [LFBS]: id del proceso (0 para la primera instancia, 1 para la segunda, ...)
27. iid [LFBS]: id único del proxy
28. sid [L..S]: id del servidor (único dentro de un proxy)
29. throttle [...S]: porcentaje de limitación actual del servidor, cuando
    slowstart está activo, o sin valor si no está en slowstart.
30. lbtot [..BS]: número total de veces que se seleccionó un servidor, ya sea
    para nuevas sesiones o al reenviar. El contador del servidor es el número
    de veces que se seleccionó ese servidor.
31. tracked [...S]: id del proxy/servidor si el seguimiento está activado.
32. type [LFBS]: (0=frontend, 1=backend, 2=server, 3=socket/listener)
33. rate [.FBS]: número de sesiones por segundo durante el último segundo transcurrido
34. rate_lim [.F..]: límite configurado de nuevas sesiones por segundo
35. rate_max [.FBS]: número máximo de nuevas sesiones por segundo
36. check_status [...S]: estado de la última comprobación de estado, uno de:
       UNK     -> desconocido
       INI     -> inicializando
       SOCKERR -> error de socket
       L4OK    -> comprobación superada en la capa 4, sin pruebas de capas superiores
                  activadas
       L4TOUT  -> timeout en las capas 1-4
       L4CON   -> problema de conexión en las capas 1-4, por ejemplo
                  "Connection refused" (tcp rst) o "No route to host" (icmp)
       L6OK    -> comprobación superada en la capa 6
       L6TOUT  -> timeout en la capa 6 (SSL)
       L6RSP   -> respuesta no válida en la capa 6 - error de protocolo
       L7OK    -> comprobación superada en la capa 7
       L7OKC   -> comprobación superada condicionalmente en la capa 7, por
                  ejemplo 404 con disable-on-404
       L7TOUT  -> timeout en la capa 7 (HTTP/SMTP)
       L7RSP   -> respuesta no válida en la capa 7 - error de protocolo
       L7STS   -> error de respuesta en la capa 7, por ejemplo HTTP 5xx
    Nota: si hay una comprobación en ejecución, se reportará el último estado
    conocido, precedido de "* ", p. ej. "* L7OK".
37. check_code [...S]: código de las capas 5-7, si está disponible
38. check_duration [...S]: tiempo en ms que tomó terminar la última comprobación de estado
39. hrsp_1xx [.FBS]: respuestas http con código 1xx
40. hrsp_2xx [.FBS]: respuestas http con código 2xx
41. hrsp_3xx [.FBS]: respuestas http con código 3xx
42. hrsp_4xx [.FBS]: respuestas http con código 4xx
43. hrsp_5xx [.FBS]: respuestas http con código 5xx
44. hrsp_other [.FBS]: respuestas http con otros códigos (error de protocolo)
45. hanafail [...S]: detalles de las comprobaciones de estado fallidas
46. req_rate [.F..]: peticiones HTTP por segundo durante el último segundo transcurrido
47. req_rate_max [.F..]: número máximo observado de peticiones HTTP por segundo
48. req_tot [.FB.]: número total de peticiones HTTP recibidas
49. cli_abrt [..BS]: número de transferencias de datos abortadas por el cliente
50. srv_abrt [..BS]: número de transferencias de datos abortadas por el servidor
    (incluido en eresp)
51. comp_in [.FB.]: número de bytes de respuesta HTTP suministrados al compresor
52. comp_out [.FB.]: número de bytes de respuesta HTTP emitidos por el compresor
53. comp_byp [.FB.]: número de bytes que eludieron el compresor HTTP
    (límite de CPU/BW)
54. comp_rsp [.FB.]: número de respuestas HTTP que fueron comprimidas
55. lastsess [..BS]: número de segundos desde la última sesión asignada al
    servidor/backend
56. last_chk [...S]: contenido de la última comprobación de estado o error textual
57. last_agt [...S]: contenido de la última comprobación de agente o error textual
58. qtime [..BS]: tiempo medio en cola, en ms, sobre las últimas 1024 peticiones
59. ctime [..BS]: tiempo medio de conexión, en ms, sobre las últimas 1024 peticiones
60. rtime [..BS]: tiempo medio de respuesta, en ms, sobre las últimas 1024 peticiones
    (0 para TCP)
61. ttime [..BS]: tiempo medio total de sesión, en ms, sobre las últimas 1024
    peticiones
62. agent_status [...S]: estado de la última comprobación de agente, uno de:
       UNK     -> desconocido
       INI     -> inicializando
       SOCKERR -> error de socket
       L4OK    -> comprobación superada en la capa 4, sin pruebas de capas superiores
                  activadas
       L4TOUT  -> timeout en las capas 1-4
       L4CON   -> problema de conexión en las capas 1-4, por ejemplo
                  "Connection refused" (tcp rst) o "No route to host" (icmp)
       L7OK    -> el agente reportó "up"
       L7STS   -> el agente reportó "fail", "stop" o "down"
63. agent_code [...S]: código numérico reportado por el agente, si lo hay (sin uso por ahora)
64. agent_duration [...S]: tiempo en ms que tomó terminar la última comprobación
65. check_desc [...S]: descripción breve legible por humanos de check_status
66. agent_desc [...S]: descripción breve legible por humanos de agent_status
67. check_rise [...S]: parámetro "rise" del servidor usado por las comprobaciones
68. check_fall [...S]: parámetro "fall" del servidor usado por las comprobaciones
69. check_health [...S]: valor de comprobación de estado del servidor, entre 0 y rise+fall-1
70. agent_rise [...S]: parámetro "rise" del agente, normalmente 1
71. agent_fall [...S]: parámetro "fall" del agente, normalmente 1
72. agent_health [...S]: parámetro de estado del agente, entre 0 y rise+fall-1
73. addr [L..S]: address:port o "unix". Una dirección IPv6 lleva corchetes alrededor.
74: cookie [..BS]: valor de cookie del servidor o nombre de cookie del backend
75: mode [LFBS]: modo del proxy (tcp, http, health, unknown)
76: algo [..B.]: algoritmo de balanceo de carga
77: conn_rate [.F..]: número de conexiones durante el último segundo transcurrido
78: conn_rate_max [.F..]: valor máximo conocido de conn_rate
79: conn_tot [.F..]: número acumulado de conexiones
80: intercepted [.FB.]: número acum. de peticiones interceptadas (monitor, stats)
81: dcon [LF..]: peticiones rechazadas por reglas "tcp-request connection"
82: dses [LF..]: peticiones rechazadas por reglas "tcp-request session"
83: wrew [LFBS]: número acumulado de avisos de reescritura de cabecera fallida
84: connect [..BS]: número acumulado de intentos de establecimiento de conexión
85: reuse [..BS]: número acumulado de reutilizaciones de conexión
86: cache_lookups [.FB.]: número acumulado de búsquedas en caché
87: cache_hits [.FB.]: número acumulado de aciertos de caché
88: srv_icur [...S]: número actual de conexiones inactivas disponibles para reutilización
89: src_ilim [...S]: límite del número de conexiones inactivas disponibles
90. qtime_max [..BS]: tiempo máximo observado en cola, en ms
91. ctime_max [..BS]: tiempo máximo observado de conexión, en ms
92. rtime_max [..BS]: tiempo máximo observado de respuesta, en ms (0 para TCP)
93. ttime_max [..BS]: tiempo máximo total observado de sesión, en ms
94. eint [LFBS]: número acumulado de errores internos
95. idle_conn_cur [...S]: número actual de conexiones inactivas no seguras
96. safe_conn_cur [...S]: número actual de conexiones inactivas seguras
97. used_conn_cur [...S]: número actual de conexiones en uso
98. need_conn_est [...S]: número estimado de conexiones necesarias
99. uweight [..BS]: peso de usuario total (backend), peso de usuario del servidor (servidor)
100. agg_server_status [..B.]: medidor agregado del backend del estado de los servidores
101. agg_server_status_check [..B.]: (obsoleto)
102. agg_check_status [..B.]: medidor agregado del backend del estado de las
     comprobaciones de estado de los servidores
103. srid [...S]: revisión del id del servidor
104. sess_other [.F..]: número total de sesiones distintas de HTTP desde que
     empezó el proceso
105. h1_sess [.F..]: número total de sesiones HTTP/1 desde que empezó el proceso
106. h2_sess [.F..]: número total de sesiones HTTP/2 desde que empezó el proceso
107. h3_sess [.F..]: número total de sesiones HTTP/3 desde que empezó el proceso
108. req_other [.F..]: número total de sesiones distintas de HTTP procesadas por
     este objeto desde que empezó el proceso worker
109. h1req [.F..]: número total de sesiones HTTP/1 procesadas por este objeto
     desde que empezó el proceso worker
110. h2req [.F..]: número total de sesiones HTTP/2 procesadas por este objeto
     desde que empezó el proceso worker
111. h3req [.F..]: número total de sesiones HTTP/3 procesadas por este objeto
     desde que empezó el proceso worker
112. proto [L...]: protocolo
113. priv_idle_cur [...S]: número actual de conexiones inactivas privadas
114. reqbin [LFBS]: número total de bytes de petición recibidos desde que
     empezó el proceso worker
115. reqbout [LFBS]: número total de bytes de petición enviados desde que
     empezó el proceso worker
116. resbin [LFBS]: número total de bytes de respuesta recibidos desde que
     empezó el proceso worker
117. resbout [LFBS]: número total de bytes de respuesta enviados desde que
     empezó el proceso worker
```

Para todos los demás dominios de estadísticas no se garantiza la presencia ni el orden de los
campos. En este caso, la línea de cabecera debe usarse siempre para analizar los datos CSV.

## 9.2. Formato de salida tipado {#section-9-2}

Tanto "show info" como "show stat" admiten un modo en el que cada valor de salida viene acompañado
de su tipo y de información suficiente para saber cómo se supone que el valor debe agregarse entre
procesos y cómo evoluciona.

En todos los casos, la salida consiste en un único valor por línea con toda la información dividida
en campos delimitados por dos puntos (':').

La primera columna designa el objeto o métrica que se vuelca. Su formato es específico del comando
que produce esta salida y no se describirá en esta sección. Normalmente consistirá en una serie de
identificadores y nombres de campos.

La segunda columna contiene 4 caracteres que indican respectivamente el origen, la naturaleza, el
ámbito y el estado de persistencia del valor comunicado. El primer carácter (el origen) indica de
dónde se extrajo el valor. Los caracteres posibles son:

```text
M   El valor es una métrica. Es válido en un instante dado y puede cambiar
    según su naturaleza.

S   El valor es un estado. Representa un valor discreto que, por definición,
    no puede agregarse. Puede ser el estado de un servidor ("UP" o "DOWN"),
    el PID del proceso, etc.

K   El valor es una clave de ordenación. Representa un identificador que puede
    usarse para agrupar algunos valores porque es único dentro de su clase.
    Todos los identificadores internos son claves. Algunos nombres pueden
    listarse como claves si son únicos (p. ej., el nombre de un frontend es
    único). En general, las claves vienen de la configuración, aunque algunas
    pueden asignarse automáticamente. Para la mayoría de los fines, las claves
    pueden considerarse equivalentes a la configuración.

C   El valor viene de la configuración. Ciertos valores de configuración tienen
    sentido en la salida, por ejemplo un límite de conexiones simultáneas o un
    nombre de cookie. Por definición, estos valores son los mismos en todos los
    procesos iniciados desde el mismo archivo de configuración.

P   El valor viene del propio producto. Hay muy pocos valores de este tipo; el
    uso más común es reportar el nombre del producto, la versión y la fecha de
    publicación. Estos elementos también son los mismos entre todos los procesos.
```

El segundo carácter (la naturaleza) indica la naturaleza de la información transportada por el
campo, con el fin de permitir que un agregador decida qué operación utilizar para agregar varios
valores. Los caracteres posibles son:

```text
A   El valor representa la antigüedad desde el último evento. Es un poco
    diferente de la duración en que una antigüedad se calcula automáticamente
    en función de la fecha actual. Un ejemplo típico es cuánto tiempo hace que
    ocurrió la última sesión en un servidor. Las antigüedades generalmente se
    agregan tomando el valor mínimo y no necesitan almacenarse.

a   El valor representa un valor ya promediado. Los tiempos de respuesta
    promedio y los pesos de los servidores son de esta naturaleza. Las medias
    normalmente pueden promediarse entre procesos.

C   El valor representa un contador acumulativo. Estas medidas aumentan
    perpetuamente hasta que dan la vuelta. Algunos protocolos de monitorización
    necesitan distinguir entre un contador y un medidor (gauge) para reportar
    un tipo diferente. En general, los contadores pueden simplemente sumarse
    ya que representan eventos o volúmenes. Ejemplos de métricas de esta
    naturaleza son los recuentos de conexiones o de bytes.

D   El valor representa la duración de un estado. Hay pocos usos de esto; la
    mayoría incluyen el tiempo que tomó la última comprobación de estado y el
    tiempo que un servidor ha pasado caído. Las duraciones generalmente no se
    suman; la mayoría de las veces se retendrá el máximo para calcular un SLA.

G   El valor representa un medidor (gauge). Es una medida en un instante. El
    uso de memoria o el número actual de conexiones activas son de esta
    naturaleza. Las métricas de este tipo normalmente se suman durante la
    agregación.

L   El valor representa un límite (generalmente configurado). Por naturaleza,
    los límites son más difíciles de agregar ya que son específicos del punto
    donde se recuperaron. En ciertas situaciones pueden sumarse o mantenerse
    separados.

M   El valor representa un máximo. En general se aplicará a un medidor y
    conservará el valor más alto conocido. Un ejemplo de una métrica así
    podría ser la cantidad máxima de conexiones simultáneas que se encontró
    durante la vida del producto. Para agregar correctamente los máximos, se
    espera que emitas un rango que vaya desde el máximo de todos los máximos
    hasta la suma de todos ellos. En efecto, no hay forma de saber si se
    encontraron simultáneamente o no.

m   El valor representa un mínimo. En general se aplicará a un medidor y
    conservará el valor más bajo conocido. Un ejemplo de una métrica así
    podría ser la cantidad mínima de pools de memoria libres que se encontró
    durante la vida del producto. Para agregar correctamente los mínimos, se
    espera que emitas un rango que vaya desde el mínimo de todos los mínimos
    hasta la suma de todos ellos. En efecto, no hay forma de saber si se
    encontraron simultáneamente o no.

N   El valor representa un nombre, por lo que es una cadena. Se usa para
    reportar nombres de proxies, de servidores y de cookies. Los nombres
    tienen como origen la configuración o claves y se supone que son los
    mismos en todos los procesos.

O   El valor representa una salida de texto libre. Las salidas de diversos
    comandos, los resultados de las comprobaciones de estado y las
    descripciones de nodos son de tal naturaleza.

R   El valor representa una tasa de eventos. Es una medida en un instante. Es
    bastante similar a un medidor, excepto que el destinatario sabe que esta
    medida se mueve lentamente y puede decidir no conservar todos los valores.
    Un ejemplo de una métrica así es la cantidad medida de conexiones por
    segundo. Las métricas de este tipo normalmente se suman durante la
    agregación.

T   El valor representa una fecha u hora. Un campo que emita la fecha actual
    sería de este tipo. El método para agregar tal información se deja como
    una elección de implementación. Por ahora ningún campo usa este tipo.
```

El tercer carácter (el ámbito) indica qué extensión refleja el valor. Algunos elementos pueden ser
por proceso mientras que otros pueden ser por configuración o por sistema. La distinción es
importante para saber si debe conservarse un único valor durante la agregación o si los valores
deben agregarse. Actualmente se admiten los siguientes caracteres:

```text
C   El valor es válido para todo un clúster de nodos, que es el conjunto de
    nodos que se comunican mediante el protocolo peers. Un ejemplo podría ser
    la cantidad de entradas presentes en una stick-table replicada con otros
    pares. En este momento ninguna métrica usa este ámbito.

P   El valor es válido solo para el proceso que lo reporta. La mayoría de las
    métricas usan este ámbito.

S   El valor es válido para todo el servicio, que es el conjunto de procesos
    iniciados juntos desde el mismo archivo de configuración. Todas las
    métricas que se originan en la configuración usan este ámbito. Algunas
    otras métricas también pueden usarlo para algunos recursos compartidos
    (p. ej., estadísticas de caché SSL compartida).

s   El valor es válido para todo el sistema, como el nombre de host del
    sistema, la fecha actual o el uso de recursos. En este momento este ámbito
    no lo usa ninguna métrica.
```

El cuarto carácter (estado de persistencia) indica si el valor (la métrica) es volátil o persistente
entre recargas. Se esperan los siguientes caracteres:

```text
V   La métrica es volátil porque es local al proceso actual, por lo que el
    valor se perderá al recargar.

P   La métrica es persistente porque puede compartirse con otros coprocesos,
    de modo que el valor se conserva entre recargas.
```

Los consumidores de esta información generalmente tendrán suficiente con estos 4 caracteres para
determinar cómo informar con precisión la información agregada de múltiples procesos.

Después de esta columna, la tercera columna indica el tipo del campo, entre "s32" (entero con signo
de 32 bits), "s64" (entero con signo de 64 bits), "u32" (entero sin signo de 32 bits), "u64"
(entero sin signo de 64 bits), "str" (cadena). Es importante conocer el tipo antes de analizar el
valor para leerlo correctamente. Por ejemplo, una cadena que contiene solo dígitos sigue siendo una
cadena y no un entero (por ejemplo: un código de error extraído por una comprobación).

A continuación, la cuarta columna es el valor en sí, codificado según su tipo. Las cadenas se
vuelcan tal cual inmediatamente después de los dos puntos sin ningún espacio inicial. Si una cadena
contiene dos puntos, aparecerá con normalidad. Esto significa que la salida no debe dividirse
exclusivamente por los dos puntos, o algunas salidas de comprobaciones o direcciones de servidor
podrían quedar truncadas.

## 9.3. Comandos del socket Unix {#section-9-3}

El socket de estadísticas no está activado por defecto. Para activarlo es necesario añadir una línea
en la sección global de la configuración de haproxy. Se recomienda una segunda línea para
establecer un timeout mayor, siempre apreciado cuando se emiten comandos a mano:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats timeout 2m
```

También es posible añadir múltiples instancias del socket de estadísticas repitiendo la línea, y
hacer que escuchen en un puerto TCP en lugar de en un socket UNIX. Esto nunca se hace por defecto
porque es peligroso, pero puede resultar práctico en algunas situaciones:

```text
global
    stats socket /var/run/haproxy.sock mode 600 level admin
    stats socket ipv4@192.168.0.1:9999 level admin
    stats timeout 2m
```

Para acceder al socket se requiere una utilidad externa como "socat". Socat es una navaja suiza
para conectar cualquier cosa con cualquier cosa. Lo usamos para conectar terminales al socket, o un
par de tuberías stdin/stdout a él para los scripts. Las dos sintaxis principales que usaremos son
las siguientes:

```shell
# socat /var/run/haproxy.sock stdio
# socat /var/run/haproxy.sock readline
```

La primera se usa con scripts. Es posible enviar la salida de un script a haproxy y pasar la salida
de haproxy a otro script. Esto es útil, por ejemplo, para recuperar contadores o trazas de ataques.

La segunda solo es útil para emitir comandos a mano. Tiene la ventaja de que el terminal es
gestionado por la biblioteca readline, que admite edición de líneas e historial, lo cual es muy
conveniente al emitir comandos repetidos (por ejemplo: observar un contador).

El socket admite tres modos de funcionamiento:

- no interactivo, silencioso
- interactivo, silencioso
- interactivo con prompt

El modo no interactivo es el predeterminado cuando socat se conecta al socket. En este modo puede
enviarse una sola línea. Se procesa en su totalidad, se devuelven las respuestas y la conexión se
cierra tras el final de la respuesta. Este es el modo que usan los scripts y las herramientas de
monitorización. Es posible enviar varios comandos en este modo; deben estar delimitados por un
punto y coma (';'). Por ejemplo:

```shell
# echo "show info;show stat;show table" | socat /var/run/haproxy stdio
```

Si un comando necesita usar un punto y coma o una barra invertida (por ejemplo, en un valor), debe
precederse de una barra invertida ('&#92;').

El modo interactivo permite enviar nuevos comandos después de que terminen los de las líneas
anteriores. Existe en dos variantes: una silenciosa, que funciona como el modo no interactivo salvo
porque el socket espera un nuevo comando en lugar de cerrarse, y otra en la que se muestra un
prompt ('\>') al principio de la línea. El modo interactivo es el preferido para las herramientas
avanzadas, mientras que el modo prompt es el preferido para los humanos.

El modo puede cambiarse con el comando "prompt". Por defecto, alterna los modos interactivo+prompt.
Introducir "prompt" en modo interactivo cambia al modo prompt. El comando acepta opcionalmente un
modo específico entre los siguientes:

- "n": modo no interactivo (un solo comando y sale)
- "i": modo interactivo (múltiples comandos, sin prompt)
- "p": modo prompt (múltiples comandos con prompt)

Dado que el modo predeterminado es el no interactivo, "prompt" debe usarse como primer comando para
cambiarlo; de lo contrario, el comando anterior provocará el cierre de la conexión. Cambiar al modo
no interactivo hará que la conexión se cierre después de que se completen todos los comandos de la
misma línea.

Por esta razón, al depurar a mano, es bastante común comenzar con el comando "prompt":

```haproxy
# socat /var/run/haproxy readline
prompt
```

> show info ...

Las herramientas interactivas podrían preferir comenzar con "prompt i" para cambiar al modo
interactivo sin el prompt.

Opcionalmente puede mostrarse el tiempo de actividad del proceso en el prompt. Para activarlo, el
comando "prompt timed" activará el prompt y alternará la visualización del tiempo de actividad. El tiempo de
actividad se muestra en el formato "d:hh:mm:ss", donde "d" es el número de días y "hh", "mm", "ss"
son respectivamente el número de horas, minutos y segundos, cada uno con dos dígitos:

```haproxy
# socat /var/run/haproxy readline
prompt timed
```

[23:03:34:39]\> show version 2.8-dev9-e5e622-18

[23:03:34:41]\> quit

Cuando el prompt temporizado está activado en la CLI maestra, el prompt mostrará el tiempo de
actividad del proceso actualmente seleccionado, por lo que esto funcionará para el maestro, el
worker actual o un worker más antiguo:

```shell
master> prompt timed
[0:00:00:50] master> show proc
(...)
[0:00:00:58] master> @!11955     <-- maestro, cambio al worker actual
[0:00:01:03] 11955> @!11942      <-- worker actual, cambio a un worker más antiguo
[0:00:02:17] 11942> @            <-- worker más antiguo, vuelta al maestro
[0:00:01:10] master>
```

Dado que pueden emitirse varios comandos a la vez, haproxy usa la línea vacía como delimitador para
marcar el fin de la salida de cada comando, y se encarga de garantizar que ningún comando pueda
emitir una línea vacía en la salida. Así, un script puede analizar fácilmente la salida incluso
cuando se han encadenado múltiples comandos en una sola línea.

Algunos comandos pueden aceptar un payload opcional. Para añadir uno a un comando, la primera línea
debe terminar con el patrón "\<\<&#92;n". Las líneas siguientes se tratarán como el payload
y pueden contener tantas líneas como sea necesario. Para validar un comando con un payload, debe
terminar con una línea vacía.

El patrón del payload puede personalizarse para cambiar la forma en que termina el payload. Para
terminar un payload con algo distinto de una línea vacía, puede establecerse un patrón
personalizado entre '\<\<' y '&#92;n'. Pueden usarse hasta 64 caracteres además de '\<\<'; de lo
contrario, esto no se considerará un payload. Debería ser suficiente para usar patrones de payload
aleatorios. Por ejemplo, para usar un archivo PEM que contiene líneas vacías y comentarios:

```haproxy
# echo -e "set ssl cert common.pem <<%EOF%\n$(cat common.pem)\n%EOF%\n" | \
socat /var/run/haproxy.stat -
```

Existen limitaciones: el patrón "\<\<" no debe estar pegado a la última palabra de la línea. La
longitud de una línea de comando no debe ser mayor que tune.bufsize, incluyendo el patrón que inicia
el payload, pero excluyendo el payload en sí. El tamaño del payload está limitado a 128KB por
defecto. Esto puede cambiarse estableciendo el parámetro global "tune.cli.max-payload-size", con
algunas precauciones. Ten en cuenta que el patrón que marca el final del payload forma parte de este
límite.

Al introducir un payload en modo interactivo, el prompt cambiará de "\> " a "+ ".

Es importante entender que cuando se inician múltiples procesos de haproxy en los mismos sockets,
cualquier proceso puede recoger la petición y mostrará sus propias estadísticas.

A continuación se proporciona la lista de comandos admitidos actualmente en el socket de
estadísticas. Si se envía un comando desconocido, haproxy muestra el mensaje de uso que recuerda
todos los comandos admitidos. Algunos comandos admiten una sintaxis más compleja; generalmente
explicará qué parte del comando no es válida cuando esto ocurre.

Algunos comandos requieren un nivel de privilegios superior para funcionar. Si no tienes
suficientes privilegios, obtendrás un error "Permission denied". Consulta la opción "level" de las
líneas de la palabra clave "bind" en el manual de configuración para más información.

<a id="entry-9-3-abort-ssl-ca-file"></a>

**`abort ssl ca-file <cafile>`**

```haproxy
abort ssl ca-file <cafile>
```

Aborta y destruye una transacción de actualización temporal de un archivo CA.

Ver también "set ssl ca-file" y "commit ssl ca-file".

<a id="entry-9-3-abort-ssl-cert"></a>

**`abort ssl cert <filename>`**

```haproxy
abort ssl cert <filename>
```

Aborta y destruye una transacción de actualización temporal de un certificado SSL.

Ver también "set ssl cert" y "commit ssl cert".

<a id="entry-9-3-abort-ssl-crl-file"></a>

**`abort ssl crl-file <crlfile>`**

```haproxy
abort ssl crl-file <crlfile>
```

Aborta y destruye una transacción de actualización temporal de un archivo CRL.

Ver también "set ssl crl-file" y "commit ssl crl-file".

<a id="entry-9-3-acme-renew"></a>

**`acme renew <certificate>`**

```haproxy
acme renew <certificate>
```

Inicia una tarea de generación de certificado ACME con el nombre de certificado dado. El
certificado debe estar vinculado a una sección acme; consulta la [sección
12.8](/es/haproxy/other-sections/#section-12-8) "ACME" del manual de configuración. Ver también
"acme status".

<a id="entry-9-3-acme-status"></a>

**`acme status`**

```haproxy
acme status
```

Muestra el estado de todos los certificados que fueron configurados con ACME.

Este comando muestra, separado por un tabulador:

- El nombre del certificado configurado en haproxy
- La sección acme utilizada en la configuración
- El estado de la tarea acme: "Running", "Scheduled" o "Stopped"
- La fecha de caducidad UTC del certificado en formato ISO8601
- El tiempo relativo hasta la caducidad (0d si ya caducó)
- La fecha programada UTC del certificado en formato ISO8601
- El tiempo relativo hasta la programación (0d si está en Running)

Ejemplo:

```shell
$ echo "@1; acme status" | socat /tmp/master.sock - | column -t -s $'\t'
# certificate   section  state      expiration date (UTC)  expires in        scheduled date (UTC)  scheduled in
ecdsa.pem       LE       Running    2020-01-18T09:31:12Z   0d 0h00m00s       2020-01-15T21:31:12Z  0d 0h00m00s
foobar.pem.rsa  LE       Scheduled  2025-08-04T11:50:54Z   89d 23h01m13s     2025-07-27T23:50:55Z  82d 11h01m14s
```

<a id="entry-9-3-add-acl"></a>

**`add acl [@<ver>] <acl> <pattern>`**

```haproxy
add acl [@<ver>] <acl> <pattern>
```

Añade una entrada en la ACL `<acl>`. `<acl>` es el \#`<id>` o el `<name>` devuelto por "show acl".
Este comando no verifica si la entrada ya existe. Las entradas se añaden a la versión actual de la
ACL, salvo que se especifique una versión concreta con "@`<ver>`". Este número de versión debe
haber sido asignado previamente por "prepare acl" y estará comprendido entre las versiones
indicadas en "curr_ver" y "next_ver" en la salida de "show acl". Las entradas añadidas con un
número de versión específico no producirán coincidencias hasta que se realice sobre ellas una
operación "commit acl". Sin embargo, pueden consultarse con el comando "show acl @`<ver>`" y
borrarse con un comando "clear acl @`<ver>`". Este comando no puede usarse si la referencia
`<acl>` es un nombre también utilizado con un mapa. En este caso, debe usarse en su lugar el
comando "add map".

<a id="entry-9-3-add-backend"></a>

**`add backend <name> from <defproxy> [mode <mode>] [guid <guid>]`**

```haproxy
add backend <name> from <defproxy> [mode <mode>] [guid <guid>]
```

Instancia un nuevo proxy backend con el nombre `<name>`.

Solo pueden crearse proxies TCP o HTTP. Todos los ajustes se heredan de la instancia de proxy por
defecto `<defproxy>`. Por defecto, es obligatorio especificar el modo del backend mediante el
argumento del mismo nombre, a menos que `<defproxy>` ya lo defina explícitamente. También es
posible usar un argumento GUID opcional si se desea.

Los servidores pueden añadirse mediante el comando "add server". El backend se inicializa en el
estado no publicado. Una vez que se considere listo para el tráfico, usa "publish backend" para
exponer la instancia recién creada.

Pueden usarse todos los proxies por defecto con nombre, siempre que validen las mismas reglas de
herencia aplicadas durante el análisis de la configuración. Hay algunas excepciones, sin embargo,
por ejemplo cuando el modo no es ni TCP ni HTTP.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-add-map"></a>

**`add map [@<ver>] <map> <key> <value>`**

```haproxy
add map [@<ver>] <map> <key> <value>
add map [@<ver>] <map> <payload>
```

Añade una entrada en el mapa `<map>` para asociar el valor `<value>` a la clave `<key>`. Este
comando no verifica si la entrada ya existe. Se usa principalmente para rellenar un mapa después de
una operación "clear" o "prepare". Las entradas se añaden a la versión actual de la ACL, salvo que
se especifique una versión concreta con "@`<ver>`". Este número de versión debe haber sido asignado
previamente por "prepare acl" y estará comprendido entre las versiones indicadas en "curr_ver" y
"next_ver" en la salida de "show acl". Las entradas añadidas con un número de versión específico no
producirán coincidencias hasta que se realice sobre ellas una operación "commit map". Sin embargo,
pueden consultarse con el comando "show map @`<ver>`" y borrarse con un comando "clear acl
@`<ver>`". Si el mapa designado también se usa como una ACL, la ACL solo coincidirá con la parte
`<key>` e ignorará la parte `<value>`. Usando la sintaxis de payload es posible añadir múltiples
pares clave/valor introduciéndolos en líneas separadas. En cada línea nueva, la primera palabra es
la clave y el resto de la línea se considera el valor, que incluso puede contener espacios.

Ejemplo:

```shell
# socat /tmp/sock1 -
prompt

> add map #-1 <<
+ key1 value1
+ key2 value2 with spaces
+ key3 value3 also with spaces
+ key4 value4

>
```

<a id="entry-9-3-add-server"></a>

**`add server <backend>/<server> [args]*`**

```haproxy
add server <backend>/<server> [args]*
```

Instancia un nuevo servidor adjunto al backend `<backend>`.

El nombre `<server>` no debe estar ya en uso en el backend. Se aplica una restricción especial al
backend, que debe usar un algoritmo de balanceo de carga dinámico. Puede usarse un subconjunto de
palabras clave de la declaración server del archivo de configuración para configurar el
comportamiento del servidor (consulta "add server help" para listarlas). Ten en cuenta también que
no se reutilizará ningún ajuste de una hipotética declaración 'default-server' en el mismo backend.

Actualmente, un servidor dinámico se inicializa estáticamente con el método init-addr "none". Esto
significa que no se realizará ninguna resolución si se especifica un FQDN como dirección, aunque la
creación del servidor se valide.

Para admitir las operaciones de recarga, se espera que el servidor creado vía CLI también se
inserte manualmente en el archivo de configuración de haproxy correspondiente. Un servidor dinámico
no presente en la configuración no será restaurado después de una operación de recarga.

Un servidor dinámico puede usar la palabra clave "track" para seguir el estado de las
comprobaciones de otro servidor de la configuración. Sin embargo, no es posible hacer seguimiento
de otro servidor dinámico. Esto es para garantizar que la cadena de seguimiento se mantenga
coherente incluso en caso de eliminación de servidores dinámicos.

Usa la palabra clave "check" para activar el soporte de comprobaciones de estado. Ten en cuenta que
la comprobación de estado está desactivada por defecto y debe activarse de forma independiente del
servidor mediante el comando "enable health". Para las comprobaciones de agente, usa la palabra
clave "agent-check" y el comando "enable agent". Ten en cuenta que en este caso el servidor puede
activarse vía agente dependiendo del estado comunicado, sin un comando "enable server" explícito.
Esto también significa que se requiere especial cuidado al eliminar un servidor dinámico con
comprobación de agente. El agente debe desactivarse primero mediante "disable agent" para poder
poner el servidor en el modo de mantenimiento requerido antes de eliminarlo.

Es posible alcanzar el límite de descriptores (fd) al usar un gran número de servidores dinámicos.
Consulta en este caso la documentación de la palabra clave global "u-limit".

<a id="entry-9-3-add-server-help"></a>

**`add server help`**

```haproxy
add server help
```

Lista las palabras clave admitidas para servidores dinámicos por la versión actual de haproxy. La
sintaxis de las palabras clave es similar a la línea server del archivo de configuración; consulta
su documentación individual para más detalles.

<a id="entry-9-3-add-ssl-ca-file"></a>

**`add ssl ca-file <cafile> <payload>`**

```haproxy
add ssl ca-file <cafile> <payload>
```

Añade un certificado nuevo a un ca-file. Este comando es útil cuando se alcanza el límite de tamaño
del búfer en la CLI y se quieren añadir múltiples certificados. En lugar de hacer un "set" con
todos los certificados, puedes añadir cada certificado individualmente. Un "set ssl ca-file"
restablece el ca-file.

Ejemplo:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate1.crt)\n" | \
socat /var/run/haproxy.stat -
echo -e "add ssl ca-file cafile.pem <<\n$(cat intermediate2.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-add-ssl-crt-list"></a>

**`add ssl crt-list <crtlist> <certificate>`**

```haproxy
add ssl crt-list <crtlist> <certificate>
add ssl crt-list <crtlist> <payload>
```

Añade un certificado a una crt-list. También puede usarse para directorios, ya que ahora los
directorios se cargan de la misma forma que las crt-lists. Este comando permite usar un nombre de
certificado como parámetro; para usar opciones o filtros SSL debe enviarse en su lugar una línea de
crt-list como payload. Solo se admite una línea de crt-list en el payload. Este comando cargará el
certificado para todas las líneas bind que usan la crt-list. Para enviar un certificado nuevo a
HAProxy deben usarse los comandos "new ssl cert" y "set ssl cert".

Ejemplo:

```shell
$ echo "new ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo -e "set ssl cert foobar.pem <<\n$(cat foobar.pem)\n" | socat
/tmp/sock1 -
$ echo "commit ssl cert foobar.pem" | socat /tmp/sock1 -
$ echo "add ssl crt-list certlist1 foobar.pem" | socat /tmp/sock1 -

$ echo -e 'add ssl crt-list certlist1 <<\nfoobar.pem [allow-0rtt] foo.bar.com
!test1.com\n' | socat /tmp/sock1 -
```

<a id="entry-9-3-add-ssl-ech"></a>

**`add ssl ech <bind> <payload>`**

```haproxy
add ssl ech <bind> <payload>
```

Añade una clave ECH a una línea `<bind>`. El payload debe estar en el formato PEM for ECH.
(<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

El formato de la línea bind es `<frontend>`/@`<filename>`:`<linenum>` (Ejemplo:
frontend1/@haproxy.conf:19) o `<frontend>`/`<name>` si la línea bind fue nombrada con la palabra
clave "name".

Requiere una versión de OpenSSL que admita ECH y que HAProxy esté compilado con USE_ECH=1. Este
comando solo se admite en una conexión CLI ejecutándose en modo experimental (ver
"experimental-mode on").

Ver también "show ssl ech" y "ech" en la [Sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1) del manual de configuración.

Ejemplo:

```shell
$ openssl ech -public_name foobar.com -out foobar3.com.ech
$ echo -e "experimental-mode on; add ssl ech frontend1/@haproxy.conf:19 <<%EOF%\n$(cat foobar3.com.ech)\n%EOF%\n" | \
  socat /tmp/haproxy.sock -
added a new ECH config to frontend1
```

<a id="entry-9-3-add-ssl-jwt"></a>

**`add ssl jwt <filename>`**

```haproxy
add ssl jwt <filename>
```

Añade un certificado ya cargado a la lista de certificados que pueden usarse para la validación
JWT (ver el conversor "jwt_verify_cert"). Este comando no funciona con transacciones en curso. Ver
también los comandos "del ssl jwt" y "show ssl jwt". Consulta la opción de certificado "jwt" para
más información.

<a id="entry-9-3-clear-counters"></a>

**`clear counters`**

```haproxy
clear counters
```

Borra los valores máximos de los contadores de estadísticas de cada proxy (frontend y backend) y de
cada servidor. Los contadores acumulados no se ven afectados. También se restablecen los contadores
internos de actividad mostrados por "show activity". Puede usarse para obtener contadores limpios
después de un incidente, sin tener que reiniciar ni borrar los contadores de tráfico. Este comando
está restringido y solo puede emitirse en sockets configurados con niveles "operator" o "admin".

<a id="entry-9-3-clear-counters-all"></a>

**`clear counters all`**

```haproxy
clear counters all
```

Borra todos los contadores de estadísticas de cada proxy (frontend y backend) y de cada servidor.
Esto tiene el mismo efecto que reiniciar. Este comando está restringido y solo puede emitirse en
sockets configurados con nivel "admin".

<a id="entry-9-3-clear-acl"></a>

**`clear acl [@<ver>] <acl>`**

```haproxy
clear acl [@<ver>] <acl>
```

Elimina todas las entradas de la ACL `<acl>`. `<acl>` es el \#`<id>` o el `<name>` devuelto por
"show acl". Ten en cuenta que si la referencia `<acl>` es un nombre compartido con un mapa, ese
mapa también se borrará. Por defecto solo se borra la versión actual de la ACL (la que se usa para
las coincidencias). Sin embargo, es posible especificar otra versión usando '@' seguido de esa
versión.

<a id="entry-9-3-clear-map"></a>

**`clear map [@<ver>] <map>`**

```haproxy
clear map [@<ver>] <map>
```

Elimina todas las entradas del mapa `<map>`. `<map>` es el \#`<id>` o el `<name>` devuelto por
"show map". Ten en cuenta que si la referencia `<map>` es un nombre compartido con una ACL, esa ACL
también se borrará. Por defecto solo se borra la versión actual del mapa (la que se usa para las
coincidencias). Sin embargo, es posible especificar otra versión usando '@' seguido de esa versión.

<a id="entry-9-3-clear-table"></a>

**`clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |`**

```haproxy
clear table <table> [ data.<type> <operator> <value> ] | [ key <key> ] |
                    [ ptr <ptr> ]
```

Elimina entradas de la stick-table `<table>`.

Esto se usa típicamente para desbloquear a algunos usuarios que se quejan de que se les ha
denegado el acceso a un servicio de forma abusiva, pero también puede usarse para borrar algunas
entradas de persistencia que coinciden con un servidor que va a ser reemplazado (ver "show table"
más abajo para más detalles). Ten en cuenta que a veces la eliminación de una entrada será
rechazada porque está siendo rastreada por una sesión en ese momento. Bastará normalmente con
reintentarlo unos segundos después de que la sesión termine.

En el caso de que no se den argumentos de opciones, se eliminarán todas las entradas.

Cuando se usa la forma "data.", se eliminan las entradas que coinciden con un filtro aplicado
usando los datos almacenados (ver "stick-table" en la sección 4.2). Debe especificarse un tipo de
datos almacenado en `<type>`, y este tipo de datos debe estar almacenado en la tabla; de lo
contrario se informa de un error. Los datos se comparan según `<operator>` con el entero de 64
bits `<value>`. Los operadores son los mismos que con las ACLs:

    - eq: coincide con entradas cuyos datos son iguales a este valor
    - ne: coincide con entradas cuyos datos no son iguales a este valor
    - le: coincide con entradas cuyos datos son menores o iguales a este valor
    - ge: coincide con entradas cuyos datos son mayores o iguales a este valor
    - lt: coincide con entradas cuyos datos son menores que este valor
    - gt: coincide con entradas cuyos datos son mayores que este valor

Cuando se usa la forma key, se elimina la entrada `<key>`. La clave debe ser del mismo tipo que
la tabla, lo que actualmente se limita a IPv4, IPv6, entero y cadena.

Cuando se usa la forma ptr, se elimina la entrada `<ptr>`. `<ptr>` se escribe en la forma 0xffff y
debe corresponder a la dirección devuelta por un comando "show table" anterior. Identificar una
entrada mediante su puntero puede ser pertinente si la entrada no puede identificarse mediante la
clave debido a una clave vacía o a caracteres incompatibles en la CLI.

Si data.`<type>` es un tipo array, puede usarse "[]" para acceder a un índice específico del
array, así: data.gpt[1]

Ejemplo:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1 \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy key 127.0.0.1" | socat stdio /tmp/sock1

    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200
      bytes_out_rate(60000)=191
    $ echo "clear table http_proxy data.gpc0 eq 1" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:1
>>> 0x80e6b40: key=127.0.0.3 use=0 exp=3594743 gpc0=2 conn_rate(30000)=10 \
      bytes_out_rate(60000)=200

    $ echo "clear table http_proxy ptr 0x80e6b40" | socat stdio /tmp/sock1
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:0
```

<a id="entry-9-3-commit-acl"></a>

**`commit acl @<ver> <acl>`**

```haproxy
commit acl @<ver> <acl>
```

Confirma todos los cambios realizados en la versión `<ver>` de la ACL `<acl>` y elimina todas las
versiones anteriores. `<acl>` es el \#`<id>` o el `<name>` devuelto por "show acl". El número de
versión debe estar entre "curr_ver"+1 y "next_ver" tal como se informa en "show acl". El contenido
que se va a confirmar en la ACL puede consultarse con "show acl @`<ver>` `<acl>`" si se desea. El
número de versión especificado normalmente se habrá creado con el comando "prepare acl". El
reemplazo es atómico. Consiste en actualizar atómicamente la versión actual a la versión
especificada, lo que hará que instantáneamente todas las entradas de otras versiones se vuelvan
invisibles y todas las entradas de la nueva versión se vuelvan visibles. También es posible usar
este comando para realizar una eliminación atómica de todas las entradas visibles de una ACL
llamando primero a "prepare acl" y confirmando después sin añadir ninguna entrada. Este comando no
puede usarse si la referencia `<acl>` es un nombre también utilizado como mapa. En este caso, debe
usarse en su lugar el comando "commit map".

<a id="entry-9-3-commit-map"></a>

**`commit map @<ver> <map>`**

```haproxy
commit map @<ver> <map>
```

Confirma todos los cambios realizados en la versión `<ver>` del mapa `<map>` y elimina todas las
versiones anteriores. `<map>` es el \#`<id>` o el `<name>` devuelto por "show map". El número de
versión debe estar entre "curr_ver"+1 y "next_ver" tal como se informa en "show map". El contenido
que se va a confirmar en el mapa puede consultarse con "show map @`<ver>` `<map>`" si se desea. El
número de versión especificado normalmente se habrá creado con el comando "prepare map". El
reemplazo es atómico. Consiste en actualizar atómicamente la versión actual a la versión
especificada, lo que hará que instantáneamente todas las entradas de otras versiones se vuelvan
invisibles y todas las entradas de la nueva versión se vuelvan visibles. También es posible usar
este comando para realizar una eliminación atómica de todas las entradas visibles de un mapa
llamando primero a "prepare map" y confirmando después sin añadir ninguna entrada.

<a id="entry-9-3-commit-ssl-ca-file"></a>

**`commit ssl ca-file <cafile>`**

```haproxy
commit ssl ca-file <cafile>
```

Confirma una transacción de actualización temporal de un archivo CA SSL.

En el caso de un archivo CA existente (en estado "Used" en "show ssl ca-file"), la nueva entrada
del árbol de archivos CA se inserta en el árbol de archivos CA y cada instancia que usaba la
entrada del archivo CA se reconstruye, junto con los contextos SSL que necesita. Se eliminan todos
los contextos usados previamente por las instancias reconstruidas. En caso de éxito, la entrada
anterior del archivo CA se elimina del árbol. En caso de fallo, no se elimina ni se borra nada, y
todos los contextos SSL originales se conservan y se usan. Una vez confirmada la transacción
temporal, se destruye.

En el caso de un archivo CA nuevo (después de un "new ssl ca-file" y en estado "Unused" en "show
ssl ca-file"), el archivo CA se insertará en el árbol de archivos CA pero no se usará en ningún
lugar de HAProxy. Para usarlo y generar contextos SSL que lo utilicen, tendrás que añadirlo a una
crt-list con "add ssl crt-list".

Ver también "new ssl ca-file", "set ssl ca-file", "add ssl ca-file", "abort ssl ca-file" y "add
ssl crt-list".

<a id="entry-9-3-commit-ssl-cert"></a>

**`commit ssl cert <filename>`**

```haproxy
commit ssl cert <filename>
```

Confirma una transacción de actualización temporal de un certificado SSL.

En el caso de un certificado existente (en estado "Used" en "show ssl cert"), genera todos los
contextos SSL y SNIs que necesita, los inserta y elimina los anteriores. Reemplaza en memoria los
certificados SSL anteriores en todos los lugares donde se usó `<filename>` en la configuración. En
caso de fallo no elimina ni inserta nada. Una vez confirmada la transacción temporal, se destruye.

En el caso de un certificado nuevo (después de un "new ssl cert" y en estado "Unused" en "show ssl
cert"), el certificado se confirmará en un almacenamiento de certificados, pero no se usará en
ningún lugar de haproxy. Para usarlo y generar sus SNIs tendrás que añadirlo a una crt-list o a un
directorio con "add ssl crt-list".

Ver también "new ssl cert", "set ssl cert", "abort ssl cert" y "add ssl crt-list".

<a id="entry-9-3-commit-ssl-crl-file"></a>

**`commit ssl crl-file <crlfile>`**

```haproxy
commit ssl crl-file <crlfile>
```

Confirma una transacción de actualización temporal de un archivo CRL SSL.

En el caso de un archivo CRL existente (en estado "Used" en "show ssl crl-file"), la nueva entrada
del archivo CRL se inserta en el árbol de archivos CA (que contiene tanto los archivos CA como los
archivos CRL) y cada instancia que usaba la entrada del archivo CRL se reconstruye, junto con los
contextos SSL que necesita. Se eliminan todos los contextos usados previamente por las instancias
reconstruidas. En caso de éxito, la entrada anterior del archivo CRL se elimina del árbol. En caso
de fallo, no se elimina ni se borra nada, y todos los contextos SSL originales se conservan y se
usan. Una vez confirmada la transacción temporal, se destruye.

En el caso de un archivo CRL nuevo (después de un "new ssl crl-file" y en estado "Unused" en "show
ssl crl-file"), el archivo CRL se insertará en el árbol de archivos CRL pero no se usará en ningún
lugar de HAProxy. Para usarlo y generar contextos SSL que lo utilicen, tendrás que añadirlo a una
crt-list con "add ssl crt-list".

Ver también "new ssl crl-file", "set ssl crl-file", "abort ssl crl-file" y "add ssl crt-list".

<a id="entry-9-3-debug-counters"></a>

**`debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*`**

```haproxy
debug counters [reset|show|on|off|all|bug|chk|cnt|glt|?]*
```

Lista los contadores internos colocados en el código, que pueden variar según algunas opciones de
compilación. Algunos dependen de DEBUG_STRICT, otros de DEBUG_COUNTERS. El comando toma una
combinación de múltiples argumentos, algunos que definen acciones y otros que definen filtros: -
bug permite listar los contadores de las sentencias BUG_ON() - cnt permite listar los contadores
de las sentencias COUNT_IF() - chk permite listar los contadores de las sentencias CHECK_IF() -
glt permite listar los contadores de las sentencias COUNT_GLITCH() - all permite mostrar los
contadores que nunca se dispararon (valor 0) - acción off: desactiva la actualización de los
contadores COUNT_IF() - acción on: activa la actualización de los contadores COUNT_IF() - acción
reset: restablece todos los contadores especificados - acción show: muestra todos los contadores
especificados

Por defecto, la acción es "show" para mostrar contadores, y los contadores listados son de todos
los tipos con un valor distinto de cero. El comando "show" es implícito cuando no se especifica
otra acción, y solo está presente para facilitar la generación de comandos desde scripts.

La salida comienza con un contador entero, seguido del tipo del contador en mayúsculas, luego su
ubicación en el código (archivo:línea), el nombre de la función y, opcionalmente, ": " seguido de
una descripción. Ten en cuenta que el formato de salida puede cambiar entre versiones principales,
y que se pueden retroportar nuevos tipos y entradas a las versiones estables con el propósito de
mejorar las capacidades de depuración. Cualquier monitorización realizada sobre ellos debería
hacerse solo de una forma muy flexible y permisiva, y preferiblemente no hacerse.

Normalmente, los usuarios finales no usarán este comando, pero un desarrollador puede invitarles a
hacerlo al intentar averiguar la causa de un problema, buscando entradas CNT o GLT. Por cierto, no
se espera que ocurran entradas "CHK" distintas de cero y deberían comunicarse a los desarrolladores,
ya que podrían indicar suposiciones incorrectas en el código.

<a id="entry-9-3-debug-dev"></a>

**`debug dev <command> [args]*`**

```haproxy
debug dev <command> [args]*
```

Llama a un comando específico de desarrolladores. Solo se admite en una conexión CLI ejecutándose
en modo experto (ver "expert-mode on"). Estos comandos son extremadamente peligrosos y no perdonan
errores; cualquier uso indebido puede provocar un fallo del proceso. Están destinados únicamente a
expertos y realmente no deben usarse salvo que se indique lo contrario. Algunos de ellos solo están
disponibles cuando haproxy se compila con DEBUG_DEV definido, porque pueden tener implicaciones de
seguridad. Todos estos comandos requieren privilegios de administrador y están deliberadamente sin
documentar para no fomentar su uso por parte de personas que no están familiarizadas con el código
fuente.

<a id="entry-9-3-del-acl"></a>

**`del acl <acl> [<key>|#<ref>]`**

```haproxy
del acl <acl> [<key>|#<ref>]
```

Elimina todas las entradas de la ACL `<acl>` correspondientes a la clave `<key>`. `<acl>` es el
\#`<id>` o el `<name>` devuelto por "show acl". Si se usa `<ref>`, este comando elimina únicamente
la referencia indicada. La referencia puede encontrarse listando el contenido de la ACL. Ten en
cuenta que si la referencia `<acl>` es un nombre compartido con un mapa, la entrada también se
eliminará en el mapa.

<a id="entry-9-3-del-backend"></a>

**`del backend <name>`**

```haproxy
del backend <name>
```

Elimina el proxy backend con el nombre `<name>`.

Esta operación solo es posible para proxies TCP o HTTP. Para tener éxito, la instancia del backend
debe haberse despublicado primero. Además, todos sus servidores deben eliminarse primero (vía el
comando CLI "del server"). Finalmente, ningún stream debe seguir adjunto a la instancia del
backend.

Existen restricciones adicionales que impiden la eliminación de un backend. Primero, un backend no
puede eliminarse si está referenciado explícitamente por elementos de configuración, por ejemplo
mediante una regla use_backend o en expresiones de muestra (sample). Algunas opciones de proxies
también son incompatibles con la eliminación en tiempo de ejecución. Actualmente, este es el caso
cuando se usan los obsoletos dispatch o option transparent. Además, un backend no puede eliminarse
si hay una stick-table declarada en él. Finalmente, por ahora es imposible eliminar un backend si
había servidores QUIC en él.

Puede ser útil usar "wait be-removable" antes de este comando para comprobar los requisitos antes
mencionados. Esto también proporciona un método para esperar el cierre definitivo de los streams
adjuntos al backend de destino.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-del-map"></a>

**`del map <map> [<key>|#<ref>]`**

```haproxy
del map <map> [<key>|#<ref>]
```

Elimina todas las entradas del mapa `<map>` correspondientes a la clave `<key>`. `<map>` es el
\#`<id>` o el `<name>` devuelto por "show map". Si se usa `<ref>`, este comando elimina únicamente
la referencia indicada. La referencia puede encontrarse listando el contenido del mapa. Ten en
cuenta que si la referencia `<map>` es un nombre compartido con una ACL, la entrada también se
eliminará en el mapa.

<a id="entry-9-3-del-ssl-ca-file"></a>

**`del ssl ca-file <cafile>`**

```haproxy
del ssl ca-file <cafile>
```

Elimina una entrada del árbol de archivos CA de HAProxy. El archivo CA debe estar sin usar y
eliminado de cualquier crt-list. "show ssl ca-file" muestra el estado de los archivos CA. La
eliminación no funciona con un certificado referenciado directamente con las directivas "ca-file" o
"ca-verify-file" en la configuración.

<a id="entry-9-3-del-ssl-cert"></a>

**`del ssl cert <certfile>`**

```haproxy
del ssl cert <certfile>
```

Elimina un almacén de certificados de HAProxy. El certificado no debe usarse (tampoco para la validación JWT) y debe haberse eliminado de cualquier crt-list o directorio. "show ssl cert" muestra el
estado del certificado. La eliminación no funciona con un certificado referenciado directamente con
la directiva "crt" en la configuración.

<a id="entry-9-3-del-ssl-crl-file"></a>

**`del ssl crl-file <crlfile>`**

```haproxy
del ssl crl-file <crlfile>
```

Elimina una entrada del árbol de archivos CRL de HAProxy. El archivo CRL debe estar sin usar y
eliminado de cualquier crt-list. "show ssl crl-file" muestra el estado de los archivos CRL. La
eliminación no funciona con un certificado referenciado directamente con la directiva "crl-file" en
la configuración.

<a id="entry-9-3-del-ssl-crt-list"></a>

**`del ssl crt-list <filename> <certfile[:line]>`**

```haproxy
del ssl crt-list <filename> <certfile[:line]>
```

Elimina una entrada de una crt-list. Esto eliminará todos los SNIs usados para esta entrada en los
frontends. Si un certificado se usa varias veces en una crt-list, tendrás que indicar qué línea
deseas eliminar. Para mostrar los números de línea, usa "show ssl crt-list -n `<crtlist>`".

<a id="entry-9-3-del-ssl-ech"></a>

**`del ssl ech <bind>`**

```haproxy
del ssl ech <bind>
```

Elimina las claves ECH de una línea bind.

El formato de la línea bind es `<frontend>`/@`<filename>`:`<linenum>` (Ejemplo:
frontend1/@haproxy.conf:19) o `<frontend>`/`<name>` si la línea bind fue nombrada con la palabra
clave "name".

Requiere una versión de OpenSSL que admita ECH y que HAProxy esté compilado con USE_ECH=1. Este
comando solo se admite en una conexión CLI ejecutándose en modo experimental (ver
"experimental-mode on").

Ver también "show ssl ech", "add ssl ech" y "ech" en la [Sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1) del manual de configuración.

Ejemplo:

```shell
$ echo "experimental-mode on; del ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
deleted all ECH configs from frontend1/@haproxy.conf:19
```

<a id="entry-9-3-del-ssl-jwt"></a>

**`del ssl jwt <filename>`**

```haproxy
del ssl jwt <filename>
```

Elimina un certificado ya cargado de la lista de certificados que pueden usarse para la validación
JWT (ver el conversor "jwt_verify_cert"). Este comando no funciona con transacciones en curso. Ver
también los comandos "add ssl jwt" y "show ssl jwt". Consulta la opción de certificado "jwt" para
más información.

<a id="entry-9-3-del-server"></a>

**`del server <backend>/<server>`**

```haproxy
del server <backend>/<server>
```

Elimina un servidor eliminable adjunto al backend `<backend>`. Un servidor eliminable es el
servidor que cumple todas estas condiciones:

- no referenciado por otros elementos de configuración
- debe estar ya en mantenimiento (ver "disable server")
- no debe tener ninguna conexión activa ni inactiva

Si no se cumple alguna de estas condiciones, el comando fallará.

Las conexiones activas son aquellas con al menos una petición en curso. Es posible acelerar su
terminación usando "shutdown sessions server". Es muy recomendable usar "wait srv-removable" antes
de "del server" para asegurarse de que todas las conexiones activas o inactivas estén cerradas y de
que el comando tenga éxito.

<a id="entry-9-3-disable-agent"></a>

**`disable agent <backend>/<server>`**

```haproxy
disable agent <backend>/<server>
```

Marca la comprobación auxiliar del agente como detenida temporalmente.

En el caso de que una comprobación de agente se ejecute como comprobación auxiliar, debido al
parámetro agent-check de una directiva server, las nuevas comprobaciones solo se inicializan
cuando el agente está activado. Por lo tanto, disable agent impedirá que se inicien nuevas
comprobaciones de agente hasta que el agente se reactive con enable agent.

Cuando un agente está desactivado, el procesamiento de una comprobación auxiliar de agente que se
inició mientras el agente estaba activado es el siguiente: todos los resultados que alterarían el
peso, específicamente "drain" o un peso devuelto por el agente, se ignoran. El procesamiento de la
comprobación de agente no cambia en lo demás.

La motivación de esta característica es permitir pausar los efectos de cambio de peso de las
comprobaciones del agente, para permitir configurar el peso de un servidor con set weight sin que
el agente lo sobrescriba.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-disable-dynamic-cookie-backend"></a>

**`disable dynamic-cookie backend <backend>`**

```haproxy
disable dynamic-cookie backend <backend>
```

Desactiva la generación de cookies dinámicas para el backend `<backend>`

<a id="entry-9-3-disable-frontend"></a>

**`disable frontend <frontend>`**

```haproxy
disable frontend <frontend>
```

Marca el frontend como detenido temporalmente. Esto corresponde al modo que se usa durante un
reinicio suave: el frontend libera el puerto pero puede activarse de nuevo si es necesario. Debe
usarse con cuidado, ya que algunos sistemas operativos que no son Linux no pueden reactivarlo.
Está pensado para usarse en entornos donde detener un proxy es impensable pero un proxy mal
configurado debe corregirse. De este modo es posible liberar el puerto y enlazarlo en otro proceso
para restaurar las operaciones. El frontend aparecerá con el estado "STOP" en la página de
estadísticas.

El frontend puede especificarse por su nombre o por su ID numérico, precedido de una almohadilla
('#').

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-disable-health"></a>

**`disable health <backend>/<server>`**

```haproxy
disable health <backend>/<server>
```

Marca la comprobación de estado principal como detenida temporalmente. Esto desactivará el envío de
comprobaciones de estado y el último resultado de la comprobación de estado se ignorará. El
servidor quedará en estado sin comprobar y se considerará UP salvo que una comprobación auxiliar de
agente lo fuerce a caer.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-disable-server"></a>

**`disable server <backend>/<server>`**

```haproxy
disable server <backend>/<server>
```

Marca el servidor como DOWN por mantenimiento. En este modo no se realizarán más comprobaciones
sobre el servidor hasta que salga del mantenimiento. Si el servidor es seguido por otros
servidores, esos servidores se pondrán en DOWN durante el mantenimiento.

En la página de estadísticas, un servidor DOWN por mantenimiento aparecerá con el estado "MAINT",
y sus servidores que lo siguen con el estado "MAINT(via)".

Tanto el backend como el servidor pueden especificarse por su nombre o por su ID numérico,
precedido de una almohadilla ('#').

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-dump-ssl-cert"></a>

**`dump ssl cert <certfile>`**

```haproxy
dump ssl cert <certfile>
```

Vuelca un certificado cargado en la memoria de HAProxy. Esto volcará el certificado en formato PEM,
la clave privada, luego el certificado hoja y finalmente se volcará la cadena. También puedes
volcar una transacción prefijando el nombre de archivo con un asterisco. Esto es útil para guardar
certificados en el sistema de archivos cuando se actualizaron en la CLI y no en el sistema de
archivos.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

Ejemplos:

```shell
$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 -

$ echo "dump ssl cert cert1.pem" | socat /tmp/sock1 - | openssl storeutl -noout -text /dev/stdin
```

<a id="entry-9-3-dump-stats-file"></a>

**`dump stats-file`**

```haproxy
dump stats-file
```

Genera un stats-file que puede usarse para precargar los valores de los contadores de haproxy al
arrancar. Consulta la sección "Stats-file" para más detalle.

<a id="entry-9-3-echo"></a>

**`echo <text>`**

```haproxy
echo <text>
```

Imprime texto con la CLI. Puede ser útil para escribir comentarios entre comandos al volcar el
resultado de múltiples comandos.

Ejemplo:

```text
echo "expert-mode on; echo FDs from fdtab; show fd; echo wild FDs; debug dev fd" | socat /var/run/haproxy.sock -

```

<a id="entry-9-3-enable-agent"></a>

**`enable agent <backend>/<server>`**

```haproxy
enable agent <backend>/<server>
```

Reanuda la comprobación auxiliar de agente que fue detenida temporalmente.

Consulta "disable agent" para más detalles sobre el efecto de iniciar y detener temporalmente un
agente auxiliar.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-enable-dynamic-cookie-backend"></a>

**`enable dynamic-cookie backend <backend>`**

```haproxy
enable dynamic-cookie backend <backend>
```

Activa la generación de cookies dinámicas para el backend `<backend>`. También debe proporcionarse
una clave secreta.

<a id="entry-9-3-enable-frontend"></a>

**`enable frontend <frontend>`**

```haproxy
enable frontend <frontend>
```

Reanuda un frontend que fue detenido temporalmente. Es posible que algunos de los puertos de
escucha ya no puedan enlazarse (por ejemplo: si otro proceso los tomó desde la operación 'disable
frontend'). Si esto ocurre, se muestra un error. Algunos sistemas operativos podrían no poder
reanudar un frontend que fue desactivado.

El frontend puede especificarse por su nombre o por su ID numérico, precedido de una almohadilla
('#').

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-enable-health"></a>

**`enable health <backend>/<server>`**

```haproxy
enable health <backend>/<server>
```

Reanuda una comprobación de estado principal que fue detenida temporalmente. Esto volverá a
activar el envío de comprobaciones de estado. Consulta "disable health" para más detalles.

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-enable-server"></a>

**`enable server <backend>/<server>`**

```haproxy
enable server <backend>/<server>
```

Si el servidor fue marcado previamente como DOWN por mantenimiento, esto marca el servidor como UP
y las comprobaciones se reactivan.

Tanto el backend como el servidor pueden especificarse por su nombre o por su ID numérico,
precedido de una almohadilla ('#').

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Sin opciones, indica si el modo experimental está activado o desactivado en la conexión actual.
Cuando se pasa "on", activa el modo experimental solo para la conexión CLI actual. Con "off" lo
desactiva.

El modo experimental se usa para acceder a características adicionales aún en desarrollo. Estas
características actualmente no son estables y deben usarse con cuidado. Pueden estar sujetas a
cambios rupturistas entre versiones.

Cuando se usa desde la CLI maestra, este comando no debe llevar prefijo, ya que establecerá el modo
para cualquier worker al conectarse a su CLI.

Ejemplo:

```text
echo "@1; experimental-mode on; <experimental_cmd>..." | socat /var/run/haproxy.master -
echo "experimental-mode on; @1 <experimental_cmd>..." | socat /var/run/haproxy.master -
```

<a id="entry-9-3-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Este comando es similar a experimental-mode pero se usa para alternar el modo experto.

El modo experto permite mostrar comandos de experto que pueden ser extremadamente peligrosos para
el proceso y que en ocasiones pueden ayudar a los desarrolladores a recopilar información
importante sobre errores complejos. Cualquier uso indebido de estas características probablemente
provoque un fallo del proceso. No uses esta opción sin que se te invite a hacerlo. Ten en cuenta
que este comando deliberadamente no aparece en el mensaje de ayuda. Este comando solo es accesible
con nivel admin. Cambiar a otro nivel restablece automáticamente el modo experto.

Cuando se usa desde la CLI maestra, este comando no debe llevar prefijo, ya que establecerá el modo
para cualquier worker al conectarse a su CLI.

Ejemplo:

```text
echo "@1; expert-mode on; debug dev exit 1" | socat /var/run/haproxy.master -
echo "expert-mode on; @1 debug dev exit 1" | socat /var/run/haproxy.master -
```

<a id="entry-9-3-get-map"></a>

**`get map <map> <value>`**

```haproxy
get map <map> <value>
get acl <acl> <value>
```

Busca el valor `<value>` en el mapa `<map>` o en la ACL `<acl>`. `<map>` o `<acl>` son el
\#`<id>` o el `<name>` devueltos por "show map" o "show acl". Este comando devuelve todos los
patrones coincidentes asociados a este mapa. Esto es útil para depurar mapas y ACLs. El formato de
salida se compone de una línea por tipo de coincidencia. Cada línea se compone de una serie de
palabras delimitadas por espacios.

Las dos primeras palabras son:

```text
<match method>:   El método de coincidencia aplicado. Puede ser "found", "bool",
                  "int", "ip", "bin", "len", "str", "beg", "sub", "dir",
                  "dom", "end" o "reg".

<match result>:   El resultado. Puede ser "match" o "no-match".
```

Las palabras siguientes solo se devuelven si el patrón coincide con una entrada.

     `<index type>`:     "tree" o "list". El algoritmo interno de búsqueda.

     `<case>`:           "case-insensitive" o "case-sensitive". La
                       interpretación de las mayúsculas y minúsculas.

     `<entry matched>`:  match="`<entry>`". Devuelve el patrón coincidente. Es
                       útil con expresiones regulares.

Las dos últimas palabras se usan para mostrar el valor devuelto y su tipo. En el caso de "acl", el
patrón no existe.

     return=nothing:        Sin retorno porque no hay "map".
     return="`<value>`":      El valor devuelto en formato de cadena.
     return=cannot-display: El valor no puede convertirse a cadena.

     type="`<type>`":         El tipo de la muestra devuelta.

<a id="entry-9-3-get-var"></a>

**`get var <name>`**

```haproxy
get var <name>
```

Muestra la existencia, el tipo y el contenido de la variable de ámbito de proceso 'name'. Solo las
variables de ámbito de proceso son legibles, por lo que el nombre debe comenzar por 'proc.'; de lo
contrario no se encontrará ninguna variable. Este comando requiere niveles "operator" o "admin".

<a id="entry-9-3-get-weight"></a>

**`get weight <backend>/<server>`**

```haproxy
get weight <backend>/<server>
```

Informa del peso actual y del peso inicial del servidor `<server>` en el backend `<backend>`, o de
un error si alguno de los dos no existe. El peso inicial es el que aparece en el archivo de
configuración. Normalmente ambos son iguales, salvo que el peso actual haya sido cambiado. Tanto el
backend como el servidor pueden especificarse por su nombre o por su ID numérico, precedido de una
almohadilla ('#').

<a id="entry-9-3-help"></a>

**`help [<command>]`**

```haproxy
help [<command>]
```

Imprime la lista de palabras clave conocidas y su uso básico, o los comandos que coinciden con el
solicitado. La misma pantalla de ayuda también se muestra para los comandos desconocidos.

<a id="entry-9-3-httpclient"></a>

**`httpclient [--htx] <method> <URI>`**

```haproxy
httpclient [--htx] <method> <URI>
```

Lanza una petición de cliente HTTP e imprime la respuesta en la CLI. Solo se admite en una
conexión CLI ejecutándose en modo experto (ver "expert-mode on"). Está destinado únicamente a la
depuración. El httpclient es capaz de resolver un nombre de servidor en la URL usando la sección
de resolvers "default", que se rellena por defecto con los servidores DNS de tu /etc/resolv.conf.
Sin embargo, no podrá resolver un host desde /etc/hosts si no usas un demonio dns local que pueda
resolverlos.

La opción --htx permite usar la representación htx interna de haproxy mediante la función
htx_dump(), usada principalmente para depuración.

<a id="entry-9-3-new-ssl-ca-file"></a>

**`new ssl ca-file <cafile>`**

```haproxy
new ssl ca-file <cafile>
```

Crea una nueva entrada vacía en el árbol de archivos CA, para rellenarla con un conjunto de
certificados CA y añadirla a una crt-list. Este comando debería usarse en combinación con "set ssl
ca-file", "add ssl ca-file" y "add ssl crt-list".

<a id="entry-9-3-new-ssl-cert"></a>

**`new ssl cert <filename>`**

```haproxy
new ssl cert <filename>
```

Crea un nuevo almacén de certificados SSL vacío, para rellenarlo con un certificado y añadirlo a
un directorio o a una crt-list. Este comando debería usarse en combinación con "set ssl cert" y
"add ssl crt-list".

<a id="entry-9-3-new-ssl-crl-file"></a>

**`new ssl crl-file <crlfile>`**

```haproxy
new ssl crl-file <crlfile>
```

Crea una nueva entrada vacía en el árbol de archivos CRL, para rellenarla con un conjunto de CRL y
añadirla a una crt-list. Este comando debería usarse en combinación con "set ssl crl-file" y "add
ssl crt-list".

<a id="entry-9-3-prepare-acl"></a>

**`prepare acl <acl>`**

```haproxy
prepare acl <acl>
```

Asigna un nuevo número de versión en la ACL `<acl>` para un reemplazo atómico. `<acl>` es el
\#`<id>` o el `<name>` devuelto por "show acl". El nuevo número de versión se muestra en la
respuesta después de "New version created:". Este número podrá usarse entonces para preparar
adiciones de nuevas entradas en la ACL, que reemplazarán atómicamente las actuales una vez
confirmadas. Se informa como "next_ver" en "show acl". Asignar nuevas versiones no tiene impacto,
ya que las versiones sin usar se eliminarán automáticamente una vez que se confirme una versión
más reciente. Los números de versión son valores sin signo de 32 bits que se desbordan al final,
por lo que debe tenerse cuidado al compararlos en un programa externo. Este comando no puede usarse
si la referencia `<acl>` es un nombre también utilizado como mapa. En este caso, debe usarse en su
lugar el comando "prepare map".

<a id="entry-9-3-prepare-map"></a>

**`prepare map <map>`**

```haproxy
prepare map <map>
```

Asigna un nuevo número de versión en el mapa `<map>` para un reemplazo atómico. `<map>` es el
\#`<id>` o el `<name>` devuelto por "show map". El nuevo número de versión se muestra en la
respuesta después de "New version created:". Este número podrá usarse entonces para preparar
adiciones de nuevas entradas en el mapa, que reemplazarán atómicamente las actuales una vez
confirmadas. Se informa como "next_ver" en "show map". Asignar nuevas versiones no tiene impacto,
ya que las versiones sin usar se eliminarán automáticamente una vez que se confirme una versión
más reciente. Los números de versión son valores sin signo de 32 bits que se desbordan al final,
por lo que debe tenerse cuidado al compararlos en un programa externo.

<a id="entry-9-3-prompt"></a>

**`prompt [help | n | i | p | timed]*`**

```haproxy
prompt [help | n | i | p | timed]*
```

Cambia el comportamiento del modo interactivo y del prompt mostrado al principio de la línea en
modo interactivo: - "help": muestra el uso del comando - "n": cambia al modo no interactivo -
"i": cambia al modo interactivo - "p": cambia al modo interactivo + prompt - "timed": alterna la
visualización del tiempo de actividad en el prompt

Sin ninguna opción, esto alternará entre el modo prompt y luego el modo no interactivo. En el modo
no interactivo, la conexión se cierra después de que se complete el último comando de la línea
actual. En el modo interactivo, la conexión no se cierra después de que se complete un comando, de
modo que pueda introducirse uno nuevo. En el modo prompt, el modo interactivo sigue en uso y
aparecerá un prompt al principio de la línea, indicando al usuario que el intérprete está
esperando un comando nuevo. El prompt consiste en un corchete angular de cierre seguido de un
espacio "\> ".

El modo prompt es más adecuado para usuarios humanos, el modo interactivo para scripts avanzados y
el modo no interactivo (predeterminado) para scripts básicos. Ten en cuenta que el modo no
interactivo no está disponible para el socket maestro.

<a id="entry-9-3-publish-backend"></a>

**`publish backend <backend>`**

```haproxy
publish backend <backend>
```

Activa la conmutación de contenido hacia una instancia de backend. Es la operación inversa del
comando "unpublish backend". Este comando está restringido y solo puede emitirse en sockets
configurados con niveles "operator" o "admin".

<a id="entry-9-3-quit"></a>

**`quit`**

```haproxy
quit
```

Cierra la conexión cuando está en modo interactivo.

<a id="entry-9-3-set-anon"></a>

**`set anon [on|off] [<key>]`**

```haproxy
set anon [on|off] [<key>]
```

Este comando activa o desactiva el "modo anonimizado" para la sesión CLI actual, que reemplaza
ciertos campos considerados sensibles o confidenciales en las salidas de comandos por hashes que
conservan suficiente coherencia entre elementos para ayudar a los desarrolladores a identificar
relaciones entre elementos al intentar detectar errores, pero con un número de bits lo bastante
bajo (24) para hacerlos no reversibles debido al alto número de coincidencias posibles. Al
activarlo, si no se especifica ninguna clave, se usará la clave global (especificada en el archivo
de configuración mediante "anonkey" o establecida con el comando CLI "set anon global-key"). Si no
se había establecido tal clave, se generará una aleatoria. De lo contrario, es posible especificar
la clave de 32 bits que se usará para la sesión actual, por ejemplo, para reutilizar la clave que
se usó en un volcado anterior y ayudar a comparar salidas. Los desarrolladores nunca necesitarán
esta clave y se recomienda no compartirla nunca, ya que podría permitir confirmar o descartar
algunas conjeturas sobre lo que ciertos hashes podrían estar ocultando.

<a id="entry-9-3-set-dynamic-cookie-key-backend"></a>

**`set dynamic-cookie-key backend <backend> <value>`**

```haproxy
set dynamic-cookie-key backend <backend> <value>
```

Modifica la clave secreta usada para generar las cookies persistentes dinámicas. Esto romperá las
sesiones existentes.

<a id="entry-9-3-set-anon-global-key"></a>

**`set anon global-key <key>`**

```haproxy
set anon global-key <key>
```

Establece la clave global de anonimización en `<key>`, que debe ser un entero de 32 bits entre 0 y
4294967295 (0 desactiva la clave global). Este comando requiere privilegios de administrador.

<a id="entry-9-3-set-map"></a>

**`set map <map> [<key>|#<ref>] <value>`**

```haproxy
set map <map> [<key>|#<ref>] <value>
```

Modifica el valor correspondiente a cada clave `<key>` en un mapa `<map>`. `<map>` es el \#`<id>`
o el `<name>` devuelto por "show map". Si se usa `<ref>` en lugar de `<key>`, solo se cambia la
entrada apuntada por `<ref>`. El nuevo valor es `<value>`.

<a id="entry-9-3-set-maxconn-frontend"></a>

**`set maxconn frontend <frontend> <value>`**

```haproxy
set maxconn frontend <frontend> <value>
```

Cambia dinámicamente el ajuste maxconn del frontend especificado. Se permite cualquier valor
positivo, incluido el cero, pero establecer valores mayores que el maxconn global no tiene mucho
sentido. Si se aumenta el límite y había conexiones pendientes, se aceptarán inmediatamente. Si se
reduce a un valor inferior al número actual de conexiones, la aceptación de nuevas conexiones se
retrasará hasta alcanzar el umbral. El frontend puede especificarse por su nombre o por su ID
numérico precedido de una almohadilla ('#').

<a id="entry-9-3-set-maxconn-server"></a>

**`set maxconn server <backend/server> <value>`**

```haproxy
set maxconn server <backend/server> <value>
```

Cambia dinámicamente el ajuste maxconn del servidor especificado. Se permite cualquier valor
positivo, incluido el cero, pero establecer valores mayores que el maxconn global no tiene mucho
sentido.

<a id="entry-9-3-set-maxconn-global"></a>

**`set maxconn global <maxconn>`**

```haproxy
set maxconn global <maxconn>
```

Cambia dinámicamente el ajuste maxconn global dentro del rango definido por el ajuste maxconn
global inicial. Si se aumenta y había conexiones pendientes, se aceptarán inmediatamente. Si se
reduce a un valor inferior al número actual de conexiones, la aceptación de nuevas conexiones se
retrasará hasta alcanzar el umbral. Un valor de cero restablece el ajuste inicial.

<a id="entry-9-3-set-profiling-memory"></a>

**`set profiling memory { on | off }`**

```haproxy
set profiling memory { on | off }
set profiling tasks { auto | on | off | lock | no-lock | memory | no-memory }
```

Activa o desactiva el perfilado de CPU o de memoria para el subsistema indicado. Esto es
equivalente a establecer o borrar los ajustes "profiling" en la sección "global" del archivo de
configuración. Ver también "show profiling". Ten en cuenta que establecer manualmente el perfilado
de tareas en "on" restablece automáticamente las estadísticas del planificador, lo que permite
comprobar la actividad durante un intervalo dado. El perfilado de memoria está limitado a ciertos
sistemas operativos (se sabe que funciona en el destino linux-glibc) y requiere que
USE_MEMORY_PROFILING esté definido en tiempo de compilación.

. Para el perfilado de tareas, es posible activar o desactivar en tiempo de ejecución la
recolección de tiempos de bloqueo y memoria por tarea, pero el cambio solo se tiene en cuenta la
próxima vez que el perfilador pase de off/auto a on (ya sea automáticamente o manualmente). Por
ello, al usar "no-lock" para desactivar el perfilado de bloqueos por tarea y ahorrar ciclos de
CPU, se recomienda poner el perfilado de tareas en off y después en on para confirmar el cambio.

<a id="entry-9-3-set-rate-limit-connections-global"></a>

**`set rate-limit connections global <value>`**

```haproxy
set rate-limit connections global <value>
```

Cambia el límite de tasa de conexiones de todo el proceso, que se establece con el ajuste global
'maxconnrate'. Un valor de cero desactiva la limitación. Este límite se aplica a todos los
frontends y el cambio tiene efecto inmediato. El valor se pasa en número de conexiones por segundo.

<a id="entry-9-3-set-rate-limit-http-compression-global"></a>

**`set rate-limit http-compression global <value>`**

```haproxy
set rate-limit http-compression global <value>
```

Cambia la tasa máxima de compresión de entrada, que se establece con el ajuste global
'maxcomprate'. Un valor de cero desactiva la limitación. El valor se pasa en número de kilobytes
por segundo. El valor está disponible en "show info", en la línea "CompressBpsRateLim", en bytes.

<a id="entry-9-3-set-rate-limit-sessions-global"></a>

**`set rate-limit sessions global <value>`**

```haproxy
set rate-limit sessions global <value>
```

Cambia el límite de tasa de sesiones de todo el proceso, que se establece con el ajuste global
'maxsessrate'. Un valor de cero desactiva la limitación. Este límite se aplica a todos los
frontends y el cambio tiene efecto inmediato. El valor se pasa en número de sesiones por segundo.

<a id="entry-9-3-set-rate-limit-ssl-sessions-global"></a>

**`set rate-limit ssl-sessions global <value>`**

```haproxy
set rate-limit ssl-sessions global <value>
```

Cambia el límite de tasa de sesiones SSL de todo el proceso, que se establece con el ajuste global
'maxsslrate'. Un valor de cero desactiva la limitación. Este límite se aplica a todos los frontends
y el cambio tiene efecto inmediato. El valor se pasa en número de sesiones por segundo enviadas a
la pila SSL. Se aplica antes del saludo (handshake) para proteger la pila contra abusos del
saludo.

<a id="entry-9-3-set-server"></a>

**`set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]`**

```haproxy
set server <backend>/<server> addr <ip4 or ip6 address> [port <port>]
```

Reemplaza la dirección IP actual de un servidor por la proporcionada. Opcionalmente, el puerto
puede cambiarse con el parámetro 'port'. Ten en cuenta que cambiar el puerto también admite la
conmutación hacia/desde el mapeo de puertos (notación con +X o -Y), solo si hay un puerto
configurado para la comprobación de estado.

<a id="entry-9-3-set-server-2"></a>

**`set server <backend>/<server> agent [ up | down ]`**

```haproxy
set server <backend>/<server> agent [ up | down ]
```

Fuerza el agente de un servidor a un nuevo estado. Esto puede ser útil, por ejemplo, para cambiar
inmediatamente el estado de un servidor independientemente de algunas comprobaciones de agente
lentas. Ten en cuenta que el cambio se propaga a los servidores que lo siguen, si los hay.

<a id="entry-9-3-set-server-3"></a>

**`set server <backend>/<server> agent-addr <addr> [port <port>]`**

```haproxy
set server <backend>/<server> agent-addr <addr> [port <port>]
```

Cambia la dirección (addr) de las comprobaciones de agente de los servidores. Permite migrar las
comprobaciones de agente a otra dirección en tiempo de ejecución. Puedes especificar tanto una IP
como un nombre de host; se resolverá. Opcionalmente, cambia el puerto del agente.

<a id="entry-9-3-set-server-4"></a>

**`set server <backend>/<server> agent-port <port>`**

```haproxy
set server <backend>/<server> agent-port <port>
```

Cambia el puerto usado para las comprobaciones de agente.

<a id="entry-9-3-set-server-5"></a>

**`set server <backend>/<server> agent-send <value>`**

```haproxy
set server <backend>/<server> agent-send <value>
```

Cambia la cadena del agente enviada al destino de la comprobación del agente. Permite actualizar
la cadena al cambiar la dirección del servidor para mantener ambas coincidentes.

<a id="entry-9-3-set-server-6"></a>

**`set server <backend>/<server> health [ up | stopping | down ]`**

```haproxy
set server <backend>/<server> health [ up | stopping | down ]
```

Fuerza el estado de salud de un servidor a un nuevo estado. Esto puede ser útil, por ejemplo, para
cambiar inmediatamente el estado de un servidor independientemente de algunas comprobaciones de
estado lentas. Ten en cuenta que el cambio se propaga a los servidores que lo siguen, si los hay.

<a id="entry-9-3-set-server-7"></a>

**`set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]`**

```haproxy
set server <backend>/<server> check-addr <ip4 | ip6> [port <port>]
```

Cambia la dirección IP usada para las comprobaciones de estado del servidor. Opcionalmente, cambia
el puerto usado para las comprobaciones de estado del servidor.

<a id="entry-9-3-set-server-8"></a>

**`set server <backend>/<server> check-port <port>`**

```haproxy
set server <backend>/<server> check-port <port>
```

Cambia el puerto usado para las comprobaciones de estado a `<port>`

<a id="entry-9-3-set-server-9"></a>

**`set server <backend>/<server> state [ ready | drain | maint ]`**

```haproxy
set server <backend>/<server> state [ ready | drain | maint ]
```

Fuerza el estado administrativo de un servidor a un nuevo estado. Esto puede ser útil para
desactivar el balanceo de carga y/o cualquier tráfico hacia un servidor. Establecer el estado en
"ready" pone el servidor en modo normal, y el comando es el equivalente del comando "enable
server". Establecer el estado en "maint" desactiva cualquier tráfico hacia el servidor así como
cualquier comprobación de estado. Es el equivalente del comando "disable server". Establecer el
modo en "drain" solo retira el servidor del balanceo de carga pero sigue permitiendo que se
compruebe y que acepte nuevas conexiones persistentes. Los cambios se propagan a los servidores que
lo siguen, si los hay.

<a id="entry-9-3-set-server-10"></a>

**`set server <backend>/<server> weight <weight>[%]`**

```haproxy
set server <backend>/<server> weight <weight>[%]
```

Cambia el peso de un servidor al valor pasado como argumento. Es el equivalente exacto del comando
"set weight" que sigue.

<a id="entry-9-3-set-server-11"></a>

**`set server <backend>/<server> fqdn <FQDN>`**

```haproxy
set server <backend>/<server> fqdn <FQDN>
```

Cambia el FQDN de un servidor al valor pasado como argumento. Esto requiere que el resolvedor DNS
interno en tiempo de ejecución esté configurado y activado para este servidor.

<a id="entry-9-3-set-server-12"></a>

**`set server <backend>/<server> ssl [ on | off ]  (deprecated)`**

```haproxy
set server <backend>/<server> ssl [ on | off ]  (deprecated)
```

Esta opción configura el cifrado SSL en las conexiones salientes hacia el servidor. Cuando se
desactiva, todo el tráfico se convierte en texto plano; la ruta de la comprobación de estado no
cambia.

Este comando está obsoleto; crea en su lugar un servidor nuevo dinámicamente con o sin SSL, usando
el comando "add server".

<a id="entry-9-3-set-severity-output"></a>

**`set severity-output [ none | number | string ]`**

```haproxy
set severity-output [ none | number | string ]
```

Cambia el formato de salida de la gravedad del socket de estadísticas al que se está conectado,
durante la sesión actual.

<a id="entry-9-3-set-ssl-ca-file"></a>

**`set ssl ca-file <cafile> <payload>`**

```haproxy
set ssl ca-file <cafile> <payload>
```

este comando es parte de un sistema de transacciones; los comandos "commit ssl ca-file" y "abort
ssl ca-file" podrían ser necesarios. si no hay una transacción en curso, creará una entrada en el
árbol de archivos ca en la que se almacenarán los certificados contenidos en el payload. la
entrada del archivo ca no se almacenará en el árbol de archivos ca y solo se mantendrá en una
transacción temporal. si ya existe una transacción con el mismo nombre de archivo, la entrada
anterior del archivo ca se eliminará y será reemplazada por la nueva. una vez hechas las
modificaciones, debes confirmar la transacción mediante una llamada a "commit ssl ca-file". Si
quieres añadir varios certificados por separado, puedes usar el comando "add ssl ca-file"

Ejemplo:

```text
echo -e "set ssl ca-file cafile.pem <<\n$(cat rootCA.crt)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl ca-file cafile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-cert"></a>

**`set ssl cert <filename> <payload>`**

```haproxy
set ssl cert <filename> <payload>
```

Este comando es parte de un sistema de transacciones; los comandos "commit ssl cert" y "abort ssl
cert" podrían ser necesarios. Todo este sistema de transacciones funciona con cualquier
certificado mostrado por el comando "show ssl cert", es decir, con cualquier certificado de
frontend o de backend. Si no hay una transacción en curso, duplicará en memoria el certificado
`<filename>` en una transacción temporal y luego actualizará esta transacción con el archivo PEM
del payload. Si existe una transacción con el mismo nombre de archivo, actualizará esta
transacción. También es posible actualizar los archivos vinculados a un certificado (.issuer,
.sctl, .ocsp etc.) Una vez hechas las modificaciones, debes aplicar "commit ssl cert" a la
transacción.

La inyección de archivos por la CLI debe hacerse con precaución, ya que se usa una línea vacía
para notificar el final del payload. Se recomienda inyectar un archivo PEM que haya sido depurado
(sanitized). Un método simple sería eliminar cada línea vacía y dejar solo lo que hay en las
secciones PEM. Podría lograrse con un comando sed.

Ejemplo:

```haproxy
# With some simple sanitizing
 echo -e "set ssl cert localhost.pem <<\n$(sed -n '/^$/d;/-BEGIN/,/-END/p' 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -

 # Complete example with commit
 echo -e "set ssl cert localhost.pem <<\n$(cat 127.0.0.1.pem)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.issuer <<\n $(cat 127.0.0.1.pem.issuer)\n" | \
 socat /var/run/haproxy.stat -
 echo -e \
 "set ssl cert localhost.pem.ocsp <<\n$(base64 -w 1000 127.0.0.1.pem.ocsp)\n" | \
 socat /var/run/haproxy.stat -
 echo "commit ssl cert localhost.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-crl-file"></a>

**`set ssl crl-file <crlfile> <payload>`**

```haproxy
set ssl crl-file <crlfile> <payload>
```

Este comando es parte de un sistema de transacciones; los comandos "commit ssl crl-file" y "abort
ssl crl-file" podrían ser necesarios. Si no hay una transacción en curso, creará una entrada en el
árbol de archivos CRL en la que se almacenarán las Listas de Revocación contenidas en el payload.
La entrada del archivo CRL no se almacenará en el árbol de archivos CRL y solo se mantendrá en una
transacción temporal. Si ya existe una transacción con el mismo nombre de archivo, la entrada
anterior del archivo CRL se eliminará y será reemplazada por la nueva. Una vez hechas las
modificaciones, debes confirmar la transacción mediante una llamada a "commit ssl crl-file".

Ejemplo:

```text
echo -e "set ssl crl-file crlfile.pem <<\n$(cat rootCRL.pem)\n" | \
socat /var/run/haproxy.stat -
echo "commit ssl crl-file crlfile.pem" | socat /var/run/haproxy.stat -
```

<a id="entry-9-3-set-ssl-ech"></a>

**`set ssl ech <bind> <payload>`**

```haproxy
set ssl ech <bind> <payload>
```

Reemplaza las claves ECH de una línea bind por esta. El payload debe estar en el formato PEM for
ECH. (<https://datatracker.ietf.org/doc/html/draft-farrell-tls-pemesni>)

El formato de la línea bind es `<frontend>`/@`<filename>`:`<linenum>` (Ejemplo:
frontend1/@haproxy.conf:19) o `<frontend>`/`<name>` si la línea bind fue nombrada con la palabra
clave "name".

Requiere una versión de OpenSSL que admita ECH y que HAProxy esté compilado con USE_ECH=1. Este
comando solo se admite en una conexión CLI ejecutándose en modo experimental (ver
"experimental-mode on").

Ver también "show ssl ech", "add ssl ech" y "ech" en la [Sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1) del manual de configuración.

    $ openssl ech -public_name foobar.com -out foobar3.com.ech
    $ echo -e "experimental-mode on;
               set ssl ech frontend1/@haproxy.conf:19 <<%EOF%&#92;n$(cat foobar3.com.ech)&#92;n%EOF%&#92;n" | &#92;
      socat /tmp/haproxy.sock -
    set new ECH configs for frontend1/@haproxy.conf:19

<a id="entry-9-3-set-ssl-ocsp-response"></a>

**`set ssl ocsp-response <response | payload>`**

```haproxy
set ssl ocsp-response <response | payload>
```

Este comando se usa para actualizar una Respuesta OCSP de un certificado (ver "crt" en las líneas
"bind"). Se realizan los mismos controles que durante la carga inicial de la respuesta.
`<response>` debe pasarse como una cadena codificada en base64 de la respuesta codificada en DER
del servidor OCSP. Este comando no es compatible con BoringSSL.

Ejemplo:

```text
openssl ocsp -issuer issuer.pem -cert server.pem \
             -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | \
             socat stdio /var/run/haproxy.stat

usando la sintaxis del payload:
echo -e "set ssl ocsp-response <<\n$(base64 resp.der)\n" | \
             socat stdio /var/run/haproxy.stat
```

<a id="entry-9-3-set-ssl-tls-key"></a>

**`set ssl tls-key <id> <tlskey>`**

```haproxy
set ssl tls-key <id> <tlskey>
```

Establece la siguiente clave TLS del listener `<id>` en `<tlskey>`. Esta clave se convierte en la
clave última, mientras que la penúltima se usa para el cifrado (las demás solo descifran). La
clave TLS más antigua presente se sobrescribe. `<id>` es un \#`<id>` numérico o un `<file>`
devuelto por "show tls-keys". `<tlskey>` es una clave de ticket TLS de 48 u 80 bytes codificada en
base64 (ej. openssl rand 80 \| openssl base64 -A).

<a id="entry-9-3-set-table"></a>

**`set table <table> key <key> [data.<data_type> <value>]*`**

```haproxy
set table <table> key <key> [data.<data_type> <value>]*
set table <table> ptr <ptr> [data.<data_type> <value>]*
```

Crea o actualiza una entrada de stick-table en la tabla. Si la clave no está presente, se inserta
una entrada. Consulta stick-table en la sección 4.2 para encontrar todos los valores posibles de
`<data_type>`. El uso más probable consiste en introducir dinámicamente entradas para direcciones
IP de origen, con un indicador en gpc0 para bloquear dinámicamente una dirección IP o afectar su
calidad de servicio. Es posible pasar múltiples data_types en una sola llamada.

La búsqueda opcional por ptr puede usarse en lugar de la búsqueda por clave para una entrada
existente: `<ptr>` se escribe en la forma 0xffff y debe corresponder a la dirección devuelta por
un comando "show table" anterior. Identificar una entrada mediante su puntero puede ser pertinente
si la entrada no puede identificarse mediante la clave debido a una clave vacía o a caracteres
incompatibles en la CLI.

Si data.`<data_type>` es un tipo array, puede usarse "[]" para acceder a un índice específico del
array, así: data.gpt[1]

<a id="entry-9-3-set-timeout-cli"></a>

**`set timeout cli <delay>`**

```haproxy
set timeout cli <delay>
```

Cambia el timeout de la interfaz CLI para la conexión actual. Esto puede ser útil durante sesiones
de depuración largas donde el usuario necesita inspeccionar constantemente algunos indicadores sin
ser desconectado. El retardo se pasa en segundos.

<a id="entry-9-3-set-var"></a>

**`set var <name> <expression>`**

```haproxy
set var <name> <expression>
set var <name> expr <expression>
set var <name> fmt <format>
```

Permite establecer o sobrescribir la variable de ámbito de proceso 'name' con el resultado de la
expresión `<expression>` o de la cadena de formato `<format>`. Solo pueden usarse variables de
ámbito de proceso, por lo que el nombre debe comenzar por 'proc.'; de lo contrario no se
establecerá ninguna variable. `<expression>` y `<format>` solo pueden involucrar palabras clave y
conversores de obtención de muestras "internos", aunque las más útiles probablemente serán
str('something'), int(), cadenas simples o referencias a otras variables. Ten en cuenta que el
analizador de la línea de comandos no conoce las comillas, por lo que cualquier espacio en la
expresión debe ir precedido de una barra invertida. Este comando requiere niveles "operator" o
"admin". Este comando solo se admite en una conexión CLI ejecutándose en modo experimental (ver
"experimental-mode on").

<a id="entry-9-3-set-weight"></a>

**`set weight <backend>/<server> <weight>[%]`**

```haproxy
set weight <backend>/<server> <weight>[%]
```

Cambia el peso de un servidor al valor pasado como argumento. Si el valor termina con el signo
'%', el nuevo peso será relativo al peso configurado inicialmente. Se permiten pesos absolutos
entre 0 y 256. Los pesos relativos deben ser positivos y el peso absoluto resultante está limitado
a 256. Los servidores que forman parte de una granja que ejecuta un algoritmo de balanceo de carga
estático tienen limitaciones más estrictas porque el peso no puede cambiar una vez establecido.
Así, para estos servidores, los únicos valores aceptados son 0 y 100% (o 0 y el peso inicial). Los
cambios surten efecto inmediatamente, aunque ciertos algoritmos de LB requieren una cierta
cantidad de peticiones para considerar los cambios. Un uso típico de este comando es desactivar un
servidor durante una actualización estableciendo su peso a cero y luego reactivarlo tras la
actualización devolviéndolo al 100%. Este comando está restringido y solo puede emitirse en
sockets configurados con nivel "admin". Tanto el backend como el servidor pueden especificarse por
su nombre o por su ID numérico, precedido de una almohadilla ('#').

<a id="entry-9-3-show-acl"></a>

**`show acl [[@<ver>] <acl>]`**

```haproxy
show acl [[@<ver>] <acl>]
```

Vuelca información sobre los conversores acl. Sin argumento, se devuelve la lista de todas las
ACLs disponibles. Si se especifica un `<acl>`, se vuelca su contenido. `<acl>` es el \#`<id>` o el
`<name>`. Por defecto se muestra la versión actual de la ACL (la versión usada actualmente para
las coincidencias e informada como 'curr_ver' en la lista de ACLs). Es posible volcar en su lugar
otras versiones anteponiendo '@`<ver>`' antes del identificador de la ACL. La versión funciona como
un filtro y las versiones inexistentes simplemente no informarán ningún resultado. El formato del
volcado es el mismo que el de los mapas, incluso para los valores de muestra. Los datos devueltos
no son una lista de ACLs disponibles, sino la lista de todos los patrones que componen cualquier
ACL. Muchos de estos patrones pueden compartirse con mapas. El valor 'entry_cnt' representa el
recuento de todas las entradas de la ACL, no solo las activas, lo que significa que también incluye
las entradas que se están añadiendo actualmente.

<a id="entry-9-3-show-anon"></a>

**`show anon`**

```haproxy
show anon
```

Muestra el estado actual del modo anonimizado (activado o desactivado) y la clave de la sesión
actual.

<a id="entry-9-3-show-backend"></a>

**`show backend`**

```haproxy
show backend
```

Vuelca la lista de backends disponibles en el proceso en ejecución

<a id="entry-9-3-show-cli-level"></a>

**`show cli level`**

```haproxy
show cli level
```

Muestra el nivel CLI de la sesión CLI actual. El resultado podría ser 'admin', 'operator' o
'user'. Ver también los comandos 'operator' y 'user'.

Ejemplo:

```shell
$ socat /tmp/sock1 readline
prompt
> operator
> show cli level
operator
> user
> show cli level
user
> operator
Permission denied
```

<a id="entry-9-3-operator"></a>

**`operator`**

```haproxy
operator
```

Reduce el nivel CLI de la sesión CLI actual a operator. No puede aumentarse. También descarta el
modo experto y el modo experimental. Ver también "show cli level".

<a id="entry-9-3-unpublish-backend"></a>

**`unpublish backend <backend>`**

```haproxy
unpublish backend <backend>
```

Marca el backend como no cualificado para la selección futura de tráfico. En efecto, las reglas
use_backend / default_backend que lo referencian se ignoran y se evalúan las siguientes reglas de
conmutación de contenido. Al contrario que los backends desactivados, las comprobaciones de estado
de los servidores permanecen activas. Este comando está restringido y solo puede emitirse en
sockets configurados con niveles "operator" o "admin".

<a id="entry-9-3-user"></a>

**`user`**

```haproxy
user
```

Reduce el nivel CLI de la sesión CLI actual a user. No puede aumentarse. También descarta el modo
experto y el modo experimental. Ver también "show cli level".

<a id="entry-9-3-show-activity"></a>

**`show activity [-1 | 0 | thread_num]`**

```haproxy
show activity [-1 | 0 | thread_num]
```

Informa de algunos contadores sobre eventos internos que ayudarán a los desarrolladores y, en
general, a las personas que conocen haproxy lo suficiente a acotar las causas de los informes de
comportamientos anómalos. Un ejemplo típico sería un proceso funcionando correctamente que nunca
duerme y consume el 100% de la CPU. Los campos de salida estarán formados por una línea por
métrica, con contadores por hilo en la misma línea. Estos contadores son de 32 bits y se
desbordarán durante la vida del proceso, lo cual no es un problema dado que las llamadas a este
comando se realizarán típicamente dos veces. Los campos están deliberadamente sin documentar para
que su significado exacto se verifique en el código donde se alimentan los contadores. Estos
valores también se restablecen con el comando "clear counters". En despliegues multi-hilo, la
primera columna indicará el total (o el promedio, dependiendo de la naturaleza de la métrica) de
todos los hilos, y la lista de los valores de todos los hilos se representará entre corchetes en
el orden de los hilos. Opcionalmente puede especificarse como argumento el número de hilo que se va
a volcar. El valor especial "0" informará del valor agregado (primera columna), y "-1", que es el
predeterminado, mostrará todas las columnas. Ten en cuenta que, igual que en el modo de un solo
hilo, no habrá corchetes cuando se solicite una sola columna.

<a id="entry-9-3-show-cli-sockets"></a>

**`show cli sockets`**

```haproxy
show cli sockets
```

Lista los sockets CLI. El formato de salida se compone de 3 campos separados por espacios. El
primer campo es la dirección del socket; puede ser un socket unix, un par dirección:puerto ipv4 o
uno ipv6. Los sockets de otros tipos no se volcarán. El segundo campo describe el nivel del
socket: 'admin', 'user' u 'operator'. El último campo lista los procesos a los que está enlazado el
socket, separados por comas; pueden ser números o 'all'.

Ejemplo:

```shell
$ echo 'show cli sockets' | socat stdio /tmp/sock1
# socket lvl processes
/tmp/sock1 admin all
127.0.0.1:9999 user 2,3,4
127.0.0.2:9969 user 2
[::1]:9999 operator 2
```

<a id="entry-9-3-show-cache"></a>

**`show cache`**

```haproxy
show cache
```

Lista las cachés configuradas y los objetos almacenados en cada árbol de caché.

\$ echo 'show cache' \| socat stdio /tmp/sock1 0x7f6ac6c5b03a: foobar (shctx:0x7f6ac6c5b000,
available blocks:3918) 1 2 3 4

1.  puntero a la estructura de la caché
2.  nombre de la caché
3.  puntero al área mmap (shctx)
4.  número de bloques disponibles para reutilización en el shctx

0x7f6ac6c5b4cc hash:286881868 vary:0x0011223344556677 size:39114 (39 blocks), refcount:9, expire:237
1 2 3 4 5 6 7

1.  puntero a la entrada de la caché
2.  primeros 32 bits del hash
3.  hash secundario de la entrada en caso de vary
4.  tamaño del objeto en bytes
5.  número de bloques usados por el objeto
6.  número de transacciones que usan la entrada
7.  tiempo de expiración, puede ser negativo si ya expiró

<a id="entry-9-3-show-dev"></a>

**`show dev`**

```haproxy
show dev
```

Este comando está pensado para centralizar cierta información que los desarrolladores de HAProxy
podrían necesitar para comprender mejor las causas de un problema dado. Por lo general no
proporciona información útil para el usuario, pero esta información permite a los desarrolladores
descartar ciertas hipótesis. El formato es, a grandes rasgos, una serie de secciones que contienen
líneas indentadas con un elemento por línea, como por ejemplo el tipo y la versión del sistema
operativo, el tipo de CPU o los límites de FD en el arranque. Algunos campos se omitirán para
evitar repeticiones o contaminación de la salida cuando no aporten valor (p. ej., valores
ilimitados). Es posible que en el futuro aparezcan más campos y que algunos cambien. Esta salida
no está pensada para ser analizada por scripts y no debe considerarse con un alto grado de
fiabilidad; su objetivo es esencialmente ahorrar tiempo a quienes saben leerla.

Técnicamente hablando, dicha información se toma tal cual de una estructura interna que la
almacena junta en el momento del arranque, de modo que también pueda encontrarse en un archivo
core tras un cuelgue. Por ello puede ocurrir que los desarrolladores pidan una salida temprana de
un proceso con buen comportamiento para compararla con lo que se encuentra en un volcado core, o
para comparar entre varias recargas (p. ej., algunos límites podrían cambiar). Si el anonimizado
está activado, cualquier valor posiblemente sensible también será anonimizado (p. ej., el nombre
del nodo).

Ejemplo de salida:

```shell
$ socat stdio /tmp/sock1 <<< "show dev"
Platform info
  machine vendor: To be filled by O.E.M
  machine family: Altra
  cpu model: Impl 0x41 Arch 8 Part 0xd0c r3p1
  virtual machine: no
  container: no
  OS name: Linux
  OS release: 6.2.0-36-generic
  OS version: #37~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct  9 18:01:07 UTC 2
  OS architecture: aarch64
  node name: 489aaf
Process info
  pid: 1735846
  boot uid: 509
  boot gid: 1002
  fd limit (soft): 1024
  fd limit (hard): 1048576
```

<a id="entry-9-3-show-env"></a>

**`show env [<name>]`**

```haproxy
show env [<name>]
```

Vuelca una o todas las variables de entorno conocidas por el proceso. Sin ningún argumento, se
vuelcan todas las variables. Con un argumento, solo se vuelca la variable especificada si existe.
En caso contrario se emite "Variable not found". Las variables se vuelcan en el mismo formato en
que se almacenan o son devueltas por la utilidad "env", es decir, "`<name>`=`<value>`". Esto puede
resultar práctico al depurar ciertos archivos de configuración que hacen un uso intensivo de
variables de entorno, para asegurarse de que contienen los valores esperados. Este comando está
restringido y solo puede emitirse en sockets configurados con niveles "operator" o "admin".

<a id="entry-9-3-show-errors"></a>

**`show errors [<iid>|<proxy>] [request|response]`**

```haproxy
show errors [<iid>|<proxy>] [request|response]
```

Vuelca los últimos errores de petición y respuesta HTTP/1.x conocidos, recogidos por los frontends
y los backends. Si se especifica `<iid>`, el volcado se limita a los errores que conciernen al
frontend o al backend cuyo ID es `<iid>`. El ID de proxy "-1" hará que se vuelquen todas las
instancias. Si en su lugar se especifica un nombre de proxy, su ID se usará como filtro. Si se
añade "request" o "response" después del nombre o ID del proxy, solo se volcarán los errores de
petición o de respuesta. Este comando está restringido y solo puede emitirse en sockets
configurados con niveles "operator" o "admin".

Los errores que pueden recogerse son los últimos errores de petición y respuesta causados por
violaciones del protocolo, a menudo debidas a caracteres no válidos en nombres de cabecera. El
informe indica con precisión qué carácter exacto violó el protocolo. También se informa de otra
información importante, como la fecha exacta en que se detectó el error, los nombres del frontend
y del backend, el nombre del servidor (cuando se conoce), el ID interno de la transacción y la
dirección de origen que inició la sesión.

Se devuelven todos los caracteres y los caracteres no imprimibles se codifican. Los más comunes
(&#92;t = 9, &#92;n = 10, &#92;r =
13 y &#92;e = 27) se codifican como una letra tras una barra invertida. La
propia barra invertida se codifica como '&#92;&#92;' para evitar
confusiones. Otros caracteres no imprimibles se codifican como '&#92;xNN', donde NN es
la representación hexadecimal de dos dígitos del código ASCII del carácter.

Las líneas llevan como prefijo la posición de su primer carácter, comenzando en 0 para el inicio
del búfer. Se imprime como máximo una línea de entrada por línea, y las líneas largas se
dividirán en varias líneas de salida consecutivas para que la salida nunca supere los 79
caracteres de ancho. Es fácil detectar si una línea se dividió, porque no terminará con
'&#92;n' y el desplazamiento de la línea siguiente irá seguido de un signo '+', lo
que indica que es una continuación de la línea anterior.

Ejemplo:

```shell
    $ echo "show errors -1 response" | socat stdio /tmp/sock1
>>> [04/Mar/2009:15:46:56.081] backend http-in (#2): invalid response
      src 127.0.0.1, session #54, frontend fe-eth0 (#1), server s2 (#1)
      response length 213 bytes, error at position 23:

      00000  HTTP/1.0 200 OK\r\n
      00017  header/bizarre:blah\r\n
      00038  Location: blah\r\n
      00054  Long-line: this is a very long line which should b
      00104+ e broken into multiple lines on the output buffer,
      00154+  otherwise it would be too large to print in a ter
      00204+ minal\r\n
      00211  \r\n

En el ejemplo anterior, vemos que el backend "http-in", cuyo ID interno es
2, ha bloqueado una respuesta no válida de su servidor s2, cuyo ID interno
es 1. La petición pertenecía a la transacción 54 (llamada "session" aquí),
iniciada por la fuente 127.0.0.1 y recibida por el frontend fe-eth0, cuyo
ID es 1. La longitud total de la respuesta era de 213 bytes cuando se detectó
el error, y el error estaba en el byte 23. Se trata de la barra ('/') en el
nombre de cabecera "header/bizarre", que no es un carácter HTTP válido para
un nombre de cabecera.
```

<a id="entry-9-3-show-events"></a>

**`show events [<sink>] [-w] [-n] [-0] [-s]`**

```haproxy
show events [<sink>] [-w] [-n] [-0] [-s]
```

Sin ninguna opción, lista todos los sumideros de eventos conocidos y sus tipos. Con una opción,
volcará todos los eventos disponibles en el sumidero designado si este es de tipo búfer. Si se
pasa la opción "-w" después del nombre del sumidero, una vez alcanzado el final del búfer, el
comando esperará nuevos eventos y los mostrará. Es posible detener la operación introduciendo
cualquier entrada (que será descartada) o cerrando la sesión. Finalmente, la opción "-n" se usa
para posicionarse directamente al final del búfer, lo que a menudo resulta práctico cuando se
combina con "-w" para informar solo de los eventos nuevos. Para mayor comodidad, pueden usarse
"-wn" o "-nw" para activar ambas opciones a la vez. Por defecto, todos los eventos están
delimitados por un carácter de salto de línea ('&#92;n' o 10 o 0x0A). Es posible
cambiarlo por el carácter NUL ('&#92;0' o 0) pasando el argumento "-0". La opción
"-s" sanea la salida, de modo que el contenido binario resultante de datos capturados o
decodificados no altere el renderizado del terminal. Los caracteres de espacio en blanco (espacio
y tabulación) se sustituyen por un espacio para que cada registro permanezca en una sola línea, y
los demás caracteres de control (0x00 a 0x1F y 0x7F), así como los caracteres no ASCII (0x80 y
superiores), se sustituyen por un '?'. La longitud de la salida se conserva. De esta forma,
volcar un anillo no puede inyectar secuencias de escape ANSI ni códigos de dirección de escritura
en el terminal del operador, lo cual es útil cuando se vuelca a un terminal o a un programa cuya
entrada no debe interpretarse como especial (p. ej., scripts de monitorización cuya salida se
copia literalmente en informes).

<a id="entry-9-3-show-fd"></a>

**`show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]`**

```haproxy
show fd [-!plcfbsd]* [[<tgid>]/[<fd>] | <fd>]
```

Vuelca la lista de todos los descriptores de archivo abiertos o solo la del número `<fd>` si se
especifica. También se acepta la forma "`<tgid>`/`<fd>`", donde cualquiera de los dos lados puede
quedar vacío como comodín ("/`<fd>`" para el fd `<fd>` en todos los grupos de hilos, "`<tgid>`/"
para todos los fds de `<tgid>`). El `<tgid>` actualmente se analiza pero se ignora, a la espera
de un futuro soporte de tablas de fd por grupo de hilos. Puede pasarse opcionalmente un conjunto
de flags para restringir el volcado solo a ciertos tipos de FD u omitir ciertos tipos de FD.
Cuando se encuentra '-' o '!', la selección se invierte para los caracteres siguientes del mismo
argumento. La inversión se restablece antes de cada palabra de argumento delimitada por espacios
en blanco. Los tipos de FD seleccionables incluyen 'p' para tuberías, 'l' para listeners, 'c'
para conexiones (de cualquier tipo), 'f' para conexiones de frontend, 'b' para conexiones de
backend (de cualquier tipo), 's' para conexiones a servidores, 'd' para conexiones a la dirección
"dispatch" o a la dirección transparente del backend. Con esto, 'b' es un atajo de 'sd' y 'c' de
'fb' o 'fsd'. 'c!f' es equivalente a 'b' (las "conexiones excepto las de frontend" son
efectivamente conexiones de backend). Esto está dirigido únicamente a desarrolladores que
necesitan observar estados internos para depurar problemas complejos como consumos anómalos de
CPU. Se informa de un fd por línea y, para cada uno, su estado en el poller usando letras
mayúsculas para los flags activados y minúsculas para los desactivados, usando "P" para "polled",
"R" para "ready", "A" para "active"; el estado de los eventos usando "H" para "hangup", "E" para
"error", "O" para "output", "P" para "priority" e "I" para "input"; algunos otros flags como "N"
para "new" (recién añadido a la caché de fds), "U" para "updated" (recibió una actualización en
la caché de fds), "L" para "linger_risk", "C" para "cloned"; luego la posición de la entrada en
caché, el puntero al propietario interno, el puntero al callback de E/S y su nombre cuando se
conoce. Cuando el propietario es una conexión, se informan los flags de la conexión y el destino
(frontend, proxy o servidor). Cuando el propietario es un listener, se informan el estado del
listener y su frontend. No tiene sentido usar este comando sin un buen conocimiento de las
interioridades. Merece la pena señalar que el formato de salida puede evolucionar con el tiempo,
por lo que esta salida no debe ser analizada por herramientas diseñadas para ser duraderas.
Algunos estados de estructuras internas pueden parecer sospechosos para la función que los
lista; en ese caso, la línea de salida llevará como sufijo un signo de exclamación ('!'). Esto
puede ayudar a encontrar un punto de partida al intentar diagnosticar un incidente.

<a id="entry-9-3-show-info"></a>

**`show info [typed|json] [desc] [float]`**

```haproxy
show info [typed|json] [desc] [float]
```

Vuelca información sobre el estado de haproxy en el proceso actual. Si se pasa "typed" como
argumento opcional, también se emiten los números, nombres y tipos de los campos, de manera que
los productos de monitorización externos puedan recuperar fácilmente, posiblemente agregar y
luego informar de la información encontrada en campos que no conocen. Cada campo se vuelca en su
propia línea. Si se pasa "json" como argumento opcional, la información proporcionada por la
salida "typed" se proporciona en formato JSON como una lista de objetos JSON. Por defecto, el
formato contiene solo dos columnas delimitadas por dos puntos (':'). La de la izquierda es el
nombre del campo y la de la derecha el valor. Es muy importante señalar que, en el formato de
salida tipado, el volcado de un solo objeto es contiguo, de modo que un consumidor no necesita
almacenarlo todo de una vez. Si se pasa "float" como argumento opcional, algunos campos
habitualmente emitidos como enteros pueden pasar a flotantes para mayor precisión. Se deja
deliberadamente sin especificar cuáles son los afectados, ya que esto puede evolucionar con el
tiempo. El uso de esta opción implica que el consumidor es capaz de procesar flotantes. El
formato de salida usado es sprintf("%f").

Al usar el formato de salida tipado, cada línea consta de 4 columnas delimitadas por dos puntos
(':'). La primera columna es una serie de 3 elementos separados por puntos. El primer elemento es
la posición numérica del campo en la lista (comenzando en cero). Esta posición no debe cambiar
con el tiempo, pero cabe esperar huecos, según las opciones de compilación o si algunos campos se
eliminan en el futuro. El segundo elemento es el nombre del campo tal como aparece en la salida
"show info" por defecto. El tercer elemento es el número relativo del proceso comenzando en 1.

El resto de la línea, a partir del primer carácter dos puntos, sigue el "formato de salida
tipado" descrito en la sección anterior. En resumen, la segunda columna (tras el primer ':')
indica el origen, la naturaleza y el ámbito de la variable. La tercera columna indica el tipo del
campo, entre "s32", "s64", "u32", "u64" y "str". La cuarta columna es el valor en sí, que el
consumidor sabe analizar gracias a la columna 3 y procesar gracias a la columna 2.

Así, el formato global de la línea en modo tipado es:

```text
<field_pos>.<field_name>.<process_num>:<tags>:<type>:<value>
```

Cuando se añade "desc" al comando, se añade un carácter dos puntos extra seguido de una cadena
entre comillas con una descripción de la métrica. En el momento de escribir esto, solo es
compatible con los formatos de salida "typed" y el predeterminado.

Ejemplo:

```shell
> show info
Name: HAProxy
Version: 1.7-dev1-de52ea-146
Release_date: 2016/03/11
Nbproc: 1
Process_num: 1
Pid: 28105
Uptime: 0d 0h00m04s
Uptime_sec: 4
Memmax_MB: 0
PoolAlloc_MB: 0
PoolUsed_MB: 0
PoolFailed: 0
(...)

> show info typed
0.Name.1:POSV:str:HAProxy
1.Version.1:POSV:str:3.1-dev0-7c653d-2466
2.Release_date.1:POSV:str:2025/07/01
3.Nbthread.1:CGSV:u32:1
4.Nbproc.1:CGSV:u32:1
5.Process_num.1:KGPV:u32:1
6.Pid.1:SGPV:u32:638069
7.Uptime.1:MDPV:str:0d 0h00m07s
8.Uptime_sec.1:MDPV:u32:7
9.Memmax_MB.1:CLPV:u32:0
10.PoolAlloc_MB.1:MGPV:u32:0
11.PoolUsed_MB.1:MGPV:u32:0
12.PoolFailed.1:MCPV:u32:0
(...)
```

En el formato tipado, la presencia del ID de proceso al final de la primera columna hace que sea
muy fácil agregar visualmente salidas de múltiples procesos. Ejemplo:

```shell
$ ( echo show info typed | socat /var/run/haproxy.sock1;    \
    echo show info typed | socat /var/run/haproxy.sock2 ) |  \
  sort -t . -k 1,1n -k 2,2 -k 3,3n
0.Name.1:POS:str:HAProxy
0.Name.2:POS:str:HAProxy
1.Version.1:POS:str:1.7-dev1-868ab3-148
1.Version.2:POS:str:1.7-dev1-868ab3-148
2.Release_date.1:POS:str:2016/03/11
2.Release_date.2:POS:str:2016/03/11
3.Nbproc.1:CGS:u32:2
3.Nbproc.2:CGS:u32:2
4.Process_num.1:KGP:u32:1
4.Process_num.2:KGP:u32:2
5.Pid.1:SGP:u32:30120
5.Pid.2:SGP:u32:30121
6.Uptime.1:MDP:str:0d 0h01m28s
6.Uptime.2:MDP:str:0d 0h01m28s
(...)
```

El formato de la salida JSON se describe en un esquema que puede emitirse usando "show schema
json".

La salida JSON no contiene espacios en blanco adicionales para reducir el volumen de salida. Para
consumo humano, pasar la salida por un formateador (pretty printer) puede resultar útil.
Ejemplo:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

La salida JSON no contiene espacios en blanco adicionales para reducir el volumen de salida. Para
consumo humano, pasar la salida por un formateador (pretty printer) puede resultar útil.
Ejemplo:

\$ echo "show info json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-libs"></a>

**`show libs`**

```haproxy
show libs
```

Vuelca la lista de bibliotecas dinámicas compartidas y archivos objeto cargados, en sistemas que
lo admiten. Cuando esté disponible, para cada objeto compartido se indicarán el rango de
direcciones virtuales, el tamaño y la ruta al objeto. Esto puede usarse, por ejemplo, para
intentar estimar qué biblioteca proporciona una función que aparece en un volcado. Ten en cuenta
que en muchos sistemas las direcciones cambiarán en cada reinicio (aleatorización del espacio de
direcciones), de modo que esta lista debería recuperarse en el arranque si se prevé usarla para
analizar un archivo core. Este comando solo puede emitirse en sockets configurados con niveles
"operator" o "admin". Ten en cuenta que el formato de salida puede variar entre sistemas
operativos, arquitecturas e incluso versiones de haproxy, y no deberías fiarte de él en scripts.

<a id="entry-9-3-show-map"></a>

**`show map [[@<ver>] <map>]`**

```haproxy
show map [[@<ver>] <map>]
```

Vuelca información sobre los conversores map. Sin argumento, se devuelve la lista de todos los
map disponibles. Si se especifica un `<map>`, se vuelca su contenido. `<map>` es el \#`<id>` o
`<name>`. Por defecto se muestra la versión actual del map (la versión contra la que se está
comparando actualmente y que se informa como 'curr_ver' en la lista de maps). Es posible volcar
en su lugar otras versiones anteponiendo '@`<ver>`' antes del identificador del map. La versión
funciona como un filtro y las versiones inexistentes simplemente no informarán de ningún
resultado. El valor 'entry_cnt' representa el recuento de todas las entradas del map, no solo las
activas, lo que significa que también incluye las entradas que se están añadiendo actualmente.

En la salida, la primera columna es un identificador único de entrada, utilizable como referencia
para las operaciones "del map" y "set map". La segunda columna es el patrón y la tercera columna
es la muestra si está disponible. Los datos devueltos no son directamente una lista de maps
disponibles, sino la lista de todos los patrones que componen cualquier map. Muchos de estos
patrones pueden compartirse con ACL.

<a id="entry-9-3-show-peers"></a>

**`show peers [dict|-] [<peers section>]`**

```haproxy
show peers [dict|-] [<peers section>]
```

Vuelca información sobre los peers configurados en secciones "peers". Sin argumento, se lista la
lista de los peers pertenecientes a todas las secciones "peers". Si se especifica `<peers
section>`, solo se vuelca la información sobre los peers pertenecientes a esta sección "peers".
Cuando se especifica "dict" antes del nombre de la sección peers, también se volcarán por
completo las cachés del diccionario Tx/Rx (muy grande). Pasar "-" puede ser necesario para volcar
una sección peers llamada "dict".

A continuación hay dos ejemplos de salidas donde los peers hostA, hostB y hostC pertenecen a
secciones peers "sharedlb". Solo hostA y hostB están conectados. Solo hostA ha enviado datos a
hostB.

\$ echo "show peers" \| socat - /tmp/hostA 0x55deb0224320: [15/Apr/2019:11:28:01] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=45122
0x55deb022b540: id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92;
reconnect=4s confirm=0 flags=0x0 0x55deb022a440: id=hostA(local) addr=127.0.0.10:10000 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55deb0227d70: id=hostB(remote)
addr=127.0.0.11:10001 status=ESTA reconnect=2s confirm=0 flags=0x20000200 appctx:0x55deb028fba0
st0=7 st1=0 task_calls=14456 &#92; state=EST xprt=RAW src=127.0.0.1:37257
addr=127.0.0.10:10000 remote_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1
last_local_table:0x55deb0224a10 id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55deb0224a10 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=0 last_pushed=3 last_get=0 teaching_origin=0 update=3
  table:0x55deb022d6a0 id=stkt update=3 localupdate=3 \
    commitupdate=3 syncing=0
```

\$ echo "show peers" \| socat - /tmp/hostB 0x55871b5ab320: [15/Apr/2019:11:28:03] id=sharedlb
state=0 flags=0x3 &#92; resync_timeout=`<PAST>` task_calls=3 0x55871b5b2540:
id=hostC(remote) addr=127.0.0.12:10002 status=CONN &#92; reconnect=3s
confirm=0 flags=0x0 0x55871b5b1440: id=hostB(local) addr=127.0.0.11:10001 status=NONE
&#92; reconnect=`<NEVER>` confirm=0 flags=0x0 0x55871b5aed70: id=hostA(remote)
addr=127.0.0.10:10000 status=ESTA &#92; reconnect=2s confirm=0
flags=0x20000200 appctx:0x7fa46800ee00 st0=7 st1=0 task_calls=62356 &#92;
state=EST remote_table:0x55871b5ab960 id=stkt local_id=1 remote_id=1 last_local_table:0x55871b5ab960
id=stkt local_id=1 remote_id=1 shared tables:

```text
0x55871b5ab960 local_id=1 remote_id=1 flags=0x0 remote_data=0x65
  last_acked=3 last_pushed=0 last_get=3 teaching_origin=0 update=0
  table:0x55871b5b46a0 id=stkt update=1 localupdate=0 \
    commitupdate=0 syncing=0
```

<a id="entry-9-3-show-pools"></a>

**`show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]`**

```haproxy
show pools [byname|bysize|byusage] [detailed] [match <pfx>] [<nb>]
```

Vuelca el estado de los pools de memoria internos. Esto es útil para rastrear el uso de memoria
cuando se sospecha, por ejemplo, de una fuga de memoria. Hace exactamente lo mismo que el SIGQUIT
cuando se ejecuta en primer plano, excepto que no vacía los pools. La salida no está ordenada por
defecto. Si se especifica "byname", se ordena por nombre de pool; si se especifica "bysize", se
ordena por tamaño de elemento en orden inverso; si se especifica "byusage", se ordena por uso
total en orden inverso y solo se muestran las entradas usadas. También es posible limitar la
salida a las `<nb>` primeras entradas (p. ej., al ordenar por uso). Es posible volcar también más
detalles internos, incluida la lista de todos los pools que se fusionaron, especificando
"detailed". Finalmente, si se especifica "match" seguido de un prefijo, solo se mostrarán los
pools cuyo nombre comience por ese prefijo. El total informado solo concierne a los pools que
coinciden con los criterios de filtrado. Ejemplo:

```shell
$ socat - /tmp/haproxy.sock <<< "show pools match quic byusage"
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool quic_conn_r (65560 bytes): 1337 allocated (87653720 bytes), ...
  - Pool quic_crypto (1048 bytes): 6685 allocated (7005880 bytes), ...
  - Pool quic_conn (4056 bytes): 1337 allocated (5422872 bytes), ...
  - Pool quic_rxbuf (262168 bytes): 8 allocated (2097344 bytes), ...
  - Pool quic_conne (184 bytes): 9359 allocated (1722056 bytes), ...
  - Pool quic_frame (184 bytes): 7938 allocated (1460592 bytes), ...
  - Pool quic_tx_pac (152 bytes): 6454 allocated (981008 bytes), ...
  - Pool quic_tls_ke (56 bytes): 12033 allocated (673848 bytes), ...
  - Pool quic_rx_pac (408 bytes): 1596 allocated (651168 bytes), ...
  - Pool quic_tls_se (88 bytes): 6685 allocated (588280 bytes), ...
  - Pool quic_cstrea (88 bytes): 4011 allocated (352968 bytes), ...
  - Pool quic_tls_iv (24 bytes): 12033 allocated (288792 bytes), ...
  - Pool quic_dgram (344 bytes): 732 allocated (251808 bytes), ...
  - Pool quic_arng (56 bytes): 4011 allocated (224616 bytes), ...
  - Pool quic_conn_c (152 bytes): 1337 allocated (203224 bytes), ...
Total: 15 pools, 109578176 bytes allocated, 109578176 used ...
```

<a id="entry-9-3-show-profiling"></a>

**`show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*`**

```haproxy
show profiling [{all | status | tasks | memory}] [byaddr|bytime|byctx|aggr|<max_lines>]*
```

Vuelca la configuración actual del profiling, una por línea, así como el comando necesario para
cambiarla. Cuando el profiling de tareas está activado, también se emitirán algunas estadísticas
por función recogidas por el planificador, con un resumen que cubre el número de llamadas, el
tiempo total/medio de CPU y la latencia total/media. Cuando el profiling de memoria está
activado, se informará de cierta información, como el número de asignaciones/liberaciones y sus
tamaños. Es posible limitar el volcado solo al estado del profiling, a las tareas o al profiling
de memoria especificando las palabras clave respectivas; por defecto se vuelca toda la
información del profiling. También es posible limitar el número de líneas de salida de cada
categoría especificando un límite numérico. Es posible solicitar que la salida se ordene por
dirección, por tiempo total de ejecución o por contexto de llamada en lugar de por uso, p. ej.
para facilitar comparaciones entre llamadas sucesivas o para comprobar qué debe optimizarse, y
agregar la actividad de las tareas por función llamada en lugar de ver los detalles. Ten en
cuenta que el profiling está esencialmente dirigido a los desarrolladores, ya que da pistas sobre
dónde se desperdician ciclos de CPU o memoria en el código. No hay nada útil que monitorizar ahí.

<a id="entry-9-3-show-resolvers"></a>

**`show resolvers [<resolvers section id>]`**

```haproxy
show resolvers [<resolvers section id>]
```

Vuelca estadísticas de la sección de resolutores dada, o de todas las secciones de resolutores
si no se suministra ninguna sección.

Para cada servidor de nombres, se informan los siguientes contadores:

```text
sent: número de peticiones DNS enviadas a este servidor
valid: número de respuestas DNS válidas recibidas de este servidor
update: número de respuestas DNS usadas para actualizar la dirección IP del servidor
cname: número de respuestas CNAME
cname_error: errores CNAME encontrados con este servidor
any_err: número de respuestas vacías (es decir, el servidor no admite el tipo ANY)
nx: respuesta de dominio inexistente recibida de este servidor
timeout: número de veces que este servidor no respondió a tiempo
refused: número de peticiones rechazadas por este servidor
other: cualquier otro error DNS
invalid: respuesta DNS no válida (desde el punto de vista del protocolo)
too_big: respuesta demasiado grande
outdated: número de respuestas llegadas demasiado tarde (después de otro servidor de nombres)
```

<a id="entry-9-3-show-quic"></a>

**`show quic [<format>] [<filter>]`**

```haproxy
show quic [<format>] [<filter>]
```

Vuelca información sobre todas las conexiones QUIC activas de los frontends. Este comando está
restringido y solo puede emitirse en sockets configurados con niveles "operator" o "admin".

Puede especificarse un argumento opcional para controlar la verbosidad. Su valor puede
interpretarse de diferentes maneras. La primera posibilidad es usar valores predefinidos:
"oneline" para el formato por defecto, "stream" para listar todos los streams activos y "full"
para mostrar toda la información. Alternativamente, puede especificarse una lista de campos
delimitados por comas para restringir la salida. Los valores actualmente admitidos son "tp",
"sock", "pktns", "cc" y "mux". Finalmente, "help" en el formato mostrará en su lugar un mensaje
de ayuda más detallado.

El argumento final se usa para restringir o ampliar la lista de conexiones. Por defecto, solo se
muestran las conexiones activas de frontend. Usa el argumento extra "clo" para listar en su lugar
las conexiones de frontend en cierre, "be" para las conexiones de backend o "all" para todas las
categorías. También es posible restringir a una única conexión especificando su dirección
hexadecimal.

<a id="entry-9-3-show-servers-conn"></a>

**`show servers conn [<backend>]`**

```haproxy
show servers conn [<backend>]
```

Vuelca el estado de las conexiones actuales e inactivas de los servidores pertenecientes al
backend designado (o a todos los backends si no se especifica ninguno). Puede usarse un nombre o
identificador de backend.

La salida consiste en una línea de cabecera que muestra los títulos de los campos y, a
continuación, un servidor por línea con, para cada uno, el nombre y el ID del backend, el nombre
y el ID del servidor, la dirección, el puerto y una serie de valores. El número de campos varía
según el número de hilos. El formato exacto de la salida puede variar ligeramente entre
versiones y dependiendo del número de hilos. Hay que prestar atención a la línea de cabecera
para hacer coincidir las columnas al extraer valores de la salida, y al número de hilos, ya que
las últimas columnas son por hilo:

```text
bkname/svname         Nombre del backend '/' nombre del servidor
bkid/svid             ID del backend '/' ID del servidor
addr                  Dirección IP del servidor
port                  Puerto del servidor (o cero si no tiene)
-                     Campo sin usar, sirve de delimitador visual
purge_delay           Intervalo entre purgas de conexiones, en milisegundos
served                Número de conexiones actualmente en uso
used_cur              Número de conexiones actualmente en uso
                      ten en cuenta que esto excluye las conexiones adjuntas a una sesión
used_max              Valor más alto de used_cur desde que empezó el proceso
need_est              Estimación variable del total de conexiones necesarias
idle_sess             Número de conexiones inactivas marcadas como privadas
unsafe_nb             Número de conexiones inactivas consideradas "unsafe"
safe_nb               Número de conexiones inactivas consideradas "safe"
idle_lim              Número máximo configurado de conexiones inactivas
idle_cur              Total de las conexiones actualmente inactivas por hilo
idle_per_thr[NB]      Conexiones inactivas por hilo para cada uno de los NB hilos
```

HAProxy matará una porción de `<idle_cur>` cada `<purge_delay>` cuando el total de `<idle_cur>` +
`<used_cur>` supere la estimación `<need_est>`. Esta estimación varía según la actividad de las
conexiones.

Dada la naturaleza multihilo de las conexiones inactivas, es importante entender que algunos
valores pueden cambiar una vez leídos y que, por tanto, no se garantiza la consistencia dentro de
una línea. Esta salida se proporciona principalmente como herramienta de depuración y no es
relevante monitorizarla de forma rutinaria ni graficarla.

<a id="entry-9-3-show-servers-state"></a>

**`show servers state [<backend>]`**

```haproxy
show servers state [<backend>]
```

Vuelca el estado de los servidores encontrados en la configuración en ejecución. Puede
proporcionarse un nombre o identificador de backend para limitar la salida solo a ese backend.

El volcado tiene el siguiente formato:

- la primera línea contiene la versión del formato (1 en esta especificación);
- la segunda línea contiene las cabeceras de las columnas, precedidas de una almohadilla ('#');
- la tercera línea y las siguientes contienen datos;
- cada línea que empieza por una almohadilla ('#') se considera un comentario.

Dado que pueden coexistir múltiples versiones de la salida, a continuación se muestra la lista de
campos y su orden por versión del formato de archivo:

```text
1:
  be_id:                       ID único del backend.
  be_name:                     Etiqueta del backend.
  srv_id:                      ID único del servidor (en el backend).
  srv_name:                    Etiqueta del servidor.
  srv_addr:                    Dirección IP del servidor.
  srv_op_state:                Estado operativo del servidor (UP/DOWN/...).
                                 0 = SRV_ST_STOPPED
                                   El servidor está caído.
                                 1 = SRV_ST_STARTING
                                   El servidor está arrancando progresivamente
                                   (disponible pero limitado).
                                 2 = SRV_ST_RUNNING
                                   El servidor está totalmente disponible.
                                 3 = SRV_ST_STOPPING
                                   El servidor está disponible pero en parada
                                   suave (p. ej., 404).
  srv_admin_state:             Estado administrativo del servidor (MAINT/DRAIN/...).
                               En realidad, el estado es una máscara de valores:
                                 0x01 = SRV_ADMF_FMAINT
                                   El servidor fue forzado explícitamente a
                                   mantenimiento.
                                 0x02 = SRV_ADMF_IMAINT
                                   El servidor ha heredado el estado de
                                   mantenimiento de un servidor seguido.
                                 0x04 = SRV_ADMF_CMAINT
                                   El servidor está en mantenimiento debido
                                   a la configuración.
                                 0x08 = SRV_ADMF_FDRAIN
                                   El servidor fue forzado explícitamente al
                                   estado "drain".
                                 0x10 = SRV_ADMF_IDRAIN
                                   El servidor ha heredado el estado "drain"
                                   de un servidor seguido.
                                 0x20 = SRV_ADMF_RMAINT
                                   El servidor está en mantenimiento debido a
                                   un fallo de resolución de la dirección IP.
                                 0x40 = SRV_ADMF_HMAINT
                                   El FQDN del servidor se estableció desde el
                                   socket de estadísticas.

  srv_uweight:                 Peso del servidor visible para el usuario.
  srv_iweight:                 Peso inicial del servidor.
  srv_time_since_last_change:  Tiempo desde el último cambio operativo.
  srv_check_status:            Estado de la última comprobación de estado.
  srv_check_result:            Último resultado de la comprobación (FAILED/PASSED/...).
                                 0 = CHK_RES_UNKNOWN
                                   Inicializado a esto por defecto.
                                 1 = CHK_RES_NEUTRAL
                                   Comprobación válida pero sin información de estado.
                                 2 = CHK_RES_FAILED
                                   La comprobación falló.
                                 3 = CHK_RES_PASSED
                                   La comprobación tuvo éxito y el servidor
                                   vuelve a estar totalmente disponible.
                                 4 = CHK_RES_CONDPASS
                                   La comprobación reporta que el servidor no
                                   quiere nuevas sesiones.
  srv_check_health:            Contador actual de rise / fall de las comprobaciones.
  srv_check_state:             Estado de la comprobación (ENABLED/PAUSED/...).
                               En realidad, el estado es una máscara de valores:
                                 0x01 = CHK_ST_INPROGRESS
                                   Hay una comprobación en ejecución actualmente.
                                 0x02 = CHK_ST_CONFIGURED
                                   Esta comprobación está configurada y puede
                                   activarse.
                                 0x04 = CHK_ST_ENABLED
                                   Esta comprobación está actualmente activada
                                   administrativamente.
                                 0x08 = CHK_ST_PAUSED
                                   Las comprobaciones están en pausa debido al
                                   mantenimiento (solo las de estado).
  srv_agent_state:             Estado de la comprobación de agente (ENABLED/PAUSED/...).
                               Este estado usa los mismos valores de máscara que
                               "srv_check_state", añadiendo este específico:
                                 0x10 = CHK_ST_AGENT
                                   La comprobación es de agente (si no, es una
                                   comprobación de estado).
  bk_f_forced_id:              Indicador para saber si el ID del backend está
                               forzado por la configuración.
  srv_f_forced_id:             Indicador para saber si el ID del servidor está
                               forzado por la configuración.
  srv_fqdn:                    FQDN del servidor.
  srv_port:                    Puerto del servidor.
  srvrecord:                   Registro DNS SRV asociado a este SRV.
  srv_use_ssl:                 usar ssl para las conexiones del servidor.
  srv_check_port:              Puerto de la comprobación de estado del servidor.
  srv_check_addr:              Dirección de la comprobación de estado del servidor.
  srv_agent_addr:              Dirección de la comprobación de agente del servidor.
  srv_agent_port:              Puerto de la comprobación de agente del servidor.
```

<a id="entry-9-3-show-sess"></a>

**`show sess [<options>*]`**

```haproxy
show sess [<options>*]
```

Vuelca todos los streams activos conocidos (antes llamados "sesiones"). Evita hacer esto en
conexiones lentas, ya que la salida puede ser enorme. Este comando está restringido y solo puede
emitirse en sockets configurados con niveles "operator" o "admin". Ten en cuenta que en máquinas
con conexiones recicladas rápidamente, es posible que esta salida informe de menos entradas de
las que realmente existen, porque volcará todos los streams existentes hasta el último que se
creó antes de introducir el comando; los que mueran mientras tanto no aparecerán. Para las
opciones admitidas, ver más abajo.

<a id="entry-9-3-show-sess-2"></a>

**`show sess [<id> | all | help] [<options>*]`**

```haproxy
show sess [<id> | all | help] [<options>*]
```

Muestra mucha información interna sobre los streams que coinciden. El comando conoce dos formatos
de salida: uno corto, que es el predeterminado cuando no se solicita un identificador de stream
específico, y uno extendido al listar streams designados. El formato corto, usado por defecto con
"show sess", solo vuelca un stream por línea con poca información, y el identificador del stream
al principio de la línea en hexadecimal (corresponde al puntero al stream).

En la forma extendida, usada por "show sess `<id>`" o "show sess all", los streams se vuelcan con
una enorme cantidad de detalles de depuración en múltiples líneas (unas 20 cada uno), y siguen
comenzando con su identificador. El delimitador entre streams aquí es el identificador al
principio de la línea; las líneas extra pertenecientes al mismo stream comienzan con uno o varios
espacios (el stream se vuelca indentado). Volcar muchos streams puede producir una salida enorme,
llevar mucho tiempo y consumir mucha CPU, así que siempre es mejor volcar solo el mínimo
necesario. Esta información es inútil para la mayoría de los usuarios, pero puede ser usada por
los desarrolladores de HAProxy para solucionar un bug complejo. El formato exacto de salida está
deliberadamente sin documentar para que pueda evolucionar libremente según las necesidades,
incluido en ramas estables. Esta salida está pensada para interpretarse mientras se consulta la
función strm_dump_to_buffer() en src/stream.c para averiguar el significado exacto de ciertos
campos.

El argumento "help" mostrará el uso detallado del comando en lugar de volcar streams.

Es posible establecer algunas opciones para personalizar el volcado o aplicar algunos filtros.
Estas son las opciones admitidas: - backend `<b>` muestra solo los streams adjuntos a este
backend - frontend `<f>` muestra solo los streams adjuntos a este frontend - older `<age>` muestra
solo los streams con más de `<age>` segundos - server `<b/s>` muestra solo los streams adjuntos a
este backend+servidor - show-uri vuelca la URI de la transacción, tal como se capturó durante el
análisis de la petición. Solo se muestra si fue capturada. - susp muestra solo los streams
considerados sospechosos por los desarrolladores según criterios que pueden cambiar con el tiempo
o variar entre versiones.

<a id="entry-9-3-show-stat"></a>

**`show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \`**

```haproxy
show stat [domain <resolvers|proxy>] [{<iid>|<proxy>} <type> <sid>] \
          [typed|json] [desc] [up|no-maint]
```

Vuelca estadísticas. El dominio se usa para seleccionar qué estadísticas imprimir; por ahora
están disponibles resolvers y proxy. Por defecto se usa el formato CSV; puedes activar el formato
de salida tipado extendido descrito en la sección anterior si se pasa "typed" después de los
demás argumentos; o en JSON si se pasa "json" después de los demás argumentos. Pasando `<id>`,
`<type>` y `<sid>`, es posible volcar solo los elementos seleccionados: - `<iid>` es un ID de
proxy, -1 para volcarlo todo. Alternativamente, puede especificarse un nombre de proxy
`<proxy>`. En este caso, el ID de ese proxy se usará como selector de ID. - `<type>` selecciona
el tipo de objetos volcables: 1 para frontends, 2 para backends, 4 para servidores, -1 para todo.
Estos valores pueden combinarse con OR, por ejemplo:

```text
1 + 2     = 3   -> frontend + backend.
1 + 2 + 4 = 7   -> frontend + backend + server.
```

    - `<sid>` es un ID de servidor, -1 para volcar todo lo del proxy seleccionado.

Ejemplo:

```shell
    $ echo "show info;show stat" | socat stdio unix-connect:/tmp/sock1
>>> Name: HAProxy
    Version: 1.4-dev2-49
    Release_date: 2009/09/23
    Nbproc: 1
    Process_num: 1
    (...)

    # pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,  (...)
    stats,FRONTEND,,,0,0,1000,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,1,0, (...)
    stats,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,0,0,0,,0,250,(...)
    (...)
    www1,BACKEND,0,0,0,0,1000,0,0,0,0,0,,0,0,0,0,UP,1,1,0,,0,250, (...)

    $
```

En este ejemplo se han emitido dos comandos a la vez. De este modo es fácil saber a qué proceso
se aplican las estadísticas en modo multiproceso. Esto no es necesario en el formato de salida
tipado, ya que el número de proceso se informa en cada línea. Observa la línea vacía tras la
salida de información, que marca el final del primer bloque. Aparece una línea vacía similar al
final del segundo bloque (stats) para que el lector sepa que la salida no ha sido truncada.

Cuando se especifica "typed", el formato de salida es más adecuado para herramientas de
monitorización porque proporciona posiciones numéricas e indica el tipo de cada campo de salida.
Cada valor está en su propia línea con el número de proceso, el número de elemento, la naturaleza,
el origen y el ámbito. Este mismo formato está disponible vía las estadísticas HTTP pasando
";typed" tras la URI. Es muy importante señalar que, en el formato de salida tipado, el volcado
de un solo objeto es contiguo, de modo que un consumidor no necesita almacenarlo todo de una vez.

El modificador "up" hará que solo se listen los servidores que están activos (up) o sin
comprobar. Los que están caídos (down), sin resolver o en mantenimiento no se listarán. Esto es
análogo a la opción ";up" de las estadísticas HTTP. De forma similar, el modificador "no-maint"
actuará como el modificador HTTP ";no-maint" y hará que los servidores desactivados no se
listen. La diferencia es que los que están activados pero caídos no serán excluidos.

Al usar el formato de salida tipado, cada línea consta de 4 columnas delimitadas por dos puntos
(':'). La primera columna es una serie de 5 elementos separados por puntos. El primer elemento es
una letra que indica el tipo del objeto descrito. Por el momento se conocen los siguientes tipos
de objeto: 'F' para un frontend, 'B' para un backend, 'L' para un listener y 'S' para un
servidor. El segundo elemento El segundo elemento es un entero positivo que representa el
identificador único del proxy al que pertenece el objeto. Es equivalente a la columna "iid" de la
salida CSV y coincide con el valor frente a la directiva opcional "id" que se encuentra en la
sección del frontend o del backend. El tercer elemento es un entero positivo que contiene el
identificador único del objeto dentro del proxy, y corresponde a la columna "sid" de la salida
CSV. El ID 0 se informa al volcar un frontend o un backend. Para un listener o un servidor, esto
corresponde a su respectivo ID dentro del proxy. El cuarto elemento es la posición numérica del
campo en la lista (comenzando en cero). Esta posición no debe cambiar con el tiempo, pero cabe
esperar huecos, según las opciones de compilación o si algunos campos se eliminan en el futuro.
El quinto elemento es el nombre del campo tal como aparece en la salida CSV. El sexto elemento es
un entero positivo y es el número relativo de proceso comenzando en 1.

El resto de la línea, a partir del primer carácter dos puntos, sigue el "formato de salida
tipado" descrito en la sección anterior. En resumen, la segunda columna (tras el primer ':')
indica el origen, la naturaleza, el ámbito y el estado de persistencia de la variable. La tercera
columna indica el tipo del campo, entre "s32", "s64", "u32", "u64", "flt" y "str". La cuarta
columna es el valor en sí, que el consumidor sabe analizar gracias a la columna 3 y procesar
gracias a la columna 2.

Cuando se añade "desc" al comando, se añade un carácter dos puntos extra seguido de una cadena
entre comillas con una descripción de la métrica. En el momento de escribir esto, solo es
compatible con el formato de salida "typed".

Así, el formato global de la línea en modo tipado es:

```text
<obj>.<px_id>.<id>.<fpos>.<fname>.<process_num>:<tags>:<type>:<value>
```

A continuación hay un ejemplo del formato de salida tipado:

```shell
$ echo "show stat typed" | socat stdio unix-connect:/tmp/sock1
F.2.0.0.pxname.1:KNSV:str:dummy
F.2.0.1.svname.1:KNSV:str:FRONTEND
F.2.0.4.scur.1:MGPV:u32:0
F.2.0.5.smax.1:MMPV:u32:0
F.2.0.6.slim.1:CLPV:u32:524269
F.2.0.7.stot.1:MCPP:u64:0
F.2.0.8.bin.1:MCPP:u64:0
F.2.0.9.bout.1:MCPP:u64:0
F.2.0.10.dreq.1:MCPP:u64:0
F.2.0.11.dresp.1:MCPP:u64:0
F.2.0.12.ereq.1:MCPP:u64:0
F.2.0.17.status.1:SGPV:str:OPEN
F.2.0.26.pid.1:KGPV:u32:1
F.2.0.27.iid.1:KGSV:u32:2
F.2.0.28.sid.1:KGSV:u32:0
F.2.0.32.type.1:CGSV:u32:0
F.2.0.33.rate.1:MRPP:u32:0
F.2.0.34.rate_lim.1:CLPV:u32:0
F.2.0.35.rate_max.1:MMPV:u32:0
F.2.0.46.req_rate.1:MRPP:u32:0
F.2.0.47.req_rate_max.1:MMPV:u32:0
F.2.0.48.req_tot.1:MCPP:u64:0
F.2.0.51.comp_in.1:MCPP:u64:0
F.2.0.52.comp_out.1:MCPP:u64:0
F.2.0.53.comp_byp.1:MCPP:u64:0
F.2.0.54.comp_rsp.1:MCPP:u64:0
(...)
```

En el formato tipado, la presencia del ID de proceso al final de la primera columna hace que sea
muy fácil agregar visualmente salidas de múltiples procesos, como se muestra en el ejemplo
siguiente, donde cada línea aparece por cada proceso:

```shell
$ ( echo show stat typed | socat /var/run/haproxy.sock1 -; \
    echo show stat typed | socat /var/run/haproxy.sock2 - ) | \
  sort -t . -k 1,1 -k 2,2n -k 3,3n -k 4,4n -k 5,5 -k 6,6n
B.3.0.0.pxname.1:KNSV:str:private-backend
B.3.0.0.pxname.2:KNSV:str:private-backend
B.3.0.1.svname.1:KNSV:str:BACKEND
B.3.0.1.svname.2:KNSV:str:BACKEND
B.3.0.2.qcur.1:MGPV:u32:0
B.3.0.2.qcur.2:MGPV:u32:0
B.3.0.3.qmax.1:MMPV:u32:0
B.3.0.3.qmax.2:MMPV:u32:0
B.3.0.4.scur.1:MGPV:u32:0
B.3.0.4.scur.2:MGPV:u32:0
B.3.0.5.smax.1:MMPV:u32:0
B.3.0.5.smax.2:MMPV:u32:0
B.3.0.6.slim.1:CLPV:u32:1000
B.3.0.6.slim.2:CLPV:u32:1000
(...)
```

El formato de la salida JSON se describe en un esquema que puede emitirse usando "show schema
json".

La salida JSON no contiene espacios en blanco adicionales para reducir el volumen de salida. Para
consumo humano, pasar la salida por un formateador (pretty printer) puede resultar útil.
Ejemplo:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

La salida JSON no contiene espacios en blanco adicionales para reducir el volumen de salida. Para
consumo humano, pasar la salida por un formateador (pretty printer) puede resultar útil.
Ejemplo:

\$ echo "show stat json" \| socat /var/run/haproxy.sock stdio \| &#92; python
-m json.tool

<a id="entry-9-3-show-ssl-ca-file"></a>

**`show ssl ca-file [[*][\]<cafile>[:<index>]]`**

```haproxy
show ssl ca-file [[*][\]<cafile>[:<index>]]
```

Muestra la lista de archivos CA cargados en el proceso y sus respectivos recuentos de
certificados. Los certificados no son usados por ningún frontend ni backend hasta que su estado
sea "Used". Puede aparecer en la lista una entrada "@system-ca"; la carga el httpclient por
defecto. Contiene la lista de CA de confianza de tu sistema devuelta por OpenSSL. Si un nombre de
archivo va precedido de un asterisco, es una transacción que aún no se ha confirmado. Si se
especifica un `<cafile>` sin `<index>`, mostrará el estado del archivo CA ("Used"/"Unused")
seguido de detalles sobre todos los certificados contenidos en el archivo CA. Los detalles
mostrados para cada certificado son los mismos que los mostrados por un comando "show ssl cert".
Si se especifica un `<cafile>` seguido de un `<index>`, solo mostrará los detalles del
certificado que tiene el índice especificado. Los índices comienzan en 1. Si el índice no es
válido (demasiado grande, por ejemplo), no se mostrará nada. Este comando puede ser útil para
comprobar si un archivo CA se actualizó correctamente. También puedes mostrar los detalles de una
transacción en curso prefijando el nombre de archivo con un '*'. Si el primer carácter del nombre
de archivo es un '*', puede escaparse con '&#92;\*'.

Ejemplo:

```shell
$ echo "show ssl ca-file" | socat /var/run/haproxy.master -
# transaction
*cafile.crt - 2 certificate(s)
# filename
cafile.crt - 1 certificate(s)

$ echo "show ssl ca-file cafile.crt" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Used

Certificate #1:
Serial: 11A4D2200DC84376E7D233CAFF39DF44BF8D1211
notBefore: Apr  1 07:40:53 2021 GMT
notAfter: Aug 17 07:40:53 2048 GMT
Subject Alternative Name:
Algorithm: RSA4096
SHA1 FingerPrint: A111EF0FEFCDE11D47FE3F33ADCA8435EBEA4864
Subject: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA
Issuer: /C=FR/ST=Some-State/O=HAProxy Technologies/CN=HAProxy Technologies CA

$ echo "show ssl ca-file *cafile.crt:2" | socat /var/run/haproxy.master -
Filename: */home/tricot/work/haproxy/reg-tests/ssl/set_cafile_ca2.crt
Status: Unused

Certificate #2:
Serial: 587A1CE5ED855040A0C82BF255FF300ADB7C8136
[...]
```

<a id="entry-9-3-show-ssl-cert"></a>

**`show ssl cert [[*][\]<filename>]`**

```haproxy
show ssl cert [[*][\]<filename>]
```

Muestra la lista de certificados cargados en el proceso. No son usados por ningún frontend ni
backend hasta que su estado sea "Used". Si un nombre de archivo va precedido de un asterisco, es
una transacción que aún no se ha confirmado. Si se especifica un nombre de archivo, mostrará
detalles sobre el certificado. Este comando puede ser útil para comprobar si un certificado se
actualizó bien. También puedes mostrar los detalles de una transacción prefijando el nombre de
archivo con un '*'. Si el primer carácter del nombre de archivo es un '*', puede escaparse con
'&#92;\*'. Este comando también puede usarse para mostrar los detalles de la respuesta OCSP de un
certificado añadiendo al nombre de archivo un sufijo con la extensión ".ocsp". Funciona tanto con
certificados confirmados como con transacciones en curso. Sobre un certificado confirmado, este
comando equivale a llamar a "show ssl ocsp-response" con el ID de respuesta OCSP correspondiente
del certificado.

Ejemplo:

```shell
$ echo "@1 show ssl cert" | socat /var/run/haproxy.master -
# transaction
*test.local.pem
# filename
test.local.pem

$ echo "@1 show ssl cert test.local.pem" | socat /var/run/haproxy.master -
Filename: test.local.pem
Status: Used
Serial: 03ECC19BA54B25E85ABA46EE561B9A10D26F
notBefore: Sep 13 21:20:24 2019 GMT
notAfter: Dec 12 21:20:24 2019 GMT
Issuer: /C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
Subject: /CN=test.local
Subject Alternative Name: DNS:test.local, DNS:imap.test.local
Algorithm: RSA2048
SHA1 FingerPrint: 417A11CAE25F607B24F638B4A8AEE51D1E211477

$ echo "@1 show ssl cert *test.local.pem" | socat /var/run/haproxy.master -
Filename: *test.local.pem
Status: Unused
[...]

$ echo "@1 show ssl cert \*.local.pem" | socat /var/run/haproxy.master -
Filename: *.local.pem
Status: Used
[...]
```

<a id="entry-9-3-show-ssl-crl-file"></a>

**`show ssl crl-file [[*][\]<crlfile>[:<index>]]`**

```haproxy
show ssl crl-file [[*][\]<crlfile>[:<index>]]
```

Muestra la lista de archivos CRL cargados en el proceso. No son usados por ningún frontend ni
backend hasta que su estado sea "Used". Si un nombre de archivo va precedido de un asterisco, es
una transacción que aún no se ha confirmado. Si se especifica un `<crlfile>` sin `<index>`,
mostrará el estado del archivo CRL ("Used"/"Unused") seguido de detalles sobre todas las listas
de revocación contenidas en el archivo CRL. Los detalles mostrados para cada lista se basan en la
salida de "openssl crl -text -noout -in `<file>`". Si se especifica un `<crlfile>` seguido de un
`<index>`, solo mostrará los detalles de la lista que tiene el índice especificado. Los índices
comienzan en 1. Si el índice no es válido (demasiado grande, por ejemplo), no se mostrará nada.
Este comando puede ser útil para comprobar si un archivo CRL se actualizó correctamente. También
puedes mostrar los detalles de una transacción en curso prefijando el nombre de archivo con un
'*'. Si el primer carácter del nombre de archivo es un '*', puede escaparse con
'&#92;\*'.

Ejemplo:

```shell
$ echo "show ssl crl-file" | socat /var/run/haproxy.master -
# transaction
*crlfile.pem
# filename
crlfile.pem

$ echo "show ssl crl-file crlfile.pem" | socat /var/run/haproxy.master -
Filename: /home/tricot/work/haproxy/reg-tests/ssl/crlfile.pem
Status: Used

Certificate Revocation List #1:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Intermediate CA2
Last Update: Apr 23 14:45:39 2021 GMT
Next Update: Sep  8 14:45:39 2048 GMT
Revoked Certificates:
    Serial Number: 1008
        Revocation Date: Apr 23 14:45:36 2021 GMT

Certificate Revocation List #2:
Version 1
Signature Algorithm: sha256WithRSAEncryption
Issuer: /C=FR/O=HAProxy Technologies/CN=Root CA
Last Update: Apr 23 14:30:44 2021 GMT
Next Update: Sep  8 14:30:44 2048 GMT
No Revoked Certificates.
```

<a id="entry-9-3-show-ssl-crt-list"></a>

**`show ssl crt-list [-n] [<filename>]`**

```haproxy
show ssl crt-list [-n] [<filename>]
```

Muestra la lista de crt-list y directorios usados en la configuración de HAProxy. Si se
especifica un nombre de archivo, vuelca el contenido de una crt-list o de un directorio. Una vez
volcado, la salida puede usarse como archivo crt-list. La opción '-n' puede usarse para mostrar
el número de línea, lo cual es útil combinado con la opción 'del ssl crt-list' cuando una entrada
está duplicada. La salida con la opción '-n' no es compatible con el formato crt-list y no la
puede cargar haproxy.

Ejemplo:

```shell
echo "show ssl crt-list -n localhost.crt-list" | socat /tmp/sock1 -
# localhost.crt-list
common.pem:1 !not.test1.com *.test1.com !localhost
common.pem:2
ecdsa.pem:3 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3] localhost !www.test1.com
ecdsa.pem:4 [verify none allow-0rtt ssl-min-ver TLSv1.0 ssl-max-ver TLSv1.3]
```

<a id="entry-9-3-show-ssl-ech"></a>

**`show ssl ech [<name>]`**

```haproxy
show ssl ech [<name>]
```

Muestra la lista de claves ECH cargadas en el proceso de HAProxy.

Cuando se especifica `<name>`, muestra las claves de una línea bind específica. El formato de la
línea bind es `<frontend>`/@`<filename>`:`<linenum>` (Ejemplo:
frontend1/@haproxy.conf:19) o `<frontend>`/`<name>` si la línea bind fue nombrada con la palabra
clave "name".

La entrada 'age' representa el tiempo, en segundos, desde que la clave se cargó en la línea bind.
Este valor se restablece cuando HAProxy se inicia, se recarga o se reinicia.

Requiere una versión de OpenSSL que admita ECH, y HAProxy debe compilarse con USE_ECH=1. Este
comando solo es compatible con una conexión CLI que se ejecute en modo experimental (ver
"experimental-mode on").

Ver también "ech" en la [Sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1) del manual de configuración.

Ejemplo:

```shell
$ echo "experimental-mode on; show ssl ech" | socat /tmp/haproxy.sock -
 ***
 frontend: frontend1

 bind: frontend1/@haproxy.conf:19

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

 bind: frontend1/@haproxy.conf:20

 ECH entry: 0 public_name: example.com age: 557 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

 ECH entry: 1 public_name: example.com age: 557 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]

$ echo "experimental-mode on; show ssl ech frontend1/@haproxy.conf:19" | socat /tmp/haproxy.sock -
***
ECH for frontend1/@haproxy.conf:19
ECH entry: 0 public_name: example.com age: 786 (has private key)
      [fe0d,94,example.com,[0020,0001,0001],c39285b774bf61c071864181c5292a012b30adaf767e39369a566af05573ef2b,00,00]

ECH entry: 1 public_name: example.com age: 786 (has private key)
      [fe0d,ee,example.com,[0020,0001,0001],6572191131b5cabba819f8cacf2d2e06fa0b87b30d9b793644daba7b8866d511,00,00]
```

<a id="entry-9-3-show-ssl-jwt"></a>

**`show ssl jwt`**

```haproxy
show ssl jwt
```

Muestra la lista de certificados que pueden usarse para la validación de JWT. Ver también los
comandos "add ssl jwt" y "del ssl jwt". Ver la opción de certificado "jwt" para más información.

Ejemplo:

```shell
echo "show ssl jwt"  | socat /tmp/sock1 -
#filename
jwt.pem
```

<a id="entry-9-3-show-ssl-ocsp-response"></a>

**`show ssl ocsp-response [[text|base64] <id|path>]`**

```haproxy
show ssl ocsp-response [[text|base64] <id|path>]
```

Muestra los IDs de las entradas del árbol OCSP correspondientes a todas las respuestas OCSP
usadas en HAProxy, así como la ruta del certificado del frontend correspondiente, el nombre y el
hash de clave del emisor, y el número de serie del certificado para el que se construyó la
respuesta OCSP. Si se proporciona un `<id>` válido o la `<path>` de un certificado de frontend
válido, muestra el contenido de la respuesta OCSP correspondiente. Cuando se proporciona un
`<id>`, es posible definir el formato en el que se vuelcan los datos. La opción 'text' es la
predeterminada y permite mostrar información detallada sobre la respuesta OCSP igual que en una
llamada "openssl ocsp -respin `<ocsp-response>` -text". El formato 'base64' permite volcar el
contenido de una respuesta OCSP en base64.

Ejemplo:

```shell
$ echo "show ssl ocsp-response" | socat /var/run/haproxy.master -
# Certificate IDs
  Certificate ID key: 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a
  Certificate path: /path_to_cert/foo.pem
    Certificate ID:
      Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
      Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
      Serial Number: 100A

$ echo "show ssl ocsp-response 303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a0202100a" | socat /var/run/haproxy.master -
OCSP Response Data:
  OCSP Response Status: successful (0x0)
  Response Type: Basic OCSP Response
  Version: 1 (0x0)
  Responder Id: C = FR, O = HAProxy Technologies, CN = ocsp.haproxy.com
  Produced At: May 27 15:43:38 2021 GMT
  Responses:
  Certificate ID:
    Hash Algorithm: sha1
    Issuer Name Hash: 8A83E0060FAFF709CA7E9B95522A2E81635FDA0A
    Issuer Key Hash: F652B0E435D5EA923851508F0ADBE92D85DE007A
    Serial Number: 100A
  Cert Status: good
  This Update: May 27 15:43:38 2021 GMT
  Next Update: Oct 12 15:43:38 2048 GMT
  [...]

$ echo "show ssl ocsp-response base64 /path_to_cert/foo.pem" | socat /var/run/haproxy.sock -
  MIIB8woBAKCCAewwggHoBgkrBgEFBQcwAQEEggHZMIIB1TCBvqE[...]
```

<a id="entry-9-3-show-ssl-ocsp-updates"></a>

**`show ssl ocsp-updates`**

```haproxy
show ssl ocsp-updates
```

Muestra información sobre las entradas afectadas por el mecanismo de actualización OCSP. El
comando emitirá una línea por respuesta OCSP y contendrá la hora esperada de actualización de la
respuesta, así como la hora de la última actualización correcta y contadores de actualizaciones
correctas y fallidas. También dará el estado de la última actualización (correcta o no) en forma
numérica así como en forma de texto. Ver más abajo la lista completa de posibles errores. Las
líneas se ordenarán por hora 'Next Update' ascendente. Las líneas contendrán también una ruta al
primer certificado de frontend que usa la respuesta OCSP. Ver el comando "show ssl ocsp-response"
y la opción "ocsp-update" para más información sobre la actualización automática OCSP.

Los códigos de error de actualización y las cadenas de error pueden ser los siguientes:

```text
  +----+-------------------------------------+
  | ID | message                             |
  +----+-------------------------------------+
  |  0 | "Unknown"                           |
  |  1 | "Update successful"                 |
  |  2 | "HTTP error"                        |
  |  3 | "Missing \"ocsp-response\" header"  |
  |  4 | "OCSP response check failure"       |
  |  5 | "Error during insertion"            |
  +----+-------------------------------------+
```

Ejemplo:

```shell
$ echo "show ssl ocsp-updates" | socat /tmp/haproxy.sock -
  OCSP Certid | Path | Next Update | Last Update | Successes | Failures | Last Update Status | Last Update Status (str)
      303b300906052b0e03021a050004148a83e0060faff709ca7e9b95522a2e81635fda0a0414f652b0e435d5ea923851508f0adbe92d85de007a02021015 | /path_to_cert/cert.pem | 30/Jan/2023:00:08:09 +0000 | - | 0 | 1 | 2 | HTTP error
      304b300906052b0e03021a0500041448dac9a0fb2bd32d4ff0de68d2f567b735f9b3c40414142eb317b75856cbae500940e61faf9d8b14c2c6021203e16a7aa01542f291237b454a627fdea9c1 | /path_to_cert/other_cert.pem | 30/Jan/2023:01:07:09 +0000 | 30/Jan/2023:00:07:09 +0000 | 1 | 0 | 1 | Update successful
```

<a id="entry-9-3-show-ssl-providers"></a>

**`show ssl providers`**

```haproxy
show ssl providers
```

Muestra los nombres de los proveedores cargados por OpenSSL durante el arranque (init). La carga
de proveedores puede efectivamente configurarse vía el archivo de configuración de OpenSSL y esta
opción permite comprobar que se cargaron los proveedores correctos. Este comando solo está
disponible con OpenSSL v3.

Ejemplo:

```shell
$ echo "show ssl providers" | socat /var/run/haproxy.master -
Loaded providers:
    - fips
    - base
```

<a id="entry-9-3-show-ssl-sni"></a>

**`show ssl sni [-f <frontend>] [-A] [-t <offset>]`**

```haproxy
show ssl sni [-f <frontend>] [-A] [-t <offset>]
```

Vuelca cada SNI configurado para el frontend designado, o todos los frontends si no se especificó
ninguno. Permite ver qué SNI se ofrecen para un frontend e identificar si un SNI está definido
varias veces por múltiples certificados para el mismo frontend.

La opción -A permite filtrar la lista y muestra solo los certificados que han pasado la fecha
notAfter, lo que permite mostrar solo los certificados caducados.

La opción -t toma un desplazamiento en segundos, o con una unidad de tiempo (s, m, h, d), que se
suma a la hora actual, lo que permite comprobar qué certificados estarán caducados al aplicar el desplazamiento
cuando se combina con -A. Por ejemplo, si quieres comprobar qué certificados estarían caducados
en 30d, basta con hacer "show ssl sni -A -t 30d".

Las columnas están separadas por un único &#92;t, lo que permite analizarla de forma sencilla.

La columna 'Frontend/Bind' muestra el nombre del frontend seguido de la posición de la línea bind
en la configuración (frontend/file:linenum).

La columna 'SNI' muestra el SNI; puede ser un CN, un SAN o un filtro de una crt-list. Los
certificados predeterminados de una línea bind (declarados explícitamente con 'default-crt' o,
implícitamente, el primer certificado de una línea bind cuando no se usa 'strict-sni') muestran
el carácter '\*' en la columna SNI.

La columna 'Negative Filter' es la lista de filtros negativos asociados a un comodín; mostrará
todos los filtros negativos que están en la misma línea de la crt-list. Se muestra un guion si
no hay ninguno.

La columna 'Type' muestra el tipo de algoritmo de cifrado; puede ser "rsa", "ecdsa" o "dsa".

La columna 'Filename' puede ser un nombre de archivo de la configuración o un alias declarado en
un crt-store.

Las columnas 'NotAfter' y 'NotBefore' se extraen directamente del certificado X509 hoja.

Ejemplo:

```shell
$ echo "@1 show ssl sni -A -t 30d" | socat /var/run/haproxy-master.sock - | column -t -s $'\t'
# Frontend/Bind        SNI        Negative Filter  Type   Filename             NotAfter                  NotBefore
li1/haproxy.cfg:10021  *.ex.lan   !m1.ex.lan       rsa    example.lan.pem      Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                rsa    machine10.pem.rsa    Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  machine10  -                ecdsa  machine10.pem.ecdsa  Jun 13 13:37:21 2024 GMT  May 14 13:37:21 2024 GMT
li1/haproxy.cfg:10021  localhost  -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
li1/haproxy.cfg:10021  localhost  -                ecdsa  localhost.pem.ecdsa  Jun 13 13:37:10 2024 GMT  May 14 13:37:10 2024 GMT
li1/haproxy.cfg:10021  *          -                rsa    localhost.pem.rsa    Jun 13 13:37:11 2024 GMT  May 14 13:37:11 2024 GMT
```

<a id="entry-9-3-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

Vuelca todos los mensajes emitidos durante el arranque del proceso haproxy actual; cada búfer
startup-logs es único de su worker haproxy.

Esta palabra clave también existe en la CLI maestra, que muestra el último intento de arranque o
recarga.

<a id="entry-9-3-show-table"></a>

**`show table`**

```haproxy
show table
```

Vuelca información general sobre todas las stick-tables conocidas. Se devuelve su nombre (el
nombre del proxy que las contiene), su tipo (actualmente cero, siempre IP), su tamaño en número
máximo posible de entradas y el número de entradas actualmente en uso.

Ejemplo:

```shell
    $ echo "show table" | socat stdio /tmp/sock1
>>> # table: front_pub, type: ip, size:204800, used:171454
>>> # table: back_rdp, type: ip, size:204800, used:0
```

<a id="entry-9-3-show-table-2"></a>

**`show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |`**

```haproxy
show table <name> [ data.<type> <operator> <value> [data.<type> ...]] |
                  [ key <key> ] | [ ptr <ptr> ]
```

Vuelca el contenido de la stick-table `<name>`. En este modo, se informa primero de una línea de
información genérica sobre la tabla, como con "show table", y luego se vuelcan todas las
entradas. Dado que esto puede ser bastante pesado, es posible especificar un filtro para
concretar qué entradas mostrar.

Cuando se usa la forma "data.", el filtro se aplica a los datos almacenados (ver "stick-table"
en la sección 4.2). Debe especificarse un tipo de dato almacenado en `<type>`, y este tipo de
dato debe estar almacenado en la tabla; de lo contrario se informa de un error. Los datos se
comparan según `<operator>` con el entero de 64 bits `<value>`. Los operadores son los mismos
que con las ACL:

    - eq: coincide con las entradas cuyo dato es igual a este valor
    - ne: coincide con las entradas cuyo dato no es igual a este valor
    - le: coincide con las entradas cuyo dato es menor o igual que este valor
    - ge: coincide con las entradas cuyo dato es mayor o igual que este valor
    - lt: coincide con las entradas cuyo dato es menor que este valor
    - gt: coincide con las entradas cuyo dato es mayor que este valor

En esta forma puedes usar múltiples entradas de filtro de datos, hasta un máximo definido en
tiempo de compilación (4 por defecto).

Cuando se usa la forma key, se muestra la entrada `<key>`. La clave debe ser del mismo tipo que
la tabla, lo que actualmente se limita a IPv4, IPv6, entero y cadena.

Cuando se usa la forma ptr, se muestra la entrada `<ptr>`. `<ptr>` se escribe en la forma 0xffff
y debe corresponder a la dirección devuelta por un comando "show table" anterior. Identificar una entrada mediante su puntero puede ser pertinente si la entrada no puede identificarse mediante la clave
debido a una clave vacía o caracteres incompatibles en la CLI.

Si data.`<type>` es un tipo array, puede usarse "[]" para acceder a un índice específico del
array, así: data.gpt[1]

Ejemplo:

```shell
    $ echo "show table http_proxy" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a4c: key=127.0.0.1 use=0 exp=3594729 gpc0=0 conn_rate(30000)=1  \
      bytes_out_rate(60000)=187
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.gpc0 gt 0" | socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy data.conn_rate gt 5" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy key 127.0.0.2" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191

    $ echo "show table http_proxy ptr 0x80e6a80" | \
        socat stdio /tmp/sock1
>>> # table: http_proxy, type: ip, size:204800, used:2
>>> 0x80e6a80: key=127.0.0.2 use=0 exp=3594740 gpc0=1 conn_rate(30000)=10 \
      bytes_out_rate(60000)=191
```

Cuando el criterio de datos se aplica a un valor dinámico dependiente del tiempo, como una tasa
de bytes, el valor se calcula dinámicamente durante la evaluación de la entrada para decidir si
debe volcarse o no. Esto significa que tal filtro podría coincidir durante un tiempo y luego
dejar de coincidir porque, con el paso del tiempo, la tasa media de eventos baja.

Es posible usar esto para extraer listas de direcciones IP que abusan del servicio, para
monitorizarlas o incluso incluirlas en una lista negra en un firewall. Ejemplo:

```shell
$ echo "show table http_proxy data.gpc0 gt 0" \
  | socat stdio /tmp/sock1 \
  | fgrep 'key=' | cut -d' ' -f2 | cut -d= -f2 > abusers-ip.txt
  ( o | awk '/key/{ print a[split($2,a,"=")]; }' )
```

Cuando la stick-table está sincronizada con una sección peers que admite sharding, se mostrará
el número de shard para cada clave (de lo contrario se informa '0'). Esto permite saber qué
peers recibirán esta clave. Ejemplo:

```shell
$ echo "show table http_proxy" | socat stdio /tmp/sock1 | fgrep shard=
  0x7f23b0c822a8: key=10.0.0.2 use=0 exp=296398 shard=9 gpc0=0
  0x7f23a063f948: key=10.0.0.6 use=0 exp=296075 shard=12 gpc0=0
  0x7f23b03920b8: key=10.0.0.8 use=0 exp=296766 shard=1 gpc0=0
  0x7f23a43c09e8: key=10.0.0.12 use=0 exp=295368 shard=8 gpc0=0
```

<a id="entry-9-3-show-tasks"></a>

**`show tasks`**

```haproxy
show tasks
```

Vuelca el número de tareas actualmente en la cola de ejecución, con el número de apariciones de
cada función y su latencia media cuando se conoce (para tareas puras con el profiling de tareas
activado). El volcado es una instantánea del instante en que se hace, y puede haber variaciones
dependiendo de qué tareas queden en la cola en el momento en que ocurre, especialmente en modo
de un solo hilo, ya que hay menos probabilidad de que las E/S rellenen la cola (a menos que la
cola esté llena). Este comando toma acceso exclusivo al proceso y puede causar latencias menores
pero medibles cuando se emite en un proceso muy cargado, así que no debe abusar de él un bot de
monitorización.

<a id="entry-9-3-show-threads"></a>

**`show threads`**

```haproxy
show threads
```

Vuelca algunos estados y estructuras internas de cada hilo, lo que puede ser útil para ayudar a
los desarrolladores a entender un problema. La salida intenta ser legible mostrando un bloque
por hilo. Cuando haproxy se construye con USE_THREAD_DUMP=1, se usa un mecanismo avanzado de
volcado que implica señales de hilo, de modo que cada hilo pueda volcar su propio estado por
turnos. Sin esta opción, el hilo que procesa el comando muestra todos sus detalles, pero los
demás son menos detallados. Se muestra una estrella ('\*') delante del hilo que maneja el
comando. También puede mostrarse un corchete angular derecho ('\>') delante de hilos que no
hayan progresado desde la última invocación de este comando, lo que indica un bug en el código
que debe reportarse sin falta. Cuando esto ocurre entre dos hilos suele indicar un bloqueo
mutuo (deadlock). Si un hilo está solo, es un bug diferente, como una lista corrupta. En todos
los casos, el proceso ya no es totalmente funcional y necesita ser reiniciado.

El formato de salida está deliberadamente sin documentar para que pueda evolucionar fácilmente
a medida que se identifiquen nuevas necesidades, sin tener que mantener ninguna forma de
compatibilidad hacia atrás, e igual que con "show activity", los valores carecen de sentido sin
el código a mano.

<a id="entry-9-3-show-tls-keys"></a>

**`show tls-keys [id|*]`**

```haproxy
show tls-keys [id|*]
```

Vuelca todas las referencias de claves de tickets TLS cargadas. Se muestran el ID de referencia
de la clave de ticket TLS y el archivo desde el que se cargaron las claves. Ambos pueden usarse
para actualizar las claves TLS usando "set ssl tls-key". Si se especifica un ID como parámetro,
volcará los tickets; usando \* volcará todas las claves de todas las referencias.

<a id="entry-9-3-show-schema-json"></a>

**`show schema json`**

```haproxy
show schema json
```

Vuelca el esquema usado para la salida de "show info json" y "show stat json".

La salida no contiene espacios en blanco adicionales para reducir el volumen de salida. Para
consumo humano, pasar la salida por un formateador (pretty printer) puede resultar útil.
Ejemplo:

\$ echo "show schema json" \| socat /var/run/haproxy.sock stdio \| &#92;
python -m json.tool

El esquema sigue "JSON Schema" (json-schema.org) y, en consecuencia, pueden usarse verificadores
para comprobar contra el esquema la salida de "show info json" y "show stat json".

<a id="entry-9-3-show-trace"></a>

**`show trace [<source>]`**

```haproxy
show trace [<source>]
```

Muestra el estado actual del trazado. Para cada fuente se muestra una línea con un estado de un
solo carácter que indica si el trazado está detenido, en espera o en ejecución. Se indica el
sumidero de salida usado por el trazado (o "none" si no se configuró ninguno), así como el número
de eventos descartados en ese sumidero, seguido de una breve descripción de la fuente. Si se
especifica un nombre de fuente, se muestra una lista detallada de todos los eventos admitidos
por la fuente y su estado para cada acción (report, start, pause, stop), indicado con un "+" si
están activados o un "-" en caso contrario. Todos estos eventos son independientes y un evento
podría desencadenar un inicio sin ser reportado, y viceversa.

<a id="entry-9-3-show-version"></a>

**`show version`**

```haproxy
show version
```

Muestra la versión del proceso HAProxy actual. Esto está disponible desde la CLI del master y de
los workers. Ejemplo:

```shell
$ echo "show version" | socat /var/run/haproxy.sock stdio
2.4.9

$ echo "show version" | socat /var/run/haproxy-master.sock stdio
2.5.0
```

<a id="entry-9-3-shutdown-frontend"></a>

**`shutdown frontend <frontend>`**

```haproxy
shutdown frontend <frontend>
```

Elimina por completo el frontend especificado. Se liberarán todos los puertos a los que estaba
enlazado. No será posible activar el frontend nunca más tras esta operación. Está pensado para
usarse en entornos donde detener un proxy es impensable pero un proxy mal configurado debe
corregirse. De este modo es posible liberar el puerto y enlazarlo en otro proceso para restaurar
las operaciones. El frontend no aparecerá en absoluto en la página de estadísticas una vez
terminado.

El frontend puede especificarse por su nombre o por su ID numérico, precedido de una almohadilla
('#').

Este comando está restringido y solo puede emitirse en sockets configurados con nivel "admin".

<a id="entry-9-3-shutdown-session"></a>

**`shutdown session <id>`**

```haproxy
shutdown session <id>
```

Termina inmediatamente el stream que coincide con el identificador de stream especificado. Este
identificador es el primer campo al principio de las líneas en los volcados de "show sess"
(corresponde al puntero del stream). Esto puede usarse para terminar un stream de larga duración
sin esperar un timeout o cuando hay una transferencia interminable en curso. Dichos streams
terminados se reportan con un flag 'K' en los registros.

<a id="entry-9-3-shutdown-sessions-server"></a>

**`shutdown sessions server <backend>/<server>`**

```haproxy
shutdown sessions server <backend>/<server>
```

Termina inmediatamente todos los streams adjuntos al servidor especificado. Esto puede usarse
para terminar streams de larga duración después de poner un servidor en modo mantenimiento, por
ejemplo. Dichos streams terminados se reportan con un flag 'K' en los registros.

Las conexiones de backend se dejan en estado inactivo, salvo que el servidor ya esté en modo
mantenimiento, en cuyo caso se programarán inmediatamente para su eliminación.

<a id="entry-9-3-trace"></a>

**`trace`**

```haproxy
trace
```

El comando "trace" por sí solo lista las fuentes de trazado, su estado actual y sus breves
descripciones. Solo pretende ser un menú para entrar en los niveles siguientes; ver los demás
comandos "trace" más abajo.

<a id="entry-9-3-trace-0"></a>

**`trace 0`**

```haproxy
trace 0
```

Detiene inmediatamente todos los trazados. Está hecho para usarse como una solución rápida para
terminar una sesión de depuración o como una acción de emergencia para usar en caso de que se
hayan activado trazados complejos en múltiples fuentes y afecten al servicio.

<a id="entry-9-3-trace-2"></a>

**`trace <source> [<args...>]`**

```haproxy
trace <source> [<args...>]
```

Configura los trazados para la fuente `<source>`. Sin argumento, listará todos los subcomandos
admitidos para la fuente dada. Pueden encadenarse múltiples subcomandos. Se admiten los
siguientes subcomandos:

event [ [+\|-\|!]`<name>` ] Sin argumento, listará todos los eventos admitidos por la fuente
designada. Van precedidos de un "-" si no están activados o de un "+" si lo están. Es importante
señalar que un único trazado puede estar etiquetado con múltiples eventos y, mientras cualquiera
de los eventos activados coincida con uno de los eventos etiquetados en el trazado, el evento se
pasará al subsistema de trazado. Por ejemplo, recibir una trama HTTP/2 de tipo HEADERS puede
desencadenar un evento de trama y un evento de stream, ya que la trama crea un nuevo stream. Si
el evento de trama o el evento de stream están activados para esta fuente, la trama se pasará al
framework de trazado.

    Con un argumento, es posible alternar el estado de cada evento y activarlos o
    desactivarlos individualmente. Se admiten dos palabras clave especiales:
    "none", que no coincide con ningún evento y se usa para desactivar todos
    los eventos a la vez, y "any", que coincide con todos los eventos y se usa
    para activarlos todos a la vez. Los demás eventos son específicos de la
    fuente de eventos. Es posible activar un evento especificando su nombre,
    opcionalmente precedido de '+' para una mejor legibilidad. Es posible
    desactivar un evento especificando su nombre precedido de un '-' o un '!'.

    Una forma de desactivar por completo una fuente de trazado es pasar
    "event none", y esta fuente será ignorada totalmente al instante.

follow `<other_source>` Esto permite que la fuente `<source>` emita también trazados cuando la
otra fuente `<other_source>` está bloqueada sobre un criterio y el mismo criterio coincide
también para la fuente actual. Por ejemplo, si una fuente está bloqueada sobre una sesión,
seguir esa fuente desde otra hará que esa otra emita trazados para todos los eventos
relacionados con esta sesión. Esto puede usarse hasta cierto punto para rastrear las peticiones
del backend junto con las conexiones del frontend asociadas. La fuente "session" facilita esto
proporcionando eventos "new" y "end" que son utilizables para el procesamiento de bloqueo
(lock-on). Ten en cuenta que la fuente `<source>` no necesita tener sus trazados activados en
este caso, y su estado de trazado tampoco se verá afectado. Sin embargo, es posible que falten
algunos eventos si no contienen información que permita correlacionarlos con el elemento
rastreado. La metafuente "all" también puede usarse con este comando: en este caso, todas las
fuentes seguirán a `<other_source>`.

Ejemplo:

```text
trace h1 lock session start sess_new pause sess_end follow session
```

level [`<level>`] Sin argumento, listará todos los niveles de trazado de esta fuente, y el
actual se indicará con una estrella ('\*') antepuesta delante. Con un argumento, cambiará el
nivel de trazado al nivel especificado. Los niveles de detalle son una forma de filtros que se
aplican antes de reportar los eventos. Estos filtros se usan para incluir o excluir eventos de
forma selectiva según su nivel de importancia. Por ejemplo, un desarrollador podría necesitar
saber con precisión en qué parte del código se consideró inválida una cabecera HTTP, mientras
que al usuario final puede que ni le importe la validez de esa cabecera. Actualmente existen 5
niveles distintos para un trazado:

```text
user       reportará información adecuada para el uso por parte de un usuario
           habitual de haproxy que quiera observar su tráfico.
           Normalmente se reportarán algunas peticiones y respuestas HTTP sin
           mucho detalle. La mayoría de las fuentes establecerán este como el
           nivel por defecto para facilitar las operaciones.

proto      además de lo que se reporta en el nivel "user", también muestra
           actualizaciones a nivel del protocolo. Por ejemplo, los tipos de
           trama o las cabeceras HTTP tras el decodificado.

state      además de lo que se reporta en el nivel "proto", también mostrará
           las transiciones de estado (o transiciones fallidas) que ocurren
           en los analizadores, por lo que esto mostrará los intentos de
           realizar una operación, mientras que el nivel "proto" solo
           muestra la operación final.

data       además de lo que se reporta en el nivel "state", también incluirá
           las transferencias de datos entre las diversas capas.

developer  reporta todo lo disponible, lo que puede incluir información
           avanzada como "breaking out of this loop", que solo es relevante
           para un desarrollador que intenta entender un fallo que solo
           ocurre de vez en cuando en el terreno. Los nombres de función
           solo se reportan en este nivel.
```

    Es muy recomendable usar siempre solo el nivel "user" y cambiar a
    otros niveles solo si lo indica un desarrollador. También es buena idea
    configurar primero los eventos antes de cambiar a niveles superiores,
    ya que puede ahorrar el volcado de muchas líneas si no se aplica
    ningún filtro. La metafuente "all" también puede usarse con este
    comando: en este caso, el nivel se aplicará a todas las fuentes
    existentes a la vez.

lock [criterion] Sin argumento, listará todos los criterios admitidos por esta fuente para el
procesamiento de bloqueo (lock-on), y mostrará la elección actual con una estrella ('\*')
delante. Bloqueo (lock-on) significa que la fuente se centrará en el primer evento que coincida
y se ceñirá solo al criterio que desencadenó ese evento, ignorando todos los demás hasta que se
detenga el trazado. Esto permite, por ejemplo, tomar un trazado de una única conexión o de un
único stream. Los siguientes criterios son admitidos por algunos trazados, aunque no
necesariamente por todos, ya que algunos podrían no estar disponibles para la fuente:

```text
backend      bloquea sobre el backend que inició el trazado
connection   bloquea sobre la conexión que inició el trazado
frontend     bloquea sobre el frontend que inició el trazado
listener     bloquea sobre la escucha que inició el trazado
nothing      no bloquea sobre nada
server       bloquea sobre el servidor que inició el trazado
session      bloquea sobre la sesión que inició el trazado
thread       bloquea sobre el hilo que inició el trazado
```

    Además de esto, cada fuente puede proporcionar hasta 4 criterios
    específicos, como estados internos o IDs de conexión. Por ejemplo, en
    HTTP/2 es posible bloquearse en el stream H2 e ignorar otros streams
    una vez que comienza un strace.

    Cuando se pasa un criterio como argumento, este se usa en lugar de los
    demás y cualquier rastreo existente termina inmediatamente para que
    pueda reiniciarse con el nuevo criterio. La palabra clave especial
    "nothing" está admitida por todas las fuentes para desactivar el
    rastreo permanentemente.

{ pause \| start \| stop } [ [+\|-\|!]event] Sin argumento, listará los eventos activados para
pausar, iniciar o detener automáticamente un trazado de esta fuente. Estos eventos son
específicos de cada fuente de trazado. Con un argumento, activará el evento para la acción
especificada (si va precedido opcionalmente de un '+') o lo desactivará (si va precedido de un
'-' o '!'). La palabra clave especial "now" no es un evento y solicita tomar la acción
inmediatamente. Las palabras clave "none" y "any" están admitidas igual que en "trace event".

    Las 3 acciones admitidas son respectivamente "pause", "start" y "stop".
    La acción "pause" enumera los eventos que provocarán que un trazado en
    ejecución se detenga y espere un nuevo evento de inicio para
    reiniciarlo. La acción "start" enumera los eventos que conmutan el
    trazado al modo de espera hasta que aparezca uno de los eventos de
    inicio. Y la acción "stop" enumera los eventos que detienen
    definitivamente el trazado hasta que se vuelva a activar manualmente.
    En la práctica, tiene sentido iniciar manualmente un trazado usando
    "start now" sin preocuparse de los eventos, y detenerlo con "stop
    now". Para capturar secuencias de eventos más sutiles, configurar
    "start" en un evento normal (como recibir una petición HTTP) y "stop"
    en un evento muy raro, como emitir un determinado error, garantizará
    que los últimos eventos capturados coincidan con los criterios
    deseados. Y el evento de pausa es útil para detectar el final de una
    secuencia, desactivar el bloqueo (lock-on) y esperar otra oportunidad
    para tomar una captura. En este caso puede tener sentido activar el
    bloqueo para detectar solo un criterio específico (p. ej., un
    stream), tener "start" configurado en cualquier cosa que inicie ese
    criterio (p. ej., todos los eventos que crean un stream), "stop" en
    la anomalía esperada y "pause" en cualquier cosa que finalice ese
    criterio (p. ej., cualquier evento de fin de stream). En este caso, el
    registro de trazado contendrá secuencias completas de series
    perfectamente limpias que afectan a un único objeto, hasta la última
    secuencia que contiene todo, desde el principio hasta la anomalía.

sink [`<sink>`] Sin argumento, listará todos los sumideros de eventos disponibles para esta
fuente, y el configurado actualmente llevará una estrella ('\*') antepuesta delante. El sumidero
"none" está siempre disponible y significa que todos los eventos simplemente se descartan,
aunque su procesamiento no se ignora (p. ej., el bloqueo sí ocurre). Otros sumideros están
disponibles según la configuración y las opciones de compilación, pero normalmente "stdout" y
"stderr" serán utilizables en modo depuración, y los búferes circulares en memoria deberían
estar también disponibles. Cuando se especifica un nombre, el sumidero cambia al instante para
la fuente especificada. Los eventos no se modifican durante un cambio de sumidero. En el peor
de los casos, algunos podrían perderse si se usa un sumidero no válido (o "none"), pero las
operaciones continúan hacia un destino diferente. La metafuente "all" también puede usarse con
este comando: en este caso, el sumidero se aplicará a todas las fuentes existentes a la vez.

verbosity [`<level>`] Sin argumento, listará todos los niveles de verbosidad de esta fuente, y
el actual se indicará con una estrella ('\*') antepuesta delante. Con un argumento, cambiará el
nivel de verbosidad al especificado.

    Los niveles de verbosidad indican hasta dónde debe llegar el decodificador
    de trazado para proporcionar información detallada. Depende de la fuente
    de trazado, ya que algunas fuentes ni siquiera proporcionarán un
    decodificador específico. El nivel "quiet" está siempre disponible y
    desactiva cualquier decodificación. Puede ser útil cuando se intenta
    averiguar qué está pasando antes de intentar entender los detalles, ya
    que tendrá un impacto muy bajo en el rendimiento y en el tamaño del
    trazado. Cuando una fuente no declara niveles de verbosidad, el nivel
    "default" está disponible y hará que se llame a un decodificador cuando
    se especifique en los trazados. Es una decodificación oportunista.
    Cuando la fuente declara algunos niveles de verbosidad, estos se listan
    con una descripción de a qué corresponden. En este caso, el decodificador
    de trazado proporcionado por la fuente será lo más preciso posible según
    la información disponible en el punto de trazado. El primer nivel por
    encima de "quiet" se establece por defecto.

<a id="entry-9-3-update-ssl-ocsp-response"></a>

**`update ssl ocsp-response <certfile>`**

```haproxy
update ssl ocsp-response <certfile>
```

Crea una petición OCSP para el `<certfile>` especificado y la envía al respondedor OCSP cuya URI
debería estar especificada en la sección "Authority Information Access" del certificado. Solo se
tiene en cuenta la primera URI. La respuesta OCSP que deberíamos recibir a cambio se comprueba y
se inserta en el árbol local de respuestas OCSP. Este comando solo funcionará con certificados
que ya tenían almacenada una respuesta OCSP, bien porque se proporcionó durante el arranque
(init) o porque se estableció previamente mediante los comandos "set ssl cert" o "set ssl
ocsp-response". Si la respuesta OCSP recibida es válida y se insertó correctamente en el árbol
local, su contenido se mostrará en la salida estándar. El formato es el mismo que el descrito en
"show ssl ocsp-response".

<a id="entry-9-3-wait"></a>

**`wait { -h | <delay> } [<condition> [<args>...]]`**

```haproxy
wait { -h | <delay> } [<condition> [<args>...]]
```

En su forma más simple, sin ninguna condición, simplemente espera el retardo solicitado antes de
continuar. Esto puede usarse para recopilar métricas en torno a un intervalo específico.

Con una condición y argumentos opcionales, el comando esperará a que la condición especificada se
cumpla, falle de forma irrecuperable o permanezca incumplida durante toda la duración del
`<delay>`. Las condiciones admitidas son:

- be-removable `<proxy>`: esperará a que el backend del proxy especificado sea eliminable por el
  comando "del backend". Algunas condiciones nunca serán aceptadas (p. ej., backend que aún no se ha despublicado o con servidores en él) y provocarán el informe de un mensaje de error específico
  que indica qué condición no se cumple. Si todo está bien antes del retardo, se devuelve un
  éxito y la operación termina.

- srv-removable `<proxy>`/`<server>`: esperará a que el servidor especificado sea eliminable por
  el comando "del server", es decir, estar en mantenimiento y no tener ya ninguna conexión en él
  (ni activa ni inactiva). Algunas condiciones nunca serán aceptadas (p. ej., no estar en
  mantenimiento) y provocarán el informe de un mensaje de error específico que indica qué
  condición no se cumple. El servidor podría incluso haber sido eliminado en paralelo y ya no
  existir. Si todo está bien antes del retardo, se devuelve un éxito y la operación termina.

La unidad por defecto para el retardo es el milisegundo, aunque se aceptan otras unidades si van
sufijadas con las unidades de temporizador habituales (us, ms, s, m, h, d). Cuando se use con la
utilidad 'socat', no olvides extender el timeout de cierre de socat para cubrir el tiempo de
espera. Pasar "-h" como primer o segundo argumento muestra el uso del comando. Ejemplo:

```shell
$ socat -t20 /path/to/socket - <<< "show activity; wait 10s; show activity"

$ socat -t5 /path/to/socket - <<< "
    disable server px/srv1
    shutdown sessions server px/srv1
    wait 2s srv-removable px/srv1
    del server px/srv1"
```

## 9.4. CLI maestra {#section-9-4}

La CLI maestra es un socket enlazado al proceso maestro en modo maestro-worker. Esta CLI da
acceso a los comandos del socket unix en todos los procesos en ejecución o en proceso de salida,
y permite una supervisión básica de esos procesos.

La CLI maestra solo es configurable desde los argumentos del programa haproxy con la opción -S.
Esta opción también admite opciones bind separadas por comas.

Ejemplo:

```haproxy
# haproxy -W -S 127.0.0.1:1234 -f test1.cfg
# haproxy -Ws -S /tmp/master-socket,uid,1000,gid,1000,mode,600 -f test1.cfg
# haproxy -W -S /tmp/master-socket,level,user -f test1.cfg
```

### 9.4.1. Comandos de la CLI maestra {#section-9-4-1}

<a id="entry-9-4-1-entry"></a>

**`@<[!]pid>`**

```haproxy
@<[!]pid>
```

La CLI maestra usa una notación especial de prefijo para acceder a los múltiples procesos. Esta
notación es fácilmente identificable porque comienza por una @.

Un prefijo @ puede ir seguido de un número de proceso relativo o de un signo de exclamación y un
PID (p. ej., @1 o @!1271). Una @ sola puede usarse para especificar el master. Los procesos en
proceso de salida solo son accesibles con el PID, ya que los números relativos de proceso solo
son utilizables con los procesos actuales.

Este prefijo puede usarse como envoltorio antes de un comando, lo que indica que ese comando y
solo ese se enviará al proceso designado. En este caso, el comando completo termina al final de
línea o en el punto y coma, como cualquier comando normal.

Bugs: se sabe que el protocolo sockpair@ usado para implementar la comunicación entre el master
y el worker no es fiable en macOS debido a un problema en la implementación de sendmsg(2) de
macOS. Un comando podría quedarse sin respuesta por ello.

Ejemplos:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1 show info; @2 show info
[...]
Process_num: 1
Pid: 1271
[...]
Process_num: 2
Pid: 1272
[...]
master>

$ echo '@!1271 show info; @!1272 show info' | socat /var/run/haproxy-master.sock -
[...]
```

El prefijo también puede usarse como comando independiente para conmutar el contexto de
ejecución por defecto al proceso designado, lo que indica que todos los comandos posteriores se
ejecutarán todos en ese proceso, hasta que un nuevo comando '@' vuelva a cambiar el contexto de
ejecución.

Ejemplos:

```shell
$ socat /var/run/haproxy-master.sock readline
prompt
master> @1
1271> show info
[...]
1271> show stat
[...]
1271> @
master>

$ echo '@1; show info; show stat; @2; show info; show stat' | socat /var/run/haproxy-master.sock -
[...]
```

Nota sobre limitaciones: unos pocos comandos raros alteran el estado de una sesión CLI (p. ej.
"set anon", "set timeout") y podrían no comportarse exactamente igual cuando se ejecutan desde la
CLI maestra, debido a que los comandos se envían de uno en uno en su propia sesión CLI. De forma
similar, unos pocos comandos raros ("show events", "wait") monitorizan activamente la CLI en
busca de entrada o cierre y se interrumpen inmediatamente cuando la CLI se cierra. Estos
comandos no funcionarán como se espera a través de la CLI maestra porque la entrada del comando
se cierra tras cada comando. Para estos casos poco comunes, la variante "@@" de más abajo podría
ser más adecuada.

<a id="entry-9-4-1-entry-2"></a>

**`@@<[!]pid> [command...]`**

```haproxy
@@<[!]pid> [command...]
```

Este prefijo o comando es muy similar al prefijo "@" documentado más arriba, excepto en que
entra en el proceso worker, entrega la línea de comandos completa en él tal cual y permanece allí
hasta que el comando termina. Los puntos y coma también se entregan, lo que permite ejecutar un
comando completo con pipeline en un proceso worker. La conexión con el worker permanece abierta
hasta que la lista de comandos se completa. Cualquier dato enviado después de los comandos se
reenviará a la CLI del proceso worker y podría ser consumido por los comandos en ejecución y se
perderá para la CLI del proceso maestro, ofreciendo una conexión verdaderamente bidireccional
con el proceso worker. Por ello, los usuarios de tales comandos deben tener mucho cuidado de
esperar la finalización del comando antes de enviar nuevos comandos a la CLI maestra.

En lugar de ejecutar un solo comando, también es posible abrir una sesión totalmente interactiva
en el proceso worker sin especificar ningún comando (es decir, "@@1" en su propia línea). Esta
sesión puede terminarse cerrando la conexión o saliendo del proceso worker (usando el comando
"quit"). En este caso, el modo de prompt del socket maestro (interactive, prompt, timed) se
propaga al proceso worker.

Bugs: se sabe que el protocolo sockpair@ usado para implementar la comunicación entre el master
y el worker no es fiable en macOS debido a un problema en la implementación de sendmsg(2) de
macOS. Un comando podría quedarse sin respuesta por ello.

Ejemplos:

```shell
# gracefully close connections and delete a server once idle (wait max 10s)
$ socat -t 11 /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   wait 10000 srv-removable app2/srv36; \
   del server app2/srv36"

# forcefully close connections and quickly delete a server
$ socat /var/run/haproxy-master.sock - <<< \
   "@@1 disable server app2/srv36; \
   shutdown sessions server app2/srv36; \
   wait 100 srv-removable app2/srv36; \
   del server app2/srv36"

# show messages arriving to this ring in real time ("tail -f" equivalent)
$ (echo "show events buf0 -w"; read) | socat /var/run/haproxy-master.sock -
```

<a id="entry-9-4-1-expert-mode"></a>

**`expert-mode [on|off]`**

```haproxy
expert-mode [on|off]
```

Este comando activa el "expert-mode" para cada worker al que se accede desde la CLI maestra.
Combinado con "mcli-debug-mode", también activa el comando en el master. Muestra el flag "e" en
el prompt de la CLI maestra.

Ver también "expert-mode" en la [Sección 9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) y "mcli-debug-mode" en 9.4.1.

<a id="entry-9-4-1-experimental-mode"></a>

**`experimental-mode [on|off]`**

```haproxy
experimental-mode [on|off]
```

Este comando activa el "experimental-mode" para cada worker al que se accede desde la CLI
maestra. Combinado con "mcli-debug-mode", también activa el comando en el master. Muestra el
flag "x" en el prompt de la CLI maestra.

Ver también "experimental-mode" en la [Sección 9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) y "mcli-debug-mode" en 9.4.1.

<a id="entry-9-4-1-hard-reload"></a>

**`hard-reload`**

```haproxy
hard-reload
```

Este comando hace lo mismo que el comando "reload" sobre la CLI maestra, con la excepción de que
hace una parada dura (-st) del proceso anterior en lugar de una parada suave (-sf). Esto
significa que el proceso anterior no espera a completar nada antes de salir, por lo que se
cerrarán todas las conexiones.

Ver también el comando "reload".

<a id="entry-9-4-1-mcli-debug-mode"></a>

**`mcli-debug-mode [on|off]`**

```haproxy
mcli-debug-mode [on|off]
```

Esta palabra clave permite un modo especial en la CLI maestra que activa todas las palabras
clave que estaban pensadas para una CLI de worker en la CLI maestra, lo que permite depurar el
proceso maestro. Una vez activado, lista las nuevas palabras clave disponibles con "help".
Combinado con "experimental-mode" o "expert-mode" activa aún más palabras clave. Muestra el flag
"d" en el prompt de la CLI maestra.

<a id="entry-9-4-1-prompt"></a>

**`prompt`**

```haproxy
prompt
```

Cuando el prompt está activado (vía el comando "prompt"), el contexto en el que trabaja la CLI
se muestra en el prompt. El master se identifica con la cadena "master" y los demás procesos se
identifican con su PID. En caso de que la última recarga fallara, el prompt del master cambiará
a "master[ReloadFailed]\>" para que resulte visible que el proceso sigue ejecutándose con la
configuración anterior y que la nueva configuración no está operativa.

El prompt de la CLI maestra puede mostrar varios flags, que son los modos activados. "d" para
mcli-debug-mode, "e" para expert-mode, "x" para experimental-mode.

Ejemplo:

```shell
$ socat /var/run/haproxy-master.sock -
prompt
master> expert-mode on
master(e)> experimental-mode on
master(xe)> mcli-debug-mode on
master(xed)> @1
95191(xed)>
```

<a id="entry-9-4-1-reload"></a>

**`reload`**

```haproxy
reload
```

También puedes recargar el proceso maestro de HAProxy con el comando "reload", que hace lo mismo
que un `kill -USR2` sobre el proceso maestro, siempre que el usuario tenga al menos privilegios
de "operator" o "admin".

Este comando permite realizar una recarga síncrona; el comando devolverá un estado de la recarga
una vez que esta se haya realizado. Ten cuidado con el timeout si se usa una herramienta para
analizarlo: solo se devuelve una vez que la configuración se ha analizado y el nuevo worker se
ha bifurcado (fork). El comando "socat" usa un timeout de 0.5s por defecto, así que terminará
antes de mostrar el mensaje si la recarga es demasiado larga. "ncat" no tiene timeout por
defecto. Cuando se compila con USE_SHM_OPEN=1, el comando reload también puede volcar los
startup-logs del master.

Ejemplo:

```shell
$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=1
--
[NOTICE]   (482713): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482713): path to executable is ./haproxy
[WARNING]  (482713): config: 'http-request' rules ignored for proxy 'frt1' as they require HTTP mode.
[NOTICE]   (482713): New worker (482720) forked
[NOTICE]   (482713): Loading success.

$ echo "reload" | socat -t300 /var/run/haproxy-master.sock stdin
Success=0
--
[NOTICE]   (482886): haproxy version is 2.7-dev7-4827fb-69
[NOTICE]   (482886): path to executable is ./haproxy
[ALERT]    (482886): config: parsing [test3.cfg:1]: unknown keyword 'Aglobal' out of section.
[ALERT]    (482886): config: Fatal errors found in configuration.
[WARNING]  (482886): Loading failure!

$
```

El comando reload es el último que se ejecuta en la CLI maestra; todos los demás comandos
después de él se ignoran. Una vez que el comando reload devuelve su estado, cerrará la conexión
con la CLI.

Ten en cuenta que una recarga cerrará todas las conexiones a la CLI maestra. Ver también el
comando "hard-reload".

<a id="entry-9-4-1-show-proc"></a>

**`show proc [debug]`**

```haproxy
show proc [debug]
```

La CLI maestra introduce un comando 'show proc' para supervisar los procesos.

Ejemplo:

```shell
$ echo 'show proc' | socat /var/run/haproxy-master.sock -
#<PID>          <type>          <reloads>       <uptime>        <version>
1162            master          5 [failed: 0]   0d00h02m07s     2.5-dev13
# workers
1271            worker          1               0d00h00m00s     2.5-dev13
# old workers
1233            worker          3               0d00h00m43s     2.0-dev3-6019f6-289
```

En este ejemplo, el master ha sido recargado 5 veces pero uno de los workers antiguos sigue
ejecutándose y sobrevivió a 3 recargas. Podrías acceder a la CLI de ese worker para entender qué
está pasando.

El parámetro 'debug' es útil para mostrar detalles de depuración; actualmente muestra los FDs
para la comunicación IPC. Ten en cuenta que no se garantiza que la salida de depuración sea
estable entre versiones de haproxy.

<a id="entry-9-4-1-show-startup-logs"></a>

**`show startup-logs`**

```haproxy
show startup-logs
```

HAProxy debe compilarse con USE_SHM_OPEN=1 para usarse correctamente en la CLI maestra, o no
todos los mensajes serán visibles.

Como su contrapartida en el socket de estadísticas, este comando puede mostrar los mensajes de
arranque de HAProxy. Sin embargo, no vuelca los mensajes de arranque del worker actual, sino los
mensajes de arranque del último arranque o recarga, lo que significa que es capaz de volcar los
mensajes de análisis de una recarga fallida.

Esos mensajes también se vuelcan con el comando "reload".

## 9.5. Archivo de estadísticas {#section-9-5}

Un llamado stats-file puede usarse para precargar contadores internos de haproxy en el arranque
del proceso con valores no nulos. Su propósito principal es preservar las estadísticas de los
procesos worker a través de las recargas. En un stats-file solo está presente un extracto de
todas las estadísticas de haproxy expuestas, ya que solo tiene sentido precargar valores de tipo
métrica.

Por el momento, solo los contadores de proxy son compatibles en el stats-file. Esto permite
precargar valores para frontends, backends, servidores y listeners. Sin embargo, solo las
instancias de objetos con un GUID no vacío se almacenan en un stats-file. Esto garantiza que el
valor se precargará para el objeto con tipo y GUID coincidentes, incluso si otros parámetros
difieren.

El propósito del comando CLI "dump stats-file" es generar un stats-file. El formato del
stats-file está definido internamente y sujeto libremente a cambios y extensiones futuras. Está
diseñado para ser compatible al menos entre versiones de ramas estables adyacentes de haproxy, pero puede
requerir configuración extra opcional al cargar un stats-file en un proceso que ejecute una
versión más antigua.
