---
title: وحدات Golang
weight: 1650
description: تنظيم وحدات Golang في مشروع etcd
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-internal/modules.md"
---

يُنظَّم مشروع etcd (اعتبارًا من الإصدار 3.5) في [وحدات Golang](https://golang.org/ref/mod) متعددة مستضافة في [مستودع واحد](https://golang.org/ref/mod#vcs-dir).

![مخطط الوحدات](/etcd/dev-internal/img/modules.svg)

توجد الوحدات التالية:

  - **go.etcd.io/etcd/api/v3** - يحتوي على تعريفات API
  (مثل protos والمكتبات المولَّدة منها) التي تحدد بروتوكول الاتصال
  بين عملاء etcd وخادمه.

  - **go.etcd.io/etcd/pkg/v3** - مجموعة من الحزم المساعدة يستخدمها etcd
  دون أن تكون خاصة بـ etcd نفسه. لا تنتمي الحزمة إلى هنا إلا إذا كان من الممكن نقلها إلى مستودعها الخاص في المستقبل.
  يرجى تجنُّب إضافة شيفرة ذات تبعيات كثيرة هنا، لأنها تصبح تلقائيًا تبعيات لمكتبة العميل
  (التي نريد إبقاءها خفيفة).

  - **go.etcd.io/etcd/client/v3** - مكتبة العميل المستخدمة للاتصال بـ etcd عبر
  الشبكة (grpc). موصى بها لكل استخدام جديد لـ etcd.

  - **go.etcd.io/etcd/client/v2** - مكتبة العميل القديمة المستخدمة للاتصال بـ etcd
  عبر بروتوكول HTTP. مهملة. يجب أن يعتمد كل استخدام جديد على مكتبة /v3.

  - **go.etcd.io/etcd/raft/v3** - تنفيذ لبروتوكول الإجماع الموزَّع.
  لا ينبغي أن يحتوي على شيفرة خاصة بـ etcd.

  - **go.etcd.io/etcd/server/v3** - تنفيذ etcd.
  الشيفرة في هذه الحزمة داخلية بالنسبة إلى etcd ولا ينبغي أن تُستخدم من مشاريع
  خارجية. قد يتغير تخطيط الحزمة وواجهة API ضمن الإصدارات الفرعية.

  - **go.etcd.io/etcd/etcdctl/v3** - أداة سطر أوامر للوصول إلى etcd وإدارته.

  - **go.etcd.io/etcd/tests/v3** - وحدة تحتوي على جميع اختبارات التكامل الخاصة بـ etcd.
    ملاحظة: يجب الاحتفاظ بجميع اختبارات الوحدة (السريعة والتي لا تتطلب تبعيات عبر الوحدات)
    في الوحدات المحلية للشيفرة الخاضعة للاختبار.

  - **go.etcd.io/bbolt** - تنفيذ لشجرة B دائمة.
    مستضاف في مستودع منفصل: https://github.com/etcd-io/bbolt.


### العمليات {#operations}

1. يجب إصدار جميع وحدات etcd بالإصدارات نفسها، مثلًا:
   يجب أن يعتمد `go.etcd.io/etcd/client/v3@v3.5.10` على `go.etcd.io/etcd/api/v3@v3.5.10`.

   يمكن إجراء تحديث الإصدارات بشكل متسق باستخدام:
   ```shell script
   % DRY_RUN=false TARGET_VERSION="v3.5.10" ./scripts/release_mod.sh update_versions
   ```
2. يجب وسم الوحدات المصدَرة وفق قواعد https://golang.org/ref/mod#vcs-version،
   أي أن كل وحدة يجب أن تحصل على وسمها الخاص.
   يمكن تنفيذ الوسم باستخدام:
   ```shell script
   % DRY_RUN=false REMOTE_REPO="origin" ./scripts/release_mod.sh push_mod_tags
   ```

3. يجب أن تعتمد جميع وحدات etcd على الإصدارات نفسها من التبعيات الأساسية.
   يمكن التحقق من ذلك باستخدام:
   ```shell script
   % PASSES="dep" ./test.sh
   ```

4. يجب ألا تحتوي ملفات go.mod على تبعيات غير مستخدمة ويجب
   أن تتوافق مع تنسيق `go mod tidy`.
   يتم التحقق من ذلك بواسطة:
   ```
   % PASSES="mod_tidy" ./test.sh
   ```

5. لتشغيل إجراءات عبر جميع الوحدات (مثل التنسيق التلقائي لجميع الملفات)، يرجى
   استخدام/توسيع النص البرمجي التالي:
   ```shell script
   % ./scripts/fix.sh
   ```

### المستقبل {#future}

نود توجيه تطوير وحدات etcd نحو النموذج التالي، بوصفه هدفًا نسترشد به:

![مخطط الوحدات المستقبلي](/etcd/dev-internal/img/modules-future.svg)

يفترض هذا ما يلي:
  - فصل etcdmigrate/etcdadm عن الملف التنفيذي etcdctl.
    بفضل ذلك سيتحول etcdctl بوضوح إلى غلاف سطر أوامر حول واجهة API
    لعميل الشبكة، بينما سيدعم etcdmigrate/etcdadm العمليات الفيزيائية المباشرة على
    ملفات تخزين etcd.
  - فصل etcd-proxy عن الملف التنفيذي ./etcd، لأنه يحتوي على شيفرة تجريبية أكثر
    ومن ثم يحمل مخاطر وتبعيات إضافية.
  - إهمال دعم بروتوكول v2.
