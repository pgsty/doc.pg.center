---
title: خفض إصدار etcd من 3.5 إلى 3.4
weight: 6700
description: العمليات وقوائم التحقق والملاحظات المتعلقة بخفض إصدار etcd من 3.5 إلى 3.4
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_5.md"
---

في الحالة العامة، يمكن أن يتم خفض الإصدار من etcd 3.5 إلى 3.4 دون أي توقف عن الخدمة، وبأسلوب متدرج:

- واحدًا تلو الآخر، أوقف عمليات etcd 3.5 واستبدلها بعمليات etcd 3.4
- بعد بدء أي عمليات 3.4، لن تعود الميزات الجديدة في 3.5 متاحة للعنقود

قبل [بدء خفض الإصدار](#downgrade-procedure)، اقرأ بقية هذا الدليل استعدادًا لذلك.

### قوائم التحقق لخفض الإصدار {#downgrade-checklists}

> [!WARNING]
> إذا كانت المصادقة مفعلة على عنقودك، فلا يُدعم خفض الإصدار المتدرج من 3.5 لأن الإصدار 3.5 [يغيِّر تنسيق مدخلات WAL المتعلقة بالمصادقة](https://github.com/etcd-io/etcd/pull/11943). يمكنك اتباع [تعليمات المصادقة](/ar/etcd/op-guide/authentication/rbac/) لتعطيل المصادقة وحذف جميع المستخدمين أولًا.

أبرز التغييرات الكاسرة من 3.5 إلى 3.4:

#### الاختلافات في الخيارات {#difference-in-flags}

إذا كنت تستخدم أيًّا من الخيارات التالية في تهيئات 3.5، فاحرص على إزالتها أو إعادة تسميتها أو تغيير قيمتها الافتراضية عند خفض الإصدار إلى 3.4.

> [!NOTE]
> يستند هذا الفرق إلى الإصدارين 3.5.14 وv.3.4.33. وقد يختلف الفرق الفعلي تبعًا لإصدار التصحيح لديك، فتحقق أولًا باستخدام `diff <(etcd-3.5/bin/etcd -h | grep \\-\\-) <(etcd-3.4/bin/etcd -h | grep \\-\\-)`.

```diff
# flags not available in 3.4
-etcd --socket-reuse-port
-etcd --socket-reuse-address
-etcd --raft-read-timeout
-etcd --raft-write-timeout
-etcd --v2-deprecation
-etcd --client-cert-file
-etcd --client-key-file
-etcd --peer-client-cert-file
-etcd --peer-client-key-file
-etcd --self-signed-cert-validity
-etcd --enable-log-rotation --log-rotation-config-json=some.json
-etcd --experimental-enable-distributed-tracing --experimental-distributed-tracing-address='localhost:4317' --experimental-distributed-tracing-service-name='etcd' --experimental-distributed-tracing-instance-id='' --experimental-distributed-tracing-sampling-rate='0'
-etcd --experimental-compact-hash-check-enabled --experimental-compact-hash-check-time='1m'
-etcd --experimental-downgrade-check-time
-etcd --experimental-memory-mlock
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-stop-grpc-service-on-defrag

# same flag with different names
-etcd --backend-bbolt-freelist-type=map
+etcd --experimental-backend-bbolt-freelist-type=array

# same flag different defaults
-etcd --pre-vote=true
+etcd --pre-vote=false

-etcd --logger=zap
+etcd --logger=capnslog
```

#### `etcd --logger zap` {#etcd---logger-zap}

يكون الإعداد الافتراضي في 3.4 هو `--logger=capnslog` بينما يكون الإعداد الافتراضي في 3.5 هو `--logger=zap`.

إذا أردت الاستمرار في استخدام `zap`، فيجب تحديده صراحةً.

```diff
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

#### الاختلافات في مقاييس Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in 3.4
-etcd_debugging_mvcc_db_compaction_last
```

### قوائم التحقق لخفض إصدار الخادم {#server-downgrade-checklists}

#### متطلبات خفض الإصدار {#downgrade-requirements}

لضمان خفض إصدار متدرج وسلس، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

يجب أن يكون إصدار 3.4 الذي سيُخفَّض الإصدار إليه >= 3.4.32.

#### التحضير {#preparation}

قبل خفض إصدار etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة ما قبل الإنتاج قبل نشر خفض الإصدار إلى بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء خفض الإصدار، يمكن استخدام هذه النسخة الاحتياطية [للتراجع](#rollback) إلى إصدار etcd الحالي. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط. أما بيانات v2 فراجع [النسخ الاحتياطي لمخزن بيانات v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

قبل البدء، نزِّل أحدث إصدار من etcd 3.4، وتأكد من أن إصداره >= 3.4.32.

#### الإصدارات المختلطة {#mixed-versions}

أثناء خفض الإصدار، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. ويُعتبر أن العنقود خُفض إصداره بمجرد خفض إصدار أي من أعضائه إلى الإصدار 3.4. وداخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

ملاحظة: إذا كان العنقود يحتوي على بيانات v3 فقط ولا يحتوي على بيانات v2، فلا ينطبق عليه هذا القيد.

إذا كان العنقود يخدم مجموعة بيانات v2 يزيد حجمها عن 50MB، فقد يستغرق كل عضو مُخفَّض الإصدار حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود الحالي. تحقق من حجم لقطة حديثة لتقدير حجم البيانات الإجمالي. بعبارة أخرى، الأسلم هو الانتظار دقيقتين بين خفض إصدار كل عضو.

أما بالنسبة إلى حجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، فقد يستغرق هذا النوع من العمليات الذي يجري مرة واحدة وقتًا أطول. يمكن لمديري عناقيد etcd الكبيرة جدًا من هذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل خفض الإصدار، ويسعدنا تقديم النصائح حول الإجراء.

#### التراجع {#rollback}

إذا خُفض إصدار أي عضو إلى 3.4، فسيُخفض إصدار العنقود إلى 3.4، وستكون العمليات متوافقة مع "3.4". ستحتاج إلى اتباع تعليمات [ترقية etcd من 3.4 إلى 3.5](/ar/etcd/upgrades/upgrade_3_5/) للتراجع.

يرجى [تنزيل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتظل إمكانية التراجع عن خفض الإصدار متاحة حتى بعد خفض إصدار العنقود بالكامل.

### إجراءات خفض الإصدار {#downgrade-procedure}

يوضح هذا المثال كيفية خفض إصدار عنقود etcd 3.5 مكوَّن من 3 أعضاء يعمل على جهاز محلي.

#### الخطوة 1: التحقق من متطلبات خفض الإصدار {#step-1-check-downgrade-requirements}

هل العنقود سليم ويعمل بالإصدار 3.5.x؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT
```

#### الخطوة 2: تنزيل النسخة الاحتياطية من اللقطة من القائد {#step-2-download-snapshot-backup-from-leader}

[نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتوفير مسار للتراجع في حال حدوث أي مشكلات.

#### الخطوة 3: إيقاف أحد خوادم etcd القائمة {#step-3-stop-one-existing-etcd-server}

قبل إيقاف الخادم، تحقق مما إذا كان هو القائد

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |      true |      false |         2 |          9 |                  9 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

إذا كان الخادم الذي سيُوقف هو القائد، فيمكنك تفادي بعض فترة التوقف بنقل القيادة إلى خادم آخر عبر `move-leader` قبل إيقاف هذا الخادم.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |      true |      false |         3 |         11 |                 11 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

عند إيقاف كل عملية etcd، ستسجِّل بقية أعضاء العنقود أخطاءً متوقعة. هذا أمر طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```bash
{"level":"info","ts":"2024-05-14T20:25:47.051124Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"91bc3c398fb3c146 became leader at term 3"}
{"level":"info","ts":"2024-05-14T20:25:47.051139Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: 91bc3c398fb3c146 elected leader 91bc3c398fb3c146 at term 3"}

^C{"level":"warn","ts":"2024-05-14T20:27:09.094119Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.09427Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.095535Z","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"8211f1d0f64f3269","error":"failed to dial 8211f1d0f64f3269 on stream MsgApp v2 (peer 8211f1d0f64f3269 failed to find local node 91bc3c398fb3c146)"}
{"level":"warn","ts":"2024-05-14T20:27:09.43915Z","caller":"rafthttp/stream.go:223","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269"}
{"level":"warn","ts":"2024-05-14T20:27:11.085646Z","caller":"etcdserver/cluster_util.go:294","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:11.085718Z","caller":"etcdserver/cluster_util.go:158","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:13.557385Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"416.079µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### الخطوة 4: إعادة تشغيل خادم etcd بالتهيئة نفسها + `--next-cluster-version-compatible` {#step-4-restart-the-etcd-server-with-same-configuration----next-cluster-version-compatible}

أعد تشغيل خادم etcd بالتهيئة نفسها ولكن مع الملف التنفيذي الجديد لـ etcd ومع `--next-cluster-version-compatible`.

```diff
-etcd-3.5/bin --name s1 \
+etcd-3.4/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
  --next-cluster-version-compatible
```

سينشر etcd 3.4 الجديد معلوماته إلى العنقود. عند هذه النقطة، سيبدأ العنقود في العمل ببروتوكول 3.4، وهو أدنى إصدار مشترك.

```bash
> `{"level":"info","ts":"2024-05-13T21:05:43.981445Z","caller":"membership/cluster.go:561","msg":"set initial cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982188Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982312Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.0","from":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982376Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:44.000672Z","caller":"etcdserver/server.go:2152","msg":"published local member to cluster through raft","local-member-id":"8211f1d0f64f3269","local-member-attributes":"{Name:infra1 ClientURLs:[http://127.0.0.1:2379]}","request-path":"/0/members/8211f1d0f64f3269/attributes","cluster-id":"ef37ad9dc622a7c4","publish-timeout":"7s"}`

> `{"level":"info","ts":"2024-05-13T21:05:46.452631Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.5","from":"3.4"}`
```

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف التنفيذي الجديد لـ etcd 3.4:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

سيسجِّل الأعضاء غير المُخفَّض إصدارهم معلومات مثل ما يلي

```bash
{"level":"info","ts":"2024-05-13T21:05:46.450764Z","caller":"etcdserver/server.go:2633","msg":"updating cluster version using v2 API","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452419Z","caller":"membership/cluster.go:576","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452547Z","caller":"etcdserver/server.go:2652","msg":"cluster version is updated","cluster-version":"3.4"}
```

#### الخطوة 5: تكرار *الخطوة 3* و*الخطوة 4* لبقية الأعضاء {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

بعد خفض إصدار جميع الأعضاء، تحقق من حالة الصحة وإصدار العنقود:

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
