---
title: "Referencia de API: concurrencia"
weight: 3900
description: "Referencia de las API de concurrencia de etcd"
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

Esta referencia de API se genera automáticamente a partir de los archivos `.proto` nombrados.

##### service `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

El servicio de bloqueo expone funcionalidades de bloqueo del lado del cliente como una interfaz gRPC.

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lock adquiere un bloqueo compartido distribuido sobre un bloqueo con nombre determinado. En caso de éxito, devolverá una clave única que existe mientras el bloqueo esté en poder del llamador. Esta clave puede usarse junto con transacciones para garantizar de forma segura que las actualizaciones a etcd solo ocurran mientras se mantiene la propiedad del bloqueo. El bloqueo se mantiene hasta que se llame a Unlock sobre la clave o hasta que expire la concesión asociada al propietario. |
| Unlock | UnlockRequest | UnlockResponse | Unlock toma una clave devuelta por Lock y libera la retención del bloqueo. El siguiente llamador de Lock que esté esperando el bloqueo será entonces despertado y recibirá la propiedad del bloqueo. |

##### message `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name | name es el identificador del bloqueo compartido distribuido que se va a adquirir. | bytes |
| lease | lease es el ID de la concesión que se adjuntará a la propiedad del bloqueo. Si la concesión expira o es revocada y actualmente mantiene el bloqueo, el bloqueo se libera automáticamente. Las llamadas a Lock con la misma concesión se tratarán como una única adquisición; bloquear dos veces con la misma concesión es una operación sin efecto. | int64 |

##### message `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | key es una clave que existirá en etcd durante el tiempo en que el llamador de Lock posea el bloqueo. Los usuarios no deben modificar esta clave o el bloqueo podría presentar un comportamiento indefinido. | bytes |

##### message `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| key | key es la clave de propiedad del bloqueo otorgada por Lock. | bytes |

##### message `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### service `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

El servicio de elección expone funcionalidades de elección del lado del cliente como una interfaz gRPC.

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaign espera adquirir el liderazgo en una elección, devolviendo una LeaderKey que representa el liderazgo en caso de éxito. La LeaderKey puede usarse entonces para emitir nuevos valores en la elección, proteger transaccionalmente solicitudes a la API mientras el liderazgo se mantenga, y renunciar a la elección. |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaim actualiza el valor publicado del líder con un nuevo valor. |
| Leader | LeaderRequest | LeaderResponse | Leader devuelve la proclamación actual de la elección, si la hay. |
| Observe | LeaderRequest | LeaderResponse | Observe transmite en orden las proclamaciones de la elección a medida que las realizan los líderes electos. |
| Resign | ResignRequest | ResignResponse | Resign libera el liderazgo de la elección para que otros candidatos puedan adquirir el liderazgo de la elección. |

##### message `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name | name es el identificador de la elección para la campaña. | bytes |
| lease | lease es el ID de la concesión adjunta al liderazgo de la elección. Si la concesión expira o es revocada antes de renunciar al liderazgo, este se transfiere al siguiente candidato, si lo hay. | int64 |
| value | value es el valor proclamado inicial que se establece cuando el candidato gana la elección. | bytes |

##### message `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader describe los recursos utilizados para mantener el liderazgo de la elección. | LeaderKey |

##### message `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name | name es el identificador de la elección que corresponde a la clave de liderazgo. | bytes |
| key | key es una clave opaca que representa la propiedad de la elección. Si la clave se elimina, se pierde el liderazgo. | bytes |
| rev | rev es la revisión de creación de la clave. Puede usarse para comprobar la propiedad de una elección durante transacciones verificando que la revisión de creación de la clave coincida con rev. | int64 |
| lease | lease es el ID de la concesión del líder de la elección. | int64 |

##### message `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name | name es el identificador de la elección para la información del liderazgo. | bytes |

##### message `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv es el par clave-valor que representa la última actualización del líder. | mvccpb.KeyValue |

##### message `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| leader | leader es la retención del liderazgo sobre la elección. | LeaderKey |
| value | value es una actualización destinada a sobrescribir el valor actual del líder. | bytes |

##### message `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### message `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| leader | leader es el liderazgo que se abandona al renunciar. | LeaderKey |

##### message `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### message `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| type | type es el tipo de evento. Si type es un PUT, indica que se han almacenado nuevos datos en la clave. Si type es un DELETE, indica que la clave fue eliminada. | EventType |
| kv | kv contiene el KeyValue del evento. Un evento PUT contiene el par kv actual. Un evento PUT con kv.Version=1 indica la creación de una clave. Un evento DELETE/EXPIRE contiene la clave eliminada con su revisión de modificación establecida en la revisión de la eliminación. | KeyValue |
| prev_kv | prev_kv contiene el par clave-valor existente antes de que ocurra el evento. | KeyValue |

##### message `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| key | key es la clave en bytes. No se permite una clave vacía. | bytes |
| create_revision | create_revision es la revisión de la última creación de esta clave. | int64 |
| mod_revision | mod_revision es la revisión de la última modificación de esta clave. | int64 |
| version | version es la versión de la clave. Una eliminación restablece la versión a cero y cualquier modificación de la clave incrementa su versión. | int64 |
| value | value es el valor que contiene la clave, en bytes. | bytes |
| lease | lease es el ID de la concesión adjunta a la clave. Cuando la concesión adjunta expira, la clave se eliminará. Si lease es 0, no hay ninguna concesión adjunta a la clave. | int64 |
