---
title: "Référence API : concurrence"
weight: 3900
description: "Référence des API de concurrence etcd"
categories: [Référence]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

Cette référence d'API est générée automatiquement à partir des fichiers nommés `.proto`.

##### service `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

Le service de verrouillage expose des fonctionnalités de verrouillage côté client sous forme d'une interface gRPC.

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lock acquiert un verrou partagé distribué sur un verrou nommé donné. En cas de succès, elle retourne une clé unique qui reste existante tant que le verrou est détenu par l'appelant. Cette clé peut être utilisée conjointement avec des transactions afin de garantir en toute sécurité que les mises à jour sur etcd ne s'effectuent qu'en tenant le verrou. Le verrou est détenu jusqu'à ce que Unlock soit appelé sur la clé ou que le bail associé au propriétaire expire. |
| Unlock | UnlockRequest | UnlockResponse | Unlock prend une clé retournée par Lock et libère la possession du verrou. Le prochain appelant de Lock en attente du verrou est alors réveillé et obtient la possession du verrou. |

##### message `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name | name est l'identifiant de la verrouille partagée distribuée à acquérir. | bytes |
| lease | lease est l'ID du bail qui sera attaché à la possession du verrou. Si le bail expire ou est révoqué et qu'il détient actuellement le verrou, celui-ci est automatiquement libéré. Les appels à Lock avec le même bail seront traités comme une seule acquisition ; verrouiller deux fois avec le même bail est sans effet. | int64 |

##### message `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | key est une clé qui existera dans etcd pendant toute la durée où l'appelant du verrou détient le verrou. Les utilisateurs ne doivent pas modifier cette clé, sinon le verrou peut présenter un comportement indéfini. | bytes |

##### message `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| key | key est la clé d'acquisition du verrou octroyée par Lock. | bytes |

##### message `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### service `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

Le service d'élection expose des fonctionnalités d'élection côté client sous forme d'une interface gRPC.

| Méthode | Type de requête | Type de réponse | Description |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaign attend d'acquérir le leadership lors d'une élection, en retournant une clé de leader représentant le leadership si l'opération réussit. Cette clé de leader peut ensuite être utilisée pour publier de nouvelles valeurs dans l'élection, protéger transactionnellement les requêtes d'API en fonction du maintien du leadership, ou se retirer de l'élection. |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaim met à jour la valeur publiée par le leader avec une nouvelle valeur. |
| Leader | LeaderRequest | LeaderResponse | Leader retourne la proclamation actuelle de l'élection, le cas échéant. |
| Observe | LeaderRequest | LeaderResponse | Observe diffuse les proclamations d'élection dans l'ordre, telles qu'elles sont émises par les leaders élus. |
| Resign | ResignRequest | ResignResponse | Resign libère le leadership de l'élection afin que d'autres candidats puissent acquérir le leadership. |

##### message `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name | name est l'identifiant de l'élection pour la campagne. | bytes |
| lease | lease est l'ID du bail associé à la direction de l'élection. Si le bail expire ou est révoqué avant la démission de la direction, la direction est transférée au prochain candidat, le cas échéant. | int64 |
| value | value est la valeur déclarée initiale définie lorsque le candidat remporte l'élection. | bytes |

##### message `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader décrit les ressources utilisées pour la détention du rôle de leader lors de l'élection. | LeaderKey |

##### message `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name | name est l'identifiant d'élection correspondant à la clé de leadership. | bytes |
| key | key est une clé opaque représentant la possession de l'élection. Si la clé est supprimée, le leadership est perdu. | bytes |
| rev | rev est la révision de création de la clé. Elle peut être utilisée pour vérifier la possession d'une élection au cours de transactions en testant que la révision de création de la clé correspond à rev. | int64 |
| lease | lease est l'ID du bail du leader de l'élection. | int64 |

##### message `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| name | name est l'identifiant d'élection pour les informations de leadership. | bytes |

##### message `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv est la paire clé-valeur représentant la mise à jour récente du leader. | mvccpb.KeyValue |

##### message `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| leader | leader est la détenue du leadership lors de l'élection. | LeaderKey |
| value | value est une mise à jour destinée à remplacer la valeur actuelle du leader. | bytes |

##### message `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### message `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| leader | leader est la prise de leadership à abandonner par démission. | LeaderKey |

##### message `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### message `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| type | type est le type d'événement. Si type est un PUT, cela indique que de nouvelles données ont été stockées pour la clé. Si type est un DELETE, cela indique que la clé a été supprimée. | EventType |
| kv | kv contient la paire clé-valeur pour l'événement. Un événement PUT contient la paire clé-valeur actuelle. Un événement PUT avec kv.Version=1 indique la création d'une clé. Un événement DELETE/EXPIRE contient la clé supprimée, avec sa révision de modification définie à la révision de la suppression. | KeyValue |
| prev_kv | prev_kv contient la paire clé-valeur avant l'événement. | KeyValue |

##### message `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| Champ | Description | Type |
| ----- | ----------- | ---- |
| key | key est la clé sous forme d'octets. Une clé vide n'est pas autorisée. | octets |
| create_revision | create_revision est la révision de la dernière création sur cette clé. | int64 |
| mod_revision | mod_revision est la révision de la dernière modification sur cette clé. | int64 |
| version | version est la version de la clé. Une suppression réinitialise la version à zéro, et toute modification de la clé augmente sa version. | int64 |
| value | value est la valeur stockée par la clé, sous forme d'octets. | octets |
| bail | bail est l'ID du bail associé à la clé. Lorsque le bail associé expire, la clé sera supprimée. Si bail est 0, aucun bail n'est associé à la clé. | int64 |
