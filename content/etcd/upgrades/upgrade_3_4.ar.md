---
title: ترقية etcd من 3.3 إلى 3.4
weight: 6700
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من 3.3 إلى 3.4"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd 3.3 إلى 3.4 ترقية متدرجة دون أي توقف:
 - واحدًا تلو الآخر، أوقف عمليات etcd v3.3 واستبدلها بعمليات etcd v3.4
 - بعد تشغيل جميع عمليات v3.4، تصبح الميزات الجديدة في v3.4 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.



### قوائم التحقق من الترقية {#upgrade-checklists}

> [!WARNING]
> عند [الترحيل من v2 دون بيانات v3](https://github.com/etcd-io/etcd/issues/9480)، يُسبب خادم etcd v3.2+ حالة panic عندما يستعيد etcd من لقطات موجودة ولكن دون ملف v3 باسم `ETCD_DATA_DIR/member/snap/db`. يحدث هذا عندما يكون الخادم قد رُحِّل من v2 دون أي بيانات v3 سابقة. ويمنع هذا أيضًا الفقدان العرضي لبيانات v3 (مثلًا، قد يكون ملف `db` قد نُقل). يشترط etcd وجود بيانات v3 لإجراء عمليات الترحيل اللاحقة ضمن v3. لا تقم بالترقية إلى إصدارات v3 أحدث حتى يحتوي خادم v3.0 على بيانات v3.

أبرز التغييرات الكاسرة في 3.4.

#### جعل `ETCDCTL_API=3 etcdctl` هو الافتراضي {#make-etcdctl_api3-etcdctl-default}

أصبح `ETCDCTL_API=3` هو الافتراضي الآن.

```diff
etcdctl set foo bar
Error: unknown command "set" for "etcdctl"

-etcdctl set foo bar
+ETCDCTL_API=2 etcdctl set foo bar
bar

ETCDCTL_API=3 etcdctl put foo bar
OK

-ETCDCTL_API=3 etcdctl put foo bar
+etcdctl put foo bar
```

#### جعل `etcd --enable-v2=false` هو الافتراضي {#make-etcd---enable-v2false-default}

أصبح [`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) هو الافتراضي الآن.

هذا يعني أنه ما لم يُحدَّد `etcd --enable-v2=true`، فلن يخدم خادم etcd v3.4 طلبات واجهة v2 API.

إذا كانت واجهة v2 API مستخدمة، فتأكد من تمكين واجهة v2 API في v3.4:

```diff
-etcd
+etcd --enable-v2=true
```

ستظل واجهات HTTP الأخرى تعمل (مثلًا `[CLIENT-URL]/metrics` و`[CLIENT-URL]/health` وبوابة gRPC الخاصة بـ v3).

#### إهمال العلامتين `etcd --ca-file` و`etcd --peer-ca-file` {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

العلامتان `--ca-file` و`--peer-ca-file` مهملتان؛ فقد أُهملتا منذ v2.1.

لاحظ أن تعيين هذه المعلمة سيمكّن أيضًا تلقائيًا مصادقة شهادة العميل بغض النظر عن القيمة المعينة للعلامة `--client-cert-auth`.

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### إهمال الخطأ `grpc.ErrClientConnClosing` {#deprecated-grpcerrclientconnclosing-error}

أُهمل `grpc.ErrClientConnClosing` [في gRPC >= 1.10](https://github.com/grpc/grpc-go/pull/1854).

```diff
import (
+	"go.etcd.io/etcd/clientv3"

	"google.golang.org/grpc"
+	"google.golang.org/grpc/codes"
+	"google.golang.org/grpc/status"
)

_, err := kvc.Get(ctx, "a")
-if err == grpc.ErrClientConnClosing {
+if clientv3.IsConnCanceled(err) {

// or
+s, ok := status.FromError(err)
+if ok {
+  if s.Code() == codes.Canceled
```

#### اشتراط `grpc.WithBlock` لاتصال العميل {#require-grpcwithblock-for-client-dial}

يستخدم [موازن الحمل الجديد في جانب العميل](/ar/etcd/learning/design-client/) محلِّلًا (resolver) غير متزامن لتمرير نقاط النهاية إلى دالة الاتصال (dial) في gRPC. نتيجة لذلك، يتطلب عميل v3.4 خيار الاتصال `grpc.WithBlock` للانتظار حتى يصبح الاتصال الأساسي جاهزًا.

```diff
import (
	"time"
	"go.etcd.io/etcd/clientv3"
+	"google.golang.org/grpc"
)

+// "grpc.WithBlock()" to block until the underlying connection is up
ccfg := clientv3.Config{
  Endpoints:            []string{"localhost:2379"},
  DialTimeout:          time.Second,
+ DialOptions:          []grpc.DialOption{grpc.WithBlock()},
  DialKeepAliveTime:    time.Second,
  DialKeepAliveTimeout: 500 * time.Millisecond,
}
```

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

ترفع v3.4 مقاييس Prometheus ‏`etcd_debugging_mvcc_db_total_size_in_bytes` إلى `etcd_mvcc_db_total_size_in_bytes`، لتشجيع مراقبة تخزين etcd.

لا يزال المقياس `etcd_debugging_mvcc_db_total_size_in_bytes` يُقدَّم في v3.4 لأجل التوافق مع الإصدارات الأقدم. وسيُهمل تمامًا في v3.5.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_put_total` {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

ترفع v3.4 مقاييس Prometheus ‏`etcd_debugging_mvcc_put_total` إلى `etcd_mvcc_put_total`، لتشجيع مراقبة تخزين etcd.

لا يزال المقياس `etcd_debugging_mvcc_put_total` يُقدَّم في v3.4 لأجل التوافق مع الإصدارات الأقدم. وسيُهمل تمامًا في v3.5.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_delete_total` {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

ترفع v3.4 مقاييس Prometheus ‏`etcd_debugging_mvcc_delete_total` إلى `etcd_mvcc_delete_total`، لتشجيع مراقبة تخزين etcd.

لا يزال المقياس `etcd_debugging_mvcc_delete_total` يُقدَّم في v3.4 لأجل التوافق مع الإصدارات الأقدم. وسيُهمل تمامًا في v3.5.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_txn_total` {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

ترفع v3.4 مقاييس Prometheus ‏`etcd_debugging_mvcc_txn_total` إلى `etcd_mvcc_txn_total`، لتشجيع مراقبة تخزين etcd.

لا يزال المقياس `etcd_debugging_mvcc_txn_total` يُقدَّم في v3.4 لأجل التوافق مع الإصدارات الأقدم. وسيُهمل تمامًا في v3.5.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_range_total` {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

ترفع v3.4 مقاييس Prometheus ‏`etcd_debugging_mvcc_range_total` إلى `etcd_mvcc_range_total`، لتشجيع مراقبة تخزين etcd.

لا يزال المقياس `etcd_debugging_mvcc_range_total` يُقدَّم في v3.4 لأجل التوافق مع الإصدارات الأقدم. وسيُهمل تمامًا في v3.5.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال العلامة `etcd --log-output` (أصبحت الآن `--log-outputs`) {#deprecating-etcd---log-output-flag-now---log-outputs}

أُعيدت تسمية [`etcd --log-output` إلى `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) لدعم مخارج سجلات متعددة. **لا يدعم `etcd --logger=capnslog` مخارج سجلات متعددة.**

ستُهمل **`etcd --log-output`** في v3.5. **سيُهمل `etcd --logger=capnslog` في v3.5**.

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

تضيف v3.4 دعم `etcd --logger=zap --log-outputs=stderr` للتسجيل المهيكل ولمخارج سجلات متعددة. الدافع الرئيسي هو تشجيع المراقبة الآلية لـ etcd بدلًا من الرجوع إلى سجلات الخادم عندما يبدأ بالتعطل. سيجعل التطوير المستقبلي etcd يسجل أقل قدر ممكن، ويسهّل مراقبة etcd بالمقاييس والتنبيهات. **سيُهمل `etcd --logger=capnslog` في v3.5**.

#### تغيير نوع حقل `log-outputs` في `etcd --config-file` إلى `[]string` {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

الآن بعد أن يقبل `log-outputs` (اسم الحقل القديم `log-output`) وجهات كتابة (writers) متعددة، يجب تغيير حقل `log-outputs` في ملف إعداد etcd بصيغة YAML إلى النوع `[]string` كما يلي:

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### إعادة تسمية `embed.Config.LogOutput` إلى `embed.Config.LogOutputs` {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

أُعيدت تسمية [**`embed.Config.LogOutput`** إلى **`embed.Config.LogOutputs`**](https://github.com/etcd-io/etcd/pull/9624) لدعم مخارج سجلات متعددة. وغُيِّر [نوع `embed.Config.LogOutput` من `string` إلى `[]string`](https://github.com/etcd-io/etcd/pull/9579) لدعم مخارج سجلات متعددة.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5 تهمل `capnslog` {#v35-deprecates-capnslog}

**ستهمل v3.5 العلامة `etcd --log-package-levels` الخاصة بـ `capnslog`**؛ وسيصبح `etcd --logger=zap --log-outputs=stderr` هو الافتراضي. **ستهمل v3.5 نقطة النهاية `[CLIENT-URL]/config/local/log`.**

```diff
-etcd
+etcd --logger zap
```

#### إهمال العلامة `etcd --debug` (أصبحت الآن `--log-level=debug`) {#deprecating-etcd---debug-flag-now---log-leveldebug}

تهمل v3.4 العلامة [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947). استخدم بدلًا منها العلامة `etcd --log-level=debug`.

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### إهمال الحقل `pkg/transport.TLSInfo.CAFile` {#deprecated-pkgtransporttlsinfocafile-field}

أُهمل الحقل `pkg/transport.TLSInfo.CAFile`.

```diff
import "github.com/coreos/etcd/pkg/transport"

tlsInfo := transport.TLSInfo{
    CertFile: "/tmp/test-certs/test.pem",
    KeyFile: "/tmp/test-certs/test-key.pem",
-   CAFile: "/tmp/test-certs/trusted-ca.pem",
+   TrustedCAFile: "/tmp/test-certs/trusted-ca.pem",
}
tlsConfig, err := tlsInfo.ClientConfig()
if err != nil {
    panic(err)
}
```

#### تغيير `embed.Config.SnapCount` إلى `embed.Config.SnapshotCount` {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

اتساقًا مع اسم العلامة `etcd --snapshot-count`، أعيدت تسمية الحقل `embed.Config.SnapCount` إلى `embed.Config.SnapshotCount`:

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### تغيير `etcdserver.ServerConfig.SnapCount` إلى `etcdserver.ServerConfig.SnapshotCount` {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

اتساقًا مع اسم العلامة `etcd --snapshot-count`، أعيدت تسمية الحقل `etcdserver.ServerConfig.SnapCount` إلى `etcdserver.ServerConfig.SnapshotCount`:

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### تغيير تواقيع الدوال في الحزمة `wal` {#changed-function-signature-in-package-wal}

غُيِّرت تواقيع دوال `wal` لدعم المسجِّل المهيكل.

```diff
import "github.com/coreos/etcd/wal"
+import "go.uber.org/zap"

+lg, _ = zap.NewProduction()

-wal.Open(dirpath, snap)
+wal.Open(lg, dirpath, snap)

-wal.OpenForRead(dirpath, snap)
+wal.OpenForRead(lg, dirpath, snap)

-wal.Repair(dirpath)
+wal.Repair(lg, dirpath)

-wal.Create(dirpath, metadata)
+wal.Create(lg, dirpath, metadata)
```

#### تغيير النوع `IntervalTree` في الحزمة `pkg/adt` {#changed-intervaltree-type-in-package-pkgadt}

أصبح `pkg/adt.IntervalTree` يُعرَّف الآن باعتباره `interface`.

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### إهمال `embed.Config.SetupLogging` {#deprecated-embedconfigsetuplogging}

أُزيل `embed.Config.SetupLogging` لمنع إعداد تسجيل خاطئ، وأصبح الإعداد يجري تلقائيًا الآن.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### تغيير نقاط نهاية HTTP لبوابة gRPC (استبدال `/v3beta` بـ `/v3`) {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

قبل

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

بعد

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

سيُعاد توجيه الطلبات إلى نقاط النهاية `/v3beta` إلى `/v3`، وستُزال `/v3beta` في إصدار 3.5.

#### إهمال وسوم صور الحاويات {#deprecated-container-image-tags}

أُهمل وسم `latest` ووسوم صور الإصدارات الثانوية:

```diff
-docker pull gcr.io/etcd-development/etcd:latest
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.1

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.2
```

### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى 3.4، يجب أن يكون العنقود قيد التشغيل بالإصدار 3.3 أو أحدث. إذا كان إصداره أقدم من 3.3، فيرجى [الترقية إلى 3.3](/ar/etcd/upgrades/upgrade_3_3/) قبل الترقية إلى 3.4.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للرجوع إلى إصدار أقدم](#downgrade) والعودة إلى إصدار etcd القائم. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط. أما بيانات v2، فراجع [إنشاء نسخة احتياطية من مخزن بيانات v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار 3.4. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

ملاحظة: إذا كان العنقود يحتوي على بيانات v3 فقط ولا يحتوي على أي بيانات v2، فلا يخضع لهذا القيد.

إذا كان العنقود يخدم مجموعة بيانات v2 أكبر من 50MB، فقد يستغرق كل عضو مرقًّى حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود القائم. تحقق من حجم لقطة حديثة لتقدير الحجم الإجمالي للبيانات. بعبارة أخرى، فالأسلم هو انتظار دقيقتين بين ترقية كل عضو.

أما بالنسبة لحجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، فقد يستغرق هذا الإجراء الذي يجري مرة واحدة وقتًا أطول. يمكن لمسؤولي عناقيد etcd الضخمة جدًا بهذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل الترقية، وسيكون من دواعي سرورنا تقديم النصائح حول الإجراء.

#### الرجوع إلى إصدار أقدم {#downgrade}

إذا رُقِّي جميع الأعضاء إلى v3.4، فسيُرقّى العنقود إلى v3.4، ويصبح الرجوع إلى إصدار أقدم من هذه الحالة المكتملة **غير ممكن**. أما إذا بقي أي عضو واحد بالإصدار v3.3، فيظل العنقود وعملياته في حالة «v3.3»، ومن الممكن من حالة العنقود المختلط هذه العودة إلى استخدام الملف الثنائي etcd v3.3 على جميع الأعضاء.

يرجى [تنزيل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لجعل الرجوع بالعنقود إلى إصدار أقدم ممكنًا حتى بعد اكتمال ترقيته.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.3 ثلاثي الأعضاء يعمل على جهاز محلي.

#### الخطوة 1: التحقق من متطلبات الترقية {#step-1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.3.x؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT
```

#### الخطوة 2: تنزيل النسخة الاحتياطية من اللقطة من القائد {#step-2-download-snapshot-backup-from-leader}

[نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتوفير مسار للرجوع إلى إصدار أقدم في حال حدوث أي مشكلات.

مضمون أن يكون قائد etcd هو من يملك أحدث بيانات التطبيق، لذا نزِّل اللقطة من القائد:

```bash
curl -sL http://localhost:2379/metrics | grep etcd_server_is_leader
<<COMMENT
# HELP etcd_server_is_leader Whether or not this member is a leader. 1 if is, 0 otherwise.
# TYPE etcd_server_is_leader gauge
etcd_server_is_leader 1
COMMENT

curl -sL http://localhost:22379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

curl -sL http://localhost:32379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":1526585787.148433,"caller":"snapshot/v3_snapshot.go:109","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":1526585787.1485257,"caller":"snapshot/v3_snapshot.go:120","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":1526585787.1519694,"caller":"snapshot/v3_snapshot.go:133","msg":"fetched snapshot","endpoint":"localhost:2379","took":0.003502721}
{"level":"info","ts":1526585787.1520295,"caller":"snapshot/v3_snapshot.go:142","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### الخطوة 3: إيقاف أحد خوادم etcd القائمة {#step-3-stop-one-existing-etcd-server}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```bash
10.237579 I | etcdserver: updating the cluster version from 3.0 to 3.3
10.238315 N | etcdserver/membership: updated the cluster version from 3.0 to 3.3
10.238451 I | etcdserver/api: enabled capabilities for version 3.3


^C21.192174 N | pkg/osutil: received interrupt signal, shutting down...
21.192459 I | etcdserver: 7339c4e5e833c029 starts leadership transfer from 7339c4e5e833c029 to 729934363faa4a24
21.192569 I | raft: 7339c4e5e833c029 [term 8] starts to transfer leadership to 729934363faa4a24
21.192619 I | raft: 7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log
WARNING: 2018/05/17 12:45:21 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 0  <nil>}
WARNING: 2018/05/17 12:45:21 grpc: addrConn.transportMonitor exits due to: grpc: the connection is closing
21.193589 I | raft: 7339c4e5e833c029 [term: 8] received a MsgVote message with higher term from 729934363faa4a24 [term: 9]
21.193626 I | raft: 7339c4e5e833c029 became follower at term 9
21.193651 I | raft: 7339c4e5e833c029 [logterm: 8, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 8, index: 9] at term 9
21.193675 I | raft: raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 9
21.194424 I | raft: raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 9
21.292898 I | etcdserver: 7339c4e5e833c029 finished leadership transfer from 7339c4e5e833c029 to 729934363faa4a24 (took 100.436391ms)
21.292975 I | rafthttp: stopping peer 729934363faa4a24...
21.293206 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 writer)
21.293225 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293437 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream Message writer)
21.293459 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293514 I | rafthttp: stopped HTTP pipelining with peer 729934363faa4a24
21.293590 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293610 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293680 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream Message reader)
21.293700 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream Message reader)
21.293711 I | rafthttp: stopped peer 729934363faa4a24
21.293720 I | rafthttp: stopping peer b548c2511513015...
21.293987 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 writer)
21.294063 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294467 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream Message writer)
21.294561 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294742 I | rafthttp: stopped HTTP pipelining with peer b548c2511513015
21.294867 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 reader)
21.294892 I | rafthttp: stopped streaming with peer b548c2511513015 (stream MsgApp v2 reader)
21.294990 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream Message reader)
21.295004 E | rafthttp: failed to read b548c2511513015 on stream Message (context canceled)
21.295013 I | rafthttp: peer b548c2511513015 became inactive
21.295024 I | rafthttp: stopped streaming with peer b548c2511513015 (stream Message reader)
21.295035 I | rafthttp: stopped peer b548c2511513015
```

#### الخطوة 4: إعادة تشغيل خادم etcd بالإعداد نفسه {#step-4-restart-the-etcd-server-with-same-configuration}

أعد تشغيل خادم etcd بالإعداد نفسه ولكن بالملف الثنائي etcd الجديد.

```diff
-etcd-old --name s1 \
+etcd-new --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
+ --initial-cluster-state new \
+ --logger zap \
+ --log-outputs stderr
```

سينشر إصدار etcd v3.4 الجديد معلوماته إلى العنقود. في هذه المرحلة، يظل العنقود يعمل ببروتوكول v3.3، وهو أدنى إصدار مشترك.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.4 الجديد:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

سيسجّل الأعضاء غير المرقّاة تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله.

هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.4:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### الخطوة 5: كرر *الخطوة 3* و*الخطوة 4* لبقية الأعضاء {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى 3.4:

العضو 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

العضو 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

العضو 3:

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
