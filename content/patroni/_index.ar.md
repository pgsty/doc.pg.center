---
title: "توثيق Patroni 4.1.5"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "نظرة عامة على توثيق Patroni للتوفر العالي لـ PostgreSQL."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [مفهوم]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> تشغيل Patroni على **الأنظمة محدودة الذاكرة مع Python 3.11+**

إذا كنت تشغّل Patroni على نظام بحدود ذاكرة صارمة، مثلًا مع `vm.overcommit_memory=2` (الموصى به لـ PostgreSQL)، وتستخدم Python 3.11 أو أحدث، فقد تلاحظ سلوكًا غير متوقع:

- يبدو Patroni سليمًا
- يستمر PostgreSQL في العمل
- تصبح **REST API** الخاصة بـ Patroni **غير مستجيبة**
- يبلغ نظام التشغيل أن Patroni يستمع على منفذ REST API
- تبدو سجلات Patroni طبيعية؛ ومع ذلك قد تظهر الرسائل التالية مرة واحدة: `Exception ignored in thread started by: <object repr() failed>`، `MemoryError`
- قد تحتوي سجلات النواة على رسائل مثل `not enough memory for the allocation`

ينتج هذا السلوك عن [خلل في Python 3.11+](https://github.com/python/cpython/issues/140746). في ظل ظروف الذاكرة الصارمة، قد يتوقف بدء خيط جديد إلى ما لا نهاية عندما لا توجد ذاكرة حرة كافية.

## الحل الموصى به {#recommended-solution}

تقلل إصدارات Patroni الحديثة (4.1.1+، 4.0.8+) من تأثير هذه المشكلة عبر بدء جميع الخيوط المطلوبة مبكرًا أثناء بدء التشغيل، قبل أن يصبح النظام تحت ضغط الذاكرة.

## توصيات إضافية (Linux وglibc) {#additional-recommendations-linux-glibc}

عند التشغيل مع `vm.overcommit_memory=2` (الموصى به لـ PostgreSQL)، نوصي أيضًا ببدء Patroni مع ضبط متغيرات البيئة التالية:

- `MALLOC_ARENA_MAX=1` - يقلل مقدار الذاكرة الافتراضية التي يخصصها glibc للتطبيقات متعددة الخيوط
- `PG_MALLOC_ARENA_MAX=` - يعيد تعيين قيمة `MALLOC_ARENA_MAX` لعمليات PostgreSQL التي يبدأها Patroni.

بالإضافة إلى ذلك، يمكنك ضبط معاملات إعداد Patroni التالية:

- `thread_stack_size` - حجم المكدس المستخدم للخيوط التي يبدأها Patroni. خفض هذه القيمة يقلل استهلاك الذاكرة لعملية Patroni. القيمة الافتراضية التي يضبطها Patroni هي `512kB`. زد `thread_stack_size` إذا تعرض Patroni لأعطال متعلقة بالمكدس؛ وإلا فالقيمة الافتراضية كافية.
- `thread_pool_size` - حجم تجمع الخيوط الذي يستخدمه Patroni للمهام غير المتزامنة والتواصل عبر REST API مع الأعضاء الآخرين أثناء سباق القيادة أو فحوصات الفشل الآمن. القيمة الافتراضية هي `5`، وهي كافية لعناقيد من ثلاث عقد.
- `restapi.thread_pool_size` - حجم تجمع الخيوط المستخدم لمعالجة طلبات REST API. القيمة الافتراضية هي `5`، ما يسمح حتى بخمسة طلبات REST API متوازية. لاحظ أن الطلبات التي تنطوي على استعلامات SQL تُسلسَل عمليًا لأن اتصال قاعدة بيانات واحدًا يُستخدم، لذا فإن زيادة هذه القيمة لا توفر فائدة عادةً.

--------

Patroni هو قالب لحلول PostgreSQL عالية التوفر (HA) باستخدام Python. ولتحقيق أقصى إمكانية وصول، يدعم Patroni مجموعة متنوعة من مخازن الإعداد الموزعة مثل [ZooKeeper](https://zookeeper.apache.org/) أو [etcd](https://github.com/coreos/etcd) أو [Consul](https://github.com/hashicorp/consul) أو [Kubernetes](https://kubernetes.io). نأمل أن يجد مهندسو قواعد البيانات ومديروها ومهندسو DevOps ومهندسو الموثوقية (SREs) الباحثون عن نشر سريع لـ PostgreSQL عالي التوفر في مراكز البيانات — أو في أي مكان آخر — أنه مفيد.

نطلق على Patroni اسم "قالب" لأنه بعيد كل البعد عن كونه نظام نسخ متماثل واحدًا يناسب الجميع أو جاهزًا للتوصيل والتشغيل. ستكون له تحفظاته الخاصة. استخدمه بحكمة. هناك طرق كثيرة لتشغيل التوفر العالي مع PostgreSQL؛ للحصول على قائمة بها، راجع [وثائق PostgreSQL](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling).

إصدارات PostgreSQL المدعومة حاليًا: من 9.3 إلى 18.

**ملاحظة لمستخدمي Citus**: بدءًا من 3.0 يتكامل Patroni بسلاسة مع امتداد قاعدة البيانات [Citus](https://github.com/citusdata/citus) لـ Postgres. يرجى مراجعة [صفحة دعم Citus](/ar/patroni/citus#citus) في توثيق Patroni لمزيد من المعلومات حول كيفية استخدام التوفر العالي في Patroni مع عنقود Citus الموزع.

**ملاحظة لمستخدمي Kubernetes**: يمكن لـ Patroni العمل أصليًا فوق Kubernetes. ألقِ نظرة على فصل [Kubernetes](/ar/patroni/kubernetes#kubernetes) من توثيق Patroni.

<img src="/img/patroni/patroni-logo.png" width="128" height="128" alt="صورة" />
