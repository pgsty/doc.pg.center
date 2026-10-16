---
title: "أمر ping الخادم (server-ping)"
linkTitle: "server-ping"
weight: 130
description: "مرجع لخيارات الأمر `server-ping` وسلوكه في pgBackRest."
icon: fa-solid fa-heart-pulse
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-server-ping"
---

أرسل ping إلى خادم pgBackRest TLS للتأكد من أنه يقبل الاتصالات. لا يُستخدم هذا إلا كفحص للتحقق من حيوية الخادم إذ لا تتم محاولة أي مصادقة.

إذا لم يُحدَّد أي مضيف على سطر الأوامر فسيتم استخدام الخيار `tls-server-host`.

## خيارات الأمر {#command-options}

### خيار عنوان خادم TLS (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

عنوان خادم TLS.

عنوان IP الذي سيستمع عليه الخادم لطلبات العملاء.

```yaml
default: localhost
example: --tls-server-address=*
```

### خيار منفذ خادم TLS (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

منفذ خادم TLS.

المنفذ الذي سيستمع عليه الخادم لطلبات العملاء.

```yaml
default: 8432
allowed: [1, 65535]
example: --tls-server-port=8000
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

### خيار مهلة الإدخال/الإخراج (`--io-timeout`) {#io-timeout-option---io-timeout}

مهلة الإدخال/الإخراج.

المهلة، بالثواني، المستخدمة للاتصالات وعمليات القراءة/الكتابة.

لاحظ أن عملية القراءة/الكتابة بأكملها لا تحتاج إلى الاكتمال ضمن هذه المهلة، ولكن يجب تحقيق *بعض* التقدم، حتى لو كان بايتًا واحدًا فقط.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### خيار ضبط أولوية العملية (`--priority`) {#set-process-priority-option---priority}

ضبط أولوية العملية.

يحدد مقدار الأولوية (أي قيمة niceness) التي سيمنحها مجدول النواة للعملية. القيم الموجبة تخفض الأولوية والقيم السالبة ترفعها. في معظم الحالات لا تمتلك العمليات صلاحية رفع أولويتها.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### خيار Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

تمكين Keep-alive.

يُمكِّن رسائل keep-alive على اتصالات المقابس (sockets).

```yaml
default: y
example: --no-sck-keep-alive
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

### خيار الطابع الزمني للسجل (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

تمكين الطابع الزمني في التسجيل.

يُمكِّن الطابع الزمني في تسجيل وحدة التحكم والملفات. يُعطَّل هذا الخيار في مواقف خاصة مثل توليد التوثيق.

```yaml
default: y
example: --no-log-timestamp
```
