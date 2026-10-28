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

| المكوّن | العمل الأصلي | المراجعة المثبّتة | الترخيص | الإشعار المحفوظ |
|---|---|---|---|---|
| [Patroni](/ar/patroni/) | [توثيق Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [`LICENSE` الأصلي](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ar/pgbackrest/) | [توثيق pgBackRest](https://pgbackrest.org/) | v2.60.0 | [MIT](https://opensource.org/license/mit) | [`LICENSE` الأصلي](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ar/pgbouncer/) | [توثيق PgBouncer](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [`COPYRIGHT` الأصلي](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/ar/pgbadger/) | [توثيق pgBadger](https://pgbadger.darold.net/) | v13.2، لقطة تطوير، الالتزام `f373ac6` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ar/haproxy/) | [أدلة HAProxy 3.4](https://docs.haproxy.org/3.4/) | 3.4.7-57؛ المستقرة v3.4.7، الالتزام `0faeaed` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ar/etcd/) | [توثيق etcd v3.7](https://etcd.io/docs/v3.7/) | توثيق v3.7، الالتزام `d20f8ae`؛ إصدار البرنامج v3.7.3 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE` الأصلي](https://github.com/etcd-io/website/blob/main/LICENSE) |

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

استُورد في 2026-08-15 من [موقع توثيق pgBackRest](https://pgbackrest.org/)، وحُدِّث في 2026-10-23 إلى **v2.60.0**، بالوسم `release/2.60.0` والالتزام [`2e1c4f2`](https://github.com/pgbackrest/pgbackrest/commit/2e1c4f2ba727c45a0a23d4b326905088dc15b1a1).

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

استُورد في 2026-08-15 من <https://pgbadger.darold.net/> ومن [`darold/pgbadger`](https://github.com/darold/pgbadger)، وحُدِّث في 2026-10-23 إلى الالتزام [`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67).
هذه لقطة من توثيق التطوير بعد أحدث إصدار منشور، v13.2، وليست إصدارًا مستقرًا جديدًا. وتحتفظ مقتطفات الموقع التاريخية ونماذج التقارير بمصادرها الخاصة.

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

استُورد في 2026-08-16، وحُدِّث في 2026-08-30، وجُدِّد في 2026-10-23 بلقطة الصيانة
الرسمية الإنجليزية لـ HAProxy 3.4 رقم `3.4.7-57`، الالتزام
[`0faeaeda6cdb`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3).
أحدث إصدار مستقر هو `3.4.7` (الوسم `v3.4.7`)؛ وتشمل لقطة التوثيق تغييرات فرع الصيانة
اللاحقة لذلك الإصدار.
النثر الإنجليزي مشتق من أدلة `doc/intro.txt` و`doc/configuration.txt` و
`doc/management.txt` الكاملة — 40,246 سطرًا إجمالًا — أُعيد تنظيمها في 34 صفحة قراءة.

حقوق نشر HAProxy 2000-2026 محفوظة لـ Willy Tarreau، ويوزَّع بموجب
[رخصة GNU العمومية الإصدار 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
شرح HAProxy لرخصته، واستثناء OpenSSL الخاص به، والنص الكامل لـ GPLv2 منشورة كـ
[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) و
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> الصفحات المشتقة من HAProxy **غير** مشمولة برخصة CC BY 4.0 الخاصة بهذا الموقع. إنها
> تحمل شروط GPLv2 الخاصة بـ HAProxy.

## etcd {#etcd}

استُورد من التوثيق الرسمي لـ etcd v3.7 وحُدِّث في 2026-10-13 عند الالتزام
[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc).
شجرة المصدر المثبّتة هي
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7).

في 2026-10-28، حُدِّثت أمثلة التثبيت وDocker وKubernetes وملخّص تغييرات الإصدار لتوافق
[etcd v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3)، عند التزام الإصدار
[`0a173d0`](https://github.com/etcd-io/etcd/commit/0a173d0410a96d01091b484daae81365bbcde57e).
يثبّت ملف `go.mod` لهذا الإصدار Go 1.26.10. تُسجَّل لقطة التوثيق وإصدار البرنامج
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
