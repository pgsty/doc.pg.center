---
title: "9. Filtros admitidos"
linkTitle: "9. Filtros"
weight: 200
description: "Filtros de trace, compresión, SPOE, caché, FastCGI, OpenTracing y ancho de banda"
icon: fa-solid fa-layer-group
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/filters/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 9"
---

A continuación se enumeran los filtros oficialmente admitidos junto con la lista de parámetros que
aceptan. Dependiendo de las opciones de compilación, algunos de estos filtros podrían no estar
disponibles. La lista de filtros disponibles se muestra en haproxy -vv.

Consulta también: «filter»

## 9.1. Traza {#section-9-1}

filter trace [name `<name>`] [random-forwarding] [max-fwd `<max>`] [hexdump]

Argumentos:

```text
<name>               es un nombre arbitrario que se mostrará en los
                     mensajes. Si no se proporciona ningún nombre, se
                     utiliza «TRACE».

<quiet>              suprime los mensajes de trace.

<random-forwarding>  activa el reenvío aleatorio de los datos analizados.
                     Por defecto, este filtro reenvía todos los datos ya
                     analizados. Con este parámetro, solo reenvía una
                     cantidad aleatoria de los datos analizados.

<max>                es la cantidad máxima de datos que pueden reenviarse
                     a la vez. La opción «max-fwd» puede combinarse con el
                     reenvío aleatorio. <max> debe ser un entero positivo.
                     0 significa que no hay límite.

<hexdump>             vuelca todos los datos reenviados hacia el servidor
                     y hacia el cliente.
```

Este filtro puede utilizarse como base para desarrollar nuevos filtros. Define todas las
retrollamadas (callbacks) e imprime un mensaje en el flujo de error estándar (stderr) con
información útil para cada una de ellas. Puede ser útil para depurar la actividad de otros filtros
o, simplemente, la actividad de HAProxy.

Usar los parámetros `<random-parsing>` y/o `<random-forwarding>` es una buena manera de probar el
comportamiento de un filtro que analiza datos intercambiados entre un cliente y un servidor
añadiendo algunas latencias en el procesamiento.

## 9.2. Compresión HTTP {#section-9-2}

filter comp-req

Activa el filtro que intenta explícitamente comprimir las solicitudes HTTP según los parámetros
«compression». Define implícitamente «compression direction request».

filter comp-res

Activa el filtro que intenta explícitamente comprimir las respuestas HTTP según los parámetros
«compression». Define implícitamente «compression direction response»

filter compression (obsoleto)

Alias con fines de compatibilidad con versiones anteriores, funcionalmente equivalente a activar
tanto el filtro «comp-req» como el «comp-res». La palabra clave «compression» debe utilizarse para
configurar el comportamiento adecuado:

La compresión HTTP se trasladó a un filtro en HAProxy 1.7. La palabra clave «compression» debe
seguir utilizándose para activar y configurar la compresión HTTP. Y cuando no se utiliza ningún otro
filtro, es suficiente. Cuando se usa con la caché o con fcgi-app activados, también es suficiente.
En este caso, la compresión siempre se realiza después de que la respuesta se almacene en la caché.
Pero es obligatorio usar explícitamente una línea de filtro para activar la compresión HTTP cuando
se utiliza al menos un filtro distinto de la caché o de fcgi-app para el mismo
listener/frontend/backend. Esto es importante para conocer el orden de evaluación de los filtros.

Consulta también: «compression», la [sección 9.4](/es/haproxy/filters/#section-9-4) sobre el filtro de
caché y la [sección 9.5](/es/haproxy/filters/#section-9-5) sobre el filtro fcgi-app.

## 9.3. Motor de descarga de procesamiento de flujos (SPOE) {#section-9-3}

filter spoe [engine `<name>`] config `<file>`

Argumentos:

```text
<name>      es el nombre del motor que se utilizará para encontrar el
            ámbito correcto en el archivo de configuración. Si no se
            proporciona, se analizará el archivo completo.

<file>      es la ruta del archivo de configuración del motor. Este
            archivo puede contener la configuración de varios motores.
            En ese caso, cada parte debe colocarse en su propio ámbito.
```

El motor de descarga de procesamiento de flujos (SPOE) es un filtro que se comunica con componentes
externos. Permite descargar ciertos procesamientos específicos sobre los flujos en aplicaciones por
niveles. Estos componentes externos y la información intercambiada con ellos se configuran, en su
mayor parte, en archivos dedicados. También requiere backends dedicados, definidos en la
configuración de HAProxy.

SPOE se comunica con los componentes externos mediante un protocolo binario propio, el Stream
Processing Offload Protocol (SPOP).

Cuando se utiliza el SPOE en un flujo, se genera un flujo dedicado para gestionar la comunicación
con el componente externo. El flujo principal es el flujo padre de este flujo «SPOE». Esto significa
que es posible recuperar variables del flujo principal desde el flujo «SPOE». Consulta la
[sección 2.8](/es/haproxy/configuration-basics/#section-2-8) sobre las variables para más detalles.

Para toda la información sobre la configuración de SPOE y la especificación de SPOP, consulta
«doc/SPOE.txt».

## 9.4. Caché {#section-9-4}

filter cache `<name>`

Argumentos:

```text
<name>      es el nombre de la sección cache que utilizará este filtro.
```

La caché utiliza un filtro para almacenar las respuestas que pueden almacenarse en caché. Las
reglas HTTP «cache-store» y «cache-use» deben utilizarse para definir cómo y cuándo usar una caché.
Por defecto, el filtro correspondiente queda definido implícitamente. Y cuando no se usan otros
filtros más que fcgi-app o compression, es suficiente. En tal caso, el filtro de compresión siempre
se evalúa después del filtro de caché. Pero es obligatorio usar explícitamente una línea de filtro
para usar una caché cuando se utiliza al menos un filtro distinto de compression o fcgi-app para el
mismo listener/frontend/backend. Esto es importante para conocer el orden de evaluación de los
filtros.

Consulta también: la [sección 9.2](/es/haproxy/filters/#section-9-2) sobre el filtro de compresión, la
[sección 9.5](/es/haproxy/filters/#section-9-5) sobre el filtro fcgi-app y la
[sección 6](/es/haproxy/cache/) sobre la caché.

## 9.5. Fcgi-app {#section-9-5}

filter fcgi-app `<name>`

Argumentos:

```text
<name>      es el nombre de la sección fcgi-app que utilizará este filtro.
```

La aplicación FastCGI utiliza un filtro para evaluar todos los parámetros personalizados en la ruta
de la solicitud y para procesar los encabezados en la ruta de la respuesta. `<name>` debe hacer
referencia a una sección fcgi-app existente. La directiva «use-fcgi-app» debería utilizarse para
definir la aplicación que se va a usar. Por defecto, el filtro correspondiente queda definido
implícitamente. Y cuando no se usan otros filtros más que cache o compression, es suficiente. Pero
es obligatorio usar explícitamente una línea de filtro para una fcgi-app cuando se utiliza al menos
un filtro distinto de compression o cache para el mismo backend. Esto es importante para conocer el
orden de evaluación de los filtros.

Consulta también: «use-fcgi-app», la [sección 9.2](/es/haproxy/filters/#section-9-2) sobre el filtro de
compresión, la [sección 9.4](/es/haproxy/filters/#section-9-4) sobre el filtro de caché y la
[sección 10](/es/haproxy/fastcgi/) sobre la aplicación FastCGI.

## 9.6. OpenTracing {#section-9-6}

El filtro OpenTracing añade compatibilidad nativa para utilizar el trazado distribuido en HAProxy.
Esto se activa enviando una solicitud conforme a OpenTracing a uno de los trazadores (tracers)
admitidos, como los trazadores Datadog, Jaeger, Lightstep y Zipkin. Ten en cuenta: los trazadores no
están listados por orden de preferencia, sino alfabéticamente.

Esta funcionalidad solo se activa cuando HAProxy se ha compilado con USE_OT=1.

La activación del filtro OpenTracing se realiza explícitamente al especificarlo en la configuración
de HAProxy. Si no se hace, el filtro OpenTracing no participa en absoluto en el trabajo de HAProxy.

filter opentracing [id `<id>`] config `<file>`

Argumentos:

```text
<id>        es el identificador del filtro OpenTracing que se utilizará
            para encontrar el ámbito correcto en el archivo de
            configuración. Si no se especifica ningún identificador de
            filtro, se utiliza «ot-filter» por defecto. Si no se
            especifica ningún ámbito en el archivo de configuración, se
            aplica a todos los filtros OpenTracing definidos.

<file>      es la ruta del archivo de configuración de OpenTracing. El
            mismo archivo puede contener configuraciones para varios
            filtros OpenTracing simultáneamente. En ese caso, no hace
            falta definir un ámbito si la misma configuración se aplica a
            todos los filtros, o bien cada filtro debe tener definido su
            propio ámbito.
```

Puede encontrarse documentación más detallada sobre el funcionamiento, la configuración y el uso del
filtro en el directorio addons/ot.

Nota: El filtro OpenTracing no debería utilizarse en nuevos diseños, ya que OpenTracing en sí ya no
recibe mantenimiento ni soporte de sus autores. Como tal, OpenTracing quedará obsoleto en 3.3 y se
eliminará en 3.5. Un filtro de reemplazo basado en OpenTelemetry está disponible desde 3.4, con
instrucciones de compilación completas actualmente en:

```text
https://github.com/haproxytech/haproxy-opentelemetry/
```

## 9.7. Limitación del ancho de banda {#section-9-7}

```haproxy
filter bwlim-in  <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-out <name> default-limit <size> default-period <time> [min-size <sz>]
filter bwlim-in  <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
filter bwlim-out <name> limit <size> key <pattern> [table <table>] [min-size <sz>]
```

Argumentos:

```text
<name>      es el nombre del filtro que utilizarán las acciones
            «set-bandwidth-limit» para hacer referencia a un filtro
            específico de limitación de ancho de banda.

<size>      es el número máximo de bytes que pueden reenviarse durante el
            periodo. El valor debe especificarse para los filtros de
            limitación de ancho de banda por flujo y compartidos. Sigue
            el formato de tamaño de HAProxy y se expresa en bytes.

<pattern>   es una regla de expresión de muestra como se describe en la
            sección 7.3. Describe qué elementos se analizarán, extraerán,
            combinarán y utilizarán para seleccionar la entrada de la
            tabla cuyos contadores se actualizarán. Debe especificarse
            únicamente para los filtros de limitación de ancho de banda
            compartidos.

<table>     es una tabla opcional que se utilizará en lugar de la
            predeterminada, que es la stick-table declarada en el proxy
            actual. Puede especificarse únicamente para los filtros de
            limitación de ancho de banda compartidos.

<time>      es el periodo de tiempo predeterminado que se utiliza para
            evaluar la tasa de limitación de ancho de banda. Puede
            especificarse únicamente para los filtros de limitación de
            ancho de banda por flujo. Sigue el formato de tiempo de
            HAProxy y se expresa en milisegundos.

<min-size>  es el número mínimo opcional de bytes reenviados a la vez por
            un flujo, excluyendo el último paquete, que puede ser más
            pequeño. Este valor puede especificarse para los filtros de
            limitación de ancho de banda por flujo y compartidos. Sigue
            el formato de tamaño de HAProxy y se expresa en bytes.
```

Los filtros de limitación de ancho de banda deberían utilizarse para restringir la velocidad de
reenvío de datos a nivel de flujo. Por extensión, dichos filtros limitan el ancho de banda de red
consumido por un recurso. Pueden utilizarse varios filtros de limitación de ancho de banda. Por
ejemplo, es posible definir un límite por dirección de origen para asegurarse de que un cliente
nunca consuma todo el ancho de banda de red, perjudicando así a otros clientes, y otro por flujo
para poder gestionar de forma equitativa varias conexiones de un mismo cliente.

El orden de definición de estos filtros es importante. Si se activan varios filtros de ancho de
banda en un flujo, el filtrado se aplicará en su orden de definición. También es importante entender
que el orden de definición de los otros filtros tiene influencia. Por ejemplo, dependiendo de si el
filtro de compresión HTTP se define antes o después de un filtro de limitación de ancho de banda, el
límite se aplicará o no sobre la carga comprimida. Lo mismo ocurre con el filtro de caché.

Existen dos tipos de filtros de limitación de ancho de banda. El primero impone un límite
predeterminado y se aplica por flujo. El segundo utiliza una tabla de persistencia (stick-table)
para imponer un límite dividido por igual entre todos los flujos que comparten la misma entrada en
la tabla.

Además, para un filtro dado, dependiendo de la palabra clave del filtro utilizada, la limitación
puede aplicarse a los datos entrantes, recibidos del cliente y reenviados a un servidor, o a los
datos salientes, recibidos de un servidor y enviados al cliente. Para aplicar un límite a los datos
entrantes debe utilizarse la palabra clave «bwlim-in». Para aplicarlo a los datos salientes debe
utilizarse la palabra clave «bwlim-out». En ambos casos, la limitación de ancho de banda se aplica a
los datos reenviados, a nivel de flujo.

La limitación de ancho de banda se aplica a nivel de flujo y no a nivel de conexión. Para los
protocolos multiplexados (H2, H3 y FastCGI), los flujos de la misma conexión pueden tener límites
diferentes.

Para un filtro de limitación de ancho de banda por flujo, deben definirse el periodo y el límite
predeterminados. Como sugieren sus nombres, son los valores predeterminados que se utilizan para
configurar la tasa de limitación de ancho de banda de un flujo. Sin embargo, para este tipo de
filtro, y solo para este, es posible redefinir estos valores mediante expresiones de muestra cuando
el filtro se activa con una acción TCP/HTTP «set-bandwidth-limit».

Para un filtro de limitación de ancho de banda compartido, dependiendo de si se aplica a los datos
entrantes o salientes, la tabla de persistencia utilizada debe almacenar la información de tasa de
bytes correspondiente. El contador «bytes_in_rate(`<period>`)» debe almacenarse para limitar los
datos entrantes y el contador «bytes_out_rate(`<period>`)» debe utilizarse para limitar los datos
salientes.

Finalmente, es posible establecer el número mínimo de bytes que un filtro de limitación de ancho de
banda puede reenviar a la vez para un flujo dado. Debería utilizarse para no reenviar cantidades de
datos demasiado pequeñas y reducir así el uso de CPU. Debe definirse con cuidado. Un valor
demasiado pequeño puede aumentar el uso de CPU. Demasiado alto, puede aumentar la latencia. También
está estrechamente ligado al límite de ancho de banda definido. Si está demasiado cerca del límite
de ancho de banda, pueden experimentarse pausas para no superar el límite, porque se consumirán
demasiados bytes a la vez. Depende en gran medida de la configuración del filtro. Una buena idea es
empezar con un valor cercano a 2 MSS de TCP, normalmente 2896 bytes, y ajustarlo tras algunas
experimentaciones.

Ejemplo:

```text
frontend http
    bind *:80
    mode http

    # If this filter is enabled, the stream will share the download limit
    # of 10m/s with all other streams with the same source address.
    filter bwlim-out limit-by-src key src table limit-by-src limit 10m

    # If this filter is enabled, the stream will be limited to download at 1m/s,
    # independently of all other streams.
    filter bwlim-out limit-by-strm default-limit 1m default-period 1s

    # Limit all streams to 1m/s (the default limit) and those accessing the
    # internal API to 100k/s. Limit each source address to 10m/s. The shared
    # limit is applied first. Both are limiting the download rate.
    http-request set-bandwidth-limit limit-by-strm
    http-request set-bandwidth-limit limit-by-strm limit 100k if { path_beg /internal }
    http-request set-bandwidth-limit limit-by-src
    ...

backend limit-by-src
    # The stickiness table used by <limit-by-src> filter
    stick-table type ip size 1m expire 3600s store bytes_out_rate(1s)
```

Consulta también: «tcp-request content set-bandwidth-limit», «tcp-response content
set-bandwidth-limit», «http-request set-bandwidth-limit» y «http-response set-bandwidth-limit».
