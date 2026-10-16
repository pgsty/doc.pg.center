---
title: "10. Aplicaciones FastCGI"
linkTitle: "10. FastCGI"
weight: 210
description: "Configuración de aplicaciones FastCGI: parámetros, ejemplos y limitaciones"
icon: fa-solid fa-bolt
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/fastcgi/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

HAProxy es capaz de enviar solicitudes HTTP a aplicaciones FastCGI Responder. Esta funcionalidad se
añadió en HAProxy 2.1. Para ello, los servidores deben configurarse para utilizar el protocolo
FastCGI (mediante la palabra clave «proto fcgi» en la línea del servidor) y una aplicación FastCGI
debe configurarse y ser utilizada por el backend que gestiona estos servidores (mediante la palabra
clave «use-fcgi-app» en la sección proxy). Pueden definirse varias aplicaciones FastCGI, pero solo
una puede utilizarse a la vez por un backend.

HAProxy implementa todas las funcionalidades de la especificación FastCGI para aplicaciones
Responder. En particular, es capaz de multiplexar varias solicitudes en una única conexión.

## 10.1. Configuración {#section-10-1}



### 10.1.1. Sección fcgi-app {#section-10-1-1}

<a id="entry-10-1-1-fcgi-app"></a>

**`fcgi-app <name>`**

```haproxy
fcgi-app <name>
```

Declara una aplicación FastCGI llamada `<name>`. Para ser válida, al menos la raíz de documentos
debe estar definida.

<a id="entry-10-1-1-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

Declara o completa una lista de acceso.

Consulta la palabra clave «acl» en la [sección 4.2](/es/haproxy/proxies/#section-4-2) y la
[sección 7](/es/haproxy/acls-and-samples/) para más detalles sobre el uso de las ACL. Las ACL
definidas para una aplicación FastCGI son privadas. No pueden ser utilizadas por ninguna otra
aplicación ni por ningún proxy. Del mismo modo, las ACL definidas en cualquier otra sección no son
utilizables por una aplicación FastCGI. Sin embargo, las ACL predefinidas están disponibles.

<a id="entry-10-1-1-docroot"></a>

**`docroot <path>`**

```haproxy
docroot <path>
```

Define la raíz de documentos en el host remoto. `<path>` se utilizará para construir el valor
predeterminado de los parámetros FastCGI SCRIPT_FILENAME y PATH_TRANSLATED. Es un parámetro
obligatorio.

<a id="entry-10-1-1-index"></a>

**`index <script-name>`**

```haproxy
index <script-name>
```

Define el nombre del script que se añadirá tras un URI que termina con una barra («/») para
establecer el valor predeterminado del parámetro FastCGI SCRIPT_NAME. Es un parámetro opcional.

Ejemplo:

```text
index index.php
```

<a id="entry-10-1-1-log-stderr-global"></a>

**`log-stderr global`**

```haproxy
log-stderr global
log-stderr <target> [len <length>] [format <format>]
    [sample <ranges>:<sample_size>] <facility> [<level> [<minlevel>]]
```

Activa el registro de los mensajes STDERR reportados por la aplicación FastCGI.

Consulta la palabra clave «log» en la [sección 4.2](/es/haproxy/proxies/#section-4-2) para más
detalles. Es un parámetro opcional. Por defecto, los mensajes STDERR se ignoran.

<a id="entry-10-1-1-pass-header"></a>

**`pass-header <name> [ { if | unless } <condition> ]`**

```haproxy
pass-header <name> [ { if | unless } <condition> ]
```

Especifica el nombre de un encabezado de solicitud que se pasará a la aplicación FastCGI. Puede ir
seguido opcionalmente de una condición basada en ACL, en cuyo caso solo se evaluará si la condición
es verdadera.

La mayoría de los encabezados de solicitud ya están disponibles para la aplicación FastCGI, con el
prefijo «HTTP\_». Por lo tanto, esta directiva solo es necesaria para pasar encabezados que se
omiten deliberadamente. Actualmente, los encabezados «Authorization», «Proxy-Authorization» y los
encabezados hop-by-hop se omiten.

Ten en cuenta que los encabezados «Content-type» y «Content-length» nunca se pasan a la aplicación
FastCGI porque ya se han convertido en parámetros.

<a id="entry-10-1-1-path-info"></a>

**`path-info <regex>`**

```haproxy
path-info <regex>
```

Define una expresión regular para extraer el nombre del script (script-name) y la información de
ruta (path-info) a partir de la ruta decodificada de URL. Así, `<regex>` puede tener dos capturas:
la primera para capturar el nombre del script y la segunda para capturar la información de ruta. La
primera es obligatoria, la segunda es opcional. De esta manera, es posible extraer el nombre del
script de la ruta ignorando la información de ruta. Es un parámetro opcional. Si no se define, no
se realiza ninguna coincidencia sobre la ruta y los parámetros FastCGI PATH_INFO y PATH_TRANSLATED
no se rellenan.

Por razones de seguridad, cuando esta expresión regular está definida, los caracteres de nueva
línea y nulos quedan prohibidos en la ruta, una vez decodificada la URL. La razón de esta limitación
es que, de lo contrario, la coincidencia siempre falla (debido a una limitación en la forma en que
se ejecutan las expresiones regulares en HAProxy). Por ello, si se encuentra uno de estos dos
caracteres en la ruta decodificada de URL, se devuelve un error al cliente. Aquí se aplica el
principio de mínima sorpresa.

Ejemplo:

```text
path-info ^(/.+\.php)(/.*)?$ # both script-name and path-info may be set
path-info ^(/.+\.php)        # the path-info is ignored
```

<a id="entry-10-1-1-option-get-values"></a>

**`option get-values`**

```haproxy
option get-values
no option get-values
```

Activa o desactiva la recuperación de variables sobre la gestión de conexiones.

HAProxy puede enviar el registro FCGI_GET_VALUES al establecerse la conexión para recuperar el
valor de las siguientes variables:

    * FCGI_MAX_REQS     Número máximo de solicitudes simultáneas que esta
                        aplicación aceptará.

    * FCGI_MPXS_CONNS   «0» si esta aplicación no multiplexa conexiones,
                        «1» en caso contrario.

Algunas aplicaciones FastCGI no admiten esta funcionalidad. Otras cierran la conexión
inmediatamente después de enviar su respuesta. Por ello, por defecto esta opción está desactivada.

Ten en cuenta que el número máximo de solicitudes simultáneas aceptadas por una aplicación FastCGI
es una variable de conexión. Solo limita el número de flujos por conexión. Si la carga global debe
limitarse en la aplicación, deben establecerse los parámetros de servidor «maxconn» y
«pool-max-conn». Además, si una aplicación no admite la multiplexación de conexiones, el número
máximo de solicitudes simultáneas se establece automáticamente en 1.

<a id="entry-10-1-1-option-keep-conn"></a>

**`option keep-conn`**

```haproxy
option keep-conn
no option keep-conn
```

Indica a la aplicación FastCGI que mantenga abierta la conexión o no después de enviar una
respuesta.

Si está desactivada, la aplicación FastCGI cierra la conexión después de responder a esta
solicitud. Por defecto, esta opción está activada.

<a id="entry-10-1-1-option-max-reqs"></a>

**`option max-reqs <reqs>`**

```haproxy
option max-reqs <reqs>
```

Define el número máximo de solicitudes simultáneas que esta aplicación aceptará.

Esta opción puede sobrescribirse si la variable FCGI_MAX_REQS se recupera durante el
establecimiento de la conexión. Además, si la aplicación no admite la multiplexación de conexiones,
esta opción se ignorará. Por defecto se establece en 1.

<a id="entry-10-1-1-option-mpxs-conns"></a>

**`option mpxs-conns`**

```haproxy
option mpxs-conns
no option mpxs-conns
```

Activa o desactiva la compatibilidad con la multiplexación de conexiones.

Esta opción puede sobrescribirse si la variable FCGI_MPXS_CONNS se recupera durante el
establecimiento de la conexión. Está desactivada por defecto.

<a id="entry-10-1-1-set-param"></a>

**`set-param <name> <fmt> [ { if | unless } <condition> ]`**

```haproxy
set-param <name> <fmt> [ { if | unless } <condition> ]
```

Establece un parámetro FastCGI que debe pasarse a esta aplicación. Su valor, definido por `<fmt>`,
debe seguir las reglas del formato de registro personalizado (consulta la
[sección 8.2.6](/es/haproxy/configuration-logging/#section-8-2-6) «Formato de registro
personalizado»). Puede ir seguido opcionalmente de una condición basada en ACL, en cuyo caso solo
se evaluará si la condición es verdadera.

Con esta directiva, es posible sobrescribir el valor de los parámetros FastCGI predeterminados. Si
el valor se evalúa como una cadena vacía, la regla se ignora. Estas directivas se evalúan en su
orden de declaración.

Ejemplo:

```shell
# PHP only, required if PHP was built with --enable-force-cgi-redirect
set-param REDIRECT_STATUS 200

set-param PHP_AUTH_DIGEST %[req.hdr(Authorization)]
```

### 10.1.2. Sección proxy {#section-10-1-2}

use-fcgi-app `<name>` Define la aplicación FastCGI que utilizará el backend.

Argumentos:

```text
<name>    es el nombre de la aplicación FastCGI que se utilizará.
```

Esta palabra clave solo está disponible para proxies HTTP con capacidad de backend y con al menos
un servidor FastCGI. Sin embargo, los servidores FastCGI pueden mezclarse con servidores HTTP. Pero
salvo que exista una buena razón para hacerlo, no se recomienda (consulta la
[sección 10.3](/es/haproxy/fastcgi/#section-10-3) para más detalles sobre las limitaciones). Solo
puede definirse una aplicación a la vez por backend.

Ten en cuenta que, una vez que se hace referencia a una aplicación FastCGI para un backend,
dependiendo de la configuración puede realizarse cierto procesamiento incluso si la solicitud no se
envía a un servidor FastCGI. Se evalúan las reglas para establecer parámetros o pasar encabezados a
una aplicación.

### 10.1.3. Ejemplo {#section-10-1-3}

```haproxy
frontend front-http
    mode http
    bind *:80

    use_backend back-dynamic if { path_reg ^/.+\.php(/.*)?$ }
    default_backend back-static

backend back-static
    mode http
    server www A.B.C.D:80

backend back-dynamic
    mode http
    use-fcgi-app php-fpm
    server php-fpm A.B.C.D:9000 proto fcgi

fcgi-app php-fpm
    log-stderr global
    option keep-conn

    docroot /var/www/my-app
    index index.php
    path-info ^(/.+\.php)(/.*)?$
```

## 10.2. Parámetros predeterminados {#section-10-2}

Una aplicación FastCGI Responder tiene el mismo propósito que un programa CGI/1.1. En la
especificación CGI/1.1 (RFC3875), varias variables deben pasarse al script. Por ello, HAProxy las
establece, junto con algunas otras comúnmente utilizadas por las aplicaciones FastCGI. Todas estas
variables pueden sobrescribirse, aunque con precaución.

```text
  +-------------------+-----------------------------------------------------+
  | AUTH_TYPE         | Identifica el mecanismo, si existe, utilizado por   |
  |                   | HAProxy para autenticar al usuario. En la práctica, |
  |                   | solo se admite el mecanismo de autenticación BASIC. |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_LENGTH    | Contiene el tamaño del cuerpo del mensaje adjunto a |
  |                   | la solicitud. Esto significa que solo las           |
  |                   | solicitudes con un tamaño conocido se consideran    |
  |                   | válidas y se envían a la aplicación.                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | CONTENT_TYPE      | Contiene el tipo del cuerpo del mensaje adjunto a   |
  |                   | la solicitud. Puede no estar definido.              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | DOCUMENT_ROOT     | Contiene la raíz de documentos del host remoto bajo |
  |                   | la cual debe ejecutarse el script, tal como se      |
  |                   | definió en la configuración de la aplicación.       |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | GATEWAY_INTERFACE | Contiene el dialecto de CGI utilizado por HAProxy   |
  |                   | para comunicarse con la aplicación FastCGI. En la   |
  |                   | práctica, se establece en «CGI/1.1».                |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_INFO         | Contiene la porción de la jerarquía de la ruta del  |
  |                   | URI que sigue a la parte que identifica al propio   |
  |                   | script. Para que se establezca, debe definirse la   |
  |                   | directiva «path-info».                              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | PATH_TRANSLATED   | Si PATH_INFO está definido, contiene su versión     |
  |                   | traducida: la concatenación de DOCUMENT_ROOT y      |
  |                   | PATH_INFO. Si PATH_INFO no está definido, este      |
  |                   | parámetro tampoco se define.                        |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | QUERY_STRING      | Contiene la cadena de consulta de la solicitud.     |
  |                   | Puede no estar definido.                            |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_ADDR       | Contiene la dirección de red del cliente que envía  |
  |                   | la solicitud.                                       |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REMOTE_USER       | Contiene la cadena de identificación del usuario    |
  |                   | proporcionada por el cliente como parte de la       |
  |                   | autenticación del usuario.                          |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_METHOD    | Contiene el método que el script debe utilizar para |
  |                   | procesar la solicitud.                              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | REQUEST_URI       | Contiene el URI de la solicitud.                    |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_FILENAME   | Contiene la ruta absoluta del script: la            |
  |                   | concatenación de DOCUMENT_ROOT y SCRIPT_NAME.       |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SCRIPT_NAME       | Contiene el nombre del script. Si la directiva      |
  |                   | «path-info» está definida, es la primera parte de   |
  |                   | la jerarquía de la ruta del URI, que termina con el |
  |                   | nombre del script. En caso contrario, es la ruta    |
  |                   | completa del URI.                                   |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_NAME       | Contiene el nombre del host del servidor al que se  |
  |                   | dirige la solicitud del cliente. Es el valor del    |
  |                   | encabezado «Host», si está definido; en caso        |
  |                   | contrario, la dirección de destino de la conexión   |
  |                   | por parte del cliente.                              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PORT       | Contiene el puerto TCP de destino de la conexión    |
  |                   | por parte del cliente, es decir, el puerto al que   |
  |                   | se conectó el cliente.                              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_PROTOCOL   | Contiene el protocolo de la solicitud.              |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | SERVER_SOFTWARE   | Contiene la cadena «HAProxy» seguida de la versión  |
  |                   | actual de HAProxy.                                  |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
  | HTTPS             | Se establece en un valor no vacío («on») si se      |
  |                   | accedió al script a través del protocolo HTTPS.     |
  |                   |                                                     |
  +-------------------+-----------------------------------------------------+
```

## 10.3. Limitaciones {#section-10-3}

La implementación actual tiene algunas limitaciones. La primera se refiere a la forma en que
algunos encabezados de solicitud se ocultan a las aplicaciones FastCGI. Esto ocurre durante el
análisis de los encabezados, en el lado del backend, antes del establecimiento de la conexión. En
esta etapa, HAProxy sabe que el backend utiliza una aplicación FastCGI, pero no sabe si la solicitud
se enrutará o no a un servidor FastCGI. Pero para ocultar los encabezados de solicitud, simplemente
los elimina del mensaje HTX. Así, si la solicitud finalmente se enruta a un servidor HTTP, este
nunca ve dichos encabezados. Por esta razón, no se recomienda mezclar servidores FastCGI y
servidores HTTP bajo el mismo backend.

Del mismo modo, las reglas «set-param» y «pass-header» se evalúan durante el análisis de los
encabezados de solicitud. Por lo tanto, la evaluación siempre se realiza, incluso si la solicitud
finalmente se reenvía a un servidor HTTP.

Respecto a las reglas «set-param», cuando se aplica una regla, se añade un pseudoencabezado al
mensaje HTX. Así, de la misma manera que para las reescrituras de encabezados HTTP, puede fallar si
el búfer está lleno. Las reglas «set-param» competirán con las de «http-request».

Finalmente, todos los parámetros FastCGI y los encabezados HTTP se envían en un único registro
FCGI_PARAM. La codificación de este registro debe hacerse en una sola pasada; de lo contrario, se
devuelve un error de procesamiento. Esto significa que el registro FCGI_PARAM, una vez codificado,
no debe superar el tamaño de un búfer. Sin embargo, no hay ninguna reserva que respetar aquí.
