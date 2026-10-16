---
title: "إعداد Patroni"
weight: 30
icon: fa-solid fa-code
description: "نموذج إعداد Patroni وقواعد الأسبقية وأدوات التحقق."
sidebar_expanded: true
module: [PATRONI]
categories: [مرجع]
upstream_link: "https://patroni.readthedocs.io/en/latest/patroni_configuration.html"
---

<a id="config"></a>
هناك 3 أنواع من إعداد Patroni:

- [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) العامة.  
  تُخزن هذه الخيارات في DCS (مخزن الإعداد الموزع) وتُطبق على جميع عقد العنقود. يمكن ضبط التهيئة الديناميكية في أي وقت باستخدام أداة [patronictl_edit_config](/ar/patroni/patronictl#patronictl_edit_config) أو [REST API](/ar/patroni/rest_api#rest_api) في Patroni. إذا لم تكن الخيارات المتغيرة جزءًا من تهيئة بدء التشغيل، فإنها تُطبق بشكل غير متزامن (عند دورة الاستيقاظ التالية) على كل عقدة، التي يُعاد تحميلها بعد ذلك. وإذا كانت العقدة تتطلب إعادة تشغيل لتطبيق التهيئة (بالنسبة لـ[معاملات PostgreSQL](https://www.postgresql.org/docs/current/view-pg-settings.html) ذات السياق postmaster، إذا تغيرت قيمها)، فسيُضبط علم خاص `pending_restart` يشير إلى ذلك في members.data JSON. بالإضافة إلى ذلك، تشير حالة العقدة إلى ذلك بعرض `"restart_pending": true`.

- [ملف التهيئة](/ar/patroni/config/yaml#yaml) المحلي (patroni.yml).  
  تُعرَّف هذه الخيارات في ملف التهيئة وتأخذ الأسبقية على التهيئة الديناميكية. يمكن تغيير `patroni.yml` وإعادة تحميله في وقت التشغيل (دون إعادة تشغيل Patroni) بإرسال SIGHUP إلى عملية Patroni، أو تنفيذ طلب `POST /reload` عبر REST-API، أو تنفيذ [patronictl_reload](/ar/patroni/patronictl#patronictl_reload). يمكن أن تكون التهيئة المحلية ملف YAML واحدًا أو دليلًا. عندما يكون دليلًا، تُحمَّل جميع ملفات YAML في ذلك الدليل واحدًا تلو الآخر بترتيب فرزها. في حال تعريف مفتاح في عدة ملفات، فإن وجوده في الملف الأخير يأخذ الأسبقية.

- [تهيئة البيئة](/ar/patroni/config/env#env).  
  من الممكن ضبط/تجاوز بعض معاملات التهيئة "المحلية" بمتغيرات البيئة. تهيئة البيئة مفيدة جدًا عندما تعمل في بيئة ديناميكية ولا تعرف بعض المعاملات مسبقًا (مثلًا لا يمكن معرفة عنوان IP الخارجي لديك عندما تعمل داخل `docker`).

<a id="important_configuration_rules"></a>

--------

## قواعد مهمة {#important-rules}

### معاملات PostgreSQL التي يتحكم بها Patroni {#postgresql-parameters-controlled-by-patroni}

بعض معاملات PostgreSQL **يجب أن تحمل القيم نفسها على العقدة الرئيسية والنسخ المتماثلة**. بالنسبة لها، **القيم المضبوطة إما في ملفات تهيئة patroni المحلية أو عبر متغيرات البيئة ليس لها أي تأثير**. لتغيير قيمها أو ضبطها يجب تغيير التهيئة المشتركة في DCS. فيما يلي القائمة الفعلية لهذه المعاملات مع القيم الافتراضية والدنيا:

- **max_connections**: القيمة الافتراضية 100، والقيمة الدنيا 25
- **max_locks_per_transaction**: القيمة الافتراضية 64، والقيمة الدنيا 32
- **max_worker_processes**: القيمة الافتراضية 8، والقيمة الدنيا 2
- **max_prepared_transactions**: القيمة الافتراضية 0، والقيمة الدنيا 0
- **wal_level**: القيمة الافتراضية hot_standby، والقيم المقبولة: hot_standby, replica, logical
- **track_commit_timestamp**: القيمة الافتراضية off

بالنسبة للمعاملات أدناه، لا يشترط PostgreSQL قيمًا متساوية بين العقدة الرئيسية وجميع النسخ المتماثلة. مع ذلك، ونظرًا لإمكانية أن تصبح نسخة متماثلة هي العقدة الرئيسية في أي وقت، لا معنى حقًا لضبطها بشكل مختلف؛ لذلك، **يقيّد Patroni ضبط قيمها على** [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic).

- **max_wal_senders**: القيمة الافتراضية 10، والقيمة الدنيا 3
- **max_replication_slots**: القيمة الافتراضية 10، والقيمة الدنيا 4
- **wal_keep_segments**: القيمة الافتراضية 8، والقيمة الدنيا 1
- **wal_keep_size**: القيمة الافتراضية 128MB، والقيمة الدنيا 16MB
- **wal_log_hints**: on

يتم التحقق من هذه المعاملات لضمان أنها سليمة، أو أنها تلبي قيمة دنيا.

هناك بعض معاملات Postgres الأخرى التي يتحكم بها Patroni:

- **listen_addresses** - يُضبط إما من `postgresql.listen` أو من متغير البيئة `PATRONI_POSTGRESQL_LISTEN`
- **port** - يُضبط إما من `postgresql.listen` أو من متغير البيئة `PATRONI_POSTGRESQL_LISTEN`
- **cluster_name** - يُضبط إما من `scope` أو من متغير البيئة `PATRONI_SCOPE`
- **hot_standby: on**

احتياطًا، تُكتب المعاملات من القوائم أعلاه في `postgresql.conf`، وتُمرر كقائمة وسائط إلى `postgres` مما يمنحها الأسبقية الأعلى (باستثناء `wal_keep_segments` و`wal_keep_size`)، حتى فوق [ALTER SYSTEM](https://www.postgresql.org/docs/current/static/sql-altersystem.html)

هناك أيضًا بعض المعاملات مثل **postgresql.listen** و**postgresql.data_dir** التي **يمكن ضبطها محليًا فقط**، أي في [ملف تهيئة](/ar/patroni/config/yaml#yaml) Patroni أو عبر متغير [تهيئة البيئة](/ar/patroni/config/env#env). في معظم الحالات ستتجاوز التهيئة المحلية التهيئة الديناميكية.

عند تطبيق خيارات التهيئة المحلية أو الديناميكية، تُتخذ الإجراءات التالية:

- تتحقق العقدة أولًا مما إذا كان هناك ملف `postgresql.base.conf` أو إذا كان المعامل `custom_conf` مضبوطًا.
- إذا كان المعامل `custom_conf` مضبوطًا، فسيُستخدم الملف الذي يحدده كتهيئة أساسية، مع تجاهل `postgresql.base.conf` و`postgresql.conf`.
- إذا لم يكن المعامل `custom_conf` مضبوطًا ووُجد `postgresql.base.conf`، فإنه يحتوي على التهيئة «الأصلية» المعاد تسميتها ويُستخدم كتهيئة أساسية.
- إذا لم يوجد `custom_conf` ولا `postgresql.base.conf`، يُعاد تسمية `postgresql.conf` الأصلي إلى `postgresql.base.conf` ويُستخدم كتهيئة أساسية.
- تُفرَّغ الخيارات الديناميكية (مع الاستثناءات أعلاه) في `postgresql.conf` ويُضبط تضمين في `postgresql.conf` للتهيئة الأساسية (إما `postgresql.base.conf` أو الملف في `custom_conf`). لذلك، سنتمكن من تطبيق خيارات جديدة دون إعادة قراءة ملف التهيئة للتحقق من وجود التضمين من عدمه.
- تُتجاوز بعض المعاملات الأساسية لإدارة Patroni للعنقود باستخدام سطر الأوامر.
- إذا غُيّر خيار يتطلب إعادة تشغيل (يجب أن ننظر إلى السياق في pg_settings وإلى القيم الفعلية لتلك الخيارات)، يُضبط علم pending_restart على تلك العقدة. يُعاد ضبط هذا العلم عند أي إعادة تشغيل.

ستُطبق المعاملات بالترتيب التالي (تُمنح معاملات وقت التشغيل الأسبقية الأعلى):

1.  تحميل المعاملات من الملف `postgresql.base.conf` (أو من ملف `custom_conf`، إذا كان مضبوطًا)
2.  تحميل المعاملات من الملف `postgresql.conf`
3.  تحميل المعاملات من الملف `postgresql.auto.conf`
4.  معامل وقت التشغيل باستخدام `-o --name=value`

يتيح ذلك تهيئة جميع العقد (2)، وتهيئة عقدة معينة باستخدام `ALTER SYSTEM` (3)، ويضمن فرض المعاملات الأساسية لتشغيل Patroni (4)، فضلًا عن ترك مجال لأدوات التهيئة التي تدير `postgresql.conf` مباشرة دون إشراك Patroni (1).

<a id="shared_memory_gucs"></a>

### معاملات PostgreSQL التي تمس الذاكرة المشتركة {#postgresql-parameters-that-touch-shared-memory}

لدى PostgreSQL بعض المعاملات التي تحدد حجم الذاكرة المشتركة المستخدمة من قبلها:

- **max_connections**
- **max_prepared_transactions**
- **max_locks_per_transaction**
- **max_wal_senders**
- **max_worker_processes**

يتطلب تغيير هذه المعاملات إعادة تشغيل PostgreSQL لتصبح سارية، ولا يمكن أن تكون بنيات الذاكرة المشتركة الخاصة بها أصغر على عقد الاستعداد منها على العقدة الرئيسية.

كما هو موضح سابقًا، يقيّد Patroni تغيير قيمها عبر [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic)، والتي تتكون عادةً من:

1.  تطبيق التغييرات عبر [patronictl_edit_config](/ar/patroni/patronictl#patronictl_edit_config) (أو عبر نقطة النهاية `/config` في REST API)
2.  إعادة تشغيل العقد عبر [patronictl_restart](/ar/patroni/patronictl#patronictl_restart) (أو عبر نقطة النهاية `/restart` في REST API)

**ملاحظة:** يرجى أن تضع في اعتبارك أنه يجب عليك تنفيذ إعادة تشغيل عقد PostgreSQL عبر أمر [patronictl_restart](/ar/patroni/patronictl#patronictl_restart)، أو عبر نقطة النهاية `/restart` في REST API. قد تؤدي محاولة إعادة تشغيل PostgreSQL عبر إعادة تشغيل daemon الخاص بـ Patroni، مثل تنفيذ `systemctl restart patroni`، إلى حدوث تجاوز أعطال في العنقود، إذا كنت تعيد تشغيل العقدة الرئيسية.

مع ذلك، وبما أن تلك الإعدادات تدير الذاكرة المشتركة، فيجب توخي حذر إضافي عند إعادة تشغيل العقد:

- إذا أردت **زيادة** قيمة أي من تلك الإعدادات:

  > 1.  أعد تشغيل جميع عقد الاستعداد أولًا
  > 2.  أعد تشغيل العقدة الرئيسية بعد ذلك

- إذا أردت **إنقاص** قيمة أي من تلك الإعدادات:

  > 1.  أعد تشغيل العقدة الرئيسية أولًا
  > 2.  أعد تشغيل جميع عقد الاستعداد بعد ذلك

**ملاحظة:** إذا حاولت إعادة تشغيل جميع العقد دفعة واحدة بعد **إنقاص** قيمة أي من تلك الإعدادات، فسيتجاهل Patroni التغيير ويعيد تشغيل عقدة الاستعداد بالقيمة الأصلية للإعداد، ما يستلزم إعادة تشغيل عقد الاستعداد مرة أخرى لاحقًا. يفعل Patroni ذلك لمنع دخول عقدة الاستعداد في حلقة انهيار لا نهائية، لأن PostgreSQL يتوقف برسالة `FATAL` إذا حاولت ضبط أي من تلك المعاملات على قيمة أدنى مما هو ظاهر في `pg_controldata` على عقدة الاستعداد. بعبارة أخرى، لا يمكننا إنقاص الإعداد على عقدة الاستعداد إلا بعد أن يصبح `pg_controldata` الخاص بها محدثًا من العقدة الرئيسية فيما يتعلق بهذه التغييرات على العقدة الرئيسية.

يمكن العثور على مزيد من المعلومات حول ذلك في [نظرة عامة لمسؤول PostgreSQL](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN).

### معاملات إعداد Patroni {#patroni-configuration-parameters}

أيضًا خيارات إعداد Patroni التالية **يمكن تغييرها ديناميكيًا فقط**:

- **ttl**: 30
- **loop_wait**: 10
- **retry_timeout**: 10
- **maximum_lag_on_failover**: 1048576
- **max_timelines_history**: 0
- **check_timeline**: false
- **postgresql.use_slots**: true

عند تغيير هذه الخيارات، سيقرأ Patroni القسم ذي الصلة من التهيئة المخزنة في DCS ويغير قيم وقت التشغيل الخاصة به.

تحفظ عقد Patroni تهيئة DCS على القرص بعد كل تغيير في التهيئة، في الملف `patroni.dynamic.json` الواقع في دليل بيانات Postgres. يُسمح فقط للقائد باستعادة هذه الخيارات من النسخة المفرغة على القرص إذا كانت غائبة تمامًا عن DCS أو إذا كانت غير صالحة.

<a id="validate_generate_config"></a>

--------

## توليد التهيئة والتحقق منها {#configuration-generation-and-validation}

يوفر Patroni واجهات سطر أوامر لتوليد [تهيئة Patroni المحلية](/ar/patroni/config/yaml#yaml) والتحقق منها. باستخدام الملف التنفيذي `patroni` يمكنك:

- إنشاء نموذج تهيئة محلية لـ Patroni؛
- إنشاء ملف تهيئة Patroni لمثيل PostgreSQL العامل محليًا (مثلًا كخطوة تحضيرية لـ[تكامل Patroni](/ar/patroni/existing_data#existing_data))؛
- التحقق من صحة ملف تهيئة Patroni معين.

<a id="generate_sample_config"></a>

### نموذج تهيئة Patroni {#sample-patroni-configuration}

```text
patroni --generate-sample-config [configfile]
```

#### الوصف {#description}

توليد ملف تهيئة نموذجي لـ Patroni بصيغة `yaml`. تُحدد قيم المعاملات باستخدام [تهيئة البيئة](/ar/patroni/config/env#env)، وإلا، إن لم تكن مضبوطة، فالافتراضيات المستخدمة في Patroni أو السلسلة `#FIXME` للقيم التي ينبغي على المستخدم تحديدها لاحقًا.

تُحدد بعض القيم الافتراضية بناءً على الإعداد المحلي:

> - **postgresql.listen**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `5432`.
> - **postgresql.connect_address**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `5432`.
> - **postgresql.authentication.rewind**: لا يُعرَّف إلا إذا أمكن تحديد إصدار PostgreSQL من الملف الثنائي وكان الإصدار 11 أو أحدث.
> - **restapi.listen**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `8008`.
> - **restapi.connect_address**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `8008`.

#### المعاملات {#parameters}

`configfile` - المسار الكامل لملف التهيئة المستخدم لتخزين النتيجة. إذا لم يُقدم، تُرسل النتيجة إلى `stdout`.

<a id="generate_config"></a>

### تهيئة Patroni لمثيل قيد التشغيل {#patroni-configuration-for-a-running-instance}

```text
patroni --generate-config [--dsn DSN] [configfile]
```

#### الوصف {#description-1}

توليد تهيئة Patroni بصيغة `yaml` لمثيل PostgreSQL العامل محليًا. سيُستخدم للاتصال بـ PostgreSQL إما DSN المقدم (يأخذ الأسبقية) أو [متغيرات البيئة](https://www.postgresql.org/docs/current/libpq-envars.html) الخاصة بـ PostgreSQL. إذا لم تُقدم كلمة المرور، فينبغي إدخالها عبر موجّه الإدخال (prompt).

ستُستخدم جميع معاملات GUC غير الداخلية المعرّفة في مثيل Postgres المصدر، بصرف النظر عما إذا كانت مضبوطة عبر ملف تهيئة أو عبر سطر أوامر postmaster أو عبر متغيرات البيئة، كمصدر لمعاملات تهيئة Patroni التالية:

> - **scope**: قيمة GUC لـ `cluster_name`؛
> - **postgresql.listen**: قيم GUC لـ `listen_addresses` و`port`؛
> - **postgresql.data_dir**: قيمة GUC لـ `data_directory`؛
> - **postgresql.parameters**: قيم GUC لـ `archive_command`, `restore_command`, `archive_cleanup_command`, `recovery_end_command`, `ssl_passphrase_command`, `hba_file`, `ident_file`, `config_file`؛
> - **bootstrap.dcs**: جميع معاملات GUC الأخرى المجمعة من PostgreSQL.

إذا لم يُضبط `scope` أو `postgresql.listen` أو `postgresql.data_dir` من معاملات GUC الخاصة بـ Postgres، فتُستخدم قيمة [تهيئة البيئة](/ar/patroni/config/env#env) المقابلة.

قواعد أخرى مطبقة في تحديد القيم:

> - **name**: قيمة متغير البيئة `PATRONI_NAME` إذا كان مضبوطًا، وإلا اسم المضيف الحالي للجهاز.
> - **postgresql.bin_dir**: المسار إلى ملفات Postgres الثنائية المجمعة من المثيل قيد التشغيل.
> - **postgresql.connect_address**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ المستخدم لاتصال المثيل أو قيمة GUC لـ `port`.
> - **postgresql.authentication.superuser**: التهيئة المستخدمة لاتصال المثيل؛
> - **postgresql.pg_hba**: الأسطر المجمعة من `hba_file` للمثيل المصدر.
> - **postgresql.pg_ident**: الأسطر المجمعة من `ident_file` للمثيل المصدر.
> - **restapi.listen**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `8008`.
> - **restapi.connect_address**: عنوان IP الذي يحله `getaddrinfo` من اسم المضيف الحالي للجهاز الذي يعيده `gethostname` والمنفذ القياسي `8008`.

تُضم أيضًا في التهيئة المعاملات الأخرى المحددة باستخدام [تهيئة البيئة](/ar/patroni/config/env#env).

#### المعاملات {#parameters-1}

`configfile`  
المسار الكامل لملف التهيئة المستخدم لتخزين النتيجة. إذا لم يُقدم، تُرسل النتيجة إلى `stdout`.

`dsn`  
سلسلة DSN اختيارية للمثيل المحلي لـ PostgreSQL للحصول على قيم GUC منه.

### التحقق من صحة تهيئة Patroni {#validate-patroni-configuration}

```text
patroni --validate-config [configfile] [--ignore-listen-port | -i]
```

#### الوصف {#description-2}

التحقق من صحة تهيئة Patroni المعطاة وطباعة المعلومات حول الفحوصات الفاشلة.

#### المعاملات {#parameters-2}

`configfile`  
المسار الكامل لملف التهيئة المراد فحصه. إذا لم يُعطَ أو لم يوجد الملف، فسيحاول القراءة من متغير البيئة `PATRONI_CONFIGURATION` أو، إن لم يكن مضبوطًا، من [متغيرات بيئة Patroni](/ar/patroni/config/env#env).

`--ignore-listen-port | -i`  
علم اختياري لتجاهل إخفاقات الربط لمنافذ `listen` المستخدمة بالفعل عند التحقق من صحة `configfile`.

`--print | -p`  
علم اختياري لطباعة التهيئة المحلية (بما في ذلك تجاوزات تهيئة البيئة) بعد التحقق من صحتها بنجاح.
