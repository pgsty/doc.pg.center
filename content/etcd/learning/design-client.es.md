---
title: "Diseño del cliente etcd"
weight: 2250
description: "Decisiones arquitectónicas del cliente y sus detalles de implementación"
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-client.md"
---

Diseño del cliente etcd {#etcd-client-design}
===================

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


Introducción {#introduction}
===================

El servidor de etcd ha demostrado su robustez con años de pruebas de inyección de fallos. La mayor parte de la lógica de aplicación compleja ya está gestionada por el servidor de etcd y sus almacenes de datos (por ejemplo, la pertenencia al clúster es transparente para los clientes, con la capa Raft reenviando las propuestas al líder). Aunque los componentes del servidor son correctos, su composición con el cliente requiere un conjunto diferente de protocolos intrincados para garantizar su corrección y alta disponibilidad bajo condiciones con fallos. Idealmente, el servidor de etcd proporciona una vista lógica única de un clúster compuesto por muchas máquinas físicas, y el cliente implementa la conmutación por error automática entre réplicas. Este documento describe las decisiones arquitectónicas del cliente y sus detalles de implementación.


Glosario {#glossary}
===================

*clientv3*: cliente Go oficial de etcd para la API etcd v3.

*clientv3-grpc1.0*: Implementación oficial del cliente, con [`grpc-go v1.0.x`](https://github.com/grpc/grpc-go/releases/tag/v1.0.0), que se usa en la última versión de etcd v3.1.

*clientv3-grpc1.7*: Implementación oficial del cliente, con [`grpc-go v1.7.x`](https://github.com/grpc/grpc-go/releases/tag/v1.7.0), que se usa en las últimas versiones de etcd v3.2 y v3.3.

*clientv3-grpc1.23*: Implementación oficial del cliente, con [`grpc-go v1.23.x`](https://github.com/grpc/grpc-go/releases/tag/v1.23.0), que se usa en la última versión de etcd v3.4.

*Balancer*: el balanceador de carga del cliente de etcd, que implementa el mecanismo de reintento y de conmutación por error. El cliente de etcd debería balancear la carga automáticamente entre múltiples endpoints.

*Endpoints*: una lista de endpoints del servidor de etcd a los que los clientes pueden conectarse. Típicamente, 3 o 5 URLs de cliente de un clúster de etcd.

*Endpoint fijado*: cuando se configura con múltiples endpoints, el balanceador del cliente <= v3.3 elige un solo endpoint para establecer una conexión TCP, con el fin de limitar el número total de conexiones abiertas hacia el clúster de etcd. En la v3.4, el balanceador aplica round-robin a los endpoints fijados en cada solicitud, distribuyendo así la carga de manera más uniforme.

*Conexión de cliente*: conexión TCP que se ha establecido con un servidor de etcd, mediante gRPC Dial.

*Subconexión*: interfaz gRPC SubConn. Cada subconexión contiene una lista de direcciones. El balanceador crea una SubConn a partir de una lista de direcciones resueltas. Una ClientConn de gRPC puede corresponder a múltiples SubConn (por ejemplo, example.com se resuelve en `10.10.10.1` y `10.10.10.2` de dos subconexiones). El balanceador de etcd v3.4 emplea un resolvedor interno para establecer una subconexión por cada endpoint.

*Desconexión transitoria*: cuando el servidor gRPC devuelve un error de estado [`code Unavailable`](https://godoc.org/google.golang.org/grpc/codes#Code).


Requisitos del cliente {#client-requirements}
===================

*Corrección*. Las solicitudes pueden fallar en presencia de fallos del servidor. Sin embargo, nunca se violan las garantías de consistencia: propiedades de ordenamiento global, nunca escribir datos corruptos, semántica de como máximo una vez para las operaciones mutables, la observación nunca percibe eventos parciales, etc.

*Vivacidad*. Los servidores pueden fallar o desconectarse brevemente. Los clientes deberían progresar en cualquiera de los casos. Los clientes [nunca deberían caer en interbloqueo](https://github.com/etcd-io/etcd/issues/8980) esperando que un servidor vuelva a estar en línea, salvo que se configuren para ello. Idealmente, los clientes detectan los servidores no disponibles con pings HTTP/2 y conmutan por error a otros nodos con mensajes de error claros.

*Eficacia*. Los clientes deberían operar con eficacia y con el mínimo de recursos: las conexiones TCP anteriores deberían [cerrarse de forma ordenada](https://github.com/etcd-io/etcd/issues/9212) tras un cambio de endpoint. El mecanismo de conmutación por error debería predecir con eficacia la siguiente réplica a la que conectarse, sin reintentar inútilmente en nodos fallidos.

*Portabilidad*. El cliente oficial debería estar claramente documentado y su implementación debería ser aplicable a otros enlaces de lenguaje. La gestión de errores entre los distintos enlaces de lenguaje debería ser consistente. Dado que etcd está plenamente comprometido con gRPC, la implementación debería alinearse estrechamente con los objetivos de diseño a largo plazo de gRPC (por ejemplo, una política de reintentos conectable debería ser compatible con [gRPC retry](https://github.com/grpc/proposal/blob/master/A6-client-retries.md)). Las actualizaciones entre dos versiones del cliente no deberían ser disruptivas.


Descripción general del cliente {#client-overview}
===================

El cliente de etcd implementa los siguientes componentes:

* un balanceador que establece conexiones gRPC a un clúster de etcd,
* un cliente de API que envía RPC a un servidor de etcd, y
* un gestor de errores que decide si reintentar una solicitud fallida o cambiar de endpoint.

Los lenguajes pueden diferir en cómo establecer una conexión inicial (por ejemplo, configurar TLS), en cómo codificar y enviar mensajes Protocol Buffer al servidor, en cómo gestionar los RPC de flujo, etc. Sin embargo, los errores devueltos por el servidor de etcd serán los mismos. La gestión de errores y la política de reintentos también deberían serlo.

Por ejemplo, el servidor de etcd puede devolver `"rpc error: code = Unavailable desc = etcdserver: request timed out"`, que es un error transitorio que admite reintentos. O devolver `rpc error: code = InvalidArgument desc = etcdserver: key is not provided`, lo que significa que la solicitud era inválida y no debe reintentarse. El cliente Go puede analizar los errores con `google.golang.org/grpc/status.FromError`, y el cliente Java con `io.grpc.Status.fromThrowable`.


clientv3-grpc1.0: Descripción general del balanceador {#clientv3-grpc10-balancer-overview}
-----------------------------------

`clientv3-grpc1.0` mantiene múltiples conexiones TCP cuando se configura con múltiples endpoints de etcd. Luego elige una dirección y la usa para enviar todas las solicitudes del cliente. La dirección fijada se mantiene hasta que se cierra el objeto cliente (ver *Figura 1*). Cuando el cliente recibe un error, elige otra al azar y reintenta.

![client-balancer-figure-01.png](/etcd/learning/img/client-balancer-figure-01.png)


clientv3-grpc1.0: Limitación del balanceador {#clientv3-grpc10-balancer-limitation}
-------------------------------------

Que `clientv3-grpc1.0` abra múltiples conexiones TCP puede proporcionar una conmutación por error del balanceador más rápida, pero requiere más recursos. El balanceador no comprende el estado de salud de los nodos ni la pertenencia al clúster. Por eso es posible que el balanceador quede atascado con un nodo fallido o particionado.


clientv3-grpc1.7: Descripción general del balanceador {#clientv3-grpc17-balancer-overview}
------------------------------------

`clientv3-grpc1.7` mantiene una sola conexión TCP con un servidor de etcd elegido. Cuando se le dan múltiples endpoints del clúster, un cliente primero intenta conectarse a todos. En cuanto una conexión está activa, el balanceador fija la dirección y cierra las demás (ver *Figura 2*). La dirección fijada debe mantenerse hasta que se cierre el objeto cliente. Un error, proveniente de un fallo del servidor o de la red del cliente, se envía al gestor de errores del cliente (ver *Figura 3*).

![client-balancer-figure-02.png](/etcd/learning/img/client-balancer-figure-02.png)

![client-balancer-figure-03.png](/etcd/learning/img/client-balancer-figure-03.png)

El gestor de errores del cliente toma un error del servidor gRPC y decide si reintentar en el mismo endpoint o cambiar a otras direcciones, según el código y el mensaje de error (ver *Figura 4* y *Figura 5*).

![client-balancer-figure-04.png](/etcd/learning/img/client-balancer-figure-04.png)

![client-balancer-figure-05.png](/etcd/learning/img/client-balancer-figure-05.png)

Los RPC de flujo, como Watch y KeepAlive, a menudo se solicitan sin tiempos de espera. En su lugar, el cliente puede enviar pings HTTP/2 periódicos para comprobar el estado de un endpoint fijado; si el servidor no responde al ping, el balanceador cambia a otros endpoints (ver *Figura 6*).

![client-balancer-figure-06.png](/etcd/learning/img/client-balancer-figure-06.png)


clientv3-grpc1.7: Limitación del balanceador {#clientv3-grpc17-balancer-limitation}
-------------------------------------

El balanceador de `clientv3-grpc1.7` envía keepalives HTTP/2 para detectar desconexiones en las solicitudes de streaming. Se trata de un mecanismo simple de ping al servidor gRPC que no razona sobre la pertenencia al clúster, por lo que no puede detectar particiones de red. Como un servidor gRPC particionado todavía puede responder a los pings del cliente, el balanceador puede quedar atascado con un nodo particionado. Idealmente, el ping de keepalive detecta la partición y activa el cambio de endpoint antes del tiempo de espera de la solicitud (ver [etcd#8673](https://github.com/etcd-io/etcd/issues/8673) y *Figura 7*).

![client-balancer-figure-07.png](/etcd/learning/img/client-balancer-figure-07.png)

El balanceador de `clientv3-grpc1.7` mantiene una lista de endpoints en mal estado. Las direcciones desconectadas se añaden a la lista de «en mal estado» y se consideran no disponibles hasta pasado el tiempo de espera, que está codificado de forma fija como el tiempo de espera de conexión (dial timeout), con el valor por defecto de 5 segundos. El balanceador puede dar falsos positivos sobre qué endpoints están en mal estado. Por ejemplo, el endpoint A puede volver justo después de ser incluido en la lista negra, pero seguir inutilizable durante los 5 segundos siguientes (ver *Figura 8*).

`clientv3-grpc1.0` sufría los mismos problemas descritos anteriormente.

![client-balancer-figure-08.png](/etcd/learning/img/client-balancer-figure-08.png)

El gRPC Go upstream ya había migrado a la nueva interfaz del balanceador. Por ejemplo, la implementación del balanceador subyacente de `clientv3-grpc1.7` usa el nuevo balanceador de gRPC e intenta mantener la consistencia con los comportamientos del balanceador antiguo. Aunque su compatibilidad se ha mantenido razonablemente bien, el cliente de etcd [siguió sufriendo cambios sutiles de ruptura](https://github.com/grpc/grpc-go/issues/1649). Además, el mantenedor de gRPC recomienda [no depender de la interfaz antigua del balanceador](https://github.com/grpc/grpc-go/issues/1942#issuecomment-375368665). En general, para obtener mejor soporte del upstream, lo mejor es mantenerse sincronizado con las versiones más recientes de gRPC. Y las características nuevas, como la política de reintentos, podrían no retroportarse a la rama gRPC 1.7. Por lo tanto, tanto el servidor como el cliente de etcd deben migrar a las versiones más recientes de gRPC.


clientv3-grpc1.23: Descripción general del balanceador {#clientv3-grpc123-balancer-overview}
------------------------------------

`clientv3-grpc1.7` está tan estrechamente acoplado a la interfaz antigua de gRPC que cada actualización de una dependencia de gRPC rompía el comportamiento del cliente. La mayor parte de los esfuerzos de desarrollo y depuración se dedicaron a corregir esos cambios de comportamiento del cliente. Como resultado, su implementación se ha vuelto excesivamente complicada, con suposiciones erróneas sobre las conectividades del servidor.

El objetivo principal de `clientv3-grpc1.23` es simplificar la lógica de conmutación por error del balanceador; en lugar de mantener una lista de endpoints en mal estado, que puede estar obsoleta, simplemente avanza en round-robin al siguiente endpoint siempre que el cliente se desconecta del endpoint actual. No asume el estado de los endpoints. Por lo tanto, ya no se necesita un seguimiento de estado complicado (ver *Figura 8* y anteriores). La actualización a `clientv3-grpc1.23` no debería suponer ningún problema; todos los cambios fueron internos, conservando toda la compatibilidad con versiones anteriores.

Internamente, cuando se le dan múltiples endpoints, `clientv3-grpc1.23` crea múltiples subconexiones (una subconexión por cada endpoint), mientras que `clientv3-grpc1.7` crea una sola conexión a un endpoint fijado (ver *Figura 9*). Por ejemplo, en un clúster de 5 nodos, el balanceador de `clientv3-grpc1.23` requeriría 5 conexiones TCP, mientras que `clientv3-grpc1.7` solo requiere una. Al conservar el conjunto de conexiones TCP, `clientv3-grpc1.23` puede consumir más recursos, pero proporciona un balanceador de carga más flexible con mejor rendimiento de conmutación por error. La política de balanceo por defecto es round robin, pero puede ampliarse fácilmente para admitir otros tipos de balanceadores (por ejemplo, power of two, elegir el líder, etc.). `clientv3-grpc1.23` usa el grupo de resolutores de gRPC (resolver group) e implementa la política de selección del balanceador (picker), para delegar el trabajo complejo de balanceo al gRPC upstream. Por otro lado, `clientv3-grpc1.7` gestiona manualmente cada conexión gRPC y la conmutación por error del balanceador, lo que complica la implementación. `clientv3-grpc1.23` implementa el reintento en la cadena de interceptores de gRPC, que gestiona automáticamente los errores internos de gRPC y permite políticas de reintento más avanzadas como el backoff, mientras que `clientv3-grpc1.7` interpreta manualmente los errores de gRPC para los reintentos.

![client-balancer-figure-09.png](/etcd/learning/img/client-balancer-figure-09.png)


clientv3-grpc1.23: Limitación del balanceador {#clientv3-grpc123-balancer-limitation}
--------------------------------------

Pueden hacerse mejoras almacenando en caché el estado de cada endpoint. Por ejemplo, el balanceador puede hacer ping a cada servidor por adelantado para mantener una lista de candidatos sanos y usar esta información al hacer el round-robin. O, al desconectarse, el balanceador puede dar prioridad a los endpoints sanos. Esto puede complicar la implementación del balanceador, por lo que puede abordarse en versiones posteriores.

El ping de keepalive del lado del cliente todavía no razona sobre las particiones de red. Una solicitud de streaming puede quedar atascada con un nodo particionado. Hay que implementar un servicio avanzado de comprobación de salud para comprender la pertenencia al clúster (ver [etcd#8673](https://github.com/etcd-io/etcd/issues/8673) para más detalles).

![client-balancer-figure-07.png](/etcd/learning/img/client-balancer-figure-07.png)

Actualmente, la lógica de reintento se gestiona manualmente como un interceptor. Esto podría simplificarse mediante los [reintentos oficiales de gRPC](https://github.com/grpc/proposal/blob/master/A6-client-retries.md).
