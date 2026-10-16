---
title: "التنزيل والتثبيت"
linkTitle: "التنزيل والتثبيت"
weight: 20
description: "الإصدارات الرسمية، والحزم، والمتطلبات، والتثبيت من المصدر"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [درس تعليمي]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## اختر قناة التوزيع {#distribution-channels}

| القناة | تُستخدم من أجل | الموقع |
|---|---|---|
| إصدار رسمي | أرشيفات المصدر وملاحظات الإصدار | [إصدارات GitHub](https://github.com/darold/pgbadger/releases) |
| حزمة RPM | توزيعات Linux المعتمدة على RPM | [مستودع PostgreSQL لـ Yum](https://yum.postgresql.org/packages/) |
| حزمة Debian/Ubuntu | توزيعات Linux المعتمدة على APT | [مستودع PostgreSQL لـ Apt](https://wiki.postgresql.org/wiki/Apt) |
| المصدر التطويري | الكود الحالي غير المُصدر بعد | [darold/pgbadger](https://github.com/darold/pgbadger) |

تستخدم أمثلة التثبيت pgBadger 13.2. راجع صفحة الإصدارات قبل اختيار إصدار معين.

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
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

قد يحتوي الكود التطويري على تغييرات لم تشملها ملاحظات الإصدار بعد. فضِّل أرشيفًا موسومًا بوسم إصدار للحصول على تغليف إنتاجي قابل للتكرار.

## التحقق من التثبيت {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

تابع مع [مرجع سطر الأوامر](/ar/pgbadger/command-line/) و[تهيئة تسجيل PostgreSQL](/ar/pgbadger/postgresql-logging/).
