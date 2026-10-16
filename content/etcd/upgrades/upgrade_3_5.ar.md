---
title: ترقية etcd من 3.4 إلى 3.5
weight: 6650
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من 3.4 إلى 3.5"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd 3.4 إلى 3.5 ترقية متدرجة دون أي توقف:
 - واحدًا تلو الآخر، أوقف عمليات etcd v3.4 واستبدلها بعمليات etcd v3.5
 - بعد تشغيل جميع عمليات v3.5، تصبح الميزات الجديدة في v3.5 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.



### قوائم التحقق من الترقية {#upgrade-checklists}

> [!WARNING]
> عند [الترحيل من v2 دون بيانات v3](https://github.com/etcd-io/etcd/issues/9480)، يُسبب خادم etcd v3.2+ حالة panic عندما يستعيد etcd من لقطات موجودة ولكن دون ملف v3 باسم `ETCD_DATA_DIR/member/snap/db`. يحدث هذا عندما يكون الخادم قد رُحِّل من v2 دون أي بيانات v3 سابقة. ويمنع هذا أيضًا الفقدان العرضي لبيانات v3 (مثلًا، قد يكون ملف `db` قد نُقل). يشترط etcd وجود بيانات v3 لإجراء عمليات الترحيل اللاحقة ضمن v3. لا تقم بالترقية إلى إصدارات v3 أحدث حتى يحتوي خادم v3.0 على بيانات v3.

> [!WARNING]
> إذا كان العنقود لديك يفعّل المصادقة، فالترقية المتدرجة من 3.4 أو إصدار أقدم غير مدعومة لأن 3.5 [تغيّر تنسيق إدخالات WAL المتعلقة بالمصادقة](https://github.com/etcd-io/etcd/pull/11943).

أبرز التغييرات الكاسرة في 3.5.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

رفعت v3.5 مقاييس Prometheus ‏`etcd_debugging_mvcc_db_total_size_in_bytes` إلى `etcd_mvcc_db_total_size_in_bytes`، لتشجيع مراقبة تخزين etcd. وتهمل v3.5 تمامًا المقياس `etcd_debugging_mvcc_db_total_size_in_bytes`.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_put_total` {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

رفعت v3.5 مقاييس Prometheus ‏`etcd_debugging_mvcc_put_total` إلى `etcd_mvcc_put_total`، لتشجيع مراقبة تخزين etcd. وتهمل v3.5 تمامًا المقياس `etcd_debugging_mvcc_put_total`.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_delete_total` {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

رفعت v3.5 مقاييس Prometheus ‏`etcd_debugging_mvcc_delete_total` إلى `etcd_mvcc_delete_total`، لتشجيع مراقبة تخزين etcd. وتهمل v3.5 تمامًا المقياس `etcd_debugging_mvcc_delete_total`.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_txn_total` {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

رفعت v3.5 مقاييس Prometheus ‏`etcd_debugging_mvcc_txn_total` إلى `etcd_mvcc_txn_total`، لتشجيع مراقبة تخزين etcd. وتهمل v3.5 تمامًا المقياس `etcd_debugging_mvcc_txn_total`.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال مقاييس Prometheus `etcd_debugging_mvcc_range_total` {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

رفعت v3.5 مقاييس Prometheus ‏`etcd_debugging_mvcc_range_total` إلى `etcd_mvcc_range_total`، لتشجيع مراقبة تخزين etcd. وتهمل v3.5 تمامًا المقياس `etcd_debugging_mvcc_range_total`.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

لاحظ أن مقاييس نطاق الأسماء `etcd_debugging_*` صُنِّفت تجريبية. ومع تحسيننا لدليل المراقبة، قد نرفع مزيدًا من المقاييس.

#### إهمال `etcd --logger capnslog` {#deprecated-etcd---logger-capnslog}

تستخدم v3.5 افتراضيًا `--logger=zap` لدعم مخارج سجلات متعددة والتسجيل المهيكل.

**أُهمل `etcd --logger=capnslog` في v3.5**، وأصبح `--logger=zap` هو الافتراضي الآن.

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

تضيف v3.4 دعم `etcd --logger=zap` للتسجيل المهيكل ولمخارج سجلات متعددة. الدافع الرئيسي هو تشجيع المراقبة الآلية لـ etcd بدلًا من الرجوع إلى سجلات الخادم عندما يبدأ بالتعطل. سيجعل التطوير المستقبلي etcd يسجل أقل قدر ممكن، ويسهّل مراقبة etcd بالمقاييس والتنبيهات. **سيُهمل `etcd --logger=capnslog` في v3.5.**

#### إهمال `etcd --log-output` {#deprecated-etcd---log-output}

أعادت v3.4 تسمية [`etcd --log-output` إلى `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) لدعم مخارج سجلات متعددة.

**أُهمل `etcd --log-output` في v3.5.**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### إهمال العلامة `etcd --debug` (أصبحت الآن `--log-level=debug`) {#deprecated-etcd---debug-flag-now---log-leveldebug}

**أُهملت العلامة `etcd --debug`.**

```diff
-etcd --debug
+etcd --log-level debug
```

#### إهمال `etcd --log-package-levels` {#deprecated-etcd---log-package-levels}

**أُهملت العلامة `etcd --log-package-levels` الخاصة بـ `capnslog`.**

الآن، أصبح **`etcd --logger=zap`** هو الافتراضي.

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### إهمال `[CLIENT-URL]/config/local/log` {#deprecated-client-urlconfiglocallog}

**نقطة النهاية `/config/local/log` قيد الإهمال في v3.5، وكذلك العلامة `etcd --log-package-levels`.**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### تغيير نقاط نهاية HTTP لبوابة gRPC (إهمال `/v3beta`) {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

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

أُزيلت `/v3beta` في إصدار 3.5.



### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى 3.5، يجب أن يكون العنقود قيد التشغيل بالإصدار 3.4 أو أحدث. إذا كان إصداره أقدم من 3.4، فيرجى [الترقية إلى 3.4](/ar/etcd/upgrades/upgrade_3_4/) قبل الترقية إلى 3.5.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للرجوع إلى إصدار أقدم](#downgrade) والعودة إلى إصدار etcd القائم. يرجى ملاحظة أن الأمر `snapshot` ينشئ نسخة احتياطية لبيانات v3 فقط. أما بيانات v2، فراجع [إنشاء نسخة احتياطية من مخزن بيانات v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار 3.5. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

ملاحظة: إذا كان العنقود يحتوي على بيانات v3 فقط ولا يحتوي على أي بيانات v2، فلا يخضع لهذا القيد.

إذا كان العنقود يخدم مجموعة بيانات v2 أكبر من 50MB، فقد يستغرق كل عضو مرقًّى حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود القائم. تحقق من حجم لقطة حديثة لتقدير الحجم الإجمالي للبيانات. بعبارة أخرى، فالأسلم هو انتظار دقيقتين بين ترقية كل عضو.

أما بالنسبة لحجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، فقد يستغرق هذا الإجراء الذي يجري مرة واحدة وقتًا أطول. يمكن لمسؤولي عناقيد etcd الضخمة جدًا بهذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل الترقية، وسيكون من دواعي سرورنا تقديم النصائح حول الإجراء.

#### الرجوع إلى إصدار أقدم {#downgrade}

إذا رُقِّي جميع الأعضاء إلى v3.5، فسيُرقّى العنقود إلى v3.5، ويصبح الرجوع إلى إصدار أقدم من هذه الحالة المكتملة **غير ممكن**. أما إذا بقي أي عضو واحد بالإصدار v3.4، فيظل العنقود وعملياته في حالة «v3.4»، ومن الممكن من حالة العنقود المختلط هذه العودة إلى استخدام الملف الثنائي etcd v3.4 على جميع الأعضاء.

يرجى [تنزيل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لجعل الرجوع بالعنقود إلى إصدار أقدم ممكنًا حتى بعد اكتمال ترقيته.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.4 ثلاثي الأعضاء يعمل على جهاز محلي.

#### الخطوة 1: التحقق من متطلبات الترقية {#step-1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.4.x؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
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
{"level":"info","ts":1526587281.2001143,"caller":"etcdserver/server.go:2249","msg":"updating cluster version","from":"3.0","to":"3.4"}
{"level":"info","ts":1526587281.2010646,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}
{"level":"info","ts":1526587281.2012327,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}
{"level":"info","ts":1526587281.2013083,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}



^C{"level":"info","ts":1526587299.0717514,"caller":"osutil/interrupt_unix.go:63","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":1526587299.0718873,"caller":"embed/etcd.go:285","msg":"closing etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
{"level":"info","ts":1526587299.0722554,"caller":"etcdserver/server.go:1341","msg":"leadership transfer starting","local-member-id":"7339c4e5e833c029","current-leader-member-id":"7339c4e5e833c029","transferee-member-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.0723994,"caller":"raft/raft.go:1107","msg":"7339c4e5e833c029 [term 3] starts to transfer leadership to 729934363faa4a24"}
{"level":"info","ts":1526587299.0724802,"caller":"raft/raft.go:1113","msg":"7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log"}
{"level":"info","ts":1526587299.0737045,"caller":"raft/raft.go:797","msg":"7339c4e5e833c029 [term: 3] received a MsgVote message with higher term from 729934363faa4a24 [term: 4]"}
{"level":"info","ts":1526587299.0737681,"caller":"raft/raft.go:656","msg":"7339c4e5e833c029 became follower at term 4"}
{"level":"info","ts":1526587299.073831,"caller":"raft/raft.go:882","msg":"7339c4e5e833c029 [logterm: 3, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 3, index: 9] at term 4"}
{"level":"info","ts":1526587299.0738947,"caller":"raft/node.go:312","msg":"raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 4"}
{"level":"info","ts":1526587299.0748374,"caller":"raft/node.go:306","msg":"raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 4"}
{"level":"info","ts":1526587299.1726425,"caller":"etcdserver/server.go:1362","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"729934363faa4a24","took":0.100389359}
{"level":"info","ts":1526587299.1728148,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1751974,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1752589,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.177348,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1774004,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.177515,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1777067,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34636->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1778402,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1780295,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34634->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1780987,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781602,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781986,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1802843,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1803446,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1824749,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.18255,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.18261,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1827736,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"read tcp 127.0.0.1:51482->127.0.0.1:22380: use of closed network connection"}
{"level":"info","ts":1526587299.182845,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1830168,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"context canceled"}
{"level":"warn","ts":1526587299.1831107,"caller":"rafthttp/peer_status.go:65","msg":"peer became inactive","peer-id":"729934363faa4a24","error":"failed to read 729934363faa4a24 on stream Message (context canceled)"}
{"level":"info","ts":1526587299.1831737,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.1832306,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1837125,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1840093,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1842315,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1844475,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"info","ts":1526587299.2056687,"caller":"embed/etcd.go:473","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.205819,"caller":"embed/etcd.go:480","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.2058413,"caller":"embed/etcd.go:289","msg":"closed etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
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
  --initial-cluster-state new
```

سينشر إصدار etcd v3.5 الجديد معلوماته إلى العنقود. في هذه المرحلة، يظل العنقود يعمل ببروتوكول v3.4، وهو أدنى إصدار مشترك.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.5 الجديد:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

سيسجّل الأعضاء غير المرقّاة تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله.

هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.5:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### الخطوة 5: كرر *الخطوة 3* و*الخطوة 4* لبقية الأعضاء {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى 3.5:

العضو 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

العضو 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

العضو 3:

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
