---
title: "إنشاء صور النسخ المتماثلة والتهيئة الأولية"
linkTitle: "تهيئة النسخ المتماثلة"
weight: 60
icon: fa-solid fa-boxes-stacked
description: "إنشاء صور النسخ المتماثلة، والتهيئة الأولية (bootstrap)، وسير عمل إنشاء النسخ المتماثلة المخصصة."
module: [PATRONI]
categories: [مهمة]
upstream_link: "https://patroni.readthedocs.io/en/latest/replica_bootstrap.html"
---

<a id="replica_imaging_and_bootstrap"></a>
يتيح Patroni تخصيص عملية إنشاء نسخة متماثلة جديدة. كما يدعم تحديد ما يحدث عند تهيئة عنقود جديد فارغ أول مرة (bootstrap). والتمييز بين الأمرين محدد بوضوح: ينشئ Patroni النسخ المتماثلة فقط إذا كان المفتاح `initialize` موجودًا في DCS الخاص بالعنقود. وإذا لم يكن هناك مفتاح `initialize`، يستدعي Patroni التهيئة الأولية حصريًا على أول عقدة تحصل على قفل مفتاح initialize.

<a id="custom_bootstrap"></a>

--------

## التهيئة الأولية (bootstrap) {#bootstrap}

يوفر PostgreSQL أمر `initdb` لتهيئة عنقود جديد، ويستدعيه Patroni افتراضيًا. وفي حالات معينة، لا سيما عند إنشاء عنقود جديد كنسخة من عنقود قائم، يلزم استبدال الطريقة المدمجة بإجراءات مخصصة. يدعم Patroni تنفيذ نصوص برمجية يحددها المستخدم لتهيئة العناقيد الجديدة، مع تزويدها ببعض الوسائط المطلوبة، أي اسم العنقود ومسار دليل البيانات. يُضبط ذلك في قسم `bootstrap` من إعداد Patroni. على سبيل المثال:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script> [param1 [, ...]]
        keep_existing_recovery_conf: False
        no_params: False
        recovery_conf:
            recovery_target_action: promote
            recovery_target_timeline: latest
            restore_command: <method_specific_restore_command>
```

يجب أن تُسمّى كل طريقة تهيئة أولية مخصصة عبر الإعداد `method` وأن تُعرّف أمر `command` في القسم الذي يحمل ذلك الاسم. وتتوفر طريقة خاصة باسم `initdb` لتفعيل السلوك الافتراضي، وفي هذه الحالة يمكن حذف المعامل `method` كليًا. يمكن لأمر `command` أن يستخدم مسارًا مطلقًا، أو مسارًا نسبيًا إلى دليل العمل الخاص بـ Patroni، أو اسم أمر متاحًا في `PATH`. وإضافةً إلى المعاملات الثابتة المعرّفة في ملفات الإعداد، يزوّد Patroni الأمر بمعاملين خاصين بالعنقود:

`--scope`  
اسم العنقود الذي سيجري تهيئته

`--datadir`  
المسار إلى دليل البيانات لنسخة العنقود التي سيجري تهيئتها

يمكن تعطيل تمرير هذين الخيارين الإضافيين عبر ضبط المعامل الخاص `no_params` على `True`.

إذا أعاد نص التهيئة البرمجي القيمة `0`، يحاول Patroni إعداد نسخة PostgreSQL الناتجة عنه وتشغيلها. وإذا فشلت أي من الخطوات الوسيطة، أو أعاد النص البرمجي قيمة غير صفرية، يفترض Patroni أن التهيئة الأولية قد فشلت، فينظّف ما خلفه ويحرر قفل التهيئة لإتاحة الفرصة لعقدة أخرى لإجراء التهيئة الأولية.

إذا وُجد قسم `recovery_conf` معرّفًا في القسم نفسه الخاص بطريقة التهيئة الأولية المخصصة، فسيولّد Patroni ملف `recovery.conf` قبل تشغيل النسخة المهيّأة حديثًا (أو يضبط إعدادات الاستعادة في إعداد Postgres إذا كان يعمل على PostgreSQL \>= 12). وعادةً ما ينبغي أن يحتوي إعداد الاستعادة هذا على واحد على الأقل من معاملات `recovery_target_*`، مع ضبط `recovery_target_action` على `promote`.

إذا كان `keep_existing_recovery_conf` معرّفًا ومضبوطًا على `True`، فلن يحذف Patroni ملف `recovery.conf` الموجود إن وُجد (PostgreSQL \<= 11). وبالمثل، في هذه الحالة لن يحذف Patroni ملف `recovery.signal` أو `standby.signal` الموجود إذا وُجد أيٌّ منهما، كما لن يتجاوز إعدادات الاستعادة المضبوطة (PostgreSQL \>= 12). وهذا مفيد عند التهيئة الأولية من نسخة احتياطية باستخدام أدوات مثل pgBackRest تولّد لك إعداد الاستعادة المناسب.

إضافةً إلى ذلك، ستُمرر أي أزواج مفتاح/قيمة إضافية تُحدد في إعداد طريقة التهيئة الأولية المخصصة كوسائط إلى `command` بالصيغة `--name=value`. على سبيل المثال:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script>
        arg1: value1
        arg2: value2
```

فيجعل ذلك `command` المضبوط يُستدعى إضافةً إلى ذلك بوسيطتي سطر الأوامر `--arg1=value1 --arg2=value2`.

> [!NOTE]
> لا تُسلسل طرق التهيئة الأولية، ولا يجري الرجوع إلى الطريقة الافتراضية في حال فشل الطريقة الأساسية

على سبيل المثال، يمكنك تهيئة عنقود Patroni جديد بالكامل من نسخة احتياطية Barman بإعداد مثل هذا:

```yaml
bootstrap:
    method: barman
    barman:
        keep_existing_recovery_conf: true
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
```

> [!NOTE]
> يتطلب `patroni_barman recover` أن يكون كلٌّ من Barman و`pg-backup-api` مضبوطين على مضيف Barman، ليتمكن من تنفيذ `barman recover` عن بُعد عبر واجهة برمجة تطبيقات النسخ الاحتياطي (backup API). يستخدم المثال أعلاه مجموعة فرعية من المعاملات المتاحة. يمكنك الحصول على مزيد من المعلومات بتشغيل `patroni_barman recover --help`.

<a id="custom_replica_creation"></a>

--------

## بناء النسخ المتماثلة {#building-replicas}

يستخدم Patroni أمر `pg_basebackup` المجرَّب والموثوق لإنشاء نسخ متماثلة جديدة. ويتطلب هذا الأمر نسخة PostgreSQL مصدر قيد التشغيل، ولا يوفر تنظيفًا مدمجًا لملفات النسخ الاحتياطية المتقادمة. يفضّل البعض حلول نسخ احتياطي أخرى، مثل `WAL-E` و`pgBackRest` و`Barman` وغيرها، أو ببساطة يكتبون نصوصهم البرمجية الخاصة. ولكي يستوعب Patroni جميع حالات الاستخدام هذه، يدعم تشغيل نصوص برمجية مخصصة لاستنساخ نسخة متماثلة جديدة. وتُضبط هذه الطرق في قسم الإعداد `postgresql`:

```yaml
postgresql:
    create_replica_methods:
        - <method name>
    <method name>:
        command: <command name>
        keep_data: True
        no_params: True
        no_leader: 1
```

مثال: wal_e

```yaml
postgresql:
    create_replica_methods:
        - wal_e
        - basebackup
    wal_e:
        command: patroni_wale_restore
        no_leader: 1
        envdir: '{{WALE_ENV_DIR}}'
        use_iam: 1
    basebackup:
        max-rate: '100M'
```

مثال: pgbackrest

```yaml
postgresql:
    create_replica_methods:
        - pgbackrest
        - basebackup
    pgbackrest:
        command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
        keep_data: True
        no_params: True
    basebackup:
        max-rate: '100M'
```

مثال: Barman

```yaml
postgresql:
    create_replica_methods:
        - barman
        - basebackup
    barman:
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
    basebackup:
        max-rate: '100M'
```

> [!NOTE]
> يتطلب `patroni_barman recover` أن يكون كلٌّ من Barman و`pg-backup-api` مضبوطين على مضيف Barman، ليتمكن من تنفيذ `barman recover` عن بُعد عبر واجهة برمجة تطبيقات النسخ الاحتياطي (backup API). يستخدم المثال أعلاه مجموعة فرعية من المعاملات المتاحة. يمكنك الحصول على مزيد من المعلومات بتشغيل `patroni_barman recover --help`.

يحدد `create_replica_methods` طرق إنشاء النسخ المتماثلة المتاحة وترتيب تنفيذها. سيتوقف Patroni عند أول طريقة تعيد القيمة 0. يجب أن تُعرّف كل طريقة قسمًا منفصلًا في ملف الإعداد، يسرد الأمر المراد تنفيذه وأي معاملات مخصصة ينبغي تمريرها إلى ذلك الأمر. ستُمرر جميع المعاملات بالصيغة `--name=value`. وإضافةً إلى المعاملات التي يحددها المستخدم، يزوّد Patroni الأمر ببعض المعاملات الخاصة بالعنقود:

`--scope`  
إلى أي عنقود تنتمي هذه النسخة المتماثلة

`--datadir`  
المسار إلى دليل البيانات للنسخة المتماثلة

`--role`  
دائمًا 'replica'

`--connstring`  
سلسلة الاتصال للاتصال بعضو العنقود الذي سيجري الاستنساخ منه (الأساسي أو نسخة متماثلة أخرى). يمكن للمستخدم الموجود في سلسلة الاتصال تنفيذ أوامر SQL وأوامر بروتوكول النسخ المتماثل.

المعامل الخاص `no_leader`، عند تفعيله، يتيح لـ Patroni استدعاء طريقة إنشاء النسخة المتماثلة حتى لو لم يكن هناك قائد أو نسخ متماثلة قيد التشغيل. في هذه الحالة، ستُمرر سلسلة فارغة في سلسلة الاتصال. وهذا مفيد لاستعادة عنقود كان يعمل سابقًا من نسخة احتياطية ثنائية.

المعامل الخاص `keep_data`، عند تفعيله، يوجّه Patroni إلى عدم تنظيف مجلد PGDATA قبل استدعاء الاستعادة.

المعامل الخاص `no_params`، عند تفعيله، يعطّل الإضافة التلقائية للمعاملات الخاصة بالعنقود إلى الأمر المخصص. وتبقى المعاملات التي يحددها المستخدم تُمرر.

طريقة `basebackup` هي حالة خاصة: ستُستخدم إذا كان `create_replica_methods` فارغًا، مع أنه من الممكن إدراجها صراحةً ضمن طرق `create_replica_methods`. تهيّئ هذه الطريقة نسخة متماثلة جديدة باستخدام `pg_basebackup`، وتُؤخذ النسخة الاحتياطية الأساسية من القائد إلا إذا وُجدت نسخ متماثلة تحمل الوسم `clonefrom`، وفي هذه الحالة ستُستخدم إحدى تلك النسخ كمصدر لـ pg_basebackup. وهي تعمل دون أي إعداد؛ ومع ذلك يمكن تحديد قسم إعداد `basebackup`. وتنطبق القواعد نفسها المتّبعة مع إعداد الطرق الأخرى، أي أنه لا ينبغي تحديد سوى الخيارات الطويلة (التي تبدأ بـ --) هناك. لا يقبل Patroni تجاوزات الاتصال ولا الخيارات التي تُنتج نسخًا احتياطية بصيغة tar أو مضغوطة من جهة العميل. وعلى PostgreSQL 15 وأحدث، يُدعم الضغط من جهة الخادم عبر `compress: server-gzip` أو `compress: server-zstd`. يرشّح Patroni الخيارات التي يتحكم فيها وإعدادات الضغط باستثناء الضغط من جهة الخادم، لكنه لا يجري تحققًا كاملًا من جميع أسماء الخيارات وقيمها. ولاحظ أيضًا أنه في حال استخدام روابط رمزية لمجلد WAL، فإن تحديد مسار `--waldir` الصحيح كخيار مسؤوليةُ المستخدم، بحيث يبقى الرابط الرمزي قائمًا بعد بناء النسخة المتماثلة أو إعادة تهيئتها. غير أن هذا الخيار مدعوم فقط منذ الإصدار v10.

يمكنك تحديد معاملات basebackup إما كخريطة (أزواج مفتاح-قيمة) أو كقائمة عناصر، حيث يمكن أن يكون كل عنصر إما زوج مفتاح-قيمة أو مفتاحًا مفردًا (للخيارات التي لا تتلقى أي قيم، مثل `--verbose`). خذ هذين المثالين في الاعتبار:

```yaml
postgresql:
    basebackup:
        max-rate: '100M'
        checkpoint: 'fast'
```

و

```yaml
postgresql:
    basebackup:
        - verbose
        - max-rate: '100M'
        - waldir: /pg-wal-mount/external-waldir
```

إذا فشلت جميع طرق إنشاء النسخة المتماثلة، فسيحاول Patroni جميع الطرق مجددًا بالترتيب خلال دورة حلقة الأحداث التالية.
