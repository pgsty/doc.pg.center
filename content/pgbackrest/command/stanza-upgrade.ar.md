---
title: "أمر ترقية الـ stanza (stanza-upgrade)"
linkTitle: "stanza-upgrade"
weight: 160
description: "مرجع لخيارات الأمر `stanza-upgrade` وسلوكه في pgBackRest."
icon: fa-solid fa-arrow-up-right-dots
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-stanza-upgrade"
---

مباشرة بعد ترقية PostgreSQL إلى إصدار رئيسي أحدث، يجب ضبط `pg-path` لجميع إعدادات pgBackRest على موقع قاعدة البيانات الجديد وتشغيل الأمر `stanza-upgrade`. إذا كان هناك أكثر من مستودع واحد مهيأ على المضيف، فستُرقَّى الـ stanza على كل منها. إذا كانت قاعدة البيانات غير متصلة فاستخدم الخيار `--no-online`.

## خيارات الأمر {#command-options}

### خيار العمل مع عنقود قيد التشغيل (`--online`) {#online-option---online}

تحديث عنقود متصل.

تحديد --no-online يمنع pgBackRest من الاتصال بـ PostgreSQL عند ترقية الـ stanza.

```yaml
default: y
example: --no-online
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

### خيار حجم المخزن المؤقت (`--buffer-size`) {#buffer-size-option---buffer-size}

حجم المخزن المؤقت لعمليات الإدخال/الإخراج.

حجم المخزن المؤقت المستخدم لعمليات النسخ والضغط والتشفير وغيرها. يعتمد عدد المخازن المؤقتة المستخدمة على الخيارات، وقد تستخدم كل عملية ذاكرة إضافية، مثلًا قد يستخدم ضغط `gz` ذاكرة إضافية قدرها 256KiB.

القيم المسموح بها هي `16KiB`، `32KiB`، `64KiB`، `128KiB`، `256KiB`، `512KiB`، `1MiB`، `2MiB`، `4MiB`، `8MiB`، و`16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### خيار أمر عميل SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

أمر عميل SSH.

استخدم أمر عميل SSH معينًا عندما يُراد بديل عنه أو عندما لا يكون الأمر `ssh` موجودًا في $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### خيار مستوى ضغط الشبكة (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

مستوى ضغط الشبكة.

يضبط مستوى ضغط الشبكة عندما يكون `compress-type=none` ولا يُشغَّل الأمر على المضيف نفسه الذي يوجد به المستودع. يُستخدم الضغط لتقليل حركة مرور الشبكة. عندما لا يساوي `compress-type` القيمة `none` يتم تجاهل الإعداد `compress-level-network` واستخدام `compress-level` بدلًا منه بحيث يُضغط الملف مرة واحدة فقط.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
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

### خيار مهلة قاعدة البيانات (`--db-timeout`) {#database-timeout-option---db-timeout}

مهلة استعلام قاعدة البيانات.

يضبط المهلة، بالثواني، للاستعلامات على قاعدة البيانات. يشمل ذلك وظيفتي بدء/إيقاف النسخ الاحتياطي اللتين قد تستغرق كل منهما وقتًا طويلًا. لهذا السبب يجب إبقاء المهلة مرتفعة ما لم تعرف أن هاتين الوظيفتين ستعودان بسرعة (أي إذا كنت قد ضبطت `start-fast=y` وتعرف أن عنقود قاعدة البيانات لن يولّد مقاطع WAL كثيرة أثناء النسخ الاحتياطي).

> **ملاحظة:** يجب أن يكون خيار `db-timeout` أصغر من خيار `protocol-timeout`.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### خيار مهلة الإدخال/الإخراج (`--io-timeout`) {#io-timeout-option---io-timeout}

مهلة الإدخال/الإخراج.

المهلة، بالثواني، المستخدمة للاتصالات وعمليات القراءة/الكتابة.

لاحظ أن عملية القراءة/الكتابة بأكملها لا تحتاج إلى الاكتمال ضمن هذه المهلة، لكن يجب إحراز *بعض* التقدم، حتى لو كان بايتًا واحدًا فقط.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
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

### خيار مهلة البروتوكول (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

مهلة البروتوكول.

يضبط المهلة، بالثواني، التي ستنتظرها العملية المحلية أو البعيدة لاستلام رسالة جديدة على طبقة البروتوكول. يمنع هذا العمليات من الانتظار إلى ما لا نهاية انتظارًا لرسالة.

> **ملاحظة:** يجب أن يكون خيار `protocol-timeout` أكبر من خيار `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### خيار Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

تمكين Keep-alive.

يفعّل رسائل Keep-alive على اتصالات المقابس.

```yaml
default: y
example: --no-sck-keep-alive
```

### خيار الـ stanza (`--stanza`) {#stanza-option---stanza}

يعرّف الـ stanza.

الـ stanza هي الإعداد الخاص بعنقود قاعدة بيانات PostgreSQL الذي يحدد مكانه، وكيف ستُؤخذ نسخة احتياطية له، وخيارات الأرشفة، وما إلى ذلك. لن يكون لدى معظم خوادم قواعد البيانات سوى عنقود قاعدة بيانات PostgreSQL واحد وبالتالي stanza واحدة، بينما سيكون لخوادم النسخ الاحتياطي stanza لكل عنقود قاعدة بيانات يحتاج إلى نسخ احتياطي.

قد يبدو من المغري تسمية الـ stanza باسم العنقود الأساسي، لكن الاسم الأفضل هو ما يصف قواعد البيانات الواردة في العنقود. ولأن اسم الـ stanza سيُستخدم للأساسي وجميع النسخ المتماثلة، فمن الأنسب اختيار اسم يصف الوظيفة الفعلية للعنقود، مثل app أو dw، بدلًا من اسم العنقود المحلي، مثل main أو prod.

```yaml
example: --stanza=main
```

### خيار عدد رسائل Keep-alive (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

عدد رسائل Keep-alive.

يحدد عدد رسائل TCP keep-alive التي يمكن فقدانها قبل اعتبار الاتصال ميتًا.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPCNT`.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### خيار وقت خمول Keep-alive (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

وقت خمول Keep-alive.

يحدد مقدار الوقت (بالثواني) دون أي نشاط شبكي، وبعد انقضائه ينبغي لنظام التشغيل إرسال رسالة TCP keep-alive.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPIDLE`.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### خيار فاصل Keep-alive (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

مدة فاصل Keep-alive.

يحدد مقدار الوقت (بالثواني)، وبعد انقضائه ينبغي إعادة إرسال رسالة TCP keep-alive التي لم يُقر باستلامها.

هذا الخيار متاح على الأنظمة التي تدعم خيار المقبس `TCP_KEEPINTVL`.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### خيار مجموعات تشفير TLSv1.2 (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

مجموعات تشفير TLSv1.2 المسموح بها.

جميع اتصالات TLS بين عميل pgBackRest وخادمه مشفرة. وبشكل افتراضي، تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

> **ملاحظة:** الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل مجموعات التشفير المقبولة عند الحاجة. المثال المذكور خيار معقول ما لم تكن لديك متطلبات أمنية محددة. إذا لم يُضبط (وهذا الافتراضي)، فتُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### خيار مجموعات تشفير TLSv1.3 (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

مجموعات تشفير TLSv1.3 المسموح بها.

جميع اتصالات TLS بين عميل pgBackRest وخادمه مشفرة. وبشكل افتراضي، تكون الاتصالات بمخازن الكائنات (مثل S3) مشفرة أيضًا.

> **ملاحظة:** الحد الأدنى المطلق لمستوى الأمان لأي اتصال نقل هو TLSv1.2.

يمكن تعديل مجموعات التشفير المقبولة عند الحاجة. إذا لم يُضبط (وهذا الافتراضي)، فتُطبَّق القيمة الافتراضية لمكتبة OpenSSL الأساسية.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
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

### خيار تسجيل العمليات الفرعية (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

تمكين التسجيل في العمليات الفرعية.

يفعّل تسجيل الملف لأي عمليات فرعية تنشئها هذه العملية باستخدام مستوى السجل الذي يحدده `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### خيار الطابع الزمني للسجل (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

تمكين الطابع الزمني في التسجيل.

يفعّل الطابع الزمني في التسجيل على وحدة التحكم وفي الملفات. يُعطَّل هذا الخيار في حالات خاصة مثل توليد الوثائق.

```yaml
default: y
example: --no-log-timestamp
```

## خيارات المشرفين {#maintainer-options}

### خيار فرض إصدار PostgreSQL (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

فرض إصدار PostgreSQL.

سيُستخدم إصدار PostgreSQL المحدد بدلًا من الإصدار المكتشف تلقائيًا بقراءة `pg_control` أو ترويسات WAL. هذا مفيد بشكل أساسي للتفرعات (forks) من PostgreSQL أو لإصداراتها التطويرية حيث تختلف هذه القيم عن الإصدار الرسمي. يجب أن يتطابق الإصدار الذي يبلغ عنه PostgreSQL عبر `server_version_num` مع الإصدار المفروض.

تحذير:

كن حذرًا عند استخدام هذا الخيار لأن `pg_control` وترويسات WAL ستُقرأ مع ذلك بالتنسيق المتوقع للإصدار المحدد، أي التنسيق الخاص بإصدار PostgreSQL المفتوح المصدر الرسمي. إذا غيّرت التفرعة أو الإصدار التطويري تنسيق الحقول التي يعتمد عليها pgBackRest فسيؤدي ذلك إلى سلوك غير متوقع. بشكل عام، لن يعمل هذا الخيار كما هو متوقع إلا إذا أضافت التفرعة جميع أعضاء البنيات (struct) المخصصة *بعد* أعضاء PostgreSQL القياسية.

```yaml
example: --pg-version-force=15
```

## خيارات المستودع {#repository-options}

### خيار حاوية مستودع Azure (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

حاوية مستودع Azure.

حاوية Azure المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها Azure في الحاوية أيضًا.

```yaml
example: --repo1-azure-container=pg-backup
```

### خيار نوع مفتاح مستودع Azure (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

نوع مفتاح مستودع Azure.

تُدعم أنواع التخويل التالية:

- `shared` - مفتاح مشترك
- `sas` - توقيع وصول مشترك
- `auto` - تخويل تلقائي باستخدام الهويات المُدارة في Azure

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### خيار نمط URI لمستودع Azure (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

نمط URI في Azure.

أنماط URI التالية مدعومة:

- `host` - الاتصال بمضيف `account.endpoint`.
- `path` - الاتصال بمضيف `endpoint` وإضافة الحساب إلى بداية URIs.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### خيار نوع التشفير للمستودع (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

التشفير المستخدم لتشفير المستودع.

أنواع التشفير التالية مدعومة:

- `none` - المستودع غير مشفر
- `aes-256-cbc` - معيار التشفير المتقدم (AES) بطول مفتاح 256 بت

لاحظ أن التشفير يُنفَّذ دائمًا على جانب العميل حتى لو كان نوع المستودع (مثل S3) يدعم التشفير.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### خيار حاوية مستودع GCS (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

حاوية مستودع GCS.

حاوية GCS المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها GCS في الحاوية أيضًا.

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

- `auto` - التخويل باستخدام حساب الخدمة للنسخة (instance).
- `service` - حساب خدمة من مفتاح مخزن محليًا.
- `token` - للاختبار المحلي، مثل `fakegcs`.
- `web-id` - التخويل باستخدام Workload Identity Federation (اتحاد هوية أحمال العمل).

عندما يكون `repo-gcs-key-type=service` ستُعاد قراءة بيانات الاعتماد عند تجديد رمز المصادقة المميز.

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

### خيار مضيف المستودع (`--repo-host`) {#repository-host-option---repo-host}

مضيف المستودع عند التشغيل عن بُعد.

عند إجراء النسخ الاحتياطي والأرشفة إلى نظام ملفات محمَّل محليًا لا يكون هذا الإعداد مطلوبًا.

```yaml
example: --repo1-host=repo1.domain.com
```

اسم مهمل: backup-host

### خيار ملف هيئة الشهادات لمضيف المستودع (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

ملف هيئة الشهادات لمضيف المستودع.

استخدم ملف هيئة شهادات (CA) غير الافتراضي للنظام للاتصال بمضيف المستودع.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة الشهادات لمضيف المستودع (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

مسار هيئة الشهادات لمضيف المستودع.

استخدم مسار هيئة شهادات (CA) غير الافتراضي للنظام للاتصال بمضيف المستودع.

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

مطلوب فقط إذا كان مسار أمر pgBackRest مختلفًا على المضيف المحلي ومضيف المستودع. إذا لم يُعرَّف، فسيُضبط أمر مضيف المستودع مماثلًا للأمر المحلي.

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

يثبت أن شهادة العميل أرسلها مالكها.

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

أنواع البروتوكول التالية مدعومة:

- `ssh` - الصدفة الآمنة (Secure Shell).
- `tls` - خادم TLS الخاص بـ pgBackRest.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### خيار مستخدم مضيف المستودع (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

مستخدم مضيف المستودع عندما يكون `repo-host` مضبوطًا.

يعرّف المستخدم الذي سيُستخدم للعمليات على مضيف المستودع. يُفضَّل ألا يكون هذا المستخدم `postgres` بل مستخدم آخر مثل `pgbackrest`. إذا كان PostgreSQL يعمل على مضيف المستودع فيمكن وضع المستخدم `postgres` في مجموعة `pgbackrest` بحيث تكون له صلاحية القراءة على المستودع دون أن يتمكن من إتلاف محتوياته عن طريق الخطأ.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

اسم مهمل: backup-user

### خيار مسار المستودع (`--repo-path`) {#repository-path-option---repo-path}

المسار حيث تُخزن النسخ الاحتياطية والأرشيف.

المستودع هو المكان الذي يخزن فيه pgBackRest النسخ الاحتياطية ويؤرشف فيه مقاطع WAL.

قد يصعب تقدير مقدار المساحة التي ستحتاجها مسبقًا. أفضل ما يمكن فعله هو إجراء بعض النسخ الاحتياطية ثم تسجيل حجم الأنواع المختلفة من النسخ الاحتياطية (full/incr/diff) وقياس كمية WAL المولدة يوميًا. سيمنحك هذا فكرة عامة عن مقدار المساحة التي ستحتاجها، مع العلم بالطبع أن المتطلبات ستتغير على الأرجح مع مرور الوقت مع تطور قاعدة بياناتك.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### خيار حاوية مستودع S3 (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

حاوية مستودع S3.

حاوية S3 المستخدمة لتخزين المستودع.

يمكن تخزين مستودعات pgBackRest في جذر الحاوية بضبط `repo-path=/`، لكن من الأفضل عادةً تحديد بادئة، مثل `/repo`، بحيث يمكن تخزين السجلات والمحتويات الأخرى التي تنشئها AWS في الحاوية أيضًا.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### خيار نقطة نهاية مستودع S3 (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

نقطة نهاية مستودع S3.

يجب أن تكون نقطة نهاية AWS صالحة للمنطقة المحددة.

بالنسبة للإعدادات المخصصة/الاختبارية قد تكون الخيارات `repo-storage-ca-file`، و`repo-storage-ca-path`، و`repo-storage-host`، و`repo-storage-port`، و`repo-storage-verify-tls` مفيدة.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### خيار نوع مفتاح مستودع S3 (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

نوع مفتاح مستودع S3.

تُدعم أنواع التخويل التالية:

- `shared` - مفاتيح مشتركة
- `auto` - استرجاع بيانات اعتماد مؤقتة تلقائيًا
- `web-id` - استرجاع بيانات اعتماد هوية الويب تلقائيًا
- `pod-id` - استرجاع بيانات اعتماد هوية جراب EKS (pod) تلقائيًا
- `process` - استرجاع بيانات الاعتماد بتنفيذ عملية

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### خيار معرِّف مفتاح KMS لمستودع S3 (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

مفتاح KMS لمستودع S3.

يفعّل تشفير S3 من جانب الخادم باستخدام مفتاح خدمة إدارة المفاتيح في AWS المحدد.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### خيار أمر عملية مصادقة S3 (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

أمر عملية مصادقة S3.

الأمر (والوسائط الاختيارية) الذي سيُنفَّذ لاسترجاع بيانات اعتماد S3 المؤقتة. أول عنصر في القائمة هو الأمر وتُمرَّر العناصر المتبقية كمعاملات.

يجب أن تُخرِج العملية JSON يحتوي على الحقول `AccessKeyId` و`SecretAccessKey` و`SessionToken` و`Expiration`. ستُحدَّث بيانات الاعتماد تلقائيًا قبل وقت انتهاء الصلاحية. انظر [مزوّد بيانات الاعتماد عبر عملية (Process Credential Provider)](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) لتفاصيل التنسيق.

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

الدفع من قبل الطالب لمستودع S3.

يفعّل الدفع من قبل الطالب (requester pays) في S3.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### خيار دور مستودع S3 (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

دور مستودع S3.

اسم دور AWS (وليس ARN الكامل) المستخدم لاسترجاع بيانات اعتماد مؤقتة عندما يكون `repo-s3-key-type=auto`.

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

نقطة نهاية STS المستخدمة لاسترجاع بيانات اعتماد مؤقتة عندما يكون `repo-s3-key-type=web-id` مضبوطًا. اضبطها على نقطة نهاية إقليمية (مثل `sts.us-east-1.amazonaws.com`) لاستخدام STS الإقليمي، وقد يكون ذلك مطلوبًا من أجل GovCloud أو مناطق الصين أو لتقليل زمن الاستجابة.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### خيار نمط URI لمستودع S3 (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

نمط URI في S3.

أنماط URI التالية مدعومة:

- `host` - الاتصال بمضيف `bucket.endpoint`.
- `path` - الاتصال بمضيف `endpoint` وإضافة الحاوية إلى بداية URIs.

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

ينبغي أن يطابق توليد بصمة مضيف مستودع SFTP الخيار `repo-sftp-host-key-hash-type`. ولِّد البصمة عبر `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. توجد مفاتيح مضيف ssh عادةً في الدليل `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### خيار نوع التحقق من مفتاح مضيف SFTP (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

نوع التحقق من مفتاح مضيف SFTP.

أنواع التحقق من مفتاح مضيف SFTP التالية مدعومة:

- `strict` - لن يضيف pgBackRest مفاتيح المضيف تلقائيًا أبدًا إلى الملف ~/.ssh/known_hosts، وسيرفض الاتصال بالمضيفين الذين تغير مفتاح مضيفهم أو غير موجود في ملفات المضيفين المعروفين. يجبر هذا الخيار المستخدم على إضافة جميع المضيفين الجدد يدويًا.
- `accept-new` - سيضيف pgBackRest تلقائيًا مفاتيح المضيف الجديدة إلى ملف المضيفين المعروفين للمستخدم، لكنه لن يسمح بالاتصال بالمضيفين الذين تغيرت مفاتيح مضيفهم.
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

ملف مضيفين معروفين يُبحث فيه عن مطابقة مضيف SFTP أثناء المصادقة. عندما لا يُحدد، سيلجأ pgBackRest افتراضيًا إلى البحث في `~/.ssh/known_hosts`، و`~/.ssh/known_hosts2`، و`/etc/ssh/ssh_known_hosts`، و`/etc/ssh/ssh_known_hosts2`. وإذا هُيِّئ بمسار ملف واحد أو أكثر فسيبحث pgBackRest في تلك المسارات عن مطابقة. يجب أن تكون مسارات الملفات كاملة أو تبدأ بعلامة التيلدا (~). يمكن تمرير الخيار `repo-sftp-known-host` مرات متعددة لتحديد أكثر من ملف مضيفين معروفين للبحث فيها. وللاستفادة من التحقق عبر ملف المضيفين المعروفين يجب ألا يكون `repo-sftp-host-fingerprint` محددًا. انظر أيضًا خيار `repo-sftp-host-check-type`.

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

ملف المفتاح العام لـ SFTP المستخدم للمصادقة. اختياري إذا جرى البناء مقابل OpenSSL، ومطلوب إذا جرى البناء مقابل مكتبة مختلفة.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### خيار ملف CA لتخزين المستودع (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

ملف CA لتخزين المستودع.

استخدم ملف هيئة شهادات (CA) غير الافتراضي للنظام لشهادات التخزين (مثل S3 وAzure).

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

أسماء مهملة: repo-azure-ca-file, repo-s3-ca-file

### خيار مسار CA لـ TLS في تخزين المستودع (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

مسار CA لتخزين المستودع.

استخدم مسار هيئة شهادات (CA) غير الافتراضي للنظام لشهادات التخزين (مثل S3 وAzure).

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

أسماء مهملة: repo-azure-ca-path, repo-s3-ca-path

### خيار مضيف تخزين المستودع (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

مضيف تخزين المستودع.

اتصل بمضيف غير نقطة نهاية التخزين (مثل S3 أو Azure). يُستخدم هذا عادةً للاختبار.

```yaml
example: --repo1-storage-host=127.0.0.1
```

أسماء مهملة: repo-azure-host, repo-s3-host

### خيار منفذ تخزين المستودع (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

منفذ تخزين المستودع.

المنفذ الذي سيُستخدم عند الاتصال بنقطة نهاية التخزين (مثل S3 أو Azure) (أو بالمضيف إذا حُدد).

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

لا توجد في pgBackRest وسيلة لتعديل هذه الوسوم، لذا احرص على ضبطها بشكل صحيح قبل تشغيل `stanza-create` لضمان وسوم موحدة عبر المستودع بأكمله.

```yaml
example: --repo1-storage-tag=key1=value1
```

### خيار حجم أجزاء الرفع لتخزين المستودع (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

حجم أجزاء الرفع لتخزين المستودع.

تسمح مخازن الكائنات مثل S3 برفع الملفات على أجزاء عندما يكون الملف أكبر من أن يُخزن في الذاكرة. وحتى لو أمكن تخزين الملف في الذاكرة، فإن تقييد مقدار الذاكرة المستخدم للرفع أكفأ من حيث استهلاك الذاكرة.

سيؤدي حجم الجزء الأكبر عمومًا إلى أداء أفضل لأنه يقلل طلبات الرفع ويسمح برفع ملفات أكثر في طلب واحد بدلًا من رفعها على أجزاء. والعيب هو أن استهلاك الذاكرة سيكون أعلى، ولأنه يجب تخصيص مخزن الجزء المؤقت لكل عملية، فإن قيم `process-max` الأكبر ستؤدي إلى استهلاك ذاكرة أكبر إجمالًا.

لاحظ أن أحجام الأجزاء الصالحة تختلف حسب نوع التخزين والمنصة. مثلًا، لدى AWS S3 حد أدنى لحجم الجزء قدره 5MiB. وتختلف مصطلحات حجم الجزء حسب نوع التخزين، لذا عند البحث عن القيم الدنيا/القصوى استخدم "part size" لـ AWS S3، و"chunk size" لـ GCS، و"block size" لـ Azure.

إذا كان الملف أكبر من 1GiB (الحجم الأقصى الذي سينشئه PostgreSQL افتراضيًا) فسيُزاد حجم الجزء تدريجيًا حتى الحد الأقصى المسموح به لإكمال رفع الملف.

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

يوفر هذا الخيار القدرة على تمكين/تعطيل التحقق من شهادة TLS لخادم التخزين (مثل S3 أو Azure). لا يجوز استخدام التعطيل إلا للاختبار أو للسيناريوهات الأخرى التي تكون فيها الشهادة موقعة ذاتيًا.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

أسماء مهملة: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### خيار نوع المستودع (`--repo-type`) {#repository-type-option---repo-type}

نوع التخزين المستخدم للمستودع.

أنواع المستودعات التالية مدعومة:

- `azure` - خدمة تخزين Azure Blob
- `cifs` - مثل `posix`، لكنه يعطّل الروابط ومزامنة fsync للأدلة
- `gcs` - تخزين Google Cloud
- `posix` - أنظمة الملفات المتوافقة مع Posix
- `s3` - خدمة التخزين البسيطة من AWS
- `sftp` - بروتوكول نقل الملفات الآمن (Secure File Transfer Protocol)

عند استخدام تحميل NFS كمستودع `posix`، تنطبق على pgBackRest القواعد نفسها الموصوفة في وثائق PostgreSQL: [إنشاء عنقود قاعدة بيانات - أنظمة الملفات](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```yaml
default: posix
example: --repo1-type=cifs
```

## خيارات الـ stanza {#stanza-options}

### خيار قاعدة بيانات PostgreSQL (`--pg-database`) {#postgresql-database-option---pg-database}

قاعدة بيانات PostgreSQL.

اسم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. الافتراضي هو الأفضل عادةً لكن بعض التثبيتات قد لا تحتوي على قاعدة البيانات هذه.

لاحظ أنه لأسباب تاريخية سيتم تجاهل قيمة متغير البيئة `PGDATABASE`.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### خيار مضيف PostgreSQL (`--pg-host`) {#postgresql-host-option---pg-host}

مضيف PostgreSQL للتشغيل عن بُعد.

يُستخدم للنسخ الاحتياطي عندما يكون مضيف PostgreSQL مختلفًا عن مضيف المستودع.

```yaml
example: --pg1-host=db.domain.com
```

اسم مهمل: db-host

### خيار ملف هيئة الشهادات لمضيف PostgreSQL (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

ملف هيئة الشهادات لمضيف PostgreSQL.

استخدم ملف هيئة شهادات (CA) غير الافتراضي للنظام للاتصال بمضيف PostgreSQL.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### خيار مسار هيئة الشهادات لمضيف PostgreSQL (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

مسار هيئة الشهادات لمضيف PostgreSQL.

استخدم مسار هيئة شهادات (CA) غير الافتراضي للنظام للاتصال بمضيف PostgreSQL.

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

مطلوب فقط إذا كان مسار أمر pgBackRest مختلفًا على المضيف المحلي ومضيفي PostgreSQL. إذا لم يُعرَّف، فسيُضبط أمر مضيف PostgreSQL مماثلًا للأمر المحلي.

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

يثبت أن شهادة العميل أرسلها مالكها.

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

أنواع البروتوكول التالية مدعومة:

- `ssh` - الصدفة الآمنة (Secure Shell).
- `tls` - خادم TLS الخاص بـ pgBackRest.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### خيار مستخدم مضيف PostgreSQL (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

مستخدم تسجيل الدخول لمضيف PostgreSQL عندما يكون `pg-host` مضبوطًا.

سيكون هذا المستخدم أيضًا مالك عملية pgBackRest البعيدة وسيبدأ الاتصالات بـ PostgreSQL. ولكي يعمل هذا بشكل صحيح ينبغي أن يكون المستخدم مالك عنقود قاعدة بيانات PostgreSQL وهو عمومًا `postgres`، القيمة الافتراضية.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

اسم مهمل: db-user

### خيار مسار PostgreSQL (`--pg-path`) {#postgresql-path-option---pg-path}

دليل بيانات PostgreSQL.

ينبغي أن يكون هذا مماثلًا للقيمة `data_directory` التي يبلغ عنها PostgreSQL. ومع أنه يمكن قراءة هذه القيمة من أماكن متعددة، فمن الحكمة ضبطها تحسبًا لاحتمال عدم توفر تلك الموارد أثناء سيناريو استعادة أو نسخ احتياطي دون اتصال.

يُختبر خيار `pg-path` مقابل القيمة التي يبلغ عنها PostgreSQL عند كل نسخة احتياطية متصلة، لذا ينبغي أن يكون محدثًا دائمًا.

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

مسار مقبس Unix الخاص بـ PostgreSQL.

دليل مقبس unix الذي حُدد عند بدء تشغيل PostgreSQL. سيبحث pgBackRest تلقائيًا في الموقع القياسي لنظام التشغيل لديك، لذا لا حاجة عادةً إلى تحديد هذا الإعداد ما لم يُعدَّل دليل المقبس صراحةً بالإعداد `unix_socket_directories` في `postgresql.conf`.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

اسم مهمل: db-socket-path

### خيار مستخدم قاعدة بيانات PostgreSQL (`--pg-user`) {#postgresql-database-user-option---pg-user}

مستخدم قاعدة بيانات PostgreSQL.

اسم مستخدم قاعدة البيانات المستخدم عند الاتصال بـ PostgreSQL. إذا لم يُحدد فسيتصل pgBackRest بمستخدم نظام التشغيل المحلي أو بـ `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
