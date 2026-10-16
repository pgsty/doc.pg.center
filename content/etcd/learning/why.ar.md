---
title: etcd مقارنةً بمخازن المفاتيح/القيم الأخرى
weight: 2875
description: تاريخ etcd واستخداماته ومقارنته بالأدوات الأخرى
categories: [مفهوم]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
---

نشأ اسم "etcd" عن فكرتين: مجلد "/etc" في unix، والأنظمة الموزعة «d»istributed. فمجلد "/etc" مكان لتخزين بيانات الإعداد لنظام واحد، بينما يخزن etcd معلومات الإعداد للأنظمة الموزعة واسعة النطاق. ومن ثم، فإن "/etc" «d»istributed هو "etcd".

صُمِّم etcd ركيزةً عامة للأنظمة الموزعة واسعة النطاق. وهي أنظمة لن تتسامح أبدًا مع التشغيل في حالة انقسام الدماغ (split-brain) ومستعدة للتضحية بالتوافر لبلوغ هذه الغاية. يخزن etcd البيانات الوصفية بطريقة متسقة ومتحملة للأعطال. وعنقود etcd مصمم ليقدم تخزين مفاتيح/قيم بأفضل ما في فئته من استقرار وموثوقية وقابلية توسع وأداء.

تستخدم الأنظمة الموزعة etcd مخزنًا متسقًا للمفاتيح/القيم لإدارة الإعداد، واكتشاف الخدمات، وتنسيق العمل الموزع. وتستخدم كثير من [المؤسسات][production-users] etcd لتنفيذ أنظمة إنتاجية مثل مجدولات الحاويات، وخدمات اكتشاف الخدمات، ومخازن البيانات الموزعة. وتشمل الأنماط الموزعة الشائعة باستخدام etcd [انتخاب القائد][etcd-etcdctl-elect]، و[الأقفال الموزعة][etcd-etcdctl-lock]، ومراقبة حيوية الأجهزة.

## حالات الاستخدام {#use-cases}

- Container Linux by CoreOS: تحصل التطبيقات العاملة على [Container Linux][container-linux] على تحديثات تلقائية لنواة Linux دون توقف. يستخدم Container Linux [locksmith] لتنسيق التحديثات. ينفذ Locksmith آلية تزامن موزعة (semaphore) فوق etcd لضمان أن جزءًا فقط من العنقود يعاد إقلاعه في أي لحظة معينة.
- يخزن [Kubernetes][kubernetes] بيانات الإعداد في etcd لأغراض اكتشاف الخدمات وإدارة العنقود؛ واتساق etcd حاسم للجدولة الصحيحة للخدمات وتشغيلها. يحفظ خادم Kubernetes API حالة العنقود في etcd. ويستخدم watch API الخاصة بـ etcd لمراقبة العنقود وطرح تغييرات الإعداد الحرجة.

## جدول المقارنة {#comparison-chart}

ربما يبدو etcd بالفعل خيارًا ملائمًا، لكن كما هو الشأن مع كل القرارات التقنية، امضِ بحذر. يرجى ملاحظة أن هذه الوثيقة كتبها فريق etcd. ومع أن المثالية هي مقارنة منزهة للتقنية والميزات، فإن خبرة المؤلفين وتحيزاتهم تحابي etcd بوضوح. استخدمه فقط وفق التوجيهات.

الجدول أدناه مرجع سريع عملي لالتقاط الفروق بين etcd وأشهر بدائله بنظرة واحدة. ومزيد من التعليقات والتفاصيل لكل عمود في الأقسام التالية للجدول.

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| بدائيات التزامن |  [استدعاءات RPC للأقفال][etcd-v3lock]، [استدعاءات RPC للانتخابات][etcd-v3election]، [أقفال سطر الأوامر][etcd-etcdctl-lock]، [انتخابات سطر الأوامر][etcd-etcdctl-elect]، [وصفات][etcd-recipe] بلغة go | وصفات [curator][curator] خارجية بلغة Java | [واجهة API أقفال أصلية][consul-lock] | [نادر][newsql-leader]، إن وُجد |
| قراءات قابلة للخطية | [نعم][etcd-linread] | لا | [نعم][consul-linread] | أحيانًا |
| تحكم تزامن متعدد الإصدارات | [نعم][etcd-mvcc] | لا | لا | أحيانًا |
| المعاملات | [مقارنات حقول، قراءة، كتابة][etcd-txn] | [فحوص إصدار، كتابة][zk-txn] | [مقارنة حقل، قفل، قراءة، كتابة][consul-txn]  | بأسلوب SQL |
| إخطار التغييرات | [فواصل مفاتيح تاريخية وحالية][etcd-watch] | [مفاتيح وأدلة حالية][zk-watch] | [مفاتيح وبادئات حالية][consul-watch] | مشغلات (أحيانًا) |
| أذونات المستخدم | [قائمة على الأدوار][etcd-rbac] | [ACLs][zk-acl] | [ACLs][consul-acl] | تتفاوت ([GRANT][cockroach-grant] لكل جدول، [أدوار][spanner-roles] لكل قاعدة بيانات) |
| HTTP/JSON API | [نعم][etcd-json] | لا | [نعم][consul-json] | نادرًا |
| إعادة تهيئة العضوية | [نعم][etcd-reconfig] | [>3.5.0][zk-reconfig] | [نعم][consul-reconfig] | نعم |
| الحد الأقصى لحجم قاعدة البيانات الموثوقة | عدة غيغابايت | مئات الميغابايت (أحيانًا عدة غيغابايت) | مئات الميغابايت | تيرابايت فأكثر |
| الحد الأدنى لزمن خطّية القراءة | RTT الشبكة | لا خطّية للقراءة | RTT + fsync | حواجز ساعة (ذرية، NTP) |

### ZooKeeper {#zookeeper}

يحل ZooKeeper المشكلة نفسها التي يحلها etcd: تنسيق الأنظمة الموزعة وتخزين البيانات الوصفية. لكن etcd ينعم بميزة النظر إلى الوراء المستمدة من الخبرة الهندسية والتشغيلية مع تصميم ZooKeeper وتنفيذه. والدروس المستفادة من Zookeeper وجهت بالتأكيد تصميم etcd، وساعدته على دعم أنظمة واسعة النطاق مثل Kubernetes. وتشمل التحسينات التي أدخلها etcd على Zookeeper:

* إعادة تهيئة ديناميكية لعضوية العنقود
* قراءة/كتابة مستقرة تحت الحمل العالي
* نموذج بيانات بتحكم تزامن متعدد الإصدارات
* مراقبة مفاتيح موثوقة لا تُسقط الأحداث أبدًا بصمت
* بدائيات عقد إيجار تفصل الاتصالات عن الجلسات
* واجهات API لأقفال مشتركة موزعة آمنة

علاوة على ذلك، يدعم etcd طيفًا واسعًا من اللغات والأطر بصورة جاهزة للاستخدام. فبينما يمتلك Zookeeper بروتوكول RPC مخصصًا خاصًا به هو Jute، فريدًا من نوعه في Zookeeper ومحددًا لـ[روابط اللغات المدعومة][zk-bindings]، فإن بروتوكول عميل etcd مبني على [gRPC][grpc]، إطار RPC شائع له روابط لغات لـ go و C++ و Java وغيرها. وبالمثل، يمكن تحويل gRPC إلى JSON فوق HTTP، بحيث تستطيع حتى أدوات سطر الأوامر العامة مثل `curl` محادثته. وبما أن الأنظمة تستطيع الاختيار من بين خيارات شتى، فإنها تُبنى فوق etcd بأدوات أصلية بدلًا من البناء حول etcd بطقم تقنيات ثابت واحد.

عند النظر في الميزات والدعم والاستقرار، حريٌّ بالتطبيقات الجديدة التي تخطط لاستخدام Zookeeper مخزنًا متسقًا للمفاتيح/القيم أن تختار etcd بدلًا منه.

### Consul {#consul}

Consul إطار اكتشاف خدمات شامل من الطرف إلى الطرف. يوفر فحوص صحة مدمجة، وكشف أعطال، وخدمات DNS. وإضافة إلى ذلك، يكشف Consul مخزن مفاتيح/قيم عبر واجهات HTTP RESTful. [كما هو الحال في Consul 1.0][dbtester-comparison-results]، لا يتوسع نظام التخزين بالجودة نفسها التي تتوسع بها أنظمة أخرى مثل etcd أو Zookeeper في عمليات المفاتيح/القيم؛ والأنظمة التي تتطلب ملايين المفاتيح ستقاسي أزمنة استجابة مرتفعة وضغطًا على الذاكرة. وتنقص واجهة API للمفاتيح/القيم، أبرز ما فيها، المفاتيح متعددة الإصدارات، والمعاملات المشروطة، ومراقبات التدفق الموثوقة.

يحل etcd و Consul مشكلتين مختلفتين. فإن كنت تبحث عن مخزن مفاتيح/قيم متسق موزع، فإن etcd خيار أفضل من Consul. وإن كنت تبحث عن اكتشاف خدمات شامل للعنقود من الطرف إلى الطرف، فلن تكون ميزات etcd كافية؛ فاختر Kubernetes أو Consul أو SmartStack.

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

يقدم كلٌّ من etcd وقواعد بيانات NewSQL (مثل [Cockroach][cockroach] و [TiDB][tidb] و [Google Spanner][spanner]) ضمانات قوية لاتساق البيانات مع توافر عال. لكن اختلاف معاملات تصميم النظام اختلافًا كبيرًا يقود إلى واجهات API عميلة وخصائص أداء مختلفة اختلافًا كبيرًا.

قواعد بيانات NewSQL مصممة للتوسع أفقيًا عبر مراكز البيانات. تقسم هذه الأنظمة عادةً البيانات بين مجموعات نسخ متسقة متعددة (shards) يحتمل أن تكون متباعدة، وتخزن مجموعات بيانات بحجم تيرابايت فأكثر. وهذا النوع من التوسع يجعلها مرشحًا سيئًا للتنسيق الموزع لأن لديها أزمنة استجابة طويلة ناتجة عن انتظار الساعات، وتتوقع تحديثات ذات رسوم اعتماد محلية في معظمها. وتُنظم البيانات في جداول، بما في ذلك مرافق استعلام بأسلوب SQL بدلالات أغنى من etcd، لكن بثمن تعقيد إضافي في معالجة الاستعلامات وتخطيطها وتحسينها.

باختصار، اختر etcd لتخزين البيانات الوصفية أو تنسيق التطبيقات الموزعة. وإذا كان عليك تخزين أكثر من بضعة GB من البيانات أو الحاجة إلى استعلامات SQL كاملة، فاختر قاعدة بيانات NewSQL.

## استخدام etcd للبيانات الوصفية {#using-etcd-for-metadata}

ينسخ etcd جميع البيانات داخل مجموعة نسخ متسقة واحدة. ولتخزين ما يصل إلى بضعة GB من البيانات بترتيب متسق، هذا هو النهج الأكثر كفاءة. فكل تعديل لحالة العنقود، وقد يغير مفاتيح متعددة، يُعيَّن له معرف فريد شامل، يسمى في etcd مراجعة، من عداد متزايد رتيبًا للاستدلال على الترتيب. وبما أن هناك مجموعة نسخ واحدة فقط، يحتاج طلب التعديل فقط إلى المرور عبر بروتوكول raft ليُثبَّت. وبحصر الإجماع في مجموعة نسخ واحدة، يحصل etcd على اتساق موزع ببروتوكول بسيط مع تحقيق زمن استجابة منخفض ومعدل نقل عال.

النسخ الكامن خلف etcd لا يستطيع التوسع الأفقي لغياب تقسيم البيانات. في المقابل، تقسم قواعد بيانات NewSQL عادةً البيانات عبر مجموعات نسخ متسقة متعددة، وتخزن مجموعات بيانات بحجم تيرابايت فأكثر. لكن لتعيين معرف فريد شامل متزايد لكل تعديل، يجب أن يمر كل طلب عبر بروتوكول تنسيق إضافي بين مجموعات النسخ. وقد تتعارض خطوة التنسيق الإضافية هذه على المعرف الشامل، فتجبر الطلبات المرتبة على إعادة المحاولة. والنتيجة نهج أعقد بأداء أسوأ عادةً من أداء etcd للترتيب الصارم.

إن كان تطبيق يستدل بالأساس على البيانات الوصفية أو ترتيبها، مثل تنسيق العمليات، فاختر etcd. وإن كان التطبيق يحتاج مخزن بيانات كبيرًا ممتدًا عبر مراكز بيانات متعددة ولا يعتمد كثيرًا على خصائص الترتيب الشامل القوي، فاختر قاعدة بيانات NewSQL.

## استخدام etcd للتنسيق الموزع {#using-etcd-for-distributed-coordination}

يقدم etcd بدائيات تنسيق موزع مثل مراقبة الأحداث، وعقود الإيجار، والانتخابات، والأقفال المشتركة الموزعة بصورة جاهزة للاستخدام (لاحظ أنه في حالة القفل المشترك الموزع، يحتاج المستخدمون إلى الوعي بخصائصه غير البديهية. التفاصيل موصوفة أدناه). هذه البدائيات يصونها مطورو etcd ويدعمونها؛ فتركها لمكتبات خارجية تنصلٌ من مسؤولية تطوير البرمجيات الموزعة التأسيسية، وتركٌ للنظام ناقصًا فعليًا. وتتوقع قواعد بيانات NewSQL عادةً أن تكتب هذه البدائيات التنسيقية الموزعةَ أطرافٌ ثالثة. وكذلك، يشتهر ZooKeeper بمكتبة [وصفات تنسيق][curator] منفصلة ومستقلة. أما Consul، الذي يقدم واجهة API أصلية للأقفال، فيصل إلى حد الاعتذار بأنها "[ليست طريقة مضمونة][consul-bulletproof]".

نظريًا، يمكن بناء هذه البدائيات فوق أي نظام تخزين يوفر اتساقًا قويًا. لكن الخوارزميات تميل إلى الدقة؛ فمن السهل تطوير خوارزمية قفل تبدو عاملة، لتتعطل فجأة بسبب ظاهرة القطيع (thundering herd) وانحراف التوقيت. علاوة على ذلك، فإن بدائيات أخرى يدعمها etcd، مثل الذاكرة المعاملاتية، تعتمد على نموذج بيانات MVCC الخاص بـ etcd؛ فالاتساق القوي البسيط لا يكفي.

للتنسيق الموزع، يمكن لاختيار etcd أن يساعد على تفادي الصداع التشغيلي وتوفير الجهد الهندسي.

### ملاحظات حول استخدام القفل وعقد الإيجار {#notes-on-the-usage-of-lock-and-lease}
يوفر etcd [واجهات API للأقفال][etcd-v3lock] مبنية على [آلية عقد الإيجار][lease] و[تنفيذها في etcd][etcdlease]. الفكرة الأساسية لآلية عقد الإيجار هي: يمنح الخادم رمزًا، يسمى عقد إيجار (lease)، لعميل طالب. وعندما يمنح الخادم عقد إيجار، يقرن به مدة بقاء (TTL). وعندما يرصد الخادم مرور زمن أطول من TTL، يبطل عقد الإيجار. وما دام العميل يحمل عقد إيجار غير مبطل، يمكنه الادعاء بملكية الوصول إلى مورد مرتبط بعقد الإيجار. وفي حالة etcd، المورد مفتاح في فضاء مفاتيح etcd. يوفر etcd واجهات API للأقفال بهذا النظام. لكن لا يمكن استخدام واجهات API للأقفال بذاتها آليةً للاستئثار المتبادل. إنما سميت واجهات API هذه أقفالًا [لأسباب تاريخية][chubby]. ومع ذلك، يمكن استخدام واجهات API للأقفال آليةَ تحسين للاستئثار المتبادل كما هو موصوف أدناه.

أهم جانب في آلية عقد الإيجار أن TTL معرف بوصفه فاصلًا زمنيًا فيزيائيًا. فالخادم والعميل كلاهما يقيس مرور الزمن بساعاته الخاصة. ويسمح ذلك بحالة يبطل فيها الخادم عقد الإيجار لكن العميل ما زال يدعي بملكيته.

فكيف تضمن آلية عقد الإيجار الاستئثار المتبادل لآلية القفل؟ في الواقع، لا تضمن آلية عقد الإيجار ذاتها الاستئثار المتبادل. فامتلاك عقد إيجار لا يضمن أن المالك يحمل قفل المورد.

في حالة التحكم في الوصول المتبادل إلى مفاتيح etcd ذاتها بقفل etcd، ينفذ الاستئثار المتبادل استنادًا إلى آلية التحقق من رقم الإصدار (تسمى أحيانًا compare and swap في أنظمة أخرى مثل Consul). في استدعاءات RPC الخاصة بـ etcd مثل `Put` أو `Txn`، يمكننا تحديد شروط مطلوبة حول رقم المراجعة ومعرف عقد الإيجار للعمليات. فإذا لم تُستوف الشروط، فقد تفشل العملية. وبهذه الآلية، يوفر etcd قفلًا موزعًا للعملاء. ما يعني أن العميل يعرف أنه يكتسب قفل مفتاح عندما يُكمل عنقودُ etcd طلباتِه بنجاح.

في أدبيات القفل الموزع توصف تصاميم مشابهة:
* في [ورقة Chubby][chubby]، قُدِّم مفهوم *المُسلسِل (sequencer)*. ونفسر أن المُسلسِل قريب جدًا من تركيبة رقم المراجعة ومعرف عقد الإيجار في etcd.
* في [كيف تنفذ قفلًا موزعًا][fencing]، قدم Martin Kleppmann فكرة *رمز السياج (fencing token)*. ويفسر المؤلفون أن رمز السياج هو رقم المراجعة في حالة etcd.
* في [الاستخدامات العملية للساعات المتزامنة في الأنظمة الموزعة][physicalclock]، نجد وصفًا بأن Thor ينفذ آلية قفل موزع مبنية على التحقق من رقم الإصدار وعقد الإيجار.

لماذا يوفر etcd وغيره من الأنظمة عقود إيجار وهي توفر استئثارًا متبادلًا مبنيًا على التحقق من رقم الإصدار؟ حسنًا، توفر عقود الإيجار آلية تحسين لتقليل عدد الطلبات المجهضة.

لاحظ أنه في حالة مفاتيح etcd، يمكن قفلها بكفاءة بفضل آليتي عقد الإيجار والتحقق من رقم الإصدار. فإذا احتاج المستخدمون إلى حماية موارد لا علاقة لها بـ etcd، وجب أن توفر تلك الموارد آلية التحقق من رقم الإصدار واتساق النسخ مثل مفاتيح etcd. ولا يمكن استخدام ميزة القفل في etcd ذاتها لحماية موارد خارجية.

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /ar/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /ar/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /ar/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /ar/etcd/learning/data_model/
[etcd-rbac]: /ar/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /ar/etcd/op-guide/runtime-configuration
[etcd-txn]: /ar/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /ar/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
