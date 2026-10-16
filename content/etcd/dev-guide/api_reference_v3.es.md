---
title: Referencia de API
weight: 3800
description: "Referencia completa de la API v3 de etcd"
categories: [Referencia]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

Esta referencia de API se genera automáticamente a partir de los archivos `.proto` nombrados.

##### service `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable activa la autenticación. |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable desactiva la autenticación. |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus muestra el estado de la autenticación. |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate procesa una solicitud de autenticación. |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd añade un usuario nuevo. El nombre de usuario no puede estar vacío. |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet obtiene información detallada del usuario. |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList obtiene una lista de todos los usuarios. |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete elimina un usuario especificado. |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword cambia la contraseña de un usuario especificado. |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrantRole otorga un rol a un usuario especificado. |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole revoca un rol de un usuario especificado. |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd añade un rol nuevo. El nombre del rol no puede estar vacío. |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet obtiene información detallada del rol. |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList obtiene listas de todos los roles. |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete elimina un rol especificado. |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission otorga a un rol especificado un permiso sobre una clave o un rango especificados. |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission revoca un permiso de clave o de rango de un rol especificado. |

##### service `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd añade un miembro al clúster. |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove elimina del clúster un miembro existente. |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate actualiza la configuración del miembro. |
| MemberList | MemberListRequest | MemberListResponse | MemberList enumera todos los miembros del clúster. |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote asciende a un miembro de aprendiz de raft (sin derecho a voto) a miembro de raft con derecho a voto. |

##### service `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range obtiene del almacén clave-valor las claves del rango. |
| Put | PutRequest | PutResponse | Put coloca la clave dada en el almacén clave-valor. Una solicitud put incrementa la revisión del almacén clave-valor y genera un evento en el historial de eventos. |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange elimina del almacén clave-valor el rango dado. Una solicitud delete incrementa la revisión del almacén clave-valor y genera un evento de eliminación en el historial de eventos por cada clave eliminada. |
| Txn | TxnRequest | TxnResponse | Txn procesa múltiples solicitudes en una sola transacción. Una solicitud txn incrementa la revisión del almacén clave-valor y genera eventos con la misma revisión por cada solicitud completada. No está permitido modificar la misma clave varias veces dentro de un txn. |
| Compact | CompactionRequest | CompactionResponse | Compact compacta el historial de eventos del almacén clave-valor de etcd. El almacén clave-valor debería compactarse periódicamente o el historial de eventos seguirá creciendo indefinidamente. |

##### service `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant crea una concesión que expira si el servidor no recibe un keepAlive dentro de un periodo de tiempo de vida dado. Todas las claves asociadas a la concesión expirarán y se eliminarán si la concesión expira. Cada clave expirada genera un evento de eliminación en el historial de eventos. |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke revoca una concesión. Todas las claves asociadas a la concesión expirarán y se eliminarán. |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive mantiene viva la concesión enviando en flujo solicitudes de keep alive del cliente al servidor y respuestas de keep alive del servidor al cliente. |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive recupera información de la concesión. |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases enumera todas las concesiones existentes. |

##### service `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | Alarm activa, desactiva y consulta alarmas relativas a la salud del clúster. |
| Status | StatusRequest | StatusResponse | Status obtiene el estado del miembro. |
| Defragment | DefragmentRequest | DefragmentResponse | Defragment desfragmenta la base de datos backend de un miembro para recuperar espacio de almacenamiento. |
| Hash | HashRequest | HashResponse | Hash calcula el hash de todo el espacio de claves del backend, incluidos los buckets key, lease y otros del almacenamiento. ¡Esto está diseñado SOLO para pruebas! No dependas de esto en producción con transacciones en curso, ya que la operación Hash no mantiene bloqueos MVCC. Usa en su lugar la API «HashKV» para comprobaciones de consistencia del bucket «key». |
| HashKV | HashKVRequest | HashKVResponse | HashKV calcula el hash de todas las claves MVCC hasta una revisión dada. Solo itera el bucket «key» del almacenamiento backend. |
| Snapshot | SnapshotRequest | SnapshotResponse | Snapshot envía una instantánea de todo el backend de un miembro a un cliente mediante un flujo. |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | MoveLeader solicita al nodo líder actual que transfiera su liderazgo al destinatario. |
| Downgrade | DowngradeRequest | DowngradeResponse | Downgrade solicita degradaciones, verifica la viabilidad o cancela la degradación de la versión del clúster. Soportado desde etcd 3.5. |

##### service `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| Método | Tipo de solicitud | Tipo de respuesta | Descripción |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watch observa eventos que están ocurriendo o que ya han ocurrido. Tanto la entrada como la salida son flujos; el flujo de entrada sirve para crear y cancelar observadores y el flujo de salida envía eventos. Una RPC de watch puede observar varios rangos de claves, enviando en flujo eventos de varias observaciones a la vez. Se puede observar todo el historial de eventos comenzando por la última revisión de compactación. |

##### message `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID es el ID del miembro asociado a la alarma generada. | uint64 |
| alarm | alarm es el tipo de alarma que se ha generado. | AlarmType |

##### message `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action es el tipo de solicitud de alarma que se va a emitir. La acción puede obtener (GET) los estados de alarma, activar (ACTIVATE) una alarma o desactivar (DEACTIVATE) una alarma generada. | AlarmAction |
| memberID | memberID es el ID del miembro asociado a la alarma. Si memberID es 0, la solicitud de alarma cubre a todos los miembros. | uint64 |
| alarm | alarm es el tipo de alarma a considerar para esta solicitud. | AlarmType |

##### message `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms es una lista de alarmas asociadas a la solicitud de alarma. | (slice of) AlarmMember |

##### message `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name es el nombre del rol que se va a añadir al sistema de autenticación. | string |

##### message `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### message `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### message `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (slice of) authpb.Permission |

##### message `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name es el nombre del rol al que se otorgará el permiso. | string |
| perm | perm es el permiso que se otorga al rol. | authpb.Permission |

##### message `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### message `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### message `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision es la revisión actual del almacén de autenticación | uint64 |

##### message `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### message `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name es el nombre del usuario cuya contraseña se está cambiando. | string |
| password | password es la contraseña nueva del usuario. Ten en cuenta que este campo se eliminará en la capa de API. | string |
| hashedPassword | hashedPassword es la nueva contraseña con hash del usuario. Ten en cuenta que este campo se inicializará en la capa de API. | string |

##### message `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name es el nombre del usuario que se va a eliminar. | string |

##### message `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### message `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### message `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user es el nombre del usuario al que se le debe otorgar un rol determinado. | string |
| role | role es el nombre del rol que se otorga al usuario. | string |

##### message `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (slice of) string |

##### message `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### message `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### message `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | token es un token autorizado que puede usarse en RPC posteriores | string |

##### message `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequest compacta el almacén clave-valor hasta una revisión dada. Todas las claves sustituidas con una revisión menor que la revisión de compactación se eliminarán.

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision es la revisión del almacén clave-valor para la operación de compactación. | int64 |
| physical | physical se establece para que la RPC espere hasta que la compactación se aplique físicamente a la base de datos local, de modo que las entradas compactadas se eliminen totalmente de la base de datos backend. | bool |

##### message `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result es la operación lógica de comparación para esta comparación. | CompareResult |
| target | target es el campo clave-valor que se va a inspeccionar para la comparación. | CompareTarget |
| key | key es la clave objeto de la operación de comparación. | bytes |
| target_union |  | oneof |
| version | version es la versión de la clave dada | int64 |
| create_revision | create_revision es la revisión de creación de la clave dada | int64 |
| mod_revision | mod_revision es la última revisión modificada de la clave dada. | int64 |
| value | value es el valor de la clave dada, en bytes. | bytes |
| lease | lease es el ID de concesión de la clave dada. | int64 |
| range_end | range_end compara el objetivo dado con todas las claves del rango [key, range_end). Consulta RangeRequest para más detalles sobre los rangos de claves. | bytes |

##### message `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key es la primera clave que se va a eliminar del rango. | bytes |
| range_end | range_end es la clave siguiente a la última clave que se va a eliminar para el rango [key, range_end). Si no se proporciona range_end, el rango se define para contener solo el argumento key. Si range_end es la clave dada más uno, el rango son todas las claves con el prefijo (la clave dada). Si range_end es '\0', el rango son todas las claves mayores o iguales que el argumento key. | bytes |
| prev_kv | Si prev_kv está establecido, etcd obtiene los pares clave-valor anteriores antes de eliminarlos. Los pares clave-valor anteriores se devolverán en la respuesta de eliminación. | bool |

##### message `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted es el número de claves eliminadas por la solicitud de eliminación de rango. | int64 |
| prev_kvs | si prev_kv está establecido en la solicitud, se devolverán los pares clave-valor anteriores. | (slice of) mvccpb.KeyValue |

##### message `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| enabled | enabled indica si el clúster está habilitado para degradarse. | bool |
| targetVersion | targetVersion es la versión objetivo de la degradación. | string |

##### message `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action es el tipo de solicitud de degradación que se va a emitir. La acción puede validar (VALIDATE) la versión objetivo, reducir (DOWNGRADE) la versión del clúster o cancelar (CANCEL) el trabajo de degradación actual. | DowngradeAction |
| version | version es la versión objetivo a la que degradar. | string |

##### message `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version es la versión actual del clúster. | string |

##### message `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequest se usa solo para pruebas. La versión de esta solicitud se leerá como la versión del registro WAL. Si la versión objetivo de degradación es menor que esta versión, la degradación (con el servidor en funcionamiento) o la migración (con el servidor detenido) no es segura, por lo que no debería permitirse.

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### message `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision es la revisión del almacén clave-valor para la operación de hash. | int64 |

##### message `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash es el valor de hash calculado a partir de las claves MVCC del miembro que responde hasta una revisión dada. | uint32 |
| compact_revision | compact_revision es la revisión compactada del almacén clave-valor cuando comienza el hash. | int64 |
| hash_revision | hash_revision es la revisión hasta la cual se calcula el hash. | int64 |

##### message `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash es el valor de hash calculado a partir del backend de KV del miembro que responde. | uint32 |

##### message `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de la concesión a la que se va a aplicar el checkpoint. | int64 |
| remaining_TTL | Remaining_TTL es el tiempo restante hasta la expiración de la concesión. | int64 |

##### message `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice of) LeaseCheckpoint |

##### message `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL es el tiempo de vida orientativo en segundos. Una concesión expirada devolverá -1. | int64 |
| ID | ID es el ID solicitado para la concesión. Si ID se establece en 0, el otorgante elige un ID. | int64 |

##### message `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID es el ID de la concesión otorgada. | int64 |
| TTL | TTL es el tiempo de vida de la concesión elegido por el servidor, en segundos. | int64 |
| error |  | string |

##### message `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de la concesión que se va a mantener viva. | int64 |

##### message `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID es el ID de la concesión de la solicitud de keep alive. | int64 |
| TTL | TTL es el nuevo tiempo de vida de la concesión. | int64 |

##### message `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (slice of) LeaseStatus |

##### message `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de la concesión que se va a revocar. Cuando se revoca el ID, todas las claves asociadas se eliminarán. | int64 |

##### message `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### message `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de la concesión. | int64 |
| keys | keys es true para consultar todas las claves asociadas a esta concesión. | bool |

##### message `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID es el ID de la concesión de la solicitud de keep alive. | int64 |
| TTL | TTL es el TTL restante en segundos para la concesión; la concesión expirará en menos de TTL+1 segundos. | int64 |
| grantedTTL | GrantedTTL es el tiempo inicial otorgado en segundos al crearse o renovarse la concesión. | int64 |
| keys | Keys es la lista de claves asociadas a esta concesión. | (slice of) bytes |

##### message `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de miembro de este miembro. | uint64 |
| name | name es el nombre legible por humanos del miembro. Si el miembro no está iniciado, el nombre será una cadena vacía. | string |
| peerURLs | peerURLs es la lista de URLs que el miembro expone al clúster para la comunicación. | (slice of) string |
| clientURLs | clientURLs es la lista de URLs que el miembro expone a los clientes para la comunicación. Si el miembro no está iniciado, clientURLs estará vacía. | (slice of) string |
| isLearner | isLearner indica si el miembro es aprendiz de raft. | bool |

##### message `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs es la lista de URLs que el miembro añadido usará para comunicarse con el clúster. | (slice of) string |
| isLearner | isLearner indica si el miembro añadido es aprendiz de raft. | bool |

##### message `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member es la información del miembro del miembro añadido. | Member |
| members | members es una lista de todos los miembros tras añadir el miembro nuevo. | (slice of) Member |

##### message `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### message `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members es una lista de todos los miembros asociados al clúster. | (slice of) Member |

##### message `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de miembro del miembro que se va a ascender. | uint64 |

##### message `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members es una lista de todos los miembros tras ascender al miembro. | (slice of) Member |

##### message `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de miembro del miembro que se va a eliminar. | uint64 |

##### message `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members es una lista de todos los miembros tras eliminar al miembro. | (slice of) Member |

##### message `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID es el ID de miembro del miembro que se va a actualizar. | uint64 |
| peerURLs | peerURLs es la lista nueva de URLs que el miembro usará para comunicarse con el clúster. | (slice of) string |

##### message `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members es una lista de todos los miembros tras actualizar al miembro. | (slice of) Member |

##### message `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID es el ID de nodo del nuevo líder. | uint64 |

##### message `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key es la clave, en bytes, que se va a poner en el almacén clave-valor. | bytes |
| value | value es el valor, en bytes, que se va a asociar con la clave en el almacén clave-valor. | bytes |
| lease | lease es el ID de concesión que se va a asociar con la clave en el almacén clave-valor. Un valor de lease de 0 indica que no hay concesión. | int64 |
| prev_kv | Si prev_kv está establecido, etcd obtiene el par clave-valor anterior antes de cambiarlo. El par clave-valor anterior se devolverá en la respuesta de put. | bool |
| ignore_value | Si ignore_value está establecido, etcd actualiza la clave usando su valor actual. Devuelve un error si la clave no existe. | bool |
| ignore_lease | Si ignore_lease está establecido, etcd actualiza la clave usando su concesión actual. Devuelve un error si la clave no existe. | bool |

##### message `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | si prev_kv está establecido en la solicitud, se devolverá el par clave-valor anterior. | mvccpb.KeyValue |

##### message `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key es la primera clave del rango. Si no se proporciona range_end, la solicitud solo busca key. | bytes |
| range_end | range_end es el límite superior del rango solicitado [key, range_end). Si range_end es '\0', el rango son todas las claves >= key. Si range_end es la clave más uno (p. ej., "aa"+1 == "ab", "a\xff"+1 == "b"), la solicitud de rango obtiene todas las claves con el prefijo key. Si tanto key como range_end son '\0', la solicitud de rango devuelve todas las claves. | bytes |
| limit | limit es un límite en el número de claves devueltas para la solicitud. Cuando limit se establece en 0, se trata como sin límite. | int64 |
| revision | revision es el punto en el tiempo del almacén clave-valor que se va a usar para el rango. Si revision es menor o igual que cero, el rango se realiza sobre el almacén clave-valor más reciente. Si la revisión se ha compactado, se devuelve ErrCompacted como respuesta. | int64 |
| sort_order | sort_order es el orden de los resultados ordenados devueltos. | SortOrder |
| sort_target | sort_target es el campo clave-valor que se va a usar para la ordenación. | SortTarget |
| serializable | serializable hace que la solicitud de rango use lecturas serializables locales al miembro. Las solicitudes de rango son linealizables por defecto; las solicitudes linealizables tienen mayor latencia y menor caudal de solicitudes que las solicitudes serializables, pero reflejan el consenso actual del clúster. Para obtener mejor rendimiento, a cambio de posibles lecturas obsoletas, una solicitud de rango serializable se atiende localmente sin necesidad de alcanzar consenso con los demás nodos del clúster. | bool |
| keys_only | keys_only, cuando se establece, devuelve solo las claves y no los valores. | bool |
| count_only | count_only, cuando se establece, devuelve solo el recuento de las claves del rango. | bool |
| min_mod_revision | min_mod_revision es el límite inferior para las revisiones de modificación de las claves devueltas; todas las claves con revisiones de modificación menores se excluirán. | int64 |
| max_mod_revision | max_mod_revision es el límite superior para las revisiones de modificación de las claves devueltas; todas las claves con revisiones de modificación mayores se excluirán. | int64 |
| min_create_revision | min_create_revision es el límite inferior para las revisiones de creación de las claves devueltas; todas las claves con revisiones de creación menores se excluirán. | int64 |
| max_create_revision | max_create_revision es el límite superior para las revisiones de creación de las claves devueltas; todas las claves con revisiones de creación mayores se excluirán. | int64 |

##### message `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs es la lista de pares clave-valor que coinciden con la solicitud de rango. kvs está vacía cuando se solicita el recuento. | (slice of) mvccpb.KeyValue |
| more | more indica si hay más claves que devolver en el rango solicitado. | bool |
| count | count se establece con el número real de claves dentro del rango cuando se solicita. A diferencia de Kvs, no se ve afectado por límites ni filtros (p. ej., Min/Max, Create/Modify, Revisions) y refleja el recuento completo dentro del rango especificado. | int64 |

##### message `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request es una unión de tipos de solicitud aceptados por una transacción. | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### message `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id es el ID del clúster que envió la respuesta. | uint64 |
| member_id | member_id es el ID del miembro que envió la respuesta. | uint64 |
| revision | revision es la revisión del almacén clave-valor cuando se aplicó la solicitud, y no está establecida (por lo tanto, 0) en el caso de llamadas que no interactúan con el almacén clave-valor. Para las respuestas de progreso de watch, header.revision indica el progreso. Se garantiza que todos los eventos futuros recibidos en este flujo tengan un número de revisión mayor que el número de header.revision. | int64 |
| raft_term | raft_term es el término de raft cuando se aplicó la solicitud. | uint64 |

##### message `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response es una unión de tipos de respuesta devueltos por una transacción. | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### message `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header contiene la información actual del almacén clave-valor. El primer header del flujo de la instantánea indica el punto en el tiempo de la instantánea. | ResponseHeader |
| remaining_bytes | remaining_bytes es el número de bytes del blob que se enviarán después de este mensaje | uint64 |
| blob | blob contiene el siguiente fragmento de la instantánea en el flujo de la instantánea. | bytes |
| version | Versión del esquema de almacenamiento registrada en la instantánea. Se lee del backend local del miembro y puede diferir de su versión binaria. Indica qué versión de almacenamiento de etcd debe admitirse al restaurar la instantánea. | string |

##### message `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version es la versión binaria del miembro de etcd que responde. La versión del esquema de almacenamiento se informa por separado en storageVersion. | string |
| dbSize | dbSize es el tamaño, en bytes, de la base de datos backend físicamente asignada del miembro que responde. | int64 |
| leader | leader es el ID del miembro que, según el miembro que responde, es el líder actual. | uint64 |
| raftIndex | raftIndex es el índice confirmado actual de raft del miembro que responde. | uint64 |
| raftTerm | raftTerm es el término actual de raft del miembro que responde. | uint64 |
| raftAppliedIndex | raftAppliedIndex es el índice aplicado actual de raft del miembro que responde. | uint64 |
| errors | errors contiene información y estado de alarmas/salud. | (slice of) string |
| dbSizeInUse | dbSizeInUse es el tamaño, en bytes, de la base de datos backend lógicamente en uso del miembro que responde. | int64 |
| isLearner | isLearner indica si el miembro es aprendiz de raft. | bool |
| storageVersion | storageVersion es la versión del archivo de la base de datos. Podría actualizarse con retraso en relación con la versión objetivo del clúster. | string |
| dbSizeQuota | dbSizeQuota es la cuota de almacenamiento de etcd configurada en bytes (el valor pasado a la instancia de etcd mediante la opción --quota-backend-bytes) | int64 |
| downgradeInfo | downgradeInfo indica si hay un proceso de degradación. | DowngradeInfo |

##### message `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

Del artículo de Google sobre paxosdb: Nuestra implementación gira en torno a una primitiva potente que llamamos MultiOp. Todas las demás operaciones de la base de datos, excepto la iteración, se implementan como una única llamada a MultiOp. Un MultiOp se aplica de forma atómica y consta de tres componentes: 1. Una lista de pruebas llamada guard. Cada prueba de guard comprueba una única entrada de la base de datos. Puede comprobar la ausencia o la presencia de un valor, o comparar con un valor dado. Dos pruebas diferentes de guard pueden aplicarse a la misma entrada o a entradas diferentes de la base de datos. Se aplican todas las pruebas de guard y MultiOp devuelve los resultados. Si todas las pruebas son verdaderas, MultiOp ejecuta t op (consulta el elemento 2 más abajo); de lo contrario, ejecuta f op (consulta el elemento 3 más abajo). 2. Una lista de operaciones de base de datos llamada t op. Cada operación de la lista es una operación de inserción, eliminación o búsqueda, y se aplica a una única entrada de la base de datos. Dos operaciones diferentes de la lista pueden aplicarse a la misma entrada o a entradas diferentes de la base de datos. Estas operaciones se ejecutan si guard se evalúa como true. 3. Una lista de operaciones de base de datos llamada f op. Como t op, pero se ejecuta si guard se evalúa como false.

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare es una lista de predicados que representan una conjunción de términos. Si las comparaciones tienen éxito, las solicitudes de éxito se procesarán en orden y la respuesta contendrá sus respuestas respectivas en orden. Si las comparaciones fallan, las solicitudes de fallo se procesarán en orden y la respuesta contendrá sus respuestas respectivas en orden. | (slice of) Compare |
| success | success es una lista de solicitudes que se aplicarán cuando compare se evalúe como true. | (slice of) RequestOp |
| failure | failure es una lista de solicitudes que se aplicarán cuando compare se evalúe como false. | (slice of) RequestOp |

##### message `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | succeeded se establece en true si compare se evaluó como true, o en false en caso contrario. | bool |
| responses | responses es una lista de respuestas correspondientes a los resultados de aplicar success si succeeded es true, o failure si succeeded es false. | (slice of) ResponseOp |

##### message `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id es el ID del observador que se va a cancelar para que no se transmitan más eventos. | int64 |

##### message `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key es la clave que se va a registrar para observar. | bytes |
| range_end | range_end es el final del rango [key, range_end) que se va a observar. Si no se proporciona range_end, solo se observa el argumento key. Si range_end es igual a '\0', se observan todas las claves mayores o iguales que el argumento key. Si range_end es la clave dada más uno, se observarán todas las claves con el prefijo (la clave dada). | bytes |
| start_revision | start_revision es una revisión opcional desde la que observar (inclusive). Si no se especifica start_revision, es «ahora». | int64 |
| progress_notify | progress_notify se establece para que el servidor etcd envíe periódicamente una WatchResponse sin eventos al observador nuevo si no hay eventos recientes. Es útil cuando los clientes desean recuperar un observador desconectado a partir de una revisión conocida reciente. El servidor etcd puede decidir con qué frecuencia enviará notificaciones según la carga actual. | bool |
| filters | filters filtra los eventos en el lado del servidor antes de enviarlos de vuelta al observador. | (slice of) FilterType |
| prev_kv | Si prev_kv está establecido, el observador creado obtiene el KV anterior antes de que ocurra el evento. Si el KV anterior ya está compactado, no se devolverá nada. | bool |
| watch_id | Si se proporciona watch_id y es distinto de cero, se asignará a este observador. Como crear un observador en etcd no es una operación síncrona, esto puede usarse para asegurar que el orden sea correcto al crear varios observadores en el mismo flujo. Crear un observador con un ID ya en uso en el flujo provocará que se devuelva un error. | int64 |
| fragment | fragment permite dividir revisiones grandes en múltiples respuestas de watch. | bool |

##### message `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

Solicita que el estado de progreso de un flujo de observación se envíe en el flujo de respuestas de watch lo antes posible.

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union es una solicitud para crear un observador nuevo o cancelar un observador existente. | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### message `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id es el ID del observador que corresponde a la respuesta. | int64 |
| created | created se establece en true si la respuesta corresponde a una solicitud de creación de watch. El cliente debería registrar el watch_id y esperar recibir eventos para el observador creado desde el mismo flujo. Todos los eventos enviados al observador creado se adjuntarán con el mismo watch_id. | bool |
| canceled | canceled se establece en true si la respuesta corresponde a una solicitud de cancelación de watch o si start_revision ya se ha compactado. No se enviarán más eventos al observador cancelado. | bool |
| compact_revision | compact_revision se establece en el índice mínimo si un observador intenta observar en un índice compactado. Esto ocurre al crear un observador en una revisión compactada o cuando el observador no puede ponerse al día con el progreso del almacén clave-valor. El cliente debería tratar el observador como cancelado y no debería intentar crear de nuevo ningún observador con la misma start_revision. | int64 |
| cancel_reason | cancel_reason indica el motivo de la cancelación del observador. | string |
| fragment | fragment es true si una respuesta de watch grande se dividió en múltiples respuestas. | bool |
| events |  | (slice of) mvccpb.Event |

##### message `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| type | type es el tipo de evento. Si type es un PUT, indica que se han almacenado datos nuevos en la clave. Si type es un DELETE, indica que la clave fue eliminada. | EventType |
| kv | kv contiene el KeyValue del evento. Un evento PUT contiene el par kv actual. Un evento PUT con kv.Version=1 indica la creación de una clave. Un evento DELETE/EXPIRE contiene la clave eliminada con su revisión de modificación establecida en la revisión de la eliminación. | KeyValue |
| prev_kv | prev_kv contiene el par clave-valor anterior a que ocurra el evento. | KeyValue |

##### message `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| key | key es la clave en bytes. No se permite una clave vacía. | bytes |
| create_revision | create_revision es la revisión de la última creación de esta clave. | int64 |
| mod_revision | mod_revision es la revisión de la última modificación de esta clave. | int64 |
| version | version es la versión de la clave. Una eliminación restablece la versión a cero y cualquier modificación de la clave incrementa su versión. | int64 |
| value | value es el valor que contiene la clave, en bytes. | bytes |
| lease | lease es el ID de la concesión asociada a la clave. Cuando la concesión asociada expira, la clave se eliminará. Si lease es 0, no hay ninguna concesión asociada a la clave. | int64 |

##### message `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### message `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### message `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### message `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Permission es una entidad única

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### message `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Role es una entrada única en el bucket authRoles

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (slice of) Permission |

##### message `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

User es una entrada única en el bucket authUsers

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (slice of) string |
| options |  | UserAddOptions |

##### message `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| Campo | Descripción | Tipo |
| ----- | ----------- | ---- |
| no_password |  | bool |
