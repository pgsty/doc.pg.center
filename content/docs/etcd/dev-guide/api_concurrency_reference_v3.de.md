---
title: "API-Referenz: Nebenläufigkeit"
weight: 3900
description: "Referenz der APIs für Nebenläufigkeit in etcd"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
aliases: [/etcd/dev-guide/api_concurrency_reference_v3/]
---

Diese API-Referenz wird automatisch aus den angegebenen `.proto`-Dateien erzeugt.

##### Dienst `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

Der Lock-Dienst stellt clientseitige Sperrfunktionen als gRPC-Schnittstelle bereit.

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | Lock erwirbt eine verteilte gemeinsame Sperre für einen bestimmten Sperrnamen. Bei Erfolg gibt es einen eindeutigen Schlüssel zurück, der so lange existiert, wie der Aufrufer die Sperre hält. Mit diesem Schlüssel und Transaktionen lässt sich zuverlässig sicherstellen, dass etcd nur aktualisiert wird, während der Aufrufer die Sperre besitzt. Die Sperre wird gehalten, bis Unlock für den Schlüssel aufgerufen wird oder die dem Besitzer zugeordnete Lease abläuft. |
| Unlock | UnlockRequest | UnlockResponse | Unlock nimmt einen von Lock zurückgegebenen Schlüssel entgegen und gibt die Sperre frei. Anschließend wird der nächste auf die Sperre wartende Lock-Aufrufer geweckt und erhält die Sperre. |

##### Nachricht `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name | name ist der Bezeichner der zu erwerbenden verteilten gemeinsamen Sperre. | bytes |
| lease | lease ist die ID der Lease, die dem Besitz der Sperre zugeordnet wird. Läuft die Lease ab oder wird sie widerrufen, während sie die Sperre hält, wird die Sperre automatisch freigegeben. Aufrufe von Lock mit derselben Lease werden als einmaliger Erwerb behandelt; zweimaliges Sperren mit derselben Lease hat keine zusätzliche Wirkung. | int64 |

##### Nachricht `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | key ist ein Schlüssel, der in etcd existiert, solange der Lock-Aufrufer die Sperre besitzt. Benutzer sollten diesen Schlüssel nicht ändern, da die Sperre sonst ein undefiniertes Verhalten zeigen kann. | bytes |

##### Nachricht `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| key | key ist der von Lock vergebene Schlüssel, der den Besitz der Sperre repräsentiert. | bytes |

##### Nachricht `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### Dienst `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

Der Election-Dienst stellt clientseitige Wahlfunktionen als gRPC-Schnittstelle bereit.

| Methode | Anfragetyp | Antworttyp | Beschreibung |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | Campaign wartet darauf, bei einer Wahl die Führung zu übernehmen, und gibt bei Erfolg einen LeaderKey zurück, der die Führungsrolle repräsentiert. Der LeaderKey kann anschließend verwendet werden, um neue Werte für die Wahl zu veröffentlichen, API-Anfragen durch Transaktionen vom fortbestehenden Besitz der Führungsrolle abhängig zu machen und von der Führungsrolle zurückzutreten. |
| Proclaim | ProclaimRequest | ProclaimResponse | Proclaim ersetzt den vom Leader veröffentlichten Wert durch einen neuen Wert. |
| Leader | LeaderRequest | LeaderResponse | Leader gibt den aktuell für die Wahl veröffentlichten Wert zurück, sofern vorhanden. |
| Observe | LeaderRequest | LeaderResponse | Observe überträgt die von den gewählten Leadern veröffentlichten Werte in ihrer Reihenfolge als Stream. |
| Resign | ResignRequest | ResignResponse | Resign gibt die Führungsrolle der Wahl frei, sodass andere Kandidaten sie übernehmen können. |

##### Nachricht `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name | name ist der Bezeichner der Wahl, für die die Kandidatur gilt. | bytes |
| lease | lease ist die ID der Lease, die der Führungsrolle der Wahl zugeordnet ist. Läuft die Lease vor dem Rücktritt ab oder wird sie widerrufen, geht die Führungsrolle auf den nächsten Kandidaten über, sofern vorhanden. | int64 |
| value | value ist der anfänglich veröffentlichte Wert, der gesetzt wird, wenn der Kandidat die Wahl gewinnt. | bytes |

##### Nachricht `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader beschreibt die Ressourcen, die zum Halten der Führungsrolle der Wahl verwendet werden. | LeaderKey |

##### Nachricht `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name | name ist der Wahlbezeichner, der dem Schlüssel für die Führungsrolle entspricht. | bytes |
| key | key ist ein opaker Schlüssel, der den Besitz der Führungsrolle der Wahl repräsentiert. Wird der Schlüssel gelöscht, geht die Führungsrolle verloren. | bytes |
| rev | rev ist die Erstellungsrevision des Schlüssels. In Transaktionen lässt sich damit der Besitz der Führungsrolle prüfen, indem die Erstellungsrevision des Schlüssels mit rev verglichen wird. | int64 |
| lease | lease ist die Lease-ID des gewählten Leaders. | int64 |

##### Nachricht `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| name | name ist der Wahlbezeichner für die Informationen zur Führungsrolle. | bytes |

##### Nachricht `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv ist das Schlüssel-Wert-Paar, das die neueste Aktualisierung des Leaders repräsentiert. | mvccpb.KeyValue |

##### Nachricht `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| leader | leader repräsentiert den Besitz der Führungsrolle der Wahl. | LeaderKey |
| value | value ist eine Aktualisierung, die den aktuellen Wert des Leaders überschreiben soll. | bytes |

##### Nachricht `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### Nachricht `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| leader | leader ist die Führungsrolle, die durch den Rücktritt aufgegeben werden soll. | LeaderKey |

##### Nachricht `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| Feld | Beschreibung | Typ |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

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
