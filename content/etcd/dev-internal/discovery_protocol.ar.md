---
title: بروتوكول خدمة الاكتشاف
weight: 1500
description: اكتشاف بقية أعضاء etcd في مرحلة التهيئة الأولية للعنقود
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/discovery_protocol.md"
---

يساعد بروتوكول خدمة الاكتشاف عضو etcd الجديد على اكتشاف جميع الأعضاء الآخرين في مرحلة التهيئة الأولية للعنقود باستخدام رمز اكتشاف مشترك وقائمة نقاط نهاية.

يُستخدم بروتوكول خدمة الاكتشاف _فقط_ في مرحلة التهيئة الأولية للعنقود، ولا يمكن استخدامه لإعادة التهيئة أثناء التشغيل أو لمراقبة العنقود.

يستخدم البروتوكول رمز اكتشاف جديدًا لتهيئة عنقود etcd _فريد_ واحد. تذكَّر أن رمز اكتشاف واحدًا لا يمكن أن يمثل إلا عنقود etcd واحدًا. فبمجرد بدء بروتوكول الاكتشاف على هذا الرمز، حتى لو فشل في منتصف الطريق، يجب ألا يُستخدم لتهيئة عنقود etcd آخر.

تستعرض بقية هذه المقالة عملية الاكتشاف بأمثلة تنطبق على عنقود اكتشاف مستضاف ذاتيًا.

لاحظ أن هذا المستند يخص اكتشاف v3 فقط. راجع المستند السابق لمزيد من التفاصيل حول [اكتشاف v2][v2-discovery].

## سير عمل البروتوكول {#protocol-workflow}

تقوم فكرة بروتوكول الاكتشاف على استخدام عنقود etcd داخلي لتنسيق تهيئة عنقود جديد. أولًا، يتفاعل جميع الأعضاء الجدد مع خدمة الاكتشاف ويساعدون في توليد قائمة الأعضاء المتوقعة. ثم يُهيِّئ كل عضو جديد خادمه باستخدام هذه القائمة، بما يؤدي الوظيفة نفسها التي يؤديها الخيار -initial-cluster.

في سير العمل النموذجي التالي، سنعرض كل خطوة من خطوات البروتوكول باستخدام الأمر `etcdctl` لتسهيل الفهم، ونفترض أن `http://example.com:2379` يستضيف عنقود etcd مخصصًا لخدمة الاكتشاف.

بحسب الاصطلاح، يستخدم بروتوكول اكتشاف etcd بادئة المفتاح `/_etcd/registry`.


### إنشاء رمز اكتشاف جديد {#creating-a-new-discovery-token}

أنشئ رمزًا فريدًا سيحدد هوية العنقود الجديد. سيُستخدم هذا الرمز بادئةً فريدة في فضاء مفاتيح الاكتشاف في الخطوات التالية. وتتمثل طريقة سهلة لذلك في استخدام `uuidgen`:

```
UUID=$(uuidgen)
```

### تحديد حجم العنقود المتوقع {#specifying-the-expected-cluster-size}

يتوقع رمز الاكتشاف حجمًا للعنقود يجب تحديده. وتستخدم خدمة الاكتشاف هذا الحجم لمعرفة متى تكون قد وجدت جميع الأعضاء الذين سيشكّلون العنقود مبدئيًا.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/_config/size ${cluster_size}
```

عادةً ما يكون حجم العنقود 3 أو 5 أو 7. راجع [الحجم الأمثل للعنقود][cluster-size] لمزيد من التفاصيل.

### تشغيل عمليات etcd {#bringing-up-etcd-processes}

عيِّن رمز الاكتشاف `${UUID}` في الخيار `--discovery-token`، وعيِّن نقاط نهاية عنقود etcd الذي يدعم خدمة الاكتشاف في الخيار `--discovery-endpoints`. سيؤدي ذلك إلى تمكين اكتشاف v3 لتهيئة عنقود etcd.

ستتبع كل عملية etcd الخطوات التالية القليلة داخليًا إذا تم تقديم الخيارين `--discovery-token` و`--discovery-endpoints`.

إذا كانت خدمة الاكتشاف تفعِّل مصادقة شهادة العميل، فهيِّئ الخيارات التالية. وهي تتبع الاستخدام نفسه تمامًا كاستخدام `etcdctl` للتواصل مع عنقود etcd.
```
--discovery-insecure-transport
--discovery-insecure-skip-tls-verify
--discovery-cert
--discovery-key
--discovery-cacert
```

إذا كانت خدمة الاكتشاف تفعِّل المصادقة القائمة على الأدوار، فهيِّئ الخيارات التالية. وهي تتبع الاستخدام نفسه تمامًا كاستخدام `etcdctl` للتواصل مع عنقود etcd.
```
--discovery-user
--discovery-password
```

يمكن أيضًا تغيير قيم الوقت أو المهلة الافتراضية باستخدام الخيارات التالية، وهي تتبع الاستخدام نفسه تمامًا كاستخدام `etcdctl` للتواصل مع عنقود etcd.
```
--discovery-dial-timeout
--discovery-request-timeout
--discovery-keepalive-time
--discovery-keepalive-timeout
```

### تسجيل العضو نفسه {#registering-itself}

أول ما تفعله كل عملية etcd هو تسجيل نفسها في العنقود الجديد المعطى بوصفها عضوًا. يتم ذلك بإنشاء مُعرِّف العضو مفتاحًا في مفتاح السجل الكامل.

```
etcdctl --endpoints=http://example.com:2379 put /_etcd/registry/${UUID}/members/${member_id} ${member_name}=${member_peer_url_1}&${member_name}=${member_peer_url_2}
```

### التحقق من الحالة {#checking-the-status}

يتحقق من حجم العنقود المتوقع وحالة التسجيل، ثم يقرر الإجراء التالي.

```
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/_config/size
etcdctl --endpoints=http://example.com:2379 get /_etcd/registry/${UUID}/members
```

إذا كان الأعضاء المسجلون لا يزالون غير كافيين، فسينتظر ظهور أعضاء آخرين.

إذا كان عدد الأعضاء المسجلين أكبر من الحجم المتوقع N، فسيُعامل أول N عضوًا مسجلًا بوصفهم قائمة أعضاء العنقود. إذا كان العضو نفسه ضمن قائمة الأعضاء، تنجح إجراءات الاكتشاف، ويجلب جميع الأقران عبر قائمة الأعضاء. أما إذا لم يكن ضمن قائمة الأعضاء، فتنتهي إجراءات الاكتشاف بالفشل لأن العنقود قد امتلأ.

قد يتحقق العضو من حالة العنقود حتى قبل تسجيل نفسه. لذلك قد يفشل بسرعة إذا كان العنقود ممتلئًا.

### انتظار جميع الأعضاء {#waiting-for-all-members}

تواصل عملية الانتظار مراقبة بادئة المفتاح `/_etcd/registry/${UUID}/members` حتى العثور على جميع الأعضاء.

```
etcdctl --endpoints=http://example.com:2379 watch /_etcd/registry/${UUID}/members --prefix
```

[v2-discovery]: https://etcd.io/docs/v3.5/dev-internal/discovery_protocol
[cluster-size]: https://etcd.io/docs/v2.3/admin_guide#optimal-cluster-size
[expected-cluster-size]: #specifying-the-expected-cluster-size
[new-discovery-token]: #creating-a-new-discovery-token
