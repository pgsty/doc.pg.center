---
title: "توثيق etcd 3.7"
linkTitle: "etcd 3.7"
description: "أدلة etcd 3.7 الرسمية للمطورين والمشغّلين، والترقيات، وواجهات API، والبنية الداخلية."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd-20261121
categories: [مفهوم]
search_keywords: [v3.7.4, "Go 1.26.11", force-new-cluster, NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7"
cascade:
  upstream_source: etcd-20261121
  type: docs
  module: [ETCD]
---

etcd هو مخزن مفاتيح-قيم موزّع ذو اتساق قوي. تغطي هذه الأدلة تثبيت etcd وتشغيله، وبناء التطبيقات
استنادًا إلى واجهات API الخاصة به، وفهم تصميمه، وقياس الأداء، وترقية العناقيد أو خفض إصدارها ضمن خط
الإصدار 3.7.

ابدأ بـ [البدء السريع](/ar/etcd/quickstart/) لعنقود محلي أحادي العضو، أو [التثبيت](/ar/etcd/install/) لمسارات
التثبيت المدعومة، أو [دليل العمليات](/ar/etcd/op-guide/) لعمليات النشر الإنتاجية.

## etcd v3.7.4 {#etcd-v3-7-4}

إصدار الصيانة الحالي هو [v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4)، المنشور في 19 نوفمبر 2026. تستهدف أمثلة التثبيت وDocker وKubernetes في هذه النسخة هذا الإصدار.

- يصلح الاستعادة باستخدام `--force-new-cluster` عندما يكون الفهرس المتسق للواجهة الخلفية متقدمًا على WAL.
- يستخدم مؤشرًا ذريًا لمخزن الإنذارات لتجنب حالة تسابق.
- يصلح حالات panic عند البدء أثناء إعادة تشغيل مدخلات WAL القديمة لسمات الأعضاء في v2.
- يُبنى باستخدام Go 1.26.11.

راجع [سجل التغييرات الثابت في المنبع](https://github.com/etcd-io/etcd/blob/1ce5a2b779143279c89ed8c7e33a42e51fb697fa/CHANGELOG/CHANGELOG-3.7.md#v374-tbc). لا يزال عنوانه يقول «TBC»؛ ووسم الإصدار المنشور يثبت توفره.

## etcd v3.7.3 {#etcd-v3-7-3}

كان إصدار الصيانة السابق هو [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3).

- يصلح حالات تسابق البيانات بين `Hash` و`Restore` في مخزن MVCC وفي عمليات `RangeStream` التي تُعيد المفاتيح فقط، إضافةً إلى تراجع في أداء النسخ المتماثل سببه إرسال القائد رسائل `MsgApp` بترتيب معكوس.
- يُبنى باستخدام Go 1.26.10، ويُحدّث اعتماديات OpenTelemetry و`golang.org/x/net` لمعالجة المشكلات الأمنية المُبلّغ عنها.
- يعلن إهمال `NewJournalWriter` في `client/pkg/v3/logutil`، مع التخطيط لإزالته في v3.8.

راجع [سجل التغييرات في المشروع الأصلي](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22) للاطلاع على جميع التغييرات.
