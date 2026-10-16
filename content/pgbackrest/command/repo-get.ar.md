---
title: "أمر الجلب من المستودع (repo-get)"
linkTitle: "repo-get"
weight: 90
description: "مرجع لخيارات الأمر `repo-get` وسلوكه في pgBackRest."
icon: fa-solid fa-file-arrow-down
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/command.html#command-repo-get"
---

مشابه لأمر `cat` في يونكس لكنه يعمل مع أي نوع مستودع مدعوم. يتطلب هذا الأمر اسم ملف مؤهلًا بالكامل، وهو مخصص أساسًا للإدارة والتحقيق والاختبار. وهو ليس جزءًا مطلوبًا من إعداد pgBackRest العادي.

إذا كان المستودع مشفرًا فسيقوم `repo-get` بفك تشفير الملف تلقائيًا. لا يُفك ضغط الملفات تلقائيًا ولكن يمكن تمرير الإخراج عبر أمر فك الضغط المناسب، مثل `gzip -d`.

إذا كان مهيأً أكثر من مستودع واحد، فسيعتمد الأمر افتراضيًا المستودع ذا الأولوية الأعلى (مثل `repo1`) ما لم يُحدَّد الخيار `--repo`.

## خيارات الأمر {#command-options}

### خيار تجاهل الملفات المفقودة (`--ignore-missing`) {#ignore-missing-option---ignore-missing}

تجاهل ملف المصدر المفقود.

اخرج بالقيمة 1 إذا كان ملف المصدر مفقودًا دون رفع خطأ.

```yaml
default: n
example: --ignore-missing
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

### خيار أمر عميل SSH (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

أمر عميل SSH.

استخدم أمر عميل SSH محددًا عند الرغبة في استخدام بديل أو عندما لا يكون الأمر `ssh` موجودًا في $PATH.

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

لاحظ أن عملية القراءة/الكتابة بأكملها لا تحتاج إلى الاكتمال ضمن هذه المهلة، ولكن يجب إحراز *بعض* التقدم، حتى لو كان بايتًا واحدًا فقط.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
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

### خيار مهلة البروتوكول (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

مهلة البروتوكول.

يضبط المهلة، بالثواني، التي ستنتظرها العملية المحلية أو البعيدة لاستلام رسالة جديدة على طبقة البروتوكول. يمنع هذا العمليات من الانتظار إلى ما لا نهاية وصولًا لرسالة.

> **ملاحظة:** يجب أن يكون خيار `protocol-timeout` أكبر من خيار `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### خيار البيانات الخام (`--raw`) {#raw-data-option---raw}

عدم تحويل البيانات.

عدم تحويل (أي التشفير أو فك الضغط أو غير ذلك) بيانات الأمر الحالي.

```yaml
default: n
example: --raw
```

### خيار Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

تمكين Keep-alive.

يُمكِّن رسائل keep-alive على اتصالات المقابس.

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

يحدد مقدار الوقت (بثوانٍ) الذي يجب بعده إعادة إرسال رسالة TCP keep-alive التي لم يتم الإقرار باستلامها.

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

تُدعم الأنواع التالية للتخويل:

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

تُدعم الأنواع التالية للتخويل:

- `auto` - التخويل باستخدام حساب خدمة المثيل.
- `service` - حساب خدمة من مفتاح مخزن محليًا.
- `token` - للاختبار المحلي، مثل `fakegcs`.

عندما يكون `repo-gcs-key-type=service` يُعاد تحميل بيانات الاعتماد عند تجديد رمز المصادقة المميز.

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

تُدعم الأنواع التالية:

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

نوع تجزئة مفتاح مضيف مستودع SFTP. يعلن نوع التجزئة الذي سيُستخدم لحساب ملخص مفتاح المضيف للنظام البعيد عند بدء تشغيل SSH. تدعم الإصدارات الأحدث من `libssh2` خيار `sha256` بالإضافة إلى md5 وsha1.

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

### خيار الوقت المستهدف للمستودع (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

الوقت المستهدف للمستودع.

يحدد الوقت المستهدف الوقت الذي تستخدمه الأوامر لقراءة مستودع على تخزين يدعم تعدد الإصدارات (versioned). يتيح هذا للأمر قراءة المستودع كما كان عند نقطة زمنية معينة لاسترداد بيانات حُذفت أو أُتلفت بسبب خطأ من المستخدم أو برمجية خبيثة.

التخزين الذي يدعم تعدد الإصدارات مدعوم في S3 وGCS وAzure لكنه غير ممكَّن افتراضيًا بشكل عام. بالإضافة إلى تمكين الإصدارات، قد يكون من المفيد تمكين قفل الكائنات لـ S3 والحذف الناعم لـ GCS أو Azure.

عندما يُحدَّد الخيار `repo-target-time` فيجب تقديم الخيار `repo` أيضًا. من المرجح أن ليست كل أنواع المستودعات تدعم الإصدارات، وعمومًا من المنطقي استهداف مستودع واحد للاسترداد.

لاحظ أن المقارنات مع الطابع الزمني للتخزين تكون <= للطابع الزمني المقدم، وتُقتطع المللي ثانية من الطابع الزمني عند تقديمه.

```yaml
example: --repo-target-time=2024-08-08 12:12:12+00
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
