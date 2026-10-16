---
title: دليل بناء العناقيد
weight: 4150
description: "تهيئة عنقود etcd أوليًا: الطريقة الثابتة، واكتشاف etcd، واكتشاف DNS"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/clustering.md"
---

## نظرة عامة {#overview}

يتطلب بدء عنقود etcd بطريقة ثابتة أن يعرف كل عضو عضوًا آخر في العنقود. في عدد من الحالات، قد لا تكون عناوين IP لأعضاء العنقود معروفة مسبقًا. في هذه الحالات، يمكن تهيئة عنقود etcd أوليًا بمساعدة خدمة اكتشاف.

بمجرد أن يصبح عنقود etcd قيد التشغيل، تتم إضافة الأعضاء أو إزالتهم عبر [إعادة التهيئة أثناء التشغيل][runtime-conf]. لفهم التصميم الكامن وراء إعادة التهيئة أثناء التشغيل بشكل أفضل، نقترح قراءة [وثيقة تصميم تهيئة التشغيل][runtime-reconf-design].

سيغطي هذا الدليل الآليات التالية لتهيئة عنقود etcd أوليًا:

* [التهيئة الثابتة](#static)
* [اكتشاف etcd](#etcd-discovery)
* [اكتشاف DNS](#dns-discovery)

ستُستخدم كل من آليات التهيئة الأولية لإنشاء عنقود etcd يتكون من ثلاثة أجهزة بالتفاصيل التالية:

|الاسم|العنوان|اسم المضيف|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

## التهيئة الثابتة {#static}

بما أننا نعرف أعضاء العنقود وعناوينهم وحجم العنقود قبل البدء، يمكننا استخدام تهيئة أولية دون اتصال بضبط الخيار `initial-cluster`. ستحصل كل آلة على متغيرات البيئة التالية أو سطر الأوامر التالي:

```
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380"
ETCD_INITIAL_CLUSTER_STATE=new
```

```
--initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
--initial-cluster-state new
```

لاحظ أن عناوين URL المحددة في `initial-cluster` هي _عناوين URL المعلنة للأقران_، أي أنها يجب أن تطابق قيمة `initial-advertise-peer-urls` على العقد المعنية.

إذا كنت تشغل عدة عناقيد (أو تنشئ عنقودًا واحدًا وتدمره) بالتهيئة نفسها لأغراض الاختبار، فمن المستحسن بشدة إعطاء كل عنقود `initial-cluster-token` فريدًا. بذلك يستطيع etcd توليد معرفات عناقيد ومعرفات أعضاء فريدة للعناقيد حتى لو كانت لها بخلاف ذلك التهيئة نفسها تمامًا. يمكن لهذا حماية etcd من التفاعل المتقاطع بين العناقيد، الذي قد يُفسد العناقيد.

يستمع etcd على [`listen-client-urls`][conf-listen-client] لقبول حركة بيانات العملاء. يعلن عضو etcd عناوين URL المحددة في [`advertise-client-urls`][conf-adv-client] إلى الأعضاء الآخرين والوكلاء والعملاء. يرجى التأكد من إمكانية الوصول إلى `advertise-client-urls` من العملاء المقصودين. من الأخطاء الشائعة تعيين `advertise-client-urls` على localhost أو تركه بالقيمة الافتراضية في حين ينبغي أن يتمكن العملاء البعيدون من الوصول إلى etcd.

على كل آلة، ابدأ etcd بهذه الخيارات:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state new
```

ستُتجاهل معاملات سطر الأوامر التي تبدأ بـ `--initial-cluster` في عمليات التشغيل اللاحقة لـ etcd. لا تتردد في إزالة متغيرات البيئة أو خيارات سطر الأوامر بعد عملية التهيئة الأولية. إذا احتاجت التهيئة إلى تغييرات لاحقًا (مثل إضافة أعضاء إلى العنقود أو إزالتهم منه)، راجع دليل [التهيئة أثناء التشغيل][runtime-conf].

### TLS {#tls}

يدعم etcd الاتصال المشفر عبر بروتوكول TLS. يمكن استخدام قنوات TLS للاتصال الداخلي المشفر بين الأقران داخل العنقود وكذلك لحركة بيانات العملاء المشفرة. يقدم هذا القسم أمثلة لإعداد عنقود باستخدام TLS للأقران والعملاء. يمكن العثور على معلومات إضافية تفصّل دعم etcd لـ TLS في [دليل الأمان][security-guide].

#### الشهادات الموقعة ذاتيًا {#self-signed-certificates}

يقوم العنقود الذي يستخدم شهادات موقعة ذاتيًا بتشفير حركة البيانات ومصادقة اتصالاته في آن واحد. لبدء عنقود بشهادات موقعة ذاتيًا، يجب أن يمتلك كل عضو في العنقود زوج مفاتيح فريدًا (`member.crt`، `member.key`) موقّعًا من شهادة CA مشتركة للعنقود (`ca.crt`) لكلٍّ من اتصالات الأقران واتصالات العملاء. يمكن توليد الشهادات باتباع مثال [تهيئة TLS][tls-setup] الخاص بـ etcd.

على كل آلة، سيُبدأ etcd بهذه الخيارات:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra0-client.crt --key-file=/path/to/infra0-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra0-peer.crt --peer-key-file=/path/to/infra0-peer.key
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra1-client.crt --key-file=/path/to/infra1-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra1-peer.crt --peer-key-file=/path/to/infra1-peer.key
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --client-cert-auth --trusted-ca-file=/path/to/ca-client.crt \
  --cert-file=/path/to/infra2-client.crt --key-file=/path/to/infra2-client.key \
  --peer-client-cert-auth --peer-trusted-ca-file=ca-peer.crt \
  --peer-cert-file=/path/to/infra2-peer.crt --peer-key-file=/path/to/infra2-peer.key
```

#### الشهادات التلقائية {#automatic-certificates}

إذا كان العنقود يحتاج إلى اتصال مشفر لكنه لا يتطلب اتصالات مصادَقًا عليها، يمكن تهيئة etcd لتوليد مفاتيحه تلقائيًا. عند التهيئة الأولية، ينشئ كل عضو مجموعته الخاصة من المفاتيح استنادًا إلى عناوين IP والمضيفين المعلنين له.

على كل آلة، سيُبدأ etcd بهذه الخيارات:

```
$ etcd --name infra0 --initial-advertise-peer-urls https://10.0.1.10:2380 \
  --listen-peer-urls https://10.0.1.10:2380 \
  --listen-client-urls https://10.0.1.10:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.10:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra1 --initial-advertise-peer-urls https://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls https://10.0.1.11:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.11:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```
```
$ etcd --name infra2 --initial-advertise-peer-urls https://10.0.1.12:2380 \
  --listen-peer-urls https://10.0.1.12:2380 \
  --listen-client-urls https://10.0.1.12:2379,https://127.0.0.1:2379 \
  --advertise-client-urls https://10.0.1.12:2379 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-cluster infra0=https://10.0.1.10:2380,infra1=https://10.0.1.11:2380,infra2=https://10.0.1.12:2380 \
  --initial-cluster-state new \
  --auto-tls \
  --peer-auto-tls
```

### حالات الخطأ {#error-cases}

في المثال التالي، لم نُدرج مضيفنا الجديد في قائمة العقد المعدودة. إذا كان هذا عنقودًا جديدًا، فإن العقدة _يجب_ أن تُضاف إلى قائمة أعضاء العنقود الأوليين.

```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls https://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380 \
  --initial-cluster-state new
etcd: infra1 not listed in the initial cluster config
exit 1
```

في هذا المثال، نحاول تعيين عقدة (infra0) على عنوان مختلف (127.0.0.1:2380) عن عنوانها المعدود في قائمة العنقود (10.0.1.10:2380). إذا كانت هذه العقدة ستستمع على عناوين متعددة، فإن جميع العناوين _يجب_ أن تنعكس في توجيه التهيئة "initial-cluster".

```
$ etcd --name infra0 --initial-advertise-peer-urls http://127.0.0.1:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state=new
etcd: error setting up initial cluster: infra0 has different advertised URLs in the cluster and advertised peer URLs list
exit 1
```

إذا هُيّئ قرين بمجموعة مختلفة من معاملات التهيئة وحاول الانضمام إلى هذا العنقود، فسيبلغ etcd عن عدم تطابق معرف العنقود وسيخرج.

```
$ etcd --name infra3 --initial-advertise-peer-urls http://10.0.1.13:2380 \
  --listen-peer-urls http://10.0.1.13:2380 \
  --listen-client-urls http://10.0.1.13:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.13:2379 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra3=http://10.0.1.13:2380 \
  --initial-cluster-state=new
etcd: conflicting cluster ID to the target cluster (c6ab534d07e8fcc4 != bc25ea2a74fb18b0). Exiting.
exit 1
```

## الاكتشاف {#discovery}

في عدد من الحالات، قد لا تكون عناوين IP لأقران العنقود معروفة مسبقًا. هذا شائع عند الاستعانة بمزودي الخدمات السحابية أو عندما تستخدم الشبكة DHCP. في هذه الحالات، وبدلًا من تحديد تهيئة ثابتة، استخدم عنقود etcd موجودًا لتهيئة عنقود جديد أوليًا. تسمى هذه العملية "الاكتشاف".

هناك طريقتان يمكن استخدامهما للاكتشاف:

* خدمة اكتشاف etcd
* سجلات DNS SRV

### اكتشاف etcd {#etcd-discovery}

> [!NOTE]
> توضح أمثلة خدمة الاكتشاف في هذا القسم بروتوكول v2 القديم الذي أُزيل في etcd 3.7. لعنقود v3.7 جديد، استخدم [اكتشاف v3](/ar/etcd/dev-internal/discovery_protocol/) أو طريقتي التهيئة الأولية الثابتة و DNS SRV في هذا الدليل.

لفهم تصميم بروتوكول خدمة الاكتشاف بشكل أفضل، نقترح قراءة [الوثائق][discovery-proto] الخاصة ببروتوكول خدمة الاكتشاف.

#### دورة حياة عنوان URL للاكتشاف {#lifetime-of-a-discovery-url}

يحدد عنوان URL للاكتشاف عنقود etcd فريدًا. وبدلًا من إعادة استخدام عنوان URL للاكتشاف موجود، تشارك كل نسخة من etcd عنوان URL للاكتشاف جديدًا لتهيئة العنقود الجديد أوليًا.

علاوة على ذلك، يجب استخدام عناوين URL للاكتشاف للتهيئة الأولية للعنقود فقط. لتغيير عضوية العنقود بعد أن يصبح قيد التشغيل بالفعل، راجع دليل [إعادة التهيئة أثناء التشغيل][runtime-conf].

#### خدمة اكتشاف etcd مخصصة {#custom-etcd-discovery-service}

يستخدم الاكتشاف عنقودًا موجودًا لتهيئة نفسه أوليًا. إذا كنت تستخدم عنقود etcd خاصًا، فأنشئ عنوان URL كما يلي:

```
$ curl -X PUT https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
```

بتعيين مفتاح الحجم size في عنوان URL، يُنشأ عنوان URL للاكتشاف بحجم عنقود متوقع قدره 3.

سيكون عنوان URL المستخدم في هذه الحالة هو `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` وسيستخدم أعضاء etcd الدليل `https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83` للتسجيل عند بدئهم.

**يجب تحديد قيمة مختلفة للخيار name لكل عضو. يمكن أن يكون `Hostname` أو `machine-id` خيارًا جيدًا. وإلا سيفشل الاكتشاف بسبب تكرار الاسم.**

الآن نبدأ etcd بهذه الخيارات ذات الصلة لكل عضو:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://myetcd.local/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
```

سيؤدي هذا إلى تسجيل كل عضو لدى خدمة اكتشاف etcd المخصصة وبدء العنقود بمجرد تسجيل جميع الأجهزة.

#### خدمة اكتشاف etcd العامة {#public-etcd-discovery-service}

إذا لم يتوفر عنقود قائم، استخدم خدمة الاكتشاف العامة المستضافة على `discovery.etcd.io`. لإنشاء عنوان URL اكتشاف خاص باستخدام نقطة النهاية "new"، استخدم الأمر:

```
$ curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

سيؤدي هذا إلى إنشاء العنقود بحجم أولي يبلغ 3 أعضاء. إذا لم يُحدد حجم، فسيُستخدم الافتراضي وهو 3.

```
ETCD_DISCOVERY=https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

```
--discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

**يجب تحديد قيمة مختلفة للخيار name لكل عضو وإلا سيفشل الاكتشاف بسبب تكرار الأسماء. يمكن أن يكون `Hostname` أو `machine-id` خيارًا جيدًا.**

الآن نبدأ etcd بهذه الخيارات ذات الصلة لكل عضو:

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra1 --initial-advertise-peer-urls http://10.0.1.11:2380 \
  --listen-peer-urls http://10.0.1.11:2380 \
  --listen-client-urls http://10.0.1.11:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.11:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```
```
$ etcd --name infra2 --initial-advertise-peer-urls http://10.0.1.12:2380 \
  --listen-peer-urls http://10.0.1.12:2380 \
  --listen-client-urls http://10.0.1.12:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.12:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
```

سيؤدي هذا إلى تسجيل كل عضو لدى خدمة الاكتشاف وبدء العنقود بمجرد تسجيل جميع الأعضاء.

استخدم متغير البيئة `ETCD_DISCOVERY_PROXY` لجعل etcd يستخدم وكيل HTTP للاتصال بخدمة الاكتشاف.

#### حالات الأخطاء والتحذيرات {#error-and-warning-cases}

##### أخطاء خادم الاكتشاف {#discovery-server-errors}


```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcd: error: the cluster doesn’t have a size configuration value in https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de/_config
exit 1
```

##### تحذيرات {#warnings}

هذا تحذير غير ضار يشير إلى أن عنوان URL للاكتشاف سيُتجاهل على هذه الآلة.

```
$ etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380 \
  --listen-peer-urls http://10.0.1.10:2380 \
  --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379 \
  --advertise-client-urls http://10.0.1.10:2379 \
  --discovery https://discovery.etcd.io/3e86b59982e49066c5d813af1c2e2579cbf573de
etcdserver: discovery token ignored since a cluster has already been initialized. Valid log found at /var/lib/etcd
```

### اكتشاف DNS {#dns-discovery}

يمكن استخدام [سجلات SRV][rfc-srv] في DNS كآلية للاكتشاف.
يمكن استخدام الخيار `--discovery-srv` لتعيين اسم نطاق DNS حيث يمكن العثور على سجلات SRV الخاصة بالاكتشاف.
يؤدي ضبط `--discovery-srv example.com` إلى البحث عن سجلات DNS SRV بالترتيب المدرج:

* _etcd-server-ssl._tcp.example.com
* _etcd-server._tcp.example.com

إذا وُجد `_etcd-server-ssl._tcp.example.com` فسيحاول etcd تنفيذ عملية التهيئة الأولية عبر TLS.

لمساعدة العملاء على اكتشاف عنقود etcd، يتم البحث عن سجلات DNS SRV التالية بالترتيب المدرج:

* _etcd-client._tcp.example.com
* _etcd-client-ssl._tcp.example.com

إذا وُجد `_etcd-client-ssl._tcp.example.com`، فسيحاول العملاء الاتصال بعنقود etcd عبر SSL/TLS.

إذا كان etcd يستخدم TLS، فيجب تضمين سجل SRV الخاص بالاكتشاف (مثل `example.com`) في DNS SAN لشهادة SSL مع اسم المضيف، وإلا سيفشل بناء العنقود مع رسائل في السجل مثل التالية:

```
[...] rejected connection from "10.0.1.11:53162" (error "remote error: tls: bad certificate", ServerName "example.com")
```

إذا كان etcd يستخدم TLS دون جهة إصدار شهادات مخصصة، فيجب أن يتطابق نطاق الاكتشاف (مثل example.com) مع نطاق سجل SRV (مثل infra1.example.com). هذا للتخفيف من الهجمات التي تزوّر سجلات SRV لتشير إلى نطاق مختلف؛ إذ سيكون لذلك النطاق شهادة صالحة وفق PKI لكنه يخضع لسيطرة طرف ثالث مجهول.

يضيف الخيار `-discovery-srv-name` كذلك لاحقة إلى اسم SRV الذي يُستعلم عنه أثناء الاكتشاف.
استخدم هذا الخيار للتمييز بين عدة عناقيد etcd تحت النطاق نفسه.
على سبيل المثال، إذا ضُبط `discovery-srv=example.com` و `-discovery-srv-name=foo`، فستُنفَّذ استعلامات DNS SRV التالية:

* _etcd-server-ssl-foo._tcp.example.com
* _etcd-server-foo._tcp.example.com

#### إنشاء سجلات DNS SRV {#create-dns-srv-records}

```
$ dig +noall +answer SRV _etcd-server._tcp.example.com
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra0.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra1.example.com.
_etcd-server._tcp.example.com. 300 IN  SRV  0 0 2380 infra2.example.com.
```

```
$ dig +noall +answer SRV _etcd-client._tcp.example.com
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra0.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra1.example.com.
_etcd-client._tcp.example.com. 300 IN SRV 0 0 2379 infra2.example.com.
```

```
$ dig +noall +answer infra0.example.com infra1.example.com infra2.example.com
infra0.example.com.  300  IN  A  10.0.1.10
infra1.example.com.  300  IN  A  10.0.1.11
infra2.example.com.  300  IN  A  10.0.1.12
```

#### تهيئة عنقود etcd أوليًا باستخدام DNS {#bootstrap-the-etcd-cluster-using-dns}

يمكن لأعضاء عنقود etcd الإعلان عن أسماء نطاقات أو عناوين IP، وستقوم عملية التهيئة الأولية بتحليل سجلات DNS A.
بدءًا من الإصدار 3.2 (الإصدار 3.1 يطبع تحذيرات)، سيرفض الخياران `--listen-peer-urls` و `--listen-client-urls` اسم النطاق عند الربط بواجهة الشبكة.

*يجب أن يتطابق* العنوان المحلَّل في `--initial-advertise-peer-urls` مع أحد العناوين المحلَّلة في أهداف SRV. يقرأ عضو etcd العنوان المحلَّل ليعرف ما إذا كان ينتمي إلى العنقود المعرّف في سجلات SRV.

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra0.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra0.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra1.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra1.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://infra2.example.com:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://infra2.example.com:2379 \
--listen-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380
```

يمكن للعنقود أيضًا أن تتم تهيئته أوليًا باستخدام عناوين IP بدلًا من أسماء النطاقات:

```
$ etcd --name infra0 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.10:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.10:2379 \
--listen-client-urls http://10.0.1.10:2379 \
--listen-peer-urls http://10.0.1.10:2380
```

```
$ etcd --name infra1 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.11:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.11:2379 \
--listen-client-urls http://10.0.1.11:2379 \
--listen-peer-urls http://10.0.1.11:2380
```

```
$ etcd --name infra2 \
--discovery-srv example.com \
--initial-advertise-peer-urls http://10.0.1.12:2380 \
--initial-cluster-token etcd-cluster-1 \
--initial-cluster-state new \
--advertise-client-urls http://10.0.1.12:2379 \
--listen-client-urls http://10.0.1.12:2379 \
--listen-peer-urls http://10.0.1.12:2380
```

منذ الإصدار v3.1.0 (باستثناء v3.2.9)، عندما تُهيَّأ `etcd --discovery-srv=example.com` مع TLS، فسيصادق الخادم الأقران/العملاء فقط عندما تتضمن الشهادات المقدمة النطاق الجذر `example.com` كإدخال في حقل اسم الموضوع البديل (SAN). راجع [ملاحظات حول DNS SRV][security-guide-dns-srv].

### البوابة {#gateway}

بوابة etcd هي وكيل TCP بسيط يعيد توجيه بيانات الشبكة إلى عنقود etcd. يرجى قراءة [دليل البوابة][gateway] لمزيد من المعلومات.

### الوكيل {#proxy}

دعمت إصدارات etcd الأقدم [وضع وكيل][proxy] مقتصرًا على v2 عبر `--proxy`. أُزيل هذا الوضع ولا يمكن استخدامه مع etcd 3.7. أما لواجهة v3 API فاستخدم [وكيل gRPC](/ar/etcd/op-guide/grpc_proxy/).

لعمليات النشر التاريخية لوكيل v2، راجع [وثيقة بناء العناقيد في إصدار etcd 2.3][clustering_etcd2].

[clustering_etcd2]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/clustering.md
[conf-adv-client]: /ar/etcd/op-guide/configuration/#clustering
[conf-listen-client]: /ar/etcd/op-guide/configuration/#member
[discovery-proto]: /ar/etcd/dev-internal/discovery_protocol/
[gateway]: /ar/etcd/op-guide/gateway/
[proxy]: https://github.com/etcd-io/etcd/blob/release-2.3/Documentation/proxy.md
[rfc-srv]: http://www.ietf.org/rfc/rfc2052.txt
[runtime-conf]: /ar/etcd/op-guide/runtime-configuration/
[runtime-reconf-design]: /ar/etcd/op-guide/runtime-reconf-design/
[security-guide-dns-srv]: /ar/etcd/op-guide/security/#notes-for-dns-srv
[security-guide]: /ar/etcd/op-guide/security/
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
