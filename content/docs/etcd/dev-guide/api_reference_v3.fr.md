---
title: "Référence de l'API"
weight: 3800
description: "Référence complète de l'API etcd v3"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/api_reference_v3.md"
aliases: [/etcd/dev-guide/api_reference_v3/]
---

Cette référence d'API est générée automatiquement à partir des fichiers nommés `.proto`.

##### service `Auth` (api/etcdserverpb/rpc.proto) {#service-auth-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| AuthEnable | AuthEnableRequest | AuthEnableResponse | AuthEnable active l'authentification. |
| AuthDisable | AuthDisableRequest | AuthDisableResponse | AuthDisable désactive l'authentification. |
| AuthStatus | AuthStatusRequest | AuthStatusResponse | AuthStatus affiche l'état de l'authentification. |
| Authenticate | AuthenticateRequest | AuthenticateResponse | Authenticate traite une requête d'authentification. |
| UserAdd | AuthUserAddRequest | AuthUserAddResponse | UserAdd ajoute un nouvel utilisateur. Le nom d'utilisateur ne peut pas être vide. |
| UserGet | AuthUserGetRequest | AuthUserGetResponse | UserGet obtient les informations détaillées d'un utilisateur. |
| UserList | AuthUserListRequest | AuthUserListResponse | UserList obtient la liste de tous les utilisateurs. |
| UserDelete | AuthUserDeleteRequest | AuthUserDeleteResponse | UserDelete supprime un utilisateur spécifié. |
| UserChangePassword | AuthUserChangePasswordRequest | AuthUserChangePasswordResponse | UserChangePassword modifie le mot de passe d'un utilisateur spécifié. |
| UserGrantRole | AuthUserGrantRoleRequest | AuthUserGrantRoleResponse | UserGrant accorde un rôle à un utilisateur spécifié. |
| UserRevokeRole | AuthUserRevokeRoleRequest | AuthUserRevokeRoleResponse | UserRevokeRole retire un rôle à un utilisateur spécifié. |
| RoleAdd | AuthRoleAddRequest | AuthRoleAddResponse | RoleAdd ajoute un nouveau rôle. Le nom de rôle ne peut pas être vide. |
| RoleGet | AuthRoleGetRequest | AuthRoleGetResponse | RoleGet obtient les informations détaillées sur un rôle. |
| RoleList | AuthRoleListRequest | AuthRoleListResponse | RoleList obtient la liste de tous les rôles. |
| RoleDelete | AuthRoleDeleteRequest | AuthRoleDeleteResponse | RoleDelete supprime un rôle spécifié. |
| RoleGrantPermission | AuthRoleGrantPermissionRequest | AuthRoleGrantPermissionResponse | RoleGrantPermission accorde une permission sur une clé ou une plage spécifique à un rôle spécifié. |
| RoleRevokePermission | AuthRoleRevokePermissionRequest | AuthRoleRevokePermissionResponse | RoleRevokePermission retire une permission sur une clé ou une plage spécifique à un rôle spécifié. |

##### service `Cluster` (api/etcdserverpb/rpc.proto) {#service-cluster-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| MemberAdd | MemberAddRequest | MemberAddResponse | MemberAdd ajoute un membre au cluster. |
| MemberRemove | MemberRemoveRequest | MemberRemoveResponse | MemberRemove supprime un membre existant du cluster. |
| MemberUpdate | MemberUpdateRequest | MemberUpdateResponse | MemberUpdate met à jour la configuration du membre. |
| MemberList | MemberListRequest | MemberListResponse | MemberList liste tous les membres du cluster. |
| MemberPromote | MemberPromoteRequest | MemberPromoteResponse | MemberPromote promeut un membre de type apprenant Raft (non votant) en membre votant Raft. |

##### service `KV` (api/etcdserverpb/rpc.proto) {#service-kv-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| Range | RangeRequest | RangeResponse | Range récupère les clés dans la plage depuis le magasin clé-valeur. |
| Put | PutRequest | PutResponse | Put insère la clé donnée dans le magasin clé-valeur. Une requête Put incrémente la révision du magasin clé-valeur et génère un événement dans l'historique des événements. |
| DeleteRange | DeleteRangeRequest | DeleteRangeResponse | DeleteRange supprime la plage donnée depuis le magasin clé-valeur. Une requête de suppression incrémente la révision du magasin clé-valeur et génère un événement de suppression dans l'historique des événements pour chaque clé supprimée. |
| Txn | TxnRequest | TxnResponse | Txn traite plusieurs requêtes dans une seule transaction. Une requête Txn incrémente la révision du magasin clé-valeur et génère des événements avec la même révision pour chaque requête terminée. Il est interdit de modifier la même clé plusieurs fois au sein d'une même transaction. |
| Compact | CompactionRequest | CompactionResponse | Compact compresse l'historique des événements dans le magasin clé-valeur etcd. Le magasin clé-valeur doit être régulièrement compacté, sinon l'historique des événements continuera de croître indéfiniment. |

##### service `Lease` (api/etcdserverpb/rpc.proto) {#service-lease-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| LeaseGrant | LeaseGrantRequest | LeaseGrantResponse | LeaseGrant crée un bail qui expire si le serveur ne reçoit pas de demande de maintien de vie dans un délai défini. Toutes les clés associées au bail expireront et seront supprimées si le bail expire. Chaque clé expirée génère un événement de suppression dans l'historique des événements. |
| LeaseRevoke | LeaseRevokeRequest | LeaseRevokeResponse | LeaseRevoke révoque un bail. Toutes les clés associées au bail expireront et seront supprimées. |
| LeaseKeepAlive | LeaseKeepAliveRequest | LeaseKeepAliveResponse | LeaseKeepAlive maintient le bail actif en transmettant en continu des demandes de maintien de vie du client vers le serveur et des réponses de maintien de vie du serveur vers le client. |
| LeaseTimeToLive | LeaseTimeToLiveRequest | LeaseTimeToLiveResponse | LeaseTimeToLive récupère les informations relatives au bail. |
| LeaseLeases | LeaseLeasesRequest | LeaseLeasesResponse | LeaseLeases liste tous les bails existants. |

##### service `Maintenance` (api/etcdserverpb/rpc.proto) {#service-maintenance-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| Alarme | AlarmRequest | AlarmResponse | Alarme active, désactive et interroge les alarmes relatives à l'intégrité du cluster. |
| Statut | StatusRequest | StatusResponse | Statut obtient l'état du membre. |
| Défragmentation | DefragmentRequest | DefragmentResponse | Défragmentation défragmente la base de données du membre backend afin de récupérer de l'espace de stockage. |
| Hachage | HashRequest | HashResponse | Hachage calcule le hachage de l'espace de clés backend entier, y compris les clés, les bails et les autres compartiments dans le stockage. Conçu uniquement à des fins de test ! Ne pas compter sur cette fonctionnalité en production avec des transactions en cours, car l'opération Hachage ne détient pas de verrous MVCC. Utilisez plutôt l'API "HashKV" pour vérifier la cohérence du compartiment "key". |
| HachageKV | HashKVRequest | HashKVResponse | HachageKV calcule le hachage de toutes les clés MVCC jusqu'à une révision donnée. Il ne parcourt que le compartiment "key" dans le stockage backend. |
| Instantané | SnapshotRequest | SnapshotResponse | Instantané envoie un instantané de l'ensemble du backend depuis un membre vers un client via un flux. |
| Transfert du leader | MoveLeaderRequest | MoveLeaderResponse | Transfert du leader demande au nœud leader actuel de transférer son leadership au destinataire. |
| Mise à jour vers une version inférieure | DowngradeRequest | DowngradeResponse | Mise à jour vers une version inférieure demande une mise à jour vers une version inférieure, vérifie la faisabilité ou annule la mise à jour vers une version inférieure sur la version du cluster. Prise en charge depuis etcd 3.5. |

##### service `Watch` (api/etcdserverpb/rpc.proto) {#service-watch-apietcdserverpbrpcproto}

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| Surveillance | WatchRequest | WatchResponse | La surveillance observe les événements survenus ou survenant. Les entrées et sorties sont des flux ; le flux d'entrée sert à créer et annuler des observateurs, tandis que le flux de sortie envoie les événements. Une seule requête RPC de surveillance peut surveiller plusieurs plages de clés, en diffusant les événements de plusieurs surveillance simultanément. L'historique complet des événements peut être surveillé à partir de la dernière révision de compactage. |

##### message `AlarmMember` (api/etcdserverpb/rpc.proto) {#message-alarmmember-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| memberID | memberID est l'identifiant du membre associé à l'alarme déclenchée. | uint64 |
| alarm | alarm est le type d'alarme qui a été déclenchée. | AlarmType |

##### message `AlarmRequest` (api/etcdserverpb/rpc.proto) {#message-alarmrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action est le type de requête d'alarme à émettre. L'action peut être GET pour obtenir les états d'alarme, ACTIVATE pour activer une alarme, ou DEACTIVATE pour désactiver une alarme activée. | AlarmAction |
| memberID | memberID est l'identifiant du membre associé à l'alarme. Si memberID est 0, la requête d'alarme concerne tous les membres. | uint64 |
| alarm | alarm est le type d'alarme à prendre en compte pour cette requête. | AlarmType |

##### message `AlarmResponse` (api/etcdserverpb/rpc.proto) {#message-alarmresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| alarms | alarms est une liste d'alertes associées à la requête d'alerte. | (slice de) AlarmMember |

##### message `AuthDisableRequest` (api/etcdserverpb/rpc.proto) {#message-authdisablerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthDisableResponse` (api/etcdserverpb/rpc.proto) {#message-authdisableresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthEnableRequest` (api/etcdserverpb/rpc.proto) {#message-authenablerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthEnableResponse` (api/etcdserverpb/rpc.proto) {#message-authenableresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleAddRequest` (api/etcdserverpb/rpc.proto) {#message-authroleaddrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name est le nom du rôle à ajouter au système d'authentification. | string |

##### message `AuthRoleAddResponse` (api/etcdserverpb/rpc.proto) {#message-authroleaddresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authroledeleterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | chaîne de caractères |

##### message `AuthRoleDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authroledeleteresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleGetRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegetrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | chaîne de caractères |

##### message `AuthRoleGetResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegetresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | ResponseHeader |
| perm |  | (tranche de) authpb.Permission |

##### message `AuthRoleGrantPermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name est le nom du rôle auquel la permission sera accordée. | string |
| perm | perm est la permission à accorder au rôle. | authpb.Permission |

##### message `AuthRoleGrantPermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolegrantpermissionresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthRoleListRequest` (api/etcdserverpb/rpc.proto) {#message-authrolelistrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthRoleListResponse` (api/etcdserverpb/rpc.proto) {#message-authrolelistresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (tranche de) string |

##### message `AuthRoleRevokePermissionRequest` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| role |  | string |
| key |  | bytes |
| range_end |  | bytes |

##### message `AuthRoleRevokePermissionResponse` (api/etcdserverpb/rpc.proto) {#message-authrolerevokepermissionresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthStatusRequest` (api/etcdserverpb/rpc.proto) {#message-authstatusrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthStatusResponse` (api/etcdserverpb/rpc.proto) {#message-authstatusresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| enabled |  | bool |
| authRevision | authRevision est la révision actuelle du magasin d'authentification | uint64 |

##### message `AuthUserAddRequest` (api/etcdserverpb/rpc.proto) {#message-authuseraddrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |
| options |  | authpb.UserAddOptions |
| hashedPassword |  | string |

##### message `AuthUserAddResponse` (api/etcdserverpb/rpc.proto) {#message-authuseraddresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserChangePasswordRequest` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name est le nom de l'utilisateur dont le mot de passe est modifié. | string |
| password | password est le nouveau mot de passe de l'utilisateur. Notez que ce champ sera supprimé au niveau de l'API. | string |
| hashedPassword | hashedPassword est le nouveau mot de passe de l'utilisateur. Notez que ce champ sera initialisé au niveau de l'API. | string |

##### message `AuthUserChangePasswordResponse` (api/etcdserverpb/rpc.proto) {#message-authuserchangepasswordresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserDeleteRequest` (api/etcdserverpb/rpc.proto) {#message-authuserdeleterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name | name est le nom de l'utilisateur à supprimer. | string |

##### message `AuthUserDeleteResponse` (api/etcdserverpb/rpc.proto) {#message-authuserdeleteresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserGetRequest` (api/etcdserverpb/rpc.proto) {#message-authusergetrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |

##### message `AuthUserGetResponse` (api/etcdserverpb/rpc.proto) {#message-authusergetresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| roles |  | (tranche de) string |

##### message `AuthUserGrantRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authusergrantrolerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| user | user est le nom de l'utilisateur auquel il faut attribuer un rôle donné. | string |
| role | role est le nom du rôle à attribuer à l'utilisateur. | string |

##### message `AuthUserGrantRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authusergrantroleresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthUserListRequest` (api/etcdserverpb/rpc.proto) {#message-authuserlistrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `AuthUserListResponse` (api/etcdserverpb/rpc.proto) {#message-authuserlistresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| users |  | (tranche de) string |

##### message `AuthUserRevokeRoleRequest` (api/etcdserverpb/rpc.proto) {#message-authuserrevokerolerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| role |  | string |

##### message `AuthUserRevokeRoleResponse` (api/etcdserverpb/rpc.proto) {#message-authuserrevokeroleresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `AuthenticateRequest` (api/etcdserverpb/rpc.proto) {#message-authenticaterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| name |  | string |
| password |  | string |

##### message `AuthenticateResponse` (api/etcdserverpb/rpc.proto) {#message-authenticateresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| token | le jeton est un jeton autorisé pouvant être utilisé dans les RPC suivants | string |

##### message `CompactionRequest` (api/etcdserverpb/rpc.proto) {#message-compactionrequest-apietcdserverpbrpcproto}

CompactionRequest compacte le magasin clé-valeur jusqu'à une révision donnée. Toutes les clés obsolètes dont la révision est inférieure à la révision de compactage seront supprimées.

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| révision | révision est la révision du magasin clé-valeur pour l'opération de compactage. | int64 |
| physique | physique est défini afin que l'appel RPC attende que le compactage soit physiquement appliqué à la base de données locale, de sorte que les entrées compactées soient totalement supprimées de la base de données arrière. | bool |

##### message `CompactionResponse` (api/etcdserverpb/rpc.proto) {#message-compactionresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `Compare` (api/etcdserverpb/rpc.proto) {#message-compare-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| result | result est l'opération de comparaison logique pour cette comparaison. | CompareResult |
| target | target est le champ clé-valeur à inspecter pour la comparaison. | CompareTarget |
| key | key est la clé concernée par l'opération de comparaison. | bytes |
| target_union |  | oneof |
| version | version est la version de la clé donnée. | int64 |
| create_revision | create_revision est la révision de création de la clé donnée. | int64 |
| mod_revision | mod_revision est la dernière révision de modification de la clé donnée. | int64 |
| value | value est la valeur de la clé donnée, en bytes. | bytes |
| lease | lease est l'identifiant du bail associé à la clé donnée. | int64 |
| range_end | range_end compare la cible donnée à toutes les clés de la plage [key, range_end). Voir RangeRequest pour plus de détails sur les plages de clés. | bytes |

##### message `DefragmentRequest` (api/etcdserverpb/rpc.proto) {#message-defragmentrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `DefragmentResponse` (api/etcdserverpb/rpc.proto) {#message-defragmentresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `DeleteRangeRequest` (api/etcdserverpb/rpc.proto) {#message-deleterangerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key est la première clé à supprimer dans la plage. | bytes |
| range_end | range_end est la clé suivant la dernière clé à supprimer dans la plage [key, range_end). Si range_end n'est pas fourni, la plage est définie comme ne contenant que la clé fournie. Si range_end est supérieure d'un bit à la clé fournie, la plage correspond à toutes les clés ayant le préfixe (la clé fournie). Si range_end est '\0', la plage correspond à toutes les clés supérieures ou égales à la clé fournie. | bytes |
| prev_kv | Si prev_kv est défini, etcd récupère les paires clé-valeur précédentes avant leur suppression. Les paires clé-valeur précédentes seront renvoyées dans la réponse de suppression. | bool |

##### message `DeleteRangeResponse` (api/etcdserverpb/rpc.proto) {#message-deleterangeresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| deleted | deleted est le nombre de clés supprimées par la requête de suppression par plage. | int64 |
| prev_kvs | si prev_kv est défini dans la requête, les paires clé-valeur précédentes seront renvoyées. | (slice de) mvccpb.KeyValue |

##### message `DowngradeInfo` (api/etcdserverpb/rpc.proto) {#message-downgradeinfo-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| enabled | enabled indique si le cluster est activé pour une mise à jour inverse. | bool |
| targetVersion | targetVersion est la version cible de la mise à jour inverse. | string |

##### message `DowngradeRequest` (api/etcdserverpb/rpc.proto) {#message-downgraderequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| action | action est le type de demande de rétrogradation à émettre. L'action peut VALIDER la version cible, DOWNGRADE le cluster vers une version antérieure, ou CANCELLER le travail de rétrogradation en cours. | DowngradeAction |
| version | version est la version cible de la rétrogradation. | string |

##### message `DowngradeResponse` (api/etcdserverpb/rpc.proto) {#message-downgraderesponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version est la version actuelle du cluster. | string |

##### message `DowngradeVersionTestRequest` (api/etcdserverpb/rpc.proto) {#message-downgradeversiontestrequest-apietcdserverpbrpcproto}

DowngradeVersionTestRequest n'est utilisé que à des fins de test. La version indiquée dans cette requête sera lue comme la version des enregistrements WAL. Si la version cible du downgrade est inférieure à cette version, alors le downgrade (en ligne) ou la migration (hors ligne) n'est pas sécurisé, et ne doit donc pas être autorisé.

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ver |  | string |

##### message `HashKVRequest` (api/etcdserverpb/rpc.proto) {#message-hashkvrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| révision | révision est la révision du magasin clé-valeur pour l'opération de hachage. | int64 |

##### message `HashKVResponse` (api/etcdserverpb/rpc.proto) {#message-hashkvresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash est la valeur de hachage calculée à partir des clés MVCC du membre répondant jusqu'à une révision donnée. | uint32 |
| compact_revision | compact_revision est la révision compactée du magasin clé-valeur au moment où le hachage commence. | int64 |
| hash_revision | hash_revision est la révision jusqu'à laquelle le hachage est calculé. | int64 |

##### message `HashRequest` (api/etcdserverpb/rpc.proto) {#message-hashrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `HashResponse` (api/etcdserverpb/rpc.proto) {#message-hashresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| hash | hash est la valeur de hachage calculée à partir du backend des données clé-valeur du membre répondant. | uint32 |

##### message `LeaseCheckpoint` (api/etcdserverpb/rpc.proto) {#message-leasecheckpoint-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du bail à sauvegarder. | int64 |
| remaining_TTL | remaining_TTL est le temps restant avant l'expiration du bail. | int64 |

##### message `LeaseCheckpointRequest` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| checkpoints |  | (slice de) LeaseCheckpoint |

##### message `LeaseCheckpointResponse` (api/etcdserverpb/rpc.proto) {#message-leasecheckpointresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseGrantRequest` (api/etcdserverpb/rpc.proto) {#message-leasegrantrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| TTL | TTL est le délai d'expiration conseillé en secondes. Un bail expiré retourne -1. | int64 |
| ID | ID est l'identifiant demandé pour le bail. Si ID est défini à 0, le concessionnaire choisit un identifiant. | int64 |

##### message `LeaseGrantResponse` (api/etcdserverpb/rpc.proto) {#message-leasegrantresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID est l'identifiant de bail pour le bail accordé. | int64 |
| TTL | TTL est le délai de vie (time-to-live) choisi par le serveur, en secondes. | int64 |
| error |  | string |

##### message `LeaseKeepAliveRequest` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliverequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du bail à maintenir actif. | int64 |

##### message `LeaseKeepAliveResponse` (api/etcdserverpb/rpc.proto) {#message-leasekeepaliveresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID est l'identifiant du bail issu de la requête de maintien. | int64 |
| TTL | TTL est le nouveau délai de validité du bail. | int64 |

##### message `LeaseLeasesRequest` (api/etcdserverpb/rpc.proto) {#message-leaseleasesrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `LeaseLeasesResponse` (api/etcdserverpb/rpc.proto) {#message-leaseleasesresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| leases |  | (tranche de) LeaseStatus |

##### message `LeaseRevokeRequest` (api/etcdserverpb/rpc.proto) {#message-leaserevokerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du bail à révoquer. Lorsque l'identifiant est révoqué, toutes les clés associées seront supprimées. | int64 |

##### message `LeaseRevokeResponse` (api/etcdserverpb/rpc.proto) {#message-leaserevokeresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `LeaseStatus` (api/etcdserverpb/rpc.proto) {#message-leasestatus-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID |  | int64 |

##### message `LeaseTimeToLiveRequest` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliverequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du bail. | int64 |
| keys | keys vaut true pour interroger toutes les clés associées à ce bail. | bool |

##### message `LeaseTimeToLiveResponse` (api/etcdserverpb/rpc.proto) {#message-leasetimetoliveresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| ID | ID est l'identifiant du bail issu de la requête de renouvellement. | int64 |
| TTL | TTL est le temps restant en secondes pour le bail ; le bail expirera en moins de TTL+1 secondes. | int64 |
| grantedTTL | GrantedTTL est le délai initial accordé en secondes lors de la création ou du renouvellement du bail. | int64 |
| keys | keys est la liste des clés associées à ce bail. | (slice de) bytes |

##### message `Member` (api/etcdserverpb/rpc.proto) {#message-member-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du membre pour ce membre. | uint64 |
| name | name est le nom lisible par l'humain du membre. Si le membre n'est pas démarré, le nom sera une chaîne vide. | string |
| peerURLs | peerURLs est la liste des URL que le membre expose au cluster pour la communication. | (slice de) string |
| clientURLs | clientURLs est la liste des URL que le membre expose aux clients pour la communication. Si le membre n'est pas démarré, clientURLs sera vide. | (slice de) string |
| isLearner | isLearner indique si le membre est un membre apprenant Raft. | bool |

##### message `MemberAddRequest` (api/etcdserverpb/rpc.proto) {#message-memberaddrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| peerURLs | peerURLs est la liste des URL que le membre ajouté utilisera pour communiquer avec le cluster. | (slice de) chaîne |
| isLearner | isLearner indique si le membre ajouté est un membre apprenant Raft. | bool |

##### message `MemberAddResponse` (api/etcdserverpb/rpc.proto) {#message-memberaddresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| member | member contient les informations du membre ajouté. | Member |
| members | members est la liste de tous les membres après l'ajout du nouveau membre. | (slice de) Member |

##### message `MemberListRequest` (api/etcdserverpb/rpc.proto) {#message-memberlistrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| linearizable |  | bool |

##### message `MemberListResponse` (api/etcdserverpb/rpc.proto) {#message-memberlistresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| membres | membres est une liste de tous les membres associés au cluster. | (liste de) Membre |

##### message `MemberPromoteRequest` (api/etcdserverpb/rpc.proto) {#message-memberpromoterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du membre à promouvoir. | uint64 |

##### message `MemberPromoteResponse` (api/etcdserverpb/rpc.proto) {#message-memberpromoteresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| membres | membres est une liste de tous les membres après la promotion du membre. | (liste de) Member |

##### message `MemberRemoveRequest` (api/etcdserverpb/rpc.proto) {#message-memberremoverequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du membre à supprimer. | uint64 |

##### message `MemberRemoveResponse` (api/etcdserverpb/rpc.proto) {#message-memberremoveresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| membres | membres est une liste de tous les membres après suppression du membre. | (liste de) Member |

##### message `MemberUpdateRequest` (api/etcdserverpb/rpc.proto) {#message-memberupdaterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| ID | ID est l'identifiant du membre à mettre à jour. | uint64 |
| peerURLs | peerURLs est la nouvelle liste d'URLs que le membre utilisera pour communiquer avec le cluster. | (slice de) string |

##### message `MemberUpdateResponse` (api/etcdserverpb/rpc.proto) {#message-memberupdateresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| membres | membres est une liste de tous les membres après mise à jour du membre. | (liste de) Member |

##### message `MoveLeaderRequest` (api/etcdserverpb/rpc.proto) {#message-moveleaderrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| targetID | targetID est l'identifiant du nœud du nouveau leader. | uint64 |

##### message `MoveLeaderResponse` (api/etcdserverpb/rpc.proto) {#message-moveleaderresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |

##### message `PutRequest` (api/etcdserverpb/rpc.proto) {#message-putrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key est la clé, sous forme d'octets, à insérer dans le magasin clé-valeur. | bytes |
| value | value est la valeur, sous forme d'octets, à associer à la clé dans le magasin clé-valeur. | bytes |
| lease | lease est l'identifiant de bail à associer à la clé dans le magasin clé-valeur. Une valeur de bail égale à 0 indique l'absence de bail. | int64 |
| prev_kv | Si prev_kv est défini, etcd récupère la paire clé-valeur précédente avant de la modifier. La paire clé-valeur précédente est renvoyée dans la réponse de mise à jour. | bool |
| ignore_value | Si ignore_value est défini, etcd met à jour la clé en utilisant sa valeur actuelle. Retourne une erreur si la clé n'existe pas. | bool |
| ignore_lease | Si ignore_lease est défini, etcd met à jour la clé en utilisant son bail actuel. Retourne une erreur si la clé n'existe pas. | bool |

##### message `PutResponse` (api/etcdserverpb/rpc.proto) {#message-putresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| prev_kv | Si prev_kv est défini dans la requête, la paire clé-valeur précédente sera renvoyée. | mvccpb.KeyValue |

##### message `RangeRequest` (api/etcdserverpb/rpc.proto) {#message-rangerequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key est la première clé de la plage. Si range_end n'est pas fourni, la requête ne recherche que key. | bytes |
| range_end | range_end est la borne supérieure de la plage demandée [key, range_end). Si range_end est '\0', la plage comprend toutes les clés >= key. Si range_end est key plus un (par exemple, "aa"+1 == "ab", "a\xff"+1 == "b"), la requête retourne toutes les clés ayant key comme préfixe. Si key et range_end sont tous deux '\0', la requête retourne toutes les clés. | bytes |
| limit | limit est une limite sur le nombre de clés retournées par la requête. Si limit est défini à 0, il n'y a pas de limite. | int64 |
| revision | revision est le point dans le temps du magasin clé-valeur à utiliser pour la plage. Si revision est inférieur ou égal à zéro, la plage porte sur le magasin clé-valeur le plus récent. Si la révision a été compactée, la réponse renvoie ErrCompacted. | int64 |
| sort_order | sort_order est l'ordre des résultats triés retournés. | SortOrder |
| sort_target | sort_target est le champ clé-valeur à utiliser pour le tri. | SortTarget |
| serializable | serializable définit la requête de plage pour utiliser des lectures locales sérialisables. Les requêtes de plage sont linéarisables par défaut ; les requêtes linéarisables ont une latence plus élevée et un débit plus faible que les requêtes sérialisables, mais reflètent le consensus actuel du cluster. Pour de meilleures performances, au prix de lectures potentiellement obsolètes, une requête de plage sérialisable est servie localement sans nécessiter de consensus avec les autres nœuds du cluster. | bool |
| keys_only | keys_only, lorsqu'il est défini, retourne uniquement les clés et non les valeurs. | bool |
| count_only | count_only, lorsqu'il est défini, retourne uniquement le nombre de clés dans la plage. | bool |
| min_mod_revision | min_mod_revision est la borne inférieure des révisions de modification des clés retournées ; toutes les clés ayant une révision de modification inférieure sont filtrées. | int64 |
| max_mod_revision | max_mod_revision est la borne supérieure des révisions de modification des clés retournées ; toutes les clés ayant une révision de modification supérieure sont filtrées. | int64 |
| min_create_revision | min_create_revision est la borne inférieure des révisions de création des clés retournées ; toutes les clés ayant une révision de création inférieure sont filtrées. | int64 |
| max_create_revision | max_create_revision est la borne supérieure des révisions de création des clés retournées ; toutes les clés ayant une révision de création supérieure sont filtrées. | int64 |

##### message `RangeResponse` (api/etcdserverpb/rpc.proto) {#message-rangeresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| kvs | kvs est la liste des paires clé-valeur correspondant à la requête de plage. kvs est vide lorsque le comptage est demandé. | (slice de) mvccpb.KeyValue |
| more | more indique s'il reste d'autres clés à renvoyer dans la plage demandée. | bool |
| count | count est défini sur le nombre réel de clés présentes dans la plage lorsqu'une requête de comptage est effectuée. Contrairement à Kvs, il n'est pas affecté par les limites ni les filtres (par exemple, Min/Max, Création/Modification, Révisions) et reflète le comptage complet dans la plage spécifiée. | int64 |

##### message `RequestOp` (api/etcdserverpb/rpc.proto) {#message-requestop-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request | request est une union de types de requête acceptés par une transaction. | oneof |
| request_range |  | RangeRequest |
| request_put |  | PutRequest |
| request_delete_range |  | DeleteRangeRequest |
| request_txn |  | TxnRequest |

##### message `ResponseHeader` (api/etcdserverpb/rpc.proto) {#message-responseheader-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| cluster_id | cluster_id est l'identifiant du cluster qui a envoyé la réponse. | uint64 |
| member_id | member_id est l'identifiant du membre qui a envoyé la réponse. | uint64 |
| revision | revision est la révision du magasin clé-valeur au moment où la requête a été appliquée, et elle est non définie (donc 0) en cas d'appels n'interagissant pas avec le magasin clé-valeur. Pour les réponses de progression de surveillance, le champ header.revision indique la progression. Tous les événements futurs reçus sur ce flux sont garantis d'avoir un numéro de révision strictement supérieur au numéro de révision header.revision. | int64 |
| raft_term | raft_term est le terme Raft au moment où la requête a été appliquée. | uint64 |

##### message `ResponseOp` (api/etcdserverpb/rpc.proto) {#message-responseop-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| response | response est une union de types de réponse retournés par une transaction. | oneof |
| response_range |  | RangeResponse |
| response_put |  | PutResponse |
| response_delete_range |  | DeleteRangeResponse |
| response_txn |  | TxnResponse |

##### message `SnapshotRequest` (api/etcdserverpb/rpc.proto) {#message-snapshotrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `SnapshotResponse` (api/etcdserverpb/rpc.proto) {#message-snapshotresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header | header contient les informations actuelles du magasin clé-valeur. Le premier header dans le flux d'instantané indique le moment précis de l'instantané. | ResponseHeader |
| remaining_bytes | remaining_bytes est le nombre d'octets de données binaires à envoyer après ce message | uint64 |
| blob | blob contient le morceau suivant de l'instantané dans le flux d'instantané. | bytes |
| version | version locale du serveur qui a créé l'instantané. Dans un cluster avec des binaires de versions différentes, chaque cluster peut renvoyer un résultat différent. Indique quelle version du serveur etcd doit être utilisée pour restaurer l'instantané. | string |

##### message `StatusRequest` (api/etcdserverpb/rpc.proto) {#message-statusrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `StatusResponse` (api/etcdserverpb/rpc.proto) {#message-statusresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| version | version est la version du protocole du cluster utilisée par le membre répondant. | string |
| dbSize | dbSize est la taille de la base de données du backend physiquement allouée, en octets, du membre répondant. | int64 |
| leader | leader est l'identifiant du membre que le membre répondant considère comme leader actuel. | uint64 |
| raftIndex | raftIndex est l'index de validation Raft actuel du membre répondant. | uint64 |
| raftTerm | raftTerm est le terme Raft actuel du membre répondant. | uint64 |
| raftAppliedIndex | raftAppliedIndex est l'index appliqué Raft actuel du membre répondant. | uint64 |
| errors | errors contient les informations et l'état d'alarme/santé. | (slice de) string |
| dbSizeInUse | dbSizeInUse est la taille de la base de données du backend logiquement utilisée, en octets, du membre répondant. | int64 |
| isLearner | isLearner indique si le membre est un membre apprenant Raft. | bool |
| storageVersion | storageVersion est la version du fichier de base de données. Elle peut être mise à jour avec un délai par rapport à la version cible du cluster. | string |
| dbSizeQuota | dbSizeQuota est la limite de stockage etcd configurée en octets (valeur passée à l'instance etcd par le drapeau --quota-backend-bytes) | int64 |
| downgradeInfo | downgradeInfo indique s'il existe un processus de rétrogradation. | DowngradeInfo |

##### message `TxnRequest` (api/etcdserverpb/rpc.proto) {#message-txnrequest-apietcdserverpbrpcproto}

Du papier Google PaxosDB : Notre implémentation repose sur une primitive puissante que nous appelons MultiOp. Toutes les autres opérations sur la base de données, à l’exception de l’itération, sont implémentées comme un appel unique à MultiOp. Un MultiOp est appliqué de manière atomique et se compose de trois composants : 1. Une liste de tests appelée garde. Chaque test dans la garde vérifie une entrée unique dans la base de données. Il peut vérifier l’absence ou la présence d’une valeur, ou comparer avec une valeur donnée. Deux tests différents dans la garde peuvent s’appliquer à la même ou à des entrées différentes dans la base de données. Tous les tests de la garde sont appliqués, et MultiOp retourne les résultats. Si tous les tests sont vrais, MultiOp exécute l’opération t op (voir l’élément 2 ci-dessous), sinon il exécute l’opération f op (voir l’élément 3 ci-dessous). 2. Une liste d’opérations sur la base de données appelée t op. Chaque opération de la liste est soit une opération d’insertion, de suppression ou de recherche, et s’applique à une seule entrée de la base de données. Deux opérations différentes de la liste peuvent s’appliquer à la même ou à des entrées différentes dans la base de données. Ces opérations sont exécutées si la garde évalue à vrai. 3. Une liste d’opérations sur la base de données appelée f op. Comme t op, mais exécutée si la garde évalue à faux.

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| compare | compare est une liste de prédicats représentant une conjonction de termes. Si les comparaisons réussissent, les requêtes réussies seront traitées dans l'ordre, et la réponse contiendra leurs réponses respectives dans l'ordre. Si les comparaisons échouent, les requêtes échouées seront traitées dans l'ordre, et la réponse contiendra leurs réponses respectives dans l'ordre. | (liste de) Compare |
| success | success est une liste de requêtes qui seront appliquées lorsque compare évalue à true. | (liste de) RequestOp |
| failure | failure est une liste de requêtes qui seront appliquées lorsque compare évalue à false. | (liste de) RequestOp |

##### message `TxnResponse` (api/etcdserverpb/rpc.proto) {#message-txnresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| succeeded | succeeded est défini à true si la comparaison a été évaluée à true, ou à false sinon. | bool |
| responses | responses est une liste de réponses correspondant aux résultats de l'application de succès si succeeded est true, ou d'échec si succeeded est false. | (slice de) ResponseOp |

##### message `WatchCancelRequest` (api/etcdserverpb/rpc.proto) {#message-watchcancelrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| watch_id | watch_id est l'identifiant de l'observateur à annuler afin qu'aucun événement supplémentaire ne soit transmis. | int64 |

##### message `WatchCreateRequest` (api/etcdserverpb/rpc.proto) {#message-watchcreaterequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| key | key est la clé à enregistrer pour la surveillance. | bytes |
| range_end | range_end est la fin de la plage [key, range_end) à surveiller. Si range_end n'est pas fourni, seule la clé spécifiée est surveillée. Si range_end est égal à '\0', toutes les clés supérieures ou égales à la clé spécifiée sont surveillées. Si range_end est supérieure d'un bit à la clé donnée, toutes les clés ayant le préfixe (la clé donnée) sont surveillées. | bytes |
| start_revision | start_revision est une révision facultative à partir de laquelle commencer la surveillance (inclusivement). Aucune valeur de start_revision signifie « maintenant ». | int64 |
| progress_notify | progress_notify est défini afin que le serveur etcd envoie périodiquement une réponse de surveillance sans événements à l'observateur si aucun événement récent n'a eu lieu. Cela est utile lorsque les clients souhaitent récupérer un observateur déconnecté à partir d'une révision connue récente. Le serveur etcd peut décider de la fréquence à laquelle il envoie les notifications en fonction de la charge actuelle. | bool |
| filters | filters filtre les événements côté serveur avant leur envoi à l'observateur. | (slice de) FilterType |
| prev_kv | Si prev_kv est défini, l'observateur créé reçoit la paire clé-valeur précédente avant l'événement. Si la paire clé-valeur précédente a déjà été compactée, rien n'est retourné. | bool |
| watch_id | Si watch_id est fourni et non nul, il sera attribué à cet observateur. Étant donné que la création d'un observateur dans etcd n'est pas une opération synchrone, cela permet d'assurer un ordre correct lors de la création de plusieurs observateurs sur le même flux. La création d'un observateur avec un ID déjà utilisé sur le flux provoque une erreur. | int64 |
| fragment | fragment permet de diviser de grandes révisions en plusieurs réponses de surveillance. | bool |

##### message `WatchProgressRequest` (api/etcdserverpb/rpc.proto) {#message-watchprogressrequest-apietcdserverpbrpcproto}

Demande que le statut d’avancement du flux de surveillance soit envoyé dans le flux de réponse de surveillance dès que possible.

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |

##### message `WatchRequest` (api/etcdserverpb/rpc.proto) {#message-watchrequest-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| request_union | request_union est une requête visant à créer un nouvel observateur ou à annuler un observateur existant. | oneof |
| create_request |  | WatchCreateRequest |
| cancel_request |  | WatchCancelRequest |
| progress_request |  | WatchProgressRequest |

##### message `WatchResponse` (api/etcdserverpb/rpc.proto) {#message-watchresponse-apietcdserverpbrpcproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| (versionpb.etcd_version_msg) |  | option |
| header |  | ResponseHeader |
| watch_id | watch_id est l'identifiant de l'observateur correspondant à la réponse. | int64 |
| created | created est défini à true si la réponse correspond à une requête de création d'observateur. Le client doit enregistrer l'identifiant d'observateur et s'attendre à recevoir des événements pour l'observateur créé depuis le même flux. Tous les événements envoyés à l'observateur créé seront associés au même watch_id. | bool |
| canceled | canceled est défini à true si la réponse correspond à une requête d'annulation d'observateur ou si la révision de départ a déjà été compactée. Aucun événement supplémentaire ne sera envoyé à l'observateur annulé. | bool |
| compact_revision | compact_revision est défini à l'index minimum si un observateur tente de surveiller à une révision compactée. Cela se produit lorsqu'un observateur est créé à une révision compactée ou lorsque l'observateur ne parvient pas à suivre l'évolution du magasin clé-valeur. Le client doit traiter l'observateur comme annulé et ne pas tenter de créer un nouvel observateur avec la même révision de départ. | int64 |
| cancel_reason | cancel_reason indique la raison de l'annulation de l'observateur. | string |
| fragment | fragment est défini à true si une réponse de surveillance importante a été divisée en plusieurs réponses. | bool |
| events |  | (slice de) mvccpb.Event |

##### message `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| type | type est le type d'événement. Si type est un PUT, cela indique que de nouvelles données ont été stockées pour la clé. Si type est un DELETE, cela indique que la clé a été supprimée. | EventType |
| kv | kv contient le KeyValue associé à l'événement. Un événement PUT contient la paire clé-valeur actuelle. Un événement PUT avec kv.Version=1 indique la création d'une clé. Un événement DELETE/EXPIRE contient la clé supprimée, avec sa révision de modification définie à la révision de la suppression. | KeyValue |
| prev_kv | prev_kv contient la paire clé-valeur avant l'événement. | KeyValue |

##### message `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| key | key est la clé sous forme d'octets. Une clé vide n'est pas autorisée. | octets |
| create_revision | create_revision est la révision de la dernière création sur cette clé. | int64 |
| mod_revision | mod_revision est la révision de la dernière modification sur cette clé. | int64 |
| version | version est la version de la clé. Une suppression réinitialise la version à zéro, et toute modification de la clé augmente sa version. | int64 |
| value | value est la valeur stockée par la clé, sous forme d'octets. | octets |
| lease | lease est l'ID du bail associé à la clé. Lorsque le bail associé expire, la clé sera supprimée. Si lease vaut 0, aucun bail n'est associé à la clé. | int64 |

##### message `Lease` (server/lease/leasepb/lease.proto) {#message-lease-serverleaseleasepbleaseproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| ID |  | int64 |
| TTL |  | int64 |
| RemainingTTL |  | int64 |

##### message `LeaseInternalRequest` (server/lease/leasepb/lease.proto) {#message-leaseinternalrequest-serverleaseleasepbleaseproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| LeaseTimeToLiveRequest |  | etcdserverpb.LeaseTimeToLiveRequest |

##### message `LeaseInternalResponse` (server/lease/leasepb/lease.proto) {#message-leaseinternalresponse-serverleaseleasepbleaseproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| LeaseTimeToLiveResponse |  | etcdserverpb.LeaseTimeToLiveResponse |

##### message `Permission` (api/authpb/auth.proto) {#message-permission-apiauthpbauthproto}

Les autorisations constituent une entité unique

| Champ | Description | Type |
| ----- | ----------- | ---- |
| permType |  | Type |
| key |  | bytes |
| range_end |  | bytes |

##### message `Role` (api/authpb/auth.proto) {#message-role-apiauthpbauthproto}

Le rôle est une entrée unique dans le bac authRoles

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name |  | bytes |
| keyPermission |  | (tranche de) Permission |

##### message `User` (api/authpb/auth.proto) {#message-user-apiauthpbauthproto}

Utilisateur est une entrée unique dans le bucket authUsers

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name |  | bytes |
| password |  | bytes |
| roles |  | (tranche de) string |
| options |  | UserAddOptions |

##### message `UserAddOptions` (api/authpb/auth.proto) {#message-useraddoptions-apiauthpbauthproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| no_password |  | bool |
