---
title: "إعدادات التهيئة عبر متغيرات البيئة"
linkTitle: "تهيئة البيئة"
weight: 30
icon: fa-solid fa-sliders
description: "متغيرات البيئة لتجاوز معاملات إعداد Patroni."
module: [PATRONI]
categories: [مرجع]
upstream_link: "https://patroni.readthedocs.io/en/latest/ENVIRONMENT.html"
---

<a id="env"></a>
من الممكن تجاوز بعض معاملات التهيئة المعرّفة في ملف تهيئة Patroni باستخدام متغيرات بيئة النظام. تسرد هذه الوثيقة جميع متغيرات البيئة التي يتعامل معها Patroni. القيم المضبوطة عبر تلك المتغيرات تأخذ الأسبقية دائمًا على القيم المضبوطة في ملف تهيئة Patroni.

--------

## عام/شامل {#globaluniversal}

- **PATRONI_CONFIGURATION**: من الممكن ضبط التهيئة الكاملة لـ Patroni عبر متغير البيئة [PATRONI_CONFIGURATION](/ar/patroni/config#config). في هذه الحالة لن يُؤخذ في الاعتبار أي متغيرات بيئة أخرى!
- **PATRONI_THREAD_POOL_SIZE**: حجم تجمع الخيوط الذي يستخدمه Patroni لتنفيذ المهام غير المتزامنة والتواصل عبر REST API مع الأعضاء الآخرين أثناء سباق القيادة أو فحوصات الفشل الآمن. القيمة الدنيا هي `5`، والقيمة الافتراضية هي `5`.
- **PATRONI_THREAD_STACK_SIZE**: يحدد حجم المكدس المستخدم للخيوط التي يبدأها Patroni. يجب أن تكون القيمة بمحاذاة `64kB`. القيمة الدنيا هي `64kB`، والقيمة الافتراضية (التي يضبطها Patroni) هي `512kB`.
- **PATRONI_NAME**: اسم العقدة التي يعمل عليها المثيل الحالي من Patroni. يجب أن يكون فريدًا للعنقود.
- **PATRONI_NAMESPACE**: المسار داخل مخزن التهيئة حيث سيحتفظ Patroni بمعلومات عن العنقود. القيمة الافتراضية: "/service"
- **PATRONI_SCOPE**: اسم العنقود
- **PG_MALLOC_ARENA_MAX**: قيمة مخصصة لمتغير البيئة `MALLOC_ARENA_MAX` لعملية `postmaster`. إذا لم تُضبط، فسيرث `postmaster` قيمة `MALLOC_ARENA_MAX`.

--------

## السجل {#log}

- **PATRONI_LOG_TYPE**: يضبط صيغة السجلات. يمكن أن تكون إما **plain** أو **json**. لاستخدام صيغة **json**، يجب أن يكون لديك [jsonlogger](/ar/patroni/installation#extras) مثبتًا. القيمة الافتراضية هي **plain**.
- **PATRONI_LOG_LEVEL**: يضبط مستوى التسجيل العام. القيمة الافتراضية هي **INFO** (راجع [وثائق التسجيل للغة Python](https://docs.python.org/3.6/library/logging.html#levels))
- **PATRONI_LOG_TRACEBACK_LEVEL**: يضبط المستوى الذي ستكون التتبعات العكسية (tracebacks) مرئية عنده. القيمة الافتراضية هي **ERROR**. اضبطه على **DEBUG** إذا أردت رؤية التتبعات العكسية فقط عند تمكين **PATRONI_LOG_LEVEL=DEBUG**.
- **PATRONI_LOG_FORMAT**: يضبط سلسلة تنسيق السجل. إذا كان نوع السجل **plain**، فيجب أن يكون تنسيق السجل سلسلة. راجع [سمات LogRecord](https://docs.python.org/3.6/library/logging.html#logrecord-attributes) للسمات المتاحة. إذا كان نوع السجل **json**، فيمكن أن يكون تنسيق السجل قائمة بالإضافة إلى سلسلة. يجب أن يقابل كل عنصر في القائمة سمات LogRecord. كن حذرًا من أن اسم الحقل فقط هو المطلوب، وأنه يجب حذف **%(** و**)**. إذا رغبت في طباعة حقل سجل باسم مفتاح مختلف، فاستخدم قاموسًا يكون مفتاح القاموس فيه هو حقل السجل، والقيمة هي اسم الحقل الذي تريد طباعته في السجل. القيمة الافتراضية هي **%(asctime)s %(levelname)s: %(message)s**
- **PATRONI_LOG_DATEFORMAT**: يضبط سلسلة تنسيق التاريخ والوقت. (راجع [وثائق formatTime()](https://docs.python.org/3.6/library/logging.html#logging.Formatter.formatTime))
- **PATRONI_LOG_STATIC_FIELDS**: يضيف حقولًا إضافية إلى السجل. هذا الخيار متاح فقط عند ضبط نوع السجل على **json**. مثال `PATRONI_LOG_STATIC_FIELDS="{app: patroni}"`
- **PATRONI_LOG_MAX_QUEUE_SIZE**: يستخدم Patroni تسجيلًا على مرحلتين. تُكتب سجلات التسجيل في قائمة انتظار في الذاكرة وهناك خيط منفصل يسحبها من قائمة الانتظار ويكتبها إلى stderr أو إلى ملف. حجم قائمة الانتظار الداخلية محدود افتراضيًا بـ **1000** سجل، وهو ما يكفي للاحتفاظ بسجلات المدة 1h20m الماضية.
- **PATRONI_LOG_DIR**: الدليل الذي تُكتب إليه سجلات التطبيق. يجب أن يكون الدليل موجودًا وقابلًا للكتابة من قبل المستخدم الذي ينفذ Patroni. إذا ضبطت متغير البيئة هذا، فسيحتفظ التطبيق افتراضيًا بـ 4 سجلات بحجم 25MB. يمكنك ضبط قيم الاحتفاظ تلك باستخدام `PATRONI_LOG_FILE_NUM` و`PATRONI_LOG_FILE_SIZE` (انظر أدناه).
- **PATRONI_LOG_MODE**: صلاحيات ملفات السجل (مثلًا، `0644`). إذا لم تُحدد، فستُضبط الصلاحيات بناءً على قيمة umask الحالية.
- **PATRONI_LOG_FILE_NUM**: عدد سجلات التطبيق التي يُحتفظ بها.
- **PATRONI_LOG_FILE_SIZE**: حجم ملف patroni.log (بالبايتات) الذي يشغّل تدوير السجل.
- **PATRONI_LOG_LOGGERS**: إعادة تعريف مستوى التسجيل لكل وحدة python. مثال `PATRONI_LOG_LOGGERS="{patroni.postmaster: WARNING, urllib3: DEBUG}"`
- **PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS**: إذا ضُبط على `true`، فلن تُخرج سجلات نبض القلب المتتالية المتطابقة. القيمة الافتراضية هي `false`.

> [!WARNING]
> يمكن أن يكون وقت تنفيذ حلقة HA معلومة قيمة جدًا في تشخيص تجاوزات الأعطال الناتجة عن استنزاف الموارد والمشكلات المشابهة. عندما يُضبط `PATRONI_LOG_DEDUPLICATE_HEARTBEAT_LOGS` على `true` فلن يُولَّد أي سجل لتنفيذ حلقة HA (إلا إذا تغير القائد)، وبالتالي فلن تتوفر هذه المعلومة المفيدة المحتملة من السجلات.

--------

## Citus {#citus}

يفعّل تكامل Patroni مع [Citus](https://docs.citusdata.com). إذا ضُبط، فسيهتم Patroni بتسجيل عقد Citus العاملة على المنسق. يمكنك العثور على مزيد من المعلومات حول دعم Citus [هنا](/ar/patroni/citus#citus).

- **PATRONI_CITUS_GROUP**: معرف مجموعة Citus، عدد صحيح. استخدم `0` للمنسق و`1`، `2`، إلخ... للعقد العاملة
- **PATRONI_CITUS_DATABASE**: قاعدة البيانات التي ينبغي إنشاء امتداد [citus](/ar/patroni/citus#citus) فيها. يجب أن تكون نفسها على المنسق وجميع العقد العاملة. حاليًا يُدعم قاعدة بيانات واحدة فقط.

--------

## Consul {#consul}

- **PATRONI_CONSUL_HOST**: host:port لوكيل Consul المحلي.
- **PATRONI_CONSUL_URL**: عنوان url لوكيل Consul المحلي، بالصيغة: http(s)://host:port
- **PATRONI_CONSUL_PORT**: (اختياري) منفذ Consul
- **PATRONI_CONSUL_SCHEME**: (اختياري) **http** أو **https**، الافتراضي هو **http**
- **PATRONI_CONSUL_TOKEN**: (اختياري) رمز ACL
- **PATRONI_CONSUL_VERIFY**: (اختياري) ما إذا كان سيُتحقق من شهادة SSL لطلبات HTTPS
- **PATRONI_CONSUL_CACERT**: (اختياري) شهادة المرجع (ca). إذا وُجدت فستُمكِّن التحقق.
- **PATRONI_CONSUL_CERT**: (اختياري) ملف شهادة العميل
- **PATRONI_CONSUL_KEY**: (اختياري) ملف مفتاح العميل. يمكن أن يكون فارغًا إذا كان المفتاح جزءًا من الشهادة.
- **PATRONI_CONSUL_DC**: (اختياري) مركز البيانات الذي سيتم التواصل معه. افتراضيًا يُستخدم مركز بيانات المضيف.
- **PATRONI_CONSUL_CONSISTENCY**: (اختياري) اختر وضع الاتساق لـ consul. القيم الممكنة هي `default` أو `consistent` أو `stale` (مزيد من التفاصيل في [مرجع consul API](https://www.consul.io/api/features/consistency.html/))
- **PATRONI_CONSUL_CHECKS**: (اختياري) قائمة فحوصات صحة Consul المستخدمة للجلسة. افتراضيًا تُستخدم قائمة فارغة.
- **PATRONI_CONSUL_REGISTER_SERVICE**: (اختياري) ما إذا كان ستُسجَّل خدمة بالاسم الذي يحدده المعامل scope وبالوسم master أو primary أو replica أو standby-leader بحسب دور العقدة. الافتراضي هو **false**
- **PATRONI_CONSUL_SERVICE_TAGS**: (اختياري) وسوم ثابتة إضافية تُضاف إلى خدمة Consul فضلًا عن الدور (`primary`/`replica`/`standby-leader`). افتراضيًا تُستخدم قائمة فارغة.
- **PATRONI_CONSUL_SERVICE_CHECK_INTERVAL**: (اختياري) كم مرة يُنفَّذ فحص الصحة مقابل url المسجل
- **PATRONI_CONSUL_SERVICE_CHECK_TLS_SERVER_NAME**: (اختياري) تجاوز مضيف SNI عند الاتصال عبر TLS، راجع أيضًا [مرجع واجهة consul agent check API](https://www.consul.io/api-docs/agent/check#tlsservername).

--------

## Etcd {#etcd}

- **PATRONI_ETCD_PROXY**: عنوان url للوسيط الخاص بـ etcd. إذا كنت تتصل بـ etcd عبر وسيط، فاستخدم هذا المعامل بدلًا من **PATRONI_ETCD_URL**
- **PATRONI_ETCD_URL**: عنوان url الخاص بـ etcd، بالصيغة: http(s)://(username:password@)host:port
- **PATRONI_ETCD_HOSTS**: قائمة نقاط نهاية etcd بالصيغة 'host1:port1','host2:port2',etc...
- **PATRONI_ETCD_USE_PROXIES**: إذا ضُبط هذا المعامل على true، فسيعتبر Patroni **hosts** قائمة وسطاء ولن ينفذ اكتشاف طبولوجيا عنقود etcd بل سيلتزم بقائمة **hosts** ثابتة.
- **PATRONI_ETCD_PROTOCOL**: http أو https، وإذا لم يُحدد فتُستخدم http. إذا حُدد **url** أو **proxy** - فسيأخذ البروتوكول منهما.
- **PATRONI_ETCD_HOST**: host:port لنقطة نهاية etcd.
- **PATRONI_ETCD_SRV**: النطاق للبحث عن سجلات SRV للاكتشاف التلقائي للعنقود. سيحاول Patroni الاستعلام عن أسماء خدمات SRV هذه للنطاق المحدد (بهذا الترتيب حتى أول نجاح): `_etcd-client-ssl`, `_etcd-client`, `_etcd-ssl`, `_etcd`, `_etcd-server-ssl`, `_etcd-server`. إذا استُرجعت سجلات SRV لـ `_etcd-server-ssl` أو `_etcd-server` فسيُستخدم بروتوكول ETCD peer للاستعلام عن ETCD عن الأعضاء المتاحين. وإلا فسيُستخدم المضيفون من سجلات SRV.
- **PATRONI_ETCD_SRV_SUFFIX**: يضبط لاحقة لاسم SRV الذي يُستعلم عنه أثناء الاكتشاف. استخدم هذا الخيار للتمييز بين عناقيد etcd متعددة تحت النطاق نفسه. يعمل فقط بالاقتران مع **PATRONI_ETCD_SRV**. مثلًا، إذا ضُبط `PATRONI_ETCD_SRV_SUFFIX=foo` و`PATRONI_ETCD_SRV=example.org`، فسيُنفذ استعلام DNS SRV التالي:`_etcd-client-ssl-foo._tcp.example.org` (وهكذا لكل أسماء خدمات ETCD SRV الممكنة).
- **PATRONI_ETCD_USERNAME**: اسم المستخدم لمصادقة etcd.
- **PATRONI_ETCD_PASSWORD**: كلمة المرور لمصادقة etcd.
- **PATRONI_ETCD_CACERT**: شهادة المرجع (ca). إذا وُجدت فستُمكِّن التحقق.
- **PATRONI_ETCD_CERT**: ملف شهادة العميل.
- **PATRONI_ETCD_KEY**: ملف مفتاح العميل. يمكن أن يكون فارغًا إذا كان المفتاح جزءًا من الشهادة.

--------

## Etcdv3 {#etcdv3}

أسماء متغيرات البيئة لـ Etcdv3 مشابهة لما هي عليه لـ Etcd، عليك فقط استخدام `ETCD3` بدلًا من `ETCD` في اسم المتغير. مثال: `PATRONI_ETCD3_HOST`، `PATRONI_ETCD3_CACERT`، وهكذا.

> [!WARNING]
> المفاتيح التي أُنشئت بإصدار البروتوكول 2 لا تُرى بإصدار البروتوكول 3 والعكس صحيح، لذلك لا يمكن الانتقال من Etcd إلى Etcdv3 بمجرد تحديث تهيئة Patroni. بالإضافة إلى ذلك، يستخدم Patroni بوابة gRPC-gateway (الوسيط) الخاصة بـ Etcd للتواصل مع V3 API، ما يعني أن مصادقة الاسم الشائع (common name) لـ TLS غير ممكنة.

--------

## ZooKeeper {#zookeeper}

- **PATRONI_ZOOKEEPER_HOSTS**: قائمة مفصولة بفواصل لأعضاء عنقود ZooKeeper: "'host1:port1','host2:port2','etc...'". من المهم وضع علامات اقتباس حول كل عنصر على حدة!
- **PATRONI_ZOOKEEPER_USE_SSL**: (اختياري) ما إذا كان يُستخدم SSL أم لا. الافتراضي هو `false`. إذا ضُبط على `false`، فتُتجاهل جميع المعاملات الخاصة بـ SSL.
- **PATRONI_ZOOKEEPER_CACERT**: (اختياري) شهادة المرجع (CA). إذا وُجدت فستُمكِّن التحقق.
- **PATRONI_ZOOKEEPER_CERT**: (اختياري) ملف شهادة العميل.
- **PATRONI_ZOOKEEPER_KEY**: (اختياري) ملف مفتاح العميل.
- **PATRONI_ZOOKEEPER_KEY_PASSWORD**: (اختياري) كلمة مرور مفتاح العميل.
- **PATRONI_ZOOKEEPER_VERIFY**: (اختياري) ما إذا كان سيُتحقق من الشهادة أم لا. الافتراضي هو `true`.
- **PATRONI_ZOOKEEPER_SET_ACLS**: (اختياري) إذا ضُبط، فسيُضبط Kazoo لتطبيق ACL افتراضي على كل ZNode ينشئه. يمكن أن تستخدم ACLs إما مخطط `x509` (الافتراضي) أو مخططات ZooKeeper الأخرى المدعومة مثل `digest`. يجب تحديدها كقاموس يكون المفتاح فيه هو الاسم الرئيسي الكامل (مع بادئة المخطط اختياريًا) والقيمة قائمة بالصلاحيات. يمكن أن تكون الصلاحيات واحدة أو أكثر من `CREATE`, `READ`, `WRITE`, `DELETE`, `ADMIN`, أو `ALL`. مثلًا، `set_acls: {CN=principal1: [CREATE, READ], digest:principal2:+pjROuBuuwNNSujKyH8dGcEnFPQ=: [ALL]}`.
- **PATRONI_ZOOKEEPER_AUTH_DATA**: (اختياري) بيانات اعتماد المصادقة المستخدمة للاتصال. يجب أن تكون قاموسًا بالشكل الذي يكون فيه `scheme` هو المفتاح و`credential` هو القيمة. الافتراضي قاموس فارغ.

> [!NOTE]
> يلزم تثبيت `kazoo>=2.6.0` لدعم SSL.

--------

## Exhibitor {#exhibitor}

- **PATRONI_EXHIBITOR_HOSTS**: القائمة الأولية لعقد Exhibitor (ZooKeeper) بالصيغة: 'host1,host2,etc...'. تُحدَّث هذه القائمة تلقائيًا كلما تغيرت طبولوجيا عنقود Exhibitor (ZooKeeper).
- **PATRONI_EXHIBITOR_PORT**: منفذ Exhibitor.

<a id="kubernetes_environment"></a>

--------

## Kubernetes {#kubernetes}

- **PATRONI_KUBERNETES_BYPASS_API_SERVICE**: (اختياري) عند التواصل مع واجهة Kubernetes API، يعتمد Patroni عادةً على خدمة [kubernetes](/ar/patroni/kubernetes#kubernetes)، التي يُكشف عنوانها في الـ pods عبر متغير البيئة `KUBERNETES_SERVICE_HOST`. إذا ضُبط `PATRONI_KUBERNETES_BYPASS_API_SERVICE` على `true`، فسيحل Patroni قائمة عقد API الكامنة خلف الخدمة ويتصل بها مباشرة.
- **PATRONI_KUBERNETES_NAMESPACE**: (اختياري) فضاء الأسماء في Kubernetes حيث يعمل pod الخاص بـ Patroni. القيمة الافتراضية هي `default`.
- **PATRONI_KUBERNETES_LABELS**: تسميات بالصيغة `{label1: value1, label2: value2}`. ستُستخدم هذه التسميات للعثور على الكائنات الموجودة (Pods وإما Endpoints أو ConfigMaps) المرتبطة بالعنقود الحالي. كما سيضعها Patroni على كل كائن (Endpoint أو ConfigMap) ينشئه.
- **PATRONI_KUBERNETES_SCOPE_LABEL**: (اختياري) اسم التسمية التي تحتوي على اسم العنقود. القيمة الافتراضية هي `cluster-name`.
- **PATRONI_KUBERNETES_BOOTSTRAP_LABELS**: (اختياري) تسميات بالصيغة `{label1: value1, label2: value2}`. ستُخصص هذه التسميات لـ pod الخاص بـ Patroni عندما تكون حالته إما `initializing new cluster` أو `running custom bootstrap script` أو `starting after custom bootstrap` أو `creating replica`.
- **PATRONI_KUBERNETES_ROLE_LABEL**: (اختياري) اسم التسمية التي تحتوي على الدور (`primary` أو `replica` أو قيمة مخصصة أخرى). سيضبط Patroni هذه التسمية على الـ pod الذي يعمل فيه. القيمة الافتراضية هي `role`.
- **PATRONI_KUBERNETES_LEADER_LABEL_VALUE**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `primary`. القيمة الافتراضية هي `primary`.
- **PATRONI_KUBERNETES_FOLLOWER_LABEL_VALUE**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `replica`. القيمة الافتراضية هي `replica`.
- **PATRONI_KUBERNETES_STANDBY_LEADER_LABEL_VALUE**: (اختياري) قيمة تسمية الـ pod عندما يكون دور Postgres هو `standby_leader`. القيمة الافتراضية هي `primary`.
- **PATRONI_KUBERNETES_TMP_ROLE_LABEL**: (اختياري) اسم التسمية المؤقتة التي تحتوي على الدور (`primary` أو `replica`). ستستخدم قيمة هذه التسمية دائمًا القيمة الافتراضية للدور المقابل. لا تضبطها إلا عند الضرورة.
- **PATRONI_KUBERNETES_USE_ENDPOINTS**: (اختياري) إذا ضُبط على true، فسيستخدم Patroni Endpoints بدلًا من ConfigMaps لإجراء انتخابات القائد والاحتفاظ بحالة العنقود.
- **PATRONI_KUBERNETES_POD_IP**: (اختياري) عنوان IP للـ pod الذي يعمل فيه Patroni. هذه القيمة مطلوبة عند تمكين `PATRONI_KUBERNETES_USE_ENDPOINTS` وتُستخدم لتعبئة مجموعات نقطة نهاية القائد عند ترقية PostgreSQL الخاص بالـ pod.
- **PATRONI_KUBERNETES_PORTS**: (اختياري) إذا كان كائن Service يحمل اسمًا للمنفذ، فيجب أن يظهر الاسم نفسه في كائن Endpoint، وإلا فلن تعمل الخدمة. مثلًا، إذا كانت خدمتك معرفة كـ `{Kind: Service, spec: {ports: [{name: postgresql, port: 5432, targetPort: 5432}]}}`، فعليك ضبط `PATRONI_KUBERNETES_PORTS='[{"name": "postgresql", "port": 5432}]'` وسيستخدمه Patroni لتحديث مجموعات نقطة نهاية القائد Endpoint. يُستخدم هذا المعامل فقط إذا ضُبط `PATRONI_KUBERNETES_USE_ENDPOINTS`.
- **PATRONI_KUBERNETES_CACERT**: (اختياري) يحدد الملف الذي يحتوي CA_BUNDLE بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات SSL لواجهة Kubernetes API. إذا لم يُقدم، فسيستخدم patroni القيمة التي يوفرها سر ServiceAccount.
- **PATRONI_RETRIABLE_HTTP_CODES**: (اختياري) قائمة رموز حالة HTTP من واجهة K8s API التي يُعاد المحاولة عندها. افتراضيًا يعيد Patroni المحاولة عند `500` و`503` و`504`، أو إذا كانت استجابة K8s API تحمل ترويسة HTTP `retry-after`.

--------

## Raft (مهمل) {#raft-deprecated}

- **PATRONI_RAFT_SELF_ADDR**: `ip:port` للاستماع لاتصالات Raft. يجب أن يكون `self_addr` متاحًا من العقد الأخرى للعنقود. إذا لم يُضبط، فلن تشارك العقدة في التوافق (consensus).
- **PATRONI_RAFT_BIND_ADDR**: (اختياري) `ip:port` للاستماع لاتصالات Raft. إذا لم يُحدد فسيُستخدم `self_addr`.
- **PATRONI_RAFT_PARTNER_ADDRS**: قائمة عقد Patroni الأخرى في العنقود بالصيغة `"'ip1:port1','ip2:port2'"`. من المهم وضع علامات اقتباس حول كل عنصر على حدة!
- **PATRONI_RAFT_DATA_DIR**: الدليل الذي يُخزن فيه سجل Raft واللقطة (snapshot). إذا لم يُحدد فسيُستخدم دليل العمل الحالي.
- **PATRONI_RAFT_PASSWORD**: (اختياري) تشفير حركة مرور Raft بكلمة مرور محددة، يتطلب وحدة `cryptography` للغة python.
- **PATRONI_RAFT_MIN_TIMEOUT**: (اختياري) الحد الأدنى لمهلة الانتخابات بالثواني لتنفيذ pysyncobj Raft الأساسي. يجب أن يكون أكبر من 3 * `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. الافتراضي: `0.4`.
- **PATRONI_RAFT_MAX_TIMEOUT**: (اختياري) الحد الأقصى لمهلة الانتخابات بالثواني لتنفيذ pysyncobj Raft الأساسي. يجب أن يكون أكبر من `PATRONI_RAFT_MIN_TIMEOUT`. الافتراضي: `1.4`.
- **PATRONI_RAFT_CONNECTION_TIMEOUT**: (اختياري) الوقت بالثواني الذي يُعد بعده اتصال لم تُستقبل فيه بيانات ميّتًا. يجب أن يكون أكبر من أو يساوي `PATRONI_RAFT_MAX_TIMEOUT`. الافتراضي: `3.5`.
- **PATRONI_RAFT_APPEND_ENTRIES_PERIOD**: (اختياري) الفاصل الزمني بالثواني لإرسال أوامر نبض القلب. يجب أن يكون أقل من ثلث `PATRONI_RAFT_MIN_TIMEOUT`. الافتراضي: `0.1`.
- **PATRONI_RAFT_CONNECTION_RETRY_TIME**: (اختياري) الفاصل الزمني بالثواني بين محاولات إعادة الاتصال بالعقد غير المتصلة. الافتراضي: `5.0`.
- **PATRONI_RAFT_LEADER_FALLBACK_TIMEOUT**: (اختياري) الوقت بالثواني الذي يتراجع بعده قائد بلا استجابة من الأغلبية إلى حالة التابع. يجب أن يكون أكبر من `PATRONI_RAFT_APPEND_ENTRIES_PERIOD`. الافتراضي: `30.0`.

> [!NOTE]
> يتحقق Patroni من هذه القيود عند بدء التشغيل وسيرفض البدء إذا كانت منتهكة. لا يمكن تغيير هذه القيم في وقت التشغيل وتتطلب إعادة تشغيل. راجع [إعدادات Raft](/ar/patroni/config/yaml#raft_settings) للتفاصيل، بما في ذلك قيد زمن الاستجابة العالي.

--------

## PostgreSQL {#postgresql}

- **PATRONI_POSTGRESQL_LISTEN**: عنوان IP + المنفذ الذي يستمع إليه Postgres. يُسمح بعناوين متعددة مفصولة بفواصل، طالما أن مكوّن المنفذ يُلحق بعد الأخير منها بنقطتين، أي `listen: 127.0.0.1,127.0.0.2:5432`. سيستخدم Patroni أول عنوان من هذه القائمة لتأسيس اتصالات محلية بعقدة PostgreSQL.
- **PATRONI_POSTGRESQL_CONNECT_ADDRESS**: عنوان IP + المنفذ الذي يمكن الوصول إلى Postgres من خلاله من العقد والتطبيقات الأخرى.
- **PATRONI_POSTGRESQL_PROXY_ADDRESS**: عنوان IP + المنفذ الذي يمكن الوصول من خلاله إلى مجمّع اتصالات (مثل pgbouncer) يعمل بجوار Postgres. تُكتب القيمة في مفتاح العضو في DCS كـ `proxy_url` ويمكن أن تكون مستخدمة/مفيدة لاكتشاف الخدمات.
- **PATRONI_POSTGRESQL_DATA_DIR**: موقع دليل بيانات Postgres، إما موجود أو ليقوم Patroni بتهيئته.
- **PATRONI_POSTGRESQL_CONFIG_DIR**: موقع دليل تهيئة Postgres، الافتراضي هو دليل البيانات. يجب أن يكون قابلًا للكتابة من Patroni.
- **PATRONI_POSTGRESQL_BIN_DIR**: المسار إلى ملفات PostgreSQL الثنائية. (pg_ctl, initdb, pg_controldata, pg_basebackup, postgres, pg_isready, pg_rewind) القيمة الافتراضية سلسلة فارغة ما يعني أنه سيُستخدم متغير البيئة PATH للعثور على الملفات التنفيذية.
- **PATRONI_POSTGRESQL_BIN_PG_CTL**: (اختياري) اسم مخصص للملف الثنائي `pg_ctl`.
- **PATRONI_POSTGRESQL_BIN_INITDB**: (اختياري) اسم مخصص للملف الثنائي `initdb`.
- **PATRONI_POSTGRESQL_BIN_PG_CONTROLDATA**: (اختياري) اسم مخصص للملف الثنائي `pg_controldata`.
- **PATRONI_POSTGRESQL_BIN_PG_BASEBACKUP**: (اختياري) اسم مخصص للملف الثنائي `pg_basebackup`.
- **PATRONI_POSTGRESQL_BIN_POSTGRES**: (اختياري) اسم مخصص للملف الثنائي `postgres`.
- **PATRONI_POSTGRESQL_BIN_IS_READY**: (اختياري) اسم مخصص للملف الثنائي `pg_isready`.
- **PATRONI_POSTGRESQL_BIN_PG_REWIND**: (اختياري) اسم مخصص للملف الثنائي `pg_rewind`.
- **PATRONI_POSTGRESQL_PGPASS**: المسار إلى ملف كلمات المرور [.pgpass](https://www.postgresql.org/docs/current/static/libpq-pgpass.html). ينشئ Patroni هذا الملف قبل تنفيذ pg_basebackup وفي بعض الظروف الأخرى. يجب أن يكون الموقع قابلًا للكتابة من Patroni.
- **PATRONI_REPLICATION_USERNAME**: اسم مستخدم النسخ المتماثل؛ سيُنشأ المستخدم أثناء التهيئة الأولية. ستستخدم النسخ المتماثلة هذا المستخدم للوصول إلى مصدر النسخ المتماثل عبر النسخ المتماثل الانسيابي
- **PATRONI_REPLICATION_PASSWORD**: كلمة مرور النسخ المتماثل؛ سيُنشأ المستخدم أثناء التهيئة الأولية.
- **PATRONI_REPLICATION_SSLMODE**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
- **PATRONI_REPLICATION_SSLKEY**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
- **PATRONI_REPLICATION_SSLPASSWORD**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `PATRONI_REPLICATION_SSLKEY`.
- **PATRONI_REPLICATION_SSLCERT**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
- **PATRONI_REPLICATION_SSLROOTCERT**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
- **PATRONI_REPLICATION_SSLCRL**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_REPLICATION_SSLCRLDIR**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_REPLICATION_SSLNEGOTIATION**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
- **PATRONI_REPLICATION_GSSENCMODE**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
- **PATRONI_REPLICATION_CHANNEL_BINDING**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).
- **PATRONI_SUPERUSER_USERNAME**: اسم المستخدم الفائق، يُضبط أثناء التهيئة الأولية (initdb) ويستخدمه Patroni لاحقًا للاتصال بـ postgres. كما يستخدم pg_rewind هذا المستخدم.
- **PATRONI_SUPERUSER_PASSWORD**: كلمة مرور المستخدم الفائق، تُضبط أثناء التهيئة الأولية (initdb).
- **PATRONI_SUPERUSER_SSLMODE**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
- **PATRONI_SUPERUSER_SSLKEY**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
- **PATRONI_SUPERUSER_SSLPASSWORD**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `PATRONI_SUPERUSER_SSLKEY`.
- **PATRONI_SUPERUSER_SSLCERT**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
- **PATRONI_SUPERUSER_SSLROOTCERT**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
- **PATRONI_SUPERUSER_SSLCRL**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_SUPERUSER_SSLCRLDIR**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_SUPERUSER_SSLNEGOTIATION**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
- **PATRONI_SUPERUSER_GSSENCMODE**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
- **PATRONI_SUPERUSER_CHANNEL_BINDING**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).
- **PATRONI_REWIND_USERNAME**: (اختياري) اسم المستخدم لـ `pg_rewind`؛ سيُنشأ المستخدم أثناء تهيئة postgres 11+ وستُمنح جميع [الصلاحيات](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8) اللازمة.
- **PATRONI_REWIND_PASSWORD**: (اختياري) كلمة مرور المستخدم لـ `pg_rewind`؛ سيُنشأ المستخدم أثناء التهيئة الأولية.
- **PATRONI_REWIND_SSLMODE**: (اختياري) يتطابق مع معامل الاتصال [sslmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)، الذي يتيح للعميل تحديد نوع وضع التفاوض على TLS مع الخادم. لمزيد من المعلومات عن كيفية عمل كل وضع، يرجى زيارة [وثائق PostgreSQL](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-SSLMODE-STATEMENTS). الوضع الافتراضي هو `prefer`.
- **PATRONI_REWIND_SSLKEY**: (اختياري) يتطابق مع معامل الاتصال [sslkey](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLKEY)، الذي يحدد موقع المفتاح السري المستخدم مع شهادة العميل.
- **PATRONI_REWIND_SSLPASSWORD**: (اختياري) يتطابق مع معامل الاتصال [sslpassword](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLPASSWORD)، الذي يحدد كلمة المرور للمفتاح السري المحدد في `PATRONI_REWIND_SSLKEY`.
- **PATRONI_REWIND_SSLCERT**: (اختياري) يتطابق مع معامل الاتصال [sslcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCERT)، الذي يحدد موقع شهادة العميل.
- **PATRONI_REWIND_SSLROOTCERT**: (اختياري) يتطابق مع معامل الاتصال [sslrootcert](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT)، الذي يحدد موقع ملف يحتوي على شهادة أو شهادات مرجع أو أكثر (CA) سيستخدمها العميل للتحقق من شهادة الخادم.
- **PATRONI_REWIND_SSLCRL**: (اختياري) يتطابق مع معامل الاتصال [sslcrl](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRL)، الذي يحدد موقع ملف يحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_REWIND_SSLCRLDIR**: (اختياري) يتطابق مع معامل الاتصال [sslcrldir](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLCRLDIR)، الذي يحدد موقع دليل بملفات تحتوي على قائمة إبطال شهادات. سيرفض العميل الاتصال بأي خادم لديه شهادة موجودة في هذه القائمة.
- **PATRONI_REWIND_SSLNEGOTIATION**: (اختياري) يتطابق مع معامل الاتصال [sslnegotiation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-SSLNEGOTIATION)، الذي يتحكم في كيفية التفاوض على تشفير SSL مع الخادم، إذا كان SSL مستخدمًا.
- **PATRONI_REWIND_GSSENCMODE**: (اختياري) يتطابق مع معامل الاتصال [gssencmode](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-GSSENCMODE)، الذي يحدد ما إذا أو بأي أولوية سيُتفاوض على اتصال GSS TCP/IP آمن مع الخادم
- **PATRONI_REWIND_CHANNEL_BINDING**: (اختياري) يتطابق مع معامل الاتصال [channel_binding](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-CHANNEL-BINDING)، الذي يتحكم في استخدام العميل لربط القناة (channel binding).

--------

## REST API {#rest-api}

- **PATRONI_RESTAPI_THREAD_POOL_SIZE**: حجم تجمع الخيوط الذي يستخدمه Patroni لمعالجة طلبات REST API. القيمة الدنيا هي `5`، والقيمة الافتراضية هي `5`.
- **PATRONI_RESTAPI_CONNECT_ADDRESS**: عنوان IP والمنفذ للوصول إلى REST API.
- **PATRONI_RESTAPI_LISTEN**: عنوان IP والمنفذ الذي سيستمع إليه Patroni، لتوفير معلومات فحص الصحة لـ HAProxy.
- **PATRONI_RESTAPI_USERNAME**: اسم مستخدم المصادقة الأساسية لحماية نقاط نهاية REST API غير الآمنة.
- **PATRONI_RESTAPI_PASSWORD**: كلمة مرور المصادقة الأساسية لحماية نقاط نهاية REST API غير الآمنة.
- **PATRONI_RESTAPI_CERTFILE**: يحدد الملف الذي يحتوي الشهادة بصيغة PEM. إذا لم يُحدد ملف الشهادة أو تُرك فارغًا، فسيعمل خادم API دون SSL.
- **PATRONI_RESTAPI_KEYFILE**: يحدد الملف الذي يحتوي المفتاح السري بصيغة PEM.
- **PATRONI_RESTAPI_KEYFILE_PASSWORD**: يحدد كلمة مرور لفك تشفير ملف المفتاح.
- **PATRONI_RESTAPI_CAFILE**: يحدد الملف الذي يحتوي CA_BUNDLE بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات العميل.
- **PATRONI_RESTAPI_CIPHERS**: (اختياري) يحدد مجموعات التشفير المسموح بها (مثل "ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:!SSLv1:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1")
- **PATRONI_RESTAPI_VERIFY_CLIENT**: `none` (الافتراضي)، أو `optional` أو `required`. عند `none` لن تتحقق REST API من شهادات العميل. عند `required` تكون شهادات العميل مطلوبة لجميع استدعاءات REST API. عند `optional` تكون شهادات العميل مطلوبة لجميع نقاط نهاية REST API غير الآمنة. عند استخدام `required`، تنجح مصادقة العميل إذا نجح التحقق من توقيع الشهادة. مع `optional` لن تُفحص شهادة العميل إلا لطلبات `PUT` و`POST` و`PATCH` و`DELETE`.
- **PATRONI_RESTAPI_ALLOWLIST**: (اختياري): يحدد مجموعة المضيفين المسموح لهم باستدعاء نقاط نهاية REST API غير الآمنة. يمكن أن يكون العنصر الواحد اسم مضيف أو عنوان IP أو عنوان شبكة باستخدام تدوين CIDR. افتراضيًا يُستخدم `allow all`. في حال ضبط `allowlist` أو `allowlist_include_members`، يُرفض أي شيء غير مشمول.
- **PATRONI_RESTAPI_ALLOWLIST_INCLUDE_MEMBERS**: (اختياري): إذا ضُبط على `true` فهو يسمح بالوصول إلى نقاط نهاية REST API غير الآمنة من أعضاء العنقود الآخرين المسجلين في DCS (يُؤخذ عنوان IP أو اسم المضيف من `api_url` للأعضاء). كن حذرًا، قد يحدث أن يستخدم نظام التشغيل عنوان IP مختلفًا للاتصالات الصادرة.
- **PATRONI_RESTAPI_HTTP_EXTRA_HEADERS**: (اختياري) ترويسات HTTP تتيح لخادم REST API تمرير معلومات إضافية مع استجابة HTTP.
- **PATRONI_RESTAPI_HTTPS_EXTRA_HEADERS**: (اختياري) ترويسات HTTPS تتيح لخادم REST API تمرير معلومات إضافية مع استجابة HTTP عند تمكين TLS. سيؤدي هذا أيضًا إلى تمرير المعلومات الإضافية المضبوطة في `http_extra_headers`.
- **PATRONI_RESTAPI_REQUEST_QUEUE_SIZE**: (اختياري): يضبط حجم قائمة انتظار الطلبات لمقبس TCP الذي تستخدمه Patroni REST API. عند امتلاء قائمة الانتظار، تحصل الطلبات اللاحقة على خطأ "Connection denied". القيمة الافتراضية هي 5.
- **PATRONI_RESTAPI_SERVER_TOKENS**: (اختياري) يضبط قيمة ترويسة `Server` في HTTP. `Original` (الافتراضي) سيُظهر السلوك الأصلي ويعرض إصداري BaseHTTP وPython، مثل `BaseHTTP/0.6 Python/3.12.3`. `Minimal`: ستحتوي الترويسة على إصدار Patroni فقط، مثل `Patroni/4.0.0`. `ProductOnly`: ستحتوي الترويسة على اسم المنتج فقط، مثل `Patroni`.

<div class="warning">

<div class="title">

تحذير

</div>

- يجب أن يكون `PATRONI_RESTAPI_CONNECT_ADDRESS` متاحًا من جميع عقد عنقود Patroni المعني. داخليًا يستخدمه Patroni أثناء سباق القيادة للعثور على العقد ذات أدنى تأخر في النسخ المتماثل.
- إذا فعّلت التحقق من شهادات العميل (`PATRONI_RESTAPI_VERIFY_CLIENT` مضبوط على `required`)، فعليك أيضًا **تقديم** **شهادات عميل صالحة** في `PATRONI_CTL_CERTFILE`, `PATRONI_CTL_KEYFILE`, `PATRONI_CTL_KEYFILE_PASSWORD`. إذا لم تُقدم، فلن يعمل Patroni بشكل صحيح.

</div>

--------

## CTL {#ctl}

- **PATRONICTL_CONFIG_FILE**: (اختياري) موقع ملف التهيئة.
- **PATRONI_CTL_USERNAME**: (اختياري) اسم مستخدم المصادقة الأساسية للوصول إلى نقاط نهاية REST API المحمية. إذا لم يُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "username" في REST API.
- **PATRONI_CTL_PASSWORD**: (اختياري) كلمة مرور المصادقة الأساسية للوصول إلى نقاط نهاية REST API المحمية. إذا لم تُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "password" في REST API.
- **PATRONI_CTL_INSECURE**: (اختياري) السماح بالاتصالات إلى REST API دون التحقق من شهادات SSL.
- **PATRONI_CTL_CACERT**: (اختياري) يحدد الملف الذي يحتوي CA_BUNDLE أو الدليل بشهادات المراجع الموثوقة لاستخدامها أثناء التحقق من شهادات SSL لـ REST API. إذا لم يُقدم فسيستخدم [patronictl](/ar/patroni/patronictl#patronictl) القيمة المقدمة لمعامل "cafile" في REST API.
- **PATRONI_CTL_CERTFILE**: (اختياري) يحدد الملف الذي يحتوي شهادة العميل بصيغة PEM.
- **PATRONI_CTL_KEYFILE**: (اختياري) يحدد الملف الذي يحتوي المفتاح السري للعميل بصيغة PEM.
- **PATRONI_CTL_KEYFILE_PASSWORD**: (اختياري) يحدد كلمة مرور لفك تشفير ملف مفتاح العميل.
