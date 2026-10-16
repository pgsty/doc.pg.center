---
title: "الأسئلة المتكررة"
linkTitle: "FAQ"
weight: 90
description: "الأسئلة المتكررة حول PgBouncer"
icon: fa-solid fa-circle-question
module: [PGBOUNCER]
categories: [مرجع]
upstream_link: "https://www.pgbouncer.org/faq.html"
---

--------

## كيف تتصل بـ PgBouncer؟ {#how-to-connect-to-pgbouncer}

يعمل PgBouncer كخادم Postgres، لذا يكفي أن توجه عميلك إلى
منفذ PgBouncer.

--------

## كيف توزّع الاستعلامات على عدة خوادم؟ {#how-to-load-balance-queries-between-several-servers}

يدعم PgBouncer قائمة مضيفين مفصولة بفواصل في سلسلة اتصال قاعدة البيانات. مع
[`load_balance_hosts=round-robin`](/ar/pgbouncer/config/#load_balance_hosts)،
تتداول الاتصالات الخادمية الجديدة عبر تلك القائمة. مثلًا:

```ini
[databases]
app = host=pg1,pg2 port=5432 dbname=app load_balance_hosts=round-robin
```

يمكنك أيضًا استخدام أدوات خارجية:

1.  التناوب عبر DNS (round-robin). استخدم عدة عناوين IP خلف اسم DNS واحد. لا يبحث PgBouncer
    في DNS في كل مرة يُطلق فيها اتصال جديد، بل يخزّن جميع
    عناوين IP مؤقتًا ويجري التناوب داخليًا. ملاحظة: إذا كان
    هناك أكثر من 8 عناوين IP خلف اسم واحد، فيجب أن تدعم خلفية DNS
    بروتوكول EDNS0. راجع [دعم الاستعلام عن DNS](/ar/pgbouncer/install/#dns-lookup-support) للتفاصيل.

2.  استخدم موزِّع حمل لاتصالات TCP. يبدو أن
    [LVS](http://www.linuxvirtualserver.org/) أو
    [HAProxy](https://www.haproxy.org/) خياران جيدان. من جهة
    PgBouncer قد يكون من الجيد جعل `server_lifetime` أصغر
    وتشغيل `server_round_robin` أيضًا: افتراضيًا تُعاد استخدام الاتصالات
    الخاملة وفق خوارزمية LIFO، وهو ما قد لا يعمل جيدًا عندما
    تكون موازنة الحمل مطلوبة.

--------

## كيف تجري تجاوز الأعطال {#how-to-failover}

مع قائمة مضيفين مفصولة بفواصل و
[`load_balance_hosts=disable`](/ar/pgbouncer/config/#load_balance_hosts)،
يواصل PgBouncer استخدام المضيف نفسه حتى تفشل محاولة اتصال،
ثم يجرب المضيف التالي. لا يؤدي هذا إلى كشف الدور الأساسي/النسخة المماثلة
(primary/replica). لتجاوز أعطالٍ يتبع التغييرات في طبولوجيا قاعدة البيانات،
استخدم أدوات خارجية:

1. إعادة إعداد DNS: عندما يُعاد إعداد عنوان IP خلف اسم DNS
   ما، سيعيد PgBouncer الاتصال بالخادم الجديد. يمكن
   ضبط هذا السلوك بمعاملَي إعداد اثنين:
   `dns_max_ttl` يضبط مدة الحياة لاسم مضيف واحد، بينما
   `dns_zone_check_period` يضبط مدى تكرار الاستعلام عن سجل SOA للمنطقة
   لكشف التغييرات. وإذا تغيّر سجل SOA لمنطقة ما، فإن PgBouncer
   سيعيد الاستعلام عن جميع أسماء المضيفين تحت تلك المنطقة.

2. اكتب مضيفًا جديدًا في الإعداد ودع PgBouncer يعيد تحميله:
   أرسل SIGHUP أو استخدم الأمر `RELOAD` على وحدة التحكم. سيكتشف PgBouncer
   تغيّر إعداد المضيف وسيتصل بالخادم
   الجديد.

3. استخدم الأمر `RECONNECT`. هذا مخصص للحالات التي
   لا ينطبق فيها أي من الخيارين السابقين، مثلًا عندما
   تستخدم HAProxy المذكور آنفًا لتوجيه الاتصالات النازلة من PgBouncer
   إلى المصب. يتسبب `RECONNECT` ببساطة في إعادة فتح جميع اتصالات
   الخادم. لذا شغّله بعد أن يغيّر المكوّن الآخر
   معلومات توجيه الاتصالات الخاصة به.

--------

## كيف تستخدم العبارات المُجهَّزة مع تجميع الجلسات؟ {#how-to-use-prepared-statements-with-session-pooling}

في وضع تجميع الجلسات، يجب أن ينظّف استعلام إعادة التعيين العبارات المُجهَّزة
القديمة. يمكن تحقيق ذلك باستخدام `server_reset_query = DISCARD ALL;`
أو على الأقل `DEALLOCATE ALL;`.

--------

## كيف تستخدم العبارات المُجهَّزة مع تجميع المعاملات؟ {#how-to-use-prepared-statements-with-transaction-pooling}

منذ الإصدار 1.21.0 يستطيع PgBouncer تتبّع العبارات المُجهَّزة في وضع تجميع
المعاملات وضمان تجهيزها فور الحاجة على اتصال الخادم المرتبط. لتمكين هذه الميزة، يجب
ضبط `max_prepared_statements` على قيمة غير صفرية (الافتراضي هو 200). راجع [وثائق
`max_prepared_statements`](/ar/pgbouncer/config/#max_prepared_statements)
لمزيد من التفاصيل.

إذا كنت تستخدم PHP/PDO، فقد يكون غير متوافق — تبعًا لإصداره — مع
دعم PgBouncer للعبارات المُجهَّزة ([#991]). لا يتوافق PHP/PDO إلا
عند استخدام [PHP 8.4+ **و** libpq 17][php-fix]. لذا يُنصح للتجهيزات ذات الإصدارات الأقدم
بالترقية، أو بتعطيل العبارات المُجهَّزة من جهة
العميل.

[php-fix]: https://github.com/php/php-src/commit/f35ad560b468e3e0a6c289949ba9b19af4fa3e7b

[#991]: https://github.com/pgbouncer/pgbouncer/issues/991

### تعطيل العبارات المُجهَّزة في JDBC {#disabling-prepared-statements-in-jdbc}

الطريقة الصحيحة لفعل ذلك في JDBC هي إضافة المعامل `prepareThreshold=0`
إلى سلسلة الاتصال.

### تعطيل العبارات المُجهَّزة في PHP/PDO {#disabling-prepared-statements-in-phppdo}

لتعطيل استخدام العبارات المُجهَّزة من جهة الخادم، يجب ضبط سمة PDO
وهي `PDO::ATTR_EMULATE_PREPARES` على `true`. إما وقت
الاتصال:

    $db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));

أو لاحقًا:

    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);

--------

## كيف ترقّي PgBouncer دون قطع الاتصالات؟ {#how-to-upgrade-pgbouncer-without-dropping-connections}

يمكنك استخدام إعادة تشغيل متدرجة باتباع الإجراء الموصوف في
[قسم الوثائق الخاص بـ `SHUTDOWN WAIT_FOR_CLIENTS`](/ar/pgbouncer/usage/#shutdown-wait_for_clients).

--------

## كيف تعرف أي عميل على أي اتصال خادم؟ {#how-to-know-which-client-is-on-which-server-connection}

استخدم الأمرين `SHOW CLIENTS` و`SHOW SERVERS` على وحدة التحكم.

1.  استخدم `ptr` و`link` لربط اتصال العميل المحلي باتصال
    الخادم.

2.  استخدم `addr` و`port` لاتصال العميل لتحديد اتصال TCP
    الوارد من العميل.

3.  استخدم `local_addr` و`local_port` لتحديد اتصال TCP
    بالخادم.

--------

## هل يجب تثبيت PgBouncer على خادم الويب أم على خادم قاعدة البيانات؟ {#should-pgbouncer-be-installed-on-the-web-server-or-database-server}

يعتمد ذلك على الحالة.

تثبيت PgBouncer على خادم الويب أمر جيد عندما تُستخدم اتصالات قصيرة العمر؛
إذ يُقلَّل عندئذٍ زمن تأخير إنشاء الاتصال. (يتطلب TCP بضع جولات ذهابًا وإيابًا
للحزم قبل أن يصبح الاتصال قابلًا للاستخدام.) أما تثبيت PgBouncer على خادم قاعدة البيانات
فأمر جيد عندما تتصل به مضيفات مختلفة كثيرة (مثل خوادم الويب)؛
إذ يمكن عندئذٍ تحسين اتصالاتها معًا.

من الممكن أيضًا تثبيت PgBouncer على خادم الويب وخادم قاعدة البيانات معًا. الجانب السلبي
لذلك أن كل قفزة PgBouncer تضيف قدرًا صغيرًا من زمن التأخير
إلى كل استعلام.

في نهاية المطاف، ستحتاج إلى اختبار أي نموذج يعمل بشكل أفضل مع احتياجاتك
الأدائية. يجب أيضًا أن تأخذ في الحسبان كيف سيؤثر تثبيت PgBouncer
في تجاوز الأعطال لدى تطبيقاتك في حال اختفاء خادم
الويب أو خادم قاعدة البيانات.
