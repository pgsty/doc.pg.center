---
title: "6. إدارة الذاكرة"
linkTitle: "6. الذاكرة"
weight: 300
description: "تخصيص الذاكرة، وحدودها، والمجمعات، والمخازن المؤقتة، وتحجيم العملية"
icon: fa-solid fa-memory
module: [HAPROXY]
categories: [مهمة]
aliases:
  - /haproxy/management/memory/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 6"
---

يستخدم HAProxy إدارة ذاكرة بسيطة وسريعة معتمدة على المجمعات (pools). وبما أنه يعتمد
على عدد صغير من أنواع الكائنات المختلفة، فإنه أكثر كفاءة بكثير أن تُلتقط الكائنات
الجديدة من مجمع يحتوي أصلًا على كائنات بالحجم المناسب من استدعاء malloc() لكل حجم
مختلف. وتُنظَّم المجمعات كمكدس (stack) أو LIFO، بحيث تُؤخذ الكائنات المخصصة حديثًا من
كائنات أُفرج عنها حديثًا وما تزال ساخنة في مخازن CPU المؤقتة. وتُدمج المجمعات ذات
الأحجام المتشابهة معًا للحد من تشظي الذاكرة.

افتراضيًا، وبما أن التركيز منصبّ على الأداء، يُعاد كل كائن أُفرج عنه إلى المجمع الذي
جاء منه، ولا تُحرَّر الكائنات المخصصة أبدًا لأنه متوقع إعادة استخدامها قريبًا جدًا.

على واجهة سطر الأوامر (CLI)، يمكن التحقق من كيفية استخدام الذاكرة في المجمعات بفضل
الأمر «show pools»:

```shell
> show pools
Dumping pools usage. Use SIGQUIT to flush them.
  - Pool cache_st (16 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccc40=03 [SHARED]
  - Pool pipe (32 bytes): 5 allocated (160 bytes), 5 used, 0 failures, 2 users, @0x9ccac0=00 [SHARED]
  - Pool comp_state (48 bytes): 3 allocated (144 bytes), 3 used, 0 failures, 5 users, @0x9cccc0=04 [SHARED]
  - Pool filter (64 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 3 users, @0x9ccbc0=02 [SHARED]
  - Pool vars (80 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccb40=01 [SHARED]
  - Pool uniqueid (128 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9cd240=15 [SHARED]
  - Pool task (144 bytes): 55 allocated (7920 bytes), 55 used, 0 failures, 1 users, @0x9cd040=11 [SHARED]
  - Pool session (160 bytes): 1 allocated (160 bytes), 1 used, 0 failures, 1 users, @0x9cd140=13 [SHARED]
  - Pool h2s (208 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccec0=08 [SHARED]
  - Pool h2c (288 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cce40=07 [SHARED]
  - Pool spoe_ctx (304 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 2 users, @0x9ccf40=09 [SHARED]
  - Pool connection (400 bytes): 2 allocated (800 bytes), 2 used, 0 failures, 1 users, @0x9cd1c0=14 [SHARED]
  - Pool hdr_idx (416 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd340=17 [SHARED]
  - Pool dns_resolut (480 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccdc0=06 [SHARED]
  - Pool dns_answer_ (576 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9ccd40=05 [SHARED]
  - Pool stream (960 bytes): 1 allocated (960 bytes), 1 used, 0 failures, 1 users, @0x9cd0c0=12 [SHARED]
  - Pool requri (1024 bytes): 0 allocated (0 bytes), 0 used, 0 failures, 1 users, @0x9cd2c0=16 [SHARED]
  - Pool buffer (8030 bytes): 3 allocated (24090 bytes), 2 used, 0 failures, 1 users, @0x9cd3c0=18 [SHARED]
  - Pool trash (8062 bytes): 1 allocated (8062 bytes), 1 used, 0 failures, 1 users, @0x9cd440=19
Total: 19 pools, 42296 bytes allocated, 34266 used.
```

اسم المجمع استرشادي فقط، فهو اسم أول نوع كائن يستخدم هذا المجمع. والحجم بين القوسين هو
حجم الكائن للكائنات في هذا المجمع. وتُقرَّب أحجام الكائنات لأعلى دائمًا إلى أقرب مضاعف للعدد
16 بايت. ويُعرض عدد الكائنات المخصصة حاليًا وما يقابلها من بايتات بحيث يسهل معرفة
المجمع المسؤول عن أعلى استهلاك للذاكرة. كما يُعرض عدد الكائنات المستخدمة حاليًا في
الحقل «used». ويقابل الفرق بين «allocated» و«used» الكائنات التي حُررت وهي متاحة
للاستخدام الفوري. أما العنوان في نهاية السطر فهو عنوان المجمع، والرقم التالي له هو
فهرس المجمع إن وُجد، أو يُعرض بقيمة -1 إذا لم يُخصص أي فهرس.

يمكن تحديد كمية الذاكرة المخصصة لكل عملية باستخدام خيار سطر الأوامر «-m» متبوعًا
بعدد من الميغابايت. وهو يغطي كامل الفضاء القابل للعنونة للعملية، بحيث يشمل الذاكرة
المستخدمة من قبل بعض المكتبات وكذلك المكدس، لكنه حد موثوق عند بناء نظام مقيَّد
الموارد. ويعمل بالطريقة نفسها التي يعمل بها "ulimit -v" على الأنظمة التي توفره، أو
"ulimit -d" على الأنظمة الأخرى.

إذا فشل تخصيص الذاكرة بسبب بلوغ حد الذاكرة أو لأن النظام لا يملك ذاكرة كافية، فسيبدأ
haproxy أولًا بتحرير جميع الكائنات المتاحة من جميع المجمعات قبل محاولة تخصيص الذاكرة
مجددًا. ويمكن تفعيل آلية تحرير الذاكرة غير المستخدمة هذه بإرسال الإشارة SIGQUIT إلى
عملية haproxy.

وأثناء عملية إعادة التحميل، تؤدي العملية المنتقلة إلى حالة التوقف الرشيق (graceful
stop) أيضًا بعض عمليات الإفراغ تلقائيًا بعد تحرير أي اتصال، بحيث تُحرَّر كل الذاكرة
الممكنة لتوفيرها للعملية الجديدة.
