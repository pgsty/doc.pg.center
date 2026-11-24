---
title: "الإسناد والتراخيص"
linkTitle: "الإسناد"
description: "من أين تأتي كل صفحة في هذا الموقع، ومن يملك حقوقها، وأي ترخيص تحمله، وأين تُحفظ الإشعارات الكاملة."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

يعيد PG.CENTER نشر توثيق كتبه ستة مشاريع أصلية. تحمل كل صفحة توثيق في نهايتها سطر إسناد
يذكر العمل المشتق منه، وصاحب حقوقه، وترخيصه، ورابطًا إلى قسم هذه الصفحة الذي يغطيه.

هذه الصفحة هي ذلك السجل. تبيّن ما استُورد، ومتى، ومن أي مراجعة مثبّتة، وتحت أي ترخيص،
وأين يُحفظ الإشعار الأصلي الكامل.

> [!NOTE]
> PG.CENTER مشروع توثيقي مجتمعي مستقل. لا ينتسب إلى أي من المشاريع أدناه ولا يحظى
> بتأييد منها، وليس نشرة رسمية عنها ولا عن PostgreSQL Global Development Group.

## الملخص {#summary}

تتضمن أدلة التشغيل الستة في هذه الطبعة تحديثات النسخة الإنجليزية. وفي 23 نوفمبر 2026، أنجز المجتمع أيضًا مهام الترجمة والمراجعة المسجّلة لـ117 صفحة من أدلة قواعد البيانات الصينية، وأكمل النص الناقص في أربع صفحات تمهيدية لأقسام pgEdge.

| المكوّن | العمل الأصلي | المراجعة المثبّتة | الترخيص | الإشعار المحفوظ |
|---|---|---|---|---|
| [Patroni](/ar/patroni/) | [توثيق Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [`LICENSE` الأصلي](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ar/pgbackrest/) | [توثيق pgBackRest](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [`LICENSE` الأصلي](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ar/pgbouncer/) | [توثيق PgBouncer](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [`COPYRIGHT` الأصلي](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/ar/pgbadger/) | [توثيق pgBadger](https://pgbadger.darold.net/) | v13.3، الالتزام `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ar/haproxy/) | [أدلة HAProxy 3.4](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ar/etcd/) | [توثيق etcd v3.7](https://etcd.io/docs/v3.7/) | توثيق v3.7، الالتزام `e60635a`؛ إصدار البرنامج v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE` الأصلي](https://github.com/etcd-io/website/blob/main/LICENSE) |
{.wide .expand}

كل مجموعة **مُعدَّلة** لا منسوخة حرفيًا. أُعيدت صياغة العناوين والمراسي والوصلات
المتقاطعة وتواقيع الشيفرة وتجميع الصفحات والتنقل لهذه الطبعة؛ والنثر الأصلي
محفوظ كما هو. يشير إسناد نهاية الصفحة إلى ذلك، ويصل بسجل تغييرات هذا الموقع للصفحة
التي تقرؤها.

## Patroni {#patroni}

استُورد في 2026-08-15 من [توثيق Patroni](https://patroni.readthedocs.io/en/latest/)
للإصدار **v4.1.5**.

حقوق نشر Patroni (c) 2025 محفوظة لـ Compose وZalando SE وPatroni Contributors، ويوزَّع
بموجب [رخصة MIT](https://opensource.org/license/mit). يُحفظ النص الكامل للرخصة
[في المشروع الأصلي](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

استُورد في 2026-08-15 من [موقع توثيق pgBackRest](https://pgbackrest.org/)، وحُدِّث في 2026-11-21 إلى **v2.60.1**، بالوسم `release/2.60.1` والالتزام [`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870). هذه النسخة المترجمة متزامنة مع هذا التنقيح.

حقوق نشر pgBackRest (c) 2015-2026 محفوظة لـ The PostgreSQL Global Development Group
وDavid Steele، ويوزَّع بموجب [رخصة MIT](https://opensource.org/license/mit). يُحفظ النص
الكامل للرخصة [في المشروع الأصلي](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

استُورد في 2026-08-15 من [موقع توثيق PgBouncer](https://www.pgbouncer.org/) للإصدار
**v1.25.2** وحُدِّث في 2026-10-23 إلى
[**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1).

حقوق نشر PgBouncer (c) 2007-2009 محفوظة لـ Marko Kreen وSkype Technologies OÜ، ويوزَّع
بموجب [رخصة ISC](https://opensource.org/license/isc-license-txt). يُحفظ النص الكامل
للرخصة [في المشروع الأصلي](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT).

## pgBadger {#pgbadger}

استُورد في 2026-08-15 من <https://pgbadger.darold.net/> ومن [`darold/pgbadger`](https://github.com/darold/pgbadger)، وحُدِّث في 2026-11-21 إلى الإصدار المنشور **v13.3** عند الالتزام [`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e). هذه النسخة المترجمة متزامنة مع هذا التنقيح. وتحتفظ مقتطفات الموقع التاريخية ونماذج التقارير بمصادرها الخاصة.

حقوق نشر pgBadger (c) 2012-2026 محفوظة لـ Gilles Darold، ويوزَّع بموجب
[رخصة PostgreSQL](https://opensource.org/license/postgresql). يُحفظ النص الكامل للرخصة
بجوار الأمثلة بلا اتصال كـ
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) وفي
`static/third_party/pgbadger/LICENSE` في مستودع الموقع.

> [!IMPORTANT]
> يضم pgBadger وحدة `SQL::Beautify` معدّلة بموجب Artistic License 2.0، وتشمل موارد
> التقارير التي يولّدها مكوّنات MIT وGPL-2.0 وSIL Open Font License 1.1. يُحفظ جرد
> الموارد الأصلي الكامل كـ
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> [التقارير النموذجية](/ar/pgbadger/sample-reports/) المنشورة هنا نتاجات تاريخية
> مولّدة مسبقًا وتحتفظ بإشعاراتها الأصلية المضمّنة.

## HAProxy {#haproxy}

استُورد في 2026-08-16، وحُدِّث في 2026-11-21 إلى إصدار HAProxy 3.4 الرسمي [**v3.4.8 LTS**](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). أُعيد تنظيم أدلة `doc/intro.txt` و`doc/configuration.txt` و`doc/management.txt` الكاملة في 34 صفحة قراءة. لم يتغير دليل البدء ودليل الإدارة عن اللقطة السابقة، وتُسجَّل تغييرات دليل الإعداد في فرق التحديث وتشملها هذه النسخة المترجمة.

حقوق نشر HAProxy 2000-2026 محفوظة لـ Willy Tarreau، ويوزَّع بموجب
[رخصة GNU العمومية الإصدار 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
شرح HAProxy لرخصته، واستثناء OpenSSL الخاص به، والنص الكامل لـ GPLv2 منشورة كـ
[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) و
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> الصفحات المشتقة من HAProxy **غير** مشمولة برخصة CC BY 4.0 الخاصة بهذا الموقع. إنها
> تحمل شروط GPLv2 الخاصة بـ HAProxy.

## etcd {#etcd}

استُورد من التوثيق الرسمي لـ etcd v3.7 وحُدِّث في 2026-11-21 عند الالتزام
[`e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7).
شجرة المصدر المثبّتة هي `content/en/docs/v3.7`.

تستهدف أمثلة التثبيت وملخّص تغييرات الإصدار [etcd v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4)، عند التزام الإصدار `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`، المبني بـ Go 1.26.11. يحتفظ سجل التغييرات المثبّت بشكل منفصل بالعنوان “v3.7.4 (TBC)”، بينما يؤكد وسم الإصدار نشره. تُسجَّل لقطة التوثيق وإصدار البرنامج
بشكل منفصل في `data/upstreams.yaml`، مع قيم التحقق من ملفات المصدر.

حقوق نشر توثيق etcd 2013-الآن محفوظة لمؤلفي etcd. نثره مرخّص بموجب
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)، بينما الشيفرة وأمثلتها مرخّصة
بموجب [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). يُحفظ الإشعار الكامل
[في المشروع الأصلي](https://github.com/etcd-io/website/blob/main/LICENSE).

## هذا الموقع {#site}

النص الأصلي المكتوب لـ PG.CENTER منشور بموجب
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)، باستثناء الصفحات التي ينطبق عليها أحد تراخيص المشاريع الأصلية المذكورة أعلاه.

فيل PostgreSQL (Slonik) الظاهر في الصفحة الرئيسية هو علامة مشروع PostgreSQL نفسها،
مأخوذة من [مستودع موقع postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git)
ويعاد نشرها هنا دون تعديل بموجب [سياسة علامات PostgreSQL التجارية وشعاراتها](https://www.postgresql.org/about/policies/trademarks/)
كإشارة إلى PostgreSQL. إنها علامة PostgreSQL Community Association of Canada، واستخدامها
هنا لا يعني أي تأييد.

بُني الموقع بـ [OINK](https://oink.pgsty.com/) v1.2.0، وهو قالب Hugo مرخّص بموجب
[رخصة Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)، ويحمل إشعاراته الخاصة
بأصوله وتبعياته المضمّنة في مصدر الوحدة.

نرحّب بتصحيحات أي إسناد في هذه الصفحة عبر
[مستودع الموقع](https://github.com/pgsty/doc.pg.center/issues).
