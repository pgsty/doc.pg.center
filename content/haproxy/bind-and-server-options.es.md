---
title: "5. Opciones de bind y de servidor"
linkTitle: "5. Opciones bind y server"
weight: 160
description: "Opciones de listener, server, default-server y resolución DNS"
icon: fa-solid fa-network-wired
module: [HAPROXY]
categories: [Referencia]
aliases:
  - /haproxy/configuration/bind-and-server-options/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 5"
---

Las palabras clave "bind", "server" y "default-server" soportan cierto número de parámetros según
algunas opciones de compilación y según el sistema sobre el que se compiló HAProxy. Generalmente,
cada uno de estos parámetros consiste en una palabra, a veces seguida de un valor, escritos en la
misma línea que la línea "bind" o "server". Todas estas opciones se describen en esta sección.

## 5.1. Opciones de bind {#section-5-1}

La palabra clave "bind" soporta cierto número de parámetros, todos pasados como argumentos en la
misma línea. El orden en que aparecen esos argumentos carece de importancia, siempre que aparezcan
después de la dirección de bind. Todos estos parámetros son opcionales. Algunos consisten en una
sola palabra (booleanos), mientras que otros esperan un valor a continuación. En este caso, el valor
debe proporcionarse inmediatamente después del nombre del parámetro.

Los parámetros soportados actualmente son los siguientes.

<a id="entry-5-1-accept-netscaler-cip"></a>

**`accept-netscaler-cip <magic number>`**

```haproxy
accept-netscaler-cip <magic number>
```

Fuerza el uso del protocolo de inserción de IP de cliente de NetScaler en cualquier conexión
aceptada por cualquiera de los sockets TCP declarados en la misma línea. El protocolo de inserción
de IP de cliente de NetScaler dicta que las direcciones de capa 3/4 de la conexión entrante se usen
en cualquier lugar donde se use una dirección, con la única excepción de las reglas "tcp-request
connection", que solo verán la dirección real de la conexión. Los registros reflejarán las
direcciones indicadas en el protocolo, salvo que este se incumpla, en cuyo caso se seguirá usando la
dirección real. Esta palabra clave, combinada con soporte de componentes externos, puede usarse como
una alternativa eficiente y fiable al mecanismo X-Forwarded-For, que no siempre es fiable y ni
siquiera siempre utilizable. Ver también "tcp-request connection expect-netscaler-cip" para un
ajuste más fino de qué cliente puede usar el protocolo.

<a id="entry-5-1-accept-proxy"></a>

**`accept-proxy`**

```haproxy
accept-proxy
```

Fuerza el uso del protocolo PROXY en cualquier conexión aceptada por cualquiera de los sockets
declarados en la misma línea. Las versiones 1 y 2 del protocolo PROXY están soportadas y se detectan
correctamente. El protocolo PROXY dicta que las direcciones de capa 3/4 de la conexión entrante se
usen en cualquier lugar donde se use una dirección, con la única excepción de las reglas
"tcp-request connection", que solo verán la dirección real de la conexión. Los registros reflejarán
las direcciones indicadas en el protocolo, salvo que este se incumpla, en cuyo caso se seguirá
usando la dirección real. Esta palabra clave, combinada con soporte de componentes externos, puede
usarse como una alternativa eficiente y fiable al mecanismo X-Forwarded-For, que no siempre es
fiable y ni siquiera siempre utilizable. Ver también "tcp-request connection expect-proxy" para un
ajuste más fino de qué cliente puede usar el protocolo.

<a id="entry-5-1-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Permite recibir early data al usar TLSv1.3. Está desactivado por defecto por consideraciones de
seguridad. Como es vulnerable a ataques de repetición, solo deberías permitirlo para solicitudes que
sean seguras de reproducir, es decir, solicitudes idempotentes. Puedes usar la acción
"wait-for-handshake" para cualquier solicitud que no sería segura con early data. Con QUIC, 0rtt es
compatible con QuicTLS, OpenSSL \>= 3.5.2 y AWS-LC. Con TCP/TLS, 0rtt solo es compatible con OpenSSL
y requiere que el cliente envíe un ALPN; de lo contrario, los early data no se considerarán antes de
que ocurra el handshake.

<a id="entry-5-1-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Esto habilita la extensión ALPN de TLS y anuncia la lista de protocolos especificada como soportada
sobre ALPN. La lista de protocolos consiste en una lista de nombres de protocolo delimitados por
comas, por ejemplo: "http/1.1,http/1.0" (sin comillas). Esto requiere que la biblioteca SSL se haya
compilado con el soporte para extensiones TLS habilitado (compruébalo con haproxy -vv). La extensión
ALPN sustituye a la extensión NPN original. A nivel de protocolo, ALPN es necesario para habilitar
HTTP/2 en un frontend HTTPS y HTTP/3 en un frontend QUIC. Sin embargo, cuando tales frontends no
tienen definido ninguno de "npn", "alpn" y "no-alpn", se usará un valor por defecto de
"h2,http/1.1" para un frontend HTTPS normal y "h3" para un frontend QUIC. Las versiones de OpenSSL
anteriores a 1.0.2 no soportaban ALPN y solo admitían la hoy obsoleta extensión NPN. Al momento de
escribir esto, la mayoría de los navegadores siguen soportando tanto ALPN como NPN para HTTP/2, por
lo que un repliegue a NPN puede seguir funcionando durante un tiempo. Pero ALPN debe usarse siempre
que sea posible. Los protocolos no anunciados no se negocian. Por ejemplo, es posible aceptar solo
conexiones HTTP/2 con esto:

```text
bind :443 ssl crt pub.pem alpn h2  # explicitly disable HTTP/1.1
```

QUIC solo soporta h3 y hq-interop como ALPN. h3 es para HTTP/3 y hq-interop se usa para http/0.9 y
el interop runner de QUIC (ver <https://interop.seemann.io>). Cada declaración "alpn" sustituirá a
una anterior. Para eliminarlas, usa "no-alpn".

Ten en cuenta que algunos navegadores antiguos como Firefox 88 solían sufrir problemas con WebSocket
sobre H2 y, en caso de encontrar tal configuración, puede ser necesario deshabilitar explícitamente
HTTP/2 en la cadena "alpn" forzándola a "http/1.1" o "no-alpn", o habilitar
"h2-workaround-bogus-websocket-clients" globalmente.

<a id="entry-5-1-backlog"></a>

**`backlog <backlog>`**

```haproxy
backlog <backlog>
```

Fija el backlog del socket a este valor. Si no se especifica o es 0, se usa en su lugar el backlog
del frontend, que generalmente toma por defecto el valor de maxconn.

<a id="entry-5-1-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM del cual cargar los certificados de CA usados para verificar el certificado del cliente. Es
posible cargar un directorio que contenga varias CA; en este caso HAProxy intentará cargar todo
".pem", ".crt", ".cer" y .crl" disponible en el directorio; los archivos que empiezan por un punto
se ignoran.

Advertencia: El parámetro "@system-ca" podría usarse en lugar del cafile para usar las CA de
confianza de tu sistema, igual que se hace con la directiva server. Pero no debes usarlo salvo que
sepas lo que haces. Configurarlo de esta manera básicamente significa que el bind aceptará cualquier
certificado de cliente generado por una de las CA presentes en tu sistema, lo cual es extremadamente
inseguro.

<a id="entry-5-1-ca-ignore-err"></a>

**`ca-ignore-err [all|<errorID>,...]`**

```haproxy
ca-ignore-err [all|<errorID>,...]
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define una lista
separada por comas de errorIDs que se ignoran durante la verificación a profundidad \> 0. Puede ser
un ID numérico o el nombre de la constante (X509_V_ERR), disponible en la documentación de OpenSSL:
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES> Se recomienda
usar el nombre de la constante, ya que el valor numérico puede cambiar en nuevas versiones de
OpenSSL. Si se define como 'all', se ignoran todos los errores. El handshake SSL no se aborta si se
ignora un error.

<a id="entry-5-1-ca-sign-file"></a>

**`ca-sign-file <cafile>`**

```haproxy
ca-sign-file <cafile>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM que contiene tanto el certificado de la CA como la clave privada de la CA, usados para crear y
firmar certificados de servidor. Es un parámetro obligatorio cuando la generación dinámica de
certificados está habilitada. Ver 'generate-certificates' para más detalles.

<a id="entry-5-1-ca-sign-pass"></a>

**`ca-sign-pass <passphrase>`**

```haproxy
ca-sign-pass <passphrase>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Es la frase de
contraseña de la clave privada de la CA. Este parámetro es opcional y se usa solo cuando la
generación dinámica de certificados está habilitada. Ver 'generate-certificates' para más detalles.

<a id="entry-5-1-ca-verify-file"></a>

**`ca-verify-file <cafile>`**

```haproxy
ca-verify-file <cafile>
```

Este parámetro designa un archivo PEM del cual cargar los certificados de CA usados para verificar
el certificado del cliente. Designa certificados de CA que no deben incluirse en los nombres de CA
enviados en el mensaje server hello. Típicamente, "ca-file" debe definirse con certificados
intermedios y "ca-verify-file" con certificados que terminan la cadena, como la CA raíz.

<a id="entry-5-1-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Este parámetro solo está disponible en sistemas que definen TCP_CONGESTION y se validó en Linux y
FreeBSD. Toma el nombre de un algoritmo de control de congestión TCP y configura el listener para
que use este algoritmo en todas las conexiones que se acepten desde este listener. Los nombres
típicos incluyen "reno" y "cubic" y dependerán del sistema operativo. En algunos sistemas pueden
requerirse permisos especiales para configurar ciertos algoritmos. En Linux, la lista de algoritmos
disponibles puede encontrarse en el sysctl "net.ipv4.tcp_available_congestion_control" y la de los
permitidos sin privilegios en "net.ipv4.tcp_allowed_congestion_control". Para acceder a algoritmos
que requieren permisos adicionales puede necesitarse la capacidad "cap_net_admin" (ver "setcap" en
la sección global). En caso de fallo al configurar un algoritmo de control de congestión específico,
el predeterminado permanecerá sin cambios y se emitirá una advertencia para reportar el problema.
Ver también: la palabra clave "cc" de server ([sección 5.2](/es/haproxy/bind-and-server-options/#section-5-2)). Ejemplo:

```text
frontend public
    bind :443 cc bbr   # use the BBR algorithm for high bandwidths
```

<a id="entry-5-1-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de cifrado ("cipher suite") que se negocian durante el handshake
SSL/TLS hasta TLSv1.2. El formato de la cadena está definido en "man 1 ciphers" de las páginas man de
OpenSSL. Para información de contexto y recomendaciones ver p. ej.
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) y
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Para la configuración de
cifrados de TLSv1.3, consulta la palabra clave "ciphersuites".

<a id="entry-5-1-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL y se usó OpenSSL
1.1.1 o posterior para compilar HAProxy. Define la cadena que describe la lista de algoritmos de
cifrado ("cipher suite") que se negocian durante el handshake TLSv1.3. El formato de la cadena está
definido en "man 1 ciphers" de las páginas man de OpenSSL, en la sección "ciphersuites". Para la
configuración de cifrados para TLSv1.2 y anteriores, consulta la palabra clave "ciphers". Este
parámetro podría aceptar ciphersuites de TLSv1.2; sin embargo, es un comportamiento no documentado y
no recomendado, pues podría ser inconsistente o defectuoso. Los ciphersuites TLSv1.3 por defecto de
OpenSSL son:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 solo soporta 5 ciphersuites:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Ejemplo:

```text
ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-5-1-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de firma relacionados con la autenticación de cliente que se
negocian. El formato de la cadena está definido en "man 3 SSL_CTX_set1_client_sigalgs" de las páginas
man de OpenSSL. No se recomienda usar este parámetro si no se ha identificado un caso de uso
específico.

<a id="entry-5-1-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM del cual cargar la lista de revocación de certificados usada para verificar el certificado del
cliente. Necesitas proporcionar una lista de revocación de certificados por cada certificado de tu
cadena de autoridades de certificación.

<a id="entry-5-1-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL.

HAProxy usa un sistema de caché: los archivos se cargan una sola vez en el almacenamiento de
certificados y cada aparición siguiente de la palabra clave "crt" usará esta versión en caché.
Cuando el certificado se declaró en un "crt-store", el almacenamiento de certificados se llena desde
ahí y no se intenta cargar archivos adicionales detectando extensiones de archivo.

Designa un archivo PEM que contiene tanto los certificados requeridos como cualquier clave privada
asociada. Este archivo puede construirse concatenando varios archivos PEM en uno (p. ej. cat cert.pem
key.pem \> combined.pem). Si tu CA requiere un certificado intermedio, este también puede
concatenarse en este archivo. El certificado intermedio también puede compartirse en un directorio
mediante la directiva "issuers-chain-path".

Si el archivo no contiene una clave privada, HAProxy intentará cargar la clave en la misma ruta con
el sufijo ".key".

Si el OpenSSL usado soporta Diffie-Hellman, los parámetros presentes en este archivo se cargan.

Si se usa un nombre de directorio en lugar de un archivo PEM, todos los archivos encontrados en ese
directorio se cargarán en orden alfabético, salvo que su nombre termine en '.key', '.issuer',
'.ocsp' o '.sctl' (extensiones reservadas). Los archivos que empiezan por un punto también se
ignoran. Esta directiva puede especificarse varias veces para cargar certificados de varios archivos
o directorios. Los certificados se presentarán a los clientes que proporcionen un campo TLS Server
Name Indication válido que coincida con uno de sus CN o alt subjects. Se soportan comodines, donde
un carácter comodín '\*' se usa en lugar del primer componente del nombre de host (p. ej.
\*.example.org coincide con [www.example.org](http://www.example.org) pero no con
[www.sub.example.org](http://www.sub.example.org)). Si se usa un directorio vacío, HAProxy no
arrancará salvo que se use la palabra clave "strict-sni".

Si el cliente no proporciona SNI, o si la biblioteca SSL no soporta extensiones TLS, o si el cliente
proporciona un nombre de host SNI que no coincide con ningún certificado, se presentará el primer
certificado cargado. Esto significa que, al cargar certificados desde un directorio, es muy
recomendable cargar primero el predeterminado como archivo o asegurarse de que siempre será el
primero en el directorio. Para elegir varios certificados predeterminados (1 rsa y 1 ecdsa), hay 3
opciones:

- Puede configurarse un paquete multi-cert como primer certificado (`crt foobar.pem` en la
  configuración, donde los archivos existentes son `foobar.pem.ecdsa` y `foobar.pem.rsa`.
- O un filtro '\*' para cada certificado en una línea de crt-list.
- Puede usarse la palabra clave 'default-crt'.

Ten en cuenta que el mismo certificado puede cargarse varias veces sin efectos secundarios.

Algunas CA (como GoDaddy) ofrecen una lista desplegable de tipos de servidor que no incluye HAProxy
al obtener un certificado. Si esto ocurre, asegúrate de elegir un servidor web para el cual la CA
considere que se requiere una CA intermedia (para GoDaddy, seleccionar Apache Tomcat dará el paquete
correcto, pero muchos otros, p. ej. nginx, dan como resultado un paquete incorrecto que no funcionará
con algunos clientes).

Para cada archivo PEM, HAProxy comprueba la presencia de un archivo en la misma ruta con el sufijo
".ocsp". Si se encuentra tal archivo, el soporte para la extensión TLS Certificate Status Request
(también conocida como "OCSP stapling") se habilita automáticamente. El contenido de este archivo es
opcional. Si no está vacío, debe contener una OCSP Response válida en formato DER. Para ser válida,
una OCSP Response debe cumplir las siguientes reglas: debe indicar un estado good, debe ser una
respuesta única para el certificado del archivo PEM y debe ser válida en el momento de la adición.
Si no se respetan estas reglas, la OCSP Response se ignora y se emite una advertencia. Para
identificar a qué certificado se aplica una OCSP Response, es necesario el certificado del emisor.
Si el certificado del emisor no se encuentra en el archivo PEM, se cargará desde un archivo en la
misma ruta que el archivo PEM con el sufijo ".issuer" si existe; de lo contrario fallará con un
error.

Para cada archivo PEM, HAProxy también comprueba la presencia de un archivo en la misma ruta con el
sufijo ".sctl". Si se encuentra tal archivo, se habilita el soporte para la extensión TLS de
Certificate Transparency (RFC6962). El archivo debe contener una Signed Certificate Timestamp List
válida, como se describe en el RFC. El archivo se analiza para comprobar la sintaxis básica, pero no
se verifica ninguna firma.

Hay casos en los que es deseable soportar múltiples tipos de clave, p. ej. RSA y ECDSA en los cipher
suites ofrecidos a los clientes. Esto permite que los clientes que soportan certificados EC puedan
usar cifrados EC, mientras se soporta simultáneamente a clientes antiguos que solo usan RSA.

Para lograrlo se requiere OpenSSL 1.1.1; puedes configurar este comportamiento proporcionando una
entrada crt por tipo de certificado, o configurando un "cert bundle" como se requería antes de
HAProxy 1.8. Ver "ssl-load-extra-files".

<a id="entry-5-1-crt-ignore-err"></a>

**`crt-ignore-err <errors>`**

```haproxy
crt-ignore-err <errors>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define una lista
separada por comas de errorIDs que se ignoran durante la verificación a profundidad == 0. Puede ser
un ID numérico o el nombre de la constante (X509_V_ERR), disponible en la documentación de OpenSSL:
<https://www.openssl.org/docs/manmaster/man3/X509_STORE_CTX_get_error.html#ERROR-CODES> Se recomienda
usar el nombre de la constante, ya que el valor numérico puede cambiar en nuevas versiones de
OpenSSL. Si se define como 'all', se ignoran todos los errores. El handshake SSL no se aborta si se
ignora un error.

<a id="entry-5-1-crt-list"></a>

**`crt-list <file>`**

```haproxy
crt-list <file>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa una lista de
archivos PEM con una configuración ssl opcional y un filtro SNI por certificado, con el siguiente
formato para cada línea:

```text
<crtfile> [\[<sslbindconf> ...\]] [[!]<snifilter> ...]
```

Las líneas vacías así como las que comienzan con una almohadilla ('#') se ignoran.

La crt-list puede manipularse dinámicamente a través del socket de estadísticas. (Ver "add ssl
crt-list", "del ssl crt-list", "show ssl crt-list" en la guía de gestión).

Las crt-list suelen ser archivos dedicados; sin embargo, un directorio cargado con la directiva
"crt" se representa internamente como una crt-list. La directiva "ssl-f-use" en un frontend también
declara una crt-list vinculada a ese frontend.

crtfile:

```text
Este es el nombre del archivo del certificado, o un identificador si este fue
declarado en otro lugar (por la CLI o en un crt-store con un alias, por ejemplo).

Es posible usar el mismo <crtfile> en varias líneas con diferentes
opciones y filtros.

El empaquetado multi-cert (ver "ssl-load-extra-files") está soportado en una
crt-list, siempre que solo se indique el nombre base en <crtfile>. HAProxy
duplicará internamente la línea de la crt-list, añadiendo una extensión de
algoritmo (.rsa, .ecdsa, .dsa) al cargar el archivo.
```

sslbindconf:

```text
 <sslbindconf> soporta las siguientes palabras clave de la línea bind (ver
 Sección 5.1. Opciones de bind):

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
 - no-alpn
 - no-ca-names
 - npn
 - sigalgs
 - ssl-min-ver
 - ssl-max-ver
 - verify

 <sslbindconf> también soporta las siguientes palabras clave de la palabra
 clave load de crt-store (ver Sección 12.7.1. Opciones de carga):

 - crt
 - key
 - ocsp
 - issuer
 - sctl
 - ocsp-update

Los parámetros de la línea bind se heredan en <sslbindconf>; si no se
especificó ninguno, se heredan las opciones por defecto; los parámetros
especificados en <sslbindconf> sobrescriben esos ajustes heredados.
```

snifilter:

```text
Cuando el parámetro <snifilter> se usa en una línea de crt-list, los CN y SAN
ya no se usan para seleccionar el certificado de esa línea durante el
handshake; en su lugar se usa el <snifilter>.

<snifilter> es una lista de entradas separadas por espacios. Esta lista puede
contener dominios o comodines. Los comodines siguen el formato DNS con
comodín, usando un único asterisco como primer carácter de la entrada. Es
posible excluir un dominio de un comodín mediante un filtro negativo,
especificando un '!' delante de un dominio único. Un ! delante de un * se
ignora. Tener filtros negativos sin un comodín en la misma línea tampoco
está soportado. La entrada especial '*' se usa para especificar certificados
predeterminados, que se emplean como alternativa cuando ningún dominio
coincidió.

Los certificados se presentarán a los clientes que proporcionen un campo TLS
Server Name Indication válido que coincida con uno de los filtros SNI, o con
los CN y SAN de un <crtfile>. El algoritmo de coincidencia busca primero una
entrada de dominio positiva en la lista; si no la encuentra, intentará buscar
un comodín en la lista. Si coincide un comodín, haproxy comprueba si hay un
filtro negativo en la misma línea y descarta la coincidencia si es necesario.
En caso de haber varios algoritmos de clave (RSA,ECDSA,DSA), HAProxy
intentará encontrar un certificado por tipo y elegir el adecuado según lo
que soporte el cliente.

Si el cliente no presenta ningún SNI o si ningún certificado coincidió, se
recurrirá a uno de los certificados predeterminados. Para deshabilitar este
comportamiento, puede usarse la opción 'strict-sni'.
Cuando se definen varios certificados predeterminados, HAProxy es capaz de
elegir el adecuado, ECDSA o RSA, según lo que soporte el cliente.

El primer certificado declarado en una línea bind se usa como certificado
predeterminado, ya sea desde la opción crt o desde crt-list.
También es posible declarar un filtro '*', lo que añadirá este
certificado a la lista de certificados predeterminados. Para aclarar la
configuración, los certificados predeterminados pueden ser explícitos (con un
filtro '*') al principio de la lista, de modo que no se añada antes un
predeterminado implícito.
Debido a que los paquetes multi-cert se duplican para cada algoritmo en la
crt-list, solo un algoritmo ocupará la primera línea de la crt-list y será
considerado el predeterminado. Especifica el paquete completo como
predeterminado declarando '*' como filtro, o bien configúralo en la línea
bind.

El comando "show ssl sni" del socket de estadísticas puede usarse para
depurar la configuración. (Ver "show ssl sni" en la guía de gestión)
```

Ejemplo:

```shell
# comment
default.pem.rsa *
default.pem.ecdsa *
cert2.pem [alpn h2,http/1.1]
certW.pem *.domain.tld !secure.domain.tld
certS.pem [curves X25519:P-256 ciphers ECDHE-ECDSA-AES256-GCM-SHA384] secure.domain.tld
foo.crt [key bar.pem ocsp foo.ocsp ocsp-update on] foo.bar.com
```

<a id="entry-5-1-default-crt"></a>

**`default-crt <cert>`**

```haproxy
default-crt <cert>
```

Esta opción hace lo mismo que la opción "crt", con la diferencia de que este certificado se usará
también como certificado predeterminado. Es posible añadir varios certificados predeterminados para
tener uno ECDSA y uno RSA; tener más no es realmente útil.

Esta opción no deshabilita los certificados predeterminados implícitos: si un certificado 'crt' se
declara primero antes que cualquier 'default-crt' u otro 'crt', se seguirá usando como certificado
predeterminado.

Un certificado predeterminado se usa cuando no se emplea la opción "strict-sni" en la línea bind. Se
proporciona un certificado predeterminado cuando el cliente no usó la extensión servername, o cuando
el servername no coincide con ningún certificado configurado.

Ejemplo:

```shell
# this bind line has 2 default certificates
bind *:443 default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa crt website.pem.rsa

# this bind line has 3 default certificates
bind *:443 crt website.pem.rsa default-crt foobar.pem.rsa default-crt foobar.pem.ecdsa
```

Ver también la palabra clave "crt".

<a id="entry-5-1-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de curvas elípticas ("curve suite") que se negocian durante el
handshake SSL/TLS con ECDHE. El formato de la cadena es una lista de nombres de curva delimitada por
dos puntos. Ejemplo: "X25519:P-256" (sin comillas). Cuando se define "curves", el parámetro "ecdhe"
se ignora.

<a id="entry-5-1-defer-accept"></a>

**`defer-accept`**

```haproxy
defer-accept
```

Es una palabra clave opcional que solo está soportada en ciertos kernels de Linux. Indica que una
conexión solo se aceptará una vez lleguen datos por ella o, en el peor de los casos, tras la primera
retransmisión. Debería usarse solo en protocolos en los que el cliente habla primero (p. ej. HTTP).
Puede mejorar ligeramente el rendimiento al asegurar que la mayor parte de la solicitud ya está
disponible cuando se acepta la conexión. Por el contrario, no permitirá detectar las conexiones que
no hablan. Es importante señalar que esta opción está rota en todos los kernels hasta 2.6.31, ya que
la conexión nunca se acepta hasta que el cliente habla. Esto puede causar problemas con los
firewalls delanteros, que verían una conexión establecida mientras el proxy solo la verá en estado
SYN_RECV. Esta opción solo está soportada en sockets TCPv4/TCPv6 y es ignorada por los demás.

<a id="entry-5-1-ecdhe"></a>

**`ecdhe <named curve>`**

```haproxy
ecdhe <named curve>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la curva con
nombre (RFC 4492) usada para generar claves efímeras ECDH. Por defecto, la curva con nombre usada es
prime256v1.

<a id="entry-5-1-ech"></a>

**`ech <dir> [ EXPERIMENTAL ]`**

```haproxy
ech <dir> [ EXPERIMENTAL ]
```

Aplica todas las claves ECH de `<dir>` a la línea bind. Los archivos deben tener la extensión .ech y
usar el formato de archivo PEM para ECH. ( <https://datatracker.ietf.org/doc/draft-farrell-tls-pemesni/> )

Esta palabra clave habilita ECH en modo compartido, con HAProxy actuando tanto como extremo TLS como
extremo ECH. Ver <https://datatracker.ietf.org/doc/draft-ietf-tls-esni/>

Se trata de una funcionalidad experimental que requiere la opción
"expose-experimental-directives" en la sección global. También necesita una versión de OpenSSL que
soporte ECH ( <https://github.com/openssl/openssl/tree/feature/ech> ) y HAProxy debe compilarse con
USE_ECH=1. La API ECH de AWS-LC no está soportada.

Ejemplo:

```shell
$ openssl ech -public_name foobar.com -out /etc/haproxy/echkeydir/foobar.com.ech

$ cat haproxy.cfg
[...]
bind :443 ech /etc/haproxy/echkeydir/ ssl crt example.com.pem

// Use the ECHCONFIG section of your .ech file
$ openssl s_client -tls1_3 -connect example.com:443 -servername example.com \
-ech_config_list AD3+DQA5cwAgACB6ybtgtFYoM5r8nJSotus4c7K0EG..9vYmFyLmNvbQAA
```

<a id="entry-5-1-expose-fd-listeners"></a>

**`expose-fd listeners`**

```haproxy
expose-fd listeners
```

Esta opción solo es utilizable con el socket de estadísticas. Da a tu socket de estadísticas la
capacidad de pasar los FD de los listeners a otro proceso HAProxy. En modo master-worker esto ya no
es necesario: los listeners se pasarán mediante los pares de sockets internos entre el master y los
workers. Ver también "-x" en la guía de gestión.

<a id="entry-5-1-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Esta opción fuerza el uso exclusivo de SSLv3 en las conexiones SSL instanciadas desde este listener.
SSLv3 es generalmente menos costoso que sus equivalentes TLS para tasas de conexión altas. Esta
opción también está disponible en la directiva global "ssl-default-bind-options". Ver también
"ssl-min-ver" y "ssl-max-ver".

<a id="entry-5-1-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Esta opción fuerza el uso exclusivo de TLSv1.0 en las conexiones SSL instanciadas desde este
listener. Esta opción también está disponible en la directiva global "ssl-default-bind-options". Ver
también "ssl-min-ver" y "ssl-max-ver".

<a id="entry-5-1-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Esta opción fuerza el uso exclusivo de TLSv1.1 en las conexiones SSL instanciadas desde este
listener. Esta opción también está disponible en la directiva global "ssl-default-bind-options". Ver
también "ssl-min-ver" y "ssl-max-ver".

<a id="entry-5-1-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Esta opción fuerza el uso exclusivo de TLSv1.2 en las conexiones SSL instanciadas desde este
listener. Esta opción también está disponible en la directiva global "ssl-default-bind-options". Ver
también "ssl-min-ver" y "ssl-max-ver".

<a id="entry-5-1-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Esta opción fuerza el uso exclusivo de TLSv1.3 en las conexiones SSL instanciadas desde este
listener. Esta opción también está disponible en la directiva global "ssl-default-bind-options". Ver
también "ssl-min-ver" y "ssl-max-ver".

<a id="entry-5-1-generate-certificates"></a>

**`generate-certificates`**

```haproxy
generate-certificates
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Habilita la
generación dinámica de certificados SSL. Son necesarios un certificado de CA y su clave privada (ver
'ca-sign-file'). Cuando HAProxy se configura como proxy directo transparente, las solicitudes SSL
generan errores debido a un desajuste del nombre común en el certificado presentado al cliente. Con
esta opción habilitada, HAProxy intentará falsificar un certificado usando el nombre de host SNI
indicado por el cliente. Esto se hace solo si ningún certificado coincide con el nombre de host SNI
(ver 'crt-list').

En caso de error de generación de certificado, la conexión retrocederá al certificado predeterminado.
Al usar 'strict-sni', el certificado predeterminado no se usará y la conexión resultará en un fallo
del handshake.

También puede usarse cuando HAProxy se configura como proxy inverso para facilitar el despliegue de
una arquitectura con muchos backends.

Crear un certificado SSL es una operación costosa, de modo que se usa una caché LRU para almacenar
los certificados falsificados (ver 'tune.ssl.ssl-ctx-cache-size'). Esto incrementa el consumo de
memoria de HAProxy para reducir la latencia cuando el mismo certificado se usa muchas veces.

<a id="entry-5-1-gid"></a>

**`gid <gid>`**

```haproxy
gid <gid>
```

Fija el grupo de los sockets UNIX al gid del sistema designado. También puede establecerse por
defecto en la directiva "unix-bind" de la sección global. Ten en cuenta que algunas plataformas simplemente
lo ignoran. Este parámetro es equivalente al parámetro "group", excepto que se usa el ID de grupo en
lugar de su nombre. Este parámetro es ignorado por los sockets que no son UNIX.

<a id="entry-5-1-group"></a>

**`group <group>`**

```haproxy
group <group>
```

Fija el grupo de los sockets UNIX al grupo del sistema designado. También puede establecerse por
defecto en la directiva "unix-bind" de la sección global. Ten en cuenta que algunas plataformas simplemente
lo ignoran. Este parámetro es equivalente al parámetro "gid", excepto que se usa el nombre del grupo
en lugar de su gid. Este parámetro es ignorado por los sockets que no son UNIX.

<a id="entry-5-1-guid-prefix"></a>

**`guid-prefix <string>`**

```haproxy
guid-prefix <string>
```

Genera IDs globales únicos, sensibles a mayúsculas y minúsculas, para cada socket en escucha
asignado en esta línea bind. El prefijo se concatenará con el índice de posición de los listeners en
la línea bind actual, usando el carácter '-' como separador. Ver la descripción de la palabra clave
"guid" de proxy para más información sobre su formato. Ver también "shm-stats-file".

<a id="entry-5-1-id"></a>

**`id <id>`**

```haproxy
id <id>
```

Fija el ID del socket. Por defecto, los IDs de socket se asignan automáticamente, pero a veces es
más cómodo fijarlos para facilitar la supervisión. Este valor debe ser estrictamente positivo y único
dentro del listener/frontend. Esta opción solo puede usarse al definir un único socket.

<a id="entry-5-1-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Puede usarse en los siguientes contextos: tcp, http, log

Define un intervalo para comprobar periódicamente la vitalidad de las conexiones inactivas del
frontend. Si el par no puede responder antes de la siguiente prueba programada, la conexión se
cierra. En caso contrario, el tiempo de espera del cliente se refresca y la conexión se mantiene.
Ten en cuenta que los temporizadores http-request/http-keep-alive funcionan en paralelo y no los refresca
idle-ping.

Esta funcionalidad depende del soporte del protocolo subyacente específico. Por ahora, solo el mux
H2 la implementa. Idle-ping simplemente es ignorado por otros protocolos.

Esta opción es particularmente útil al usar reverse HTTP. Definirla en la línea bind es útil para el
par encargado de iniciar activamente las conexiones y que luego recibirá por ellas el tráfico
entrante.

<a id="entry-5-1-interface"></a>

**`interface <interface>`**

```haproxy
interface <interface>
```

Restringe el socket a una interfaz específica. Cuando se especifica, solo los paquetes recibidos de
esa interfaz en particular son procesados por el socket. Esto actualmente solo está soportado en
Linux. La interfaz debe ser una interfaz primaria del sistema, no una interfaz con alias. También es
posible vincular varios frontends a la misma dirección si están ligados a interfaces diferentes.
Ten en cuenta que vincular a una interfaz de red requiere privilegios de root. Este parámetro solo es
compatible con sockets TCPv4/TCPv6. Cuando se especifica, el tráfico de retorno usa la misma
interfaz que el tráfico entrante y su tabla de enrutamiento asociada, incluso si hay rutas
explícitas configuradas a través de interfaces diferentes. Esto puede resultar útil para abordar
problemas de enrutamiento asimétrico cuando las mismas direcciones IP de cliente deben poder
alcanzar frontends alojados en interfaces diferentes.

<a id="entry-5-1-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Habilita o deshabilita ktls para estos sockets. Si se habilita, se usará kTLS si el kernel lo
soporta y el cifrado es compatible. Esto solo está disponible en Linux kernel 4.17 y posteriores.
Ten en cuenta que algunos controladores de red y/o pilas TLS podrían restringir el uso de kTLS solo
a TLS v1.2. Ver también "force-tlsv12".

<a id="entry-5-1-label"></a>

**`label <label>`**

```haproxy
label <label>
```

Define una etiqueta opcional para estos sockets. Podría usarse para agrupar sockets por etiqueta, con
independencia de dónde se declararan las líneas bind.

<a id="entry-5-1-level"></a>

**`level <level>`**

```haproxy
level <level>
```

Este parámetro se usa únicamente con los sockets de estadísticas para restringir la naturaleza de los
comandos que pueden emitirse en el socket. Es ignorado por los demás sockets. `<level>` puede ser uno
de:

- "user" es el nivel con menos privilegios; solo pueden leerse las estadísticas no sensibles y no se
  permite ningún cambio. Tiene sentido en sistemas donde no es fácil restringir el acceso al socket.
- "operator" es el nivel por defecto y encaja con los usos más comunes. Pueden leerse todos los
  datos y solo se permiten cambios no sensibles (p. ej. limpiar los contadores max).
- "admin" debería usarse con cuidado, ya que todo está permitido (p. ej. limpiar todos los
  contadores).

<a id="entry-5-1-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Limita los sockets a este número de conexiones concurrentes. Las conexiones excedentes permanecerán
en el backlog del sistema hasta que se libere una conexión. Si no se especifica, el límite será el
mismo que el maxconn del frontend. Ten en cuenta que en caso de rangos de puertos o direcciones múltiples,
se aplicará el mismo valor a cada socket. Este parámetro permite limitaciones diferentes en sockets
costosos, por ejemplo las entradas SSL, que pueden consumir fácilmente toda la memoria.

<a id="entry-5-1-mode"></a>

**`mode <mode>`**

```haproxy
mode <mode>
```

Define el modo octal usado para establecer los permisos de acceso en el socket UNIX. También puede
establecerse por defecto en la directiva "unix-bind" de la sección global. Ten en cuenta que algunas
plataformas simplemente lo ignoran. Este parámetro es ignorado por los sockets que no son UNIX.

<a id="entry-5-1-mss"></a>

**`mss <maxseg>`**

```haproxy
mss <maxseg>
```

Define el valor del MSS (Maximum Segment Size) de TCP que se anunciará en las conexiones entrantes.
Esto puede usarse para forzar un MSS menor para ciertos puertos específicos, por ejemplo para
conexiones que pasan por una VPN. Ten en cuenta que esto depende de una funcionalidad del kernel que está
teóricamente soportada en Linux pero tenía errores en todas las versiones anteriores a 2.6.28. Puede
o no funcionar en otros sistemas operativos. También podría no cambiar el valor anunciado sino el
tamaño efectivo de los segmentos salientes. El valor habitualmente anunciado para TCPv4 en redes
Ethernet es 1460 = 1500(MTU) - 40(IP+TCP). Si este valor es positivo, se usará como el MSS anunciado.
Si es negativo, indicará en cuánto reducir el MSS anunciado de la conexión entrante para los
segmentos salientes. Este parámetro solo es compatible con sockets TCP v4/v6.

<a id="entry-5-1-name"></a>

**`name <name>`**

```haproxy
name <name>
```

Define un nombre opcional para estos sockets, que se mostrará en la página de estadísticas.

<a id="entry-5-1-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

En Linux es posible especificar a qué espacio de nombres de red pertenecerá un socket. Esta
directiva permite vincular explícitamente un listener a un espacio de nombres distinto del
predeterminado. Consulta la documentación de tu sistema operativo para encontrar más detalles sobre
los espacios de nombres de red.

<a id="entry-5-1-nbconn"></a>

**`nbconn <nbconn> [ EXPERIMENTAL ]`**

```haproxy
nbconn <nbconn> [ EXPERIMENTAL ]
```

Este parámetro solo es válido para instancias de listener que usan reverse HTTP. Definirá el número
de conexiones que se montarán en paralelo. Si no se especifica, se usa un valor por defecto de 1.

Reverse HTTP está actualmente aún en desarrollo activo. El mecanismo de configuración puede cambiar
en el futuro. Por esta razón está marcado internamente como experimental, lo que significa que
"expose-experimental-directives" debe aparecer en una línea antes de esta directiva.

<a id="entry-5-1-nice"></a>

**`nice <nice>`**

```haproxy
nice <nice>
```

Define la "amabilidad" (niceness) de las conexiones iniciadas desde el socket. El valor debe estar
en el rango -1024..1024 inclusive y su valor por defecto es cero. Los valores positivos significan
que tales conexiones son más consideradas con las demás y ceden fácilmente su lugar en el
planificador. Por el contrario, los valores negativos significan que las conexiones quieren
ejecutarse con mayor prioridad que las demás. La diferencia solo se manifiesta bajo cargas altas,
cuando el sistema está cerca de la saturación. Los valores negativos son apropiados para servicios
de baja latencia o de administración, y los valores altos se recomiendan generalmente para tareas
intensivas de CPU como el procesado SSL o las transferencias masivas, menos sensibles a la latencia.
Por ejemplo, puede tener sentido usar un valor positivo para un socket SMTP y uno negativo para un
socket RDP.

<a id="entry-5-1-no-alpn"></a>

**`no-alpn`**

```haproxy
no-alpn
```

Deshabilita el procesamiento de ALPN (técnicamente hablando, define la cadena ALPN como una cadena
vacía que no se anunciará). Permite cancelar una aparición anterior de un parámetro "alpn" y
deshabilitar la negociación del protocolo de aplicación. También puede usarse para impedir que un
listener negocie ALPN con un cliente en un listener HTTPS o QUIC; por defecto, los listeners HTTPS
anunciarán "h2,http/1.1" y los listeners QUIC anunciarán "h3". Ver también "alpn" más arriba.
Ten en cuenta que, al usar "crt-list", un certificado puede anular el parámetro "alpn" y reactivar su
procesamiento.

<a id="entry-5-1-no-ca-names"></a>

**`no-ca-names`**

```haproxy
no-ca-names
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Impide enviar
nombres de CA en el mensaje server hello cuando se usa ca-file. Usa "ca-verify-file" en lugar de
"ca-file" junto con "no-ca-names".

<a id="entry-5-1-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita el
soporte de SSLv3 en cualquier socket instanciado desde el listener cuando se soporta SSL. Ten en cuenta que
SSLv2 está deshabilitado a la fuerza en el código y no puede habilitarse con ninguna opción de
configuración. Esta opción también está disponible en la directiva global
"ssl-default-bind-options". Usa "ssl-min-ver" y "ssl-max-ver" en su lugar.

<a id="entry-5-1-no-strict-sni"></a>

**`no-strict-sni`**

```haproxy
no-strict-sni
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita la
imposición de strict-sni procedente de una directiva "strict-sni" anterior. Puede ser necesario para
deshabilitar selectivamente el uso de strict-sni en una línea "bind" cuando ya se había impuesto
globalmente mediante "ssl-default-bind-options". Ver también la opción de bind "strict-sni".

<a id="entry-5-1-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita la
reanudación de sesión sin estado (extensión TLS Ticket de RFC 5077) y fuerza el uso de la reanudación
de sesión con estado. La reanudación sin estado es más costosa en uso de CPU. Esta opción también
está disponible en la directiva global "ssl-default-bind-options". El mecanismo de TLS ticket solo se
usa hasta TLS 1.2. El secreto hacia adelante (Forward Secrecy) queda comprometido con los TLS
tickets, salvo que las claves de los tickets se roten periódicamente (mediante un reload o usando
"tls-ticket-keys").

<a id="entry-5-1-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita el
soporte de TLSv1.0 en cualquier socket instanciado desde el listener cuando se soporta SSL. Ten en cuenta
que SSLv2 está deshabilitado a la fuerza en el código y no puede habilitarse con ninguna opción de
configuración. Esta opción también está disponible en la directiva global
"ssl-default-bind-options". Usa "ssl-min-ver" y "ssl-max-ver" en su lugar.

<a id="entry-5-1-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita el
soporte de TLSv1.1 en cualquier socket instanciado desde el listener cuando se soporta SSL. Ten en cuenta
que SSLv2 está deshabilitado a la fuerza en el código y no puede habilitarse con ninguna opción de
configuración. Esta opción también está disponible en la directiva global
"ssl-default-bind-options". Usa "ssl-min-ver" y "ssl-max-ver" en su lugar.

<a id="entry-5-1-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita el
soporte de TLSv1.2 en cualquier socket instanciado desde el listener cuando se soporta SSL. Ten en cuenta
que SSLv2 está deshabilitado a la fuerza en el código y no puede habilitarse con ninguna opción de
configuración. Esta opción también está disponible en la directiva global
"ssl-default-bind-options". Usa "ssl-min-ver" y "ssl-max-ver" en su lugar.

<a id="entry-5-1-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Deshabilita el
soporte de TLSv1.3 en cualquier socket instanciado desde el listener cuando se soporta SSL. Ten en cuenta
que SSLv2 está deshabilitado a la fuerza en el código y no puede habilitarse con ninguna opción de
configuración. Esta opción también está disponible en la directiva global
"ssl-default-bind-options". Usa "ssl-min-ver" y "ssl-max-ver" en su lugar.

<a id="entry-5-1-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Esto habilita la extensión NPN de TLS y anuncia la lista de protocolos especificada como soportada
sobre NPN. La lista de protocolos consiste en una lista de nombres de protocolo delimitados por
comas, por ejemplo: "http/1.1,http/1.0" (sin comillas). Esto requiere que la biblioteca SSL se haya
compilado con el soporte para extensiones TLS habilitado (compruébalo con haproxy -vv). Ten en cuenta que la
extensión NPN ha sido sustituida por la extensión ALPN (ver la palabra clave "alpn"), aunque esta
última solo está disponible a partir de OpenSSL 1.0.2. Si se desea HTTP/2 con una versión de OpenSSL
anterior, NPN puede seguir usándose, ya que la mayoría de los clientes aún la soportan al momento de
escribir esto. Es posible habilitar tanto NPN como ALPN, aunque probablemente no tenga sentido fuera
de pruebas.

Compatibilidad: OpenSSL >= 1.0.1. No compatible con AWS-LC.

<a id="entry-5-1-prefer-client-ciphers"></a>

**`prefer-client-ciphers`**

```haproxy
prefer-client-ciphers
```

Usa la preferencia del cliente al seleccionar el cipher suite; por defecto se impone la preferencia
del servidor. Esta opción también está disponible en la directiva global
"ssl-default-bind-options".

Ten en cuenta que con OpenSSL \>= 1.1.1 ChaCha20-Poly1305 se reprioriza de todos modos (sin definir esta
opción) si un cifrado ChaCha20-Poly1305 está al principio de la lista de cifrados del cliente.

Al usar una configuración de algoritmos duales (RSA + ECDSA), el algoritmo de selección elegirá
entre RSA y ECDSA y siempre priorizará ECDSA. Una vez elegido el certificado correcto, dejará que la
biblioteca SSL priorice los cifrados, las curvas, etc. Esto significa que esta opción no puede usarse
para priorizar un certificado RSA sobre uno ECDSA.

<a id="entry-5-1-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Fuerza el protocolo del multiplexor que se usará para las conexiones entrantes. Debe ser compatible
con el modo del frontend (TCP o HTTP). También debe ser utilizable en el lado del frontend. La lista
de protocolos disponibles se muestra en haproxy -vv. Se reportan las propiedades de los protocolos:
el modo (TCP/HTTP), el lado (FE/BE), el nombre del mux y sus flags.

Algunos protocolos están sujetos al bloqueo de cabecera de línea en el lado del servidor
(flag=HOL_RISK). Finalmente, algunos protocolos no admiten cambios de protocolo (flag=NO_UPG). También se
reporta la compatibilidad HTX (flag=HTX).

Estos son los protocolos que pueden usarse como argumento de una directiva "proto" en una línea
bind:

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
 qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
 h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
 h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
 none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
```

La idea detrás de esta opción es saltarse la selección del mejor protocolo de multiplexado para todas
las conexiones instanciadas desde este socket en escucha. Por ejemplo, es posible forzar http/2 sobre
TCP sin cifrar especificando "proto h2" en la línea bind.

Si los parámetros ALPN o NPN están configurados, los protocolos especificados deberían ser
compatibles con el protocolo del multiplexor para evitar cualquier problema. Por ejemplo, si se
define "proto h1", el ALPN no debería definirse como "h2".

QMux es un subconjunto de QUIC que funciona sobre TCP. Corresponde al siguiente protocolo en borrador
<https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. Por ahora se considera experimental
en haproxy.

<a id="entry-5-1-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Este es un parámetro específico de QUIC para seleccionar el algoritmo de control de congestión para
cualquier intento de conexión a los listeners QUIC configurados. Son similares a los usados por TCP.

El pacing se activa sobre el algoritmo de congestión para reducir las pérdidas y mejorar el
rendimiento. Puede desactivarse mediante la palabra clave global "tune.quic.fe.tx.pacing". En la
mayoría de los casos, el pacing debería permanecer activado, especialmente al usar BBR, ya que este
depende de él para funcionar como se espera. Usar BBR sin pacing puede causar ralentizaciones o tasas
de pérdida altas durante las transferencias.

Valor por defecto: cubic

Para una personalización adicional, puede especificarse una lista de parámetros después del token del
algoritmo. Debe escribirse entre paréntesis, separada por comas. Cada argumento es opcional y puede
quedar vacío si es necesario. Este es el orden obligatorio de cada parámetro:

- tamaño máximo de la ventana en bytes. Debe ser mayor que 10k y menor que 4g. Por defecto se usa el
  valor "tune.quic.fe.cc.max-win-size".

Ejemplo:

```shell
# newreno congestion control algorithm
quic-cc-algo newreno
# cubic congestion control algorithm with one megabytes as window
quic-cc-algo cubic(1m)
```

Puede usarse un valor especial "nocc" para forzar una ventana de congestión fija siempre definida al
tamaño máximo. Está reservado para escenarios de depuración, para eliminar cualquier efecto
secundario causado por el controlador de congestión. No debe usarse en producción, ya que puede
provocar rápidamente problemas de red tales como una tasa de pérdida alta.

<a id="entry-5-1-quic-force-retry"></a>

**`quic-force-retry`**

```haproxy
quic-force-retry
```

Este es un parámetro específico de QUIC que fuerza el uso de la funcionalidad QUIC Retry para todos
los intentos de conexión a los listeners QUIC configurados. Consiste en verificar que los pares
pueden recibir paquetes en la dirección de transporte que usaron para iniciar una nueva conexión,
enviándoles un paquete Retry que contiene un token. Este token debe devolverse al remitente del
paquete Retry, siendo este último el único capaz de validar el token. Ten en cuenta que QUIC Retry se usará
siempre, incluso si se definió un umbral de Retry (ver el parámetro
"tune.quic.fe.sec.retry-threshold").

Este parámetro requiere que el secreto del clúster esté definido; de lo contrario se reportará un
error al arrancar (ver "cluster-secret").

Ver <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2> para más información sobre QUIC
retry.

<a id="entry-5-1-quic-socket"></a>

**`quic-socket [ connection | listener ]`**

```haproxy
quic-socket [ connection | listener ]
```

Este parámetro específico de QUIC permite definir el modo de asignación de sockets para los listeners
específicos. Ver "tune.quic.fe.sock-per-conn" para una descripción completa de los pros y los contras
de cada modo.

Este parámetro se aplica junto con la opción global "tune.quic.fe.sock-per-conn". Si el modo
"default-on" está activo en el ajuste global (este es el valor por defecto), cada conexión QUIC usará
su propio socket, excepto los listeners con "quic-socket listener". Sin embargo, si el modo global se
define como "force-off", la configuración individual del listener será ignorada.

<a id="entry-5-1-severity-output"></a>

**`severity-output <format>`**

```haproxy
severity-output <format>
```

Este parámetro se usa únicamente con los sockets de estadísticas, para configurar la salida del nivel
de severidad que se antepone a los mensajes informativos de respuesta. El nivel de severidad de los
mensajes puede variar entre 0 y 7, conforme al syslog rfc5424. Los comandos de socket válidos y
exitosos que solicitan datos (es decir, "show map", "get acl foo", etc.) nunca llevarán antepuesto un
nivel de severidad. Es ignorado por los demás sockets. `<format>` puede ser uno de:

- "none" (predeterminado) no se antepone ningún nivel de severidad a los mensajes de respuesta.
- "number" el nivel de severidad se antepone como un número.
- "string" el nivel de severidad se antepone como una cadena conforme a la convención rfc5424.

<a id="entry-5-1-shards"></a>

**`shards { <number> | by-thread | by-group }`**

```haproxy
shards { <number> | by-thread | by-group }
```

En modo multi-hilo, en sistemas operativos que soportan múltiples listeners en el mismo IP:port,
esto creará automáticamente ese número de listeners idénticos para la misma línea, todos ellos
ligados a una parte equitativa del número de hilos adjuntos a este listener. Esto puede ser útil a
veces al usar recuentos de hilos muy grandes, donde el bloqueo dentro del kernel sobre un único
socket empieza a causar una sobrecarga significativa. En este caso, el tráfico entrante se distribuye
entre múltiples sockets y la contención se reduce. Ten en cuenta que hacer esto puede incrementar
fácilmente el uso de CPU al hacer que más hilos trabajen un poco.

Si el número de shards es mayor que el número de hilos disponibles, se recortará automáticamente al
número de hilos (es decir, un shard por hilo). El valor especial "by-thread" también crea tantos
shards como hilos haya en la línea "bind". Dado que el sistema distribuirá uniformemente el tráfico
entrante entre todos estos shards, es importante que este número sea un divisor entero del número de
hilos. Alternativamente, el otro valor especial "by-group" creará un shard por grupo de hilos. Esto
puede ser útil cuando se trabaja con muchos hilos y no se quieren crear demasiados sockets. La
distribución de carga será algo menos óptima, pero la contención (especialmente en el sistema)
seguirá siendo menor que con un único socket.

En sistemas operativos que no soportan múltiples sockets ligados a la misma dirección, "by-thread" y
"by-group" retrocederán automáticamente a un único shard. Para "by-group" esto se hace sin ninguna
advertencia, ya que no cambia nada para un único grupo, y dará como resultado sockets duplicados por
cada grupo de todos modos. Sin embargo, para "by-thread" se emitirá una advertencia de diagnóstico
si esto ocurre, ya que el número resultante de listeners no será el esperado.

<a id="entry-5-1-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de firma que se negocian durante el handshake TLSv1.2 y TLSv1.3. El
formato de la cadena está definido en "man 3 SSL_CTX_set1_sigalgs" de las páginas man de OpenSSL. No
se recomienda usar este parámetro salvo que se requiera compatibilidad con un middlebox.

<a id="entry-5-1-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Habilita el
descifrado SSL en las conexiones instanciadas desde este listener. Es necesario un certificado (ver
"crt" más arriba). Todo el contenido de los búferes aparecerá en texto claro, de modo que las ACL y
el procesado HTTP solo tendrán acceso al contenido descifrado. SSLv3 está deshabilitado por defecto;
usa "ssl-min-ver SSLv3" para habilitarlo.

<a id="entry-5-1-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Esta opción fuerza el uso de `<version>` o inferior en las conexiones SSL instanciadas desde este
listener. Usar este parámetro sin "ssl-min-ver" puede ser ambiguo, porque el valor por defecto de
ssl-min-ver podría cambiar en futuras versiones de HAProxy. Esta opción también está disponible en
la directiva global "ssl-default-bind-options". Ver también "ssl-min-ver".

<a id="entry-5-1-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Esta opción fuerza el uso de `<version>` o superior en las conexiones SSL instanciadas desde este
listener. El valor por defecto es "TLSv1.2". Esta opción también está disponible en la directiva
global "ssl-default-bind-options". Ver también "ssl-max-ver".

<a id="entry-5-1-strict-sni"></a>

**`strict-sni`**

```haproxy
strict-sni
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. La negociación
SSL/TLS solo se permite si el cliente proporcionó un SNI que coincide con un certificado. El
certificado predeterminado no se usa. Esta opción también permite arrancar sin ningún certificado en
una línea bind, de modo que podría usarse un directorio vacío y llenarse más tarde desde el socket de
estadísticas. Esta opción también está disponible en la directiva global
"ssl-default-bind-options" y puede deshabilitarse selectivamente en una línea "bind" usando
"no-strict-sni". Ver la opción "crt" para más información. Ver el comando "add ssl crt-list" en la
guía de gestión.

<a id="entry-5-1-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Habilita la firma MD5 de TCP (RFC 2385 Protection of BGP Sessions via the TCP MD5 Signature Option)
para todas las conexiones entrantes instanciadas desde este socket en escucha. Esta opción solo está
disponible en Linux. Cuando está habilitada, la cadena `<password>` se usa para firmar cada segmento
TCP con un resumen MD5 de 16 bytes. Esto protegerá la conexión TCP contra la suplantación. El caso de
uso principal de esta opción es permitir que BGP se proteja contra la introducción de segmentos TCP
suplantados en el flujo de la conexión. Pero puede ser útil para cualquier conexión TCP de muy larga
duración.

<a id="entry-5-1-tcp-ss"></a>

**`tcp-ss <mode>`**

```haproxy
tcp-ss <mode>
```

Define la opción TCP Save SYN para todas las conexiones entrantes instanciadas desde este socket en
escucha. Esta opción está disponible en Linux desde la versión 4.3. Indica al kernel que intente
conservar una copia del paquete IP entrante que contiene el flag TCP SYN, para su inspección
posterior mediante la función de obtención de muestras "fc_saved_syn". La opción conoce 3 modos: - 0
el guardado de paquetes SYN está deshabilitado, este es el valor por defecto - 1 el guardado de
paquetes SYN está habilitado y contiene las cabeceras IP y TCP - 2 el guardado de paquetes SYN está
habilitado y contiene las cabeceras ETH, IP y TCP

Esto solo funciona para conexiones TCP normales y se ignora para otros protocolos (p. ej. sockets
UNIX). Ver también "fc_saved_syn".

<a id="entry-5-1-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Define el TCP User Timeout para todas las conexiones entrantes instanciadas desde este socket en
escucha. Esta opción está disponible en Linux desde la versión 2.6.37. Permite que HAProxy configure
un tiempo de espera para sockets que contienen datos que no reciben un reconocimiento durante el
retardo configurado. Esto es especialmente útil en conexiones de larga duración que experimentan
largos periodos de inactividad, como terminales remotos o grupos de conexiones de bases de datos,
donde los tiempos de espera del cliente y del servidor deben permanecer altos para permitir un largo
periodo de inactividad, pero donde es importante detectar que el cliente ha desaparecido para liberar
todos los recursos asociados a su conexión (y a la sesión del servidor). El argumento es un retardo
expresado por defecto en milisegundos. Esto solo funciona para conexiones TCP normales y se ignora
para otros protocolos.

<a id="entry-5-1-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Es una palabra clave opcional que solo está soportada en kernels de Linux \>= 3.7. Habilita TCP Fast
Open en el socket en escucha, lo que significa que los clientes que soportan esta funcionalidad
podrán enviar una solicitud y recibir una respuesta durante el handshake de 3 vías a partir de la
segunda conexión, ahorrando así un viaje de ida y vuelta tras la primera conexión. Esto solo tiene
sentido con protocolos que usan tasas de conexión altas y donde cada viaje de ida y vuelta importa.
Esto posiblemente puede causar problemas con muchos firewalls que no aceptan datos en paquetes SYN,
por lo que esta opción solo debería habilitarse una vez bien probada. Esta opción solo está soportada
en sockets TCPv4/TCPv6 y es ignorada por los demás. Puede que necesites compilar HAProxy con
USE_TFO=1 si tu libc no define TCP_FASTOPEN.

<a id="entry-5-1-thread"></a>

**`thread [<thread-group>/]<thread-set>[,...]`**

```haproxy
thread [<thread-group>/]<thread-set>[,...]
```

Esto restringe la lista de hilos en los que este listener puede ejecutarse. No fuerza ninguno de
ellos, pero elimina los que no coinciden. Limita los hilos autorizados a procesar las conexiones
entrantes de este listener.

Hay dos esquemas de numeración. Por defecto, los números de hilo son absolutos en el proceso, entre 1
y el valor especificado en global.nbthread. También es posible designar un número de hilo usando su
número relativo dentro de su grupo de hilos, especificando primero el número del grupo de hilos,
luego una barra ('/') y el número o números de hilo relativos. En este caso, los números de hilo
también empiezan en 1 y terminan en 32 o 64 dependiendo de la plataforma. Cuando se especifican
números de hilo absolutos, se traducirán automáticamente a números relativos una vez que se conozcan
los grupos de hilos. Normalmente se prefieren los números absolutos para configuraciones simples, y
los relativos para configuraciones complejas donde la disposición de la CPU importa para el
rendimiento.

Tras el número opcional de grupo de hilos, la especificación "thread-set" debe usar el siguiente
formato:

```text
"all" | "odd" | "even" | [number][-[number]]
```

Como sus nombres indican, "all" valida todos los hilos del conjunto (bien todos los del grupo cuando
se especifica un grupo, bien todos los hilos del proceso), "odd" valida todos los hilos de
numeración impar (uno de cada dos hilos empezando por el 1), ya sea para el proceso o para el grupo,
y "even" valida todos los hilos de numeración par (uno de cada dos hilos empezando por el 2). Si en
cambio se usan rangos de números de hilo, se validan todos los hilos incluidos en el rango desde el
primer hasta el último número de hilo. Los números son relativos al grupo o absolutos dependiendo de
la presencia de un número de grupo de hilos. Si se omite el primer número de hilo, se usa "1", que
representa bien el primer hilo del grupo o el primer hilo del proceso. Si se omite el último número
de hilo, se usa bien el último número de hilo del grupo (32 o 64) o el último número de hilo del
proceso (global.nbthread).

Estos rangos pueden repetirse y delimitarse por una coma, de modo que puedan especificarse conjuntos
de hilos no contiguos, y el grupo, si está presente, debe especificarse de nuevo para cada rango
nuevo. Ten en cuenta que no está permitido mezclar especificaciones relativas al grupo y absolutas, porque
la línea "bind" completa debe usar una notación absoluta o una relativa, ya que las no definidas se
resolverán al final del análisis.

Es importante saber que cada listener descrito por una línea "bind" crea al menos un socket
representado por al menos un descriptor de archivo. Dado que los descriptores de archivo no pueden
abarcar varios grupos de hilos, si una línea "bind" especifica un rango de hilos que cubre más de un
grupo, se crearán automáticamente varios descriptores de archivo para que haya al menos uno por
grupo. Técnicamente hablando, todos se refieren al mismo socket en el kernel, pero recibirán un
identificador distinto en haproxy e incluso tendrán una entrada de estadísticas dedicada si se usa
"option socket-stats".

El propósito principal es tener múltiples líneas bind que compartan el mismo IP:port pero no el
mismo hilo en un listener, de modo que el sistema pueda distribuir las conexiones entrantes en
múltiples colas, saltándose el balanceo interno de colas de haproxy. Actualmente se sabe que Linux
3.9 y posteriores soportan esto. Ver también la palabra clave "shards" más arriba, que automatiza la
duplicación de líneas "bind" y su asignación a múltiples grupos de hilos.

Esta palabra clave es compatible con los bind de reverse HTTP. Sin embargo, está prohibido
especificar un conjunto de hilos que abarque varios grupos de hilos para tal listener, ya que esto
podría hacer que "nbconn" no funcionara como se pretende.

<a id="entry-5-1-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Habilita la
reanudación de sesión sin estado (extensión TLS Ticket de RFC 5077). Es el comportamiento por
defecto, pero puede ser necesario reactivar selectivamente la funcionalidad en una línea "bind" si
se había deshabilitado globalmente mediante "no-tls-tickets" citado en
"ssl-default-bind-options". Ver también la palabra clave de bind "no-tls-tickets".

<a id="entry-5-1-tls-ticket-keys"></a>

**`tls-ticket-keys <keyfile>`**

```haproxy
tls-ticket-keys <keyfile>
```

Define el archivo de claves de TLS ticket del cual cargar las claves. Las claves deben tener una
longitud de 48 o 80 bytes, dependiendo de si se usa aes128 o aes256, codificadas con base64 con una
línea por clave (p. ej. openssl rand 80 \| openssl base64 -A \| xargs echo). La primera clave
determina la longitud de clave usada para las siguientes claves: no se pueden mezclar claves aes128 y
aes256. El número de claves lo especifica la opción de compilación TLS_TICKETS_NO (por defecto 3) y
al menos esas claves deben estar presentes en el archivo. Las últimas TLS_TICKETS_NO claves se
usarán para el descifrado y la penúltima para el cifrado. Esto permite una rotación de claves fácil
con solo añadir una clave nueva al archivo y recargar el proceso. Las claves deben rotarse
periódicamente (p. ej. cada 12h) o el Perfect Forward Secrecy queda comprometido. También es buena
idea mantener las claves fuera de cualquier almacenamiento permanente como los discos duros
(sugerencia: usa tmpfs y no intercambies esos archivos a swap). La sugerencia de duración puede
cambiarse con tune.ssl.timeout.

<a id="entry-5-1-transparent"></a>

**`transparent`**

```haproxy
transparent
```

Es una palabra clave opcional que solo está soportada en ciertos kernels de Linux. Indica que las
direcciones se vincularán incluso si no pertenecen a la máquina local y que los paquetes destinados
a cualquiera de estas direcciones serán interceptados igual que si las direcciones estuvieran
configuradas localmente. Esto normalmente requiere que el reenvío de IP esté habilitado.
¡Cuidado! no uses esto con la dirección predeterminada '\*', ya que redirigiría cualquier tráfico al
puerto especificado. Esta palabra clave solo está disponible cuando HAProxy se compila con
USE_LINUX_TPROXY=1. Este parámetro solo es compatible con sockets TCPv4 y TCPv6, dependiendo de la
versión del kernel. Algunos kernels de distribuciones incluyen retroportes de la funcionalidad, así
que comprueba el soporte con tu proveedor.

<a id="entry-5-1-uid"></a>

**`uid <uid>`**

```haproxy
uid <uid>
```

Fija el propietario de los sockets UNIX al uid del sistema designado. También puede establecerse por
defecto en la directiva "unix-bind" de la sección global. Ten en cuenta que algunas plataformas simplemente
lo ignoran. Este parámetro es equivalente al parámetro "user", excepto que se usa el ID numérico del
usuario en lugar de su nombre. Este parámetro es ignorado por los sockets que no son UNIX.

<a id="entry-5-1-user"></a>

**`user <user>`**

```haproxy
user <user>
```

Fija el propietario de los sockets UNIX al usuario del sistema designado. También puede establecerse
por defecto en la directiva "unix-bind" de la sección global. Ten en cuenta que algunas plataformas
simplemente lo ignoran. Este parámetro es equivalente al parámetro "uid", excepto que se usa el
nombre de usuario en lugar de su uid. Este parámetro es ignorado por los sockets que no son UNIX.

<a id="entry-5-1-v4v6"></a>

**`v4v6`**

```haproxy
v4v6
```

Es una palabra clave opcional que solo está soportada en los sistemas más recientes, incluidos los
kernels de Linux \>= 2.4.21. Se usa para vincular un socket tanto a IPv4 como a IPv6 cuando usa la
dirección predeterminada. Hacerlo a veces es necesario en sistemas que por defecto solo vinculan a
IPv6. No tiene efecto en sockets que no son IPv6 y es anulada por la opción "v6only".

<a id="entry-5-1-v6only"></a>

**`v6only`**

```haproxy
v6only
```

Es una palabra clave opcional que solo está soportada en los sistemas más recientes, incluidos los
kernels de Linux \>= 2.4.21. Se usa para vincular un socket solo a IPv6 cuando usa la dirección
predeterminada. Hacerlo a veces se prefiere a hacerlo en todo el sistema, ya que es por listener. No
tiene efecto en sockets que no son IPv6 y tiene precedencia sobre la opción "v4v6".

<a id="entry-5-1-verify"></a>

**`verify [none|optional|required]`**

```haproxy
verify [none|optional|required]
```

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Si se define como
'none', no se solicita el certificado del cliente. Este es el valor por defecto. En los demás casos,
se solicita un certificado de cliente. Si el cliente no proporciona un certificado tras la solicitud
y 'verify' está definido como 'required', el handshake se aborta, mientras que habría tenido éxito si
estuviera definido como 'optional'. El certificado proporcionado por el cliente siempre se verifica
usando las CA de 'ca-file' y las CRL opcionales de 'crl-file'. Ante un fallo de verificación el
handshake se aborta, independientemente de la opción 'verify', salvo que el código de error coincida
exactamente con uno de los listados con 'ca-ignore-err' o 'crt-ignore-err'.

## 5.2. Opciones de server y default-server {#section-5-2}

Las palabras clave "server" y "default-server" soportan cierto número de parámetros, todos pasados
como argumentos en la línea del servidor. El orden en que aparecen esos argumentos no cuenta y todos
son opcionales. Algunos de estos parámetros son palabras simples (booleanos), mientras que otros
esperan uno o varios valores a continuación. En este caso, los valores deben seguir inmediatamente al
nombre del parámetro. Excepto default-server, todos estos parámetros deben especificarse después de
la dirección del servidor si se usan:

```text
server <name> <address>[:port] [settings ...]
default-server [settings ...]
```

Ten en cuenta que todos estos parámetros están soportados tanto por las palabras clave "server" como
"default-server", excepto "id", que solo está soportado por "server".

Los parámetros soportados actualmente son los siguientes.

<a id="entry-5-2-addr"></a>

**`addr <ipv4|ipv6>`**

```haproxy
addr <ipv4|ipv6>
```

Puede usarse en los siguientes contextos: tcp, http, log

Usando el parámetro "addr" se hace posible usar una dirección IP diferente para enviar las
comprobaciones de estado o para sondear el agent-check. En algunos servidores puede ser deseable
dedicar una dirección IP a un componente específico capaz de realizar pruebas complejas más
adecuadas para las comprobaciones de estado que la aplicación. Este parámetro se ignora si el
parámetro "check" no está definido. Ver también el parámetro "port".

<a id="entry-5-2-agent-check"></a>

**`agent-check`**

```haproxy
agent-check
```

Puede usarse en los siguientes contextos: tcp, http, log

Habilita una comprobación de agente auxiliar que se ejecuta con independencia de una comprobación de
estado regular. Una comprobación de agente se realiza estableciendo una conexión TCP al puerto
definido por el parámetro "agent-port" y leyendo una cadena ASCII terminada por el primer '&#92;r' o
'&#92;n' que se encuentre. La cadena se compone de una serie de palabras delimitadas por espacios,
tabuladores o comas en cualquier orden, cada una consistente en:

- Una representación ASCII de un porcentaje entero positivo, p. ej. "75%". Los valores en este
  formato fijarán el peso proporcional al peso inicial de un servidor tal como se configuró cuando
  HAProxy arranca. Ten en cuenta que un peso cero se muestra en la página de estadísticas como "DRAIN",
  ya que tiene el mismo efecto en el servidor (queda eliminado de la granja de LB). Es la forma
  heredada de fijar el peso de un servidor. Es preferible definirlo con el prefijo "weight:".

- La cadena "weight:" seguida de un entero positivo o de un porcentaje entero positivo, sin espacio.
  Si el valor termina con el signo '%', el nuevo peso será proporcional al peso inicial del
  servidor. De lo contrario, el valor se considera un peso absoluto y debe estar entre 0 y 256. Los
  servidores que forman parte de una granja con un algoritmo de balanceo de carga estático tienen
  limitaciones más estrictas porque el peso no puede cambiar una vez definido. Así, para estos
  servidores, los únicos valores aceptados son 0 y 100% (o 0 y el peso inicial). Los cambios surten
  efecto inmediatamente, aunque ciertos algoritmos de LB requieren cierta cantidad de solicitudes
  para considerar los cambios. Ten en cuenta que un peso cero se muestra en la página de estadísticas como
  "DRAIN", ya que tiene el mismo efecto en el servidor (queda eliminado de la granja de LB).

- La cadena "maxconn:" seguida de un entero (sin espacio entre ambos). Los valores en este formato
  fijarán el maxconn de un servidor. El número máximo de conexiones anunciado debe multiplicarse por
  el número de balanceadores de carga y backends diferentes que usan esta comprobación de estado para
  obtener el número total de conexiones que el servidor podría recibir. Ejemplo: maxconn:30

- La palabra "ready". Esto pondrá el estado administrativo del servidor en el modo READY, cancelando
  así cualquier estado DRAIN o MAINT

- La palabra "drain". Esto pondrá el estado administrativo del servidor en el modo DRAIN, de modo que
  no aceptará ninguna conexión nueva aparte de las aceptadas mediante persistencia.

- La palabra "maint". Esto pondrá el estado administrativo del servidor en el modo MAINT, de modo que
  no aceptará ninguna conexión nueva en absoluto y se detendrán las comprobaciones de estado.

- Las palabras "down", "fail" o "stopped", seguidas opcionalmente de una cadena de descripción tras
  una almohadilla ('#'). Todas ellas marcan el estado operativo del servidor como DOWN, pero como la
  palabra en sí se muestra en la página de estadísticas, la diferencia permite a un administrador
  saber si la situación era esperada o no: el servicio puede estar detenido intencionadamente, puede
  parecer activo pero fallar algunas pruebas de validez, o puede verse como caído (p. ej. proceso
  inexistente o puerto que no responde).

- La palabra "up" restablece el estado operativo del servidor como UP si las comprobaciones de
  estado también reportan que el servicio es accesible.

Los parámetros que el agente no anuncia no se cambian. Por ejemplo, un agente podría diseñarse para
supervisar el uso de CPU y reportar únicamente un peso relativo, sin interactuar nunca con el estado
operativo. De forma similar, un agente podría diseñarse como interfaz de usuario final con 3 botones
de opción que permitan a un administrador cambiar solo el estado administrativo. Sin embargo, es
importante considerar que solo el agente puede revertir sus propias acciones, de modo que si un
servidor se pone en modo DRAIN o en estado DOWN usando el agente, el agente debe implementar las
demás acciones equivalentes para volver a poner el servicio en operación.

El fallo al conectar con el agente no se considera un error, ya que la conectividad la prueba la
comprobación de estado regular que habilita el parámetro "check". Advertencia sin embargo: no es
buena idea detener un agente después de que reporte "down", ya que solo un agente que reporte "up"
podrá volver a activar el servidor. Ten en cuenta que la CLI del socket de estadísticas Unix también puede
forzar el resultado de un agente para sortear un agente defectuoso si es necesario.

Requiere que el parámetro "agent-port" esté definido. Ver también los parámetros "agent-inter" y
"no-agent-check".

<a id="entry-5-2-agent-send"></a>

**`agent-send <string>`**

```haproxy
agent-send <string>
```

Puede usarse en los siguientes contextos: tcp, http, log

Si se especifica esta opción, HAProxy enviará la cadena dada (literalmente) al servidor del agente al
conectar. Podrías, por ejemplo, codificar el nombre del backend en esta cadena, lo que permitiría a
tu agente enviar respuestas diferentes según el backend. Asegúrate de incluir un '&#92;n' si quieres
terminar tu solicitud con un salto de línea.

<a id="entry-5-2-agent-inter"></a>

**`agent-inter <delay>`**

```haproxy
agent-inter <delay>
```

Puede usarse en los siguientes contextos: tcp, http, log

El parámetro "agent-inter" fija el intervalo entre dos comprobaciones del agente a `<delay>`
milisegundos. Si no se especifica, el retardo toma por defecto 2000 ms.

Al igual que con cualquier otro parámetro basado en tiempo, puede introducirse en cualquier otra
unidad explícita de entre { us, ms, s, m, h, d }. El parámetro "agent-inter" sirve también como
tiempo de espera para las comprobaciones del agente si no se define "timeout check". Para reducir los
efectos de "resonancia" cuando varios servidores están alojados en el mismo hardware, las
comprobaciones del agente y de estado de todos los servidores se inician con un pequeño desfase
temporal entre ellas. También es posible añadir algo de ruido aleatorio en el intervalo de las
comprobaciones del agente y de estado usando la palabra clave global "spread-checks". Esto tiene
sentido, por ejemplo, cuando muchos backends usan los mismos servidores.

Ver también los parámetros "agent-check" y "agent-port".

<a id="entry-5-2-agent-addr"></a>

**`agent-addr <addr>`**

```haproxy
agent-addr <addr>
```

Puede usarse en los siguientes contextos: tcp, http, log

El parámetro "agent-addr" define la dirección para la comprobación del agente.

Puedes descargar el agent-check en otro destino, de modo que puedas tener un único punto que gestione
el estado y los pesos de los servidores definidos en HAProxy en caso de que no puedas hacer
servicios conscientes de sí mismos y autogestionados. Puedes especificar tanto una IP como un nombre
de host; se resolverá.

<a id="entry-5-2-agent-port"></a>

**`agent-port <port>`**

```haproxy
agent-port <port>
```

Puede usarse en los siguientes contextos: tcp, http, log

El parámetro "agent-port" define el puerto TCP usado para las comprobaciones del agente.

Ver también los parámetros "agent-check" y "agent-inter".

<a id="entry-5-2-allow-0rtt"></a>

**`allow-0rtt`**

```haproxy
allow-0rtt
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Permite enviar early data al servidor cuando se usa TLS 1.3. Ten en cuenta que los early data solo se
enviarán si el cliente usó early data, o si el backend usa "retry-on" con la palabra clave
"0rtt-rejected". Con QUIC, 0rtt es compatible con QuicTLS, OpenSSL \>= 3.5.2 y AWS-LC. Con TCP/TLS,
0rtt solo es compatible con OpenSSL.

<a id="entry-5-2-alpn"></a>

**`alpn <protocols>`**

```haproxy
alpn <protocols>
```

Puede usarse en los siguientes contextos: tcp, http

Esto habilita la extensión ALPN de TLS y anuncia la lista de protocolos especificada como soportada
sobre ALPN. La lista de protocolos consiste en una lista de nombres de protocolo delimitados por
comas, por ejemplo: "http/1.1,http/1.0" (sin comillas). Esto requiere que la biblioteca SSL se haya
compilado con el soporte para extensiones TLS habilitado (compruébalo con haproxy -vv). La extensión
ALPN sustituye a la extensión NPN original. ALPN es necesario para conectarse a servidores HTTP/2.
También es necesario para poder usar HTTP/3 mediante un servidor QUIC; "h3" sirve como valor por
defecto para los servidores QUIC sin parámetro "alpn". Las versiones de OpenSSL anteriores a 1.0.2
no soportaban ALPN y solo admitían la hoy obsoleta extensión NPN. Si se espera soportar tanto HTTP/2
como HTTP/1.1, pueden anunciarse ambas versiones, en orden de preferencia, así:

```text
server 127.0.0.1:443 ssl crt pub.pem alpn h2,http/1.1
```

Ver también "ws" para usar un ALPN alternativo para los flujos websocket.

<a id="entry-5-2-backup"></a>

**`backup`**

```haproxy
backup
```

Puede usarse en los siguientes contextos: tcp, http, log

Cuando "backup" está presente en una línea de servidor, el servidor solo se usa en el balanceo de
carga cuando todos los demás servidores que no son de respaldo no están disponibles. Aun así, las
solicitudes que lleguen con una cookie de persistencia que referencie al servidor siempre serán
atendidas. Por defecto solo se usa el primer servidor de respaldo operativo, salvo que la opción
"allbackups" esté definida en el backend. Ver también las opciones "no-backup" y "allbackups".

<a id="entry-5-2-ca-file"></a>

**`ca-file <cafile>`**

```haproxy
ca-file <cafile>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM del cual cargar los certificados de CA usados para verificar el certificado del servidor. Es
posible cargar un directorio que contenga varias CA; en este caso HAProxy intentará cargar todo
".pem", ".crt", ".cer" y .crl" disponible en el directorio; los archivos que empiezan por un punto
se ignoran.

Para usar las CA de confianza de tu sistema, puede usarse el parámetro "@system-ca" en lugar del
cafile. La ubicación de este directorio puede sobrescribirse definiendo la variable de entorno
SSL_CERT_DIR.

<a id="entry-5-2-cc"></a>

**`cc <algo>`**

```haproxy
cc <algo>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible en sistemas que definen TCP_CONGESTION y se validó en Linux y
FreeBSD. Toma el nombre de un algoritmo de control de congestión TCP y configura las conexiones
salientes para usar este algoritmo. Los nombres típicos incluyen "reno" o "cubic" y dependerán del
sistema operativo. En algunos sistemas pueden requerirse permisos especiales para configurar ciertos
algoritmos. En Linux, los algoritmos disponibles se listan en el sysctl
"net.ipv4.tcp_available_congestion_control" y los permitidos sin privilegios están en
"net.ipv4.tcp_allowed_congestion_control". Para acceder a algoritmos que requieren permisos
adicionales puede necesitarse la capacidad "cap_net_admin" (ver "setcap" en la sección global). En
caso de fallo al configurar un algoritmo de control de congestión específico, el predeterminado
permanece sin cambios. Ver también: la palabra clave "cc" de bind ([sección 5.1](/es/haproxy/bind-and-server-options/#section-5-1)).

<a id="entry-5-2-check"></a>

**`check`**

```haproxy
check
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción habilita las comprobaciones de estado en un servidor: - cuando no está definida, no se
realiza ninguna comprobación de estado y el servidor se considera siempre disponible. - cuando está
definida y no se configura ningún otro método de comprobación, el servidor se considera disponible
cuando puede establecerse una conexión en la capa de transporte más alta configurada. Esto significa
TCP por defecto, o SSL/TLS cuando se definen "ssl" o "check-ssl", ambos posiblemente combinados con
prefijos de conexión tales como una cabecera de protocolo PROXY cuando se definen "send-proxy" o
"check-send-proxy". Este comportamiento es ligeramente diferente para los servidores dinámicos; lee
los párrafos siguientes para más detalles. - cuando está definida y hay definida una comprobación de
estado a nivel de aplicación, los intercambios a nivel de aplicación se realizan sobre la capa de
transporte configurada y el servidor se considera disponible si todos los intercambios tienen éxito.

Por defecto, las comprobaciones de estado se realizan en la misma dirección y puerto configurados en
el servidor, usando los mismos parámetros de encapsulación (SSL/TLS, cabecera proxy-protocol,
etc...). Es posible cambiar la dirección de destino usando "addr" y el puerto usando "port". Al
hacerlo, se asume que el servidor no se comprueba en el puerto del servicio y que los parámetros de
encapsulación configurados no se reutilizan. Hay que definir explícitamente "check-send-proxy" para
enviar cabeceras de conexión, o "check-ssl" para usar SSL/TLS.

Ten en cuenta que la configuración implícita de ssl y del protocolo PROXY no se realiza para los servidores
dinámicos. En este caso, es necesario usar explícitamente "check-ssl" y "check-send-proxy" cuando se
desea, incluso si el puerto de comprobación no está sobrescrito.

Cuando "sni" o "alpn" están definidos en la línea del servidor, su valor no se usa para las
comprobaciones de estado y hay que usar "check-sni" o "check-alpn".

La dirección de origen por defecto para el tráfico de comprobación de estado es la misma que la
definida en el backend. Puede cambiarse con la palabra clave "source".

El intervalo entre comprobaciones puede fijarse con la palabra clave "inter", y las palabras clave
"rise" y "fall" pueden usarse para definir cuántas comprobaciones de estado exitosas o fallidas se
requieren para marcar un servidor como disponible o no disponible.

Pueden configurarse comprobaciones de estado opcionales a nivel de aplicación con "option httpchk",
"option mysql-check" "option smtpchk", "option pgsql-check", "option ldap-check" u "option
redis-check".

Ejemplo:

```shell
# simple tcp check
backend foo
  server s1 192.168.0.1:80 check
# this does a tcp connect + tls handshake
backend foo
  server s1 192.168.0.1:443 ssl check
# simple tcp check is enough for check success
backend foo
  option tcp-check
  tcp-check connect
  server s1 192.168.0.1:443 ssl check
```

<a id="entry-5-2-check-reuse-pool"></a>

**`check-reuse-pool`**

```haproxy
check-reuse-pool
```

Puede usarse en los siguientes contextos: tcp, http

Esta opción permite que las comprobaciones reutilicen conexiones inactivas si hay disponibles, en
lugar de abrir una dedicada. La conexión se reincorpora al grupo al completarse la comprobación. El
objetivo principal es limitar el número de aperturas y cierres de conexiones en un servidor
específico. Esta funcionalidad solo es compatible con conjuntos de reglas http-check. Se ignora
silenciosamente para otros tipos de comprobación. Además, la política de reutilización debería
definirse como aggressive en el backend, ya que cada intento de comprobación se realiza sobre una
sesión dedicada.

Por simplicidad de configuración, esta opción se ignora silenciosamente si hay definida cualquier
opción específica de conexión de comprobación, ya sea en la línea del servidor o mediante una regla
tcp-check connect personalizada.

Esta opción se habilita automáticamente para los servidores que actúan como puerta de enlace pasiva
de reverse HTTP, ya que para esos servidores connect solo está soportado mediante reutilización.

Ver también: "check-pool-conn-name"

<a id="entry-5-2-check-send-proxy"></a>

**`check-send-proxy`**

```haproxy
check-send-proxy
```

Puede usarse en los siguientes contextos: tcp, http

Esta opción fuerza la emisión de una línea de protocolo PROXY con las comprobaciones de estado
salientes, independientemente de que el servidor use send-proxy o no para el tráfico normal. Por
defecto, el protocolo PROXY está habilitado para las comprobaciones de estado si ya lo está para el
tráfico normal y si no hay presente ninguna directiva "port" ni "addr". Sin embargo, si tal directiva
está presente, hay que usar la opción "check-send-proxy" para forzar el uso del protocolo. Ver
también la opción "send-proxy" para más información.

<a id="entry-5-2-check-alpn"></a>

**`check-alpn <protocols>`**

```haproxy
check-alpn <protocols>
```

Puede usarse en los siguientes contextos: tcp, http

Define qué protocolos anunciar con ALPN. La lista de protocolos consiste en una lista de nombres de
protocolo delimitados por comas, por ejemplo: "http/1.1,http/1.0" (sin comillas). Si no está
definida, se usa el ALPN del servidor.

<a id="entry-5-2-check-pool-conn-name"></a>

**`check-pool-conn-name <name>`**

```haproxy
check-pool-conn-name <name>
```

Puede usarse en los siguientes contextos: tcp, http

Cuando se realiza reutilización de conexiones para las comprobaciones, usa `<name>`, si está
definido, como identificador de conexión para encontrar una conexión correspondiente en el grupo.
Esto equivale a la palabra clave de servidor "pool-conn-name". "check-sni" también se usará como
repliegue si no se usa la opción actual.

Ver también: "check-reuse-pool"

<a id="entry-5-2-check-proto"></a>

**`check-proto <name>`**

```haproxy
check-proto <name>
```

Puede usarse en los siguientes contextos: tcp, http

Fuerza el protocolo del multiplexor que se usará para las conexiones de comprobación de estado del
servidor. Debe ser compatible con el tipo de comprobación de estado (TCP o HTTP). También debe ser
utilizable en el lado del backend. La lista de protocolos disponibles se muestra en haproxy -vv. Se
reportan las propiedades de los protocolos: el modo (TCP/HTTP), el lado (FE/BE), el nombre del mux y
sus flags.

Algunos protocolos están sujetos al bloqueo de cabecera de línea en el lado del servidor
(flag=HOL_RISK). Finalmente, algunos protocolos no admiten cambios de protocolo (flag=NO_UPG). También se
reporta la compatibilidad HTX (flag=HTX).

Estos son los protocolos que pueden usarse como argumento de una directiva "check-proto" en una
línea de servidor:

```text
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

La idea detrás de esta opción es saltarse la selección del mejor protocolo de multiplexado para las
conexiones de comprobación de estado establecidas hacia este servidor. Si no está definido, se usará
el del servidor, si lo tiene.

Si los parámetros ALPN o NPN están configurados, los protocolos especificados deberían ser
compatibles con el protocolo del multiplexor para evitar cualquier problema. Por ejemplo, si se
define "proto h1", el ALPN no debería definirse como "h2".

La configuración de comprobaciones QUIC aún no está completamente implementada. Primero, las
comprobaciones QUIC solo pueden realizarse para servidores QUIC. Segundo, si se especifica uno o más
parámetros de conexión específicos de la comprobación en un servidor QUIC, el protocolo de
comprobación retrocederá al uso de TCP.

<a id="entry-5-2-check-sni-auto"></a>

**`check-sni-auto`**

```haproxy
check-sni-auto
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción habilita la selección automática del SNI al hacer comprobaciones de estado sobre SSL, si
no había ya ningún valor definido. Está habilitada por defecto, pero este parámetro puede usarse como
ajuste de "server" para restablecer cualquier ajuste "no-check-sni-auto" que se hubiera heredado de
la directiva "default-server" como valor por defecto. También puede usarse como ajuste de
"default-server" para restablecer cualquier ajuste previo "no-check-sni-auto" de "default-server".

Para las conexiones HTTPS, el SNI se selecciona automáticamente pero solo si no hay ninguna regla
"http-check connect". En ese caso, el SNI seleccionado se basa en el valor de la cabecera host,
especificado mediante la directiva "option httpchk" o una regla "http-check send". No hay selección
automática para las reglas "http-check connect". Para otros protocolos, la opción se ignora.

Si se usa la selección automática del SNI para las comprobaciones de estado, el valor se asigna al
nombre de la conexión si el ajuste "check-reuse-pool" está definido, salvo que lo sobrescriba la
palabra clave de servidor "check-pool-conn-name".

Ver la opción "sni-auto" para habilitar la selección automática del SNI para el tráfico proxiado.

<a id="entry-5-2-check-sni"></a>

**`check-sni <sni>`**

```haproxy
check-sni <sni>
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción te permite especificar el SNI que se usará al hacer comprobaciones de estado sobre SSL.
Solo es posible usar una cadena para definir `<sni>`. Si quieres definir un SNI para el tráfico
proxiado, ver "sni".

<a id="entry-5-2-check-ssl"></a>

**`check-ssl`**

```haproxy
check-ssl
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción fuerza el cifrado de todas las comprobaciones de estado sobre SSL, independientemente de
que el servidor use SSL o no para el tráfico normal. Generalmente se usa cuando se especifica una
directiva "port" o "addr" explícita y las comprobaciones de estado SSL no se heredan. Es importante
entender que esta opción inserta una capa de transporte SSL por debajo de las comprobaciones, de modo
que una comprobación simple de conexión TCP se convierte en una conexión SSL, lo que sustituye a la
antigua ssl-hello-chk. El uso más común es enviar comprobaciones HTTPS combinando "httpchk" con
comprobaciones SSL. Todos los ajustes SSL son comunes a las comprobaciones de estado y al tráfico
(p. ej. ciphers). Ver la opción "ssl" para más información y "no-check-ssl" para deshabilitar esta
opción.

<a id="entry-5-2-check-via-socks4"></a>

**`check-via-socks4`**

```haproxy
check-via-socks4
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción habilita las comprobaciones de estado salientes usando un proxy socks4 ascendente. Por
defecto, las comprobaciones de estado no pasarán por el túnel socks aunque estuviera habilitado para
el tráfico normal.

<a id="entry-5-2-ciphers"></a>

**`ciphers <ciphers>`**

```haproxy
ciphers <ciphers>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Esta opción define
la cadena que describe la lista de algoritmos de cifrado que se negocian durante el handshake SSL/TLS
con el servidor. El formato de la cadena está definido en "man 1 ciphers" de las páginas man de
OpenSSL. Para información de contexto y recomendaciones ver p. ej.
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) y
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Para la configuración de
cifrados de TLSv1.3, consulta la palabra clave "ciphersuites".

<a id="entry-5-2-ciphersuites"></a>

**`ciphersuites <ciphersuites>`**

```haproxy
ciphersuites <ciphersuites>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL y se usó OpenSSL
1.1.1 o posterior para compilar HAProxy. Esta opción define la cadena que describe la lista de
algoritmos de cifrado que se negocian durante el handshake TLS 1.3 con el servidor. El formato de la
cadena está definido en "man 1 ciphers" de las páginas man de OpenSSL, en la sección "ciphersuites".
Para la configuración de cifrados para TLSv1.2 y anteriores, consulta la palabra clave "ciphers".

<a id="entry-5-2-client-sigalgs"></a>

**`client-sigalgs <sigalgs>`**

```haproxy
client-sigalgs <sigalgs>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de firma relacionados con la autenticación de cliente que se
negocian. El formato de la cadena está definido en "man 3 SSL_CTX_set1_client_sigalgs" de las páginas
man de OpenSSL. No se recomienda usar este parámetro si no se ha identificado un caso de uso
específico.

<a id="entry-5-2-cookie"></a>

**`cookie <value>`**

```haproxy
cookie <value>
```

Puede usarse en los siguientes contextos: http

El parámetro "cookie" fija el valor de cookie asignado al servidor a `<value>`. Este valor se
comprobará en las solicitudes entrantes y se seleccionará el primer servidor operativo que posea el
mismo valor. A cambio, en los modos de inserción o reescritura de cookie, este valor se asignará a la
cookie enviada al cliente. No hay nada malo en que varios servidores compartan el mismo valor de
cookie; de hecho es bastante común entre servidores normales y de respaldo. Ver también la palabra
clave "cookie" en la sección backend.

<a id="entry-5-2-crl-file"></a>

**`crl-file <crlfile>`**

```haproxy
crl-file <crlfile>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM del cual cargar la lista de revocación de certificados usada para verificar el certificado del
servidor.

<a id="entry-5-2-crt"></a>

**`crt <cert>`**

```haproxy
crt <cert>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Designa un archivo
PEM del cual cargar tanto un certificado como la clave privada asociada. Este archivo puede
construirse concatenando ambos archivos PEM en uno. Este certificado se enviará si el servidor envía
una solicitud de certificado de cliente.

Si el archivo no contiene una clave privada, HAProxy intentará cargar la clave en la misma ruta con
el sufijo ".key" (siempre que la opción "ssl-load-extra-files" esté definida en consecuencia).

<a id="entry-5-2-curves"></a>

**`curves <curves>`**

```haproxy
curves <curves>
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Este parámetro solo está disponible cuando se compiló con soporte para OpenSSL. Define la cadena que
describe la lista de algoritmos de curvas elípticas ("curve suite") que se negocian durante el
handshake SSL/TLS con ECDHE. El formato de la cadena es una lista de nombres de curva delimitada por
dos puntos. Ejemplo: "X25519:P-256" (sin comillas)

<a id="entry-5-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

Puede usarse en los siguientes contextos: tcp, http, log

La palabra clave "disabled" arranca el servidor en estado "disabled". Esto significa que queda
marcado como caído en modo mantenimiento y que ninguna conexión, aparte de las permitidas por el modo
persist, lo alcanzará. Es muy adecuado para poner en marcha servidores nuevos, porque el tráfico
normal nunca los alcanzará, mientras que sigue siendo posible probar el servicio haciendo uso del
mecanismo force-persist. Ver también el ajuste "enabled".

<a id="entry-5-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

Puede usarse en los siguientes contextos: tcp, http, log

Esta opción puede usarse como ajuste de 'server' para restablecer cualquier ajuste 'disabled' que se
hubiera heredado de la directiva 'default-server' como valor por defecto. También puede usarse como
ajuste de 'default-server' para restablecer cualquier ajuste previo 'disabled' de 'default-server'.

<a id="entry-5-2-error-limit"></a>

**`error-limit <count>`**

```haproxy
error-limit <count>
```

Puede usarse en los siguientes contextos: tcp, http, log

Si la observación de errores está habilitada, el parámetro "error-limit" especifica el número de
errores consecutivos que dispara el evento seleccionado por la opción "on-error". Por defecto está
definido a 10 errores consecutivos.

Ver también "check", "error-limit" y "on-error".

<a id="entry-5-2-fall"></a>

**`fall <count>`**

```haproxy
fall <count>
```

Puede usarse en los siguientes contextos: tcp, http, log

El parámetro "fall" establece que un servidor se considerará muerto tras `<count>` comprobaciones de
estado consecutivas sin éxito. Este valor toma por defecto 3 si no se especifica. Ver también los
parámetros "check", "inter" y "rise".

<a id="entry-5-2-force-sslv3"></a>

**`force-sslv3`**

```haproxy
force-sslv3
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción fuerza el uso exclusivo de SSLv3 cuando se usa SSL para comunicarse con el servidor.
SSLv3 es generalmente menos costoso que sus equivalentes TLS para tasas de conexión altas. Esta
opción también está disponible en la directiva global "ssl-default-server-options". Ver también
"ssl-min-ver" y ssl-max-ver".

<a id="entry-5-2-force-tlsv10"></a>

**`force-tlsv10`**

```haproxy
force-tlsv10
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción fuerza el uso exclusivo de TLSv1.0 cuando se usa SSL para comunicarse con el servidor.
Esta opción también está disponible en la directiva global "ssl-default-server-options". Ver también
"ssl-min-ver" y ssl-max-ver".

<a id="entry-5-2-force-tlsv11"></a>

**`force-tlsv11`**

```haproxy
force-tlsv11
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción fuerza el uso exclusivo de TLSv1.1 cuando se usa SSL para comunicarse con el servidor.
Esta opción también está disponible en la directiva global "ssl-default-server-options". Ver también
"ssl-min-ver" y ssl-max-ver".

<a id="entry-5-2-force-tlsv12"></a>

**`force-tlsv12`**

```haproxy
force-tlsv12
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción fuerza el uso exclusivo de TLSv1.2 cuando se usa SSL para comunicarse con el servidor.
Esta opción también está disponible en la directiva global "ssl-default-server-options". Ver también
"ssl-min-ver" y ssl-max-ver".

<a id="entry-5-2-force-tlsv13"></a>

**`force-tlsv13`**

```haproxy
force-tlsv13
```

Puede usarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción fuerza el uso exclusivo de TLSv1.3 cuando se usa SSL para comunicarse con el servidor.
Esta opción también está disponible en la directiva global "ssl-default-server-options". Ver también
"ssl-min-ver" y ssl-max-ver".

<a id="entry-5-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

Puede usarse en los siguientes contextos: tcp, http, log

Especifica un ID global único, sensible a mayúsculas y minúsculas, para este servidor. Debe ser único
en toda la configuración de haproxy y en todos los tipos de objeto. Ver la descripción de la palabra
clave "guid" de proxy para más información sobre su formato. Ver también "shm-stats-file".

<a id="entry-5-2-hash-key"></a>

**`hash-key <key>`**

```haproxy
hash-key <key>
```

Puede usarse en los siguientes contextos: tcp, http, log

Especifica cómo se calculan las claves de nodo de "hash-type consistent"

Argumentos:

```text
<key>   <key> puede ser uno de los valores siguientes:

  id         Las claves de los nodos se derivarán del identificador numérico
             del servidor, tal como se definió con "id" o que por defecto
             corresponde a su posición en la lista de servidores. Este es el
             valor por defecto. Ten en cuenta que solo se usarán los 20 bits más
             bajos del ID (es decir, (id % 1048576)), de modo que es mejor
             usar únicamente valores comprendidos entre 1 y este valor para
             evitar solapamientos.

  id32       Las claves de los nodos se derivarán del identificador numérico
             del servidor, tal como se definió con "id" o que por defecto
             corresponde a su posición en la lista de servidores, pero se
             usarán los 32 bits completos del ID, de modo que no haya
             colisiones. Este valor no se escala como sí se hace con "id",
             por lo que se recomienda usarlo siempre con una función de
             hash (ver "hash-key") o con valores de ID asignados
             explícitamente que estén distribuidos uniformemente por el
             espacio de 32 bits.

  guid       Las claves de los nodos se derivarán del guid del servidor
             cuando esté disponible; de lo contrario, recurrirán a "id". La
             ventaja es que no depende en absoluto del orden, sino solo de
             un identificador interno estable que puede replicarse en
             muchos balanceadores de carga.

  addr       Las claves de los nodos se derivarán de la dirección del
             servidor cuando esté disponible, o de lo contrario recurrirán
             a "id".

  addr-port  Las claves de los nodos se derivarán de la dirección y el
             puerto del servidor cuando estén disponibles, o de lo contrario
             recurrirán a "id".
```

Las opciones "addr" y "addr-port" pueden ser útiles en escenarios donde múltiples procesos HAProxy
balancean tráfico hacia el mismo conjunto de servidores. Si el orden de los servidores de cada
proceso es diferente (porque, por ejemplo, los registros DNS se resolvieron en órdenes distintos),
esto permitirá que cada proceso HAProxy independiente se ponga de acuerdo en las decisiones de
enrutamiento. Nota: "balance random" también usa "hash-type consistent" y la calidad de la
distribución dependerá de la calidad de las claves.

<a id="entry-5-2-healthcheck"></a>

**`healthcheck <name>`**

```haproxy
healthcheck <name>
```

Puede usarse en los siguientes contextos: tcp, http

Especifica la sección de health-check que se usará para realizar la comprobación en el servidor.

Argumento:

```text
<name>    es el nombre de la sección de health-check.
```

Gracias a esta opción es posible usar una configuración de health-check pre-servidor en lugar de usar
la configuración del proxy. Ver también "healthcheck section".

<a id="entry-5-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

Puede usarse en los siguientes contextos: tcp, http, log

Define un ID persistente para el servidor. Este ID debe ser un número positivo de 32 bits y único
para el proxy. Si no se define, se asignará automáticamente un ID no utilizado. El primer valor
asignado será 1. Este ID actualmente solo se devuelve en las estadísticas y se usa para colocar los
nodos de LB al usar algoritmos de hash consistente cuando "hash-key" está definido como "id" (el
valor por defecto). En este caso, solo se usan los 20 bits más bajos del valor (es decir, (id %
1048576)), de modo que es mejor usar solo valores comprendidos entre 1 y este valor para evitar
solapamientos.

<a id="entry-5-2-idle-ping"></a>

**`idle-ping <delay>`**

```haproxy
idle-ping <delay>
```

Puede usarse en los siguientes contextos: tcp, http, log

Define un intervalo para comprobar periódicamente la vitalidad de las conexiones inactivas del
backend. Si el par no puede responder antes de la siguiente prueba programada, la conexión se
cierra. Esta palabra clave se refiere al lado del backend, así que es útil para comprobar que las
conexiones inactivas siguen siendo utilizables. Ten en cuenta que esto no impedirá que la conexión se
destruya al purgar el grupo de conexiones inactivas.

Esta funcionalidad depende del soporte del protocolo subyacente específico. Por ahora, solo el mux
H2 la implementa. Idle-ping simplemente es ignorado por otros protocolos.

Esta opción es particularmente útil al usar reverse HTTP. Definirla en la línea del servidor es útil
para el par que escucha las conexiones entrantes y las adjunta a un servidor correspondiente para
poder reutilizarlas más adelante en el reenvío de tráfico.

<a id="entry-5-2-init-addr"></a>

**`init-addr {last | libc | none | <ip>},[...]*`**

```haproxy
init-addr {last | libc | none | <ip>},[...]*
```

Puede usarse en los siguientes contextos: tcp, http, log

Indica en qué orden debería resolverse la dirección del servidor al arrancar si usa un FQDN. Se
hacen intentos de resolver la dirección aplicando sucesivamente cada uno de los métodos mencionados
en la lista delimitada por comas. Se usa el primer método que tenga éxito. Si se alcanza el final de
la lista sin encontrar un método que funcione, se lanza un error. El método "last" sugiere elegir la
dirección que aparece en el archivo de estado (ver "server-state-file"). El método "libc" usa el
resolver interno de libc (gethostbyname() o getaddrinfo() dependiendo del sistema operativo y de las
opciones de compilación). El método "none" indica específicamente que el servidor debe arrancar sin
ninguna dirección IP válida, en estado down. Puede ser útil para ignorar algunos problemas DNS al
arrancar, a la espera de que la situación se corrija más tarde. Finalmente, puede proporcionarse una
dirección IP (IPv4 o IPv6). Puede ser la dirección conocida actualmente del servidor (p. ej.
rellenada por un generador de configuración), o la dirección de un servidor ficticio usado para
capturar sesiones antiguas y presentarles un mensaje de error decente, por ejemplo. Cuando se usa el
algoritmo de balanceo de carga "first", esta dirección IP podría apuntar a un servidor falso usado
para provocar la creación de instancias nuevas sobre la marcha. Esta opción toma por defecto
"last,libc", lo que indica que la dirección anterior encontrada en el archivo de estado (si la hay)
se usa primero; de lo contrario se usa el resolver de libc. Esto asegura la compatibilidad continua
con el comportamiento histórico. Al usar resolvers internos, generalmente se recomienda deshabilitar
la resolución basada en libc, o hacerla explícita (consulta la [sección 5.3](/es/haproxy/bind-and-server-options/#section-5-3) para más detalles).

Ejemplo 1:

```text
defaults
    # never fail on address resolution
    default-server init-addr last,libc,none
```

Ejemplo 2:

```text
defaults
    # disable libc resolution in combination with resolvers
    default-server init-addr last,none
```

<a id="entry-5-2-inter"></a>

**`inter <delay>`**

```haproxy
inter <delay>
fastinter <delay>
downinter <delay>
```

Puede usarse en los siguientes contextos: tcp, http, log

El parámetro "inter" fija el intervalo entre dos comprobaciones de estado consecutivas a `<delay>`
milisegundos. Si no se especifica, el retardo toma por defecto 2000 ms. También es posible usar
"fastinter" y "downinter" para optimizar los retardos entre comprobaciones dependiendo del estado del
servidor:

```text
             Estado del servidor            |         Intervalo usado
    ----------------------------------------+----------------------------------
     UP 100% (no transicional)              | "inter"
    ----------------------------------------+----------------------------------
     UP transicional (bajando "fall"),      | "fastinter" si está definido,
     DOWN transicional (subiendo "rise"),   | "inter" en caso contrario.
     o todavía sin comprobar.              |
    ----------------------------------------+----------------------------------
     DOWN 100% (no transicional)            | "downinter" si está definido,
                                            | "inter" en caso contrario.
    ----------------------------------------+----------------------------------
```

Al igual que con cualquier otro parámetro basado en tiempo, pueden introducirse en cualquier otra
unidad explícita de entre { us, ms, s, m, h, d }. El parámetro "inter" sirve también como tiempo de
espera para las comprobaciones de estado enviadas a los servidores si no se define "timeout check".
Para reducir los efectos de "resonancia" cuando varios servidores están alojados en el mismo
hardware, las comprobaciones del agente y de estado de todos los servidores se inician con un pequeño
desfase temporal entre ellas. También es posible añadir algo de ruido aleatorio en el intervalo de
las comprobaciones del agente y de estado usando la palabra clave global "spread-checks". Esto tiene
sentido, por ejemplo, cuando muchos backends usan los mismos servidores. El ajuste global
"tune.max-checks-per-thread", si se define con un valor no nulo, limitará el número de comprobaciones
concurrentes que se realizan a la vez en cualquier hilo dado. Para lograrlo, haproxy pondrá en una
cola las comprobaciones que estaban a punto de iniciarse en un hilo que ha alcanzado este límite,
hasta que termine otra comprobación. Esto tendrá como efecto extender el intervalo efectivo de
comprobación. En tal caso, reducir el ajuste "inter" tendrá un efecto muy limitado, ya que no podrá
reducir el tiempo pasado en la cola.

<a id="entry-5-2-init-state"></a>

**`init-state { fully-up | up | down | fully-down | none }`**

```haproxy
init-state { fully-up | up | down | fully-down | none }
```

Puede usarse en los siguientes contextos: tcp, http

Puede usarse en las secciones: defaults \| frontend \| listen \| backend no \| no \| sí \| sí

La opción "init-state" define el estado inicial del servidor: - cuando se define como 'fully-up', el
servidor se considera inmediatamente disponible y, si las comprobaciones de estado están habilitadas
para este servidor, pasará al estado DOWN cuando TODAS las comprobaciones de estado fallen. - cuando
se define como 'up', el servidor se considera inmediatamente disponible y, si las comprobaciones de
estado están habilitadas para este servidor, pasará inmediatamente al estado DOWN si falla la
siguiente comprobación de estado. - cuando se define como 'down', el servidor se considera
inicialmente no disponible y, si las comprobaciones de estado están habilitadas para este servidor,
podrá pasar al estado UP si la siguiente comprobación de estado tiene éxito. - cuando se define como
'fully-down', el servidor se considera inicialmente no disponible y, si las comprobaciones de estado
están habilitadas para este servidor, pasará al estado UP cuando TODAS las comprobaciones de estado
tengan éxito. - cuando se define como 'none' (el valor por defecto), la gestión de init-state está
deshabilitada. Puede usarse para restablecer el comportamiento por defecto cuando este parámetro se
heredó de una directiva 'default-server'.

El init-state del servidor se tiene en cuenta cuando la instancia de HAProxy se (re)inicia, se
detecta un servidor nuevo (por ejemplo mediante service discovery / resolución DNS), se activa un
servidor dinámico, un servidor sale del mantenimiento, etc. Esta directiva no puede usarse cuando el
servidor sigue el estado de otro.

Ejemplos:

```shell
# pass client traffic ONLY to Redis "master" node
backend redis-master
  mode tcp
  balance first
  option tcp-check
  tcp-check send role\r\n
  tcp-check expect string master
  server-template redis 3 _redis._tcp.redis-headless-service.sandbox.svc.cluster.local:6379 check ... init-state down

# pass traffic to the server only after 3 successful health checks
backend google-backend
  mode http
  server srv1 google.com:80 check init-state fully-down rise 3
  server srv2 google.com:80 check init-state fully-down rise 3
```

Consulta también: «option tcp-check», «option httpchk»

<a id="entry-5-2-ktls"></a>

**`ktls <on|off> [ EXPERIMENTAL ]`**

```haproxy
ktls <on|off> [ EXPERIMENTAL ]
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Activa o desactiva ktls para estos sockets. Si está activado, se utilizará kTLS si el núcleo lo
soporta y el cifrado es compatible. Esto solo está disponible en Linux 4.17 y superior. Ten en
cuenta que algunos controladores de red y/o pilas TLS podrían restringir el uso de kTLS
únicamente a TLS v1.2. Consulta también «force-tlsv12».

<a id="entry-5-2-log-bufsize"></a>

**`log-bufsize <bufsize>`**

```haproxy
log-bufsize <bufsize>
```

Puede utilizarse en los siguientes contextos: log

El parámetro «log-bufsize» especifica el tamaño de búfer del ring que se utilizará para el ring
implícito que se asociará al servidor de registro en un backend de registro. Si no se especifica,
el valor por defecto es BUFSIZE. El uso de un valor mayor incrementará el consumo de memoria,
pero puede ayudar a evitar la pérdida de mensajes de registro con servidores lentos, ya que el
búfer podrá contener más mensajes pendientes. Esta palabra clave solo puede utilizarse en
secciones de backend de registro (con «mode log»)

<a id="entry-5-2-log-proto"></a>

**`log-proto <logproto>`**

```haproxy
log-proto <logproto>
```

Puede utilizarse en los siguientes contextos: log, ring

El parámetro «log-proto» especifica el protocolo utilizado para reenviar los mensajes de eventos
a un servidor configurado en una sección log o ring. Los valores posibles son «legacy» y
«octet-count», que corresponden respectivamente a «Non-transparent-framing» y «Octet counting»
en el rfc6587. «legacy» es el valor por defecto.

<a id="entry-5-2-maxconn"></a>

**`maxconn <maxconn>`**

```haproxy
maxconn <maxconn>
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «maxconn» especifica el número máximo de conexiones simultáneas que se enviarán a
este servidor. Si el número de conexiones entrantes simultáneas supera este valor, se pondrán en
cola a la espera de que se libere un hueco. Este parámetro es muy importante, ya que puede salvar
a servidores frágiles de caer bajo cargas extremas. Si se especifica un parámetro «minconn», el
límite se vuelve dinámico. El valor por defecto es «0», lo que significa sin límite. Consulta
también los parámetros «minconn» y «maxqueue», así como la palabra clave «fullconn» del backend.

En modo HTTP, este parámetro limita el número de solicitudes simultáneas en lugar del número de
conexiones. Varias solicitudes pueden multiplexarse sobre una única conexión TCP hacia el
servidor. Como ejemplo, si especificas un maxconn de 50, puedes ver entre 1 y 50 conexiones
reales al servidor, pero nunca más de 50 solicitudes simultáneas.

<a id="entry-5-2-maxqueue"></a>

**`maxqueue <maxqueue>`**

```haproxy
maxqueue <maxqueue>
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «maxqueue» especifica el número máximo de conexiones que esperarán en la cola por
este servidor. Si se alcanza este límite, las siguientes solicitudes se redistribuirán a otros
servidores en lugar de esperar indefinidamente a ser atendidas. Esto romperá la persistencia,
pero puede permitir a los usuarios iniciar sesión de nuevo rápidamente cuando el servidor al que
intentan conectarse está muriendo. Algunos algoritmos de balanceo de carga, como leastconn,
tienen esto en cuenta y aceptan añadir solicitudes a la cola de un servidor hasta este valor si
está establecido explícitamente a un valor mayor que cero, lo que a menudo permite suavizar mejor
la carga cuando se tratan valores de maxconn de un solo dígito. El valor por defecto es «0», lo
que significa que la cola es ilimitada. Consulta también los parámetros «maxconn» y «minconn», y
«balance leastconn».

<a id="entry-5-2-max-reuse"></a>

**`max-reuse <count>`**

```haproxy
max-reuse <count>
```

Puede utilizarse en los siguientes contextos: http, ring

Cuando se utiliza en contexto http:

El argumento «max-reuse» indica a los procesadores de conexiones HTTP que no deben reutilizar una
conexión al servidor más veces que este número para enviar nuevas solicitudes. Los valores
permitidos son -1 (el valor por defecto), que desactiva este límite, o cualquier valor positivo.
El valor cero desactivará efectivamente keep-alive. Esto solo se utiliza para sortear ciertos
errores de servidores que provocan fugas de recursos con el tiempo. El argumento no
necesariamente es respetado por las capas inferiores, ya que puede haber limitaciones técnicas
que hagan imposible aplicarlo. Al menos las conexiones HTTP/2 hacia los servidores lo respetarán.

Cuando se utiliza en contexto ring:

El argumento «max-reuse» indica que los procesadores de conexiones TCP del sumidero no deben
reutilizar una conexión al servidor más veces que este número para enviar mensajes. Esto
significa que la conexión con el servidor se destruirá de forma forzada una vez que al menos
«max-reuse + 1» mensajes se hayan manejado en la misma conexión. La conexión con el servidor se
volverá a crear automáticamente entonces. Al manejar una gran cantidad de mensajes en un
contexto multihilo, esto puede ayudar a distribuir mejor la carga del ring entre varios hilos.
En efecto, cada conexión está ligada al mismo hilo de CPU durante toda su duración: a diferencia
de HTTP, no existe algo como una transacción syslog, así que la conexión con el servidor podría
vivir indefinidamente mientras el servidor no cierre la conexión ni ocurra un error de red. Al
destruir conexiones de vez en cuando damos la oportunidad a otros hilos de recoger algunos
mensajes por turnos. También puede ayudar a rotar de forma ordenada los servidores de registro
en contextos donde hay una capa adicional de balanceo de carga entre haproxy y los servidores de
registro. Sin embargo, ten en cuenta que cada reciclaje de conexión dejará un puerto de salida
en estado TIME_WAIT que no será reutilizable durante alrededor de un minuto en los sistemas
operativos modernos, y que por ello hay que tener cuidado de no usar valores demasiado bajos
para prevenir un agotamiento rápido de los puertos de origen. Como regla general, asegúrate de
nunca cerrar más de unas pocas veces por segundo, y preferiblemente mucho menos a menudo. Los
valores permitidos son -1 (el valor por defecto), que desactiva este límite, o cualquier valor
positivo. A diferencia del contexto HTTP, cuando se usa con servidores de sumidero «max-reuse»
es de mejor esfuerzo: los mensajes del ring se agrupan en lotes, así que el límite se comprueba
entre cada lote.

<a id="entry-5-2-minconn"></a>

**`minconn <minconn>`**

```haproxy
minconn <minconn>
```

Puede utilizarse en los siguientes contextos: tcp, http

Cuando se establece el parámetro «minconn», el límite maxconn se convierte en un límite dinámico
que sigue la carga del backend. El servidor aceptará siempre al menos `<minconn>` conexiones,
nunca más de `<maxconn>`, y el límite estará en la rampa entre ambos valores cuando el backend
tenga menos de `<fullconn>` conexiones simultáneas. Esto hace posible limitar la carga sobre el
servidor durante cargas normales, pero empujarla más allá para cargas importantes sin
sobrecargar el servidor durante cargas excepcionales. Consulta también los parámetros «maxconn» y
«maxqueue», así como la palabra clave de backend «fullconn».

<a id="entry-5-2-namespace"></a>

**`namespace <name>`**

```haproxy
namespace <name>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

En Linux, es posible especificar a qué espacio de nombres de red pertenecerá un socket. Esta
directiva hace posible vincular explícitamente un servidor a un espacio de nombres diferente del
predeterminado. Consulta la documentación de tu sistema operativo para encontrar más detalles
sobre los espacios de nombres de red.

<a id="entry-5-2-no-agent-check"></a>

**`no-agent-check`**

```haproxy
no-agent-check
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«agent-check» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«agent-check» de «default-server» anterior.

<a id="entry-5-2-no-backup"></a>

**`no-backup`**

```haproxy
no-backup
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste «backup» que
se haya heredado como valor por defecto de la directiva «default-server». También puede
utilizarse como ajuste «default-server» para restablecer cualquier ajuste «backup» de
«default-server» anterior.

<a id="entry-5-2-no-check"></a>

**`no-check`**

```haproxy
no-check
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste «check» que
se haya heredado como valor por defecto de la directiva «default-server». También puede
utilizarse como ajuste «default-server» para restablecer cualquier ajuste «check» de
«default-server» anterior.

<a id="entry-5-2-no-check-reuse-pool"></a>

**`no-check-reuse-pool`**

```haproxy
no-check-reuse-pool
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción revierte cualquier «check-reuse-pool» anterior posiblemente heredado de un
«default-server». Todas las comprobaciones se realizarán en su conexión dedicada.

<a id="entry-5-2-no-check-sni-auto"></a>

**`no-check-sni-auto`**

```haproxy
no-check-sni-auto
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción puede utilizarse como ajuste «server» para desactivar la selección automática de SNI
para las comprobaciones de estado SSL, que está activada por defecto.

Consulta la opción «no-sni-auto» para desactivar la selección automática de SNI para el tráfico que
pasa por el proxy.

<a id="entry-5-2-no-check-ssl"></a>

**`no-check-ssl`**

```haproxy
no-check-ssl
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«check-ssl» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«check-ssl» de «default-server» anterior.

<a id="entry-5-2-no-renegotiate"></a>

**`no-renegotiate`**

```haproxy
no-renegotiate
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Este ajuste solo está disponible si se compiló con soporte para OpenSSL. Desactiva los mecanismos
de renegociación, ya sea el antiguo e inseguro o el más reciente de «renegociación segura»
(extensión de indicación de renegociación TLS de la RFC 5746) para el backend SSL dado. Esta
opción también está disponible en la instrucción global «ssl-default-server-options». La
renegociación ya no es posible en TLS 1.3. Si no se especifica ni «renegotiate» ni
«no-renegotiate», se mantiene el comportamiento por defecto de la biblioteca SSL. Ten en cuenta
que, por ejemplo, la biblioteca OpenSSL activa la renegociación segura por defecto, mientras
que AWS-LC la desactiva. Consulta también «renegotiate».

<a id="entry-5-2-no-send-proxy"></a>

**`no-send-proxy`**

```haproxy
no-send-proxy
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«send-proxy» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«send-proxy» de «default-server» anterior.

<a id="entry-5-2-no-send-proxy-v2"></a>

**`no-send-proxy-v2`**

```haproxy
no-send-proxy-v2
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«send-proxy-v2» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«send-proxy-v2» de «default-server» anterior.

<a id="entry-5-2-no-send-proxy-v2-ssl"></a>

**`no-send-proxy-v2-ssl`**

```haproxy
no-send-proxy-v2-ssl
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«send-proxy-v2-ssl» que se haya heredado como valor por defecto de la directiva
«default-server». También puede utilizarse como ajuste «default-server» para restablecer
cualquier ajuste «send-proxy-v2-ssl» de «default-server» anterior.

<a id="entry-5-2-no-send-proxy-v2-ssl-cn"></a>

**`no-send-proxy-v2-ssl-cn`**

```haproxy
no-send-proxy-v2-ssl-cn
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«send-proxy-v2-ssl-cn» que se haya heredado como valor por defecto de la directiva
«default-server». También puede utilizarse como ajuste «default-server» para restablecer
cualquier ajuste «send-proxy-v2-ssl-cn» de «default-server» anterior.

<a id="entry-5-2-no-sni-auto"></a>

**`no-sni-auto`**

```haproxy
no-sni-auto
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para desactivar la selección automática de
SNI, que está activada por defecto.

Consulta la opción «no-check-sni-auto» para desactivar la selección automática de SNI para las
comprobaciones de estado SSL.

<a id="entry-5-2-no-ssl"></a>

**`no-ssl`**

```haproxy
no-ssl
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste «ssl» que se
haya heredado como valor por defecto de la directiva «default-server». También puede utilizarse
como ajuste «default-server» para restablecer cualquier ajuste «ssl» de «default-server»
anterior.

Ten en cuenta que usar el ajuste `default-server ssl` y `no-ssl` en el servidor, sin embargo,
iniciará la conexión SSL, de modo que pueda activarse más adelante mediante la API en tiempo de
ejecución: consulta los comandos `set server` en la documentación de administración.

<a id="entry-5-2-no-ssl-reuse"></a>

**`no-ssl-reuse`**

```haproxy
no-ssl-reuse
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva la reutilización de sesiones SSL cuando se utiliza SSL para comunicarse
con el servidor. Obligará al servidor a realizar una negociación completa por cada nueva
conexión. Probablemente solo sea útil para pruebas de rendimiento, diagnóstico de problemas y
para usuarios paranoicos.

<a id="entry-5-2-no-sslv3"></a>

**`no-sslv3`**

```haproxy
no-sslv3
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva el soporte de SSLv3 cuando se utiliza SSL para comunicarse con el
servidor. Ten en cuenta que SSLv2 está desactivado en el código y no puede activarse mediante
ninguna opción de configuración. Utiliza «ssl-min-ver» y «ssl-max-ver» en su lugar.

Soportado en default-server: No

<a id="entry-5-2-no-tls-tickets"></a>

**`no-tls-tickets`**

```haproxy
no-tls-tickets
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Este ajuste solo está disponible si se compiló con soporte para OpenSSL. Desactiva la
reanudación de sesión sin estado (extensión TLS Ticket de la RFC 5077) y fuerza el uso de la
reanudación de sesión con estado. La reanudación de sesión sin estado es más costosa en uso de
CPU para los servidores. Esta opción también está disponible en la instrucción global
«ssl-default-server-options». El mecanismo de tickets TLS solo se utiliza hasta TLS 1.2. La
confidencialidad directa queda comprometida con los tickets TLS, a menos que las claves de los
tickets se roten periódicamente (mediante recarga o usando «tls-ticket-keys»). Consulta también
«tls-tickets».

<a id="entry-5-2-no-tlsv10"></a>

**`no-tlsv10`**

```haproxy
no-tlsv10
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva el soporte de TLSv1.0 cuando se utiliza SSL para comunicarse con el
servidor. Ten en cuenta que SSLv2 está desactivado en el código y no puede activarse mediante
ninguna opción de configuración. TLSv1 es más costoso que SSLv3, por lo que a menudo tiene
sentido desactivarlo al comunicarse con servidores locales. Esta opción también está disponible
en la instrucción global «ssl-default-server-options». Utiliza «ssl-min-ver» y «ssl-max-ver» en
su lugar.

Soportado en default-server: No

<a id="entry-5-2-no-tlsv11"></a>

**`no-tlsv11`**

```haproxy
no-tlsv11
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva el soporte de TLSv1.1 cuando se utiliza SSL para comunicarse con el
servidor. Ten en cuenta que SSLv2 está desactivado en el código y no puede activarse mediante
ninguna opción de configuración. TLSv1 es más costoso que SSLv3, por lo que a menudo tiene
sentido desactivarlo al comunicarse con servidores locales. Esta opción también está disponible
en la instrucción global «ssl-default-server-options». Utiliza «ssl-min-ver» y «ssl-max-ver» en
su lugar.

Soportado en default-server: No

<a id="entry-5-2-no-tlsv12"></a>

**`no-tlsv12`**

```haproxy
no-tlsv12
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva el soporte de TLSv1.2 cuando se utiliza SSL para comunicarse con el
servidor. Ten en cuenta que SSLv2 está desactivado en el código y no puede activarse mediante
ninguna opción de configuración. TLSv1 es más costoso que SSLv3, por lo que a menudo tiene
sentido desactivarlo al comunicarse con servidores locales. Esta opción también está disponible
en la instrucción global «ssl-default-server-options». Utiliza «ssl-min-ver» y «ssl-max-ver» en
su lugar.

Soportado en default-server: No

<a id="entry-5-2-no-tlsv13"></a>

**`no-tlsv13`**

```haproxy
no-tlsv13
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción desactiva el soporte de TLSv1.3 cuando se utiliza SSL para comunicarse con el
servidor. Ten en cuenta que SSLv2 está desactivado en el código y no puede activarse mediante
ninguna opción de configuración. TLSv1 es más costoso que SSLv3, por lo que a menudo tiene
sentido desactivarlo al comunicarse con servidores locales. Esta opción también está disponible
en la instrucción global «ssl-default-server-options». Utiliza «ssl-min-ver» y «ssl-max-ver» en
su lugar.

Soportado en default-server: No

<a id="entry-5-2-no-verifyhost"></a>

**`no-verifyhost`**

```haproxy
no-verifyhost
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«verifyhost» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«verifyhost» de «default-server» anterior.

<a id="entry-5-2-no-tfo"></a>

**`no-tfo`**

```haproxy
no-tfo
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste «tfo» que
se haya heredado como valor por defecto de la directiva «default-server». También puede
utilizarse como ajuste «default-server» para restablecer cualquier ajuste «tfo» de
«default-server» anterior.

<a id="entry-5-2-non-stick"></a>

**`non-stick`**

```haproxy
non-stick
```

Puede utilizarse en los siguientes contextos: tcp, http

Nunca añade a una stick-table las conexiones asignadas a este servidor. Puede utilizarse junto
con backup para garantizar que la persistencia por stick-table esté desactivada para los
servidores de respaldo.

<a id="entry-5-2-npn"></a>

**`npn <protocols>`**

```haproxy
npn <protocols>
```

Puede utilizarse en los siguientes contextos: tcp, http

Esto activa la extensión TLS NPN y anuncia la lista de protocolos especificada como soportada
sobre NPN. La lista de protocolos consiste en una lista de nombres de protocolos delimitados por
comas, por ejemplo: "http/1.1,http/1.0" (sin comillas). Esto requiere que la biblioteca SSL se
haya compilado con el soporte de extensiones TLS activado (compruébalo con haproxy -vv). Ten en
cuenta que la extensión NPN ha sido sustituida por la extensión ALPN (consulta la palabra clave
«alpn»), aunque esta última solo está disponible a partir de OpenSSL 1.0.2.

Compatibilidad: OpenSSL >= 1.0.1. No compatible con AWS-LC.

<a id="entry-5-2-observe"></a>

**`observe <mode>`**

```haproxy
observe <mode>
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción activa el ajuste del estado de salud basado en la observación de la comunicación con
el servidor. Por defecto esta funcionalidad está desactivada y activarla requiere también
activar las comprobaciones de estado. Hay dos modos soportados: "layer4" y "layer7". En modo
layer4, solo son significativas las conexiones tcp exitosas/no exitosas. En layer7, que solo
está permitido para proxies http, se verifican las respuestas recibidas del servidor, como un
código http válido/incorrecto, encabezados no analizables, un tiempo de espera agotado, etc. Los
códigos de estado válidos incluyen del 100 al 499, 501 y 505.

Consulta también «check», «on-error» y «error-limit».

<a id="entry-5-2-on-error"></a>

**`on-error <mode>`**

```haproxy
on-error <mode>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Selecciona qué debe ocurrir cuando se detectan suficientes errores consecutivos. Actualmente
hay cuatro modos disponibles:

- fastinter: fuerza fastinter
- fail-check: simula una comprobación fallida, también fuerza fastinter (por defecto)
- sudden-death: simula una comprobación de estado fallida pre-fatal, una comprobación fallida
  más marcará el servidor como caído, fuerza fastinter
- mark-down: marca inmediatamente el servidor como caído y fuerza fastinter

Consulta también «check», «observe» y «error-limit».

<a id="entry-5-2-on-marked-down"></a>

**`on-marked-down <action>`**

```haproxy
on-marked-down <action>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Modifica lo que ocurre cuando un servidor se marca como caído. Actualmente hay una acción
disponible:

- shutdown-sessions: Termina los flujos de los peers. Cuando este ajuste está activado, todas
  las conexiones al servidor se terminan inmediatamente cuando el servidor cae. Puede utilizarse
  si la comprobación de estado detecta casos más complejos que un simple estado de conexión, y
  unos tiempos de espera largos harían que el servicio permaneciera sin respuesta durante
  demasiado tiempo. Por ejemplo, una comprobación de estado podría detectar que una base de
  datos está bloqueada y que ya no hay posibilidad de reutilizar las conexiones existentes. Las
  conexiones terminadas de esta manera se registran con un código de terminación 'D' (de
  "Down").

Las acciones están desactivadas por defecto

<a id="entry-5-2-on-marked-up"></a>

**`on-marked-up <action>`**

```haproxy
on-marked-up <action>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Modifica lo que ocurre cuando un servidor se marca como activo. Actualmente hay una acción
disponible:

- shutdown-backup-sessions: Termina los flujos en todos los servidores de respaldo. Esto se
  hace solo si el servidor no está en estado de respaldo y no está desactivado (debe tener un
  peso efectivo \> 0). Esto puede utilizarse a veces para forzar que un servidor activo recupere
  todo el tráfico después de una recuperación cuando se manejan sesiones largas (p. ej., LDAP,
  SQL, ...). Hacerlo puede causar más problemas de los que intenta resolver (p. ej.,
  transacciones incompletas), así que usa esta característica con extremo cuidado. Los flujos
  terminados porque un servidor se levanta se registran con un código de terminación 'U' (de
  "Up").

Las acciones están desactivadas por defecto

<a id="entry-5-2-pool-conn-name"></a>

**`pool-conn-name <expr>`**

```haproxy
pool-conn-name <expr>
```

Puede utilizarse en los siguientes contextos: http

Cuando se establece una conexión con el backend, esta expresión se evalúa para generar el nombre
de la conexión. Este nombre es una de las propiedades clave de la conexión en el pool de conexiones inactivas al servidor. Consulta la palabra clave «http-reuse». Cuando una solicitud busca una
conexión inactiva existente, esta expresión se evalúa para encontrar una conexión idéntica.

En un contexto donde se utiliza SNI SSL para la conexión al backend, el nombre de la conexión se
asigna automáticamente al resultado de la expresión «sni». Esto se ajusta al uso más común. Para
configuraciones más avanzadas, puede utilizarse «pool-conn-name» para sobrescribirlo.

Consulta también: «http-reuse», «sni»

<a id="entry-5-2-pool-low-conn"></a>

**`pool-low-conn <max>`**

```haproxy
pool-low-conn <max>
```

Puede utilizarse en los siguientes contextos: http

Establece un umbral bajo en el número de conexiones inactivas de un servidor, por debajo del
cual un hilo no intentará robar una conexión a otro hilo. Esto puede ser útil para mejorar los
patrones de uso de CPU en escenarios con muchos servidores muy rápidos, para asegurar que todos
los hilos conserven siempre unas pocas conexiones inactivas en lugar de dejar que se acumulen
sobre un hilo y migren de hilo en hilo. Valores típicos del doble del número de hilos parecen
mostrar ya un rendimiento muy bueno con tiempos de respuesta submilisegundo. El valor por
defecto es cero, lo que indica que cualquier conexión inactiva puede utilizarse en cualquier
momento. Es el ajuste recomendado para un uso normal. Esto solo se aplica a conexiones que
pueden compartirse según los mismos principios que los aplicables a «http-reuse». En caso de
que el intercambio de conexiones entre hilos esté desactivado mediante
"tune.idle-pool.shared", puede volverse muy importante la utilización de este ajuste para
asegurarse de que cada hilo tenga siempre unas pocas conexiones, o la tasa de reutilización de
conexiones disminuirá a medida que aumente el número de hilos.

<a id="entry-5-2-pool-max-conn"></a>

**`pool-max-conn <max>`**

```haproxy
pool-max-conn <max>
```

Puede utilizarse en los siguientes contextos: http

Establece el número máximo de conexiones inactivas de un servidor. -1 significa conexiones
ilimitadas, 0 significa ninguna conexión inactiva. El valor por defecto es -1. Cuando las
conexiones inactivas están activadas, las conexiones inactivas huérfanas que ya no pertenecen a
ninguna sesión de cliente se trasladan a un pool dedicado para que sigan siendo utilizables por
clientes futuros. Esto solo se aplica a conexiones que pueden compartirse según los mismos
principios que los aplicables a «http-reuse».

<a id="entry-5-2-pool-purge-delay"></a>

**`pool-purge-delay <delay>`**

```haproxy
pool-purge-delay <delay>
```

Puede utilizarse en los siguientes contextos: http

Establece el retardo para comenzar la purga de conexiones inactivas. Cada intervalo `<delay>`, se
cierra la mitad de las conexiones inactivas. 0 significa que no se conserva ninguna conexión
inactiva. El valor por defecto es 5s.

<a id="entry-5-2-port"></a>

**`port <port>`**

```haproxy
port <port>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Mediante el parámetro «port», es posible utilizar un puerto diferente para enviar las
comprobaciones de estado o para sondear el agent-check. En algunos servidores, puede ser
deseable dedicar un puerto a un componente específico capaz de realizar pruebas complejas más
adecuadas para comprobaciones de estado que la aplicación. Es común, por ejemplo, ejecutar un
script sencillo en inetd. Este parámetro se ignora si el parámetro «check» no está establecido.
Consulta también el parámetro «addr».

<a id="entry-5-2-proto"></a>

**`proto <name>`**

```haproxy
proto <name>
```

Puede utilizarse en los siguientes contextos: tcp, http

Fuerza el protocolo del multiplexor que se utilizará para las conexiones salientes a este
servidor. Debe ser compatible con el modo del backend (TCP o HTTP). También debe poder
utilizarse en el lado del backend. La lista de protocolos disponibles se muestra en haproxy -vv.
Se informan las propiedades de los protocolos: el modo (TCP/HTTP), el lado (FE/BE), el nombre
del mux y sus indicadores.

Algunos protocolos están sujetos al bloqueo de cabeza de línea en el lado del servidor
(flag=HOL_RISK). Finalmente, algunos protocolos no admiten cambios de protocolo (flag=NO_UPG). La
compatibilidad HTX también se informa (flag=HTX).

Estos son los protocolos que pueden utilizarse como argumento de una directiva «proto» en una
línea de servidor:

```text
quic: mode=HTTP  side=FE|BE  mux=QUIC  flags=HTX|NO_UPG|FRAMED
qmux: mode=HTTP  side=FE|BE  mux=QMUX  flags=HTX|NO_UPG
h2  : mode=HTTP  side=FE|BE  mux=H2    flags=HTX|HOL_RISK|NO_UPG
fcgi: mode=HTTP  side=BE     mux=FCGI  flags=HTX|HOL_RISK|NO_UPG
h1  : mode=HTTP  side=FE|BE  mux=H1    flags=HTX|NO_UPG
none: mode=TCP   side=FE|BE  mux=PASS  flags=NO_UPG
spop: mode=SPOP  side=BE     mux=SPOP  flags=HOL_RISK|NO_UPG
```

La idea detrás de esta opción es omitir la selección del mejor protocolo de multiplexor para
todas las conexiones establecidas a este servidor.

Si los ajustes de ALPN o NPN están configurados, los protocolos especificados deberían ser
compatibles con el protocolo del multiplexor para evitar cualquier problema. Por ejemplo, si se
establece "proto h1", el ALPN no debería establecerse en "h2".

Consulta también «ws» para utilizar un protocolo alternativo para los flujos websocket.

QMux es un subconjunto de QUIC que funciona sobre TCP. Corresponde al siguiente protocolo en
borrador <https://www.ietf.org/archive/id/draft-ietf-quic-qmux-01.html>. Por ahora se considera
experimental en haproxy.

<a id="entry-5-2-quic-cc-algo"></a>

**`quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]`**

```haproxy
quic-cc-algo { cubic | newreno | bbr | nocc }[(<args,...>)]
```

Este es un ajuste específico de QUIC para seleccionar el algoritmo de control de congestión para
cualquier conexión dirigida a este servidor. Son similares a los utilizados por TCP. Consulta la
opción bind con un nombre similar para una descripción completa de todas las opciones de
personalización.

Valor por defecto: cubic

Consulta también: "tune.quic.be.tx.pacing" y "tune.quic.be.cc.max-win-size"

<a id="entry-5-2-redir"></a>

**`redir <prefix>`**

```haproxy
redir <prefix>
```

Puede utilizarse en los siguientes contextos: http

El parámetro «redir» activa el modo de redirección para todas las solicitudes GET y HEAD
dirigidas a este servidor. Esto significa que, en lugar de que HAProxy reenvíe la solicitud al
servidor, enviará una respuesta "HTTP 302" con el encabezado «Location» compuesto por este
prefijo seguido inmediatamente del URI solicitado comenzando por la '/' inicial del componente
de ruta. Esto significa que no debe usarse ninguna barra diagonal final después de `<prefix>`.
Todas las solicitudes no válidas serán rechazadas, y todas las solicitudes que no sean GET o
HEAD serán atendidas con normalidad por el servidor. Ten en cuenta que, dado que la respuesta
está completamente falsificada, no es posible la manipulación de encabezados ni la inserción de
cookies en la respuesta. Sin embargo, las cookies en las solicitudes se siguen analizando, lo
que hace esta solución completamente utilizable para dirigir a los usuarios a una ubicación
remota en caso de desastre local. Su uso principal consiste en aumentar el ancho de banda de
los servidores estáticos haciendo que los clientes se conecten directamente a ellos. Nota:
nunca uses una ubicación relativa aquí, ¡ello causaría un bucle entre el cliente y HAProxy!

Ejemplo: server srv1 192.168.1.1:80 redir <http://image1.mydomain.com> check

<a id="entry-5-2-renegotiate"></a>

**`renegotiate`**

```haproxy
renegotiate
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción activa el mecanismo de renegociación segura (extensión de indicación de
renegociación TLS de la RFC 5746) para un backend SSL dado. No significa que el cliente SSL
envíe solicitudes de renegociación; solo permite a los backends renegociar cuando los servidores
lo solicitan. Sigue siendo necesario que la biblioteca SSL subyacente soporte realmente la
renegociación. Esta opción también está disponible en la instrucción global
«ssl-default-server-options». La renegociación ya no es posible en TLS 1.3. Si no se especifica
ni «renegotiate» ni «no-renegotiate», se mantiene el comportamiento por defecto de la
biblioteca SSL. Ten en cuenta que, por ejemplo, la biblioteca OpenSSL activa la renegociación
segura por defecto, mientras que AWS-LC la desactiva.

<a id="entry-5-2-rise"></a>

**`rise <count>`**

```haproxy
rise <count>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

El parámetro «rise» establece que un servidor se considerará operativo tras `<count>`
comprobaciones de estado consecutivas exitosas. Este valor por defecto es 2 si no se especifica.
Consulta también los parámetros «check», «inter» y «fall».

resolve-opts `<option>`,`<option>`,... Puede utilizarse en los siguientes contextos: tcp, http, log

Lista de opciones separadas por comas que se aplican a la resolución DNS vinculada a este
servidor.

Opciones disponibles:

- allow-dup-ip Por defecto, HAProxy impide la duplicación de direcciones IP en un backend cuando
  la resolución DNS en tiempo de ejecución está en operación. Dicho esto, en algunos casos tiene
  sentido que dos servidores (en el mismo backend, resueltos por el mismo FQDN) tengan la misma
  dirección IP. Para tal caso, basta con activar esta opción. Es lo contrario de prevent-dup-ip.

- ignore-weight Ignora cualquier peso que esté establecido en un registro SRV. Esto es útil
  cuando deseas controlar los pesos mediante un método alternativo, como usar un «agent-check»
  o a través de la API en tiempo de ejecución.

- prevent-dup-ip Asegura que el comportamiento por defecto de HAProxy se aplique en un servidor:
  impide reutilizar una dirección IP ya asignada a un servidor en el mismo backend y que
  comparte el mismo fqdn. Es lo contrario de allow-dup-ip.

Ejemplo:

```text
backend b_myapp
  default-server init-addr none resolvers dns
  server s1 myapp.example.com:80 check resolve-opts allow-dup-ip
  server s2 myapp.example.com:81 check resolve-opts allow-dup-ip
```

Con la opción allow-dup-ip establecida:

- si el servidor de nombres devuelve una única dirección IP, ambos servidores la usarán
- Si el servidor de nombres devuelve 2 direcciones IP, cada servidor tomará una dirección
  diferente

Valor por defecto: sin establecer

<a id="entry-5-2-resolve-prefer"></a>

**`resolve-prefer <family>`**

```haproxy
resolve-prefer <family>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Cuando la resolución DNS está activada para un servidor y se devuelven varias direcciones IP de
familias diferentes, HAProxy preferirá utilizar una dirección IP de la familia mencionada en el
parámetro «resolve-prefer». Consulta también la palabra clave global «dns-accept-family» para
imponer el uso estricto de una familia específica. Familias disponibles: "ipv4" e "ipv6".

Valor por defecto: ipv6

Ejemplo:

```text
server s1 app1.domain.com:80 resolvers mydns resolve-prefer ipv6
```

<a id="entry-5-2-resolve-net"></a>

**`resolve-net <network>[,<network[,...]]`**

```haproxy
resolve-net <network>[,<network[,...]]
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción prioriza la elección de una dirección IP que coincida con una red. Esto es útil con
los entornos cloud para preferir una IP local. En algunos casos, un servicio de alta
disponibilidad de cloud puede anunciarse con muchas direcciones IP en muchos centros de datos
diferentes. La latencia entre centros de datos no es despreciable, así que este parche permite
preferir un centro de datos local. Si ninguna dirección coincide con la red configurada, se
selecciona otra dirección.

Ejemplo:

```text
server s1 app1.domain.com:80 resolvers mydns resolve-net 10.0.0.0/8
```

<a id="entry-5-2-resolvers"></a>

**`resolvers <id>`**

```haproxy
resolvers <id>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Apunta a una sección «resolvers» existente para resolver el nombre de host del servidor actual.
A menudo se recomienda desactivar la resolución basada en libc cuando se usan resolvers, aunque
existen excepciones (consulta la [sección 5.3.1](/es/haproxy/bind-and-server-options/#section-5-3-1)). En cualquier caso, es una buena práctica especificar
explícitamente «init-addr» al usar resolvers para no pasar por alto este elemento.

Ejemplo:

```text
server s1 app1.domain.com:80 init-addr last,none check resolvers mydns
```

Consulta también la [sección 5.3](/es/haproxy/bind-and-server-options/#section-5-3) para los detalles de implementación y las trampas que conviene conocer.

<a id="entry-5-2-send-proxy"></a>

**`send-proxy`**

```haproxy
send-proxy
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «send-proxy» impone el uso del protocolo PROXY sobre cualquier conexión establecida
con este servidor. El protocolo PROXY informa al otro extremo de las direcciones de capa 3/4 de
la conexión entrante, de modo que pueda conocer la dirección del cliente o la dirección pública
a la que accedió, sea cual sea el protocolo de capa superior. Para las conexiones aceptadas por
un listener «accept-proxy» o «accept-netscaler-cip», se utilizará la dirección anunciada. Solo
se soportan las familias de direcciones TCPv4 y TCPv6. Otras familias, como los sockets Unix,
informarán de una familia UNKNOWN. Los servidores que usan esta opción pueden encadenarse por
completo a otra instancia de HAProxy que escuche con un ajuste «accept-proxy». Este ajuste no
debe usarse si el servidor no conoce el protocolo. Cuando se envían comprobaciones de estado al
servidor, el protocolo PROXY se usa automáticamente cuando esta opción está establecida, salvo
que exista una directiva explícita «port» o «addr», en cuyo caso también se necesitaría una
directiva explícita «check-send-proxy» para usar el protocolo PROXY. Consulta también la opción
«no-send-proxy» de esta sección y las opciones «accept-proxy» y «accept-netscaler-cip» de la
palabra clave «bind».

<a id="entry-5-2-send-proxy-v2"></a>

**`send-proxy-v2`**

```haproxy
send-proxy-v2
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «send-proxy-v2» impone el uso de la versión 2 del protocolo PROXY sobre cualquier
conexión establecida con este servidor. El protocolo PROXY informa al otro extremo de las
direcciones de capa 3/4 de la conexión entrante, de modo que pueda conocer la dirección del
cliente o la dirección pública a la que accedió, sea cual sea el protocolo de capa superior.
También envía información de ALPN si se ha negociado un alpn. Este ajuste no debe usarse si el
servidor no conoce esta versión del protocolo. Consulta también la opción «no-send-proxy-v2» de
esta sección y la opción «send-proxy» de la palabra clave «bind».

<a id="entry-5-2-set-proxy-v2-tlv-fmt"></a>

**`set-proxy-v2-tlv-fmt(<id>) <fmt>`**

```haproxy
set-proxy-v2-tlv-fmt(<id>) <fmt>
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «set-proxy-v2-tlv-fmt» se utiliza para enviar TLVs arbitrarios de la versión 2 del
protocolo PROXY. Para el rango de tipos (`<id>`) del tipo de TLV definido, consulta la sección
2.2.8 de la especificación del protocolo PROXY. Sin embargo, el valor puede elegirse libremente
siempre que no exceda la longitud máxima de 65,535 bytes. También puede utilizarse para
reenviar TLVs usando la extracción "fc_pp_tlv" para recuperar un TLV recibido desde el frontend.
Puede usarse como opción de servidor o de default-server. Debe utilizarse en combinación con
send-proxy-v2 para que los TLVs de PPv2 se envíen efectivamente.

Ejemplo: server srv1 192.168.1.1:80 send-proxy-v2 set-proxy-v2-tlv-fmt(0x20) %[fc_pp_tlv(0x20)]

En este caso, obtenemos el TLV con el tipo 0x20 como cadena de texto y lo establecemos como
valor de un TLV recién creado que también tiene el tipo 0x20.

<a id="entry-5-2-proxy-v2-options"></a>

**`proxy-v2-options <option>[,<option>]*`**

```haproxy
proxy-v2-options <option>[,<option>]*
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «proxy-v2-options» añade opciones que enviar en la versión 2 del protocolo PROXY
cuando se usa «send-proxy-v2». Las opciones disponibles son:

- ssl : Consulta también «send-proxy-v2-ssl».
- cert-cn : Consulta también «send-proxy-v2-ssl-cn».
- ssl-cipher: Nombre del cifrado utilizado.
- cert-sig : Algoritmo de firma del certificado utilizado.
- cert-key : Algoritmo de clave del certificado utilizado.
- authority: Valor del nombre de host pasado por el cliente (solo se soporta el SNI de una
  conexión TLS).
- crc32c : Suma de comprobación del encabezado PROXYv2.
- unique-id: Envía un ID único generado usando el «unique-id-format» del frontend dentro del
  encabezado PROXYv2. Este unique-id está destinado principalmente a «mode tcp». Puede
  provocar resultados inesperados en «mode http», porque el ID único generado también se usa
  para la primera solicitud HTTP dentro de una conexión Keep-Alive.

<a id="entry-5-2-send-proxy-v2-ssl"></a>

**`send-proxy-v2-ssl`**

```haproxy
send-proxy-v2-ssl
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «send-proxy-v2-ssl» impone el uso de la versión 2 del protocolo PROXY sobre
cualquier conexión establecida con este servidor. El protocolo PROXY informa al otro extremo de
las direcciones de capa 3/4 de la conexión entrante, de modo que pueda conocer la dirección del
cliente o la dirección pública a la que accedió, sea cual sea el protocolo de capa superior.
Además, la extensión de información SSL del protocolo PROXY se añade al encabezado del
protocolo PROXY. Este ajuste no debe usarse si el servidor no conoce esta versión del
protocolo. Consulta también la opción «no-send-proxy-v2-ssl» de esta sección y la opción
«send-proxy-v2» de la palabra clave «bind».

<a id="entry-5-2-send-proxy-v2-ssl-cn"></a>

**`send-proxy-v2-ssl-cn`**

```haproxy
send-proxy-v2-ssl-cn
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «send-proxy-v2-ssl» impone el uso de la versión 2 del protocolo PROXY sobre
cualquier conexión establecida con este servidor. El protocolo PROXY informa al otro extremo de
las direcciones de capa 3/4 de la conexión entrante, de modo que pueda conocer la dirección del
cliente o la dirección pública a la que accedió, sea cual sea el protocolo de capa superior.
Además, la extensión de información SSL del protocolo PROXY, junto con el Common Name del
sujeto del certificado del cliente (si lo hay), se añade al encabezado del protocolo PROXY.
Este ajuste no debe usarse si el servidor no conoce esta versión del protocolo. Consulta también
la opción «no-send-proxy-v2-ssl-cn» de esta sección y la opción «send-proxy-v2» de la palabra
clave «bind».

<a id="entry-5-2-shard"></a>

**`shard <shard>`**

```haproxy
shard <shard>
```

Puede utilizarse en los siguientes contextos: peers

Este parámetro se usa solo en el contexto de la sincronización de stick-tables con el protocolo
de peers. El parámetro «shard» identifica los peers que recibirán todas las actualizaciones de
la stick-table para las claves que tengan este shard como hash de distribución. Los valores
aceptados van de 0 al valor del parámetro «shards» especificado en la sección «peers». El valor
0 es el valor por defecto y significa que el peer recibirá todas las actualizaciones de claves.
Los valores mayores que «shards» se ignorarán. Esto también ocurre con cualquier valor
proporcionado al peer local.

Ejemplo:

```haproxy
peers mypeers
     shards 3
     peer A 127.0.0.1:40001 # local peer without shard value (0 internally)
     peer B 127.0.0.1:40002 shard 1
     peer C 127.0.0.1:40003 shard 2
     peer D 127.0.0.1:40004 shard 3
```

<a id="entry-5-2-sigalgs"></a>

**`sigalgs <sigalgs>`**

```haproxy
sigalgs <sigalgs>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Este ajuste solo está disponible si se compiló con soporte para OpenSSL. Establece la cadena
que describe la lista de algoritmos de firma que se negocian durante la negociación TLSv1.2 y
TLSv1.3. El formato de la cadena está definido en "man 3 SSL_CTX_set1_sigalgs" de las páginas
de manual de OpenSSL. No se recomienda usar este ajuste a menos que se requiera compatibilidad
con un middlebox.

<a id="entry-5-2-slowstart"></a>

**`slowstart <start_time_in_ms>`**

```haproxy
slowstart <start_time_in_ms>
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «slowstart» de un servidor acepta un valor en milisegundos que indica tras cuánto
tiempo un servidor que acaba de volver a estar activo funcionará a plena velocidad. Igual que
con cualquier otro parámetro basado en tiempo, puede introducirse en cualquier otra unidad
explícita de entre { us, ms, s, m, h, d }. La velocidad crece linealmente de 0 a 100% durante
este tiempo. La limitación se aplica a dos parámetros:

- maxconn: el número de conexiones aceptadas por el servidor crecerá del 1 al 100% del límite
  dinámico habitual definido por (minconn,maxconn,fullconn).

- weight: cuando el backend usa un algoritmo de ponderación dinámica, el peso crece linealmente
  de 1 a 100%. En este caso, el peso se actualiza en cada comprobación de estado. Por esta
  razón, es importante que el parámetro «inter» sea menor que «slowstart», para maximizar el
  número de pasos.

El slowstart nunca se aplica cuando HAProxy arranca, de lo contrario causaría problemas a los
servidores en ejecución. Solo se aplica cuando un servidor se ha visto previamente como
fallido.

<a id="entry-5-2-sni"></a>

**`sni <expression>`**

```haproxy
sni <expression>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

El parámetro «sni» evalúa la expresión de extracción de muestra, la convierte a una cadena de
texto y utiliza el resultado como nombre de host enviado en la extensión TLS SNI al servidor.
Un caso de uso típico es enviar el SNI recibido del cliente en un escenario TCP/SSL en puente,
usando la extracción de muestra "ssl_fc_sni" para la expresión. ESTO NO DEBE UTILIZARSE PARA
HTTPS, donde debería usarse req.hdr(host) en su lugar, ya que el SNI en HTTPS debe coincidir
siempre con el campo Host y los clientes pueden usar nombres de host diferentes sobre la misma
conexión). Si se establece «verify required» (que es el ajuste recomendado), el nombre
resultante también se cotejará con los nombres del certificado del servidor. Consulta la directiva
«verify» para más detalles. Si deseas establecer un SNI para las comprobaciones de estado,
consulta la directiva «check-sni» para más detalles.

Por defecto, el SNI se asigna al nombre de conexión para «http-reuse», a menos que lo
sobrescriba la palabra clave de servidor «pool-conn-name».

<a id="entry-5-2-sni-auto"></a>

**`sni-auto`**

```haproxy
sni-auto
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

El parámetro «sni-auto» activa la selección automática del SNI, si ningún valor se ha
establecido ya. Establece la expresión «sni» como "req.hdr(host),field(1,:)", lo que significa
que se presentará un SNI con el nombre de host de la solicitud que se envía al servidor, pero
descartando el número de puerto. Está activado por defecto, pero este parámetro puede
utilizarse como ajuste «server» para restablecer cualquier ajuste «no-sni-auto» que se haya
heredado como valor por defecto de la directiva «default-server». También puede utilizarse
como ajuste «default-server» para restablecer cualquier ajuste «no-sni-auto» de
«default-server» anterior.

Para las conexiones HTTPS, el SNI seleccionado se basa en el valor del encabezado host de la
solicitud, si se encuentra. De lo contrario, permanece sin establecer. Para otros protocolos,
la opción se ignora.

Si se utiliza la selección automática del SNI, el valor se asigna al nombre de conexión para
«http-reuse», a menos que lo sobrescriba la palabra clave de servidor «pool-conn-name».

Consulta la opción «check-sni-auto» para activar la selección automática del SNI para las
comprobaciones de estado SSL.

<a id="entry-5-2-source"></a>

**`source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<pl>[-<ph>]] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<pl>[-<ph>]] [interface <name>] ...
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

El parámetro «source» establece la dirección de origen que se utilizará al conectarse al
servidor. Sigue exactamente los mismos parámetros y principios que la palabra clave «source»
del backend, excepto que solo se aplica al servidor que la referencia. Consulta la palabra
clave «source» para más detalles.

Además, la instrucción «source» en una línea de servidor permite especificar un rango de
puertos de origen indicando los límites inferior y superior delimitados por un guion ('-').
Algunos sistemas operativos podrían requerir una dirección IP válida cuando se especifica un
rango de puertos de origen. Está permitido usar la misma IP/rango para varios servidores.
Hacerlo hace posible sobrepasar el máximo de 64k conexiones simultáneas totales. El límite
alcanzará entonces las 64k conexiones por servidor.

Desde Linux 4.2/libc 2.23, IP_BIND_ADDRESS_NO_PORT se establece para las conexiones que
especifican la dirección de origen sin puerto(s).

<a id="entry-5-2-ssl"></a>

**`ssl`**

```haproxy
ssl
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción activa el cifrado SSL en las conexiones salientes al servidor. Es crítico verificar
los certificados del servidor usando «verify» cuando se usa SSL para conectarse a los
servidores; de lo contrario, la comunicación es propensa a ataques triviales de intermediario
que hacen inútil el SSL. Cuando se usa esta opción, las comprobaciones de estado se envían
automáticamente también en SSL, salvo que haya una directiva «port» o «addr» indicando que la
comprobación debe enviarse a una ubicación diferente. Consulta «no-ssl» para desactivar la opción
«ssl» y «check-ssl» para forzar comprobaciones de estado SSL.

<a id="entry-5-2-ssl-max-ver"></a>

**`ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-max-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción impone el uso de `<version>` o inferior cuando se utiliza SSL para comunicarse con
el servidor. Esta opción también está disponible en la instrucción global
«ssl-default-server-options». Consulta también «ssl-min-ver».

<a id="entry-5-2-ssl-min-ver"></a>

**`ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]`**

```haproxy
ssl-min-ver [ SSLv3 | TLSv1.0 | TLSv1.1 | TLSv1.2 | TLSv1.3 ]
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción impone el uso de `<version>` o superior cuando se utiliza SSL para comunicarse con
el servidor. Esta opción también está disponible en la instrucción global
«ssl-default-server-options». Consulta también «ssl-max-ver».

<a id="entry-5-2-ssl-reuse"></a>

**`ssl-reuse`**

```haproxy
ssl-reuse
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«no-ssl-reuse» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«no-ssl-reuse» de «default-server» anterior.

<a id="entry-5-2-stick"></a>

**`stick`**

```haproxy
stick
```

Puede utilizarse en los siguientes contextos: tcp, http

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«non-stick» que se haya heredado como valor por defecto de la directiva «default-server».
También puede utilizarse como ajuste «default-server» para restablecer cualquier ajuste
«non-stick» de «default-server» anterior.

<a id="entry-5-2-strict-maxconn"></a>

**`strict-maxconn`**

```haproxy
strict-maxconn
```

Puede utilizarse en los siguientes contextos: tcp, http

maxconn hacia los servidores es un nombre algo equívoco: en realidad configura el número máximo
de solicitudes que enviamos a un servidor, pero, con conexiones inactivas, podemos tener más
conexiones totales al servidor. Si se requiere un límite estricto de conexiones a un servidor,
puede añadirse strict-maxconn. Nunca estableceremos entonces más conexiones a un servidor que
maxconn, e intentaremos reutilizar o matar conexiones si es necesario. Ten en cuenta, sin
embargo, que puede provocar solicitudes fallidas en caso de que no podamos establecer una nueva
conexión y no haya ninguna conexión inactiva disponible. Esto puede ocurrir cuando se
establecen conexiones «privadas», conexiones ligadas solo a una sesión, porque ocurrió una
autenticación.

<a id="entry-5-2-socks4"></a>

**`socks4 <addr>:<port>`**

```haproxy
socks4 <addr>:<port>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción activa un túnel socks4 ascendente para las conexiones salientes al servidor. Usar
esta opción no fuerza por defecto que la comprobación de estado pase por socks4. Tendrás que
usar la palabra clave «check-via-socks4» para activarlo.

<a id="entry-5-2-tcp-md5sig"></a>

**`tcp-md5sig <password>`**

```haproxy
tcp-md5sig <password>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Activa la firma MD5 de TCP (RFC 2385, protección de sesiones BGP mediante la opción de firma
MD5 de TCP) para todas las conexiones salientes a este servidor. Esta opción solo está
disponible en Linux. Cuando está activada, la cadena `<password>` se usa para firmar cada
segmento TCP con un resumen MD5 de 16 bytes. Esto protegerá la conexión TCP contra la
suplantación. El caso de uso principal de esta opción es permitir que BGP se proteja contra la
introducción de segmentos TCP falsificados en el flujo de la conexión. Pero puede ser útil para
cualquier conexión TCP de muy larga duración.

<a id="entry-5-2-tcp-ut"></a>

**`tcp-ut <delay>`**

```haproxy
tcp-ut <delay>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Establece el TCP User Timeout para todas las conexiones salientes a este servidor. Esta opción
está disponible en Linux desde la versión 2.6.37. Permite a HAProxy configurar un tiempo de
espera para los sockets que contienen datos que no reciben un reconocimiento durante el retardo
configurado. Esto es especialmente útil en conexiones de larga duración con largos periodos de
inactividad, como terminales remotos o pools de conexiones a bases de datos, donde los tiempos
de espera del cliente y del servidor deben permanecer altos para permitir un largo periodo de
inactividad, pero donde es importante detectar que el servidor ha desaparecido para liberar
todos los recursos asociados a su conexión (y a la sesión del cliente). Un caso de uso típico
es también forzar la muerte de las conexiones a un servidor muerto cuando las comprobaciones
de estado son demasiado lentas o durante una recarga suave, ya que entonces las comprobaciones
de estado están desactivadas. El argumento es un retardo expresado en milisegundos por defecto.
Esto solo funciona para conexiones TCP regulares y se ignora para otros protocolos.

<a id="entry-5-2-tfo"></a>

**`tfo`**

```haproxy
tfo
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción permite usar TCP fast open al conectarse a los servidores, en sistemas que lo
soportan (actualmente solo el kernel Linux \>= 4.11). Consulta la opción bind «tfo» para más
información sobre TCP fast open. Ten en cuenta que al usar tfo, también deberías usar las
palabras clave «conn-failure», «empty-response» y «response-timeout» para «retry-on», o HAProxy
no podrá reintentar la conexión en caso de fallo. Consulta también «no-tfo».

<a id="entry-5-2-track"></a>

**`track [<backend>/]<server>`**

```haproxy
track [<backend>/]<server>
```

Puede utilizarse en los siguientes contextos: tcp, http, log

Esta opción permite establecer el estado actual de un servidor siguiendo el de otro. Es posible
seguir un servidor que a su vez sigue a otro servidor, siempre que al final de la cadena un
servidor tenga las comprobaciones de estado activadas. Si se omite `<backend>`, se usa el
actual. Si se usa disable-on-404, debe estar activado en ambos proxies.

Ejemplo:

```text
backend A
server a1 1.1.1.1:80 track B/b1
server a2 1.1.1.2:80 track B/b1

backend B
server b1 2.2.2.2:80 check
```

<a id="entry-5-2-tls-tickets"></a>

**`tls-tickets`**

```haproxy
tls-tickets
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Esta opción puede utilizarse como ajuste «server» para restablecer cualquier ajuste
«no-tls-tickets» que se haya heredado como valor por defecto de la directiva
«default-server». El mecanismo de tickets TLS solo se usa hasta TLS 1.2. La confidencialidad
directa queda comprometida con los tickets TLS, a menos que las claves de los tickets se roten
periódicamente (mediante recarga o usando «tls-ticket-keys»). También puede utilizarse como
ajuste «default-server» para restablecer cualquier ajuste «no-tls-tickets» de «default-server»
anterior.

<a id="entry-5-2-verify"></a>

**`verify [none|required]`**

```haproxy
verify [none|required]
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Este ajuste solo está disponible si se compiló con soporte para OpenSSL. Si se establece en
'none', no se verifica el certificado del servidor. En el otro caso, el certificado
proporcionado por el servidor se verifica usando las CA de 'ca-file' y las CRL opcionales de
'crl-file', después de haber comprobado que los nombres proporcionados en los atributos
subject y subjectAlternateNames del certificado coinciden con el nombre pasado mediante la
directiva «sni», o, si no se proporciona, con el nombre de host estático pasado mediante la
directiva «verifyhost». Cuando no se encuentra ningún nombre, los nombres del certificado se
ignoran. Por esta razón, sin SNI es importante usar «verifyhost». En caso de fallo de la
verificación, la negociación se aborta. Es de importancia crítica verificar los certificados
del servidor al usar SSL para conectarse a servidores; de lo contrario, la comunicación es
propensa a ataques triviales de intermediario que hacen totalmente inútil el SSL. A menos que
"ssl_server_verify" aparezca en la sección global, «verify» está establecido en «required» por
defecto.

<a id="entry-5-2-verifyhost"></a>

**`verifyhost <hostname>`**

```haproxy
verifyhost <hostname>
```

Puede utilizarse en los siguientes contextos: tcp, http, log, peers, ring

Este ajuste solo está disponible si se compiló con soporte para OpenSSL, y solo surte efecto si
también se especifica 'verify required'. Esta directiva establece un nombre de host estático
por defecto contra el cual comprobar el certificado del servidor cuando no se usó SNI para
conectarse al servidor. Si no se usa SNI, esta es la única forma de activar la verificación del
nombre de host. Este nombre de host estático, cuando se establece, también se usará para las
comprobaciones de estado cuando no se proporcione un valor SNI. Si ninguno de los nombres de
host del certificado coincide con el nombre de host especificado, la negociación se aborta. Los
nombres de host del certificado proporcionado por el servidor pueden incluir comodines. Consulta
también las opciones «verify», «sni» y «no-verifyhost».

<a id="entry-5-2-weight"></a>

**`weight <weight>`**

```haproxy
weight <weight>
```

Puede utilizarse en los siguientes contextos: tcp, http

El parámetro «weight» se usa para ajustar el peso del servidor en relación con otros
servidores. Todos los servidores recibirán una carga proporcional a su peso respecto a la suma
de todos los pesos, de modo que cuanto mayor el peso, mayor la carga. El peso por defecto es 1
y el valor máximo es 256. Un valor de 0 significa que el servidor no participará en el balanceo
de carga, pero seguirá aceptando conexiones persistentes. Si este parámetro se usa para
distribuir la carga según la capacidad del servidor, se recomienda empezar con valores que
puedan tanto crecer como reducirse, por ejemplo entre 10 y 100, para dejar suficiente margen
por encima y por debajo para ajustes posteriores.

<a id="entry-5-2-ws"></a>

**`ws { auto | h1 | h2 }`**

```haproxy
ws { auto | h1 | h2 }
```

Puede utilizarse en los siguientes contextos: http

Esta opción permite configurar el protocolo utilizado al retransmitir flujos websocket. Esto es
más notablemente útil cuando se usa un backend HTTP/2 sin soporte para los websockets H2
mediante la RFC8441.

El modo por defecto es "auto". Esto reutilizará el mismo protocolo que el principal. La única
diferencia es al usar ALPN. En este caso, puede intentar degradar el ALPN a "http/1.1" solo
para los flujos websocket si el ALPN configurado del servidor lo contiene.

El valor "h1" se usa para forzar HTTP/1.1 para los flujos websocket, a través de ALPN si el
ALPN SSL está activado para el servidor. De forma similar, "h2" puede usarse para forzar los
websockets HTTP/2.0. Usa este valor con cuidado: el servidor debe soportar la RFC8441 o se
reportará un error por haproxy al retransmitir websockets.

Ten en cuenta que NPN no se tiene en cuenta, ya que su uso ha quedado obsoleto en favor de la
extensión ALPN.

Consulta también «alpn» y «proto».

## 5.3. Resolución de direcciones IP del servidor mediante DNS {#section-5-3}

HAProxy permite usar un nombre de host en la línea del servidor para recuperar su dirección IP
mediante servidores de nombres. Por defecto, HAProxy resuelve el nombre al analizar el archivo
de configuración, en el arranque, y almacena en caché el resultado durante la vida del proceso.
Esto no es suficiente en algunos casos, como en Amazon, donde la IP de un servidor puede
cambiar tras un reinicio o una IP virtual de un ELB puede cambiar según la carga de trabajo
actual.

Este capítulo describe cómo puede configurarse HAProxy para procesar la resolución de nombres
de los servidores en tiempo de ejecución.

Esté activada o no la resolución de nombres de servidor en tiempo de ejecución, por defecto
HAProxy realizará la primera resolución en el arranque, durante el análisis de la
configuración, vía libc, a menos que la desactive el parámetro «init-addr».

### 5.3.1. Vista general {#section-5-3-1}

Como hemos visto en la introducción, la resolución de nombres en HAProxy ocurre en dos pasos
diferentes de la vida del proceso:

```text
1. Al arrancar, HAProxy analiza la definición de la línea del servidor y
   encuentra un nombre de host. Utiliza las funciones de libc para resolver
   el nombre de host. Esta resolución se basa en el archivo /etc/resolv.conf.

2. En tiempo de ejecución, HAProxy realiza periódicamente resoluciones de
   nombres para los servidores que requieren resoluciones DNS.
```

Otros pocos eventos pueden desencadenar una resolución de nombres en tiempo de ejecución:

- cuando la comprobación de estado de un servidor termina en un tiempo de espera de conexión agotado:
  esto puede deberse a que el servidor tiene una nueva dirección IP. Por ello es necesario
  desencadenar una resolución de nombres para conocer esta nueva IP.

Al usar resolvers, el nombre del servidor puede ser un nombre de host o una etiqueta SRV.
HAProxy considera como etiqueta SRV todo lo que empiece por un guion bajo. Si se especifica una
etiqueta SRV, los registros SRV correspondientes se recuperarán del servidor DNS y se usarán
los nombres de host proporcionados. La etiqueta SRV se comprobará periódicamente y, si se
añade o elimina algún servidor, HAProxy hará lo mismo automáticamente.

Algunas cosas importantes que conviene notar:

- todos los servidores de nombres se consultan al mismo tiempo. HAProxy procesará la primera
  respuesta válida.

- una resolución se considera no válida (NX, timeout, refused) cuando todos
  los servidores devuelven un error.

- El cliente DNS implementado en HAProxy es muy básico y no comprenderá el gran número de
  opciones y configuraciones avanzadas con las que puede tratar el resolver de un sistema
  operativo. Por ello, salvo en configuraciones realmente triviales donde un servidor conocido
  por su FQDN tiene exactamente una dirección IP a la vez y podría renovarla ocasionalmente
  (p. ej., un reinicio), es altamente recomendable evitar mezclar la resolución en tiempo de
  inicialización basada en libc con la resolución en tiempo de ejecución basada en DNS, ya que
  se sabe que tales configuraciones causan fallos al renovar la dirección. En conclusión, salvo
  que sepas exactamente lo que haces, siempre deberías excluir «libc» de «init-addr» al usar
  «resolvers» en una línea de servidor.

### 5.3.2. La sección resolvers {#section-5-3-2}

Esta sección está dedicada a la información de hosts relacionada con la resolución de nombres
en HAProxy. Puede haber tantas secciones resolvers como se necesite. Cada sección puede
contener muchos servidores de nombres.

En el arranque, HAProxy intenta generar una sección resolvers llamada «default», si ninguna
sección fue nombrada así en la configuración. Esta sección es usada por defecto por el
httpclient y usa la palabra clave parse-resolv-conf. Si HAProxy no logró generar
automáticamente esta sección, no se emite ningún error ni advertencia.

Cuando se configuran varios servidores de nombres en una sección resolvers, HAProxy usa la
primera respuesta válida. En caso de respuestas no válidas, solo se trata la última. El
propósito es dar la oportunidad a un servidor lento de entregar una respuesta válida después
de un servidor rápido defectuoso u obsoleto.

Cuando cada servidor devuelve un tipo de error diferente, HAProxy solo usa el último error. Se
aplica el siguiente procesamiento a este error:

```text
1. HAProxy reintenta la misma consulta DNS con un nuevo tipo de consulta. Las
   consultas A pasan a AAAA o al contrario. Las consultas SRV no se ven
   afectadas aquí. Los errores de tiempo de espera agotado también se
   excluyen.

2. Cuando se hizo la conmutación al tipo de consulta (o no aplica), HAProxy
   reintenta la consulta DNS original, con el tipo de consulta preferido.

3. HAProxy reintenta los pasos anteriores <resolve_retries> veces. Si no se
   recibe ninguna respuesta válida después de eso, detiene la resolución DNS
   y reporta el error.
```

Por ejemplo, con 2 servidores de nombres configurados en una sección resolvers, son posibles
los siguientes escenarios:

- La primera respuesta es válida y se aplica directamente, la segunda respuesta se ignora

- La primera respuesta no es válida y la segunda es válida, entonces se aplica la segunda
  respuesta

- La primera respuesta es un dominio NX y la segunda una respuesta truncada, entonces HAProxy
  reintenta la consulta con un nuevo tipo

- La primera respuesta es un dominio NX y la segunda es un tiempo de espera agotado, entonces
  HAProxy reintenta la consulta con un nuevo tipo

- La consulta agotó el tiempo de espera para ambos servidores de nombres, entonces HAProxy la
  reintenta con el mismo tipo de consulta

Como un servidor DNS puede no responder con todas las IP en una sola solicitud DNS, HAProxy
mantiene una caché de respuestas anteriores; una respuesta se considerará obsoleta tras
`<hold obsolete>` segundos sin la IP devuelta.

<a id="entry-5-3-2-resolvers"></a>

**`resolvers <resolvers id>`**

```haproxy
resolvers <resolvers id>
```

Crea una nueva lista de servidores de nombres etiquetada `<resolvers id>`. Como se menciona
arriba, el nombre especial "default" siempre existe y se creará automáticamente si no se
declara explícitamente; esta será la que usen los servicios internos como httpclient. Declarar
una entrada «default» afectará a la forma en que estos servicios realizan su resolución de
nombres.

Una sección resolvers acepta los siguientes parámetros:

<a id="entry-5-3-2-accepted-payload-size"></a>

**`accepted_payload_size <nb>`**

```haproxy
accepted_payload_size <nb>
```

Define el tamaño máximo de carga útil aceptado por HAProxy y anunciado a todos los servidores
de nombres configurados en esta sección resolvers. `<nb>` está en bytes. Si no se establece,
HAProxy anuncia 512. (valor mínimo definido por el RFC 6891)

Nota: el valor máximo permitido es 65535. El valor recomendado para UDP es 4096 y no se
recomienda superar 8192, excepto si estás seguro de que tu sistema y tu red pueden manejarlo
(superar 65507 no tiene sentido, ya que es el tamaño máximo de carga útil UDP). Si usas solo
servidores de nombres TCP para manejar respuestas DNS enormes, deberías poner este valor al
máximo: 65535.

<a id="entry-5-3-2-nameserver"></a>

**`nameserver <name> <address>[:port] [param*]`**

```haproxy
nameserver <name> <address>[:port] [param*]
```

Se usa para configurar un servidor de nombres. El `<name>` del servidor de nombres debe ser
único. Por defecto, la `<address>` se considera de tipo datagrama. Esto significa que si se
configura una IPv4 o IPv6 sin prefijos de dirección especiales (párrafo 11.), se usará el
protocolo UDP. Si se usa un prefijo de dirección de protocolo de flujo, el servidor de nombres
se considerará un servidor de flujo (TCP por ejemplo) y se considerarán los parámetros
«server» del párrafo 5.2 que sean relevantes para la resolución DNS.
Nota: actualmente, en modo TCP, 4 consultas se envían en cadena sobre las mismas conexiones.
Un lote de conexiones inactivas se elimina cada 5 segundos. «maxconn» puede configurarse para
limitar la cantidad de esas conexiones simultáneas y TLS también debería poder utilizarse si
el servidor lo soporta.

<a id="entry-5-3-2-parse-resolv-conf"></a>

**`parse-resolv-conf`**

```haproxy
parse-resolv-conf
```

Añade todos los servidores de nombres encontrados en /etc/resolv.conf a esta lista de
servidores de nombres del resolver. Se ordenan como si cada servidor de nombres de
/etc/resolv.conf se hubiera colocado individualmente en la sección resolvers en lugar de esta
directiva.

<a id="entry-5-3-2-hold"></a>

**`hold <status> <period>`**

```haproxy
hold <status> <period>
```

Al recibir la respuesta DNS `<status>`, determina si el estado de un servidor debería cambiar
de UP a DOWN. Para tomar esa determinación, comprueba si se ha recibido algún estado válido
durante los últimos `<period>` para contrarrestar el estado no válido recién recibido.

    `<status>`: último estado de la resolución de nombres.
           nx        Tras recibir un estado NXDOMAIN, comprobar si hubo algún
                     estado válido durante el período anterior indicado.

           refused   Tras recibir un estado REFUSED, comprobar si hubo algún
                     estado válido durante el período anterior indicado.

           timeout   Una vez que ha vencido el "timeout retry", comprobar si
                     hubo algún estado válido durante el período anterior indicado.

           other     Tras recibir cualquier otro estado no válido, comprobar si
                     hubo algún estado válido durante el período anterior indicado.

           valid     Se aplica solo a las acciones "http-request do-resolve" y
                     "tcp-request content do-resolve". Define el período durante
                     el cual el servidor mantendrá una respuesta válida antes de
                     desencadenar otra resolución. No afecta a la resolución
                     dinámica de los servidores.

           obsolete  Define cuánto esperar antes de eliminar los registros DNS
                     obsoletos tras recibir un registro de respuesta
                     actualizado. Se aplica a los registros SRV.

    `<period>`: Cantidad de tiempo hacia el pasado durante la cual debe haberse
               recibido una respuesta válida. Sigue el formato de tiempo de
               HAProxy y está en milisegundos por defecto.

Para un servidor que depende de la resolución DNS dinámica para determinar su dirección IP,
recibir una respuesta DNS no válida, como NXDOMAIN, provocará el cambio del estado del
servidor de UP a DOWN. Las directivas hold definen cuánto retroceder en el pasado para buscar
una respuesta válida. Si se ha recibido una respuesta válida dentro de `<period>`, el estado
no válido recién recibido se ignorará.

A menos que se haya recibido una respuesta válida durante el período anterior indicado, el
servidor se marcará como DOWN. Por ejemplo, si se establece «hold nx 30s» y la última
respuesta DNS recibida fue NXDOMAIN, el servidor se marcará como DOWN a menos que se haya
recibido una respuesta válida durante los últimos 30 segundos.

Un servidor en estado DOWN se marcará como UP inmediatamente al recibir un estado válido del
servidor DNS.

Existe un comportamiento aparte para «hold valid» y «hold obsolete».

El valor por defecto es 10s para «valid», 0s para «obsolete» y 30s para los demás.

<a id="entry-5-3-2-resolve-retries"></a>

**`resolve_retries <nb>`**

```haproxy
resolve_retries <nb>
```

Define el número `<nb>` de consultas que enviar para resolver un nombre de servidor antes de
rendirse. Valor por defecto: 3

Se produce un reintento cuando se agota el tiempo de espera del servidor de nombres o cuando
la secuencia completa de conmutación por error de los tipos de consulta DNS ha terminado y hay
que empezar de nuevo desde el tipo de consulta ANY por defecto.

<a id="entry-5-3-2-timeout"></a>

**`timeout <event> <time>`**

```haproxy
timeout <event> <time>
```

Define los tiempos de espera relacionados con la resolución de nombres `<event>`: el evento al
que se aplica el período de tiempo de espera `<time>`. Los eventos disponibles son: - resolve:
tiempo por defecto para desencadenar resoluciones de nombres cuando no se aplica ningún otro
tiempo. Valor por defecto: 1s - retry : tiempo entre dos consultas DNS, cuando no se ha
recibido ninguna respuesta válida. Valor por defecto: 1s `<time>` : tiempo relacionado con el
evento. Sigue el formato de tiempo de HAProxy. `<time>` se expresa en milisegundos.

Ejemplo:

```text
resolvers mydns
  nameserver dns1 10.0.0.1:53
  nameserver dns2 10.0.0.2:53
  nameserver dns3 tcp@10.0.0.3:53
  parse-resolv-conf
  resolve_retries       3
  timeout resolve       1s
  timeout retry         1s
  hold other           30s
  hold refused         30s
  hold nx              30s
  hold timeout         30s
  hold valid           10s
  hold obsolete        30s
```
