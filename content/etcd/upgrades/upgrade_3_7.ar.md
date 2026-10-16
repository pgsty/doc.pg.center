---
title: ترقية etcd من v3.6 إلى v3.7
weight: 6550
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من v3.6 إلى v3.7"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd v3.6 إلى v3.7 ترقية متدرجة دون أي توقف:

- واحدًا تلو الآخر، أوقف عمليات etcd v3.6 واستبدلها بعمليات etcd v3.7
- بعد تشغيل جميع عمليات v3.7، تصبح الميزات الجديدة في v3.7 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.

### قوائم التحقق من الترقية {#upgrade-checklists}

#### تحديث 3.6 {#update-36}

> [!IMPORTANT]
> قبل الترقية إلى 3.7، تأكد من تحديث جميع أعضاء 3.6 لديك إلى 3.6.11 أو أحدث. قد لا تكون إصدارات الترقيع 3.6 الأقدم متوافقة مع ترقية متدرجة إلى 3.7.

#### مخزن V2 {#v2-store}

أُزيل مخزن v2 بالكامل في v3.7. فقد اختفت جميعها: واجهة v2 HTTP ‏(`--enable-v2`)، ومحاكاة v2 فوق v3 ‏(`--experimental-enable-v2v3`)، وخدمة اكتشاف v2، والحزمة `client/v2`، وتحميل ملفات لقطات v2. راجع مراجع التغييرات الكاسرة في [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

إذا كنت ترقي من عنقود 3.6 فهذه العلامات غائبة أصلًا ولا يلزم أي إجراء. أما إذا كنت قادمًا من إصدار أقدم مع بيانات v2 مخصصة، فاتبع [دليل الترحيل من v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) قبل الترقية.

#### إعادة هيكلة Go {#go-refactoring}

يحتوي v3.7 على إعادة هيكلة داخلية كبيرة لا تؤثر على المرقّين العاديين، لكن من الجدير معرفتها عند ترقية تكاملات مخصصة:

- الانتقال من `gogo/protobuf` إلى الحزمة القياسية `google.golang.org/protobuf` (يُتابع في [#14533](https://github.com/etcd-io/etcd/issues/14533)).
- ترحيل مكتبتي التسجيل والوسوم `go-grpc-middleware` v1 المهملتين إلى دوال الاعتراض في v2 ([#20420](https://github.com/etcd-io/etcd/pull/20420)).
- حُدِّثت دوال الاعتراض في OpenTelemetry لـ gRPC إلى `otelgrpc` v0.61.0، مستبدلةً الدالتين المهملتين `UnaryServerInterceptor` و`StreamServerInterceptor` بـ `NewServerHandler` ([#20017](https://github.com/etcd-io/etcd/pull/20017)).

إذا كنت تضمّن etcd كمكتبة، أو تبني على واجهة `clientv3`، أو تعتمد على حزم داخلية، فراجع [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md) قبل الترقية.

### علامات أُزيلت {#flags-removed}

أُزيلت جميع العلامات `--experimental-*` المهملة في v3.7 ([#19959](https://github.com/etcd-io/etcd/pull/19959)). في v3.6 استُبدل كل منها إما بعلامة غير تجريبية بالاسم نفسه أو بإدخال في `--feature-gates`. إذا كانت أي منها لا تزال معينة لديك، فاستبدلها بما يقابلها في v3.6 **قبل** الترقية المتدرجة إلى v3.7، وإلا فسيفشل تشغيل عملية v3.7.

```diff
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-compact-hash-check-enabled
-etcd --experimental-compact-hash-check-time
-etcd --experimental-compaction-batch-limit
-etcd --experimental-compaction-sleep-interval
-etcd --experimental-corrupt-check-time
-etcd --experimental-distributed-tracing-address
-etcd --experimental-distributed-tracing-instance-id
-etcd --experimental-distributed-tracing-sampling-rate
-etcd --experimental-distributed-tracing-service-name
-etcd --experimental-downgrade-check-time
-etcd --experimental-enable-distributed-tracing
-etcd --experimental-enable-lease-checkpoint
-etcd --experimental-enable-lease-checkpoint-persist
-etcd --experimental-initial-corrupt-check
-etcd --experimental-memory-mlock
-etcd --experimental-peer-skip-client-san-verification
-etcd --experimental-snapshot-catchup-entries
-etcd --experimental-stop-grpc-service-on-defrag
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-warning-apply-duration
-etcd --experimental-warning-unary-request-duration
-etcd --experimental-watch-progress-notify-interval
```

راجع [دليل الترقية من v3.5 إلى v3.6](/ar/etcd/upgrades/upgrade_3_6/) للاطلاع على مطابقة كل علامة أزيلت بما يقابلها غير التجريبي أو إدخال `--feature-gates`.

### علامات أُضيفت {#flags-added}

لا شيء.

### علامات بقيم افتراضية جديدة {#flags-with-new-defaults}

لا شيء.

### قوائم التحقق من ترقية الخادم {#server-upgrade-checklists}

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى v3.7، يجب أن يكون العنقود قيد التشغيل بالإصدار v3.6.11 أو أحدث. إذا كان على إصدار ثانوي أقدم، فيرجى [الترقية إلى v3.6](/ar/etcd/upgrades/upgrade_3_6/) أولًا؛ إذ يدعم etcd ترقية إصدار ثانوي واحد فقط في كل مرة.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl endpoint health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للتراجع](#rollback) والعودة إلى إصدار etcd القائم.

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار v3.7. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### التراجع {#rollback}

قبل ترقية عنقود etcd لديك، يرجى إنشاء [نسخة احتياطية من اللقطة وتنزيلها](/ar/etcd/op-guide/maintenance/#snapshot-backup) لعنقود etcd. يمكن استخدام هذه اللقطة لاستعادة العنقود إلى حالته السابقة للترقية عند الحاجة. إذا واجه المستخدمون مشكلات أثناء الترقية، فعليهم أولًا تحديد السبب الجذري وحله. وإذا كان العنقود لا يزال في حالة إصدارات مختلطة، حيث بقي عضو واحد على الأقل على v3.6، فيمكنهم إما استبدال الملف الثنائي أو الصورة بإصدار v3.6 القديم أو استعادة العنقود مباشرة باستخدام اللقطة. في هذه الحالة المختلطة، يواصل العنقود العمل باعتباره عنقود v3.6، مما يسمح بالتراجع دون اتباع عملية رسمية للرجوع إلى إصدار أقدم.

ومع ذلك، بمجرد ترقية جميع الأعضاء إلى v3.7، يُعتبر العنقود مرقّى بالكامل، ولم يعد التراجع باستخدام الملفات الثنائية ممكنًا. في هذه الحالة، خيارا الاستعادة الوحيدان هما الاسترجاع من اللقطة المأخوذة قبل الترقية أو اتباع [دليل الرجوع إلى إصدار أقدم](/ar/etcd/downgrades/downgrading-etcd/) الرسمي في حال ساءت ترقيتك.

### إجراء الترقية {#upgrade-procedure}

يوضح هذا المثال كيفية ترقية عنقود etcd v3.6 ثلاثي الأعضاء يعمل على جهاز محلي. المخرجات أدناه من تشغيل حقيقي مقابل etcd v3.6.12 وetcd v3.7.0-rc.0 على مضيف واحد بثلاثة منافذ على واجهة الحلقة المحلية (loopback).

#### الخطوة 1: التحقق من متطلبات الترقية {#step-1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v3.6.11 أو أحدث؟

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 7.681459ms
localhost:22379 is healthy: successfully committed proposal: took = 7.691750ms
localhost:32379 is healthy: successfully committed proposal: took = 7.698000ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.12","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

#### الخطوة 2: تنزيل النسخة الاحتياطية من اللقطة من القائد {#step-2-download-snapshot-backup-from-leader}

[نزِّل النسخة الاحتياطية من اللقطة](/ar/etcd/op-guide/maintenance/#snapshot-backup) لتوفير مسار للرجوع إلى إصدار أقدم في حال حدوث أي مشكلات.

مضمون أن يكون قائد etcd هو من يملك أحدث بيانات التطبيق، لذا نزِّل اللقطة من القائد:

```bash
for p in 2379 22379 32379; do
  echo -n "localhost:$p leader="
  curl -sL http://localhost:$p/metrics | grep "^etcd_server_is_leader " | awk '{print $2}'
done
<<COMMENT
localhost:2379 leader=1
localhost:22379 leader=0
localhost:32379 leader=0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-06-02T07:01:41.863225+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-06-02T07:01:41.866451+0300","logger":"client","caller":"v3@v3.6.12/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-06-02T07:01:41.874080+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-06-02T07:01:41.877203+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"13.822583ms","etcd-version":"3.6.0"}
{"level":"info","ts":"2026-06-02T07:01:41.877303+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.6.0
COMMENT
```

#### الخطوة 3: إيقاف أحد خوادم etcd القائمة {#step-3-stop-one-existing-etcd-server}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا). سينقل القائد القيادة قبل الخروج:

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
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

سينشر إصدار etcd v3.7 الجديد معلوماته إلى العنقود. في هذه المرحلة، يظل العنقود يعمل ببروتوكول v3.6، وهو أدنى إصدار مشترك.

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.7 الجديد:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | LEADER | RAFT TERM |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  false |         3 |
| localhost:22379 | 729934363faa4a24 |     3.6.12 |           3.6.0 |   98 kB |  false |         3 |
| localhost:32379 |  b548c2511513015 |     3.6.12 |           3.6.0 |   98 kB |   true |         3 |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
COMMENT
```

سيسجّل الأعضاء غير المرقّاة والعضو المرقّى رسائل عن حالة الإصدارات المختلطة حتى تكتمل ترقية العنقود بأكمله. هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.7.

#### الخطوة 5: كرر *الخطوة 3* و*الخطوة 4* لبقية الأعضاء {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى v3.7:

> `{"level":"info","ts":"2026-06-02T07:02:36.054783+0300","caller":"etcdserver/server.go:2311","msg":"updating cluster version using v3 API","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059345+0300","caller":"membership/cluster.go:593","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059409+0300","caller":"etcdserver/server.go:2326","msg":"cluster version is updated","cluster-version":"3.7"}`

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 550.833µs
localhost:32379 is healthy: successfully committed proposal: took = 733.458µs
localhost:22379 is healthy: successfully committed proposal: took = 714.416µs
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
```
