---
title: Справочник API
weight: 3800
description: "Полный справочник API etcd v3"
categories: [Справочник]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

Этот справочник API автоматически создан из указанных файлов `.proto`.

##### Служба `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable включает аутентификацию. |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable отключает аутентификацию. |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus отображает состояние аутентификации. |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate обрабатывает запрос аутентификации. |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd добавляет нового пользователя. Имя пользователя не может быть пустым. |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet получает подробные сведения о пользователе. |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList получает список всех пользователей. |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete удаляет указанного пользователя. |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword изменяет пароль указанного пользователя. |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrantRole предоставляет указанному пользователю роль. |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole отзывает роль указанного пользователя. |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd добавляет новую роль. Имя роли не может быть пустым. |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet получает подробные сведения о роли. |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList получает список всех ролей. |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete удаляет указанную роль. |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission предоставляет указанной роли разрешение на заданный ключ или диапазон. |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission отзывает у указанной роли разрешение на ключ или диапазон. |

##### Служба `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd добавляет участника в кластер. |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove удаляет существующего участника из кластера. |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate обновляет конфигурацию участника. |
| MemberList | MemberListRequest | MemberListResponse | MemberList перечисляет всех участников кластера. |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote повышает обучающегося участника raft без права голоса до участника raft с правом голоса. |

##### Служба `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range получает ключи диапазона из хранилища ключей и значений. |
| Put | PutRequest | PutResponse | Put помещает заданный ключ в хранилище ключей и значений. Запрос put увеличивает ревизию хранилища и создаёт одно событие в истории событий. |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange удаляет заданный диапазон из хранилища ключей и значений. Запрос удаления увеличивает ревизию хранилища и создаёт событие удаления в истории для каждого удалённого ключа. |
| Txn | TxnRequest | TxnResponse | Txn обрабатывает несколько запросов в одной транзакции. Запрос txn увеличивает ревизию хранилища ключей и значений и создаёт события с одной ревизией для каждого выполненного запроса. Многократное изменение одного ключа в одной txn недопустимо. |
| Compact | CompactionRequest | CompactionResponse | Compact компактизирует историю событий в хранилище ключей и значений etcd. Хранилище следует периодически компактизировать, иначе история событий будет расти бесконечно. |

##### Служба `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant создаёт аренду, которая истекает, если сервер не получает keepAlive в течение заданного срока жизни. При истечении аренды все присоединённые к ней ключи истекают и удаляются. Каждый истёкший ключ создаёт событие удаления в истории событий. |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke отзывает аренду. Все присоединённые к ней ключи истекают и удаляются. |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive поддерживает аренду активной, передавая потоком запросы поддержания активности от клиента серверу и ответы от сервера клиенту. |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive получает сведения об аренде. |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases перечисляет все существующие аренды. |

##### Служба `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | Alarm активирует, деактивирует и запрашивает аварийные сигналы о состоянии кластера. |
| Status | StatusRequest | StatusResponse | Status получает состояние участника. |
| Defragment | DefragmentRequest | DefragmentResponse | Defragment дефрагментирует базу данных бэкенда участника для освобождения места. |
| Hash | HashRequest | HashResponse | Hash вычисляет хеш всего пространства ключей бэкенда, включая сегменты key, lease и другие сегменты хранилища. Предназначено ТОЛЬКО для тестирования! Не полагайтесь на операцию в рабочей среде с текущими транзакциями, поскольку Hash не удерживает блокировки MVCC. Для проверки согласованности сегмента "key" используйте API "HashKV". |
| HashKV | HashKVRequest | HashKVResponse | HashKV вычисляет хеш всех ключей MVCC до заданной ревизии. Перебирает только сегмент "key" в хранилище бэкенда. |
| Snapshot | SnapshotRequest | SnapshotResponse | Snapshot передаёт снимок всего бэкенда от участника клиенту потоком. |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | MoveLeader запрашивает у текущего узла-лидера передачу лидерства назначенному узлу. |
| Downgrade | DowngradeRequest | DowngradeResponse | Downgrade запрашивает понижение версии, проверяет его допустимость или отменяет его для версии кластера. Поддерживается начиная с etcd 3.5. |

##### Служба `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| Метод | Тип запроса | Тип ответа | Описание |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watch наблюдает за происходящими или уже произошедшими событиями. Ввод и вывод являются потоками: входной поток создаёт и отменяет наблюдателей, выходной отправляет события. Один RPC watch может наблюдать несколько диапазонов ключей и одновременно передавать события нескольких наблюдений. Всю историю событий можно наблюдать с последней ревизии компактизации. |

##### Сообщение `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID — идентификатор участника, связанного с активированным аварийным сигналом. | uint64 |
| alarm | alarm — тип активированного аварийного сигнала. | AlarmType |

##### Сообщение `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action — тип отправляемого запроса аварийного сигнала. Действие может запрашивать состояния сигналов (GET), активировать сигнал (ACTIVATE) или отключать активированный сигнал (DEACTIVATE). | AlarmAction |
| memberID | memberID — идентификатор участника, связанного с сигналом. Если memberID равен 0, запрос относится ко всем участникам. | uint64 |
| alarm | alarm — тип аварийного сигнала, рассматриваемого запросом. | AlarmType |

##### Сообщение `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms — список аварийных сигналов, связанных с запросом. | (slice of) AlarmMember |

##### Сообщение `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name — имя роли, добавляемой в систему аутентификации. | string |

##### Сообщение `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### Сообщение `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### Сообщение `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (slice of) authpb.Permission |

##### Сообщение `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name — имя роли, которой будет предоставлено разрешение. | string |
| perm | perm — разрешение, предоставляемое роли. | authpb.Permission |

##### Сообщение `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### Сообщение `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### Сообщение `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision — текущая ревизия хранилища аутентификации | uint64 |

##### Сообщение `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### Сообщение `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name — имя пользователя, пароль которого изменяется. | string |
| password | password — новый пароль пользователя. Обратите внимание: это поле будет удалено на уровне API. | string |
| hashedPassword | hashedPassword — новый хешированный пароль пользователя. Обратите внимание: это поле будет инициализировано на уровне API. | string |

##### Сообщение `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name — имя удаляемого пользователя. | string |

##### Сообщение `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### Сообщение `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (slice of) string |

##### Сообщение `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user — имя пользователя, которому следует предоставить указанную роль. | string |
| role | role — имя роли, предоставляемой пользователю. | string |

##### Сообщение `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (slice of) string |

##### Сообщение `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### Сообщение `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### Сообщение `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | token — авторизованный токен, который можно использовать в последующих RPC | string |

##### Сообщение `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequest компактизирует хранилище ключей и значений до заданной ревизии. Все замещённые ключи с ревизией меньше ревизии компактизации удаляются.

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision — ревизия хранилища ключей и значений для операции компактизации. | int64 |
| physical | physical задаётся, чтобы RPC дождался физического применения компактизации к локальной базе данных и полного удаления компактизированных записей из базы данных бэкенда. | bool |

##### Сообщение `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result — логическая операция данного сравнения. | CompareResult |
| target | target — поле пары «ключ — значение», проверяемое при сравнении. | CompareTarget |
| key | key — целевой ключ операции сравнения. | bytes |
| target_union |  | oneof |
| version | version — версия заданного ключа | int64 |
| create_revision | create_revision — ревизия создания заданного ключа | int64 |
| mod_revision | mod_revision — ревизия последнего изменения заданного ключа. | int64 |
| value | value — значение заданного ключа в байтах. | bytes |
| lease | lease — идентификатор аренды заданного ключа. | int64 |
| range_end | range_end сравнивает заданную цель со всеми ключами диапазона [key, range_end). Подробнее о диапазонах ключей см. RangeRequest. | bytes |

##### Сообщение `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key — первый удаляемый ключ диапазона. | bytes |
| range_end | range_end — ключ, следующий за последним удаляемым ключом диапазона [key, range_end). Если range_end не задан, диапазон содержит только аргумент key. Если range_end равен заданному ключу плюс один, диапазон содержит все ключи с префиксом заданного ключа. Если range_end равен '\0', диапазон содержит все ключи, большие либо равные аргументу key. | bytes |
| prev_kv | Если prev_kv задан, etcd получает предыдущие пары «ключ — значение» перед удалением. Они возвращаются в ответе удаления. | bool |

##### Сообщение `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted — количество ключей, удалённых запросом удаления диапазона. | int64 |
| prev_kvs | если в запросе задан prev_kv, возвращаются предыдущие пары «ключ — значение». | (slice of) mvccpb.KeyValue |

##### Сообщение `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| enabled | enabled указывает, включено ли понижение версии кластера. | bool |
| targetVersion | targetVersion — целевая версия понижения. | string |

##### Сообщение `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action — тип отправляемого запроса понижения версии. Действие может проверять целевую версию (VALIDATE), понижать версию кластера (DOWNGRADE) или отменять текущую задачу понижения (CANCEL). | DowngradeAction |
| version | version — целевая версия понижения. | string |

##### Сообщение `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version — текущая версия кластера. | string |

##### Сообщение `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequest используется только для тестирования. Версия в запросе читается как версия записи WAL. Если целевая версия понижения меньше этой версии, понижение (online) или миграция (offline) небезопасны и не должны разрешаться.

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### Сообщение `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision — ревизия хранилища ключей и значений для операции хеширования. | int64 |

##### Сообщение `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash — значение хеша, вычисленное по ключам MVCC отвечающего участника до заданной ревизии. | uint32 |
| compact_revision | compact_revision — компактизированная ревизия хранилища ключей и значений в момент начала хеширования. | int64 |
| hash_revision | hash_revision — ревизия, до которой вычислен хеш. | int64 |

##### Сообщение `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash — значение хеша, вычисленное по бэкенду KV отвечающего участника. | uint32 |

##### Сообщение `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор аренды для контрольной точки. | int64 |
| remaining_TTL | Remaining_TTL — время, оставшееся до истечения аренды. | int64 |

##### Сообщение `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice of) LeaseCheckpoint |

##### Сообщение `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL — рекомендуемый срок жизни в секундах. Истёкшая аренда возвращает -1. | int64 |
| ID | ID — запрошенный идентификатор аренды. Если ID равен 0, арендодатель выбирает идентификатор. | int64 |

##### Сообщение `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID — идентификатор выданной аренды. | int64 |
| TTL | TTL — выбранный сервером срок жизни аренды в секундах. | int64 |
| error |  | string |

##### Сообщение `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор аренды, активность которой поддерживается. | int64 |

##### Сообщение `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID — идентификатор аренды из запроса поддержания активности. | int64 |
| TTL | TTL — новый срок жизни аренды. | int64 |

##### Сообщение `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (slice of) LeaseStatus |

##### Сообщение `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор отзываемой аренды. При отзыве ID все связанные ключи удаляются. | int64 |

##### Сообщение `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### Сообщение `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор аренды. | int64 |
| keys | keys равно true для запроса всех ключей, присоединённых к этой аренде. | bool |

##### Сообщение `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID — идентификатор аренды из запроса поддержания активности. | int64 |
| TTL | TTL — оставшийся срок жизни аренды в секундах; аренда истечёт менее чем через TTL+1 секунд. | int64 |
| grantedTTL | GrantedTTL — исходный выданный срок в секундах при создании или обновлении аренды. | int64 |
| keys | Keys — список ключей, присоединённых к аренде. | (slice of) bytes |

##### Сообщение `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор этого участника. | uint64 |
| name | name — понятное человеку имя участника. Если участник не запущен, имя является пустой строкой. | string |
| peerURLs | peerURLs — список URL, которые участник предоставляет кластеру для связи. | (slice of) string |
| clientURLs | clientURLs — список URL, которые участник предоставляет клиентам для связи. Если участник не запущен, clientURLs пуст. | (slice of) string |
| isLearner | isLearner указывает, является ли участник обучающимся участником raft. | bool |

##### Сообщение `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs — список URL, которые добавленный участник использует для связи с кластером. | (slice of) string |
| isLearner | isLearner указывает, является ли добавленный участник обучающимся участником raft. | bool |

##### Сообщение `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member — сведения о добавленном участнике. | Member |
| members | members — список всех участников после добавления нового. | (slice of) Member |

##### Сообщение `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### Сообщение `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members — список всех участников, связанных с кластером. | (slice of) Member |

##### Сообщение `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор повышаемого участника. | uint64 |

##### Сообщение `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members — список всех участников после повышения участника. | (slice of) Member |

##### Сообщение `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор удаляемого участника. | uint64 |

##### Сообщение `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members — список всех участников после удаления участника. | (slice of) Member |

##### Сообщение `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID — идентификатор обновляемого участника. | uint64 |
| peerURLs | peerURLs — новый список URL, которые участник использует для связи с кластером. | (slice of) string |

##### Сообщение `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members — список всех участников после обновления участника. | (slice of) Member |

##### Сообщение `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID — идентификатор узла нового лидера. | uint64 |

##### Сообщение `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Сообщение `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key — ключ в байтах, помещаемый в хранилище ключей и значений. | bytes |
| value | value — значение в байтах, связываемое с ключом в хранилище. | bytes |
| lease | lease — идентификатор аренды, связываемой с ключом. Значение аренды 0 означает отсутствие аренды. | int64 |
| prev_kv | Если prev_kv задан, etcd получает предыдущую пару «ключ — значение» перед её изменением. Она возвращается в ответе put. | bool |
| ignore_value | Если ignore_value задан, etcd обновляет ключ с его текущим значением. Если ключ не существует, возвращается ошибка. | bool |
| ignore_lease | Если ignore_lease задан, etcd обновляет ключ с его текущей арендой. Если ключ не существует, возвращается ошибка. | bool |

##### Сообщение `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | если в запросе задан prev_kv, возвращается предыдущая пара «ключ — значение». | mvccpb.KeyValue |

##### Сообщение `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key — первый ключ диапазона. Если range_end не задан, запрос ищет только key. | bytes |
| range_end | range_end — верхняя граница запрошенного диапазона [key, range_end). Если range_end равен '\0', диапазон содержит все ключи >= key. Если range_end равен key плюс один (например, "aa"+1 == "ab", "a\xff"+1 == "b"), запрос получает все ключи с префиксом key. Если и key, и range_end равны '\0', запрос возвращает все ключи. | bytes |
| limit | limit — ограничение количества ключей, возвращаемых запросом. Значение limit 0 означает отсутствие ограничения. | int64 |
| revision | revision — момент состояния хранилища ключей и значений для диапазона. Если revision меньше или равна нулю, диапазон относится к новейшему состоянию хранилища. Если ревизия компактизирована, возвращается ErrCompacted. | int64 |
| sort_order | sort_order — порядок возвращаемых отсортированных результатов. | SortOrder |
| sort_target | sort_target — поле пары «ключ — значение» для сортировки. | SortTarget |
| serializable | serializable задаёт использование сериализуемого локального чтения с участника для диапазонного запроса. По умолчанию запросы Range линеаризуемы; их задержка выше, а пропускная способность ниже, чем у сериализуемых запросов, зато они отражают текущий консенсус кластера. Ради повышения производительности ценой возможного чтения устаревших данных сериализуемый запрос обслуживается локально без достижения консенсуса с другими узлами. | bool |
| keys_only | если keys_only задан, возвращаются только ключи без значений. | bool |
| count_only | если count_only задан, возвращается только количество ключей в диапазоне. | bool |
| min_mod_revision | min_mod_revision — нижняя граница возвращаемых ревизий изменения ключей; ключи с меньшими ревизиями отфильтровываются. | int64 |
| max_mod_revision | max_mod_revision — верхняя граница возвращаемых ревизий изменения ключей; ключи с большими ревизиями отфильтровываются. | int64 |
| min_create_revision | min_create_revision — нижняя граница возвращаемых ревизий создания ключей; ключи с меньшими ревизиями отфильтровываются. | int64 |
| max_create_revision | max_create_revision — верхняя граница возвращаемых ревизий создания ключей; ключи с большими ревизиями отфильтровываются. | int64 |

##### Сообщение `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs — список пар «ключ — значение», соответствующих диапазонному запросу. При запросе count поле kvs пусто. | (slice of) mvccpb.KeyValue |
| more | more указывает, остались ли в запрошенном диапазоне ключи для возврата. | bool |
| count | при запросе count содержит фактическое количество ключей в диапазоне. В отличие от Kvs, оно не зависит от ограничений и фильтров (например, Min/Max, Create/Modify, Revisions) и отражает полное количество в указанном диапазоне. | int64 |

##### Сообщение `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request — объединение типов запросов, принимаемых транзакцией. | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### Сообщение `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id — идентификатор кластера, отправившего ответ. | uint64 |
| member_id | member_id — идентификатор участника, отправившего ответ. | uint64 |
| revision | revision — ревизия хранилища ключей и значений при применении запроса; для вызовов, не взаимодействующих с хранилищем, она не задана (то есть равна 0). В ответах о ходе наблюдения header.revision обозначает прогресс. Все последующие события в этом потоке гарантированно имеют номер ревизии выше номера header.revision. | int64 |
| raft_term | raft_term — срок полномочий raft при применении запроса. | uint64 |

##### Сообщение `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response — объединение типов ответов, возвращаемых транзакцией. | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### Сообщение `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header содержит текущие сведения о хранилище ключей и значений. Первый заголовок в потоке снимка указывает момент времени снимка. | ResponseHeader |
| remaining_bytes | remaining_bytes — количество байтов blob, отправляемых после этого сообщения | uint64 |
| blob | blob содержит следующий фрагмент снимка в потоке снимка. | bytes |
| version | Версия схемы хранилища, записанная в снимке. Она считывается из локального бэкенда участника и может отличаться от версии его двоичного файла. Указывает, какая версия хранилища etcd должна поддерживаться при восстановлении снимка. | string |

##### Сообщение `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version — версия двоичного файла отвечающего участника etcd. Версия схемы хранилища отдельно сообщается в storageVersion. | string |
| dbSize | dbSize — физически выделенный размер базы данных бэкенда отвечающего участника в байтах. | int64 |
| leader | leader — идентификатор участника, которого отвечающий участник считает текущим лидером. | uint64 |
| raftIndex | raftIndex — текущий зафиксированный индекс raft отвечающего участника. | uint64 |
| raftTerm | raftTerm — текущий срок полномочий raft отвечающего участника. | uint64 |
| raftAppliedIndex | raftAppliedIndex — текущий применённый индекс raft отвечающего участника. | uint64 |
| errors | errors содержит сведения об аварийных сигналах, работоспособности и состоянии. | (slice of) string |
| dbSizeInUse | dbSizeInUse — логически используемый размер базы данных бэкенда отвечающего участника в байтах. | int64 |
| isLearner | isLearner указывает, является ли участник обучающимся участником raft. | bool |
| storageVersion | storageVersion — версия файла БД. Она может обновляться с задержкой относительно целевой версии кластера. | string |
| dbSizeQuota | dbSizeQuota — настроенная квота хранилища etcd в байтах (значение, переданное экземпляру etcd флагом --quota-backend-bytes) | int64 |
| downgradeInfo | downgradeInfo указывает на наличие процесса понижения версии. | DowngradeInfo |

##### Сообщение `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

Из статьи Google о paxosdb: наша реализация строится вокруг мощного примитива MultiOp. Все остальные операции с базой данных, кроме итерации, реализованы как один вызов MultiOp. MultiOp применяется атомарно и состоит из трёх компонентов: 1. Список проверок guard. Каждая проверка guard проверяет одну запись базы данных: отсутствие или наличие значения либо равенство заданному значению. Две проверки guard могут относиться к одной или разным записям. Все проверки guard применяются, и MultiOp возвращает результаты. Если все проверки истинны, MultiOp выполняет t op (см. пункт 2 ниже), иначе — f op (см. пункт 3 ниже). 2. Список операций базы данных t op. Каждая операция списка является вставкой, удалением или поиском и применяется к одной записи. Две операции могут относиться к одной или разным записям. Они выполняются, если guard истинно. 3. Список операций базы данных f op. Аналогичен t op, но выполняется, если guard ложно.

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare — список предикатов, представляющих конъюнкцию условий. Если сравнения успешны, запросы success обрабатываются по порядку, а ответ содержит их соответствующие ответы в том же порядке. Если сравнения неудачны, по порядку обрабатываются запросы failure, и ответ содержит соответствующие ответы по порядку. | (slice of) Compare |
| success | success — список запросов, применяемых, когда compare истинно. | (slice of) RequestOp |
| failure | failure — список запросов, применяемых, когда compare ложно. | (slice of) RequestOp |

##### Сообщение `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | succeeded равно true, если compare истинно, и false в противном случае. | bool |
| responses | responses — список ответов, соответствующих результатам применения success, если succeeded равно true, либо failure, если succeeded равно false. | (slice of) ResponseOp |

##### Сообщение `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id — идентификатор отменяемого наблюдателя, которому больше не будут передаваться события. | int64 |

##### Сообщение `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key — ключ, регистрируемый для наблюдения. | bytes |
| range_end | range_end — конец наблюдаемого диапазона [key, range_end). Если range_end не задан, наблюдается только аргумент key. Если range_end равен '\0', наблюдаются все ключи, большие либо равные аргументу key. Если range_end равен заданному ключу плюс один, наблюдаются все ключи с префиксом заданного ключа. | bytes |
| start_revision | start_revision — необязательная ревизия, с которой включительно начинается наблюдение. Отсутствие start_revision означает "now". | int64 |
| progress_notify | progress_notify задаётся, чтобы сервер etcd периодически отправлял новому наблюдателю WatchResponse без событий, если недавних событий нет. Это полезно для восстановления отключённого наблюдателя с недавней известной ревизии. Сервер etcd может выбирать частоту уведомлений по текущей нагрузке. | bool |
| filters | filters фильтруют события на стороне сервера до их отправки наблюдателю. | (slice of) FilterType |
| prev_kv | Если prev_kv задан, созданный наблюдатель получает предыдущий KV до события. Если предыдущий KV уже компактизирован, ничего не возвращается. | bool |
| watch_id | Если предоставлен ненулевой watch_id, он назначается этому наблюдателю. Поскольку создание наблюдателя в etcd не является синхронной операцией, это помогает обеспечить правильный порядок при создании нескольких наблюдателей в одном потоке. Создание наблюдателя с уже используемым в потоке ID возвращает ошибку. | int64 |
| fragment | fragment позволяет разбивать большие ревизии на несколько ответов наблюдения. | bool |

##### Сообщение `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

Запрашивает как можно скорее отправить состояние прогресса потока наблюдения в потоке ответов наблюдения.

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Сообщение `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union — запрос создания нового либо отмены существующего наблюдателя. | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### Сообщение `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id — идентификатор наблюдателя, соответствующего ответу. | int64 |
| created | created равно true, если это ответ на запрос создания наблюдения. Клиент должен сохранить watch_id и ожидать события созданного наблюдателя из того же потока. Все отправленные созданному наблюдателю события имеют одинаковый watch_id. | bool |
| canceled | canceled равно true, если это ответ на запрос отмены наблюдения или start_revision уже компактизирована. Отменённому наблюдателю больше не отправляются события. | bool |
| compact_revision | compact_revision содержит минимальный индекс, если наблюдатель пытается наблюдать с компактизированного индекса. Это происходит при создании наблюдателя на компактизированной ревизии или когда наблюдатель не успевает за изменениями хранилища ключей и значений. Клиент должен считать наблюдателя отменённым и больше не пытаться создавать наблюдателя с тем же start_revision. | int64 |
| cancel_reason | cancel_reason указывает причину отмены наблюдателя. | string |
| fragment | fragment равно true, если большой ответ наблюдения разбит на несколько ответов. | bool |
| events |  | (slice of) mvccpb.Event |

##### Сообщение `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| type | type — тип события. PUT означает сохранение новых данных по ключу, DELETE — удаление ключа. | EventType |
| kv | kv содержит KeyValue события. Событие PUT содержит текущую пару kv. PUT с kv.Version=1 означает создание ключа. DELETE/EXPIRE содержит удалённый ключ, ревизия изменения которого равна ревизии удаления. | KeyValue |
| prev_kv | prev_kv содержит пару «ключ — значение» до события. | KeyValue |

##### Сообщение `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| key | key — ключ в байтах. Пустой ключ недопустим. | bytes |
| create_revision | create_revision — ревизия последнего создания этого ключа. | int64 |
| mod_revision | mod_revision — ревизия последнего изменения этого ключа. | int64 |
| version | version — версия ключа. Удаление сбрасывает её в ноль, а любое изменение ключа увеличивает версию. | int64 |
| value | value — значение ключа в байтах. | bytes |
| lease | lease — идентификатор аренды, присоединённой к ключу. При истечении аренды ключ удаляется. Если lease равен 0, аренда к ключу не присоединена. | int64 |

##### Сообщение `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### Сообщение `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### Сообщение `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### Сообщение `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Permission — отдельная сущность

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### Сообщение `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Role — отдельная запись в сегменте authRoles

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (slice of) Permission |

##### Сообщение `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

User — отдельная запись в сегменте authUsers

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (slice of) string |
| options |  | UserAddOptions |

##### Сообщение `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| Поле | Описание | Тип |
| ----- | ----------- | ---- |
| no_password |  | bool |
