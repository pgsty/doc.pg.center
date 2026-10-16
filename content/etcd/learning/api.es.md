---
title: etcd API
weight: 2625
description: Visión general del diseño central de la API de etcd
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/api.md"
---

Este documento pretende ofrecer una visión general del diseño central de las API de etcd v3.
No debe confundirse con la API v2 de etcd, obsoleta a partir de etcd v3.5.
No es de ningún modo exhaustivo, sino que pretende centrarse en las ideas básicas necesarias para entender etcd sin la distracción de las llamadas a la API menos habituales.
Todas las API de etcd están definidas en [servicios gRPC][grpc-service], que clasifican las llamadas a procedimiento remoto (RPC) que entiende el servidor etcd.
Un listado completo de todas las RPC de etcd está documentado en markdown en el [listado de la API gRPC][grpc-api].

## Servicios gRPC {#grpc-services}

Cada solicitud de API enviada a un servidor etcd es una llamada a procedimiento remoto gRPC. Las RPC en etcd se clasifican según su funcionalidad en servicios.

Los servicios importantes para trabajar con el espacio de claves de etcd incluyen:
* KV - Crea, actualiza, obtiene y elimina pares clave-valor.
* Watch - Observa los cambios en las claves.
* Lease - Primitivas para consumir los mensajes keep-alive de los clientes.

Los servicios que gestionan el propio clúster incluyen:
* Auth - Mecanismo de autenticación basado en roles para autenticar usuarios.
* Cluster - Proporciona información de pertenencia y utilidades de configuración.
* Maintenance - Toma instantáneas de recuperación, desfragmenta el almacén y devuelve información de estado por miembro.

### Solicitudes y respuestas {#requests-and-responses}

Todas las RPC en etcd siguen el mismo formato. Cada RPC tiene una función `Name` que toma `NameRequest` como argumento y devuelve `NameResponse` como respuesta. Por ejemplo, esta es la descripción de la RPC `Range`:

```protobuf
service KV {
  Range(RangeRequest) returns (RangeResponse)
  ...
}
```

### Cabecera de respuesta {#response-header}

Todas las respuestas de la API de etcd llevan adjunta una cabecera de respuesta que incluye metadatos del clúster para la respuesta:

```proto
message ResponseHeader {
  uint64 cluster_id = 1;
  uint64 member_id = 2;
  int64 revision = 3;
  uint64 raft_term = 4;
}
```

* Cluster_ID - el ID del clúster que genera la respuesta.
* Member_ID - el ID del miembro que genera la respuesta.
* Revision - la revisión del almacén clave-valor al generar la respuesta.
* Raft_Term - el término de Raft del miembro al generar la respuesta.

Una aplicación puede leer el campo `Cluster_ID` o `Member_ID` para asegurarse de que se comunica con el clúster (miembro) previsto.

Las aplicaciones pueden usar el campo `Revision` para conocer la última revisión del almacén clave-valor. Esto es especialmente útil cuando las aplicaciones especifican una revisión histórica para hacer una `time travel query` y desean conocer la última revisión en el momento de la solicitud.

Las aplicaciones pueden usar `Raft_Term` para detectar cuándo el clúster completa una nueva elección de líder.

## API clave-valor {#key-value-api}

La API clave-valor manipula pares clave-valor almacenados dentro de etcd. La mayoría de las solicitudes hechas a etcd suelen ser solicitudes clave-valor.

### Primitivas del sistema {#system-primitives}

### Par clave-valor {#key-value-pair}

Un par clave-valor es la unidad más pequeña que la API clave-valor puede manipular. Cada par clave-valor tiene una serie de campos, definidos en [formato protobuf][kv-proto]:

```protobuf
message KeyValue {
  bytes key = 1;
  int64 create_revision = 2;
  int64 mod_revision = 3;
  int64 version = 4;
  bytes value = 5;
  int64 lease = 6;
}
```

* Key - clave en bytes. No se permite una clave vacía.
* Value - valor en bytes.
* Version - la versión de la clave. Una eliminación restablece la versión a cero y cualquier modificación de la clave incrementa su versión.
* Create_Revision - revisión de la última creación de la clave.
* Mod_Revision - revisión de la última modificación de la clave.
* Lease - el ID de la concesión adjunta a la clave. Si lease es 0, no hay ninguna concesión adjunta a la clave.


Además de la clave y el valor, etcd adjunta metadatos de revisión adicionales como parte del mensaje de la clave. Esta información de revisión ordena las claves por su momento de creación y modificación, lo cual es útil para gestionar la concurrencia en la sincronización distribuida. Los [bloqueos compartidos distribuidos][locks] del cliente de etcd usan la revisión de creación para esperar la propiedad del bloqueo. De forma similar, la revisión de modificación se usa para detectar los conflictos del conjunto de lectura de la [memoria transaccional de software][STM] y para esperar las actualizaciones de la [elección de líder][elections].

#### Revisiones {#revisions}

etcd mantiene un contador de 64 bits para todo el clúster, la revisión del almacén, que se incrementa cada vez que se modifica el espacio de claves. La revisión sirve como reloj lógico global, ordenando secuencialmente todas las actualizaciones del almacén. El cambio representado por una nueva revisión es incremental; los datos asociados a una revisión son los datos que cambiaron el almacén. Internamente, una nueva revisión significa escribir los cambios en el árbol B+ del backend, indexados por la revisión incrementada.

Las revisiones se vuelven más valiosas al considerar el backend de [control de concurrencia multiversión][mvcc] de etcd. El modelo MVCC significa que el almacén clave-valor puede verse desde revisiones pasadas, ya que se conservan las revisiones históricas de las claves. La política de retención de este historial puede ser configurada por los administradores del clúster para una gestión fina del almacenamiento; normalmente etcd descarta las revisiones antiguas de las claves de forma temporizada. Un clúster de etcd típico conserva durante horas los datos sustituidos de las claves. Esto también proporciona una gestión fiable de las desconexiones largas de clientes, y no solo de interrupciones de red transitorias: las observaciones simplemente se reanudan desde la última revisión histórica observada. De forma similar, para leer del almacén en un punto temporal concreto, las solicitudes de lectura pueden etiquetarse con una revisión para devolver las claves de una vista del espacio de claves en el momento en que esa revisión se confirmó.

#### Rangos de claves {#key-ranges}

El modelo de datos de etcd indexa todas las claves en un espacio de claves binario plano. Esto difiere de otros sistemas de almacén clave-valor que usan un sistema jerárquico de organización de claves en directorios. En lugar de listar las claves por directorio, las claves se listan por intervalos de claves `[a, b)`.

Estos intervalos se denominan a menudo «rangos» en etcd. Las operaciones sobre rangos son más potentes que las operaciones sobre directorios. Igual que un almacén jerárquico, los intervalos permiten búsquedas de clave única mediante `[a, a+1)` (por ejemplo, ['a', 'a\x00') busca 'a') y búsquedas por directorio codificando las claves por su profundidad de directorio. Además de esas operaciones, los intervalos también pueden codificar prefijos; por ejemplo, el intervalo `['a', 'b')` busca todas las claves que tienen por prefijo la cadena 'a'.

Por convención, los rangos de una solicitud se denotan con los campos `key` y `range_end`. El campo `key` es la primera clave del rango y debe ser no vacío. El `range_end` es la clave siguiente a la última clave del rango. Si `range_end` no se proporciona o está vacío, el rango se define para contener solo la clave del argumento. Si `range_end` es `key` más uno (por ejemplo, "aa"+1 == "ab", "a\xff"+1 == "b"), entonces el rango representa todas las claves que tienen por prefijo la clave. Si tanto `key` como `range_end` son '\0', el rango representa todas las claves. Si `range_end` es '\0', el rango son todas las claves mayores o iguales que la clave del argumento.

### Range {#range}

Las claves se obtienen del almacén clave-valor usando la llamada a la API `Range`, que toma un `RangeRequest`:

```protobuf
message RangeRequest {
  enum SortOrder {
	NONE = 0; // default, no sorting
	ASCEND = 1; // lowest target value first
	DESCEND = 2; // highest target value first
  }
  enum SortTarget {
	KEY = 0;
	VERSION = 1;
	CREATE = 2;
	MOD = 3;
	VALUE = 4;
  }

  bytes key = 1;
  bytes range_end = 2;
  int64 limit = 3;
  int64 revision = 4;
  SortOrder sort_order = 5;
  SortTarget sort_target = 6;
  bool serializable = 7;
  bool keys_only = 8;
  bool count_only = 9;
  int64 min_mod_revision = 10;
  int64 max_mod_revision = 11;
  int64 min_create_revision = 12;
  int64 max_create_revision = 13;
}
```

* Key, Range_End - El rango de claves a obtener.
* Limit - el número máximo de claves devueltas para la solicitud. Cuando limit se establece en 0, se trata como sin límite.
* Revision - el punto temporal del almacén clave-valor que se usará para el rango. Si revision es menor o igual que cero, el rango se hace sobre el almacén clave-valor más reciente. Si la revisión está compactada, se devuelve ErrCompacted como respuesta.
* Sort_Order - el orden para las solicitudes ordenadas.
* Sort_Target - el campo clave-valor por el que ordenar.
* Serializable - establece que la solicitud de rango use lecturas serializables locales al miembro. Por defecto, Range es linealizable; refleja el consenso actual del clúster. Para obtener mejor rendimiento y disponibilidad, a cambio de posibles lecturas obsoletas, una solicitud de rango serializable se atiende localmente sin necesidad de alcanzar consenso con los otros nodos del clúster.
* Keys_Only - devuelve solo las claves y no los valores.
* Count_Only - devuelve solo el número de claves del rango.
* Min_Mod_Revision - el límite inferior para las revisiones de modificación de las claves; excluye las revisiones de modificación menores.
* Max_Mod_Revision - el límite superior para las revisiones de modificación de las claves; excluye las revisiones de modificación mayores.
* Min_Create_Revision - el límite inferior para las revisiones de creación de las claves; excluye las revisiones de creación menores.
* Max_Create_Revision - el límite superior para las revisiones de creación de las claves; excluye las revisiones de creación mayores.

El cliente recibe un mensaje `RangeResponse` de la llamada `Range`:

```protobuf
message RangeResponse {
  ResponseHeader header = 1;
  repeated mvccpb.KeyValue kvs = 2;
  bool more = 3;
  int64 count = 4;
}
```

* Kvs - la lista de pares clave-valor que coinciden con la solicitud de rango. Cuando se establece `Count_Only`, `Kvs` está vacío.
* More - indica si hay más claves que devolver en el rango solicitado si se establece `limit`.
* Count - el número total de claves que satisfacen la solicitud de rango.

Para rangos de claves grandes donde almacenar en búfer la respuesta completa no sea deseable, consulta [RangeStream](#rangestream).

### RangeStream {#rangestream}

`RangeStream` devuelve el mismo conjunto de resultados que `Range`, pero el servidor divide la respuesta en una secuencia de fragmentos y los transmite en streaming al cliente. Esto evita almacenar en búfer rangos grandes por completo en memoria en cualquiera de los dos lados. `RangeStream` acepta el mismo `RangeRequest` que `Range`.

El cliente recibe un flujo de mensajes `RangeStreamResponse` de la llamada `RangeStream`:

```protobuf
message RangeStreamResponse {
  RangeResponse range_response = 1;
}
```

Relleno de los campos entre fragmentos:

* Kvs - cada fragmento lleva una porción disjunta del resultado. Concatenar los `kvs` de cada fragmento en el orden en que llegan produce el mismo conjunto de claves que una única llamada `Range`.
* Header, More, Count - se rellenan solo en el fragmento final, y solo cuando el flujo termina sin error. Los fragmentos anteriores dejan estos campos con valor cero. Aplicar `proto.Merge` sobre el `range_response` de cada fragmento produce un `RangeResponse` equivalente a lo que `Range` habría devuelto.

Si el flujo termina con error, ningún fragmento lleva un `header`, `more` o `count` válidos.

Cada fragmento del flujo se atiende sobre la misma revisión. Si la solicitud no establece `Revision`, el servidor captura la última revisión confirmada cuando comienza el flujo y la reutiliza para el resto del flujo.

`RangeStream` no admite órdenes de clasificación personalizadas ni filtros de revisión (`min_mod_revision`, `max_mod_revision`, `min_create_revision`, `max_create_revision`). Las solicitudes que usen cualquiera de ellos devuelven `Unimplemented`. `RangeStream` tampoco está soportado por el proxy gRPC de etcd.

Hay dos formas habituales de consumir un `RangeStream`:

1. **Procesar cada fragmento de forma independiente.** Adecuado para escenarios de alto rendimiento donde el cliente quiere decodificar y actuar sobre las claves a medida que llegan, en lugar de recopilar primero todo el resultado. El cliente itera los fragmentos y gestiona los `kvs` de cada uno, y después lee `header`, `more` o `count` del último fragmento cuando el flujo termina limpiamente.
2. **Ensamblar una única respuesta.** Adecuado cuando el cliente quiere un resultado equivalente a un `Range` unario. El cliente fusiona el `range_response` de cada fragmento en un solo `RangeResponse` (por ejemplo, mediante `proto.Merge`). El resultado fusionado contiene los `kvs` completos, más `header`, `more` y `count` del fragmento final. El cliente Go proporciona `clientv3.GetStreamToGetResponse` como utilidad para este patrón.

### Put {#put}

Las claves se guardan en el almacén clave-valor emitiendo una llamada `Put`, que toma un `PutRequest`:

```protobuf
message PutRequest {
  bytes key = 1;
  bytes value = 2;
  int64 lease = 3;
  bool prev_kv = 4;
  bool ignore_value = 5;
  bool ignore_lease = 6;
}
```

* Key - el nombre de la clave a poner en el almacén clave-valor.
* Value - el valor, en bytes, que asociar a la clave en el almacén clave-valor.
* Lease - el ID de la concesión que asociar a la clave en el almacén clave-valor. Un valor de lease de 0 indica que no hay concesión.
* Prev_Kv - cuando se establece, responde con los datos del par clave-valor previos a la actualización de esta solicitud `Put`.
* Ignore_Value - cuando se establece, actualiza la clave sin cambiar su valor actual. Devuelve un error si la clave no existe.
* Ignore_Lease - cuando se establece, actualiza la clave sin cambiar su concesión actual. Devuelve un error si la clave no existe.

El cliente recibe un mensaje `PutResponse` de la llamada `Put`:

```protobuf
message PutResponse {
  ResponseHeader header = 1;
  mvccpb.KeyValue prev_kv = 2;
}
```

* Prev_Kv - el par clave-valor sobrescrito por `Put`, si `Prev_Kv` se estableció en el `PutRequest`.

### Eliminar un rango {#delete-range}

Los rangos de claves se eliminan usando la llamada `DeleteRange`, que toma un `DeleteRangeRequest`:

```protobuf
message DeleteRangeRequest {
  bytes key = 1;
  bytes range_end = 2;
  bool prev_kv = 3;
}
```

* Key, Range_End - El rango de claves a eliminar.
* Prev_Kv - cuando se establece, devuelve el contenido de los pares clave-valor eliminados.

El cliente recibe un mensaje `DeleteRangeResponse` de la llamada `DeleteRange`:

```protobuf
message DeleteRangeResponse {
  ResponseHeader header = 1;
  int64 deleted = 2;
  repeated mvccpb.KeyValue prev_kvs = 3;
}
```

* Deleted - número de claves eliminadas.
* Prev_Kv - una lista de todos los pares clave-valor eliminados por la operación `DeleteRange`.

### Transacción {#transaction}

Una transacción es una construcción atómica If/Then/Else sobre el almacén clave-valor. Proporciona una primitiva para agrupar solicitudes en bloques atómicos (es decir, then/else) cuya ejecución está protegida (es decir, if) según el contenido del almacén clave-valor. Las transacciones pueden usarse para proteger las claves de actualizaciones concurrentes no deseadas, construir operaciones compare-and-swap y desarrollar control de concurrencia de nivel superior.

Una transacción puede procesar atómicamente varias solicitudes en una sola solicitud. Para las modificaciones del almacén clave-valor, esto significa que la revisión del almacén se incrementa solo una vez para la transacción y que todos los eventos generados por la transacción tendrán la misma revisión. Sin embargo, está prohibido modificar la misma clave varias veces dentro de una misma transacción.

Todas las transacciones están protegidas por una conjunción de comparaciones, similar a una instrucción `If`. Cada comparación comprueba una sola clave del almacén. Puede comprobar la ausencia o presencia de un valor, comparar con un valor dado, o comprobar la revisión o la versión de una clave. Dos comparaciones distintas pueden aplicarse a la misma clave o a claves diferentes. Todas las comparaciones se aplican atómicamente; si todas las comparaciones son verdaderas, se dice que la transacción tiene éxito y etcd aplica el bloque de solicitudes then / `success`; de lo contrario se dice que falla y aplica el bloque de solicitudes else / `failure`.

Cada comparación se codifica como un mensaje `Compare`:

```protobuf
message Compare {
  enum CompareResult {
    EQUAL = 0;
    GREATER = 1;
    LESS = 2;
    NOT_EQUAL = 3;
  }
  enum CompareTarget {
    VERSION = 0;
    CREATE = 1;
    MOD = 2;
    VALUE= 3;
  }
  CompareResult result = 1;
  // target is the key-value field to inspect for the comparison.
  CompareTarget target = 2;
  // key is the subject key for the comparison operation.
  bytes key = 3;
  oneof target_union {
    int64 version = 4;
    int64 create_revision = 5;
    int64 mod_revision = 6;
    bytes value = 7;
  }
}
```

* Result - el tipo de operación de comparación lógica (por ejemplo, igual, menor que, etc.).
* Target - el campo clave-valor que se va a comparar. Puede ser la versión de la clave, la revisión de creación, la revisión de modificación o el valor.
* Key - la clave de la comparación.
* Target_Union - los datos especificados por el usuario para la comparación.

Tras procesar el bloque de comparación, la transacción aplica un bloque de solicitudes. Un bloque es una lista de mensajes `RequestOp`:

```protobuf
message RequestOp {
  // request is a union of request types accepted by a transaction.
  oneof request {
    RangeRequest request_range = 1;
    PutRequest request_put = 2;
    DeleteRangeRequest request_delete_range = 3;
  }
}
```

* Request_Range - una `RangeRequest`.
* Request_Put - una `PutRequest`. Las claves deben ser únicas. No puede compartir claves con ningún otro Put o Delete.
* Request_Delete_Range - una `DeleteRangeRequest`. No puede compartir claves con ninguna solicitud Put o Delete.

Todo junto, una transacción se emite con una llamada a la API `Txn`, que toma un `TxnRequest`:

```protobuf
message TxnRequest {
  repeated Compare compare = 1;
  repeated RequestOp success = 2;
  repeated RequestOp failure = 3;
}
```

* Compare - Una lista de predicados que representan una conjunción de términos para proteger la transacción.
* Success - Una lista de solicitudes que procesar si todas las pruebas de comparación se evalúan como true.
* Failure - Una lista de solicitudes que procesar si alguna prueba de comparación se evalúa como false.

El cliente recibe un mensaje `TxnResponse` de la llamada `Txn`:

```protobuf
message TxnResponse {
  ResponseHeader header = 1;
  bool succeeded = 2;
  repeated ResponseOp responses = 3;
}
```

* Succeeded - Indica si `Compare` se evaluó como true o false.
* Responses - Una lista de respuestas correspondientes a los resultados de aplicar el bloque `Success` si succeeded es true, o el bloque `Failure` si succeeded es false.

La lista `Responses` corresponde a los resultados de la lista `RequestOp` aplicada, con cada respuesta codificada como un `ResponseOp`:

```protobuf
message ResponseOp {
  oneof response {
    RangeResponse response_range = 1;
    PutResponse response_put = 2;
    DeleteRangeResponse response_delete_range = 3;
  }
}
```

El `ResponseHeader` incluido en cada respuesta interna no debería interpretarse de ninguna manera.
Si los clientes necesitan obtener la última revisión, deberían comprobar siempre el `ResponseHeader` de nivel superior en `TxnResponse`.


## API de observación {#watch-api}

La API `Watch` proporciona una interfaz basada en eventos para observar de forma asíncrona los cambios en las claves. Una observación de etcd espera los cambios en las claves observando continuamente desde una revisión dada, actual o histórica, y transmite en streaming las actualizaciones de claves al cliente.

### Eventos {#events}

Cada cambio en cada clave se representa con mensajes `Event`. Un mensaje `Event` proporciona tanto los datos de la actualización como el tipo de actualización:

```protobuf
message Event {
  enum EventType {
    PUT = 0;
    DELETE = 1;
  }
  EventType type = 1;
  KeyValue kv = 2;
  KeyValue prev_kv = 3;
}
```

* Type - El tipo de evento. Un tipo PUT indica que se han almacenado datos nuevos en la clave. Un tipo DELETE indica que la clave fue eliminada.
* KV - El KeyValue asociado con el evento. Un evento PUT contiene el par clave-valor actual. Un evento PUT con kv.Version=1 indica la creación de una clave. Un evento DELETE contiene la clave eliminada con su revisión de modificación fijada en la revisión de la eliminación.
* Prev_KV - El par clave-valor de la clave en la revisión inmediatamente anterior al evento. Para ahorrar ancho de banda, solo se rellena si la observación lo ha activado explícitamente.

### Flujos de observación {#watch-streams}

Las observaciones son solicitudes de larga duración y usan flujos gRPC para transmitir los datos de eventos. Un flujo de observación es bidireccional; el cliente escribe en el flujo para establecer observaciones y lee para recibir los eventos de observación. Un único flujo de observación puede multiplexar muchas observaciones distintas etiquetando los eventos con identificadores propios de cada observación. Esta multiplexación ayuda a reducir el uso de memoria y la sobrecarga de conexiones en el clúster central de etcd.

Para leer sobre las garantías ofrecidas para los eventos de observación, consulta las [garantías de la API de etcd][watch-api-guarantees].

Un cliente crea una observación enviando un `WatchCreateRequest` por un flujo devuelto por `Watch`:

```protobuf
message WatchCreateRequest {
  bytes key = 1;
  bytes range_end = 2;
  int64 start_revision = 3;
  bool progress_notify = 4;

  enum FilterType {
    NOPUT = 0;
    NODELETE = 1;
  }
  repeated FilterType filters = 5;
  bool prev_kv = 6;
}
```

* Key, Range_End - El rango de claves a observar.
* Start_Revision - Una revisión opcional a partir de la cual empezar a observar de forma inclusiva. Si no se proporciona, se transmitirán los eventos posteriores a la revisión de la cabecera de la respuesta de creación de la observación. Todo el historial de eventos disponible puede observarse desde la última revisión de compactación.
* Progress_Notify - Cuando se establece, la observación recibirá periódicamente una WatchResponse sin eventos, si no hay eventos recientes. Es útil cuando los clientes quieren recuperar una observación desconectada desde una revisión conocida reciente. El servidor etcd decide con qué frecuencia enviar notificaciones según la carga actual del servidor.
* Filters - Una lista de tipos de eventos que excluir en el lado del servidor.
* Prev_Kv - Cuando se establece, la observación recibe los datos clave-valor previos a que ocurra el evento. Esto es útil para saber qué datos se han sobrescrito.

En respuesta a un `WatchCreateRequest`, o si hay un evento nuevo para alguna observación establecida, el cliente recibe un `WatchResponse`:

```protobuf
message WatchResponse {
  ResponseHeader header = 1;
  int64 watch_id = 2;
  bool created = 3;
  bool canceled = 4;
  int64 compact_revision = 5;

  repeated mvccpb.Event events = 11;
}
```

* Watch_ID - el ID de la observación a la que corresponde la respuesta.
* Created - se establece a true si la respuesta corresponde a una solicitud de creación de observación. El cliente debería almacenar el ID y esperar recibir eventos para esa observación en el flujo. Todos los eventos enviados a la observación creada tendrán el mismo watch_id.
* Canceled - se establece a true si la respuesta corresponde a una solicitud de cancelación de observación. No se enviarán más eventos a la observación cancelada.
* Compact_Revision - se establece a la mínima revisión histórica disponible en etcd si una observación intenta observar en una revisión compactada. Esto ocurre al crear una observación en una revisión compactada o cuando la observación no puede seguir el progreso del almacén clave-valor. La observación será cancelada; crear observaciones nuevas con la misma start_revision fallará.
* Events - una lista de eventos nuevos en secuencia correspondiente al ID de observación dado.

Si el cliente desea dejar de recibir eventos para una observación, emite un `WatchCancelRequest`:

```protobuf
message WatchCancelRequest {
   int64 watch_id = 1;
}
```

* Watch_ID - el ID de la observación a cancelar para que no se transmitan más eventos.

## API de concesiones {#lease-api}

Las concesiones son un mecanismo para detectar la vitalidad de los clientes. El clúster otorga concesiones con un tiempo de vida. Una concesión expira si el clúster de etcd no recibe un keepAlive dentro de un periodo TTL dado.

Para vincular las concesiones con el almacén clave-valor, cada clave puede adjuntarse como máximo a una concesión. Cuando una concesión expira o es revocada, todas las claves adjuntas a esa concesión se eliminarán. Cada clave expirada genera un evento de eliminación en el historial de eventos.

### Obtención de concesiones {#obtaining-leases}

Las concesiones se obtienen mediante la llamada a la API `LeaseGrant`, que toma un `LeaseGrantRequest`:

```protobuf
message LeaseGrantRequest {
  int64 TTL = 1;
  int64 ID = 2;
}
```

* TTL - el tiempo de vida orientativo, en segundos.
* ID - el ID solicitado para la concesión. Si ID se establece en 0, etcd elegirá un ID.

El cliente recibe un `LeaseGrantResponse` de la llamada `LeaseGrant`:

```protobuf
message LeaseGrantResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - el ID de la concesión de la concesión otorgada.
* TTL - es el tiempo de vida, en segundos, seleccionado por el servidor para la concesión.

```protobuf
message LeaseRevokeRequest {
  int64 ID = 1;
}
```

* ID - el ID de la concesión a revocar. Cuando se revoca la concesión, todas las claves adjuntas se eliminan.

### Renovación de concesiones {#keep-alives}

Las concesiones se renuevan usando un flujo bidireccional creado con la llamada a la API `LeaseKeepAlive`. Cuando el cliente desea renovar una concesión, envía un `LeaseKeepAliveRequest` por el flujo:

```protobuf
message LeaseKeepAliveRequest {
  int64 ID = 1;
}
```

* ID - el ID de la concesión que se debe mantener viva.

El flujo de keep alive responde con un `LeaseKeepAliveResponse`:

```protobuf
message LeaseKeepAliveResponse {
  ResponseHeader header = 1;
  int64 ID = 2;
  int64 TTL = 3;
}
```

* ID - la concesión que fue renovada con un nuevo TTL.
* TTL - el nuevo tiempo de vida, en segundos, que le queda a la concesión.

[watch-api-guarantees]: /es/etcd/learning/api_guarantees/#watch-apis
[elections]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/election.go
[grpc-api]: /es/etcd/dev-guide/api_reference_v3/
[grpc-service]: https://github.com/etcd-io/etcd/blob/main/api/etcdserverpb/rpc.proto
[kv-proto]: https://github.com/etcd-io/etcd/blob/main/api/mvccpb/kv.proto
[locks]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go
[mvcc]: https://en.wikipedia.org/wiki/Multiversion_concurrency_control
[stm]: https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/stm.go
