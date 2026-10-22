---
title: "سجل التغييرات"
weight: 70
description: "تاريخ إصدارات PgBouncer وملاحظات الإصدارات"
icon: fa-solid fa-scroll
module: [PGBOUNCER]
categories: [مرجع]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/NEWS.md"
---

--------

## PgBouncer 1.26.x {#pgbouncer-126x}

**2026-10-14  -  PgBouncer 1.26.1  -  «بدء التشغيل مرة واحدة فقط»**

- الأمان
    * إصلاح CVE-2026-107350: كان PgBouncer من الإصدار 1.17.0 إلى 1.26.0 يعالج رسالة StartupMessage ثانية تُرسَل أثناء مصادقة SCRAM عندما يتصل العميل بقاعدة بيانات غير موجودة. كان بإمكان مهاجم يعرف كلمة مرور مستخدم مُدرج في `auth_file` استغلال ذلك لتسجيل الدخول باسم أي مستخدم آخر يُصادَق عليه باستخدام SCRAM، بما في ذلك المشرفون والمستخدمون الفائقون في خادم PostgreSQL. يتطلب ذلك استخدام مصادقة SCRAM لكلا المستخدمين. ويمكن أن يأتي المستخدم المنتحَلة هويته من `auth_file` أو من `auth_query`.
    * إصلاح CVE-2026-107349: كان بإمكان عميل غير مُصادَق عليه جعل PgBouncer من الإصدار 1.20.0 إلى 1.26.0 يدور بلا نهاية على نواة واحدة من المعالج، فيتوقف عن خدمة جميع العملاء، عبر إرسال معامل بدء التشغيل `options` متضمنًا اسم خيار فارغًا مثل `-c=`. لا يمكن استغلال هذه الثغرة إلا عندما يكون `ignore_startup_parameters` غير فارغ ولا يحتوي على `options`.
    * إصلاح CVE-2026-107348: كان من الممكن أن يؤدي تجاوز عدد صحيح في منطق نمو مخزن الحزم المؤقت لدى PgBouncer من الإصدار 1.21.0 إلى 1.26.0 إلى تجمُّد PgBouncer في حلقة لا نهائية عندما يرسل عميل ترويسة حزمة تعلن طولًا أكبر من 2^31. لا يمكن استغلال هذه الثغرة إلا عندما يُضبط `max_packet_size` على 2147483649 أو أكثر؛ أما القيمة الافتراضية 2147483647 فلا تتأثر. منذ الإصدار 1.23.0، يمكن الوصول إلى هذا العيب قبل المصادقة. ينتمي هذا العيب إلى فئة CVE-2026-6668 نفسها، لكنه يقع في تنفيذ مختلف للمخزن المؤقت.
- الإصلاحات
    * منح `ignore_startup_parameters` الأولوية على المعاملات المتتبَّعة. منذ الإصدار 1.26.0، يُتتبَّع `search_path` افتراضيًا، مما جعل `ignore_startup_parameters = search_path` يفقد تأثيره دون تنبيه. ومنذ صدور ذلك الإصدار، أُبلغ عن عيوب مختلفة تتعلق بتتبّع معامل `search_path`. ستُعالج هذه العيوب في إصدار لاحق. أصبحت إضافة `search_path` إلى `ignore_startup_parameters` تستعيد الآن سلوك الإصدار 1.25 الذي يتجاهله. (أُدخل العيب في الإصدار 1.26.0)

**2026-09-23  -  PgBouncer 1.26.0  -  «تجاهُل جميع search_path السابقة»**

- الأمان
    * إصلاح CVE-2026-19888: لم يكن PgBouncer قبل الإصدار 1.26.0 يتحقق من أن رسالة client-final-message الخاصة بـ SCRAM تحتوي على nonce. كان بإمكان مهاجم بعيد غير مُصادَق عليه إحداث انهيار PgBouncer عبر إرسال رسالة client-final-message بدون nonce. ينطبق ذلك أيضًا على المستخدمين غير الموجودين، لأن PgBouncer يجري لأجلهم تبادل SCRAM وهميًا. هذا العيب موجود منذ أُضيف دعم SCRAM في PgBouncer 1.11.0.
    * إصلاح CVE-2026-6668: كان تجاوز عدد صحيح في منطق نمو مخزن الحزم المؤقت لدى PgBouncer قبل الإصدار 1.26.0 قد يسبب تجمُّد PgBouncer في حلقة لا نهائية. تطلّب ذلك إرسال كمية كبيرة من البيانات إلى مخزن حزم مؤقت واحد، وهو أمر ممكن دون مصادقة مسبقة عندما يُترك `max_packet_size` عند قيمته الافتراضية. ولأن PgBouncer أحادي الترابط، فقد أوقفه هذا التجمّد عن خدمة أي عميل حتى تُقتل العملية.
    * إصلاح CVE-2026-6669: لم يكن PgBouncer قبل الإصدار 1.26.0 يقيّد عدد تكرارات SCRAM التي يقبلها من الخادم. كان بإمكان خادم PostgreSQL خبيث أو مخترق أن يجعل PgBouncer يؤدي كمية غير محدودة من العمل أثناء عملية تسجيل دخول واحدة، فيمنعه خلال ذلك من خدمة سائر العملاء وقواعد البيانات. أصبح عدد التكرارات الآن يجب ألا يتجاوز 1000000.
- الميزات
    * تتبّع جميع المعاملات التي يُبلغ عنها PostgreSQL افتراضيًا. يعني ذلك عمليًا أن `search_path` (على PostgreSQL 18 وما فوق) و`default_transaction_read_only` (على PostgreSQL 14 وما فوق) أصبحا الآن مُتتبَّعين افتراضيًا. سابقًا كان العميل الذي يشغّل `SET search_path` أو `SET default_transaction_read_only = true` في وضع تجميع المعاملات يؤثر في عملاء آخرين يستخدمون لاحقًا اتصال الخادم نفسه. ([#1580], [#1573])
    * إضافة إعداد `pool_idle_timeout` لتنظيف المجمّعات التي لم تُستخدم منذ فترة. هذا مفيد في التجهيزات ذات المستخدمين الكثيرين المختلفين الذين يتصلون بشكل نادر. دون تمكين هذا الإعداد ينمو عدد المجمّعات بلا حد في مثل هذه التجهيزات. الإعداد معطَّل افتراضيًا، لأن إزالة مجمّع تُفقده أيضًا إحصاءاته. ([#1491])
    * السماح بضبط `query_wait_timeout` لكل مستخدم ولكل قاعدة بيانات. ([#1449])
    * إضافة الإحصائية `client_login_count` إلى `SHOW STATS`، التي تعدّ عمليات تسجيل دخول العملاء الناجحة. يجعل هذا من الممكن اكتشاف العملاء الذين يتنقلون بين الاتصالات باستمرار. ([#1457])
    * إرسال رسائل `ParameterStatus` خاصة بـ PgBouncer إلى العملاء عند تسجيل الدخول: `pgbouncer.version` و`pgbouncer.pool_mode` و`pgbouncer.max_prepared_statements`. يتيح هذا للعملاء والمشغّلات اكتشاف أنهم متصلون عبر PgBouncer وتكييف سلوكهم وفقًا لذلك. ([#1490])
    * إضافة إعداد `login_notify_message`. عندما يكون مضبوطًا، تُرسَل قيمته إلى العملاء كرسالة NOTICE بعد تسجيل دخولهم. يمكن استخدام هذا لتوضيح للعملاء أنهم متصلون عبر PgBouncer لا مباشرة بـ PostgreSQL. ([#1488])
    * إضافة دعم بناء PgBouncer باستخدام meson، بما في ذلك بناء Windows باستخدام بيئة UCRT64. تظل عمليات البناء عبر Autoconf مدعومة. ([#1524], [#1426], [#1568], [#1585], [#1602], [#1607])
    * إضافة شعار. ([#1609])
- التغييرات
    * إزالة ميزة إعادة التشغيل المباشر المهملة (`-R`، المعروفة أيضًا بالاستحواذ)، مع الأمرين الإداريين `SHOW FDS` و`SUSPEND` اللذين لم يكونا موجودين إلا لدعمها. استخدم [إعادة التشغيل المتدرجة باستخدام `so_reuseport`][rolling-restart-docs] بدلًا منها. ([#1581])
    * زيادة الطول الأقصى لكلمات المرور إلى 65535 بايت، بما يطابق libpq. ([#1310], [#1520])
    * التعامل مع اسم مستخدم `NULL` يعيده `auth_query` كما لو لم تُعَد أي صفوف، بدلًا من التعامل معه كخطأ. ([#1569])
    * قبول `SET extra_float_digits` على قاعدة بيانات الإدارة، التي ترسلها مشغّلات JDBC الأحدث لـ PostgreSQL أثناء إعداد الاتصال. ([#1550])
    * السماح لـ `mkauth.py` بالكتابة إلى stdout بتمرير `-` كملف إخراج. ([#1514])
    * التوقف عن تسجيل أخطاء مزعجة عند حدوث EOF غير متوقع من العملاء عند البناء مقابل OpenSSL 3. ([#1507])
    * تضمين خطأ النظام الكامن في رسائل أخطاء TLS عند البناء مقابل OpenSSL 3. ([#1492])
    * اشتراط مُصرِّف C11. ([#1417])
    * تسجيل الحد الذي تسبب في إخلاء اتصال خادم. أصبح سبب قطع الاتصال الآن `evicted for max_db_connections` أو `evicted for pool_size` أو `evicted for max_user_connections` بدلًا من `evicted` المجردة. ([#1597])
- الإصلاحات
    * إصلاح تسبّب رسائل `COPY` المتأخرة في استنزاف المجمّعات في وضع تجميع المعاملات. يجعل هذا أيضًا `COPY` يعمل خارج معاملة صريحة في وضع تجميع المعاملات. ([#1471])
    * إصلاح إخفاقات مصادقة LDAP مع أسماء DN الطويلة بزيادة الطول الأقصى لعناوين URL الخاصة بـ LDAP. ([#1497])
    * إصلاح إتلاف تمرير SCRAM (pass-through) لبيانات الاعتماد المخزنة مؤقتًا لمستخدم مُجبَر، مما كان يسبب فشل عمليات تسجيل الدخول إلى الخادم مع رفض الخادم الحقيقي لإثبات SCRAM. ([#1612])
    * إصلاح فشل تمرير SCRAM مع أسرار SCRAM المخزنة بعد إعادة اتصال بالخادم، مع الخطأ "password is SCRAM secret but client authentication did not provide SCRAM keys". ([#1504], عيب أُدخل في الإصدار 1.25.1)
    * إصلاح انهيار use-after-free عند انقطاع اتصال عميل نسخ مماثل بينما لا يزال اتصال خادمه في طور تسجيل الدخول. ([#1577])
    * إصلاح إخلاء اتصالات الخادم الخاملة لعملاء النسخ المماثل عندما يكون المجمّع ممتلئًا. سابقًا كان عميل نسخ مماثل واحد قادرًا على إخلاء كل خادم خامل في المجمّع بدلًا من خادم واحد فقط، ولم يكن أي إخلاء يحدث إطلاقًا عندما يحتوي المجمّع على خوادم أكثر من `pool_size` بسبب المجمّع الاحتياطي أو طلبات الإلغاء. ([#1597])
    * إصلاح توقف اتصالات TLS عندما تتجاوز حزمة واحدة حدود مخزن الحزم المؤقت، مثل `SET application_name` بقيمة طويلة. ([#1531])
    * إصلاح إرسال ردود العبارات المعدة مسبقًا بترتيب خاطئ عندما تمزج دفعة واحدة رسائل `Parse` و`Close` دون `Sync` بينهما. ([#1555])
    * إصلاح سلوك غير صحيح تحدثه المعاملات المدرجة في `track_extra_parameters` التي لا يُبلغ عنها الخادم عندما يضبطها عميل في حزمة البدء الخاصة به. ([#1576])
    * إصلاح إخفاقات تسجيل الدخول عندما يقسّم الخادم حزم تسجيل دخوله عبر حزم TCP متعددة، كما في حالة وجود وسيط آخر بين PgBouncer وPostgreSQL. ([#1446])
    * إصلاح إغلاق `query_timeout` لاتصالات عندما لا يوجد استعلام قيد التنفيذ. ([#1395])
    * إصلاح إرسال رسالة `NegotiateProtocolVersion` مكررة عندما لا يتوفر خادم فورًا. ([#1460])
    * إصلاح عرض العمود `pool_size` في `SHOW USERS` قيمةً لمستخدمين ليس لديهم قيمة مضبوطة. ([#1489])
    * إصلاح رسالة الخطأ للأمر الإداري `ENABLE`. ([#1308])
    * إصلاح البناء مقابل إصدارات OpenSSL المستقبلية التي تجعل `struct asn1_string_st` مبهمة. ([#1440])
    * منع المُصرِّف من إزالة محو البيانات التشفيرية الحساسة من المكدس عبر التحسين. ([#1508])
    * إصلاح ربط `pgbevent.dll` باستخدام clang على Windows. ([#1571])
    * إصلاح مسارات الملفات في المستوى الجذري في أرشيف tar الخاص بالإصدار، والتي كانت مخزنة بالشكل `pgbouncer-X.Y.Z/./configure` بدلًا من `pgbouncer-X.Y.Z/configure`. ([#1549])
    * إصلاح تسريب للذاكرة عند قراءة `track_extra_parameters` من التهيئة. ([#1510])
    * إصلاح تسريب للذاكرة عند كل حزمة بدء تحتوي على معامل ملحق بروتوكول (بادئة `_pq_.`)، كان يمكن لعملاء غير مُصادَق عليهم التحريض عليه. ([#1540])

[rolling-restart-docs]: /ar/pgbouncer/usage/#shutdown-wait_for_clients
[#1308]: https://github.com/pgbouncer/pgbouncer/pull/1308
[#1310]: https://github.com/pgbouncer/pgbouncer/pull/1310
[#1395]: https://github.com/pgbouncer/pgbouncer/pull/1395
[#1417]: https://github.com/pgbouncer/pgbouncer/pull/1417
[#1426]: https://github.com/pgbouncer/pgbouncer/pull/1426
[#1440]: https://github.com/pgbouncer/pgbouncer/pull/1440
[#1446]: https://github.com/pgbouncer/pgbouncer/pull/1446
[#1449]: https://github.com/pgbouncer/pgbouncer/pull/1449
[#1457]: https://github.com/pgbouncer/pgbouncer/pull/1457
[#1460]: https://github.com/pgbouncer/pgbouncer/pull/1460
[#1471]: https://github.com/pgbouncer/pgbouncer/pull/1471
[#1488]: https://github.com/pgbouncer/pgbouncer/pull/1488
[#1489]: https://github.com/pgbouncer/pgbouncer/pull/1489
[#1490]: https://github.com/pgbouncer/pgbouncer/pull/1490
[#1491]: https://github.com/pgbouncer/pgbouncer/pull/1491
[#1492]: https://github.com/pgbouncer/pgbouncer/pull/1492
[#1497]: https://github.com/pgbouncer/pgbouncer/pull/1497
[#1504]: https://github.com/pgbouncer/pgbouncer/pull/1504
[#1507]: https://github.com/pgbouncer/pgbouncer/pull/1507
[#1508]: https://github.com/pgbouncer/pgbouncer/pull/1508
[#1510]: https://github.com/pgbouncer/pgbouncer/pull/1510
[#1514]: https://github.com/pgbouncer/pgbouncer/pull/1514
[#1520]: https://github.com/pgbouncer/pgbouncer/pull/1520
[#1524]: https://github.com/pgbouncer/pgbouncer/pull/1524
[#1531]: https://github.com/pgbouncer/pgbouncer/pull/1531
[#1540]: https://github.com/pgbouncer/pgbouncer/pull/1540
[#1549]: https://github.com/pgbouncer/pgbouncer/pull/1549
[#1550]: https://github.com/pgbouncer/pgbouncer/pull/1550
[#1555]: https://github.com/pgbouncer/pgbouncer/pull/1555
[#1568]: https://github.com/pgbouncer/pgbouncer/pull/1568
[#1569]: https://github.com/pgbouncer/pgbouncer/pull/1569
[#1571]: https://github.com/pgbouncer/pgbouncer/pull/1571
[#1573]: https://github.com/pgbouncer/pgbouncer/pull/1573
[#1576]: https://github.com/pgbouncer/pgbouncer/pull/1576
[#1577]: https://github.com/pgbouncer/pgbouncer/pull/1577
[#1580]: https://github.com/pgbouncer/pgbouncer/pull/1580
[#1581]: https://github.com/pgbouncer/pgbouncer/pull/1581
[#1585]: https://github.com/pgbouncer/pgbouncer/pull/1585
[#1597]: https://github.com/pgbouncer/pgbouncer/pull/1597
[#1602]: https://github.com/pgbouncer/pgbouncer/pull/1602
[#1607]: https://github.com/pgbouncer/pgbouncer/pull/1607
[#1609]: https://github.com/pgbouncer/pgbouncer/pull/1609
[#1612]: https://github.com/pgbouncer/pgbouncer/pull/1612

--------

## PgBouncer 1.25.x {#pgbouncer-125x}

**2026-05-08  -  PgBouncer 1.25.2  -  «لمسة إنسانية بانعطافة جديدة في سباق على اللقب مليء بالمجهول»**

- الأمان
  * إصلاح CVE-2026-6664: تجاوز عدد صحيح في شيفرة تحليل حزم الشبكة لدى PgBouncer قبل الإصدار 1.25.2 يتجاوز فحص حدود وقد يؤدي إلى انهيار. يستطيع مهاجم بعيد غير مُصادَق عليه إحداث انهيار PgBouncer بحزمة مصادقة SCRAM مشوهة.
  * إصلاح CVE-2026-6665: لم تتحقق شيفرة SCRAM في PgBouncer قبل الإصدار 1.25.2 من القيمة المرجعة لـ `strlcat()` بشكل صحيح عند بناء محتوى رسالة client-final-message الخاصة بـ SCRAM. يستطيع خادم خلفي خبيث يرسل رسالة server-final-message الخاصة بـ SCRAM بـ nonce طويل التحريض على تجاوز المكدس.
  * إصلاح CVE-2026-6666: إحالة محتملة إلى مؤشر فارغ في PgBouncer قبل الإصدار 1.25.2 كان يمكن أن تؤدي إلى انهيار إذا أرسل الخادم استجابة خطأ دون حقل SQLSTATE.
  * إصلاح CVE-2026-6667: لم يُجرِ PgBouncer قبل الإصدار 1.25.2 فحص تخويل مناسب للأمر الإداري `KILL_CLIENT`. كان جميع المستخدمين الذين لديهم وصول إلى وحدة تحكم الإدارة، التي تتطلب هي نفسها تخويلًا، قادرين على تشغيل هذا الأمر. كان ينبغي السماح به فقط للمستخدمين المدرجين في المعامل `admin_users`.

- الإصلاحات
  * توضيح توثيق المعامل `default_pool_size`.
  * تصحيح التوثيق لأجل `client_tls13_ciphers` و`server_tls13_ciphers`.

**2025-12-03  -  PgBouncer 1.25.1  -  «إصلاح حزمة من العيوب قبل عيد الميلاد»**

- الأمان
  * إصلاح CVE-2025-12819: قبل هذا الإصدار كان بإمكان مهاجم غير مُصادَق عليه تنفيذ SQL اعتباطي أثناء المصادقة عبر تقديم معامل search_path خبيث في رسالة StartupMessage. الأنظمة التي تجمع كل التهيئات التالية معرضة للإصابة:

    1. `track_extra_parameters` يشمل search_path (تهيئة غير افتراضية، مضبوطة على الأرجح فقط في بيئات تستخدم Citus أو PostgreSQL 18)
    2. `auth_user` مضبوط على سلسلة نصية غير فارغة (تهيئة غير افتراضية)
    3. `auth_query` مُهيأ دون أسماء كائنات مؤهلة بالكامل (تهيئة افتراضية، المعامل < غير مؤهل بالمخطط)

- الإصلاحات
    - إصلاح أخطاء مصادقة SCRAM الارتجالية بعد إعادة الاتصال بالخادم ([#1432], أُدخل في الإصدار 1.25.0)
    - إضافة تعريفات الأنواع (typedefs) الناقصة للمعماريات النادرة التي لا تدعم SIMD ([#1414], أُدخل في الإصدار 1.25.0)
    - إزالة تحذير السجل المزعج عندما يغلق العميل الاتصال قبل إرسال أي بيانات ([#1420], أُدخل في الإصدار 1.25.0)
    - منع إحالة مؤشر NULL محتملة ([#1423], أُدخل في الإصدار 1.25.0)
    - إصلاح تسريب محتمل للذاكرة ([#1422], أُدخل في الإصدار 1.25.0)
    - إصلاح تحليل SCRAM لرسائل الخادم ([#1431], أُدخل في الإصدار 1.25.0)

[#1414]: https://github.com/pgbouncer/pgbouncer/pull/1414
[#1420]: https://github.com/pgbouncer/pgbouncer/pull/1420
[#1422]: https://github.com/pgbouncer/pgbouncer/pull/1422
[#1423]: https://github.com/pgbouncer/pgbouncer/pull/1423
[#1431]: https://github.com/pgbouncer/pgbouncer/pull/1431
[#1432]: https://github.com/pgbouncer/pgbouncer/pull/1432

**2025-11-09  -  PgBouncer 1.25.0  -  «ذلك الإصدار بدعم LDAP»**

- الميزات
    * إضافة مصادقة LDAP! يمكنك تهيئتها باستخدام ملف HBA أو باستخدام `auth_ldap_options`. ([#731])
    * إضافة دعم اتصالات TLS المباشرة من جانب العميل. يتيح هذا للعملاء استخدام إعداد اتصال TLS الأسرع الذي قُدِّم في PostgreSQL 17. لا يستطيع PgBouncer (بعدُ) الاتصال بخوادم PostgreSQL باستخدام إعداد الاتصال الأسرع هذا. ([#1359])
    * إضافة حالة الخمول إلى `SHOW CLIENTS`. ([#1191])
    * إضافة إعداد `transaction_timeout`، عالميًا وعلى مستوى المستخدم معًا. ([#1242])
    * إرسال رسالة NOTICE إلى العميل إذا بقي في قائمة الانتظار دون تلقي اتصال لأكثر من 5 ثوانٍ. يمكن تغيير هذه المدة/تعطيلها باستخدام `query_wait_notify`. ([#1264])
    * إضافة إعداد `scram_iterations` للسماح للمشغلين بمقايضة الأمن بسرعة المصادقة ([#1339])
    * إضافة `client_tls13_ciphers` و`server_tls13_ciphers` لاختيار حِزم تشفير TLSv1.3 التي تُمكَّن. ([#1352])
- التغييرات
    * تحسين أداء مصادقة SCRAM الارتجالية بشكل كبير. ([#1338])
    * السماح لـ `KILL` بألا يأخذ قاعدة بيانات، ما يعني الآن تنفيذ `KILL` على جميع قواعد البيانات. ([#1317])
    * يرسل استعلام فحص الصحة افتراضيًا استعلامًا فارغًا بدلًا من `SELECT 1`. ([#1233])
    * تسجيل تحذير عند امتلاء قائمة انتظار PAM. يسهّل هذا تحديد سبب بطء الاستعلامات الناتج عن امتلائها. ([#1297])
    * يُبلغ الأمر `RELOAD` الآن عن أي أخطاء وقعت أثناء إعادة التحميل. ([#1231])
    * تمكين الوصول إلى مقبس UNIX الخاص بـ PgBouncer أثناء الإيقاف لاتصالات الإدارة. يسهّل هذا على المشغّل معرفة سبب عدم توقف عملية PgBouncer و/أو تشغيل `KILL_CLIENT` يدويًا للاتصالات العالقة. ([#1305])
    * تغيير `mkauth.py` بحيث لم يعد يضيف حقلًا ثالثًا مهملًا ([#1365])
    * تحسين رسائل `FATAL` في الدالتين `disconnect_client` و`disconnect_server`. ([#1382])
    * التوقف عن استخدام دالة OpenSSL المهملة `EVP_PKEY_get0_EC_KEY`. كان هذا قد يسبب مشكلات مع بعض تطبيقات FIPS. ([#1384])
- الإصلاحات
    * إصلاح انهيار يتعلق بكلمات المرور الطويلة (1024 حرفًا أو أكثر). ([#1215])
    * إصلاح الاتصالات متعددة المضيفين عند استخدام `server_tls_sslmode=verify-full`. ([#1303])
    * إصلاح خطأ `FATAL` نادر عند تمرير طلبات الإلغاء. ([#1383])
    * إصلاح فرز المعاملات في `SHOW CONFIG`. ([#1403])
    * تحصين تحليل حزمة البدء. ([#1407])

[#731]: https://github.com/pgbouncer/pgbouncer/pull/731
[#1191]: https://github.com/pgbouncer/pgbouncer/pull/1191
[#1215]: https://github.com/pgbouncer/pgbouncer/pull/1215
[#1231]: https://github.com/pgbouncer/pgbouncer/pull/1231
[#1233]: https://github.com/pgbouncer/pgbouncer/pull/1233
[#1242]: https://github.com/pgbouncer/pgbouncer/pull/1242
[#1264]: https://github.com/pgbouncer/pgbouncer/pull/1264
[#1297]: https://github.com/pgbouncer/pgbouncer/pull/1297
[#1303]: https://github.com/pgbouncer/pgbouncer/pull/1303
[#1305]: https://github.com/pgbouncer/pgbouncer/pull/1305
[#1317]: https://github.com/pgbouncer/pgbouncer/pull/1317
[#1338]: https://github.com/pgbouncer/pgbouncer/pull/1338
[#1339]: https://github.com/pgbouncer/pgbouncer/pull/1339
[#1352]: https://github.com/pgbouncer/pgbouncer/pull/1352
[#1359]: https://github.com/pgbouncer/pgbouncer/pull/1359
[#1365]: https://github.com/pgbouncer/pgbouncer/pull/1365
[#1382]: https://github.com/pgbouncer/pgbouncer/pull/1382
[#1383]: https://github.com/pgbouncer/pgbouncer/pull/1383
[#1384]: https://github.com/pgbouncer/pgbouncer/pull/1384
[#1403]: https://github.com/pgbouncer/pgbouncer/pull/1403
[#1407]: https://github.com/pgbouncer/pgbouncer/pull/1407

--------

## PgBouncer 1.24.x {#pgbouncer-124x}

**2025-04-16  -  PgBouncer 1.24.1  -  «CVE-2025-2291 ‏VALID UNTIL بالأمس»**

- الأمان
  * إصلاح CVE-2025-2291: سابقًا لم يكن PgBouncer يأخذ في الحسبان صلاحية VALID
    UNTIL لكلمة مرور المستخدم عند الاستعلام عن تجزئات كلمات المرور باستخدام
    auth_query الخاص به. لذا إذا استُخدم PgBouncer كوكيل شفاف أمام
    Postgres فقد كان يسمح بكلمات مرور انتهت صلاحيتها بالفعل. لحل هذه
    المشكلة غُيِّر auth_query الافتراضي وأمثلة دوال auth_query المخصصة
    في التوثيق لتأخذ VALID UNTIL في الحسبان. إذا كنت تستخدم
    auth_query مخصصًا فينبغي أن تحدّثه تبعًا لذلك. إذا كنت
    تستخدم auth_query الافتراضي، فيمكنك إما التحديث إلى PgBouncer
    1.24.1 أو تغيير تهيئتك لاستخدام auth_query الافتراضي الجديد على
    إصدار سابق من PgBouncer.

- الإصلاحات
  * إصلاح دعم PAM بالتراجع عن دعم مصادقة `pam` في ملف HBA. ([#1291]) (عيب أُدخل في الإصدار 1.24.0)
  * إصلاح عيب عند إنقاص عدد اتصالات المستخدم. كان هذا مضمَّنًا في الوسم 1.24.0 على GitHub، لكن أرشيف tar الخاص بالإصدار لم يحتوِ على هذا الإصلاح.  ([#1238]) (عيب أُدخل في الإصدار 1.24.0)
  * إضافة `test_load_balance_hosts.py` إلى أرشيف tar. ([#1282])
  * إصلاح مشكلات في الاختبارات للسماح لمجهزي حزم Debian بتشغيلها. ([#1266], [#1250])

- التوثيق
  * تحديث مثال `auth_query` لضبط `search_path` آمن. ([#1245])

[#1238]: https://github.com/pgbouncer/pgbouncer/pull/1238
[#1291]: https://github.com/pgbouncer/pgbouncer/pull/1291
[#1282]: https://github.com/pgbouncer/pgbouncer/pull/1282
[#1266]: https://github.com/pgbouncer/pgbouncer/pull/1266
[#1250]: https://github.com/pgbouncer/pgbouncer/pull/1250
[#1245]: https://github.com/pgbouncer/pgbouncer/pull/1245

**2025-01-10  -  PgBouncer 1.24.0  -  «عام جديد، bouncer جديد»**

- الميزات
  * إضافة دعم `Type=notify-reload` لأجل systemd. يتطلب هذا
    إصدار systemd 253 أو أحدث. ([#1148])
  * إضافة الأمر `KILL_CLIENT` إلى وحدة تحكم الإدارة. يتيح هذا إنهاء
    اتصال عميل بالقوة. ([#1147])
  * إضافة إعداد `max_user_client_connections`، عالميًا وعلى مستوى المستخدم معًا. ([#1137])
  * إضافة إعداد `max_db_client_connections`، عالميًا وعلى مستوى قاعدة البيانات معًا. ([#1138])
  * إضافة العداد `current_client_connections` إلى ناتج `SHOW USERS` و`SHOW DATABASES`. ([#1137], [#1138])
  * إضافة المعامل `load_balance_hosts`، لدعم **عدم** موازنة الحمل بين المضيفين. ([#736])
  * كشف عدادات استخدام العبارات المعدة مسبقًا في `SHOW STATS`. ([#1192])
  * إضافة إعداد `client_idle_timeout`. ([#1189])
  * إضافة `query_timeout` و`reserve_pool_size` على مستوى المستخدم. ([#1180], [#1228])
  * تمكين دعم مصادقة `pam` في ملف HBA. ([#326])

- التغييرات
  * عدم إعادة تدوير الاتصالات عند RELOAD إذا لم تتغير تهيئة TLS. سابقًا
    إذا كانت لديك اتصالات TLS فكانت جميعها تُعاد تدويرها عند RELOAD، مما قد
    يسبب تدهورًا مؤقتًا لكنه خطير في الأداء. الآن لا يحدث
    هذا إلا عندما تتغير إعدادات TLS فعلًا. ([#1157])
  * تمكين دعم العبارات المعدة مسبقًا افتراضيًا؛ أصبح `max_prepared_statements`
    مضبوطًا الآن على 200 افتراضيًا. ينبغي أن يؤثر تغيير القيم الافتراضية هذا فقط في
    العملاء الذين يستخدمون العبارات المعدة مسبقًا فعلًا. إذا كنت تستخدم العبارات
    المعدة مسبقًا فيُنصح بقراءة قيود دعم العبارات المعدة
    مسبقًا في [وثائقنا][prepared-docs] ([#1144])
  * أصبح بالإمكان الآن التعرف على المقابس/العملاء/الخوادم بمعرّف فريد في ناتج
    الإدارة. سابقًا كان يمكن التعرف عليها بمؤشرها (pointer)، لكن هذه
    المؤشرات كانت غالبًا ما يعاد استخدامها من عملاء جدد بعد قطع الاتصال. ([#1172])
  * خطأ أوضح لملف pidfile فارغ. ([#1195])
  * إعادة الخطأ الأصلي إلى العميل في حال فشل `server_login_retry`. ([#1152])
  * تسجيل خطأ الخادم الأصلي في حال حدوث خطأ من `auth_query`. ([#1187])
  * ضبط `default_pool_size` على 0 يعني حجمًا غير محدود. ([#1227])
  * تغيير اسم إعداد `reserve_pool` الخاص بقواعد البيانات إلى
    `reserve_pool_size`. ما يزال الاسم السابق اسمًا بديلًا للاسم الجديد.
    ([#1232])

- الإصلاحات
  * التعامل بشكل أفضل مع حالات خطأ غير محتملة مختلفة، مثل أخطاء OOM. كانت هذه
    تسبب سابقًا انهيارات أو تسريبات للذاكرة. ([#1108], [#1101], [#1099], [#1169], [#1202])
  * تصحيح القيمة الافتراضية لـ `server_tls_sslmode` في ملف التهيئة النموذجي. ([#1133])
  * إزالة ذكر اسم بديل غير صالح لـ `server_tls_protocols` في التوثيق. ([#1155])
  * إصلاح عيب عند استخدام `auth_query` واتصالات النسخ المماثل معًا. كان هذا
    العيب يسبب إخفاقات اتصال في مثل هذه التجهيزات. ([#1166])
  * تجاهل طلبات إلغاء العميل أثناء قيام PgBouncer بضبط إعداد الخادم. ([#298])

[prepared-docs]: /ar/pgbouncer/config/#max_prepared_statements

[#1148]: https://github.com/pgbouncer/pgbouncer/pull/1148
[#1147]: https://github.com/pgbouncer/pgbouncer/pull/1147
[#1137]: https://github.com/pgbouncer/pgbouncer/pull/1137
[#1138]: https://github.com/pgbouncer/pgbouncer/pull/1138
[#736]: https://github.com/pgbouncer/pgbouncer/pull/736
[#1192]: https://github.com/pgbouncer/pgbouncer/pull/1192
[#1189]: https://github.com/pgbouncer/pgbouncer/pull/1189
[#1180]: https://github.com/pgbouncer/pgbouncer/pull/1180
[#1228]: https://github.com/pgbouncer/pgbouncer/pull/1228
[#326]: https://github.com/pgbouncer/pgbouncer/pull/326
[#1157]: https://github.com/pgbouncer/pgbouncer/pull/1157
[#1144]: https://github.com/pgbouncer/pgbouncer/pull/1144
[#1172]: https://github.com/pgbouncer/pgbouncer/pull/1172
[#1195]: https://github.com/pgbouncer/pgbouncer/pull/1195
[#1152]: https://github.com/pgbouncer/pgbouncer/pull/1152
[#1187]: https://github.com/pgbouncer/pgbouncer/pull/1187
[#1227]: https://github.com/pgbouncer/pgbouncer/pull/1227
[#1232]: https://github.com/pgbouncer/pgbouncer/pull/1232
[#1108]: https://github.com/pgbouncer/pgbouncer/pull/1108
[#1101]: https://github.com/pgbouncer/pgbouncer/pull/1101
[#1099]: https://github.com/pgbouncer/pgbouncer/pull/1099
[#1169]: https://github.com/pgbouncer/pgbouncer/pull/1169
[#1202]: https://github.com/pgbouncer/pgbouncer/pull/1202
[#1133]: https://github.com/pgbouncer/pgbouncer/pull/1133
[#1155]: https://github.com/pgbouncer/pgbouncer/pull/1155
[#1166]: https://github.com/pgbouncer/pgbouncer/pull/1166
[#298]: https://github.com/pgbouncer/pgbouncer/pull/298

--------

## PgBouncer 1.23.x {#pgbouncer-123x}

**2024-08-02  -  PgBouncer 1.23.1  -  «كل شيء أُعيد إلى نظامه»**

- الإصلاحات
  * إصلاح خطأ تجزئة (segmentation fault) محتمل بعد إعادة تحميل PgBouncer
    لتهيئته. ([#1105]) (عيب أُدخل في الإصدار 1.23.0)
  * إصلاح جميع انهيارات put_in_order المعروفة. ([#1120])
    (أُدخلت انهيارات جديدة في الإصدار 1.23.0)
  * إضافة الملفات الناقصة إلى أرشيف tar الخاص بالإصدار والمطلوبة للاختبار.
    ([#1124]) (أُدخلت الملفات الناقصة في الإصدار 1.23.0)

[#1120]: https://github.com/pgbouncer/pgbouncer/pull/1120
[#1105]: https://github.com/pgbouncer/pgbouncer/pull/1105
[#1124]: https://github.com/pgbouncer/pgbouncer/pull/1124

**2024-07-03  -  PgBouncer 1.23.0  -  «نحو بدايات جديدة»**

- الميزات
  * إضافة دعم إعادة التشغيل المتدرجة. لم يعد SIGTERM يسبب إيقافًا فوريًا
    لعملية PgBouncer. أصبح يجري الآن «إيقافًا فائق الأمان»:
    انتظار انقطاع اتصال جميع العملاء قبل الإيقاف. يسمح سلوك SIGTERM
    الجديد بإعادة تشغيل متدرجة لعدة عمليات PgBouncer خلف
    موازن حمل واحد، أو الاستماع على المنفذ نفسه باستخدام `so_reuseport`.
    هذا **تغيير كاسر بسيط**. إذا كنت تعتمد على السلوك القديم لـ
    SIGTERM في ملف Dockerfile أو ملف خدمة Systemd الخاص بك فينبغي عليك الآن استخدام SIGQUIT.
    ([#902])
  * إضافة دعم خرائط أسماء المستخدمين لطريقتي المصادقة `cert` و`peer`.
    توفر هذه الميزة مرونة كون المستخدم الذي يبدأ
    الاتصال ليس بالضرورة مستخدم قاعدة البيانات. دعم
    PgBouncer لخرائط أسماء المستخدمين يعمل بطريقة تشبه إلى حد كبير postgres مع الاستثناءات
    المذكورة في التوثيق. ([#996])
  * إضافة دعم اتصالات النسخ المماثل عبر PgBouncer. ([#876])

- التغييرات
  * تحسين ناتج `SHOW USERS` بإدراج الاتصالات. ([#1040])
  * السماح بتهيئة `pool_size` لكل مستخدم. ([#1049])
  * السماح بتهيئة `server_lifetime` لكل قاعدة بيانات. ([#1057])
  * إضافة دعم إدراج المستخدمين المنشأين ديناميكيًا في ناتج `SHOW USERS`. ([#1052])
  * إضافة دعم نوع العنوان `all` في تهيئة hba. ([#1078])
  * إضافة دعم إعادة التشغيل التلقائي عند استخدام systemd. ([#1080])
  * رفع الحد الأدنى المطلوب لإصدار c-ares إلى 1.9.0 ([#1076])

- الإصلاحات
  * إصلاح مشكلات التعامل مع حزم البدء الكبيرة والجزئية. ([#1058])
  * إضافة دعم صيغة `--config=value` في معامل بدء options. ([#1064])
  * إصلاح حساب مقياس `avg_wait_time`. ([#727])
  * إضافة دعم التفاوض على إصدار بروتوكول postgres مع العميل. ([#1007])
  * إضافة طلب قائم (outstanding) لأجل `auth_query`. ([#1034])
  * تحسينات متعددة على التوثيق وCI.

[#996]: https://github.com/pgbouncer/pgbouncer/pull/996
[#1040]: https://github.com/pgbouncer/pgbouncer/pull/1040
[#1049]: https://github.com/pgbouncer/pgbouncer/pull/1049
[#1057]: https://github.com/pgbouncer/pgbouncer/pull/1057
[#1052]: https://github.com/pgbouncer/pgbouncer/pull/1052
[#1058]: https://github.com/pgbouncer/pgbouncer/pull/1058
[#1007]: https://github.com/pgbouncer/pgbouncer/pull/1007
[#876]: https://github.com/pgbouncer/pgbouncer/pull/876
[#902]: https://github.com/pgbouncer/pgbouncer/pull/902
[#1064]: https://github.com/pgbouncer/pgbouncer/pull/1064
[#1078]: https://github.com/pgbouncer/pgbouncer/pull/1078
[#1080]: https://github.com/pgbouncer/pgbouncer/pull/1080
[#727]: https://github.com/pgbouncer/pgbouncer/pull/727
[#1076]: https://github.com/pgbouncer/pgbouncer/pull/1076
[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034

--------

## PgBouncer 1.22.x {#pgbouncer-122x}

**2024-03-04  -  PgBouncer 1.22.1  -  «إنه الصيف في بنغالور»**

- الإصلاحات
  * إصلاح مشكلات يسببها بعض العملاء الذين يستخدمون استعلامات `COPY FROM STDIN`. كانت مثل
    هذه الاستعلامات قادرة على إحداث تسريبات للذاكرة وتراجعات في الأداء وسلوك خاطئ للعبارات
    المعدة مسبقًا. ([#1025])
    (عيب أُدخل في الإصدار 1.21.0)
  * إضافة الاختبارات الناقصة إلى أرشيف tar الخاص بالإصدار ([#1026])
    (أُدخلت الاختبارات الناقصة في الإصدارين 1.19.0 و1.21.0)

[#1025]: https://github.com/pgbouncer/pgbouncer/pull/1025
[#1026]: https://github.com/pgbouncer/pgbouncer/pull/1026

**2024-01-31  -  PgBouncer 1.22.0  -  «DEALLOCATE ALL»**

- الميزات
  * إضافة دعم `DEALLOCATE ALL` و`DISCARD ALL` عندما
    تكون `max_prepared_statements` مضبوطة على قيمة غير صفرية (`DEALLOCATE`
    العادية ما تزال غير مدعومة) ([#972])
  * دعم تهيئة `auth_query` لكل قاعدة بيانات ([#979])

- التغييرات
  * تحسين الإعدادات في ملف وحدة systemd الموصى به ([#983])
  * جعل منطق الفشل السريع يغطي جميع السيناريوهات التي لم تعد فيها توجد اتصالات عاملة
    بقاعدة البيانات ولا يمكن إنشاء أي اتصال جديد ([#998])
  * تحسينات متعددة على التوثيق

- الإصلاحات
  * إصلاح مشكلة في PG14+ حيث كان PgBouncer يرسل `SET DateStyle='ISO'` مع
    كل معاملة ([#879])
  * إصلاح التعامل مع `application_name` الفارغ ([#999])
  * إصلاح البناء على Windows باستخدام OpenSSL 3.2.0 ([#1009])

[#972]: https://github.com/pgbouncer/pgbouncer/pull/972
[#979]: https://github.com/pgbouncer/pgbouncer/pull/979
[#983]: https://github.com/pgbouncer/pgbouncer/pull/983
[#998]: https://github.com/pgbouncer/pgbouncer/pull/998
[#879]: https://github.com/pgbouncer/pgbouncer/pull/879
[#999]: https://github.com/pgbouncer/pgbouncer/pull/999
[#1009]: https://github.com/pgbouncer/pgbouncer/pull/1009

--------

## PgBouncer 1.21.x {#pgbouncer-121x}

**2023-10-16  -  PgBouncer 1.21.0  -  «ذلك الإصدار بالعبارات المعدة مسبقًا»**

- الميزات
  * إضافة دعم العبارات المعدة مسبقًا المسماة على مستوى البروتوكول! هذه على الأرجح
    واحدة من أكثر الميزات طلبًا في PgBouncer. استخدام العبارات المعدة مسبقًا
    مع PgBouncer يمكن أن يقلل حمل CPU على نظامك كثيرًا (على جانب
    PgBouncer وعلى جانب PostgreSQL معًا). في الاختبارات المصطنعة
    كانت هذه الميزة قادرة على رفع معدل إنجاز الاستعلامات بنسبة تتراوح من 15% إلى
    250%، تبعًا لحمل العمل. للاستفادة من هذه الميزة الجديدة تحتاج إلى
    تغيير الإعداد الجديد `max_prepared_statements` إلى قيمة غير صفرية
    (القيمة الدقيقة تعتمد على حمل عملك، لكن 100 قيمة معقولة على الأرجح).
    راجع [وثائق
    `max_prepared_statements`](/ar/pgbouncer/config/#max_prepared_statements)
    لتفاصيل حول كيفية عمل الميزة وقيودها وكيفية ضبط
    القيمة. بعد ذلك عليك التأكد من أن مكتبة العميل لديك
    تستخدم العبارات المعدة مسبقًا فعلًا. تختلف طريقة ذلك من عميل لآخر،
    لذا ينبغي أن تراجع وثائق العميل الذي تستخدمه. اختُبرت هذه الميزة
    جيدًا قبل إصدارها، لكن مشكلات أداء أو
    عيوبًا قد تكون موجودة تمامًا نظرًا لتعقيد الميزة. إذا
    وجدت شيئًا من ذلك، فيُرجى الإبلاغ عنه. ([#845])

- التغييرات
  * تحسين أمن إعدادات OpenSSL، فالقيم الافتراضية المستخدمة كانت قديمة جدًا.
    مع هذا الإصدار أصبحت القيم الافتراضية الآن مطابقة لقيم OpenSSL الافتراضية على
    النظام الذي يشغّل PgBouncer. ([#948] & [libusual/#41])
  * أصبح PgBouncer الآن يستخدم OpenSSL لحساب تجزئات MD5 عندما يكون ذلك ممكنًا. هذا
    ضروري لاستخدام PgBouncer بطريقة متوافقة مع FIPS. ([#949])
  * صيانة `min_pool_size` للمجمّعات ذات المستخدم المُجبَر حتى لو لم يكن أي عملاء
    متصلين بـ PgBouncer ([#947])
  * تغيّرت الطريقة التي يرمّز بها PgBouncer نظيره `peer_id` في رمز الإلغاء،
    وهذا يعني أن التناظر بين إصدارات مختلفة من PgBouncer لن
    يعمل إذا لم تكن جميعها على الجانب نفسه من حدّ الإصدار
    v1.21.0. ([#945])

- الإصلاحات
  * إصلاح انهيار مع رسالة الخطأ: "FATAL in function client\_proto(): bad
    client state: 6/7" ([#928]) (عيب أُدخل في الإصدار 1.18.0)
  * إصلاح انهيار مع رسالة الخطأ: "FATAL in function server\_proto(): server in
    bad state: 11" ([#927]) (عيب أُدخل في الإصدار 1.18.0)
  * خفض مستوى تسجيل إرسال الإلغاء ([#903])
  * إصلاح بادئة سجل slog للنظراء ([#922])
  * إصلاح أخطاء إملائية في التوثيق ([#932])
  * إصلاح أخطاء أشار إليها المحلل الساكن ([#943])
  * عدم قتل جميع العملاء المنتظرين عند أخطاء FATAL مؤقتة أثناء تسجيل الدخول ([#946])
  * استخدام قاعدة البيانات التلقائية عندما لا تكون قاعدة البيانات في `auth_dbname` مضبوطة صراحةً
    ([#921])

- التنظيف
  * إزالة دعم udns ([#938])

[#845]: https://github.com/pgbouncer/pgbouncer/pull/845
[#948]: https://github.com/pgbouncer/pgbouncer/pull/948
[#949]: https://github.com/pgbouncer/pgbouncer/pull/949
[#947]: https://github.com/pgbouncer/pgbouncer/pull/947
[#945]: https://github.com/pgbouncer/pgbouncer/pull/945
[#903]: https://github.com/pgbouncer/pgbouncer/pull/903
[#922]: https://github.com/pgbouncer/pgbouncer/pull/922
[#932]: https://github.com/pgbouncer/pgbouncer/pull/932
[#928]: https://github.com/pgbouncer/pgbouncer/pull/928
[#927]: https://github.com/pgbouncer/pgbouncer/pull/927
[#943]: https://github.com/pgbouncer/pgbouncer/pull/943
[#946]: https://github.com/pgbouncer/pgbouncer/pull/946
[#921]: https://github.com/pgbouncer/pgbouncer/pull/921
[#938]: https://github.com/pgbouncer/pgbouncer/pull/938
[libusual/#41]: https://github.com/libusual/libusual/pull/41

--------

## PgBouncer 1.20.x {#pgbouncer-120x}

**2023-08-09  -  PgBouncer 1.20.1  -  «خيارات اختيارية»**

- الإصلاحات
  * إصلاح تراجع حيث لم يعد وضع `options` داخل `ignore_startup_parameters`
    يتجاهل المعاملات غير المعروفة داخل معامل بدء `options`
    بعد ذلك. ([#908]) (أُدخل التراجع في الإصدار 1.20.0)
  * إصلاح خطأ إملائي مربك في التوثيق ([#917])

[#908]: https://github.com/pgbouncer/pgbouncer/pull/908
[#917]: https://github.com/pgbouncer/pgbouncer/pull/917

**2023-07-20  -  PgBouncer 1.20.0  -  «يوضع هنا اسم طريف»**

- الإهمالات
  * أصبح خيار إعادة التشغيل المباشر الآن مهملًا. لم تحظَ الميزة
    باهتمام يُذكر في السنوات الأخيرة. توجد عدة مشكلات معروفة
    فيها وغالبًا ما لا تدعمها الميزات المضافة حديثًا. الطريقة الموصى
    بها لإجراء إعادة التشغيل المباشر هذه الأيام هي استخدام ميزتي `so_reuseport` و
    `peers`. بهذه الطريقة يمكنك تشغيل عدة عمليات PgBouncer
    مختلفة على المنفذ نفسه. ثم بإعادة تشغيل هذه العمليات
    واحدة تلو الأخرى، يمكنك التأكد من وجود عملية PgBouncer دائمًا تستمع
    على المنفذ المطلوب. ([#894])

- الميزات
  * تقديم `track_extra_parameters` الذي يسمح بتتبّع مزيد من
    المعاملات في وضع تجميع المعاملات. سابقًا، كان PgBouncer يتتبع فقط
    `application_name` و`DateStyle` و`TimeZone` و
    `standard_conforming_strings`. الآن يتتبع PgBouncer أيضًا `IntervalStyle`
    افتراضيًا. وبتغيير `track_extra_parameters` يمكنك تتبّع مزيد من
    الإعدادات أيضًا، ولكن فقط [الإعدادات التي يُبلغ عنها PostgreSQL إلى
    العميل][guc_report]. إذا كنت تستخدم Citus 12.0+، فسيتكفل Citus بأن
    يُبلغ PostgreSQL أيضًا عن `search_path` إلى العميل. لذا إذا كنت تستخدم
    Citus فيمكنك إضافة `search_path` إلى إعداد `track_extra_parameters`.
    ([#867])
  * تمرير SQLSTATE في مرحلة المصادقة. يتيح هذا اكتشاف عدم وجود
    قاعدة البيانات، وهو ما يقوم به Npgsql (مزود بيانات .NET لـ
    PostgreSQL). ([#814])
  * تغيير `server_tls_sslmode` الافتراضي إلى `prefer`. ([#866])
  * إضافة دعم معامل بدء `options`. يتيح هذا استخدام [متغير
    البيئة `PGOPTIONS` الذي يعرفه كل من `psql` و
    `libpq`][pgoptions]. باستخدام هذا المتغير يمكنك ضبط أي معامل PostgreSQL عند
    البدء. يعمل هذا فقط مع معاملات PostgreSQL التي يتتبعها PgBouncer
    عبر `track_extra_parameters`. ([#878])

- الإصلاحات
  * عدم الانهيار عند استخدام قاعدة بيانات `pgbouncer` الإدارية كـ auth_dbname. ما
    زالت غير مدعومة، لكن هذا يعطي الآن خطأً واضحًا بدلًا من الانهيار.
    ([#817])
  * إصلاح اسم `peer_cache` في `SHOW MEM`. كانت تظهر خطأً بالاسم
    `db_cache` قبل ذلك. ([#864])
  * إصلاح الالتباس بين src/dst في السجل. كان PgBouncer يسجل عنوان IP مصدر عندما
    كان يقصد تسجيل عنوان IP الوجهة. ([#880])
  * تسجيل اتصالات الإدارة عبر مقابس unix فقط عندما يكون `log_connections` مضبوطًا
    على `1`. ([#883])

[guc_report]: https://www.postgresql.org/docs/15/protocol-flow.html#PROTOCOL-ASYNC
[pgoptions]: https://www.postgresql.org/docs/current/config-setting.html#id-1.6.7.4.5
[#867]: https://github.com/pgbouncer/pgbouncer/pull/867
[#814]: https://github.com/pgbouncer/pgbouncer/pull/814
[#866]: https://github.com/pgbouncer/pgbouncer/pull/866
[#878]: https://github.com/pgbouncer/pgbouncer/pull/878
[#817]: https://github.com/pgbouncer/pgbouncer/pull/817
[#864]: https://github.com/pgbouncer/pgbouncer/pull/864
[#880]: https://github.com/pgbouncer/pgbouncer/pull/880
[#883]: https://github.com/pgbouncer/pgbouncer/pull/883
[#894]: https://github.com/pgbouncer/pgbouncer/pull/894

--------

## PgBouncer 1.19.x {#pgbouncer-119x}

**2023-05-31  -  PgBouncer 1.19.1  -  «ربيع مشمس»**

هذا إصدار ثانوي يصلح بعض العيوب أُدخلت حديثًا:

- الإصلاحات
  * إصلاح: FATAL in function disconnect_client(): bad client state: 0 ([#846])
    (عيب أُدخل في الإصدار 1.18.0)
  * إصلاح: FATAL in function server_proto(): server in bad state: 14 ([#849])
    (عيب أُدخل في الإصدار 1.18.0)
  * إضافة الملفات المطلوبة لتشغيل الاختبارات المبنية على python إلى أرشيف tar الخاص بالإصدار ([#852])
    (أُدخلت اختبارات جديدة في الإصدار 1.19.0)

[#846]: https://github.com/pgbouncer/pgbouncer/pull/846
[#849]: https://github.com/pgbouncer/pgbouncer/pull/849
[#852]: https://github.com/pgbouncer/pgbouncer/pull/852

**2023-05-04  -  PgBouncer 1.19.0  -  «النوع التقليدي المولَّد بشريًا»**

- الميزات
  * إضافة خيار `auth_dbname`، الذي يحدد قاعدة البيانات التي سيُشغَّل عليها
    `auth_query`. ([#764])
  * إضافة الأمر `SHOW STATE`، الذي يُظهر هل PgBouncer نشط أم
    متوقف مؤقتًا أم معلّق. ([#528])
  * إضافة دعم التناظر بين عمليات PgBouncer. يتيح هذا
    تهيئة PgBouncer بحيث تواصل طلبات الإلغاء
    العمل عندما توجد عدة عمليات PgBouncer مختلفة خلف
    موازن حمل واحد. ([#666])
  * إضافة إعداد مخصص `cancel_wait_timeout`، الذي يحدد
    بعد كم من الوقت التوقف عن محاولة تمرير طلب إلغاء. القيمة الافتراضية
    هي 10 ثوانٍ. ([#833])
  * إطار عمل اختبار جديد ([#792])

- الإصلاحات
  * إصلاح تسريب محتمل للذاكرة عند فشل مصافحة TLS. ([#796])
  * إعطاء رسائل خطأ أدق لخيارات سطر الأوامر غير المدعومة
    على Windows. ([#620])
  * إصلاح استدعاء `disconnect_server` على خادم في حالة `BEING_CANCELED`
    . ([#815]) (أُدخل في الإصدار 1.18.0)
  * عدم الخروج بحالة غير صفرية عند استلام
    `SIGTERM`. ([#834])
  * الفشل الصريح أثناء البدء عندما تعذر إنشاء مقبس في
    `unix_socket_dir`. ([#830])
  * الفشل الصريح أثناء البدء عندما تعذر الاستماع على أي من العناوين في
    `listen_addr`. ([#838])
  * إعطاء رسائل تحذير أكثر وذات معلومات أكثر عند فشل
    `sbuf_connect`. هذا مفيد بشكل خاص عند الفشل في
    إنشاء مقابس Unix. ([#837])

- أعمال التنظيف
  * تحديثات متنوعة على CI لأداء أفضل
  * إزالة AppVeyor

[#528]: https://github.com/pgbouncer/pgbouncer/issues/528
[#620]: https://github.com/pgbouncer/pgbouncer/pull/620
[#666]: https://github.com/pgbouncer/pgbouncer/pull/666
[#764]: https://github.com/pgbouncer/pgbouncer/pull/764
[#792]: https://github.com/pgbouncer/pgbouncer/pull/792
[#796]: https://github.com/pgbouncer/pgbouncer/pull/796
[#815]: https://github.com/pgbouncer/pgbouncer/pull/815
[#830]: https://github.com/pgbouncer/pgbouncer/pull/830
[#833]: https://github.com/pgbouncer/pgbouncer/pull/833
[#834]: https://github.com/pgbouncer/pgbouncer/pull/834
[#837]: https://github.com/pgbouncer/pgbouncer/pull/837
[#838]: https://github.com/pgbouncer/pgbouncer/pull/838

--------

## PgBouncer 1.18.x {#pgbouncer-118x}

**2022-12-12  -  PgBouncer 1.18.0  -  «بلا لغز حقيقي»**

- الميزات
  * إضافة `application_name` إلى ناتج `SHOW CLIENTS`/`SERVERS`/`SOCKETS`
    ([#449](https://github.com/pgbouncer/pgbouncer/pull/449))
  * إضافة معلومات عن طلبات الإلغاء إلى ناتج `SHOW CLIENTS`/`SERVERS`/`POOLS`
    ([#782](https://github.com/pgbouncer/pgbouncer/pull/782))

- الإصلاحات
  * إفشال عملية `sbuf_send_pending` إذا كان مقبس الوجهة مغلقًا
    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))
  * إصلاح بعض الانهيارات المحتملة
    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),
    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))
  * إصلاح عيب تجاوز في ميزة قائمة المضيفين المفصولة بفواصل، كان يسبب
    إعادة توجيه الاتصال إلى مقبس Unix
    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))
  * عدم إخلاء الاتصالات لتحقيق `min_pool_size`
    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))
  * إصلاح `SHOW HELP` مع PostgreSQL 15
    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))
  * إصلاح حالة تسابق في التعامل مع إلغاء الاستعلام. كان من الممكن
    أن يُلغي إلغاءُ استعلامٍ لعميل واحد استعلامًا لعميل
    آخر. كان هذا يمكن أن يحدث عندما يستلم
    PgBouncer طلب إلغاء بينما كان الاستعلام المقصود إلغاؤه قد اكتمل
    من تلقاء نفسه بالفعل.
    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))

- أعمال التنظيف
  * تحديثات متنوعة على CI

--------

## PgBouncer 1.17.x {#pgbouncer-117x}

**2022-03-23  -  PgBouncer 1.17.0  -  «لقد رُسم خط»**

- الميزات
  * يمكن لتعريف قاعدة البيانات أن يحدد قائمة مضيفين مفصولة بفواصل.
    سيجري الاتصال بالمضيفين بطريقة التناوب الدائري (round-robin).
  * عند الاتصال بقاعدة بيانات غير موجودة، يُبلغ الآن عن الخطأ ("no such
    database") بعد المصادقة. يمنع هذا
    العملاء غير المُصادَق عليهم من استكشاف قواعد البيانات الموجودة. (هذا
    مشابه للتغيير في الإصدار 1.15.0 للإبلاغ عن المستخدمين
    المفقودين بعد المصادقة.)
  * عدم إرسال أخطاء قطع اتصال الخادم إلى العميل قبل تسجيل الدخول.
    كان هذا قد يكشف معلومات ليست علنية تمامًا، مثل
    تفاصيل التهيئة، لعميل لم يسجل الدخول بعد.
  * زيادة الطول الأقصى لكلمة المرور مجددًا. على ما يبدو، الزيادة
    السابقة لم تظل كافية مدة طويلة.
  * إزالة إعادة التحميل التلقائية لـ `auth_file`. يعاد الآن قراءة
    `auth_file` فقط عند إعادة تحميل ملف التهيئة، لا تلقائيًا
    بمجرد تغييره.
  * يتضمن بناء Windows الآن ملف مورد
    لمعلومات الإصدار.
  * أصبحت عمليات البناء لـ Windows المنشأة على CI مرتبطة بشكل ساكن، بحيث
    يمكن استخدامها مباشرة دون الحاجة إلى أي تبعيات.

- الإصلاحات
  * أُصلح دعم OpenSSL 3. كانت الإصدارات السابقة تنهار.
  * عدم تطبيق الفشل السريع وقت الاتصال. هذا جزء من
    التغيير المذكور أعلاه بعدم الإبلاغ عن أخطاء الخادم قبل
    المصادقة. وهو يصلح أيضًا حالة معينة في مصادقة SCRAM
    بالتمرير، حيث نحتاج إلى السماح بتبادل
    المصادقة من جانب العميل حتى نتمكن من إصلاح اتصال
    جانب الخادم بإعادة المصادقة. ما يزال مبدأ الفشل
    السريع مطبقًا بعد المصادقة مباشرة، لذا سيكون السلوك
    الفعلي الملاحَظ نفسه في معظم الحالات.
  * تغيير `auth_type` في ملف `pgbouncer.ini` النموذجي إلى `md5` بما يطابق
    الافتراضي المدمج. ينشر البعض هذا الملف بوصفه ملف التهيئة
    الافتراضي، لذا تحقق إن كانت هذه التهيئة المتغيرة ما تزال
    مناسبة لك.
  * إصلاح انهيار عند الخروج في إصدارات البناء التي تُفعَّل فيها فحوصات assert.
  * تحسين توثيق `tcp_defer_accept` وسلوكه. كان
    التوثيق غير صحيح ومضللًا بخصوص القيمة الافتراضية. في
    بعض الحالات كانت القيمة الخاطئة تظهر في "show config". أيضًا، إذا
    كان مضبوطًا لكنه غير مدعوم، فإعطاء خطأ بدلًا من التجاهل،
    بشكل مشابه للطريقة التي تُعالَج بها خيارات المقابس الأخرى الخاصة بالمنصة.
  * إصلاح البناء باستخدام c-ares على Windows. أصبح c-ares >=1.18.0
    مطلوبًا الآن على Windows.

- أعمال التنظيف
  * نُظفت معظم تحذيرات الإهمال الصادرة من Autoconf >=2.70. ما تزال
    إصدارات Autoconf الأقدم مدعومة.
  * وُسّع استخدام Cirrus CI ليشمل مزيدًا من المنصات.
  * أُزيل دعم Travis CI.
  * تحديث المواقع التي يُبحث فيها عن ملف شهادات الجذر الافتراضي، لتغطية مزيد من
    المنصات، مثل Fedora/RHEL/CentOS.
  * تستخدم سكربتات Python الآن جميعها `python3` افتراضيًا. لم تعد
    التوافقية مع Python 2 تُصان.
  * تستخدم سكربتات مجموعة الاختبار `command -v` بدلًا من `which` وهي
    مهملة.
  * أُعيدت صياغة عدة رسائل خطأ لتوضيح الأمر أو
    إعداد التهيئة الذي تتعلق به.
  * لم تعد سكربتات مجموعة الاختبار تتطلب GNU sed.
  * يعمل `make check` الآن على Windows (لكن ليس مجموعة اختبار SSL
    بعد).
  * توثيق أن وحدة تحكم الإدارة تدعم بروتوكول الاستعلام البسيط فقط،
    وإعطاء رسائل خطأ أفضل بخصوص ذلك.

--------

## PgBouncer 1.16.x {#pgbouncer-116x}

**2021-11-11  -  PgBouncer 1.16.1  -  «اختبار العمق في مواجهة الكفاءة الهادئة»**

هذا إصدار ثانوي بإصلاح أمني.

* جعل PgBouncer العامل كخادم يرفض البيانات الزائدة بعد مصافحة تشفير
  SSL أو GSS.

  يستطيع رجل في المنتصف يملك القدرة على حقن بيانات في اتصال TCP
  حشوَ بعض البيانات غير المشفرة في بداية جلسة قاعدة بيانات يُفترض أنها
  محمية بالتشفير. كان يمكن إساءة استخدام ذلك لإرسال أوامر SQL مزيفة
  إلى الخادم،
  رغم أن ذلك لن ينجح إلا إذا لم يطلب PgBouncer أي بيانات مصادقة.
  (مع ذلك، فقد لا يطلب تجهيز PgBouncer المعتمد على مصادقة
  شهادات SSL ذلك.) (CVE-2021-3935)

**2021-08-09  -  PgBouncer 1.16.0  -  «صدَّ جاكوارًا»**

- الميزات
  * دعم إعادة التحميل الفوري لإعدادات TLS. عند إعادة تحميل ملف
    التهيئة، تدخل إعدادات TLS المتغيرة حيز التنفيذ تلقائيًا.
  * إضافة دعم مقابس Unix المجردة. سابق مسار مقبس Unix
    بـ `@` لاستخدام مقبس في النطاق المجرد. يتوافق هذا مع ميزة PostgreSQL 14
    المقابلة.
  * زيدت الأطوال القصوى لكلمات المرور وأسماء المستخدمين إلى 996 و
    128 على التوالي. تتطلب ذلك خدمات سحابية
    مختلفة.
  * يمكن الآن ضبط الحد الأدنى لحجم المجمّع لكل قاعدة بيانات، بشكل مشابه لحجم
    المجمّع العادي وحجم المجمّع الاحتياطي.
  * يظهر عدد عمليات إلغاء الاستعلام المعلقة في `SHOW
    POOLS`.

- الإصلاحات
  * أصبح تحليل التهيئة الآن أشد صرامة في التعامل مع الأخطاء في مواضع
    كثيرة. حيث كان سابقًا قد يسجل خطأً ويمضي، أصبحت أخطاء التهيئة
    تلك الآن
    تؤدي إلى إخفاقات في البدء. هذا ما كان يجب أن يحدث دائمًا، لكن بعض
    الشيفرة لم تفعل ذلك بشكل صحيح. قد يكتشف بعض المستخدمين أن تهيئاتهم
    كانت معيبة طوال الوقت ولن تعمل
    بعد الآن.
  * أُصلح التعامل مع إلغاء الاستعلام. في بعض الظروف، كانت
    طلبات الإلغاء تبدو عالقة لفترة طويلة. لم يعد
    ينبغي أن يحدث هذا. في الواقع، يمكن لطلبات الإلغاء الآن
    أن تتجاوز حجم المجمّع بمعامل اثنين، لذا فهي حقًا لا ينبغي
    أن تتعطل
    بعد الآن. ([#542](https://github.com/pgbouncer/pgbouncer/pull/542),
    [#543](https://github.com/pgbouncer/pgbouncer/pull/543))
  * أُصلح الاستخدام المختلط لـ md5 وscram عبر hba.
  * أُصلح البناء باستخدام c-ares على Windows.
  * أُصلحت رسائل "FIXME: query end, but query_start == 0" المخيفة. نعرف
    الآن لماذا تحدث، ولا ينبغي أن تراها
    بعد الآن. ([#565](https://github.com/pgbouncer/pgbouncer/pull/565))
  * إصلاح إعادة تحميل `default_pool_size` و`min_pool_size` و
    `reserve_pool_size`. لم تكن إعادة تحميل هذه الإعدادات تعمل سابقًا.

- أعمال التنظيف
  * أصبح Cirrus CI الآن
    [مستخدمًا](https://cirrus-ci.com/github/pgbouncer/pgbouncer) بدلًا
    من Travis CI.
  * كالعادة، أُضيف العديد من الاختبارات.
  * وُضّحت رسالة السجل "unclean server" قليلًا. تقول الآن
    "client disconnect while server was not ready" أو "client
    disconnect before everything was sent to the server". يمكن للأولى
    أن تحدث إذا أُغلق اتصال العميل بينما لدى الخادم
    كتلة معاملة مفتوحة، مما أربك بعض المستخدمين.
  * لم يعد بإمكانك استخدام "pgbouncer" كاسم لقاعدة بيانات. هذا الاسم
    محفوظ لوحدة تحكم الإدارة، واستخدامه كاسم لقاعدة بيانات
    عادية لم يعمل بشكل صحيح قط. أصبح هذا محظورًا
    الآن بشكل صريح.
  * أصبحت الأخطاء المرسلة إلى العملاء قبل إغلاق الاتصال الآن
    موسومة بوصف FATAL بدلًا من ERROR فقط. كان بعض العملاء
    يتشوشون
    لولا ذلك. ([#564](https://github.com/pgbouncer/pgbouncer/pull/564))
  * إصلاح تحذيرات المُصرِّف مع GCC 11.
    ([#623](https://github.com/pgbouncer/pgbouncer/issues/623))

--------

## PgBouncer 1.15.x {#pgbouncer-115x}

**2020-11-19  -  PgBouncer 1.15.0  -  «Ich hab noch einen Koffer in Berlin (ما زالت لديّ حقيبة في برلين)»**

- الميزات
  * تحسين الإبلاغ عن إخفاق المصادقة. رسائل إخفاق المصادقة
    المرسلة إلى العميل تكتفي الآن بالقول إن المصادقة
    فشلت دون تقديم أي تفاصيل أخرى. التفاصيل متاحة
    في سجل PgBouncer. أيضًا، إذا كان المستخدم المطلوب
    غير موجود، تُعالَج المصادقة حتى النهاية وستؤدي
    إلى الرسالة العامة نفسها للفشل. كل هذا يمنع
    العملاء من استكشاف نسخة PgBouncer بحثًا عن
    أسماء المستخدمين وغير ذلك من المعلومات المتعلقة
    بالمصادقة. هذا مشابه لسلوك PostgreSQL.
  * عدم تسجيل أي شيء إذا انقطع اتصال العميل فورًا. يتجنب
    هذا إغراق السجل عندما تفتح أنظمة المراقبة اتصال
    TCP/IP لكنها لا ترسل شيئًا قبل قطع الاتصال.
  * استخدام يومية systemd للتسجيل عندما تكون قيد الاستخدام.
    عندما نكتشف أن stderr يذهب إلى يومية systemd، نستخدم
    دوال systemd الأصلية لناتج السجل. يتجنب هذا طباعة
    الطابع الزمني وpid المكررين، وبذلك يصبح السجل
    أنظف قليلًا. أيضًا، يضيف هذا بيانات وصفية مثل درجة
    الخطورة إلى السجلات، بحيث إذا أُرسلت اليومية
    إلى syslog، تحمل الرسائل بيانات وصفية مفيدة.
  * يمكن الآن تشغيل مجموعة فرعية من مجموعة الاختبار على Windows.
  * يعرض `SHOW CONFIG` الآن أيضًا القيم الافتراضية للإعدادات.

- الإصلاحات
  * إصلاح خيار `so_reuseport` على FreeBSD. الشيفرة الأصلية
    في PgBouncer 1.12.0 لم تكن تعمل فعلًا على FreeBSD.
    ([#504](https://github.com/pgbouncer/pgbouncer/pull/504))
  * إصلاح البناء على الأنظمة ذات إصدارات systemd الأقدم.
    كان هذا معطوبًا في الإصدار 1.14.0.
    ([#505](https://github.com/pgbouncer/pgbouncer/issues/505))
  * أُصلح هدف makefile لبناء حزم
    zip لملفات Windows الثنائية.
  * تعمل خيارات سطر الأوامر الطويلة الآن أيضًا على Windows.
  * إصلاح سلوك الإعداد العالمي `auth_user`. كان السلوك
    القديم مربكًا وهشًا لأنه كان يعتمد على الترتيب في
    ملف التهيئة. لم يعد هذا هو الحال.
    ([#391](https://github.com/pgbouncer/pgbouncer/issues/391),
    [#393](https://github.com/pgbouncer/pgbouncer/issues/393))

- أعمال التنظيف
  * تحسين استقرار الاختبارات وقابليتها للنقل.
  * تحديث الشيفرة المتعلقة بـ Autoconf.
  * تعطيل تحذيرات إهمال المُصرِّف الصادرة من OpenSSL 3.0.0.

--------

## PgBouncer 1.14.x {#pgbouncer-114x}

**2020-06-11  -  PgBouncer 1.14.0  -  «La ritrovata magia (السحر المستعاد)»**

- الميزات
  * إضافة تمرير مصادقة SCRAM. يتيح هذا استخدام أسرار
    SCRAM مشفرة في PgBouncer (سواء في `userlist.txt`
    أو من `auth_query`) لتسجيل الدخول إلى الخوادم.
  * إضافة دعم تنشيط مقابس systemd. هذا مفيد
    بشكل خاص لترك systemd يتولى إنشاء مقابس
    Unix على الأنظمة التي يكون فيها الوصول
    إلى `/var/run/postgresql` مقيدًا.
  * إضافة دعم مقابس Unix على Windows.

- أعمال التنظيف
  * إضافة ملف تهيئة نموذجي أصغر بديل هو `pgbouncer-minimal.ini`
    للاختبار أو النشر.

--------

## PgBouncer 1.13.x {#pgbouncer-113x}

**2020-04-27  -  PgBouncer 1.13.0  -  «لعبتي المفضلة»**

- الميزات
  * إضافة إعداد التهيئة `tcp_user_timeout`،
    لضبط خيار المقبس المقابل.
  * أصبح الافتراضي لـ `client_tls_protocols` و`server_tls_protocols`
    الآن `secure`، ما يعني تمكين TLS 1.2 وTLS
    1.3 فقط. ما تزال الإصدارات الأقدم مدعومة،
    لكنها فقط غير مفعّلة بشكل افتراضي.
  * إضافة دعم إشعارات خدمة systemd. حاليًا، يتيح
    هذا استخدام وحدات الخدمة `Type=notify`. المزيد
    من التكامل مخطط له للإصدارات المستقبلية.

- الإصلاحات
  * إصلاح رسائل السجل متعددة الأسطر ([libusual
    #24](https://github.com/libusual/libusual/pull/24))
  * التعامل بشكل صحيح مع أسماء المستخدمين NULL المعادة من `auth_query`
    ([#340](https://github.com/pgbouncer/pgbouncer/pull/340))

- أعمال التنظيف
  * أُزيلت ملفات تهيئة حزمة Debian الموجودة تحت `debian`.
    يُنصح باستخدام الحزم من https://apt.postgresql.org/.
  * إصلاحات وتحسينات عديدة في مجموعة الاختبار
  * لم تعد الاختبارات تحاول استخدام sudo
    افتراضيًا. يمكن الآن تنشيط ذلك صراحةً
    بضبط متغير البيئة `USE_SUDO`.
  * حُدّث استخدام واجهة برمجة libevent لاستخدام واجهات النمط إصدار
    2 وعدم استخدام الواجهات المهملة من الإصدار 1 بعد الآن.

--------

## PgBouncer 1.12.x {#pgbouncer-112x}

**2019-10-17  -  PgBouncer 1.12.0  -  «الأمر يتعلق بالتعلم والتحسن»**

يحتوي هذا الإصدار على مجموعة متنوعة من التحسينات والإصلاحات الثانوية.

- الميزات
  * إضافة إعداد لتمكين خيار المقبس `SO_REUSEPORT`.
    على بعض أنظمة التشغيل، يتيح هذا تشغيل عدة نسخ
    من PgBouncer على المضيف نفسه تستمع على المنفذ
    نفسه وأن يوزع النواة الاتصالات تلقائيًا.
  * إضافة إعداد لاستخدام ملف `resolv.conf`
    منفصل عن نظام التشغيل. يتيح هذا ضبط خوادم
    DNS مخصصة وربما خيارات DNS أخرى.
  * إرسال ناتج `SHOW VERSION` كصف نتيجة عادي
    بدلًا من رسالة NOTICE. يسهّل هذا استهلاكه
    ويجعله متسقًا مع أوامر `SHOW` الأخرى.

- الإصلاحات
  * إرسال أعمدة الإحصاءات بنوع `numeric` بدلًا من `bigint`.
    يتجنب هذا فشل بعض مكتبات العملاء مع القيم التي
    تتجاوز نطاق `bigint`.
    ([#360](https://github.com/pgbouncer/pgbouncer/pull/360),
    [#401](https://github.com/pgbouncer/pgbouncer/pull/401))
  * إصلاح مشكلة فقدان مستخدمي PAM لكلمة المرور.
    ([#285](https://github.com/pgbouncer/pgbouncer/issues/285))
  * قبول العملاء الذين مكّنوا SCRAM channel binding.
    سابقًا، كان العميل الداعم لربط القناة (أي PostgreSQL
    11+) سيحصل على فشل اتصال عند الاتصال بـ PgBouncer
    في ظروف معينة. (لا يدعم PgBouncer ربط القناة. هذا
    التغيير يصلح فقط دعم العملاء الذين يقدمونه.)
  * إصلاح البناء مع الإصدارات الأحدث من musl-libc
    (التي تستخدمها Alpine Linux).

- أعمال التنظيف
  * إضافة هدف `make check`. يتيح هذا تشغيل
    جميع الاختبارات من أمر واحد.
  * إزالة الإشارات إلى ويكي PostgreSQL. جميع المعلومات الآن
    إما في توثيق PgBouncer أو على الموقع الإلكتروني.
  * إزالة دعم Libevent الإصدار 1.x. أصبح Libevent 2.x مطلوبًا
    الآن. يُكتشف Libevent الآن باستخدام pkg-config.
  * إصلاح تحذيرات المُصرِّف على macOS وWindows. ينبغي أن
    يكون البناء على هذه المنصات الآن خاليًا من التحذيرات.
  * إصلاح بعض التحذيرات الصادرة من LLVM scan-build.

--------

## PgBouncer 1.11.x {#pgbouncer-111x}

**2019-08-27  -  PgBouncer 1.11.0  -  «غريزة نحو العظمة»**

- الميزات
  * إضافة دعم مصادقة SCRAM للعملاء والخوادم. تُضاف
    طريقة مصادقة جديدة هي `scram-sha-256`.
  * التعامل مع `auth_type=password` عندما تكون كلمة المرور
    المخزنة بنمط md5، كما يفعل خادم PostgreSQL.
    ([#129](https://github.com/pgbouncer/pgbouncer/pull/129))
  * إضافة الخيار `log_stats` لتعطيل طباعة الإحصاءات إلى السجل.
    ([#287](https://github.com/pgbouncer/pgbouncer/pull/287))
  * إضافة المنطقة الزمنية إلى طوابع السجل الزمنية.
  * وضع PID داخل [أقواس] في بادئة السجل.
- الإصلاحات
  * إصلاح اختبار تهيئة OpenSSL عند التشغيل
    مقابل OpenSSL أحدث مع `-Werror`.
  * إصلاح حساب زمن الانتظار مع `auth_user`. كان هذا إما يسبب
    انهيارًا أو يبلغ عن قيم مهملة لزمن الانتظار.
    ([#393](https://github.com/pgbouncer/pgbouncer/pull/393))
  * التعامل مع حزمة GSSENCRequest، التي أُضيفت في
    PostgreSQL 12. لا تفعل شيئًا حاليًا، لكنها تتجنب
    رسائل خطأ مربكة حول "bad packet header".
- أعمال التنظيف
  * تحسينات كثيرة في مجموعة الاختبار وعدة اختبارات جديدة
  * إصلاح عدة تحذيرات للمُصرِّف على Windows.
  * توسيع توثيق قسم `[users]` وإضافته إلى ملف
    التهيئة النموذجي.
    ([#330](https://github.com/pgbouncer/pgbouncer/pull/330))

--------

## PgBouncer 1.10.x {#pgbouncer-110x}

**2019-07-01  -  PgBouncer 1.10.0  -  «خائف من العالم»**

- الميزات
  * إضافة دعم تمكين وتعطيل TLS 1.3. (كان TLS
    1.3 مدعومًا بالفعل، تبعًا لمكتبة OpenSSL،
    لكن إعدادات التهيئة لاختيار إصدارات بروتوكول
    TLS أصبحت أيضًا تدعمه الآن.)
- الإصلاحات
  * إصلاح دعم TLS 1.3. كان معطوبًا مع OpenSSL
    1.1.1 و1.1.1a (لكن ليس قبلها أو بعدها).
  * إصلاح انهيار نادر في `SHOW FDS`
    ([#311](https://github.com/pgbouncer/pgbouncer/issues/311)).
  * إصلاح مشكلة كانت قد تؤدي إلى توقف طويل إذا وصلت
    أعداد كبيرة من طلبات الإلغاء
    ([#329](https://github.com/pgbouncer/pgbouncer/issues/329)).
  * تجنب "unexpected response from login query"
    بعد إعادة تحميل postgres
    ([#220](https://github.com/pgbouncer/pgbouncer/issues/220)).
  * إصلاح حساب `idle_transaction_timeout` ([#125](https://github.com/pgbouncer/pgbouncer/issues/125)).
    كان العيب قد يؤدي إلى انتهاء
    مهلات مبكرة في مواقف محددة.
- أعمال التنظيف
  * جعل رسائل السجل والخطأ المختلفة أدق.
  * إصلاح مشكلات اكتشفها Coverity (لم يكن
    لأي منها أثر كبير في الممارسة).
  * تحسين جميع سكربتات الاختبار وتوثيقها.
  * إضافة أوامر SHOW إضافية إلى التوثيق.
  * تحويل التوثيق من rst إلى Markdown.
  * سكربتات Python في الشجرة المصدرية
    متوافقة جميعها مع Python 3 الآن.

--------

## PgBouncer 1.9.x {#pgbouncer-19x}

**2018-08-13  -  PgBouncer 1.9.0  -  «النجاة من الفوضى»**

- الميزات
  * أمر RECONNECT
  * أمر WAIT_CLOSE
  * الإغلاق السريع - قطع اتصال خادم في وضع تجميع الجلسات
    فورًا إذا كان في وضع "close_needed" (إعادة الاتصال).
  * إضافة عمود close_needed إلى SHOW SERVERS
- الإصلاحات
  * تجنب double-free في parse_filename
  * تجنب فكّ إشارة مؤشر NULL في parse_line
- أعمال التنظيف
  * نقل mkauth.py إلى Python 3
  * تحسين توثيق الإشارات (signals)
  * تحسين توثيق البدء السريع
  * توثيق أمر SET
  * تصحيح قائمة البرمجيات المطلوبة
  * إصلاح تحذيرات -Wimplicit-fallthrough
  * إضافة التوثيق الناقص لحقول SHOW متنوعة
  * توثيق سلوك إعادة الاتصال عند إعادة التحميل وتغيّر DNS
  * توثيق أن KILL يتطلب RESUME بعده
  * توضيح توثيق server_lifetime
  * إصلاحات إملائية وتصحيح حالة الأحرف في الرسائل والتوثيق
  * إصلاح استدعاء psql في الاختبارات
  * تحسينات متنوعة أخرى على إعداد الاختبارات

--------

## PgBouncer 1.8.x {#pgbouncer-18x}

**2017-12-20  -  PgBouncer 1.8.1  -  «عقلية الإسقاط والضرب الأرضي»**

- الإصلاحات
  * تضمين الملف `include/pam.h` في أرشيف tar الخاص بالتوزيع.
    كان هذا يمنع أرشيف 1.8 من البناء أصلًا.

**2017-12-19  -  PgBouncer 1.8  -  «واثق من الدفة»**

- الميزات
  * دعم مصادقة PAM. (مكّنها باستخدام `--with-pam`.)
  * إضافة الحقلين `paused` و`disabled` إلى ناتج `SHOW DATABASES`.
  * إضافة الحقل `maxwait_us` إلى ناتج `SHOW POOLS`.
  * إضافة الحقلين `wait` و`wait_us` إلى ناتج أوامر `SHOW`.
  * إضافة الأمرين الجديدين `SHOW STATS_TOTALS` و`SHOW STATS_AVERAGES`.
  * تتبّع الاستعلامات والمعاملات بشكل منفصل في
    `SHOW STATS`. حلّت الحقول `total_requests`
    و`avg_req` و`avg_query` محلها حقول جديدة.
  * إضافة `wait_time` إلى `SHOW STATS`.
- الإصلاحات
  * libusual المحدّث يدعم OpenSSL 1.1.
  * عدم محاولة استخدام TLS على مقابس Unix.
  * عند تحليل `pg_hba.conf`، مواصلة التحليل بعد الأسطر الخاطئة بدلًا من رفض الملف
    بأكمله. ([#118](https://github.com/pgbouncer/pgbouncer/issues/118))
  * عدة إصلاحات أخرى لتحليل hba.
  * إصلاح حالة تسابق عند إلغاء استعلام.
    ([#141](https://github.com/pgbouncer/pgbouncer/issues/141))
- أعمال التنظيف
  * أصبح إعداد `auth_user` مسموحًا به الآن أيضًا عالميًا، لا لكل قاعدة بيانات
    فقط. ([#142](https://github.com/pgbouncer/pgbouncer/issues/142))
  * ضبط ترميز عميل وحدة التحكم وخادمها على `UTF8`.

--------

## PgBouncer 1.7.x {#pgbouncer-17x}

**2016-02-26  -  PgBouncer 1.7.2  -  «أخيرًا في الجو»**

- الإصلاحات
  * إصلاح انهيار عند إزالة ملف pid قديم. أُدخلت المشكلة في الإصدار 1.7.1.
  * تعطيل التنظيف - فهو يعطّل الاستحواذ وليس مفيدًا للأحمال
    الإنتاجية. أُدخلت المشكلة في الإصدار 1.7.1.
  * بعد الاستحواذ، الانتظار حتى يختفي ملف pid قبل الإقلاع. كشف
    الإيقاف البطيء بسبب تنظيف الذاكرة حالة تسابق موجودة.
    ([#113](https://github.com/pgbouncer/pgbouncer/issues/113))
- أعمال التنظيف
  * جعل البناء قابلًا لإعادة الإنتاج بالتخلي عن معالجة DBGVER.
    ([#112](https://github.com/pgbouncer/pgbouncer/issues/112))
  * Antimake: فرز قائمة الملفات من $(wildcard)، فإن
    gmake الأحدث لا يفرزها بعد الآن.
    ([#111](https://github.com/pgbouncer/pgbouncer/issues/111))
  * عرض إصدار libssl في السجل.
  * deb: تمكين التحصين الكامل.

**2016-02-18  -  PgBouncer 1.7.1  -  «أرسلها إلى خمسة أصدقاء وإلا...»**

تحذير: منذ الإصدار 1.7، لا يُنفَّذ `server_reset_query` عندما
تكون قاعدة البيانات في وضع تجميع المعاملات. يبدو أن هذا لم يُبرَز
بما يكفي في إعلان 1.7. إذا كانت تطبيقاتك تعتمد على حدوث ذلك،
فاستخدم `server_reset_query_always` لاستعادة السلوك السابق.

وإلا فقد كان العمل الرئيسي في هذا الإصدار هو تعقّب تسريب ذاكرة
متعلق بـ TLS، الذي تبيّن أنه غير موجود. وبدلًا من ذلك هناك بناء
libssl في Debian/wheezy يستهلك 600k لكل اتصال (دون تسريب) بدلًا
من 20-30k المتوقعة. أمر يستحق الانتباه عند استخدام TLS.

- الإصلاحات
  * TLS: إعادة تسمية sslmode من "disabled" إلى
    "disable" لأن هذا ما يستخدمه PostgreSQL.
  * TLS: أصبح `client_tls_sslmode=verify-ca/-full`
    الآن يرفض الاتصالات دون شهادة عميل.
    ([#104](https://github.com/pgbouncer/pgbouncer/issues/104))
  * TLS: يتحقق `client_tls_sslmode=allow/require` من شهادة
    العميل إذا أُرسلت. سابقًا كانتا تتركان التحقق من الشهادة
    غير مُهيأ فتفشل الاتصالات بشهادة عميل.
    ([#105](https://github.com/pgbouncer/pgbouncer/issues/105))
  * إصلاح تسريب ذاكرة عند تحرير قاعدة بيانات.
  * إصلاح تسريب محتمل في tls_handshake().
  * إصلاح التعامل مع EOF في tls_handshake().
  * إصلاح memset صغير جدًا في asn1_time_parse compat.
  * إصلاح البناء بدون TLS (`--without-openssl`).
    ([#101](https://github.com/pgbouncer/pgbouncer/issues/101))
  * إصلاح مشكلات مختلفة في بناء Windows.
    ([#100](https://github.com/pgbouncer/pgbouncer/issues/100))
- أعمال التنظيف
  * TLS: استخدام SSL_MODE_RELEASE_BUFFERS لتقليل
    استخدام الذاكرة للاتصالات غير النشطة.
  * تنظيف الذاكرة المخصصة عند الخروج. يساعد على تشغيل فاحصات تسريب الذاكرة.
  * تحسين توثيق `server_reset_query`.
    ([#110](https://github.com/pgbouncer/pgbouncer/issues/110))
  * إضافة خيارات TLS إلى ملف التهيئة النموذجي.

**2015-12-18  -  PgBouncer 1.7  -  «الألوان تختلف بعد البعث»**

- الميزات
  * دعم اتصالات TLS. يُستخدم OpenSSL/LibreSSL
    كتنفيذ خلفي.
  * دعم المصادقة عبر شهادة عميل TLS.
  * دعم مصادقة "peer" على مقابس Unix.
  * دعم ملف التحكم في الوصول المبني على المضيف، مثل [pg_hba.conf](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
    في Postgres. يتيح هذا تهيئة
    TLS لاتصالات الشبكة ومصادقة
    "peer" للاتصالات المحلية.
- أعمال التنظيف
  * ضبط `query_wait_timeout` على 120 ثانية افتراضيًا.
    القيمة الافتراضية الحالية (0) تسبب انتظارًا
    لا نهائيًا، وهذا غير مفيد. ويعني ذلك أنه
    إذا كان لدى عميل استعلام معلّق ولم يُسنَد
    إلى اتصال خادم، فسيُقطع اتصال العميل.
  * تعطيل `server_reset_query_always` افتراضيًا. الآن لا يُستخدم
    استعلام إعادة التعيين إلا في المجمّعات التي في وضع الجلسة.
  * زيادة pkt_buf إلى 4096 بايت. يحسّن الأداء مع TLS.
    السلوك على الأرجح خاص بالحمل، لكن ينبغي أن يكون
    ذلك آمنًا لأنه منذ الإصدار v1.2 فُصلت مخازن الحزم
    المؤقتة عن الاتصالات وتُستخدم بكسل من المجمّع.
  * دعم عدّ حزم ReadyForQuery المتوقعة في وضع pipeline.
    يتجنب هذا تحرير الخادم مبكرًا جدًا. يصلح
    [#52](https://github.com/pgbouncer/pgbouncer/issues/52).
  * تحسين منطق sbuf_loopcnt - يُضمن إعادة معالجة
    المقبس حتى لو لم ترد أحداث من المقبس. مطلوب
    لـ TLS لأن له تخزينه المؤقت الخاص.
  * تكييف اختبارات النظام للعمل مع BSD
    وMacOS الحديثة. (Eric Radman)
  * إزالة مصادقة **crypt**. إنها مهملة وغير
    مدعومة من PostgreSQL منذ الإصدار 8.4.
  * إصلاح خيار التهيئة المجرد "--with-cares" -
    فبدون وسيطة كان معطوبًا.

--------

## PgBouncer 1.6.x {#pgbouncer-16x}

**2015-09-03  -  PgBouncer 1.6.1  -  «جمهور الاستوديو يوافق»**

- الميزات
  * إعداد جديد: `server_reset_query_always`. عندما يُضبط، يعطّل
    استخدام `server_reset_query` على المجمّعات غير الجلسية. يقدم
    PgBouncer وضع تجميع لكل مجمّع، لكن تجميع الجلسات وتجميع المعاملات
    لا ينبغي أن يستخدما استعلام إعادة تعيين نفسه. في الواقع، لا
    ينبغي أن يستخدم تجميع المعاملات أي استعلام إعادة تعيين.

    وهو ممكّن في الإصدار 1.6.x، لكنه سيعطَّل في الإصدار 1.7.

- الإصلاحات
  * [أمني] إزالة الإسناد غير الصالح لـ `auth_user`. (#69) عندما
    يكون `auth_user` مضبوطًا ويطلب العميل اسم مستخدم غير
    موجود، فسيسجل دخوله بوصفه `auth_user`. ليس ذلك جيدًا.

    [CVE-2015-6817](https://access.redhat.com/security/cve/cve-2015-6817)

  * تخطي NoticeResponse في handle_auth_response. وإلا فإن مستويات
    السجل المطوّلة على الخادم تسبب إخفاقات تسجيل الدخول.

  * console: ملء `auth_user` عندما يكون auth_type=any. وإلا فقد
    ينهار التسجيل (#67).

  * إصلاحات قابلية نقل متنوعة (OpenBSD، Solaris، OSX).

**2015-08-01  -  PgBouncer 1.6  -  «زومبي المستقبل»**

- الميزات

  * تحميل تجزئة كلمة مرور المستخدم من قاعدة بيانات postgres.
    معاملات جديدة:

    auth_user
        المستخدم الذي يُستخدم للاتصال بقاعدة البيانات نفسها وجلب معلومات المستخدم.
        يمكن ضبطه لكل قاعدة بيانات أيضًا.

    auth_query
        استعلام SQL يُنفّذ باسم auth_user.
        القيمة الافتراضية: "SELECT usename, passwd FROM pg_shadow WHERE usename=$1"

    (Cody Cutrer)

  * يمكن تهيئة وضع التجميع لكل قاعدة بيانات ولكل مستخدم معًا.
    (Cody Cutrer)

  * حدود اتصال لكل قاعدة بيانات ولكل مستخدم:
    max_db_connections وmax_user_connections.
    (Cody Cutrer / Pavel Stehule)

  * إضافة الأمرين DISABLE/ENABLE لمنع الاتصالات الجديدة.
    (William Grant)

  * خلفية DNS جديدة: c-ares. الخلفية الوحيدة التي تدعم جميع
    الميزات المهمة: /etc/hosts مع التحديث، وبحث SOA، والردود
    الكبيرة (عبر TCP/EDNS+UDP)، وIPv6. وهي الآن الخلفية
    المفضلة، وستكون على الأرجح الخلفية **الوحيدة** في المستقبل،
    إذ لا معنى لدعم حشد من المكتبات غير الكافية.

    SNAFU: إصدارات c-ares التي <= 1.10 بها عيب يكسر دعم CNAME-s عند
      تمكين IPv6. (أُصلح upstream.) وكحل بديل، تُستخدم c-ares التي <=
      1.10 بـ IPv4 فقط. لذا لن يتخلى PgBouncer عن الخلفيات الأخرى إلا
      عندما يكون c-ares الذي >1.10 (غير مصدر بعد) قد صدر منذ فترة...

  * عرض remote_pid في SHOW CLIENTS/SERVERS. متاح للعملاء
    الذين يتصلون عبر مقابس unix ولكل من خادم tcp ومقبس
    unix. في حالة خادم tcp، يُؤخذ pid من مفتاح الإلغاء.

  * إضافة معامل تهيئة منفصل (dns_nxdomain_ttl)
    للتحكم في التخزين المؤقت السلبي
    لـ dns. (Cody Cutrer)

  * إضافة عنوان IP لمضيف العميل ومنفذه إلى application_name.
    يُمكَّن هذا بمعامل تهيئة application_name_add_host
    الذي يكون افتراضيًا 'off'.
    (Andrew Dunstan)

  * تحتوي ملفات التهيئة على التوجيه '%include
    FILENAME' للسماح بتقسيم التهيئة
    إلى عدة ملفات. (Andrew Dunstan)

- أعمال التنظيف

  * log: إحاطة عنوان ipv6 بـ []
  * log: عند الاتصال بالخادم، إظهار ip المحلي والمنفذ
  * win32: استخدام النمط gnu للوسائط الطويلة: --foo
  * السماح بالأرقام في اسم المضيف، ومحاولة التحليل دائمًا بـ inet_pton
  * إصلاح deallocate_all() في FAQ
  * إصلاح كلمة مفتاحية غير صحيحة في ملف التهيئة النموذجي
    (Magnus Hagander)
  * السماح بالتعليقات (بـ ';') في ملفات المصادقة.
    (Guillaume Aubert)
  * إصلاح أخطاء إملائية في رسائل السجل والتعليقات.
    (Dmitriy Olshevskiy)

- الإصلاحات

  * إصلاح إطلاق اتصالات جديدة أثناء الصيانة
    (Cody Cutrer)
  * عدم تحميل ملف المصادقة مرتين عند الإقلاع
    (Cody Cutrer)
  * إبطال صحيح لقواعد البيانات التلقائية (autodbs)
  * ipv6: ضبط IPV6_V6ONLY على مقبس الاستماع.
  * win32: عدم ضبط SO_REUSEADDR على مقبس الاستماع.
  * إصلاح نسخ عنوان IPv6 (memcpy)
  * إصلاح إلغاء انتظار العملاء.
    (Mathieu Fenniak)
  * إصلاح عيب صغير، يجب فحص نتيجة calloc
    (Heikki Linnakangas)
  * إضافة سطر جديد في نهاية ملف PID
    (Peter Eisentraut)
  * عدم السماح باتصالات خادم جديدة عندما يكون PAUSE <db> قد صدر.
    (Petr Jelinek)
  * إصلاح 'bad packet' أثناء تسجيل الدخول عندما يكون الترويسة متأخرًا.
    (Michał Trojnara, Marko Kreen)
  * إصلاح أخطاء اكتشفها Coverity.
    (Euler Taveira)
  * تعطيل server_idle_timeout عندما يقل عدد الخوادم عن min_pool (#60)
    (Marko Kreen)

--------

## PgBouncer 1.5.x {#pgbouncer-15x}

**2015-04-09  -  PgBouncer 1.5.5  -  «تظاهّر بالموت كي تفوز»**

- الإصلاحات
  * إصلاح انهيار عن بُعد - ترتيب حزم غير صالح يسبب البحث
    عن مؤشر NULL. غير قابل للاستغلال، مجرد DoS فحسب.

**2012-11-28  -  PgBouncer 1.5.4  -  «لا تسريبات، والتدريب على النظافة نجح»**

- الإصلاحات
  * DNS: إصلاح تسريب ذاكرة في خلفية getaddrinfo_a().
  * DNS: إصلاح تسريب ذاكرة في خلفية udns.
  * DNS: إصلاح حساب الإحصاءات.
  * DNS: تحسين التعامل مع رسائل الخطأ لـ getaddrinfo_a().
  * إصلاح بناء win32.
  * إصلاح فحص دعم اعتماديات المُصرِّف في configure.
  * بعض إصلاحات التوثيق.

**2012-09-12  -  PgBouncer 1.5.3  -  «محمصة كمية»**

- إصلاح حرج

  * أسماء قواعد البيانات الطويلة جدًا قد تؤدي إلى انهيار، وهو ما يمكن التحريض
    عليه عن بُعد إذا كانت قواعد البيانات التلقائية (autodbs) ممكّنة.

    افترضت الفحوصات الأصلية أن جميع الأسماء تأتي من ملفات التهيئة،
    لذا كان استخدام fatal() مقبولًا، لكن عندما تكون قواعد البيانات التلقائية ممكّنة
    - باستخدام '*' في قسم [databases] - يمكن أن يأتي اسم قاعدة البيانات
    من الشبكة، مما يجعل الإيقاف عن بُعد ممكنًا.

    [CVE-2012-4575](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-4575)

- ميزات ثانوية

  * max_packet_size - معامل تهيئة لضبط الحجم الأقصى
    للحزم المسموح بمرورها. أُبقيت القيمة الافتراضية
    نفسها: (2G-1)، لكن يمكن الآن جعلها أصغر.
  * في حالة ترويسة حزمة غير قابلة للتحليل، إظهارها
    بالنظام الست عشري في السجل ورسالة الخطأ.

- الإصلاحات

  * AntiMake: كان يستخدم $(relpath) و$(abspath) لمعالجة أسماء المسارات،
    لكن النتيجة كانت فشل بناء عندما يحتوي مسار الشجرة المصدرية على روابط
    رمزية. غُيِّرت الشيفرة الآن لتعمل على سلاسل نصية مجردة فقط.
  * console: يمكن الآن استخدام SET لضبط قيم سلسلة نصية فارغة.
  * config.txt: إظهار أن جميع المدد (timeouts) يمكن ضبطها كأعداد
    عشرية. هذه ميزة مخفية جيدًا أُدخلت في الإصدار 1.4.

**2012-05-29  -  PgBouncer 1.5.2  -  «لا تمضغ، فقط ابتلع»**

- الإصلاحات
  * بسبب خطأ، كان reserve_pool_timeout يؤخذ بالميكروثواني
    لا بالثواني، ما كان يفعّل المجمّع الاحتياطي
    فورًا عند امتلاء المجمّع. الآن يُستخدم بالثواني،
    كما كان مقصودًا. (لاحظه Keyur Govande)

**2012-04-17  -  PgBouncer 1.5.1  -  «إحباط، إعادة محاولة، تجاهل؟»**

- الميزات
  * معاملات لضبط أذونات مقبس unix:
    unix_socket_mode=0777, unix_socket_group=''.
- الإصلاحات
  * السماح بسلسلة فارغة لمتغير جانب الخادم - هذا ضروري
    لعمل "application_name" بشكل صحيح، لأنه المعامل
    الوحيد الذي لا يملك قيمة افتراضية جانب الخادم.
  * إذا تغير نص الاتصال، اشتراط تحديث معاملات الخادم.
    سابقًا كان PgBouncer يواصل بالمعاملات القديمة،
    وهو ما يكسر العمل عند ترقية Postgres.
  * إذا تغير نص اتصال قاعدة البيانات التلقائية (autodb)، إسقاط الاتصالات القديمة.
  * cf_setint: استخدام strtol() بدلًا من atoi() لتحليل معاملات التهيئة التي تكون قيمها
    أعدادًا صحيحة. يتيح ذلك النظام الست عشري والثماني وكشفًا أفضل للأخطاء.
  * استخدام sigqueue() لاكتشاف وجود union
    sigval - يصلح البناء على HPUX.
  * إزالة أمر 'git' من Makefile، فهو يرمي أخطاء
    عشوائية في حالة البناء من أرشيف tar مجرد.
  * توثيق معامل stats_period. يضبط
    هذا الفترة لناتج الإحصاءات.
  * اشتراط Asciidoc >= 8.4، فالتوثيق لم يعد متوافقًا
    مع الإصدارات الأقدم على ما يبدو.
  * التوقف عن محاولة إعادة المحاولة عند EINTR من close().

**2012-01-05  -  PgBouncer 1.5  -  «تمرير عملاء راضين منذ 2007»**

إذا كنت تستخدم أكثر من 8 عناوين IP خلف اسم DNS واحد، فأنت الآن
بحاجة إلى استخدام بروتوكول EDNS0 للاستعلام. الخلفيات getaddrinfo_a()/getaddrinfo()
وUDNS فقط تدعمه، أما libevent 1.x/2.x فلا. لتمكينه
لـ libc، أضف 'options edns0' إلى /etc/resolv.conf.

يُطلب GNU Make 3.81+ للبناء.

- الميزات
  * اكتشاف تغيّر ردود DNS وإبطال الاتصالات
    بعناوين IP لم تعد موجودة
    في آخر رد. (Petr Jelinek)
  * إبطال أسماء المضيفين المبني على الرقم التسلسلي
    لمنطقة DNS. عندما يكون الخيار dns_zone_check_period
    مضبوطًا، ستُستعلم جميع مناطق DNS عن SOA، وعندما
    يتغير الرقم التسلسلي، ستُستعلم جميع أسماء المضيفين.
    هذا ضروري للحصول على إبطال اتصال حتمي، لأن
    الإبطال وقت البحث بلا فائدة عندما لا تُجرى
    عمليات بحث. يعمل مع خلفية UDNS الجديدة فقط.
  * أمران جديدان SHOW DNS_HOSTS وSHOW DNS_ZONES لفحص ذاكرة DNS المؤقتة.
  * معامل جديد: min_pool_size - يتجنب
    إسقاط جميع الاتصالات عندما لا يوجد
    حمل. (Filip Rembiałkowski)
  * idle_in_transaction_timeout - قتل المعاملة
    إذا طال الخمول. غير مضبوط افتراضيًا.
  * خلفية libudns جديدة لعمليات بحث DNS. أكثر ميزات من evdns.
    استخدم --with-udns للتنشيط. لا يعمل مع IPv6 بعد.
  * أمر KILL، لقتل جميع الاتصالات لقاعدة بيانات واحدة فورًا.
    (Michael Tharp)
  * الانتقال إلى نظام بناء Antimake للحصول على ملفات
    Makefile أجمل. يُطلب الآن GNU Make 3.81+ للبناء.
- الإصلاحات
  * يعمل DNS الآن مع أسماء مضيفي IPv6.
  * عدم تغيير حالة الاتصال عند وصول NOTIFY من الخادم.
  * إصلاحات توثيق متنوعة.
    (Dan McGee)
  * Console: دعم اقتباس المعرفات بـ "". في الأصل لم تكن لدينا
    أي أوامر تأخذ أسماء قواعد بيانات، فلم يكن الاقتباس لازمًا.
  * Console: السماح بالأرقام في بداية كلمة التعبير النمطي.
    محاولة استخدام محلل صارم تجعل الأمور معقدة للغاية هنا.
  * عدم انتهاء صلاحية قواعد البيانات التلقائية المتوقفة مؤقتًا.
    (Michael Tharp)
  * إنشاء قواعد البيانات التلقائية عند الحاجة عند تنفيذ PAUSE.
    (Michael Tharp)
  * إصلاح رسالة سجل خاطئة أصدرها أمر RESUME.
    (Peter Eisentraut)
  * عندما يكون user= دون password= في نص اتصال قاعدة
    البيانات، تؤخذ كلمة المرور من userlist.
  * تحليل '*' بشكل صحيح في شيفرة الاستحواذ.
  * autogen.sh: العمل مع autoconf/automake الأقدم.
  * إصلاح انهيار التشغيل كخدمة على win32 بسبب basename() سيئ من
    مكتبة mingw/msvc. يُستخدم الآن basename() المتوافق دائمًا.

--------

## PgBouncer 1.4.x {#pgbouncer-14x}

**2011-06-16  -  PgBouncer 1.4.2  -  «خوارزمية الضربة الأولى»**

أنظمة التشغيل المتأثرة: \*BSD، Solaris، Win32.

- إصلاحات قابلية النقل
  * إعطاء CFLAGS إلى الرابط. ضروري عند استخدام
    بديل getaddrinfo_a() المبني على pthread.
  * lib/find_modules.sh: استبدال split() بـ index()+substr().
    يفترض أن يجعلها تعمل مع إصدارات AWK الأقدم.
  * <usual/endian.h>: تجاهل تعريفات htoX/Xtoh الخاصة بالنظام.
    قد تكون هناك مجموعة فرعية فقط من المعرفات (macros) معرفة.
  * <usual/signal.h>: فصل compat sigval عن compat sigevent
  * <usual/socket.h>: تضمين <sys/uio.h> للحصول على iovec
  * <usual/time.h>: كشف أفضل للدوال تلقائيًا على win32
  * <usual/base_win32.h>: إزالة إعلان sigval/sigevent المكرر

**2011-04-01  -  PgBouncer 1.4.1  -  «كان كل ذلك تمثيلًا»**

- الميزات

  * دعم الاستماع/الاتصال لعناوين IPv6.
    (Hannu Krosing)
  * عناوين استماع متعددة في 'listen_addr'. لكل منها تستدعى
    getaddrinfo()، فيمكن استخدام الأسماء أيضًا.
  * console: إرسال إصدار PgBouncer بوصفه 'server_version' إلى العميل.

- إصلاحات مهمة

  * تعطيل getaddrinfo_a() على glibc < 2.9 لأنه ينهار على الإصدارات الأقدم.

    أنظمة التشغيل المتأثرة البارزة: RHEL/CentOS 5.x (glibc 2.5)، Ubuntu
      8.04 (glibc 2.7). وأيضًا Debian/lenny (glibc 2.7) الذي يملك getaddrinfo_a()
      لا ينهار لكن ليس لدينا طريقة جيدة لاكتشاف ذلك.

    يُرجى استخدام libevent 2.x على مثل هذه الأنظمة، فبديل getaddrinfo_a()
      ليس مخصصًا للأنظمة الإنتاجية. واقرأ قسم 'DNS lookup
      support' الجديد في README لترى كيف تُختار خلفية DNS.

    (Hubert Depesz Lubaczewski, Dominique Hermsdorff, David Sommerseth)

  * الافتراض إلى --enable-evdns إذا استُخدم libevent 2.x.

  * تمكين tcp_keepalive افتراضيًا، فهذا ما يفعله Postgres أيضًا.
    (Hubert Depesz Lubaczewski)

  * ضبط server_reset_query الافتراضي إلى DISCARD
    ALL ليكون متوافقًا مع Postgres افتراضيًا.

  * win32: إصلاح انهيارات مع عنوان مقبس unix بقيمة NULL.
    (Hiroshi Saito)

  * إصلاح تنظيف قواعد البيانات التلقائية: شيفرة التنظيف القديمة كانت تخلط بين
    قواعد البيانات والمجمّعات: فبمجرد العثور على مجمّع فارغ واحد، تُوسم قاعدة
    البيانات بوصفها 'idle'، وقد تقتل لاحقًا قاعدة بيانات بها مستخدمون نشطون.

    Reported-By: Hubert Depesz Lubaczewski

- الإصلاحات

  * جعل بديل getaddrinfo_a() غير حاصر، باستخدام
    خيط واحد متوازٍ لإجراء عمليات البحث.
  * تمكين بناء pthread إذا استُخدم بديل getaddrinfo_a.
  * release_server لم يكن يضبط ->last_lifetime_disconnect عند قطع الاتصال ببلوغ العمر.
    (Emmanuel Courreges)
  * win32: إصلاح ملف المصادقة مع نهايات أسطر
    DOS - لم يأخذ load_file() في الحسبان
    تقلص الملف عند التحميل. (Rich Schaaf)
  * <usual/endian.h>: إضافة كشف autoconf
    لدوال enc/dec حتى لا يسبب تعارضات
    على BSD. (James Pye)
  * عدم الانهيار عندما لا يكون ملف التهيئة موجودًا.
    (Lou Picciano)
  * عدم الانهيار عند فشل بحث DNS عند التسجيل على مستوى الضجيج (-v -v).
    (Hubert Depesz Lubaczewski, Dominique Hermsdorff)
  * استخدام العلامات العكسية (backticks) بدلًا من $(cmd) في find_modules.sh لجعله أكثر قابلية للنقل.
    (Lou Picciano)
  * استخدام 'awk' بدلًا من 'sed' في find_modules.sh لجعله أكثر قابلية للنقل.
    (Giorgio Valoti)
  * تسجيل معلومات خلفية DNS غير المتزامنة النشطة عند البدء.
  * إصلاح --disable-evdns ليعني 'no' بدلًا من 'yes'.
  * الإشارة في التوثيق إلى أن -R يتطلب unix_socket_dir.
  * مناقشة server_reset_query في faq.txt.
  * استعادة memset المفقود في مخصص slab
  * إصلاحات قابلية نقل ثانوية متنوعة في libusual.

**2011-01-11  -  PgBouncer 1.4  -  «شيفرة دامية»**

- الميزات

  * بحث DNS غير متزامن - بدلًا من تحليل أسماء المضيفين
    وقت إعادة التحميل، تُحلّ الأسماء الآن وقت الاتصال،
    مع تخزين مؤقت قابل للضبط. (انظر معامل dns_max_ttl.)

    يستخدم افتراضيًا getaddrinfo_a() (من glibc) كخلفية، وإن لم تكن
      موجودة، تُحاكى getaddrinfo_a() عبر getaddrinfo() الحاصر(!).

    عند تمرير الوسيطة --enable-evdns إلى configure، تُستخدم evdns الخاصة
      بـ libevent كخلفية. لا تُستخدم افتراضيًا، لأن libevent 1.3/1.4
      تحوي تنفيذًا معيبًا. تبدو evdns في libevent 2.0 سليمة فقط.

  * متغير تهيئة جديد: syslog_ident، لضبط اسم syslog.

  * دعم سليم لمعامل بدء `application_name`.

  * خيارات سطر أوامر طويلة (Guillaume Lelarge)

  * إصلاحات قابلية نقل Solaris (Hubert Depesz Lubaczewski)

  * متغير تهيئة جديد: disable_pqexec. تستطيع البيئات
    شديدة الحذر تعطيل بروتوكول الاستعلام البسيط به. يتطلب
    تطبيقات تستخدم بروتوكول الاستعلام الموسع فقط.

  * توافق مع Postgres: إذا كان اسم قاعدة البيانات فارغًا
    في حزمة البدء، استخدام اسم المستخدم كقاعدة بيانات.

- الإصلاحات

  * معاملا الخادم DateStyle وTimeZone يحتاجان إلى استخدام حالة الأحرف الدقيقة.
  * console: إرسال معاملات الخادم datetime وtimezone وstdstr إلى العميل.

- تنظيفات داخلية

  * استخدام مكتبة libusual للدوال المساعدة منخفضة المستوى.
  * إزالة حد الطول الثابت من معاملات الخادم.

--------

## PgBouncer 1.3.x {#pgbouncer-13x}

**2010-09-09  -  PgBouncer 1.3.4  -  «الـ bouncer دائمًا على صواب»**

- الإصلاحات
  * تطبيق منطق الفشل السريع وقت الاتصال. فإذا كان
    الخادم يفشل، يتلقى العملاء خطأً عند الاتصال.
  * عدم وسم قواعد البيانات المولدة تلقائيًا للفحص وقت إعادة
    التحميل، وإلا فستُقتل، لأنها غير موجودة في التهيئة.
  * تجاهل معامل application_name افتراضيًا. يتجنب
    هذا حاجة جميع مستخدمي Postgres 9.0 إلى إضافته
    إلى ignore_startup_parameters= بأنفسهم.
  * تصحيح اقتباس pg_auth. '\' لا يُستخدم هناك.
  * إبلاغ أفضل عن الأخطاء على وحدة التحكم، بإظهار الاستعلام الوارد للمستخدم.
  * دعم أنظمة التشغيل (OpenBSD) حيث tv_sec ليس time_t.
  * تجنب تحذيرات مفرطة الضجيج على gcc 4.5.

**2010-05-10  -  PgBouncer 1.3.3  -  «NSFW»**

- تحسينات
  * جعل وسيطة listen(2) قابلة للضبط: listen_backlog. هذا مفيد على أنظمة
    التشغيل حيث يكون الحد الأقصى المسموح للنظام قابلاً للضبط.
  * تحسين رسائل قطع الاتصال لتُظهر أي اسم مستخدم
    أو قاعدة بيانات تسبب في فشل تسجيل الدخول.
- الإصلاحات
  * نقل منطق إعادة إطلاق الفشل السريع. كان القديم مزعجًا في حالة
    قواعد البيانات أو المستخدمين المعطلين نهائيًا، بمحاولته إعادة
    المحاولة حتى لو لم يكن هناك عملاء يريدون تسجيل الدخول.
  * جعل دوال التسجيل تحفظ errno القديم، وإلا فقد يتصرف pgbouncer
    بشكل غريب على مستويات السجل الأعلى وعند مشكلات التسجيل.
  * زيادة حجم مخازن متنوعة متعلقة بالبدء
    للتعامل مع بدء EDB الأكثر ضجيجًا.
  * اكتشاف طلب بدء بروتوكول V2 وإعطاء سبب واضح لقطع الاتصال.

**2010-03-15  -  PgBouncer 1.3.2  -  «رصاصة البوميرانغ»**

- الإصلاحات

  * متغير تهيئة جديد 'query_wait_timeout'. إذا لم يحصل العميل
    على اتصال خادم خلال هذا عدد الثواني، فسيُقتل.

  * إذا لم يكن في المجمّع اتصال خادم وفشل آخر اتصال،
    فعدم تعليق اتصالات العملاء بل إرسال خطأ فورًا.

    هذا مع الإصلاح السابق يتجنب التعطلات غير
      الضرورية إذا كانت قاعدة بيانات قد سقطت.

  * تتبّع حالة libevent في sbuf.c لتجنب event_del() مزدوج.
    رغم أنه آمن عادةً، لا يبدو أنه يعمل بنسبة 100%.
    ينبغي الآن أن نعرف دائمًا هل استُدعي أم لا.

  * تعطيل الصيانة أثناء SUSPEND. وإلا فمع المهل القصيرة كان
    bouncer القديم قد يغلق بعض الاتصالات بعد إرسالها.

  * تطبيق client_login_timeout على العملاء المنتظرين لحزمة
    الترحيب (أول اتصال خادم). وإلا فقد يبقون منتظرين إلى
    ما لا نهاية، ما لم يكن هناك query_timeout مضبوطًا.

  * win32: إضافة الخيارين -U/-P إلى -regservice ليتيح للمستخدم
    اختيار الحساب الذي تعمل الخدمة تحته. كان الاختيار التلقائي
    القديم بين Local Service و Local System غير موثوق بما يكفي.

  * console: إزالة \0 من نهاية أعمدة النص. كان يصعب
    ملاحظته، لأن عملاء C كانت بلا مشكلة معه.

  * تحسينات على التوثيق.  (Greg Sabino Mullane)

  * توضيح بعض رسائل السجل المتعلقة بتسجيل الدخول.

  * تغيير مستوى تسجيل الأخطاء التي يرسلها المجمِّع (عادة عند
    قطع الاتصال) من INFO إلى WARNING، لأنها تنبئ بمشكلات.

  * تغيير رسالة السجل لـ query_timeout إلى "query timeout".

**2009-07-06  -  PgBouncer 1.3.1  -  «مطابق الآن تمامًا لمتطلبات مراقبة NSA»**

- الإصلاحات
  * إصلاح مشكلة مع sbuf_loopcnt كانت قد تجعل الاتصالات
    تتعطل. إذا كان طول الاستعلام أو النتيجة قريبًا من
    مضاعف لـ (pktlen*sbuf_loopcnt) [10k افتراضيًا]، فقد
    يبقى منتظرًا مزيدًا من البيانات لن تظهر أبدًا.
  * جعل إعادة تهيئة قاعدة البيانات فورية. حاليًا كانت
    الاتصالات القديمة قد تُعاد استخدامها بعد SIGHUP.
  * إصلاح SHOW DATABASES الذي كان معطوبًا بسبب إضافة عمود.
  * كان الوصول إلى وحدة التحكم معطلًا عندما يكون "auth_type=any" لأن pgbouncer يهمل اسم المستخدم.
    الإصلاح: إذا كان "auth_type=any"، السماح لأي مستخدم بوحدة التحكم بوصفه مشرفًا.
  * إصلاح الماكرو CUSTOM_ALIGN السيئ. لحسن الحظ هو غير مستخدم إذا كان نظام
    التشغيل يعرّف ماكرو ALIGN مسبقًا، لذا يبدو أن العيب لم يحدث في الواقع.
  * win32: استدعاء WSAStartup() دائمًا، لا في وضع daemon
    فقط لأن تحليل التهيئة يريد حل أسماء المضيفين.
  * win32: وضع علامات اقتباس حول اسم ملف التهيئة في سطر
    أوامر الخدمة للسماح بالمسافات في المسارات. يبدو أن مسار
    الملف التنفيذي لا يحتاج ذلك بسبب بعض سحر win32.
  * إضافة STATS إلى نص SHOW HELP.
  * doc/usage.txt: وحدات الزمن في نتائج وحدة التحكم
    هي بالميكروثانية، لا بالميلي ثانية.

**2009-02-18  -  PgBouncer 1.3 -  «حركة الإنهاء الجديدة Ki-Smash»**

- الميزات

  * خصصت IANA المنفذ 6432 ليكون المنفذ الرسمي لـ PgBouncer.
    لذلك تغير رقم المنفذ الافتراضي إلى 6432. لا
    يحتاج المستخدمون الأفراد الحاليون إلى التغيير،
    لكن إذا كنت توزع حزم PgBouncer، فيُرجى تغيير
    الافتراضي في الحزمة إلى المنفذ الرسمي.

  * إنشاء قواعد بيانات ديناميكيًا (David Galoyan)

    يمكنك الآن تعريف قاعدة بيانات بالاسم "*". إذا عُرِّفت،
      فسيُستخدم نص اتصالها لجميع قواعد البيانات غير المعرفة.
      مفيد في الغالب لبيئات الاختبار / التطوير.

  * دعم Windows (Hiroshi Saito)

    يعمل PgBouncer الآن على Windows 2000+. يبقى استخدام سطر الأوامر نفسه،
      باستثناء أنه لا يمكنه العمل كـ daemon ولا القيام بإعادة تشغيل مباشر.
      للتشغيل كخدمة، عرِّف المعامل service_name في التهيئة. ثم:

        > pgbouncer.exe config.ini -regservice
        > net start SERVICE_NAME

    للإيقاف وإلغاء التسجيل:

        > net stop SERVICE_NAME
        > pgbouncer.exe config.ini -unregservice

    لاستخدام سجل أحداث Windows، يجب تسجيل DLL الأحداث أولًا:

        > regsvr32 pgbevent.dll

    بعدها يمكنك ضبط "syslog = 1" في التهيئة.

- ميزات ثانوية

  * أصبح بالإمكان الآن اقتباس أسماء قواعد البيانات في ملف التهيئة باقتباس المعرفات
    القياسي في SQL، للسماح بأحرف غير قياسية في أسماء قواعد البيانات.

  * قيمتان جديدتان قابلتان للضبط: 'reserve_pool_size' و'reserve_pool_timeout'.
    في حال وجود عملاء في المجمّع انتظروا أكثر من 'reserve_pool_timeout'
    ثانية، يحدد 'reserve_pool_size' عدد الاتصالات
    التي يمكن إضافتها إلى المجمّع. يمكن أيضًا ضبطها
    لكل مجمّع بمتغير الاتصال 'reserve_pool'.

  * قيمة قابلة للضبط جديدة 'sbuf_loopcnt' للحد من الوقت المستغرق على مقبس واحد.

    في بعض المواقف - مثل خادم SMP وPostgres محلي وشبكة سريعة -
      يمكن لـ pgbouncer تشغيل حلقة recv()->send() مرات كثيرة
      دون حجب على أي من الجانبين. لكن هذا يعني أن الاتصالات
      الأخرى ستتعطل لفترة طويلة. لجعل المعالجة أكثر عدلًا،
      حدّ عدد مرات تنفيذ recv()->send() على مقبس واحد. إذا
      بلغ العدد الحد، فواصل معالجة المقابس الأخرى. ستُستأنف
      معالجة ذلك المقبس في حلقة الأحداث التالية.

    شكرًا لـ Alexander Schöcke على التقرير والاختبار.

  * أصبحت مصادقة crypt() اختيارية الآن، لأنها أزيلت من Postgres.
    إذا لم يوفرها نظام التشغيل، يعمل pgbouncer جيدًا بدونها.

  * إضافة الميلي ثانية إلى طوابع السجل الزمنية.

  * استبدال تنفيذ MD5 القديم بآخر أكثر إيجازًا.

  * تحديث رخصة ISC بتوضيح FSF.

- الإصلاحات

  * في حال أبلغ event_del() عن فشل، المواصلة بالتنظيف فقط.
    سابقًا كان pgbouncer يعيد المحاولة، في حال كان الفشل
    بسبب ENOMEM. لكن هذا تسبب في فيضانات السجل بتكرارات
    لا نهائية، لذا يبدو أن libevent لا يحب ذلك.

    لماذا يبلغ event_del() عن فشل في المرة الأولى لا يزال لغزًا.

  * --enable-debug الآن يكتفي بالتبديل بين نزع معلومات التنقيح من
    الثنائي أو لا. لم يعد يعبث مع -fomit-frame-pointer لأنه خطير.

  * إصلاح ترتيب التضمينات، وإلا فقد تأتي تضمينات النظام
    قبل الداخلية. كانت مشكلة لملف التضمين md5.h الجديد.

  * تضمين ملف COPYRIGHT في .tgz...

--------

## PgBouncer 1.2.x {#pgbouncer-12x}

**2008-08-08  -  PgBouncer 1.2.3  -  «بايتات منتقاة بعناية»**

- الإصلاحات
  * تعطيل شيفرة SO_ACCEPTFILTER لـ BSDs التي لم تكن تعمل.
  * تضمين etc/userlist.txt النموذجي في tgz.
  * استخدام '$(MAKE)' بدلًا من 'make' للتكرار (Jørgen Austvik)
  * تعريف _GNU_SOURCE وإلا فـ glibc عديم الفائدة.
  * ترك libevent 1.1 يجتاز اختبار الربط حتى نبلغ لاحقًا "1.3b+ needed"
  * اكتشاف ملف pid القديم وإزالته.

شكرًا لـ Devrim GÜNDÜZ وBjoern Metzdorf على تقارير المشكلات والاختبار.

**2008-08-06  -  PgBouncer 1.2.2  -  «كيس التقيؤ مرفق»**

- الإصلاحات
  * إزالة 'drop_on_error'، فقد كانت فكرة سيئة. أُضيفت كحل بديل
    لسلوك مخزن الخطط المعطل في Postgres، لكنها قد تسبب ضررًا في
    الحالة الشائعة عندما تُرجع بعض الاستعلامات خطأً دائمًا.

**2008-08-04  -  PgBouncer 1.2.1  -  «مقاوم للماء»**

- الميزات
  * معامل جديد 'drop_on_error' - إذا رمى الخادم خطأً
    فلن يُعاد استخدام الاتصال بل يُسقط بعد أن ينتهي
    العميل منه. هذا ضروري لتحديث مخزن الخطط. التحديث
    التلقائي لا يعمل حتى في 8.3. الافتراضي 1.
- الإصلاحات
  * SHOW SOCKETS/CLIENTS/SERVERS: عدم الانهيار إذا لم يكن للمقبس مخزن مؤقت.
  * إصلاح حلقة لا نهائية عند SUSPEND إذا تنشّط suspend_timeout.
- أعمال تنظيف ثانوية
  * استخدام <sys/uio.h> لأجل 'struct iovec'.
  * إلغاء الإيقاف (من SIGINT) عند RESUME/SIGUSR2،
    وإلا فسينشط عند PAUSE التالي.
  * رسالة سجل سليمة إذا أُلغيت عملية وحدة التحكم.

**2008-07-29  -  PgBouncer 1.2  -  «ناي سحري عادي»**

يتطلب PgBouncer 1.2 الآن إصدار libevent 1.3b أو أحدث. إصدارات
libevent الأقدم تنهار مع شيفرة إعادة التشغيل الجديدة.

- الميزات

  * خيار سطر الأوامر (-u) ومعامل التهيئة (user=) لدعم تبديل المستخدم
    عند البدء. أيضًا يرفض pgbouncer الآن العمل بوصفه root.

    (Jacob Coby)

  * نص استخدام أكثر وضوحًا (-h).  (Jacob Coby)

  * خيار قاعدة بيانات جديد: connect_query للسماح بتشغيل استعلام
    على الاتصالات الجديدة قبل أخذها في الاستخدام.

    (Teodor Sigaev)

  * متغير تهيئة جديد 'ignore_startup_parameters' للسماح بمعاملات
    إضافية في حزمة البدء وتجاهلها. افتراضيًا يُسمح فقط بـ
    'database' و'user'، وكل ما عداهما يرمي خطأً. هذا ضروري
    للتسامح مع JDBC المفرط في حماسه الذي يريد وضع 'extra_float_digits=2'
    في حزمة البدء دون قيد أو شرط.

  * التسجيل إلى syslog: معاملان جديدان syslog=0/1
    و syslog_facility=daemon/user/local0.

  * إعادة تشغيل مباشر أقل رعبًا (-R)

    - نقل تحميل FD قبل fork، ليسجل إلى وحدة التحكم ويمكن إلغاؤه بـ ^C

    - الإبقاء على SHUTDOWN بعد fork، ليكون ^C آمنًا

    - تُجرى محاولة connect() إلى مقبس unix لمعرفة هل يستمع أحد. الآن
      يمكن استخدام -R حتى عندما لم تكن هناك عملية سابقة تعمل. إذا
      كانت هناك عملية سابقة، لكن -R غير مستخدم، يفشل البدء.

  * أوامر وحدة تحكم جديدة:

    - SHOW TOTALS الذي يعرض ملخص الإحصاءات (كما يذهب إلى السجل) مع استخدام الذاكرة.

    - SHOW ACTIVE_SOCKETS - مثل show sockets؛ لكن بترشيح النشط منها فقط.

- ميزات أقل ظهورًا

  * suspend_timeout - إسقاط الاتصالات المتعطلة وتسجيلات الدخول
    الطويلة. يضيف هذا أمانًا إضافيًا لإعادة التشغيل.

  * عند رمي قاعدة البيانات البعيدة خطأً عند تسجيل الدخول، إخطار العملاء.

  * إزالة قاعدة بيانات من التهيئة وإعادة التحميل تعمل -
    تُقتل جميع الاتصالات وتزال قاعدة البيانات.

  * تزييف بعض المعاملات في أوامر SHOW/SET في وحدة التحكم لتكون أكثر شبهًا
    بـ Postgres. كان ذلك ضروريًا للسماح لـ psycopg بالاتصال بوحدة التحكم.
    (client_encoding/default_transaction_isolation/datestyle/timezone)

  * جعل server_lifetime=0 يقطع اتصال الخادم فورًا بعد
    الاستخدام الأول. سابقًا كانت "0" تجعل PgBouncer يتجاهل
    عمر الخادم. وبما أن هذا السلوك لم يكن موثقًا،
    فلا ينبغي أن يكون هناك مستخدمون يعتمدون عليه.

  * تحسينات داخلية:

    - تُخصَّص مخازن الحزم بكسل ويُعاد استخدامها. يفترض أن يحقق
      هذا نقصًا كبيرًا في استخدام الذاكرة. يجعل هذا أيضًا من
      الواقعي استخدام pktbuf كبيرًا مع كثير من الاتصالات.

    - الكثير من تحسينات التعامل مع الأخطاء، ينبغي الآن
      أن ينجو PgBouncer من مواقف OOM بشكل سليم.

    - استخدام مخصص slab لإدارة الذاكرة.

    - الكثير من تنظيفات الشيفرة.

- الإصلاحات

  * كان يُصدر accept() واحد فقط لكل حلقة أحداث وكان
    قد يسبب تراكمًا في طابور الاتصالات عند وجود كمية
    كبيرة من محاولات الاتصال. الآن يُفرَّغ مقبس الاستماع
    دائمًا بالكامل، ما ينبغي أن يصلح هذا.
  * التعامل مع EINTR من connect().
  * جعل configure.ac متوافقًا مع autoconf 2.59.
  * إصلاحات توافق Solaris (Magne Mæhre)

--------

## PgBouncer 1.1.x {#pgbouncer-11x}

**2007-12-10  -  PgBouncer 1.1.2  -  «المطرقة»**

- الميزات
  * أصبحت قطوع الاتصال بسبب server_lifetime الآن متباعدة
    بمقدار (server_lifetime / pool_size) ثانية. يتجنب
    هذا أن يسبب pgbouncer فيضانات إعادة اتصال.
- الإصلاحات
  * مشكلات الترقية المباشرة من 1.0 إلى 1.1:
    - 1.0 لا يتتبع معاملات الخادم، فتبقى NULL
      لكن 1.1 لم يتوقع ذلك فانهار.
    - إذا كانت معاملات الخادم مجهولة، لكن معاملات العميل مضبوطة،
      فإصدار SET لها، بدلًا من الشكوى.
  * إزالة عبارات التنقيح المؤقتة التي تُركت سهوًا
    في الشيفرة على مستوى INFO، فكانت تلوث السجلات.
  * إعادة إصلاح debian/changelog
- التنظيف
  * إعادة ترتيب حقول struct SBuf للحصول على محاذاة أفضل للمخزن المؤقت.

**2007-10-26  -  PgBouncer 1.1.1  -  «نحلة ترقص البريك»**

- الإصلاحات
  * كان مخزن معاملات الخادم المؤقت قد يبقى غير مهيأ، ما
    تسبب في SET غير ضروري لها. تسبب هذا في مشكلة على 8.1
    الذي لا يسمح بلمس standard_conforming_strings. (شكرًا
    لـ Dimitri Fontaine على التقرير والاختبار.)
  * بعض إصلاحات التوثيق.
  * تضمين doc/fixman.py في .tgz.

**2007-10-09  -  PgBouncer 1.1  -  «صندوق أدوات القبعة المجنونة»**

- الميزات

  * تتبّع معاملات الخادم التالية:

        client_encoding  datestyle, timezone, standard_conforming_strings

  * تحسينات نص اتصال قاعدة البيانات:

    - قبول اسم المضيف في host=
    - قبول موقع مقبس unix مخصص في host=
    - قبول القيم المقتبسة: password=' asd''foo'

  * متغير تهيئة جديد: server_reset_query، ليُرسل فور التحرير
  * متغير تهيئة جديد: server_round_robin، للتبديل بين LIFO وRR.
  * حزمة الإلغاء المرسلة لاتصال خامل لم تعد تسقطه.
  * الإلغاء بـ ^C من psql يعمل مع SUSPEND / PAUSE.
  * طباعة حدود FD عند البدء.
  * عند التعليق، محاولة بلوغ حدود الحزم بأسرع ما يمكن.
  * إضافة 'timezone' إلى معاملات قاعدة البيانات.
  * استخدام واصف ملف سجل طويل العمر. يُعاد فتحه عند SIGHUP / RELOAD؛
  * معلومات طرف الاتصال المحلي في SHOW SERVERS/CLIENTS/SOCKETS.

- تنظيف الشيفرة

  * رسائل سجل تنقيح أكثر تتضمن معلومات المقبس.
  * إزالة الأرقام السحرية وتنظيف رسائل الخطأ. (David Fetter)
  * بنية غلاف لمعلومات الحزمة الحالية. يزيل الكثير من التعقيد.

- الإصلاحات

  * اكتشاف ترويسات الحزم غير الصالحة بشكل أفضل.
  * كان فحص تعديل auth_file معطوبًا، ما جعل pgbouncer
    يعيد تحميله كثيرًا أكثر من اللازم.

--------

## PgBouncer 1.0.x {#pgbouncer-10x}

**2007-06-18  -  PgBouncer 1.0.8  -  «جوتسو المجرفة غير الميتة»**

- الإصلاحات
  * إصلاح انهيار في التعامل مع حزمة الإلغاء. (^C من psql)
- الميزات
  * PAUSE <db>; RESUME <db>; يعملان الآن.
  * تنظيف تحليل أوامر وحدة التحكم.
  * تعطيل فحص الـ assert المكلف داخل القوائم.

**2007-04-19  -  PgBouncer 1.0.7  -  «بفيتامينات من A إلى Z»**

- الإصلاحات
  * كان إرسال عدة حزم خطأ/إشعار مع حجب send() بينها
    يحرّك assert. إصلاحه بإزالة منطق التفريغ كليًا.
    بما أن PgBouncer لا يخزن أي شيء بنشاط، فهذا المنطق
    غير ضروري. كان بقايا من الوقت الذي كان الدفع
    فيه إلى المخزن المؤقت للنواة يتم بـ MSG_MORE.
  * إضافةً إلى ذلك تجنب استدعاء منطق recv() عند انفكاك حجب الإرسال.
  * كانت شيفرة البحث في القائمة لـ admin_users وstats_users
    تسيء التعامل مع النتائج الجزئية. إصلاحها.
  * توحيد إيجاد UID نظير مقبس UNIX على getpeereid().

**2007-04-12  -  PgBouncer 1.0.6  -  «الجرعة اليومية»**

- الإصلاحات
  * كان إصلاح "تعطيل الصيانة أثناء الاستحواذ"
    قد يعطل الصيانة كليًا. إصلاحه.
  * إصلاح بناء لـ FreeBSD، <sys/ucred.h> يتطلب <sys/param.h>
    هناك. الشكر موصول إلى Robert Gogolok على التقرير.

**2007-04-11  -  PgBouncer 1.0.5  -  «يكفي اليوم»**

- الإصلاحات
  * إصلاح عيوب إعادة التشغيل المباشر:
    - ضبط ->ready للخوادم الخاملة.
    - إزالة الشيفرة المهملة من use_client_socket()
    - تعطيل الصيانة أثناء الاستحواذ.

**2007-04-11  -  PgBouncer 1.0.4  -  «آخر عيب "أخير"»**

- الإصلاحات
  * إشعار من خادم خامل يوسم الخادم
    بالوسخ (dirty). لم تتوقع release_server()
    ذلك. إصلاحه بإسقاطها.

**2007-04-11  -  PgBouncer 1.0.3  -  «تفريع بلا خوف»**

- الإصلاحات
  * كان بعض التعامل مع الأخطاء مفقودًا في مسار تسجيل
    الدخول، فقد كان اتصال يحتضر هناك قد يحرك asserts.
  * تنظيف asserts في sbuf.c لالتقاط المشكلات أبكر.
  * إنشاء core عند تنشيط Assert().

- إضافات جديدة
  * متغيرات تهيئة جديدة: log_connections، log_disconnections،
    log_pooler_errors لتشغيل/إيقاف الضجيج.
  * متغير تهيئة: client_login_timeout لقتل الاتصالات الميتة في طور تسجيل
    الدخول التي كانت قد تعطل SUSPEND وبالتالي إعادة التشغيل المباشر.

**2007-03-28  -  PgBouncer 1.0.2  -  «ملعقة تفوق صوتي»**

- الإصلاحات
  * قد يبلغ libevent عن حدث محذوف داخل الحلقة نفسها.
    تجنب إعادة استخدام المقبس لحلقة واحدة.
  * لم يكن release_server() من disconnect_client()
    يتحقق هل أُرسلت الحزمة فعلًا.

**2007-03-15  -  PgBouncer 1.0.1  -  «تقنية فضائية»**

- الإصلاحات
  * الاستخدام المختلط للوقت المخزن وغير المخزن، مع تعريف النوع
    usec_t بلا إشارة تسبّب في أخطاء query_timeout زائفة.
  * إصلاح حالة نادرة عندما يستيقظ مقبس من انتظار الإرسال وقد يبقى متعطلًا.
  * اصطفاف أعدل لاتصالات الخادم. سابقًا، كان استعلام
    جديد قد يحصل على اتصال خادم قبل استعلام أقدم.
  * تأخير تحرير الخادم حتى يُضمن إرسال كل شيء.

- الميزات
  * أمر SHOW SOCKETS للحصول على معلومات تفصيلية عن الحالة.
  * وضع مؤشر PgSocket ptr في السجل، للمساعدة على تتبع اتصال واحد.
  * في وحدة التحكم، السماح بـ SELECT مكان SHOW.
  * تنظيفات شيفرة متنوعة.

**2007-03-13  -  PgBouncer 1.0  -  «Tuunitud bemm (بي إم دبليو معدّل)»**

- أول إصدار عام.
