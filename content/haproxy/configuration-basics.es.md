---
title: "2. Configuración de HAProxy"
linkTitle: "2. Configuración básica"
weight: 130
description: "Sintaxis de archivos, comillas, variables, condiciones, formatos de tiempo y tamaño, direcciones y ejemplos"
icon: fa-solid fa-file-code
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/configuration-basics/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 2"
---

## 2.1. Formato del archivo de configuración {#section-2-1}

El proceso de configuración de HAProxy involucra 3 fuentes principales de parámetros:

- los argumentos de la línea de comandos, que siempre tienen prioridad
- el archivo o los archivos de configuración, cuyo formato se describe aquí
- el entorno del proceso en ejecución, en caso de que se haga referencia explícita a algunas variables
  de entorno

El archivo de configuración sigue un formato jerárquico bastante simple que obedece a algunas reglas
básicas:

```text
1. un archivo de configuración es una secuencia ordenada de instrucciones

2. una instrucción es una sola línea no vacía antes de cualquier «#» (almohadilla) sin proteger

3. una línea es una serie de tokens o «palabras» delimitados por espacios o
   tabulaciones sin proteger

4. la primera palabra o secuencia de palabras de una línea es una de las
   palabras clave o secuencias de palabras clave listadas en este documento

5. todas las demás palabras son argumentos de la primera; algunas son palabras
   clave conocidas listadas en este documento, otras son valores, referencias
   a otras partes de la configuración o expresiones

6. ciertas palabras clave delimitan una sección dentro de la cual solo se
   soporta un subconjunto de palabras clave

7. una sección termina al final de un archivo o con una palabra clave especial
   que inicia una nueva sección
```

Esto es todo lo que hay que saber para escribir un generador de configuración simple pero fiable, pero
esto no es suficiente para analizar de forma fiable cualquier configuración ni para determinar cómo
tratar ciertos casos límite.

En primer lugar, hay algunas consecuencias de las reglas anteriores. Las reglas 6 y 7 implican que las
palabras clave usadas para definir una nueva sección son válidas en todas partes y no pueden tener un
significado diferente en una sección específica. Estas palabras clave son siempre una sola palabra (en
contraposición a una secuencia de palabras) y, tradicionalmente, la sección que las sigue se designa
usando el mismo nombre. Por ejemplo, al hablar de la «sección global», esto designa la sección de
configuración que sigue a la palabra clave «global». Este uso se emplea mucho en los mensajes de error
para ayudar a localizar las partes que deben corregirse.

Varias secciones crean un objeto interno o un espacio de configuración que requiere distinguirse de los
demás. En este caso tomarán una palabra adicional que establecerá el nombre de esa sección en
particular. Para algunas de ellas el nombre de la sección es obligatorio. Por ejemplo, «frontend foo»
creará una nueva sección de tipo «frontend» llamada «foo». Normalmente un nombre es específico de su
sección y dos secciones de tipos diferentes pueden usar el mismo nombre, pero esto no se recomienda ya
que tiende a complicar la gestión de la configuración.

Una consecuencia directa de la regla 7 es que, cuando se leen varios archivos a la vez, cada uno de
ellos debe comenzar con una nueva sección, y el final de cada archivo terminará una sección. Un archivo
no puede contener subsecciones ni terminar una sección existente y comenzar una nueva.

La regla 1 mencionaba que el orden importa. En efecto, algunas palabras clave crean directivas que
pueden repetirse varias veces para crear secuencias ordenadas de reglas que se aplican en un cierto
orden. Por ejemplo, «tcp-request» puede usarse para alternar reglas «accept» y «reject» según criterios
variados. Como tal, un procesador de archivos de configuración debe conservar siempre el orden de una
sección al editar un archivo. El orden de las secciones normalmente no importa, excepto para la sección
global, que debe colocarse antes que otras secciones, aunque puede repetirse si es necesario. Además,
algunos identificadores automáticos pueden asignarse automáticamente a algunos de los objetos creados
(p. ej., proxies), y al reordenar las secciones sus identificadores cambiarán. Estos aparecen, por
ejemplo, en las estadísticas. Así, la configuración siguiente asignará a «foo» un número de
identificador menor que el de su homólogo «bar». Esto se invertirá si las dos secciones se intercambian:

```text
listen foo
    bind :80

listen bar
    bind :81
```

Otro punto importante es que, según las reglas 2 y 3 anteriores, las líneas vacías, los espacios, las
tabulaciones y los comentarios que siguen a un carácter «#» sin proteger no forman parte de la
configuración, ya que solo se usan como delimitadores. Esto implica que las siguientes configuraciones
son estrictamente equivalentes:

```text
    global#this is the global section
daemon#daemonize
    frontend         foo
mode             http   # or tcp
```

y:

```shell
global
    daemon

# this is the public web frontend
frontend foo
    mode http
```

La práctica habitual consiste en alinear a la izquierda solo la palabra clave que inicia una nueva
sección, y aplicar sangría (es decir, anteponer un carácter de tabulación o unos pocos espacios) a todas
las demás palabras clave, de modo que sea inmediatamente visible que pertenecen a la misma sección (como
se hace en el segundo ejemplo anterior). Colocar comentarios antes de una nueva sección ayuda al lector
a decidir si es la deseada. Dejar una línea en blanco al final de una sección también ayuda
visualmente a detectar el final al editarla.

Las tabulaciones son muy cómodas para la sangría, pero no se copian y pegan bien. Si se usan espacios
en su lugar, se recomienda no colocar demasiados (de 2 a 4) para que la edición sobre el terreno no se
convierta en una carga con editores limitados que no soportan la sangría automática.

En los primeros tiempos era común ver argumentos divididos en posiciones de tabulación fijas porque la
mayoría de las palabras clave no tomaban más de dos argumentos. Con las versiones modernas, que
incorporan expresiones complejas, esta práctica ya no se sostiene y no se recomienda.

## 2.2. Comillas y escape {#section-2-2}

En las configuraciones modernas, algunos argumentos requieren el uso de ciertos caracteres que
anteriormente se consideraban puros delimitadores. Para hacer esto posible, HAProxy soporta el escape
de caracteres anteponiendo una barra invertida ('&#92;') delante del carácter que se va a escapar, el
entrecomillado débil con comillas dobles ("") alrededor de un fragmento de texto y el entrecomillado
fuerte con comillas simples ('') alrededor de un fragmento de texto.

Esto es bastante similar a lo que se hace en varios lenguajes de programación y muy parecido a lo que
se encuentra comúnmente en el shell de Bourne. El principio es el siguiente: mientras el analizador de
configuración corta las líneas en palabras, también se ocupa de las comillas y de las barras invertidas
para decidir si un carácter es un delimitador o es la representación cruda de ese carácter dentro de la
palabra actual. El carácter de escape se elimina, las comillas se eliminan y la palabra restante se usa
tal cual como palabra clave o argumento, por ejemplo.

Si se necesita una barra invertida en una palabra, debe escaparse usando la propia barra (es decir, una
barra invertida doble) o ponerse bajo entrecomillado fuerte.

El escape fuera de las comillas se logra precediendo un carácter especial con una barra invertida
('&#92;'):

```text
\    para marcar un espacio y diferenciarlo de un delimitador
\#   para marcar una almohadilla y diferenciarla de un comentario
\\   para usar una barra invertida
\'   para usar una comilla simple y diferenciarla del entrecomillado fuerte
\"   para usar una comilla doble y diferenciarla del entrecomillado débil
```

Además, algunos caracteres no imprimibles pueden emitirse usando su representación habitual del lenguaje
C:

```text
\n   para insertar un salto de línea (LF, carácter \x0a o ASCII 10 decimal)
\r   para insertar un retorno de carro (CR, carácter \x0d o ASCII 13 decimal)
\t   para insertar una tabulación (carácter \x09 o ASCII 9 decimal)
\xNN para insertar un carácter de código ASCII hexadecimal NN (p. ej. \x0a para LF).
```

El entrecomillado débil se logra rodeando con comillas dobles ("") el carácter o la secuencia de
caracteres que se desea proteger. El entrecomillado débil impide la interpretación de:

```text
     espacio o tabulación como separador de palabras
'    comilla simple como delimitador de entrecomillado fuerte
```

```haproxy
#    almohadilla como inicio de comentario
```

El entrecomillado débil permite la interpretación de las variables de entorno (que no se evalúan fuera
de las comillas) precediéndolas con un signo de dólar ('\$'). Si se necesita un carácter de dólar dentro
de comillas dobles, debe escaparse usando una barra invertida.

El entrecomillado fuerte se logra rodeando con comillas simples ('') el carácter o la secuencia de
caracteres que se desea proteger. Dentro de las comillas simples no se interpreta nada; es la forma
eficiente de entrecomillar expresiones regulares.

En consecuencia, aquí está la matriz que indica cómo pueden introducirse los caracteres especiales en
diferentes contextos (los caracteres no imprimibles se sustituyen por su nombre entre corchetes
angulares). Ten en cuenta que algunos caracteres que solo pueden representarse escapados no tienen
representación posible dentro de las comillas simples, de ahí su ausencia ahí:

```text
   Carácter  |  Sin comillas |       Comillas débiles      | Comillas fuertes
  -----------+---------------+-----------------------------+-----------------
    <TAB>    |  \<TAB>, \x09 |  "<TAB>", "\<TAB>", "\x09"  |  '<TAB>'
  -----------+---------------+-----------------------------+-----------------
    <LF>     |  \n, \x0a     |  "\n", "\x0a"               |
  -----------+---------------+-----------------------------+-----------------
    <CR>     |  \r, \x0d     |  "\r", "\x0d"               |
  -----------+---------------+-----------------------------+-----------------
    <SPC>    |  \<SPC>, \x20 |  "<SPC>", "\<SPC>", "\x20"  |  '<SPC>'
  -----------+---------------+-----------------------------+-----------------
    "        |  \", \x22     |  "\"", "\x22"               |  '"'
  -----------+---------------+-----------------------------+-----------------
    #        |  \#, \x23     |  "#", "\#", "\x23"          |  '#'
  -----------+---------------+-----------------------------+-----------------
    $        |  $, \$, \x24  |  "\$", "\x24"               |  '$'
  -----------+---------------+-----------------------------+-----------------
    '        |  \', \x27     |  "'", "\'", "\x27"          |
  -----------+---------------+-----------------------------+-----------------
    \        |  \\, \x5c     |  "\\", "\x5c"               |  '\'
  -----------+---------------+-----------------------------+-----------------
```

Ejemplo:

```shell
# those are all strictly equivalent:
log-format %{+Q}o\ %t\ %s\ %{-Q}r
log-format "%{+Q}o %t %s %{-Q}r"
log-format '%{+Q}o %t %s %{-Q}r'
log-format "%{+Q}o %t"' %s %{-Q}r'
log-format "%{+Q}o %t"' %s'\ %{-Q}r
```

Existe un caso particular donde puede ser necesario un segundo nivel de entrecomillado o escape.
Algunas palabras clave toman argumentos entre paréntesis, a veces delimitados por comas. Estos
argumentos suelen ser enteros o palabras predefinidas, pero cuando son cadenas arbitrarias, puede ser
necesario realizar un nivel de escape separado para desambiguar los caracteres que pertenecen al
argumento de los caracteres que se usan para delimitar los propios argumentos. Un caso bastante común
es el conversor «regsub». Toma una expresión regular como argumento y, si se necesita un paréntesis de
cierre dentro, este requerirá tener sus propias comillas.

El analizador de argumentos de palabras clave es exactamente el mismo que el del nivel superior en
cuanto a las comillas, con la excepción de que los escapes &#92;#, &#92;\$ y &#92;xNN no se procesan.
Pero lo que no siempre resulta evidente es que los delimitadores usados dentro deben escaparse o
entrecomillarse primero para que no se resuelvan en el nivel superior.

Tomemos este ejemplo que hace uso del conversor «regsub», que toma 3 argumentos: una expresión
regular, una cadena de reemplazo y un conjunto de indicadores:

```shell
# replace all occurrences of "foo" with "blah" in the path:
http-request set-path %[path,regsub(foo,blah,g)]
```

Aquí no fue necesario ningún entrecomillado especial. Pero si ahora queremos reemplazar «foo» o «bar»
por «blah», necesitaremos la expresión regular «(foo\|bar)». No podemos escribir:

```text
http-request set-path %[path,regsub((foo|bar),blah,g)]
```

porque nos gustaría que la cadena se cortara de esta manera:

```text
    http-request set-path %[path,regsub((foo|bar),blah,g)]
                                       |---------|----|-|
                                 arg1 _/         /    /
                                 arg2 __________/    /
                                 arg3 ______________/
```

pero en realidad lo que se pasa es una cadena entre el paréntesis de apertura y el de cierre, seguida
de basura:

```text
    http-request set-path %[path,regsub((foo|bar),blah,g)]
                                       |--------|--------|
                        arg1=(foo|bar _/        /
                     basura al final  _________/
```

La solución obvia aquí parece ser que el paréntesis de cierre necesita entrecomillarse, pero por sí
solo esto no funcionará, porque, como se mencionó anteriormente, las comillas son procesadas por el
analizador del nivel superior, que las resolverá antes de procesar esta palabra:

```text
http-request set-path %[path,regsub("(foo|bar)",blah,g)]
------------ -------- ----------------------------------
   pal.1       pal.2    pal.3=%[path,regsub((foo|bar),blah,g)]
```

Así que no cambiamos nada para el analizador de argumentos del segundo nivel, que sigue viendo una
expresión regular truncada como único argumento, y basura al final de la cadena. Al escapar las
comillas, estas se pasarán sin modificación al segundo nivel:

```text
    http-request set-path %[path,regsub(\"(foo|bar)\",blah,g)]
    ------------ -------- ------------------------------------
       pal.1       pal.2    pal.3=%[path,regsub("(foo|bar)",blah,g)]
                                                |---------||----|-|
                                arg1=(foo|bar) _/          /    /
                                    arg2=blah  ___________/    /
                                        arg3=g _______________/
```

Otro enfoque consiste en usar comillas simples fuera de toda la cadena y comillas dobles dentro (para
que las comillas dobles no se eliminen de nuevo):

```text
    http-request set-path '%[path,regsub("(foo|bar)",blah,g)]'
    ------------ --------  ----------------------------------
       pal.1       pal.2    pal.3=%[path,regsub("(foo|bar)",blah,g)]
                                                |---------||----|-|
                                arg1=(foo|bar) _/          /    /
                                          arg2 ___________/    /
                                          arg3 _______________/
```

Pero en este caso es importante notar que los delimitadores incrustados en la cadena de nivel superior
permanecen como caracteres puros y ya no son delimitadores. En particular, esto significa que los
espacios y las tabulaciones alrededor de las comas forman parte de la cadena. El ejemplo siguiente es
incorrecto en varios puntos:

```text
    http-request set-path '%[path, regsub("(foo|bar)", blah, g)]'
    ------------ --------  --------------------------------------
       pal.1       pal.2    pal.3=%[path, regsub("(foo|bar)", blah, g)]
                                        |--------|---------||-----|--|
                       conversor=" regsub" _/        /         /   /
                                    arg1=(foo|bar) _/         /   /
                                     arg2=" blah" ___________/   /
                                        arg3=" g" ______________/
```

El simple hecho de rodear las comas con espacios hizo que esos espacios formaran parte del propio
campo, de ahí el conversor « regsub» (que comienza con un espacio), que no se encontrará y
desencadenará un error, pero de manera más sutil, la cadena de reemplazo « blah» insertará un espacio
en la salida. Una buena regla general es no insertar nunca espacios innecesarios dentro de las
expresiones.

Al usar expresiones regulares, puede ocurrir que el carácter de dólar ('\$') aparezca en la expresión o
que una barra invertida ('&#92;') se use en la cadena de reemplazo. En este caso, estos también se
procesarán dentro de las comillas dobles; por ello se prefieren las comillas simples (o el doble
escape). Ejemplo:

```text
    http-request set-path '%[path,regsub("^/(here)(/|$)","my/\1",g)]'
    ------------ --------  -----------------------------------------
       pal.1       pal.2    pal.3=%[path,regsub("^/(here)(/|$)","my/\1",g)]
                                                |-------------| |-----||-|
                              arg1=(here)(/|$) _/               /      /
                                    arg2=my/\1 ________________/      /
                                          arg3 ______________________/
```

Recuerda que las barras invertidas no son caracteres de escape dentro de las comillas simples y que
toda la palabra anterior ya está protegida contra ellas gracias a las comillas simples. Por el
contrario, si se hubieran usado comillas dobles alrededor de toda la expresión, el carácter de dólar y
las barras invertidas se habrían resuelto en el nivel superior, rompiendo el contenido del argumento
en el segundo nivel.

Desafortunadamente, dado que las comillas simples no pueden escaparse dentro del entrecomillado
fuerte, si necesitas incluir comillas simples en tu argumento, tendrás que escaparlas o
entrecomillarlas dos veces. Hay algunas formas de hacerlo:

```text
http-request set-var(txn.foo) str("\\'foo\\'")
http-request set-var(txn.foo) str(\"\'foo\'\")
http-request set-var(txn.foo) str(\\\'foo\\\')
```

En caso de duda, simplemente no uses comillas en ninguna parte, y comienza a colocar comillas simples
o dobles alrededor de los argumentos que requieran una coma o un paréntesis de cierre, y piensa en
escapar esas comillas usando una barra invertida si la cadena contiene un dólar o una barra invertida.
Una vez más, esto es bastante similar a lo que se usa bajo un shell de Bourne al realizar un doble
escape de un comando pasado a «eval». Para los autores de API, lo mejor probablemente sea colocar
comillas escapadas alrededor de cada argumento, sin importar su contenido. Los usuarios probablemente
encontrarán que usar comillas simples alrededor de toda la expresión y comillas dobles alrededor de
cada argumento proporciona configuraciones más legibles.

## 2.3. Variables de entorno {#section-2-3}

La configuración de HAProxy soporta variables de entorno. Estas variables se interpretan solo dentro
de comillas dobles. Las variables se expanden durante el análisis de la configuración. Los nombres de
variables deben ir precedidos de un dólar ("\$") y, opcionalmente, encerrados entre llaves ("{}"), de
manera similar a lo que se hace en el shell de Bourne. Los nombres de variables pueden contener
caracteres alfanuméricos o el carácter de subrayado ("\_") pero no deben comenzar por un dígito. Si la
variable contiene una lista de varios valores separados por espacios, puede expandirse como argumentos
individuales encerrando la variable entre llaves y añadiendo el sufijo '[\*]' antes de la llave de
cierre. También es posible especificar un valor por defecto que se usará cuando la variable no esté
definida, añadiendo ese valor después de un guion '-' junto al nombre de la variable. Ten en cuenta
que el valor por defecto solo sustituye a las variables no existentes, no a las vacías.

Ejemplo:

```text
bind "fd@${FD_APP1}"

log "${LOCAL_SYSLOG-127.0.0.1}:514" local0 notice  # send to local server

user "$HAPROXY_USER"
```

Algunas variables están definidas por HAProxy y pueden usarse en el archivo de configuración. Estas
variables se listan en la matriz siguiente y se clasifican en cuatro categorías:

- utilizable: la variable es accesible desde la configuración, ya sea para resolverse tal cual, o para
  usarse dentro de bloques condicionales o predicados para activar o desactivar algunos fragmentos de
  configuración, como se describe en la [sección 2.4](/es/haproxy/configuration-basics/#section-2-4)
  «Bloques condicionales».

- modificable: la variable puede redefinirse o eliminarse en la configuración mediante las palabras
  clave «setenv»/«unsetenv».

- listada: la variable aparece en la salida del comando «show env» de la CLI, descrito en la
  [sección 9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) «Comandos de sockets Unix» de la
  guía de gestión.

También existen dos subcategorías, «master» y «worker», marcadas respectivamente con «M» y «W» en la
tabla siguiente, que muestran las diferencias entre los dos procesos cuando HAProxy se lanza en modo
master-worker.

- master: la variable está definida y es accesible desde el proceso master. Por lo tanto, aparecerá en
  la salida «show env» de la CLI del master y puede usarse en bloques condicionales o directivas para
  activar algunos ajustes especiales para el master (consulta los ejemplos en la
  [sección 2.4](/es/haproxy/configuration-basics/#section-2-4) «Bloques condicionales»).

- worker: la variable está definida y es accesible desde el proceso worker. Aparecerá en el «show env»
  de la CLI del worker (o en el «@1 show env» de la CLI del master) y también puede condicionar
  algunos parámetros del proceso worker (consulta los ejemplos de la
  [sección 2.4](/es/haproxy/configuration-basics/#section-2-4) «Bloques condicionales»).

En modo autónomo (sin la opción «-W» ni la palabra clave «master-worker») el proceso se comporta como
un worker, excepto por las variables «HAPROXY_MASTER_CLI» y «HAPROXY_MWORKER», que no están definidas.

Algunas variables están marcadas como no utilizables y no modificables:

- HAPROXY_CFGFILES
- HAPROXY_MWORKER
- HAPROXY_CLI
- HAPROXY_MASTER_CLI
- HAPROXY_LOCALPEER

Sus valores están sin definir durante el análisis de la configuración; se establecen más tarde,
durante la inicialización. Por lo tanto, se recomienda no usar estas variables dentro de bloques
condicionales y no referenciarlas en las palabras clave «setenv»/«resetenv»/«unsetenv» de la sección
global.

La tabla siguiente resume el estado de cada variable para los diferentes modos de funcionamiento:

```text
  +---------------------------+---------+------------+-----------+
  |          variable         | utiliz. |modificable |  listada  |
  |                           +---------+------------+-----------+
  |                           |  M | W  |   M  |  W  |  M  |  W  |
  +---------------------------+----+----+------+-----+-----+-----+
  | HAPROXY_STARTUP_VERSION   |  X | X  |      |     |  X  |  X  |
  | HAPROXY_BRANCH            |  X | X  |      |     |  X  |  X  |
  | HAPROXY_CFGFILES          |    |    |      |     |  X  |  X  |
  | HAPROXY_MWORKER           |    |    |      |     |  X  |  X  |
  | HAPROXY_CLI               |    |    |      |     |     |  X  |
  | HAPROXY_MASTER_CLI        |    |    |      |     |  X  |     |
  | HAPROXY_LOCALPEER         |    | X  |      |     |     |  X  |
  | HAPROXY_HTTP_LOG_FMT      |    | X  |      |  X  |     |     |
  | HAPROXY_HTTP_CLF_LOG_FMT  |    | X  |      |  X  |     |     |
  | HAPROXY_HTTPS_LOG_FMT     |    | X  |      |  X  |     |     |
  | HAPROXY_TCP_LOG_FMT       |    | X  |      |  X  |     |     |
  | HAPROXY_TCP_CLF_LOG_FMT   |    | X  |      |  X  |     |     |
  | HAPROXY_KEYLOG_FC_LOG_FMT |    | X  |      |  X  |     |     |
  | HAPROXY_KEYLOG_BC_LOG_FMT |    | X  |      |  X  |     |     |
  +---------------------------+----+----+------+-----+-----+-----+
```

Las variables en cuestión son las siguientes:

- HAPROXY_LOCALPEER: definida al inicio del proceso, contiene el nombre del par local. (Consulta «-L» en
  la guía de gestión.)

- HAPROXY_CFGFILES: lista de los archivos de configuración cargados por HAProxy, separados por puntos
  y coma. Puede ser útil en el caso de que hayas especificado un directorio.

- HAPROXY_HTTP_LOG_FMT: contiene el valor del formato de registro HTTP por defecto tal como se define
  en la [sección 8.2.3](/es/haproxy/configuration-logging/#section-8-2-3) «Formato de registro HTTP».
  Puede usarse para sobrescribir el formato de registro por defecto sin tener que copiar toda la
  definición original.

- HAPROXY_HTTP_CLF_LOG_FMT: contiene el valor del formato de registro HTTP CLF por defecto tal como se
  define en la [sección 8.2.3](/es/haproxy/configuration-logging/#section-8-2-3) «Formato de registro
  HTTP». Puede usarse para sobrescribir el formato de registro por defecto sin tener que copiar toda
  la definición original.

Ejemplo:

```shell
# Add the rule that gave the final verdict to the log
log-format "${HAPROXY_TCP_LOG_FMT} lr=%[last_rule_file]:%[last_rule_line]"
```

- HAPROXY_HTTPS_LOG_FMT: similar a HAPROXY_HTTP_LOG_FMT pero para el formato de registro HTTPS tal
  como se define en la [sección 8.2.4](/es/haproxy/configuration-logging/#section-8-2-4) «Formato de
  registro HTTPS».

- HAPROXY_TCP_LOG_FMT: similar a HAPROXY_HTTP_LOG_FMT pero para el formato de registro TCP tal como
  se define en la [sección 8.2.2](/es/haproxy/configuration-logging/#section-8-2-2) «Formato de
  registro TCP».

- HAPROXY_TCP_CLF_LOG_FMT: similar a HAPROXY_HTTP_CLF_LOG_FMT pero para el formato de registro TCP
  CLF tal como se define en la [sección 8.2.2](/es/haproxy/configuration-logging/#section-8-2-2)
  «Formato de registro TCP».

- HAPROXY_KEYLOG_FC_LOG_FMT: contiene el formato de registro de claves para la conexión TLS del
  frontend (orientada al cliente), con las entradas de claves separadas por saltos de línea, por lo
  que podría no ser compatible con tu servidor syslog. Se requiere «tune.ssl.keylog on».

- HAPROXY_KEYLOG_BC_LOG_FMT: similar a HAPROXY_KEYLOG_FC_LOG_FMT pero para la conexión TLS del backend
  (orientada al servidor). Las entradas de claves están separadas por saltos de línea, por lo que
  podría no ser compatible con tu servidor syslog. Se requiere «tune.ssl.keylog on».

- HAPROXY_MWORKER: en modo master-worker, esta variable se establece a 1.

- HAPROXY_CLI: direcciones de las escuchas configuradas del socket de estadísticas de cada proceso,
  separadas por puntos y coma.

- HAPROXY_MASTER_CLI: en modo master-worker, direcciones de las escuchas de la CLI del master,
  separadas por puntos y coma.

- HAPROXY_STARTUP_VERSION: contiene la versión usada para el inicio; en modo master-worker es la
  versión que se usó para iniciar el master, incluso después de actualizar el binario y recargar.

- HAPROXY_BRANCH: contiene la versión de la rama de HAProxy (por ejemplo «2.8»). No contiene el
  número de versión completo. Puede ser útil en caso de migración si los recursos (como mapas o
  certificados) están en una ruta que contiene el número de rama.

Además, algunas pseudovariables se resuelven internamente y pueden usarse como variables regulares.
Las pseudovariables siempre comienzan con un punto («.») y son las únicas donde el punto está
permitido. La lista actual de pseudovariables es:

- .FILE: el nombre del archivo de configuración que se está analizando actualmente.

- .LINE: el número de línea del archivo de configuración que se está analizando actualmente,
  comenzando en uno.

- .SECTION: el nombre de la sección que se está analizando actualmente, o su tipo si la sección no
  tiene nombre (p. ej. «global»), o una cadena vacía antes de la primera sección.

Estas variables se resuelven en la ubicación donde se analizan. Por ejemplo, si una variable «.LINE»
se usa en una directiva «log-format» situada en una sección defaults, su número de línea se resolverá
antes de analizar y compilar la directiva «log-format», de modo que este mismo número de línea será
reutilizado por los proxies posteriores.

De esta forma es posible emitir información que ayude a localizar una regla en variables, registros,
estados de error, comprobaciones de estado, valores de cabecera, o incluso usar números de línea para
nombrar algunos objetos de configuración, como servidores, por ejemplo.

## 2.4. Bloques condicionales {#section-2-4}

A veces puede resultar práctico poder activar o desactivar condicionalmente algunas partes
arbitrarias de la configuración, por ejemplo para activar/desactivar SSL o los cifrados, activar o
desactivar algunas escuchas de preproducción sin modificar la configuración, o ajustar la sintaxis de
la configuración para soportar dos versiones distintas de HAProxy durante una migración. HAProxy
aporta un conjunto de directivas anidables similares a las de un preprocesador que permiten integrar
o ignorar algunos bloques de texto. Estas directivas deben colocarse en su propia línea y actúan
sobre las líneas que las siguen. Dos de ellas admiten una expresión; las demás solo cambian a un
bloque alternativo o terminan un nivel actual. Las 4 directivas siguientes se definen para formar
bloques condicionales:

- .if `<condition>`
- .elif `<condition>`
- .else
- .endif

La directiva «.if» anida un nuevo nivel, «.elif» permanece en el mismo nivel, «.else» también, y
«.endif» cierra un nivel. Cada «.if» debe terminarse con un «.endif» correspondiente. La directiva
«.elif» solo puede colocarse después de «.if» o «.elif», y no hay límite en el número de «.elif» que
pueden encadenarse. Solo puede haber un «.else» por «.if» y siempre debe ir después del «.if» o del
último «.elif» de un bloque.

Los comentarios pueden colocarse en la misma línea si es necesario, después de un «#»; se
ignorarán. Las directivas se tokenizan como las demás directivas de configuración y, como tal, es
posible usar variables de entorno en las condiciones.

Las condiciones también pueden evaluarse al inicio con el parámetro -cc. Consulta «3. Inicio de
HAProxy» en la documentación de gestión.

Las condiciones son una cadena vacía (que entonces devuelve false) o una expresión formada por
cualquier combinación de:

- el entero cero ('0'), siempre devuelve «false»
- un entero no nulo (p. ej. '1'), siempre devuelve «true».
- un predicado seguido opcionalmente de argumento(s) entre paréntesis.
- una condición colocada entre un par de paréntesis '(' y ')'
- un signo de exclamación ('!') que precede a cualquiera de los elementos no vacíos anteriores, y
  que negará su estado.
- expresiones combinadas con un Y lógico ('&&'), que se evaluarán de izquierda a derecha hasta que
  una devuelva false
- expresiones combinadas con un O lógico ('\|\|'), que se evaluarán de derecha a izquierda hasta que
  una devuelva true

Se usan el mismo tokenizador de líneas y el mismo analizador de argumentos que para el resto del
lenguaje de configuración. Las palabras se dividen alrededor de series consecutivas de uno o más
espacios o tabulaciones sin entrecomillar, y se reensamblan usando un solo espacio para delimitarlas
antes de la evaluación, para ahorrar al usuario tener que entrecomillar toda la línea. Pero esto
también significa que los espacios que rodean las comas o los paréntesis definitivamente forman
parte del valor, lo que no siempre se espera. Por ejemplo, la expresión siguiente:

```text
.if defined( HAPROXY_MWORKER )
```

comprobará la existencia de la variable " HAPROXY_MWORKER " (con espacios), y esta:

```text
.if streq("$ENABLE_SSL",     1)
```

comparará la variable de entorno "ENABLE_SSL" con el valor " 1" (con un solo espacio inicial). La
razón es que la línea primero se divide en palabras así:

```text
   .if streq("$ENABLE_SSL",     1)
  |---|--------------------|   |--|
    1           2               3
```

luego se aplica el entrecomillado débil y la variable de entorno "\$ENABLE_SSL" se resuelve (digamos
por ejemplo que ENABLE_SSL=0), y finalmente las palabras se reensamblan en una sola cadena colocando
un solo espacio entre las palabras:

```text
   .if streq(0, 1)
  |---|-------|--|
    1     2     3
```

y solo entonces se analiza como una expresión única. El espacio que se insertó entre la coma y "1"
sigue formando parte del valor del argumento, haciendo que este argumento sea " 1":

```text
   .if streq(0, 1)
  |---|-----|-|--|
    \    \    \  \_ argumento2: " 1"
     \    \    \___ argumento1: "0"
      \    \_______ función: "streq"
       \___________ directiva: ".if"
```

Aquí se ve que, incluso si ENABLE_SSL hubiera sido igual a "1", no habría coincidido con " 1" ya que
la cadena diferiría en un espacio.

Nota: como se explica en la sección «2.2. Comillas y escape», una buena regla general es no insertar
nunca espacios innecesarios dentro de las expresiones.

Ten en cuenta que, como en otros lenguajes, el operador Y tiene precedencia sobre el operador O, de
modo que "A && B \|\| C && D" se evalúa como "(A && B) \|\| (C && D)".

La lista de predicados actualmente soportados es la siguiente:

- awslc_api_atleast(`<ver>`): devuelve true si el número de API awslc actual es al menos tan reciente
  como `<ver>`, en caso contrario false. Ejemplo: awslc_api_atleast(35)

- awslc_api_before(`<ver>`): devuelve true si el número de API awslc actual es estrictamente anterior
  a `<ver>`, en caso contrario false. Ejemplo: awslc_api_before(26)

- defined(`<name>`) : devuelve true si existe una variable de entorno `<name>`, independientemente de
  su contenido

- feature(`<name>`) : devuelve true si la característica `<name>` figura como presente en la lista de
  características reportada por «haproxy -vv» (lo que significa que un `<name>` aparece después de
  un «+»)

- openssl_version_atleast(`<ver>`): devuelve true si la versión actual de OpenSSL es al menos tan
  reciente como `<ver>`, en caso contrario false. Bibliotecas como LibreSSL, AWS-LC y WolfSSL
  también proporcionan una pseudo-versión de OpenSSL. Ejemplo:

```text
ssllib_name_startswith(OpenSSL) && openssl_version_atleast(1.1.1)
```

- openssl_version_before(`<ver>`): devuelve true si la versión actual de OpenSSL es estrictamente
  anterior a `<ver>`, en caso contrario false. Bibliotecas como LibreSSL, AWS-LC y WolfSSL también
  proporcionan una pseudo-versión de OpenSSL. Ejemplo: openssl_version_before(3.5.0)

- ssllib_name_startswith(`<name>`) : devuelve true si el nombre de la biblioteca SSL con la que
  HAProxy fue enlazado comienza por `<name>`. Ejemplo: ssllib_name_startswith(wolfSSL)

- streq(`<str1>`,`<str2>`) : devuelve true solo si las dos cadenas son iguales

- strneq(`<str1>`,`<str2>`): devuelve true solo si las dos cadenas difieren

- strstr(`<str1>`,`<str2>`): devuelve true solo si la segunda cadena se encuentra en la primera.

- version_atleast(`<ver>`): devuelve true si la versión actual de haproxy es al menos tan reciente
  como `<ver>`, en caso contrario false. La sintaxis de la versión es la misma que muestra
  «haproxy -v» y las componentes que falten se asumen como cero.

- version_before(`<ver>`): devuelve true si la versión actual de haproxy es estrictamente anterior a
  `<ver>`, en caso contrario false. La sintaxis de la versión es la misma que muestra «haproxy -v»
  y las componentes que falten se asumen como cero.

- enabled(`<opt>`) : devuelve true si la opción `<opt>` está activada en tiempo de ejecución. Solo
  se soporta un subconjunto de opciones:

```text
POLL, EPOLL, KQUEUE, EVPORTS, SPLICE,
GETADDRINFO, REUSEPORT, FAST-FORWARD,
SERVER-SSL-VERIFY-NONE
```

Ejemplo:

```haproxy
# 1. HAPROXY_MWORKER variable is set automatically by HAProxy in master and
# in worker process environments (see HAProxy variables matrix from
# 2.3. Environment variables). Its presence enables an additional listener.

global
  master-worker

.if defined(HAPROXY_MWORKER)
    listen mwcli_px
       bind :1111
       ...
.endif
```

```haproxy
# 2. HAPROXY_BRANCH is set automatically by HAProxy in master and in worker
# process environments (see HAProxy variables matrix from 2.3. Environment
# variables). We check HAPROXY_BRANCH value and conditionally enable
# mworker-max-reloads parameter.

global
  master-worker

.if streq("$HAPROXY_BRANCH",3.1)
     mworker-max-reloads 5
.endif
```

```haproxy
# 3. Some arbitrary environment variables are set by user in the global
# section. If HAProxy is started in master-worker mode, they are presented in
# master and in worker process environments. We check values of these
# variables and conditionally enable ports 80 and 443. Environment variables
# checks can be mixed with features and version checks.

global
  setenv WITH_SSL yes
  unsetenv SSL_ONLY

.if strneq("$SSL_ONLY",yes)
       bind :80
.endif

.if streq("$WITH_SSL",yes)
  .if feature(OPENSSL)
       bind :443 ssl crt ...
  .endif
.endif

.if feature(OPENSSL) && (streq("$WITH_SSL",yes) || streq("$SSL_ONLY",yes))
       bind :443 ssl crt ...
.endif

.if version_atleast(2.4-dev19)
    profiling.memory on
.endif

.if !feature(OPENSSL)
    .alert "SSL support is mandatory"
.endif
```

Cuatro directivas más se proporcionan para informar de algún estado:

- .diag "message" : emite este mensaje solo en modo diagnóstico (-dD)
- .notice "message" : emite este mensaje al nivel NOTICE
- .warning "message": emite este mensaje al nivel WARNING
- .alert "message" : emite este mensaje al nivel ALERT

Los mensajes emitidos al nivel WARNING pueden provocar que el proceso no arranque si «zero-warning»
está activado. Los mensajes emitidos al nivel ALERT siempre provocarán un error fatal. Estas
directivas pueden usarse para detectar algunas condiciones inapropiadas y proporcionar consejos al
usuario.

Ejemplo:

```text
.if "${A}"
  .if "${B}"
     .notice "A=1, B=1"
  .elif "${C}"
     .notice "A=1, B=0, C=1"
  .elif "${D}"
     .warning "A=1, B=0, C=0, D=1"
  .else
     .alert "A=1, B=0, C=0, D=0"
  .endif
.else
     .notice "A=0"
.endif

.diag "WTA/2021-05-07: replace 'redirect' with 'return' after switch to 2.4"
      http-request redirect location /goaway if ABUSE
```

## 2.5. Formato de tiempo {#section-2-5}

Algunos parámetros involucran valores que representan tiempo, como los tiempos de espera. Estos
valores generalmente se expresan en milisegundos (salvo indicación expresa en contrario) pero pueden
expresarse en cualquier otra unidad añadiendo la unidad como sufijo al valor numérico. Es importante
tenerlo en cuenta porque no se repetirá para cada palabra clave. Las unidades soportadas son:

- us: microsegundos. 1 microsegundo = 1/1000000 segundo
- ms: milisegundos. 1 milisegundo = 1/1000 segundo. Esta es la unidad por defecto.
- s : segundos. 1s = 1000ms
- m : minutos. 1m = 60s = 60000ms
- h : horas. 1h = 60m = 3600s = 3600000ms
- d : días. 1d = 24h = 1440m = 86400s = 86400000ms

## 2.6. Formato de tamaño {#section-2-6}

Algunos parámetros involucran valores que representan un tamaño, como los límites de ancho de banda.
Estos valores generalmente se expresan en bytes (salvo indicación expresa en contrario) pero pueden
expresarse en cualquier otra unidad añadiendo la unidad como sufijo al valor numérico. Es importante
tenerlo en cuenta porque no se repetirá para cada palabra clave. Las unidades soportadas no
distinguen mayúsculas de minúsculas:

- k: kilobytes. 1 kilobyte = 1024 bytes
- m: megabytes. 1 megabyte = 1048576 bytes
- g: gigabytes. 1 gigabyte = 1073741824 bytes

Tanto el formato de tiempo como el de tamaño requieren enteros; la notación decimal no está
permitida.

## 2.7. Formato de nombre para mapas y ACL {#section-2-7}

Es posible usar una lista de patrones para mapas o ACL. Una lista de patrones se identifica por su
nombre y puede usarse en diferentes lugares de la configuración. Las listas de patrones se dividen
en tres categorías según el formato del nombre:

- Listas de patrones basadas en archivos regulares: es el caso por defecto. El nombre del archivo,
  absoluto o relativo, se usa como nombre. El archivo debe existir, de lo contrario se desencadena un
  error. Pero puede estar vacío. El prefijo «file@» también puede especificarse, pero no forma parte
  del nombre que identifica la lista. Un nombre de archivo, con o sin el prefijo, referencia la misma
  lista de patrones.

- Listas de patrones basadas en archivos opcionales: el nombre del archivo debe ir precedido del
  prefijo «opt@». La existencia del archivo es opcional. Si el archivo existe, su contenido se carga,
  pero no se reporta ningún error si no existe. El prefijo no forma parte del nombre que identifica
  la lista. Esto significa que, para un nombre de archivo dado, los archivos opcionales y los
  archivos regulares referencian la misma lista de patrones.

- Listas de patrones basadas en archivos virtuales: el nombre es solo un identificador. No es una
  referencia a ningún archivo. Debe usarse el prefijo «virt@». Forma parte del nombre. Por lo tanto,
  no puede mezclarse con otro tipo de listas.

Los archivos virtuales son útiles cuando los patrones se gestionan completamente de forma dinámica,
sin patrones al inicio ni al recargar. Los archivos opcionales pueden usarse en las mismas
condiciones. Pero los patrones pueden volcarse en el archivo, mediante un script externo basado en el
comando CLI «show map», por ejemplo. De esta forma, es posible conservar los patrones al recargar.

Nota: aunque es improbable, esto significa que ningún archivo regular que comience por «file@»,
«opt@» o «virt@» puede cargarse, excepto añadiendo «./» explícitamente delante del nombre del
archivo (por ejemplo «file@./virt@map»).

## 2.8. Variables {#section-2-8}

En la configuración de HAProxy, las variables pueden usarse en funciones de extracción de muestras,
conversores, cadenas log-format o acciones TCP/HTTP. Pueden definirse variables de ámbito de
proceso, accesibles globalmente durante toda la vida del proceso. Algunas otras tienen una vida más
corta. Las variables son similares a las que se encuentran en los scripts de shell. Es un nombre
simbólico para un bloque de memoria. El tamaño de las variables no está limitado y se asigna
dinámicamente. Por ello deben usarse con precaución, especialmente en un uso intensivo. Sin
embargo, es posible limitar la cantidad máxima de memoria usada por las variables configurando los
parámetros globales «tune.vars».

Las variables deben designarse usando el formato «`<scope>`.`<name>`». El `<scope>` es una sola
palabra que indica el tiempo de vida de la variable. La parte `<name>`, dentro de un ámbito, solo
puede contener los caracteres «a-z», «A-Z», «0-9» y «\_». Es única en ese ámbito, pero el mismo
nombre en ámbitos diferentes puede usarse y referirse a variables diferentes. Los ámbitos
soportados son:

- proc : para variables conocidas durante toda la vida del proceso y accesibles globalmente. Las
  variables «proc» pueden manipularse desde la CLI usando los comandos «get var» y «set var».
  También pueden establecerse desde secciones «global» mediante las directivas «set-var» y
  «set-var-fmt».

- sess : para variables conocidas durante toda la vida de una sesión. Las variables «sess» son
  privadas de una sesión, no visibles desde fuera de ella y no se comparten con otras sesiones.

- txn : para variables conocidas durante toda la vida de una transacción. Las variables «txn» son
  privadas de un flujo, no visibles desde fuera de él y no se comparten con otros flujos.

- req : para variables conocidas durante el procesamiento de la solicitud de un flujo específico.
  Las variables «req» son visibles desde la creación del flujo y hasta el primer intento de
  conexión al servidor. Son privadas de un flujo, no visibles desde fuera de él y no se comparten
  con otros flujos. No hay ningún solapamiento entre las variables «req» y «res».

- res : para variables conocidas durante el procesamiento de la respuesta de un flujo específico.
  Las variables «res» son visibles desde el primer intento de conexión al servidor y hasta la
  destrucción del flujo. Son privadas de un flujo, no visibles desde fuera de él y no se comparten
  con otros flujos. No hay ningún solapamiento entre las variables «req» y «res».

- check: para variables conocidas durante la ejecución de una comprobación de estado. Las variables
  «check» son privadas de una comprobación de estado, no visibles desde fuera de ella y no se
  comparten con otras comprobaciones de estado. Pueden establecerse usando las directivas dedicadas
  «tcp-check» o «http-check».

Según el contexto, pueden usarse ámbitos adicionales que referencian al padre de un flujo actual:

- psess: igual que «sess» pero usando la sesión del flujo padre, si existe.

- ptxn : igual que «txn» pero usando la transacción del flujo padre, si existe.

- preq : igual que «req» pero usando el flujo padre, si existe. Las variables «preq» solo son
  accesibles durante el procesamiento de la solicitud del flujo padre.

- pres : igual que «res» pero usando el flujo padre, si existe. Las variables «pres» solo son
  accesibles durante el procesamiento de la respuesta del flujo padre.

Los ámbitos que referencian el flujo padre son utilizables desde el momento en que este queda
definido. La mayoría de las veces no hay flujo padre. Pero, si aplica, esto se especificará
explícitamente. Por ahora, solo es posible recuperar el valor de las variables definidas en un
ámbito del flujo padre. No es posible establecer ni eliminar tales variables. Normalmente, un flujo
hijo realiza algún procesamiento para el padre en un momento preciso y le impide avanzar hasta que
se completa la operación que realiza. Esto significa que el padre puede quedar detenido en medio del
procesamiento de una solicitud o de una respuesta, por ejemplo. Como tal, ciertos ámbitos no
estarán disponibles desde el flujo hijo. Por ejemplo, si una solicitud se somete a algún análisis
realizado por un flujo hijo, este flujo hijo no encontrará ninguna variable en el ámbito «pres»,
ya que el padre no está procesando una respuesta y, por lo tanto, no tiene ninguna variable en su
ámbito «res».

El contenido de una variable es el resultado de la evaluación de una expresión de extracción de
muestra y hereda el tipo de salida de esa expresión. Es importante cuando se usa la variable porque
su tipo debe ser compatible con su uso. Por ejemplo, una variable que contiene una cadena usada en
el conversor «add()» debe ser convertible a un entero válido para tener éxito. Esto es especialmente
cierto cuando las variables se comparan con un valor estático. Debe usarse el método de coincidencia
adecuado.

## 2.9. Formatos de dirección {#section-2-9}

Varias instrucciones como «bind», «server», «nameserver» y «log» requieren una dirección.

Esta dirección puede ser un nombre de host, una dirección IPv4, una dirección IPv6 o «*». El «*» es
igual a la dirección especial «0.0.0.0» y puede usarse, en el caso de «bind» o «dgram-bind», para
escuchar en todas las IPv4 del sistema. El equivalente IPv6 es «::».

Según la instrucción, un puerto o un rango de puertos sigue a la dirección IP. Esto es obligatorio
en la instrucción «bind», opcional en «server».

Esta dirección también puede comenzar con una barra «/». Se considera de la familia «unix», y «/»
y los caracteres siguientes deben estar presentes en la ruta.

El tipo de socket o método de transporte por defecto, «datagram» o «stream», depende de la
instrucción de configuración que muestra la dirección. En efecto, «bind» y «server» usarán un tipo
de socket «stream» por defecto, mientras que «log», «nameserver» o «dgram-bind» usarán un
«datagram».

Opcionalmente, puede usarse un prefijo para forzar la familia de direcciones y/o el tipo de socket
y el método de transporte.

### 2.9.1. Prefijos de familia de direcciones {#section-2-9-1}

«abns@`<name>`» el `<name>` que sigue es un espacio de nombres abstracto (solo Linux).

«abnsz@`<name>`» el `<name>` que sigue es un espacio de nombres abstracto terminado en cero (solo
Linux).

«fd@`<n>`» la dirección que sigue es un descriptor de archivo `<n>` heredado del padre. El fd debe
estar vinculado y puede estar o no ya en escucha.

«ip@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera una dirección IPv4 o IPv6
según la sintaxis. Según la instrucción que use esta dirección, un puerto o un rango de puertos
puede o debe especificarse.

«ipv4@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv4. Según la instrucción que use esta dirección, un puerto o un rango de puertos puede o debe
especificarse.

«ipv6@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv6. Según la instrucción que use esta dirección, un puerto o un rango de puertos puede o debe
especificarse.

«sockpair@`<n>`» la dirección que sigue es el descriptor de archivo de un socket unix conectado o
de un par de sockets. Durante una conexión, el iniciador crea un par de sockets conectados y pasa
uno de ellos mediante el FD al otro extremo. El proceso a la escucha espera recibir el FD desde el
socket unix y lo usa como si fuera el FD de un accept(). Debe usarse con cuidado.

               Errores: se sabe que este protocolo no es fiable en macOS debido a
               un problema en la implementación de sendmsg(2) de macOS. La
               conexión podría no aceptarse correctamente.

«unix@`<path>`» la cadena que sigue se considera una ruta `<path>` de socket UNIX. Este prefijo es
útil para declarar una ruta de socket UNIX que no comienza por una barra «/».

### 2.9.2. Prefijos de tipo de socket {#section-2-9-2}

Los «Prefijos de familia de direcciones» anteriores también pueden llevar un prefijo para forzar
el tipo de socket y el método de transporte. El valor por defecto depende de la instrucción que use
esta dirección, pero en algunos casos el usuario puede forzar uno diferente. Este es el caso de la
instrucción «log», donde el valor por defecto es syslog sobre UDP, pero podríamos forzar el uso de
syslog sobre TCP.

Estos prefijos fueron diseñados con fines internos y los usuarios deberían en su lugar usar los
alias de la siguiente sección «2.9.3 Prefijos de protocolo». Sin embargo, pueden resultar prácticos
en ocasiones, por ejemplo en combinación con sockets heredados conocidos por su número de
descriptor de archivo, en cuyo caso la familia de direcciones es «fd» y el tipo de socket debe
declararse.

Si los usuarios necesitan uno de estos prefijos para lograr lo que esperan porque no pueden
configurar lo mismo usando los prefijos de protocolo, deberían informarlo a los mantenedores.

«stream+`<family>`@`<address>`» fuerza el tipo de socket y el método de transporte a «stream»

«dgram+`<family>`@`<address>`» fuerza el tipo de socket y el método de transporte a «datagram».

«quic+`<family>`@`<address>`» fuerza el tipo de socket a «datagram» y el método de transporte a
«stream».

### 2.9.3. Prefijos de protocolo {#section-2-9-3}

«quic4@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv4, pero el tipo de socket se fuerza a «datagram» y el método de transporte se fuerza a «stream».
Según la instrucción que use esta dirección, un puerto UDP o un rango de puertos puede o debe
especificarse. Es equivalente a «quic+ipv4@».

«quic6@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv6, pero el tipo de socket se fuerza a «datagram» y el método de transporte se fuerza a «stream».
Según la instrucción que use esta dirección, un puerto UDP o un rango de puertos puede o debe
especificarse. Es equivalente a «quic+ipv6@».

«tcp@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera una dirección IPv4 o IPv6
según la sintaxis, pero el tipo de socket y el método de transporte se fuerzan a «stream». Según la
instrucción que use esta dirección, un puerto o un rango de puertos puede o debe especificarse. Se
considera un alias de «stream+ip@».

«tcp4@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv4, pero el tipo de socket y el método de transporte se fuerzan a «stream». Según la instrucción
que use esta dirección, un puerto o un rango de puertos puede o debe especificarse. Se considera un
alias de «stream+ipv4@».

«tcp6@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv6, pero el tipo de socket y el método de transporte se fuerzan a «stream». Según la instrucción
que use esta dirección, un puerto o un rango de puertos puede o debe especificarse. Se considera un
alias de «stream+ipv6@».

«mptcp@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera una dirección IPv4 o IPv6
según la sintaxis, pero el tipo de socket y el método de transporte se fuerzan a «stream», con el
protocolo MPTCP. Según la instrucción que use esta dirección, un puerto o un rango de puertos puede
o debe especificarse.

«mptcp4@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv4, pero el tipo de socket y el método de transporte se fuerzan a «stream», con el protocolo
MPTCP. Según la instrucción que use esta dirección, un puerto o un rango de puertos puede o debe
especificarse.

«mptcp6@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv6, pero el tipo de socket y el método de transporte se fuerzan a «stream», con el protocolo
MPTCP. Según la instrucción que use esta dirección, un puerto o un rango de puertos puede o debe
especificarse.

«udp@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera una dirección IPv4 o IPv6
según la sintaxis, pero el tipo de socket y el método de transporte se fuerzan a «datagram». Según
la instrucción que use esta dirección, un puerto o un rango de puertos puede o debe especificarse.
Se considera un alias de «dgram+ip@».

«udp4@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv4, pero el tipo de socket y el método de transporte se fuerzan a «datagram». Según la instrucción
que use esta dirección, un puerto o un rango de puertos puede o debe especificarse. Se considera un
alias de «dgram+ipv4@».

«udp6@`<address>`[:port1[-port2]]» el `<address>` que sigue se considera siempre una dirección
IPv6, pero el tipo de socket y el método de transporte se fuerzan a «datagram». Según la instrucción
que use esta dirección, un puerto o un rango de puertos puede o debe especificarse. Se considera un
alias de «dgram+ipv6@».

«uxdg@`<path>`» la cadena que sigue se considera una ruta `<path>` de socket unix, pero el método
de transporte se fuerza a «datagram». Se considera un alias de «dgram+unix@».

«uxst@`<path>`» la cadena que sigue se considera una ruta `<path>` de socket unix, pero el método
de transporte se fuerza a «stream». Se considera un alias de «stream+unix@».

En versiones futuras, podrían usarse otros prefijos para especificar protocolos como QUIC, que
propone un transporte de flujo basado en sockets de tipo «datagram».

## 2.10. Ejemplos {#section-2-10}

```haproxy
# Simple configuration for an HTTP proxy listening on port 80 on all
    # interfaces and forwarding requests to a single backend "servers" with a
    # single server "server1" listening on 127.0.0.1:8000
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    frontend http-in
        bind *:80
        default_backend servers

    backend servers
        server server1 127.0.0.1:8000 maxconn 32


    # The same configuration defined with a single listen block. Shorter but
    # less expressive, especially in HTTP mode.
    global
        daemon
        maxconn 256

    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms

    listen http-in
        bind *:80
        server server1 127.0.0.1:8000 maxconn 32
```

Suponiendo que haproxy está en \$PATH, prueba estas configuraciones en un shell con:

```shell
$ sudo haproxy -f configuration.conf -c
```
