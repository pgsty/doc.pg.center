---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "مرجع الأوامر لإعداد patronictl وصياغته وأوامره الفرعية."
module: [PATRONI]
categories: [مرجع]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
يتوفر Patroni على واجهة سطر أوامر تُدعى [patronictl](/ar/patroni/patronictl#patronictl)، تُستخدم أساسًا للتفاعل مع واجهة REST API الخاصة بـ Patroni ومع DCS. الغرض منها تسهيل تنفيذ العمليات في العنقود، ويمكن للبشر أو للسكربتات استخدامها بسهولة.

<a id="patronictl_configuration"></a>

--------

## الإعداد {#configuration}

يستخدم [patronictl](/ar/patroni/patronictl#patronictl) 3 أقسام من الإعداد:

- **ctl**: كيفية المصادقة على واجهة REST API الخاصة بـ Patroni، وكيفية التحقق من هوية الخادم. راجع [إعدادات ctl](/ar/patroni/config/yaml#patronictl_settings) لمزيد من التفاصيل؛
- **restapi**: كيفية المصادقة على واجهة REST API الخاصة بـ Patroni، وكيفية التحقق من هوية الخادم. يُستخدم فقط إذا لم يكن إعداد `ctl` كافيًا. يهتم [patronictl](/ar/patroni/patronictl#patronictl) أساسًا بقسم `restapi.authentication` (في حال غياب `ctl.authentication`) وإعداد `restapi.cafile` (في حال غياب `ctl.cacert`). راجع [إعدادات REST API](/ar/patroni/config/yaml#restapi_settings) لمزيد من التفاصيل؛
- DCS (مثل **etcd**): كيفية الاتصال بـ DCS الذي يستخدمه Patroni والمصادقة عليه.

يمكن أن تأتي خيارات الإعداد هذه إما من متغيرات البيئة أو من ملف إعداد. ابحث عن الأقسام أعلاه في [إعدادات الإعداد عبر متغيرات البيئة](/ar/patroni/config/env#env) أو [إعدادات الإعداد عبر YAML](/ar/patroni/config/yaml#yaml) لتفهم كيف يمكنك ضبط خياراتها عبر متغيرات البيئة أو عبر ملف إعداد.

إذا اخترت استخدام متغيرات البيئة، فالطريقة مباشرة. سيقرأ patronictl متغيرات البيئة ويستخدم قيمها.

إذا اخترت استخدام ملف إعداد، فلديك طرق مختلفة لإخبار [patronictl](/ar/patroni/patronictl#patronictl) بالملف المراد استخدامه. افتراضيًا سيحاول [patronictl](/ar/patroni/patronictl#patronictl) تحميل ملف إعداد باسم `patronictl.yaml`، ويتوقع العثور عليه في أحد هذه المسارات، بحسب نظامك:

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (ملف تعريف متنقل): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (ملف تعريف غير متنقل): `C:\Users\<user>\AppData\Local\patroni`

يمكنك تجاوز هذا السلوك بإحدى الطريقتين التاليتين:

- ضبط متغير البيئة `PATRONICTL_CONFIG_FILE` على مسار ملف إعداد مخصص؛
- استخدام وسيط سطر الأوامر `-c` / `--config-file` الخاص بـ [patronictl](/ar/patroni/patronictl#patronictl) مع مسار ملف إعداد مخصص.

> [!NOTE]
> إذا كنت تشغّل [patronictl](/ar/patroni/patronictl#patronictl) على المضيف نفسه الذي يعمل عليه البرنامج الخفي `patroni`، فيمكنك ببساطة استخدام ملف الإعداد نفسه إذا كان يحتوي على جميع أقسام الإعداد التي يحتاجها [patronictl](/ar/patroni/patronictl#patronictl).

<a id="patronictl_usage"></a>

--------

## الاستخدام {#usage}

يوفر [patronictl](/ar/patroni/patronictl#patronictl) عدة عمليات مفيدة. يهدف هذا القسم إلى وصف كل منها.

قبل الانتقال إلى كل من الأوامر الفرعية لـ [patronictl](/ar/patroni/patronictl#patronictl)، كن على دراية بأن [patronictl](/ar/patroni/patronictl#patronictl) نفسه يقبل وسائط سطر الأوامر التالية:

`-c` / `--config-file`  
كما شُرح سابقًا، تُستخدم لتوفير مسار ملف إعداد لـ [patronictl](/ar/patroni/patronictl#patronictl).

`-d` / `--dcs-url` / `--dcs`  
توفر سلسلة اتصال بـ DCS الذي يستخدمه Patroni.

يمكن استخدام هذا الوسيط إما لتجاوز إعدادات DCS و`namespace` الواردة في إعداد [patronictl](/ar/patroni/patronictl#patronictl)، أو لتعريفها إذا كانت غائبة عن الإعداد.

يجب أن تكون القيمة بالصيغة `DCS://HOST:PORT/NAMESPACE`، مثل `etcd3://localhost:2379/service` للاتصال بـ etcd v3 يعمل على `localhost` مع تخزين عنقود Patroni تحت نطاق `service`. أي جزء مفقود من قيمة الوسيط سيُستبدل بالقيمة الموجودة في الإعداد أو بقيمته الافتراضية.

`-k` / `--insecure`  
علامة لتجاوز التحقق من شهادة SSL لخادم REST API.

هذه هي الصيغة العامة لتشغيل أمر من [patronictl](/ar/patroni/patronictl#patronictl):

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> هذه هي اصطلاحات الصياغة المستخدمة في الصيغة العامة:
>
> - الخيارات بين الأقواس المربعة اختيارية؛
> - الخيارات بين الأقواس المعقوفة تمثل عملية «اختر واحدًا من المجموعة»؛
> - الخيارات ذات `[, ... ]` يمكن تحديدها مرات متعددة؛
> - ما يُكتب بأحرف كبيرة يمثل قيمة حرفية ينبغي إعطاؤها قيمة.
>
> سنستخدم الصياغة نفسها عند وصف الأوامر الفرعية لـ [patronictl](/ar/patroni/patronictl#patronictl) في الأقسام الفرعية التالية. أيضًا، عند وصف الأوامر الفرعية في الأقسام الفرعية التالية، ينبغي اعتبار الصيغة العامة للأمر بديلًا عن `SUBCOMMAND` في الصيغة العامة أعلاه.

في الأقسام الفرعية التالية يمكنك أن تجد وصفًا لكل أمر ينفذه [patronictl](/ar/patroni/patronictl#patronictl). ومن باب التوضيح بالأمثلة، سنستخدم ملفات الإعداد الموجودة في مستودع GitHub الخاص بـ Patroni (الملفات `postgres0.yml` و`postgres1.yml` و`postgres2.yml`).

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### الصيغة العامة {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### الوصف {#description}

يحوّل `patronictl demote-cluster` عنقود Patroni عاديًا إلى [عنقود استعداد](/ar/patroni/standby_cluster#standby_cluster).

يرقّع الأمر الإعداد الديناميكي بقسم `standby_cluster` مبني من خيارات الاتصال بالأساسي البعيد المقدَّمة، ثم ينتظر حتى يعمل القائد كقائد استعداد. يطبع طوبولوجيا العنقود الحالية قبل تغيير الإعداد ويطلب التأكيد ما لم يُستخدم `--force`.

يجب تحديد واحد من `--host` أو `--port` أو `--restore-command` على الأقل.

<a id="patronictl_demote_cluster_parameters"></a>

#### المعاملات {#parameters}

`CLUSTER_NAME`: اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--host`: عنوان العقدة البعيدة.

`--port`: منفذ العقدة البعيدة.

`--restore-command`: أمر لاستعادة سجلات WAL من الأساسي البعيد.

`--primary-slot-name`: اسم فتحة النسخ المتماثل على العقدة البعيدة التي ستُستخدم للنسخ المتماثل.

`--force`: علامة لتخطي مطالبات التأكيد عند تخفيض العنقود.

مفيد للسكربتات.

<a id="patronictl_demote_cluster_examples"></a>

#### أمثلة {#examples}

تخفيض العنقود إلى عنقود استعداد يتبع نقطة نهاية أساسي بعيد:

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### الصيغة العامة {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### الوصف {#description-1}

يجلب `patronictl dsn` سلسلة الاتصال لأحد أعضاء عنقود Patroni.

إذا طابقت عدة أعضاء معاملات هذا الأمر، فسيُختار أحدهم، مع إعطاء الأولوية للعقدة الأساسية.

<a id="patronictl_dsn_parameters"></a>

#### المعاملات {#parameters-1}

`CLUSTER_NAME`: اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`-r` / `--role`  
اختيار عضو له الدور المعطى.

يمكن أن يكون الدور أحد التالي:

- `leader`: قائد عنقود Patroni عادي أو عنقود استعداد Patroni؛ أو
- `primary`: قائد عنقود Patroni عادي؛ أو
- `standby-leader`: قائد عنقود استعداد Patroni؛ أو
- `replica`: نسخة متماثلة في عنقود Patroni؛ أو
- `standby`: نفس `replica`؛ أو
- `any`: أي دور. مثل حذف هذا المعامل؛ أو

`-m` / `--member`  
اختيار عضو في العنقود بالاسم المعطى.

`MEMBER_NAME` هو اسم العضو.

`--group`  
اختيار عضو يشكل جزءًا من مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

<a id="patronictl_dsn_examples"></a>

#### أمثلة {#examples-1}

جلب DSN الخاص بالعقدة الأساسية:

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

جلب DSN الخاص بالعقدة المسماة `postgresql1`:

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### الصيغة العامة {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### الوصف {#description-2}

يغيّر `patronictl edit-config` الإعداد الديناميكي للعنقود ويحدّث DCS به.

> [!NOTE]
> عند استدعائه عبر TTY يحاول الأمر عرض فروقات الإعداد الديناميكي عبر عارض صفحات (pager). افتراضيًا يحاول استخدام `less` أو `more`. إذا أردت عارضًا مختلفًا، فاضبط متغير البيئة `PAGER` على العارض المطلوب.

<a id="patronictl_edit_config_parameters"></a>

#### المعاملات {#parameters-2}

`CLUSTER_NAME`: اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
تغيير الإعداد الديناميكي لمجموعة Citus المعطاة.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `citus.group`، إن وُجد.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-q` / `--quiet`  
علامة لتخطي عرض فروقات الإعداد.

`-s` / `--set`  
ضبط خيار إعداد ديناميكي معطى بقيمة معطاة.

`CONFIG` هو اسم مسار الإعداد الديناميكي في شجرة YAML، مع وصل المستويات بـ `.`.

`VALUE` هي قيمة `CONFIG`. إذا كانت `null`، فسيُزال `CONFIG` من الإعداد الديناميكي.

`-p` / `--pg`  
ضبط خيار إعداد Postgres ديناميكي معطى بالقيمة المعطاة.

هو في الأساس اختصار لـ `-s` / `--set` مع إلحاق بادئة `postgresql.parameters.` بـ `CONFIG`.

`PG_CONFIG` هو اسم إعداد Postgres الذي سيُضبط.

`PG_VALUE` هي قيمة `PG_CONFIG`. إذا كانت `null`، فسيُزال `PG_CONFIG` من الإعداد الديناميكي.

`--apply`  
تطبيق الإعداد الديناميكي من الملف المعطى.

هو مشابه لتحديد خيارات `-s` / `--set` متعددة، خيار واحد لكل إعداد من `CONFIG_FILE`.

`CONFIG_FILE` هو المسار إلى ملف يحتوي على الإعداد الديناميكي المراد تطبيقه، بصيغة YAML. استخدم `-` إذا أردت القراءة من `stdin`.

`--replace`  
استبدال الإعداد الديناميكي في DCS بالإعداد الديناميكي المحدد في الملف المعطى.

`CONFIG_FILE` هو المسار إلى ملف يحتوي على الإعداد الديناميكي الجديد الذي سيدخل حيز التنفيذ، بصيغة YAML. استخدم `-` إذا أردت القراءة من `stdin`.

`--force`  
علامة لتخطي مطالبات التأكيد عند تغيير الإعداد الديناميكي.

مفيد للسكربتات.

<a id="patronictl_edit_config_examples"></a>

#### أمثلة {#examples-2}

تغيير الـ GUC `max_connections` في Postgres:

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

تغيير الإعدادين `loop_wait` و`ttl`:

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

إزالة إعداد `maximum_lag_on_failover` من الإعداد الديناميكي:

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### الصيغة العامة {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### الوصف {#description-3}

ينفّذ `patronictl failover` تجاوز أعطال يدويًا في العنقود.

صُمم ليُستخدم عندما لا يكون العنقود سليمًا، مثلًا:

- لا يوجد قائد؛ أو
- لا توجد عقدة استعداد متزامنة متاحة في عنقود متزامن.

كما يسمح بتجاوز الأعطال إلى عقدة غير متزامنة إذا كان الوضع المتزامن مفعّلًا.

> [!NOTE]
> لا شيء يمنعك من تشغيل `patronictl failover` في عنقود سليم. ومع ذلك، نوصي باستخدام `patronictl switchover` في تلك الحالات.

> [!WARNING]
> قد يؤدي تشغيل تجاوز الأعطال إلى فقدان بيانات اعتمادًا على مدى حداثة النسخة المتماثلة المرقّاة مقارنة بالأساسي.

<a id="patronictl_failover_parameters"></a>

#### المعاملات {#parameters-3}

`CLUSTER_NAME`: اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
تنفيذ تجاوز الأعطال في مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`--candidate`  
العقدة التي ستُرقَّى عند تجاوز الأعطال.

`CANDIDATE_NAME` هو اسم العقدة التي ستُرقَّى.

`--force`  
علامة لتخطي مطالبات التأكيد عند تنفيذ تجاوز الأعطال.

مفيد للسكربتات.

<a id="patronictl_failover_examples"></a>

#### أمثلة {#examples-3}

تجاوز الأعطال إلى العقدة `postgresql2`:

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### الصيغة العامة {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### الوصف {#description-4}

يتخلص `patronictl flush` من الأحداث المجدولة، إن وُجدت.

<a id="patronictl_flush_parameters"></a>

#### المعاملات {#parameters-4}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`MEMBER_NAME`  
التخلص من الأحداث المجدولة لعضو/أعضاء Patroni المعطين.

يمكن تحديد عدة أعضاء. إذا لم يُحدد أي عضو، تُؤخذ جميعها في الحسبان.

> [!NOTE]
> يُستخدم فقط عند التخلص من أحداث إعادة التشغيل المجدولة.

`restart`  
التخلص من أحداث إعادة التشغيل المجدولة.

`switchover`  
التخلص من حدث التبديل المجدول.

`--group`  
التخلص من الأحداث المجدولة من مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-r` / `--role`  
التخلص من الأحداث المجدولة للأعضاء الذين لهم الدور المعطى.

يمكن أن يكون الدور أحد التالي:

- `leader`: قائد عنقود Patroni عادي أو عنقود استعداد Patroni؛ أو
- `primary`: قائد عنقود Patroni عادي؛ أو
- `standby-leader`: قائد عنقود استعداد Patroni؛ أو
- `replica`: نسخة متماثلة في عنقود Patroni؛ أو
- `standby`: نفس `replica`؛ أو
- `any`: أي دور. مثل حذف هذا المعامل.

> [!NOTE]
> يُستخدم فقط عند التخلص من أحداث إعادة التشغيل المجدولة.

`--force`  
علامة لتخطي مطالبات التأكيد عند تنفيذ flush.

مفيد للسكربتات.

<a id="patronictl_flush_examples"></a>

#### أمثلة {#examples-4}

التخلص من حدث تبديل مجدول:

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

التخلص من إعادة التشغيل المجدولة لجميع عقد الاستعداد:

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

التخلص من إعادة التشغيل المجدولة للعقدتين `postgresql0` و`postgresql1`:

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### الصيغة العامة {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### الوصف {#description-5}

يعرض `patronictl history` سجل أحداث تجاوز الأعطال والتبديل في العنقود، إن وُجدت.

تُضمَّن المعلومات التالية في المخرجات:

`TL`  
الخط الزمني (timeline) في Postgres الذي وقع عنده الحدث.

`LSN`  
موقع LSN في Postgres الذي وقع عنده الحدث.

`Reason`  
السبب كما جُلب من ملف `.history` الخاص بـ Postgres.

`Timestamp`  
الوقت الذي وقع فيه الحدث.

`New Leader`  
عضو Patroni الذي رُقّي خلال الحدث.

<a id="patronictl_history_parameters"></a>

#### المعاملات {#parameters-5}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
عرض سجل أحداث مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `citus.group`، إن وُجد.

`-f` / `--format`  
كيفية تنسيق قائمة الأحداث في المخرجات.

يمكن أن يكون التنسيق أحد التالي:

- `pretty`: يطبع السجل كجدول منسق؛ أو
- `tsv`: يطبع السجل معلوماتٍ جدولية مع فصل الأعمدة بـ `\t`؛ أو
- `json`: يطبع السجل بصيغة JSON؛ أو
- `yaml`: يطبع السجل بصيغة YAML.

الافتراضي هو `pretty`.

<a id="patronictl_history_examples"></a>

#### أمثلة {#examples-5}

عرض سجل الأحداث:

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

عرض سجل الأحداث بصيغة YAML:

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### الصيغة العامة {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### الوصف {#description-6}

يعرض `patronictl list` معلومات عن عنقود Patroni وأعضائه.

تُضمَّن المعلومات التالية في المخرجات:

`Cluster`  
اسم عنقود Patroni.

`Member`  
اسم عضو Patroni.

`Host`  
المضيف الذي يقع فيه العضو.

`Role`  
الدور الحالي للعضو.

يمكن أن يكون أحد ما يلي:

- `Leader`: القائد الحالي لعنقود Patroni عادي؛ أو
- `Standby Leader`: القائد الحالي لعنقود استعداد Patroni؛ أو
- `Sync Standby`: عقدة استعداد متزامنة في عنقود Patroni مع تفعيل الوضع المتزامن؛ أو
- `Replica`: عقدة استعداد عادية في عنقود Patroni.

`State`  
الحالة الحالية لـ Postgres في عضو Patroni.

بعض الأمثلة من الحالات الممكنة:

- `running`: إذا كان Postgres يعمل حاليًا؛
- `streaming`: إذا كانت نسخة متماثلة وكان Postgres يبث حاليًا سجلات WAL من العقدة الأساسية؛
- `in archive recovery`: إذا كانت نسخة متماثلة وكان Postgres يجلب حاليًا سجلات WAL من الأرشيف؛
- `stopped`: إذا كان Postgres قد أُوقف؛
- `crashed`: إذا كان Postgres قد انهار.

`TL`  
الخط الزمني الحالي لـ Postgres في عضو Patroni.

`Receive LSN`  
آخر موقع لسجل الكتابة المسبقة (WAL) استلمه النسخ المتماثل بالبث الخاص بالعضو وزامنه مع القرص (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
تأخر النسخ المتماثل بين موقع `Receive LSN` الخاص بالعضو ومصدره الأعلى (upstream) بوحدة MB.

`Replay LSN`  
آخر موقع لسجل الكتابة المسبقة (WAL) أُعيد تطبيقه أثناء الاستعادة في العضو (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
تأخر النسخ المتماثل بين موقع `Replay LSN` الخاص بالعضو ومصدره الأعلى (upstream) بوحدة MB.

بالإضافة إلى ذلك، قد تُضمَّن المعلومات التالية في المخرجات:

`System identifier`  
معرّف النظام في Postgres.

> [!NOTE]
> يظهر في رأس الجدول.
>
> يظهر فقط إذا كانت صيغة المخرجات `pretty`.

`Group`  
معرّف مجموعة Citus.

> [!NOTE]
> يظهر في رأس الجدول.
>
> يظهر فقط إذا كان عنقود Citus.

`Pending restart`  
تشير العلامة `*` إلى أن العقدة تحتاج إلى إعادة تشغيل كي يدخل بعض إعدادات Postgres حيز التنفيذ. القيمة الفارغة تشير إلى أن العقدة لا تتطلب إعادة تشغيل.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا:
>
> - كانت الطباعة بصيغة `pretty` أو `tsv` مع تفعيل المخرجات الموسعة؛ أو
> - كانت العقدة تتطلب إعادة تشغيل.

`Scheduled restart`  
الطابع الزمني الذي جُدولت عنده إعادة تشغيل لنسخة Postgres التي يديرها عضو Patroni. القيمة الفارغة تشير إلى عدم وجود إعادة تشغيل مجدولة للعضو.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا:
>
> - كانت الطباعة بصيغة `pretty` أو `tsv` مع تفعيل المخرجات الموسعة؛ أو
> - كانت للعقدة إعادة تشغيل مجدولة.

`Tags`  
يحتوي على الوسوم المضبوطة لعضو Patroni. القيمة الفارغة تشير إلى أنه إما لم تُضبط أي وسوم، أو أنها ضُبطت بقيم افتراضية.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا:
>
> - كانت الطباعة بصيغة `pretty` أو `tsv` مع تفعيل المخرجات الموسعة؛ أو
> - كانت للعقدة أي وسوم مخصصة، أو أي وسوم افتراضية بقيم غير افتراضية.

`Scheduled switchover`  
الطابع الزمني الذي جُدول عنده تبديل لعنقود Patroni، إن وُجد.

> [!NOTE]
> يظهر في تذييل الجدول.
>
> يظهر فقط إذا كان هناك تبديل مجدول، وكانت صيغة المخرجات `pretty`.

`Maintenance mode`

> إذا كانت مراقبة العنقود متوقفة مؤقتًا حاليًا.
>
> > [!NOTE]
> > يظهر في تذييل الجدول.
> >
> > يظهر فقط إذا كان العنقود في وضع الإيقاف المؤقت، وكانت صيغة المخرجات `pretty`.

<a id="patronictl_list_parameters"></a>

#### المعاملات {#parameters-6}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
عرض معلومات عن أعضاء مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-e` / `--extended`  
عرض معلومات موسعة.

يفرض عرض السمتين `Pending restart` و`Scheduled restart` والسمة `Tags`، حتى لو كانت قيمتها فارغة.

> [!NOTE]
> ينطبق فقط على صيغتي المخرجات `pretty` و`tsv`.

`-t` / `--timestamp`  
طباعة الطابع الزمني قبل طباعة المعلومات عن العنقود وأعضائه.

`-f` / `--format`  
كيفية تنسيق قائمة أعضاء العنقود في المخرجات.

يمكن أن يكون التنسيق أحد التالي:

- `pretty`: يطبع أعضاء العنقود كجدول منسق؛ أو
- `tsv`: يطبع أعضاء العنقود معلوماتٍ جدولية مع فصل الأعمدة بـ `\t`؛ أو
- `json`: يطبع أعضاء العنقود بصيغة JSON؛ أو
- `yaml`: يطبع أعضاء العنقود بصيغة YAML.

الافتراضي هو `pretty`.

`-W`  
تحديث المعلومات تلقائيًا كل ثانيتين.

`-w` / `--watch`  
تحديث المعلومات تلقائيًا بالفاصل الزمني المحدد.

`TIME` هو الفاصل بين التحديثات، بالثواني.

<a id="patronictl_list_examples"></a>

#### أمثلة {#examples-6}

عرض معلومات عن العنقود بصيغة pretty:

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

عرض معلومات عن العنقود بصيغة pretty مع الأعمدة الموسعة:

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

عرض معلومات عن العنقود بصيغة YAML، مع الطابع الزمني للتنفيذ:

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### الصيغة العامة {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### الوصف {#description-7}

يضع `patronictl pause` عنقود Patroni مؤقتًا في وضع الصيانة ويعطّل تجاوز الأعطال التلقائي.

<a id="patronictl_pause_parameters"></a>

#### المعاملات {#parameters-7}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
إيقاف مجموعة Citus المعطاة مؤقتًا.

`CITUS_GROUP` هو معرّف مجموعة Citus.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `citus.group`، إن وُجد.

`--wait`  
الانتظار حتى يتوقف جميع أعضاء Patroni مؤقتًا قبل إعادة التحكم إلى المستدعي.

<a id="patronictl_pause_examples"></a>

#### أمثلة {#examples-7}

وضع العنقود في وضع الصيانة، والانتظار حتى تتوقف جميع العقد مؤقتًا:

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### الصيغة العامة {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### الوصف {#description-8}

يحوّل `patronictl promote-cluster` عنقود الاستعداد إلى عنقود Patroni عادي.

يزيل الأمر قسم `standby_cluster` من الإعداد الديناميكي وينتظر حتى يعمل القائد كأساسي. يطبع طوبولوجيا العنقود الحالية قبل تغيير الإعداد ويطلب التأكيد ما لم يُستخدم `--force`.

<a id="patronictl_promote_cluster_parameters"></a>

#### المعاملات {#parameters-8}

`CLUSTER_NAME`: اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--force`: علامة لتخطي مطالبات التأكيد عند ترقية العنقود.

مفيد للسكربتات.

<a id="patronictl_promote_cluster_examples"></a>

#### أمثلة {#examples-8}

ترقية عنقود الاستعداد ليعمل كعنقود Patroni عادي:

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### الصيغة العامة {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### الوصف {#description-9}

ينفّذ `patronictl query` أمر SQL أو سكربت على أحد أعضاء عنقود Patroni.

<a id="patronictl_query_parameters"></a>

#### المعاملات {#parameters-9}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
الاستعلام عن مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-r` / `--role`  
اختيار عضو له الدور المعطى.

يمكن أن يكون الدور أحد التالي:

- `leader`: قائد عنقود Patroni عادي أو عنقود استعداد Patroni؛ أو
- `primary`: قائد عنقود Patroni عادي؛ أو
- `standby-leader`: قائد عنقود استعداد Patroni؛ أو
- `replica`: نسخة متماثلة في عنقود Patroni؛ أو
- `standby`: نفس `replica`؛ أو
- `any`: أي دور. مثل حذف هذا المعامل.

`-m` / `--member`  
اختيار عضو له الاسم المعطى.

`MEMBER_NAME` هو اسم العضو الذي سيُختار.

`-d` / `--dbname`  
قاعدة البيانات التي سيجري الاتصال بها وتشغيل الاستعلام.

`DBNAME` هو اسم قاعدة البيانات. إذا لم يُحدد، فالافتراض هو `USERNAME`.

`-U` / `--username`  
المستخدم الذي سيتصل بقاعدة البيانات.

`USERNAME` هو اسم المستخدم. إذا لم يُحدد، فالافتراض هو مستخدم نظام التشغيل الذي يشغّل `patronictl query`.

`--password`  
المطالبة بكلمة مرور المستخدم المتصل.

بما أن Patroni يستخدم `libpq`، يمكنك بدلًا من ذلك إنشاء ملف `~/.pgpass` أو ضبط متغير البيئة `PGPASSWORD`.

`--format`  
كيفية تنسيق مخرجات الاستعلام.

يمكن أن يكون التنسيق أحد التالي:

- `pretty`: يطبع مخرجات الاستعلام كجدول منسق؛ أو
- `tsv`: يطبع مخرجات الاستعلام معلوماتٍ جدولية مع فصل الأعمدة بـ `\t`؛ أو
- `json`: يطبع مخرجات الاستعلام بصيغة JSON؛ أو
- `yaml`: يطبع مخرجات الاستعلام بصيغة YAML.

الافتراضي هو `tsv`.

`-f` / `--file`  
استخدام ملف مصدرًا للأوامر لتشغيل الاستعلامات.

`FILE_NAME` هو المسار إلى الملف المصدر.

`-c` / `--command`  
تشغيل أمر SQL المعطى في الاستعلام.

`SQL_COMMAND` هو أمر SQL الذي سيُنفَّذ.

`--delimiter`  
الفاصل عند طباعة المعلومات بصيغة `tsv`، أو `\t` إذا حُذف.

`-W`  
إعادة تشغيل الاستعلام تلقائيًا كل ثانيتين.

`-w` / `--watch`  
إعادة تشغيل الاستعلام تلقائيًا بالفاصل الزمني المحدد.

`TIME` هو الفاصل بين إعادات التشغيل، بالثواني.

<a id="patronictl_query_examples"></a>

#### أمثلة {#examples-9}

تشغيل أمر SQL بصفتك المستخدم `postgres`، مع طلب كلمة مروره:

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

تشغيل أمر SQL بصفتك المستخدم `postgres`، وأخذ كلمة المرور من متغير بيئة `libpq`:

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

تشغيل أمر SQL والطباعة بصيغة `pretty` كل ثانيتين:

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

تشغيل أمر SQL على قاعدة البيانات `test` وطباعة المخرجات بصيغة YAML:

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

تشغيل أمر SQL على العضو `postgresql2`:

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

تشغيل أمر SQL على أي من عقد الاستعداد:

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### الصيغة العامة {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### الوصف {#description-10}

يعيد `patronictl reinit` بناء نسخة Postgres الاستعدادية التي يديرها عضو متماثل في عنقود Patroni.

<a id="patronictl_reinit_parameters"></a>

#### المعاملات {#parameters-10}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`MEMBER_NAME`  
اسم العضو المتماثل الذي ستُعاد بناء نسخة Postgres له.

يمكن تحديد عدة أعضاء متماثلين. إذا لم يُحدد أي عضو، لا يفعل الأمر شيئًا.

`--group`  
إعادة بناء عضو متماثل من مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`--wait`  
الانتظار حتى تكتمل إعادة تهيئة عقدة/عقد Postgres الاستعدادية.

`--force`  
علامة لتخطي مطالبات التأكيد عند إعادة بناء نسخ Postgres الاستعدادية.

مفيد للسكربتات.

`--from-leader`  
علامة لأخذ النسخة الأساسية (basebackup) من القائد مباشرة.

<a id="patronictl_reinit_examples"></a>

#### أمثلة {#examples-10}

طلب إعادة بناء جميع الأعضاء المتماثلين في عنقود Patroni مع إعادة التحكم إلى المستدعي فورًا:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

طلب إعادة بناء `postgresql2` والانتظار حتى يكتمل:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

طلب إعادة بناء `postgresql2` وأخذ النسخة الأساسية (basebackup) من القائد مباشرة:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### الصيغة العامة {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### الوصف {#description-11}

يطلب `patronictl reload` إعادة تحميل الإعداد المحلي لعضو واحد أو أكثر من أعضاء Patroni.

كما يشغّل `pg_ctl reload` على نسخة Postgres المُدارة، حتى لو لم يتغير شيء.

<a id="patronictl_reload_parameters"></a>

#### المعاملات {#parameters-11}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`MEMBER_NAME`  
طلب إعادة تحميل الإعداد المحلي لعضو/أعضاء Patroni المعطين.

يمكن تحديد عدة أعضاء. إذا لم يُحدد أي عضو، تُؤخذ جميعها في الحسبان.

`--group`  
طلب إعادة تحميل لأعضاء مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-r` / `--role`  
اختيار الأعضاء الذين لهم الدور المعطى.

يمكن أن يكون الدور أحد التالي:

- `leader`: قائد عنقود Patroni عادي أو عنقود استعداد Patroni؛ أو
- `primary`: قائد عنقود Patroni عادي؛ أو
- `standby-leader`: قائد عنقود استعداد Patroni؛ أو
- `replica`: نسخة متماثلة في عنقود Patroni؛ أو
- `standby`: نفس `replica`؛ أو
- `any`: أي دور. مثل حذف هذا المعامل.

`--force`  
علامة لتخطي مطالبات التأكيد عند طلب إعادة تحميل الإعداد المحلي.

مفيد للسكربتات.

<a id="patronictl_reload_examples"></a>

#### أمثلة {#examples-11}

طلب إعادة تحميل الإعداد المحلي لجميع أعضاء عنقود Patroni:

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### الصيغة العامة {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### الوصف {#description-12}

يزيل `patronictl remove` معلومات العنقود من DCS.

هو إجراء تفاعلي.

> [!WARNING]
> ستدمر هذه العملية معلومات عنقود Patroni من DCS.

<a id="patronictl_remove_parameters"></a>

#### المعاملات {#parameters-12}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`--group`  
إزالة المعلومات المتعلقة بعنقود Patroni لمجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-f` / `--format`  
كيفية تنسيق قائمة الأعضاء في المخرجات عند المطالبة بالتأكيد.

يمكن أن يكون التنسيق أحد التالي:

- `pretty`: يطبع الأعضاء كجدول منسق؛ أو
- `tsv`: يطبع الأعضاء معلوماتٍ جدولية مع فصل الأعمدة بـ `\t`؛ أو
- `json`: يطبع الأعضاء بصيغة JSON؛ أو
- `yaml`: يطبع الأعضاء بصيغة YAML.

الافتراضي هو `pretty`.

<a id="patronictl_remove_examples"></a>

#### أمثلة {#examples-12}

إزالة معلومات عنقود Patroni `batman` من DCS:

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### الصيغة العامة {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### الوصف {#description-13}

يطلب `patronictl restart` إعادة تشغيل نسخة Postgres التي يديرها أحد أعضاء عنقود Patroni.

يمكن تنفيذ إعادة التشغيل فورًا أو جدولتها لوقت لاحق.

<a id="patronictl_restart_parameters"></a>

#### المعاملات {#parameters-13}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`--group`  
إعادة تشغيل عنقود Patroni المتعلق بمجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-r` / `--role`  
اختيار الأعضاء الذين لهم الدور المعطى.

يمكن أن يكون الدور أحد التالي:

- `leader`: قائد عنقود Patroni عادي أو عنقود استعداد Patroni؛ أو
- `primary`: قائد عنقود Patroni عادي؛ أو
- `standby-leader`: قائد عنقود استعداد Patroni؛ أو
- `replica`: نسخة متماثلة في عنقود Patroni؛ أو
- `standby`: نفس `replica`؛ أو
- `any`: أي دور. مثل حذف هذا المعامل.

`--any`  
إعادة تشغيل عقدة عشوائية واحدة من بين العقد التي تطابق المرشِّحات المعطاة.

`--pg-version`  
اختيار الأعضاء فقط الذين تكون نسخة Postgres المُدارة لديهم أقدم من الإصدار المعطى.

`PG_VERSION` هي نسخة Postgres التي ستُقارن بها.

`--pending`  
اختيار الأعضاء الموسومين بـ `Pending restart` فقط.

`--timeout`: إجهاض إعادة التشغيل إذا استغرقت أكثر من المهلة المحددة، وتجاوز الأعطال إلى نسخة متماثلة إذا كانت المشكلة في الأساسي.

`TIMEOUT` هي عدد الثواني للانتظار قبل إجهاض إعادة التشغيل.

`--scheduled`  
جدولة إعادة تشغيل لتقع عند الطابع الزمني المعطى.

`TIMESTAMP` هو الطابع الزمني الذي ينبغي أن تقع عنده إعادة التشغيل. حدده بصيغة غير ملتبسة، ويفضل مع المنطقة الزمنية. يمكنك أيضًا استخدام الكلمة الحرفية `now` لتنفيذ إعادة التشغيل فورًا.

`--force`  
علامة لتخطي مطالبات التأكيد عند طلب عمليات إعادة التشغيل.

مفيد للسكربتات.

<a id="patronictl_restart_examples"></a>

#### أمثلة {#examples-13}

إعادة تشغيل جميع أعضاء العنقود فورًا:

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

إعادة تشغيل عضو عشوائي من العنقود فورًا:

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

جدولة إعادة تشغيل لتقع عند `2023-09-13T18:00-03:00`:

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### الصيغة العامة {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### الوصف {#description-14}

يُخرج `patronictl resume` عنقود Patroni من وضع الصيانة ويعيد تفعيل تجاوز الأعطال التلقائي.

<a id="patronictl_resume_parameters"></a>

#### المعاملات {#parameters-14}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
استئناف مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `citus.group`، إن وُجد.

`--wait`  
الانتظار حتى يُلغى الإيقاف المؤقت عن جميع أعضاء Patroni قبل إعادة التحكم إلى المستدعي.

<a id="patronictl_resume_examples"></a>

#### أمثلة {#examples-14}

إخراج العنقود من وضع الصيانة:

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### الصيغة العامة {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### الوصف {#description-15}

يعرض `patronictl show-config` الإعداد الديناميكي للعنقود المخزَّن في DCS.

<a id="patronictl_show_config_parameters"></a>

#### المعاملات {#parameters-15}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
عرض الإعداد الديناميكي لمجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `citus.group`، إن وُجد.

<a id="patronictl_show_config_examples"></a>

#### أمثلة {#examples-15}

عرض الإعداد الديناميكي للعنقود `batman`:

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### الصيغة العامة {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### الوصف {#description-16}

ينفّذ `patronictl switchover` تبديلًا في العنقود.

صُمم ليُستخدم عندما يكون العنقود سليمًا، مثلًا:

- يوجد قائد؛
- توجد عقد استعداد متزامنة متاحة في عنقود متزامن.

> [!NOTE]
> إذا كان عنقودك غير سليم فقد يهمّك `patronictl failover` بدلًا منه.

<a id="patronictl_switchover_parameters"></a>

#### المعاملات {#parameters-16}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
تنفيذ تبديل في مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`--leader` / `--primary`  
تحديد من هو القائد الذي سيُخفَّض عند وقت التبديل.

`LEADER_NAME` ينبغي أن يطابق اسم القائد الحالي في العنقود.

`--candidate`  
العقدة التي ستُرقَّى عند التبديل وتأخذ الدور الأساسي.

`CANDIDATE_NAME` هو اسم العقدة التي ستُرقَّى.

`--scheduled`  
جدولة تبديل ليقع عند الطابع الزمني المعطى.

`TIMESTAMP` هو الطابع الزمني الذي ينبغي أن يقع عنده التبديل. حدده بصيغة غير ملتبسة، ويفضل مع المنطقة الزمنية. يمكنك أيضًا استخدام الكلمة الحرفية `now` لتنفيذ التبديل فورًا.

`--force`  
علامة لتخطي مطالبات التأكيد عند تنفيذ التبديل.

مفيد للسكربتات.

<a id="patronictl_switchover_examples"></a>

#### أمثلة {#examples-16}

التبديل مع العقدة `postgresql2`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

جدولة تبديل بين `postgresql0` و`postgresql2` ليقع عند `2023-09-13T18:00:00-03:00`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### الصيغة العامة {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### الوصف {#description-17}

يعرض `patronictl topology` معلومات عن عنقود Patroni وأعضائه بأسلوب العرض الشجري.

تُضمَّن المعلومات التالية في المخرجات:

`Cluster`  
اسم عنقود Patroni.

> [!NOTE]
> يظهر في رأس الجدول.

`System identifier`  
معرّف النظام في Postgres.

> [!NOTE]
> يظهر في رأس الجدول.

`Member`  
اسم عضو Patroni.

> [!NOTE]
> تُعرض المعلومات في هذا العمود كعرض شجري للأعضاء من حيث اتصالات النسخ المتماثل.

`Host`  
المضيف الذي يقع فيه العضو.

`Role`  
الدور الحالي للعضو.

يمكن أن يكون أحد ما يلي:

- `Leader`: القائد الحالي لعنقود Patroni عادي؛ أو
- `Standby Leader`: القائد الحالي لعنقود استعداد Patroni؛ أو
- `Sync Standby`: عقدة استعداد متزامنة في عنقود Patroni مع تفعيل الوضع المتزامن؛ أو
- `Replica`: عقدة استعداد عادية في عنقود Patroni.

`State`  
الحالة الحالية لـ Postgres في عضو Patroni.

بعض الأمثلة من الحالات الممكنة:

- `running`: إذا كان Postgres يعمل حاليًا؛
- `streaming`: إذا كانت نسخة متماثلة وكان Postgres يبث حاليًا سجلات WAL من العقدة الأساسية؛
- `in archive recovery`: إذا كانت نسخة متماثلة وكان Postgres يجلب حاليًا سجلات WAL من الأرشيف؛
- `stopped`: إذا كان Postgres قد أُوقف؛
- `crashed`: إذا كان Postgres قد انهار.

`TL`  
الخط الزمني الحالي لـ Postgres في عضو Patroni.

`Receive LSN`  
آخر موقع لسجل الكتابة المسبقة (WAL) استلمه النسخ المتماثل بالبث الخاص بالعضو وزامنه مع القرص (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
تأخر النسخ المتماثل بين موقع `Receive LSN` الخاص بالعضو ومصدره الأعلى (upstream) بوحدة MB.

`Replay LSN`  
آخر موقع لسجل الكتابة المسبقة (WAL) أُعيد تطبيقه أثناء الاستعادة في العضو (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
تأخر النسخ المتماثل بين موقع `Replay LSN` الخاص بالعضو ومصدره الأعلى (upstream) بوحدة MB.

بالإضافة إلى ذلك، قد تُضمَّن المعلومات التالية في المخرجات:

`Group`  
معرّف مجموعة Citus.

> [!NOTE]
> يظهر في رأس الجدول.
>
> يظهر فقط إذا كان عنقود Citus.

`Pending restart`  
تشير العلامة `*` إلى أن العقدة تحتاج إلى إعادة تشغيل كي يدخل بعض إعدادات Postgres حيز التنفيذ. القيمة الفارغة تشير إلى أن العقدة لا تتطلب إعادة تشغيل.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا كانت العقدة تتطلب إعادة تشغيل.

`Scheduled restart`  
الطابع الزمني الذي جُدولت عنده إعادة تشغيل لنسخة Postgres التي يديرها عضو Patroni. القيمة الفارغة تشير إلى عدم وجود إعادة تشغيل مجدولة للعضو.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا كانت للعقدة إعادة تشغيل مجدولة.

`Tags`  
يحتوي على الوسوم المضبوطة لعضو Patroni. القيمة الفارغة تشير إلى أنه إما لم تُضبط أي وسوم، أو أنها ضُبطت بقيم افتراضية.

> [!NOTE]
> يظهر كسمة من سمات العضو.
>
> يظهر إذا كانت للعقدة أي وسوم مخصصة، أو أي وسوم افتراضية بقيم غير افتراضية.

`Scheduled switchover`  
الطابع الزمني الذي جُدول عنده تبديل لعنقود Patroni، إن وُجد.

> [!NOTE]
> يظهر في تذييل الجدول.
>
> يظهر فقط إذا كان هناك تبديل مجدول.

`Maintenance mode`

> إذا كانت مراقبة العنقود متوقفة مؤقتًا حاليًا.
>
> > [!NOTE]
> > يظهر في تذييل الجدول.
> >
> > يظهر فقط إذا كان العنقود في وضع الإيقاف المؤقت.

<a id="patronictl_topology_parameters"></a>

#### المعاملات {#parameters-17}

`CLUSTER_NAME`  
اسم عنقود Patroni.

إذا لم يُحدد، فسيحاول [patronictl](/ar/patroni/patronictl#patronictl) جلبه من إعداد `scope`، إن وُجد.

`--group`  
عرض معلومات عن أعضاء مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

`-W`  
تحديث المعلومات تلقائيًا كل ثانيتين.

`-w` / `--watch`  
تحديث المعلومات تلقائيًا بالفاصل الزمني المحدد.

`TIME` هو الفاصل بين التحديثات، بالثواني.

<a id="patronictl_topology_examples"></a>

#### أمثلة {#examples-17}

عرض طوبولوجيا العنقود `batman` -- حيث تنفّذ `postgresql1` و`postgresql2` النسخ المتماثل من `postgresql0`:

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### الصيغة العامة {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### الوصف {#description-18}

يجلب `patronictl version` إصدار تطبيق [patronictl](/ar/patroni/patronictl#patronictl). بالإضافة إلى ذلك قد يتضمن أيضًا معلومات الإصدار عن عناقيد Patroni وأعضائها.

<a id="patronictl_version_parameters"></a>

#### المعاملات {#parameters-18}

`CLUSTER_NAME`  
اسم عنقود Patroni.

`MEMBER_NAME`  
اسم عضو عنقود Patroni.

`--group`  
اعتبار عنقود Patroni ذي مجموعة Citus المعطاة.

`CITUS_GROUP` هو معرّف مجموعة Citus.

<a id="patronictl_version_examples"></a>

#### أمثلة {#examples-18}

جلب إصدار [patronictl](/ar/patroni/patronictl#patronictl) فقط:

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

جلب إصدار [patronictl](/ar/patroni/patronictl#patronictl) وإصدار جميع أعضاء العنقود `batman`:

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

جلب إصدار [patronictl](/ar/patroni/patronictl#patronictl) وإصدار العضوين `postgresql1` و`postgresql2` من العنقود `batman`:

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
