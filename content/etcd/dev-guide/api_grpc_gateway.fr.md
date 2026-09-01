---
title: Pourquoi utiliser une passerelle gRPC
weight: 3375
description: "Pourquoi envisager l'utilisation de la passerelle gRPC"
categories: [Concept]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
---

etcd v3 utilise [gRPC][grpc] comme protocole de messagerie. Le projet etcd inclut un client [Go][go-client] basé sur gRPC ainsi qu'une utilitaire en ligne de commande, [etcdctl][etcdctl], pour communiquer avec un cluster etcd via gRPC. Pour les langages ne disposant pas de prise en charge gRPC, etcd fournit une passerelle [gRPC][grpc-gateway] en JSON. Cette passerelle fournit un proxy RESTful qui traduit les requêtes HTTP/JSON en messages gRPC.

## Utilisation de la passerelle gRPC {#using-grpc-gateway}

La passerelle accepte une correspondance [JSON][json-mapping] pour les définitions de messages du protocole buffer [de etcd][api-ref]. Notez que les champs `key` et `value` sont définis comme des tableaux d'octets et doivent donc être encodés en base64 dans le JSON. Les exemples suivants utilisent `curl`, mais tout client HTTP/JSON devrait fonctionner de la même manière.

### Notes {#notes}

Point de terminaison de passerelle gRPC a changé depuis etcd v3.3 :

- etcd v3.2 ou antérieure utilise uniquement `[CLIENT-URL]/v3alpha/*`.
- etcd v3.3 utilise `[CLIENT-URL]/v3beta/*` tout en conservant `[CLIENT-URL]/v3alpha/*`.
- etcd v3.4 utilise `[CLIENT-URL]/v3/*` tout en conservant `[CLIENT-URL]/v3beta/*`.
  - **`[CLIENT-URL]/v3alpha/*` est obsolète**.
- etcd v3.5 ou ultérieure utilise uniquement `[CLIENT-URL]/v3/*`.
  - **`[CLIENT-URL]/v3beta/*` est obsolète**.

Le passerelle gRPC ne prend pas en charge l'authentification par le nom commun TLS.

### Mettre et obtenir des clés {#put-and-get-keys}

Utilisez les services `/v3/kv/range` et `/v3/kv/put` pour lire et écrire des clés :

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

### Surveillance des clés {#watch-keys}

Utilisez le service `/v3/watch` pour surveiller les clés :

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### Transactions {#transactions}

Émettre une transaction avec `/v3/kv/txn` :

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

### Authentification {#authentication}

Mettez en place une authentification avec le service `/v3/auth` :

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

Authentifiez-vous auprès d’etcd pour obtenir un jeton d’authentification en utilisant `/v3/auth/authenticate` :

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

Définissez l’en-tête `Authorization` sur le jeton d’authentification pour récupérer une clé à l’aide des identifiants d’authentification :

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### Réponses d'erreur {#error-responses}

La passerelle gRPC traduit les états gRPC en codes d’état HTTP et un corps d’erreur au format JSON. À compter d’etcd v3.6, la mise à jour vers grpc-gateway v2 a modifié la gestion des erreurs (voir la note [gestion des erreurs][grpc-gateway-v2-errors] dans le guide de migration v2), et le comportement de la passerelle est désormais conforme à `google.rpc.Status` (code, message, détails) tel que décrit dans [modèle d’erreur d’API de Google][google-api-errors]. Historiquement, les versions antérieures de grpc-gateway incluaient également un champ de niveau supérieur `error`, mais ce champ n’est plus pris en charge à partir d’etcd v3.6 et des versions ultérieures.

Les clients doivent considérer le code d’état HTTP comme l’indicateur principal de succès ou d’échec. Si une requête échoue, les clients doivent s’appuyer sur le champ `message` comme source principale d’information d’erreur et utiliser tout détail supplémentaire pour obtenir un contexte plus précis.

## Swagger {#swagger}

Les définitions d'API [Swagger][swagger] générées peuvent être trouvées dans [rpc.swagger.json][swagger-doc].

[api-ref]: /fr/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /etcd/dev-guide/apispec/swagger/rpc.swagger.json
