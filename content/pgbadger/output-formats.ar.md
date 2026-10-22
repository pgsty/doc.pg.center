---
title: "صيغ المخرجات"
linkTitle: "صيغ المخرجات"
weight: 70
description: "اختر مخرجات HTML أو نصية أو ثنائية أو JSON أو CSV خام وادمج الملفات الوسيطة"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [مرجع]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

يحدد pgBadger صيغة المخرجات من امتداد اسم الملف أو عبر `-x` / `--extension`. استخدم `-o` / `--outfile` أكثر من مرة لإنشاء عدة صيغ من التحليل نفسه.

| الصيغة | الامتداد المعتاد | الاستخدام الأنسب |
|---|---|---|
| HTML | `.html` | تقرير تفاعلي مقروء بشريًا مع رسوم بيانية |
| نص | `.txt` | مراجعة في الطرفية ومخرجات أرشيفية نصية بسيطة |
| ثنائي | `.bin` | إحصاءات وسيطة قابلة للدمج وإعادة بناء التقارير |
| JSON | `.json` | التكامل مع برامج أخرى؛ يتطلب `JSON::XS` |
| CSV خام | ملف المخرجات المحدد | استخراج موجه بالأسطر باستخدام `--dump-raw-csv` |

## HTML والنص {#html-and-text}

المخرجات الافتراضية هي `out.html`:

```console
$ pgbadger postgresql.log -o report.html
```

تضمّن مخرجات HTML عادة النصوص البرمجية والأنماط والخطوط وبيانات التقرير اللازمة للعرض المستقل. ينقل `-X` / `--extra-files` ملفات JavaScript وCSS المشتركة خارج التقارير التزايدية؛ أبقِ تلك الموارد بجوار شجرة ملفات HTML.

أنشئ مخرجات نصية صراحةً:

```console
$ pgbadger -x text -o report.txt postgresql.log
```

استخدم `-` اسمًا لملف المخرجات لكتابة صيغة مدعومة إلى المخرجات القياسية.

## البيانات الوسيطة الثنائية {#binary-format}

تفصل المخرجات الثنائية بين التحليل والعرض. أنشئ زيادات بالساعة من سجل يومي واحد آخذ في النمو:

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

ادمج ملفًا ثنائيًا واحدًا أو أكثر في تقرير جديد:

```console
$ pgbadger -o sunday.html sunday/*.bin
```

عندما يكتب الخادم ملف سجل واحدًا كل ساعة، أنشئ ملفًا ثنائيًا واحدًا لكل تدوير، ثم أعد بناء HTML التراكمي كلما لزم الأمر:

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

احتفظ بالملفات الثنائية من إصدارات pgBadger المتوافقة معًا. راجع ملاحظات الإصدار بشأن توافق صيغة التقارير التزايدية قبل ترقية دليل تقارير قديم وطويل الأمد.

## JSON {#json-format}

مخرجات JSON مخصصة للمستهلكين البرمجيين مثل خطوط المراقبة أو إعداد التقارير:

```console
$ pgbadger -o report.json postgresql.log
```

ثبِّت `JSON::XS` أولًا. أضف `--prettify-json` لتحسين قابلية القراءة عندما يكون حجم الملف وزمن التوليد أمرين ثانويين.

## التصديرات الخام والموجهة للاستعلامات {#raw-exports}

يوفر مرجع الأوامر أيضًا تصديرات متخصصة:

- يحلل `--dump-raw-csv` السجل ويكتب CSV موجهًا بالأسطر دون بناء تقرير؛
- يغير `--csv-separator` محدد CSV الخام، الذي تكون قيمته الافتراضية فاصلة في الإصدار 13.2؛
- يُصدر `--dump-all-queries` كل استعلام بعد استبدال معاملات الربط؛
- يكتب `--normalized-only` الاستعلامات الموحَّدة نمطيًا؛
- يضيف `--query-numbering` ترقيمًا إلى المخرجات النصية الموجهة للاستعلامات.

قد تحتوي هذه الأوضاع على SQL خاص بالتطبيق، أو معرفات، أو مستخدمين، أو عناوين عملاء، أو قيمًا حرفية. راجع المخرجات قبل مشاركتها واستخدم `--anonymize` عندما لا يتطلب التحليل المقصود قيمًا حرفية.

