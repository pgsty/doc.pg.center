---
title: التحكم في الوصول المبني على الأدوار
weight: 4100
description: دليل أساسي للمصادقة والتحكم في الوصول المبني على الأدوار
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/authentication/rbac.md"
---

## نظرة عامة {#overview}

أُضيفت المصادقة في etcd 2.1. أجرى etcd v3 API تعديلًا طفيفًا على واجهة برمجة تطبيقات ميزة المصادقة وواجهة المستخدم الخاصة بها لتناسب نموذج البيانات الجديد بشكل أفضل. يهدف هذا الدليل إلى مساعدة المستخدمين على إعداد مصادقة أساسية والتحكم في الوصول المبني على الأدوار في etcd v3.

## المستخدمون والأدوار الخاصة {#special-users-and-roles}

هناك مستخدم خاص واحد، هو `root`، ودور خاص واحد، هو `root`.

### المستخدم `root` {#user-root}

يجب إنشاء المستخدم `root`، الذي يملك وصولًا كاملًا إلى etcd، قبل تنشيط المصادقة. تكمن الفكرة وراء المستخدم `root` في الأغراض الإدارية: إدارة الأدوار والمستخدمين العاديين. يجب أن يمتلك المستخدم `root` الدور `root`، ويسمح له بتغيير أي شيء داخل etcd.

### الدور `root` {#role-root}

يمكن منح الدور `root` لأي مستخدم، بالإضافة إلى المستخدم root. يمتلك المستخدم الذي يحمل الدور `root` وصولًا شاملًا للقراءة والكتابة وصلاحية تحديث تهيئة المصادقة للعنقود. علاوة على ذلك، يمنح الدور `root` امتيازات للصيانة العامة للعنقود، بما في ذلك تعديل عضوية العنقود، وإلغاء تجزئة المخزن، وأخذ اللقطات.

## العمل مع المستخدمين {#working-with-users}

يتولى الأمر الفرعي `user` الخاص بـ `etcdctl` كل ما يتعلق بحسابات المستخدمين.

يمكن الحصول على قائمة بالمستخدمين باستخدام:

```
$ etcdctl user list
```

إنشاء مستخدم بسيط مثل:

```
$ etcdctl user add myusername
```

سيطالب إنشاء مستخدم جديد بإدخال كلمة مرور جديدة. يمكن تزويد كلمة المرور من المدخل القياسي عند تقديم الخيار `--interactive=false`. يمكن أيضًا استخدام `--new-user-password` لتزويد كلمة المرور.

من الممكن أيضًا إنشاء مستخدم لا يمكن المصادقة عليه بكلمة مرور كما يلي:

```
$ etcdctl user add myusername --no-password
```

لا يمكن لمثل هذا المستخدم المصادقة إلا [بالاسم الشائع لـ TLS](#using-tls-common-name).

> [!NOTE]
> لا يدعم etcd المصادقة بكلمة مرور فارغة عبر `--user username:`. على سبيل المثال، لا يمكن للمستخدم المُنشأ بكلمة مرور فارغة، مثل `etcdctl user add anonymous:''`، المصادقة من خلال طلبات اسم المستخدم/كلمة المرور، وتفشل الطلبات مثل `etcdctl --user anonymous: get foo` بالخطأ `user name is empty`.

يمكن منح الأدوار لمستخدم وسحبها منه باستخدام:

```
$ etcdctl user grant-role myusername foo
$ etcdctl user revoke-role myusername bar
```

يمكن فحص إعدادات المستخدم باستخدام:

```
$ etcdctl user get myusername
```

ويمكن تغيير كلمة مرور مستخدم باستخدام

```
$ etcdctl user passwd myusername
```

سيطالب تغيير كلمة المرور مجددًا بإدخال كلمة مرور جديدة. يمكن تزويد كلمة المرور من المدخل القياسي عند تقديم الخيار `--interactive=false`.

احذف حسابًا باستخدام:
```
$ etcdctl user delete myusername
```


## العمل مع الأدوار {#working-with-roles}

يتولى الأمر الفرعي `role` الخاص بـ `etcdctl` كل ما يتعلق بضوابط الوصول لأدوار معينة، كما مُنحت للمستخدمين الأفراد.

اسرد الأدوار باستخدام:

```
$ etcdctl role list
```

أنشئ دورًا جديدًا باستخدام:

```
$ etcdctl role add myrolename
```

لا يمتلك الدور كلمة مرور؛ فهو يعرّف ببساطة مجموعة جديدة من حقوق الوصول.

تُمنح الأدوار الوصول إلى مفتاح واحد أو نطاق من المفاتيح.

يمكن تحديد النطاق كفترة [start-key, end-key) حيث يجب أن يكون start-key أقل من end-key معجميًا بطريقة أبجدية.

يمكن منح الوصول للقراءة أو الكتابة أو كليهما، كما في الأمثلة التالية:

```
# Give read access to a key /foo
$ etcdctl role grant-permission myrolename read /foo

# Give read access to keys with a prefix /foo/. The prefix is equal to the range [/foo/, /foo0)
$ etcdctl role grant-permission myrolename --prefix=true read /foo/

# Give write-only access to the key at /foo/bar
$ etcdctl role grant-permission myrolename write /foo/bar

# Give full access to keys in a range of [key1, key5)
$ etcdctl role grant-permission myrolename readwrite key1 key5

# Give full access to keys with a prefix /pub/
$ etcdctl role grant-permission myrolename --prefix=true readwrite /pub/
```

لمعرفة ما تم منحه، يمكننا الاطلاع على الدور في أي وقت:

```
$ etcdctl role get myrolename
```

يتم إلغاء الصلاحيات بالطريقة المنطقية نفسها:

```
$ etcdctl role revoke-permission myrolename /foo/bar
```

وكذلك الحال مع إزالة دور تمامًا:

```
$ etcdctl role delete myrolename
```

## تمكين المصادقة {#enabling-authentication}

الخطوات الدنيا لتمكين المصادقة هي كما يلي. يمكن للمسؤول إعداد المستخدمين والأدوار قبل تمكين المصادقة أو بعده، بحسب التفضيل.

تأكد من إنشاء المستخدم root:

```
$ etcdctl user add root
Password of root:
```

فعّل المصادقة:

```
$ etcdctl auth enable
```

بعد ذلك، يعمل etcd مع تمكين المصادقة. لتعطيلها لأي سبب كان، استخدم الأمر العكسي:

```
$ etcdctl --user root:rootpw auth disable
```

## نطاق أمان المصادقة {#security-scope-of-authentication}

عند تمكين المصادقة بالأمر `etcdctl auth enable`، فإنها تحمي عمليات gRPC API للإصدار V3‏ (مثل get، وput، وdelete، وwatch، وغيرها).

تعمل نقطتا النهاية HTTP‏ `/metrics` و `/health` على معالج منفصل و**ليستا** محميتين بمصادقة RBAC للإصدار V3. يتيح هذا التصميم لـ Prometheus وموازنات الحمل جمع المقاييس دون الحاجة إلى مصادقة gRPC، مع الاستمرار في حماية بيانات المفتاح والقيمة.

لتأمين نقاط النهاية هذه الخاصة بالرصد:

- فعّل mTLS بالخيارات `--cert-file` و `--key-file` و `--client-cert-auth`
- أو اربط المقاييس بواجهة شبكة خاصة باستخدام `--listen-metrics-urls`
- أو استخدم سياسات الشبكة/قواعد جدار الحماية لتقييد الوصول

## استخدام `etcdctl` للمصادقة {#using-etcdctl-to-authenticate}

يدعم `etcdctl` خيارًا مشابهًا لخيار `curl` للمصادقة.

```
$ etcdctl --user user:password get foo
```

يمكن أخذ كلمة المرور من موجه إدخال:

```
$ etcdctl --user user get foo
```

يمكن أيضًا أخذ كلمة المرور من خيار سطر أوامر هو `--password`:

```
$ etcdctl --user user --password password get foo
```


بخلاف ذلك، تظل جميع أوامر `etcdctl` كما هي. لا يزال بإمكانك إنشاء المستخدمين والأدوار وتعديلها، لكنها تتطلب مصادقة من مستخدم يحمل الدور root.

## استخدام الاسم الشائع لـ TLS {#using-tls-common-name}
ابتداءً من الإصدار v3.2، إذا أُطلق خادم etcd بالخيار `--client-cert-auth=true`، فسيُستخدم حقل الاسم الشائع (CN) في شهادة TLS الخاصة بالعميل كمستخدم etcd. في هذه الحالة، يقوم الاسم الشائع بمصادقة المستخدم ولا يحتاج العميل إلى كلمة مرور. لاحظ أنه في حال تحقق الشرطين معًا: 1. تمرير `--client-cert-auth=true` وتقديم العميل للـ CN، و 2. تقديم العميل لاسم المستخدم وكلمة المرور، تُمنح الأولوية للمصادقة المبنية على اسم المستخدم وكلمة المرور. لاحظ أن هذه الميزة لا يمكن استخدامها مع gRPC-proxy ولا مع gRPC-gateway. ذلك لأن gRPC-proxy ينهي اتصال TLS الوارد من عميله فيتشارك جميع العملاء شهادة واحدة خاصة بالوكيل. أما gRPC-gateway فيستخدم اتصال TLS داخليًا لتحويل طلب HTTP إلى طلب gRPC، لذا يتشارك القيد نفسه. وبالتالي لا يستطيع العملاء تقديم الـ CN الخاص بهم إلى الخادم بشكل صحيح. سيتسبب gRPC-proxy في حدوث خطأ وسيتوقف إذا كانت الشهادة المقدمة تحتوي على CN غير فارغ. يعيد gRPC-proxy خطأً يشير إلى أن العميل يمتلك CN غير فارغ في شهادته.

## ملاحظات حول قوة كلمة المرور {#notes-on-password-strength}
لا تفرض `etcdctl` ولا واجهة etcd API طولًا محددًا لكلمة المرور أثناء عمليات إنشاء المستخدمين أو تحديث كلمات مرورهم. إن فرض هذه المتطلبات مسؤولية تقع على عاتق المسؤول. لتجنب مخاطر الأمان المتعلقة بقوة كلمة المرور، يمكن الاستعانة [بالمصادقة المبنية على الاسم الشائع لـ TLS](#using-tls-common-name) وبالمستخدمين المنشأين بالخيار `--no-password`.
