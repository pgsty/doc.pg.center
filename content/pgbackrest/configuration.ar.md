---
title: "مرجع الإعداد"
linkTitle: "الإعداد"
weight: 50
description: "مرجع كامل لإعداد pgBackRest يغطي جميع الإعدادات بما فيها خيارات الأرشفة والنسخ الاحتياطي والمستودع والتخزين السحابي."
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/configuration.html"
---

--------

## مقدمة {#introduction}

يمكن استخدام pgBackRest بالكامل عبر معاملات سطر الأوامر، لكن ملف الإعداد أكثر عملية للتثبيتات المعقدة أو التي تضبط الكثير من الخيارات. الموقع الافتراضي لملف الإعداد هو `/etc/pgbackrest/pgbackrest.conf`. وإذا لم يوجد ملف في ذلك الموقع فسيتم التحقق من الموقع الافتراضي القديم `/etc/pgbackrest.conf`.

تُستخدم أنواع الخيارات التالية:

**سلسلة نصية**: سلسلة نصية، تكون عادة معرّفًا أو كلمة مرور أو نحو ذلك.

مثال من سطر الأوامر: `--stanza=demo`<br/>مثال من ملف الإعداد: `repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**مسار**: يُستخدم لتحديد موقع في بنية الدلائل تحديدًا فريدًا. يجب أن تبدأ المسارات بـ /، ولا يُسمح بـ // المزدوجة، ولا يُتوقع وجود / في النهاية.

مثال من سطر الأوامر: `--repo1-path=/var/lib/pgbackrest`<br/>مثال من ملف الإعداد: `repo1-path=/var/lib/pgbackrest`

**قيمة منطقية**: تمكّن الخيار أو تعطّله. القيمتان y/n فقط هما قيمتا الوسيطة الصالحتان.

أمثلة من سطر الأوامر: `--start-fast`، `--no-start-fast`، `--start-fast=y`، `--start-fast=n`<br/>أمثلة من ملف الإعداد: `start-fast=y`، `start-fast=n`

**عدد صحيح**: يُستخدم للمنافذ، وعدّادات الاحتفاظ/إعادة المحاولة، وعدد العمليات المتوازية المسموح بها، إلخ.

مثال من سطر الأوامر: `--compress-level=3`<br/>مثال من ملف الإعداد: `pg1-port=5432`

**حجم**: يُستخدم لأحجام المخازن المؤقتة، واستخدام القرص، إلخ. يمكن تحديد الحجم بالبايت (الافتراضي) أو بـ KiB أو MiB أو GiB أو TiB أو PiB حيث يكون المضاعف قوة للعدد 1024. فمثلًا، يمكن استخدام القيمة غير الحساسة لحالة الأحرف 5GiB (أو 5GB أو 5g) بدلًا من 5368709120. والقيم الكسرية مثل 2.5GiB غير مسموح بها؛ استخدم 2560MiB بدلًا منها.

مثال من سطر الأوامر: `--archive-get-queue-max=1GiB`<br/>مثال من ملف الإعداد: `buffer-size=2MiB`

**وقت**: الوقت بالثواني.

مثال من سطر الأوامر: `--io-timeout=90`<br/>مثال من ملف الإعداد: `db-timeout=600`

**قائمة**: يجوز تقديم الخيار عدة مرات.

مثال من سطر الأوامر: `--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`

مثال من ملف الإعداد، كلٌّ في سطر مستقل:

```ini
db-exclude=db1
db-exclude=db2
db-exclude=db5
```

**مفتاح/قيمة**: يجوز تقديم الخيار عدة مرات بالشكل `key=value`.

مثال من سطر الأوامر: `--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`

مثال من ملف الإعداد، كلٌّ في سطر مستقل:

```ini
tablespace-map=ts_01=/db/ts_01
tablespace-map=ts_02=/db/ts_02
```

--------

## خيارات الأرشفة {#archive-options}

يُعرِّف قسم `archive` الخيارات الخاصة بالأمرين `archive-push` و`archive-get`.

### خيار الأرشفة غير المتزامنة (`--archive-async`) {#asynchronous-archiving-option---archive-async}

دفع/جلب مقاطع WAL بشكل غير متزامن.

يمكّن التشغيل غير المتزامن للأمرين `archive-push` و`archive-get`.

التشغيل غير المتزامن أكثر كفاءة لأنه يمكنه إعادة استخدام الاتصالات والاستفادة من التوازي. راجع الخيارات `spool-path` و`archive-get-queue-max` و`archive-push-queue-max` لمزيد من المعلومات.

```text
default: n
example: archive-async=y
```

### خيار الحجم الأقصى لقائمة انتظار الجلب من الأرشيف (`--archive-get-queue-max`) {#maximum-archive-get-queue-size-option---archive-get-queue-max}

الحجم الأقصى لقائمة انتظار archive-get في pgBackRest.

يحدد الحجم الأقصى لقائمة انتظار `archive-get` عند تمكين `archive-async`. تُخزَّن قائمة الانتظار في `spool-path` وتُستخدم لتسريع تزويد PostgreSQL بـ WAL.

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### خيار إعادة محاولة مقطع WAL المفقود (`--archive-missing-retry`) {#retry-missing-wal-segment-option---archive-missing-retry}

إعادة محاولة مقطع WAL المفقود

يعيد محاولة مقطع WAL أُبلغ سابقًا بأنه مفقود من الأمر `archive-get` عند العمل في الوضع غير المتزامن. ويمنع ذلك استخدام الإشعارات الموجودة في مسار الـ spool من عملية استعادة سابقة وما قد يسببه ذلك من فشل في الاسترداد إذا لم يتحقق الاتساق بعد.

يتيح تعطيل هذا الخيار لـ PostgreSQL التعرف بدرجة موثوقية أعلى على متى بلغ نهاية WAL في الأرشيف، ما يسمح له بالتحول إلى البث (streaming) من الرئيسي. ومع تمكين إعادة المحاولة، سيؤدي التدفق المستمر لأرشفة WAL إلى استمرار PostgreSQL في جلب WAL من الأرشيف بدلًا من التحول إلى البث.

عند تعطيل هذا الخيار من المهم التأكد من أن مسار الـ spool للـ stanza فارغ. يقوم الأمر `restore` بذلك تلقائيًا إذا كان مسار الـ spool مهيأً وقت الاستعادة. وإلا فالأمر متروك للمستخدم لضمان خلو مسار الـ spool.

```text
default: y
example: archive-missing-retry=n
```

### خيار حجم دفعة الدفع إلى الأرشيف (`--archive-push-batch-size`) {#archive-push-batch-size-option---archive-push-batch-size}

الحد الأقصى لمقدار WAL المدفوع في كل تشغيلة غير متزامنة.

في الوضع غير المتزامن تدفع عملية `archive-push` جميع مقاطع WAL الجاهزة في تشغيلة واحدة. وبما أن `archive-push-queue-max` لا يُتحقق منه إلا عند بداية كل تشغيلة، فإن التشغيلة التي تعالج عددًا كبيرًا جدًا من المقاطع قد تسمح لقائمة الانتظار بالنمو إلى ما يتجاوز الحد بكثير قبل إعادة التحقق منه.

يحد هذا الخيار مقدار WAL المعالج في كل تشغيلة بحيث تخرج العملية وتُطلقها تشغيلة `archive-push` التالية التي تعيد التحقق من قائمة الانتظار. والقيم الأدنى تعيد التحقق من قائمة الانتظار مرات أكثر على حساب إطلاق العملية غير المتزامنة بتواتر أعلى. تُقرَّب القيمة نزولًا إلى عدد صحيح من مقاطع WAL، لكن يُعالج مقطع واحد على الأقل دائمًا.

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### خيار الحجم الأقصى لقائمة انتظار الدفع إلى الأرشيف (`--archive-push-queue-max`) {#maximum-archive-push-queue-size-option---archive-push-queue-max}

الحجم الأقصى لقائمة انتظار الأرشيف في PostgreSQL.

بعد بلوغ الحد، سيحدث ما يلي:

- سيُبلغ pgBackRest قاعدةَ PostgreSQL بأن WAL أُرشف بنجاح، ثم **يحذفه (DROP IT)**.
- سيُخرَج تحذير في سجل PostgreSQL.

إذا حدث ذلك فسيُقطع تدفق سجل الأرشيف، ولن تكون الاستعادة إلى نقطة زمنية (PITR) ممكنة بعد تلك النقطة. وستلزم نسخة احتياطية جديدة لاستعادة القدرة على الاسترداد الكاملة.

في الوضع غير المتزامن ستُحذف قائمة الانتظار بأكملها منعًا لوصول دفعات متقطعة من WAL قبل تجاوز حد قائمة الانتظار مجددًا.

في الوضع غير المتزامن لا يُتحقق من هذا الحد إلا عند بداية كل تشغيلة `archive-push`، لذا يمكن لقائمة الانتظار أن تنمو متجاوزةً إياه ضمن تشغيلة واحدة. قلّل `archive-push-batch-size` للتحقق من قائمة الانتظار بتواتر أعلى.

الغاية من هذه الميزة هي منع امتلاء وحدة تخزين السجلات، إذ ستتوقف PostgreSQL كليًا عند امتلائها. فخسارة النسخة الاحتياطية خير من تعطل PostgreSQL.

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

الاسم المهمل: archive-queue-max

### خيار مهلة الأرشفة (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

مهلة الأرشفة.

يعيّن الحد الأقصى للوقت، بالثواني، لانتظار وصول كل مقطع WAL إلى مستودع أرشيف pgBackRest. تنطبق المهلة على الأمرين `check` و`backup` عند انتظار أرشفة مقاطع WAL المطلوبة لاتساق النسخة الاحتياطية.

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## خيارات النسخ الاحتياطي {#backup-options}

يُعرِّف قسم `backup` الإعدادات المتعلقة بالنسخ الاحتياطي.

### خيار التعليقات التوضيحية للنسخة الاحتياطية (`--annotation`) {#backup-annotation-option---annotation}

إضافة تعليقات توضيحية إلى النسخة الاحتياطية على شكل أزواج مفتاح/قيمة يحددها المستخدم.

يمكن للمستخدمين إرفاق أزواج مفتاح/قيمة معلوماتية بالنسخة الاحتياطية. ويمكن استخدام هذا الخيار عدة مرات لإرفاق تعليقات توضيحية متعددة.

تُخرَج التعليقات التوضيحية في المخرجات النصية للأمر `info` عند تحديد نسخة احتياطية باستخدام `--set`، وتظهر دائمًا في مخرجات JSON.

```text
example: annotation=source="Sunday backup for website database"
```

### خيار فحص الأرشيف (`--archive-check`) {#check-archive-option---archive-check}

التحقق من وجود مقاطع WAL في الأرشيف قبل اكتمال النسخة الاحتياطية.

يتحقق من وجود جميع مقاطع WAL المطلوبة لجعل النسخة الاحتياطية متسقة في أرشيف WAL. من الجيد ترك هذا الخيار على قيمته الافتراضية ما لم تكن تستخدم طريقة أخرى للأرشفة.

يجب تمكين هذا الخيار إذا كان `archive-copy` ممكّنًا.

```text
default: y
example: archive-check=n
```

### خيار نسخ الأرشيف (`--archive-copy`) {#copy-archive-option---archive-copy}

نسخ مقاطع WAL اللازمة للاتساق إلى النسخة الاحتياطية.

يحمي هذا الخيار، الذي يتسم بقدر من الحذر الزائد، من التلف في أرشيف مقاطع WAL عبر تخزين مقاطع WAL المطلوبة للاتساق مباشرةً في النسخة الاحتياطية. وما زالت مقاطع WAL تُخزَّن في الأرشيف، لذا سيستخدم هذا الخيار مساحة إضافية.

من الأفضل أن يستخدم الأمران `archive-push` و`backup` نوع `compress-type` نفسه (مثل `lz4`) عند استخدام هذا الخيار. وإلا فسيلزم إعادة ضغط مقاطع WAL بنوع `compress-type` الذي تستخدمه النسخة الاحتياطية، وقد يكون ذلك مكلفًا إلى حدٍّ ما اعتمادًا على مقدار WAL الذي أُنشئ أثناء النسخ الاحتياطي.

عند الاستعادة، ستكون مقاطع WAL موجودة في `pg_xlog/pg_wal` وستستخدمها PostgreSQL بدلًا من استدعاء `restore_command`.

يجب تمكين الخيار `archive-check` إذا كان `archive-copy` ممكّنًا.

```text
default: n
example: archive-copy=y
```

### خيار فحص وضع الأرشفة (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

فحص إعداد `archive_mode` في PostgreSQL.

مُمكَّن افتراضيًا، ولا يسمح هذا الخيار بالقيمة `archive_mode=always` لـ PostgreSQL.

قد تكون مقاطع WAL المدفوعة من خادم استعداد مطابقة منطقيًا لمقاطع WAL المدفوعة من الرئيسي لكن بمجاميع تحقق مختلفة. ويُنصح بتعطيل الأرشفة من مصادر متعددة تجنبًا للتعارض.

تنبيه:

إذا عُطّل هذا الخيار فمن الأهمية بمكان ضمان أن مؤرشفًا واحدًا فقط يكتب إلى المستودع عبر الأمر `archive-push`.

```text
default: y
example: archive-mode-check=n
```

### خيار النسخ الاحتياطي من الاستعداد (`--backup-standby`) {#backup-from-standby-option---backup-standby}

النسخ الاحتياطي من عنقود الاستعداد.

مكّن النسخ الاحتياطي من الاستعداد لتقليل الحمل على العنقود الرئيسي. يتطلب هذا الخيار تهيئة المضيفين الرئيسي والاستعداد معًا.

الأوضاع التالية مدعومة:

- `y` - الاستعداد مطلوب للنسخ الاحتياطي.
- `prefer` - النسخ الاحتياطي من الاستعداد إذا كان متاحًا، وإلا فمن الرئيسي.
- `n` - النسخ الاحتياطي من الرئيسي فقط.

```text
default: n
example: backup-standby=y
```

### خيار مجاميع تحقق الصفحات (`--checksum-page`) {#page-checksums-option---checksum-page}

التحقق من مجاميع تحقق صفحات البيانات.

يوجّه pgBackRest للتحقق من جميع مجاميع تحقق صفحات البيانات أثناء النسخ الاحتياطي لعنقود. ويُمكَّن هذا الخيار تلقائيًا عند تمكين مجاميع تحقق صفحات البيانات على العنقود.

لن تؤدي حالات فشل التحقق من مجاميع التحقق إلى إجهاض نسخة احتياطية، بل ستُصدر تحذيرات في السجل (وإلى وحدة التحكم بالإعدادات الافتراضية)، وستُخزَّن قائمة الصفحات غير الصالحة في بيان النسخة الاحتياطية.

```text
example: checksum-page=n
```

### خيار استثناءات المسارات/الملفات (`--exclude`) {#pathfile-exclusions-option---exclude}

استثناء مسارات/ملفات من النسخة الاحتياطية.

جميع الاستثناءات نسبية إلى `$PGDATA`. فإذا انتهى الاستثناء بـ / فلن تُستثنى إلا الملفات في الدليل المحدد، مثلًا `--exclude=junk/` سيستثني جميع الملفات في الدليل `$PGDATA/junk` لكنه يتضمن الدليل نفسه. وإذا لم ينتهِ الاستثناء بـ / فيجوز أن يطابق الملفُ الاستثناءَ مطابقةً تامة أو مطابقةً مع إلحاق / بالاستثناء، مثلًا `--exclude=junk` سيستثني الدليل `$PGDATA/junk` وجميع الملفات التي يحتويها.

**احترس عند استخدام هذه الميزة — فمن السهل جدًا استثناء شيء حرج يجعل النسخة الاحتياطية غير متسقة. تأكد من اختبار عمليات الاستعادة لديك!**

ستُسجَّل جميع الملفات المستثناة في السجل بمستوى `info` مع قاعدة الاستثناء. فتأكد من تدقيق قائمة الملفات المستثناة لضمان عدم استثناء أي شيء غير متوقع.

ملاحظة:

لا تُحترم الاستثناءات في عمليات الاستعادة التفاضلية (delta). وأي ملفات/دلائل استُثنيت بواسطة النسخة الاحتياطية ستُزال عند الاستعادة التفاضلية.

لا ينبغي استخدام هذا الخيار لاستثناء سجلات PostgreSQL من نسخة احتياطية. يمكن نقل السجلات خارج الدليل `PGDATA` باستخدام إعداد `log_directory` في PostgreSQL، وميزة ذلك السماح بالاحتفاظ بالسجلات بعد الاستعادة.

يجوز تحديد استثناءات متعددة في سطر الأوامر أو في ملف إعداد.

```text
example: exclude=junk/
```

### خيار انتهاء الصلاحية التلقائي (`--expire-auto`) {#expire-auto-option---expire-auto}

تشغيل الأمر `expire` تلقائيًا بعد اكتمال نسخة احتياطية ناجحة.

هذا الإعداد مُمكَّن افتراضيًا. وتوخَّ الحذر عند تعطيل هذا الخيار، إذ سيؤدي ذلك إلى الاحتفاظ بجميع النسخ الاحتياطية والأرشيفات إلى أجل غير مسمى، ما قد يتسبب في نفاد مساحة المستودع. وستحتاج إلى تشغيل الأمر `expire` بانتظام لمنع حدوث ذلك.

عند تشغيل `expire` تلقائيًا بعد نسخة احتياطية ناجحة فإنه يستخدم تهيئة الأمر `backup`، لذا لا تُطبَّق الخيارات المضبوطة في قسم الأمر `expire` فقط (مثل `[global:expire]`). ولتطبيق تهيئة خاصة بالأمر `expire`، عطّل هذا الخيار وشغّل الأمر `expire` منفصلًا.

```text
default: y
example: expire-auto=y
```

### خيار عتبة حفظ البيان (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

عتبة حفظ البيان أثناء النسخ الاحتياطي.

تحدد مدى تكرار حفظ البيان أثناء النسخ الاحتياطي. فحفظ البيان مهم لأنه يخزن مجاميع التحقق ويتيح لخاصية الاستئناف العمل بكفاءة. والعتبة الفعلية المستخدمة هي 1% من حجم النسخة الاحتياطية أو `manifest-save-threshold`، أيهما أكبر.

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### خيار الاستئناف (`--resume`) {#resume-option---resume}

السماح باستئناف نسخة احتياطية فاشلة.

يحدد ما إذا كانت خاصية الاستئناف مُمكَّنة. يمكن للاستئناف أن يقلل كثيرًا من الوقت اللازم لتشغيل نسخة احتياطية بعد فشل نسخة احتياطية سابقة من النوع نفسه. غير أنه يضيف تعقيدًا، لذا قد يكون من المستحسن تعطيله في البيئات التي لا تتطلب هذه الخاصية.

```text
default: y
example: resume=n
```

### خيار البدء السريع (`--start-fast`) {#start-fast-option---start-fast}

فرض نقطة تحقق (checkpoint) لبدء النسخ الاحتياطي بسرعة.

يفرض نقطة تحقق (عن طريق تمرير `y` إلى المعامل `fast` في دالة بدء النسخ الاحتياطي) بحيث تبدأ النسخة الاحتياطية فورًا. وإلا فستبدأ النسخة الاحتياطية بعد نقطة التحقق المنتظمة التالية.

```text
default: n
example: start-fast=y
```

--------

## الخيارات العامة {#general-options}

يُعرِّف قسم `general` الخيارات المشتركة بين العديد من الأوامر.

### خيار السماح بالتشغيل باعتبار المستخدم الجذر (`--allow-root`) {#allow-run-as-root-option---allow-root}

السماح بتشغيل الأمر باعتبار المستخدم الجذر (root).

بشكل افتراضي لا يجوز تشغيل إلا الأمر `restore` باعتبار المستخدم الجذر لأنه مصمم لإدارة ملكية الملفات بعناية. أما تشغيل الأوامر الأخرى باعتبار الجذر فيخاطر بإنشاء ملفات (مثلًا في المستودع) يملكها الجذر ويتعذر على مستخدم PostgreSQL الوصول إليها، ما يتسبب في فشل الأوامر اللاحقة.

مكّن هذا الخيار لتشغيل أمر باعتبار الجذر رغم ذلك. غير أنه من الأفضل بكثير تشغيل pgBackRest باعتبار المستخدم الذي يملك المستودع وعنقود PostgreSQL.

```text
default: n
example: allow-root=y
```

### خيار حجم المخزن المؤقت (`--buffer-size`) {#buffer-size-option---buffer-size}

حجم المخزن المؤقت لعمليات الإدخال/الإخراج.

حجم المخزن المؤقت المستخدم للنسخ والضغط والتشفير وعمليات أخرى. يعتمد عدد المخازن المؤقتة المستخدمة على الخيارات، وقد تستخدم كل عملية ذاكرة إضافية، مثلًا قد يستخدم ضغط `gz` ذاكرة إضافية قدرها 256KiB.

القيم المسموح بها هي `16KiB` و`32KiB` و`64KiB` و`128KiB` و`256KiB` و`512KiB` و`1MiB` و`2MiB` و`4MiB` و`8MiB` و`16MiB`.

```text
default: 1MiB
example: buffer-size=2MiB
```

### خيار أمر pgBackRest (`--cmd`) {#pgbackrest-command-option---cmd}

أمر pgBackRest.

قد يولّد pgBackRest سلسلة أمر، مثلًا عندما يولّد الأمر `restore` إعداد restore_command. سيُستخدم في هذه الحالة الأمرُ المستخدم لتشغيل عملية pgBackRest ما لم يُقدَّم الخيار `cmd`.

تنبيه:

قد يتسبب تغليف أمر pgBackRest في سلوك غير متوقع ولا يُنصح به.

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### خيار أمر عميل SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

أمر عميل SSH.

استخدم أمر عميل SSH محددًا عند الرغبة في بديل أو عندما لا يكون الأمر `ssh` في $PATH.

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### خيار الضغط (`--compress`) {#compress-option---compress}

استخدام ضغط الملفات.

ملفات النسخ الاحتياطي متوافقة مع أدوات الضغط من سطر الأوامر.

هذا الخيار مهمَل الآن. وينبغي استخدام الخيار `compress-type` بدلًا منه.

```text
default: y
example: compress=n
```

### خيار مستوى الضغط (`--compress-level`) {#compress-level-option---compress-level}

مستوى ضغط الملفات.

يعيّن المستوى الذي سيُستخدم لضغط الملفات عندما لا يساوي `compress-type` القيمة `none` أو عندما يكون `compress=y` (مهمَل).

```text
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

example: compress-level=9
```

### خيار مستوى ضغط الشبكة (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

مستوى ضغط الشبكة.

يعيّن مستوى ضغط الشبكة عندما يكون `compress-type=none` ولا يُشغَّل الأمر على المضيف نفسه الذي يوجد به المستودع. يُستخدم الضغط لتقليل حركة مرور الشبكة. وعندما لا يساوي `compress-type` القيمة `none` يُتجاهل الإعداد `compress-level-network` ويُستخدم `compress-level` بدلًا منه بحيث لا يُضغط الملف إلا مرة واحدة.

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### خيار نوع الضغط (`--compress-type`) {#compress-type-option---compress-type}

نوع ضغط الملفات.

أنواع الضغط التالية مدعومة:

- `none` - بلا ضغط
- `bz2` - تنسيق ضغط bzip2
- `gz` - تنسيق ضغط gzip
- `lz4` - تنسيق ضغط lz4 (غير متاح على جميع المنصات)
- `zst` - تنسيق ضغط Zstandard (غير متاح على جميع المنصات)

```text
default: gz
example: compress-type=none
```

### خيار مهلة قاعدة البيانات (`--db-timeout`) {#database-timeout-option---db-timeout}

مهلة استعلام قاعدة البيانات.

يعيّن المهلة، بالثواني، للاستعلامات على قاعدة البيانات. ويشمل ذلك دالتي بدء/إيقاف النسخ الاحتياطي اللتين قد تستغرق كل منهما وقتًا طويلًا. لهذا ينبغي إبقاء المهلة مرتفعة ما لم تكن تعلم أن هذه الدوال ستعود بسرعة (أي إذا ضبطت `start-fast=y` وتعلم أن عنقود قاعدة البيانات لن يولّد مقاطع WAL كثيرة أثناء النسخ الاحتياطي).

ملاحظة:

يجب أن يكون الخيار `db-timeout` أقل من الخيار `protocol-timeout`.

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### خيار الدلتا (`--delta`) {#delta-option---delta}

الاستعادة أو النسخ الاحتياطي باستخدام مجاميع التحقق.

أثناء الاستعادة، يُتوقع افتراضيًا أن تكون دلائل بيانات PostgreSQL ودلائل مساحات الجداول موجودة لكنها فارغة. ينفّذ هذا الخيار استعادة تفاضلية (delta) باستخدام مجاميع التحقق.

وأثناء النسخ الاحتياطي، سيستخدم هذا الخيار مجاميع التحقق بدلًا من الأختام الزمنية لتحديد الملفات التي ستُنسخ.

```text
default: n
example: delta=y
```

### خيار مهلة الإدخال/الإخراج (`--io-timeout`) {#io-timeout-option---io-timeout}

مهلة الإدخال/الإخراج.

المهلة، بالثواني، المستخدمة للاتصالات وعمليات القراءة/الكتابة.

لاحظ أن عملية القراءة/الكتابة بأكملها لا يلزم أن تكتمل ضمن هذه المهلة، لكن يجب تحقيق *بعض* التقدم، حتى لو كان بايتًا واحدًا.

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### خيار مسار الأقفال (`--lock-path`) {#lock-path-option---lock-path}

المسار الذي تُخزَّن فيه ملفات الأقفال.

يوفر مسار الأقفال موقعًا ينشئ فيه pgBackRest ملفات أقفال لمنع تشغيل عمليات متعارضة بشكل متزامن.

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### خيار umask المحايد (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

استخدام umask محايد.

يضبط umask على 0000 بحيث تُنشأ الأوضاع في المستودع بطريقة معقولة. وضع الدليل الافتراضي هو 0750 ووضع الملف الافتراضي هو 0640.

ولاستخدام umask الخاص بالمستخدم المنفِّذ بدلًا من ذلك، حدد `neutral-umask=n` في ملف الإعداد أو `--no-neutral-umask` في سطر الأوامر.

```text
default: y
example: neutral-umask=n
```

### خيار تعيين أولوية العملية (`--priority`) {#set-process-priority-option---priority}

تعيين أولوية العملية.

يحدد مقدار الأولوية (أي قيمة niceness) التي سيمنحها مجدول النواة للعملية. القيم الموجبة تخفض الأولوية والقيم السالبة ترفعها. وفي معظم الحالات لا تمتلك العمليات صلاحية رفع أولويتها.

```text
allowed: [-20, 19]
example: priority=19
```

### خيار الحد الأقصى للعمليات (`--process-max`) {#process-maximum-option---process-max}

الحد الأقصى للعمليات المستخدمة للضغط/النقل.

ستؤدي كل عملية الضغطَ والنقل لتسريع تشغيل الأمر، لكن لا تضبط `process-max` إلى حد يؤثر في أداء قاعدة البيانات.

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### خيار مهلة البروتوكول (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

مهلة البروتوكول.

يعيّن المهلة، بالثواني، التي ستنتظرها العملية المحلية أو البعيدة وصولَ رسالة جديدة عبر طبقة البروتوكول. ويمنع ذلك العمليات من الانتظار إلى ما لا نهاية لرسالة.

ملاحظة:

يجب أن يكون الخيار `protocol-timeout` أكبر من الخيار `db-timeout`.

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### خيار Keep Alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

تمكين رسائل البقاء (keep-alive).

يمكّن رسائل keep-alive على اتصالات المقابس.

```text
default: y
example: sck-keep-alive=n
```

### خيار مسار الـ Spool (`--spool-path`) {#spool-path-option---spool-path}

المسار الذي تُخزَّن فيه البيانات العابرة.

يُستخدم هذا المسار لتخزين البيانات للأمرين غير المتزامنين `archive-push` و`archive-get`.

يكتب الأمر `archive-push` غير المتزامن إشعارات الاستلام في مسار الـ spool عند تخزينه WAL في الأرشيف بنجاح (وأخطاءً عند الفشل) بحيث تستطيع العملية الأمامية إبلاغ PostgreSQL سريعًا. وملفات إشعارات الاستلام صغيرة جدًا (صفرية عند النجاح وبضع مئات من البايتات عند الخطأ).

يضع الأمر `archive-get` غير المتزامن WAL في قائمة انتظار ضمن مسار الـ spool بحيث يمكن توفيره بسرعة كبيرة عندما تطلبه PostgreSQL. ويكون نقل الملفات إلى PostgreSQL أكثر كفاءة عندما يكون مسار الـ spool على نظام الملفات نفسه الذي يوجد عليه `pg_xlog`/`pg_wal`. غير أنه لا يُنصح بوضع مسار الـ spool *داخل* الدليل `pg_xlog`/`pg_wal` لأن ذلك قد يسبب مشكلات لأدوات PostgreSQL مثل `pg_rewind`.

البيانات المخزنة في مسار الـ spool ليست مؤقتة بشكل صارم، إذ يمكنها ويجب أن تصمد أمام إعادة التشغيل. ومع ذلك فإن فقدان البيانات في مسار الـ spool ليس مشكلة؛ فببساطة سيعيد pgBackRest التحقق من كل مقطع WAL لضمان أرشفته بأمان من أجل `archive-push`، وسيعيد بناء قائمة الانتظار من أجل `archive-get`.

الغرض من مسار الـ spool أن يقع على نظام ملفات محلي متوافق مع Posix، لا على نظام ملفات بعيد مثل NFS أو CIFS.

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### خيار عدد رسائل البقاء (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

عدد رسائل keep-alive.

يحدد عدد رسائل TCP keep-alive التي يمكن فقدانها قبل اعتبار الاتصال ميتًا.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPCNT`.

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### خيار خمول رسائل البقاء (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

زمن خمول رسائل keep-alive.

يحدد مقدار الوقت (بالثواني) بلا أي نشاط شبكي ينبغي بعده أن يرسل نظام التشغيل رسالة TCP keep-alive.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPIDLE`.

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### خيار الفاصل بين رسائل البقاء (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

زمن الفاصل بين رسائل keep-alive.

يحدد مقدار الوقت (بالثواني) الذي ينبغي بعده إعادة إرسال رسالة TCP keep-alive لم يُعترف باستلامها.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPINTVL`.

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### خيار حزم تشفير TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

حزم التشفير المسموح بها لـ TLSv1.2.

جميع اتصالات TLS بين عميل وخادم pgBackRest مشفرة. وافتراضيًا تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

ملاحظة:

الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل حزم التشفير المقبولة عند الحاجة. والمثال خيار معقول ما لم تكن لديك متطلبات أمنية محددة. وإذا تُرك دون ضبط (وهو الافتراضي)، تُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### خيار حزم تشفير TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

حزم التشفير المسموح بها لـ TLSv1.3.

جميع اتصالات TLS بين عميل وخادم pgBackRest مشفرة. وافتراضيًا تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

ملاحظة:

الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل حزم التشفير المقبولة عند الحاجة. وإذا تُرك دون ضبط (وهو الافتراضي)، تُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## خيارات السجل {#log-options}

يُعرِّف قسم `log` الإعدادات المتعلقة بالسجلات.

تحذير:

قد يكشف التسجيل بمستوى trace أسرارًا مثل المفاتيح وكلمات المرور. فاستخدمه بحذر!

### خيار مستوى سجل وحدة التحكم (`--log-level-console`) {#console-log-level-option---log-level-console}

المستوى للتسجيل في وحدة التحكم.

مستويات السجل التالية مدعومة:

- `off` - لا تسجيل إطلاقًا (غير موصى به)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```text
default: warn
example: log-level-console=error
```

### خيار مستوى سجل الملف (`--log-level-file`) {#file-log-level-option---log-level-file}

المستوى للتسجيل في الملف.

مستويات السجل التالية مدعومة:

- `off` - لا تسجيل إطلاقًا (غير موصى به)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```text
default: info
example: log-level-file=debug
```

### خيار مستوى سجل الأخطاء القياسية (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

المستوى للتسجيل في stderr.

يحدد مستويات السجل التي ستُخرَج إلى `stderr` بدلًا من `stdout` (الذي يحدده `log-level-console`). ولن يُخرَج الختم الزمني والعملية إلى `stderr`.

مستويات السجل التالية مدعومة:

- `off` - لا تسجيل إطلاقًا (غير موصى به)
- `error` - تسجيل الأخطاء فقط
- `warn` - تسجيل التحذيرات والأخطاء
- `info` - تسجيل المعلومات والتحذيرات والأخطاء
- `detail` - تسجيل التفاصيل والمعلومات والتحذيرات والأخطاء
- `debug` - تسجيل التصحيح والتفاصيل والمعلومات والتحذيرات والأخطاء
- `trace` - تسجيل التتبع (تصحيح مطوَّل جدًا) والتصحيح والمعلومات والتحذيرات والأخطاء

```text
default: off
example: log-level-stderr=error
```

### خيار مسار السجل (`--log-path`) {#log-path-option---log-path}

المسار الذي تُخزَّن فيه ملفات السجل.

يوفر مسار السجل موقعًا يخزن فيه pgBackRest ملفات السجل. ولاحظ أنه إذا كان `log-level-file=off` فلا حاجة إلى مسار سجل.

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### خيار تسجيل العمليات الفرعية (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

تمكين التسجيل في العمليات الفرعية.

مكّن تسجيل الملف لأي عمليات فرعية تنشئها هذه العملية باستخدام مستوى السجل الذي يحدده `log-level-file`.

```text
default: n
example: log-subprocess=y
```

### خيار الختم الزمني للسجل (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

تمكين الختم الزمني في التسجيل.

يمكّن الختم الزمني في التسجيل لوحدة التحكم والملفات. ويُعطَّل هذا الخيار في مواقف خاصة مثل توليد الوثائق.

```text
default: y
example: log-timestamp=n
```

--------

## خيارات المشرف (Maintainer) {#maintainer-options}

الغرض من خيارات المشرف دعم النسخ المشتقة (forks) من PostgreSQL. وينبغي أن يحدد مشرف النسخة المشتقة الإعدادات الصحيحة ثم يبلّغها لمستخدمي النسخة المشتقة.

تحذير:

قد يؤدي الاستخدام غير الصحيح لهذه الخيارات إلى سلوك غير متوقع أو إتلاف البيانات.

ومن مسؤولية مشرف النسخة المشتقة اختبار pgBackRest مع الخيارات المطلوبة. ولا يضمن pgBackRest التوافق مع أي نسخة مشتقة.

### خيار فحص ترويسات WAL (`--archive-header-check`) {#check-wal-headers-option---archive-header-check}

فحص إصدار/معرّف PostgreSQL في ترويسات WAL.

مُمكَّن افتراضيًا، يفحص هذا الخيار ترويسة WAL مقابل إصدار PostgreSQL ومعرّف النظام لضمان نسخ WAL إلى الـ stanza الصحيحة. ويأتي ذلك إضافةً إلى مطابقة `pg_control` مع الـ stanza والتحقق من أن WAL يُنسَخ من دليل بيانات PostgreSQL نفسه الذي يقع فيه `pg_control`.

ولذلك فإن تعطيل هذا الفحص آمن إلى حدٍّ ما، لكن لا ينبغي اللجوء إليه إلا عند الحاجة، مثلًا إذا كان WAL مشفرًا.

```text
default: y
example: archive-header-check=n
```

### خيار فحص ترويسة الصفحة (`--page-header-check`) {#page-header-check-option---page-header-check}

فحص ترويسات صفحات PostgreSQL.

مُمكَّن افتراضيًا، يضيف هذا الخيار فحوص ترويسة الصفحات.

وينبغي تجنب تعطيل هذا الخيار إلا عند الضرورة، مثلًا إذا كانت الصفحات مشفرة.

```text
default: y
example: page-header-check=n
```

### خيار فرض إصدار PostgreSQL (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

فرض إصدار PostgreSQL.

سيُستخدم إصدار PostgreSQL المحدد بدلًا من الإصدار المكتشف تلقائيًا بقراءة `pg_control` أو ترويسات WAL. ويفيد ذلك أساسًا في النسخ المشتقة من PostgreSQL أو الإصدارات التطويرية التي تختلف فيها تلك القيم عن الإصدار الرسمي. ويجب أن يطابق الإصدارُ الذي يبلّغ عنه PostgreSQL عبر `server_version_num` الإصدارَ المفروض.

تحذير:

كن حذرًا عند استخدام هذا الخيار، لأن `pg_control` وترويسات WAL ستُقرآن مع ذلك بالتنسيق المتوقع للإصدار المحدد، أي التنسيق الخاص بالإصدار الرسمي مفتوح المصدر من PostgreSQL. فإذا غيّرت النسخة المشتقة أو الإصدار التطويري تنسيق الحقول التي يعتمد عليها pgBackRest فسيؤدي ذلك إلى سلوك غير متوقع. وبشكل عام، لن يعمل هذا الخيار كما هو متوقع إلا إذا أضافت النسخة المشتقة جميع أعضاء البُنى (struct) المخصصة *بعد* أعضاء PostgreSQL القياسية.

```text
example: pg-version-force=15
```

--------

## خيارات المستودع {#repository-options}

يُعرِّف قسم `repository` الخيارات المستخدمة لتهيئة المستودع.

**الفهرسة**: جميع الخيارات `repo-` مفهرسة للسماح بتهيئة مستودعات متعددة. فمثلًا، يُهيَّأ مستودع واحد بالخيارين `repo1-path` و`repo1-host` وغيرهما. وإذا هُيّئ أكثر من مستودع ولم يُحدَّد الخيار `--repo` لأمر ما، فستُنفَّذ الإجراءات على المستودعات بترتيب الأولوية الأعلى (مثلًا repo1 ثم repo2).

تُعرِّف خيارات `repo-retention-*` مدة الاحتفاظ بالنسخ الاحتياطية. ولا يحدث انتهاء الصلاحية إلا عندما يتجاوز عدد النسخ الاحتياطية الكاملة الاحتفاظَ المسموح به. بعبارة أخرى، إذا ضُبط `repo1-retention-full-type` على `count` (الافتراضي) وضُبط `repo1-retention-full` على 2، فيجب أن توجد 3 نسخ احتياطية كاملة قبل أن تنتهي صلاحية الأقدم. وإذا ضُبط `repo1-retention-full-type` على `time` فإن `repo1-retention-full` يمثل أيامًا، فيجب أن تكون هناك نسخ احتياطية كاملة تغطي ذلك العدد من الأيام على الأقل قبل أن يمكن انتهاء الصلاحية. واحرص دائمًا على توفر مساحة كافية لعدد النسخ الاحتياطية المحدد بالاحتفاظ + 1.

### خيار حساب مستودع Azure (`--repo-azure-account`) {#azure-repository-account-option---repo-azure-account}

حساب مستودع Azure.

حساب Azure المستخدم لتخزين المستودع.

```text
example: repo1-azure-account=pg-backup
```

### خيار حاوية مستودع Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

حاوية مستودع Azure.

حاوية Azure المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها Azure في الحاوية أيضًا.

```text
example: repo1-azure-container=pg-backup
```

### خيار نقطة نهاية مستودع Azure (`--repo-azure-endpoint`) {#azure-repository-endpoint-option---repo-azure-endpoint}

نقطة نهاية مستودع Azure.

نقطة النهاية المستخدمة للاتصال بخدمة الكائنات الثنائية كبيرة الحجم (blob). والقيمة الافتراضية صحيحة عمومًا ما لم تكن تستخدم Azure Government.

بالنسبة إلى التهيئات المخصصة/الاختبارية، قد تكون الخيارات `repo-storage-ca-file` و`repo-storage-ca-path` و`repo-storage-host` و`repo-storage-port` و`repo-storage-verify-tls` مفيدة.

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### خيار مفتاح مستودع Azure (`--repo-azure-key`) {#azure-repository-key-option---repo-azure-key}

مفتاح مستودع Azure.

مفتاح مشترك أو توقيع وصول مشترك تبعًا للخيار `repo-azure-key-type`.

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### خيار نوع مفتاح مستودع Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

نوع مفتاح مستودع Azure.

الأنواع التالية مدعومة للتخويل:

- `shared` - مفتاح مشترك
- `sas` - توقيع وصول مشترك
- `auto` - التخويل تلقائيًا باستخدام الهويات المدارة لـ Azure

```text
default: shared
example: repo1-azure-key-type=sas
```

### خيار نمط URI لمستودع Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

نمط URI لـ Azure.

أنماط URI التالية مدعومة:

- `host` - الاتصال بالمضيف `account.endpoint`.
- `path` - الاتصال بالمضيف `endpoint` وإضافة اسم الحساب في بداية عناوين URI.

```text
default: host
example: repo1-azure-uri-style=path
```

### خيار النسخ الاحتياطي التزايدي بالكتل (`--repo-block`) {#block-incremental-backup-option---repo-block}

تمكين النسخ الاحتياطي التزايدي بالكتل.

تتيح الكتلُ التزايدية نسخًا احتياطية أكثر دقة عبر تقسيم الملفات إلى كتل يمكن النسخ الاحتياطي لها بشكل مستقل. ويوفر ذلك مساحة في المستودع ويمكن أن يحسّن أداء الاستعادة التفاضلية (delta) لأنه يمكن جلب كتل مفردة دون قراءة الملف بأكمله من المستودع.

ملاحظة:

يجب تمكين الخيار `repo-bundle` قبل تمكين `repo-block`.

يُحدَّد حجم الكتلة للملف استنادًا إلى حجم الملف وعمره. وعمومًا ستحصل الملفات الأقدم/الأكبر على أحجام كتل أكبر. وإذا كان الملف قديمًا بما يكفي فلن يُنسخ احتياطيًا باستخدام الكتل التزايدية.

تكون الكتل التزايدية أكثر كفاءة عند تمكينها لجميع أنواع النسخ الاحتياطية، بما فيها الكاملة. ويجعل ذلك النسخة الكاملة أكبر قليلًا، لكن النسخ الاحتياطية التفاضلية والتزايدية اللاحقة تستطيع الاستفادة من خرائط الكتل التي ولّدتها النسخة الكاملة لتوفير المساحة.

```text
default: n
example: repo1-block=y
```

### خيار حزم المستودع (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

تجميع الملفات في المستودع.

يجمع (يدمج) الملفات الأصغر لتقليل العدد الإجمالي للملفات المكتوبة إلى المستودع. فكتابة ملفات أقل أكثر كفاءة عمومًا، لا سيما في مخازن الكائنات مثل S3. وإضافةً إلى ذلك، لا تُخزَّن الملفات الصفرية الطول (إلا في البيان)، ما يوفر الوقت والمساحة.

```text
default: n
example: repo1-bundle=y
```

### خيار حد حزم المستودع (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

الحد لملفات الحزم.

حد الحجم للملفات التي ستُضم إلى الحزم. أما الملفات الأكبر من هذا الحجم فستُخزَّن بشكل منفصل.

لا يمكن إعادة استخدام الملفات المحزمة عند استئناف نسخة احتياطية، لذا يتحكم هذا الخيار في الملفات التي يمكن استئنافها، أي أن القيم الأعلى تؤدي إلى ملفات أقل قابلة للاستئناف.

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### خيار حجم حزم المستودع (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

الحجم الهدف لحزم الملفات.

يحدد الحجم الهدف للملفات التي ستُضاف إلى حزمة واحدة. وقد يبلغ حجم الحزمة غير المضغوطة `repo-bundle-size` + `repo-bundle-limit`، لذا لا تضبط هذا الخيار على الحجم الأقصى الذي يسمح به نظام ملفاتك.

عمومًا ليس من الجيد ضبط هذا الخيار على قيمة مرتفعة جدًا لأن إعادة المحاولة ستضطر إلى إعادة الحزمة بأكملها.

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### خيار عبارة مرور تشفير المستودع (`--repo-cipher-pass`) {#repository-cipher-passphrase-option---repo-cipher-pass}

عبارة مرور تشفير المستودع.

عبارة المرور المستخدمة لتشفير/فك تشفير ملفات المستودع.

ملاحظة:

عند التشغيل دون الخيار `stanza` يقرأ الأمر `info` إعدادات التشفير من قسم `global` فقط. فإذا هُيئت إعدادات التشفير لكل stanza على حدة، فشغّل الأمر `info` مع الخيار `stanza` لقراءة stanza مشفرة.

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### خيار نوع تشفير المستودع (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

التشفير المستخدم لتشفير المستودع.

أنواع التشفير التالية مدعومة:

- `none` - المستودع غير مشفر
- `aes-256-cbc` - معيار التشفير المتقدم بطول مفتاح 256 بتًا

لاحظ أن التشفير يُنفَّذ دائمًا لدى العميل حتى لو كان نوع المستودع (مثل S3) يدعم التشفير.

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### خيار حاوية مستودع GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

حاوية مستودع GCS.

حاوية GCS المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها GCS في الحاوية أيضًا.

```text
example: repo1-gcs-bucket=/pg-backup
```

### خيار نقطة نهاية مستودع GCS (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

نقطة نهاية مستودع GCS.

نقطة النهاية المستخدمة للاتصال بخدمة التخزين. ويجوز تحديثها لاستخدام خادم GCS محلي أو نقطة نهاية بديلة.

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### خيار مفتاح مستودع GCS (`--repo-gcs-key`) {#gcs-repository-key-option---repo-gcs-key}

مفتاح مستودع GCS.

رمز مميز (token) أو ملف مفتاح خدمة تبعًا للخيار `repo-gcs-key-type`.

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### خيار نوع مفتاح مستودع GCS (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

نوع مفتاح مستودع GCS.

الأنواع التالية مدعومة للتخويل:

- `auto` - التخويل باستخدام حساب الخدمة للنسخة (instance).
- `service` - حساب خدمة من مفتاح مخزن محليًا.
- `token` - للاختبار المحلي، مثل `fakegcs`.

عند `repo-gcs-key-type=service` ستُعاد قراءة بيانات الاعتماد عند تجديد الرمز المميز للمصادقة.

```text
default: service
example: repo1-gcs-key-type=auto
```

### خيار معرّف مشروع GCS (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

معرّف مشروع GCS.

معرّف مشروع GCS المستخدم لتحديد فوترة الطلبات.

```text
example: repo1-gcs-user-project=my-project
```

### خيار الروابط الصلبة في المستودع (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

إنشاء روابط صلبة للملفات بين النسخ الاحتياطية في المستودع.

يمكّن الربط الصلب للملفات في النسخ الاحتياطية التفاضلية والتزايدية بنسخها الكاملة. ويوفر ذلك مظهرًا بأن كل نسخة احتياطية نسخة كاملة على مستوى نظام الملفات. لكن احترس، لأن تعديل الملفات المرتبطة ارتباطًا صلبًا يمكن أن يؤثر في جميع النسخ الاحتياطية في المجموعة.

```text
default: n
example: repo1-hardlink=y
```

الاسم المهمل: hardlink

### خيار مضيف المستودع (`--repo-host`) {#repository-host-option---repo-host}

مضيف المستودع عند التشغيل عن بُعد.

عند النسخ الاحتياطي والأرشفة إلى نظام ملفات مثبت محليًا، لا يلزم هذا الإعداد.

```text
example: repo1-host=repo1.domain.com
```

الاسم المهمل: backup-host

### خيار ملف هيئة شهادات مضيف المستودع (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

ملف هيئة شهادات مضيف المستودع.

استخدم ملف CA غير الافتراضي للنظام للاتصال بمضيف المستودع.

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة شهادات مضيف المستودع (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

مسار هيئة شهادات مضيف المستودع.

استخدم مسار CA غير الافتراضي للنظام للاتصال بمضيف المستودع.

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### خيار ملف شهادة مضيف المستودع (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

ملف شهادة مضيف المستودع.

يُرسَل إلى مضيف المستودع لإثبات هوية العميل.

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### خيار أمر مضيف المستودع (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

أمر pgBackRest على مضيف المستودع.

مطلوب فقط إذا كان المسار إلى أمر pgBackRest مختلفًا على المضيفين المحلي ومضيف المستودع. وإذا لم يُعرَّف، فسيُضبط أمر مضيف المستودع مثل الأمر المحلي نفسه.

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

الاسم المهمل: backup-cmd

### خيار إعداد مضيف المستودع (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

ملف إعداد pgBackRest لمضيف المستودع.

يعيّن موقع ملف الإعداد على مضيف المستودع. وهذا مطلوب فقط إذا كان ملف إعداد مضيف المستودع في موقع مختلف عن ملف الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

الاسم المهمل: backup-config

### خيار مسار تضمين إعداد مضيف المستودع (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

مسار تضمين إعداد pgBackRest لمضيف المستودع.

يعيّن موقع مسار تضمين الإعداد على مضيف المستودع. وهذا مطلوب فقط إذا كان مسار تضمين إعداد مضيف المستودع في موقع مختلف عن مسار تضمين الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار إعداد مضيف المستودع (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

مسار إعداد pgBackRest لمضيف المستودع.

يعيّن موقع مسار الإعداد على مضيف المستودع. وهذا مطلوب فقط إذا كان مسار إعداد مضيف المستودع في موقع مختلف عن مسار الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### خيار ملف مفتاح مضيف المستودع (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

ملف مفتاح مضيف المستودع.

يثبت أن شهادة العميل أرسلها مالكها.

```text
example: repo1-host-key-file=/path/to/client.key
```

### خيار منفذ مضيف المستودع (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

منفذ مضيف المستودع عندما يكون `repo-host` مضبوطًا.

استخدم هذا الخيار لتحديد منفذ غير افتراضي لبروتوكول مضيف المستودع.

ملاحظة:

عند `repo-host-type=ssh` لا توجد قيمة افتراضية لـ `repo-host-port`. وفي هذه الحالة سيكون المنفذ هو ما هو مهيأ للأمر الذي يحدده `cmd-ssh`.

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

الاسم المهمل: backup-ssh-port

### خيار نوع بروتوكول مضيف المستودع (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

نوع بروتوكول مضيف المستودع.

أنواع البروتوكول التالية مدعومة:

- `ssh` - Secure Shell.
- `tls` - خادم TLS لـ pgBackRest.

```text
default: ssh
example: repo1-host-type=tls
```

### خيار مستخدم مضيف المستودع (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

مستخدم مضيف المستودع عندما يكون `repo-host` مضبوطًا.

يحدد المستخدم الذي سيُستخدم للعمليات على مضيف المستودع. ويُفضَّل ألا يكون هذا هو المستخدم `postgres` بل مستخدمًا آخر مثل `pgbackrest`. فإذا كانت PostgreSQL تعمل على مضيف المستودع، يمكن وضع المستخدم `postgres` في مجموعة `pgbackrest` ليحصل على أذونات القراءة على المستودع دون أن يستطيع إتلاف محتوياته سهوًا.

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

الاسم المهمل: backup-user

### خيار مسار المستودع (`--repo-path`) {#repository-path-option---repo-path}

المسار الذي تُخزَّن فيه النسخ الاحتياطية والأرشيف.

المستودع هو المكان الذي يخزن فيه pgBackRest النسخ الاحتياطية ويؤرشف فيه مقاطع WAL.

قد يصعب تقدير المساحة التي ستحتاجها مسبقًا. وأفضل ما يمكن فعله هو أخذ بعض النسخ الاحتياطية ثم تسجيل أحجام الأنواع المختلفة من النسخ الاحتياطية (full/incr/diff) وقياس مقدار WAL المولَّد يوميًا. سيمنحك ذلك فكرة عامة عن المساحة التي ستحتاجها، وإن كانت المتطلبات ستتغير على الأرجح مع مرور الوقت مع تطور قاعدة بياناتك بالطبع.

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### خيار الاحتفاظ بالأرشيف (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

عدد النسخ الاحتياطية بما يعادلها من WAL المتواصل الذي يُحتفظ به.

ملاحظة:

مقاطع WAL المطلوبة لجعل نسخة احتياطية متسقة يُحتفظ بها دائمًا حتى انتهاء صلاحية النسخة الاحتياطية بصرف النظر عن كيفية تهيئة هذا الخيار.

إذا لم تُضبط هذه القيمة وكان `repo-retention-full-type` هو `count` (الافتراضي)، فستكون قيمة انتهاء صلاحية الأرشيف الافتراضية هي قيمة `repo-retention-full` (أو `repo-retention-diff`) المقابلة لـ `repo-retention-archive-type` إذا ضُبطت على `full` (أو `diff`). ويضمن ذلك عدم انتهاء صلاحية WAL إلا لنسخ احتياطية انتهت صلاحيتها بالفعل. وإذا كان `repo-retention-full-type` هو `time`، فستكون القيمة الافتراضية إزالة الأرشيفات الأسبق من أقدم نسخة كاملة يُحتفظ بها بعد تلبية إعداد `repo-retention-full`.

يجب ضبط هذا الخيار إذا ضُبط `repo-retention-archive-type` على `incr`. وإذا كانت مساحة القرص شحيحة، فيمكن استخدام هذا الإعداد، بالاقتران مع `repo-retention-archive-type`، لإنهاء صلاحية مقاطع WAL بوتيرة شرسة. غير أن ذلك يُلغي إمكانية إجراء الاستعادة إلى نقطة زمنية (PITR) من النسخ الاحتياطية ذات WAL منتهي الصلاحية، ولذلك **لا** يُنصح به.

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

الاسم المهمل: retention-archive

### خيار نوع الاحتفاظ بالأرشيف (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

نوع النسخة الاحتياطية لاحتفاظ WAL.

إذا ضُبط على `full` فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة الذي يحدده `repo-retention-archive`. وإذا ضُبط على `diff` (تفاضلية) فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة والتفاضلية الذي يحدده `repo-retention-archive`، أي أنه إذا كانت آخر نسخة احتياطية مأخوذة نسخة كاملة، فستُحتسب تفاضلية لأغراض repo-retention. وإذا ضُبط على `incr` (تزايدية) فسيحتفظ pgBackRest بسجلات الأرشيف بعدد النسخ الاحتياطية الكاملة والتفاضلية والتزايدية الذي يحدده `repo-retention-archive`. ويُستحسن عدم تغيير هذا الإعداد عن قيمته الافتراضية التي تنهي صلاحية WAL فقط بالاقتران مع إنهاء صلاحية النسخ الاحتياطية الكاملة.

```text
default: full
example: repo1-retention-archive-type=diff
```

الاسم المهمل: retention-archive-type

### خيار الاحتفاظ التفاضلي (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

عدد النسخ الاحتياطية التفاضلية التي يُحتفظ بها.

عند انتهاء صلاحية نسخة احتياطية تفاضلية، ستنتهي صلاحية جميع النسخ الاحتياطية التزايدية المرتبطة بها أيضًا. وعندما لا يُعرَّف، سيُحتفظ بجميع النسخ الاحتياطية التفاضلية حتى تنتهي صلاحية النسخ الكاملة التي تعتمد عليها.

لاحظ أن النسخ الاحتياطية الكاملة تُحتسب ضمن عدد النسخ الاحتياطية التفاضلية لأغراض انتهاء الصلاحية. ويقلل ذلك قليلًا عدد النسخ الاحتياطية التفاضلية الواجب الاحتفاظ بها في معظم الحالات.

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

الاسم المهمل: retention-diff

### خيار الاحتفاظ الكامل (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

عدد/مدة الاحتفاظ بالنسخ الاحتياطية الكاملة.

عند انتهاء صلاحية نسخة احتياطية كاملة، ستنتهي صلاحية جميع النسخ الاحتياطية التفاضلية والتزايدية المرتبطة بها أيضًا. وعندما لا يُعرَّف الخيار سيُصدر تحذير. وإذا رغبت في الاحتفاظ إلى أجل غير مسمى فاضبط الخيار على القيمة القصوى.

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

الاسم المهمل: retention-full

### خيار نوع الاحتفاظ الكامل (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

نوع الاحتفاظ للنسخ الاحتياطية الكاملة.

يحدد ما إذا كان إعداد `repo-retention-full` يمثل مدة زمنية (أيامًا) أم عدد نسخ احتياطية كاملة يُحتفظ بها.

إذا ضُبط على `time` فستُزال من المستودع النسخ الاحتياطية الكاملة الأقدم من `repo-retention-full` إذا وُجدت نسخة احتياطية أخرى تساوي إعداد `repo-retention-full` أو تتجاوزه. فمثلًا، إذا كان `repo-retention-full` هو 30 (يومًا) وكانت هناك نسختان كاملتان: واحدة عمرها 25 يومًا وأخرى عمرها 35 يومًا، فلن تنتهي صلاحية أي نسخة كاملة، لأن إنهاء صلاحية النسخة ذات العمر 35 يومًا سيُبقي النسخة ذات العمر 25 يومًا فقط، بما ينتهك سياسة الاحتفاظ لمدة 30 يومًا التي تشترط وجود نسخة احتياطية واحدة بعمر 30 يومًا على الأقل قبل إنهاء صلاحية نسخة أقدم. وتنتهي صلاحية WAL المؤرشف الأقدم من أقدم نسخة كاملة متبقية تلقائيًا ما لم يُضبط `repo-retention-archive-type` و`repo-retention-archive` صراحةً.

وإذا ضُبط على `count` فستُنهى صلاحية النسخ الاحتياطية الكاملة التي تتجاوز `repo-retention-full`. فمثلًا، إذا كان `repo-retention-full` هو `4` واكتملت نسخة احتياطية كاملة خامسة، فستُنهى صلاحية أقدم نسخة كاملة للإبقاء على العدد 4.

لاحظ أنه يجب أن تكتمل النسخة الاحتياطية بنجاح قبل أن تُؤخذ في الاعتبار للاحتفاظ. فمثلًا، إذا كان `repo-retention-full-type` هو `count` و`repo-retention-full` هو `2`، فيجب أن توجد 3 نسخ احتياطية كاملة قبل أن تُنهى صلاحية الأقدم.

```text
default: count
example: repo1-retention-full-type=time
```

### خيار الاحتفاظ بسجل النسخ الاحتياطية (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

عدد أيام بيانات سجل النسخ الاحتياطية التي يُحتفظ بها.

تُخزَّن نسخة من بيان النسخة الاحتياطية في المسار `backup.history` عند اكتمال النسخة الاحتياطية. وافتراضيًا لا تنتهي صلاحية هذه الملفات أبدًا لأنها مفيدة لتنقيب البيانات، مثل قياس نمو النسخ الاحتياطية وWAL بمرور الوقت.

اضبط `repo-retention-history` لتحديد عدد أيام بيانات سجل النسخ الاحتياطية التي يُحتفظ بها. والنسخ الاحتياطية غير منتهية الصلاحية يُحتفظ بها دائمًا في سجل النسخ الاحتياطية. وحدد `repo-retention-history=0` للاحتفاظ بسجل النسخ الاحتياطية للنسخ غير منتهية الصلاحية فقط.

عند انتهاء صلاحية بيان سجل نسخة احتياطية كاملة، تنتهي صلاحية جميع بيانات سجل النسخ الاحتياطية التفاضلية والتزايدية المرتبطة بالنسخة الكاملة أيضًا.

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### خيار حاوية مستودع S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

حاوية مستودع S3.

حاوية S3 المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها AWS في الحاوية أيضًا.

```text
example: repo1-s3-bucket=pg-backup
```

### خيار نقطة نهاية مستودع S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

نقطة نهاية مستودع S3.

ينبغي أن تكون نقطة نهاية AWS صالحة للمنطقة المحددة.

بالنسبة إلى التهيئات المخصصة/الاختبارية، قد تكون الخيارات `repo-storage-ca-file` و`repo-storage-ca-path` و`repo-storage-host` و`repo-storage-port` و`repo-storage-verify-tls` مفيدة.

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### خيار مفتاح الوصول لمستودع S3 (`--repo-s3-key`) {#s3-repository-access-key-option---repo-s3-key}

مفتاح الوصول لمستودع S3.

مفتاح AWS المستخدم للوصول إلى هذه الحاوية.

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### خيار مفتاح الوصول السري لمستودع S3 (`--repo-s3-key-secret`) {#s3-repository-secret-access-key-option---repo-s3-key-secret}

مفتاح الوصول السري لمستودع S3.

المفتاح السري لـ AWS المستخدم للوصول إلى هذه الحاوية.

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### خيار نوع مفتاح مستودع S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

نوع مفتاح مستودع S3.

الأنواع التالية مدعومة:

- `shared` - مفاتيح مشتركة
- `auto` - استرداد بيانات اعتماد مؤقتة تلقائيًا
- `web-id` - استرداد بيانات اعتماد هوية الويب تلقائيًا
- `pod-id` - استرداد بيانات اعتماد هوية pod في EKS تلقائيًا
- `process` - استرداد بيانات الاعتماد بتنفيذ عملية

```text
default: shared
example: repo1-s3-key-type=auto
```

### خيار معرّف مفتاح KMS لمستودع S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

مفتاح KMS لمستودع S3.

يمكّن تشفير S3 من جانب الخادم باستخدام مفتاح خدمة إدارة المفاتيح المحدد من AWS.

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### خيار أمر عملية مصادقة S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

أمر عملية مصادقة S3.

الأمر (والوسائط الاختيارية) المطلوب تنفيذه لاسترداد بيانات اعتماد S3 مؤقتة. أول عنصر في القائمة هو الأمر، وتُمرَّر العناصر المتبقية كمعاملات.

يجب أن تُخرج العملية JSON يحتوي الحقول `AccessKeyId` و`SecretAccessKey` و`SessionToken` و`Expiration`. وستُجدَّد بيانات الاعتماد تلقائيًا قبل وقت انتهاء الصلاحية. راجع [موفر بيانات اعتماد العملية](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) لتفاصيل التنسيق.

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### خيار منطقة مستودع S3 (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

منطقة مستودع S3.

منطقة AWS التي أُنشئت فيها الحاوية.

```text
example: repo1-s3-region=us-east-1
```

### خيار "الطالب يدفع" لمستودع S3 (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

خاصية الطالب يدفع (requester pays) لمستودع S3.

يمكّن خاصية requester pays في S3.

```text
default: n
example: repo1-s3-requester-pays=n
```

### خيار دور مستودع S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

دور مستودع S3.

اسم دور AWS (وليس ARN الكامل) المستخدم لاسترداد بيانات اعتماد مؤقتة عندما يكون `repo-s3-key-type=auto`.

```text
example: repo1-s3-role=authrole
```

### خيار خدمة مستودع S3 (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

خدمة توقيع S3.

خدمة توقيع S3 المستخدمة في مصادقة SigV4. والقيمة الافتراضية `s3` لنقاط النهاية القياسية لـ S3. اضبطها على `s3-outposts` عند استخدام نقطة نهاية S3 Outposts.

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### خيار مفتاح عميل SSE لمستودع S3 (`--repo-s3-sse-customer-key`) {#s3-repository-sse-customer-key-option---repo-s3-sse-customer-key}

مفتاح عميل SSE لمستودع S3.

يمكّن تشفير S3 من جانب الخادم باستخدام مفتاح العميل المحدد.

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### خيار نقطة نهاية STS لمستودع S3 (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

نقطة نهاية STS لمستودع S3.

نقطة نهاية STS المستخدمة لاسترداد بيانات اعتماد مؤقتة عند تهيئة `repo-s3-key-type=web-id`. اضبطها على نقطة نهاية إقليمية (مثل `sts.us-east-1.amazonaws.com`) لاستخدام STS الإقليمي، وقد يكون ذلك مطلوبًا لـ GovCloud أو المناطق الصينية أو لتقليل زمن الاستجابة.

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### خيار رمز الأمان لمستودع S3 (`--repo-s3-token`) {#s3-repository-security-token-option---repo-s3-token}

رمز الأمان لمستودع S3.

رمز أمان AWS المستخدم مع بيانات الاعتماد المؤقتة.

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### خيار نمط URI لمستودع S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

نمط URI لـ S3.

أنماط URI التالية مدعومة:

- `host` - الاتصال بالمضيف `bucket.endpoint`.
- `path` - الاتصال بالمضيف `endpoint` وإضافة اسم الحاوية في بداية عناوين URI.

```text
default: host
example: repo1-s3-uri-style=path
```

### خيار مضيف مستودع SFTP (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

مضيف مستودع SFTP.

مضيف SFTP الذي يحتوي المستودع.

```text
example: repo1-sftp-host=sftprepo.domain
```

### خيار بصمة مضيف مستودع SFTP (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

بصمة مضيف مستودع SFTP.

ينبغي أن يتوافق توليد بصمة مضيف مستودع SFTP مع `repo-sftp-host-key-hash-type`. وولّد البصمة عبر `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. وعادةً ما توجد مفاتيح مضيف ssh في الدليل `/etc/ssh`.

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### خيار نوع فحص مفتاح مضيف SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

نوع فحص مفتاح مضيف SFTP.

أنواع فحص مفتاح مضيف SFTP التالية مدعومة:

- `strict` - لن يضيف pgBackRest أبدًا مفاتيح المضيف تلقائيًا إلى الملف ~/.ssh/known_hosts، ويرفض الاتصال بمضيفات تغيّر مفتاح مضيفها أو لا يوجد مفتاحها في ملفات المضيفات المعروفة. يجبر هذا الخيار المستخدم على إضافة جميع المضيفين الجدد يدويًا.
- `accept-new` - سيضيف pgBackRest تلقائيًا مفاتيح المضيف الجديدة إلى ملف المضيفات المعروفة للمستخدم، لكنه لن يسمح بالاتصال بمضيفات تغيّرت مفاتيح مضيفها.
- `fingerprint` - سيفحص pgBackRest مفتاح المضيف مقابل البصمة التي يحددها الخيار `repo-sftp-host-fingerprint`.
- `none` - لن يُنفَّذ أي فحص لمفتاح المضيف.

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### خيار نوع تجزئة مفتاح مضيف مستودع SFTP (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

نوع تجزئة مفتاح مضيف مستودع SFTP.

نوع تجزئة مفتاح مضيف مستودع SFTP. يُعلن نوع التجزئة الذي سيُستخدم لحساب ملخص مفتاح مضيف النظام البعيد عند بدء SSH. وتدعم الإصدارات الأحدث من `libssh2` خوارزمية `sha256` إضافةً إلى md5 وsha1.

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### خيار منفذ مضيف مستودع SFTP (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

منفذ مضيف مستودع SFTP.

منفذ مضيف مستودع SFTP.

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### خيار مستخدم مضيف مستودع SFTP (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

مستخدم مضيف مستودع SFTP.

المستخدم على المضيف المستخدم لتخزين المستودع.

```text
example: repo1-sftp-host-user=pg-backup
```

### خيار ملف المضيفات المعروفة لـ SFTP (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

ملف المضيفات المعروفة لـ SFTP.

ملف مضيفات معروفة يُبحث فيه عن مطابقة مضيف SFTP أثناء المصادقة. وعند عدم تحديده، سيلجأ pgBackRest افتراضيًا إلى البحث في `~/.ssh/known_hosts` و`~/.ssh/known_hosts2` و`/etc/ssh/ssh_known_hosts` و`/etc/ssh/ssh_known_hosts2`. وإذا هُيّئ بمسار ملف واحد أو أكثر، فسيبحث pgBackRest فيها عن مطابقة. ويجب أن تكون مسارات الملفات كاملة أو تبدأ بالتيلدا (~). ويمكن تمرير الخيار `repo-sftp-known-host` عدة مرات لتحديد أكثر من ملف مضيفات معروفة للبحث فيه. ولاستخدام فحص ملف المضيفات المعروفة يجب ألا يُحدَّد `repo-sftp-host-fingerprint`. راجع أيضًا خيار `repo-sftp-host-check-type`.

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### خيار ملف المفتاح الخاص لمستودع SFTP (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

ملف المفتاح الخاص لـ SFTP.

ملف المفتاح الخاص لـ SFTP المستخدم للمصادقة.

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### خيار عبارة مرور المفتاح الخاص لمستودع SFTP (`--repo-sftp-private-key-passphrase`) {#sftp-repository-private-key-passphrase-option---repo-sftp-private-key-passphrase}

عبارة مرور المفتاح الخاص لـ SFTP.

عبارة المرور المستخدمة للوصول إلى المفتاح الخاص. وهي ميزة اختيارية عند إنشاء زوج مفاتيح SSH عام/خاص.

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### خيار ملف المفتاح العام لمستودع SFTP (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

ملف المفتاح العام لـ SFTP.

ملف المفتاح العام لـ SFTP المستخدم للمصادقة. وهو اختياري إذا جرى البناء مقابل OpenSSL، ومطلوب إذا جرى البناء مقابل مكتبة مختلفة.

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### خيار ملف CA لتخزين المستودع (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

ملف CA لتخزين المستودع.

استخدم ملف CA غير الافتراضي للنظام لشهادات التخزين (مثل S3 وAzure).

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

الأسماء المهملة: repo-azure-ca-file, repo-s3-ca-file

### خيار مسار CA لـ TLS في تخزين المستودع (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

مسار CA لتخزين المستودع.

استخدم مسار CA غير الافتراضي للنظام لشهادات التخزين (مثل S3 وAzure).

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

الأسماء المهملة: repo-azure-ca-path, repo-s3-ca-path

### خيار مضيف التخزين للمستودع (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

مضيف تخزين المستودع.

اتصل بمضيف غير نقطة نهاية التخزين (مثل S3 أو Azure). ويُستخدم هذا عادةً للاختبار.

```text
example: repo1-storage-host=127.0.0.1
```

الأسماء المهملة: repo-azure-host, repo-s3-host

### خيار منفذ التخزين للمستودع (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

منفذ تخزين المستودع.

المنفذ المطلوب استخدامه عند الاتصال بنقطة نهاية التخزين (مثل S3 أو Azure) (أو بالمضيف إذا حُدد).

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

الأسماء المهملة: repo-azure-port, repo-s3-port

### خيار وسوم التخزين للمستودع (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

وسم/وسوم تخزين المستودع.

حدد وسومًا ستُضاف إلى الكائنات عندما يكون المستودع مخزن كائنات (مثل S3). ويمكن تكرار الخيار لإضافة وسوم متعددة.

لا يوفر pgBackRest طريقة لتعديل هذه الوسوم، فاحرص على ضبطها بشكل صحيح قبل تشغيل `stanza-create` لضمان اتساق الوسوم في أنحاء المستودع كافة.

```text
example: repo1-storage-tag=key1=value1
```

### خيار حجم جزء الرفع لتخزين المستودع (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

حجم جزء الرفع لتخزين المستودع.

تسمح مخازن الكائنات مثل S3 برفع الملفات على شكل أجزاء عندما يكون الملف أكبر من أن يُخزَّن في الذاكرة. وحتى لو أمكن تخزين الملف في الذاكرة، فإن تحديد مقدار الذاكرة المستخدم للرفع أكثر كفاءة من حيث الذاكرة.

سيؤدي حجم الجزء الأكبر عمومًا إلى أداء أفضل لأنه يقلل طلبات الرفع ويسمح برفع ملفات أكثر في طلب واحد بدلًا من رفعها على شكل أجزاء. والعيب هو أن استخدام الذاكرة سيكون أعلى، ولأنه يجب تخصيص مخزن الأجزاء لكل عملية على حدة، فإن قيم `process-max` الأكبر ستؤدي إلى استهلاك ذاكرة أكبر إجمالًا.

لاحظ أن أحجام الأجزاء الصالحة تختلف بحسب نوع التخزين وبحسب المنصة. فمثلًا، الحد الأدنى لحجم الجزء في AWS S3 هو 5MiB. ويختلف مصطلح حجم الجزء بحسب نوع التخزين، فعند البحث عن القيم الدنيا/القصوى استخدم "part size" لـ AWS S3، و"chunk size" لـ GCS، و"block size" لـ Azure.

إذا كان الملف أكبر من 1GiB (الحجم الأقصى الذي تنشئه PostgreSQL افتراضيًا) فسيرتفع حجم الجزء تزايديًا حتى الحد الأقصى المسموح به لإكمال رفع الملف.

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### خيار التحقق من شهادة التخزين للمستودع (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

التحقق من شهادة تخزين المستودع.

يوفر هذا الخيار القدرة على تمكين/تعطيل التحقق من شهادة TLS لخادم التخزين (مثل S3 أو Azure). ولا ينبغي استخدام التعطيل إلا للاختبار أو للسيناريوهات الأخرى التي تكون فيها الشهادة موقعة ذاتيًا.

```text
default: y
example: repo1-storage-verify-tls=n
```

الأسماء المهملة: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### خيار الروابط الرمزية في المستودع (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

إنشاء روابط رمزية داخل المستودع.

يمكّن إنشاء الرابط الرمزي `latest` والروابط الرمزية لمساحات الجداول. وهذه الروابط الرمزية أنفع ما تكون عند استخدام اللقطات لإجراء استعادة في موضعها داخل المستودع، وهي حالة استخدام غير شائعة.

وبينما لا تبدو هذه الميزة مفيدة للغالبية العظمى من المستخدمين، فإنها تبقى مُمكَّنة افتراضيًا لأغراض الإرث. ومع ذلك، قد يكون من المفيد تعطيل الروابط الرمزية لمخازن شبيهة بـ Posix لا تدعمها.

```text
default: y
example: repo1-symlink=n
```

### خيار الوقت الهدف للمستودع (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

الوقت الهدف للمستودع.

يحدد الوقت الهدف الوقتَ الذي تستخدمه الأوامر لقراءة مستودع على تخزين يدعم تعدد الإصدارات (versioned). ويتيح ذلك للأمر قراءة المستودع كما كان في نقطة زمنية لاسترداد بيانات حُذفت أو أُتلفت بخطأ من المستخدم أو ببرمجية خبيثة.

التخزين الذي يدعم تعدد الإصدارات مدعوم في S3 وGCS وAzure لكنه غير مُمكَّن افتراضيًا عمومًا. وإضافةً إلى تمكين الإصدارات، قد يكون من المفيد تمكين قفل الكائنات لـ S3 والحذف الناعم لـ GCS أو Azure.

عند تحديد الخيار `repo-target-time` يجب تقديم الخيار `repo` أيضًا. ومن غير المرجح أن تدعم جميع أنواع المستودعات الإصدارات، وعمومًا من المنطقي استهداف مستودع واحد للاسترداد.

لاحظ أن المقارنات بختم وقت التخزين هي <= للختم الزمني المقدم، وتُقتطع المللي ثانية من الختم الزمني عند تقديمه.

```text
example: repo-target-time=2024-08-08 12:12:12+00
```

### خيار نوع المستودع (`--repo-type`) {#repository-type-option---repo-type}

نوع التخزين المستخدم للمستودع.

أنواع المستودعات التالية مدعومة:

- `azure` - خدمة Azure Blob Storage
- `cifs` - مثل `posix`، لكنها تعطل الروابط وعمليات fsync للدلائل
- `gcs` - Google Cloud Storage
- `posix` - أنظمة ملفات متوافقة مع Posix
- `s3` - خدمة AWS Simple Storage Service
- `sftp` - بروتوكول نقل الملفات الآمن (Secure File Transfer Protocol)

عند استخدام تركيب NFS كمستودع `posix`، تنطبق على pgBackRest القواعد نفسها الموضحة في وثائق PostgreSQL: [إنشاء عنقود قاعدة بيانات - أنظمة الملفات](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```text
default: posix
example: repo1-type=cifs
```

--------

## خيارات الاستعادة {#restore-options}

يُعرِّف قسم `restore` الإعدادات المستخدمة لاستعادة النسخ الاحتياطية.

### خيار وضع الأرشفة (`--archive-mode`) {#archive-mode-option---archive-mode}

الحفاظ على الأرشفة أو تعطيلها في العنقود المستعاد.

يتيح هذا الخيار الحفاظ على الأرشفة أو تعطيلها في عنقود مستعاد. ويفيد ذلك عندما يجب ترقية العنقود لإنجاز عمل ما لكنه غير مخصص ليصبح الرئيسي الجديد. وفي هذه الحالة لا يُستحسن دفع WAL من العنقود إلى المستودع.

الأوضاع التالية مدعومة:

- `off` - تعطيل الأرشفة بضبط `archive_mode=off`.
- `preserve` - الحفاظ على إعداد `archive_mode` الحالي.

**ملاحظة**: هذا الخيار غير متاح في PostgreSQL < 12.

```text
default: preserve
example: archive-mode=off
```

### خيار استثناء قواعد البيانات (`--db-exclude`) {#exclude-database-option---db-exclude}

الاستعادة مع استثناء قواعد البيانات المحددة.

ستُستعاد قواعد البيانات المستثناة كملفات متناثرة (sparse) مملوءة بالأصفار لتوفير المساحة مع إبقاء إمكانية PostgreSQL لإجراء الاسترداد. وبعد الاسترداد، لن تكون تلك القواعد متاحة لكن يمكن إزالتها بالأمر `drop database`. ويمكن تمرير الخيار `--db-exclude` عدة مرات لتحديد أكثر من قاعدة بيانات لاستثنائها.

وعند استخدامه مع الخيار `--db-include`، سيطبق `--db-exclude` فقط على قواعد بيانات النظام القياسية (`template0` و`template1` و`postgres`).

```text
example: db-exclude=db_main
```

### خيار تضمين قواعد البيانات (`--db-include`) {#include-database-option---db-include}

استعادة قواعد البيانات المحددة فقط.

تتيح هذه الميزة استعادة قواعد بيانات مختارة فقط. أما قواعد البيانات غير المضمنة تحديدًا فستُستعاد كملفات متناثرة مملوءة بالأصفار لتوفير المساحة مع إبقاء إمكانية PostgreSQL لإجراء الاسترداد. وبعد الاسترداد، لن تكون قواعد البيانات غير المضمنة متاحة لكن يمكن إزالتها بالأمر `drop database`.

ملاحظة:

قواعد البيانات المدمجة (`template0` و`template1` و`postgres`) تُستعاد دائمًا ما لم تُستثنَ صراحةً.

ويمكن تمرير الخيار `--db-include` عدة مرات لتحديد أكثر من قاعدة بيانات لتضمينها.

راجع [استعادة قواعد بيانات محددة](/ar/pgbackrest/user-guide/#restore-selected-databases) لمعلومات إضافية وتحفظات.

```text
example: db-include=db_main
```

### خيار ربط الكل (`--link-all`) {#link-all-option---link-all}

استعادة جميع الروابط الرمزية.

افتراضيًا تُستعاد الدلائل والملفات المرتبطة رمزيًا كدلائل وملفات عادية في $PGDATA. والسبب أنه قد لا يكون آمنًا استعادة الروابط الرمزية إلى وجهاتها الأصلية على نظام غير النظام الذي أُجريت فيه النسخة الاحتياطية الأصلية. يستعيد هذا الخيار جميع الروابط الرمزية تمامًا كما كانت على النظام الأصلي الذي أُجريت فيه النسخة الاحتياطية.

```text
default: n
example: link-all=y
```

### خيار خريطة الروابط (`--link-map`) {#link-map-option---link-map}

تعديل وجهة رابط رمزي.

يسمح بتغيير الملف أو المسار الوجهة لرابط رمزي عند الاستعادة. ويفيد ذلك عند الاستعادة إلى أنظمة ذات تخطيط تخزين مختلف عن النظام الأصلي الذي أُنشئت فيه النسخة الاحتياطية.

```text
example: link-map=pg_xlog=/data/xlog
```

### خيار الاسترداد (`--recovery-option`) {#recovery-option---recovery-option}

ضبط خيار في `postgresql.auto.conf` أو `recovery.conf`.

راجع [إعداد الخادم](https://www.postgresql.org/docs/current/runtime-config.html) لتفاصيل خيارات `postgresql.auto.conf` أو `recovery.conf` (احرص على تحديد إصدار PostgreSQL لديك). ويمكن استخدام هذا الخيار عدة مرات.

بالنسبة إلى PostgreSQL >= 12، ستُكتب الخيارات في `postgresql.auto.conf`. ولكل الإصدارات الأخرى، ستُكتب الخيارات في `recovery.conf`.

ملاحظة:

سيُولَّد الخيار `restore_command` تلقائيًا لكن يمكن تجاوزه بهذا الخيار. واحترس من تحديد `restore_command` بنفسك، فـ pgBackRest مصمم ليتولى ذلك عنك. أما خيارات الاسترداد الهدف (recovery_target_name وrecovery_target_time وغيرها) فيولّدها pgBackRest تلقائيًا ولا ينبغي ضبطها بهذا الخيار.

وبما أن pgBackRest لا يشغّل PostgreSQL بعد كتابة ملف `postgresql.auto.conf` أو `recovery.conf`، فمن الممكن دائمًا تحرير/فحص `postgresql.auto.conf` أو `recovery.conf` قبل إعادة التشغيل يدويًا.

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### خيار خريطة مساحات الجداول (`--tablespace-map`) {#tablespace-map-option---tablespace-map}

استعادة مساحة جدول إلى الدليل المحدد.

ينقل مساحة جدول إلى موقع جديد أثناء الاستعادة. ويفيد ذلك عندما لا تكون مواقع مساحات الجداول هي نفسها على نسخة متماثلة، أو عندما يكون لنظام مرقّى نقاط تركيب مختلفة.

مواقع مساحات الجداول لا تُخزَّن في pg_tablespace، لذا يمكن نقل مساحات الجداول دون عواقب. غير أنه لا يُنصح بنقل مساحة جدول إلى `data_directory` وقد يسبب مشكلات. ولمزيد من المعلومات عن نقل مساحات الجداول، يُعد http://www.databasesoup.com/2013/11/moving-tablespaces.html موردًا جيدًا.

```text
example: tablespace-map=ts_01=/db/ts_01
```

### خيار إعادة تعيين جميع مساحات الجداول (`--tablespace-map-all`) {#map-all-tablespaces-option---tablespace-map-all}

استعادة جميع مساحات الجداول إلى الدليل المحدد.

تُستعاد مساحات الجداول إلى مواقعها الأصلية افتراضيًا. ويمكن تعديل هذا السلوك لكل مساحة جدول بالخيار `tablespace-map`، لكن يُفضَّل أحيانًا إعادة تعيين جميع مساحات الجداول إلى دليل جديد دفعة واحدة. ويفيد ذلك بوجه خاص في أنظمة التطوير أو الإعداد (staging) التي قد لا يكون لها تخطيط التخزين نفسه الموجود على النظام الأصلي الذي أُنشئت فيه النسخة الاحتياطية.

المسار المحدد سيكون المسار الأصل المستخدم لإنشاء جميع مساحات الجداول في النسخة الاحتياطية.

تنبيه:

مساحات الجداول التي أُنشئت بعد بدء النسخة الاحتياطية لن تُعاد تعيينها. فخذ نسخة احتياطية جديدة بعد إنشاء مساحة جدول إذا كان تعيين مساحات الجداول مطلوبًا.

```text
example: tablespace-map-all=/data/tablespace
```

--------

## خيارات الخادم {#server-options}

يُعرِّف قسم `server` الخيارات المستخدمة لتهيئة خادم TLS.

### خيار عنوان خادم TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

عنوان خادم TLS.

عنوان IP الذي سيستمع عليه الخادم لطلبات العملاء.

```text
default: localhost
example: tls-server-address=*
```

### خيار العملاء المخوّلين لخادم TLS (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

العملاء المخوّلون لخادم TLS.

يُخوَّل العملاء على الخادم بالتحقق من شهاداتهم ومطابقة الاسم الشائع (CN) لشهادتهم مع قائمة على الخادم مهيأة بالخيار `tls-server-auth`.

ويمكن تخويل اسم شائع لعميل لأي عدد من الـ stanza بإمداد قائمة مفصولة بفواصل إلى الخيار `tls-server-auth`، أو لجميع الـ stanza بتحديد `tls-server-auth=client-cn=*`. ولا يجوز استخدام أحرف البدل في الاسم الشائع للعميل.

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### خيار هيئات شهادات خادم TLS (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

هيئات شهادات خادم TLS.

يتحقق من أن شهادات العملاء موقعة من هيئة شهادات موثوقة.

```text
example: tls-server-ca-file=/path/to/server.ca
```

### خيار شهادة خادم TLS (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

ملف شهادة خادم TLS.

يُرسَل إلى العميل لإظهار هوية الخادم.

```text
example: tls-server-cert-file=/path/to/server.crt
```

### خيار مفتاح خادم TLS (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

ملف مفتاح خادم TLS.

يثبت أن شهادة الخادم أرسلها مالكها.

```text
example: tls-server-key-file=/path/to/server.key
```

### خيار منفذ خادم TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

منفذ خادم TLS.

المنفذ الذي سيستمع عليه الخادم لطلبات العملاء.

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## خيارات الـ Stanza {#stanza-options}

تُعرِّف الـ stanza تهيئةَ النسخ الاحتياطي لعنقود قاعدة بيانات PostgreSQL محدد. ويجب أن يحدد قسم الـ stanza مسار عنقود قاعدة البيانات والمضيف/المستخدم إذا كان عنقود قاعدة البيانات بعيدًا. كما يمكن تجاوز أي أقسام إعداد عامة لتحديد إعدادات خاصة بكل stanza.

**الفهرسة**: جميع الخيارات `pg-` مفهرسة للسماح بتهيئة مضيفي PostgreSQL متعددين. فمثلًا، يُهيَّأ رئيسي واحد بالخيارين `pg1-path` و`pg1-port` وغيرهما. وإذا هُيّئ مضيف استعداد ففهرِس الخيارات `pg-` على مضيف المستودع بالشكل `pg2-` (مثل pg2-host وpg2-path وغيرها).

### خيار قاعدة بيانات PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

قاعدة بيانات PostgreSQL.

اسم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. والقيمة الافتراضية هي الأفضل عادةً، لكن بعض التثبيتات قد لا تحتوي قاعدة البيانات هذه.

لاحظ أنه لأسباب تاريخية سيُتجاهل ضبط متغير البيئة `PGDATABASE`.

```text
default: postgres
example: pg1-database=backupdb
```

### خيار مضيف PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

مضيف PostgreSQL للتشغيل عن بُعد.

يُستخدم للنسخ الاحتياطي عندما يختلف مضيف PostgreSQL عن مضيف المستودع.

```text
example: pg1-host=db.domain.com
```

الاسم المهمل: db-host

### خيار ملف هيئة شهادات مضيف PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

ملف هيئة شهادات مضيف PostgreSQL.

استخدم ملف CA غير الافتراضي للنظام للاتصال بمضيف PostgreSQL.

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة شهادات مضيف PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

مسار هيئة شهادات مضيف PostgreSQL.

استخدم مسار CA غير الافتراضي للنظام للاتصال بمضيف PostgreSQL.

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### خيار ملف شهادة مضيف PostgreSQL (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

ملف شهادة مضيف PostgreSQL.

يُرسَل إلى مضيف PostgreSQL لإثبات هوية العميل.

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### خيار أمر مضيف PostgreSQL (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

أمر pgBackRest على مضيف PostgreSQL.

مطلوب فقط إذا كان المسار إلى أمر pgBackRest مختلفًا على المضيفين المحلي ومضيف PostgreSQL. وإذا لم يُعرَّف، فسيُضبط أمر مضيف PostgreSQL مثل الأمر المحلي نفسه.

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

الاسم المهمل: db-cmd

### خيار إعداد مضيف PostgreSQL (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

ملف إعداد pgBackRest لمضيف قاعدة البيانات.

يعيّن موقع ملف الإعداد على مضيف PostgreSQL. وهذا مطلوب فقط إذا كان ملف إعداد مضيف PostgreSQL في موقع مختلف عن ملف الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

الاسم المهمل: db-config

### خيار مسار تضمين إعداد مضيف PostgreSQL (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

مسار تضمين إعداد pgBackRest لمضيف قاعدة البيانات.

يعيّن موقع مسار تضمين الإعداد على مضيف PostgreSQL. وهذا مطلوب فقط إذا كان مسار تضمين إعداد مضيف PostgreSQL في موقع مختلف عن مسار تضمين الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار إعداد مضيف PostgreSQL (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

مسار إعداد pgBackRest لمضيف قاعدة البيانات.

يعيّن موقع مسار الإعداد على مضيف PostgreSQL. وهذا مطلوب فقط إذا كان مسار إعداد مضيف PostgreSQL في موقع مختلف عن مسار الإعداد المحلي.

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### خيار ملف مفتاح مضيف PostgreSQL (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

ملف مفتاح مضيف PostgreSQL.

يثبت أن شهادة العميل أرسلها مالكها.

```text
example: pg1-host-key-file=/path/to/client.key
```

### خيار منفذ مضيف PostgreSQL (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

منفذ مضيف PostgreSQL عندما يكون `pg-host` مضبوطًا.

استخدم هذا الخيار لتحديد منفذ غير افتراضي لبروتوكول مضيف PostgreSQL.

ملاحظة:

عند `pg-host-type=ssh` لا توجد قيمة افتراضية لـ `pg-host-port`. وفي هذه الحالة سيكون المنفذ هو ما هو مهيأ للأمر الذي يحدده `cmd-ssh`.

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

الاسم المهمل: db-ssh-port

### خيار نوع بروتوكول مضيف PostgreSQL (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

نوع بروتوكول مضيف PostgreSQL.

أنواع البروتوكول التالية مدعومة:

- `ssh` - Secure Shell.
- `tls` - خادم TLS لـ pgBackRest.

```text
default: ssh
example: pg1-host-type=tls
```

### خيار مستخدم مضيف PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

مستخدم تسجيل الدخول لمضيف PostgreSQL عندما يكون `pg-host` مضبوطًا.

سيملك هذا المستخدم أيضًا عملية pgBackRest البعيدة وسيبدأ الاتصالات بـ PostgreSQL. ولكي يعمل ذلك بشكل صحيح، ينبغي أن يكون المستخدم مالك عنقود قاعدة بيانات PostgreSQL، وهو عمومًا `postgres`، القيمة الافتراضية.

```text
default: postgres
example: pg1-host-user=db_owner
```

الاسم المهمل: db-user

### خيار مسار PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

دليل بيانات PostgreSQL.

ينبغي أن يكون هذا هو نفسه `data_directory` الذي يبلّغ عنه PostgreSQL. وحتى لو كان يمكن قراءة هذه القيمة من مواضع مختلفة، فمن الحصافة ضبطها تحسبًا لعدم توفر تلك الموارد أثناء سيناريو استعادة أو نسخ احتياطي دون اتصال.

يُختبر الخيار `pg-path` مقابل القيمة التي يبلّغ عنها PostgreSQL في كل نسخة احتياطية متصلة، لذا ينبغي أن يكون محدثًا دائمًا.

```text
example: pg1-path=/data/db
```

الاسم المهمل: db-path

### خيار منفذ PostgreSQL (`--pg-port`) {#postgresql-port-option---pg-port}

منفذ PostgreSQL.

المنفذ الذي تعمل عليه PostgreSQL. ولا يحتاج هذا عادةً إلى تحديد لأن معظم عناقيد PostgreSQL تعمل على المنفذ الافتراضي.

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

الاسم المهمل: db-port

### خيار مسار مقبس PostgreSQL (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

مسار مقبس Unix لـ PostgreSQL.

دليل مقبس unix الذي حُدد عند تشغيل PostgreSQL. سيبحث pgBackRest تلقائيًا في الموقع القياسي لنظام التشغيل لديك، لذا لا حاجة عادةً إلى تحديد هذا الإعداد ما لم يُعدَّل دليل المقبس صراحةً بالإعداد `unix_socket_directories` في `postgresql.conf`.

```text
example: pg1-socket-path=/var/run/postgresql
```

الاسم المهمل: db-socket-path

### خيار مستخدم قاعدة بيانات PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

مستخدم قاعدة بيانات PostgreSQL.

اسم مستخدم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. وإذا لم يُحدد، سيتصل pgBackRest بمستخدم نظام التشغيل المحلي أو بـ `PGUSER`.

```text
example: pg1-user=backupuser
```
