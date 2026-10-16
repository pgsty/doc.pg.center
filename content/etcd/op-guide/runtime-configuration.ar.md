---
title: إعادة الإعداد أثناء التشغيل
weight: 4700
description: دعم etcd لإعادة الإعداد التزايدي أثناء التشغيل
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
---

يأتي etcd بدعم إعادة الإعداد التزايدي أثناء التشغيل، مما يتيح للمستخدمين تحديث عضوية العنقود في وقت التشغيل.

لا يمكن معالجة طلبات إعادة الإعداد إلا عندما تكون أغلبية أعضاء العنقود تعمل بشكل سليم. **يوصى بشدة** بأن يكون حجم العنقود في الإنتاج أكبر من اثنين دائمًا. إن إزالة عضو من عنقود مكوّن من عضوين أمر غير آمن. فأغلبية عنقود من عضوين هي أيضًا اثنان. وفي حال حدث فشل أثناء عملية الإزالة، فقد لا يتمكن العنقود من مواصلة العمل ويحتاج إلى [إعادة التشغيل من فشل الأغلبية][majority failure].

لفهم التصميم الكامن وراء إعادة الإعداد أثناء التشغيل على نحو أفضل، يرجى قراءة [وثيقة إعادة الإعداد أثناء التشغيل][runtime-reconf].

## حالات استخدام إعادة الإعداد {#reconfiguration-use-cases}

يستعرض هذا القسم بعض الأسباب الشائعة لإعادة إعداد عنقود. تنطوي معظم هذه الأسباب ببساطة على توليفات من إضافة عضو أو إزالته، وهي موضع الشرح أدناه تحت [عمليات إعادة إعداد العنقود][cluster-reconf].

### تدوير عدة أجهزة أو ترقيتها {#cycle-or-upgrade-multiple-machines}

إذا كان يلزم نقل عدة أعضاء في العنقود بسبب صيانة مخطط لها (ترقيات العتاد، انقطاع الشبكة، إلخ)، يوصى بتعديل الأعضاء واحدًا تلو الآخر.

من الآمن إزالة القائد، غير أن هناك فترة توقف وجيزة أثناء إجراء عملية الانتخاب. إذا كان العنقود يحتوي على أكثر من 50MB من بيانات v2، يوصى [بترحيل دليل بيانات العضو][member migration].

### تغيير حجم العنقود {#change-the-cluster-size}

يمكن أن تعزز زيادة حجم العنقود [تحمّل الأعطال][fault tolerance table] وتوفر أداء قراءة أفضل. وبما أن العملاء يمكنهم القراءة من أي عضو، فإن زيادة عدد الأعضاء ترفع إجمالي إنتاجية القراءة القابلة للتسلسل.

يمكن أن يحسّن تقليل حجم العنقود أداء الكتابة للعنقود، مقابل انخفاض في المرونة. تُنسخ عمليات الكتابة إلى العنقود إلى أغلبية أعضاء العنقود قبل اعتبارها مُثبَّتة (committed). ويؤدي تقليل حجم العنقود إلى خفض الأغلبية، فتُثبَّت كل عملية كتابة بسرعة أكبر.

### استبدال جهاز فاشل {#replace-a-failed-machine}

إذا فشل جهاز بسبب عطل في العتاد، أو تلف في دليل البيانات، أو أي حالة قاتلة أخرى، فينبغي استبداله في أقرب وقت ممكن. فالأجهزة التي فشلت لكنها لم تُزَل بعد تؤثر سلبًا على النصاب وتقلّل التحمّل لفشل إضافي.

لاستبدال الجهاز، اتبع تعليمات [إزالة العضو][remove member] من العنقود، ثم [إضافة عضو جديد][add member] مكانه. إذا كان العنقود يحتوي على أكثر من 50MB، يوصى [بترحيل دليل بيانات العضو الفاشل][member migration] إذا كان لا يزال متاحًا.

### إعادة تشغيل العنقود من فشل الأغلبية {#restart-cluster-from-majority-failure}

إذا فُقدت أغلبية العنقود أو إذا غيّرت جميع العقد عناوين IP الخاصة بها، فمن الضروري اتخاذ إجراء يدوي للتعافي بأمان. تشمل الخطوات الأساسية في عملية التعافي [إنشاء عنقود جديد باستخدام البيانات القديمة][disaster recovery]، وإجبار عضو واحد على العمل بوصفه القائد، ثم أخيرًا استخدام الإعداد أثناء التشغيل [لإضافة أعضاء جدد][add member] إلى هذا العنقود الجديد واحدًا تلو الآخر.

### التعافي من فشل الأقلية {#recover-cluster-from-minority-failure}

إذا فُقد عضو بعينه، فإن ذلك يعادل استبدال جهاز فاشل. ذُكرت الخطوات في [استبدال جهاز فاشل](/ar/etcd/op-guide/runtime-configuration/#replace-a-failed-machine).

## عمليات إعادة إعداد العنقود {#cluster-reconfiguration-operations}

بوضع حالات الاستخدام هذه في الحسبان، يمكن وصف العمليات المتضمنة لكل منها.

قبل إجراء أي تغيير، يجب أن تتوفر أغلبية بسيطة (النصاب) من أعضاء etcd. وهذا في جوهره المتطلب نفسه لأي نوع من الكتابة إلى etcd.

يجب إجراء جميع التغييرات على العنقود بشكل متسلسل:

* لتحديث peerURLs لعضو واحد، أصدر عملية تحديث
* لاستبدال عضو سليم واحد، أزل العضو القديم ثم أضف عضوًا جديدًا
* للزيادة من 3 إلى 5 أعضاء، أصدر عمليتي إضافة
* للنقصان من 5 إلى 3، أصدر عمليتي إزالة

تستخدم جميع هذه الأمثلة أداة سطر الأوامر `etcdctl` التي تأتي مع etcd. لتغيير العضوية بدون `etcdctl`، استخدم [واجهة برمجة تطبيقات أعضاء gRPC الخاصة بـ v3][member-api-grpc].

### تحديث عضو {#update-a-member}

#### تحديث عناوين URL للعملاء المُعلَنة {#update-advertise-client-urls}

لتحديث عناوين URL للعملاء المُعلَنة الخاصة بعضو، ما عليك إلا إعادة تشغيل ذلك العضو مع علم عناوين URL للعملاء المحدث (`--advertise-client-urls`) أو متغير البيئة (`ETCD_ADVERTISE_CLIENT_URLS`). سينشر العضو المُعاد تشغيله عناوين URL المحدثة بنفسه. لن يؤثر عنوان URL عميل حُدِّث بشكل خاطئ على صحة عنقود etcd.

#### تحديث عناوين URL للأقران المُعلَنة {#update-advertise-peer-urls}

لتحديث عناوين URL للأقران المُعلَنة الخاصة بعضو، حدّثها أولًا بشكل صريح عبر أمر member ثم أعد تشغيل العضو. هذا الإجراء الإضافي مطلوب لأن تحديث عناوين URL للأقران يغيّر الإعداد على مستوى العنقود بأكمله ويمكن أن يؤثر على صحة عنقود etcd.

لتحديث عناوين URL للأقران المُعلَنة، اعثر أولًا على معرّف العضو المستهدف. لسرد جميع الأعضاء باستخدام `etcdctl`:

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

سيجري هذا المثال `update` على معرّف العضو a8266ecf031671f3 ويغيّر قيمة peerURLs الخاصة به إلى `http://10.0.1.10:2380`:

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### إزالة عضو {#remove-a-member}

افترض أن معرّف العضو المطلوب إزالته هو a8266ecf031671f3. استخدم الأمر `remove` لتنفيذ الإزالة:

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

سيتوقف العضو المستهدف نفسه عند هذه النقطة ويطبع الإزالة في السجل:

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

من الآمن إزالة القائد، غير أن العنقود سيكون غير نشط أثناء انتخاب قائد جديد. هذه المدة هي عادةً مدة مهلة الانتخاب مضافًا إليها مدة عملية التصويت.

### إضافة عضو جديد {#add-a-new-member}

إضافة عضو عملية من خطوتين:

 * أضف العضو الجديد إلى العنقود عبر [واجهة برمجة تطبيقات أعضاء gRPC الخاصة بـ v3][member-api-grpc] أو الأمر `etcdctl member add`.
 * ابدأ العضو الجديد بإعداد العنقود الجديد، بما في ذلك قائمة الأعضاء المحدثين (الأعضاء الموجودون + العضو الجديد).

يضيف `etcdctl` عضوًا جديدًا إلى العنقود بتحديد [الاسم][conf-name] الخاص بالعضو و[عناوين URL للأقران المُعلَنة][conf-adv-peer]:

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

أبلغ `etcdctl` العنقود بالعضو الجديد وطبع متغيرات البيئة اللازمة لبدء تشغيله بنجاح. الآن ابدأ عملية etcd الجديدة بالأعلام ذات الصلة بالعضو الجديد:

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

سيعمل العضو الجديد بوصفه جزءًا من العنقود وسيبدأ فورًا في مواكبة بقية العنقود.

عند إضافة عدة أعضاء، فإن أفضل ممارسة هي إعداد عضو واحد في كل مرة والتحقق من أنه يبدأ بشكل صحيح قبل إضافة أعضاء جدد آخرين. إذا أضفت عضوًا جديدًا إلى عنقود أحادي العقدة، فلن يتمكن العنقود من مواصلة العمل قبل بدء العضو الجديد، لأنه يحتاج إلى عضوين كأغلبية للوصول إلى الإجماع. يحدث هذا السلوك فقط بين الوقت الذي يُبلغ فيه `etcdctl member add` العنقود بالعضو الجديد والوقت الذي ينشئ فيه العضو الجديد اتصالًا ناجحًا بالعضو الموجود.

#### إضافة عضو جديد كمتعلم {#add-a-new-member-as-learner}

بدءًا من v3.4، يدعم etcd إضافة عضو جديد بوصفه متعلمًا (learner) / عضوًا غير مصوّت.
يمكن العثور على الدافع والتصميم في [وثيقة التصميم][design-learner].
ولجعل عملية إضافة عضو جديد أكثر أمانًا،
ولتقليل وقت تعطل العنقود عند إضافة العضو الجديد، يوصى بأن يُضاف العضو الجديد إلى العنقود
بوصفه متعلمًا حتى يواكب العنقود. يمكن وصف هذه العملية بأنها عملية من ثلاث خطوات:

 * أضف العضو الجديد كمتعلم عبر [واجهة برمجة تطبيقات أعضاء gRPC][member-api-grpc] أو الأمر `etcdctl member add --learner`.

 * ابدأ العضو الجديد بإعداد العنقود الجديد، بما في ذلك قائمة الأعضاء المحدثين (الأعضاء الموجودون + العضو الجديد).
     هذه الخطوة هي نفسها تمامًا كما في السابق.

 * رقِّ المتعلم المضاف حديثًا إلى عضو مصوّت عبر [واجهة برمجة تطبيقات أعضاء gRPC][member-api-grpc] أو الأمر `etcdctl member promote`.
     يتحقق خادم etcd من طلب الترقية لضمان أمانه التشغيلي.
     لا يمكن ترقية متعلم إلى عضو مصوّت إلا بعد لحاق سجل raft الخاص به بسجل القائد.
     إذا لم يكن المتعلم قد لحق بسجل raft الخاص بالقائد، فسيفشل طلب ترقية العضو
     (انظر قسم [حالات الخطأ عند ترقية عضو][error cases when promoting a member] لمزيد من التفاصيل).
     في هذه الحالة، ينبغي على المستخدم الانتظار وإعادة المحاولة لاحقًا.

في v3.4، يحد خادم etcd من عدد المتعلمين الذين يمكن أن يضمهم العنقود إلى واحد. والاعتبار الرئيسي هو الحد من
العبء الإضافي على القائد بسبب نشر البيانات من القائد إلى المتعلم.

استخدم `etcdctl member add` مع العلم `--learner` لإضافة عضو جديد إلى العنقود بوصفه متعلمًا.

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

بعد بدء عملية etcd الجديدة للعضو المتعلم المضاف حديثًا، استخدم `etcdctl member promote` لترقية المتعلم إلى عضو مصوّت.
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### حالات الخطأ عند إضافة أعضاء {#error-cases-when-adding-members}

في الحالة التالية، لم يُدرَج مضيف جديد في قائمة العقد المعدودة. إذا كان هذا عنقودًا جديدًا، فيجب إضافة العقدة إلى قائمة أعضاء العنقود الأولي.

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

في هذا المثال الفاشل، يبدأ العضو بعنوان (10.0.1.14:2380) يختلف عن عنوان القرين المسجل (10.0.1.13:2380):

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

إذا بدأ etcd باستخدام دليل بيانات عضو أُزيل، فسيخرج etcd تلقائيًا إذا اتصل بأي عضو نشط في العنقود:

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### حالات الخطأ عند إضافة عضو متعلم {#error-cases-when-adding-a-learner-member}

لا يمكن إضافة متعلم إلى العنقود إذا كان العنقود يضم متعلمًا واحدًا بالفعل (v3.4).
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### حالات الخطأ عند ترقية عضو متعلم {#error-cases-when-promoting-a-learner-member}

لا يمكن ترقية المتعلم إلى عضو مصوّت إلا إذا كان متزامنًا مع القائد.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

سوف تفشل ترقية عضو ليس متعلمًا.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

سوف تفشل ترقية عضو غير موجود في العنقود.
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### وضع فحص إعادة الإعداد الصارم (`-strict-reconfig-check`) {#strict-reconfiguration-check-mode--strict-reconfig-check}

كما وُصف أعلاه، فإن أفضل ممارسة لإضافة أعضاء جدد هي إعداد عضو واحد في كل مرة والتحقق من أنه يبدأ بشكل صحيح قبل إضافة أعضاء جدد آخرين. هذا النهج التدريجي مهم جدًا، لأنه إذا لم يُعدّ الأعضاء المضافون حديثًا بشكل صحيح (مثلًا إذا كانت عناوين URL للأقران غير صحيحة)، فقد يفقد العنقود النصاب. يحدث فقدان النصاب لأن العضو المضاف حديثًا يُحتسب ضمن النصاب حتى لو كان غير قابل للوصول من بقية الأعضاء الموجودين. أيضًا قد يحدث فقدان النصاب إذا وُجدت مشكلة اتصال أو مشكلات تشغيلية.

لتجنب هذه المشكلة، يوفر etcd الخيار `-strict-reconfig-check`. إذا مُرِّر هذا الخيار إلى etcd، فسيرفض etcd طلبات إعادة الإعداد إذا كان عدد الأعضاء الذين بدأ تشغيلهم سيكون أقل من نصاب العنقود المُعاد إعداده.

وهو مُمكَّن افتراضيًا.

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /ar/etcd/op-guide/configuration#clustering
[conf-name]: /ar/etcd/op-guide/configuration#member
[design-learner]: /ar/etcd/learning/design-learner
[disaster recovery]: /ar/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /ar/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /ar/etcd/op-guide/runtime-reconf-design/
