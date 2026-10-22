---
title: "التنزيل والتثبيت"
linkTitle: "التنزيل والتثبيت"
weight: 20
description: "الإصدارات الرسمية، والحزم، والمتطلبات، والتثبيت من المصدر"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [درس تعليمي]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

## اختر قناة التوزيع {#distribution-channels}

| القناة | تُستخدم من أجل | الموقع |
|---|---|---|
| إصدار رسمي | أرشيفات المصدر وملاحظات الإصدار | [إصدارات GitHub](https://github.com/darold/pgbadger/releases) |
| حزمة RPM | توزيعات Linux المعتمدة على RPM | [مستودع PostgreSQL لـ Yum](https://yum.postgresql.org/packages/) |
| حزمة Debian/Ubuntu | توزيعات Linux المعتمدة على APT | [مستودع PostgreSQL لـ Apt](https://wiki.postgresql.org/wiki/Apt) |
| المصدر التطويري | الكود الحالي غير المُصدر بعد | [darold/pgbadger](https://github.com/darold/pgbadger) |

أحدث إصدار مستقر جرى التحقق منه في 2026-10-23 هو [pgBadger 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2)، الصادر في 2025-12-29. يثبّت المثال أدناه، الذي يستخدم أرشيف الإصدار، هذه النسخة. يغطي هذا الدليل أيضًا لقطة تطوير غير منشورة؛ استخدم أمر الانتقال إلى الالتزام المحدد أدناه لإعادة إنتاج سلوكها الأحدث.

## المتطلبات {#requirements}

لا يحتاج مسار تقارير HTML إلى سوى:

- توزيعة Perl حديثة؛
- متصفح ويب لعرض الرسوم البيانية بـ JavaScript المضمّنة.

تضيف القدرات الاختيارية التبعيات التالية:

| القدرة | التبعية |
|---|---|
| تحليل سجلات CSV الخاصة بـ PostgreSQL | `Text::CSV_XS` |
| كتابة مخرجات JSON | `JSON::XS` |
| قراءة مدخلات `.gz` أو `.bz2` أو `.lz4` أو `.xz` أو `.zip` أو `.zst` | الأداة المقابلة: `zcat` أو `bzcat` أو `lz4cat` أو `xz` أو `unzip` أو `zstdcat` |

ثبِّت دعم JSON على Debian أو Ubuntu:

```console
$ sudo apt-get install libjson-xs-perl
```

على نظام معتمد على RPM:

```console
$ sudo yum install perl-JSON-XS
```

استخدم `--zcat` لتجاوز مسار أداة فك الضغط. يؤدي تقديم أمر مخصص واحد إلى تعطيل خلط صيغ ضغط مختلفة في الاستدعاء نفسه.

يجب أن تدعم أداة `xz` الخيار `--robot` ليتمكن pgBadger من قراءة البيانات الوصفية للأرشيف. واضغط سجلات lz4 باستخدام `--content-size` ليتمكن pgBadger من تحديد حجمها غير المضغوط.

## التثبيت من أرشيف رسمي {#install-from-tarball}

نزِّل أرشيف إصدار، ثم ابنِه وثبِّته باستخدام سلسلة أدوات Perl القياسية:

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

يثبِّت التخطيط الافتراضي `site` البرنامج بالمسار `/usr/local/bin/pgbadger` وصفحة الدليل بالمسار `/usr/local/share/man/man1/pgbadger.1`.

للحصول على تثبيت بنمط توزيعات النظام تحت `/usr`، أنشئ ملف Makefile باستخدام:

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

التخطيط `INSTALLDIRS=perl` تخطيط آخر يدعمه المشروع الأصلي. افحص المسارات المولَّدة قبل التثبيت في نظام مُدار.

## تثبيت الكود التطويري {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach f373ac678c756f66a785c5ab4773d1f05f468d67
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

تطابق نسخة الكود هذه لقطة التطوير غير المنشورة الموثقة هنا: [`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67)، التي سُجّل التزامها في 2026-10-21 (UTC). وهي أحدث من الإصدار المستقر 13.2، لكنها ليست إصدارًا مستقرًا جديدًا. قد يحتوي الكود التطويري على تغييرات لم تشملها ملاحظات الإصدار بعد؛ فضِّل أرشيفًا موسومًا بوسم إصدار عند إعداد حزم لبيئة الإنتاج.

## التحقق من التثبيت {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

تابع مع [مرجع سطر الأوامر](/ar/pgbadger/command-line/) و[تهيئة تسجيل PostgreSQL](/ar/pgbadger/postgresql-logging/).
