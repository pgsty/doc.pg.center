---
title: إعداد عنقود محلي
weight: 3125
description: إعداد عناقيد محلية للاختبار والتطوير
categories: [درس تعليمي]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/local_cluster.md"
---

لعمليات النشر المخصصة للاختبار والتطوير، تكون الطريقة الأسرع والأسهل هي إعداد عنقود محلي. لنشر إنتاجي، راجع قسم [إعداد العناقيد (clustering)][clustering].

## عنقود محلي مستقل {#local-standalone-cluster}

### بدء عنقود {#starting-a-cluster}

شغّل ما يلي لنشر عنقود etcd كعنقود مستقل:

```
$ ./etcd
...
```

إذا لم يكن الملف التنفيذي `etcd` موجودًا في دليل العمل الحالي، فقد يقع إما في `$GOPATH/bin/etcd` أو في `/usr/local/bin/etcd`. شغّل الأمر وفقًا لذلك.

يستمع عضو etcd قيد التشغيل على `localhost:2379` لطلبات العملاء.

### التفاعل مع العنقود {#interacting-with-the-cluster}

استخدم `etcdctl` للتفاعل مع العنقود قيد التشغيل:

1. خزّن زوج مفتاح/قيمة مثالًا في العنقود:

    ```
      $ ./etcdctl put foo bar
      OK
    ```

    إذا طُبع OK، فإن تخزين زوج المفتاح/القيمة نجح.

2. استرجع قيمة `foo`:

    ```
    $ ./etcdctl get foo
    bar
    ```

    إذا أُرجع `bar`، فالتفاعل مع عنقود etcd يعمل كما هو متوقع.

## عنقود محلي متعدد الأعضاء {#local-multi-member-cluster}

### بدء عنقود {#starting-a-cluster-1}

يوفر ملف `Procfile` الموجود في جذر مستودع git الخاص بـetcd طريقة سهلة لإعداد عنقود محلي متعدد الأعضاء. لبدء عنقود متعدد الأعضاء، انتقل إلى جذر شجرة مصادر etcd ونفّذ ما يلي:

1. ثبّت `goreman` للتحكم في التطبيقات القائمة على Procfile:

    ```
    $ go install github.com/mattn/goreman@latest
    ```

2. ابدأ عنقودًا بـ`goreman` باستخدام ملف Procfile الافتراضي الخاص بـetcd:

    ```
    $ goreman -f Procfile start
    ```

    يبدأ الأعضاء بالتشغيل. يستمعون على `localhost:2379` و`localhost:22379` و`localhost:32379` على التوالي لطلبات العملاء.

### التفاعل مع العنقود {#interacting-with-the-cluster-1}

استخدم `etcdctl` للتفاعل مع العنقود قيد التشغيل:

1. اطبع قائمة الأعضاء:

    ```
    $ etcdctl --write-out=table --endpoints=localhost:2379 member list
    ```
    تُعرض قائمة أعضاء etcd كما يلي:

    ```
    +------------------+---------+--------+------------------------+------------------------+
    |        ID        | STATUS  |  NAME  |       PEER ADDRS       |      CLIENT ADDRS      |
    +------------------+---------+--------+------------------------+------------------------+
    | 8211f1d0f64f3269 | started | infra1 | http://127.0.0.1:2380  | http://127.0.0.1:2379  |
    | 91bc3c398fb3c146 | started | infra2 | http://127.0.0.1:22380 | http://127.0.0.1:22379 |
    | fd422379fda50e48 | started | infra3 | http://127.0.0.1:32380 | http://127.0.0.1:32379 |
    +------------------+---------+--------+------------------------+------------------------+
    ```

2. خزّن زوج مفتاح/قيمة مثالًا في العنقود:

    ```
    $ etcdctl put foo bar
    OK
    ```

    إذا طُبع OK، فإن تخزين زوج المفتاح/القيمة نجح.

### اختبار تحمل الأعطال {#testing-fault-tolerance}

لاختبار تحمل etcd للأعطال، أوقف عضوًا وحاول استرجاع المفتاح.

1. حدد اسم عملية العضو الذي سيتم إيقافه.

    يعرض `Procfile` خصائص العنقود متعدد الأعضاء. على سبيل المثال، خذ العضو الذي اسم عمليته `etcd2`.

2. أوقف العضو:

    ```
    # kill etcd2
    $ goreman run stop etcd2
    ```

3. خزّن مفتاحًا:

    ```
    $ etcdctl put key hello
    OK
    ```

4.  استرجع المفتاح الذي خُزن في الخطوة السابقة:

    ```
    $ etcdctl get key
    hello
    ```

5. استرجع مفتاحًا من العضو المتوقف:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    ```

    ينبغي أن يعرض الأمر خطأً ناتجًا عن فشل الاتصال:

    ```
    2017/06/18 23:07:35 grpc: Conn.resetTransport failed to create client transport: connection error: desc = "transport: dial tcp 127.0.0.1:22379: getsockopt: connection refused"; Reconnecting to "localhost:22379"
    Error:  grpc: timed out trying to connect
    ```
6. أعد تشغيل العضو المتوقف:

    ```
    $ goreman run restart etcd2
    ```

7. احصل على المفتاح من العضو المعاد تشغيله:

    ```
    $ etcdctl --endpoints=localhost:22379 get key
    hello
    ```

    إعادة تشغيل العضو تعيد تأسيس الاتصال. سيتمكن `etcdctl` الآن من استرجاع المفتاح بنجاح. لمعرفة المزيد عن التفاعل مع etcd، اقرأ قسم [التفاعل مع etcd][interacting].

[clustering]: /ar/etcd/op-guide/clustering/
[interacting]: /ar/etcd/dev-guide/interacting_v3/
