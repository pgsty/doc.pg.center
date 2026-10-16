---
title: نموذج أمان النقل
weight: 4125
description: تأمين البيانات أثناء النقل
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/security.md"
---

يدعم etcd خاصية TLS التلقائية وكذلك المصادقة عبر شهادات العملاء لاتصالات العميل إلى الخادم وكذلك لاتصالات الأقران (من خادم إلى خادم / العنقود). **لاحظ أن etcd لا يُمكّن [المصادقة القائمة على RBAC][auth] ولا ميزة المصادقة في طبقة النقل افتراضيًا لتقليل العوائق أمام المستخدمين الذين يبدؤون العمل مع قاعدة البيانات. علاوة على ذلك، فإن تغيير هذا الإعداد الافتراضي سيكون تغييرًا كاسرًا (breaking change) لمشروع تأسس منذ عام 2013. عنقود etcd الذي لا تُمكَّن فيه ميزات الأمان قد يعرّض بياناته لأي عميل.**

للبدء والتشغيل، جهّز أولًا شهادة CA وزوجًا موقّعًا من المفاتيح لأحد الأعضاء. يوصى بإنشاء زوج مفاتيح جديد وتوقيعه لكل عضو في العنقود.

للتيسير، توفر أداة [cfssl] واجهة سهلة لإنشاء الشهادات، ونوفر مثالًا يستخدم هذه الأداة [هنا][tls-setup]. وبدلًا من ذلك، جرّب هذا [الدليل لإنشاء أزواج مفاتيح موقعة ذاتيًا][tls-guide].

قد لا تكون قائمة الأعلام المقدمة أدناه محدثة بسبب تغييرات التطوير المستمرة. للحصول على أحدث الأعلام المتاحة، شغّل `etcd --help` أو راجع [مساعدة etcd][etcd help].

## الإعداد الأساسي {#basic-setup}

يتقبل etcd عدة خيارات إعداد متعلقة بالشهادات، إما عبر أعلام سطر الأوامر وإما عبر متغيرات البيئة:

**اتصالات العميل إلى الخادم:**

`--cert-file=<path>`: الشهادة المستخدمة لاتصالات SSL/TLS **إلى** etcd. عند ضبط هذا الخيار، يمكن لـ advertise-client-urls استخدام مخطط HTTPS.

`--key-file=<path>`: مفتاح الشهادة. يجب أن يكون غير مشفر.

`--client-cert-auth`: عند ضبط هذا، سيتحقق etcd من جميع طلبات HTTPS الواردة بحثًا عن شهادة عميل موقعة من مرجع الشهادات الموثوق، وستفشل الطلبات التي لا تقدم شهادة عميل صالحة. إذا كانت [المصادقة][auth] مُمكّنة، فإن الشهادة توفر بيانات الاعتماد لاسم المستخدم المعطى في حقل Common Name.

`--trusted-ca-file=<path>`: مرجع الشهادات الموثوق.

`--auto-tls`: استخدم شهادات موقعة ذاتيًا مولدة تلقائيًا لاتصالات TLS مع العملاء.

**اتصالات الأقران (من خادم إلى خادم / العنقود):**

تعمل خيارات الأقران بالطريقة نفسها التي تعمل بها خيارات العميل إلى الخادم:

`--peer-cert-file=<path>`: الشهادة المستخدمة لاتصالات SSL/TLS بين الأقران. ستُستخدم هذه الشهادة للاستماع على عنوان القرين وكذلك لإرسال الطلبات إلى الأقران الآخرين.

`--peer-key-file=<path>`: مفتاح الشهادة. يجب أن يكون غير مشفر.

`--peer-client-cert-auth`: عند ضبطه، سيتحقق etcd من جميع طلبات الأقران الواردة من العنقود بحثًا عن شهادات عملاء صالحة موقعة من مرجع الشهادات المقدم.

`--peer-trusted-ca-file=<path>`: مرجع الشهادات الموثوق.

`--peer-auto-tls`: استخدم شهادات موقعة ذاتيًا مولدة تلقائيًا لاتصالات TLS بين الأقران.

إذا قُدّمت شهادة عميل-إلى-خادم أو شهادة قرين، فيجب ضبط المفتاح أيضًا. جميع خيارات الإعداد هذه متاحة أيضًا عبر متغيرات البيئة، مثل `ETCD_TRUSTED_CA_FILE` و`ETCD_PEER_TRUSTED_CA_FILE` وما إلى ذلك.

**خيارات مشتركة:**

`--cipher-suites`: قائمة مفصولة بفواصل بمجموعات تشفير TLS المدعومة بين الخادم/العميل والأقران (الفارغة ستُملأ تلقائيًا بواسطة Go).

`--tls-min-version=<version>` يضبط الحد الأدنى لإصدار TLS الذي يدعمه etcd.

`--tls-max-version=<version>` يضبط الحد الأقصى لإصدار TLS الذي يدعمه etcd. إذا لم يُضبط، فسيُستخدم الحد الأقصى للإصدار الذي يدعمه Go.

### استخدام الامتدادين keyUsage وextendedKeyUsage في شهادة TLS {#tls-certificate-keyusage-and-extendedkeyusage}

عند إنشاء شهادات X.509 لتأمين نقل بيانات etcd،
ينبغي أن تتضمن الشهادات حقول `keyUsage` و
`extendedKeyUsage` المناسبة بحسب دورها. يعتمد etcd على مكتبتي
`crypto/tls` و`crypto/x509` في Go للتحقق من الشهادات،
وهما تفرضان هذه الاستخدامات أثناء مصافحة TLS.

يلخص الجدول التالي الاستخدامات الموصى بها لأدوار الشهادات الشائعة:

| دور الشهادة | keyUsage | extendedKeyUsage |
| ---------------- | -------- | ---------------- |
| خادم (من العميل إلى الخادم) | digitalSignature, keyEncipherment | serverAuth |
| عميل | digitalSignature, keyEncipherment | clientAuth |
| قرين (من خادم إلى خادم) | digitalSignature, keyEncipherment | serverAuth, clientAuth |

ملاحظات:

- عند تمكين `--peer-client-cert-auth`، تُستخدم شهادات الأقران لمصادقة TLS المتبادلة بين أعضاء etcd،
  ولذلك تتطلب كلًّا من `serverAuth` و`clientAuth`.
- ينبغي أن تتضمن شهادات العملاء المستخدمة مع `--client-cert-auth`
  القيمةَ `clientAuth`.

## المثال 1: أمان النقل من العميل إلى الخادم عبر HTTPS {#example-1-client-to-server-transport-security-with-https}

للقيام بذلك، جهّز مسبقًا شهادة CA (`ca.crt`) وزوج مفاتيح موقّعًا (`server.crt`، `server.key`).

لنضبط etcd لتوفير أمان نقل HTTPS بسيط خطوة بخطوة:

```sh
$ etcd --name infra0 --data-dir infra0 \
  --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls=https://127.0.0.1:2379 --listen-client-urls=https://127.0.0.1:2379
```

ينبغي أن يبدأ هذا دون مشكلات وستكون هناك إمكانية لاختبار الإعداد بالتحدث إلى etcd عبر HTTPS:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

ينبغي أن يُظهر الأمر نجاح المصافحة. وبما أننا نستخدم شهادات موقعة ذاتيًا مع مرجع الشهادات الخاص بنا، فيجب تمرير CA إلى curl باستخدام الخيار `--cacert`. وثمة إمكانية أخرى وهي إضافة شهادة CA إلى دليل الشهادات الموثوقة في النظام (عادةً في `/etc/pki/tls/certs` أو `/etc/ssl/certs`).

**مستخدمو OSX 10.9+**: لا يفهم curl 7.30.0 على OSX 10.9+ الشهادات الممررة في سطر الأوامر.
فبدلًا من ذلك، استورد ملف ca.crt التجريبي مباشرة إلى سلسلة المفاتيح (keychain) أو أضف العلم `-k` إلى curl لتجاهل الأخطاء.
لاختبار ذلك بدون العلم `-k`، شغّل `open ./tests/fixtures/ca/ca.crt` واتبع المطالبات.
يرجى إزالة هذه الشهادة بعد الاختبار!
إذا كانت هناك طريقة بديلة، فأخبرنا بها.

## المثال 2: المصادقة من العميل إلى الخادم بشهادات عملاء HTTPS {#example-2-client-to-server-authentication-with-https-client-certificates}

حتى الآن أعطينا عميل etcd القدرة على التحقق من هوية الخادم وتوفير أمان النقل. لكن يمكننا أيضًا استخدام شهادات العملاء لمنع الوصول غير المصرح به إلى etcd.

سيقدم العملاء شهاداتهم إلى الخادم، وسيتحقق الخادم مما إذا كانت الشهادة موقعة من مرجع الشهادات المقدم، ويقرر ما إذا كان سيخدم الطلب.

يلزم لذلك الملفات نفسها المذكورة في المثال الأول، وكذلك زوج مفاتيح للعميل (`client.crt`، `client.key`) موقّع من مرجع الشهادات نفسه.

```sh
$ etcd --name infra0 --data-dir infra0 \
  --client-cert-auth --trusted-ca-file=/path/to/ca.crt --cert-file=/path/to/server.crt --key-file=/path/to/server.key \
  --advertise-client-urls https://127.0.0.1:2379 --listen-client-urls https://127.0.0.1:2379
```

الآن جرّب الطلب نفسه السابق إلى هذا الخادم:

```sh
$ curl --cacert /path/to/ca.crt https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

ينبغي أن يرفض الخادم الطلب:

```
...
routines:SSL3_READ_BYTES:sslv3 alert bad certificate
...
```

لكي ينجح الطلب، يلزمنا إعطاء الخادم شهادة العميل الموقعة من CA:

```sh
$ curl --cacert /path/to/ca.crt --cert /path/to/client.crt --key /path/to/client.key \
  -L https://127.0.0.1:2379/v2/keys/foo -XPUT -d value=bar -v
```

ينبغي أن يتضمن المخرج:

```
...
SSLv3, TLS handshake, CERT verify (15):
...
TLS handshake, Finished (20)
```

وكذلك الاستجابة من الخادم:

```json
{
    "action": "set",
    "node": {
        "createdIndex": 12,
        "key": "/foo",
        "modifiedIndex": 12,
        "value": "bar"
    }
}
```

حدد مجموعات تشفير لصد [مجموعات تشفير TLS الضعيفة](https://github.com/etcd-io/etcd/issues/8320).

ستفشل مصافحة TLS عندما يُطلب ترحيب العميل (client hello) بمجموعات تشفير غير صالحة.

على سبيل المثال:

```bash
$ etcd \
  --cert-file ./server.crt \
  --key-file ./server.key \
  --trusted-ca-file ./ca.crt \
  --cipher-suites TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

بعد ذلك، يجب أن تحدد طلبات العميل إحدى مجموعات التشفير المحددة في الخادم:

```bash
# valid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-AES128-GCM-SHA256

# request succeeds
etcd_server_version{server_version="3.2.22"} 1
...
```

```bash
# invalid cipher suite
$ curl \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  -L [CLIENT-URL]/metrics \
  --ciphers ECDHE-RSA-DES-CBC3-SHA

# request fails with
(35) error:14094410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure
```

## المثال 3: أمان النقل وشهادات العملاء في عنقود {#example-3-transport-security--client-certificates-in-a-cluster}

يدعم etcd النموذج نفسه المذكور أعلاه **لاتصالات الأقران**، أي التواصل بين أعضاء etcd في عنقود.

بافتراض أن لدينا `ca.crt` وعضوين بأزواج مفاتيح خاصة بهما (`member1.crt` و`member1.key`، `member2.crt` و`member2.key`) موقعة من هذا المرجع، نطلق etcd كما يلي:


```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member1.crt --peer-key-file=/path/to/member1.key \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --peer-client-cert-auth --peer-trusted-ca-file=/path/to/ca.crt --peer-cert-file=/path/to/member2.crt --peer-key-file=/path/to/member2.key \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

سيشكل أعضاء etcd عنقودًا، وسيكون جميع التواصل بين أعضاء العنقود مشفرًا ومصادقًا عليه باستخدام شهادات العملاء. سيُظهر مخرج etcd أن العناوين التي يتصل بها تستخدم HTTPS.

## المثال 4: أمان نقل ذاتي التوقيع تلقائي {#example-4-automatic-self-signed-transport-security}

> [!WARNING]
> عند تحديد ClientAutoTLS وPeerAutoTLS، فإن مدة صلاحية شهادة العميل وشهادة القرين المولدتين تلقائيًا بواسطة etcd هي سنة واحدة فقط. يمكنك تحديد العلم --self-signed-cert-validity لضبط مدة صلاحية الشهادة بالسنوات.

للحالات التي يلزم فيها تشفير الاتصال دون المصادقة، يدعم etcd تشفير رسائله بشهادات موقعة ذاتيًا مولدة تلقائيًا. هذا يبسّط النشر لأنه لا حاجة إلى إدارة الشهادات والمفاتيح خارج etcd.
اضبط etcd لاستخدام الشهادات الموقعة ذاتيًا لاتصالات العملاء والأقران بالعلمين `--auto-tls` و`--peer-auto-tls`:

```sh
DISCOVERY_URL=... # from https://discovery.etcd.io/new

# member1
$ etcd --name infra1 --data-dir infra1 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.10:2380 --listen-peer-urls=https://10.0.1.10:2380 \
  --discovery ${DISCOVERY_URL}

# member2
$ etcd --name infra2 --data-dir infra2 \
  --auto-tls --peer-auto-tls \
  --initial-advertise-peer-urls=https://10.0.1.11:2380 --listen-peer-urls=https://10.0.1.11:2380 \
  --discovery ${DISCOVERY_URL}
```

الشهادات الموقعة ذاتيًا لا تصادق على الهوية، لذلك سيعيد curl خطأ:

```sh
curl: (60) SSL certificate problem: Invalid certificate chain
```

لتعطيل فحص سلسلة الشهادات، استدعِ curl بالعلم `-k`:

```sh
$ curl -k https://127.0.0.1:2379/v2/keys/foo -Xput -d value=bar -v
```

## ملاحظات بشأن DNS SRV {#notes-for-dns-srv}

منذ v3.1.0 (باستثناء v3.2.9)، تصادق تهيئة الإقلاع عبر اكتشاف SRV على `ServerName` باستخدام اسم نطاق جذر مأخوذ من العلم `--discovery-srv`. الغرض من ذلك تجنب هجمات شهادات الوسيط (man-in-the-middle) عبر اشتراط أن تحمل الشهادة اسم نطاق جذر مطابقًا في حقل اسم الموضوع البديل (SAN). فمثلًا، `etcd --discovery-srv=etcd.local` لن يصادق على الأقران/العملاء إلا عندما تحمل الشهادات المقدمة اسم النطاق الجذر `etcd.local` بوصفه إدخالًا في حقل اسم الموضوع البديل (SAN)

## ملاحظات بشأن وسيط etcd {#notes-for-etcd-proxy}

> [!NOTE]
> يصف هذا القسم وسيط v2 التاريخي، الذي أزيل. بالنسبة إلى etcd 3.7، استخدم [وسيط gRPC الخاص بـ v3](/ar/etcd/op-guide/grpc_proxy/).

ينهي وسيط etcd اتصال TLS القادم من عميله إذا كان الاتصال آمنًا، ويستخدم مفتاح/شهادة الوسيط نفسه المحددين في `--peer-key-file` و`--peer-cert-file` للتواصل مع أعضاء etcd.

يتواصل الوسيط مع أعضاء etcd عبر كل من `--advertise-client-urls` و`--advertise-peer-urls` لعضو معيّن. فهو يحيل طلبات العملاء إلى عناوين URL للعملاء المُعلَنة الخاصة بأعضاء etcd، ويزامن إعداد العنقود الأولي عبر عناوين URL للأقران المُعلَنة الخاصة بأعضاء etcd.

عند تمكين مصادقة العملاء لأحد أعضاء etcd، يجب على المسؤول التأكد من أن شهادة القرين المحددة في خيار `--peer-cert-file` الخاص بالوسيط صالحة لتلك المصادقة. ويجب أيضًا أن تكون شهادة القرين الخاصة بالوسيط صالحة لمصادقة الأقران إذا كانت مصادقة الأقران مُمكّنة.

## ملاحظات بشأن مصادقة TLS {#notes-for-tls-authentication}

منذ [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)، [يُعاد تحميل شهادات TLS عند كل اتصال عميل](https://github.com/etcd-io/etcd/pull/7829). هذا مفيد عند استبدال الشهادات منتهية الصلاحية دون إيقاف خوادم etcd؛ ويمكن ذلك بالكتابة فوق الشهادات القديمة بأخرى جديدة. لا ينبغي أن يكون لإعادة تحميل الشهادات عند كل اتصال عبء كبير، لكن يمكن تحسينها مستقبلًا بطبقة تخزين مؤقت. يمكن العثور على أمثلة اختبارات [هنا](https://github.com/etcd-io/etcd/blob/b041ce5d514a4b4aaeefbffb008f0c7570a18986/integration/v3_grpc_test.go#L1601-L1757).

منذ [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)، [يرفض الخادم شهادات الأقران الواردة ذات `SAN` بعنوان IP خاطئ](https://github.com/etcd-io/etcd/pull/7687). فمثلًا، إذا كانت شهادة القرين تحتوي على أي عناوين IP في حقل اسم الموضوع البديل (SAN)، فسيصادق الخادم على القرين فقط عندما يطابق عنوان IP البعيد أحد تلك العناوين. الغرض من ذلك منع نقاط النهاية غير المصرح بها من الانضمام إلى العنقود. فمثلًا، طلب توقيع الشهادة (CSR) الخاص بالقرين B (باستخدام `cfssl`) هو:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local",
    "10.138.0.27"
  ],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "US",
      "L": "CA",
      "ST": "San Francisco"
    }
  ]
}
```

بينما عنوان IP الفعلي للقرين B هو `10.138.0.2` وليس `10.138.0.27`. عندما يحاول القرين B الانضمام إلى العنقود، سيرفضه القرين A بالخطأ `x509: certificate is valid for 10.138.0.27, not 10.138.0.2`، لأن عنوان IP البعيد لـ B لا يطابق العنوان الموجود في حقل اسم الموضوع البديل (SAN).

منذ [v3.2.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v320-2017-06-09)، [يحل الخادم أسماء `DNSNames` في TLS عند فحص `SAN`](https://github.com/etcd-io/etcd/pull/7767). فمثلًا، إذا كانت شهادة القرين لا تحتوي إلا على أسماء DNS (بلا عناوين IP) في حقل اسم الموضوع البديل (SAN)، فسيصادق الخادم على القرين فقط عندما تعيد عمليات البحث الأمامية (`dig b.com`) على أسماء DNS تلك عنوان IP مطابقًا لعنوان IP البعيد. فمثلًا، طلب توقيع الشهادة (CSR) الخاص بالقرين B (باستخدام `cfssl`) هو:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "b.com"
  ],
```

عندما يكون عنوان IP البعيد للقرين B هو `10.138.0.2`. عندما يحاول القرين B الانضمام إلى العنقود، يبحث القرين A عن المضيف الوارد `b.com` للحصول على قائمة عناوين IP (مثل `dig b.com`). ويرفض B إذا كانت القائمة لا تحتوي على IP ‏`10.138.0.2`، بالخطأ `tls: 10.138.0.2 does not match any of DNSNames ["b.com"]`.

منذ [v3.2.2](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v322-2017-07-07)، [يقبل الخادم الاتصالات إذا تطابق عنوان IP دون فحص إدخالات DNS](https://github.com/etcd-io/etcd/pull/8223). فمثلًا، إذا كانت شهادة القرين تحتوي على عناوين IP وأسماء DNS في حقل اسم الموضوع البديل (SAN)، وكان عنوان IP البعيد يطابق أحد تلك العناوين، فسيقبل الخادم الاتصال ببساطة دون فحص أسماء DNS بمزيد من التدقيق. فمثلًا، طلب توقيع الشهادة (CSR) الخاص بالقرين B (باستخدام `cfssl`) هو:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "invalid.domain",
    "10.138.0.2"
  ],
```

عندما يكون عنوان IP البعيد للقرين B هو `10.138.0.2` و`invalid.domain` مضيفًا غير صالح. عندما يحاول القرين B الانضمام إلى العنقود، يصادق القرين A على B بنجاح، لأن حقل اسم الموضوع البديل (SAN) يحتوي على عنوان IP صالح مطابق. انظر [issue#8206](https://github.com/etcd-io/etcd/issues/8206) لمزيد من التفاصيل.

منذ [v3.2.5](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md#v325-2017-08-04)، [يدعم الخادم البحث العكسي على `SAN` لأسماء DNS ذات أحرف البدل](https://github.com/etcd-io/etcd/pull/8281). فمثلًا، إذا كانت شهادة القرين لا تحتوي إلا على أسماء DNS (بلا عناوين IP) في حقل اسم الموضوع البديل (SAN)، فسيجري الخادم أولًا بحثًا عكسيًا عن عنوان IP البعيد للحصول على قائمة أسماء ترتبط بذلك العنوان (مثل `nslookup IPADDR`). ثم يقبل الاتصال إذا كان لأحد تلك الأسماء اسم مطابق لأسماء DNS في شهادة القرين (بالتطابق التام أو بمطابقة أحرف البدل). وإن لم يتطابق أي منها، يبحث الخادم بحثًا أماميًا عن كل إدخال DNS في شهادة القرين (مثل البحث عن `example.default.svc` عندما يكون الإدخال `*.example.default.svc`)، ولا يقبل الاتصال إلا عندما تكون للعناوين التي حُلَّ إليها المضيف قيمة IP مطابقة لعنوان IP البعيد للقرين. فمثلًا، طلب توقيع الشهادة (CSR) الخاص بالقرين B (باستخدام `cfssl`) هو:

```json
{
  "CN": "etcd peer",
  "hosts": [
    "*.example.default.svc",
    "*.example.default.svc.cluster.local"
  ],
```

عندما يكون عنوان IP البعيد للقرين B هو `10.138.0.2`. عندما يحاول القرين B الانضمام إلى العنقود، يجري القرين A بحثًا عكسيًا عن IP ‏`10.138.0.2` للحصول على قائمة أسماء المضيفين. ثم يطابق أسماء المضيفين، تطابقًا تامًا أو بمطابقة أحرف البدل، مع أسماء DNS في شهادة القرين B في حقل اسم الموضوع البديل (SAN). وإذا لم ينجح أي من البحثين العكسي/الأمامي، يعيد الخطأ `"tls: "10.138.0.2" does not match any of DNSNames ["*.example.default.svc","*.example.default.svc.cluster.local"]`. انظر [issue#8268](https://github.com/etcd-io/etcd/issues/8268) لمزيد من التفاصيل.

يضيف [v3.3.0](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) العلم [`etcd --peer-cert-allowed-cn`](https://github.com/etcd-io/etcd/pull/8616) لدعم [المصادقة القائمة على CN (الاسم الشائع) لاتصالات الأقران](https://github.com/etcd-io/etcd/issues/8262). تتضمن تهيئة إقلاع TLS في Kubernetes إنشاء شهادات ديناميكية لأعضاء etcd ولمكونات النظام الأخرى (مثل خادم API وkubelet وغيرها). والحفاظ على مراجع CAs مختلفة لكل مكون يوفر تحكمًا أدق في الوصول إلى عنقود etcd لكنه غالبًا ما يكون مرهقًا. عند تحديد العلم --peer-cert-allowed-cn، لن تتمكن العقدة من الانضمام إلا باسم شائع مطابق حتى مع مراجع CAs مشتركة. المطابقة هي مقارنة نصية تامة مقابل حقل الاسم الشائع (CN) في الشهادة — لا تدعم أحرف البدل ولا مطابقة البادئات. أما الترشيح القائم على اسم المضيف باستخدام --peer-cert-allowed-hostname أو --client-cert-allowed-hostname، فتستخدم المطابقة فيه الدالة x509.Certificate.VerifyHostname() في Go، التي تدعم أسماء المضيفين التامة وإدخالات أحرف البدل معًا (مثل *.example.com). فمثلًا، يُعد كل عضو في عنقود من 3 عقد بطلبات توقيع شهادات (CSRs) (باستخدام cfssl) كما يلي:



```json
{
  "CN": "etcd.local",
  "hosts": [
    "m1.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m2.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

```json
{
  "CN": "etcd.local",
  "hosts": [
    "m3.etcd.local",
    "127.0.0.1",
    "localhost"
  ],
```

بعدها لن يُصادق إلا على الأقران ذوي الأسماء الشائعة المطابقة إذا أُعطي `--peer-cert-allowed-cn etcd.local`. وستُرفض العقد ذات CNs مختلفة في CSRs أو ذات `--peer-cert-allowed-cn` مختلف:

```bash
$ etcd --peer-cert-allowed-cn m1.etcd.local

I | embed: rejected connection from "127.0.0.1:48044" (error "CommonName authentication failed", ServerName "m1.etcd.local")
I | embed: rejected connection from "127.0.0.1:55702" (error "remote error: tls: bad certificate", ServerName "m3.etcd.local")
```

ينبغي بدء كل عملية بما يلي:

```bash
etcd --peer-cert-allowed-cn etcd.local

I | pkg/netutil: resolving m3.etcd.local:32380 to 127.0.0.1:32380
I | pkg/netutil: resolving m2.etcd.local:22380 to 127.0.0.1:22380
I | pkg/netutil: resolving m1.etcd.local:2380 to 127.0.0.1:2380
I | etcdserver: published {Name:m3 ClientURLs:[https://m3.etcd.local:32379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m1 ClientURLs:[https://m1.etcd.local:2379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | etcdserver: published {Name:m2 ClientURLs:[https://m2.etcd.local:22379]} to cluster 9db03f09b20de32b
I | embed: ready to serve client requests
I | embed: serving client requests on 127.0.0.1:32379
I | embed: serving client requests on 127.0.0.1:22379
I | embed: serving client requests on 127.0.0.1:2379
```

يصلح [v3.2.19](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.2.md) و[v3.3.4](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) إعادة تحميل TLS عندما [يشتمل حقل SAN في الشهادة على عناوين IP فقط دون أسماء نطاقات](https://github.com/etcd-io/etcd/issues/9541). فمثلًا، يُعد أحد الأعضاء بطلب توقيع شهادة (CSR) (باستخدام `cfssl`) كما يلي:

```json
{
  "CN": "etcd.local",
  "hosts": [
    "127.0.0.1"
  ],
```

في Go، يستدعي الخادم `(*tls.Config).GetCertificate` لإعادة تحميل TLS إذا وفقط إذا كان حقل `(*tls.Config).Certificates` الخاص بالخادم فارغًا، أو كان `(*tls.ClientHelloInfo).ServerName` غير فارغ مع SNI صالح من العميل. سابقًا، كان etcd يملأ `(*tls.Config).Certificates` دائمًا عند مصافحة TLS الأولية للعميل بقيمة غير فارغة. وبالتالي كان يُتوقع من العميل دائمًا أن يقدم SNI مطابقًا لاجتياز التحقق من TLS ولتحفيز `(*tls.Config).GetCertificate` على إعادة تحميل أصول TLS.

غير أن الشهادة التي [لا يتضمن حقل SAN فيها أي أسماء نطاقات بل عناوين IP فقط](https://github.com/etcd-io/etcd/issues/9541) ستطلب `*tls.ClientHelloInfo` بحقل `ServerName` فارغ، فتفشل بالتالي في تحفيز إعادة تحميل TLS عند مصافحة TLS الأولية؛ وتصبح هذه مشكلة عندما يلزم استبدال شهادات منتهية الصلاحية أثناء التشغيل.

الآن، يُنشأ `(*tls.Config).Certificates` فارغًا عند مصافحة TLS الأولية للعميل، أولًا لتحفيز `(*tls.Config).GetCertificate`، ثم لملء بقية الشهادات عند كل اتصال TLS جديد، حتى عندما يكون SNI للعميل فارغًا (مثلًا عندما تتضمن الشهادة عناوين IP فقط).

## ملاحظات بشأن القائمة البيضاء للمضيفين {#notes-for-host-whitelist}

يحدد العلم `etcd --host-whitelist` أسماء المضيفين المقبولة من طلبات HTTP الخاصة بالعملاء. تحمي سياسة أصل العميل من هجمات [«إعادة ربط DNS» (DNS Rebinding)](https://en.wikipedia.org/wiki/DNS_rebinding) على خوادم etcd غير الآمنة. ذلك أن أي موقع ويب يمكنه ببساطة إنشاء اسم DNS مصرح به، وتوجيه DNS إلى `"localhost"` (أو أي عنوان آخر). وعندها تصبح جميع نقاط نهاية HTTP لخادم etcd المستمع على `"localhost"` متاحة الوصول، ومن ثم عرضة لهجمات إعادة ربط DNS. انظر [CVE-2018-5702](https://bugs.chromium.org/p/project-zero/issues/detail?id=1447#c2) لمزيد من التفاصيل.

تعمل سياسة أصل العميل كما يلي:

1. إذا كان اتصال العميل آمنًا عبر HTTPS، فاسمح بأي أسماء مضيفين.
2. إذا كان اتصال العميل غير آمن وكانت `"HostWhitelist"` غير فارغة، فاسمح فقط بطلبات HTTP التي يكون حقل Host فيها مدرجًا في القائمة البيضاء.

لاحظ أن سياسة أصل العميل مفروضة سواء مُكنت المصادقة أم لم تُمكن، لأغراض تحكم أدق.

افتراضيًا، يستخدم `etcd --host-whitelist` و`embed.Config.HostWhitelist` القيمة `*` للسماح بجميع أسماء المضيفين. والقائمة البيضاء الفارغة تسمح أيضًا بجميع أسماء المضيفين. لاحظ أنه عند تحديد أسماء المضيفين، لا تُضاف عناوين loopback تلقائيًا. للسماح بواجهات loopback، أضفها يدويًا إلى القائمة البيضاء (مثل `"localhost"` و`"127.0.0.1"` وما إلى ذلك).

## الأسئلة الشائعة {#frequently-asked-questions}

### أرى فشل مصافحة بتنبيه SSLv3 عند استخدام مصادقة عميل TLS؟ {#im-seeing-a-sslv3-alert-handshake-failure-when-using-tls-client-authentication}

تتحقق الحزمة `crypto/tls` في `golang` من استخدام مفتاح الشهادة العام قبل استخدامه.
ولاستخدام مفتاح الشهادة العام للمصادقة على العميل، يلزمنا إضافة `clientAuth` إلى `Extended Key Usage` عند إنشاء مفتاح الشهادة العام.

إليك كيفية القيام بذلك:

أضف القسم التالي إلى openssl.cnf:

```
[ ssl_client ]
...
  extendedKeyUsage = clientAuth
...
```

عند إنشاء الشهادة، احرص على الإشارة إليه في العلم `-extensions`:

```
$ openssl ca -config openssl.cnf -policy policy_anything -extensions ssl_client -out certs/machine.crt -infiles machine.csr
```

### مع مصادقة شهادة القرين أتلقى "certificate is valid for 127.0.0.1, not $MY_IP" {#with-peer-certificate-authentication-i-receive-certificate-is-valid-for-127001-not-my_ip}
احرص على توقيع الشهادات باسم موضوع يحدد عنوان IP العام للعضو. فأداة `etcd-ca` مثلًا توفر خيار `--ip=` لأمرها `new-cert`.

يلزم توقيع الشهادة باسم FQDN الخاص بالعضو في اسم الموضوع، واستخدام أسماء الموضوع البديلة (اختصارًا IP SANs) لإضافة عنوان IP. توفر أداة `etcd-ca` الخيار `--domain=` لأمرها `new-cert`، ويمكن لـ openssl أيضًا [فعل ذلك][alt-name].

### هل يشفر etcd البيانات المخزنة على محركات الأقراص؟ {#does-etcd-encrypt-data-stored-on-disk-drives}
لا. لا يشفر etcd بيانات المفتاح/القيمة المخزنة على محركات الأقراص. إذا احتاج المستخدم إلى تشفير البيانات المخزنة في etcd، فهناك بعض الخيارات:
* ترك تطبيقات العميل تشفر البيانات وتفك تشفيرها
* استخدام ميزة من نظم التخزين الكامنة لتشفير البيانات المخزنة مثل [dm-crypt]

### أرى في السجل تحذيرًا بأن "directory X exist without recommended permission -rwx------" {#im-seeing-a-log-warning-that-directory-x-exist-without-recommended-permission--rwx}
عندما ينشئ etcd أدلة جديدة معينة، يضبط صلاحية الملف على 700 لمنع الوصول غير المصرح به قدر الإمكان. لكن إذا كان المستخدم قد أنشأ دليلًا بالفعل حسب تفضيله، فسيستخدم etcd الدليل الموجود ويسجل رسالة تحذير إذا كانت الصلاحية مختلفة عن 700.

[alt-name]: http://wiki.cacert.org/FAQ/subjectAltName
[auth]: /ar/etcd/op-guide/authentication/
[cfssl]: https://github.com/cloudflare/cfssl
[dm-crypt]: https://en.wikipedia.org/wiki/Dm-crypt
[tls-guide]: https://github.com/coreos/docs/blob/master/os/generate-self-signed-certificates.md
[tls-setup]: https://github.com/etcd-io/etcd/tree/main/hack/tls-setup
[etcd help]: https://github.com/etcd-io/etcd/blob/main/server/etcdmain/help.go
