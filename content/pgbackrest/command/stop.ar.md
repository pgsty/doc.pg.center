---
title: "أمر الإيقاف (stop)"
linkTitle: "stop"
weight: 180
description: "مرجع لخيارات الأمر `stop` وسلوكه في pgBackRest."
icon: fa-solid fa-stop
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-stop"
---

لا يسمح بتشغيل أي عمليات pgBackRest جديدة. بشكل افتراضي سيُسمح للعمليات الجارية بالاكتمال بنجاح. استخدم الخيار `--force` لإنهاء العمليات الجارية.

ستعيد عمليات pgBackRest خطأً إذا شُغِّلت بعد اكتمال الأمر stop. انظر [البدء والإيقاف](/ar/pgbackrest/user-guide/#starting-and-stopping) لمزيد من المعلومات والأمثلة.

## خيارات الأمر {#command-options}

### خيار الإجبار (`--force`) {#force-option---force}

إجبار جميع عمليات pgBackRest على التوقف.

سيرسل هذا الخيار إشارات TERM إلى جميع عمليات pgBackRest الجارية لإحداث إيقاف منظم وفوري في آن واحد. لاحظ أن هذا سيوقف أيضًا العمليات التي بدأت على نظام آخر لكن لديها عمليات بعيدة تعمل على النظام الحالي. مثلًا، إذا بدأت نسخة احتياطية على خادم النسخ الاحتياطي فإن تشغيل `stop --force` على خادم قاعدة البيانات سيوقف عملية النسخ الاحتياطي على خادم النسخ الاحتياطي.

```yaml
default: n
example: --force
```

## الخيارات العامة {#general-options}

### خيار السماح بالتشغيل كمستخدم جذر (`--allow-root`) {#allow-run-as-root-option---allow-root}

السماح بتشغيل الأمر كمستخدم الجذر (root).

بشكل افتراضي لا يُسمح بتشغيل سوى الأمر `restore` كمستخدم الجذر لأنه مصمم لإدارة ملكية الملفات بعناية. إن تشغيل الأوامر الأخرى كمستخدم جذر يخاطر بإنشاء ملفات (مثلًا في المستودع) مملوكة لمستخدم الجذر وبالتالي غير متاحة لمستخدم PostgreSQL، مما يتسبب في فشل الأوامر اللاحقة.

فعِّل هذا الخيار لتشغيل أمر ما كمستخدم جذر رغم ذلك. ومع ذلك، فمن الأفضل بكثير تشغيل pgBackRest بالمستخدم الذي يملك المستودع وعنقود PostgreSQL.

```yaml
default: n
example: --allow-root
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

ستُدمج ملفات الإعداد الموجودة في الموقع المحدد بالامتداد `.conf` مع ملف إعداد pgBackRest، مما ينتج عنه ملف إعداد واحد.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### خيار مسار الإعداد (`--config-path`) {#config-path-option---config-path}

المسار الأساسي لملفات إعداد pgBackRest.

يُستخدم هذا الإعداد لتجاوز إعداد المسار الأساسي الافتراضي للخيارين `--config` و`--config-include-path` ما لم يُضبطا صراحةً على سطر الأوامر.

مثلًا، تمرير `--config-path=/conf/pgbackrest` وحده يجعل الافتراضي للخيار `--config` مضبوطًا على `/conf/pgbackrest/pgbackrest.conf` والافتراضي للخيار `--config-include-path` مضبوطًا على `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### خيار مسار القفل (`--lock-path`) {#lock-path-option---lock-path}

المسار حيث تُخزن ملفات القفل.

يوفر مسار القفل موقعًا ينشئ فيه pgBackRest ملفات قفل لمنع تشغيل عمليات متعارضة في وقت واحد.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### خيار umask المحايد (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

استخدام umask محايد.

يضبط umask على 0000 بحيث تُنشأ الأوضاع في المستودع بطريقة معقولة. وضع الدليل الافتراضي هو 0750 ووضع الملف الافتراضي هو 0640.

لاستخدام umask الخاص بالمستخدم المنفذ بدلًا منه، حدد `neutral-umask=n` في ملف الإعداد أو `--no-neutral-umask` على سطر الأوامر.

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

### خيار الـ stanza (`--stanza`) {#stanza-option---stanza}

يعرّف الـ stanza.

الـ stanza هي الإعداد الخاص بعنقود قاعدة بيانات PostgreSQL الذي يحدد مكانه، وكيف ستُؤخذ نسخة احتياطية له، وخيارات الأرشفة، وما إلى ذلك. لن يكون لدى معظم خوادم قواعد البيانات سوى عنقود قاعدة بيانات PostgreSQL واحد وبالتالي stanza واحدة، بينما سيكون لخوادم النسخ الاحتياطي stanza لكل عنقود قاعدة بيانات يحتاج إلى نسخ احتياطي.

قد يبدو من المغري تسمية الـ stanza باسم العنقود الأساسي، لكن الاسم الأفضل هو ما يصف قواعد البيانات الواردة في العنقود. ولأن اسم الـ stanza سيُستخدم للأساسي وجميع النسخ المتماثلة، فمن الأنسب اختيار اسم يصف الوظيفة الفعلية للعنقود، مثل app أو dw، بدلًا من اسم العنقود المحلي، مثل main أو prod.

```yaml
example: --stanza=main
```

## خيارات السجل {#log-options}

### خيار مستوى سجل وحدة التحكم (`--log-level-console`) {#console-log-level-option---log-level-console}

مستوى التسجيل في وحدة التحكم.

مستويات السجل المدعومة هي التالية:

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

مستوى التسجيل في الملف.

مستويات السجل المدعومة هي التالية:

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

مستوى التسجيل في stderr.

يحدد مستويات السجل التي ستُخرَج إلى `stderr` بدلًا من `stdout` (الذي يحدده `log-level-console`). لن يُخرَج الطابع الزمني ولا العملية إلى `stderr`.

مستويات السجل المدعومة هي التالية:

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

المسار حيث تُخزن ملفات السجل.

يوفر مسار السجل موقعًا يخزن فيه pgBackRest ملفات السجل. لاحظ أنه إذا كان `log-level-file=off` فلا حاجة إلى مسار السجل.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### خيار الطابع الزمني للسجل (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

تمكين الطابع الزمني في التسجيل.

يفعّل الطابع الزمني في التسجيل على وحدة التحكم وفي الملفات. يُعطَّل هذا الخيار في حالات خاصة مثل توليد الوثائق.

```yaml
default: y
example: --no-log-timestamp
```
