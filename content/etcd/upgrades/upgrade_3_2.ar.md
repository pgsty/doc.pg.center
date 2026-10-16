---
title: ترقية etcd من 3.1 إلى 3.2
weight: 6800
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من 3.1 إلى 3.2"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd 3.1 إلى 3.2 ترقية متدرجة دون أي توقف:
 - واحدًا تلو الآخر، أوقف عمليات etcd v3.1 واستبدلها بعمليات etcd v3.2
 - بعد تشغيل جميع عمليات v3.2، تصبح الميزات الجديدة في v3.2 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.

### قوائم التحقق من الترقية {#upgrade-checklists}

> [!WARNING]
> عند [الترحيل من v2 دون بيانات v3](https://github.com/etcd-io/etcd/issues/9480)، يُسبب خادم etcd v3.2+ حالة panic عندما يستعيد etcd من لقطات موجودة ولكن دون ملف v3 باسم `ETCD_DATA_DIR/member/snap/db`. يحدث هذا عندما يكون الخادم قد رُحِّل من v2 دون أي بيانات v3 سابقة. ويمنع هذا أيضًا الفقدان العرضي لبيانات v3 (مثلًا، قد يكون ملف `db` قد نُقل). يشترط etcd وجود بيانات v3 لإجراء عمليات الترحيل اللاحقة ضمن v3. لا تقم بالترقية إلى إصدارات v3 أحدث حتى يحتوي خادم v3.0 على بيانات v3.

أبرز التغييرات الكاسرة في 3.2.

#### تغيير القيمة الافتراضية لـ `snapshot-count` {#changed-default-snapshot-count-value}

تحتفظ القيمة الأعلى لـ `--snapshot-count` بمزيد من إدخالات Raft في الذاكرة حتى اللقطة، مما يسبب [استخدامًا أعلى متكررًا للذاكرة](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). وبما أن القائد يحتفظ بأحدث إدخالات Raft لمدة أطول، فإن للتابع البطيء وقتًا أطول للّحاق قبل لقطة القائد. يمثل `--snapshot-count` مقايضة بين استخدام أعلى للذاكرة وتوافر أفضل للتوابع البطيئة.

منذ v3.2، [تغيّرت القيمة الافتراضية لـ `--snapshot-count` من 10,000 إلى 100,000](https://github.com/etcd-io/etcd/pull/7160).

#### تغيير تبعية gRPC (>=3.2.10) {#changed-grpc-dependency-3210}

يتطلب الإصدار 3.2.10 أو أحدث الآن [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) بالإصدار `v1.7.5` (الإصدارات <=3.2.9 تتطلب `v1.2.1`).

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

سابقًا، كان الخطأ `grpc.ErrClientConnTimeout` يُعاد عند انتهاء مهلة اتصال العميل. بدلًا من ذلك، يعيد 3.2 الخطأ `context.DeadlineExceeded` (راجع [#8504](https://github.com/etcd-io/etcd/issues/8504)).

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

#### تغيير حدود الحجم الأقصى للطلبات (>=3.2.10) {#changed-maximum-request-size-limits-3210}

يسمح الإصداران 3.2.10 و3.2.11 بحدود مخصصة لحجم الطلبات في جانب الخادم. وتسمح الإصدارات >=3.2.12 بحدود مخصصة لحجم الطلبات لكل من الخادم **وجانب العميل**. في الإصدارات السابقة (v3.2.10 وv3.2.11)، كان حجم استجابة العميل محدودًا بـ 4 MiB فقط.

يمكن تهيئة حدود الطلبات في جانب الخادم باستخدام الراية `--max-request-bytes`:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

أو قم بتهيئة الحقل `embed.Config.MaxRequestBytes`:

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

**إذا لم يُحدَّد، فإن الحد الافتراضي في جانب الخادم هو 1.5 MiB**.

يجب تهيئة حدود الطلبات في جانب العميل استنادًا إلى حدود جانب الخادم.

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

**إذا لم يُحدَّد، فإن حد الإرسال الافتراضي في جانب العميل هو 2 MiB (1.5 MiB + بايتات النفقات الإضافية لـ gRPC) وحد الاستلام هو `math.MaxInt32`**. يرجى مراجعة [clientv3 godoc](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) لمزيد من التفاصيل.

#### تغيير أغلفة عميل gRPC الخام {#changed-raw-grpc-client-wrappers}

يغيّر الإصدار 3.2.12 أو أحدث توقيعات دوال غلاف عميل gRPC الخاص بـ `clientv3`. كان هذا التغيير ضروريًا لدعم [خيارات `grpc.CallOption` المخصصة لحدود حجم الرسائل](https://github.com/etcd-io/etcd/pull/9047).

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

#### تغيير واجهة API الخاصة بـ `clientv3.Lease.TimeToLive` {#changed-clientv3leasetimetolive-api}

سابقًا، كانت واجهة API الخاصة بـ `clientv3.Lease.TimeToLive` تعيد `lease.ErrLeaseNotFound` عند معرّف عقد إيجار (lease) غير موجود. بدلًا من ذلك، يعيد 3.2 القيمة TTL=-1 في استجابته دون أي خطأ (راجع [#7305](https://github.com/etcd-io/etcd/pull/7305)).

قبل

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

بعد

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### نقل `clientv3.NewFromConfigFile` إلى `clientv3.yaml.NewConfig` {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

نُقل `clientv3.NewFromConfigFile` إلى `yaml.NewConfig`.

قبل

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

بعد

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### تغيير في `--listen-peer-urls` و`--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

يرفض 3.2 الآن أسماء النطاقات لـ `--listen-peer-urls` و`--listen-client-urls` (كان 3.1 يطبع تحذيرات فقط)، لأن اسم النطاق غير صالح لربط واجهة الشبكة. تأكد من أن هذه العناوين منسقة بشكل صحيح بالصيغة `scheme://IP:port`.

راجع [القضية #6336](https://github.com/etcd-io/etcd/issues/6336) لمزيد من السياقات.

### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى 3.2، يجب أن يكون العنقود قيد التشغيل بالإصدار 3.1 أو أحدث. إذا كان إصداره أقدم من 3.1، فيرجى [الترقية إلى 3.1](/ar/etcd/upgrades/upgrade_3_1) قبل الترقية إلى 3.2.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [أنشئ نسخة احتياطية من بيانات etcd](/ar/etcd/op-guide/maintenance#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للرجوع إلى إصدار أقدم](#downgrade) والعودة إلى إصدار etcd القائم. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط. أما بيانات v2، فراجع [إنشاء نسخة احتياطية من مخزن بيانات v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار 3.2. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

ملاحظة: إذا كان العنقود يحتوي على بيانات v3 فقط ولا يحتوي على أي بيانات v2، فلا يخضع لهذا القيد.

إذا كان العنقود يخدم مجموعة بيانات v2 أكبر من 50MB، فقد يستغرق كل عضو مرقًّى حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود القائم. تحقق من حجم لقطة حديثة لتقدير الحجم الإجمالي للبيانات. بعبارة أخرى، فالأسلم هو انتظار دقيقتين بين ترقية كل عضو.

لحجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، قد تستغرق هذه العملية التي تجري مرة واحدة وقتًا أطول. يمكن لمسؤولي عناقيد etcd الكبيرة جدًا بهذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل الترقية، ويسعدنا تقديم المشورة بشأن الإجراء.

#### الرجوع إلى إصدار أقدم {#downgrade}

إذا رُقِّي جميع الأعضاء إلى v3.2، فسيُرقّى العنقود إلى v3.2، ويصبح الرجوع إلى إصدار أقدم من هذه الحالة المكتملة **غير ممكن**. أما إذا بقي أي عضو واحد بالإصدار v3.1، فيظل العنقود وعملياته في حالة «v3.1»، ومن الممكن من حالة العنقود المختلط هذه العودة إلى استخدام الملف الثنائي etcd v3.1 على جميع الأعضاء.

يرجى [إنشاء نسخة احتياطية من دليل البيانات](/ar/etcd/op-guide/maintenance#snapshot-backup) لجميع أعضاء etcd لجعل الرجوع بالعنقود إلى إصدار أقدم ممكنًا حتى بعد اكتمال ترقيته.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.1 ثلاثي الأعضاء يعمل على جهاز محلي.

#### 1. تحقق من متطلبات الترقية {#1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.1.x؟

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. أوقف عملية etcd القائمة {#2-stop-the-existing-etcd-process}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```
2017-04-27 14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
2017-04-27 14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
2017-04-27 14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
2017-04-27 14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
2017-04-27 14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
2017-04-27 14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
2017-04-27 14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
2017-04-27 14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
2017-04-27 14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
2017-04-27 14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
2017-04-27 14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
2017-04-27 14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

من الجيد في هذه المرحلة [إنشاء نسخة احتياطية من بيانات etcd](/ar/etcd/op-guide/maintenance#snapshot-backup) لتوفير مسار للرجوع إلى إصدار أقدم في حال حدوث أي مشكلات:

```
$ etcdctl snapshot save backup.db
```

#### 3. ضع الملف الثنائي etcd v3.2 وابدأ عملية etcd الجديدة {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

سينشر إصدار etcd v3.2 الجديد معلوماته إلى العنقود:

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.2 الجديد:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

سيسجّل الأعضاء المرقّون تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله. هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.2:

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. كرر الخطوة 2 إلى الخطوة 3 لجميع الأعضاء الآخرين {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. الإنهاء {#5-finish}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى 3.2:

```
2017-04-27 14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.1 to 3.2
2017-04-27 14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.2
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
