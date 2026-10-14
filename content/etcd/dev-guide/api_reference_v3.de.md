---
title: API-Referenz
weight: 3800
description: "Vollständige Referenz der etcd-v3-API"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
---

Diese API-Referenz wird automatisch aus den angegebenen `.proto`-Dateien erzeugt.

##### Dienst `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable aktiviert die Authentifizierung. |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable deaktiviert die Authentifizierung. |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus zeigt den Authentifizierungsstatus an. |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate verarbeitet eine Authentifizierungsanfrage. |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd fügt einen neuen Benutzer hinzu. Der Benutzername darf nicht leer sein. |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet ruft ausführliche Benutzerinformationen ab. |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList ruft eine Liste aller Benutzer ab. |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete löscht einen angegebenen Benutzer. |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword ändert das Passwort eines angegebenen Benutzers. |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrantRole weist einem angegebenen Benutzer eine Rolle zu. |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole entzieht einem angegebenen Benutzer eine Rolle. |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd fügt eine neue Rolle hinzu. Der Rollenname darf nicht leer sein. |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet ruft ausführliche Rolleninformationen ab. |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList ruft Listen aller Rollen ab. |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete löscht eine angegebene Rolle. |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission gewährt einer angegebenen Rolle eine Berechtigung für einen bestimmten Schlüssel oder Bereich. |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission entzieht einer angegebenen Rolle eine Berechtigung für einen Schlüssel oder Bereich. |

##### Dienst `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd fügt dem Cluster ein Mitglied hinzu. |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove entfernt ein vorhandenes Mitglied aus dem Cluster. |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate aktualisiert die Mitgliedskonfiguration. |
| MemberList | MemberListRequest | MemberListResponse | MemberList listet alle Mitglieder des Clusters auf. |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote stuft ein Mitglied von einem nicht stimmberechtigten Raft-Learner zu einem stimmberechtigten Raft-Mitglied hoch. |

##### Dienst `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range ruft die Schlüssel im Bereich aus dem Schlüssel-Wert-Speicher ab. |
| Put | PutRequest | PutResponse | Put schreibt den angegebenen Schlüssel in den Schlüssel-Wert-Speicher. Eine Put-Anfrage erhöht die Revision des Schlüssel-Wert-Speichers und erzeugt ein Ereignis im Ereignisverlauf. |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange löscht den angegebenen Bereich aus dem Schlüssel-Wert-Speicher. Eine Löschanfrage erhöht die Revision des Schlüssel-Wert-Speichers und erzeugt für jeden gelöschten Schlüssel ein Löschereignis im Ereignisverlauf. |
| Txn | TxnRequest | TxnResponse | Txn verarbeitet mehrere Anfragen in einer einzigen Transaktion. Eine Txn-Anfrage erhöht die Revision des Schlüssel-Wert-Speichers und erzeugt für jede abgeschlossene Anfrage Ereignisse mit derselben Revision. Derselbe Schlüssel darf innerhalb einer Transaktion nicht mehrfach geändert werden. |
| Compact | CompactionRequest | CompactionResponse | Compact kompaktiert den Ereignisverlauf im Schlüssel-Wert-Speicher von etcd. Der Schlüssel-Wert-Speicher sollte regelmäßig kompaktiert werden, da der Ereignisverlauf andernfalls unbegrenzt weiterwächst. |

##### Dienst `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant erstellt eine Lease, die abläuft, wenn der Server innerhalb einer vorgegebenen Lebensdauer kein keepAlive empfängt. Läuft die Lease ab, laufen alle ihr zugeordneten Schlüssel ebenfalls ab und werden gelöscht. Jeder abgelaufene Schlüssel erzeugt ein Löschereignis im Ereignisverlauf. |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke widerruft eine Lease. Alle ihr zugeordneten Schlüssel laufen ab und werden gelöscht. |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive hält die Lease am Leben, indem es Keepalive-Anfragen vom Client zum Server und Keepalive-Antworten vom Server zum Client als Streams überträgt. |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive ruft Informationen zur Lease ab. |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases listet alle vorhandenen Leases auf. |

##### Dienst `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| Alarm | AlarmRequest | AlarmResponse | Alarm aktiviert, deaktiviert und erfragt Alarme zum Zustand des Clusters. |
| Status | StatusRequest | StatusResponse | Status ruft den Status des Mitglieds ab. |
| Defragment | DefragmentRequest | DefragmentResponse | Defragment defragmentiert die Backend-Datenbank eines Mitglieds, um Speicherplatz zurückzugewinnen. |
| Hash | HashRequest | HashResponse | Hash berechnet den Hash des gesamten Backend-Schlüsselraums einschließlich der Buckets key, lease und weiterer Buckets im Speicher. Dies ist NUR für Tests vorgesehen! Im Produktivbetrieb mit laufenden Transaktionen darf man sich nicht darauf verlassen, da die Hash-Operation keine MVCC-Sperren hält. Für Konsistenzprüfungen des Buckets "key" stattdessen die API "HashKV" verwenden. |
| HashKV | HashKVRequest | HashKVResponse | HashKV berechnet den Hash aller MVCC-Schlüssel bis zu einer angegebenen Revision. Es durchläuft nur den Bucket "key" im Backend-Speicher. |
| Snapshot | SnapshotRequest | SnapshotResponse | Snapshot sendet einen Snapshot des gesamten Backends eines Mitglieds über einen Stream an einen Client. |
| MoveLeader | MoveLeaderRequest | MoveLeaderResponse | MoveLeader fordert den aktuellen Leader-Knoten auf, seine Führungsrolle an den vorgesehenen Empfänger zu übertragen. |
| Downgrade | DowngradeRequest | DowngradeResponse | Downgrade fordert ein Downgrade der Clusterversion an, prüft dessen Durchführbarkeit oder bricht es ab. Seit etcd 3.5 unterstützt. |

##### Dienst `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| Watch | WatchRequest | WatchResponse | Watch beobachtet aktuelle oder bereits vergangene Ereignisse. Ein- und Ausgabe sind Streams: Der Eingabestream dient zum Erstellen und Abbrechen von Watchern, der Ausgabestream überträgt Ereignisse. Ein Watch-RPC kann mehrere Schlüsselbereiche beobachten und Ereignisse für mehrere Watches gleichzeitig streamen. Der gesamte Ereignisverlauf kann ab der letzten Kompaktierungsrevision beobachtet werden. |

##### Nachricht `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID ist die ID des Mitglieds, dem der ausgelöste Alarm zugeordnet ist. | uint64 |
| alarm | alarm ist der Typ des ausgelösten Alarms. | AlarmType |

##### Nachricht `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action ist die Art der auszuführenden Alarmanfrage. Die Aktion kann Alarmzustände abrufen (GET), einen Alarm aktivieren (ACTIVATE) oder einen ausgelösten Alarm deaktivieren (DEACTIVATE). | AlarmAction |
| memberID | memberID ist die ID des Mitglieds, dem der Alarm zugeordnet ist. Ist memberID 0, umfasst die Alarmanfrage alle Mitglieder. | uint64 |
| alarm | alarm ist der bei dieser Anfrage zu berücksichtigende Alarmtyp. | AlarmType |

##### Nachricht `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms ist eine Liste der Alarme, die der Alarmanfrage zugeordnet sind. | (Slice von) AlarmMember |

##### Nachricht `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name ist der Name der Rolle, die dem Authentifizierungssystem hinzugefügt werden soll. | string |

##### Nachricht `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### Nachricht `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |

##### Nachricht `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (Slice von) authpb.Permission |

##### Nachricht `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name ist der Name der Rolle, der die Berechtigung erteilt wird. | string |
| perm | perm ist die Berechtigung, die der Rolle erteilt werden soll. | authpb.Permission |

##### Nachricht `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (Slice von) string |

##### Nachricht `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### Nachricht `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision ist die aktuelle Revision des Authentifizierungsspeichers | uint64 |

##### Nachricht `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### Nachricht `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name ist der Name des Benutzers, dessen Passwort geändert wird. | string |
| password | password ist das neue Passwort des Benutzers. Dieses Feld wird in der API-Schicht entfernt. | string |
| hashedPassword | hashedPassword ist der Hashwert des neuen Passworts des Benutzers. Dieses Feld wird in der API-Schicht initialisiert. | string |

##### Nachricht `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name ist der Name des zu löschenden Benutzers. | string |

##### Nachricht `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### Nachricht `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (Slice von) string |

##### Nachricht `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user ist der Name des Benutzers, dem eine angegebene Rolle zugewiesen werden sollte. | string |
| role | role ist der Name der Rolle, die dem Benutzer zugewiesen werden soll. | string |

##### Nachricht `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (Slice von) string |

##### Nachricht `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### Nachricht `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### Nachricht `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | token ist ein autorisiertes Token, das in nachfolgenden RPCs verwendet werden kann | string |

##### Nachricht `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequest kompaktiert den Schlüssel-Wert-Speicher bis zu einer angegebenen Revision. Alle ersetzten Schlüssel mit einer Revision unterhalb der Kompaktierungsrevision werden entfernt.

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision ist die Revision des Schlüssel-Wert-Speichers für die Kompaktierungsoperation. | int64 |
| physical | Wenn physical gesetzt ist, wartet der RPC, bis die Kompaktierung physisch auf die lokale Datenbank angewendet wurde und die kompaktierten Einträge vollständig aus der Backend-Datenbank entfernt sind. | bool |

##### Nachricht `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result ist die logische Vergleichsoperation für diesen Vergleich. | CompareResult |
| target | target ist das Schlüssel-Wert-Feld, das für den Vergleich geprüft werden soll. | CompareTarget |
| key | key ist der Schlüssel, auf den die Vergleichsoperation angewendet wird. | bytes |
| target_union |  | oneof |
| version | version ist die Version des angegebenen Schlüssels | int64 |
| create_revision | create_revision ist die Erstellungsrevision des angegebenen Schlüssels | int64 |
| mod_revision | mod_revision ist die Revision der letzten Änderung des angegebenen Schlüssels. | int64 |
| value | value ist der Wert des angegebenen Schlüssels als Bytes. | bytes |
| lease | lease ist die Lease-ID des angegebenen Schlüssels. | int64 |
| range_end | range_end vergleicht das angegebene target mit allen Schlüsseln im Bereich [key, range_end). Weitere Informationen zu Schlüsselbereichen enthält RangeRequest. | bytes |

##### Nachricht `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key ist der erste zu löschende Schlüssel im Bereich. | bytes |
| range_end | range_end ist der Schlüssel nach dem letzten zu löschenden Schlüssel im Bereich [key, range_end). Ist range_end nicht angegeben, enthält der Bereich nur das Argument key. Ist range_end gleich dem angegebenen Schlüssel plus eins, umfasst der Bereich alle Schlüssel mit diesem Präfix, also dem angegebenen Schlüssel. Ist range_end '\0', umfasst der Bereich alle Schlüssel größer oder gleich dem Argument key. | bytes |
| prev_kv | Ist prev_kv gesetzt, ruft etcd vor dem Löschen die vorherigen Schlüssel-Wert-Paare ab. Diese werden in der Löschantwort zurückgegeben. | bool |

##### Nachricht `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted ist die Anzahl der durch die Bereichslöschanfrage gelöschten Schlüssel. | int64 |
| prev_kvs | Ist prev_kv in der Anfrage gesetzt, werden die vorherigen Schlüssel-Wert-Paare zurückgegeben. | (Slice von) mvccpb.KeyValue |

##### Nachricht `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| enabled | enabled gibt an, ob für den Cluster ein Downgrade aktiviert ist. | bool |
| targetVersion | targetVersion ist die Zielversion des Downgrades. | string |

##### Nachricht `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action ist die Art der auszuführenden Downgrade-Anfrage. Die Aktion kann die Zielversion validieren (VALIDATE), die Clusterversion herabsetzen (DOWNGRADE) oder den laufenden Downgrade-Vorgang abbrechen (CANCEL). | DowngradeAction |
| version | version ist die Zielversion des Downgrades. | string |

##### Nachricht `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version ist die aktuelle Clusterversion. | string |

##### Nachricht `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequest wird nur für Tests verwendet. Die Version in dieser Anfrage wird als Version des WAL-Eintrags gelesen. Ist die Downgrade-Zielversion kleiner als diese Version, ist das Downgrade im laufenden Betrieb oder die Offline-Migration nicht sicher und sollte daher nicht zugelassen werden.

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### Nachricht `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| revision | revision ist die Revision des Schlüssel-Wert-Speichers für die Hash-Operation. | int64 |

##### Nachricht `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash ist der Hashwert, der aus den MVCC-Schlüsseln des antwortenden Mitglieds bis zu einer angegebenen Revision berechnet wurde. | uint32 |
| compact_revision | compact_revision ist die Kompaktierungsrevision des Schlüssel-Wert-Speichers zu Beginn der Hash-Berechnung. | int64 |
| hash_revision | hash_revision ist die Revision, bis zu der der Hash berechnet wird. | int64 |

##### Nachricht `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash ist der Hashwert, der aus dem KV-Backend des antwortenden Mitglieds berechnet wurde. | uint32 |

##### Nachricht `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Lease-ID, für die ein Checkpoint erstellt werden soll. | int64 |
| remaining_TTL | Remaining_TTL ist die verbleibende Zeit bis zum Ablauf der Lease. | int64 |

##### Nachricht `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (Slice von) LeaseCheckpoint |

##### Nachricht `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL ist die empfohlene Lebensdauer in Sekunden. Für eine abgelaufene Lease wird -1 zurückgegeben. | int64 |
| ID | ID ist die angeforderte ID der Lease. Ist ID auf 0 gesetzt, wählt der Lease-Geber eine ID aus. | int64 |

##### Nachricht `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID ist die Lease-ID der gewährten Lease. | int64 |
| TTL | TTL ist die vom Server gewählte Lebensdauer der Lease in Sekunden. | int64 |
| error |  | string |

##### Nachricht `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Lease-ID der am Leben zu haltenden Lease. | int64 |

##### Nachricht `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID ist die Lease-ID aus der Keepalive-Anfrage. | int64 |
| TTL | TTL ist die neue Lebensdauer der Lease. | int64 |

##### Nachricht `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (Slice von) LeaseStatus |

##### Nachricht `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Lease-ID der zu widerrufenden Lease. Wird die ID widerrufen, werden alle zugeordneten Schlüssel gelöscht. | int64 |

##### Nachricht `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### Nachricht `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Lease-ID der Lease. | int64 |
| keys | keys wird auf true gesetzt, um alle dieser Lease zugeordneten Schlüssel abzufragen. | bool |

##### Nachricht `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID ist die Lease-ID aus der Keepalive-Anfrage. | int64 |
| TTL | TTL ist die verbleibende TTL der Lease in Sekunden; die Lease läuft in weniger als TTL+1 Sekunden ab. | int64 |
| grantedTTL | GrantedTTL ist die bei der Erstellung oder Verlängerung der Lease anfänglich gewährte Zeit in Sekunden. | int64 |
| keys | Keys ist die Liste der dieser Lease zugeordneten Schlüssel. | (Slice von) bytes |

##### Nachricht `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Mitglieds-ID dieses Mitglieds. | uint64 |
| name | name ist der menschenlesbare Name des Mitglieds. Ist das Mitglied nicht gestartet, ist name eine leere Zeichenfolge. | string |
| peerURLs | peerURLs ist die Liste der URLs, die das Mitglied dem Cluster zur Kommunikation bereitstellt. | (Slice von) string |
| clientURLs | clientURLs ist die Liste der URLs, die das Mitglied Clients zur Kommunikation bereitstellt. Ist das Mitglied nicht gestartet, ist clientURLs leer. | (Slice von) string |
| isLearner | isLearner gibt an, ob das Mitglied ein Raft-Learner ist. | bool |

##### Nachricht `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs ist die Liste der URLs, die das hinzugefügte Mitglied zur Kommunikation mit dem Cluster verwendet. | (Slice von) string |
| isLearner | isLearner gibt an, ob das hinzugefügte Mitglied ein Raft-Learner ist. | bool |

##### Nachricht `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member enthält die Mitgliedsinformationen des hinzugefügten Mitglieds. | Member |
| members | members ist eine Liste aller Mitglieder nach dem Hinzufügen des neuen Mitglieds. | (Slice von) Member |

##### Nachricht `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### Nachricht `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members ist eine Liste aller dem Cluster zugeordneten Mitglieder. | (Slice von) Member |

##### Nachricht `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Mitglieds-ID des hochzustufenden Mitglieds. | uint64 |

##### Nachricht `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members ist eine Liste aller Mitglieder nach der Hochstufung des Mitglieds. | (Slice von) Member |

##### Nachricht `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Mitglieds-ID des zu entfernenden Mitglieds. | uint64 |

##### Nachricht `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members ist eine Liste aller Mitglieder nach dem Entfernen des Mitglieds. | (Slice von) Member |

##### Nachricht `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID ist die Mitglieds-ID des zu aktualisierenden Mitglieds. | uint64 |
| peerURLs | peerURLs ist die neue Liste der URLs, die das Mitglied zur Kommunikation mit dem Cluster verwendet. | (Slice von) string |

##### Nachricht `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| members | members ist eine Liste aller Mitglieder nach der Aktualisierung des Mitglieds. | (Slice von) Member |

##### Nachricht `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID ist die Knoten-ID des neuen Leaders. | uint64 |

##### Nachricht `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### Nachricht `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key ist der Schlüssel als Bytes, der in den Schlüssel-Wert-Speicher geschrieben werden soll. | bytes |
| value | value ist der Wert als Bytes, der dem Schlüssel im Schlüssel-Wert-Speicher zugeordnet werden soll. | bytes |
| lease | lease ist die Lease-ID, die dem Schlüssel im Schlüssel-Wert-Speicher zugeordnet werden soll. Der Lease-Wert 0 bedeutet, dass keine Lease zugeordnet ist. | int64 |
| prev_kv | Ist prev_kv gesetzt, ruft etcd vor der Änderung das vorherige Schlüssel-Wert-Paar ab. Dieses wird in der Put-Antwort zurückgegeben. | bool |
| ignore_value | Ist ignore_value gesetzt, aktualisiert etcd den Schlüssel mit seinem aktuellen Wert. Wenn der Schlüssel nicht existiert, wird ein Fehler zurückgegeben. | bool |
| ignore_lease | Ist ignore_lease gesetzt, aktualisiert etcd den Schlüssel mit seiner aktuellen Lease. Wenn der Schlüssel nicht existiert, wird ein Fehler zurückgegeben. | bool |

##### Nachricht `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | Ist prev_kv in der Anfrage gesetzt, wird das vorherige Schlüssel-Wert-Paar zurückgegeben. | mvccpb.KeyValue |

##### Nachricht `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key ist der erste Schlüssel des Bereichs. Ist range_end nicht angegeben, sucht die Anfrage nur nach key. | bytes |
| range_end | range_end ist die obere Grenze des angeforderten Bereichs [key, range_end). Ist range_end '\0', umfasst der Bereich alle Schlüssel >= key. Ist range_end key plus eins, etwa "aa"+1 == "ab" oder "a\xff"+1 == "b", ruft die Bereichsanfrage alle Schlüssel mit dem Präfix key ab. Sind key und range_end beide '\0', gibt die Bereichsanfrage alle Schlüssel zurück. | bytes |
| limit | limit begrenzt die Anzahl der für die Anfrage zurückgegebenen Schlüssel. Der Wert 0 bedeutet keine Begrenzung. | int64 |
| revision | revision ist der für den Bereich zu verwendende Zeitpunkt im Schlüssel-Wert-Speicher. Ist revision kleiner oder gleich null, bezieht sich der Bereich auf den neuesten Stand des Schlüssel-Wert-Speichers. Wurde die Revision bereits kompaktiert, wird ErrCompacted zurückgegeben. | int64 |
| sort_order | sort_order ist die Reihenfolge der zurückgegebenen sortierten Ergebnisse. | SortOrder |
| sort_target | sort_target ist das Schlüssel-Wert-Feld, nach dem sortiert wird. | SortTarget |
| serializable | serializable legt fest, dass die Bereichsanfrage serialisierbare, auf das Mitglied beschränkte Lesezugriffe verwendet. Bereichsanfragen sind standardmäßig linearisierbar. Linearisierbare Anfragen haben eine höhere Latenz und einen geringeren Durchsatz als serialisierbare Anfragen, spiegeln aber den aktuellen Konsens des Clusters wider. Für bessere Leistung auf Kosten möglicherweise veralteter Leseergebnisse wird eine serialisierbare Bereichsanfrage lokal bearbeitet, ohne einen Konsens mit anderen Clusterknoten herstellen zu müssen. | bool |
| keys_only | Wenn keys_only gesetzt ist, werden nur die Schlüssel und nicht die Werte zurückgegeben. | bool |
| count_only | Wenn count_only gesetzt ist, wird nur die Anzahl der Schlüssel im Bereich zurückgegeben. | bool |
| min_mod_revision | min_mod_revision ist die Untergrenze für die Änderungsrevisionen der zurückgegebenen Schlüssel. Alle Schlüssel mit kleineren Änderungsrevisionen werden herausgefiltert. | int64 |
| max_mod_revision | max_mod_revision ist die Obergrenze für die Änderungsrevisionen der zurückgegebenen Schlüssel. Alle Schlüssel mit größeren Änderungsrevisionen werden herausgefiltert. | int64 |
| min_create_revision | min_create_revision ist die Untergrenze für die Erstellungsrevisionen der zurückgegebenen Schlüssel. Alle Schlüssel mit kleineren Erstellungsrevisionen werden herausgefiltert. | int64 |
| max_create_revision | max_create_revision ist die Obergrenze für die Erstellungsrevisionen der zurückgegebenen Schlüssel. Alle Schlüssel mit größeren Erstellungsrevisionen werden herausgefiltert. | int64 |

##### Nachricht `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs ist die Liste der Schlüssel-Wert-Paare, die der Bereichsanfrage entsprechen. Bei einer Anfrage nach count ist kvs leer. | (Slice von) mvccpb.KeyValue |
| more | more gibt an, ob im angeforderten Bereich weitere Schlüssel zurückzugeben sind. | bool |
| count | count wird auf Anfrage auf die tatsächliche Anzahl der Schlüssel im Bereich gesetzt. Anders als Kvs bleibt es von Begrenzungen und Filtern wie Min/Max, Create/Modify und Revisions unbeeinflusst und gibt die vollständige Anzahl im angegebenen Bereich wieder. | int64 |

##### Nachricht `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request ist eine Vereinigung der von einer Transaktion akzeptierten Anfragetypen. | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### Nachricht `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id ist die ID des Clusters, der die Antwort gesendet hat. | uint64 |
| member_id | member_id ist die ID des Mitglieds, das die Antwort gesendet hat. | uint64 |
| revision | revision ist die Revision des Schlüssel-Wert-Speichers zum Zeitpunkt der Anwendung der Anfrage. Bei Aufrufen ohne Zugriff auf den Schlüssel-Wert-Speicher ist sie nicht gesetzt und daher 0. Bei Watch-Fortschrittsantworten zeigt header.revision den Fortschritt an. Alle künftig in diesem Stream empfangenen Ereignisse haben garantiert eine höhere Revisionsnummer als header.revision. | int64 |
| raft_term | raft_term ist der Raft-Term zum Zeitpunkt der Anwendung der Anfrage. | uint64 |

##### Nachricht `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response ist eine Vereinigung der von einer Transaktion zurückgegebenen Antworttypen. | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### Nachricht `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header enthält die aktuellen Informationen zum Schlüssel-Wert-Speicher. Der erste Header im Snapshot-Stream gibt den Zeitpunkt des Snapshots an. | ResponseHeader |
| remaining_bytes | remaining_bytes ist die Anzahl der Blob-Bytes, die nach dieser Nachricht noch gesendet werden | uint64 |
| blob | blob enthält den nächsten Teil des Snapshots im Snapshot-Stream. | bytes |
| version | Im Snapshot gespeicherte Version des Speicherschemas. Sie wird aus dem lokalen Backend des Mitglieds gelesen und kann von dessen Binärversion abweichen. Gibt an, welche etcd-Speicherversion beim Wiederherstellen des Snapshots unterstützt werden muss. | string |

##### Nachricht `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version ist die Binärversion des antwortenden etcd-Mitglieds. Die Version des Speicherschemas wird separat in storageVersion angegeben. | string |
| dbSize | dbSize ist die physisch zugewiesene Größe der Backend-Datenbank des antwortenden Mitglieds in Bytes. | int64 |
| leader | leader ist die Mitglieds-ID, die das antwortende Mitglied für den aktuellen Leader hält. | uint64 |
| raftIndex | raftIndex ist der aktuelle bestätigte Raft-Index des antwortenden Mitglieds. | uint64 |
| raftTerm | raftTerm ist der aktuelle Raft-Term des antwortenden Mitglieds. | uint64 |
| raftAppliedIndex | raftAppliedIndex ist der aktuelle angewendete Raft-Index des antwortenden Mitglieds. | uint64 |
| errors | errors enthält Alarm- und Zustandsinformationen sowie den Status. | (Slice von) string |
| dbSizeInUse | dbSizeInUse ist die logisch verwendete Größe der Backend-Datenbank des antwortenden Mitglieds in Bytes. | int64 |
| isLearner | isLearner gibt an, ob das Mitglied ein Raft-Learner ist. | bool |
| storageVersion | storageVersion ist die Version der db-Datei. Sie kann gegenüber der angestrebten Clusterversion verzögert aktualisiert werden. | string |
| dbSizeQuota | dbSizeQuota ist das konfigurierte etcd-Speicherkontingent in Bytes, also der über die Option --quota-backend-bytes an die etcd-Instanz übergebene Wert | int64 |
| downgradeInfo | downgradeInfo gibt an, ob ein Downgrade-Vorgang läuft. | DowngradeInfo |

##### Nachricht `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

Aus dem Google-PaxosDB-Papier: Unsere Implementierung beruht auf einer leistungsfähigen Grundoperation namens MultiOp. Alle anderen Datenbankoperationen außer der Iteration sind als einzelner MultiOp-Aufruf implementiert. Eine MultiOp wird atomar angewendet und besteht aus drei Komponenten: 1. Einer Liste von Prüfungen namens guard. Jede Prüfung in guard prüft einen einzelnen Datenbankeintrag. Sie kann prüfen, ob ein Wert fehlt oder vorhanden ist, oder ihn mit einem angegebenen Wert vergleichen. Zwei verschiedene Prüfungen in guard können denselben oder unterschiedliche Datenbankeinträge betreffen. Alle Prüfungen in guard werden ausgeführt, und MultiOp gibt die Ergebnisse zurück. Sind alle Prüfungen wahr, führt MultiOp t op aus (siehe Punkt 2 unten), andernfalls f op (siehe Punkt 3 unten). 2. Einer Liste von Datenbankoperationen namens t op. Jede Operation ist eine Einfüge-, Lösch- oder Suchoperation und betrifft einen einzelnen Datenbankeintrag. Zwei verschiedene Operationen können denselben oder unterschiedliche Datenbankeinträge betreffen. Diese Operationen werden ausgeführt, wenn guard true ergibt. 3. Einer Liste von Datenbankoperationen namens f op. Wie t op, wird jedoch ausgeführt, wenn guard false ergibt.

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare ist eine Liste von Prädikaten, die eine Konjunktion von Bedingungen repräsentiert. Sind die Vergleiche erfolgreich, werden die success-Anfragen der Reihe nach verarbeitet, und die Antwort enthält deren Antworten in derselben Reihenfolge. Schlagen die Vergleiche fehl, werden die failure-Anfragen der Reihe nach verarbeitet, und die Antwort enthält deren Antworten in derselben Reihenfolge. | (Slice von) Compare |
| success | success ist eine Liste von Anfragen, die angewendet werden, wenn compare true ergibt. | (Slice von) RequestOp |
| failure | failure ist eine Liste von Anfragen, die angewendet werden, wenn compare false ergibt. | (Slice von) RequestOp |

##### Nachricht `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | succeeded wird auf true gesetzt, wenn compare true ergab, andernfalls auf false. | bool |
| responses | responses ist eine Liste von Antworten auf die Ergebnisse der Anwendung von success, falls succeeded true ist, beziehungsweise failure, falls succeeded false ist. | (Slice von) ResponseOp |

##### Nachricht `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id ist die ID des abzubrechenden Watchers, damit keine weiteren Ereignisse übertragen werden. | int64 |

##### Nachricht `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key ist der Schlüssel, der zur Beobachtung registriert werden soll. | bytes |
| range_end | range_end ist das Ende des zu beobachtenden Bereichs [key, range_end). Ist range_end nicht angegeben, wird nur das Argument key beobachtet. Ist range_end gleich '\0', werden alle Schlüssel größer oder gleich dem Argument key beobachtet. Ist range_end gleich dem angegebenen Schlüssel plus eins, werden alle Schlüssel mit diesem Präfix, also dem angegebenen Schlüssel, beobachtet. | bytes |
| start_revision | start_revision ist eine optionale Revision, ab der einschließlich beobachtet wird. Ohne start_revision beginnt die Beobachtung „jetzt“. | int64 |
| progress_notify | Wenn progress_notify gesetzt ist und keine aktuellen Ereignisse vorliegen, sendet der etcd-Server regelmäßig eine WatchResponse ohne Ereignisse an den neuen Watcher. Das ist nützlich, wenn Clients einen unterbrochenen Watcher ab einer kürzlich bekannt gewordenen Revision wiederherstellen möchten. Der etcd-Server kann anhand der aktuellen Last entscheiden, wie häufig er Benachrichtigungen sendet. | bool |
| filters | filters filtert die Ereignisse serverseitig, bevor sie an den Watcher zurückgesendet werden. | (Slice von) FilterType |
| prev_kv | Ist prev_kv gesetzt, erhält der erstellte Watcher den vorherigen KV vor dem Ereignis. Wurde der vorherige KV bereits kompaktiert, wird nichts zurückgegeben. | bool |
| watch_id | Wird watch_id angegeben und ist ungleich null, wird sie diesem Watcher zugewiesen. Da das Erstellen eines Watchers in etcd kein synchroner Vorgang ist, lässt sich damit beim Erstellen mehrerer Watcher im selben Stream die richtige Reihenfolge sicherstellen. Wird ein Watcher mit einer im Stream bereits verwendeten ID erstellt, wird ein Fehler zurückgegeben. | int64 |
| fragment | fragment ermöglicht das Aufteilen großer Revisionen auf mehrere Watch-Antworten. | bool |

##### Nachricht `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

Fordert an, dass der Fortschrittsstatus eines Watch-Streams so bald wie möglich im Watch-Antwortstream gesendet wird.

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### Nachricht `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union ist eine Anfrage zum Erstellen eines neuen Watchers oder zum Abbrechen eines vorhandenen Watchers. | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### Nachricht `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id ist die ID des Watchers, zu dem die Antwort gehört. | int64 |
| created | created wird auf true gesetzt, wenn die Antwort zu einer Anfrage zum Erstellen eines Watches gehört. Der Client sollte watch_id speichern und die Ereignisse für den erstellten Watcher im selben Stream erwarten. Alle an diesen Watcher gesendeten Ereignisse enthalten dieselbe watch_id. | bool |
| canceled | canceled wird auf true gesetzt, wenn die Antwort zu einer Anfrage zum Abbrechen eines Watches gehört oder start_revision bereits kompaktiert wurde. An den abgebrochenen Watcher werden keine weiteren Ereignisse gesendet. | bool |
| compact_revision | compact_revision wird auf den kleinsten Index gesetzt, wenn ein Watcher versucht, einen bereits kompaktierten Index zu beobachten. Dies geschieht beim Erstellen eines Watchers an einer kompaktierten Revision oder wenn der Watcher den Fortschritt des Schlüssel-Wert-Speichers nicht einholen kann. Der Client sollte den Watcher als abgebrochen behandeln und nicht erneut versuchen, einen Watcher mit derselben start_revision zu erstellen. | int64 |
| cancel_reason | cancel_reason gibt den Grund für den Abbruch des Watchers an. | string |
| fragment | fragment ist true, wenn eine große Watch-Antwort auf mehrere Antworten aufgeteilt wurde. | bool |
| events |  | (Slice von) mvccpb.Event |

##### Nachricht `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| type | type ist die Art des Ereignisses. Ist type ein PUT, wurden neue Daten unter dem Schlüssel gespeichert. Ist type ein DELETE, wurde der Schlüssel gelöscht. | EventType |
| kv | kv enthält den KeyValue für das Ereignis. Ein PUT-Ereignis enthält das aktuelle kv-Paar. Ein PUT-Ereignis mit kv.Version=1 zeigt die Erstellung eines Schlüssels an. Ein DELETE/EXPIRE-Ereignis enthält den gelöschten Schlüssel, dessen Änderungsrevision auf die Revision der Löschung gesetzt ist. | KeyValue |
| prev_kv | prev_kv enthält das Schlüssel-Wert-Paar vor dem Ereignis. | KeyValue |

##### Nachricht `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| key | key ist der Schlüssel als Bytes. Ein leerer Schlüssel ist nicht zulässig. | bytes |
| create_revision | create_revision ist die Revision der letzten Erstellung dieses Schlüssels. | int64 |
| mod_revision | mod_revision ist die Revision der letzten Änderung dieses Schlüssels. | int64 |
| version | version ist die Version des Schlüssels. Eine Löschung setzt die Version auf null zurück, und jede Änderung des Schlüssels erhöht seine Version. | int64 |
| value | value ist der unter dem Schlüssel gespeicherte Wert als Bytes. | bytes |
| lease | lease ist die ID der dem Schlüssel zugeordneten Lease. Wenn diese Lease abläuft, wird der Schlüssel gelöscht. Ist lease 0, ist dem Schlüssel keine Lease zugeordnet. | int64 |

##### Nachricht `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### Nachricht `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### Nachricht `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### Nachricht `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Permission ist eine einzelne Entität

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### Nachricht `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Role ist ein einzelner Eintrag im Bucket authRoles

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (Slice von) Permission |

##### Nachricht `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

User ist ein einzelner Eintrag im Bucket authUsers

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (Slice von) string |
| options |  | UserAddOptions |

##### Nachricht `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| no_password |  | bool |
