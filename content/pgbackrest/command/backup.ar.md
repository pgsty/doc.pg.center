---
title: "أمر النسخ الاحتياطي (backup)"
linkTitle: "backup"
weight: 40
description: "مرجع لخيارات الأمر `backup` وسلوكه في pgBackRest."
icon: fa-solid fa-box-archive
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-backup"
---

عند تهيئة عدة مستودعات، ستنشئ pgBackRest النسخة الاحتياطية في المستودع ذي الأولوية الأعلى (مثل `repo1`) ما لم يُحدَّد الخيار `--repo`.

لا تتضمن pgBackRest مجدولًا مدمجًا، لذا فمن الأفضل تشغيلها من cron أو من آلية جدولة أخرى.

انظر [إجراء نسخة احتياطية](/ar/pgbackrest/user-guide/#perform-a-backup) لمزيد من التفاصيل والأمثلة.

## خيارات الأمر {#command-options}

### خيار تعليقات النسخة الاحتياطية (`--annotation`) {#backup-annotation-option---annotation}

إضافة تعليقات توضيحية إلى النسخة الاحتياطية على شكل أزواج مفتاح/قيمة يحددها المستخدم.

يمكن للمستخدمين إرفاق أزواج مفتاح/قيمة معلوماتية بالنسخة الاحتياطية. يمكن استخدام هذا الخيار عدة مرات لإرفاق تعليقات توضيحية متعددة.

تُخرَج التعليقات التوضيحية في المخرجات النصية للأمر `info` عند تحديد نسخة احتياطية باستخدام `--set`، وتظهر دائمًا في مخرجات JSON.

```yaml
example: --annotation=source="Sunday backup for website database"
```

### خيار فحص الأرشيف (`--archive-check`) {#check-archive-option---archive-check}

التحقق من وجود مقاطع WAL في الأرشيف قبل اكتمال النسخة الاحتياطية.

يتحقق من وجود جميع مقاطع WAL المطلوبة لجعل النسخة الاحتياطية متسقة في أرشيف WAL. من الجيد ترك هذا الخيار على قيمته الافتراضية ما لم تكن تستخدم طريقة أخرى للأرشفة.

يجب تمكين هذا الخيار إذا كان `archive-copy` ممكّنًا.

```yaml
default: y
example: --no-archive-check
```

### خيار نسخ الأرشيف (`--archive-copy`) {#copy-archive-option---archive-copy}

نسخ مقاطع WAL اللازمة للاتساق إلى النسخة الاحتياطية.

يحمي هذا الخيار، الذي يتسم بقدر من الحذر الزائد، من التلف في أرشيف مقاطع WAL عبر تخزين مقاطع WAL المطلوبة للاتساق مباشرةً في النسخة الاحتياطية. وما زالت مقاطع WAL تُخزَّن في الأرشيف، لذا سيستخدم هذا الخيار مساحة إضافية.

من الأفضل أن يستخدم الأمران `archive-push` و`backup` نوع `compress-type` نفسه (مثل `lz4`) عند استخدام هذا الخيار. وإلا فسيلزم إعادة ضغط مقاطع WAL بنوع `compress-type` الذي تستخدمه النسخة الاحتياطية، وقد يكون ذلك مكلفًا إلى حدٍّ ما اعتمادًا على حجم WAL الذي أُنشئ أثناء النسخ الاحتياطي.

عند الاستعادة، ستكون مقاطع WAL موجودة في `pg_xlog/pg_wal` وستستخدمها PostgreSQL بدلًا من استدعاء `restore_command`.

يجب تمكين الخيار `archive-check` إذا كان `archive-copy` ممكّنًا.

```yaml
default: n
example: --archive-copy
```

### خيار فحص وضع الأرشفة (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

فحص إعداد `archive_mode` في PostgreSQL.

هذا الخيار ممكّن افتراضيًا، وهو يمنع استخدام `archive_mode=always` في PostgreSQL.

قد تكون مقاطع WAL المدفوعة من خادم الاستعداد (standby) مطابقةً منطقيًا لمقاطع WAL المدفوعة من الخادم الأساسي لكن بمجاميع تحققية (checksums) مختلفة. يوصى بتعطيل الأرشفة من مصادر متعددة لتجنب التعارضات.

تنبيه:

إذا عُطِّل هذا الخيار فمن الأهمية بمكان التأكد من أن مؤرشفًا واحدًا فقط يكتب إلى المستودع عبر الأمر `archive-push`.

```yaml
default: y
example: --no-archive-mode-check
```

### خيار مهلة الأرشفة (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

مهلة الأرشفة.

يضبط أقصى وقت، بالثواني، للانتظار حتى يصل كل مقطع WAL إلى مستودع أرشيف pgBackRest. تنطبق المهلة على الأمرين `check` و`backup` عند الانتظار لأرشفة مقاطع WAL المطلوبة لاتساق النسخة الاحتياطية.

```yaml
default: 1m
allowed: [100ms, 1d]
example: --archive-timeout=30
```

### خيار النسخ الاحتياطي من خادم الاستعداد (`--backup-standby`) {#backup-from-standby-option---backup-standby}

النسخ الاحتياطي من عنقود الاستعداد.

فعِّل النسخ الاحتياطي من خادم الاستعداد لتقليل الحمل على العنقود الأساسي. يتطلب هذا الخيار تهيئة كلٍّ من المضيف الأساسي ومضيف الاستعداد.

تُدعم الأوضاع التالية:

- `y` - خادم الاستعداد مطلوب للنسخ الاحتياطي.
- `prefer` - النسخ الاحتياطي من خادم الاستعداد إن كان متاحًا وإلا فمن الأساسي.
- `n` - النسخ الاحتياطي من الأساسي فقط.

```yaml
default: n
example: --backup-standby=y
```

### خيار مجاميع تحقق الصفحات (`--checksum-page`) {#page-checksums-option---checksum-page}

التحقق من مجاميع تحقق صفحات البيانات.

يوجِّه pgBackRest للتحقق من جميع مجاميع تحقق صفحات البيانات أثناء النسخ الاحتياطي لعنقود. يُفعَّل هذا الخيار تلقائيًا عندما تكون مجاميع تحقق صفحات البيانات ممكّنة على العنقود.

افتراضيًا، لا يؤدي فشل التحقق من مجاميع التحقق إلى إيقاف النسخ الاحتياطي. بل تصدر تحذيرات في السجل (وفي وحدة التحكم بالإعدادات الافتراضية)، وتُحفظ قائمة الصفحات غير الصالحة في بيان النسخة الاحتياطية. اضبط `checksum-page-error=y` لإنهاء النسخ الاحتياطي بدلًا من ذلك.

```yaml
example: --no-checksum-page
```

### خيار الإبلاغ عن خطأ عند وجود مجاميع تحقق صفحات غير صالحة (`--checksum-page-error`) {#error-on-invalid-page-checksums-option---checksum-page-error}

الإبلاغ عن خطأ عند وجود مجاميع تحقق صفحات غير صالحة.

عند تفعيله مع الخيار `checksum-page`، يؤدي فشل التحقق من مجموع تحقق صفحة إلى إنهاء النسخ الاحتياطي.

```yaml
default: n
example: --no-checksum-page-error
```

### خيار استثناء المسارات/الملفات (`--exclude`) {#pathfile-exclusions-option---exclude}

استثناء مسارات/ملفات من النسخة الاحتياطية.

جميع الاستثناءات نسبية إلى `$PGDATA`. إذا انتهى الاستثناء بـ / فستُستثنى الملفات الموجودة في الدليل المحدد فقط، مثلًا `--exclude=junk/` سيستثني جميع الملفات في الدليل `$PGDATA/junk` لكنه يتضمن الدليل نفسه. أما إذا لم ينته الاستثناء بـ / فيجوز أن يطابق الملف الاستثناء مطابقةً تامة أو مطابقته مع إلحاق / به، مثلًا `--exclude=junk` سيستثني الدليل `$PGDATA/junk` وجميع الملفات التي يحتوي عليها.

**احذر عند استخدام هذه الميزة -- فمن السهل جدًا استثناء شيء بالغ الأهمية يجعل النسخة الاحتياطية غير متسقة. تأكد من اختبار عمليات الاستعادة لديك!**

ستُسجَّل جميع الملفات المستثناة بمستوى `info` مع قاعدة الاستثناء. تأكد من تدقيق قائمة الملفات المستثناة لضمان عدم استثناء أي شيء غير متوقع.

> **ملاحظة:** لا تُراعى الاستثناءات في عمليات الاستعادة التفاضلية (delta). سيجري *إزالة* أي ملفات/أدلة استُثنيت أثناء النسخ الاحتياطي عند الاستعادة التفاضلية.

لا ينبغي استخدام هذا الخيار لاستثناء سجلات PostgreSQL من النسخة الاحتياطية. يمكن نقل السجلات خارج دليل `PGDATA` باستخدام إعداد `log_directory` في PostgreSQL، والذي يعطي ميزة إتاحة الاحتفاظ بالسجلات بعد الاستعادة.

يمكن تحديد استثناءات متعددة في سطر الأوامر أو في ملف إعداد.

```yaml
example: --exclude=junk/
```

### خيار انتهاء الصلاحية التلقائي (`--expire-auto`) {#expire-auto-option---expire-auto}

تشغيل الأمر `expire` تلقائيًا بعد نسخة احتياطية ناجحة.

هذا الإعداد ممكّن افتراضيًا. كن حذرًا عند تعطيل هذا الخيار، لأن ذلك سيؤدي إلى الاحتفاظ بجميع النسخ الاحتياطية والأرشيف إلى أجل غير مسمى، مما قد يتسبب في نفاد مساحة المستودع. سيلزم تشغيل الأمر `expire` بانتظام لمنع حدوث ذلك.

عندما يُشغَّل `expire` تلقائيًا بعد نسخة احتياطية ناجحة فإنه يستخدم إعداد الأمر `backup`، لذا لا تُطبَّق الخيارات المحددة في قسم الأمر `expire` فقط (مثل `[global:expire]`). لتطبيق إعداد خاص بـ `expire`، عطِّل هذا الخيار وشغِّل الأمر `expire` بشكل منفصل.

```yaml
default: y
example: --expire-auto
```

### خيار الإجبار (`--force`) {#force-option---force}

فرض نسخة احتياطية دون اتصال.

عند استخدامه مع `--no-start-stop` ستُنفَّذ نسخة احتياطية حتى إذا رأت pgBackRest أن PostgreSQL قيد التشغيل. **يجب استخدام هذا الخيار بمنتهى الحذر لأنه سيؤدي على الأرجح إلى نسخة احتياطية معطوبة.**

هناك بعض السيناريوهات التي قد تبقى فيها النسخة الاحتياطية مرغوبةً في ظل هذه الظروف. مثلًا، إذا انهار خادم ولم يمكن تحميل وحدة تخزين عنقود قاعدة البيانات إلا للقراءة فقط، فسيكون من الجيد أخذ نسخة احتياطية حتى لو كان `postmaster.pid` موجودًا. في هذه الحالة سيكون من الأفضل الرجوع إلى النسخة الاحتياطية السابقة وإعادة تشغيل WAL، ولكن ربما توجد معاملة بالغة الأهمية في مقطع WAL لم تُؤرشف.

```yaml
default: n
example: --force
```

### خيار حد حفظ البيان (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

حد حفظ البيان أثناء النسخ الاحتياطي.

يحدد عدد مرات حفظ البيان أثناء النسخ الاحتياطي. حفظ البيان مهم لأنه يخزن المجاميع التحققية ويتيح عمل وظيفة الاستئناف بكفاءة. الحد الفعلي المستخدم هو 1% من حجم النسخة الاحتياطية أو `manifest-save-threshold`، أيهما أكبر.

```yaml
default: 1GiB
allowed: [1B, 1TiB]
example: --manifest-save-threshold=8GiB
```

### خيار النسخ الاحتياطي أثناء التشغيل (`--online`) {#online-option---online}

إجراء نسخة احتياطية متصلة.

تحديد --no-online يمنع pgBackRest من تشغيل وظيفتي بدء/إيقاف النسخ الاحتياطي على عنقود قاعدة البيانات. ولكي يعمل هذا يجب أن يكون PostgreSQL متوقفًا عن التشغيل، وستولِّد pgBackRest خطأ إذا لم يكن كذلك.

الغرض من هذا الخيار هو السماح بالنسخ الاحتياطي دون اتصال. يُنسخ الدليل `pg_xlog`/`pg_wal` كما هو، ويُعطَّل `archive-check` تلقائيًا للنسخة الاحتياطية.

```yaml
default: y
example: --no-online
```

### خيار الاستئناف (`--resume`) {#resume-option---resume}

السماح باستئناف نسخة احتياطية فاشلة.

يحدد ما إذا كانت خاصية الاستئناف ممكّنة. يمكن للاستئناف أن يقلل كثيرًا من الوقت اللازم لتشغيل نسخة احتياطية بعد فشل نسخة احتياطية سابقة من النوع نفسه. لكنه يضيف تعقيدًا، لذا قد يكون تعطيله مرغوبًا فيه في البيئات التي لا تتطلب هذه الخاصية.

```yaml
default: y
example: --no-resume
```

### خيار البدء السريع (`--start-fast`) {#start-fast-option---start-fast}

فرض نقطة تحقق (checkpoint) لبدء النسخ الاحتياطي بسرعة.

يفرض نقطة تحقق (عن طريق تمرير `y` إلى المعامل `fast` في وظيفة بدء النسخ الاحتياطي) بحيث تبدأ النسخة الاحتياطية فورًا. وإلا فستبدأ النسخة الاحتياطية بعد نقطة التحقق النظامية التالية.

```yaml
default: n
example: --start-fast
```

### خيار النوع (`--type`) {#type-option---type}

نوع النسخة الاحتياطية.

تُدعم أنواع النسخ الاحتياطي التالية:

- `full` - ستُنسخ جميع ملفات عنقود قاعدة البيانات ولن تكون هناك أي تبعيات على نسخ احتياطية سابقة.
- `incr` - تزايدي من آخر نسخة احتياطية ناجحة.
- `diff` - مثل النسخة الاحتياطية التزايدية لكنه يعتمد دائمًا على آخر نسخة احتياطية كاملة.

```yaml
default: incr
example: --type=full
```

## الخيارات العامة {#general-options}

### خيار السماح بالتشغيل كمستخدم جذر (`--allow-root`) {#allow-run-as-root-option---allow-root}

السماح بتشغيل الأمر كمستخدم الجذر (root).

بشكل افتراضي، يُسمح بتشغيل الأمر `restore` فقط بصفة المستخدم الجذر لأنه مصمم لإدارة ملكية الملفات بعناية. إن تشغيل الأوامر الأخرى بصفة الجذر ينطوي على خطر إنشاء ملفات (مثلًا في المستودع) يملكها الجذر وغير متاحة بالتالي لمستخدم PostgreSQL، مما يتسبب في فشل الأوامر اللاحقة.

فعِّل هذا الخيار لتشغيل أمر ما بصفة الجذر رغم ذلك. ومع ذلك، فإنه من الأفضل بكثير تشغيل pgBackRest بصفة المستخدم الذي يملك المستودع وعنقود PostgreSQL.

```yaml
default: n
example: --allow-root
```

### خيار حجم المخزن المؤقت (`--buffer-size`) {#buffer-size-option---buffer-size}

حجم المخزن المؤقت لعمليات الإدخال/الإخراج.

حجم المخزن المؤقت المستخدم لعمليات النسخ والضغط والتشفير وغيرها. يعتمد عدد المخازن المؤقتة المستخدمة على الخيارات، وقد تستهلك كل عملية ذاكرة إضافية، مثلًا قد يستخدم ضغط `gz` ذاكرة إضافية قدرها 256KiB.

القيم المسموح بها هي `16KiB`، و`32KiB`، و`64KiB`، و`128KiB`، و`256KiB`، و`512KiB`، و`1MiB`، و`2MiB`، و`4MiB`، و`8MiB`، و`16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### خيار أمر pgBackRest (`--cmd`) {#pgbackrest-command-option---cmd}

أمر pgBackRest.

قد يولِّد pgBackRest سلسلة أمر، مثلًا عندما يولِّد الأمر `restore` الإعداد restore_command. سيُستخدم في هذه الحالة الأمر المستخدم لتشغيل عملية pgBackRest ما لم يُقدَّم الخيار `cmd`.

تنبيه:

قد يسبب تغليف أمر pgBackRest سلوكًا غير متوقع، ولا يُنصح به.

```yaml
default: [path of executed pgbackrest binary]
example: --cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### خيار أمر عميل SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

أمر عميل SSH.

استخدم أمر عميل SSH محددًا عند الرغبة في استخدام بديل أو عندما لا يكون الأمر `ssh` موجودًا في $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### خيار الضغط (`--compress`) {#compress-option---compress}

استخدام ضغط الملفات.

ملفات النسخ الاحتياطي متوافقة مع أدوات الضغط من سطر الأوامر.

هذا الخيار مهمل الآن. يجب استخدام الخيار `compress-type` بدلًا منه.

```yaml
default: y
example: --no-compress
```

### خيار مستوى الضغط (`--compress-level`) {#compress-level-option---compress-level}

مستوى ضغط الملفات.

يضبط المستوى المستخدم لضغط الملفات عندما لا يساوي `compress-type` القيمة `none` أو عندما يكون `compress=y` (مهملًا).

```yaml
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: --compress-level=9
```

### خيار مستوى ضغط الشبكة (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

مستوى ضغط الشبكة.

يضبط مستوى ضغط الشبكة عندما يكون `compress-type=none` ولا يُشغَّل الأمر على المضيف نفسه الذي يوجد به المستودع. يُستخدم الضغط لتقليل حركة مرور الشبكة. عندما لا يساوي `compress-type` القيمة `none` يتم تجاهل الإعداد `compress-level-network` واستخدام `compress-level` بدلًا منه بحيث يُضغط الملف مرة واحدة فقط.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### خيار نوع الضغط (`--compress-type`) {#compress-type-option---compress-type}

نوع ضغط الملفات.

تُدعم أنواع الضغط التالية:

- `none` - بلا ضغط
- `bz2` - صيغة ضغط bzip2
- `gz` - صيغة ضغط gzip
- `lz4` - صيغة ضغط lz4 (غير متاحة على جميع المنصات)
- `zst` - صيغة ضغط Zstandard (غير متاحة على جميع المنصات)

```yaml
default: gz
example: --compress-type=none
```

### خيار ملف الإعداد (`--config`) {#config-option---config}

ملف إعداد pgBackRest.

استخدم هذا الخيار لتحديد ملف إعداد مختلف عن الملف الافتراضي.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### خيار مسار تضمين الإعداد (`--config-include-path`) {#config-include-path-option---config-include-path}

المسار إلى ملفات إعداد pgBackRest الإضافية.

تُدمَج ملفات الإعداد الموجودة في الموقع المحدد ذات الامتداد `.conf` مع ملف إعداد pgBackRest، مما ينتج عنه ملف إعداد واحد.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار الإعداد (`--config-path`) {#config-path-option---config-path}

المسار الأساسي لملفات إعداد pgBackRest.

يُستخدم هذا الإعداد لتجاوز إعداد المسار الأساسي الافتراضي للخيارين `--config` و`--config-include-path` ما لم يُحدَّدا صراحةً على سطر الأوامر.

على سبيل المثال، يؤدي تمرير `--config-path=/conf/pgbackrest` فقط إلى ضبط القيمة الافتراضية للخيار `--config` على `/conf/pgbackrest/pgbackrest.conf` وضبط القيمة الافتراضية للخيار `--config-include-path` على `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### خيار مهلة قاعدة البيانات (`--db-timeout`) {#database-timeout-option---db-timeout}

مهلة الاستعلام إلى قاعدة البيانات.

يضبط المهلة، بالثواني، للاستعلامات الموجهة إلى قاعدة البيانات. يشمل ذلك وظيفتي بدء/إيقاف النسخ الاحتياطي اللتين قد تستغرق كل منهما وقتًا طويلًا. لهذا يجب إبقاء المهلة مرتفعة ما لم تكن تعرف أن هاتين الوظيفتين ستعودان بسرعة (أي إذا كنت قد ضبطت `start-fast=y` وتعرف أن عنقود قاعدة البيانات لن ينشئ مقاطع WAL كثيرة أثناء النسخ الاحتياطي).

> **ملاحظة:** يجب أن يكون خيار `db-timeout` أصغر من خيار `protocol-timeout`.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### خيار التفاضل (delta) (`--delta`) {#delta-option---delta}

استعادة أو نسخ احتياطي باستخدام المجاميع التحققية.

أثناء الاستعادة، يُتوقع افتراضيًا أن تكون أدلة بيانات PostgreSQL ومساحات الجداول موجودة لكنها فارغة. يجري هذا الخيار استعادة تفاضلية (delta) باستخدام المجاميع التحققية.

أثناء النسخ الاحتياطي، سيستخدم هذا الخيار المجاميع التحققية بدلًا من الطوابع الزمنية لتحديد الملفات التي ستُنسخ.

```yaml
default: n
example: --delta
```

### خيار مهلة الإدخال/الإخراج (`--io-timeout`) {#io-timeout-option---io-timeout}

مهلة الإدخال/الإخراج.

المهلة، بالثواني، المستخدمة للاتصالات وعمليات القراءة/الكتابة.

لاحظ أن عملية القراءة/الكتابة بأكملها لا تحتاج إلى الاكتمال ضمن هذه المهلة، ولكن يجب إحراز *بعض* التقدم، حتى لو كان بايتًا واحدًا فقط.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### خيار مسار القفل (`--lock-path`) {#lock-path-option---lock-path}

المسار الذي تُخزن فيه ملفات القفل.

يوفر مسار القفل موقعًا لينشئ فيه pgBackRest ملفات قفل لمنع تشغيل عمليات متضاربة بشكل متزامن.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### خيار umask المحايد (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

استخدام umask محايد.

يضبط umask على 0000 بحيث تُنشأ الأوضاع في المستودع بطريقة معقولة. وضع الدليل الافتراضي هو 0750 ووضع الملف الافتراضي هو 0640.

لاستخدام umask الخاص بالمستخدم المنفِّذ بدلًا من ذلك، حدد `neutral-umask=n` في ملف الإعداد أو `--no-neutral-umask` على سطر الأوامر.

```yaml
default: y
example: --no-neutral-umask
```

### خيار ضبط أولوية العملية (`--priority`) {#set-process-priority-option---priority}

ضبط أولوية العملية.

يحدد مقدار الأولوية (أي قيمة niceness) التي سيمنحها مجدول النواة للعملية. القيم الموجبة تقلل الأولوية والقيم السالبة ترفعها. في معظم الحالات لا تملك العمليات صلاحية رفع أولويتها.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### خيار الحد الأقصى للعمليات (`--process-max`) {#process-maximum-option---process-max}

أقصى عدد عمليات للاستخدام في الضغط/النقل.

ستنفذ كل عملية الضغط والنقل لتسريع تنفيذ الأمر، لكن لا تضبط `process-max` بقيمة عالية لدرجة تؤثر في أداء قاعدة البيانات.

```yaml
default: 1
allowed: [1, 999]
example: --process-max=4
```

### خيار مهلة البروتوكول (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

مهلة البروتوكول.

يضبط المهلة، بالثواني، التي ستنتظرها العملية المحلية أو البعيدة لاستلام رسالة جديدة على طبقة البروتوكول. يمنع هذا العمليات من الانتظار إلى ما لا نهاية وصولًا لرسالة.

> **ملاحظة:** يجب أن يكون خيار `protocol-timeout` أكبر من خيار `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### خيار Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

تمكين Keep-alive.

يُمكِّن رسائل keep-alive على اتصالات المقابس.

```yaml
default: y
example: --no-sck-keep-alive
```

### خيار الـ stanza (`--stanza`) {#stanza-option---stanza}

يعرِّف الـ stanza.

الـ stanza هي إعداد عنقود قاعدة بيانات PostgreSQL الذي يحدد مكان وجوده، وكيفية النسخ الاحتياطي له، وخيارات الأرشفة، وما إلى ذلك. معظم خوادم قواعد البيانات لن يكون بها سوى عنقود PostgreSQL واحد وبالتالي stanza واحدة، في حين سيكون لخوادم النسخ الاحتياطي stanza لكل عنقود قواعد بيانات يحتاج إلى نسخ احتياطي.

قد يبدو مغريًا تسمية الـ stanza باسم العنقود الأساسي، لكن الاسم الأفضل هو ما يصف قواعد البيانات التي يحتوي عليها العنقود. ولأن اسم الـ stanza سيُستخدم للأساسي وجميع النسخ المتماثلة، فمن الأنسب اختيار اسم يصف الوظيفة الفعلية للعنقود، مثل app أو dw، بدلًا من اسم العنقود المحلي، مثل main أو prod.

```yaml
example: --stanza=main
```

### خيار عدد رسائل Keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

عدد رسائل Keep-alive.

يحدد عدد رسائل TCP keep-alive التي يمكن فقدانها قبل اعتبار الاتصال مقطوعًا.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPCNT`.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### خيار وقت خمول Keep-alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

وقت خمول Keep-alive.

يحدد مقدار الوقت (بالثواني) الذي يمر دون أي نشاط شبكي وبعده ينبغي على نظام التشغيل إرسال رسالة TCP keep-alive.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPIDLE`.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### خيار فاصل Keep-alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

زمن الفاصل بين رسائل Keep-alive.

يحدد مقدار الوقت (بالثواني) الذي يجب بعده إعادة إرسال رسالة TCP keep-alive التي لم يتم الإقرار باستلامها.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPINTVL`.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### خيار مجموعات تشفير TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

مجموعات تشفير TLSv1.2 المسموح بها.

جميع اتصالات TLS بين عميل وخادم pgBackRest مشفرة. وبشكل افتراضي، تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

> **ملاحظة:** الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل مجموعات التشفير المقبولة عند الحاجة. المثال الوارد خيار معقول ما لم تكن لديك متطلبات أمان محددة. إذا لم يُضبَط (وهو الافتراضي)، فتُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### خيار مجموعات تشفير TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

مجموعات تشفير TLSv1.3 المسموح بها.

جميع اتصالات TLS بين عميل وخادم pgBackRest مشفرة. وبشكل افتراضي، تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

> **ملاحظة:** الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل مجموعات التشفير المقبولة عند الحاجة. إذا لم يُضبَط (وهو الافتراضي)، فتُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## خيارات السجل {#log-options}

### خيار مستوى سجل وحدة التحكم (`--log-level-console`) {#console-log-level-option---log-level-console}

المستوى لتسجيل وحدة التحكم.

تُدعم مستويات السجل التالية:

- `off` - لا تسجيل على الإطلاق (غير مستحسن)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```yaml
default: warn
example: --log-level-console=error
```

### خيار مستوى سجل الملف (`--log-level-file`) {#file-log-level-option---log-level-file}

المستوى لتسجيل الملف.

تُدعم مستويات السجل التالية:

- `off` - لا تسجيل على الإطلاق (غير مستحسن)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```yaml
default: info
example: --log-level-file=debug
```

### خيار مستوى سجل الخطأ القياسي (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

المستوى لتسجيل stderr.

يحدد أي مستويات السجل ستُخرَج إلى `stderr` بدلًا من `stdout` (المحدد بواسطة `log-level-console`). لن يُخرَج الطابع الزمني والعملية إلى `stderr`.

تُدعم مستويات السجل التالية:

- `off` - لا تسجيل على الإطلاق (غير مستحسن)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```yaml
default: off
example: --log-level-stderr=error
```

### خيار مسار السجل (`--log-path`) {#log-path-option---log-path}

المسار الذي تُخزن فيه ملفات السجل.

يوفر مسار السجل موقعًا ليخزن فيه pgBackRest ملفات السجل. لاحظ أنه إذا كان `log-level-file=off` فلن يكون هناك حاجة إلى مسار سجل.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### خيار تسجيل العمليات الفرعية (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

تمكين التسجيل في العمليات الفرعية.

يُمكِّن تسجيل الملفات لأي عمليات فرعية تنشئها هذه العملية باستخدام مستوى السجل المحدد بواسطة `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### خيار الطابع الزمني للسجل (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

تمكين الطابع الزمني في التسجيل.

يُمكِّن الطابع الزمني في تسجيل وحدة التحكم والملفات. يُعطَّل هذا الخيار في مواقف خاصة مثل توليد التوثيق.

```yaml
default: y
example: --no-log-timestamp
```

## خيارات المشرفين {#maintainer-options}

### خيار فحص ترويسات الصفحات (`--page-header-check`) {#page-header-check-option---page-header-check}

فحص ترويسات صفحات PostgreSQL.

هذا الخيار ممكّن افتراضيًا، ويضيف فحوص ترويسات الصفحات.

ينبغي تجنب تعطيل هذا الخيار إلا عند الضرورة، مثلًا إذا كانت الصفحات مشفرة.

```yaml
default: y
example: --no-page-header-check
```

### خيار فرض إصدار PostgreSQL (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

فرض إصدار PostgreSQL.

سيُستخدم إصدار PostgreSQL المحدد بدلًا من الإصدار المكتشف تلقائيًا بقراءة `pg_control` أو ترويسات WAL. هذا مفيد بشكل أساسي للتفرعات (forks) من PostgreSQL أو إصداراتها التطويرية حيث تختلف هذه القيم عن الإصدار الرسمي. يجب أن يتطابق الإصدار الذي يبلغ عنه PostgreSQL عبر `server_version_num` مع الإصدار المفروض.

تحذير:

كن حذرًا عند استخدام هذا الخيار لأن `pg_control` وترويسات WAL ستُقرأ مع ذلك بالتنسيق المتوقع للإصدار المحدد، أي التنسيق الخاص بإصدار PostgreSQL المفتوح المصدر الرسمي. إذا غيّرت التفرعة أو الإصدار التطويري تنسيق الحقول التي يعتمد عليها pgBackRest فسيؤدي ذلك إلى سلوك غير متوقع. بشكل عام، لن يعمل هذا الخيار كما هو متوقع إلا إذا أضافت التفرعة جميع أعضاء البنيات (struct) المخصصة *بعد* أعضاء PostgreSQL القياسية.

```yaml
example: --pg-version-force=15
```

## خيارات المستودع {#repository-options}

### خيار تعيين المستودع (`--repo`) {#set-repository-option---repo}

تعيين المستودع.

تعيين المستودع الذي سيعمل عليه الأمر.

على سبيل المثال، يمكن استخدام هذا الخيار لإجراء استعادة من مستودع محدد بدلًا من ترك الاختيار لـ pgBackRest.

```yaml
allowed: [1, 256]
example: --repo=1
```

### خيار حاوية مستودع Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

حاوية مستودع Azure.

حاوية Azure المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، حتى يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها Azure في الحاوية أيضًا.

```yaml
example: --repo1-azure-container=pg-backup
```

### خيار نوع مفتاح مستودع Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

نوع مفتاح مستودع Azure.

تُدعم أنواع التخويل التالية:

- `shared` - مفتاح مشترك
- `sas` - توقيع وصول مشترك
- `auto` - التخويل تلقائيًا باستخدام الهويات المُدارة في Azure

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### خيار نمط URI لمستودع Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

نمط URI في Azure.

تُدعم أنماط URI التالية:

- `host` - الاتصال بالمضيف `account.endpoint`.
- `path` - الاتصال بالمضيف `endpoint` وإضافة الحساب إلى بداية URIs.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### خيار النسخ الاحتياطي التزايدي على مستوى الكتل (`--repo-block`) {#block-incremental-backup-option---repo-block}

تمكين النسخ الاحتياطي التزايدي على مستوى الكتل.

يتيح النسخ التزايدي على مستوى الكتل نسخًا احتياطية أكثر تفصيلًا عبر تقسيم الملفات إلى كتل يمكن النسخ الاحتياطي لها بشكل مستقل. يوفر هذا مساحة في المستودع ويمكن أن يحسّن أداء الاستعادة التفاضلية (delta) لأنه يمكن جلب كتل فردية دون قراءة الملف بأكمله من المستودع.

> **ملاحظة:** يجب تمكين الخيار `repo-bundle` قبل التمكن من تمكين `repo-block`.

يتحدد حجم الكتلة للملف بناءً على حجم الملف وعمره. عمومًا، تحصل الملفات الأقدم/الأكبر على أحجام كتل أكبر. وإذا كان الملف قديمًا بما فيه الكفاية فلن يُنسخ احتياطيًا باستخدام النسخ التزايدي على مستوى الكتل.

يكون النسخ التزايدي على مستوى الكتل أكثر كفاءة عند تمكينه لجميع أنواع النسخ الاحتياطي، بما في ذلك الكامل. يجعل هذا النسخة الكاملة أكبر قليلًا لكن النسخ الاحتياطية التفاضلية والتزايدية اللاحقة يمكنها الاستفادة من خرائط الكتل التي ولّدتها النسخة الكاملة لتوفير المساحة.

```yaml
default: n
example: --repo1-block
```

### خيار حزم المستودع (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

تجميع الملفات في حزم في المستودع.

تجميع (دمج) الملفات الأصغر لتقليل العدد الإجمالي للملفات المكتوبة إلى المستودع. كتابة عدد أقل من الملفات أكثر كفاءة عمومًا، لا سيما على مخازن الكائنات مثل S3. إضافةً إلى ذلك، لا تُخزَّن الملفات ذات الطول الصفري (إلا في البيان)، مما يوفر الوقت والمساحة.

```yaml
default: n
example: --repo1-bundle
```

### خيار حد حزم المستودع (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

الحد لحزم الملفات.

حد الحجم للملفات التي ستُضم إلى الحزم. الملفات الأكبر من هذا الحجم ستُخزَّن بشكل منفصل.

لا يمكن إعادة استخدام الملفات المجمَّعة في حزم عند استئناف نسخة احتياطية، لذا يتحكم هذا الخيار في الملفات التي يمكن استئنافها، أي أن القيم الأعلى تؤدي إلى عدد أقل من الملفات القابلة للاستئناف.

```yaml
default: 2MiB
allowed: [8KiB, 1PiB]
example: --repo1-bundle-limit=10MiB
```

### خيار حجم حزم المستودع (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

الحجم المستهدف لحزم الملفات.

يحدد الحجم المستهدف للملفات التي ستُضاف إلى حزمة واحدة. قد يبلغ حجم الحزمة غير المضغوطة `repo-bundle-size` + `repo-bundle-limit`، لذا لا تضبط هذا الخيار على الحجم الأقصى الذي يسمح به نظام الملفات لديك.

عمومًا، ليست فكرة جيدة ضبط هذا الخيار على قيمة مرتفعة جدًا لأن إعادة المحاولة ستضطر إلى إعادة الحزمة بأكملها.

```yaml
default: 20MiB
allowed: [1MiB, 1PiB]
example: --repo1-bundle-size=10MiB
```

### خيار نوع التشفير للمستودع (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

الشيفرة المستخدمة لتشفير المستودع.

تُدعم أنواع الشيفرات التالية:

- `none` - المستودع غير مشفر
- `aes-256-cbc` - معيار التشفير المتقدم بطول مفتاح 256 بت

لاحظ أن التشفير يتم دائمًا من جهة العميل حتى لو كان نوع المستودع (مثل S3) يدعم التشفير.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### خيار حاوية مستودع GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

حاوية مستودع GCS.

حاوية GCS المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، حتى يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها GCS في الحاوية أيضًا.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### خيار نقطة نهاية مستودع GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

نقطة نهاية مستودع GCS.

نقطة النهاية المستخدمة للاتصال بخدمة التخزين. يمكن تحديثها لاستخدام خادم GCS محلي أو نقطة نهاية بديلة.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### خيار نوع مفتاح مستودع GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

نوع مفتاح مستودع GCS.

تُدعم أنواع التخويل التالية:

- `auto` - التخويل باستخدام حساب خدمة المثيل.
- `service` - حساب خدمة من مفتاح مخزن محليًا.
- `token` - للاختبار المحلي، مثل `fakegcs`.
- `web-id` - التخويل باستخدام Workload Identity Federation (اتحاد هوية أحمال العمل).

عندما يكون `repo-gcs-key-type=service` يُعاد تحميل بيانات الاعتماد عند تجديد رمز المصادقة المميز.

عندما يكون `repo-gcs-key-type=web-id`، يجب أن يشير الخيار `repo-gcs-key` إلى ملف بيانات اعتماد حساب خارجي، ويُعاد تحميل رمز هوية الويب عند تجديد رمز المصادقة.

لا يُدعم `service_account_impersonation_url`. يُدعم `credential_source.file` فقط، وعند تحديد `credential_source.format` يجب أن يكون النوع `text`.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### خيار معرِّف مشروع GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

معرِّف مشروع GCS.

معرِّف مشروع GCS المستخدم لتحديد فوترة الطلبات.

```yaml
example: --repo1-gcs-user-project=my-project
```

### خيار الروابط الصلبة في المستودع (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

إنشاء روابط صلبة للملفات بين النسخ الاحتياطية في المستودع.

تمكين الربط الصلب للملفات في النسخ الاحتياطية التفاضلية والتزايدية بنسخها الكاملة. يعطي هذا مظهرًا بأن كل نسخة احتياطية نسخة كاملة على مستوى نظام الملفات. لكن احذر، لأن تعديل الملفات المرتبطة ارتباطًا صلبًا يمكن أن يؤثر على جميع النسخ الاحتياطية في المجموعة.

```yaml
default: n
example: --repo1-hardlink
```

اسم مهمل: hardlink

### خيار مضيف المستودع (`--repo-host`) {#repository-host-option---repo-host}

مضيف المستودع عند التشغيل عن بُعد.

عند النسخ الاحتياطي والأرشفة إلى نظام ملفات مركب محليًا لا يكون هذا الإعداد مطلوبًا.

```yaml
example: --repo1-host=repo1.domain.com
```

اسم مهمل: backup-host

### خيار ملف هيئة الشهادات لمضيف المستودع (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

ملف هيئة الشهادات لمضيف المستودع.

استخدم ملف CA غير الافتراضي في النظام للاتصال بمضيف المستودع.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة الشهادات لمضيف المستودع (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

مسار هيئة الشهادات لمضيف المستودع.

استخدم مسار CA غير الافتراضي في النظام للاتصال بمضيف المستودع.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### خيار ملف شهادة مضيف المستودع (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

ملف شهادة مضيف المستودع.

يُرسَل إلى مضيف المستودع لإثبات هوية العميل.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### خيار أمر مضيف المستودع (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

أمر pgBackRest على مضيف المستودع.

مطلوب فقط إذا كان المسار إلى أمر pgBackRest مختلفًا على المضيف المحلي ومضيف المستودع. إذا لم يُعرَّف، فسيُضبَط أمر مضيف المستودع ليكون هو نفسه الأمر المحلي.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

اسم مهمل: backup-cmd

### خيار إعداد مضيف المستودع (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

ملف إعداد مضيف مستودع pgBackRest.

يضبط موقع ملف الإعداد على مضيف المستودع. هذا مطلوب فقط إذا كان ملف إعداد مضيف المستودع في موقع مختلف عن ملف الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

اسم مهمل: backup-config

### خيار مسار تضمين إعداد مضيف المستودع (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

مسار تضمين إعداد مضيف مستودع pgBackRest.

يضبط موقع مسار تضمين الإعداد على مضيف المستودع. هذا مطلوب فقط إذا كان مسار تضمين إعداد مضيف المستودع في موقع مختلف عن مسار تضمين الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار إعداد مضيف المستودع (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

مسار إعداد مضيف مستودع pgBackRest.

يضبط موقع مسار الإعداد على مضيف المستودع. هذا مطلوب فقط إذا كان مسار إعداد مضيف المستودع في موقع مختلف عن مسار الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### خيار ملف مفتاح مضيف المستودع (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

ملف مفتاح مضيف المستودع.

يثبت أن شهادة العميل أُرسلت من مالكها.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### خيار منفذ مضيف المستودع (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

منفذ مضيف المستودع عندما يكون `repo-host` مضبوطًا.

استخدم هذا الخيار لتحديد منفذ غير افتراضي لبروتوكول مضيف المستودع.

> **ملاحظة:** عندما يكون `repo-host-type=ssh` لا توجد قيمة افتراضية للخيار `repo-host-port`. في هذه الحالة سيكون المنفذ أيَّ قيمة مهيأة للأمر المحدد بواسطة `cmd-ssh`.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

اسم مهمل: backup-ssh-port

### خيار نوع بروتوكول مضيف المستودع (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

نوع بروتوكول مضيف المستودع.

تُدعم أنواع البروتوكولات التالية:

- `ssh` - Secure Shell.
- `tls` - خادم pgBackRest TLS.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### خيار مستخدم مضيف المستودع (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

مستخدم مضيف المستودع عندما يكون `repo-host` مضبوطًا.

يحدد المستخدم الذي سيُستخدم للعمليات على مضيف المستودع. يُفضَّل ألا يكون هذا هو المستخدم `postgres` بل مستخدمًا آخر مثل `pgbackrest`. إذا كان PostgreSQL يعمل على مضيف المستودع فيمكن وضع المستخدم `postgres` في مجموعة `pgbackrest` ليحصل على أذونات القراءة على المستودع دون أن يتمكن من إتلاف المحتويات عن طريق الخطأ.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

اسم مهمل: backup-user

### خيار مسار المستودع (`--repo-path`) {#repository-path-option---repo-path}

المسار الذي تُخزن فيه النسخ الاحتياطية والأرشيف.

المستودع هو المكان الذي يخزن فيه pgBackRest النسخ الاحتياطية ويؤرشف مقاطع WAL.

قد يصعب تقدير المساحة التي ستحتاجها مسبقًا. أفضل ما يمكن فعله هو أخذ بعض النسخ الاحتياطية ثم تسجيل حجم الأنواع المختلفة من النسخ الاحتياطية (full/incr/diff) وقياس كمية WAL المُنتَجة يوميًا. سيمنحك هذا فكرة عامة عن المساحة التي ستحتاجها، مع أن المتطلبات ستتغير على الأرجح بمرور الوقت مع تطور قاعدة بياناتك بالطبع.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### خيار الاحتفاظ بالأرشيف (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

عدد النسخ الاحتياطية المعادل من WAL المتواصل المطلوب الاحتفاظ به.

> **ملاحظة:** مقاطع WAL المطلوبة لجعل نسخة احتياطية متسقة يُحتفظ بها دائمًا حتى تنتهي صلاحية النسخة الاحتياطية بغض النظر عن كيفية إعداد هذا الخيار.

إذا لم تُضبط هذه القيمة وكان `repo-retention-full-type` هو `count` (الافتراضي)، فسيكون الافتراضي للأرشيف الذي ستنتهي صلاحيته هو قيمة `repo-retention-full` (أو `repo-retention-diff`) المقابلة لـ `repo-retention-archive-type` إذا كانت مضبوطة على `full` (أو `diff`). سيضمن ذلك عدم انتهاء صلاحية WAL إلا لنسخ احتياطية انتهت صلاحيتها بالفعل. أما إذا كان `repo-retention-full-type` هو `time`، فسيكون الافتراضي لهذه القيمة إزالة الأرشيفات الأقدم من أقدم نسخة احتياطية كاملة محتفظ بها بعد تلبية إعداد `repo-retention-full`.

يجب ضبط هذا الخيار إذا ضُبط `repo-retention-archive-type` على `incr`. إذا كانت مساحة القرص محدودة، فيمكن استخدام هذا الإعداد، بالاقتران مع `repo-retention-archive-type`، لإنهاء صلاحية مقاطع WAL بقوة. لكن القيام بذلك يُلغي إمكانية إجراء PITR من النسخ الاحتياطية ذات WAL منتهي الصلاحية، ولذلك **لا** يوصى به.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-archive=2
```

اسم مهمل: retention-archive

### خيار نوع الاحتفاظ بالأرشيف (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

نوع النسخة الاحتياطية لاحتفاظ WAL.

تُدعم أنواع النسخ الاحتياطية التالية:

- `full` - فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة الذي يحدده `repo-retention-archive`.
- `diff` - (تفاضلية) فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة والتفاضلية الذي يحدده `repo-retention-archive`، أي أنه إذا كانت آخر نسخة احتياطية مأخوذة نسخة كاملة، فستُحتسب تفاضلية لأغراض repo-retention.
- `incr` - (تزايدية) فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة والتفاضلية والتزايدية الذي يحدده `repo-retention-archive`.

ويُستحسن عدم تغيير هذا الإعداد عن قيمته الافتراضية التي تنهي صلاحية WAL فقط بالاقتران مع إنهاء صلاحية النسخ الاحتياطية الكاملة.

```yaml
default: full
example: --repo1-retention-archive-type=diff
```

اسم مهمل: retention-archive-type

### خيار الاحتفاظ بالتفاضلية (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

عدد النسخ الاحتياطية التفاضلية المطلوب الاحتفاظ به.

عندما تنتهي صلاحية نسخة احتياطية تفاضلية، تنتهي صلاحية جميع النسخ الاحتياطية التزايدية المرتبطة بالنسخة التفاضلية أيضًا. وعند عدم التحديد يُحتفظ بجميع النسخ الاحتياطية التفاضلية حتى تنتهي صلاحية النسخ الكاملة التي تعتمد عليها.

لاحظ أن النسخ الاحتياطية الكاملة تُحتسب ضمن عدد النسخ الاحتياطية التفاضلية لأغراض إنهاء الصلاحية. يقلل هذا قليلًا من عدد النسخ الاحتياطية التفاضلية التي يلزم الاحتفاظ بها في معظم الحالات.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-diff=3
```

اسم مهمل: retention-diff

### خيار الاحتفاظ بالنسخ الكاملة (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

عدد/مدة الاحتفاظ بالنسخ الاحتياطية الكاملة.

عندما تنتهي صلاحية نسخة احتياطية كاملة، تنتهي صلاحية جميع النسخ الاحتياطية التفاضلية والتزايدية المرتبطة بالنسخة الكاملة أيضًا. وعند عدم تحديد الخيار سيُصدَر تحذير. وإذا كان الاحتفاظ إلى أجل غير مسمى مرغوبًا فيه فاضبط الخيار على القيمة القصوى.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-full=2
```

اسم مهمل: retention-full

### خيار نوع الاحتفاظ بالنسخ الكاملة (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

نوع الاحتفاظ للنسخ الاحتياطية الكاملة.

يحدد ما إذا كان إعداد `repo-retention-full` يمثل فترة زمنية (أيام) أم عددًا من النسخ الاحتياطية الكاملة المطلوب الاحتفاظ بها.

تُدعم أنواع الاحتفاظ التالية:

- `time` - فستُزال من المستودع النسخ الاحتياطية الكاملة الأقدم من `repo-retention-full` إذا وُجدت نسخة احتياطية أخرى تساوي إعداد `repo-retention-full` أو تتجاوزه. فمثلًا، إذا كان `repo-retention-full` هو 30 (يومًا) وكانت هناك نسختان كاملتان: واحدة عمرها 25 يومًا وأخرى عمرها 35 يومًا، فلن تنتهي صلاحية أي نسخة كاملة، لأن إنهاء صلاحية النسخة ذات العمر 35 يومًا سيُبقي النسخة ذات العمر 25 يومًا فقط، بما ينتهك سياسة الاحتفاظ لمدة 30 يومًا التي تشترط وجود نسخة احتياطية واحدة بعمر 30 يومًا على الأقل قبل إنهاء صلاحية نسخة أقدم. وتنتهي صلاحية WAL المؤرشف الأقدم من أقدم نسخة كاملة متبقية تلقائيًا ما لم يُضبط `repo-retention-archive-type` و`repo-retention-archive` صراحةً.
- `count` - فستُنهى صلاحية النسخ الاحتياطية الكاملة التي تتجاوز `repo-retention-full`. فمثلًا، إذا كان `repo-retention-full` هو `4` واكتملت نسخة احتياطية كاملة خامسة، فستُنهى صلاحية أقدم نسخة كاملة للإبقاء على العدد 4.

لاحظ أنه يجب إكمال النسخة الاحتياطية بنجاح قبل أخذها في الاعتبار للاحتفاظ. مثلًا، إذا كان `repo-retention-full-type` هو `count` و`repo-retention-full` هو `2`، فيجب وجود 3 نسخ احتياطية كاملة مكتملة قبل أن تنتهي صلاحية الأقدم.

```yaml
default: count
example: --repo1-retention-full-type=time
```

### خيار الاحتفاظ بسجل النسخ الاحتياطي (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

عدد أيام ملفات بيان سجل النسخ الاحتياطي المطلوب الاحتفاظ بها.

تُخزَّن نسخة من بيان النسخة الاحتياطية في مسار `backup.history` عند اكتمال النسخة الاحتياطية. افتراضيًا لا تنتهي صلاحية هذه الملفات أبدًا لأنها مفيدة لاستخراج البيانات، مثل قياس نمو النسخ الاحتياطية وWAL بمرور الوقت.

اضبط `repo-retention-history` لتحديد عدد أيام ملفات بيان سجل النسخ الاحتياطي المطلوب الاحتفاظ بها. النسخ الاحتياطية غير منتهية الصلاحية يُحتفظ بها دائمًا في سجل النسخ الاحتياطي. حدد `repo-retention-history=0` للاحتفاظ بسجل النسخ الاحتياطي للنسخ غير منتهية الصلاحية فقط.

عندما ينتهي بيان سجل نسخة احتياطية كاملة، تنتهي صلاحية جميع ملفات بيان سجل النسخ الاحتياطية التفاضلية والتزايدية المرتبطة بالنسخة الكاملة أيضًا.

```yaml
allowed: [0, 9999999]
example: --repo1-retention-history=365
```

### خيار حاوية مستودع S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

حاوية مستودع S3.

حاوية S3 المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، حتى يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها AWS في الحاوية أيضًا.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### خيار نقطة نهاية مستودع S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

نقطة نهاية مستودع S3.

يجب أن تكون نقطة نهاية AWS صالحة للمنطقة المحددة.

للإعدادات المخصصة/الاختبارية قد تكون الخيارات `repo-storage-ca-file` و`repo-storage-ca-path` و`repo-storage-host` و`repo-storage-port` و`repo-storage-verify-tls` مفيدة.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### خيار نوع مفتاح مستودع S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

نوع مفتاح مستودع S3.

تُدعم أنواع التخويل التالية:

- `shared` - مفاتيح مشتركة
- `auto` - استرداد بيانات اعتماد مؤقتة تلقائيًا
- `web-id` - استرداد بيانات اعتماد هوية الويب تلقائيًا
- `pod-id` - استرداد بيانات اعتماد هوية الـ pod في EKS تلقائيًا
- `process` - استرداد بيانات الاعتماد بتنفيذ عملية

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### خيار معرِّف مفتاح KMS لمستودع S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

مفتاح KMS لمستودع S3.

يُمكِّن التشفير من جهة الخادم في S3 باستخدام مفتاح خدمة إدارة المفاتيح في AWS المحدد.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### خيار أمر عملية مصادقة S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

أمر عملية مصادقة S3.

الأمر (والوسائط الاختيارية) الذي سيُنفَّذ لاسترداد بيانات اعتماد S3 مؤقتة. الإدخال الأول في القائمة هو الأمر وتُمرَّر الإدخالات المتبقية كمعاملات.

يجب أن تُخرِج العملية JSON يحتوي على الحقول `AccessKeyId` و`SecretAccessKey` و`SessionToken` و`Expiration`. ستُحدَّث بيانات الاعتماد تلقائيًا قبل وقت انتهاء الصلاحية. انظر [مزود بيانات اعتماد العملية](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) لتفاصيل التنسيق.

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### خيار منطقة مستودع S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

منطقة مستودع S3.

منطقة AWS التي أُنشئت فيها الحاوية.

```yaml
example: --repo1-s3-region=us-east-1
```

### خيار الدفع من قبل الطالب لمستودع S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

ميزة الدفع من قبل الطالب لمستودع S3.

يُمكِّن ميزة الدفع من قبل الطالب في S3.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### خيار دور مستودع S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

دور مستودع S3.

اسم دور AWS (وليس ARN الكامل) المستخدم لاسترداد بيانات اعتماد مؤقتة عندما يكون `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### خيار خدمة مستودع S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

خدمة توقيع S3.

خدمة توقيع S3 المستخدمة في مصادقة SigV4. الافتراضي هو `s3` لنقاط نهاية S3 القياسية. اضبطها على `s3-outposts` عند استخدام نقطة نهاية S3 Outposts.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### خيار نقطة نهاية STS لمستودع S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

نقطة نهاية STS لمستودع S3.

نقطة نهاية STS المستخدمة لاسترداد بيانات اعتماد مؤقتة عندما يكون `repo-s3-key-type=web-id` مهيأً. اضبطها على نقطة نهاية إقليمية (مثل `sts.us-east-1.amazonaws.com`) لاستخدام STS الإقليمي، وهو ما قد يكون مطلوبًا لمناطق GovCloud أو الصين أو لتقليل زمن الاستجابة.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### خيار نمط URI لمستودع S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

نمط URI في S3.

تُدعم أنماط URI التالية:

- `host` - الاتصال بالمضيف `bucket.endpoint`.
- `path` - الاتصال بالمضيف `endpoint` وإضافة الحاوية إلى بداية URIs.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### خيار مضيف مستودع SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

مضيف مستودع SFTP.

مضيف SFTP الذي يحتوي على المستودع.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### خيار بصمة مضيف مستودع SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

بصمة مضيف مستودع SFTP.

يجب أن تطابق طريقة توليد بصمة مضيف مستودع SFTP الخيار `repo-sftp-host-key-hash-type`. ولِّد البصمة عبر `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. توجد مفاتيح مضيف ssh عادةً في الدليل `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### خيار نوع التحقق من مفتاح مضيف SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

نوع التحقق من مفتاح مضيف SFTP.

تُدعم أنواع التحقق من مفتاح مضيف SFTP التالية:

- `strict` - لن يضيف pgBackRest أبدًا مفاتيح المضيفين تلقائيًا إلى ملف ~/.ssh/known_hosts، ويرفض الاتصال بالمضيفين الذين تغيَّر مفتاح المضيف لديهم أو لم يُعثَر عليه في ملفات المضيفين المعروفين. يجبر هذا الخيار المستخدم على إضافة جميع المضيفين الجدد يدويًا.
- `accept-new` - سيضيف pgBackRest تلقائيًا مفاتيح المضيفين الجديدة إلى ملف المضيفين المعروفين للمستخدم، لكنه لن يسمح بالاتصال بمضيفين تغيَّرت مفاتيح المضيف لديهم.
- `fingerprint` - سيتحقق pgBackRest من مفتاح المضيف مقابل البصمة المحددة بواسطة الخيار `repo-sftp-host-fingerprint`.
- `none` - لن يُجرى أي تحقق من مفتاح المضيف.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### خيار نوع تجزئة مفتاح مضيف مستودع SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

نوع تجزئة مفتاح مضيف مستودع SFTP.

يحدد نوع التجزئة المستخدم لحساب ملخص مفتاح مضيف النظام البعيد عند بدء SSH. القيم المسموح بها هي `md5` و`sha1` و`sha256`، لكن `sha256` لا تدعمه إلا الإصدارات الأحدث من `libssh2`.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### خيار منفذ مضيف مستودع SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

منفذ مضيف مستودع SFTP.

منفذ مضيف مستودع SFTP.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### خيار مستخدم مضيف مستودع SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

مستخدم مضيف مستودع SFTP.

المستخدم على المضيف المستخدم لتخزين المستودع.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### خيار ملف المضيفين المعروفين لـ SFTP (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

ملف المضيفين المعروفين لـ SFTP.

ملف مضيفين معروفين للبحث فيه عن تطابق مضيف SFTP أثناء المصادقة. عند عدم تحديده، سيكون البحث الافتراضي في pgBackRest ضمن `~/.ssh/known_hosts` و`~/.ssh/known_hosts2` و`/etc/ssh/ssh_known_hosts` و`/etc/ssh/ssh_known_hosts2`. إذا كان مهيأً بمسار ملف واحد أو أكثر، فسيبحث pgBackRest فيها عن تطابق. يجب أن تكون مسارات الملفات مسارات كاملة أو تبدأ بعلامة التيلدا (~). يمكن تمرير الخيار `repo-sftp-known-host` عدة مرات لتحديد أكثر من ملف مضيفين معروفين للبحث فيه. للاستفادة من التحقق عبر ملف المضيفين المعروفين يجب عدم تحديد `repo-sftp-host-fingerprint`. انظر أيضًا خيار `repo-sftp-host-check-type`.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### خيار ملف المفتاح الخاص لمستودع SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

ملف المفتاح الخاص لـ SFTP.

ملف المفتاح الخاص لـ SFTP المستخدم للمصادقة.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### خيار ملف المفتاح العام لمستودع SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

ملف المفتاح العام لـ SFTP.

ملف المفتاح العام لـ SFTP المستخدم للمصادقة. اختياري إذا تم البناء مقابل OpenSSL، ومطلوب إذا تم البناء مقابل مكتبة مختلفة.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### خيار ملف CA لتخزين المستودع (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

ملف CA لتخزين المستودع.

استخدم ملف CA غير الافتراضي في النظام لشهادات التخزين (مثل S3 وAzure).

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

أسماء مهملة: repo-azure-ca-file, repo-s3-ca-file

### خيار مسار CA لـ TLS في تخزين المستودع (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

مسار CA لتخزين المستودع.

استخدم مسار CA غير الافتراضي في النظام لشهادات التخزين (مثل S3 وAzure).

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

أسماء مهملة: repo-azure-ca-path, repo-s3-ca-path

### خيار مضيف تخزين المستودع (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

مضيف تخزين المستودع.

الاتصال بمضيف آخر غير نقطة نهاية التخزين (مثل S3 وAzure). يُستخدم هذا عادةً للاختبار.

```yaml
example: --repo1-storage-host=127.0.0.1
```

أسماء مهملة: repo-azure-host, repo-s3-host

### خيار منفذ تخزين المستودع (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

منفذ تخزين المستودع.

المنفذ الذي سيُستخدم عند الاتصال بنقطة نهاية التخزين (مثل S3 وAzure) (أو بالمضيف إذا حُدد).

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

أسماء مهملة: repo-azure-port, repo-s3-port

### خيار الجلب المسبق من تخزين المستودع (`--repo-storage-prefetch`) {#repository-storage-prefetch-option---repo-storage-prefetch}

الجلب المسبق من تخزين المستودع.

يحدد عدد الطلبات التي تُرسل مسبقًا عند القراءة من مخازن الكائنات، مثل S3. لا يمثل ذلك تزامنًا فعليًا، لكنه يقلل زمن الانتظار المرتبط بإرسال الطلبات.

عدد الطلبات المفتوحة لكل عملية قراءة يزيد بواحد على قيمة الجلب المسبق، لأن القراءة الأولى لا يمكن جلبها مسبقًا.

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### خيار تجاوز البيانات غير اللازمة أثناء القراءة من تخزين المستودع (`--repo-storage-read-over`) {#repository-storage-read-over-option---repo-storage-read-over}

تجاوز البيانات غير اللازمة أثناء القراءة من تخزين المستودع.

قد تحتوي الحزم على بيانات غير مطلوبة أثناء الاستعادة، مثل ملفات موجودة بالفعل. يتيح هذا الخيار تجاوز البيانات غير اللازمة بمواصلة القراءة دون بدء طلب قراءة جديد إلى مخزن الكائنات. ويكون ذلك أسرع عادةً لأن زمن انتظار طلبات القراءة الجديدة أطول من مواصلة قراءة جارية. كما أنه أقل تكلفة لمعظم فئات التخزين.

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

### خيار وسوم تخزين المستودع (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

وسوم تخزين المستودع.

حدد الوسوم التي ستُضاف إلى الكائنات عندما يكون المستودع مخزن كائنات (مثل S3). يمكن تكرار الخيار لإضافة وسوم متعددة.

لا توجد وسيلة في pgBackRest لتعديل هذه الوسوم، لذا احرص على ضبطها بشكل صحيح قبل تشغيل `stanza-create` لضمان توحيد الوسوم عبر المستودع بأكمله.

```yaml
example: --repo1-storage-tag=key1=value1
```

### خيار حجم أجزاء الرفع لتخزين المستودع (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

حجم جزء الرفع لتخزين المستودع.

تسمح مخازن الكائنات مثل S3 برفع الملفات على شكل أجزاء عندما يكون الملف أكبر من أن يُخزن في الذاكرة. وحتى لو أمكن تخزين الملف في الذاكرة، فإن تحديد كمية الذاكرة المستخدمة للرفع أكفأ من حيث استهلاك الذاكرة.

سيؤدي حجم الجزء الأكبر عمومًا إلى أداء أفضل لأنه يقلل طلبات الرفع إلى الحد الأدنى ويسمح برفع ملفات أكثر في طلب واحد بدلًا من رفعها على شكل أجزاء. العيب هو أن استهلاك الذاكرة سيكون أعلى، ولأنه يجب تخصيص المخزن المؤقت للأجزاء لكل عملية على حدة، فإن قيم `process-max` الأكبر ستؤدي إلى استهلاك ذاكرة أكبر إجمالًا.

لاحظ أن أحجام الأجزاء الصالحة تختلف باختلاف نوع التخزين والمنصة. على سبيل المثال، الحد الأدنى لحجم الجزء في AWS S3 هو 5MiB. تختلف المصطلحات الدالة على حجم الجزء باختلاف نوع التخزين، لذا عند البحث عن الحد الأدنى/الأقصى استخدم "part size" لـ AWS S3، و"chunk size" لـ GCS، و"block size" لـ Azure.

إذا كان الملف أكبر من 1GiB (وهو الحد الأقصى للحجم الذي ينشئه PostgreSQL افتراضيًا) فسيزداد حجم الجزء تدريجيًا حتى الحد الأقصى المسموح به لإكمال رفع الملف.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### خيار التحقق من شهادة تخزين المستودع (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

التحقق من شهادة تخزين المستودع.

يوفر هذا الخيار القدرة على تمكين/تعطيل التحقق من شهادة TLS لخادم التخزين (مثل S3 وAzure). لا ينبغي استخدام التعطيل إلا للاختبار أو في السيناريوهات الأخرى التي تكون فيها الشهادة موقَّعة ذاتيًا.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

أسماء مهملة: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### خيار الروابط الرمزية في المستودع (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

إنشاء روابط رمزية داخل المستودع.

تمكين إنشاء الروابط الرمزية `latest` وروابط مساحات الجداول. تكون هذه الروابط الرمزية أكثر فائدة عند استخدام اللقطات لإجراء استرداد في الموقع في المستودع، وهي حالة استخدام غير شائعة.

على الرغم من أن هذه الميزة على الأرجح غير مفيدة للغالبية العظمى من المستخدمين، فهي تبقى ممكّنة افتراضيًا لأغراض التوافق القديم. ومع ذلك، قد يكون من المفيد تعطيل الروابط الرمزية لتخزين شبيه بـ Posix لا يدعمها.

```yaml
default: y
example: --no-repo1-symlink
```

### خيار نوع المستودع (`--repo-type`) {#repository-type-option---repo-type}

نوع التخزين المستخدم للمستودع.

تُدعم أنواع المستودعات التالية:

- `azure` - خدمة Azure Blob Storage
- `cifs` - مثل `posix`، لكنه يعطل الروابط ومزامنة الأدلة (fsync)
- `gcs` - Google Cloud Storage
- `posix` - أنظمة ملفات متوافقة مع Posix
- `s3` - خدمة AWS Simple Storage Service
- `sftp` - بروتوكول نقل الملفات الآمن

عند استخدام تركيب NFS كمستودع `posix`، تنطبق على pgBackRest القواعد نفسها الموضحة في توثيق PostgreSQL: [إنشاء عنقود قاعدة بيانات - أنظمة الملفات](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```yaml
default: posix
example: --repo1-type=cifs
```

## خيارات الـ stanza {#stanza-options}

### خيار قاعدة بيانات PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

قاعدة بيانات PostgreSQL.

اسم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. الافتراضي هو الأفضل عادةً لكن بعض التثبيتات قد لا تحتوي على قاعدة البيانات هذه.

لاحظ أنه لأسباب تاريخية سيُتجاهَل إعداد متغير البيئة `PGDATABASE`.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### خيار مضيف PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

مضيف PostgreSQL للعمل عن بُعد.

يستخدم للنسخ الاحتياطي في الحالات التي يختلف فيها مضيف PostgreSQL عن مضيف المستودع.

```yaml
example: --pg1-host=db.domain.com
```

اسم مهمل: db-host

### خيار ملف هيئة الشهادات لمضيف PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

ملف هيئة الشهادات لمضيف PostgreSQL.

استخدم ملف CA غير الافتراضي في النظام للاتصال بمضيف PostgreSQL.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة الشهادات لمضيف PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

مسار هيئة الشهادات لمضيف PostgreSQL.

استخدم مسار CA غير الافتراضي في النظام للاتصال بمضيف PostgreSQL.

```yaml
example: --pg1-host-ca-path=/etc/pki/tls/certs
```

### خيار ملف شهادة مضيف PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

ملف شهادة مضيف PostgreSQL.

يُرسَل إلى مضيف PostgreSQL لإثبات هوية العميل.

```yaml
example: --pg1-host-cert-file=/path/to/client.crt
```

### خيار أمر مضيف PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

أمر pgBackRest على مضيف PostgreSQL.

مطلوب فقط إذا كان المسار إلى أمر pgBackRest مختلفًا على المضيف المحلي ومضيف PostgreSQL. إذا لم يُعرَّف، فسيُضبَط أمر مضيف PostgreSQL ليكون هو نفسه الأمر المحلي.

```yaml
default: [path of executed pgbackrest binary]
example: --pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

اسم مهمل: db-cmd

### خيار إعداد مضيف PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

ملف إعداد مضيف قاعدة بيانات pgBackRest.

يضبط موقع ملف الإعداد على مضيف PostgreSQL. هذا مطلوب فقط إذا كان ملف إعداد مضيف PostgreSQL في موقع مختلف عن ملف الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

اسم مهمل: db-config

### خيار مسار تضمين إعداد مضيف PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

مسار تضمين إعداد مضيف قاعدة بيانات pgBackRest.

يضبط موقع مسار تضمين الإعداد على مضيف PostgreSQL. هذا مطلوب فقط إذا كان مسار تضمين إعداد مضيف PostgreSQL في موقع مختلف عن مسار تضمين الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار إعداد مضيف PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

مسار إعداد مضيف قاعدة بيانات pgBackRest.

يضبط موقع مسار الإعداد على مضيف PostgreSQL. هذا مطلوب فقط إذا كان مسار إعداد مضيف PostgreSQL في موقع مختلف عن مسار الإعداد المحلي.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --pg1-host-config-path=/conf/pgbackrest
```

### خيار ملف مفتاح مضيف PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

ملف مفتاح مضيف PostgreSQL.

يثبت أن شهادة العميل أُرسلت من مالكها.

```yaml
example: --pg1-host-key-file=/path/to/client.key
```

### خيار منفذ مضيف PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

منفذ مضيف PostgreSQL عندما يكون `pg-host` مضبوطًا.

استخدم هذا الخيار لتحديد منفذ غير افتراضي لبروتوكول مضيف PostgreSQL.

> **ملاحظة:** عندما يكون `pg-host-type=ssh` لا توجد قيمة افتراضية للخيار `pg-host-port`. في هذه الحالة سيكون المنفذ أيَّ قيمة مهيأة للأمر المحدد بواسطة `cmd-ssh`.

```yaml
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: --pg1-host-port=25
```

اسم مهمل: db-ssh-port

### خيار نوع بروتوكول مضيف PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

نوع بروتوكول مضيف PostgreSQL.

تُدعم أنواع البروتوكولات التالية:

- `ssh` - Secure Shell.
- `tls` - خادم pgBackRest TLS.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### خيار مستخدم مضيف PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

مستخدم تسجيل الدخول إلى مضيف PostgreSQL عندما يكون `pg-host` مضبوطًا.

سيملك هذا المستخدم أيضًا عملية pgBackRest البعيدة وسيبدأ الاتصالات بـ PostgreSQL. ولكي يعمل هذا بشكل صحيح ينبغي أن يكون المستخدم مالك عنقود قاعدة بيانات PostgreSQL، وهو عمومًا `postgres`، القيمة الافتراضية.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

اسم مهمل: db-user

### خيار مسار PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

دليل بيانات PostgreSQL.

ينبغي أن يكون هذا هو نفسه الدليل `data_directory` الذي يبلغ عنه PostgreSQL. ومع أن هذه القيمة يمكن قراءتها من أماكن مختلفة، فمن الحكمة ضبطها تحسبًا لعدم توفر تلك الموارد أثناء سيناريو استعادة أو نسخ احتياطي دون اتصال.

يُختبر الخيار `pg-path` مقابل القيمة التي يبلغ عنها PostgreSQL في كل نسخة احتياطية أثناء تشغيل PostgreSQL، لذا ينبغي أن يكون محدثًا دائمًا.

```yaml
example: --pg1-path=/data/db
```

اسم مهمل: db-path

### خيار منفذ PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

منفذ PostgreSQL.

المنفذ الذي يعمل عليه PostgreSQL. لا يحتاج هذا عادةً إلى تحديد لأن معظم عناقيد PostgreSQL تعمل على المنفذ الافتراضي.

```yaml
default: 5432
allowed: [0, 65535]
example: --pg1-port=6543
```

اسم مهمل: db-port

### خيار مسار مقبس PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

مسار مقبس unix لـ PostgreSQL.

دليل مقبس unix الذي حُدد عند تشغيل PostgreSQL. سيبحث pgBackRest تلقائيًا في الموقع القياسي لنظام التشغيل لديك، لذا لا تكون هناك عادةً حاجة إلى تحديد هذا الإعداد ما لم يُعدَّل دليل المقبس صراحةً بإعداد `unix_socket_directories` في `postgresql.conf`.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

اسم مهمل: db-socket-path

### خيار مستخدم قاعدة بيانات PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

مستخدم قاعدة بيانات PostgreSQL.

اسم مستخدم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. إذا لم يُحدد فسيتصل pgBackRest بمستخدم نظام التشغيل المحلي أو `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
