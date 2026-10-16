---
title: "توثيق PgBouncer 1.26.0"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer - مجمِّع اتصالات خفيف الوزن لـ PostgreSQL
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [مفهوم]
upstream_source: pgbouncer
upstream_ref: v1.26.0
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  upstream_ref: v1.26.0
  type: docs
  module: [PGBOUNCER]
---

يستند هذا الدليل إلى [PgBouncer 1.26.0](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0)، الصادر في 2026-09-23. راجع [ملاحظات الإصدار](/ar/pgbouncer/changelog/#pgbouncer-126x) للاطلاع على التغييرات عن الإصدارات السابقة.

**pgbouncer** هو مجمِّع اتصالات لـ PostgreSQL. يمكن ربط أي تطبيق
هدف بـ **pgbouncer** وكأنه خادم PostgreSQL،
وسينشئ **pgbouncer** اتصالًا بالخادم الفعلي، أو
سيعيد استخدام أحد اتصالاته الموجودة.

الهدف من **pgbouncer** هو تقليل الأثر على الأداء الناتج عن فتح
اتصالات جديدة بـ PostgreSQL.

حرصًا على عدم المساس بدلالات المعاملات عند تجميع
الاتصالات، يدعم **pgbouncer** عدة أنواع من التجميع عند
تدوير الاتصالات:

- **تجميع الجلسات**: الأسلوب الأكثر لباقة. عندما يتصل عميل، سيُخصَّص له اتصال خادم طوال المدة التي يبقى فيها العميل متصلًا. وعندما ينقطع اتصال العميل، يُعاد اتصال الخادم إلى المجمّع. هذا هو الأسلوب الافتراضي.
- **تجميع المعاملات**: يُخصَّص اتصال خادم للعميل فقط أثناء معاملة واحدة. وعندما يلاحظ PgBouncer أن المعاملة قد انتهت، يُعاد اتصال الخادم إلى المجمّع.
- **تجميع العبارات**: الأسلوب الأكثر عدوانية. يُعاد اتصال الخادم إلى المجمّع فور اكتمال استعلام. المعاملات متعددة العبارات غير مسموح بها في هذا الوضع.
