---
title: ترقية عناقيد etcd والتطبيقات
weight: 6500
description: قائمة الوثائق الخاصة بترقية عناقيد etcd والتطبيقات
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
---

يحتوي هذا القسم على الوثائق الخاصة بترقية عناقيد etcd والتطبيقات.

## سياسة الترقية {#upgrade-policy}

قبل إجراء الترقية، لاحظ أن etcd لا يدعم سوى حالتي الترقية التاليتين:

* **ترقية التصحيح:** الترقية بين إصدارات التصحيح داخل الإصدار الثانوي نفسه (مثل 3.7.0 - 3.7.1).
* **الترقية الثانوية:** ترقية إصدار فرعي واحد في كل مرة (مثل 3.6 - 3.7). الترقيات التي تتخطى إصدارًا ثانويًا غير مدعومة ومن المرجح أن تفشل. حدِّث إلى أحدث إصدار تصحيحي قبل الترقية إلى الإصدار الثانوي التالي.

## ترقية عنقود etcd v3.x {#upgrading-an-etcd-v3x-cluster}

* [ترقية etcd من 3.0 إلى 3.1](/ar/etcd/upgrades/upgrade_3_1/)
* [ترقية etcd من 3.1 إلى 3.2](/ar/etcd/upgrades/upgrade_3_2/)
* [ترقية etcd من 3.2 إلى 3.3](/ar/etcd/upgrades/upgrade_3_3/)
* [ترقية etcd من 3.3 إلى 3.4](/ar/etcd/upgrades/upgrade_3_4/)
* [ترقية etcd من 3.4 إلى 3.5](/ar/etcd/upgrades/upgrade_3_5/)
* [ترقية etcd من 3.5 إلى 3.6](/ar/etcd/upgrades/upgrade_3_6/)
* [ترقية etcd من 3.6 إلى 3.7](/ar/etcd/upgrades/upgrade_3_7/)

## الترقية من etcd v2.3 {#upgrading-from-etcd-v23}

* [ترقية عنقود v2.3 إلى v3.0](/ar/etcd/upgrades/upgrade_3_0/)
