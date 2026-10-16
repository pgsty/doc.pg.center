---
title: "إعدادات تهيئة YAML"
linkTitle: "تهيئة YAML"
weight: 20
icon: fa-solid fa-code
description: "مرجع كامل لخيارات وأقسام إعداد Patroni بصيغة YAML."
module: [PATRONI]
categories: [مرجع]
upstream_link: "https://patroni.readthedocs.io/en/latest/yaml_configuration.html"
---

<a id="yaml"></a>

--------

## عام/شامل {#globaluniversal}

- **thread_pool_size**: حجم تجمع الخيوط الذي يستخدمه Patroni لتنفيذ المهام غير المتزامنة والتواصل عبر REST API مع الأعضاء الآخرين أثناء سباق القيادة أو فحوصات الفشل الآمن. القيمة الدنيا هي `5`، والقيمة الافتراضية هي `5`.
- **thread_stack_size**: يحدد حجم المكدس المستخدم للخيوط التي يبدأها Patroni. يجب أن تكون القيمة بمحاذاة `64kB`. القيمة الدنيا هي `64kB`، والقيمة الافتراضية (التي يضبطها Patroni) هي `512kB`.
- **name**: اسم المضيف. يجب أن يكون فريدًا للعنقود.
- **namespace**: المسار داخل مخزن التهيئة حيث سيحتفظ Patroni بمعلومات عن العنقود. القيمة الافتراضية: "/service"
- **scope**: اسم العنقود

<a id="log_settings"></a>

--------

## السجل {#log}

- **type**: يضبط صيغة السجلات. يمكن أن تكون إما **plain** أو **json**. لاستخدام صيغة **json**، يجب أن يكون لديك [jsonlogger](/ar/patroni/installation#extras) مثبتًا. القيمة الافتراضية هي **plain**.
- **level**: يضبط مستوى التسجيل العام. القيمة الافتراضية هي **INFO** (راجع [وثائق التسجيل للغة Python](https://docs.python.org/3.6/library/logging.html#levels))
- **traceback_level**: يضبط المستوى الذي ستكون التتبعات العكسية (tracebacks) مرئية عنده. القيمة الافتراضية هي **ERROR**. اضبطه على **DEBUG** إذا أردت رؤية التتبعات العكسية فقط عند تمكين **log.level=DEBUG**.
- **format**: يضبط سلسلة تنسيق السجل. إذا كان نوع السجل **plain**، فيجب أن يكون تنسيق السجل سلسلة. راجع [سمات LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) للسمات المتاحة. إذا كان نوع السجل **json**، فيمكن أن يكون تنسيق السجل قائمة بالإضافة إلى سلسلة. يجب أن يقابل كل عنصر في القائمة سمات LogRecord. كن حذرًا من أن اسم الحقل فقط هو المطلوب، وأنه يجب حذف **%(** و**)**. إذا رغبت في طباعة حقل سجل باسم مفتاح مختلف، فاستخدم قاموسًا يكون مفتاح القاموس فيه هو حقل السجل، والقيمة هي اسم الحقل الذي تريد طباعته في السجل. القيمة الافتراضية هي **%(asctime)s %(levelname)s: %(message)s**
- **dateformat**: يضبط سلسلة تنسيق التاريخ والوقت. (راجع [وثائق formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **static_fields**: يضيف حقولًا إضافية إلى السجل. هذا الخيار متاح فقط عند ضبط نوع السجل على **json**.
- **max_queue_size**: يستخدم Patroni تسجيلًا على مرحلتين. تُكتب سجلات التسجيل في قائمة انتظار في الذاكرة وهناك خيط منفصل يسحبها من قائمة الانتظار ويكتبها إلى stderr أو إلى ملف. حجم قائمة الانتظار الداخلية محدود افتراضيًا بـ **1000** سجل، وهو ما يكفي للاحتفاظ بسجلات المدة 1h20m الماضية.
- **dir**: الدليل الذي تُكتب إليه سجلات التطبيق. يجب أن يكون الدليل موجودًا وقابلًا للكتابة من قبل المستخدم الذي ينفذ Patroni. إذا ضبطت هذه القيمة، فسيحتفظ التطبيق افتراضيًا بـ 4 سجلات بحجم 25MB. يمكنك ضبط قيم الاحتفاظ تلك باستخدام `file_num` و`file_size` (انظر أدناه).
- **mode**: صلاحيات ملفات السجل (مثلًا، `0644`). إذا لم تُحدد، فستُضبط الصلاحيات بناءً على قيمة umask الحالية.
- **file_num**: عدد سجلات التطبيق التي يُحتفظ بها.
- **file_size**: حجم ملف patroni.log (بالبايتات) الذي يشغّل تدوير السجل.
- **loggers**: يتيح هذا القسم إعادة تعريف مستوى التسجيل لكل وحدة python
  - **patroni.postmaster: WARNING**
  - **urllib3: DEBUG**
- **deduplicate_heartbeat_logs**: إذا ضُبط على `true`، فلن تُخرج سجلات نبض القلب المتتالية المتطابقة. القيمة الافتراضية هي `false`.

> [!WARNING]
> يمكن أن يكون وقت تنفيذ حلقة HA معلومة قيمة جدًا في تشخيص تجاوزات الأعطال الناتجة عن استنزاف الموارد والمشكلات المشابهة. عندما يُضبط `deduplicate_heartbeat_logs` على `true` فلن يُولَّد أي سجل لتنفيذ حلقة HA (إلا إذا تغير القائد)، وبالتالي فلن تتوفر هذه المعلومة المفيدة المحتملة من السجلات.

إليك مثال على كيفية ضبط patroni للتسجيل بصيغة json.

```yaml
log:
   type: json
   format:
      - message
      - module
      - asctime: '@timestamp'
      - levelname: level
   static_fields:
      app: patroni
```

<a id="bootstrap_settings"></a>

--------

## تهيئة بدء التشغيل (Bootstrap) {#bootstrap-configuration}

> [!NOTE]
> بعد أن يقوم Patroni بتهيئة العنقود لأول مرة وتخزين الإعدادات في DCS، لن يكون لأي تغييرات مستقبلية على قسم `bootstrap.dcs` من تهيئة YAML أي تأثير! إذا أردت تغييرها فيرجى استخدام إما [patronictl_edit_config](/ar/patroni/patronictl#patronictl_edit_config) أو [REST API](/ar/patroni/rest_api#rest_api) في Patroni.

- **bootstrap**:
  - **dcs**: سيُكتب هذا القسم في `/<namespace>/<scope>/config` لمخزن التهيئة المعني بعد تهيئة العنقود الجديد. التهيئة الديناميكية العامة للعنقود. يمكنك وضع أي من المعاملات الموصوفة في [إعدادات التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) تحت `bootstrap.dcs` وبعد أن يقوم Patroni بتهيئة (bootstrapping) العنقود الجديد، سيكتب هذا القسم في `/<namespace>/<scope>/config` لمخزن التهيئة.

  - **method**: سكربت مخصص لاستخدامه في بدء تهيئة هذا العنقود.

    راجع [وثائق أساليب بدء التهيئة المخصصة](/ar/patroni/replica_bootstrap#custom_bootstrap) للتفاصيل. عند تحديد `initdb` يُرجع إلى أمر `initdb` الافتراضي. يُفعَّل `initdb` أيضًا عند عدم وجود معامل `method` في ملف التهيئة.

  - **initdb**: (اختياري) قائمة الخيارات التي ستمرر إلى initdb.

    - **- data-checksums**: يجب تمكينه عند الحاجة إلى pg_rewind على 9.3.
    - **- encoding: UTF8**: الترميز الافتراضي لقواعد البيانات الجديدة.
    - **- locale: UTF8**: الإعدادات المحلية (locale) الافتراضية لقواعد البيانات الجديدة.

  - **post_bootstrap** أو **post_init**: سكربت إضافي سيُنفَّذ بعد تهيئة العنقود. يتلقى السكربت سلسلة URL اتصال (مع المستخدم الفائق للعنقود كاسم مستخدم). يُضبط متغير PGPASSFILE على موقع ملف pgpass.

<a id="citus_settings"></a>

--------

## Citus {#citus}

يفعّل تكامل Patroni مع [Citus](https://docs.citusdata.com). إذا ضُبط، فسيهتم Patroni بتسجيل عقد Citus العاملة على المنسق. يمكنك العثور على مزيد من المعلومات حول دعم Citus [هنا](/ar/patroni/citus#citus).

- **group**: معرف مجموعة Citus، عدد صحيح. استخدم `0` للمنسق و`1`، `2`، إلخ... للعقد العاملة
- **database**: قاعدة البيانات التي ينبغي إنشاء امتداد [citus](/ar/patroni/citus#citus) فيها. يجب أن تكون نفسها على المنسق وجميع العقد العاملة. حاليًا يُدعم قاعدة بيانات واحدة فقط.

<a id="consul_settings"></a>

--------

## Consul {#consul}

معظم المعاملات اختيارية، لكن عليك تحديد واحدًا من **host** أو **url**

- **host**: host:port لوكيل Consul المحلي.
- **url**: عنوان url لوكيل Consul المحلي، بالصيغة: http(s)://host:port.
- **port**: (اختياري) منفذ Consul.
- **scheme**: (اختياري) **http** أو **https**، الافتراضي هو **http**.
- **token**: (اختياري) رمز ACL.
- **verify**: (اختياري) ما إذا كان سيُتحقق من شهادة SSL لطلبات HTTPS.
- **cacert**: (اختياري) شهادة المرجع (ca). إذا وُجدت فستُمكِّن التحقق.
- **cert**: (اختياري) ملف شهادة العميل.
- **key**: (اختياري) ملف مفتاح العميل. يمكن أن يكون فارغًا إذا كان المفتاح جزءًا من **cert**.
- **dc**: (اختياري) مركز البيانات الذي سيتم التواصل معه. افتراضيًا يُستخدم مركز بيانات المضيف.
- **consistency**: (اختياري) اختر وضع الاتساق لـ consul. القيم الممكنة هي `default` أو `consistent` أو `stale` (مزيد من التفاصيل في [مرجع consul API](https://www.consul.io/api/features/consistency.html/))
- **checks**: (اختياري) قائمة فحوصات صحة Consul المستخدمة للجلسة. افتراضيًا تُستخدم قائمة فارغة.
- **register_service**: (اختياري) ما إذا كان ستُسجَّل خدمة بالاسم الذي يحدده المعامل scope وبالوسم master أو primary أو replica أو standby-leader بحسب دور العقدة. الافتراضي هو **false**.
- **service_tags**: (اختياري) وسوم ثابتة إضافية تُضاف إلى خدمة Consul فضلًا عن الدور (`primary`/`replica`/`standby-leader`). افتراضيًا تُستخدم قائمة فارغة.
- **service_check_interval**: (اختياري) كم مرة يُنفَّذ فحص الصحة مقابل url المسجل. الافتراضي هو '5s'.
- **service_check_tls_server_name**: (اختياري) تجاوز مضيف SNI عند الاتصال عبر TLS، راجع أيضًا [مرجع واجهة consul agent check API](https://www.consul.io/api-docs/agent/check#tlsservername).

يحتاج `token` إلى صلاحيات ACL التالية:

    service_prefix "${scope}" {
        policy = "write"
    }
    key_prefix "${namespace}/${scope}" {
        policy = "write"
    }
    session_prefix "" {
        policy = "write"
    }

--------

## Etcd {#etcd}

معظم المعاملات اختيارية، لكن عليك تحديد واحدًا من **host** أو **hosts** أو **url** أو **proxy** أو **srv**

- **host**: host:port لنقطة نهاية etcd.
- **hosts**: قائمة نقاط نهاية etcd بالصيغة host1:port1,host2:port2,etc... يمكن أن تكون سلسلة مفصولة بفواصل أو قائمة yaml فعلية.
- **use_proxies**: إذا ضُبط هذا المعامل على true، فسيعتبر Patroni **hosts** قائمة وسطاء ولن ينفذ اكتشاف طبولوجيا عنقود etcd.
- **url**: عنوان url الخاص بـ etcd.
- **proxy**: عنوان url للوسيط الخاص بـ etcd. إذا كنت تتصل بـ etcd عبر وسيط، فاستخدم هذا المعامل بدلًا من **url**.
- **srv**: النطاق للبحث عن سجلات SRV للاكتشاف التلقائي للعنقود. سيحاول Patroni الاستعلام عن أسماء خدمات SRV هذه للنطاق المحدد (بهذا الترتيب حتى أول نجاح): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. إذا استُرجعت سجلات SRV لـ `_etcd-server-ssl` أو `_etcd-server` فسيُستخدم بروتوكول ETCD peer للاستعلام عن ETCD عن الأعضاء المتاحين. وإلا فسيُستخدم المضيفون من سجلات SRV.
- **srv_suffix**: يضبط لاحقة لاسم SRV الذي يُستعلم عنه أثناء الاكتشاف. استخدم هذا الخيار للتمييز بين عناقيد etcd متعددة تحت النطاق نفسه. يعمل فقط بالاقتران مع **srv**. مثلًا، إذا ضُبط `srv_suffix: foo` و`srv: example.org`، فسيُنفذ استعلام DNS SRV التالي:`_etcd-client-ssl-foo._tcp.example.org` (وهكذا لكل أسماء خدمات ETCD SRV الممكنة).
- **protocol**: (اختياري) http أو https، وإذا لم يُحدد فتُستخدم http. إذا حُدد **url** أو **proxy** - فسيأخذ البروتوكول منهما.
- **username**: (اختياري) اسم المستخدم لمصادقة etcd.
- **password**: (اختياري) كلمة المرور لمصادقة etcd.
- **cacert**: (اختياري) شهادة المرجع (ca). إذا وُجدت فستُمكِّن التحقق.
- **cert**: (اختياري) ملف شهادة العميل.
- **key**: (اختياري) ملف مفتاح العميل. يمكن أن يكون فارغًا إذا كان المفتاح جزءًا من **cert**.

--------

## Etcdv3 {#etcdv3}

إذا أردت أن يعمل Patroni مع عنقود Etcd عبر إصدار البروتوكول 3، فعليك استخدام قسم `etcd3` في ملف تهيئة Patroni. جميع معاملات التهيئة هي نفسها كما هي لـ `etcd`.

> [!WARNING]
> المفاتيح التي أُنشئت بإصدار البروتوكول 2 غير مرئية بإصدار البروتوكول 3 والعكس صحيح، لذلك لا يمكن الانتقال من `etcd` إلى `etcd3` بمجرد تحديث ملف تهيئة Patroni. بالإضافة إلى ذلك، يستخدم Patroni بوابة gRPC-gateway (الوسيط) الخاصة بـ Etcd للتواصل مع V3 API، ما يعني أن مصادقة الاسم الشائع (common name) لـ TLS غير ممكنة.

--------

## ZooKeeper {#zookeeper}

- **hosts**: قائمة أعضاء عنقود ZooKeeper بالصيغة: \['host1:port1', 'host2:port2', 'etc...'\].
- **use_ssl**: (اختياري) ما إذا كان يُستخدم SSL أم لا. الافتراضي هو `false`. إذا ضُبط على `false`، فتُتجاهل جميع المعاملات الخاصة بـ SSL.
- **cacert**: (اختياري) شهادة المرجع (CA). إذا وُجدت فستُمكِّن التحقق.
- **cert**: (اختياري) ملف شهادة العميل.
- **key**: (اختياري) ملف مفتاح العميل.
- **key_password**: (اختياري) كلمة مرور مفتاح العميل.
- **verify**: (اختياري) ما إذا كان سيُتحقق من الشهادة أم لا. الافتراضي هو `true`.
- **set_acls**: (اختياري) إذا ضُبط، فسيُضبط Kazoo لتطبيق ACL افتراضي على كل ZNode ينشئه. يمكن أن تستخدم ACLs إما مخطط `x509` (الافتراضي) أو مخططات ZooKeeper الأخرى المدعومة مثل `digest`. يجب تحديدها كقاموس يكون المفتاح فيه هو الاسم الرئيسي الكامل (مع بادئة المخطط اختياريًا) والقيمة قائمة بالصلاحيات. يمكن أن تكون الصلاحيات واحدة أو أكثر من `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN`, أو `ALL`. مثلًا، `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **auth_data**: (اختياري) بيانات اعتماد المصادقة المستخدمة للاتصال. يجب أن تكون قاموسًا بالشكل الذي يكون فيه `scheme` هو المفتاح و`credential` هو القيمة. الافتراضي قاموس فارغ.

> [!NOTE]
> يلزم تثبيت `kazoo>=2.6.0` لدعم SSL.

--------

## Exhibitor {#exhibitor}

- **hosts**: القائمة الأولية لعقد Exhibitor (ZooKeeper) بالصيغة: 'host1,host2,etc...'. تُحدَّث هذه القائمة تلقائيًا كلما تغيرت طبولوجيا عنقود Exhibitor (ZooKeeper).
- **poll_interval**: كم مرة ينبغي تحديث قائمة عقد ZooKeeper وExhibitor من Exhibitor.
- **port**: منفذ Exhibitor.

<a id="kubernetes_settings"></a>

--------

## Kubernetes {#kubernetes}

- **bypass_api_service**: (اختياري) عند التواصل مع واجهة Kubernetes API، يعتمد Patroni عادةً على خدمة [kubernetes](/ar/patroni/kubernetes#kubernetes)، التي يُكشف عنوانها في الـ pods عبر متغير البيئة `KUBERNETES_SERVICE_HOST`. إذا ضُبط `bypass_api_service` على `true`، فسيحل Patroni قائمة عقد API الكامنة خلف الخدمة ويتصل بها مباشرة.
- **namespace**: (اختياري) فضاء الأسماء في Kubernetes حيث يعمل pod الخاص بـ Patroni. القيمة الافتراضية هي `default`.
- **labels**: تسميات بالصيغة `{label1: value1, label2: value2}`. ستُستخدم هذه التسميات للعثور على الكائنات الموجودة (Pods وإما Endpoints أو ConfigMaps) المرتبطة بالعنقود الحالي. كما سيضعها Patroni على كل كائن (Endpoint أو ConfigMap) ينشئه.
- **scope_label**: (اختياري) اسم التسمية التي تحتوي على اسم العنقود. القيمة الافتراضية هي `cluster-name`.
- **bootstrap_labels**: (اختياري) تسميات بالصيغة `{label1: value1, label2: value2}`. ستُخصص هذه التسميات لـ pod الخاص بـ Patroni عندما تكون حالته إما `initializing new cluster` أو `running custom bootstrap script` أو `starting after custom bootstrap` أو `creating replica`.
- **role_label**: (اختياري) اسم التسمية التي تحتوي على الدور (`primary` أو `replica` أو قيمة مخصصة أخرى). سيضبط Patroni هذه التسمية على الـ pod الذي يعمل فيه. القيمة الافتراضية هي `role`.
- **leader_label_value**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `primary`. القيمة الافتراضية هي `primary`.
- **follower_label_value**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `replica`. القيمة الافتراضية هي `replica`.
- **standby_leader_label_value**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `standby_leader`. القيمة الافتراضية هي `primary`.
- **tmp_role_label**: (اختياري) اسم التسمية المؤقتة التي تحتوي على الدور (`primary` أو `replica`). ستستخدم قيمة هذه التسمية دائمًا القيمة الافتراضية للدور المقابل. لا تضبطها إلا عند الضرورة.
- **use_endpoints**: (اختياري) إذا ضُبط على true، فسيستخدم Patroni Endpoints بدلًا من ConfigMaps لإجراء انتخابات القائد والاحتفاظ بحالة العنقود.
- **pod_ip**: (اختياري) عنوان IP للـ pod الذي يعمل فيه Patroni. هذه القيمة مطلوبة عند تمكين `use_endpoints` وتُستخدم لتعبئة مجموعات نقطة نهاية القائد عند ترقية PostgreSQL الخاص بالـ pod.
- **ports**: (اختياري) إذا كان كائن Service يحمل اسمًا للمنفذ، فيجب أن يظهر الاسم نفسه في كائن Endpoint، وإلا فلن تعمل الخدمة. مثلًا، إذا كانت خدمتك معرفة كـ `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`، فعليك ضبط `kubernetes.ports: [{"name": "postgresql", "port": 5432}]` وسيستخدمه Patroni لتحديث مجموعات نقطة نهاية القائد Endpoint. يُستخدم هذا المعامل فقط إذا ضُبط `kubernetes.use_endpoints`.
- **cacert**: (اختياري) يحدد الملف الذي يحتوي CA_BUNDLE بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات SSL لواجهة Kubernetes API. إذا لم يُقدم، فسيستخدم patroni القيمة التي يوفرها سر ServiceAccount.
- **retriable_http_codes**: (اختياري) قائمة رموز حالة HTTP من واجهة K8s API التي يُعاد المحاولة عندها. افتراضيًا يعيد Patroni المحاولة عند `500` و`503` و`504`، أو إذا كانت استجابة K8s API تحمل ترويسة HTTP `retry-after`.

<a id="raft_settings"></a>

--------

## Raft (مهمل) {#raft-deprecated}

- **self_addr**: `ip:port` للاستماع لاتصالات Raft. يجب أن يكون `self_addr` متاحًا من العقد الأخرى للعنقود. إذا لم يُضبط، فلن تشارك العقدة في التوافق (consensus).

- **bind_addr**: (اختياري) `ip:port` للاستماع لاتصالات Raft. إذا لم يُحدد فسيُستخدم `self_addr`.

- **partner_addrs**: قائمة عقد Patroni الأخرى في العنقود بالصيغة: \['ip1:port', 'ip2:port', 'etc...'\]

- **data_dir**: الدليل الذي يُخزن فيه سجل Raft واللقطة (snapshot). إذا لم يُحدد فسيُستخدم دليل العمل الحالي.

- **password**: (اختياري) تشفير حركة مرور Raft بكلمة مرور محددة، يتطلب وحدة `cryptography` للغة python.
- **min_timeout**: (اختياري) الحد الأدنى لمهلة الانتخابات بالثواني لتنفيذ pysyncobj Raft الأساسي. يجب أن يكون أكبر من 3 * `append_entries_period`. الافتراضي: `0.4`.
- **max_timeout**: (اختياري) الحد الأقصى لمهلة الانتخابات بالثواني لتنفيذ pysyncobj Raft الأساسي. يجب أن يكون أكبر من `min_timeout`. الافتراضي: `1.4`.
- **connection_timeout**: (اختياري) الوقت بالثواني الذي يُعد بعده اتصال لم تُستقبل فيه بيانات ميّتًا. يجب أن يكون أكبر من أو يساوي `max_timeout`. الافتراضي: `3.5`.
- **append_entries_period**: (اختياري) الفاصل الزمني بالثواني لإرسال أوامر نبض القلب (append_entries). يجب أن يكون أقل من ثلث `min_timeout`. الافتراضي: `0.1`.
- **connection_retry_time**: (اختياري) الفاصل الزمني بالثواني بين محاولات إعادة الاتصال بالعقد غير المتصلة. الافتراضي: `5.0`.
- **leader_fallback_timeout**: (اختياري) الوقت بالثواني الذي يتراجع بعده قائد بلا استجابة من الأغلبية إلى حالة التابع. يجب أن يكون أكبر من `append_entries_period`. الافتراضي: `30.0`.

> [!NOTE]
> معاملات المهلة هذه مفيدة للشبكات عالية زمن الاستجابة حيث تكون مهلات pysyncobj الافتراضية عدوانية للغاية. يجب استيفاء القيود التالية: `min_timeout` > 3 * `append_entries_period`، و`max_timeout` > `min_timeout`، و`connection_timeout` >= `max_timeout`، و`leader_fallback_timeout` > `append_entries_period`. يتحقق Patroni منها عند بدء التشغيل وسيرفض البدء إذا كانت منتهكة. لا يمكن تغيير هذه القيم في وقت التشغيل وتتطلب إعادة تشغيل.
>
> [!WARNING]
> تخفف هذه الأدوات فقط مهلات انتخاب واتصال pysyncobj؛ فهي لا تمد الموعد النهائي لكل أمر يطبقه Patroni على عمليات Raft. يجب أن يكتمل كل أمر Raft (تحديث قفل القائد، كتابة حالة العنقود) ضمن `retry_timeout` (الافتراضي `10`) مع ذلك. على الوصلات عالية زمن الاستجابة جدًا - أي فوق بضع ثوانٍ من زمن الذهاب والإياب تقريبًا - يمكن لأمر واحد أن يتجاوز `retry_timeout` حتى عندما تُرفع `connection_timeout` بما يتجاوز RTT بكثير، ولذلك سيبدو DCS غير متاح وقد تُخفَّض العقدة الرئيسية. على مثل هذه الوصلات عليك أيضًا رفع `retry_timeout` و`ttl` وفقًا لذلك، مع الحفاظ على `loop_wait + 2 * retry_timeout <= ttl`.

  أسئلة وأجوبة قصيرة حول تنفيذ Raft

  - س: كيف أعرض جميع العقد التي توفر التوافق (consensus)؟

    ج: `syncobj_admin -conn host:port -status` حيث يكون host:port عنوان إحدى عقد العنقود

  - س: عقدة كانت جزءًا من التوافق وقد اختفت ولا يمكنني إعادة استخدام IP نفسه لعقدة أخرى. كيف أزيل هذه العقدة من التوافق؟

    ج: `syncobj_admin -conn host:port -remove host2:port2` حيث يكون `host2:port2` عنوان العقدة التي تريد إزالتها من التوافق.

  - س: من أين أحصل على أداة `syncobj_admin`؟

    ج: تُثبَّت مع وحدة `pysyncobj` (تنفيذ RAFT بلغة python)، وهي تبعية لـ Patroni.

  - س: هل من الممكن تشغيل عقدة Patroni دون إضافتها إلى التوافق؟

    ج: نعم، فقط علّق أو أزل `raft.self_addr` من تهيئة Patroni.

  - س: هل من الممكن تشغيل Patroni وPostgreSQL على عقدتين فقط؟

    ج: نعم، على العقدة الثالثة يمكنك تشغيل `patroni_raft_controller` (دون Patroni وPostgreSQL). في مثل هذا الإعداد، يمكن فقدان عقدة واحدة مؤقتًا دون التأثير على العقدة الرئيسية.

<a id="postgresql_settings"></a>

--------

## PostgreSQL {#postgresql}

- **postgresql**:
  - **authentication**:

    - **superuser**:
      - **username**: اسم المستخدم الفائق، يُضبط أثناء التهيئة الأولية (initdb) ويستخدمه Patroni لاحقًا للاتصال بـ postgres.
      - **password**: كلمة مرور المستخدم الفائق، تُضبط أثناء التهيئة الأولية (initdb).
      - **sslmode**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
      - **sslkey**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
      - **sslpassword**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `sslkey`.
      - **sslcert**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
      - **sslrootcert**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
      - **sslcrl**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslcrldir**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslnegotiation**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
      - **gssencmode**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
      - **channel_binding**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).
    - **replication**:
      - **username**: اسم مستخدم النسخ المتماثل؛ سيُنشأ المستخدم أثناء التهيئة الأولية. ستستخدم النسخ المتماثلة هذا المستخدم للوصول إلى مصدر النسخ المتماثل عبر النسخ المتماثل الانسيابي
      - **password**: كلمة مرور النسخ المتماثل؛ سيُنشأ المستخدم أثناء التهيئة الأولية.
      - **sslmode**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
      - **sslkey**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
      - **sslpassword**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `sslkey`.
      - **sslcert**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
      - **sslrootcert**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
      - **sslcrl**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslcrldir**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslnegotiation**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
      - **gssencmode**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
      - **channel_binding**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).
    - **rewind**:
      - **username**: (اختياري) اسم المستخدم لـ `pg_rewind`؛ سيُنشأ المستخدم أثناء تهيئة postgres 11+ وستُمنح جميع [الصلاحيات](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) اللازمة.
      - **password**: (اختياري) كلمة مرور المستخدم لـ `pg_rewind`؛ سيُنشأ المستخدم أثناء التهيئة الأولية.
      - **sslmode**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
      - **sslkey**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
      - **sslpassword**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `sslkey`.
      - **sslcert**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
      - **sslrootcert**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
      - **sslcrl**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslcrldir**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
      - **sslnegotiation**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
      - **gssencmode**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
      - **channel_binding**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).

  - **callbacks**: سكربتات الاستدعاء (callback) التي تُشغَّل عند أفعال معينة. سيمرر Patroni الفعل والدور واسم العنقود. (راجع scripts/aws.py كمثال على كيفية كتابتها.)

    - **on_reload**: شغّل هذا السكربت عند تشغيل إعادة تحميل التهيئة.
    - **on_restart**: شغّل هذا السكربت عند إعادة تشغيل postgres (دون تغيير الدور).
    - **on_role_change**: شغّل هذا السكربت عند ترقية postgres أو تخفيضه.
    - **on_start**: شغّل هذا السكربت عند بدء postgres.
    - **on_stop**: شغّل هذا السكربت عند إيقاف postgres.

  - **connect_address**: عنوان IP + المنفذ الذي يمكن الوصول إلى Postgres من خلاله من العقد والتطبيقات الأخرى.

  - **proxy_address**: عنوان IP + المنفذ الذي يمكن الوصول من خلاله إلى مجمّع اتصالات (مثل pgbouncer) يعمل بجوار Postgres. تُكتب القيمة في مفتاح العضو في DCS كـ `proxy_url` ويمكن أن تكون مستخدمة/مفيدة لاكتشاف الخدمات.

  - **create_replica_methods**: قائمة مرتبة بأساليب الإنشاء لتحويل عقدة Patroni إلى نسخة متماثلة جديدة. "basebackup" هو الأسلوب الافتراضي؛ ويُفترض أن تشير الأساليب الأخرى إلى سكربتات، كل منها يُضبط كبند تهيئة مستقل. راجع [وثائق أساليب إنشاء النسخ المتماثلة المخصصة](/ar/patroni/replica_bootstrap#custom_replica_creation) لمزيد من الشرح.

  - **data_dir**: موقع دليل بيانات Postgres، إما [موجود](/ar/patroni/existing_data#existing_data) أو ليقوم Patroni بتهيئته.

  - **config_dir**: موقع دليل تهيئة Postgres، الافتراضي هو دليل البيانات. يجب أن يكون قابلًا للكتابة من Patroni.

  - **bin_dir**: (اختياري) المسار إلى ملفات PostgreSQL الثنائية (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind). إذا لم يُقدم أو كان سلسلة فارغة، فسيُستخدم متغير البيئة PATH للعثور على الملفات التنفيذية.

  - **bin_name**: (اختياري) يجعل من الممكن تجاوز أسماء ملفات Postgres الثنائية، إذا كنت تستخدم توزيعة Postgres مخصصة:

    - **pg_ctl**: (اختياري) اسم مخصص للملف الثنائي `pg_ctl`.
    - **initdb**: (اختياري) اسم مخصص للملف الثنائي `initdb`.
    - **pg_controldata**: (اختياري) اسم مخصص للملف الثنائي `pg_controldata`.
    - **pg_basebackup**: (اختياري) اسم مخصص للملف الثنائي `pg_basebackup`.
    - **postgres**: (اختياري) اسم مخصص للملف الثنائي `postgres`.
    - **pg_isready**: (اختياري) اسم مخصص للملف الثنائي `pg_isready`.
    - **pg_rewind**: (اختياري) اسم مخصص للملف الثنائي `pg_rewind`.

  - **listen**: عنوان IP + المنفذ الذي يستمع إليه Postgres؛ يجب أن يكون متاحًا من العقد الأخرى في العنقود، إذا كنت تستخدم النسخ المتماثل الانسيابي. يُسمح بعناوين متعددة مفصولة بفواصل، طالما أن مكوّن المنفذ يُلحق بعد الأخير منها بنقطتين، أي `listen: 127.0.0.1,127.0.0.2:5432`. سيستخدم Patroni أول عنوان من هذه القائمة لتأسيس اتصالات محلية بعقدة PostgreSQL.

  - **use_unix_socket**: يحدد أن يفضل Patroni استخدام مقابس unix للاتصال بالعنقود. القيمة الافتراضية هي `false`. إذا عُرِّف `unix_socket_directories`، فسيستخدم Patroni أول قيمة مناسبة منه للاتصال بالعنقود والرجوع إلى tcp إذا لم يكن هناك ما يناسب. إذا لم يُحدد `unix_socket_directories` في `postgresql.parameters`، فسيفترض Patroni أنه يجب استخدام القيمة الافتراضية وسيتجاهل `host` من معاملات الاتصال.

  - **use_unix_socket_repl**: يحدد أن يفضل Patroni استخدام مقابس unix لاتصال العنقود بمستخدم النسخ المتماثل. القيمة الافتراضية هي `false`. إذا عُرِّف `unix_socket_directories`، فسيستخدم Patroni أول قيمة مناسبة منه للاتصال بالعنقود والرجوع إلى tcp إذا لم يكن هناك ما يناسب. إذا لم يُحدد `unix_socket_directories` في `postgresql.parameters`، فسيفترض Patroni أنه يجب استخدام القيمة الافتراضية وسيتجاهل `host` من معاملات الاتصال.

  - **pgpass**: المسار إلى ملف كلمات المرور [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). ينشئ Patroni هذا الملف قبل تنفيذ pg_basebackup وسكربت post_init وفي بعض الظروف الأخرى. يجب أن يكون الموقع قابلًا للكتابة من Patroni.

  - **recovery_conf**: إعدادات تهيئة إضافية تُكتب إلى recovery.conf عند تهيئة التابع.

  - **custom_conf** : المسار إلى ملف `postgresql.conf` مخصص اختياري، سيُستخدم بدلًا من `postgresql.base.conf`. يجب أن يكون الملف موجودًا على جميع عقد العنقود، وقابلًا للقراءة من PostgreSQL، وسيُضمَّن من موقعه في `postgresql.conf` الفعلي. لاحظ أن Patroni لن يراقب هذا الملف للتغييرات، ولن يأخذ نسخة احتياطية منه. مع ذلك، لا يزال من الممكن تجاوز إعداداته بمرافق تهيئة Patroni نفسها - راجع [التهيئة الديناميكية](/ar/patroni/config#config) للتفاصيل.

  - **parameters**: معاملات تهيئة (GUCs) لـ Postgres بالصيغة `{ssl: "on", ssl_cert_file: "cert_file"}`.
  - **parameters_primary**: (اختياري) تجاوزات معاملات خاصة بالدور للعقدة الرئيسية. تُدمج هذه القيم مع **parameters** الأساسية وتتجاوزها.
  - **parameters_replica**: (اختياري) تجاوزات معاملات خاصة بالدور للنسخة المتماثلة. تُدمج هذه القيم مع **parameters** الأساسية وتتجاوزها.
  - **parameters_standby_leader**: (اختياري) تجاوزات معاملات خاصة بالدور لقائد الاستعداد (standby_leader). تُدمج هذه القيم مع **parameters** الأساسية وتتجاوزها.

  - **pg_hba**: قائمة الأسطر التي سيستخدمها Patroni لتوليد `pg_hba.conf`. يتجاهل Patroni هذا المعامل إذا ضُبط معامل PostgreSQL `hba_file` على قيمة غير افتراضية. مع [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) يبسط هذا المعامل إدارة `pg_hba.conf`.

    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: يلزم سطر مثل هذا للنسخ المتماثل.
  - **pg_hba_primary**: (اختياري) مدخلات pg_hba خاصة بالدور للعقدة الرئيسية. تستبدل هذه **pg_hba** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_hba**.
  - **pg_hba_replica**: (اختياري) مدخلات pg_hba خاصة بالدور للنسخة المتماثلة. تستبدل هذه **pg_hba** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_hba**.
  - **pg_hba_standby_leader**: (اختياري) مدخلات pg_hba خاصة بالدور لقائد الاستعداد (standby_leader). تستبدل هذه **pg_hba** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_hba**.

  - **pg_ident**: قائمة الأسطر التي سيستخدمها Patroni لتوليد `pg_ident.conf`. يتجاهل Patroni هذا المعامل إذا ضُبط معامل PostgreSQL `ident_file` على قيمة غير افتراضية. مع [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) يبسط هذا المعامل إدارة `pg_ident.conf`.

    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (اختياري) مدخلات pg_ident خاصة بالدور للعقدة الرئيسية. تستبدل هذه **pg_ident** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_ident**.
  - **pg_ident_replica**: (اختياري) مدخلات pg_ident خاصة بالدور للنسخة المتماثلة. تستبدل هذه **pg_ident** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_ident**.
  - **pg_ident_standby_leader**: (اختياري) مدخلات pg_ident خاصة بالدور لقائد الاستعداد (standby_leader). تستبدل هذه **pg_ident** بالكامل (دون دمج). إذا لم تُعرَّف، يُستخدم **pg_ident**.

  - **pg_ctl_timeout**: كم ينبغي لـ pg_ctl الانتظار عند تنفيذ `start` أو `stop` أو `restart`. القيمة الافتراضية هي 60 ثانية.

  - **use_pg_rewind**: محاولة استخدام pg_rewind على القائد السابق عند انضمامه إلى العنقود كنسخة متماثلة. يجب إما تهيئة العنقود مع `data page checksums` (خيار `--data-checksums` لـ `initdb`) و/أو ضبط `wal_log_hints` على `on`، وإلا فلن يعمل `pg_rewind`.

  - **rewind**: (اختياري) خيارات مخصصة تمرر إلى أمر `pg_rewind`. يمكن تحديدها كقائمة سلاسل و/أو قواميس مفتاح-قيمة مفردة. الخيارات غير المسموح بها تشمل: `target-pgdata`, `source-pgdata`, `source-server`, `write-recovery-conf`, `dry-run`, `restore-target-wal`, `config-file`, `no-ensure-shutdown`, `version`, و`help`. مثال على الاستخدام:

    ```yaml
    postgresql:
      rewind:
        - debug
        - progress
        - sync-method: fsync
    ```

  - **remove_data_directory_on_rewind_failure**: إذا مُكِّن هذا الخيار، فسيزيل Patroni دليل بيانات PostgreSQL ويعيد إنشاء النسخة المتماثلة. وإلا فسيحاول متابعة القائد الجديد. القيمة الافتراضية هي **false**.

  - **remove_data_directory_on_diverged_timelines**: سيزيل Patroni دليل بيانات PostgreSQL ويعيد إنشاء النسخة المتماثلة إذا لاحظ أن الخطوط الزمنية تتشعب وأن العقدة الرئيسية السابقة لا يمكنها بدء البث من العقدة الرئيسية الجديدة. هذا الخيار مفيد عندما لا يمكن استخدام `pg_rewind`. أثناء تنفيذ فحص تشعب الخطوط الزمنية على PostgreSQL v10 وما أقدم سيحاول Patroni الاتصال ببيانات اعتماد النسخ المتماثل إلى قاعدة بيانات "postgres". لذلك، يجب السماح بمثل هذا الوصول في pg_hba.conf. القيمة الافتراضية هي **false**.

  - **replica_method**: لكل create_replica_methods غير basebackup، ستضيف قسم تهيئة بالاسم نفسه. كحد أدنى، ينبغي أن يتضمن ذلك "command" مع مسار كامل إلى السكربت الفعلي الذي سيُنفَّذ. ستُمرر معاملات التهيئة الأخرى إلى السكربت بصيغة "parameter=value".

  - **pre_promote**: سكربت تحويط (fencing) ينفَّذ أثناء تجاوز الأعطال بعد اكتساب قفل القائد وقبل ترقية النسخة المتماثلة. إذا خرج السكربت برمز غير صفري، فلن يرقّي Patroni النسخة المتماثلة، وسيزيل مفتاح القائد من DCS.

  - **before_stop**: سكربت ينفَّذ مباشرة قبل إيقاف postgres. على عكس الاستدعاء (callback)، يعمل هذا السكربت بشكل متزامن، مانعًا إيقاف التشغيل حتى يكتمل. لا يؤثر رمز الإرجاع لهذا السكربت في ما إذا كان إيقاف التشغيل سيتابع بعده أم لا.

<a id="restapi_settings"></a>

--------

## REST API {#rest-api}

- **restapi**:
  - **thread_pool_size**: حجم تجمع الخيوط الذي يستخدمه Patroni لمعالجة طلبات REST API. القيمة الدنيا هي `5`، والقيمة الافتراضية هي `5`.
  - **connect_address**: عنوان IP (أو اسم مضيف) والمنفذ، للوصول إلى [REST API](/ar/patroni/rest_api#rest_api) الخاص بـ Patroni. يجب أن يكون جميع أعضاء العنقود قادرين على الوصول إلى هذا العنوان. ما لم يكن Patroni مستخدمًا للعرض التجريبي المحلي فقط، استخدم عنوان شبكة بدلًا من "localhost" أو عنوان حلقي (loopback) مثل "127.0.0.1". يمكن أن يكون نقطة نهاية لفحوصات صحة HTTP (اقرأ أدناه عن معامل REST API "listen")، وأيضًا لاستعلامات المستخدم (إما مباشرة أو عبر REST API)، وكذلك لفحوصات الصحة التي يجريها أعضاء العنقود أثناء انتخابات القائد (مثلًا، لتحديد ما إذا كان القائد لا يزال يعمل، أو ما إذا كانت هناك عقدة لديها موضع WAL متقدم على العقدة التي تنفذ الاستعلام؛ إلخ). يوضع connect_address في مفتاح العضو في DCS، ما يجعل من الممكن ترجمة اسم العضو إلى العنوان للاتصال بواجهة REST API الخاصة به.
  - **listen**: عنوان IP (أو اسم مضيف) والمنفذ الذي سيستمع إليه Patroni من أجل REST API - لتوفير فحوصات الصحة نفسها ورسائل العنقود بين العقد المشاركة أيضًا، كما هو موصوف أعلاه. لتوفير معلومات فحص الصحة لـ HAProxy (أو أي موازن حمل آخر قادر على تنفيذ فحوصات "OPTIONS" أو "GET" عبر HTTP).
  - **authentication**: (اختياري)
    - **username**: اسم مستخدم المصادقة الأساسية لحماية نقاط نهاية REST API غير الآمنة.
    - **password**: كلمة مرور المصادقة الأساسية لحماية نقاط نهاية REST API غير الآمنة.
  - **certfile**: (اختياري): يحدد الملف الذي يحتوي الشهادة بصيغة PEM. إذا لم يُحدد ملف الشهادة أو تُرك فارغًا، فسيعمل خادم API دون SSL.
  - **keyfile**: (اختياري): يحدد الملف الذي يحتوي المفتاح السري بصيغة PEM.
  - **keyfile_password**: (اختياري): يحدد كلمة مرور لفك تشفير ملف المفتاح.
  - **cafile**: (اختياري): يحدد الملف الذي يحتوي CA_BUNDLE بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات العميل.
  - **ciphers**: (اختياري): يحدد مجموعات التشفير المسموح بها (مثل "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
  - **verify_client**: (اختياري): `none` (الافتراضي)، أو `optional` أو `required`. عند `none` لن تتحقق REST API من شهادات العميل. عند `required` تكون شهادات العميل مطلوبة لجميع استدعاءات REST API. عند `optional` تكون شهادات العميل مطلوبة لجميع نقاط نهاية REST API غير الآمنة. عند استخدام `required`، تنجح مصادقة العميل إذا نجح التحقق من توقيع الشهادة. مع `optional` لن تُفحص شهادة العميل إلا لطلبات `PUT` و`POST` و`PATCH` و`DELETE`.
  - **allowlist**: (اختياري): يحدد مجموعة المضيفين المسموح لهم باستدعاء نقاط نهاية REST API غير الآمنة. يمكن أن يكون العنصر الواحد اسم مضيف أو عنوان IP أو عنوان شبكة باستخدام تدوين CIDR. افتراضيًا يُستخدم `allow all`. في حال ضبط `allowlist` أو `allowlist_include_members`، يُرفض أي شيء غير مشمول.
  - **allowlist_include_members**: (اختياري): إذا ضُبط على `true` فهو يسمح بالوصول إلى نقاط نهاية REST API غير الآمنة من أعضاء العنقود الآخرين المسجلين في DCS (يُؤخذ عنوان IP أو اسم المضيف من `api_url` للأعضاء). كن حذرًا، قد يحدث أن يستخدم نظام التشغيل عنوان IP مختلفًا للاتصالات الصادرة.
  - **http_extra_headers**: (اختياري): ترويسات HTTP تتيح لخادم REST API تمرير معلومات إضافية مع استجابة HTTP.
  - **https_extra_headers**: (اختياري): ترويسات HTTPS تتيح لخادم REST API تمرير معلومات إضافية مع استجابة HTTP عند تمكين TLS. سيؤدي هذا أيضًا إلى تمرير المعلومات الإضافية المضبوطة في `http_extra_headers`.
  - **request_queue_size**: (اختياري): يضبط حجم قائمة انتظار الطلبات لمقبس TCP الذي تستخدمه Patroni REST API. عند امتلاء قائمة الانتظار، تحصل الطلبات اللاحقة على خطأ "Connection denied". القيمة الافتراضية هي 5.
  - **server_tokens**: (اختياري): يضبط قيمة ترويسة `Server` في HTTP.
    - `Minimal`: ستحتوي الترويسة على إصدار Patroni فقط، مثل `Patroni/4.0.0`.
    - `ProductOnly`: ستحتوي الترويسة على اسم المنتج فقط، مثل `Patroni`.
    - `Original` (الافتراضي): ستكشف الترويسة السلوك الأصلي وتعرض إصداري BaseHTTP وPython، مثل `BaseHTTP/0.6 Python/3.12.3`.

إليك مثال على كلا من **http_extra_headers** و**https_extra_headers**:

```yaml
restapi:
  listen: <listen>
  connect_address: <connect_address>
  authentication:
    username: <username>
    password: <password>
  http_extra_headers:
    'X-Frame-Options': 'SAMEORIGIN'
    'X-XSS-Protection': '1; mode=block'
    'X-Content-Type-Options': 'nosniff'
  cafile: <ca file>
  certfile: <cert>
  keyfile: <key>
  https_extra_headers:
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
```

<div class="warning">

<div class="title">

تحذير

</div>

- يجب أن يكون `restapi.connect_address` متاحًا من جميع عقد عنقود Patroni المعني. داخليًا يستخدمه Patroni أثناء سباق القيادة للعثور على العقد ذات أدنى تأخر في النسخ المتماثل.
- إذا فعّلت التحقق من شهادات العميل (`restapi.verify_client` مضبوط على `required`)، فعليك أيضًا **تقديم** **شهادات عميل صالحة** في `ctl.certfile`، و`ctl.keyfile`، و`ctl.keyfile_password`. إذا لم تُقدم، فلن يعمل Patroni بشكل صحيح.

</div>

<a id="patronictl_settings"></a>

--------

## CTL {#ctl}

- **ctl**: (اختياري)
  - **authentication**:
    - **username**: اسم مستخدم المصادقة الأساسية للوصول إلى نقاط نهاية REST API المحمية. إذا لم يُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "username" في REST API.
    - **password**: كلمة مرور المصادقة الأساسية للوصول إلى نقاط نهاية REST API المحمية. إذا لم تُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "password" في REST API.
  - **insecure**: السماح بالاتصالات إلى REST API دون التحقق من شهادات SSL.
  - **cacert**: يحدد الملف الذي يحتوي CA_BUNDLE أو الدليل بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات SSL لـ REST API. إذا لم يُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "cafile" في REST API.
  - **certfile**: يحدد الملف الذي يحتوي شهادة العميل بصيغة PEM.
  - **keyfile**: يحدد الملف الذي يحتوي المفتاح السري للعميل بصيغة PEM.
  - **keyfile_password**: يحدد كلمة مرور لفك تشفير ملف مفتاح العميل.

--------

## المراقب (Watchdog) {#watchdog}

- **mode**: `off` أو `automatic` أو `required`. عند `off` يكون المراقب (watchdog) معطلًا. عند `automatic` سيُستخدم المراقب إن توفر، ويُتجاهل إن لم يتوفر. عند `required` لن تصبح العقدة قائدة إلا إذا أمكن تمكين المراقب بنجاح.
- **device**: المسار إلى جهاز المراقب (watchdog). الافتراضي هو `/dev/watchdog`.
- **safety_margin**: عدد ثواني هامش الأمان بين استثارة المراقب وانتهاء صلاحية مفتاح القائد.

<a id="tags_settings"></a>

--------

## الوسوم {#tags}

- **clonefrom**: `true` أو `false`. إذا ضُبط على `true` فقد تفضل العقد الأخرى استخدام هذه العقدة لبدء التهيئة (أخذ `pg_basebackup` منها). إذا كانت هناك عدة عقد بوسم `clonefrom` مضبوط على `true` فسيُختار العقدة التي سيُبدأ التهيئة منها عشوائيًا. القيمة الافتراضية هي `false`.
- **noloadbalance**: `true` أو `false`. إذا ضُبط على `true` فستعيد العقدة رمز حالة HTTP 503 لفحص صحة `GET /replica` في REST API وبالتالي ستُستثنى من موازنة الحمل. الافتراضي هو `false`.
- **replicatefrom**: اسم نسخة متماثلة أخرى للنسخ المتماثل منها. يُستخدم لدعم النسخ المتماثل المتتالي.
- **nosync**: `true` أو `false`. إذا ضُبط على `true` فلن تُختار العقدة أبدًا كنسخة متماثلة متزامنة.
- **sync_priority**: عدد صحيح، يتحكم في الأولوية التي ينبغي أن تكون لهذه العقدة أثناء اختيار النسخة المتماثلة المتزامنة عندما يكون [synchronous_mode](/ar/patroni/replication_modes#synchronous_mode) مضبوطًا على `on`. ستُفضل العقد ذات الأولوية الأعلى على العقد ذات الأولوية الأدنى. إذا كانت `sync_priority` تساوي 0 أو كانت سالبة - فلا يُسمح بكتابة مثل هذه العقدة في معامل PostgreSQL `synchronous_standby_names` (مشابه لـ `nosync: true`). يرتب هذا المعامل الأولويات في الاتجاه المعاكس لعمود `sync_priority` في العرض `pg_stat_replication`.
- **nofailover**: `true` أو `false`، يتحكم فيما إذا كان يُسمح لهذه العقدة بالمشاركة في سباق القيادة وأن تصبح قائدة. الافتراضي هو `false`، ما يعني أن هذه العقدة <span id="can">تستطيع</span>\_ المشاركة في سباقات القيادة.
- **failover_priority**: عدد صحيح، يتحكم في الأولوية التي ينبغي أن تكون لهذه العقدة أثناء تجاوز الأعطال. ستُفضل العقد ذات الأولوية الأعلى على العقد ذات الأولوية الأدنى إذا استلمت/أعادت تشغيل الكمية نفسها من WAL. مع ذلك، تُفضل العقد ذات قيم receive/replay LSN الأعلى بغض النظر عن أولويتها. إذا كانت `failover_priority` تساوي 0 أو كانت سالبة - فلا يُسمح لمثل هذه العقدة بالمشاركة في سباق القيادة وأن تصبح قائدة (مشابه لـ `nofailover: true`). قيد معروف: `failover_priority` لا يعمل حاليًا مع [النسخ المتماثل المتزامن القائم على النصاب](/ar/patroni/replication_modes#quorum_mode).
- **nostream**: `true` أو `false`. إذا ضُبط على `true` فلن تستخدم العقدة بروتوكول النسخ المتماثل لبث WAL. بل ستعتمد على الاستعادة من الأرشيف (إذا ضُبط `restore_command`) واستقصاء `pg_wal`/`pg_xlog`. كما يعطل نسخ ومزامنة فتحات النسخ المتماثل المنطقية الدائمة على العقدة نفسها وجميع نسخها المتماثلة المتتالية. ضبط هذا الوسم على العقدة الرئيسية ليس له أي تأثير.

> [!WARNING]
> قدّم واحدًا فقط من `nofailover` أو `failover_priority`. تقديم `nofailover: true` هو نفسه `failover_priority: 0`، وتقديم `nofailover: false` سيمنح العقدة الأولوية 1.

بالإضافة إلى هذه الوسوم المعرفة مسبقًا، يمكنك أيضًا إضافة وسومك الخاصة:

- **key1**: `true`
- **key2**: `false`
- **key3**: `1.4`
- **key4**: `"RandomString"`

الوسوم مرئية في [REST API](/ar/patroni/rest_api#rest_api) وفي [patronictl_list](/ar/patroni/patronictl#patronictl_list) كما يمكنك التحقق من صحة مثيل باستخدام هذه الوسوم. إذا لم يُعرَّف الوسم لمثيل، أو إذا كانت القيمة المقابلة لا تطابق قيمة الاستعلام، فسيعيد رمز حالة HTTP 503.
