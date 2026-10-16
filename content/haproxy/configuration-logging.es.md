---
title: "8. Registro"
linkTitle: "8. Registro"
weight: 190
description: "Niveles, formatos, perfiles, temporizadores, capturas, estados y ejemplos de registro"
icon: fa-solid fa-file-lines
module: [HAPROXY]
categories: [Tarea]
aliases:
  - /haproxy/configuration/logging/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 8"
---

Uno de los puntos fuertes de HAProxy reside ciertamente en sus registros precisos. Probablemente
ofrece el nivel más fino de información disponible para un producto de este tipo, lo cual es muy
importante para resolver problemas en entornos complejos. La información estándar proporcionada en
los registros incluye puertos del cliente, temporizadores de estado TCP/HTTP, estado preciso del
flujo al terminar y causa precisa de la terminación, información sobre las decisiones de dirigir el
tráfico a un servidor y, por supuesto, la capacidad de capturar cabeceras arbitrarias.

Para mejorar la reactividad de los administradores, ofrece una gran transparencia sobre los problemas
encontrados, tanto internos como externos, y es posible enviar registros a diferentes destinos al
mismo tiempo con filtros de nivel diferentes:

- registros globales a nivel de proceso (errores del sistema, arranque/parada, etc..)
- errores del sistema e internos por instancia (falta de recursos, bugs, ...)
- problemas externos por instancia (servidores activos/caídos, conexiones máximas)
- actividad por instancia (conexiones de clientes), ya sea en el establecimiento o en la terminación.
- control por petición del nivel de registro, p. ej. http-request set-log-level silent if sensitive_request

La capacidad de distribuir diferentes niveles de registros a diferentes servidores de registro
permite que varios equipos de producción interactúen y corrijan sus problemas lo antes posible. Por
ejemplo, el equipo de sistema podría monitorizar los errores globales del sistema, mientras que el
equipo de aplicación podría monitorizar en tiempo real el estado activo/caído de sus servidores, y
el equipo de seguridad podría analizar los registros de actividad con una hora de retraso.

## 8.1. Niveles de registro {#section-8-1}

Las conexiones TCP y HTTP pueden registrarse con información como la fecha, la hora, la dirección IP
de origen, la dirección de destino, la duración de la conexión, los tiempos de respuesta, la
petición HTTP, el código de retorno HTTP, el número de bytes transmitidos, las condiciones en las
que terminó el flujo e incluso los valores de las cookies intercambiadas. Por ejemplo, seguir los
problemas de un usuario concreto. Todos los mensajes pueden enviarse a hasta dos servidores syslog.
Consulta la palabra clave «log» en la [sección 4.2](/es/haproxy/proxies/#section-4-2) para más información sobre las facilidades de registro.

## 8.2. Formatos de registro {#section-8-2}

HAProxy soporta 5 formatos de registro. Varios campos son comunes entre estos formatos y se
detallarán en las secciones siguientes. Algunos pueden variar ligeramente con la configuración, por
indicadores específicos de ciertas opciones. Los formatos soportados son los siguientes:

- el formato por defecto, que es muy básico y se usa muy raramente. Solo proporciona información muy
  básica sobre la conexión entrante en el momento en que se acepta: IP:puerto de origen,
  IP:puerto de destino y nombre del frontend. Este modo acabará desapareciendo, de modo que no se
  describirá en gran profundidad.

- el formato TCP, que es más avanzado. Este formato se activa cuando se establece «option tcplog»
  en el frontend. HAProxy entonces normalmente esperará a que la conexión termine antes de
  registrar. Este formato proporciona información mucho más rica, como temporizadores, contadores
  de conexiones, tamaño de colas, etc... Este formato es el recomendado para proxies TCP puros.

- el formato HTTP, que es el más avanzado para el proxy HTTP. Este formato se activa cuando se
  establece «option httplog» en el frontend. Proporciona la misma información que el formato TCP
  con algunos campos específicos de HTTP, como la petición, el código de estado y las capturas de
  cabeceras y cookies. Este formato es el recomendado para proxies HTTP.

- el formato HTTP CLF, que es equivalente al formato HTTP, pero con los campos dispuestos en el
  mismo orden que el formato CLF. En este modo, todos los temporizadores, capturas, indicadores,
  etc... aparecen uno por campo después del final de los campos comunes, en el mismo orden en que
  aparecen en el formato HTTP estándar.

- el formato de registro personalizado, permite construir tu propia línea de registro.

Las secciones siguientes profundizarán en los detalles de cada uno de estos formatos. La
especificación del formato se realizará a nivel de «campo». Salvo indicación en contrario, un campo
es una porción de texto delimitada por cualquier número de espacios. Dado que los servidores syslog
pueden insertar campos al principio de una línea, siempre se asume que el primer campo es el que
contiene el nombre del proceso y su identificador.

Nota: como las líneas de registro pueden ser bastante largas, los ejemplos de registro de las
secciones siguientes podrían estar partidos en varias líneas. Las líneas de ejemplo de registro
irán precedidas de 3 paréntesis angulares de cierre («\>\>\>») y, cada vez que un registro se parta
en varias líneas, cada línea no final terminará con una barra invertida («&#92;») y la línea
siguiente empezará indentada dos caracteres.

### 8.2.1. Formato de registro por defecto {#section-8-2-1}

Este formato se usa cuando no se establece ninguna opción específica. El registro se emite tan
pronto como se acepta la conexión. Conviene señalar que este es actualmente el único formato que
registra la IP y los puertos de destino de la petición.

Ejemplo:

```shell
    listen www
        mode http
        log global
        server srv1 127.0.0.1:8000

>>> Feb  6 12:12:09 localhost \
      haproxy[14385]: Connect from 10.0.1.2:33312 to 10.0.3.31:8012 \
      (www/HTTP)
```

Campo Formato Extracto del ejemplo anterior

```text
    1   process_name '[' pid ']:'                            haproxy[14385]:
    2   'Connect from'                                          Connect from
    3   source_ip ':' source_port                             10.0.1.2:33312
    4   'to'                                                              to
    5   destination_ip ':' destination_port                   10.0.3.31:8012
    6   '(' frontend_name '/' mode ')'                            (www/HTTP)
```

Descripción detallada de los campos:

- «source_ip» es la dirección IP del cliente que inició la conexión.
- «source_port» es el puerto TCP del cliente que inició la conexión.
- «destination_ip» es la dirección IP a la que se conectó el cliente.
- «destination_port» es el puerto TCP al que se conectó el cliente.
- «frontend_name» es el nombre del frontend (o listener) que recibió y procesó la conexión.
- «mode» es el modo en que opera el frontend (TCP o HTTP).

En el caso de un socket UNIX, las direcciones de origen y destino se marcan como «unix:» y los
puertos reflejan el ID interno del socket que aceptó la conexión (el mismo ID que se reporta en
las estadísticas).

Se desaconseja usar este formato obsoleto en instalaciones nuevas, ya que acabará desapareciendo.

### 8.2.2. Formato de registro TCP {#section-8-2-2}

El formato TCP se usa cuando se especifica «option tcplog» en el frontend, y es el formato
recomendado para proxies TCP puros. Proporciona mucha información valiosa para la resolución de
problemas. Como este formato incluye temporizadores y contadores de bytes, el registro se emite
normalmente al final de la sesión. Puede emitirse antes si se especifica «option logasap», lo cual
tiene sentido en la mayoría de entornos con sesiones largas, como terminales remotos. Las sesiones
que coinciden con las reglas «monitor» nunca se registran. También es posible no emitir registros
para sesiones en las que no se intercambiaron datos entre el cliente y el servidor, especificando
«option dontlognull» en el frontend. Las conexiones satisfactorias no se registrarán si se
especifica «option dontlog-normal» en el frontend.

El formato de registro TCP está declarado internamente como un formato de registro personalizado
basado en la cadena exacta siguiente, que también puede usarse como base para extender el formato
si es necesario. Adicionalmente, puede usarse en su lugar la variable HAPROXY_TCP_LOG_FMT.
Consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6) «Formato de registro personalizado» para ver
cómo usarlo:

```shell
# strict equivalent of "option tcplog"
log-format "%ci:%cp [%t] %ft %b/%s %Tw/%Tc/%Tt %B %ts \
            %ac/%fc/%bc/%sc/%rc %sq/%bq"
# or using the HAPROXY_TCP_LOG_FMT variable
log-format "${HAPROXY_TCP_LOG_FMT}"
```

Y el formato de registro CLF está declarado internamente como un formato de registro personalizado
basado en esta cadena exacta:

```shell
# strict equivalent of "option tcplog clf"
log-format "%{Q}o %{-Q}ci - - [%T] \"TCP \" 000 %B \"\" \"\" %cp \
            %ms %ft %b %s %Th %Tw %Tc %Tt %U %ts-- %ac %fc %bc \
            %sc %rc %sq %bq \"\" \"\" "
```

Algunos campos pueden variar ligeramente según algunas opciones de configuración; estos se marcan
con un asterisco («\*») tras el nombre del campo a continuación.

Ejemplo:

```shell
    frontend fnt
        mode tcp
        option tcplog
        log global
        default_backend bck

    backend bck
        server srv1 127.0.0.1:8000

>>> Feb  6 12:12:56 localhost \
      haproxy[14387]: 10.0.1.2:33313 [06/Feb/2009:12:12:51.443] fnt \
      bck/srv1 0/0/5007 212 -- 0/0/0/0/3 0/0
```

Campo Formato Extracto del ejemplo anterior

```text
    1   process_name '[' pid ']:'                            haproxy[14387]:
    2   client_ip ':' client_port                             10.0.1.2:33313
    3   '[' accept_date ']'                       [06/Feb/2009:12:12:51.443]
    4   frontend_name                                                    fnt
    5   backend_name '/' server_name                                bck/srv1
    6   Tw '/' Tc '/' Tt*                                           0/0/5007
    7   bytes_read*                                                      212
    8   termination_state                                                 --
    9   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*    0/0/0/0/3
   10   srv_queue '/' backend_queue                                      0/0
```

Descripción detallada de los campos:

- «client_ip» es la dirección IP del cliente que inició la conexión TCP hacia HAProxy. Si la
  conexión se aceptó en cambio en un socket UNIX, la dirección IP se reemplazaría por la palabra
  «unix». Ten en cuenta que cuando la conexión se acepta en un socket configurado con
  «accept-proxy» y el protocolo PROXY se usa correctamente, o con «accept-netscaler-cip» y el
  protocolo NetScaler Client IP insertion se usa correctamente, los registros reflejarán la
  información de la conexión reenviada.

- «client_port» es el puerto TCP del cliente que inició la conexión. Si la conexión se aceptó en
  cambio en un socket UNIX, el puerto se reemplazaría por el ID del socket que la aceptó, que
  también se reporta en la interfaz de estadísticas.

- «accept_date» es la fecha exacta en que la conexión fue recibida por HAProxy (que puede diferir
  muy ligeramente de la fecha observada en la red si hubo alguna cola en el backlog del sistema).
  Esta suele ser la misma fecha que puede aparecer en el registro de cualquier cortafuegos previo.
  Cuando se usa en modo HTTP, el campo accept_date se reinicia al primer instante en que la
  conexión está lista para recibir una nueva petición (fin de la respuesta anterior para HTTP/1,
  inmediatamente después de la petición anterior para HTTP/2).

- «frontend_name» es el nombre del frontend (o listener) que recibió y procesó la conexión.

- «backend_name» es el nombre del backend (o listener) que fue seleccionado para gestionar la
  conexión al servidor. Será el mismo que el frontend si no se aplicó ninguna regla de
  conmutación, lo cual es común en aplicaciones TCP.

- «server_name» es el nombre del último servidor al que se envió la conexión, que puede diferir
  del primero si hubo errores de conexión y ocurrió una reasignación. Ten en cuenta que este
  servidor pertenece al backend que procesó la petición. Si la conexión se abortó antes de
  alcanzar un servidor, se indica «`<NOSRV>`» en lugar de un nombre de servidor.

- «Tw» es el tiempo total en milisegundos pasado esperando en las distintas colas. Puede ser «-1»
  si la conexión se abortó antes de alcanzar la cola. Consulta «Temporizadores» más abajo para más
  detalles.

- «Tc» es el tiempo total en milisegundos pasado esperando el establecimiento de la conexión con
  el servidor final, incluidos los reintentos. Puede ser «-1» si la conexión se abortó antes de
  que pudiera establecerse una conexión. Consulta «Temporizadores» más abajo para más detalles.

- «Tt» es el tiempo total en milisegundos transcurrido entre la aceptación y el último cierre.
  Cubre todo el procesamiento posible. Hay una excepción: si se especificó «option logasap», el
  conteo del tiempo se detiene en el momento en que se emite el registro. En este caso, se añade
  un signo «+» delante del valor, lo que indica que el final será mayor. Consulta «Temporizadores»
  más abajo para más detalles.

- «bytes_read» es el número total de bytes transmitidos del servidor al cliente cuando se emite
  el registro. Si se especifica «option logasap», este valor irá precedido de un signo «+» que
  indica que el final puede ser mayor. Ten en cuenta que este valor es un contador de 64 bits,
  así que las herramientas de análisis de registros deben poder manejarlo sin desbordarse.

- «termination_state» es la condición en que estaba la sesión cuando la sesión terminó. Esto
  indica el estado de la sesión, qué lado provocó el final de la sesión y por qué motivo (tiempo
  de espera agotado, error, ...). Los indicadores normales deberían ser «--», lo que indica que
  la sesión fue cerrada por cualquiera de los extremos sin quedar datos en los búferes. Consulta más
  abajo «Estado del flujo en la desconexión» para más detalles.

- «actconn» es el número total de conexiones simultáneas en el proceso cuando se registró la
  sesión. Es útil para detectar cuándo se han alcanzado ciertos límites del sistema por proceso.
  Por ejemplo, si actconn está cerca de 512 cuando ocurren múltiples errores de conexión, es muy
  probable que el sistema limite el proceso a un máximo de 1024 descriptores de ficheros y que
  todos estén en uso. Consulta la [sección 3](/es/haproxy/global/) «Sección global» para encontrar cómo ajustar el sistema.

- «feconn» es el número total de conexiones simultáneas en el frontend cuando se registró la
  sesión. Es útil para estimar la cantidad de recursos necesaria para sostener cargas altas y
  para detectar cuándo se ha alcanzado el «maxconn» del frontend. Cuando este valor aumenta a
  grandes saltos, lo más habitual es que haya congestión en los servidores del backend, aunque a
  veces puede deberse a un ataque de denegación de servicio.

- «beconn» es el número total de conexiones simultáneas gestionadas por el backend cuando se
  registró la sesión. Incluye el número total de conexiones simultáneas activas en los servidores
  así como el número de conexiones pendientes en colas. Es útil para estimar la cantidad de
  servidores adicionales necesarios para soportar cargas altas en una aplicación dada. Cuando
  este valor aumenta a grandes saltos, lo más habitual es que haya congestión en los servidores
  del backend, aunque a veces puede deberse a un ataque de denegación de servicio.

- «srv_conn» es el número total de conexiones simultáneas todavía activas en el servidor cuando
  se registró la sesión. Nunca puede exceder el parámetro «maxconn» configurado del servidor. Si
  este valor está muy a menudo cerca o igual al «maxconn» del servidor, significa que hay mucha
  regulación de tráfico, lo que indica que el valor maxconn del servidor es demasiado bajo, o que
  no hay suficientes servidores para procesar la carga con un tiempo de respuesta óptimo. Cuando
  solo el «srv_conn» de uno de los servidores es alto, normalmente significa que ese servidor
  tiene algún problema que hace que las conexiones tarden más en procesarse que en otros
  servidores.

- «retries» es el número de reintentos de conexión experimentados por esta sesión al intentar
  conectarse al servidor. Normalmente debe ser cero, salvo que se esté deteniendo un servidor en
  el mismo momento en que se intentó la conexión. Los reintentos frecuentes generalmente indican
  un problema de red entre HAProxy y el servidor, o un backlog del sistema mal configurado en el
  servidor que impide que las conexiones nuevas se pongan en cola. Este campo puede llevar
  opcionalmente un prefijo con el signo «+», lo que indica que la sesión ha experimentado una
  reasignación tras alcanzarse el número máximo de reintentos en el servidor inicial. En este
  caso, el nombre de servidor que aparece en el registro es aquel al que se reasignó la conexión,
  y no el primero, aunque ambos a veces pueden ser el mismo, por ejemplo en el caso de hashing.
  Así, como regla general, cuando hay un «+» delante del contador de reintentos, ese contador no
  debe atribuirse al servidor registrado.

- «srv_queue» es el número total de peticiones que fueron procesadas antes que esta en la cola
  del servidor. Es cero cuando la petición no pasó por la cola del servidor. Permite estimar el
  tiempo de respuesta aproximado del servidor dividiendo el tiempo pasado en cola por el número
  de peticiones de la cola. Conviene señalar que si una sesión experimenta una reasignación y
  pasa por dos colas de servidor, sus posiciones serán acumulativas. Una petición no debería
  pasar tanto por la cola del servidor como por la del backend a menos que ocurra una
  reasignación.

- «backend_queue» es el número total de peticiones que fueron procesadas antes que esta en la
  cola global del backend. Es cero cuando la petición no pasó por la cola global. Permite estimar
  la longitud media de la cola, que se traduce fácilmente en un número de servidores faltantes al
  dividirla por el parámetro «maxconn» de un servidor. Conviene señalar que si una sesión
  experimenta una reasignación, puede pasar dos veces por la cola del backend, y entonces ambas
  posiciones serán acumulativas. Una petición no debería pasar tanto por la cola del servidor
  como por la del backend a menos que ocurra una reasignación.

### 8.2.3. Formato de registro HTTP {#section-8-2-3}

El formato HTTP es el más completo y el mejor adaptado a los proxies HTTP. Se activa cuando se
especifica «option httplog» en el frontend. Proporciona el mismo nivel de información que el
formato TCP con características adicionales específicas del protocolo HTTP. Igual que el formato
TCP, el registro se emite normalmente al final del flujo, salvo que se especifique «option
logasap», lo que generalmente solo tiene sentido para sitios de descargas. Un flujo que coincide
con las reglas «monitor» nunca se registrará. También es posible no registrar flujos en los que
el cliente no envió datos, especificando «option dontlognull» en el frontend. Las conexiones
satisfactorias no se registrarán si se especifica «option dontlog-normal» en el frontend.

El formato de registro HTTP está declarado internamente como un formato de registro personalizado
basado en la cadena exacta siguiente, que también puede usarse como base para extender el formato
si es necesario. Adicionalmente, puede usarse en su lugar la variable HAPROXY_HTTP_LOG_FMT.
Consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6) «Formato de registro personalizado» para ver
cómo usarlo:

```shell
# strict equivalent of "option httplog"
log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC \
            %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r"
# or using the HAPROXY_HTTP_LOG_FMT variable
log-format "${HAPROXY_HTTP_LOG_FMT}"
```

Y el formato de registro CLF está declarado internamente como un formato de registro personalizado
basado en esta cadena exacta:

```shell
# strict equivalent of "option httplog clf"
log-format "%{+Q}o %{-Q}ci - - [%trg] %r %ST %B \"\" \"\" %cp \
            %ms %ft %b %s %TR %Tw %Tc %Tr %Ta %tsc %ac %fc \
            %bc %sc %rc %sq %bq %CC %CS %hrl %hsl"
```

La mayoría de los campos se comparten con el registro TCP, siendo algunos diferentes. Algunos
campos pueden variar ligeramente según algunas opciones de configuración. Estos se marcan con un
asterisco («\*») tras el nombre del campo a continuación.

Ejemplo:

```shell
    frontend http-in
        mode http
        option httplog
        log global
        default_backend bck

    backend static
        server srv1 127.0.0.1:8000

>>> Feb  6 12:14:14 localhost \
      haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
      static/srv1 10/0/30/69/109 200 2750 - - ---- 1/1/1/1/0 0/0 {1wt.eu} \
      {} "GET /index.html HTTP/1.1"
```

Campo Formato Extracto del ejemplo anterior

```text
    1   process_name '[' pid ']:'                            haproxy[14389]:
    2   client_ip ':' client_port                             10.0.1.2:33317
    3   '[' request_date ']'                      [06/Feb/2009:12:14:14.655]
    4   frontend_name                                                http-in
    5   backend_name '/' server_name                             static/srv1
    6   TR '/' Tw '/' Tc '/' Tr '/' Ta*                       10/0/30/69/109
    7   status_code                                                      200
    8   bytes_read*                                                     2750
    9   captured_request_cookie                                            -
   10   captured_response_cookie                                           -
   11   termination_state                                               ----
   12   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*    1/1/1/1/0
   13   srv_queue '/' backend_queue                                      0/0
   14   '{' captured_request_headers* '}'                   {haproxy.1wt.eu}
   15   '{' captured_response_headers* '}'                                {}
   16   '"' http_request '"'                      "GET /index.html HTTP/1.1"
```

Descripción detallada de los campos:

- «client_ip» es la dirección IP del cliente que inició la conexión TCP hacia HAProxy. Si la
  conexión se aceptó en cambio en un socket UNIX, la dirección IP se reemplazaría por la palabra
  «unix». Ten en cuenta que cuando la conexión se acepta en un socket configurado con
  «accept-proxy» y el protocolo PROXY se usa correctamente, o con «accept-netscaler-cip» y el
  protocolo NetScaler Client IP insertion se usa correctamente, los registros reflejarán la
  información de la conexión reenviada.

- «client_port» es el puerto TCP del cliente que inició la conexión. Si la conexión se aceptó en
  cambio en un socket UNIX, el puerto se reemplazaría por el ID del socket que la aceptó, que
  también se reporta en la interfaz de estadísticas.

- «request_date» es la fecha exacta en que el primer byte de la petición HTTP fue recibido por
  HAProxy (campo de registro %tr).

- «frontend_name» es el nombre del frontend (o listener) que recibió y procesó la conexión.

- «backend_name» es el nombre del backend (o listener) que fue seleccionado para gestionar la
  conexión al servidor. Será el mismo que el frontend si no se aplicó ninguna regla de
  conmutación.

- «server_name» es el nombre del último servidor al que se envió la conexión, que puede diferir
  del primero si hubo errores de conexión y ocurrió una reasignación. Ten en cuenta que este
  servidor pertenece al backend que procesó la petición. Si la petición se abortó antes de
  alcanzar un servidor, se indica «`<NOSRV>`» en lugar de un nombre de servidor. Si la petición
  fue interceptada por el subsistema de estadísticas, se indica «`<STATS>`» en su lugar.

- «TR» es el tiempo total en milisegundos pasado esperando una petición HTTP completa del cliente
  (sin contar el cuerpo) después de recibirse el primer byte. Puede ser «-1» si la conexión se
  abortó antes de que pudiera recibirse una petición completa o si se recibió una petición
  errónea. Siempre debería ser muy pequeño porque una petición generalmente cabe en un solo
  paquete. Tiempos grandes aquí generalmente indican problemas de red entre el cliente y HAProxy
  o peticiones tecleadas a mano. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
  detalles.

- «Tw» es el tiempo total en milisegundos pasado esperando en las distintas colas. Puede ser
  «-1» si la conexión se abortó antes de alcanzar la cola. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de
  temporización» para más detalles.

- «Tc» es el tiempo total en milisegundos pasado esperando el establecimiento de la conexión con
  el servidor final, incluidos los reintentos. Puede ser «-1» si la petición se abortó antes de
  que pudiera establecerse una conexión. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización»
  para más detalles.

- «Tr» es el tiempo total en milisegundos pasado esperando que el servidor enviara una respuesta
  HTTP completa, sin contar los datos. Puede ser «-1» si la petición se abortó antes de que
  pudiera recibirse una respuesta completa. Generalmente coincide con el tiempo de procesamiento
  del servidor para la petición, aunque puede verse alterado por la cantidad de datos enviados
  por el cliente al servidor. Tiempos grandes aquí en peticiones «GET» generalmente indican un
  servidor sobrecargado. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
  detalles.

- «Ta» es el tiempo durante el cual la petición permaneció activa en HAProxy, que es el tiempo
  total en milisegundos transcurrido entre la recepción del primer byte de la petición y el envío
  del último byte de la respuesta. Cubre todo el procesamiento posible excepto el handshake
  (consulta Th) y el tiempo de inactividad (consulta Ti). Hay una excepción: si se especificó
  «option logasap», el conteo del tiempo se detiene en el momento en que se emite el registro.
  En este caso, se añade un signo «+» delante del valor, lo que indica que el final será mayor.
  Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más detalles.

- «status_code» es el código de estado HTTP devuelto al cliente. Este estado generalmente lo
  establece el servidor, pero también puede establecerlo HAProxy cuando el servidor no puede ser
  alcanzado o cuando su respuesta es bloqueada por HAProxy.

- «bytes_read» es el número total de bytes transmitidos al cliente cuando se emite el registro.
  Esto incluye las cabeceras HTTP. Si se especifica «option logasap», este valor irá precedido
  de un signo «+» que indica que el final puede ser mayor. Ten en cuenta que este valor es un
  contador de 64 bits, así que las herramientas de análisis de registros deben poder manejarlo
  sin desbordarse.

- «captured_request_cookie» es una entrada opcional «nombre=valor» que indica que el cliente
  tenía esta cookie en la petición. El nombre de la cookie y su longitud máxima los define la
  instrucción «capture cookie» en la configuración del frontend. El campo es un guion sencillo
  («-») cuando la opción no está establecida. Solo puede capturarse una cookie; generalmente se
  usa para rastrear los intercambios de ID de sesión entre un cliente y un servidor y detectar
  cruces de sesión entre clientes debidos a bugs de la aplicación. Para más detalles, consulta
  la sección «Captura de cabeceras y cookies HTTP» más abajo.

- «captured_response_cookie» es una entrada opcional «nombre=valor» que indica que el servidor
  devolvió una cookie con su respuesta. El nombre de la cookie y su longitud máxima los define
  la instrucción «capture cookie» en la configuración del frontend. El campo es un guion
  sencillo («-») cuando la opción no está establecida. Solo puede capturarse una cookie;
  generalmente se usa para rastrear los intercambios de ID de sesión entre un cliente y un
  servidor y detectar cruces de sesión entre clientes debidos a bugs de la aplicación. Para más
  detalles, consulta la sección «Captura de cabeceras y cookies HTTP» más abajo.

- «termination_state» es la condición en que estaba el flujo cuando el flujo terminó. Esto
  indica el estado del flujo, qué lado provocó el final del flujo y por qué motivo (tiempo de
  espera agotado, error, ...), igual que en los registros TCP, e información sobre las
  operaciones de persistencia en las cookies en los dos últimos caracteres. Los indicadores
  normales deberían empezar por «--», lo que indica que el flujo fue cerrado por cualquiera de
  los extremos sin quedar datos en los búferes. Consulta más abajo «Estado del flujo en la
  desconexión» para más detalles.

- «actconn» es el número total de conexiones simultáneas en el proceso cuando se registró el
  flujo. Es útil para detectar cuándo se han alcanzado ciertos límites del sistema por proceso.
  Por ejemplo, si actconn está cerca de 512 o 1024 cuando ocurren múltiples errores de conexión,
  es muy probable que el sistema limite el proceso a un máximo de 1024 descriptores de ficheros
  y que todos estén en uso. Consulta la [sección 3](/es/haproxy/global/) «Sección global» para encontrar cómo ajustar el sistema.

- «feconn» es el número total de conexiones simultáneas en el frontend cuando se registró el
  flujo. Es útil para estimar la cantidad de recursos necesaria para sostener cargas altas y
  para detectar cuándo se ha alcanzado el «maxconn» del frontend. Cuando este valor aumenta a
  grandes saltos, lo más habitual es que haya congestión en los servidores del backend, aunque a
  veces puede deberse a un ataque de denegación de servicio.

- «beconn» es el número total de conexiones simultáneas gestionadas por el backend cuando se
  registró el flujo. Incluye el número total de conexiones simultáneas activas en los servidores
  así como el número de conexiones pendientes en colas. Es útil para estimar la cantidad de
  servidores adicionales necesarios para soportar cargas altas en una aplicación dada. Cuando
  este valor aumenta a grandes saltos, lo más habitual es que haya congestión en los servidores
  del backend, aunque a veces puede deberse a un ataque de denegación de servicio.

- «srv_conn» es el número total de conexiones simultáneas todavía activas en el servidor cuando
  se registró el flujo. Nunca puede exceder el parámetro «maxconn» configurado del servidor. Si
  este valor está muy a menudo cerca o igual al «maxconn» del servidor, significa que hay mucha
  regulación de tráfico, lo que indica que el valor maxconn del servidor es demasiado bajo, o
  que no hay suficientes servidores para procesar la carga con un tiempo de respuesta óptimo.
  Cuando solo el «srv_conn» de uno de los servidores es alto, normalmente significa que ese
  servidor tiene algún problema que hace que las peticiones tarden más en procesarse que en
  otros servidores.

- «retries» es el número de reintentos de conexión experimentados por este flujo al intentar
  conectarse al servidor. Normalmente debe ser cero, salvo que se esté deteniendo un servidor en
  el mismo momento en que se intentó la conexión. Los reintentos frecuentes generalmente indican
  un problema de red entre HAProxy y el servidor, o un backlog del sistema mal configurado en el
  servidor que impide que las conexiones nuevas se pongan en cola. Este campo puede llevar
  opcionalmente un prefijo con el signo «+», lo que indica que el flujo ha experimentado una
  reasignación tras alcanzarse el número máximo de reintentos en el servidor inicial. En este
  caso, el nombre de servidor que aparece en el registro es aquel al que se reasignó la
  conexión, y no el primero, aunque ambos a veces pueden ser el mismo, por ejemplo en el caso de
  hashing. Así, como regla general, cuando hay un «+» delante del contador de reintentos, ese
  contador no debe atribuirse al servidor registrado.

- «srv_queue» es el número total de peticiones que fueron procesadas antes que esta en la cola
  del servidor. Es cero cuando la petición no pasó por la cola del servidor. Permite estimar el
  tiempo de respuesta aproximado del servidor dividiendo el tiempo pasado en cola por el número
  de peticiones de la cola. Conviene señalar que si un flujo experimenta una reasignación y pasa
  por dos colas de servidor, sus posiciones serán acumulativas. Una petición no debería pasar
  tanto por la cola del servidor como por la del backend a menos que ocurra una reasignación.

- «backend_queue» es el número total de peticiones que fueron procesadas antes que esta en la
  cola global del backend. Es cero cuando la petición no pasó por la cola global. Permite
  estimar la longitud media de la cola, que se traduce fácilmente en un número de servidores
  faltantes al dividirla por el parámetro «maxconn» de un servidor. Conviene señalar que si un
  flujo experimenta una reasignación, puede pasar dos veces por la cola del backend, y entonces
  ambas posiciones serán acumulativas. Una petición no debería pasar tanto por la cola del
  servidor como por la del backend a menos que ocurra una reasignación.

- «captured_request_headers» es una lista de cabeceras capturadas en la petición debido a la
  presencia de la instrucción «capture request header» en el frontend. Pueden capturarse varias
  cabeceras; se delimitarán con una barra vertical («\|»). Cuando no hay ninguna captura
  activada, las llaves no aparecen, lo que provoca un desplazamiento de los campos restantes.
  Es importante señalar que este campo puede contener espacios y que usarlo requiere un
  analizador de registros más avanzado que cuando no se usa. Consulta la sección «Captura de
  cabeceras y cookies HTTP» más abajo para más detalles.

- «captured_response_headers» es una lista de cabeceras capturadas en la respuesta debido a la
  presencia de la instrucción «capture response header» en el frontend. Pueden capturarse varias
  cabeceras; se delimitarán con una barra vertical («\|»). Cuando no hay ninguna captura
  activada, las llaves no aparecen, lo que provoca un desplazamiento de los campos restantes.
  Es importante señalar que este campo puede contener espacios y que usarlo requiere un
  analizador de registros más avanzado que cuando no se usa. Consulta la sección «Captura de
  cabeceras y cookies HTTP» más abajo para más detalles.

- «http_request» es la línea completa de la petición HTTP, incluidos el método, la petición y la
  cadena de versión HTTP. Los caracteres no imprimibles se codifican (consulta más abajo la
  sección «Caracteres no imprimibles»). Este es siempre el último campo, siempre está delimitado
  por comillas y es el único que puede contener comillas. Si se añaden campos nuevos al formato
  de registro, se añadirán antes de este campo. Este campo puede quedar truncado si la petición
  es enorme y no cabe en el búfer syslog estándar (1024 caracteres). Esta es la razón por la que
  este campo debe permanecer siempre el último.

### 8.2.4. Formato de registro HTTPS {#section-8-2-4}

El formato HTTPS es el mejor adaptado a las conexiones HTTP sobre SSL. Es una extensión del
formato HTTP (consulta la [sección 8.2.3](/es/haproxy/configuration-logging/#section-8-2-3)) a la que se añade información relacionada con SSL. Se activa cuando se
especifica «option httpslog» en el frontend. Igual que los formatos TCP y HTTP, el registro se
emite normalmente al final del flujo, salvo que se especifique «option logasap». Un flujo que
coincide con las reglas «monitor» nunca se registrará. También es posible no registrar flujos en
los que el cliente no envió datos, especificando «option dontlognull» en el frontend. Las
conexiones satisfactorias no se registrarán si se especifica «option dontlog-normal» en el
frontend.

El formato de registro HTTPS está declarado internamente como un formato de registro
personalizado basado en la cadena exacta siguiente, que también puede usarse como base para
extender el formato si es necesario. Adicionalmente, puede usarse en su lugar la variable
HAPROXY_HTTPS_LOG_FMT. Consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6) «Formato de registro personalizado» para
ver cómo usarlo:

```shell
# strict equivalent of "option httpslog"
log-format "%ci:%cp [%tr] %ft %b/%s %TR/%Tw/%Tc/%Tr/%Ta %ST %B %CC \
           %CS %tsc %ac/%fc/%bc/%sc/%rc %sq/%bq %hr %hs %{+Q}r \
           %[fc_err]/%[ssl_fc_err,hex]/%[ssl_c_err]/\
           %[ssl_c_ca_err]/%[ssl_fc_is_resumed] %[ssl_fc_sni]/%sslv/%sslc"
# or using the HAPROXY_HTTPS_LOG_FMT variable
log-format "${HAPROXY_HTTPS_LOG_FMT}"
```

Este formato es básicamente el HTTP (consulta la [sección 8.2.3](/es/haproxy/configuration-logging/#section-8-2-3)) con campos nuevos añadidos. Los campos
nuevos (líneas 17 y 18) se detallan aquí. Para los HTTP, consulta la sección HTTP.

Ejemplo:

```shell
    frontend https-in
        mode http
        option httpslog
        log global
        bind *:443 ssl crt mycerts/srv.pem ...
        default_backend bck

    backend static
        server srv1 127.0.0.1:8000 ssl crt mycerts/clt.pem ...

>>> Feb  6 12:14:14 localhost \
      haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] https-in \
      static/srv1 10/0/30/69/109 200 2750 - - ---- 1/1/1/1/0 0/0 {1wt.eu} \
      {} "GET /index.html HTTP/1.1" 0/0/0/0/0 \
      1wt.eu/TLSv1.3/TLS_AES_256_GCM_SHA384
```

Campo Formato Extracto del ejemplo anterior

```text
    1   process_name '[' pid ']:'                              haproxy[14389]:
    2   client_ip ':' client_port                               10.0.1.2:33317
    3   '[' request_date ']'                        [06/Feb/2009:12:14:14.655]
    4   frontend_name                                                 https-in
    5   backend_name '/' server_name                               static/srv1
    6   TR '/' Tw '/' Tc '/' Tr '/' Ta*                         10/0/30/69/109
    7   status_code                                                        200
    8   bytes_read*                                                       2750
    9   captured_request_cookie                                              -
   10   captured_response_cookie                                             -
   11   termination_state                                                 ----
   12   actconn '/' feconn '/' beconn '/' srv_conn '/' retries*      1/1/1/1/0
   13   srv_queue '/' backend_queue                                        0/0
   14   '{' captured_request_headers* '}'                     {haproxy.1wt.eu}
   15   '{' captured_response_headers* '}'                                  {}
   16   '"' http_request '"'                        "GET /index.html HTTP/1.1"
   17   fc_err '/' ssl_fc_err '/' ssl_c_err
        '/' ssl_c_ca_err '/' ssl_fc_is_resumed                       0/0/0/0/0
   18   ssl_fc_sni '/' ssl_version
        '/' ssl_ciphers                  1wt.eu/TLSv1.3/TLS_AES_256_GCM_SHA384
```

Descripción detallada de los campos:

- «fc_err» es el estado de la conexión por el lado del frontend. Corresponde a la extracción de
  muestra «fc_err». Consulta las funciones de extracción de muestra «fc_err» y «fc_err_str» para
  más información.

- «ssl_fc_err» es el último error de la primera pila de errores SSL que se produjo en la
  conexión desde la perspectiva del frontend. Podría usarse, por ejemplo, para detectar errores
  de handshake SSL. Será 0 si todo fue bien. Consulta la descripción de la extracción de muestra
  «ssl_fc_err» para más información.

- «ssl_c_err» es el estado del proceso de verificación del certificado del cliente. El handshake
  puede tener éxito con un código de error de verificación no nulo si este es uno ignorado.
  Consulta la extracción de muestra «ssl_c_err» y la opción «crt-ignore-err».

- «ssl_c_ca_err» es el estado del proceso de verificación de la cadena de certificados del
  cliente. El handshake puede tener éxito con un código de error de verificación no nulo si
  este es uno ignorado. Consulta la extracción de muestra «ssl_c_ca_err» y la opción
  «ca-ignore-err».

- «ssl_fc_is_resumed» es verdadero si la sesión TLS entrante se reanudó con la caché con estado
  o un ticket sin estado. No olvides que una sesión TLS puede compartirse entre múltiples
  peticiones.

- «ssl_fc_sni» es el SNI (Server Name Indication) presentado por el cliente para seleccionar el
  certificado que se usará. Normalmente coincide con el nombre de host de la primera petición
  de una conexión. La ausencia de este campo puede indicar que el cliente no envió el SNI, y
  llevará a haproxy a usar el certificado por defecto, o a rechazar la conexión en caso de
  strict-sni.

- «ssl_version» es la versión SSL del frontend.

- «ssl_ciphers» es el cifrado SSL usado para la conexión.

### 8.2.5. Formato de registro de errores {#section-8-2-5}

Cuando una conexión entrante falla por un handshake SSL o una cabecera de protocolo PROXY
inválida, HAProxy registrará el evento usando un formato de línea más corto y fijo, salvo que se
defina un formato de registro de errores dedicado mediante una línea «error-log-format». Por
defecto, los registros se emiten al nivel LOG_INFO, salvo que la opción «log-separate-errors»
esté establecida en el backend, en cuyo caso se usará el nivel LOG_ERR. Las conexiones en las
que no se intercambian datos (p. ej., sondeos) no se registran si la opción «dontlognull» está
establecida.

El formato por defecto tiene este aspecto:

```text
  >>> Dec  3 18:27:14 localhost \
        haproxy[6103]: 127.0.0.1:56059 [03/Dec/2012:17:35:10.380] frt/f1: \
        Connection error during SSL handshake

Campo   Formato                                Extracto del ejemplo anterior
```

```text
    1   process_name '[' pid ']:'                             haproxy[6103]:
    2   client_ip ':' client_port                            127.0.0.1:56059
    3   '[' accept_date ']'                       [03/Dec/2012:17:35:10.380]
    4   frontend_name "/" bind_name ":"                              frt/f1:
    5   message                        Connection error during SSL handshake
```

Estos campos solo proporcionan información mínima para ayudar a depurar fallos de conexión.

Al usar la directiva «error-log-format», el formato de registro heredado descrito anteriormente
ya no se usará, y todas las líneas de registro de errores seguirán el formato definido.

A continuación un ejemplo de error-log-format razonablemente completo; reportará la dirección y
el puerto de origen, la fecha accept() de la conexión, el nombre del frontend, el número de
conexiones activas en el proceso y en este frontend, el identificador interno de error de
haproxy en la conexión frontal, el número de error de OpenSSL en hexadecimal (que puede
copiarse y pegarse en «openssl errstr» para su decodificación completa), el estado de
extracción del certificado del cliente (0 indica que no hay error), el estado de validación del
certificado del cliente con la CA (0 indica que no hay error), un booleano que indica si la
conexión es nueva o fue reanudada, la indicación opcional de nombre de servidor (SNI)
proporcionada por el cliente, el nombre de la versión SSL y los cifrados SSL usados en la
conexión, si los hay. Ten en cuenta que los errores de conexión del backend nunca se reportan
aquí, ya que para que una conexión de backend falle, tendría que haber pasado por un flujo
satisfactorio, y por tanto estará disponible como registro de tráfico normal (consulta option
httplog u option httpslog).

```haproxy
# detailed frontend connection error log
error-log-format "%ci:%cp [%tr] %ft %ac/%fc %[fc_err]/\
      %[ssl_fc_err,hex]/%[ssl_c_err]/%[ssl_c_ca_err]/%[ssl_fc_is_resumed] \
      %[ssl_fc_sni]/%sslv/%sslc"
```

### 8.2.6. Formato de registro personalizado {#section-8-2-6}

Históricamente, los formatos de registro personalizados solo se usaban para producir registros.
Pero su comodidad para producir una cadena ensamblando múltiples expresiones complejas hizo que
los adoptaran muchas directivas que antes tomaban solo una cadena como argumento y que ahora
también pueden tomar una definición de formato de registro personalizado. Tales argumentos,
designados comúnmente por «`<fmt>`» en este documento, se definen exactamente igual que el
argumento de la directiva «log-format», descrito aquí.

En lo que respecta a los registros, y cuando los formatos por defecto no son suficientes, es
posible definir otros nuevos con mucho detalle. Como crear un log-format desde cero no siempre
es una tarea trivial, se recomienda encarecidamente echar primero un vistazo a los formatos
existentes («option tcplog», «option httplog», «option httpslog»), elegir el que más se parezca
a lo esperado, copiar su cadena «log-format» equivalente y ajustarla.

Una definición de formato de registro personalizado es un solo argumento desde la perspectiva de
la configuración. Esto significa que no puede contener espacios (espacios o tabuladores), salvo
que estos estén escapados usando el carácter barra invertida («&#92;»), o que toda la definición
vaya entre comillas (que es la forma recomendada de usarlos). El uso de cadenas de formato sin
entrecomillar ya no se recomienda, ya que la historia ha demostrado que era muy propenso a
errores, porque una sola barra invertida ausente podía provocar el truncamiento silencioso del
formato. Todavía es común encontrarse tales configuraciones debido a la adopción masiva de los
formatos de registro tras la versión 1.5-dev9, 3 años antes de que las comillas fueran
utilizables, pero se recomienda convertirlas a cadenas entre comillas y eliminar ahora las
barras invertidas.

Una definición de formato de registro está formada por cualquier número de elementos de formato
de registro separados por texto y espacios. Un elemento de formato de registro empieza por el
carácter «%». Para emitir un «%» literal, debe ir precedido de otro «%», resultando en «%%».

Los elementos de logformat pueden ser alias o expresiones de muestra:

Si un elemento se nombra entre corchetes («[» .. «]») entonces se usa como regla de expresión de
muestra (consulta la [sección 7.3](/es/haproxy/acls-and-samples/#section-7-3)). Esto es útil para añadir alguna información menos común, como
el DN del certificado SSL del cliente, o para registrar la clave que se usaría para almacenar
una entrada en una stick-table. También se usa comúnmente con acciones ajenas al registro
(manipulación de cabeceras, variables, etc).

Si no, si el elemento se nombra con un nombre alfanumérico, es un alias. (Consulta la tabla
siguiente para la lista de alias disponibles)

Los elementos pueden tomar argumentos usando llaves («{}»), y los argumentos múltiples se
separan por comas dentro de las llaves. Los flags pueden añadirse o quitarse prefijándolos con
un signo «+» o «-» (consulta más abajo la lista de flags disponibles).

El alias especial «%o» puede usarse para propagar sus flags a todos los demás elementos de
logformat de la misma cadena de formato. Esto es particularmente práctico con los formatos de
cadena entrecomillados («Q») y escapados («E»).

El alias especial «%OG» puede usarse para recuperar el origen del registro (cuándo/dónde se
generó el registro) en un formato legible por humanos. Es particularmente útil con
«option logasap», porque algunas variables de registro o extracciones de muestra podrían
reportar valores incompletos o comportarse de forma diferente según cuándo/dónde se evaluó la
expresión de logformat. Los valores posibles son:

- «sess_error»: el registro se generó durante la gestión de un error de sesión
- «sess_killed»: el registro se generó durante el aborto de la sesión (sesión embrionaria
  eliminada)
- «txn_accept»: el registro se generó justo después de aceptar la conexión del frontend
- «txn_request»: el registro se generó después de recibir la petición del cliente
- «txn_connect»: el registro se generó tras el establecimiento de la conexión con el backend
- «txn_response»: el registro se generó durante la gestión de la respuesta del servidor
- «txn_close»: el registro se generó en el paso final de la txn, antes del cierre
- «unspec»: desconocido o no especificado «%OG» solo es relevante en contexto de registro.

Los elementos pueden opcionalmente nombrarse usando («()»). El nombre debe proporcionarse justo
después de «%» (antes de los argumentos). Se usará automáticamente como nombre de clave cuando
se establece un flag de codificación como «json» o «cbor». Cuando no se especifica ningún flag
de codificación (por defecto), el nombre del elemento se ignorará. También es posible forzar el
tipo de salida del elemento añadiendo «:type» después del nombre, así:
%(itemname:itemtype)aliasname o %(itemname:itemtype)[expr] donde itemtype puede ser «str»,
«sint» o «bool». Especificar el tipo solo es relevante cuando se usa un método de codificación.
También está soportado proporcionar un nombre vacío para forzar el tipo de salida en un
elemento anónimo: %(:itemtype), es decir: cuando la codificación no está globalmente
establecida; consulta las definiciones de flags más abajo para más información.

Debido al objetivo original de los formatos de registro personalizados, que era usarlos
únicamente para registrar, hay un caso especial para los caracteres no imprimibles e inseguros
(aquellos fuera de los códigos ASCII 32 a 126 más algunos otros) según dónde se usen. La
[sección 8.6](/es/haproxy/configuration-logging/#section-8-6) describe exactamente qué se hace con los registros para asegurarse de que
no se envíen códigos inseguros que alteren la legibilidad de la salida en un terminal. Cuando
se usan para formar campos de cabecera, comprobaciones de estado o respuestas de carga útil,
las reglas son menos estrictas y solo los caracteres prohibidos en los campos de cabecera HTTP
se sustituyen por su codificación hexadecimal precedida del carácter «%». Normalmente esto no
es un problema, pero puede afectar a la salida cuando se esperaba que el carácter se
reprodujera literalmente (p. ej., al construir una página de error o una carga útil de
respuesta completa, donde los saltos de línea podrían aparecer como «%0A»).

Nota: en las directivas de configuración «log-format», «log-format-sd» y «unique-id-format»,
los espacios se consideran delimitadores y se fusionan.

Nota: cuando se usa el formato de mensaje syslog RFC5424, los caracteres '"',
«&#92;» y «]» dentro de PARAM-VALUE deberían escaparse con
«&#92;» como prefijo (consulta <https://tools.ietf.org/html/rfc5424#section-6.3.3> para
más detalles). En tales casos, debería considerarse el uso del flag «E».

Los flags de elemento soportados son (pueden activarse/desactivarse desde los argumentos del
elemento):

- Q: entrecomillar una cadena
- X: representación hexadecimal (IPs, puertos, %Ts, %rt, %pid)
- E: escapar los caracteres '"', «&#92;» y «]» en una cadena con
  «&#92;» como prefijo (el propósito previsto son los formatos de registro estructurado
  RFC5424)
- bin: intentar preservar datos binarios; esto puede ser útil con expresiones de muestra que
  producen datos binarios para preservar los datos originales. Ten cuidado, sin embargo,
  porque evidentemente puede generar caracteres no imprimibles, incluido el byte NULL, que la
  mayoría de los extremos syslog no esperan. Así, está principalmente pensado para usarse con
  set-var-fmt, rings y extremos de registro con capacidad binaria. Esta opción solo puede
  establecerse globalmente (con %o); se ignorará si se establece en las opciones de un elemento
  individual.
- json: codificar automáticamente el valor en formato JSON (cuando se establece globalmente,
  solo se consideran los elementos de logformat nombrados). Los valores numéricos incompletos
  (p. ej.: «%B» cuando se usa logasap), que normalmente llevan el prefijo «+» sin codificar,
  se codificarán tal cual. Además, la opción «+E» se ignorará. Como se describe en la
  [sección 8.6](/es/haproxy/configuration-logging/#section-8-6), los caracteres fuera del rango 32..126 se escapan un byte a la vez,
  usando las secuencias de escape JSON, de modo que la salida siga siendo ASCII imprimible
  puro sea cual sea la entrada. Esto incluye las secuencias UTF-8 válidas, lo que significa que
  el texto no ASCII aparecerá como sus bytes individuales una vez decodificado (p. ej., U+00E9,
  codificado como 0xC3 0xA9, se registra como "&#92;u00C3&#92;u00A9"). Consulta «utf8» más abajo
  para preservar dicho texto.
- utf8: combinado con «json», permite que las secuencias UTF-8 multibyte válidas pasen sin
  escapar. Los caracteres de control C1 (U+0080 a U+009F) siguen escapándose, representados por
  su punto de código. Las secuencias inválidas se escapan un byte a la vez para que la salida
  siga siendo siempre UTF-8 válido. Ten en cuenta que, como el UTF-8 válido se emite tal cual,
  un cliente puede usar algunos caracteres especiales para alterar el renderizado de una línea
  de registro en un terminal o en un visor de registros, como cambios de dirección, caracteres
  de ancho cero o separadores de línea y párrafo. Por ello se recomienda usarlo solo para
  contenidos provenientes de fuentes de confianza, o cuando los registros no están destinados a
  mostrarse en un terminal. No tiene efecto sin «json».
- cbor: codificar automáticamente el valor en formato CBOR (cuando se establece globalmente,
  solo se consideran los elementos de logformat nombrados). Por defecto, los datos codificados
  en cbor se representan en forma HEX para que sigan siendo imprimibles por stdout y puedan
  usarse con los extremos syslog habituales. Igual que con la codificación json, los valores
  numéricos incompletos se codificarán tal cual y la opción «+E» se ignorará. Cuando se combina
  con la opción «+bin», generará directamente una carga útil CBOR binaria en bruto. Ten
  cuidado, porque evidentemente generará caracteres no imprimibles, por lo que está
  principalmente pensado para usarse con set-var-fmt, rings y extremos de registro con
  capacidad binaria.

Ejemplo:

```text
log-format %T\ %t\ Some\ Text
log-format %{+Q}o\ %t\ %s\ %{-Q}r

log-format-sd %{+Q,+E}o\ [exampleSDID@1234\ header=%[capture.req.hdr(0)]]

log-format "%{+json}o %(request)r %(custom_expr)[str(custom)]"
log-format "%{+json,+utf8}o %(request)r %(custom_expr)[str(custom)]"
log-format "%{+cbor}o %(request)r %(custom_expr)[str(custom)]"
```

Consulta la tabla siguiente para los alias definidos actualmente:

```text
  +---+------+------------------------------------------------------+---------+
  | R | alias| nombre del campo (descripción en 8.2.2 y 8.2.3)      | tipo    |
  |   |      | alternativa mediante sample fetch                    |         |
  +===+======+======================================================+=========+
  |   | %o   | especial: aplica flags a los elementos siguientes    |         |
  +---+------+------------------------------------------------------+---------+
  |                          formatos de fecha                                |
  +---+------+------------------------------------------------------+---------+
  |   | %T   | fecha de aceptación UTC + zona horaria               |         |
  |   |      | %[accept_date,utime("%d/%b/%Y:%H:%M:%S %z")]         | fecha   |
  +---+------+------------------------------------------------------+---------+
  |   | %Tl  | fecha de aceptación local + zona horaria             |         |
  |   |      | %[accept_date,ltime("%d/%b/%Y:%H:%M:%S %z")]         | fecha   |
  +---+------+------------------------------------------------------+---------+
  |   | %Ts  | fecha de aceptación como marca de tiempo UNIX        | numér.  |
  |   |      | %[accept_date]                                       |         |
  +---+------+------------------------------------------------------+---------+
  |   | %t   | fecha de aceptación local (resolución milisegundos)  |         |
  |   |      | %[accept_date(ms),ms_ltime("%d/%b/%Y:%H:%M:%S.%3N")] | fecha   |
  +---+------+------------------------------------------------------+---------+
  |   | %ms  | milisegundos de la fecha de aceptación               |         |
  |   |      | %[accept_date(ms),ms_utime("%3N")]                   | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %tr  | fecha local de la petición (resolución milisegundos) |         |
  |   |      | %[request_date(ms),ms_ltime("%d/%b/%Y:%H:%M:%S.%3N")]| fecha   |
  +---+------+------------------------------------------------------+---------+
  | H | %trg | fecha de petición UTC + zona horaria                 |         |
  |   |      | %[request_date,utime("%d/%b/%Y:%H:%M:%S %z")]        | fecha   |
  +---+------+------------------------------------------------------+---------+
  | H | %trl | fecha de petición local + zona horaria               |         |
  |   |      | %[request_date,ltime("%d/%b/%Y:%H:%M:%S %z")]        | fecha   |
  +---+------+------------------------------------------------------+---------+
  |                          Eventos de temporización                         |
  +---+------+------------------------------------------------------+---------+
  | H | %Ta  | tiempo activo de la petición (de TR al final)        |         |
  |   |      | %[txn.timer.total]                                   | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Tc  | Tc                                                   |         |
  |   |      | %[bc.timer.connect]                                  | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Td  | Td = Tt - (Tq + Tw + Tc + Tr)                        |         |
  |   |      | %[res.timer.data]                                    | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Th  | tiempo de handshake de la conexión (SSL, proto PROXY)|         |
  |   |      | %[fc.timer.handshake]                                | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %Ti  | tiempo de inactividad antes de la petición HTTP      |         |
  |   |      | %[req.timer.idle]                                    | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %Tq  | Th + Ti + TR                                         |         |
  |   |      | %[req.timer.tq]                                      | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %TR  | tiempo en recibir toda la petición desde el 1er byte |         |
  |   |      | %[req.timer.hdr]                                     | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %Tr  | Tr (tiempo de respuesta)                             |         |
  |   |      | %[res.timer.hdr]                                     | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Tt  | Tt                                                   |         |
  |   |      | %[fc.timer.total]                                    | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Tu  | Tu                                                   |         |
  |   |      | %[txn.timer.user]                                    | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %Tw  | Tw                                                   |         |
  |   |      | %[req.timer.queue]                                   | numér.  |
  +---+------+------------------------------------------------------+---------+
  |                          Otros                                            |
  +---+------+------------------------------------------------------+---------+
  |   | %B   | bytes_read           (del servidor al cliente)       | numér.  |
  |   |      | %[res.bytes_in]                                      |         |
  +---+------+------------------------------------------------------+---------+
  | H | %CC  | captured_request_cookie                              | cadena  |
  +---+------+------------------------------------------------------+---------+
  | H | %CS  | captured_response_cookie                             | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %H   | hostname                                             | cadena  |
  |   |      | %[hostname]                                          |         |
  +---+------+------------------------------------------------------+---------+
  | H | %HM  | método HTTP (ej: POST)                               | cadena  |
  |   |      | %[method]
  +---+------+------------------------------------------------------+---------+
  | H | %HP  | URI de petición HTTP sin cadena de consulta          | cadena  |
  +---+------+------------------------------------------------------+---------+
  | H | %HPO | path HTTP solamente (sin host ni cadena de consulta) | cadena  |
  +---+------+------------------------------------------------------+---------+
  | H | %HQ  | cadena de consulta de la URI HTTP (ej: ?bar=baz)     | cadena  |
  |   |      | ?%[query]                                            |         |
  +---+------+------------------------------------------------------+---------+
  | H | %HU  | URI de petición HTTP (ej: /foo?bar=baz)              | cadena  |
  +---+------+------------------------------------------------------+---------+
  | H | %HV  | versión HTTP (ej: HTTP/1.0)                          | cadena  |
  |   |      | HTTP/%[req.ver]                                      |         |
  +---+------+------------------------------------------------------+---------+
  |   | %ID  | unique-id                                            | cadena  |
  |   |      | %[unique-id]                                         |         |
  +---+------+------------------------------------------------------+---------+
  |   | %ST  | status_code                                          | numér.  |
  |   |      | %[txn.status]                                        |         |
  +---+------+------------------------------------------------------+---------+
  |   | %U   | bytes_uploaded       (del cliente al servidor)       | numér.  |
  |   |      | %[req.bytes_in]                                      |         |
  +---+------+------------------------------------------------------+---------+
  |   | %ac  | actconn                                              |         |
  |   |      | %[act_conn]                                          | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %b   | backend_name                                         |         |
  |   |      | %[be_name]                                           | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %bc  | beconn      (conexiones concurrentes del backend)    | numér.  |
  |   |      | %[be_conn]                                           |         |
  +---+------+------------------------------------------------------+---------+
  |   | %bi  | backend_source_ip       (dirección de conexión)      |         |
  |   |      | %[bc_src]                                            | IP      |
  +---+------+------------------------------------------------------+---------+
  |   | %bp  | backend_source_port     (dirección de conexión)      |         |
  |   |      | %[bc_src_port]                                       | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %bq  | backend_queue                                        | numér.  |
  |   |      | %[bc_be_queue]                                       |         |
  +---+------+------------------------------------------------------+---------+
  |   | %ci  | client_ip                 (dirección de aceptación)  |         |
  |   |      | %[src]                                               | IP      |
  +---+------+------------------------------------------------------+---------+
  |   | %cp  | client_port               (dirección de aceptación)  |         |
  |   |      | %[src_port]                                          | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %f   | frontend_name                                        | cadena  |
  |   |      | %[fe_name]                                           |         |
  +---+------+------------------------------------------------------+---------+
  |   | %fc  | feconn     (conexiones concurrentes del frontend)    | numér.  |
  |   |      | %[fe_conn]                                           |         |
  +---+------+------------------------------------------------------+---------+
  |   | %fi  | frontend_ip              (dirección de aceptación)   |         |
  |   |      | %[dst]                                               | IP      |
  +---+------+------------------------------------------------------+---------+
  |   | %fp  | frontend_port            (dirección de aceptación)   |         |
  |   |      | %[dst_port]                                          | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %ft  | frontend_name_transport (sufijo '~' para SSL)        | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %lc  | frontend_log_counter                                 | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %hr  | captured_request_headers estilo por defecto          | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %hrl | captured_request_headers estilo CLF                  | cadena  |
  |   |      |                                                      | lista   |
  +---+------+------------------------------------------------------+---------+
  |   | %hs  | captured_response_headers estilo por defecto         | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %hsl | captured_response_headers estilo CLF                 | cadena  |
  |   |      |                                                      | lista   |
  +---+------+------------------------------------------------------+---------+
  | L | %OG  | origen del registro legible por humanos              | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %pid | PID                                                  |         |
  |   |      | %[pid]                                               | numér.  |
  +---+------+------------------------------------------------------+---------+
  | H | %r   | http_request                                         | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %rc  | retries                                              | numér.  |
  |   |      | %[txn.redispatched,iif(+,)]%[txn.conn_retries]       |         |
  +---+------+------------------------------------------------------+---------+
  |   | %rt  | request_counter (petición HTTP o sesión TCP)         | numér.  |
  |   |      | %[txn.id32]                                          |         |
  +---+------+------------------------------------------------------+---------+
  |   | %s   | server_name                                          | cadena  |
  |   |      | %[srv_name]                                          |         |
  +---+------+------------------------------------------------------+---------+
  |   | %sc  | srv_conn     (conexiones concurrentes del servidor)  | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %si  | server_IP                   (dirección de destino)   |         |
  |   |      | %[bc_dst]                                            | IP      |
  +---+------+------------------------------------------------------+---------+
  |   | %sp  | server_port                 (dirección de destino)   |         |
  |   |      | %[bc_dst_port]                                       | numér.  |
  +---+------+------------------------------------------------------+---------+
  |   | %sq  | srv_queue                                            | numér.  |
  |   |      | %[bc_srv_queue]                                      |         |
  +---+------+------------------------------------------------------+---------+
  | S | %sslc| ssl_ciphers (ej: AES-SHA)                            |         |
  |   |      | %[ssl_fc_cipher]                                     | cadena  |
  +---+------+------------------------------------------------------+---------+
  | S | %sslv| ssl_version (ej: TLSv1)                              |         |
  |   |      | %[ssl_fc_protocol]                                   | cadena  |
  +---+------+------------------------------------------------------+---------+
  |   | %ts  | termination_state                                    | cadena  |
  |   |      | %[txn.sess_term_state]                               |         |
  +---+------+------------------------------------------------------+---------+
  | H | %tsc | termination_state con estado del cookie              | cadena  |
  +---+------+------------------------------------------------------+---------+
```

    R = Restricciones: H = solo modo http; S = solo SSL; L = solo registro

## 8.3. Opciones avanzadas de registro {#section-8-3}

A menudo se buscan algunas opciones avanzadas de registro, pero no es fácil descubrirlas con
solo mirar las distintas opciones. Aquí hay un punto de entrada para las pocas opciones que
pueden habilitar un mejor registro. Consulta la referencia de palabras clave para más
información sobre su uso.

### 8.3.1. Desactivación del registro de pruebas externas {#section-8-3-1}

Es bastante común que algunas herramientas de monitorización realicen comprobaciones de estado
sobre HAProxy. A veces será un balanceador de carga de capa 3 como LVS o cualquier balanceador
comercial, y a veces será simplemente un sistema de monitorización más completo como Nagios.
Cuando las pruebas son muy frecuentes, los usuarios suelen preguntar cómo desactivar el
registro de esas comprobaciones. Hay tres posibilidades:

- si las conexiones vienen de todas partes y son solo sondeos TCP, a menudo se desea
  simplemente desactivar el registro de conexiones sin intercambio de datos, estableciendo
  «option dontlognull» en el frontend. Esto también desactiva el registro de escaneos de
  puertos, lo que puede o no desearse.

- es posible usar la acción «http-request set-log-level silent» con una variedad de condiciones
  (redes de origen, rutas, user-agents, etc).

- si las pruebas se realizan sobre un URI conocido, usa «monitor-uri» para declarar ese URI como
  dedicado a la monitorización. Cualquier host que envíe esta petición solo obtendrá el
  resultado de una comprobación de estado, y la petición no se registrará.

### 8.3.2. Registro antes de esperar la terminación del flujo {#section-8-3-2}

El problema de registrar al final de la conexión es que no tienes ni idea de lo que está
ocurriendo durante flujos muy largos, como sesiones de terminal remoto o descargas de archivos
grandes. Este problema puede sortearse especificando «option logasap» en el frontend. HAProxy
registrará entonces lo antes posible, justo antes de que comience la transferencia de datos.
Esto significa que en el caso de TCP seguirá registrando el estado de la conexión al servidor,
y en el caso de HTTP registrará justo después de procesar las cabeceras del servidor. En este
caso, el número de bytes reportado es el número de bytes de cabecera enviados al cliente. Para
evitar la confusión con los registros normales, el campo de tiempo total y el número de bytes
llevan el prefijo de un signo «+», lo que significa que los números reales son ciertamente
mayores.

### 8.3.3. Elevar el nivel de registro ante errores {#section-8-3-3}

A veces es más cómodo separar el tráfico normal de los registros de errores, por ejemplo para
facilitar la monitorización de errores desde los archivos de registro. Cuando se usa la opción
«log-separate-errors», las conexiones que experimentan errores, tiempos de espera agotados,
reintentos, reasignaciones o códigos de estado HTTP 5xx verán su nivel syslog elevado de
«info» a «err». Esto ayudará a un demonio syslog a almacenar el registro en un archivo
separado. Es muy importante conservar también los errores en el archivo de tráfico normal,
para que el orden de los registros no se altere. También deberías tener cuidado si ya has
configurado tu demonio syslog para almacenar todos los registros superiores a «notice» en un
archivo «admin», porque el nivel «err» es superior a «notice».

### 8.3.4. Desactivación del registro de conexiones satisfactorias {#section-8-3-4}

Aunque puede sonar extraño al principio, algunos sitios grandes tienen que lidiar con varios
miles de registros por segundo y tienen dificultades para conservarlos intactos durante mucho
tiempo o para detectar errores en ellos. Si la opción «dontlog-normal» está establecida en el
frontend, todas las conexiones normales no se registrarán. A este respecto, una conexión normal
se define como una sin ningún error, tiempo de espera agotado, reintento ni reasignación. En
HTTP, el código de estado también se comprueba, y una respuesta con un estado 5xx no se
considera normal y también se registrará. Por supuesto, hacer esto está realmente
desaconsejado, ya que eliminará la mayor parte de la información útil de los registros.
Hazlo solo si no tienes otra alternativa.

### 8.3.5. Perfiles de registro {#section-8-3-5}

Si bien algunas directivas como «log-format», «log-format-sd», «error-log-format» o «log-tag»
permiten configurar el formato de registro globalmente o a nivel de proxy, puede ser relevante
configurar tales ajustes lo más cerca posible de los extremos de registro, es decir, por
directiva «log».

Aquí es donde entra en juego la sección «log-profile»: «log-profile» puede definirse en
cualquier parte de la configuración. Esta sección acepta un conjunto de palabras clave
diferentes que se usan para describir cómo deben construirse los registros emitidos para una
directiva `log` dada.

Desde una directiva «log», puede elegirse usar un log-profile específico por su nombre. El
mismo perfil puede usarse desde múltiples directivas «log».

log-profile `<name>` Crea un nuevo perfil de registro identificado como `<name>`

log-tag `<string>` Sobrescribe la etiqueta de registro syslog establecida globalmente o por
proxy mediante la directiva «log-tag».

on `<step>` [drop] [format `<fmt>`] [sd `<sd_fmt>`] Sobrescribe la cadena log-format usada
normalmente para construir la línea de registro en el paso de registro `<step>`. `<fmt>` se
usa para sobrescribir las cadenas «log-format» o «error-log-format» (dependiendo del
`<step>`), mientras que `<sd_fmt>` se usa para sobrescribir la cadena «log-format-sd» (ambas
pueden combinarse).

La palabra clave especial «drop» puede usarse para especificar que no debe emitirse ningún
registro para el `<step>` dado. Tiene precedencia sobre «format» y «sd» si se definieron
previamente.

Los valores posibles para `<step>` son:

- «accept» : sobrescribe log-format si el registro se genera justo después de aceptar la
  conexión del frontend
- «request» : sobrescribe log-format si el registro se genera después de recibir la petición
  del cliente
- «connect» : sobrescribe log-format si el registro se genera tras el establecimiento de la
  conexión con el backend
- «response»: sobrescribe log-format si el registro se genera durante la gestión de la
  respuesta del servidor
- «close» : sobrescribe log-format si el registro se genera en el paso final de la transacción
  (txn)
- «error» : sobrescribe error-log-format si el registro se genera debido a un error de
  transacción
- «any» : sobrescribe tanto log-format como error-log-format para todos los pasos de registro,
  salvo que se declare una sobrescritura de paso más precisa.

Consulta la acción «do-log» para valores `<step>` adicionales relevantes.

Este ajuste solo es relevante para directivas «log» usadas desde contextos donde usar la
directiva «log-format» tiene sentido (p. ej.: proxies http y tcp). Si no, simplemente se
ignorará.

Ejemplo:

```text
log-profile myprof

  log-tag "custom-tag"

  on error format "%ci: error"
  on connect drop
  on any sd "custom-sd"

listen myproxy
  mode http
  option httplog
  log-tag "normal"

  log stdout format rfc5424 local0
  # success:
  # <134>1 2024-06-12T10:09:11.823400+02:00 - normal 224482 - - 127.0.0.1:53594 [12/Jun/2024:10:09:11.814] myproxy myproxy/<NOSRV> 0/-1/-1/-1/0 200 49 - - LR-- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
  #
  # error:
  # <134>1 2024-06-12T10:09:44.810929+02:00 - normal 224482 - - 127.0.0.1:59258 [12/Jun/2024:10:09:44.426] myproxy myproxy/<NOSRV> -1/-1/-1/-1/384 400 0 - - CR-- 1/1/0/0/0 0/0 "<BADREQ>"

  log 127.0.0.1:514 format rfc5424 profile myprof local0
  # success:
  # <134>1 2024-06-12T10:09:11.823428+02:00 - custom-tag 224482 - custom-sd 127.0.0.1:53594 [12/Jun/2024:10:09:11.814] myproxy myproxy/<NOSRV> 0/-1/-1/-1/0 200 49 - - LR-- 1/1/0/0/0 0/0 "GET / HTTP/1.1"
  #
  # error:
  # <134>1 2024-06-12T10:09:51.566524+02:00 - custom-tag 224482 - - 127.0.0.1: error
```

## 8.4. Eventos de temporización {#section-8-4}

Los temporizadores son de gran ayuda para resolver problemas de red. Todos los valores se
reportan en milisegundos (ms). Estos temporizadores deberían usarse junto con los indicadores
de terminación del flujo. En modo TCP con «option tcplog» establecido en el frontend, se
reportan 3 puntos de control bajo la forma «Tw/Tc/Tt», y en modo HTTP se reportan 5 puntos de
control bajo la forma «TR/Tw/Tc/Tr/Ta». Además, se proporcionan otras tres medidas: «Th», «Ti»
y «Tq».

Eventos de temporización en modo HTTP:

```text
               primera solicitud             2.ª solicitud
      |<-------------------------------->|<-------------- ...
      t         tr                       t    tr ...
   ---|----|----|----|----|----|----|----|----|--
     : Th   Ti   TR   Tw   Tc   Tr   Td: Ti   ...
     :<---- Tq ---->:                  :
     :<-------------- Tt -------------->:
     :<--        -----Tu--------------->:
               :<--------- Ta --------->:
```

Eventos de temporización en modo TCP:

```text
           sesión TCP
      |<----------------->|
      t                   t
   ---|----|----|----|----|---
      | Th   Tw   Tc   Td |
      |<------ Tt ------->|
```

- Th: tiempo total para aceptar la conexión tcp y ejecutar los handshakes de los protocolos de
  bajo nivel. Actualmente, estos protocolos son proxy-protocol y SSL. Esto solo puede ocurrir
  una vez durante toda la vida de la conexión. Un tiempo grande aquí puede indicar que el
  cliente solo pre-estableció la conexión sin hablar, que sufre problemas de red que le impiden
  completar un handshake en un tiempo razonable (p. ej., problemas de MTU), o que un handshake
  SSL fue muy costoso de calcular. Ten en cuenta que este tiempo se reporta solo antes de la
  primera petición, así que es seguro promediarlo sobre todas las peticiones para calcular el
  valor amortizado. La segunda petición y las siguientes siempre reportarán cero aquí.

  Este temporizador se llama %Th como alias de log-format, y fc.timer.handshake como
  extracción de muestra.

- Ti: es el tiempo de inactividad antes de la petición HTTP (solo modo HTTP). Este temporizador
  cuenta entre el final de los handshakes y el primer byte de la petición HTTP. Cuando se
  trata de una segunda petición en modo keep-alive, empieza a contar después del final de la
  transmisión de la respuesta anterior. Cuando se usa un protocolo multiplexado como HTTP/2,
  empieza a contar inmediatamente después de la petición anterior. Algunos navegadores
  pre-establecen conexiones a un servidor para reducir la latencia de una petición futura, y
  las mantienen pendientes hasta que las necesitan. Este retraso se reportará como el tiempo de
  inactividad. Un valor de -1 indica que no se recibió nada en la conexión.

  Este temporizador se llama %Ti como alias de log-format, y req.timer.idle como extracción de
  muestra.

- TR: tiempo total para recibir la petición del cliente (solo modo HTTP). Es el tiempo
  transcurrido entre los primeros bytes recibidos y el momento en que el proxy recibió la línea
  vacía que marca el final de las cabeceras HTTP. El valor «-1» indica que nunca se vio el final
  de las cabeceras. Esto ocurre cuando el cliente cierra prematuramente o se le agota el tiempo
  de espera. Este tiempo suele ser muy corto, dado que la mayoría de las peticiones caben en un
  solo paquete. Un tiempo grande puede indicar una petición tecleada a mano durante una prueba.

  Este temporizador se llama %TR como alias de log-format, y req.timer.hdr como extracción de
  muestra.

- Tq: tiempo total para recibir la petición del cliente desde la fecha de aceptación o desde la
  emisión del último byte de la respuesta anterior (solo modo HTTP). Es exactamente igual a
  Th + Ti + TR salvo que alguno de ellos sea -1, en cuyo caso también devuelve -1. Este
  temporizador solía ser muy útil antes de la llegada del keep-alive HTTP y de la función de
  preconexión de los navegadores. Hoy en día se recomienda descartarlo en favor de TR, ya que
  el tiempo de inactividad añade mucho ruido a los informes.

  Este temporizador se llama %Tq como alias de log-format, y req.timer.tq como extracción de
  muestra.

- Tw: tiempo total pasado en las colas esperando un hueco de conexión. Incluye tanto la cola
  del backend como las colas de los servidores, y depende del tamaño de la cola y del tiempo
  que el servidor necesita para completar las peticiones anteriores. El valor «-1» significa
  que la petición fue eliminada antes de alcanzar la cola, que generalmente es lo que ocurre
  con peticiones inválidas o denegadas.

  Este temporizador se llama %Tw como alias de log-format, y req.timer.queue como extracción
  de muestra.

- Tc: tiempo total para establecer la conexión TCP con el servidor. Es el tiempo transcurrido
  entre el momento en que el proxy envió la petición de conexión y el momento en que fue
  reconocida por el servidor, o entre el paquete TCP SYN y el paquete SYN/ACK correspondiente
  de vuelta. El valor «-1» significa que la conexión nunca se estableció.

  Este temporizador se llama %Tc como alias de log-format, y bc.timer.connect como extracción
  de muestra.

- Tr: tiempo de respuesta del servidor (solo modo HTTP). Es el tiempo transcurrido entre el
  momento en que se estableció la conexión TCP con el servidor y el momento en que el servidor
  envió sus cabeceras de respuesta completas. Muestra puramente su tiempo de procesamiento de
  la petición, sin la sobrecarga de red debida a la transmisión de los datos. Conviene señalar
  que cuando el cliente tiene datos que enviar al servidor, por ejemplo durante una petición
  POST, el tiempo ya corre, y esto puede distorsionar el tiempo de respuesta aparente. Por esta
  razón, en general es prudente no confiar demasiado en este campo para peticiones POST
  iniciadas por clientes detrás de una red no confiable. Un valor de «-1» aquí significa que
  nunca se vio la última cabecera de respuesta (línea vacía), muy probablemente porque el
  tiempo de espera del servidor se agotó antes de que el servidor lograra procesar la petición
  o porque el servidor devolvió una respuesta inválida.

  Este temporizador se llama %Tr como alias de log-format, y res.timer.hdr como extracción de
  muestra.

- Td: este es el tiempo total de transferencia de la carga útil de la respuesta hasta el último
  byte enviado al cliente. En HTTP empieza después de la última cabecera de respuesta
  (después de Tr).

  Los datos enviados no tienen garantizada su recepción por el cliente; pueden quedar atascados
  tanto en el núcleo como en la red.

  Este temporizador se llama %Td como alias de log-format, y res.timer.data como extracción de
  muestra.

- Ta: tiempo activo total de la petición HTTP, entre el momento en que el proxy recibió el
  primer byte de la cabecera de la petición y la emisión del último byte del cuerpo de la
  respuesta. La excepción es cuando se especifica la opción «logasap». En este caso, solo es
  igual a (TR+Tw+Tc+Tr), y lleva el prefijo de un signo «+». A partir de este campo podemos
  deducir «Td», el tiempo de transmisión de datos, restando otros temporizadores cuando sean
  válidos:

```text
Td = Ta - (TR + Tw + Tc + Tr)
```

    Los temporizadores con valor «-1» deben excluirse de esta ecuación.
    Ten en cuenta que «Ta» nunca puede ser negativo.

    Este temporizador se llama %Ta como alias de log-format, y
    txn.timer.total como extracción de muestra.

- Tt: duración total del flujo, entre el momento en que el proxy lo aceptó y el momento en que
  ambos extremos se cerraron. La excepción es cuando se especifica la opción «logasap». En este
  caso, solo es igual a (Th+Ti+TR+Tw+Tc+Tr), y lleva el prefijo de un signo «+». A partir de
  este campo podemos deducir «Td», el tiempo de transmisión de datos, restando otros
  temporizadores cuando sean válidos:

```text
Td = Tt - (Th + Ti + TR + Tw + Tc + Tr)
```

    Los temporizadores con valor «-1» deben excluirse de esta ecuación. En
    modo TCP, «Ti», «Tq» y «Tr» también deben excluirse. Ten en cuenta que
    «Tt» nunca puede ser negativo y que para HTTP, Tt es simplemente igual a
    (Th+Ti+Ta).

    Este temporizador se llama %Tt como alias de log-format, y
    fc.timer.total como extracción de muestra.

- Tu: tiempo total estimado visto desde el cliente, entre el momento en que el proxy lo aceptó
  y el momento en que ambos extremos se cerraron, sin el tiempo de inactividad. Esto es útil
  para medir aproximadamente el tiempo extremo a extremo tal como lo vería un usuario, sin la
  contaminación del tiempo de inactividad del keep-alive entre peticiones. Este temporizador es
  solo una estimación del tiempo visto por el usuario, ya que asume que la latencia de red es
  la misma en ambas direcciones. La excepción es cuando se especifica la opción «logasap». En
  este caso, solo es igual a (Th+TR+Tw+Tc+Tr), y lleva el prefijo de un signo «+».

  Este temporizador se llama %Tu como alias de log-format, y txn.timer.user como extracción de
  muestra.

Estos temporizadores proporcionan indicaciones valiosas sobre las causas de los problemas.
Como el protocolo TCP define retrasos de retransmisión de 3, 6, 12... segundos, sabemos con
certeza que los temporizadores cercanos a múltiplos de 3s se deben casi siempre a paquetes
perdidos por problemas de red (cables, negociación, congestión). Además, si «Ta» o «Tt» está
cerca de un valor de tiempo de espera especificado en la configuración, a menudo significa que
un flujo ha sido abortado por tiempo de espera agotado.

Casos más comunes:

- Si «Th» o «Ti» están cerca de 3000, probablemente se perdió un paquete entre el cliente y el
  proxy. Esto es muy raro en redes locales, pero puede ocurrir cuando los clientes están en
  redes muy remotas y envían peticiones grandes. Puede ocurrir que aparezcan aquí valores
  mayores de lo habitual sin ninguna causa de red. A veces, durante un ataque o justo después
  de que termine un agotamiento de recursos, HAProxy puede aceptar miles de conexiones en unos
  pocos milisegundos. El tiempo empleado en aceptar estas conexiones retrasará inevitablemente
  un poco el procesamiento de otras conexiones, y puede ocurrir que se midan tiempos de
  petición del orden de unas decenas de milisegundos después de que se hayan aceptado de golpe
  unos pocos miles de conexiones nuevas. Usar uno de los modos keep-alive puede mostrar
  tiempos de inactividad mayores, ya que «Ti» mide el tiempo pasado esperando peticiones
  adicionales.

- Si «Tc» está cerca de 3000, probablemente se perdió un paquete entre el servidor y el proxy
  durante la fase de conexión al servidor. Este valor debería ser siempre muy bajo, como 1 ms
  en redes locales y menos que unas decenas de ms en redes remotas.

- Si «Tr» es casi siempre menor que 3000 salvo algunos valores raros que parecen ser la media
  aumentada en 3000, probablemente se pierden algunos paquetes entre el proxy y el servidor.

- Si «Ta» es grande incluso con conteos de bytes pequeños, generalmente es porque ni el
  cliente ni el servidor deciden cerrar la conexión mientras HAProxy se ejecuta en modo túnel
  y ambos han acordado un modo de conexión keep-alive. Para resolver este problema, hará falta
  especificar una de las opciones HTTP para manipular las opciones keep-alive o close en el
  frontend o en el backend. Tener el menor «Ta» o «Tt» posible es importante cuando se usa
  regulación de conexiones con la opción «maxconn» en los servidores, ya que no se enviará
  ninguna conexión nueva al servidor hasta que se libere otra.

Otros casos de registro HTTP destacables («xx» significa cualquier valor a ignorar):

```text
TR/Tw/Tc/Tr/+Ta  La «option logasap» está presente en el frontend y el
                 registro se emitió antes de la fase de datos. Todos los
                 temporizadores son válidos excepto «Ta», que es menor que
                 la realidad.

-1/xx/xx/xx/Ta   El cliente no pudo enviar una petición completa a tiempo o
                 la abortó demasiado pronto. Comprueba los indicadores de
                 terminación del flujo y luego los ajustes
                 «timeout http-request» y «timeout client».

TR/-1/xx/xx/Ta   No fue posible procesar la petición, quizá porque los
                 servidores no funcionaban, porque la petición era inválida
                 o estaba prohibida por reglas ACL. Comprueba los
                 indicadores de terminación del flujo.

TR/Tw/-1/xx/Ta   No se pudo establecer la conexión con el servidor. Este la
                 rechazó activamente o agotó el tiempo de espera tras
                 Ta-(TR+Tw) ms. Comprueba los indicadores de terminación del
                 flujo y luego el ajuste «timeout connect». Ten en cuenta
                 que la acción tarpit puede devolver patrones de aspecto
                 similar, con «Tw» igual al tiempo que se mantuvo abierta la
                 conexión del cliente.

TR/Tw/Tc/-1/Ta   El servidor aceptó la conexión pero no devolvió una
                 respuesta completa a tiempo, o cerró su conexión de forma
                 inesperada tras Ta-(TR+Tw+Tc) ms. Comprueba los indicadores
                 de terminación del flujo y luego el ajuste «timeout server».
```

## 8.5. Estado del flujo en la desconexión {#section-8-5}

Los registros TCP y HTTP proporcionan un indicador de terminación del flujo en el campo
«termination_state», justo antes del número de conexiones activas. Tiene 2 caracteres de
longitud en modo TCP, y se extiende a 4 caracteres en modo HTTP, cada uno de los cuales tiene un
significado especial:

- En el primer carácter, un código que reporta el primer evento que causó la terminación del
  flujo:

```text
C: la sesión TCP fue abortada inesperadamente por el cliente.

S: la sesión TCP fue abortada inesperadamente por el servidor, o el
    servidor la rechazó explícitamente.

P: el flujo o la sesión fue abortado prematuramente por el proxy, porque
    se aplicó un límite de conexiones, porque coincidió un filtro DENY,
    o porque una comprobación de seguridad detectó y bloqueó un error
    peligroso en la respuesta del servidor que podría haber causado una
    fuga de información (p. ej., una cookie almacenable en caché).

L: el flujo fue procesado localmente por HAProxy.

R: se agotó un recurso del proxy (memoria, sockets, puertos de origen,
    ...). Normalmente esto aparece durante la fase de conexión, y los
    registros del sistema deberían contener una copia del error preciso.
    Si esto ocurre, debe considerarse una anomalía muy grave que debe
    corregirse cuanto antes por cualquier medio.

I: el proxy identificó un error interno durante una autocomprobación.
    Esto NUNCA debería ocurrir, y te animamos a reportar cualquier
    registro que lo contenga, porque casi con certeza sería un bug.
    También sería prudente reiniciar preventivamente el proceso tras
    un evento así, por si estuviera causado por corrupción de memoria.

D: el flujo fue terminado por HAProxy porque el servidor se detectó
    como caído y estaba configurado para matar todas las conexiones
    al caer.

U: el flujo fue terminado por HAProxy en este servidor de respaldo
    porque un servidor activo se detectó como levantado y estaba
    configurado para matar todas las conexiones de respaldo al
    levantarse.

K: el flujo fue terminado activamente por un administrador que opera
    HAProxy.

c: el tiempo de espera del lado del cliente expiró mientras esperaba
    a que el cliente enviara o recibiera datos.

s: el tiempo de espera del lado del servidor expiró mientras esperaba
    a que el servidor enviara o recibiera datos.

-: terminación normal del flujo; tanto el cliente como el servidor
    cerraron sin quedar nada en los búferes.
```

- en el segundo carácter, el estado del flujo TCP o HTTP cuando se cerró:

```text
R: el proxy estaba esperando una PETICIÓN completa y válida del cliente
    (solo en modo HTTP). No se envió nada a ningún servidor.

Q: el proxy estaba esperando en la COLA un hueco de conexión. Esto solo
    puede ocurrir cuando los servidores tienen un parámetro «maxconn»
    establecido. También puede ocurrir en la cola global tras un
    redispatch consecutivo a un intento fallido de conexión a un
    servidor que estaba muriendo. Si no se reporta ningún redispatch,
    entonces no se hizo ningún intento de conexión a ningún servidor.

C: el proxy estaba esperando que la CONEXIÓN se estableciera con el
    servidor. El servidor, como mucho, pudo notar un intento de
    conexión.

H: el proxy estaba esperando CABECERAS de respuesta completas y válidas
    del servidor (solo HTTP).

D: el flujo estaba en la fase de DATOS.

L: el proxy todavía estaba transmitiendo los ÚLTIMOS datos al cliente
    cuando el servidor ya había terminado. Este caso es muy raro, pues
    solo puede ocurrir cuando el cliente muere mientras recibe los
    últimos paquetes.

T: la petición fue puesta en tarpit. Se mantuvo abierta con el cliente
    durante toda la duración de «timeout tarpit» o hasta que el cliente
    cerró; ambos casos se reportarán en el temporizador «Tw».

-: terminación normal del flujo tras el fin de la transferencia de datos.
```

- el tercer carácter indica si el cliente proporcionó la cookie de persistencia (solo en modo
  HTTP):

```text
N: el cliente NO proporcionó ninguna cookie. Suele ser el caso de los
    visitantes nuevos, así que contar el número de ocurrencias de este
    indicador en los registros generalmente refleja una tendencia válida
    de frecuencia de visita del sitio.

I: el cliente proporcionó una cookie INVÁLIDA que no corresponde a
    ningún servidor conocido. Esto podría deberse a un cambio reciente
    de configuración, cookies mezcladas entre sitios HTTP/HTTPS,
    persistencia ignorada condicionalmente, o un ataque.

D: el cliente proporcionó una cookie que designaba un servidor CAÍDO;
    entonces, o bien se usó «option persist» y el cliente fue enviado a
    ese servidor, o bien no estaba establecida y el cliente fue
    reenviado a otro servidor.

V: el cliente proporcionó una cookie VÁLIDA y fue enviado al servidor
    asociado.

E: el cliente proporcionó una cookie válida, pero con una última fecha
    más antigua de lo permitido por el parámetro de cookie «maxidle»,
    así que la cookie se considera EXPIRADA y se ignora. La petición se
    reenviará tal y como si no hubiera cookie.

O: el cliente proporcionó una cookie válida, pero con una primera fecha
    más antigua de lo permitido por el parámetro de cookie «maxlife»,
    así que la cookie se considera demasiado ANTIGUA y se ignora. La
    petición se reenviará tal y como si no hubiera cookie.

U: había una cookie presente pero no se usó para seleccionar el
    servidor porque en su lugar se usó algún otro mecanismo de selección
    de servidor (típicamente una regla «use-server»).

-: no aplica (ninguna cookie establecida en la configuración).
```

- el último carácter reporta qué operaciones se realizaron sobre la cookie de persistencia
  devuelta por el servidor (solo en modo HTTP):

```text
N: el servidor NO proporcionó ninguna cookie, y tampoco se insertó
    ninguna.

I: el servidor no proporcionó ninguna cookie, y el proxy INSERTÓ una.
    Ten en cuenta que en modo «cookie insert», si el servidor
    proporciona una cookie, esta se sobrescribirá igualmente y se
    reportará aquí como «I».

U: el proxy ACTUALIZÓ la última fecha en la cookie presentada por el
    cliente. Esto solo puede ocurrir en modo insert con «maxidle».
    Ocurre cada vez que hay actividad en una fecha distinta de la fecha
    indicada en la cookie. Si ocurre cualquier otro cambio, como un
    redispatch, la cookie se marcará como insertada en su lugar.

P: el servidor PROVEYÓ una cookie y se transmitió tal cual.

R: la cookie proporcionada por el servidor fue REESCRITA por el proxy,
    lo que ocurre en los modos «cookie rewrite» o «cookie prefix».

D: la cookie proporcionada por el servidor fue ELIMINADA por el proxy.

-: no aplica (ninguna cookie establecida en la configuración).
```

La combinación de los dos primeros indicadores da mucha información sobre lo que estaba
ocurriendo cuando el flujo o la sesión terminó, y por qué terminó. Puede ser útil para detectar
saturación de servidores, problemas de red, agotamiento de recursos del sistema local,
ataques, etc...

Las combinaciones de indicadores de terminación más comunes se indican a continuación. Están
ordenadas alfabéticamente, con el conjunto en minúsculas justo después del de mayúsculas para
facilitar su búsqueda y comprensión.

Indicadores Motivo

     --   Terminación normal.

     CC   El cliente abortó antes de que la conexión pudiera establecerse con el
          servidor. Esto puede ocurrir cuando HAProxy intenta conectarse a un
          servidor muerto recientemente (o no verificado), y el cliente aborta
          mientras HAProxy espera la respuesta del servidor o la expiración de
          «timeout connect».

     CD   El cliente abortó inesperadamente durante la transferencia de datos.
          Esto puede deberse a un fallo del navegador, a un equipo intermedio
          entre el cliente y HAProxy que decidió romper activamente la
          conexión, a problemas de enrutado de red entre el cliente y HAProxy,
          o a un flujo keep-alive entre el servidor y el cliente terminado
          primero por el cliente.

     cD   El cliente no envió ni reconoció ningún dato durante el plazo definido por
          «timeout client». Esto suele deberse a fallos de red en el lado del
          cliente, o a que el cliente simplemente abandona la red de forma
          abrupta.

     CH   El cliente abortó mientras esperaba a que el servidor empezara a
          responder. Puede ser que el servidor tarde demasiado en responder o
          que el cliente pulse el botón «Detener» demasiado rápido.

     cH   El «timeout client» se disparó mientras se esperaban datos del
          cliente durante una petición POST. A veces esto lo causan valores
          TCP MSS demasiado grandes para redes PPPoE que no pueden
          transportar paquetes de tamaño completo. También puede ocurrir
          cuando el timeout del cliente es menor que el del servidor y el
          servidor tarda demasiado en responder.

     CQ   El cliente abortó mientras su flujo estaba en cola, esperando un
          servidor con suficientes huecos libres para aceptarlo. Puede ser que
          todos los servidores estuvieran saturados o que el servidor asignado
          tardara demasiado en responder.

     CR   El cliente abortó antes de enviar una petición HTTP completa. Lo más
          probable es que la petición se tecleara a mano con un cliente telnet
          y se abortara demasiado pronto. Aquí el código de estado HTTP
          probable es un 400. A veces esto también puede deberse a un IDS que
          mata la conexión entre HAProxy y el cliente. Puede usarse «option
          http-ignore-probes» para ignorar conexiones sin ninguna
          transferencia de datos.

     cR   El «timeout http-request» se disparó antes de que el cliente enviara
          una petición HTTP completa. A veces esto lo causan valores TCP MSS
          demasiado grandes en el lado del cliente para redes PPPoE que no
          pueden transportar paquetes de tamaño completo, o clientes que
          envían peticiones a mano sin teclear lo bastante rápido, u olvidando
          introducir la línea vacía al final de la petición. Aquí el código de
          estado HTTP probable es un 408. Nota: recientemente, algunos
          navegadores empezaron a implementar una función de «pre-conexión»
          que consiste en conectarse de forma especulativa a algunos sitios
          web visitados recientemente, por si el usuario quisiera visitarlos.
          Esto resulta en muchas conexiones establecidas a sitios web, que
          acaban en 408 Request Timeout si el timeout se dispara primero, o en
          400 Bad Request cuando el navegador decide cerrarlas primero. Estas
          contaminan el registro y alimentan los contadores de errores. Se ha
          reportado incluso que algunas versiones de algunos navegadores
          muestran el código de error. Es posible sortear los efectos
          indeseables de este comportamiento añadiendo «option
          http-ignore-probes» en el frontend, lo que hace que las conexiones
          sin ninguna transferencia de datos se ignoren totalmente. Aunque
          esto ocultará definitivamente los errores de las personas con
          problemas de conectividad.

     CT   El cliente abortó mientras su flujo estaba en tarpit. Es importante
          comprobar si esto ocurre con peticiones válidas, para estar seguro
          de que no se han escrito reglas tarpit incorrectas. Si ocurren
          muchas, puede tener sentido bajar el valor de «timeout tarpit» a
          algo más cercano al temporizador «Tw» medio reportado, para no
          consumir recursos por solo unos pocos atacantes.

     LC   La petición fue interceptada y gestionada localmente por HAProxy.
          La petición no se envió al servidor. Solo ocurre con una
          redirección debida a un parámetro «redir» en la línea del servidor.

     LR   La petición fue interceptada y gestionada localmente por HAProxy.
          La petición no se envió al servidor. Generalmente significa que se
          devolvió una redirección, se procesó una instrucción HTTP return o
          la petición fue gestionada por un applet (stats, caché, exportador
          de Prometheus, applet de lua...).

     LH   La respuesta fue interceptada y gestionada localmente por HAProxy.
          Generalmente significa que se devolvió una redirección o se procesó
          una instrucción HTTP return.

     SC   El servidor o un equipo entre este y HAProxy rechazó explícitamente
          la conexión TCP (el proxy recibió un TCP RST o un mensaje ICMP de
          vuelta). Bajo ciertas circunstancias, también puede ser la pila de
          red informando al proxy de que el servidor es inalcanzable (p. ej.,
          sin ruta, o sin respuesta ARP en la red local). Cuando esto ocurre
          en modo HTTP, aquí el código de estado probable es un 502 o 503.

     sC   El «timeout connect» se disparó antes de que una conexión al
          servidor pudiera completarse. Cuando esto ocurre en modo HTTP, aquí
          el código de estado probable es un 503 o 504.

     SD   La conexión al servidor murió con un error durante la transferencia
          de datos. Esto normalmente significa que HAProxy recibió un RST del
          servidor o un mensaje ICMP de un equipo intermedio mientras
          intercambiaba datos con el servidor. Puede deberse a una caída del
          servidor o a un problema de red en un equipo intermedio.

     sD   El servidor no envió ni reconoció ningún dato durante el plazo definido por el
          ajuste «timeout server» en la fase de datos. Esto suele deberse a
          timeouts demasiado cortos en los equipos L4 delante del servidor
          (firewalls, balanceadores, ...), así como a sesiones keep-alive
          mantenidas entre el cliente y el servidor que expiran primero en
          HAProxy.

     SH   El servidor abortó antes de enviar todas sus cabeceras de respuesta
          HTTP, o falló mientras procesaba la petición. Dado que es muy
          raro que un servidor aborte en este momento, sería prudente
          inspeccionar sus registros para comprobar si falló y por qué.
          La petición registrada puede indicar un pequeño conjunto de
          peticiones defectuosas, que evidencian bugs en la aplicación. A
          veces esto también puede deberse a un IDS que mata la conexión entre
          HAProxy y el servidor.

     sH   El «timeout server» se disparó antes de que el servidor pudiera
          devolver sus cabeceras de respuesta. Esta es la anomalía más común,
          e indica transacciones demasiado largas, probablemente causadas por
          la saturación del servidor o de la base de datos. La solución
          inmediata consiste en aumentar el ajuste «timeout server», pero es
          importante tener en cuenta que la experiencia de usuario se
          resentirá con estos tiempos de respuesta tan largos. La única
          solución a largo plazo es arreglar la aplicación.

     sQ   El flujo pasó demasiado tiempo en cola y ha expirado. Consulta los
          ajustes «timeout queue» y «timeout connect» para saber cómo
          corregirlo si ocurre con demasiada frecuencia. Si ocurre a menudo
          de forma masiva en periodos cortos, puede indicar problemas
          generales en los servidores afectados por congestión de E/S o de
          base de datos, o saturación causada por ataques externos.

     PC   El proxy rechazó establecer una conexión con el servidor porque se
          alcanzó el límite de sockets del proceso al intentar conectarse. El
          parámetro global «maxconn» puede aumentarse en la configuración
          para que no vuelva a ocurrir. Este estado es muy raro y puede
          ocurrir cuando el parámetro global «ulimit-n» se fuerza a mano.

     PD   El proxy bloqueó un mensaje con codificación chunked mal formateado
          en una petición o una respuesta, después de que el servidor emitiera
          sus cabeceras. En la mayoría de los casos, esto indicará un mensaje
          inválido del servidor al cliente. HAProxy admite tamaños de chunk
          de hasta 2GB - 1 (2147483647 bytes). Cualquier tamaño mayor se
          considerará un error.

     PH   El proxy bloqueó la respuesta del servidor porque era inválida,
          incompleta, peligrosa (control de caché) o coincidió con un filtro
          de seguridad. En cualquier caso, se envía un error HTTP 502 al
          cliente. Una causa posible de este error es una sintaxis inválida
          en un nombre de cabecera HTTP que contiene caracteres no
          autorizados. También es posible, aunque bastante raro, que el proxy
          bloqueara una petición con codificación chunked del cliente por una
          sintaxis inválida, antes de que el servidor respondiera. En este
          caso, se envía un error HTTP 400 al cliente y se reporta en los
          registros. Por último, puede deberse a un fallo de reescritura de
          cabeceras HTTP en la respuesta. En este caso, se envía un error
          HTTP 500 (ver «tune.maxrewrite» y «http-response strict-mode» para
          más información).

     PR   El proxy bloqueó la petición HTTP del cliente, ya fuera por una
          sintaxis HTTP inválida, en cuyo caso devolvió un error HTTP 400 al
          cliente, o porque coincidió un filtro deny, en cuyo caso devolvió
          un error HTTP 403. También puede deberse a un fallo de reescritura
          de cabeceras HTTP en la petición. En este caso, se envía un error
          HTTP 500 (ver «tune.maxrewrite» y «http-request strict-mode» para
          más información).

     PT   El proxy bloqueó la petición del cliente y puso su conexión en
          tarpit antes de devolverle un error de servidor 500. No se envió
          nada al servidor. La conexión se mantuvo abierta durante el tiempo
          que reporta el campo del temporizador «Tw».

     RC   Se agotó un recurso local (memoria, sockets, puertos de origen),
          impidiendo que la conexión al servidor se estableciera. Los
          registros de error dirán con precisión qué faltaba. Esto es muy
          raro y solo puede resolverse con una configuración adecuada del
          sistema.

La combinación de los dos últimos indicadores da mucha información sobre cómo se gestionó la
persistencia por el cliente, el servidor y HAProxy. Esto es muy importante para resolver
desconexiones, cuando los usuarios se quejan de tener que reautenticarse. Los indicadores que
se encuentran comúnmente son:

```text
--   La cookie de persistencia no está activada.

NN   El cliente no proporcionó ninguna cookie y no se insertó ninguna en
     la respuesta. Por ejemplo, esto puede ocurrir en modo insert con
     «postonly» establecido en una petición GET.

II   El cliente proporcionó una cookie que designa un servidor inválido,
     y se insertó una válida en la respuesta. Esto ocurre típicamente
     cuando se elimina una entrada «server» de la configuración, ya que
     su valor de cookie puede ser presentado por un cliente cuando
     ningún otro servidor lo conoce.

NI   El cliente no proporcionó ninguna cookie; se insertó una en la
     respuesta. Esto ocurre típicamente en las primeras peticiones de
     cada usuario en modo «insert», lo que la convierte en una forma
     sencilla de contar usuarios reales.

VN   El cliente proporcionó una cookie; no se insertó ninguna en la
     respuesta. Esto ocurre en la mayoría de las respuestas para las
     que el cliente ya tiene una cookie.

VU   El cliente proporcionó una cookie con una fecha de última visita
     que no está completamente al día, así que se proporcionó una cookie
     actualizada en la respuesta. Esto también puede ocurrir si no había
     fecha en absoluto, o si había fecha pero el parámetro «maxidle» no
     estaba establecido, de modo que la cookie pueda cambiarse a tiempo
     ilimitado.

EI   El cliente proporcionó una cookie con una fecha de última visita
     demasiado antigua para el parámetro «maxidle», así que la cookie se
     ignoró y se insertó una nueva cookie en la respuesta.

OI   El cliente proporcionó una cookie con una fecha de primera visita
     demasiado antigua para el parámetro «maxlife», así que la cookie se
     ignoró y se insertó una nueva cookie en la respuesta.

DI   El servidor designado por la cookie estaba caído; se seleccionó un
     nuevo servidor y se emitió una nueva cookie en la respuesta.

VI   El servidor designado por la cookie no estaba marcado como muerto
     pero no se pudo alcanzar. Ocurrió un redispatch y se seleccionó
     otro, que fue entonces el anunciado en la respuesta.
```

## 8.6. Caracteres no imprimibles {#section-8-6}

Para no causar problemas a las herramientas de análisis de registros ni a los terminales durante
la consulta de registros, los caracteres no imprimibles no se envían tal cual a los archivos de
registro, sino que se convierten a la representación hexadecimal de dos dígitos de su código
ASCII, prefijada por el carácter «#». Los únicos caracteres que pueden registrarse sin escaparse
están comprendidos entre el 32 y el 126 (inclusive). Evidentemente, el carácter de escape «#»
mismo también se codifica para evitar cualquier ambigüedad («#23»). Lo mismo ocurre con el
carácter '"', que se convierte en «#22», así como con «{», «\|» y «}» al registrar cabeceras.

Esto no se aplica a la codificación cbor, que ya usa dígitos hexadecimales seguros, o bloques
binarios correctamente delimitados que no se enviarán a un terminal sino que serán consumidos
por un analizador CBOR.

La codificación json usa en su lugar las secuencias de escape JSON, y la opción +utf8 también
deja pasar tal cual las secuencias UTF-8 multibyte válidas (consulta el flag «utf8» en la
[sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)).

Ten en cuenta que el carácter de espacio (' ') no se codifica en las cabeceras, lo que puede
causar problemas a las herramientas que se basan en el conteo de espacios para localizar
campos. Una cabecera típica que contiene espacios es «User-Agent».

Por último, se ha observado que algunos demonios syslog como syslog-ng escapan la comilla
('"') con una barra invertida («&#92;»). La operación inversa puede realizarse con seguridad,
ya que ninguna comilla puede aparecer en ningún otro lugar de los registros.

## 8.7. Captura de cookies HTTP {#section-8-7}

La captura de cookies simplifica el rastreo de una sesión completa de usuario. Esto puede
lograrse usando la instrucción «capture cookie» en el frontend. Consulta la [sección 4.2](/es/haproxy/proxies/#section-4-2) para más detalles. Solo puede capturarse
una cookie, y la misma cookie se comprobará simultáneamente en la petición (cabecera
«Cookie:») y en la respuesta (cabecera «Set-Cookie:»). Los valores respectivos se reportarán en
los registros HTTP en las posiciones «captured_request_cookie» y
«captured_response_cookie» (consulta la [sección 8.2.3](/es/haproxy/configuration-logging/#section-8-2-3) sobre el formato de registro HTTP). Cuando no se ve
una de las cookies, un guion («-») sustituye su valor. De este modo, es fácil detectar,
por ejemplo, cuándo un usuario cambia a una sesión nueva, porque el servidor le reasignará una
cookie nueva. También es posible detectar si un servidor establece inesperadamente una cookie
errónea a un cliente, lo que provocaría un cruce de sesiones.

Ejemplos:

```shell
# capture the first cookie whose name starts with "ASPSESSION"
capture cookie ASPSESSION len 32

# capture the first cookie whose name is exactly "vgnvisitor"
capture cookie vgnvisitor= len 32
```

Es posible realizar capturas más avanzadas usando reglas «http-request» y «http-response» para
asignar cookies a variables de ámbito «txn». Los valores de las cookies pueden entonces
extraerse de la petición o la respuesta usando las funciones de extracción de muestra
«req.cook» y «res.cook» (consulta la [sección 7.3.6](/es/haproxy/acls-and-samples/#section-7-3-6)) y asignarse a una variable usando las
acciones «set-var» o «set-var-fmt» (consulta la [sección 4.3](/es/haproxy/proxies/#section-4-3)). Un formato de registro personalizado
permitirá entonces presentar estas variables donde se desee (consulta la
[sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)).

## 8.8. Captura de cabeceras HTTP (heredado) {#section-8-8}

Las capturas de cabeceras son útiles para rastrear identificadores únicos de petición
establecidos por un proxy superior, nombres de host virtuales, user-agents, content-length de
POST, referrers, etc. En la respuesta, puede buscarse información sobre la longitud de la
respuesta, cómo pidió el servidor a la caché que se comportara, o la localización de un objeto
durante una redirección.

Hay dos formas de realizar capturas de cabeceras. La moderna consiste en establecer variables
a partir de las cabeceras que se van a capturar, o a partir de muestras compuestas devueltas
por «req.hdr_names», «req.hdrs», «res.hdr_names», «res.hdrs» (consulta la
[sección 7.3.6](/es/haproxy/acls-and-samples/#section-7-3-6)) para todas las posibilidades. Estas pueden asignarse a variables de ámbito
«txn» usando las acciones «set-var» y «set-var-fmt» de los conjuntos de reglas «http-request»
y «http-response» (consulta la [sección 4.3](/es/haproxy/proxies/#section-4-3)), que luego pueden referenciarse desde formatos de registro
personalizados (consulta la [sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6)). Esta es la forma recomendada de capturar cabeceras HTTP.

También existe el método heredado, anterior a las reglas http-request y a las variables, que
no implica ajustar el formato de registro, y que además se ha usado durante mucho tiempo tanto
para registrar como de forma artificial para transmitir información de la petición a lo largo
de toda la transacción HTTP, usando los conjuntos de reglas «capture» más antiguos. Esto es lo
que se describe en esta sección.

Las capturas de cabeceras heredadas se realizan usando las instrucciones «capture request
header» y «capture response header» en el frontend. Consulta su definición en la
[sección 4.2](/es/haproxy/proxies/#section-4-2) para más detalles.

Es posible incluir al mismo tiempo cabeceras de petición y cabeceras de respuesta. Las
cabeceras inexistentes se registran como cadenas vacías, y si una cabecera aparece más de una
vez, solo se registrará su última ocurrencia. Las cabeceras de petición se agrupan dentro de
llaves «{» y «}» en el mismo orden en que se declararon, y delimitadas con una barra vertical
«\|» sin ningún espacio. Las cabeceras de respuesta siguen la misma representación, pero se
muestran tras un espacio que sigue al bloque de cabeceras de petición. Estos bloques se
muestran justo antes de la petición HTTP en los registros.

Como caso especial, es posible especificar una captura de cabecera HTTP en un frontend TCP. El
propósito es habilitar el registro de cabeceras que se analizarán en un backend HTTP si la
petición se conmuta luego a ese backend HTTP.

Ejemplo:

```shell
# This instance chains to the outgoing proxy
listen proxy-out
    mode http
    option httplog
    option logasap
    log global
    server cache1 192.168.1.1:3128

    # log the name of the virtual server
    capture request  header Host len 20

    # log the amount of data uploaded during a POST
    capture request  header Content-Length len 10

    # log the beginning of the referrer
    capture request  header Referer len 20

    # server name (useful for outgoing proxies only)
    capture response header Server len 20

    # logging the content-length is useful with "option logasap"
    capture response header Content-Length len 10

    # log the expected cache behavior on the response
    capture response header Cache-Control len 8

    # the Via header will report the next proxy's name
    capture response header Via len 20

    # log the URL location during a redirection
    capture response header Location len 20
```

```text
    >>> Aug  9 20:26:09 localhost \
          haproxy[2022]: 127.0.0.1:34014 [09/Aug/2004:20:26:09] proxy-out \
          proxy-out/cache1 0/0/0/162/+162 200 +350 - - ---- 0/0/0/0/0 0/0 \
          {fr.adserver.yahoo.co||http://fr.f416.mail.} {|864|private||} \
          "GET http://fr.adserver.yahoo.com/"
```

```text
    >>> Aug  9 20:30:46 localhost \
          haproxy[2022]: 127.0.0.1:34020 [09/Aug/2004:20:30:46] proxy-out \
          proxy-out/cache1 0/0/0/182/+182 200 +279 - - ---- 0/0/0/0/0 0/0 \
          {w.ods.org||} {Formilux/0.1.8|3495|||} \
          "GET http://trafic.1wt.eu/ HTTP/1.1"
```

```text
    >>> Aug  9 20:30:46 localhost \
          haproxy[2022]: 127.0.0.1:34028 [09/Aug/2004:20:30:46] proxy-out \
          proxy-out/cache1 0/0/2/126/+128 301 +223 - - ---- 0/0/0/0/0 0/0 \
          {www.sytadin.equipement.gouv.fr||http://trafic.1wt.eu/} \
          {Apache|230|||http://www.sytadin.} \
          "GET http://www.sytadin.equipement.gouv.fr/ HTTP/1.1"
```

## 8.9. Ejemplos de registros {#section-8-9}

Estos son ejemplos reales de registros acompañados de una explicación. Algunos de ellos se han
inventado a mano. La parte syslog se ha eliminado para una mejor lectura. Su único propósito es
explicar cómo descifrarlos.

    >>> haproxy[674]: 127.0.0.1:33318 [15/Oct/2003:08:31:57.130] px-http &#92;
          px-http/srv1 6559/0/7/147/6723 200 243 - - ---- 5/3/3/1/0 0/0 &#92;
          "HEAD / HTTP/1.0"

    => petición larga (6.5s) introducida a mano mediante «telnet». El servidor
       respondió en 147 ms, y la sesión terminó con normalidad («----»)

    >>> haproxy[674]: 127.0.0.1:33319 [15/Oct/2003:08:31:57.149] px-http &#92;
          px-http/srv1 6559/1230/7/147/6870 200 243 - - ---- 324/239/239/99/0 &#92;
          0/9 "HEAD / HTTP/1.0"

    => Ídem, pero la petición se puso en la cola global detrás de otras 9
       peticiones, y esperó allí durante 1230 ms.

```text
    >>> haproxy[674]: 127.0.0.1:33320 [15/Oct/2003:08:32:17.654] px-http \
          px-http/srv1 9/0/7/14/+30 200 +243 - - ---- 3/3/3/1/0 0/0 \
          "GET /image.iso HTTP/1.0"
```

    => petición de una transferencia de datos larga. Se especificó la opción
       «logasap», así que el registro se produjo justo antes de transferir los
       datos. El servidor respondió en 14 ms, se enviaron 243 bytes de
       cabeceras al cliente, y el tiempo total desde la aceptación hasta el
       primer byte de datos es de 30 ms.

    >>> haproxy[674]: 127.0.0.1:33320 [15/Oct/2003:08:32:17.925] px-http &#92;
          px-http/srv1 9/0/7/14/30 502 243 - - PH-- 3/2/2/0/0 0/0 &#92;
          "GET /cgi-bin/bug.cgi? HTTP/1.0"

    => el proxy bloqueó una respuesta del servidor, ya sea por una regla
       «http-response deny», porque la respuesta estaba mal formateada y no era
       conforme con HTTP, o porque bloqueó información sensible que corría el
       riesgo de ser almacenada en caché. En este caso, la respuesta se
       sustituye por un «502 bad gateway». Los indicadores («PH--») nos dicen
       que fue HAProxy quien decidió devolver el 502 y no el servidor.

    >>> haproxy[18113]: 127.0.0.1:34548 [15/Oct/2003:15:18:55.798] px-http &#92;
          px-http/`<NOSRV>` -1/-1/-1/-1/8490 -1 0 - - CR-- 2/2/2/0/0 0/0 ""

    => el cliente nunca completó su petición y se abortó a sí mismo («C---»)
       tras 8.5s, mientras el proxy esperaba las cabeceras de la petición
       («-R--»). No se envió nada a ningún servidor.

    >>> haproxy[18113]: 127.0.0.1:34549 [15/Oct/2003:15:19:06.103] px-http &#92;
         px-http/`<NOSRV>` -1/-1/-1/-1/50001 408 0 - - cR-- 2/2/2/0/0 0/0 ""

    => El cliente nunca completó su petición, que fue abortada por el timeout
       («c---») tras 50s, mientras el proxy esperaba las cabeceras de la
       petición («-R--»). No se envió nada a ningún servidor, pero el proxy
       pudo enviar un código de retorno 408 al cliente.

    >>> haproxy[18989]: 127.0.0.1:34550 [15/Oct/2003:15:24:28.312] px-tcp &#92;
          px-tcp/srv1 0/0/5007 0 cD 0/0/0/0/0 0/0

    => Este registro se produjo con «option tcplog». El cliente agotó el
       tiempo de espera tras 5 segundos («c----»).

    >>> haproxy[18989]: 10.0.0.1:34552 [15/Oct/2003:15:26:31.462] px-http &#92;
          px-http/srv1 3183/-1/-1/-1/11215 503 0 - - SC-- 205/202/202/115/3 &#92;
          0/0 "HEAD / HTTP/1.0"

    => La petición tardó 3s en completarse (probablemente un problema de red),
       y la conexión al servidor falló («SC--») tras 4 intentos de 2 segundos
       (la configuración dice «retries 3»), y sin redispatch (de lo contrario
       habríamos visto «/+3»). Se devolvió el código de estado 503 al cliente.
       Había 115 conexiones en este servidor, 202 conexiones en este proxy, y
       205 en el proceso global. Es posible que el servidor rechazara la
       conexión porque ya tenía demasiadas establecidas.
