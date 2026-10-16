---
title: Por qué usar la pasarela gRPC
weight: 3375
description: Por qué considerar el uso de la pasarela gRPC
categories: [Concepto]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
---

etcd v3 usa [gRPC][grpc] como protocolo de mensajería. El proyecto etcd incluye un cliente [Go][go-client] basado en gRPC y una utilidad de línea de comandos, [etcdctl][etcdctl], para comunicarse con un clúster de etcd a través de gRPC. Para los lenguajes sin soporte de gRPC, etcd proporciona una [pasarela gRPC][grpc-gateway] en JSON. Esta pasarela ofrece un proxy RESTful que traduce las solicitudes HTTP/JSON en mensajes gRPC.

## Uso de la pasarela gRPC {#using-grpc-gateway}

La pasarela acepta una [correspondencia JSON][json-mapping] para las definiciones de mensajes [protocol buffer][api-ref] de etcd. Ten en cuenta que los campos `key` y `value` están definidos como arreglos de bytes y, por lo tanto, deben codificarse en base64 en el JSON. Los siguientes ejemplos usan `curl`, pero cualquier cliente HTTP/JSON debería funcionar igual.

### Notas {#notes}

El endpoint de la pasarela gRPC ha cambiado desde etcd v3.3:

- etcd v3.2 o anterior usa solo `[CLIENT-URL]/v3alpha/*`.
- etcd v3.3 usa `[CLIENT-URL]/v3beta/*` a la vez que conserva `[CLIENT-URL]/v3alpha/*`.
- etcd v3.4 usa `[CLIENT-URL]/v3/*` a la vez que conserva `[CLIENT-URL]/v3beta/*`.
  - **`[CLIENT-URL]/v3alpha/*` está obsoleto**.
- etcd v3.5 o posterior usa solo `[CLIENT-URL]/v3/*`.
  - **`[CLIENT-URL]/v3beta/*` está obsoleto**.

gRPC-gateway no admite la autenticación mediante TLS Common Name.

### Escribir y leer claves {#put-and-get-keys}

Usa los servicios `/v3/kv/range` y `/v3/kv/put` para leer y escribir claves:

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

### Observar claves {#watch-keys}

Usa el servicio `/v3/watch` para observar claves:

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### Transacciones {#transactions}

Emite una transacción con `/v3/kv/txn`:

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

### Autenticación {#authentication}

Configura la autenticación con el servicio `/v3/auth`:

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

Autentícate en etcd para obtener un token de autenticación usando `/v3/auth/authenticate`:

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

Configura el encabezado `Authorization` con el token de autenticación para recuperar una clave usando credenciales de autenticación:

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### Respuestas de error {#error-responses}

La pasarela gRPC traduce los estados gRPC en códigos de estado HTTP y un cuerpo de error
JSON. A partir de etcd v3.6, la actualización a grpc-gateway v2 cambió la gestión de
errores (consulta la [nota sobre gestión de errores][grpc-gateway-v2-errors] de la guía
de migración a v2), y el comportamiento de la pasarela ahora se alinea con
`google.rpc.Status` (code, message, details), tal como se describe en el [modelo de
errores de API de Google][google-api-errors]. Históricamente, las versiones antiguas de
grpc-gateway también incluían un campo `error` de nivel superior, pero este campo no es
compatible con etcd v3.6 ni con versiones posteriores.

Los clientes deberían tratar el código de estado HTTP como el indicador principal de éxito o
fracaso. Si una solicitud falla, los clientes deberían basarse en el campo `message` como
fuente principal de información del error y usar cualquier detalle adicional para obtener más
contexto.

## Swagger {#swagger}

Las definiciones de API de [Swagger][swagger] generadas pueden encontrarse en [rpc.swagger.json][swagger-doc].

[api-ref]: /es/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /etcd/dev-guide/apispec/swagger/rpc.swagger.json
