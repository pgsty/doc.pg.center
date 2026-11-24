---
title: "توثيق pgBadger 13.3"
linkTitle: pgBadger
weight: 40
description: "تحليل سريع لسجلات PostgreSQL وPgBouncer مع تقارير مفصلة مكتفية ذاتيًا"
search_keywords: [csvlog, jsonlog, logplex, stderr, syslog]
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [مفهوم]
aliases: [/pgbadger/documentation/]
upstream_source: pgbadger-20261121
upstream_ref: "v13.3"
upstream_link: "https://github.com/darold/pgbadger/tree/0514893e97296695c77755fa36c59288c3afef3e"
cascade:
  upstream_source: pgbadger-20261121
  upstream_ref: "v13.3"
  type: docs
  module: [PGBADGER]
---

يغطي هذا الدليل [pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3) الصادر في 3 نوفمبر 2026. يتضمن الإصدار التصفية على المضيف البعيد في وضع المراقبة، وترميز أدلة التقارير الخاصة بكل قاعدة بيانات، وسلاسل الرسوم البيانية القابلة للتمرير، والإصلاحات المدرجة في [ملاحظات إصدار 13.3](/ar/pgbadger/releases/13/#v13-3).

![شعار pgBadger](/img/pgbadger/logo.png "pgBadger")

**pgBadger** هو محلِّل سجلات PostgreSQL سريع ومستقل، مكتوب بلغة Perl. يقرأ سجلات PostgreSQL أو PgBouncer وينتج مخرجات مفصلة بصيغة HTML أو نص أو ملفات ثنائية أو JSON أو CSV خام. وتكون تقارير HTML مكتفية ذاتيًا وتفاعلية وقابلة للتقريب، ولا تحتاج إلى سوى متصفح ويب لعرضها.

## لماذا pgBadger {#why-pgbadger}

صُمم pgBadger للسجلات الكبيرة وللاستخدام التشغيلي:

- برنامج Perl واحد، دون أي وحدات Perl إلزامية خارج النواة؛
- كشف تلقائي لمدخلات `stderr` و`syslog` و`csvlog` و`jsonlog` وRDS وCloud SQL وlogplex وRedshift وPgBouncer؛
- قراءة مباشرة للملفات المحلية والمدخل القياسي والملفات البعيدة عبر SSH، وعناوين URL ببروتوكول HTTP أو FTP أو SFTP؛
- دعم المدخلات المضغوطة بـ gzip أو bzip2 أو lz4 أو xz أو zip أو zstd؛
- تحليل متوازٍ لملف واحد كبير أو لعدد كبير من الملفات الأصغر؛
- تقارير تزايدية يومية وأسبوعية وشهرية عند الطلب؛
- تصفية حسب الوقت وقاعدة البيانات والمستخدم والعميل والتطبيق والعملية والجلسة ونمط الاستعلام.

## ماذا تحتوي التقارير {#report-coverage}

تغطي مجموعة تقارير PostgreSQL ما يلي:

- النشاط العام وإحصاءات الاستعلامات؛
- الاستعلامات البطيئة والمتكررة والمستهلكة للوقت والمنتظرة والملغاة؛
- الملفات المؤقتة ونقاط التحقق (checkpoints) والأقفال والجلسات والاتصالات؛
- نشاط autovacuum وautoanalyze حسب الجدول؛
- الأخطاء والأحداث حسب درجة الشدة والفئة؛
- التوزيعات حسب قاعدة البيانات والمستخدم والعميل والتطبيق ونوع العبارة.

تضيف مدخلات PgBouncer تقارير عن معدل النقل ومتوسط مدة الاستعلام والجلسات المتزامنة وتوزيعات الاتصالات والجلسات واستخدام المجمِّع المحجوز، بالإضافة إلى تقارير الأخطاء/الأحداث المتكررة.

## خريطة التوثيق {#documentation-map}

اقرأ الدليل بهذا الترتيب، أو استخدم الشريط الجانبي للانتقال مباشرة إلى مهمة محددة:

1. [نزِّل وثبِّت](/ar/pgbadger/download/) pgBadger ووحداته الاختيارية.
2. راجع [مرجع سطر الأوامر](/ar/pgbadger/command-line/) الكامل.
3. تهيئة [تسجيل PostgreSQL](/ar/pgbadger/postgresql-logging/) ببادئة قابلة للتحليل.
4. اختر وضع [المعالجة المتوازية](/ar/pgbadger/parallel-processing/) المناسب.
5. أنشئ [التقارير التزايدية](/ar/pgbadger/incremental-reports/) بأمان.
6. حدد [صيغة مخرجات](/ar/pgbadger/output-formats/) وافحص [الأمثلة المحلية](/ar/pgbadger/sample-reports/).
7. تابع [سجل الإصدارات](/ar/pgbadger/releases/) و[الدعم](/ar/pgbadger/support/) و[الترخيص](/ar/pgbadger/license/).

## روابط المشروع الأصلي {#upstream-links}

- [موقع المشروع](https://pgbadger.darold.net/)
- [الكود المصدري](https://github.com/darold/pgbadger)
- [الإصدارات](https://github.com/darold/pgbadger/releases)
- [متتبع المشكلات](https://github.com/darold/pgbadger/issues)
