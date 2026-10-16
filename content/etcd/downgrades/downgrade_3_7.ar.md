---
title: خفض إصدار etcd من v3.7 إلى v3.6
weight: 6600
description: العمليات وقوائم التحقق والملاحظات المتعلقة بخفض إصدار etcd من v3.7 إلى v3.6
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
---

في الحالة العامة، يمكن أن يتم خفض الإصدار من etcd v3.7 إلى v3.6 دون أي توقف عن الخدمة، وبأسلوب متدرج:

- واحدًا تلو الآخر، أوقف عمليات etcd v3.7 واستبدلها بعمليات etcd v3.6
- بعد تمكين خفض الإصدار، لن تعود الميزات الجديدة في v3.7 متاحة للعنقود

قبل [بدء خفض الإصدار](#downgrade-procedure)، اقرأ بقية هذا الدليل استعدادًا لذلك.

### قوائم التحقق لخفض الإصدار {#downgrade-checklists}

أبرز الاختلافات بين v3.7 وv3.6:

#### الاختلافات في الخيارات {#difference-in-flags}

لا يقدم v3.7 أي خيارات جديدة، لذلك تقبل عملية v3.6 كل خيار من خيارات تهيئة v3.7 ولا حاجة إلى أي تغييرات في التهيئة عند خفض الإصدار.

> [!NOTE]
> يستند هذا الفرق إلى الإصدارين v3.7.0-rc.0 وv3.6.13. وقد يختلف الفرق الفعلي تبعًا لإصدار التصحيح لديك، فتحقق أولًا باستخدام `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`.

لا تزال الخيارات المهملة `--experimental-*` التي أزيلت في v3.7 موجودة في v3.6، لكن لا تعد إضافتها بعد خفض الإصدار؛ استخدم بدائلها غير التجريبية أو مدخلات `--feature-gates`، وهي تعمل على كلا الإصدارين.

#### الاختلافات في مقاييس Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### قوائم التحقق لخفض إصدار الخادم {#server-downgrade-checklists}

#### متطلبات خفض الإصدار {#downgrade-requirements}

لضمان خفض إصدار متدرج وسلس، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل خفض إصدار etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة ما قبل الإنتاج قبل نشر خفض الإصدار إلى بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء خفض الإصدار، يمكن استخدام هذه النسخة الاحتياطية [للتراجع](#rollback) إلى إصدار etcd الحالي.

قبل البدء، نزِّل أحدث إصدار من etcd v3.6.

#### الإصدارات المختلطة {#mixed-versions}

أثناء خفض الإصدار، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. ويُعتبر أن العنقود خُفض إصداره بمجرد تمكين خفض الإصدار عبر `etcdctl downgrade enable 3.6`. وداخليًا، يُضبط إصدار العنقود الكلي على الإصدار الهدف لخفض الإصدار، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### التراجع {#rollback}

قبل خفض إصدار عنقود etcd الخاص بك، يرجى إنشاء [نسخة احتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لعنقود etcd الخاص بك وتنزيلها. يمكن استخدام هذه اللقطة لاستعادة العنقود إلى حالته قبل خفض الإصدار إذا لزم الأمر. وإذا واجه المستخدمون مشكلات أثناء خفض الإصدار، فيجب عليهم أولًا تحديد السبب الجذري ومعالجته.

إذا كان خفض الإصدار قد بدأ بعد تشغيل `etcdctl downgrade enable`، وكان العنقود لا يزال في حالة إصدارات مختلطة، أي أن عضوًا واحدًا على الأقل لا يزال على v3.7، فيمكن للمستخدمين إلغاء عملية خفض الإصدار الجارية بتشغيل `etcdctl downgrade cancel` وإعادة تشغيل جميع الأعضاء المُخفَّض إصدارهم بالملفات التنفيذية الأصلية v3.7.

بمجرد خفض إصدار جميع الأعضاء إلى v3.6، يُعتبر أن العنقود خُفض إصداره بالكامل. وإذا رغب المستخدمون في العودة إلى الإصدار الأصلي بعد اكتمال خفض الإصدار الكامل، فعليهم اتباع [دليل الترقية](/ar/etcd/upgrades/upgrade_3_7/) الرسمي لضمان الاتساق وتجنب تلف البيانات.

### إجراءات خفض الإصدار {#downgrade-procedure}

يوضح هذا المثال كيفية خفض إصدار عنقود etcd v3.7 مكوَّن من 3 أعضاء يعمل على جهاز محلي. المخرجات أدناه مأخوذة من تشغيل حقيقي مقابل etcd v3.7.0-rc.0 وetcd v3.6.13 على مضيف واحد بثلاثة منافذ على واجهة الحلقة المحلية (loopback)، على عنقود تمت ترقيته من v3.6.13 قبل وقت قصير.

#### الخطوة 1: التحقق من متطلبات خفض الإصدار {#step-1-check-downgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.7.x؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### الخطوة 2: تنزيل النسخة الاحتياطية من اللقطة من القائد {#step-2-download-snapshot-backup-from-leader}

[نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتوفير مسار للتراجع في حال حدوث أي مشكلات:

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### الخطوة 3: التحقق من صلاحية الإصدار الهدف لخفض الإصدار {#step-3-validate-downgrade-target-version}

تحقق من صلاحية الإصدار الهدف لخفض الإصدار قبل تمكين خفض الإصدار:

- لا ندعم سوى خفض إصدار فرعي واحد في كل مرة. على سبيل المثال، لا يُسمح بخفض الإصدار من v3.7 إلى v3.5.
- يرجى عدم الانتقال إلى الخطوة التالية قبل نجاح التحقق.

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### الخطوة 4: تمكين خفض الإصدار {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

بعد تمكين خفض الإصدار، سيبدأ العنقود في العمل ببروتوكول v3.6، وهو الإصدار الهدف لخفض الإصدار. بالإضافة إلى ذلك، سينقل etcd المخطط تلقائيًا إلى الإصدار الهدف لخفض الإصدار، ويحدث ذلك عادةً بسرعة كبيرة. تأكد من ترحيل إصدار التخزين لجميع الخوادم إلى v3.6 بفحص حالة نقاط النهاية قبل الانتقال إلى الخطوة التالية.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> بمجرد تمكين خفض الإصدار، سيواصل العنقود العمل ببروتوكول v3.6 حتى لو كانت جميع الخوادم لا تزال تشغِّل الملف التنفيذي v3.7، ما لم يُلغَ خفض الإصدار باستخدام `etcdctl downgrade cancel`

#### الخطوة 5: إيقاف أحد خوادم etcd القائمة {#step-5-stop-one-existing-etcd-server}

قبل إيقاف الخادم، تحقق مما إذا كان هو القائد. نوصي بخفض إصدار القائد أخيرًا. إذا كان الخادم الذي سيُوقف هو القائد، فيمكنك تفادي بعض فترة التوقف بنقل القيادة إلى خادم آخر عبر `move-leader` قبل إيقاف هذا الخادم.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

عند إيقاف كل عملية etcd، ستسجِّل بقية أعضاء العنقود أخطاءً متوقعة. هذا أمر طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### الخطوة 6: إعادة تشغيل خادم etcd بالتهيئة نفسها {#step-6-restart-the-etcd-server-with-same-configuration}

أعد تشغيل خادم etcd بالتهيئة نفسها ولكن مع الملف التنفيذي لـ etcd v3.6.

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف التنفيذي لـ etcd v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> على خلاف v3.5، تُبلِّغ نقطة نهاية الحالة في v3.6 عن معلومات خفض الإصدار، لذلك يواصل الأعضاء المُخفَّض إصدارهم إظهار `DOWNGRADE ENABLED` بالقيمة true وإصدار تخزينهم حتى يكتمل خفض الإصدار.

#### الخطوة 7: تكرار *الخطوة 5* و*الخطوة 6* لبقية الأعضاء {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

بعد خفض إصدار جميع الأعضاء، يكتمل خفض الإصدار تلقائيًا وتُعاد `DOWNGRADE ENABLED` إلى false. تحقق من صحة العنقود وحالته، وأكِّد أن الإصدار الفرعي لجميع الأعضاء وإصدار التخزين هما v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

في سجل القائد، ينبغي أن ترى رسالة مشابهة لما يلي:

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
