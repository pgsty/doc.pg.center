---
title: وسيط gRPC (gRPC proxy)
weight: 4350
description: "وسيط عكسي عديم الحالة لـ etcd يعمل في طبقة gRPC"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/grpc_proxy.md"
---

وسيط gRPC هو وسيط عكسي عديم الحالة لـ etcd يعمل في طبقة gRPC (L7). صُمم الوسيط لتقليل إجمالي حمل المعالجة الواقع على عنقود etcd الأساسي. وللحفاظ على قابلية التوسع الأفقي، يدمج طلبات واجهة watch وعقود الإيجار (lease). ولحماية العنقود من العملاء المسيئين، يخزّن طلبات نطاقات المفاتيح مؤقتًا.

يدعم وسيط gRPC نقاط نهاية متعددة لخوادم etcd. عند بدء الوسيط، يختار عشوائيًا نقطة نهاية واحدة لخادم etcd لاستخدامها. تخدم نقطة النهاية هذه جميع الطلبات حتى يكتشف الوسيط تعطل نقطة النهاية. وإذا اكتشف وسيط gRPC تعطل نقطة النهاية، ينتقل إلى نقطة نهاية مختلفة، إن كانت متاحة، لإخفاء الأعطال عن عملائه. وقد تُدعم سياسات إعادة محاولة أخرى، مثل التناوب الدوري الموزون، مستقبلًا.

## واجهة API المراقبة القابلة للتوسع {#scalable-watch-api}

يدمج وسيط gRPC عدة مراقِبين للعملاء (`c-watchers`) على المفتاح نفسه أو النطاق نفسه في مراقِب واحد (`s-watcher`) متصل بخادم etcd. ويبثّ الوسيط جميع الأحداث الواردة من `s-watcher` إلى مراقِبيه `c-watchers`.

بافتراض أن N من العملاء يراقبون المفتاح نفسه، يستطيع وسيط gRPC واحد تقليل حمل المراقبة على خادم etcd من N إلى 1. ويمكن للمستخدمين نشر عدة وسطاء gRPC لتوزيع حمل الخادم على نطاق أوسع.

في المثال التالي، يراقب ثلاثة عملاء المفتاح A. يدمج وسيط gRPC المراقِبين الثلاثة، منشئًا مراقِبًا واحدًا مرفقًا بخادم etcd.

```
            +-------------+
            | etcd server |
            +------+------+
                   ^ watch key A (s-watcher)
                   |
           +-------+-----+
           | gRPC proxy  | <-------+
           |             |         |
           ++-----+------+         |watch key A (c-watcher)
watch key A ^     ^ watch key A    |
(c-watcher) |     | (c-watcher)    |
    +-------+-+  ++--------+  +----+----+
    |  client |  |  client |  |  client |
    |         |  |         |  |         |
    +---------+  +---------+  +---------+
```

### القيود {#limitations}

لدمج مراقِبي العملاء المتعددين بفعالية في مراقِب واحد، يدمج وسيط gRPC مراقِبي `c-watchers` الجدد في `s-watcher` موجود كلما أمكن ذلك. وقد يكون `s-watcher` المدموج هذا غير متزامن مع خادم etcd بسبب تأخيرات الشبكة أو أحداث مخزنة مؤقتًا لم تُسلَّم بعد. وعندما لا تُحدَّد مراجعة المراقبة، لن يضمن وسيط gRPC أن يبدأ `c-watcher` المراقبة من أحدث مراجعة للمخزن. مثلًا، إذا راقب عميل من خادم etcd ذي المراجعة 1000، فسيبدأ ذلك المراقِب من المراجعة 1000. أما إذا راقب عميل من وسيط gRPC، فقد يبدأ المراقبة من المراجعة 990.

تنطبق قيود مشابهة على الإلغاء. عند إلغاء المراقِب، قد تكون مراجعة خادم etcd أكبر من مراجعة استجابة الإلغاء.

ينبغي ألا يسبب هذان القيدان مشكلات لمعظم حالات الاستخدام. وقد تتوفر مستقبلًا خيارات إضافية لإجبار المراقِب على تجاوز وسيط gRPC للحصول على استجابات مراجعة أدق.

## واجهة API عقود الإيجار القابلة للتوسع {#scalable-lease-api}

لإبقاء عقود الإيجار الخاصة به نشطة، يجب على العميل إنشاء تدفق gRPC واحد على الأقل إلى خادم etcd لإرسال نبضات القلب الدورية. وإذا تضمن عبء عمل etcd نشاطًا كثيفًا لعقود الإيجار موزعًا على عملاء كثيرين، فقد تسهم هذه التدفقات في استهلاك مفرط للمعالج. ولتقليل العدد الإجمالي للتدفقات على العنقود الأساسي، يدعم الوسيط دمج تدفقات عقود الإيجار.

بافتراض أن N من العملاء يحدّثون عقود الإيجار، يقلل وسيط gRPC واحد حمل التدفقات على خادم etcd من N إلى 1. وقد تتضمن عمليات النشر وسطاء gRPC إضافيين لتوزيع التدفقات على وسطاء متعددين على نحو أوسع.

في المثال التالي، يحدّث ثلاثة عملاء ثلاثة عقود إيجار مستقلة (`L1` و`L2` و`L3`). يدمج وسيط gRPC تدفقات عقود الإيجار الثلاثة للعملاء (`c-streams`) في تدفق واحد لإبقاء عقود الإيجار حية (`s-stream`) مرفق بخادم etcd. ويعيد الوسيط توجيه نبضات قلب عقود الإيجار من جهة العملاء من c-streams إلى s-stream، ثم يعيد الاستجابات إلى c-streams المقابلة.

```
          +-------------+
          | etcd server |
          +------+------+
                 ^
                 | heartbeat L1, L2, L3
                 | (s-stream)
                 v
         +-------+-----+
         | gRPC proxy  +<-----------+
         +---+------+--+            | heartbeat L3
             ^      ^               | (c-stream)
heartbeat L1 |      | heartbeat L2  |
(c-stream)   v      v (c-stream)    v
      +------+-+  +-+------+  +-----+--+
      | client |  | client |  | client |
      +--------+  +--------+  +--------+
```

## الحماية من العملاء المسيئين {#abusive-clients-protection}

يخزّن وسيط gRPC الاستجابات للطلبات مؤقتًا عندما لا يخل ذلك بمتطلبات الاتساق. ويحمي هذا خادم etcd من العملاء المسيئين الذين ينفذون حلقات for ضيقة.

## بدء وسيط gRPC لـ etcd {#start-etcd-grpc-proxy}

تخيّل عنقود etcd بنقاط النهاية الثابتة التالية:

|الاسم|العنوان|اسم المضيف|
|------|---------|------------------|
|infra0|10.0.1.10|infra0.example.com|
|infra1|10.0.1.11|infra1.example.com|
|infra2|10.0.1.12|infra2.example.com|

ابدأ وسيط gRPC لـ etcd ليستخدم نقاط النهاية الثابتة هذه بالأمر التالي:

```bash
$ etcd grpc-proxy start --endpoints=infra0.example.com,infra1.example.com,infra2.example.com --listen-addr=127.0.0.1:2379
```

يبدأ وسيط gRPC لـ etcd ويستمع على المنفذ 2379. ويعيد توجيه طلبات العملاء إلى إحدى نقاط النهاية الثلاث المقدمة أعلاه.

إرسال الطلبات عبر الوسيط:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 put foo bar
OK
$ ETCDCTL_API=3 etcdctl --endpoints=127.0.0.1:2379 get foo
foo
bar
```

## مزامنة نقاط نهاية العملاء وترجمة الأسماء {#client-endpoint-synchronization-and-name-resolution}

يدعم الوسيط تسجيل نقاط نهايته لغرض الاكتشاف عبر الكتابة إلى نقطة نهاية يحددها المستخدم. ويخدم ذلك هدفين. أولًا، يتيح للعملاء مزامنة نقاط نهايتهم مع مجموعة من نقاط نهاية الوسيط لتحقيق التوافرية العالية. ثانيًا، يعمل موفّرًا لنقاط النهاية لـ etcd [ترجمة أسماء gRPC](/ar/etcd/dev-guide/grpc_naming/).

سجّل وسيطًا واحدًا أو أكثر بتقديم بادئة يحددها المستخدم:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --advertise-client-url=127.0.0.1:23790 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60

$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23791 \
  --advertise-client-url=127.0.0.1:23791 \
  --resolver-prefix="___grpc_proxy_endpoint" \
  --resolver-ttl=60
```

سيدرج الوسيط جميع أعضائه في member list:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23790 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23791 |
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23790 |
+----+---------+--------------------------------+------------+-----------------+
```

يتيح هذا للعملاء اكتشاف نقاط نهاية الوسيط تلقائيًا عبر Sync:

```go
cli, err := clientv3.New(clientv3.Config{
    Endpoints: []string{"http://localhost:23790"},
})
if err != nil {
    log.Fatal(err)
}
defer cli.Close()

// fetch registered grpc-proxy endpoints
if err := cli.Sync(context.Background()); err != nil {
    log.Fatal(err)
}
```

لاحظ أنه إذا أُعدّ وسيط دون بادئة محلِّل (resolver)،

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23792 \
  --advertise-client-url=127.0.0.1:23792
```

فإن واجهة API الخاصة بـ member list على grpc-proxy تُعيد عنوان `advertise-client-url` الخاص بها:

```bash
ETCDCTL_API=3 etcdctl --endpoints=http://localhost:23792 member list --write-out table

+----+---------+--------------------------------+------------+-----------------+
| ID | STATUS  |              NAME              | PEER ADDRS |  CLIENT ADDRS   |
+----+---------+--------------------------------+------------+-----------------+
|  0 | started | Gyu-Hos-MBP.sfo.coreos.systems |            | 127.0.0.1:23792 |
+----+---------+--------------------------------+------------+-----------------+
```

## مساحات الأسماء {#namespacing}

افترض أن تطبيقًا ما يتوقع تحكمًا كاملًا في فضاء المفاتيح بأكمله، بينما يُشارَك عنقود etcd مع تطبيقات أخرى. ولكي تعمل جميع التطبيقات دون التداخل فيما بينها، يستطيع الوسيط تقسيم فضاء مفاتيح etcd بحيث يبدو للعملاء أن لديهم وصولًا إلى فضاء المفاتيح كاملًا. وعندما يُعطى الوسيط العلم `--namespace`، تُترجم جميع طلبات العملاء الداخلة إلى الوسيط بحيث تصبح للمفاتيح بادئة يحددها المستخدم. وستكون عمليات الوصول إلى عنقود etcd تحت هذه البادئة، وستنزع الاستجابات الصادرة عن الوسيط البادئةَ؛ فيبدو للعميل وكأن لا بادئة على الإطلاق.

لوضع الوسيط في مساحة أسماء، ابدأه بـ `--namespace`:

```bash
$ etcd grpc-proxy start --endpoints=localhost:2379 \
  --listen-addr=127.0.0.1:23790 \
  --namespace=my-prefix/
```

أصبحت عمليات الوصول إلى الوسيط تُسبَق بالبادئة بشفافية على عنقود etcd:

```bash
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 put my-key abc
# OK
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:23790 get my-key
# my-key
# abc
$ ETCDCTL_API=3 etcdctl --endpoints=localhost:2379 get my-prefix/my-key
# my-prefix/my-key
# abc
```

## إنهاء TLS {#tls-termination}

أنهِ اتصالات TLS الواردة من عنقود etcd مؤمَّن بمساعدة وسيط gRPC عبر تقديم نقطة نهاية محلية غير مشفَّرة.

لتجربة ذلك، ابدأ عنقود etcd أحادي العضو بـ https على جهة العميل:

```sh
$ etcd --listen-client-urls https://localhost:2379 --advertise-client-urls https://localhost:2379 --cert-file=peer.crt --key-file=peer.key --trusted-ca-file=ca.crt --client-cert-auth
```

تأكد من أن منفذ العميل يقدم خدمة https:

```sh
# fails
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:2379 endpoint status
# works
$ ETCDCTL_API=3 etcdctl --endpoints=https://localhost:2379 --cert=client.crt --key=client.key --cacert=ca.crt endpoint status
```

بعد ذلك، ابدأ وسيط gRPC على `localhost:12379` بالاتصال بنقطة نهاية etcd ‏`https://localhost:2379` باستخدام شهادات العميل:

```sh
$ etcd grpc-proxy start --endpoints=https://localhost:2379 --listen-addr localhost:12379 --cert client.crt --key client.key --cacert=ca.crt --insecure-skip-tls-verify &
```

أخيرًا، اختبر إنهاء TLS بوضع مفتاح في الوسيط عبر http:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints=http://localhost:12379 put abc def
# OK
```

## المقاييس والصحة {#metrics-and-health}

يعرّض وسيط gRPC نقطتَي النهاية `/health` وPrometheus ‏`/metrics` لأعضاء etcd المحددين بواسطة `--endpoints`. وبدلًا من ذلك، يمكن تحديد URL إضافية ستستجيب لنقطتَي النهاية `/metrics` و`/health` معًا باستخدام العلم `--metrics-addr`.

```bash
$ etcd grpc-proxy start \
  --endpoints https://localhost:2379 \
  --metrics-addr https://0.0.0.0:4443 \
  --listen-addr 127.0.0.1:23790 \
  --key client.key \
  --key-file proxy-server.key \
  --cert client.crt \
  --cert-file proxy-server.crt \
  --cacert ca.pem \
  --trusted-ca-file proxy-ca.pem
 ```

### مشكلة معروفة {#known-issue}

تخدم الواجهة الرئيسية للوسيط كلًّا من HTTP2 وHTTP/1.1. فإذا أُعدّ الوسيط بـ TLS كما في المثال أعلاه، فإن استخدام عميل مثل cURL ضد الواجهة المستمعة سيتطلب تعيين البروتوكول صراحةً إلى HTTP/1.1 في الطلب لإرجاع `/metrics` أو `/health`. وباستخدام العلم `--metrics-addr` لن تخضع الواجهة الثانوية لهذا المطلب.

```bash
 $ curl --cacert proxy-ca.pem --key proxy-client.key --cert proxy-client.crt https://127.0.0.1:23790/metrics --http1.1
```
