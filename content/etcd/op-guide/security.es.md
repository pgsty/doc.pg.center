---
title: Modelo de seguridad del transporte
weight: 4125
description: Protección de los datos en tránsito
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/security.md"
---

etcd admite TLS automático, así como autenticación mediante certificados de cliente, tanto para la comunicación de clientes con el servidor como para la comunicación entre pares (servidor a servidor / clúster). **Ten en cuenta que etcd no activa por defecto la [autenticación basada en RBAC][auth] ni la funcionalidad de autenticación en la capa de transporte, para reducir la fricción de los usuarios que empiezan con la base de datos. Además, cambiar este valor por defecto sería un cambio incompatible para el proyecto, establecido desde 2013. Un clúster de etcd que no active las funcionalidades de seguridad puede exponer sus datos a cualquier cliente.**

Para empezar a funcionar, ten primero un certificado de CA y un par de claves firmado para un miembro. Se recomienda crear y firmar un par de claves nuevo para cada miembro de un clúster.

Para mayor comodidad, la herramienta [cfssl] ofrece una interfaz sencilla para la generación de certificados, y proporcionamos un ejemplo de uso de la herramienta [aquí][tls-setup]. Alternativamente, prueba esta [guía para generar pares de claves autofirmados][tls-guide].

La lista de indicadores que se proporciona a continuación puede no estar actualizada debido a los cambios de desarrollo en curso. Para consultar los indicadores disponibles más recientes, ejecuta `etcd --help` o consulta la [ayuda de etcd][etcd help].

## Configuración básica {#basic-setup}

etcd acepta varias opciones de configuración relacionadas con certificados, ya sea mediante indicadores de línea de comandos o variables de entorno:

**Comunicación cliente-servidor:**

`--cert-file=<path>`: Certificado usado para las conexiones SSL/TLS **hacia** etcd. Cuando se establece esta opción, advertise-client-urls puede usar el esquema HTTPS.

`--key-file=<path>`: Clave del certificado. Debe estar sin cifrar.

`--client-cert-auth`: Cuando se establece, etcd comprobará que todas las solicitudes HTTPS entrantes incluyan un certificado de cliente firmado por la CA de confianza; las solicitudes que no suministren un certificado de cliente válido fallarán. Si la [autenticación][auth] está activada, el certificado proporciona las credenciales del nombre de usuario indicado por el campo Common Name.

`--trusted-ca-file=<path>`: Autoridad de certificación de confianza.

`--auto-tls`: Usa certificados autofirmados generados automáticamente para las conexiones TLS con clientes.

**Comunicación entre pares (servidor a servidor / clúster):**

Las opciones de par funcionan igual que las opciones cliente-servidor:

`--peer-cert-file=<path>`: Certificado usado para las conexiones SSL/TLS entre pares. Se usará tanto para escuchar en la dirección de par como para enviar solicitudes a otros pares.

`--peer-key-file=<path>`: Clave del certificado. Debe estar sin cifrar.

`--peer-client-cert-auth`: Cuando se establece, etcd comprobará que todas las solicitudes de par entrantes del clúster incluyan certificados de cliente válidos firmados por la CA suministrada.

`--peer-trusted-ca-file=<path>`: Autoridad de certificación de confianza.

`--peer-auto-tls`: Usa certificados autofirmados generados automáticamente para las conexiones TLS entre pares.

Si se suministra un certificado cliente-servidor o de par, la clave también debe establecerse. Todas estas opciones de configuración también están disponibles mediante las variables de entorno, `ETCD_TRUSTED_CA_FILE`, `ETCD_PEER_TRUSTED_CA_FILE`, etc.

**Opciones comunes:**

`--cipher-suites`: Lista separada por comas de los conjuntos de cifrado TLS admitidos entre servidor/cliente y pares (si está vacía, la rellena Go automáticamente).

`--tls-min-version=<version>` Establece la versión mínima de TLS admitida por etcd.

`--tls-max-version=<version>` Establece la versión máxima de TLS admitida por etcd. Si no se establece, se usará la versión máxima admitida por Go.

### keyUsage y extendedKeyUsage del certificado TLS {#tls-certificate-keyusage-and-extendedkeyusage}

Al generar certificados X.509 para proteger el transporte de etcd,
los certificados deben incluir los campos `keyUsage` y
`extendedKeyUsage` apropiados según su rol. etcd se apoya en las
bibliotecas `crypto/tls` y `crypto/x509` de Go para la verificación de certificados,
que hacen cumplir estos usos durante el handshake TLS.

La siguiente tabla resume los usos recomendados para los roles de certificado habituales:

| Rol del certificado | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| Servidor (cliente-servidor) | digitalSignature, keyEncipherment | serverAuth |
| Cliente | digitalSignature, keyEncipherment | clientAuth |
| Par (servidor-servidor) | digitalSignature, keyEncipherment | serverAuth, clientAuth |

Notas:

- Cuando `--peer-client-cert-auth` está activado, los certificados de par se
  usan para TLS mutuo entre los miembros de etcd y, por lo tanto, requieren tanto
  `serverAuth` como `clientAuth`.
- Los certificados de cliente usados con `--client-cert-auth` deben incluir
  `clientAuth`.

## Ejemplo 1: Seguridad del transporte cliente-servidor con HTTPS {#example-1-client-to-server-transport-security-with-https}

Para ello, ten listos un certificado de CA (`ca.crt`) y un par de claves firmado (`server.crt`, `server.key`).

Configuremos etcd para proporcionar una seguridad de transporte HTTPS sencilla paso a paso:

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

Esto debería arrancar sin problemas y será posible probar la configuración hablando HTTPS con etcd:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

El comando debería mostrar que el handshake tuvo éxito. Dado que usamos certificados autofirmados con nuestra propia autoridad de certificación, hay que pasarle la CA a curl usando la opción `--cacert`. Otra posibilidad sería añadir el certificado de la CA al directorio de certificados de confianza del sistema (normalmente en `/etc/pki/tls/certs` o `/etc/ssl/certs`).

**Usuarios de OSX 10.9+**: curl 7.30.0 en OSX 10.9+ no entiende los certificados pasados por la línea de comandos.
En su lugar, importa el ca.crt de prueba directamente en el llavero o añade el indicador `-k` a curl para ignorar los errores.
Para probar sin el indicador `-k`, ejecuta `open ./tests/fixtures/ca/ca.crt` y sigue las indicaciones.
¡Elimina este certificado después de las pruebas!
Si conoces una solución alternativa, háznoslo saber.

## Ejemplo 2: Autenticación cliente-servidor con certificados de cliente HTTPS {#example-2-client-to-server-authentication-with-https-client-certificates}

Hasta ahora hemos dado al cliente de etcd la capacidad de verificar la identidad del servidor y proporcionar seguridad de transporte. Sin embargo, también podemos usar certificados de cliente para evitar el acceso no autorizado a etcd.

Los clientes proporcionarán sus certificados al servidor y el servidor comprobará si el certificado está firmado por la CA suministrada y decidirá si atiende la solicitud.

Para esto se necesitan los mismos archivos mencionados en el primer ejemplo, así como un par de claves para el cliente (`client.crt`, `client.key`) firmado por la misma autoridad de certificación.

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

Ahora prueba la misma solicitud de antes contra este servidor:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

El servidor debería rechazar la solicitud:

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

Para que tenga éxito, debemos entregar al servidor el certificado de cliente firmado por la CA:

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

La salida debería incluir:

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

Y también la respuesta del servidor:

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

Especifica conjuntos de cifrado para bloquear los [conjuntos de cifrado TLS débiles](https://github.com/etcd-io/etcd/issues/8320).

El handshake TLS fallaría cuando el client hello se solicite con conjuntos de cifrado no válidos.

Por ejemplo:

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

Luego, las solicitudes del cliente deben especificar uno de los conjuntos de cifrado especificados en el servidor:

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## Ejemplo 3: Seguridad del transporte y certificados de cliente en un clúster {#example-3-transport-security--client-certificates-in-a-cluster}

etcd admite el mismo modelo que el anterior para la **comunicación entre pares**, es decir, la comunicación entre los miembros de etcd en un clúster.

Suponiendo que tenemos nuestro `ca.crt` y dos miembros con sus propios pares de claves (`member1.crt` & `member1.key`, `member2.crt` & `member2.key`) firmados por esta CA, lanzamos etcd de la siguiente manera:


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Los miembros de etcd formarán un clúster y toda la comunicación entre los miembros del clúster se cifrará y autenticará usando los certificados de cliente. La salida de etcd mostrará que las direcciones a las que se conecta usan HTTPS.

## Ejemplo 4: Seguridad de transporte autofirmada automática {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> Cuando especificas ClientAutoTLS y PeerAutoTLS, el periodo de validez del certificado de cliente y del certificado de par generados automáticamente por etcd es de solo 1 año. Puedes especificar el indicador --self-signed-cert-validity para establecer el periodo de validez del certificado en años.

Para los casos en que se necesita cifrado de la comunicación, pero no autenticación, etcd admite cifrar sus mensajes con certificados autofirmados generados automáticamente. Esto simplifica el despliegue porque no hay necesidad de gestionar certificados y claves fuera de etcd.
Configura etcd para que use certificados autofirmados para las conexiones de cliente y de par con los indicadores `--auto-tls` y `--peer-auto-tls`:

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

Los certificados autofirmados no autentican la identidad, así que curl devolverá un error:

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

Para desactivar la comprobación de la cadena de certificados, invoca curl con el indicador `-k`:

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## Notas para DNS SRV {#notes-for-dns-srv}

Desde v3.1.0 (excepto v3.2.9), el arranque mediante descubrimiento SRV autentica el `ServerName` con un nombre de dominio raíz procedente del indicador `--discovery-srv`. Esto evita ataques de certificado de hombre en el medio (man-in-the-middle), al exigir que un certificado tenga un nombre de dominio raíz coincidente en su campo Subject Alternative Name (SAN). Por ejemplo, `etcd --discovery-srv=etcd.local` solo autenticará pares/clientes cuando los certificados proporcionados tengan el dominio raíz `etcd.local` como entrada en el campo Subject Alternative Name (SAN)

## Notas para el proxy de etcd {#notes-for-etcd-proxy}

> [!NOTE]
> Esta sección describe el proxy histórico de v2, que ha sido eliminado. Para etcd 3.7, usa el [proxy gRPC v3](/es/etcd/op-guide/grpc_proxy/).

El proxy de etcd termina el TLS de su cliente si la conexión es segura, y usa su propia clave/certificado especificados en `--peer-key-file` y `--peer-cert-file` para comunicarse con los miembros de etcd.

El proxy se comunica con los miembros de etcd a través tanto de las `--advertise-client-urls` como de las `--advertise-peer-urls` de un miembro dado. Reenvía las solicitudes de los clientes a las URLs de cliente anunciadas de los miembros de etcd y sincroniza la configuración inicial del clúster a través de las URLs de par anunciadas de los miembros de etcd.

Cuando la autenticación de cliente está activada para un miembro de etcd, el administrador debe asegurarse de que el certificado de par especificado en la opción `--peer-cert-file` del proxy es válido para esa autenticación. El certificado de par del proxy también debe ser válido para la autenticación de pares si la autenticación de pares está activada.

## Notas para la autenticación TLS {#notes-for-tls-authentication}

Desde [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [los certificados TLS se recargan en cada conexión de cliente](https://github.com/etcd-io/etcd/pull/7829). Esto es útil para reemplazar certificados caducados sin detener los servidores de etcd; puede hacerse sobrescribiendo los certificados antiguos con otros nuevos. Refrescar los certificados en cada conexión no debería suponer demasiada sobrecarga, pero puede mejorarse en el futuro con una capa de caché. Se pueden encontrar pruebas de ejemplo [aquí](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757).

Desde [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [el servidor rechaza los certificados de pares entrantes con una `SAN` de IP incorrecta](https://github.com/etcd-io/etcd/pull/7687). Por ejemplo, si el certificado de par contiene direcciones IP en el campo Subject Alternative Name (SAN), el servidor autentica un par solo cuando la dirección IP remota coincide con una de esas direcciones IP. Esto evita que puntos de conexión no autorizados se unan al clúster. Por ejemplo, la CSR del par B (con `cfssl`) es:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

cuando la dirección IP real del par B es `10.138.0.2`, no `10.138.0.27`. Cuando el par B intenta unirse al clúster, el par A rechazará a B con el error `x509: certificate is valid for 10.138.0.27, not 10.138.0.2`, porque la dirección IP remota de B no coincide con la del campo Subject Alternative Name (SAN).

Desde [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09), [el servidor resuelve los `DNSNames` del TLS al comprobar la `SAN`](https://github.com/etcd-io/etcd/pull/7767). Por ejemplo, si el certificado de par contiene solo nombres DNS (sin direcciones IP) en el campo Subject Alternative Name (SAN), el servidor autentica un par solo cuando las resoluciones directas (`dig b.com`) de esos nombres DNS tienen una IP coincidente con la dirección IP remota. Por ejemplo, la CSR del par B (con `cfssl`) es:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

cuando la dirección IP remota del par B es `10.138.0.2`. Cuando el par B intenta unirse al clúster, el par A resuelve el host entrante `b.com` para obtener la lista de direcciones IP (p. ej. `dig b.com`). Y rechaza a B si la lista no contiene la IP `10.138.0.2`, con el error `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`.

Desde [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07), [el servidor acepta las conexiones si la IP coincide, sin comprobar las entradas DNS](https://github.com/etcd-io/etcd/pull/8223). Por ejemplo, si el certificado de par contiene direcciones IP y nombres DNS en el campo Subject Alternative Name (SAN), y la dirección IP remota coincide con una de esas direcciones IP, el servidor simplemente acepta la conexión sin comprobar más los nombres DNS. Por ejemplo, la CSR del par B (con `cfssl`) es:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

cuando la dirección IP remota del par B es `10.138.0.2` e `invalid.domain` es un host no válido. Cuando el par B intenta unirse al clúster, el par A autentica a B con éxito, ya que el campo Subject Alternative Name (SAN) tiene una dirección IP válida coincidente. Consulta [issue#8206](https://github.com/etcd-io/etcd/issues/8206) para más detalles.

Desde [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04), [el servidor admite la resolución inversa en `SAN` DNS con comodines](https://github.com/etcd-io/etcd/pull/8281). Por ejemplo, si el certificado de par contiene solo nombres DNS (sin direcciones IP) en el campo Subject Alternative Name (SAN), el servidor primero hace una resolución inversa de la dirección IP remota para obtener una lista de nombres que se corresponden con esa dirección (p. ej. `nslookup IPADDR`). Luego acepta la conexión si esos nombres incluyen uno que coincida con los nombres DNS del certificado de par (ya sea por coincidencia exacta o con comodines). Si ninguno coincide, el servidor hace una resolución directa de cada entrada DNS del certificado de par (p. ej. resuelve `example.default.svc` cuando la entrada es `*.example.default.svc`), y acepta la conexión solo cuando las direcciones resueltas del host tienen la dirección IP coincidente con la dirección IP remota del par. Por ejemplo, la CSR del par B (con `cfssl`) es:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

cuando la dirección IP remota del par B es `10.138.0.2`. Cuando el par B intenta unirse al clúster, el par A hace una resolución inversa de la IP `10.138.0.2` para obtener la lista de nombres de host. Y hace coincidir los nombres de host, de forma exacta o con comodines, con los nombres DNS del certificado del par B en el campo Subject Alternative Name (SAN). Si ni la resolución inversa ni la directa funcionaron, devuelve un error `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]`. Consulta [issue#8268](https://github.com/etcd-io/etcd/issues/8268) para más detalles.

[v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) añade el indicador [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616) para admitir la [autenticación basada en CN (Common Name) para las conexiones entre pares](https://github.com/etcd-io/etcd/issues/8262). El arranque TLS de Kubernetes implica generar certificados dinámicos para los miembros de etcd y otros componentes del sistema (p. ej. servidor de API, kubelet, etc.). Mantener CA distintas para cada componente proporciona un control de acceso más estricto al clúster de etcd, pero a menudo resulta tedioso. Cuando se especifica el indicador --peer-cert-allowed-cn, un nodo solo puede unirse con un nombre común coincidente, incluso con CA compartidas. La coincidencia es una comparación exacta de cadenas contra el campo Common Name (CN) del certificado; no se admiten comodines ni coincidencias por prefijo. Para el filtrado basado en nombres de host mediante --peer-cert-allowed-hostname o --client-cert-allowed-hostname, la coincidencia usa la función x509.Certificate.VerifyHostname() de Go, que admite tanto nombres de host exactos como entradas con comodines (p. ej. *.example.com). Por ejemplo, cada miembro de un clúster de 3 nodos se configura con las siguientes CSRs (con cfssl):




```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

Luego, solo los pares con nombres comunes coincidentes serán autenticados si se proporciona `--peer-cert-allowed-cn etcd.local`. Y los nodos con CN diferentes en las CSRs o con un `--peer-cert-allowed-cn` diferente serán rechazados:

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

Cada proceso debe iniciarse con:

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

[v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) y [v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) corrigen la recarga de TLS cuando [el campo SAN del certificado incluye solo direcciones IP pero ningún nombre de dominio](https://github.com/etcd-io/etcd/issues/9541). Por ejemplo, un miembro se configura con las siguientes CSRs (con `cfssl`):

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

En Go, el servidor llama a `(*tls.Config).GetCertificate` para recargar el TLS si y solo si el campo `(*tls.Config).Certificates` del servidor está vacío, o `(*tls.ClientHelloInfo).ServerName` no está vacío con un SNI válido del cliente. Anteriormente, etcd siempre rellenaba `(*tls.Config).Certificates` en el handshake TLS inicial del cliente, como no vacío. Por ello, siempre se esperaba que el cliente suministrara un SNI coincidente para pasar la verificación TLS y activar `(*tls.Config).GetCertificate` para recargar los recursos TLS.

Sin embargo, un certificado cuyo campo SAN [no incluye ningún nombre de dominio sino solo direcciones IP](https://github.com/etcd-io/etcd/issues/9541) solicitaría un `*tls.ClientHelloInfo` con el campo `ServerName` vacío, fallando así el disparo de la recarga TLS en el handshake TLS inicial; esto se convierte en un problema cuando hay que reemplazar certificados caducados en caliente.

Ahora, `(*tls.Config).Certificates` se crea vacío en el handshake TLS inicial del cliente, primero para disparar `(*tls.Config).GetCertificate`, y luego para rellenar el resto de los certificados en cada nueva conexión TLS, incluso cuando el SNI del cliente está vacío (p. ej. el certificado solo incluye IPs).

## Notas para la lista blanca de hosts {#notes-for-host-whitelist}

El indicador `etcd --host-whitelist` especifica los nombres de host aceptables de las solicitudes HTTP de los clientes. La política de origen del cliente protege contra ataques de [«DNS Rebinding»](https://en.wikipedia.org/wiki/DNS_rebinding) a servidores etcd no seguros. Es decir, cualquier sitio web puede simplemente crear un nombre DNS autorizado y dirigir el DNS a `"localhost"` (o cualquier otra dirección). Entonces, todos los puntos de conexión HTTP del servidor etcd que escuchan en `"localhost"` se vuelven accesibles, quedando así vulnerables a ataques de DNS rebinding. Consulta [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2) para más detalles.

La política de origen del cliente funciona así:

1. Si la conexión del cliente es segura mediante HTTPS, se permiten todos los nombres de host.
2. Si la conexión del cliente no es segura y `"HostWhitelist"` no está vacía, solo se permiten las solicitudes HTTP cuyo campo Host figure en la lista blanca.

Ten en cuenta que la política de origen del cliente se aplica esté o no activada la autenticación, para lograr controles más estrictos.

Por defecto, `etcd --host-whitelist` y `embed.Config.HostWhitelist` usan `*` para permitir todos los nombres de host. Una lista blanca vacía también permite todos los nombres de host. Ten en cuenta que, al especificar nombres de host, las direcciones de loopback no se añaden automáticamente. Para permitir las interfaces de loopback, añádelas manualmente a la lista blanca (p. ej. `"localhost"`, `"127.0.0.1"`, etc.).

## Preguntas frecuentes {#frequently-asked-questions}

### ¿Veo una alerta SSLv3 de fallo del handshake al usar la autenticación de cliente TLS? {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

El paquete `crypto/tls` de `golang` comprueba el uso de la clave pública del certificado antes de usarla.
Para usar la clave pública del certificado para la autenticación de cliente, hay que añadir `clientAuth` a `Extended Key Usage` al crear la clave pública del certificado.

Aquí se explica cómo hacerlo:

Añade la siguiente sección a openssl.cnf:

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

Al crear el certificado, asegúrate de referenciarlo en el indicador `-extensions`:

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### Con la autenticación de certificado de par recibo «certificate is valid for 127.0.0.1, not $MY_IP» {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
Asegúrate de firmar los certificados con un Subject Name que contenga la dirección IP pública del miembro. La herramienta `etcd-ca`, por ejemplo, proporciona una opción `--ip=` para su comando `new-cert`.

El certificado debe firmarse para el FQDN del miembro en su Subject Name; usa Subject Alternative Names (abreviadas como IP SANs) para añadir la dirección IP. La herramienta `etcd-ca` proporciona la opción `--domain=` para su comando `new-cert`, y openssl también puede [hacerlo][alt-name].

### ¿Cifra etcd los datos almacenados en las unidades de disco? {#does-etcd-encrypt-data-stored-on-disk-drives}
No. etcd no cifra los datos clave/valor almacenados en las unidades de disco. Si un usuario necesita cifrar los datos almacenados en etcd, hay algunas opciones:
* Dejar que las aplicaciones cliente cifren y descifren los datos
* Usar una funcionalidad del sistema de almacenamiento subyacente para cifrar los datos almacenados, como [dm-crypt]

### Veo una advertencia en el registro que dice «directory X exist without recommended permission -rwx------» {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
Cuando etcd crea ciertos directorios nuevos, establece el permiso de los archivos en 700 para evitar en lo posible el acceso sin privilegios. Sin embargo, si el usuario ya ha creado un directorio con sus propias preferencias, etcd usa el directorio existente y registra un mensaje de advertencia si el permiso es distinto de 700.

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /es/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
