---
title: التثبيت
weight: 1150
description: تعليمات لتثبيت etcd من الملفات الثنائية المبنية مسبقًا أو من المصدر.
icon: fa-solid fa-download
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## المتطلبات {#requirements}

قبل تثبيت etcd، راجع الصفحات التالية:

- [المنصات المدعومة][Supported platforms]
- [توصيات العتاد][Hardware recommendations]

## تثبيت الملفات الثنائية المبنية مسبقًا {#install-pre-built-binaries}

أسهل طريقة لتثبيت etcd هي من الملفات الثنائية المبنية مسبقًا:

 1. نزّل الملف المضغوط لمنصتك من [الإصدارات المنشورة][releases]،
    مع اختيار الإصدار [v3.7.2][tagged-release] أو أحدث.
 2. فك ضغط الملف المضغوط. ينتج عن ذلك دليل يحتوي على الملفات الثنائية.
 3. أضف الملفات الثنائية القابلة للتنفيذ إلى مسارك. مثلًا، أعد تسمية الملفات
    الثنائية و/أو انقلها إلى دليل موجود في مسارك (مثل `/usr/local/bin`)، أو
    أضف الدليل الذي أنشأته الخطوة السابقة إلى مسارك.
 4. من خلال الصدفة (shell)، اختبر أن `etcd` موجود في مسارك:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

## البناء من المصدر {#build-from-source}

بالنسبة لـ etcd v3.7.2، استخدم [Go إصدار 1.26+][go]؛ يثبّت هذا الإصدار سلسلة أدوات Go 1.26.8.
ابنِ من المصدر باتباع الخطوات التالية:

 1. [نزّل مستودع etcd على شكل ملف zip][download] وفك ضغطه، أو استنسخ
    المستودع باستخدام الأمر التالي.

    ```sh
    $ git clone -b v3.7.2 https://github.com/etcd-io/etcd.git
    ```
    للبناء من `main@HEAD`، احذف العلامة `-b v3.7.2`.

 2. غيّر الدليل:

    ```sh
    $ cd etcd
    ```
 3. شغّل سكربت البناء:

    ```sh
    $ ./scripts/build.sh
    ```

    توجد الملفات الثنائية في الدليل `bin`.

 4. أضف المسار الكامل للدليل `bin` إلى مسارك، مثلًا:

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. اختبر أن `etcd` موجود في مسارك:

    ```sh
    $ etcd --version
    ```

## التثبيت عبر حزم نظام التشغيل {#installation-via-os-packages}
*تنويه: قد تقدم تثبيتات etcd عبر مديري حزم نظام التشغيل إصدارات قديمة لأنها لا تُصان تلقائيًا ولا تحظى بدعم رسمي من مشروع etcd. لذا استخدم حزم نظام التشغيل بحذر.*

توجد طرق متعددة لتثبيت etcd على أنظمة التشغيل المختلفة، وهذه مجرد بعض الأمثلة على كيفية القيام بذلك.

### MacOS (Homebrew) {#macos-homebrew}

1. حدّث homebrew:
```sh
$ brew update
```

2. ثبّت etcd:
```sh
$ brew install etcd
```

3. تحقق من التثبيت
```sh
$ etcd --version
```

## Linux {#linux}

مع أنه من الممكن تثبيت etcd عبر المستودعات الرسمية ومديري الحزم للعديد من توزيعات Linux الرئيسية، فإن الإصدارات المنشورة قد تكون قديمة بشكل كبير. لذا يُنصح بشدة بعدم التثبيت بهذه الطريقة.

الطريقة الموصى بها لتثبيت etcd على Linux هي إما عبر [الملفات الثنائية المبنية مسبقًا](#install-pre-built-binaries) أو باستخدام Homebrew.

### Homebrew على Linux {#homebrew-on-linux}

يمكن لـ [Homebrew العمل على Linux][Homebrew can run on Linux]، ويمكنه توفير إصدارات حديثة من البرمجيات.

- المتطلبات المسبقة
  - حدّث Homebrew:

    ```sh
    $ brew update
    ```

- الإجراء
  - التثبيت باستخدام `brew`:

    ```sh
    $ brew install etcd
    ```

- النتيجة
  - تحقق من التثبيت بالحصول على الإصدار:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

    المخرجات أعلاه مجرد مثال. قد يوفر Homebrew إصدار ترقيع مختلفًا؛ تحقق من الإصدار المثبت باستخدام `etcd --version`.

## Docker {#docker}

يستخدم etcd [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) كسجل
حاويات رئيسي، و[`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) كسجل
ثانوي.

لتشغيل etcd باستخدام Docker:

```sh
ETCD_VER=v3.7.2

rm -rf /tmp/etcd-data.tmp && mkdir -p /tmp/etcd-data.tmp && \
  docker rmi gcr.io/etcd-development/etcd:${ETCD_VER} || true && \
  docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
  --name etcd-gcr-${ETCD_VER} \
  gcr.io/etcd-development/etcd:${ETCD_VER} \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster s1=http://0.0.0.0:2380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --log-level info \
  --logger zap \
  --log-outputs stderr

docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcd --version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdutl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl endpoint health
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl put foo bar
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl get foo
```

## التثبيت كجزء من تثبيت Kubernetes {#installation-as-part-of-kubernetes-installation}

- [تشغيل etcd كـ StatefulSet في Kubernetes][Running etcd as a Kubernetes StatefulSet]

## فحص التثبيت {#installation-check}

لإجراء فحص سلامة أكثر شمولًا قليلًا لتثبيتك، راجع
[البدء السريع][Quickstart].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.2.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /ar/etcd/op-guide/hardware/
[Quickstart]: /ar/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /ar/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.2
[Supported platforms]: /ar/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
