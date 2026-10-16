---
title: "التقارير التزايدية"
linkTitle: "التقارير التزايدية"
weight: 60
description: "أنشئ تقارير يومية وأسبوعية، وتحكم في مدة الاحتفاظ، وأعد بناء المخرجات، وأضف ملخصات شهرية"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [مهمة]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

يخزّن الوضع التزايدي الإحصاءات المحلَّلة في صورة ثنائية، ثم يبني تقرير HTML واحدًا لكل يوم، وتقريرًا تراكميًا لكل أسبوع، وفهرسًا بنمط التقويم يربط بينها. وهو مخصص للمعالجة المتكررة للسجلات المُداورة دون عدّ الإدخالات نفسها مرة أخرى.

## إنشاء التقارير اليومية والأسبوعية {#daily-and-weekly}

شغِّل pgBadger بعد تدوير السجل اليومي وحدد دليل مخرجات دائمًا:

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

يفعّل `-I` الوضع التزايدي ويحدد `-O` الدليل الذي يحتوي على الحالة الثنائية وفهرس التقويم والتقارير المولدة. يحتفظ pgBadger بحالته التزايدية الخاصة في ذلك الدليل، لذا لا حاجة إلى `--last-parsed` إلا إذا أردت عمدًا وضع ملف الحالة في مكان آخر.

استخدم دليل HTML منفصلًا مع الاحتفاظ بالحالة الثنائية في الدليل الأصلي:

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

تعامل مع الملفات الثنائية بوصفها بيانات مصدرية لإعادة البناء مستقبلًا. أنشئ لها نسخًا احتياطية أو احتفظ بالسجلات الأصلية إذا كانت إعادة توليد التقارير أمرًا مهمًا.

## مدة الاحتفاظ {#retention}

احتفظ بعدد محدد من الأسابيع فقط:

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

تُحذف أدلة الأسابيع والأيام الأقدم تلقائيًا. اختبر السياسة على نسخة غير تشغيلية قبل تفعيلها على سجل تقاريرك الوحيد.

## كتابة الموارد المشتركة بشكل منفصل {#shared-assets}

بشكل افتراضي، تضمّن تقارير HTML ملفات JavaScript وCSS الخاصة بها. في دليل يحتوي على تقارير تزايدية كثيرة، يكتب `-X` / `--extra-files` الموارد المشتركة بشكل منفصل ويقلل المخرجات المكررة:

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

يجب نقل جميع التقارير مع دليل الموارد المُرقَّم بالنسخة الخاص بها معًا.

## إعادة بناء التقارير القائمة {#rebuild}

بعد ترقية pgBadger أو تطبيق إصلاح متعلق بتوليد التقارير، أعد بناء HTML من البيانات الثنائية المحتفظ بها:

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

استخدم `-E` / `--explode` مرة أخرى إذا كانت التقارير الأصلية قد وُلِّدت لكل قاعدة بيانات على حدة.

> استخدم الخيار الطويل `--rebuild`. في مرجع الأوامر الحالي، يعني `-R` الخيار `--retention`؛ والتعامل مع `-R` بوصفه اختصارًا لإعادة البناء سيطبّق الخيار الخطأ.

## إضافة تقرير شهري {#monthly-reports}

التقارير اليومية والأسبوعية تلقائية. أما التجميع الشهري فيكون صريحًا لأنه قد يكون مكلفًا مع سجل تقارير طويل:

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

يضاف الشهر المولَّد إلى فهرس التقويم. وإعادة تشغيل الأمر تعيد بناء ذلك الشهر من البيانات الثنائية المتاحة. للحصول على السجل لكل قاعدة بيانات على حدة، كرر `-E`:

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

يوفر مرجع الأوامر الكامل أيضًا `--day-report YYYY-MM-DD` و`--no-week` و`--noreport` و`--start-monday` و`--iso-week-number` لجداول تشغيل أكثر تخصصًا.

افتح [مثال التقرير التزايدي المرفق](/third_party/pgbadger/examples/report/index.html) لفحص التقويم وروابط الأسابيع وتسلسل التقارير اليومية دون اتصال بالشبكة.

