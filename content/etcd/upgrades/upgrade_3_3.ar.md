---
title: ترقية etcd من 3.2 إلى 3.3
weight: 6750
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من 3.2 إلى 3.3"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd 3.2 إلى 3.3 ترقية متدرجة دون أي توقف:
 - واحدًا تلو الآخر، أوقف عمليات etcd v3.2 واستبدلها بعمليات etcd v3.3
 - بعد تشغيل جميع عمليات v3.3، تصبح الميزات الجديدة في v3.3 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.

### قوائم التحقق من الترقية {#upgrade-checklists}

> [!WARNING]
> عند [الترحيل من v2 دون بيانات v3](https://github.com/etcd-io/etcd/issues/9480)، يُسبب خادم etcd v3.2+ حالة panic عندما يستعيد etcd من لقطات موجودة ولكن دون ملف v3 باسم `ETCD_DATA_DIR/member/snap/db`. يحدث هذا عندما يكون الخادم قد رُحِّل من v2 دون أي بيانات v3 سابقة. ويمنع هذا أيضًا الفقدان العرضي لبيانات v3 (مثلًا، قد يكون ملف `db` قد نُقل). يشترط etcd وجود بيانات v3 لإجراء عمليات الترحيل اللاحقة ضمن v3. لا تقم بالترقية إلى إصدارات v3 أحدث حتى يحتوي خادم v3.0 على بيانات v3.

> [!WARNING]
> إذا فعّلت المصادقة واستخدمت عقود الإيجار (lease) (مع TTL صغير لعقد الإيجار)، فمن المرجح بشدة مواجهة [مشكلة](https://github.com/etcd-io/etcd/issues/11689) ستؤدي إلى عدم اتساق البيانات. يوصى بشدة بالترقية إلى 3.2.31+ أولًا لإصلاح هذه المشكلة، ثم الترقية إلى 3.3. بالإضافة إلى ذلك، إذا أرسل مستخدم دون صلاحية طلب `LeaseRevoke` إلى عقدة 3.3 أثناء عملية الترقية، فقد يظل ذلك يسبب تلف البيانات، لذا فالأفضل التأكد من عدم وجود مثل هذه الاستدعاءات الشاذة في بيئتك قبل الترقية، وراجع [#11691](https://github.com/etcd-io/etcd/pull/11691) للتفاصيل.


أبرز التغييرات الكاسرة في 3.3.

#### تغيير نوع قيمة العلامة `etcd --auto-compaction-retention` إلى `string` {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

غُيِّرت العلامة `--auto-compaction-retention` لتقبل [قيمًا نصية](https://github.com/etcd-io/etcd/pull/8563) مع [دقة زمنية أدق](https://github.com/etcd-io/etcd/issues/8503). الآن بعد أن تقبل `--auto-compaction-retention` قيمًا نصية، يجب تغيير حقل `auto-compaction-retention` في ملف إعداد etcd بصيغة YAML إلى النوع `string`. سابقًا، كان بإمكان `--config-file etcd.config.yaml` أن يحتوي على الحقل `auto-compaction-retention: 24`، أما الآن فيجب أن يكون `auto-compaction-retention: "24"` أو `auto-compaction-retention: "24h"`. إذا عُيِّن بالشكل `--auto-compaction-mode periodic --auto-compaction-retention "24h"`، فيجب أن تكون قيمة المدة الزمنية للعلامة `--auto-compaction-retention` صالحة للدالة [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration) في Go.

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### تغيير `*etcdserver.ServerConfig` إلى `etcdserver.ServerConfig` {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

غيّر `etcdserver.EtcdServer` نوع حقل العضو `*etcdserver.ServerConfig` إلى `etcdserver.ServerConfig`. وأصبح `etcdserver.NewServer` يستقبل الآن `etcdserver.ServerConfig` بدلًا من `*etcdserver.ServerConfig`.

قبل وبعد (مثلًا [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55))

```diff
import "github.com/coreos/etcd/etcdserver"

type EtcdServer struct {
	*etcdserver.EtcdServer
-	config *etcdserver.ServerConfig
+	config etcdserver.ServerConfig
}

func NewEtcd(dataDir string) *EtcdServer {
-	config := &etcdserver.ServerConfig{
+	config := etcdserver.ServerConfig{
		DataDir: dataDir,
        ...
	}
	return &EtcdServer{config: config}
}

func (e *EtcdServer) Start() error {
	var err error
	e.EtcdServer, err = etcdserver.NewServer(e.config)
    ...
```

#### إضافة حقل `embed.Config.LogOutput` {#added-embedconfiglogoutput-struct}

> [!WARNING]
> لاحظ أن هذا الحقل أعيدت تسميته إلى `embed.Config.LogOutputs` بالنوع `[]string` في v3.4. يرجى الاطلاع على [دليل الترقية إلى v3.4](/ar/etcd/upgrades/upgrade_3_4/) لمزيد من التفاصيل.

أُضيف الحقل `LogOutput` إلى `embed.Config`:

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

سابقًا، كانت تحذيرات خادم gRPC تُسجَّل في etcdserver.

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

ابتداءً من v3.3، تكون سجلات خادم gRPC معطلة افتراضيًا.

> [!WARNING]
> لاحظ أن الدالة `embed.Config.SetupLogging` أُهملت في v3.4. يرجى الاطلاع على [دليل الترقية إلى v3.4](/ar/etcd/upgrades/upgrade_3_4/) لمزيد من التفاصيل.

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

عيِّن الحقل `embed.Config.Debug` إلى `true` لتمكين سجلات خادم gRPC.

#### تغيير استجابة نقطة النهاية `/health` {#changed-health-endpoint-response}

سابقًا، كانت `[endpoint]:[client-port]/health` تعيد قيمة JSON جرى تسلسلها يدويًا. تحدد 3.3 الآن البنية [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health).

لاحظ أن `etcdhttp.Health` في v3.3.0-rc.0 وv3.3.0-rc.1 وv3.3.0-rc.2 يحتوي على الحقلين `"health"` و`"errors"` من النوع boolean. ولأجل التوافق مع الإصدارات الأقدم، أعدنا الحقل `"health"` إلى النوع `string` وأزلنا الحقل `"errors"`. وستُقدَّم معلومات الصحة الإضافية في واجهات API منفصلة.

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### تغيير نقاط نهاية HTTP لبوابة gRPC (استبدال `/v3alpha` بـ `/v3beta`) {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

قبل

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

بعد

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

سيُعاد توجيه الطلبات إلى نقاط النهاية `/v3alpha` إلى `/v3beta`، وستُزال `/v3alpha` في إصدار 3.4.

#### تغيير حدود الحجم الأقصى للطلبات {#changed-maximum-request-size-limits}

تسمح 3.3 الآن بحدود مخصصة لحجم الطلب لكل من الخادم و**جانب العميل**. في الإصدارات السابقة (v3.2.10 وv3.2.11)، كان حجم استجابة العميل محدودًا بـ 4 MiB فقط.

يمكن تهيئة حدود الطلبات في جانب الخادم باستخدام العلامة `--max-request-bytes`:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

أو تهيئة الحقل `embed.Config.MaxRequestBytes`:

```go
import "github.com/coreos/etcd/embed"
import "github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes"

// limit requests to 5 MiB
cfg := embed.NewConfig()
cfg.MaxRequestBytes = 5 * 1024 * 1024

// client writes exceeding 5 MiB will be rejected
_, err := cli.Put(ctx, "foo", [LARGE VALUE...])
err == rpctypes.ErrRequestTooLarge
```

**إذا لم يُحدَّد، فإن الحد في جانب الخادم يكون افتراضيًا 1.5 MiB**.

يجب تهيئة حدود الطلبات في جانب العميل بناءً على حدود جانب الخادم.

```bash
# limits request size to 1 MiB
etcd --max-request-bytes 1048576
```

```go
import "github.com/coreos/etcd/clientv3"

cli, _ := clientv3.New(clientv3.Config{
    Endpoints: []string{"127.0.0.1:2379"},
    MaxCallSendMsgSize: 2 * 1024 * 1024,
    MaxCallRecvMsgSize: 3 * 1024 * 1024,
})


// client writes exceeding "--max-request-bytes" will be rejected from etcd server
_, err := cli.Put(ctx, "foo", strings.Repeat("a", 1*1024*1024+5))
err == rpctypes.ErrRequestTooLarge


// client writes exceeding "MaxCallSendMsgSize" will be rejected from client-side
_, err = cli.Put(ctx, "foo", strings.Repeat("a", 5*1024*1024))
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: trying to send message larger than max (5242890 vs. 2097152)"


// some writes under limits
for i := range []int{0,1,2,3,4} {
    _, err = cli.Put(ctx, fmt.Sprintf("foo%d", i), strings.Repeat("a", 1*1024*1024-500))
    if err != nil {
        panic(err)
    }
}
// client reads exceeding "MaxCallRecvMsgSize" will be rejected from client-side
_, err = cli.Get(ctx, "foo", clientv3.WithPrefix())
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: received message larger than max (5240509 vs. 3145728)"
```

**إذا لم يُحدَّد، فإن حد الإرسال في جانب العميل يكون افتراضيًا 2 MiB (1.5 MiB + بايتات الحمل الإضافي لـ gRPC) وحد الاستلام هو `math.MaxInt32`**. يرجى الاطلاع على [توثيق clientv3 godoc](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) لمزيد من التفاصيل.

#### تغيير تواقيع دوال غلاف عميل gRPC الخام {#changed-raw-grpc-client-wrapper-function-signatures}

تتغيّر تواقيع دوال غلاف عميل gRPC في `clientv3` في الإصدار 3.3. كان هذا التغيير ضروريًا لدعم [`grpc.CallOption` مخصصة لحدود حجم الرسائل](https://github.com/etcd-io/etcd/pull/9047).

قبل وبعد

```diff
-func NewKVFromKVClient(remote pb.KVClient) KV {
+func NewKVFromKVClient(remote pb.KVClient, c *Client) KV {

-func NewClusterFromClusterClient(remote pb.ClusterClient) Cluster {
+func NewClusterFromClusterClient(remote pb.ClusterClient, c *Client) Cluster {

-func NewLeaseFromLeaseClient(remote pb.LeaseClient, keepAliveTimeout time.Duration) Lease {
+func NewLeaseFromLeaseClient(remote pb.LeaseClient, c *Client, keepAliveTimeout time.Duration) Lease {

-func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient) Maintenance {
+func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient, c *Client) Maintenance {

-func NewWatchFromWatchClient(wc pb.WatchClient) Watcher {
+func NewWatchFromWatchClient(wc pb.WatchClient, c *Client) Watcher {
```

#### تغيير نوع أخطاء واجهة `Snapshot` في clientv3 {#changed-clientv3-snapshot-api-error-type}

سابقًا، كانت واجهة `Snapshot` في clientv3 تعيد خطأً من النوع الخام [`grpc/*status.statusError`]. تترجم v3.3 الآن هذه الأخطاء إلى أنواع الأخطاء العامة المقابلة، اتساقًا مع بقية الواجهات.

قبل

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err.Error() == "rpc error: code = Canceled desc = context canceled"

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err.Error() == "rpc error: code = DeadlineExceeded desc = context deadline exceeded"
```

بعد

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err == context.Canceled

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err == context.DeadlineExceeded
```

#### تغيير مخرجات الأمر `etcdctl lease timetolive` {#changed-etcdctl-lease-timetolive-command-output}

سابقًا، كان الأمر `lease timetolive LEASE_ID` على عقد إيجار (lease) منتهٍ يطبع `-1s` للثواني المتبقية. تُخرج 3.3 الآن رسائل أوضح.

قبل


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

بعد

```bash
lease 2d8257079fa1bc0c already expired
```

#### تغيير استيرادات `golang.org/x/net/context` {#changed-golangorgxnetcontext-imports}

أهمل `clientv3` الحزمة `golang.org/x/net/context`. إذا كان مشروع ما يُدرج `golang.org/x/net/context` في كود آخر (مثل كود protocol buffer المولَّد من etcd) ويستورد `github.com/coreos/etcd/clientv3`، فإنه يتطلب Go 1.9+ للترجمة.

قبل

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

بعد

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### تغيير تبعية gRPC {#changed-grpc-dependency}

تتطلب 3.3 الآن [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) بالإصدار `v1.7.5`.

##### إهمال `grpclog.Logger` {#deprecated-grpcloglogger}

أُهمل `grpclog.Logger` لصالح [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). أصبح `clientv3.Logger` الآن `grpclog.LoggerV2`.

قبل

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

بعد

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### إهمال `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

سابقًا، كان الخطأ `grpc.ErrClientConnTimeout` يُعاد عند انتهاء مهلة اتصال العميل. تعيد 3.3 بدلًا من ذلك الخطأ `context.DeadlineExceeded` (راجع [#8504](https://github.com/etcd-io/etcd/issues/8504)).

قبل

```go
// expect dial time-out on ipv4 blackhole
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == grpc.ErrClientConnTimeout {
	// handle errors
}
```

بعد

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### تغيير مستودع الحاويات الرسمي {#changed-official-container-registry}

يستخدم etcd الآن [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) مستودعًا رئيسيًا للحاويات، و[`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) مستودعًا ثانويًا.

قبل

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

بعد

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### الترقيات إلى >= v3.3.14 {#upgrades-to--v3314}

كان لا بد أن يتضمن [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) بعض ميزات 3.4، مع محاولة تقليل الفروق بين تنفيذات موازن الحمل في جانب العميل. يصلح هذا الإصدار مشكلة ["رفض kube-apiserver 1.13.x العمل عندما يكون أول خادم etcd غير متاح" (kubernetes#72102)](https://github.com/kubernetes/kubernetes/issues/72102).

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

يستخدم [موازن الحمل الجديد في جانب العميل](/ar/etcd/learning/design-client/) محلِّلًا (resolver) غير متزامن لتمرير نقاط النهاية إلى دالة الاتصال (dial) في gRPC. نتيجة لذلك، يتطلب [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) أو أحدث خيار الاتصال `grpc.WithBlock` للانتظار حتى يصبح الاتصال الأساسي جاهزًا.

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

يرجى الاطلاع على [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) للحصول على القائمة الكاملة للتغييرات.

### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى 3.3، يجب أن يكون العنقود قيد التشغيل بالإصدار 3.2 أو أحدث. إذا كان إصداره أقدم من 3.2، فيرجى [الترقية إلى 3.2](/ar/etcd/upgrades/upgrade_3_2/) قبل الترقية إلى 3.3.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [أنشئ نسخة احتياطية من بيانات etcd](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للرجوع إلى إصدار أقدم](#downgrade) والعودة إلى إصدار etcd القائم. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط. أما بيانات v2، فراجع [إنشاء نسخة احتياطية من مخزن بيانات v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار 3.3. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

ملاحظة: إذا كان العنقود يحتوي على بيانات v3 فقط ولا يحتوي على أي بيانات v2، فلا يخضع لهذا القيد.

إذا كان العنقود يخدم مجموعة بيانات v2 أكبر من 50MB، فقد يستغرق كل عضو مرقًّى حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود القائم. تحقق من حجم لقطة حديثة لتقدير الحجم الإجمالي للبيانات. بعبارة أخرى، فالأسلم هو انتظار دقيقتين بين ترقية كل عضو.

أما بالنسبة لحجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، فقد يستغرق هذا الإجراء الذي يجري مرة واحدة وقتًا أطول. يمكن لمسؤولي عناقيد etcd الضخمة جدًا بهذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل الترقية، وسيكون من دواعي سرورنا تقديم النصائح حول الإجراء.

#### الرجوع إلى إصدار أقدم {#downgrade}

إذا رُقِّي جميع الأعضاء إلى v3.3، فسيُرقّى العنقود إلى v3.3، ويصبح الرجوع إلى إصدار أقدم من هذه الحالة المكتملة **غير ممكن**. أما إذا بقي أي عضو واحد بالإصدار v3.2، فيظل العنقود وعملياته في حالة «v3.2»، ومن الممكن من حالة العنقود المختلط هذه العودة إلى استخدام الملف الثنائي etcd v3.2 على جميع الأعضاء.

يرجى [إنشاء نسخة احتياطية من دليل البيانات](/ar/etcd/op-guide/maintenance/#snapshot-backup) لجميع أعضاء etcd لجعل الرجوع بالعنقود إلى إصدار أقدم ممكنًا حتى بعد اكتمال ترقيته.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.2 ثلاثي الأعضاء يعمل على جهاز محلي.

#### 1. التحقق من متطلبات الترقية {#1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.2.x؟

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. إيقاف عملية etcd القائمة {#2-stop-the-existing-etcd-process}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```
14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

من الجيد في هذه المرحلة [إنشاء نسخة احتياطية من بيانات etcd](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتوفير مسار للرجوع إلى إصدار أقدم في حال حدوث أي مشكلات:

```
$ etcdctl snapshot save backup.db
```

#### 3. تركيب الملف الثنائي etcd v3.3 وتشغيل عملية etcd الجديدة {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

سينشر إصدار etcd v3.3 الجديد معلوماته إلى العنقود:

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.3 الجديد:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

سيسجّل الأعضاء المرقّون تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله. هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.3:

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. كرر الخطوة 2 إلى الخطوة 3 لجميع الأعضاء الآخرين {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. الإنهاء {#5-finish}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى 3.3:

```
14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.2 to 3.3
14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.3
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
