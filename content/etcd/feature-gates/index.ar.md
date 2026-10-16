---
title: بوابات الميزات
weight: 1175
icon: fa-solid fa-toggle-on
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/feature-gates/index.md"
---

<!-- overview -->
تحتوي هذه الصفحة على نظرة عامة على بوابات الميزات المتنوعة التي يمكن لمسؤول النظام تحديدها على etcd.

راجع [مراحل الميزات](#feature-stages) للاطلاع على شرح لمراحل الميزة.

<!-- body -->
## نظرة عامة {#overview}

بوابات الميزات هي مجموعة من أزواج مفتاح=قيمة تصف ميزات etcd.
يمكنك تشغيل هذه الميزات أو إيقاف تشغيلها باستخدام علامة سطر الأوامر `--feature-gates` على etcd.

يتيح لك etcd تمكين أو تعطيل مجموعة من بوابات الميزات.
استخدم العلامة `-h` لعرض مجموعة كاملة من بوابات الميزات.
لتعيين بوابات الميزات، استخدم العلامة `--feature-gates` مسندة إلى قائمة من أزواج الميزات في سطر الأوامر:

```shell
--feature-gates=...,StopGRPCServiceOnDefrag=true
```

أو حدد `feature-gates` في ملف تهيئة YAML:

```shell
feature-gates: ...,StopGRPCServiceOnDefrag=true
```

### التغيير في البنية `embed.Config` {#change-in-embedetcdserver-struct}

في الإصدار 3.6، أُضيف الحقل `ServerFeatureGate` إلى `embed.Config`، وينبغي أن يحل محل الحقول التجريبية المدرجة أدناه:

```diff
package embed

type Config struct {
  // Deprecated: Use CompactHashCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalCompactHashCheckEnabled bool `json:"experimental-compact-hash-check-enabled"`

  // Deprecated: Use InitialCorruptCheck Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalInitialCorruptCheck bool `json:"experimental-initial-corrupt-check"`

  // Deprecated: Use TxnModeWriteWithSharedBuffer Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalTxnModeWriteWithSharedBuffer bool `json:"experimental-txn-mode-write-with-shared-buffer"`

  // Deprecated: Use StopGRPCServiceOnDefrag Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalStopGRPCServiceOnDefrag bool `json:"experimental-stop-grpc-service-on-defrag"`

  // Deprecated: Use LeaseCheckpoint Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpoint bool `json:"experimental-enable-lease-checkpoint"`
  
  // Deprecated: Use LeaseCheckpointPersist Feature Gate instead. Will be decommissioned in v3.7.
  ExperimentalEnableLeaseCheckpointPersist bool `json:"experimental-enable-lease-checkpoint-persist"`

+ // ServerFeatureGate is a server level feature gate
+ ServerFeatureGate featuregate.FeatureGate
  ...
```

### بوابات الميزات لميزات Alpha أو Beta {#feature-gates-for-alpha-or-beta-features}

الجداول التالية هي ملخص لبوابات الميزات التي يمكنك تعيينها على etcd.

| الميزة                          | الافتراضي | المرحلة | التفاصيل                                                                               |
|----------------------------------|---------|-------|--------------------------------------------------------------------------------------|
| CompactHashCheck                 | false   | Alpha |يمكّن القائد من التحقق دوريًا من تجزئات الضغط لدى التوابع.                                                                           |
| InitialCorruptCheck              | false   | Alpha |يمكّن من فحص تلف البيانات قبل خدمة أي حركة من العميل أو الأقران.                                                                              |
| LeaseCheckpoint                  | false   | Alpha |يمكّن القائد من إرسال نقاط تحقق منتظمة إلى الأعضاء الآخرين لمنع إعادة تعيين TTL المتبقي عند تغيير القائد.                                              |
| LeaseCheckpointPersist           | false   | Alpha |يمكّن من الاحتفاظ بقيمة remainingTTL لمنع التجديد التلقائي غير المحدد لعقود الإيجار طويلة الأمد.                                                                         |
| SetMemberLocalAddr               | false   | Alpha |يمكّن من استخدام أول عنوان محلي محدد من initial-advertise-peer-urls ليس من عناوين loopback كعنوان محلي عند التواصل مع أحد الأقران.      |
| StopGRPCServiceOnDefrag          | false   | Alpha |يمكّن خدمة gRPC في etcd من التوقف عن خدمة طلبات العملاء أثناء إزالة التجزئة.                                                                      |
| TxnModeWriteWithSharedBuffer     | true    | Beta  |يمكّن معاملة الكتابة من استخدام مخزن مؤقت مشترك في عمليات التحقق للقراءة فقط.                                                                                |

## استخدام ميزة {#using-a-feature}

### مراحل الميزات {#feature-stages}

يمكن أن تكون الميزة في مرحلة *Alpha* أو *Beta* أو *GA* أو *Deprecated*.
تعني ميزة *Alpha* ما يلي:

* معطلة افتراضيًا.
* قد تحتوي على أخطاء. قد يؤدي تمكين الميزة إلى الكشف عن أخطاء.
* قد يُسحب دعم الميزة في أي وقت ودون إشعار.
* قد تتغير واجهة API بطرق غير متوافقة في إصدار برمجي لاحق دون إشعار.
* موصى بها فقط للاستخدام في عناقيد الاختبار قصيرة العمر، نظرًا لزيادة خطر الأخطاء
  وغياب الدعم طويل الأمد.

تعني ميزة *Beta* ما يلي:

* ممكّنة افتراضيًا.
* الميزة مختبرة جيدًا. يُعد تمكين الميزة آمنًا.
* لن يُسحب دعم الميزة ككل، رغم أن التفاصيل قد تتغير.
* موصى بها فقط للاستخدامات غير الحرجة للأعمال بسبب احتمال اكتشاف أخطاء جديدة
  يصعب رصدها من خلال التبنّي الأوسع.

> [!NOTE]
> يرجى تجربة ميزات *Beta* وتقديم الملاحظات عنها!
> بعد تخرجها من مرحلة Beta، قد لا يكون من العملي بالنسبة لنا إجراء مزيد من التغييرات.

تُعرف ميزة *General Availability* (GA) أيضًا بالميزة *المستقرة*. وهي تعني ما يلي:

* الميزة ممكّنة دائمًا؛ لا يمكنك تعطيلها.
* بوابة الميزة المقابلة لم تعد ضرورية.
* ستظهر الإصدارات المستقرة من الميزات في البرمجيات المُصدرة للعديد من الإصدارات اللاحقة.

تعني ميزة *Deprecated* ما يلي:

* بوابة الميزة لم تعد مستخدمة.
* الميزة تخرجت إلى مرحلة GA أو أُزيلت.
