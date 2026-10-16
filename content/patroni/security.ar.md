---
title: "اعتبارات الأمان"
weight: 160
icon: fa-solid fa-lock
description: "اعتبارات الأمان الخاصة بـ DCS وREST API والتعامل مع بيانات الاعتماد."
module: [PATRONI]
categories: [مفهوم]
upstream_link: "https://patroni.readthedocs.io/en/latest/security.html"
---

<a id="security"></a>
لعنقود Patroni واجهتان ينبغي حمايتهما من الوصول غير المصرح به: مخزن الإعداد الموزع (DCS) وواجهة REST API الخاصة بـ Patroni.

--------

## حماية DCS {#protecting-dcs}

يخزّن كلٌّ من Patroni و[patronictl](/ar/patroni/patronictl#patronictl) البيانات في DCS ويسترجعانها منه.

وحتى عندما لا يحتوي DCS على أي معلومات حساسة، فإنه يسمح بتغيير بعض إعداد Patroni/Postgres. ولذلك فإن أول ما ينبغي حمايته هو DCS نفسه.

وتعتمد تفاصيل الحماية على نوع DCS المستخدم. وتغطى معاملات المصادقة والتشفير (الرموز/المصادقة الأساسية/شهادات العميل) لأنواع DCS المدعومة في [الإعدادات](/ar/patroni/config/yaml#yaml).

والتوصية العامة هي تفعيل TLS لجميع اتصالات DCS.

--------

## حماية REST API {#protecting-the-rest-api}

حماية REST API مهمة أكثر تعقيدًا.

تُستخدم واجهة REST API الخاصة بـ Patroni من قبل Patroni نفسه أثناء سباق القيادة، ومن قبل أداة [patronictl](/ar/patroni/patronictl#patronictl) لتنفيذ عمليات تجاوز الأعطال/التبديل/إعادة التهيئة/إعادة التشغيل/إعادة التحميل، ومن قبل HAProxy أو أي موازن حمل آخر لإجراء فحوص الصحة عبر HTTP، وبالطبع يمكن أيضًا استخدامها للمراقبة.

من منظور الأمان، تحتوي REST API على نقاط نهاية آمنة (طلبات `GET`، لاسترجاع المعلومات فقط) ونقاط نهاية غير آمنة (طلبات `PUT` و`POST` و`PATCH` و`DELETE`، تغيّر حالة العقد).

يمكن حماية نقاط النهاية غير الآمنة بالمصادقة الأساسية HTTP عبر ضبط المعاملين `restapi.authentication.username` و`restapi.authentication.password`. ولا توجد طريقة لحماية نقاط النهاية الآمنة دون تفعيل TLS.

عندما يكون TLS لواجهة REST API مفعلًا وتكون البنية التحتية للمفاتيح العامة (PKI) منشأة، تصبح المصادقة المتبادلة بين خادم API وعميل API ممكنة لجميع نقاط النهاية.

تُفعّل معاملات قسم `restapi` مصادقة عميل TLS تجاه الخادم. وبحسب قيمة المعامل `verify_client`، يشترط خادم API نجاح التحقق من شهادة العميل لكلٍّ من استدعاءات API الآمنة وغير الآمنة (`verify_client: required`)، أو لاستدعاءات API غير الآمنة فقط (`verify_client: optional`)، أو لا يشترطها لأي استدعاءات API (`verify_client: none`).

تُفعّل معاملات قسم `ctl` مصادقة خادم TLS تجاه العميل (أداة [patronictl](/ar/patroni/patronictl#patronictl) التي تستخدم الإعداد نفسه الذي يستخدمه patroni). اضبط `insecure: true` لتعطيل التحقق من شهادة الخادم من قبل العميل. راجع [الإعدادات](/ar/patroni/config/yaml#patronictl_settings) لوصف تفصيلي لمعاملات عميل TLS.

أما حماية قاعدة بيانات PostgreSQL نفسها من الوصول غير المصرح به فتقع خارج نطاق هذا المستند، وتغطى في <https://www.postgresql.org/docs/current/client-authentication.html>
