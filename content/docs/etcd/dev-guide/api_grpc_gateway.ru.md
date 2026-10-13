---
title: Зачем нужен шлюз gRPC
weight: 3375
description: Почему стоит использовать шлюз gRPC
categories: [Концепция]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
aliases: [/etcd/dev-guide/api_grpc_gateway/]
---

etcd v3 использует [gRPC][grpc] как протокол обмена сообщениями. Проект etcd
включает основанный на gRPC [клиент Go][go-client] и утилиту командной строки
[etcdctl][etcdctl] для взаимодействия с кластером etcd через gRPC. Для языков
без поддержки gRPC etcd предоставляет JSON-[шлюз gRPC][grpc-gateway]. Он служит
RESTful-прокси, преобразующим запросы HTTP/JSON в сообщения gRPC.

## Использование шлюза gRPC {#using-grpc-gateway}

Шлюз принимает [JSON-сопоставление][json-mapping] определений сообщений
[protocol buffer][api-ref] etcd. Поля `key` и `value` определены как массивы
байтов, поэтому в JSON их обязательно кодировать в base64. В следующих примерах
используется `curl`, но подойдёт любой клиент HTTP/JSON.

### Примечания {#notes}

Конечная точка шлюза gRPC менялась начиная с etcd v3.3:

- etcd v3.2 и более ранние версии используют только `[CLIENT-URL]/v3alpha/*`.
- etcd v3.3 использует `[CLIENT-URL]/v3beta/*`, сохраняя `[CLIENT-URL]/v3alpha/*`.
- etcd v3.4 использует `[CLIENT-URL]/v3/*`, сохраняя `[CLIENT-URL]/v3beta/*`.
  - **`[CLIENT-URL]/v3alpha/*` устарел**.
- etcd v3.5 и более поздние версии используют только `[CLIENT-URL]/v3/*`.
  - **`[CLIENT-URL]/v3beta/*` устарел**.

gRPC-gateway не поддерживает аутентификацию по Common Name сертификата TLS.

### Запись и получение ключей {#put-and-get-keys}

Для чтения и записи ключей используйте службы `/v3/kv/range` и `/v3/kv/put`:

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

### Наблюдение за ключами {#watch-keys}

Для наблюдения за ключами используйте службу `/v3/watch`:

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### Транзакции {#transactions}

Выполните транзакцию через `/v3/kv/txn`:

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

### Аутентификация {#authentication}

Настройте аутентификацию с помощью службы `/v3/auth`:

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

Получите токен аутентификации etcd через `/v3/auth/authenticate`:

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

Чтобы получить ключ с учётными данными аутентификации, задайте токен в заголовке `Authorization`:

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### Ответы об ошибках {#error-responses}

Шлюз gRPC преобразует статус gRPC в код состояния HTTP и тело ошибки JSON.
Начиная с etcd v3.6, обновление до grpc-gateway v2 изменило обработку ошибок
(см. [примечание об обработке ошибок][grpc-gateway-v2-errors] в руководстве по
миграции на v2), и теперь поведение шлюза соответствует `google.rpc.Status`
(code, message, details), как описано в [модели ошибок API Google][google-api-errors].
В старых версиях grpc-gateway также присутствовало поле верхнего уровня `error`,
но etcd v3.6 и более новые версии его не поддерживают.

Клиентам следует считать код состояния HTTP главным признаком успеха или ошибки.
При ошибке запроса основным источником сведений следует считать поле `message`, а
любые дополнительные данные использовать для дальнейшего контекста.

## Swagger {#swagger}

Сгенерированные определения API [Swagger][swagger] находятся в [rpc.swagger.json][swagger-doc].

[api-ref]: /ru/docs/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /docs/etcd/dev-guide/apispec/swagger/rpc.swagger.json
