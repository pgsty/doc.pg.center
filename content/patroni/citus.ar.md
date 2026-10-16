---
title: "دعم Citus"
weight: 130
icon: fas fa-lemon
description: "تفاصيل تكامل Patroni مع منسق Citus ومجموعات العقد العاملة."
module: [PATRONI]
categories: [مفهوم]
upstream_link: "https://patroni.readthedocs.io/en/latest/citus.html"
---

<a id="citus"></a>
يجعل Patroni نشر عناقيد [Multi-Node Citus](https://docs.citusdata.com/en/stable/installation/multi_node.html) أمرًا بالغ البساطة.

--------

## الخلاصة السريعة (TL;DR) {#tldr}

هناك فقط قواعد بسيطة قليلة عليك اتباعها:

1.  يجب أن يكون امتداد قاعدة البيانات [Citus](https://github.com/citusdata/citus) لـ PostgreSQL متوفرًا على جميع العقد. الحد الأدنى المطلق لإصدار Citus المدعوم هو 10.0، لكن، للاستفادة من كامل مزايا التبديلات وإعادات تشغيل العقد العاملة الشفافة نوصي باستخدام Citus 11.2 على الأقل.
2.  يجب أن يكون اسم العنقود (`scope`) نفسه لجميع عقد Citus!
3.  يجب أن تكون بيانات اعتماد المستخدم الفائق نفسها على المنسق وجميع العقد العاملة، وأن يسمح `pg_hba.conf` بوصول المستخدم الفائق بين جميع العقد.
4.  يجب السماح بالوصول إلى [REST API](/ar/patroni/config/yaml#restapi_settings) من العقد العاملة إلى المنسق. مثلًا، يجب أن تكون بيانات الاعتماد نفسها، وإذا ضُبطت شهادات العميل، فيجب أن يقبل المنسق شهادات العميل من العقد العاملة.
5.  أضف القسم التالي إلى `patroni.yaml`:

```yaml
citus:
  group: X  # 0 for coordinator and 1, 2, 3, etc for workers
  database: citus  # must be the same on all nodes
```

بعد ذلك تحتاج فقط إلى بدء Patroni ويتولى الباقي:

0.  سيضبط Patroni `bootstrap.dcs.synchronous_mode` على [quorum](/ar/patroni/replication_modes#quorum_mode) إذا لم يكن مضبوطًا صراحةً على قيمة أخرى.
1.  سيُضاف امتداد [citus](/ar/patroni/citus#citus) تلقائيًا إلى `shared_preload_libraries`.
2.  إذا لم يُضبط `max_prepared_transactions` صراحةً في [التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) العامة فسيضبطه Patroni تلقائيًا على `2*max_connections`.
3.  ستُعدَّل قيمة GUC لـ `citus.local_hostname` من `localhost` إلى القيمة التي يستخدمها Patroni للاتصال بمثيل PostgreSQL المحلي. ينبغي أحيانًا أن تكون القيمة مختلفة عن `localhost` لأن PostgreSQL قد لا يكون مستمعًا عليه.
4.  ستُنشأ `citus.database` تلقائيًا تتبعها `CREATE EXTENSION citus`.
5.  ستُضاف [بيانات الاعتماد](/ar/patroni/config/yaml#postgresql_settings) الحالية للمستخدم الفائق إلى جدول `pg_dist_authinfo` للسماح بالتواصل بين العقد. لا تنسَ تحديثها إذا قررت لاحقًا تغيير اسم المستخدم الفائق/كلمة المرور/sslcert/sslkey!
6.  ستكتشف عقدة المنسق الرئيسية تلقائيًا العقد العاملة الرئيسية وتضيفها إلى جدول `pg_dist_node` باستخدام الدالة `citus_add_node()`.
7.  سيصون Patroni أيضًا `pg_dist_node` في حال حدوث تجاوز أعطال/تبديل على عناقيد المنسق أو العمال.

--------

## patronictl {#patronictl}

عناقيد المنسق والعمال هي عناقيد PostgreSQL/Patroni مختلفة فيزيائيًا مجمعة معًا منطقيًا فقط باستخدام امتداد قاعدة البيانات [Citus](https://github.com/citusdata/citus) لـ PostgreSQL. لذلك في معظم الحالات لا يمكن إدارتها ككيان واحد.

ينتج عن ذلك اختلافان رئيسيان في سلوك [patronictl](/ar/patroni/patronictl#patronictl) عندما يحتوي `patroni.yaml` على قسم [citus](/ar/patroni/citus#citus) مقارنة بالوضع المعتاد:

1.  يعرض أمرا `list` و`topology` افتراضيًا جميع أعضاء تشكيلة Citus (المنسقون والعمال). يشير العمود الجديد `Group` إلى مجموعة Citus التي ينتمون إليها.
2.  لجميع أوامر [patronictl](/ar/patroni/patronictl#patronictl) أُدخل خيار جديد باسم `--group`. لبعض الأوامر قد تؤخذ القيمة الافتراضية للمجموعة من `patroni.yaml`. مثلًا، سيمكّن [patronictl_pause](/ar/patroni/patronictl#patronictl_pause) وضع الصيانة افتراضيًا للمجموعة `group` المضبوطة في قسم [citus](/ar/patroni/citus#citus)، لكن مثلًا بالنسبة لـ [patronictl_switchover](/ar/patroni/patronictl#patronictl_switchover) أو [patronictl_remove](/ar/patroni/patronictl#patronictl_remove) يجب تحديد المجموعة صراحةً.

مثال على مخرجات [patronictl_list](/ar/patroni/patronictl#patronictl_list) لعنقود Citus:

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     1 | work1-2 | 172.27.0.2  | Leader         | running |  1 |             |     |            |     |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

إذا أضفنا خيار `--group`، فستتغير المخرجات إلى:

    postgres@coord1:~$ patronictl list demo --group 0
    + Citus cluster: demo (group: 0, 7179854923829112860) -+-------------+-----+------------+-----+
    | Member | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    | coord1 | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord2 | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    | coord3 | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    +--------+-------------+----------------+---------+----+-------------+-----+------------+-----+

    postgres@coord1:~$ patronictl list demo --group 1
    + Citus cluster: demo (group: 1, 7179854923881963547) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work1-1 | 172.27.0.8 | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    | work1-2 | 172.27.0.2 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+

--------

## تبديل عقد Citus العاملة {#citus-worker-switchover}

عند تنسيق تبديل لعقدة عاملة في Citus، يوفر Citus فرصة لجعل التبديل قريبًا من الشفافية بالنسبة للتطبيق. ولأن التطبيق يتصل بالمنسق، الذي يتصل بدوره بالعقد العاملة، فمن الممكن مع Citus إيقاف حركة SQL مؤقتًا على المنسق بالنسبة للأجزاء (shards) المستضافة على عقدة عاملة. يحدث التبديل بعد ذلك بينما تبقى الحركة موقفة على المنسق، وتُستأنف فور جاهزية عقدة عاملة رئيسية جديدة لقبول استعلامات القراءة والكتابة.

مثال على [patronictl_switchover](/ar/patroni/patronictl#patronictl_switchover) على عنقود العمال:

    postgres@coord1:~$ patronictl switchover demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    |     2 | work2-2 | 172.27.0.7  | Leader         | running |  1 |             |     |            |     |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    Citus group: 2
    Primary [work2-2]:
    Candidate ['work2-1'] []:
    When should the switchover take place (e.g. 2024-08-26T08:02 )  [now]:
    Current cluster topology
    + Citus cluster: demo (group: 2, 7179854924063375386) -+-------------+-----+------------+-----+
    | Member  | Host       | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    | work2-1 | 172.27.0.5 | Quorum Standby | running |  1 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    | work2-2 | 172.27.0.7 | Leader         | running |  1 |             |     |            |     |
    +---------+------------+----------------+---------+----+-------------+-----+------------+-----+
    Are you sure you want to switchover cluster demo, demoting current primary work2-2? [y/N]: y
    2024-08-26 07:02:40.33003 Successfully switched over to "work2-1"
    + Citus cluster: demo (group: 2, 7179854924063375386) --------+---------+------------+---------+
    | Member  | Host       | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+
    | work2-1 | 172.27.0.5 | Leader  | running |  1 |             |         |            |         |
    | work2-2 | 172.27.0.7 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
    +---------+------------+---------+---------+----+-------------+---------+------------+---------+

    postgres@coord1:~$ patronictl list demo
    + Citus cluster: demo ----------+----------------+---------+----+-------------+-----+------------+-----+
    | Group | Member  | Host        | Role           | State   | TL | Receive LSN | Lag | Replay LSN | Lag |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+
    |     0 | coord1  | 172.27.0.10 | Replica        | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord2  | 172.27.0.6  | Quorum Standby | running |  1 |   0/41C0368 |   0 |  0/41C0368 |   0 |
    |     0 | coord3  | 172.27.0.4  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-1 | 172.27.0.8  | Leader         | running |  1 |             |     |            |     |
    |     1 | work1-2 | 172.27.0.2  | Quorum Standby | running |  1 |   0/31D3198 |   0 |  0/31D3198 |   0 |
    |     2 | work2-1 | 172.27.0.5  | Leader         | running |  2 |             |     |            |     |
    |     2 | work2-2 | 172.27.0.7  | Quorum Standby | running |  2 |   0/31CDFC0 |   0 |  0/31CDFC0 |   0 |
    +-------+---------+-------------+----------------+---------+----+-------------+-----+------------+-----+

وهذا هو كيف يبدو الأمر من جانب المنسق:

    # The worker primary notifies the coordinator that it is going to execute "pg_ctl stop".
    2024-08-26 07:02:38,636 DEBUG: query(BEGIN, ())
    2024-08-26 07:02:38,636 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.7-demoted', 5432, 10000))
    # From this moment all application traffic on the coordinator to the worker group 2 is paused.

    # The old worker primary is assigned as a secondary.
    2024-08-26 07:02:40,084 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (7, '172.19.0.7', 5432, 10000))

    # The future worker primary notifies the coordinator that it acquired the leader lock in DCS and about to run "pg_ctl promote".
    2024-08-26 07:02:40,085 DEBUG: query(SELECT pg_catalog.citus_update_node(%s, %s, %s, true, %s), (3, '172.19.0.5', 5432, 10000))

    # The new worker primary just finished promote and notifies coordinator that it is ready to accept read-write traffic.
    2024-08-26 07:02:41,485 DEBUG: query(COMMIT, ())
    # From this moment the application traffic on the coordinator to the worker group 2 is unblocked.

--------

## العقد الثانوية {#secondary-nodes}

بدءًا من Patroni v4.0.0 تُسجَّل أيضًا عقد Citus الثانوية غير الحاملة لوسم [noloadbalance](/ar/patroni/config/yaml#tags_settings) في `pg_dist_node`. مع ذلك، لاستخدام العقد الثانوية لاستعلامات القراءة فقط تحتاج التطبيقات إلى تغيير GUC الخاص بـ [citus.use_secondary_nodes](https://docs.citusdata.com/en/latest/develop/api_guc.html#citus-use-secondary-nodes-enum).

--------

## نظرة داخل DCS {#peek-into-dcs}

يُخزن عنقود Citus (المنسق والعمال) في DCS كأسطول من عناقيد Patroni مجمعة معًا منطقيًا:

    /service/batman/              # scope=batman
    /service/batman/0/            # citus.group=0, coordinator
    /service/batman/0/initialize
    /service/batman/0/leader
    /service/batman/0/members/
    /service/batman/0/members/m1
    /service/batman/0/members/m2
    /service/batman/1/            # citus.group=1, worker
    /service/batman/1/initialize
    /service/batman/1/leader
    /service/batman/1/members/
    /service/batman/1/members/m3
    /service/batman/1/members/m4
    ...

اختير هذا الأسلوب لأنه مع معظم DCS يصبح من الممكن جلب عنقود Citus بأكمله بطلب قراءة تكراري واحد. فقط عقد منسق Citus تقرأ الشجرة كاملة، لأنها مضطرة لاكتشاف العقد العاملة. تقرأ العقد العاملة الشجرة الفرعية لمجموعتها الخاصة فقط، وفي بعض الحالات يمكنها قراءة الشجرة الفرعية لمجموعة المنسق.

--------

## Citus على Kubernetes {#citus-on-kubernetes}

بما أن Kubernetes لا يدعم البنى الهرمية اضطررنا إلى تضمين مجموعة citus في جميع كائنات K8s التي ينشئها Patroni:

    batman-0-leader  # the leader config map for the coordinator
    batman-0-config  # the config map holding initialize, config, and history "keys"
    ...
    batman-1-leader  # the leader config map for worker group 1
    batman-1-config
    ...

أي أن نمط التسمية هو: `${scope}-${citus.group}-${type}`.

تُكتشف جميع كائنات Kubernetes بواسطة Patroni باستخدام [منتقي التسميات](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors)، لذلك يجب أن تحمل جميع الـ Pods ذات Patroni&Citus وEndpoints/ConfigMaps تسميات تطابق منتقي التسميات المشترك، ويجب ضبط Patroni لاستخدامها عبر [إعدادات](/ar/patroni/config/yaml#kubernetes_settings) Kubernetes أو [متغيرات البيئة](/ar/patroni/config/env#kubernetes_environment).

بضعة أمثلة على تهيئة Patroni باستخدام متغيرات بيئة الـ Pods:

1.  لعنقود المنسق

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "0"
    citus-type: coordinator
    cluster-name: citusdemo
  name: citusdemo-0-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "0"
```

2.  لعنقود العمال من المجموعة 2

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: patroni
    citus-group: "2"
    citus-type: worker
    cluster-name: citusdemo
  name: citusdemo-2-0
  namespace: default
spec:
  containers:
  - env:
    - name: PATRONI_SCOPE
      value: citusdemo
    - name: PATRONI_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    - name: PATRONI_KUBERNETES_POD_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.podIP
    - name: PATRONI_KUBERNETES_NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
    - name: PATRONI_KUBERNETES_LABELS
      value: '{application: patroni}'
    - name: PATRONI_CITUS_DATABASE
      value: citus
    - name: PATRONI_CITUS_GROUP
      value: "2"
```

كما قد تكون لاحظت، كلا المثالين لديه تسمية `citus-group` مضبوطة. تتيح هذه التسمية لـ Patroni تحديد أن الكائن ينتمي إلى مجموعة Citus معينة. إضافة إلى ذلك، هناك أيضًا متغير البيئة `PATRONI_CITUS_GROUP`، الذي له القيمة نفسها كتسمية `citus-group`. عندما ينشئ Patroni كائنات Kubernetes جديدة من نوع ConfigMaps أو Endpoints، فإنه يضع عليها تلقائيًا تسمية `citus-group: ${env.PATRONI_CITUS_GROUP}`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: citusdemo-0-leader  # Is generated as ${env.PATRONI_SCOPE}-${env.PATRONI_CITUS_GROUP}-leader
  labels:
    application: patroni    # Is set from the ${env.PATRONI_KUBERNETES_LABELS}
    cluster-name: citusdemo # Is automatically set from the ${env.PATRONI_SCOPE}
    citus-group: '0'        # Is automatically set from the ${env.PATRONI_CITUS_GROUP}
```

يمكنك العثور على مثال كامل لنشر Patroni على Kubernetes مع دعم Citus في مجلد [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) من مستودع Patroni.

هناك ملفان مهمان لك:

1.  Dockerfile.citus
2.  citus_k8s.yaml

--------

## ترقيات Citus والترقيات الرئيسية لـ PostgreSQL {#citus-upgrades-and-postgresql-major-upgrades}

أولًا، يرجى قراءة المقال عن ترقية إصدار Citus في [الوثائق](https://docs.citusdata.com/en/latest/admin_guide/upgrading_citus.html). هناك تغيير طفيف واحد في العملية. عند تنفيذ الترقية، عليك استخدام [patronictl_restart](/ar/patroni/patronictl#patronictl_restart) بدلًا من `systemctl restart` لإعادة تشغيل PostgreSQL.

الترقية الرئيسية لـ PostgreSQL مع Citus أعقد قليلًا. سيكون عليك الجمع بين الأساليب المستخدمة في وثائق Citus حول الترقيات الرئيسية ووثائق Patroni حول [الترقية الرئيسية لـ PostgreSQL](/ar/patroni/existing_data#major_upgrade). يرجى أن تضع في اعتبارك أن عنقود Citus يتكون من العديد من عناقيد Patroni (المنسق والعمال) وكلها يجب ترقيتها بشكل مستقل.
