---
title: التفاعل مع etcd
weight: 3250
description: "etcdctl: أداة سطر أوامر للتفاعل مع خادم etcd"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/interacting_v3.md"
---

يتفاعل المستخدمون في الغالب مع etcd عن طريق وضع قيمة مفتاح أو جلبها. يصف هذا القسم كيفية القيام بذلك باستخدام etcdctl، أداة سطر أوامر للتفاعل مع خادم etcd. تنطبق المفاهيم الموصوفة هنا على واجهات gRPC APIs أو واجهات برمجة تطبيقات مكتبات العملاء.

يستخدم etcdctl v3.7 واجهة v3 API. لقد أزيلت واجهة v2 API والاختيار بين إصدارات `ETCDCTL_API`.

> [!NOTE]
> تحتفظ الأمثلة أدناه بمخرجات أوامر تاريخية، لذا قد تختلف أرقام الإصدارات المعروضة عن تثبيتك. احتفظت إصدارات etcd الأقدم بمفاتيح v2 وv3 في مخازن منفصلة؛ رحّل أي بيانات v2 قديمة قبل الترقية إلى v3.7.


## معرفة الإصدارات {#find-versions}

يمكن أن يكون إصدار etcdctl وإصدار API الخاصة بالخادم مفيدَين في العثور على الأوامر المناسبة لاستخدامها في تنفيذ عمليات مختلفة على etcd.

إليك الأمر للعثور على الإصدارات:

```bash
$ etcdctl version
etcdctl version: 3.1.0-alpha.0+git
API version: 3.1
```

## كتابة مفتاح {#write-a-key}

تخزن التطبيقات المفاتيح في عنقود etcd عن طريق الكتابة إلى المفاتيح. يُنسخ كل مفتاح مخزن إلى جميع أعضاء عنقود etcd عبر بروتوكول Raft لتحقيق الاتساق والموثوقية.

إليك الأمر لتعيين قيمة المفتاح `foo` إلى `bar`:

```bash
$ etcdctl put foo bar
OK
```

يمكن أيضًا تعيين مفتاح لفترة زمنية محددة بإرفاق عقد إيجار (lease) به.

إليك الأمر لتعيين قيمة المفتاح `foo1` إلى `bar1` لمدة 10s.

```bash
$ etcdctl put foo1 bar1 --lease=1234abcd
OK
```

> [!NOTE]
> يشير معرّف عقد الإيجار `1234abcd` في الأمر أعلاه إلى المعرّف المُرجَع عند إنشاء عقد إيجار مدته 10s. يمكن بعد ذلك إرفاق هذا المعرّف بالمفتاح.

## قراءة المفاتيح {#read-keys}

يمكن للتطبيقات قراءة قيم المفاتيح من عنقود etcd. قد تقرأ الاستعلامات مفتاحًا واحدًا أو نطاقًا من المفاتيح.

افترض أن عنقود etcd خزّن المفاتيح التالية:

```bash
foo = bar
foo1 = bar1
foo2 = bar2
foo3 = bar3
```

إليك الأمر لقراءة قيمة المفتاح `foo`:

```bash
$ etcdctl get foo
foo
bar
```

إليك الأمر لقراءة قيمة المفتاح `foo` بصيغة سداسية عشرية (hex):

```bash
$ etcdctl get foo --hex
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

إليك الأمر لقراءة قيمة المفتاح `foo` فقط:

```bash
$ etcdctl get foo --print-value-only
bar
```

إليك الأمر لاستعراض المفاتيح من `foo` إلى `foo3`:

```bash
$ etcdctl get foo foo3
foo
bar
foo1
bar1
foo2
bar2
```

> [!NOTE]
> `foo3` مستبعد لأن النطاق يقع على الفترة نصف المفتوحة `[foo, foo3)`، مع استبعاد `foo3`.

إليك الأمر لاستعراض جميع المفاتيح ذات البادئة `foo`:

```bash
$ etcdctl get --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

إليك الأمر لاستعراض جميع المفاتيح ذات البادئة `foo`، مع تحديد عدد النتائج بـ2:

```bash
$ etcdctl get --prefix --limit=2 foo
foo
bar
foo1
bar1
```

إليك الأمر لاستعراض جميع المفاتيح ذات البادئة `foo` باستخدام استدعاء الإجراء البعيد (RPC) [`RangeStream`](/ar/etcd/learning/api/#rangestream). النتيجة مطابقة لاستدعاء `Range` الأحادي (unary):

```bash
$ etcdctl get --stream --prefix foo
foo
bar
foo1
bar1
foo2
bar2
foo3
bar3
```

لا يدعم `--stream` كلاً من `--order` و`--sort-by` ولا مرشحات المراجعات.

## قراءة الإصدارات السابقة من المفاتيح {#read-past-version-of-keys}

قد ترغب التطبيقات في قراءة الإصدارات المتجاوزة لمفتاح. مثلًا، قد يرغب تطبيق في التراجع إلى إعداد قديم بالوصول إلى إصدار سابق من مفتاح. أو قد يريد تطبيق الحصول على عرض متسق عبر مفاتيح متعددة من خلال طلبات متعددة بالوصول إلى سجل المفاتيح.
وبما أن كل تعديل على مخزن مفاتيح/قيم عنقود etcd يزيد المراجعة العامة لعنقود etcd، يمكن للتطبيق قراءة المفاتيح المتجاوزة بتقديم مراجعة etcd أقدم.

افترض أن عنقود etcd لديه بالفعل المفاتيح التالية:

```bash
foo = bar         # revision = 2
foo1 = bar1       # revision = 3
foo = bar_new     # revision = 4
foo1 = bar1_new   # revision = 5
```

إليك مثال للوصول إلى الإصدارات السابقة من المفاتيح:

```bash
$ etcdctl get --prefix foo # access the most recent versions of keys
foo
bar_new
foo1
bar1_new

$ etcdctl get --prefix --rev=4 foo # access the versions of keys at revision 4
foo
bar_new
foo1
bar1

$ etcdctl get --prefix --rev=3 foo # access the versions of keys at revision 3
foo
bar
foo1
bar1

$ etcdctl get --prefix --rev=2 foo # access the versions of keys at revision 2
foo
bar

$ etcdctl get --prefix --rev=1 foo # access the versions of keys at revision 1
```

## قراءة المفاتيح التي تزيد قيمتها البايتية عن قيمة المفتاح المحدد أو تساويها {#read-keys-which-are-greater-than-or-equal-to-the-byte-value-of-the-specified-key}

قد ترغب التطبيقات في قراءة المفاتيح التي تزيد قيمتها البايتية عن قيمة المفتاح المحدد أو تساويها.

افترض أن عنقود etcd لديه بالفعل المفاتيح التالية:

```bash
a = 123
b = 456
z = 789
```

إليك الأمر لقراءة المفاتيح التي تزيد قيمتها البايتية عن قيمة المفتاح `b` أو تساويها:

```bash
$ etcdctl get --from-key b
b
456
z
789
```

## حذف المفاتيح {#delete-keys}

يمكن للتطبيقات حذف مفتاح أو نطاق من المفاتيح من عنقود etcd.

افترض أن عنقود etcd لديه بالفعل المفاتيح التالية:

```bash
foo = bar
foo1 = bar1
foo3 = bar3
zoo = val
zoo1 = val1
zoo2 = val2
a = 123
b = 456
z = 789
```

إليك الأمر لحذف المفتاح `foo`:

```bash
$ etcdctl del foo
1 # one key is deleted
```

إليك الأمر لحذف المفاتيح في النطاق من `foo` إلى `foo9`:

```bash
$ etcdctl del foo foo9
2 # two keys are deleted
```

إليك الأمر لحذف المفتاح `zoo` مع إرجاع زوج المفتاح/القيمة المحذوف:

```bash
$ etcdctl del --prev-kv zoo
1   # one key is deleted
zoo # deleted key
val # the value of the deleted key
```

إليك الأمر لحذف المفاتيح ذات البادئة `zoo`:

```bash
$ etcdctl del --prefix zoo
2 # two keys are deleted
```

إليك الأمر لحذف المفاتيح التي تزيد قيمتها البايتية عن قيمة المفتاح `b` أو تساويها:

```bash
$ etcdctl del --from-key b
2 # two keys are deleted
```

## مراقبة تغييرات المفاتيح {#watch-key-changes}

يمكن للتطبيقات المراقبة على مفتاح أو نطاق من المفاتيح لرصد أي تحديثات.

إليك الأمر للمراقبة على المفتاح `foo`:

```bash
$ etcdctl watch foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
```

إليك الأمر للمراقبة على المفتاح `foo` بصيغة سداسية عشرية:

```bash
$ etcdctl watch foo --hex
# in another terminal: etcdctl put foo bar
PUT
\x66\x6f\x6f          # Key
\x62\x61\x72          # Value
```

إليك الأمر للمراقبة على نطاق مفاتيح من `foo` إلى `foo9`:

```bash
$ etcdctl watch foo foo9
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put foo1 bar1
PUT
foo1
bar1
```

إليك الأمر للمراقبة على المفاتيح ذات البادئة `foo`:

```bash
$ etcdctl watch --prefix foo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put fooz1 barz1
PUT
fooz1
barz1
```

إليك الأمر للمراقبة على المفاتيح المتعددة `foo` و`zoo`:

```bash
$ etcdctl watch -i
$ watch foo
$ watch zoo
# in another terminal: etcdctl put foo bar
PUT
foo
bar
# in another terminal: etcdctl put zoo val
PUT
zoo
val
```

## مراقبة التغييرات التاريخية للمفاتيح {#watch-historical-changes-of-keys}

قد ترغب التطبيقات في مراقبة التغييرات التاريخية للمفاتيح في etcd. مثلًا، قد يريد تطبيق استلام جميع التعديلات على مفتاح؛ إذا بقي التطبيق متصلًا بـetcd، فإن `watch` كافٍ. ومع ذلك، إذا فشل التطبيق أو etcd، فقد يحدث تغيير أثناء الفشل، ولن يستلم التطبيق التحديث في الوقت الفعلي. لضمان تسليم التحديث، يجب أن يكون التطبيق قادرًا على مراقبة التغييرات التاريخية للمفاتيح. للقيام بذلك، يمكن للتطبيق تحديد مراجعة تاريخية عند المراقبة، تمامًا مثل قراءة الإصدارات السابقة من المفاتيح.

افترض أننا أنجزنا تسلسل العمليات التالي:

```bash
$ etcdctl put foo bar         # revision = 2
OK
$ etcdctl put foo1 bar1       # revision = 3
OK
$ etcdctl put foo bar_new     # revision = 4
OK
$ etcdctl put foo1 bar1_new   # revision = 5
OK
```

إليك مثال لمراقبة التغييرات التاريخية:

```bash
# watch for changes on key `foo` since revision 2
$ etcdctl watch --rev=2 foo
PUT
foo
bar
PUT
foo
bar_new
```

```bash
# watch for changes on key `foo` since revision 3
$ etcdctl watch --rev=3 foo
PUT
foo
bar_new
```

إليك مثالًا للمراقبة من آخر تغيير تاريخي فقط:

```bash
# watch for changes on key `foo` and return last revision value along with modified value
$ etcdctl watch --prev-kv foo
# in another terminal: etcdctl put foo bar_latest
PUT
foo         # key
bar_new     # last value of foo key before modification
foo         # key
bar_latest  # value of foo key after modification
```

## تقدم المراقبة {#watch-progress}

قد ترغب التطبيقات في التحقق من تقدم المراقبة لتحديد مدى حداثة تدفق المراقبة. مثلًا، إذا استُخدمت مراقبة لتحديث ذاكرة تخزين مؤقت، فقد يكون من المفيد معرفة ما إذا كانت ذاكرة التخزين المؤقت قديمة مقارنة بالمراجعة الواردة من قراءة نصاب (quorum).

يمكن إصدار طلبات التقدم باستخدام الأمر "progress" في جلسة مراقبة تفاعلية للطلب من خادم etcd إرسال تحديث إشعار تقدم في تدفق المراقبة:

```bash
$ etcdctl watch -i
$ watch a
$ progress
progress notify: 1
# in another terminal: etcdctl put x 0
# in another terminal: etcdctl put y 1
$ progress
progress notify: 3
```

> [!NOTE]
> رقم المراجعة في استجابة إشعار التقدم هو المراجعة الواردة من عقدة خادم etcd المحلية المتصل بها تدفق المراقبة. إذا كانت هذه العقدة معزولة (partitioned) وغير جزء من النصاب، فقد تكون مراجعة إشعار التقدم هذه أقل من المراجعة المُرجَعة من قراءة نصاب مقابل عقدة خادم etcd غير معزولة.

## المراجعات المضغوطة {#compacted-revisions}

كما ذكرنا، يحتفظ etcd بالمراجعات لكي تستطيع التطبيقات قراءة الإصدارات السابقة من المفاتيح. ومع ذلك، لتجنب تراكم كمية غير محدودة من السجل، من المهم ضغط المراجعات السابقة. بعد الضغط، يزيل etcd المراجعات التاريخية، محررًا الموارد لاستخدام مستقبلي. ستكون جميع البيانات المتجاوزة ذات المراجعات السابقة للمراجعة المضغوطة غير متاحة.

إليك الأمر لضغط المراجعات:

```bash
$ etcdctl compact 5
compacted revision 5

# any revisions before the compacted one are not accessible
$ etcdctl get --rev=4 foo
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

> [!NOTE]
> يمكن العثور على المراجعة الحالية لخادم etcd باستخدام الأمر get على أي مفتاح (موجود أو غير موجود) بصيغة JSON. المثال أدناه لمفتاح mykey الذي لا يوجد في خادم etcd:

```bash
$ etcdctl get mykey -w=json
{"header":{"cluster_id":14841639068965178418,"member_id":10276657743932975437,"revision":15,"raft_term":4}}
```

## منح عقود الإيجار {#grant-leases}

يمكن للتطبيقات منح عقود إيجار (lease) للمفاتيح من عنقود etcd. عندما يُرفق مفتاح بعقد إيجار، ترتبط مدة حياته بمدة حياة عقد الإيجار التي تحكمها بدورها مدة البقاء (TTL). لكل عقد إيجار قيمة دنيا لمدة البقاء (TTL) يحددها التطبيق عند المنح. قيمة TTL الفعلية لعقد الإيجار هي على الأقل TTL الدنيا ويختارها عنقود etcd. بمجرد انقضاء TTL لعقد إيجار، تنتهي صلاحيته وتُحذف جميع المفاتيح المرفقة به.

إليك الأمر لمنح عقد إيجار:

```bash
# grant a lease with 60 second TTL
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)

# attach key foo to lease 32695410dcc0ca06
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

## إبطال عقود الإيجار {#revoke-leases}

تبطل التطبيقات عقود الإيجار بمعرّف عقد الإيجار. يؤدي إبطال عقد إيجار إلى حذف جميع المفاتيح المرفقة به.

افترض أننا أنجزنا تسلسل العمليات التالي:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
$ etcdctl put --lease=32695410dcc0ca06 foo bar
OK
```

إليك الأمر لإبطال عقد الإيجار نفسه:

```bash
$ etcdctl lease revoke 32695410dcc0ca06
lease 32695410dcc0ca06 revoked

$ etcdctl get foo
# empty response since foo is deleted due to lease revocation
```

## إبقاء عقود الإيجار نشطة {#keep-leases-alive}

يمكن للتطبيقات إبقاء عقد إيجار نشطًا بتجديد TTL الخاص به حتى لا تنتهي صلاحيته.

افترض أننا أنجزنا تسلسل العمليات التالي:

```bash
$ etcdctl lease grant 60
lease 32695410dcc0ca06 granted with TTL(60s)
```

إليك الأمر لإبقاء عقد الإيجار نفسه نشطًا:

```bash
$ etcdctl lease keep-alive 32695410dcc0ca06
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
lease 32695410dcc0ca06 keepalived with TTL(60)
...
```

## الحصول على معلومات عقد الإيجار {#get-lease-information}

قد ترغب التطبيقات في معرفة معلومات عقد الإيجار، بحيث يمكن تجديد عقد الإيجار أو للتحقق مما إذا كان عقد الإيجار لا يزال موجودًا أم انتهت صلاحيته. وقد ترغب التطبيقات أيضًا في معرفة المفاتيح المرفقة بعقد إيجار معين.

افترض أننا أنجزنا تسلسل العمليات التالي:

```bash
# grant a lease with 500 second TTL
$ etcdctl lease grant 500
lease 694d5765fc71500b granted with TTL(500s)

# attach key zoo1 to lease 694d5765fc71500b
$ etcdctl put zoo1 val1 --lease=694d5765fc71500b
OK

# attach key zoo2 to lease 694d5765fc71500b
$ etcdctl put zoo2 val2 --lease=694d5765fc71500b
OK
```

إليك الأمر للحصول على معلومات عن عقد الإيجار:

```bash
$ etcdctl lease timetolive 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(258s)
```

إليك الأمر للحصول على معلومات عن عقد الإيجار مع المفاتيح المرفقة به:

```bash
$ etcdctl lease timetolive --keys 694d5765fc71500b
lease 694d5765fc71500b granted with TTL(500s), remaining(132s), attached keys([zoo2 zoo1])

# if the lease has expired or does not exist it will give the below response:
Error:  etcdserver: requested lease not found
```
