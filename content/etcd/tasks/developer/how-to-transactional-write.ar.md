---
title: كيفية إجراء كتابات متعددة في معاملة واحدة
description: دليل لإجراء الكتابات ضمن المعاملات
weight: 500
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
---

## المتطلبات الأساسية {#prerequisites}

* تثبيت [`etcd` و`etcdctl`](/ar/etcd/install/).
* عنقود `etcd` قيد التشغيل.

## المصطلحات {#terminology}

فيما يلي تعريفات لبعض المصطلحات الرئيسية المستخدمة في [المثال](#example) أدناه.

| المصطلحات | التعريف |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | أداة سطر الأوامر للتفاعل مع خادم etcd. |
| أمر [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options) | الأمر `txn` هو اختصار لكلمة "transaction" (معاملة). يقرأ عدة طلبات etcd من المدخل القياسي ويطبقها كمعاملة ذرية واحدة. تتكون المعاملة من قائمة شروط، وقائمة طلبات تُطبق إذا كانت جميع الشروط صحيحة، وقائمة طلبات تُطبق إذا كان أي شرط منها خاطئًا. راجع [أوامر قيم المفاتيح في etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands) لمزيد من المعلومات.|
| `compare` | تعمل عبارة `compare` ضمن المعاملة (`txn`) كفحص شرطي يحدد ما إذا كان يجب تنفيذ عمليات المعاملة. فهي تضمن عدم تطبيق التغييرات إلا إذا كانت الحالة الحالية لمخزن قيم المفاتيح مطابقة للشروط المتوقعة، وبذلك تحافظ على اتساق البيانات وتمنع التعارضات في البيئات المتزامنة. للاطلاع على بنية الأمر، راجع قسم [تنفيذ معاملة](#2-perform-a-transaction) أدناه.|

## المعاملات {#transactions}

`txn` لمعالجة جميع الطلبات في معاملة واحدة:

```bash
etcdctl txn --help
```

تتيح لك المعاملات في etcd تنفيذ عمليات متعددة بشكل ذري، مما يضمن أنه إما أن تُطبق جميع العمليات أو لا تُطبق أي منها. وهذا أمر بالغ الأهمية للحفاظ على اتساق البيانات عند إجراء تحديثات مترابطة. اعرف المزيد عن المعاملات في [وثائق الـ API](/ar/etcd/learning/api/#transaction).

### المثال {#example}

لنتأمل سيناريو ترغب فيه في تحديث البريد الإلكتروني ورقم الهاتف لمستخدم في معاملة واحدة. ويضمن هذا تطبيق كلا التحديثين معًا.

![05_etcdctl_transaction_2024101213](/etcd/tasks/img/transactional-write.gif)

#### 0. المتغيرات والأعلام المستخدمة {#0-variables-and-flags-used}

| المتغيرات |
| :--- |
| `/users/{<user_id>/email` : مفتاح etcd يمثل عنوان البريد الإلكتروني للمستخدم.|
| `/users/<user_id>/phone` : مفتاح etcd يمثل رقم هاتف المستخدم.|
| **الأعلام** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3) : علم يتيح إدخال بيانات المعاملة يدويًا|

#### 1. إعداد البيانات الأولية {#1-set-up-initial-data}

أولًا، أنشئ مستخدمًا مع بعض البيانات الأولية.

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. تنفيذ معاملة {#2-perform-a-transaction}

حدّث البريد الإلكتروني ورقم الهاتف للمستخدم في معاملة واحدة.

   ```shell
   etcdctl txn --interactive

   compares:
   value("/users/12345/email") = "old.address@johndoe.com"

   success requests (get, put, delete):
   put /users/12345/email "new.address@johndoe.com"
   put /users/12345/phone "098-765-4321"

   failure requests (get, put, delete):
   get /users/12345/email
   ```

* **المقارنة**: تحقق مما إذا كان البريد الإلكتروني الحالي هو "<old.address@johndoe.com>". يضمن هذا عدم متابعة المعاملة إلا إذا كانت البيانات كما هو متوقع.
* **النجاح**: إذا كانت المقارنة صحيحة، فحدّث كلًّا من البريد الإلكتروني ورقم الهاتف.
* **الفشل**: إذا فشلت المقارنة، فاسترجع البريد الإلكتروني الحالي لفهم سبب عدم متابعة المعاملة.

### اعتبارات مهمة {#important-considerations}

* **الذرية**: تضمن المعاملة تحديث البريد الإلكتروني ورقم الهاتف معًا. وإذا لم يتحقق الشرط الأولي (المقارنة)، فلن يُطبق أي من التحديثين.
* **الاتساق**: يحافظ استخدام المعاملات على اتساق البيانات، خاصة عند التعامل مع تحديثات مترابطة متعددة.
* **تجنب عمليات put المتعددة على نفس المفتاح**: لا تضع قيمًا متعددة لنفس المفتاح ضمن معاملة واحدة، إذ قد يؤدي ذلك إلى نتائج غير متوقعة. يجب تحديث كل مفتاح مرة واحدة فقط في كل معاملة.
