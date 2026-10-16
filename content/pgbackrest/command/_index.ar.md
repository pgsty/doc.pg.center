---
title: "مرجع الأوامر"
linkTitle: "الأوامر"
weight: 40
description: "مرجع أوامر pgBackRest مع جميع الخيارات لعمليات النسخ الاحتياطي والاستعادة والأرشفة والإدارة."
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html"
---

## مقدمة {#introduction}

تُستخدم الأوامر لتنفيذ وظائف pgBackRest المختلفة. تُدرَج خيارات الأوامر هنا بشكل استقصائي، أي أن كل خيار ينطبق على أمر ما يُدرَج مع ذلك الأمر حتى لو كان ينطبق على أمر آخر أو أكثر. يشمل ذلك جميع الخيارات التي يمكن أيضًا تهيئتها في `pgbackrest.conf`.

يمكن إعادة الخيارات غير المنطقية (غير البوليانية) المهيأة في `pgbackrest.conf` إلى قيمها الافتراضية من سطر الأوامر باستخدام البادئة `reset-`. يمكن استخدام هذه الميزة لاستعادة نسخة احتياطية مباشرة على مضيف المستودع. في الوضع الاعتيادي سيُصدر pgBackRest خطأ لأنه يرى أن مضيف قاعدة البيانات بعيد ولا يمكن إجراء الاستعادة عن بُعد. بإضافة `--reset-pg1-host` على سطر الأوامر سيتجاهل pgBackRest مضيف قاعدة البيانات البعيد ويستعيد محليًا. قد يكون من الضروري تمرير `--pg1-path` جديد لإجبار الاستعادة على الحدوث في مسار محدد، أي ليس المسار المستخدم على مضيف قاعدة البيانات.

يمكن استخدام البادئة `no-` لضبط خيار منطقي (بولياني) على القيمة false على سطر الأوامر.

يمكن ضبط أي خيار في متغير بيئة باستخدام البادئة `PGBACKREST_` واسم الخيار بأحرف كبيرة مع استبدال `-` بـ `_`، مثلًا يصبح `pg1-path` هو `PGBACKREST_PG1_PATH` ويصبح `stanza` هو `PGBACKREST_STANZA`. تُمثَّل الخيارات المنطقية كما تكون في ملف الإعداد، مثل `PGBACKREST_COMPRESS="n"`، ولا يُسمح بصيغ `reset-*`. ويمكن تمثيل الخيارات التي يمكن تحديدها عدة مرات على سطر الأوامر أو في ملف إعداد بفصل القيم بنقطتين رأسيتين، مثل `PGBACKREST_DB_INCLUDE="db1:db2"`.

تتجاوز خيارات سطر الأوامر خيارات البيئة التي تتجاوز بدورها خيارات ملف الإعداد.

انظر [مقدمة الإعداد](/ar/pgbackrest/configuration/#introduction) للحصول على معلومات حول أنواع الخيارات

## الأوامر {#commands}

| الأمر                                                            | الملخص                                                                                    |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [**`annotate`**](/ar/pgbackrest/command/annotate/)             | إضافة تعليقات توضيحية للنسخة الاحتياطية أو تعديلها أو إزالتها بعد إنشاء النسخة الاحتياطية.                  |
| [**`archive-get`**](/ar/pgbackrest/command/archive-get/)       | جلب مقاطع WAL المؤرشفة للاستعادة أو الاسترداد حتى نقطة زمنية (PITR) أو استرداد النسخة المتماثلة.                     |
| [**`archive-push`**](/ar/pgbackrest/command/archive-push/)     | قبول مقاطع WAL من PostgreSQL ودفعها إلى المستودعات المهيأة.           |
| [**`backup`**](/ar/pgbackrest/command/backup/)                 | إنشاء نسخ احتياطية إلى المستودع الهدف (الافتراضي هو المستودع ذو الأولوية الأعلى).      |
| [**`check`**](/ar/pgbackrest/command/check/)                   | التحقق من صحة إعداد النسخ الاحتياطي/الأرشفة للـ stanza وحالة أرشفة WAL.                  |
| [**`expire`**](/ar/pgbackrest/command/expire/)                 | إنهاء صلاحية النسخ الاحتياطية و WAL المؤرشف وفقًا لسياسات الاحتفاظ المهيأة.                 |
| [**`help`**](/ar/pgbackrest/command/help/)                     | عرض تعليمات الأوامر والخيارات على المستوى العام أو مستوى الأمر أو مستوى الخيار.                      |
| [**`info`**](/ar/pgbackrest/command/info/)                     | عرض حالة/بيانات الـ stanza التعريفية والنسخ الاحتياطية بصيغة نصية أو JSON.                       |
| [**`repo-get`**](/ar/pgbackrest/command/repo-get/)             | قراءة ملفات المستودع (مثل `cat`) للإدارة والتحري والاختبار.      |
| [**`repo-ls`**](/ar/pgbackrest/command/repo-ls/)               | عرض قائمة ملفات/مسارات المستودع (مثل `ls`) للإدارة والتحري والاختبار. |
| [**`restore`**](/ar/pgbackrest/command/restore/)               | الاستعادة من نسخة احتياطية (الأحدث افتراضيًا) مع إمكانية الاسترداد حتى نقطة زمنية.           |
| [**`server`**](/ar/pgbackrest/command/server/)                 | تشغيل خادم pgBackRest TLS للوصول إلى المضيف البعيد بدون SSH.                       |
| [**`server-ping`**](/ar/pgbackrest/command/server-ping/)       | إجراء ping لخادم pgBackRest TLS للتحقق من أنه يقبل الاتصالات.                     |
| [**`stanza-create`**](/ar/pgbackrest/command/stanza-create/)   | إنشاء بيانات الـ stanza التعريفية في جميع المستودعات المهيأة.                                  |
| [**`stanza-delete`**](/ar/pgbackrest/command/stanza-delete/)   | إزالة جميع النسخ الاحتياطية والأرشيفات الخاصة بـ stanza نهائيًا.                               |
| [**`stanza-upgrade`**](/ar/pgbackrest/command/stanza-upgrade/) | ترقية بيانات الـ stanza التعريفية بعد ترقية إصدار رئيسي من PostgreSQL.                       |
| [**`start`**](/ar/pgbackrest/command/start/)                   | السماح مجددًا بتشغيل عمليات pgBackRest بعد أمر `stop` سابق.                           |
| [**`stop`**](/ar/pgbackrest/command/stop/)                     | منع عمليات pgBackRest الجديدة مع إمكانية إيقاف العمليات الجارية قسرًا.                |
| [**`verify`**](/ar/pgbackrest/command/verify/)                 | التحقق من أن بيانات النسخ الاحتياطي والأرشيف في المستودع صالحة.                         |
| [**`version`**](/ar/pgbackrest/command/version/)               | عرض إصدار pgBackRest المثبت.                                               |
{.full-width}
