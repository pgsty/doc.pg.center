---
title: "مرجع API: التزامن"
weight: 3900
description: "مرجع لواجهات API الخاصة بالتزامن في etcd"
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/api_concurrency_reference_v3.md"
---

يتم توليد مرجع API هذا تلقائيًا من ملفات `.proto` المذكورة.

##### الخدمة `Lock` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#service-lock-serveretcdserverapiv3lockv3lockpbv3lockproto}

تكشف خدمة القفل مرافق القفل من جانب العميل في صورة واجهة gRPC.

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| Lock | LockRequest | LockResponse | تكتسب Lock قفلًا مشتركًا موزعًا على قفل مسمّى معين. عند النجاح، ستعيد مفتاحًا فريدًا يظل موجودًا طالما يحتفظ المُستدعي بالقفل. يمكن استخدام هذا المفتاح بالاقتران مع المعاملات (transactions) لضمان ألا تحدث تحديثات etcd إلا أثناء امتلاك القفل، وذلك بأمان. يظل القفل محتفظًا به حتى يتم استدعاء Unlock على المفتاح أو تنتهي صلاحية عقد الإيجار (lease) المرتبط بالمالك. |
| Unlock | UnlockRequest | UnlockResponse | يأخذ Unlock مفتاحًا أعادته Lock ويحرر التمسك بالقفل. عندئذٍ يُوقَظ مستدعي Lock التالي المنتظر للقفل وتُمنح له ملكية القفل. |

##### الرسالة `LockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name | name هو معرّف القفل المشترك الموزع المُراد اكتسابه. | bytes |
| lease | lease هو معرّف عقد الإيجار (lease) الذي سيُرفق بملكية القفل. إذا انتهت صلاحية عقد الإيجار أو أُلغي وهو يحمل القفل حاليًا، يُحرر القفل تلقائيًا. تُعامل الاستدعاءات إلى Lock بنفس عقد الإيجار على أنها اكتساب واحد؛ فالقفل مرتين بنفس عقد الإيجار عملية لا فعل لها (no-op). | int64 |

##### الرسالة `LockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-lockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| key | key هو مفتاح سيوجد في etcd طوال المدة التي يمتلك فيها مستدعي Lock القفل. ينبغي للمستخدمين عدم تعديل هذا المفتاح وإلا فقد يُظهر القفل سلوكًا غير معرّف. | bytes |

##### الرسالة `UnlockRequest` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockrequest-serveretcdserverapiv3lockv3lockpbv3lockproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| key | key هو مفتاح ملكية القفل الممنوح من Lock. | bytes |

##### الرسالة `UnlockResponse` (server/etcdserver/api/v3lock/v3lockpb/v3lock.proto) {#message-unlockresponse-serveretcdserverapiv3lockv3lockpbv3lockproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### الخدمة `Election` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#service-election-serveretcdserverapiv3electionv3electionpbv3electionproto}

تكشف خدمة الانتخاب مرافق الانتخاب من جانب العميل في صورة واجهة gRPC.

| الطريقة | نوع الطلب | نوع الاستجابة | الوصف |
| ------ | ------------ | ------------- | ----------- |
| Campaign | CampaignRequest | CampaignResponse | ينتظر Campaign لاكتساب القيادة في انتخاب، ويعيد LeaderKey تمثل القيادة عند النجاح. يمكن بعد ذلك استخدام LeaderKey لإصدار قيم جديدة في الانتخاب، وحماية طلبات API عبر المعاملات (transactions) ما دامت القيادة قائمة، والانسحاب من الانتخاب. |
| Proclaim | ProclaimRequest | ProclaimResponse | يحدّث Proclaim القيمة المعلنة للقائد بقيمة جديدة. |
| Leader | LeaderRequest | LeaderResponse | يعيد Leader إعلان الانتخاب الحالي، إن وُجد. |
| Observe | LeaderRequest | LeaderResponse | يبث Observe إعلانات الانتخاب بالترتيب كما يصدرها قادة الانتخاب المنتخبون. |
| Resign | ResignRequest | ResignResponse | يحرر Resign قيادة الانتخاب حتى يتمكن مرشحون آخرون من اكتساب القيادة في الانتخاب. |

##### الرسالة `CampaignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name | name هو معرّف الانتخاب الخاص بالحملة. | bytes |
| lease | lease هو معرّف عقد الإيجار (lease) المرفق بقيادة الانتخاب. إذا انتهت صلاحية عقد الإيجار أو أُلغي قبل الاستقالة من القيادة، تُنقل القيادة إلى المرشح التالي، إن وُجد. | int64 |
| value | value هي القيمة المعلنة الأولية التي تُضبط عندما يفوز المرشح بالانتخاب. | bytes |

##### الرسالة `CampaignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-campaignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| leader | leader يصف الموارد المستخدمة للاحتفاظ بقيادة الانتخاب. | LeaderKey |

##### الرسالة `LeaderKey` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderkey-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name | name هو معرّف الانتخاب المقابل لمفتاح القيادة. | bytes |
| key | key هو مفتاح مبهم (opaque) يمثل ملكية الانتخاب. إذا حُذف المفتاح، تُفقد القيادة. | bytes |
| rev | rev هو مراجعة الإنشاء الخاصة بالمفتاح. يمكن استخدامه لاختبار ملكية انتخاب أثناء المعاملات عبر التحقق من أن مراجعة إنشاء المفتاح تطابق rev. | int64 |
| lease | lease هو معرّف عقد الإيجار (lease) لقائد الانتخاب. | int64 |

##### الرسالة `LeaderRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| name | name هو معرّف الانتخاب لمعلومات القيادة. | bytes |

##### الرسالة `LeaderResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-leaderresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |
| kv | kv هو زوج المفتاح-القيمة الذي يمثل آخر تحديث للقائد. | mvccpb.KeyValue |

##### الرسالة `ProclaimRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| leader | leader هو التمسك بالقيادة في الانتخاب. | LeaderKey |
| value | value هي قيمة تحديث الغرض منها الكتابة فوق القيمة الحالية للقائد. | bytes |

##### الرسالة `ProclaimResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-proclaimresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### الرسالة `ResignRequest` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignrequest-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| leader | leader هي القيادة التي سيتم التخلي عنها بالاستقالة. | LeaderKey |

##### الرسالة `ResignResponse` (server/etcdserver/api/v3election/v3electionpb/v3election.proto) {#message-resignresponse-serveretcdserverapiv3electionv3electionpbv3electionproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| header |  | etcdserverpb.ResponseHeader |

##### الرسالة `Event` (api/mvccpb/kv.proto) {#message-event-apimvccpbkvproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| type | type هو نوع الحدث. إذا كان type هو PUT، فهذا يشير إلى أنه تم تخزين بيانات جديدة في المفتاح. وإذا كان type هو DELETE، فهذا يشير إلى أنه تم حذف المفتاح. | EventType |
| kv | يحمل kv قيمة KeyValue للحدث. يحتوي حدث PUT على زوج المفتاح-القيمة الحالي. يشير حدث PUT مع kv.Version=1 إلى إنشاء مفتاح. يحتوي حدث DELETE/EXPIRE على المفتاح المحذوف مع ضبط مراجعة التعديل الخاصة به على مراجعة الحذف. | KeyValue |
| prev_kv | يحمل prev_kv زوج المفتاح-القيمة كما كان قبل وقوع الحدث. | KeyValue |

##### الرسالة `KeyValue` (api/mvccpb/kv.proto) {#message-keyvalue-apimvccpbkvproto}

| الحقل | الوصف | النوع |
| ----- | ----------- | ---- |
| key | key هو المفتاح بصيغة بايتات. لا يُسمح بمفتاح فارغ. | bytes |
| create_revision | create_revision هو مراجعة آخر إنشاء لهذا المفتاح. | int64 |
| mod_revision | mod_revision هو مراجعة آخر تعديل لهذا المفتاح. | int64 |
| version | version هو إصدار المفتاح. يعيد الحذف ضبط الإصدار إلى 0، وأي تعديل للمفتاح يزيد إصداره. | int64 |
| value | value هي القيمة التي يحملها المفتاح، بصيغة بايتات. | bytes |
| lease | lease هو معرّف عقد الإيجار (lease) المرفق بالمفتاح. عندما تنتهي صلاحية عقد الإيجار المرفق، سيُحذف المفتاح. إذا كان lease يساوي 0، فلا يوجد عقد إيجار مرفق بالمفتاح. | int64 |
