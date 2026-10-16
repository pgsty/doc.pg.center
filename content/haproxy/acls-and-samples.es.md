---
title: "7. ACLs y extracción de muestras"
linkTitle: "7. ACLs y muestras"
weight: 180
description: "Coincidencia de ACL, condiciones, conversores, extracciones de muestras y ACL predefinidas"
icon: fa-solid fa-filter
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/acls-and-samples/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 7"
---

HAProxy es capaz de extraer datos de los flujos de solicitudes o respuestas, de la información del
cliente o del servidor, de tablas, de información del entorno, etc. La acción de extraer dichos
datos se denomina obtención de una muestra. Una vez recuperadas, estas muestras pueden usarse con
diversos fines, como clave de una tabla de persistencia, pero los usos más comunes consisten en
compararlas con datos constantes predefinidos llamados patrones.

## 7.1. Conceptos básicos de ACL {#section-7-1}

Las Listas de Control de Acceso (ACL) consisten en declarar un método con nombre para comparar
cualquier pieza de información contra una lista de patrones predefinidos. Deben verse como
prácticamente equivalentes a las funciones en la mayoría de los lenguajes de programación, en el
sentido de que su declaración las hace disponibles para ser llamadas más adelante cuando se
necesiten. Su evaluación solo devuelve una coincidencia o una no coincidencia, lo cual es comparable
a los booleanos en muchos lenguajes de programación. Al contrario que las funciones en los lenguajes
de programación, las ACL pueden sobrecargarse tantas veces como se necesite para definir métodos de
coincidencia adicionales para el mismo nombre. En este caso, todas se evaluarán en su orden de
declaración hasta que una coincida.

El uso de ACL proporciona una solución flexible para realizar conmutación de contenido y, en
general, para tomar decisiones basadas en el contenido extraído de la solicitud, la respuesta o
cualquier estado del entorno. El principio es simple:

- extraer una muestra de datos de un flujo, una tabla o el entorno
- aplicar opcionalmente alguna conversión de formato a la muestra extraída
- aplicar uno o varios métodos de coincidencia de patrones sobre esta muestra
- realizar acciones solo cuando un patrón coincide con la muestra

Las acciones generalmente consisten en bloquear una solicitud, seleccionar un backend o añadir una
cabecera.

Para definir una prueba se utiliza la palabra clave "acl". La sintaxis es:

```text
acl <aclname> <criterion> [flags] [operator] [<value>] ...
```

Esto crea una nueva ACL `<aclname>` o completa una existente con nuevas pruebas. Esas pruebas se
aplican a la porción de solicitud/respuesta especificada en `<criterion>` y pueden ajustarse con
flags opcionales [flags]. Algunos criterios también soportan un operador que puede especificarse
antes del conjunto de valores. Opcionalmente pueden aplicarse algunos operadores de conversión a la
muestra, y se especificarán como una lista de palabras clave delimitada por comas justo después de
la primera palabra clave. Los valores son del tipo soportado por el criterio y están separados por
espacios.

Los nombres de ACL deben estar formados por letras mayúsculas y minúsculas, dígitos, '-' (guion),
'\_' (guion bajo), '.' (punto) y ':' (dos puntos). Los nombres de ACL distinguen mayúsculas de
minúsculas, lo que significa que "my_acl" y "My_Acl" son dos ACL diferentes.

No hay ningún límite impuesto al número de ACL. Las que no se usan no afectan al rendimiento, solo
consumen una pequeña cantidad de memoria.

El criterio generalmente es el nombre de un método de obtención de muestras o una de sus
declinaciones específicas de ACL. El método de prueba por defecto está implícito en el tipo de
salida de este método de obtención de muestras. Las declinaciones de ACL pueden describir métodos
de coincidencia alternativos de un mismo método de obtención de muestras. Los métodos de obtención
de muestras son los únicos que soportan una conversión.

Los métodos de obtención de muestras devuelven datos que pueden ser de los siguientes tipos:

- booleano
- entero (con signo o sin signo)
- dirección IPv4 o IPv6
- cadena
- bloque de datos

Los conversores transforman cualquiera de estos datos en cualquiera de ellos. Por ejemplo, algunos
conversores pueden convertir una cadena a minúsculas mientras que otros convertirían una cadena en
una dirección IPv4, o aplicar una máscara de red a una dirección IP. La muestra resultante es del
tipo del último conversor aplicado de la lista, que por defecto es el tipo del método de obtención
de muestras.

Cada muestra o conversor devuelve datos de un tipo específico, especificado con su palabra clave en
esta documentación. Cuando se declara una ACL utilizando un método de obtención de muestras
estándar, ciertos tipos implican automáticamente un método de coincidencia por defecto, que se
resume en la tabla siguiente:

```text
   +---------------------+-------------------+
   | Muestra o conversor | Por defecto       |
   |    tipo de salida   | método de prueba  |
   +---------------------+-------------------+
   | boolean             | bool              |
   +---------------------+-------------------+
   | integer             | int               |
   +---------------------+-------------------+
   | ip                  | ip                |
   +---------------------+-------------------+
   | string              | str               |
   +---------------------+-------------------+
   | binary              | ninguno, usa "-m" |
   +---------------------+-------------------+
```

Ten en cuenta que para comparar muestras binarias es obligatorio especificar un método de
coincidencia; ver más abajo.

El motor de ACL puede comparar estos tipos contra patrones de los siguientes tipos:

- booleano
- entero o rango de enteros
- dirección IP / red
- cadena (exacta, subcadena, sufijo, prefijo, subdirectorio, dominio)
- expresión regular
- bloque hexadecimal

Actualmente se soportan los siguientes flags de ACL:

```text
-i: ignora las mayúsculas y minúsculas durante la coincidencia de todos los patrones posteriores.
-f: carga los patrones desde una lista.
-m: usa un método específico de coincidencia de patrones
-n: prohíbe las resoluciones DNS
-M: carga el archivo apuntado por -f como un mapa.
-u: fuerza el identificador único de la ACL
--: fuerza el fin de los flags. Útil cuando una cadena parece uno de los flags.
```

El flag "-f" va seguido del nombre, que debe seguir el formato descrito en 2.7 sobre el formato de
nombres para mapas y ACL. Incluso es posible pasar varios argumentos "-f" si los patrones van a
cargarse desde varias listas. Si se referencia un archivo existente, todas las líneas se leerán como
valores individuales. Las líneas vacías, así como las que comienzan por una almohadilla ('#'), se
ignorarán. Todos los espacios y tabulaciones iniciales se eliminarán. Si es absolutamente necesario
insertar un patrón válido que comience por una almohadilla, basta con anteponerle un espacio para
que no se tome por un comentario. Dependiendo del tipo de dato y del método de coincidencia, HAProxy
puede cargar las líneas en un árbol binario, permitiendo búsquedas muy rápidas. Esto es cierto para
IPv4 y la coincidencia exacta de cadenas. En este caso, los duplicados se eliminarán automáticamente.

El flag "-M" permite que una ACL utilice un mapa. Si este flag está activo, la lista se analiza como
entradas de dos columnas. La primera columna contiene los patrones utilizados por la ACL y la
segunda columna contiene las muestras. La muestra puede usarse más adelante mediante un mapa. Esto
puede ser útil en algunos casos raros en los que una ACL solo se usaría para comprobar la
existencia de un patrón en un mapa antes de aplicar una correspondencia.

El flag "-u" fuerza el identificador único de la ACL. Este identificador único se utiliza con la
interfaz de socket para identificar la ACL y cambiar dinámicamente sus valores. Ten en cuenta que un
archivo siempre se identifica por su nombre incluso si se establece un id.

Ten en cuenta también que el flag "-i" se aplica a las entradas posteriores y no a las entradas
cargadas desde archivos que lo preceden. Por ejemplo:

```text
acl valid-ua hdr(user-agent) -f exact-ua.lst -i -f generic-ua.lst test
```

En este ejemplo, cada línea de "exact-ua.lst" se comparará exactamente contra la cabecera
"user-agent" de la solicitud. Luego cada línea de "generic-ua" se comparará sin distinguir
mayúsculas de minúsculas. Después, la palabra "test" también se comparará sin distinguir mayúsculas
de minúsculas.

El flag "-m" se utiliza para seleccionar un método específico de coincidencia de patrones sobre la
muestra de entrada. Todos los criterios específicos de ACL implican un método de coincidencia de
patrones y generalmente no necesitan este flag. Sin embargo, este flag es útil con los métodos
genéricos de obtención de muestras para describir cómo se van a comparar con los patrones. Es
obligatorio para obtenciones de muestras que devuelven un tipo de dato para el cual no existe un
método de coincidencia evidente (p. ej. cadena o binario). Cuando se especifica "-m" seguido de un
nombre de método de coincidencia de patrones, se utiliza ese método en lugar del predeterminado
para el criterio. Esto permite comparar contenidos de formas que no estaban previstas
inicialmente, o con métodos de obtención de muestras que devuelven una cadena. El método de
coincidencia también afecta a la forma en que se analizan los patrones. Por lo tanto, no debe
utilizarse con obtenciones de muestras con un sufijo de coincidencia (\_beg, \_end, \_sub...).
Además, especificar varios métodos de coincidencia de patrones "-m" no está permitido.

El flag "-n" prohíbe las resoluciones DNS. Se utiliza con la carga de archivos de IP. Por defecto,
si el analizador no puede analizar una dirección IP, considera que la cadena analizada quizá sea un
nombre de dominio e intenta la resolución DNS. El flag "-n" deshabilita esta resolución. Es útil
para detectar listas de IP mal formadas. Ten en cuenta que si el servidor DNS no está accesible, el
análisis de la configuración de HAProxy puede durar muchos minutos esperando a que expire el tiempo
de espera. Durante ese tiempo no se muestra ningún mensaje de error. El flag "-n" deshabilita este
comportamiento. Ten en cuenta también que durante la ejecución, esta función está deshabilitada
para las modificaciones dinámicas de ACL.

Sin embargo, hay algunas restricciones. No todos los métodos pueden utilizarse con todos los métodos
de obtención de muestras. Además, si "-m" se usa junto con "-f", debe colocarse primero. El método
de coincidencia de patrones debe ser uno de los siguientes:

- "found": solo comprueba si la muestra solicitada pudo encontrarse en el flujo, pero no la compara
  con ningún patrón. Se recomienda no pasar ningún patrón para evitar confusiones. Este método de
  coincidencia es particularmente útil para detectar la presencia de ciertos contenidos, como
  cabeceras, cookies, etc., incluso si están vacíos, y sin compararlos con nada ni contarlos.

- "bool" : comprueba el valor como booleano. Solo puede aplicarse a obtenciones que devuelven un
  valor booleano o entero, y no toma ningún patrón. El valor cero o falso no coincide; todos los
  demás valores sí coinciden.

- "int" : compara el valor como un entero. Puede usarse con muestras enteras y booleanas. El
  booleano falso es el entero 0, el verdadero es el entero 1.

- "ip" : compara el valor como una dirección IPv4 o IPv6. Solo es compatible con muestras de
  direcciones IP, por lo que está implícito y nunca es necesario.

- "bin" : compara el contenido contra una cadena hexadecimal que representa una secuencia binaria.
  Puede usarse con muestras binarias o de cadena.

- "len" : compara la longitud de la muestra como un entero. Puede usarse con muestras binarias o de
  cadena.

- "str" : coincidencia exacta: compara el contenido contra una cadena. Puede usarse con muestras
  binarias o de cadena.

- "sub" : coincidencia de subcadena: comprueba que el contenido contenga al menos una de las
  cadenas de patrón proporcionadas. Puede usarse con muestras binarias o de cadena.

- "reg" : coincidencia de expresión regular: compara el contenido contra una lista de expresiones
  regulares. Puede usarse con muestras binarias o de cadena.

- "beg" : coincidencia de prefijo: comprueba que el contenido comience como las cadenas de patrón
  proporcionadas. Puede usarse con muestras binarias o de cadena.

- "end" : coincidencia de sufijo: comprueba que el contenido termine como las cadenas de patrón
  proporcionadas. Puede usarse con muestras binarias o de cadena.

- "dir" : coincidencia de subdirectorio: comprueba que una porción del contenido delimitada por
  barras coincida exactamente con una de las cadenas de patrón proporcionadas. Puede usarse con
  muestras binarias o de cadena.

- "dom" : coincidencia de dominio: comprueba que una porción del contenido delimitada por puntos
  coincida exactamente con una de las cadenas de patrón proporcionadas. Puede usarse con muestras
  binarias o de cadena.

Por ejemplo, para detectar rápidamente la presencia de la cookie "JSESSIONID" en una solicitud
HTTP, es posible hacer:

```text
acl jsess_present req.cook(JSESSIONID) -m found
```

Para aplicar una expresión regular sobre los primeros 500 bytes de datos del búfer, se usaría la
siguiente acl:

```text
acl script_tag req.payload(0,500) -m reg -i <script>
```

En sistemas donde la biblioteca de expresiones regulares es mucho más lenta al usar "-i", es posible
convertir la muestra a minúsculas antes de comparar, así:

```text
acl script_tag req.payload(0,500),lower -m reg <script>
```

Todos los criterios específicos de ACL implican un método de coincidencia por defecto. La mayoría
de las veces, estos criterios se componen concatenando el nombre del método de obtención de
muestras original y el método de coincidencia. Por ejemplo, "hdr_beg" aplica la coincidencia "beg"
a las muestras recuperadas con el método de obtención "hdr". Este método de coincidencia solo es
utilizable cuando la palabra clave se usa sola, sin ningún conversor. Si se fuera a aplicar algún
conversor tras tal palabra clave de ACL, el método de coincidencia por defecto de la palabra clave
de ACL simplemente se ignora, ya que lo que importa para la coincidencia es el tipo de salida del
último conversor. Dado que todos los criterios específicos de ACL se basan en un método de
obtención de muestras, siempre es posible, en su lugar, utilizar el método de obtención de muestras
original y el método de coincidencia explícito usando "-m".

Si se especifica una coincidencia alternativa usando "-m" sobre un criterio específico de ACL, el
método de coincidencia simplemente se aplica al método de obtención de muestras subyacente. Por
ejemplo, todas las ACL siguientes son exactamente equivalentes:

```text
acl short_form  hdr_beg(host)        www.
acl alternate1  hdr_beg(host) -m beg www.
acl alternate2  hdr_dom(host) -m beg www.
acl alternate3  hdr(host)     -m beg www.

```

La tabla siguiente resume la matriz de compatibilidad entre los tipos de muestra o conversor y los
tipos de patrón contra los que realizar la obtención. Indica, para cada combinación compatible, el
nombre del método de coincidencia a utilizar, rodeado con los símbolos "\>" y "\<" cuando el método
es el predeterminado y funcionará por defecto sin "-m".

```text
                           +-------------------------------------------------+
                           |           Tipo de muestra de entrada            |
    +----------------------+---------+---------+---------+---------+---------+
    |    tipo de patrón    | boolean | integer |   ip    | string  | binary  |
    +----------------------+---------+---------+---------+---------+---------+
    | ninguno (presencia)  |  found  |  found  |  found  |  found  |  found  |
    +----------------------+---------+---------+---------+---------+---------+
    | ninguno (valor bool) |>  bool <|   bool  |         |   bool  |         |
    +----------------------+---------+---------+---------+---------+---------+
    | entero (valor)       |   int   |>  int  <|   int   |   int   |         |
    +----------------------+---------+---------+---------+---------+---------+
    | entero (longitud)    |   len   |   len   |   len   |   len   |   len   |
    +----------------------+---------+---------+---------+---------+---------+
    | dirección IP         |         |         |>   ip  <|    ip   |    ip   |
    +----------------------+---------+---------+---------+---------+---------+
    | cadena exacta        |   str   |   str   |   str   |>  str  <|   str   |
    +----------------------+---------+---------+---------+---------+---------+
    | prefijo              |   beg   |   beg   |   beg   |   beg   |   beg   |
    +----------------------+---------+---------+---------+---------+---------+
    | sufijo               |   end   |   end   |   end   |   end   |   end   |
    +----------------------+---------+---------+---------+---------+---------+
    | subcadena            |   sub   |   sub   |   sub   |   sub   |   sub   |
    +----------------------+---------+---------+---------+---------+---------+
    | subdirectorio        |   dir   |   dir   |   dir   |   dir   |   dir   |
    +----------------------+---------+---------+---------+---------+---------+
    | dominio              |   dom   |   dom   |   dom   |   dom   |   dom   |
    +----------------------+---------+---------+---------+---------+---------+
    | expresión regular    |   reg   |   reg   |   reg   |   reg   |   reg   |
    +----------------------+---------+---------+---------+---------+---------+
    | bloque hexadecimal   |         |         |         |   bin   |   bin   |
    +----------------------+---------+---------+---------+---------+---------+
```

### 7.1.1. Coincidencia de booleanos {#section-7-1-1}

Para comparar un booleano no se necesita ningún valor y todos los valores se ignoran. La
coincidencia booleana se utiliza por defecto para todos los métodos de obtención de tipo "boolean".
Cuando se utiliza la coincidencia booleana, el valor obtenido se devuelve tal cual, lo que
significa que un booleano "true" siempre coincidirá y un booleano "false" nunca coincidirá.

La coincidencia booleana también puede forzarse usando "-m bool" en métodos de obtención que
devuelven un valor entero. Entonces, el valor entero 0 se convierte al booleano "false" y todos los
demás valores se convierten a "true".

### 7.1.2. Coincidencia de enteros {#section-7-1-2}

La coincidencia de enteros se aplica por defecto a los métodos de obtención de enteros. También
puede forzarse en obtenciones booleanas usando "-m int". En este caso, "false" se convierte al
entero 0 y "true" se convierte al entero 1.

La coincidencia de enteros también soporta rangos de enteros y operadores. Ten en cuenta que la
coincidencia de enteros solo se aplica a valores positivos. Un rango es un valor expresado con un
límite inferior y un límite superior separados por dos puntos, y ambos pueden omitirse.

Por ejemplo, "1024:65535" es un rango válido para representar un rango de puertos no
privilegiados, y "1024:" también funcionaría. "0:1023" es una representación válida de puertos
privilegiados, y ":1023" también funcionaría.

Como caso especial, algunas funciones de ACL soportan números decimales que en realidad son dos
enteros separados por un punto. Esto se usa, por ejemplo, con algunas comprobaciones de versión.
Todas las propiedades de los enteros se aplican a esos números decimales, incluidos los rangos y
los operadores.

Para facilitar su uso, también se soportan operadores de comparación. Ten en cuenta que usar
operadores con rangos no tiene mucho sentido y está totalmente desaconsejado. Del mismo modo, no
tiene mucho sentido realizar comparaciones de orden con un conjunto de valores.

Los operadores disponibles para la coincidencia de enteros son:

```text
eq: verdadero si el valor probado es igual a al menos un valor
ge: verdadero si el valor probado es mayor o igual que al menos un valor
gt: verdadero si el valor probado es mayor que al menos un valor
le: verdadero si el valor probado es menor o igual que al menos un valor
lt: verdadero si el valor probado es menor que al menos un valor
```

Por ejemplo, la siguiente ACL coincide con cualquier cabecera Content-Length negativa:

```text
acl negative-length req.hdr_val(content-length) lt 0
```

Esta coincide con versiones SSL entre 3.0 y 3.1 (inclusive):

```text
acl sslv3 req.ssl_ver 3:3.1
```

### 7.1.3. Coincidencia de cadenas {#section-7-1-3}

La coincidencia de cadenas se aplica a métodos de obtención de cadenas o binarios, y existe en 6
formas diferentes:

- coincidencia exacta (-m str): la cadena extraída debe coincidir exactamente con los patrones;

- coincidencia de subcadena (-m sub): los patrones se buscan dentro de la cadena extraída, y la ACL
  coincide si se encuentra alguno de ellos dentro;

- coincidencia de prefijo (-m beg): los patrones se comparan con el comienzo de la cadena
  extraída, y la ACL coincide si alguno de ellos coincide.

- coincidencia de sufijo (-m end): los patrones se comparan con el final de la cadena extraída, y
  la ACL coincide si alguno de ellos coincide.

- coincidencia de subdirectorio (-m dir): los patrones se buscan en cualquier parte de la cadena
  extraída, delimitados por barras ("/"), el comienzo o el final de la cadena. La ACL coincide si
  alguno de ellos coincide. Así, la cadena "/images/png/logo/32x32.png" coincidiría con "/images",
  "/images/png", "images/png", "/png/logo", "logo/32x32.png" o "32x32.png", pero no con "png" ni
  con "32x32".

- coincidencia de dominio (-m dom): los patrones se buscan en cualquier parte de la cadena
  extraída, delimitados por puntos ("."), dos puntos (":"), barras ("/") o signos de interrogación
  ("?"), o por el comienzo o el final de la cadena. Está hecho para usarse con URLs. Los
  delimitadores iniciales y finales del patrón se ignoran. La ACL coincide si alguno de ellos
  coincide. Así, en la cadena de ejemplo "<http://www1.dc-eu.example.com:80/blah>", los patrones
  "http", "www1", ".www1", "dc-eu", "example", "com", "80", "dc-eu.example", "blah", ":www1:",
  "dc-eu.example:80" coincidirían, pero no "eu" ni "dc". Usarlo para comparar sufijos de dominio
  con fines de filtrado o enrutado generalmente no es una buena idea, ya que el enrutado podría
  burlarse fácilmente anteponiendo, por ejemplo, el prefijo coincidente delante de otro dominio.

La coincidencia de cadenas se aplica a cadenas literales tal como se pasan, con la excepción de la
barra invertida ("&#92;"), que posibilita escapar algunos caracteres como el espacio. Si se pasa el
flag "-i" antes de la primera cadena, la coincidencia se realizará ignorando mayúsculas y
minúsculas. Para comparar con la cadena "-i", colócala en segundo lugar, o pasa el flag "--" antes
de la primera cadena. Lo mismo se aplica, por supuesto, para comparar con la cadena "--".

No uses coincidencias de cadena para obtenciones binarias que podrían contener bytes nulos (0x00),
ya que la comparación se detiene ante la aparición del primer byte nulo. En su lugar, convierte
primero la obtención binaria a una cadena hexadecimal con el conversor hex.

Ejemplo:

```shell
# matches if the string <tag> is present in the binary sample
acl tag_found req.payload(0,0),hex -m sub 3C7461673E
```

### 7.1.4. Coincidencia de expresiones regulares (regexes) {#section-7-1-4}

Al igual que con la coincidencia de cadenas, la coincidencia de expresiones regulares se aplica a
cadenas literales tal como se pasan, con la excepción de la barra invertida ("&#92;"), que
posibilita escapar algunos caracteres como el espacio. Si se pasa el flag "-i" antes de la primera
expresión regular, la coincidencia se realizará ignorando mayúsculas y minúsculas. Para comparar
con la cadena "-i", colócala en segundo lugar, o pasa el flag "--" antes de la primera cadena. El
mismo principio se aplica, por supuesto, para comparar con la cadena "--".

### 7.1.5. Coincidencia de bloques de datos arbitrarios {#section-7-1-5}

Es posible comparar algunas muestras extraídas contra un bloque binario que quizá no pueda
representarse de forma segura como una cadena. Para ello, los patrones deben pasarse como una serie
de dígitos hexadecimales en número par, cuando el método de coincidencia está establecido en
binario. Cada secuencia de dos dígitos representará un byte. Los dígitos hexadecimales pueden
usarse en mayúsculas o minúsculas.

Ejemplo:

```shell
# match "Hello\n" in the input stream (\x48 \x65 \x6c \x6c \x6f \x0a)
acl hello req.payload(0,6) -m bin 48656c6c6f0a
```

### 7.1.6. Coincidencia de direcciones IPv4 e IPv6 {#section-7-1-6}

Los valores de direcciones IPv4 pueden especificarse como direcciones simples o con una máscara de
red añadida, en cuyo caso la dirección IPv4 coincide siempre que esté dentro de la red. Las
direcciones simples también pueden sustituirse por un nombre de host resoluble, pero esta práctica
está generalmente desaconsejada, ya que dificulta la lectura y la depuración de las
configuraciones. Si se usan nombres de host, deberías al menos asegurarte de que estén presentes
en /etc/hosts, de modo que la configuración no dependa de ninguna resolución DNS aleatoria en el
momento en que se analiza la configuración.

La notación de dirección IPv4 con puntos se soporta tanto en la forma regular como en la forma
abreviada con los octetos de valor 0 omitidos:

```text
    +------------------+------------------+------------------+
    | Ejemplo 1        | Ejemplo 2        | Ejemplo 3        |
    +------------------+------------------+------------------+
    |  192.168.0.1     |   10.0.0.12      |   127.0.0.1      |
    |  192.168.1       |   10.12          |   127.1          |
    |  192.168.0.1/22  |   10.0.0.12/8    |   127.0.0.1/8    |
    |  192.168.1/22    |   10.12/8        |   127.1/8        |
    +------------------+------------------+------------------+
```

Observa que esto es diferente de la notación de direcciones CIDR del RFC 4632, en la que
192.168.42/24 sería equivalente a 192.168.42.0/24.

IPv6 puede introducirse en su forma habitual, con o sin máscara de red añadida. Solo se aceptan
recuentos de bits para las máscaras de red IPv6. Para evitar cualquier riesgo de problemas con
direcciones IP resueltas aleatoriamente, los nombres de host nunca se permiten en patrones IPv6.

HAProxy también es capaz de comparar direcciones IPv4 con direcciones IPv6 en las siguientes
situaciones:

- la dirección probada es IPv4, la dirección del patrón es IPv4: la coincidencia se aplica en IPv4
  usando la máscara suministrada, si la hay.
- la dirección probada es IPv6, la dirección del patrón es IPv6: la coincidencia se aplica en IPv6
  usando la máscara suministrada, si la hay.
- la dirección probada es IPv6, la dirección del patrón es IPv4: la coincidencia se aplica en IPv4
  usando la máscara del patrón si la dirección IPv6 coincide con 2002:IPV4::, ::IPV4 o::ffff:IPV4;
  en caso contrario, falla.
- la dirección probada es IPv4, la dirección del patrón es IPv6: la dirección IPv4 se convierte
  primero a IPv6 anteponiéndole::ffff:, y luego la coincidencia se aplica en IPv6 usando la
  máscara IPv6 suministrada.

## 7.2. Uso de ACL para formar condiciones {#section-7-2}

Algunas acciones solo se realizan ante una condición válida. Una condición es una combinación de
ACL con operadores. Se soportan 3 operadores:

- AND (implícito)
- OR (explícito con la palabra clave "or" o el operador "\|\|")
- Negación con el signo de exclamación ("!")

Una condición se forma como una forma disyuntiva:

```text
[!]acl1 [!]acl2 ... [!]acln  { or [!]acl1 [!]acl2 ... [!]acln } ...
```

Tales condiciones generalmente se usan tras una instrucción "if" o "unless", indicando cuándo la
condición disparará la acción.

Por ejemplo, para bloquear las solicitudes HTTP a la URL "\*" con métodos distintos de "OPTIONS",
así como las solicitudes POST sin content-length, y las solicitudes GET o HEAD con un
content-length mayor que 0, y finalmente toda solicitud que no sea ni GET/HEAD/POST/OPTIONS !

```haproxy
acl missing_cl req.hdr_cnt(Content-length) eq 0
http-request deny if HTTP_URL_STAR !METH_OPTIONS || METH_POST missing_cl
http-request deny if METH_GET HTTP_CONTENT
http-request deny unless METH_GET or METH_POST or METH_OPTIONS
```

Para seleccionar un backend distinto para las solicitudes de contenidos estáticos del sitio "www" y
para toda solicitud de los hosts "img", "video", "download" y "ftp":

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
acl host_www    hdr_beg(host) -i www
acl host_static hdr_beg(host) -i img. video. download. ftp.
```

```haproxy
# now use backend "static" for all static-only hosts, and for static URLs
# of host "www". Use backend "www" for the rest.
use_backend static if host_static or host_www url_static
use_backend www    if host_www
```

También es posible formar reglas usando «ACL anónimas». Son expresiones de ACL sin nombre que se
construyen al vuelo sin necesidad de declararlas. Deben encerrarse entre llaves, con un espacio
antes y después de cada llave (porque las llaves deben verse como palabras independientes).
Ejemplo:

```text
La siguiente regla:

    acl missing_cl req.hdr_cnt(Content-length) eq 0
    http-request deny if METH_POST missing_cl

También puede escribirse así:

    http-request deny if METH_POST { req.hdr_cnt(Content-length) eq 0 }
```

Generalmente no se recomienda usar esta construcción porque es mucho más fácil dejar errores en la
configuración cuando se escribe de esa forma. Sin embargo, para reglas muy simples que solo
comparan una dirección IP de origen, por ejemplo, puede tener más sentido usarlas que declarar ACL
con nombres aleatorios. Otro ejemplo de buen uso es el siguiente:

```text
Con ACL con nombre:

     acl site_dead nbsrv(dynamic) lt 2
     acl site_dead nbsrv(static)  lt 2
     monitor fail  if site_dead

Con ACL anónimas:

     monitor fail if { nbsrv(dynamic) lt 2 } || { nbsrv(static) lt 2 }
```

Consulta la [sección 4.2](/es/haproxy/proxies/#section-4-2) para obtener ayuda detallada sobre las palabras clave "http-request deny" y "use_backend".

## 7.3. Obtención de muestras {#section-7-3}

Históricamente, los métodos de obtención de muestras solo se usaban para recuperar datos que
comparar contra patrones mediante ACL. Con la llegada de las tablas de persistencia, se creó una
nueva clase de métodos de obtención de muestras, que en la mayoría de los casos comparten la misma
sintaxis que su contraparte de ACL. Estos métodos de obtención de muestras también se conocen como
«fetches». Hoy en día, las ACL y los fetches han convergido. Todos los métodos de obtención de ACL
se han puesto a disposición como métodos de obtención, y las ACL también pueden usar cualquier
método de obtención de muestras.

Esta sección detalla todos los métodos de obtención de muestras disponibles y su tipo de salida.
Algunos métodos de obtención de muestras tienen alias obsoletos que se usan para mantener la
compatibilidad con configuraciones existentes. Estos se marcan explícitamente como obsoletos y no
deberían usarse en configuraciones nuevas.

Las muestras tienen tipo. El tipo de una muestra determina cómo puede compararse con patrones,
qué conversores pueden aplicársele y cómo se convierte cuando se espera otro tipo. Se utilizan los
siguientes tipos:

- booleano: un valor verdadero o falso, tal como lo devuelven los métodos de obtención que solo
  informan de una condición. Tales muestras se comparan sin ninguna opción "-m". Un entero se
  considera verdadero cuando no es cero, y una cadena se analiza primero como entero.

- entero: un entero de 64 bits con signo, es decir, un valor entre -2^63 y 2^63-1
  (-9223372036854775808 y 9223372036854775807). Cuando se convierte una cadena a entero, la
  conversión se detiene en el primer carácter que no sea dígito y que no sea el carácter de signo
  inicial ('+' o '-'). Se utiliza el valor formado por los dígitos leídos, que es cero si no hubo
  ninguno, pero las cadenas vacías fallan al convertir. Los valores que no caben se ajustan al
  entero representable más pequeño o más grande.

- dirección IPv4 y dirección IPv6: son dos tipos distintos, aunque la mayoría de los lugares que
  aceptan uno también aceptan el otro y simplemente se documentan como que toman una dirección. Una
  dirección IPv4 puede convertirse a un entero, lo que da el valor de 32 bits de la dirección, y a
  una dirección IPv6, lo que da su forma IPv4 mapeada en IPv6 ("::ffff:a.b.c.d"). Las conversiones
  inversas son más limitadas: una dirección IPv6 no tiene ninguna forma entera, y solo se convierte
  a una dirección IPv4 si es una dirección IPv4 mapeada en IPv6, compatible con IPv4 o 6to4.

- cadena: una serie de bytes que se detiene en el primer carácter NUL (0x00), el cual no forma
  parte de la cadena (usa el tipo binario si se necesita un carácter NUL incrustado). No se infiere
  ninguna codificación: haproxy no intenta interpretar estos bytes como caracteres; si representan
  texto, en qué juego de caracteres y cómo se muestran depende únicamente de para qué se use la
  cadena. Convertir una muestra binaria a cadena, por tanto, descarta silenciosamente todo a partir
  del primer carácter NUL, ya sea la conversión explícita o implícita.

- binario: un bloque de bytes cuya longitud se conoce, pudiendo tomar cada byte cualquier valor de
  0 a 255, NUL incluido. Esto es lo que devuelven los métodos de obtención que extraen datos en
  bruto, como un cuerpo de solicitud o el contenido de un protocolo binario. Tal muestra no puede
  convertirse a booleano, entero ni dirección, y debe compararse como bloque binario usando "-m
  bin" (consulta la [sección 7.1.5](/es/haproxy/acls-and-samples/#section-7-1-5)) o transformarse primero en una forma imprimible, por
  ejemplo usando el conversor "hex". La conversión inversa es gratuita, ya que una cadena siempre
  es un bloque binario válido.

- método: un método HTTP. Los métodos conocidos por haproxy se representan mediante un
  identificador; los demás conservan su cadena original.

La tabla de conversores siguiente también usa "any" para designar los conversores que aceptan
cualquier tipo de entrada.

Las derivadas de ACL también se indican cuando están disponibles, con sus respectivos métodos de
coincidencia. Todas ellas tienen un método de coincidencia de patrones por defecto bien definido,
por lo que nunca es necesario (aunque sí está permitido) pasar la opción "-m" para indicar cómo se
comparará la muestra usando ACL.

Como se indica en la matriz de compatibilidad de tipos de muestra frente a coincidencia que figura
más arriba, al usar un método genérico de obtención de muestras en una ACL, la opción "-m" es
obligatoria salvo que el tipo de muestra sea booleano, entero, IPv4 o IPv6. Cuando la misma palabra
clave existe como palabra clave de ACL y como método de obtención estándar, el motor de ACL
escogerá automáticamente por defecto la exclusiva de ACL.

Algunas de estas palabras clave soportan uno o varios argumentos obligatorios, y uno o varios
argumentos opcionales. Estos argumentos están fuertemente tipados y se comprueban cuando se
analiza la configuración, de modo que no haya riesgo de ejecutarse con un argumento incorrecto
(p. ej. un nombre de backend sin resolver). Los argumentos de las funciones de obtención se pasan
entre paréntesis y están delimitados por comas. Cuando un argumento es opcional, se indicará más
abajo entre corchetes ('[ ]'). Cuando todos los argumentos son opcionales, los paréntesis pueden
omitirse.

Así, la sintaxis de un método de obtención de muestras estándar es una de las siguientes:

- name
- name(arg1)
- name(arg1,arg2)

### 7.3.1. Conversores {#section-7-3-1}

Los métodos de obtención de muestras pueden combinarse con transformaciones que se aplican sobre
la muestra obtenida (también llamados «conversores»). Estas combinaciones forman lo que se llama
«expresiones de muestra» y el resultado es una «muestra». Inicialmente esto solo estaba soportado
por las directivas "stick on" y "stick store-request", pero ahora se ha extendido a todos los
lugares donde pueden usarse muestras (ACL, log-format, unique-id-format, add-header, ...).

Estas transformaciones se enumeran como una serie de palabras clave específicas tras el método de
obtención de muestras. Estas palabras clave igualmente pueden añadirse inmediatamente después del
argumento de la palabra clave de obtención, delimitadas por una coma. Estas palabras clave también
pueden soportar algunos argumentos (p. ej. una máscara de red) que deben pasarse entre paréntesis.

Una cierta categoría de conversores son operadores a nivel de bits y aritméticos que soportan la
realización de operaciones básicas con enteros. Se soportan algunas operaciones a nivel de bits
(and, or, xor, cpl) y algunas operaciones aritméticas (add, sub, mul, div, mod, neg). Se
proporcionan algunos comparadores (odd, even, not, bool) que posibilitan informar de una
coincidencia sin tener que escribir una ACL.

Se soportan las siguientes palabras clave:

```text
   palabra clave                                   tipo de entrada   tipo de salida
------------------------------------------------+-------------+----------------
51d.single(prop[,prop*])                           string       string
add(value)                                         integer      integer
add_item(delim[,var[,suff]])                       string       string
aes_cbc_dec(bits,nonce,key[,<aad>])                binary       binary
aes_cbc_enc(bits,nonce,key[,<aad>])                binary       binary
aes_gcm_dec(bits,nonce,key,aead_tag[,aad])         binary       binary
aes_gcm_enc(bits,nonce,key,aead_tag[,aad])         binary       binary
and(value)                                         integer      integer
b64dec                                             string       binary
base2                                              binary       string
base64                                             binary       string
be2dec(separator,chunk_size[,truncate])            binary       string
le2dec(separator,chunk_size[,truncate])            binary       string
be2hex([separator[,chunk_size[,truncate]]])        binary       string
bool                                               integer      boolean
bytes(offset[,length])                             binary       binary
capture-req(id)                                    string       string
capture-res(id)                                    string       string
concat([start[,var[,end]]])                        string       string
cpl                                                integer      integer
crc32([avalanche])                                 binary       integer
crc32c([avalanche])                                binary       integer
cut_crlf                                           string       string
da-csv-conv(prop[,prop*])                          string       string
date                                               string       integer
debug([prefix][,destination])                       any          same
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
digest(algorithm)                                  binary       binary
div(value)                                         integer      integer
djb2([avalanche])                                  binary       integer
eth.data                                           binary       binary
eth.dst                                            binary       binary
eth.hdr                                            binary       binary
eth.proto                                          binary       integer
eth.src                                            binary       binary
eth.vlan                                           binary       integer
even                                               integer      boolean
fe_exists                                          string       boolean
field(index,delimiters[,count])                    string       string
fix_is_valid                                       binary       boolean
fix_tag_value(tag)                                 binary       binary
has_ctl([mask])                                    binary       boolean
hex                                                binary       string
hex2i                                              binary       integer
hmac(algorithm,key)                                binary       binary
host_only                                          string       string
htonl                                              integer      integer
http_date([offset[,unit]])                         integer      string
iif(true,false)                                    boolean      string
in_table([table])                                  any          boolean
ip.data                                            binary       binary
ip.df                                              binary       integer
ip.dst                                             binary       address
ip.fp                                              binary       binary
ip.hdr                                             binary       binary
ip.proto                                           binary       integer
ip.src                                             binary       address
ip.tos                                             binary       integer
ip.ttl                                             binary       integer
ip.ver                                             binary       integer
ipmask(mask4[,mask6])                              address      address
json([input-code])                                 string       string
json_query(json_path[,output_type])                string       _outtype_
jwt_decrypt_jwk(<jwk>)                             string       binary
jwt_decrypt_cert(<cert>)                           string       binary
jwt_decrypt_secret(<secret>)                       string       binary
jwt_header_query([json_path[,output_type]])        string       string
jwt_payload_query([json_path[,output_type]])       string       string
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
jwt_verify(alg,key)                                string       integer
jwt_verify_cert(alg,cert)                          string       integer
language(value[,default])                          string       string
length                                             string       integer
lower                                              string       string
ltime(format[,offset])                             integer      string
ltrim(chars)                                       string       string
map(map_name[,default_value])                      string       string
map_match(map_name[,default_value])                _match_      string
map_match_output(map_name[,default_value])         _match_      _output_
mod(value)                                         integer      integer
mqtt_field_value(pkt_type,fieldname_or_prop_ID)    binary       binary
mqtt_is_valid                                      binary       boolean
ms_ltime(format[,offset])                          integer      string
ms_utime(format[,offset])                          integer      string
mul(value)                                         integer      integer
nbsrv                                              string       integer
neg                                                integer      integer
not                                                integer      boolean
odd                                                integer      boolean
or(value)                                          integer      integer
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
param(name[,delim])                                string       string
port_only                                          string       integer
protobuf(field_number[,field_type])                binary       binary
regsub(regex,subst[,flags])                        string       string
reverse                                            string       string
reverse_dom                                        string       string
rfc7239_field(field)                               string       string
rfc7239_is_valid                                   string       boolean
rfc7239_n2nn                                       string       address / str
rfc7239_n2np                                       string       integer / str
rfc7239_nn                                         address/str  string
rfc7239_np                                         integer/str  string
rtrim(chars)                                       string       string
sdbm([avalanche])                                  binary       integer
secure_memcmp(var)                                 string       boolean
set-var(var[,cond...])                              any          same
sha1                                               binary       binary
sha2([bits])                                       binary       binary
srv_is_up                                          string       boolean
srv_queue                                          string       integer
strcmp(var)                                        string       boolean
sub(value)                                         integer      integer
table_bytes_in_rate([table])                       any          integer
table_bytes_out_rate([table])                      any          integer
table_clr_gpc(idx[,table])                         any          integer
table_clr_gpc0([table])                            any          integer
table_clr_gpc1([table])                            any          integer
table_conn_cnt([table])                            any          integer
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
table_conn_cur([table])                            any          integer
table_conn_rate([table])                           any          integer
table_expire([table[,default_value]])              any          integer
table_glitch_cnt([table])                          any          integer
table_glitch_rate([table])                         any          integer
table_gpc(idx[,table])                             any          integer
table_gpc0([table])                                any          integer
table_gpc0_rate([table])                           any          integer
table_gpc1([table])                                any          integer
table_gpc1_rate([table])                           any          integer
table_gpc_rate(idx[,table])                        any          integer
table_gpt(idx[,table])                             any          integer
table_gpt0([table])                                any          integer
table_http_err_cnt([table])                        any          integer
table_http_err_rate([table])                       any          integer
table_http_fail_cnt([table])                       any          integer
table_http_fail_rate([table])                      any          integer
table_http_req_cnt([table])                        any          integer
table_http_req_rate([table])                       any          integer
table_idle([table[,default_value]])                any          integer
table_inc_gpc(idx[,table])                         any          integer
table_inc_gpc0([table])                            any          integer
table_inc_gpc1([table])                            any          integer
table_kbytes_in([table])                           any          integer
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
table_kbytes_out([table])                          any          integer
table_server_id([table])                           any          integer
table_sess_cnt([table])                            any          integer
table_sess_rate([table])                           any          integer
table_trackers([table])                            any          integer
tcp.dst                                            binary       integer
tcp.flags                                          binary       integer
tcp.options.mss                                    binary       integer
tcp.options.sack                                   binary       integer
tcp.options.tsopt                                  binary       integer
tcp.options.tsval                                  binary       integer
tcp.options.wscale                                 binary       integer
tcp.options.wsopt                                  binary       integer
tcp.options_list                                   binary       binary
tcp.seq                                            binary       integer
tcp.src                                            binary       integer
tcp.win                                            binary       integer
ub64dec                                            string       string
ub64enc                                            string       string
ungrpc(field_number[,field_type])                  binary       binary / int
unset-var(var)                                      any          same
upper                                              string       string
url_dec([in_form])                                 string       string
url_enc([enc_type])                                string       string
us_ltime(format[,offset])                          integer      string
us_utime(format[,offset])                          integer      string
utime(format[,offset])                             integer      string
when(condition)                                     any          same
word(index,delimiters[,count])                     string       string
wt6([avalanche])                                   binary       integer
x509_v_err_str                                     integer      string
xor(value)                                         integer      integer
-- palabra clave -----------------------------+- tipo entrada + tipo salida -
xxh3([seed])                                       binary       integer
xxh32([seed])                                      binary       integer
xxh64([seed])                                      binary       integer
```

A continuación se detalla la lista de palabras clave de los conversores:

<a id="entry-7-3-1-51d-single"></a>

**`51d.single(<prop>[,<prop>*])`**

```haproxy
51d.single(<prop>[,<prop>*])
```

Devuelve los valores de las propiedades solicitadas como una cadena, donde los valores están
separados por el delimitador especificado con "51degrees-property-separator". El dispositivo se
identifica usando la cabecera User-Agent pasada al conversor. A la función pueden pasársele hasta
cinco nombres de propiedades, y si no puede encontrarse un nombre de propiedad, se devuelve el
valor "NoData".

Ejemplo:

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request,
# containing values for the three properties requested by using the
# User-Agent passed to the converter.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[req.fhdr(User-Agent),51d.single(DeviceType,IsMobile,IsTablet)]
```

<a id="entry-7-3-1-add"></a>

**`add(<value>)`**

```haproxy
add(<value>)
```

Suma `<value>` al valor de entrada de tipo entero con signo y devuelve el resultado como un entero
con signo. `<value>` puede ser un valor numérico o un nombre de variable. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para
más detalles.

<a id="entry-7-3-1-add-item"></a>

**`add_item(<delim>[,<var>[,<suff>]])`**

```haproxy
add_item(<delim>[,<var>[,<suff>]])
```

Concatena un mínimo de 2 y hasta 3 campos después de la muestra actual, que luego se convierte en
cadena. El primero, `<delim>`, es una cadena constante que se añadirá inmediatamente después de la
muestra existente si la muestra existente no está vacía y `<var>` o `<suff>` no está vacío. El
segundo, `<var>`, es un nombre de variable. La variable se buscará, su contenido se convertirá a
cadena y se añadirá inmediatamente después de la parte `<delim>`. Si la variable no se encuentra,
no se añade nada. Es opcional y puede ir seguido opcionalmente de una cadena constante `<suff>`;
sin embargo, si se omite `<var>`, entonces `<suff>` es obligatorio. Este conversor es similar al
conversor concat y puede usarse para construir nuevas variables formadas por una sucesión de otras
variables, pero la diferencia principal es que realiza las comprobaciones de si añadir un
delimitador tiene sentido, como no sería el caso si, p. ej., la muestra actual está vacía. Esa
situación requeriría 2 reglas separadas usando el conversor concat, donde la primera regla tendría
que comprobar si la cadena de la muestra actual está vacía antes de añadir un delimitador. Si se
necesitan comas o paréntesis de cierre como delimitadores, deben protegerse con comillas o barras
invertidas, ellas mismas protegidas para que no las elimine el analizador de primer nivel
(consulta la [sección 2.2](/es/haproxy/configuration-basics/#section-2-2) sobre el uso de comillas y el escapado). Ver ejemplos más abajo.

Ejemplo:

```text
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1,"(site1)") if src,in_table(site1)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score2,"(site2)") if src,in_table(site2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score3,"(site3)") if src,in_table(site3)'
http-request set-header x-tagged %[var(req.tagged)]

http-request set-var(req.tagged) 'var(req.tagged),add_item(",",req.score1),add_item(",",req.score2)'
http-request set-var(req.tagged) 'var(req.tagged),add_item(",",,(site1))' if src,in_table(site1)
```

<a id="entry-7-3-1-aes-cbc-dec"></a>

**`aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_dec(<bits>,<nonce>,<key>[,<aad>])
```

Descifra la entrada de bytes en bruto usando el algoritmo AES128-CBC, AES192-CBC o AES256-CBC,
dependiendo del parámetro `<bits>`. Todos los demás parámetros deben estar codificados en base64 y
el resultado devuelto está en formato de bytes en bruto. El parámetro `<aad>` es opcional. Si la
validación de `<aad>` falla, el conversor no devuelve ningún dato. `<nonce>`, `<key>` y `<aad>`
pueden ser cadenas o variables. Este conversor requiere al menos OpenSSL 1.0.1.

Ejemplo:

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_cbc_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-cbc-enc"></a>

**`aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])`**

```haproxy
aes_cbc_enc(<bits>,<nonce>,<key>[,<aad>])
```

Cifra la entrada de bytes en bruto usando el algoritmo AES128-CBC, AES192-CBC o AES256-CBC,
dependiendo del parámetro `<bits>`. Los parámetros `<nonce>`, `<key>` y `<aad>` deben estar
codificados en base64. El parámetro `<aad>` es opcional. El resultado devuelto está en formato de
bytes en bruto. `<nonce>`, `<key>` y `<aad>` pueden ser cadenas o variables. Este conversor
requiere al menos OpenSSL 1.0.1.

Ejemplo:

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_cbc_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==)]
```

<a id="entry-7-3-1-aes-gcm-dec"></a>

**`aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_dec(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

Descifra la entrada de bytes en bruto usando el algoritmo AES128-GCM, AES192-GCM o AES256-GCM,
dependiendo del parámetro `<bits>`. Todos los demás parámetros deben estar codificados en base64 y
el resultado devuelto está en formato de bytes en bruto. Si la validación de `<aead_tag>` o
`<aad>` falla, el conversor no devuelve ningún dato. El parámetro `<aad>` es opcional. `<nonce>`,
`<key>`, `<aead_tag>` y `<aad>` pueden ser cadenas o variables. Este conversor requiere al menos
OpenSSL 1.0.1.

Ejemplo:

```text
http-response set-header X-Decrypted-Text %[var(txn.enc),\
  aes_gcm_dec(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-aes-gcm-enc"></a>

**`aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])`**

```haproxy
aes_gcm_enc(<bits>,<nonce>,<key>,<aead_tag>[,<aad>])
```

Cifra la entrada de bytes en bruto usando el algoritmo AES128-GCM, AES192-GCM o AES256-GCM,
dependiendo del parámetro `<bits>`. Los parámetros `<nonce>`, `<key>` y `<aad>` deben estar
codificados en base64. El parámetro `<aead_tag>` debe ser una variable. La etiqueta AEAD se
almacenará codificada en base64 en esa variable. El parámetro `<aad>` es opcional. El resultado
devuelto está en formato de bytes en bruto. `<nonce>`, `<key>` y `<aad>` pueden ser cadenas o
variables. Este conversor requiere al menos OpenSSL 1.0.1.

Ejemplo:

```text
http-response set-header X-Encrypted-Text %[var(txn.plain),\
  aes_gcm_enc(128,txn.nonce,Zm9vb2Zvb29mb29wZm9vbw==,txn.aead_tag)]
```

<a id="entry-7-3-1-and"></a>

**`and(<value>)`**

```haproxy
and(<value>)
```

Realiza un "AND" a nivel de bits entre `<value>` y el valor de entrada de tipo entero con signo, y
devuelve el resultado como un entero con signo. `<value>` puede ser un valor numérico o un nombre
de variable. Consulta la [sección
2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-1-b64dec"></a>

**`b64dec`**

```haproxy
b64dec
```

Convierte (decodifica) una cadena de entrada codificada en base64 a su representación binaria.
Realiza la operación inversa de base64(). Para la variante base64url ("URL and Filename Safe
Alphabet" (RFC 4648)) ver "ub64dec".

<a id="entry-7-3-1-base2"></a>

**`base2`**

```haproxy
base2
```

Convierte una muestra binaria de entrada en una cadena binaria que contiene ocho dígitos binarios
por byte de entrada. Se usa para poder realizar coincidencia de prefijo más largo en tipos donde
la representación nativa no permite la coincidencia por prefijo, por ejemplo prefijos IP.

<a id="entry-7-3-1-base64"></a>

**`base64`**

```haproxy
base64
```

Convierte una muestra binaria de entrada en una cadena base64. Se usa para registrar o transferir
contenido binario de una forma en la que pueda transferirse de manera fiable (p. ej. un ID SSL
puede copiarse en una cabecera). Para la variante base64url ("URL and Filename Safe Alphabet"
(RFC 4648)) ver "ub64enc".

<a id="entry-7-3-1-be2dec"></a>

**`be2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
be2dec(<separator>,<chunk_size>[,<truncate>])
```

Convierte una muestra binaria de entrada big-endian en una cadena que contiene un número entero
sin signo por cada `<chunk_size>` bytes de entrada. `<separator>` se coloca cada `<chunk_size>`
bytes binarios de entrada si se especifica. El flag `<truncate>` indica si la entrada binaria se
trunca en los límites de `<chunk_size>`. El valor máximo de `<chunk_size>` está limitado por el
tamaño de long long int (8 bytes).

Ejemplo:

```text
bin(01020304050607),be2dec(:,2)   # 258:772:1286:7
bin(01020304050607),be2dec(-,2,1) # 258-772-1286
bin(01020304050607),be2dec(,2,1)  # 2587721286
bin(7f000001),be2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-le2dec"></a>

**`le2dec(<separator>,<chunk_size>[,<truncate>])`**

```haproxy
le2dec(<separator>,<chunk_size>[,<truncate>])
```

Convierte una muestra binaria de entrada little-endian en una cadena que contiene un número entero
sin signo por cada `<chunk_size>` bytes de entrada. `<separator>` se inserta cada `<chunk_size>`
bytes binarios de entrada si se especifica. El flag `<truncate>` indica si la entrada binaria se
trunca en los límites de `<chunk_size>`. El valor máximo de `<chunk_size>` está limitado por el
tamaño de long long int (8 bytes).

Ejemplo:

```text
bin(01020304050607),le2dec(:,2)   # 513:1284:2055:7
bin(01020304050607),le2dec(-,2,1) # 513-1284-2055
bin(01020304050607),le2dec(,2,1)  # 51312842055
bin(7f000001),le2dec(.,1)         # 127.0.0.1
```

<a id="entry-7-3-1-be2hex"></a>

**`be2hex([<separator>[,<chunk_size>[,<truncate>]]])`**

```haproxy
be2hex([<separator>[,<chunk_size>[,<truncate>]]])
```

Convierte una muestra binaria de entrada big-endian en una cadena hexadecimal que contiene dos
dígitos hexadecimales por byte de entrada. Se usa para registrar o transferir volcados
hexadecimales de algunos datos binarios de entrada de una forma en la que puedan transferirse de
manera fiable (p. ej. un ID SSL puede copiarse en una cabecera). `<separator>` se coloca cada
`<chunk_size>` bytes binarios de entrada si se especifica. El flag `<truncate>` indica si la
entrada binaria se trunca en los límites de `<chunk_size>`.

Ejemplo:

```text
bin(01020304050607),be2hex         # 01020304050607
bin(01020304050607),be2hex(:,2)    # 0102:0304:0506:07
bin(01020304050607),be2hex(--,2,1) # 0102--0304--0506
bin(0102030405060708),be2hex(,3,1) # 010203040506
```

<a id="entry-7-3-1-bool"></a>

**`bool`**

```haproxy
bool
```

Devuelve un booleano TRUE si el valor de entrada de tipo entero con signo no es nulo; en caso
contrario devuelve FALSE. Usado junto con and(), puede utilizarse para informar de
verdadero/falso en pruebas de bits sobre valores de entrada (p. ej. verificar la presencia de un
flag).

<a id="entry-7-3-1-bytes"></a>

**`bytes(<offset>[,<length>])`**

```haproxy
bytes(<offset>[,<length>])
```

Extrae algunos bytes de una muestra binaria de entrada. El resultado es una muestra binaria que
comienza en un desplazamiento (en bytes) de la muestra original y truncada opcionalmente en la
longitud dada. `<offset>` y `<length>` pueden ser valores numéricos o nombres de variable. El
conversor devuelve una muestra vacía si `<offset>` o `<length>` es inválido. Un `<offset>`
inválido significa un valor negativo o un valor \>= la longitud de la muestra de entrada. Un
`<length>` inválido significa un valor negativo.

Ejemplo:

```text
http-request set-var(txn.input) req.hdr(input) # let's say input is "012345"

http-response set-header bytes_0 "%[var(txn.input),bytes(0)]"  # outputs "012345"
http-response set-header bytes_1_3 "%[var(txn.input),bytes(1,3)]"  # outputs "123"

http-response set-var(txn.var_start) int(1)
http-response set-var(txn.var_length) int(3)
http-response set-header bytes_var1_var3    "%[var(txn.input),bytes(txn.var_start,txn.var_length)]"  # outputs "123"
```

<a id="entry-7-3-1-capture-req"></a>

**`capture-req(<id>)`**

```haproxy
capture-req(<id>)
```

Captura la entrada de cadena en el slot de solicitud `<id>` y devuelve la entrada tal cual. Si el
slot no existe, la captura falla silenciosamente.

Ver también: "declare capture", "http-request capture", "http-response capture",
"capture.req.hdr" y "capture.res.hdr" (obtenciones de muestras).

<a id="entry-7-3-1-capture-res"></a>

**`capture-res(<id>)`**

```haproxy
capture-res(<id>)
```

Captura la entrada de cadena en el slot de respuesta `<id>` y devuelve la entrada tal cual. Si el
slot no existe, la captura falla silenciosamente.

Ver también: "declare capture", "http-request capture", "http-response capture",
"capture.req.hdr" y "capture.res.hdr" (obtenciones de muestras).

<a id="entry-7-3-1-concat"></a>

**`concat([<start>[,<var>[,<end>]]])`**

```haproxy
concat([<start>[,<var>[,<end>]]])
```

Concatena hasta 3 campos después de la muestra actual, que luego se convierte en cadena. El
primero, `<start>`, es una cadena constante que se añadirá inmediatamente después de la muestra
existente. Puede omitirse si no se usa. El segundo, `<var>`, es un nombre de variable. La variable
se buscará, su contenido se convertirá a cadena y se añadirá inmediatamente después de la parte
`<first>`. Si la variable no se encuentra, no se añade nada. También puede omitirse. El tercer
campo, `<end>`, es una cadena constante que se añadirá después de la variable. También puede
omitirse. Juntos, estos elementos permiten concatenar variables con delimitadores a un conjunto
existente de variables. Esto puede usarse para construir nuevas variables formadas por una
sucesión de otras variables, como valores delimitados por dos puntos. Si se necesitan comas o
paréntesis de cierre como delimitadores, deben protegerse con comillas o barras invertidas, ellas
mismas protegidas para que no las elimine el analizador de primer nivel. A menudo se usa para
construir variables compuestas a partir de otras, pero a veces usar una cadena de formato con
múltiples campos puede ser más cómodo. Ver ejemplos más abajo.

Ejemplo:

```text
tcp-request session set-var(sess.src) src
tcp-request session set-var(sess.dn)  ssl_c_s_dn
tcp-request session set-var(txn.sig) str(),concat(<ip=,sess.ip,>),concat(<dn=,sess.dn,>)
tcp-request session set-var(txn.ipport) "str(),concat('addr=(',sess.ip),concat(',',sess.port,')')"
tcp-request session set-var-fmt(txn.ipport) "addr=(%[sess.ip],%[sess.port])"  ## does the same
http-request set-header x-hap-sig %[var(txn.sig)]
```

<a id="entry-7-3-1-cpl"></a>

**`cpl`**

```haproxy
cpl
```

Toma el valor de entrada de tipo entero con signo, aplica un complemento a uno (invierte todos los
bits) y devuelve el resultado como un entero con signo.

<a id="entry-7-3-1-crc32"></a>

**`crc32([<avalanche>])`**

```haproxy
crc32([<avalanche>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
función hash CRC32. Opcionalmente, es posible aplicar una función hash de avalancha completa a la
salida si el argumento opcional `<avalanche>` es igual a 1. Este conversor usa las mismas
funciones que usan los diversos algoritmos de balanceo de carga basados en hash, por lo que
proporcionará exactamente los mismos resultados. Se proporciona por compatibilidad con otro
software que quiere que se calcule un CRC32 sobre algunas claves de entrada, así que sigue la
implementación más común, la que se encuentra en Ethernet, Gzip, PNG, etc. Es más lento que los
otros algoritmos, pero puede proporcionar una distribución mejor o, al menos, menos predecible. No
debe usarse con fines de seguridad, ya que romper un hash de 32 bits es trivial. Ver también
"djb2", "sdbm", "wt6", "crc32c" y la directiva "hash-type".

<a id="entry-7-3-1-crc32c"></a>

**`crc32c([<avalanche>])`**

```haproxy
crc32c([<avalanche>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
función hash CRC32C. Opcionalmente, es posible aplicar una función hash de avalancha completa a la
salida si el argumento opcional `<avalanche>` es igual a 1. Este conversor usa las mismas
funciones que las descritas en el RFC4960, Apéndice B [8]. Se proporciona por compatibilidad con
otro software que quiere que se calcule un CRC32C sobre algunas claves de entrada. Es más lento
que los otros algoritmos y no debe usarse con fines de seguridad, ya que romper un hash de 32 bits
es trivial. Ver también "djb2", "sdbm", "wt6", "crc32" y la directiva "hash-type".

<a id="entry-7-3-1-cut-crlf"></a>

**`cut_crlf`**

```haproxy
cut_crlf
```

Corta la representación en cadena de la muestra de entrada en el primer retorno de carro
('&#92;r') o salto de línea ('&#92;n') encontrado. Solo se
actualiza la longitud de la cadena.

<a id="entry-7-3-1-da-csv-conv"></a>

**`da-csv-conv(<prop>[,<prop>*])`**

```haproxy
da-csv-conv(<prop>[,<prop>*])
```

Pide al conversor DeviceAtlas que identifique la cadena de User Agent pasada en la entrada y que
emita una cadena formada por la concatenación de las propiedades enumeradas en el argumento,
delimitadas por el separador definido por la palabra clave global
"deviceatlas-property-separator", o por defecto el carácter barra vertical ('\|'). Hay un límite
de 12 propiedades diferentes impuesto por el lenguaje de configuración de HAProxy.

Ejemplo:

```text
frontend www
  bind *:8881
  default_backend servers
  http-request set-header X-DeviceAtlas-Data %[req.fhdr(User-Agent),da-csv(primaryHardwareType,osName,osVersion,browserName,browserVersion,browserRenderingEngine)]
```

<a id="entry-7-3-1-date"></a>

**`date`**

```haproxy
date
```

Este conversor se usa para convertir una fecha de una cabecera HTTP. Puede ser una fecha IMF, una
fecha ASCTIME o una fecha RFC850. Devolverá una marca de tiempo UNIX.

Ejemplo:

```text
http-request return lf-string "%[str('Sun, 06 Nov 1994 08:49:37 GMT'),date]\n" content-type text/plain
```

<a id="entry-7-3-1-debug"></a>

**`debug([<prefix][,<destination>])`**

```haproxy
debug([<prefix][,<destination>])
```

Este conversor se usa como herramienta de depuración. Toma una captura de la muestra de entrada y
la envía al sumidero de eventos `<destination>`, que puede designar un búfer circular como "buf0",
así como "stdout" o "stderr". Los sumideros disponibles pueden comprobarse en tiempo de ejecución
emitiendo "show events" en la CLI. Cuando no se especifica, la salida será "buf0", que puede
consultarse mediante el comando "show events" de la CLI. Puede pasarse un prefijo opcional
`<prefix>` para ayudar a distinguir salidas de múltiples expresiones. Aparecerá entonces antes de
los dos puntos en el mensaje de salida. La muestra de entrada se pasa tal cual a la salida, de
modo que es seguro insertar el conversor debug en cualquier punto de una cadena, incluso con tipos
de muestra no imprimibles.

Ejemplo:

```text
tcp-request connection track-sc0 src,debug(track-sc)
```

<a id="entry-7-3-1-digest"></a>

**`digest(<algorithm>)`**

```haproxy
digest(<algorithm>)
```

Convierte una muestra binaria de entrada en un resumen de mensaje. El resultado es una muestra
binaria. `<algorithm>` debe ser un nombre de resumen de mensaje de OpenSSL (p. ej. sha256).

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

<a id="entry-7-3-1-div"></a>

**`div(<value>)`**

```haproxy
div(<value>)
```

Divide el valor de entrada de tipo entero con signo por `<value>` y devuelve el resultado como un
entero con signo. Si `<value>` es nulo, se devuelve el mayor entero sin signo (típicamente
2^63-1). `<value>` puede ser un valor numérico o un nombre de variable. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-1-djb2"></a>

**`djb2([<avalanche>])`**

```haproxy
djb2([<avalanche>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
función hash DJB2. Opcionalmente, es posible aplicar una función hash de avalancha completa a la
salida si el argumento opcional `<avalanche>` es igual a 1. Este conversor usa las mismas
funciones que usan los diversos algoritmos de balanceo de carga basados en hash, por lo que
proporcionará exactamente los mismos resultados. Está destinado principalmente a la depuración,
pero puede usarse como entrada de una tabla de persistencia para recopilar estadísticas
aproximadas. No debe usarse con fines de seguridad, ya que romper un hash de 32 bits es trivial.
Ver también "crc32", "sdbm", "wt6", "crc32c" y la directiva "hash-type".

<a id="entry-7-3-1-eth-data"></a>

**`eth.data`**

```haproxy
eth.data
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Omite toda la cabecera
Ethernet, incluidas las posibles VLAN, y devuelve un bloque de datos binarios que comienza en el
protocolo de capa 3 (normalmente IPv4 o IPv6). Ver también "fc_saved_syn" y "tcp-ss".

<a id="entry-7-3-1-eth-dst"></a>

**`eth.dst`**

```haproxy
eth.dst
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Devuelve los 6 bytes de
la cabecera Ethernet correspondientes a la dirección de destino de la trama, como bloque binario.
Ver también "fc_saved_syn" y "tcp-ss".

<a id="entry-7-3-1-eth-hdr"></a>

**`eth.hdr`**

```haproxy
eth.hdr
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Recorta todo lo que
haya más allá de la cabecera Ethernet pero conserva las posibles VLAN, y devuelve esta cabecera
como bloque de datos binarios. Ver también "fc_saved_syn" y "tcp-ss".

<a id="entry-7-3-1-eth-proto"></a>

**`eth.proto`**

```haproxy
eth.proto
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Devuelve el número de
protocolo (también conocido como EtherType) encontrado en una cabecera Ethernet tras cualquier
VLAN opcional, como valor entero. Normalmente debería ser 0x800 para IPv4 o 0x86DD para IPv6. Ver
también "fc_saved_syn" y "tcp-ss".

<a id="entry-7-3-1-eth-src"></a>

**`eth.src`**

```haproxy
eth.src
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Devuelve los 6 bytes de
la cabecera Ethernet correspondientes a la dirección de origen de la trama, como bloque binario.
Ver también "fc_saved_syn" y "tcp-ss".

<a id="entry-7-3-1-eth-vlan"></a>

**`eth.vlan`**

```haproxy
eth.vlan
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "2". Devuelve el último ID
de VLAN encontrado en una cabecera Ethernet como valor entero. Ver también "fc_saved_syn" y
"tcp-ss".

<a id="entry-7-3-1-even"></a>

**`even`**

```haproxy
even
```

Devuelve un booleano TRUE si el valor de entrada de tipo entero con signo es par; en caso
contrario devuelve FALSE. Es funcionalmente equivalente a "not,and(1),bool".

<a id="entry-7-3-1-field"></a>

**`field(<index>,<delimiters>[,<count>])`**

```haproxy
field(<index>,<delimiters>[,<count>])
```

Extrae la subcadena en el índice dado contando desde el principio (índice positivo) o desde el
final (índice negativo) considerando los delimitadores dados de una cadena de entrada. Los índices
comienzan en 1 o -1 y los delimitadores son una lista de caracteres con formato de cadena.
Opcionalmente puedes especificar el `<count>` de campos a extraer (predeterminado: 1). El valor 0
indica la extracción de todos los campos restantes.

Ejemplo:

```text
str(f1_f2_f3__f5),field(4,_)    # <empty>
str(f1_f2_f3__f5),field(5,_)    # f5
str(f1_f2_f3__f5),field(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),field(2,_,2)  # f2_f3
str(f1_f2_f3__f5),field(-2,_,3) # f2_f3_
str(f1_f2_f3__f5),field(-3,_,0) # f1_f2_f3
```

<a id="entry-7-3-1-fe-exists"></a>

**`fe_exists`**

```haproxy
fe_exists
```

Toma un nombre de frontend como valor de entrada y devuelve un booleano TRUE si dicho frontend con
ese nombre existe en la configuración actual; en caso contrario devuelve FALSE. Puede usarse en
lugares donde comprobar la existencia de un frontend a partir de un nombre dinámico es valioso,
como búsquedas en mapas o respuestas a una comprobación externa.

Ejemplo:

```text
http-request deny unless { var(txn.fe_name),fe_exists }
```

<a id="entry-7-3-1-fix-is-valid"></a>

**`fix_is_valid`**

```haproxy
fix_is_valid
```

Analiza una carga binaria y realiza comprobaciones de coherencia respecto a FIX (Financial
Information eXchange):

- comprueba que todos los IDs de tag y valores no estén vacíos y que los IDs de tags sean
  realmente numéricos
- comprueba que el tag BeginString sea el primer tag con una versión de FIX válida
- comprueba que el tag BodyLength sea el segundo con la longitud de cuerpo correcta
- comprueba que el tag MsgType sea el tercer tag.
- comprueba que el último tag del mensaje sea el tag CheckSum con una suma de comprobación válida

Debido al diseño actual de HAProxy, solo puede analizarse el primer mensaje enviado por el cliente
y el servidor.

Este conversor devuelve un booleano: true si la carga contiene un mensaje FIX válido, false si no.

Ver también el conversor fix_tag_value.

Ejemplo:

```text
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
```

<a id="entry-7-3-1-fix-tag-value"></a>

**`fix_tag_value(<tag>)`**

```haproxy
fix_tag_value(<tag>)
```

Analiza un mensaje FIX (Financial Information eXchange) y extrae el valor del tag `<tag>`. `<tag>`
puede ser una cadena o un entero que apunte al tag deseado. Se acepta cualquier valor entero, pero
solo las siguientes cadenas se traducen a su equivalente entero: BeginString, BodyLength, MsgType,
SenderCompID, TargetCompID, CheckSum. Pueden añadirse fácilmente más nombres de tags.

Debido al diseño actual de HAProxy, solo puede analizarse el primer mensaje enviado por el cliente
y el servidor. Este conversor no realiza ninguna validación del mensaje. Es muy recomendable
validar primero el mensaje usando el conversor fix_is_valid.

Ver también el conversor fix_is_valid.

Ejemplo:

```shell
tcp-request inspect-delay 10s
tcp-request content reject unless { req.payload(0,0),fix_is_valid }
# MsgType tag ID is 35, so both lines below will return the same content
tcp-request content set-var(txn.foo) req.payload(0,0),fix_tag_value(35)
tcp-request content set-var(txn.bar) req.payload(0,0),fix_tag_value(MsgType)
```

<a id="entry-7-3-1-has-ctl"></a>

**`has_ctl([mask])`**

```haproxy
has_ctl([mask])
```

Comprueba en la muestra binaria de entrada los caracteres de control definidos por el argumento de
máscara. La máscara es un número de 33 bits (decimal o hexadecimal con prefijo "0x"), que tiene un
bit activado por cada carácter a detectar en el rango 0x00 a 0x1F, y el bit 32 activado para
coincidir con el carácter DEL (0x7F). Cuando no se especifica máscara, el conversor usará el valor
0x1FFFFFDFF, que coincide con todos los caracteres de control excepto TAB (0x09), de uso común en
cabeceras HTTP. La máscara especial "any" corresponde a 0x1FFFFFFFF, que coincidirá con todos los
caracteres de control, TAB incluido. La máscara especial "http" corresponde a 0x2401 y solo hará
que se detecten los caracteres de control prohibidos en valores de cabeceras HTTP, que son CR
(0x0D), LF (0x0A) y NUL (0x00).

Ejemplos:

```shell
# reject presence of DEL, CR, LF, NUL characters in the referer header
http-request deny if { req.fhdr(referer),has_ctl(0x100002401) }
# reject presence of any control char but tab in any HTTP header value
http-request deny if { req.hdr(),has_ctl }
```

<a id="entry-7-3-1-hex"></a>

**`hex`**

```haproxy
hex
```

Convierte una muestra binaria de entrada en una cadena hexadecimal que contiene dos dígitos
hexadecimales por byte de entrada. Se usa para registrar o transferir volcados hexadecimales de
algunos datos binarios de entrada de una forma en la que puedan transferirse de manera fiable
(p. ej. un ID SSL puede copiarse en una cabecera).

<a id="entry-7-3-1-hex2i"></a>

**`hex2i`**

```haproxy
hex2i
```

Convierte una cadena hexadecimal que contiene dos dígitos hexadecimales por byte de entrada en un
entero. Si el valor de entrada contiene un carácter que no es un dígito hexadecimal, el conversor
falla y no devuelve nada, lo que posibilita diferenciar una entrada inválida de un cero válido.

<a id="entry-7-3-1-hmac"></a>

**`hmac(<algorithm>,<key>)`**

```haproxy
hmac(<algorithm>,<key>)
```

Convierte una muestra binaria de entrada en un código de autenticación de mensajes con la clave
dada. El resultado es una muestra binaria. `<algorithm>` debe ser uno de los nombres de resumen de
mensaje de OpenSSL registrados (p. ej. sha256). El parámetro `<key>` debe estar codificado en
base64 y puede ser una cadena o una variable.

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

<a id="entry-7-3-1-host-only"></a>

**`host_only`**

```haproxy
host_only
```

Convierte una cadena que contiene un valor de cabecera Host y elimina su puerto. La entrada debe
respetar el formato del valor de la cabecera host (rfc9110#section-7.2). Soportará ese tipo de
entrada: hostname, hostname:80, 127.0.0.1, 127.0.0.1:80, [::1], [::1]:80.

Este conversor además convierte la cadena a minúsculas.

Ver también: el conversor "port_only", que devolverá el puerto.

<a id="entry-7-3-1-htonl"></a>

**`htonl`**

```haproxy
htonl
```

Convierte el valor entero de entrada a su representación binaria de 32 bits en el orden de bytes
de red. Como las obtenciones de muestras manejan enteros de 64 bits con signo, cuando se usa este
conversor, el valor entero de entrada se convierte primero a un entero sin signo de 32 bits.

<a id="entry-7-3-1-http-date"></a>

**`http_date([<offset[,<unit>]])`**

```haproxy
http_date([<offset[,<unit>]])
```

Convierte un entero que se supone contiene una fecha desde epoch en una cadena que
representa esta fecha en un formato adecuado para su uso en campos de cabecera HTTP. Si se
especifica un valor de desplazamiento, se añade a la fecha antes de realizar la conversión. Esto
es particularmente útil para emitir campos de cabecera Date, valores Expires en respuestas cuando
se combina con un desplazamiento positivo, o valores Last-Modified cuando el desplazamiento es
negativo. Si se especifica un valor de unidad, considera la marca de tiempo como "s" para segundos
(comportamiento predeterminado), "ms" para milisegundos o "us" para microsegundos desde epoch. Se
asume que el desplazamiento tiene la misma unidad que la marca de tiempo de entrada.

<a id="entry-7-3-1-iif"></a>

**`iif(<true>,<false>)`**

```haproxy
iif(<true>,<false>)
```

Devuelve la cadena `<true>` si el valor de entrada es verdadero. En caso contrario devuelve la
cadena `<false>`.

Ejemplo:

```text
http-request set-header x-forwarded-proto %[ssl_fc,iif(https,http)]
```

<a id="entry-7-3-1-in-table"></a>

**`in_table([<table>])`**

```haproxy
in_table([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve un
booleano false. En caso contrario se devuelve un booleano true. Esto puede usarse para verificar
la presencia de una determinada clave en una tabla que rastrea algunos elementos (p. ej. si ya se
vio o no una dirección IP de origen o una cabecera Authorization).

<a id="entry-7-3-1-ip-data"></a>

**`ip.data`**

```haproxy
ip.data
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Omite la cabecera IP y cualquier opción o extensión opcional, y devuelve un bloque de
datos binarios que comienza en el protocolo de transporte (normalmente TCP o UDP). Ver también
"fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-df"></a>

**`ip.df`**

```haproxy
ip.df
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve el valor entero 1 si el flag DF (don't fragment) está activado en la cabecera
IP, 0 en caso contrario. IPv6 no tiene flag DF y no fragmenta por defecto, así que siempre
devuelve 1. Ver también "fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-dst"></a>

**`ip.dst`**

```haproxy
ip.dst
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve la dirección IPv4 o IPv6 de destino de la cabecera IPv4/v6. Ver también
"fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-fp"></a>

**`ip.fp([<mode>])`**

```haproxy
ip.fp([<mode>])
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Inspecciona varias partes de la cabecera IP y de la cabecera TCP para construir una
especie de huella dactilar de las partes invariables, que puede usarse para distinguir entre
múltiples hosts aparentemente idénticos. El caso de uso real es refinar la identificación de hosts
con mal comportamiento tras una dirección IP compartida, para evitar bloquear a usuarios legítimos
cuando solo uno se comporta mal y debe bloquearse. El conversor construye un bloque binario mínimo
de 8 bytes a partir de la entrada. Los bytes de la huella se organizan así: - byte 0: campo IP TOS
(ver ip.tos) - byte 1: - bit 7: IPv6 (1) / IPv4 (0) - bit 6: ip.df - bit 5..4: 0:ip.ttl\<=32;
1:ip.ttl\<=64; 2:ip.ttl\<=128; 3:ip.ttl\<=255 - bit 3: opciones IP presentes (1) / ausentes (0) -
bit 2: datos TCP presentes (1) / ausentes (0) - bit 1: TCP.flags con CWR activado (1) /
desactivado (0) - bit 0: TCP.flags con ECE activado (1) / desactivado (0) - byte 2: - bits 7..4:
longitud de la cabecera TCP en palabras de 4 bytes - bits 3..0: TCP window scaling + 1 (1..15) /
0 (sin WS anunciado) - byte 3..4: tcp.win - byte 5..6: tcp.options.mss, o cero si está ausente -
byte 7: 1 bit por cada opción TCP presente, con las opciones 2 a 8 mapeadas a los bits 0..6
respectivamente, y el bit 7 indicando la presencia de cualquier opción de la 9 a la 255.

El argumento `<mode>` permite añadir más información a la huella. Por defecto, cuando el argumento
`<mode>` no está establecido o es cero, la huella se compone únicamente de los 8 bytes descritos
anteriormente. Si `<mode>` se especifica con otro valor, corresponde entonces a la suma de los
siguientes valores, y los componentes respectivos se concatenarán a la huella, en el orden
siguiente: - 1: el valor TTL recibido se añade a la huella (1 byte) - 2: la lista de tipos de
opciones TCP, tal como la devuelve "tcp.options_list", formada por 0 a 40 bytes extra, se añade a
la huella - 4: la dirección IP de origen se añade a la huella, lo que suma 4 bytes para IPv4 y 16
para IPv6.

Ejemplo: crear una huella de 13..25 bytes usando el FP base, el TTL y la dirección de origen
(1+4=5):

    frontend test
        mode http
        bind :4445 tcp-ss 1
        tcp-request connection set-var(sess.syn) fc_saved_syn
        http-request return status 200 content-type text/plain lf-string &#92;
              "src=%[var(sess.syn),ip.src] fp=%[var(sess.syn),ip.fp(5),hex]&#92;n"

Ver también "fc_saved_syn", "tcp-ss", "eth.data", "ip.df", "ip.ttl", "tcp.win",
"tcp.options.mss" y "tcp.options_list".

<a id="entry-7-3-1-ip-hdr"></a>

**`ip.hdr`**

```haproxy
ip.hdr
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve un bloque de datos binarios que comienza con la cabecera IP y se detiene tras
la última opción o extensión, y antes de la cabecera del protocolo de transporte. Ver también
"fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-proto"></a>

**`ip.proto`**

```haproxy
ip.proto
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve el número de protocolo de transporte, normalmente 6 para TCP o 17 para UDP.
Ver también "fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-src"></a>

**`ip.src`**

```haproxy
ip.src
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve la dirección IPv4 o IPv6 de origen de la cabecera IPv4/v6. Ver también
"fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-tos"></a>

**`ip.tos`**

```haproxy
ip.tos
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve un entero correspondiente al valor del campo type-of-service (TOS) de la
cabecera IPv4 o del campo traffic class (TC) de la cabecera IPv6. Ten en cuenta que en el internet
moderno este campo contiene con mayor frecuencia un valor DSCP (Differentiated Services
Codepoint) en los 6 bits superiores, y los dos bits inferiores o no se usan, o los usa IP ECN.
Consulta el RFC2474 y el RFC8436 para los valores DSCP, y el RFC3168 para los campos IP ECN. Ver
también "fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-ttl"></a>

**`ip.ttl`**

```haproxy
ip.ttl
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve un entero correspondiente al campo TTL (Time To Live) o HL (Hop Limit) de la
cabecera IPv4/IPv6. Este valor suele estar preestablecido a un valor fijo y lo decrementa cada
router que cruza el paquete. Puede ayudar a inferir a qué distancia se conecta un cliente cuando se
conoce el valor inicial. Ten en cuenta que la mayoría de los sistemas operativos modernos
comienzan con un valor inicial de 64. Ver también "fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ip-ver"></a>

**`ip.ver`**

```haproxy
ip.ver
```

Se usa con una muestra de entrada que representa una trama Ethernet binaria, tal como la devuelve
"fc_saved_syn" combinada con la opción de bind "tcp-ss" establecida a "1", o con la salida de
"eth.data". Devuelve la versión IP de la cabecera IP, normalmente 4 o 6. Ten en cuenta que esto no
comprueba si coincide el número de protocolo de la trama Ethernet de capa superior, pero como se
espera que se use con paquetes válidos, se espera que el sistema operativo ya lo haya verificado.
Ver también "fc_saved_syn", "tcp-ss" y "eth.data".

<a id="entry-7-3-1-ipmask"></a>

**`ipmask(<mask4>[,<mask6>])`**

```haproxy
ipmask(<mask4>[,<mask6>])
```

Aplica una máscara a una dirección IP y usa el resultado para búsquedas y almacenamiento. Esto
puede usarse para que todos los hosts dentro de una determinada máscara compartan las mismas
entradas de tabla y, por tanto, usen el mismo servidor. La mask4 puede pasarse en forma de puntos
(p. ej. 255.255.255.0) o en forma CIDR (p. ej. 24). La mask6 puede pasarse en grupos de cuatro dígitos hexadecimales
(p. ej. ffff:ffff::) o en forma CIDR (p. ej. 64). Si no se da mask6, las direcciones IPv6 fallarán
al convertir por motivos de compatibilidad con versiones anteriores.

<a id="entry-7-3-1-json"></a>

**`json([<input-code>])`**

```haproxy
json([<input-code>])
```

Escapa la cadena de entrada y produce una cadena de salida ASCII lista para usarse como cadena
JSON. El conversor intenta decodificar la cadena de entrada según el parámetro `<input-code>`.
Puede ser "ascii", "utf8", "utf8s", "utf8p" o "utf8ps". El decodificador "ascii" nunca falla. El
decodificador "utf8" detecta 3 tipos de errores:

- secuencia UTF-8 errónea (byte de continuación huérfano, número erróneo de bytes de
  continuación, ...)
- rango inválido (el valor decodificado está dentro de un rango prohibido de UTF-8),
- código demasiado largo (el valor está codificado con más bytes de los necesarios).

La codificación UTF-8 de JSON puede producir un error de «valor demasiado largo» cuando el carácter
UTF-8 es mayor que 0xffff, porque la especificación de escape de cadenas JSON solo autoriza 4
dígitos hexadecimales para la codificación del valor. El decodificador UTF-8 existe en 4 variantes
designadas por una combinación de dos letras sufijo: "p" de «permisivo» y "s" de «ignorar
silenciosamente». Los comportamientos de los decodificadores son:

- "ascii" : nunca falla;
- "utf8" : falla ante cualquier error detectado;
- "utf8s" : nunca falla, pero elimina los caracteres correspondientes a errores;
- "utf8p" : acepta y corrige los errores de código demasiado largo, pero falla ante cualquier otro
  error;
- "utf8ps": nunca falla, acepta y corrige los errores de código demasiado largo, pero elimina los
  caracteres correspondientes a los otros errores.

Este conversor es particularmente útil para construir JSON correctamente escapado para el registro
en servidores que consumen registros de tráfico con formato JSON.

Ejemplo:

```text
capture request header Host len 15
capture request header user-agent len 150
log-format '{"ip":"%[src]","user-agent":"%[capture.req.hdr(1),json(utf8s)]"}'
```

Solicitud de entrada del cliente 127.0.0.1:

```text
GET / HTTP/1.0
User-Agent: Very "Ugly" UA 1/2
```

Registro de salida:

```text
{"ip":"127.0.0.1","user-agent":"Very \"Ugly\" UA 1\/2"}
```

<a id="entry-7-3-1-json-query"></a>

**`json_query(<json_path>[,<output_type>])`**

```haproxy
json_query(<json_path>[,<output_type>])
```

El conversor json_query soporta los tipos JSON string, boolean, number y array. Los números en
coma flotante se devolverán como cadena. Especificando el output_type 'int', el valor se convertirá a un entero. Los arrays se devolverán como cadena, comenzando y terminando con
corchetes. El contenido es un CSV. Dependiendo del tipo de dato, los valores del array pueden ir
entre comillas. Si los valores del array son tipos complejos, la cadena contiene la representación
json completa de cada valor separada por una coma. Resultado de ejemplo para una consulta de roles
a un JWT:

```text
["manage-account","manage-account-links","view-profile"]
```

Si la conversión no es posible, el conversor json_query falla.

`<json_path>` debe ser una cadena JSON Path válida tal como se define en
<https://datatracker.ietf.org/doc/draft-ietf-jsonpath-base/>

Nota: dependiendo del contexto y de la implementación subyacente, la extracción de claves JSON
duplicadas está sin definir y podría devolver la primera, la última o cualquier otra aparición de
la misma clave del contenido de entrada, y si se pasan nombres de clave codificados, podrían no
coincidir siempre. En resumen, este conversor no es adecuado para la sanitización de contenido.

Ejemplo:

```shell
# get a integer value from the request body
# "{"integer":4}" => 5
http-request set-var(txn.pay_int) req.body,json_query('$.integer','int'),add(1)

# get a key with '.' in the name
# {"my.key":"myvalue"} => myvalue
http-request set-var(txn.pay_mykey) req.body,json_query('$.my\\.key')

# {"boolean-false":false} => 0
http-request set-var(txn.pay_boolean_false) req.body,json_query('$.boolean-false')

# get the value of the key 'iss' from a JWT Bearer token
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec,json_query('$.iss')
```

<a id="entry-7-3-1-jwt-decrypt-cert"></a>

**`jwt_decrypt_cert(<cert>)`**

```haproxy
jwt_decrypt_cert(<cert>)
```

Realiza una validación de firma de un JSON Web Token que sigue el formato JSON Web Encryption (ver
RFC 7516) dado en la entrada y devuelve su contenido descifrado gracias al certificado
proporcionado. El parámetro `<cert>` debe ser una ruta a un certificado ya cargado (que puede
volcarse mediante el comando CLI "dump ssl cert"). El certificado debe tener su opción "jwt"
explícitamente establecida en "on" (ver la opción "jwt" de crt-list). Puede proporcionarse
directamente o mediante una variable. Los únicos tokens gestionados por ahora son los que usan el
formato Compact Serialization (cinco cadenas codificadas en base64-url separadas por puntos).

Este conversor puede usarse para tokens que tienen un algoritmo (campo "alg" de la cabecera JOSE)
entre los siguientes: RSA-OAEP, RSA-OAEP-256, ECDH-ES, ECDH-ES+A128KW, ECDH-ES+A192KW o
ECDH-ES+A256KW. El algoritmo RSA1_5 está implementado pero deshabilitado por defecto, siguiendo lo
sugerido en la [sección
3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) del RFC 8725. Puede reactivarse si se necesita gracias a la opción global 'jwt.decrypt_alg_list'.

Los algoritmos y algoritmos de cifrado soportados (campos "alg" y "enc" de la cabecera JOSE,
respectivamente) pueden modificarse gracias a las opciones globales 'jwt.decrypt_alg_list' y
'jwt.decrypt_enc_list'.

El token JWE debe proporcionarse codificado en base64url y la salida se proporcionará "raw". Si
ocurre un error durante el análisis del token, la verificación de la firma o el descifrado del
contenido, se devolverá una cadena vacía.

Ejemplo:

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_cert("/foo/bar.pem")]
```

<a id="entry-7-3-1-jwt-decrypt-jwk"></a>

**`jwt_decrypt_jwk(<jwk>)`**

```haproxy
jwt_decrypt_jwk(<jwk>)
```

Realiza una validación de firma de un JSON Web Token que sigue el formato JSON Web Encryption (ver
RFC 7516) dado en la entrada y devuelve su contenido descifrado gracias a la JSON Web Key
proporcionada (RFC7517). El parámetro `<jwk>` debe ser un JWK válido de tipo 'oct', 'EC' o 'RSA'
(campo 'kty' de la clave JSON) que puede proporcionarse como cadena o mediante una variable.

Los únicos tokens gestionados por ahora son los que usan el formato Compact Serialization (cinco
cadenas codificadas en base64-url separadas por puntos).

Este conversor puede usarse para decodificar tokens que tienen un algoritmo de tipo simétrico
(campo "alg" de la cabecera JOSE) entre los siguientes: A128KW, A192KW, A256KW, A128GCMKW,
A192GCMKW, A256GCMKW, dir. En este caso, esperamos que el JWK proporcionado sea de tipo 'oct'.

Este conversor también gestiona tokens que tienen un algoritmo (campo "alg" de la cabecera JOSE)
de la familia RSA (RSA-OAEP o RSA-OAEP-256) cuando se proporciona un JWK 'RSA', o de la familia
ECDH (ECDH-ES, ECDH-ES+A128KW, ECDH-ES+A192KW o ECDH-ES+A256KW) cuando se proporciona un JWK 'EC'.
El algoritmo RSA1_5 está implementado pero deshabilitado por defecto, siguiendo lo sugerido en la [sección 3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) del RFC 8725. Puede
reactivarse si se necesita gracias a la opción global 'jwt.decrypt_alg_list'.

Ten en cuenta que los algoritmos A128KW y A192KW no están disponibles en AWS-LC, así que los
algoritmos A128KW, A192KW, ECDH-ES+A128KW y ECDH-ES+A192KW no funcionarán.

Los algoritmos y algoritmos de cifrado soportados (campos "alg" y "enc" de la cabecera JOSE,
respectivamente) pueden modificarse gracias a las opciones globales 'jwt.decrypt_alg_list' y
'jwt.decrypt_enc_list'.

El token JWE debe proporcionarse codificado en base64url y la salida se proporcionará "raw". Si
ocurre un error durante el análisis del token, la verificación de la firma o el descifrado del
contenido, se devolverá una cadena vacía.

Debido a la forma en que se tratan las comillas, las comas y las comillas dobles en la
configuración, el contenido del JWK debe escaparse correctamente para que este conversor funcione
correctamente (consulta la [sección 2.2](/es/haproxy/configuration-basics/#section-2-2) para más
información).

Ejemplo:

```shell
 # Get a JWT from the authorization header, put its decrypted content in an
 # HTTP header
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(\'{\"kty\":\"oct\",\"k\":\"wAsgsg\"}\')

# or via a variable
 http-request set-var(txn.bearer) http_auth_bearer
 http-request set-var(txn.jwk) str(\'{\"kty\":\"oct\",\"k\":\"Q-NFLlghQ\"}\')
 http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_jwk(txn.jwk)
```

<a id="entry-7-3-1-jwt-decrypt-secret"></a>

**`jwt_decrypt_secret(<secret>)`**

```haproxy
jwt_decrypt_secret(<secret>)
```

Realiza una validación de firma de un JSON Web Token que sigue el formato JSON Web Encryption (ver
RFC 7516) dado en la entrada y devuelve su contenido descifrado gracias al secreto codificado en
base64 proporcionado. El secreto puede darse como cadena o mediante una variable. Los únicos
tokens gestionados por ahora son los que usan el formato Compact Serialization (cinco cadenas
codificadas en base64-url separadas por puntos).

Este conversor puede usarse para tokens que tienen un algoritmo (campo "alg" de la cabecera JOSE)
entre los siguientes: A128KW, A192KW, A256KW, A128GCMKW, A192GCMKW, A256GCMKW, dir. Ten en cuenta
que los algoritmos A128KW y A192KW no están disponibles en AWS-LC y el descifrado no funcionará.

El token JWE debe proporcionarse codificado en base64url y la salida se proporcionará "raw". Si
ocurre un error durante el análisis del token, la verificación de la firma o el descifrado del
contenido, se devolverá una cadena vacía.

Ejemplo:

```shell
# Get a JWT from the authorization header, put its decrypted content in an
# HTTP header
http-request set-var(txn.bearer) http_auth_bearer
http-request set-header X-Decrypted %[var(txn.bearer),jwt_decrypt_secret("GawgguFyGrWKav7AX4VKUg")]
```

<a id="entry-7-3-1-jwt-header-query"></a>

**`jwt_header_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_header_query([<json_path>[,<output_type>]])
```

Dado un JSON Web Token (JWT) en la entrada, devuelve la parte de cabecera decodificada del token
(la primera parte codificada en base64-url del JWT) si no se da ningún parámetro, o realiza una
json_query sobre la parte de cabecera decodificada del token. Consulta el conversor "json_query"
para más detalles sobre los parámetros json_path y output_type aceptados. Este conversor puede
usarse con tokens JWS o JWE siempre que estén en el formato Compact Serialization.

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

<a id="entry-7-3-1-jwt-payload-query"></a>

**`jwt_payload_query([<json_path>[,<output_type>]])`**

```haproxy
jwt_payload_query([<json_path>[,<output_type>]])
```

Dado un JSON Web Token (JWT) del formato JSON Web Signed (JWS) en la entrada, devuelve la parte de
carga (payload) decodificada del token (la segunda parte codificada en base64-url del JWT) si no
se da ningún parámetro, o realiza una json_query sobre la parte de carga decodificada del token.
Consulta el conversor "json_query" para más detalles sobre los parámetros json_path y output_type
aceptados.

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

jwt_verify(`<alg>`,`<key>`)

Realiza una verificación de firma para el JSON Web Token (JWT) dado en la entrada usando el
algoritmo `<alg>` y el parámetro `<key>`. Por ahora, solo pueden procesarse tokens JWS que usen el
formato Compact Serialization (tres cadenas codificadas en base64-url separadas por puntos). Este
conversor solo verifica la firma del token y no realiza una validación JWT completa tal como se
especifica en la [sección 7.2](https://www.rfc-editor.org/rfc/rfc7519#section-7.2) del
RFC7519. Por ejemplo, no nos aseguramos de que los contenidos de la cabecera y de la carga sean
JSON completamente válidos una vez decodificados, y no se realiza ninguna comprobación respecto a
sus contenidos respectivos.

- `<alg>` puede ser una cadena o un nombre de variable (ver también "set-var") que contenga el
  nombre del algoritmo usado para verificar.

  Se gestionan los algoritmos mencionados en la [sección 3.1](https://www.rfc-editor.org/rfc/rfc7518#section-3.1) del RFC7518:

```text
   +--------------+---------------------------------------------------------+
   | Param. "alg" | Algoritmo de firma digital o MAC                        |
   | Valor        |                                                         |
   +--------------+---------------------------------------------------------+
   | HS256        | HMAC con SHA-256                                        |
   | HS384        | HMAC con SHA-384                                        |
   | HS512        | HMAC con SHA-512                                        |
   | RS256        | RSASSA-PKCS1-v1_5 con SHA-256                           |
   | RS384        | RSASSA-PKCS1-v1_5 con SHA-384                           |
   | RS512        | RSASSA-PKCS1-v1_5 con SHA-512                           |
   | ES256        | ECDSA con P-256 y SHA-256                               |
   | ES384        | ECDSA con P-384 y SHA-384                               |
   | ES512        | ECDSA con P-521 y SHA-512                               |
   | PS256        | RSASSA-PSS con SHA-256 y MGF1 con SHA-256               |
   | PS384        | RSASSA-PSS con SHA-384 y MGF1 con SHA-384               |
   | PS512        | RSASSA-PSS con SHA-512 y MGF1 con SHA-512               |
   | none         | Sin firma digital ni MAC (ver la nota más abajo)        |
   +--------------+---------------------------------------------------------+
```

Ten en cuenta que el algoritmo "none" no está permitido por defecto, para seguir las
recomendaciones del RFC8725, [sección 3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2). Establece la opción global 'jwt.allow_none_alg' para permitirlo explícitamente.

- `<key>` puede ser una cadena o un nombre de variable (ver también "set-var") que contenga un
  secreto o una ruta de clave pública.

  Los secretos solo son aplicables cuando se usan algoritmos HMAC.

  Las claves públicas deben estar en formato PKCS#1 (para claves RSA, comenzando con BEGIN RSA
  PUBLIC KEY) o en formato SPKI (Subject Public Key Info, comenzando con BEGIN PUBLIC KEY). Las
  claves públicas deben estar disponibles durante el análisis de la configuración y no pueden
  actualizarse ni cargarse en tiempo de ejecución. Consulta el conversor "jwt_verify_cert" para la
  validación de tokens JWT basada en certificados PEM completos.

  Todas las claves públicas que podrían usarse para verificar JWT deben conocerse durante el
  inicio para añadirse a una caché dedicada, de modo que no se requiera acceso a disco durante la
  ejecución.

Devuelve 1 en caso de verificación correcta, 0 en caso de fallo de verificación y un valor
estrictamente negativo para cualquier otro error. Debido a todos esos valores de retorno de error
no nulos, el resultado de este conversor nunca debería convertirse a booleano. Ver más abajo la
lista completa de los valores de retorno posibles.

Los valores de retorno posibles son los siguientes:

```text
  +----+----------------------------------------------------------------------+
  | ID | message                                                              |
  +----+----------------------------------------------------------------------+
  |  1 | "Verification success"                                               |
  |  0 | "Verification failure"                                               |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)"                       |
  | -2 | "Unmanaged algorithm"                                                |
  | -3 | "Invalid token"                                                      |
  | -4 | "Out of memory"                                                      |
  | -5 | "Unknown pubkey/certificate"                                         |
  | -6 | "Internal error"                                                     |
  +----+----------------------------------------------------------------------+
```

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

Ejemplo:

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public key to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify(txn.jwt_alg,"/path/to/pubkey.pem") 1 }
```

jwt_verify_cert(`<alg>`,`<cert>`)

Realiza una verificación de firma para el JSON Web Token (JWT) dado en la entrada usando el
algoritmo `<alg>` y el parámetro `<cert>`. Por ahora, solo pueden procesarse tokens JWS que usen
el formato Compact Serialization (tres cadenas codificadas en base64-url separadas por puntos).
Este conversor solo verifica la firma del token y no realiza una validación JWT completa tal como
se especifica en la [sección 7.2](https://www.rfc-editor.org/rfc/rfc7519#section-7.2) del RFC7519. Por ejemplo, no nos aseguramos de que los contenidos de la cabecera y de la carga sean
JSON completamente válidos una vez decodificados, y no se realiza ninguna comprobación respecto a
sus contenidos respectivos.

- `<alg>` puede ser una cadena o un nombre de variable (ver también "set-var") que contenga el
  nombre del algoritmo usado para verificar. A diferencia del conversor "jwt_verify", este
  conversor solo espera un certificado como segundo parámetro, así que no debería usarse para
  tokens que usen algoritmos HMAC.

  Se gestionan los algoritmos mencionados en la [sección 3.1](https://www.rfc-editor.org/rfc/rfc7518#section-3.1) del RFC7518 (aparte de los HMAC):

```text
   +--------------+---------------------------------------------------------+
   | Param. "alg" | Algoritmo de firma digital o MAC                        |
   | Valor        |                                                         |
   +--------------+---------------------------------------------------------+
   | RS256        | RSASSA-PKCS1-v1_5 con SHA-256                           |
   | RS384        | RSASSA-PKCS1-v1_5 con SHA-384                           |
   | RS512        | RSASSA-PKCS1-v1_5 con SHA-512                           |
   | ES256        | ECDSA con P-256 y SHA-256                               |
   | ES384        | ECDSA con P-384 y SHA-384                               |
   | ES512        | ECDSA con P-521 y SHA-512                               |
   | PS256        | RSASSA-PSS con SHA-256 y MGF1 con SHA-256               |
   | PS384        | RSASSA-PSS con SHA-384 y MGF1 con SHA-384               |
   | PS512        | RSASSA-PSS con SHA-512 y MGF1 con SHA-512               |
   | none         | Sin firma digital ni MAC                                |
   +--------------+---------------------------------------------------------+
```

- `<key>` puede ser una cadena o un nombre de variable (ver también "set-var") que contenga una
  ruta de certificado.

  Los certificados deben ser certificados PEM estándar (comenzando con BEGIN CERTIFICATE). Su ruta
  puede pasarse directamente al conversor o referenciarse mediante una variable. Si se usa una
  variable, los certificados correspondientes pueden declararse en un crt-store o cargarse
  dinámicamente mediante el socket de estadísticas. Cuando se da una ruta directamente, si el
  certificado correspondiente aún no se había cargado en el almacén interno de certificados, se
  cargará durante el análisis de la configuración y, por tanto, debe existir ya; de lo contrario
  se producirá un error.

  Solo pueden usarse los certificados definidos explícitamente como utilizables para la validación
  JWT. Ver la opción "jwt" de crt-store.

  Es posible actualizar certificados dinámicamente y añadir certificados nuevos usando el socket
  de estadísticas. Ver también "set ssl cert" y "new ssl cert" en la guía de gestión.

Devuelve 1 en caso de verificación correcta, 0 en caso de fallo de verificación y un valor
estrictamente negativo para cualquier otro error. Debido a todos esos valores de retorno de error
no nulos, el resultado de este conversor nunca debería convertirse a booleano. Ver más abajo la
lista completa de los valores de retorno posibles.

Los valores de retorno posibles son los siguientes:

```text
  +----+----------------------------------------------------------------------+
  | ID | message                                                              |
  +----+----------------------------------------------------------------------+
  |  1 | "Verification success"                                               |
  |  0 | "Verification failure"                                               |
  | -1 | "Unknown algorithm (not mentioned in RFC7518)"                       |
  | -2 | "Unmanaged algorithm"                                                |
  | -3 | "Invalid token"                                                      |
  | -4 | "Out of memory"                                                      |
  | -5 | "Unknown pubkey/certificate"                                         |
  | -6 | "Internal error"                                                     |
  | -7 | "Unavailable certificate" (ver "jwt")                                |
  +----+----------------------------------------------------------------------+
```

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

Ejemplo:

```shell
# Get a JWT from the authorization header, extract the "alg" field of its
# JOSE header and use a public certificate to verify a signature
http-request set-var(txn.bearer) http_auth_bearer
http-request set-var(txn.jwt_alg) var(txn.bearer),jwt_header_query('$.alg')
http-request deny unless { var(txn.jwt_alg) -m str "RS256" }
http-request deny unless { var(txn.bearer),jwt_verify_cert(txn.jwt_alg,"/path/to/cert.pem") 1 }
```

<a id="entry-7-3-1-language"></a>

**`language(<value>[,<default>])`**

```haproxy
language(<value>[,<default>])
```

Devuelve el valor con el mayor factor q de una lista tal como la extraída de la cabecera
"accept-language" usando "req.fhdr". Los valores sin factor q tienen un factor q de 1. Los valores
con un factor q de 0 se descartan. Solo se considerarán los valores que pertenezcan a la lista de
`<values>` delimitados por punto y coma. La sintaxis del argumento `<value>` es
"lang[;lang[;lang[;...]]]". Si ningún valor coincide con la lista dada y se proporciona un valor
por defecto, se devuelve. Ten en cuenta que los nombres de idioma pueden tener una variante tras
un guion ('-'). Si esta variante está presente en la lista, se comparará, pero si no lo está, solo
se comprueba el idioma base. La coincidencia distingue mayúsculas de minúsculas, y la cadena de
salida es siempre una de las proporcionadas en los argumentos. El orden de los argumentos no tiene
sentido; solo cuenta el orden de los valores en la solicitud, ya que se usa el primer valor entre
múltiples que comparten el mismo factor q.

Ejemplo:

```shell
# this configuration switches to the backend matching a
# given language based on the request:

acl es req.fhdr(accept-language),language(es;fr;en) -m str es
acl fr req.fhdr(accept-language),language(es;fr;en) -m str fr
acl en req.fhdr(accept-language),language(es;fr;en) -m str en
use_backend spanish if es
use_backend french  if fr
use_backend english if en
default_backend choose_your_language
```

<a id="entry-7-3-1-length"></a>

**`length`**

```haproxy
length
```

Obtiene la longitud de la cadena. Solo puede colocarse tras una función de obtención de muestras
de cadena o tras una palabra clave de transformación que devuelva un tipo cadena. El resultado es
de tipo entero.

<a id="entry-7-3-1-lower"></a>

**`lower`**

```haproxy
lower
```

Convierte una muestra de cadena a minúsculas. Solo puede colocarse tras una función de obtención
de muestras de cadena o tras una palabra clave de transformación que devuelva un tipo cadena. El
resultado es de tipo cadena.

<a id="entry-7-3-1-ltime"></a>

**`ltime(<format>[,<offset>])`**

```haproxy
ltime(<format>[,<offset>])
```

Convierte un entero que se supone contiene una fecha en segundos desde epoch en una cadena que
representa esta fecha en hora local usando un formato definido por la cadena `<format>` mediante
strftime(3). El propósito es permitir que se use cualquier formato de fecha en los registros. Un
`<offset>` opcional en segundos puede aplicarse a la fecha de entrada (positivo o negativo).
Consulta la página man de strftime() para conocer el formato soportado por tu sistema operativo.
Ver también el conversor utime.

Ejemplo:

```shell
# Emit two colons, one with the local time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,ltime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-ltrim"></a>

**`ltrim(<chars>)`**

```haproxy
ltrim(<chars>)
```

Omite cualquier carácter de `<chars>` del principio de la representación en cadena de la muestra
de entrada.

<a id="entry-7-3-1-map"></a>

**`map(<map_name>[,<default_value>])`**

```haproxy
map(<map_name>[,<default_value>])
map_<match_type>(<map_name>[,<default_value>])
map_<match_type>_<output_type>(<map_name>[,<default_value>])
```

Busca el valor de entrada en `<map_name>` usando el método de coincidencia `<match_type>` y
devuelve el valor asociado convertido al tipo `<output_type>`. Si el valor de entrada no puede
encontrarse en el `<map_name>`, el conversor devuelve el `<default_value>`. Si el
`<default_value>` no está establecido, el conversor falla y actúa como si no pudiera obtenerse
ningún valor de entrada. Si el `<match_type>` no está establecido, su valor predeterminado es
"str". Asimismo, si el `<output_type>` no está establecido, su valor predeterminado es "str". Por
comodidad, la palabra clave "map" es un alias de "map_str" y mapea una cadena a otra cadena.
`<map_name>` debe seguir el formato descrito en 2.7 sobre el formato de nombres para mapas y ACL

Es importante evitar el solapamiento entre las claves: las direcciones IP y las cadenas se
almacenan en árboles, así que se usará la primera entre las coincidencias más específicas. Otras claves se
almacenan en listas, así que se usará la primera aparición que coincida.

El array siguiente contiene la lista de todas las funciones de mapa disponibles ordenadas por tipo
de entrada, tipo de coincidencia y tipo de salida.

```text
  tipo de entrada | método de coincidencia | tipo de salida str | tipo de salida int | tipo de salida ip | tipo de salida key
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | str                    | map_str            | map_str_int        | map_str_ip        | map_str_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | beg                    | map_beg            | map_beg_int        | map_beg_ip        | map_beg_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | sub                    | map_sub            | map_sub_int        | map_sub_ip        | map_sub_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | dir                    | map_dir            | map_dir_int        | map_dir_ip        | map_dir_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | dom                    | map_dom            | map_dom_int        | map_dom_ip        | map_dom_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | end                    | map_end            | map_end_int        | map_end_ip        | map_end_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | reg                    | map_reg            | map_reg_int        | map_reg_ip        | map_reg_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  str             | reg                    | map_regm           | map_reg_int        | map_reg_ip        | map_reg_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  int             | int                    | map_int            | map_int_int        | map_int_ip        | map_int_key       
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
  ip              | ip                     | map_ip             | map_ip_int         | map_ip_ip         | map_ip_key        
  ----------------+------------------------+--------------------+--------------------+-------------------+-------------------
```

El mapa especial llamado "map_regm" espera una zona de coincidencia en la expresión regular y
modifica la salida sustituyendo la referencia hacia atrás (como "&#92;1") por el texto
coincidente correspondiente.

El tipo de salida "key" significa que es la clave de la entrada coincidente (tal como se encuentra
en el archivo de mapa) la que se devolverá como cadena en lugar del valor. Ten en cuenta que el
argumento opcional `<default_value>` no está soportado cuando se usa el tipo de salida "key".

Los archivos referenciados por `<map_name>` contienen una clave + valor por línea. Las líneas que
comienzan por '#' se ignoran, igual que las líneas vacías. Las tabulaciones y espacios iniciales se
eliminan. La clave es entonces la primera "palabra" (serie de caracteres que no son
espacio/tabulación), y el valor es lo que sigue a esta serie de espacios/tabulaciones hasta el
final de la línea, excluidos los espacios/tabulaciones finales.

Ejemplo:

```text
     # this is a comment and is ignored
        2.22.246.0/23    United Kingdom      \n
     <-><-----------><--><------------><---->
      |       |       |         |        `- se ignoran los espacios finales
      |       |       |         `---------- valor
      |       |       `-------------------- se ignoran los espacios intermedios
      |       `---------------------------- clave
      `------------------------------------ se ignoran los espacios iniciales
```

<a id="entry-7-3-1-mod"></a>

**`mod(<value>)`**

```haproxy
mod(<value>)
```

Divide el valor de entrada de tipo entero con signo por `<value>` y devuelve el resto como un
entero con signo. Si `<value>` es nulo, se devuelve cero. `<value>` puede ser un valor numérico o
un nombre de variable. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-1-mqtt-field-value"></a>

**`mqtt_field_value(<packettype>,<fieldname_or_property_ID>)`**

```haproxy
mqtt_field_value(<packettype>,<fieldname_or_property_ID>)
```

Devuelve el valor de `<fieldname>` encontrado en la carga MQTT de entrada de tipo
`<packettype>`. `<packettype>` puede ser una cadena (coincidencia sin distinguir mayúsculas de
minúsculas) o un valor numérico correspondiente al tipo de paquete del que se supone que
extraemos datos. Las cadenas y enteros soportados pueden encontrarse aquí:
<https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718021>
<https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022>

`<fieldname>` depende de `<packettype>` y puede ser cualquiera de los siguientes. (ten en cuenta
que la coincidencia de `<fieldname>` no distingue mayúsculas de minúsculas). `<property id>` solo
puede encontrarse en flujos MQTT v5.0. consulta esta tabla:
<https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901029>

- CONNECT (o 1): flags, protocol_name, protocol_version, client_identifier, will_topic,
  will_payload, username, password, keepalive O cualquier ID de propiedad como valor numérico
  (solo para paquetes MQTT v5.0):

```text
17: Session Expiry Interval
33: Receive Maximum
39: Maximum Packet Size
34: Topic Alias Maximum
25: Request Response Information
23: Request Problem Information
21: Authentication Method
22: Authentication Data
18: Will Delay Interval
 1: Payload Format Indicator
 2: Message Expiry Interval
 3: Content Type
 8: Response Topic
 9: Correlation Data
```

Todavía no está soportado:

```text
38: User Property
```

- CONNACK (o 2): flags, protocol_version, reason_code O cualquier ID de propiedad como valor
  numérico (solo para paquetes MQTT v5.0):

```text
17: Session Expiry Interval
33: Receive Maximum
36: Maximum QoS
37: Retain Available
39: Maximum Packet Size
18: Assigned Client Identifier
34: Topic Alias Maximum
31: Reason String
40; Wildcard Subscription Available
41: Subscription Identifiers Available
42: Shared Subscription Available
19: Server Keep Alive
26: Response Information
28: Server Reference
21: Authentication Method
22: Authentication Data
```

Todavía no está soportado:

```text
38: User Property
```

Debido al diseño actual de HAProxy, solo puede analizarse el primer mensaje enviado por el cliente
y el servidor. Así, este conversor puede extraer datos solo de los tipos de paquete CONNECT y
CONNACK. CONNECT es el primer mensaje enviado por el cliente y CONNACK es la primera respuesta
enviada por el servidor.

Ejemplo:

```shell
acl data_in_buffer req.len ge 4
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(connect,protocol_name) \
        if data_in_buffer
# do the same as above
tcp-request content set-var(txn.username) \
        req.payload(0,0),mqtt_field_value(1,protocol_name) \
        if data_in_buffer
```

<a id="entry-7-3-1-mqtt-is-valid"></a>

**`mqtt_is_valid`**

```haproxy
mqtt_is_valid
```

Comprueba que la entrada binaria es un paquete MQTT válido. Devuelve un booleano.

Debido al diseño actual de HAProxy, solo puede analizarse el primer mensaje enviado por el cliente
y el servidor. Así, este conversor puede extraer datos solo de los tipos de paquete CONNECT y
CONNACK. CONNECT es el primer mensaje enviado por el cliente y CONNACK es la primera respuesta
enviada por el servidor.

Solo se soportan MQTT 3.1, 3.1.1 y 5.0.

Ejemplo:

```text
acl data_in_buffer req.len ge 4
tcp-request content reject unless { req.payload(0,0),mqtt_is_valid }
```

<a id="entry-7-3-1-ms-ltime"></a>

**`ms_ltime(<format>[,<offset>])`**

```haproxy
ms_ltime(<format>[,<offset>])
```

Funciona como "ltime", pero toma una entrada en milisegundos. También soporta el especificador de
conversión %N inspirado en date(1). Convierte un entero que se supone contiene una fecha desde epoch en una cadena que representa esta fecha en hora local usando un formato
definido por la cadena `<format>` mediante strftime(3). El propósito es permitir que se use
cualquier formato de fecha en los registros. Un `<offset>` opcional en milisegundos puede
aplicarse a la fecha de entrada (positivo o negativo). Consulta la página man de strftime() para
conocer el formato soportado por tu sistema operativo.

El especificador de conversión %N permite mostrar la parte de nanosegundos de la fecha; la
precisión está limitada, ya que la entrada son milisegundos. (000000000..999000000). %N puede
tomar un argumento de anchura entre % y N. Es útil para mostrar milisegundos (%3N) o microsegundos
(%6N). La anchura predeterminada y máxima es 9 (%N = %9N).

Ver también el conversor utime para UTC, así como los conversores "ltime" y "us_ltime".

Ejemplo:

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/11:53:02.196 +0200 127.0.0.1:41530
log-format %[accept_date(ms),ms_ltime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-ms-utime"></a>

**`ms_utime(<format>[,<offset>])`**

```haproxy
ms_utime(<format>[,<offset>])
```

Funciona como "utime", pero toma una entrada en milisegundos. También soporta el especificador de
conversión %N inspirado en date(1). Convierte un entero que se supone contiene una fecha desde epoch en una cadena que representa esta fecha en hora UTC usando un formato
definido por la cadena `<format>` mediante strftime(3). El propósito es permitir que se use
cualquier formato de fecha en los registros. Un `<offset>` opcional en milisegundos puede
aplicarse a la fecha de entrada (positivo o negativo). Consulta la página man de strftime() para
conocer el formato soportado por tu sistema operativo.

El especificador de conversión %N permite mostrar la parte de nanosegundos de la fecha; la
precisión está limitada, ya que la entrada son milisegundos. (000000000..999000000). %N puede
tomar un argumento de anchura entre % y N. Es útil para mostrar milisegundos (%3N) o microsegundos
(%6N). La anchura predeterminada y máxima es 9 (%N = %9N).

Ver también el conversor ltime para la hora local, así como los conversores "utime" y "us_utime".

Ejemplo:

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196 +0000 127.0.0.1:41530
log-format %[accept_date(ms),ms_utime("%Y/%m/%d/%H:%M:%S.%3N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-mul"></a>

**`mul(<value>)`**

```haproxy
mul(<value>)
```

Multiplica el valor de entrada de tipo entero con signo por `<value>` y devuelve el producto como
un entero con signo. En caso de desbordamiento, se devuelve el mayor valor posible para el signo,
de modo que la operación no dé la vuelta. `<value>` puede ser un valor numérico o un nombre de
variable. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8)
sobre las variables para más detalles.

<a id="entry-7-3-1-nbsrv"></a>

**`nbsrv`**

```haproxy
nbsrv
```

Toma un valor de entrada de tipo cadena, lo interpreta como un nombre de backend y devuelve el
número de servidores utilizables en ese backend. Puede usarse en lugares donde queremos buscar un
backend a partir de un nombre dinámico, como el resultado de una búsqueda en un mapa.

<a id="entry-7-3-1-neg"></a>

**`neg`**

```haproxy
neg
```

Toma el valor de entrada de tipo entero con signo, calcula el valor opuesto y devuelve el resto
como un entero con signo. 0 es la identidad. Este operador se proporciona para las restas
invertidas: para restar la entrada de una constante, simplemente realiza un "neg,add(value)".

<a id="entry-7-3-1-not"></a>

**`not`**

```haproxy
not
```

Devuelve un booleano FALSE si el valor de entrada de tipo entero con signo no es nulo; en caso
contrario devuelve TRUE. Usado junto con and(), puede utilizarse para informar de
verdadero/falso en pruebas de bits sobre valores de entrada (p. ej. verificar la ausencia de un
flag).

<a id="entry-7-3-1-odd"></a>

**`odd`**

```haproxy
odd
```

Devuelve un booleano TRUE si el valor de entrada de tipo entero con signo es impar; en caso
contrario devuelve FALSE. Es funcionalmente equivalente a "and(1),bool".

<a id="entry-7-3-1-or"></a>

**`or(<value>)`**

```haproxy
or(<value>)
```

Realiza un "OR" a nivel de bits entre `<value>` y el valor de entrada de tipo entero con signo, y
devuelve el resultado como un entero con signo. `<value>` puede ser un valor numérico o un nombre
de variable. Consulta la [sección
2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-1-param"></a>

**`param(<name>[,<delim>])`**

```haproxy
param(<name>[,<delim>])
```

Extrae la primera aparición del parámetro `<name>` en la cadena de entrada, donde los parámetros
están delimitados por `<delim>`, cuyo valor predeterminado es "&", y el nombre y el valor del
parámetro están separados por un "=". Si no hay "=" ni valor antes del final del segmento del
parámetro, se trata como equivalente a un valor de cadena vacía.

Esto puede ser útil para extraer parámetros de una query string o, posiblemente, de un cuerpo
x-www-form-urlencoded. En particular, `query,param(<name>)` solo usa "&" como delimitador y puede usarse como alternativa a `urlp(<name>)`, que también usa "?" y ";".

Ten en cuenta que este conversor no hace nada especial con los caracteres codificados como URL. Si
quieres decodificar el valor, puedes usar el conversor url_dec sobre la salida. Si el nombre del
parámetro en la entrada podría contener caracteres codificados, probablemente querrás normalizar
la entrada antes de llamar a "param". Esto puede hacerse usando "http-request normalize-uri", en
particular las opciones percent-decode-unreserved y percent-to-uppercase.

Ejemplo:

```text
str(a=b&c=d&a=r),param(a)   # b
str(a&b=c),param(a)         # ""
str(a=&b&c=a),param(b)      # ""
str(a=1;b=2;c=4),param(b,;) # 2
query,param(redirect_uri),urldec()
```

<a id="entry-7-3-1-port-only"></a>

**`port_only`**

```haproxy
port_only
```

Convierte una cadena que contiene un valor de cabecera Host en un entero devolviendo su puerto. La
entrada debe respetar el formato del valor de la cabecera host (rfc9110#section-7.2). Soportará ese
tipo de entrada: hostname, hostname:80, 127.0.0.1, 127.0.0.1:80, [::1], [::1]:80.

Si no se proporcionó puerto en la entrada, devolverá 0.

Ver también: el conversor "host_only", que devolverá el host.

<a id="entry-7-3-1-protobuf"></a>

**`protobuf(<field_number>[,<field_type>])`**

```haproxy
protobuf(<field_number>[,<field_type>])
```

Extrae en modo en bruto el campo de mensaje de Protocol Buffers de una muestra binaria de
entrada que representa un mensaje de Protocol Buffers con `<field_number>` como número de campo
(notación con puntos) si `<field_type>` no está presente, o como una muestra entera si este campo
está presente (ver también "ungrpc" más abajo). La lista de tipos autorizados es la siguiente:
"int32", "int64", "uint32", "uint64", "sint32", "sint64", "bool", "enum" para el tipo de codificación
"varint" 0, "fixed64", "sfixed64", "double" para el tipo de codificación de 64bit 1, "fixed32", "sfixed32",
"float" para el tipo de codificación 5. Ten en cuenta que "string" se considera un tipo delimitado por
longitud, así que no requiere ningún argumento `<field_type>` para extraerse. Puede encontrarse
más información aquí sobre los tipos de campo de mensaje de Protocol Buffers:
<https://developers.google.com/protocol-buffers/docs/encoding>

<a id="entry-7-3-1-regsub"></a>

**`regsub(<regex>,<subst>[,<flags>])`**

```haproxy
regsub(<regex>,<subst>[,<flags>])
```

Aplica una sustitución basada en expresiones regulares a la cadena de entrada. Realiza la misma
operación que la conocida utilidad "sed" con "s/`<regex>`/`<subst>`/". Por defecto reemplazará en
la cadena de entrada la primera aparición de la mayor parte que coincida con la expresión regular
`<regex>` por la cadena de sustitución `<subst>`. Es posible reemplazar todas las apariciones
añadiendo el flag "g" en el tercer argumento `<flags>`. También es posible hacer que la expresión
regular no distinga mayúsculas de minúsculas añadiendo el flag "i" en `<flags>`. Como `<flags>` es
una cadena, se forma con la concatenación de todos los flags deseados. Así, si se desean tanto "i"
como "g", usar "gi" o "ig" tendrá el mismo efecto. El primer uso de este conversor es reemplazar
determinados caracteres o secuencias de caracteres por otros.

Es muy recomendable encerrar la parte de la expresión regular usando comillas protegidas para
mejorar la claridad y que nunca se confunda un paréntesis de cierre de la expresión regular con el
paréntesis de la función. Igual que en el shell Bourne, el primer nivel de comillas se procesa al
delimitar grupos de palabras en la línea; un segundo nivel es utilizable para el argumento. Se
recomienda usar comillas simples fuera, ya que estas no intentan resolver barras invertidas ni
signos de dólar.

Ejemplos:

```shell
# de-duplicate "/" in header "x-path".
# input:  x-path: /////a///b/c/xzxyz/
# output: x-path: /a/b/c/xzxyz/
http-request set-header x-path "%[hdr(x-path),regsub('/+','/','g')]"

# copy query string to x-query and drop all leading '?', ';' and '&'
http-request set-header x-query "%[query,regsub([?;&]*,'')]"

# capture groups and backreferences
# both lines do the same.
http-request redirect location %[url,'regsub("(foo|bar)([0-9]+)?","\2\1",i)']
http-request redirect location %[url,regsub(\"(foo|bar)([0-9]+)?\",\"\2\1\",i)]
```

<a id="entry-7-3-1-reverse"></a>

**`reverse`**

```haproxy
reverse
```

Invierte la cadena de entrada byte a byte.

Este conversor es agnóstico de la codificación e invierte bytes, no caracteres; no es adecuado
para invertir texto humano codificado como UTF-8.

Esto puede convertir las búsquedas de sufijo sobre la cadena original en búsquedas de prefijo sobre
la cadena invertida, permitiendo el uso de comparadores de prefijo indexados como "map_beg" en
mapas grandes.

Ejemplos:

```shell
"example.com" -> "moc.elpmaxe"
"ab cd" -> "dc ba"

# Given a map file where each key contains a reversed hostname:
#   moc.elpmaxe.ppa app1
#   moc.elpmaxe.bd  dbcluster
# Pick a backend based on the domain suffix of the Host header:
use_backend %[req.hdr(host),lower,reverse,map_beg(/etc/haproxy/hosts.map,default)]
```

<a id="entry-7-3-1-reverse-dom"></a>

**`reverse_dom`**

```haproxy
reverse_dom
```

Convierte una cadena que contiene un nombre de host tipo FQDN en su forma de etiquetas
invertidas. Un único punto final en la entrada se ignora. Las etiquetas vacías hacen que el
conversor falle.

Este conversor no convierte su entrada a minúsculas ni elimina ningún puerto. Está pensado para
combinarse con conversores existentes como "lower" o "host_only" cuando se necesite.

La política del punto final se deja intencionadamente al que llama. Esto permite a quien llama
decidir si quiere comparar también el ápice o solo los subdominios.

La forma de etiquetas invertidas es útil para mapas de dominios grandes, porque convierte las
búsquedas de sufijo de dominio en búsquedas de prefijo, permitiendo el uso de comparadores de
prefijo indexados como "map_beg".

Ejemplos:

```shell
"example.com" -> "com.example"
"mail.example.com" -> "com.example.mail"
"example.com." -> "com.example"

# match only subdomains of example.net, not the apex
acl example_net_sub req.hdr(Host),host_only,reverse_dom -m beg net.example.

# match only the apex
acl example_net_apex req.hdr(Host),host_only,reverse_dom -i net.example

# exact-or-subdomain prefix lookup using an explicit dotted form
http-request set-var(txn.rev_host) req.hdr(Host),host_only,reverse_dom,concat(.)
use_backend %[var(txn.rev_host),map_beg(/etc/haproxy/domains.map)]
```

<a id="entry-7-3-1-rfc7239-field"></a>

**`rfc7239_field(<field>)`**

```haproxy
rfc7239_field(<field>)
```

Extrae un único campo/parámetro de una entrada de valor de cabecera conforme a RFC 7239.

Los campos soportados son: - proto: 'http' o 'https' - host: host conforme con http - for: nodo
RFC7239 - by: nodo RFC7239

Más información aquí:

```text
https://www.rfc-editor.org/rfc/rfc7239.html#section-6
```

Ejemplo:

```shell
# extract host field from forwarded header and store it in req.fhost var
http-request set-var(req.fhost) req.hdr(forwarded),rfc7239_field(host)
#input: "proto=https;host=\"haproxy.org:80\""
#  output: "haproxy.org:80"

# extract for field from forwarded header and store it in req.ffor var
http-request set-var(req.ffor) req.hdr(forwarded),rfc7239_field(for)
#input: "proto=https;host=\"haproxy.org:80\";for=\"127.0.0.1:9999\""
#  output: "127.0.0.1:9999"
```

<a id="entry-7-3-1-rfc7239-is-valid"></a>

**`rfc7239_is_valid`**

```haproxy
rfc7239_is_valid
```

Devuelve true si la cabecera de entrada es un valor de cabecera conforme a RFC 7239 y false en
caso contrario.

Ejemplo:

```shell
acl valid req.hdr(forwarded),rfc7239_is_valid
#input: "for=127.0.0.1;proto=http"
#  output: TRUE
#input: "proto=custom"
#  output: FALSE
```

<a id="entry-7-3-1-rfc7239-n2nn"></a>

**`rfc7239_n2nn`**

```haproxy
rfc7239_n2nn
```

Convierte un nodo RFC7239 (proporcionado por los campos de cabecera 7239 'for' o 'by') en su forma
final de nombre de nodo correspondiente: - dirección ipv4 - dirección ipv6 - 'unknown' -
identificador '\_obfs'

Ejemplo:

```shell
# extract 'for' field from forwarded header, extract nodename from
# resulting node identifier and store the result in req.fnn
http-request set-var(req.fnn) req.hdr(forwarded),rfc7239_field(for),rfc7239_n2nn
#input: "127.0.0.1:9999"
#  output: 127.0.0.1 (ipv4)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: ab:cd:ff:ff:ff:ff:ff:ff (ipv6)
#input: "_name:_port"
#  output: "_name" (string)
```

<a id="entry-7-3-1-rfc7239-n2np"></a>

**`rfc7239_n2np`**

```haproxy
rfc7239_n2np
```

Convierte un nodo RFC7239 (proporcionado por los campos de cabecera 7239 'for' o 'by') en su forma
final de puerto de nodo correspondiente: - entero sin signo - identificador '\_obfs'

Ejemplo:

```shell
# extract 'by' field from forwarded header, extract node port from
# resulting node identifier and store the result in req.fnp
http-request set-var(req.fnp) req.hdr(forwarded),rfc7239_field(by),rfc7239_n2np
#input: "127.0.0.1:9999"
#  output: 9999 (integer)
#input: "[ab:cd:ff:ff:ff:ff:ff:ff]:9998"
#  output: 9998 (integer)
#input: "_name:_port"
#  output: "_port" (string)
```

<a id="entry-7-3-1-rfc7239-nn"></a>

**`rfc7239_nn`**

```haproxy
rfc7239_nn
```

Convierte la dirección / cadena de entrada proporcionada en un nombre de nodo conforme a RFC7239.
Puede usarse para construir manualmente campos de cabecera 7239 'for' o 'by'.

Cuando la entrada proporcionada es una cadena, se antepondrá automáticamente el carácter '\_'
para representar un identificador ofuscado. La cadena debe cumplir el juego de caracteres de
RFC7239. Si la cadena está vacía, se convertirá en el identificador "unknown".

Ejemplo:

```shell
#input: ipv6(ab:cd:ff:ff:ff:ff:ff:ff)
#  output: "[ab:cd:ff:ff:ff:ff:ff:ff]"
#input: str(test)
#  output: "_test"
#input: str()
#  output: "unknown"
```

Ver también: "rfc7239_np"

<a id="entry-7-3-1-rfc7239-np"></a>

**`rfc7239_np`**

```haproxy
rfc7239_np
```

Convierte el entero sin signo / cadena de entrada proporcionado en un puerto de nodo conforme a
RFC7239. Puede usarse para construir manualmente campos de cabecera 7239 'for' o 'by'.

Cuando la entrada proporcionada es una cadena, se antepondrá automáticamente el carácter '\_'
para representar un identificador ofuscado. La cadena debe cumplir el juego de caracteres de
RFC7239 y no puede estar vacía.

Ejemplo:

```shell
#input: int(12)
#  output: "12"
#input: str(test)
#  output: "_test"

# build 'for' forwarded header field
http-request set-var-fmt(txn.test) "for=\"%[ipv6(::1),rfc7239_nn]:%[int(8080),rfc7239_np]\";"
#  output: "for=\"[::1]:8080\";"

# build RFC-compliant 7239 header:
http-request set-var-fmt(txn.forwarded) "for=\"%[ipv6(::1),rfc7239_nn]:%[str(8888),rfc7239_np]\";host=\"haproxy.org\";proto=http"
# check RFC-compliancy:
http-request set-var(txn.test) "var(txn.forwarded),debug(test,stderr),rfc7239_is_valid,debug(test,stderr)"
#  stderr output:
#    [debug] test: type=str <for="[::1]:_8888";host="haproxy.org";proto=http>
#    [debug] test: type=bool <1>
```

Ver también: "rfc7239_nn"

<a id="entry-7-3-1-rtrim"></a>

**`rtrim(<chars>)`**

```haproxy
rtrim(<chars>)
```

Omite cualquier carácter de `<chars>` del final de la representación en cadena de la muestra de
entrada.

<a id="entry-7-3-1-sdbm"></a>

**`sdbm([<avalanche>])`**

```haproxy
sdbm([<avalanche>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
función hash SDBM. Opcionalmente, es posible aplicar una función hash de avalancha completa a la
salida si el argumento opcional `<avalanche>` es igual a 1. Este conversor usa las mismas
funciones que usan los diversos algoritmos de balanceo de carga basados en hash, por lo que
proporcionará exactamente los mismos resultados. Está destinado principalmente a la depuración,
pero puede usarse como entrada de una tabla de persistencia para recopilar estadísticas
aproximadas. No debe usarse con fines de seguridad, ya que romper un hash de 32 bits es trivial.
Ver también "crc32", "djb2", "wt6", "crc32c" y la directiva "hash-type".

<a id="entry-7-3-1-secure-memcmp"></a>

**`secure_memcmp(<var>)`**

```haproxy
secure_memcmp(<var>)
```

Compara el contenido de `<var>` con el valor de entrada. Ambos valores se tratan como una cadena
binaria. Devuelve un booleano que indica si ambas cadenas binarias coinciden.

Si ambas cadenas binarias tienen la misma longitud, la comparación se realizará en tiempo
constante.

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

Ejemplo:

```shell
http-request set-var(txn.token) hdr(token)
# Check whether the token sent by the client matches the secret token
# value, without leaking the contents using a timing attack.
acl token_given str(my_secret_token),secure_memcmp(txn.token)
```

<a id="entry-7-3-1-set-var"></a>

**`set-var(<var>[,<cond>...])`**

```haproxy
set-var(<var>[,<cond>...])
```

Establece una variable con el contenido de entrada y devuelve el contenido en la salida tal cual
si todas las condiciones especificadas son verdaderas (ver más abajo una lista de condiciones
posibles). La variable conserva el valor y el tipo de entrada asociado. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

Puedes pasar como máximo cuatro condiciones al conversor de entre las siguientes condiciones
posibles:

- "ifexists"/"ifnotexists":

```text
Comprueba si la variable ya existía antes de la llamada actual a set-var.
Una variable normalmente se crea mediante una llamada exitosa a set-var.
Ten en cuenta que las variables de ámbito "proc" se crean durante el análisis
de la configuración, por lo que la condición "ifexists" será siempre verdadera para ellas.
```

- "ifempty"/"ifnotempty":

```text
Comprueba si la entrada está vacía o no.
Los tipos escalares nunca están vacíos, por lo que la condición ifempty será falsa para
ellos independientemente del contenido de la entrada (enteros, booleanos, IPs, ...).
```

- "ifset"/"ifnotset":

```text
Comprueba si la variable estaba previamente definida o no, o si se llamó a unset-var
sobre la variable.
Una variable que aún no existe se considera como no definida. Una variable "proc"
puede existir sin estar definida, ya que estas variables se crean durante el análisis
de la configuración.
```

- "ifgt"/"iflt":

```text
Comprueba si el contenido de la variable es "mayor que" o "menor que"
la entrada. Esta comprobación solo puede realizarse si tanto la entrada como
la variable son de tipo integer. De lo contrario, la comprobación se considera
verdadera por defecto.
```

<a id="entry-7-3-1-sha1"></a>

**`sha1`**

```haproxy
sha1
```

Convierte una muestra binaria de entrada en un resumen SHA-1. El resultado es una muestra binaria
con una longitud de 20 bytes.

<a id="entry-7-3-1-sha2"></a>

**`sha2([<bits>])`**

```haproxy
sha2([<bits>])
```

Convierte una muestra binaria de entrada en un resumen de la familia SHA-2. El resultado es una
muestra binaria con una longitud de `<bits>`/8 bytes.

Los valores válidos para `<bits>` son 224, 256, 384, 512, cada uno correspondiente a
SHA-`<bits>`. El valor predeterminado es 256.

Ten en cuenta que este conversor solo está disponible cuando HAProxy se ha compilado con
USE_OPENSSL.

<a id="entry-7-3-1-srv-is-up"></a>

**`srv_is_up`**

```haproxy
srv_is_up
```

Toma un valor de entrada de tipo cadena, bien un nombre de servidor o el formato
`<backend>`/`<server>`, y devuelve true cuando el servidor designado está actualmente UP. Puede
usarse en lugares donde queremos consultar el estado de un servidor a partir de un nombre
dinámico, como un valor de cookie (p. ej. req.cook(SRVID),srv_is_up), y luego tomar la decisión de
dirigir una solicitud a otro lugar. Antes de usar esto, ten en cuenta que usar este conversor con
datos no controlados podría permitir a un observador externo consultar el estado de cualquier
servidor de toda la configuración, lo que posiblemente no sea aceptable en algunos entornos.

<a id="entry-7-3-1-srv-queue"></a>

**`srv_queue`**

```haproxy
srv_queue
```

Toma un valor de entrada de tipo cadena, bien un nombre de servidor o el formato
`<backend>`/`<server>`, y devuelve el número de flujos en cola en ese servidor. Puede usarse en
lugares donde queremos consultar los flujos en cola a partir de un nombre dinámico, como un valor
de cookie (p. ej. req.cook(SRVID),srv_queue), y luego tomar la decisión de romper la persistencia
o dirigir una solicitud a otro lugar. Antes de usar esto, ten en cuenta que usar este conversor
con datos no controlados podría permitir a un observador externo consultar el estado de cualquier
servidor de toda la configuración, lo que posiblemente no sea aceptable en algunos entornos.

<a id="entry-7-3-1-strcmp"></a>

**`strcmp(<var>)`**

```haproxy
strcmp(<var>)
```

Compara el contenido de `<var>` con el valor de entrada de tipo cadena. Devuelve el resultado como
un entero con signo compatible con strcmp(3): 0 si ambas cadenas son idénticas. Un valor menor que
0 si la cadena de la izquierda es lexicográficamente menor que la cadena de la derecha o si la
cadena de la izquierda es más corta. Un valor mayor que 0 en caso contrario (cadena de la derecha
mayor que la de la izquierda, o la cadena de la derecha más corta).

Ver también el conversor secure_memcmp si necesitas comparar dos cadenas binarias en tiempo
constante.

Ejemplo:

```shell
http-request set-var(txn.host) hdr(host)
# Check whether the client is attempting domain fronting.
acl ssl_sni_http_host_match ssl_fc_sni,strcmp(txn.host) eq 0

```

<a id="entry-7-3-1-sub"></a>

**`sub(<value>)`**

```haproxy
sub(<value>)
```

Resta `<value>` del valor de entrada de tipo entero con signo y devuelve el resultado como un
entero con signo. Nota: para restar la entrada a una constante, simplemente realiza un
"neg,add(value)". `<value>` puede ser un valor numérico o un nombre de variable. Consulta la
[sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más
detalles.

<a id="entry-7-3-1-table-bytes-in-rate"></a>

**`table_bytes_in_rate([<table>])`**

```haproxy
table_bytes_in_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la tasa media de bytes de cliente a servidor
asociada a la muestra de entrada en la tabla designada, medida en cantidad de bytes durante el
periodo configurado en la tabla. Ver también la palabra clave de obtención de muestras
sc_bytes_in_rate.

<a id="entry-7-3-1-table-bytes-out-rate"></a>

**`table_bytes_out_rate([<table>])`**

```haproxy
table_bytes_out_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la tasa media de bytes de servidor a cliente
asociada a la muestra de entrada en la tabla designada, medida en cantidad de bytes durante el
periodo configurado en la tabla. Ver también la palabra clave de obtención de muestras
sc_bytes_out_rate.

<a id="entry-7-3-1-table-clr-gpc"></a>

**`table_clr_gpc(<idx>[,<table>])`**

```haproxy
table_clr_gpc(<idx>[,<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Borra el Contador de Propósito General en el índice `<idx>`
del array gpc y devuelve su valor anterior. `<idx>` es un entero entre 0 y 99. Si no se encuentra la
entrada, se crea una entrada y se devuelve 0. Este conversor se aplica solo al tipo de datos del
array 'gpc' (y no a los tipos de datos obsoletos 'gpc0' ni 'gpc1'). Ver también la palabra clave de
obtención de muestras sc_clr_gpc.

<a id="entry-7-3-1-table-clr-gpc0"></a>

**`table_clr_gpc0([<table>])`**

```haproxy
table_clr_gpc0([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Borra el primer Contador de Propósito General '0' y devuelve
su valor anterior. Si no se encuentra la entrada, se crea una entrada y se devuelve 0. Esto se usa
típicamente como una segunda ACL en una expresión para marcar una conexión cuando se verificó una
primera ACL:

Ejemplo:

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse src_http_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 5
acl save  src,table_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

Ver también la palabra clave de obtención de muestras sc_clr_gpc0.

<a id="entry-7-3-1-table-clr-gpc1"></a>

**`table_clr_gpc1([<table>])`**

```haproxy
table_clr_gpc1([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Borra el primer Contador de Propósito General '1' y devuelve
su valor anterior. Si no se encuentra la entrada, se crea una entrada y se devuelve 0. Esto se usa
típicamente como una segunda ACL en una expresión para marcar una conexión cuando se verificó una
primera ACL. Ver también la palabra clave de obtención de muestras sc_clr_gpc1.

<a id="entry-7-3-1-table-conn-cnt"></a>

**`table_conn_cnt([<table>])`**

```haproxy
table_conn_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de conexiones entrantes
asociadas a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención
de muestras sc_conn_cnt.

<a id="entry-7-3-1-table-conn-cur"></a>

**`table_conn_cur([<table>])`**

```haproxy
table_conn_cur([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la cantidad actual de conexiones rastreadas
simultáneas asociadas a la muestra de entrada en la tabla designada. Ver también la palabra clave
de obtención de muestras sc_conn_cur.

<a id="entry-7-3-1-table-conn-rate"></a>

**`table_conn_rate([<table>])`**

```haproxy
table_conn_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la tasa media de conexiones entrantes
asociada a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención
de muestras sc_conn_rate.

<a id="entry-7-3-1-table-expire"></a>

**`table_expire([<table>[,<default_value>]])`**

```haproxy
table_expire([<table>[,<default_value>]])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, el conversor falla
excepto si se establece `<default_value>`: esto hace que el conversor tenga éxito y devuelva
`<default_value>`. Si se encuentra la clave, el conversor devuelve el retardo de expiración de la
clave asociada a la muestra de entrada en la tabla designada. Ver también la palabra clave de
obtención de muestras table_idle.

<a id="entry-7-3-1-table-glitch-cnt"></a>

**`table_glitch_cnt([<table>])`**

```haproxy
table_glitch_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de glitches de conexión
frontal asociados a la muestra de entrada en la tabla designada. Ver también la palabra clave de
obtención de muestras sc_glitch_cnt y fc_glitches para el valor medido en la conexión frontal
actual.

<a id="entry-7-3-1-table-glitch-rate"></a>

**`table_glitch_rate([<table>])`**

```haproxy
table_glitch_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la tasa media de glitches de conexión frontal
asociada a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención
de muestras sc_glitch_rate.

<a id="entry-7-3-1-table-gpc"></a>

**`table_gpc(<idx>[,<table>])`**

```haproxy
table_gpc(<idx>[,<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el valor actual del Contador de Propósito
General en el índice `<idx>` del array asociado a la muestra de entrada en la `<table>` designada.
`<idx>` es un entero entre 0 y 99. Si no hay ningún GPC almacenado en ese índice, también devuelve
el valor entero 0. Esto se aplica solo al tipo de datos del array 'gpc' (y no a los tipos de datos
obsoletos 'gpc0' ni 'gpc1'). Ver también la palabra clave de obtención de muestras sc_get_gpc.

<a id="entry-7-3-1-table-gpc0"></a>

**`table_gpc0([<table>])`**

```haproxy
table_gpc0([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el valor actual del primer contador de
propósito general asociado a la muestra de entrada en la tabla designada. Ver también la palabra
clave de obtención de muestras sc_get_gpc0.

<a id="entry-7-3-1-table-gpc0-rate"></a>

**`table_gpc0_rate([<table>])`**

```haproxy
table_gpc0_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la frecuencia con la que el contador gpc0 fue
incrementado durante el periodo configurado en la tabla, asociado a la muestra de entrada en la
tabla designada. Ver también la palabra clave de obtención de muestras sc_get_gpc0_rate.

<a id="entry-7-3-1-table-gpc1"></a>

**`table_gpc1([<table>])`**

```haproxy
table_gpc1([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el valor actual del segundo contador de
propósito general asociado a la muestra de entrada en la tabla designada. Ver también la palabra
clave de obtención de muestras sc_get_gpc1.

<a id="entry-7-3-1-table-gpc1-rate"></a>

**`table_gpc1_rate([<table>])`**

```haproxy
table_gpc1_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la frecuencia con la que el contador gpc1 fue
incrementado durante el periodo configurado en la tabla, asociado a la muestra de entrada en la
tabla designada. Ver también la palabra clave de obtención de muestras sc_get_gpc1_rate.

<a id="entry-7-3-1-table-gpc-rate"></a>

**`table_gpc_rate(<idx>[,<table>])`**

```haproxy
table_gpc_rate(<idx>[,<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la frecuencia con la que el Contador de
Propósito General en el índice `<idx>` del array (asociado a la muestra de entrada en la tabla de
persistencia designada `<table>`) fue incrementado durante el periodo configurado. `<idx>` es un
entero entre 0 y 99. Si no hay ningún gpc_rate almacenado en ese índice, también devuelve el valor
entero 0. Esto se aplica solo al tipo de datos del array 'gpc_rate' (y no a los tipos de datos
obsoletos 'gpc0_rate' ni 'gpc1_rate'). Ver también la palabra clave de obtención de muestras
sc_gpc_rate.

<a id="entry-7-3-1-table-gpt"></a>

**`table_gpt(<idx>[,<table>])`**

```haproxy
table_gpt(<idx>[,<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el valor actual de la etiqueta de propósito
general en el índice `<idx>` del array asociado a la muestra de entrada en la `<table>` designada.
`<idx>` es un entero entre 0 y 99. Si no hay ningún GPT almacenado en ese índice, también devuelve
el valor entero 0. Esto se aplica solo al tipo de datos del array 'gpt' (y no al tipo de datos
obsoleto 'gpt0'). Ver también la palabra clave de obtención de muestras sc_get_gpt.

<a id="entry-7-3-1-table-gpt0"></a>

**`table_gpt0([<table>])`**

```haproxy
table_gpt0([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el valor actual de la primera etiqueta de
propósito general asociada a la muestra de entrada en la tabla designada. Ver también la palabra
clave de obtención de muestras sc_get_gpt0.

<a id="entry-7-3-1-table-http-err-cnt"></a>

**`table_http_err_cnt([<table>])`**

```haproxy
table_http_err_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de errores HTTP asociados
a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención de
muestras sc_http_err_cnt.

<a id="entry-7-3-1-table-http-err-rate"></a>

**`table_http_err_rate([<table>])`**

```haproxy
table_http_err_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, devuelve la tasa media de errores HTTP asociada a la muestra de entrada en
la tabla designada, medida en cantidad de errores durante el periodo configurado en la tabla. Ver
también la palabra clave de obtención de muestras sc_http_err_rate.

<a id="entry-7-3-1-table-http-fail-cnt"></a>

**`table_http_fail_cnt([<table>])`**

```haproxy
table_http_fail_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de fallos HTTP asociados
a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención de
muestras sc_http_fail_cnt.

<a id="entry-7-3-1-table-http-fail-rate"></a>

**`table_http_fail_rate([<table>])`**

```haproxy
table_http_fail_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, devuelve la tasa media de fallos HTTP asociada a la muestra de entrada en la
tabla designada, medida en cantidad de fallos durante el periodo configurado en la tabla. Ver
también la palabra clave de obtención de muestras sc_http_fail_rate.

<a id="entry-7-3-1-table-http-req-cnt"></a>

**`table_http_req_cnt([<table>])`**

```haproxy
table_http_req_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de solicitudes HTTP
asociadas a la muestra de entrada en la tabla designada. Ver también la palabra clave de obtención
de muestras sc_http_req_cnt.

<a id="entry-7-3-1-table-http-req-rate"></a>

**`table_http_req_rate([<table>])`**

```haproxy
table_http_req_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, devuelve la tasa media de solicitudes HTTP asociada a la muestra de entrada
en la tabla designada, medida en cantidad de solicitudes durante el periodo configurado en la
tabla. Ver también la palabra clave de obtención de muestras sc_http_req_rate.

<a id="entry-7-3-1-table-idle"></a>

**`table_idle([<table>[,<default_value>]])`**

```haproxy
table_idle([<table>[,<default_value>]])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, el conversor falla
excepto si se establece `<default_value>`: esto hace que el conversor tenga éxito y devuelva
`<default_value>`. Si se encuentra la clave, el conversor devuelve el tiempo que la entrada de la
clave asociada a la muestra de entrada en la tabla designada permaneció inactiva desde la última
vez que se actualizó. Ver también la palabra clave de obtención de muestras table_expire.

<a id="entry-7-3-1-table-inc-gpc"></a>

**`table_inc_gpc(<idx>[,<table>])`**

```haproxy
table_inc_gpc(<idx>[,<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Incrementa el Contador de Propósito General en el índice
`<idx>` del array y devuelve su nuevo valor. `<idx>` es un entero entre 0 y 99. Si no se encuentra
la entrada, se crea una entrada y se devuelve 1. Este conversor se aplica solo al tipo de datos del
array 'gpc' (y no a los tipos de datos obsoletos 'gpc0' ni 'gpc1'). Ver también sc_inc_gpc.

<a id="entry-7-3-1-table-inc-gpc0"></a>

**`table_inc_gpc0([<table>])`**

```haproxy
table_inc_gpc0([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Incrementa el Contador de Propósito General '0' y devuelve
su nuevo valor. Si no se encuentra la entrada, se crea una entrada y se devuelve 1. Ver también
sc0/sc2/sc2_inc_gpc0. Esto se usa típicamente como una segunda ACL en una expresión para marcar
una conexión cuando se verificó una primera ACL:

Ejemplo:

```text
acl abuse src,table_req_rate gt 10
acl kill  src,table_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-1-table-inc-gpc1"></a>

**`table_inc_gpc1([<table>])`**

```haproxy
table_inc_gpc1([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Incrementa el Contador de Propósito General '1' y devuelve
su nuevo valor. Si no se encuentra la entrada, se crea una entrada y se devuelve 1. Ver también
sc0/sc2/sc2_inc_gpc1. Esto se usa típicamente como una segunda ACL en una expresión para marcar
una conexión cuando se verificó una primera ACL.

<a id="entry-7-3-1-table-kbytes-in"></a>

**`table_kbytes_in([<table>])`**

```haproxy
table_kbytes_in([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de datos de cliente a
servidor asociados a la muestra de entrada en la tabla designada, medido en kilobytes. La prueba se
realiza actualmente sobre enteros de 32 bits, lo que limita los valores a 4 terabytes. Ver también
la palabra clave de obtención de muestras sc_kbytes_in.

<a id="entry-7-3-1-table-kbytes-out"></a>

**`table_kbytes_out([<table>])`**

```haproxy
table_kbytes_out([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de datos de servidor a
cliente asociados a la muestra de entrada en la tabla designada, medido en kilobytes. La prueba se
realiza actualmente sobre enteros de 32 bits, lo que limita los valores a 4 terabytes. Ver también
la palabra clave de obtención de muestras sc_kbytes_out.

<a id="entry-7-3-1-table-server-id"></a>

**`table_server_id([<table>])`**

```haproxy
table_server_id([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el ID de servidor asociado a la muestra de
entrada en la tabla designada. Un ID de servidor se asocia a una muestra mediante una regla "stick"
cuando una conexión a un servidor tiene éxito. Un ID de servidor cero significa que ningún servidor
está asociado a esta clave.

<a id="entry-7-3-1-table-sess-cnt"></a>

**`table_sess_cnt([<table>])`**

```haproxy
table_sess_cnt([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve el número acumulado de sesiones entrantes
asociadas a la muestra de entrada en la tabla designada. Ten en cuenta que una sesión aquí se
refiere a una conexión entrante aceptada por los conjuntos de reglas "tcp-request connection". Ver
también la palabra clave de obtención de muestras sc_sess_cnt.

<a id="entry-7-3-1-table-sess-rate"></a>

**`table_sess_rate([<table>])`**

```haproxy
table_sess_rate([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la tasa media de sesiones entrantes asociada
a la muestra de entrada en la tabla designada. Ten en cuenta que una sesión aquí se refiere a una
conexión entrante aceptada por los conjuntos de reglas "tcp-request connection". Ver también la
palabra clave de obtención de muestras sc_sess_rate.

<a id="entry-7-3-1-table-trackers"></a>

**`table_trackers([<table>])`**

```haproxy
table_trackers([<table>])
```

Usa la muestra de entrada para realizar una búsqueda en la tabla de persistencia del proxy actual o
en la tabla de persistencia designada. Si la clave no se encuentra en la tabla, se devuelve el valor
entero cero. En caso contrario, el conversor devuelve la cantidad actual de conexiones simultáneas
que rastrean la misma clave que la muestra de entrada en la tabla designada. Se diferencia de
table_conn_cur en que no depende de ninguna información almacenada sino del contador de referencias
de la tabla (el valor "use" que devuelve "show table" en la CLI). Esto puede ser a veces más
adecuado para el rastreo en capa 7. Puede usarse, por ejemplo, para indicar a un servidor cuántas
conexiones simultáneas hay desde una dirección determinada. Ver también la palabra clave de
obtención de muestras sc_trackers.

<a id="entry-7-3-1-tcp-dst"></a>

**`tcp.dst`**

```haproxy
tcp.dst
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Devuelve un entero que representa el puerto de destino presente en la cabecera TCP. Ver
también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-flags"></a>

**`tcp.flags`**

```haproxy
tcp.flags
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Devuelve un entero que representa los flags TCP de esa cabecera TCP. Se recuperan los 8
flags, desde FIN hasta CWR. Cada flag puede comprobarse usando el conversor "and()". Consulta el
RFC9293 para conocer el valor de cada flag. Ver también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-options-mss"></a>

**`tcp.options.mss`**

```haproxy
tcp.options.mss
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "MSS" y, si la encuentra, devuelve un valor entero que
corresponde al valor anunciado en esa opción; en caso contrario, cero. El MSS es el Maximum Segment
Size e indica el mayor segmento que el par puede recibir, en bytes. Ver también "fc_saved_syn",
"tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-options-sack"></a>

**`tcp.options.sack`**

```haproxy
tcp.options.sack
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "Sack-Permitted" y, si la encuentra, devuelve 1; en caso
contrario, cero. Ver también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-options-tsopt"></a>

**`tcp.options.tsopt`**

```haproxy
tcp.options.tsopt
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "Timestamp" y, si la encuentra, devuelve 1; en caso
contrario, cero. Ver también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-options-tsval"></a>

**`tcp.options.tsval`**

```haproxy
tcp.options.tsval
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "Timestamp" y, si la encuentra, devuelve el valor de
timestamp emitido por el par; en caso contrario, no devuelve nada. Ten en cuenta que los timestamps
son valores sin signo de 32 bits sin ninguna unidad en particular que solo decide el par, y se
espera que los timestamps sean independientes entre conexiones diferentes. Ver también
"fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-options-wscale"></a>

**`tcp.options.wscale`**

```haproxy
tcp.options.wscale
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "Window Scale" y, si la encuentra, devuelve el valor de
escalado de ventana emitido por el par; en caso contrario, cero. Ten en cuenta que no se espera que
los valores superen 14, aunque ninguna limitación técnica impide que se envíen. Para detectar si se
usó la opción window scale, usa "tcp.options.wsopt". Ver también "tcp-ss", "fc_saved_syn",
"ip.data" y "tcp.options.wsopt".

<a id="entry-7-3-1-tcp-options-wsopt"></a>

**`tcp.options.wsopt`**

```haproxy
tcp.options.wsopt
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Busca una opción TCP de tipo "Window Scale" y, si la encuentra, devuelve 1; en caso
contrario, 0. Ver también "fc_saved_syn", "tcp-ss", "ip.data" "tcp.options.wscale".

<a id="entry-7-3-1-tcp-options-list"></a>

**`tcp.options_list`**

```haproxy
tcp.options_list
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Construye una secuencia binaria de todos los tipos de opciones TCP en el mismo orden en
que aparecen en la cabecera TCP. Puede producir de 0 a 60 bytes (en el peor de los casos). El
End-of-options no se emite. Ver también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-seq"></a>

**`tcp.seq`**

```haproxy
tcp.seq
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Devuelve un entero que representa el número de secuencia usado por el par en la cabecera
TCP. Los números de secuencia son valores sin signo de 32 bits. Ver también "fc_saved_syn",
"tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-src"></a>

**`tcp.src`**

```haproxy
tcp.src
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Devuelve un entero que representa el puerto de origen presente en la cabecera TCP. Ver
también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-tcp-win"></a>

**`tcp.win`**

```haproxy
tcp.win
```

Se usa con una muestra de entrada que representa una cabecera TCP binaria, tal como la devuelve
"ip.data". Devuelve un entero que representa el tamaño de ventana anunciado por el par en la
cabecera TCP. El valor se proporciona tal cual, como una cantidad sin signo de 16 bits, sin aplicar
el factor de escalado de ventana. Ver también "fc_saved_syn", "tcp-ss" y "ip.data".

<a id="entry-7-3-1-ub64dec"></a>

**`ub64dec`**

```haproxy
ub64dec
```

Este conversor es la variante base64url del conversor b64dec. La codificación base64url es la
variante "URL and Filename Safe Alphabet" de la codificación base64. También es la codificación
usada en el estándar JWT (JSON Web Token).

Ejemplo:

```shell
# Decoding a JWT payload:
http-request set-var(txn.token_payload) req.hdr(Authorization),word(2,.),ub64dec
```

<a id="entry-7-3-1-ub64enc"></a>

**`ub64enc`**

```haproxy
ub64enc
```

Este conversor es la variante base64url del conversor base64.

<a id="entry-7-3-1-ungrpc"></a>

**`ungrpc(<field_number>[,<field_type>])`**

```haproxy
ungrpc(<field_number>[,<field_type>])
```

Esto extrae el campo de mensaje de Protocol Buffers en modo raw de una muestra binaria de entrada
que representa un mensaje gRPC con `<field_number>` como número de campo (notación con puntos) si
`<field_type>` no está presente, o como una muestra entera si este campo está presente. La lista de
los tipos autorizados es la siguiente: "int32", "int64", "uint32", "uint64", "sint32", "sint64",
"bool", "enum" para el tipo de codificación "varint" 0, "fixed64", "sfixed64", "double" para el tipo de
codificación de 64bit 1, "fixed32", "sfixed32", "float" para el tipo de codificación 5. Ten en cuenta que
"string" se considera un tipo delimitado por longitud, por lo que no requiere ningún argumento
`<field_type>` para extraerse. Puede encontrarse más información sobre los tipos de campos de
mensaje de Protocol Buffers aquí:
<https://developers.google.com/protocol-buffers/docs/encoding>

Ejemplo:

```text
// with such a protocol buffer .proto file content adapted from
// https://github.com/grpc/grpc/blob/master/examples/protos/route_guide.proto

message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}

message PPoint {
  Point point = 59;
}

message Rectangle {
  // One corner of the rectangle.
  PPoint lo = 48;
  // The other corner of the rectangle.
  PPoint hi = 49;
}
```

digamos que el cuerpo de una solicitud está formado por un valor de objeto "Rectangle" (dos
mensajes de protocol buffers PPoint); los cuatro campos de protocol buffers podrían extraerse con
estas directivas "ungrpc":

```text
req.body,ungrpc(48.59.1,int32) # "latitude" of "lo" first PPoint
req.body,ungrpc(48.59.2,int32) # "longitude" of "lo" first PPoint
req.body,ungrpc(49.59.1,int32) # "latitude" of "hi" second PPoint
req.body,ungrpc(49.59.2,int32) # "longitude" of "hi" second PPoint
```

También podríamos extraer el campo intermedio 48.59 como una muestra binaria de la siguiente
manera:

```text
req.body,ungrpc(48.59)
```

Como un mensaje gRPC siempre está formado por una cabecera gRPC seguida de mensajes de protocol
buffers, en el ejemplo anterior la "latitude" del primer PPoint "lo" podría extraerse con estas
directivas equivalentes:

```text
req.body,ungrpc(48.59),protobuf(1,int32)
req.body,ungrpc(48),protobuf(59.1,int32)
req.body,ungrpc(48),protobuf(59),protobuf(1,int32)
```

Ten en cuenta que la primera conversión debe ser "ungrpc", las restantes deben ser "protobuf" y
solo la última puede llevar o no un segundo argumento para interpretar la muestra binaria
anterior.

<a id="entry-7-3-1-unset-var"></a>

**`unset-var(<var>)`**

```haproxy
unset-var(<var>)
```

Elimina el valor de una variable si el contenido de entrada está definido. El nombre de la variable comienza
con una indicación sobre su ámbito. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-1-upper"></a>

**`upper`**

```haproxy
upper
```

Convierte una muestra de cadena a mayúsculas. Solo puede colocarse tras una función de obtención de
muestras de cadena o tras una palabra clave de transformación que devuelva un tipo cadena. El
resultado es de tipo cadena.

<a id="entry-7-3-1-url-dec"></a>

**`url_dec([<in_form>])`**

```haproxy
url_dec([<in_form>])
```

Toma una cadena codificada como url proporcionada como entrada y devuelve la versión decodificada
como salida. La entrada y la salida son de tipo cadena. Si el argumento `<in_form>` se establece a
un valor entero distinto de cero, se asume que la cadena de entrada forma parte de un formulario o
de una cadena de consulta y el carácter '+' se convertirá en un espacio (' '). En caso contrario,
esto solo ocurrirá tras un signo de interrogación que indica una cadena de consulta ('?').

<a id="entry-7-3-1-url-enc"></a>

**`url_enc([<enc_type>])`**

```haproxy
url_enc([<enc_type>])
```

Toma una cadena proporcionada como entrada y devuelve la versión codificada como salida. La entrada
y la salida son de tipo cadena. Por defecto, el tipo de codificación está pensado para el tipo
`query`. Por ahora no hay ningún otro tipo soportado, pero el argumento opcional está ahí para
cambios futuros.

<a id="entry-7-3-1-us-ltime"></a>

**`us_ltime(<format>[,<offset>])`**

```haproxy
us_ltime(<format>[,<offset>])
```

Funciona como "ltime" pero toma una entrada en microsegundos. También soporta el especificador de
conversión %N inspirado en date(1). Convierte un entero que se supone contiene una fecha desde
epoch en una cadena que representa esta fecha en hora local usando un formato definido por la
cadena `<format>` mediante strftime(3). El propósito es permitir que se use cualquier formato de
fecha en los registros. Un `<offset>` opcional en microsegundos puede aplicarse a la fecha de
entrada (positivo o negativo). Consulta la página man de strftime() para conocer el formato
soportado por tu sistema operativo.

El especificador de conversión %N permite mostrar la parte de nanosegundos de la fecha; la precisión
es limitada ya que la entrada está en microsegundos. (000000000..999999000). %N puede tomar un
argumento de anchura entre % y N. Es útil para mostrar milisegundos (%3N) o microsegundos (%6N). La
anchura por defecto y máxima es 9 (%N = %9N).

Ver también el conversor "utime" para UTC, así como los conversores "ltime" y "ms_ltime".

Ejemplo:

```shell
# Emit 3 colons, the local time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_ltime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-us-utime"></a>

**`us_utime(<format>[,<offset>])`**

```haproxy
us_utime(<format>[,<offset>])
```

Funciona como "utime" pero toma una entrada en microsegundos. También soporta el especificador de
conversión %N inspirado en date(1). Convierte un entero que se supone contiene una fecha desde
epoch en una cadena que representa esta fecha en hora UTC usando un formato definido por la cadena
`<format>` mediante strftime(3). El propósito es permitir que se use cualquier formato de fecha en
los registros. Un `<offset>` opcional en microsegundos puede aplicarse a la fecha de entrada
(positivo o negativo). Consulta la página man de strftime() para conocer el formato soportado por
tu sistema operativo.

El especificador de conversión %N permite mostrar la parte de nanosegundos de la fecha; la precisión
es limitada ya que la entrada está en microsegundos. (000000000..999999000). %N puede tomar un
argumento de anchura entre % y N. Es útil para mostrar milisegundos (%3N) o microsegundos (%6N). La
anchura por defecto y máxima es 9 (%N = %9N).

Ver también el conversor "ltime" para la hora local, así como los conversores "utime" y "ms_utime".

Ejemplo:

```shell
# Emit 3 colons, the UTC time, the timezone and another with ip:port
# e.g. 2023/07/24/09:53:02.196234 +0000 127.0.0.1:41530
log-format %[accept_date(us),us_utime("%Y/%m/%d/%H:%M:%S.%6N %z")]\ %ci:%cp
```

<a id="entry-7-3-1-utime"></a>

**`utime(<format>[,<offset>])`**

```haproxy
utime(<format>[,<offset>])
```

Convierte un entero que se supone contiene una fecha desde epoch en una cadena que representa esta
fecha en hora UTC usando un formato definido por la cadena `<format>` mediante strftime(3). El
propósito es permitir que se use cualquier formato de fecha en los registros. Un `<offset>` opcional
en segundos puede aplicarse a la fecha de entrada (positivo o negativo). Consulta la página man de
strftime() para conocer el formato soportado por tu sistema operativo. Ver también el conversor
"ltime", así como "ms_utime" y "us_utime".

Ejemplo:

```shell
# Emit two colons, one with the UTC time and another with ip:port
# e.g.  20140710162350 127.0.0.1:57325
log-format %[date,utime(%Y%m%d%H%M%S)]\ %ci:%cp
```

<a id="entry-7-3-1-when"></a>

**`when(<condition>[,<args>...])`**

```haproxy
when(<condition>[,<args>...])
```

Evalúa la condición y, cuando es verdadera, pasa la muestra de entrada tal cual a la salida; en
caso contrario, no devuelve nada. Está diseñado específicamente para producir algunos datos
raramente necesarios que solo deberían emitirse bajo ciertas condiciones, como información de
depuración cuando se encuentra un error.

La condición está formada por una palabra clave de la lista siguiente, opcionalmente precedida de
un signo de exclamación ('!') para negarla, y opcionalmente seguida de algunos argumentos
específicos de esa condición:

    - "error" devuelve true cuando se encontró un error durante el procesamiento
      de la solicitud o del flujo. Usa las mismas reglas que "dontlog-normal"
      (p. ej. una reexpedición exitosa cuenta como error).

    - "forwarded" devuelve true cuando la solicitud fue reenviada a un servidor
      backend

    - "normal" devuelve true cuando no ocurrió ningún error (equivale a "!error").

    - "processed" devuelve true cuando la solicitud fue reenviada a un servidor
      backend o procesada por un applet.

    - "stopping" devuelve true si el proceso se está deteniendo actualmente
      cuando se evalúa la regla

    - "toapplet" devuelve true cuando la solicitud fue procesada por un applet.

    - "acl" devuelve true cuando la ACL designada por el argumento siguiente
      evalúa a true. Ten en cuenta que la ACL se evalúa en línea en el conversor,
      de modo que aquello a lo que se refiere debe ser válido en ese contexto. Un
      caso de uso particular consiste en evaluar si el tiempo total de
      transferencia es demasiado largo o no antes de decidir registrar detalles
      de transferencias anormalmente largas.

Ten en cuenta que el contenido se evalúa en cualquier caso, por lo que hacer esto no evita la
generación de esa información. Solo pretende evitar emitirla.

Un ejemplo sería añadir información de depuración del flujo del backend en los registros solo
cuando se encontró un error durante el procesamiento, o registrar información adicional durante la
detención, etc.

Ejemplo:

```shell
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on error:
log-format "$HAPROXY_HTTP_LOG_FMT dbg={%[bs.debug_str,when(!normal)]}"

Aquí, el campo "dbg" del registro solo contendrá un guion ('-') para
indicar un contenido ausente cuando la regla no se valida, y emitirá un
bloque completo de depuración cuando sí se valida.
```

Ejemplo

```haproxy
# log "dbg={-}" when fine, or "dbg={... debug info ...}" on slow transfers
acl slow_xfer res.timer.data ge 10000   # more than 10s is slow
log-format "$HAPROXY_HTTP_LOG_FMT                                         \
            fsdbg={%[fs.debug_str,when(acl,slow_xfer)]}                   \
            bsdbg={%[bs.debug_str,when(acl,slow_xfer)]}"
```

Ejemplo

```haproxy
# only emit the backend src/port when a real connection was issued:
log-format "$HAPROXY_HTTP_LOG_FMT \
           src=[%[bc_src,when(forwarded)]:%[bc_src_port,when(forwarded)]]"
```

Dado que interrumpe la evaluación de la expresión cuando no es verdadera, también es posible usarlo
para impedir que se llame a un conversor posterior. Esto puede usarse, por ejemplo, para llamar al
conversor debug() solo en caso de error, para registrar un elemento solo cuando sea absolutamente
necesario.

Ejemplo:

```shell
# emit the whole response headers list to stderr only on error and only
# when the output is a connection. We abuse a dummy variable here.
http-after-response set-var(res.test) \
              res.hdrs,when(error),when(forwarded),debug(hdrs,stderr)
```

Ver también: conversor debug

<a id="entry-7-3-1-word"></a>

**`word(<index>,<delimiters>[,<count>])`**

```haproxy
word(<index>,<delimiters>[,<count>])
```

Extrae la n-ésima palabra contando desde el principio (índice positivo) o desde el final (índice
negativo) considerando los delimitadores dados de una cadena de entrada. Los índices comienzan en
1 o -1 y los delimitadores son una lista de caracteres con formato de cadena. Las palabras vacías
se omiten. Esto significa que los delimitadores al principio o al final de la cadena de entrada se
ignoran y los delimitadores consecutivos dentro de la cadena de entrada se consideran un único
delimitador. Opcionalmente puedes especificar un `<count>` de palabras a extraer (por defecto: 1).
El valor 0 indica la extracción de todas las palabras restantes.

Ejemplo:

```text
str(f1_f2_f3__f5),word(4,_)    # f5
str(f1_f2_f3__f5),word(5,_)    # <not found>
str(f1_f2_f3__f5),word(2,_,0)  # f2_f3__f5
str(f1_f2_f3__f5),word(3,_,2)  # f3__f5
str(f1_f2_f3__f5),word(-2,_,3) # f1_f2_f3
str(f1_f2_f3__f5),word(-3,_,0) # f1_f2
str(/f1/f2/f3/f4),word(1,/)    # f1
str(/f1////f2/f3/f4),word(1,/) # f2
```

<a id="entry-7-3-1-wt6"></a>

**`wt6([<avalanche>])`**

```haproxy
wt6([<avalanche>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
función hash WT6. Opcionalmente, es posible aplicar una función hash de avalancha completa a la
salida si el argumento opcional `<avalanche>` es igual a 1. Este conversor usa las mismas funciones
que usan los diversos algoritmos de balanceo de carga basados en hash, por lo que proporcionará
exactamente los mismos resultados. Está destinado principalmente a la depuración, pero puede usarse
como entrada de una tabla de persistencia para recopilar estadísticas aproximadas. No debe usarse
con fines de seguridad, ya que romper un hash de 32 bits es trivial. Ver también "crc32", "djb2",
"sdbm", "crc32c" y la directiva "hash-type".

<a id="entry-7-3-1-x509-v-err-str"></a>

**`x509_v_err_str`**

```haproxy
x509_v_err_str
```

Convierte un valor numérico en el nombre de la constante X509_V_ERR correspondiente. Es útil en ACL
para disponer de una configuración que funciona con múltiples versiones de OpenSSL, ya que algunos
códigos pueden cambiar al cambiar de versión.

Cuando no se encuentra el nombre de la constante correspondiente, muestra el valor numérico como
una cadena.

La lista de constantes proporcionada por OpenSSL puede encontrarse en
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES> Ten
cuidado de leer la página correspondiente a la versión correcta de OpenSSL.

Ejemplo:

```text
bind :443 ssl crt common.pem ca-file ca-auth.crt verify optional crt-ignore-err X509_V_ERR_CERT_REVOKED,X509_V_ERR_CERT_HAS_EXPIRED

acl cert_expired ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_HAS_EXPIRED
acl cert_revoked ssl_c_verify,x509_v_err_str -m str X509_V_ERR_CERT_REVOKED
acl cert_ok      ssl_c_verify,x509_v_err_str -m str X509_V_OK

http-response add-header X-SSL Ok if cert_ok
http-response add-header X-SSL Expired if cert_expired
http-response add-header X-SSL Revoked if cert_revoked

http-response add-header X-SSL-verify %[ssl_c_verify,x509_v_err_str]
```

<a id="entry-7-3-1-xor"></a>

**`xor(<value>)`**

```haproxy
xor(<value>)
```

Realiza un "XOR" (OR exclusivo) a nivel de bits entre `<value>` y el valor de entrada de tipo
entero con signo, y devuelve el resultado como un entero con signo. `<value>` puede ser un valor
numérico o un nombre de variable. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más
detalles.

<a id="entry-7-3-1-xxh3"></a>

**`xxh3([<seed>])`**

```haproxy
xxh3([<seed>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad con signo de 64 bits usando la
variante de 64 bits XXH3 de la función hash XXhash. Este hash soporta una semilla cuyo valor por
defecto es cero, pero puede pasarse un valor diferente como argumento `<seed>`. Este hash es
conocido por ser muy bueno y muy rápido, por lo que puede usarse para calcular el hash de URLs
y/o parámetros de URL para usarlos como claves de tabla de persistencia y recopilar estadísticas
con una tasa de colisión baja, aunque se debe tener cuidado, ya que el algoritmo no se considera
criptográficamente seguro.

<a id="entry-7-3-1-xxh32"></a>

**`xxh32([<seed>])`**

```haproxy
xxh32([<seed>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad sin signo de 32 bits usando la
variante de 32 bits de la función hash XXHash. Este hash soporta una semilla cuyo valor por defecto
es cero, pero puede pasarse un valor diferente como argumento `<seed>`. Este hash es conocido por
ser muy bueno y muy rápido, por lo que puede usarse para calcular el hash de URLs y/o parámetros de
URL para usarlos como claves de tabla de persistencia y recopilar estadísticas con una tasa de
colisión baja, aunque se debe tener cuidado, ya que el algoritmo no se considera criptográficamente
seguro.

<a id="entry-7-3-1-xxh64"></a>

**`xxh64([<seed>])`**

```haproxy
xxh64([<seed>])
```

Calcula el hash de una muestra binaria de entrada en una cantidad con signo de 64 bits usando la
variante de 64 bits de la función hash XXHash. Este hash soporta una semilla cuyo valor por defecto
es cero, pero puede pasarse un valor diferente como argumento `<seed>`. Este hash es conocido por
ser muy bueno y muy rápido, por lo que puede usarse para calcular el hash de URLs y/o parámetros de
URL para usarlos como claves de tabla de persistencia y recopilar estadísticas con una tasa de
colisión baja, aunque se debe tener cuidado, ya que el algoritmo no se considera criptográficamente
seguro.

### 7.3.2. Obtención de muestras a partir de los estados internos {#section-7-3-2}

Un primer conjunto de métodos de obtención de muestras se aplica a información interna que ni
siquiera está relacionada con información del cliente. Estos se usan a veces con directivas
"monitor fail" para informar de un estado interno a observadores externos. Los métodos de
obtención de muestras descritos en esta sección son utilizables en cualquier lugar.

Resumen de los métodos de obtención de muestras de esta sección y sus tipos respectivos:

```text
  palabra clave                                    tipo de salida
-------------------------------------------------+-------------
acl([!]<name>[,...])                               boolean
act_conn                                           integer
always_false                                       boolean
always_true                                        boolean
avg_queue([<backend>])                             integer
be_conn([<backend>])                               integer
be_conn_free([<backend>])                          integer
be_sess_rate([<backend>])                          integer
bin(<hex>)                                         bin
bool(<bool>)                                       bool
connslots([<backend>])                             integer
cpu_calls                                          integer
cpu_ns_avg                                         integer
cpu_ns_tot                                         integer
date([<offset>[,<unit>]])                          integer
date_us                                            integer
env(<name>)                                        string
fe_conn([<frontend>])                              integer
fe_req_rate([<frontend>])                          integer
fe_sess_rate([<frontend>])                         integer
hostname                                           string
int(<integer>)                                     signed
ipv4(<ipv4>)                                       ipv4
ipv6(<ipv6>)                                       ipv6
last_entity                                        string
last_rule_file                                     string
last_rule_line                                     integer
lat_ns_avg                                         integer
lat_ns_tot                                         integer
meth(<method>)                                     method
nbsrv([<backend>])                                 integer
pid                                                integer
prio_class                                         integer
prio_offset                                        integer
proc                                               integer
queue([<backend>])                                 integer
quic_enabled                                       boolean
rand([<range>])                                    integer
srv_conn([<backend>/]<server>)                     integer
srv_conn_free([<backend>/]<server>)                integer
srv_is_up([<backend>/]<server>)                    boolean
srv_iweight([<backend>/]<server>)                  integer
srv_queue([<backend>/]<server>)                    integer
srv_sess_rate([<backend>/]<server>)                integer
srv_uweight([<backend>/]<server>)                  integer
srv_weight([<backend>/]<server>)                   integer
stopping                                           boolean
str(<string>)                                      string
table_avl([<table>])                               integer
table_cnt([<table>])                               integer
term_events                                        string
thread                                             integer
txn.id32                                           integer
txn.sess_term_state                                string
uptime                                             integer
uuid([<version>])                                  string
var(<var-name>[,<default>])                        undefined
wait_end                                           boolean
waiting_entity                                     string
-------------------------------------------------+-------------
```

Lista detallada:

<a id="entry-7-3-2-acl-boolean"></a>

**`acl([!]<name>[,...]): boolean`**

```haproxy
acl([!]<name>[,...]): boolean
```

Devuelve true si la evaluación de todas las ACL con nombre es true; en caso contrario, devuelve
false. Se pueden proporcionar hasta 12 ACL, cada una delimitada por comas. Cada ACL con nombre puede
ir precedida de un "!" para invertir el resultado. Si alguna evaluación produce un error, la muestra
también devuelve un error. Ten en cuenta que HAProxy no realiza ninguna comprobación de validación
sobre las ACL referenciadas, como por ejemplo si una ACL que usa una muestra de solicitud HTTP se
usa en un contexto de respuesta. Este comportamiento podría cambiar en el futuro.

act_conn: integer Devuelve el número total de conexiones simultáneas activas en el proceso.

always_false: boolean Siempre devuelve el valor booleano "false". Puede usarse con ACL como
sustituto temporal de otra cuando se ajustan configuraciones.

always_true: boolean Siempre devuelve el valor booleano "true". Puede usarse con ACL como sustituto
temporal de otra cuando se ajustan configuraciones.

<a id="entry-7-3-2-avg-queue-integer"></a>

**`avg_queue([<backend>]): integer`**

```haproxy
avg_queue([<backend>]): integer
```

Devuelve el número total de conexiones en cola del backend designado dividido por el número de
servidores activos. Se usa el backend actual si no se especifica ningún backend. Esto es muy
similar a "queue", excepto en que se considera el tamaño de la granja, para dar una medida más
precisa del tiempo que puede tardar en procesarse una nueva conexión. El uso principal es con ACL
para devolver una página de disculpa a los usuarios nuevos cuando es cierto que obtendrán un
servicio degradado, o para pasarlo a los servidores del backend en una cabecera para que decidan
trabajar en modo degradado o desactivar algunas funciones para acelerar un poco el procesamiento.
Ten en cuenta que en el caso de que ya no quedara ningún servidor activo, se consideraría como
valor medido el doble del número de conexiones en cola. Es una estimación razonable, ya que de
todos modos se espera que un servidor vuelva pronto, pero aún así preferimos enviar el tráfico
nuevo a otro backend si está en mejor estado. Ver también las obtenciones de muestras "queue",
"be_conn" y "be_sess_rate".

<a id="entry-7-3-2-be-conn-integer"></a>

**`be_conn([<backend>]): integer`**

```haproxy
be_conn([<backend>]): integer
```

Se aplica al número de conexiones establecidas actualmente en el backend, posiblemente incluyendo
la conexión que se está evaluando. Si no se especifica ningún nombre de backend, se usa el actual.
Pero también es posible comprobar otro backend. Puede usarse para usar una granja específica cuando
la nominal está llena. Ver también los criterios "fe_conn", "queue", "be_conn_free" y
"be_sess_rate".

<a id="entry-7-3-2-be-conn-free-integer"></a>

**`be_conn_free([<backend>]): integer`**

```haproxy
be_conn_free([<backend>]): integer
```

Devuelve un valor entero correspondiente al número de conexiones disponibles entre los servidores
disponibles del backend. No se incluyen los espacios de cola. Los servidores de respaldo tampoco se
incluyen, salvo que todos los demás servidores estén caídos. Si no se especifica ningún nombre de
backend, se usa el actual. Pero también es posible comprobar otro backend. Puede usarse para usar
una granja específica cuando la nominal está llena. Ver también los criterios "be_conn",
"connslots" y "srv_conn_free".

OTRAS ADVERTENCIAS Y NOTAS: si el maxconn o el maxqueue de cualquiera de los servidores es 0 (lo
que significa ilimitado), esta obtención claramente no tiene sentido, en cuyo caso el valor
devuelto será -1.

<a id="entry-7-3-2-be-sess-rate-integer"></a>

**`be_sess_rate([<backend>]): integer`**

```haproxy
be_sess_rate([<backend>]): integer
```

Devuelve un valor entero correspondiente a la tasa de creación de sesiones en el backend, en número
de sesiones nuevas por segundo. Esto se usa con ACL para cambiar a un backend alternativo cuando
uno caro o frágil alcanza una tasa de sesiones demasiado alta, o para limitar el abuso del servicio
(p. ej. evitar el vaciado de un diccionario en línea). También puede ser útil añadir este elemento
a los registros usando una directiva log-format.

Ejemplo:

```shell
# Redirect to an error page if the dictionary is requested too often
backend dynamic
    mode http
    acl being_scanned be_sess_rate gt 100
    redirect location /denied.html if being_scanned
```

<a id="entry-7-3-2-bin-bin"></a>

**`bin(<hex>): bin`**

```haproxy
bin(<hex>): bin
```

Devuelve una cadena binaria. La entrada es la representación hexadecimal de la cadena.

<a id="entry-7-3-2-bool-bool"></a>

**`bool(<bool>): bool`**

```haproxy
bool(<bool>): bool
```

Devuelve un valor booleano. `<bool>` puede ser 'true', 'false', '1' o '0'. 'false' y '0' son lo
mismo. 'true' y '1' son lo mismo.

<a id="entry-7-3-2-connslots-integer"></a>

**`connslots([<backend>]): integer`**

```haproxy
connslots([<backend>]): integer
```

Devuelve un valor entero correspondiente al número de espacios de conexión aún disponibles en el
backend, sumando la cantidad máxima de conexiones en todos los servidores y el tamaño máximo de
cola. Esto probablemente solo se usa con ACL.

La idea básica aquí es poder medir el número de "espacios" de conexión aún disponibles (conexión +
cola), de modo que cualquier cosa más allá de eso (uso previsto; ver la palabra clave
"use_backend") pueda redirigirse a un backend diferente.

'connslots' = número de espacios de conexión de servidor disponibles, + número de espacios de cola
de servidor disponibles.

Ten en cuenta que mientras "fe_conn" puede usarse, "connslots" resulta especialmente útil cuando se
da el caso de tráfico que va a una única ip y se divide en múltiples backends (quizá usando ACL
para hacer balanceo de carga basado en nombres) y se quiere poder diferenciar entre los diferentes
backends y sus "connslots" disponibles. Además, mientras que "nbsrv" solo mide los servidores que
están realmente *caídos*, esta obtención es más fina y también examina el número de espacios de
conexión disponibles. Ver también "queue" y "avg_queue".

OTRAS ADVERTENCIAS Y NOTAS: en este momento, el código no tiene en cuenta las conexiones dinámicas.
Además, si el maxconn o el maxqueue de cualquiera de los servidores es 0, esta obtención
claramente no tiene sentido, en cuyo caso el valor devuelto será -1.

cpu_calls: integer Devuelve el número de llamadas a la tarea que procesa el flujo o la solicitud
actual desde que se asignó. Este número se reinicia para cada nueva solicitud en las mismas
conexiones en caso de HTTP keep-alive. Este valor debería ser normalmente bajo y estable (alrededor
de 2 llamadas para una solicitud típicamente simple), pero puede volverse alto si se realiza algún
procesamiento (compresión, caché o análisis). Esto es puramente con fines de supervisión del
rendimiento.

cpu_ns_avg: integer Devuelve el número medio de nanosegundos invertidos en cada llamada a la tarea
que procesa el flujo o la solicitud actual. Este número se reinicia para cada nueva solicitud en
las mismas conexiones en caso de HTTP keep-alive. Este valor indica el coste global de procesar la
solicitud o la conexión en cada llamada. No hay un valor bueno ni malo, pero el tiempo invertido en
una llamada causa automáticamente latencia a otro procesamiento (ver lat_ns_avg más abajo) y puede
afectar al tiempo de respuesta aparente de otras conexiones. Ciertas operaciones como la compresión,
la coincidencia de expresiones regulares complejas o las operaciones Lua pesadas pueden afectar
directamente este valor, y tenerlo en los registros facilitará detectar el procesamiento
defectuoso que debe corregirse para recuperar un rendimiento decente. Nota: este valor es
exactamente cpu_ns_tot dividido por cpu_calls.

cpu_ns_tot: integer Devuelve el número total de nanosegundos invertidos en cada llamada a la tarea
que procesa el flujo o la solicitud actual. Este número se reinicia para cada nueva solicitud en
las mismas conexiones en caso de HTTP keep-alive. Este valor indica el coste global de procesar la
solicitud o la conexión en cada llamada. No hay un valor bueno ni malo, pero el tiempo invertido en
una llamada causa automáticamente latencia a otro procesamiento (ver lat_ns_avg más abajo), induce
costes de CPU en la máquina y puede afectar al tiempo de respuesta aparente de otras conexiones.
Ciertas operaciones como la compresión, la coincidencia de expresiones regulares complejas o las
operaciones Lua pesadas pueden afectar directamente este valor, y tenerlo en los registros
facilitará detectar el procesamiento defectuoso que debe corregirse para recuperar un rendimiento
decente. El valor puede ser artificialmente alto debido a un recuento alto de cpu_calls, por
ejemplo al procesar muchos fragmentos HTTP, y por esta razón a menudo se prefiere registrar
cpu_ns_avg en su lugar.

cpu_usage_grp: integer Devuelve el uso de CPU medido durante el último bucle de sondeo, entre 0 y
100, promediado sobre todos los hilos del grupo de hilos actual. Esto puede usarse para
diagnosticar problemas y para el registro. La medida es extremadamente volátil, pero seguirá siendo
precisa para cargas sostenidas, ya que cada hilo la mide a lo largo de unas decenas a centenas de
solicitudes.

cpu_usage_proc: integer Devuelve el uso de CPU medido durante el último bucle de sondeo, entre 0 y
100, promediado sobre todos los hilos en ejecución. Esto puede usarse para diagnosticar problemas y
para el registro. La medida es extremadamente volátil, pero seguirá siendo precisa para cargas
sostenidas, ya que cada hilo la mide a lo largo de unas decenas a centenas de solicitudes. Esto es
100 menos el valor informado en la proporción de inactividad de la página de estadísticas y en
"show info".

cpu_usage_thr: integer Devuelve el uso de CPU medido durante el último bucle de sondeo, entre 0 y
100, para el hilo que llama. Esto puede usarse para diagnosticar problemas y para el registro. La
medida es extremadamente volátil, pero seguirá siendo precisa para cargas sostenidas, ya que se
mide a lo largo de unas decenas a centenas de solicitudes. Es el mismo valor que se usa para decidir
activar la eliminación de conexiones ante demasiados glitches, o desactivar la compresión. Ver
también "tune.glitches.kill.cpu-usage" y "maxcompcpuusage".

<a id="entry-7-3-2-date-integer"></a>

**`date([<offset>[,<unit>]]): integer`**

```haproxy
date([<offset>[,<unit>]]): integer
```

Devuelve la fecha actual como el epoch (número de segundos desde 01/01/1970).

Si se especifica un valor de offset, se añade a la fecha actual antes de devolver el valor. Esto es
particularmente útil para calcular fechas relativas, ya que se permiten offsets tanto positivos
como negativos. Es útil combinado con el conversor http_date.

`<unit>` es opcional y puede establecerse a "s" para segundos (comportamiento por defecto), "ms"
para milisegundos o "us" para microsegundos. Si se establece la unidad, el valor devuelto es un
entero que refleja segundos, milisegundos o microsegundos desde epoch, más el offset. Es útil
cuando se necesita una resolución de tiempo inferior a un segundo.

Ejemplo:

```shell
# set an expires header to now+1 hour in every response
http-response set-header Expires %[date(3600),http_date]

# set an expires header to now+1 hour in every response, with
# millisecond granularity
http-response set-header Expires %[date(3600000,ms),http_date(0,ms)]
```

date_us: integer Devuelve la parte de microsegundos de la fecha (la parte de "segundos" la devuelve
la muestra date). Esta muestra es coherente con la muestra date, ya que proviene de la misma
estructura timeval.

<a id="entry-7-3-2-env-string"></a>

**`env(<name>): string`**

```haproxy
env(<name>): string
```

Devuelve una cadena que contiene el valor de la variable de entorno `<name>`. Como recordatorio,
las variables de entorno son por proceso y se muestrean cuando el proceso arranca. Esto puede ser
útil para pasar cierta información a un servidor del siguiente salto, o con ACL para tomar medidas
específicas cuando el proceso se arranca de una determinada manera.

Ejemplos:

```shell
# Pass the Via header to next hop with the local hostname in it
http-request add-header Via 1.1\ %[env(HOSTNAME)]

# reject cookie-less requests when the STOP environment variable is set
http-request deny if !{ req.cook(SESSIONID) -m found } { env(STOP) -m found }
```

<a id="entry-7-3-2-fe-conn-integer"></a>

**`fe_conn([<frontend>]): integer`**

```haproxy
fe_conn([<frontend>]): integer
```

Devuelve el número de conexiones establecidas actualmente en el frontend, posiblemente incluyendo
la conexión que se está evaluando. Si no se especifica ningún nombre de frontend, se usa el actual.
Pero también es posible comprobar otro frontend. Puede usarse para devolver una página de disculpa
antes del bloqueo definitivo, o para usar un backend específico en el que drenar las solicitudes
nuevas cuando la granja se considera llena. Esto se usa principalmente con ACL, pero también puede
usarse para pasar algunas estadísticas a los servidores en cabeceras HTTP. Ver también las
obtenciones "dst_conn", "be_conn" y "fe_sess_rate".

<a id="entry-7-3-2-fe-req-rate-integer"></a>

**`fe_req_rate([<frontend>]): integer`**

```haproxy
fe_req_rate([<frontend>]): integer
```

Devuelve un valor entero correspondiente al número de solicitudes HTTP por segundo enviadas a un
frontend. Este número puede diferir de "fe_sess_rate" en situaciones donde el keep-alive del lado
del cliente está activado.

<a id="entry-7-3-2-fe-sess-rate-integer"></a>

**`fe_sess_rate([<frontend>]): integer`**

```haproxy
fe_sess_rate([<frontend>]): integer
```

Devuelve un valor entero correspondiente a la tasa de creación de sesiones en el frontend, en
número de sesiones nuevas por segundo. Esto se usa con ACL para limitar la tasa de sesiones
entrantes a un rango aceptable para prevenir el abuso del servicio lo antes posible, por ejemplo
cuando se combina con otras ACL de capa 4 para forzar a los clientes a esperar un poco a que la
tasa baje por debajo del límite. También puede ser útil añadir este elemento a los registros
usando una directiva log-format. Ver también la directiva "rate-limit sessions" para su uso en
frontends.

Ejemplo:

```shell
# This frontend limits incoming mails to 10/s with a max of 100
# concurrent connections. We accept any connection below 10/s, and
# force excess clients to wait for 100 ms. Since clients are limited to
# 100 max, there cannot be more than 10 incoming mails per second.
frontend mail
    bind :25
    mode tcp
    maxconn 100
    acl too_fast fe_sess_rate ge 10
    tcp-request inspect-delay 100ms
    tcp-request content accept if ! too_fast
    tcp-request content accept if WAIT_END
```

hostname: string Devuelve el nombre de host del sistema.

<a id="entry-7-3-2-int-signed-integer"></a>

**`int(<integer>): signed integer`**

```haproxy
int(<integer>): signed integer
```

Devuelve un entero con signo.

<a id="entry-7-3-2-ipv4-ipv4"></a>

**`ipv4(<ipv4>): ipv4`**

```haproxy
ipv4(<ipv4>): ipv4
```

Devuelve una ipv4.

<a id="entry-7-3-2-ipv6-ipv6"></a>

**`ipv6(<ipv6>): ipv6`**

```haproxy
ipv6(<ipv6>): ipv6
```

Devuelve una ipv6.

last_entity: string Devuelve la identidad de la última entidad que fue evaluada durante el
análisis del flujo. Puede ser la regla final que coincidió o el filtro que interrumpió el
procesamiento.

Una regla final es aquella que termina la evaluación del conjunto de reglas (como un "accept",
"deny" o "redirect"). Esto funciona para las reglas de solicitud y respuesta TCP que actúan sobre
los conjuntos de reglas "content", y para las reglas HTTP de los conjuntos de reglas
"http-request", "http-response" y "http-after-response". Los conjuntos de reglas "redirect"
heredados no están soportados (dicha información no se almacena allí), y tampoco lo están los
conjuntos de reglas "tcp-request connection" ni "tcp-request session", porque la información se
almacena a nivel de flujo y los flujos no existen durante estas reglas. En ese caso, el valor
devuelto es equivalente a "last_rule_file:last_rule_line". Ver también "last_rule_file" y
"last_rule_line".

Para un filtro, se devuelve su identificador tal como lo definieron los desarrolladores. Si este
identificador no está definido, se devuelve un valor hexadecimal que corresponde a un identificador
interno único.

El propósito principal de esta función es poder informar en los registros de la última entidad que
interrumpió un procesamiento, para ayudar a depurar problemas. La información devuelta sobre las
entidades puede cambiar con el tiempo y no debe usarse para otra cosa que no sea la depuración.

Ejemplo:

```shell
# Log the last entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[last_entity,when(error)]
```

last_rule_file: string Devuelve el nombre del archivo de configuración que contiene la última regla
final que coincidió durante el análisis del flujo. Una regla final es aquella que termina la
evaluación del conjunto de reglas (como un "accept", "deny" o "redirect"). Esto funciona para las
reglas de solicitud y respuesta TCP que actúan sobre los conjuntos de reglas "content", y para las
reglas HTTP de los conjuntos de reglas "http-request", "http-response" y "http-after-response". Los
conjuntos de reglas "redirect" heredados no están soportados (dicha información no se almacena
allí), y tampoco lo están los conjuntos de reglas "tcp-request connection" ni "tcp-request
session", porque la información se almacena a nivel de flujo y los flujos no existen durante estas
reglas. El propósito principal de esta función es poder informar en los registros de dónde estaba
la regla que dio el veredicto final, para ayudar a averiguar, por ejemplo, por qué se denegó una
solicitud. Ver también "last_rule_line".

last_rule_line: integer Devuelve el número de línea en el archivo de configuración donde se
encuentra la última regla final que coincidió durante el análisis del flujo. Una regla final es
aquella que termina la evaluación del conjunto de reglas (como un "accept", "deny" o "redirect").
Esto funciona para las reglas de solicitud y respuesta TCP que actúan sobre los conjuntos de reglas
"content", y para las reglas HTTP de los conjuntos de reglas "http-request", "http-response" y
"http-after-response". Los conjuntos de reglas "redirect" heredados no están soportados (dicha
información no se almacena allí), y tampoco lo están los conjuntos de reglas "tcp-request
connection" ni "tcp-request session", porque la información se almacena a nivel de flujo y los
flujos no existen durante estas reglas. El propósito principal de esta función es poder informar en
los registros de dónde estaba la regla que dio el veredicto final, para ayudar a averiguar, por
ejemplo, por qué se denegó una solicitud. Ver también "last_rule_file".

lat_ns_avg: integer Devuelve el número medio de nanosegundos transcurridos entre el momento en que
la tarea que gestiona el flujo se despierta y el momento en que se la llama efectivamente. Este
número se reinicia para cada nueva solicitud en las mismas conexiones en caso de HTTP keep-alive.
Este valor indica la latencia global infligida a la solicitud actual por todas las demás
solicitudes que se procesan en paralelo, y es un indicador directo del rendimiento percibido debido
a los vecinos ruidosos. Para mantener el valor bajo, es posible reducir la profundidad de la cola
de ejecución del planificador usando "tune.runqueue-depth", reducir el número de eventos
simultáneos procesados a la vez usando "tune.maxpollevents", disminuir el valor nice del flujo
usando la opción "nice" en las líneas "bind" o en el frontend, activar la planificación de baja
latencia usando "tune.sched.low-latency", o buscar otras solicitudes pesadas en los registros
(aquellas que muestran valores grandes de "cpu_ns_avg"), cuyo procesamiento debe ajustarse o
corregirse. La compresión de búferes grandes puede ser la causante, igual que las expresiones
regulares pesadas o las listas largas de expresiones regulares. Nota: este valor es exactamente
lat_ns_tot dividido por cpu_calls.

lat_ns_tot: integer Devuelve el número total de nanosegundos transcurridos entre el momento en que
la tarea que gestiona el flujo se despierta y el momento en que se la llama efectivamente. Este
número se reinicia para cada nueva solicitud en las mismas conexiones en caso de HTTP keep-alive.
Este valor indica la latencia global infligida a la solicitud actual por todas las demás
solicitudes que se procesan en paralelo, y es un indicador directo del rendimiento percibido debido
a los vecinos ruidosos. Para mantener el valor bajo, es posible reducir la profundidad de la cola
de ejecución del planificador usando "tune.runqueue-depth", reducir el número de eventos
simultáneos procesados a la vez usando "tune.maxpollevents", disminuir el valor nice del flujo
usando la opción "nice" en las líneas "bind" o en el frontend, activar la planificación de baja
latencia usando "tune.sched.low-latency", o buscar otras solicitudes pesadas en los registros
(aquellas que muestran valores grandes de "cpu_ns_avg"), cuyo procesamiento debe ajustarse o
corregirse. La compresión de búferes grandes puede ser la causante, igual que las expresiones
regulares pesadas o las listas largas de expresiones regulares. Nota: aunque intuitivamente puede
parecer que la latencia total se suma a un tiempo de transferencia, casi nunca es cierto, porque
mientras una tarea espera la CPU, los búferes de red siguen llenándose y la siguiente llamada
procesará más de una sola vez. El valor puede ser artificialmente alto debido a un recuento alto
de cpu_calls, por ejemplo al procesar muchos fragmentos HTTP, y por esta razón a menudo se prefiere
registrar lat_ns_avg en su lugar, que es un indicador de rendimiento más relevante.

<a id="entry-7-3-2-meth-method"></a>

**`meth(<method>): method`**

```haproxy
meth(<method>): method
```

Devuelve un método.

<a id="entry-7-3-2-nbsrv-integer"></a>

**`nbsrv([<backend>]): integer`**

```haproxy
nbsrv([<backend>]): integer
```

Devuelve un valor entero correspondiente al número de servidores utilizables del backend actual o
del backend con nombre. Esto se usa principalmente con ACL, pero también puede ser útil al
añadirlo a los registros. Normalmente se usa para cambiar a un backend alternativo cuando el número
de servidores es demasiado bajo para manejar cierta carga. Es útil para informar de un fallo cuando
se combina con "monitor fail".

pid: integer Devuelve el PID del proceso actual. En la mayoría de los casos, este es el PID del
proceso worker.

prio_class: integer Devuelve la clase de prioridad del flujo actual para el modo http o de la
conexión para el modo tcp. El valor será el establecido por la última llamada a "http-request
set-priority-class" o "tcp-request content set-priority-class".

prio_offset: integer Devuelve el offset de prioridad del flujo actual para el modo http o de la
conexión para el modo tcp. El valor será el establecido por la última llamada a "http-request
set-priority-offset" o "tcp-request content set-priority-offset".

proc: integer Siempre devuelve el valor 1 (históricamente devolvería el número del proceso que
llama).

<a id="entry-7-3-2-queue-integer"></a>

**`queue([<backend>]): integer`**

```haproxy
queue([<backend>]): integer
```

Devuelve el número total de conexiones en cola del backend designado, incluyendo todas las
conexiones en las colas de servidores. Si no se especifica ningún nombre de backend, se usa el
actual, pero también es posible comprobar otro. Esto es útil con ACL o para pasar estadísticas a
los servidores del backend. Puede usarse para tomar medidas cuando la cola supera un nivel
conocido, lo que generalmente indica un pico de tráfico o una ralentización masiva de los
servidores. Una acción posible podría ser rechazar a los usuarios nuevos pero seguir aceptando a
los antiguos. Ver también las obtenciones "avg_queue", "be_conn" y "be_sess_rate".

quic_enabled: boolean Devuelve true cuando el soporte del protocolo de transporte QUIC fue
compilado y si los listeners QUIC no están desactivados por la opción global "tune.quic.listen".
Ver también la opción global "tune.quic.listen".

<a id="entry-7-3-2-rand-integer"></a>

**`rand([<range>]): integer`**

```haproxy
rand([<range>]): integer
```

Devuelve un valor entero aleatorio dentro de un rango de `<range>` valores posibles, comenzando en
cero. Si no se especifica el rango, el valor por defecto es 2^32, lo que da números entre 0 y
4294967295. Puede ser útil para pasar algunos valores necesarios para tomar decisiones de
enrutamiento, por ejemplo, o simplemente con fines de depuración. Este aleatorio no debe usarse con
fines de seguridad.

<a id="entry-7-3-2-srv-conn-integer"></a>

**`srv_conn([<backend>/]<server>): integer`**

```haproxy
srv_conn([<backend>/]<server>): integer
```

Devuelve un valor entero correspondiente al número de conexiones establecidas actualmente en el
servidor designado, posiblemente incluyendo la conexión que se está evaluando. Si se omite
`<backend>`, el servidor se busca en el backend actual. Puede usarse para usar una granja
específica cuando un servidor está lleno, o para informar al servidor de nuestra visión del número
de conexiones activas con él. Ver también los métodos de obtención "fe_conn", "be_conn", "queue" y
"srv_conn_free".

<a id="entry-7-3-2-srv-conn-free-integer"></a>

**`srv_conn_free([<backend>/]<server>): integer`**

```haproxy
srv_conn_free([<backend>/]<server>): integer
```

Devuelve un valor entero correspondiente al número de conexiones disponibles en el servidor
designado, posiblemente incluyendo la conexión que se está evaluando. El valor no incluye los
espacios de cola. Si se omite `<backend>`, el servidor se busca en el backend actual. Puede usarse
para usar una granja específica cuando un servidor está lleno, o para informar al servidor de
nuestra visión del número de conexiones activas con él. Ver también los métodos de obtención
"be_conn_free" y "srv_conn".

OTRAS ADVERTENCIAS Y NOTAS: si el maxconn del servidor es 0, esta obtención claramente no tiene
sentido, en cuyo caso el valor devuelto será -1.

<a id="entry-7-3-2-srv-is-up-boolean"></a>

**`srv_is_up([<backend>/]<server>): boolean`**

```haproxy
srv_is_up([<backend>/]<server>): boolean
```

Devuelve true cuando el servidor designado está UP, y false cuando está DOWN o en modo de
mantenimiento. Si se omite `<backend>`, el servidor se busca en el backend actual. Se usa
principalmente para tomar medidas basándose en un estado externo informado mediante una
comprobación de salud (p. ej. la disponibilidad de un sitio geográfico). Otro uso posible, que ya
es más un truco, consiste en usar servidores dummy como variables booleanas que pueden activarse o
desactivarse desde la CLI, de modo que las reglas que dependen de esas ACL puedan ajustarse en
tiempo real.

<a id="entry-7-3-2-srv-iweight-integer"></a>

**`srv_iweight([<backend>/]<server>): integer`**

```haproxy
srv_iweight([<backend>/]<server>): integer
```

Devuelve un entero correspondiente al peso inicial del servidor. Si se omite `<backend>`, el
servidor se busca en el backend actual. Ver también "srv_weight" y "srv_uweight".

<a id="entry-7-3-2-srv-queue-integer"></a>

**`srv_queue([<backend>/]<server>): integer`**

```haproxy
srv_queue([<backend>/]<server>): integer
```

Devuelve un valor entero correspondiente al número de conexiones actualmente pendientes en la cola
del servidor designado. Si se omite `<backend>`, el servidor se busca en el backend actual. A
veces puede usarse junto con la directiva "use-server" para forzar el uso de un servidor conocido
más rápido cuando no está muy cargado. Ver también los métodos de obtención de muestras "srv_conn",
"avg_queue" y "queue".

<a id="entry-7-3-2-srv-sess-rate-integer"></a>

**`srv_sess_rate([<backend>/]<server>): integer`**

```haproxy
srv_sess_rate([<backend>/]<server>): integer
```

Devuelve un entero correspondiente a la tasa de creación de sesiones en el servidor designado, en
número de sesiones nuevas por segundo. Si se omite `<backend>`, el servidor se busca en el backend
actual. Esto se usa principalmente con ACL, pero también puede tener sentido con los registros. Se
usa para cambiar a un backend alternativo cuando uno caro o frágil alcanza una tasa de sesiones
demasiado alta, o para limitar el abuso del servicio (p. ej. evitar que las solicitudes latentes
sobrecarguen los servidores).

Ejemplo:

```shell
# Redirect to a separate back
acl srv1_full srv_sess_rate(be1/srv1) gt 50
acl srv2_full srv_sess_rate(be1/srv2) gt 50
use_backend be2 if srv1_full or srv2_full
```

<a id="entry-7-3-2-srv-uweight-integer"></a>

**`srv_uweight([<backend>/]<server>): integer`**

```haproxy
srv_uweight([<backend>/]<server>): integer
```

Devuelve un entero correspondiente al peso del servidor tal como lo ve el usuario. Si se omite
`<backend>`, el servidor se busca en el backend actual. Ver también "srv_weight" y "srv_iweight".

<a id="entry-7-3-2-srv-weight-integer"></a>

**`srv_weight([<backend>/]<server>): integer`**

```haproxy
srv_weight([<backend>/]<server>): integer
```

Devuelve un entero correspondiente al peso actual (o efectivo) del servidor. Si se omite
`<backend>`, el servidor se busca en el backend actual. Ver también "srv_iweight" y "srv_uweight".

stopping: boolean Devuelve TRUE si el proceso que llama a la función se está deteniendo
actualmente. Esto puede ser útil para el registro, o para relajar ciertas comprobaciones o ayudar
a cerrar ciertas conexiones durante un apagado controlado.

<a id="entry-7-3-2-str-string"></a>

**`str(<string>): string`**

```haproxy
str(<string>): string
```

Devuelve una cadena.

<a id="entry-7-3-2-table-avl-integer"></a>

**`table_avl([<table>]): integer`**

```haproxy
table_avl([<table>]): integer
```

Devuelve el número total de entradas disponibles en la tabla de persistencia del proxy actual o en
la tabla de persistencia designada. Ver también "table_cnt".

<a id="entry-7-3-2-table-cnt-integer"></a>

**`table_cnt([<table>]): integer`**

```haproxy
table_cnt([<table>]): integer
```

Devuelve el número total de entradas actualmente en uso en la tabla de persistencia del proxy
actual o en la tabla de persistencia designada. Ver también "table_conn_cnt" y table_avl para otros
métodos de recuento de entradas.

term_events: string Devuelve todos los eventos de terminación conocidos para todas las entidades
adjuntas a un flujo, en los lados de cliente y de servidor. Se devuelve una tupla de siete
elementos con la siguiente información:

    - los eventos de terminación de la conexión del frontend
    - los eventos de terminación de la conexión multiplexada del frontend
    - los eventos de terminación del descriptor del extremo de flujo del frontend
      (el flujo multiplexado o el applet)
    - los eventos de terminación del flujo
    - los eventos de terminación del descriptor del extremo de flujo del backend
      (el flujo multiplexado o el applet)
    - los eventos de terminación de la conexión multiplexada del backend
    - los eventos de terminación de la conexión del backend

En cada nivel, se informan los primeros cuatro eventos. Se devuelve una cadena vacía si aún no se
informó de ningún evento para un nivel específico. Si los eventos de terminación no están
soportados, se devuelve un "-".

Solo debe usarse con fines de depuración. El formato exacto no está documentado porque puede
evolucionar según los requisitos de los desarrolladores.

tgroup: integer Devuelve un valor entero correspondiente a la posición del grupo de hilos que
llama a la función, entre 0 y (global.thread-groups - 1). Esto es útil para el registro y la
depuración.

thread: integer Devuelve un valor entero correspondiente a la posición del hilo que llama a la
función, entre 0 y (global.nbthread-1). Esto es útil para el registro y la depuración.

txn.id32: integer Devuelve el ID interno de la transacción. Es un entero de 32bits. Por tanto, en términos absolutos, su valor no es único; los IDs de transacción pueden dar la vuelta. El periodo hasta dar
la vuelta depende de la tasa de solicitudes. En la práctica, no debería ser un problema. Para un ID
verdaderamente único, ver la directiva "unique-id-format".

txn.sess_term_state: string Devuelve el estado de terminación del flujo TCP o HTTP, tal como se
informa en el registro. Es una cadena de 2 caracteres: el estado final del flujo seguido del evento
que causó su terminación. Consulta la [sección 8.5](/es/haproxy/configuration-logging/#section-8-5) sobre el estado del flujo en la desconexión para la lista de eventos posibles. Se devuelve el
valor actual en el momento en que se evalúa la obtención de la muestra. Está sujeto a cambios.
Excepto si se usa con ACL en conjuntos de reglas "http-after-response" o en mensajes de registro,
siempre será "--".

Ejemplo:

```shell
# Return a 429-Too-Many-Requests if stream timed out in queue
http-after-response set-status 429 if { txn.sess_term_state  "sQ" }
```

uptime: integer Devuelve el tiempo de actividad del worker de HAProxy actual en segundos.

<a id="entry-7-3-2-uuid-string"></a>

**`uuid([<version>]): string`**

```haproxy
uuid([<version>]): string
```

Devuelve un UUID conforme al estándar RFC 9562. Si no se especifica la versión, se devuelve un
UUID versión 4 (completamente aleatorio).

Las versiones 4 y 7 están soportadas.

<a id="entry-7-3-2-var-undefined"></a>

**`var(<var-name>[,<default>]): undefined`**

```haproxy
var(<var-name>[,<default>]): undefined
```

Devuelve una variable con el tipo almacenado. Si la variable no está establecida, la obtención de
la muestra falla, salvo que se proporcione un valor por defecto, en cuyo caso lo devolverá como
cadena. Se permiten las cadenas vacías. Consulta la [sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

<a id="entry-7-3-2-dump-all-vars-string"></a>

**`dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string`**

```haproxy
dump_all_vars([<scope>][,<prefix>][,<delimiter>]): string
```

Devuelve una lista de todas las variables en el ámbito especificado, opcionalmente filtradas por
prefijo de nombre y con un delimitador personalizable.

Formato de salida: var1=value1`<delim>`var2=value2`<delim>`...

Codificación de valores por tipo:

- Cadenas: entre comillas y con escapes (", &#92;, &#92;r,
  &#92;n, &#92;b, &#92;0) Ejemplo:
  txn.name="John &#92;"Doe&#92;""
- Binario: codificado en hexadecimal con prefijo 'x', sin comillas Ejemplo: txn.data=x48656c6c6f
- Enteros: decimal sin comillas Ejemplo: txn.count=42
- Booleanos: "true" o "false" sin comillas Ejemplo: txn.active=true
- Direcciones: cadena de dirección IP sin comillas Ejemplo: txn.client=192.168.1.1
- Métodos HTTP: cadena entre comillas Ejemplo: req.method="GET"

Argumentos:

- `<scope>` (opcional): sess, txn, req, res o proc. Si se omite, todos estos ámbitos se recorren
  en el mismo orden en que se presentan aquí.

- `<prefix>` (opcional): filtra las variables cuyos nombres comienzan por el prefijo especificado
  (tras eliminar el prefijo de ámbito). Nota de rendimiento: cuando se usa el filtrado por
  prefijo, todas las variables del ámbito se siguen recorriendo. Esto no debería usarse con
  configuraciones que involucren miles de variables.

- `<delimiter>` (opcional): cadena para separar las variables. Por defecto es ", " (coma y
  espacio). Puede personalizarse con cualquier cadena. Como recordatorio, para pasar comas o
  espacios en un argumento de función, deben ir entre comillas simples o dobles (si la expresión
  misma ya está entre comillas, usa las otras).

Valor devuelto:

- En caso de éxito: cadena que contiene todas las variables coincidentes
- En caso de fallo: vacío (la obtención de la muestra falla) si el búfer de salida es demasiado
  pequeño. La función no truncará la salida; falla completamente para evitar datos parciales.

Esto es particularmente útil para depurar, registrar o exportar estados de variables.

Ejemplos:

```shell
# Dump all transaction variables
http-request return string %[dump_all_vars(txn)]

# Dump only variables starting with "user"
http-request set-header X-User-Vars "%[dump_all_vars(txn,user)]"

# Dump all process variables
http-request return string %[dump_all_vars(proc)]

# Custom delimiter (semicolon)
http-request set-header X-Vars "%[dump_all_vars(txn,,; )]"

# Force the default delimiter (comma space)
http-request set-header X-Vars "%[dump_all_vars(txn,,', ')]"

# Prefix filter with custom delimiter
http-request set-header X-Session "%[dump_all_vars(sess,user,|)]"

```

wait_end: boolean Esta obtención bien devuelve true cuando el periodo de inspección ha terminado, o
no obtiene nada. Solo se usa en ACL, junto con el análisis de contenido para evitar devolver un
veredicto erróneo prematuramente. También puede usarse para retrasar algunas acciones, como un
rechazo diferido para ciertas direcciones especiales. Dado que bien detiene la evaluación de las
reglas o devuelve inmediatamente true, se recomienda usar esta ACL como la última de una regla.
Ten en cuenta que la ACL por defecto "WAIT_END" siempre es utilizable sin declaración previa. Esta
prueba fue diseñada para usarse con la inspección de contenido de solicitudes TCP.

Ejemplos:

```shell
# delay every incoming request by 2 seconds
tcp-request inspect-delay 2s
tcp-request content accept if WAIT_END

# don't immediately tell bad guys they are rejected
tcp-request inspect-delay 10s
acl goodguys src 10.0.0.0/24
acl badguys  src 10.0.1.0/24
tcp-request content accept if goodguys
tcp-request content reject if badguys WAIT_END
tcp-request content reject
```

waiting_entity: string Devuelve la identidad de la entidad que estaba esperando continuar su
procesamiento cuando se encontró un error o un tiempo de espera agotado. Puede ser, por ejemplo,
una regla o un filtro. Sin embargo, esta lista no es exhaustiva y el formato de todas las posibles
entidades no está necesariamente documentado.

Cuando la entidad es una regla, se devuelve su ubicación. Es el archivo de configuración que
contiene la regla seguido de la línea donde la regla está definida en ese archivo, separados por
dos puntos.

Para un filtro, se devuelve su identificador tal como lo definieron los desarrolladores. Si este
identificador no está definido, se devuelve un valor hexadecimal que corresponde a un identificador
interno único.

El propósito principal de esta función es poder informar en los registros de la entidad que
bloqueaba el análisis del flujo cuando se encontró un error o un tiempo de espera agotado,
interrumpiendo este procesamiento, para ayudar a depurar problemas. La información devuelta sobre
las entidades puede cambiar con el tiempo y no debe usarse para otra cosa que no sea la depuración.

Ejemplo:

```shell
# Log the waiting entity, if any, and only if an error is reported
log-format "$HAPROXY_HTTP_LOG_FMT %{Q}[waiting_entity,when(error)]
```

### 7.3.3. Obtención de muestras en la capa 4 {#section-7-3-3}

La capa 4 normalmente describe solo la capa de transporte que, en HAProxy, es la más cercana a la
conexión, donde todavía no hay contenido disponible. Los métodos de obtención descritos aquí son
utilizables tan pronto como en los conjuntos de reglas "tcp-request connection", salvo que
requieran información futura. Estos generalmente incluyen direcciones y puertos TCP/IP, así como
elementos de las tablas de persistencia relacionados con la conexión entrante. Para recuperar un
valor de los contadores persistentes, el número de contador puede establecerse explícitamente como
0, 1 o 2 usando el prefijo predefinido "sc0\_", "sc1\_" o "sc2\_". Estos tres prefijos
predefinidos solo pueden usarse si el valor global "tune.stick-counters" no supera 3; en caso
contrario, el número de contador puede especificarse como el primer argumento entero al usar el
prefijo "sc\_" desde "sc_0" hasta "sc_N", donde N es (tune.stick-counters-1). Una tabla opcional
puede especificarse con la forma "sc\*", en cuyo caso la clave rastreada actualmente se buscará en
esta tabla alternativa en lugar de en la tabla que se está rastreando actualmente.

Resumen de los métodos de obtención de muestras de esta sección y sus tipos respectivos:

```text
  palabra clave                                    tipo de salida
-------------------------------------------------+-------------
accept_date([<unit>])                              integer
bc.timer.connect                                   integer
bc_be_queue                                        integer
bc_dst                                             ip
bc_dst_port                                        integer
bc_err                                             integer
bc_err_name                                        string
bc_err_str                                         string
bc_glitches                                        integer
bc_http_major                                      integer
bc_nb_streams                                      integer
bc_reused                                          boolean
bc_rtt(<unit>)                                     integer
bc_rttvar(<unit>)                                  integer
bc_settings_streams_limit                          integer
bc_src                                             ip
bc_src_port                                        integer
bc_srv_queue                                       integer
be_id                                              integer
be_name                                            string
be_connect_timeout                                 integer
be_queue_timeout                                   integer
be_server_timeout                                  integer
be_tarpit_timeout                                  integer
be_tunnel_timeout                                  integer
bytes_in                                           integer
bytes_out                                          integer
cur_connect_timeout                                integer
cur_client_timeout                                 integer
cur_queue_timeout                                  integer
cur_server_timeout                                 integer
cur_tarpit_timeout                                 integer
cur_tunnel_timeout                                 integer
dst                                                ip
dst_conn                                           integer
dst_is_local                                       boolean
dst_port                                           integer
fc.timer.handshake                                 integer
fc.timer.total                                     integer
fc_dst                                             ip
fc_dst_is_local                                    boolean
fc_dst_port                                        integer
fc_err                                             integer
fc_err_name                                        string
fc_err_str                                         string
fc_fackets                                         integer
fc_glitches                                        integer
fc_http_major                                      integer
fc_lost                                            integer
fc_nb_streams                                      integer
fc_pp_authority                                    string
fc_pp_tlv(<id>)                                    string
fc_pp_unique_id                                    string
fc_rcvd_proxy                                      boolean
fc_reordering                                      integer
fc_retrans                                         integer
fc_rtt(<unit>)                                     integer
fc_rttvar(<unit>)                                  integer
fc_sacked                                          integer
fc_saved_syn                                       binary
fc_settings_streams_limit                          integer
fc_src                                             ip
fc_src_is_local                                    boolean
fc_src_port                                        integer
fc_unacked                                         integer
fe_tarpit_timeout                                  integer
fe_client_timeout                                  integer
fe_defbe                                           string
fe_id                                              integer
fe_name                                            string
req.bytes_in                                       integer
req.bytes_out                                      integer
res.bytes_in                                       integer
res.bytes_out                                      integer
res.timer.data                                     integer
sc0_bytes_in_rate([<table>])                       integer
sc0_bytes_out_rate([<table>])                      integer
sc0_clr_gpc0([<table>])                            integer
sc0_clr_gpc1([<table>])                            integer
sc0_conn_cnt([<table>])                            integer
sc0_conn_cur([<table>])                            integer
sc0_conn_rate([<table>])                           integer
sc0_get_gpc0([<table>])                            integer
sc0_get_gpc1([<table>])                            integer
sc0_get_gpt0([<table>])                            integer
sc0_glitch_cnt([<table>])                          integer
sc0_glitch_rate([<table>])                         integer
sc0_gpc0_rate([<table>])                           integer
sc0_gpc1_rate([<table>])                           integer
sc0_http_err_cnt([<table>])                        integer
sc0_http_err_rate([<table>])                       integer
sc0_http_fail_cnt([<table>])                       integer
sc0_http_fail_rate([<table>])                      integer
sc0_http_req_cnt([<table>])                        integer
sc0_http_req_rate([<table>])                       integer
sc0_inc_gpc0([<table>])                            integer
sc0_inc_gpc1([<table>])                            integer
sc0_kbytes_in([<table>])                           integer
sc0_kbytes_out([<table>])                          integer
sc0_key                                            any
sc0_sess_cnt([<table>])                            integer
sc0_sess_rate([<table>])                           integer
sc0_tracked([<table>])                             boolean
sc0_trackers([<table>])                            integer
sc1_bytes_in_rate([<table>])                       integer
sc1_bytes_out_rate([<table>])                      integer
sc1_clr_gpc0([<table>])                            integer
sc1_clr_gpc1([<table>])                            integer
sc1_conn_cnt([<table>])                            integer
sc1_conn_cur([<table>])                            integer
sc1_conn_rate([<table>])                           integer
sc1_get_gpc0([<table>])                            integer
sc1_get_gpc1([<table>])                            integer
sc1_get_gpt0([<table>])                            integer
sc1_glitch_cnt([<table>])                          integer
sc1_glitch_rate([<table>])                         integer
sc1_gpc0_rate([<table>])                           integer
sc1_gpc1_rate([<table>])                           integer
sc1_http_err_cnt([<table>])                        integer
sc1_http_err_rate([<table>])                       integer
sc1_http_fail_cnt([<table>])                       integer
sc1_http_fail_rate([<table>])                      integer
sc1_http_req_cnt([<table>])                        integer
sc1_http_req_rate([<table>])                       integer
sc1_inc_gpc0([<table>])                            integer
sc1_inc_gpc1([<table>])                            integer
sc1_kbytes_in([<table>])                           integer
sc1_kbytes_out([<table>])                          integer
sc1_key                                            any
sc1_sess_cnt([<table>])                            integer
sc1_sess_rate([<table>])                           integer
sc1_tracked([<table>])                             boolean
sc1_trackers([<table>])                            integer
sc2_bytes_in_rate([<table>])                       integer
sc2_bytes_out_rate([<table>])                      integer
sc2_clr_gpc0([<table>])                            integer
sc2_clr_gpc1([<table>])                            integer
sc2_conn_cnt([<table>])                            integer
sc2_conn_cur([<table>])                            integer
sc2_conn_rate([<table>])                           integer
sc2_get_gpc0([<table>])                            integer
sc2_get_gpc1([<table>])                            integer
sc2_get_gpt0([<table>])                            integer
sc2_glitch_cnt([<table>])                          integer
sc2_glitch_rate([<table>])                         integer
sc2_gpc0_rate([<table>])                           integer
sc2_gpc1_rate([<table>])                           integer
sc2_http_err_cnt([<table>])                        integer
sc2_http_err_rate([<table>])                       integer
sc2_http_fail_cnt([<table>])                       integer
sc2_http_fail_rate([<table>])                      integer
sc2_http_req_cnt([<table>])                        integer
sc2_http_req_rate([<table>])                       integer
sc2_inc_gpc0([<table>])                            integer
sc2_inc_gpc1([<table>])                            integer
sc2_kbytes_in([<table>])                           integer
sc2_kbytes_out([<table>])                          integer
sc2_key                                            any
sc2_sess_cnt([<table>])                            integer
sc2_sess_rate([<table>])                           integer
sc2_tracked([<table>])                             boolean
sc2_trackers([<table>])                            integer
sc_bytes_in_rate(<ctr>[,<table>])                  integer
sc_bytes_out_rate(<ctr>[,<table>])                 integer
sc_clr_gpc(<idx>,<ctr>[,<table>])                  integer
sc_clr_gpc0(<ctr>[,<table>])                       integer
sc_clr_gpc1(<ctr>[,<table>])                       integer
sc_conn_cnt(<ctr>[,<table>])                       integer
sc_conn_cur(<ctr>[,<table>])                       integer
sc_conn_rate(<ctr>[,<table>])                      integer
sc_get_gpc(<idx>,<ctr>[,<table>])                  integer
sc_get_gpc0(<ctr>[,<table>])                       integer
sc_get_gpc1(<ctr>[,<table>])                       integer
sc_get_gpt(<idx>,<ctr>[,<table>])                  integer
sc_get_gpt0(<ctr>[,<table>])                       integer
sc_glitch_cnt(<ctr>[,<table>])                     integer
sc_glitch_rate(<ctr>[,<table>])                    integer
sc_gpc0_rate(<ctr>[,<table>])                      integer
sc_gpc1_rate(<ctr>[,<table>])                      integer
sc_gpc_rate(<idx>,<ctr>[,<table>])                 integer
sc_http_err_cnt(<ctr>[,<table>])                   integer
sc_http_err_rate(<ctr>[,<table>])                  integer
sc_http_fail_cnt(<ctr>[,<table>])                  integer
sc_http_fail_rate(<ctr>[,<table>])                 integer
sc_http_req_cnt(<ctr>[,<table>])                   integer
sc_http_req_rate(<ctr>[,<table>])                  integer
sc_inc_gpc(<idx>,<ctr>[,<table>])                  integer
sc_inc_gpc0(<ctr>[,<table>])                       integer
sc_inc_gpc1(<ctr>[,<table>])                       integer
sc_kbytes_in(<ctr>[,<table>])                      integer
sc_kbytes_out(<ctr>[,<table>])                     integer
sc_key(<ctr>)                                      any
sc_sess_cnt(<ctr>[,<table>])                       integer
sc_sess_rate(<ctr>[,<table>])                      integer
sc_tracked(<ctr>[,<table>])                        boolean
sc_trackers(<ctr>[,<table>])                       integer
so_id                                              integer
so_name                                            string
src                                                ip
src_bytes_in_rate([<table>])                       integer
src_bytes_out_rate([<table>])                      integer
src_clr_gpc(<idx>[,<table>])                       integer
src_clr_gpc0([<table>])                            integer
src_clr_gpc1([<table>])                            integer
src_conn_cnt([<table>])                            integer
src_conn_cur([<table>])                            integer
src_conn_rate([<table>])                           integer
src_get_gpc(<idx>[,<table>])                       integer
src_get_gpc0([<table>])                            integer
src_get_gpc1([<table>])                            integer
src_get_gpt(<idx>[,<table>])                       integer
src_get_gpt0([<table>])                            integer
src_glitch_cnt([<table>])                          integer
src_glitch_rate([<table>])                         integer
src_gpc0_rate([<table>])                           integer
src_gpc1_rate([<table>])                           integer
src_gpc_rate(<idx>[,<table>])                      integer
src_http_err_cnt([<table>])                        integer
src_http_err_rate([<table>])                       integer
src_http_fail_cnt([<table>])                       integer
src_http_fail_rate([<table>])                      integer
src_http_req_cnt([<table>])                        integer
src_http_req_rate([<table>])                       integer
src_inc_gpc(<idx>[,<table>])                       integer
src_inc_gpc0([<table>])                            integer
src_inc_gpc1([<table>])                            integer
src_is_local                                       boolean
src_kbytes_in([<table>])                           integer
src_kbytes_out([<table>])                          integer
src_port                                           integer
src_sess_cnt([<table>])                            integer
src_sess_rate([<table>])                           integer
src_updt_conn_cnt([<table>])                       integer
srv_id                                             integer
srv_name                                           string
txn.conn_retries                                   integer
txn.redispatched                                   boolean
-------------------------------------------------+-------------
```

Lista detallada:

<a id="entry-7-3-3-accept-date-integer"></a>

**`accept_date([<unit>]): integer`**

```haproxy
accept_date([<unit>]): integer
```

Esta es la fecha exacta en que HAProxy recibió la conexión (que podría diferir muy ligeramente de
la fecha observada en la red si hubo algo de cola en la lista de pendientes del sistema). Esta
suele ser la misma fecha que puede aparecer en el registro de cualquier cortafuegos aguas arriba.
Cuando se usa en modo HTTP, el campo accept_date se reinicia al primer momento en que la conexión
está lista para recibir una nueva solicitud (fin de la respuesta anterior para HTTP/1,
inmediatamente después de la solicitud anterior para HTTP/2).

Devuelve un valor en número de segundos desde epoch.

`<unit>` es opcional y puede establecerse a "s" para segundos (comportamiento por defecto), "ms"
para milisegundos o "us" para microsegundos. Si se establece la unidad, el valor devuelto es un
entero que refleja segundos, milisegundos o microsegundos desde epoch. Es útil cuando se necesita
una resolución de tiempo inferior a un segundo.

bc.timer.connect: integer Tiempo total para establecer la conexión TCP con el servidor. Esto es el
equivalente de %Tc en el log-format. Se informa en milisegundos (ms). Para más información, ver la
[Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) "Eventos de temporización"

bc_be_queue: integer Número de flujos extraídos de la cola mientras esperaban un espacio de
conexión en el backend de destino. Esto es el equivalente de %bq en el log-format.

bc_dst: ip Esta es la dirección IP de destino de la conexión en el lado del servidor, que es la
dirección del servidor al que HAProxy se conectó. Es de tipo IP y funciona tanto en tablas IPv4
como IPv6. En las tablas IPv6, la dirección IPv4 se mapea a su equivalente IPv6, de acuerdo con el
RFC 4291.

bc_dst_port: integer Devuelve un valor entero correspondiente al puerto TCP de destino de la
conexión en el lado del servidor, que es el puerto al que HAProxy se conectó.

bc_err: integer Devuelve el ID del error que podría haber ocurrido en la conexión del backend
actual. Ver la obtención "fc_err_str" para una lista completa de los códigos de error y sus
mensajes de error correspondientes.

bc_err_name: string Devuelve el nombre interno del error que describe qué problema ocurrió en la
conexión del backend, que resulta en un fallo de conexión. Esta cadena está formada por una sola
palabra y está vacía cuando no hay error presente. Corresponde a la columna «nombre» de la tabla
presentada en la palabra clave "fc_err_str".

bc_err_str: string Devuelve un mensaje de error que describe qué problema ocurrió en la conexión
del backend actual, que resulta en un fallo de conexión. Ver la obtención "fc_err_str" para una
lista completa de los códigos de error y sus mensajes de error correspondientes.

bc_glitches: integer Devuelve el número de glitches de protocolo contados en la conexión del
backend. Estos generalmente cubren violaciones de protocolo así como pequeñas anomalías que
generalmente indican un servidor defectuoso o con mal comportamiento que puede causar problemas en
la infraestructura (p. ej. provocar abortos tempranos de conexiones, inducir renegociaciones TLS
frecuentes). También pueden estar causados por respuestas demasiado grandes que no caben en un
único búfer, lo que explica los errores HTTP 502. Idealmente, este número debería permanecer en
cero, aunque generalmente está bien si permanece muy bajo comparado con el número total de
solicitudes. Estos valores normalmente no deberían considerarse alarmantes (especialmente los
pequeños), aunque un salto repentino puede indicar una anomalía en algún lugar. No todos los
multiplexores de protocolo miden esta métrica y la única forma de obtener más detalles sobre los
eventos es activar trazas para capturar todos los intercambios.

bc_http_major: integer Devuelve la codificación de la versión principal HTTP de la conexión del
backend, que puede ser 1 para HTTP/0.9 a HTTP/1.1 o 2 para HTTP/2. Ten en cuenta que esto se basa
en la codificación on-wire y no en la versión presente en la cabecera de la solicitud.

bc_nb_streams: integer Devuelve el número de flujos abiertos en la conexión del backend.

bc_reused: boolean Devuelve true si la transferencia se realizó mediante una conexión del backend
reutilizada.

<a id="entry-7-3-3-bc-rtt-integer"></a>

**`bc_rtt(<unit>): integer`**

```haproxy
bc_rtt(<unit>): integer
```

Devuelve el Round Trip Time (RTT) medido por el kernel para la conexión del backend. `<unit>` es
opcional; por defecto la unidad es milisegundos. `<unit>` puede establecerse a "ms" para
milisegundos o "us" para microsegundos. Si la conexión con el servidor no está establecida, si la
conexión no es TCP o si el sistema operativo no soporta TCP_INFO, por ejemplo los kernels Linux
anteriores a 2.4, la obtención de la muestra falla.

<a id="entry-7-3-3-bc-rttvar-integer"></a>

**`bc_rttvar(<unit>): integer`**

```haproxy
bc_rttvar(<unit>): integer
```

Devuelve la varianza del Round Trip Time (RTT) medida por el kernel para la conexión del backend.
`<unit>` es opcional; por defecto la unidad es milisegundos. `<unit>` puede establecerse a "ms"
para milisegundos o "us" para microsegundos. Si la conexión con el servidor no está establecida,
si la conexión no es TCP o si el sistema operativo no soporta TCP_INFO, por ejemplo los kernels
Linux anteriores a 2.4, la obtención de la muestra falla.

bc_settings_streams_limit: integer Devuelve el número máximo de flujos permitidos en la conexión
del backend. Para conexiones TCP y HTTP/1.1, siempre es 1. Para otros protocolos, depende de los
ajustes negociados con el servidor.

bc_src: ip Esta es la dirección IP de origen de la conexión en el lado del servidor, que es la
dirección del servidor desde la que HAProxy se conectó. Es de tipo IP y funciona tanto en tablas
IPv4 como IPv6. En las tablas IPv6, las direcciones IPv4 se mapean a su equivalente IPv6, de
acuerdo con el RFC 4291.

bc_src_port: integer Devuelve un valor entero correspondiente al puerto TCP de origen de la
conexión en el lado del servidor, que es el puerto desde el que HAProxy se conectó.

bc_srv_queue: integer Número de flujos extraídos de la cola mientras esperaban un espacio de
conexión en el servidor de destino. Esto es el equivalente de %sq en el log-format.

be_id: integer Devuelve un entero que contiene el id del backend actual. Puede usarse en frontends
con respuestas para comprobar qué backend procesó la solicitud. Si se usa en un frontend y no se
usó ningún backend, devuelve el id del frontend actual. También puede usarse en un conjunto de
reglas tcp-check o http-check.

be_connect_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de
espera de conexión del backend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout". Ver también "cur_connect_timeout".

be_name: string Devuelve una cadena que contiene el nombre del backend actual. Puede usarse en
frontends con respuestas para comprobar qué backend procesó la solicitud. Si se usa en un
frontend y no se usó ningún backend, devuelve el nombre del frontend actual. También puede usarse
en un conjunto de reglas tcp-check o http-check.

be_queue_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
de cola del backend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout". Ver también "cur_queue_timeout".

be_server_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
de servidor del backend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout". Ver también "cur_server_timeout".

be_tarpit_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
de cola del backend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout". Ver también "cur_tarpit_timeout".

be_tunnel_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
de túnel del backend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout". Ver también "cur_tunnel_timeout".

bytes_in: integer Ver "req.bytes_in".

bytes_out: integer Ver "res.bytes_in".

cur_connect_timeout: integer Devuelve el tiempo de espera de conexión actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a be_connect_timeout salvo que
se haya aplicado una regla "set-timeout". Ver también "be_connect_timeout".

cur_client_timeout: integer Devuelve el tiempo de espera de cliente actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a fe_client_timeout salvo que
se haya aplicado una regla "set-timeout". Ver también "fe_client_timeout".

cur_queue_timeout: integer Devuelve el tiempo de espera de cola actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a be_queue_timeout salvo que
se haya aplicado una regla "set-timeout". Ver también "be_queue_timeout".

cur_server_timeout: integer Devuelve el tiempo de espera de servidor actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a be_server_timeout salvo que
se haya aplicado una regla "set-timeout". Ver también "be_server_timeout".

cur_tarpit_timeout: integer Devuelve el tiempo de espera tarpit actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a
fe_tarpit_timeout/be_tarpit_timeout salvo que se haya aplicado una regla "set-timeout". Ver
también "fe_tarpit_timeout" y "be_tarpit_timeout".

cur_tunnel_timeout: integer Devuelve el tiempo de espera de túnel actualmente aplicado en
milisegundos para el flujo. En el caso por defecto, esto será igual a be_tunnel_timeout salvo que
se haya aplicado una regla "set-timeout". Ver también "be_tunnel_timeout".

dst: ip Esta es la dirección IP de destino de la conexión en el lado del cliente, que es la
dirección a la que se conectó el cliente. Cualquier regla tcp/http puede alterar esta dirección.
Puede ser útil al ejecutarse en modo transparente. Es de tipo IP y funciona tanto en tablas IPv4
como IPv6. En las tablas IPv6, la dirección IPv4 se mapea a su equivalente IPv6, de acuerdo con el
RFC 4291. Cuando la conexión entrante pasó por una traducción o redirección de direcciones que
involucra seguimiento de conexiones, se informará la dirección de destino original anterior a la
redirección. En sistemas Linux, el origen y el destino rara vez pueden aparecer invertidos si el
sysctl nf_conntrack_tcp_loose está establecido, porque una respuesta tardía puede reabrir una
conexión cuyo tiempo de espera se agotó e intercambiar lo que se cree que es el origen y el
destino.

dst_conn: integer Devuelve un valor entero correspondiente al número de conexiones establecidas
actualmente en el mismo socket, incluyendo la que se está evaluando. Normalmente se usa con ACL,
pero igualmente puede usarse para pasar la información a los servidores en una cabecera HTTP o en
los registros. Puede usarse para devolver una página de disculpa antes del bloqueo definitivo, o
para usar un backend específico en el que drenar las solicitudes nuevas cuando el socket se
considera saturado. Esto ofrece la posibilidad de asignar límites diferentes a diferentes puertos
o direcciones de escucha. Ver también las obtenciones "fe_conn" y "be_conn".

dst_is_local: boolean Devuelve true si la dirección de destino de la conexión entrante es local al
sistema, o false si la dirección no existe en el sistema, lo que significa que fue interceptada en
modo transparente. Puede ser útil aplicar ciertas reglas por defecto al tráfico reenviado y otras
reglas al tráfico dirigido a la dirección real de la máquina. Por ejemplo, la página de
estadísticas podría entregarse solo en esta dirección, o el acceso SSH podría redirigirse
localmente. Ten en cuenta que la comprobación involucra algunas llamadas al sistema, así que es
mejor hacerla solo una vez por conexión.

dst_port: integer Devuelve un valor entero correspondiente al puerto TCP de destino de la conexión
en el lado del cliente, que es el puerto al que se conectó el cliente. Cualquier regla tcp/http
puede alterar esta dirección. Esto podría usarse al ejecutarse en modo transparente, cuando se
asignan puertos dinámicos a algunos clientes durante toda una sesión de aplicación, para fijar a
todos los usuarios a un mismo servidor, o para pasar la información del puerto de destino a un
servidor usando una cabecera HTTP.

fc.timer.handshake: integer Tiempo total para aceptar la conexión tcp y ejecutar los handshakes de
los protocolos de bajo nivel. Actualmente, estos protocolos son proxy-protocol y SSL. Esto es el
equivalente de %Th en el log-format. Se informa en milisegundos (ms). Para más información, ver la
[Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) "Eventos de temporización"

fc.timer.total: integer Duración total del flujo, entre el momento en que el proxy lo aceptó y el
momento en que ambos extremos se cerraron. Esto es el equivalente de %Tt en el log-format. Se
informa en milisegundos (ms). Para más información, ver la [Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) "Eventos de temporización"

fc_dst: ip Esta es la dirección IP de destino original de la conexión en el lado del cliente. Solo
las reglas "tcp-request connection" pueden alterar esta dirección. Ver "dst" para más detalles.

fc_dst_is_local: boolean Devuelve true si la dirección de destino original de la conexión entrante
es local al sistema, o false si la dirección no existe en el sistema. Ver "dst_is_local" para más
detalles.

fc_dst_port: integer Devuelve un valor entero correspondiente al puerto TCP de destino original de
la conexión en el lado del cliente. Solo las reglas "tcp-request connection" pueden alterar esta
dirección. Ver "dst-port" para más detalles.

fc_err: integer Devuelve el ID del error que podría haber ocurrido en la conexión actual.
Cualquier valor estrictamente positivo de esta obtención indica que la conexión no tuvo éxito y
daría lugar a que se emita un registro de error (como se describe en la [sección 8.2.5](/es/haproxy/configuration-logging/#section-8-2-5)). Ver la obtención "fc_err_str" para una lista
completa de los códigos de error y sus mensajes de error correspondientes.

fc_err_name: string Devuelve el nombre interno del error que describe qué problema ocurrió en la
conexión del frontend, que resulta en un fallo de conexión. Esta cadena está formada por una sola
palabra y está vacía cuando no hay error presente. Corresponde a la columna «nombre» de la tabla
presentada en la palabra clave "fc_err_str".

fc_err_str: string Devuelve un mensaje de error que describe qué problema ocurrió en la conexión
actual, que resulta en un fallo de conexión. Esta cadena corresponde a la parte "message" del
formato del registro de errores (ver la [sección 8.2.5](/es/haproxy/configuration-logging/#section-8-2-5)). Ver más abajo una lista completa de los códigos de error y sus
mensajes de error correspondientes:

```text
  +----+------------------+-------------------------------------------------------------------------+
  | ID | nombre           | mensaje                                                                 |
  +----+------------------+-------------------------------------------------------------------------+
  | 0  | -                | "Success"                                                               |
  | 1  | CONF_FDLIM       | "Reached configured maxconn value"                                      |
  | 2  | PROC_FDLIM       | "Too many sockets on the process"                                       |
  | 3  | SYS_FDLIM        | "Too many sockets on the system"                                        |
  | 4  | SYS_MEMLIM       | "Out of system buffers"                                                 |
  | 5  | NOPROTO          | "Protocol or address family not supported"                              |
  | 6  | SOCK_ERR         | "General socket error"                                                  |
  | 7  | PORT_RANGE       | "Source port range exhausted"                                           |
  | 8  | CANT_BIND        | "Can't bind to source address"                                          |
  | 9  | FREE_PORTS       | "Out of local source ports on the system"                               |
  | 10 | ADDR_INUSE       | "Local source address already in use"                                   |
  | 11 | PRX_EMPTY        | "Connection closed while waiting for PROXY protocol header"             |
  | 12 | PRX_ABORT        | "Connection error while waiting for PROXY protocol header"              |
  | 13 | PRX_TIMEOUT      | "Timeout while waiting for PROXY protocol header"                       |
  | 14 | PRX_TRUNCATED    | "Truncated PROXY protocol header received"                              |
  | 15 | PRX_NOT_HDR      | "Received something which does not look like a PROXY protocol header"   |
  | 16 | PRX_BAD_HDR      | "Received an invalid PROXY protocol header"                             |
  | 17 | PRX_BAD_PROTO    | "Received an unhandled protocol in the PROXY protocol header"           |
  | 18 | CIP_EMPTY        | "Connection closed while waiting for NetScaler Client IP header"        |
  | 19 | CIP_ABORT        | "Connection error while waiting for NetScaler Client IP header"         |
  | 20 | CIP_TIMEOUT      | "Timeout while waiting for a NetScaler Client IP header"                |
  | 21 | CIP_TRUNCATED    | "Truncated NetScaler Client IP header received"                         |
  | 22 | CIP_BAD_MAGIC    | "Received an invalid NetScaler Client IP magic number"                  |
  | 23 | CIP_BAD_PROTO    | "Received an unhandled protocol in the NetScaler Client IP header"      |
  | 24 | SSL_EMPTY        | "Connection closed during SSL handshake"                                |
  | 25 | SSL_ABORT        | "Connection error during SSL handshake"                                 |
  | 26 | SSL_TIMEOUT      | "Timeout during SSL handshake"                                          |
  | 27 | SSL_TOO_MANY     | "Too many SSL connections"                                              |
  | 28 | SSL_NO_MEM       | "Out of memory when initializing an SSL connection"                     |
  | 29 | SSL_RENEG        | "Rejected a client-initiated SSL renegotiation attempt"                 |
  | 30 | SSL_CA_FAIL      | "SSL client CA chain cannot be verified"                                |
  | 31 | SSL_CRT_FAIL     | "SSL client certificate not trusted"                                    |
  | 32 | SSL_MISMATCH     | "Server presented an SSL certificate different from the configured one" |
  | 33 | SSL_MISMATCH_SNI | "Server presented an SSL certificate different from the expected one"   |
  | 34 | SSL_HANDSHAKE    | "SSL handshake failure"                                                 |
  | 35 | SSL_HANDSHAKE_HB | "SSL handshake failure after heartbeat"                                 |
  | 36 | SSL_KILLED_HB    | "Stopped a TLSv1 heartbeat attack (CVE-2014-0160)"                      |
  | 37 | SSL_NO_TARGET    | "Attempt to use SSL on an unknown target (internal error)"              |
  | 38 | SSL_EARLY_FAILED | "Server refused early data"                                             |
  | 39 | SOCKS4_SEND      | "SOCKS4 Proxy write error during handshake"                             |
  | 40 | SOCKS4_RECV      | "SOCKS4 Proxy read error during handshake"                              |
  | 41 | SOCKS4_DENY      | "SOCKS4 Proxy deny the request"                                         |
  | 42 | SOCKS4_ABORT     | "SOCKS4 Proxy handshake aborted by server"                              |
  | 43 | SSL_FATAL        | "SSL fatal error"                                                       |
  | 44 | REVERSE          | "Reverse connect failure"                                               |
  | 45 | POLLERR          | "Poller reported POLLERR"                                               |
  | 46 | EREFUSED         | "ECONNREFUSED returned by OS"                                           |
  | 47 | ERESET           | "ECONNRESET returned by OS"                                             |
  | 48 | EUNREACH         | "ENETUNREACH returned by OS"                                            |
  | 49 | ENOMEM           | "ENOMEM returned by OS"                                                 |
  | 50 | EBADF            | "EBADF returned by OS"                                                  |
  | 51 | EFAULT           | "EFAULT returned by OS"                                                 |
  | 52 | EINVAL           | "EINVAL returned by OS"                                                 |
  | 53 | ENCONN           | "ENCONN returned by OS"                                                 |
  | 54 | ENSOCK           | "ENSOCK returned by OS"                                                 |
  | 55 | ENOBUFS          | "ENOBUFS returned by OS"                                                |
  | 56 | EPIPE            | "EPIPE returned by OS"                                                  |
  +----+------------------+-------------------------------------------------------------------------+
```

fc_fackets: integer Devuelve el contador fack medido por el kernel para la conexión del cliente.
Si la conexión con el servidor no está establecida, si la conexión no es TCP o si el sistema
operativo no soporta TCP_INFO, por ejemplo los kernels Linux anteriores a 2.4, la obtención de la
muestra falla.

fc_glitches: integer Devuelve el número de glitches de protocolo contados en la conexión del
frontend. Estos generalmente cubren violaciones de protocolo así como pequeñas anomalías que
generalmente indican un cliente defectuoso o con mal comportamiento que puede causar problemas en
la infraestructura, como un exceso de errores en los registros, o muchas conexiones abortadas
temprano, induciendo renegociaciones TLS frecuentes. También pueden estar causados por
solicitudes demasiado grandes que no caben en un único búfer, lo que explica los errores HTTP 400.
Idealmente, este número debería permanecer en cero, aunque es posible que algunos navegadores que
juegan con los límites del protocolo lo activen de vez en cuando. Estos valores normalmente no
deberían considerarse alarmantes (especialmente los pequeños), aunque un salto repentino puede
indicar una anomalía en algún lugar. Valores grandes (es decir, de cientos a miles por conexión, o
tantos como las solicitudes) pueden indicar un cliente construido a propósito que intenta tomar la
huella del protocolo o atacar la pila de protocolo. No todos los multiplexores de protocolo miden
esta métrica, y la única forma de obtener más detalles sobre los eventos es activar trazas para
capturar todos los intercambios.

fc_http_major: integer Informa de la codificación de la versión principal HTTP de la conexión
frontal, que puede ser 1 para HTTP/0.9 a HTTP/1.1 o 2 para HTTP/2. Ten en cuenta que esto se basa
en la codificación on-wire y no en la versión presente en la cabecera de la solicitud.

fc_lost: integer Si la conexión no es TCP ni QUIC, la obtención de la muestra falla. Para QUIC,
devuelve el número de paquetes QUIC perdidos por la conexión del cliente. Para TCP, devuelve el
contador de paquetes perdidos medido por el kernel para la conexión del cliente. Si la conexión con
el servidor no está establecida, o si el sistema operativo no soporta TCP_INFO, por ejemplo los
kernels Linux anteriores a 2.4, la obtención de la muestra falla.

fc_nb_streams: integer Devuelve el número de flujos abiertos en la conexión del frontend.

fc_pp_authority: string Devuelve el primer TLV de autoridad enviado por el cliente en la cabecera
del protocolo PROXY, si existe.

<a id="entry-7-3-3-fc-pp-tlv-string"></a>

**`fc_pp_tlv(<id>): string`**

```haproxy
fc_pp_tlv(<id>): string
```

Devuelve el valor del TLV para el ID de TLV dado. El ID debe ser un valor numérico entre 0 y 255 o
uno de los siguientes nombres simbólicos soportados que corresponden a los sufijos de constantes
TLV de la especificación PPv2: "ALPN": PP2_TYPE_ALPN, "AUTHORITY": PP2_TYPE_AUTHORITY, "CRC32":
PP2_TYPE_CRC32C, "NETNS": PP2_TYPE_NETNS, "NOOP: PP2_TYPE_NOOP", "SSL": PP2_TYPE_SSL,
"SSL_CIPHER": PP2_SUBTYPE_SSL_CIPHER, "SSL_CN": PP2_SUBTYPE_SSL_CN, "SSL_KEY_ALG":
PP2_SUBTYPE_SSL_KEY_ALG, "SSL_SIG_ALG": PP2_SUBTYPE_SSL_SIG_ALG, "SSL_VERSION":
PP2_SUBTYPE_SSL_VERSION, "UNIQUE_ID": PP2_TYPE_UNIQUE_ID.

El valor recibido debe ser menor o igual que 1024 bytes. Esto se hace para prevenir posibles
ataques DoS. Los valores menores o iguales que 256 bytes podrán agruparse en memoria. Por ello,
intenta restringir la longitud de los valores enviados a 256 bytes para un rendimiento óptimo.

Ten en cuenta que, a diferencia de fc_pp_authority y fc_pp_unique_id, fc_pp_tlv es capaz de iterar
sobre todas las apariciones de un TLV solicitado en caso de que haya IDs de TLV duplicados. El
orden de iteración coincide con la posición en la cabecera del protocolo PROXY. Sin embargo,
depender de los duplicados debería evitarse en su mayoría, ya que los TLV normalmente se asumen
únicos. En general, encontrar IDs de TLV duplicados indica un error en el lado emisor de la
cabecera del protocolo PROXY.

fc_pp_unique_id: string Devuelve el primer TLV de ID único enviado por el cliente en la cabecera
del protocolo PROXY, si existe.

fc_rcvd_proxy: boolean Devuelve true si el cliente inició la conexión con una cabecera de
protocolo PROXY.

fc_reordering: integer Si la conexión no es TCP ni QUIC, la obtención de la muestra falla. Para
QUIC, devuelve el número de paquetes QUIC reordenados para la conexión del cliente. Para TCP,
devuelve el contador de reordenación medido por el kernel para la conexión del cliente. Si la
conexión con el servidor no está establecida, o si el sistema operativo no soporta TCP_INFO, por
ejemplo los kernels Linux anteriores a 2.4, la obtención de la muestra falla.

fc_retrans: integer Devuelve el contador de retransmisiones medido por el kernel para la conexión
del cliente. Si la conexión con el servidor no está establecida, si la conexión no es TCP o si el
sistema operativo no soporta TCP_INFO, por ejemplo los kernels Linux anteriores a 2.4, la
obtención de la muestra falla.

<a id="entry-7-3-3-fc-rtt-integer"></a>

**`fc_rtt(<unit>): integer`**

```haproxy
fc_rtt(<unit>): integer
```

Si la conexión no es TCP ni QUIC, la obtención de la muestra falla. Para QUIC, devuelve el
Smoothed Round Trip Time para la conexión del cliente. Para TCP, devuelve el Round Trip Time (RTT)
medido por el kernel para la conexión del cliente. `<unit>` es opcional; por defecto la unidad es
milisegundos. `<unit>` puede establecerse a "ms" para milisegundos o "us" para microsegundos. Si
la conexión con el servidor no está establecida, o si el sistema operativo no soporta TCP_INFO,
por ejemplo los kernels Linux anteriores a 2.4, la obtención de la muestra falla.

<a id="entry-7-3-3-fc-rttvar-integer"></a>

**`fc_rttvar(<unit>): integer`**

```haproxy
fc_rttvar(<unit>): integer
```

Si la conexión no es TCP ni QUIC, la obtención de la muestra falla. Para QUIC, devuelve la
varianza del Smoothed Round Trip Time para la conexión del cliente. Para TCP, devuelve la varianza
del Round Trip Time (RTT) medida por el kernel para la conexión del cliente. `<unit>` es opcional;
por defecto la unidad es milisegundos. `<unit>` puede establecerse a "ms" para milisegundos o "us"
para microsegundos. Si la conexión con el servidor no está establecida, o si el sistema operativo
no soporta TCP_INFO, por ejemplo los kernels Linux anteriores a 2.4, la obtención de la muestra
falla.

fc_sacked: integer Devuelve el contador sacked medido por el kernel para la conexión del cliente.
Si la conexión con el servidor no está establecida, si la conexión no es TCP o si el sistema
operativo no soporta TCP_INFO, por ejemplo los kernels Linux anteriores a 2.4, la obtención de la
muestra falla.

fc_saved_syn: binary Devuelve una copia del paquete SYN guardado que fue preservado por el sistema
durante el establecimiento de la conexión entrante. Esto requiere que la opción "tcp-ss" estuviera
presente en la línea "bind", y un kernel Linux 4.3 como mínimo. Cuando "tcp-ss" está establecido a
1, solo están presentes las cabeceras IP y TCP. Cuando "tcp-ss" está establecido a 2, la cabecera
Ethernet también está presente antes de la cabecera IP y puede usarse, por ejemplo, para controlar
o registrar la dirección MAC de origen o las VLAN. Ten en cuenta que no hay garantía de que se
guarde un SYN. Por ejemplo, si se usan SYN cookies, el paquete SYN no se preserva y la conexión se
establece en el paquete ACK correspondiente. Además, el sistema no garantiza preservar la copia
más allá de la primera lectura. Como tal, es muy recomendable copiarla en una variable de ámbito
"sess" desde una regla "tcp-request connection" y usar únicamente esa variable para manipulaciones
posteriores. Merece la pena señalar que en la interfaz loopback el sistema construye una cabecera
ethernet dummy de 14 bytes donde tanto la dirección de origen como la de destino son cero, y solo
el protocolo está establecido. Es conveniente convertir tales muestras a hexadecimal usando el
conversor "hex" durante la depuración. Ejemplo (campos separados manualmente y comentados más
abajo):

```shell
frontend test
    mode http
    bind :::4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain \
                 lf-string "%[var(sess.syn),hex]\n"

$ curl '0:4445'
000000000000 000000000000 0800 \  # MAC_DST MAC_SRC PROTO=IPv4
4500003C0A65400040063255       \  # IPv4 header, proto=6 (TCP)
7F000001 7F000001              \  # IP_SRC=127.0.0.1 IP_DST=127.0.0.1
E1F2 115D 01AF4E3E 00000000    \  # TCP_SPORT=57842 TCP_DPORT=4445, SEQ
A0 02 FFD7 FE300000            \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65495
0204FFD70402080A01C2A71A0000000001030307 # MSS=65495, TS, SACK, WSCALE 7

$ curl '[::1]:4445'
000000000000 000000000000 86DD   \ # MAC_DST MAC_SRC PROTO=IPv6
6008018F00280640                 \ # IPv6 header, proto=6 (TCP)
00000000000000000000000000000001 \ # SRC=::1
00000000000000000000000000000001 \ # DST=::1
9758 115D B5511F5D 00000000      \ # TCP_SPORT=38744 TCP_DPORT=4445, SEQ
A0 02 FFC4 00300000              \  # OPT_LEN=20 TCP_FLAGS=SYN WIN=65476
0204FFC40402080A9C231D680000000001030307 # MSS=65476, TS, SACK, WSCALE 7
```

El conversor "bytes()" ayuda a extraer campos específicos del paquete. El be2dec() también permite
leer fragmentos y emitirlos en forma de entero. Para una extracción más precisa, consulta los
conversores "eth.XXX".

Ejemplo con entrada IPv4:

```shell
frontend test
    mode http
    bind :4445 tcp-ss 2
    tcp-request connection set-var(sess.syn) fc_saved_syn
    http-request return status 200 content-type text/plain lf-string \
                 "mac_dst=%[var(sess.syn),eth.dst,hex] \
                  mac_src=%[var(sess.syn),eth.src,hex] \
                  proto=%[var(sess.syn),eth.proto,bytes(6),be2hex(,2)] \
                  ipv4h=%[var(sess.syn),eth.data,bytes(0,12),hex] \
                  ipv4_src=%[var(sess.syn),eth.data,ip.src] \
                  ipv4_dst=%[var(sess.syn),eth.data,ip.dst] \
                  tcp_spt=%[var(sess.syn),eth.data,ip.data,tcp.src] \
                  tcp_dpt=%[var(sess.syn),eth.data,ip.data,tcp.dst] \
                  tcp_win=%[var(sess.syn),eth.data,ip.data,tcp.win] \
                  tcp_opt=%[var(sess.syn),eth.data,ip.data,bytes(20),hex]\n"

$ curl '0:4445'
mac_dst=000000000000 mac_src=000000000000 proto=0800 \
ipv4h=4500003CC9B7400040067302 ipv4_src=127.0.0.1 ipv4_dst=127.0.0.1 \
tcp_spt=43970 tcp_dpt=4445 tcp_win=65495 \
tcp_opt=0204FFD70402080A01DC0D410000000001030307
```

Ver también la acción "set-var" y los conversores "be2dec", "bytes", "hex", "eth.XXX", "ip.XXX" y
"tcp.XXX".

fc_settings_streams_limit: integer Devuelve el número máximo de flujos permitidos en la conexión
del frontend. Para conexiones TCP y HTTP/1.1, siempre es 1. Para otros protocolos, depende de los
ajustes negociados con el cliente.

fc_src: ip Esta es la dirección IP de origen original de la conexión en el lado del cliente. Solo
las reglas "tcp-request connection" pueden alterar esta dirección. Ver "src" para más detalles.

fc_src_is_local: boolean Devuelve true si la dirección de origen de la conexión entrante es local
al sistema, o false si la dirección no existe en el sistema. Ver "src_is_local" para más detalles.

fc_src_port: integer Devuelve un valor entero correspondiente al puerto TCP de origen de la
conexión en el lado del cliente. Solo las reglas "tcp-request connection" pueden alterar esta
dirección. Ver "src-port" para más detalles.

fc_unacked: integer Devuelve el contador unacked medido por el kernel para la conexión del cliente.
Si la conexión con el servidor no está establecida, si la conexión no es TCP o si el sistema
operativo no soporta TCP_INFO, por ejemplo los kernels Linux anteriores a 2.4, la obtención de la
muestra falla.

fe_client_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
de cliente del frontend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout".

fe_defbe: string Devuelve una cadena que contiene el nombre del backend por defecto del frontend.
Puede usarse en frontends para comprobar qué backend manejará las solicitudes por defecto.

fe_id: integer Devuelve un entero que contiene el id del frontend actual. Puede usarse en backends
para comprobar desde qué frontend fue llamado, o para fijar a todos los usuarios que llegan vía un
mismo frontend al mismo servidor.

fe_name: string Devuelve una cadena que contiene el nombre del frontend actual. Puede usarse en
backends para comprobar desde qué frontend fue llamado, o para fijar a todos los usuarios que
llegan vía un mismo frontend al mismo servidor.

fe_tarpit_timeout: integer Devuelve el valor de configuración en milisegundos del tiempo de espera
tarpit del frontend actual. Este tiempo de espera puede sobrescribirse con una regla
"set-timeout".

req.bytes_in: integer Devuelve el número de bytes recibidos del cliente. El valor corresponde a lo
que fue recibido por HAProxy, incluyendo algunas cabeceras y cierta sobrecarga de codificación
interna. La compresión de solicitudes no afecta al valor informado aquí.

req.bytes_out: integer Devuelve el número de bytes enviados al servidor. El valor corresponde a lo
que fue enviado por HAProxy, incluyendo algunas cabeceras y cierta sobrecarga de codificación
interna. La compresión de solicitudes afecta al valor informado aquí.

res.bytes_in: integer Devuelve el número de bytes recibidos del servidor. El valor corresponde a
lo que fue recibido por HAProxy, incluyendo algunas cabeceras y cierta sobrecarga de codificación
interna. La compresión de respuestas no afecta al valor informado aquí.

res.bytes_out: integer Devuelve el número de bytes enviados al cliente. El valor corresponde a lo
que fue enviado por HAProxy, incluyendo algunas cabeceras y cierta sobrecarga de codificación
interna. La compresión de respuestas afecta al valor informado aquí.

res.timer.data: integer Este es el tiempo total de transferencia de la carga útil de la respuesta
hasta el último byte enviado al cliente. En HTTP comienza tras la última cabecera de respuesta
(tras Tr). Esto es el equivalente de %Td en el log-format y se informa en milisegundos (ms). Para
más información, ver la [Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) "Eventos de
temporización"

<a id="entry-7-3-3-sc-bytes-in-rate-integer"></a>

**`sc_bytes_in_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_in_rate(<ctr>[,<table>]): integer
sc0_bytes_in_rate([<table>]): integer
sc1_bytes_in_rate([<table>]): integer
sc2_bytes_in_rate([<table>]): integer
```

Devuelve la tasa media de bytes de cliente a servidor de los contadores rastreados actualmente,
medida en cantidad de bytes durante el periodo configurado en la tabla. Ver también
"table_bytes_in_rate".

<a id="entry-7-3-3-sc-bytes-out-rate-integer"></a>

**`sc_bytes_out_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_bytes_out_rate(<ctr>[,<table>]): integer
sc0_bytes_out_rate([<table>]): integer
sc1_bytes_out_rate([<table>]): integer
sc2_bytes_out_rate([<table>]): integer
```

Devuelve la tasa media de bytes de servidor a cliente de los contadores rastreados actualmente,
medida en cantidad de bytes durante el periodo configurado en la tabla. Ver también
"table_bytes_out_rate".

<a id="entry-7-3-3-sc-clr-gpc-integer"></a>

**`sc_clr_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc(<idx>,<ctr>[,<table>]): integer
```

Borra el Contador de Propósito General en el índice `<idx>` del array asociado al contador
rastreado designado de ID `<ctr>` de la tabla de persistencia del proxy actual o de la tabla de
persistencia designada `<table>`, y devuelve su valor anterior. `<idx>` es un entero entre 0 y 99
y `<ctr>` un entero entre 0 y 2. Antes de la primera invocación, el valor almacenado es cero, por
lo que la primera invocación siempre devolverá cero. Esta obtención se aplica solo al tipo de datos
del array 'gpc' (y no a los tipos de datos obsoletos 'gpc0' ni 'gpc1').

<a id="entry-7-3-3-sc-clr-gpc0-integer"></a>

**`sc_clr_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc0(<ctr>[,<table>]): integer
sc0_clr_gpc0([<table>]): integer
sc1_clr_gpc0([<table>]): integer
sc2_clr_gpc0([<table>]): integer
```

Borra el primer Contador de Propósito General asociado a los contadores rastreados actualmente, y
devuelve su valor anterior. Antes de la primera invocación, el valor almacenado es cero, por lo que
la primera invocación siempre devolverá cero. Esto se usa típicamente como una segunda ACL en una
expresión para marcar una conexión cuando se verificó una primera ACL:

Ejemplo:

```shell
# block if 5 consecutive requests continue to come faster than 10 sess
# per second, and reset the counter as soon as the traffic slows down.
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 5
acl save  sc0_clr_gpc0 ge 0
tcp-request connection accept if !abuse save
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-clr-gpc1-integer"></a>

**`sc_clr_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_clr_gpc1(<ctr>[,<table>]): integer
sc0_clr_gpc1([<table>]): integer
sc1_clr_gpc1([<table>]): integer
sc2_clr_gpc1([<table>]): integer
```

Borra el segundo Contador de Propósito General asociado a los contadores actualmente rastreados y
devuelve su valor anterior. Antes de la primera invocación, el valor almacenado es cero, por lo que
la primera invocación siempre devolverá cero. Esto se usa habitualmente como una segunda ACL en una
expresión para marcar una conexión cuando se verificó una primera ACL.

<a id="entry-7-3-3-sc-conn-cnt-integer"></a>

**`sc_conn_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cnt(<ctr>[,<table>]): integer
sc0_conn_cnt([<table>]): integer
sc1_conn_cnt([<table>]): integer
sc2_conn_cnt([<table>]): integer
```

Devuelve el número acumulado de conexiones entrantes de los contadores actualmente rastreados. Ver
también "table_conn_cnt".

<a id="entry-7-3-3-sc-conn-cur-integer"></a>

**`sc_conn_cur(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_cur(<ctr>[,<table>]): integer
sc0_conn_cur([<table>]): integer
sc1_conn_cur([<table>]): integer
sc2_conn_cur([<table>]): integer
```

Devuelve la cantidad actual de conexiones concurrentes que rastrean los mismos contadores
rastreados. Este número se incrementa automáticamente cuando comienza el rastreo y se decrementa
cuando este se detiene. Ver también "table_conn_cur".

<a id="entry-7-3-3-sc-conn-rate-integer"></a>

**`sc_conn_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_conn_rate(<ctr>[,<table>]): integer
sc0_conn_rate([<table>]): integer
sc1_conn_rate([<table>]): integer
sc2_conn_rate([<table>]): integer
```

Devuelve la tasa media de conexiones de los contadores actualmente rastreados, medida como la
cantidad de conexiones durante el periodo configurado en la tabla. Ver también "table_conn_rate".

<a id="entry-7-3-3-sc-get-gpc-integer"></a>

**`sc_get_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc(<idx>,<ctr>[,<table>]): integer
```

Devuelve el valor del Contador de Propósito General en el índice `<idx>` del array GPC y asociado
al contador actualmente rastreado de ID `<ctr>`, de la stick-table del proxy actual o de la
stick-table designada `<table>`. `<idx>` es un entero entre 0 y 99 y `<ctr>` un entero entre 0 y 2.
Si no hay ningún gpc almacenado en este índice, se devuelve cero. Esta obtención se aplica solo al
data_type del array 'gpc' (y no a los data_type heredados 'gpc0' ni 'gpc1'). Ver también
"table_gpc" y "sc_inc_gpc".

<a id="entry-7-3-3-sc-get-gpc0-integer"></a>

**`sc_get_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc0(<ctr>[,<table>]): integer
sc0_get_gpc0([<table>]): integer
sc1_get_gpc0([<table>]): integer
sc2_get_gpc0([<table>]): integer
```

Devuelve el valor del primer Contador de Propósito General asociado a los contadores actualmente
rastreados. Ver también "table_gpc0" y sc/sc0/sc1/sc2_inc_gpc0.

<a id="entry-7-3-3-sc-get-gpc1-integer"></a>

**`sc_get_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpc1(<ctr>[,<table>]): integer
sc0_get_gpc1([<table>]): integer
sc1_get_gpc1([<table>]): integer
sc2_get_gpc1([<table>]): integer
```

Devuelve el valor del segundo Contador de Propósito General asociado a los contadores actualmente
rastreados. Ver también "table_gpc1" y sc/sc0/sc1/sc2_inc_gpc1.

<a id="entry-7-3-3-sc-get-gpt-integer"></a>

**`sc_get_gpt(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt(<idx>,<ctr>[,<table>]): integer
```

Devuelve el valor de la primera Etiqueta de Propósito General en el índice `<idx>` del array
asociado al contador rastreado de ID `<ctr>`, de la stick-table del proxy actual o de la
stick-table designada `<table>`. `<idx>` es un entero entre 0 y 99 y `<ctr>` un entero entre 0 y
2. Si no hay ningún GPT almacenado en este índice, se devuelve cero. Esta obtención se aplica solo
al data_type del array 'gpt' (y no al tipo de datos heredado 'gpt0'). Ver también "table_gpt".

<a id="entry-7-3-3-sc-get-gpt0-integer"></a>

**`sc_get_gpt0(<ctr>[,<table>]): integer`**

```haproxy
sc_get_gpt0(<ctr>[,<table>]): integer
sc0_get_gpt0([<table>]): integer
sc1_get_gpt0([<table>]): integer
sc2_get_gpt0([<table>]): integer
```

Devuelve el valor de la primera Etiqueta de Propósito General asociada a los contadores
actualmente rastreados. Ver también "table_gpt0".

<a id="entry-7-3-3-sc-glitch-cnt-integer"></a>

**`sc_glitch_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_cnt(<ctr>[,<table>]): integer
sc0_glitch_cnt([<table>]): integer
sc1_glitch_cnt([<table>]): integer
sc2_glitch_cnt([<table>]): integer
```

Devuelve el número acumulado de glitches de conexión frontal que se observaron en conexiones
asociadas a los contadores actualmente rastreados. Normalmente estos provocan que se aborten
solicitudes o conexiones, por lo que el valor devuelto a menudo corresponderá a conexiones pasadas.
No hay un valor bueno ni malo, pero un cliente de mala calidad puede causar ocasionalmente algunos
glitches por conexión, mientras que un cliente muy defectuoso o malintencionado puede causar
rápidamente miles de eventos en una conexión. Ver también fc_glitches para el número que afecta a
la conexión actual, src_glitch_cnt para buscarlos por origen, y sc_glitch_rate para las medidas de
tasas de eventos.

<a id="entry-7-3-3-sc-glitch-rate-integer"></a>

**`sc_glitch_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_glitch_rate(<ctr>[,<table>]): integer
sc0_glitch_rate([<table>]): integer
sc1_glitch_rate([<table>]): integer
sc2_glitch_rate([<table>]): integer
```

Devuelve la tasa media a la que se observaron glitches de conexión frontal para los contadores
actualmente rastreados, medida como la cantidad de eventos durante el periodo configurado en la
tabla. Normalmente estos glitches provocan que se aborten solicitudes o conexiones, por lo que el
valor devuelto a menudo estará relacionado con conexiones pasadas. No hay un valor bueno ni malo,
pero un cliente de mala calidad puede causar ocasionalmente algunos glitches por conexión, por lo
que generalmente se espera una tasa baja. Sin embargo, un cliente muy defectuoso o malintencionado
puede causar rápidamente miles de eventos por conexión y mantener aquí una tasa alta. Ver también
"table_glitch_rate" y "sc_glitch_cnt".

<a id="entry-7-3-3-sc-gpc-rate-integer"></a>

**`sc_gpc_rate(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_gpc_rate(<idx>,<ctr>[,<table>]): integer
```

Devuelve la tasa media de incremento del Contador de Propósito General en el índice `<idx>` del
array asociado al contador rastreado de ID `<ctr>`, de la tabla del proxy actual o de la
stick-table designada `<table>`. Informa de la frecuencia con la que se incrementó el contador gpc
durante el periodo configurado. `<idx>` es un entero entre 0 y 99 y `<ctr>` un entero entre 0 y 2.
Ten en cuenta que el array de contadores 'gpc_rate' debe almacenarse en la stick-table para que se
devuelva un valor, ya que 'gpc' solo contiene el recuento de eventos. Esta obtención se aplica solo
al data_type del array 'gpc_rate' (y no a los data_type heredados 'gpc0_rate' ni 'gpc1_rate'). Ver
también "table_gpc_rate", "sc_get_gpc" y "sc_inc_gpc".

<a id="entry-7-3-3-sc-gpc0-rate-integer"></a>

**`sc_gpc0_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc0_rate(<ctr>[,<table>]): integer
sc0_gpc0_rate([<table>]): integer
sc1_gpc0_rate([<table>]): integer
sc2_gpc0_rate([<table>]): integer
```

Devuelve la tasa media de incremento del primer Contador de Propósito General asociado a los
contadores actualmente rastreados. Informa de la frecuencia con la que se incrementó el contador
gpc0 durante el periodo configurado. Ver también src_gpc0_rate, sc/sc0/sc1/sc2_get_gpc0 y
sc/sc0/sc1/sc2_inc_gpc0. Ten en cuenta que el contador "gpc0_rate" debe almacenarse en la
stick-table para que se devuelva un valor, ya que "gpc0" solo contiene el recuento de eventos.

<a id="entry-7-3-3-sc-gpc1-rate-integer"></a>

**`sc_gpc1_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_gpc1_rate(<ctr>[,<table>]): integer
sc0_gpc1_rate([<table>]): integer
sc1_gpc1_rate([<table>]): integer
sc2_gpc1_rate([<table>]): integer
```

Devuelve la tasa media de incremento del segundo Contador de Propósito General asociado a los
contadores actualmente rastreados. Informa de la frecuencia con la que se incrementó el contador
gpc1 durante el periodo configurado. Ver también src_gpc1_rate, sc/sc0/sc1/sc2_get_gpc1 y
sc/sc0/sc1/sc2_inc_gpc1. Ten en cuenta que el contador "gpc1_rate" debe almacenarse en la
stick-table para que se devuelva un valor, ya que "gpc1" solo contiene el recuento de eventos.

<a id="entry-7-3-3-sc-http-err-cnt-integer"></a>

**`sc_http_err_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_cnt(<ctr>[,<table>]): integer
sc0_http_err_cnt([<table>]): integer
sc1_http_err_cnt([<table>]): integer
sc2_http_err_cnt([<table>]): integer
```

Devuelve el número acumulado de errores HTTP de los contadores actualmente rastreados. Esto incluye
tanto los errores de solicitud como las respuestas de error 4xx. Ver también "table_http_err_cnt".

<a id="entry-7-3-3-sc-http-err-rate-integer"></a>

**`sc_http_err_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_err_rate(<ctr>[,<table>]): integer
sc0_http_err_rate([<table>]): integer
sc1_http_err_rate([<table>]): integer
sc2_http_err_rate([<table>]): integer
```

Devuelve la tasa media de errores HTTP de los contadores actualmente rastreados, medida como la
cantidad de errores durante el periodo configurado en la tabla. Esto incluye tanto los errores de
solicitud como las respuestas de error 4xx. Ver también src_http_err_rate.

<a id="entry-7-3-3-sc-http-fail-cnt-integer"></a>

**`sc_http_fail_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_cnt(<ctr>[,<table>]): integer
sc0_http_fail_cnt([<table>]): integer
sc1_http_fail_cnt([<table>]): integer
sc2_http_fail_cnt([<table>]): integer
```

Devuelve el número acumulado de fallos de respuesta HTTP de los contadores actualmente
rastreados. Esto incluye tanto los errores de respuesta como los códigos de estado 5xx distintos
de 501 y 505. Ver también "table_http_fail_cnt".

<a id="entry-7-3-3-sc-http-fail-rate-integer"></a>

**`sc_http_fail_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_fail_rate(<ctr>[,<table>]): integer
sc0_http_fail_rate([<table>]): integer
sc1_http_fail_rate([<table>]): integer
sc2_http_fail_rate([<table>]): integer
```

Devuelve la tasa media de fallos de respuesta HTTP de los contadores actualmente rastreados,
medida como la cantidad de fallos durante el periodo configurado en la tabla. Esto incluye tanto
los errores de respuesta como los códigos de estado 5xx distintos de 501 y 505. Ver también
"table_http_fail_rate".

<a id="entry-7-3-3-sc-http-req-cnt-integer"></a>

**`sc_http_req_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_cnt(<ctr>[,<table>]): integer
sc0_http_req_cnt([<table>]): integer
sc1_http_req_cnt([<table>]): integer
sc2_http_req_cnt([<table>]): integer
```

Devuelve el número acumulado de solicitudes HTTP de los contadores actualmente rastreados. Esto
incluye cada solicitud iniciada, válida o no. Ver también src_http_req_cnt.

<a id="entry-7-3-3-sc-http-req-rate-integer"></a>

**`sc_http_req_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_http_req_rate(<ctr>[,<table>]): integer
sc0_http_req_rate([<table>]): integer
sc1_http_req_rate([<table>]): integer
sc2_http_req_rate([<table>]): integer
```

Devuelve la tasa media de solicitudes HTTP de los contadores actualmente rastreados, medida como
la cantidad de solicitudes durante el periodo configurado en la tabla. Esto incluye cada solicitud
iniciada, válida o no. Ver también src_http_req_rate.

<a id="entry-7-3-3-sc-inc-gpc-integer"></a>

**`sc_inc_gpc(<idx>,<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc(<idx>,<ctr>[,<table>]): integer
```

Incrementa el Contador de Propósito General en el índice `<idx>` del array asociado al contador
rastreado designado de ID `<ctr>`, de la stick-table del proxy actual o de la stick-table
designada `<table>`, y devuelve su nuevo valor. `<idx>` es un entero entre 0 y 99 y `<ctr>` un
entero entre 0 y 2. Antes de la primera invocación, el valor almacenado es cero, por lo que la
primera invocación lo aumentará a 1 y devolverá 1. Esta obtención se aplica solo al data_type del
array 'gpc' (y no a los data_type heredados 'gpc0' ni 'gpc1').

<a id="entry-7-3-3-sc-inc-gpc0-integer"></a>

**`sc_inc_gpc0(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc0(<ctr>[,<table>]): integer
sc0_inc_gpc0([<table>]): integer
sc1_inc_gpc0([<table>]): integer
sc2_inc_gpc0([<table>]): integer
```

Incrementa el primer Contador de Propósito General asociado a los contadores actualmente
rastreados y devuelve su nuevo valor. Antes de la primera invocación, el valor almacenado es cero,
por lo que la primera invocación lo aumentará a 1 y devolverá 1. Esto se usa habitualmente como una
segunda ACL en una expresión para marcar una conexión cuando se verificó una primera ACL:

Ejemplo:

```text
acl abuse sc0_http_req_rate gt 10
acl kill  sc0_inc_gpc0 gt 0
tcp-request connection reject if abuse kill
```

<a id="entry-7-3-3-sc-inc-gpc1-integer"></a>

**`sc_inc_gpc1(<ctr>[,<table>]): integer`**

```haproxy
sc_inc_gpc1(<ctr>[,<table>]): integer
sc0_inc_gpc1([<table>]): integer
sc1_inc_gpc1([<table>]): integer
sc2_inc_gpc1([<table>]): integer
```

Incrementa el segundo Contador de Propósito General asociado a los contadores actualmente
rastreados y devuelve su nuevo valor. Antes de la primera invocación, el valor almacenado es cero,
por lo que la primera invocación lo aumentará a 1 y devolverá 1. Esto se usa habitualmente como una
segunda ACL en una expresión para marcar una conexión cuando se verificó una primera ACL.

<a id="entry-7-3-3-sc-kbytes-in-integer"></a>

**`sc_kbytes_in(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_in(<ctr>[,<table>]): integer
sc0_kbytes_in([<table>]): integer
sc1_kbytes_in([<table>]): integer
sc2_kbytes_in([<table>]): integer
```

Devuelve la cantidad total de datos de cliente a servidor de los contadores actualmente
rastreados, medida en kilobytes. La comprobación se realiza actualmente sobre enteros de 32 bits,
lo que limita los valores a 4 terabytes. Ver también "table_kbytes_in".

<a id="entry-7-3-3-sc-kbytes-out-integer"></a>

**`sc_kbytes_out(<ctr>[,<table>]): integer`**

```haproxy
sc_kbytes_out(<ctr>[,<table>]): integer
sc0_kbytes_out([<table>]): integer
sc1_kbytes_out([<table>]): integer
sc2_kbytes_out([<table>]): integer
```

Devuelve la cantidad total de datos de servidor a cliente de los contadores actualmente
rastreados, medida en kilobytes. La comprobación se realiza actualmente sobre enteros de 32 bits,
lo que limita los valores a 4 terabytes. Ver también "table_kbytes_out".

sc_key(`<ctr>`): any sc0_key: any sc1_key: any sc2_key: any Devuelve la clave utilizada para
coincidir con el contador actualmente rastreado.

<a id="entry-7-3-3-sc-sess-cnt-integer"></a>

**`sc_sess_cnt(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_cnt(<ctr>[,<table>]): integer
sc0_sess_cnt([<table>]): integer
sc1_sess_cnt([<table>]): integer
sc2_sess_cnt([<table>]): integer
```

Devuelve el número acumulado de conexiones entrantes que se transformaron en sesiones, lo que
significa que fueron aceptadas por una regla "tcp-request connection", de los contadores
actualmente rastreados. Un backend puede contabilizar más sesiones que conexiones, porque cada
conexión podría dar lugar a muchas sesiones de backend si se realiza algún HTTP keep-alive sobre la
conexión con el cliente. Ver también "table_sess_cnt".

<a id="entry-7-3-3-sc-sess-rate-integer"></a>

**`sc_sess_rate(<ctr>[,<table>]): integer`**

```haproxy
sc_sess_rate(<ctr>[,<table>]): integer
sc0_sess_rate([<table>]): integer
sc1_sess_rate([<table>]): integer
sc2_sess_rate([<table>]): integer
```

Devuelve la tasa media de sesiones de los contadores actualmente rastreados, medida como la
cantidad de sesiones durante el periodo configurado en la tabla. Una sesión es una conexión que
superó las primeras reglas "tcp-request connection". Un backend puede contabilizar más sesiones
que conexiones, porque cada conexión podría dar lugar a muchas sesiones de backend si se realiza
algún HTTP keep-alive sobre la conexión con el cliente. Ver también "table_sess_rate".

<a id="entry-7-3-3-sc-tracked-boolean"></a>

**`sc_tracked(<ctr>[,<table>]): boolean`**

```haproxy
sc_tracked(<ctr>[,<table>]): boolean
sc0_tracked([<table>]): boolean
sc1_tracked([<table>]): boolean
sc2_tracked([<table>]): boolean
```

Devuelve true si el contador de sesión designado está siendo rastreado actualmente por la sesión
actual. Esto puede ser útil al decidir si queremos o no establecer algunos valores en una cabecera
pasada al servidor.

<a id="entry-7-3-3-sc-trackers-integer"></a>

**`sc_trackers(<ctr>[,<table>]): integer`**

```haproxy
sc_trackers(<ctr>[,<table>]): integer
sc0_trackers([<table>]): integer
sc1_trackers([<table>]): integer
sc2_trackers([<table>]): integer
```

Devuelve la cantidad actual de conexiones concurrentes que rastrean los mismos contadores
rastreados. Este número se incrementa automáticamente cuando comienza el rastreo y se decrementa
cuando este se detiene. Se diferencia de sc0_conn_cur en que no depende de ninguna información
almacenada sino del recuento de referencias de la tabla (el valor "use" que devuelve "show table"
en la CLI). Esto puede ser a veces más adecuado para el rastreo en capa 7. Puede usarse para
indicar a un servidor cuántas conexiones concurrentes hay desde una dirección dada, por ejemplo.

so_id: integer Devuelve un entero que contiene el id del socket de escucha actual. Es útil en
frontends con muchas líneas "bind", o para fijar al mismo servidor a todos los usuarios que llegan
mediante un mismo socket.

so_name: string Devuelve una cadena que contiene el nombre del socket de escucha actual, tal como
se definió con name en una línea "bind". Puede servir para los mismos propósitos que so_id pero con
cadenas en lugar de enteros.

src: ip Esta es la dirección IP de origen del cliente de la sesión. Cualquier regla tcp/http puede
alterar esta dirección. Es de tipo IP y funciona tanto en tablas IPv4 como IPv6. En las tablas
IPv6, las direcciones IPv4 se mapean a su equivalente IPv6, de acuerdo con el RFC 4291. Ten en
cuenta que es la dirección de origen a nivel TCP la que se utiliza, y no la dirección de un cliente
detrás de un proxy. Sin embargo, si se usa la directiva bind "accept-proxy" o
"accept-netscaler-cip", puede ser la dirección de un cliente detrás de otro componente compatible
con el protocolo PROXY para todos los conjuntos de reglas excepto "tcp-request connection", que ve
la dirección real. Cuando la conexión entrante pasó por una traducción o redirección de direcciones
que implica rastreo de conexiones, se informará la dirección de destino original anterior a la
redirección. En sistemas Linux, el origen y el destino pueden rara vez aparecer invertidos si el
sysctl nf_conntrack_tcp_loose está establecido, porque una respuesta tardía puede reabrir una
conexión caducada e intercambiar lo que se considera el origen y el destino.

Ejemplo:

```shell
# add an HTTP header in requests with the originating address' country
http-request set-header X-Country %[src,map_ip(geoip.lst)]
```

<a id="entry-7-3-3-src-bytes-in-rate-integer"></a>

**`src_bytes_in_rate([<table>]): integer`**

```haproxy
src_bytes_in_rate([<table>]): integer
```

Igual que el conversor "table_bytes_in_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_bytes_in_rate([`<table>`])

<a id="entry-7-3-3-src-bytes-out-rate-integer"></a>

**`src_bytes_out_rate([<table>]): integer`**

```haproxy
src_bytes_out_rate([<table>]): integer
```

Igual que el conversor "table_bytes_out_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_bytes_out_rate([`<table>`])

<a id="entry-7-3-3-src-clr-gpc-integer"></a>

**`src_clr_gpc(<idx>[,<table>]): integer`**

```haproxy
src_clr_gpc(<idx>[,<table>]): integer
```

Igual que el conversor "table_clr_gpc" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_clr_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-clr-gpc0-integer"></a>

**`src_clr_gpc0([<table>]): integer`**

```haproxy
src_clr_gpc0([<table>]): integer
```

Igual que el conversor "table_clr_gpc0" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_clr_gpc0([`<table>`])

<a id="entry-7-3-3-src-clr-gpc1-integer"></a>

**`src_clr_gpc1([<table>]): integer`**

```haproxy
src_clr_gpc1([<table>]): integer
```

Igual que el conversor "table_clr_gpc1" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_clr_gpc1([`<table>`])

<a id="entry-7-3-3-src-conn-cnt-integer"></a>

**`src_conn_cnt([<table>]): integer`**

```haproxy
src_conn_cnt([<table>]): integer
```

Igual que el conversor "table_conn_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_conn_cnt([`<table>`])

<a id="entry-7-3-3-src-conn-cur-integer"></a>

**`src_conn_cur([<table>]): integer`**

```haproxy
src_conn_cur([<table>]): integer
```

Igual que el conversor "table_conn_cur" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_conn_cur([`<table>`])

<a id="entry-7-3-3-src-conn-rate-integer"></a>

**`src_conn_rate([<table>]): integer`**

```haproxy
src_conn_rate([<table>]): integer
```

Igual que el conversor "table_conn_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_conn_rate([`<table>`])

<a id="entry-7-3-3-src-get-gpc-integer"></a>

**`src_get_gpc(<idx>[,<table>]): integer`**

```haproxy
src_get_gpc(<idx>[,<table>]): integer
```

Igual que el conversor "table_gpc" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpc0-integer"></a>

**`src_get_gpc0([<table>]): integer`**

```haproxy
src_get_gpc0([<table>]): integer
```

Igual que el conversor "table_gpc0" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc0([`<table>`])

<a id="entry-7-3-3-src-get-gpc1-integer"></a>

**`src_get_gpc1([<table>]): integer`**

```haproxy
src_get_gpc1([<table>]): integer
```

Igual que el conversor "table_gpc1" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc1([`<table>`])

<a id="entry-7-3-3-src-get-gpt-integer"></a>

**`src_get_gpt(<idx>[,<table>]): integer`**

```haproxy
src_get_gpt(<idx>[,<table>]): integer
```

Igual que el conversor "table_gpt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpt(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-get-gpt0-integer"></a>

**`src_get_gpt0([<table>]): integer`**

```haproxy
src_get_gpt0([<table>]): integer
```

Igual que el conversor "table_gpt0" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpt0([`<table>`])

<a id="entry-7-3-3-src-glitch-cnt-integer"></a>

**`src_glitch_cnt([<table>]): integer`**

```haproxy
src_glitch_cnt([<table>]): integer
```

Igual que el conversor "table_glitch_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_glitch_cnt([`<table>`])

<a id="entry-7-3-3-src-glitch-rate-integer"></a>

**`src_glitch_rate([<table>]): integer`**

```haproxy
src_glitch_rate([<table>]): integer
```

Igual que el conversor "table_glitch_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_glitch_rate([`<table>`])

<a id="entry-7-3-3-src-gpc-rate-integer"></a>

**`src_gpc_rate(<idx>[,<table>]): integer`**

```haproxy
src_gpc_rate(<idx>[,<table>]): integer
```

Igual que el conversor "table_gpc_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc_rate(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-gpc0-rate-integer"></a>

**`src_gpc0_rate([<table>]): integer`**

```haproxy
src_gpc0_rate([<table>]): integer
```

Igual que el conversor "table_gpc0_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc0_rate([`<table>`])

<a id="entry-7-3-3-src-gpc1-rate-integer"></a>

**`src_gpc1_rate([<table>]): integer`**

```haproxy
src_gpc1_rate([<table>]): integer
```

Igual que el conversor "table_gpc1_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_gpc1_rate([`<table>`])

<a id="entry-7-3-3-src-http-err-cnt-integer"></a>

**`src_http_err_cnt([<table>]): integer`**

```haproxy
src_http_err_cnt([<table>]): integer
```

Igual que el conversor "table_http_err_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_err_cnt([`<table>`])

<a id="entry-7-3-3-src-http-err-rate-integer"></a>

**`src_http_err_rate([<table>]): integer`**

```haproxy
src_http_err_rate([<table>]): integer
```

Igual que el conversor "table_http_err_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_err_rate([`<table>`])

<a id="entry-7-3-3-src-http-fail-cnt-integer"></a>

**`src_http_fail_cnt([<table>]): integer`**

```haproxy
src_http_fail_cnt([<table>]): integer
```

Igual que el conversor "table_http_fail_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_fail_cnt([`<table>`])

<a id="entry-7-3-3-src-http-fail-rate-integer"></a>

**`src_http_fail_rate([<table>]): integer`**

```haproxy
src_http_fail_rate([<table>]): integer
```

Igual que el conversor "table_http_fail_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_fail_rate([`<table>`])

<a id="entry-7-3-3-src-http-req-cnt-integer"></a>

**`src_http_req_cnt([<table>]): integer`**

```haproxy
src_http_req_cnt([<table>]): integer
```

Igual que el conversor "table_http_req_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_req_cnt([`<table>`])

<a id="entry-7-3-3-src-http-req-rate-integer"></a>

**`src_http_req_rate([<table>]): integer`**

```haproxy
src_http_req_rate([<table>]): integer
```

Igual que el conversor "table_http_req_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_http_req_rate([`<table>`])

<a id="entry-7-3-3-src-inc-gpc-integer"></a>

**`src_inc_gpc(<idx>[,<table>]): integer`**

```haproxy
src_inc_gpc(<idx>[,<table>]): integer
```

Igual que el conversor "src_inc_gpc" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_inc_gpc(`<idx>`[,`<table>`])

<a id="entry-7-3-3-src-inc-gpc0-integer"></a>

**`src_inc_gpc0([<table>]): integer`**

```haproxy
src_inc_gpc0([<table>]): integer
```

Igual que el conversor "src_inc_gpc0" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_inc_gpc0([`<table>`])

<a id="entry-7-3-3-src-inc-gpc1-integer"></a>

**`src_inc_gpc1([<table>]): integer`**

```haproxy
src_inc_gpc1([<table>]): integer
```

Igual que el conversor "src_inc_gpc1" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_inc_gpc1([`<table>`])

src_is_local: boolean Devuelve true si la dirección de origen de la conexión entrante es local al
sistema, o false si la dirección no existe en el sistema, lo que significa que proviene de una
máquina remota. Ten en cuenta que las direcciones UNIX se consideran locales. Puede ser útil
aplicar ciertas restricciones de acceso basadas en el origen del cliente (p. ej. exigir
autenticación o https para máquinas remotas). Ten en cuenta que la comprobación implica algunas
llamadas al sistema, así que es mejor hacerla solo una vez por conexión.

<a id="entry-7-3-3-src-kbytes-in-integer"></a>

**`src_kbytes_in([<table>]): integer`**

```haproxy
src_kbytes_in([<table>]): integer
```

Igual que el conversor "table_kbytes_in" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_kbytes_in([`<table>`])

<a id="entry-7-3-3-src-kbytes-out-integer"></a>

**`src_kbytes_out([<table>]): integer`**

```haproxy
src_kbytes_out([<table>]): integer
```

Igual que el conversor "table_kbytes_out" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_kbytes_out([`<table>`])

src_port: integer Devuelve un valor entero correspondiente al puerto TCP de origen de la conexión
en el lado del cliente, que es el puerto desde el que se conectó el cliente. Cualquier regla
tcp/http puede alterar esta dirección. El uso de esta función es muy limitado, ya que los protocolos
modernos actualmente no se preocupan mucho por los puertos de origen.

<a id="entry-7-3-3-src-sess-cnt-integer"></a>

**`src_sess_cnt([<table>]): integer`**

```haproxy
src_sess_cnt([<table>]): integer
```

Igual que el conversor "table_sess_cnt" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_sess_cnt([`<table>`])

<a id="entry-7-3-3-src-sess-rate-integer"></a>

**`src_sess_rate([<table>]): integer`**

```haproxy
src_sess_rate([<table>]): integer
```

Igual que el conversor "table_sess_rate" con la clave establecida en la dirección de origen de la conexión entrante.

Equivalente a: src,table_sess_rate([`<table>`])

<a id="entry-7-3-3-src-updt-conn-cnt-integer"></a>

**`src_updt_conn_cnt([<table>]): integer`**

```haproxy
src_updt_conn_cnt([<table>]): integer
```

Crea o actualiza la entrada asociada a la dirección de origen de la conexión entrante en la
stick-table del proxy actual o en la stick-table designada. Esta tabla debe configurarse para
almacenar el tipo de datos "conn_cnt"; de lo contrario, la coincidencia se ignorará. El recuento
actual se incrementa en uno y el temporizador de expiración se renueva. Se devuelve el recuento
actualizado, por lo que esta coincidencia no puede devolver cero. Esto se usaba para rechazar a los
abusadores del servicio basándose en su dirección de origen. Nota: se recomienda usar en su lugar
las acciones más completas "track-sc\*" en reglas "tcp-request".

Ejemplo:

```shell
# This frontend limits incoming SSH connections to 3 per 10 second for
# each source address, and rejects excess connections until a 10 second
# silence is observed. At most 20 addresses are tracked.
listen ssh
    bind :22
    mode tcp
    maxconn 100
    stick-table type ip size 20 expire 10s store conn_cnt
    tcp-request content reject if { src_updt_conn_cnt gt 3 }
    server local 127.0.0.1:22
```

srv_id: integer Devuelve un entero que contiene el id del servidor al procesar la respuesta. Aunque
casi solo se usa con ACL, puede usarse para registro o depuración. También puede usarse en un
conjunto de reglas tcp-check o http-check.

srv_name: string Devuelve una cadena que contiene el nombre del servidor al procesar la respuesta.
Aunque casi solo se usa con ACL, puede usarse para registro o depuración. También puede usarse en
un conjunto de reglas tcp-check o http-check.

txn.conn_retries: integer Devuelve el número de reintentos de conexión experimentados por este flujo
al intentar conectarse al servidor. Este valor puede cambiar mientras la conexión no esté
completamente establecida. Para conexiones HTTP, el valor puede verse afectado por reintentos de
capa 7.

txn.redispatched: boolean Devuelve true si la conexión ha experimentado un redispatch al reintentar,
según la configuración de "option redispatch". Este valor puede cambiar mientras la conexión no
esté completamente establecida. Para conexiones HTTP, el valor puede verse afectado por reintentos
de capa 7.

### 7.3.4. Obtención de muestras en la capa 5 {#section-7-3-4}

La capa 5 normalmente describe solo la capa de sesión, que en HAProxy está más próxima a la sesión
una vez terminados todos los handshakes de conexión, pero cuando aún no hay disponible ningún
contenido. Los métodos de obtención descritos aquí pueden usarse tan pronto como en los conjuntos
de reglas "tcp-request content", salvo que requieran información futura. Estos incluyen
generalmente los resultados de las negociaciones SSL.

Resumen de los métodos de obtención de muestras de esta sección y sus tipos respectivos:

```text
  palabra clave                                    tipo de salida
-------------------------------------------------+-------------
51d.all(<prop>[,<prop>*])                          string
bs.aborted                                         boolean
bs.debug_str([<bitmap>])                           string
bs.id                                              integer
bs.rst_code                                        integer
fs.aborted                                         boolean
fs.debug_str([<bitmap>])                           string
fs.id                                              integer
fs.rst_code                                        integer
ssl_bc                                             boolean
ssl_bc_alg_keysize                                 integer
ssl_bc_alpn                                        string
ssl_bc_cipher                                      string
ssl_bc_client_early_traffic_secret                 string
ssl_bc_client_handshake_traffic_secret             string
ssl_bc_client_random                               binary
ssl_bc_client_traffic_secret_0                     string
ssl_bc_curve                                       string
ssl_bc_early_exporter_secret                       string
ssl_bc_err                                         integer
ssl_bc_err_str                                     string
ssl_bc_exporter_secret                             string
ssl_bc_is_resumed                                  boolean
ssl_bc_npn                                         string
ssl_bc_protocol                                    string
ssl_bc_server_handshake_traffic_secret             string
ssl_bc_server_random                               binary
ssl_bc_server_traffic_secret_0                     string
ssl_bc_session_id                                  binary
ssl_bc_session_key                                 binary
ssl_bc_sni                                         string
ssl_bc_unique_id                                   binary
ssl_bc_use_keysize                                 integer
ssl_c_ca_err                                       integer
ssl_c_ca_err_depth                                 integer
ssl_c_chain_der                                    binary
ssl_c_der                                          binary
ssl_c_err                                          integer
ssl_c_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_key_alg                                      string
ssl_c_notafter                                     string
ssl_c_notbefore                                    string
ssl_c_r_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_c_san                                          string
ssl_c_serial                                       binary
ssl_c_sha1                                         binary
ssl_c_sig_alg                                      string
ssl_c_used                                         boolean
ssl_c_verify                                       integer
ssl_c_version                                      integer
ssl_f_der                                          binary
ssl_f_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_key_alg                                      string
ssl_f_notafter                                     string
ssl_f_notbefore                                    string
ssl_f_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_f_serial                                       binary
ssl_f_sha1                                         binary
ssl_f_sig_alg                                      string
ssl_f_version                                      integer
ssl_fc                                             boolean
ssl_fc_alg_keysize                                 integer
ssl_fc_alpn                                        string
ssl_fc_cipher                                      string
ssl_fc_cipherlist_bin([<filter_option>])           binary
ssl_fc_cipherlist_hex([<filter_option>])           string
ssl_fc_cipherlist_str([<filter_option>])           string
ssl_fc_cipherlist_xxh                              integer
ssl_fc_client_early_traffic_secret                 string
ssl_fc_client_handshake_traffic_secret             string
ssl_fc_client_random                               binary
ssl_fc_client_traffic_secret_0                     string
ssl_fc_crtname                                     string
ssl_fc_curve                                       string
ssl_fc_early_exporter_secret                       string
ssl_fc_ecformats_bin                               binary
ssl_fc_eclist_bin([<filter_option>])               binary
ssl_fc_err                                         integer
ssl_fc_err_str                                     string
ssl_fc_exporter_secret                             string
ssl_fc_extlist_bin([<filter_option>])              binary
ssl_fc_has_crt                                     boolean
ssl_fc_has_early                                   boolean
ssl_fc_has_sni                                     boolean
ssl_fc_is_resumed                                  boolean
ssl_fc_npn                                         string
ssl_fc_protocol                                    string
ssl_fc_protocol_hello_id                           integer
ssl_fc_server_handshake_traffic_secret             string
ssl_fc_server_random                               binary
ssl_fc_server_traffic_secret_0                     string
ssl_fc_session_id                                  binary
ssl_fc_session_key                                 binary
ssl_fc_sigalgs_bin([<filter_option>])              binary
ssl_fc_sni                                         string
ssl_fc_supported_versions_bin([<filter_option>])   binary
ssl_fc_unique_id                                   binary
ssl_fc_use_keysize                                 integer
ssl_s_chain_der                                    binary
ssl_s_der                                          binary
ssl_s_i_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_key_alg                                      string
ssl_s_notafter                                     string
ssl_s_notbefore                                    string
ssl_s_s_dn([<entry>[,<occ>[,<format>]]])           string
ssl_s_serial                                       binary
ssl_s_sha1                                         binary
ssl_s_sig_alg                                      string
ssl_s_version                                      integer
txn.timer.user                                     integer
-------------------------------------------------+-------------
```

Lista detallada:

<a id="entry-7-3-4-51d-all-string"></a>

**`51d.all(<prop>[,<prop>*]): string`**

```haproxy
51d.all(<prop>[,<prop>*]): string
```

Devuelve los valores de las propiedades solicitadas como una cadena, donde los valores van separados
por el delimitador especificado con "51degrees-property-separator". El dispositivo se identifica
usando todas las cabeceras HTTP importantes de la solicitud. A la función se le pueden pasar hasta
cinco nombres de propiedades, y si no puede encontrarse un nombre de propiedad, se devuelve el
valor "NoData".

Ejemplo:

```shell
# Here the header "X-51D-DeviceTypeMobileTablet" is added to the request
# containing the three properties requested using all relevant headers from
# the request.
frontend http-in
  bind *:8081
  default_backend servers
  http-request set-header X-51D-DeviceTypeMobileTablet \
    %[51d.all(DeviceType,IsMobile,IsTablet)]
```

bs.aborted: boolean Devuelve true si se recibió un abort del servidor para el flujo actual. En caso
contrario se devuelve false.

<a id="entry-7-3-4-bs-debug-str-string"></a>

**`bs.debug_str([<bitmap>]): string`**

```haproxy
bs.debug_str([<bitmap>]): string
```

Esta función está pensada para que la usen los desarrolladores durante ciertas sesiones complejas
de resolución de problemas. Extrae algunos estados internos de las capas inferiores del flujo y la
conexión del backend, y los organiza como una cadena, generalmente en forma de una serie de
"nombre=valor" delimitados con espacios. El argumento opcional `<bitmap>` indica de qué capa(s)
extraer información, y es un OR aritmético (o una suma) de los siguientes valores: - capa de
socket: 16 - capa de conexión: 8 - capa de transporte (p. ej. SSL): 4 - conexión del mux: 2 - flujo
del mux: 1

Estos valores pueden cambiar entre versiones. El valor por defecto de cero es especial y habilita
todas las capas. No dependas del resultado de esta función para la supervisión a largo plazo en producción. Está pensada para evolucionar incluso dentro de una rama estable, a medida que surgen
necesidades de mayor detalle. Un caso de uso típico es concatenar esta información al final de un
log-format, junto con fs.debug_str(). Ejemplo:

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

bs.id: integer Devuelve el ID de flujo del multiplexor en el lado del servidor. Es responsabilidad
del multiplexor devolver la información apropiada.

bs.rst_code: integer Devuelve el código de reinicio recibido del servidor para el flujo actual. Se
devuelve el código de la trama H2 RST_STREAM o de la trama QUIC STOP_SENDING recibida del servidor.
La obtención de muestra falla si no se recibió ningún abort o si el flujo del servidor no es un
flujo H2/QUIC.

fs.aborted: boolean Devuelve true si se recibió un abort del cliente para el flujo actual. En caso
contrario se devuelve false.

<a id="entry-7-3-4-fs-debug-str-string"></a>

**`fs.debug_str([<bitmap>]): string`**

```haproxy
fs.debug_str([<bitmap>]): string
```

Esta función está pensada para que la usen los desarrolladores durante ciertas sesiones complejas
de resolución de problemas. Extrae algunos estados internos de las capas inferiores del flujo y la
conexión del frontend, y los organiza como una cadena, generalmente en forma de una serie de
"nombre=valor" delimitados con espacios. El argumento opcional `<bitmap>` indica de qué capa(s)
extraer información, y es un OR aritmético (o una suma) de los siguientes valores: - capa de
socket: 16 - capa de conexión: 8 - capa de transporte (p. ej. SSL): 4 - conexión del mux: 2 - flujo
del mux: 1

Estos valores pueden cambiar entre versiones. El valor por defecto de cero es especial y habilita
todas las capas. No dependas del resultado de esta función para la supervisión a largo plazo en producción. Está pensada para evolucionar incluso dentro de una rama estable, a medida que surgen
necesidades de mayor detalle. Un caso de uso típico es concatenar esta información al final de un
log-format, junto con bs.debug_str(). Ejemplo:

```text
log-format "$HAPROXY_HTTP_LOG_FMT fs=<%[fs.debug_str]> bs=<%[bs.debug_str]>"
```

fs.id: integer Devuelve el ID de flujo del multiplexor en el lado del cliente. Es responsabilidad
del multiplexor devolver la información apropiada. Por ejemplo, en TCP puro siempre se devuelve 0
porque no hay flujo.

fs.rst_code: integer Devuelve el código de reinicio recibido del cliente para el flujo actual. Se
devuelve el código de la trama H2 RST_STREAM o de la trama QUIC STOP_SENDING recibida del cliente.
La obtención de muestra falla si no se recibió ningún abort o si el flujo del cliente no es un
flujo H2/QUIC.

ssl_bc: boolean Devuelve true cuando la conexión trasera se realizó mediante una capa de transporte
SSL/TLS y se descifra localmente. Esto significa que la conexión saliente se realizó a un servidor
con la opción "ssl". Puede usarse en un conjunto de reglas tcp-check o http-check.

ssl_bc_alg_keysize: integer Devuelve el tamaño de clave del cifrado simétrico soportado en bits
cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS. Puede usarse en un
conjunto de reglas tcp-check o http-check.

ssl_bc_alpn: string Esto extrae el campo Application Layer Protocol Negotiation de una conexión
saliente realizada mediante una capa de transporte TLS. El resultado es una cadena que contiene el
nombre del protocolo negociado con el servidor. La biblioteca SSL debe haberse compilado con
soporte para extensiones TLS habilitado (comprueba haproxy -vv). Ten en cuenta que la extensión TLS
ALPN no se anuncia salvo que la palabra clave "alpn" de la línea "server" especifique una lista de
protocolos. Además, nada obliga al servidor a escoger un protocolo de esta lista; puede solicitarse
cualquier otro. La extensión TLS ALPN está pensada para reemplazar a la extensión TLS NPN. Ver
también "ssl_bc_npn". Puede usarse en un conjunto de reglas tcp-check o http-check.

ssl_bc_cipher: string Devuelve el nombre del cifrado usado cuando la conexión saliente se realizó
sobre una capa de transporte SSL/TLS. Puede usarse en un conjunto de reglas tcp-check o
http-check.

ssl_bc_client_early_traffic_secret: string Devuelve el CLIENT_EARLY_TRAFFIC_SECRET como cadena
hexadecimal para la conexión trasera cuando la conexión saliente se realizó sobre una capa de
transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_client_handshake_traffic_secret: string Devuelve el CLIENT_HANDSHAKE_TRAFFIC_SECRET como
cadena hexadecimal para la conexión trasera cuando la conexión saliente se realizó sobre una capa
de transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_client_random: binary Devuelve el client random de la conexión trasera cuando la conexión
entrante se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar tráfico enviado
usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL. Puede usarse en un conjunto
de reglas tcp-check o http-check.

ssl_bc_client_traffic_secret_0: string Devuelve el CLIENT_TRAFFIC_SECRET_0 como cadena hexadecimal
para la conexión trasera cuando la conexión saliente se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_curve: string Devuelve el nombre de la curva usada en el acuerdo de claves cuando la
conexión saliente se realizó sobre una capa de transporte SSL/TLS. Esto requiere OpenSSL \>= 3.0.0
o AWS-LC \>= 1.57.0.

ssl_bc_early_exporter_secret: string Devuelve el EARLY_EXPORTER_SECRET como cadena hexadecimal
para la conexión trasera cuando la conexión saliente se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_err: integer Cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS,
devuelve el ID del último error de la primera pila de errores generada en el lado del backend.
Puede generar errores de handshake así como otros errores de lectura o escritura ocurridos durante
la vida de la conexión. Para obtener una descripción textual de este código de error, puedes usar
la obtención de muestra "ssl_bc_err_str" o el comando "openssl errstr" (que toma como parámetro un
código de error en representación hexadecimal). Consulta la documentación de tu biblioteca SSL
para encontrar la lista exhaustiva de códigos de error.

ssl_bc_err_str: string Cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS,
devuelve una representación en cadena del último error de la primera pila de errores que se generó
en la conexión desde la perspectiva del backend. Ver también "ssl_fc_err".

ssl_bc_exporter_secret: string Devuelve el EXPORTER_SECRET como cadena hexadecimal para la
conexión trasera cuando la conexión saliente se realizó sobre una capa de transporte TLS 1.3.
Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog de
OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_is_resumed: boolean Devuelve true cuando la conexión trasera se realizó sobre una capa de
transporte SSL/TLS y la sesión SSL recién creada se reanudó usando una sesión en caché o un ticket
TLS. Puede usarse en un conjunto de reglas tcp-check o http-check.

ssl_bc_npn: string Esto extrae el campo Next Protocol Negotiation de una conexión saliente
realizada mediante una capa de transporte TLS. El resultado es una cadena que contiene el nombre
del protocolo negociado con el servidor. La biblioteca SSL debe haberse compilado con soporte para
extensiones TLS habilitado (comprueba haproxy -vv). Ten en cuenta que la extensión TLS NPN no se
anuncia salvo que la palabra clave "npn" de la línea "server" especifique una lista de protocolos.
Además, nada obliga al servidor a escoger un protocolo de esta lista; puede usarse cualquier otro.
Ten en cuenta que la extensión TLS NPN fue reemplazada por ALPN. Puede usarse en un conjunto de
reglas tcp-check o http-check.

ssl_bc_protocol: string Devuelve el nombre del protocolo usado cuando la conexión saliente se
realizó sobre una capa de transporte SSL/TLS. Puede usarse en un conjunto de reglas tcp-check o
http-check.

ssl_bc_server_handshake_traffic_secret: string Devuelve el SERVER_HANDSHAKE_TRAFFIC_SECRET como
cadena hexadecimal para la conexión trasera cuando la conexión saliente se realizó sobre una capa
de transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_server_random: binary Devuelve el server random de la conexión trasera cuando la conexión
entrante se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar tráfico enviado
usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL. Puede usarse en un conjunto
de reglas tcp-check o http-check.

ssl_bc_server_traffic_secret_0: string Devuelve el SERVER_TRAFFIC_SECRET_0 como cadena hexadecimal
para la conexión trasera cuando la conexión saliente se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_bc_session_id: binary Devuelve el ID SSL de la conexión trasera cuando la conexión saliente se
realizó sobre una capa de transporte SSL/TLS. Es útil registrarlo si queremos saber si la sesión se
reutilizó o no. Puede usarse en un conjunto de reglas tcp-check o http-check.

ssl_bc_session_key: binary Devuelve la clave maestra de sesión SSL de la conexión trasera cuando la
conexión saliente se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar tráfico
enviado usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL. Puede usarse en un
conjunto de reglas tcp-check o http-check.

ssl_bc_sni: string Esto recupera el campo de la extensión TLS Server Name Indication (SNI) que se
usó en la conexión al servidor. El resultado (cuando está presente) típicamente es una cadena que
coincide con el nombre de host HTTPS (253 caracteres o menos). El principal caso de uso es con
fines de registro y depuración (p. ej. averiguar qué SNI se usó cuando se estableció la conexión
para compararlo con lo que el servidor ha visto).

ssl_bc_unique_id: binary Cuando la conexión saliente se realizó sobre una capa de transporte
SSL/TLS, devuelve el ID único de TLS tal como se define en el RFC5929 [sección 3](https://www.rfc-editor.org/rfc/rfc5929#section-3). El id único puede codificarse en base64 usando el
conversor: "ssl_bc_unique_id,base64". Puede usarse en un conjunto de reglas tcp-check o
http-check.

ssl_bc_use_keysize: integer Devuelve el tamaño de clave del cifrado simétrico usado en bits cuando
la conexión saliente se realizó sobre una capa de transporte SSL/TLS. Puede usarse en un conjunto
de reglas tcp-check o http-check.

ssl_c_ca_err: integer Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS,
devuelve el ID del primer error detectado durante la verificación del certificado del cliente a
profundidad \> 0, o 0 si no se encontró ningún error durante este proceso de verificación. Consulta
la documentación de tu biblioteca SSL para encontrar la lista exhaustiva de códigos de error.

ssl_c_ca_err_depth: integer Cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS, devuelve la profundidad en la cadena de CA del primer error detectado durante la
verificación del certificado del cliente. Si no se encuentra ningún error, se devuelve 0.

ssl_c_chain_der: binary Devuelve la cadena de certificados en formato DER presentada por el cliente
cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una
ACL, el valor o valores con los que comparar pueden pasarse en forma hexadecimal. El resultado
puede analizarse con cualquier biblioteca que acepte datos ASN.1 DER. Actualmente no soporta
sesiones reanudadas.

ssl_c_der: binary Devuelve el certificado en formato DER presentado por el cliente cuando la
conexión entrante se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL, el
valor o valores con los que comparar pueden pasarse en forma hexadecimal.

ssl_c_err: integer Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS,
devuelve el ID del primer error detectado durante la verificación a profundidad 0, o 0 si no se
encontró ningún error durante este proceso de verificación. Consulta la documentación de tu
biblioteca SSL para encontrar la lista exhaustiva de códigos de error.

<a id="entry-7-3-4-ssl-c-i-dn-string"></a>

**`ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del emisor del certificado presentado por el cliente cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_c_i_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_c_i_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_c_i_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_c_key_alg: string Devuelve el nombre del algoritmo usado para generar la clave del certificado
presentado por el cliente cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS.

ssl_c_notafter: string Devuelve la fecha de fin presentada por el cliente como cadena con formato
YYMMDDhhmmss[Z] cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_c_notbefore: string Devuelve la fecha de inicio presentada por el cliente como cadena con
formato YYMMDDhhmmss[Z] cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS.

<a id="entry-7-3-4-ssl-c-r-dn-string"></a>

**`ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_r_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS y se valida
correctamente con el ca-file configurado, devuelve el nombre completo (distinguished name) de la CA
raíz del certificado presentado por el cliente cuando no se especifica `<entry>`, o el valor de la
primera entrada dada encontrada desde el principio del DN. Si se especifica un número de ocurrencia
positivo/negativo como segundo argumento opcional, devuelve el valor de la n-ésima entrada dada
desde el principio/final del DN. Por ejemplo, "ssl_c_r_dn(OU,2)" recupera la segunda unidad organizativa, y
"ssl_c_r_dn(CN)" recupera el nombre común. El parámetro `<format>` permite recibir el DN apto para
el consumo por diferentes protocolos. Actualmente se soporta rfc2253 para LDAP v3. Si deseas
modificar solo el formato, puedes especificar una cadena vacía y cero para los dos primeros
parámetros. Ejemplo: ssl_c_r_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando
no se especifica `<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de
otros datos, se considera mal formado y no se devuelve ningún dato.

<a id="entry-7-3-4-ssl-c-s-dn-string"></a>

**`ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_c_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del sujeto del certificado presentado por el cliente cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_c_s_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_c_s_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_c_s_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_c_san: string Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS y se
proporcionó un certificado de cliente. Devuelve una cadena de campos Subject Alt Name separados por
comas contenidos en el certificado proporcionado.

Esto puede usarse para inspeccionar el certificado del cliente.

Ejemplo:

```text
acl is_valid_client_cert ssl_c_used && ! ssl_c_verify
http-request set-header X-SSL-Client-SAN %[ssl_c_san] if is_valid_client_cert
```

dará como resultado:

```text
X-SSL-Client-SAN: IP Address:127.0.0.1, IP Address:127.0.0.2, IP Address:127.0.0.3, URI:http://docs.haproxy.org/2.7/, DNS:ca.tests.haproxy.com

```

ssl_c_serial: binary Devuelve el número de serie del certificado presentado por el cliente cuando
la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL,
el valor o valores con los que comparar pueden pasarse en forma hexadecimal.

ssl_c_sha1: binary Devuelve la huella digital SHA-1 del certificado presentado por el cliente cuando
la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Esto puede usarse para fijar
un cliente a un servidor, o para pasar esta información a un servidor. Ten en cuenta que la salida
es binaria, por lo que si deseas pasar esa firma al servidor, necesitas codificarla en hexadecimal
o base64, como en el ejemplo siguiente:

Ejemplo:

```text
http-request set-header X-SSL-Client-SHA1 %[ssl_c_sha1,hex]
```

ssl_c_sig_alg: string Devuelve el nombre del algoritmo usado para firmar el certificado presentado
por el cliente cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_c_used: boolean Devuelve true si la sesión SSL actual usa un certificado de cliente incluso si
la conexión actual usa reanudación de sesión SSL. Ver también "ssl_fc_has_crt".

ssl_c_verify: integer Devuelve el ID de error del resultado de la verificación cuando la conexión
entrante se realizó sobre una capa de transporte SSL/TLS, o cero si no se encuentra ningún error.
Consulta la documentación de tu biblioteca SSL para una lista exhaustiva de códigos de error.

ssl_c_version: integer Devuelve la versión del certificado presentado por el cliente cuando la
conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_f_der: binary Devuelve el certificado en formato DER presentado por el frontend cuando la
conexión entrante se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL, el
valor o valores con los que comparar pueden pasarse en forma hexadecimal.

<a id="entry-7-3-4-ssl-f-i-dn-string"></a>

**`ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del emisor del certificado presentado por el frontend cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_f_i_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_f_i_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_f_i_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_f_key_alg: string Devuelve el nombre del algoritmo usado para generar la clave del certificado
presentado por el frontend cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS.

ssl_f_notafter: string Devuelve la fecha de fin presentada por el frontend como cadena con formato
YYMMDDhhmmss[Z] cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_f_notbefore: string Devuelve la fecha de inicio presentada por el frontend como cadena con
formato YYMMDDhhmmss[Z] cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS.

<a id="entry-7-3-4-ssl-f-s-dn-string"></a>

**`ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_f_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del sujeto del certificado presentado por el frontend cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_f_s_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_f_s_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_f_s_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_f_serial: binary Devuelve el número de serie del certificado presentado por el frontend cuando
la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL,
el valor o valores con los que comparar pueden pasarse en forma hexadecimal.

ssl_f_sha1: binary Devuelve la huella digital SHA-1 del certificado presentado por el frontend
cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Esto puede usarse para
saber qué certificado se eligió usando SNI.

ssl_f_sig_alg: string Devuelve el nombre del algoritmo usado para firmar el certificado presentado
por el frontend cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_f_version: integer Devuelve la versión del certificado presentado por el frontend cuando la
conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_fc: boolean Devuelve true cuando la conexión frontal se realizó mediante una capa de transporte
SSL/TLS y se descifra localmente. Esto significa que coincidió con un socket declarado con una
línea "bind" que tiene la opción "ssl".

Ejemplo:

```shell
# This passes "X-Proto: https" to servers when client connects over SSL
listen http-https
    bind :80
    bind :443 ssl crt /etc/haproxy.pem
    http-request add-header X-Proto https if { ssl_fc }
```

ssl_fc_alg_keysize: integer Devuelve el tamaño de clave del cifrado simétrico soportado en bits
cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_fc_alpn: string Esto extrae el campo Application Layer Protocol Negotiation de una conexión
entrante realizada mediante una capa de transporte TLS y descifrada localmente por HAProxy. El
resultado es una cadena que contiene el nombre del protocolo anunciado por el cliente. La
biblioteca SSL debe haberse compilado con soporte para extensiones TLS habilitado (comprueba
haproxy -vv). Ten en cuenta que la extensión TLS ALPN no se anuncia salvo que la palabra clave
"alpn" de la línea "bind" especifique una lista de protocolos. Además, nada obliga al cliente a
escoger un protocolo de esta lista; puede solicitarse cualquier otro. La extensión TLS ALPN está
pensada para reemplazar a la extensión TLS NPN. Ver también "ssl_fc_npn".

ssl_fc_cipher: string Devuelve el nombre del cifrado usado cuando la conexión entrante se realizó
sobre una capa de transporte SSL/TLS.

<a id="entry-7-3-4-ssl-fc-cipherlist-bin-binary"></a>

**`ssl_fc_cipherlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_cipherlist_bin([<filter_option>]): binary
```

Devuelve la forma binaria de la lista de cifrados del client hello. La longitud máxima del valor
devuelto está limitada por el tamaño del búfer de captura compartido controlado por el ajuste
"tune.ssl.capture-buffer-size". Establecer `<filter_option>` permite filtrar los datos devueltos.
Valores aceptados:

```text
0: devuelve la lista completa de cifrados (por defecto)
1: excluye los valores GREASE (RFC8701) de la salida
```

Ejemplo:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-cipherlist-hex-string"></a>

**`ssl_fc_cipherlist_hex([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_hex([<filter_option>]): string
```

Devuelve la forma binaria de la lista de cifrados del client hello codificada como hexadecimal. La
longitud máxima del valor devuelto está limitada por el tamaño del búfer de captura compartido
controlado por el ajuste "tune.ssl.capture-buffer-size". Establecer `<filter_option>` permite
filtrar los datos devueltos. Valores aceptados:

```text
0: devuelve la lista completa de cifrados (por defecto)
1: excluye los valores GREASE (RFC8701) de la salida
```

<a id="entry-7-3-4-ssl-fc-cipherlist-str-string"></a>

**`ssl_fc_cipherlist_str([<filter_option>]): string`**

```haproxy
ssl_fc_cipherlist_str([<filter_option>]): string
```

Devuelve la forma de texto decodificada de la lista de cifrados del client hello. La longitud
máxima del valor devuelto está limitada por el tamaño del búfer de captura compartido controlado
por el ajuste "tune.ssl.capture-buffer-size". Establecer `<filter_option>` permite filtrar los
datos devueltos. Valores aceptados:

```text
0: devuelve la lista completa de cifrados (por defecto)
1: excluye los valores GREASE (RFC8701) de la salida
```

Ten en cuenta que esta obtención de muestra solo está disponible con OpenSSL \>= 1.0.2. Si la
función no está habilitada, esta obtención de muestra devuelve el hash como
"ssl_fc_cipherlist_xxh".

ssl_fc_cipherlist_xxh: integer Devuelve un xxh64 de la lista de cifrados. Este hash solo puede
devolverse si el valor "tune.ssl.capture-buffer-size" está establecido mayor que 0; sin embargo, el
hash tiene en cuenta todos los datos de la lista de cifrados.

ssl_fc_client_early_traffic_secret: string Devuelve el CLIENT_EARLY_TRAFFIC_SECRET como cadena
hexadecimal para la conexión frontal cuando la conexión entrante se realizó sobre una capa de
transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_client_handshake_traffic_secret: string Devuelve el CLIENT_HANDSHAKE_TRAFFIC_SECRET como
cadena hexadecimal para la conexión frontal cuando la conexión entrante se realizó sobre una capa
de transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_client_random: binary Devuelve el client random de la conexión frontal cuando la conexión
entrante se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar tráfico enviado
usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL.

ssl_fc_client_traffic_secret_0: string Devuelve el CLIENT_TRAFFIC_SECRET_0 como cadena hexadecimal
para la conexión frontal cuando la conexión entrante se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_crtname: string Devuelve el nombre del certificado que se seleccionó para la conexión
SSL/TLS entrante. Este es el nombre tal como aparece en "show ssl cert": puede ser el nombre de
archivo con su ruta relativa o absoluta, o un alias, dependiendo de cómo se declaró el certificado
en la configuración.

Ejemplo:

```text
crt-store example
    load crt "example.com.pem"

frontend www
    bind *:443 ssl crt "@example/example.com.pem"
    acl match_certificate ssl_fc_crtname -m beg -i "@example/"
    http-request set-header X-Cert-Name %[ssl_fc_crtname] if match_certificate
```

ssl_fc_curve: string Devuelve el nombre de la curva usada en el acuerdo de claves cuando la
conexión entrante se realizó sobre una capa de transporte SSL/TLS. Esto requiere OpenSSL \>= 3.0.0.

ssl_fc_early_rcvd: boolean Devuelve true si se vieron early data sobre esa conexión, sin importar
que el handshake se haya completado desde entonces. No tiene un caso de uso práctico para el
procesamiento de tráfico; sin embargo, es prácticamente la única forma de "ver" que un cliente usó
0-RTT para enviar early data, y a veces es útil al depurar, ya que las únicas alternativas son
capturas de tráfico de red o registrar los flags de la conexión frontal y compararlos en el código.
También puede ser útil para obtener estadísticas sobre las capacidades de los clientes. Ver también
"ssl_fc_has_early".

ssl_fc_early_exporter_secret: string Devuelve el EARLY_EXPORTER_SECRET como cadena hexadecimal
para la conexión frontal cuando la conexión entrante se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_ecformats_bin: binary Devuelve la forma binaria de los formatos de punto de curva elíptica
soportados del client hello. La longitud máxima del valor devuelto está limitada por el tamaño del
búfer de captura compartido controlado por el ajuste "tune.ssl.capture-buffer-size".

Ejemplo:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

<a id="entry-7-3-4-ssl-fc-eclist-bin-binary"></a>

**`ssl_fc_eclist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_eclist_bin([<filter_option>]): binary
```

Devuelve la forma binaria de las curvas elípticas soportadas del client hello. La longitud máxima
del valor devuelto está limitada por el tamaño del búfer de captura compartido controlado por el
ajuste "tune.ssl.capture-buffer-size". Establecer `<filter_option>` permite filtrar los datos
devueltos. Valores aceptados:

```text
0: devuelve la lista completa de curvas elípticas soportadas (por defecto)
1: excluye los valores GREASE (RFC8701) de la salida
```

Ejemplo:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_err: integer Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS,
devuelve el ID del último error de la primera pila de errores generada en el lado frontal, o 0 si
no se encontró ningún error. Puede usarse para identificar errores relacionados con el handshake
que no sean de verificación (como una no coincidencia de cifrado), así como otros errores de
lectura o escritura ocurridos durante la vida de la conexión. Cualquier error que ocurra durante el
proceso de verificación del certificado del cliente no se generará a través de esta obtención sino
mediante las obtenciones existentes "ssl_c_err", "ssl_c_ca_err" y "ssl_c_ca_err_depth". Para
obtener una descripción textual de este código de error, puedes usar la obtención de muestra
"ssl_fc_err_str" o el comando "openssl errstr" (que toma como parámetro un código de error en
representación hexadecimal). Consulta la documentación de tu biblioteca SSL para encontrar la
lista exhaustiva de códigos de error.

ssl_fc_err_str: string Cuando la conexión entrante se realizó sobre una capa de transporte SSL/TLS,
devuelve una representación en cadena del último error de la primera pila de errores que se generó
en el lado frontal. Cualquier error que ocurra durante el proceso de verificación del certificado
del cliente no se generará a través de esta obtención. Ver también "ssl_fc_err".

ssl_fc_exporter_secret: string Devuelve el EXPORTER_SECRET como cadena hexadecimal para la
conexión frontal cuando la conexión entrante se realizó sobre una capa de transporte TLS 1.3.
Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog de
OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

<a id="entry-7-3-4-ssl-fc-extlist-bin-binary"></a>

**`ssl_fc_extlist_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_extlist_bin([<filter_option>]): binary
```

Devuelve la forma binaria de la lista de extensiones del client hello. La longitud máxima del valor
devuelto está limitada por el tamaño del búfer de captura compartido controlado por el ajuste
"tune.ssl.capture-buffer-size". Establecer `<filter_option>` permite filtrar los datos devueltos.
Valores aceptados:

```text
0: devuelve la lista completa de extensiones (por defecto)
1: excluye los valores GREASE (RFC8701) de la salida
```

Ejemplo:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_has_crt: boolean Devuelve true si hay un certificado de cliente presente en una conexión
entrante sobre una capa de transporte SSL/TLS. Útil si la declaración 'verify' está establecida a
'optional'. Nota: en la reanudación de sesión SSL con Session ID o ticket TLS, el certificado de
cliente no está presente en la conexión actual pero puede recuperarse de la caché o del ticket.
Por ello prefiere "ssl_c_used" si deseas comprobar si la sesión SSL actual usa un certificado de
cliente.

ssl_fc_has_early: boolean Devuelve true si se enviaron early data y el handshake aún no se ha completado. Como esto tiene implicaciones de seguridad, es útil poder rechazarlas, o esperar a que el handshake se complete (mediante la acción "wait-for-handshake"). Ver también
"ssl_fc_early_rcvd".

ssl_fc_has_sni: boolean Esto comprueba la presencia de una extensión TLS Server Name Indication
(SNI) en una conexión entrante realizada sobre una capa de transporte SSL/TLS. Devuelve true
cuando la conexión entrante presenta un campo SNI de TLS. Esto requiere que la biblioteca SSL esté
compilada con soporte para extensiones TLS habilitado (comprueba haproxy -vv).

ssl_fc_is_resumed: boolean Devuelve true si la sesión SSL/TLS se ha reanudado mediante el uso de
caché de sesión SSL o tickets TLS en una conexión entrante sobre una capa de transporte SSL/TLS.

ssl_fc_npn: string Esto extrae el campo Next Protocol Negotiation de una conexión entrante
realizada mediante una capa de transporte TLS y descifrada localmente por HAProxy. El resultado es
una cadena que contiene el nombre del protocolo anunciado por el cliente. La biblioteca SSL debe
haberse compilado con soporte para extensiones TLS habilitado (comprueba haproxy -vv). Ten en
cuenta que la extensión TLS NPN no se anuncia salvo que la palabra clave "npn" de la línea "bind"
especifique una lista de protocolos. Además, nada obliga al cliente a escoger un protocolo de esta
lista; puede solicitarse cualquier otro. Ten en cuenta que la extensión TLS NPN fue reemplazada
por ALPN.

ssl_fc_protocol: string Devuelve el nombre del protocolo usado cuando la conexión entrante se
realizó sobre una capa de transporte SSL/TLS.

ssl_fc_protocol_hello_id: integer La versión del protocolo TLS con la que el cliente desea
comunicarse durante la sesión, según lo indicado en el mensaje client hello. Este valor solo puede
devolverse si el valor "tune.ssl.capture-buffer-size" está establecido mayor que 0.

Ejemplo:

```text
http-request set-header X-SSL-JA3 %[ssl_fc_protocol_hello_id],\
    %[ssl_fc_cipherlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_extlist_bin(1),be2dec(-,2)],\
    %[ssl_fc_eclist_bin(1),be2dec(-,2)],\
    %[ssl_fc_ecformats_bin,be2dec(-,1)]
acl is_malware req.fhdr(x-ssl-ja3),digest(md5),hex \
    -f /path/to/file/with/malware-ja3.lst
http-request set-header X-Malware True if is_malware
http-request set-header X-Malware False if !is_malware
```

ssl_fc_server_handshake_traffic_secret: string Devuelve el SERVER_HANDSHAKE_TRAFFIC_SECRET como
cadena hexadecimal para la conexión frontal cuando la conexión entrante se realizó sobre una capa
de transporte TLS 1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la
retrollamada de keylog de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe
activarse con "tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_server_random: binary Devuelve el server random de la conexión frontal cuando la conexión
entrante se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar tráfico enviado
usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL.

ssl_fc_server_traffic_secret_0: string Devuelve el SERVER_TRAFFIC_SECRET_0 como cadena hexadecimal
para la conexión frontal cuando la conexión entrante se realizó sobre una capa de transporte TLS
1.3. Requiere OpenSSL \>= 1.1.1. Esta es una de las claves volcadas por la retrollamada de keylog
de OpenSSL para generar el SSLKEYLOGFILE. El registro de claves SSL debe activarse con
"tune.ssl.keylog on" en la sección global. Ver también "tune.ssl.keylog"

ssl_fc_session_id: binary Devuelve el ID SSL de la conexión frontal cuando la conexión entrante se
realizó sobre una capa de transporte SSL/TLS. Es útil para fijar un cliente dado a un servidor. Es
importante tener en cuenta que algunos navegadores refrescan su ID de sesión cada pocos minutos.

ssl_fc_session_key: binary Devuelve la clave maestra de sesión SSL de la conexión frontal cuando
la conexión entrante se realizó sobre una capa de transporte SSL/TLS. Es útil para descifrar
tráfico enviado usando cifrados efímeros. Esto requiere OpenSSL \>= 1.1.0 o BoringSSL.

<a id="entry-7-3-4-ssl-fc-sigalgs-bin-binary"></a>

**`ssl_fc_sigalgs_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_sigalgs_bin([<filter_option>]): binary
```

Devuelve el contenido de la extensión TLS signatures_algorithms (13) presentada durante el Client
Hello. Proporciona una lista binaria de algoritmos de 2 bytes definidos en el RFC de TLS:
<https://datatracker.ietf.org/doc/html/rfc8446#section-4.2.3>.

Este valor solo puede devolverse si el valor "tune.ssl.capture-buffer-size" está establecido mayor
que 0. Establecer `<filter_option>` permite filtrar los datos devueltos. Valores aceptados: 0:
devuelve la lista completa de cifrados (por defecto) 1: excluye los valores GREASE (RFC8701) de la
salida

ssl_fc_sni: string Esto extrae el campo de la extensión TLS Server Name Indication (SNI) de una
conexión entrante realizada mediante una capa de transporte SSL/TLS y descifrada localmente por
HAProxy. El resultado (cuando está presente) típicamente es una cadena que coincide con el nombre
de host HTTPS (253 caracteres o menos). La biblioteca SSL debe haberse compilado con soporte para
extensiones TLS habilitado (comprueba haproxy -vv).

Esta obtención se diferencia de "req.ssl_sni" anterior en que se aplica a la conexión que está
siendo descifrada por HAProxy y no a contenido SSL que se reenvía a ciegas. Ver también
"ssl_fc_sni_end" y "ssl_fc_sni_reg" más abajo. Esto requiere que la biblioteca SSL esté compilada
con soporte para extensiones TLS habilitado (comprueba haproxy -vv).

¡CUIDADO! Salvo en condiciones muy específicas, normalmente no es correcto usar este campo como
sustituto del campo de cabecera HTTP "Host". Por ejemplo, al reenviar una conexión HTTPS a un
servidor, el campo SNI debe establecerse desde el campo de cabecera HTTP Host usando "req.hdr(host)"
y no desde el valor SNI frontal. La razón es que el SNI se usa únicamente para seleccionar el
certificado que presentará el lado del servidor, y que luego se permite a los clientes enviar
solicitudes con valores Host diferentes siempre que coincidan con los nombres del certificado. Por
ello, "ssl_fc_sni" normalmente no debería usarse como argumento de la palabra clave de servidor
"sni", salvo que el backend trabaje en modo TCP.

Derivadas de ACL:

```text
ssl_fc_sni_end: coincidencia de sufijo
ssl_fc_sni_reg: coincidencia de expresión regular
```

<a id="entry-7-3-4-ssl-fc-supported-versions-bin-binary"></a>

**`ssl_fc_supported_versions_bin([<filter_option>]): binary`**

```haproxy
ssl_fc_supported_versions_bin([<filter_option>]): binary
```

Devuelve el contenido de la extensión TLS supported_versions (43) presentada durante el Client
Hello. Proporciona una lista binaria de versiones de 2 bytes. TLSv1.3 (0x0304), TLSv1.2 (0x0303).

Este valor solo puede devolverse si el valor "tune.ssl.capture-buffer-size" está establecido mayor
que 0. Establecer `<filter_option>` permite filtrar los datos devueltos. Valores aceptados: 0:
devuelve la lista completa de cifrados (por defecto) 1: excluye los valores GREASE (RFC8701) de la
salida

ssl_fc_unique_id: binary Cuando la conexión entrante se realizó sobre una capa de transporte
SSL/TLS, devuelve el ID único de TLS tal como se define en el RFC5929 [sección 3](https://www.rfc-editor.org/rfc/rfc5929#section-3). El id único puede codificarse en base64
usando el conversor: "ssl_fc_unique_id,base64".

ssl_fc_use_keysize: integer Devuelve el tamaño de clave del cifrado simétrico usado en bits cuando
la conexión entrante se realizó sobre una capa de transporte SSL/TLS.

ssl_s_chain_der: binary Devuelve la cadena de certificados en formato DER presentada por el
servidor cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS. Cuando se
usa para una ACL, el valor o valores con los que comparar pueden pasarse en forma hexadecimal. El
resultado puede analizarse con cualquier biblioteca que acepte datos ASN.1 DER. Actualmente no
soporta sesiones reanudadas.

ssl_s_der: binary Devuelve el certificado en formato DER presentado por el servidor cuando la
conexión saliente se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL, el
valor o valores con los que comparar pueden pasarse en forma hexadecimal.

<a id="entry-7-3-4-ssl-s-i-dn-string"></a>

**`ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_i_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del emisor del certificado presentado por el servidor cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_s_i_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_s_i_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_s_i_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_s_key_alg: string Devuelve el nombre del algoritmo usado para generar la clave del certificado
presentado por el servidor cuando la conexión saliente se realizó sobre una capa de transporte
SSL/TLS.

ssl_s_notafter: string Devuelve la fecha de fin presentada por el servidor como cadena con formato
YYMMDDhhmmss[Z] cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS.

ssl_s_notbefore: string Devuelve la fecha de inicio presentada por el servidor como cadena con
formato YYMMDDhhmmss[Z] cuando la conexión saliente se realizó sobre una capa de transporte
SSL/TLS.

<a id="entry-7-3-4-ssl-s-s-dn-string"></a>

**`ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string`**

```haproxy
ssl_s_s_dn([<entry>[,<occ>[,<format>]]]): string
```

Cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS, devuelve el nombre
completo (distinguished name) del sujeto del certificado presentado por el servidor cuando no se
especifica `<entry>`, o el valor de la primera entrada dada encontrada desde el principio del DN.
Si se especifica un número de ocurrencia positivo/negativo como segundo argumento opcional,
devuelve el valor de la n-ésima entrada dada desde el principio/final del DN. Por ejemplo,
"ssl_s_s_dn(OU,2)" recupera la segunda unidad organizativa, y "ssl_s_s_dn(CN)" recupera el nombre común. El
parámetro `<format>` permite recibir el DN apto para el consumo por diferentes protocolos.
Actualmente se soporta rfc2253 para LDAP v3. Si deseas modificar solo el formato, puedes
especificar una cadena vacía y cero para los dos primeros parámetros. Ejemplo:
ssl_s_s_dn(,0,rfc2253) Si el valor ASN.1 de la entrada solicitada (o, cuando no se especifica
`<entry>`, cualquier entrada del DN) contiene un byte NUL incrustado seguido de otros datos, se
considera mal formado y no se devuelve ningún dato.

ssl_s_serial: binary Devuelve el número de serie del certificado presentado por el servidor cuando
la conexión saliente se realizó sobre una capa de transporte SSL/TLS. Cuando se usa para una ACL,
el valor o valores con los que comparar pueden pasarse en forma hexadecimal.

ssl_s_sha1: binary Devuelve la huella digital SHA-1 del certificado presentado por el servidor
cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS. Esto puede usarse para
saber qué certificado se eligió usando SNI.

ssl_s_sig_alg: string Devuelve el nombre del algoritmo usado para firmar el certificado presentado
por el servidor cuando la conexión saliente se realizó sobre una capa de transporte SSL/TLS.

ssl_s_version: integer Devuelve la versión del certificado presentado por el servidor cuando la
conexión saliente se realizó sobre una capa de transporte SSL/TLS.

txn.timer.user: integer Tiempo total estimado visto desde el cliente, entre el momento en que el
proxy lo aceptó y el momento en que se cerraron ambos extremos, sin tiempo de inactividad. Es el
equivalente de %Tu en el log-format y se informa en milisegundos (ms). Para más detalles ver
[Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) "Eventos de temporización"

### 7.3.5. Obtención de muestras a partir del contenido del búfer (capa 6) {#section-7-3-5}

La obtención de muestras a partir del contenido del búfer es un poco diferente de las obtenciones
de muestras anteriores porque los datos muestreados son efímeros. Estos datos solo pueden usarse
cuando están disponibles y se perderán cuando se reenvíen. Por esta razón, las muestras obtenidas
del contenido del búfer durante una solicitud no pueden usarse en una respuesta, por ejemplo.
Incluso mientras se obtienen los datos, estos pueden cambiar. A veces es necesario establecer
algunos retrasos o combinar varios métodos de obtención de muestras para asegurar que los datos
esperados estén completos y sean utilizables, por ejemplo mediante la inspección de contenido de
solicitudes TCP. Ver la palabra clave "tcp-request content" para información más detallada sobre
el tema.

Aviso: Las siguientes obtenciones de muestras se ignoran si se usan desde proxies HTTP. Estas solo
tratan con contenido en bruto encontrado en los búferes. Por su parte, los proxies HTTP usan
contenido estructurado. Por tanto, la representación en bruto de estos datos carece de sentido. Se
emite un aviso si una ACL depende de una de las siguientes obtenciones de muestras. Pero no es
posible detectar todos los usos no válidos (por ejemplo dentro de un formato de registro
personalizado o una expresión de muestra). Así que ten cuidado.

Resumen de los métodos de obtención de muestras de esta sección y sus tipos respectivos:

```text
  palabra clave                                       tipo de salida
----------------------------------------------------+-------------
distcc_body(<token>[,<occ>])                          binary
distcc_param(<token>[,<occ>])                         integer
payload(<offset>,<length>)                            binary
payload_lv(<offset1>,<length>[,<offset2>])            binary
rdp_cookie([<name>])                                  string
rdp_cookie_cnt([name])                                integer
rep_ssl_hello_type                                    integer
req.len                                               integer
req.payload(<offset>,<length>)                        binary
req.payload_lv(<offset1>,<length>[,<offset2>])        binary
req.proto_http                                        boolean
req.rdp_cookie([<name>])                              string
req.rdp_cookie_cnt([name])                            integer
req.ssl_alpn                                          string
req.ssl_cipherlist                                    binary
req.ssl_ec_ext                                        boolean
req.ssl_hello_type                                    integer
req.ssl_keyshare_groups                               binary
req.ssl_sigalgs                                       binary
req.ssl_sni                                           string
req.ssl_st_ext                                        integer
req.ssl_supported_groups                              binary
req.ssl_ver                                           integer
req_len                                               integer
req_proto_http                                        boolean
req_ssl_hello_type                                    integer
req_ssl_sni                                           string
req_ssl_ver                                           integer
res.len                                               integer
res.payload(<offset>,<length>)                        binary
res.payload_lv(<offset1>,<length>[,<offset2>])        binary
res.ssl_hello_type                                    integer
----------------------------------------------------+-------------
```

Lista detallada:

<a id="entry-7-3-5-distcc-body-binary"></a>

**`distcc_body(<token>[,<occ>]): binary`**

```haproxy
distcc_body(<token>[,<occ>]): binary
```

Analiza un mensaje distcc y devuelve el cuerpo asociado a la ocurrencia \#`<occ>` del token
`<token>`. Las ocurrencias comienzan en 1, y cuando no se especifica, cualquiera puede coincidir,
aunque en la práctica por ahora solo se comprueba la primera. Esto puede usarse para extraer
nombres de archivo o argumentos en archivos compilados usando distcc a través de HAProxy. Consulta
la documentación del protocolo de distcc para la lista completa de tokens soportados.

<a id="entry-7-3-5-distcc-param-integer"></a>

**`distcc_param(<token>[,<occ>]): integer`**

```haproxy
distcc_param(<token>[,<occ>]): integer
```

Analiza un mensaje distcc y devuelve el parámetro asociado a la ocurrencia \#`<occ>` del token
`<token>`. Las ocurrencias comienzan en 1, y cuando no se especifica, cualquiera puede coincidir,
aunque en la práctica por ahora solo se comprueba la primera. Esto puede usarse para extraer
cierta información como la versión del protocolo, el tamaño del archivo o el argumento en archivos
compilados usando distcc a través de HAProxy. Otro caso de uso consiste en esperar el inicio del
contenido del archivo preprocesado antes de conectar al servidor para evitar mantener conexiones
inactivas. Consulta la documentación del protocolo de distcc para la lista completa de tokens
soportados.

Ejemplo:

```shell
# wait up to 20s for the pre-processed file to be uploaded
tcp-request inspect-delay 20s
tcp-request content accept if { distcc_param(DOTI) -m found }
# send large files to the big farm
use_backend big_farm if { distcc_param(DOTI) gt 1000000 }
```

<a id="entry-7-3-5-payload-binary"></a>

**`payload(<offset>,<length>): binary (deprecated)`**

```haproxy
payload(<offset>,<length>): binary (deprecated)
```

Esto es un alias de "req.payload" cuando se usa en el contexto de una solicitud (p. ej. "stick on",
"stick match"), y de "res.payload" cuando se usa en el contexto de una respuesta, como en
"stick store response".

<a id="entry-7-3-5-payload-lv-binary"></a>

**`payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)`**

```haproxy
payload_lv(<offset1>,<length>[,<offset2>]): binary (deprecated)
```

Esto es un alias de "req.payload_lv" cuando se usa en el contexto de una solicitud (p. ej.
"stick on", "stick match"), y de "res.payload_lv" cuando se usa en el contexto de una respuesta,
como en "stick store response".

req.len: integer req_len: integer (deprecated) Devuelve un valor entero correspondiente al número
de bytes presentes en el búfer de solicitud. Esto se usa principalmente en ACL. Es importante
entender que esta prueba no devuelve false mientras el búfer esté cambiando. Esto significa que una
comprobación de igualdad a cero casi siempre coincidirá inmediatamente al principio de la sesión,
mientras que una prueba de más datos esperará a que lleguen esos datos y devolverá false solo
cuando HAProxy esté seguro de que no llegarán más datos. Esta prueba se diseñó para usarse con la
inspección de contenido de solicitudes TCP.

<a id="entry-7-3-5-req-payload-binary"></a>

**`req.payload(<offset>,<length>): binary`**

```haproxy
req.payload(<offset>,<length>): binary
```

Esto extrae un bloque binario de `<length>` bytes que comienza en el byte `<offset>` del búfer de
solicitud. Como caso especial, si el argumento `<length>` es cero, se extrae todo el búfer desde
`<offset>` hasta el final. Esto puede usarse con ACL para comprobar la presencia de algún
contenido en un búfer en cualquier ubicación.

Derivadas de ACL:

```text
req.payload(<offset>,<length>): coincidencia binaria hexadecimal
```

<a id="entry-7-3-5-req-payload-lv-binary"></a>

**`req.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
req.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

Esto extrae un bloque binario cuyo tamaño se especifica en `<length>` bytes a partir de `<offset1>`, y
que comienza en `<offset2>` si se especifica, o justo después de la longitud en el búfer de
solicitud. El parámetro `<offset2>` también soporta offsets relativos si se le antepone un signo
'+' o '-'.

Derivadas de ACL:

```text
req.payload_lv(<offset1>,<length>[,<offset2>]): coincidencia binaria hexadecimal
```

Ejemplo: consulta el ejemplo de la palabra clave "stick store-response".

req.proto_http: boolean req_proto_http: boolean (deprecated) Devuelve true cuando los datos del
búfer de solicitud parecen HTTP y se analizan correctamente como tal. Se usa el mismo analizador
que el analizador común de solicitudes HTTP, así que no debería haber sorpresas. La prueba no
coincide hasta que la solicitud esté completa, haya fallado o caduque. Esta prueba puede usarse
para informar del protocolo en registros TCP, pero el mayor uso es bloquear el análisis de
solicitudes TCP hasta que haya una solicitud HTTP completa en el búfer, por ejemplo para rastrear
una cabecera.

Ejemplo:

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content reject if !HTTP
tcp-request content track-sc0 base table req-rate
```

<a id="entry-7-3-5-req-rdp-cookie-string"></a>

**`req.rdp_cookie([<name>]): string`**

```haproxy
req.rdp_cookie([<name>]): string
rdp_cookie([<name>]): string (deprecated)
```

Cuando el búfer de solicitud parece el protocolo RDP, extrae la cookie RDP `<name>`, o cualquier
cookie si no se especifica. El analizador solo comprueba la primera cookie, tal como se ilustra en
la especificación del protocolo RDP. El nombre de la cookie no distingue mayúsculas de minúsculas.
Generalmente se usará el nombre de cookie "MSTS", ya que puede contener el nombre de usuario del
cliente que se conecta al servidor si está correctamente configurado en el cliente. La cookie
"MSTSHASH" también se usa a menudo para la persistencia de sesión en servidores.

Esto se diferencia de "balance rdp-cookie" en que puede usarse cualquier algoritmo de balanceo y,
por tanto, la distribución de clientes a servidores de backend no está ligada a un hash de la
cookie RDP. Se prevé que usar un algoritmo de balanceo como "balance roundrobin" o
"balance leastconn" conduzca a una distribución de clientes a servidores de backend más uniforme
que el hash usado por "balance rdp-cookie".

Derivadas de ACL:

```text
req.rdp_cookie([<name>]): coincidencia exacta de cadena
```

Ejemplo:

```text
listen tse-farm
    bind 0.0.0.0:3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # Persist based on the mstshash cookie
    # This is only useful makes sense if
    # balance rdp-cookie is not used
    stick-table type string size 204800
    stick on req.rdp_cookie(mstshash)
    server srv1 1.1.1.1:3389
    server srv1 1.1.1.2:3389
```

Ver también: "balance rdp-cookie", "persist rdp-cookie", "tcp-request" y la ACL "req.rdp_cookie".

<a id="entry-7-3-5-req-rdp-cookie-cnt-integer"></a>

**`req.rdp_cookie_cnt([name]): integer`**

```haproxy
req.rdp_cookie_cnt([name]): integer
rdp_cookie_cnt([name]): integer (deprecated)
```

Intenta analizar el búfer de solicitud como protocolo RDP y luego devuelve un entero
correspondiente al número de cookies RDP encontradas. Si se pasa un nombre de cookie opcional,
solo se consideran las cookies que coinciden con ese nombre. Esto se usa principalmente en ACL.

Derivadas de ACL:

```text
req.rdp_cookie_cnt([<name>]): coincidencia de enteros
```

req.ssl_alpn: string Devuelve una cadena que contiene los valores de la extensión TLS
Application-Layer Protocol Negotiation (ALPN) (RFC7301), enviada por el cliente dentro del mensaje
SSL ClientHello. Ten en cuenta que esto solo se aplica al contenido en bruto encontrado en el
búfer de solicitud y no al contenido descifrado mediante una capa de datos SSL, por lo que no
funcionará con líneas "bind" que tengan la opción "ssl". Esto es útil en ACL para tomar una
decisión de enrutamiento basada en las preferencias ALPN de un cliente TLS, como en el ejemplo
siguiente. Ver también "ssl_fc_alpn". Esta obtención solo analiza el primer mensaje ClientHello
encontrado en el búfer de solicitud; ver la documentación de la palabra clave "req.ssl_sni" para
más detalles sobre las implicaciones de esta limitación (HelloRetryRequest, Renegociación,
Encrypted Client Hello).

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_acme if { req.ssl_alpn acme-tls/1 }
default_backend bk_default
```

<a id="entry-7-3-5-req-ssl-cipherlist-binary"></a>

**`req.ssl_cipherlist binary`**

```haproxy
req.ssl_cipherlist binary
```

Devuelve la forma binaria de la lista de opciones de cifrado simétrico soportadas por el cliente,
según lo informado en el contenido de un ClientHello TLS. Ten en cuenta que esto solo se aplica al
contenido en bruto encontrado en el búfer de solicitud y no al contenido descifrado mediante una
capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan la opción "ssl". Ver
"ssl_fc_cipherlist_bin", que es el equivalente para bind SSL que puede usarse cuando se especifica
la opción "ssl". Esta obtención solo analiza el primer mensaje ClientHello encontrado en el búfer
de solicitud; ver la documentación de la palabra clave "req.ssl_sni" para más detalles sobre las
implicaciones de esta limitación (HelloRetryRequest, Renegociación, Encrypted Client Hello).

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_cipherlist,be2hex(:,2),lower -m sub 1302:009f }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ec_ext: boolean Devuelve un booleano que identifica si el cliente envió la extensión
Supported Elliptic Curves Extension definida en el RFC4492, [sección 5.1](https://www.rfc-editor.org/rfc/rfc4492#section-5.1), dentro del mensaje SSL
ClientHello. Esto puede usarse para presentar a los clientes compatibles con ECC un certificado EC
y usar RSA para todos los demás, sobre la misma dirección IP. Ten en cuenta que esto solo se aplica
al contenido en bruto encontrado en el búfer de solicitud y no al contenido descifrado mediante una
capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan la opción "ssl". Esta
obtención solo analiza el primer mensaje ClientHello encontrado en el búfer de solicitud; ver la
documentación de la palabra clave "req.ssl_sni" para más detalles sobre las implicaciones de esta
limitación (HelloRetryRequest, Renegociación, Encrypted Client Hello).

req.ssl_hello_type: integer req_ssl_hello_type: integer (deprecated) Devuelve un valor entero que
contiene el tipo del mensaje hello SSL encontrado en el búfer de solicitud si el búfer contiene
datos que se analizan como un mensaje client hello SSL completo (v3 o superior). Ten en cuenta que
esto solo se aplica al contenido en bruto encontrado en el búfer de solicitud y no al contenido
descifrado mediante una capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan la
opción "ssl". Esto se usa principalmente en ACL para detectar la presencia de un mensaje hello SSL
que se supone contiene un ID de sesión SSL utilizable para persistencia. Esta obtención solo
analiza el primer mensaje ClientHello encontrado en el búfer de solicitud; ver la documentación de
la palabra clave "req.ssl_sni" para más detalles sobre las implicaciones de esta limitación
(HelloRetryRequest, Renegociación, Encrypted Client Hello).

<a id="entry-7-3-5-req-ssl-keyshare-groups-binary"></a>

**`req.ssl_keyshare_groups binary`**

```haproxy
req.ssl_keyshare_groups binary
```

Devuelve el formato binario de la lista de parámetros criptográficos para el intercambio de
claves soportados por el cliente, según lo informado en el ClientHello TLS. En TLS v1.3, keyshare
forma parte del mensaje ClientHello y es la última extensión del client hello. Ten en cuenta que
esto solo se aplica al contenido en bruto encontrado en el búfer de solicitud y no al contenido
descifrado mediante una capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan la
opción "ssl". Esta obtención solo analiza el primer mensaje ClientHello encontrado en el búfer de
solicitud; ver la documentación de la palabra clave "req.ssl_sni" para más detalles sobre las
implicaciones de esta limitación (HelloRetryRequest, Renegociación, Encrypted Client Hello).

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_keyshare_groups,be2hex(:,2),lower -m sub 001d  }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

<a id="entry-7-3-5-req-ssl-sigalgs-binary"></a>

**`req.ssl_sigalgs binary`**

```haproxy
req.ssl_sigalgs binary
```

Devuelve la forma binaria de la lista de algoritmos de firma soportados por el cliente, según lo
informado en el ClientHello TLS. Esto está disponible como una extensión del client hello. Ten en
cuenta que esto solo se aplica al contenido en bruto encontrado en el búfer de solicitud y no al
contenido descifrado mediante una capa de datos SSL, por lo que no funcionará con líneas "bind"
que tengan la opción "ssl". Ver "ssl_fc_sigalgs_bin", que es el equivalente para bind SSL que
puede usarse cuando se especifica la opción "ssl". Esta obtención solo analiza el primer mensaje
ClientHello encontrado en el búfer de solicitud; ver la documentación de la palabra clave
"req.ssl_sni" para más detalles sobre las implicaciones de esta limitación (HelloRetryRequest,
Renegociación, Encrypted Client Hello).

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe4 if { req.ssl_sigalgs,be2hex(:,2),lower -m sub 0403:0805 }
server fe4  ${htst_fe4_addr}:${htst_fe4_port}
```

req.ssl_sni: string req_ssl_sni: string (deprecated) Devuelve una cadena que contiene el valor de
la extensión TLS Server Name enviada por un cliente en un flujo TLS que pasa por el búfer de
solicitud, si el búfer contiene datos que se analizan como un mensaje client hello SSL completo
(v3 o superior). Ten en cuenta que esto solo se aplica al contenido en bruto encontrado en el
búfer de solicitud y no al contenido descifrado mediante una capa de datos SSL, por lo que no
funcionará con líneas "bind" que tengan la opción "ssl". Esto solo funcionará para protocolos
reales basados en TLS implícito como HTTPS (443), IMAPS (993) o SMTPS (465); sin embargo, no
funcionará para protocolos basados en TLS explícito, como SMTP (25/587) o IMAP (143). El SNI
normalmente contiene el nombre del host al que el cliente intenta conectarse (en navegadores
recientes). Esta prueba se diseñó para usarse con la inspección de contenido de solicitudes TCP.
Si se necesita conmutación de contenido, se recomienda esperar primero un client hello completo
(tipo 1), como en el ejemplo siguiente. Ver también "ssl_fc_sni". Ten cuidado que, por las razones
detalladas más abajo (HelloRetryRequest, Renegociación, Encrypted Client Hello), el valor devuelto
por esta obtención no es lo suficientemente fiable como para usarse solo para permitir o denegar
el acceso a ciertos hosts.

Esta obtención solo analiza el primer mensaje ClientHello encontrado en el búfer de solicitud. Si
el cliente envía varios mensajes ClientHello dentro del mismo flujo TCP, por ejemplo porque el
servidor solicitó un HelloRetryRequest (HRR) como parte de TLS 1.3, o porque el cliente inicia una
renegociación TLS (que envía un nuevo ClientHello más tarde en el mismo flujo TCP, posiblemente
transportando un SNI diferente), solo se devolverá el SNI transportado por ese primer ClientHello;
el contenido de cualquier ClientHello posterior se ignorará.

Cuando se usa Encrypted Client Hello (ECH), el ClientHello visto en el cable es solo el ClientHello
"Outer" (exterior), que incrusta el ClientHello "Inner" (interior) real y cifrado. El SNI extraído
por esta obtención en ese caso es el del ClientHello Outer, que es un SNI señuelo y no el host real
al que el cliente pretende llegar. Esta obtención actualmente no puede descifrar ni analizar el
ClientHello Inner, por lo que no debe confiarse en ella para tomar decisiones de enrutamiento o de
control de acceso cuando ECH está en uso.

Derivadas de ACL:

```text
req.ssl_sni: coincidencia exacta de cadena
```

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use_backend bk_allow if { req.ssl_sni -f allowed_sites }
default_backend bk_sorry_page
```

req.ssl_st_ext: integer Devuelve 0 si el cliente no envió una extensión TLS SessionTicket
(RFC5077) Devuelve 1 si el cliente envió la extensión TLS SessionTicket Devuelve 2 si el cliente
también envió un SessionTicket TLS de longitud no nula Ten en cuenta que esto solo se aplica al
contenido en bruto encontrado en el búfer de solicitud y no al contenido descifrado mediante una
capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan la opción "ssl". Esto
puede usarse, por ejemplo, para detectar si el cliente envió o no un SessionTicket y fijarlo en
consecuencia; si no hay SessionTicket, entonces fijar sobre el SessionID o no fijar, ya que no hay
estado en el lado del servidor cuando se usan SessionTickets. Esta obtención solo analiza el
primer mensaje ClientHello encontrado en el búfer de solicitud; ver la documentación de la palabra
clave "req.ssl_sni" para más detalles sobre las implicaciones de esta limitación
(HelloRetryRequest, Renegociación, Encrypted Client Hello).

<a id="entry-7-3-5-req-ssl-supported-groups-binary"></a>

**`req.ssl_supported_groups binary`**

```haproxy
req.ssl_supported_groups binary
```

Devuelve la forma binaria de la lista de grupos soportados por el cliente, según lo informado en
el ClientHello TLS y usados para el intercambio de claves, lo que puede incluir tanto intercambio
de claves con curva elíptica como no EC. Ten en cuenta que esto solo se aplica al contenido en
bruto encontrado en el búfer de solicitud y no al contenido descifrado mediante una capa de datos
SSL, por lo que no funcionará con líneas "bind" que tengan la opción "ssl". Ver
"ssl_fc_eclist_bin", que es el equivalente para bind SSL que puede usarse cuando se especifica la
opción "ssl". Esta obtención solo analiza el primer mensaje ClientHello encontrado en el búfer de
solicitud; ver la documentación de la palabra clave "req.ssl_sni" para más detalles sobre las
implicaciones de esta limitación (HelloRetryRequest, Renegociación, Encrypted Client Hello).

Ejemplos:

```shell
# Wait for a client hello for at most 5 seconds
tcp-request inspect-delay 5s
tcp-request content accept if { req.ssl_hello_type 1 }
use-server fe3 if { req.ssl_supported_groups, be2hex(:,2),lower -m sub 0017 }
server fe3  ${htst_fe3_addr}:${htst_fe3_port}
```

req.ssl_ver: integer req_ssl_ver: integer (deprecated) Devuelve un valor entero que contiene la
versión del protocolo SSL/TLS de un flujo presente en el búfer de solicitud. Se soportan tanto los
mensajes hello SSLv2 como los mensajes SSLv3. TLSv1 se anuncia como SSL versión 3.1. El valor se
compone de la versión mayor multiplicada por 65536, sumada a la versión menor. Ten en cuenta que
esto solo se aplica al contenido en bruto encontrado en el búfer de solicitud y no al contenido
descifrado mediante una capa de datos SSL, por lo que no funcionará con líneas "bind" que tengan
la opción "ssl". La versión ACL de la prueba coincide con una notación decimal de la forma
MAYOR.MENOR (p. ej. 3.1). Esta obtención se usa principalmente en ACL. Esta obtención solo analiza
el primer mensaje ClientHello encontrado en el búfer de solicitud; ver la documentación de la
palabra clave "req.ssl_sni" para más detalles sobre las implicaciones de esta limitación
(HelloRetryRequest, Renegociación, Encrypted Client Hello).

Derivadas de ACL:

```text
req.ssl_ver: coincidencia decimal
```

res.len: integer Devuelve un valor entero correspondiente al número de bytes presentes en el búfer
de respuesta. Esto se usa principalmente en ACL. Es importante entender que esta prueba no
devuelve false mientras el búfer esté cambiando. Esto significa que una comprobación de igualdad a
cero casi siempre coincidirá inmediatamente al principio del flujo, mientras que una prueba de más
datos esperará a que lleguen esos datos y devolverá false solo cuando HAProxy esté seguro de que
no llegarán más datos. Esta prueba se diseñó para usarse con la inspección de contenido de
respuestas TCP. Pero también puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-5-res-payload-binary"></a>

**`res.payload(<offset>,<length>): binary`**

```haproxy
res.payload(<offset>,<length>): binary
```

Esto extrae un bloque binario de `<length>` bytes que comienza en el byte `<offset>` del búfer de
respuesta. Como caso especial, si el argumento `<length>` es cero, se extrae todo el búfer desde
`<offset>` hasta el final. Esto puede usarse con ACL para comprobar la presencia de algún
contenido en un búfer en cualquier ubicación. También puede usarse en reglas expect basadas en
tcp-check.

<a id="entry-7-3-5-res-payload-lv-binary"></a>

**`res.payload_lv(<offset1>,<length>[,<offset2>]): binary`**

```haproxy
res.payload_lv(<offset1>,<length>[,<offset2>]): binary
```

Esto extrae un bloque binario cuyo tamaño se especifica en `<length>` bytes a partir de `<offset1>`, y
que comienza en `<offset2>` si se especifica, o justo después de la longitud en el búfer de
respuesta. El parámetro `<offset2>` también soporta offsets relativos si se le antepone un signo
'+' o '-'. También puede usarse en reglas expect basadas en tcp-check.

Ejemplo: consulta el ejemplo de la palabra clave "stick store-response".

res.ssl_hello_type: integer rep_ssl_hello_type: integer (deprecated) Devuelve un valor entero que
contiene el tipo del mensaje hello SSL encontrado en el búfer de respuesta si el búfer contiene
datos que se analizan como un mensaje hello SSL completo (v3 o superior). Ten en cuenta que esto
solo se aplica al contenido en bruto encontrado en el búfer de respuesta y no al contenido
descifrado mediante una capa de datos SSL, por lo que no funcionará con líneas "server" que tengan
la opción "ssl". Esto se usa principalmente en ACL para detectar la presencia de un mensaje hello
SSL que se supone contiene un ID de sesión SSL utilizable para persistencia.

### 7.3.6. Obtención de muestras HTTP (capa 7) {#section-7-3-6}

Es posible obtener muestras del contenido HTTP, de las solicitudes y de las respuestas. Esta capa
de aplicación también se denomina capa 7. Solo es posible obtener los datos de esta sección cuando
se ha analizado una solicitud o respuesta HTTP completa desde su búfer de solicitud o respuesta
respectivo. Este es siempre el caso con todas las reglas específicas HTTP y para las secciones que
se ejecutan con "mode http". Al usar la inspección de contenido TCP, puede ser necesario soportar
un retraso de inspección para dejar que la solicitud o respuesta llegue primero. Estas obtenciones
pueden requerir algo más de recursos de CPU que las de capa 4, pero no mucho, ya que la solicitud
y la respuesta están indexadas.

Nota: En cuanto al procesamiento HTTP desde las reglas tcp-request content, todo funcionará como
se espera desde un proxy HTTP. Sin embargo, desde un proxy TCP, sin un cambio al protocolo HTTP, solo
funcionará para contenido HTTP/1. Para contenido HTTP/2, solo el prefacio es visible. Por tanto,
solo es posible confiar en las obtenciones de muestras "req.proto_http", "req.ver" y
eventualmente "method". Todas las demás obtenciones de muestras L7 fallarán. Tras un cambio al protocolo HTTP, funcionarán de la misma manera que desde un proxy HTTP.

Resumen de los métodos de obtención de muestras de esta sección y sus tipos respectivos:

```text
  palabra clave                                    tipo de salida
-------------------------------------------------+-------------
base                                               string
base32                                             integer
base32+src                                         binary
baseq                                              string
capture.req.hdr(<idx>)                             string
capture.req.method                                 string
capture.req.uri                                    string
capture.req.ver                                    string
capture.res.hdr(<idx>)                             string
capture.res.ver                                    string
cook([<name>])                                     string
cook_cnt([<name>])                                 integer
cook_val([<name>])                                 integer
cookie([<name>])                                   string
hdr([<name>[,<occ>]])                              string
hdr_cnt([<header>])                                integer
hdr_ip([<name>[,<occ>]])                           ip
hdr_val([<name>[,<occ>]])                          integer
http_auth(<userlist>)                              boolean
http_auth_bearer([<header>])                       string
http_auth_group(<userlist>)                        string
http_auth_pass                                     string
http_auth_type                                     string
http_auth_user                                     string
http_first_req                                     boolean
method                                             integer
path                                               string
pathq                                              string
query([<options>])                                 string
req.body                                           binary
req.body_len                                       integer
req.body_param([<name>[,i]])                       string
req.body_size                                      integer
req.cook([<name>])                                 string
req.cook_cnt([<name>])                             integer
req.cook_names([<delim>])                          string
req.cook_val([<name>])                             integer
req.fhdr(<name>[,<occ>])                           string
req.fhdr_cnt([<name>])                             integer
req.hdr([<name>[,<occ>]])                          string
req.hdr_cnt([<name>])                              integer
req.hdr_ip([<name>[,<occ>]])                       ip
req.hdr_names([<delim>])                           string
req.hdr_val([<name>[,<occ>]])                      integer
req.hdrs                                           string
req.hdrs_bin                                       binary
req.timer.hdr                                      integer
req.timer.idle                                     integer
req.timer.queue                                    integer
req.timer.tq                                       integer
req.ver                                            string
req_ver                                            string
request_date([<unit>])                             integer
res.body                                           binary
res.body_len                                       integer
res.body_size                                      integer
res.cache_hit                                      boolean
res.cache_name                                     string
res.comp                                           boolean
res.comp_algo                                      string
res.cook([<name>])                                 string
res.cook_cnt([<name>])                             integer
res.cook_names([<delim>])                          string
res.cook_val([<name>])                             integer
res.fhdr([<name>[,<occ>]])                         string
res.fhdr_cnt([<name>])                             integer
res.hdr([<name>[,<occ>]])                          string
res.hdr_cnt([<name>])                              integer
res.hdr_ip([<name>[,<occ>]])                       ip
res.hdr_names([<delim>])                           string
res.hdr_val([<name>[,<occ>]])                      integer
res.hdrs                                           string
res.hdrs_bin                                       binary
res.timer.hdr                                      integer
res.ver                                            string
resp_ver                                           string
scook([<name>])                                    string
scook_cnt([<name>])                                integer
scook_val([<name>])                                integer
server_status                                      integer
set-cookie([<name>])                               string
shdr([<name>[,<occ>]])                             string
shdr_cnt([<name>])                                 integer
shdr_ip([<name>[,<occ>]])                          ip
shdr_val([<name>[,<occ>]])                         integer
status                                             integer
txn.status                                         integer
txn.timer.total                                    integer
unique-id                                          string
url                                                string
url32                                              integer
url32+src                                          binary
url_ip                                             ip
url_param([<name>[,<delim>[,i]]])                  string
url_port                                           integer
urlp([<name>[,<delim>[,i]]])                       string
urlp_val([<name>[,<delim>[,i]]])                   integer
-------------------------------------------------+-------------
```

Lista detallada:

base: string Esto devuelve la concatenación de la primera cabecera Host y la parte de la ruta de
la solicitud, que comienza en la primera barra y termina antes del signo de interrogación. Puede
ser útil en entornos con hosting virtual para detectar abusos de URL, así como para mejorar la
eficiencia de las cachés compartidas. Usarlo con una stick table de tamaño limitado también
permite recopilar estadísticas sobre los objetos más solicitados por host/ruta. Con ACL puede
permitir reglas simples de conmutación de contenido que involucren el host y la ruta al mismo
tiempo, como "[www.example.com/favicon.ico](http://www.example.com/favicon.ico)". Ver también
"path" y "uri".

Derivadas de ACL:

```text
base    : coincidencia exacta de cadena
base_beg: coincidencia de prefijo
base_dir: coincidencia de subdirectorio
base_dom: coincidencia de dominio
base_end: coincidencia de sufijo
base_len: coincidencia de longitud
base_reg: coincidencia de expresión regular
base_sub: coincidencia de subcadena
```

Nota: Las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

base32: integer Esto devuelve un hash de 32 bits del valor devuelto por el método de obtención
"base" anterior. Esto es útil para rastrear la actividad por URL en sitios con mucho tráfico sin
tener que almacenar todas las URL. En su lugar se almacena un hash más corto, ahorrando mucha
memoria. El tipo de salida es un entero sin signo. La función hash usada es SDBM con avalancha
completa en la salida. Técnicamente, base32 es exactamente igual a "base,sdbm(1)".

base32+src: binary Esto devuelve la concatenación de la obtención base32 anterior y la obtención
src siguiente. El tipo resultante es de tipo binario, con un tamaño de 8 o 20 bytes dependiendo de
la familia de la dirección de origen. Esto puede usarse para rastrear contadores por IP y por URL.

baseq: string Esto devuelve la concatenación de la primera cabecera Host y la parte de la ruta de
la solicitud con la cadena de consulta, que comienza en la primera barra. Usarlo en lugar de
"base" permite identificar correctamente el recurso de destino, para casos de uso de estadísticas
o caché. Ver también "path", "pathq" y "base".

<a id="entry-7-3-6-capture-req-hdr-string"></a>

**`capture.req.hdr(<idx>): string`**

```haproxy
capture.req.hdr(<idx>): string
```

Esto extrae el contenido de la cabecera capturada por "capture request header"; idx es la posición
de la palabra clave de captura en la configuración. La primera entrada tiene índice 0. Ver
también: "capture request header".

capture.req.method: string Esto extrae el METHOD de una solicitud HTTP. Puede usarse tanto en
solicitud como en respuesta. A diferencia de "method", puede usarse tanto en solicitud como en
respuesta porque está asignado en memoria.

capture.req.uri: string Esto extrae el URI de la solicitud, que comienza en la primera barra y
termina antes del primer espacio en la solicitud (sin la parte del host). A diferencia de "path" y
"url", puede usarse tanto en solicitud como en respuesta porque está asignado en memoria.

capture.req.ver: string Esto extrae la versión HTTP de la solicitud y la devuelve con el formato
"HTTP/`<major>`.`<minor>`". Puede usarse en solicitud, respuesta y registros porque depende de una
información persistente. Si la versión de la solicitud no es válida, esta obtención de muestra
falla.

<a id="entry-7-3-6-capture-res-hdr-string"></a>

**`capture.res.hdr(<idx>): string`**

```haproxy
capture.res.hdr(<idx>): string
```

Esto extrae el contenido de la cabecera capturada por "capture response header"; idx es la
posición de la palabra clave de captura en la configuración. La primera entrada tiene índice 0.
Ver también: "capture response header"

capture.res.ver: string Esto extrae la versión HTTP de la respuesta y la devuelve con el formato
"HTTP/`<major>`.`<minor>`". Puede usarse en registros porque depende de una información
persistente. Si la versión de la respuesta no es válida, esta obtención de muestra falla.

<a id="entry-7-3-6-cookie-string"></a>

**`cookie([<name>]): string (deprecated)`**

```haproxy
cookie([<name>]): string (deprecated)
```

Esto extrae la última ocurrencia de la cookie de nombre `<name>` en una línea de cabecera
"Cookie" de la solicitud, o una cabecera "Set-Cookie" de la respuesta, y devuelve su valor como
cadena. Un uso típico es conseguir que múltiples clientes que comparten un mismo perfil usen el
mismo servidor. Esto puede ser similar a lo que hacía "appsession" con la declaración
"request-learn", pero con soporte de sincronización multi-par y conservación de estado entre
reinicios. Si no se especifica ningún nombre, se devuelve el primer valor de cookie. Esta
obtención ya no debería usarse y debería sustituirse por req.cook() o res.cook(), ya que usa de
forma ambigua la dirección basándose en el contexto donde se usa.

<a id="entry-7-3-6-hdr-string"></a>

**`hdr([<name>[,<occ>]]): string`**

```haproxy
hdr([<name>[,<occ>]]): string
```

Esto es equivalente a req.hdr() cuando se usa en solicitudes, y a res.hdr() cuando se usa en
respuestas. Consulta estas obtenciones respectivas para más detalles. En caso de duda sobre la
dirección de la obtención, usa las explícitas. Ten en cuenta que, a diferencia del método de
obtención de muestras hdr(), las palabras clave ACL hdr\_\* se aplican sin ambigüedad a las
cabeceras de la solicitud.

<a id="entry-7-3-6-http-auth-boolean"></a>

**`http_auth(<userlist>): boolean`**

```haproxy
http_auth(<userlist>): boolean
```

Devuelve un booleano que indica si los datos de autenticación recibidos del cliente coinciden con
un nombre de usuario y contraseña almacenados en la lista de usuarios especificada. Esta función
de obtención no es realmente útil fuera de las ACL. Actualmente solo se soporta la autenticación
básica http.

<a id="entry-7-3-6-http-auth-bearer-string"></a>

**`http_auth_bearer([<header>]): string`**

```haproxy
http_auth_bearer([<header>]): string
```

Devuelve el token proporcionado por el cliente encontrado en los datos de autorización cuando se
usa el esquema Bearer (para enviar JSON Web Tokens, por ejemplo). No se realiza ninguna
comprobación sobre los datos enviados por el cliente. Si se proporciona un `<header>` específico,
se analizará esa cabecera en lugar de la de Authorization.

<a id="entry-7-3-6-http-auth-group-string"></a>

**`http_auth_group(<userlist>): string`**

```haproxy
http_auth_group(<userlist>): string
```

Devuelve una cadena correspondiente al nombre de usuario encontrado en los datos de autenticación
recibidos del cliente si tanto el nombre de usuario como la contraseña son válidos según la lista
de usuarios especificada. El propósito principal es usarla en ACL, donde luego se comprueba si el
usuario pertenece a algún grupo dentro de una lista. Esta función de obtención no es realmente
útil fuera de las ACL. Actualmente solo se soporta la autenticación básica http.

Derivadas de ACL:

```text
http_auth_group(<userlist>): group ...
Devuelve true cuando el usuario extraído de la solicitud, cuya contraseña es
válida según la lista de usuarios especificada, pertenece a al menos uno de
los grupos.
```

http_auth_pass: string Devuelve la contraseña del usuario encontrada en los datos de autenticación
recibidos del cliente, tal como se suministró en la cabecera Authorization. Esta obtención de
muestra no realiza comprobaciones. Solo se soporta la autenticación Basic.

http_auth_type: string Devuelve el método de autenticación encontrado en los datos de
autenticación recibidos del cliente, tal como se suministró en la cabecera Authorization. Esta
obtención de muestra no realiza comprobaciones. Solo se soporta la autenticación Basic.

http_auth_user: string Devuelve el nombre de usuario encontrado en los datos de autenticación
recibidos del cliente, tal como se suministró en la cabecera Authorization. Esta obtención de
muestra no realiza comprobaciones. Solo se soporta la autenticación Basic.

http_first_req: boolean Devuelve true cuando la solicitud en procesamiento es la primera de la
conexión. Esto puede usarse para añadir o eliminar cabeceras que pueden faltar en algunas
solicitudes cuando una solicitud no es la primera, o para ayudar a agrupar solicitudes en los
registros.

method: integer + string Devuelve un valor entero correspondiente al método de la solicitud HTTP.
Por ejemplo, "GET" equivale a 1 (consulta las fuentes para establecer la correspondencia). El
valor 9 significa "otro método" y puede convertirse a una cadena extraída del flujo. Esto no
debería usarse directamente como muestra; está pensado solo para usarse desde ACL, que convierten
transparentemente los métodos de patrones a estos valores entero + cadena. Algunas ACL
predefinidas ya comprueban los métodos más comunes.

Derivadas de ACL:

```text
method: coincidencia del método sin distinguir mayúsculas y minúsculas
```

Ejemplo:

```shell
# only accept GET and HEAD requests
acl valid_method method GET HEAD
http-request deny if ! valid_method
```

path: string Extrae la ruta URL de la solicitud, que comienza en la primera barra y termina antes del signo
de interrogación (sin la parte del host). Un uso típico es con cachés capaces de precarga, y con
portales que necesitan agregar información múltiple de bases de datos y mantenerla en cachés. Ten en cuenta
que con cachés de salida sería más prudente usar "url" en su lugar. Con ACL, se usa típicamente para
coincidir con nombres de archivo exactos (p. ej. "/login.php"), o con partes de directorios usando
las formas derivadas. Consulta también los métodos de obtención "url" y "base". Ten en cuenta que cualquier
referencia a un fragmento en el URI ('#' tras la ruta) está estrictamente prohibida por el estándar
HTTP y será rechazada. Sin embargo, si el frontend que recibe la solicitud tiene "option
accept-unsafe-violations-in-http-request", entonces esta parte del fragmento será aceptada y también
aparecerá en la ruta.

Derivadas de ACL:

```text
path    : coincidencia exacta de cadena
path_beg: coincidencia de prefijo
path_dir: coincidencia de subdirectorio
path_dom: coincidencia de dominio
path_end: coincidencia de sufijo
path_len: coincidencia de longitud
path_reg: coincidencia de expresión regular
path_sub: coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

pathq: string Extrae la ruta URL de la solicitud junto con la cadena de consulta, que comienza en la
primera barra. Esta obtención de muestra es muy práctica para recuperar siempre un URI relativo,
excluyendo el esquema y la parte de autoridad, si existen. De hecho, mientras que esta es la
representación común de un destino de solicitud HTTP/1.1, en HTTP/2 se usa a menudo un URI absoluto.
Esta obtención de muestra devolverá el mismo resultado en ambos casos. Ten en cuenta que cualquier
referencia a un fragmento en el URI ('#' tras la ruta) está estrictamente prohibida por el estándar
HTTP y será rechazada. Sin embargo, si el frontend que recibe la solicitud tiene "option
accept-unsafe-violations-in-http-request", entonces esta parte del fragmento será aceptada y también
aparecerá en la ruta.

<a id="entry-7-3-6-query-string"></a>

**`query([<options>]): string`**

```haproxy
query([<options>]): string
```

Extrae la cadena de consulta de la solicitud, que comienza después del primer signo de
interrogación. Si no hay ningún signo de interrogación, esta obtención no devuelve nada. Si hay un
signo de interrogación pero no sigue nada, devuelve una cadena vacía. Esto significa que es posible
saber fácilmente si hay una cadena de consulta usando el método de coincidencia "found". Esta
obtención es el complemento de "path", que se detiene antes del signo de interrogación, y de
"query_string", que incluye el signo de interrogación.

Puede usarse un parámetro opcional para personalizar el valor devuelto. Se soportan las siguientes
opciones:

    - with_qm: Incluir el signo de interrogación al comienzo de la cadena de
                consulta, si no está vacía.

req.body: binary Devuelve el cuerpo disponible de la solicitud HTTP como un bloque de datos. Se
recomienda usar "option http-buffer-request" para asegurarse de esperar, en la medida de lo posible,
el cuerpo de la solicitud.

req.body_len: integer Devuelve la longitud del cuerpo disponible de la solicitud HTTP en bytes.
Puede ser inferior a la longitud anunciada si el cuerpo es mayor que el búfer. Se recomienda usar
"option http-buffer-request" para asegurarse de esperar, en la medida de lo posible, el cuerpo de la
solicitud.

<a id="entry-7-3-6-req-body-param-string"></a>

**`req.body_param([<name>[,i]]): string`**

```haproxy
req.body_param([<name>[,i]]): string
```

Esta obtención asume que el cuerpo de la solicitud POST está codificado en URL. El usuario puede
comprobar si "content-type" contiene el valor "application/x-www-form-urlencoded". Extrae la primera
aparición del parámetro `<name>` en el cuerpo, que termina antes de '&'. El nombre del parámetro
distingue entre mayúsculas y minúsculas, salvo que se añada "i" como segundo argumento. Si no se
indica ningún nombre, cualquier parámetro coincidirá y se devolverá el primero. El resultado es una
cadena correspondiente al valor del parámetro `<name>` tal como se presenta en el cuerpo de la
solicitud (no se realiza ninguna decodificación de URL). Ten en cuenta que la versión ACL de esta obtención
itera sobre múltiples parámetros e informará iterativamente de los valores de todos los parámetros
si no se indica ningún nombre.

req.body_size: integer Devuelve la longitud anunciada del cuerpo de la solicitud HTTP en bytes.
Representará la cabecera Content-Length anunciada, o el tamaño de los datos disponibles en caso de
codificación por fragmentos.

<a id="entry-7-3-6-req-cook-string"></a>

**`req.cook([<name>]): string`**

```haproxy
req.cook([<name>]): string
cook([<name>]): string (deprecated)
```

Extrae la última aparición del nombre de cookie `<name>` en una línea de cabecera "Cookie" de la
solicitud, y devuelve su valor como cadena. Si no se especifica ningún nombre, se devuelve el valor
de la primera cookie. Cuando se usa con ACL, se evalúan todas las cookies que coinciden. Los
espacios alrededor del nombre y del valor se ignoran, tal como exige la especificación de la
cabecera Cookie (RFC6265). El nombre de la cookie distingue entre mayúsculas y minúsculas. Las
cookies vacías son válidas, de modo que una cookie vacía puede perfectamente devolver un valor vacío
si está presente. Usa la coincidencia "found" para detectar la presencia. Usa la variante res.cook()
para las cookies de respuesta enviadas por el servidor.

Derivadas de ACL:

```text
req.cook([<name>])    : coincidencia exacta de cadena
req.cook_beg([<name>]): coincidencia de prefijo
req.cook_dir([<name>]): coincidencia de subdirectorio
req.cook_dom([<name>]): coincidencia de dominio
req.cook_end([<name>]): coincidencia de sufijo
req.cook_len([<name>]): coincidencia de longitud
req.cook_reg([<name>]): coincidencia de expresión regular
req.cook_sub([<name>]): coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

<a id="entry-7-3-6-req-cook-cnt-integer"></a>

**`req.cook_cnt([<name>]): integer`**

```haproxy
req.cook_cnt([<name>]): integer
cook_cnt([<name>]): integer (deprecated)
```

Devuelve un valor entero que representa el número de apariciones de la cookie `<name>` en la
solicitud, o de todas las cookies si no se especifica `<name>`.

<a id="entry-7-3-6-req-cook-names-string"></a>

**`req.cook_names([<delim>]): string`**

```haproxy
req.cook_names([<delim>]): string
```

Construye una cadena formada por la concatenación de todos los nombres de cookies tal como aparecen
en la solicitud (cabecera Cookie) cuando se evalúa la regla. El delimitador por defecto es la coma
(','), pero puede sobrescribirse como argumento opcional `<delim>`. En este caso, solo se considera
el primer carácter de `<delim>`.

<a id="entry-7-3-6-req-cook-val-integer"></a>

**`req.cook_val([<name>]): integer`**

```haproxy
req.cook_val([<name>]): integer
cook_val([<name>]): integer (deprecated)
```

Extrae la última aparición del nombre de cookie `<name>` en una línea de cabecera "Cookie" de la
solicitud, y convierte su valor en un entero que se devuelve. Si no se especifica ningún nombre, se
devuelve el valor de la primera cookie. Cuando se usa en ACL, se iteran todos los nombres que
coinciden hasta que un valor coincida.

<a id="entry-7-3-6-req-fhdr-string"></a>

**`req.fhdr(<name>[,<occ>]): string`**

```haproxy
req.fhdr(<name>[,<occ>]): string
```

Devuelve el valor completo de la última aparición de la cabecera `<name>` en una solicitud HTTP. Se
diferencia de req.hdr() en que cualquier coma presente en el valor se devuelve y no se usa como
delimitador. Esto a veces resulta útil con cabeceras como User-Agent.

Cuando se usa desde una ACL, se iteran todas las apariciones hasta encontrar una coincidencia.

Opcionalmente, puede especificarse una aparición concreta como número de posición. Los valores
positivos indican una posición contada desde la primera aparición, siendo 1 la primera. Los valores
negativos indican posiciones relativas a la última, siendo -1 la última.

<a id="entry-7-3-6-req-fhdr-cnt-integer"></a>

**`req.fhdr_cnt([<name>]): integer`**

```haproxy
req.fhdr_cnt([<name>]): integer
```

Devuelve un valor entero que representa el número de apariciones del nombre de campo de cabecera de
solicitud `<name>`, o el número total de campos de cabecera si no se especifica `<name>`. Al igual
que req.fhdr(), se diferencia de res.hdr_cnt() en que no divide las cabeceras por las comas.

<a id="entry-7-3-6-req-hdr-string"></a>

**`req.hdr([<name>[,<occ>]]): string`**

```haproxy
req.hdr([<name>[,<occ>]]): string
```

Devuelve el último valor separado por comas de la cabecera `<name>` en una solicitud HTTP. Esta
obtención considera cualquier coma como un delimitador de valores distintos. Esto es útil si
necesitas procesar cabeceras que están definidas como una lista de valores, como Accept o
X-Forwarded-For. Si en su lugar se desean cabeceras de línea completa, usa req.fhdr(). Comprueba
cuidadosamente el RFC 7231 para saber cómo se supone que se analizan ciertas cabeceras. Además,
algunas de ellas no distinguen entre mayúsculas y minúsculas (p. ej. Connection).

Cuando se usa desde una ACL, se iteran todas las apariciones hasta encontrar una coincidencia.

Opcionalmente, puede especificarse una aparición concreta como número de posición. Los valores
positivos indican una posición contada desde la primera aparición, siendo 1 la primera. Los valores
negativos indican posiciones relativas a la última, siendo -1 la última.

Un uso típico es con la cabecera X-Forwarded-For una vez convertida a IP, asociada a una tabla de
persistencia de IP.

Derivadas de ACL:

```text
hdr([<name>[,<occ>]])    : coincidencia exacta de cadena
hdr_beg([<name>[,<occ>]]): coincidencia de prefijo
hdr_dir([<name>[,<occ>]]): coincidencia de subdirectorio
hdr_dom([<name>[,<occ>]]): coincidencia de dominio
hdr_end([<name>[,<occ>]]): coincidencia de sufijo
hdr_len([<name>[,<occ>]]): coincidencia de longitud
hdr_reg([<name>[,<occ>]]): coincidencia de expresión regular
hdr_sub([<name>[,<occ>]]): coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

<a id="entry-7-3-6-req-hdr-cnt-integer"></a>

**`req.hdr_cnt([<name>]): integer`**

```haproxy
req.hdr_cnt([<name>]): integer
hdr_cnt([<header>]): integer (deprecated)
```

Devuelve un valor entero que representa el número de apariciones del nombre de campo de cabecera de
solicitud `<name>`, o el número total de valores de campos de cabecera si no se especifica
`<name>`. Al igual que req.hdr(), cuenta cada parte del valor de la cabecera separada por comas. Si
se desea contar cabeceras de línea completa, debe usarse req.fhdr_cnt() en su lugar.

Con ACL, puede usarse para detectar la presencia, ausencia o abuso de una cabecera concreta, así
como para bloquear ataques de request smuggling rechazando solicitudes que contengan más de una de
ciertas cabeceras.

Consulta req.hdr() para más información sobre la coincidencia de cabeceras.

<a id="entry-7-3-6-req-hdr-ip-ip"></a>

**`req.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
req.hdr_ip([<name>[,<occ>]]): ip
hdr_ip([<name>[,<occ>]]): ip (deprecated)
```

Extrae la última aparición de la cabecera `<name>` en una solicitud HTTP, la convierte en una
dirección IPv4 o IPv6 y devuelve dicha dirección. Cuando se usa con ACL, se comprueban todas las
apariciones, y si se omite `<name>`, se comprueba cada valor de cada cabecera. El analizador se
adhiere estrictamente al formato descrito en el RFC7239, con la extensión de que las direcciones
IPv4 pueden ir seguidas opcionalmente de dos puntos (':') y un número de puerto decimal válido (de 0
a 65535), que se descartará silenciosamente. Todas las demás formas no coincidirán y provocarán que
la dirección se ignore.

El parámetro `<occ>` se procesa como en req.hdr().

Un uso típico es con las cabeceras X-Forwarded-For y X-Client-IP.

<a id="entry-7-3-6-req-hdr-names-string"></a>

**`req.hdr_names([<delim>]): string`**

```haproxy
req.hdr_names([<delim>]): string
```

Construye una cadena formada por la concatenación de todos los nombres de cabecera tal como
aparecen en la solicitud cuando se evalúa la regla. El delimitador por defecto es la coma (','),
pero puede sobrescribirse como argumento opcional `<delim>`. En este caso, solo se considera el
primer carácter de `<delim>`.

<a id="entry-7-3-6-req-hdr-val-integer"></a>

**`req.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
req.hdr_val([<name>[,<occ>]]): integer
hdr_val([<name>[,<occ>]]): integer (deprecated)
```

Extrae la última aparición de la cabecera `<name>` en una solicitud HTTP y la convierte en un valor
entero. Cuando se usa con ACL, se comprueban todas las apariciones, y si se omite `<name>`, se
comprueba cada valor de cada cabecera.

El parámetro `<occ>` se procesa como en req.hdr().

Un uso típico es con la cabecera X-Forwarded-For.

req.hdrs: string Devuelve las cabeceras de solicitud actuales como cadena, incluida la última línea
vacía que separa las cabeceras del cuerpo de la solicitud. La última línea vacía puede usarse para
detectar un bloque de cabeceras truncado. Esta obtención de muestra es útil para algunos
analizadores de cabeceras SPOE y para el registro avanzado.

req.hdrs_bin: binary Devuelve las cabeceras de solicitud actuales contenidas en forma binaria
preanalizada. Esto es útil para descargar cierto procesamiento con SPOE. Cada cadena se describe
mediante una longitud seguida del número de bytes indicado en la longitud. La longitud se representa
usando la codificación de entero variable detallada en la documentación de SPOE. El final de la
lista está marcado por un par de nombres y valores de cabecera vacíos (longitud 0 para ambos).

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: consulta la documentación de SPOE para la codificación str: ``` <int:length>``<bytes> ```

req.timer.hdr: integer Tiempo total para obtener la solicitud del cliente (solo en modo HTTP). Es el
tiempo transcurrido entre la recepción de los primeros bytes y el momento en que el proxy recibió la
línea vacía que marca el final de las cabeceras HTTP. Se expresa en milisegundos (ms) y equivale a
%TR en el formato de registro. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
detalles.

req.timer.idle: integer Es el tiempo de inactividad antes de la solicitud HTTP (solo en modo HTTP).
Este temporizador cuenta entre el final de los handshakes y el primer byte de la solicitud HTTP. Se
expresa en milisegundos y equivale a %Ti en el formato de registro. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
detalles.

req.timer.queue: integer Tiempo total pasado en las colas esperando un hueco de conexión. Se expresa
en milisegundos y equivale a %Tw en el formato de registro. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para
más detalles.

req.timer.tq: integer Tiempo total para obtener la solicitud del cliente desde la fecha de
aceptación o desde la emisión del último byte de la respuesta anterior. Se expresa en milisegundos y
equivale a %Tq en el formato de registro. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
detalles.

req.ver: string req_ver: string (obsoleto) Devuelve la cadena de versión de la solicitud HTTP, con
el formato "`<major>`.`<minor>`". Esto puede ser útil para las ACL. Algunas ACL predefinidas ya
comprueban las versiones comunes. Puede usarse tanto en la solicitud, como en la respuesta y en los
registros, porque se basa en una información persistente. Si la versión de la solicitud no es
válida, esta obtención de muestra falla.

Los valores comunes son "1.0", "1.1", "2.0" o "3.0".

Derivadas de ACL:

```text
req.ver: coincidencia exacta de cadena
```

<a id="entry-7-3-6-request-date-integer"></a>

**`request_date([<unit>]): integer`**

```haproxy
request_date([<unit>]): integer
```

Esta es la fecha exacta en que HAProxy recibió el primer byte de la solicitud HTTP (alias %tr en el
formato de registro). Se calcula como accept_date + tiempo de handshake (%Th) + tiempo de
inactividad (%Ti).

Devuelve un valor en número de segundos desde epoch.

`<unit>` es facultativo y puede establecerse a "s" para segundos (comportamiento por defecto), "ms"
para milisegundos o "us" para microsegundos. Si se establece la unidad, el valor devuelto es un
entero que refleja segundos, milisegundos o microsegundos desde epoch. Es útil cuando se necesita
una resolución temporal inferior a un segundo.

res.body: binary Devuelve el cuerpo disponible de la respuesta HTTP como un bloque de datos. A
diferencia del lado de la solicitud, no existe ninguna directiva para esperar el cuerpo de la
respuesta. Esta obtención de muestra es realmente útil (y utilizable) en el contexto de las
comprobaciones de estado.

Puede usarse en reglas expect basadas en tcp-check.

res.body_len: integer Devuelve la longitud del cuerpo disponible de la respuesta HTTP en bytes. A
diferencia del lado de la solicitud, no existe ninguna directiva para esperar el cuerpo de la
respuesta. Esta obtención de muestra es realmente útil (y utilizable) en el contexto de las
comprobaciones de estado.

Puede usarse en reglas expect basadas en tcp-check.

res.body_size: integer Devuelve la longitud anunciada del cuerpo de la respuesta HTTP en bytes.
Representará la cabecera Content-Length anunciada, o el tamaño de los datos disponibles en caso de
codificación por fragmentos. A diferencia del lado de la solicitud, no existe ninguna directiva para
esperar el cuerpo de la respuesta. Esta obtención de muestra es realmente útil (y utilizable) en el
contexto de las comprobaciones de estado.

Puede usarse en reglas expect basadas en tcp-check.

res.cache_hit: boolean Devuelve el valor booleano "true" si la respuesta se ha construido a partir
de una entrada de la caché HTTP; en caso contrario devuelve el booleano "false".

res.cache_name: string Devuelve una cadena que contiene el nombre de la caché HTTP utilizada para
construir la respuesta HTTP si res.cache_hit es true; en caso contrario devuelve una cadena vacía.

res.comp: boolean Devuelve el valor booleano "true" si la respuesta ha sido comprimida por HAProxy;
en caso contrario devuelve el booleano "false". Esto puede usarse para añadir información en los
registros.

res.comp_algo: string Devuelve una cadena que contiene el nombre del algoritmo utilizado si la
respuesta fue comprimida por HAProxy, por ejemplo: "deflate". Esto puede usarse para añadir alguna
información en los registros.

<a id="entry-7-3-6-res-cook-string"></a>

**`res.cook([<name>]): string`**

```haproxy
res.cook([<name>]): string
scook([<name>]): string (deprecated)
```

Extrae la última aparición del nombre de cookie `<name>` en una línea de cabecera "Set-Cookie" de la
respuesta, y devuelve su valor como cadena. Si no se especifica ningún nombre, se devuelve el valor
de la primera cookie.

Puede usarse en reglas expect basadas en tcp-check.

Derivadas de ACL:

```text
res.scook([<name>]: coincidencia exacta de cadena
```

<a id="entry-7-3-6-res-cook-cnt-integer"></a>

**`res.cook_cnt([<name>]): integer`**

```haproxy
res.cook_cnt([<name>]): integer
scook_cnt([<name>]): integer (deprecated)
```

Devuelve un valor entero que representa el número de apariciones de la cookie `<name>` en la
respuesta, o de todas las cookies si no se especifica `<name>`. Esto es especialmente útil cuando se
combina con ACL para detectar respuestas sospechosas.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-cook-names-string"></a>

**`res.cook_names([<delim>]): string`**

```haproxy
res.cook_names([<delim>]): string
```

Construye una cadena formada por la concatenación de todos los nombres de cookies tal como aparecen
en la respuesta (cabeceras Set-Cookie) cuando se evalúa la regla. El delimitador por defecto es la
coma (','), pero puede sobrescribirse como argumento opcional `<delim>`. En este caso, solo se
considera el primer carácter de `<delim>`.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-cook-val-integer"></a>

**`res.cook_val([<name>]): integer`**

```haproxy
res.cook_val([<name>]): integer
scook_val([<name>]): integer (deprecated)
```

Extrae la última aparición del nombre de cookie `<name>` en una línea de cabecera "Set-Cookie" de la
respuesta, y convierte su valor en un entero que se devuelve. Si no se especifica ningún nombre, se
devuelve el valor de la primera cookie.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-fhdr-string"></a>

**`res.fhdr([<name>[,<occ>]]): string`**

```haproxy
res.fhdr([<name>[,<occ>]]): string
```

Esta obtención funciona como la de req.fhdr(), con la diferencia de que actúa sobre las cabeceras de
una respuesta HTTP.

Al igual que req.fhdr(), la obtención res.fhdr() devuelve valores completos. Si la cabecera está
definida como una lista, deberías usar res.hdr().

Esta obtención a veces resulta útil con cabeceras como Date o Expires.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-fhdr-cnt-integer"></a>

**`res.fhdr_cnt([<name>]): integer`**

```haproxy
res.fhdr_cnt([<name>]): integer
```

Esta obtención funciona como la de req.fhdr_cnt(), con la diferencia de que actúa sobre las
cabeceras de una respuesta HTTP.

Al igual que req.fhdr_cnt(), la obtención res.fhdr_cnt() actúa sobre valores completos. Si la
cabecera está definida como una lista, deberías usar res.hdr_cnt().

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-hdr-string"></a>

**`res.hdr([<name>[,<occ>]]): string`**

```haproxy
res.hdr([<name>[,<occ>]]): string
shdr([<name>[,<occ>]]): string (deprecated)
```

Esta obtención funciona como la de req.hdr(), con la diferencia de que actúa sobre las cabeceras de
una respuesta HTTP.

Al igual que req.hdr(), la obtención res.hdr() considera la coma como un delimitador. Si esto no es
lo deseado, debe usarse res.fhdr().

Puede usarse en reglas expect basadas en tcp-check.

Derivadas de ACL:

```text
res.hdr([<name>[,<occ>]])    : coincidencia exacta de cadena
res.hdr_beg([<name>[,<occ>]]): coincidencia de prefijo
res.hdr_dir([<name>[,<occ>]]): coincidencia de subdirectorio
res.hdr_dom([<name>[,<occ>]]): coincidencia de dominio
res.hdr_end([<name>[,<occ>]]): coincidencia de sufijo
res.hdr_len([<name>[,<occ>]]): coincidencia de longitud
res.hdr_reg([<name>[,<occ>]]): coincidencia de expresión regular
res.hdr_sub([<name>[,<occ>]]): coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

<a id="entry-7-3-6-res-hdr-cnt-integer"></a>

**`res.hdr_cnt([<name>]): integer`**

```haproxy
res.hdr_cnt([<name>]): integer
shdr_cnt([<name>]): integer (deprecated)
```

Esta obtención funciona como la de req.hdr_cnt(), con la diferencia de que actúa sobre las cabeceras
de una respuesta HTTP.

Al igual que req.hdr_cnt(), la obtención res.hdr_cnt() considera la coma como un delimitador. Si
esto no es lo deseado, debe usarse res.fhdr_cnt().

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-hdr-ip-ip"></a>

**`res.hdr_ip([<name>[,<occ>]]): ip`**

```haproxy
res.hdr_ip([<name>[,<occ>]]): ip
shdr_ip([<name>[,<occ>]]): ip (deprecated)
```

Esta obtención funciona como la de req.hdr_ip(), con la diferencia de que actúa sobre las cabeceras
de una respuesta HTTP.

Esto puede ser útil para aprender algunos datos en una tabla de persistencia.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-hdr-names-string"></a>

**`res.hdr_names([<delim>]): string`**

```haproxy
res.hdr_names([<delim>]): string
```

Construye una cadena formada por la concatenación de todos los nombres de cabecera tal como aparecen
en la respuesta cuando se evalúa la regla. El delimitador por defecto es la coma (','), pero puede
sobrescribirse como argumento opcional `<delim>`. En este caso, solo se considera el primer carácter
de `<delim>`.

Puede usarse en reglas expect basadas en tcp-check.

<a id="entry-7-3-6-res-hdr-val-integer"></a>

**`res.hdr_val([<name>[,<occ>]]): integer`**

```haproxy
res.hdr_val([<name>[,<occ>]]): integer
shdr_val([<name>[,<occ>]]): integer (deprecated)
```

Esta obtención funciona como la de req.hdr_val(), con la diferencia de que actúa sobre las cabeceras
de una respuesta HTTP.

Esto puede ser útil para aprender algunos datos en una tabla de persistencia.

Puede usarse en reglas expect basadas en tcp-check.

res.hdrs: string Devuelve las cabeceras de respuesta actuales como cadena, incluida la última línea
vacía que separa las cabeceras del cuerpo de la solicitud. La última línea vacía puede usarse para
detectar un bloque de cabeceras truncado. Esta obtención de muestra es útil para algunos
analizadores de cabeceras SPOE y para el registro avanzado.

También puede usarse en reglas expect basadas en tcp-check.

res.hdrs_bin: binary Devuelve las cabeceras de respuesta actuales contenidas en forma binaria
preanalizada. Esto es útil para descargar cierto procesamiento con SPOE. Puede usarse en reglas
expect basadas en tcp-check. Cada cadena se describe mediante una longitud seguida del número de
bytes indicado en la longitud. La longitud se representa usando la codificación de entero variable
detallada en la documentación de SPOE. El final de la lista está marcado por un par de nombres y
valores de cabecera vacíos (longitud 0 para ambos).

\*(``` <str:header-name>``<str:header-value> ```)``` <empty string>``<empty string> ```

int: consulta la documentación de SPOE para la codificación str: ``` <int:length>``<bytes> ```

res.timer.hdr: integer Es el tiempo transcurrido entre el momento en que se estableció la conexión
TCP con el servidor y el momento en que el servidor envió sus cabeceras de respuesta completas. Se
expresa en milisegundos y equivale a %Tr en el formato de registro. Consulta la [sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización» para más
detalles.

res.ver: string resp_ver: string (obsoleto) Devuelve la cadena de versión de la respuesta HTTP, con
el formato "`<major>`.`<minor>`". Esto puede ser útil para los registros, pero existe sobre todo
para las ACL. Si la versión de la respuesta no es válida, esta obtención de muestra falla.

Puede usarse en reglas expect basadas en tcp-check.

Derivadas de ACL:

```text
resp.ver: coincidencia exacta de cadena
```

server_status: integer Devuelve un entero que contiene el código de estado HTTP tal como se recibió
del servidor. Si no se recibió ninguna respuesta del servidor, la obtención de muestra falla.

<a id="entry-7-3-6-set-cookie-string"></a>

**`set-cookie([<name>]): string (deprecated)`**

```haproxy
set-cookie([<name>]): string (deprecated)
```

Extrae la última aparición del nombre de cookie `<name>` en una línea de cabecera "Set-Cookie" de la
respuesta y usa el valor correspondiente para la coincidencia. Esto puede compararse con lo que
hacía "appsession" con las opciones por defecto, pero con soporte para la sincronización entre
múltiples pares y la conservación del estado entre reinicios.

Esta función de obtención está obsoleta y ha sido sustituida por la obtención "res.cook". Esta
palabra clave desaparecerá pronto.

status: integer Devuelve un entero que contiene el código de estado HTTP en la respuesta HTTP, por
ejemplo, 302. Se usa principalmente dentro de ACL y rangos de enteros, por ejemplo, para eliminar
cualquier cabecera Location si la respuesta no es una 3xx. Será el código de estado recibido por el
cliente si no se cambia, por ejemplo mediante una acción 'set-status'.

Puede usarse en reglas expect basadas en tcp-check.

txn.status: integer Devuelve un entero que contiene el código de estado HTTP de la transacción,
tal como se informa en el registro.

txn.timer.total: integer Tiempo activo total de la solicitud HTTP, entre el momento en que el proxy
recibió el primer byte de la cabecera de la solicitud y la emisión del último byte del cuerpo de la
respuesta. Es el equivalente de %Ta en el formato de registro y se expresa en milisegundos (ms).
Para más información, consulta la [Sección 8.4](/es/haproxy/configuration-logging/#section-8-4) «Eventos de temporización»

unique-id: string Devuelve el unique-id asociado a la solicitud. La directiva "unique-id-format"
debe estar establecida. Si no lo está, la obtención de muestra unique-id falla. Ten en cuenta que el
unique-id se usa normalmente con solicitudes HTTP; sin embargo, esta obtención de muestra puede
usarse con otros protocolos. Obviamente, si se usa con protocolos distintos de HTTP, la directiva
unique-id-format no debe contener partes HTTP. Consulta: unique-id-format y unique-id-header

url: string Extrae la URL de la solicitud tal como se presenta en la solicitud. Un uso típico es
con cachés capaces de precarga, y con portales que necesitan agregar información múltiple de bases
de datos y mantenerla en cachés. Con ACL, se prefiere usar "path" antes que "url", porque los
clientes pueden enviar una URL completa, como se hace normalmente con los proxys. El único uso real
es coincidir con "\*", que no coincide en "path", y para el cual ya existe una ACL predefinida.
Consulta también "path" y "base". Ten en cuenta que cualquier referencia a un fragmento en el URI ('#' tras
la ruta) está estrictamente prohibida por el estándar HTTP y será rechazada. Sin embargo, si el
frontend que recibe la solicitud tiene "option accept-unsafe-violations-in-http-request", entonces
esta parte del fragmento será aceptada y también aparecerá en la url.

Derivadas de ACL:

```text
url    : coincidencia exacta de cadena
url_beg: coincidencia de prefijo
url_dir: coincidencia de subdirectorio
url_dom: coincidencia de dominio
url_end: coincidencia de sufijo
url_len: coincidencia de longitud
url_reg: coincidencia de expresión regular
url_sub: coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

url32: integer Devuelve un hash de 32 bits del valor obtenido al concatenar la primera cabecera
Host y la URL completa incluidos los parámetros (no solo la parte de la ruta de la solicitud, como
en la obtención "base32" anterior). Esto es útil para rastrear la actividad por URL. Se almacena un
hash más corto, lo que ahorra mucha memoria. El tipo de salida es un entero sin signo.

url32+src: binary Devuelve la concatenación de la obtención "url32" y la obtención "src". El tipo
resultante es de tipo binario, con un tamaño de 8 o 20 bytes según la familia de la dirección de
origen. Esto puede usarse para rastrear contadores por IP y por URL.

url_ip: ip Extrae la dirección IP de la URL de la solicitud cuando la parte del host se presenta
como una dirección IP. La obtención falla cuando la parte del host es un nombre, ya que no se
realiza ninguna resolución. Su uso es muy limitado. Por ejemplo, un sistema de monitorización
podría usar este campo como alternativa a la IP de origen para probar qué ruta seguiría una
dirección de origen dada, o para forzar una entrada en una tabla para una dirección de origen dada.
Puede usarse en combinación con 'http-request set-dst' para emular la antigua 'option http_proxy'.

url_port: integer Extrae la parte del puerto de la URL de la solicitud. Ten en cuenta que si el puerto no
se especifica en la solicitud, se asume el puerto 80. Al igual que con "url_ip", esto solo funciona
cuando la autoridad de la URL se presenta como una dirección; la obtención falla cuando se trata de
un nombre de host, ya que aquí no se realiza ninguna resolución.

<a id="entry-7-3-6-urlp-string"></a>

**`urlp([<name>[,<delim>[,i]]]): string`**

```haproxy
urlp([<name>[,<delim>[,i]]]): string
url_param([<name>[,<delim>[,i]]]): string
```

Extrae la primera aparición del parámetro `<name>` en la cadena de consulta, que comienza después
de '?' o de `<delim>`, y que termina antes de '&', ';' o `<delim>`. El nombre del parámetro
distingue entre mayúsculas y minúsculas, salvo que se añada "i" como tercer argumento. Si no se
indica ningún nombre, cualquier parámetro coincidirá y se devolverá el primero. El resultado es una
cadena correspondiente al valor del parámetro `<name>` tal como se presenta en la solicitud (no se
realiza ninguna decodificación de URL). Esto puede usarse para la persistencia de sesión basada en
un ID de cliente, para extraer una cookie de aplicación pasada como parámetro de URL, o en ACL para
aplicar algunas comprobaciones. Ten en cuenta que la versión ACL de esta obtención itera sobre múltiples
parámetros e informará iterativamente de los valores de todos los parámetros si no se indica ningún
nombre

Derivadas de ACL:

```text
urlp(<name>[,<delim>])    : coincidencia exacta de cadena
urlp_beg(<name>[,<delim>]): coincidencia de prefijo
urlp_dir(<name>[,<delim>]): coincidencia de subdirectorio
urlp_dom(<name>[,<delim>]): coincidencia de dominio
urlp_end(<name>[,<delim>]): coincidencia de sufijo
urlp_len(<name>[,<delim>]): coincidencia de longitud
urlp_reg(<name>[,<delim>]): coincidencia de expresión regular
urlp_sub(<name>[,<delim>]): coincidencia de subcadena
```

Nota: las derivadas de ACL no deben usarse seguidas de un conversor ni en ACL con un método de
coincidencia de patrones "-m".

Ejemplo:

```shell
# match http://example.com/foo?PHPSESSIONID=some_id
stick on urlp(PHPSESSIONID)
# match http://example.com/foo;JSESSIONID=some_id
stick on urlp(JSESSIONID,;)
```

<a id="entry-7-3-6-urlp-val-integer"></a>

**`urlp_val([<name>[,<delim>[,i]]]): integer`**

```haproxy
urlp_val([<name>[,<delim>[,i]]]): integer
```

Consulta "urlp" más arriba. Esta extrae el parámetro de URL `<name>` de la solicitud y lo convierte en
un valor entero. Esto puede usarse, por ejemplo, para la persistencia de sesión basada en un ID de
usuario, o con ACL para coincidir con un número de página o un precio.

### 7.3.7. Obtención de muestras para desarrolladores {#section-7-3-7}

Este conjunto de métodos de obtención de muestras está reservado a los desarrolladores y nunca debe
usarse en un entorno de producción, salvo a petición del desarrollador, con fines de depuración.
Además, no se prestará especial atención a la compatibilidad con versiones anteriores. No hay
garantía de que las siguientes obtenciones de muestras no cambien, se renombren o simplemente se
eliminen. Así que sé realmente cuidadoso si tienes que usar una de ellas. Para evitar cualquier
ambigüedad, estas obtenciones de muestras se colocan en el ámbito dedicado "internal"; por ejemplo,
"internal.strm.is_htx".

Resumen de los métodos de obtención de muestras de esta sección y sus respectivos tipos:

```text
  palabra clave                                    tipo de salida
-------------------------------------------------+-------------
internal.htx.data                                  integer
internal.htx.free                                  integer
internal.htx.free_data                             integer
internal.htx.has_eom                               boolean
internal.htx.nbblks                                integer
internal.htx.size                                  integer
internal.htx.used                                  integer
internal.htx_blk.size(<idx>)                       integer
internal.htx_blk.type(<idx>)                       string
internal.htx_blk.data(<idx>)                       binary
internal.htx_blk.hdrname(<idx>)                    string
internal.htx_blk.hdrval(<idx>)                     string
internal.htx_blk.start_line(<idx>)                 string
internal.strm.is_htx                               boolean
-------------------------------------------------+-------------
```

Lista detallada:

internal.htx.data: integer Devuelve el tamaño en bytes usado por los datos en el mensaje HTX
asociado a un canal. El canal se elige según la dirección de la muestra.

internal.htx.free: integer Devuelve el espacio libre (size - used) en bytes en el mensaje HTX
asociado a un canal. El canal se elige según la dirección de la muestra.

internal.htx.free_data: integer Devuelve el espacio libre para los datos en bytes en el mensaje HTX
asociado a un canal. El canal se elige según la dirección de la muestra.

internal.htx.has_eom: boolean Devuelve true si el mensaje HTX asociado a un canal contiene el
indicador de fin de mensaje (EOM). En caso contrario, devuelve false. El canal se elige según la
dirección de la muestra.

internal.htx.nbblks: integer Devuelve el número de bloques presentes en el mensaje HTX asociado a
un canal. El canal se elige según la dirección de la muestra.

internal.htx.size: integer Devuelve el tamaño total en bytes del mensaje HTX asociado a un canal.
El canal se elige según la dirección de la muestra.

internal.htx.used: integer Devuelve el tamaño total usado en bytes (datos + metadatos) en el
mensaje HTX asociado a un canal. El canal se elige según la dirección de la muestra.

<a id="entry-7-3-7-internal-htx-blk-size-integer"></a>

**`internal.htx_blk.size(<idx>): integer`**

```haproxy
internal.htx_blk.size(<idx>): integer
```

Devuelve el tamaño del bloque en la posición `<idx>` en el mensaje HTX asociado a un canal, o 0 si
no existe. El canal se elige según la dirección de la muestra. `<idx>` puede ser cualquier entero
positivo o uno de los valores especiales: \* head : El bloque insertado más antiguo \* tail : El
bloque insertado más reciente \* first: El primer bloque por donde (re)iniciar el análisis

<a id="entry-7-3-7-internal-htx-blk-type-string"></a>

**`internal.htx_blk.type(<idx>): string`**

```haproxy
internal.htx_blk.type(<idx>): string
```

Devuelve el tipo del bloque en la posición `<idx>` en el mensaje HTX asociado a un canal, o
"HTX_BLK_UNUSED" si no existe. El canal se elige según la dirección de la muestra. `<idx>` puede
ser cualquier entero positivo o uno de los valores especiales: \* head : El bloque insertado más
antiguo \* tail : El bloque insertado más reciente \* first: El primer bloque por donde (re)iniciar
el análisis

<a id="entry-7-3-7-internal-htx-blk-data-binary"></a>

**`internal.htx_blk.data(<idx>): binary`**

```haproxy
internal.htx_blk.data(<idx>): binary
```

Devuelve el valor del bloque DATA en la posición `<idx>` en el mensaje HTX asociado a un canal, o
una cadena vacía si no existe o si no es un bloque DATA. El canal se elige según la dirección de la
muestra. `<idx>` puede ser cualquier entero positivo o uno de los valores especiales:

    * head : El bloque insertado más antiguo
    * tail : El bloque insertado más reciente
    * first: El primer bloque a partir del cual (re)iniciar el análisis

<a id="entry-7-3-7-internal-htx-blk-hdrname-string"></a>

**`internal.htx_blk.hdrname(<idx>): string`**

```haproxy
internal.htx_blk.hdrname(<idx>): string
```

Devuelve el nombre de cabecera del bloque HEADER en la posición `<idx>` en el mensaje HTX asociado
a un canal, o una cadena vacía si no existe o si no es un bloque HEADER. El canal se elige según la
dirección de la muestra. `<idx>` puede ser cualquier entero positivo o uno de los valores
especiales:

    * head : El bloque insertado más antiguo
    * tail : El bloque insertado más reciente
    * first: El primer bloque a partir del cual (re)iniciar el análisis

<a id="entry-7-3-7-internal-htx-blk-hdrval-string"></a>

**`internal.htx_blk.hdrval(<idx>): string`**

```haproxy
internal.htx_blk.hdrval(<idx>): string
```

Devuelve el valor de cabecera del bloque HEADER en la posición `<idx>` en el mensaje HTX asociado a
un canal, o una cadena vacía si no existe o si no es un bloque HEADER. El canal se elige según la
dirección de la muestra. `<idx>` puede ser cualquier entero positivo o uno de los valores
especiales:

    * head : El bloque insertado más antiguo
    * tail : El bloque insertado más reciente
    * first: El primer bloque a partir del cual (re)iniciar el análisis

<a id="entry-7-3-7-internal-htx-blk-start-line-string"></a>

**`internal.htx_blk.start_line(<idx>): string`**

```haproxy
internal.htx_blk.start_line(<idx>): string
```

Devuelve el valor del bloque REQ_SL o RES_SL en la posición `<idx>` en el mensaje HTX asociado a un
canal, o una cadena vacía si no existe o si no es un bloque SL. El canal se elige según la dirección
de la muestra. `<idx>` puede ser cualquier entero positivo o uno de los valores especiales:

    * head : El bloque insertado más antiguo
    * tail : El bloque insertado más reciente
    * first: El primer bloque a partir del cual (re)iniciar el análisis

internal.strm.is_htx: boolean Devuelve true si el flujo actual es un flujo HTX. Esto significa que
los datos de los búferes de los canales se almacenan usando la representación interna HTX. En caso
contrario, devuelve false.

## 7.4. ACL predefinidas {#section-7-4}

Algunas ACL predefinidas están codificadas de forma fija para que no haya que declararlas en cada
frontend que las necesite. Todas tienen sus nombres en mayúsculas para evitar confusiones. Su
equivalencia se proporciona a continuación.

```text
Nombre de ACL          Equivale a                Uso
---------------+----------------------------------+------------------------------------------------------
FALSE            always_false                       nunca coincide
HTTP             req.proto_http                     coincide si el protocolo de la solicitud es HTTP válido
HTTP_1.0         req.ver 1.0                        coincide si la versión de la solicitud HTTP es 1.0
HTTP_1.1         req.ver 1.1                        coincide si la versión de la solicitud HTTP es 1.1
HTTP_2.0         req.ver 2.0                        coincide si la versión de la solicitud HTTP es 2.0
HTTP_3.0         req.ver 3.0                        coincide si la versión de la solicitud HTTP es 3.0
HTTP_CONTENT     req.hdr_val(content-length) gt 0   coincide con un content-length existente en la solicitud HTTP
HTTP_URL_ABS     url_reg ^[^/:]*://                 coincide con una URL absoluta con esquema
HTTP_URL_SLASH   url_beg /                          coincide con una URL que comienza por "/"
HTTP_URL_STAR    url     *                          coincide con una URL igual a "*"
LOCALHOST        src 127.0.0.1/8::1                coincide con una conexión desde el host local
METH_CONNECT     method  CONNECT                    coincide con el método HTTP CONNECT
METH_DELETE      method  DELETE                     coincide con el método HTTP DELETE
METH_GET         method  GET HEAD                   coincide con el método HTTP GET o HEAD
METH_HEAD        method  HEAD                       coincide con el método HTTP HEAD
METH_OPTIONS     method  OPTIONS                    coincide con el método HTTP OPTIONS
METH_POST        method  POST                       coincide con el método HTTP POST
METH_PUT         method  PUT                        coincide con el método HTTP PUT
METH_TRACE       method  TRACE                      coincide con el método HTTP TRACE
RDP_COOKIE       req.rdp_cookie_cnt gt 0            coincide con la presencia de una cookie RDP en el búfer de solicitud
REQ_CONTENT      req.len gt 0                       coincide con datos en el búfer de solicitud
TRUE             always_true                        coincide siempre
WAIT_END         wait_end                           espera el final del análisis de contenido
---------------+----------------------------------+------------------------------------------------------
```
