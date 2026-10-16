---
title: Guía de creación de clústeres
weight: 4150
description: "Arranque de un clúster etcd: método estático, descubrimiento de etcd y descubrimiento DNS"
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/clustering.md"
---

## Visión general {#overview}

Iniciar un clúster etcd de forma estática requiere que cada miembro conozca a otro miembro del clúster. En muchos casos, las IP de los miembros del clúster pueden desconocerse de antemano. En estos casos, el clúster etcd puede arrancarse con la ayuda de un servicio de descubrimiento.

Una vez que un clúster etcd está en funcionamiento, la adición o eliminación de miembros se realiza mediante la [reconfiguración en tiempo de ejecución][runtime-conf]. Para comprender mejor el diseño que hay detrás de la reconfiguración en tiempo de ejecución, sugerimos leer [el documento de diseño de la configuración en tiempo de ejecución][runtime-reconf-design].

Esta guía cubrirá los siguientes mecanismos para arrancar un clúster etcd:

* [Estático](#static)
* [Descubrimiento de etcd](#etcd-discovery)
* [Descubrimiento DNS](#dns-discovery)

Cada uno de los mecanismos de arranque se usará para crear un clúster etcd de tres máquinas con los siguientes detalles:

|Nombre|Dirección|Nombre de host|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## Estático {#static}

Como conocemos los miembros del clúster, sus direcciones y el tamaño del clúster antes de empezar, podemos usar una configuración de arranque sin conexión definiendo la opción `initial-cluster`. Cada máquina recibirá las siguientes variables de entorno o la siguiente línea de comandos:

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

Ten en cuenta que las URL especificadas en `initial-cluster` son las _URL de peer anunciadas_, es decir, deben coincidir con el valor de `initial-advertise-peer-urls` en los nodos respectivos.

Si se inician varios clústeres (o se crea y destruye un único clúster) con la misma configuración con fines de prueba, es muy recomendable que cada clúster reciba un `initial-cluster-token` único. Al hacer esto, etcd puede generar ID de clúster y de miembro únicos para los clústeres incluso si por lo demás tienen exactamente la misma configuración. Esto puede proteger a etcd de las interacciones entre clústeres, que podrían corromperlos.

etcd escucha en [`listen-client-urls`][conf-listen-client] para aceptar el tráfico de clientes. El miembro de etcd anuncia las URL especificadas en [`advertise-client-urls`][conf-adv-client] a los demás miembros, proxies y clientes. Asegúrate de que las `advertise-client-urls` sean accesibles desde los clientes previstos. Un error común es definir `advertise-client-urls` como localhost o dejar el valor por defecto cuando los clientes remotos deben alcanzar etcd.

En cada máquina, inicia etcd con estas opciones:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

Los parámetros de línea de comandos que empiezan por `--initial-cluster` se ignorarán en ejecuciones posteriores de etcd. Puedes eliminar las variables de entorno o las opciones de línea de comandos después del proceso de arranque inicial. Si la configuración necesita cambios más adelante (por ejemplo, añadir o eliminar miembros del clúster), consulta la guía de [configuración en tiempo de ejecución][runtime-conf].

### TLS {#tls}

etcd admite la comunicación cifrada mediante el protocolo TLS. Los canales TLS pueden usarse tanto para la comunicación interna cifrada del clúster entre pares como para el tráfico de clientes cifrado. Esta sección proporciona ejemplos para configurar un clúster con TLS para pares y clientes. Puede encontrarse información adicional que detalla la compatibilidad de etcd con TLS en la [guía de seguridad][security-guide].

#### Certificados autofirmados {#self-signed-certificates}

Un clúster que usa certificados autofirmados cifra el tráfico y autentica sus conexiones. Para iniciar un clúster con certificados autofirmados, cada miembro del clúster debe tener un par de claves único (`member.crt`, `member.key`) firmado por un certificado CA compartido del clúster (`ca.crt`), tanto para las conexiones entre pares como para las conexiones de clientes. Los certificados pueden generarse siguiendo el ejemplo de [configuración de TLS][tls-setup] de etcd.

En cada máquina, etcd se iniciaría con estas opciones:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### Certificados automáticos {#automatic-certificates}

Si el clúster necesita comunicación cifrada pero no requiere conexiones autenticadas, etcd puede configurarse para generar sus claves automáticamente. Durante la inicialización, cada miembro crea su propio conjunto de claves basándose en sus direcciones IP y hosts anunciados.

En cada máquina, etcd se iniciaría con estas opciones:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### Casos de error {#error-cases}

En el siguiente ejemplo, no hemos incluido nuestro nuevo host en la lista de nodos enumerados. Si se trata de un clúster nuevo, el nodo _debe_ añadirse a la lista de miembros iniciales del clúster.

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

En este ejemplo, intentamos asignar un nodo (infra0) a una dirección diferente (127.0.0.1:2380) de su dirección enumerada en la lista del clúster (10.0.1.10:2380). Si este nodo debe escuchar en varias direcciones, todas las direcciones _deben_ reflejarse en la directiva de configuración «initial-cluster».

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

Si un par se configura con un conjunto diferente de argumentos de configuración e intenta unirse a este clúster, etcd informará de un error de coincidencia de ID de clúster y saldrá.

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## Descubrimiento {#discovery}

En muchos casos, es posible que las IP de los pares del clúster no se conozcan de antemano. Esto es habitual cuando se usan proveedores de nube o cuando la red usa DHCP. En estos casos, en lugar de especificar una configuración estática, usa un clúster etcd existente para arrancar uno nuevo. Este proceso se llama «descubrimiento».

Existen dos métodos que pueden usarse para el descubrimiento:

* el servicio de descubrimiento de etcd
* los registros DNS SRV

### Descubrimiento de etcd {#etcd-discovery}

> [!NOTE]
> Los ejemplos del servicio de descubrimiento de esta sección describen el protocolo v2 heredado, que se eliminó en etcd 3.7. Para un clúster nuevo de v3.7, usa el [descubrimiento v3](/es/etcd/dev-internal/discovery_protocol/) o los métodos de arranque estático y por DNS SRV de esta guía.

Para comprender mejor el diseño del protocolo del servicio de descubrimiento, sugerimos leer la [documentación del protocolo del servicio de descubrimiento][discovery-proto].

#### Duración de vida de una URL de descubrimiento {#lifetime-of-a-discovery-url}

Una URL de descubrimiento identifica un clúster etcd único. En lugar de reutilizar una URL de descubrimiento existente, cada instancia de etcd comparte una nueva URL de descubrimiento para arrancar el clúster nuevo.

Además, las URL de descubrimiento deben usarse ÚNICAMENTE para el arranque inicial de un clúster. Para cambiar la composición del clúster cuando ya está en ejecución, consulta la guía de [reconfiguración en tiempo de ejecución][runtime-conf].

#### Servicio de descubrimiento etcd personalizado {#custom-etcd-discovery-service}

El descubrimiento usa un clúster existente para arrancarse. Si se usa un clúster etcd privado, crea una URL así:

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

Al definir la clave size en la URL, se crea una URL de descubrimiento con un tamaño de clúster esperado de 3.

La URL que se usará en este caso será `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` y los miembros de etcd usarán el directorio `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` para registrarse cuando se inicien.

**Cada miembro debe tener especificado un valor diferente para la opción name. `Hostname` o `machine-id` pueden ser una buena elección. De lo contrario, el descubrimiento fallará debido a un nombre duplicado.**

Ahora iniciamos etcd con esas opciones relevantes para cada miembro:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

Esto hará que cada miembro se registre en el servicio de descubrimiento etcd personalizado y que el clúster comience una vez que todas las máquinas se hayan registrado.

#### Servicio de descubrimiento etcd público {#public-etcd-discovery-service}

Si no hay disponible ningún clúster existente, usa el servicio de descubrimiento público alojado en `discovery.etcd.io`.  Para crear una URL de descubrimiento privada usando el endpoint «new», usa el comando:

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Esto creará el clúster con un tamaño inicial de 3 miembros. Si no se especifica ningún tamaño, se usa el valor por defecto de 3.

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**Cada miembro debe tener especificado un valor diferente para la opción name, de lo contrario el descubrimiento fallará debido a nombres duplicados. `Hostname` o `machine-id` pueden ser una buena elección.**

Ahora iniciamos etcd con esas opciones relevantes para cada miembro:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

Esto hará que cada miembro se registre en el servicio de descubrimiento y que el clúster comience una vez que todos los miembros se hayan registrado.

Usa la variable de entorno `ETCD_DISCOVERY_PROXY` para hacer que etcd use un proxy HTTP para conectarse al servicio de descubrimiento.

#### Casos de error y aviso {#error-and-warning-cases}

##### Errores del servidor de descubrimiento {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### Avisos {#warnings}

Se trata de un aviso inofensivo que indica que la URL de descubrimiento se ignorará en esta máquina.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### Descubrimiento DNS {#dns-discovery}

Los [registros SRV][rfc-srv] de DNS pueden usarse como mecanismo de descubrimiento.
La opción `--discovery-srv` puede usarse para definir el nombre de dominio DNS donde se pueden encontrar los registros SRV de descubrimiento.
Al definir `--discovery-srv example.com`, los registros SRV de DNS se buscan en el orden indicado:

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

Si se encuentra `_etcd-server-ssl._tcp.example.com`, etcd intentará realizar el proceso de arranque a través de TLS.

Para ayudar a los clientes a descubrir el clúster etcd, se buscan los siguientes registros SRV de DNS en el orden indicado:

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

Si se encuentra `_etcd-client-ssl._tcp.example.com`, los clientes intentarán comunicarse con el clúster etcd a través de SSL/TLS.

Si etcd usa TLS, el registro SRV de descubrimiento (por ejemplo, `example.com`) debe incluirse en el SAN DNS del certificado SSL junto con el nombre de host, o la formación del clúster fallará con mensajes de registro como el siguiente:

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

Si etcd usa TLS sin una autoridad de certificación personalizada, el dominio de descubrimiento (por ejemplo, example.com) debe coincidir con el dominio del registro SRV (por ejemplo, infra1.example.com). Esto sirve para mitigar los ataques que falsifican registros SRV para apuntar a un dominio diferente; dicho dominio tendría un certificado válido según la PKI, pero estaría controlado por un tercero desconocido.

La opción `-discovery-srv-name` configura además un sufijo para el nombre SRV que se consulta durante el descubrimiento.
Usa esta opción para diferenciar varios clústeres de etcd bajo el mismo dominio.
Por ejemplo, si se definen `discovery-srv=example.com` y `-discovery-srv-name=foo`, se realizan las siguientes consultas DNS SRV:

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### Crear registros DNS SRV {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### Arrancar el clúster etcd usando DNS {#bootstrap-the-etcd-cluster-using-dns}

Los miembros de un clúster etcd pueden anunciar nombres de dominio o direcciones IP; el proceso de arranque resolverá los registros A de DNS.
Desde la versión 3.2 (la 3.1 muestra avisos), `--listen-peer-urls` y `--listen-client-urls` rechazarán los nombres de dominio para el enlace a la interfaz de red.

La dirección resuelta en `--initial-advertise-peer-urls` *debe coincidir* con una de las direcciones resueltas de los objetivos SRV. El miembro de etcd lee la dirección resuelta para averiguar si pertenece al clúster definido en los registros SRV.

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

El clúster también puede arrancar usando direcciones IP en lugar de nombres de dominio:

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

Desde la versión v3.1.0 (excepto la v3.2.9), cuando `etcd --discovery-srv=example.com` se configura con TLS, el servidor solo autenticará a los pares y clientes cuando los certificados proporcionados tengan el dominio raíz `example.com` como entrada en el campo Subject Alternative Name (SAN). Consulta [Notas para DNS SRV][security-guide-dns-srv].

### Puerta de enlace {#gateway}

La puerta de enlace (gateway) de etcd es un proxy TCP simple que reenvía los datos de red al clúster etcd. Lee la [guía de gateway][gateway] para más información.

### Proxy {#proxy}

Las versiones anteriores de etcd admitían un [modo proxy][proxy] exclusivo de v2 mediante `--proxy`. Ese modo se ha eliminado y no puede usarse con etcd 3.7. Para la API v3, usa el [proxy gRPC](/es/etcd/op-guide/grpc_proxy/).

Para los despliegues históricos del proxy v2, consulta el [documento de clustering de la versión 2.3 de etcd][clustering_etcd2].

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /es/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /es/etcd/op-guide/configuration/#member
[discovery-proto]: /es/etcd/dev-internal/discovery_protocol/
[gateway]: /es/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /es/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /es/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /es/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /es/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
