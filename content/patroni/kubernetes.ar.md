---
title: "استخدام Patroni مع Kubernetes"
linkTitle: "الاستخدام مع Kubernetes"
weight: 120
icon: fas fa-dharmachakra
description: "استخدام Patroni مع كائنات Kubernetes والتسميات واكتشاف الخدمات."
module: [PATRONI]
categories: [مهمة]
upstream_link: "https://patroni.readthedocs.io/en/latest/kubernetes.html"
---

<a id="kubernetes"></a>
يمكن لـ Patroni استخدام كائنات Kubernetes من أجل تخزين حالة العنقود وإدارة مفتاح القائد. وهذا يجعله قادرًا على تشغيل Postgres في بيئة Kubernetes دون أي مخزن للاتساق، أي دون الحاجة إلى تشغيل نشر Etcd إضافي. هناك نوعان مختلفان من كائنات Kubernetes يمكن لـ Patroni استخدامهما لتخزين مفتاح القائد ومفاتيح التهيئة، ويُحدد نوع الكائن عبر خيار التهيئة `kubernetes.use_endpoints` أو متغير البيئة `PATRONI_KUBERNETES_USE_ENDPOINTS`.

--------

## استخدام Endpoints {#use-endpoints}

رغم أن هذا هو الوضع الموصى به، فإنه معطل افتراضيًا لأسباب تتعلق بالتوافق. عندما يكون ممكنًا، يخزن Patroni تهيئة العنقود ومفتاح القائد في حقول `metadata: annotations` الخاصة بالكائن `Endpoints` المعني الذي ينشئه. تغيير القائد أكثر أمانًا مما هو عليه عند استخدام `ConfigMaps`، إذ تُحدَّث في عملية واحدة التعليقات التوضيحية (annotations) الحاوية لمعلومات القائد والعناوين الفعلية المشيرة إلى pod القائد قيد التشغيل.

--------

## استخدام ConfigMaps {#use-configmaps}

في هذا الوضع، سينشئ Patroni كائنات ConfigMaps بدلًا من Endpoints ويخزن المفاتيح داخل البيانات الوصفية لتلك الكائنات. ويستغرق تغيير القائد تحديثين على الأقل: أحدهما للكائن ConfigMap الخاص بالقائد والآخر للكائن Endpoint المقابل.

لتوجيه حركة البيانات إلى قائد Postgres عليك تهيئة خدمة Postgres في Kubernetes لتستخدم منتقي التسمية (label selector) مع `role_label` (المضبوط في تهيئة patroni).

لاحظ أنه في بعض الحالات، مثلًا عند التشغيل على OpenShift، لا بديل عن استخدام ConfigMaps.

--------

## التهيئة {#configuration}

تُوصف [الإعدادات](/ar/patroni/config/yaml#kubernetes_settings) الخاصة بـ Patroni في Kubernetes و[متغيرات البيئة](/ar/patroni/config/env#kubernetes_environment) في الفصول العامة من الوثائق.

<a id="kubernetes_role_values"></a>

### تخصيص تسمية الدور {#customize-role-label}

افتراضيًا، سيضبط Patroni التسميات المناسبة على الـ pod الذي يعمل فيه بناءً على دور العقدة، مثل `role=primary`. يمكن تخصيص مفتاح التسمية وقيمتها عبر `kubernetes.role_label` و`kubernetes.leader_label_value` و`kubernetes.follower_label_value` و`kubernetes.standby_leader_label_value`.

لاحظ أنه إذا انتقلت من تسميات الدور الافتراضية إلى تسميات مخصصة، فيمكنك تقليل زمن التوقف باتباع خطوات الترحيل التالية:

1.  أضف تسمية مؤقتة تستخدم قيمة الدور الأصلية للـ pod عبر `kubernetes.tmp_role_label` (مثل `tmp_role`). بمجرد إعادة تشغيل الـ pods ستحصل على التسميات التالية التي يضبطها Patroni:

> ```yaml
> labels:
>   cluster-name: foo
>   role: primary
>   tmp_role: primary
> ```

2.  بعد تحديث جميع الـ pods، عدّل منتقي الخدمة ليختار التسمية المؤقتة.

> ```yaml
> selector:
>   cluster-name: foo
>   tmp_role: primary
> ```

3.  أضف تسمية الدور المخصصة لديك (مثلًا اضبط `kubernetes.leader_label_value=leader`). بمجرد إعادة تشغيل الـ pods ستحصل على التسميات الجديدة التالية التي يضبطها Patroni:

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
>   tmp_role: primary
> ```

4.  بعد تحديث جميع الـ pods مجددًا، عدّل منتقي الخدمة ليستخدم قيمة الدور الجديدة.

> ```yaml
> selector:
>   cluster-name: foo
>   role: leader
> ```

5.  أخيرًا، أزل التسمية المؤقتة من تهيئتك وحدّث جميع الـ pods.

> ```yaml
> labels:
>   cluster-name: foo
>   role: leader
> ```

--------

## أمثلة {#examples}

- يحتوي مجلد [kubernetes](https://github.com/patroni/patroni/tree/master/kubernetes) في مستودع Patroni على أمثلة لصورة Docker وعلى بيان Kubernetes (manifest) لاختبار إعداد Patroni على Kubernetes. لاحظ أنه في حالته الحالية لن يكون قادرًا على استخدام PersistentVolumes بسبب مشكلات الأذونات.
- يمكنك العثور على صورة Docker الكاملة الميزات القادرة على استخدام Persistent Volumes في [مشروع Spilo](https://github.com/zalando/spilo).
- يوجد أيضًا [Helm chart](https://github.com/kubernetes/charts/tree/master/incubator/patroni) لنشر صورة Spilo المهيأة مع تشغيل Patroni باستخدام Kubernetes.
- لتشغيل عناقيد قواعد البيانات على نطاق واسع باستخدام Patroni وSpilo، ألقِ نظرة على مشروع [postgres-operator](https://github.com/zalando/postgres-operator). يطبق هذا المشروع نمط المشغّل (operator) لإدارة عناقيد Spilo.
