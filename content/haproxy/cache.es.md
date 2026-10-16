---
title: "6. Caché"
linkTitle: "6. Caché"
weight: 170
description: "Limitaciones y configuración de la caché en las secciones cache y proxy"
icon: fa-solid fa-box-archive
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/cache/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 6"
---

HAProxy proporciona una caché, diseñada para almacenar en caché objetos pequeños (favicon, css...).
Se trata de una caché minimalista y de bajo mantenimiento que se ejecuta en RAM.

La caché se basa en una zona de memoria compartida entre todos los hilos, dividida en bloques de 1kB.

Si un objeto ya no se utiliza, puede eliminarse para almacenar un objeto nuevo con independencia de
su fecha de expiración. Los objetos más antiguos se eliminan primero cuando se intenta asignar uno
nuevo.

La caché utiliza como clave un hash del encabezado host y del URI.

Es posible consultar el estado de una caché mediante el comando «show cache» del socket Unix;
consulta la [sección 9.3](/es/haproxy/statistics-and-monitoring/#section-9-3) «Comandos del socket
Unix» de la Guía de administración para más detalles.

Cuando se entrega un objeto desde la caché, el nombre del servidor en el registro se sustituye por
«`<CACHE>`».

## 6.1. Limitación {#section-6-1}

La caché no almacenará ni entregará objetos en estos casos:

- Si la respuesta no es un 200

- Si la respuesta contiene un encabezado Vary y la opción process-vary está desactivada, o se
  especifica en el valor de Vary un encabezado actualmente no gestionado (por ahora solo se
  gestionan accept-encoding, referer y origin)

- Si el valor de Content-Length más el tamaño de los encabezados es mayor que «max-object-size»

- Si la respuesta no se puede almacenar en caché

- Si la respuesta no tiene un tiempo de expiración explícito (directivas s-maxage o max-age de
  Cache-Control o encabezado Expires) ni un validador (encabezados ETag o Last-Modified)

- Si la opción process-vary está activada y ya existen max-secondary-entries entradas con la misma
  clave primaria que la respuesta actual

- Si la opción process-vary está activada y la respuesta tiene una codificación desconocida (no
  mencionada en <https://www.iana.org/assignments/http-parameters/http-parameters.xhtml>) mientras
  varía según el encabezado del cliente accept-encoding

- Si la solicitud no es un GET

- Si la versión HTTP de la solicitud es inferior a 1.1

- Si la solicitud contiene un encabezado Authorization

## 6.2. Configuración {#section-6-2}

Para configurar una caché, debes definir una sección de caché y utilizarla en un proxy con las
acciones http-request y http-response correspondientes.

### 6.2.1. Sección de caché {#section-6-2-1}

<a id="entry-6-2-1-cache"></a>

**`cache <name>`**

```haproxy
cache <name>
```

Declara una sección de caché, asigna una memoria de caché compartida llamada `<name>`; el tamaño
de la caché es obligatorio (consulta la palabra clave «total-max-size» a continuación).

<a id="entry-6-2-1-max-age"></a>

**`max-age <seconds>`**

```haproxy
max-age <seconds>
```

Define la duración máxima de expiración. La expiración se establece como el valor más bajo entre
la directiva s-maxage o max-age (en este orden) del encabezado de respuesta Cache-Control y este
valor. El valor por defecto es 60 segundos, lo que significa que por defecto no se puede almacenar
en caché un objeto durante más de 60 segundos.

<a id="entry-6-2-1-max-object-size"></a>

**`max-object-size <bytes>`**

```haproxy
max-object-size <bytes>
```

Define el tamaño máximo de los objetos que se almacenarán en caché. No debe ser mayor que la mitad
de «total-max-size». Si no se establece, equivale a 1/256 del tamaño de la caché. Todos los objetos
cuyo tamaño supere «max-object-size» no se almacenarán en caché.

<a id="entry-6-2-1-max-secondary-entries"></a>

**`max-secondary-entries <number>`**

```haproxy
max-secondary-entries <number>
```

Define el número máximo de entradas secundarias simultáneas con la misma clave primaria en la
caché. Esto requiere que el soporte de vary esté activado. Su valor por defecto es 10 y debe
pasársele un entero estrictamente positivo.

<a id="entry-6-2-1-process-vary"></a>

**`process-vary <on/off>`**

```haproxy
process-vary <on/off>
```

Activa o desactiva el procesamiento del encabezado Vary. Cuando está desactivado, una respuesta
que contenga dicho encabezado nunca se almacenará en caché. Cuando está activado, es necesario
calcular un hash preliminar para un subconjunto de los encabezados de la solicitud en todas las
solicitudes entrantes (lo que puede tener un coste de CPU), que se utilizará para construir una
clave secundaria para una solicitud determinada (consulta RFC 7234#4.1). Por ahora, la clave
secundaria se construye a partir del contenido de los encabezados «accept-encoding», «referer» y
«origin». Ten en cuenta que los encabezados «origin» y «referer» son de valor único según la RFC,
por lo que una solicitud que contenga más de una ocurrencia de cualquiera de ellos debe
considerarse malformada. Para tales solicitudes no se construye ninguna clave secundaria y la
respuesta nunca se entrega desde la caché, para dejar que el servidor decida cómo manejar la
situación. El valor por defecto es off (desactivado).

<a id="entry-6-2-1-total-max-size"></a>

**`total-max-size <megabytes>`**

```haproxy
total-max-size <megabytes>
```

Define el tamaño en RAM de la caché en megabytes. Este tamaño se divide en bloques de 1kB que
utilizan las entradas de la caché. Su valor máximo es 4095.

### 6.2.2. Sección proxy {#section-6-2-2}

La sección proxy que utilice la caché deberá incluir la acción «cache-use» en el conjunto de
reglas «http-request» para buscar en la caché el objeto solicitado, y la acción «cache-store» en
el conjunto de reglas «http-response» para almacenar o actualizar en la caché el objeto
recuperado. Cada una de estas acciones puede incluir opcionalmente condiciones. Por ejemplo, se
puede decidir omitir la acción «cache-use» para cierto subdirectorio que se sabe que no se puede
almacenar en caché, u omitir la acción «cache-store» para ciertos tipos de contenido que se sabe
que carecen de valor. Ten en cuenta que la clave de indexación de la caché se calcula durante la
acción «cache-use», de modo que si se omite esta acción, de todos modos no se intentará actualizar
la caché en la ruta de la respuesta.

Ejemplo:

```text
backend bck1
  mode http

  http-request cache-use foobar
  http-response cache-store foobar
  server srv1 127.0.0.1:80

cache foobar
  total-max-size 4
  max-age 240
```
