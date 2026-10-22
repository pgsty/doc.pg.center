---
title: "4. Proxies"
linkTitle: "4. Proxies"
weight: 150
description: "Valores por defecto, frontends, backends, listeners, palabras clave de proxy y referencias de acciones"
icon: fa-solid fa-right-left
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/proxies/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 4"
---

La configuración del proxy puede ubicarse en un conjunto de secciones:

- defaults [`<name>`] [ from `<defaults_name>` ]
- frontend `<name>` [ from `<defaults_name>` ]
- backend `<name>` [ from `<defaults_name>` ]
- listen `<name>` [ from `<defaults_name>` ]

Una sección "frontend" describe un conjunto de sockets de escucha que aceptan conexiones de clientes.

Una sección "backend" describe un conjunto de servidores a los que el proxy se conectará para
reenviar las conexiones entrantes.

Una sección "listen" define un proxy completo con sus partes frontend y backend combinadas en una
sola sección. Generalmente es útil para tráfico exclusivamente TCP.

Una sección "defaults" restablece todos los parámetros a sus valores documentados y predefine otros
nuevos para su uso por las secciones posteriores. Todas las secciones "frontend", "backend" y
"listen" toman siempre sus parámetros iniciales de una sección defaults; por defecto, la última que
aparece antes de la sección recién creada. Es posible designar explícitamente una sección
"defaults" específica de la cual cargar los parámetros iniciales, indicando su nombre en la línea
de sección tras la palabra clave opcional "from". Aunque las secciones "defaults" no exigen un
nombre, se recomienda esta práctica para una mejor legibilidad. También es la única manera de
designar una sección específica que usar en lugar de la anterior por defecto. Dado que los nombres
de las secciones "defaults" son opcionales, por defecto se les aplica una comprobación muy
permisiva e incluso se permite que se solapen. Sin embargo, si una sección "defaults" es
referenciada por cualquier otra sección, su nombre debe cumplir la sintaxis impuesta a todos los
nombres de proxy, y este nombre debe ser único entre las secciones defaults. Ten en cuenta que,
independientemente de lo que se permita actualmente, se recomienda evitar en general los nombres de
sección duplicados y respetar la misma sintaxis que para los nombres de proxy. Esta regla podría
imponerse en una versión futura. Además, se emite un aviso si una sección defaults es usada
explícitamente por un proxy mientras también es usada implícitamente por otro por ser la última
definida. Se recomienda encarecidamente no mezclar ambos usos, empleando siempre referencias
explícitas o añadiendo una última sección defaults común reservada para todos los usos implícitos.

Ten en cuenta que incluso es posible que una sección defaults tome sus parámetros iniciales de
otra y, de este modo, herede parámetros a través de múltiples niveles de secciones defaults. Esto
puede resultar cómodo para establecer ciertos perfiles de configuración que agrupan conjuntos de
parámetros por defecto (p. ej. TCP frente a HTTP, o tiempos de espera cortos frente a largos),
pero puede volverse rápidamente confuso de seguir.

Por defecto, las secciones defaults con nombre se conservan tras el análisis de la configuración.
Esto permite reutilizarlas para la creación dinámica de backends. Este comportamiento puede
cambiarse globalmente mediante la palabra clave "tune.defaults.purge".

Todos los nombres de proxy deben estar formados por letras mayúsculas y minúsculas, dígitos, '-'
(guion), '\_' (guion bajo), '.' (punto) y ':' (dos puntos). Los nombres de ACL distinguen
mayúsculas de minúsculas, lo que significa que "www" y "WWW" son dos proxies diferentes.

Históricamente, todos los nombres de proxy podían solaparse cuando se cumplían ciertas condiciones
(p. ej. al no tener las mismas capacidades de frontend/backend), pero esto solía causar demasiados
problemas en los registros, así como confusión en las operaciones por CLI, en el nombre de las
stick-tables y en la obtención de estadísticas. Ahora es obligatorio que dos proxies tengan nombres
diferentes, independientemente de sus capacidades respectivas.

Actualmente se soportan dos modos principales de proxy: "tcp", también conocido como capa 4, y
"http", también conocido como capa 7. En modo capa 4, HAProxy simplemente reenvía el tráfico
bidireccional entre dos extremos. En modo capa 7, HAProxy analiza el protocolo y puede interactuar
con él permitiendo, bloqueando, conmutando, añadiendo, modificando o eliminando contenidos
arbitrarios en las solicitudes o respuestas, según criterios arbitrarios.

En modo HTTP, el procesamiento aplicado a las solicitudes y respuestas que fluyen por una conexión
depende de la combinación de las opciones HTTP del frontend y las del backend. HAProxy soporta 3
modos de conexión:

- KAL: keep alive ("option http-keep-alive"), que es el modo por defecto: todas las solicitudes y
  respuestas se procesan, y las conexiones permanecen abiertas pero inactivas entre las respuestas
  y las nuevas solicitudes.

- SCL: server close ("option http-server-close"): la conexión hacia el servidor se cierra tras
  recibir el final de la respuesta, pero la conexión hacia el cliente permanece abierta.

- CLO: close ("option httpclose"): la conexión se cierra tras el final de la respuesta y se añade
  "Connection: close" en ambas direcciones.

El modo efectivo que se aplicará a una conexión que pasa por un frontend y un backend puede
determinarse a partir de ambos modos de proxy según la siguiente matriz, pero en resumen, los
modos son simétricos, keep-alive es la opción más débil y close la más fuerte.

                   Modo del backend

```text
                | KAL | SCL | CLO
            ----+-----+-----+----
            KAL | KAL | SCL | CLO
            ----+-----+-----+----
   modo     SCL | SCL | SCL | CLO
            ----+-----+-----+----
            CLO | CLO | CLO | CLO
```

Es posible encadenar un frontend TCP a un backend HTTP. No tiene sentido si solo se maneja tráfico
HTTP. Pero puede usarse para manejar varios protocolos dentro del mismo frontend. En este caso, la
conexión del cliente se trata primero como una conexión tcp en bruto antes de cambiarla al protocolo HTTP.
Antes del cambio, los procesamientos de contenido se realizan sobre datos en bruto. Una vez
realizado el cambio, los datos se analizan y almacenan usando una representación interna llamada HTX y ya no
es posible basarse en la representación en bruto. No hay manera de volver atrás.

Existen dos clases de cambios de protocolo: los cambios in situ y los cambios destructivos. Los primeros
implican un cambio de TCP a HTTP/1. En HTTP/1, los procesamientos de las solicitudes están
serializados, por lo que el flujo aplicativo puede conservarse. Los segundos implican un cambio de
TCP a HTTP/2. Al tratarse de un protocolo multiplexado, el flujo aplicativo no puede asociarse a
ningún flujo HTTP/2 y se destruye. Después se crean nuevos flujos aplicativos cuando HAProxy
recibe nuevos flujos HTTP/2 en el nivel inferior, en el multiplexor H2. Es importante entender esta
diferencia porque cambia drásticamente la manera de procesar los datos. Cuando se realiza un
cambio a HTTP/1, los procesamientos de contenido ya realizados sobre los datos en bruto no se
pierden ni se reejecutan, mientras que en un cambio a HTTP/2 los flujos aplicativos son
distintos y todas las reglas del frontend se evalúan sistemáticamente sobre cada uno. Y como se ha
dicho, el primer flujo, el de TCP, se destruye, pero solo después de que se hayan evaluado las
reglas del frontend.

Hay otro punto importante que entender cuando se realizan procesamientos HTTP desde un proxy TCP.
Aunque HAProxy es capaz de analizar HTTP/1 al vuelo desde las reglas tcp-request content, no es
posible para HTTP/2. Solo puede analizarse el preámbulo de HTTP/2. Esta es una gran limitación en
lo que respecta al análisis de contenido HTTP en TCP. En la práctica, solo es posible saber si los
datos recibidos son HTTP. Por ejemplo, no es posible elegir un backend basándose en el valor de la
cabecera Host, algo que en HTTP/1 es trivial. Afortunadamente, existe una solución para mitigar
este inconveniente.

Hay dos maneras de realizar un cambio a HTTP. La primera, el método histórico, consiste en
seleccionar un backend HTTP. El cambio ocurre cuando se define el backend. Así, para los cambios de protocolo
in situ, en el procesamiento de datos HTTP solo se considera la configuración del backend. Para
los cambios de protocolo destructivos, el flujo aplicativo se destruye y su procesamiento se detiene. Con este
método, las posibilidades de elegir un backend con una conexión HTTP/2 son realmente limitadas,
como se mencionó arriba, y algo inútiles porque el flujo se destruye. El segundo método consiste en
realizar el cambio durante la evaluación de las reglas tcp-request content, gracias a la acción
"switch-mode http". En este caso, el cambio se realiza en el contexto del frontend y es posible
definir directivas HTTP en este frontend. Para los cambios de protocolo in situ, ofrece toda la potencia del
análisis HTTP lo antes posible. No dista mucho de un frontend HTTP. Para los cambios de protocolo destructivos,
no cambia nada, salvo que es inútil elegir un backend con información limitada. Es por supuesto el
método recomendado. Así pues, comprobar el protocolo de la solicitud desde las reglas
tcp-request content para realizar un cambio a HTTP es suficiente. Toda la manipulación HTTP
restante puede trasladarse al conjunto de reglas http-request del frontend. Pero ten en cuenta que
las reglas tcp-request content se siguen evaluando en cada flujo, y eso no puede cambiarse.

## 4.1. Matriz de palabras clave de proxy {#section-4-1}

Se soporta la siguiente lista de palabras clave. La mayoría de ellas solo puede usarse en un
conjunto limitado de tipos de sección. Algunas están marcadas como obsoletas ("deprecated") porque
se heredan de una sintaxis antigua que puede resultar confusa o funcionalmente limitada, y existen
nuevas palabras clave recomendadas para reemplazarlas. Las palabras clave marcadas con "(\*)"
pueden invertirse opcionalmente usando el prefijo "no", p. ej. "no option contstats". Esto tiene
sentido cuando la opción ha sido activada por defecto y debe desactivarse para una instancia
específica. Tales opciones también pueden llevar el prefijo "default" para restaurar los
parámetros por defecto independientemente de lo especificado en una sección "defaults" anterior.
Las palabras clave soportadas en secciones defaults marcadas con "(!)" solo se soportan en
secciones defaults con nombre, no en anónimas.

Nota: Algunas directivas peligrosas y no recomendadas no se listan intencionadamente en la
siguiente matriz. Es a propósito. Estas directivas están documentadas. Pero no listarlas a
continuación es una manera más de disuadir a cualquiera de usarlas.

```text
 palabra clave                        defaults   frontend   listen    backend
------------------------------------+----------+----------+---------+---------
acl                                       X (!)      X         X         X
backlog                                   X          X         X         -
balance                                   X          -         X         X
be-unpublished                            -          -         X         X
bind                                      -          X         X         -
capture cookie                            -          X         X         -
capture request header                    -          X         X         -
capture response header                   -          X         X         -
clitcpka-cnt                              X          X         X         -
clitcpka-idle                             X          X         X         -
clitcpka-intvl                            X          X         X         -
compression                               X          X         X         X
cookie                                    X          -         X         X
crt                                       -          X         X         -
declare capture                           -          X         X         -
default-server                            X          -         X         X
default_backend                           X          X         X         -
description                               -          X         X         X
disabled                                  X          X         X         X
dispatch                    (deprecated)  -          -         X         X
email-alert from                          X          X         X         X
email-alert level                         X          X         X         X
email-alert mailers                       X          X         X         X
email-alert myhostname                    X          X         X         X
email-alert to                            X          X         X         X
enabled                                   X          X         X         X
errorfile                                 X          X         X         X
errorfiles                                X          X         X         X
errorloc                                  X          X         X         X
errorloc302                               X          X         X         X
-- palabra clave--------------------- defaults - frontend - listen -- backend -
errorloc303                               X          X         X         X
error-log-format                          X          X         X         -
external-check command                    X          -         X         X
external-check path                       X          -         X         X
force-persist                             -          -         X         X
force-be-switch                           -          X         X         -
filter                                    -          X         X         X
fullconn                                  X          -         X         X
guid                                      -          X         X         X
hash-balance-factor                       X          -         X         X
hash-preserve-affinity                    X          -         X         X
hash-type                                 X          -         X         X
http-after-response                       X (!)      X         X         X
http-check comment                        X          -         X         X
http-check connect                        X          -         X         X
http-check disable-on-404                 X          -         X         X
http-check expect                         X          -         X         X
http-check send                           X          -         X         X
http-check send-state                     X          -         X         X
http-check set-var                        X          -         X         X
http-check unset-var                      X          -         X         X
http-error                                X          X         X         X
http-request                              X (!)      X         X         X
http-response                             X (!)      X         X         X
http-reuse                                X          -         X         X
http-send-name-header                     X          -         X         X
id                                        -          X         X         X
ignore-persist                            -          -         X         X
load-server-state-from-file               X          -         X         X
log                                  (*)  X          X         X         X
log-format                                X          X         X         -
log-format-sd                             X          X         X         -
log-tag                                   X          X         X         X
log-steps                                 X          X         X         -
max-keep-alive-queue                      X          -         X         X
max-session-srv-conns                     X          X         X         -
maxconn                                   X          X         X         -
mode                                      X          X         X         X
monitor fail                              -          X         X         -
monitor-uri                               X          X         X         -
option abortonclose                  (*)  X          X         X         X
option allbackups                    (*)  X          -         X         X
option checkcache                    (*)  X          -         X         X
option clitcpka                      (*)  X          X         X         -
option contstats                     (*)  X          X         X         -
option disable-h2-upgrade            (*)  X          X         X         -
option dontlog-normal                (*)  X          X         X         -
option dontlognull                   (*)  X          X         X         -
-- palabra clave--------------------- defaults - frontend - listen -- backend -
option external-check                     X          -         X         X
option forwardfor                         X          X         X         X
option forwarded                     (*)  X          -         X         X
option h1-case-adjust-bogus-client   (*)  X          X         X         -
option h1-case-adjust-bogus-server   (*)  X          -         X         X
option http-buffer-request           (*)  X          X         X         X
option http-drop-request-trailers    (*)  X          -         -         X
option http-drop-response-trailers   (*)  X          -         X         -
option http-ignore-probes            (*)  X          X         X         -
option http-keep-alive               (*)  X          X         X         X
option http-no-delay                 (*)  X          X         X         X
option http-pretend-keepalive        (*)  X          -         X         X
option http-restrict-req-hdr-names        X          X         X         X
option http-server-close             (*)  X          X         X         X
option http-use-proxy-header         (*)  X          X         X         -
option httpchk                            X          -         X         X
option httpclose                     (*)  X          X         X         X
option httplog                            X          X         X         -
option httpslog                           X          X         X         -
option idle-close-on-response        (*)  X          X         X         -
option independent-streams           (*)  X          X         X         X
option ldap-check                         X          -         X         X
option log-health-checks             (*)  X          -         X         X
option log-separate-errors           (*)  X          X         X         -
option logasap                       (*)  X          X         X         -
option mysql-check                        X          -         X         X
option nolinger                      (*)  X          X         X         X
option originalto                         X          X         X         X
option persist                       (*)  X          -         X         X
option pgsql-check                        X          -         X         X
option prefer-last-server            (*)  X          -         X         X
option redispatch                    (*)  X          -         X         X
option redis-check                        X          -         X         X
option smtpchk                            X          -         X         X
option socket-stats                  (*)  X          X         X         -
option splice-auto                   (*)  X          X         X         X
option splice-request                (*)  X          X         X         X
option splice-response               (*)  X          X         X         X
option spop-check                         X          -         X         X
option srvtcpka                      (*)  X          -         X         X
option ssl-hello-chk                      X          -         X         X
-- palabra clave--------------------- defaults - frontend - listen -- backend -
option tcp-check                          X          -         X         X
option tcp-smart-accept              (*)  X          X         X         -
option tcp-smart-connect             (*)  X          -         X         X
option tcpka                              X          X         X         X
option tcplog                             X          X         X         -
option transparent      (deprecated) (*)  X          -         X         X
option use-small-buffers             (*)  X          -         X         X
persist rdp-cookie                        X          -         X         X
quic-initial                              X (!)      X         X         -
rate-limit sessions                       X          X         X         -
redirect                                  -          X         X         X
-- palabra clave--------------------- defaults - frontend - listen -- backend -
retries                                   X          -         X         X
retry-on                                  X          -         X         X
server                                    -          -         X         X
server-state-file-name                    X          -         X         X
server-template                           -          -         X         X
source                                    X          -         X         X
srvtcpka-cnt                              X          -         X         X
srvtcpka-idle                             X          -         X         X
srvtcpka-intvl                            X          -         X         X
stats admin                               -          X         X         X
stats auth                                X          X         X         X
stats enable                              X          X         X         X
stats hide-version                        X          X         X         X
stats http-request                        -          X         X         X
stats realm                               X          X         X         X
stats refresh                             X          X         X         X
stats scope                               X          X         X         X
stats show-desc                           X          X         X         X
stats show-legends                        X          X         X         X
stats show-node                           X          X         X         X
stats show-version                        X          X         X         X
stats uri                                 X          X         X         X
-- palabra clave--------------------- defaults - frontend - listen -- backend -
stick match                               -          -         X         X
stick on                                  -          -         X         X
stick store-request                       -          -         X         X
stick store-response                      -          -         X         X
stick-table                               -          X         X         X
tcp-check comment                         X          -         X         X
tcp-check connect                         X          -         X         X
tcp-check expect                          X          -         X         X
tcp-check send                            X          -         X         X
tcp-check send-lf                         X          -         X         X
tcp-check send-binary                     X          -         X         X
tcp-check send-binary-lf                  X          -         X         X
tcp-check set-var                         X          -         X         X
tcp-check unset-var                       X          -         X         X
tcp-request connection                    X (!)      X         X         -
tcp-request content                       X (!)      X         X         X
tcp-request inspect-delay                 X (!)      X         X         X
tcp-request session                       X (!)      X         X         -
tcp-response content                      X (!)      -         X         X
tcp-response inspect-delay                X (!)      -         X         X
timeout check                             X          -         X         X
timeout client                            X          X         X         -
timeout client-fin                        X          X         X         -
timeout client-hs                         X          X         X         -
timeout connect                           X          -         X         X
timeout http-keep-alive                   X          X         X         X
timeout http-request                      X          X         X         X
timeout queue                             X          -         X         X
timeout server                            X          -         X         X
timeout server-fin                        X          -         X         X
timeout tarpit                            X          X         X         X
timeout tunnel                            X          -         X         X
transparent                 (deprecated)  X          -         X         X
unique-id-format                          X          X         X         X
unique-id-header                          X          X         X         -
use_backend                               -          X         X         -
use-fcgi-app                              -          -         X         X
use-server                                -          -         X         X
------------------------------------+----------+----------+---------+---------
 palabra clave                        defaults   frontend   listen    backend
```

## 4.2. Referencia de palabras clave ordenadas alfabéticamente {#section-4-2}

Esta sección proporciona una descripción de cada palabra clave y su uso.

<a id="entry-4-2-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

Declara o completa una lista de acceso.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

Esta directiva solo está disponible en secciones defaults con nombre, no en anónimas. Las ACL
definidas en una sección defaults no son visibles desde otras secciones que la usen.

Ejemplo:

```text
acl invalid_src  src          0.0.0.0/7 224.0.0.0/3
acl invalid_src  src_port     0:1023
acl local_dst    hdr(host) -i localhost
```

Consulta la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de las ACL.

<a id="entry-4-2-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

Proporciona al sistema pistas sobre el tamaño aproximado deseado de la cola backlog de escucha

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<conns>   es el número de conexiones pendientes. Según el sistema operativo,
          puede representar el número de conexiones ya reconocidas, no
          reconocidas, o ambas.
```

Esta opción solo tiene sentido para listeners de flujo, incluidos los QUIC. Su comportamiento sin
embargo no es idéntico con instancias QUIC.

Para todos los listeners excepto QUIC, con el fin de protegerse de los ataques de SYN flood, una
solución consiste en aumentar el tamaño de la cola SYN del sistema. Según el sistema, a veces
simplemente es ajustable mediante un parámetro del sistema, a veces no es ajustable en absoluto, y
a veces el sistema se basa en las pistas dadas por la aplicación en el momento de la llamada al
sistema listen(). Por defecto, HAProxy pasa el valor maxconn del frontend a la llamada al sistema
listen(). En sistemas que pueden aprovechar este valor, a veces puede ser útil poder especificar
un valor diferente, de ahí este parámetro backlog.

En Linux 2.4, el sistema ignora el parámetro. En Linux 2.6, se usa como pista y el sistema acepta
hasta la menor potencia de dos superior, y nunca más allá de ciertos límites (normalmente 32768).

Para los listeners QUIC, backlog establece un límite compartido tanto para el número máximo de
negociaciones activas como de conexiones en espera de ser aceptadas. La fase de negociación depende
principalmente de la latencia de red con el par remoto, mientras que la segunda fase depende
únicamente de la carga de haproxy. Cuando se alcanza cualquiera de estos límites, haproxy comienza
a descartar la recepción de paquetes INITIAL, impidiendo cualquier nueva asignación de conexión,
hasta que el exceso de conexiones comienza a disminuir. Esta situación puede provocar que los
navegadores degraden silenciosamente las versiones de HTTP y cambien a TCP.

Ver también: "maxconn" y la guía de ajuste del sistema operativo de destino.

<a id="entry-4-2-balance"></a>

**`balance <algorithm> [ <arguments> ]`**

```haproxy
balance <algorithm> [ <arguments> ]
balance url_param <param> [check_post]
```

Define el algoritmo de balanceo de carga que se usará en un backend.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<algorithm> es el algoritmo usado para seleccionar un servidor al realizar el
            balanceo de carga. Solo se aplica cuando no hay disponible
            información de persistencia, o cuando una conexión se redistribuye
            a otro servidor. <algorithm> puede ser uno de los siguientes:

  roundrobin  Cada servidor se usa por turnos, según sus pesos. Es el
              algoritmo más suave y equitativo cuando el tiempo de
              procesamiento de los servidores permanece uniformemente
              repartido. Es un algoritmo dinámico, lo que significa que los
              pesos de los servidores pueden ajustarse al vuelo, por ejemplo
              para un arranque lento (slow start). Está limitado por diseño a
              4095 servidores activos por backend. Ten en cuenta que, en
              algunas granjas grandes, cuando un servidor pasa a estar activo
              tras haber estado inactivo un tiempo muy corto, a veces pueden
              hacer falta unos cientos de solicitudes para que se
              reincorpore a la granja y empiece a recibir tráfico. Esto es
              normal, aunque muy raro. Se indica aquí por si tuvieras la
              suerte de observarlo, para que no te preocupes. Nota: los pesos
              se ignoran en los backends en modo LOG.

  static-rr   Cada servidor se usa por turnos, según sus pesos. Este
              algoritmo es similar a roundrobin, salvo en que es estático,
              lo que significa que cambiar el peso de un servidor al vuelo
              no tiene ningún efecto. A cambio, no tiene limitación de
              diseño en el número de servidores, y cuando un servidor pasa
              a estar activo siempre se reintroduce de inmediato en la
              granja, una vez recalculado el mapa completo. También consume
              algo menos de CPU (alrededor de -1%). Este algoritmo no puede
              usarse en modo LOG.

  leastconn   El servidor con el menor número de conexiones recibe la
              conexión. Se aplica round-robin dentro de los grupos de
              servidores con la misma carga para asegurar que se usen
              todos. Se recomienda usar este algoritmo donde se esperen
              sesiones muy largas, como LDAP, SQL, TSE, etc..., pero no es
              muy adecuado para protocolos con sesiones cortas como HTTP.
              Es un algoritmo dinámico, lo que significa que los pesos de
              los servidores pueden ajustarse al vuelo, por ejemplo para un
              arranque lento (slow start). También tendrá en cuenta el
              número de conexiones en cola, además de las establecidas,
              para minimizar las esperas. Este algoritmo no puede usarse en
              modo LOG.

  first       El primer servidor con huecos de conexión disponibles recibe la
              conexión. Los servidores se eligen del identificador numérico
              menor al mayor (ver el parámetro de servidor "id"), que por
              defecto corresponde a la posición del servidor en la granja.
              Cuando un servidor alcanza su valor maxconn, se usa el
              siguiente servidor. No tiene sentido usar este algoritmo sin
              establecer maxconn. El propósito de este algoritmo es usar
              siempre el menor número de servidores, de modo que los
              servidores sobrantes puedan apagarse en horas de poca carga.
              Este algoritmo ignora el peso del servidor y beneficia más a
              las sesiones largas, como RDP o IMAP, que a HTTP, aunque
              también puede ser útil ahí. Para usar este algoritmo con
              eficiencia, se recomienda que un controlador cloud compruebe
              regularmente el uso de los servidores para apagarlos cuando
              no se usen, y que compruebe regularmente la cola del backend
              para encender nuevos servidores cuando la cola crezca.
              Alternativamente, usar "http-check send-state" puede informar
              a los servidores de la carga. Este algoritmo no puede usarse
              en modo LOG.

  hash        Toma como argumento una expresión de muestra regular. La
              expresión se evalúa para cada solicitud y se procesa con hash
              según el "hash-type" configurado. El resultado del hash se
              divide entre el peso total de los servidores activos para
              designar qué servidor recibirá la solicitud. Puede usarse en
              lugar de "source", "uri", "hdr()", "url_param()",
              "rdp-cookie" para emplear un convertidor, refinar la
              evaluación o, por ejemplo, extraer datos de variables locales.
              Cuando los datos no están disponibles, se aplica round robin.
              Este algoritmo es estático por defecto, lo que significa que
              cambiar el peso de un servidor al vuelo no tiene ningún
              efecto, pero puede cambiarse con "hash-type". Este algoritmo
              no puede usarse en backends en modo LOG; usa "log-hash" en su
              lugar.

  source      La dirección IP de origen se procesa con hash y se divide entre
              el peso total de los servidores activos para designar qué
              servidor recibirá la solicitud. Esto garantiza que la misma
              dirección IP de cliente llegue siempre al mismo servidor
              mientras ningún servidor suba o baje. Si el resultado del hash
              cambia porque cambia el número de servidores activos, muchos
              clientes se dirigirán a un servidor diferente. Este algoritmo
              se usa generalmente en modo TCP, donde no puede insertarse
              ninguna cookie. También puede usarse en Internet para ofrecer
              una afinidad best-effort a los clientes que rechazan las
              cookies de sesión. Este algoritmo es estático por defecto, lo
              que significa que cambiar el peso de un servidor al vuelo no
              tiene ningún efecto, pero puede cambiarse con "hash-type".
              Ver también la opción "hash" anterior. Este algoritmo no
              puede usarse en backends en modo LOG.

  uri         Este algoritmo calcula el hash de la parte izquierda del URI
              (antes del signo de interrogación) o del URI completo (si el
              parámetro "whole" está presente) y divide el valor del hash
              entre el peso total de los servidores activos. El resultado
              designa qué servidor recibirá la solicitud. Esto garantiza
              que el mismo URI se dirija siempre al mismo servidor mientras
              ningún servidor suba o baje. Se usa con cachés de proxy y
              proxies antivirus para maximizar la tasa de aciertos de
              caché. Ten en cuenta que este algoritmo solo puede usarse en
              un backend HTTP. Este algoritmo es estático por defecto, lo
              que significa que cambiar el peso de un servidor al vuelo no
              tiene ningún efecto, pero puede cambiarse con "hash-type".

              Este algoritmo admite dos parámetros opcionales, "len" y
              "depth", ambos seguidos de un número entero positivo. Estas
              opciones pueden ser útiles cuando es necesario balancear los
              servidores basándose solo en el comienzo del URI. El
              parámetro "len" indica que el algoritmo solo debe considerar
              ese número de caracteres del comienzo del URI para calcular
              el hash. Ten en cuenta que fijar "len" a 1 rara vez tiene
              sentido, ya que la mayoría de los URI comienzan con una "/".

              El parámetro "depth" indica la profundidad máxima de
              directorios que se usará para calcular el hash. Se cuenta un
              nivel por cada barra en la solicitud. Si se especifican ambos
              parámetros, la evaluación se detiene al alcanzar cualquiera
              de los dos.

              El parámetro "path-only" indica que la clave del hash comienza
              en la primera '/' de la ruta. Puede usarse para ignorar la
              parte de autoridad de los URI absolutos y para asegurar que
              los URI de HTTP/1 y HTTP/2 produzcan el mismo hash. Ver
              también la opción "hash" anterior.

  url_param   El parámetro de URL especificado en el argumento se buscará en
              la cadena de consulta de cada solicitud HTTP GET.

              Si se usa el modificador "check_post", se buscará el
              parámetro en la entidad de una solicitud HTTP POST cuando no
              se encuentre en una cadena de consulta tras un signo de
              interrogación ('?') en la URL. El cuerpo del mensaje solo
              comenzará a analizarse cuando se haya recibido la cantidad de
              datos anunciada o cuando el búfer de solicitud esté lleno. En
              el improbable caso de que se use codificación por bloques
              (chunked), solo se examina el primer bloque. Los valores de
              parámetros separados por un límite de bloque pueden
              balancearse aleatoriamente, o no balancearse en absoluto.
              Esta palabra clave admitía un parámetro opcional <max_wait>
              que ahora se ignora.

              Si se encuentra el parámetro seguido de un signo igual ('=') y
              un valor, el valor se procesa con hash y se divide entre el
              peso total de los servidores activos. El resultado designa qué
              servidor recibirá la solicitud.

              Se usa para rastrear identificadores de usuario en las
              solicitudes y garantizar que un mismo ID de usuario se envíe
              siempre al mismo servidor mientras ningún servidor suba o
              baje. Si no se encuentra ningún valor o si no se encuentra el
              parámetro, se aplica un algoritmo round robin. Ten en cuenta
              que este algoritmo solo puede usarse en un backend HTTP.
              Este algoritmo es estático por defecto, lo que significa que
              cambiar el peso de un servidor al vuelo no tiene ningún
              efecto, pero puede cambiarse con "hash-type". Ver también la
              opción "hash" anterior.

  hdr(<name>) La cabecera HTTP <name> se buscará en cada solicitud HTTP. Al
              igual que con la función ACL equivalente 'hdr()', el nombre
              de la cabecera entre paréntesis no distingue mayúsculas de
              minúsculas. Si la cabecera está ausente o no contiene ningún
              valor, se aplica en su lugar el algoritmo roundrobin.

              Existe un parámetro opcional 'use_domain_only' para reducir
              el algoritmo de hash a la parte del dominio principal con
              ciertas cabeceras específicas como 'Host'. Por ejemplo, en el
              valor de Host "haproxy.1wt.eu", solo se considerará "1wt".

              Este algoritmo es estático por defecto, lo que significa que
              cambiar el peso de un servidor al vuelo no tiene ningún
              efecto, pero puede cambiarse con "hash-type". Ver también la
              opción "hash" anterior.

  random
  random(<draws>)
              Se usará un número aleatorio como clave para la función de
              hash consistente. Esto significa que se respetan los pesos
              de los servidores, y que los cambios dinámicos de peso y las
              altas de nuevos servidores surten efecto de inmediato. El
              balanceo aleatorio puede ser útil con granjas grandes o
              cuando los servidores se añaden o eliminan con frecuencia,
              ya que puede evitar el efecto martilleo que roundrobin o
              leastconn podrían provocar en esta situación. La directiva
              hash-balance-factor puede usarse para mejorar aún más la
              equidad del balanceo de carga, especialmente en situaciones
              donde los servidores muestran tiempos de respuesta muy
              variables. Cuando hay un argumento <draws>, debe ser un
              valor entero igual o mayor que uno, que indica el número de
              extracciones antes de seleccionar el menos cargado de esos
              servidores. En efecto, se demostró que elegir el menos
              cargado de dos servidores basta para mejorar
              significativamente la equidad del algoritmo, al evitar
              siempre escoger el servidor más cargado de una granja y
              eliminar cualquier sesgo que pudiera inducir la distribución
              desigual de la lista consistente. Valores N más altos
              descartarán a los N-1 servidores más cargados a costa de
              rendimiento. Con valores muy altos, el algoritmo convergerá
              hacia el resultado de leastconn, pero mucho más despacio.
              Además, con granjas grandes de carga muy baja (o equilibrio
              perfecto), comparar cargas suele terminar en empate, de modo
              que si todos los servidores medidos tienen la misma carga se
              comparan sus tasas de solicitudes del último segundo, lo que
              permite repartir mejor el uso de los servidores a lo largo
              del tiempo con el mismo espíritu que roundrobin y suavizar
              la falta de equidad del hash consistente. El valor por
              defecto es 2, que en general muestra una distribución y un
              rendimiento muy buenos. Para granjas grandes con poca carga
              (menos de unas pocas solicitudes por segundo y por
              servidor), puede ayudar subirlo a 3 o incluso 4. Este
              algoritmo también se conoce como Power of Two Random Choices
              y se describe aquí:
              http://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf

              En los backends en modo LOG, el número de extracciones se
              ignora y se toma un único aleatorio, ya que no existe la
              noción de carga del servidor. El balanceo aleatorio de
              registros puede ser útil con granjas grandes o cuando los
              servidores se añaden o eliminan con frecuencia del conjunto
              de servidores disponibles, ya que puede evitar el efecto
              martilleo que roundrobin podría provocar en esta situación.

  rdp-cookie
  rdp-cookie(<name>)
              La cookie RDP <name> (o "mstshash" si se omite) se buscará y
              se procesará con hash para cada solicitud TCP entrante. Al
              igual que con la función ACL equivalente 'req.rdp_cookie()',
              el nombre no distingue mayúsculas de minúsculas. Este
              mecanismo es útil como modo de persistencia degradado, ya
              que permite enviar siempre al mismo usuario (o el mismo ID
              de sesión) al mismo servidor. Si no se encuentra la cookie,
              se usa el algoritmo roundrobin normal.

              Ten en cuenta que, para que esto funcione, el frontend debe
              garantizar que ya haya una cookie RDP en el búfer de
              solicitud. Para ello debes usar una regla 'tcp-request
              content accept' combinada con una ACL 'req.rdp_cookie_cnt'.

              Este algoritmo es estático por defecto, lo que significa que
              cambiar el peso de un servidor al vuelo no tiene ningún
              efecto, pero puede cambiarse con "hash-type". Ver también la
              opción "hash" anterior.

  log-hash    Toma como argumento una lista de convertidores separados por
              comas. Estos convertidores se aplican en secuencia al
              mensaje de registro de entrada, y el resultado se convertirá
              a cadena y luego se procesará con hash según el "hash-type"
              configurado. El hash resultante se usará para seleccionar el
              servidor de destino entre los declarados en el backend de
              registro. El objetivo de este algoritmo es poder extraer una
              clave del mensaje de registro final usando convertidores de
              cadenas y luego poder mantenerse en el mismo servidor gracias
              al hash. Por ahora solo se soportan los hashes "map-based".
              Este algoritmo solo puede usarse en backends en modo LOG;
              para los demás, usa "hash" en su lugar.

  sticky      Intenta mantenerse en el mismo servidor tanto como sea posible.
              El primer servidor de la lista de servidores disponibles
              recibe todos los mensajes de registro. Cuando ese servidor
              pasa a DOWN, el siguiente servidor de la lista ocupa su
              lugar. Cuando un servidor que estaba DOWN vuelve a UP se
              añade al final de la lista, de modo que el servidor sticky
              no cambia hasta pasar a DOWN.

<arguments> es una lista opcional de argumentos que pueden necesitar algunos
            algoritmos. Actualmente, solo "url_param", "uri" y "log-hash"
            admiten un argumento opcional.
```

El algoritmo de balanceo de carga de un backend se establece a "random" cuando no se ha definido
ningún otro algoritmo, modo ni opción. El algoritmo solo puede establecerse una vez por backend.

Con esquemas de autenticación que requieren la misma conexión, como NTLM, no deben usarse
algoritmos basados en el URI, ya que provocarían que las solicitudes posteriores se enruten a
diferentes servidores del backend, rompiendo los supuestos no válidos en los que se basa NTLM.

Ejemplos TCP/HTTP:

```text
balance roundrobin
balance url_param userid
balance url_param session_id check_post 64
balance hdr(User-Agent)
balance hdr(host)
balance hdr(Host) use_domain_only
balance hash req.cookie(clientid)
balance hash var(req.client_id)
balance hash req.hdr_ip(x-forwarded-for,-1),ipmask(24)
```

Ejemplos de backend LOG:

```text
global
  log backend@mylog-rrb local0 # send all logs to mylog-rrb backend
  log backend@mylog-hash local0 # send all logs to mylog-hash backend

backend mylog-rrb
  mode log
  balance roundrobin

  server s1 udp@127.0.0.1:514 # will receive 50% of log messages
  server s2 udp@127.0.0.1:514

backend mylog-hash
  mode log

  # extract "METHOD URL PROTO" at the end of the log message,
  # and let haproxy hash it so that log messages generated from
  # similar requests get sent to the same syslog server:
  balance log-hash 'field(-2,\")'

  # server list here
  server s1 127.0.0.1:514
  #...
```

Nota: deben tenerse en cuenta las siguientes advertencias y limitaciones sobre el uso de la
extensión "check_post" con "url_param":

    - todas las solicitudes POST son susceptibles de ser consideradas, porque
      no hay forma de determinar si los parámetros estarán en el cuerpo o en
      la entidad, que puede contener datos binarios. Por tanto, puede
      requerirse otro método para restringir la consideración de las
      solicitudes POST que no tengan parámetros URL en el cuerpo. (ver acl
      http_end)

    - usar un valor `<max_wait>` mayor que el tamaño del búfer de solicitud
      no tiene sentido y es inútil. El tamaño del búfer se fija en tiempo de
      compilación y por defecto es de 16 kB.

    - Content-Encoding no está soportado; la búsqueda del parámetro
      probablemente fallará y el balanceo de carga volverá a Round Robin.

    - Expect: 100-continue no está soportado; el balanceo de carga volverá a
      Round Robin.

    - Transfer-Encoding (RFC7230 3.3.1) solo está soportado en el primer
      bloque. Si el valor completo del parámetro no está presente en el
      primer bloque, la selección del servidor queda indefinida (en
      realidad, la define cuán poco apareció realmente en el primer bloque).

    - Esta característica no soporta la generación de una respuesta 100, 411
      o 501.

    - En algunos casos, solicitar "check_post" PUEDE intentar examinar todo
      el contenido de un cuerpo de mensaje. El análisis termina
      normalmente al encontrar espacios en blanco lineales o caracteres de
      control, lo que indica el final de lo que podría ser una lista de
      parámetros URL. Esto probablemente no suponga un problema con los
      cuerpos de mensaje de tipo SGML.

Ver también: "dispatch", "cookie", "transparent", "hash-type".

<a id="entry-4-2-be-unpublished"></a>

**`be-unpublished`**

```haproxy
be-unpublished
```

Indica al backend que arranque en estado no publicado.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

En la práctica, cualquier regla use_backend y default_backend de otro proxy que referencie al proxy
actual se ignora y se evalúan las siguientes reglas de conmutación de contenido. Esto puede
omitirse no obstante mediante una regla "force-be-switch".

Este estado es similar al de desactivado, pero con algunas diferencias. Primero, un backend no
publicado se inicializará completamente, incluidas las comprobaciones de estado de los servidores,
que permanecen activas. Finalmente, un backend puede exponerse públicamente mediante el comando
"publish backend" en la CLI. Consulta el manual de gestión.

Ver también: "force-be-switch"

<a id="entry-4-2-bind"></a>

**`bind [<address>]:<port_range> [, ...] [param*]`**

```haproxy
bind [<address>]:<port_range> [, ...] [param*]
bind /<path> [, ...] [param*]
```

Define una o varias direcciones y/o puertos de escucha en un frontend.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<address>     es opcional y puede ser un nombre de host, una dirección IPv4,
              una dirección IPv6 o '*'. Designa la dirección en la que
              escuchará el frontend. Si no se establece, se escuchará en
              todas las direcciones IPv4 del sistema. Lo mismo se aplica
              con '*' o la dirección especial del sistema "0.0.0.0". El
              equivalente IPv6 es '::'. Ten en cuenta que, para UDP, se
              requieren características específicas del sistema operativo
              al enlazar en varias direcciones para garantizar que se use
              la interfaz de red y la dirección de origen correctas en la
              respuesta. Dicho de otro modo, en los listeners QUIC solo se
              debe enlazar en varias direcciones si se ejecuta con sistemas
              suficientemente modernos.

              Opcionalmente, puede usarse un prefijo de familia de
              direcciones antes de la dirección para forzar la familia sin
              importar el formato de la dirección, lo que puede ser útil
              para especificar la ruta de un socket unix sin barra ('/').
              Los prefijos soportados actualmente son:
                - 'ipv4@'  -> la dirección es siempre IPv4
                - 'ipv6@'  -> la dirección es siempre IPv6
                - 'udp@'   -> la dirección se resuelve como IPv4 o IPv6 y se
                  usa el protocolo UDP. Actualmente esos listeners solo se
                  soportan en secciones log-forward.
                - 'udp4@'  -> la dirección es siempre IPv4 y se usa el
                  protocolo UDP. Actualmente esos listeners solo se
                  soportan en secciones log-forward.
                - 'udp6@'  -> la dirección es siempre IPv6 y se usa el
                  protocolo UDP. Actualmente esos listeners solo se
                  soportan en secciones log-forward.
                - 'unix@'  -> la dirección es una ruta a un socket unix local
                - 'abns@'  -> la dirección está en el espacio de nombres
                  abstracto (solo Linux).
                - 'abnsz@'  -> la dirección está en el espacio de nombres
                   abstracto (solo Linux), pero terminada explícitamente en
                   cero. Esto significa que no se usa relleno \0 para
                   completar sun_path. Es útil para interconectar con
                   programas que no implementan la lógica de nombres abns
                   por defecto que usa haproxy.
                - 'fd@<n>' -> usa el descriptor de archivo <n> heredado del
                  proceso padre. El fd debe estar enlazado y puede o no
                  estar ya escuchando.
                - 'sockpair@<n>'-> como fd@, pero se debe usar el fd de un
                  socket unix conectado o de un socketpair. El bind espera
                  recibir un FD por el socket unix y lo usa como si fuera
                  el FD de un accept(). Debe usarse con cuidado.
                - 'quic4@' -> la dirección se resuelve como IPv4 y se usa el
                  protocolo UDP. Ten en cuenta que para lograr el mejor
                  rendimiento con mucho tráfico se debería mantener
                  "tune.quic.fe.sock-per-conn
                  default-on". De lo contrario, las conexiones QUIC se
                  multiplexarán sobre el socket del listener. Otra
                  alternativa sería duplicar las instancias del listener
                  QUIC en varios hilos, por ejemplo usando la palabra clave
                  "shards", para al menos reducir la contención de hilos.
                - 'quic6@' -> la dirección se resuelve como IPv6 y se usa el
                  protocolo UDP. La nota de rendimiento de QUIC sobre IPv4
                  se aplica igualmente.
                - 'rhttp@' [ EXPERIMENTAL ] -> usado para HTTP inverso.
                  La dirección debe ser un servidor con el formato
                  '<backend>/<server>'. El servidor se usará para
                  instanciar conexiones a una dirección remota. El listener
                  intentará mantener "nbconn" conexiones. Esta es una
                  característica experimental que requiere
                  "expose-experimental-directives" en una línea anterior a
                  este bind.

              Puede que quieras hacer referencia a algunas variables de
              entorno en el parámetro de dirección; ver la sección 2.3 sobre
              variables de entorno.

<port_range>  es un puerto TCP único o un rango de puertos en los que el
              proxy aceptará conexiones para la dirección IP especificada
              arriba. El puerto es obligatorio para los listeners TCP. Ten
              en cuenta que, en el caso de una dirección IPv6, el puerto es
              siempre el número que va tras el último signo de dos puntos
              (':'). Un rango puede ser:
               - un puerto numérico (p. ej. '80')
               - un rango de puertos delimitado por guiones que indica
                 explícitamente los límites inferior y superior (p. ej.
                 '2000-2100'), ambos incluidos en el rango.

              Se debe tener un cuidado particular con los rangos de puertos,
              porque cada pareja <address:port> consume un socket (= un
              descriptor de archivo), así que es fácil consumir muchos
              descriptores con un simple rango y quedarse sin sockets.
              Además, cada pareja <address:port> debe usarse una sola vez
              entre todas las instancias que se ejecutan en un mismo
              sistema. Ten en cuenta que enlazar a puertos inferiores a
              1024 generalmente requiere privilegios especiales para
              iniciar el programa, independientes del parámetro 'uid'.

<path>        es una ruta de socket UNIX que comienza con una barra ('/').
              Es la alternativa al puerto de escucha TCP. HAProxy recibirá
              entonces conexiones UNIX en el socket ubicado en ese lugar.
              La ruta debe comenzar con una barra y por defecto es absoluta.
              Puede ser relativa al prefijo definido por "unix-bind" en la
              sección global. Ten en cuenta que la longitud total del
              prefijo seguido de la ruta del socket no puede exceder
              ciertos límites del sistema para los sockets UNIX, que
              habitualmente están fijados en 107 caracteres.

<param*>      es una lista de parámetros comunes a todos los sockets
              declarados en la misma línea. Estos numerosos parámetros
              dependen del sistema operativo y de las opciones de
              compilación y tienen una sección completa dedicada a ellos.
              Ver la sección 5 para más detalles.
```

Es posible especificar una lista de combinaciones dirección:puerto delimitadas por comas. El
frontend escuchará entonces en todas estas direcciones. No hay un límite fijo al número de
direcciones y puertos en los que puede escucharse en un frontend, así como tampoco hay límite al
número de instrucciones "bind" en un frontend.

Ejemplo:

```text
listen http_proxy
    bind :80,:443
    bind 10.0.0.1:10080,10.0.0.1:10443
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy

listen http_https_proxy
    bind :80
    bind :443 ssl crt /etc/haproxy/site.pem

listen http_https_proxy_explicit
    bind ipv6@:80
    bind ipv4@public_ssl:443 ssl crt /etc/haproxy/site.pem
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy

listen external_bind_app1
    bind "fd@${FD_APP1}"

listen h3_quic_proxy
    bind quic4@10.0.0.1:8888 ssl crt /etc/mycrt
```

Nota: en lo que respecta a los sockets de espacio de nombres abstracto de Linux, los sockets
"abns" de HAProxy usan la longitud completa de sun_path como longitud de la dirección. Algunos
otros programas, como socat, usan por defecto solo la longitud de la cadena. Pasa la opción
",unix-tightsocklen=0" a cualquier definición de socket abstracto en socat para hacerla compatible
con la de HAProxy, o usa en su lugar la familia de sockets "abnsz" de HAProxy.

Ver también: "source", "option forwardfor", "unix-bind" y la documentación del protocolo PROXY,
así como la [sección 5](/es/haproxy/bind-and-server-options/) sobre las opciones de bind.

<a id="entry-4-2-capture-cookie"></a>

**`capture cookie <name> len <length>`**

```haproxy
capture cookie <name> len <length>
```

Captura y registra una cookie en la solicitud y en la respuesta.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<name>    es el comienzo del nombre de la cookie que se va a capturar. Para
          que coincida el nombre exacto, basta con añadir un signo igual
          ('=') como sufijo al nombre. El nombre completo aparecerá en los
          registros, lo cual es útil con servidores de aplicación que
          ajustan tanto el nombre como el valor de la cookie (p. ej.
          ASPSESSIONXXX).

<length>  es el número máximo de caracteres que se informan en los
          registros, lo que incluye el nombre de la cookie, el signo igual
          y el valor, todo en la forma estándar "name=value". La cadena se
          truncará por la derecha si excede <length>.
```

Solo se captura la primera cookie. Se vigilan tanto las cabeceras de solicitud "cookie" como las
cabeceras de respuesta "set-cookie". Esto es particularmente útil para comprobar fallos de la
aplicación que causen cruce o robo de sesiones entre usuarios, porque generalmente las cookies del
usuario solo pueden cambiar en una página de inicio de sesión.

Cuando el cliente no presentó la cookie, la columna de registro asociada mostrará "-". Cuando una
solicitud no provoca que el servidor asigne una cookie, se informa "-" en la columna de respuesta.

La captura se realiza únicamente en el frontend porque es necesario que el formato de registro no
cambie para un frontend dado en función de los backends. Esto podría cambiar en el futuro. Ten en
cuenta que solo puede haber una instrucción "capture cookie" en un frontend. La longitud máxima de
captura la define el parámetro global "tune.http.cookielen" y es por defecto de 63 caracteres. No
es posible especificar una captura en una sección "defaults".

Ejemplo:

```text
capture cookie ASPSESSION len 32
```

Ver también: "capture request header", "capture response header", así como la [sección 8](/es/haproxy/configuration-logging/) sobre el registro.

<a id="entry-4-2-capture-request-header"></a>

**`capture request header <name> len <length>`**

```haproxy
capture request header <name> len <length>
```

Captura y registra la última aparición de la cabecera de solicitud especificada.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<name>    es el nombre de la cabecera que se va a capturar. Los nombres de
          las cabeceras no distinguen mayúsculas de minúsculas, pero es
          práctica común escribirlos tal como aparecen en las solicitudes,
          con la primera letra de cada palabra en mayúscula. El nombre de
          la cabecera no aparecerá en los registros: solo se informa del
          valor, pero se respeta la posición en los registros.

<length>  es el número máximo de caracteres que se extraen del valor y se
          informan en los registros. La cadena se truncará por la derecha
          si excede <length>.
```

Se captura el valor completo de la última aparición de la cabecera. El valor se añadirá a los
registros entre llaves ('{}'). Si se capturan varias cabeceras, se delimitarán por una barra
vertical ('\|') y aparecerán en el mismo orden en que se declararon en la configuración. Las
cabeceras inexistentes se registrarán como una cadena vacía. Usos comunes de las capturas de
cabeceras de solicitud incluyen el campo "Host" en entornos de hosting virtual, "Content-length"
cuando se soportan subidas, "User-agent" para diferenciar rápidamente entre usuarios reales y
robots, y "X-Forwarded-For" en entornos con proxy para averiguar de dónde provenía la solicitud.

Ten en cuenta que al capturar cabeceras como "User-agent", pueden registrarse algunos espacios,
lo que dificulta el análisis del registro. Así que cuidado con lo que registras si sabes que tu
analizador de registros no es lo bastante inteligente para basarse en las llaves.

No hay límite al número de cabeceras de solicitud capturadas ni a su longitud, aunque es prudente
mantenerlos bajos para limitar el uso de memoria por flujo. Con el fin de mantener el formato de
registro consistente para un mismo frontend, las capturas de cabeceras solo pueden declararse en
un frontend. No es posible especificar una captura en una sección "defaults".

Ejemplo:

```text
capture request header Host len 15
capture request header X-Forwarded-For len 15
capture request header Referer len 15
```

Ver también: "capture cookie", "capture response header", así como la [sección 8](/es/haproxy/configuration-logging/) sobre el registro.

<a id="entry-4-2-capture-response-header"></a>

**`capture response header <name> len <length>`**

```haproxy
capture response header <name> len <length>
```

Captura y registra la última aparición de la cabecera de respuesta especificada.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<name>    es el nombre de la cabecera que se va a capturar. Los nombres de
          las cabeceras no distinguen mayúsculas de minúsculas, pero es
          práctica común escribirlos tal como aparecen en las respuestas,
          con la primera letra de cada palabra en mayúscula. El nombre de
          la cabecera no aparecerá en los registros: solo se informa del
          valor, pero se respeta la posición en los registros.

<length>  es el número máximo de caracteres que se extraen del valor y se
          informan en los registros. La cadena se truncará por la derecha
          si excede <length>.
```

Se captura el valor completo de la última aparición de la cabecera. El resultado se añadirá a los
registros entre llaves ('{}') después de las cabeceras de solicitud capturadas. Si se capturan
varias cabeceras, se delimitarán por una barra vertical ('\|') y aparecerán en el mismo orden en
que se declararon en la configuración. Las cabeceras inexistentes se registrarán como una cadena
vacía. Usos comunes de las capturas de cabeceras de respuesta incluyen la cabecera
"Content-length", que indica cuántos bytes se espera devolver, y la cabecera "Location" para
seguir redirecciones.

No hay límite al número de cabeceras de respuesta capturadas ni a su longitud, aunque es prudente
mantenerlos bajos para limitar el uso de memoria por flujo. Con el fin de mantener el formato de
registro consistente para un mismo frontend, las capturas de cabeceras solo pueden declararse en
un frontend. No es posible especificar una captura en una sección "defaults".

Ejemplo:

```text
capture response header Content-length len 9
capture response header Location len 15
```

Ver también: "capture cookie", "capture request header", así como la [sección 8](/es/haproxy/configuration-logging/) sobre el registro.

<a id="entry-4-2-clitcpka-cnt"></a>

**`clitcpka-cnt <count>`**

```haproxy
clitcpka-cnt <count>
```

Establece el número máximo de sondas keepalive que TCP debe enviar antes de descartar la conexión
en el lado del cliente.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<count>   es el número máximo de sondas keepalive.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPCNT. Si no se especifica, se usa el
parámetro TCP del sistema (tcp_keepalive_probes). La disponibilidad de este ajuste depende del
sistema operativo. Se sabe que funciona en Linux.

Ver también: "option clitcpka", "clitcpka-idle", "clitcpka-intvl".

<a id="entry-4-2-clitcpka-idle"></a>

**`clitcpka-idle <timeout>`**

```haproxy
clitcpka-idle <timeout>
```

Establece el tiempo que la conexión debe permanecer inactiva antes de que TCP comience a enviar
sondas keepalive, si está activado el envío de paquetes keepalive de TCP en el lado del cliente.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<timeout> es el tiempo que la conexión debe permanecer inactiva antes de que
          TCP comience a enviar sondas keepalive. Se especifica en segundos
          por defecto, pero puede estar en cualquier otra unidad si el
          número lleva la unidad como sufijo, tal y como se explica al
          principio de este documento.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPIDLE. Si no se especifica, se usa el
parámetro TCP del sistema (tcp_keepalive_time). La disponibilidad de este ajuste depende del
sistema operativo. Se sabe que funciona en Linux.

Ver también: "option clitcpka", "clitcpka-cnt", "clitcpka-intvl".

<a id="entry-4-2-clitcpka-intvl"></a>

**`clitcpka-intvl <timeout>`**

```haproxy
clitcpka-intvl <timeout>
```

Establece el tiempo entre sondas keepalive individuales en el lado del cliente.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<timeout> es el tiempo entre sondas keepalive individuales. Se especifica en
          segundos por defecto, pero puede estar en cualquier otra unidad
          si el número lleva la unidad como sufijo, tal y como se explica
          al principio de este documento.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPINTVL. Si no se especifica, se usa el
parámetro TCP del sistema (tcp_keepalive_intvl). La disponibilidad de este ajuste depende del
sistema operativo. Se sabe que funciona en Linux.

Ver también: "option clitcpka", "clitcpka-cnt", "clitcpka-idle".

<a id="entry-4-2-compression-algo"></a>

**`compression algo <algorithm> ...`**

```haproxy
compression algo <algorithm> ...
compression algo-req <algorithm>
compression algo-res <algorithm>
compression type <mime type> ...
```

Activa la compresión HTTP.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
algo     va seguido de la lista de algoritmos de compresión soportados para
         las respuestas (palabra clave heredada)
algo-req va seguido del algoritmo de compresión para las solicitudes (solo se
  proporciona uno).
algo-res va seguido de la lista de algoritmos de compresión soportados para
         las respuestas.
type     va seguido de la lista de tipos MIME que se comprimirán en las
         respuestas (palabra clave heredada).
type-req va seguido de la lista de tipos MIME que se comprimirán en las
         solicitudes.
type-res va seguido de la lista de tipos MIME que se comprimirán en las
         respuestas.
```

Los algoritmos soportados actualmente son:

```text
identity     sirve sobre todo para depuración, y fue útil para desarrollar
             la característica de compresión. Identity no aplica ningún
             cambio en los datos.

gzip         aplica compresión gzip. Este ajuste solo está disponible cuando
             se compiló con soporte para zlib o libslz.

deflate      igual que "gzip", pero con el algoritmo deflate y el formato
             zlib. Ten en cuenta que este algoritmo tiene un soporte
             ambiguo en muchos navegadores y ningún soporte en los más
             recientes. Se recomienda encarecidamente no usarlo para nada
             más que la experimentación. Este ajuste solo está disponible
             cuando se compiló con soporte para zlib o libslz.

raw-deflate  igual que "deflate" sin la envoltura zlib, y se usa como
             alternativa cuando el navegador quiere "deflate". Todos los
             navegadores principales lo entienden y, a pesar de violar los
             estándares, se sabe que funciona mejor que "deflate", al menos
             en MSIE y en algunas versiones de Safari. No lo uses junto con
             "deflate"; usa uno u otro, ya que ambos reaccionan al mismo
             token Accept-Encoding. Este ajuste solo está disponible cuando
             se compiló con soporte para zlib o libslz.
```

La compresión se activará en función de la cabecera de solicitud Accept-Encoding. Con identity,
no se tiene en cuenta esa cabecera. Si los servidores del backend soportan compresión HTTP, estas
directivas no tendrán efecto: HAProxy verá la respuesta comprimida y no volverá a comprimir. Si
los servidores del backend no soportan compresión HTTP y hay una cabecera Accept-Encoding en la
solicitud, HAProxy comprimirá la respuesta correspondiente.

La compresión se desactiva cuando: \* la solicitud no anuncia un algoritmo de compresión
soportado en la cabecera "Accept-Encoding" \* el mensaje de respuesta no es HTTP/1.1 o superior \*
el código de estado HTTP no es uno de 200, 201, 202 o 203 \* la respuesta no contiene ni una
cabecera "Content-Length" ni una "Transfer-Encoding" cuyo último valor sea "chunked" \* la
respuesta contiene una cabecera "Content-Type" cuyo primer valor comienza por "multipart" \* la
respuesta contiene el valor "no-transform" en la cabecera "Cache-control" \* el User-Agent
coincide con "Mozilla/4", salvo que sea MSIE 6 con XP SP2, o MSIE 7 y posteriores \* la respuesta
contiene una cabecera "Content-Encoding", lo que indica que ya está comprimida (ver compression
offload) \* la respuesta contiene una cabecera "ETag" no válida o múltiples cabeceras ETag \* el
tamaño del payload es menor que el tamaño mínimo (ver compression minsize-res)

Nota: La compresión no emite la cabecera Warning.

Ejemplos:

```text
compression algo gzip
compression type text/html text/plain
```

Ver también: "compression offload", "compression direction", "compression minsize-req" y
"compression minsize-res"

<a id="entry-4-2-compression-minsize-req"></a>

**`compression minsize-req <size>`**

```haproxy
compression minsize-req <size>
compression minsize-res <size>
```

Establece el tamaño mínimo del payload en bytes para que se aplique la compresión.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Los payloads menores que este tamaño no se comprimirán, evitando sobrecarga de CPU innecesaria
para datos que no se beneficiarían significativamente de la compresión. "minsize-req" se aplica a
las solicitudes y "minsize-res" a las respuestas. El valor por defecto es 0.

<a id="entry-4-2-compression-offload"></a>

**`compression offload`**

```haproxy
compression offload
```

Hace que HAProxy asuma por sí solo el trabajo de compresión.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

El ajuste "offload" hace que HAProxy elimine la cabecera Accept-Encoding para impedir que los
servidores del backend compriman las respuestas. Se recomienda encarecidamente no hacer esto
porque significa que todo el trabajo de compresión se realizará en el único punto donde está
ubicado HAProxy. Sin embargo, en algunos escenarios de despliegue, HAProxy puede instalarse frente
a una pasarela defectuosa con una implementación de compresión HTTP rota que no puede
desactivarse. En ese caso, HAProxy puede usarse para impedir que esa pasarela emita payloads no
válidos. En tal caso, simplemente eliminar la cabecera en la configuración no funciona porque se
aplica antes de que la cabecera se analice, lo que impide que HAProxy comprima. El ajuste
"offload" debería usarse entonces para tales escenarios.

Si este ajuste se usa en una sección defaults, se emite un aviso y la opción se ignora.

Ver también: "compression type", "compression algo", "compression direction"

<a id="entry-4-2-compression-direction"></a>

**`compression direction <direction> (deprecated)`**

```haproxy
compression direction <direction> (deprecated)
```

Permite a haproxy comprimir tanto solicitudes como respuestas. Los valores válidos son "request",
para comprimir solo solicitudes, "response", para comprimir solo respuestas, o "both", cuando se
quieren comprimir ambas. El valor por defecto es "response".

Esta directiva solo es relevante cuando el "filter compression" heredado estaba activado, ya que
con los filtros explícitos comp-req y comp-res la dirección de compresión es redundante.

Puede usarse en los siguientes contextos: http

Ver también: "compression type", "compression algo", "compression offload"

<a id="entry-4-2-cookie"></a>

**`cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]`**

```haproxy
cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]
              [ postonly ] [ preserve ] [ httponly ] [ secure ]
              [ domain <domain> ]* [ maxidle <idle> ] [ maxlife <life> ]
              [ dynamic ] [ attr <value> ]*
```

Activa la persistencia basada en cookies en un backend.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<name>    es el nombre de la cookie que se monitorizará, modificará o
          insertará para aportar persistencia. Esta cookie se envía al
          cliente mediante una cabecera "Set-Cookie" en la respuesta, y el
          cliente la devuelve en una cabecera "Cookie" en todas las
          solicitudes. Se debe tener especial cuidado en elegir un nombre
          que no entre en conflicto con ninguna cookie probable de la
          aplicación. Además, si los mismos backends pueden ser usados por
          los mismos clientes (p. ej. HTTP/HTTPS), se debe cuidar usar
          nombres de cookie diferentes entre todos los backends si no se
          desea persistencia entre ellos.

rewrite   Esta palabra clave indica que la cookie la proporcionará el
          servidor y que HAProxy tendrá que modificar su valor para
          establecer en ella el identificador del servidor. Este modo es
          práctico cuando la gestión de combinaciones complejas de
          cabeceras "Set-cookie" y "Cache-control" se deja a la aplicación.
          La aplicación puede entonces decidir si es apropiado o no emitir
          una cookie de persistencia. Como deben monitorizarse todas las
          respuestas, este modo no funciona en modo túnel HTTP. Salvo que
          el comportamiento de la aplicación sea muy complejo y/o esté
          roto, se aconseja no comenzar con este modo en los nuevos
          despliegues. Esta palabra clave es incompatible con "insert" y
          "prefix".

insert    Esta palabra clave indica que HAProxy tendrá que insertar la
          cookie de persistencia en las respuestas del servidor si el
          cliente aún no tenía una cookie que le hubiera permitido acceder
          a este servidor. Cuando se usa sin la opción "preserve", si el
          servidor emite una cookie con el mismo nombre, se eliminará
          antes del procesamiento. Por esta razón, este modo puede usarse
          para actualizar configuraciones existentes que se ejecutan en el
          modo "rewrite". La cookie será solo una cookie de sesión y no se
          almacenará en el disco del cliente. Por defecto, salvo que se
          añada la opción "indirect", el servidor verá las cookies emitidas
          por el cliente. Debido a los efectos de la caché, generalmente
          es prudente añadir las palabras clave "nocache" o "postonly"
          (ver abajo). La palabra clave "insert" no es compatible con
          "rewrite" y "prefix".

prefix    Esta palabra clave indica que, en lugar de depender de una cookie
          dedicada para la persistencia, se completará una existente. Esto
          puede ser necesario en algunos entornos específicos donde el
          cliente no soporta más que una única cookie y la aplicación ya
          la necesita. En este caso, siempre que el servidor establezca
          una cookie llamada <name>, se le añadirá como prefijo el
          identificador del servidor y un delimitador. El prefijo se
          eliminará de todas las solicitudes del cliente para que el
          servidor encuentre la cookie que emitió. Como todas las
          solicitudes y respuestas pueden ser modificadas, este modo no
          funciona en modo túnel. La palabra clave "prefix" no es
          compatible con "rewrite" e "insert". Nota: se recomienda
          encarecidamente no usar "indirect" con "prefix", de lo contrario
          las actualizaciones de la cookie del servidor no se enviarían a
          los clientes.

indirect  Cuando se especifica esta opción, no se emitirá ninguna cookie a
          un cliente que ya tenga una válida para el servidor que procesó
          la solicitud. Si el servidor establece él mismo tal cookie, se
          eliminará, salvo que la opción "preserve" también esté
          establecida. En modo "insert", esto eliminará además las cookies
          de las solicitudes transmitidas al servidor, haciendo el
          mecanismo de persistencia totalmente transparente desde el punto
          de vista de la aplicación. Nota: se recomienda encarecidamente no
          usar "indirect" con "prefix", de lo contrario las
          actualizaciones de la cookie del servidor no se enviarían a los
          clientes.

nocache   Esta opción se recomienda junto con el modo insert cuando hay una
          caché entre el cliente y HAProxy, pues garantiza que una
          respuesta almacenable en caché se marcará como no almacenable si
          hay que insertar una cookie. Esto es importante porque si, por
          ejemplo, todas las cookies de persistencia se añaden a una
          página de inicio almacenable en caché, todos los clientes
          obtendrán la página desde una caché exterior y compartirán todos
          la misma cookie de persistencia, haciendo que un servidor reciba
          mucho más tráfico que otros. Ver también las opciones "insert" y
          "postonly".

postonly  Esta opción garantiza que la inserción de cookies solo se
          realizará en las respuestas a solicitudes POST. Es una
          alternativa a la opción "nocache", porque las respuestas POST no
          son almacenables en caché, así que esto asegura que la cookie de
          persistencia nunca se guardará en la caché. Como la mayoría de
          los sitios no necesitan ningún tipo de persistencia antes del
          primer POST, que generalmente es una solicitud de inicio de
          sesión, este es un método muy eficiente para optimizar la caché
          sin riesgo de encontrar una cookie de persistencia en la caché.
          Ver también las opciones "insert" y "nocache".

preserve  Esta opción solo puede usarse con "insert" y/o "indirect".
          Permite que el servidor emita la cookie de persistencia por sí
          mismo. En este caso, si se encuentra una cookie en la respuesta,
          HAProxy la dejará intacta. Esto es útil, por ejemplo, para
          terminar la persistencia tras una solicitud de cierre de sesión.
          Para ello, el servidor solo tiene que emitir una cookie con un
          valor inválido (p. ej. vacío) o con una fecha en el pasado.
          Combinando este mecanismo con la opción de comprobación
          "disable-on-404", es posible realizar un apagado totalmente controlado porque los usuarios abandonarán definitivamente el
          servidor tras cerrar sesión.

httponly  Esta opción indica a HAProxy que añada un atributo de cookie
          "HttpOnly" cuando se inserta una cookie. Este atributo se usa
          para que un agente de usuario no comparta la cookie con
          componentes no HTTP. Consulta RFC6265 para más información sobre
          este atributo.

secure    Esta opción indica a HAProxy que añada un atributo de cookie
          "Secure" cuando se inserta una cookie. Este atributo se usa para
          que un agente de usuario nunca emita esta cookie por canales no
          seguros, lo que significa que una cookie aprendida con este
          atributo solo se presentará por conexiones SSL/TLS. Consulta
          RFC6265 para más información sobre este atributo.

domain    Esta opción permite especificar el dominio en el que se inserta
          una cookie. Requiere exactamente un parámetro: un nombre de
          dominio válido. Si el dominio comienza por un punto, el
          navegador puede usarla para cualquier host que termine con ese
          nombre. También es posible especificar varios nombres de dominio
          invocando esta opción varias veces. Algunos navegadores pueden
          tener límites bajos en el número de dominios, así que ten
          cuidado al hacerlo. Para que conste, enviar 10 dominios a MSIE 6
          o Firefox 2 funciona como se espera.

maxidle   Esta opción permite que las cookies insertadas se ignoren tras
          cierto tiempo de inactividad. Solo funciona con cookies en modo
          insert. Cuando se envía una cookie al cliente, también se envía
          la fecha de emisión de esa cookie. En presentaciones posteriores
          de esta cookie, si la fecha es más antigua que el retraso
          indicado por el parámetro (en segundos), se ignorará. De lo
          contrario, se renovará si es necesario cuando se envíe la
          respuesta al cliente. Esto es particularmente útil para evitar
          que los usuarios que nunca cierran su navegador permanezcan
          demasiado tiempo en el mismo servidor (p. ej. tras un cambio en
          el tamaño de la granja). Cuando esta opción está establecida y
          una cookie no tiene fecha, siempre se acepta, pero se renueva en
          la respuesta. Esto mantiene la capacidad de los administradores
          de acceder a sus sitios. Las cookies con una fecha en el futuro
          más allá de 24 horas se ignoran. Esto permite a los
          administradores corregir problemas de zona horaria sin riesgo de
          expulsar a los usuarios del sitio.

maxlife   Esta opción permite que las cookies insertadas se ignoren tras
          cierto tiempo de vida, se usen o no. Solo funciona con cookies
          en modo insert. Cuando la cookie se envía por primera vez al
          cliente, también se envía la fecha de emisión. En presentaciones
          posteriores de esta cookie, si la fecha es más antigua que el
          retraso indicado por el parámetro (en segundos), se ignorará. Si
          la cookie de la solicitud no tiene fecha, se acepta y se le
          asigna una fecha. Las cookies con una fecha en el futuro más
          allá de 24 horas se ignoran, lo que permite a los
          administradores corregir problemas de zona horaria sin riesgo de
          expulsar a los usuarios del sitio. Contrariamente a maxidle,
          este valor no se renueva: solo cuenta la fecha de la primera
          visita. Pueden usarse maxidle y maxlife al mismo tiempo. Esto es
          particularmente útil para evitar que los usuarios que nunca
          cierran su navegador permanezcan demasiado tiempo en el mismo
          servidor (p. ej. tras un cambio en el tamaño de la granja). Es
          más estricto que el método maxidle en cuanto que fuerza una
          redistribución tras cierto retraso absoluto.

dynamic   Activa las cookies dinámicas. Cuando se usa, se crea
          dinámicamente una cookie de sesión para cada servidor, basada en
          la IP y el puerto del servidor, y una clave secreta, especificada
          en la directiva de backend "dynamic-cookie-key". La cookie se
          regenerará cada vez que cambie la dirección IP, y solo se genera
          para IPv4/IPv6.

attr      Esta opción indica a HAProxy que añada un atributo adicional
          cuando se inserta una cookie. El valor del atributo puede
          contener cualquier carácter excepto los de control o ";".
          Esta opción puede repetirse.
```

Solo puede haber una cookie de persistencia por backend HTTP, y puede declararse en una sección
defaults. El valor de la cookie será el indicado tras la palabra clave "cookie" en una instrucción
"server". Si no se declara cookie para un servidor dado, la cookie no se establece.

Ejemplos:

```text
cookie JSESSIONID prefix
cookie SRV insert indirect nocache
cookie SRV insert postonly indirect
cookie SRV insert indirect nocache maxidle 30m maxlife 8h
```

Ver también: "balance source", "capture cookie", "server" y "ignore-persist".

<a id="entry-4-2-declare-capture"></a>

**`declare capture [ request | response ] len <length>`**

```haproxy
declare capture [ request | response ] len <length>
```

Declara un hueco de captura.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<length> es la longitud permitida para la captura.
```

Esta declaración solo está disponible en la sección frontend o listen, pero el hueco reservado
puede usarse en los backends. La palabra clave "request" asigna un hueco de captura para su uso
en la solicitud, y "response" asigna un hueco de captura para su uso en la respuesta.

Ver también: "capture-req", "capture-res" (conversores de muestra), "capture.req.hdr",
"capture.res.hdr" (obtención de muestras), "http-request capture" y "http-response capture".

<a id="entry-4-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

Cambia las opciones por defecto de un servidor en un backend

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<param*>  es una lista de parámetros para este servidor. La palabra clave
          "default-server" acepta un número importante de opciones y tiene
          una sección completa dedicada a ella. Ver la sección 5 para más
          detalles.
```

Ejemplo:

```text
default-server inter 1000 weight 13
```

Ver también: "server" y la [sección 5](/es/haproxy/bind-and-server-options/) sobre las opciones de servidor

<a id="entry-4-2-default-backend"></a>

**`default_backend <backend>`**

```haproxy
default_backend <backend>
```

Especifica el backend a usar cuando ninguna regla "use_backend" ha coincidido.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<backend> es el nombre del backend que se va a usar.
```

Al hacer conmutación de contenido entre frontend y backends mediante la palabra clave
"use_backend", a menudo es útil indicar qué backend se usará cuando ninguna regla haya coincidido.
Generalmente es el backend dinámico el que recogerá todas las solicitudes indeterminadas.

Si un backend está desactivado o no publicado, las reglas default_backend que lo apunten se
ignorarán y el procesamiento del flujo permanecerá en el proxy original.

Ejemplo:

```text
use_backend     dynamic  if  url_dyn
use_backend     static   if  url_css url_img extension_img
default_backend dynamic
```

Ver también: "use_backend"

<a id="entry-4-2-description"></a>

**`description <string>`**

```haproxy
description <string>
```

Describe un listen, frontend o backend.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Argumentos: cadena

Permite añadir una frase para describir el objeto relacionado en la página HTML de estadísticas
de HAProxy. La descripción se mostrará a la derecha del nombre del objeto que describe. No es
necesario escapar con barra invertida los espacios en los argumentos `<string>`.

<a id="entry-4-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Desactiva un proxy, frontend o backend.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

La palabra clave "disabled" se usa para desactivar una instancia, principalmente para liberar un
puerto de escucha o desactivar temporalmente un servicio. La instancia seguirá creándose y su
configuración se comprobará, pero se creará en estado "stopped" y así aparecerá en las
estadísticas. No recibirá ningún tráfico ni enviará comprobaciones de estado ni registros. Es
posible desactivar muchas instancias a la vez añadiendo la palabra clave "disabled" en una sección
"defaults".

Por defecto, un backend desactivado no puede seleccionarse para conmutación de contenido. Sin
embargo, una parte del tráfico puede ignorar esto cuando se usa "force-be-switch".

Ver también: "enabled", "force-be-switch"

<a id="entry-4-2-dispatch"></a>

**`dispatch <address>:<port>   (deprecated)`**

```haproxy
dispatch <address>:<port>   (deprecated)
```

Establece una dirección de servidor por defecto

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<address> es la dirección IPv4 del servidor por defecto. Alternativamente, se
          soporta un nombre de host resoluble, pero este nombre se
          resolverá durante el arranque.

<ports>   es una especificación obligatoria de puerto. Todas las conexiones
          se enviarán a este puerto, y no está permitido usar
          desplazamientos de puerto como es posible con los servidores
          normales.
```

La palabra clave "dispatch" designa un servidor por defecto para su uso cuando ningún otro
servidor puede tomar la conexión. En el pasado se usaba para reenviar conexiones no persistentes a
un balanceador de carga auxiliar. Debido a su sintaxis simple, también se ha usado para relés TCP
simples. Se recomienda no usarla para mayor claridad, y usar en su lugar la directiva "server".

Esta palabra clave quedó obsoleta en 3.3 y se eliminará en 3.5 debido a algunas limitaciones
internas (sin soporte de SSL ni de conexiones inactivas, etc.). Su uso emitirá un aviso que puede
silenciarse activando la directiva "expose-deprecated-directives" en la sección global.

La manera correcta de proceder sin esta directiva es simplemente declarar un servidor con la misma
dirección y puerto. Si la directiva "dispatch" se mezclaba con otros servidores, esos servidores
deberían configurarse con un peso de cero para no ser elegidos nunca por el algoritmo de balanceo
de carga.

Ejemplo:

```text
backend deprecated_setup
    dispatch 192.168.100.100:80 # external load balancer's address
    server s1 192.168.100.1:80 cookie S1 check
    server s2 192.168.100.2:80 cookie S2 check

backend modern_setup
    server external_lb 192.168.100.100:80
    server s1 192.168.100.1:80 cookie S1 check weight 0
    server s2 192.168.100.2:80 cookie S2 check weight 0
```

Ver también: "server"

<a id="entry-4-2-dynamic-cookie-key"></a>

**`dynamic-cookie-key <string>`**

```haproxy
dynamic-cookie-key <string>
```

Establece la clave secreta de cookie dinámica para un backend.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: La clave secreta a usar.

Cuando las cookies dinámicas están activadas (ver la directiva "dynamic" de cookie), se crea una
cookie dinámica para cada servidor (salvo que se especifique una explícitamente en la línea
"server"), usando un hash de la dirección IP del servidor, el puerto TCP y la clave secreta. De
este modo, podemos garantizar la persistencia de sesión entre múltiples balanceadores de carga,
incluso si se añaden o eliminan servidores dinámicamente.

<a id="entry-4-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Activa un proxy, frontend o backend.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

La palabra clave "enabled" se usa para activar explícitamente una instancia cuando los valores
por defecto se han establecido a "disabled". Se usa muy raramente.

Ver también: "disabled"

<a id="entry-4-2-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

Devuelve el contenido de un archivo en lugar de los errores generados por HAProxy

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<code>    es el código de estado HTTP. Actualmente, HAProxy es capaz de
          generar los códigos 200, 400, 401, 403, 404, 405, 407, 408,
          410, 413, 414, 425, 429, 431, 500, 501, 502, 503 y 504.

<file>    designa un archivo que contiene la respuesta HTTP completa. Se
          recomienda seguir la práctica común de añadir ".http" al nombre
          del archivo para que la gente no confunda la respuesta con
          páginas de error HTML, y usar rutas absolutas, ya que los
          archivos se leen antes de realizar cualquier chroot.
```

Es importante entender que esta palabra clave no está pensada para reescribir los errores
devueltos por el servidor, sino los errores detectados y devueltos por HAProxy. Por esto, la
lista de errores soportados se limita a un conjunto pequeño.

El código 200 se emite en respuesta a solicitudes que coinciden con una regla "monitor-uri".

Los archivos se analizan cuando HAProxy arranca y deben ser válidos según la especificación HTTP.
No deberían superar el tamaño de búfer configurado (BUFSIZE), que generalmente es de 16 kB; de
lo contrario se devolverá un error interno. También es prudente no poner ninguna referencia a
contenidos locales (p. ej. imágenes) para evitar bucles entre el cliente y HAProxy cuando todos
los servidores están caídos, lo que causaría que se devuelva un error en lugar de una imagen.
Finalmente, la respuesta no puede superar (tune.bufsize - tune.maxrewrite) para que las reglas
"http-after-response" sigan teniendo margen de operación (ver "tune.maxrewrite").

Los archivos se leen al mismo tiempo que la configuración y se mantienen en memoria. Por esta
razón, los errores siguen devolviéndose incluso cuando el proceso está enjaulado con chroot, y
no se considera ningún cambio de archivo mientras el proceso está en ejecución. Un método simple
para desarrollar esos archivos consiste en asociarlos al código de estado 403 e interrogar una
URL bloqueada.

Ver también: "http-error", "errorloc", "errorloc302", "errorloc303"

Ejemplo:

```text
errorfile 400 /etc/haproxy/errorfiles/400badreq.http
errorfile 408 /dev/null  # work around Chrome pre-connect bug
errorfile 403 /etc/haproxy/errorfiles/403forbid.http
errorfile 503 /etc/haproxy/errorfiles/503sorry.http

```

<a id="entry-4-2-errorfiles"></a>

**`errorfiles <name> [<code> ...]`**

```haproxy
errorfiles <name> [<code> ...]
```

Importa, total o parcialmente, los archivos de error definidos en la sección http-errors `<name>`.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<name>  es el nombre de una sección http-errors existente.

<code>  es un código de estado HTTP. Pueden listarse varios códigos de
        estado. Actualmente, HAProxy es capaz de generar los códigos 200,
        400, 401, 403, 404, 405, 407, 408, 410, 413, 414, 425, 429, 431,
        500, 501, 502, 503 y 504.
```

Los errores definidos en la sección http-errors con el nombre `<name>` se importan en el proxy
actual. Si no se especifica ningún código de estado, se importan todos los archivos de error de
la sección http-errors. En caso contrario, solo se importan los archivos de error asociados a los
códigos de estado listados. Esos archivos de error sustituyen a los errores personalizados ya
definidos para el proxy. Y a su vez pueden ser sustituidos por los siguientes. Funcionalmente,
es exactamente lo mismo que declarar a mano todos los archivos de error usando directivas
"errorfile".

Ver también: "http-error", "errorfile", "errorloc", "errorloc302" , "errorloc303" y la [sección 12.4](/es/haproxy/other-sections/#section-12-4)
sobre http-errors.

Ejemplo:

```text
errorfiles generic
errorfiles site-1 403 404

```

<a id="entry-4-2-errorloc"></a>

**`errorloc <code> <url>`**

```haproxy
errorloc <code> <url>
errorloc302 <code> <url>
```

Devuelve una redirección HTTP a una URL en lugar de los errores generados por HAProxy

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<code>    es el código de estado HTTP. Actualmente, HAProxy es capaz de
          generar los códigos 200, 400, 401, 403, 404, 405, 407, 408,
          410, 413, 414, 425, 429, 431, 500, 501, 502, 503 y 504.

<url>     es el contenido exacto de la cabecera "Location". Puede contener
          un URI relativo a una página de error alojada en el mismo sitio,
          o un URI absoluto que designe una página de error en otro sitio.
          Se debe prestar especial atención a los URI relativos para
          evitar bucles de redirección si el propio URI puede generar el
          mismo error (p. ej. 500).
```

Es importante entender que esta palabra clave no está pensada para reescribir los errores
devueltos por el servidor, sino los errores detectados y devueltos por HAProxy. Por esto, la
lista de errores soportados se limita a un conjunto pequeño.

El código 200 se emite en respuesta a solicitudes que coinciden con una regla "monitor-uri".

Ten en cuenta que ambas palabras clave devuelven el código de estado HTTP 302, que indica al
cliente que recupere la URL designada usando el mismo método HTTP. Esto puede ser bastante
problemático en el caso de métodos distintos de GET, como POST, porque la URL enviada al cliente
podría no estar permitida para algo distinto de GET. Para sortear este problema, usa
"errorloc303", que envía el código de estado HTTP 303, indicando al cliente que la URL debe
recuperarse con una solicitud GET.

Ver también: "http-error", "errorfile", "errorloc303"

<a id="entry-4-2-errorloc303"></a>

**`errorloc303 <code> <url>`**

```haproxy
errorloc303 <code> <url>
```

Devuelve una redirección HTTP a una URL en lugar de los errores generados por HAProxy

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<code>    es el código de estado HTTP. Actualmente, HAProxy es capaz de
          generar los códigos 200, 400, 401, 403, 404, 405, 407, 408,
          410, 413, 414, 425, 429, 431, 500, 501, 502, 503 y 504.

<url>     es el contenido exacto de la cabecera "Location". Puede contener
          un URI relativo a una página de error alojada en el mismo sitio,
          o un URI absoluto que designe una página de error en otro sitio.
          Se debe prestar especial atención a los URI relativos para
          evitar bucles de redirección si el propio URI puede generar el
          mismo error (p. ej. 500).
```

Es importante entender que esta palabra clave no está pensada para reescribir los errores
devueltos por el servidor, sino los errores detectados y devueltos por HAProxy. Por esto, la
lista de errores soportados se limita a un conjunto pequeño.

El código 200 se emite en respuesta a solicitudes que coinciden con una regla "monitor-uri".

Ten en cuenta que ambas palabras clave devuelven el código de estado HTTP 303, que indica al
cliente que recupere la URL designada usando el mismo método HTTP GET. Esto resuelve los
problemas habituales asociados a "errorloc" y al código 302. Es posible que algunos navegadores
muy antiguos diseñados antes de HTTP/1.1 no lo soporten, pero no se ha informado de tal problema
hasta ahora.

Ver también: "http-error", "errorfile", "errorloc", "errorloc302"

<a id="entry-4-2-email-alert-from"></a>

**`email-alert from <emailaddr>`**

```haproxy
email-alert from <emailaddr>
```

Declara la dirección de correo electrónico de origen que se usará tanto en el sobre como en la
cabecera de las alertas por correo. Esta es la dirección desde la que se envían las alertas por
correo.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<emailaddr> es la dirección de correo electrónico de origen que se usará al enviar alertas por correo
```

Requiere también que estén definidos "email-alert mailers" y "email-alert to" y, si es así, el
envío de alertas por correo queda activado para el proxy.

Ver también: "email-alert level", "email-alert mailers", "email-alert myhostname", "email-alert to",
la [sección 12.3](/es/haproxy/other-sections/#section-12-3) sobre mailers.

<a id="entry-4-2-email-alert-level"></a>

**`email-alert level <level>`**

```haproxy
email-alert level <level>
```

Declara el nivel máximo de registro de los mensajes para los que se enviarán alertas por correo.
Actúa como un filtro sobre el envío de alertas por correo.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<level> Uno de los 8 niveles de syslog:
          emerg alert crit err warning notice info  debug
        Los niveles de syslog anteriores están ordenados de menor a mayor.
```

Por defecto el nivel es alert

Requiere también que estén definidos "email-alert from", "email-alert mailers" y "email-alert to"
y, si es así, el envío de alertas por correo queda activado para el proxy.

Las alertas se envían cuando:

- Un servidor no pausado se marca como caído y `<level>` es alert o inferior
- Un servidor pausado se marca como caído y `<level>` es notice o inferior
- Un servidor se marca como activo o entra en estado drain y `<level>` es notice o inferior
- "option log-health-checks" está activado, `<level>` es info o inferior, y ocurre una
  actualización del estado de una comprobación de estado

Ver también: "email-alert from", "email-alert mailers", "email-alert myhostname", "email-alert to",
la [sección 12.3](/es/haproxy/other-sections/#section-12-3) sobre mailers.

<a id="entry-4-2-email-alert-mailers"></a>

**`email-alert mailers <mailersect>`**

```haproxy
email-alert mailers <mailersect>
```

Declara los mailers que se usarán al enviar alertas por correo

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<mailersect> es el nombre de la sección mailers que se usará para enviar las alertas por correo.
```

Requiere también que estén definidos "email-alert from" y "email-alert to" y, si es así, el envío
de alertas por correo queda activado para el proxy.

Ver también: "email-alert from", "email-alert level", "email-alert myhostname", "email-alert to",
la [sección 12.3](/es/haproxy/other-sections/#section-12-3) sobre mailers.

<a id="entry-4-2-email-alert-myhostname"></a>

**`email-alert myhostname <hostname>`**

```haproxy
email-alert myhostname <hostname>
```

Declara el nombre de host que se usará al comunicarse con los mailers.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<hostname> es el nombre de host que se usará al comunicarse con los mailers
```

Por defecto se usa el nombre de host del sistema.

Requiere también que estén definidos "email-alert from", "email-alert mailers" y "email-alert to"
y, si es así, el envío de alertas por correo queda activado para el proxy.

Ver también: "email-alert from", "email-alert level", "email-alert mailers", "email-alert to", la [sección
12.3](/es/haproxy/other-sections/#section-12-3) sobre mailers.

<a id="entry-4-2-email-alert-to"></a>

**`email-alert to <emailaddr>`**

```haproxy
email-alert to <emailaddr>
```

Declara tanto la dirección de destinatario en el sobre como la dirección de destino en la
cabecera de las alertas por correo. Esta es la dirección a la que se envían las alertas por
correo.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<emailaddr> es la dirección de correo electrónico de destino que se usará al enviar alertas por correo
```

Requiere también que estén definidos "email-alert mailers" y "email-alert to" y, si es así, el
envío de alertas por correo queda activado para el proxy.

Ver también: "email-alert from", "email-alert level", "email-alert mailers", "email-alert myhostname",
la [sección 12.3](/es/haproxy/other-sections/#section-12-3) sobre mailers.

<a id="entry-4-2-error-log-format"></a>

**`error-log-format <fmt>`**

```haproxy
error-log-format <fmt>
```

Especifica la cadena de formato de registro a usar en caso de error de conexión en el lado del
frontend.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Esta directiva especifica la cadena de formato de registro que se usará para los registros que
contienen información relacionada con errores, tiempos de espera agotados, reintentos, redistribuciones o códigos de estado HTTP 5xx. En resumen, este formato se usará para cada línea de registro que
concerniría a la opción "log-separate-errors", incluidos los errores de conexión descritos en la
[sección 8.2.5](/es/haproxy/configuration-logging/#section-8-2-5).

Si la directiva se usa en una sección defaults, todos los frontends posteriores usarán el mismo
formato de registro. Consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6),
que cubre en profundidad la cadena de formato de registro personalizado.

La directiva "error-log-format" prevalece sobre directivas "error-log-format" anteriores.

<a id="entry-4-2-force-persist"></a>

**`force-persist { if | unless } <condition>`**

```haproxy
force-persist { if | unless } <condition>
```

Declara una condición para forzar la persistencia en servidores caídos

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Por defecto, las solicitudes no se despachan a servidores caídos. Es posible forzarlo usando
"option persist", pero es incondicional y reenvía a un servidor válido si "option redispatch"
está definido. Esto deja muy pocas posibilidades de forzar que algunas solicitudes lleguen a un
servidor marcado artificialmente como caído por operaciones de mantenimiento.

La instrucción "force-persist" permite declarar diversas condiciones basadas en ACL que, cuando
se cumplen, hacen que una solicitud ignore el estado caído de un servidor e intente conectarse a
él de todos modos. Esto posibilita arrancar un servidor que aún responde un error a las
comprobaciones de estado, y ejecutar un navegador configurado especialmente para probar el
servicio. Entre los métodos prácticos, se podría usar una dirección IP de origen específica, o
una cookie específica. La cookie tiene además la ventaja de que puede añadirse/eliminarse
fácilmente en el navegador desde una página de prueba. Una vez validado el servicio, es posible
abrirlo al mundo devolviendo una respuesta válida a las comprobaciones de estado.

La persistencia forzada se activa cuando se cumple una condición "if", o salvo que se cumpla una
condición "unless". El reenvío final siempre está desactivado cuando se usa esto.

Ver también: "option redispatch", "ignore-persist", "persist", y la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de las ACL.

<a id="entry-4-2-external-check-command"></a>

**`external-check command <command>`**

```haproxy
external-check command <command>
```

Ejecutable a ejecutar cuando se realiza un external-check

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<command> es el comando externo que se va a ejecutar
```

Los argumentos pasados al comando son:

`<proxy_address>` `<proxy_port>` `<server_address>` `<server_port>`

Los `<proxy_address>` y `<proxy_port>` se derivan del primer listener que sea IPv4, IPv6 o un
socket UNIX. En el caso de un listener de socket UNIX, proxy_address será la ruta del socket y
`<proxy_port>` será la cadena "NOT_USED". En una sección backend no es posible determinar un
listener, y tanto `<proxy_address>` como `<proxy_port>` tendrán el valor de cadena "NOT_USED".

Algunos valores también se proporcionan mediante variables de entorno.

Variables de entorno:

```text
HAPROXY_PROXY_ADDR      La primera dirección bind, si está disponible (o
                        vacía si no aplica, por ejemplo en una sección
                        "backend").

HAPROXY_PROXY_ID        El id del backend.

HAPROXY_PROXY_NAME      El nombre del backend.

HAPROXY_PROXY_PORT      El primer puerto bind, si está disponible (o vacío
                        si no aplica, por ejemplo en una sección
                        "backend" o para un socket UNIX).

HAPROXY_SERVER_ADDR     La dirección del servidor.

HAPROXY_SERVER_CURCONN  El número actual de conexiones en el servidor.

HAPROXY_SERVER_ID       El id del servidor.

HAPROXY_SERVER_MAXCONN  El número máximo de conexiones del servidor.

HAPROXY_SERVER_NAME     El nombre del servidor.

HAPROXY_SERVER_PORT     El puerto del servidor, si está disponible (o vacío
                        para un socket UNIX).

HAPROXY_SERVER_SSL      "0" cuando no se usa SSL, "1" cuando se usa

HAPROXY_SERVER_PROTO    El protocolo usado por este servidor, que puede ser
                        uno de "cli" (la CLI de haproxy), "syslog"
                        (servidor syslog TCP), "peers" (servidor TCP
                        peers), "h1" (servidor HTTP/1.x), "h2"
                        (servidor HTTP/2) o "tcp" (cualquier otro
                        servidor TCP).

PATH                    La variable de entorno PATH usada al ejecutar el
                        comando puede establecerse mediante
                        "external-check path".
```

Si el comando se ejecuta y termina con estado cero, la comprobación se considera superada; de
lo contrario, la comprobación se considera fallida.

Ejemplo:

```text
external-check command /bin/true
```

Ver también: "external-check", "option external-check", "external-check path"

<a id="entry-4-2-external-check-path"></a>

**`external-check path <path>`**

```haproxy
external-check path <path>
```

El valor de la variable de entorno PATH usado al ejecutar un external-check

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<path> es la ruta usada al ejecutar el comando externo
```

La ruta por defecto es "".

Ejemplo:

```text
external-check path "/usr/bin:/bin"
```

Ver también: "external-check", "option external-check", "external-check command"

<a id="entry-4-2-force-be-switch"></a>

**`force-be-switch { if | unless } <condition>`**

```haproxy
force-be-switch { if | unless } <condition>
```

Permite que la conmutación de contenido seleccione una instancia de backend incluso si está
desactivada o no publicada. Los administradores pueden usar esta regla para probar el tráfico
hacia servicios antes de exponerlos al mundo exterior.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Ver también: "be-unpublished", "disabled"

<a id="entry-4-2-filter"></a>

**`filter <name> [param*]`**

```haproxy
filter <name> [param*]
```

Añade el filtro `<name>` a la lista de filtros adjunta al proxy.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Argumentos:

```text
<name>     es el nombre del filtro. Los filtros soportados oficialmente se
           referencian en la sección 9.

<param*>   es una lista de parámetros aceptados por el filtro <name>. El
           análisis de estos parámetros es responsabilidad del filtro.
           Ver la documentación del filtro correspondiente (sección 9)
           para todos los detalles de los parámetros soportados.
```

Pueden usarse múltiples apariciones de la línea filter para el mismo proxy. El mismo filtro
puede referenciarse tantas veces como se necesite.

Ejemplo:

```text
listen
  bind *:80

  filter trace name BEFORE-HTTP-COMP
  filter compression
  filter trace name AFTER-HTTP-COMP

  compression algo gzip
  compression offload

  server srv1 192.168.0.1:80
```

Ver también: la [sección 9](/es/haproxy/filters/).

<a id="entry-4-2-fullconn"></a>

**`fullconn <conns>`**

```haproxy
fullconn <conns>
```

Especifica con qué carga del backend los servidores alcanzarán su maxconn

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<conns>   es el número de conexiones en el backend que hará que los
          servidores usen el número máximo de conexiones.
```

Cuando un servidor tiene especificado un parámetro "maxconn", significa que su número de
conexiones concurrentes nunca será mayor. Además, si tiene un parámetro "minconn", indica un
límite dinámico que sigue la carga del backend. El servidor aceptará entonces siempre al menos
`<minconn>` conexiones, nunca más de `<maxconn>`, y el límite estará en la rampa entre ambos
valores cuando el backend tenga menos de `<conns>` conexiones concurrentes. Esto permite limitar
la carga de los servidores en cargas normales, pero empujarla más lejos en cargas importantes sin
sobrecargar los servidores en cargas excepcionales.

Como es difícil acertar con este valor, HAProxy lo establece automáticamente al 10% de la suma
de los maxconn de todos los frontends que puedan derivar a este backend (basándose en las reglas
"use_backend" y "default_backend"). Así es seguro dejarlo sin definir. Sin embargo, los
"use_backend" que involucran nombres dinámicos no se cuentan, ya que no hay manera de saber si
podrían coincidir o no.

Ejemplo:

```shell
# The servers will accept between 100 and 1000 concurrent connections each
# and the maximum of 1000 will be reached when the backend reaches 10000
# connections.
backend dynamic
   fullconn   10000
   server     srv1   dyn1:80 minconn 100 maxconn 1000
   server     srv2   dyn2:80 minconn 100 maxconn 1000
```

Ver también: "maxconn", "server"

<a id="entry-4-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

Especifica un ID único global que distingue mayúsculas de minúsculas para este proxy.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

`<string>` debe ser único en toda la configuración de haproxy y en todos los tipos de objeto. El
formato se deja sin especificar para permitir al usuario elegir su política de nombres. La única
restricción es su longitud, que no puede ser mayor de 127 caracteres. Todos los valores
alfanuméricos y los caracteres '.', ':', '-' y '\_' son válidos. Ver también "shm-stats-file".

<a id="entry-4-2-hash-balance-factor"></a>

**`hash-balance-factor <factor>`**

```haproxy
hash-balance-factor <factor>
```

Especifica el factor de balanceo para el hash consistente con carga acotada

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| no \| sí

Argumentos:

```text
<factor> es el control del número máximo de solicitudes concurrentes que se
         envían a un servidor, expresado como porcentaje del número medio
         de solicitudes concurrentes en el conjunto de todos los
         servidores activos.
```

Especificar un "hash-balance-factor" para un servidor con "hash-type consistent" activa un
algoritmo que impide que un solo servidor reciba demasiadas solicitudes a la vez, incluso si
algunos cubos de hash reciben muchas más solicitudes que otros. Establecer `<factor>` a 0 (el
valor por defecto) desactiva la función. De lo contrario, `<factor>` es un porcentaje mayor que
100. Por ejemplo, si `<factor>` es 150, ningún servidor podrá tener una carga superior a 1.5
veces la media. Si se usan pesos de servidor, se respetarán.

Si el servidor de primera opción queda descalificado, el algoritmo elegirá otro servidor
basándose en el hash de la solicitud, hasta encontrar un servidor con capacidad adicional. Un
`<factor>` mayor permite más desequilibrio entre los servidores, mientras que un `<factor>`
menor significa que se comprobarán más servidores por término medio, afectando al rendimiento.
Valores razonables van de 125 a 200.

Este ajuste también lo usa "balance random", que internamente se basa en el mecanismo de hash
consistente.

Ver también: "balance" y "hash-type".

<a id="entry-4-2-hash-preserve-affinity"></a>

**`hash-preserve-affinity { always | maxconn | maxqueue }`**

```haproxy
hash-preserve-affinity { always | maxconn | maxqueue }
```

Especifica un método para asignar flujos a servidores con balanceo de carga por hash cuando los
servidores están saturados o tienen la cola llena.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Pueden especificarse los siguientes valores:

    - "always" : esta es la estrategia por defecto. Un flujo se asigna a un
                   servidor en función del hash, independientemente de si
                   el servidor está actualmente saturado o no.

    - "maxconn" : cuando se selecciona, se omitirán los servidores que
                   tienen "maxconn" establecido y están actualmente
                   saturados. Se elegirá otro servidor siguiendo el anillo
                   de hash. Esto no afecta a los servidores que no
                   establecen "maxconn". Si todos los servidores están
                   saturados, la solicitud se encola en el último servidor
                   del anillo de hash anterior al servidor inicialmente
                   seleccionado.

    - "maxqueue": cuando se selecciona, se omitirán los servidores que
                   tienen "maxconn" establecido, "maxqueue" establecido a
                   un valor no nulo (tamaño de cola limitado) y tienen
                   actualmente la cola llena. Se elegirá otro servidor
                   siguiendo el anillo de hash. Esto no afecta a los
                   servidores que no establecen a la vez "maxconn" y
                   "maxqueue".

Ver también: "maxconn", "maxqueue", "hash-balance-factor"

<a id="entry-4-2-hash-type"></a>

**`hash-type <method> <function> <modifier>`**

```haproxy
hash-type <method> <function> <modifier>
```

Especifica un método para mapear hashes a servidores

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<method> es el método usado para seleccionar un servidor a partir del hash
         calculado por la <function>:

  map-based   la tabla hash es un array estático que contiene todos los
              servidores vivos. Los hashes serán muy suaves, tendrán en
              cuenta los pesos, pero serán estáticos en el sentido de que
              los cambios de peso mientras un servidor está activo se
              ignorarán. Esto significa que no habrá arranque lento
              (slow start). Además, como un servidor se selecciona por su
              posición en el array, la mayoría de las asignaciones cambian
              cuando cambia el número de servidores. Esto significa que
              cuando un servidor sube o baja, o cuando se añade un
              servidor a una granja, la mayoría de las conexiones se
              redistribuirán a servidores diferentes. Esto puede ser
              inconveniente, por ejemplo, con las cachés.

  consistent  la tabla hash es un árbol lleno de muchas apariciones de cada
              servidor. La clave hash se busca en el árbol y se elige el
              servidor más cercano. Este hash es dinámico, soporta
              cambios de pesos mientras los servidores están activos, así
              que es compatible con la característica de arranque lento.
              Tiene la ventaja de que cuando un servidor sube o baja, solo
              se mueven sus asociaciones. Cuando se añade un servidor a
              la granja, solo una pequeña parte de las asignaciones se
              redistribuye, lo que lo convierte en un método ideal para
              cachés. Sin embargo, debido a su principio, la distribución
              nunca será muy suave y a veces puede ser necesario ajustar
              el peso o el ID de un servidor para obtener una distribución
              más equilibrada. Para obtener la misma distribución en
              varios balanceadores de carga, es importante que todos los
              servidores tengan exactamente los mismos IDs. Nota: el hash
              consistente usa sdbm y avalanche si no se especifica
              ninguna función hash.

<function> es la función hash que se va a usar:

   sdbm   esta función se creó inicialmente para la biblioteca de bases de
          datos sdbm (una reimplementación de dominio público de ndbm).
          Demostró mezclar bien los bits, lo que produce una mejor
          distribución de las claves y menos divisiones. También resulta
          ser una buena función hash general con buena distribución,
          salvo cuando el peso total de los servidores es múltiplo de 64,
          en cuyo caso aplicar el modificador avalanche puede ayudar.

   djb2   esta función fue propuesta por Dan Bernstein hace muchos años en
          comp.lang.c. Los estudios han demostrado que, para ciertas
          cargas de trabajo, esta función proporciona una mejor
          distribución que sdbm. Generalmente funciona bien con entradas
          de texto, aunque puede comportarse extremadamente mal con
          entradas solo numéricas o cuando el peso total de los
          servidores es múltiplo de 33, salvo que también se use el
          modificador avalanche.

   wt6    esta función se diseñó para HAProxy mientras se probaban otras
          funciones en el pasado. No es tan suave como las otras, pero es
          mucho menos sensible al conjunto de datos de entrada o al
          número de servidores. Puede tener sentido como alternativa a
          sdbm+avalanche o djb2+avalanche para el hash consistente o para
          hacer hash de datos numéricos como una dirección IP de origen o
          un identificador de visitante en un parámetro de URL.

   crc32  esta es la implementación CRC32 más común, usada en Ethernet,
          gzip, PNG, etc. Es más lenta que las otras pero puede ofrecer
          una mejor distribución o resultados menos predecibles,
          especialmente al usarse con cadenas.

   none   no calcula el hash de la clave; la clave se usará directamente
          como hash. Esto puede ser útil para calcular manualmente el
          hash de la clave usando un convertidor para tal fin y dejar
          que haproxy use el resultado directamente. La operación
          convertirá la clave a cadena si aún no lo es, y la interpretará
          como un entero cuyo valor se usará como clave. Algunos tipos de
          clave de entrada podrían no ser adecuados aquí (p. ej. las
          direcciones IP).

<modifier> indica un método opcional aplicado tras calcular el hash de la
         clave:

   avalanche   Esta directiva indica que el resultado de la función hash
               anterior no debe usarse en bruto, sino que antes debe
               aplicarse un hash completo de avalancha de 4 bytes. El
               propósito de este paso es mezclar los bits resultantes del
               hash anterior para evitar cualquier efecto no deseado
               cuando la entrada contiene valores limitados o cuando el
               número de servidores es múltiplo de una de las componentes
               del hash (64 para SDBM, 33 para DJB2). Activar avalanche
               tiende a hacer el resultado menos predecible, pero
               tampoco es tan suave como cuando se usa la función
               original. Es posible que se necesiten algunas pruebas con
               ciertas cargas de trabajo. Este hash es uno de los muchos
               propuestos por Bob Jenkins.
```

El tipo de hash por defecto es "map-based" y se recomienda para la mayoría de los usos. La
función por defecto es "sdbm"; la selección de una función debería basarse en el rango de los
valores a los que se aplica el hash.

Ver también: "balance", "hash-balance-factor", "hash-preserve-affinity", "server"

<a id="entry-4-2-http-after-response"></a>

**`http-after-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-after-response <action> <options...> [ { if | unless } <condition> ]
```

Control de acceso para todas las respuestas de capa 7 (las del servidor, las de applet/servicio
y las internas).

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

La instrucción http-after-response define un conjunto de reglas que se aplican al procesamiento
de capa 7. Las reglas se evalúan en su orden de declaración cuando aparecen en una sección
frontend, listen o backend. Como estas reglas se aplican a respuestas, las reglas del backend se
aplican primero, seguidas de las del frontend. Cualquier regla puede ir seguida opcionalmente de
una condición basada en ACL, en cuyo caso solo se evaluará si la condición se evalúa como
verdadera.

A diferencia de las reglas http-response, estas se aplican a todas las respuestas, las de los
servidores pero también a todas las respuestas generadas por HAProxy. Estas reglas se evalúan al
final del análisis de las respuestas, antes de la fase de reenvío de datos.

La condición se evalúa justo antes de que la acción se ejecute, y la acción se realiza
exactamente una vez. Así, no hay problema si una acción cambia un elemento que se comprueba como
parte de la condición. Esto también significa que múltiples acciones pueden basarse en la misma
condición, de modo que la primera acción que cambie la evaluación de la condición basta para
desactivar implícitamente las acciones restantes. Esto se usa, por ejemplo, al intentar asignar
un valor a una variable desde diversas fuentes cuando está vacía. No hay límite al número de
instrucciones "http-after-response" por instancia.

La primera palabra clave tras "http-after-response" en la sintaxis es la acción de la regla,
seguida opcionalmente de un número variable de argumentos para la acción. Las acciones
soportadas y sus respectivas sintaxis se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3)
«Acciones» (busca las acciones que marcan "HTTP Aft").

Esta directiva solo está disponible en secciones defaults con nombre, no en anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección de proxy asociada. Para
evitar ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con
capacidad de frontend y por proxies con capacidad de backend. Esto significa que una sección
listen no puede usar una sección defaults que defina tales reglas.

Nota: Los errores emitidos en una fase temprana del análisis de la solicitud los maneja el
multiplexor en un nivel inferior, antes de cualquier análisis http. Por tanto, no se evalúa
ningún conjunto de reglas http-after-response sobre estos errores.

Ejemplo:

```text
http-after-response set-header Strict-Transport-Security "max-age=31536000"
http-after-response set-header Cache-Control "no-store,no-cache,private"
http-after-response set-header Pragma "no-cache"

```

<a id="entry-4-2-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
```

Define un comentario para la regla http-check siguiente, mostrado en los registros si falla.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<string>  es el mensaje de comentario que se añadirá a los registros si
          falla la regla http-check siguiente.
```

Solo funciona con las reglas connect, send y expect. Es útil para elaborar informes de error
amigables para el usuario.

Ver también: "option httpchk", "http-check connect", "http-check send" y "http-check expect".

<a id="entry-4-2-http-check-connect"></a>

**`http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]`**

```haproxy
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
```

Abre una nueva conexión para realizar una comprobación de estado HTTP

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje que se informará si falla la evaluación de la regla.

default      Usa las opciones por defecto de la línea del servidor para
             hacer las comprobaciones de estado. Las opciones del
             servidor se usan solo si no se redefinen.

port <expr>  si no se establece, se usa el puerto de comprobación o el
             puerto del servidor. Indica a HAProxy dónde abrir la
             conexión. <port> debe ser un entero válido de puerto TCP de
             origen, de 1 a 65535, o una expresión sample-fetch.

addr <ip>    define la dirección IP con la que hacer la comprobación de
             estado.

send-proxy   envía una cadena de protocolo PROXY

via-socks4   habilita las comprobaciones de estado salientes usando un
             proxy socks4 ascendente.

ssl          abre una conexión cifrada

sni <sni>    especifica el SNI que se usará para hacer comprobaciones de
             estado sobre SSL.

alpn <alpn>  define qué protocolos anunciar con ALPN. La lista de
             protocolos consiste en una lista de nombres de protocolo
             delimitada por comas, por ejemplo: "h2,http/1.1". Si no se
             establece, se usa el ALPN del servidor.

proto <name> fuerza el protocolo del multiplexor que se usará para esta
             conexión. Debe ser un protocolo mux HTTP y debe poder usarse
             en el lado del backend. La lista de protocolos disponibles se
             muestra en haproxy -vv.

linger       cierra limpiamente la conexión en lugar de usar un único RST.
```

Al igual que con las comprobaciones de estado tcp-check, es posible configurar la conexión a
usar para realizar la comprobación de estado HTTP. Esta directiva también debería usarse para
describir un escenario que involucre varios intercambios solicitud/respuesta, posiblemente en
puertos diferentes o con servidores diferentes.

Cuando no hay ningún puerto TCP configurado en la línea server ni directiva de puerto de
servidor, el primer paso de la secuencia http-check debe ser especificar el puerto con un
"http-check connect".

En un conjunto de reglas http-check se requiere un 'connect'; también es obligatorio comenzar el
conjunto de reglas con una regla 'connect'. El propósito es asegurar que el administrador sabe lo
que hace.

Cuando un connect debe comenzar el conjunto de reglas, todavía puede ir precedido de reglas
set-var, unset-var o comment.

Ejemplos:

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option httpchk

http-check connect
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399
http-check connect port 443 ssl sni haproxy.1wt.eu
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399

server www 10.0.0.1 check port 80
```

Ver también: "option httpchk", "http-check send", "http-check expect"

<a id="entry-4-2-http-check-disable-on-404"></a>

**`http-check disable-on-404`**

```haproxy
http-check disable-on-404
```

Activa un modo de mantenimiento ante una respuesta HTTP/404 a las comprobaciones de estado

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando esta opción está definida, un servidor que devuelva un código HTTP 404 será excluido del
balanceo de carga posterior, pero seguirá recibiendo conexiones persistentes. Esto proporciona
un método muy cómodo para que los administradores web realicen un apagado controlado de sus
servidores. También es importante señalar que un servidor detectado como fallido mientras estaba
en este modo no generará una alerta, solo un aviso. Si el servidor vuelve a responder 2xx o 3xx,
se reincorporará inmediatamente a la granja. El estado en la página de estadísticas muestra
"NOLB" para un servidor en este modo. Es importante señalar que esta opción solo funciona junto
con la opción "httpchk". Si esta opción se usa con "http-check expect", tiene precedencia sobre
ella, de modo que las respuestas 404 seguirán considerándose como parada suave. Ten en cuenta
también que un servidor detenido permanecerá detenido aunque responda 404. Esta opción solo se
evalúa para servidores en ejecución.

Ver también: "option httpchk" y "http-check expect".

<a id="entry-4-2-http-check-expect"></a>

**`http-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
```

Hace que las comprobaciones de estado HTTP consideren el contenido de las respuestas o códigos
de estado específicos

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje que se informará si falla la evaluación de la regla.

min-recv  es opcional y puede definir la cantidad mínima de datos necesaria
          para evaluar la regla expect actual. Si el número de bytes
          recibidos está por debajo de este límite, la comprobación
          esperará más datos. Esta opción puede usarse para resolver
          algunas reglas de coincidencia ambiguas o para evitar ejecutar
          coincidencias de expresiones regulares costosas sobre contenido
          que se sabe que está aún incompleto. Si se usa una cadena exacta,
          se usa el mínimo entre la longitud de la cadena y este
          parámetro. Este parámetro se ignora si se establece a -1. Si la
          regla expect no coincide, la comprobación esperará más datos.
          Si se establece a 0, el resultado de la evaluación siempre es
          concluyente.

ok-status <st>     es opcional y puede usarse para establecer el estado de
                   la comprobación si la regla expect se evalúa con éxito
                   y es la última regla del conjunto de reglas tcp-check.
                   Se soportan "L7OK", "L7OKC", "L6OK" y "L4OK":
                     - L7OK : comprobación superada en capa 7
                     - L7OKC: comprobación superada condicionalmente en
                               capa 7; pone el servidor en estado NOLB.
                     - L6OK : comprobación superada en capa 6
                     - L4OK : comprobación superada en capa 4
                   Por defecto se usa "L7OK".

error-status <st>  es opcional y puede usarse para establecer el estado de
                   la comprobación si ocurre un error durante la
                   evaluación de la regla expect. Se soportan "L7OKC",
                   "L7RSP", "L7STS", "L6RSP" y "L4CON":
                     - L7OKC: comprobación superada condicionalmente en
                               capa 7; pone el servidor en estado NOLB.
                     - L7RSP: respuesta inválida de capa 7 - error de
                               protocolo
                     - L7STS: error de respuesta de capa 7, por ejemplo
                               HTTP 5xx
                     - L6RSP: respuesta inválida de capa 6 - error de
                               protocolo
                     - L4CON: problema de conexión en capas 1-4
                   Por defecto se usa "L7RSP".

tout-status <st>   es opcional y puede usarse para establecer el estado de
                   la comprobación si se agota el tiempo de espera durante
                   la evaluación de la regla expect. Se soportan "L7TOUT",
                   "L6TOUT" y "L4TOUT":
                     - L7TOUT: tiempo de espera agotado en capa 7
                               (HTTP/SMTP)
                     - L6TOUT: tiempo de espera agotado en capa 6 (SSL)
                     - L4TOUT: tiempo de espera agotado en capas 1-4
                   Por defecto se usa "L7TOUT".

on-success <fmt>   es opcional y puede usarse para personalizar el mensaje
                   informativo que se informa en los registros si la regla
                   expect se evalúa con éxito y es la última regla del
                   conjunto de reglas tcp-check. <fmt> es una cadena de
                   formato de registro personalizado (ver sección 8.2.6).

on-error <fmt>     es opcional y puede usarse para personalizar el mensaje
                   informativo que se informa en los registros si ocurre
                   un error durante la evaluación de la regla expect.
                   <fmt> es una cadena de formato de registro
                   personalizado (ver sección 8.2.6).

status-code <expr> es opcional y puede usarse para establecer el código de
                   estado de la comprobación que se informa en los
                   registros, en caso de éxito o de error. <expr> es una
                   expresión HAProxy estándar formada por un sample-fetch
                   seguido de algunos convertidores.

<match>   es una palabra clave que indica cómo buscar un patrón específico
          en la respuesta. La palabra clave puede ser una de "status",
          "rstatus", "hdr", "fhdr", "string" o "rstring". La palabra clave
          puede ir precedida de un signo de exclamación ("!") para negar
          la coincidencia. Se permiten espacios entre el signo de
          exclamación y la palabra clave. Ver abajo más detalles sobre las
          palabras clave soportadas.

<pattern> es el patrón que se va a buscar. Puede ser una cadena, una
          expresión regular o un patrón más complejo con varios
          argumentos. Si el patrón de cadena contiene espacios, deben
          escaparse con la barra invertida habitual ('\').
```

Por defecto, "option httpchk" considera que los estados de respuesta 2xx y 3xx son válidos, y
que los demás no lo son. Cuando se usa "http-check expect", define qué se considera válido o no
válido. Solo se soporta una instrucción "http-check" por backend. Si un servidor no responde o
agota el tiempo de espera, la comprobación obviamente falla. Las coincidencias disponibles son:

```text
status <codes>:  comprueba los códigos de estado resultantes de analizar la
                  cadena <codes>. Debe ser una lista separada por comas de
                  códigos de estado o de rangos de códigos. Una respuesta
                  de comprobación de estado se considerará válida si el
                  código de estado de la respuesta coincide con cualquier
                  código de estado o está dentro de cualquier rango de la
                  lista. Si la palabra clave "status" va precedida de "!",
                  la respuesta se considerará inválida si el código de
                  estado coincide.

rstatus <regex>: comprueba una expresión regular contra el código de estado
                  HTTP. Una respuesta de comprobación de estado se
                  considerará válida si el código de estado de la
                  respuesta coincide con la expresión. Si la palabra clave
                  "rstatus" va precedida de "!", la respuesta se
                  considerará inválida si el código de estado coincide.
                  Se usa sobre todo para comprobar varios códigos.

hdr  { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  comprueba el patrón de cabecera especificado en las
                  cabeceras de respuesta HTTP. El patrón del nombre es
                  obligatorio pero el patrón del valor es opcional. Si no
                  se especifica, solo se verifica la presencia de la
                  cabecera. <meth> es el método de coincidencia, aplicado
                  al nombre de la cabecera o al valor de la cabecera. Los
                  métodos de coincidencia soportados son "str"
                  (coincidencia exacta), "beg" (coincidencia de prefijo),
                  "end" (coincidencia de sufijo), "sub" (coincidencia de
                  subcadena) o "reg" (coincidencia de expresión regular).
                  Si no se especifica, se usa el método de coincidencia
                  exacta. Si se usa el parámetro "name-lf", <name> se
                  evalúa como una cadena de formato de registro
                  personalizado (ver sección 8.2.6). Si se usa el
                  parámetro "value-lf", <value> se evalúa como una cadena
                  log-format. Estos parámetros no pueden usarse con el
                  método de coincidencia por expresión regular. Por
                  último, el valor de la cabecera se considera una lista
                  separada por comas. Ten en cuenta que las
                  coincidencias no distinguen mayúsculas de minúsculas en
                  los nombres de cabecera.

fhdr { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  comprueba el patrón de cabecera completo especificado en
                  las cabeceras de respuesta HTTP. Hace exactamente lo
                  mismo que la palabra clave "hdr", salvo que se prueba el
                  valor completo de la cabecera y las comas no se
                  consideran delimitadores.

string <string>: comprueba la coincidencia exacta de la cadena en el cuerpo
                  de la respuesta HTTP. Una respuesta de comprobación de
                  estado se considerará válida si el cuerpo de la
                  respuesta contiene esta cadena exacta. Si la palabra
                  clave "string" va precedida de "!", la respuesta se
                  considerará inválida si el cuerpo contiene la cadena.
                  Puede usarse para buscar una palabra obligatoria al
                  final de una página dinámica, o para detectar un fallo
                  cuando aparece un error específico en la página de
                  comprobación (p. ej. un volcado de pila).

rstring <regex>: comprueba una expresión regular en el cuerpo de la
                  respuesta HTTP. Una respuesta de comprobación de estado
                  se considerará válida si el cuerpo de la respuesta
                  coincide con esta expresión. Si la palabra clave
                  "rstring" va precedida de "!", la respuesta se
                  considerará inválida si el cuerpo coincide con la
                  expresión. Puede usarse para buscar una palabra
                  obligatoria al final de una página dinámica, o para
                  detectar un fallo cuando aparece un error específico en
                  la página de comprobación (p. ej. un volcado de pila).

string-lf <fmt>: comprueba en el cuerpo de la respuesta HTTP la
                  coincidencia de una cadena de formato de registro
                  personalizado (ver sección 8.2.6). Una respuesta de
                  comprobación de estado se considerará válida si el
                  cuerpo de la respuesta contiene la cadena resultante de
                  la evaluación de <fmt>, que sigue las reglas de
                  log-format. Si va precedida de "!", la respuesta se
                  considerará inválida si el cuerpo contiene la cadena.
```

Es importante señalar que las respuestas estarán limitadas a un cierto tamaño definido por la
opción global "tune.bufsize", cuyo valor por defecto es 16384 bytes. Así, las respuestas
demasiado grandes pueden no contener el patrón obligatorio al usar "string" o "rstring". Si una
respuesta grande es absolutamente necesaria, es posible cambiar el tamaño máximo por defecto
definiendo la variable global. Sin embargo, vale la pena tener en cuenta que analizar respuestas
muy grandes puede desperdiciar ciclos de CPU, especialmente cuando se usan expresiones regulares,
y que siempre es mejor centrar las comprobaciones en recursos más pequeños.

En un conjunto de reglas http-check, la última regla expect puede ser implícita. Si no se
especifica ninguna regla expect después del último "http-check send", se define una regla expect
implícita que coincide con los códigos de estado 2xx o 3xx. Esto significa que esta regla también
se define si no hay ninguna regla "http-check", cuando solo está definido "option httpchk".

Por último, si "http-check expect" se combina con "http-check disable-on-404", este último tiene
precedencia cuando el servidor responde con 404.

Ejemplos:

```shell
# only accept status 200 as valid
http-check expect status 200,201,300-310

# be sure a sessid coookie is set
http-check expect hdr name "set-cookie" value -m beg "sessid="

# consider SQL errors as errors
http-check expect ! string SQL\ Error

# consider status 5xx only as errors
http-check expect ! rstatus ^5

# check that we have a correct hexadecimal tag before /html
http-check expect rstring <!--tag:[0-9a-f]*--></html>
```

Ver también: "option httpchk", "http-check connect", "http-check disable-on-404" y "http-check send".

<a id="entry-4-2-http-check-send"></a>

**`http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]`**

```haproxy
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
```

Añade una posible lista de cabeceras y/o un cuerpo a la solicitud enviada durante las comprobaciones
de estado HTTP.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje que se informará si falla la evaluación de la regla.

meth <method>  es el método HTTP opcional usado con las solicitudes. Cuando
               no se establece, se usa el método "OPTIONS", ya que
               generalmente requiere poco procesamiento en el servidor y
               es fácil de filtrar de los registros. Puede usarse
               cualquier método, aunque no se recomienda inventar métodos
               no estándar.

uri <uri>      es opcional y establece el URI referenciado en las
               solicitudes HTTP a la cadena <uri>. Por defecto es "/",
               accesible por defecto en casi cualquier servidor, pero
               puede cambiarse a cualquier otro URI. Se permiten cadenas
               de consulta.

uri-lf <fmt>   es opcional y establece el URI referenciado en las
               solicitudes HTTP usando el formato de registro
               personalizado <fmt> (ver sección 8.2.6). Por defecto es
               "/", accesible por defecto en casi cualquier servidor,
               pero puede cambiarse a cualquier otro URI. Se permiten
               cadenas de consulta.

ver <version>  es la cadena opcional de versión HTTP. Por defecto es
               "HTTP/1.0", pero algunos servidores pueden comportarse de
               forma incorrecta en HTTP 1.0, así que cambiarla a HTTP/1.1
               puede ayudar a veces. Ten en cuenta que el campo Host es
               obligatorio en HTTP/1.1; usa el argumento "hdr" para
               añadirlo.

hdr <name> <fmt>  añade la cabecera HTTP cuyo nombre se especifica en
                  <name> y cuyo valor lo define <fmt>, que sigue las
                  reglas de formato de registro personalizado descritas
                  en la sección 8.2.6.

body <string>  añade a la solicitud enviada durante las comprobaciones de
               estado HTTP el cuerpo definido por <string>. Si se define,
               la cabecera "Content-Length" se añade así automáticamente
               a la solicitud.

body-lf <fmt>  añade a la solicitud enviada durante las comprobaciones de
               estado HTTP el cuerpo definido por el formato de registro
               personalizado <fmt> (ver sección 8.2.6). Si se define, la
               cabecera "Content-Length" se añade así automáticamente a
               la solicitud.
```

Además de la línea de solicitud definida por la directiva "option httpchk", esta es la forma válida de
añadir algunas cabeceras y, opcionalmente, un cuerpo a la solicitud enviada durante las comprobaciones
de estado HTTP. Si se define un cuerpo, la cabecera "Content-Length" asociada se añade automáticamente.
Por lo tanto, esta cabecera o la cabecera "Transfer-encoding" no deberían estar presentes en la
solicitud proporcionada por "http-check send". Si lo están, se ignorarán. El truco antiguo que
consistía en añadir cabeceras después de la cadena de versión en la línea "option httpchk" está ahora
obsoleto.

Además, "http-check send" no soporta HTTP keep-alive. Ten en cuenta que se añadirá automáticamente una
cabecera "Connection: close", a menos que una cabecera Connection ya haya sido configurada mediante
una entrada hdr.

Ten en cuenta que la cabecera Host y la autoridad de la solicitud, cuando ambas están definidas, se
sincronizan automáticamente. Esto significa que, cuando se envía la solicitud HTTP, al insertarse un
Host en la solicitud, la autoridad de la solicitud se actualiza en consecuencia. Así que no te
sorprendas si el valor de la cabecera Host sobrescribe la autoridad de la solicitud configurada.

Ten en cuenta también que, por ahora, no se añade automáticamente ninguna cabecera Host en las
solicitudes HTTP/1.1 o superiores. Deberías añadirla explícitamente.

Ver también: "option httpchk", "http-check send-state" y "http-check expect".

<a id="entry-4-2-http-check-send-state"></a>

**`http-check send-state`**

```haproxy
http-check send-state
```

Activa la emisión de una cabecera de estado con las comprobaciones de estado HTTP

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando se establece esta opción, HAProxy enviará sistemáticamente una cabecera especial
"X-Haproxy-Server-State" con una lista de parámetros que indican a cada servidor cómo los ve HAProxy.
Esto puede usarse, por ejemplo, cuando se manipula un servidor sin acceso a HAProxy y el operador
necesita saber si HAProxy todavía lo ve activo o no, o si el servidor es el último de una granja.

La cabecera se compone de campos delimitados por punto y coma, el primero de los cuales es una palabra
("UP", "DOWN", "NOLB"), posiblemente seguida de un número de comprobaciones válidas sobre el total
antes de la transición, tal y como aparece en la interfaz de estadísticas. Las cabeceras siguientes
tienen la forma "`<variable>`=`<value>`", indicando, sin un orden específico, algunos valores
disponibles en la interfaz de estadísticas: - una variable "address", que contiene la dirección del
servidor del backend. Esto corresponde al campo `<address>` de la declaración del servidor. Para los
sockets de dominio unix, leerá "unix".

    - una variable "port", que contiene el puerto del servidor del backend. Esto
      corresponde al campo `<port>` de la declaración del servidor. Para los
      sockets de dominio unix, leerá "unix".

    - una variable "name", que contiene el nombre del backend seguido de una barra
      ("/") y el nombre del servidor. Esto puede usarse cuando un servidor se
      comprueba en varios backends.

    - una variable "node" que contiene el nombre del nodo HAProxy, tal como se
      establece en la variable global "node", o el nombre de host del sistema si
      no se especifica.

    - una variable "weight" que indica el peso del servidor, una barra ("/") y el
      peso total de la granja (contando solo los servidores utilizables). Esto
      ayuda a saber si hay otros servidores disponibles para atender la carga
      cuando este falla.

    - una variable "scur" que indica el número actual de conexiones simultáneas
      en el servidor, seguida de una barra ("/") y el número total de
      conexiones en todos los servidores del mismo backend.

    - una variable "qcur" que indica el número actual de solicitudes en la cola
      del servidor.

Ejemplo de una cabecera recibida por el servidor de aplicaciones:

```shell
>>>  X-Haproxy-Server-State: UP 2/3; name=bck/srv2; node=lb1; weight=1/2; \
       scur=13/22; qcur=0
```

Ver también: "option httpchk", "http-check disable-on-404" y "http-check send".

<a id="entry-4-2-http-check-set-var"></a>

**`http-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Esta operación establece el contenido de una variable. La variable se declara en línea.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<var-name>   El nombre de la variable. Solo pueden usarse los ámbitos
             "proc", "sess" y "check". Ver la sección 2.8 sobre variables
             para más detalles.

 <cond>      Un conjunto de condiciones que deben cumplirse todas para que
             la variable se establezca realmente (tales como
             "ifnotempty", "ifgt"...). Ver la descripción del
             convertidor set-var para la lista completa de condiciones
             posibles.

 <expr>      Es una expresión sample-fetch potencialmente seguida de
             convertidores.

 <fmt>       Es el valor expresado usando el formato de registro
             personalizado (ver Formato de registro personalizado en la sección 8.2.6).
```

Ejemplos:

```text
http-check set-var(check.port) int(1234)
http-check set-var-fmt(check.port) "name=%H"

```

<a id="entry-4-2-http-check-unset-var"></a>

**`http-check unset-var(<var-name>)`**

```haproxy
http-check unset-var(<var-name>)
```

Libera una referencia a una variable dentro de su ámbito.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<var-name>   El nombre de la variable. Solo pueden usarse los ámbitos
             "proc", "sess" y "check". Ver la sección 2.8 sobre variables
             para más detalles.
```

Ejemplos:

```text
http-check unset-var(check.port)

```

<a id="entry-4-2-http-error-status"></a>

**`http-error status <code> [content-type <type>]`**

```haproxy
http-error status <code> [content-type <type>]
           [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

               file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
           [ hdr `<name>` `<fmt>` ]*

Define un mensaje de error personalizado para usar en lugar de los errores generados por HAProxy.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
status <code>        es el código de estado HTTP. Debe especificarse.
                     Actualmente, HAProxy es capaz de generar los códigos
                     200, 400, 401, 403, 404, 405, 407, 408, 410, 413,
                     414, 425, 429, 431, 500, 501, 502, 503 y 504.

content-type <type>  es el tipo de contenido de la respuesta, por ejemplo
                     "text/plain". Este parámetro se ignora y debería
                     omitirse cuando se configura un errorfile o cuando
                     el cuerpo está vacío. De lo contrario, debe
                     definirse.

default-errorfiles   Restablece el mensaje de error definido previamente
                     para el proxy actual para el estado <code>. Si se usa
                     en un backend, se usa el mensaje de error del
                     frontend, si está definido. Si se usa en un frontend,
                     se usa el mensaje de error por defecto.

errorfile <file>     designa un archivo que contiene la respuesta HTTP
                     completa. Se recomienda seguir la práctica común de
                     añadir ".http" al nombre del archivo para que la
                     gente no confunda la respuesta con páginas de error
                     HTML, y usar rutas absolutas, ya que los archivos se
                     leen antes de realizar cualquier chroot.

errorfiles <name>    designa la sección http-errors que se usará para
                     importar el mensaje de error con el código de estado
                     <code>. Si no se encuentra tal mensaje, se
                     consideran los mensajes de error del proxy.

file <file>          especifica el archivo que se usará como cuerpo de la
                     respuesta. Si el archivo no está vacío, su
                     content-type debe establecerse como argumento de
                     "content-type"; de lo contrario, se ignora cualquier
                     argumento "content-type". <file> se considera una
                     cadena en bruto.

string <str>         especifica la cadena en bruto que se usará como cuerpo
                     de la respuesta. El content-type debe establecerse
                     siempre como argumento de "content-type".

lf-file <file>       especifica el archivo que se usará como cuerpo de la
                     respuesta. Si el archivo no está vacío, su
                     content-type debe establecerse como argumento de
                     "content-type"; de lo contrario, se ignora cualquier
                     argumento "content-type". <file> se evalúa como un
                     formato de registro personalizado (ver sección
                     8.2.6).

lf-string <str>      especifica la cadena log-format que se usará como
                     cuerpo de la respuesta. El content-type debe
                     establecerse siempre como argumento de
                     "content-type".

hdr <name> <fmt>     añade a la respuesta la cabecera HTTP cuyo nombre se
                     especifica en <name> y cuyo valor lo define <fmt>,
                     que sigue las reglas de formato de registro
                     personalizado (ver sección 8.2.6). Este parámetro se
                     ignora si se usa un errorfile.
```

Esta directiva puede usarse en lugar de "errorfile" para definir un mensaje de error personalizado.
Igual que la directiva "errorfile", se usa para los errores detectados y devueltos por HAProxy. Si se
define un errorfile, se analiza cuando HAProxy arranca y debe ser válido según los estándares HTTP.
La respuesta generada no debe superar el tamaño de búfer configurado (BUFFSIZE); de lo contrario, se
devolverá un error interno. Finalmente, si consideras usar algunas reglas http-after-response para
reescribir estos errores, el espacio de búfer reservado debería estar disponible (consulta
"tune.maxrewrite").

Los archivos se leen al mismo tiempo que la configuración y se mantienen en memoria. Por esta razón,
los errores siguen devolviéndose incluso cuando el proceso está bajo chroot, y no se considera ningún
cambio de archivo mientras el proceso está en ejecución.

Nota: los errores 400/408/500 emitidos en una etapa temprana del análisis de la solicitud los gestiona
el multiplexor en un nivel inferior. En este nivel no se soporta ningún formato personalizado. Por lo
tanto, solo se soportan los mensajes de error estáticos, definidos con la directiva "errorfile". Sin
embargo, esta limitación solo existe durante el análisis de las cabeceras de la solicitud o entre dos
transacciones.

Ver también: "errorfile", "errorfiles", "errorloc", "errorloc302", "errorloc303" y la [sección 12.4](/es/haproxy/other-sections/#section-12-4) acerca de
http-errors.

<a id="entry-4-2-http-request"></a>

**`http-request <action> [options...] [ { if | unless } <condition> ]`**

```haproxy
http-request <action> [options...] [ { if | unless } <condition> ]
```

Control de acceso para solicitudes de capa 7

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

La instrucción http-request define un conjunto de reglas que se aplican al procesamiento de capa 7.
Las reglas se evalúan en su orden de declaración cuando se aplican en una sección frontend, listen o
backend. Cualquier regla puede ir seguida opcionalmente de una condición basada en ACL, en cuyo caso
solo se evaluará si la condición se evalúa como verdadera.

La condición se evalúa justo antes de que se ejecute la acción, y la acción se realiza exactamente una
vez. Así, no hay problema si una acción cambia un elemento que se comprueba como parte de la
condición. Esto también significa que varias acciones pueden depender de la misma condición, de modo
que la primera acción que cambie la evaluación de la condición basta para desactivar implícitamente
las acciones restantes. Esto se usa, por ejemplo, al intentar asignar un valor a una variable desde
diversas fuentes cuando está vacía. No hay límite en el número de instrucciones "http-request" por
instancia.

La primera palabra clave después de "http-request" en la sintaxis es la acción de la regla, seguida
opcionalmente de un número variable de argumentos para la acción. Las acciones soportadas y sus
sintaxis respectivas se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3) "Acciones" (busca las acciones que
marcan "HTTP Req").

Esta directiva solo está disponible en secciones defaults con nombre, no en anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección de proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con capacidad de
frontend y por proxies con capacidad de backend. Esto significa que una sección listen no puede usar
una sección defaults que defina tales reglas.

Ejemplo:

```text
acl nagios src 192.168.129.3
acl local_net src 192.168.0.0/16
acl auth_ok http_auth(L1)

http-request allow if nagios
http-request allow if local_net auth_ok
http-request auth realm Gimme if local_net auth_ok
http-request deny
```

Ejemplo:

```text
acl key req.hdr(X-Add-Acl-Key) -m found
acl add path /addacl
acl del path /delacl

acl myhost hdr(Host) -f myhost.lst

http-request add-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key add
http-request del-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key del
```

Ejemplo:

```text
acl value  req.hdr(X-Value) -m found
acl setmap path /setmap
acl delmap path /delmap

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-request set-map(map.lst) %[src] %[req.hdr(X-Value)] if setmap value
http-request del-map(map.lst) %[src]                     if delmap
```

Ver también: "stats http-request", la [sección 12.2](/es/haproxy/other-sections/#section-12-2) acerca de las listas de usuarios y la [sección 7](/es/haproxy/acls-and-samples/) acerca del uso de ACL.

<a id="entry-4-2-http-response"></a>

**`http-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-response <action> <options...> [ { if | unless } <condition> ]
```

Control de acceso para respuestas de capa 7

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

La instrucción http-response define un conjunto de reglas que se aplican al procesamiento de capa 7.
Las reglas se evalúan en su orden de declaración cuando se aplican en una sección frontend, listen o
backend. Como estas reglas se aplican a las respuestas, primero se aplican las reglas del backend,
seguidas de las del frontend. Cualquier regla puede ir seguida opcionalmente de una condición basada
en ACL, en cuyo caso solo se evaluará si la condición se evalúa como verdadera.

La condición se evalúa justo antes de que se ejecute la acción, y la acción se realiza exactamente una
vez. Así, no hay problema si una acción cambia un elemento que se comprueba como parte de la
condición. Esto también significa que varias acciones pueden depender de la misma condición, de modo
que la primera acción que cambie la evaluación de la condición basta para desactivar implícitamente
las acciones restantes. Esto se usa, por ejemplo, al intentar asignar un valor a una variable desde
diversas fuentes cuando está vacía. No hay límite en el número de instrucciones "http-response" por
instancia.

La primera palabra clave después de "http-response" en la sintaxis es la acción de la regla, seguida
opcionalmente de un número variable de argumentos para la acción. Las acciones soportadas y sus
sintaxis respectivas se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3) "Acciones" (busca las acciones que
marcan "HTTP Res").

Esta directiva solo está disponible en secciones defaults con nombre, no en anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección de proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con capacidad de
frontend y por proxies con capacidad de backend. Esto significa que una sección listen no puede usar
una sección defaults que defina tales reglas.

Ejemplo:

```text
acl key_acl res.hdr(X-Acl-Key) -m found

acl myhost hdr(Host) -f myhost.lst

http-response add-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
http-response del-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
```

Ejemplo:

```text
acl value  res.hdr(X-Value) -m found

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-response set-map(map.lst) %[src] %[res.hdr(X-Value)] if value
http-response del-map(map.lst) %[src]                     if ! value
```

Ver también: "http-request", la [sección 12.2](/es/haproxy/other-sections/#section-12-2) acerca de las listas de usuarios y la [sección 7](/es/haproxy/acls-and-samples/) acerca del uso de ACL.

<a id="entry-4-2-http-reuse"></a>

**`http-reuse { never | safe | aggressive | always }`**

```haproxy
http-reuse { never | safe | aggressive | always }
```

Declara cómo se pueden compartir entre solicitudes las conexiones HTTP inactivas

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Para evitar el coste de establecer nuevas conexiones a los servidores del backend por cada solicitud
HTTP, HAProxy intenta mantener abiertas dichas conexiones inactivas después de usarlas. Estas
conexiones son específicas de un servidor, se almacenan en una lista llamada pool y se agrupan por un
conjunto de propiedades clave comunes. Las solicitudes HTTP posteriores provocarán una búsqueda de una
conexión compatible que comparta propiedades idénticas en el pool asociado y harán que esa conexión se
reutilice en lugar de establecer una nueva.

Un límite en el número de conexiones inactivas que mantener en un servidor puede especificarse mediante
la palabra clave de servidor "pool-max-conn". Las conexiones sin uso se purgan periódicamente según el
intervalo "pool-purge-delay".

Las siguientes propiedades de conexión se usan para determinar si una conexión inactiva es elegible
para reutilizarse en una solicitud dada:

- direcciones de origen y destino
- protocolo proxy
- opciones de socket TOS y mark
- nombre de conexión, determinado por el resultado de la evaluación de la expresión "pool-conn-name"
  si está presente, o de lo contrario por la expresión "sni", cuyo valor por defecto es
  "req.hdr(host),field(1,:)", es decir, usa el campo de cabecera "Host" de la solicitud entrante sin
  los dos puntos ni el número de puerto.

En algunas ocasiones, la búsqueda o reutilización de la conexión no se realiza debido a restricciones
adicionales. Esto lo determina la estrategia de reutilización especificada mediante el argumento de la
palabra clave:

    - "never" : las conexiones inactivas nunca se comparten entre sesiones. Este
                 modo puede imponerse para cancelar una estrategia diferente
                 heredada de una sección defaults o para resolver problemas. Por
                 ejemplo, si una aplicación antigua y defectuosa considera que
                 varias solicitudes sobre la misma conexión provienen del mismo
                 cliente y no es posible arreglar la aplicación, puede ser
                 deseable desactivar el compartir conexiones en un único backend.
                 Un ejemplo de tal aplicación podría ser un HAProxy antiguo que
                 usa inserción de cookies en modo túnel y no comprueba ninguna
                 solicitud más allá de la primera.

    - "safe"  : esta es la estrategia por defecto y la recomendada. La primera
                 solicitud de una sesión siempre se envía por su propia conexión,
                 y solo las solicitudes posteriores pueden repartirse por otras
                 conexiones existentes. Esto garantiza que, en caso de que el
                 servidor cierre la conexión mientras se envía la solicitud, el
                 navegador pueda decidir reintentarla en silencio. Como es
                 exactamente equivalente al keep-alive normal, no debería haber
                 efectos secundarios. También existe una gestión especial para
                 las conexiones que usan protocolos sujetos al bloqueo de cabeza
                 de línea (backend con h2 o fcgi). En este caso, cuando se
                 procesa al menos un flujo, la conexión usada se reserva para
                 gestionar flujos de la misma sesión. Cuando ya no se procesan
                 flujos, la conexión se libera y puede reutilizarse.

    - "aggressive": este modo puede ser útil en entornos de servicios web donde
                 no se conocen necesariamente todos los servidores y donde
                 sería apreciable entregar la mayoría de las primeras solicitudes
                 sobre conexiones existentes. En este caso, las primeras
                 solicitudes solo se entregan por conexiones existentes que
                 hayan sido reutilizadas al menos una vez, lo que demuestra que
                 el servidor soporta correctamente la reutilización de
                 conexiones. Solo debería usarse cuando se está seguro de que el
                 cliente puede reintentar de vez en cuando una solicitud fallida
                 y donde el beneficio de la reutilización agresiva de conexiones
                 supera significativamente los inconvenientes de fallos de
                 conexión raros.

    - "always": este modo solo se recomienda cuando se sabe que la ruta al
                 servidor nunca rompe rápidamente las conexiones existentes tras
                 liberarlas. Permite que la primera solicitud de una sesión se
                 envíe a una conexión existente. Esto puede proporcionar un
                 aumento significativo de rendimiento respecto a la estrategia
                 "safe" cuando el backend es una granja de cachés, ya que tales
                 componentes suelen mostrar un comportamiento consistente y se
                 beneficiarán del compartir conexiones. Se recomienda que el
                 timeout "http-keep-alive" se mantenga bajo en este modo para
                 que ninguna conexión muerta permanezca utilizable. En la
                 mayoría de los casos, esto llevará a las mismas ganancias de
                 rendimiento que "aggressive" pero con más riesgos. Solo debería
                 usarse cuando mejora la situación respecto a "aggressive".

Ten en cuenta también que las conexiones con ciertos esquemas de autenticación defectuosos (que
dependen de la conexión), como NTLM, se marcan como privadas si es posible y nunca se comparten. Sin
embargo, este no será el caso cuando se usa un protocolo con capacidades de multiplexación y un valor
de nivel del modo de reutilización mayor que la estrategia por defecto "safe", ya que en este caso
nada impide que la conexión ya esté compartida.

Las reglas para decidir mantener abierta una conexión inactiva o cerrarla tras el procesamiento también
se rigen por "tune.pool-low-fd-ratio" (por defecto: 20%) y "tune.pool-high-fd-ratio" (por defecto:
25%). Corresponden al porcentaje de descriptores de archivo totales gastados en conexiones inactivas
por encima del cual haproxy, respectivamente, se abstendrá de mantener una conexión abierta tras una
respuesta, o matará activamente conexiones inactivas. Algunas configuraciones que usan una proporción
muy alta de conexiones inactivas, ya sea por un "maxconn" global demasiado bajo, o debido a mucho
tráfico HTTP/2 o HTTP/3 en el frontend (pocas conexiones) pero conexiones HTTP/1 en el backend, pueden
observar una tasa de reutilización menor porque se mantienen abiertas muy pocas conexiones. En este
caso puede ser deseable ajustar tales umbrales o simplemente aumentar el valor global de "maxconn".

En algunos casos raros, cuando el nombre de host se usa para distinguir conexiones TLS salientes (p.
ej., un proxy de reenvío), donde la mayoría de las solicitudes apuntan a hosts diferentes, la tasa de
reutilización será muy baja, y la expulsión automática de conexiones poco usadas entrará en acción
antes de que las conexiones tengan ocasión de reutilizarse, porque el mecanismo mide continuamente el
número medio de conexiones necesarias para prestar el servicio sin agotar recursos. En tales
situaciones, establecer "pool-low-conn" a un valor cercano al número medio esperado de conexiones
inactivas puede ayudar a conservar más conexiones animando a los hilos a establecer las suyas propias
en lugar de intentar tomar las de otros hilos y reducir el pool de conexiones disponibles.

Si un servidor alojado localmente usa un único certificado (con varios nombres de host o comodines) y
opera varios sitios, puede ser más eficaz usar simplemente "no-sni-auto" en la línea "server" para
evitar reservar una conexión a un único nombre de Host. Esto aumentará significativamente la tasa de
reutilización. Sin embargo, algunos servidores podrían realizar comprobaciones excesivas entre Host y
SNI, rechazando solicitudes posteriores, por lo que esta opción requiere una validación preliminar.
El comportamiento por defecto ("sni-auto") es ser seguro incluso con tales servidores.

Cuando los grupos de hilos están explícitamente habilitados, es importante entender que las conexiones
inactivas solo son utilizables entre hilos de un mismo grupo. Así, puede ocurrir que una carga
desigual entre grupos provoque la necesidad de más conexiones inactivas, causando una tasa de
reutilización menor. Entonces puede aplicarse la misma solución (aumentar el "maxconn" global o
aumentar las proporciones del pool).

Ver también: "option http-keep-alive", "pool-conn-name", "pool-max-conn", "pool-purge-delay", "server
maxconn", "sni", "thread-groups", "tune.pool-high-fd-ratio", "tune.pool-low-fd-ratio"

<a id="entry-4-2-http-send-name-header"></a>

**`http-send-name-header [<header>]`**

```haproxy
http-send-name-header [<header>]
```

Añade el nombre del servidor a una solicitud. Usa la cadena de cabecera dada por `<header>`

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<header>  La cadena de cabecera que se usará para enviar el nombre del servidor
```

La instrucción "http-send-name-header" hace que el campo de cabecera llamado `<header>` se establezca
al nombre del servidor de destino en el momento en que la solicitud está a punto de enviarse por el
cable. Cualquier aparición existente de esta cabecera se elimina. En los reintentos y reenvíos, el
campo de cabecera se actualiza para reflejar siempre el servidor al que se está intentando conectar.
Dado que esta cabecera se modifica muy tarde en el establecimiento de la conexión, puede tener
efectos inesperados en cabeceras ya modificadas. Por ejemplo, usarla con cabeceras de nivel de
transporte como connection, content-length, transfer-encoding, etc., probablemente dará como
resultado el envío al servidor de solicitudes no válidas. Es por eso que los siguientes nombres de
cabecera están prohibidos: host, content-length, transfer-encoding y connection.

Ver también: "server"

<a id="entry-4-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

Asigna un ID persistente a un proxy.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Argumentos: ninguno

Establece un ID persistente para el proxy. Este ID debe ser único y positivo. Se asignará
automáticamente un ID sin usar si no se establece. Debido a un comportamiento histórico, el valor 1
no se usa a menos que se establezca explícitamente. Así, el valor más bajo asignado automáticamente
será 2. Este ID actualmente solo se devuelve en las estadísticas.

<a id="entry-4-2-ignore-persist"></a>

**`ignore-persist { if | unless } <condition>`**

```haproxy
ignore-persist { if | unless } <condition>
```

Declara una condición para ignorar la persistencia

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Por defecto, cuando la persistencia por cookie está habilitada, todas las solicitudes que contienen la
cookie son incondicionalmente persistentes (asumiendo que el servidor de destino está activo y en
ejecución).

La instrucción "ignore-persist" permite declarar diversas condiciones basadas en ACL que, cuando se
cumplen, harán que una solicitud ignore la persistencia. Esto a veces es útil para balancear
solicitudes de archivos estáticos, que a menudo no requieren persistencia. También puede usarse para
desactivar por completo la persistencia para un User-Agent específico (por ejemplo, algunos bots
rastreadores web).

La persistencia se ignora cuando se cumple una condición "if", o salvo que se cumpla una condición
"unless".

Ejemplo:

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
ignore-persist  if url_static
```

Ver también: "force-persist", "cookie" y la [sección 7](/es/haproxy/acls-and-samples/) acerca del uso de ACL.

<a id="entry-4-2-load-server-state-from-file"></a>

**`load-server-state-from-file { global | local | none }`**

```haproxy
load-server-state-from-file { global | local | none }
```

Permite la recarga sin interrupciones de HAProxy

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Esta directiva indica a HAProxy un archivo donde se ha guardado el estado de los servidores del
proceso en ejecución anterior. De este modo, al arrancar, antes de gestionar el tráfico, el nuevo
proceso puede aplicar los estados antiguos a los servidores exactamente como si no hubiera ocurrido
ninguna recarga. El propósito de la directiva "load-server-state-from-file" es decirle a HAProxy qué
archivo usar. Por ahora, solo existen 2 argumentos para impedir la carga del estado o para cargar
estados desde un archivo que contiene todos los backends y servidores. El archivo de estado puede
generarse ejecutando el comando "show servers state" sobre el socket de estadísticas y redirigiendo
la salida.

El formato del archivo está versionado y es muy específico. Para entenderlo, lee la documentación del
comando "show servers state" (capítulo 9.3 de la Guía de Gestión).

Argumentos:

```text
global     carga el contenido del archivo apuntado por la directiva global
           llamada "server-state-file".

local      carga el contenido del archivo apuntado por la directiva
           "server-state-file-name" si está establecida. Si no lo está,
           se usa el nombre del backend como nombre de archivo.

none       no carga ningún estado para este backend
```

Notas: - la dirección IP del servidor se conserva a través de las recargas por defecto, pero el orden
puede cambiarse gracias al ajuste "init-addr" del servidor. Esto significa que un cambio de dirección
IP realizado en la CLI en tiempo de ejecución se conservará, y que cualquier cambio en el resolutor
local (p. ej., /etc/hosts) posiblemente no tenga ningún efecto si el archivo de estado está en uso.

    - el peso del servidor se aplica del proceso en ejecución anterior a menos que
      haya cambiado entre los archivos de configuración anterior y nuevo.

Ejemplo: Configuración mínima

      global
       stats socket /tmp/socket
       server-state-file /tmp/server_state

      defaults
       load-server-state-from-file global

      backend bk
       server s1 127.0.0.1:22 check weight 11
       server s2 127.0.0.1:22 check weight 12

Luego se puede ejecutar:

```text
socat /tmp/socket - <<< "show servers state" > /tmp/server_state
```

El contenido del archivo /tmp/server_state sería algo así:

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

Ejemplo: Configuración mínima

    global
     stats socket /tmp/socket
     server-state-base /etc/haproxy/states

    defaults
     load-server-state-from-file local

    backend bk
     server s1 127.0.0.1:22 check weight 11
     server s2 127.0.0.1:22 check weight 12

Luego se puede ejecutar:

```text
socat /tmp/socket - <<< "show servers state bk" > /etc/haproxy/states/bk
```

El contenido del archivo /etc/haproxy/states/bk sería algo así:

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

Ver también: "server-state-file", "server-state-file-name" y "show servers state"

<a id="entry-4-2-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [<level> [<minlevel>]]
no log
```

Habilita el registro de eventos y tráfico por instancia.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Prefijo:

```text
no         debe usarse cuando la lista de loggers debe vaciarse. Por
           ejemplo, si no se quiere heredar la lista de loggers por
           defecto. Este prefijo no admite argumentos.
```

Argumentos:

```text
global     debe usarse cuando los parámetros de registro de la instancia
           son los mismos que los globales. Este es el uso más común.
           "global" sustituye todos los argumentos de log por los de las
           entradas log que se encuentren en la sección "global". Solo
           puede usarse una instrucción "log global" por instancia, y
           esta forma no admite ningún otro parámetro.

<target>   indica dónde enviar los registros. Toma el mismo formato que
           los logs de la sección "global", y puede ser uno de:

           - Una dirección IPv4 seguida opcionalmente de dos puntos (':')
             y un puerto UDP. Si no se especifica puerto, se usa 514 por
             defecto (el puerto syslog estándar).

           - Una dirección IPv6 seguida de dos puntos (':') y
             opcionalmente un puerto UDP. Si no se especifica puerto, se
             usa 514 por defecto (el puerto syslog estándar).

           - Una ruta del sistema de archivos a un socket de dominio
             UNIX, teniendo en cuenta las consideraciones sobre chroot
             (asegúrate de que la ruta es accesible dentro del chroot) y
             uid/gid (asegúrate de que la ruta tiene permisos de
             escritura adecuados).

           - Un número de descriptor de archivo con la forma "fd@<number>",
             que puede apuntar a una tubería, terminal o socket. En este
             caso se usan registros sin búfer y se realiza una llamada
             writev() por registro. Esto es algo costoso pero aceptable
             para la mayoría de cargas de trabajo. Los mensajes enviados
             de esta forma no se truncarán pero pueden descartarse, en
             cuyo caso el contador DroppedLogs se incrementará. La
             llamada writev() es atómica incluso en tuberías para
             mensajes de hasta el tamaño PIPE_BUF, que POSIX recomienda
             que sea al menos 512 y que es 4096 bytes en la mayoría de
             sistemas operativos modernos. Cualquier mensaje mayor puede
             intercalarse con mensajes de otros procesos.
             Excepcionalmente, con fines de depuración, el descriptor de
             archivo también puede dirigirse a un archivo, pero hacerlo
             ralentizará significativamente HAProxy, ya que las llamadas
             no bloqueantes se ignorarán. Además, no habrá forma de
             purgar ni rotar este archivo sin reiniciar el proceso. Ten
             en cuenta que el formato syslog configurado se conserva, por
             lo que la salida es apta para su uso con un servidor syslog
             TCP. Ver también los formatos "short" y "raw" de abajo.

           - "stdout" / "stderr", que son respectivamente alias de
             "fd@1" y "fd@2"; ver arriba.

           - Un búfer de anillo con la forma "ring@<name>", que
             corresponderá a un búfer de anillo en memoria accesible por
             la CLI con el comando "show events", que además listará los
             anillos existentes y sus tamaños. Estos búferes se pierden
             en una recarga o un reinicio, pero usados como complemento
             pueden ayudar en el diagnóstico al tener los registros
             disponibles al instante. Ver la sección 12.5 sobre los
             anillos (rings).

           - Un backend de registro con la forma "backend@<name>", que
             enviará los mensajes de registro al backend de registro
             correspondiente, responsable de enviar el mensaje al
             servidor adecuado según la configuración de balanceo del
             backend. Un backend de registro es una sección backend con
             "mode log" establecido (ver "mode" para más información).

           - Un prefijo explícito de dirección de flujo como "tcp@",
             "tcp6@", "tcp4@" o "uxst@" asignará un búfer de anillo
             implícito con un servidor de reenvío de flujo dirigido a la
             dirección indicada.

           Puede que quieras hacer referencia a algunas variables de
           entorno en el parámetro de dirección; ver la sección 2.3 sobre
           variables de entorno.

<length>   es una longitud máxima de línea opcional. Las líneas de registro
           mayores que este valor se truncarán antes de enviarse. La
           razón es que los servidores syslog se comportan de forma
           distinta con la longitud de las líneas de registro. Todos los
           servidores soportan el valor por defecto de 1024, pero
           algunos simplemente descartan las líneas mayores mientras que
           otros sí las registran. Si un servidor soporta líneas largas,
           puede tener sentido establecer aquí este valor para evitar
           truncar líneas largas. Del mismo modo, si un servidor
           descarta las líneas largas, es preferible truncarlas antes de
           enviarlas. Los valores aceptados van de 80 a 65535 inclusive.
           El valor por defecto de 1024 generalmente sirve para todos los
           usos estándar. Algunos casos específicos de capturas largas o
           de registros con formato JSON pueden requerir valores mayores.
           También puedes necesitar aumentar "tune.http.logurilen" si tus
           URI de solicitud se truncan.

<ranges>   Una lista de rangos separados por comas para identificar los
           registros que se van a muestrear. Se usa para repartir la
           carga de los registros que se envían al servidor de
           registros. Los límites de los rangos no pueden ser nulos. Se
           numeran a partir de 1. El tamaño o periodo (en número de
           registros) de la muestra debe establecerse con el parámetro
           <sample_size>.

<sample_size>
           El tamaño de la muestra en número de registros que se
           consideran al repartir sus cargas de registro. Se usa para
           repartir la carga de los registros que se envían al servidor
           syslog. Este tamaño debe ser mayor o igual que el máximo de
           los límites superiores de los rangos.
           (ver también el parámetro <ranges>).

<format> es el formato de registro usado al generar los mensajes syslog.
         Puede ser uno de los siguientes:

  local     Análogo al formato de mensaje syslog rfc3164 excepto en que se
            elimina el campo de nombre de host. Es el valor por defecto.
            Nota: la opción "log-send-hostname" cambia el defecto a
            rfc3164.

  rfc3164   El formato de mensaje syslog RFC3164.
            (https://tools.ietf.org/html/rfc3164)

  rfc5424   El formato de mensaje syslog RFC5424.
            (https://tools.ietf.org/html/rfc5424)

  priority  Un mensaje que contiene solo un nivel más la facility syslog
            entre corchetes angulares como '<63>', seguido del texto. Se
            omiten el PID, la fecha, la hora, el nombre del proceso y el
            nombre del sistema. Está pensado para usarse con un servidor
            de registros local.

  short     Un mensaje que contiene solo un nivel entre corchetes
            angulares como '<3>', seguido del texto. Se omiten el PID,
            la fecha, la hora, el nombre del proceso y el nombre del
            sistema. Está pensado para usarse con un servidor de
            registros local. Este formato es compatible con lo que
            consume el logger de systemd.

  timed     Un mensaje que contiene solo un nivel entre corchetes
            angulares como '<3>', seguido de la fecha ISO y del texto.
            Se omiten el PID, el nombre del proceso y el nombre del
            sistema. Está pensado para usarse con un servidor de
            registros local.

  iso       Un mensaje que contiene solo la fecha ISO, seguida del texto.
            Se omiten el PID, el nombre del proceso y el nombre del
            sistema. Está pensado para usarse con un servidor de
            registros local.

  raw       Un mensaje que contiene solo el texto. Se omiten el nivel, el
            PID, la fecha, la hora, el nombre del proceso y el nombre del
            sistema. Está pensado para usarse en contenedores o durante
            el desarrollo, donde la gravedad depende solo del descriptor
            de archivo usado (stdout/stderr).

<prof>     nombre de la sección opcional "log-profile" que se considerará
           durante el proceso de construcción del registro para
           sustituir algunas opciones de registro. Ver «8.3.5. Perfiles de registro» para más información.

<facility> debe ser una de las 24 facilities syslog estándar:

               kern   user   mail   daemon auth   syslog lpr    news
               uucp   cron   auth2  ftp    ntp    audit  alert  cron2
               local0 local1 local2 local3 local4 local5 local6 local7

           Ten en cuenta que la facility se ignora para los formatos
           "short" y "raw", pero sigue siendo obligatoria como campo
           posicional. Se recomienda usar "daemon" en este caso para
           dejar claro que solo se supone que se use localmente.

<level>    es opcional y puede especificarse para filtrar los mensajes
           salientes. Por defecto, se envían todos los mensajes. Si se
           especifica un nivel, solo se enviarán los mensajes con una
           gravedad al menos tan importante como ese nivel. Puede
           especificarse un nivel mínimo opcional. Si se establece, los
           registros emitidos con un nivel más grave que este se
           limitarán a este nivel. Se usa para evitar enviar mensajes
           "emerg" a todas las terminales con algunas configuraciones
           syslog por defecto. Se conocen ocho niveles:

             emerg  alert  crit   err    warning notice info  debug
```

Es importante tener en mente que es el frontend quien decide qué registrar de una conexión, y que en
caso de conmutación de contenido, las entradas de registro del backend serán ignoradas. Las conexiones
se registran a nivel "info".

Sin embargo, las declaraciones de registro del backend definen cómo y dónde se registrarán los cambios
de estado de los servidores. El nivel "notice" se usará para indicar que un servidor sube, "warning"
se usará para las señales de terminación y la terminación definitiva del servicio, y "alert" se usará
para cuando un servidor baja.

Nota: Según RFC3164, los mensajes se truncan a 1024 bytes antes de emitirse.

Ejemplo:

```text
log global
log stdout format short daemon          # send log to systemd
log stdout format raw daemon            # send everything to stdout
log stderr format raw daemon notice     # send important events to stderr
log 127.0.0.1:514 local0 notice         # only send important events
log tcp@127.0.0.1:514 local0 notice notice  # same but limit output
                                            # level and send in tcp
log "${LOCAL_SYSLOG}:514" local0 notice   # send to local server
```

<a id="entry-4-2-log-format"></a>

**`log-format <fmt>`**

```haproxy
log-format <fmt>
```

Especifica la cadena de formato de registro personalizado que se usará para los registros de tráfico

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Esta directiva especifica la cadena de formato de registro que se usará para todos los registros
resultantes del tráfico que pasa por el frontend que usa esta línea. Si la directiva se usa en una
sección defaults, todos los frontends posteriores usarán el mismo formato de registro. Consulta la
[sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6), que cubre en profundidad la cadena
de formato de registro personalizado.

También puede definirse un log-format específico usado solo en caso de error de conexión; consulta la
opción "error-log-format".

La directiva "log-format" prevalece sobre las directivas anteriores "option tcplog", "log-format",
"option httplog" y "option httpslog".

<a id="entry-4-2-log-format-sd"></a>

**`log-format-sd <fmt>`**

```haproxy
log-format-sd <fmt>
```

Especifica la cadena de formato de registro personalizado usada para producir los datos estructurados
RFC5424

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Esta directiva especifica la cadena de formato de registro de datos estructurados RFC5424 que se
usará para todos los registros resultantes del tráfico que pasa por el frontend que usa esta línea.
Si la directiva se usa en una sección defaults, todos los frontends posteriores usarán el mismo
formato de registro. Consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6),
que cubre en profundidad la cadena de formato de registro.

Consulta <https://tools.ietf.org/html/rfc5424#section-6.3> para más información sobre la parte de datos
estructurados de RFC5424.

Nota: Esta cadena de formato de registro solo se usará para los loggers que tengan el formato de
registro establecido a "rfc5424".

Ejemplo:

```text
log-format-sd [exampleSDID@1234\ bytes=\"%B\"\ status=\"%ST\"]
```

<a id="entry-4-2-log-steps"></a>

**`log-steps <steps>`**

```haproxy
log-steps <steps>
```

Especifica en qué pasos del procesamiento de transacciones deben generarse los registros.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Durante el procesamiento de transacciones tcp/http, haproxy puede producir registros en diferentes
pasos del procesamiento (es decir: accept, connect, request, response, close).

Por defecto, HAProxy emite un único registro por transacción, una vez que todos los elementos usados
en la expresión logformat han podido satisfacerse, lo que significa que en la práctica el registro
suele emitirse al final de la transacción (tras el final de la respuesta para HTTP o el final de la
conexión para TCP), a menos que se use "option logasap".

La directiva "log-steps" permite refinar los instantes precisos en que se emitirán los registros, e
incluso permite emitir múltiples registros para una misma transacción. El valor especial 'all' puede
usarse para habilitar todos los orígenes de registro disponibles, haciendo posible seguir una
transacción desde accept hasta close. También pueden especificarse orígenes de registro individuales
usando sus nombres separados por comas para habilitar selectivamente cuándo deben producirse los
registros.

Los orígenes de registro comunes son: accept, connect, request, response, close.

Ejemplo:

```text
frontend myfront
    option httplog
    log-steps accept,close         #only log accept and close for the txn
```

Los orígenes de registro especificados como "logging steps" (pasos de registro, tales como accept,
close) pueden usarse tal cual en los perfiles de registro (log-profiles, tras la directiva 'on').
Combinar "log-steps" con log-profiles es realmente interesante para tener un control fino sobre los
registros generados automáticamente por haproxy durante el procesamiento de transacciones.

Este ajuste solo es relevante en los frontends; se ignora en los backends.

Ver también: "log-profile"

<a id="entry-4-2-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

Especifica la etiqueta de registro que se usará para todos los registros salientes

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Establece el campo de etiqueta en la cabecera syslog a esta cadena. Por defecto es el log-tag
establecido en la sección global; de lo contrario, el nombre del programa tal como se lanzó desde la
línea de comandos, que normalmente es "HAProxy". A veces puede ser útil diferenciar entre múltiples
procesos en ejecución en el mismo host, o diferenciar instancias de clientes en ejecución en el mismo
proceso. En el backend, los registros sobre servidores subidos/bajados usarán esta etiqueta. Como
consejo, puede ser conveniente establecer un log-tag relacionado con un cliente alojado en una
sección defaults, poner luego en ella todos los frontends y backends de ese cliente, y después
empezar otro cliente en una nueva sección defaults. Consulta también la directiva global "log-tag".

<a id="entry-4-2-max-keep-alive-queue"></a>

**`max-keep-alive-queue <value>`**

```haproxy
max-keep-alive-queue <value>
```

Establece el tamaño máximo de la cola del servidor para mantener conexiones keep-alive

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

HTTP keep-alive intenta reutilizar la misma conexión al servidor siempre que sea posible, pero a
veces puede ser contraproducente, por ejemplo si un servidor tiene muchas conexiones mientras otros están inactivos. Esto es especialmente cierto para los servidores estáticos.

El propósito de este ajuste es establecer un umbral en el número de conexiones en cola a partir del
cual HAProxy deja de intentar reutilizar el mismo servidor y prefiere buscar otro. El valor por
defecto, -1, significa que no hay límite. Un valor de cero significa que las solicitudes keep-alive
nunca se pondrán en cola. Para servidores muy cercanos que pueden alcanzarse con una latencia baja y
que no son sensibles a romper el keep-alive, se recomienda un valor bajo (p. ej., un servidor estático
local puede usar un valor de 10 o menos). Para servidores remotos que sufren una latencia alta, pueden
necesitarse valores más altos para cubrir la latencia y/o el coste de elegir un servidor diferente.

Ten en cuenta que esto no afecta a las respuestas que se mantienen en el mismo servidor
consecutivamente a una respuesta 401. Seguirán yendo al mismo servidor incluso si tienen que ponerse
en cola.

Ver también: "option http-server-close", "option prefer-last-server", "maxconn" del servidor y la
persistencia por cookie.

<a id="entry-4-2-max-session-srv-conns"></a>

**`max-session-srv-conns <nb>`**

```haproxy
max-session-srv-conns <nb>
```

Establece el número máximo de conexiones salientes que podemos mantener inactivas para una sesión de
cliente dada. El valor por defecto es 5 (equivale exactamente a MAX_SRV_LIST, que se define en tiempo
de compilación).

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no


<a id="entry-4-2-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

Fija el número máximo de conexiones simultáneas en un frontend

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<conns>   es el número máximo de conexiones concurrentes que el frontend
          aceptará atender. Las conexiones en exceso se encolarán por el
          sistema en la cola de escucha del socket y se atenderán en
          cuanto se cierre una conexión.
```

Si el sistema lo soporta, puede ser útil en sitios grandes elevar este límite muy alto para que
HAProxy gestione las colas de conexiones, en lugar de dejar a los clientes con intentos de conexión
sin respuesta. Este valor no debería superar el maxconn global. Además, ten en mente que una conexión
contiene dos búferes de tune.bufsize (16kB por defecto) cada uno, así como otros datos que resultan
en unos 33 kB de RAM consumidos por conexión establecida. Esto significa que un sistema medio
equipado con 1GB de RAM puede soportar alrededor de 20000-25000 conexiones simultáneas si se ajusta
correctamente.

Además, cuando `<conns>` se establece a valores grandes, es posible que los servidores no estén
dimensionados para aceptar tales cargas, y por esta razón generalmente es prudente asignarles límites
de conexión razonables.

Cuando este valor se establece a cero, que es el valor por defecto, se usa el valor "maxconn" global.

Ver también: "server", "maxconn" de la sección global, "fullconn"

<a id="entry-4-2-mode"></a>

**`mode { tcp|http|log|spop }`**

```haproxy
mode { tcp|http|log|spop }
```

Establece el modo de ejecución o el protocolo de la instancia Puede usarse en las secciones: defaults \| frontend \|
listen \| backend sí \| sí \| sí \| sí Argumentos:

```text
tcp       La instancia funcionará en modo TCP puro. Se establecerá una
          conexión full-duplex entre clientes y servidores, y no se
          realizará ningún examen de capa 7. Este es el modo por defecto.
          Debería usarse para SSL, SSH, SMTP, ...

http      La instancia funcionará en modo HTTP. La solicitud del cliente se
          analizará en profundidad antes de conectar con cualquier
          servidor. Cualquier solicitud que no cumpla las RFC será
          rechazada. Serán posibles el filtrado, el procesamiento y la
          conmutación de capa 7. Este es el modo que aporta a HAProxy la
          mayor parte de su valor.

haterm    El frontend funcionará en modo de prueba (benchmark) HTTP
          haterm. No está soportado por los backends. Ver doc/haterm.txt
          para más detalles.

log       Cuando se usa en una sección backend, convierte el backend en un
          backend de registro. Tal backend puede usarse como destino de
          registros para cualquier directiva "log" usando la sintaxis
          "backend@<name>". Los mensajes de registro se distribuirán a
          los servidores del backend según la configuración de balanceo,
          que puede configurarse con la palabra clave "balance". Los
          backends de registro soportan servidores UDP prefijando la
          dirección del servidor con el prefijo "udp@". Se soportan las
          características comunes de backend y de servidor, pero no las
          específicas de TCP o HTTP.

spop      Cuando se usa en una sección backend, convierte el backend en un
          backend spop. Este modo es obligatorio si el backend contiene
          servidores SPOA, pero cuando el modo es tcp, se convertirá
          automáticamente a modo spop si se detectan tales servidores.

```

Al hacer conmutación de contenido, es obligatorio que el frontend y el backend estén en el mismo modo
(generalmente HTTP); de lo contrario, la configuración será rechazada.

Ejemplo:

```text
defaults http_instances
    mode http

```

<a id="entry-4-2-monitor-fail"></a>

**`monitor fail { if | unless } <condition>`**

```haproxy
monitor fail { if | unless } <condition>
```

Añade una condición para informar de un fallo a una solicitud HTTP de monitorización.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
if <cond>     la solicitud del monitor fallará si la condición se cumple,
              y tendrá éxito en caso contrario. La condición debería
              describir una comprobación combinada que deba provocar un
              fallo si se cumplen todas las condiciones, por ejemplo un
              número bajo de servidores tanto en un backend como en su
              backup.

unless <cond> la solicitud del monitor solo tendrá éxito si la condición se
              cumple, y fallará en caso contrario. Tal condición puede
              basarse en una comprobación de la presencia de un número
              mínimo de servidores activos en una lista de backends.
```

Esta instrucción añade una condición que puede forzar que la respuesta a una solicitud de
monitorización informe de un fallo. Por defecto, cuando un componente externo consulta el URI
dedicado a la monitorización, se devuelve una respuesta 200. Cuando se cumple una de las condiciones
anteriores, HAProxy devolverá 503 en lugar de 200. Esto es muy útil para informar del fallo de un
sitio a un componente externo que puede basar los anuncios de enrutamiento entre múltiples sitios en
la disponibilidad informada por HAProxy. En este caso, convendría usar una ACL que involucre el
criterio "nbsrv". Ten en cuenta que "monitor fail" solo funciona en modo HTTP. Ambos mensajes de
estado pueden ajustarse usando "errorfile" o "errorloc" si es necesario.

Ejemplo:

```text
frontend www
   mode http
   acl site_dead nbsrv(dynamic) lt 2
   acl site_dead nbsrv(static)  lt 2
   monitor-uri   /site_alive
   monitor fail  if site_dead
```

Ver también: "monitor-uri", "errorfile", "errorloc"

<a id="entry-4-2-monitor-uri"></a>

**`monitor-uri <uri>`**

```haproxy
monitor-uri <uri>
```

Intercepta un URI usado por las solicitudes de monitorización de componentes externos

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<uri>     es el URI exacto que se quiere interceptar para devolver el estado
          de salud de HAProxy en lugar de reenviar la solicitud.
```

Cuando se reciba en un frontend una solicitud HTTP que referencie `<uri>`, HAProxy no la reenviará ni
la registrará, sino que devolverá "HTTP/1.0 200 OK" o "HTTP/1.0 503 Service unavailable", dependiendo
de las condiciones de fallo definidas con "monitor fail". Esto normalmente basta para que cualquier
sonda HTTP frontal detecte que el servicio está UP y en ejecución sin reenviar la solicitud a un
servidor del backend. Ten en cuenta que el método HTTP, la versión y todas las cabeceras se ignoran,
pero la solicitud debe ser al menos válida a nivel HTTP. Esta palabra clave solo puede usarse con un
frontend en modo HTTP.

Las solicitudes de monitorización se procesan muy pronto, justo después de analizar la solicitud e
incluso antes que cualquier "http-request". Los únicos conjuntos de reglas que se aplican antes son
los de tcp-request. Tampoco pueden registrarse, y ese es el propósito previsto. Solo puede
configurarse un URI para la monitorización; cuando hay presentes múltiples instrucciones
"monitor-uri", la última definirá el URI que se usará. Solo se usan para informar de la salud de
HAProxy a un componente superior, nada más. Sin embargo, es posible añadir cualquier número de
condiciones usando "monitor fail" y ACLs para que el resultado pueda ajustarse a cualquier
comprobación imaginable (muy a menudo el número de servidores disponibles en un backend).

Nota: si `<uri>` empieza por una barra ('/'), la coincidencia se realiza contra la ruta (path) de la
solicitud en lugar del uri de la solicitud. Es una solución para permitir que las solicitudes HTTP/2
coincidan con monitor-uri. En efecto, en HTTP/2, se recomienda a los clientes enviar solo URIs
absolutos.

Ejemplo:

```shell
# Use /haproxy_test to report HAProxy's status
frontend www
    mode http
    monitor-uri /haproxy_test
```

Ver también: "monitor fail"

<a id="entry-4-2-option-abortonclose"></a>

**`option abortonclose`**

```haproxy
option abortonclose
no option abortonclose
```

Habilita o deshabilita el aborto temprano del procesamiento no iniciado cuando el cliente cierra

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Las conexiones TCP soportan el cierre independiente en cada dirección, y una conexión con solo una
dirección cerrada suele decirse que está "semicerrada" (half-closed). Originalmente, cuando el
ecosistema HTTP estaba compuesto mayormente del "modo close", con solo una solicitud y una respuesta
por conexión antes de cerrar, era bastante frecuente ver clientes con script enviar su solicitud,
cerrar el lado de envío, esperar la respuesta, recibir la indicación de cierre y terminar. Pero con
la llegada del keep-alive y de protocolos más avanzados, esta práctica ha desaparecido prácticamente
y los únicos casos en que un cliente cierra antes de recibir su respuesta son esencialmente cuando el
usuario quiere abortar una transferencia, o cuando se dispara un timeout y la conexión se cierra.

Estas dos situaciones (semicierre frente a aborto) son indistinguibles desde el lado del servidor
(aquí el listener de HAProxy). Esto es un problema porque dejar la conexión viva y continuar
procesando una solicitud cuando los clientes abortan puede costar muchos recursos, particularmente si
el cierre es el resultado de que un usuario pulse el botón de "recargar", ya que significa que se
ponen en cola nuevas solicitudes sin abortar las anteriores. Y a la inversa, abortar sistemáticamente
ante tal situación de semicierre rompería a varias aplicaciones TCP e incluso algunas HTTP en redes
internas que interactúan con agentes heredados.

La opción "abortonclose" permite elegir el comportamiento deseado: - cuando está presente en un
frontend, evita procesar negociaciones TLS pendientes en una conexión semicerrada. Esto puede ser el
resultado de que un usuario pulse "recargar" durante una solicitud HTTPS bajo carga alta, como una
conmutación por error VRRP entre un nodo HAProxy activo y el de respaldo: todos los clientes se
reconectan al mismo tiempo al nuevo nodo y todos tienen que realizar una negociación TLS completa y
costosa. Si tarda más de unos segundos, es probable que algunos usuarios se rindan, y no tiene
sentido desperdiciar ciclos de CPU en sus negociaciones. Dado el coste de CPU de las negociaciones
TLS, se recomienda dejar esta opción habilitada en frontends expuestos a internet. Este es el valor
por defecto para las conexiones TLS entrantes.

    - cuando está presente en un backend, hará que las conexiones semicerradas
      intenten abortar una solicitud que aún no se ha enviado a un servidor
      (es decir, cuando está pendiente en la cola o cuando se está intentando
      conectar). Si la solicitud ya está siendo atendida por un servidor,
      entonces la conexión al servidor pasa a su vez a semicierre para indicar
      la misma condición al servidor, que decidirá entonces cómo proceder.
      Este es el valor por defecto para los backends en modo HTTP.

La recomendación es habilitar esta opción en los extremos TLS y servicios HTTP expuestos a internet,
y deshabilitarla para los puramente TCP así como para entornos heredados no expuestos. Está
habilitada por defecto en los backends HTTP, y puede deshabilitarse forzadamente anteponiendo la
palabra clave "no", bien en la propia sección backend, bien en la sección "defaults" de la que
hereda. También está habilitada por defecto para los listeners TLS y puede deshabilitarse
forzadamente igualmente especificando "no option abortonclose" en el frontend o en la sección
"defaults" de la que hereda.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "timeout queue" y los parámetros "maxconn" y "maxqueue" del servidor

<a id="entry-4-2-option-accept-invalid-http-request"></a>

**`option accept-invalid-http-request     (deprecated)`**

```haproxy
option accept-invalid-http-request     (deprecated)
no option accept-invalid-http-request  (deprecated)
```

Habilita o deshabilita la relajación del análisis de solicitudes HTTP

La palabra clave "accept-invalid-http-request" está obsoleta; usa "option
accept-unsafe-violations-in-http-request" en su lugar.

<a id="entry-4-2-option-accept-invalid-http-response"></a>

**`option accept-invalid-http-response     (deprecated)`**

```haproxy
option accept-invalid-http-response     (deprecated)
no option accept-invalid-http-response  (deprecated)
```

Habilita o deshabilita la relajación del análisis de respuestas HTTP

La palabra clave "accept-invalid-http-response" está obsoleta; usa "option
accept-unsafe-violations-in-http-response" en su lugar.

<a id="entry-4-2-option-accept-unsafe-violations-in-http-request"></a>

**`option accept-unsafe-violations-in-http-request`**

```haproxy
option accept-unsafe-violations-in-http-request
no option accept-unsafe-violations-in-http-request
```

Habilita o deshabilita la relajación del análisis de solicitudes HTTP

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Por defecto, HAProxy cumple las diferentes RFC HTTP en términos de análisis de mensajes. Esto
significa que el análisis de mensajes es bastante estricto y provoca que se devuelva un error al
cliente por los mensajes malformados. Este es el comportamiento deseado, ya que tales mensajes
malformados se usan esencialmente para construir ataques que explotan debilidades del servidor y
eluden el filtrado de seguridad. A veces, un navegador con errores no respetará estas RFC por la
razón que sea (configuración, implementación...) y el problema no se corregirá de inmediato. En tal
caso, es posible relajar el analizador de HAProxy para aceptar algunas solicitudes no válidas
especificando esta opción. La mayoría de las reglas afectan al análisis de H1 por razones
históricas. Las versiones más nuevas de HTTP tienden a ser más limpias y las aplicaciones siguen
estos protocolos con más rigor.

Cuando se establece esta opción, se observan las siguientes reglas:

    * Solo en H1, los caracteres no válidos, incluido el carácter NULL, en el
      nombre de cabecera no se rechazarán; sin embargo, la cabecera se
      descartará.

    * Solo en H1, el carácter NULL en el valor de cabecera será aceptado;

    * Solo en H1, los caracteres por encima de 127 en el URI serán aceptados.
      La lista de caracteres que pueden aparecer en un URI está bien definida
      por RFC3986, y los caracteres 0-31, 32 (espacio), 34 ('"'), 60 ('<'),
      62 ('>'), 92 ('&#92;'), 94 ('^'), 96 ('`'), 123 ('{'), 124 ('|'),
      125 ('}'), 127 (suprimir) y cualquier valor superior normalmente no
      están permitidos. En H1, todos los caracteres entre (0..32) y 127
      siempre se bloquearán. Todos los caracteres por encima de 127
      (excluido) también se bloquearán, excepto cuando esta opción está
      habilitada. Los demás caracteres (33..126) no se comprobarán en
      absoluto.

    * En H1 y H2, las URL que contienen referencias de fragmento ('#' tras la
      ruta) serán aceptadas;

    * Solo en H1, no se realizará ninguna comprobación sobre la autoridad para
      las solicitudes CONNECT;

    * Solo en H1, no se realizará ninguna comprobación entre la autoridad y el
      valor de la cabecera Host.

    * Solo en H1, las pruebas sobre la versión HTTP se relajarán. Permitirá
      pasar solicitudes GET HTTP/0.9 (sin versión especificada), así como
      diferentes nombres de protocolo (p. ej., RTSP), y múltiples dígitos
      tanto para la versión mayor como para la menor.

    * Solo en H1, las solicitudes WebSocket (RFC6455) que no presenten un
      campo de cabecera "Sec-Websocket-Key" válido serán aceptadas.

Esta opción nunca debería habilitarse por defecto, ya que oculta errores de aplicación y abre brechas
de seguridad. Solo debería desplegarse después de que se haya confirmado un problema.

Cuando esta opción está habilitada, las solicitudes H1 no válidas pero aceptadas se capturarán para
permitir un análisis posterior usando la solicitud "show errors" en el socket de estadísticas
UNIX. Hacer esto también ayuda a confirmar que el problema se ha resuelto.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option accept-unsafe-violations-in-http-response" y "show errors" en el socket de estadísticas.

<a id="entry-4-2-option-accept-unsafe-violations-in-http-response"></a>

**`option accept-unsafe-violations-in-http-response`**

```haproxy
option accept-unsafe-violations-in-http-response
no option accept-unsafe-violations-in-http-response
```

Habilita o deshabilita la relajación del análisis de respuestas HTTP

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

De forma similar a "option accept-unsafe-violations-in-http-request", esta opción puede usarse para
relajar las reglas de análisis de las respuestas HTTP. Solo debería habilitarse para servidores
heredados de confianza para aceptar algunas respuestas no válidas. La mayoría de las reglas afectan
al análisis de H1 por razones históricas. Las versiones más nuevas de HTTP tienden a ser más limpias
y las aplicaciones siguen estos protocolos con más rigor.

Cuando se establece esta opción, se observan las siguientes reglas:

    * Solo en H1, los códigos de estado de más de 3 dígitos pero cuyo valor
      cabe en 16 bits no se rechazan.

    * Solo en H1, los caracteres no válidos, incluido el carácter NULL, en el
      nombre de cabecera no se rechazarán; sin embargo, la cabecera se
      descartará.

    * Solo en H1, el carácter NULL en el valor de cabecera será aceptado;

    * Solo en H1, los valores vacíos o varias apariciones del valor "chunked"
      para la cabecera Transfer-Encoding serán aceptados;

    * Solo en H1, no se realizará ninguna comprobación entre la autoridad y el
      valor de la cabecera Host.

    * Solo en H1, las pruebas sobre la versión HTTP se relajarán. Permitirá
      diferentes nombres de protocolo (p. ej., RTSP), y múltiples dígitos
      tanto para la versión mayor como para la menor.

    * Solo en H1, las respuestas WebSocket (RFC6455) que no presenten un campo
      de cabecera "Sec-Websocket-Accept" válido serán aceptadas.

Esta opción nunca debería habilitarse por defecto, ya que oculta errores de aplicación y abre brechas
de seguridad. Solo debería desplegarse después de que se haya confirmado un problema.

Cuando esta opción está habilitada, los nombres de cabecera erróneos seguirán siendo aceptados en las
respuestas, pero la respuesta completa se capturará para permitir un análisis posterior usando la
solicitud "show errors" en el socket de estadísticas UNIX. Hacer esto también ayuda a confirmar que
el problema se ha resuelto.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option accept-unsafe-violations-in-http-request" y "show errors" en el socket de estadísticas.

<a id="entry-4-2-option-allbackups"></a>

**`option allbackups`**

```haproxy
option allbackups
no option allbackups
```

Usa todos los servidores de respaldo a la vez o solo el primero

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Por defecto, el primer servidor de respaldo operativo recibe todo el tráfico cuando los servidores
normales están todos caídos. A veces puede preferirse usar múltiples respaldos a la vez, porque uno
no será suficiente. Cuando "option allbackups" está habilitada, el balanceo de carga se realizará
entre todos los servidores de respaldo cuando todos los normales no estén disponibles. Se usará el
mismo algoritmo de balanceo de carga y se respetarán los pesos de los servidores. Así, ya no habrá
ningún orden de prioridad entre los servidores de respaldo.

Esta opción se usa mayormente con granjas de servidores estáticos dedicadas a devolver una página de
"disculpa" cuando una aplicación está completamente fuera de línea.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

<a id="entry-4-2-option-checkcache"></a>

**`option checkcache`**

```haproxy
option checkcache
no option checkcache
```

Analiza todas las respuestas del servidor y bloquea las respuestas con cookies cacheables

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Algunos frameworks de alto nivel establecen cookies de aplicación en todas partes y no siempre dejan
suficiente control al desarrollador para gestionar cómo deberían cachearse las respuestas. Cuando se
devuelve una cookie de sesión en un objeto cacheable, hay un alto riesgo de cruce o robo de sesión
entre usuarios que atraviesan las mismas cachés. En algunas situaciones, es mejor bloquear la
respuesta que dejar que cierta información sensible de sesión se exponga.

La opción "checkcache" habilita la inspección profunda de todas las respuestas del servidor para un
estricto cumplimiento de la especificación HTTP en términos de cacheabilidad. Comprueba
cuidadosamente las cabeceras "Cache-control", "Pragma" y "Set-cookie" en la respuesta del servidor
para verificar si hay riesgo de cachear una cookie en un proxy del lado del cliente. Cuando esta
opción está habilitada, las únicas respuestas que pueden entregarse al cliente son: - todas aquellas
sin cabecera "Set-Cookie"; - todas aquellas con un código de retorno distinto de 200, 203, 204, 206,
300, 301, 404, 405, 410, 414, 501, siempre que el servidor no haya establecido un campo de cabecera
"Cache-control: public"; - todas aquellas que resultan de una solicitud que usa un método distinto de
GET, HEAD, OPTIONS, TRACE, siempre que el servidor no haya establecido un campo de cabecera
'Cache-Control: public'; - aquellas con una cabecera 'Pragma: no-cache' - aquellas con una cabecera
'Cache-control: private' - aquellas con una cabecera 'Cache-control: no-store' - aquellas con una
cabecera 'Cache-control: max-age=0' - aquellas con una cabecera 'Cache-control: s-maxage=0' - aquellas
con una cabecera 'Cache-control: no-cache' - aquellas con una cabecera 'Cache-control:
no-cache="set-cookie"' - aquellas con una cabecera 'Cache-control: no-cache="set-cookie,' (permitiendo
otros campos después de set-cookie) - aquellas que no llevan ni información de frescura
("Cache-control" con un "max-age" o un "s-maxage", o una cabecera "Expires") ni un validador (una
cabecera "ETag" o "Last-Modified"), ya que tal respuesta no es almacenada por una caché conforme.

Si una respuesta no respeta estos requisitos, será bloqueada igual que si proviniera de una regla
"http-response deny", con un "HTTP 502 bad gateway". El estado de la sesión muestra "PH--", lo que
significa que el proxy bloqueó la respuesta durante el procesamiento de las cabeceras. Además, se
enviará una alerta en los registros para que los administradores sepan que hay algo que corregir.

Debido al alto impacto en la aplicación, la aplicación debería probarse a fondo con la opción
habilitada antes de pasar a producción. También es una buena práctica activarla siempre durante las
pruebas, incluso si no se usa en producción, ya que informará de comportamientos de aplicación
potencialmente peligrosos.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

<a id="entry-4-2-option-clitcpka"></a>

**`option clitcpka`**

```haproxy
option clitcpka
no option clitcpka
```

Habilita o deshabilita el envío de paquetes TCP keepalive en el lado del cliente

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Cuando hay un cortafuegos o cualquier componente consciente de sesión entre un cliente y un servidor,
y cuando el protocolo implica sesiones muy largas con largos periodos de inactividad (p. ej.,
escritorios remotos), existe el riesgo de que uno de los componentes intermedios decida expirar una
sesión que ha permanecido inactiva demasiado tiempo.

Habilitar los TCP keep-alive a nivel de socket hace que el sistema envíe paquetes regularmente al
otro extremo de la conexión, manteniéndola activa. El retardo entre sondeos keep-alive lo controla
únicamente el sistema y depende tanto del sistema operativo como de sus parámetros de ajuste.

Es importante entender que los paquetes keep-alive no se emiten ni se reciben a nivel de aplicación.
Solo las pilas de red los ven. Por esta razón, incluso si un lado del proxy ya usa keep-alives para
mantener viva su conexión, esos paquetes keep-alive no se reenviarán al otro lado del proxy.

Ten en cuenta que esto no tiene nada que ver con HTTP keep-alive.

Usar la opción "clitcpka" habilita la emisión de sondeos TCP keep-alive en el lado del cliente de una
conexión, lo que debería ayudar cuando se notan expiraciones de sesión entre HAProxy y un cliente.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option srvtcpka", "option tcpka"

<a id="entry-4-2-option-contstats"></a>

**`option contstats`**

```haproxy
option contstats
```

Habilita actualizaciones continuas de las estadísticas de tráfico

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Por defecto, los contadores usados para el cálculo de estadísticas se incrementan solo cuando un
flujo termina. Funciona bastante bien al servir objetos pequeños, pero con objetos grandes (por
ejemplo imágenes grandes o archivos) o con streaming de A/V, un gráfico generado desde los contadores
de HAProxy parece un erizo. Con esta opción habilitada, los contadores se incrementan con frecuencia
a lo largo del flujo, típicamente cada 5 segundos, lo que a menudo basta para producir gráficos
limpios. El recuento toca directamente una ruta caliente (hotpath), así que no está habilitado por
defecto, ya que puede causar muchos despertares para números de sesiones muy grandes y provocar una
pequeña caída de rendimiento.


<a id="entry-4-2-option-disable-h2-upgrade"></a>

**`option disable-h2-upgrade`**

```haproxy
option disable-h2-upgrade
no option disable-h2-upgrade
```

Habilita o deshabilita el cambio implícito al protocolo HTTP/2 desde una conexión de cliente HTTP/1.x.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Por defecto, HAProxy es capaz de cambiar implícitamente una conexión de cliente HTTP/1.x a una
conexión HTTP/2 si la primera solicitud que recibe de una conexión HTTP dada coincide con el
preámbulo de conexión HTTP/2 (es decir, la cadena "PRI \* HTTP/2.0&#92;r&#92;n&#92;r&#92;nSM&#92;r&#92;n&#92;r&#92;n").
De este modo, es posible soportar clientes HTTP/1.x y HTTP/2 en conexiones no SSL. Esta opción debe
usarse para deshabilitar el cambio implícito de protocolo. Ten en cuenta que este cambio implícito de protocolo
solo está soportado para proxies HTTP, y por tanto también esta opción. Ten en cuenta también que es
posible forzar HTTP/2 en conexiones sin cifrar especificando "proto h2" en la línea bind. Finalmente,
esta opción se aplica en todas las líneas bind. Para deshabilitar los cambios implícitos a
HTTP/2 para una línea bind específica, es posible usar "proto h1".

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

<a id="entry-4-2-option-dontlog-normal"></a>

**`option dontlog-normal`**

```haproxy
option dontlog-normal
no option dontlog-normal
```

Habilita o deshabilita el registro de conexiones normales y correctas

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Hay sitios grandes que gestionan varios miles de conexiones por segundo y para los que el registro es
un gran problema. Algunos se ven incluso obligados a desactivar los registros y no pueden depurar
problemas de producción. Establecer esta opción garantiza que las conexiones normales, aquellas que
no experimentan ningún error, ningún timeout, ningún reintento ni reenvío, no se registrarán. Esto
deja espacio en disco para las anomalías. En modo HTTP, se comprueba el código de estado de la
respuesta y los códigos de retorno 5xx seguirán registrándose.

Se desaconseja encarecidamente usar esta opción, ya que la mayoría de las veces la clave de los
problemas complejos está en los registros normales, que aquí no se registrarán. Si necesitas separar
los registros, consulta en cambio la opción "log-separate-errors".

Ver también: "log", "dontlognull", "log-separate-errors" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-dontlognull"></a>

**`option dontlognull`**

```haproxy
option dontlognull
no option dontlognull
```

Habilita o deshabilita el registro de conexiones nulas

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

En ciertos entornos, hay componentes que se conectarán regularmente a varios sistemas para
asegurarse de que siguen vivos. Puede ser el caso de otro balanceador de carga, así como de sistemas
de monitorización. Por defecto, incluso una simple sonda o escaneo de puerto producirá un registro.
Si esas conexiones contaminan demasiado los registros, es posible habilitar la opción "dontlognull"
para indicar que una conexión en la que no se ha transferido ningún dato no se registrará, lo que
corresponde típicamente a esas sondas. Ten en cuenta que los errores seguirán devolviéndose al
cliente y contabilizándose en las estadísticas. Si esto no es lo deseado, puede usarse en cambio la
opción http-ignore-probes.

Generalmente se recomienda no usar esta opción en entornos no controlados (p. ej., internet); de lo
contrario, los escaneos y otras actividades maliciosas no se registrarían.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "log", "http-ignore-probes", "monitor-uri" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-external-check"></a>

**`option external-check`**

```haproxy
option external-check
```

Usa procesos externos para las comprobaciones de estado de los servidores

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Es posible comprobar la salud de un servidor usando un comando externo. Esto se consigue ejecutando
el ejecutable establecido con "external-check command".

Requiere que esté establecido el "external-check" global.

Ver también: "external-check", "external-check command", "external-check path"

<a id="entry-4-2-option-forwarded"></a>

**`option forwarded [ proto ]`**

```haproxy
option forwarded [ proto ]
                 [ host | host-expr <host_expr> ]
                 [ by | by-expr <by_expr> ] [ by_port | by_port-expr <by_port_expr>]
                 [ for | for-expr <for_expr> ] [ for_port | for_port-expr <for_port_expr>]
no option forwarded
```

Habilita la inserción de la cabecera forwarded de la rfc 7239 en las solicitudes enviadas a los
servidores

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<host_expr>     argumento opcional para especificar una expresión de
                muestra personalizada cuyo resultado se usará como valor
                del parámetro 'host'

<by_expr>       argumento opcional para especificar una expresión de
                muestra personalizada cuyo resultado se usará como valor
                nodename del parámetro 'by'

<for_expr>      argumento opcional para especificar una expresión de
                muestra personalizada cuyo resultado se usará como valor
                nodename del parámetro 'for'

<by_port_expr>  argumento opcional para especificar una expresión de
                muestra personalizada cuyo resultado se usará como valor
                nodeport del parámetro 'by'

<for_port_expr> argumento opcional para especificar una expresión de
                muestra personalizada cuyo resultado se usará como valor
                nodeport del parámetro 'for'

```

Como HAProxy trabaja en modo proxy inverso, los servidores pierden parte del contexto de la solicitud
(origen de la solicitud: dirección IP del cliente, protocolo usado...)

Una forma común de abordar esta limitación es usar las conocidas x-forward-for y sus amigas
x-forward-\* para exponer parte de este contexto a los servidores/aplicaciones subyacentes. Aunque
esto solía funcionar y está ampliamente desplegado, no está soportado oficialmente por el IETF y puede
ser la raíz de algunos problemas de interoperabilidad así como de seguridad.

Para resolver esto, el IETF ha descrito una nueva extensión HTTP: la cabecera forwarded (RFC7239).
Más información aquí: <https://www.rfc-editor.org/rfc/rfc7239.html>

El uso de esta única cabecera permite transmitir numerosos detalles dentro de la misma cabecera y, lo
más importante, corrige el problema del encadenamiento de proxies. (la rfc permite que múltiples
proxies encadenados añadan sus propios valores a una cabecera ya existente).

Esta opción puede especificarse en las secciones defaults, listen o backend, pero se ignorará en las
secciones frontend.

Establecer la opción forwarded sin argumentos resulta en el uso del comportamiento implícito por
defecto. El comportamiento por defecto habilita el parámetro proto e inyecta la IP original del
cliente.

La configuración explícita/manual equivalente sería:

```text
option forwarded proto for
```

La palabra clave 'by' se usa para habilitar el parámetro 'by' ("nodename") en la cabecera forwarded.
Permite incrustar información del proxy de la solicitud. El valor de 'by' se establecerá a la IP del
proxy (dirección de destino). Si no está disponible (es decir: listener UNIX), 'by' se establecerá a
"unknown".

La palabra clave 'by-expr' se usa para habilitar el parámetro 'by' ("nodename") en la cabecera
forwarded. Permite incrustar información del proxy de la solicitud. El valor de 'by' se establecerá
al resultado de la expresión de muestra `<by_expr>`, si es válida; de lo contrario, se establecerá a
"unknown".

La palabra clave 'for' se usa para habilitar el parámetro 'for' ("nodename") en la cabecera
forwarded. Permite incrustar información del cliente de la solicitud. El valor de 'for' se
establecerá a la IP del cliente (dirección de origen). Si no está disponible (es decir: listener
UNIX), 'for' se establecerá a "unknown".

La palabra clave 'for-expr' se usa para habilitar el parámetro 'for' ("nodename") en la cabecera
forwarded. Permite incrustar información del cliente de la solicitud. El valor de 'for' se
establecerá al resultado de la expresión de muestra `<for_expr>`, si es válida; de lo contrario, se
establecerá a "unknown".

La palabra clave 'by_port' se usa para proporcionar información del "nodeport" al parámetro 'by'.
'by_port' requiere que 'by' o 'by-expr' estén establecidos o se ignorará. El "nodeport" se
establecerá al puerto del proxy (destino) si está disponible; de lo contrario, se ignorará.

La palabra clave 'by_port-expr' se usa para proporcionar información del "nodeport" al parámetro
'by'. 'by_port-expr' requiere que 'by' o 'by-expr' estén establecidos o se ignorará. El "nodeport" se
establecerá al resultado de la expresión de muestra `<by_port_expr>`, si es válida; de lo contrario,
se ignorará.

La palabra clave 'for_port' se usa para proporcionar información del "nodeport" al parámetro 'for'.
'for_port' requiere que 'for' o 'for-expr' estén establecidos o se ignorará. El "nodeport" se
establecerá al puerto del cliente (origen) si está disponible; de lo contrario, se ignorará.

La palabra clave 'for_port-expr' se usa para proporcionar información del "nodeport" al parámetro
'for'. 'for_port-expr' requiere que 'for' o 'for-expr' estén establecidos o se ignorará. El
"nodeport" se establecerá al resultado de la expresión de muestra `<for_port_expr>`, si es válida; de
lo contrario, se ignorará.

Ejemplos:

```shell
# Those servers want the ip address and protocol of the client request
# Resulting header would look like this:
#   forwarded: proto=http;for=127.0.0.1
backend www_default
    mode http
    option forwarded
    #equivalent to: option forwarded proto for

# Those servers want the requested host and hashed client ip address
# as well as client source port (you should use seed for xxh32 if ensuring
# ip privacy is a concern)
# Resulting header would look like this:
#   forwarded: host="haproxy.org";for="_000000007F2F367E:60138"
backend www_host
    mode http
    option forwarded host for-expr src,xxh32,hex for_port

# Those servers want custom data in host, for and by parameters
# Resulting header would look like this:
#   forwarded: host="host.com";by=_haproxy;for="[::1]:10"
backend www_custom
    mode http
    option forwarded host-expr str(host.com) by-expr str(_haproxy) for for_port-expr int(10)

# Those servers want random 'for' obfuscated identifiers for request
# tracing purposes while protecting sensitive IP information
# Resulting header would look like this:
#   forwarded: for=_000000002B1F4D63
backend www_for_hide
    mode http
    option forwarded for-expr rand,hex
```

Ver también: "option forwardfor", "option originalto"

<a id="entry-4-2-option-forwardfor"></a>

**`option forwardfor [ except <network> ] [ header <name> ] [ if-none ]`**

```haproxy
option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
```

Habilita la inserción de la cabecera X-Forwarded-For en las solicitudes enviadas a los servidores

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<network> es un argumento opcional usado para desactivar esta opción para las
          fuentes que coincidan con <network>
<name>    un argumento opcional para especificar un nombre de cabecera
          distinto para "X-Forwarded-For".
```

Como HAProxy trabaja en modo proxy inverso, los servidores ven su dirección IP como su dirección de
cliente. Esto a veces resulta molesto cuando se espera la dirección IP del cliente en los registros
del servidor. Para resolver este problema, HAProxy puede añadir la conocida cabecera HTTP
"X-Forwarded-For" a todas las solicitudes enviadas al servidor. Esta cabecera contiene un valor que
representa la dirección IP del cliente. Como esta cabecera siempre se añade al final de la lista de
cabeceras existente, el servidor debe configurarse para usar siempre solo la última aparición de esta
cabecera. Consulta el manual del servidor para saber cómo habilitar el uso de esta cabecera
estándar. Ten en cuenta que solo debe usarse la última aparición de la cabecera, ya que es realmente
posible que el cliente ya haya traído una.

La palabra clave "header" puede usarse para suministrar un nombre de cabecera diferente que reemplace
la "X-Forwarded-For" por defecto. Esto puede ser útil cuando ya podrías tener una cabecera
"X-Forwarded-For" de una aplicación diferente (p. ej., stunnel) y necesitas conservarla. También si tu
servidor del backend no usa la cabecera "X-Forwarded-For" y requiere otra diferente (p. ej., Zeus Web
Servers requiere "X-Cluster-Client-IP").

A veces, una misma instancia de HAProxy puede compartirse entre un acceso directo de clientes y un
acceso de proxy inverso (por ejemplo cuando se usa un proxy inverso SSL para descifrar el tráfico
HTTPS). Es posible deshabilitar la adición de la cabecera para una dirección o red de origen conocida
añadiendo la palabra clave "except" seguida de la dirección de red. En este caso, cualquier IP de
origen que coincida con la red no provocará la adición de esta cabecera. Los usos más comunes son con
redes privadas o 127.0.0.1. Se soportan tanto IPv4 como IPv6.

Alternativamente, la palabra clave "if-none" indica que la cabecera solo se añadirá si no está
presente. Esto solo debería usarse en un entorno de total confianza, ya que podría causar un problema
de seguridad si las cabeceras que llegan a HAProxy están bajo el control del usuario final.

Esta opción puede especificarse en el frontend o en el backend. Si al menos uno de ellos la usa, la
cabecera se añadirá. Ten en cuenta que el ajuste del subargumento header del backend prevalece sobre
el del frontend si ambos están definidos. En el caso del argumento "if-none", si al menos uno del
frontend o del backend no lo especifica, quiere que la adición sea obligatoria, así que gana.

Ejemplo:

```shell
# Public HTTP address also used by stunnel on the same machine
frontend www
    mode http
    option forwardfor except 127.0.0.1  # stunnel already adds the header

# Those servers want the IP Address in X-Client
backend www
    mode http
    option forwardfor header X-Client
```

Ver también: "option httpclose", "option http-server-close", "option http-keep-alive"

<a id="entry-4-2-option-h1-case-adjust-bogus-client"></a>

**`option h1-case-adjust-bogus-client`**

```haproxy
option h1-case-adjust-bogus-client
no option h1-case-adjust-bogus-client
```

Habilita o deshabilita el ajuste de mayúsculas/minúsculas de las cabeceras HTTP/1 enviadas a clientes
defectuosos

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

No existe un uso de mayúsculas estándar para los nombres de cabecera porque, como se indica en
RFC7230, son insensibles a mayúsculas/minúsculas. Así que las aplicaciones deben gestionarlas de
forma insensible a mayúsculas/minúsculas. Pero algunas aplicaciones defectuosas violan los estándares
y dependen erróneamente de los usos de mayúsculas más comunes de los navegadores. Este problema se
vuelve crítico con HTTP/2 porque todos los nombres de cabecera deben intercambiarse en minúsculas, y
HAProxy sigue la misma convención. Todos los nombres de cabecera se envían en minúsculas a clientes y
servidores, independientemente de la versión HTTP.

Cuando HAProxy recibe una respuesta HTTP/1, sus nombres de cabecera se convierten a minúsculas, se
manipulan y se envían así a los clientes. Si se sabe que un cliente viola los estándares HTTP y falla
al procesar una respuesta proveniente de HAProxy, es posible transformar los nombres de cabecera en
minúsculas a un formato diferente cuando la respuesta se formatea y se envía al cliente, habilitando
esta opción y especificando la lista de cabeceras que deben reformatearse usando las directivas
globales "h1-case-adjust" o "h1-case-adjust-file". Esto debe ser solo una solución temporal durante
el tiempo que tarda el cliente en corregirse, porque los clientes que requieren tales soluciones
podrían ser vulnerables a ataques de contrabando de contenido y deben corregirse sin falta.

Ten en cuenta que esta opción no afectará a los clientes conformes al estándar.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option h1-case-adjust-bogus-server", "h1-case-adjust", "h1-case-adjust-file".

<a id="entry-4-2-option-h1-case-adjust-bogus-server"></a>

**`option h1-case-adjust-bogus-server`**

```haproxy
option h1-case-adjust-bogus-server
no option h1-case-adjust-bogus-server
```

Habilita o deshabilita el ajuste de mayúsculas/minúsculas de las cabeceras HTTP/1 enviadas a
servidores defectuosos

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

No existe un uso de mayúsculas estándar para los nombres de cabecera porque, como se indica en
RFC7230, son insensibles a mayúsculas/minúsculas. Así que las aplicaciones deben gestionarlas de
forma insensible a mayúsculas/minúsculas. Pero algunas aplicaciones defectuosas violan los estándares
y dependen erróneamente de los usos de mayúsculas más comunes de los navegadores. Este problema se
vuelve crítico con HTTP/2 porque todos los nombres de cabecera deben intercambiarse en minúsculas, y
HAProxy sigue la misma convención. Todos los nombres de cabecera se envían en minúsculas a clientes y
servidores, independientemente de la versión HTTP.

Cuando HAProxy recibe una solicitud HTTP/1, sus nombres de cabecera se convierten a minúsculas, se
manipulan y se envían así a los servidores. Si se sabe que un servidor viola los estándares HTTP y
falla al procesar una solicitud proveniente de HAProxy, es posible transformar los nombres de
cabecera en minúsculas a un formato diferente cuando la solicitud se formatea y se envía al servidor,
habilitando esta opción y especificando la lista de cabeceras que deben reformatearse usando las
directivas globales "h1-case-adjust" o "h1-case-adjust-file". Esto debe ser solo una solución
temporal durante el tiempo que tarda el servidor en corregirse, porque los servidores que requieren
tales soluciones podrían ser vulnerables a ataques de contrabando de contenido y deben corregirse
sin falta.

Ten en cuenta que esta opción no afectará a los servidores conformes al estándar.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option h1-case-adjust-bogus-client", "h1-case-adjust", "h1-case-adjust-file".

<a id="entry-4-2-option-http-buffer-request"></a>

**`option http-buffer-request`**

```haproxy
option http-buffer-request
no option http-buffer-request
```

Habilita o deshabilita la espera de todo el cuerpo de la solicitud HTTP antes de continuar

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

A veces es deseable esperar el cuerpo de una solicitud HTTP antes de tomar una decisión. Esto es lo
que hace, por ejemplo, "balance url_param". El primer caso de uso es almacenar en búfer las
solicitudes de clientes lentos antes de conectar con el servidor. Otro caso de uso consiste en tomar
la decisión de enrutamiento basándose en el contenido del cuerpo de la solicitud. Esta opción,
situada en un frontend o backend, fuerza al procesamiento HTTP a esperar hasta que se reciba todo el
cuerpo o el búfer de solicitud esté lleno. Puede tener efectos secundarios no deseados con algunas
aplicaciones que abusan de HTTP esperando transmisiones sin búfer entre el frontend y el backend,
así que definitivamente no debería usarse por defecto.

Ver también: "option http-no-delay", "timeout http-request", "http-request wait-for-body"

<a id="entry-4-2-option-http-drop-request-trailers"></a>

**`option http-drop-request-trailers`**

```haproxy
option http-drop-request-trailers
no option http-drop-request-trailers
```

Descarta los trailers HTTP de la solicitud cuando se envía al servidor

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| no \| sí

Argumentos: ninguno

Cuando esta opción está habilitada, cualquier trailer HTTP encontrado en una solicitud se descartará
antes de enviarla al servidor.

RFC9110#section-6.5.1 establecía que los campos trailer podían fusionarse con los campos de cabecera.
Debería hacerse a propósito, pero puede ser un problema para algunas aplicaciones, especialmente si
clientes maliciosos ocultan campos de cabecera sensibles en la parte de trailers y algunos
intermediarios los fusionan con las cabeceras sin comprobaciones específicas. En ese caso, puede
habilitarse esta opción en el backend para descartar cualquier campo trailer encontrado en las
solicitudes antes de enviarlas al servidor.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option http-drop-response-trailers"

<a id="entry-4-2-option-http-drop-response-trailers"></a>

**`option http-drop-response-trailers`**

```haproxy
option http-drop-response-trailers
no option http-drop-response-trailers
```

Descarta los trailers HTTP de la respuesta cuando se envía al cliente

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Esta opción es similar a "option http-drop-request-trailers", pero debe usarse para descartar los
campos trailer de las respuestas antes de enviarlas a los clientes.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option http-drop-request-trailers"

<a id="entry-4-2-option-http-ignore-probes"></a>

**`option http-ignore-probes`**

```haproxy
option http-ignore-probes
no option http-ignore-probes
```

Habilita o deshabilita el registro de conexiones nulas y timeouts de solicitud

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Recientemente, algunos navegadores empezaron a implementar una función de "preconexión" que consiste
en conectarse de forma especulativa a algunos sitios web visitados recientemente por si el usuario
quisiera visitarlos. Esto da como resultado muchas conexiones establecidas a sitios web, que terminan
en 408 Request Timeout si el timeout se dispara primero, o 400 Bad Request cuando el navegador decide
cerrarlas primero. Estas contaminan el registro y alimentan los contadores de errores. Ya existía
"option dontlognull", pero es insuficiente en este caso. En su lugar, esta opción hace lo siguiente: - impide que se envíe al cliente cualquier mensaje 400/408 si no se recibió nada por una conexión
antes de que se cerrara; - impide que se emita cualquier registro en esta situación; - impide que se
incremente cualquier contador de errores

De este modo, la conexión vacía se ignora en silencio. Ten en cuenta que es mejor no usar esto salvo
que esté claro que es necesario, porque ocultará problemas reales. La razón más común de no recibir
una solicitud y ver un 408 se debe a una inconsistencia de MTU entre el cliente y un elemento
intermedio como una VPN, que bloquea los paquetes demasiado grandes. Estos problemas generalmente se
ven con solicitudes POST así como GET con cookies grandes. Los registros a menudo son la única forma
de detectarlos.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "log", "dontlognull", "errorfile" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-http-keep-alive"></a>

**`option http-keep-alive`**

```haproxy
option http-keep-alive
no option http-keep-alive
```

Habilita o deshabilita HTTP keep-alive de cliente a servidor para conexiones HTTP/1.x

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Por defecto, HAProxy opera en modo keep-alive con respecto a las conexiones HTTP/1.x persistentes:
por cada conexión procesa cada solicitud y respuesta, y deja la conexión inactiva en ambos lados.
Este modo puede cambiarse con varias opciones como "option http-server-close" o "option httpclose".
Esta opción permite restablecer el modo keep-alive, lo que puede ser útil cuando se usó otro modo en
una sección defaults.

Establecer "option http-keep-alive" habilita el modo HTTP keep-alive en los lados de cliente y
servidor. Esto proporciona la latencia más baja en el lado del cliente (red lenta) y la reutilización
de sesión más rápida en el lado del servidor a costa de mantener conexiones inactivas a los
servidores. En general, con esta opción es posible alcanzar aproximadamente el doble de la tasa de
solicitudes que alcanza la opción "http-server-close" en objetos pequeños. Hay principalmente dos
situaciones donde esta opción puede ser útil:

    - cuando el servidor no cumple HTTP y autentica la conexión en lugar de
      las solicitudes (p. ej., autenticación NTLM)

    - cuando el coste de establecer la conexión al servidor es significativo
      comparado con el coste de recuperar del servidor el objeto asociado.

Este último caso puede ocurrir cuando el servidor es un servidor estático o caché rápido.

Por el momento, los registros no indicarán si las solicitudes provinieron o no de la misma sesión. La
fecha de aceptación informada en los registros corresponde al final de la solicitud anterior, y el
tiempo de solicitud corresponde al tiempo pasado esperando una nueva solicitud. El tiempo de
solicitud keep-alive sigue ligado al timeout definido por "timeout http-keep-alive" o "timeout
http-request" si no se establece.

Esta opción deshabilita y reemplaza cualquier "option httpclose" o "option http-server-close"
anterior.

Ver también: "option httpclose",, "option http-server-close", "option prefer-last-server" y "option
http-pretend-keepalive".


<a id="entry-4-2-option-http-no-delay"></a>

**`option http-no-delay`**

```haproxy
option http-no-delay
no option http-no-delay
```

Indica al sistema que favorezca los retardos interactivos bajos frente al rendimiento en HTTP

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

En HTTP, cada carga útil es unidireccional y no tiene noción de interactividad. Se espera que
cualquier agente ponga los datos en cola hasta cierto punto para lograr un retardo razonablemente
bajo. Existen algunas aplicaciones servidor-a-servidor muy raras que abusan del protocolo HTTP y
esperan que la fase de carga útil sea altamente interactiva, con muchos fragmentos de datos
intercalados en ambas direcciones dentro de una sola solicitud. Esto no está en absoluto soportado
por la especificación HTTP y no funcionará a través de la mayoría de proxies o servidores. Cuando
tales aplicaciones intentan hacerlo a través de HAProxy, funciona, pero experimentarán retardos
altos debido a las optimizaciones de red que favorecen el rendimiento indicando al sistema que
espere a que haya suficientes datos disponibles para enviar solo paquetes completos. Los retardos
típicos rondan los 200 ms por recorrido de ida y vuelta. Ten en cuenta que esto solo ocurre con usos
anormales. Los usos normales, como las solicitudes CONNECT o los WebSockets, no se ven afectados.

Cuando "option http-no-delay" está presente en el frontend o en el backend usado por una conexión,
todas esas optimizaciones se deshabilitarán para hacer los intercambios tan rápidos como sea
posible. Por supuesto, esto no ofrece ninguna garantía sobre la funcionalidad, ya que puede romperse
en cualquier otro lugar. Pero si funciona vía HAProxy, funcionará tan rápido como sea posible. Esta
opción nunca debería usarse por defecto, y no debería usarse en absoluto salvo que se descubra tal
aplicación defectuosa. El impacto de usar esta opción es un aumento del uso de ancho de banda y de
CPU, lo que puede reducir significativamente el rendimiento en entornos de alta latencia.

Ver también: "option http-buffer-request"

<a id="entry-4-2-option-http-pretend-keepalive"></a>

**`option http-pretend-keepalive`**

```haproxy
option http-pretend-keepalive
no option http-pretend-keepalive
```

Define si HAProxy anunciará o no keepalive para la conexión HTTP/1.x al servidor

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando se ejecuta con "option http-server-close" o "option httpclose", HAProxy añade una cabecera
"Connection: close" a la solicitud HTTP/1.x reenviada al servidor. Desafortunadamente, cuando
algunos servidores ven esta cabecera, se abstienen automáticamente de usar la codificación por
fragmentos (chunked) para respuestas de longitud desconocida, aunque esto no tiene nada que ver. El
efecto es que un cliente o una caché podrían recibir una respuesta incompleta sin ser conscientes de ello, y considerar la respuesta completa.

Al establecer "option http-pretend-keepalive", HAProxy hará creer al servidor que mantendrá la
conexión viva. El servidor entonces no recurrirá al comportamiento anormal no deseado descrito
arriba. Cuando HAProxy recibe toda la respuesta, cerrará la conexión con el servidor igual que
haría con "option httpclose". De ese modo el cliente obtiene una respuesta normal y la conexión se
cierra correctamente en el lado del servidor.

Se recomienda no habilitar esta opción por defecto, porque la mayoría de los servidores cerrarán la
conexión por sí mismos de forma más eficiente tras el último paquete, y liberarán sus búferes algo
antes. Además, el paquete añadido en la red podría reducir ligeramente el rendimiento máximo global.
Sin embargo, vale la pena señalar que cuando esta opción está habilitada, HAProxy tendrá ligeramente
menos trabajo que hacer. Así que si HAProxy es el cuello de botella de toda la arquitectura,
habilitar esta opción podría ahorrar algunos ciclos de CPU.

Esta opción puede establecerse en las secciones backend y listen. Usarla en una sección frontend
será ignorado y se informará de un aviso durante el arranque. Es una opción relacionada con el
backend, así que no hay una razón real para establecerla en un frontend.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option httpclose", "option http-server-close" y "option http-keep-alive"

<a id="entry-4-2-option-http-restrict-req-hdr-names"></a>

**`option http-restrict-req-hdr-names { preserve | delete | reject }`**

```haproxy
option http-restrict-req-hdr-names { preserve | delete | reject }
```

Establece la política de HAProxy sobre los nombres de cabecera de solicitud HTTP que contienen
caracteres fuera del conjunto de caracteres "[a-zA-Z0-9-]"

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
preserve  desactiva el filtrado. Es el modo por defecto para los proxies
          HTTP sin ninguna aplicación FastCGI configurada.

delete    elimina las cabeceras de solicitud cuyo nombre contenga un
          carácter fuera del juego de caracteres "[a-zA-Z0-9-]". Es el
          modo por defecto para los backends HTTP con una aplicación
          FastCGI configurada.

reject    rechaza la solicitud con una respuesta 403-Forbidden si contiene
          un nombre de cabecera con un carácter fuera del juego de
          caracteres "[a-zA-Z0-9-]".
```

Esta opción puede usarse para restringir los nombres de cabecera de solicitud a caracteres
alfanuméricos y al guion ([A-Za-z0-9-]). Esto puede ser obligatorio para interoperar con servidores
que no cumplen HTTP y que fallan al gestionar algunos caracteres en los nombres de cabecera. También
puede ser obligatorio para aplicaciones FastCGI porque todos los caracteres no alfanuméricos de los
nombres de cabecera se reemplazan por un guion bajo ('\_'). Así, es fácilmente posible confundir
nombres de cabecera y eludir algunas reglas. Por ejemplo, las cabeceras "X-Forwarded-For" y
"X_Forwarded-For" se convierten ambas en "HTTP_X_FORWARDED_FOR" en FastCGI.

Ten en cuenta que esta opción se evalúa por proxy y después de la evaluación de las reglas
http-request.

<a id="entry-4-2-option-http-server-close"></a>

**`option http-server-close`**

```haproxy
option http-server-close
no option http-server-close
```

Habilita o deshabilita el cierre de conexiones HTTP/1.x en el lado del servidor

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Por defecto, HAProxy opera en modo keep-alive con respecto a las conexiones HTTP/1.x persistentes:
por cada conexión procesa cada solicitud y respuesta, y deja la conexión inactiva en ambos lados.
Este modo puede cambiarse con varias opciones como "option http-server-close" o "option httpclose".
Establecer "option http-server-close" habilita el modo de cierre de conexión HTTP en el lado del
servidor conservando la capacidad de soportar HTTP keep-alive y pipelining en el lado del cliente.
Esto proporciona la latencia más baja en el lado del cliente (red lenta) y la reutilización de sesión
más rápida en el lado del servidor para ahorrar recursos del servidor, de forma similar a "option
httpclose". También permite que servidores sin capacidad de keep-alive se sirvan en modo keep-alive
a los clientes si cumplen los requisitos de RFC7230. Ten en cuenta que algunos servidores no siempre
cumplen esos requisitos cuando ven "Connection: close" en la solicitud. El efecto será que el
keep-alive nunca se usará. Una solución consiste en habilitar "option http-pretend-keepalive".

Por el momento, los registros no indicarán si las solicitudes provinieron o no de la misma sesión.
La fecha de aceptación informada en los registros corresponde al final de la solicitud anterior, y
el tiempo de solicitud corresponde al tiempo pasado esperando una nueva solicitud. El tiempo de
solicitud keep-alive sigue ligado al timeout definido por "timeout http-keep-alive" o "timeout
http-request" si no se establece.

Esta opción puede establecerse tanto en un frontend como en un backend. Está habilitada si al menos
uno del frontend o backend que mantiene una conexión la tiene habilitada. Deshabilita y reemplaza
cualquier "option httpclose" o "option http-keep-alive" anterior. Consulta la [sección 4](/es/haproxy/proxies/)
("Proxies") para ver cómo se combina esta opción con otras cuando las opciones del frontend y del
backend difieren.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option httpclose", "option http-pretend-keepalive" y "option http-keep-alive".

<a id="entry-4-2-option-http-use-proxy-header"></a>

**`option http-use-proxy-header`**

```haproxy
option http-use-proxy-header
no option http-use-proxy-header
```

Usa la cabecera no estándar Proxy-Connection en lugar de Connection

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Aunque RFC7230 establece explícitamente que los agentes HTTP/1.1 deben usar la cabecera Connection
para indicar su deseo de conexiones persistentes o no persistentes, tanto los navegadores como los
proxies ignoran esta cabecera para las conexiones con proxy y usan en su lugar la cabecera no
documentada y no estándar Proxy-Connection. El problema comienza al intentar poner un balanceador de
carga entre navegadores y tales proxies, porque habrá una diferencia entre lo que HAProxy entiende y
lo que el cliente y el proxy acuerdan.

Al establecer esta opción en un frontend, HAProxy puede cambiar automáticamente a usar esa cabecera
no estándar si ve solicitudes con proxy. Una solicitud con proxy se define aquí como aquella cuyo
URI no comienza ni por '/' ni por '\*'. Esto es incompatible con el modo túnel HTTP. Ten en cuenta
que esta opción solo puede especificarse en un frontend y afectará a la solicitud durante toda su
vida.

Además, cuando esta opción está establecida, una solicitud que requiere autenticación cambiará
automáticamente a usar cabeceras de autenticación de proxy si es en sí misma una solicitud con
proxy. Eso hace posible comprobar o imponer la autenticación delante de un proxy existente.

Esta opción normalmente nunca debería usarse, excepto delante de un proxy.

Ver también: "option httpclose" y "option http-server-close".

<a id="entry-4-2-option-httpchk"></a>

**`option httpchk`**

```haproxy
option httpchk
option httpchk <uri>
option httpchk <method> <uri>
option httpchk <method> <uri> <version>
option httpchk <method> <uri> <version> <host>
```

Habilita el protocolo HTTP para comprobar la salud de los servidores

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<method>  es el método HTTP opcional usado con las solicitudes. Cuando no
          se establece, se usa el método "OPTIONS", ya que generalmente
          requiere poco procesamiento en el servidor y es fácil de
          filtrar de los registros. Puede usarse cualquier método,
          aunque no se recomienda inventar métodos no estándar.

<uri>     es el URI referenciado en las solicitudes HTTP. Por defecto es
          " / ", accesible por defecto en casi cualquier servidor, pero
          puede cambiarse a cualquier otro URI. Se permiten cadenas de
          consulta.

<version> es la cadena opcional de versión HTTP. Por defecto es
          "HTTP/1.0", pero algunos servidores pueden comportarse de forma
          incorrecta en HTTP 1.0, así que cambiarla a HTTP/1.1 puede
          ayudar a veces. Ten en cuenta que el campo Host es obligatorio
          en HTTP/1.1.

<host>    es el valor opcional de la cabecera HTTP Host. No se establece
          por defecto. Es una cadena log-format.
```

Por defecto, las comprobaciones de estado de los servidores solo consisten en intentar establecer
una conexión TCP. Cuando se especifica "option httpchk", se envía una solicitud HTTP completa una
vez establecida la conexión TCP, y las respuestas 2xx y 3xx se consideran válidas, mientras que
todas las demás indican un fallo del servidor, incluida la ausencia de respuesta.

Combinada con directivas "http-check", es posible personalizar la solicitud enviada durante las
comprobaciones de estado HTTP o las reglas de coincidencia sobre la respuesta. También es posible
configurar una secuencia send/expect, igual que con la directiva "tcp-check" para comprobaciones de
estado TCP.

La configuración del servidor se usa por defecto para abrir conexiones y realizar comprobaciones de
estado HTTP. Pero también es posible sobrescribir los parámetros del servidor usando reglas
"http-check connect".

La opción "httpchk" no requiere necesariamente un backend HTTP; también funciona con backends TCP
simples. Esto es particularmente útil para comprobar scripts simples ligados a algunos puertos
dedicados usando el demonio inetd. Sin embargo, siempre dependerá internamente de un multiplexor
HTX. Así, esto significa que el formateo de la solicitud y el análisis de la respuesta serán
estrictos.

Ejemplos:

```shell
# Relay HTTPS traffic to Apache instance and check service availability
# using HTTP request "OPTIONS * HTTP/1.1" on port 80.
backend https_relay
    mode tcp
    option httpchk OPTIONS * HTTP/1.1
    http-check send hdr Host www
    server apache1 192.168.1.1:443 check port 80
```

Ver también: "option ssl-hello-chk", "option smtpchk", "option mysql-check", "option pgsql-check",
"http-check" y las opciones de servidor "check", "port" e "inter".

<a id="entry-4-2-option-httpclose"></a>

**`option httpclose`**

```haproxy
option httpclose
no option httpclose
```

Habilita o deshabilita el cierre de conexiones HTTP/1.x

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Por defecto, HAProxy opera en modo keep-alive con respecto a las conexiones HTTP/1.x persistentes:
por cada conexión procesa cada solicitud y respuesta, y deja la conexión inactiva en ambos lados.
Este modo puede cambiarse con varias opciones como "option http-server-close" o "option
httpclose".

Si se establece "option httpclose", HAProxy cerrará la conexión del cliente o la del servidor,
dependiendo de dónde se establezca la opción. El frontend se considera para las conexiones de
cliente mientras que el backend se considera para las de servidor. Si la opción se establece en un
listener, se aplica tanto en las conexiones de cliente como de servidor. Comprobará si ya hay una
cabecera "Connection: close" establecida en cada dirección, y añadirá una si falta.

Esta opción también puede combinarse con "option http-pretend-keepalive", que deshabilitará el envío
de la cabecera de solicitud "Connection: close", pero seguirá causando el cierre de la conexión una
vez recibida toda la respuesta.

Deshabilita y reemplaza cualquier "option http-server-close" o "option http-keep-alive" anterior.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option http-server-close".

<a id="entry-4-2-option-httplog"></a>

**`option httplog [ clf ]`**

```haproxy
option httplog [ clf ]
```

Habilita el registro de la solicitud HTTP, el estado del flujo y los temporizadores

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
clf       si se añade el argumento "clf", el formato de salida será el
          formato CLF en lugar del formato HTTP por defecto de HAProxy.
          Puedes usarlo cuando necesites alimentar los registros de
          HAProxy a través de un analizador de registros específico que
          solo soporte el formato CLF y que no sea extensible.
```

Por defecto, el formato de salida del registro es muy pobre, ya que solo contiene las direcciones de
origen y destino, y el nombre de la instancia. Al especificar "option httplog", cada línea de
registro se convierte en un formato mucho más rico que incluye, entre otras cosas, la solicitud
HTTP, los temporizadores de conexión, el estado del flujo, los números de conexiones, las cabeceras
y cookies capturadas, el nombre del frontend, backend y servidor, y por supuesto la dirección y
puertos de origen.

Especificar solo "option httplog" borrará automáticamente el modo 'clf' si estaba establecido por
defecto.

"option httplog" prevalece sobre cualquier directiva "log-format" anterior.

Ver también: la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-httpslog"></a>

**`option httpslog`**

```haproxy
option httpslog
```

Habilita el registro de la solicitud HTTPS, el estado del flujo y los temporizadores

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Por defecto, el formato de salida del registro es muy pobre, ya que solo contiene las direcciones de
origen y destino, y el nombre de la instancia. Al especificar "option httpslog", cada línea de
registro se convierte en un formato mucho más rico que incluye, entre otras cosas, la solicitud
HTTP, los temporizadores de conexión, el estado del flujo, los números de conexiones, las cabeceras
y cookies capturadas, el nombre del frontend, backend y servidor, la verificación del certificado
SSL y los estados del intercambio SSL, y por supuesto la dirección y puertos de origen.

"option httpslog" prevalece sobre cualquier directiva "log-format" anterior.

Ver también: la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-idle-close-on-response"></a>

**`option idle-close-on-response`**

```haproxy
option idle-close-on-response
no option idle-close-on-response
```

Evita el cierre de conexiones inactivas del frontend si hay una parada suave en curso

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Por defecto, las conexiones inactivas se cerrarán durante una parada suave. En algunos entornos, un
cliente que habla con el proxy puede haber preparado algunas conexiones inactivas para enviar
solicitudes más tarde. Si no hay un reintento adecuado en errores de escritura, esto puede dar como
resultado errores mientras haproxy se está recargando. Aunque una implementación adecuada debería
reintentar ante errores de conexión/escritura, esta opción se introdujo para soportar la
compatibilidad hacia atrás con haproxy anterior a la versión 2.4. En efecto, antes de v2.4, haproxy
solía esperar una última solicitud y respuesta para añadir una cabecera "connection: close" antes de
cerrar, notificando así al cliente que la conexión no sería reutilizable.

En un ejemplo de la vida real, este comportamiento se vio en AWS usando un ALB delante de un
haproxy. El resultado final fue el ALB enviando 502 durante las recargas de haproxy.

Se advierte a los usuarios que usar esta opción puede aumentar el número de procesos antiguos si las
conexiones permanecen inactivas demasiado tiempo. Puede ser necesario ajustar los timeouts de
cliente y/o el parámetro "hard-stop-after" en consecuencia en caso de recargas frecuentes.

Ver también: "timeout client", "timeout client-fin", "timeout http-request", "hard-stop-after"

<a id="entry-4-2-option-independent-streams"></a>

**`option independent-streams`**

```haproxy
option independent-streams
no option independent-streams
```

Habilita o deshabilita el procesamiento independiente de timeouts para ambas direcciones

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Por defecto, cuando se envían datos por un socket, se refrescan tanto el timeout de escritura como
el timeout de lectura de ese socket, porque consideramos que hay actividad en ese socket, y no
tenemos otro medio de adivinar si deberíamos recibir datos o no.

Aunque este comportamiento por defecto es deseable para casi todas las aplicaciones, existe una
situación donde es deseable deshabilitarlo, y refrescar solo el timeout de lectura si hay datos
entrantes. Esto ocurre en flujos con timeouts grandes y cantidades bajas de datos intercambiados,
como una sesión telnet. Si el servidor desaparece de repente, los datos de salida se acumulan en los
búferes de socket del sistema, ambos timeouts se refrescan correctamente, y no hay forma de saber
que el servidor no los recibe, así que no se agota el tiempo. Sin embargo, cuando el protocolo
subyacente siempre hace eco de los datos enviados, sería suficiente por sí mismo detectar el
problema usando el timeout de lectura. Ten en cuenta que este problema no ocurre con protocolos más
verbosos porque los datos no se acumulan mucho tiempo en los búferes del socket.

Cuando esta opción se establece en el frontend, deshabilitará las actualizaciones del timeout de
lectura sobre los datos enviados al cliente. Probablemente haya poco uso de este caso. Cuando la
opción se establece en el backend, deshabilitará las actualizaciones del timeout de lectura sobre
los datos enviados al servidor. Hacerlo normalmente romperá los posts HTTP grandes desde líneas
lentas, así que úsala con cautela.

Ver también: "timeout client", "timeout server" y "timeout tunnel"

<a id="entry-4-2-option-ldap-check"></a>

**`option ldap-check`**

```haproxy
option ldap-check
```

Usa comprobaciones de estado LDAPv3 para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Es posible comprobar que el servidor habla correctamente LDAPv3 en lugar de solo comprobar que
acepta la conexión TCP. Cuando se establece esta opción, se envía al servidor un mensaje de bind
simple anónimo LDAPv3, y la respuesta se analiza para encontrar un mensaje de respuesta de bind
LDAPv3.

El servidor se considera válido solo cuando la respuesta LDAP contiene un resultCode de éxito
(<http://tools.ietf.org/html/rfc4511#section-4.1.9>).

El registro de las solicitudes bind depende del servidor; consulta tu documentación sobre cómo
configurarlo.

Ejemplo:

```text
option ldap-check
```

Ver también: "option httpchk"

<a id="entry-4-2-option-log-health-checks"></a>

**`option log-health-checks`**

```haproxy
option log-health-checks
no option log-health-checks
```

Habilita o deshabilita el registro de las actualizaciones del estado de las comprobaciones de estado

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Por defecto, las comprobaciones de estado fallidas se registran si el servidor está UP y las
comprobaciones de estado correctas se registran si el servidor está DOWN, así que la cantidad de
información adicional es limitada.

Cuando esta opción está habilitada, cualquier cambio del estado de la comprobación de estado o de la
salud del servidor se registrará, de modo que sea posible saber que un servidor fallaba
comprobaciones ocasionales antes de caerse, o exactamente cuándo falló al responder un estado HTTP
válido, luego cuándo el puerto empezó a rechazar conexiones, y luego cuándo el servidor dejó de
responder por completo.

Ten en cuenta que los cambios de estado no causados por comprobaciones de estado (p. ej.,
habilitar/deshabilitar en la CLI) no se registran intencionadamente con esta opción.

Ver también: "option httpchk", "option ldap-check", "option mysql-check", "option pgsql-check",
"option redis-check", "option smtpchk", "option tcp-check", "log" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-log-separate-errors"></a>

**`option log-separate-errors`**

```haproxy
option log-separate-errors
no option log-separate-errors
```

Cambia el nivel de registro de las conexiones no completamente correctas

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

A veces buscar errores en los registros no es fácil. Esta opción hace que HAProxy eleve el nivel de
los registros que contienen información potencialmente interesante como errores, timeouts,
reintentos, reenvíos o códigos de estado HTTP 5xx. El nivel cambia de "info" a "err". Esto hace
posible registrarlos por separado en un archivo diferente con la mayoría de demonios syslog. Ten
cuidado de no eliminarlos del archivo original; de lo contrario, perderías el orden, que proporciona
información muy importante.

Usando esta opción, los sitios grandes que gestionan varios miles de conexiones por segundo pueden
registrar el tráfico normal en un búfer rotativo y archivar solo los registros de errores más
pequeños.

Ver también: "log", "dontlognull", "dontlog-normal" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.


<a id="entry-4-2-option-logasap"></a>

**`option logasap`**

```haproxy
option logasap
no option logasap
```

Habilita o deshabilita el registro temprano.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Por defecto, los registros se emiten cuando todos los alias de formato de registro y las obtenciones
de muestra usados en la definición de la cadena log-format devuelven un valor, o cuando el flujo
termina. Esto permite que las cadenas log-format integradas contabilicen el tiempo de transferencia
o el número de bytes en los mensajes de registro.

Al gestionar conexiones de larga vida como transferencias de archivos grandes o RDP, puede pasar un
rato hasta que la solicitud o conexión aparezca en los registros. Usando "option logasap", el
mensaje de registro se crea tan pronto como se establece la conexión al servidor en modo tcp, o tan
pronto como el servidor envía las cabeceras completas en modo http. La información que faltará en
los registros será el número total de bytes, que solo indicará la cantidad de datos transferidos
antes de que se creara el mensaje, y el tiempo total, que no tendrá en cuenta el resto de la vida de
la conexión ni el tiempo de transferencia. Para el caso de HTTP, es una buena práctica capturar la
cabecera de respuesta Content-Length para que los registros indiquen al menos cuántos bytes se
espera transferir.

Ejemplos:

```text
listen http_proxy 0.0.0.0:80
    mode http
    option httplog
    option logasap
    log 192.168.2.200 local3
```

```text
    >>> Feb  6 12:14:14 localhost \
          haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
          static/srv1 9/10/7/14/+30 200 +243 - - ---- 3/1/1/1/0 1/0 \
          "GET /image.iso HTTP/1.0"
```

Ver también: "option httplog", "capture response header" y la [sección 8](/es/haproxy/configuration-logging/) acerca del registro.

<a id="entry-4-2-option-mysql-check"></a>

**`option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]`**

```haproxy
option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]
```

Usa comprobaciones de estado MySQL para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<username> Es el nombre de usuario que se usará al conectar con el servidor
           MySQL.
post-41    Envía comprobaciones compatibles con clientes posteriores a v4.1
           (el valor por defecto)
pre-41     Envía comprobaciones compatibles con clientes anteriores a v4.1
post-80    Envía comprobaciones compatibles con clientes posteriores a v8.0,
           con la capacidad CLIENT_PLUGIN_AUTH establecida y
           mysql_native_password como plugin de autenticación. Usa esta
           opción al conectar con servidores MySQL 8.0+ donde el usuario
           de la comprobación de estado se crea con autenticación
           mysql_native_password. Ejemplo:
             CREATE USER 'haproxy'@'%' IDENTIFIED WITH mysql_native_password BY '';
```

Si especificas un nombre de usuario, la comprobación consiste en enviar dos paquetes MySQL, un
paquete Client Authentication y un paquete QUIT, para cerrar correctamente la sesión MySQL. Luego
analizamos el paquete MySQL Handshake Initialization y/o el paquete Error. Es una prueba básica
pero útil que no produce error ni conexión abortada en el servidor. Sin embargo, requiere un
usuario autorizado sin bloquear y sin contraseña. Para crear un usuario básico limitado en MySQL
con límites de recursos opcionales:

```text
CREATE USER '<username>'@'<ip_of_haproxy|network_of_haproxy/netmask>'
/*!50701 WITH MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 0 */
/*M!100201 MAX_STATEMENT_TIME 0.0001 */;
```

Si no especificas un nombre de usuario (está obsoleto y no se recomienda), la comprobación solo
consiste en analizar el paquete Mysql Handshake Initialization o el paquete Error; no enviamos nada
en este modo. Se informó de que puede generar bloqueo si la comprobación es demasiado frecuente
y/o si no hay tráfico suficiente. De hecho, en este caso necesitas comprobar el valor
"max_connect_errors" de MySQL, ya que si una conexión se establece con éxito en menos de
"max_connect_errors" intentos de MySQL tras interrumpirse una conexión previa, el contador de
errores del host se pone a cero. Si el servidor de HAProxy queda bloqueado, la sentencia
"FLUSH HOSTS" es la única forma de desbloquearlo.

Recuerda que esto no comprueba la presencia de la base de datos ni su consistencia. Para ello,
puedes usar una comprobación externa con xinetd, por ejemplo.

La comprobación requiere MySQL \>=3.22; para versiones más antiguas, usa la comprobación TCP.

Muy a menudo, un servidor MySQL entrante necesita ver la dirección IP del cliente para varios
propósitos, incluida la coincidencia de privilegios de IP y el registro de conexiones. Cuando es
posible, a menudo es prudente usar la dirección IP del cliente como dirección de origen al conectar con el servidor
usando el argumento "usesrc" de la palabra clave "source", lo que requiere que la función de proxy
transparente esté compilada y que el servidor MySQL enrute al cliente vía la máquina que aloja
HAProxy.

Ver también: "option httpchk"

<a id="entry-4-2-option-nolinger"></a>

**`option nolinger`**

```haproxy
option nolinger
no option nolinger
```

Habilita o deshabilita la limpieza inmediata de los recursos de la sesión tras el cierre

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Cuando los clientes o servidores abortan conexiones de forma sucia (p. ej., se desconectan
físicamente), se disparan los timeouts de sesión y la sesión se cierra. Pero permanecerá en estado
FIN_WAIT1 durante algún tiempo en el sistema, usando algunos recursos y posiblemente limitando la
capacidad de establecer conexiones más nuevas.

Cuando esto ocurre, es posible activar "option nolinger", que fuerza al sistema a eliminar
inmediatamente cualquier dato pendiente del socket al cerrar. Así, se emite un TCP RST, cualquier
dato pendiente se trunca, y la sesión se purga al instante de las tablas del sistema. El efecto
generalmente visible para un cliente es que las respuestas se truncan si el cierre ocurre con un
último bloque de datos (p. ej., en una respuesta de redirección o de error). En el lado del
servidor, puede ayudar a liberar inmediatamente los puertos de origen al propagar por los túneles la interrupción de una conexión por parte del cliente. En ambos casos, se emiten resets TCP y, dado que la sesión se
destruye al instante, no habrá retransmisión. En una red con pérdidas esto puede aumentar los
problemas, especialmente cuando hay un cortafuegos en el lado con pérdidas, porque el cortafuegos
podría ver y procesar el reset (y por tanto purgar su sesión) y bloquear cualquier tráfico
posterior para esta sesión,, incluidas las retransmisiones del otro lado. Así que si el otro lado
no lo recibe, nunca volverá a recibir ningún RST, y el cortafuegos podría registrar muchos paquetes
bloqueados.

Por todas estas razones, se recomienda encarecidamente NO usar esta opción, salvo que sea
absolutamente necesaria como último recurso. En la mayoría de las situaciones, usar los timeouts
"client-fin" o "server-fin" logra resultados similares con un comportamiento más fiable. En Linux
también es posible usar el ajuste de bind o servidor "tcp-ut".

Esta opción puede usarse tanto en frontends como en backends, dependiendo del lado donde se
requiera. Úsala en el frontend para los clientes, y en el backend para los servidores. Aunque esta
opción está técnicamente soportada en secciones "defaults", realmente no debe usarse allí, ya que
corre el riesgo de propagarse accidentalmente a secciones que no deben usarla y causar problemas.

Si esta opción se ha habilitado en una sección "defaults", puede deshabilitarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "timeout client-fin", "timeout server-fin", palabras clave de bind o servidor "tcp-ut".

<a id="entry-4-2-option-originalto"></a>

**`option originalto [ except <network> ] [ header <name> ]`**

```haproxy
option originalto [ except <network> ] [ header <name> ]
```

Habilita la inserción de la cabecera X-Original-To en las solicitudes enviadas a los servidores

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<network> es un argumento opcional usado para desactivar esta opción para las
          fuentes que coincidan con <network>
<name>    un argumento opcional para especificar un nombre de cabecera
          distinto para "X-Original-To".
```

Como HAProxy puede trabajar en modo transparente, cada solicitud de un cliente puede ser redirigida
al proxy y el propio HAProxy puede hacer de proxy de cada solicitud hacia un entorno SQUID
complejo, y el host de destino de SO_ORIGINAL_DST se perderá. Esto resulta molesto cuando quieres
reglas de acceso basadas en direcciones IP de destino. Para resolver este problema, HAProxy puede
añadir una nueva cabecera HTTP "X-Original-To" a todas las solicitudes enviadas al servidor. Esta
cabecera contiene un valor que representa la dirección IP de destino original. Dado esto, debe
configurarse para usar siempre solo la última aparición de esta cabecera. Ten en cuenta que solo
debe usarse la última aparición de la cabecera, ya que es realmente posible que el cliente ya haya
traído una.

La palabra clave "header" puede usarse para suministrar un nombre de cabecera diferente que
reemplace la "X-Original-To" por defecto. Esto puede ser útil cuando ya podrías tener una cabecera
"X-Original-To" de una aplicación diferente y necesitas conservarla. También si tu servidor del
backend no usa la cabecera "X-Original-To" y requiere otra diferente.

A veces, una misma instancia de HAProxy puede compartirse entre un acceso directo de clientes y un
acceso de proxy inverso (por ejemplo cuando se usa un proxy inverso SSL para descifrar el tráfico
HTTPS). Es posible deshabilitar la adición de la cabecera para una dirección o red de destino
conocida añadiendo la palabra clave "except" seguida de la dirección de red. En este caso, cualquier
IP de destino que coincida con la red no provocará la adición de esta cabecera. Los usos más
comunes son con redes privadas o 127.0.0.1. Se soportan tanto IPv4 como IPv6.

Esta opción puede especificarse en el frontend o en el backend. Si al menos uno de ellos la usa, la
cabecera se añadirá. Ten en cuenta que el ajuste del subargumento header del backend prevalece
sobre el del frontend si ambos están definidos.

Ejemplos:

```shell
# Original Destination address
frontend www
    mode http
    option originalto except 127.0.0.1

# Those servers want the IP Address in X-Client-Dst
backend www
    mode http
    option originalto header X-Client-Dst
```

Ver también: "option httpclose", "option http-server-close".

<a id="entry-4-2-option-persist"></a>

**`option persist`**

```haproxy
option persist
no option persist
```

Activa o desactiva la persistencia forzada en servidores caídos

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando una solicitud HTTP llega a un backend con una cookie que hace referencia a un servidor
caído, por defecto se redistribuye a otro servidor. Es posible forzar el envío de la solicitud al
servidor caído primero usando "option persist" si es absolutamente necesario. Un caso de uso común
es cuando los servidores están bajo una carga extrema y pasan el tiempo oscilando entre estados. En
este caso, los usuarios seguirían siendo dirigidos al servidor en el que abrieron la sesión, con la
esperanza de ser atendidos correctamente. Se recomienda usar "option redispatch" junto con esta
opción para que, en el caso de que no fuera posible conectarse en absoluto al servidor (servidor
definitivamente muerto), el cliente finalmente sea redirigido a otro servidor válido.

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option redispatch", "retries", "force-persist"

<a id="entry-4-2-option-pgsql-check-user"></a>

**`option pgsql-check user <username>`**

```haproxy
option pgsql-check user <username>
```

Usa comprobaciones de estado PostgreSQL para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<username> Es el nombre de usuario que se usará al conectarse al
           servidor PostgreSQL.
```

La comprobación envía un StartupMessage de PostgreSQL y espera una solicitud de autenticación o un
mensaje ErrorResponse. Es una prueba básica pero útil que no produce errores ni conexiones
abortadas en el servidor. Esta comprobación es idéntica a "mysql-check".

Ver también: "option httpchk"

<a id="entry-4-2-option-prefer-last-server"></a>

**`option prefer-last-server`**

```haproxy
option prefer-last-server
no option prefer-last-server
```

Permite que múltiples solicitudes balanceadas permanezcan en el mismo servidor

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando el algoritmo de balanceo de carga en uso no es determinista, y una solicitud anterior se
envió a un servidor del cual HAProxy aún conserva una conexión, a veces es deseable que las
solicitudes posteriores de una misma sesión vayan al mismo servidor tanto como sea posible. Ten en
cuenta que esto es diferente de la persistencia, ya que solo se indica una preferencia que HAProxy
intenta aplicar sin ningún tipo de garantía. Su uso real es para conexiones keep-alive enviadas a
los servidores. Cuando se usa esta opción, HAProxy intentará reutilizar la misma conexión asociada
al servidor en lugar de rebalancear hacia otro servidor, lo que provocaría el cierre de la conexión.
Esto puede tener sentido para servidores de archivos estáticos. No tiene mucho sentido usarla en
combinación con algoritmos de hash. Ten en cuenta que HAProxy ya intenta automáticamente mantenerse
en un servidor que envía un 401 o en un proxy que envía un 407 (autenticación requerida), cuando el
algoritmo de balanceo de carga no es determinista. Esto es obligatorio para su uso con el desafío
de autenticación NTLM defectuoso, y ayuda significativamente a diagnosticar algunas aplicaciones
defectuosas. La opción prefer-last-server también puede ser deseable en estos entornos, para evitar
redistribuir el tráfico después de cualquier otra respuesta.

Puede ser útil precisar aquí qué algoritmos de balanceo de carga se consideran deterministas. Los
algoritmos deterministas siempre seleccionarán el mismo servidor para unos datos de cliente dados,
suponiendo que el conjunto de servidores disponibles no haya cambiado. En general, los algoritmos
deterministas implican hash o búsquedas sobre las solicitudes entrantes para elegir el servidor de
destino. Sin embargo, no siempre es el caso; "static-rr", por ejemplo, también puede considerarse
determinista porque la elección del servidor se basa en el peso estático del servidor, lo que hace
la selección predecible. El algoritmo "sticky" proporciona enrutamiento determinista para los
clientes que regresan.

En cuanto a los algoritmos no deterministas, estos seleccionan un servidor basándose en el estado
dinámico del servidor o en una simple rotación, por lo que no está garantizado que dos solicitudes
consecutivas caigan en el mismo servidor. option prefer-last-server está diseñado
específicamente para estos. roundrobin y leastconn son ejemplos de tales algoritmos.

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option http-keep-alive"

<a id="entry-4-2-option-redispatch"></a>

**`option redispatch`**

```haproxy
option redispatch
option redispatch <interval>
no option redispatch
```

Activa o desactiva la redistribución de sesiones en caso de fallo de conexión

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<interval> El valor entero opcional que controla con qué frecuencia ocurren
           las redistribuciones al reintentar conexiones. Un valor positivo P
           indica que se desea una redistribución en cada P-ésimo reintento,
           y un valor negativo N indica que se desea en el N-ésimo reintento
           previo al último. Por ejemplo, el valor por defecto de -1 conserva
           el comportamiento histórico de redistribuir en el último reintento,
           un valor positivo de 1 indicaría una redistribución en cada
           reintento, y un valor positivo de 3 indicaría una en cada tercer
           reintento. Puedes desactivar las redistribuciones con el valor 0.

```

En modo HTTP, si un servidor designado por una cookie está caído, los clientes pueden quedar
definitivamente pegados a él, por ejemplo al usar "option persist" o "force-persist", porque no
pueden descartar la cookie, por lo que ya no podrán acceder al servicio.

Especificar "option redispatch" permitirá al proxy romper la persistencia basada en cookies o en
hash consistente y redistribuir a los clientes a un servidor funcional.

Los servidores activos se seleccionan de un subconjunto de la lista de servidores disponibles.
Los servidores activos que no están caídos ni en mantenimiento (es decir, cuya salud no se
comprueba o que se han comprobado como "up") se seleccionan en el siguiente orden:

```text
1. Cualquier servidor activo que no sea de respaldo, si existe, o:

2. Si la opción "allbackups" no está establecida, el primer servidor de
   respaldo de la lista, o:

3. Si la opción "allbackups" está establecida, cualquier servidor de respaldo.
```

Cuando ocurre un reintento, HAProxy intenta seleccionar otro servidor distinto del último. El
nuevo servidor se selecciona de la lista actual de servidores.

A veces, si la lista se actualiza entre reintentos (p. ej., si ocurren numerosos reintentos que
duran más que el tiempo necesario para comprobar que un servidor está caído, eliminarlo de la
lista y recurrir a la lista de servidores de respaldo), las conexiones pueden acabar redirigidas a
un servidor de respaldo.

También permite reintentar conexiones a otro servidor en caso de múltiples fallos de conexión.
Por supuesto, requiere que "retries" esté establecido a un valor distinto de cero.

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option persist", "force-persist", "retries"

<a id="entry-4-2-option-redis-check"></a>

**`option redis-check`**

```haproxy
option redis-check
```

Usa comprobaciones de estado redis para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Es posible comprobar que el servidor habla correctamente el protocolo REDIS en lugar de solo
comprobar que acepta la conexión TCP. Cuando se establece esta opción, se envía un comando redis
PING al servidor, y se analiza la respuesta para encontrar el mensaje de respuesta "+PONG".

Ejemplo:

```text
option redis-check
```

Ver también: "option httpchk", "option tcp-check", "tcp-check expect"

<a id="entry-4-2-option-smtpchk"></a>

**`option smtpchk`**

```haproxy
option smtpchk
option smtpchk <hello> <domain>
```

Usa comprobaciones de estado SMTP para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<hello>   es un argumento opcional. Es el comando "hello" a usar. Puede ser
          "HELO" (para SMTP) o "EHLO" (para ESMTP). Todos los demás valores
          se convertirán en el comando por defecto ("HELO").

<domain>  es el nombre de dominio a presentar al servidor. Solo puede
          especificarse (y es obligatorio) si se ha especificado el comando
          hello. Por defecto se usa "localhost".
```

Cuando se establece "option smtpchk", las comprobaciones de estado consistirán en conexiones TCP
seguidas de un comando SMTP. Por defecto, este comando es "HELO localhost". Se analiza el código de
retorno del servidor y solo se considerarán válidos los códigos de retorno que comiencen por "2".
Todas las demás respuestas, incluida la ausencia de respuesta, constituirán un error e indicarán
un servidor muerto.

Esta prueba está pensada para usarse con servidores o relés SMTP. Según la solicitud, es posible
que algunos servidores no registren cada intento de conexión, por lo que puede convenir
experimentar para mejorar el comportamiento. Usar telnet en el puerto 25 suele ser más fácil que
ajustar la configuración.

Con frecuencia, un servidor SMTP entrante necesita ver la dirección IP del cliente con diversos
propósitos: filtrado de spam, anti-suplantación y registro. Cuando sea posible, suele ser
aconsejable usar la IP del cliente como dirección de origen al conectar con el servidor mediante el argumento
"usesrc" de la palabra clave "source", lo que requiere compilar el soporte de proxy transparente.

Ejemplo:

```text
option smtpchk HELO mydomain.org
```

Ver también: "option httpchk", "source"

```haproxy
option socket-stats
no option socket-stats
```

Activa o desactiva la recolección y provisión de estadísticas separadas para cada socket.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

<a id="entry-4-2-option-splice-auto"></a>

**`option splice-auto`**

```haproxy
option splice-auto
no option splice-auto
```

Activa o desactiva la aceleración automática del kernel en los sockets en ambas direcciones

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Cuando esta opción se activa en un frontend o en un backend, HAProxy evaluará automáticamente la
oportunidad de usar el splicing TCP del kernel para reenviar datos entre el cliente y el servidor,
en cualquiera de las direcciones. HAProxy usa heurísticas para estimar si el splicing del kernel
puede mejorar o no el rendimiento. Ambas direcciones se gestionan de forma independiente. Ten en
cuenta que las heurísticas usadas no son muy agresivas para limitar el uso excesivo del splicing.
Esta opción requiere que el splicing esté activado en tiempo de compilación y puede desactivarse
globalmente con la opción global "nosplice". Como splice usa pipes, su uso requiere que haya
suficientes pipes de repuesto.

Nota importante: el splicing TCP basado en kernel es una funcionalidad específica de Linux que
apareció por primera vez en el kernel 2.6.25. Ofrece aceleración basada en kernel para transferir
datos entre sockets sin copiarlos al espacio de usuario, proporcionando así notorias mejoras de
rendimiento y ahorro de ciclos de CPU. Como muchas implementaciones tempranas tienen errores,
corrompen datos y/o son ineficientes, esta funcionalidad no está activada por defecto y debe usarse
con extremo cuidado. Aunque no es posible detectar la corrección de una implementación, 2.6.29 es
la primera versión que ofrece una implementación que funciona correctamente. En caso de duda, el
splicing puede desactivarse globalmente usando la palabra clave global "nosplice".

Ejemplo:

```text
option splice-auto
```

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option splice-request", "option splice-response", y las opciones globales "nosplice" y
"maxpipes"

<a id="entry-4-2-option-splice-request"></a>

**`option splice-request`**

```haproxy
option splice-request
no option splice-request
```

Activa o desactiva la aceleración automática del kernel en los sockets para las solicitudes

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Cuando esta opción se activa en un frontend o en un backend, HAProxy usará el splicing TCP del
kernel siempre que sea posible para reenviar los datos que van del cliente al servidor. Aún podría
usar el esquema recv/send si no quedan pipes de repuesto. Esta opción requiere que el splicing esté
activado en tiempo de compilación y puede desactivarse globalmente con la opción global
"nosplice". Como splice usa pipes, su uso requiere que haya suficientes pipes de repuesto.

Nota importante: ver "option splice-auto" para las limitaciones de uso.

Ejemplo:

```text
option splice-request
```

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option splice-auto", "option splice-response", y las opciones globales "nosplice" y
"maxpipes"

<a id="entry-4-2-option-splice-response"></a>

**`option splice-response`**

```haproxy
option splice-response
no option splice-response
```

Activa o desactiva la aceleración automática del kernel en los sockets para las respuestas

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Cuando esta opción se activa en un frontend o en un backend, HAProxy usará el splicing TCP del
kernel siempre que sea posible para reenviar los datos que van del servidor al cliente. Aún podría
usar el esquema recv/send si no quedan pipes de repuesto. Esta opción requiere que el splicing esté
activado en tiempo de compilación y puede desactivarse globalmente con la opción global
"nosplice". Como splice usa pipes, su uso requiere que haya suficientes pipes de repuesto.

Nota importante: ver "option splice-auto" para las limitaciones de uso.

Ejemplo:

```text
option splice-response
```

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option splice-auto", "option splice-request", y las opciones globales "nosplice" y
"maxpipes"

<a id="entry-4-2-option-spop-check"></a>

**`option spop-check`**

```haproxy
option spop-check
```

Usa comprobaciones de estado SPOP para probar los servidores

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Es posible comprobar que el servidor habla correctamente el protocolo SPOP en lugar de solo
comprobar que acepta la conexión TCP. Cuando se establece esta opción, se efectúa un handshake
HELLO entre HAProxy y el servidor, y se analiza la respuesta para verificar que no se informe de
ningún error.

Ejemplo:

```text
option spop-check
```

Ver también: "option httpchk"

<a id="entry-4-2-option-srvtcpka"></a>

**`option srvtcpka`**

```haproxy
option srvtcpka
no option srvtcpka
```

Activa o desactiva el envío de paquetes TCP keepalive en el lado del servidor

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando hay un cortafuegos o cualquier componente consciente de sesiones entre un cliente y un
servidor, y cuando el protocolo implica sesiones muy largas con largos períodos de inactividad
(p. ej., escritorios remotos), existe el riesgo de que uno de los componentes intermedios decida
expirar una sesión que ha permanecido inactiva durante demasiado tiempo.

Activar los TCP keep-alive a nivel de socket hace que el sistema envíe paquetes regularmente al
otro extremo de la conexión, manteniéndola activa. El retardo entre sondas keep-alive lo controla
únicamente el sistema y depende tanto del sistema operativo como de sus parámetros de ajuste.

Es importante entender que los paquetes keep-alive no se emiten ni se reciben a nivel de
aplicación. Solo las pilas de red los ven. Por esta razón, aunque un lado del proxy ya use
keep-alives para mantener viva su conexión, esos paquetes keep-alive no se reenviarán al otro lado
del proxy.

Ten en cuenta que esto no tiene nada que ver con el keep-alive de HTTP.

Usar la opción "srvtcpka" activa la emisión de sondas TCP keep-alive en el lado del servidor de una
conexión, lo que debería ayudar cuando se notan expiraciones de sesión entre HAProxy y un servidor.

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option clitcpka", "option tcpka"

<a id="entry-4-2-option-ssl-hello-chk"></a>

**`option ssl-hello-chk`**

```haproxy
option ssl-hello-chk
```

Usa comprobaciones de estado SSLv3 client hello para probar los servidores

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Cuando algunos protocolos basados en SSL se retransmiten en modo TCP a través de HAProxy, es
posible comprobar que el servidor habla correctamente SSL en lugar de solo comprobar que acepta la
conexión TCP. Cuando se establece "option ssl-hello-chk", se envían mensajes puros SSLv3 client
hello una vez establecida la conexión con el servidor, y se analiza la respuesta para encontrar un
mensaje SSL server hello. El servidor se considera válido solo cuando la respuesta contiene este
mensaje server hello.

Todos los servidores probados hasta ahora responden correctamente a los mensajes SSLv3 client
hello, y la mayoría de los servidores probados ni siquiera registran las solicitudes que contienen
solo mensajes hello, lo cual es apreciable.

Ten en cuenta que esta comprobación funciona incluso cuando el soporte SSL no está compilado en
HAProxy, porque falsifica el mensaje SSL. Cuando el soporte SSL está disponible, es mejor usar
comprobaciones de estado SSL nativas en lugar de esta.

Ver también: "option httpchk", "check-ssl"

<a id="entry-4-2-option-tcp-check"></a>

**`option tcp-check`**

```haproxy
option tcp-check
```

Realiza comprobaciones de estado usando secuencias tcp-check send/expect

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Este método de comprobación de estado está pensado para combinarse con listas de comandos
"tcp-check" para soportar secuencias de comprobación de estado del tipo send/expect.

Las comprobaciones TCP actualmente soportan 4 modos de operación: - sin directiva "tcp-check": la
comprobación de estado consiste únicamente en un intento de conexión, que sigue siendo el modo por
defecto.

    - solo se menciona "tcp-check send" o "tcp-check send-binary": se usa
      para enviar una cadena junto con la apertura de una conexión. Con
      algunos protocolos, esto ayuda a enviar un mensaje "QUIT", por
      ejemplo, que evita que el servidor registre un error de conexión por
      cada comprobación de estado. El resultado de la comprobación seguirá
      basándose únicamente en la capacidad de abrir la conexión.

    - solo se menciona "tcp-check expect": se usa para probar un banner. La
      conexión se abre y HAProxy espera a que el servidor presente unos
      contenidos que deben validar algunas reglas. El resultado de la
      comprobación se basará en la coincidencia entre los contenidos y las
      reglas. Esto es adecuado para POP, IMAP, SMTP, FTP, SSH y TELNET.

    - se mencionan tanto "tcp-check send" como "tcp-check expect": se usa
      para probar un protocolo de tipo hello. HAProxy envía un mensaje, el
      servidor responde y su respuesta se analiza. El resultado de la
      comprobación se basará en la coincidencia entre los contenidos de la
      respuesta y las reglas. Esto suele ser adecuado para protocolos que
      requieren un enlace o un modelo solicitud/respuesta. LDAP, MySQL, Redis
      y SSL son ejemplos de tales protocolos, aunque todos ellos ya tienen
      sus comprobaciones dedicadas con una comprensión más profunda de los
      respectivos protocolos.
      En este modo, pueden enviarse muchas preguntas y analizarse muchas
      respuestas.

Un quinto modo puede usarse para insertar comentarios en diferentes pasos del script.

Para cada regla tcp-check que crees, puedes añadir una directiva "comment" seguida de una cadena.
Esta cadena se informará en el registro y en stderr en modo depuración. Es útil para generar
informes de errores fáciles de entender. La directiva "comment" es, por supuesto, opcional.

Durante la ejecución de una comprobación de estado, se pone a disposición un ámbito de variables
para almacenar muestras de datos, usando la operación "tcp-check set-var". Liberar esas variables
es posible usando "tcp-check unset-var".

Ejemplos:

```shell
# perform a POP check (analyze only server's banner)
option tcp-check
tcp-check expect string +OK\ POP3\ ready comment POP\ protocol

# perform an IMAP check (analyze only server's banner)
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready comment IMAP\ protocol

# look for the redis master server after ensuring it speaks well
# redis protocol, then it exits properly.
# (send a command then analyze the response 3 times)
option tcp-check
tcp-check comment PING\ phase
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check comment role\ check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check comment QUIT\ phase
tcp-check send QUIT\r\n
tcp-check expect string +OK

forjar una solicitud HTTP y luego analizar la respuesta
(enviar muchas cabeceras antes de analizar)
option tcp-check
tcp-check comment forge\ and\ send\ HTTP\ request
tcp-check send HEAD\ /\ HTTP/1.1\r\n
tcp-check send Host:\ www.mydomain.com\r\n
tcp-check send User-Agent:\ HAProxy\ tcpcheck\r\n
tcp-check send \r\n
tcp-check expect rstring HTTP/1\..\ (2..|3..) comment check\ HTTP\ response

```

Ver también: "tcp-check connect", "tcp-check expect" y "tcp-check send".

<a id="entry-4-2-option-tcp-smart-accept"></a>

**`option tcp-smart-accept`**

```haproxy
option tcp-smart-accept
no option tcp-smart-accept
```

Activa o desactiva el ahorro de un paquete ACK durante la secuencia de accept

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos: ninguno

Cuando entra una solicitud de conexión HTTP, el sistema acusa recibo de ella en nombre de HAProxy,
luego el cliente envía inmediatamente su solicitud, y el sistema también acusa recibo mientras
notifica a HAProxy sobre la nueva conexión. HAProxy entonces lee la solicitud y responde. Esto
significa que el sistema envía un TCP ACK para nada, porque la solicitud bien podría ser
reconocida por HAProxy cuando envía su respuesta.

Por esta razón, en modo HTTP, HAProxy pide automáticamente al sistema que evite enviar este ACK
inútil en las plataformas que lo soportan (actualmente, al menos Linux). No debe causar ningún
problema, porque el sistema lo enviará de todos modos después de 40 ms si la respuesta tarda más
de lo esperado en llegar.

Durante sesiones complejas de depuración de red, puede ser deseable desactivar esta optimización
porque los ACK retrasados pueden complicar la resolución de problemas cuando se intenta identificar
dónde se retrasan los paquetes. Es posible volver al comportamiento normal especificando "no
option tcp-smart-accept".

También es posible forzarlo para proxies no HTTP simplemente especificando "option
tcp-smart-accept". Por ejemplo, puede tener sentido con algunos servicios como SMTP donde el
servidor habla primero.

Se recomienda evitar forzar esta opción en una sección defaults. En caso de duda, considera
restablecerla a valores automáticos anteponiendo la palabra clave "default", o desactivarla usando
la palabra clave "no".

Ver también: "option tcp-smart-connect"

<a id="entry-4-2-option-tcp-smart-connect"></a>

**`option tcp-smart-connect`**

```haproxy
option tcp-smart-connect
no option tcp-smart-connect
```

Activa o desactiva el ahorro de un paquete ACK durante la secuencia de connect

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

En ciertos sistemas (al menos Linux), HAProxy puede pedir al kernel que no envíe inmediatamente
un ACK vacío tras una solicitud de conexión, sino que envíe directamente la solicitud del búfer.
Esto ahorra un paquete en la red y por tanto mejora el rendimiento. También puede ser útil para
algunos servidores, porque reciben inmediatamente la solicitud junto con la conexión entrante.

Esta funcionalidad se activa cuando se establece "option tcp-smart-connect" en un backend. No
está activada por defecto porque complica la resolución de problemas de red.

Solo tiene sentido activarla con protocolos donde el cliente habla primero, como HTTP. En otras
situaciones, si no hay datos que enviar en lugar del ACK, se envía un ACK normal.

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: "option tcp-smart-accept"

<a id="entry-4-2-option-tcpka"></a>

**`option tcpka`**

```haproxy
option tcpka
```

Activa o desactiva el envío de paquetes TCP keepalive en ambos lados

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Cuando hay un cortafuegos o cualquier componente consciente de sesiones entre un cliente y un
servidor, y cuando el protocolo implica sesiones muy largas con largos períodos de inactividad
(p. ej., escritorios remotos), existe el riesgo de que uno de los componentes intermedios decida
expirar una sesión que ha permanecido inactiva durante demasiado tiempo.

Activar los TCP keep-alive a nivel de socket hace que el sistema envíe paquetes regularmente al
otro extremo de la conexión, manteniéndola activa. El retardo entre sondas keep-alive lo controla
únicamente el sistema y depende tanto del sistema operativo como de sus parámetros de ajuste.

Es importante entender que los paquetes keep-alive no se emiten ni se reciben a nivel de
aplicación. Solo las pilas de red los ven. Por esta razón, aunque un lado del proxy ya use
keep-alives para mantener viva su conexión, esos paquetes keep-alive no se reenviarán al otro lado
del proxy.

Ten en cuenta que esto no tiene nada que ver con el keep-alive de HTTP.

Usar la opción "tcpka" activa la emisión de sondas TCP keep-alive tanto en el lado del cliente
como en el del servidor de una conexión. Ten en cuenta que esto solo tiene sentido en las secciones
"defaults" o "listen". Si esta opción se usa en un frontend, solo el lado del cliente recibirá
keep-alives, y si se usa en un backend, solo el lado del servidor los recibirá. Por esta razón, se
recomienda encarecidamente usar explícitamente "option clitcpka" y "option srvtcpka" cuando la
configuración está repartida entre frontends y backends.

Ver también: "option clitcpka", "option srvtcpka"

<a id="entry-4-2-option-tcplog"></a>

**`option tcplog [clf]`**

```haproxy
option tcplog [clf]
```

Activa el registro avanzado de conexiones TCP con estado del flujo y temporizadores

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
clf       si se añade el argumento "clf", el formato de salida será el
          formato CLF en lugar del formato TCP por defecto de HAProxy.
          Puedes usarlo cuando necesites alimentar los registros de HAProxy
          a través de un analizador de registros específico que solo
          soporte el formato CLF y que no sea extensible. Como este espera
          un formato HTTP, algunos valores han sido preestablecidos. La
          solicitud http se mostrará como TCP y el código de respuesta se
          mostrará como 000.
```

Por defecto, el formato de salida del registro es muy pobre, ya que solo contiene las direcciones
de origen y destino, y el nombre de la instancia. Al especificar "option tcplog", cada línea de
registro se convierte en un formato mucho más rico que incluye, entre otras cosas, los
temporizadores de conexión, el estado del flujo, los números de conexiones, el nombre del frontend,
del backend y del servidor y, por supuesto, la dirección y puertos de origen. Esta opción es útil
para proxies TCP puros para averiguar cuál de los dos, cliente o servidor, se desconecta o agota
el tiempo de espera. Para proxies HTTP normales, es mejor usar "option httplog", que es aún más
completo.

"option tcplog" anula cualquier directiva "log-format" anterior.

Ver también: "option httplog", y la [sección 8](/es/haproxy/configuration-logging/) sobre registro.

<a id="entry-4-2-option-transparent"></a>

**`option transparent        (deprecated)`**

```haproxy
option transparent        (deprecated)
no option transparent     (deprecated)
```

Activa el proxy transparente en el lado del cliente

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Esta opción se introdujo para proporcionar persistencia de capa 7 a balanceadores de carga de
capa 3. La idea es usar la capacidad del sistema operativo de redirigir una conexión entrante hacia
una dirección remota a un proceso local (aquí HAProxy), y hacer que este proceso sepa qué dirección
fue la solicitada originalmente. Cuando se usa esta opción, las sesiones sin cookies se reenviarán
a la dirección IP de destino original de la solicitud entrante (que debería corresponder a la de
otro equipo), mientras que las solicitudes con cookies seguirán reenviándose al servidor adecuado.

Ten en cuenta que, contrariamente a una creencia común, esta opción NO hace que HAProxy presente
la IP del cliente al servidor al establecer la conexión.

A partir de 3.3, esta opción está obsoleta porque solía sufrir varias limitaciones técnicas
internas. Usarla emitirá una advertencia, que puede evitarse si de verdad es necesario mediante la
palabra clave global "expose-deprecated-directives".

El enfoque correcto es declarar un servidor en la dirección 0.0.0.0, que se encargará de
conectarse a la dirección de destino esperada. Un servidor también gestionará adecuadamente las
conexiones inactivas hacia los servidores de destino.

Ejemplo:

```shell
# option transparent  ## before 3.3
server transparent 0.0.0.0
```

Ver también: el argumento "usesrc" de la palabra clave "source", y la opción "transparent" de la
palabra clave "bind".

option use-small-buffers [ queue \| l7-retries \| check ]\*

Activa el soporte de búferes pequeños para las categorías indicadas.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Esta opción puede usarse para activar el soporte de búferes pequeños en diferentes lugares para
ahorrar memoria. Por defecto, sin parámetros, los búferes pequeños se usan tanto como sea posible
en todos los lugares posibles. De lo contrario, es posible limitarlo a los siguientes lugares:

- queue: cuando se establece, se usarán búferes pequeños para almacenar las solicitudes, si son
  lo bastante pequeñas, cuando la conexión está en cola.
- l7-retries: cuando se establece, se usarán búferes pequeños para guardar las solicitudes cuando los reintentos L7 están activados.
- check: cuando se establece, se usarán búferes pequeños para las solicitudes de las comprobaciones de estado.

Cuando está activada, se usan búferes pequeños, pero solo si es posible. De lo contrario, cuando
los datos son demasiado grandes, se usa automáticamente un búfer regular. El tamaño de los búferes
pequeños es configurable mediante el ajuste global "tune.bufsize.small".

Si esta opción se ha activado en una sección "defaults", puede desactivarse en una instancia
específica anteponiendo la palabra clave "no".

Ver también: tune.bufsize.small

<a id="entry-4-2-persist-rdp-cookie"></a>

**`persist rdp-cookie`**

```haproxy
persist rdp-cookie
persist rdp-cookie(<name>)
```

Activa la persistencia basada en cookies RDP

Puede usarse en los siguientes contextos: tcp

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<name>    es el nombre opcional de la cookie RDP a comprobar. Si se omite,
          se usará el nombre de cookie por defecto "msts". Actualmente no
          hay ninguna razón válida para cambiar este nombre.
```

Esta instrucción activa la persistencia basada en una cookie RDP. La cookie RDP contiene toda la
información necesaria para encontrar el servidor en la lista de servidores conocidos. Así, cuando
esta opción se establece en el backend, la solicitud se analiza y, si se encuentra una cookie RDP,
se decodifica. Si coincide con un servidor conocido que sigue UP (o si "option persist" está
establecida), la conexión se reenvía a ese servidor.

Ten en cuenta que esto solo tiene sentido en un backend TCP, pero para que funcione, el frontend
debe haber esperado lo suficiente para asegurar que una cookie RDP esté presente en el búfer de la
solicitud. Es el mismo requisito que con el método de balanceo "rdp-cookie". Por ello, es muy
recomendable poner todas las instrucciones en una única sección "listen".

Además, es importante entender que el servidor de terminales emitirá esta cookie RDP solo si está
configurado en "token redirection mode" (modo de redirección por token), lo que significa que la
opción "IP address redirection" está desactivada.

Ejemplo:

```text
listen tse-farm
    bind :3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # if server is unknown, let's balance on the same cookie.
    # alternatively, "balance leastconn" may be useful too.
    balance rdp-cookie
    server srv1 1.1.1.1:3389
    server srv2 1.1.1.2:3389
```

Ver también: "balance rdp-cookie", "tcp-request" y la ACL "req.rdp_cookie".

<a id="entry-4-2-quic-initial"></a>

**`quic-initial <action> [ { if | unless } <condition> ]`**

```haproxy
quic-initial <action> [ { if | unless } <condition> ]
```

Realiza una acción sobre un paquete QUIC Initial entrante. Al contrario que "tcp-request
connection", esto se ejecuta antes de la instanciación de cualquier elemento de conexión y del inicio y finalización del handshake SSL, lo cual es más eficiente cuando se quieren rechazar
intentos de conexión.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| no

Argumentos:

```text
<action>    define la acción a realizar si la condición aplica. Ver más
            abajo.

<condition> es una condición estándar basada en ACL de solo capa 4 (ver
            sección 7). Sin embargo, las reglas QUIC initial se ejecutan
            demasiado pronto incluso para algunos métodos de obtención de
            muestras de capa 4, sin que haya advertencia de configuración, y
            pueden dar lugar a un comportamiento en tiempo de ejecución no
            especificado, aunque no provocarán la caída del proceso. Considera que, por
            ahora, solo se consideran soportadas las muestras internas y las
            de capa 4 "src*" y "dst*".

```

Esta acción se ejecuta temprano durante el análisis de paquetes QUIC. Como tal, solo se soporta
una lista mínima de acciones: - accept - dgram-drop - reject - send-retry

<a id="entry-4-2-rate-limit-sessions"></a>

**`rate-limit sessions <rate>`**

```haproxy
rate-limit sessions <rate>
```

Establece un límite en el número de nuevas sesiones aceptadas por segundo en un frontend

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<rate>    El parámetro <rate> es un entero que designa el número máximo de
          nuevas sesiones por segundo a aceptar en el frontend.
```

Cuando el frontend alcanza el número especificado de nuevas sesiones por segundo, deja de aceptar
nuevas conexiones hasta que la tasa vuelva a bajar del límite. Durante este tiempo, las sesiones
pendientes se mantendrán en el backlog del socket (en búferes del sistema) y HAProxy ni siquiera
será consciente de que hay sesiones pendientes. Al aplicar un límite muy bajo en un servicio muy
cargado, puede tener sentido aumentar el backlog del socket usando la palabra clave "backlog".

Esta funcionalidad es particularmente eficiente para bloquear ataques basados en conexiones o
abusos del servicio en servidores frágiles. Como la tasa de sesiones se mide cada milisegundo, es
extremadamente precisa. Además, el límite se aplica de inmediato; no se necesita ningún retardo
para detectar el umbral.

Ejemplo: limitar la tasa de conexiones en SMTP a 10 por segundo como máximo

```haproxy
listen smtp
    mode tcp
    bind :25
    rate-limit sessions 10
    server smtp1 127.0.0.1:1025
```

Nota: cuando se alcanza la tasa máxima, el estado del frontend no cambia, pero sus sockets
aparecen como "WAITING" en las estadísticas si la opción "socket-stats" está activada.

Ver también: la palabra clave "backlog" y el criterio de ACL "fe_sess_rate".

<a id="entry-4-2-redirect-location"></a>

**`redirect location <loc> [code <code>] <option> [{if | unless} <condition>]`**

```haproxy
redirect location <loc> [code <code>] <option> [{if | unless} <condition>]
redirect prefix   <pfx> [code <code>] <option> [{if | unless} <condition>]
redirect scheme   <sch> [code <code>] <option> [{if | unless} <condition>]
```

Devuelve una redirección HTTP si/no se cumple una condición

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Si/no se cumple la condición, la solicitud HTTP dará lugar a una respuesta de redirección. Si no
se especifica ninguna condición, la redirección se aplica incondicionalmente.

Argumentos:

```text
<loc>     Con "redirect location", el valor exacto de <loc> se coloca en la
          cabecera HTTP "Location". Cuando se usa en una regla
          "http-request", el valor <loc> sigue las reglas del formato de
          registro personalizado y puede incluir
          algunos valores dinámicos (ver formato de registro personalizado en la sección
          8.2.6).

<pfx>     Con "redirect prefix", la cabecera "Location" se construye a
          partir de la concatenación de <pfx> y la ruta URI completa,
          incluyendo la cadena de consulta, salvo que se especifique la
          opción "drop-query" (ver más abajo). Como caso especial, si <pfx>
          es exactamente "/", no se inserta nada antes de la URI original.
          Esto permite redirigir a la misma URL (por ejemplo, para insertar
          una cookie). Cuando se usa en una regla "http-request", el valor
          <pfx> sigue las reglas del formato de registro personalizado y puede incluir
          algunos valores dinámicos (ver formato de registro personalizado en la sección
          8.2.6).

<sch>     Con "redirect scheme", la cabecera "Location" se construye
          concatenando <sch> con "://", luego la primera ocurrencia de la
          cabecera "Host" y después la ruta URI, incluyendo la cadena de
          consulta salvo que se especifique la opción "drop-query" (ver más
          abajo). Si no se encuentra ninguna ruta o si la ruta es "*", se
          usa "/" en su lugar. Si no se encuentra cabecera "Host", se
          devolverá un componente de host vacío, que la mayoría de los
          navegadores recientes interpretan como una redirección al mismo
          host. Esta directiva se usa sobre todo para redirigir HTTP a
          HTTPS. Cuando se usa en una regla "http-request", el valor <sch>
          sigue las reglas del formato de registro personalizado y puede incluir algunos
          valores dinámicos (ver formato de registro personalizado en la sección 8.2.6).

<code>    El código es opcional. Indica qué tipo de redirección HTTP se
          desea. Solo se soportan los códigos 301, 302, 303, 307 y 308,
          usándose 302 por defecto si no se especifica código. 301
          significa "Moved permanently" (movido permanentemente), y un
          navegador puede cachear la Location. 302 significa "Moved
          temporarily" (movido temporalmente) e implica que el navegador no
          debe cachear la redirección. 303 equivale a 302, salvo que el
          navegador obtendrá la localización con un método GET. 307 es como
          302 pero deja claro que debe reutilizarse el mismo método. De
          igual modo, 308 sustituye a 301 si debe usarse el mismo método.

<option>  Existen varias opciones que pueden especificarse para ajustar el
          comportamiento esperado de una redirección:

  - "drop-query"
    Cuando esta palabra clave se usa en una redirección basada en prefijo,
    la localización se establecerá sin ninguna cadena de consulta posible,
    lo cual es útil, por ejemplo, para dirigir a los usuarios a una página
    no segura. No tiene efecto con una redirección de tipo location.

  - "append-slash"
    Esta palabra clave puede usarse junto con "drop-query" para redirigir a
    los usuarios que usan una URL que no termina en '/' a la misma con la
    '/'. Puede ser útil para asegurar que los motores de búsqueda solo vean
    una URL. Para ello, se prefiere un código de retorno 301.

  - "ignore-empty"
    Esta palabra clave solo tiene efecto cuando la localización se produce
    mediante una expresión de formato de registro (es decir, cuando se usa
    en http-request o http-response). Indica que si el resultado de la
    expresión está vacío, la regla debe omitirse silenciosamente. Su uso
    principal es permitir redirecciones masivas de rutas conocidas usando
    un mapa simple.

  - "set-cookie NAME[=value]"
    Se añadirá una cabecera "Set-Cookie" con NAME (y opcionalmente
    "=value") a la respuesta. Esto se usa a veces para indicar que un
    usuario ya ha sido visto, por ejemplo para protegerse de algunos tipos
    de DoS. No se añade ninguna otra opción de cookie, por lo que será una
    cookie de sesión. Ten en cuenta que, para un navegador, un nombre de
    cookie solo, sin signo igual, es diferente de una cookie con signo
    igual.

  - "set-cookie-fmt <fmt>"
    Es equivalente a la opción anterior, salvo que la cabecera "Set-Cookie"
    se rellenará con el resultado de la evaluación de la cadena de
    log-format <fmt>. Ten cuidado de respetar el formato "NAME[=value]"
    porque no se realiza ninguna comprobación especial durante el análisis
    de la configuración.

  - "clear-cookie NAME[=]"
    Se añadirá una cabecera "Set-Cookie" con NAME (y opcionalmente "="),
    pero con el atributo "Max-Age" establecido a cero. Esto indicará al
    navegador que elimine esta cookie. Es útil, por ejemplo, en las páginas
    de cierre de sesión. Es importante notar que limpiar la cookie "NAME"
    no eliminará una cookie establecida como "NAME=value". Para eso tienes
    que limpiar la cookie "NAME=", porque el navegador hace la distinción.

  - "keep-query"
    Cuando esta palabra clave se usa en una redirección basada en
    localización, la cadena de consulta de la URI original, si existe, se
    añadirá a la localización. Si no se encuentra ninguna cadena de
    consulta, no se añade nada. Si la localización ya contiene una cadena
    de consulta, la original se añadirá con el delimitador '&'.

```

Ejemplo: mover la URL de inicio de sesión solo a HTTPS.

```haproxy
acl clear      dst_port  80
acl secure     dst_port  8080
acl login_page url_beg   /login
acl logout     url_beg   /logout
acl uid_given  url_reg   /login?userid=[^&]+
acl cookie_set hdr_sub(cookie) SEEN=1

redirect prefix   https://mysite.com set-cookie SEEN=1 if !cookie_set
redirect prefix   https://mysite.com           if login_page !secure
redirect prefix   http://mysite.com drop-query if login_page !uid_given
redirect location http://mysite.com/           if !login_page secure
redirect location / clear-cookie USERID=       if logout
```

Ejemplo: enviar redirecciones para solicitudes de artículos sin '/'.

```haproxy
acl missing_slash path_reg ^/article/[^/]*$
redirect code 301 prefix / drop-query append-slash if missing_slash
```

Ejemplo: redirigir todo el tráfico HTTP a HTTPS cuando HAProxy gestiona el SSL.

```haproxy
redirect scheme https if !{ ssl_fc }
```

Ejemplo: anteponer el prefijo 'www.' a todos los hosts que no lo tengan

```haproxy
http-request redirect code 301 location      \
  http://www.%[hdr(host)]%[capture.req.uri]  \
  unless { hdr_beg(host) -i www }
```

Ejemplo: redirigir permanentemente solo las URLs antiguas a las nuevas

```haproxy
http-request redirect code 301 location               \
  %[path,map_str(old-blog-articles.map)] ignore-empty
```

Ver la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

<a id="entry-4-2-retries"></a>

**`retries <value>`**

```haproxy
retries <value>
```

Establece el número de reintentos a realizar en un servidor tras un fallo

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<value>   es el número de veces que debe reintentarse una solicitud o un
          intento de conexión en un servidor tras un fallo.
```

Por defecto, los reintentos solo se aplican a nuevos intentos de conexión. Sin embargo, cuando se
usa la directiva "retry-on", otras condiciones pueden desencadenar un reintento (p. ej., respuesta
vacía, código de estado no deseado), y cada una contará como un intento; cuando el número total de
intentos alcance el valor aquí indicado, se devolverá un error.

Para evitar reconexiones inmediatas a un servidor que se está reiniciando, se aplica un
temporizador de recuperación de min("timeout connect", un segundo) antes de que ocurra un
reintento en el mismo servidor.

Cuando se establece "option redispatch", algunos reintentos pueden realizarse en otro servidor
incluso si una cookie hace referencia a un servidor diferente. Por defecto, esto solo será el
último reintento, salvo que se pase un argumento a "option redispatch".

Ver también: "option redispatch"

<a id="entry-4-2-retry-on"></a>

**`retry-on [space-delimited list of keywords]`**

```haproxy
retry-on [space-delimited list of keywords]
```

Especifica cuándo intentar reintentar automáticamente una solicitud fallida. Este ajuste solo es
válido cuando "mode" está establecido en http y se ignora silenciosamente en caso contrario.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
 <keywords>  es una lista de palabras clave o códigos de estado HTTP
             delimitada por espacios, cada una representando un tipo de
             evento de fallo en el que se desea intentar reintentar la
             solicitud. Lee las notas del final antes de cambiar este
             ajuste. Se soportan las siguientes palabras clave:

   none              nunca reintentar

   conn-failure      reintentar cuando la conexión o el handshake SSL falló
                     y la solicitud no pudo enviarse. Este es el valor por
                     defecto.

   empty-response    reintentar cuando la conexión del servidor se cerró
                     después de enviar parte de la solicitud y no se recibió
                     nada del servidor. Este tipo de fallo puede deberse al
                     tiempo de espera de la solicitud en el lado del
                     servidor, a una condición de red deficiente, o a un
                     fallo o reinicio del servidor mientras procesaba la
                     solicitud.

   junk-response     reintentar cuando el servidor devolvió algo que no
                     parece una respuesta HTTP completa. Esto incluye
                     cabeceras de respuesta incompletas así como contenidos
                     no HTTP. Normalmente es mala idea reintentar en estos
                     eventos, que pueden deberse a un problema de
                     configuración (puerto de servidor erróneo) o a que la
                     solicitud sea dañina para el servidor (un ataque de
                     desbordamiento de búfer, por ejemplo).

   response-timeout  el tiempo de espera del servidor se agotó mientras
                     esperaba a que el servidor respondiera a la solicitud.
                     Esto puede deberse a una condición de red deficiente, al
                     reuso de una conexión inactiva que había expirado en la
                     ruta, o a que la solicitud sea extremadamente costosa
                     de procesar. En general es mala idea reintentar en
                     estos eventos en servidores con procesamiento pesado de
                     bases de datos (escaneos completos, etc.), ya que puede
                     amplificar los ataques de denegación de servicio.

   0rtt-rejected     reintentar solicitudes que se enviaron sobre early data
                     y fueron rechazadas por el servidor. Estas solicitudes
                     generalmente se consideran seguras para reintentar.

   <status>          cualquier código de estado HTTP entre "401" (Unauthorized), "403" (Forbidden), "404" (Not Found), "408" (Request Timeout),
"421" (Misdirected Request), "425" (Too Early),
"429" (Too Many Requests), "500" (Server Error),
"501" (Not Implemented), "502" (Bad Gateway),
"503" (Service Unavailable), "504" (Gateway Timeout).

   all-retryable-errors
                     reintentar la solicitud ante cualquier error que se
                     considere reintentable. Esto activa actualmente
                     "conn-failure", "empty-response", "junk-response",
                     "response-timeout", "0rtt-rejected", "500", "502",
                     "503" y "504".
```

Usar esta directiva sustituye cualquier ajuste anterior por los nuevos; no es acumulativa.

Ten en cuenta que usar cualquier cosa distinta de "none" y "conn-failure" requiere asignar un
búfer y copiar en él la solicitud completa, por lo que tiene impactos en memoria y rendimiento.
Las solicitudes que no quepan en un solo búfer nunca se reintentarán (ver el ajuste global
tune.bufsize).

Debes asegurarte de que la aplicación tiene incorporado un mecanismo de protección contra
reproducción, como identificadores de transacción únicos pasados en las solicitudes, o de que
reproducir la misma solicitud no tiene consecuencias; de lo contrario, es muy peligroso usar
cualquier valor de retry-on aparte de "conn-failure" y "none". Los servidores de archivos
estáticos y las cachés generalmente se consideran seguros frente a cualquier tipo de reintento.
Usar un código de estado puede ser útil para abandonar rápidamente un servidor que muestra un
comportamiento anormal (falta de memoria, problemas del sistema de archivos, etc.), pero en ese
caso puede ser buena idea redistribuir de inmediato la conexión a otro servidor (ver "option
redispatch" para esto). Por último, es importante entender que la mayoría de las causas de fallo
son las propias solicitudes, y que reintentar una solicitud que provoca un mal funcionamiento del
servidor a menudo empeorará aún más la situación para ese servidor, o para todo el servicio en
caso de redistribución.

Salvo que sepas exactamente cómo la aplicación maneja las solicitudes reproducidas, no deberías
usar esta directiva.

El valor por defecto es "conn-failure".

Ejemplo:

```text
retry-on 503 504
```

Ver también: "retries", "option redispatch", "tune.bufsize"

<a id="entry-4-2-server"></a>

**`server <name> <address>[:[port]] [param*]`**

```haproxy
server <name> <address>[:[port]] [param*]
```

Declara un servidor en un backend

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<name>    es el nombre interno asignado a este servidor. Este nombre
          aparecerá en los registros y alertas. Si "http-send-name-header"
          está establecido, se añadirá a la cabecera de la solicitud enviada
          al servidor. Este nombre debe ser único dentro de la sección
          backend.

<address> es la dirección IPv4 o IPv6 del servidor. Alternativamente, se
          soporta un nombre de host resoluble, pero este nombre se
          resolverá durante el arranque. La dirección "0.0.0.0" o "*" tiene
          un significado especial: indica que la conexión se reenviará a la
          misma dirección IP que la de la conexión del cliente. Esto es
          útil en arquitecturas de proxy transparente donde la conexión del
          cliente es interceptada y HAProxy debe reenviar a la dirección de
          destino original. Esto es más o menos lo que hace la palabra
          clave "transparent", con la diferencia de que con un servidor es
          posible limitar la concurrencia e informar de estadísticas.
          Opcionalmente, puede usarse un prefijo de familia de direcciones
          antes de la dirección para forzar la familia independientemente
          del formato de la dirección, lo que puede ser útil para
          especificar una ruta a un socket unix sin barra ('/'). Los
          prefijos soportados actualmente son:
                - 'ipv4@'  -> la dirección es siempre IPv4
                - 'ipv6@'  -> la dirección es siempre IPv6
                - 'unix@'  -> la dirección es una ruta a un socket unix
                  local
                - 'abns@'  -> la dirección está en el espacio de nombres
                  abstracto (solo Linux)
                - 'abnsz@'  -> la dirección está en el espacio de nombres
                  abstracto (solo Linux), pero terminada explícitamente en
                  cero. Esto significa que no se usa relleno \0 para
                  completar sun_path. Es útil para interconectar con
                  programas que no implementan la lógica de nombres abns
                  por defecto que usa haproxy.
                - 'sockpair@' -> la dirección es el FD de un socket unix
                  conectado o de un socketpair. Durante una conexión, el
                  backend crea un par de sockets conectados y pasa uno de
                  ellos por el FD. La parte bind usará el socket recibido
                  como FD del cliente. Debe usarse con cuidado.
                - 'quic4@' [ EXPERIMENTAL] -> la dirección se resuelve como
                  IPv4 y se usa el protocolo UDP. QUIC en el lado del
                  backend se considera experimental principalmente porque
                  impide eliminar el servidor en tiempo de ejecución.
                  Requiere la palabra clave global
                  "expose-experimental-directives" para usarlo.
                - 'quic6@' [ EXPERIMENTAL] -> la dirección se resuelve como
                  IPv6 y se usa el protocolo UDP. Se considera marcado como
                  experimental de forma similar.
                - 'rhttp@' [ EXPERIMENTAL ] -> familia de direcciones
                  personalizada para un servidor pasivo en contexto de
                  proxy inverso HTTP. Es una funcionalidad experimental que
                  requiere "expose-experimental-directives" en una línea
                  anterior a este servidor.
          Puede que quieras referenciar algunas variables de entorno en el
          parámetro de dirección; ver la sección 2.3 sobre variables de
          entorno. El ajuste "init-addr" puede usarse para modificar la
          forma en que las direcciones IP deben resolverse al arrancar.

<port>    es una especificación opcional de puerto. Si se establece, todas
          las conexiones se enviarán a este puerto. Si no, se usará el
          mismo puerto al que se conectó el cliente. El puerto también puede
          ir precedido por "+" o "-". En ese caso, el puerto del servidor se
          determinará sumando este valor al puerto del cliente.

<param*>  es una lista de parámetros para este servidor. La palabra clave
          "server" acepta un número importante de opciones y tiene una
          sección completa dedicada a ella. Consulta la sección 5 para más
          detalles.
```

Ejemplos:

```text
server first  10.1.1.1:1080 cookie first  check inter 1000
server second 10.1.1.2:1080 cookie second check inter 1000
server transp ipv4@
server backup "${SRV_BACKUP}:1080" backup
server www1_dc1 "${LAN_DC1}.101:80"
server www1_dc2 "${LAN_DC2}.101:80"
```

Nota: respecto a los sockets de espacio de nombres abstracto de Linux, los sockets "abns" de
HAProxy usan toda la longitud de sun_path como longitud de la dirección. Algunos otros programas
como socat usan por defecto solo la longitud de la cadena. Pasa la opción ",unix-tightsocklen=0"
a cualquier definición de socket abstracto en socat para hacerla compatible con la de HAProxy, o
usa la familia de socket "abnsz" de HAProxy en su lugar.

Ver también: "default-server", "http-send-name-header" y la [sección 5](/es/haproxy/bind-and-server-options/) sobre opciones de servidor

<a id="entry-4-2-server-state-file-name"></a>

**`server-state-file-name [ { use-backend-name | <file> } ]`**

```haproxy
server-state-file-name [ { use-backend-name | <file> } ]
```

Establece el archivo de estado de servidores a leer, cargar y aplicar a los servidores disponibles en este backend.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Solo aplica cuando la directiva "load-server-state-from-file" está establecida en "local". Cuando
no se proporciona `<file>`, si se usa "use-backend-name" o si esta directiva no está establecida,
se usa el nombre del backend. Si `<file>` comienza con una barra '/', se considera una ruta
absoluta. De lo contrario, `<file>` se concatena con la directiva global "server-state-base".

Ejemplo: la configuración mínima siguiente haría que HAProxy buscara el archivo de estado de
servidores '/etc/haproxy/states/bk':

    global
      server-state-file-base /etc/haproxy/states

    backend bk
      load-server-state-from-file

Ver también: "server-state-base", "load-server-state-from-file", y "show servers state"

<a id="entry-4-2-server-template"></a>

**`server-template <prefix> <num | range> <fqdn>[:<port>] [params*]`**

```haproxy
server-template <prefix> <num | range> <fqdn>[:<port>] [params*]
```

Establece una plantilla para inicializar servidores con parámetros compartidos. Los nombres de
estos servidores se construyen a partir de los parámetros `<prefix>` y \<num \| range\>.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<prefix>  Un prefijo para los nombres de servidor a construir.

<num | range>
          Si se proporciona <num>, esta plantilla inicializa <num>
          servidores con sufijos de nombre de servidor del 1 al <num>.
          También puede usarse un rango de números <num_low>-<num_high>
          para usar como sufijos de nombre de servidor los números del
          <num_low> al <num_high>.

<fqdn>    Un FQDN para todos los servidores que inicializa esta plantilla.

<port>    Mismo significado que el argumento <port> de "server" (ver la
          palabra clave "server").

<params*>
          Resto de parámetros de servidor entre todos los soportados por la
          palabra clave "server".
```

Ejemplos:

```shell
# Initializes 3 servers with srv1, srv2 and srv3 as names,
# google.com as FQDN, and health-check enabled.
server-template srv 1-3 google.com:80 check

# or
server-template srv 3 google.com:80 check

# would be equivalent to:
server srv1 google.com:80 check
server srv2 google.com:80 check
server srv3 google.com:80 check


```

<a id="entry-4-2-source"></a>

**`source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<port>] [interface <name>]
```

Establece la dirección de origen para las conexiones salientes

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<addr>    es la dirección IPv4 a la que HAProxy se vinculará antes de
          conectarse a un servidor. Esta dirección también se usa como
          origen para las comprobaciones de estado.

          El valor por defecto 0.0.0.0 significa que el sistema
          seleccionará la dirección más adecuada para alcanzar su destino.
          Opcionalmente, puede usarse un prefijo de familia de direcciones
          antes de la dirección para forzar la familia independientemente
          del formato de la dirección, lo que puede ser útil para
          especificar una ruta a un socket unix sin barra ('/'). Los
          prefijos soportados actualmente son:
            - 'ipv4@' -> la dirección es siempre IPv4
            - 'ipv6@' -> la dirección es siempre IPv6
            - 'unix@' -> la dirección es una ruta a un socket unix local
            - 'abns@' -> la dirección está en el espacio de nombres
                         abstracto (solo Linux)
            - 'abnsz@'  -> la dirección está en el espacio de nombres
                           abstracto terminado en cero (solo Linux)

          Puede que quieras referenciar algunas variables de entorno en el
          parámetro de dirección; ver la sección 2.3 sobre variables de
          entorno.

<port>    es un puerto opcional. Normalmente no es necesario, pero puede
          ser útil en algunos contextos muy específicos. El valor por
          defecto cero significa que el sistema seleccionará un puerto
          libre. Ten en cuenta que no se soportan rangos de puertos en el
          backend. Si quieres forzar rangos de puertos, tienes que
          especificarlos en cada línea "server".

<addr2>   es la dirección IP a presentar al servidor cuando las conexiones
          se reenvían en modo proxy totalmente transparente. Esto
          actualmente solo está soportado en algunos kernels de Linux
          parcheados. Cuando se especifica esta dirección, el servidor verá las conexiones de los clientes
          con esta dirección, mientras que las
          comprobaciones de estado seguirán usando la dirección <addr>.

<port2>   es el puerto opcional a presentar al servidor cuando las
          conexiones se reenvían en modo proxy totalmente transparente
          (ver <addr2> más arriba). El valor por defecto cero significa
          que el sistema seleccionará un puerto libre.

<hdr>     es el nombre de una cabecera HTTP de la cual obtener la IP a la
          que vincularse. Es el nombre de una lista de cabeceras separada
          por comas que puede contener múltiples direcciones IP. Por
          defecto, se usa la última ocurrencia. Está diseñado para
          funcionar con la cabecera X-Forwarded-For y vincularse
          automáticamente a la dirección IP del cliente tal como la vio el
          proxy anterior, típicamente Stunnel. Para usar otra ocurrencia
          distinta de la última, ver el parámetro <occ> más abajo. Cuando
          no se encuentra la cabecera (o la ocurrencia), no se realiza
          ningún vínculo, de modo que se usa la dirección IP por defecto
          del proxy. Ten presente también que el nombre de la cabecera no
          distingue mayúsculas de minúsculas, como cualquier cabecera
          HTTP.

<occ>     es el número de ocurrencia de un valor a usar en una cabecera
          multi-valor. Debe usarse junto con "hdr_ip(<hdr>)", para
          especificar qué ocurrencia usar como dirección IP de origen. Los
          valores positivos indican una posición desde la primera
          ocurrencia, siendo 1 la primera. Los valores negativos indican
          posiciones relativas a la última, siendo -1 la última. Esto
          resulta útil en situaciones donde una cabecera X-Forwarded-For se
          establece en el punto de entrada de una infraestructura y debe
          usarse varias capas de proxy después. Cuando no se especifica
          este valor, se asume -1. Pasar un cero aquí desactiva la
          funcionalidad.

<name>    es un nombre de interfaz opcional al que vincularse para el
          tráfico saliente. En sistemas que soportan esta funcionalidad
          (actualmente, solo Linux), esto permite vincular todo el tráfico
          hacia el servidor a esta interfaz incluso si no es la que el
          sistema seleccionaría según las tablas de enrutamiento. Debe
          usarse con extremo cuidado. Ten en cuenta que usar esta opción
          requiere privilegios de root.
```

La palabra clave "source" es útil en entornos complejos donde solo una dirección específica puede
conectarse a los servidores. Puede ser necesaria cuando, por ejemplo, debe usarse una dirección
privada a través de una pasarela pública, y se sabe que el sistema no puede determinar por sí solo
la dirección de origen adecuada.

Una extensión disponible en ciertos kernels de Linux parcheados puede usarse mediante la palabra
clave opcional "usesrc". Permite conectarse a los servidores con una dirección IP que no pertenece
al propio sistema. Esto se llama "modo proxy totalmente transparente". Para que funcione, los
servidores de destino deben enrutar su tráfico de vuelta a esta dirección a través de la máquina
que ejecuta HAProxy, y generalmente debe activarse el reenvío de IP en esa máquina.

En este modo de "proxy totalmente transparente", es posible forzar que se presente una dirección
IP específica a los servidores. En realidad no se usa mucho. Un uso más común es decirle a HAProxy
que presente la dirección IP del cliente. Para esto, hay dos métodos:

    - presentar las direcciones IP y puerto del cliente. Es el modo más
      transparente, pero puede causar problemas cuando el seguimiento de
      conexiones IP está activado en la máquina, porque una misma conexión
      puede verse dos veces con estados diferentes. Sin embargo, esta
      solución tiene la enorme ventaja de no limitar el sistema a las 64k
      parejas dirección+puerto salientes, porque se pueden usar todos los
      rangos del cliente.

    - presentar solo la dirección IP del cliente y seleccionar un puerto
      libre. Esta solución sigue siendo bastante elegante pero ligeramente
      menos transparente (los registros de los cortafuegos aguas abajo no
      coincidirán con los de aguas arriba). También presenta el
      inconveniente de limitar el número de conexiones simultáneas a los
      habituales 64k puertos. Sin embargo, como los puertos aguas arriba y
      aguas abajo son diferentes, el seguimiento local de conexiones IP en
      la máquina no se verá alterado por el reuso de la misma sesión.

Esta opción establece el origen por defecto para todos los servidores del backend. También puede
especificarse en una sección "defaults". Es posible una especificación más fina de la dirección de
origen a nivel de servidor usando la opción de servidor "source". Consulta la [sección 5](/es/haproxy/bind-and-server-options/) para
más información.

Para funcionar, "usesrc" requiere privilegios de root o, en sistemas que lo soportan, la
capacidad "cap_net_raw". Ver también la directiva global "setcap".

Ejemplos:

```text
backend private
    # Connect to the servers using our 192.168.1.200 source address
    source 192.168.1.200

backend transparent_ssl1
    # Connect to the SSL farm from the client's source address
    source 192.168.1.200 usesrc clientip

backend transparent_ssl2
    # Connect to the SSL farm from the client's source address and port
    # not recommended if IP conntrack is present on the local machine.
    source 192.168.1.200 usesrc client

backend transparent_ssl3
    # Connect to the SSL farm from the client's source address. It
    # is more conntrack-friendly.
    source 192.168.1.200 usesrc clientip

backend transparent_smtp
    # Connect to the SMTP farm from the client's source address/port
    # with Tproxy version 4.
    source 0.0.0.0 usesrc clientip

backend transparent_http
    # Connect to the servers using the client's IP as seen by previous
    # proxy.
    source 0.0.0.0 usesrc hdr_ip(x-forwarded-for,-1)
```

Ver también: la opción de servidor "source" en la [sección 5](/es/haproxy/bind-and-server-options/), los parches Tproxy para el kernel de Linux en
[www.balabit.com](http://www.balabit.com), y la palabra clave "bind".

<a id="entry-4-2-srvtcpka-cnt"></a>

**`srvtcpka-cnt <count>`**

```haproxy
srvtcpka-cnt <count>
```

Establece el número máximo de sondas keepalive que TCP debe enviar antes de descartar la conexión
en el lado del servidor.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<count>   es el número máximo de sondas keepalive.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPCNT. Si no se especifica, se usa el
parámetro TCP global del sistema (tcp_keepalive_probes). La disponibilidad de este ajuste depende
del sistema operativo. Se sabe que funciona en Linux.

Ver también: "option srvtcpka", "srvtcpka-idle", "srvtcpka-intvl".

<a id="entry-4-2-srvtcpka-idle"></a>

**`srvtcpka-idle <timeout>`**

```haproxy
srvtcpka-idle <timeout>
```

Establece el tiempo que la conexión debe permanecer inactiva antes de que TCP comience a enviar
sondas keepalive, si está activado el envío de paquetes TCP keepalive en el lado del servidor.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el tiempo que la conexión debe permanecer inactiva antes de
          que TCP comience a enviar sondas keepalive. Se especifica en
          segundos por defecto, pero puede estar en cualquier otra unidad
          si el número lleva la unidad como sufijo, tal como se explica al
          principio de este documento.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPIDLE. Si no se especifica, se usa el
parámetro TCP global del sistema (tcp_keepalive_time). La disponibilidad de este ajuste depende
del sistema operativo. Se sabe que funciona en Linux.

Ver también: "option srvtcpka", "srvtcpka-cnt", "srvtcpka-intvl".

<a id="entry-4-2-srvtcpka-intvl"></a>

**`srvtcpka-intvl <timeout>`**

```haproxy
srvtcpka-intvl <timeout>
```

Establece el tiempo entre sondas keepalive individuales en el lado del servidor.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el tiempo entre sondas keepalive individuales. Se especifica
          en segundos por defecto, pero puede estar en cualquier otra
          unidad si el número lleva la unidad como sufijo, tal como se
          explica al principio de este documento.
```

Esta palabra clave corresponde a la opción de socket TCP_KEEPINTVL. Si no se especifica, se usa el
parámetro TCP global del sistema (tcp_keepalive_intvl). La disponibilidad de este ajuste depende
del sistema operativo. Se sabe que funciona en Linux.

Ver también: "option srvtcpka", "srvtcpka-cnt", "srvtcpka-idle".

<a id="entry-4-2-stats-admin"></a>

**`stats admin { if | unless } <cond>`**

```haproxy
stats admin { if | unless } <cond>
```

Activa el nivel de administración de estadísticas si/no se cumple una condición

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Esta instrucción activa el nivel de administración de estadísticas si/no se cumple una condición.

El nivel de administración permite activar/desactivar servidores desde la interfaz web. Por
defecto, la página de estadísticas es de solo lectura por razones de seguridad. Si se establecen
directivas "stats scope" en la sección, solo los proxies designados por estas directivas aceptarán
cambios de estado; el acceso a los demás será denegado.

Actualmente, la solicitud POST está limitada al tamaño del búfer menos el espacio de búfer
reservado, lo que significa que si la lista de servidores es demasiado larga, la solicitud no se
procesará. Se recomienda modificar pocos servidores a la vez.

Esas solicitudes POST de administración son propensas a ataques CSRF. Esto se mitiga parcialmente
comprobando que el Origin (o el Referer si no hay Origin) coincide con la cabecera Host, pero no
es suficiente para evitar totalmente el ataque. No hay forma de estar completamente protegido
frente a ellas. Se recomienda no exponerla en una interfaz pública y restringir quién puede
acceder a ella.

Ejemplo:

```shell
# statistics admin level only for localhost
backend stats_localhost
    stats enable
    stats admin if LOCALHOST
```

Ejemplo:

```shell
# statistics admin level always enabled because of the authentication
backend stats_auth
    stats enable
    stats auth  admin:AdMiN123
    stats admin if TRUE
```

Ejemplo:

```shell
# statistics admin level depends on the authenticated user
userlist stats-auth
    group admin    users admin
    user  admin    insecure-password 'AdMiN123'
    group readonly users haproxy
    user  haproxy  insecure-password 'haproxy'

backend stats_auth
    stats enable
    acl AUTH       http_auth(stats-auth)
    acl AUTH_ADMIN http_auth_group(stats-auth) admin
    stats http-request auth unless AUTH
    stats admin if AUTH_ADMIN
```

Ver también: "stats enable", "stats auth", "stats http-request", "stats scope", la [sección 12.2](/es/haproxy/other-sections/#section-12-2) sobre
listas de usuarios y la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

<a id="entry-4-2-ssl-f-use"></a>

**`ssl-f-use [<sslbindconf> ...]*`**

```haproxy
ssl-f-use [<sslbindconf> ...]*
```

Asigna un certificado al frontend actual.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<sslbindconf> soporta las siguientes palabras clave de la línea bind
(ver Sección 5.1. Opciones de bind):

- allow-0rtt
- alpn
- ca-file
- ca-verify-file
- ciphers
- ciphersuites
- client-sigalgs
- crl-file
- curves
- ecdhe
- ktls
- no-alpn
- no-ca-names
- npn
- sigalgs
- ssl-min-ver
- ssl-max-ver
- verify

sslbindconf también soporta las siguientes palabras clave de la palabra
clave load de crt-store (ver Sección 12.7.1. Opciones de carga):

- crt
- key
- ocsp
- issuer
- sctl
- ocsp-update
```

Asigna un certificado `<crtname>` a una crt-list creada automáticamente con el nombre del
frontend y con el prefijo @ (ej.: '@frontend1').

Esta crt-list implícita se asignará a todas las líneas bind "ssl" del frontend actual.

Los comandos crt-list del socket de estadísticas tienen efecto sobre esta crt-list, por lo que se
podrían sustituir, eliminar o añadir certificados y opciones SSL a ella.

Ejemplo:

```text
frontend https
    bind :443 ssl
    bind quic4@:443 ssl
    ssl-f-use crt foobar.pem.rsa sigalgs "RSA-PSS+SHA256"
    ssl-f-use crt test.foobar.pem
    ssl-f-use crt test2.foobar.crt key test2.foobar.key ocsp test2.foobar.ocsp ocsp-update on
```

Ver también: "crt-list" y "crt".

<a id="entry-4-2-stats-auth"></a>

**`stats auth <user>:<passwd>`**

```haproxy
stats auth <user>:<passwd>
```

Activa las estadísticas con autenticación y concede acceso a una cuenta

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<user>    es un nombre de usuario al que conceder acceso

<passwd>  es la contraseña en texto claro asociada a este usuario
```

Esta instrucción activa las estadísticas con ajustes por defecto y restringe el acceso solo a los
usuarios declarados. Puede repetirse tantas veces como sea necesario para permitir tantos usuarios
como se desee. Cuando un usuario intenta acceder a las estadísticas sin una cuenta válida, se
devolverá una respuesta "401 Forbidden" para que el navegador pida al usuario un usuario y
contraseña válidos. El reino (realm) que se devolverá al navegador es configurable usando "stats
realm".

Como el método de autenticación es HTTP Basic Authentication, las contraseñas circulan en texto
claro por la red. Así, se decidió que el archivo de configuración también usara contraseñas en
texto claro para recordar a los usuarios que estas no deben ser sensibles ni compartirse con
ninguna otra cuenta.

También es posible reducir el alcance de los proxies que aparecen en el informe usando "stats
scope".

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats enable", "stats realm", "stats scope", "stats uri"

<a id="entry-4-2-stats-enable"></a>

**`stats enable`**

```haproxy
stats enable
```

Activa el informe de estadísticas con ajustes por defecto

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Esta instrucción activa el informe de estadísticas con los ajustes por defecto definidos en
tiempo de compilación. Salvo indicación en contrario, se usan estos ajustes: - stats uri :
/haproxy?stats - stats realm: "HAProxy Statistics" - stats auth : sin autenticación - stats
scope: sin restricción

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats realm", "stats uri"

<a id="entry-4-2-stats-hide-version"></a>

**`stats hide-version`**

```haproxy
stats hide-version
```

Activa las estadísticas y oculta el informe de la versión de HAProxy

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

La página de estadísticas puede informar de algunos datos útiles de estado junto con las
estadísticas. Entre ellos está la versión de HAProxy. Sin embargo, generalmente se considera
peligroso informar de una versión precisa a cualquiera, ya que puede ayudarle a atacar puntos
débiles conocidos con ataques específicos. La instrucción "stats hide-version" elimina la versión
del informe de estadísticas. Se recomienda para sitios públicos o cualquier sitio con un usuario/
contraseña débil, y es el valor por defecto.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats enable", "stats realm", "stats uri", "stats show-version"

<a id="entry-4-2-stats-http-request"></a>

**`stats http-request { allow | deny | auth [realm <realm>] }`**

```haproxy
stats http-request { allow | deny | auth [realm <realm>] }
             [ { if | unless } <condition> ]
```

Control de acceso para las estadísticas

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Como "http-request", este conjunto de opciones permite controlar con precisión el acceso a las
estadísticas. Cada opción puede ir seguida de if/unless y una ACL. La primera opción cuya
condición coincida (o la opción sin condición) es definitiva. Para "deny" se devolverá un error
403, para "allow" se realiza el procesamiento normal, y para "auth" se devuelve un código de error
401/407 para que se pida al cliente un nombre de usuario y contraseña.

No hay ningún límite fijo al número de instrucciones http-request por instancia.

Ver también: "http-request", la [sección 12.2](/es/haproxy/other-sections/#section-12-2) sobre listas de usuarios y la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

<a id="entry-4-2-stats-realm"></a>

**`stats realm <realm>`**

```haproxy
stats realm <realm>
```

Activa las estadísticas y establece el reino de autenticación

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<realm>   es el nombre del reino de HTTP Basic Authentication que se
          informa al navegador. El navegador lo usa para mostrarlo en la
          ventana emergente que invita al usuario a introducir un nombre de
          usuario y contraseña válidos.
```

El reino se lee como una sola palabra, por lo que cualquier espacio en él debe escaparse usando
una barra invertida ('&#92;').

Esta instrucción solo es útil junto con "stats auth", ya que está únicamente relacionada con la
autenticación.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats enable", "stats uri"

<a id="entry-4-2-stats-refresh"></a>

**`stats refresh <delay>`**

```haproxy
stats refresh <delay>
```

Activa las estadísticas con actualización automática

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<delay>   es el retardo de actualización sugerido, especificado en
          segundos, que se devolverá al navegador que consulta la página
          del informe. Aunque el navegador es libre de aplicar cualquier
          retardo, generalmente lo respetará y actualizará la página a
          ese intervalo. El intervalo de actualización puede especificarse
          en cualquier otra unidad de tiempo no por defecto, añadiendo la
          unidad como sufijo tras el valor, tal como se explica al
          principio de este documento.
```

Esta instrucción es útil en pantallas de monitorización con una página permanente que informa de
la actividad del balanceador de carga. Cuando se establece, la página HTML del informe incluirá un
enlace "refresh"/"stop refresh" para que el usuario pueda elegir si quiere o no la actualización
automática de la página.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats enable", "stats realm", "stats uri"

<a id="entry-4-2-stats-scope"></a>

**`stats scope { <name> | "." }`**

```haproxy
stats scope { <name> | "." }
```

Activa las estadísticas y limita el alcance del acceso

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<name>    es el nombre de una sección listen, frontend o backend a
          informar. El nombre especial "." (un solo punto) designa la
          sección en la que aparece la instrucción.
```

Cuando se especifica esta instrucción, solo las secciones enumeradas con ella aparecerán en el
informe. Todas las demás quedarán ocultas y los intentos de cambiar su estado en modo
administración serán rechazados. Esta instrucción puede aparecer tantas veces como sea necesario
si hay que informar de varias secciones. Ten en cuenta que la comprobación de nombres se realiza
como simples comparaciones de cadenas y que nunca se comprueba que un nombre de sección dado
exista realmente.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats enable", "stats realm", "stats uri" y "stats admin"

<a id="entry-4-2-stats-show-desc"></a>

**`stats show-desc [ <desc> ]`**

```haproxy
stats show-desc [ <desc> ]
```

Activa el informe de una descripción en la página de estadísticas.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

    `<desc>`    es una descripción opcional a informar. Si no se especifica,
              se usará automáticamente en su lugar la descripción de la
              sección global.

Esta instrucción es útil para usuarios que ofrecen servicios compartidos a sus clientes, donde el
nodo o la descripción debe ser diferente para cada cliente.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.
Por defecto, la descripción no se muestra.

Ejemplo:

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-desc Master node for Europe, Asia, Africa
    stats uri       /admin?stats
    stats refresh   5s
```

Ver también: "show-node", "stats enable", "stats uri" y "description" en la sección global.

<a id="entry-4-2-stats-show-legends"></a>

**`stats show-legends`**

```haproxy
stats show-legends
```

Activa el informe de información adicional en la página de estadísticas

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Activa el informe de información adicional en la página de estadísticas: - cap: capacidades
(proxy) - mode: uno de tcp, http o health (proxy) - id: ID SNMP (proxy, socket, servidor) - IP
(socket, servidor) - cookie (backend, servidor)

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.
El comportamiento por defecto es no mostrar esta información.

Ver también: "stats enable", "stats uri".

<a id="entry-4-2-stats-show-modules"></a>

**`stats show-modules`**

```haproxy
stats show-modules
```

Activa la muestra del módulo de estadísticas extra en la página de estadísticas

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

Se añaden nuevas columnas al final de la línea que contiene los valores de las estadísticas extra como tooltip.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.
El comportamiento por defecto es no mostrar esta información.

Ver también: "stats enable", "stats uri".

<a id="entry-4-2-stats-show-node"></a>

**`stats show-node [ <name> ]`**

```haproxy
stats show-node [ <name> ]
```

Activa el informe de un nombre de host en la página de estadísticas.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<name>    es un nombre opcional a informar. Si no se especifica, se usará
          automáticamente en su lugar el nombre de nodo de la sección
          global.
```

Esta instrucción es útil para usuarios que ofrecen servicios compartidos a sus clientes, donde el
nodo o la descripción puede ser diferente en una página de estadísticas proporcionada a cada
cliente. El comportamiento por defecto es no mostrar el nombre de host.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-node Europe-1
    stats uri       /admin?stats
    stats refresh   5s
```

Ver también: "show-desc", "stats enable", "stats uri", y "node" en la sección global.

<a id="entry-4-2-stats-show-version"></a>

**`stats show-version`**

```haproxy
stats show-version
```

Activa las estadísticas y muestra el informe de la versión de HAProxy

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos: ninguno

La página de estadísticas puede informar de algunos datos útiles de estado junto con las
estadísticas. Entre ellos está la versión de HAProxy. Sin embargo, generalmente se considera
peligroso informar de una versión precisa a cualquiera, ya que puede ayudarle a atacar puntos
débiles conocidos con ataques específicos, y por eso está desactivado por defecto. La instrucción
"stats show-version" activa la muestra de esta información. No se recomienda para sitios públicos
ni para cualquier sitio con un usuario/contraseña débil.

Ver también: "stats auth", "stats enable", "stats realm", "stats uri", "stats hide-version"

<a id="entry-4-2-stats-uri"></a>

**`stats uri <prefix>`**

```haproxy
stats uri <prefix>
```

Activa las estadísticas y define el prefijo de URI para acceder a ellas

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<prefix>  es el prefijo de cualquier URI que será redirigida a las
          estadísticas. Este prefijo puede contener un signo de
          interrogación ('?') para indicar parte de una cadena de consulta.
```

La URI de estadísticas se intercepta en el tráfico retransmitido, por lo que aparece como una
página dentro de la aplicación normal. Se aconseja encarecidamente asegurar que la URI
seleccionada nunca aparezca en la aplicación; de lo contrario, nunca será posible alcanzarla en
la aplicación.

La URI por defecto compilada en HAProxy es "/haproxy?stats", pero esto puede cambiarse en tiempo
de compilación, así que es mejor especificarla siempre explícitamente aquí. Generalmente es buena
idea incluir un signo de interrogación en la URI para que los proxies intermedios se abstengan de
cachear los resultados. Además, como cualquier cadena que comience por el prefijo será aceptada
como solicitud de estadísticas, el signo de interrogación ayuda a asegurar que ninguna URI válida
comience con las mismas palabras.

A veces es muy conveniente usar "/" como prefijo de URI y poner esa instrucción en una instancia
"listen" propia. Eso facilita dedicar una dirección o un puerto exclusivamente a las estadísticas.

Aunque esta instrucción por sí sola basta para activar el informe de estadísticas, se recomienda
establecer todas las demás opciones para evitar depender de parámetros por defecto poco evidentes.

Ejemplo:

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

Ver también: "stats auth", "stats enable", "stats realm"

<a id="entry-4-2-stick-match"></a>

**`stick match <pattern> [table <table>] [{if | unless} <cond>]`**

```haproxy
stick match <pattern> [table <table>] [{if | unless} <cond>]
```

Define una condición de coincidencia de patrón de solicitud para fijar un usuario a un servidor

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<pattern>  es una regla de expresión de muestra tal como se describe en la
           sección 7.3. Describe qué elementos de la solicitud o conexión
           entrante se analizarán con la esperanza de encontrar una
           entrada coincidente en una tabla de persistencia. Esta regla es
           obligatoria.

<table>    es un nombre opcional de tabla de persistencia. Si no se
           especifica, se usa la tabla del mismo backend. Una tabla de
           persistencia se declara con la instrucción "stick-table".

<cond>     es una condición de coincidencia opcional. Permite coincidir en
           un cierto criterio solo cuando se cumplen (o no se cumplen)
           otras condiciones. Por ejemplo, podría usarse para coincidir en
           una dirección IP de origen salvo cuando la solicitud pasa por un
           proxy conocido, en cuyo caso coincidiríamos en una cabecera que
           contiene esa dirección IP.
```

Algunos protocolos o aplicaciones requieren reglas de persistencia complejas y no siempre pueden
basarse simplemente en cookies ni en hash. La instrucción "stick match" describe una regla para
extraer el criterio de persistencia de una solicitud o conexión entrante. Ver la [sección 7](/es/haproxy/acls-and-samples/) para una lista
completa de patrones posibles y reglas de transformación.

La tabla debe declararse con la instrucción "stick-table". Debe ser de un tipo compatible con el
patrón. Por defecto es la que está presente en el mismo backend. Es posible compartir una tabla
con otros backends referenciándola con la palabra clave "table". Si se referencia otra tabla, se
usan los ID de servidor dentro de los backends. Por defecto, todos los ID de servidor empiezan en
1 en cada backend, así que el orden de los servidores basta. Pero en caso de duda, es muy
recomendable forzar los ID de servidor usando su ajuste "id".

Es posible restringir las condiciones en que aplicará una instrucción "stick match", usando "if"
o "unless" seguido de una condición. Ver la [sección 7](/es/haproxy/acls-and-samples/) para condiciones basadas en ACL.

No hay límite en el número de instrucciones "stick match". La primera que aplique y coincida
provocará que la solicitud se dirija al mismo servidor que se usó para la solicitud que creó la
entrada. Así, pueden usarse múltiples coincidencias como alternativas.

Las reglas stick se comprueban después de las cookies de persistencia, por lo que no afectarán a
la persistencia si ya se usó una cookie para seleccionar un servidor. Así, resulta muy fácil
insertar cookies y coincidir en direcciones IP para mantener la persistencia entre HTTP y HTTPS.

Ejemplo:

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

Ver también: "stick-table", "stick on", la [sección 11](/es/haproxy/stick-tables-and-peers/) sobre tablas de persistencia, y la [sección 7](/es/haproxy/acls-and-samples/) sobre ACL y
obtención de muestras.

<a id="entry-4-2-stick-on"></a>

**`stick on <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick on <pattern> [table <table>] [{if | unless} <condition>]
```

Define un patrón de solicitud para asociar un usuario a un servidor

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Nota: Esta forma es exactamente equivalente a "stick match" seguido de "stick store-request",
todos con los mismos argumentos. Consulta ambas palabras clave para más detalles. Solo se
proporciona como comodidad para escribir configuraciones más mantenibles.

Ejemplos:

```shell
# The following form ...
stick on src table pop if !localhost

# ...is strictly equivalent to this one:
stick match src table pop if !localhost
stick store-request src table pop if !localhost


# Use cookie persistence for HTTP, and stick on source address for HTTPS as
# well as HTTP without cookie. Share the same table between both accesses.
backend http
    mode http
    balance roundrobin
    stick on src table https
    cookie SRV insert indirect nocache
    server s1 192.168.1.1:80 cookie s1
    server s2 192.168.1.1:80 cookie s2

backend https
    mode tcp
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

Ver también: "stick match", "stick store-request", y la [sección 11](/es/haproxy/stick-tables-and-peers/) sobre tablas de persistencia.

<a id="entry-4-2-stick-store-request"></a>

**`stick store-request <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-request <pattern> [table <table>] [{if | unless} <condition>]
```

Define un patrón de solicitud usado para crear una entrada en una tabla de persistencia

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<pattern>  es una regla de expresión de muestra tal como se describe en la
           sección 7.3. Describe qué elementos de la solicitud o conexión
           entrante se analizarán, extraerán y almacenarán en la tabla una
           vez seleccionado un servidor.

<table>    es un nombre opcional de tabla de persistencia. Si no se
           especifica, se usa la tabla del mismo backend. Una tabla de
           persistencia se declara con la instrucción "stick-table".

<cond>     es una condición de almacenamiento opcional. Permite almacenar
           ciertos criterios solo cuando se cumplen (o no se cumplen)
           algunas condiciones. Por ejemplo, podría usarse para almacenar
           la dirección IP de origen salvo cuando la solicitud pasa por un
           proxy conocido, en cuyo caso almacenaríamos una forma convertida
           de una cabecera que contiene esa dirección IP.
```

Algunos protocolos o aplicaciones requieren reglas de persistencia complejas y no siempre pueden
basarse simplemente en cookies ni en hash. La instrucción "stick store-request" describe una regla
para decidir qué extraer de la solicitud y cuándo hacerlo, para almacenarlo en una tabla de
persistencia y que solicitudes posteriores coincidan con ello usando la instrucción "stick
match". Obviamente, la parte extraída debe tener sentido y tener posibilidad de coincidir en una
solicitud posterior. Almacenar la dirección IP de un cliente, por ejemplo, suele tener sentido.
Almacenar un ID encontrado en un parámetro de URL también tiene sentido. Almacenar un puerto de
origen casi nunca tendrá sentido porque la coincidencia será aleatoria. Ver la [sección 7](/es/haproxy/acls-and-samples/) para una
lista completa de patrones posibles y reglas de transformación.

La tabla debe declararse con la instrucción "stick-table". Debe ser de un tipo compatible con el
patrón. Por defecto es la que está presente en el mismo backend. Es posible compartir una tabla
con otros backends referenciándola con la palabra clave "table". Si se referencia otra tabla, se
usan los ID de servidor dentro de los backends. Por defecto, todos los ID de servidor empiezan en
1 en cada backend, así que el orden de los servidores basta. Pero en caso de duda, es muy
recomendable forzar los ID de servidor usando su ajuste "id".

Es posible restringir las condiciones en que aplicará una instrucción "stick store-request",
usando "if" o "unless" seguido de una condición. Esta condición se evaluará durante el análisis de
la solicitud, por lo que puede usarse cualquier criterio. Ver la [sección 7](/es/haproxy/acls-and-samples/) para condiciones
basadas en ACL.

No hay límite en el número de instrucciones "stick store-request", pero existe un límite de 8
almacenamientos simultáneos por solicitud o respuesta. Esto permite almacenar hasta 8 criterios,
todos extraídos de la solicitud o de la respuesta, independientemente del número de reglas. Solo
se conservarán los 8 primeros que coincidan. Con esto, es posible alimentar varias tablas a la vez
con la esperanza de aumentar la posibilidad de reconocer a un usuario en otro protocolo o método
de acceso. Es posible usar varias reglas store-request con la misma tabla, lo que puede usarse
para encontrar el mejor criterio en el que confiar, ordenando las reglas en orden decreciente de
preferencia. Solo se almacenará el primer criterio extraído para una tabla dada. Todas las reglas
store-request posteriores que referencien la misma tabla se omitirán y sus ACL no se evaluarán.

Las reglas "store-request" se evalúan una vez establecida la conexión con el servidor, de modo que
la tabla contendrá el servidor real que procesó la solicitud.

Ejemplo:

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

Ver también: "stick-table", "stick on", la [sección 11](/es/haproxy/stick-tables-and-peers/) sobre tablas de persistencia, y la [sección 7](/es/haproxy/acls-and-samples/) sobre ACL y
obtención de muestras.

<a id="entry-4-2-stick-store-response"></a>

**`stick store-response <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-response <pattern> [table <table>] [{if | unless} <condition>]
```

Define un patrón de respuesta usado para crear una entrada en una tabla de persistencia

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<pattern>  es una regla de expresión de muestra tal como se describe en la
           sección 7.3. Describe qué elementos de la respuesta o conexión
           se analizarán, extraerán y almacenarán en la tabla una vez
           seleccionado un servidor.

<table>    es un nombre opcional de tabla de persistencia. Si no se
           especifica, se usa la tabla del mismo backend. Una tabla de
           persistencia se declara con la instrucción "stick-table".

<cond>     es una condición de almacenamiento opcional. Permite almacenar
           ciertos criterios solo cuando se cumplen (o no se cumplen)
           algunas condiciones. Por ejemplo, podría usarse para almacenar
           el ID de sesión SSL solo cuando la respuesta es un SSL server
           hello.
```

Algunos protocolos o aplicaciones requieren reglas de persistencia complejas y no siempre pueden
basarse simplemente en cookies ni en hash. La instrucción "stick store-response" describe una
regla para decidir qué extraer de la respuesta y cuándo hacerlo, para almacenarlo en una tabla de
persistencia y que solicitudes posteriores coincidan con ello usando la instrucción "stick match".
Obviamente, la parte extraída debe tener sentido y tener posibilidad de coincidir en una solicitud
posterior. Almacenar un ID encontrado en una cabecera de una respuesta tiene sentido. Ver la [sección 7](/es/haproxy/acls-and-samples/) para
una lista completa de patrones posibles y reglas de transformación.

La tabla debe declararse con la instrucción "stick-table". Debe ser de un tipo compatible con el
patrón. Por defecto es la que está presente en el mismo backend. Es posible compartir una tabla
con otros backends referenciándola con la palabra clave "table". Si se referencia otra tabla, se
usan los ID de servidor dentro de los backends. Por defecto, todos los ID de servidor empiezan en
1 en cada backend, así que el orden de los servidores basta. Pero en caso de duda, es muy
recomendable forzar los ID de servidor usando su ajuste "id".

Es posible restringir las condiciones en que aplicará una instrucción "stick store-response",
usando "if" o "unless" seguido de una condición. Esta condición se evaluará durante el análisis de
la respuesta, por lo que puede usarse cualquier criterio. Ver la [sección 7](/es/haproxy/acls-and-samples/) para condiciones basadas
en ACL.

No hay límite en el número de instrucciones "stick store-response", pero existe un límite de 8
almacenamientos simultáneos por solicitud o respuesta. Esto permite almacenar hasta 8 criterios,
todos extraídos de la solicitud o de la respuesta, independientemente del número de reglas. Solo
se conservarán los 8 primeros que coincidan. Con esto, es posible alimentar varias tablas a la vez
con la esperanza de aumentar la posibilidad de reconocer a un usuario en otro protocolo o método
de acceso. Es posible usar varias reglas store-response con la misma tabla, lo que puede usarse
para encontrar el mejor criterio en el que confiar, ordenando las reglas en orden decreciente de
preferencia. Solo se almacenará el primer criterio extraído para una tabla dada. Todas las reglas
store-response posteriores que referencien la misma tabla se omitirán y sus ACL no se evaluarán.
Sin embargo, aunque una regla store-request referencie una tabla, una regla store-response puede
usar también la misma tabla. Esto significa que cada tabla puede aprender exactamente un elemento
de la solicitud y un elemento de la respuesta a la vez.

La tabla contendrá el servidor real que procesó la solicitud.

Ejemplo:

```shell
# Learn SSL session ID from both request and response and create affinity.
backend https
    mode tcp
    balance roundrobin
    # maximum SSL session ID length is 32 bytes.
    stick-table type binary len 32 size 30k expire 30m

    acl clienthello req.ssl_hello_type 1
    acl serverhello res.ssl_hello_type 2

    # use tcp content accepts to detects ssl client and server hello.
    tcp-request inspect-delay 5s
    tcp-request content accept if clienthello

    # no timeout on response inspect delay by default.
    tcp-response content accept if serverhello

    # SSL session ID (SSLID) may be present on a client or server hello.
    # Its length is coded on 1 byte at offset 43 and its value starts
    # at offset 44.

    # Match and learn on request if client hello.
    stick on req.payload_lv(43,1) if clienthello

    # Learn on response if server hello.
    stick store-response resp.payload_lv(43,1) if serverhello

    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

Ver también: "stick-table", "stick on", la [sección 11](/es/haproxy/stick-tables-and-peers/) sobre tablas de persistencia, y la [sección 7](/es/haproxy/acls-and-samples/) sobre ACL y
extracción de patrones.

<a id="entry-4-2-stick-table-type"></a>

**`stick-table type <type> size <size> [expire <expire>] [args...]`**

```haproxy
stick-table type <type> size <size> [expire <expire>] [args...]
```

Configura la tabla de persistencia para la sección actual

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| sí

Esto se usa para declarar y configurar una stick-table. Consulta la [sección 11.1](/es/haproxy/stick-tables-and-peers/#section-11-1) para los detalles
completos y la lista de argumentos soportados. Solo el tipo y el tamaño son obligatorios.

<a id="entry-4-2-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
```

Define un comentario para la regla tcp-check siguiente, informado en los registros si falla.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<string>  es el mensaje de comentario a añadir en los registros si la regla
          tcp-check siguiente falla.
```

Solo funciona para las reglas connect, send y expect. Es útil para generar informes de errores
fáciles de entender.

Ver también: "option tcp-check", "tcp-check connect", "tcp-check send" y "tcp-check expect".

<a id="entry-4-2-tcp-check-connect"></a>

**`tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]`**

```haproxy
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
```

Abre una nueva conexión

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje a informar si la evaluación de la regla
               falla.

default      Usa las opciones por defecto de la línea del servidor para
             hacer las comprobaciones de estado. Las opciones del servidor
             se usan solo si no se redefinen.

port <expr>  si no se establece, se usa el puerto de comprobación o el
             puerto del servidor. Indica a HAProxy dónde abrir la conexión.
             <port> debe ser un entero válido de puerto de origen TCP, de
             1 a 65535, o una expresión sample-fetch.

addr <ip>    define la dirección IP con la que hacer la comprobación de
             estado.

send-proxy   envía una cadena de protocolo PROXY

via-socks4   activa las comprobaciones de estado salientes usando un proxy
             socks4 aguas arriba.

ssl          abre una conexión cifrada

sni <sni>    especifica el SNI a usar para hacer comprobaciones de estado
             sobre SSL.

alpn <alpn>  define qué protocolos anunciar con ALPN. La lista de
             protocolos consiste en una lista de nombres de protocolo
             delimitada por comas, por ejemplo: "http/1.1,http/1.0" (sin
             comillas). Si no se establece, se usa el ALPN del servidor.

proto <name> fuerza el protocolo del multiplexor a usar para esta
             conexión. Debe ser un protocolo mux TCP y debe poder usarse
             en el lado del backend. La lista de protocolos disponibles se
             muestra en haproxy -vv.

linger       cierra limpiamente la conexión en lugar de usar un solo RST.
```

Cuando una aplicación reside en más de un puerto TCP o cuando HAProxy balancea muchos servicios
en un solo backend, tiene sentido sondear todos los servicios individualmente antes de considerar
un servidor como operativo.

Cuando no hay ningún puerto TCP configurado en la línea del servidor ni directiva de puerto de
servidor, entonces 'tcp-check connect port `<port>`' debe ser el primer paso de la secuencia.

En un conjunto de reglas tcp-check se requiere un 'connect'; además, es obligatorio comenzar el
conjunto de reglas con una regla 'connect'. El propósito es asegurar que el administrador sabe lo
que hace.

Cuando un connect debe comenzar el conjunto de reglas, aún puede ir precedido de reglas set-var,
unset-var o comment.

Ejemplos:

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option tcp-check
tcp-check connect
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
tcp-check connect port 443 ssl
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
server www 10.0.0.1 check port 80

# check both POP and IMAP from a single server:
option tcp-check
tcp-check connect port 110 linger
tcp-check expect string +OK\ POP3\ ready
tcp-check connect port 143
tcp-check expect string *\ OK\ IMAP4\ ready
server mail 10.0.0.1 check
```

Ver también: "option tcp-check", "tcp-check send", "tcp-check expect"

<a id="entry-4-2-tcp-check-expect"></a>

**`tcp-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
```

Especifica datos a recopilar y analizar durante una comprobación de estado genérica

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje a informar si la evaluación de la regla
               falla.

min-recv  es opcional y puede definir la cantidad mínima de datos
          necesaria para evaluar la regla expect actual. Si el número de
          bytes recibidos está por debajo de este límite, la comprobación
          esperará más datos. Esta opción puede usarse para resolver
          algunas reglas de coincidencia ambiguas o para evitar ejecutar
          coincidencias de expresiones regulares costosas sobre contenido
          que se sabe que aún está incompleto. Si se usa una cadena exacta
          (string o binary), se usa el mínimo entre la longitud de la
          cadena y este parámetro. Este parámetro se ignora si está
          establecido en -1. Si la regla expect no coincide, la
          comprobación esperará más datos. Si se establece en 0, el
          resultado de la evaluación siempre es concluyente.

ok-status <st>     es opcional y puede usarse para establecer el estado de
                   la comprobación si la regla expect se evalúa
                   correctamente y si es la última regla del conjunto de
                   reglas tcp-check. Se soportan "L7OK", "L7OKC", "L6OK" y
                   "L4OK":
                     - L7OK : comprobación superada en la capa 7
                     - L7OKC: comprobación superada condicionalmente en la
                               capa 7, pone el servidor en estado NOLB.
                     - L6OK : comprobación superada en la capa 6
                     - L4OK : comprobación superada en la capa 4
                    Por defecto se usa "L7OK".

error-status <st>  es opcional y puede usarse para establecer el estado de
                   la comprobación si ocurre un error durante la
                   evaluación de la regla expect. Se soportan "L7OKC",
                   "L7RSP", "L7STS", "L6RSP" y "L4CON":
                     - L7OKC: comprobación superada condicionalmente en la
                               capa 7, pone el servidor en estado NOLB.
                     - L7RSP: respuesta inválida de capa 7 - error de
                               protocolo
                     - L7STS: error de respuesta de capa 7, por ejemplo
                               HTTP 5xx
                     - L6RSP: respuesta inválida de capa 6 - error de
                               protocolo
                     - L4CON: problema de conexión de capas 1-4
                   Por defecto se usa "L7RSP".

tout-status <st>   es opcional y puede usarse para establecer el estado de
                   la comprobación si se agota el tiempo de espera durante la
                   evaluación de la regla expect. Se soportan "L7TOUT",
                   "L6TOUT" y "L4TOUT":
                     - L7TOUT: tiempo de espera agotado de capa 7 (HTTP/SMTP)
                     - L6TOUT: tiempo de espera agotado de capa 6 (SSL)
                     - L4TOUT: tiempo de espera agotado de capas 1-4
                   Por defecto se usa "L7TOUT".

on-success <fmt>   es opcional y puede usarse para personalizar el mensaje
                   informativo informado en los registros si la regla
                   expect se evalúa correctamente y si es la última regla
                   del conjunto de reglas tcp-check. <fmt> es un formato de
                   registro personalizado (ver sección
                   8.2.6).

on-error <fmt>     es opcional y puede usarse para personalizar el mensaje
                   informativo informado en los registros si ocurre un
                   error durante la evaluación de la regla expect. <fmt>
                   es un formato de registro personalizado (ver sección 8.2.6).

status-code <expr> es opcional y puede usarse para establecer el código de
                   estado de la comprobación informado en los registros,
                   en caso de éxito o de error. <expr> es una expresión
                   estándar de HAProxy formada por un sample-fetch seguido
                   de algunos conversores.

<match>   es una palabra clave que indica cómo buscar un patrón específico
          en la respuesta. La palabra clave puede ser una de "string",
          "rstring", "binary" o "rbinary".
          La palabra clave puede ir precedida de un signo de exclamación
          ("!") para negar la coincidencia. Se permiten espacios entre el
          signo de exclamación y la palabra clave. Ver más abajo para más
          detalles sobre las palabras clave soportadas.

<pattern> es el patrón a buscar. Puede ser una cadena o una expresión
          regular. Si el patrón contiene espacios, deben escaparse con la
          habitual barra invertida ('\').
          Si la coincidencia se establece en binary, el patrón debe pasarse
          como una serie de dígitos hexadecimales en número par. Cada
          secuencia de dos dígitos representará un byte. Los dígitos
          hexadecimales pueden usarse en mayúsculas o minúsculas.
```

Las coincidencias disponibles son intencionadamente similares a sus primas de http-check:

```text
string <string>: comprueba la coincidencia de la cadena exacta en el búfer
                  de respuesta. Una respuesta de comprobación de estado se
                  considerará válida si el búfer de respuesta contiene esta
                  cadena exacta. Si la palabra clave "string" va precedida
                  de "!", la respuesta se considerará inválida si el cuerpo
                  contiene esta cadena. Esto puede usarse para buscar un
                  patrón obligatorio en una respuesta de protocolo, o para
                  detectar un fallo cuando aparece un error específico en
                  un banner de protocolo.

rstring <regex>: comprueba una expresión regular sobre el búfer de
                  respuesta. Una respuesta de comprobación de estado se
                  considerará válida si el búfer de respuesta coincide con
                  esta expresión. Si la palabra clave "rstring" va
                  precedida de "!", la respuesta se considerará inválida si
                  el cuerpo coincide con la expresión.

string-lf <fmt>: comprueba una coincidencia de formato de registro personalizado en el
                  búfer de respuesta. Una respuesta de comprobación de
                  estado se considerará válida si el búfer de respuesta
                  contiene la cadena resultante de la evaluación de <fmt>,
                  que sigue las reglas del formato de registro personalizado descritas en
                  la sección 8.2.6. Si va precedida de "!", la respuesta se
                  considerará inválida si el búfer contiene la cadena.

binary <hexstring>: comprueba que la cadena exacta en su forma
                     hexadecimal coincide en el búfer de respuesta. Una
                     respuesta de comprobación de estado se considerará
                     válida si el búfer de respuesta contiene esta cadena
                     hexadecimal exacta.
                     Su propósito es coincidir con datos en protocolos
                     binarios.

rbinary <regex>: comprueba una expresión regular sobre el búfer de
                  respuesta, como "rstring". Sin embargo, el búfer de
                  respuesta se transforma a su forma hexadecimal, incluidos
                  los bytes NUL. Esto permite usar todos los motores de
                  regex para coincidir con cualquier contenido binario. La
                  transformación hexadecimal ocupa el doble del tamaño de
                  la respuesta original. Como tal, el patrón esperado debe
                  funcionar como máximo sobre la mitad del tamaño del búfer
                  de respuesta.

binary-lf <hexfmt>: comprueba una coincidencia de un formato de registro personalizado en
                     su forma hexadecimal en el búfer de respuesta. Una
                     respuesta de comprobación de estado se considerará
                     válida si el búfer de respuesta contiene la cadena
                     hexadecimal resultante de la evaluación de <fmt>, que
                     sigue las reglas del formato de registro personalizado (ver sección
                     8.2.6). Si va precedida de "!", la respuesta se
                     considerará inválida si el búfer contiene la cadena
                     hexadecimal. La cadena hexadecimal se convierte en una
                     cadena binaria antes de coincidir con el búfer de
                     respuesta.
```

Es importante notar que las respuestas estarán limitadas a un cierto tamaño definido por la
opción global "tune.bufsize", cuyo valor por defecto es 16384 bytes. Así, las respuestas
demasiado grandes pueden no contener el patrón obligatorio al usar "string", "rstring" o binary.
Si absolutamente se requiere una respuesta grande, es posible cambiar el tamaño máximo por defecto
estableciendo la variable global. Sin embargo, conviene tener presente que analizar respuestas
muy grandes puede desperdiciar ciclos de CPU, especialmente cuando se usan expresiones regulares,
y que siempre es mejor centrar las comprobaciones en recursos más pequeños. Además, en su estado
actual, la comprobación no encontrará ninguna cadena ni regex más allá de un carácter nulo en la
respuesta. De igual modo, no es posible solicitar la coincidencia con el carácter nulo.

Ejemplos:

```shell
# perform a POP check
option tcp-check
tcp-check expect string +OK\ POP3\ ready

# perform an IMAP check
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready

# look for the redis master server
option tcp-check
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check send QUIT\r\n
tcp-check expect string +OK

```

Ver también: "option tcp-check", "tcp-check connect", "tcp-check send", "tcp-check send-binary",
"http-check expect", tune.bufsize

<a id="entry-4-2-tcp-check-send"></a>

**`tcp-check send <data> [comment <msg>]`**

```haproxy
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
```

Especifica una cadena o un formato de registro personalizado a enviar como pregunta durante una comprobación de estado genérica

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje a informar si la evaluación de la regla
               falla.

<data>         es la cadena que se enviará durante una sesión de
               comprobación de estado genérica.

<fmt>          es el formato de registro personalizado que se enviará, una vez evaluado,
               durante una sesión de comprobación de estado genérica (ver
               sección 8.2.6).
```

Ejemplos:

```shell
# look for the redis master server
option tcp-check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
```

Ver también: "option tcp-check", "tcp-check connect", "tcp-check expect", "tcp-check send-binary",
tune.bufsize

<a id="entry-4-2-tcp-check-send-binary"></a>

**`tcp-check send-binary <hexstring> [comment <msg>]`**

```haproxy
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
```

Especifica una cadena de dígitos hexadecimales o un formato de registro personalizado de dígitos hexadecimales a
enviar como pregunta binaria durante una comprobación de estado tcp en crudo

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
comment <msg>  define un mensaje a informar si la evaluación de la regla
               falla.

<hexstring>    es la cadena hexadecimal que se enviará, una vez convertida
               a binario, durante una sesión de comprobación de estado
               genérica.

<hexfmt>       es el formato de registro personalizado hexadecimal que se enviará, una vez
               evaluado y convertido a binario, durante una sesión de
               comprobación de estado genérica (ver sección 8.2.6).
```

Ejemplos:

```shell
# redis check in binary
option tcp-check
tcp-check send-binary 50494e470d0a # PING\r\n
tcp-check expect binary 2b504F4e47 # +PONG

```

Ver también: "option tcp-check", "tcp-check connect", "tcp-check expect", "tcp-check send",
tune.bufsize

<a id="entry-4-2-tcp-check-set-var"></a>

**`tcp-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Esta operación define el contenido de una variable. La variable se declara inline.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<var-name>   El nombre de la variable. Solo se pueden usar los ámbitos
             "proc", "sess" y "check". Ver la sección 2.8 sobre variables
             para más detalles.

 <cond>      Un conjunto de condiciones que deben cumplirse todas para que
             la variable se establezca realmente (como "ifnotempty",
             "ifgt"...). Ver la descripción del convertidor set-var para
             una lista completa de las condiciones posibles.

 <expr>      Es una expresión de recuperación de muestras (sample-fetch)
             potencialmente seguida de convertidores.

 <fmt>       Es el valor expresado usando las reglas del formato de registro personalizado
             (ver formato de registro personalizado en la sección 8.2.6).
```

Ejemplos:

```text
tcp-check set-var(check.port) int(1234)
tcp-check set-var-fmt(check.name) "%H"

```

<a id="entry-4-2-tcp-check-unset-var"></a>

**`tcp-check unset-var(<var-name>)`**

```haproxy
tcp-check unset-var(<var-name>)
```

Libera una referencia a una variable dentro de su ámbito.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<var-name>   El nombre de la variable. Solo se pueden usar los ámbitos
             "proc", "sess" y "check". Ver la sección 2.8 sobre variables
             para más detalles.
```

Ejemplos:

```text
tcp-check unset-var(check.port)

```

<a id="entry-4-2-tcp-request-connection"></a>

**`tcp-request connection <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
tcp-request connection <action> <options...> [ { if | unless } <condition> ]
```

Realiza una acción sobre una conexión entrante dependiendo de una condición de capa 4

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| no

Argumentos:

```text
<action>    define la acción a realizar si la condición se aplica. Ver
            abajo.

<condition> es una condición estándar basada en ACL solo de capa 4 (ver
            sección 7).
```

Inmediatamente después de la aceptación de una nueva conexión entrante, es posible evaluar algunas
condiciones para decidir si esa conexión debe aceptarse, descartarse o si se debe rastrear sus
contadores. Esas condiciones no pueden hacer uso de ningún contenido de datos porque la conexión
aún no se ha leído y los búferes aún no están asignados. Esto se usa para aceptar o descartar de
forma selectiva y muy rápida conexiones de diversas fuentes con una sobrecarga muy baja. Si es
necesario inspeccionar algún contenido para tomar la decisión, se deben usar en su lugar las
instrucciones "tcp-request content".

Las reglas "tcp-request connection" se evalúan en su orden exacto de declaración. Si ninguna regla
coincide o si no hay ninguna regla, la acción por defecto es aceptar la conexión entrante. No hay
ningún límite específico al número de reglas que pueden insertarse. Cualquier regla puede ir
seguida opcionalmente de una condición basada en ACL, en cuyo caso solo se evaluará si la
condición se evalúa como verdadera.

La condición se evalúa justo antes de que se ejecute la acción, y la acción se realiza exactamente
una vez. Como tal, no hay problema si una acción cambia un elemento que se comprueba como parte de
la condición. Esto también significa que varias acciones pueden depender de la misma condición, de
modo que la primera acción que cambia la evaluación de la condición es suficiente para desactivar
implícitamente las acciones restantes. Esto se usa, por ejemplo, al intentar asignar un valor a
una variable desde diversas fuentes cuando está vacía.

La primera palabra clave después de "tcp-request connection" en la sintaxis es la acción de la
regla, seguida opcionalmente de un número variable de argumentos para la acción. Las acciones
soportadas y sus respectivas sintaxis se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3)
"Acciones" (buscar las acciones que marcan "TCP RqCon").

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con la
capacidad frontend y por proxies con la capacidad backend. Esto significa que una sección listen
no puede usar una sección defaults que defina tales reglas.

Ten en cuenta que la condición "if/unless" es opcional. Si no se establece ninguna condición en la
acción, simplemente se realiza de forma incondicional. Esto puede ser útil para las acciones
"track-sc\*" así como para cambiar la acción por defecto a un rechazo.

Ejemplo: aceptar todas las conexiones de hosts en la lista blanca, rechazar sin contarlas las
conexiones demasiado rápidas y rastrear las conexiones aceptadas. Esto hace que la tasa de
conexiones quede limitada desde las fuentes abusivas.

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection reject if { src_conn_rate gt 10 }
        tcp-request connection track-sc0 src

Ejemplo: aceptar todas las conexiones de hosts en la lista blanca, contar todas las demás
conexiones y rechazar las demasiado rápidas. Esto hace que las abusivas queden bloqueadas
mientras no reduzcan su velocidad.

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection track-sc0 src
        tcp-request connection reject if { sc0_conn_rate gt 10 }

Ejemplo: activar el protocolo PROXY para el tráfico que proviene de todos los proxies conocidos.

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }

Ver la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

Ver también: "tcp-request session", "tcp-request content", "stick-table"

<a id="entry-4-2-tcp-request-content"></a>

**`tcp-request content <action> [{if | unless} <condition>]`**

```haproxy
tcp-request content <action> [{if | unless} <condition>]
```

Realiza una acción sobre una nueva sesión dependiendo de una condición de capas 4-7

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

Argumentos:

```text
<action>    define la acción a realizar si la condición se aplica. Ver
            abajo.

<condition> es una condición estándar basada en ACL de capas 4-7 (ver
            sección 7).
```

El contenido de una solicitud puede analizarse en una etapa temprana del procesamiento de la
solicitud llamada "inspección de contenido TCP". Durante esta etapa, las reglas basadas en ACL se
evalúan cada vez que el contenido de la solicitud se actualiza, hasta que una regla "accept", un
"reject" o un "switch-mode" coincide, o hasta que expira el tiempo de inspección de la solicitud
TCP sin ninguna regla que coincida.

La primera diferencia entre estas reglas y las reglas "tcp-request connection" es que las reglas
"tcp-request content" pueden hacer uso de los contenidos para tomar una decisión. La mayoría de
las veces, estas decisiones considerarán un reconocimiento de protocolo o su validez. La segunda
diferencia es que las reglas basadas en contenido pueden usarse tanto en frontends como en
backends. En caso de HTTP keep-alive con el cliente, todas las reglas "tcp-request content" se
evalúan de nuevo, de modo que HAProxy mantiene un registro de qué contadores sticky fueron
asignados por una regla "tcp-request connection" frente a una regla "tcp-request content", y
vacía todos los relacionados con el contenido después de procesar una solicitud HTTP, para que
puedan volver a evaluarse por las reglas que se evalúan de nuevo para la siguiente solicitud. Esto
tiene una importancia particular cuando la regla rastrea alguna información L7 o cuando está
condicionada por una ACL basada en L7, ya que el rastreo puede cambiar entre solicitudes.

Las reglas basadas en contenido se evalúan en su orden exacto de declaración. Si ninguna regla
coincide o si no hay ninguna regla, la acción por defecto es aceptar los contenidos. No hay
ningún límite específico al número de reglas que pueden insertarse.

Aunque no hay nada obligatorio al respecto, se recomienda usar track-sc0 en las reglas
"tcp-request connection", track-sc1 para las reglas "tcp-request content" en el frontend, y
track-sc2 para las reglas "tcp-request content" en el backend, porque eso hace que la
configuración sea más legible y más fácil de depurar, pero esto es solo una guía y todos los
contadores pueden usarse en cualquier parte.

La primera palabra clave después de "tcp-request content" en la sintaxis es la acción de la
regla, seguida opcionalmente de un número variable de argumentos para la acción. Las acciones
soportadas y sus respectivas sintaxis se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3)
"Acciones" (buscar las acciones que marcan "TCP RqCnt").

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con la
capacidad frontend y por proxies con la capacidad backend. Esto significa que una sección listen
no puede usar una sección defaults que defina tales reglas.

Ten en cuenta que la condición "if/unless" es opcional. Si no se establece ninguna condición en la
acción, simplemente se realiza de forma incondicional. Esto puede ser útil para las acciones
"track-sc\*" así como para cambiar la acción por defecto a un rechazo.

Ten en cuenta también que se recomienda usar una regla "tcp-request session" para rastrear
información que *no* depende de los contenidos de capa 7, especialmente en frontends HTTP.
Algunos procesamientos HTTP se realizan a nivel de sesión y pueden provocar un rechazo temprano
de las solicitudes. Así, el rastreo a nivel de contenido puede verse perturbado en tal caso. Se
emite un aviso durante el arranque para prevenir, en la medida de lo posible, ese uso poco fiable.

Es perfectamente posible coincidir con contenidos de capa 7 usando reglas "tcp-request content"
desde un proxy TCP, ya que las coincidencias ACL específicas de HTTP son capaces de analizar
previamente el contenido de un búfer antes de extraer los datos requeridos. Si los contenidos
bufferizados no se analizan como un mensaje HTTP válido, entonces la ACL no coincide. El analizador
que interviene allí es exactamente el mismo que para todo el demás procesamiento HTTP, así que no
hay riesgo de analizar algo de forma diferente. En un frontend HTTP o un backend HTTP, se garantiza
que los contenidos HTTP estarán siempre inmediatamente presentes cuando la regla se evalúe primero,
porque el análisis HTTP se realiza en las etapas tempranas del procesamiento de la conexión, a
nivel de sesión. Pero para tales proxies, usar reglas "http-request" es mucho más natural y
recomendable.

Rastrear información de capa 7 también es posible siempre que la información esté presente cuando
la regla se procesa. El motor de procesamiento de reglas es capaz de esperar hasta que expire el
retardo de inspección cuando los datos a rastrear aún no están disponibles.

Ejemplo:

```text
tcp-request content use-service lua.deny if { src -f /etc/haproxy/blacklist.lst }
```

Ejemplo:

```text
tcp-request content set-var(sess.my_var) src
tcp-request content set-var-fmt(sess.from) %[src]:%[src_port]
tcp-request content unset-var(sess.my_var2)
```

Ejemplo:

```shell
# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (Only works for HTTP/1 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 30s
tcp-request content accept if is_host_com
tcp-request content reject

# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (works for HTTP/1 and HTTP/2 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 5s
tcp-request content switch-mode http if HTTP
tcp-request content reject   # non-HTTP traffic is implicit here
...
http-request reject unless is_host_com
```

Ejemplo:

```shell
# reject SMTP connection if client speaks first
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content reject if content_present

# Forward HTTPS connection only if client speaks
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content accept if content_present
tcp-request content reject
```

Ejemplo:

```shell
# Track the last IP(stick-table type string) from X-Forwarded-For
tcp-request inspect-delay 10s
tcp-request content track-sc0 hdr(x-forwarded-for,-1)
# Or track the last IP(stick-table type ip|ipv6) from X-Forwarded-For
tcp-request content track-sc0 req.hdr_ip(x-forwarded-for,-1)
```

Ejemplo:

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content track-sc0 base table req-rate
```

Ejemplo: rastrear contadores por frontend y por backend, bloquear abusadores en el frontend
cuando el backend detecta abuso (y marca gpc0).

        frontend http
            # Use General Purpose Counter 0 in SC0 as a global abuse counter
            # protecting all our sites
            stick-table type ip size 1m expire 5m store gpc0
            tcp-request connection track-sc0 src
            tcp-request connection reject if { sc0_get_gpc0 gt 0 }
            ...
            use_backend http_dynamic if { path_end .php }

        backend http_dynamic
            # if a source makes too fast requests to this dynamic site (tracked
            # by SC1), block it globally in the frontend.
            stick-table type ip size 1m expire 5m store http_req_rate(10s)
            acl click_too_fast sc1_http_req_rate gt 10
            acl mark_as_abuser sc0_inc_gpc0(http) gt 0
            tcp-request content track-sc1 src
            tcp-request content reject if click_too_fast mark_as_abuser

Ver la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

Ver también: "tcp-request connection", "tcp-request session", "tcp-request inspect-delay", y
"http-request".

<a id="entry-4-2-tcp-request-inspect-delay"></a>

**`tcp-request inspect-delay <timeout>`**

```haproxy
tcp-request inspect-delay <timeout>
```

Define el máximo tiempo permitido para esperar datos durante la inspección de contenido

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Las personas que usan HAProxy principalmente como un relay TCP a menudo se preocupan por el riesgo
de pasar cualquier tipo de protocolo a un servidor sin ningún análisis. Para poder analizar el
contenido de la solicitud, primero debemos retener los datos y luego analizarlos. Esta instrucción
simplemente activa la retención de datos durante como máximo el tiempo especificado.

La inspección de contenido TCP se aplica muy temprano cuando una conexión llega a un frontend, y
luego muy temprano cuando la conexión se reenvía a un backend. Esto significa que una conexión
puede experimentar un primer retardo en el frontend y un segundo retardo en el backend si ambos
tienen reglas tcp-request.

Ten en cuenta que al realizar la inspección de contenido, HAProxy evaluará todas las reglas por
cada fragmento nuevo que entre, teniendo en cuenta el hecho de que esos datos son parciales. Si
ninguna regla coincide antes del retardo mencionado, se realiza una última comprobación al expirar
este, considerando esta vez que los contenidos son definitivos. Si no se establece ningún retardo,
HAProxy no esperará nada y aplicará inmediatamente un veredicto basado en la información
disponible. Obviamente, es poco probable que esto sea muy útil y podría incluso ser propenso a
condiciones de carrera, así que no se recomiendan tales configuraciones.

Ten en cuenta que el retardo de inspección se acorta si se produce un error o cierre de conexión o
si el búfer de la solicitud aparece lleno.

Tan pronto como una regla coincide, la solicitud se libera y continúa como de costumbre. Si se
alcanza el tiempo de espera y ninguna regla coincide, la política por defecto será dejarla pasar
sin afectarla.

Para la mayoría de los protocolos, basta con establecerlo en unos pocos segundos, ya que la
mayoría de los clientes envían la solicitud completa inmediatamente tras la conexión. Añade 3 o
más segundos para cubrir las retransmisiones TCP, pero eso es todo. Para algunos protocolos puede
tener sentido usar valores grandes, por ejemplo para asegurar que el cliente nunca hable antes
que el servidor (p. ej. SMTP), o para esperar a que hable un cliente antes de pasar los datos al
servidor (p. ej. SSL). Ten en cuenta que el tiempo de espera del cliente debe cubrir al menos el
retardo de inspección, de lo contrario expirará primero. Si el cliente cierra la conexión o si el
búfer está lleno, el retardo expira inmediatamente puesto que los contenidos ya no podrán cambiar.

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Los proxies
heredan este valor de su sección defaults.

Ver también: "tcp-request content accept", "tcp-request content reject", "timeout client".

<a id="entry-4-2-tcp-request-session"></a>

**`tcp-request session <action> [{if | unless} <condition>]`**

```haproxy
tcp-request session <action> [{if | unless} <condition>]
```

Realiza una acción sobre una sesión validada dependiendo de una condición de capa 5

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| sí \| sí \| no

Argumentos:

```text
<action>    define la acción a realizar si la condición se aplica. Ver
            abajo.

<condition> es una condición estándar basada en ACL solo de capa 5 (ver
            sección 7).
```

Una vez validada una sesión (es decir, después de que se hayan completado todos los handshakes),
es posible evaluar algunas condiciones para decidir si esa sesión debe aceptarse, descartarse o si
se debe rastrear sus contadores. Esas condiciones no pueden hacer uso de ningún contenido de
datos porque aún no hay búferes asignados y el procesamiento no puede esperar en esta etapa. El
caso de uso principal es copiar información temprana en variables (ya que las variables son
accesibles en la sesión), o mantener un registro de cierta información recopilada tras el
handshake, tal como elementos a nivel SSL (SNI, cifrados, CN del certificado del cliente) o
información de la cabecera del protocolo PROXY (p. ej. rastrear un origen reenviado de esta
forma). La información extraída puede así copiarse a una variable o rastrearse usando reglas
"track-sc". Por supuesto, también es posible decidir aceptar/rechazar como con otros conjuntos de
reglas. La mayoría de las operaciones realizadas aquí también podrían realizarse en reglas
"tcp-request content", excepto que en HTTP estas reglas se evalúan para cada nueva solicitud, y
eso podría no siempre ser aceptable. Por ejemplo, una regla podría incrementar un contador en
cada evaluación. También sería posible que un país se resuelva por geolocalización desde la
dirección IP de origen, se asigne a una variable de toda la sesión y luego se reescriba la
dirección de origen desde una cabecera HTTP para todas las solicitudes. Si es necesario inspeccionar
algún contenido para tomar la decisión, se deben usar en su lugar las instrucciones
"tcp-request content".

Las reglas "tcp-request session" se evalúan en su orden exacto de declaración. Si ninguna regla
coincide o si no hay ninguna regla, la acción por defecto es aceptar la sesión entrante. No hay
ningún límite específico al número de reglas que pueden insertarse.

La primera palabra clave después de "tcp-request session" en la sintaxis es la acción de la
regla, seguida opcionalmente de un número variable de argumentos para la acción. Las acciones
soportadas y sus respectivas sintaxis se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3)
"Acciones" (buscar las acciones que marcan "TCP RqSes").

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con la
capacidad frontend y por proxies con la capacidad backend. Esto significa que una sección listen
no puede usar una sección defaults que defina tales reglas.

Ten en cuenta que la condición "if/unless" es opcional. Si no se establece ninguna condición en la
acción, simplemente se realiza de forma incondicional. Esto puede ser útil para las acciones
"track-sc\*" así como para cambiar la acción por defecto a un rechazo.

Ejemplo: rastrear por defecto la dirección de origen original, o la anunciada en la cabecera del
protocolo PROXY para conexiones provenientes de los proxies locales. La primera regla a nivel de
conexión activa la recepción del protocolo PROXY para estas, la segunda regla rastrea cualquier
dirección que decidamos conservar tras la decodificación opcional.

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }
        tcp-request session track-sc0 src

Ejemplo: aceptar todas las sesiones de hosts en la lista blanca, rechazar sin contarlas las
sesiones demasiado rápidas y rastrear las sesiones aceptadas. Esto hace que la tasa de sesiones
quede limitada desde las fuentes abusivas.

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session reject if { src_sess_rate gt 10 }
        tcp-request session track-sc0 src

Ejemplo: aceptar todas las sesiones de hosts en la lista blanca, contar todas las demás sesiones
y rechazar las demasiado rápidas. Esto hace que las abusivas queden bloqueadas mientras no
reduzcan su velocidad.

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session track-sc0 src
        tcp-request session reject if { sc0_sess_rate gt 10 }

Ver la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

Ver también: "tcp-request connection", "tcp-request content", "stick-table"

<a id="entry-4-2-tcp-response-content"></a>

**`tcp-response content <action> [{if | unless} <condition>]`**

```haproxy
tcp-response content <action> [{if | unless} <condition>]
```

Realiza una acción sobre una respuesta de la sesión dependiendo de una condición de capas 4-7

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| no \| sí \| sí

Argumentos:

```text
<action>    define la acción a realizar si la condición se aplica. Ver
            abajo.

<condition> es una condición estándar basada en ACL de capas 4-7 (ver
            sección 7).
```

El contenido de las respuestas puede analizarse en una etapa temprana del procesamiento de la
respuesta llamada "inspección de contenido TCP". Durante esta etapa, las reglas basadas en ACL se
evalúan cada vez que el contenido de la respuesta se actualiza, hasta que una regla final
coincide, o hasta que se establece un tiempo de inspección de respuesta TCP y este expira sin
ninguna regla que coincida.

La mayoría de las veces, estas decisiones considerarán un reconocimiento de protocolo o su
validez.

Las reglas basadas en contenido se evalúan en su orden exacto de declaración. Si ninguna regla
coincide o si no hay ninguna regla, la acción por defecto es aceptar los contenidos. No hay
ningún límite específico al número de reglas que pueden insertarse.

La primera palabra clave después de "tcp-response content" en la sintaxis es la acción de la
regla, seguida opcionalmente de un número variable de argumentos para la acción. Las acciones
soportadas y sus respectivas sintaxis se enumeran en la [sección 4.3](/es/haproxy/proxies/#section-4-3)
"Acciones" (buscar las acciones que marcan "TCP RsCnt").

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Las reglas
definidas en la sección defaults se evalúan antes que las de la sección proxy asociada. Para evitar
ambigüedades, en este caso la misma sección defaults no puede ser usada por proxies con la
capacidad frontend y por proxies con la capacidad backend. Esto significa que una sección listen
no puede usar una sección defaults que defina tales reglas.

Ten en cuenta que la condición "if/unless" es opcional. Si no se establece ninguna condición en la
acción, simplemente se realiza de forma incondicional. Esto puede ser útil para cambiar la acción
por defecto a un rechazo.

Se soportan varios tipos de acciones:

Es perfectamente posible coincidir con contenidos de capa 7 usando reglas "tcp-response content",
pero entonces es importante asegurar que se haya bufferizado una respuesta completa, de lo
contrario ningún contenido coincidirá. Para lograrlo, la mejor solución implica detectar el
protocolo HTTP durante el período de inspección.

Ver la [sección 7](/es/haproxy/acls-and-samples/) sobre el uso de ACL.

Ver también: "tcp-request content", "tcp-response inspect-delay"

<a id="entry-4-2-tcp-response-inspect-delay"></a>

**`tcp-response inspect-delay <timeout>`**

```haproxy
tcp-response inspect-delay <timeout>
```

Define el máximo tiempo permitido para esperar una respuesta durante la inspección de contenido

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí(!) \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Esta directiva solo está disponible desde secciones defaults con nombre, no anónimas. Los proxies
heredan este valor de su sección defaults.

Ver también: "tcp-response content", "tcp-request inspect-delay".

<a id="entry-4-2-timeout-check"></a>

**`timeout check <timeout>`**

```haproxy
timeout check <timeout>
```

Define un tiempo de espera adicional para las comprobaciones, pero solo después de que una
conexión ya se haya establecido.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Si se establece, HAProxy usa min("timeout connect", "inter") como tiempo de espera de conexión
para la comprobación y "timeout check" como tiempo de espera de lectura adicional. Se usa "min"
para que las personas que funcionan con tiempos de espera de conexión *muy* largos (p. ej.
quienes lo necesitaban por la cola o el tarpit) no ralenticen sus comprobaciones. (Ten en cuenta
también que no hay ninguna razón válida para tener tiempos de espera de conexión tan largos,
porque "timeout queue" y "timeout tarpit" siempre pueden usarse para evitarlo).

Si "timeout check" no está establecido, HAProxy usa "inter" como tiempo de espera completo de la
comprobación (conexión + lectura) exactamente igual que todas las versiones \<1.3.15.

En la mayoría de los casos la solicitud de comprobación es mucho más simple y rápida de manejar
que las solicitudes normales y puede que se quiera expulsar a los servidores lentos, así que este
tiempo de espera debería ser menor que "timeout server".

Este parámetro es específico de los backends, pero puede especificarse una única vez para todos
en las secciones "defaults". De hecho, esta es una de las soluciones más sencillas para no
olvidarlo.

Ver también: "timeout connect", "timeout queue", "timeout server", "timeout tarpit".

<a id="entry-4-2-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

Define el máximo tiempo de inactividad en el lado del cliente.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

El tiempo de espera de inactividad se aplica cuando se espera que el cliente acuse recibo o envíe
datos. En modo HTTP, este tiempo de espera es particularmente importante de considerar durante la
primera fase, cuando el cliente envía la solicitud, y durante la respuesta mientras lee los datos
enviados por el servidor. Dicho esto, para la primera fase, es preferible establecer "timeout
http-request" para proteger mejor a HAProxy de ataques tipo Slowloris. El valor se especifica en
milisegundos por defecto, pero puede estar en cualquier otra unidad si el número lleva como
sufijo la unidad, tal como se especifica al principio de este documento. En modo TCP (y en menor
medida, en modo HTTP), es altamente recomendable que el tiempo de espera del cliente permanezca
igual al del servidor para evitar situaciones complejas de depurar. Es una buena práctica cubrir
una o varias pérdidas de paquetes TCP especificando tiempos de espera ligeramente superiores a
múltiplos de 3 segundos (p. ej. 4 o 5 segundos). Si se mezclan flujos de larga duración con
flujos de corta duración (p. ej. WebSocket y HTTP), vale la pena considerar "timeout tunnel", que
prevalece sobre "timeout client" y "timeout server" para los túneles, así como "timeout
client-fin" para conexiones semicerradas.

Este parámetro es específico de los frontends, pero puede especificarse una única vez para todos
en las secciones "defaults". De hecho, esta es una de las soluciones más sencillas para no
olvidarlo. Un tiempo de espera no especificado da como resultado un tiempo de espera infinito,
lo cual no está recomendado. Tal uso se acepta y funciona, pero informa de un aviso durante el
arranque porque puede provocar una acumulación de sesiones expiradas en el sistema si los
tiempos de espera del sistema tampoco están configurados.

Ver también: "timeout server", "timeout tunnel", "timeout http-request".

<a id="entry-4-2-timeout-client-fin"></a>

**`timeout client-fin <timeout>`**

```haproxy
timeout client-fin <timeout>
```

Define el tiempo de espera de inactividad en el lado del cliente para conexiones semicerradas.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

El tiempo de espera de inactividad se aplica cuando se espera que el cliente acuse recibo o envíe
datos mientras una dirección ya está cerrada. Este tiempo de espera es diferente de "timeout
client" en que solo se aplica a conexiones que están cerradas en una dirección. Esto es
particularmente útil para evitar mantener conexiones en estado FIN_WAIT durante demasiado tiempo
cuando los clientes no se desconectan limpiamente. Este problema es particularmente común en
conexiones largas tales como RDP o WebSocket. Ten en cuenta que este tiempo de espera puede
prevalecer sobre "timeout tunnel" cuando una conexión se cierra en una dirección. Se aplica a
conexiones HTTP/2 inactivas una vez que se ha enviado una trama GOAWAY, lo que a menudo indica la
expectativa de que la conexión termine rápidamente.

Este parámetro es específico de los frontends, pero puede especificarse una única vez para todos
en las secciones "defaults". Por defecto no está establecido, así que las conexiones semicerradas
usarán los otros tiempos de espera (timeout.client o timeout.tunnel).

Ver también: "timeout client", "timeout server-fin", y "timeout tunnel".

<a id="entry-4-2-timeout-client-hs"></a>

**`timeout client-hs <timeout>`**

```haproxy
timeout client-hs <timeout>
```

Define el máximo tiempo de espera para que se complete el handshake TLS del cliente. Esto es
utilizable tanto para conexiones TCP como QUIC.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Si este tiempo de espera de handshake no está establecido, es el tiempo de espera del cliente el
que se usa en su lugar.


<a id="entry-4-2-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

Define el máximo tiempo de espera para que un intento de conexión a un servidor tenga éxito.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Si el servidor está en la misma LAN que HAProxy, la conexión debería ser inmediata (menos de
unos pocos milisegundos). En cualquier caso, es una buena práctica cubrir una o varias pérdidas
de paquetes TCP especificando tiempos de espera ligeramente superiores a múltiplos de 3 segundos
(p. ej. 4 o 5 segundos). Por defecto, el tiempo de espera de conexión también preestablece los
tiempos de espera de cola y de tarpit al mismo valor si estos no han sido especificados.

Este parámetro es específico de los backends, pero puede especificarse una única vez para todos
en las secciones "defaults". De hecho, esta es una de las soluciones más sencillas para no
olvidarlo. Un tiempo de espera no especificado da como resultado un tiempo de espera infinito,
lo cual no está recomendado. Tal uso se acepta y funciona, pero informa de un aviso durante el
arranque porque puede provocar una acumulación de sesiones fallidas en el sistema si los tiempos
de espera del sistema tampoco están configurados.

Ver también: "timeout check", "timeout queue", "timeout server", "timeout tarpit".

<a id="entry-4-2-timeout-http-keep-alive"></a>

**`timeout http-keep-alive <timeout>`**

```haproxy
timeout http-keep-alive <timeout>
```

Define el máximo tiempo permitido para esperar que aparezca una nueva solicitud HTTP

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Por defecto, el tiempo de espera de una nueva solicitud en caso de keep-alive lo establece
"timeout http-request". Sin embargo, esto no siempre es conveniente porque algunas personas
quieren tiempos de espera de keep-alive muy cortos para liberar conexiones más rápido, y otras
prefieren tenerlos más grandes pero manteniendo tiempos de espera cortos una vez que la solicitud
ha empezado a presentarse.

El tiempo de espera "http-keep-alive" cubre estas necesidades. Definirá cuánto esperar a que una
nueva solicitud HTTP empiece a llegar después de que se haya enviado una respuesta. Una vez que
se ha visto el primer byte de la solicitud, se usa el tiempo de espera "http-request" para
esperar a que llegue la solicitud completa. Ten en cuenta que las líneas vacías previas a una
nueva solicitud no refrescan el tiempo de espera y no se cuentan como una nueva solicitud.

Existe también otra diferencia entre los dos tiempos de espera: cuando una conexión expira
durante el tiempo de espera http-keep-alive, no se devuelve ningún error, la conexión
simplemente se cierra. Si la conexión expira en "http-request" mientras se espera a que se
complete una solicitud, se devuelve un error HTTP 408 al cliente antes de cerrar la conexión, a
menos que "option http-ignore-probes" esté establecido en el frontend.

En general, "timeout http-keep-alive" se usa mejor para evitar que los clientes mantengan
demasiado tiempo abierta una conexión de otro modo inactiva en sitios que ven grandes cantidades
de conexiones cortas. Esto puede lograrse estableciendo el valor en unas decenas o cientos de
milisegundos en HTTP/1.1. Esto cerrará la conexión después de que el cliente solicite una página
sin tener que mantener esa conexión abierta esperando más actividad del cliente. En ese
escenario, una nueva actividad del navegador daría lugar a un nuevo handshake en la capa TCP
y/o SSL. Un caso de uso común para esto son los sitios HTTP que sirven únicamente una
redirección a la página HTTPS. Es mejor no mantener tales conexiones inactivas demasiado tiempo
porque no se reutilizarán, salvo quizás para recuperar un favicon.

Otro caso de uso es exactamente el opuesto: algunos sitios quieren permitir que los clientes
reutilicen conexiones inactivas durante mucho tiempo (p. ej. de 30 segundos a un minuto) pero no
quieren esperar tanto por la primera solicitud, para evitar un vector de ataque muy barato. En
este caso, el tiempo de espera http-keep-alive se establecería en un valor grande, pero
http-request permanecería bajo (unos pocos segundos).

Cuando se establece en un valor muy pequeño, es probable que las solicitudes adicionales que no
se envíen en secuencia sin esperar las respuestas (pipelining) se manejen por otra conexión, a menos que las solicitudes estén
realmente encadenadas de ese modo, lo cual es muy raro con HTTP/1.1 (solicitudes enviadas de forma consecutiva
sin esperar una respuesta). La mayoría de las implementaciones HTTP/1.1 envían una solicitud,
esperan una respuesta y luego envían otra solicitud. Un valor pequeño aquí para HTTP/1.1 puede
ser ventajoso para usar menos memoria y sockets en sitios con cientos de miles de clientes, a
costa de un aumento en los costos de cómputo del handshake.

Se debe tener especial cuidado con los valores pequeños cuando se trata con HTTP/2. La
naturaleza de HTTP/2 es multiplexar solicitudes sobre una conexión para ahorrar la sobrecarga
de reconectar las capas TCP y/o SSL. El protocolo también usa tramas de control que se manejan
mal con cierres tempranos de conexiones TCP; en raras ocasiones esto puede dar como resultado
respuestas truncadas cuando los datos se destruyen en vuelo después de salir de HAProxy (que
entonces ni siquiera puede registrar un error). Un valor inicial bajo sugerido para conexiones
HTTP/2 sería de unos 4 segundos. Esto evitaría que la mayoría de las implementaciones modernas
de keep-alive mantengan innecesariamente abiertas conexiones caducas, y al mismo tiempo
permitiría que solicitudes posteriores reutilicen la conexión. Sin embargo, esto debería
ajustarse según sea necesario y es simplemente un punto de partida.

Si este parámetro no está establecido, se aplica el tiempo de espera "http-request", y si
ninguno de los dos está establecido, "timeout client" sigue aplicándose en el nivel inferior.
Debe establecerse en el frontend para que surta efecto, salvo que el frontend esté en modo TCP,
en cuyo caso se usará el tiempo de espera del backend HTTP.

Ver también: "timeout http-request", "timeout client".

<a id="entry-4-2-timeout-http-request"></a>

**`timeout http-request <timeout>`**

```haproxy
timeout http-request <timeout>
```

Define el máximo tiempo permitido para esperar una solicitud HTTP completa

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Para ofrecer protección DoS, puede ser necesario reducir el máximo tiempo aceptado para recibir
una solicitud HTTP completa sin afectar al tiempo de espera del cliente. Esto ayuda a protegerse
contra conexiones establecidas en las que no se envía nada. El tiempo de espera del cliente no
puede ofrecer una buena protección contra este abuso porque es un tiempo de espera de
inactividad, lo que significa que si el atacante envía un carácter de vez en cuando, el tiempo
de espera no se disparará. Con el tiempo de espera de solicitud HTTP, sin importar a qué
velocidad escriba el cliente, la solicitud se abortará si no se completa a tiempo. Cuando el
tiempo de espera expira, se envía una respuesta HTTP 408 al cliente para informarle del
problema, y la conexión se cierra. Los registros informarán los códigos de terminación "cR".
Algunos navegadores recientes tienen problemas con este comportamiento estándar y bien
documentado, así que podría ser necesario ocultar el código 408 usando "option
http-ignore-probes" o "errorfile 408 /dev/null". Ver más detalles en las explicaciones del
código de terminación "cR" en la [sección 8.5](/es/haproxy/configuration-logging/#section-8-5).

Por defecto, este tiempo de espera solo se aplica a la parte de cabeceras de la solicitud, y no
a ningún dato. Tan pronto como se recibe la línea vacía, este tiempo de espera ya no se usa.
Cuando se combina con "option http-buffer-request", este tiempo de espera también se aplica al
cuerpo de la solicitud.. Se usa de nuevo en conexiones keep-alive para esperar una segunda
solicitud si "timeout http-keep-alive" no está establecido.

Generalmente basta con establecerlo en unos pocos segundos, ya que la mayoría de los clientes
envían la solicitud completa inmediatamente tras la conexión. Añade 3 o más segundos para cubrir
las retransmisiones TCP, pero eso es todo. Establecerlo en valores muy bajos (p. ej. 50 ms)
generalmente funcionará en redes locales siempre que no haya pérdidas de paquetes. Esto evitará
que la gente envíe solicitudes HTTP crudas usando telnet.

Si este parámetro no está establecido, el tiempo de espera del cliente sigue aplicándose entre
cada fragmento de la solicitud entrante. Debe establecerse en el frontend para que surta
efecto, salvo que el frontend esté en modo TCP, en cuyo caso se usará el tiempo de espera del
backend HTTP.

Ver también: "errorfile", "http-ignore-probes", "timeout http-keep-alive", y "timeout client",
"option http-buffer-request".

<a id="entry-4-2-timeout-queue"></a>

**`timeout queue <timeout>`**

```haproxy
timeout queue <timeout>
```

Define el máximo tiempo de espera en la cola para que se libere un hueco de conexión

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Cuando se alcanza el maxconn de un servidor, las conexiones quedan pendientes en una cola que
puede ser específica del servidor o global para el backend. Para no esperar indefinidamente, se
aplica un tiempo de espera a las solicitudes pendientes en la cola. Si se alcanza el tiempo de
espera, se considera que la solicitud casi nunca será atendida, así que se descarta y se
devuelve un error 503 al cliente.

La instrucción "timeout queue" permite fijar el máximo tiempo durante el cual una solicitud
puede quedar pendiente en una cola. Si no se especifica, se usa el mismo valor que el tiempo de
espera de conexión del backend ("timeout connect"), por compatibilidad con versiones antiguas
que no tienen el parámetro "timeout queue".

Ver también: "timeout connect".

<a id="entry-4-2-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

Define el máximo tiempo de inactividad en el lado del servidor.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

El tiempo de espera de inactividad se aplica cuando se espera que el servidor acuse recibo o
envíe datos. En modo HTTP, este tiempo de espera es particularmente importante de considerar
durante la primera fase de la respuesta del servidor, cuando debe enviar las cabeceras, ya que
representa directamente el tiempo de procesamiento del servidor para la solicitud. Para averiguar
qué valor poner ahí, a menudo es bueno partir de lo que se consideraría tiempos de respuesta
inaceptables, luego comprobar los registros para observar la distribución de los tiempos de
respuesta y ajustar el valor en consecuencia.

El valor se especifica en milisegundos por defecto, pero puede estar en cualquier otra unidad si
el número lleva como sufijo la unidad, tal como se especifica al principio de este documento. En
modo TCP (y en menor medida, en modo HTTP), es altamente recomendable que el tiempo de espera
del cliente permanezca igual al del servidor para evitar situaciones complejas de depurar.
Cualesquiera que sean los tiempos de respuesta esperados del servidor, es una buena práctica
cubrir al menos una o varias pérdidas de paquetes TCP especificando tiempos de espera
ligeramente superiores a múltiplos de 3 segundos (p. ej. 4 o 5 segundos como mínimo). Si se
mezclan flujos de larga duración con flujos de corta duración (p. ej. WebSocket y HTTP), vale
la pena considerar "timeout tunnel", que prevalece sobre "timeout client" y "timeout server"
para los túneles.

Este parámetro es específico de los backends, pero puede especificarse una única vez para todos
en las secciones "defaults". De hecho, esta es una de las soluciones más sencillas para no
olvidarlo. Un tiempo de espera no especificado da como resultado un tiempo de espera infinito,
lo cual no está recomendado. Tal uso se acepta y funciona, pero informa de un aviso durante el
arranque porque puede provocar una acumulación de sesiones expiradas en el sistema si los
tiempos de espera del sistema tampoco están configurados.

Ver también: "timeout client" y "timeout tunnel".

<a id="entry-4-2-timeout-server-fin"></a>

**`timeout server-fin <timeout>`**

```haproxy
timeout server-fin <timeout>
```

Define el tiempo de espera de inactividad en el lado del servidor para conexiones semicerradas.

Puede usarse en los siguientes contextos: tcp, http, log

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

El tiempo de espera de inactividad se aplica cuando se espera que el servidor acuse recibo o
envíe datos mientras una dirección ya está cerrada. Este tiempo de espera es diferente de
"timeout server" en que solo se aplica a conexiones que están cerradas en una dirección. Esto
es particularmente útil para evitar mantener conexiones en estado FIN_WAIT durante demasiado
tiempo cuando un servidor remoto no se desconecta limpiamente. Este problema es particularmente
común en conexiones largas tales como RDP o WebSocket. Ten en cuenta que este tiempo de espera
puede prevalecer sobre "timeout tunnel" cuando una conexión se cierra en una dirección. Este
ajuste se proporcionó por exhaustividad, pero en la mayoría de las situaciones no debería ser
necesario.

Este parámetro es específico de los backends, pero puede especificarse una única vez para todos
en las secciones "defaults". Por defecto no está establecido, así que las conexiones
semicerradas usarán los otros tiempos de espera (timeout.server o timeout.tunnel).

Ver también: "timeout client-fin", "timeout server", y "timeout tunnel".

<a id="entry-4-2-timeout-tarpit"></a>

**`timeout tarpit <timeout>`**

```haproxy
timeout tarpit <timeout>
```

Define la duración durante la cual se mantendrán las conexiones en tarpit

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<timeout> es la duración del tarpit especificada en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Cuando una conexión se pone en tarpit usando "http-request tarpit", se mantiene abierta sin
actividad durante cierto tiempo y luego se cierra. "timeout tarpit" define cuánto tiempo se
mantendrá abierta.

El valor se especifica en milisegundos por defecto, pero puede estar en cualquier otra unidad si
el número lleva como sufijo la unidad, tal como se especifica al principio de este documento. Si
no se especifica, se usa el mismo valor que el tiempo de espera de conexión del backend
("timeout connect"), por compatibilidad con versiones antiguas que no tienen el parámetro
"timeout tarpit".

Ver también: "timeout connect".

<a id="entry-4-2-timeout-tunnel"></a>

**`timeout tunnel <timeout>`**

```haproxy
timeout tunnel <timeout>
```

Define el máximo tiempo de inactividad en el lado del cliente y del servidor para los túneles.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

El tiempo de espera de túnel se aplica cuando se establece una conexión bidireccional entre un
cliente y un servidor, y la conexión permanece inactiva en ambas direcciones. Este tiempo de
espera sustituye tanto al tiempo de espera del cliente como al del servidor una vez que la
conexión se convierte en un túnel. En TCP, este tiempo de espera se usa tan pronto como no queda
ningún analizador adjunto a ninguna de las conexiones (p. ej. las reglas de contenido tcp se
aceptan). En HTTP, este tiempo de espera se usa cuando una conexión cambia de protocolo (p. ej. al
cambiar al protocolo WebSocket, o al reenviar una solicitud CONNECT a un proxy), o después de la
primera respuesta cuando no se especifica ninguna opción keepalive/close.

Dado que este tiempo de espera se usa generalmente junto con conexiones de larga duración,
usualmente es buena idea establecer también "timeout client-fin" para manejar la situación en
la que un cliente desaparece repentinamente de la red y no acusa recibo de un cierre, o envía
un shutdown y deja de acusar recibo de los datos pendientes. Esto puede ocurrir en redes con
pérdidas donde hay firewalls, y se detecta por la presencia de grandes cantidades de sesiones
en estado FIN_WAIT.

El valor se especifica en milisegundos por defecto, pero puede estar en cualquier otra unidad si
el número lleva como sufijo la unidad, tal como se especifica al principio de este documento.
Cualquiera que sea el tiempo de inactividad normal esperado, es una buena práctica cubrir al
menos una o varias pérdidas de paquetes TCP especificando tiempos de espera ligeramente
superiores a múltiplos de 3 segundos (p. ej. 4 o 5 segundos como mínimo).

Este parámetro es específico de los backends, pero puede especificarse una única vez para todos
en las secciones "defaults". De hecho, esta es una de las soluciones más sencillas para no
olvidarlo.

Ejemplo:

```text
defaults http
    option http-server-close
    timeout connect 5s
    timeout client 30s
    timeout client-fin 30s
    timeout server 30s
    timeout tunnel  1h    # timeout to use with WebSocket and CONNECT
```

Ver también: "timeout client", "timeout client-fin", "timeout server".

<a id="entry-4-2-transparent"></a>

**`transparent (deprecated)`**

```haproxy
transparent (deprecated)
```

Activa el proxying transparente en el lado del cliente

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| no \| sí \| sí

Argumentos: ninguno

Esta palabra clave se introdujo para proporcionar persistencia de capa 7 a balanceadores de
carga de capa 3. La idea es usar la capacidad del SO de redirigir una conexión entrante dirigida
a una dirección remota hacia un proceso local (aquí HAProxy), y hacer que este proceso sepa qué
dirección se solicitó inicialmente. Cuando se usa esta opción, las sesiones sin cookies se
reenviarán a la dirección IP de destino original de la solicitud entrante (que debería
corresponder a la de otro equipo), mientras que las solicitudes con cookies seguirán
reenviándose al servidor apropiado.

La palabra clave "transparent" está obsoleta, usa "option transparent" en su lugar.

Ten en cuenta que, contrariamente a una creencia común, esta opción NO hace que HAProxy
presente la IP del cliente al servidor al establecer la conexión.

Ver también: "option transparent"

<a id="entry-4-2-unique-id-format"></a>

**`unique-id-format <fmt>`**

```haproxy
unique-id-format <fmt>
```

Genera un identificador único para cada solicitud.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| sí

Argumentos:

```text
<fmt>   es una cadena en formato de registro personalizado (ver sección 8.2.6).
```

Esta palabra clave crea un ID para cada solicitud usando el formato de registro personalizado.
Un identificador único es útil para rastrear una solicitud que pasa por muchos componentes de
una infraestructura compleja. El ID recién creado también puede registrarse usando el alias %ID
en la cadena de formato de registro personalizado.

El formato debería componerse a partir de elementos que se garantiza que son únicos cuando se
combinan. Por ejemplo, si hay múltiples instancias de HAProxy involucradas, podría ser
importante incluir el nombre del nodo. A menudo es necesario registrar las direcciones y
puertos de origen y destino de la conexión entrante. Ten en cuenta que como múltiples
solicitudes pueden realizarse sobre la misma conexión, incluir un contador de solicitudes puede
ayudar a diferenciarlas. De forma similar, una marca de tiempo puede proteger contra un
desbordamiento del contador. Registrar el ID del proceso evitará colisiones tras un reinicio
del servicio.

Se recomienda usar la notación hexadecimal para muchos campos ya que los hace más compactos y
ahorra espacio en los registros.

Para las conexiones regulares se usa el formato configurado en el frontend para generar el
identificador único. Para las comprobaciones de estado se usa el formato del backend cuando se
usa el fetch "unique-id" dentro de un conjunto de reglas tcp-check o http-check.

Ejemplo:

```text
unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid

generará:

       7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A
```

Ver también: "unique-id-header"

<a id="entry-4-2-unique-id-header"></a>

**`unique-id-header <name>`**

```haproxy
unique-id-header <name>
```

Añade una cabecera de identificador único en la solicitud HTTP.

Puede usarse en los siguientes contextos: http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend sí \| sí \| sí \| no

Argumentos:

```text
<name>   es el nombre de la cabecera.
```

Añade una cabecera unique-id en la solicitud HTTP enviada al servidor, usando el
unique-id-format. No puede funcionar si el unique-id-format no existe.

Ejemplo:

```text
    unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid
    unique-id-header X-Unique-ID

    generará:

       X-Unique-ID: 7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A

Ver también: "unique-id-format"
```

<a id="entry-4-2-use-backend"></a>

**`use_backend <backend> [{if | unless} <condition>]`**

```haproxy
use_backend <backend> [{if | unless} <condition>]
```

Cambia a un backend específico si se cumple o no una condición basada en ACL, según se use if o unless.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| sí \| sí \| no

Argumentos:

```text
<backend>   es el nombre de un backend válido o de una sección "listen", o
            un formato de registro personalizado que se resuelve a un nombre de backend
            (ver formato de registro personalizado en la sección 8.2.6).

<condition> es una condición compuesta de ACLs, como se describe en la
            sección 7. Si se omite, la regla se aplica de forma
            incondicional.
```

Al hacer conmutación de contenido, las conexiones llegan a un frontend y luego se reparten
entre varios backends dependiendo de una serie de condiciones. La relación entre las condiciones
y los backends se describe con la palabra clave "use_backend". Aunque normalmente se usa con
procesamiento HTTP, también puede usarse en TCP puro, ya sea sin contenido usando ACLs sin
estado (p. ej. validación de la dirección de origen) o combinado con una regla "tcp-request"
para esperar cierta carga útil.

Puede haber tantas reglas "use_backend" como se desee. Todas estas reglas se evalúan en su orden
de declaración, y la primera que coincida asignará el backend. Esto ocurre incluso si el backend
se considera caído. Sin embargo, si una regla que coincide apunta a un backend deshabilitado o
no publicado, se ignora y la evaluación de las reglas continúa.

En la primera forma, el backend se usará si la condición se cumple. En la segunda forma, el
backend se usará si la condición no se cumple. Si ninguna condición es válida, se usará el
backend definido con "default_backend" a menos que esté deshabilitado o no publicado. Si no hay
ningún backend por defecto disponible, o se usan los servidores de la misma sección (en el caso
de una sección "listen") o, en el caso de un frontend, no se usa ningún servidor y se devuelve
una respuesta 503 servicio no disponible.

Ten en cuenta que es posible cambiar de un frontend TCP a un backend HTTP. En este caso, o el
frontend ya ha comprobado que el protocolo es HTTP y el procesamiento del backend seguirá
inmediatamente, o el backend esperará a que entre una solicitud HTTP completa. Esta función es
útil cuando un frontend debe decodificar varios protocolos en un puerto único, siendo uno de
ellos HTTP.

Cuando `<backend>` es un nombre simple, se resuelve en el momento de la configuración, y se
informa de un error si el backend especificado no existe. Si `<backend>` es un formato de registro personalizado, no puede hacerse ninguna comprobación en el momento de la configuración, así que el
nombre del backend se resuelve dinámicamente en tiempo de ejecución. Si el nombre de backend
resultante no corresponde a ningún backend válido, no se evalúa ninguna otra regla y se aplica
en su lugar la directiva default_backend. Ten en cuenta que al usar nombres dinámicos de
backend, es altamente recomendable usar un prefijo que ningún otro backend use para asegurar
que no se pueda forzar un backend no autorizado desde la solicitud.

Merece la pena mencionar que las reglas "use_backend" con un nombre explícito se usan para
detectar la asociación entre frontends y backends para calcular el ajuste "fullconn" del
backend. Esto no puede hacerse para nombres dinámicos.

Ver también: "default_backend", "tcp-request", "fullconn", "log-format", y la [sección 7](/es/haproxy/acls-and-samples/) sobre ACL.

<a id="entry-4-2-use-fcgi-app"></a>

**`use-fcgi-app <name>`**

```haproxy
use-fcgi-app <name>
```

Define la aplicación FastCGI a usar para el backend.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<name>    es el nombre de la aplicación FastCGI a usar.
```

Ver la [sección 10.1](/es/haproxy/fastcgi/#section-10-1) sobre la configuración de aplicaciones FastCGI para más detalles.

<a id="entry-4-2-use-server"></a>

**`use-server <server> if <condition>`**

```haproxy
use-server <server> if <condition>
use-server <server> unless <condition>
```

Usa un servidor específico únicamente si se cumple o no una condición basada en ACL, según se use if o unless.

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

Argumentos:

```text
<server>    es el nombre de un servidor válido en la misma sección
            backend o una cadena en formato de registro personalizado que se resuelve a un
            nombre de servidor (ver sección 8.2.6).

<condition> es una condición compuesta de ACLs, como se describe en la
            sección 7.
```

Por defecto, las conexiones que llegan a un backend se equilibran entre los servidores
disponibles según el algoritmo configurado, a menos que se use un mecanismo de persistencia tal
como una cookie y se encuentre en la solicitud.

A veces es deseable reenviar una solicitud en particular a un servidor específico sin tener que
declarar un backend dedicado para ese servidor. Esto puede lograrse usando las reglas
"use-server". Estas reglas se evalúan después de las reglas "redirect" y antes de evaluar las
cookies, y tienen precedencia sobre ellas. Puede haber tantas reglas "use-server" como se
desee. Todas estas reglas se evalúan en su orden de declaración, y la primera que coincida
asignará el servidor.

Si una regla designa un servidor que está caído, y no se usa "option persist" y ninguna regla
force-persist fue validada, se ignora y la evaluación continúa con las siguientes reglas hasta
que una coincida.

En la primera forma, el servidor se usará si la condición se cumple. En la segunda forma, el
servidor se usará si la condición no se cumple. Si ninguna condición es válida, el procesamiento
continúa y el servidor se asignará según otros mecanismos de persistencia.

Ten en cuenta que incluso si una regla coincide, el procesamiento de cookies todavía se realiza
pero no asigna el servidor. Esto permite que las cookies con prefijo vean su prefijo eliminado.

La instrucción "use-server" funciona tanto en modo HTTP como TCP. Esto la hace adecuada para su
uso con inspección basada en contenido. Por ejemplo, un servidor podría seleccionarse en una
granja según el campo SNI de TLS al usar protocolos con TLS implícito (ver también
"req.ssl_sni"). Y si estos servidores tienen su peso establecido a cero, no se usarán para otro
tráfico.

Ejemplo:

```shell
# intercept incoming TLS requests based on the SNI field
use-server www if { req.ssl_sni -i www.example.com }
server     www 192.168.0.1:443 weight 0
use-server mail if { req.ssl_sni -i mail.example.com }
server     mail 192.168.0.1:465 weight 0
use-server imap if { req.ssl_sni -i imap.example.com }
server     imap 192.168.0.1:993 weight 0
# all the rest is forwarded to this server
server  default 192.168.0.2:443 check
```

Cuando `<server>` es un nombre simple, se comprueba contra los servidores existentes en la
configuración y se informa de un error si el servidor especificado no existe. Si es un formato de registro personalizado, no se realiza ninguna comprobación al analizar la configuración, y si no podemos
resolver un nombre de servidor válido en tiempo de ejecución pero la regla use-server estuvo
condicionada por una ACL que devuelve true, no se aplica ninguna otra regla use-server y
pasamos al balanceo de carga.

Ver también: "use_backend", la [sección 5](/es/haproxy/bind-and-server-options/) sobre servidores y la [sección 7](/es/haproxy/acls-and-samples/) sobre ACL.

## 4.3. Matriz de palabras clave de acciones {#section-4-3}

Varios conjuntos de reglas se evalúan en diversas etapas del procesamiento de la solicitud o de
la respuesta, y para cada regla encontrada en estos conjuntos de reglas, se puede ejecutar una
acción si se cumple la condición opcional.

Se proporciona por defecto un gran número de acciones, que pueden modificar contenidos,
aceptar/bloquear el procesamiento, cambiar estados internos, etc. Y es posible definir nuevas
acciones en Lua (en cuyo caso sus nombres siempre llevarán el prefijo "lua.").

Aunque históricamente algunas acciones solo existían en conjuntos de reglas específicos, hoy en
día muchas acciones son utilizables con muchos conjuntos de reglas. El listado de esta sección
indicará para cada acción soportada dónde puede usarse, marcando los nombres abreviados de
entrada correspondientes entre los siguientes conjuntos de reglas:

- QUIC Ini: la acción es válida para las reglas "quic-initial"
- TCP RqCon: la acción es válida para las reglas "tcp-request connection"
- TCP RqSes: la acción es válida para las reglas "tcp-request session"
- TCP RqCnt: la acción es válida para las reglas "tcp-request content"
- TCP RsCnt: la acción es válida para las reglas "tcp-response content"
- HTTP Req: la acción es válida para las reglas "http-request"
- HTTP Res: la acción es válida para las reglas "http-response"
- HTTP Aft: la acción es válida para las reglas "http-after-response"

Las mismas abreviaturas se usan en la referencia [sección 4.4](/es/haproxy/proxies/#section-4-4) a continuación.

```text
 palabra clave          QUIC: Ini   TCP: RqCon RqSes RqCnt RsCnt   HTTP: Req Res Aft
----------------------+-----------+-----------+-----+-----+------+----------+---+----
accept                         X           X     X     X     X            -   -   -
add-acl                        -           -     -     -     -            X   X   -
add-header                     -           -     -     -     -            X   X   X
add-headers-bin                -           -     -     -     -            X   X   X
allow                          -           -     -     -     -            X   X   X
attach-srv                     -           -     X     -     -            -   -   -
auth                           -           -     -     -     -            X   -   -
cache-store                    -           -     -     -     -            -   X   -
cache-use                      -           -     -     -     -            X   -   -
capture                        -           -     -     X     -            X   X   X
close                          -           -     -     -     X            -   -   -
del-acl                        -           -     -     -     -            X   X   -
del-header                     -           -     -     -     -            X   X   X
del-headers-bin                -           -     -     -     -            X   X   X
del-map                        -           -     -     -     -            X   X   X
deny                           -           -     -     -     -            X   X   -
dgram-drop                     X           -     -     -     -            -   -   -
disable-l7-retry               -           -     -     -     -            X   -   -
do-log                         X           X     X     X     X            X   X   X
do-resolve                     -           -     -     X     -            X   -   -
early-hint                     -           -     -     -     -            X   -   -
expect-netscaler-cip           -           X     -     -     -            -   -   -
expect-proxy layer4            -           X     -     -     -            -   -   -
normalize-uri                  -           -     -     -     -            X   -   -
pause                          -           -     -     -     -            X   X   -
redirect                       -           -     -     -     -            X   X   -
reject                         X           X     X     X     X            X   -   -
replace-header                 -           -     -     -     -            X   X   X
replace-path                   -           -     -     -     -            X   -   -
replace-pathq                  -           -     -     -     -            X   -   -
replace-uri                    -           -     -     -     -            X   -   -
replace-value                  -           -     -     -     -            X   X   X
return                         -           -     -     -     -            X   X   -
sc-add-gpc                     -           X     X     X     X            X   X   X
--palabra clave---------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-sc-inc-gpc                     -           X     X     X     X            X   X   X
sc-inc-gpc0                    -           X     X     X     X            X   X   X
sc-inc-gpc1                    -           X     X     X     X            X   X   X
sc-set-gpt                     -           X     X     X     X            X   X   X
sc-set-gpt0                    -           X     X     X     X            X   X   X
send-retry                     X           -     -     -     -            -   -   -
send-spoe-group                -           -     -     X     X            X   X   -
set-bandwidth-limit            -           -     -     X     X            X   X   -
set-bc-mark                    -           -     -     X     -            X   -   -
set-bc-tos                     -           -     -     X     -            X   -   -
set-dst                        -           X     X     X     -            X   -   -
set-dst-port                   -           X     X     X     -            X   -   -
set-fc-mark                    -           X     X     X     X            X   X   -
set-fc-tos                     -           X     X     X     X            X   X   -
set-header                     -           -     -     -     -            X   X   X
set-headers-bin                -           -     -     -     -            X   X   X
set-log-level                  -           -     -     X     X            X   X   X
set-map                        -           -     -     -     -            X   X   X
set-mark (deprecated)          -           X     X     X     X            X   X   -
set-method                     -           -     -     -     -            X   -   -
set-nice                       -           -     -     X     X            X   X   -
set-path                       -           -     -     -     -            X   -   -
set-pathq                      -           -     -     -     -            X   -   -
set-priority-class             -           -     -     X     -            X   -   -
set-priority-offset            -           -     -     X     -            X   -   -
--palabra clave---------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-set-query                      -           -     -     -     -            X   -   -
set-retries                    -           -     -     X     -            X   -   -
set-src                        -           X     X     X     -            X   -   -
set-src-port                   -           X     X     X     -            X   -   -
set-status                     -           -     -     -     -            -   X   X
set-timeout                    -           -     -     -     -            X   X   -
set-tos (deprecated)           -           X     X     X     X            X   X   -
set-uri                        -           -     -     -     -            X   -   -
set-var                        -           X     X     X     X            X   X   X
set-var-fmt                    -           X     X     X     X            X   X   X
silent-drop                    -           X     X     X     X            X   X   -
strict-mode                    -           -     -     -     -            X   X   X
switch-mode                    -           -     -     X     -            -   -   -
tarpit                         -           -     -     -     -            X   -   -
track-sc0                      -           X     X     X     -            X   X   -
track-sc1                      -           X     X     X     -            X   X   -
track-sc2                      -           X     X     X     -            X   X   -
unset-var                      -           X     X     X     X            X   X   X
use-service                    -           -     -     X     -            X   -   -
wait-for-body                  -           -     -     -     -            X   X   -
wait-for-handshake             -           -     -     -     -            X   -   -
--palabra clave---------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-
```

## 4.4. Referencia de acciones ordenadas alfabéticamente {#section-4-4}

Esta sección proporciona una descripción detallada de cada acción y su uso, usando el mismo
marcado de terminología de conjuntos de reglas descrito en la [sección 4.3](/es/haproxy/proxies/#section-4-3) anterior.

<a id="entry-4-4-accept"></a>

**`accept`**

```haproxy
accept
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| - \| - \| -

Esto detiene la evaluación de las reglas y deja pasar la solicitud o la respuesta por la
comprobación. Esta acción es final, es decir, no se evalúan más reglas del mismo conjunto de
reglas para la sección actual. No hay diferencia entre esta y la acción "allow" salvo que, por
compatibilidad histórica, "accept" se usa para las reglas TCP y QUIC y "allow" para las reglas
HTTP. Ver también la acción "allow" a continuación.

<a id="entry-4-4-add-acl"></a>

**`add-acl(<file-name>) <key fmt>`**

```haproxy
add-acl(<file-name>) <key fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto se usa para añadir una nueva entrada en una ACL. La ACL debe cargarse desde un archivo
(incluso un archivo vacío de relleno). El nombre del archivo de la ACL que se va a actualizar se
pasa entre paréntesis. Toma un argumento: `<key fmt>`, que sigue las reglas del formato de registro personalizado descritas en la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6), para recopilar el contenido de la nueva
entrada. Realiza una búsqueda en la ACL antes de la inserción, para evitar valores duplicados (o
más). Es el equivalente del comando "add acl" del socket de estadísticas, pero puede
dispararse por una solicitud HTTP.

<a id="entry-4-4-add-header"></a>

**`add-header <name> <fmt>`**

```haproxy
add-header <name> <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto añade un campo de cabecera HTTP cuyo nombre se especifica en `<name>` y cuyo valor está
definido por `<fmt>`, que sigue las reglas del formato de registro personalizado (ver formato de registro personalizado en la
[sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)). Esto es particularmente útil para pasar información
específica de la conexión al servidor (p. ej. el certificado SSL del cliente), o para combinar
varias cabeceras en una. Esta regla no es final, así que es posible añadir otras reglas
similares. Ten en cuenta que la adición de la cabecera se realiza inmediatamente, así que una
regla podría reutilizar la cabecera resultante de una regla anterior.

<a id="entry-4-4-add-headers-bin"></a>

**`add-headers-bin <expr> [ prefix <str> ]`**

```haproxy
add-headers-bin <expr> [ prefix <str> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Es una variante de la acción "add-header" donde los nombres y valores de las cabeceras se pasan
como una cadena binaria codificada en varint. Ver el fetch de muestras "req.hdrs_bin" sobre el
formato varint. Esto es útil cuando quieres establecer varias cabeceras a la vez, sin tener que
conocer de antemano los nombres de las cabeceras. Ten en cuenta que estas cabeceras no han sido
validadas por el analizador HTTP y podrían llevar a emitir mensajes no válidos y, en el peor de
los casos, a ataques de request smuggling. El número de cabeceras insertadas también es
importante, ya que está limitado por tune.http.maxhdr. El prefijo opcional solo establecerá las
cabeceras de la cadena codificada que empiecen por `<str>`.

Ejemplo:

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request add-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-allow"></a>

**`allow`**

```haproxy
allow
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto detiene la evaluación de las reglas y deja pasar la solicitud por la comprobación. Esta
acción es final, es decir, no se evalúan más reglas del mismo conjunto de reglas para la sección
actual. No hay diferencia entre esta y la acción "accept" salvo que, por compatibilidad
histórica, "accept" se usa para las reglas TCP y "allow" para las reglas HTTP. Ver también la
acción "accept" anterior.

<a id="entry-4-4-attach-srv"></a>

**`attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]`**

```haproxy
attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| X \| - \| -
\| - \| - \| -

Esto se usa para interceptar la conexión después del establecimiento correcto de HTTP/2. La
conexión se invierte al lado del backend y se inserta en el pool de conexiones inactivas del
servidor `<srv>`. Solo puede usarse con servidores que tienen una dirección 'rhttp@'.

La conexión se inserta en el pool de conexiones inactivas del servidor con un nombre definido
por el resultado de la evaluación de `<expr>`. Este es el nombre contra el que coincidirán las
solicitudes sujetas al parámetro "pool-conn-name" o "sni". Ver "http-reuse" para más detalles.

Reverse HTTP está actualmente aún en desarrollo activo. El mecanismo de configuración puede
cambiar en el futuro. Por esta razón está marcado internamente como experimental, lo que
significa que "expose-experimental-directives" debe aparecer en una línea antes de esta
directiva.

Ten en cuenta que un protocolo muy similar pero independiente está en desarrollo. Ver
<https://www.ietf.org/archive/id/draft-bt-httpbis-reverse-http-00.html>.

<a id="entry-4-4-auth"></a>

**`auth [realm <realm>]`**

```haproxy
auth [realm <realm>]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto detiene la evaluación de las reglas y responde inmediatamente con un código de error HTTP
401 o 407 para invitar al usuario a presentar un nombre de usuario y contraseña válidos. No se
evalúan más reglas "http-request". Se soporta un parámetro opcional "realm", que establece el
reino de autenticación que se devuelve con la respuesta (típicamente el nombre de la
aplicación).

Se usa el mensaje de error del proxy correspondiente. Puede personalizarse usando una directiva
"errorfile" o "http-error". Para las respuestas 401, todas las apariciones de la cabecera
WWW-Authenticate se eliminan y se sustituyen por una nueva con un desafío de autenticación básica
para el reino "`<realm>`". Para las respuestas 407, se hace lo mismo con la cabecera
Proxy-Authenticate. Si el mensaje de error no debe alterarse, considera usar en su lugar una
regla "http-request return".

Ejemplo:

```text
acl auth_ok http_auth_group(L1) G1
http-request auth unless auth_ok

```

<a id="entry-4-4-cache-store"></a>

**`cache-store <name>`**

```haproxy
cache-store <name>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| -

Almacena una http-response dentro de la caché. El almacenamiento de las cabeceras de la
respuesta se hace en este paso, lo que significa que puedes usar otras acciones http-response
para modificar cabeceras antes o después del almacenamiento de la respuesta. Esta acción es la
responsable de la configuración del filtro de almacenamiento en caché.

Ver la [sección 6.2](/es/haproxy/cache/#section-6-2) sobre la configuración de la caché.

<a id="entry-4-4-cache-use"></a>

**`cache-use <name>`**

```haproxy
cache-use <name>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Intenta entregar un objeto cacheado desde la caché `<name>`. Esta directiva también es
obligatoria para almacenar en caché, ya que calcula el hash de la caché. Si quieres usar una
condición tanto para el almacenamiento como para la entrega, es buena idea ponerla después de
esta.

Ver la [sección 6.2](/es/haproxy/cache/#section-6-2) sobre la configuración de la caché.

<a id="entry-4-4-capture"></a>

**`capture <sample> [ len <length> | id <id> ]`**

```haproxy
capture <sample> [ len <length> | id <id> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| X \| X

Esto captura la expresión de muestra `<sample>` del búfer de la solicitud o de la respuesta, y
la convierte en una cadena de como máximo `<len>` caracteres. La cadena resultante se almacena
en la siguiente ranura "capture" (de solicitud o de respuesta), así que posiblemente aparecerá
junto a algunas cabeceras HTTP capturadas. Luego aparecerá automáticamente en los registros, y
será posible extraerla usando métodos de recuperación de muestras para alimentar cabeceras o
cualquier cosa. La longitud debería limitarse dado que este tamaño se asignará para cada
captura durante toda la vida del flujo. Ten en cuenta que la longitud solo es utilizable con
reglas "http-request". Tal ranura solo existe en la sección que la declara, así que cuando esta
regla se coloca en una sección "listen" que también se usa como backend de otro frontend, se
ignora para los flujos que provienen de ese frontend. Comprueba la [sección 7.3](/es/haproxy/acls-and-samples/#section-7-3)
(Obtención de muestras), "capture request header" y "capture response header" para más
información.

Si se usa la palabra clave "id" en lugar de "len", la acción intenta almacenar la cadena
capturada en una ranura de captura declarada previamente. Esto es útil para ejecutar capturas
en backends. El id de la ranura puede declararse con una directiva previa "http-request
capture" o con la palabra clave "declare capture".

Al usar esta acción en un backend, comprueba detenidamente que los frontend relevantes tengan
las ranuras de captura necesarias; de lo contrario, esta regla se ignorará en tiempo de
ejecución. Esto no puede detectarse en el momento del análisis de la configuración debido a la
capacidad de HAProxy de resolver dinámicamente el nombre del backend en tiempo de ejecución.

<a id="entry-4-4-close"></a>

**`close`**

```haproxy
close
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| X
\| - \| - \| -

Esto se usa para cerrar inmediatamente la conexión con el servidor. No se evalúan más reglas
"tcp-response content". El propósito principal de esta acción es forzar que una conexión
termine entre un cliente y un servidor después de un intercambio cuando el protocolo de la
aplicación espera que transcurran primero tiempos de espera largos. El objetivo es eliminar
conexiones inactivas que consumen recursos significativos en los servidores con ciertos
protocolos.

<a id="entry-4-4-del-acl"></a>

**`del-acl(<file-name>) <key fmt>`**

```haproxy
del-acl(<file-name>) <key fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto se usa para eliminar una entrada de una ACL. La ACL debe cargarse desde un archivo (incluso
un archivo vacío de relleno). El nombre del archivo de la ACL que se va a actualizar se pasa
entre paréntesis. Toma un argumento: `<key fmt>`, que sigue las reglas del formato de registro personalizado de
la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6), para recopilar el contenido de la entrada a
eliminar. Es el equivalente del comando "del acl" del socket de estadísticas, pero puede
dispararse por una solicitud o respuesta HTTP.

<a id="entry-4-4-del-header"></a>

**`del-header <name> [ -m <meth> ]`**

```haproxy
del-header <name> [ -m <meth> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto elimina todos los campos de cabecera HTTP cuyo nombre se especifica en `<name>`. `<meth>`
es el método de coincidencia, aplicado sobre el nombre de la cabecera. Los métodos de
coincidencia soportados son "str" (coincidencia exacta), "beg" (coincidencia por prefijo), "end"
(coincidencia por sufijo), "sub" (coincidencia por subcadena) y "reg" (coincidencia por
expresión regular). Si no se especifica, se usa el método de coincidencia exacta.

<a id="entry-4-4-del-headers-bin"></a>

**`del-headers-bin <expr> [ -m <meth> ]`**

```haproxy
del-headers-bin <expr> [ -m <meth> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto elimina todos los campos de cabecera HTTP cuyos nombres se especifican en `<expr>`.
`<expr>` debe devolver una cadena binaria codificada en varint con todos los nombres de
cabecera que deben eliminarse. Ver "add-headers-bin" y "set-headers-bin" para la descripción de
la codificación y ejemplos. `<meth>` es el método de coincidencia, aplicado sobre todos los
nombres de cabecera. Los métodos de coincidencia soportados son "str" (coincidencia exacta),
"beg" (coincidencia por prefijo), "end" (coincidencia por sufijo) y "sub" (coincidencia por
subcadena). El método "reg" (coincidencia por expresión regular) no está soportado debido a un
rendimiento impredecible durante la ejecución. Si no se especifica, se usa el método de
coincidencia exacta.

<a id="entry-4-4-del-map"></a>

**`del-map(<map-name>) <key fmt>`**

```haproxy
del-map(<map-name>) <key fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto se usa para eliminar una entrada de un MAP. `<map-name>` debe seguir el formato descrito
en 2.7 sobre el formato de nombres para maps y ACLs. El nombre del MAP que se va a actualizar se
pasa entre paréntesis. Toma un argumento: `<key fmt>`, que sigue las reglas del formato de registro personalizado de la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6), para recopilar el contenido de la entrada a
eliminar. Toma un argumento: «nombre de archivo». Es el equivalente del comando "del map" del socket de
estadísticas, pero puede dispararse por una solicitud o respuesta HTTP.

<a id="entry-4-4-deny"></a>

**`deny [ { status | deny_status } <code> ] [ content-type <type> ]`**

```haproxy
deny [ { status | deny_status } <code> ] [ content-type <type> ]
     [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

       file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
     [ hdr `<name>` `<fmt>` ]*

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto detiene la evaluación de las reglas y rechaza inmediatamente la solicitud o la respuesta.
Por defecto se devuelve un error HTTP 403 para las solicitudes y 502 para las respuestas, pero
la respuesta devuelta puede personalizarse usando la misma sintaxis que para la acción
"return". Así, ver "return" a continuación para más detalles. Por motivos de compatibilidad,
cuando no se define ningún argumento, o solo "deny_status", el argumento "default-errorfiles"
está implícito. Significa que "deny [deny_status `<status>`]" es un alias de "deny [status
`<status>`] default-errorfiles". Esta acción es final, es decir, no se evalúan más reglas del
mismo conjunto de reglas para la sección actual. Ver también la acción "return" para la sintaxis
avanzada.

<a id="entry-4-4-dgram-drop"></a>

**`dgram-drop`**

```haproxy
dgram-drop
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

Esto ignora silenciosamente la recepción de un paquete inicial QUIC que de otro modo habría
dado lugar a la creación de una nueva conexión QUIC y a la ejecución de su handshake SSL.

<a id="entry-4-4-disable-l7-retry"></a>

**`disable-l7-retry`**

```haproxy
disable-l7-retry
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto deshabilita cualquier intento de reintentar la solicitud si falla por cualquier motivo
distinto de un fallo de conexión. Esto puede ser útil, por ejemplo, para asegurar que las
solicitudes POST no se reintenten ante un fallo.

<a id="entry-4-4-do-log"></a>

**`do-log [profile <log_profile>]`**

```haproxy
do-log [profile <log_profile>]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| X \| X

Esta acción dispara manualmente una emisión de registro en el proxy. Esto significa que las
opciones de registro del proxy se considerarán (incluidas las opciones de formateo tales como
"log-format"), pero no interferirá con los registros generados automáticamente por el proxy
durante el manejo de la transacción.

Usando "log-profile", es posible describir con precisión cómo debería emitirse el registro para
cada uno de los contextos disponibles donde la acción puede usarse. Es decir, la palabra clave
'on' seguida de uno de los siguientes valores: 'quic-init', 'tcp-req-conn', 'tcp-req-sess',
'tcp-req-cont', 'tcp-res-cont', 'http-req', 'http-res', 'http-after-res'.

Además, se informarán correctamente al usar el alias de logformat "%OG".

El argumento opcional "profile" puede usarse para especificar el nombre de una sección
log-profile que debería usarse para esta acción do-log en concreto en lugar de la asociada al
logger actual que se aplica por defecto.

Ejemplo:

```text
log-profile my-dft-prof
  on tcp-req-conn format "Connect: %ci"

log-profile my-local-prof
  on tcp-req-conn format "Local Connect: %ci"

frontend myfront
  log stdout format rfc5424 profile my-dft-prof local0
  log-format "log generated using proxy logformat, from '%OG'"
  acl local src 127.0.0.1
  # on connection use either log-profile from the logger (my-dft-prof) or
  # explicit my-local-prof if source ip is localhost
  tcp-request connection do-log if !local
  tcp-request connection do-log profile my-local-prof if local
  # on content use proxy logformat, since no override was specified
  # in my-dft-prof
  tcp-request content do-log
```

<a id="entry-4-4-do-resolve"></a>

**`do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>`**

```haproxy
do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esta acción realiza una resolución DNS de la salida de `<expr>` y almacena el resultado en la
variable `<var>`. Usa la sección de resolutores DNS apuntada por `<resolvers>`. Es posible
elegir una preferencia de resolución usando los argumentos opcionales 'ipv4' o 'ipv6'. Ver
también la palabra clave global "dns-accept-family" para forzar el uso estricto de una familia
específica.

Al realizar la resolución DNS, la conexión del lado del cliente queda en pausa esperando hasta
el final de la resolución. Si se puede encontrar una dirección IP, se almacena en `<var>`. Si
ocurre cualquier tipo de error, entonces `<var>` no se establece. Se puede usar esta acción
para descubrir una dirección IP del servidor en tiempo de ejecución y basándose en información
encontrada en la solicitud (p. ej. una cabecera Host). Si esta acción se usa para encontrar la
dirección IP del servidor (usando la acción "set-dst"), entonces la dirección IP del servidor
en el backend debe establecerse a 0.0.0.0. La acción do-resolve toma un parámetro de solo host,
cualquier puerto debe eliminarse de la cadena.

Ejemplo:

```text
resolvers mydns
  nameserver local 127.0.0.53:53
  nameserver google 8.8.8.8:53
  timeout retry   1s
  hold valid 10s
  hold nx 3s
  hold other 3s
  hold obsolete 0s
  accepted_payload_size 8192

frontend fe
  bind 10.42.0.1:80
  http-request do-resolve(txn.myip,mydns,ipv4) hdr(Host),host_only
  http-request capture var(txn.myip) len 40

  # return 503 when the variable is not set,
  # which mean DNS resolution error
  use_backend b_503 unless { var(txn.myip) -m found }

  default_backend be

backend b_503
  # dummy backend used to return 503.
  # one can use the errorfile directive to send a nice
  # 503 error page to end users

backend be
  # rule to prevent HAProxy from reconnecting to services
  # on the local network (forged DNS name used to scan the network)
  http-request deny if { var(txn.myip) -m ip 127.0.0.0/8 10.0.0.0/8 }
  http-request set-dst var(txn.myip)
  server clear 0.0.0.0:0
```

NOTA: No olvides establecer las reglas de "protección" para asegurar que HAProxy no se use
para escanear la red o, peor aún, no entre en bucle sobre sí mismo...

<a id="entry-4-4-early-hint"></a>

**`early-hint <name> <fmt>`**

```haproxy
early-hint <name> <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto se usa para construir una respuesta HTTP 103 Early Hints previa a cualquier otra. Esto
añade un campo de cabecera HTTP a esa respuesta cuyo nombre se especifica en `<name>` y cuyo
valor está definido por `<fmt>`, que sigue las reglas del formato de registro personalizado (ver formato de registro personalizado en la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)). Esto es
particularmente útil para pasar al cliente algunas cabeceras Link para precargar recursos
necesarios para renderizar los documentos HTML.

Ver el RFC 8297 para más información.

<a id="entry-4-4-expect-netscaler-cip-layer4"></a>

**`expect-netscaler-cip layer4`**

```haproxy
expect-netscaler-cip layer4
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

Esto configura la conexión del lado del cliente para recibir una cabecera del protocolo de
inserción de IP de cliente de NetScaler antes de leer cualquier byte del socket. Esto es
equivalente a tener la palabra clave "accept-netscaler-cip" en la línea "bind", excepto que
usar la regla TCP permite que el protocolo PROXY se acepte solo para ciertos rangos de
direcciones IP usando una ACL. Esto es conveniente cuando múltiples capas de balanceadores de
carga son atravesadas por el tráfico proveniente de hosts públicos.

<a id="entry-4-4-expect-proxy-layer4"></a>

**`expect-proxy layer4`**

```haproxy
expect-proxy layer4
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

Esto configura la conexión del lado del cliente para recibir una cabecera del protocolo PROXY
antes de leer cualquier byte del socket. Esto es equivalente a tener la palabra clave
"accept-proxy" en la línea "bind", excepto que usar la regla TCP permite que el protocolo PROXY
se acepte solo para ciertos rangos de direcciones IP usando una ACL. Esto es conveniente cuando
múltiples capas de balanceadores de carga son atravesadas por el tráfico proveniente de hosts
públicos.

<a id="entry-4-4-normalize-uri"></a>

**`normalize-uri <normalizer>`**

```haproxy
normalize-uri <normalizer>
normalize-uri fragment-encode
normalize-uri fragment-strip
normalize-uri path-merge-slashes
normalize-uri path-strip-dot
normalize-uri path-strip-dotdot [ full ]
normalize-uri percent-decode-unreserved [ strict ]
normalize-uri percent-to-uppercase [ strict ]
normalize-uri query-sort-by-name
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Realiza la normalización del URI de la solicitud.

La normalización de URI en HAProxy 2.4 está actualmente disponible como una vista previa técnica
experimental. Como tal, requiere la directiva global 'expose-experimental-directives' antes de
poder invocarla. Debes estar preparado para que el comportamiento de los normalizadores pueda
cambiar para corregir posibles problemas, posiblemente rompiendo el procesamiento correcto de
las solicitudes en tu infraestructura.

Cada normalizador maneja un único tipo de normalización para permitir una selección fina del
nivel de normalización apropiado para el backend soportado.

Como ejemplo, el normalizador "path-strip-dotdot" podría ser útil para un servidor de archivos
estáticos que mapea directamente el URI solicitado a la ruta dentro del sistema de archivos
local. Sin embargo, podría romper el enrutamiento de una API que espera un número específico
de segmentos en la ruta.

Es importante tener en cuenta que algunos normalizadores podrían dar como resultado
transformaciones inseguras para URIs rotas. También podría ser posible que una combinación de
normalizadores que por sí mismos son seguros dé como resultado transformaciones inseguras
cuando se combinan inadecuadamente.

Como ejemplo, el normalizador "percent-decode-unreserved" podría dar resultados inesperados
cuando un URI roto incluye caracteres de porcentaje sueltos. Uno de tales URIs rotos es
"/%%36%36", que se decodificaría a "/%66", que a su vez es equivalente a "/f". Especificando la
opción "strict", las solicitudes a tal URI roto se rechazarían de forma segura.

Los siguientes normalizadores están disponibles:

- fragment-encode: Codifica "#" como "%23".

  Debería preferirse el normalizador "fragment-strip", salvo que se sepa que clientes rotos no
  codifican correctamente '#' dentro del componente de ruta.

  Ejemplo:

  - /#foo -\> /%23foo

- fragment-strip: Elimina el componente "fragment" del URI.

  Según el RFC 3986#3.5, el componente "fragment" de un URI no debería enviarse, sino
  manejarlo el User Agent después de recuperar un recurso.

  Este normalizador debería aplicarse primero para asegurar que el fragmento no se interpreta
  como parte del componente de ruta de la solicitud.

  Ejemplo:

  - /#foo -\> /

- path-strip-dot: Elimina segmentos "/./" dentro del componente "path" (RFC 3986#6.2.2.3).

  Los segmentos que incluyen puntos codificados en porcentaje ("%2E") no se detectarán. Usa
  primero el normalizador "percent-decode-unreserved" si esto no es deseable.

  Ejemplo:

  - /. -\> /
  - /./bar/ -\> /bar/
  - /a/./a -\> /a/a
  - /.well-known/ -\> /.well-known/ (sin cambios)

- path-strip-dotdot: Normaliza segmentos "/../" dentro del componente "path" (RFC
  3986#6.2.2.3).

  Esto fusiona los segmentos que intentan acceder al directorio padre con su segmento
  precedente.

  Los segmentos vacíos no reciben un tratamiento especial. Usa primero el normalizador
  "merge-slashes" si esto no es deseable.

  Los segmentos que incluyen puntos codificados en porcentaje ("%2E") no se detectarán. Usa
  primero el normalizador "percent-decode-unreserved" si esto no es deseable.

  Ejemplo:

  - /foo/../ -\> /
  - /foo/../bar/ -\> /bar/
  - /foo/bar/../ -\> /foo/
  - /../bar/ -\> /../bar/
  - /bar/../../ -\> /../
  - /foo//../ -\> /foo/
  - /foo/%2E%2E/ -\> /foo/%2E%2E/

  Si se especifica la opción "full", entonces "../" al principio también se eliminará:

  Ejemplo:

  - /../bar/ -\> /bar/
  - /bar/../../ -\> /

- path-merge-slashes: Fusiona barras adyacentes dentro del componente "path" en una sola
  barra.

  Ejemplo:

  - // -\> /
  - /foo//bar -\> /foo/bar

- percent-decode-unreserved: Decodifica caracteres no reservados codificados en porcentaje a
  su representación como carácter regular (RFC 3986#6.2.2.2).

  El conjunto de caracteres no reservados incluye todas las letras, todos los dígitos, "-",
  ".", "\_", y "~".

  Ejemplo:

  - /%61dmin -\> /admin
  - /foo%3Fbar=baz -\> /foo%3Fbar=baz (sin cambios)
  - /%%36%36 -\> /%66 (inseguro)
  - /%ZZ -\> /%ZZ

  Si se especifica la opción "strict", las secuencias no válidas darán como resultado que se
  devuelva un HTTP 400 Bad Request.

  Ejemplo:

  - /%%36%36 -\> HTTP 400
  - /%ZZ -\> HTTP 400

- percent-to-uppercase: Pasa a mayúsculas las letras dentro de secuencias codificadas en
  porcentaje (RFC 3986#6.2.2.1).

  Ejemplo:

  - /%6f -\> /%6F
  - /%zz -\> /%zz

  Si se especifica la opción "strict", las secuencias no válidas darán como resultado que se
  devuelva un HTTP 400 Bad Request.

  Ejemplo:

  - /%zz -\> HTTP 400

- query-sort-by-name: Ordena los parámetros de la cadena de consulta por nombre de parámetro.
  Se asume que los parámetros están delimitados por '&'. Los nombres más cortos se ordenan
  antes que los más largos y los nombres de parámetro idénticos mantienen su orden relativo.

  Ejemplo:

  - /?c=3&a=1&b=2 -\> /?a=1&b=2&c=3
  - /?aaa=3&a=1&aa=2 -\> /?a=1&aa=2&aaa=3
  - /?a=3&b=4&a=1&b=5&a=2 -\> /?a=3&a=1&a=2&b=4&b=5

<a id="entry-4-4-pause"></a>

**`pause { <timeout> | <expr> }`**

```haproxy
pause { <timeout> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto suspende el análisis del mensaje durante el número de milisegundos especificado. El tiempo
de espera puede especificarse en milisegundos o con cualquier otra unidad si el número lleva la
unidad como sufijo, tal como se explica al principio de este documento. También es posible
escribir una expresión que debe devolver un número interpretado como un tiempo de espera en
milisegundos. Si la evaluación de la expresión falla o si devuelve un valor no válido, la
acción se ignora y la evaluación continúa.

Esta acción puede usarse con fines de depuración. Pero también podría usarse para ralentizar a
algunos clientes basándose en criterios específicos. Por ejemplo, es posible ralentizar a los
clientes si su tasa de solicitudes es demasiado alta, rastreándolos mediante una regla
"track-sc".

<a id="entry-4-4-redirect"></a>

**`redirect <rule>`**

```haproxy
redirect <rule>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto realiza una redirección HTTP basada en una regla de redirección. Es exactamente lo mismo
que la instrucción "redirect", excepto que inserta una regla de redirección que se procesa en
medio de otras reglas "http-request" o "http-response" y que estas reglas usan el formato de registro personalizado. Para las respuestas, solo se permite el tipo "location" de redirección. Además, cuando
se realiza una redirección durante una respuesta, la transferencia del servidor a HAProxy se
interrumpe para que ninguna carga útil pueda reenviarse al cliente. Esto puede provocar que
algunas conexiones se cierren en HTTP/1. Esta acción es final, es decir, no se evalúan más
reglas del mismo conjunto de reglas para la sección actual. Ver la palabra clave "redirect"
para la sintaxis de la regla.

<a id="entry-4-4-reject"></a>

**`reject`**

```haproxy
reject
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| - \| -

Esto detiene la evaluación de las reglas y cierra inmediatamente la conexión sin enviar ninguna
respuesta. Para las reglas HTTP, actúa de forma similar a las reglas "tcp-request content
reject". Puede ser útil forzar un cierre inmediato de la conexión en conexiones HTTP/2.

En las reglas "tcp-request connection", las conexiones rechazadas ni siquiera llegan a
convertirse en sesión, razón por la cual se contabilizan por separado en las estadísticas, como
"conexiones denegadas". No se consideran para el límite de tasa de sesiones y tampoco se
registran. La razón es que estas reglas deberían usarse únicamente para filtrar tasas de
conexión extremadamente altas como las que se encuentran durante un ataque DDoS masivo. Bajo
estas condiciones extremas, la simple acción de registrar cada evento haría colapsar el sistema
y reduciría considerablemente la capacidad de filtrado. Si el registro es absolutamente
deseado, deberían usarse en su lugar reglas "tcp-request content", ya que las reglas
"tcp-request session" tampoco registrarán.

Cuando se usa en reglas "tcp-response content", la conexión del servidor se cerrará y la
respuesta se abortará. Esto generalmente se usa para evitar que se filtre información sensible,
típicamente después de inspeccionar contenidos junto con la acción "wait-for-body".

Esta acción también puede usarse en reglas "quic-initial". La conexión QUIC recién abierta se
cierra inmediatamente sin ningún procesamiento de handshake SSL y el cliente es notificado
mediante un código de error CONNECTION_REFUSED.

<a id="entry-4-4-replace-header"></a>

**`replace-header <name> <match-regex> <replace-fmt>`**

```haproxy
replace-header <name> <match-regex> <replace-fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto compara el valor de todas las apariciones del campo de cabecera `<name>` contra
`<match-regex>`. La coincidencia se realiza distinguiendo mayúsculas y minúsculas. Los valores
que coinciden se reemplazan completamente por `<replace-fmt>`. Los caracteres de formato están
permitidos en `<replace-fmt>` y funcionan como los argumentos `<fmt>` en "http-request
add-header". Se soportan las retro-referencias estándar usando la barra invertida ('&#92;')
seguida de un número.

Esta acción actúa sobre líneas de cabecera completas, sin importar el número de valores que
puedan contener. Así, está bien adaptada para procesar cabeceras que contienen naturalmente
comas en su valor, tales como If-Modified-Since o Set-Cookie. Las cabeceras que contienen una
lista de valores separados por comas, tales como Accept o Cache-Control, deberían procesarse
usando en su lugar la acción "replace-value". Ver también la acción "replace-value".

Ejemplo:

```shell
http-request replace-header Cookie foo=([^;]*);(.*) foo=\1;ip=%bi;\2

# applied to:
Cookie: foo=foobar; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# outputs:
Cookie: foo=foobar;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# assuming the backend IP is 192.168.1.20

http-request replace-header User-Agent curl foo

# applied to:
User-Agent: curl/7.47.0

# outputs:
User-Agent: foo
```

Ejemplo:

```shell
http-response replace-header Set-Cookie (C=[^;]*);(.*) \1;ip=%bi;\2

# applied to:
Set-Cookie: C=1; expires=Tue, 14-Jun-2016 01:40:45 GMT

# outputs:
Set-Cookie: C=1;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT

# assuming the backend IP is 192.168.1.20.

```

<a id="entry-4-4-replace-path"></a>

**`replace-path <match-regex> <replace-fmt>`**

```haproxy
replace-path <match-regex> <replace-fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto funciona como "replace-header", excepto que funciona sobre el componente de ruta de la
solicitud en lugar de una cabecera. El componente de ruta empieza en la primera '/' después de
un esquema+autoridad opcional y termina antes del signo de interrogación. Así, el reemplazo no
modifica el esquema, la autoridad ni la cadena de consulta.

Merece la pena señalar que las expresiones regulares pueden ser más costosas de evaluar que
ciertas ACLs, así que los reemplazos poco frecuentes pueden beneficiarse de una condición para
evitar realizar la evaluación si no coincide.

Ejemplo:

```shell
# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-path (.*) /foo\1

# strip /foo: turn /foo/bar?q=1 into /bar?q=1
http-request replace-path /foo/(.*) /\1
# or more efficient if only some requests match:
http-request replace-path /foo/(.*) /\1 if { url_beg /foo/ }

```

<a id="entry-4-4-replace-pathq"></a>

**`replace-pathq <match-regex> <replace-fmt>`**

```haproxy
replace-pathq <match-regex> <replace-fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto hace lo mismo que "http-request replace-path", excepto que la ruta contiene la cadena de
consulta si hay alguna presente. Así, se reemplazan la ruta y la cadena de consulta.

Ejemplo:

```shell
# suffix /foo: turn /bar?q=1 into /bar/foo?q=1:
http-request replace-pathq ([^?]*)(\?(.*))? \1/foo\2

```

<a id="entry-4-4-replace-uri"></a>

**`replace-uri <match-regex> <replace-fmt>`**

```haproxy
replace-uri <match-regex> <replace-fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto funciona como "replace-header", excepto que funciona sobre la parte del URI de la
solicitud en lugar de una cabecera. La parte del URI puede contener un esquema, autoridad o
cadena de consulta opcionales. Estos se consideran parte del valor contra el que se compara.

Merece la pena señalar que las expresiones regulares pueden ser más costosas de evaluar que
ciertas ACLs, así que los reemplazos poco frecuentes pueden beneficiarse de una condición para
evitar realizar la evaluación si no coincide.

NOTA IMPORTANTE: históricamente en HTTP/1.x, la gran mayoría de las solicitudes enviadas por
los navegadores usan la "forma de origen" ("origin form"), que difiere de la "forma absoluta"
en que no contienen ni esquema ni autoridad en la porción del URI. Mayormente solo las
solicitudes enviadas a proxies, las forjadas a mano y algunas emitidas por ciertas aplicaciones
usan la forma absoluta. Como tal, "replace-uri" normalmente funciona bien la mayoría del tiempo
en HTTP/1.x con reglas que empiezan por "/". Pero con HTTP/2, se anima a los clientes a enviar
únicamente URI absolutas, que se parecen a las que los clientes HTTP/1 usan para hablar con
proxies. Tales reglas replace-uri parciales pueden entonces fallar en HTTP/2 cuando funcionan
en HTTP/1. O bien las reglas deben adaptarse para coincidir opcionalmente con un esquema y una
autoridad, o debería usarse replace-path.

Ejemplo:

```shell
# rewrite all "http" absolute requests to "https":
http-request replace-uri ^http://(.*) https://\1

# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-uri ([^/:]*://[^/]*)?(.*) \1/foo\2

```

<a id="entry-4-4-replace-value"></a>

**`replace-value <name> <match-regex> <replace-fmt>`**

```haproxy
replace-value <name> <match-regex> <replace-fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto funciona como "replace-header", excepto que compara la regex contra cada valor delimitado
por comas del campo de cabecera `<name>` en lugar de contra la cabecera entera. Esto es apto
para todas las cabeceras que pueden llevar más de un valor. Un ejemplo podría ser la cabecera
de solicitud Accept, o Cache-Control para solicitudes o respuestas.

Ejemplo:

```shell
http-request replace-value X-Forwarded-For ^192\.168\.(.*)$ 172.16.\1

# applied to:
X-Forwarded-For: 192.168.10.1, 192.168.13.24, 10.0.0.37

# outputs:
X-Forwarded-For: 172.16.10.1, 172.16.13.24, 10.0.0.37
```

Ejemplo:

```shell
http-after-response replace-value Cache-control ^public$ private

# applied to:
Cache-Control: max-age=3600, public

# outputs:
Cache-Control: max-age=3600, private

```

<a id="entry-4-4-return"></a>

**`return [ status <code> ] [ content-type <type> ]`**

```haproxy
return [ status <code> ] [ content-type <type> ]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

         file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto detiene la evaluación de las reglas y devuelve inmediatamente una respuesta. El código de
estado por defecto usado para la respuesta es 200. Puede especificarse opcionalmente como
argumento de "status". El content-type de la respuesta también puede especificarse como
argumento de "content-type". Finalmente, puede definirse la respuesta en sí. Puede ser una
respuesta HTTP completa especificando el errorfile a usar, o la carga útil de la respuesta
especificando el archivo o la cadena a usar. Se siguen estas reglas para crear la respuesta:

- Si no se define ni el errorfile ni la carga útil a usar, se devuelve una respuesta de
  relleno. Solo se considera el argumento "status". Puede ser cualquier código en el rango
  [200, 599]. El argumento "content-type", si existe, se ignora.

- Si el argumento "default-errorfiles" está establecido, se consideran los errorfiles del
  proxy. Si el argumento "status" está definido, debe ser uno de los códigos de estado
  manejados por HAProxy (200, 400, 403, 404, 405, 408, 410, 413, 414, 425, 429, 431, 500, 501,
  502, 503 y 504). El argumento "content-type", si existe, se ignora.

- Si se define un errorfile específico, con un argumento "errorfile", se devuelve el archivo
  correspondiente, que contiene una respuesta HTTP completa. Solo se considera el argumento
  "status". Debe ser uno de los códigos de estado manejados por HAProxy (200, 400, 403, 404,
  405, 408, 410, 413, 414, 425, 429, 431, 500, 501, 502, 503 y 504). El argumento
  "content-type", si existe, se ignora.

- Si se define una sección http-errors, con un argumento "errorfiles", se devuelve el archivo
  correspondiente de la sección http-errors especificada, que contiene una respuesta HTTP
  completa. Solo se considera el argumento "status". Debe ser uno de los códigos de estado
  manejados por HAProxy (200, 400, 403, 404, 405, 408, 410, 413, 414, 425, 429, 431, 500, 501,
  502, 503 y 504). El argumento "content-type", si existe, se ignora.

- Si se especifica un argumento "file" o "lf-file", el contenido del archivo se usa como carga
  útil de la respuesta. Si el archivo no está vacío, su content-type debe establecerse como
  argumento de "content-type". De lo contrario, cualquier argumento "content-type" se ignora.
  Con un argumento "lf-file", el contenido del archivo se evalúa como un formato de registro personalizado
  (ver [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)). Con un argumento
  "file", se considera como contenido en crudo.

- Si se especifica un argumento "string" o "lf-string", la cadena definida se usa como carga
  útil de la respuesta. El content-type debe establecerse siempre como argumento de
  "content-type". Con un argumento "lf-string", la cadena se evalúa como un formato de registro personalizado
  (ver [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)). Con un argumento
  "string", se considera como una cadena en crudo.

Cuando la respuesta no se basa en un errorfile, es posible añadir campos de cabecera HTTP a la
respuesta usando argumentos "hdr". De lo contrario, todos los argumentos "hdr" se ignoran. Para
cada uno, el nombre de la cabecera se especifica en `<name>` y su valor está definido por
`<fmt>`, que sigue las reglas del formato de registro personalizado descritas en la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6).

Ten en cuenta que la respuesta generada debe ser más pequeña que un búfer. Y para evitar
cualquier aviso, cuando se carga un errorfile o un archivo en crudo, el espacio de búfer
reservado para la reescritura de cabeceras debería estar también libre.

Esta acción es final, es decir, no se evalúan más reglas del mismo conjunto de reglas para la
sección actual.

Ejemplo:

```text
http-request return errorfile /etc/haproxy/errorfiles/200.http \
    if { path /ping }

http-request return content-type image/x-icon file /var/www/favicon.ico  \
    if { path /favicon.ico }

http-request return status 403 content-type text/plain    \
    lf-string "Access denied. IP %[src] is blacklisted."  \
    if { src -f /etc/haproxy/blacklist.lst }

```

<a id="entry-4-4-sc-add-gpc"></a>

**`sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esta acción incrementa el contador de propósito general (General Purpose Counter) en el índice
`<idx>` del array asociado al contador sticky designado por `<sc-id>` en el valor del entero
`<int>` o de la evaluación entera de la expresión `<expr>`. Los enteros y las expresiones
están limitados a valores sin signo de 32 bits. Si ocurre un error, esta acción falla
silenciosamente y la evaluación de las acciones continúa. `<idx>` es un entero entre 0 y 99 y
`<sc-id>` es un entero entre 0 y 2. También falla silenciosamente si no hay ningún GPC
almacenado en ese índice. La entrada en la tabla se refresca incluso si el valor es cero. El
'gpc_rate' se ajusta automáticamente para reflejar la tasa media de crecimiento del valor gpc.

Esta acción se aplica solo a los data_types de array 'gpc' y 'gpc_rate' (y no a los data_types
heredados 'gpc0', 'gpc1', 'gpc0_rate' ni 'gpc1_rate'). No hay ninguna función equivalente para
los tipos de datos heredados, pero si el valor es siempre 1, ver 'sc-inc-gpc()', 'sc-inc-gpc0()' y
'sc-inc-gpc1()'. Tampoco hay forma de decrementar el valor, pero es posible almacenar valores
exactos en una etiqueta de propósito general (General Purpose Tag) usando 'sc-set-gpt()' en su
lugar.

El uso principal de esta acción es contar puntuaciones o volúmenes totales (p. ej. el peligro
estimado por IP de origen reportado por el servidor o un WAF, el total de bytes subidos,
etc.).

<a id="entry-4-4-sc-inc-gpc"></a>

**`sc-inc-gpc(<idx>,<sc-id>)`**

```haproxy
sc-inc-gpc(<idx>,<sc-id>)
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esta acción incrementa el contador de propósito general (General Purpose Counter) en el índice
`<idx>` del array asociado al contador sticky designado por `<sc-id>`. Si ocurre un error,
esta acción falla silenciosamente y la evaluación de las acciones continúa. `<idx>` es un
entero entre 0 y 99 y `<sc-id>` es un entero entre 0 y 2. También falla silenciosamente si no
hay ningún GPC almacenado en ese índice. Esta acción se aplica solo a los data_types de array
'gpc' y 'gpc_rate' (y no a los data_types heredados 'gpc0', 'gpc1', 'gpc0_rate' ni
'gpc1_rate').

<a id="entry-4-4-sc-inc-gpc0"></a>

**`sc-inc-gpc0(<sc-id>)`**

```haproxy
sc-inc-gpc0(<sc-id>)
sc-inc-gpc1(<sc-id>)
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esta acción incrementa el contador GPC0 o GPC1 de acuerdo con el contador sticky designado por
`<sc-id>`. Si ocurre un error, esta acción falla silenciosamente y la evaluación de las
acciones continúa.

<a id="entry-4-4-sc-set-gpt"></a>

**`sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esta acción establece el GPT sin signo de 32 bits en el índice `<idx>` del array asociado al
contador sticky designado por `<sc-id>` al valor de `<int>`/`<expr>`. El resultado esperado es
un booleano.

Si ocurre un error, esta acción falla silenciosamente y la evaluación de las acciones
continúa. `<idx>` es un entero entre 0 y 99 y `<sc-id>` es un entero entre 0 y 2. También
falla silenciosamente si no hay ningún GPT almacenado en ese índice.

Esta acción se aplica solo al data_type de array 'gpt' (y no al data-type heredado 'gpt0').

<a id="entry-4-4-sc-set-gpt0"></a>

**`sc-set-gpt0(<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt0(<sc-id>) { <int> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esta acción establece la etiqueta GPT0 sin signo de 32 bits de acuerdo con el contador sticky
designado por `<sc-id>` y el valor de `<int>`/`<expr>`. El resultado esperado es un booleano.
Si ocurre un error, esta acción falla silenciosamente y la evaluación de las acciones
continúa. Esta acción es un alias de "sc-set-gpt(0,`<sc-id>`)". Ver también la acción
"sc-set-gpt".

<a id="entry-4-4-send-retry"></a>

**`send-retry`**

```haproxy
send-retry
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

Esta acción fuerza la emisión de un paquete Retry en respuesta a un paquete Initial del cliente
sin token. Esto es útil para asegurar que la dirección del cliente se valida antes de
instanciar cualquier elemento de conexión y de iniciar el handshake.

<a id="entry-4-4-send-spoe-group"></a>

**`send-spoe-group <engine-name> <group-name>`**

```haproxy
send-spoe-group <engine-name> <group-name>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Esta acción se usa para disparar el envío de un grupo de mensajes SPOE. Para ello, debe
definirse el motor SPOE usado para enviar mensajes, así como el grupo SPOE a enviar. Por
supuesto, el motor SPOE debe referirse a un filtro SPOE existente. Si no se proporciona ningún
nombre de motor en la línea del filtro SPOE, debe usarse el nombre del agente SPOE.

Argumentos:

```text
<engine-name>  El nombre del motor SPOE.

<group-name>   El nombre del grupo SPOE tal como se especifica en la
               configuración del motor.

```

<a id="entry-4-4-set-bandwidth-limit"></a>

**`set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]`**

```haproxy
set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Esta acción se usa para activar el filtro de limitación de ancho de banda `<name>`, ya sea en
la dirección de subida o de bajada dependiendo del tipo de filtro. Pueden definirse límites y
períodos personalizados, si y solo si `<name>` referencia un filtro de limitación de ancho de
banda por flujo. Cuando se ejecuta una regla set-bandwidth-limit, primero restablece todos los
ajustes del filtro a sus valores por defecto antes de activarlo. En consecuencia, si se
ejecutan varias acciones "set-bandwidth-limit" para el mismo filtro, solo se considera la
última. Pueden activarse varios filtros de limitación de ancho de banda en el mismo flujo.

Ten en cuenta que esta acción no puede usarse en una sección defaults porque los filtros de
limitación de ancho de banda no pueden definirse en secciones defaults. Además, solo se limita
la transferencia de la carga útil HTTP. Las cabeceras HTTP no se consideran.

Argumentos:

```text
<expr>  Es una expresión estándar de HAProxy formada por un sample-fetch
        seguido de algunos convertidores. El resultado se convierte a un
        entero. Se interpreta como un tamaño en bytes para el parámetro
        "limit" y como una duración en milisegundos para el parámetro
        "period".

<size>  Es un número. Sigue el formato de tamaño de HAProxy y está
        expresado en bytes.

<time>  Es un número. Sigue el formato de tiempo de HAProxy y está
        expresado en milisegundos.
```

Ejemplo:

```text
http-request set-bandwidth-limit global-limit
http-request set-bandwidth-limit my-limit limit 1m period 10s
```

Ver la [sección 9.7](/es/haproxy/filters/#section-9-7) sobre la configuración del filtro de limitación de ancho de banda.

<a id="entry-4-4-set-bc-mark"></a>

**`set-bc-mark { <mark> | <expr> }`**

```haproxy
set-bc-mark { <mark> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esto se usa para establecer el MARK de Netfilter/IPFW en la conexión del backend (todos los
paquetes enviados al servidor) al valor pasado en `<mark>` o `<expr>` en plataformas que lo
soportan. Este valor es un valor sin signo de 32 bits que puede coincidir por netfilter/ipfw y
por la tabla de enrutamiento o monitorizando los paquetes mediante DTrace. `<mark>` puede
expresarse tanto en formato decimal como hexadecimal (con el prefijo "0x"). Alternativamente,
puede usarse `<expr>`: es una expresión estándar de HAProxy formada por un sample-fetch seguido
de algunos convertidores que debe resolverse a tipo entero. Esta acción puede ser útil para
forzar que ciertos paquetes tomen una ruta diferente (por ejemplo, una ruta de red más barata
para descargas masivas). Esto funciona en kernels Linux 2.6.32 y superiores y requiere
privilegios de administrador, así como en FreeBSD y OpenBSD. La marca se establecerá durante
toda la duración de la conexión backend/servidor (de la conexión al cierre).

<a id="entry-4-4-set-bc-tos"></a>

**`set-bc-tos { <tos> | <expr> }`**

```haproxy
set-bc-tos { <tos> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esto se usa para establecer el valor del campo TOS o DSCP en la conexión del backend (todos los
paquetes enviados al servidor) al valor pasado en `<tos>` o `<expr>` en plataformas que
soportan esto. Este valor representa los 8 bits completos del campo TOS de IP. Ten en cuenta
que solo los 6 bits superiores se usan en DSCP o TOS, y los dos bits inferiores son siempre 0.
Alternativamente, puede usarse `<expr>`: es una expresión estándar de HAProxy formada por un
sample-fetch seguido de algunos convertidores que debe resolverse a tipo entero. Esta acción
puede usarse para ajustar cierto comportamiento de enrutamiento en routers internos basándose
en alguna información de la solicitud. El tos se establecerá durante toda la duración de la
conexión backend/servidor (de la conexión al cierre).

Ver los RFC 2474, 2597, 3260 y 4594 para más información.

<a id="entry-4-4-set-dst"></a>

**`set-dst <expr>`**

```haproxy
set-dst <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Esto se usa para establecer la dirección IP de destino al valor de la expresión especificada.
Útil cuando un proxy delante de HAProxy reescribe la IP de destino, pero proporciona la IP
correcta en una cabecera HTTP; o quieres enmascarar la IP por privacidad. Si quieres conectarte
a la nueva dirección/puerto, usa '0.0.0.0:0' como dirección del servidor en el backend.

Argumentos:

```text
<expr>  Es una expresión estándar de HAProxy formada por un sample-fetch
        seguido de algunos convertidores.
```

Ejemplo:

```text
http-request set-dst hdr(x-dst)
http-request set-dst dst,ipmask(24)
```

Cuando es posible, set-dst conserva el puerto de destino original siempre que la familia de
direcciones lo permita; de lo contrario, el puerto de destino se establece a 0.

<a id="entry-4-4-set-dst-port"></a>

**`set-dst-port <expr>`**

```haproxy
set-dst-port <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Esto se usa para establecer el puerto de destino al valor de la expresión especificada. Si
quieres conectarte a la nueva dirección/puerto, usa '0.0.0.0:0' como dirección del servidor en
el backend.

Argumentos:

```text
<expr>  Es una expresión estándar de HAProxy formada por un sample-fetch
        seguido de algunos convertidores.
```

Ejemplo:

```text
http-request set-dst-port hdr(x-port)
http-request set-dst-port int(4000)
```

Cuando es posible, set-dst-port conserva la dirección de destino original siempre que la
familia de direcciones soporte un puerto; de lo contrario, fuerza la dirección de destino a
IPv4 "0.0.0.0" antes de reescribir el puerto.

<a id="entry-4-4-set-fc-mark"></a>

**`set-fc-mark { <mark> | <expr> }`**

```haproxy
set-fc-mark { <mark> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Esto se usa para establecer el MARK de Netfilter/IPFW en todos los paquetes enviados al cliente
al valor pasado en `<mark>` o `<expr>` en plataformas que lo soportan. Este valor es un valor
sin signo de 32 bits que puede coincidir por netfilter/ipfw y por la tabla de enrutamiento o
monitorizando los paquetes mediante DTrace. `<mark>` puede expresarse tanto en formato decimal
como hexadecimal (con el prefijo "0x"). Alternativamente, puede usarse `<expr>`: es una
expresión estándar de HAProxy formada por un sample-fetch seguido de algunos convertidores que
debe resolverse a tipo entero. Esta acción puede ser útil para forzar que ciertos paquetes
tomen una ruta diferente (por ejemplo, una ruta de red más barata para descargas masivas). Esto
funciona en kernels Linux 2.6.32 y superiores y requiere privilegios de administrador, así como
en FreeBSD y OpenBSD.

<a id="entry-4-4-set-fc-tos"></a>

**`set-fc-tos { <tos | <expr> }`**

```haproxy
set-fc-tos { <tos | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Esto se usa para establecer el valor del campo TOS o DSCP de los paquetes enviados al cliente al
valor pasado en `<tos>` o `<expr>` en plataformas que soportan esto. Este valor representa los
8 bits completos del campo TOS de IP. Ten en cuenta que solo los 6 bits superiores se usan en
DSCP o TOS, y los dos bits inferiores son siempre 0. Alternativamente, puede usarse `<expr>`:
es una expresión estándar de HAProxy formada por un sample-fetch seguido de algunos
convertidores que debe resolverse a tipo entero. Esta acción puede usarse para ajustar cierto
comportamiento de enrutamiento en routers de borde basándose en alguna información de la
solicitud.

Ver los RFC 2474, 2597, 3260 y 4594 para más información.

<a id="entry-4-4-set-header"></a>

**`set-header <name> <fmt>`**

```haproxy
set-header <name> <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto hace lo mismo que la acción "add-header", excepto que la cabecera se elimina primero si
existía. Esto es útil al pasar información de seguridad al servidor, donde la cabecera no debe
ser manipulada por usuarios externos, o para forzar ciertas cabeceras de respuesta tales como
"Server" para ocultar información externa. Ten en cuenta que el nuevo valor se calcula antes de
la eliminación, así que es posible concatenar un valor a una cabecera existente.

Ejemplo:

```text
http-request set-header X-Haproxy-Current-Date %T
http-request set-header X-SSL                  %[ssl_fc]
http-request set-header X-SSL-Session_ID       %[ssl_fc_session_id,hex]
http-request set-header X-SSL-Client-Verify    %[ssl_c_verify]
http-request set-header X-SSL-Client-DN        %{+Q}[ssl_c_s_dn]
http-request set-header X-SSL-Client-CN        %{+Q}[ssl_c_s_dn(cn)]
http-request set-header X-SSL-Issuer           %{+Q}[ssl_c_i_dn]
http-request set-header X-SSL-Client-NotBefore %{+Q}[ssl_c_notbefore]
http-request set-header X-SSL-Client-NotAfter  %{+Q}[ssl_c_notafter]
```

<a id="entry-4-4-set-headers-bin"></a>

**`set-headers-bin <expr> [ prefix <str> ]`**

```haproxy
set-headers-bin <expr> [ prefix <str> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Es una variante de la acción "set-header" donde los nombres y valores de las cabeceras se pasan
como una cadena binaria codificada en varint. Ver el fetch de muestras "req.hdrs_bin" sobre el
formato varint. Esto es útil cuando quieres establecer varias cabeceras a la vez, sin tener que
conocer de antemano los nombres de las cabeceras. Ten en cuenta que estas cabeceras no han sido
validadas por el analizador HTTP y podrían llevar a emitir mensajes no válidos y, en el peor de
los casos, a ataques de request smuggling. El número de cabeceras insertadas también es
importante, ya que está limitado por tune.http.maxhdr. El prefijo opcional solo establecerá las
cabeceras de la cadena codificada que empiecen por `<str>`.

Ejemplo:

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request set-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-set-log-level"></a>

**`set-log-level <level>`**

```haproxy
set-log-level <level>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| X

Esto se usa para cambiar el nivel de registro de la solicitud actual cuando se cumple cierta
condición. Los niveles válidos son los 8 niveles de syslog (ver la palabra clave "log") más el
nivel especial "silent", que deshabilita el registro para esta solicitud. Esta regla no es
final, así que gana la última regla que coincida. Esta regla puede ser útil para deshabilitar
las comprobaciones de estado que provienen de otro equipo.

<a id="entry-4-4-set-map"></a>

**`set-map(<map-name>) <key fmt> <value fmt>`**

```haproxy
set-map(<map-name>) <key fmt> <value fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto se usa para añadir una nueva entrada en un map. `<map-name>` debe seguir el formato
descrito en 2.7 sobre el formato de nombres para maps y ACLs. El nombre del MAP que se va a
actualizar se pasa entre paréntesis. Toma 2 argumentos: `<key fmt>`, que sigue las reglas del
formato de registro personalizado descritas en la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6), usado para recopilar la clave del map, y
`<value fmt>`, que sigue las reglas del formato de registro personalizado, usado para recopilar el contenido de
la nueva entrada. Realiza una búsqueda en el map antes de la inserción, para evitar valores
duplicados (o más). Es el equivalente del comando "set map" del socket de estadísticas, pero
puede dispararse por una solicitud HTTP.

<a id="entry-4-4-set-mark"></a>

**`set-mark <mark> (deprecated)`**

```haproxy
set-mark <mark> (deprecated)
```

Esto es un alias de "set-fc-mark" (que debería usarse en su lugar).

<a id="entry-4-4-set-method"></a>

**`set-method <fmt>`**

```haproxy
set-method <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto reescribe el método de la solicitud con el resultado de la evaluación de la cadena de
formato `<fmt>`. Debería haber muy pocas razones válidas para tener que hacer esto, ya que es
más probable que rompa algo que que lo arregle.

<a id="entry-4-4-set-nice"></a>

**`set-nice <nice>`**

```haproxy
set-nice <nice>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

Esto establece el factor "nice" de la solicitud/respuesta actual que está siendo procesada.
Solo tiene efecto frente a las demás solicitudes que se procesan al mismo tiempo. El valor por
defecto es 0, a menos que lo altere el ajuste "nice" en la línea "bind". El rango aceptado es
-1024..1024. Cuanto mayor sea el valor, más "amable" será la solicitud. Los valores más bajos
harán que la solicitud sea más importante que las otras. Esto puede ser útil para mejorar la
velocidad de algunas solicitudes, o bajar la prioridad de solicitudes no importantes. Usar este
ajuste sin experimentación previa puede provocar una ralentización importante.

<a id="entry-4-4-set-path"></a>

**`set-path <fmt>`**

```haproxy
set-path <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

    Esto reescribe la ruta de la solicitud con el resultado de la evaluación de la cadena de
    formato `<fmt>`. La cadena de consulta, si existe, se deja intacta. Si se encuentra un
    esquema y una autoridad antes de la ruta, también se dejan intactos. Si la solicitud no
    tiene una ruta ("*"), esta se reemplaza con el formato. Esto puede usarse, por ejemplo,
    para anteponer un componente de directorio delante de una ruta. Ver también "http-request
    set-query" y "http-request set-uri".

Ejemplo:

```shell
# prepend the host name before the path
http-request set-path /%[hdr(host)]%[path]

```

<a id="entry-4-4-set-pathq"></a>

**`set-pathq <fmt>`**

```haproxy
set-pathq <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto hace lo mismo que "http-request set-path", excepto que la cadena de consulta también se
reescribe. Puede usarse para eliminar la cadena de consulta, incluido el signo de interrogación
(no es posible usando "http-request set-query").

<a id="entry-4-4-set-priority-class"></a>

**`set-priority-class <expr>`**

```haproxy
set-priority-class <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esto se usa para establecer la clase de prioridad de cola de la solicitud actual. El valor debe
ser una expresión de muestra que se convierta a un entero en el rango -2047..2047. Los
resultados fuera de este rango se truncarán. La clase de prioridad determina el orden en que se
procesan las solicitudes encoladas. Los valores más bajos tienen mayor prioridad.

<a id="entry-4-4-set-priority-offset"></a>

**`set-priority-offset <expr>`**

```haproxy
set-priority-offset <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esto se usa para establecer el desplazamiento (offset) de la marca de tiempo de prioridad de
cola de la solicitud actual. El valor debe ser una expresión de muestra que se convierta a un
entero en el rango -524287..524287. Los resultados fuera de este rango se truncarán. Cuando una
solicitud se encola, se ordena primero por la clase de prioridad, luego por la marca de tiempo
actual ajustada por el desplazamiento dado en milisegundos. Los valores más bajos tienen mayor
prioridad. Ten en cuenta que la marca de tiempo resultante solo se rastrea con la suficiente
precisión durante 524,287ms (8m44s287ms). Si la solicitud permanece en cola el tiempo
suficiente para que la marca de tiempo ajustada exceda este valor, se identificará
erróneamente como de la máxima prioridad. Así que es importante establecer "timeout queue" a
un valor donde, al combinarse con el desplazamiento, no exceda este límite.

<a id="entry-4-4-set-query"></a>

**`set-query <fmt>`**

```haproxy
set-query <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto reescribe la cadena de consulta de la solicitud, que aparece después del primer signo de
interrogación ("?"), con el resultado de la evaluación de la cadena de formato `<fmt>`. La
parte anterior al signo de interrogación se deja intacta. Si la solicitud no contiene un signo
de interrogación y el nuevo valor no está vacío, entonces se añade uno al final del URI, seguido
del nuevo valor. Si había un signo de interrogación presente, nunca se eliminará incluso si el
valor está vacío. Esto puede usarse para añadir o eliminar parámetros de la cadena de consulta.

Ver también "http-request set-query" y "http-request set-uri".

Ejemplo:

```shell
# replace "%3D" with "=" in the query string
http-request set-query %[query,regsub(%3D,=,g)]

```

<a id="entry-4-4-set-retries"></a>

**`set-retries <int> | <epxr>`**

```haproxy
set-retries <int> | <epxr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esta acción sobrescribe el valor "retries" especificado solo para el flujo actual. Puede ser un
valor entero, en el rango [0, 100], o una expresión que debe devolver un entero en el rango
[0, 100].

Ten en cuenta que esta acción solo es relevante en el lado del backend y, por tanto, esta regla
solo está disponible para los proxies con capacidad de backend. Tampoco está permitida en
secciones "defaults". Cuando la acción se usa para un listener, se evalúa en el contexto del
frontend. Así que el valor de retries solo se conserva si el flujo no se enruta a un backend
diferente, por ejemplo mediante una regla use-backend. De lo contrario, se preestablecerá el
valor de retries por defecto del backend seleccionado.

Ejemplo:

```text
tcp-request content set-retries 3
http-request set-retries var(txn.retries)
```

<a id="entry-4-4-set-src"></a>

**`set-src <expr>`**

```haproxy
set-src <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Esto se usa para establecer la dirección IP de origen al valor de la expresión especificada.
Útil cuando un proxy delante de HAProxy reescribe la IP de origen, pero proporciona la IP
correcta en una cabecera HTTP; o quieres enmascarar la IP de origen por privacidad. Todas las
llamadas posteriores al fetch "src" devolverán este valor (ver ejemplo).

Argumentos:

```text
<expr>  Es una expresión estándar de HAProxy formada por un sample-fetch
        seguido de algunos convertidores.
```

Ver también "option forwardfor".

Ejemplo:

```shell
http-request set-src hdr(x-forwarded-for)
http-request set-src src,ipmask(24)

# After the masking this will track connections
# based on the IP address with the last byte zeroed out.
http-request track-sc0 src
```

Cuando es posible, set-src conserva el puerto de origen original siempre que la familia de
direcciones lo permita; de lo contrario, el puerto de origen se establece a 0.

<a id="entry-4-4-set-src-port"></a>

**`set-src-port <expr>`**

```haproxy
set-src-port <expr>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

Esto se usa para establecer el puerto de origen al valor de la expresión especificada.

Argumentos:

```text
<expr>  Es una expresión estándar de HAProxy formada por un sample-fetch
        seguido de algunos convertidores.
```

Ejemplo:

```text
http-request set-src-port hdr(x-port)
http-request set-src-port int(4000)
```

Cuando es posible, set-src-port conserva la dirección de origen original siempre que la familia
de direcciones soporte un puerto; de lo contrario, fuerza la dirección de origen a IPv4
"0.0.0.0" antes de reescribir el puerto.

<a id="entry-4-4-set-status"></a>

**`set-status <status> [reason <str>]`**

```haproxy
set-status <status> [reason <str>]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| X

Esto reemplaza el código de estado de la respuesta por `<status>`, que debe ser un entero entre
100 y 999. Opcionalmente, puede proporcionarse un texto de razón personalizado definido por
`<str>`, o se usará como alternativa la razón por defecto para el código especificado. Ten en
cuenta que la cadena de razón solo existe en HTTP/1.x y es ignorada por otras versiones del
protocolo.

Ejemplo:

```shell
# return "431 Request Header Fields Too Large"
http-response set-status 431
# return "503 Slow Down", custom reason
http-response set-status 503 reason "Slow Down".

```

<a id="entry-4-4-set-timeout"></a>

**`set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }`**

```haproxy
set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esta acción sobrescribe el tiempo de espera «client», «connect», «queue», «server», «tarpit» o
«tunnel» especificado, solo para el flujo actual. Cambiar un tiempo de espera no influye en ningún
otro, incluso si se heredan unos de otros durante el análisis de la configuración (consulta el último
ejemplo). El tiempo de espera puede especificarse en milisegundos o con cualquier otra unidad si el
número lleva la unidad como sufijo, tal como se explica al principio de este documento. También es
posible escribir una expresión que deba devolver un número interpretado como un tiempo de espera en
milisegundos.

Ten en cuenta que los tiempos de espera connect, queue, server y tunnel solo son relevantes en el
lado del backend y, por lo tanto, esta regla solo está disponible para los proxies con capacidades de
backend. Del mismo modo, el tiempo de espera client solo es relevante para el lado del frontend. El
tiempo de espera tarpit está disponible para ambos lados. El valor del tiempo de espera debe ser no
nulo para obtener los resultados esperados. Cuando la acción se utiliza para un listener, se evalúa en
el contexto del frontend. Así pues, los valores personalizados de los tiempos de espera del lado del
backend se conservan únicamente si el flujo no se enruta a un backend diferente, por ejemplo mediante
una regla use-backend. De lo contrario, se preestablecerán los valores por defecto del backend
seleccionado.

Ejemplo:

```text
http-request set-timeout tunnel 5s
http-request set-timeout server req.hdr(host),map_int(host.lst)
```

Ejemplo:

```text
http-response set-timeout tunnel 5s
http-response set-timeout server res.hdr(X-Refresh-Seconds),mul(1000)
```

Ejemplo:

```text
defaults
  # This will set both tarpit and queue timeout to 5s as they are not
  # defined
  timeout connect 5s
  timeout client 30s
  timeout server 30s

listen foo
  # This will only change the connect timeout to 10s without affecting
  # queue or tarpit timeouts
  http-request set-timeout connect 10s
```

<a id="entry-4-4-set-tos"></a>

**`set-tos <tos> (deprecated)`**

```haproxy
set-tos <tos> (deprecated)
```

Esto es un alias de «set-fc-tos» (que debería utilizarse en su lugar).

<a id="entry-4-4-set-uri"></a>

**`set-uri <fmt>`**

```haproxy
set-uri <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto reescribe el URI de la solicitud con el resultado de la evaluación de la cadena de formato
`<fmt>`. El esquema, la autoridad, la ruta y la cadena de consulta se reemplazan todos a la vez. Esto
puede utilizarse para reescribir hosts delante de proxies, o para realizar modificaciones complejas
del URI, como mover partes entre la ruta y la cadena de consulta. Si se establece un URI absoluto, se
enviará tal cual a los servidores HTTP/1.1. Si ese no es el comportamiento deseado, el host, la ruta
y/o la cadena de consulta deben establecerse por separado. Consulta también «http-request set-path» y
«http-request set-query».

<a id="entry-4-4-set-var"></a>

**`set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
set-var(<var-name>[,<cond>...]) <expr>
set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esto se utiliza para establecer el contenido de una variable. La variable se declara inline.

Argumentos:

```text
<var-name>   El nombre de la variable. No se puede establecer una variable
             del flujo padre. Consulta la sección 2.8 sobre las variables
             para más detalles.

 <cond>      Un conjunto de condiciones que deben cumplirse todas para que
             la variable se establezca realmente (como "ifnotempty",
             "ifgt", ...). Consulta la descripción del convertidor set-var
             para la lista completa de condiciones posibles.

 <expr>      Es una expresión HAProxy estándar formada por una extracción de
             muestra seguida de algunos convertidores.

 <fmt>       Es el valor expresado mediante las reglas de formato de
             registro personalizado (consulta Formato de registro
             personalizado en la sección 8.2.6).
```

Todos los ámbitos son utilizables para las reglas HTTP, pero los ámbitos «proc» y «sess» son los
únicos utilizables en conjuntos de reglas que no tienen acceso a los contenidos, como «tcp-request
connection» y «tcp-request session».

Ejemplo:

```text
http-request set-var(req.my_var) req.fhdr(user-agent),lower
http-request set-var-fmt(txn.from) %[src]:%[src_port]

```

<a id="entry-4-4-silent-drop"></a>

**`silent-drop [ rst-ttl <ttl> ]`**

```haproxy
silent-drop [ rst-ttl <ttl> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

Esto detiene la evaluación de las reglas y hace que la conexión del lado del cliente desaparezca
repentinamente de una manera dependiente del sistema que intenta evitar que el cliente reciba
notificación. Cuando se invoca sin el argumento rst-ttl, intentamos evitar el envío de cualquier
paquete FIN o RST de vuelta al cliente utilizando TCP_REPAIR. Si esto falla (principalmente por la
falta de privilegios), recurrimos a enviar un paquete RST con un TTL de 1.

El efecto es que el cliente sigue viendo una conexión establecida aunque no exista ninguna en HAProxy,
lo que ahorra recursos. Sin embargo, el equipamiento con estado situado entre HAProxy y el cliente
(cortafuegos, proxies, balanceadores de carga) también conservará la conexión establecida en sus
tablas de sesiones.

El parámetro opcional rst-ttl cambia este comportamiento: no se utiliza TCP_REPAIR y se envía un
paquete RST con un TTL configurable. Con un valor razonable, el paquete RST atraviesa la
infraestructura local, eliminando la conexión en los cortafuegos y otros sistemas, pero desaparece
antes de alcanzar al cliente. Los futuros paquetes del cliente serán entonces descartados ya por el
equipamiento frontal. Estos RST locales protegen los recursos locales, pero no los del cliente. No
debe utilizarse esto salvo que se comprendan plenamente las consecuencias de hacerlo.

<a id="entry-4-4-strict-mode"></a>

**`strict-mode { on | off }`**

```haproxy
strict-mode { on | off }
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

Esto activa o desactiva el modo de reescritura estricta para las reglas siguientes. No afecta a las
reglas declaradas antes que ella y solo es aplicable a las reglas que realizan una reescritura sobre
las solicitudes. Cuando el modo estricto está activado, cualquier fallo de reescritura desencadena un
error interno. De lo contrario, dichos errores se ignoran silenciosamente. El propósito del modo de
reescritura estricta es hacer que algunas reescrituras sean opcionales mientras que otras deben
ejecutarse para poder continuar el procesamiento de la solicitud.

Por defecto, el modo de reescritura estricta está activado. Su valor también se restablece cuando
termina la evaluación de un conjunto de reglas. Así, por ejemplo, si cambias el modo en el frontend,
el modo por defecto se restaura cuando HAProxy comienza la evaluación de las reglas del backend.

<a id="entry-4-4-switch-mode-http"></a>

**`switch-mode http [ proto <name> ]`**

```haproxy
switch-mode http [ proto <name> ]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| - \| - \| -

Esta acción se utiliza para realizar un cambio de protocolo en la conexión. Por ahora solo se
admite el cambio al protocolo HTTP. El protocolo puede especificarse opcionalmente. Esta acción
solo está disponible para un proxy con capacidad de frontend. El cambio de protocolo se realiza
de inmediato y las reglas «tcp-request content» siguientes no se evalúan. Este método de cambio
de protocolo debería preferirse al implícito, que consiste en depender del modo del backend. Al
utilizarla, es posible definir directivas HTTP en un frontend sin ningún aviso. Estas directivas
se evaluarán condicionalmente si se realiza el cambio al protocolo HTTP. Sin embargo, todavía
debe seleccionarse un backend HTTP. Sigue sin estar soportado enrutar una conexión HTTP (haya
cambiado de protocolo o no) hacia un servidor TCP.

Consulta la [sección 4](/es/haproxy/proxies/) sobre Proxies para más detalles sobre los cambios al protocolo HTTP.

<a id="entry-4-4-tarpit"></a>

**`tarpit [ { status | deny_status } <code>] [content-type <type>]`**

```haproxy
tarpit [ { status | deny_status } <code>] [content-type <type>]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

           file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto detiene la evaluación de las reglas y bloquea inmediatamente la solicitud sin responder durante
un retraso especificado por «timeout tarpit» o «timeout connect» si el primero no está definido.
Transcurrido ese retraso, si el cliente sigue conectado, se devuelve una respuesta para que el cliente
no sospeche que ha sido puesto en un tarpit. Los registros informarán de los indicadores «PT». El
objetivo de la regla tarpit es ralentizar a los robots durante un ataque cuando están limitados en el
número de solicitudes simultáneas. Puede ser muy eficiente contra robots muy tontos y reducirá
considerablemente la carga de los cortafuegos en comparación con una regla «deny». Pero frente a
robots desarrollados «correctamente», puede empeorar las cosas al obligar a HAProxy y al cortafuegos
frontal a soportar un número desorbitado de conexiones simultáneas. Por defecto se devuelve un error
HTTP 500. Pero la respuesta puede personalizarse usando la misma sintaxis que las reglas
«http-request return». Así pues, consulta «http-request return» para los detalles.

Por compatibilidad, cuando no se define ningún argumento, o solo "deny_status", se sobrentiende el
argumento «default-errorfiles». Significa que «http-request tarpit [deny_status `<status>`]» es un
alias de «http-request tarpit [status `<status>`] default-errorfiles». No se evalúa ninguna regla
«http-request» más. Consulta también «http-request return» y «http-request silent-drop».

<a id="entry-4-4-track-sc0"></a>

**`track-sc0 <key> [table <table>]`**

```haproxy
track-sc0 <key> [table <table>]
track-sc1 <key> [table <table>]
track-sc2 <key> [table <table>]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| X \| -

Esto activa el seguimiento de los contadores de persistencia desde la solicitud actual. Estas reglas
no detienen la evaluación ni cambian la acción por defecto. El número de contadores que la misma
conexión puede seguir simultáneamente lo establece el parámetro global «tune.stick-counters», cuyo
valor por defecto es MAX_SESS_STKCTR si se define en tiempo de compilación (se informa en haproxy
-vv) y cuyo valor por defecto es 3, de modo que el número de track-sc está entre 0 y
(tune.stick-counters-1). La primera regla «track-sc0» ejecutada activa el seguimiento de los
contadores de la tabla especificada como primer conjunto. La primera regla «track-sc1» ejecutada
activa el seguimiento de los contadores de la tabla especificada como segundo conjunto. La primera
regla «track-sc2» ejecutada activa el seguimiento de los contadores de la tabla especificada como
tercer conjunto. Es una práctica recomendada utilizar el primer conjunto de contadores para los
contadores por frontend y el segundo para los por backend. Pero esto es solo una orientación: todos
pueden utilizarse en cualquier parte.

Argumentos:

```text
<key>   es obligatorio y es una regla de expresión de muestra tal como se
        describe en la sección 7.3. Describe qué elementos de la conexión,
        solicitud o respuesta entrantes se analizarán, extraerán,
        combinarán y utilizarán para seleccionar qué entrada de la tabla
        actualizar con los contadores.

<table> es una tabla opcional que se utilizará en lugar de la
        predeterminada, que es la stick-table declarada en el proxy
        actual. Todos los contadores de las coincidencias y las
        actualizaciones de la clave se realizarán entonces en esa tabla
        hasta que termine la sesión.
```

Una vez ejecutada una regla «track-sc\*», se busca la clave en la tabla y, si no se encuentra, se
asigna una entrada para ella. Después se conserva un puntero a esa entrada durante toda la vida de la
sesión, y los contadores de esa entrada se actualizan tan a menudo como sea posible, cada vez que se
actualizan los contadores de la sesión, y también sistemáticamente cuando la sesión termina. Los
contadores solo se actualizan para los eventos que ocurren después de iniciado el seguimiento. Como
excepción, los contadores de conexión y los contadores de solicitud se actualizan sistemáticamente
para que reflejen información útil.

Si la entrada sigue contadores de conexiones simultáneas, se cuenta una conexión mientras la entrada
esté siendo seguida, y la entrada no expirará durante ese tiempo. El seguimiento de contadores
también proporciona una ventaja de rendimiento frente a la simple comprobación de las claves, porque
solo se realiza una búsqueda en la tabla para todas las comprobaciones de ACL que hacen uso de ella.

<a id="entry-4-4-unset-var"></a>

**`unset-var(<var-name>)`**

```haproxy
unset-var(<var-name>)
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

Esto se utiliza para eliminar una variable. Consulta la acción «set-var» para más detalles sobre
`<var-name>`.

Ejemplo:

```text
http-request unset-var(req.my_var)

```

<a id="entry-4-4-use-service"></a>

**`use-service <service-name>`**

```haproxy
use-service <service-name>
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

Esta acción ejecuta el servicio TCP o HTTP configurado para responder a la solicitud, según el
conjunto de reglas en que se utilice. La regla es final, es decir, no se evalúa ninguna otra regla en
el mismo conjunto de reglas.

Un servicio puede optar por responder enviando cualquier respuesta válida o puede cerrar
inmediatamente la conexión sin enviar ninguna respuesta. Para los servicios HTTP, una respuesta válida
requiere una respuesta HTTP válida. Fuera de los servicios nativos, por ejemplo el exportador de
Prometheus para servicios HTTP, es posible escribir servicios TCP y HTTP personalizados en Lua.

Argumentos:

```text
<service-name>  es obligatorio. Es el servicio que se invocará
```

Ejemplo:

```text
http-request use-service prometheus-exporter if { path /metrics }

```

<a id="entry-4-4-wait-for-body-time"></a>

**`wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]`**

```haproxy
wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

Esto retrasará el procesamiento de la solicitud o de la respuesta hasta que ocurra una de las
siguientes condiciones:

- Se ha recibido el cuerpo completo de la solicitud, en cuyo caso el procesamiento continúa con
  normalidad.
- Se han recibido `<bytes>` bytes, cuando se da el argumento «at-least» y `<bytes>` es distinto de
  cero, en cuyo caso el procesamiento continúa con normalidad.
- El búfer de la solicitud está lleno, en cuyo caso el procesamiento continúa con normalidad. El
  tamaño de este búfer lo determina la opción «tune.bufsize».
- La solicitud lleva esperando más de `<time>` milisegundos. En este caso, HAProxy responderá al
  cliente con un error 408 «Request Timeout» y detendrá el procesamiento de la solicitud. Ten en
  cuenta que si ocurre primero cualquiera de las otras condiciones, no se agotará este tiempo de
  espera aunque todavía no se haya recibido el cuerpo completo.

La opción «use-large-buffer» puede establecerse para asignar un búfer grande si el normal es
demasiado pequeño para almacenar el cuerpo del mensaje. Para poder utilizarla, debe estar definida la
opción global «tune.bufsize.large».

Esta acción puede utilizarse como sustituto de «option http-buffer-request».

Argumentos:

```text
<time>    es obligatorio. Es el tiempo máximo de espera del cuerpo. Sigue
          el formato de tiempo de HAProxy y se expresa en milisegundos.

<bytes>   es opcional. Es el tamaño mínimo de la carga útil que debe
          recibirse para dejar de esperar. Sigue el formato de tamaño de
          HAProxy y se expresa en bytes. Un valor de 0 (el valor por
          defecto) significa que no hay límite.
```

Ejemplo:

```text
http-request wait-for-body time 1s at-least 1k if METH_POST
```

Consulta también: «option http-buffer-request» y «tune.bufsize.large»

<a id="entry-4-4-wait-for-handshake"></a>

**`wait-for-handshake`**

```haproxy
wait-for-handshake
```

Utilizable en: QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

Esto retrasará el procesamiento de la solicitud hasta que se haya producido el saludo SSL. Resulta
útil sobre todo para retrasar el procesamiento de los early data hasta que estemos seguros de que son
válidos.
