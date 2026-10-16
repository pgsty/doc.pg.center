---
title: ترقية etcd من v3.5 إلى v3.6
weight: 6600
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من v3.5 إلى v3.6"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd v3.5 إلى v3.6 ترقية متدرجة دون أي توقف:

- واحدًا تلو الآخر، أوقف عمليات etcd v3.5 واستبدلها بعمليات etcd v3.6
- بعد تشغيل جميع عمليات v3.6، تصبح الميزات الجديدة في v3.6 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.

### قوائم التحقق من الترقية {#upgrade-checklists}

#### تحديث 3.5 {#update-35}

> [!IMPORTANT]
> قبل الترقية إلى 3.6، تأكد من [تحديث جميع أعضاء 3.5 لديك إلى 3.5.32 أو أحدث](https://etcd.io/blog/2026/july-patch-release/). تصلح إصدارات الترقيع 3.5.24 حتى 3.5.26 عدة عوائق محتملة للترقية؛ ويضيف [3.5.32](https://etcd.io/blog/2026/july-patch-release/) العلامة `--v2-deprecation=write-only-skip-check` ويوسّع `etcdutl check v2store` لفحص سجلات WAL إضافة إلى لقطة v2.

#### مخزن V2 {#v2-store}

> [!NOTE]
> إذا لم تُهيَّأ العلامة `--enable-v2` أو كانت معينة إلى false، فلا يلزم اتخاذ أي إجراء إضافي.

أما إذا كانت العلامة `--enable-v2` **مهيأة**، فشغّل الأمر `etcdutl check v2store` للتحقق مما إذا كان مخزن v2store يحتوي على أي بيانات (مخصصة) غير متعلقة بالعضوية. إذا لم توجد بيانات مخصصة، يمكن إزالة العلامة بأمان. وإلا، فراجع [دليل الترحيل من v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) لمزيد من التفاصيل.

### علامات أُضيفت {#flags-added}

```diff
+etcd --discovery-token ''
+etcd --discovery-endpoints ''
+etcd --discovery-dial-timeout '2s'
+etcd --discovery-request-timeout '5s'
+etcd --discovery-keepalive-time '2s'
+etcd --discovery-keepalive-timeout '6s'
+etcd --discovery-insecure-transport 'true'
+etcd --discovery-insecure-skip-tls-verify 'false'
+etcd --discovery-cert ''
+etcd --discovery-key ''
+etcd --discovery-cacert ''
+etcd --discovery-user ''
+etcd --discovery-password ''
+etcd --feature-gates
+etcd --log-format
```

### علامات أُزيلت {#flags-removed}

```diff
-etcd --enable-v2
-etcd --experimental-enable-v2v3
-etcd --proxy
-etcd --proxy-failure-wait
-etcd --proxy-refresh-interval
-etcd --proxy-dial-timeout
-etcd --proxy-write-timeout
-etcd --proxy-read-timeout
```

### علامات أُهملت {#flags-deprecated}

**أُهملت العلامة `etcd --experimental-bootstrap-defrag-threshold-megabytes`.**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**أُهملت العلامة `etcd --experimental-compaction-batch-limit`.**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**أُهملت العلامة `etcd --experimental-compact-hash-check-time`.**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**أُهملت العلامة `etcd --experimental-compaction-sleep-interval`.**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**أُهملت العلامة `etcd --experimental-corrupt-check-time`.**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**أُهملت العلامة `etcd --experimental-enable-distributed-tracing`.**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**أُهملت العلامة `etcd --experimental-distributed-tracing-address`.**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**أُهملت العلامة `etcd --experimental-distributed-tracing-instance-id`.**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**أُهملت العلامة `etcd --experimental-distributed-tracing-sampling-rate`.**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**أُهملت العلامة `etcd --experimental-distributed-tracing-service-name`.**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**أُهملت العلامة `etcd --experimental-downgrade-check-time`.**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**أُهملت العلامة `etcd --experimental-max-learners`.**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**أُهملت العلامة `etcd --experimental-memory-mlock`.**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**أُهملت العلامة `etcd --experimental-peer-skip-client-san-verification`.**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**أُهملت العلامة `etcd --experimental-snapshot-catchup-entries`.**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**أُهملت العلامة `etcd --experimental-warning-apply-duration`.**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**أُهملت العلامة `etcd --experimental-warning-unary-request-duration`.**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**أُهملت العلامة `etcd --experimental-watch-progress-notify-interval`.**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### ترحيل العلامات التجريبية لـ v3.5 إلى بوابات الميزات {#equivalent-flags-of-v35-feature-gates}

**بوابة الميزة المقابلة للعلامة `etcd --experimental-compact-hash-check-enabled=true`**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**بوابة الميزة المقابلة للعلامة `etcd --experimental-initial-corrupt-check=true`**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**بوابة الميزة المقابلة للعلامة `etcd --experimental-enable-lease-checkpoint=true`**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**بوابة الميزة المقابلة للعلامة `etcd --experimental-enable-lease-checkpoint-persist=true`**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**بوابة الميزة المقابلة للعلامة `etcd --experimental-stop-grpc-service-on-defrag=true`**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**بوابة الميزة المقابلة للعلامة `etcd --experimental-txn-mode-write-with-shared-buffer=false`**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### علامات بقيم افتراضية جديدة {#flags-with-new-defaults}

**القيمة الافتراضية الأصلية للعلامة `etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**القيمة الافتراضية الأصلية للعلامة `etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**القيمة الافتراضية الأصلية للعلامة `etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### الفرق في مقاييس Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى v3.6، يجب أن يكون العنقود قيد التشغيل بالإصدار v3.5 أو أحدث. إذا كان إصداره أقدم من v3.5، فيرجى [الترقية إلى v3.5](/ar/etcd/upgrades/upgrade_3_5/) قبل الترقية إلى v3.6.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للتراجع](#rollback) والعودة إلى إصدار etcd القائم. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط.

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار v3.6. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### التراجع {#rollback}

قبل ترقية عنقود etcd لديك، يرجى إنشاء [نسخة احتياطية من اللقطة وتنزيلها](/ar/etcd/op-guide/maintenance/#snapshot-backup) لعنقود etcd. يمكن استخدام هذه اللقطة لاستعادة العنقود إلى حالته السابقة للترقية عند الحاجة. إذا واجه المستخدمون مشكلات أثناء الترقية، فعليهم أولًا تحديد السبب الجذري وحله. وإذا كان العنقود لا يزال في حالة إصدارات مختلطة — حيث بقي عضو واحد على الأقل على v3.5 — فيمكنهم إما استبدال الملف الثنائي أو الصورة بإصدار v3.5 القديم أو استعادة العنقود مباشرة باستخدام اللقطة. في هذه الحالة المختلطة، يواصل العنقود العمل باعتباره عنقود v3.5، مما يسمح بالتراجع دون اتباع عملية رسمية للرجوع إلى إصدار أقدم.

ومع ذلك، بمجرد ترقية جميع الأعضاء إلى v3.6، يُعتبر العنقود مرقّى بالكامل، ولا يعد مجرد استبدال الملفات الثنائية تراجعًا صحيحًا. خيارات الاستعادة هي الاسترجاع من اللقطة المأخوذة قبل الترقية أو اتباع دليل الرجوع الرسمي إلى الإصدار الأقدم للعودة إلى الإصدار الأصلي مع ضمان الاتساق وتجنب تلف البيانات.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.5 ثلاثي الأعضاء يعمل على جهاز محلي.

#### الخطوة 1: التحقق من متطلبات الترقية {#step-1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.5.x؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.555774ms
localhost:32379 is healthy: successfully committed proposal: took = 2.631133ms
localhost:22379 is healthy: successfully committed proposal: took = 3.020958ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
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
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### الخطوة 3: إيقاف أحد خوادم etcd القائمة {#step-3-stop-one-existing-etcd-server}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```bash
{"level":"info","ts":"2025-03-01T04:31:50.654520+0530","caller":"etcdserver/server.go:2676","msg":"cluster version is updated","cluster-version":"3.5"}
{"level":"info","ts":"2025-03-01T04:34:10.345927+0530","caller":"v3rpc/maintenance.go:130","msg":"sending database snapshot to client","total-bytes":20480,"size":"20 kB"}
{"level":"info","ts":"2025-03-01T04:34:10.346094+0530","caller":"v3rpc/maintenance.go:170","msg":"sending database sha256 checksum to client","total-bytes":20480,"checksum-size":32}
{"level":"info","ts":"2025-03-01T04:34:10.346108+0530","caller":"v3rpc/maintenance.go:179","msg":"successfully sent database snapshot to client","total-bytes":20480,"size":"20 kB","took":"now"}
^C
{"level":"info","ts":"2025-03-01T04:35:01.443045+0530","caller":"osutil/interrupt_unix.go:64","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":"2025-03-01T04:35:01.443088+0530","caller":"embed/etcd.go:408","msg":"closing etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
{"level":"info","ts":"2025-03-01T04:35:01.443417+0530","caller":"etcdserver/server.go:1503","msg":"leadership transfer starting","local-member-id":"bf9071f4639c75cc","current-leader-member-id":"bf9071f4639c75cc","transferee-member-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443441+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term 2] starts to transfer leadership to 91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443455+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc sends MsgTimeoutNow to 91bc3c398fb3c146 immediately as 91bc3c398fb3c146 already has up-to-date log"}
{"level":"warn","ts":"2025-03-01T04:35:01.443517+0530","caller":"embed/serve.go:179","msg":"stopping insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"warn","ts":"2025-03-01T04:35:01.443548+0530","caller":"embed/serve.go:181","msg":"stopped insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"info","ts":"2025-03-01T04:35:01.445536+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term: 2] received a MsgVote message with higher term from 91bc3c398fb3c146 [term: 3]"}
{"level":"info","ts":"2025-03-01T04:35:01.445556+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc became follower at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445565+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [logterm: 2, index: 12, vote: 0] cast MsgVote for 91bc3c398fb3c146 [logterm: 2, index: 12] at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445572+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc lost leader bf9071f4639c75cc at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.446773+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc elected leader 91bc3c398fb3c146 at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.544062+0530","caller":"etcdserver/server.go:1520","msg":"leadership transfer finished","local-member-id":"bf9071f4639c75cc","old-leader-member-id":"bf9071f4639c75cc","new-leader-member-id":"91bc3c398fb3c146","took":"100.640374ms"}
{"level":"info","ts":"2025-03-01T04:35:01.544160+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.544956+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.544984+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545050+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545065+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545099+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545156+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545178+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"91bc3c398fb3c146","error":"failed to read 91bc3c398fb3c146 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545199+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545246+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545263+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545272+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545282+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545307+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545328+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545359+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545379+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545410+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545467+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545485+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"fd422379fda50e48","error":"failed to read fd422379fda50e48 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545504+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545560+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545577+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545592+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545669+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545698+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545732+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545765+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"info","ts":"2025-03-01T04:35:01.549658+0530","caller":"embed/etcd.go:613","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550532+0530","caller":"embed/etcd.go:618","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550561+0530","caller":"embed/etcd.go:410","msg":"closed etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
```

#### الخطوة 4: إعادة تشغيل خادم etcd بالإعداد نفسه {#step-4-restart-the-etcd-server-with-same-configuration}

أعد تشغيل خادم etcd بالإعداد نفسه ولكن بالملف الثنائي etcd الجديد.

```diff
-etcd-old --name ${name} \
+etcd-new --name ${name} \
  --data-dir /path/to/${name}.etcd \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

سينشر إصدار etcd v3.6 الجديد معلوماته إلى العنقود. في هذه المرحلة، يظل العنقود يعمل ببروتوكول v3.5، وهو أدنى إصدار مشترك.

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.6 الجديد:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

سيسجّل الأعضاء غير المرقّاة تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله.

هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.6:

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### الخطوة 5: كرر *الخطوة 3* و*الخطوة 4* لبقية الأعضاء {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى v3.6:

العضو 1:

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

العضو 2:

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

العضو 3:

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"fd422379fda50e48","from":"3.5","to":"3.6"}`

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT
```
