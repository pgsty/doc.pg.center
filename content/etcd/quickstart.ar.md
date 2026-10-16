---
title: البدء السريع
weight: 900
description: شغّل etcd واجعله جاهزًا للعمل في أقل من 5 دقائق!
icon: fa-solid fa-rocket
categories: [درس تعليمي]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/quickstart.md"
---

اتبع هذه التعليمات لتثبيت عنقود etcd أحادي العضوية وتشغيله واختباره محليًا:

 1. ثبّت etcd من الملفات الثنائية المبنية مسبقًا أو من المصدر. للتفاصيل، راجع
    [التثبيت][Install].

    > [!WARNING]
    > **مهم**: احرص على تنفيذ الخطوة الأخيرة
    > من تعليمات التثبيت للتحقق من أن `etcd` موجود في مسارك.

 2. أطلق `etcd`:

    ```console
    $ etcd
    {"level":"info","ts":"2021-09-17T09:19:32.783-0400","caller":"etcdmain/etcd.go:72","msg":... }
    ⋮
    ```

    > [!NOTE]
    > **ملاحظة**: المخرجات التي ينتجها `etcd` هي
    > [سجلات](/ar/etcd/op-guide/configuration/#logging) &mdash; ويمكن تجاهل
    > السجلات بمستوى info.

 3. من **طرفية أخرى**، استخدم `etcdctl` لضبط مفتاح:

    ```console
    $ etcdctl put greeting "Hello, etcd"
    OK
    ```

 4. من الطرفية نفسها، استرجع المفتاح:

    ```console
    $ etcdctl get greeting
    greeting
    Hello, etcd
    ```

## ما هي الخطوة التالية؟ {#whats-next}

تعرّف على المزيد من طرق إعداد etcd واستخدامه من الصفحات التالية:

- إذا كنت مطوّرًا:
  - استكشف [واجهة برمجة التطبيقات][api] gRPC.
  - اعثر على [روابط اللغات والأدوات][integrations].

- إذا كنت مشغلًا أو مسؤولًا:
  - أنشئ [عنقودًا متعدد الأجهزة][clustering].
  - تعرّف على كيفية [إعداد][configure] etcd.
  - استخدم TLS [لتأمين عنقود etcd][security].
  - [اضبط أداء etcd][tuning].

[api]: /ar/etcd/learning/api
[clustering]: /ar/etcd/op-guide/clustering
[configure]: /ar/etcd/op-guide/configuration
[integrations]: /ar/etcd/integrations
[security]: /ar/etcd/op-guide/security
[tuning]: /ar/etcd/tuning
[Install]: /ar/etcd/install/
