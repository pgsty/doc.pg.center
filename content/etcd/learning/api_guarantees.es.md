---
title: Garantías de la API de etcd
weight: 2750
description: Garantías de API ofrecidas por etcd
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/api_guarantees.md"
---

etcd es un almacén clave-valor consistente y duradero.
El almacén clave-valor se expone mediante [servicios gRPC][grpc Services].
etcd garantiza la consistencia y durabilidad más fuertes para un sistema distribuido.
Esta especificación enumera las garantías de API que ofrece etcd.

### APIs a considerar {#apis-to-consider}

* APIs de KV
  * [Range](/es/etcd/learning/api/#range)
  * [RangeStream](/es/etcd/learning/api/#rangestream)
  * [Put](/es/etcd/learning/api/#put)
  * [Delete](/es/etcd/learning/api/#delete-range)
  * [Transaction](/es/etcd/learning/api/#transaction)
* APIs de observación
  * [Watch](/es/etcd/learning/api/#watch-api)
* APIs de concesión
  * [Grant](/es/etcd/learning/api/#obtaining-leases)
  * [Revoke]
  * [Keep alive](/es/etcd/learning/api/#keep-alives)

La API de KV permite leer y manipular directamente el almacén clave-valor.
La API de observación permite suscribirse a los cambios del almacén clave-valor.
La API de concesión permite asignar un tiempo de vida a una clave.

Tanto las APIs de KV como las de observación permiten acceder no solo a las últimas versiones de las claves; las versiones
anteriores también son accesibles dentro de una ventana de historial continua, limitada
por una operación de compactación.

La llamada a la API de KV tiene un efecto inmediato, mientras que la API de observación responderá con algún retardo no acotado.
En un clúster de etcd que funciona correctamente, deberías esperar que los eventos de observación aparezcan con un retardo de 10ms después de producirse.
Sin embargo, no hay límite, y los eventos en clústeres en mal estado podrían no llegar nunca.

## APIs de KV {#kv-apis}

etcd garantiza durabilidad y serializabilidad estricta para todas las llamadas a la API de KV.
Estas son las garantías de aislamiento más fuertes de los sistemas de bases de datos transaccionales distribuidas.

### Durabilidad {#durability}

Toda operación completada es duradera. Todos los datos accesibles son también datos duraderos.
Una lectura nunca devolverá datos que no se hayan hecho duraderos.

### Serializabilidad estricta {#strict-serializability}

Las operaciones del servicio KV son atómicas y ocurren en un orden total, consistente con
el orden en tiempo real de esas operaciones. El orden total se infiere a través de la [revisión][revision].
Lee más sobre la [serializabilidad estricta][strict serializability].

Para las transacciones sin TXN anidados, se garantiza que el orden de ejecución de las operaciones
es el mismo que en su lista de operaciones, lo que significa respuestas GET estables
dentro de la transacción.
Para las transacciones con TXN anidados, el orden de ejecución no está especificado.

La serializabilidad estricta implica otras garantías más débiles que pueden ser más fáciles de entender:

#### Atomicidad {#atomicity}

Todas las solicitudes a la API son atómicas; una operación o se completa por completo o no
se completa en absoluto. Para las solicitudes de observación, todos los eventos generados por una misma operación
estarán en una sola respuesta de observación. La observación nunca ve eventos parciales de una sola operación.

#### Linealizabilidad {#linearizability}

Desde la perspectiva del cliente, la linealizabilidad ofrece propiedades útiles que
facilitan el razonamiento. Esta es una descripción clara citada del
[artículo original][linearizability]: `La linealizabilidad proporciona la ilusión
de que cada operación aplicada por procesos concurrentes surte efecto instantáneamente
en algún punto entre su invocación y su respuesta.`

Por ejemplo, considera un cliente que completa una escritura en el punto temporal 1 (*t1*). Un
cliente que emite una lectura en *t2* (con *t2* > *t1*) debería recibir un valor al menos
tan reciente como la escritura previa, completada en *t1*. Sin embargo, la lectura podría
en realidad completarse solo en *t3*. La lectura devuelve el valor vigente en
un único punto entre *t2* y *t3*. Puede incluir o excluir una escritura
concurrente con esa lectura, por lo que aún puede devolverse un valor vigente en
*t2* incluso si otra escritura se completa antes de *t3*.

etcd garantiza la linealizabilidad para todas las demás operaciones por defecto.
La linealizabilidad tiene un coste, sin embargo, porque las solicitudes linealizadas deben pasar
por el proceso de consenso de Raft. Para obtener latencias más bajas y un mayor
caudal de solicitudes de lectura, los clientes pueden configurar el modo de consistencia
de una solicitud a `serializable`, que puede acceder a datos obsoletos con respecto al cuórum, pero
elimina la penalización de rendimiento de la dependencia de los accesos linealizables en el consenso activo.

## APIs de observación {#watch-apis}

Las observaciones ofrecen garantías sobre los eventos:
* Ordenados - los eventos están ordenados por revisión.
  Un evento nunca aparecerá en una observación si precede en el tiempo a un evento
  que ya se ha publicado. Para las transacciones sin TXN anidados, el orden de los
  eventos generados se garantiza igual que en su lista de operaciones.
  Para las transacciones con TXN anidados, el orden de los eventos generados no está
  especificado.
* Únicos - un evento nunca aparecerá dos veces en una observación.
* Fiables - una secuencia de eventos nunca descartará ninguna subsecuencia de eventos
  dentro de la ventana de historial disponible. Si hay eventos ordenados en el tiempo como
  a < b < c, entonces si la observación recibe los eventos a y c, tiene garantizado
  recibir b mientras b esté en la ventana de historial disponible.
* Atómicos - se garantiza que una lista de eventos abarca revisiones completas.
  Las actualizaciones en la misma revisión sobre varias claves no se dividirán entre varias
  listas de eventos.
* Reanudables - una observación interrumpida puede reanudarse estableciendo una nueva observación que empiece
  después de la última revisión recibida en un evento de observación antes de la interrupción, siempre que
  la revisión esté en la ventana de historial.
* Con marcadores - los eventos de notificación de progreso garantizan que todos los eventos hasta una
  revisión ya han sido entregados.

etcd no garantiza la linealizabilidad para las operaciones de observación. Se espera que los usuarios
verifiquen la revisión de los eventos de observación para asegurar un orden correcto respecto a otras operaciones.

## APIs de concesión {#lease-apis}

etcd proporciona [un mecanismo de concesiones][lease]. El caso de uso principal de una concesión es
implementar mecanismos de coordinación distribuida como bloqueos distribuidos. El
mecanismo de concesión en sí es simple: una concesión puede crearse con la API grant,
adjuntarse a una clave con la API put, revocarse con la API revoke, y expirará
por su tiempo de vida (TTL) según el reloj de pared. Sin embargo, los usuarios deben conocer
[las propiedades importantes de las APIs y de su uso][why] para implementar
mecanismos de coordinación distribuida correctos.

## Definiciones específicas de etcd {#etcd-specific-definitions}

### Operación completada {#operation-completed}

Una operación de etcd se considera completa cuando se confirma mediante consenso
y, por tanto, queda «ejecutada» — almacenada de forma permanente — por el motor de almacenamiento de
etcd. El cliente sabe que una operación está completa cuando recibe una respuesta del
servidor etcd. Ten en cuenta que el cliente puede estar en duda sobre el estado de una
operación si se agota el tiempo de espera, o si hay una interrupción de red entre el cliente
y el miembro de etcd. etcd también puede abortar operaciones cuando hay una elección
de líder. etcd no envía respuestas `abort` a las solicitudes pendientes de los clientes
en tal caso.

### Revisión {#revision}

Una operación de etcd que modifica el almacén clave-valor recibe una única
revisión creciente. Una operación transaccional puede modificar el almacén clave-valor
varias veces, pero solo se asigna una revisión. El atributo revision de un
par clave-valor modificado por la operación tiene el mismo valor que la
revisión de la operación. La revisión puede usarse como reloj lógico para el almacén
clave-valor. Un par clave-valor con una revisión mayor se modifica después que un par
clave-valor con una revisión menor. Dos pares clave-valor con la misma
revisión son modificados por una operación «de forma concurrente».

[grpc Services]: /es/etcd/learning/api/#grpc-services
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[linearizability]: https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf
[serializable_isolation]: https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable
[strict serializability]: http://jepsen.io/consistency/models/strict-serializable
[txn]: /es/etcd/learning/api/#transaction
[why]: /es/etcd/learning/why/#notes-on-the-usage-of-lock-and-lease
[revision]: #revision
