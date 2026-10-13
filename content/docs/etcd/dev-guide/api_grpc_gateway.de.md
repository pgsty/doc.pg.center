---
title: Warum ein gRPC-Gateway
weight: 3375
description: Gründe für die Verwendung des gRPC-Gateways
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
aliases: [/etcd/dev-guide/api_grpc_gateway/]
---

etcd v3 verwendet [gRPC][grpc] als Nachrichtenprotokoll. Das etcd-Projekt enthält einen gRPC-basierten [Go-Client][go-client] und das Befehlszeilenwerkzeug [etcdctl][etcdctl] zur Kommunikation mit einem etcd-Cluster über gRPC. Für Sprachen ohne gRPC-Unterstützung stellt etcd ein JSON-[gRPC-Gateway][grpc-gateway] bereit. Dieses Gateway dient als RESTful-Proxy, der HTTP/JSON-Anfragen in gRPC-Nachrichten übersetzt.

## Das gRPC-Gateway verwenden {#using-grpc-gateway}

Das Gateway akzeptiert eine [JSON-Abbildung][json-mapping] der [Protocol-Buffer][api-ref]-Nachrichtendefinitionen von etcd. Die Felder `key` und `value` sind als Byte-Arrays definiert und müssen deshalb in JSON base64-kodiert sein. Die folgenden Beispiele verwenden `curl`, jeder andere HTTP/JSON-Client sollte jedoch ebenso funktionieren.

### Hinweise {#notes}

Der Endpunkt des gRPC-Gateways hat sich seit etcd v3.3 geändert:

- etcd v3.2 und frühere Versionen verwenden ausschließlich `[CLIENT-URL]/v3alpha/*`.
- etcd v3.3 verwendet `[CLIENT-URL]/v3beta/*` und behält `[CLIENT-URL]/v3alpha/*` bei.
- etcd v3.4 verwendet `[CLIENT-URL]/v3/*` und behält `[CLIENT-URL]/v3beta/*` bei.
  - **`[CLIENT-URL]/v3alpha/*` ist veraltet**.
- etcd v3.5 und spätere Versionen verwenden ausschließlich `[CLIENT-URL]/v3/*`.
  - **`[CLIENT-URL]/v3beta/*` ist veraltet**.

Das gRPC-Gateway unterstützt keine Authentifizierung über den TLS Common Name.

### Schlüssel schreiben und lesen {#put-and-get-keys}

Die Dienste `/v3/kv/range` und `/v3/kv/put` zum Lesen und Schreiben von Schlüsseln verwenden:

```bash
<<COMMENT
https://www.base64encode.org/
foo is 'Zm9v' in Base64
bar is 'YmFy'
COMMENT

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"}}

curl -L http://localhost:2379/v3/kv/range \
  -X POST -d '{"key": "Zm9v"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}],"count":"1"}

# get all keys prefixed with "foo"
curl -L http://localhost:2379/v3/kv/range \
  -X POST -d '{"key": "Zm9v", "range_end": "Zm9w"}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"3"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}],"count":"1"}
```

### Schlüssel beobachten {#watch-keys}

Den Dienst `/v3/watch` zum Beobachten von Schlüsseln verwenden:

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### Transaktionen {#transactions}

Eine Transaktion mit `/v3/kv/txn` ausführen:

```bash
# target CREATE
curl -L http://localhost:2379/v3/kv/txn \
  -X POST \
  -d '{"compare":[{"target":"CREATE","key":"Zm9v","createRevision":"2"}],"success":[{"requestPut":{"key":"Zm9v","value":"YmFy"}}]}'
# {"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"3","raft_term":"2"},"succeeded":true,"responses":[{"response_put":{"header":{"revision":"3"}}}]}
```

```bash
# target VERSION
curl -L http://localhost:2379/v3/kv/txn \
  -X POST \
  -d '{"compare":[{"version":"4","result":"EQUAL","target":"VERSION","key":"Zm9v"}],"success":[{"requestRange":{"key":"Zm9v"}}]}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"6","raft_term":"3"},"succeeded":true,"responses":[{"response_range":{"header":{"revision":"6"},"kvs":[{"key":"Zm9v","create_revision":"2","mod_revision":"6","version":"4","value":"YmF6"}],"count":"1"}}]}
```

### Authentifizierung {#authentication}

Die Authentifizierung mit dem Dienst `/v3/auth` einrichten:

```bash
# create root user
curl -L http://localhost:2379/v3/auth/user/add \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# create root role
curl -L http://localhost:2379/v3/auth/role/add \
  -X POST -d '{"name": "root"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# grant root role
curl -L http://localhost:2379/v3/auth/user/grant \
  -X POST -d '{"user": "root", "role": "root"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}

# enable auth
curl -L http://localhost:2379/v3/auth/enable -X POST -d '{}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"}}
```

Mit `/v3/auth/authenticate` bei etcd authentifizieren, um ein Authentifizierungstoken zu erhalten:

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

Den Header `Authorization` auf das Authentifizierungstoken setzen, um einen Schlüssel mit Authentifizierungsdaten abzurufen:

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### Fehlerantworten {#error-responses}

Das gRPC-Gateway übersetzt den gRPC-Status in HTTP-Statuscodes und einen JSON-Fehlerinhalt.
Ab etcd v3.6 änderte die Aktualisierung auf grpc-gateway v2 die Fehlerbehandlung
(siehe den [Hinweis zur Fehlerbehandlung][grpc-gateway-v2-errors] im v2-Migrationsleitfaden).
Das Verhalten des Gateways entspricht nun `google.rpc.Status` (code, message,
details), wie im [API-Fehlermodell von Google][google-api-errors] beschrieben.
Ältere grpc-gateway-Versionen enthielten außerdem ein `error`-Feld
auf oberster Ebene. Dieses Feld wird in etcd v3.6 und neueren Versionen nicht unterstützt.

Clients sollten den HTTP-Statuscode als vorrangigen Hinweis auf Erfolg oder
Fehlschlag behandeln. Schlägt eine Anfrage fehl, sollten Clients das Feld `message`
als wichtigste Quelle für Fehlerinformationen verwenden und zusätzliche Details
zur weiteren Einordnung heranziehen.

## Swagger {#swagger}

Generierte [Swagger][swagger]-API-Definitionen stehen unter [rpc.swagger.json][swagger-doc] bereit.

[api-ref]: /de/docs/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /docs/etcd/dev-guide/apispec/swagger/rpc.swagger.json
