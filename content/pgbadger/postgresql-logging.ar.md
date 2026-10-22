---
title: "إعداد تسجيل سجلات PostgreSQL"
linkTitle: "تسجيل سجلات PostgreSQL"
weight: 40
description: "تهيئة تسجيل الاستعلامات وlog_line_prefix والإعدادات الإقليمية والإحصاءات الداعمة لبرنامج pgBadger"
search_keywords: [--prefix, lc_messages, log_autovacuum_min_duration, log_checkpoints, log_connections, log_disconnections, log_duration, log_error_verbosity, log_line_prefix, log_lock_waits, log_min_duration_statement, log_statement, log_temp_files, prefix, stderr, syslog]
icon: fa-solid fa-database
module: [PGBADGER]
categories: [مهمة]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

لا يستطيع pgBadger تقديم تقارير إلا عن المعلومات التي يكتبها PostgreSQL في السجل. ابدأ ببادئة قابلة للتحليل وسياسة مدروسة لتسجيل التعليمات، ثم أضف الأحداث التشغيلية التي تريد تحليلها.

## الحد الأدنى من تسجيل الاستعلامات {#minimum-query-logging}

لتضمين نص الاستعلام ومدته، فعّل تسجيل التعليمات المبني على المدة:

```postgresql
log_min_duration_statement = 0
```

يسجّل `0` كل تعليمة مكتملة. على خادم مشغول، اختر عتبة أعلى بالمللي ثانية للتحكم في حجم السجل. قِس الحمل الزائد ونمو التخزين قبل تمكين عتبة منخفضة في بيئة الإنتاج.

إذا احتجت إلى المدة وعدد الاستعلامات فقط دون نص الاستعلام، فاستخدم:

```postgresql
log_min_duration_statement = -1
log_duration = on
```

فضّل `log_min_duration_statement` عندما تحتاج إلى تقارير أبطأ الاستعلامات والوقت الإجمالي المستغرق في الاستعلامات.

## حقول البادئة المطلوبة {#required-prefix-fields}

يجب أن تتضمن `log_line_prefix` مخصصة كلاً من:

- حقل وقت: `%t` أو `%m` أو `%n`؛
- حقل عملية أو جلسة: `%p` أو `%c`.

تكون بادئة `stderr` الدنيا كما يلي:

```postgresql
log_line_prefix = '%t [%p]: '
```

البادئة الأكثر فائدة تسجّل المستخدم وقاعدة البيانات والتطبيق والعميل:

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

تحذف البادئة المكافئة لوجهة syslog حقلي الطابع الزمني والعملية لأن syslog يوفرهما بالفعل:

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

يوجد ترتيب مفاتيح آخر مدعوم:

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

حين لا تكون بادئتك واحدة من الأشكال التي يتعرّف عليها pgBadger، مرّر القيمة الدقيقة عبر `--prefix`. لا تبسّطها ولا تعد كتابتها بشكل مختلف عما هي عليه في `postgresql.conf`.

## إعدادات الأحداث الموصى بها {#recommended-event-settings}

فعّل فئات الأحداث التي تريد ظهورها في التقرير:

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

قد تُنتج هذه الإعدادات حركة سجلات كبيرة. على وجه الخصوص، يسجّل `log_temp_files = 0` و`log_autovacuum_min_duration = 0` كل حدث مطابق؛ اضبطهما بما يتناسب مع حمل العمل وميزانية الاحتفاظ.

## الإبقاء على رسائل الخادم بالإنجليزية {#message-locale}

يتعرّف المحلل على رسائل خادم PostgreSQL باللغة الإنجليزية. استخدم إما:

```postgresql
lc_messages = 'en_US.UTF-8'
```

أو:

```postgresql
lc_messages = 'C'
```

الإعدادات الإقليمية مثل `fr_FR.UTF-8` غير مدعومة من قبل محلل المنبع.

## تجنب التعارض بين إعدادات تسجيل التعليمات {#statement-setting-conflicts}

لا تفعل `log_min_duration_statement` و`log_duration` و`log_statement = 'all'` معًا. فقد يُسجَّل التنفيذ نفسه أكثر من مرة، وهو ما ينفخ عدادات pgBadger ويزيد حجم السجل زيادة كبيرة.

| الهدف | الإعداد الموصى به |
|---|---|
| نص الاستعلام مع التوقيت | `log_min_duration_statement = 0` أو عتبة مختارة |
| المدة والعدد فقط | `log_min_duration_statement = -1`, `log_duration = on` |
| تدقيق واسع للتعليمات | التعامل مع `log_statement` كسياسة تسجيل منفصلة؛ وعدم جمع الإعدادات الثلاثة معًا من أجل إحصاءات pgBadger |

بعد إعادة تحميل PostgreSQL، افحص عدة مدخلات سجل حقيقية قبل تشغيل تحليل كبير. تحقق من أن حقول الطابع الزمني ومعرّف العملية/الجلسة والمستخدم وقاعدة البيانات والتطبيق والعميل تطابق التنسيق المحدد.

