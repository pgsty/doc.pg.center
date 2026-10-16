---
title: "الدعم والمساهمة"
linkTitle: "الدعم"
weight: 100
description: "الإبلاغ عن الأخطاء، وطلب الميزات، والمساهمة بالرقع، والعثور على دعم PostgreSQL احترافي"
search_keywords: [--help, help]
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [مهمة]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

تُصان pgBadger كمشروع مفتوح. تُعالَج تقارير الأخطاء ومقترحات الميزات وإصلاحات التوثيق والرقع عبر مستودع GitHub الخاص بالمشروع الأصلي.

## الأخطاء وطلبات الميزات {#bugs-and-features}

1. ترقَّ إلى أحدث إصدار منشور وتأكد من أن السلوك لا يزال يحدث.
2. ابحث في [المشكلات المفتوحة](https://github.com/darold/pgbadger/issues) و[المشكلات المغلقة](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed) عن إجابة موجودة.
3. اختزل المشكلة إلى أصغر عيّنة آمنة من ملف السجل وسطر أوامر لا يزالان يعيدان إنتاجها.
4. احذف بيانات الاعتماد واستعلامات SQL الحساسة وقيم الربط وأسماء المضيفين والعناوين وبيانات الأعمال.
5. افتح [مشكلة جديدة](https://github.com/darold/pgbadger/issues/new) مع ذكر إصدار pgBadger ونظام التشغيل وصيغة الإدخال والخيارات الدقيقة والنتيجة الملاحظة والنتيجة المتوقعة.

في حالات الانهيار أو أخطاء المحلل، أدرج فقط الحد الأدنى من أسطر السجل المنقّحة اللازمة لإعادة إنتاج الحالة الحدية. نادرًا ما يكون سجل إنتاج كامل أو تقرير مولَّد مناسبًا لمشكلة علنية.

## المساهمة برقعة {#contribute-a-patch}

يتضمن المشروع ملف `.editorconfig` لضمان تباعد متسق. حافظ على مواءمة مساعدة الأوامر وتوثيق POD وتوثيق Markdown المولَّد عندما يؤثر تغيير ما على سلوك مرئي للمستخدم.

سير عمل التوثيق في المشروع الأصلي هو:

```console
$ perl Makefile.PL
$ make README
```

الملف `doc/pgBadger.pod` هو المصدر الأساسي للتوثيق المطوَّل. يوفّر `pgbadger --help` الملخص، بينما ملفات README عروض مولَّدة. شغّل الاختبارات ذات الصلة قبل تقديم طلب سحب (pull request).

- [المستودع المصدري](https://github.com/darold/pgbadger)
- [طلبات السحب](https://github.com/darold/pgbadger/pulls)
- [دليل المساهمة](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [ملاحظات التطوير](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## الدعم التجاري {#commercial-support}

لا يعد مشروع pgBadger بصيانة أو دعم بموجب ترخيصه. للحصول على مساعدة مدفوعة بشأن تسجيل PostgreSQL أو تحليل الأداء أو أتمتة التقارير، راجع [دليل خدمات PostgreSQL الاحترافية](https://www.postgresql.org/support/professional_support/).

