---
title: "12. Otras secciones"
linkTitle: "12. Otras secciones"
weight: 230
description: "Trazas, usuarios, mailers, errores, anillos, certificados, ACME y comprobaciones de estado globales"
icon: fa-solid fa-ellipsis
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/other-sections/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 12"
---

Las secciones descritas a continuación son de uso menos común y normalmente solo admiten unos pocos
parámetros. No existe ninguna relación implícita entre ellas. Todas comienzan con una única palabra
clave. Ninguna de ellas está permitida antes de una sección «global». El soporte de algunas de ellas
puede estar condicionado por opciones de compilación (por ejemplo, todo lo relacionado con SSL).

## 12.1. Trazas {#section-12-1}

A efectos de depuración, es posible activar trazas en un subsistema de HAProxy. Esto volcará
mensajes de depuración sobre un subsistema específico. Es una herramienta muy potente para
diagnosticar problemas. Las trazas pueden configurarse dinámicamente a través de la CLI. También es
posible predefinir algunos ajustes en el archivo de configuración, en secciones «traces» dedicadas.
Puede encontrarse más detalle sobre las trazas en la guía de administración. Sigue siendo una
herramienta de desarrolladores que se usa durante sesiones de depuración complejas. Es bastante
verbosa y tiene un coste, así que úsala con precaución. Y por tratarse de una herramienta de
desarrolladores, no hay garantía alguna sobre la compatibilidad hacia atrás de esta sección.

<a id="entry-12-1-traces"></a>

**`traces`**

```haproxy
traces
```

Inicia una nueva sección traces. Puede usarse una o varias secciones «traces». Todas las directivas se
evalúan en el orden de declaración, y las últimas prevalecen sobre las anteriores.

<a id="entry-12-1-trace"></a>

**`trace <source> <args...>`**

```haproxy
trace <source> <args...>
```

Configura un subsistema de «trace». Cada uno de ellos puede encontrarse en el manual de
administración y sigue exactamente la misma sintaxis. Cualquier salida que produzca el comando
«trace» se emitirá durante la fase de análisis de la sección. La mayoría de las veces serán errores
y advertencias, pero ciertos comandos incompletos pueden listar las opciones permitidas. Este
comando no está pensado para un uso regular; generalmente solo lo sugerirán los desarrolladores
durante sesiones de depuración complejas. Es importante tener presente que, según el nivel y el
detalle de la traza, habilitar las trazas puede degradar seriamente el rendimiento global. Consulta
el manual de administración para la sintaxis de las instrucciones.

Ejemplo:

```text
ring buf1
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h1.traces

ring buf2
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h2.traces

traces
  trace h1 sink buf1 level developer verbosity complete start now
  trace h2 sink buf1 level developer verbosity complete start now
```

## 12.2. Listas de usuarios {#section-12-2}

Es posible controlar el acceso a las secciones frontend/backend/listen o a las estadísticas http
admitiendo únicamente a usuarios autenticados y autorizados. Para ello es necesario crear al menos
una userlist y definir usuarios.

<a id="entry-12-2-userlist"></a>

**`userlist <listname>`**

```haproxy
userlist <listname>
```

Crea una nueva lista de usuarios con el nombre `<listname>`. Pueden usarse varias listas de usuarios
independientes para almacenar datos de autenticación y autorización de clientes independientes.

<a id="entry-12-2-group"></a>

**`group <groupname> [users <user>,<user>,(...)]`**

```haproxy
group <groupname> [users <user>,<user>,(...)]
```

Añade el grupo `<groupname>` a la lista de usuarios actual. También es posible adjuntar usuarios a
este grupo mediante una lista de nombres separados por comas precedida de la palabra clave «users».

<a id="entry-12-2-user"></a>

**`user <username> [password|insecure-password <password>]`**

```haproxy
user <username> [password|insecure-password <password>]
                [groups <group>,<group>,(...)]
```

Añade el usuario `<username>` a la lista de usuarios actual. Pueden usarse tanto contraseñas
seguras (cifradas) como inseguras (sin cifrar). Las contraseñas cifradas se evalúan con la función
crypt(3), de modo que, según las capacidades del sistema, se admiten distintos algoritmos. Por
ejemplo, los sistemas Linux modernos basados en Glibc admiten MD5, SHA-256, SHA-512 y, por supuesto,
el método clásico basado en DES para cifrar contraseñas.

Atención: ten en cuenta que el uso de contraseñas cifradas puede aumentar significativamente el uso
de CPU, dependiendo del número de solicitudes y del algoritmo utilizado. Para cualquiera de las
variantes con hash, la contraseña de cada solicitud debe procesarse con el algoritmo elegido antes
de poder compararla con el valor especificado en el archivo de configuración. La mayoría de los
algoritmos actuales están diseñados deliberadamente para ser costosos de calcular, con el fin de
resistir los ataques de fuerza bruta. No aplican el hash con sal a la contraseña en texto claro una
sola vez, sino miles de veces. Esto puede convertirse rápidamente en un factor importante del
consumo total de CPU de HAProxy, ¡e incluso provocar caídas de la aplicación!

Para abordar el elevado uso de CPU de las funciones hash, un enfoque consiste en reducir el número
de rondas de la función hash (algoritmos de la familia SHA) o disminuir el «coste» de la función,
si el algoritmo lo permite.

Como nota al margen, se sabe que las implementaciones de musl (por ejemplo, Alpine Linux) son más
lentas que sus equivalentes de glibc al calcular hashes, así que quizá quieras considerar también este aspecto.

Todas las contraseñas se consideran argumentos normales y, por lo tanto, están sujetas a las reglas
habituales de entrecomillado y escape de la [sección 2.2](/es/haproxy/configuration-basics/#section-2-2).
Por ello se recomienda entrecomillar las contraseñas con comillas simples.

Ejemplo:

```text
userlist L1
  group G1 users tiger,scott
  group G2 users xdb,scott

  user tiger password $6$k6y3o.eP$JlKBx9za9667qe4(...)xHSwRv6J.C0/D7cV91
  user scott insecure-password 'elgato'
  user xdb insecure-password 'hello'

userlist L2
  group G1
  group G2

  user tiger password $6$k6y3o.eP$JlKBx(...)xHSwRv6J.C0/D7cV91 groups G1
  user scott insecure-password 'elgato' groups G1,G2
  user xdb insecure-password 'hello' groups G2
```

Ten en cuenta que ambas listas son funcionalmente idénticas.

## 12.3. Mailers {#section-12-3}

Es posible enviar alertas por correo electrónico cuando cambia el estado de los servidores. Si se
configuran, las alertas por correo electrónico se envían a cada mailer configurado en una sección
mailers. El correo se envía a los mailers a través de Lua (consulta examples/lua/mailers.lua).

<a id="entry-12-3-mailers"></a>

**`mailers <mailersect>`**

```haproxy
mailers <mailersect>
```

Crea una nueva lista de mailers con el nombre `<mailersect>`. Es una sección independiente a la que
hacen referencia uno o más proxies.

<a id="entry-12-3-mailer"></a>

**`mailer <mailername> <ip>:<port>`**

```haproxy
mailer <mailername> <ip>:<port>
```

Define un mailer dentro de una sección mailers.

Ejemplo:

```text
global
    # mailers.lua file as provided in the git repository
    # adjust path as needed
    lua-load examples/lua/mailers.lua

mailers mymailers
    mailer smtp1 192.168.0.1:587
    mailer smtp2 192.168.0.2:587

backend mybackend
    mode tcp
    balance roundrobin

    email-alert mailers mymailers
    email-alert from test1@horms.org
    email-alert to test2@horms.org

    server srv1 192.168.0.30:80
    server srv2 192.168.0.31:80
```

<a id="entry-12-3-timeout-mail"></a>

**`timeout mail <time>`**

```haproxy
timeout mail <time>
```

Define el tiempo disponible para establecer la conexión y enviar un mensaje al servidor de
correo. Si no se define, el valor por defecto es 10 segundos. Para permitir el envío de al menos dos
paquetes SYN-ACK durante el saludo TCP inicial, se aconseja mantener este valor por encima de 4 segundos.

Ejemplo:

```text
mailers mymailers
    timeout mail 20s
    mailer smtp1 192.168.0.1:587
```

## 12.4. Errores HTTP {#section-12-4}

Es posible declarar globalmente varios grupos de errores HTTP, para importarlos después en
cualquier sección de proxy. Un mismo grupo puede referenciarse en varios lugares e importarse total
o parcialmente.

<a id="entry-12-4-http-errors"></a>

**`http-errors <name>`**

```haproxy
http-errors <name>
```

Crea un nuevo grupo http-errors con el nombre `<name>`. Es una sección independiente a la que uno
o más proxies pueden hacer referencia mediante su nombre.

<a id="entry-12-4-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

Asocia el contenido de un archivo a un código de error HTTP

Argumentos:

```text
<code>    es el código de estado HTTP. Actualmente, HAProxy es capaz de
          generar los códigos 200, 400, 401, 403, 404, 405, 407, 408, 410,
          425, 429, 500, 501, 502, 503 y 504.

<file>    designa un archivo que contiene la respuesta HTTP completa. Se
          recomienda seguir la práctica común de añadir «.http» al nombre
          del archivo para que la gente no confunda la respuesta con páginas
          de error HTML, y usar rutas absolutas, ya que los archivos se leen
          antes de que se realice cualquier chroot.
```

Consulta la palabra clave «errorfile» en la [sección 4](/es/haproxy/proxies/) para más detalles.

Ejemplo:

```text
http-errors website-1
    errorfile 400 /etc/haproxy/errorfiles/site1/400.http
    errorfile 404 /etc/haproxy/errorfiles/site1/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug

http-errors website-2
    errorfile 400 /etc/haproxy/errorfiles/site2/400.http
    errorfile 404 /etc/haproxy/errorfiles/site2/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug
```

## 12.5. Anillos {#section-12-5}

Es posible declarar globalmente búferes de anillo, para utilizarlos como destino de servidores de registro o de trazas.

<a id="entry-12-5-ring"></a>

**`ring <ringname>`**

```haproxy
ring <ringname>
```

Crea un nuevo búfer de anillo con el nombre `<ringname>`.

<a id="entry-12-5-backing-file"></a>

**`backing-file <path>`**

```haproxy
backing-file <path>
```

Esto sustituye la asignación regular de memoria por un archivo mapeado en RAM para almacenar el
anillo. Puede ser útil para recopilar trazas o registros con fines de análisis post-mortem, sin
tener que conectar un cliente lento a la CLI. El contenido más reciente sustituirá automáticamente
al más antiguo, de modo que lo último estará siempre disponible. El contenido escrito en el anillo
será visible en ese archivo cuando el proceso se detenga (la mayoría de las veces se verá incluso
muy pronto, pero no existe tal garantía, ya que las escrituras no son síncronas).

Cuando se utiliza esta opción, el área de almacenamiento total se ve reducida por el tamaño de la
«struct ring» que se encuentra al principio del área y que es necesaria para recuperar el contenido
de esta. El archivo se creará con la propiedad del usuario que inicia el proceso, con modo 0600 y
tendrá el tamaño configurado por la directiva «size». Cuando se analiza la directiva (por tanto,
incluso durante las comprobaciones de configuración), cualquier archivo existente no vacío será
renombrado primero con el sufijo adicional «.bak», y cualquier archivo «.bak» existente con
anterioridad será eliminado. Esto garantiza que una recarga o un reinicio inmediato del proceso no
borren información de depuración valiosa, y deja tiempo para que un administrador detecte este
nuevo archivo «.bak» y lo archive si es necesario. Así, tras un fallo, el archivo designado por
`<path>` contendrá la información más reciente y, si el servicio se reinicia, será el archivo
«`<path>`.bak» el que la contenga. Esto significa que la capacidad total de almacenamiento
necesaria será el doble del tamaño del anillo. Los fallos al rotar el archivo se ignoran
silenciosamente, de modo que colocar el archivo en un directorio sin permisos de escritura será
suficiente para evitar el archivo de copia de seguridad si no se desea.

ADVERTENCIA: el uso de esta característica tiene implicaciones de estabilidad y seguridad. Primero,
respaldar el anillo en un dispositivo lento (por ejemplo, un disco duro físico) puede causar
ralentizaciones perceptibles durante los accesos, e incluso pánicos si demasiados hilos compiten
por los accesos. Segundo, un proceso externo que modifique el área podría provocar que el proceso
haproxy se bloquee o que sobrescriba parte de su propia memoria con trazas. Tercero, si el sistema
de archivos se llena antes que el anillo, las escrituras en el anillo pueden provocar el fallo del proceso.

La información presente en este anillo está estructurada y NO es directamente legible con un editor
de texto (aunque la mayor parte apenas parece legible). La salida de este archivo está destinada
únicamente a los desarrolladores.

<a id="entry-12-5-description"></a>

**`description <text>`**

```haproxy
description <text>
```

La descripción es una cadena de descripción opcional del anillo. Aparecerá en la CLI. Por defecto,
se reutiliza `<name>` para rellenar este campo.

<a id="entry-12-5-format"></a>

**`format <format>`**

```haproxy
format <format>
```

Formato utilizado para almacenar eventos en el búfer de anillo.

Argumentos:

```text
<format> es el formato de registro usado al generar mensajes syslog. Puede
         ser uno de los siguientes:

  iso     Un mensaje que contiene solo la fecha ISO, seguida del texto.
          Se omiten el PID, el nombre del proceso y el nombre del sistema.
          Está diseñado para usarse con un servidor de registros local.

  local   Análogo al formato de mensaje syslog rfc3164, excepto que se
          elimina el campo del nombre de host. Este es el valor por defecto.
          Nota: la opción «log-send-hostname» cambia el valor por defecto a
          rfc3164.

  raw     Un mensaje que contiene solo el texto. Se omiten el nivel, el PID,
          la fecha, la hora, el nombre del proceso y el nombre del sistema.
          Está diseñado para usarse en contenedores o durante el desarrollo,
          donde la severidad depende solo del descriptor de archivo usado
          (stdout/stderr). Este es el valor por defecto.

  rfc3164 El formato de mensaje syslog RFC3164.
          (https://tools.ietf.org/html/rfc3164)

  rfc5424 El formato de mensaje syslog RFC5424.
          (https://tools.ietf.org/html/rfc5424)

  short   Un mensaje que contiene solo un nivel entre corchetes angulares,
          como «<3>», seguido del texto. Se omiten el PID, la fecha, la
          hora, el nombre del proceso y el nombre del sistema. Está
          diseñado para usarse con un servidor de registros local. Este
          formato es compatible con lo que consume el logger de systemd.

 priority Un mensaje que contiene solo un nivel más la facility syslog entre
          corchetes angulares, como «<63>», seguido del texto. Se omiten el
          PID, la fecha, la hora, el nombre del proceso y el nombre del
          sistema. Está diseñado para usarse con un servidor de registros
          local.

  timed   Un mensaje que contiene solo un nivel entre corchetes angulares,
          como «<3>», seguido de la fecha ISO y del texto. Se omiten el PID,
          el nombre del proceso y el nombre del sistema. Está diseñado para
          usarse con un servidor de registros local.
```

<a id="entry-12-5-maxlen"></a>

**`maxlen <length>`**

```haproxy
maxlen <length>
```

La longitud máxima de un mensaje de evento almacenado en el anillo, incluida la cabecera
formateada. Si un mensaje de evento es más largo que `<length>`, se truncará a esta longitud.

<a id="entry-12-5-server"></a>

**`server <name> <address> [param*]`**

```haproxy
server <name> <address> [param*]
```

Se usa para configurar un servidor syslog tcp al que reenviar los mensajes del búfer de anillo.
Admite todos los parámetros de «server» que se encuentran en el apartado 5.2. Algunos de estos
parámetros son irrelevantes para las secciones «ring». Punto importante: hay pocas razones para
añadir más de un servidor a un anillo, porque todos los servidores recibirán exactamente la misma
copia del contenido del anillo y, como tal, el anillo avanzará a la velocidad del servidor más
lento. Si un servidor no responde, impedirá que los mensajes antiguos se purguen y puede bloquear
la inserción de mensajes nuevos en el anillo. La forma correcta de enviar mensajes a varios
servidores es usar un anillo distinto por cada servidor de registro, no adjuntar varios servidores
al mismo anillo. Ten en cuenta que la directiva específica de servidor «log-proto» se usa para
establecer el protocolo utilizado para enviar mensajes.

<a id="entry-12-5-size"></a>

**`size <size>`**

```haproxy
size <size>
```

Este es el tamaño opcional en bytes del búfer de anillo. El valor por defecto se establece en BUFSIZE.

<a id="entry-12-5-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

Establece el tiempo máximo de espera para que un intento de conexión a un servidor tenga éxito.

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

<a id="entry-12-5-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

Establece el tiempo máximo para los datos pendientes que permanecen en el búfer de salida.

Argumentos:

```text
<timeout> es el valor de tiempo de espera especificado en milisegundos por
          defecto, pero puede estar en cualquier otra unidad si el número
          lleva como sufijo la unidad, tal como se explica al principio de
          este documento.
```

Ejemplo:

```text
global
    log ring@myring local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    server mysyslogsrv 127.0.0.1:6514 log-proto octet-count
```

## 12.6. Reenvío de registros {#section-12-6}

Es posible declarar una o varias secciones de reenvío de registros; HAProxy reenviará todos los
mensajes de registro recibidos a una lista de servidores de registro.

<a id="entry-12-6-log-forward"></a>

**`log-forward <name>`**

```haproxy
log-forward <name>
```

Crea un nuevo proxy de reenvío de registros identificado como `<name>`.

<a id="entry-12-6-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

Da pistas al sistema sobre el tamaño aproximado deseado del backlog de escucha al aceptar conexiones.

<a id="entry-12-6-bind"></a>

**`bind <addr> [param*]`**

```haproxy
bind <addr> [param*]
```

Se usa para configurar un receptor de registros de flujo para recibir los mensajes que se van a
reenviar. Admite los parámetros de «bind» que se encuentran en el apartado 5.1, incluidos los
relacionados con ssl, pero algunas instrucciones como «alpn» pueden ser irrelevantes para el
protocolo syslog sobre TCP. Estos receptores admiten tanto el modo «Octet Counting» como el «Non-Transparent-Framing»,
tal como se definen en rfc-6587.

<a id="entry-12-6-dgram-bind"></a>

**`dgram-bind <addr> [param*]`**

```haproxy
dgram-bind <addr> [param*]
```

Se usa para configurar un receptor de registros de datagramas para recibir los mensajes que se van
a reenviar. Las direcciones deben estar en formato IPv4 o IPv6, seguidas de un puerto. Admite
algunos de los parámetros de «bind» que se encuentran en el apartado 5.1, entre ellos «interface»,
«namespace» o «transparent»; los demás se ignoran silenciosamente por irrelevantes en el caso UDP/syslog.

<a id="entry-12-6-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```

Se usa para configurar los servidores de registro de destino. Consulta más detalle en la documentación
de proxies. Si no se especifica ningún formato, HAProxy intenta conservar el formato de registro
entrante. La facility configurada se ignora, excepto si el mensaje entrante no presenta una
facility pero el formato de salida exige una. Si no hay marca de tiempo disponible en el formato de
entrada, pero el campo existe en el formato de salida, HAProxy usará la fecha local.

Ejemplo:

```text
global
   log stderr format iso local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    # syslog tcp server
    server mysyslogsrv 127.0.0.1:514 log-proto octet-count

log-forward sylog-loadb
    dgram-bind 127.0.0.1:1514
    bind 127.0.0.1:1514
    # all messages on stderr
    log global
    # all messages on local tcp syslog server
    log ring@myring local0
    # load balance messages on 4 udp syslog servers
    log 127.0.0.1:10001 sample 1:4 local0
    log 127.0.0.1:10002 sample 2:4 local0
    log 127.0.0.1:10003 sample 3:4 local0
    log 127.0.0.1:10004 sample 4:4 local0
```

<a id="entry-12-6-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

Fija el número máximo de conexiones simultáneas en un reenviador de registros. 10 es el valor por defecto.

<a id="entry-12-6-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

Establece el tiempo máximo de inactividad en el lado del cliente.

<a id="entry-12-6-option-assume-rfc6587-ntf"></a>

**`option assume-rfc6587-ntf`**

```haproxy
option assume-rfc6587-ntf
```

Indica a HAProxy que trate siempre los flujos de registro TCP entrantes como si usaran
non-transparent framing. Esta opción simplifica la lógica de encuadre y garantiza un manejo
coherente de los mensajes, particularmente útil ante caracteres iniciales mal formados.

<a id="entry-12-6-option-dont-parse-log"></a>

**`option dont-parse-log`**

```haproxy
option dont-parse-log
```

Permite a HAProxy retransmitir mensajes syslog sin intentar analizarlos y reestructurarlos, lo cual
es útil para reenviar mensajes que pueden no ajustarse a los formatos tradicionales. Esta opción
debería usarse con el ajuste format raw en los destinos de registro, para garantizar que se
preserve el contenido original del mensaje.

<a id="entry-12-6-option-host"></a>

**`option host { replace | fill | keep | append }`**

```haproxy
option host { replace | fill | keep | append }
```

Establece la estrategia de host que debe usarse en la sección log-forward respecto al campo
hostname de syslog para los mensajes salientes rfc3164 o rfc5424.

      replace Si el mensaje de entrada ya contiene un valor para el campo hostname,
              lo sustituimos por la dirección IP de origen del remitente.
              Si el mensaje de entrada no contiene un valor para el campo hostname
              (es decir: «-» como mensaje rfc5424 de entrada, o un mensaje rfc3164 o
              rfc5424 no conforme), usamos la dirección IP de origen del remitente
              como campo hostname.

      fill    Si el mensaje de entrada ya contiene un valor para el campo hostname,
              lo conservamos.
              Si el mensaje de entrada no contiene un valor para el campo hostname
              (es decir: «-» como mensaje rfc5424 de entrada, o un mensaje rfc3164 o
              rfc5424 no conforme), usamos la dirección IP de origen del remitente
              como campo hostname.
              (Este es el valor por defecto)

      keep    Si el mensaje de entrada ya contiene un valor para el campo hostname,
              lo conservamos.
              Si el mensaje de entrada no contiene un valor para el campo hostname,
              lo fijamos en «localhost» (rfc3164) o «-» (rfc5424).

      append  Si el mensaje de entrada ya contiene un valor para el campo hostname,
              añadimos una coma seguida de la dirección IP del remitente.
              Si el mensaje de entrada no contiene un valor para el campo hostname,
              usamos la dirección IP de origen del remitente.

Para todas las opciones anteriores, si la dirección IP de origen del remitente no está disponible
(es decir: socket UNIX/ABNS), la estrategia resultante es «keep».

Ten en cuenta que esta opción solo es relevante para los formatos de registro de destino rfc3164 o
rfc5424. En caso contrario, establecerla no tendrá ningún efecto visible.

## 12.7. Almacenamiento de certificados {#section-12-7}

HAProxy usa un mecanismo de almacenamiento interno para cargar y almacenar los certificados
utilizados en la configuración. Este almacén puede configurarse usando una sección «crt-store».
Permite configurar definiciones de certificados y qué archivos deben cargarse en él. Una definición
de certificado debe escribirse antes de utilizarse en cualquier otro lugar de la configuración.

crt-store [`<name>`]

La sección «crt-store» toma un nombre opcional como argumento. Si se especifica un nombre, cada
certificado de este almacén debe referenciarse usando «@`<name>`/`<crt>`» o «@`<name>`/`<alias>`».

Los archivos del almacén de certificados también pueden actualizarse dinámicamente con la CLI.
Consulta «set ssl cert» en la [sección 9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) de la guía de administración.

En la sección «crt-store» se admiten las siguientes palabras clave:

- crt-base
- key-base
- load

<a id="entry-12-7-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Asigna un directorio por defecto del que obtener los certificados SSL cuando se usa una ruta
relativa con las directivas «crt». Las ubicaciones absolutas especificadas prevalecen e ignoran
«crt-base». Cuando se usa en un crt-store, el crt-base de la sección global se ignora.

<a id="entry-12-7-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Asigna un directorio por defecto del que obtener las claves privadas SSL cuando se usa una ruta
relativa con las directivas «key». Las ubicaciones absolutas especificadas prevalecen e ignoran
«key-base». Cuando se usa en un crt-store, el key-base de la sección global se ignora.

<a id="entry-12-7-load"></a>

**`load [crt <filename>] [param*]`**

```haproxy
load [crt <filename>] [param*]
```

Carga archivos SSL en el almacén de certificados. Para la lista de parámetros, consulta la sección
«12.7.1. Opciones de carga»

Ejemplo:

```text
crt-store
    load crt "site1.crt" key "site1.key" ocsp "site1.ocsp" alias "site1"
    load crt "site2.crt" key "site2.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"

crt-store web
    crt-base /etc/ssl/certs/
    key-base /etc/ssl/private/
    load crt "site3.crt" alias "site3"
    load crt "site4.crt" key "site4.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"  crt "@web/site3" crt "@web/site4.crt"
```

### 12.7.1. Opciones de carga {#section-12-7-1}

Carga archivos SSL en el almacén de certificados. La palabra clave load puede tomar varios
parámetros, que se listan a continuación. Estas palabras clave también pueden usarse en un crt-list.

<a id="entry-12-7-1-crt"></a>

**`crt <filename>`**

```haproxy
crt <filename>
```

Este argumento es obligatorio; carga un PEM que debe contener el certificado público, pero que
también puede contener los certificados intermedios y la clave privada. Si no se proporciona una
clave privada en este archivo, puede proporcionarse una clave con la palabra clave «key».

<a id="entry-12-7-1-acme"></a>

**`acme <string>`**

```haproxy
acme <string>
```

Esta opción permite configurar el protocolo ACME para un certificado dado. Se trata de una
característica experimental que necesita la palabra clave «expose-experimental-directives» en la sección global.

Al usar la palabra clave «acme» en un crt-store, es posible iniciar sin un certificado existente en
el disco. En su lugar, se usará un par de claves temporal hasta que se genere el certificado ACME.
Este comportamiento es exclusivo de los crt-store; ni una línea crt-list ni una línea ssl-f-use
pueden lograr lo mismo sin declarar primero un crt-store.

Consulta también la [Sección 12.8](/es/haproxy/other-sections/#section-12-8) («ACME») y «domains» en esta sección.

<a id="entry-12-7-1-alias"></a>

**`alias <string>`**

```haproxy
alias <string>
```

Argumento opcional. Permite nombrar el certificado con un alias, de modo que pueda referenciarse
con él en la configuración. Un alias debe llevar el prefijo «@/» cuando se invoca en otra parte de la configuración.

<a id="entry-12-7-1-domains"></a>

**`domains <string>`**

```haproxy
domains <string>
```

Configura la lista de dominios que se usarán para los certificados ACME. El primer dominio de la
lista se usa como CN. Los dominios se separan por comas en la lista.

Consulta también la [Sección 12.8](/es/haproxy/other-sections/#section-12-8) («ACME») y «acme» en esta sección.

Ejemplo:

```text
load crt "example.com.pem" acme LE domains "bar.example.com,foo.example.com"
```

<a id="entry-12-7-1-ips"></a>

**`ips <string>`**

```haproxy
ips <string>
```

Configura la lista de direcciones IP que se incluirán como IP SAN en el certificado ACME. Las
direcciones IP se separan por comas en la lista.

Generar un certificado con IPs puede requerir el uso del perfil «shortlived».

Consulta también la [Sección 12.8](/es/haproxy/other-sections/#section-12-8) («ACME»), y «acme» y «domains» en esta sección.

Ejemplo:

```text
load crt "server.pem" acme LE ips "192.0.2.1,2001:db8::1"
```

<a id="entry-12-7-1-key"></a>

**`key <filename>`**

```haproxy
key <filename>
```

Este argumento es opcional. Carga una clave privada en formato PEM. Si ya se había definido una
clave privada en «crt», la sobrescribirá.

<a id="entry-12-7-1-ocsp"></a>

**`ocsp <filename>`**

```haproxy
ocsp <filename>
```

Este argumento es opcional; carga una respuesta OCSP en formato DER. Puede actualizarse con la CLI.

<a id="entry-12-7-1-issuer"></a>

**`issuer <filename>`**

```haproxy
issuer <filename>
```

Este argumento es opcional. Carga el emisor OCSP en formato PEM. Para identificar a qué certificado
se aplica una respuesta OCSP, es necesario el certificado del emisor. Si el certificado del emisor
no se encuentra en el archivo «crt», puede cargarse desde un archivo con este argumento.

<a id="entry-12-7-1-sctl"></a>

**`sctl <filename>`**

```haproxy
sctl <filename>
```

Este argumento es opcional. Se habilita el soporte de la extensión TLS de Certificate Transparency
(RFC6962). El archivo debe contener una Signed Certificate Timestamp List válida, tal como se
describe en el RFC. El archivo se analiza para comprobar la sintaxis básica, pero no se verifica ninguna firma.

<a id="entry-12-7-1-ocsp-update"></a>

**`ocsp-update [ off | on ]`**

```haproxy
ocsp-update [ off | on ]
```

Habilita la actualización automática de la respuesta OCSP cuando se establece en «on»; la
deshabilita en caso contrario. Su valor por defecto es «off». Para habilitar la actualización
automática de OCSP en una línea bind, puedes usar esta opción en un crt-store o usar la opción
global «tune.ocsp-update.mode». Si un certificado dado se usa en varios crt-lists con valores
distintos de «ocsp-update», se producirá un error. Asimismo, si un certificado hereda la opción
global en una línea bind y tiene fijada una opción «ocsp-update» explícita incompatible en un
crt-list, se producirá el mismo error.

Ejemplos:

A continuación, un ejemplo de configuración que lo habilita con un crt-list:

haproxy.cfg:

```text
frontend fe
    bind :443 ssl crt-list haproxy.list
```

haproxy.list:

```text
server_cert.pem [ocsp-update on] foo.bar
```

A continuación, un ejemplo de configuración que lo habilita con un crt-store:

haproxy.cfg:

```text
crt-store
  load crt foobar.pem ocsp-update on

frontend fe
    bind :443 ssl crt foobar.pem
```

Cuando la opción está establecida en «on», intentaremos obtener una respuesta ocsp siempre que se
encuentre un uri ocsp en el certificado del frontend. La única limitación de este modo es que habrá
que conocer el emisor del certificado para construir el certid OCSP. Cada respuesta OCSP se
actualizará al menos una vez por hora, e incluso con más frecuencia si una respuesta OCSP dada
tiene una fecha de caducidad anterior a ese límite de una hora. Existirá igualmente un intervalo
mínimo de actualización de 5 minutos para evitar actualizar con demasiada frecuencia respuestas con
un tiempo de caducidad realmente corto, o incluso sin «Next Update» en absoluto. Debido a este
límite estricto, ten en cuenta que cuando la actualización automática está en «on», cualquier
respuesta OCSP cargada durante el init no se actualizará hasta pasados al menos 5 minutos, incluso
si su tiempo de caducidad termina antes de now+5m. Esto no debería ser demasiado problema, ya que
una respuesta OCSP debe ser válida cuando se carga durante el init (su tiempo de caducidad debe
estar en el futuro), de modo que es improbable que esa respuesta caduque en un tiempo tan corto
tras el init. Por el contrario, si un certificado tiene especificado un uri OCSP y ninguna
respuesta OCSP, fijar esta opción en «on» para el certificado dado garantizará que la respuesta
OCSP se obtenga automáticamente justo después del init. Los retrasos mínimos y máximos por defecto
(5 minutos y 1 hora, respectivamente) pueden configurarse con las opciones globales
«ocsp-update.maxdelay» y «ocsp-update.mindelay».

Siempre que una respuesta OCSP sea actualizada por la tarea de actualización automática o a raíz
de una llamada al comando CLI «update ssl ocsp-response», se emite una línea de registro dedicada.
Sigue un formato dedicado que contiene la cabecera «`<OCSP-UPDATE>`» y va seguida de información
específica relacionada con OCSP: - la ruta del certificado del frontend correspondiente - un
estado numérico de la actualización - un estado textual de la actualización - el número de fallos
de actualización de la respuesta dada - el número de actualizaciones con éxito de la respuesta
dada. Consulta el comando CLI «show ssl ocsp-updates» para una lista completa de códigos y mensajes de
error. Esta línea se emite independientemente del éxito o el fracaso de la actualización de la
respuesta OCSP concernida. La petición/respuesta OCSP se envía y recibe a través de una instancia
http_client que tiene establecida la opción dontlog-normal y que usa el formato de registro HTTP
regular en caso de error (por ejemplo, respondedor OCSP inaccesible). Si se produce tal error, se
emitirá otra línea de registro con información relacionada con HTTP junto a la OCSP «regular»
(que probablemente tendrá «HTTP error» como estado textual). Pero si ocurre un error puramente
HTTP (por ejemplo, respondedor OCSP inaccesible), se emitirá una línea adicional que sigue el
formato de registro HTTP regular. A continuación hay dos ejemplos de tales líneas de registro:
primero una línea de registro de actualización OCSP con éxito y después un ejemplo de error HTTP
con las dos líneas diferentes (las líneas fueron partidas y la URL acortada para mejorar la legibilidad):

```text
<133>Mar  6 11:16:53 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/foo.pem 1 \
        "Update successful" 0 1

<133>Mar  6 11:18:55 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/bar.pem 2 \
        "HTTP error" 1 0
<133>Mar  6 11:18:55 haproxy[14872]: -:- [06/Mar/2023:11:18:52.200] \
        <OCSP-UPDATE> -/- 2/0/-1/-1/3009 503 217 - - SC-- 0/0/0/0/3 0/0 {} \
        "GET http://127.0.0.1:12345/MEMwQT HTTP/1.1"
```

Solución de problemas: un error común que puede producirse con los certificados de Let's Encrypt
es que la resolución DNS proporcione una dirección IPv6 y tu sistema no tenga una ruta IPv6 de
salida válida. En tal caso, puedes crear la ruta apropiada o fijar la opción
«httpclient.resolvers.prefer ipv4» en la sección global. En caso de error «OCSP response check
failure», conviene comprobar que el certificado del emisor que proporcionaste es válido. También
puede mostrarse un mensaje de error más preciso entre paréntesis después del mensaje de error
«genérico». Puede ocurrir con los errores «OCSP response check failure» o «Error during insertion».

<a id="entry-12-7-1-jwt"></a>

**`jwt [ off | on ]`**

```haproxy
jwt [ off | on ]
```

Permite que este certificado se use para la validación o el descifrado JWT mediante los
conversores «jwt_verify_cert», «jwt_decrypt_cert» o «jwt_decrypt» cuando se establece en «on». Su valor por defecto es «off».

Cuando se establece en «on» para un certificado dado, el comando CLI «del ssl cert» no funcionará.
Para poder eliminarse, un certificado no debe estar en uso, ni para los saludos SSL ni para la validación JWT.

Esta opción puede cambiarse en tiempo de ejecución mediante los comandos CLI «add ssl jwt» y «del
ssl jwt». Consulta también el comando CLI «show ssl jwt».

<a id="entry-12-7-1-generate-dummy"></a>

**`generate-dummy [ off | on ]`**

```haproxy
generate-dummy [ off | on ]
```

Permite la generación de una clave privada y de su certificado autofirmado en el momento del
análisis cuando se establece en «on». Esto puede ser útil, por ejemplo, si no se dispone de un
certificado durante la fase de pruebas. En tal caso, «keytype», «bits» y «curves» pueden usarse
para personalizar la clave privada. Cuando no se usa, el valor por defecto es «off». (consulta
también «keytype», «bits» y «curves»).

<a id="entry-12-7-1-keytype"></a>

**`keytype [ RSA | ECDSA ]`**

```haproxy
keytype [ RSA | ECDSA ]
```

Permite seleccionar el tipo de clave privada usado para generar en el momento del análisis un
certificado autofirmado. Este es el caso si «generate-dummy» está en «on» para este certificado.
Cuando no se usa, el valor por defecto es «RSA». (consulta también «generate-dummy»).

<a id="entry-12-7-1-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configura el número de bits para generar un certificado autofirmado RSA cuando «generate-dummy»
está en «on» para este certificado autofirmado y «keytype» está establecido en «RSA». Cuando no se
usa, el valor por defecto es 2048. (consulta también «generate-dummy»).

<a id="entry-12-7-1-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

Configura las curvas cuando «generate-dummy» está en «on» y «keytype» está establecido en «ECDSA»
para este certificado autofirmado. El valor por defecto es «P-384».

## 12.8. ACME {#section-12-8}

acme `<name>`

El protocolo ACME puede configurarse usando la sección «acme». La sección toma un argumento
«`<name>`», que se usa para vincular un certificado a la sección.

La sección ACME permite configurar HAProxy como cliente ACMEv2. Esta característica es
experimental, lo que significa que «expose-experimental-directives» debe estar en la sección global para poder usarla.

Hay una guía disponible en el wiki de HAProxy
<https://github.com/haproxy/wiki/wiki/ACME:--native-haproxy>

Limitaciones actuales: <a id="entry-12-8-the-feature-is"></a>

**`- La funcionalidad está limitada a los desafíos http-01, dns-01 o dns-persist-01`**

```haproxy
- La funcionalidad está limitada a los desafíos http-01, dns-01 o dns-persist-01
```

por ahora. http-01 está completamente gestionado por HAProxy, pero dns-01 y dns-persist-01
necesitan el dataplaneAPI u otra herramienta de terceros para hablar con la API de un proveedor
DNS. dns-persist-01 solo necesita que la entrada TXT se fije una vez, así que puede establecerse manualmente sin herramienta.
<a id="entry-12-8-it-is-possible"></a>

**`- Es posible iniciar sin un certificado existente en el disco. Para`**

```haproxy
- Es posible iniciar sin un certificado existente en el disco. Para
```

ello, el certificado debe configurarse en un crt-store. Al usar la palabra clave «acme» en un
crt-store, se usará un par de claves temporal hasta que se genere el certificado ACME.
<a id="entry-12-8-the-current-haproxy"></a>

**`- La arquitectura actual de HAProxy es un modelo no bloqueante; el acceso al disco`**

```haproxy
- La arquitectura actual de HAProxy es un modelo no bloqueante; el acceso al disco
```

no se supone que se haga después de que la configuración esté cargada, porque podría bloquear el
bucle de eventos, bloqueando el tráfico en el mismo hilo. Esto significa que los certificados y las
claves generados por HAProxy deberán volcarse desde fuera de HAProxy usando «dump ssl cert» en el
socket de estadísticas. Es posible automatizar el volcado de los certificados usando el
dataplaneAPI o el script haproxy-dump-certs proporcionado en el directorio admin/cli/.

El planificador ACME arranca junto con HAProxy; recorrerá los certificados e iniciará una tarea de
renovación ACME cuando el notAfter haya pasado curtime + (notAfter - notBefore) / 12, o 7 días si
notBefore no está definido. Después, el planificador dormirá y despertará al cabo de 12 horas. Es
posible iniciar manualmente una tarea de renovación con «acme renew». Consulta también «acme status»
en la guía de administración.

Las siguientes palabras clave son utilizables en la sección ACME:

<a id="entry-12-8-account-key"></a>

**`account-key <filename>`**

```haproxy
account-key <filename>
```

Configura la ruta a la clave de cuenta. La clave debe generarse antes de lanzar HAProxy. Si no se
usa la palabra clave account, la sección acme intentará cargar un archivo con el nombre de sección
«`<name>`.account.key». Si el archivo no existe, HAProxy generará una, usando los parámetros de la
sección acme.

También puedes generar manualmente una clave privada RSA con openssl:

```text
openssl genrsa -out account.key 2048
```

O una ecdsa:

```text
openssl ecparam -name secp384r1 -genkey -noout -out account.key
```

<a id="entry-12-8-acme-vars"></a>

**`acme-vars <string>`**

```haproxy
acme-vars <string>
```

Pasa variables arbitrarias a la herramienta externa de aprovisionamiento DNS (por ejemplo, el
dataplaneAPI) a través del sink «dpapi». La semántica es específica de cada herramienta; consulta
la documentación de tu herramienta de aprovisionamiento DNS.

Esta palabra clave solo tiene sentido cuando el tipo de desafío es «dns-01» o «dns-persist-01».

Consulta también: «challenge», «provider-name»

<a id="entry-12-8-bits"></a>

**`bits <number>`**

```haproxy
bits <number>
```

Configura el número de bits para generar un certificado RSA. El valor por defecto es 2048.
Establecer un valor demasiado alto puede disparar una advertencia si tu máquina no es lo bastante
potente. (Esto puede configurarse con «warn-blocked-traffic-after», pero bloquear el tráfico demasiado tiempo podría disparar el watchdog.)

<a id="entry-12-8-challenge"></a>

**`challenge <string>`**

```haproxy
challenge <string>
```

Toma como parámetro un tipo de desafío, que debe ser http-01, dns-01 o dns-persist-01. Cuando no
se usa, el valor por defecto es http-01.

dns-persist-01 implementa draft-ietf-acme-dns-persist. A diferencia de dns-01, usa un registro TXT
estático en «\_validation-persist.`<domain>`» que se fija una vez y nunca cambia entre renovaciones.
El registro debe contener el URI de la cuenta y una política opcional. Este tipo de desafío no
requiere acceso de escritura a la API del proveedor DNS en cada renovación.

<a id="entry-12-8-challenge-ready"></a>

**`challenge-ready <value>[,<value>]*`**

```haproxy
challenge-ready <value>[,<value>]*
```

Configura las condiciones que deben cumplirse antes de notificar al servidor ACME que un
desafío dns-01 está listo para validarse. Los valores aceptados son:

```text
cli  - espera a que un operador señale la disponibilidad mediante el comando
       de CLI «acme challenge_ready <crt> domain <domain>» en la CLI master
       o en el socket de estadísticas. Esto permite que una herramienta
       externa de aprovisionamiento DNS confirme que el registro TXT se ha
       establecido antes de que HAProxy continúe.

dns  - realiza una comprobación previa de DNS resolviendo el registro TXT
       de «_acme-challenge.<domain>» mediante la sección de resolutores
       «default» configurada, no los servidores de nombres autoritativos.
       El desafío no se envía hasta que el registro TXT coincida con el
       token esperado. Por ello, los resultados pueden verse afectados por
       la caché de DNS a nivel del resolutor. El retraso entre intentos de
       resolución lo controla «dns-delay». Esta opción es independiente del
       comando CLI, de modo que no se requiere intervención humana.

       Para dns-01, el registro TXT de «_acme-challenge.<domain>» se
       resuelve y debe coincidir con el token esperado. Para
       dns-persist-01, el registro TXT de «_validation-persist.<domain>»
       se resuelve y solo se comprueba su presencia.

delay - aplica una espera inicial de «dns-delay» antes de continuar. Sin
        «dns», el desafío se envía tras expirar el retraso. Cuando se
        combina con «dns», la espera inicial se aplica antes de comenzar
        las comprobaciones previas de DNS.

none - ninguna condición de disponibilidad; el desafío se envía al servidor
       ACME inmediatamente, sin esperar ninguna confirmación externa.
       Esta opción no puede combinarse con otras.
```

Se pueden combinar varios valores con una coma. Cuando se especifican varias condiciones, HAProxy
las procesa en el orden siguiente: primero espera la confirmación por CLI («cli»), luego aplica el
retraso inicial («delay») y después realiza las comprobaciones previas de DNS («dns»).

Esta opción solo es compatible con los tipos de desafío dns-01 y dns-persist-01.

Cuando «challenge» está en «dns-01» y esta opción no está configurada, el valor por defecto es «cli».

Cuando «challenge» está en «dns-persist-01» y esta opción no está configurada, el valor por
defecto es «dns,delay».

Cuando «challenge» está en «dns-persist-01», siempre se realiza una comprobación DNS oportunista
inicial antes de evaluar las condiciones de challenge-ready. Como el registro TXT
«\_validation-persist.`<domain>`» se fija una vez y nunca cambia entre renovaciones, HAProxy
comprueba en el momento de la renovación si el registro ya está presente. Si la comprobación tiene
éxito para todos los dominios, el desafío se envía inmediatamente sin pasar por los pasos de
challenge-ready (cli, delay, dns). Si la comprobación falla, HAProxy retrocede al flujo normal de
challenge-ready.

Ejemplo:

```shell
# Wait for CLI confirmation, then verify DNS propagation
challenge-ready cli,dns
```

<a id="entry-12-8-contact"></a>

**`contact <string>`**

```haproxy
contact <string>
```

El correo electrónico de contacto que se asociará a la clave de cuenta en la CA.

<a id="entry-12-8-curves"></a>

**`curves <string>`**

```haproxy
curves <string>
```

Al usar el keytype ECDSA, configura las curvas. El valor por defecto es P-384.

<a id="entry-12-8-directory"></a>

**`directory <string>`**

```haproxy
directory <string>
```

Esta palabra clave configura la URL del directorio de la CA usada por esta sección acme. Esta
palabra clave es obligatoria, ya que no existe URL por defecto.

Ejemplo:

```text
directory https://acme-staging-v02.api.letsencrypt.org/directory
```

<a id="entry-12-8-dns-delay"></a>

**`dns-delay <time>`**

```haproxy
dns-delay <time>
```

Configura el retraso usado por las condiciones «delay» y «dns» de «challenge-ready». El valor es
un tiempo expresado en el formato de tiempo de HAProxy (por ejemplo, «5m», «300s»). El valor por
defecto es 30 segundos.

Su papel depende de las condiciones «challenge-ready» en uso:

```text
delay     - el desafío se envía tras expirar este retraso, sin ninguna
            comprobación previa de DNS.

dns       - el retraso entre dos intentos consecutivos de resolución DNS.
            La primera sonda se dispara inmediatamente, sin espera inicial.

dns+delay - la espera inicial antes del primer intento de resolución DNS,
            y el retraso entre los reintentos posteriores.
```

Ten en cuenta que la resolución se hace a través de la sección de resolutores «default»
configurada, no de los servidores de nombres autoritativos. Por ello, los resultados pueden seguir
afectados por la caché de DNS a nivel del resolutor.

<a id="entry-12-8-dns-timeout"></a>

**`dns-timeout <time>`**

```haproxy
dns-timeout <time>
```

Cuando «challenge-ready» incluye «dns», configura el tiempo máximo permitido para resolver con
éxito el registro TXT antes de abortar el desafío. El valor es un tiempo expresado en el formato
de tiempo de HAProxy (por ejemplo, «10m», «600s»). El valor por defecto es 600 segundos.

El temporizador arranca en el momento en que se dispara el primer intento de resolución DNS
(después del «dns-delay» inicial). Si el siguiente intento de resolución fuera a iniciarse después de
que el tiempo de espera haya transcurrido, el desafío se aborta con un error. Esto evita un bucle
de reintentos infinito cuando la propagación DNS falla.

Consulta también: «dns-delay»

<a id="entry-12-8-keytype"></a>

**`keytype <string>`**

```haproxy
keytype <string>
```

Configura el tipo de clave que se generará. El valor puede ser «RSA» o «ECDSA». También puedes
configurar las «curves» para ECDSA y el número de «bits» para RSA. Por defecto se generan claves
EC384.

<a id="entry-12-8-map"></a>

**`map <map>`**

```haproxy
map <map>
```

Configura el mapa que se usará para almacenar el token (clave) y la huella digital (valor), lo cual
es útil para responder a un desafío cuando se usan varias cuentas. La tarea acme añadirá entradas
antes de validar el desafío y eliminará las entradas al final de la tarea.

<a id="entry-12-8-profile"></a>

**`profile <string>`**

```haproxy
profile <string>
```

Solicita a la CA un perfil de certificado específico incluyendo un campo «profile» en la petición
newOrder. Esto implementa draft-ietf-acme-profiles.

Los nombres de perfil son identificadores cortos específicos de cada CA (por ejemplo, «classic»,
«shortlived»). Cuando se establece, el nombre del perfil se envía tal cual en la carga útil JSON de
newOrder. La CA puede ignorar la petición o devolver un error si el perfil no está soportado.
Cuando no se establece, no se incluye ningún campo de perfil y la CA usa su política de emisión
por defecto.

Consulta <https://letsencrypt.org/docs/profiles/> para los perfiles de Let's Encrypt.

Ejemplo:

```shell
# Request short-lived certificates
profile shortlived
```

<a id="entry-12-8-provider-name"></a>

**`provider-name <string>`**

```haproxy
provider-name <string>
```

Establece el nombre del proveedor DNS que se pasa a la herramienta externa de aprovisionamiento
DNS (por ejemplo, el dataplaneAPI) a través del sink «dpapi». Los valores aceptados son
específicos de cada herramienta; consulta la documentación de tu herramienta de aprovisionamiento
DNS.

Esta palabra clave solo tiene sentido cuando el tipo de desafío es «dns-01» o «dns-persist-01».

Consulta también: «challenge», «acme-vars»

<a id="entry-12-8-reuse-key"></a>

**`reuse-key { on | off }`**

```haproxy
reuse-key { on | off }
```

Si se establece en «on», HAProxy no generará una nueva clave privada y conservará la anterior. Se
recomienda rotar las claves privadas; al habilitar esta opción se recomienda regenerar
manualmente las claves con regularidad.

Esta opción puede ser útil cuando se usan claves RSA mayores de 2048, que pueden tardar en
generarse y ralentizar el hilo que lo hace.

Usar la misma clave puede ser útil al usar la caché de tu servidor ACME, ya que puede ayudar a
recuperar un certificado válido correspondiente a la clave actual.

El ajuste por defecto es «off».

Ejemplo:

```text
global
    expose-experimental-directives
    httpclient.resolvers.prefer ipv4

frontend in
    bind *:80
    bind *:443 ssl
    http-request return status 200 content-type text/plain lf-string "%[path,field(-1,/)].%[path,field(-1,/),map(virt@acme)]\n" if { path_beg '/.well-known/acme-challenge/' }
    ssl-f-use crt "foo.example.com.pem.rsa"   acme LE1 domains "foo.example.com.pem,bar.example.com"
    ssl-f-use crt "foo.example.com.pem.ecdsa" acme LE2 domains "foo.example.com.pem,bar.example.com"

acme LE1
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype RSA
    bits 2048
    map virt@acme

acme LE2
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype ECDSA
    curves P-384
    map virt@acme
```

<a id="entry-12-8-eab-key-id"></a>

**`eab-key-id <filename>`**

```haproxy
eab-key-id <filename>
```

Configura la ruta al archivo del identificador de clave EAB. La credencial la proporciona la CA y
debe colocarse en la ruta especificada antes de iniciar HAProxy. Se usa únicamente durante la
creación de la cuenta.

El archivo debe contener una cadena ASCII sin formato.

Las credenciales EAB solo son necesarias durante la creación inicial de la cuenta ACME y pueden
eliminarse después, tanto de la configuración como vaciando los archivos. Un archivo vacío se
ignora silenciosamente. Los espacios en blanco no se ignoran, salvo el salto de línea final.

Consulta también: «eab-mac-key», «eab-mac-alg»

<a id="entry-12-8-eab-mac-key"></a>

**`eab-mac-key <filename>`**

```haproxy
eab-mac-key <filename>
```

Configura la ruta al archivo de la clave MAC EAB. La credencial la proporciona la CA y debe
colocarse en la ruta especificada antes de iniciar HAProxy. Se usa únicamente durante la creación
de la cuenta.

El archivo debe contener una clave MAC codificada en base64url.

Las credenciales EAB solo son necesarias durante la creación inicial de la cuenta ACME y pueden
eliminarse después, tanto de la configuración como vaciando los archivos. Un archivo vacío se
ignora silenciosamente. Los espacios en blanco no se ignoran, salvo el salto de línea final.

Consulta también: «eab-key-id», «eab-mac-alg»

<a id="entry-12-8-eab-mac-alg"></a>

**`eab-mac-alg { HS256 | HS384 | HS512 }`**

```haproxy
eab-mac-alg { HS256 | HS384 | HS512 }
```

Configura el algoritmo MAC usado para la firma EAB. El valor por defecto es HS256. La clave MAC
EAB debe ser lo bastante grande para soportar el algoritmo MAC especificado. No todas las CA
soportan algoritmos distintos de HS256.

Consulta también: «eab-key-id», «eab-mac-key»

## 12.9. Comprobaciones de estado {#section-12-9}

Es posible declarar globalmente varias comprobaciones de estado que pueden usar los servidores en
toda la configuración, prevaleciendo sobre la configuración local del proxy.

<a id="entry-12-9-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Crea una nueva comprobación de estado con el nombre `<name>`. Este nombre debe ser único. Debería
usarse en la línea server para referenciar una sección de comprobación de estado específica.

<a id="entry-12-9-type"></a>

**`type <type>`**

```haproxy
type <type>
```

Define el tipo de comprobación de estado. Este parámetro es obligatorio. Se admiten los siguientes
tipos de comprobación de estado:

    * tcp-check
    * httpchk
    * ssl-hello-chk
    * smtpchk
    * pgsql-check
    * redis-check
    * mysql-check
    * ldap-check
    * spop-check

Cada tipo usa los mismos parámetros, si los hay, que la opción correspondiente del proxy. Por
ejemplo, el método, el uri... pueden especificarse para el tipo «httpchk»:

Ejemplos:

```text
   healthcheck my-http-check
type httpchk GET /health HTTP/1.1 %[srv_name]
```

Consulta también: «option tcp-check», «option httpchk», «option ssl-hello-chk», «option smtpchk»,
«option mysql-check», «option pgsql-check», «option redis-check», «option ldap-check» y «option spop-check»

<a id="entry-12-9-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
http-check disable-on-404
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
http-check send-state
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
http-check unset-var(<var-name>)
```

Añade una regla http-check específica para una comprobación de estado «httpchk». Se usa la misma
sintaxis que las directivas correspondientes del proxy. Consulta la documentación correspondiente
del proxy para más detalles.

<a id="entry-12-9-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
tcp-check unset-var(<var-name>)
```

Añade una regla tcp-check específica para una comprobación de estado «tcp-check». Se usa la misma
sintaxis que las directivas correspondientes del proxy. Consulta la documentación correspondiente
del proxy para más detalles.
