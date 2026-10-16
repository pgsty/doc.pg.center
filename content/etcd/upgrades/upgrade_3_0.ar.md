---
title: ترقية etcd من 2.3 إلى 3.0
weight: 6900
description: "العمليات وقوائم التحقق والملاحظات المتعلقة بترقية etcd من 2.3 إلى 3.0"
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

في الحالة العامة، يمكن أن تكون الترقية من etcd 2.3 إلى 3.0 ترقية متدرجة دون أي توقف:
 - واحدًا تلو الآخر، أوقف عمليات etcd v2.3 واستبدلها بعمليات etcd v3.0
 - بعد تشغيل جميع عمليات v3.0، تصبح الميزات الجديدة في v3.0 متاحة للعنقود

قبل [بدء الترقية](#upgrade-procedure)، اقرأ بقية هذا الدليل للتحضير.

### قوائم التحقق من الترقية {#upgrade-checklists}

> [!WARNING]
> عند [الترحيل من v2 دون بيانات v3](https://github.com/etcd-io/etcd/issues/9480)، يُسبب خادم etcd v3.2+ حالة panic عندما يستعيد etcd من لقطات موجودة ولكن دون ملف v3 باسم `ETCD_DATA_DIR/member/snap/db`. يحدث هذا عندما يكون الخادم قد رُحِّل من v2 دون أي بيانات v3 سابقة. ويمنع هذا أيضًا الفقدان العرضي لبيانات v3 (مثلًا، قد يكون ملف `db` قد نُقل). يشترط etcd وجود بيانات v3 لإجراء عمليات الترحيل اللاحقة ضمن v3. لا تقم بالترقية إلى إصدارات v3 أحدث حتى يحتوي خادم v3.0 على بيانات v3.

#### متطلبات الترقية {#upgrade-requirements}

لترقية نشر etcd قائم إلى 3.0، يجب أن يكون العنقود قيد التشغيل بالإصدار 2.3 أو أحدث. إذا كان إصداره أقدم من 2.3، فيرجى الترقية إلى [2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8) قبل الترقية إلى 3.0.

أيضًا، ولضمان ترقية متدرجة سلسة، يجب أن يكون العنقود قيد التشغيل سليمًا. تحقق من صحة العنقود باستخدام الأمر `etcdctl cluster-health` قبل المتابعة.

#### التحضير {#preparation}

قبل ترقية etcd، اختبر دائمًا الخدمات التي تعتمد على etcd في بيئة تجريبية (staging) قبل نشر الترقية في بيئة الإنتاج.

قبل البدء، [أنشئ نسخة احتياطية من دليل بيانات etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore). إذا حدث خطأ ما أثناء الترقية، فمن الممكن استخدام هذه النسخة الاحتياطية [للرجوع إلى إصدار أقدم](#downgrade) والعودة إلى إصدار etcd القائم.

#### الإصدارات المختلطة {#mixed-versions}

أثناء الترقية، يدعم عنقود etcd إصدارات مختلطة من أعضاء etcd، ويعمل ببروتوكول أدنى إصدار مشترك. لا يُعتبر العنقود مرقًّى إلا بعد ترقية جميع أعضائه إلى الإصدار 3.0. داخليًا، يتفاوض أعضاء etcd فيما بينهم لتحديد إصدار العنقود الكلي، الذي يتحكم في الإصدار المُبلَّغ عنه والميزات المدعومة.

#### القيود {#limitations}

قد يستغرق العضو المرقّى حديثًا ما يصل إلى دقيقتين ليلحق بالعنقود القائم عندما يكون الحجم الإجمالي للبيانات أكبر من 50MB. تحقق من حجم لقطة حديثة لتقدير الحجم الإجمالي للبيانات. بعبارة أخرى، فالأسلم هو انتظار دقيقتين بين ترقية كل عضو.

لحجم بيانات إجمالي أكبر بكثير، 100MB أو أكثر، قد تستغرق هذه العملية التي تجري مرة واحدة وقتًا أطول. يمكن لمسؤولي عناقيد etcd الكبيرة جدًا بهذا الحجم التواصل بحرية مع [فريق etcd][etcd-contact] قبل الترقية، ويسعدنا تقديم المشورة بشأن الإجراء.

#### الرجوع إلى إصدار أقدم {#downgrade}

إذا رُقِّي جميع الأعضاء إلى v3.0، فسيُرقّى العنقود إلى v3.0، ويصبح الرجوع إلى إصدار أقدم من هذه الحالة المكتملة **غير ممكن**. أما إذا بقي أي عضو واحد بالإصدار v2.3، فيظل العنقود وعملياته في حالة «v2.3»، ومن الممكن من حالة العنقود المختلط هذه العودة إلى استخدام الملف الثنائي etcd v2.3 على جميع الأعضاء.

يرجى [إنشاء نسخة احتياطية من دليل البيانات](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) لجميع أعضاء etcd لجعل الرجوع بالعنقود إلى إصدار أقدم ممكنًا حتى بعد اكتمال ترقيته.

### إجراء الترقية {#upgrade-procedure}

يفصّل هذا المثال ترقية عنقود etcd v2.3 ثلاثي الأعضاء يعمل على جهاز محلي.

#### 1. تحقق من متطلبات الترقية. {#1-check-upgrade-requirements}

هل العنقود سليم ويعمل بالإصدار v.2.3.x؟

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. أوقف عملية etcd القائمة {#2-stop-the-existing-etcd-process}

عندما تُوقف كل عملية etcd، ستسجّل بقية أعضاء العنقود أخطاءً متوقعة. هذا طبيعي لأن اتصال أحد أعضاء العنقود قد انقطع (مؤقتًا):

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

من الجيد في هذه المرحلة [إنشاء نسخة احتياطية من دليل بيانات etcd](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) لتوفير مسار للرجوع إلى إصدار أقدم في حال حدوث أي مشكلات:

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. ضع الملف الثنائي etcd v3.0 وابدأ عملية etcd الجديدة {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

سينشر إصدار etcd v3.0 الجديد معلوماته إلى العنقود:

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

تحقق من أن كل عضو، ثم العنقود بأكمله، يصبح سليمًا مع الملف الثنائي etcd v3.0 الجديد:

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


سيسجّل الأعضاء المرقّون تحذيرات مثل ما يلي حتى تكتمل ترقية العنقود بأكمله. هذا متوقع وسيتوقف بعد ترقية جميع أعضاء عنقود etcd إلى v3.0:

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. كرر الخطوة 2 إلى الخطوة 3 لجميع الأعضاء الآخرين {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. الإنهاء {#5-finish}

عندما يُرقَّى جميع الأعضاء، سيبلّغ العنقود بنجاح الترقية إلى 3.0:

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## اعتبارات إضافية {#further-considerations}

- حُدِّثت متغيرات بيئة etcdctl. إذا كان الأمر `ETCDCTL_API=2 etcdctl cluster-health` يعمل بشكل صحيح لكن `ETCDCTL_API=3 etcdctl endpoints health` يستجيب بـ `Error:  grpc: timed out when dialing`، فتأكد من استخدام [أسماء المتغيرات الجديدة](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl).

## المشكلات المعروفة {#known-issues}

- لا يعمل etcd &lt; v3.1 بشكل صحيح إذا بُني باستخدام Go &gt; v1.7. راجع [القضية 6951](https://github.com/etcd-io/etcd/issues/6951) لمزيد من المعلومات.
- إذا ظهر خطأ مثل `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.` في سجلات خادم etcd، فتأكد من أن etcd إصدار مبنيًّا مسبقًا أو مبنيًّا باستخدام (etcd v3.1+ &amp; go v1.7+) أو (etcd &lt;v3.1 &amp; go v1.6.x).
- إضافة عقدة v3 إلى عنقود v2.3 أثناء الترقيات غير مدعومة وقد تُسبب حالات panic. راجع [القضية 7249](https://github.com/etcd-io/etcd/issues/7429) لمزيد من المعلومات. الإصدارات المختلطة من أعضاء etcd مسموح بها فقط أثناء الترحيل إلى v3. أكمل الترقيات قبل إجراء أي تغييرات على العضوية.

[etcd-contact]: https://groups.google.com/g/etcd-dev
