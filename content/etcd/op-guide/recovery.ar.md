---
title: التعافي من الكوارث
weight: 4275
description: مرافق اللقطات والاستعادة في etcd v3
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/recovery.md"
---

صُمِّم etcd لتحمّل أعطال الأجهزة. يتعافى عنقود etcd تلقائيًا من الأعطال المؤقتة (مثل إعادة تشغيل الأجهزة) ويتحمّل حتى <bdi dir="ltr">*(N-1)/2*</bdi> من الأعطال الدائمة في عنقود مكوّن من N من الأعضاء. عندما يفشل عضو فشلًا دائمًا، سواء بسبب عطل في العتاد أو تلف في القرص، فإنه يفقد وصوله إلى العنقود. وإذا فقد العنقود بشكل دائم أكثر من <bdi dir="ltr">*(N-1)/2*</bdi> من الأعضاء، فإنه يفشل فشلًا كارثيًا، فاقدًا النصاب بصورة لا رجعة فيها. وبمجرد فقدان النصاب، لا يمكن للعنقود بلوغ إجماع، وبالتالي لا يمكنه مواصلة قبول التحديثات.

للتعافي من الفشل الكارثي، يوفّر etcd v3 مرافق اللقطات والاستعادة لإعادة إنشاء العنقود دون فقدان بيانات مفاتيح v3. لاستعادة مفاتيح v2، راجع [دليل الإدارة الخاص بـ v2][v2_recover].

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## أخذ لقطة لفضاء المفاتيح {#snapshotting-the-keyspace}

تتطلب استعادة عنقود أولًا لقطة لفضاء المفاتيح من أحد أعضاء etcd. يمكن أخذ اللقطة إما من عضو قيد التشغيل باستخدام الأمر `etcdctl snapshot save` أو بنسخ الملف `member/snap/db` من أحد أدلة بيانات etcd. على سبيل المثال، يأخذ الأمر التالي لقطة لفضاء المفاتيح الذي يخدّمه `$ENDPOINT` إلى الملف `snapshot.db`:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

لاحظ أن أخذ اللقطة من الملف `member/snap/db` قد يؤدي إلى فقدان بيانات لم تُكتب بعد، لكنها مضمّنة في مجلد wal (سجل الكتابة المسبقة).

## حالة اللقطة {#status-of-a-snapshot}

لفهم أيّ مراجعة وأيّ تجزئة (hash) تحتوي عليهما لقطة معيّنة، يمكنك استخدام الأمر `etcdutl snapshot status`:

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## استعادة عنقود {#restoring-a-cluster}

### فرق المراجعات {#revision-difference}

عند استعادة عنقود، قد يلاحظ العملاء الموجودون أن المراجعة عادت إلى الوراء بمئات أو آلاف. ويعود ذلك إلى حقيقة أن اللقطة المعيّنة لا تحتوي إلا على تسلسل البيانات حتى لحظة أخذها، في حين أن الحالة الحالية قد تكون قد تجاوزت ذلك بالفعل.

تشكّل هذه مشكلةً بشكل خاص عند تشغيل Kubernetes باستخدام etcd، حيث قد تستخدم وحدات التحكم (controllers) والمشغّلات (operators) ما يُعرف بـ `informers` التي تعمل كذاكرات تخزين مؤقت محلية وتتلقى إشعارات بالتحديثات عبر عمليات المراقبة (watches). وقد لا تؤدي الاستعادة إلى مراجعة أقدم إلى تحديث هذه الذاكرات المؤقتة بشكل صحيح، مما يتسبب في سلوك غير متوقع وغير متسق في وحدات التحكم.

عند الاستعادة من لقطة في سياق أي من الحالات التالية: مستهلكين معروفين لواجهة برمجة التطبيقات watch API، أو نسخ محلية مخزّنة مؤقتًا من بيانات etcd، أو عند استخدام Kubernetes بشكل عام - يوصى بشدة بالاستعادة باستخدام «زيادات المراجعة» (revision bumps) أدناه.

### الاستعادة من لقطة {#restoring-from-snapshot}

لاستعادة عنقود، كل ما هو مطلوب هو ملف «db» واحد خاص بلقطة. تعمل استعادة العنقود باستخدام `etcdutl snapshot restore` على إنشاء أدلة بيانات etcd جديدة؛ وينبغي أن يستعيد جميع الأعضاء باستخدام اللقطة نفسها. تكتب الاستعادة فوق بعض بيانات التعريف الخاصة باللقطة (تحديدًا، معرّف العضو ومعرّف العنقود)؛ فيفقد العضو هويته السابقة. تمنع إعادة كتابة بيانات التعريف هذه العضوَ الجديد من الانضمام دون قصد إلى عنقود قائم بالفعل. لذلك، لكي يبدأ عنقود من لقطة، يجب أن تُنشئ الاستعادة عنقودًا منطقيًا جديدًا.

يمكن تنفيذ استعادة بسيطة كما يلي:

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### فحوصات السلامة {#integrity-checks}

يمكن التحقق من سلامة اللقطة اختياريًا عند وقت الاستعادة. إذا أُخذت اللقطة باستخدام `etcdctl snapshot save`، فستحتوي على تجزئة سلامة يتحقق منها `etcdutl snapshot restore`. أما إذا نُسخت اللقطة من دليل البيانات، فلا توجد تجزئة سلامة، ولن تكون الاستعادة ممكنة إلا باستخدام `--skip-hash-check`.


### الاستعادة مع زيادة المراجعة {#restoring-with-revision-bump}

من أجل ضمان عدم تناقص المراجعات أبدًا بعد الاستعادة، يمكنك تقديم الخيار `--bump-revision`. يأخذ هذا الخيار عددًا صحيحًا بحجم 64 بت يدل على عدد المراجعات التي ستُضاف إلى المراجعة الحالية للقطة. وبما أن كل عملية كتابة في etcd تزيد المراجعة بمقدار واحد، فيمكنك تغطية لقطة عمرها أسبوع بزيادة قدرها 1'000'000'000 بافتراض أن etcd يعمل بأقل من 1500 كتابة في الثانية.

في سياق وحدات التحكم في Kubernetes، من المهم أيضًا وضع علامة على جميع المراجعات، بما في ذلك الزيادة، بوصفها مضغوطة باستخدام `--mark-compacted`. يضمن ذلك إنهاء جميع عمليات المراقبة (watches) وألّا يستجيب etcd للطلبات المتعلقة بالمراجعات التي حدثت بعد أخذ اللقطة — مما يُبطل عمليًا ذاكرات informer المؤقتة.

قد يبدو الاستدعاء الكامل كما يلي:

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### الاستعادة بتحديث العضوية {#restoring-with-updated-membership}

تُخزَّن عضوية عنقود etcd في etcd نفسه وتُصان من خلال خوارزمية إجماع raft. عند فقدان النصاب بالكامل، قد ترغب في إعادة النظر في مكان تشكيل العنقود الجديد وكيفية تشكيله، مثلًا على مجموعة جديدة تمامًا من الأعضاء.

عند الاستعادة من لقطة، يمكنك تقديم العضوية الجديدة مباشرة إلى مخزن البيانات كما يلي:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

يضمن ذلك أن العنقود المشكَّل حديثًا يتصل فقط بالأعضاء الآخرين المستعادين ذوي الرمز المعطى، وليس بالأعضاء الأقدم الذين قد لا يزالون نشطين ويحاولون الاتصال.

بدلًا من ذلك، عند تشغيل etcd، يمكنك تقديم `--force-new-cluster` للكتابة فوق عضوية العنقود مع الاحتفاظ ببيانات التطبيق الموجودة. لاحظ أن يُنصح بشدة بتجنب ذلك لأنه سيتسبب في حدوث panic إذا ظل أعضاء آخرون من العنقود السابق نشطين. احرص على حفظ اللقطات بشكل دوري.


### مثال من البداية إلى النهاية {#end-2-end-example}

خذ لقطة من عنقود قيد التشغيل باستخدام:

```sh
$ etcdctl snapshot save snapshot.db
```

استكمالًا للمثال السابق، ينشئ ما يلي أدلة بيانات etcd جديدة (`m1.etcd`، `m2.etcd`، `m3.etcd`) لعنقود مكوّن من ثلاثة أعضاء:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

بعد ذلك، شغّل `etcd` بأدلة البيانات الجديدة:

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

يجب أن يكون عنقود etcd المستعاد متاحًا الآن ويخدّم فضاء المفاتيح من اللقطة.

بدءًا من etcd v3.6، لا يمكن للمستخدمين استخدام `etcdctl` إلا لأخذ البيانات إلى لقطة، بينما يستخدمون `etcdutl` لاستعادة البيانات من لقطة. إذا لم يُحدَّد `--data-dir`، فإن القيمة الافتراضية لـ `--data-dir` هي `<name>.etcd` (حيث `<name>` هي القيمة المأخوذة من `--name`). على سبيل المثال، إذا لم يُقدَّم `--data-dir` وكان الأعضاء يحملون الأسماء `m1` و`m2` و`m3`، فستكون أدلة `--data-dir` هي `m1.etcd` و`m2.etcd` و`m3.etcd`.
