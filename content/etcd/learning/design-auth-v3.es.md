---
title: "Diseño de autenticación de etcd v3"
weight: 2500
description: Autenticación de etcd v3
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-auth-v3.md"
---

## ¿Por qué no reutilizar el sistema de autenticación v2? {#why-not-reuse-the-v2-auth-system}

El protocolo v3 usa gRPC como transporte, en lugar de una interfaz RESTful como la v2. Este nuevo protocolo ofrece la oportunidad de iterar y mejorar el diseño de la v2. Por ejemplo, la autenticación v3 emplea una autenticación basada en la conexión, en lugar de la autenticación por solicitud, más lenta, de la v2. Además, la semántica de la autenticación v2 tiende a ser difícil de manejar en la práctica a la hora de razonar sobre la consistencia, como se describirá en las secciones siguientes. Para la v3 existe una descripción y una implementación bien definidas del mecanismo de autenticación, que corrige las deficiencias del sistema de autenticación v2.

### Requisitos funcionales {#functionality-requirements}

* Autenticación por conexión, no por solicitud
   * Autenticación basada en ID de usuario y contraseña, implementada para la API gRPC
   * La autenticación debe actualizarse después de cambios en la política de autenticación
* Su funcionalidad debería ser tan simple y útil como la de la v2
   * La v3 proporciona un espacio de claves plano, a diferencia de la estructura de directorios de la v2. La comprobación de permisos se proporcionará como coincidencia de intervalos.
* Debería ofrecer garantías de consistencia más fuertes que la autenticación v2

### Cambios principales requeridos {#main-required-changes}

* Un cliente debe crear una conexión dedicada exclusivamente a la autenticación antes de enviar solicitudes autenticadas
* Añadir información de permisos (ID de usuario y revisión autorizada) a los comandos de Raft (`etcdserverpb.InternalRaftRequest`)
* Cada solicitud se comprueba a nivel de permisos en la capa de la máquina de estados, en lugar de en la capa de API

### Consistencia de los metadatos de permisos {#permission-metadata-consistency}

Los metadatos de autenticación también deberían almacenarse y gestionarse en el almacenamiento controlado por el protocolo Raft de etcd, como el resto de los datos guardados en etcd. Esto es necesario para no sacrificar la disponibilidad y la consistencia de todo el clúster de etcd. Si la lectura o la escritura de los metadatos (por ejemplo, la información de permisos) necesitara el acuerdo de todos los nodos (más que un cuórum), la falla de un solo nodo podría detener todo el clúster. Exigir que todos los nodos acuerden a la vez significa que la comprobación de las solicitudes ordinarias de lectura/escritura no puede completarse si cualquier miembro del clúster está caído, incluso aunque el clúster disponga de un cuórum disponible. Este esquema unánime termina degradando la disponibilidad del clúster; el consenso basado en cuórum de raft debería bastar, ya que el acuerdo se deriva de un orden consistente.

El mecanismo de autenticación del protocolo etcd v2 tiene una parte complicada, porque la consistencia de los metadatos debería funcionar como se describió anteriormente, pero no lo hace: cada comprobación de permisos la procesa el miembro de etcd que recibe la solicitud del cliente (server/etcdserver/api/v2http/client.go), incluidos los miembros réplica. Por lo tanto, es posible que la comprobación se base en metadatos obsoletos.


Esta obsolescencia significa que la configuración de autenticación no puede reflejarse tan pronto como los operadores ejecutan etcdctl. Por lo tanto, no hay forma de saber cuánto tiempo permanecen activos los metadatos obsoletos. En la práctica, el cambio de configuración se refleja inmediatamente después de la ejecución del comando. Sin embargo, en algunos casos de carga intensa, el estado inconsistente puede prolongarse y dar lugar a situaciones contraintuitivas para los usuarios y los desarrolladores. Requiere una solución alternativa como [esta](https://github.com/etcd-io/etcd/pull/4317#issuecomment-179037582).

### Los permisos inconsistentes no son seguros para las solicitudes linealizadas {#inconsistent-permissions-are-unsafe-for-linearized-requests}

Un estado de autenticación inconsistente es especialmente grave para las escrituras. Incluso si un operador deshabilita la escritura para un usuario, si la escritura solo se ordena respecto del almacén clave-valor y no del sistema de autenticación, es posible que la escritura se complete con éxito. Sin un ordenamiento tanto en el almacén de autenticación como en el almacén clave-valor, el sistema será susceptible a ataques con permisos obsoletos.

Por consiguiente, la lógica de comprobación de permisos debería añadirse a la máquina de estados de etcd. Cada máquina de estados debería comprobar las solicitudes según su información de permisos en la fase de aplicación (apply) (por lo que la información de autenticación no debe estar obsoleta).

## Diseño e implementación {#design-and-implementation}

### Autenticación {#authentication}

En primer lugar, un cliente debe crear una conexión gRPC únicamente para autenticar su ID de usuario y su contraseña. Un servidor de etcd responderá con una respuesta de autenticación. La respuesta será un token de autenticación en caso de éxito o un error en caso de fallo. El cliente puede usar su token de autenticación para presentar sus credenciales a etcd al hacer solicitudes a la API.

La conexión del cliente usada para solicitar el token de autenticación normalmente se descarta; no puede transportar las credenciales del nuevo token. Esto se debe a que gRPC no ofrece una forma de añadir credenciales por RPC después de crear la conexión (llamando a `grpc.Dial()`). Por lo tanto, un cliente no puede asignar a su conexión un token obtenido a través de esa misma conexión. El cliente necesita una conexión nueva para usar el token.

#### Notas sobre la implementación del RPC `Authenticate()` {#notes-on-the-implementation-of-authenticate-rpc}

El RPC `Authenticate()` genera un token de autenticación a partir de un nombre de usuario y una contraseña dados. etcd guarda y comprueba una contraseña configurada y una contraseña dada usando el paquete `bcrypt` de Go. Por diseño, el mecanismo de comprobación de contraseñas de `bcrypt` es costoso computacionalmente: tarda casi 100ms en un servidor x64 ordinario. Por lo tanto, realizar esta comprobación en la fase de aplicación de la máquina de estados causaría problemas de rendimiento: todo el clúster de etcd solo podría atender casi 10 solicitudes `Authenticate()` por segundo.

Para obtener buen rendimiento, el mecanismo de autenticación v3 comprueba las contraseñas en la capa de API de etcd, donde puede paralelizarse fuera de raft. Sin embargo, esto puede dar lugar a posibles desfases de permisos de tipo time-of-check/time-of-use (TOCTOU):
1. el cliente A envía una solicitud `Authenticate()`
1. la capa de API procesa la parte de comprobación de contraseña de `Authenticate()`
1. otro cliente B envía una solicitud `ChangePassword()` y el servidor la completa
1. la capa de la máquina de estados procesa la parte de obtención de un número de revisión para el `Authenticate()` de A
1. el servidor devuelve un éxito a A
1. ahora A está autenticado con una contraseña obsoleta

Para evitar tal situación, la capa de API realiza una *validación del número de versión* basada en el número de revisión del almacén de autenticación. Durante la comprobación de la contraseña, la capa de API guarda el número de revisión del almacén de autenticación. Tras una comprobación de contraseña exitosa, la capa de API compara el número de revisión guardado con el número de revisión más reciente. Si los números difieren, significa que otra persona actualizó los metadatos de autenticación, así que reintenta la comprobación. Con este mecanismo se puede evitar una comprobación de contraseña exitosa basada en la contraseña obsoleta.

### Resolución de un token en la capa de API {#resolving-a-token-in-the-api-layer}

Tras autenticarse con `Authenticate()`, un cliente puede crear una conexión gRPC como lo haría sin autenticación. Además del proceso de inicialización existente, el cliente debe asociar el token con la conexión recién creada. `grpc.WithPerRPCCredentials()` proporciona la funcionalidad para este propósito.

Cada solicitud autenticada del cliente lleva un token. El token puede obtenerse con `grpc.metadata.FromIncomingContext()` en el lado del servidor. El servidor puede saber quién emite la solicitud y cuándo fue autorizado el usuario. La información la rellenará la capa de API en la cabecera (`etcdserverpb.RequestHeader.Username` y `etcdserverpb.RequestHeader.AuthRevision`) de una entrada del registro de Raft (`etcdserverpb.InternalRaftRequest`).

### Comprobación de permisos en la máquina de estados {#checking-permission-in-the-state-machine}

La información de autenticación de `etcdserverpb.RequestHeader` se comprueba en la fase de aplicación de la máquina de estados. Este paso comprueba que el usuario tenga concedido el permiso sobre las claves solicitadas en la última revisión del almacén de autenticación.

### Dos tipos de tokens: simple y JWT {#two-types-of-tokens-simple-and-jwt}

Existen dos tipos de tokens: simple y JWT. El token simple no está diseñado para casos de uso en producción. Sus tokens no están firmados criptográficamente y los servidores deben rastrear con estado la correspondencia entre token y usuario; está destinado a pruebas de desarrollo. Los tokens JWT deberían usarse en despliegues de producción, ya que están firmados y verificados criptográficamente. Desde la perspectiva de la implementación, JWT es sin estado. Su token puede incluir metadatos como el nombre de usuario y la revisión, de modo que los servidores no necesitan recordar la correspondencia entre los tokens y los metadatos.

> [!WARNING]
> Existe un problema conocido, el [#18437](https://github.com/etcd-io/etcd/issues/18437), con los tokens simples. Dentro de los servidores de etcd, los tokens se resuelven en la capa de API y los tokens simples tienen estado. El proceso no está protegido por una comprobación linealizable, lo que significa que es posible que un miembro de etcd no haya terminado de procesar una solicitud de autenticación anterior antes de recibir la siguiente. En tales casos, el miembro podría devolver al cliente un error de «invalid auth token». Este problema suele ser infrecuente en un nodo con buenas condiciones de red, pero puede ocurrir si hay una latencia significativa. Como solución alternativa, las aplicaciones pueden implementar un mecanismo de reintentos para gestionar este error.

### Establecimiento directo de tokens JWT {#directly-setting-jwt-tokens}

Además del flujo estándar del RPC `Authenticate()`, etcd admite el establecimiento de tokens JWT directamente a nivel del cliente. Esto permite a las aplicaciones gestionar el ciclo de vida completo de los tokens JWT fuera de etcd, incluida la generación, la validación y la rotación de tokens.

#### Caso de uso y flujo de trabajo {#use-case-and-workflow}

Este enfoque es útil cuando:

* Un sistema de gestión de tokens independiente (fuera de etcd) se encarga de la generación y del ciclo de vida de los tokens JWT
* Las aplicaciones reciben tokens JWT prefirmados mediante un mecanismo externo (por ejemplo, variables de entorno, un servicio de configuración)
* El ciclo de vida de los tokens debe gestionarse por completo mediante la aplicación cliente y no mediante la generación automática de tokens de etcd

El flujo de trabajo típico es:

1. Una autoridad externa (no etcd) genera un token JWT firmado que incluye el nombre de usuario y otros claims
2. La aplicación recibe el token prefirmado y configura con él el cliente de etcd
3. El cliente envía el token JWT directamente con las solicitudes (sin llamar a `Authenticate()`)
4. El servidor de etcd valida la firma del token usando su clave pública configurada y concede acceso según el nombre de usuario del token
5. Antes de que el token expire, la aplicación obtiene un token nuevo de la autoridad externa
6. La aplicación crea un cliente nuevo con el token actualizado (la actualización del token exige recrear el cliente)

#### En qué se diferencia de la autenticación estándar {#how-it-differs-from-standard-authentication}

Al usar el flujo estándar de `Authenticate()`:

* El cliente llama a `Authenticate()` con el nombre de usuario y la contraseña
* etcd genera y devuelve un token
* El cliente usa automáticamente este token para las solicitudes posteriores
* La renovación del token requiere llamar de nuevo a `Authenticate()`

Al establecer tokens JWT directamente:

* El cliente se inicializa con un token JWT prefirmado
* El cliente **no** llama a `Authenticate()`
* El token se usa directamente en todas las solicitudes
* La aplicación cliente es responsable de obtener tokens nuevos antes de la expiración y de gestionar el ciclo de vida del cliente

#### AuthStatus sin un token válido {#authstatus-without-valid-token}

Para dar soporte a las aplicaciones que gestionan sus propios tokens JWT, el RPC `AuthStatus` está diseñado para permitir a los clientes determinar si la autenticación está habilitada y recuperar el `authRevision` actual. Esto es importante en escenarios de recuperación donde un token ha expirado y el cliente necesita la última revisión para obtener un token nuevo y válido de su proveedor externo de tokens.

Sin esta capacidad, un token expirado podría impedir que un cliente conozca el `authRevision` actual, lo que daría lugar a un interbloqueo donde no puede generarse ningún token nuevo.

## Notas sobre la diferencia entre los modelos KVS y los modelos de sistema de archivos {#notes-on-the-difference-between-kvs-models-and-file-system-models}

etcd v3 es un KVS, no un sistema de archivos. Por eso los permisos pueden concederse a los usuarios en forma de un nombre de clave exacto o de un rango de claves como `["start key", "end key")`. Esto significa que es posible conceder un permiso sobre una clave inexistente. Los usuarios deberían cuidarse de no conceder permisos de forma no intencionada. En el caso de un sistema similar a un sistema de archivos (por ejemplo, Chubby o ZooKeeper), una estructura de datos similar a un inode puede incluir la información de permisos, por lo que conceder permiso sobre una clave inexistente no sería posible (salvo el caso de los bits sticky).

El modelo de etcd v3 requiere múltiples búsquedas de metadatos, a diferencia de los sistemas similares a sistemas de archivos. El costo de búsqueda en el peor de los casos será la suma de todas las claves e intervalos concedidos al usuario. Este costo no puede evitarse porque el espacio de claves plano de la v3 es completamente distinto del modelo de sistema de archivos de Unix (donde cada inode incluye metadatos de permisos). En la práctica, el costo no será un problema serio porque los metadatos son lo bastante pequeños para beneficiarse del caché.
