---
title: لماذا استخدام بوابة gRPC
weight: 3375
description: لماذا ينبغي لك التفكير في استخدام بوابة gRPC
categories: [مفهوم]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_grpc_gateway.md"
---

يستخدم etcd v3 بروتوكول [gRPC][grpc] لتبادل الرسائل. يتضمن مشروع etcd عميل [Go][go-client] مبنيًا على gRPC وأداة سطر أوامر، [etcdctl][etcdctl]، للتواصل مع عنقود etcd عبر gRPC. أما بالنسبة للغات التي لا تدعم gRPC، فيوفر etcd [بوابة gRPC][grpc-gateway] تعمل بصيغة JSON. تعمل هذه البوابة كوكيل RESTful يترجم طلبات HTTP/JSON إلى رسائل gRPC.

## استخدام بوابة gRPC {#using-grpc-gateway}

تقبل البوابة [تعيين JSON][json-mapping] لتعريفات رسائل [protocol buffers][api-ref] الخاصة بـ etcd. لاحظ أن الحقلين `key` و`value` معرّفان كمصفوفات بايتات، ولذلك يجب ترميزهما بـ base64 في JSON. تستخدم الأمثلة التالية `curl`، لكن ينبغي أن يعمل أي عميل HTTP/JSON بالطريقة نفسها.

### ملاحظات {#notes}

تغيّرت نقطة نهاية بوابة gRPC منذ etcd v3.3:

- يستخدم etcd v3.2 أو الإصدارات الأقدم `[CLIENT-URL]/v3alpha/*` فقط.
- يستخدم etcd v3.3 المسار `[CLIENT-URL]/v3beta/*` مع الإبقاء على `[CLIENT-URL]/v3alpha/*`.
- يستخدم etcd v3.4 المسار `[CLIENT-URL]/v3/*` مع الإبقاء على `[CLIENT-URL]/v3beta/*`.
  - **`[CLIENT-URL]/v3alpha/*` مهمل**.
- يستخدم etcd v3.5 أو الإصدارات الأحدث `[CLIENT-URL]/v3/*` فقط.
  - **`[CLIENT-URL]/v3beta/*` مهمل**.

لا تدعم بوابة gRPC المصادقة باستخدام TLS Common Name.

### وضع المفاتيح وجلبها {#put-and-get-keys}

استخدم الخدمتين `/v3/kv/range` و`/v3/kv/put` لقراءة المفاتيح وكتابتها:

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

### مراقبة المفاتيح {#watch-keys}

استخدم الخدمة `/v3/watch` لمراقبة المفاتيح:

```bash
curl -N http://localhost:2379/v3/watch \
  -X POST -d '{"create_request": {"key":"Zm9v"} }' &
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"1","raft_term":"2"},"created":true}}

curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}' >/dev/null 2>&1
# {"result":{"header":{"cluster_id":"12585971608760269493","member_id":"13847567121247652255","revision":"2","raft_term":"2"},"events":[{"kv":{"key":"Zm9v","create_revision":"2","mod_revision":"2","version":"1","value":"YmFy"}}]}}
```

### المعاملات {#transactions}

أصدر معاملة باستخدام `/v3/kv/txn`:

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

### المصادقة {#authentication}

أعدّ المصادقة باستخدام الخدمة `/v3/auth`:

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

استوثق لدى etcd للحصول على رمز مصادقة باستخدام `/v3/auth/authenticate`:

```bash
# get the auth token for the root user
curl -L http://localhost:2379/v3/auth/authenticate \
  -X POST -d '{"name": "root", "password": "pass"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"1","raft_term":"2"},"token":"sssvIpwfnLAcWAQH.9"}
```

اضبط ترويسة `Authorization` على رمز المصادقة لجلب مفتاح باستخدام بيانات اعتماد المصادقة:

```bash
curl -L http://localhost:2379/v3/kv/put \
  -H 'Authorization: sssvIpwfnLAcWAQH.9' \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
# {"header":{"cluster_id":"14841639068965178418","member_id":"10276657743932975437","revision":"2","raft_term":"2"}}
```

### استجابات الأخطاء {#error-responses}

تترجم بوابة gRPC حالة gRPC إلى رموز حالة HTTP ونص خطأ بصيغة JSON. بدءًا من etcd v3.6، غيّرت الترقية إلى grpc-gateway v2 طريقة التعامل مع الأخطاء (انظر [ملاحظة التعامل مع الأخطاء][grpc-gateway-v2-errors] في دليل الترحيل إلى v2)، وأصبح سلوك البوابة الآن متوافقًا مع `google.rpc.Status` (code, message, details) كما هو موصوف في [نموذج أخطاء API من Google][google-api-errors]. تاريخيًا، كانت إصدارات grpc-gateway الأقدم تتضمن أيضًا حقل `error` في المستوى الأعلى، لكن هذا الحقل غير مدعوم في etcd v3.6 والإصدارات الأحدث.

ينبغي للعملاء التعامل مع رمز حالة HTTP باعتباره المؤشر الأساسي للنجاح أو الفشل. إذا فشل الطلب، ينبغي أن يعتمد العملاء على الحقل `message` بوصفه المصدر الأساسي لمعلومات الخطأ، وأن يستخدموا أي تفاصيل إضافية لمزيد من السياق.

## Swagger {#swagger}

يمكن الاطلاع على تعريفات API المولّدة بصيغة [Swagger][swagger] في [rpc.swagger.json][swagger-doc].

[api-ref]: /ar/etcd/dev-guide/api_reference_v3/
[etcdctl]: https://github.com/etcd-io/etcd/tree/main/etcdctl
[go-client]: https://github.com/etcd-io/etcd/tree/main/client/v3
[grpc]: https://www.grpc.io/
[grpc-gateway]: https://github.com/grpc-ecosystem/grpc-gateway
[grpc-gateway-v2-errors]: https://github.com/grpc-ecosystem/grpc-gateway/blob/main/docs/docs/development/grpc-gateway_v2_migration_guide.md#error-handling-configuration-has-been-overhauled
[json-mapping]: https://developers.google.com/protocol-buffers/docs/proto3#json
[google-api-errors]: https://cloud.google.com/apis/design/errors
[swagger]: http://swagger.io/
[swagger-doc]: /etcd/dev-guide/apispec/swagger/rpc.swagger.json
