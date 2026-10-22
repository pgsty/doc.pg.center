---
title: "ملاحظات الإصدار"
linkTitle: "الإصدارات"
weight: 60
description: "سجل إصدارات pgBackRest مع سجل تغييرات مفصّل لكل إصدار."
icon: fa-solid fa-scroll
module: [PGBACKREST]
categories: [مرجع]
upstream_link: "https://pgbackrest.org/release.html"
---

--------

## مقدمة {#introduction}

تتكون أرقام إصدارات pgBackRest من ثلاثة أجزاء: رئيسي وثانوي وتصحيحي. *قد* يكسر الإصدار الرئيسي التوافق مع الإصدار الرئيسي السابق، لكن إصدارات v2 متوافقة تمامًا مع مستودعات v1 وتقبل جميع خيارات v1. يمكن أن تتضمن الإصدارات الثانوية إصلاحات أخطاء وميزات، لكنها لا تغيّر تنسيق المستودع وتسعى إلى تجنّب تغيير الخيارات والتسميات. تتضمن الإصدارات التصحيحية إصلاحات أخطاء أحدث إصدار ثانوي.

تُجدول إصدارات الميزات في يوم الاثنين الثالث من يناير وأبريل ويوليو وأكتوبر. وتُجدول الإصدارات التصحيحية عند الحاجة في يوم الاثنين الثالث من أي شهر آخر.

يمكن العثور على توثيق الإصدار v1 [هنا](https://pgbackrest.org/1).

قد تتضمن ملاحظات الإصدار أيضًا قسم «ملاحظات إضافية»، لكن التغييرات في هذا القسم تخص التوثيق أو مجموعة الاختبارات فقط، وليس لها تأثير مباشر على قاعدة شيفرة pgBackRest.

--------

## الإصدار المستقر الموثّق {#current-stable-release}

يغطي هذا التوثيق المطابق الإصدار v2.60.0. راجع [سجل إصدارات المنبع](https://pgbackrest.org/release.html) للإصدارات الأحدث.

### ملاحظات إصدار v2.60.0 {#v2600-release-notes}

*أخطاء المجاميع الاختبارية للصفحات والجلب المسبق من تخزين الكائنات*

*صدر في 18 أكتوبر 2026*

**ملاحظة هامة**: سيُصدر الأمر `restore` الآن خطأ ويتوقف إذا احتوى أي ملف مستعاد على مجموع اختباري غير صالح لصفحة، مما يترك العنقود غير مكتمل وغير قادر على بدء التشغيل، ولذلك يجب إعادة تشغيل الاستعادة. وسيرفض الأمر `expire` الآن الحذف إذا كانت أقدم نسخة احتياطية سيُحتفظ بها ستحتوي على أخطاء في المجاميع الاختبارية، مما يمنع أيضًا حذف الأرشيف في ذلك المستودع. عيّن `checksum-page-error=n` لإصدار تحذير بدلًا من خطأ.

**الميزات:**

- إضافة الخيار `checksum-page-error` لإصدار خطأ عند وجود مجاميع اختبارية غير صالحة للصفحات. (*ساهم به Andrew Pogrebnoi. راجعه Douglas J Hunley، David Steele، Greg Sabino Mullane، Stefan Fercot. اقترحه Greg Sabino Mullane.*)

  ينطبق هذا الخيار على الأوامر `backup` و`restore` و`expire`. يُصدر الأمر `backup` افتراضيًا تحذيرًا لكل ملف كما في السابق، ويُبلغ الآن أيضًا عن العدد الإجمالي لتحذيرات المجاميع الاختبارية في نهاية النسخ الاحتياطي. أما الأمران `restore` و`expire` فيصدران خطأ افتراضيًا. في السابق لم يكن الأمر `restore` يُبلغ عن المجاميع الاختبارية غير الصالحة للصفحات إطلاقًا.

  المشكلة [#2687](https://github.com/pgbackrest/pgbackrest/issues/2687); طلب الدمج [#2833](https://github.com/pgbackrest/pgbackrest/pull/2833); الالتزام [`d7f54b2`](https://github.com/pgbackrest/pgbackrest/commit/d7f54b2245c8a9467e9a811c65626fe77739376b)
- دعم GCS Workload Identity Federation. (*ساهم به Adol Rodriguez. راجعه Douglas J Hunley، David Steele.*)

  عيّن `repo-gcs-key-type=web-id` واجعل `repo-gcs-key` يشير إلى ملف بيانات اعتماد حساب خارجي، مثل الملف الذي يولّده `gcloud iam workload-identity-pools create-cred-config`. يُستبدل رمز هوية الويب برمز وصول دون مفتاح حساب خدمة. يُعاد تحميل ملف الرمز عند كل تبادل لالتقاط الرموز التي جرى تدويرها، مثل رموز حسابات الخدمة المسقطة في Kubernetes. انتحال هوية حساب الخدمة غير مدعوم.

  المشكلة [#2838](https://github.com/pgbackrest/pgbackrest/issues/2838); طلب الدمج [#2839](https://github.com/pgbackrest/pgbackrest/pull/2839); الالتزام [`1d217e6`](https://github.com/pgbackrest/pgbackrest/commit/1d217e626301118ae2c1e7be39a6a4affa86e501)
- إضافة الجلب المسبق لقراءات ملفات أو نطاقات متعددة من مخازن الكائنات. (*راجعه Andrew Pogrebnoi، Douglas J Hunley.*)

  تُوضع الطلبات في قائمة انتظار مسبقًا قبل انتهاء القراءة الحالية، فتتقدم الطلبات أثناء القراءة، وتُقرأ الفجوات الصغيرة بين الملفات بدلًا من بدء طلب جديد. يستخدم `Restore` ذلك لقراءة الملفات المجمّعة وخرائط النسخ التزايدي على مستوى الكتل، ويستخدمه `backup` لقراءة خرائط النسخ التزايدي على مستوى الكتل من النسخة الاحتياطية السابقة. يحدد `repo-storage-prefetch` (افتراضيًا 3) عدد الطلبات الموضوعة في قائمة الانتظار، ويحدد `repo-storage-read-over` (افتراضيًا 64KiB) أكبر فجوة تُقرأ كاملةً.

  [`e63dec3`](https://github.com/pgbackrest/pgbackrest/commit/e63dec323b9e79513638b9858e4ad13b6072d060) إضافة الجلب المسبق لقراءات ملفات أو نطاقات متعددة من مخازن الكائنات.; طلب الدمج [#2783](https://github.com/pgbackrest/pgbackrest/pull/2783)

  [`5ae4015`](https://github.com/pgbackrest/pgbackrest/commit/5ae4015d37081eba4259f4de379a9d160236de0e) دمج قراءات خرائط النسخ التزايدي السابقة على مستوى الكتل أثناء النسخ الاحتياطي.; طلب الدمج [#2816](https://github.com/pgbackrest/pgbackrest/pull/2816)

**التحسينات:**

- تقليل طلبات إبقاء الاتصال إلى العمليات البعيدة. (*راجعه Douglas J Hunley.*)

  كان يُرسل طلب إبقاء اتصال إلى كل عملية بعيدة كلما اكتملت مهمة في `archive-push` و`backup`، حتى لو أُرسل طلب إلى تلك العمليات قبل لحظات. يُرسل طلب إبقاء الاتصال الآن فقط إذا لم يُرسل أي طلب إلى العملية البعيدة لمدة 30 ثانية.

  الالتزام [`f652261`](https://github.com/pgbackrest/pgbackrest/commit/f652261d32a4ffba98e7da26a41ef4ef1cd08da3)
- إعادة محاولة طلبات Azure الفرعية المفقودة من الاستجابة للطلب الدفعي. (*راجعه Douglas J Hunley.*)

  عندما يفشل حذف دفعي في Azure، قد يعيد استجابة واحدة للدفعة بأكملها. كانت الطلبات الفرعية التي لم تتلقَّ استجابة تُعد مكتملة، ولذلك لم يكن يُحذف سوى ملف واحد في كل دفعة بينما يُبلغ الأمر عن النجاح. تُعاد الآن محاولة الطلبات الفرعية التي لم تتلقَّ استجابة.

  المشكلة [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); طلب الدمج [#2849](https://github.com/pgbackrest/pgbackrest/pull/2849); الالتزام [`567a245`](https://github.com/pgbackrest/pgbackrest/commit/567a2451244e0e7a4c54e41880fac1a007b49930)
- تقليل فحوصات ملفات manifest عند إعادة إنشاء `backup.info`. (*راجعه Douglas J Hunley. اقترحه todeb.*)

  لم تعد الأوامر `backup` و`expire` و`annotate` تتحقق من وجود `backup.manifest` عندما يُظهر إدراج المستودع أن مسار النسخة الاحتياطية غير موجود، أو عندما تنتمي نسخة تفاضلية أو تزايدية إلى مجموعة نسخة احتياطية كاملة غير مدرجة في `backup.info`. كل فحص هو طلب، ولذلك يُسجَّل فحص ملف manifest المفقود في تخزين الكائنات برمز 404.

  المشكلة [#2769](https://github.com/pgbackrest/pgbackrest/issues/2769); طلب الدمج [#2825](https://github.com/pgbackrest/pgbackrest/pull/2825); الالتزام [`0d3c340`](https://github.com/pgbackrest/pgbackrest/commit/0d3c340087bfb97263c29a8fd681cf079071236b)
- استخدام الحجم الأصلي لتحديد ما إذا كان ينبغي تجميع الملف في حزمة. (*راجعه Douglas J Hunley.*)

  كان يُستخدم حجم ملف النسخ التزايدي على مستوى الكتل في النسخة الاحتياطية السابقة لتحديد تجميعه، ولذلك كان يمكن تخزين ملف تجاوز حجمه `repo-bundle-limit` داخل حزمة. يُستخدم الآن الحجم الحالي للملف.

  طلب الدمج [#2843](https://github.com/pgbackrest/pgbackrest/pull/2843); الالتزام [`340d58b`](https://github.com/pgbackrest/pgbackrest/commit/340d58bb49d6c88a002a0d23830fd37be155cc21)
- إضافة سياق إلى أخطاء قراءة خرائط الكتل أثناء النسخ الاحتياطي. (*راجعه Stefan Fercot، Douglas J Hunley.*)

  تُبلغ أخطاء قراءة خريطة الكتل لنسخة احتياطية سابقة الآن عن الملف ومسار المستودع والإزاحة وحجم الخريطة. وإذا أعادت القراءة عددًا من البايتات أقل من المتوقع، يُبلَّغ عن ذلك صراحةً بدلًا من اعتباره خطأ تحليل.

  [`bc91688`](https://github.com/pgbackrest/pgbackrest/commit/bc91688c4cf18fa6a36ec65441784533d5e6bdd5) إضافة سياق إلى أخطاء قراءة خرائط الكتل أثناء النسخ الاحتياطي.; المشكلة [#2489](https://github.com/pgbackrest/pgbackrest/issues/2489); المشكلة [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); طلب الدمج [#2830](https://github.com/pgbackrest/pgbackrest/pull/2830)

  [`f46bfaf`](https://github.com/pgbackrest/pgbackrest/commit/f46bfafdd53dd0031a320fa95b08568263901ff3) تصحيح اسم الخيار في أخطاء خرائط النسخ التزايدي على مستوى الكتل.
- تحويل `current_timestamp` إلى `text` في وسم بدء النسخ الاحتياطي. (*ساهم به Tiago Corcelli de Oliveira. راجعه David Steele.*)

  كان تحويل ضمني يعرّفه المستخدم من `timestamptz` إلى `text` يتسبب في فشل النسخ الاحتياطي بالرسالة "operator is not unique: unknown || timestamp with time zone". لم يتغير نص الوسم.

  المشكلة [#2873](https://github.com/pgbackrest/pgbackrest/issues/2873); الالتزام [`86936e1`](https://github.com/pgbackrest/pgbackrest/commit/86936e1fa60b10b7592eaac09283c4bb5991265d)
- دعم البناء على illumos. (*ساهم به Kalevi Kolttonen. راجعه Douglas J Hunley، David Steele.*)

  أُضيفت مهمة OmniOS إلى CI. قد يعمل Solaris أيضًا، لكنه لم يُختبَر.

  طلب الدمج [#2870](https://github.com/pgbackrest/pgbackrest/pull/2870); الالتزام [`ad72e58`](https://github.com/pgbackrest/pgbackrest/commit/ad72e5815f3cf9c0c6170dcbe04ef9c41762d3d9)
- دعم OpenSSL 4. (*راجعه Douglas J Hunley.*)

  كان البناء باستخدام OpenSSL 4 يفشل لأن `X509_get_subject_name()` يعيد الآن اسمًا مؤهلًا بـ `const`.

  الالتزام [`a729ac8`](https://github.com/pgbackrest/pgbackrest/commit/a729ac881f48225622151841e80146f7a3a4bce6)
- إصلاح البناء باستخدام clang. (*راجعه Douglas J Hunley.*)

  على Linux، يثبّت gcc الملف `libbacktrace.a` في موضع يبحث فيه clang أيضًا، لكنه يثبّت `backtrace.h` في موضع لا يجده إلا gcc. كان البناء باستخدام clang يعثر على المكتبة ثم يفشل في التجميع. لا تُستخدم المكتبة الآن إلا عند العثور على ترويستها. وصُححت أيضًا أنواع القيم المُعادة التي كان clang يُبلغ عنها كتحويلات تضييق في بنى التصحيح.

  [`84b031a`](https://github.com/pgbackrest/pgbackrest/commit/84b031af68fe6a30b4150ec6c903cc8c1781fc05) اشتراط وجود الترويسة عند التحقق من libbacktrace.

  [`195e66b`](https://github.com/pgbackrest/pgbackrest/commit/195e66bafd89da511fb0d48e6e053176104c47c7) إرجاع النوع المعلن من الدوال التي تعيد تعدادًا مبنيًا على StringId.

  [`d9e5e14`](https://github.com/pgbackrest/pgbackrest/commit/d9e5e14e93f460d62930f58dd4dd5bbc2a9f3a85) إرجاع bool من دالة معلن أنها تعيد bool.
- نقل توليد الشيفرة من C إلى Python.

  تُولَّد الشيفرة أثناء البناء من تعريفات الخيارات والأخطاء والمساعدة وPostgreSQL بواسطة أداة Python بدلًا من أداة C كان يجب بناؤها أولًا. يتطلب البناء من نسخة git المكتبة PyYAML بدلًا من libyaml. يتضمن أرشيف الإصدار الشيفرة المولّدة ولا يتطلب أيًا منهما.

  الالتزام [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e)

**تحسينات التوثيق:**

- تحديث تصميم الموقع. شكر خاص لـ Jan على الشعار الذكي (والمضحك جدًا). (*ساهم به David Steele، Jan Wieremjewicz. راجعه Steve Atkins، Kai Wagner، Douglas J Hunley، Nikolaos Stamatopoulos، Matt Hudson، Stefan Fercot.*)

  أصبح للموقع تصميم جديد بنمطين فاتح وداكن وتخطيط ملائم للهواتف. تعرض الصفحات ذات جدول المحتويات هذا الجدول بجانب النص وتحدد القسم الجاري قراءته. يمكن نسخ الأوامر وملفات الإعداد بزر، وتُميَّز في ملفات الإعداد الأسطر التي يغيّرها كل قسم، ويمكن توسيع ملاحظات الإصدار لعرض مزيد من التفاصيل.

  [`5bc14b5`](https://github.com/pgbackrest/pgbackrest/commit/5bc14b581a054ab3dc9cd633954a689acc99a58f) اختصار عناوين التوثيق وإزالة اللبس منها.

  [`b668d71`](https://github.com/pgbackrest/pgbackrest/commit/b668d71f22489cbd4d5e120e7e6e73be0ca9e167) نقل قائمة الرعاة إلى أسفل الصفحة الرئيسية واختصار الدعوة إلى الدعم.

  [`60b85c5`](https://github.com/pgbackrest/pgbackrest/commit/60b85c58d98dd65d47747e6355f47c934cd6b430) تحديث تصميم الموقع.

  [`ab8df23`](https://github.com/pgbackrest/pgbackrest/commit/ab8df23807cc4c11768ef40196bcade70ebec23a) عرض بطاقة بدلًا من الشعار عند نشر رابط.

  [`76ae494`](https://github.com/pgbackrest/pgbackrest/commit/76ae49456c7dace20bbd6f17e8acdfd36bf03a46) إزالة جدول المحتويات من صفحة الإصدارات وتقليل المسافة حول التاريخ.

  [`3e86c71`](https://github.com/pgbackrest/pgbackrest/commit/3e86c71f5546c86941f35d5be3a7fdcd98af3cca) استخدام روابط للخيارات بدلًا من تكرارها في مرجع الأوامر.

  [`dc3af7b`](https://github.com/pgbackrest/pgbackrest/commit/dc3af7b2aee5778dbe9200e31d5a2f95ecae5777) توضيح عناوين الأوامر في مرجع الأوامر.

  [`078d52c`](https://github.com/pgbackrest/pgbackrest/commit/078d52c5768bb67989624b5418fdd687fab9e485) تمييز الأسطر التي يغيّرها القسم في ملف الإعداد.

  [`bd33623`](https://github.com/pgbackrest/pgbackrest/commit/bd33623ba945ed251e2a6704cea14a81d51c2c9e) تمييز مخرجات الأمر بالطريقة نفسها المستخدمة لملف الإعداد.

  [`578fc2d`](https://github.com/pgbackrest/pgbackrest/commit/578fc2de14a6a739401fd58b9a232cf587c52fb4) إتاحة نسخ الأمر إلى جانب ملف الإعداد.

  [`1fb93f9`](https://github.com/pgbackrest/pgbackrest/commit/1fb93f92725124d6afa8953b7c7243aee92fcaf5) إصدار خطأ عندما لا يغيّر قسم إعداد أي شيء يمكن للقارئ رؤيته.

  [`2f3b2f2`](https://github.com/pgbackrest/pgbackrest/commit/2f3b2f22a30a35340549d42b09d5aaa58d9dfe61) جعل شعار الموقع رابطًا إلى الصفحة الرئيسية.

  [`8f902c6`](https://github.com/pgbackrest/pgbackrest/commit/8f902c66609c0bf1de6720e60552adde515209cd) تسريع بناء التوثيق.

  [`b56b6ab`](https://github.com/pgbackrest/pgbackrest/commit/b56b6ab4d24ff6298b95b415b3115591e311de20) إدراج أحدث الأخبار تلقائيًا في الصفحة الرئيسية.

  [`5b8987d`](https://github.com/pgbackrest/pgbackrest/commit/5b8987da0bb24fc3979fb764ccbde82b7b0e9500) عرض أمثلة أنواع الخيارات ككتل شيفرة في المرجع.

  [`b5d5274`](https://github.com/pgbackrest/pgbackrest/commit/b5d527471444f90df5529f15726b3d33065f9829) تمرير القائمة أفقيًا بدلًا من التفافها خارج نطاق العرض.

  [`9ae2c32`](https://github.com/pgbackrest/pgbackrest/commit/9ae2c32a35f56f53f299e8c04f004ed3386b95e4) تمييز الصفحة الحالية في القائمة بدلًا من حذفها منها.

  [`b8da5b0`](https://github.com/pgbackrest/pgbackrest/commit/b8da5b061d0f9c5d1cc01e936dc65cbdd9f70be7) إضافة إصدارات إلى روابط الأنماط والبرامج النصية لإعادة جلب الموارد المخزنة مؤقتًا عند تقادمها.

  [`ec57431`](https://github.com/pgbackrest/pgbackrest/commit/ec57431aa88860b9058d971b938afb5e35a142c7) الانتقال مباشرةً إلى القسم بدلًا من التمرير السلس إليه.

  [`46babed`](https://github.com/pgbackrest/pgbackrest/commit/46babedaed8429026efa4592d93a8d9876acad0b) إضافة تلاشي تدريجي إلى حافة القائمة التي يستمر محتواها خارجها بدلًا من قطعها بشكل حاد.

  [`17de501`](https://github.com/pgbackrest/pgbackrest/commit/17de50192b7e40d7517a4079451e93da5c39b3f3) وضع شريط عنوان section2 أسفل العنوان بدلًا من جانبه.

  [`940f431`](https://github.com/pgbackrest/pgbackrest/commit/940f4311375dda3caabdc0bdd01c36bedf43d46f) توسيط عنوان الصفحة بجانب الشعار ومحاذاته إلى اليسار عند التفافه.

  [`050ca9e`](https://github.com/pgbackrest/pgbackrest/commit/050ca9e354421530ba4282d95dead90e31d6dc2a) إضافة تفاصيل قابلة للتوسيع إلى ملاحظات الإصدار.

  [`bd8f99b`](https://github.com/pgbackrest/pgbackrest/commit/bd8f99be00cd4b03a1b234bf7fbaa39f406c0c44) إضافة تفاصيل ملاحظات الإصدارات من v2.33 إلى v2.60.

  [`28a1e3d`](https://github.com/pgbackrest/pgbackrest/commit/28a1e3d6278992e0a347aab19248abdcddefd491) تعديل تنسيق الكلمات المفتاحية في النمط الفاتح.

  [`1911f5f`](https://github.com/pgbackrest/pgbackrest/commit/1911f5f1744ff4bfee528d95e37a0a8d9b77d6b3) إنهاء سجل ملاحظات الإصدارات عند دمج upstream في CI.
- توثيق جدول الإصدارات.

  تُجدول إصدارات الميزات في يوم الاثنين الثالث من يناير وأبريل ويوليو وأكتوبر. وتُجدول الإصدارات التصحيحية عند الحاجة في يوم الاثنين الثالث من أي شهر آخر. تصف مقدمة ملاحظات الإصدار أيضًا الأجزاء الرئيسي والثانوي والتصحيحي من رقم الإصدار.

  [`9bca69a`](https://github.com/pgbackrest/pgbackrest/commit/9bca69a591abcee0623ff910d0db3e27008cfc25) توثيق جدول الإصدارات.

  [`c179f3f`](https://github.com/pgbackrest/pgbackrest/commit/c179f3f7d6d6b1963d9d3b98b981786ef9546022) تحديث شرح ترقيم الإصدارات في مقدمة ملاحظات الإصدار.
- نقل أدوات التوثيق من C وPerl إلى Python.

  يُبنى التوثيق بواسطة `doc/doc.py` بدلًا من أداة C كانت تُشغَّل عبر `doc/doc.pl`، ولم يعد بناء التوثيق يتطلب Perl.

  [`59bd2cd`](https://github.com/pgbackrest/pgbackrest/commit/59bd2cd96cfba2b02b07e81ade57d9beb5f2812e) نقل شيفرة البناء والتوثيق من C إلى Python.

  [`fa3d197`](https://github.com/pgbackrest/pgbackrest/commit/fa3d1979b77d6252642c64d708a951914e0a0ac2) نقل ما تبقى من شيفرة التوثيق من Perl إلى Python.

**تحسينات مجموعة الاختبارات:**

- نقل إطار تشغيل الاختبارات من C وPerl إلى Python.

  تُشغَّل الاختبارات بواسطة `test/test.py` بدلًا من `test/test.pl`. لم تعد حاويات الاختبار ومنفّذات CI تتطلب Perl، وأصبح إطار تشغيل الاختبارات نفسه مغطى بالاختبارات.

  [`163e5ba`](https://github.com/pgbackrest/pgbackrest/commit/163e5ba0f9ff72ec730f0b35ddac0e5d68ece531) نقل إطار تشغيل الاختبارات من C إلى Python.

  [`e25c662`](https://github.com/pgbackrest/pgbackrest/commit/e25c6621e8427e862e4ce0196d059ab651bb276d) نقل ما تبقى من إطار تشغيل الاختبارات من Perl إلى Python.
- إضافة مهمة Fil-C إلى CI.

  Fil-C تنفيذ للغة C يضمن سلامة الذاكرة ويفحص كل وصول عبر مؤشر. اكتشف حالتي قراءة خارج الحدود لم تكتشفهما gcc وclang وValgrind. وتنفّذ أيضًا آلية عمل جديدة البناء والاختبار على منفّذ CI باستخدام gcc وclang، مع المكتبات الاختيارية وبدونها.

  [`f32a5d5`](https://github.com/pgbackrest/pgbackrest/commit/f32a5d5543c4dc547006629bdb2dd52d3edb9205) إضافة آلية عمل للتجميع والاختبار على المنفّذ دون حاوية.

  [`12396fb`](https://github.com/pgbackrest/pgbackrest/commit/12396fb353bc4aa10c3739b826189e421732adf5) إضافة مهمة Fil-C إلى آلية عمل التجميع.

  [`908a11a`](https://github.com/pgbackrest/pgbackrest/commit/908a11a841e85d4e66e4aa551380b52aabfe606f) استخدام توزيعة Fil-C كما هي بعدما أصبحت تتضمن جميع المكتبات المطلوبة.
- إضافة اختبارات التشويش لقارئات `JSON` و`Ini` و`Pack`.

  تُجرى اختبارات التشويش للقارئات باستخدام libFuzzer وAddressSanitizer وUndefinedBehaviorSanitizer في CI. كشفت هذه الاختبارات أخطاء عدة في قراءة المدخلات غير الصالحة؛ مثلًا، كان يمكن لمصفوفات JSON المتداخلة بعمق في ملف معلومات أو استجابة تخزين كائنات أن تتسبب في تجاوز سعة مكدس سياقات الذاكرة.

  الالتزام [`4c65010`](https://github.com/pgbackrest/pgbackrest/commit/4c65010e7d28ea68571732fb275d91266a97ad80)
- السماح بأسماء مستخدمي الاختبار التي يرفضها adduser على Debian. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  تُبنى حاوية الاختبار باسم المستخدم نفسه الموجود على المضيف. يرفض `adduser` في Debian الأسماء التي تحتوي على نقطة، مثل `first.last`، ولذلك كان بناء الحاوية يفشل على الصور المبنية على Debian لهؤلاء المستخدمين.

  المشكلة [#2858](https://github.com/pgbackrest/pgbackrest/issues/2858); طلب الدمج [#2859](https://github.com/pgbackrest/pgbackrest/pull/2859); الالتزام [`ce19dae`](https://github.com/pgbackrest/pgbackrest/commit/ce19dae6a2d6ab3665374ead04c270fd45d563fb)


--------

## الإصدارات المستقرة {#stable-releases}

### ملاحظات إصدار v2.59.3 {#v2593-release-notes}

*خلل المفاتيح الفرعية الضعيفة للتشفير*

*صدر في 4 أكتوبر 2026*

**ملاحظة هامة**: في الإصدارات السابقة كان من الممكن أن تُولَّد مفاتيح فرعية للتشفير وأملاح ضعيفة إذا حدث خطأ أثناء الوصول إلى بيانات العشوائية الخاصة بالنظام. راجع [المفاتيح الفرعية والأملاح الضعيفة للتشفير](/ar/pgbackrest/news/#weak-encryption) لمزيد من المعلومات.

**إصلاحات الأخطاء:**

- إصلاح خطأ محتمل في المجموع الاختباري عند تحميل ملفات المعلومات والـ manifest المشفّرة. (*أصلحه j0uinim. راجعه David Steele.*)

  كان يمكن لملف معلومات أو manifest مشفّر وكبير أن يفقد أسطره الأخيرة عند تحميله، مما يؤدي إلى فشل المجموع الاختباري. كان يجب أن تتسع كتلة التشفير الأخيرة للأسطر المفقودة، ولذلك فمن غير المرجح حدوث ذلك عمليًا.

  المشكلة [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); طلب الدمج [#2868](https://github.com/pgbackrest/pgbackrest/pull/2868); الالتزام [`2def063`](https://github.com/pgbackrest/pgbackrest/commit/2def063e06c6f0b7e137309c7ed0d7631a42f6cf)
- إصلاح احتمال توليد مفاتيح فرعية/أملاح ضعيفة للتشفير. (*أصلحه j0uinim. راجعه David Steele، Stefan Fercot، Douglas J Hunley.*)

  عندما كان OpenSSL يعجز عن الحصول على بيانات عشوائية من نظام التشغيل، كان الفشل يُتجاهل وتُولَّد المفاتيح الفرعية والأملاح من ذاكرة لا تحتوي على بيانات عشوائية. يُبلَّغ الآن عن خطأ.

  المشكلة [#2866](https://github.com/pgbackrest/pgbackrest/issues/2866); طلب الدمج [#2867](https://github.com/pgbackrest/pgbackrest/pull/2867); الالتزام [`47ed78f`](https://github.com/pgbackrest/pgbackrest/commit/47ed78f8d54a44466a872852939edc0273172bf1)

### ملاحظات إصدار v2.59.2 {#v2592-release-notes}

*دعم PostgreSQL 19beta4*

*صدر في 27 سبتمبر 2026*

**إصلاحات الأخطاء:**

- إصلاح خريطة الكتل الفارغة عندما يُقتطع ملف إلى الصفر أثناء النسخ الاحتياطي. (*راجعه Douglas J Hunley. أبلغ عنه JPCOSTA78.*)

  كان ملف النسخ التزايدي على مستوى الكتل الذي يزيد حجمه على `repo-bundle-limit` ويقتطعه PostgreSQL إلى الصفر أثناء النسخ الاحتياطي يُخزَّن كخريطة كتل بلا كتل. وكانت كل نسخة احتياطية لاحقة تشير إليه تفشل بالرسالة "unexpected eof" حتى النسخة الاحتياطية الكاملة التالية.

  المشكلة [#2829](https://github.com/pgbackrest/pgbackrest/issues/2829); طلب الدمج [#2842](https://github.com/pgbackrest/pgbackrest/pull/2842); الالتزام [`572d163`](https://github.com/pgbackrest/pgbackrest/commit/572d1631026d5f10915634592b547f3439b7a291)
- تعطيل إعادة محاولة القراءة عند تمرير مرشّحات إلى المشغّل. (*راجعه Douglas J Hunley. أبلغ عنه megamaced.*)

  كانت إعادة محاولة القراءة من مستودع في تخزين كائنات عبر مضيف المستودع تتسبب في التعطل. لم يعد العميل يعيد محاولة هذه القراءات. ولا يزال مضيف المستودع يعيد محاولة قراءته من تخزين الكائنات.

  المشكلة [#2845](https://github.com/pgbackrest/pgbackrest/issues/2845); طلب الدمج [#2846](https://github.com/pgbackrest/pgbackrest/pull/2846); الالتزام [`c6eca28`](https://github.com/pgbackrest/pgbackrest/commit/c6eca28ff8e551bd2e76f0c91b1a70ddee60b35e)
- إصلاح التقسيم إلى صفحات لإدراج إصدارات S3. (*راجعه Douglas J Hunley، guruguruguru. أبلغ عنه guruguruguru.*)

  كانت قراءة المستودع في وقت مستهدف باستخدام `repo-target-time` تفشل بالرسالة "unable to find child 'NextContinuationToken'" عندما يُدرَج أكثر من ألف إصدار تحت بادئة.

  المشكلة [#2854](https://github.com/pgbackrest/pgbackrest/issues/2854); طلب الدمج [#2855](https://github.com/pgbackrest/pgbackrest/pull/2855); الالتزام [`6f0490d`](https://github.com/pgbackrest/pgbackrest/commit/6f0490dd29f0c756e6766fd9be023805540815fc)
- تعيين ترويسة إصدار Azure لمصادقة `SAS`. (*راجعه Douglas J Hunley. أبلغ عنه Florian Helmberger.*)

  يتطلب الحذف الدفعي ترويسة الإصدار، ولذلك كانت كل دفعة تُرفض عند استخدام مصادقة `SAS`. كان الرفض يبدو كفشل ملف واحد، ولم يكن يُحذف باقي كل دفعة بينما يُبلغ `expire` عن النجاح، تاركًا نسخًا احتياطية وملفات WAL منتهية الصلاحية في المستودع.

  المشكلة [#2840](https://github.com/pgbackrest/pgbackrest/issues/2840); طلب الدمج [#2848](https://github.com/pgbackrest/pgbackrest/pull/2848); الالتزام [`ea3293b`](https://github.com/pgbackrest/pgbackrest/commit/ea3293be75c86b5e6c9ca4158b5ebe2a3224f76f)
- إصلاح تعطّل `archive-push` غير المتزامن عند وجود ملف تاريخ نسخ احتياطي بحجم صفري. (*أصلحه Andrew Kroh. راجعه David Steele، Douglas J Hunley.*)

  كان ملف تاريخ نسخ احتياطي بحجم صفري، مثل الموجود في عنقود منسوخ من لقطة تخزين، يتسبب في فشل كل تشغيل غير متزامن لـ `archive-push`، فلا تُؤرشف أي ملفات WAL. يُحوَّل `archive-push-batch-size` الآن إلى عدد مقاطع باستخدام حجم أول مقطع WAL جاهز.

  المشكلة [#2856](https://github.com/pgbackrest/pgbackrest/issues/2856); طلب الدمج [#2857](https://github.com/pgbackrest/pgbackrest/pull/2857); الالتزام [`12b1b3c`](https://github.com/pgbackrest/pgbackrest/commit/12b1b3cf58caee7b04ed788eee221726f5caa155)
- إصلاح الأمر `annotate` على مستودع بعيد مشفّر. (*أصلحه Douglas J Hunley. راجعه David Steele.*)

  عندما كان المستودع مشفّرًا وكان التشفير مضبوطًا على مضيف المستودع فقط، كان `annotate` يفشل في تحميل `backup.info`.

  الالتزام [`497ad5a`](https://github.com/pgbackrest/pgbackrest/commit/497ad5aee0c654611d2ad4185958727e1341dd8c)

**الميزات:**

- دعم PostgreSQL 19beta4/rc1.

  تراجع PostgreSQL 19beta4 عن تغييرات المجاميع الاختبارية للصفحات أثناء التشغيل، فأصبح إصدار المجموع الاختباري للصفحات مقصورًا مجددًا على 0 و1. كما غيّر إصدار `pg_control` والرقم السحري لصفحة WAL.

  الالتزام [`89eae83`](https://github.com/pgbackrest/pgbackrest/commit/89eae839d5ca79591aaea8157f437688c3b53df4)

### ملاحظات إصدار v2.59.1 {#v2591-release-notes}

*دعم PostgreSQL 19beta3*

*صدر في 17 أغسطس 2026*

**إصلاحات الأخطاء:**

- إصلاح التعليق عندما يكون مخزن القطع المؤقت أصغر من المخزن المؤقت للإدخال. (*راجعه Andrew Pogrebnoi، Douglas J Hunley. أبلغ عنه crajac66.*)

  كان يمكن للتحميل متعدد الأجزاء إلى S3 أو GCS أو Azure أن يدخل في حلقة لا تنتهي عندما يكون مخزن الجزء المؤقت أصغر من مخزن الإدخال، مثلًا بعد زيادة حجم الجزء أثناء التحميل. أصبح مخزن الجزء المؤقت الآن كبيرًا بما يكفي دائمًا لاستيعاب مخزن الإدخال.

  المشكلة [#2818](https://github.com/pgbackrest/pgbackrest/issues/2818); طلب الدمج [#2819](https://github.com/pgbackrest/pgbackrest/pull/2819); الالتزام [`a53e470`](https://github.com/pgbackrest/pgbackrest/commit/a53e470eca258c2db088af55be307403c8f43b7a)
- مقارنة وسم النسخة الاحتياطية الجديد بمجموعة النسخ الاحتياطية الكاملة الخاصة بها فقط. (*راجعه Douglas J Hunley. أبلغ عنه Anton Glushakov.*)

  تستمر بعض مخازن الكائنات في إدراج بادئة بعد حذف كل ما تحتها، مثل MinIO مع قفل الكائنات أو SeaweedFS، ولذلك كان يمكن لنسخة احتياطية كاملة محذوفة أن تظل ظاهرة في المستودع. وكانت كل نسخة تفاضلية وتزايدية بعدها تفشل بالرسالة "new backup label ... is not later than latest backup label ...". يُقارَن الوسم الجديد الآن بالنسخ الاحتياطية ضمن مجموعة نسخته الاحتياطية الكاملة فقط.

  المشكلة [#2792](https://github.com/pgbackrest/pgbackrest/issues/2792); طلب الدمج [#2824](https://github.com/pgbackrest/pgbackrest/pull/2824); الالتزام [`d01f77e`](https://github.com/pgbackrest/pgbackrest/commit/d01f77e8237f5d008bb7782c18ced12cd6d1971a)
- إصلاح نقص ملفات مطلوبة للبناء في الأرشيفات المصدرية التي يولّدها GitHub. (*أبلغ عنه aardvarkzed.*)

  كانت الأرشيفات المصدرية التي يولّدها GitHub للإصدار تفتقد أدوات توليد الشيفرة والملفات التي تقرؤها، ولذلك تعذر بناؤها. يُختصر المحتوى الآن في حزمة التوزيع فقط.

  المشكلة [#2821](https://github.com/pgbackrest/pgbackrest/issues/2821); الالتزام [`163670a`](https://github.com/pgbackrest/pgbackrest/commit/163670a4eeede6d2d170b5d1f55c5ba0b66ba564)

**الميزات:**

- دعم PostgreSQL 19beta3. (*ساهم به Lardière Sébastien. راجعه David Steele.*)

  غيّر PostgreSQL 19beta3 الرقم السحري لصفحة WAL.

  الالتزام [`5cbc256`](https://github.com/pgbackrest/pgbackrest/commit/5cbc256bf37a44fa478d73a12a2e5b2d84fa6337)

**تحسينات التوثيق:**

- توثيق استثناء النقاط في أسماء حاويات S3 عندما يكون `repo-s3-uri-style=path`.

  عند استخدام `repo-s3-uri-style=path` تكون الحاوية جزءًا من المسار بدلًا من اسم المضيف، ولذلك لا تتسبب النقاط في اسم الحاوية في عدم تطابق اسم المضيف مع الشهادة.

  الالتزام [`bbdc4b9`](https://github.com/pgbackrest/pgbackrest/commit/bbdc4b9217a0e66f6a01c05f4edc04282cffb3fc)
- إزالة إعداد `hot_standby` الصريح من دليل المستخدم.

  أصبح `hot_standby` مفعّلًا افتراضيًا منذ PostgreSQL 10. يوضح دليل البدء السريع الآن أن الخادم الاحتياطي لا يقبل اتصالات للقراءة فقط بدونه.

  الالتزام [`cda454d`](https://github.com/pgbackrest/pgbackrest/commit/cda454d4bac0c0412230a0b41513659a7d0d4205)

### ملاحظات إصدار v2.59.0 {#v2590-release-notes}

*دعم PostgreSQL 19beta2*

*صدر في 20 يوليو 2026*

**ملاحظة لمعدّي الحزم**: تتوفر الآن حزمة توزيع جديدة تبسّط عملية البناء عبر توفير توثيق HTML وصفحة man وشيفرة مولّدة مسبقًا. تُرفق الحزمة بكل إصدار كأصل وتحمل الاسم `pgbackrest-{version}.tar.gz`. راجع `README.md` داخل الحزمة للتفاصيل. يرجى استخدام حزمة التوزيع الجديدة لتجنّب أدوات البناء الإضافية المطلوبة لتوليد الشيفرة في الإصدارات المستقبلية. راجع [حزمة التوزيع الجديدة](/ar/pgbackrest/news/#distribution-tarball) لمزيد من المعلومات.<br/> <br/> **ملاحظة لمعدّي الحزم**: توجد تبعية اختيارية جديدة على `libsystemd`.<br/> <br/> **ملاحظة هامة**: ابتداءً من هذا الإصدار، لا يجوز افتراضيًا تشغيل سوى الأمر `restore` بصلاحيات root. استخدم `allow-root` لتشغيل أوامر أخرى بصلاحيات root (لكن هذا غير موصى به).

**إصلاحات الأخطاء:**

- إصلاح قيام `expire` بحذف نسخة احتياطية قيد التنفيذ على مضيف آخر. (*راجعه Douglas J Hunley. أبلغ عنه Dmitrii.*)

  لا تُضاف النسخة الاحتياطية إلى `backup.info` حتى تكتمل، ولذلك عند تشغيل `expire` على مضيف بينما يجري النسخ الاحتياطي على آخر، مثل تشغيل `expire` على خادم احتياطي أثناء نسخ الخادم الأساسي، كانت النسخة الجارية تُحذف. لم يعد التنظيف يحذف أحدث نسخة احتياطية عندما تكون قيد التنفيذ أو قابلة للاستئناف.

  المشكلة [#2622](https://github.com/pgbackrest/pgbackrest/issues/2622); طلب الدمج [#2797](https://github.com/pgbackrest/pgbackrest/pull/2797); الالتزام [`aa0e215`](https://github.com/pgbackrest/pgbackrest/commit/aa0e215019f50f92a8f0c97f907affc1d3bf86c4)
- إصلاح عدم إنفاذ `archive-push-queue-max` عندما يخطئ ملف WAL. (*راجعه Stefan Fercot. أبلغ عنه vut12.*)

  في الوضع غير المتزامن، كان حجم قائمة الانتظار يُقاس وفق ملفات WAL التي لم تُرسل بعد. عندما يتكرر الخطأ في ملف WAL، كانت الملفات اللاحقة تُرسل وتتوقف عن الاحتساب رغم بقائها في `pg_wal`، فلا يُبلَغ حد قائمة الانتظار وقد يملأ `pg_wal` القرص. تُقاس قائمة الانتظار الآن وفق جميع ملفات WAL التي ينتظر PostgreSQL أرشفتها، كما في الوضع المتزامن.

  المشكلة [#2629](https://github.com/pgbackrest/pgbackrest/issues/2629); طلب الدمج [#2799](https://github.com/pgbackrest/pgbackrest/pull/2799); الالتزام [`7fe3636`](https://github.com/pgbackrest/pgbackrest/commit/7fe363658639bbc2f70e53496fa6da4acb9e481e)
- إصلاح فشل `archive-get` غير المتزامن أثناء الاسترداد عبر تبديل الخط الزمني. (*راجعه Douglas J Hunley. أبلغ عنه Jimmy Yih.*)

  كان يمكن لعمليتين غير متزامنتين أن تتنافسا على قفل الأرشيف، فتخرج العملية التي لم تحصل عليه قبل جلب المقطع الذي بدأت من أجله. وكان `archive-get` الذي شغّلها ينتظر `archive-timeout` ثم يعيد خطأ لمقطع موجود، مما قد ينهي الاسترداد مبكرًا، خصوصًا عبر تبديل الخط الزمني. يُجلب المقطع الآن مباشرةً عندما لا تكون العملية غير المتزامنة المسؤولة عن جلبه قيد التشغيل.

  المشكلة [#2423](https://github.com/pgbackrest/pgbackrest/issues/2423); طلب الدمج [#2806](https://github.com/pgbackrest/pgbackrest/pull/2806); الالتزام [`baed942`](https://github.com/pgbackrest/pgbackrest/commit/baed942af0d61fcf3c2cb1f7d1bf1d6fe5bb6df9)
- إصلاح تجاوز محتمل للمخزن المؤقت في وحدة الأخطاء. (*أصلحه Christophe Pettus. راجعه David Steele.*)

  لم تكن تتبعات المكدس الأطول من سعة مخزنها المؤقت تُنهى بمحرف إنهاء، وكان يمكن قراءتها خارج حدوده. كما كان يمكن لرسالة خطأ أطول من مخزنها أن تتسبب في الكتابة خارجه عند إلحاق خطأ نظام بها. تتطلب الحالتان رسالة طويلة على نحو غير معتاد.

  [`7fd8bc8`](https://github.com/pgbackrest/pgbackrest/commit/7fd8bc89a15cb039111aa85fd37f9dc68f7c4d6d) إصلاح تجاوز محتمل للمخزن المؤقت في وحدة الأخطاء.

  [`5ca98ab`](https://github.com/pgbackrest/pgbackrest/commit/5ca98abc91f823ef97ff6a1e77d65727d1259218) استخدام المخزن المؤقت كاملًا عند تنسيق رسائل الأخطاء.

  [`3a71dc8`](https://github.com/pgbackrest/pgbackrest/commit/3a71dc839a89b83f592c1d5813c068bcded1b6bc) منع الكتابة خارج حدود مخزن الأخطاء عند وجود رسالة تتجاوز حجمه.
- إصلاح مشكلة استخدام-بعد-التحرير (use-after-free) في عميل البروتوكول المتوازي. (*راجعه Douglas J Hunley. أبلغ عنه Georgy Shelkovy.*)

  كان العميل الذي تنتهي مهامه يُحرَّر لكنه يبقى في قائمة العملاء ويُحرَّر مجددًا في استدعاء لاحق. عند التسجيل بمستوى debug أو trace، كان ذلك يقرأ ذاكرة محررة وقد يتسبب في التعطل، مثل النسخ الاحتياطي المتوازي باستخدام `log-level-file=trace`.

  المشكلة [#2754](https://github.com/pgbackrest/pgbackrest/issues/2754); طلب الدمج [#2804](https://github.com/pgbackrest/pgbackrest/pull/2804); الالتزام [`31432ed`](https://github.com/pgbackrest/pgbackrest/commit/31432ed3977302b5e183f2b592d85afb521b4f55)
- إصلاح فيض الكومة عند تعيين خيار pg دون pg1. (*راجعه Douglas J Hunley. أبلغ عنه Naveen.*)

  عندما كانت خيارات `pg` تُضبط لفهارس أخرى دون `pg1-path`، مثل `pg2-path` و`pg3-path`، كانت خريطة الفهارس تُستبدل. كان ذلك يفسد الكومة على musl، مثل Alpine، ويسبب خطأ تجزئة. وكان يُسقط أيضًا خيار `pg-path` ذي الرقم الأعلى.

  المشكلة [#1768](https://github.com/pgbackrest/pgbackrest/issues/1768); طلب الدمج [#2796](https://github.com/pgbackrest/pgbackrest/pull/2796); الالتزام [`2d767de`](https://github.com/pgbackrest/pgbackrest/commit/2d767de3c59cf5570639e75755dc73c626fb99e1)
- إصلاح التعطل عند وصول إشارة أثناء الخروج على musl 1.2.6.

  يتعطل musl 1.2.6، مثل الموجود على Alpine 3.24، عند استدعاء `exit()` بينما تكون عملية الخروج جارية بالفعل. كان هذا يحدث عند وصول إشارة أثناء الخروج، مثل قيام الأمر `server` بإنهاء عملية ابنة بدأت الخروج بالفعل. تُتجاهل الآن الإشارة التي تصل أثناء الخروج.

  الالتزام [`e166a33`](https://github.com/pgbackrest/pgbackrest/commit/e166a33f48a00192c09b0f1cea3465243c03d1f1)

**الميزات:**

- دعم PostgreSQL 19beta1/beta2. (*راجعه Stefan Fercot.*)

  إضافة دعم PostgreSQL 19beta1/beta2. يستطيع PostgreSQL 19 تفعيل المجاميع الاختبارية للصفحات وتعطيلها أثناء التشغيل، ولا تُفحص المجاميع الاختبارية للصفحات أثناء تنفيذ أي من العمليتين.

  [`bc6d399`](https://github.com/pgbackrest/pgbackrest/commit/bc6d399a6a160f5fa41dd3a98ae046dff66e56a8) دعم PostgreSQL 19beta1.; طلب الدمج [#2779](https://github.com/pgbackrest/pgbackrest/pull/2779)

  [`2777395`](https://github.com/pgbackrest/pgbackrest/commit/2777395dacc35aec51572d3e75c621725e2f9d9c) دعم PostgreSQL 19beta2.
- إضافة خيار `archive-expire-before` لتنظيف أرشيف WAL. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  يحذف خيار `archive-expire-before` للأمر `expire` ملفات WAL التي تسبق مقطعًا معينًا من الأرشيف، لكنه لا يحذف أبدًا ملفات WAL التي تحتاج إليها نسخة احتياطية محتفظ بها. ويمكنه تنظيف الأرشيف انطلاقًا من نقطة إعادة تشغيل خادم احتياطي بواسطة `archive_cleanup_command` بدلًا من `pg_archivecleanup` الذي لا يعرف سياسة الاحتفاظ.

  [`6cd692b`](https://github.com/pgbackrest/pgbackrest/commit/6cd692b1b321faf544ee3a9b1f503fd48007d7c7) استخراج منطق حذف WAL إلى expireArchiveId().

  [`4945139`](https://github.com/pgbackrest/pgbackrest/commit/4945139392c21f197f2e307abc3c89b5548cef8d) إضافة الخيار archive-expire-before لتنظيف أرشيف WAL.; طلب الدمج [#2801](https://github.com/pgbackrest/pgbackrest/pull/2801)
- إضافة حذف دفعي لتخزين Azure. (*راجعه Douglas J Hunley، Crispy.*)

  تُحذف الملفات باستخدام Azure Blob Batch API، حتى 256 ملفًا في الطلب الواحد، بدلًا من طلب لكل ملف. يسرّع ذلك `expire` والأوامر الأخرى التي تحذف ملفات من المستودع.

  طلب الدمج [#2786](https://github.com/pgbackrest/pgbackrest/pull/2786); الالتزام [`ffa325b`](https://github.com/pgbackrest/pgbackrest/commit/ffa325b8a44c1e9e44dc038bbcc8aece6f312a90)
- إضافة دعم S3 Outposts. (*ساهم به Shiva Kumar Ambigi. راجعه David Steele، Roberto Mello.*)

  عيّن `repo-s3-service=s3-outposts` عند استخدام نقطة نهاية S3 Outposts. يحدد الخيار اسم الخدمة المستخدم في توقيع الطلبات، وقيمته الافتراضية `s3`.

  طلب الدمج [#2762](https://github.com/pgbackrest/pgbackrest/pull/2762); الالتزام [`6c51800`](https://github.com/pgbackrest/pgbackrest/commit/6c518001c24ad2405eaf750d358f69703322a221)
- إضافة مصادقة العمليات لـ S3. (*راجعه Andrew Charlton. اقترحه Andrew Charlton.*)

  عيّن `repo-s3-key-type=process` واجعل `repo-s3-process-cmd` أمرًا يُخرج بيانات اعتماد مؤقتة بتنسيق JSON الخاص بمزوّد بيانات اعتماد العمليات في AWS. تُحدَّث بيانات الاعتماد قبل انتهاء صلاحيتها.

  طلب الدمج [#2778](https://github.com/pgbackrest/pgbackrest/pull/2778); الالتزام [`b5a578a`](https://github.com/pgbackrest/pgbackrest/commit/b5a578a5c2c88d53fca0ee8cfbfb8ee662ce7e48)
- توفير حزمة توزيع تتضمن شيفرة وتوثيقًا مولّدين مسبقًا.

  تتضمن الحزمة الشيفرة المولّدة وصفحة man وتوثيق HTML الجاهزين، ولذلك تُبنى وتُثبَّت دون أدوات توليد الشيفرة والتوثيق، بما فيها `libyaml`.

  الالتزام [`8fcfef5`](https://github.com/pgbackrest/pgbackrest/commit/8fcfef5d8732055f9bc8e50224d5b7a988512e61)

**التحسينات:**

- إعادة الاتصال بتخزين SFTP بعد أن يقطع الخادم اتصالًا خاملًا. (*راجعه Stefan Fercot. اقترحه mustafa0x، tisserat.*)

  قد تُسقط خوادم SFTP والجدران النارية اتصالًا ظل خاملًا مدةً، مثل اتصال قراءة المستودع أثناء مرحلة نسخ الملفات في النسخ الاحتياطي، وكانت محاولة استخدامه التالية تفشل بخطأ مقبس. يُعاد الآن فتح الاتصال المقطوع وتُعاد محاولة العملية مرة واحدة.

  [`d72bea9`](https://github.com/pgbackrest/pgbackrest/commit/d72bea9fe7c3975fc6832a51b0b0c1c041c467d2) جلب جلسة libssh2 من التخزين في كائنات القراءة والكتابة لـ SFTP.

  [`a31febf`](https://github.com/pgbackrest/pgbackrest/commit/a31febfbd9ba639589fe57e4083ae9358b1306a4) إعادة الاتصال بتخزين SFTP بعد أن يقطع الخادم اتصالًا خاملًا.; المشكلة [#2739](https://github.com/pgbackrest/pgbackrest/issues/2739); المشكلة [#2772](https://github.com/pgbackrest/pgbackrest/issues/2772); طلب الدمج [#2793](https://github.com/pgbackrest/pgbackrest/pull/2793)
- إضافة تخزين مؤقت للمستخدم/المجموعة لتسريع بناء الـ manifest. (*ساهم به Gunnar Lindholm. راجعه David Steele.*)

  عند البحث عن أسماء المستخدمين والمجموعات عبر خدمة أسماء بعيدة، مثل sssd أو LDAP، يتطلب كل بحث رحلة طلب واستجابة، مما كان يستغرق معظم وقت بناء ملف manifest للعناقيد ذات ملايين الملفات. تُخزَّن أسماء المستخدمين والمجموعات الآن مؤقتًا.

  طلب الدمج [#2773](https://github.com/pgbackrest/pgbackrest/pull/2773); الالتزام [`1e6d23f`](https://github.com/pgbackrest/pgbackrest/commit/1e6d23fea72ac9c599f8b62a2e0a3de02d0d08d0)
- إضافة تقدم النسخ الاحتياطي لكل مستودع إلى مخرجات الأمر `info`. (*ساهم به Will Morland. راجعه David Steele، Stefan Fercot.*)

  عند إجراء النسخ الاحتياطي إلى أكثر من مستودع في الوقت نفسه، يُبلغ الأمر `info` الآن عن التقدم لكل مستودع إلى جانب التقدم الإجمالي. تحتوي مخرجات JSON على مصفوفة `repo` لكل قفل نسخ احتياطي.

  المشكلة [#2736](https://github.com/pgbackrest/pgbackrest/issues/2736); طلب الدمج [#2740](https://github.com/pgbackrest/pgbackrest/pull/2740); الالتزام [`77312b3`](https://github.com/pgbackrest/pgbackrest/commit/77312b33ba913132b33401d862c2e354f323c786)
- إضافة فحوصات `backup.info` إلى الأمر `verify`. (*ساهم به Denis Garsh. راجعه David Steele، Douglas J Hunley.*)

  يُصدر الأمر `verify` الآن تحذيرًا عندما توجد نسخة احتياطية في المستودع ولا تكون في `backup.info`، وعندما تكون نسخة في `backup.info` مفقودة من المستودع. يُبلَّغ عن النسخة المفقودة باعتبار أن ملف manifest الخاص بها مفقود.

  المشكلة [#2723](https://github.com/pgbackrest/pgbackrest/issues/2723); طلب الدمج [#2752](https://github.com/pgbackrest/pgbackrest/pull/2752); الالتزام [`7f82fb6`](https://github.com/pgbackrest/pgbackrest/commit/7f82fb6635c1e3e9dd285d53076e9aee3fbf1ca2)
- السماح بإعداد نقطة نهاية STS لـ S3. (*ساهم به Simon Gratton. راجعه David Steele.*)

  عيّن `repo-s3-sts-host` لاستخدام نقطة نهاية STS إقليمية مع `repo-s3-key-type=web-id`، مثل `sts.eu-central-2.amazonaws.com`. لا تقبل مناطق AWS التي تتطلب تفعيلًا صريحًا بيانات اعتماد من نقطة النهاية العالمية، التي تظل الافتراضية.

  المشكلة [#2791](https://github.com/pgbackrest/pgbackrest/issues/2791); طلب الدمج [#2798](https://github.com/pgbackrest/pgbackrest/pull/2798); الالتزام [`11f5582`](https://github.com/pgbackrest/pgbackrest/commit/11f5582dfe696187cab1f15d08f649a5117730b3)
- إضافة `archive-push-batch-size` لتحديد كمية WAL المدفوعة في كل تشغيل غير متزامن. (*راجعه Stefan Fercot.*)

  في الوضع غير المتزامن لا يُفحص `archive-push-queue-max` إلا عند بداية التشغيل، ولذلك كان يمكن لتشغيل يعالج تراكمًا كبيرًا أن يسمح بنمو قائمة الانتظار إلى ما يتجاوز الحد كثيرًا. يحدد `archive-push-batch-size` (افتراضيًا 16GiB) كمية WAL المرسلة في كل تشغيل، فتُفحص قائمة الانتظار مجددًا في وقت أقرب.

  طلب الدمج [#2803](https://github.com/pgbackrest/pgbackrest/pull/2803); الالتزام [`34a035f`](https://github.com/pgbackrest/pgbackrest/commit/34a035f4d62f06822c1f60f72a605762cc1ad79c)
- الخروج من `archive-push` غير المتزامن عند أول خطأ. (*راجعه Stefan Fercot. اقترحه Lardière Sébastien.*)

  عندما كان المستودع غير متاح، كانت العملية غير المتزامنة تواصل محاولة إرسال كل مقطع WAL جاهز، وقد يستغرق التشغيل وقتًا يكفي لامتلاء `pg_wal` قبل فحص `archive-push-queue-max` مجددًا. يخرج التشغيل الآن عند أول خطأ، بعد اكتمال المهام الجارية.

  المشكلة [#1848](https://github.com/pgbackrest/pgbackrest/issues/1848); طلب الدمج [#2802](https://github.com/pgbackrest/pgbackrest/pull/2802); الالتزام [`a0c1435`](https://github.com/pgbackrest/pgbackrest/commit/a0c14359392e283d88f72e7f9f815d9e78ddfb10)
- تقوية تحليل استجابات HTTP المجزّأة. (*ساهم به Shubham. راجعه David Steele.*)

  أصبحت امتدادات الأجزاء والترويسات الختامية مقبولة، وتُقارَن `transfer-encoding` دون مراعاة حالة الأحرف، وتُرفض الاستجابة التي تحتوي على كل من `transfer-encoding` و`content-length`.

  طلب الدمج [#2785](https://github.com/pgbackrest/pgbackrest/pull/2785); الالتزام [`34bba82`](https://github.com/pgbackrest/pgbackrest/commit/34bba828c6ba97579d65c2199c02d94bf31257a5)
- إصدار خطأ عند التشغيل بصلاحيات root ما لم يُمكَّن `allow-root`. (*راجعه Douglas J Hunley.*)

  كان تشغيل أمر غير `restore` بصلاحيات root قد ينشئ ملفات في المستودع، مثل `backup.info`، لا يستطيع مستخدم PostgreSQL الوصول إليها. يُعطَّل `allow-root` افتراضيًا لكل أمر باستثناء `restore`، وينطبق الفحص أيضًا على المضيفين البعيدين.

  المشكلة [#1693](https://github.com/pgbackrest/pgbackrest/issues/1693); طلب الدمج [#2812](https://github.com/pgbackrest/pgbackrest/pull/2812); الالتزام [`0daf53d`](https://github.com/pgbackrest/pgbackrest/commit/0daf53da03fb179b5771b6aaa559f9e0cc5842bb)
- تقليل عمليات البحث الثنائي عند بناء الـ manifest. (*ساهم به Gunnar Lindholm. راجعه David Steele.*)

  كان بناء ملف manifest لنسخة تفاضلية أو تزايدية يبحث في ملف manifest السابق ثلاث مرات لكل ملف. يجري البحث الآن مرة واحدة، مما يوفر ملايين عمليات البحث للعناقيد ذات ملايين الملفات.

  طلب الدمج [#2774](https://github.com/pgbackrest/pgbackrest/pull/2774); الالتزام [`f1ef629`](https://github.com/pgbackrest/pgbackrest/commit/f1ef62956adabf305a7e959477ea1bb668fd8d65)
- تحسين أداء seek أثناء استعادة دلتا التزايدي بالكتل. (*راجعه David Christensen، Douglas J Hunley.*)

  كان يُجرى تغيير موضع القراءة والكتابة وتفريغ مخزن الكتابة لكل كتلة تُكتب أثناء استعادة دلتا لنسخ تزايدي على مستوى الكتل، وغالبًا ما تكون الكتل بحجم 8KiB. يُتتبَّع موضع الملف الآن، ولا يُجرى تغيير الموضع والتفريغ إلا عند الحاجة.

  طلب الدمج [#2732](https://github.com/pgbackrest/pgbackrest/pull/2732); الالتزام [`b908d5e`](https://github.com/pgbackrest/pgbackrest/commit/b908d5e2c5b37ef968f19e2c40a1001e19e5b87f)
- تجميع ملفات النسخة الاحتياطية بالترتيب بدلًا من المسح بحثًا عن تطابق أفضل. (*راجعه Stefan Fercot.*)

  كان الملف الذي سيرفع حجم الحزمة فوق `repo-bundle-size` يُتجاوز لصالح ملف أصغر لاحق في قائمة الانتظار. تُضاف الملفات الآن بالترتيب وتُغلق الحزمة بمجرد بلوغ `repo-bundle-size`، ولذلك قد تتجاوزه بمقدار يصل إلى `repo-bundle-limit`.

  طلب الدمج [#2794](https://github.com/pgbackrest/pgbackrest/pull/2794); الالتزام [`253dbc3`](https://github.com/pgbackrest/pgbackrest/commit/253dbc3f03e5581c98bb97b252dc77b8defd3693)
- الإبلاغ عن الخطأ الكامن عندما يفشل استعلام في الاكتمال. (*راجعه Andrew Pogrebnoi. اقترحه Marco Fontana.*)

  عندما كان الاتصال ينقطع بعد تسليم أول نتيجة لاستعلام، مثلًا تحت الحمل، كانت تظهر الرسالة العامة "NULL result required to complete request". يُبلَّغ الآن عن خطأ PostgreSQL مع تلميحات بشأن فقدان الاتصال والإعدادات الصارمة جدًا لـ `idle_session_timeout` و`idle_in_transaction_session_timeout`.

  المشكلة [#2789](https://github.com/pgbackrest/pgbackrest/issues/2789); طلب الدمج [#2790](https://github.com/pgbackrest/pgbackrest/pull/2790); الالتزام [`23e966c`](https://github.com/pgbackrest/pgbackrest/commit/23e966cd8f17a8cd446b04901d0ae66ebf4118ee)
- الإبلاغ عن الخطأ الفعلي عند فشل طلب بيانات اعتماد S3. (*راجعه Douglas J Hunley. اقترحه Mitchell Grice.*)

  كان خطأ AWS في طلب بيانات اعتماد `web-id` أو `pod-id` يُبلَّغ عنه كفشل في تحليل الاستجابة. يُبلَّغ الآن عن الخطأ الذي تعيده AWS، وتُحجب الرموز عند تسجيل الطلب.

  المشكلة [#1997](https://github.com/pgbackrest/pgbackrest/issues/1997); طلب الدمج [#2808](https://github.com/pgbackrest/pgbackrest/pull/2808); الالتزام [`b0c57c2`](https://github.com/pgbackrest/pgbackrest/commit/b0c57c280d727e743b72a6d86e2c3e413307e44b)
- الإبلاغ عن أخطاء مسار spool للأمر `archive-push` في سجل PostgreSQL. (*راجعه Douglas J Hunley. اقترحه Don Seiler.*)

  عندما كان يتعذر إنشاء مسار spool غير المتزامن، مثلًا بسبب رفض الإذن، لم يكن من الممكن كتابة الخطأ إلى spool، وكان `archive-push` يفشل بمهلة عامة تشير إلى السجل غير المتزامن. يُنشأ مسار spool الآن قبل بدء العملية غير المتزامنة، فيظهر الخطأ في سجل PostgreSQL.

  المشكلة [#1408](https://github.com/pgbackrest/pgbackrest/issues/1408); طلب الدمج [#2810](https://github.com/pgbackrest/pgbackrest/pull/2810); الالتزام [`7b0159c`](https://github.com/pgbackrest/pgbackrest/commit/7b0159c7dfd69763b63b1385fd564c18a4a5c1bc)
- التلميح إلى أن pgBackRest قد يكون قديمًا عند وجود إصدار غير مدعوم.

  عندما لا يتعرف pgBackRest على إصدار PostgreSQL، مثل وجود pgBackRest قديم على مضيف الاستعادة يقرأ نسخة احتياطية لعنقود أحدث، يلمّح الخطأ الآن إلى احتمال الحاجة لتحديث pgBackRest على جميع المضيفين. يُعرض الإصدار بصيغة مفهومة للمستخدم، مثل 13 بدلًا من 130000.

  الالتزام [`d4f697e`](https://github.com/pgbackrest/pgbackrest/commit/d4f697ebce705f9439798f970103fd38f829dfff)
- إضافة تكامل إشعارات systemd. (*ساهم به Andrew Jackson. راجعه David Steele.*)

  عند البناء مع `libsystemd`، يُخطر الأمر `server` خدمة systemd عندما يكون جاهزًا لقبول الاتصالات وعندما يتوقف، كما يفعل PostgreSQL وPgBouncer.

  المشكلة [#2757](https://github.com/pgbackrest/pgbackrest/issues/2757); طلب الدمج [#2760](https://github.com/pgbackrest/pgbackrest/pull/2760); الالتزام [`742fff1`](https://github.com/pgbackrest/pgbackrest/commit/742fff174a3f5baaed932afa284334ca2aa1be82)
- كتم أخطاء `unused parameter` في فحوصات المُجمِّع في meson. (*ساهم به Jörg Plate. راجعه David Steele.*)

  كانت اختبارات المُجمِّع في meson تعلن معاملات لـ `main()` لا تستخدمها، مما كان يفشل الاختبارات عند اعتبار تحذيرات المعاملات غير المستخدمة أخطاء.

  المشكلة [#2724](https://github.com/pgbackrest/pgbackrest/issues/2724); الالتزام [`d4465bd`](https://github.com/pgbackrest/pgbackrest/commit/d4465bd6f78d6d58d18ebedbe8f63b55d0ae2508)
- أصبح C11 الآن الحد الأدنى لمعيار C. (*راجعه Mohammad Ali Nazir Kosar.*)

  طلب الدمج [#2738](https://github.com/pgbackrest/pgbackrest/pull/2738); الالتزام [`3a6c671`](https://github.com/pgbackrest/pgbackrest/commit/3a6c67183cd9c6a12c24f0d978ef5e501b7c3fcf)

**تحسينات التوثيق:**

- جعل خيار `stanza` داخليًا لأوامر `repo-*`. (*راجعه Stefan Fercot.*)

  لا يؤثر الخيار `stanza` في أوامر `repo-*` إلا مع ثوابت مسارات التخزين غير الموثقة، ولذلك كان التوثيق يوحي بأنه يؤدي وظيفة لا يؤديها. لم يعد الخيار موثقًا لهذه الأوامر، ويعمل كما كان.

  المشكلة [#2735](https://github.com/pgbackrest/pgbackrest/issues/2735); الالتزام [`3e9eabd`](https://github.com/pgbackrest/pgbackrest/commit/3e9eabd8a5551cdaeb6bc78a52f000eaf239defb)
- توثيق أن info يقرأ إعدادات التشفير من القسم العام. (*راجعه Stefan Fercot. اقترحه Ron Johnson.*)

  عند تشغيل الأمر `info` دون `stanza`، فإنه يقرأ إعدادات التشفير من القسم العام فقط، ولذلك تتطلب إعدادات التشفير المضبوطة لمقطع stanza تحديد `stanza`.

  المشكلة [#1407](https://github.com/pgbackrest/pgbackrest/issues/1407); طلب الدمج [#2805](https://github.com/pgbackrest/pgbackrest/pull/2805); الالتزام [`2137bda`](https://github.com/pgbackrest/pgbackrest/commit/2137bda1a5a1ad890d0137feffe8491102041af3)
- توثيق أن `expire-auto` يستخدم إعداد الأمر `backup`. (*راجعه Stefan Fercot. اقترحه Lardière Sébastien.*)

  يستخدم التنظيف التلقائي بعد النسخ الاحتياطي إعداد الأمر `backup`، ولذلك لا تُطبَّق الخيارات المضبوطة للأمر `expire` فقط. عطّل `expire-auto` وشغّل `expire` بشكل منفصل عندما يحتاج إلى إعداداته الخاصة.

  المشكلة [#1874](https://github.com/pgbackrest/pgbackrest/issues/1874); طلب الدمج [#2807](https://github.com/pgbackrest/pgbackrest/pull/2807); الالتزام [`cf847f9`](https://github.com/pgbackrest/pgbackrest/commit/cf847f94cd7ab6517ec1abb30075fb53dc75d5f8)
- توثيق تعديل توجيه `su` في logrotate للمستخدم المخصص. (*راجعه Douglas J Hunley. اقترحه lkanbus.*)

  قد تثبّت الحزم إعداد logrotate الذي يدوّر السجلات باسم المستخدم `postgres`. عندما يملك مستخدم مخصص المستودع والسجلات، يجب تغيير توجيه `su` إلى ذلك المستخدم، وإلا تفشل عملية التدوير بخطأ إذن.

  المشكلة [#2737](https://github.com/pgbackrest/pgbackrest/issues/2737); طلب الدمج [#2809](https://github.com/pgbackrest/pgbackrest/pull/2809); الالتزام [`bde2c50`](https://github.com/pgbackrest/pgbackrest/commit/bde2c509c923fbe2844c10b0f95c55973378d2ae)
- توثيق أن التعليقات في نهاية السطر غير مدعومة في ملفات الإعداد. (*راجعه Douglas J Hunley. اقترحه Alex Richman.*)

  لم تكن التعليقات في نهاية السطر مدعومة قط، رغم أنها قد تبدو عاملة لبعض الخيارات. تُدعَم فقط التعليقات المكتوبة في سطر مستقل.

  المشكلة [#1633](https://github.com/pgbackrest/pgbackrest/issues/1633); طلب الدمج [#2811](https://github.com/pgbackrest/pgbackrest/pull/2811); الالتزام [`8571799`](https://github.com/pgbackrest/pgbackrest/commit/85717992cadbfdabc571fb23914b62b08c7f6f44)

**تحسينات مجموعة الاختبارات:**

- إصلاح تعارضات المجموعات في Alpine داخل حاويات CI. (*ساهم به Artur Zakirov. راجعه David Steele.*)

  تُعالَج الآن إدخالات المجموعات التي تضم أعضاء عند إعادة تسمية مجموعة الاختبار، ولا تُنشأ مجموعة Alpine إلا إذا لم تكن موجودة بالفعل.

  طلب الدمج [#2784](https://github.com/pgbackrest/pgbackrest/pull/2784); الالتزام [`760dd8d`](https://github.com/pgbackrest/pgbackrest/commit/760dd8db69e7c6e5cbb9c5b7e2067b6813cf4497)

### ملاحظات إصدار v2.58.0 {#v2580-release-notes}

*تحسينات تخزين الكائنات*

*صدر في 19 يناير 2026*

**ملاحظة هامة**: ارتفعت القيم الدنيا لخيار `repo-storage-upload-chunk-size`. وهي تمثل الآن الحد الأدنى المسموح به من قبل المزوّدين.

**إصلاحات الأخطاء:**

- إصلاح جمود ناتج عن التسجيل داخل معالج الإشارات. (*أصلحه Maxim Michkov. راجعه David Steele.*)

  كان يمكن لإشارة تصل أثناء احتفاظ `gmtime_r()` بقفل، مثل SIGTERM التي يرسلها `stop` مع `--force`، أن تسبب حالة جمود عندما يسجّل معالج الإشارة رسالة. يستخدم معالج الإشارة الآن في التسجيل دوال آمنة للإشارات غير المتزامنة فقط.

  المشكلة [#2710](https://github.com/pgbackrest/pgbackrest/issues/2710); طلب الدمج [#2715](https://github.com/pgbackrest/pgbackrest/pull/2715); الالتزام [`e13c462`](https://github.com/pgbackrest/pgbackrest/commit/e13c462908c6ee25f8795b5d1373981549d4d5cf)

**الميزات:**

- دعم HTTP لـ S3 وGCS وAzure. (*ساهم به Will Morland. راجعه David Steele.*)

  يمكن لنقطة نهاية تخزين الكائنات الآن أن تبدأ بـ `http://` للاتصال دون TLS. ويظل HTTPS مستخدمًا عندما لا تحدد نقطة النهاية بروتوكولًا.

  المشكلة [#2340](https://github.com/pgbackrest/pgbackrest/issues/2340); طلب الدمج [#2703](https://github.com/pgbackrest/pgbackrest/pull/2703); الالتزام [`2398dd4`](https://github.com/pgbackrest/pgbackrest/commit/2398dd4d432d312b3641e9fbbcbe0487ad43112d)
- السماح بإنهاء صلاحية أقدم نسخة احتياطية كاملة بغض النظر عن الاحتفاظ الحالي. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Ron Johnson.*)

  يحذف خيار `--oldest` للأمر `expire` أقدم نسخة احتياطية كاملة والنسخ المعتمدة عليها بغض النظر عن إعدادات الاحتفاظ، مثلًا عندما توشك مساحة المستودع على النفاد. وتُحذف أيضًا ملفات WAL التي تسبق أقدم نسخة احتياطية كاملة متبقية.

  المشكلة [#2666](https://github.com/pgbackrest/pgbackrest/issues/2666); طلب الدمج [#2709](https://github.com/pgbackrest/pgbackrest/pull/2709); الالتزام [`bf2b276`](https://github.com/pgbackrest/pgbackrest/commit/bf2b276dc011464b13039630870934fd42ca473c)
- دعم الهويات المُدارة في Azure. (*ساهم به Moiz Ibrar، Matthew Mols. راجعه David Steele.*)

  عيّن `repo-azure-key-type=auto` لجلب بيانات الاعتماد تلقائيًا باستخدام الهويات المُدارة بدلًا من إعدادها يدويًا. تُحدَّث بيانات الاعتماد قبل انتهاء صلاحيتها.

  المشكلة [#2023](https://github.com/pgbackrest/pgbackrest/issues/2023); طلب الدمج [#2712](https://github.com/pgbackrest/pgbackrest/pull/2712); الالتزام [`38f14d7`](https://github.com/pgbackrest/pgbackrest/commit/38f14d73b6a62d06e1ead7942e49a2bb2ae90dab)
- دعم ***تجريبي*** لهوية pod في EKS لـ S3. (*ساهم به Pierre BOUTELOUP. راجعه David Steele.*)

  عيّن `repo-s3-key-type=pod-id` لجلب بيانات الاعتماد تلقائيًا باستخدام هوية pod في EKS بدلًا من إعدادها يدويًا. تُحدَّث بيانات الاعتماد قبل انتهاء صلاحيتها.

  المشكلة [#2718](https://github.com/pgbackrest/pgbackrest/issues/2718); طلب الدمج [#2719](https://github.com/pgbackrest/pgbackrest/pull/2719); الالتزام [`79544f6`](https://github.com/pgbackrest/pgbackrest/commit/79544f64a3ce198f4685f923739def997fcafbce)
- السماح بإعداد مجموعات تشفير TLS. (*ساهم به Gunnar "Nick" Bluth. راجعه David Steele.*)

  عيّن `tls-cipher-12` لـ TLS 1.2 و`tls-cipher-13` لـ TLS 1.3، مثلًا للامتثال للمتطلبات. تنطبق مجموعات التشفير على كل اتصال تنشئه العملية.

  [`fbc607a`](https://github.com/pgbackrest/pgbackrest/commit/fbc607a48b1fb4ae65c9f2691c44453f02aef2b8) إتاحة إعداد مجموعات تشفير TLS.; المشكلة [#2697](https://github.com/pgbackrest/pgbackrest/issues/2697); طلب الدمج [#2700](https://github.com/pgbackrest/pgbackrest/pull/2700)

  [`91ad655`](https://github.com/pgbackrest/pgbackrest/commit/91ad65537f55aa3825b6c7b626a9e1b7cbb1ad4c) إصلاح اختبار الوحدة المتذبذب common/io-tls المضاف في fbc607a4.
- السماح بتعيين أولوية العملية. (*راجعه Douglas J Hunley.*)

  يضبط `priority` أولوية جدولة عمليات pgBackRest من -20 إلى 19، كما يفعل `nice`. تقلل القيمة الأعلى احتمال تأثير pgBackRest في أداء PostgreSQL.

  طلب الدمج [#2693](https://github.com/pgbackrest/pgbackrest/pull/2693); الالتزام [`0fc7e96`](https://github.com/pgbackrest/pgbackrest/commit/0fc7e96f5addb01e7f6f3585e37d209cc17dd956)

**التحسينات:**

- السماح بالنقاط في أسماء حاويات S3 عند استخدام URI بنمط المسار. (*ساهم به Joakim Hindersson. راجعه David Steele.*)

  لا تتسبب النقاط في اسم الحاوية في عدم تطابق اسم المضيف مع الشهادة إلا مع عناوين URI التي تستخدم نمط المضيف. ولذلك أصبحت مسموحة مع `repo-s3-uri-style=path` الذي تستخدمه معظم خدمات S3 المستضافة ذاتيًا.

  طلب الدمج [#2713](https://github.com/pgbackrest/pgbackrest/pull/2713); الالتزام [`3fdb4a1`](https://github.com/pgbackrest/pgbackrest/commit/3fdb4a1ea00b442aca5fc714818d293d57490386)
- اشتراط TLS >= 1.2 ما لم يُعطَّل التحقق. (*راجعه Douglas J Hunley، Gunnar "Nick" Bluth.*)

  أصبح TLS 1.0 و1.1 مهملين منذ عام 2021. يكون التحقق مفعّلًا دائمًا للاتصالات بين مضيفي pgBackRest. وعندما يُعطَّل التحقق لتخزين كائنات بواسطة `repo-storage-verify-tls`، مثلًا لشهادة موقعة ذاتيًا، يُسمح بجميع إصدارات البروتوكول.

  طلب الدمج [#2720](https://github.com/pgbackrest/pgbackrest/pull/2720); الالتزام [`5b4b20a`](https://github.com/pgbackrest/pgbackrest/commit/5b4b20a8d7d17c2bffe106595310853e3f3a9604)
- تحجيم قطع S3/GCS/Azure ديناميكيًا للرفعات الكبيرة. (*راجعه Douglas J Hunley. اقترحه Timothée Peignier.*)

  عدد الأجزاء في التحميل محدود، ولذلك مع القيمة الافتراضية لـ `repo-storage-upload-chunk-size` كان أكبر ملف قابل للتحميل بحجم 50GiB إلى S3 و40GiB إلى GCS و200GiB إلى Azure. يزداد حجم الجزء الآن أثناء التحميل، فيمكن تحميل ملفات حتى 5TiB إلى S3 وGCS وحتى 45TiB إلى Azure.

  المشكلة [#2679](https://github.com/pgbackrest/pgbackrest/issues/2679); طلب الدمج [#2701](https://github.com/pgbackrest/pgbackrest/pull/2701); الالتزام [`86554fa`](https://github.com/pgbackrest/pgbackrest/commit/86554faa707292855c2776a0c70b5e212b1e3945)
- تحسين حجم قطع S3/GCS/Azure للملفات الصغيرة. (*راجعه Douglas J Hunley.*)

  كان مخزن الجزء المؤقت يُخصَّص كاملًا عند فتح الملف، رغم أن كثيرًا من الملفات أصغر من جزء واحد. ينمو المخزن الآن مع وصول البيانات، مما يوفر الذاكرة عند تحميل ملفات صغيرة.

  طلب الدمج [#2705](https://github.com/pgbackrest/pgbackrest/pull/2705); الالتزام [`28bfa20`](https://github.com/pgbackrest/pgbackrest/commit/28bfa20ba3b860f72ba7ab6c018e37ada99e2109)
- إزالة دعم PostgreSQL `9.5`. (*راجعه Douglas J Hunley.*)

  لم يعد PostgreSQL 9.5 مدعومًا، وفق سياسة دعم خمسة إصدارات من PostgreSQL انتهى عمر دعمها.

  طلب الدمج [#2692](https://github.com/pgbackrest/pgbackrest/pull/2692); الالتزام [`5171e8b`](https://github.com/pgbackrest/pgbackrest/commit/5171e8bde31b9711c9c5b4ccc5170b61c5235548)
- تحسين تسجيل القيمة الافتراضية للخيارات ذات التبعية غير المحلولة. (*راجعه Stefan Fercot.*)

  كان الخيار المضبوط في ملف الإعداد يُسجَّل عند بدء الأمر عندما لا تكون تبعيته مستوفاة، رغم استخدام قيمته الافتراضية. لم يعد الخيار يُسجَّل في هذه الحالة.

  المشكلة [#2707](https://github.com/pgbackrest/pgbackrest/issues/2707); طلب الدمج [#2708](https://github.com/pgbackrest/pgbackrest/pull/2708); الالتزام [`38ac638`](https://github.com/pgbackrest/pgbackrest/commit/38ac6387cbbfc6f78a686de657e5a4de4ed59295)

**تحسينات التوثيق:**

- إزالة إعداد `max_wal_senders`/`wal_level` الصريح من دليل المستخدم. (*اقترحه Jamie Nguyen.*)

  أصبحت القيم الافتراضية لـ `max_wal_senders` و`wal_level` منذ PostgreSQL 10 مطابقةً للقيم التي يتطلبها دليل المستخدم.

  المشكلة [#2699](https://github.com/pgbackrest/pgbackrest/issues/2699); الالتزام [`bce97d3`](https://github.com/pgbackrest/pgbackrest/commit/bce97d3ea80675b8eab3dbf692e8bc8f077f30c7)
- توضيح أن التجميع مفيد لأنظمة الملفات ذات أحجام الكتل الكبيرة. (*اقترحه Ron Johnson.*)

  يوفر تجميع الملفات مساحة على أنظمة الملفات ذات أحجام الكتل الكبيرة، حيث يشغل كل ملف صغير كتلة كاملة.

  المشكلة [#2706](https://github.com/pgbackrest/pgbackrest/issues/2706); الالتزام [`a7e5f28`](https://github.com/pgbackrest/pgbackrest/commit/a7e5f28511c27f2504a873db26803b26a84df8f1)

### ملاحظات إصدار v2.57.0 {#v2570-release-notes}

*منع الروابط الرمزية في المستودع*

*صدر في 18 أكتوبر 2025*

**إصلاحات الأخطاء:**

- إلغاء تداخل مهل HTTP/TLS/المقابس. (*راجعه David Christensen.*)

  كانت طبقتا TLS وHTTP تعيدان أيضًا محاولة اتصال المقبس الفاشل، ولذلك مع `io-timeout` الافتراضي البالغ 60 ثانية كان انتهاء مهلة الاتصال يستغرق تسع دقائق. تعيد كل طبقة الآن محاولة إخفاقاتها الخاصة فقط.

  المشكلة [#2654](https://github.com/pgbackrest/pgbackrest/issues/2654); طلب الدمج [#2662](https://github.com/pgbackrest/pgbackrest/pull/2662); الالتزام [`9c7f064`](https://github.com/pgbackrest/pgbackrest/commit/9c7f0648648e651d82918e5dbfc3d511abee3298)
- إصلاح خطأ تقسيم محتمل في رسالة خطأ مجموع تحقق الصفحات. (*أصلحه Zsolt Parragi. راجعه David Steele.*)

  كانت رسالة خطأ المجاميع الاختبارية غير الصالحة للصفحات تستخدم سلسلة خرجت من نطاق صلاحيتها، مما قد يسجّل بيانات غير مفهومة أو يسبب التعطل. وكان ذلك أرجح مع pg_tde لأن كل ملف مشفّر يفشل في فحص المجموع الاختباري للصفحة.

  طلب الدمج [#2675](https://github.com/pgbackrest/pgbackrest/pull/2675); الالتزام [`adc5e5b`](https://github.com/pgbackrest/pgbackrest/commit/adc5e5b23b9b544745724a7eaa0461b88b691e36)
- إصلاح خطأ تجزئة محتمل في رسائل استئناف النسخ الاحتياطي.

  كانت الرسالة التي تشرح سبب تعذر استئناف النسخ الاحتياطي تستخدم سلسلة خرجت من نطاق صلاحيتها، مما قد يسجّل بيانات غير مفهومة أو يسبب التعطل.

  الالتزام [`c1c40a4`](https://github.com/pgbackrest/pgbackrest/commit/c1c40a4a851efe98be83aca2044c02fd1c7fb2ae)

**الميزات:**

- إضافة خيار `repo-symlink` لمنع إنشاء الروابط الرمزية في المستودع. (*راجعه Douglas J Hunley. اقترحه Ron Johnson.*)

  بعض أنظمة الملفات المتوافقة مع Posix من النواحي الأخرى لا تدعم الروابط الرمزية. عيّن `repo-symlink=n` لمنع إنشاء الرابط `latest` وروابط مساحات الجداول الرمزية في المستودع.

  المشكلة [#2673](https://github.com/pgbackrest/pgbackrest/issues/2673); طلب الدمج [#2674](https://github.com/pgbackrest/pgbackrest/pull/2674); الالتزام [`bfd9790`](https://github.com/pgbackrest/pgbackrest/commit/bfd97907311a25ed239798691cff52cf73acdb83)

**التحسينات:**

- إضافة إعادة محاولة HTTP لأخطاء 408 و429. (*راجعه David Christensen.*)

  تُعاد الآن محاولة الطلبات التي تفشل بأخطاء HTTP 408 (Request Timeout) و429 (Too Many Requests). أخطاء 429 شائعة على Cloudflare R2.

  طلب الدمج [#2661](https://github.com/pgbackrest/pgbackrest/pull/2661); الالتزام [`8733900`](https://github.com/pgbackrest/pgbackrest/commit/87339004e59c03d2a03a6ceb8426202346849c37)

### ملاحظات إصدار v2.56.0 {#v2560-release-notes}

*تحسينات معلومات التقدم*

*صدر في 21 يوليو 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة في إنهاء الصلاحية عند الطلب عندما لا توجد نسخ احتياطية في مستودع. (*راجعه Stefan Fercot. أبلغ عنه Anup Gupta.*)

  كان الحذف المخصص يفشل بالرسالة "cannot get index 0 from list with 0 value(s)" عندما لا توجد نسخ احتياطية في المستودع.

  المشكلة [#2645](https://github.com/pgbackrest/pgbackrest/issues/2645); طلب الدمج [#2646](https://github.com/pgbackrest/pgbackrest/pull/2646); الالتزام [`638815b`](https://github.com/pgbackrest/pgbackrest/commit/638815b4cde1ba1322516e256742c51676af66f0)

**الميزات:**

- إضافة تقدم الاستعادة إلى مخرجات الأمر `info`. (*ساهم به Denis Garsh، Maxim Michkov. راجعه David Steele.*)

  يسجّل الأمر `restore` الآن تقدمه، ويعرضه الأمر `info` إلى جانب تقدم النسخ الاحتياطي. كذلك لم يعد الأمر `stop` ينهي عملية الاستعادة.

  المشكلة [#2546](https://github.com/pgbackrest/pgbackrest/issues/2546); طلب الدمج [#2652](https://github.com/pgbackrest/pgbackrest/pull/2652); الالتزام [`8cdd9ce`](https://github.com/pgbackrest/pgbackrest/commit/8cdd9ce1c4ab6cca508932a41a3013374d7547ef)
- إضافة مستوى تفصيل للتقدم فقط لمخرجات الأمر `info`. (*ساهم به Denis Garsh. راجعه David Steele، Stefan Fercot.*)

  عيّن `--detail-level=progress` لعرض التقدم فقط، وهو أسرع لأن المستودع لا يُقرأ. القيمة الافتراضية هي `full`.

  طلب الدمج [#2550](https://github.com/pgbackrest/pgbackrest/pull/2550); الالتزام [`2706168`](https://github.com/pgbackrest/pgbackrest/commit/2706168f609af544b0453d384c7fb620626fc205)

**التحسينات:**

- إعادة محاولة القراءات الفاشلة على مخازن الكائنات. (*راجعه David Christensen.*)

  كان فشل القراءة من تخزين كائنات بعد بدئها خطأً نهائيًا قد يعيد تشغيل مهمة مكلفة، مثلًا أثناء الاستعادة. تُعاد الآن محاولة القراءة من النقطة التي توقفت عندها.

  طلب الدمج [#2642](https://github.com/pgbackrest/pgbackrest/pull/2642); الالتزام [`5e14692`](https://github.com/pgbackrest/pgbackrest/commit/5e14692588b9fd8a566c9a1795c866ba2e83eebd)
- إصلاح القيم الافتراضية في مساعدة سطر الأوامر. (*راجعه David Christensen، Chris Bandy.*)

  عندما يكون للخيار أكثر من قيمة افتراضية، مثل `repo-storage-upload-chunk-size` مع مستودعي S3 وAzure، تعرض قائمة الخيارات `<multi>` وتسرد مساعدة الخيار كل قيمة افتراضية. لا تُعرض القيم الافتراضية للخيارات غير الصالحة في الإعداد الحالي.

  طلب الدمج [#2625](https://github.com/pgbackrest/pgbackrest/pull/2625); الالتزام [`8737cad`](https://github.com/pgbackrest/pgbackrest/commit/8737cad566974c37529595715ecdc06571420752)

**تحسينات التوثيق:**

- وصف القيم المنفصلة للخيارات في قائمة حيثما كان ذلك مناسبًا. (*ساهم به Anton Kurochkin. راجعه David Steele.*)

  تُوصَف الآن قيم خيارات مثل `output` للأمرين `verify` و`version` على شكل قائمة، كما في الخيارات الأخرى.

  طلب الدمج [#2638](https://github.com/pgbackrest/pgbackrest/pull/2638); الالتزام [`2e76e9f`](https://github.com/pgbackrest/pgbackrest/commit/2e76e9fc699d22286f6bf05fddc271d8fa22523e)
- إصلاح "أقل من" في مخرجات المساعدة لخيار `archive-mode`. (*ساهم به Anton Kurochkin. راجعه David Steele.*)

  طلب الدمج [#2633](https://github.com/pgbackrest/pgbackrest/pull/2633); الالتزام [`cb67322`](https://github.com/pgbackrest/pgbackrest/commit/cb673225e90604a8865ce30c188d15661f945e5e)

### ملاحظات إصدار v2.55.1 {#v2551-release-notes}

*إصلاحات أخطاء*

*صدر في 5 مايو 2025*

**إصلاحات الأخطاء:**

- التراجع عن "حساب content-md5 على S3 فقط عند الحاجة". (*راجعه David Christensen. أبلغ عنه Frank Brendel.*)

  يتطلب S3 عند تفعيل قفل الكائنات إما `content-md5` أو مجموعًا اختباريًا من نوع `x-amz-content-*` للتحميل، ولم يكن Scality يقبل المجاميع الاختبارية البديلة، فكانت عمليات التحميل تفشل. يُحسب `content-md5` مجددًا لكل الطلبات ذات المحتوى.

  المشكلة [#2613](https://github.com/pgbackrest/pgbackrest/issues/2613); طلب الدمج [#2615](https://github.com/pgbackrest/pgbackrest/pull/2615); الالتزام [`8bbb982`](https://github.com/pgbackrest/pgbackrest/commit/8bbb98243566bfa052f6aacfd1bd3a6acd770e40)
- إصلاح فحص الحدود الدنيا لمفاتيح الخيارات. (*راجعه David Christensen، Wolfgang Walther. أبلغ عنه Wolfgang Walther.*)

  كان خيار مفهرس بمفتاح 0، مثل `pg0-path`، يسبب خطأ تجزئة. يُصدر الآن خطأً.

  المشكلة [#2610](https://github.com/pgbackrest/pgbackrest/issues/2610); طلب الدمج [#2611](https://github.com/pgbackrest/pgbackrest/pull/2611); الالتزام [`5e01098`](https://github.com/pgbackrest/pgbackrest/commit/5e01098617a3803067b153be2d41e023cd4d95e4)

### ملاحظات إصدار v2.55.0 {#v2550-release-notes}

*تحسينات التحقق ودعم PostgreSQL 18*

*صدر في 21 أبريل 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة استعادة التزايدي بالكتل على مستودع غير افتراضي. (*راجعه David Christensen. اختبره Aleksander Łukasz. أبلغ عنه Aleksander Łukasz.*)

  عندما كانت النسخة الجاري استعادتها تستخدم النسخ التزايدي على مستوى الكتل ولا تقع في المستودع ذي الرقم الأدنى، كانت الاستعادة تقرأ جزءًا من البيانات التزايدية للكتل من المستودع ذي الرقم الأدنى. كان ضبط `repo` حلًا التفافيًا للمشكلة.

  المشكلة [#2577](https://github.com/pgbackrest/pgbackrest/issues/2577); طلب الدمج [#2579](https://github.com/pgbackrest/pgbackrest/pull/2579); الالتزام [`5d2c67c`](https://github.com/pgbackrest/pgbackrest/commit/5d2c67c3c6975ea3ed08c7425f6e410ae378913f)
- عدم تعيين `recovery_target_timeline=current` لـ PostgreSQL < 12. (*راجعه Stefan Fercot.*)

  قبل PostgreSQL 12، يتصرف الضبط الصريح لـ `recovery_target_timeline` على `current` كما لو كان `latest`، رغم أن `current` هي القيمة الافتراضية. يُحذف الإعداد الآن من `recovery.conf` عند ضبطه على `current` لهذه الإصدارات.

  طلب الدمج [#2533](https://github.com/pgbackrest/pgbackrest/pull/2533); الالتزام [`6fbb28f`](https://github.com/pgbackrest/pgbackrest/commit/6fbb28fa2d615576be78376c7f539921f6b8bc6a)
- إصلاح تسجيل نطاق الأرشيف في expire. (*راجعه Stefan Fercot. أبلغ عنه Aleš Zelený.*)

  كان يُسجَّل آخر مسار أرشيف محذوف فقط بوصفه بداية النطاق، ولذلك كان السجل يوحي بأن عدد الملفات المحذوفة أقل بكثير من العدد الفعلي.

  المشكلة [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); طلب الدمج [#2554](https://github.com/pgbackrest/pgbackrest/pull/2554); الالتزام [`47f050f`](https://github.com/pgbackrest/pgbackrest/commit/47f050f8fd816e57326d881f4253d8a13c0f8da6)
- إصلاح الإبلاغ عن الأخطاء للاستعلامات دون نتائج. (*راجعه Stefan Fercot. أبلغ عنه Susantha Bathige.*)

  كان خطأ الاستعلام الذي لا يُتوقع أن يعيد نتائج يُبلَّغ عنه كنتيجة غير متوقعة بدلًا من الخطأ نفسه.

  طلب الدمج [#2539](https://github.com/pgbackrest/pgbackrest/pull/2539); الالتزام [`d5cefb7`](https://github.com/pgbackrest/pgbackrest/commit/d5cefb7290c34c64a2b9aa89ff04a718df4ec18b)

**الميزات:**

- التحقق من الخط الزمني الهدف للاسترداد. (*راجعه Stefan Fercot.*)

  كانت النسخة الاحتياطية التي لا يمكنها اتباع الخط الزمني المستهدف، مثل نسخة أُنشئت بعد ترقية خادم احتياطي وتفرع خط زمني جديد، لا تفشل إلا عند بدء الاسترداد برسالة PostgreSQL يصعب فهمها. يُفحص الخط الزمني الآن مقابل ملفات التاريخ قبل بدء الاستعادة.

  طلب الدمج [#2534](https://github.com/pgbackrest/pgbackrest/pull/2534); الالتزام [`922e9f0`](https://github.com/pgbackrest/pgbackrest/commit/922e9f0775c39b64e009251a6bec8ef9b83c190f)
- السماح بالتحقق من نسخة احتياطية محددة. (*ساهم به Maxim Michkov. راجعه David Steele.*)

  يتحقق خيار `--set` للأمر `verify` من النسخة الاحتياطية المحددة فقط ومن ملفات WAL المطلوبة لجعلها متسقة.

  المشكلة [#2419](https://github.com/pgbackrest/pgbackrest/issues/2419); طلب الدمج [#2544](https://github.com/pgbackrest/pgbackrest/pull/2544); الالتزام [`e4def88`](https://github.com/pgbackrest/pgbackrest/commit/e4def8845eb5c3fe9fb8cc44d9f64766cfb348c2)
- إضافة دعم خاصية الدفع من الطالب (requester pays) في S3/GCS. (*ساهم به Timothée Peignier. راجعه David Steele.*)

  عيّن `repo-s3-requester-pays` أو `repo-gcs-user-project` لتحميل التكلفة على صاحب الطلب بدلًا من مالك الحاوية، مثلًا لتمكين خدمة مستضافة من منح العملاء وصولًا إلى نسخهم الاحتياطية.

  [`4db0263`](https://github.com/pgbackrest/pgbackrest/commit/4db0263fd63274a8168eb4de17b320d2f86251a2) إضافة دعم تحميل تكلفة طلبات S3 على صاحب الطلب.; طلب الدمج [#2560](https://github.com/pgbackrest/pgbackrest/pull/2560)

  [`814bf48`](https://github.com/pgbackrest/pgbackrest/commit/814bf487c3955e877d226faaa22324d3c79863b2) إضافة دعم تحميل تكلفة طلبات GCS على صاحب الطلب.; طلب الدمج [#2557](https://github.com/pgbackrest/pgbackrest/pull/2557)
- دعم PostgreSQL 18. (*راجعه Stefan Fercot.*)

  صدر هذا الإصدار قبل توفر نسخة تجريبية من PostgreSQL 18، ولذلك كان الدعم تجريبيًا في البداية. لم يتغير شيء يؤثر في pgBackRest قبل PostgreSQL 18.0.

  طلب الدمج [#2603](https://github.com/pgbackrest/pgbackrest/pull/2603); الالتزام [`565d2e0`](https://github.com/pgbackrest/pgbackrest/commit/565d2e0c47cd21df890a40b3a94a8c865bed76d9)
- السماح بالاتصالات بـ PostgreSQL عبر مقابس النطاق المجردة. (*اختبره Chris Bandy. اقترحه Chris Bandy.*)

  لم يعد `pg-socket-path` ملزمًا بأن يكون مسارًا مطلقًا، فيمكنه تسمية مقبس نطاق مجرد. يُبلغ libpq عن المسار غير الصالح.

  المشكلة [#2529](https://github.com/pgbackrest/pgbackrest/issues/2529); طلب الدمج [#2535](https://github.com/pgbackrest/pgbackrest/pull/2535); الالتزام [`68f22ae`](https://github.com/pgbackrest/pgbackrest/commit/68f22aea6665b9dcbe76dbfaa731f37187e1ce20)
- إضافة مخرجات رقمية للأمر `version`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  عيّن `--output=num` لإخراج الإصدار كعدد، مثل 2055000، مما يسهل المقارنة.

  المشكلة [#2410](https://github.com/pgbackrest/pgbackrest/issues/2410); طلب الدمج [#2526](https://github.com/pgbackrest/pgbackrest/pull/2526); الالتزام [`750a051`](https://github.com/pgbackrest/pgbackrest/commit/750a051b7aeccc3dd7ae9c07af2c73cb25057de9)

**التحسينات:**

- السماح للأمر `backup` بالعمل على مستودعات بعيدة. (*راجعه Stefan Fercot.*)

  يمكن الآن تشغيل الأمر `backup` على مضيف يكون المستودع بعيدًا عنه، مما يتيح مرونة أكبر في اختيار موضع تشغيل النسخ الاحتياطي.

  [`4a94b6b`](https://github.com/pgbackrest/pgbackrest/commit/4a94b6bef9108ab775c0070571a1fb7dd8883eeb) إعادة تنظيم الوحدة المساعدة للبروتوكول.

  [`931435c`](https://github.com/pgbackrest/pgbackrest/commit/931435c0177ded2189903385d520d5c8819c4f5e) السماح للأمر backup بالعمل على مستودعات بعيدة.; طلب الدمج [#2512](https://github.com/pgbackrest/pgbackrest/pull/2512)
- استخدام lz4 لضغط البروتوكول. (*راجعه Stefan Fercot.*)

  يضغط lz4 أسرع بكثير من gz ويعطي نسبًا مماثلة عند المستويات المنخفضة المستخدمة لضغط البروتوكول. لم يعد ضبط `compress-level-network=0` يعطّل ضغط البروتوكول.

  [`0577b03`](https://github.com/pgbackrest/pgbackrest/commit/0577b0301689bc19d49c4081cc652971de5da8cf) استخدام lz4 لضغط البروتوكول.; طلب الدمج [#2488](https://github.com/pgbackrest/pgbackrest/pull/2488)

  [`5c8296d`](https://github.com/pgbackrest/pgbackrest/commit/5c8296df066564be35d3936610ebff1c332f38da) إزالة الإشارة إلى تعطيل ضغط الشبكة من التوثيق.
- حساب `content-md5` على S3 فقط عند الحاجة. (*راجعه David Christensen.*)

  تُحسب ترويسة `content-md5` فقط لطلبات الحذف الدفعي التي تتطلبها، لتوفير وقت المعالج عند تحميل الملفات. جرى التراجع عن هذا التغيير في v2.55.1.

  طلب الدمج [#2592](https://github.com/pgbackrest/pgbackrest/pull/2592); الالتزام [`20bfd14`](https://github.com/pgbackrest/pgbackrest/commit/20bfd14b73ad6d75b6fb1169565b18dcfa183c9b)
- إصدار تحذير عند استبدال قيمة خيار متعدد المفاتيح. (*راجعه David Christensen، Stefan Fercot.*)

  كانت الخيارات التي تحتوي على أزواج مفتاح/قيمة، مثل `recovery-option`، تستبدل القيمة بصمت عند تحديد مفتاحها مرة أخرى. يُسجَّل الآن تحذير.

  المشكلة [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); طلب الدمج [#2594](https://github.com/pgbackrest/pgbackrest/pull/2594); الالتزام [`cab4d6f`](https://github.com/pgbackrest/pgbackrest/commit/cab4d6fd5c775d6e1a9cd9889d825eee667b5322)
- إضافة تسجيل تفصيلي لمسار الأرشيف المنتهي صلاحيته. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  كان حذف عدد كبير من ملفات الأرشيف قد يبدو كتعليق. تعرض الآن رسالة بمستوى detail التقدم.

  [`4dcfa9e`](https://github.com/pgbackrest/pgbackrest/commit/4dcfa9ef59c5e75c6c0ee83390c64b9a3d4af1fc) إضافة تسجيل بمستوى detail إلى اختبار expire.

  [`2155a12`](https://github.com/pgbackrest/pgbackrest/commit/2155a12a3d861645de5618518350f90962fbc26d) إضافة تسجيل بمستوى detail لمسار الأرشيف المحذوف.; المشكلة [#2543](https://github.com/pgbackrest/pgbackrest/issues/2543); طلب الدمج [#2559](https://github.com/pgbackrest/pgbackrest/pull/2559)
- إزالة دعم PostgreSQL `9.4`. (*راجعه Stefan Fercot.*)

  لم يعد PostgreSQL 9.4 مدعومًا، وفق سياسة دعم خمسة إصدارات من PostgreSQL انتهى عمر دعمها. لا يزال من الممكن حذف النسخ الاحتياطية لعناقيد 9.4 بواسطة التنظيف.

  طلب الدمج [#2472](https://github.com/pgbackrest/pgbackrest/pull/2472); الالتزام [`48f511d`](https://github.com/pgbackrest/pgbackrest/commit/48f511dad339ef9357e00f7bd8e2bf4b7c800dd4)
- إزالة بناء autoconf/make. (*راجعه David Christensen.*)

  كان v2.54.0 آخر إصدار يدعم البناء باستخدام autoconf/make. استخدم meson للبناء.

  طلب الدمج [#2470](https://github.com/pgbackrest/pgbackrest/pull/2470); الالتزام [`89c9bab`](https://github.com/pgbackrest/pgbackrest/commit/89c9baba72fc99616083a7adc4be2c3e2bf9e4dd)

**تحسينات التوثيق:**

- إصلاح توثيق تحديد عدة stanza باستخدام `tls-server-auth`. (*راجعه David Christensen، Stefan Fercot. اقترحه Terry MacAndrew.*)

  تُحدد مقاطع stanza المتعددة لـ `tls-server-auth` بقائمة مفصولة بفواصل. كان التوثيق ينص على تكرار الخيار.

  المشكلة [#2591](https://github.com/pgbackrest/pgbackrest/issues/2591); طلب الدمج [#2595](https://github.com/pgbackrest/pgbackrest/pull/2595); الالتزام [`53a45d2`](https://github.com/pgbackrest/pgbackrest/commit/53a45d25c3e60e5067010b2676f5d6216638fbe3)
- توضيح انتهاء صلاحية النسخ الاحتياطية التزايدية. (*راجعه Stefan Fercot.*)

  كان التوثيق يوحي بأن حذف النسخ التزايدية يعتمد على عددها. يشرح الآن كيفية حذف النسخ التزايدية، وأن النسخ الكاملة تُحتسب كنسخ تفاضلية عند تطبيق سياسة الاحتفاظ بالنسخ التفاضلية.

  طلب الدمج [#2601](https://github.com/pgbackrest/pgbackrest/pull/2601); الالتزام [`8bdba74`](https://github.com/pgbackrest/pgbackrest/commit/8bdba747981e8805a9bf355050f70cdf19e9babc)
- توضيح متطلب تطابق إصدارات pgBackRest المحلية/البعيدة. (*ساهم به Greg Clough. راجعه David Steele.*)

  المشكلة [#2540](https://github.com/pgbackrest/pgbackrest/issues/2540); طلب الدمج [#2541](https://github.com/pgbackrest/pgbackrest/pull/2541); الالتزام [`82299eb`](https://github.com/pgbackrest/pgbackrest/commit/82299eb4cd997524eeddef170ad99669ed6651cf)
- إضافة أسئلة شائعة حول تصدير عنقود مكتفٍ ذاتيًا. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  تشرح الأسئلة الشائعة كيفية إنشاء تصدير مستقل لعنقود باستخدام نسخة احتياطية أُنشئت مع `--archive-copy` واستُعيدت مع `--type=none`.

  طلب الدمج [#2605](https://github.com/pgbackrest/pgbackrest/pull/2605); الالتزام [`9386920`](https://github.com/pgbackrest/pgbackrest/commit/9386920b79971347c6c57589190bf09b591d8b4d)
- إضافة تنبيه حول `--tablespace-map-all` فيما يخص إنشاء مساحات الجداول. (*راجعه Stefan Fercot، Christophe Courtois. اقترحه Christophe Courtois.*)

  مساحة الجدول التي تُنشأ بعد بدء النسخ الاحتياطي لا تكون في ملف manifest، ولذلك لا يستطيع `tablespace-map-all` إعادة تعيينها.

  طلب الدمج [#2538](https://github.com/pgbackrest/pgbackrest/pull/2538); الالتزام [`e625ed8`](https://github.com/pgbackrest/pgbackrest/commit/e625ed8be2228cb99c3801f9d1776909a2201c5a)
- توضيح سلوك `--repo-retention-full-type`. (*راجعه Antoine Beaupré. اقترحه Antoine Beaupré.*)

  المشكلة [#2562](https://github.com/pgbackrest/pgbackrest/issues/2562); طلب الدمج [#2583](https://github.com/pgbackrest/pgbackrest/pull/2583); الالتزام [`84eb9a7`](https://github.com/pgbackrest/pgbackrest/commit/84eb9a742dcf75f071e011946263dedaa985099e)
- تغيير توصية `--process-max` لمخازن الكائنات إلى `--repo-bundle`. (*راجعه Stefan Fercot.*)

  على مخازن الكائنات، يقلل `repo-bundle` الوقت المستغرق في إنشاء الملفات أكثر بكثير من `process-max`، لأن عدد الملفات المنشأة أقل.

  طلب الدمج [#2542](https://github.com/pgbackrest/pgbackrest/pull/2542); الالتزام [`aa7210a`](https://github.com/pgbackrest/pgbackrest/commit/aa7210a1830825e0a3e6b6740937357341127a6f)
- تحديث `unix_socket_directory` إلى `unix_socket_directories`. (*ساهم به hyunkyu han. راجعه David Steele.*)

  لم يعد `unix_socket_directory` صالحًا منذ PostgreSQL 9.2، ولذلك لا يُوثَّق إلا `unix_socket_directories`.

  المشكلة [#2589](https://github.com/pgbackrest/pgbackrest/issues/2589); الالتزام [`b28ae98`](https://github.com/pgbackrest/pgbackrest/commit/b28ae98cec7ae7e881e6476c1cba1ba7e1abc358)
- التوصية بعدم وضع `spool-path` داخل `pg_xlog`/`pg_wal`. (*راجعه Martín Marqués، Don Seiler. اقترحه Martín Marqués.*)

  قد يسبب مسار spool داخل `pg_xlog` أو `pg_wal` مشكلات لأدوات PostgreSQL مثل `pg_rewind`.

  طلب الدمج [#2600](https://github.com/pgbackrest/pgbackrest/pull/2600); الالتزام [`dd3a7d9`](https://github.com/pgbackrest/pgbackrest/commit/dd3a7d99a78d0d604967d90e8a8dbf8915432896)

### ملاحظات إصدار v2.54.2 {#v2542-release-notes}

*إصلاح خطأ*

*صدر في 20 يناير 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة بعد تعطيل التجميع مع تمكين التزايدي بالكتل. (*راجعه David Christensen.*)

  عندما كان التجميع يُعطَّل بعد إنشاء نسخ احتياطية مع تفعيل التجميع والنسخ التزايدي على مستوى الكتل، كان يتعذر قراءة النسخ السابقة. يُحتفَظ الآن بالإعداد اللازم لقراءتها.

  طلب الدمج [#2511](https://github.com/pgbackrest/pgbackrest/pull/2511); الالتزام [`dbc6f28`](https://github.com/pgbackrest/pgbackrest/commit/dbc6f2875356ec16cf4883830a0d7b00204752ee)

**تحسينات التوثيق:**

- توضيح سلوك ملفات الإعداد المتعددة. (*راجعه Paul Bierly. اقترحه Paul Bierly.*)

  يجب أن يكون كل ملف إعداد صالحًا بمفرده، ولذلك يجب تحديد القسم في كل ملف يضبط خيارًا فيه. يوضح التوثيق أيضًا أن الاقتباس غير مدعوم، وأن المسافات الزائدة تُزال من أطراف المفاتيح والقيم، وأن الأقسام المتكررة تُدمج.

  الالتزام [`5da2df4`](https://github.com/pgbackrest/pgbackrest/commit/5da2df4a933f04d5fb9a3b6c7c59529f3afa805b)

### ملاحظات إصدار v2.54.1 {#v2541-release-notes}

*إصلاح خطأ*

*صدر في 16 ديسمبر 2024*

**إصلاحات الأخطاء:**

- إصلاح مشكلة محاولة الأمرين `version`/`help` تحميل `pgbackrest.conf`. (*راجعه Stefan Fercot. أبلغ عنه Bradford Boyle، Julian.*)

  في v2.54.0، كان الأمران `version` و`help` يحمّلان `pgbackrest.conf` ويفشلان عندما يتعذر قراءته أو تحليله.

  المشكلة [#2476](https://github.com/pgbackrest/pgbackrest/issues/2476); طلب الدمج [#2477](https://github.com/pgbackrest/pgbackrest/pull/2477); الالتزام [`8d69118`](https://github.com/pgbackrest/pgbackrest/commit/8d6911898afd75c586ef70c6d8559b1e5959a155)

**تحسينات مجموعة الاختبارات:**

- تثبيت الأرشفة غير المتزامنة في اختبارات التكامل. (*ساهم به Viktor Kurilko. راجعه David Steele.*)

  كان يمكن لعملية `archive-get` غير متزامنة تركها أحد اختبارات التكامل قيد التشغيل أن تكتب خطأ في قائمة انتظار الاختبار التالي وتُفشل استرداده.

  المشكلة [#2463](https://github.com/pgbackrest/pgbackrest/issues/2463); طلب الدمج [#2481](https://github.com/pgbackrest/pgbackrest/pull/2481); الالتزام [`b90ce9e`](https://github.com/pgbackrest/pgbackrest/commit/b90ce9eb8c7cd9e9b131477a377249a3d3fda181)

### ملاحظات إصدار v2.54.0 {#v2540-release-notes}

*الوقت المستهدف للتخزين ذي الإصدارات*

*صدر في 21 أكتوبر 2024*

**ملاحظة لمعدّي الحزم**: هذا آخر إصدار ميزات يدعم بناء autoconf/make. يرجى الانتقال إلى meson إن لم تكن قد فعلت ذلك بالفعل. ستواصل إصدارات الترقيعات 2.54.X (إن وُجدت) دعم autoconf/make.

**إصلاحات الأخطاء:**

- إصلاح أداء استعلامات PostgreSQL لمجموعات البيانات الكبيرة. (*أصلحه Thibault Vincent، David Steele. راجعه David Christensen. اختبره Antoine Millet. أبلغ عنه Antoine Millet.*)

  كان منطق مهلة الاستعلام يؤخر قراءة نتائجه، مما قد يجعل الاستعلام ذي النتيجة الكبيرة يستغرق حتى `db-timeout`. تُقرأ النتائج الآن فور توفرها.

  [`6ac4e8d`](https://github.com/pgbackrest/pgbackrest/commit/6ac4e8dd78f16e93300f7747c4bc8fa8e1a0558b) نقل طبقة المحاكاة للوحدة fd إلى اختبار الوحدة io.

  [`77ae753`](https://github.com/pgbackrest/pgbackrest/commit/77ae753ef59bd40b9867be21e8519093786c3b85) السماح بتشغيل محاكاة fdReady() مرة واحدة فقط بقيمة إرجاع محددة.

  [`33fa396`](https://github.com/pgbackrest/pgbackrest/commit/33fa3965616b1432e5d1d59c489302fa4891a39e) إعادة تنظيم الكائن Wait لإتاحة زمن الانتظار المتبقي عبر waitRemains().

  [`c8ccaaa`](https://github.com/pgbackrest/pgbackrest/commit/c8ccaaa755993e3fd5e87148bd0a991acb3050c3) تحسين أداء استعلامات PostgreSQL لمجموعات البيانات الكبيرة.; المشكلة [#2458](https://github.com/pgbackrest/pgbackrest/issues/2458); طلب الدمج [#2459](https://github.com/pgbackrest/pgbackrest/pull/2459)

**الميزات:**

- السماح بقراءة المستودعات على التخزين ذي الإصدارات عند وقت مستهدف. (*راجعه Stefan Fercot، David Christensen.*)

  يمكن للأوامر `archive-get` و`info` و`repo-get` و`repo-ls` و`restore` و`verify` قراءة مستودع على تخزين Azure أو GCS أو S3 ذي إصدارات كما كان في `repo-target-time`. يتيح ذلك الاسترداد حتى لو حُذف المستودع أو أُتلف، سواءً عرضًا أو عمدًا.

  طلب الدمج [#2404](https://github.com/pgbackrest/pgbackrest/pull/2404); الالتزام [`b19134d`](https://github.com/pgbackrest/pgbackrest/commit/b19134dccd5d0dab87b5d45b443f481df00370b1)
- السماح للنسخة الاحتياطية المطلوبة من خادم الاستعداد بالمتابعة دون وجود خادم استعداد. (*راجعه Stefan Fercot.*)

  عيّن `backup-standby=prefer` للنسخ الاحتياطي من خادم احتياطي إن توفر، ومن الأساسي خلاف ذلك. لا يفيد هذا عندما يستجيب الخادم الاحتياطي لكنه يفشل في المزامنة مع الأساسي بعد بدء النسخ الاحتياطي.

  طلب الدمج [#2378](https://github.com/pgbackrest/pgbackrest/pull/2378); الالتزام [`a42629f`](https://github.com/pgbackrest/pgbackrest/commit/a42629f87ab70ffaee8d1241eb50c5ea7154a87d)

**التحسينات:**

- تلخيص قائمة مراجع النسخ الاحتياطية في المخرجات النصية للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  قد تكون قائمة مراجع النسخ الاحتياطية طويلة جدًا، ولذلك تلخّصها الآن المخرجات النصية للأمر `info`. تُعرض القائمة الكاملة عند تحديد `--set`.

  طلب الدمج [#2399](https://github.com/pgbackrest/pgbackrest/pull/2399); الالتزام [`b306f83`](https://github.com/pgbackrest/pgbackrest/commit/b306f83493cc859ad15c8f175fc6db2321b79340)
- تحديث رمز web-id عند كل مصادقة S3. (*ساهم به Brent Graveland. راجعه David Steele.*)

  كان ملف الرمز المحدد بواسطة `AWS_WEB_IDENTITY_TOKEN_FILE` يُقرأ مرة واحدة عند بدء التشغيل، ولذلك كان يمكن أن تنتهي صلاحية الرمز أثناء عملية طويلة. يُقرأ الرمز الآن عند كل مصادقة.

  المشكلة [#2428](https://github.com/pgbackrest/pgbackrest/issues/2428); طلب الدمج [#2429](https://github.com/pgbackrest/pgbackrest/pull/2429); الالتزام [`95a4b9e`](https://github.com/pgbackrest/pgbackrest/commit/95a4b9e10a3f7a26ebaae22fc6abd79cee14189a)
- عرض القيم الحالية للخيارات المفهرسة بشكل صحيح في المساعدة. (*راجعه David Christensen.*)

  كانت القيمة الحالية المعروضة لخيار مفهرس دائمًا قيمة الفهرس الأول، مثل `pg1-path`. تسرد مساعدة الخيار الآن قيمة كل فهرس، وتعرض قائمة الخيارات `<multi>` عندما توجد أكثر من قيمة واحدة.

  طلب الدمج [#2453](https://github.com/pgbackrest/pgbackrest/pull/2453); الالتزام [`b3ca2e3`](https://github.com/pgbackrest/pgbackrest/commit/b3ca2e34823b28862d999f87c4d7346707952a5b)
- حفظ `backup.info` فقط عند تغيّر محتواه. (*راجعه Stefan Fercot.*)

  كان `expire` يحفظ `backup.info` حتى عندما لا يتغير. كما أن تقليل مرات الحفظ يسهل اختيار وقت مستهدف على تخزين ذي إصدارات.

  طلب الدمج [#2403](https://github.com/pgbackrest/pgbackrest/pull/2403); الالتزام [`b454b9e`](https://github.com/pgbackrest/pgbackrest/commit/b454b9e403526b1f352df964d9206c27d2397df3)
- إزالة قيد القراءة المتوازية للملفات أثناء الاستعادة. (*راجعه David Christensen.*)

  كان البروتوكول يسمح بقراءة ملف واحد أو كتابته في المرة الواحدة على مضيف بعيد، ولذلك كانت الاستعادة تقرأ ملفًا واحدًا في كل مرة من المستودع. يمكن الآن تعدد إرسال أوامر البروتوكول، فتستطيع الاستعادة قراءة أكثر من ملف في الوقت نفسه، مثل حزمة والبيانات التزايدية للكتل لملف فيها.

  [`df8cbc9`](https://github.com/pgbackrest/pgbackrest/commit/df8cbc91c348bc2f746767c87ac5626460fb6f39) إضافة تعدد إرسال أوامر البروتوكول.; طلب الدمج [#2108](https://github.com/pgbackrest/pgbackrest/pull/2108)

  [`46c1297`](https://github.com/pgbackrest/pgbackrest/commit/46c1297be344909e900be596a865064233da9f87) إزالة قيد قراءة الملفات بالتوازي أثناء الاستعادة.; طلب الدمج [#2436](https://github.com/pgbackrest/pgbackrest/pull/2436)
- تحسين رسائل أخطاء SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)

  كانت أخطاء SFTP تُعرض كأرقام فقط. تتضمن الآن وصفًا للخطأ.

  طلب الدمج [#2439](https://github.com/pgbackrest/pgbackrest/pull/2439); الالتزام [`70bda2c`](https://github.com/pgbackrest/pgbackrest/commit/70bda2cfb21130eb589a87cb419fb5f22a71c78a)

**ميزات التوثيق:**

- إضافة قسم ضبط الأداء إلى دليل المستخدم. (*راجعه Stefan Fercot.*)

  كانت الخيارات التي تحسن الأداء عادةً موزعة في أنحاء التوثيق. يتضمن دليل البدء السريع الآن قسمًا يسردها.

  طلب الدمج [#2446](https://github.com/pgbackrest/pgbackrest/pull/2446); الالتزام [`278319e`](https://github.com/pgbackrest/pgbackrest/commit/278319eba3444070123d3f0f277be9234604d937)

**تحسينات التوثيق:**

- توضيح مصدر `data_directory`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Matthias.*)

  يجب أن يطابق `pg-path` قيمة `data_directory` التي يُبلغ عنها PostgreSQL، والتي قد تختلف عن القيمة في `postgresql.conf`.

  المشكلة [#2464](https://github.com/pgbackrest/pgbackrest/issues/2464); طلب الدمج [#2467](https://github.com/pgbackrest/pgbackrest/pull/2467); الالتزام [`9ba2db0`](https://github.com/pgbackrest/pgbackrest/commit/9ba2db017348d304f96ce89592fc01f29197e136)
- منطق أفضل لتحديد متى يجب أن يكون الملخص بأحرف صغيرة. (*اقترحه Daniel Westermann.*)

  لم تعد الملخصات التي تبدأ باسم علم أو اختصار، مثل PostgreSQL، تُحوَّل إلى أحرف صغيرة في التوثيق.

  المشكلة [#2462](https://github.com/pgbackrest/pgbackrest/issues/2462); الالتزام [`eb2f279`](https://github.com/pgbackrest/pgbackrest/commit/eb2f279a2998d1ed893c5d8984590ab4997a5f32)

### ملاحظات إصدار v2.53.1 {#v2531-release-notes}

*دعم PostgreSQL 17*

*صدر في 19 أغسطس 2024*

**إصلاحات الأخطاء:**

- إصلاح الأذونات عند تشغيل `restore` بصلاحيات المستخدم root. (*راجعه Stefan Fercot. أبلغ عنه Will M.*)

  عند تشغيل `restore` بصلاحيات root، كانت ملكية `pg_control` تعود إلى root. وكانت الاستعادة بصلاحيات root تفشل أيضًا عندما لا يكون المسار الأساسي موجودًا.

  المشكلة [#2407](https://github.com/pgbackrest/pgbackrest/issues/2407); طلب الدمج [#2416](https://github.com/pgbackrest/pgbackrest/pull/2416); الالتزام [`7bd8da4`](https://github.com/pgbackrest/pgbackrest/commit/7bd8da4eecb0ce1461854414b727606a5e884edf)
- إصلاح خطأ تقسيم عند تأخر أخطاء الاتصال. (*راجعه David Christensen. أبلغ عنه Anton Glushakov.*)

  كان يمكن لخطأ اتصال تأخر الإبلاغ عنه إلى انتظار لاحق أن يتسبب في خطأ تجزئة.

  المشكلة [#2420](https://github.com/pgbackrest/pgbackrest/issues/2420); طلب الدمج [#2422](https://github.com/pgbackrest/pgbackrest/pull/2422); الالتزام [`377ba06`](https://github.com/pgbackrest/pgbackrest/commit/377ba062ac81867dca6197265688deb0111ae81a)
- تخطي فحص التكرار للمستودع المحلي في SFTP. (*أصلحه Reid Thompson. راجعه David Steele. أبلغ عنه Anton Kurochkin.*)

  كان فحص المستودعات المحلية المضبوطة أكثر من مرة يُطبَّق أيضًا على مستودعات SFTP التي لا تكون محلية أبدًا.

  المشكلة [#2418](https://github.com/pgbackrest/pgbackrest/issues/2418); طلب الدمج [#2421](https://github.com/pgbackrest/pgbackrest/pull/2421); الالتزام [`9840304`](https://github.com/pgbackrest/pgbackrest/commit/98403046ed6af4c54fa2f572ecf9c211f94b67db)

**التحسينات:**

- دعم PostgreSQL 17.

  غيّر PostgreSQL 17beta3 تنسيقي ملف التحكم وWAL، وهو أمر غير معتاد لإصدار تجريبي.

  الالتزام [`189d15d`](https://github.com/pgbackrest/pgbackrest/commit/189d15d1a640e31aac5ffbbd0fb06eb9eed8b576)

### ملاحظات إصدار v2.53 {#v253-release-notes}

*النسخ الاحتياطي المتزامن*

*صدر في 22 يوليو 2024*

**ملاحظة هامة**: تغيّرت القيمة الافتراضية للخيار `log-level-stderr` من `warn` إلى `off`. يسهّل ذلك التقاط الأخطاء عند إعادة توجيه `stdout` فقط. للحفاظ على السلوك السابق عيّن `log-level-stderr=warn`.<br/> <br/> **ملاحظة لمعدّي الحزم**: أصبحت مكتبة lz4 مطلوبة للبناء باستخدام meson.<br/> <br/> **ملاحظة لمعدّي الحزم**: أصبح دعم المُجمِّع لـ `__builtin_clzl()` و`__builtin_bswap64()` مطلوبًا للبناء باستخدام meson.

**إصلاحات الأخطاء:**

- إصلاح فشل إعادة التسمية في SFTP عندما يكون الملف موجودًا بالفعل. (*أصلحه Reid Thompson. راجعه David Steele. أبلغ عنه ahmed112212.*)

  تُبلغ بعض خوادم SFTP عن وجود الملف مسبقًا بخطأ لم يكن يُعالَج، ولذلك كانت إعادة تسمية ملف فوق ملف موجود تفشل.

  المشكلة [#2376](https://github.com/pgbackrest/pgbackrest/issues/2376); طلب الدمج [#2377](https://github.com/pgbackrest/pgbackrest/pull/2377); الالتزام [`d6f0bf8`](https://github.com/pgbackrest/pgbackrest/commit/d6f0bf88af8b39492aa8e20c09bdf30260e2eb2f)

**الميزات:**

- السماح بتشغيل النسخ الاحتياطي بشكل متزامن على مستودعات مختلفة. (*راجعه Reid Thompson، Stefan Fercot.*)

  يمكن الآن تشغيل نسخ احتياطية لمقطع stanza نفسه في الوقت ذاته على مستودعات مختلفة، لأن الأقفال أصبحت لكل زوج من stanza ومستودع بدلًا من stanza وحده. لا يمكن ذلك مع PostgreSQL <= 9.5.

  [`270dce4`](https://github.com/pgbackrest/pgbackrest/commit/270dce41b6fff0d0ad0769b0ea5df0011140f0b9) إعادة تنظيم وحدة الأقفال.; طلب الدمج [#2371](https://github.com/pgbackrest/pgbackrest/pull/2371)

  [`cfb8aa2`](https://github.com/pgbackrest/pgbackrest/commit/cfb8aa202ee972579697db2cc8d5d8ef111f0022) إضافة أقفال بعيدة لأوامر stanza التي أُغفلت في 31c7824a.

  [`edd6163`](https://github.com/pgbackrest/pgbackrest/commit/edd61636a98d193b7c0634b5a4444527132959e0) السماح بتشغيل النسخ الاحتياطي بالتزامن على مستودعات مختلفة.; طلب الدمج [#2389](https://github.com/pgbackrest/pgbackrest/pull/2389)
- دعم SANs القائمة على IP للتحقق من شهادات TLS. (*ساهم به David Christensen. راجعه David Steele.*)

  يُتحقَّق الآن من الشهادات التي تحتوي على عنوان IP في الاسم البديل للموضوع، مثل `IP:1.2.3.4`. يجب أن تتطابق عناوين IPv4 وIPv6 تطابقًا تامًا.

  المشكلة [#1977](https://github.com/pgbackrest/pgbackrest/issues/1977); طلب الدمج [#2047](https://github.com/pgbackrest/pgbackrest/pull/2047); الالتزام [`dfb620b`](https://github.com/pgbackrest/pgbackrest/commit/dfb620b0b8cf884ca486b413f4cd162e258b2fc5)

**التحسينات:**

- جعل القيمة الافتراضية لخيار `log-level-stderr` هي `off`. (*راجعه Greg Sabino Mullane، Stefan Fercot.*)

  كانت التحذيرات والأخطاء المكتوبة إلى stderr تضيع غالبًا عند إعادة توجيه stdout وحده أثناء جمع السجلات. لا يتأثر `log-level-stderr` المضبوط صراحةً.

  طلب الدمج [#2379](https://github.com/pgbackrest/pgbackrest/pull/2379); الالتزام [`7d54073`](https://github.com/pgbackrest/pgbackrest/commit/7d540730941994d3cb630c695e9f672e047d8e7f)
- السماح بأحجام بديلة لمقاطع WAL لـ PostgreSQL ≤ 10. (*ساهم به Viktor Kurilko. راجعه David Steele.*)

  يمكن بناء PostgreSQL <= 10 بحجم مختلف لمقطع WAL، وتضبطه مشتقات مثل Greenplum بواسطة `initdb`.

  طلب الدمج [#2303](https://github.com/pgbackrest/pgbackrest/pull/2303); الالتزام [`4ac3b82`](https://github.com/pgbackrest/pgbackrest/commit/4ac3b82c99ff3bd48d2cc74651a47ce072ac0022)
- إضافة تلميح لفحص سجل التفويض في SFTP. (*ساهم به Vitalii Zurian. راجعه Reid Thompson، David Steele.*)

  عند فشل مصادقة SFTP، يلمّح الخطأ الآن إلى أن سجل التفويض على الخادم قد يحتوي على مزيد من التفاصيل.

  المشكلة [#2381](https://github.com/pgbackrest/pgbackrest/issues/2381); طلب الدمج [#2385](https://github.com/pgbackrest/pgbackrest/pull/2385); الالتزام [`ccae609`](https://github.com/pgbackrest/pgbackrest/commit/ccae60940241b30e8bc3e405936b6ba68857930c)
- عرض القيم الافتراضية والمسموح بها لخيارات الزمن بوحدات مناسبة.

  كانت القيم الافتراضية والمسموح بها لخيارات الزمن تُعرض بالثواني، مما يصعّب قراءة القيم الكبيرة. لم تعد أجزاء الثانية مسموحة، ولذلك يجب كتابة قيمة مثل `archive-timeout=0.5` بصيغة `archive-timeout=500ms`.

  الالتزام [`3a2266f`](https://github.com/pgbackrest/pgbackrest/commit/3a2266f327c340ff1133a6a2398429c844b5755d)
- اشتراط OpenSSL >= 1.1.1.

  الالتزام [`cf8625d`](https://github.com/pgbackrest/pgbackrest/commit/cf8625d24bd953ad1ed448c32b937584009e5b6b)

**تحسينات التوثيق:**

- توضيح سلوك `archive-push` مع المستودعات المتعددة. (*راجعه Stefan Fercot.*)

  عندما يفشل أحد المستودعات، لا يستطيع `archive-push` مواصلة الإرسال إلى المستودعات الأخرى ما لم يُفعَّل `archive-async`.

  طلب الدمج [#2398](https://github.com/pgbackrest/pgbackrest/pull/2398); الالتزام [`ec3e387`](https://github.com/pgbackrest/pgbackrest/commit/ec3e387bb73826c30b32bf0221acb2d56f23f1c5)

### ملاحظات إصدار v2.52.1 {#v2521-release-notes}

*إصلاح خطأ*

*صدر في 25 يونيو 2024*

**إصلاحات الأخطاء:**

- إصلاح مشكلة الملفات الأكبر على النسخة المتماثلة مقارنة بالأساسي. (*راجعه Stefan Fercot. أبلغ عنه Nicolas Lassimonne.*)

  مع النسخ التزايدي على مستوى الكتل، عندما كان حجم ملف على الأساسي مختلفًا عنه على الاحتياطي أثناء النسخ من الاحتياطي، كانت النسخة التفاضلية أو التزايدية التالية تخزن الحجم من الأساسي. وكانت النسخة التي تليها تفشل بالرسالة "repo size must be > 0".

  [`83aaa86`](https://github.com/pgbackrest/pgbackrest/commit/83aaa868ef396348bf96589457f13c1805b25cb6) إضافة اختبارات وحدات للنسخ من الخادم الاحتياطي مع النسخ التزايدي على مستوى الكتل.

  [`aabc122`](https://github.com/pgbackrest/pgbackrest/commit/aabc122021a582e9d0193f978cf710cff95c2bee) إصلاح مشكلة الملفات الأكبر على النسخة المتماثلة منها على الخادم الأساسي.; المشكلة [#2358](https://github.com/pgbackrest/pgbackrest/issues/2358); طلب الدمج [#2367](https://github.com/pgbackrest/pgbackrest/pull/2367)

### ملاحظات إصدار v2.52 {#v252-release-notes}

*دعم PostgreSQL 17beta1*

*صدر في 27 مايو 2024*

**ملاحظة لمعدّي الحزم**: أصبح نظام بناء pgBackRest الآن meson. لن يحصل بناء autoconf/make على أي ميزات جديدة وسيُزال بعد بضعة إصدارات.

**الميزات:**

- إضافة دعم الحذف الدفعي في GCS. (*راجعه Reid Thompson.*)

  تُحذف الملفات بطلبات دفعية بدلًا من طلب لكل ملف، مما يسرّع `expire` والأوامر الأخرى التي تحذف ملفات من المستودع.

  طلب الدمج [#2326](https://github.com/pgbackrest/pgbackrest/pull/2326); الالتزام [`76bcb74`](https://github.com/pgbackrest/pgbackrest/commit/76bcb740b66f64804dbbf5a2a6be6407f9cec376)
- دعم التشفير `SSE-C` في S3. (*راجعه Tim Jones. اقترحه Tim Jones.*)

  عيّن `repo-s3-sse-customer-key` لجعل S3 يشفّر البيانات بالمفتاح المقدم بعد نقلها. هذا أقل أمانًا من تشفير البيانات قبل نقلها باستخدام `repo-cipher-type`.

  المشكلة [#2279](https://github.com/pgbackrest/pgbackrest/issues/2279); طلب الدمج [#2282](https://github.com/pgbackrest/pgbackrest/pull/2282); الالتزام [`57731b6`](https://github.com/pgbackrest/pgbackrest/commit/57731b6cd261c732041aacc094429ab02ca13418)
- دعم PostgreSQL 17beta1. (*راجعه Stefan Fercot.*)

  إضافة إصدار الكتالوج والرقم السحري لـ WAL في PostgreSQL 17.

  طلب الدمج [#2328](https://github.com/pgbackrest/pgbackrest/pull/2328); الالتزام [`fb22f04`](https://github.com/pgbackrest/pgbackrest/commit/fb22f04555fecfa143354372ec3543ab186c131d)

**التحسينات:**

- السماح بتعطيل التبعيات الاختيارية بشكل صريح في بناء meson. (*ساهم به Michael Schout. راجعه David Steele.*)

  يمكن تعطيل ميزة اختيارية في بناء meson حتى عندما تكون مكتبتها مثبتة، كما تتطلب بعض المنصات مثل FreeBSD. تُفعَّل الميزة افتراضيًا عند العثور على مكتبتها.

  طلب الدمج [#2321](https://github.com/pgbackrest/pgbackrest/pull/2321); الالتزام [`7b95fd3`](https://github.com/pgbackrest/pgbackrest/commit/7b95fd3bd29346e7325aa161bfee45efd71e22eb)
- إيجاد python ديناميكيًا في بناء meson. (*ساهم به Michael Schout. راجعه David Steele.*)

  يعثر بناء meson الآن على تثبيت python بدلًا من اشتراط ملف تنفيذي باسم `python3` في مسار البحث، مثلًا عندما لا يكون مثبتًا إلا `python3.9`. أصبح الحد الأدنى لإصدار meson هو 0.47.

  [`55e9969`](https://github.com/pgbackrest/pgbackrest/commit/55e996912aa57d39ea21f5dc905b7acabe93b0f8) رفع الحد الأدنى لإصدار meson إلى 0.47.

  [`e00e33b`](https://github.com/pgbackrest/pgbackrest/commit/e00e33b52856a63e82552ccc12df235d1a7f6f17) العثور على python ديناميكيًا في بناء meson.; طلب الدمج [#2338](https://github.com/pgbackrest/pgbackrest/pull/2338)
- وسم هدف بناء `pgbackrest` في meson بأنه قابل للتثبيت. (*ساهم به Bradford Boyle. راجعه David Steele.*)

  طلب الدمج [#2312](https://github.com/pgbackrest/pgbackrest/pull/2312); الالتزام [`7877983`](https://github.com/pgbackrest/pgbackrest/commit/7877983acb3b1a27e900f7e7aea89cb7b29a817d)

**تحسينات التوثيق:**

- تحديث توثيق `start`/`stop` ليعكس الوظائف الفعلية. (*راجعه Stefan Fercot.*)

  المشكلة [#2325](https://github.com/pgbackrest/pgbackrest/issues/2325); المشكلة [#2334](https://github.com/pgbackrest/pgbackrest/issues/2334); طلب الدمج [#2352](https://github.com/pgbackrest/pgbackrest/pull/2352); الالتزام [`b6ac11b`](https://github.com/pgbackrest/pgbackrest/commit/b6ac11beec920fe978994c0d018c380477199ca8)

### ملاحظات إصدار v2.51 {#v251-release-notes}

*نظام البناء meson*

*صدر في 25 مارس 2024*

**إصلاحات الأخطاء:**

- تخطي الملفات ذات الطول الصفري لاستعادة دلتا التزايدي بالكتل. (*راجعه Sebastian Krause، René Højbjerg Larsen. أبلغ عنه Sebastian Krause.*)

  كان وجود ملف بطول صفري يتسبب في فشل استعادة دلتا للنسخ التزايدي على مستوى الكتل داخل مرشح المجموع الاختباري للكتل. تُتجاوز هذه الملفات الآن إذ لا تحتوي على شيء يمكن إعادة استخدامه.

  المشكلة [#2271](https://github.com/pgbackrest/pgbackrest/issues/2271); طلب الدمج [#2272](https://github.com/pgbackrest/pgbackrest/pull/2272); الالتزام [`f7a7ab1`](https://github.com/pgbackrest/pgbackrest/commit/f7a7ab16c9652179945717ebf9b68af3aa8a0b0e)
- إصلاح تراجع الأداء في قائمة التخزين. (*راجعه Stephen Frost. أبلغ عنه Maksym Boguk.*)

  كان إدراج مسار يطلب معلومات تفصيلية عن كل ملف، مما قد يكون بطيئًا، مثلًا على مخازن الكائنات. لا تُطلب الآن إلا المعلومات التي تحتاج إليها القائمة.

  المشكلة [#2275](https://github.com/pgbackrest/pgbackrest/issues/2275); طلب الدمج [#2276](https://github.com/pgbackrest/pgbackrest/pull/2276); الالتزام [`e00bfe2`](https://github.com/pgbackrest/pgbackrest/commit/e00bfe2d2c3f124b2883e3c2d169a2ce506a1e98)
- إصلاح تسجيل التقدم عندما يتغير حجم الملف أثناء النسخ الاحتياطي. (*راجعه Stephen Frost. أبلغ عنه samkingno.*)

  المشكلة [#2298](https://github.com/pgbackrest/pgbackrest/issues/2298); طلب الدمج [#2304](https://github.com/pgbackrest/pgbackrest/pull/2304); الالتزام [`76956e7`](https://github.com/pgbackrest/pgbackrest/commit/76956e71cfa3044867213bd65a6f22e96120c108)

**التحسينات:**

- تحسين الدعم للاتصالات ثنائية المكدس. (*راجعه Stephen Frost. اقترحه Timothée Peignier.*)

  عندما يُحل اسم مضيف إلى أكثر من عنوان، مثل IPv4 وIPv6، تُجرَّب العناوين التالية بعد منح العنوان السابق وقتًا معقولًا للاتصال، وفق نهج «happy eyeballs» في RFC 8305. لم تعد محاولة اتصال لا تفشل ولا تتصل تستهلك كل الوقت المتاح.

  المشكلة [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); طلب الدمج [#2235](https://github.com/pgbackrest/pgbackrest/pull/2235); الالتزام [`7448fde`](https://github.com/pgbackrest/pgbackrest/commit/7448fde157c6d22f57b90c0cef11957b0aadf4b3)
- جعل meson نظام البناء الأساسي. (*راجعه Stephen Frost.*)

  أصبح meson نظام البناء المستخدم للاختبار وبناء التوثيق. وتُخفى الآن الدوال غير المستخدمة خارج وحدتها، مما يقلل حجم الملف التنفيذي.

  [`e3d9df3`](https://github.com/pgbackrest/pgbackrest/commit/e3d9df3ae9669ee5749b970d59f8afeb20fd3d9d) جعل meson نظام البناء الأساسي.; طلب الدمج [#2264](https://github.com/pgbackrest/pgbackrest/pull/2264)

  [`f287178`](https://github.com/pgbackrest/pgbackrest/commit/f287178b705cc90aa887d66c932e2a223029649b) ضبط مستوى ظهور الدوال والمتغيرات على hidden.; طلب الدمج [#2265](https://github.com/pgbackrest/pgbackrest/pull/2265)
- اكتشاف الملفات التي لم تتغير أثناء النسخ الاحتياطي التزايدي غير القائم على الدلتا. (*راجعه Stephen Frost.*)

  أثناء النسخ التفاضلي أو التزايدي دون delta، يُقارَن الملف الذي يتسع في مخزن مؤقت واحد، أو أي ملف نسخ تزايدي على مستوى الكتل، بالملف في النسخة السابقة، ويُشار إليه بدلًا من تخزينه عندما لا يتغير.

  طلب الدمج [#2257](https://github.com/pgbackrest/pgbackrest/pull/2257); الالتزام [`9d91d1b`](https://github.com/pgbackrest/pgbackrest/commit/9d91d1b2f817b543fc8d970af56d1442c325ed7c)
- منع استرداد غير صالح عند إزالة `backup_label`. (*راجعه Stephen Frost.*)

  عند إزالة `backup_label` من عنقود مستعاد، يستخدم PostgreSQL نقطة التحقق في `pg_control` للاسترداد بعد التعطل، مما يؤدي إلى تلف العنقود دائمًا تقريبًا. تُبطل الاستعادة الآن نقطة التحقق في `pg_control` فيفشل الاسترداد بدلًا من ذلك. يعرض `pg_controldata` نقطة التحقق بصيغة `0/DEAD`.

  طلب الدمج [#2232](https://github.com/pgbackrest/pgbackrest/pull/2232); الالتزام [`e634fd8`](https://github.com/pgbackrest/pgbackrest/commit/e634fd85cedc1ae3aef7c4fa2556d7d73d05cb8a)
- تحسين التعامل مع قائمة انتظار مقاطع WAL في `archive-push`. (*راجعه Stephen Frost.*)

  كان حجم كل مقطع WAL في قائمة الانتظار يُقرأ لقياسها. يُستخدم الآن حجم المقطع الأول لجميع المقاطع.

  طلب الدمج [#2277](https://github.com/pgbackrest/pgbackrest/pull/2277); الالتزام [`cf17515`](https://github.com/pgbackrest/pgbackrest/commit/cf17515e409440eecfb04bf7186790d8baa8ab12)
- قصر وظيفة الاستئناف على النسخ الاحتياطية الكاملة. (*راجعه Stephen Frost، Stefan Fercot.*)

  لم يكن الاستئناف يعمل بشكل صحيح للنسخ التفاضلية والتزايدية مع delta، كما أن الملف الذي تغير منذ النسخة السابقة يُرجَّح أن يتغير مجددًا قبل الاستئناف. لا تُستأنف الآن إلا النسخ الاحتياطية الكاملة.

  طلب الدمج [#2268](https://github.com/pgbackrest/pgbackrest/pull/2268); الالتزام [`dddcbcd`](https://github.com/pgbackrest/pgbackrest/commit/dddcbcd8e9a1cae578b0cc5bb2d1aa768330f3c5)
- تحديث وظيفة الاستئناف للتزايدي بالكتل. (*راجعه Stephen Frost.*)

  كان الاستئناف يحذف ملفات النسخ التزايدي على مستوى الكتل، ولذلك كان يعمل لكنه يعيد نسخها جميعًا. يُحتفَظ بهذه الملفات الآن عند الاستئناف.

  طلب الدمج [#2296](https://github.com/pgbackrest/pgbackrest/pull/2296); الالتزام [`ff47450`](https://github.com/pgbackrest/pgbackrest/commit/ff47450402fde5ebc64a08d31791551bee52200e)
- السماح باستخدام `--version` و`--help` لعرض الإصدار والمساعدة. (*راجعه Greg Sabino Mullane. اقترحه Greg Sabino Mullane.*)

  يعمل `--version` و`--help` الآن كما في معظم البرامج. استخدم `help` للمساعدة بشأن أمر أو خيار محدد.

  طلب الدمج [#2263](https://github.com/pgbackrest/pgbackrest/pull/2263); الالتزام [`68db307`](https://github.com/pgbackrest/pgbackrest/commit/68db3075d7ac4a48377967ad54e45b95b9ee6c61)
- إضافة تتبع خلفي مفصّل إلى بناء autoconf/make. (*راجعه Stephen Frost.*)

  تتضمن تتبعات مكدس الأخطاء في بناء autoconf/make الآن تفاصيل من libbacktrace، وقد أظهرت اختبارات الأداء أن ذلك لا يضيف كلفة ملحوظة.

  طلب الدمج [#1970](https://github.com/pgbackrest/pgbackrest/pull/1970); الالتزام [`676700d`](https://github.com/pgbackrest/pgbackrest/commit/676700d8ca6f2e0e0ab8123aa9606c8ec7aa81ae)

**تحسينات التوثيق:**

- تحديث الإشارات إلى `recovery.conf`. (*راجعه Stefan Fercot. اقترحه Stephen Frost.*)

  تتضمن الإشارات إلى `recovery.conf` الآن أيضًا `postgresql.auto.conf` الذي تستخدمه إصدارات PostgreSQL الأحدث.

  طلب الدمج [#2281](https://github.com/pgbackrest/pgbackrest/pull/2281); الالتزام [`6835178`](https://github.com/pgbackrest/pgbackrest/commit/68351785f6816a23526900db595557cf6e3a0056)

### ملاحظات إصدار v2.50 {#v250-release-notes}

*تحسينات الأداء وإصلاحات أخطاء*

*صدر في 22 يناير 2024*

**إصلاحات الأخطاء:**

- إصلاح القراءة الناقصة في استعادة التزايدي بالكتل. (*راجعه Stephen Frost. اختبره Brent Graveland. أبلغ عنه Adol Rodriguez، Brent Graveland.*)

  قد تنتهي كتلة فائقة مضغوطة ببايتات غير لازمة لفك ضغطها لكنها تشير إلى نهاية البيانات. بحسب موضع المخزن المؤقت بالنسبة للبيانات، لم تكن هذه البايتات تُقرأ، وكانت الاستعادة تفشل.

  المشكلة [#2215](https://github.com/pgbackrest/pgbackrest/issues/2215); المشكلة [#2238](https://github.com/pgbackrest/pgbackrest/issues/2238); طلب الدمج [#2256](https://github.com/pgbackrest/pgbackrest/pull/2256); الالتزام [`f4a4af2`](https://github.com/pgbackrest/pgbackrest/commit/f4a4af299bee93ab7dde599ccdb35becc1c2afad)
- إصلاح فيض يخفي تقدم النسخ الاحتياطي في مخرجات `info`. (*أصلحه Robert Donovan. راجعه Joe Wildish.*)

  كانت الأحجام في ملف القفل تُقرأ كقيم ذات 32 بت، ولذلك لم يكن الأمر `info` يُبلغ عن تقدم نسخة احتياطية أكبر من 4GiB.

  المشكلة [#2251](https://github.com/pgbackrest/pgbackrest/issues/2251); طلب الدمج [#2252](https://github.com/pgbackrest/pgbackrest/pull/2252); الالتزام [`25f1489`](https://github.com/pgbackrest/pgbackrest/commit/25f14898babf4ad78baef3e8343933a863633975)

**التحسينات:**

- الحفاظ على الملفات الجزئية أثناء استعادة دلتا التزايدي بالكتل. (*راجعه Stephen Frost.*)

  لم يكن الملف الأصغر من المتوقع يُحتفَظ به لاستعادة دلتا للنسخ التزايدي على مستوى الكتل، رغم إمكانية إعادة استخدام كتله، مثلًا عند إعادة محاولة استعادة فاشلة أو الاستعادة فوق ملف أصغر.

  طلب الدمج [#2254](https://github.com/pgbackrest/pgbackrest/pull/2254); الالتزام [`a42614e`](https://github.com/pgbackrest/pgbackrest/commit/a42614e8f3a9e6871c16331f01c2cd765ab181aa)
- إضافة دعم أحجام صفحات بديلة وقت التجميع. (*ساهم به Viktor Kurilko. راجعه David Steele.*)

  يمكن بناء PostgreSQL بحجم صفحة مختلف، مثل 4096، وتفعل ذلك مشتقات مثل Greenplum.

  طلب الدمج [#2197](https://github.com/pgbackrest/pgbackrest/pull/2197); الالتزام [`89d5278`](https://github.com/pgbackrest/pgbackrest/commit/89d5278b74ab0d880345575d7ac4c239cd1fce54)
- تخطي الملفات المقتطعة أثناء النسخ الاحتياطي عند التجميع. (*ساهم به Georgy Shelkovy. راجعه David Steele.*)

  كان الملف الذي يُقتطع إلى الصفر بعد توزيع الملفات على الحزم يظل مخزنًا في حزمته، وكان بناء التصحيح يفشل في تحقق تأكيدي. تُتجاوز هذه الملفات الآن.

  [`02eea55`](https://github.com/pgbackrest/pgbackrest/commit/02eea555c7169e99892fdbc8ce7cc1ee59f50509) تجاوز الملفات المقتطعة أثناء النسخ الاحتياطي عند التجميع.; طلب الدمج [#2227](https://github.com/pgbackrest/pgbackrest/pull/2227)

  [`c879509`](https://github.com/pgbackrest/pgbackrest/commit/c8795094d418802a0e24d4d19da66973c71b00e5) السماح بإرجاع مخازن المجاميع الاختبارية المؤقتة المؤهلة بـ const من backupFile().

  [`9049fec`](https://github.com/pgbackrest/pgbackrest/commit/9049fec2c02c4110e16ffdff7b56f83d8ff32b4a) إعادة تنظيم تجاوز الملفات المقتطعة أثناء النسخ الاحتياطي عند التجميع.

  التطوير في [v2.49](#v249-release-notes):

  [`337da35`](https://github.com/pgbackrest/pgbackrest/commit/337da35ab278e058ec4cdffeb4319f1a1e2cb0df) إضافة اختبار يوضح سلوك الملفات المجمّعة التي تُقتطع أثناء النسخ الاحتياطي.
- تحسين رسائل أخطاء تخزين SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)

  طلب الدمج [#2249](https://github.com/pgbackrest/pgbackrest/pull/2249); الالتزام [`7c17eec`](https://github.com/pgbackrest/pgbackrest/commit/7c17eec3db455d3e8e660f4f8247b6975517648f)

### ملاحظات إصدار v2.49 {#v249-release-notes}

*إزالة دعم PostgreSQL 9.3*

*صدر في 27 نوفمبر 2023*

**إصلاحات الأخطاء:**

- إصلاح تراجع في عمليات إعادة المحاولة. (*راجعه Stephen Frost. أبلغ عنه Norman Adkins، Tanel Suurhans، Jordan English، Timothée Peignier.*)

  أزال v2.48 إعادة المحاولة التي كانت تُجرى عندما تستنفد العملية مهلتها بالكامل، فأصبح انتهاء المهلة خطأ، مثل انتظار جاهزية مقبس للكتابة على تخزين كائنات. تُجرى الآن محاولتان إضافيتان حتى بعد انتهاء المهلة.

  [`3c116e1`](https://github.com/pgbackrest/pgbackrest/commit/3c116e1829a0df62aaf50ce241c63d829eb438e0) إزالة ترويسة غير مستخدمة.

  [`fa5b2d4`](https://github.com/pgbackrest/pgbackrest/commit/fa5b2d44ad9f7591517eecaaaaeb07e9500dd51c) إصلاح تراجع في سلوك إعادة المحاولات.; المشكلة [#2200](https://github.com/pgbackrest/pgbackrest/issues/2200); المشكلة [#2214](https://github.com/pgbackrest/pgbackrest/issues/2214); طلب الدمج [#2221](https://github.com/pgbackrest/pgbackrest/pull/2221)
- إصلاح الحذف العودي للمسارات في مشغّل تخزين SFTP. (*أصلحه Reid Thompson. راجعه Stephen Frost. أبلغ عنه Luc.*)

  تُبلغ بعض خوادم SFTP عن رفض الإذن بدلًا من فشل عام عند محاولة حذف دليل كملف، ولذلك كان الحذف التكراري لمسار يفشل على هذه الخوادم.

  المشكلة [#2219](https://github.com/pgbackrest/pgbackrest/issues/2219); طلب الدمج [#2226](https://github.com/pgbackrest/pgbackrest/pull/2226); الالتزام [`c4dc466`](https://github.com/pgbackrest/pgbackrest/commit/c4dc4665f88e9d67a3b66f44cd59d6dd4bb5107f)

**التحسينات:**

- إزالة دعم PostgreSQL `9.3`. (*راجعه Stephen Frost.*)

  لم يعد PostgreSQL 9.3 مدعومًا، وفق سياسة دعم خمسة إصدارات من PostgreSQL انتهى عمر دعمها.

  طلب الدمج [#2220](https://github.com/pgbackrest/pgbackrest/pull/2220); الالتزام [`dcf0781`](https://github.com/pgbackrest/pgbackrest/commit/dcf078198761a2cfe9be6b4c7f4b4fb07ef53cbf)

**ميزات التوثيق:**

- توثيق خيارات المشرفين. (*راجعه Stefan Fercot.*)

  تُوثَّق الآن خيارات المشرفين في قسم مستقل مع التنبيهات المتعلقة باستخدامها، ولم يعد `pg-version-force` خيارًا داخليًا.

  طلب الدمج [#2202](https://github.com/pgbackrest/pgbackrest/pull/2202); الالتزام [`21c8c8a`](https://github.com/pgbackrest/pgbackrest/commit/21c8c8a66cb06eba714bfa41bed7239af3d14f08)
- تحديث توثيق الاسترداد إلى نقطة زمنية لـ PostgreSQL >= 13.

  منذ PostgreSQL 13، يُصدر الاسترداد خطأ إذا لم يُبلَغ هدف الاسترداد. يعمل قسم الاسترداد إلى نقطة زمنية الآن مع PostgreSQL 13 والإصدارات اللاحقة وكذلك الإصدارات الأقدم.

  الالتزام [`eb69e2e`](https://github.com/pgbackrest/pgbackrest/commit/eb69e2ee6339047f0145b751437ac2bec82bb5ab)

**تحسينات مجموعة الاختبارات:**

- السماح بتشغيل اختبار الوحدة `config/load` دون تثبيت `libssh2`. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Wu Ning.*)

  المشكلة [#2193](https://github.com/pgbackrest/pgbackrest/issues/2193); طلب الدمج [#2194](https://github.com/pgbackrest/pgbackrest/pull/2194); الالتزام [`e2b734e`](https://github.com/pgbackrest/pgbackrest/commit/e2b734eff97e3fac32895b799cc32126013aae27)

### ملاحظات إصدار v2.48 {#v248-release-notes}

*وسوم تخزين المستودع*

*صدر في 25 سبتمبر 2023*

**إصلاحات الأخطاء:**

- إصلاح مشكلة استعادة التزايدي بالكتل دون قائمة كتل. (*راجعه Stephen Frost. اختبره Burak Yurdakul. أبلغ عنه Burak Yurdakul.*)

  لم تكن خريطة الكتل الخالية من الكتل، التي تُكتب عند تغير الطابع الزمني للملف دون تغير محتواه، تُفكّ شيفرتها إذا جاءت بعد ملف مخزن دون نسخ تزايدي على مستوى الكتل ضمن قراءة الحزمة نفسها. مع عدد كافٍ من الملفات المتأثرة، كانت محاولات الإعادة تُستنفد وتفشل الاستعادة.

  المشكلة [#2182](https://github.com/pgbackrest/pgbackrest/issues/2182); طلب الدمج [#2184](https://github.com/pgbackrest/pgbackrest/pull/2184); الالتزام [`31de127`](https://github.com/pgbackrest/pgbackrest/commit/31de127cf42438b1fac04c161c47264aa1fb1060)

**الميزات:**

- إضافة خيار `--repo-storage-tag` لإنشاء وسوم الكائنات. (*راجعه Stephen Frost، Stefan Fercot، Timothée Peignier.*)

  عيّن `repo-storage-tag` لإضافة وسوم إلى الكائنات المكتوبة إلى مستودع S3 أو GCS أو Azure. تُضبط الوسوم لكل مستودع على حدة.

  المشكلة [#2150](https://github.com/pgbackrest/pgbackrest/issues/2150); طلب الدمج [#2159](https://github.com/pgbackrest/pgbackrest/pull/2159); الالتزام [`1b4e0cc`](https://github.com/pgbackrest/pgbackrest/commit/1b4e0cce5f3ff5ea3ee0b889e6d4ce4de1430b04)
- إضافة فحص المضيفين المعروفين لمشغّل تخزين SFTP. (*ساهم به Reid Thompson. راجعه Stephen Frost، David Steele.*)

  تُفحص مفاتيح مضيف SFTP الآن مقابل ملفات المضيفين المعروفين افتراضيًا، أي باستخدام `repo-sftp-host-key-check-type=strict`. عيّن `repo-sftp-host-key-check-type=accept-new` لإضافة المضيفين الجدد تلقائيًا، أو `repo-sftp-host-key-check-type=none` لتجاوز الفحص كما في السابق.

  طلب الدمج [#2125](https://github.com/pgbackrest/pgbackrest/pull/2125); الالتزام [`ce9ba0f`](https://github.com/pgbackrest/pgbackrest/commit/ce9ba0fadee652d409488bee701ea6a51cafec75)
- دعم الاتصالات ثنائية المكدس. (*راجعه Stephen Frost.*)

  تُجرَّب الآن بالتتابع كل العناوين التي يُحل إليها اسم المضيف، مثل عنوان IPv6 بلا مسار إلى المضيف ثم عنوان IPv4، حتى يتصل أحدها أو تنتهي المهلة. كما تُلخَّص أخطاء إعادة المحاولة المتكررة في رسائل الأخطاء.

  [`5314dbf`](https://github.com/pgbackrest/pgbackrest/commit/5314dbffc761bc7507db02693f2421c1578efe10) ضبط الكائن Wait لزيادة الدقة عند الاستخدام المتداخل.

  [`c180513`](https://github.com/pgbackrest/pgbackrest/commit/c1805134b370f0c5c54c40a2df8978599328784f) تجميع أخطاء إعادة المحاولات في مخرجات ErrorRetry.

  [`edbd520`](https://github.com/pgbackrest/pgbackrest/commit/edbd520c81f5d437963aaf42d1c79b2c51d01665) إعادة تنظيم البحث عن قائمة العناوين لتشمل جميع العناوين المعادة.; طلب الدمج [#2174](https://github.com/pgbackrest/pgbackrest/pull/2174)

  [`39bb8a0`](https://github.com/pgbackrest/pgbackrest/commit/39bb8a0d3a96eef63219dff262a9306a4f59dae9) دعم الاتصالات ذات المكدس المزدوج.; المشكلة [#2154](https://github.com/pgbackrest/pgbackrest/issues/2154); طلب الدمج [#2175](https://github.com/pgbackrest/pgbackrest/pull/2175)
- إضافة حجم النسخة الاحتياطية المكتمل/الإجمالي إلى مخرجات JSON للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  تتضمن مخرجات JSON للأمر `info` الآن الحجم المنجز والإجمالي للنسخة الاحتياطية الجارية، بحيث تستطيع البرامج الأخرى مراقبة التقدم.

  المشكلة [#2007](https://github.com/pgbackrest/pgbackrest/issues/2007); طلب الدمج [#2141](https://github.com/pgbackrest/pgbackrest/pull/2141); الالتزام [`e3fcd8c`](https://github.com/pgbackrest/pgbackrest/commit/e3fcd8cd9e0be42a32fc4cbd2ae3db2c072eabcd)

**التحسينات:**

- الأمر `check` متعدد الـ stanza. (*راجعه Stephen Frost.*)

  عندما لا يُحدد `stanza`، يفحص الأمر `check` الآن كل مقاطع stanza في الإعداد.

  طلب الدمج [#2057](https://github.com/pgbackrest/pgbackrest/pull/2057); الالتزام [`1141dc2`](https://github.com/pgbackrest/pgbackrest/commit/1141dc20708cf0c68296f83e74c872a7db9c2bd9)
- إعادة محاولة قراءات `pg_control` حتى يصبح المجموع الاختباري صالحًا. (*راجعه Stefan Fercot، Stephen Frost.*)

  في بعض أنظمة الملفات، مثل ext4، قد تعيد قراءة `pg_control` أثناء كتابة متزامنة بيانات ممزقة. تُعاد القراءة الآن حتى يكون المجموع الاختباري صالحًا.

  طلب الدمج [#2131](https://github.com/pgbackrest/pgbackrest/pull/2131); الالتزام [`f42d927`](https://github.com/pgbackrest/pgbackrest/commit/f42d927d2dcd58cf5a80d68eaf6888bcf2c67a4b)
- تحسين فحص مقاطع WAL بعد نسخة احتياطية ناجحة. (*راجعه Stephen Frost.*)

  كان فحص مقاطع WAL بعد النسخ الاحتياطي يُدرج التخزين مرة لكل مقطع. يُدرج الآن كل دليل WAL مرة واحدة وتُعاد الاستفادة من القائمة.

  طلب الدمج [#2169](https://github.com/pgbackrest/pgbackrest/pull/2169); الالتزام [`9d3a605`](https://github.com/pgbackrest/pgbackrest/commit/9d3a605900644059ff0e030d71a818b3965eb031)
- تحسين أداء الأجزاء المتعددة في GCS. (*راجعه Reid Thompson.*)

  تُحمَّل الآن أجزاء التحميل متعدد الأجزاء فور توفرها.

  طلب الدمج [#2162](https://github.com/pgbackrest/pgbackrest/pull/2162); الالتزام [`6cb9c40`](https://github.com/pgbackrest/pgbackrest/commit/6cb9c40fb8ea18e6572bf3f6e44bbb1d8f922682)
- السماح بتشغيل الأمر `archive-get` عندما تكون الـ stanza متوقفة. (*راجعه Tom Swartz، David Christensen، Reid Thompson.*)

  لا يكتب الأمر `archive-get` إلى المستودع، ولذلك يمكنه الآن العمل عندما يكون مقطع stanza متوقفًا، كما يستطيع `restore`.

  الالتزام [`fbd992a`](https://github.com/pgbackrest/pgbackrest/commit/fbd992adc7b18db5e70774d675c160c8c8e2f031)
- قبول التلدة (~) البادئة في مسارات المفاتيح العامة/الخاصة لـ SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)

  يمكن الآن لمساري `repo-sftp-private-key-file` و`repo-sftp-public-key-file` أن يبدآ بـ `~` كما هو موثق.

  طلب الدمج [#2136](https://github.com/pgbackrest/pgbackrest/pull/2136); الالتزام [`eb32d6d`](https://github.com/pgbackrest/pgbackrest/commit/eb32d6de5e1575a37efb166abbf7df400d93352e)
- إعادة تحميل بيانات اعتماد GCS قبل تجديد رمز المصادقة. (*راجعه Stephen Frost. اقترحه Daniel Farina.*)

  يُعاد الآن قراءة ملف مفتاح الخدمة قبل تجديد رمز المصادقة، فيمكن استبدال المفتاح أثناء تشغيل الأمر.

  طلب الدمج [#2072](https://github.com/pgbackrest/pgbackrest/pull/2072); الالتزام [`995a8e9`](https://github.com/pgbackrest/pgbackrest/commit/995a8e96691d23eaf3914a425669f89deb3ce002)

**إصلاحات أخطاء التوثيق:**

- إصلاح مثال مرجع الإعداد لخيار `tls-server-address`. (*أصلحه Hartmut Goebel. راجعه David Steele.*)

  كان المثال `::*` غير صالح. استخدم `*` لـ IPv4 أو `::` لـ IPv6.

  طلب الدمج [#2165](https://github.com/pgbackrest/pgbackrest/pull/2165); الالتزام [`43524a4`](https://github.com/pgbackrest/pgbackrest/commit/43524a47a4c6a847f76514812f94b87cb7af4c05)
- إصلاح مثال مرجع الأوامر لخيار `filter`.

  الالتزام [`cb3ff6e`](https://github.com/pgbackrest/pgbackrest/commit/cb3ff6ed4336af9e4c0643d8224d5bc3d790a655)

**تحسينات مجموعة الاختبارات:**

- السماح بتشغيل اختبار الوحدة `storage/sftp` دون تثبيت `libssh2`. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Wu Ning.*)

  المشكلة [#2163](https://github.com/pgbackrest/pgbackrest/issues/2163); طلب الدمج [#2177](https://github.com/pgbackrest/pgbackrest/pull/2177); الالتزام [`c3c0834`](https://github.com/pgbackrest/pgbackrest/commit/c3c0834e170196a1241a368779162fcca65f9ad5)

### ملاحظات إصدار v2.47 {#v247-release-notes}

*تحسينات الأداء وإصلاحات أخطاء*

*صدر في 24 يوليو 2023*

**إصلاحات الأخطاء:**

- الحفاظ على معلومات التزايدي بالكتل في الـ manifest أثناء النسخ الاحتياطي بالدلتا. (*راجعه Stephen Frost. أبلغ عنه Francisco Miguel Biete Banon.*)

  عندما كان الملف يتغير بحيث لن يستخدم النسخ التزايدي على مستوى الكتل لو كان جديدًا، مثل انخفاض حجمه عن الحد أو انتقال طابعه الزمني بعيدًا إلى الماضي، كانت معلوماته الخاصة بالنسخ التزايدي على مستوى الكتل تضيع من manifest لنسخة delta، رغم إمكانية استمرار الإشارة إلى الملف في النسخة السابقة.

  [`1d42aed`](https://github.com/pgbackrest/pgbackrest/commit/1d42aed152563fff6ec70c517d86eb39158b3f20) تحسين التحقق من الملفات المشار إليها في اختبار الوحدة command/backup.

  [`4c27d74`](https://github.com/pgbackrest/pgbackrest/commit/4c27d74bbd3a44d8ab1af140277d3cd8302060c2) الحفاظ على معلومات النسخ التزايدي على مستوى الكتل في manifest أثناء نسخ delta الاحتياطي.; المشكلة [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); طلب الدمج [#2123](https://github.com/pgbackrest/pgbackrest/pull/2123)
- إصلاح أسماء ملفات التزايدي بالكتل في الأمر `verify`. (*راجعه Reid Thompson. أبلغ عنه Francisco Miguel Biete Banon.*)

  كان الأمر `verify` يستخدم امتداد الضغط بدلًا من `.pgbi` لملفات النسخ التزايدي على مستوى الكتل المخزنة خارج حزمة، ولذلك كان يعجز عن العثور عليها.

  المشكلة [#2112](https://github.com/pgbackrest/pgbackrest/issues/2112); طلب الدمج [#2120](https://github.com/pgbackrest/pgbackrest/pull/2120); الالتزام [`cdb7e26`](https://github.com/pgbackrest/pgbackrest/commit/cdb7e26350822b55c00771d6d575242b1202e741)
- إصلاح النسخ الاحتياطي الدلتي التلقائي الزائف عند النسخ من خادم الاستعداد. (*راجعه Stephen Frost. أبلغ عنه krmozejko، Don Seiler.*)

  قد تختلف أحجام الملفات على الاحتياطي عنها على الأساسي، مثل خرائط المساحة الحرة، ولذلك كانت النسخة التزايدية التالية قد ترى تغيرًا في الحجم على الأساسي وتتحول إلى delta بالمجاميع الاختبارية، مما قد يستغرق وقتًا أطول بكثير. يُحتفَظ الآن بالحجم الأصلي في manifest ويُستخدم للمقارنة.

  المشكلة [#2020](https://github.com/pgbackrest/pgbackrest/issues/2020); طلب الدمج [#2124](https://github.com/pgbackrest/pgbackrest/pull/2124); الالتزام [`5ed6f8d`](https://github.com/pgbackrest/pgbackrest/commit/5ed6f8df1487174985c42d6e13c367d70c2d8b8a)
- تخطي `recovery.signal` لـ PostgreSQL >= 12 عندما يكون `type=none` للاسترداد. (*راجعه Stefan Fercot. أبلغ عنه T.Anastacio.*)

  عند استخدام `type=none`، لم يعد `recovery.signal` يُكتب لـ PostgreSQL >= 12، بما يطابق السلوك في الإصدارات الأقدم.

  المشكلة [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); طلب الدمج [#2070](https://github.com/pgbackrest/pgbackrest/pull/2070); الالتزام [`9cceed6`](https://github.com/pgbackrest/pgbackrest/commit/9cceed6ac4a32c14a797eba89a4ad1dc06d89d80)
- إصلاح توليد الاسم الفريد للنسخ الاحتياطي diff/incr. (*أصلحه Andrey Sokolov. راجعه David Steele.*)

  عند وجود نسختين كاملتين على الأقل مع حذف الأحدث، كانت النسخة التفاضلية أو التزايدية تفشل كما لو أن الساعة عادت إلى الوراء، لأن وسمها كان يُقارَن بوسم النسخة الكاملة المحذوفة.

  المشكلة [#1873](https://github.com/pgbackrest/pgbackrest/issues/1873); طلب الدمج [#2104](https://github.com/pgbackrest/pgbackrest/pull/2104); الالتزام [`0ac0934`](https://github.com/pgbackrest/pgbackrest/commit/0ac09344dc17fb54e250705ce49399b86329bb3d)
- إصلاح انتهاء صلاحية الأرشيف الزمني عندما لا تنتهي صلاحية أي نسخة احتياطية. (*راجعه Stefan Fercot.*)

  عندما كانت مدة الاحتفاظ مستوفاة دون حذف أي نسخ احتياطية، لم يكن الأرشيف يُحذف وكانت تُسجَّل الرسالة "time-based archive retention not met". وكان يلزم إنشاء نسخة احتياطية إضافية لحذف ملفات WAL الأقدم.

  المشكلة [#2103](https://github.com/pgbackrest/pgbackrest/issues/2103); طلب الدمج [#2109](https://github.com/pgbackrest/pgbackrest/pull/2109); الالتزام [`762498f`](https://github.com/pgbackrest/pgbackrest/commit/762498f4cd5f1425db4c176fc707926d62cc7c04)

**التحسينات:**

- تحسين أداء مشغّل تخزين SFTP. (*ساهم به Stephen Frost، Reid Thompson. راجعه David Steele.*)

  كان مشغّل تخزين SFTP ينتظر مدة ثابتة عندما يتعذر على libssh2 المتابعة. ينتظر الآن حتى يصبح المقبس جاهزًا للقراءة أو الكتابة.

  [`e280ed9`](https://github.com/pgbackrest/pgbackrest/commit/e280ed9098a6f5da9bdabb541e9c69d4f24ffcf2) جعل معالجة رموز النتائج في storage/sftp أكثر اتساقًا.

  [`125676a`](https://github.com/pgbackrest/pgbackrest/commit/125676ae0e98d3730d2dc0d47e37ca1df145d044) تنقيح التهيئة والمصافحة في storageSftpNew().

  [`28b6b2d`](https://github.com/pgbackrest/pgbackrest/commit/28b6b2d4659d78ce67c1bd3104d96e5705d955c9) تحسين أداء مشغّل تخزين SFTP.; طلب الدمج [#2089](https://github.com/pgbackrest/pgbackrest/pull/2089)
- إضافة إزاحة المنطقة الزمنية إلى مخرجات التاريخ/الوقت للأمر `info`. (*راجعه Stefan Fercot، Philip Hurst. اقترحه Philip Hurst.*)

  تتضمن الطوابع الزمنية في مخرجات الأمر `info` الآن إزاحة المنطقة الزمنية، فيمكن استخدامها مباشرةً هدفًا للاسترداد، مثلًا مع `--target`.

  [`9efd5cd`](https://github.com/pgbackrest/pgbackrest/commit/9efd5cd0bb40c5dc2fcac2e21c9b62e554b94db6) إضافة إزاحة المنطقة الزمنية إلى مخرجات التاريخ والوقت للأمر info.; المشكلة [#2093](https://github.com/pgbackrest/pgbackrest/issues/2093); طلب الدمج [#2095](https://github.com/pgbackrest/pgbackrest/pull/2095)

  [`aa229a1`](https://github.com/pgbackrest/pgbackrest/commit/aa229a1deef3afeebb66db1443b19e24559adf96) تعديل تحويلات time_t استجابةً لملاحظات Coverity.
- مركزنة معالجة الأخطاء للميزات غير المدعومة. (*راجعه Stefan Fercot.*)

  أصبحت أخطاء الميزات غير المضمنة في البناء، مثل lz4، أكثر تفصيلًا واتساقًا. ولم يعد تحديد تخزين SFTP عندما لا يكون مضمنًا في البناء يفشل في تحقق تأكيدي.

  [`de46276`](https://github.com/pgbackrest/pgbackrest/commit/de46276bf60b8a2181621b123d1a99e56808a089) إعادة تنظيم معالجة قائمة القيم المسموح بها في الوحدة config/parse.

  [`36ff81d`](https://github.com/pgbackrest/pgbackrest/commit/36ff81dc6ff7e98e40c0c05a4a343a71b91b1678) توحيد معالجة أخطاء الميزات غير المدعومة في موضع مركزي.; طلب الدمج [#2075](https://github.com/pgbackrest/pgbackrest/pull/2075)

**تحسينات التوثيق:**

- توضيح تفضيل التثبيت من الحزم في دليل المستخدم. (*راجعه Stefan Fercot. اقترحه dr-kd.*)

  طلب الدمج [#2090](https://github.com/pgbackrest/pgbackrest/pull/2090); الالتزام [`a36f480`](https://github.com/pgbackrest/pgbackrest/commit/a36f480c85c7add6fdf0e5517748d740e3a7b424)

### ملاحظات إصدار v2.46 {#v246-release-notes}

*النسخ الاحتياطي التزايدي بالكتل وتخزين SFTP*

*صدر في 22 مايو 2023*

**الميزات:**

- النسخ الاحتياطي التزايدي بالكتل. (*راجعه John Morris، Stephen Frost، Stefan Fercot.*)

  يخزن النسخ التزايدي على مستوى الكتل الأجزاء التي تغيرت فقط منذ النسخة السابقة، مما يوفر المساحة والوقت في النسخ التفاضلية والتزايدية للملفات الكبيرة. فعّله باستخدام `repo-block` الذي يتطلب `repo-bundle`.

  [`dd4e526`](https://github.com/pgbackrest/pgbackrest/commit/dd4e52679ecdc43539bd038b5aa9bd4ff9055cbf) إزالة التقسيم إلى أجزاء وأرقام الكتل من قائمة الكتل التزايدية.; طلب الدمج [#2029](https://github.com/pgbackrest/pgbackrest/pull/2029)

  [`822f2a5`](https://github.com/pgbackrest/pgbackrest/commit/822f2a584260a012b833455a7a2bd1c8487e3010) استكمال ميزة النسخ التزايدي على مستوى الكتل.; طلب الدمج [#2053](https://github.com/pgbackrest/pgbackrest/pull/2053)
- دعم SFTP لتخزين المستودع. (*ساهم به Reid Thompson. راجعه Stephen Frost، David Steele.*)

  عيّن `repo-type=sftp` و`repo-sftp-host` لتخزين المستودع على خادم SFTP.

  طلب الدمج [#1959](https://github.com/pgbackrest/pgbackrest/pull/1959); الالتزام [`87087fa`](https://github.com/pgbackrest/pgbackrest/commit/87087fac231d2110160b3219daee3f9fb91aec02)

  التطوير في [v2.42](#v242-release-notes):

  [`01b81f9`](https://github.com/pgbackrest/pgbackrest/commit/01b81f9d374701eb489dd1888bcba25fb5d6df84) نقل إنشاء الروابط إلى واجهة التخزين.; طلب الدمج [#1879](https://github.com/pgbackrest/pgbackrest/pull/1879)
- دعم PostgreSQL 16. (*راجعه Stefan Fercot.*)

  إضافة إصدار الكتالوج والرقم السحري لـ WAL في PostgreSQL 16.

  طلب الدمج [#2051](https://github.com/pgbackrest/pgbackrest/pull/2051); الالتزام [`3fc3690`](https://github.com/pgbackrest/pgbackrest/commit/3fc3690dd77ef5fa032abb006558184164db53ec)

**التحسينات:**

- السماح بتخطي فحوصات ترويسة الصفحة. (*راجعه David Christensen. اقترحه David Christensen.*)

  قد تُبلغ فحوصات ترويسة الصفحة أثناء التحقق من المجاميع الاختبارية عن أخطاء زائفة للصفحات المشفّرة. عيّن `page-header-check=n` لتجاوزها. تكون مفعّلة افتراضيًا.

  طلب الدمج [#2045](https://github.com/pgbackrest/pgbackrest/pull/2045); الالتزام [`f5e6bc2`](https://github.com/pgbackrest/pgbackrest/commit/f5e6bc26983396ec51c6579aade37db39807f3a5)
- تجنّب `chown()` على ملفات الاسترداد أثناء الاستعادة. (*راجعه Stefan Fercot، Marcelo Henrique Neppel. اقترحه Marcelo Henrique Neppel.*)

  كانت الاستعادة تتجاوز `chown()` للملفات المستعادة ذات المالك الصحيح بالفعل، لكن ليس لملفات الاسترداد التي تكتبها. يتجاوز مشغّل Posix الآن أيضًا `chown()` عندما يكون المالك صحيحًا بالفعل.

  المشكلة [#2036](https://github.com/pgbackrest/pgbackrest/issues/2036); طلب الدمج [#2038](https://github.com/pgbackrest/pgbackrest/pull/2038); الالتزام [`3ff88ff`](https://github.com/pgbackrest/pgbackrest/commit/3ff88ffbb495fd669e9a361478e60192930ee0a1)
- إضافة تفاصيل إعادة المحاولة للأخطاء في إعادة محاولات HTTP.

  يُبلغ الخطأ بعد إعادة محاولات HTTP الآن عن عدد المحاولات ومدتها.

  [`801e396`](https://github.com/pgbackrest/pgbackrest/commit/801e396dace2a4d9f4125ef0e751c90dc0cc644a) نقل وحدات الأخطاء إلى الدليل common/error.

  [`df419b3`](https://github.com/pgbackrest/pgbackrest/commit/df419b34b55a15a902ff5cc1912aaebc7e023738) تحسين رسائل أخطاء إعادة المحاولات.

  [`f33e1cf`](https://github.com/pgbackrest/pgbackrest/commit/f33e1cfb1600643820a1ae76bdeb15c62ac1fcc7) إضافة تفاصيل الأخطاء لإعادة محاولات HTTP.

**تحسينات التوثيق:**

- إضافة تحذير حول استخدام `type=none` للاسترداد. (*راجعه Stefan Fercot.*)

  لا يزيد الاسترداد باستخدام `type=none` رقم الخط الزمني عند انتهائه، مما قد يجعل PostgreSQL يؤرشف ملفات WAL مكررة تُرفض وتملأ القرص، وقد يتسبب في فشل أدوات مثل `pg_rewind` أو إفساد العنقود. يحذّر التوثيق الآن من ذلك.

  المشكلة [#2062](https://github.com/pgbackrest/pgbackrest/issues/2062); طلب الدمج [#2069](https://github.com/pgbackrest/pgbackrest/pull/2069); الالتزام [`a28b72c`](https://github.com/pgbackrest/pgbackrest/commit/a28b72c62431bcf9df02791219d9d6f5d0e60b54)
- إضافة ملاحظة حول تشغيل `stanza-create` على مستودعات أُنشئت بالفعل.

  تُتجاوز مقاطع stanza الموجودة بالفعل، ولذلك يمكن تشغيل `stanza-create` مجددًا بأمان، مثلًا بعد إعداد مستودع جديد.

  الالتزام [`0c1f823`](https://github.com/pgbackrest/pgbackrest/commit/0c1f823e7a3abf1cadb44de3832ec1ddb2da7ec8)

### ملاحظات إصدار v2.45 {#v245-release-notes}

*النسخ الاحتياطي التزايدي بالكتل (BETA)*

*صدر في 20 مارس 2023*

**إصلاحات الأخطاء:**

- تخطي كتابة `recovery.signal` افتراضيًا لاستعادة النسخ الاحتياطية المأخوذة أثناء توقف PostgreSQL. (*راجعه Stefan Fercot. أبلغ عنه Marcel Borger.*)

  على PostgreSQL >= 12، يمنع `recovery.signal` بدء PostgreSQL عندما تكون النسخة أُنشئت دون اتصال مع `wal_level=minimal`. تتجاوز الاستعادة الآن كتابة هذا الملف للنسخ غير المتصلة ما لم يُضبط `type` صراحةً، مثل الاسترداد إلى نقطة زمنية من نسخة غير متصلة أُنشئت بقيمة أعلى لـ `wal_level`.

  [`0818601`](https://github.com/pgbackrest/pgbackrest/commit/0818601c055724bde3b97d4b02d3a38b0a53899a) ضبط علامة online في manifest ضمن اختبارات الوحدة command/restore.

  [`2fa7e53`](https://github.com/pgbackrest/pgbackrest/commit/2fa7e53c5d4b5a5fd79f62d39763746727a5b9be) تجاوز كتابة recovery.signal افتراضيًا عند استعادة النسخ الاحتياطية غير المتصلة.; المشكلة [#2018](https://github.com/pgbackrest/pgbackrest/issues/2018); طلب الدمج [#2019](https://github.com/pgbackrest/pgbackrest/pull/2019)

**الميزات:**

- النسخ الاحتياطي التزايدي بالكتل (BETA). (*راجعه John Morris، Stephen Frost، Stefan Fercot.*)

  يخزن النسخ التزايدي على مستوى الكتل الأجزاء التي تغيرت منذ النسخة السابقة فقط بدلًا من الملف كاملًا. فعّله باستخدام `repo-block` الذي يتطلب `repo-bundle`. الميزة في مرحلة تجريبية وتتطلب أيضًا الخيار `beta`. لا تستخدمها في بيئة الإنتاج: سيتغير التنسيق على القرص قبل الإصدار العام.

  [`089fae0`](https://github.com/pgbackrest/pgbackrest/commit/089fae035bf0a9778fff0527ea3cbb113625a403) إضافة النسخ التزايدي على مستوى الكتل إلى مخرجات اختبار real/all.

  [`3feed38`](https://github.com/pgbackrest/pgbackrest/commit/3feed389a2199454db68e446851323498b45db20) تحسين معالجة نهاية الملف في IoChunkedRead.

  [`d520816`](https://github.com/pgbackrest/pgbackrest/commit/d520816acf9ecb01ef805cecbc9de7e8d0a9f468) إزالة قائمة المعاملات من deltaMapNew().

  [`779efe0`](https://github.com/pgbackrest/pgbackrest/commit/779efe0d7a54340141e01597279e9ab1d0bd0773) التصريح بحجم الكتلة التزايدية بشكل متسق بالنوع size_t.

  [`dffc933`](https://github.com/pgbackrest/pgbackrest/commit/dffc933384e4327e2fd52868dd19668ed9d3ed91) إعادة تسمية DeltaMap إلى BlockHash.

  [`a9867cb`](https://github.com/pgbackrest/pgbackrest/commit/a9867cb0b8e8d7abcac9b18b76e3e490c265f3cb) إضافة الخيارين repo-block-age-map وrepo-block-size-map.

  [`16ac5ee`](https://github.com/pgbackrest/pgbackrest/commit/16ac5ee8d3b926464cd27e8f064579f1e7935f4c) إعادة تسمية مفاتيح manifest للنسخ التزايدي على مستوى الكتل.

  [`da91858`](https://github.com/pgbackrest/pgbackrest/commit/da9185870222057b97365f5db0acf797f959ec5e) إضافة تنسيق خام اختياري لأنواع الضغط.

  [`7e5adc0`](https://github.com/pgbackrest/pgbackrest/commit/7e5adc03594a3b7a975001e80902a51df3ddd577) استخدام الضغط والتشفير بالتنسيق الخام للتجميع والنسخ التزايدي على مستوى الكتل.

  [`8b5153a`](https://github.com/pgbackrest/pgbackrest/commit/8b5153ad210011812c8fe6db2f2ed829a5aa543a) إضافة كتل فائقة للنسخ التزايدي على مستوى الكتل.; طلب الدمج [#1996](https://github.com/pgbackrest/pgbackrest/pull/1996)

  [`210bed4`](https://github.com/pgbackrest/pgbackrest/commit/210bed4511ae5523b170eb193b877346d787140d) استخدام xxHash بدلًا من SHA-1 للمجاميع الاختبارية للكتل التزايدية.

  [`6252c0e`](https://github.com/pgbackrest/pgbackrest/commit/6252c0e4485caee362edec13302a5f735a69bff4) استبعاد حجم مجموعة النسخ الاحتياطية من info للنسخ التزايدية على مستوى الكتل.

  [`1119a53`](https://github.com/pgbackrest/pgbackrest/commit/1119a5353911d6d326edac325f530bb796a806ae) إعادة تسمية BlockHash إلى BlockChecksum.

  [`6b409d0`](https://github.com/pgbackrest/pgbackrest/commit/6b409d049eb935146f7996b75b97744b75c411a9) تحديث القيم الافتراضية لحجم الكتلة والكتلة الفائقة بناءً على الاختبارات.

  [`1281a6e`](https://github.com/pgbackrest/pgbackrest/commit/1281a6eaf8552232c8c9af4d7fc15c082a7794d9) ضمان عدم وجود أجزاء استمرار عندما يساوي حجم الكتلة حجم الكتلة الفائقة.

  [`5c1f78d`](https://github.com/pgbackrest/pgbackrest/commit/5c1f78d4dd62c37218285d13b09a9450eb3a588e) إصلاح خطأ مطبعي في blockIncrProcess().

  [`c30d3e4`](https://github.com/pgbackrest/pgbackrest/commit/c30d3e439b77d544477e289606d30d0c8ffe301f) إصلاحات وتحسينات لخريطة الكتل التزايدية.; طلب الدمج [#2026](https://github.com/pgbackrest/pgbackrest/pull/2026)

  [`24f7252`](https://github.com/pgbackrest/pgbackrest/commit/24f725212d0c1dedc0f34fe4e939e481585ff697) إضافة البنية التحتية للميزات التجريبية.

  [`04d224b`](https://github.com/pgbackrest/pgbackrest/commit/04d224b88e73194ff1c6497dbecaaff392008dfe) إضافة ميزة النسخ التزايدي على مستوى الكتل التجريبية وتوثيقها.

  التطوير في [v2.44](#v244-release-notes):

  [`912eec6`](https://github.com/pgbackrest/pgbackrest/commit/912eec63bb971c10a545e582f628c982f4e00005) النسخ الاحتياطي التزايدي على مستوى الكتل.; المشكلة [#959](https://github.com/pgbackrest/pgbackrest/issues/959); المشكلة [#1806](https://github.com/pgbackrest/pgbackrest/issues/1806); المشكلة [#1913](https://github.com/pgbackrest/pgbackrest/issues/1913); طلب الدمج [#1916](https://github.com/pgbackrest/pgbackrest/pull/1916)

  التطوير في [v2.42](#v242-release-notes):

  [`1ea6a41`](https://github.com/pgbackrest/pgbackrest/commit/1ea6a4142e47e2e0b56911ad1f028dfcddc5fd64) تحسين تحديثات ملفات manifest.; طلب الدمج [#1888](https://github.com/pgbackrest/pgbackrest/pull/1888)

  [`c647bcb`](https://github.com/pgbackrest/pgbackrest/commit/c647bcb50954f623d29104cdb8a1457ed8e94579) إضافة علامات إلى manifest لمعالجة الملفات أثناء النسخ الاحتياطي.; طلب الدمج [#1889](https://github.com/pgbackrest/pgbackrest/pull/1889)

  [`102ce5d`](https://github.com/pgbackrest/pgbackrest/commit/102ce5dee47e8d9a8d2eeaf2b2cc2bac105914ef) إضافة قائمة مراجع دائمة إلى manifest.; طلب الدمج [#1890](https://github.com/pgbackrest/pgbackrest/pull/1890)

  [`ac99201`](https://github.com/pgbackrest/pgbackrest/commit/ac99201c0ebde616279214e600e49fdf506f7469) إضافة bufferSize إلى cvtUInt64FromVarInt128() لتقييد القراءات أكثر.

  [`5602f17`](https://github.com/pgbackrest/pgbackrest/commit/5602f179a177a8513b96c762590829c012c28175) إضافة ترميز وفك ترميز varint-128 إلى IoRead/IoWrite.; طلب الدمج [#1891](https://github.com/pgbackrest/pgbackrest/pull/1891)

  [`352cbf1`](https://github.com/pgbackrest/pgbackrest/commit/352cbf1d5738a720292b5067051a05efc2b9a8ac) تحويل الحقول المنطقية في ManifestFile إلى حقول بتّية.

  [`e7e106f`](https://github.com/pgbackrest/pgbackrest/commit/e7e106f781be01027d4829b258902549eb36eb7b) استخدام تخزين للقراءة فقط لحساب المجموع الاختباري في restoreFile().

  [`909be41`](https://github.com/pgbackrest/pgbackrest/commit/909be412f8ad0d87f23ce2a2dbca94c3e0732f9f) تبديل اختباري الوحدة command/backup وcommand/restore.

  [`1730ef4`](https://github.com/pgbackrest/pgbackrest/commit/1730ef4ac3d88137bd218e6128b0107a8bf2c121) إضافة العلامة noTruncate إلى storageNewWriteP().; طلب الدمج [#1898](https://github.com/pgbackrest/pgbackrest/pull/1898)

  [`fee38c2`](https://github.com/pgbackrest/pgbackrest/commit/fee38c2c7cc3ae318bf0d3b50fe23c22900c2311) تمرير المرشحات إلى التخزين البعيد كمصفوفة معالجات.

  [`5fceee8`](https://github.com/pgbackrest/pgbackrest/commit/5fceee88a9439460bf24082f275ec2e695cc6bf6) إضافة backupFileRepoPathP().

  [`221db61`](https://github.com/pgbackrest/pgbackrest/commit/221db610d2a054ed00ad27377663941abfb9fb98) اختصار الأسماء في مصفوفة اختبارات التكامل real/all.

  [`c9db7bc`](https://github.com/pgbackrest/pgbackrest/commit/c9db7bc274211820030c4ab6ab8c70c1b1896254) تحديث cipherBlockNew() لدعم معاملات اختيارية.

  [`58b3c91`](https://github.com/pgbackrest/pgbackrest/commit/58b3c91babc6af9e003e5ef09bf99becf8a6f827) إضافة وضع خام إلى CipherBlock لتوفير المساحة.

**التحسينات:**

- الإبقاء على فهرس مجموعة واحد فقط تكون جميع قيمه افتراضية. (*راجعه Stefan Fercot.*)

  كان يمكن لخيار غير منطبق، مثل `repo2-s3-key` عندما لا يكون `repo2-type` هو `s3`، أن يضيف مستودعًا وهميًا لا يضم إلا قيمًا افتراضية. تُزال الآن فهارس المستودعات وPostgreSQL التي لا تحتوي إلا على قيم افتراضية، ما لم يكن حذفها سيترك النظام دون أي فهرس آخر.

  طلب الدمج [#2011](https://github.com/pgbackrest/pgbackrest/pull/2011); الالتزام [`1648c13`](https://github.com/pgbackrest/pgbackrest/commit/1648c133d6bc1ffd0682ae6219934d00295aa580)

**تحسينات التوثيق:**

- إضافة تعليمات صريحة للترقية بين إصدارات `2.x`. (*ساهم به Christophe Courtois. راجعه David Steele.*)

  يوضح قسم جديد في دليل المستخدم أن الترقية بين إصدارات `2.x` لا تتطلب سوى تثبيت الملفات التنفيذية الجديدة. ويمكن أيضًا الرجوع إلى إصدار أقدم إذا لم تُستخدم ميزات غير مدعومة فيه.

  المشكلة [#1774](https://github.com/pgbackrest/pgbackrest/issues/1774); طلب الدمج [#1993](https://github.com/pgbackrest/pgbackrest/pull/1993); الالتزام [`15d5dcd`](https://github.com/pgbackrest/pgbackrest/commit/15d5dcdd3bb387aab28bbe7262011c38c7d6d22c)
- إزالة الإشارات إلى SSH التي أصبحت متقادمة عند إدخال TLS.

  لم تعد مساعدة `repo-host` و`pg-host` وخيارات المنافذ التابعة لهما تشير إلى SSH بوصفه البروتوكول البعيد الوحيد. وأُزيلت أيضًا تفاصيل ضغط SSH.

  الالتزام [`c5907a2`](https://github.com/pgbackrest/pgbackrest/commit/c5907a2e7193ca8f79cf56dca23e0df118e686c3)

### ملاحظات إصدار v2.44 {#v244-release-notes}

*إزالة دعم PostgreSQL 9.0/9.1/9.2*

*صدر في 30 يناير 2023*

**التحسينات:**

- إزالة دعم PostgreSQL `9.0`/`9.1`/`9.2`. (*راجعه Stefan Fercot.*)

  يدعم pgBackRest الآن عشرة إصدارات من PostgreSQL: الإصدارات الخمسة المدعومة وآخر خمسة إصدارات منتهية الدعم. اعتبارًا من PostgreSQL 15، يستثني ذلك `9.0` و`9.1` و`9.2`.

  طلب الدمج [#1941](https://github.com/pgbackrest/pgbackrest/pull/1941); الالتزام [`77c721e`](https://github.com/pgbackrest/pgbackrest/commit/77c721eb635c6d757d2d5ed6f2ffc083720c10a7)
- إصدار خطأ أثناء الاستعادة عندما لا تطابق أي نسخة احتياطية إصدار PostgreSQL الحالي. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Soulou.*)

  بعد تنفيذ `stanza-upgrade` دون إنشاء نسخة احتياطية جديدة، كانت الاستعادة تستخدم أحدث نسخة المأخوذة من إصدار PostgreSQL السابق. وكان يمكن للنسخ المتماثلة المبنية بهذه الطريقة أن تفشل. تُصدر الاستعادة الآن خطأ في هذه الحالة ما لم يُحدد `set` أو `type=time`/`type=lsn`.

  المشكلة [#1942](https://github.com/pgbackrest/pgbackrest/issues/1942); طلب الدمج [#1967](https://github.com/pgbackrest/pgbackrest/pull/1967); الالتزام [`b9be4fa`](https://github.com/pgbackrest/pgbackrest/commit/b9be4fa54039e2c79fad0dc1552c7ffaf883004c)
- إضافة فحص نطاق `compress-level` لكل `compress-type`. (*راجعه Stefan Fercot. اقترحه gkleen، ViperRu.*)

  كان نطاق `compress-level` هو `0-9` لكل `compress-type`. هذا هو نطاق `gz` لكنه جزء فقط مما يسمح به `lz4` و`zst`. أصبح لكل نوع نطاقه الخاص، مثل `-7` إلى `22` لـ `zst`.

  المشكلة [#1216](https://github.com/pgbackrest/pgbackrest/issues/1216); المشكلة [#1931](https://github.com/pgbackrest/pgbackrest/issues/1931); طلب الدمج [#1962](https://github.com/pgbackrest/pgbackrest/pull/1962); الالتزام [`44da314`](https://github.com/pgbackrest/pgbackrest/commit/44da314adb2b63f96b1d571f822e91a0e412e984)

**تحسينات التوثيق:**

- إضافة تحذير حول تمكين "مساحة الأسماء الهرمية" في تخزين Azure. (*راجعه Stefan Fercot. اقترحه Vojtech Galda، Pluggi، asjonos.*)

  عند تفعيل «مساحة الأسماء الهرمية»، يتطلب Azure حذف الأدلة بشكل منفصل ويفشل `expire`. يحذّر دليل المستخدم الآن من تفعيلها.

  المشكلة [#1770](https://github.com/pgbackrest/pgbackrest/issues/1770); طلب الدمج [#1980](https://github.com/pgbackrest/pgbackrest/pull/1980); الالتزام [`3aea997`](https://github.com/pgbackrest/pgbackrest/commit/3aea997df5ace85251d0579ccbe13fa938f587ee)
- إضافة استبدال الأسطر الجديدة في مثال المراقبة. (*راجعه Stefan Fercot. اقترحه rudonx، gmustdie، Ivan Shelestov.*)

  كان مثال المراقبة يفشل عندما تحتوي مخرجات `info` على محرف سطر جديد، مثل بعض رسائل الأخطاء، لأن `COPY` يحوّل `\n` إلى سطر جديد يرفضه `jsonb`. يستبدل المثال الآن محارف السطر الجديد قبل التحويل إلى `jsonb`.

  المشكلة [#1910](https://github.com/pgbackrest/pgbackrest/issues/1910); طلب الدمج [#1963](https://github.com/pgbackrest/pgbackrest/pull/1963); الالتزام [`ae258f6`](https://github.com/pgbackrest/pgbackrest/commit/ae258f604e634f1d2a760ffdb92dd359fd1129bb)
- توضيح سلوك `target-action` على إصدارات PostgreSQL المختلفة. (*ساهم به Chris Bandy. راجعه David Steele، Anton Kurochkin، Stefan Fercot. اقترحه Anton Kurochkin، Chris Bandy.*)

  يعتمد تأثير `pause` على `hot_standby` وإصدار PostgreSQL. مع `hot_standby=off`، يتصرف `pause` مثل `shutdown` على PostgreSQL >= 12 ومثل `promote` على الإصدارات الأقدم.

  المشكلة [#987](https://github.com/pgbackrest/pgbackrest/issues/987); المشكلة [#1314](https://github.com/pgbackrest/pgbackrest/issues/1314); طلب الدمج [#1960](https://github.com/pgbackrest/pgbackrest/pull/1960); الالتزام [`84a3ff8`](https://github.com/pgbackrest/pgbackrest/commit/84a3ff8b7ac1243c0b47c6585697f4fcf3c12065)
- تحديثات وتوضيحات لصفحة الفهرس. (*راجعه Stefan Fercot.*)

  لم يعد القسم الذي يذكر أن حلول النسخ الاحتياطي الأخرى لا تدعم المعالجة المتوازية دقيقًا، فأُعيدت صياغته. وحُدثت أقسام أخرى لتستخدم المصطلحات الحالية وتكون أوضح.

  طلب الدمج [#1966](https://github.com/pgbackrest/pgbackrest/pull/1966); الالتزام [`36ee30d`](https://github.com/pgbackrest/pgbackrest/commit/36ee30d118ce6cc7720653a3d3a49a06c655c463)
- إضافة الوضع الداكن إلى الموقع الإلكتروني. (*اقترحه Stephen Frost.*)

  يستخدم الموقع ألوانًا داكنة عندما يفضّل المتصفح نظام ألوان داكنًا.

  الالتزام [`ed818b3`](https://github.com/pgbackrest/pgbackrest/commit/ed818b31867c640d72ef829dd36cd0a7feff12df)

### ملاحظات إصدار v2.43 {#v243-release-notes}

*إصلاح خطأ*

*صدر في 28 نوفمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح مرجع مفقود في النسخ الاحتياطي diff/incr. (*راجعه Stefan Fercot. أبلغ عنه Marcel Borger، ulfedf، jaymefSO.*)

  في v2.42، كانت النسخة التفاضلية أو التزايدية تفشل بالرسالة "unable to find '...' in string list" عندما تكون النسخة السابقة أُنشئت بإصدار أقدم. تتضمن الآن قائمة المراجع المبنية لملف manifest من إصدار أقدم وسم النسخة الاحتياطية نفسها.

  [`28f6604`](https://github.com/pgbackrest/pgbackrest/commit/28f660482aa5abb97850a9d7c89c2e5e9f23a4c9) نقل اختبار manifestBackupLabelSet() في وحدة info/manifest.

  [`c4bf775`](https://github.com/pgbackrest/pgbackrest/commit/c4bf775099c85e3cd081f9c1ce35efd4c71d9161) إصلاح مرجع مفقود في النسخ التفاضلي أو التزايدي.; المشكلة [#1933](https://github.com/pgbackrest/pgbackrest/issues/1933); طلب الدمج [#1935](https://github.com/pgbackrest/pgbackrest/pull/1935)

**التحسينات:**

- إضافة تلميح عند تحديد خيار دون فهرس. (*راجعه Stefan Fercot.*)

  الخيار الذي يتطلب فهرسًا، مثل `repo-storage-ca-file`، يُصدر الآن خطأ مع تلميح يعرض الاسم المفهرس، مثل `repo1-storage-ca-file`. ويحصل الخيار المهمل أيضًا على تلميح باسمه الحالي.

  المشكلة [#1925](https://github.com/pgbackrest/pgbackrest/issues/1925); طلب الدمج [#1929](https://github.com/pgbackrest/pgbackrest/pull/1929); الالتزام [`3f363cb`](https://github.com/pgbackrest/pgbackrest/commit/3f363cb3aed1a7c6836ee6c32eae600129a6f6b8)

### ملاحظات إصدار v2.42 {#v242-release-notes}

*إصلاحات أخطاء*

*صدر في 22 نوفمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح تسريب للذاكرة في تجميع الملفات للأمرين `backup`/`restore`. (*راجعه John Morris. اختبره Oscar. أبلغ عنه Oscar.*)

  كانت الاستعادة تحرّر بعض كائنات الإدخال والإخراج للملفات المجمّعة فقط بعد استعادة كل ملفات الحزمة. ومع كثرة الملفات الصغيرة، كان استهلاك الذاكرة يزداد حتى تفشل الاستعادة بالرسالة "unable to allocate". وكان النسخ الاحتياطي يعاني تسربًا مشابهًا أصغر عند الاستئناف.

  المشكلة [#1877](https://github.com/pgbackrest/pgbackrest/issues/1877); طلب الدمج [#1878](https://github.com/pgbackrest/pgbackrest/pull/1878); الالتزام [`cd8db7d`](https://github.com/pgbackrest/pgbackrest/commit/cd8db7d9e53e041ad6fb31f2f015541c1d24abc2)
- إصلاح خطأ في البروتوكول عند قراءة ناقصة لملف بعيد. (*راجعه Stephen Frost.*)

  كانت قراءة ملف بعيد التي تتوقف مبكرًا أو تفشل جزئيًا تترك البروتوكول في حالة غير سليمة. وكان الأمر التالي يفشل بالرسالة "client state is 'data-get' but expected 'idle'" ويضيع الخطأ الأصلي. يُقرأ الآن باقي الملف عند إغلاقه.

  [`ea162e8`](https://github.com/pgbackrest/pgbackrest/commit/ea162e821634919b7c839e866b99bf82010dbacc) نقل storageReadRemoteOpen() في الوحدة storage/remote/read.

  [`7967c75`](https://github.com/pgbackrest/pgbackrest/commit/7967c750d83466d030081e9deb1d70a1ba240271) إصلاح خطأ البروتوكول عند قراءة ناقصة لملف بعيد.; طلب الدمج [#1900](https://github.com/pgbackrest/pgbackrest/pull/1900)

**التحسينات:**

- عدم تخزين المراجع للملفات ذات الطول الصفري عند التجميع. (*راجعه Stefan Fercot.*)

  كانت النسخ التفاضلية والتزايدية المجمّعة تخزن مرجعًا إلى نسخة سابقة للملفات ذات الطول الصفري، التي لا تُخزن في أي نسخة. كان المرجع يُتجاهل عند الاستعادة لكنه يشغل مساحة في manifest.

  طلب الدمج [#1887](https://github.com/pgbackrest/pgbackrest/pull/1887); الالتزام [`f981fb4`](https://github.com/pgbackrest/pgbackrest/commit/f981fb45d9931e597afec764e13b1a53d8365d25)
- استخدام أوصاف أكثر عمومية للدالتين `pg_start_backup()`/`pg_stop_backup()`. (*راجعه Greg Sabino Mullane، David Christensen. اقترحه Greg Sabino Mullane.*)

  أعاد PostgreSQL 15 تسمية هاتين الدالتين إلى `pg_backup_start()`/`pg_backup_stop()`. تستخدم السجلات والتوثيق الآن أوصافًا لا تعتمد على إصدار PostgreSQL.

  طلب الدمج [#1901](https://github.com/pgbackrest/pgbackrest/pull/1901); الالتزام [`ddd966c`](https://github.com/pgbackrest/pgbackrest/commit/ddd966cadc30440a81100144204d4084a0f2ac3a)

**تحسينات مجموعة الاختبارات:**

- تحديث خيار `--psql-bin` في `test.pl` ليطابق مساعدة سطر الأوامر. (*ساهم به Koshi Shibagaki. راجعه David Steele.*)

  كانت المساعدة تعرض `--psql-bin` لكن اسم الخيار كان `--pgsql-bin`. أصبح اسم الخيار الآن مطابقًا لما يظهر في المساعدة.

  طلب الدمج [#1920](https://github.com/pgbackrest/pgbackrest/pull/1920); الالتزام [`3ad5884`](https://github.com/pgbackrest/pgbackrest/commit/3ad588443b452e04f3abcc107e825dc47e078103)

### ملاحظات إصدار v2.41 {#v241-release-notes}

*التعليقات التوضيحية للنسخ الاحتياطية*

*صدر في 19 سبتمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح استخدام انتهاء صلاحية زمني غير صحيح للمستودعات غير الافتراضية. (*راجعه Stefan Fercot. أبلغ عنه Adam Brusselback.*)

  عند تشغيل `expire` دون `repo`، كانت قيمة `repo-retention-full` الزمنية لكل المستودعات تُقرأ من المستودع ذي الرقم الأدنى. يستخدم كل مستودع الآن قيمته الخاصة.

  المشكلة [#1852](https://github.com/pgbackrest/pgbackrest/issues/1852); طلب الدمج [#1854](https://github.com/pgbackrest/pgbackrest/pull/1854); الالتزام [`eda7f81`](https://github.com/pgbackrest/pgbackrest/commit/eda7f81ee4fd6818ce458768144fc3fc1e1f0f21)
- إصلاح مشكلة عند إدراج الأدلة بشكل عودي مع مرشّح. (*راجعه Stephen Frost. أبلغ عنه Efremov Egor.*)

  كان يمكن لـ `repo-ls` مع `recurse` و`filter` أن يفشل بتحرير مزدوج أو خطأ تجزئة عندما يكون آخر إدخال في دليل دليلًا يحتوي على إدخالات. كانت القائمة الأم تُحرَّر قبل معالجة إدخالات أدلتها الفرعية.

  المشكلة [#1870](https://github.com/pgbackrest/pgbackrest/issues/1870); طلب الدمج [#1871](https://github.com/pgbackrest/pgbackrest/pull/1871); الالتزام [`c39c9f2`](https://github.com/pgbackrest/pgbackrest/commit/c39c9f220ed328b4175d912e109697b726e9ea9b)

**الميزات:**

- تعليقات توضيحية مفتاح/قيمة للنسخ الاحتياطية. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Adam Berlin.*)

  أضف تعليقات مفتاح/قيمة إلى نسخة احتياطية باستخدام الخيار `annotation` للأمر `backup`، ثم أضفها أو عدّلها أو احذفها لاحقًا باستخدام الأمر الجديد `annotate`. يعرض الأمر `info` التعليقات في المخرجات النصية عند تحديد `set`، ويضمّنها دائمًا في مخرجات JSON.

  المشكلة [#1709](https://github.com/pgbackrest/pgbackrest/issues/1709); طلب الدمج [#1724](https://github.com/pgbackrest/pgbackrest/pull/1724); الالتزام [`381fd0a`](https://github.com/pgbackrest/pgbackrest/commit/381fd0a5a4de61624615b150ba98beeafac31f7e)

**التحسينات:**

- دعم `--set` في مخرجات JSON للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Anton Kurochkin.*)

  مع `set`، تتضمن مخرجات JSON من `info` الآن التفاصيل التي كانت تظهر في النص، مثل قائمتي الأخطاء ومساحات الجداول.

  المشكلة [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); طلب الدمج [#1501](https://github.com/pgbackrest/pgbackrest/pull/1501); الالتزام [`db75ffd`](https://github.com/pgbackrest/pgbackrest/commit/db75ffd27037d690a11eb02902f929250fe2bf5b)
- السماح بإعداد حجم قطعة الرفع لمخازن الكائنات. (*راجعه Stefan Fercot. اقترحه Anton Glushakov.*)

  عيّن `repo-storage-upload-chunk-size` لتغيير حجم كل جزء تحميل لـ S3 أو GCS أو Azure. قد تحسن الأجزاء الأكبر الأداء لكنها تستخدم ذاكرة أكثر. لم تتغير القيم الافتراضية.

  [`ff1188f`](https://github.com/pgbackrest/pgbackrest/commit/ff1188f92dfc9e8f6d4aeca8b71a9886f24f58b4) السماح بوسم quote في مساعدة سطر الأوامر.

  [`b05d31f`](https://github.com/pgbackrest/pgbackrest/commit/b05d31f531b55b747175cf94c963f95574c54d2b) إتاحة ضبط حجم جزء التحميل لمخازن الكائنات.; المشكلة [#1843](https://github.com/pgbackrest/pgbackrest/issues/1843); طلب الدمج [#1847](https://github.com/pgbackrest/pgbackrest/pull/1847)
- تحديث الطوابع الزمنية لملف archive.info بعد نسخة احتياطية ناجحة. (*راجعه Stefan Fercot. اقترحه Alex Richman.*)

  لم يكن `archive.info` ونسخته يُكتبان إلا بواسطة `stanza-create` و`stanza-upgrade`، وكان يمكن لسياسة دورة حياة تخزين الكائنات التي تحذف الملفات القديمة أن تزيلهما. تُحدَّث طوابعهما الزمنية الآن بعد كل نسخ احتياطي ناجح.

  المشكلة [#1853](https://github.com/pgbackrest/pgbackrest/issues/1853); طلب الدمج [#1855](https://github.com/pgbackrest/pgbackrest/pull/1855); الالتزام [`3b5df1e`](https://github.com/pgbackrest/pgbackrest/commit/3b5df1e089234d425dd225f8c1976755dc947c8a)
- نقل فحص الخط الزمني لخادم الاستعداد إلى ما بعد نقطة التحقق. (*راجعه Stefan Fercot. اختبره Keith Fiske. اقترحه Keith Fiske.*)

  كان فحص وجود الخادم الاحتياطي على الخط الزمني المتوقع يستخدم `pg_control` كما كان قبل بدء النسخ الاحتياطي. مباشرةً بعد الترقية، قد لا يكون الاحتياطي قد كتب الخط الجديد إلى `pg_control` بعد، فتفشل النسخة بالرسالة "standby is on timeline ... but expected ...". يُجرى الفحص الآن بعد نقطة التحقق.

  المشكلة [#1816](https://github.com/pgbackrest/pgbackrest/issues/1816); طلب الدمج [#1819](https://github.com/pgbackrest/pgbackrest/pull/1819); الالتزام [`c267ba5`](https://github.com/pgbackrest/pgbackrest/commit/c267ba51b1778b5872f4ee928a9614545d743f3f)
- تحسين رسالة التحذير عند استئناف النسخ الاحتياطي. (*اقترحه Cynthia Shang.*)

  كان التحذير يوحي بأن المستخدم يحتاج إلى اتخاذ إجراء. يوضح الآن أن الملفات غير الصالحة ستُحذف ثم يُستأنف النسخ الاحتياطي.

  الالتزام [`cbbe93f`](https://github.com/pgbackrest/pgbackrest/commit/cbbe93f592d8097393c5ffe214f0a8c5fb0549c1)

**تحسينات التوثيق:**

- إضافة المسار المطلق للأمر `kill` في `pgbackrest.service`. (*اقترحه Don Seiler.*)

  يستخدم مثال `pgbackrest.service` الآن `/bin/kill` في `ExecReload`. تتطلب إصدارات systemd القديمة مسارًا مطلقًا.

  الالتزام [`e9ff524`](https://github.com/pgbackrest/pgbackrest/commit/e9ff5248039eedb25da2fee550ec64fcebbc51c7)

### ملاحظات إصدار v2.40 {#v240-release-notes}

*دعم OpenSSL 3*

*صدر في 18 يوليو 2022*

**ملاحظة لمعدّي الحزم**: أُضيف بناء تجريبي بـ meson لكن على معدّي الحزم الاستمرار في استخدام بناء autoconf/make للمستقبل المنظور.

**التحسينات:**

- دعم OpenSSL 3. (*راجعه Stephen Frost.*)

  أصبح pgBackRest يُبنى مع OpenSSL 3. تُكتم تحذيرات الإهمال، وتُكتشف نهاية الملف غير المتوقعة باستخدام رموز الأخطاء التي يُبلغ عنها OpenSSL 3.

  طلب الدمج [#1767](https://github.com/pgbackrest/pgbackrest/pull/1767); الالتزام [`08242ee`](https://github.com/pgbackrest/pgbackrest/commit/08242ee6ac93b9eb9c05cc39e3db15bbafb9052c)
- إنشاء لقطة عند إدراج محتويات مسار. (*راجعه John Morris، Stephen Frost.*)

  كان المسار المُدرج دون ترتيب يُقرأ أثناء معالجة إدخالاته. عند حذف ملفات أثناء الإدراج، كانت بعض أنظمة الملفات تتجاوز ملفات ما زالت موجودة، ويتعذر حذف المسار. تستخدم عمليات الإدراج الآن دائمًا لقطة لمحتويات المسار.

  [`61ca9b5`](https://github.com/pgbackrest/pgbackrest/commit/61ca9b58a000aa8789ef3267682519bdb15e8a6b) استبدال hrnStorageInfoListCallback() بـ TEST_STORAGE_LIST() في الاختبارات.

  [`1c0bf0b`](https://github.com/pgbackrest/pgbackrest/commit/1c0bf0b15da8c0d15cc639851ff1d1bd05b51d06) إعادة ترتيب فحوصات قيم المستخدم والمجموعة null في البروتوكول البعيد وإضافة اختبارات.

  [`72960bb`](https://github.com/pgbackrest/pgbackrest/commit/72960bbf179b4e8051bd4fc50be57d95159e9e13) إعادة تسمية strTrunc() إلى strTruncIdx() وإضافة strTrunc().

  [`75623d4`](https://github.com/pgbackrest/pgbackrest/commit/75623d4583bfdaccb3a19b935fd04d744b363923) إنشاء لقطة عند إدراج محتويات مسار.; المشكلة [#1754](https://github.com/pgbackrest/pgbackrest/issues/1754); طلب الدمج [#1805](https://github.com/pgbackrest/pgbackrest/pull/1805)
- فرض `target-timeline=current` عندما يكون `type=immediate` للاستعادة. (*راجعه Stephen Frost.*)

  على PostgreSQL >= 12، يكون الخط الزمني المستهدف الافتراضي `latest`، وكان الاسترداد قد يفشل عندما يتعذر الوصول من النسخة إلى أحدث خط في المستودع. لا تغيّر الاستعادة باستخدام `type=immediate` الخطوط الزمنية، ولذلك تضبط الآن الخط المستهدف على `current`.

  طلب الدمج [#1814](https://github.com/pgbackrest/pgbackrest/pull/1814); الالتزام [`364af16`](https://github.com/pgbackrest/pgbackrest/commit/364af1635d40431276cc6fd87d6ddd689b611e09)
- اقتطاع الملفات أثناء `restore` بالدلتا عندما تكون أكبر من المتوقع. (*راجعه Stephen Frost.*)

  كانت استعادة delta تنسخ الملف من المستودع كلما اختلف حجمه عن manifest. يُقتطع الملف الأكبر الآن إلى الحجم في manifest ولا يُنسخ إلا إذا لم يتطابق مجموعه الاختباري. لم تعد الملفات التي أُلحقت بها بيانات فقط، مثل السجلات، تُنسخ.

  طلب الدمج [#1758](https://github.com/pgbackrest/pgbackrest/pull/1758); الالتزام [`7ec51e7`](https://github.com/pgbackrest/pgbackrest/commit/7ec51e7e6279ea576ad3b4b5c2ea1fc389d08ab5)
- تعطيل الحفظ التزايدي للـ manifest عندما يكون `resume=n`. (*ساهم به Reid Thompson. راجعه David Steele.*)

  يُحفظ manifest دوريًا أثناء النسخ الاحتياطي لاستخدامه عند الاستئناف. تُتجاوز هذه الحفظات الآن عندما يكون `resume=n`.

  طلب الدمج [#1760](https://github.com/pgbackrest/pgbackrest/pull/1760); الالتزام [`60d70fa`](https://github.com/pgbackrest/pgbackrest/commit/60d70fa66fc3f709914f40dd088bac1b467001f2)
- تعيين نسبة اكتمال النسخة الاحتياطية إلى الصفر قبل بدء النسخ. (*ساهم به Reid Thompson. راجعه David Steele.*)

  لم يكن تقدم النسخة الاحتياطية الجارية يُعرض حتى نسخ أول ملف. يُضبط الآن على الصفر عند بدء النسخ.

  طلب الدمج [#1759](https://github.com/pgbackrest/pgbackrest/pull/1759); الالتزام [`38ad283`](https://github.com/pgbackrest/pgbackrest/commit/38ad2838d553febae1b7fe0244d942dfaa9cf548)
- استخدام علامة `IsTruncated` في S3 لتحديد استمرار الإدراج. (*راجعه John Morris. اختبره Soulou. اقترحه Christian Montagne.*)

  ترسل إصدارات Scality الحديثة `NextContinuationToken` فارغًا عندما لا تكون القائمة مقتطعة، مما كان يسبب حلقة لا تنتهي. تحدد العلامة `IsTruncated` الآن ما إذا كانت القائمة تستمر، ويُعد غياب الرمز أو فراغه لقائمة مقتطعة خطأً.

  المشكلة [#1748](https://github.com/pgbackrest/pgbackrest/issues/1748); طلب الدمج [#1783](https://github.com/pgbackrest/pgbackrest/pull/1783); الالتزام [`845d82f`](https://github.com/pgbackrest/pgbackrest/commit/845d82f6825d4101e6a465a435ef056ff6ec15a2)

**إصلاحات أخطاء التوثيق:**

- تخطي الخيارات الداخلية في مرجع الإعداد. (*أبلغ عنه Francisco Miguel Biete Banon.*)

  كانت الخيارات الداخلية لبعض الأوامر فقط تُدرج في مرجع الإعداد. لم تتأثر مساعدة سطر الأوامر.

  الالتزام [`2643050`](https://github.com/pgbackrest/pgbackrest/commit/2643050be0dc4b7363c434f58373919bd6fdac68)

**تحسينات التوثيق:**

- إضافة رابط إلى إعداد PostgreSQL في قسم مضيف المستودع. (*راجعه Stefan Fercot. اقترحه Julien Cigar.*)

  طلب الدمج [#1809](https://github.com/pgbackrest/pgbackrest/pull/1809); الالتزام [`74a4ac8`](https://github.com/pgbackrest/pgbackrest/commit/74a4ac801db921f7b11b63b9f927228c6a6af861)

**تحسينات مجموعة الاختبارات:**

- إضافة بناء Meson تجريبي. (*راجعه Eli Schwartz، Sam Bassaly.*)

  يتميز Meson بصياغة أبسط وأداء أفضل من autoconf/make. يُستخدم لتوليد الشيفرة وبنى الاختبار، ويُصدر خطأ لأي بناء غير بناء التصحيح. ينبغي لمعدّي الحزم مواصلة استخدام autoconf/make.

  [`2feaaea`](https://github.com/pgbackrest/pgbackrest/commit/2feaaeaac803d6c0193477b56dbeb622fd991156) إضافة الامتداد .inc إلى ملفات C المضمّنة في ملفات C أخرى.

  [`b8fc20d`](https://github.com/pgbackrest/pgbackrest/commit/b8fc20d5b8e7ca003ff39f29ea6e3ba57653f55c) إضافة بناء تجريبي باستخدام Meson.; طلب الدمج [#1765](https://github.com/pgbackrest/pgbackrest/pull/1765)

  [`665da12`](https://github.com/pgbackrest/pgbackrest/commit/665da12ae7f519077512e60ce3a5ec6c6a9997fd) تحديث تعليق include في meson.build ليكون أكثر عمومية.

  [`9fd85a1`](https://github.com/pgbackrest/pgbackrest/commit/9fd85a104ad56061b028afd9057ce8c1d636d3dd) تعطيل meson لكل البنى باستثناء بنى التصحيح.

  [`59f148b`](https://github.com/pgbackrest/pgbackrest/commit/59f148bf6ea8c090d4d65ce5b135a71501e8ae22) توليد -fmacro-prefix-map لإزالة المسار النسبي من __FILE__.

  [`0eccbc8`](https://github.com/pgbackrest/pgbackrest/commit/0eccbc8bf47073ab8ec1f13fed9865d0bd7c3635) تعمل بنى Meson مع الإصدار 0.45.
- السماح بتمرير أي مسار إلى خيار `--test-path`. (*ساهم به Andrey Sokolov. راجعه David Steele.*)

  طلب الدمج [#1764](https://github.com/pgbackrest/pgbackrest/pull/1764); الالتزام [`29b2a54`](https://github.com/pgbackrest/pgbackrest/commit/29b2a54fcc74457af5c63ffb505c5fbb24bb2ade)
- إصلاح خطأ التجميع عند تعريف `DEBUG_EXEC_TIME` دون `DEBUG`. (*ساهم به Andrey Sokolov. راجعه David Steele.*)

  دون `DEBUG`، كان `ASSERT()` الذي يستخدم وقت البدء يتوسع إلى لا شيء، فيسبب المتغير غير المستخدم خطأ تجميع. يستخدم الفحص الآن `CHECK()`.

  طلب الدمج [#1775](https://github.com/pgbackrest/pgbackrest/pull/1775); الالتزام [`1a00ab1`](https://github.com/pgbackrest/pgbackrest/commit/1a00ab10033e9ac6e6f797627567e8b91e143432)

### ملاحظات إصدار v2.39 {#v239-release-notes}

*التحقق وتجميع الملفات*

*صدر في 16 مايو 2022*

**إصلاحات الأخطاء:**

- إصلاح خطأ مُطلق من `FINALLY()` يسبب حلقة لا نهائية. (*راجعه Stephen Frost.*)

  كان الخطأ المرمى داخل كتلة `FINALLY()` يعيد التنفيذ إلى الكتلة نفسها، حيث يُرجَّح أن يُرمى الخطأ مجددًا فيسبب حلقة لا تنتهي. تُنفَّذ `FINALLY()` الآن مرة واحدة فقط.

  [`9a271e9`](https://github.com/pgbackrest/pgbackrest/commit/9a271e925c6239fbd3577f9827c34940e7e43ae4) إصلاح الحلقة غير المنتهية الناتجة عن خطأ مرمي من FINALLY().; طلب الدمج [#1732](https://github.com/pgbackrest/pgbackrest/pull/1732)

  [`ef4c4ab`](https://github.com/pgbackrest/pgbackrest/commit/ef4c4ab8525f81c9ed22c7e82ed12096e81703c5) استخدام متغير بدلًا من دالة لتتبع حالة FINALLY().; طلب الدمج [#1744](https://github.com/pgbackrest/pgbackrest/pull/1744)
- إصدار خطأ عند جميع إخفاقات القفل عدا احتجاز عملية أخرى للقفل. (*راجعه Reid Thompson. اختبره Geir Råness. أبلغ عنه Geir Råness.*)

  لم يكن `archive-get`/`archive-push` يصدران خطأ عندما يتعذر الحصول على القفل لسبب آخر، مثل الأذونات، ولم تكن العملية غير المتزامنة تبدأ. كان المستخدم يتلقى رسالة فشل عامة دون سجل غير متزامن. تُعد هذه الإخفاقات أخطاء الآن.

  المشكلة [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); طلب الدمج [#1730](https://github.com/pgbackrest/pgbackrest/pull/1730); الالتزام [`9629908`](https://github.com/pgbackrest/pgbackrest/commit/962990869454b15db058f4037dbc0b1b611fc95e)

**الميزات:**

- تجميع ملفات النسخ الاحتياطي لتحسين دعم الملفات الصغيرة. (*راجعه Reid Thompson، Stefan Fercot، Chris Bandy.*)

  يخزن التجميع الملفات الصغيرة معًا في المستودع لتوفير الوقت والمساحة أثناء النسخ الاحتياطي، خصوصًا في مخازن الكائنات حيث يكون إنشاء كل ملف مكلفًا. فعّله باستخدام `repo-bundle` واضبطه بواسطة `repo-bundle-size` و`repo-bundle-limit`. تقرأ الاستعادة الملفات المتجاورة في حزمة بقراءة واحدة.

  [`4d2fef1`](https://github.com/pgbackrest/pgbackrest/commit/4d2fef1c37d357965f0ffb9af0d7489f3be1371b) إزالة اختبار restoreFile() زائد وتحسين التغطية.

  [`5141370`](https://github.com/pgbackrest/pgbackrest/commit/514137040e60e8fff0e7f42f43b493113abae5ff) إضافة المعامل limit إلى ioCopyP().

  [`dca6da8`](https://github.com/pgbackrest/pgbackrest/commit/dca6da86bfe84a0cda004df1140d125db1630c90) تحسين الأمر restore للتعامل مع تجميع الملفات.; المشكلة [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); طلب الدمج [#1683](https://github.com/pgbackrest/pgbackrest/pull/1683)

  [`0054677`](https://github.com/pgbackrest/pgbackrest/commit/0054677147121967889ead7feab0959fb19e39a6) إضافة تسجيل الحزم إلى الأمر backup.

  [`3f66f42`](https://github.com/pgbackrest/pgbackrest/commit/3f66f42ef9605a83c356e4c6eb3ef47bcb12c30d) إعادة تسمية خيارات bundle-* إلى repo-bundle-*.; طلب الدمج [#1694](https://github.com/pgbackrest/pgbackrest/pull/1694)

  [`fe9fd2f`](https://github.com/pgbackrest/pgbackrest/commit/fe9fd2ff2d778b86c0df159aabe7644f18f6479f) تعطيل الخيار repo-hardlink عند تفعيل الخيار repo-bundle.

  [`424008d`](https://github.com/pgbackrest/pgbackrest/commit/424008d293661dfb1a167cfec2697def48057447) السماح بالملفات التي يصبح طولها صفرًا بعد بناء manifest للنسخة الاحتياطية.

  [`f405fc6`](https://github.com/pgbackrest/pgbackrest/commit/f405fc6ae281eebf4d61abb39963a9830fe2fa2f) توثيق تجميع ملفات النسخ الاحتياطية.; طلب الدمج [#1740](https://github.com/pgbackrest/pgbackrest/pull/1740)

  التطوير في [v2.38](#v238-release-notes):

  [`a79034a`](https://github.com/pgbackrest/pgbackrest/commit/a79034ae2f6a8ec66b84c62ab6cd4042d2c1a249) إضافة قراءة نطاق إلى جميع مشغّلات التخزين.; طلب الدمج [#1619](https://github.com/pgbackrest/pgbackrest/pull/1619)

  [`b791f1c`](https://github.com/pgbackrest/pgbackrest/commit/b791f1c82f53fa16866837d4544b58243c682f7f) تنفيذ استعادة الملكية دون تحديث البنى الداخلية لـ manifest.

  [`f84909f`](https://github.com/pgbackrest/pgbackrest/commit/f84909f85f7dfb202ac812c67665cc590a5acad4) إصلاح معالجة إزاحة قراءة Posix بعد حدوث خطأ.

  [`4ca0590`](https://github.com/pgbackrest/pgbackrest/commit/4ca0590a51a665535fbba903b8f55e10557b606a) إعادة تنظيم backupProcessQueue() لاستخدام البنية BackupJobData.

  [`16559d9`](https://github.com/pgbackrest/pgbackrest/commit/16559d9e421c66596d21b047c8afe1b2c96ccd82) استخدام الثابت PG_FILE_POSTMTRPID حيثما يناسب.

  [`8c062e1`](https://github.com/pgbackrest/pgbackrest/commit/8c062e1af824c3dc80ff94b3df8d433f95e88d0f) إزالة العلامة primary من manifest.; طلب الدمج [#1630](https://github.com/pgbackrest/pgbackrest/pull/1630)

  [`b0db4b8`](https://github.com/pgbackrest/pgbackrest/commit/b0db4b8ff00db913cb69308017a56155d6070830) تبسيط صلاحيات المسار الأساسي في اختبارات التكامل mock/all.

  [`4a73a02`](https://github.com/pgbackrest/pgbackrest/commit/4a73a0286387f3f2185f3f193f9c20ed0d7d926d) تبسيط القيم الافتراضية لـ manifest.; طلب الدمج [#1631](https://github.com/pgbackrest/pgbackrest/pull/1631)

  [`575ae77`](https://github.com/pgbackrest/pgbackrest/commit/575ae77c0dee12b932469d479b2e45dbaf389737) استبدال varNewUInt64() بـ VARUINT64() حيثما أمكن في manifest.

  [`61ce586`](https://github.com/pgbackrest/pgbackrest/commit/61ce58692f3092b72833b6e9ee87037f45b3b702) حزم بُنى ملفات manifest لتوفير الذاكرة.; طلب الدمج [#1626](https://github.com/pgbackrest/pgbackrest/pull/1626)

  [`ca13f11`](https://github.com/pgbackrest/pgbackrest/commit/ca13f11b4a3858587c7055b0b2b4a8b396dd8451) تحسين jsonFromStrInternal().

  [`e4df5b7`](https://github.com/pgbackrest/pgbackrest/commit/e4df5b7d3846134832b9315e22786f679d63a46b) تبسيط القيم الافتراضية لملفات manifest.; طلب الدمج [#1632](https://github.com/pgbackrest/pgbackrest/pull/1632)

  [`7dd657b`](https://github.com/pgbackrest/pgbackrest/commit/7dd657b7dd163ded9fbf7caef37eea7e08bc5a37) تبسيط إنشاء أسماء الملفات في الوحدة command/verify.

  [`34d6495`](https://github.com/pgbackrest/pgbackrest/commit/34d649579eb3bd1530aa99f0ed1879e7d3125424) تجميع الملفات في حزم داخل المستودع أثناء النسخ الاحتياطي.; المشكلة [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); طلب الدمج [#1655](https://github.com/pgbackrest/pgbackrest/pull/1655)

  [`efc09db`](https://github.com/pgbackrest/pgbackrest/commit/efc09db7b9ece6e7b7f92538d56d6ab7b9798f8f) تقييد الملفات التي يمكن تجميعها في حزم.; المشكلة [#1149](https://github.com/pgbackrest/pgbackrest/issues/1149); طلب الدمج [#1662](https://github.com/pgbackrest/pgbackrest/pull/1662)

  [`e6e1122`](https://github.com/pgbackrest/pgbackrest/commit/e6e1122dbcf5e667d683295f7e7e45de4bbf56bd) تمرير الملف بالمرجع في manifestFileAdd().
- أمر verify للتحقق من صحة محتويات مستودع. (*ساهم به Cynthia Shang، Reid Thompson. راجعه David Steele، Stefan Fercot.*)

  يتحقق الأمر `verify` من صلاحية النسخ الاحتياطية وملفات WAL في المستودع. عيّن `output=text` لطباعة النتائج و`verbose` لتضمين ما جرى التحقق منه بنجاح إلى جانب الأخطاء.

  طلب الدمج [#1607](https://github.com/pgbackrest/pgbackrest/pull/1607); الالتزام [`65d22e4`](https://github.com/pgbackrest/pgbackrest/commit/65d22e43257d46ff6523ffbdb3af59e30deeaea5)
- دعم PostgreSQL 15. (*راجعه Stefan Fercot.*)

  يزيل PostgreSQL 15 النسخ الاحتياطي الحصري، ويعيد تسمية دالتي بدء النسخ وإيقافه، ويحذف `pg_database.datlastsysoid` الذي لم يعد pgBackRest يستخدمه.

  [`692fe49`](https://github.com/pgbackrest/pgbackrest/commit/692fe496bdb5fa6dcffeb9f85b6188ceb1df707a) إزالة الاعتماد على pg_database.datlastsysoid.; طلب الدمج [#1735](https://github.com/pgbackrest/pgbackrest/pull/1735)

  [`20782c8`](https://github.com/pgbackrest/pgbackrest/commit/20782c88bc8d0842d547bd5f4fecdb292e69d1f7) دعم PostgreSQL 15.; طلب الدمج [#1736](https://github.com/pgbackrest/pgbackrest/pull/1736)
- إظهار نسبة اكتمال النسخة الاحتياطية في مخرجات `info`. (*ساهم به Reid Thompson. راجعه David Steele.*)

  يعرض `info` النسبة المئوية لاكتمال النسخة الاحتياطية الجارية على المضيف الذي يجري عليه النسخ. تعرضها مخرجات JSON كعدد صحيح يمثل النسبة مضروبة في 100.

  [`d9088b2`](https://github.com/pgbackrest/pgbackrest/commit/d9088b2e2b16a89d29b967187a547976f96061fc) عرض النسبة المئوية لاكتمال النسخ الاحتياطي في مخرجات info.; المشكلة [#1490](https://github.com/pgbackrest/pgbackrest/issues/1490); طلب الدمج [#1621](https://github.com/pgbackrest/pgbackrest/pull/1621)

  [`a6b1adb`](https://github.com/pgbackrest/pgbackrest/commit/a6b1adb5fd533b4b9aca29646c8acf647d872959) إزالة محرف سطر جديد زائد عند كتابة ملف القفل.

  التطوير في [v2.38](#v238-release-notes):

  [`22734eb`](https://github.com/pgbackrest/pgbackrest/commit/22734eb376b3183924cb7794f9111c1eeb5d92d6) إضافة ioBufferReadNewOpen() وioBufferWriteNewOpen().

  [`9b2f10d`](https://github.com/pgbackrest/pgbackrest/commit/9b2f10dbb49a8b869cef2c419d9957ed4c550016) إعادة تنظيم شيفرة الأقفال.; طلب الدمج [#1643](https://github.com/pgbackrest/pgbackrest/pull/1643)
- الاختيار التلقائي للنسخة الاحتياطية للأمر `restore` مع `--type=lsn`. (*ساهم به Reid Thompson. راجعه Stefan Fercot، David Steele.*)

  عند استخدام `type=lsn`، تختار الاستعادة الآن أحدث نسخة احتياطية انتهت عند LSN المحدد في `target` أو قبله.

  [`08d9e26`](https://github.com/pgbackrest/pgbackrest/commit/08d9e269c6f03e7797584e90c53eb0743b787f60) إعادة تنظيم فحص نوع الهدف في الوحدة restore لزيادة الوضوح.

  [`d8d4132`](https://github.com/pgbackrest/pgbackrest/commit/d8d4132118edd7f93a5b221478c85c2d213c39dd) اختيار النسخة الاحتياطية تلقائيًا للأمر restore مع --type=lsn.; طلب الدمج [#1706](https://github.com/pgbackrest/pgbackrest/pull/1706)

  [`ea4d73f`](https://github.com/pgbackrest/pgbackrest/commit/ea4d73f375558c237fce696f20c19d1efef00bc1) تصحيح ترتيب الحقل backup-lsn-stop في اختبار الوحدة command/restore.
- كتم تحذير WAL الموجود مسبقًا عندما يكون `archive-mode-check` معطلًا. (*ساهم به Reid Thompson. راجعه David Steele.*)

  مع `archive-mode-check=n` وإرسال WAL من عدة مضيفين، يكون وجود ملف WAL في الأرشيف بالمجموع الاختباري نفسه متوقعًا ولم يعد يسجّل تحذيرًا. يظل اختلاف المجموع الاختباري خطأً.

  طلب الدمج [#1711](https://github.com/pgbackrest/pgbackrest/pull/1711); الالتزام [`aad7171`](https://github.com/pgbackrest/pgbackrest/commit/aad7171940afdb221a03825bee6eb2f1827289f1)
- إضافة دعم AWS IMDSv2. (*ساهم به Nuno Pires. راجعه David Steele.*)

  يحمي IMDSv2 بيانات المثيل الوصفية التي توفر بيانات الاعتماد لـ `repo-s3-key-type=auto`. يعود pgBackRest إلى IMDSv1 عندما يفشل طلب رمز IMDSv2.

  المشكلة [#1685](https://github.com/pgbackrest/pgbackrest/issues/1685); طلب الدمج [#1691](https://github.com/pgbackrest/pgbackrest/pull/1691); الالتزام [`21cef09`](https://github.com/pgbackrest/pgbackrest/commit/21cef09dfd03c313531dc66ba9556164ae2835ab)

**التحسينات:**

- السماح بتغيير خيار `repo-hardlink` بعد نسخة احتياطية كاملة. (*راجعه Reid Thompson.*)

  كان تغيير `repo-hardlink` يتطلب نسخة احتياطية كاملة جديدة. يمكن تغييره الآن في أي وقت، مثل تعطيله لتجميع الملفات.

  طلب الدمج [#1699](https://github.com/pgbackrest/pgbackrest/pull/1699); الالتزام [`7afaac0`](https://github.com/pgbackrest/pgbackrest/commit/7afaac0a3d0e43e5598d1abf548559dbe6329363)
- زيادة دقة تسجيل نسبة الاكتمال للأمرين `backup` و`restore`. (*ساهم به Reid Thompson. راجعه David Steele.*)

  تُسجَّل النسبة المئوية للاكتمال الآن حتى منزلتين عشريتين، مما يوفر تحديثات أكثر تكرارًا للنسخ الاحتياطية وعمليات الاستعادة الكبيرة.

  طلب الدمج [#1679](https://github.com/pgbackrest/pgbackrest/pull/1679); الالتزام [`330e199`](https://github.com/pgbackrest/pgbackrest/commit/330e19900ee3415d920680cf6e6856bf5e8e9a69)
- تحسين التحقق من المسارات لأوامر `repo-*`. (*ساهم به Reid Thompson. راجعه David Steele.*)

  لا يجوز أن يحتوي المسار على `//`، وتُزال `/` النهائية، ويجب أن يقع المسار المطلق داخل مسار المستودع.

  [`5ae84d5`](https://github.com/pgbackrest/pgbackrest/commit/5ae84d5e474e95dcc00c174aa5111815a5a70ba5) تحسين التحقق من المسارات لأوامر repo-*.; طلب الدمج [#1697](https://github.com/pgbackrest/pgbackrest/pull/1697)

  [`19dd015`](https://github.com/pgbackrest/pgbackrest/commit/19dd015d589ed3efd31a2a238249a150fb3748c1) إصلاح مشكلات في التحقق المحسن من المسارات لأوامر repo-*.; طلب الدمج [#1751](https://github.com/pgbackrest/pgbackrest/pull/1751)
- تحسين الأمر `stop` ليأخذ خيار `stanza` في الحسبان. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه ragaoua.*)

  ينهي `stop` مع `force` و`stanza` الآن العمليات التي تحتفظ بأقفال لذلك المقطع stanza فقط. كان ينهي سابقًا عمليات جميع مقاطع stanza.

  المشكلة [#1608](https://github.com/pgbackrest/pgbackrest/issues/1608); طلب الدمج [#1676](https://github.com/pgbackrest/pgbackrest/pull/1676); الالتزام [`f7ab002`](https://github.com/pgbackrest/pgbackrest/commit/f7ab002aa74dd2ca277123f7500018ae68a04c74)
- تحسين رسالة الخطأ لمفتاح `repo-azure-key` غير الصالح. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Seth Daniel.*)

  مع `repo-azure-key-type=shared`، يُفحص `repo-azure-key` الآن للتأكد من أنه base64 صالح.

  المشكلة [#1686](https://github.com/pgbackrest/pgbackrest/issues/1686); طلب الدمج [#1688](https://github.com/pgbackrest/pgbackrest/pull/1688); الالتزام [`7c9208b`](https://github.com/pgbackrest/pgbackrest/commit/7c9208ba856a71833dc7d8f1cf8cb2b4bb4b7414)
- إضافة تلميح لفحص السجل عند خطأ غير متزامن في `archive-get`/`archive-push`. (*راجعه Reid Thompson.*)

  عندما تعجز العملية غير المتزامنة عن كتابة ملفات حالتها، تنتهي مهلة `archive-get`/`archive-push` بخطأ عام. يتضمن الخطأ الآن تلميحًا بمسار السجل غير المتزامن الذي يحتوي على الخطأ الفعلي.

  المشكلة [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); الالتزام [`03c71aa`](https://github.com/pgbackrest/pgbackrest/commit/03c71aa606bc0dc89303b3907e7fcbd83ace79d6)
- إضافة `ClockError` لانحراف الساعة غير المتوقع وتغييرات المنطقة الزمنية. (*راجعه Greg Sabino Mullane، Stefan Fercot. اقترحه Greg Sabino Mullane.*)

  طلب الدمج [#1739](https://github.com/pgbackrest/pgbackrest/pull/1739); الالتزام [`5f8c9cd`](https://github.com/pgbackrest/pgbackrest/commit/5f8c9cd66a1b39a47acaddfbc3cf443ae8057519)
- تجريد الامتدادات من الـ manifest التاريخي قبل عرضه في رسالة الخطأ. (*راجعه Stefan Fercot.*)

  عندما لم يكن وسم النسخة الجديدة أحدث من آخر وسم في تاريخ النسخ، كان الخطأ يعرض اسم ملف manifest التاريخي، مثل `20220504-222042F_20220504-222141I.manifest.gz`. يعرض الآن الوسم فقط.

  طلب الدمج [#1738](https://github.com/pgbackrest/pgbackrest/pull/1738); الالتزام [`b6bfd9f`](https://github.com/pgbackrest/pgbackrest/commit/b6bfd9f99d74b1f5e631cf6462b68342589d2b80)
- إضافة user:group إلى خطأ أذونات القفل. (*راجعه Reid Thompson.*)

  المشكلة [#1722](https://github.com/pgbackrest/pgbackrest/issues/1722); الالتزام [`0055fa4`](https://github.com/pgbackrest/pgbackrest/commit/0055fa40fee2636fed88699f52e9e67cd2803f71)
- إضافة تلميح عند تعذر العثور على العنقود الأساسي.

  يتضمن الخطأ "unable to find primary cluster" الآن تلميحًا يسأل عما إذا كانت جميع العناقيد المتاحة في وضع الاسترداد.

  الالتزام [`46b7b72`](https://github.com/pgbackrest/pgbackrest/commit/46b7b7287446d0bb5ed0963fd01c51fb2b08893f)

**إصلاحات أخطاء التوثيق:**

- إصلاح إشارة غير صحيحة إلى `stanza-update` في دليل المستخدم. (*أصلحه Abubakar Mohammed. راجعه David Steele.*)

  الالتزام [`3dd7960`](https://github.com/pgbackrest/pgbackrest/commit/3dd796045160c4d4dbf70ec2800ad483867629f1)
- إصلاح مثال خيار `repo-gcs-key-type` في مرجع الإعداد. (*راجعه Reid Thompson.*)

  كان المثال يستخدم `none` وهي قيمة غير صالحة. أصبح الآن `auto`.

  الالتزام [`166039c`](https://github.com/pgbackrest/pgbackrest/commit/166039c0da1875581a08d41ab8a44adf95fa6db1)
- إصلاح مثال `tls-server-auth` وإضافة توضيحات. (*راجعه Reid Thompson.*)

  كان المثال يفتقد CN العميل، وأصبح الآن `client-cn=stanza1`. وتوضح المساعدة أيضًا أن أحرف البدل غير مسموحة في CN العميل.

  الالتزام [`c222ce1`](https://github.com/pgbackrest/pgbackrest/commit/c222ce1a5f6f813188b7e87a3838d6dce656e0ff)

**تحسينات التوثيق:**

- تبسيط الرسائل حول الإصدارات المدعومة في التوثيق. (*راجعه Stefan Fercot، Reid Thompson، Greg Sabino Mullane.*)

  كانت أدلة المستخدم تسرد نطاقات إصدارات PostgreSQL، مما يوحي بأن الإصدارات الأخرى غير مدعومة، مثل PostgreSQL 12 على RHEL. أُزيلت النطاقات وتشرح المقدمة الآن الإصدارات التي تغطيها الأدلة.

  طلب الدمج [#1742](https://github.com/pgbackrest/pgbackrest/pull/1742); الالتزام [`eefa0b1`](https://github.com/pgbackrest/pgbackrest/commit/eefa0b161a6a02b7843e18455443a4bce41cd4b9)
- إضافة أوصاف أنواع الخيارات. (*ساهم به Reid Thompson. راجعه David Steele.*)

  يصف مرجع الإعداد الآن كل نوع من الخيارات، مثل وحدات خيارات الحجم، بدلًا من تكرار الوصف لكل خيار.

  طلب الدمج [#1747](https://github.com/pgbackrest/pgbackrest/pull/1747); الالتزام [`a913113`](https://github.com/pgbackrest/pgbackrest/commit/a913113fda5886ffd2ff136cdd52a3f469eca026)
- إضافة أسئلة شائعة حول أنواع النسخ الاحتياطي وسرعة الاستعادة. (*ساهم به David Christensen. راجعه Reid Thompson.*)

  يوضح سؤال شائع جديد أن نوع النسخة الاحتياطية يؤثر في النسخ الاحتياطي فقط، لا في سرعة الاستعادة.

  طلب الدمج [#1731](https://github.com/pgbackrest/pgbackrest/pull/1731); الالتزام [`50d409a`](https://github.com/pgbackrest/pgbackrest/commit/50d409a812be577f2c296f3d6096cf97fab049ff)
- توثيق الفرع الأساسي المطلوب لطلبات الدمج. (*ساهم به David Christensen. راجعه Reid Thompson.*)

  ينص دليل المساهمة الآن على وجوب أن تستند طلبات الدمج إلى الفرع `integration`.

  طلب الدمج [#1733](https://github.com/pgbackrest/pgbackrest/pull/1733); الالتزام [`cc5b061`](https://github.com/pgbackrest/pgbackrest/commit/cc5b0614894e1b5ef78f1ceba3bc8e4760a40a24)

### ملاحظات إصدار v2.38 {#v238-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 6 مارس 2022*

**ملاحظة هامة**: حجم المستودع الذي يبلّغ عنه الأمر `info` يعتمد الآن بالكامل على ما كتبه pgBackRest في التخزين. سابقًا، في حالات معينة، كان بإمكان pgBackRest اكتشاف ما إذا كان التخزين يطبّق ضغطًا إضافيًا لكن هذا لم يعد مدعومًا.

**إصلاحات الأخطاء:**

- إعادة محاولة الأخطاء في الحذف الدفعي للملفات في S3. (*راجعه Reid Thompson. أبلغ عنه Alex Richman.*)

  كانت إعادة المحاولة تشمل الحذف الدفعي الفاشل، لكنها لا تشمل أخطاء الملفات المنفردة داخل الدفعة، وقد ينتهي pgBackRest أثناء التنظيف أو حذف نسخة لا يمكن استئنافها. تُحذف الآن الملفات التي تفشل ضمن دفعة بشكل منفرد مع إعادات محاولة HTTP المعتادة.

  المشكلة [#1650](https://github.com/pgbackrest/pgbackrest/issues/1650); طلب الدمج [#1653](https://github.com/pgbackrest/pgbackrest/pull/1653); الالتزام [`551e5bc`](https://github.com/pgbackrest/pgbackrest/commit/551e5bc6f67c91cf1e11da0cefe24f9650353adc)
- السماح بمطابقة غير حساسة لحالة الأحرف لقيم ترويسة `connection` في HTTP. (*راجعه Reid Thompson. أبلغ عنه Rémi Vidier.*)

  تسمح مواصفة HTTP بقيم ترويسة `connection` بأي حالة أحرف، مثل `Close`.

  المشكلة [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); طلب الدمج [#1675](https://github.com/pgbackrest/pgbackrest/pull/1675); الالتزام [`b33cabe`](https://github.com/pgbackrest/pgbackrest/commit/b33cabe08c33e29eb8aef65dd46b2c1f3cf2d186)

**الميزات:**

- إضافة دعم التشفير من جانب الخادم في AWS S3 باستخدام KMS. (*ساهم به Christoph Berg. راجعه David Steele. اختبره Tharindu Amila.*)

  عيّن `repo-s3-kms-key-id` لتشفير الكائنات بمفتاح تديره AWS KMS.

  المشكلة [#1430](https://github.com/pgbackrest/pgbackrest/issues/1430); طلب الدمج [#1567](https://github.com/pgbackrest/pgbackrest/pull/1567); الالتزام [`3097acd`](https://github.com/pgbackrest/pgbackrest/commit/3097acd73a21b630aa5352be57a82b031930f96b)
- إضافة خيار `archive-missing-retry`. (*راجعه Stefan Fercot.*)

  يعيد `archive-get` افتراضيًا محاولة جلب مقطع WAL سبق أن أبلغ عن فقدانه، متجاهلًا إشعارات الفقد التي تركتها استعادة سابقة في مسار spool. مع `archive-missing-retry=n`، يستطيع PostgreSQL اكتشاف نهاية الأرشيف والتحول إلى البث حتى أثناء استمرار أرشفة WAL. ويجب عندئذ أن يكون مسار spool فارغًا عند بدء الاسترداد.

  طلب الدمج [#1642](https://github.com/pgbackrest/pgbackrest/pull/1642); الالتزام [`10038db`](https://github.com/pgbackrest/pgbackrest/commit/10038db9c9f2b4753c3821e0b246fa8626527184)
- إضافة مرشّح نوع النسخة الاحتياطية إلى الأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  عيّن `type` لعرض النسخ من ذلك النوع فقط، مثل `type=full`.

  المشكلة [#600](https://github.com/pgbackrest/pgbackrest/issues/600); طلب الدمج [#1651](https://github.com/pgbackrest/pgbackrest/pull/1651); الالتزام [`b26097f`](https://github.com/pgbackrest/pgbackrest/commit/b26097f8d8a7e2af6e9a21576994cbb47110c6f4)

**التحسينات:**

- إعادة المحاولة عند فشل التحقق من الصفحات أثناء `backup`. (*راجعه Stephen Frost، David Christensen.*)

  تُقرأ الآن الصفحة التي تفشل في فحص المجموع الاختباري مرة أخرى. لا يُبلَّغ عنها كخطأ إلا إذا لم تتغير. الصفحة المتغيرة يكتبها PostgreSQL، ويحتوي WAL على صورة كاملة لها. وتُفحص الصفحات الصفرية الآن للتأكد من أن جميع بايتاتها أصفار، لا الحقل `pd_upper` وحده.

  [`b489707`](https://github.com/pgbackrest/pgbackrest/commit/b4897077937ee4571ba719276a44d5db0a75510e) نقل اختبارات command/backup-common في الوحدة command/backup.

  [`9eec98c`](https://github.com/pgbackrest/pgbackrest/commit/9eec98c61302121134d2067326dbd2cd0f2f0b9c) إعادة المحاولة عند فشل التحقق من المجموع الاختباري للصفحة أثناء النسخ الاحتياطي.; المشكلة [#952](https://github.com/pgbackrest/pgbackrest/issues/952); طلب الدمج [#1667](https://github.com/pgbackrest/pgbackrest/pull/1667)

  [`53f1b25`](https://github.com/pgbackrest/pgbackrest/commit/53f1b2520434221c01caf92e052403a28c455c1b) تحسين التحقق من الصفحات الصفرية.; المشكلة [#952](https://github.com/pgbackrest/pgbackrest/issues/952); طلب الدمج [#1669](https://github.com/pgbackrest/pgbackrest/pull/1669)
- التعامل مع خوادم TLS التي لا تغلق الاتصالات بسلاسة. (*راجعه David Christensen، Stephen Frost. اختبره Rémi Vidier.*)

  تغلق بعض الخوادم المقبس بدلًا من اتصال TLS. عندما لا تتضمن الاستجابة طول محتوى أو ترميزًا مجزّأً ويمكن تحليل محتواها، يُعامل إغلاق المقبس الآن كنهاية ملف. كانت هذه الخوادم قد توقفت عن العمل في v2.35.

  المشكلة [#1638](https://github.com/pgbackrest/pgbackrest/issues/1638); طلب الدمج [#1677](https://github.com/pgbackrest/pgbackrest/pull/1677); الالتزام [`59a5373`](https://github.com/pgbackrest/pgbackrest/commit/59a5373cf85e4ad0057b592bfe855495384dfcbd)
- إضافة قيم LSN للنسخ الاحتياطية إلى مخرجات الأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  يُعرض LSN البداية والنهاية للنسخة الاحتياطية مع `set` وفي مخرجات JSON، لاستخدامهما في الاسترداد إلى نقطة زمنية بناءً على LSN.

  طلب الدمج [#1610](https://github.com/pgbackrest/pgbackrest/pull/1610); الالتزام [`d866dd5`](https://github.com/pgbackrest/pgbackrest/commit/d866dd5c297dc046581134a108032cf9694cae0e)
- تجريد الشرطات المائلة الختامية تلقائيًا لمسارات `repo-ls`. (*ساهم به David Christensen. راجعه David Steele.*)

  كانت الشرطة المائلة النهائية في المسار تجعل `repo-ls` لا يعرض محتوى على بعض أنواع تخزين المستودعات.

  طلب الدمج [#1673](https://github.com/pgbackrest/pgbackrest/pull/1673); الالتزام [`6320712`](https://github.com/pgbackrest/pgbackrest/commit/632071232344a1160ef932d6e0d65eb3149ed226)
- عدم إعادة محاولة الأخطاء القاتلة. (*راجعه Reid Thompson.*)

  قد تسبب إعادة محاولة الأخطاء النهائية، خصوصًا نفاد الذاكرة، حالات تعليق. يُبلَّغ الآن عن أخطاء التحققات التأكيدية والذاكرة دون إعادة محاولة.

  [`8573a2d`](https://github.com/pgbackrest/pgbackrest/commit/8573a2df14d0bfd5578333b68147cc12c93c6f96) تحسين اختبار أخطاء وحدة البروتوكول لـ protocolClientFree().

  [`8d0cce6`](https://github.com/pgbackrest/pgbackrest/commit/8d0cce66f83abc1ff02a985ec3f0d7e285c09d72) استخدام خطأ عادي في اختبار إعادة المحاولات لوحدة البروتوكول.

  [`8046f06`](https://github.com/pgbackrest/pgbackrest/commit/8046f0630715015d5adcced570c54e9a183c0e73) عدم إعادة محاولة الأخطاء النهائية.; طلب الدمج [#1658](https://github.com/pgbackrest/pgbackrest/pull/1658)
- إزالة دعم PostgreSQL `8.3`/`8.4`. (*راجعه Reid Thompson، Stefan Fercot.*)

  لا توجد دلائل على استمرار استخدام هذه الإصدارات، ويستهلك دعمها وقت التطوير والاختبار. استخدم إصدارًا أقدم من pgBackRest للنسخ الاحتياطي لهذه الإصدارات أو الترحيل منها.

  طلب الدمج [#1611](https://github.com/pgbackrest/pgbackrest/pull/1611); الالتزام [`bb4b30d`](https://github.com/pgbackrest/pgbackrest/commit/bb4b30ddd3f80c246c565eb4769efc82b9509648)
- إزالة المنطق الذي كان يحاول تحديد الضغط الإضافي لنظام الملفات. (*راجعه Reid Thompson، Stefan Fercot.*)

  بعد نسخ الملف، كان pgBackRest يفحص حجمه على القرص لاكتشاف ضغط نظام الملفات، مثل ZFS. لم يكن هذا مختبرًا، وكان بطيئًا مع كثرة الملفات الصغيرة ويعيق التجميع. أصبح حجم المستودع في `info` هو ما كتبه pgBackRest.

  طلب الدمج [#1652](https://github.com/pgbackrest/pgbackrest/pull/1652); الالتزام [`cb630ff`](https://github.com/pgbackrest/pgbackrest/commit/cb630ffe3b5c819b5e97ac11d5974000bd44d632)

**إصلاحات أخطاء التوثيق:**

- نقل خيارات `repo` في توثيق TLS إلى القسم `global`. (*أبلغ عنه Anton Kurochkin.*)

  كان دليل المستخدم يضبط هذه الخيارات في قسم stanza، وهو ما يعمل في بعض الحالات لكنه ليس الممارسة الأفضل.

  الالتزام [`53de3e3`](https://github.com/pgbackrest/pgbackrest/commit/53de3e3aeb71f8209f56167941df35bbfcb7cdc9)
- إزالة خيار `backup-standby` غير المستخدم من أوامر الـ stanza. (*أبلغ عنه Stefan Fercot.*)

  كان `stanza-create` و`stanza-upgrade` يسردان `backup-standby` في مرجع الأوامر والمساعدة، لكنهما لا يستخدمانه.

  الالتزام [`5cbb4a3`](https://github.com/pgbackrest/pgbackrest/commit/5cbb4a3e6b13598b90cae46fad28c31604f9f094)
- إصلاح أخطاء إملائية في المساعدة وملاحظات الإصدار. (*أصلحه Daniel Gustafsson. راجعه David Steele.*)

  [`cacfdd9`](https://github.com/pgbackrest/pgbackrest/commit/cacfdd94d74307285b1b590ec0977d7db3142d0d) إصلاح أخطاء مطبعية في المساعدة وملاحظات الإصدار.; طلب الدمج [#1671](https://github.com/pgbackrest/pgbackrest/pull/1671)

  [`5c332a0`](https://github.com/pgbackrest/pgbackrest/commit/5c332a0b100d5a5180b3d95bd90d4d7b521b42db) تصحيح نسب المساهمات في ملاحظات الإصدار للالتزامين cacfdd94 وf798458e.

**تحسينات التوثيق:**

- إضافة فحص الحياة إلى إعداد خدمة systemd. (*اقترحه Yogesh Sharma.*)

  يتحقق مثال `pgbackrest.service` الآن من أن الخادم ما زال يعمل بعد وقت قصير من بدء تشغيله. سابقًا لم يكن الخادم الذي يفشل في البدء يُبلغ عن خطأ بينما يعيد systemd المحاولة في الخلفية.

  الالتزام [`f1bdf3e`](https://github.com/pgbackrest/pgbackrest/commit/f1bdf3e04b07dc9a2eaa1fdbe5278cc18371e868)
- إضافة أسئلة شائعة تشرح لاحقة أرشيف WAL. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  لاحقة ملف WAL في المستودع هي مجموعه الاختباري SHA1 المستخدم للتحقق منه. لا يمكن حذفها.

  المشكلة [#1485](https://github.com/pgbackrest/pgbackrest/issues/1485); المشكلة [#1663](https://github.com/pgbackrest/pgbackrest/issues/1663); طلب الدمج [#1664](https://github.com/pgbackrest/pgbackrest/pull/1664); الالتزام [`98d525d`](https://github.com/pgbackrest/pgbackrest/commit/98d525dba43ba259ff7989746b8e5be3382c189d)
- الإشارة إلى أن خانات النسخ المتماثل لا تُستعاد. (*ساهم به Reid Thompson. راجعه David Steele، Stefan Fercot. اقترحه Christophe Courtois.*)

  المشكلة [#1585](https://github.com/pgbackrest/pgbackrest/issues/1585); طلب الدمج [#1601](https://github.com/pgbackrest/pgbackrest/pull/1601); الالتزام [`a82f017`](https://github.com/pgbackrest/pgbackrest/commit/a82f0179cdd5742e5c5b1e0bdfd23166753fdb38)

### ملاحظات إصدار v2.37 {#v237-release-notes}

*خادم TLS*

*صدر في 3 يناير 2022*

**ملاحظة هامة**: إذا لم يتمكن الأمر `restore` من إيجاد نسخة احتياطية تطابق الهدف الزمني المحدد فسيُطلق خطأ، بينما كان يُسجَّل تحذير سابقًا.

**إصلاحات الأخطاء:**

- إصلاح تعيين روابط دلتا `restore` عندما يكون المسار/الملف موجودًا بالفعل. (*راجعه Reid Thompson. أبلغ عنه Younes Alhroub.*)

  عندما كان `link-map` أو `link-all` يعيّن مسارًا أو ملفًا موجودًا إلى رابط، كانت استعادة delta تترك المسار أو الملف كما هو. يُستبدل الآن بالرابط.

  المشكلة [#1588](https://github.com/pgbackrest/pgbackrest/issues/1588); طلب الدمج [#1589](https://github.com/pgbackrest/pgbackrest/pull/1589); الالتزام [`a73fe4e`](https://github.com/pgbackrest/pgbackrest/commit/a73fe4eb966f9685f6e4179c397a10c1e7f15f19)
- إصلاح تسريب المقابس عند إعادة محاولة الاتصال. (*راجعه Reid Thompson. أبلغ عنه James Coleman.*)

  في البنى المحسنة، لم يكن مقبس محاولة الاتصال الفاشلة يُغلق، وكانت كل إعادة محاولة تسرّب مقبسًا.

  المشكلة [#1593](https://github.com/pgbackrest/pgbackrest/issues/1593); طلب الدمج [#1594](https://github.com/pgbackrest/pgbackrest/pull/1594); الالتزام [`615bdff`](https://github.com/pgbackrest/pgbackrest/commit/615bdff4030a31bfedfe7df04676e3948ec9c2c0)

**الميزات:**

- إضافة خادم TLS. (*راجعه Stephen Frost، Reid Thompson. اختبره Andrew L'Ecuyer.*)

  يبدأ الأمر `server` خادم TLS يمكن استخدامه بدلًا من SSH للوصول إلى مضيفي المستودع وPostgreSQL. عيّن `repo-host-type=tls` أو `pg-host-type=tls` على العميل، واضبط الشهادات وتفويض العملاء باستخدام خيارات `tls-server-*`. يعيد `SIGHUP` تحميل الإعداد، ويوقف `SIGTERM` الخادم.

  [`2d963ce`](https://github.com/pgbackrest/pgbackrest/commit/2d963ce9471808172f879916c3f3accc35f14d56) إعادة تسمية الأمر server-start إلى server.

  [`7b3ea88`](https://github.com/pgbackrest/pgbackrest/commit/7b3ea883c7c010aafbeb14d150d073a113b703e4) إضافة معالجة SIGTERM وSIGHUP إلى خادم TLS.; طلب الدمج [#1572](https://github.com/pgbackrest/pgbackrest/pull/1572)

  [`f06101d`](https://github.com/pgbackrest/pgbackrest/commit/f06101de77a980c7e4115762f2fc301280aa4127) إضافة توثيق خادم TLS.; طلب الدمج [#1597](https://github.com/pgbackrest/pgbackrest/pull/1597)

  التطوير في [v2.36](#v236-release-notes):

  [`ccc255d`](https://github.com/pgbackrest/pgbackrest/commit/ccc255d3e05d8ce2b6ac251d1498f71b04098a86) إضافة خادم TLS.; طلب الدمج [#1504](https://github.com/pgbackrest/pgbackrest/pull/1504)

  [`13d4559`](https://github.com/pgbackrest/pgbackrest/commit/13d4559708819787ad05be6f37ec0badb0eccae5) فحص القيمة المعادة من getsockopt().

  التطوير في [v2.35](#v235-release-notes):

  [`947c7a8`](https://github.com/pgbackrest/pgbackrest/commit/947c7a84cb37d09ab925785ca7670c970e32b8a3) إعادة تنظيم cmdLocal()/cmdRemote() لقبول كائن ProtocolServer.

  [`0999de0`](https://github.com/pgbackrest/pgbackrest/commit/0999de0279fabf35af80396a9a8d35546ec02d53) نقل noop من protocolClientNew() إلى تهيئة local/remote.
- إضافة خيار `--cmd`. (*ساهم به Reid Thompson. راجعه Stefan Fercot، David Steele. اقترحه Virgile CREVON.*)

  اضبط `cmd` على ملف pgBackRest التنفيذي المستخدم في الأوامر التي يكتبها pgBackRest، مثل `restore_command` في `recovery.conf`.

  المشكلة [#1537](https://github.com/pgbackrest/pgbackrest/issues/1537); طلب الدمج [#1540](https://github.com/pgbackrest/pgbackrest/pull/1540); الالتزام [`2a57647`](https://github.com/pgbackrest/pgbackrest/commit/2a576477b316238473525e56bc8fc8ea5790455f)

**التحسينات:**

- فحص الأرشيف فور بدء النسخ الاحتياطي. (*راجعه Reid Thompson، David Christensen.*)

  كان النسخ الاحتياطي يفشل بسبب تعطل أرشفة WAL فقط بعد نسخ جميع الملفات. يُفحص الأرشيف الآن مباشرةً بعد بدء النسخ الاحتياطي. وعلى نظام خامل، تُنشأ نقطة استعادة لتبديل مقطع WAL.

  المشكلة [#152](https://github.com/pgbackrest/pgbackrest/issues/152); طلب الدمج [#1570](https://github.com/pgbackrest/pgbackrest/pull/1570); الالتزام [`1f14f45`](https://github.com/pgbackrest/pgbackrest/commit/1f14f45dfb0d1677a695719381cbd5a8a3c6c986)
- إضافة فحوصات الخط الزمني ونقطة التحقق إلى النسخ الاحتياطي. (*راجعه Stefan Fercot، Reid Thompson.*)

  يتحقق النسخ الاحتياطي الآن من أن `pg_control` يحتوي على نقطة التحقق والخط الزمني لبدء النسخ، وأن الاحتياطي يتبع الأساسي، أي أنه على الخط الزمني نفسه ونقطة تحققه ليست أحدث من نقطة تحقق النسخ الاحتياطي.

  طلب الدمج [#1581](https://github.com/pgbackrest/pgbackrest/pull/1581); الالتزام [`49145d7`](https://github.com/pgbackrest/pgbackrest/commit/49145d72bac16498cdbf5eeb3cd6128ea0be0667)
- التحقق من أن العناقيد حية ومُعدّة بشكل صحيح أثناء النسخ الاحتياطي. (*راجعه Stefan Fercot.*)

  يفشل النسخ الاحتياطي الآن فور توقف عنقود أو ترقية الخادم الاحتياطي. سابقًا لم يكن توقف الأساسي يُكتشف إلا في نهاية النسخ، ولم تكن ترقية الاحتياطي تُكتشف.

  طلب الدمج [#1584](https://github.com/pgbackrest/pgbackrest/pull/1584); الالتزام [`bd2ba80`](https://github.com/pgbackrest/pgbackrest/commit/bd2ba802db11c505ec69943fa81b2b379073fbf4)
- إصدار خطأ عندما يعجز `restore` عن إيجاد نسخة احتياطية تطابق الهدف الزمني. (*راجعه Reid Thompson، Douglas J Hunley. اقترحه Douglas J Hunley.*)

  كان هذا تحذيرًا يسهل تفويته، وقد يضيع وقت طويل في استعادة نسخة لا يمكنها بلوغ الهدف.

  المشكلة [#1582](https://github.com/pgbackrest/pgbackrest/issues/1582); طلب الدمج [#1586](https://github.com/pgbackrest/pgbackrest/pull/1586); الالتزام [`be4ac39`](https://github.com/pgbackrest/pgbackrest/commit/be4ac3923cb77873da298a30aca5d847b3c635af)
- تحليل البروتوكول/المنفذ في نقاط نهاية S3/Azure. (*ساهم به Reid Thompson. راجعه David Steele.*)

  يمكن لـ `repo-s3-endpoint` و`repo-azure-endpoint` و`repo-storage-host` الآن تضمين بروتوكول ومنفذ، مثل `https://host:9000`.

  المشكلة [#1560](https://github.com/pgbackrest/pgbackrest/issues/1560); طلب الدمج [#1591](https://github.com/pgbackrest/pgbackrest/pull/1591); الالتزام [`6a12458`](https://github.com/pgbackrest/pgbackrest/commit/6a12458440168f13cb05d70f36ea54b1860e390c)
- إضافة تحذير عندما يتجاوز `checkpoint_timeout` قيمة `db-timeout`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  مع `start-fast=n`، قد تنتهي مهلة النسخ الاحتياطي أثناء انتظار نقطة التحقق عندما يكون `checkpoint_timeout` أكبر من `db-timeout`. يُصدر النسخ الاحتياطي الآن تحذيرًا في هذه الحالة.

  طلب الدمج [#1564](https://github.com/pgbackrest/pgbackrest/pull/1564); الالتزام [`6723305`](https://github.com/pgbackrest/pgbackrest/commit/672330593789f07aaad90bbafcd2597cbc602686)
- إضافة الفعل إلى مخرجات أخطاء HTTP. (*ساهم به Christoph Berg. راجعه David Steele.*)

  طلب الدمج [#1566](https://github.com/pgbackrest/pgbackrest/pull/1566); الالتزام [`c38e2d3`](https://github.com/pgbackrest/pgbackrest/commit/c38e2d31709804eb4b9125a15ad84c8fc813f366)
- السماح بوسائط y/n لخيارات سطر الأوامر المنطقية. (*ساهم به Reid Thompson. راجعه David Steele.*)

  طلب الدمج [#1571](https://github.com/pgbackrest/pgbackrest/pull/1571); الالتزام [`1a0560d`](https://github.com/pgbackrest/pgbackrest/commit/1a0560d363d28737befb8c222647783d4fc2ca29)
- جعل تسجيل حجم النسخة الاحتياطية يطابق مخرجات الأمر `info` تمامًا. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Mahomed Hussein.*)

  يتضمن حجم النسخة الاحتياطية المسجّل الآن الملفات المنسوخة فقط، إضافةً إلى `backup_label` و`tablespace_map`. سابقًا كانت النسخة التزايدية بعد تبديل الأدوار، مثلًا، تسجّل حجم كل ملف جرى فحصه.

  [`6e63576`](https://github.com/pgbackrest/pgbackrest/commit/6e635764a66278d5a8c2b4d30b23063bc3923067) مطابقة حجم النسخة في السجل مع الحجم الذي يُبلغ عنه الأمر info.; المشكلة [#766](https://github.com/pgbackrest/pgbackrest/issues/766); طلب الدمج [#1562](https://github.com/pgbackrest/pgbackrest/pull/1562)

  [`afe77e7`](https://github.com/pgbackrest/pgbackrest/commit/afe77e76e0adf948138d797e227a6f4c7d47c2eb) تحديث اسم المساهم في 6e635764.

  [`1e77fc3`](https://github.com/pgbackrest/pgbackrest/commit/1e77fc3d75490b7a1b6a0b31be9298c995ec672f) تضمين حجمي الملفين backup_label وtablespace_map في مخرجات السجل.; طلب الدمج [#1568](https://github.com/pgbackrest/pgbackrest/pull/1568)

  [`a3d7a23`](https://github.com/pgbackrest/pgbackrest/commit/a3d7a23a9d90611a3d31947598fbea240b250710) استخدام infoBackupDataByLabel() لتسجيل حجم النسخة الاحتياطية.; طلب الدمج [#1573](https://github.com/pgbackrest/pgbackrest/pull/1573)

  [`dcb4f09`](https://github.com/pgbackrest/pgbackrest/commit/dcb4f09d8315e92c0877b589f3fa9b7f0fa65f93) التراجع عن تغييرات backupFilePut() التي أُجريت في 1e77fc3d.

**تحسينات التوثيق:**

- عرض القيمة الافتراضية لخيارات الحجم والقيم المسموح بها بالوحدات المناسبة. (*راجعه Reid Thompson.*)

  [`cff961e`](https://github.com/pgbackrest/pgbackrest/commit/cff961ede7e41fa8035ffe7451a22eb5ea0e46c1) توحيد منطق بناء قوائم القيم عند إخراج الإعداد في موضع مركزي.

  [`038abaa`](https://github.com/pgbackrest/pgbackrest/commit/038abaa71d816cc87b382bd81d3df62ddec9455a) عرض القيم الافتراضية والمسموح بها لخيارات الحجم بوحدات مناسبة.; طلب الدمج [#1557](https://github.com/pgbackrest/pgbackrest/pull/1557)
- إصلاح أخطاء إملائية وتحسين توثيق خيار `tablespace-map-all`. (*راجعه Reid Thompson. اقترحه Reid Thompson.*)

  الالتزام [`df89eff`](https://github.com/pgbackrest/pgbackrest/commit/df89eff429e9b8fbc68d9e9895badf9719fd31d2)
- إزالة عبارة متقادمة حول الدعم المستقبلي للمستودعات المتعددة. (*اقترحه David Christensen.*)

  كان التوثيق يذكر السماح بمستودع واحد فقط، رغم أن المستودعات المتعددة مدعومة منذ v2.33.

  الالتزام [`dea7524`](https://github.com/pgbackrest/pgbackrest/commit/dea752477ab8e812cdbd717eb2091baf3f5d0906)

### ملاحظات إصدار v2.36 {#v236-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 1 نوفمبر 2021*

**إصلاحات الأخطاء:**

- السماح بـ "global" كبادئة لـ stanza. (*راجعه Stefan Fercot. أبلغ عنه Younes Alhroub.*)

  كان اسم stanza الذي يبدأ بـ `global`، مثل `global_stanza`، يُرفض لأن محلل الإعداد يعامله كقسم عام.

  المشكلة [#1524](https://github.com/pgbackrest/pgbackrest/issues/1524); طلب الدمج [#1525](https://github.com/pgbackrest/pgbackrest/pull/1525); الالتزام [`498902e`](https://github.com/pgbackrest/pgbackrest/commit/498902e885c9d7a44648ccc01b20454094d5b742)
- إصلاح خطأ تقسيم عند وجود ملف مفتاح GCS غير صالح. (*راجعه Stephen Frost. أبلغ عنه Henrik Feldt.*)

  كان ملف مفتاح GCS الذي يفتقد بريد العميل الإلكتروني أو المفتاح الخاص أو URI الرمز يسبب خطأ تجزئة. يُصدر الآن خطأً.

  المشكلة [#1536](https://github.com/pgbackrest/pgbackrest/issues/1536); الالتزام [`2cea005`](https://github.com/pgbackrest/pgbackrest/commit/2cea005f740d640290a9948595f5933833e30e7d)

**التحسينات:**

- السماح لخيار `link-map` بإنشاء روابط جديدة. (*راجعه Don Seiler، Stefan Fercot، Chris Bandy. اقترحه Don Seiler.*)

  كان `link-map` يستطيع إعادة تعيين الروابط الموجودة في النسخة الاحتياطية فقط. يمكنه الآن إنشاء رابط جديد لأي مسار أو ملف في النسخة.

  [`d89a677`](https://github.com/pgbackrest/pgbackrest/commit/d89a67776cfbb7b3047dbe297cc0c768e5c670e8) إعادة تنظيم اختبارات restoreManifestMap() في وحدة command/restore.

  [`cf1a575`](https://github.com/pgbackrest/pgbackrest/commit/cf1a57518fe3230886509f59fcec9c9a81e6513c) إعادة تنظيم restoreManifestMap() لتُقاد بواسطة link-map.

  [`68c5f3e`](https://github.com/pgbackrest/pgbackrest/commit/68c5f3eaf18fc9bd10fde15a323890bcdcbf4534) السماح للخيار link-map بإنشاء روابط جديدة.; المشكلة [#1409](https://github.com/pgbackrest/pgbackrest/issues/1409); طلب الدمج [#1520](https://github.com/pgbackrest/pgbackrest/pull/1520)
- زيادة الحد الأقصى للفهرس المسموح به لخياري `pg`/`repo` إلى 256. (*راجعه Cynthia Shang.*)

  كان الحد الأقصى للفهرس 8 لخيارات `pg` و4 لخيارات `repo`. أصبح كلاهما 256، مثل `pg256-path`.

  [`02b06aa`](https://github.com/pgbackrest/pgbackrest/commit/02b06aa4957cf3fe64ceb7a44cc1893bff12fe99) زيادة الحد الأقصى المسموح لفهرس خيارات pg/repo إلى 256.; طلب الدمج [#1481](https://github.com/pgbackrest/pgbackrest/pull/1481)

  [`71047a9`](https://github.com/pgbackrest/pgbackrest/commit/71047a9d6d1eea71b3fbd430983541a54049cc69) استخدام strncpy() لتحديد عدد المحارف المنسوخة إلى optionName.
- إضافة مصادقة `WebIdentity` لـ AWS S3. (*راجعه James Callahan، Reid Thompson، Andrew L'Ecuyer. اختبره Benjamin Blattberg.*)

  عيّن `repo-s3-key-type=web-id` للحصول على بيانات الاعتماد تلقائيًا في بيئة EKS.

  [`cfd8233`](https://github.com/pgbackrest/pgbackrest/commit/cfd823355af2ac99f30c5e1393a121c6dbf622b7) إعادة تنظيم مشغّل تخزين S3 لدعم أساليب مصادقة إضافية.

  [`3879bc6`](https://github.com/pgbackrest/pgbackrest/commit/3879bc69b888daa04d2ca98a2d1219cf22519ddc) إضافة مصادقة WebIdentity لـ AWS S3.; المشكلة [#1203](https://github.com/pgbackrest/pgbackrest/issues/1203); طلب الدمج [#1527](https://github.com/pgbackrest/pgbackrest/pull/1527)

  [`1152f7a`](https://github.com/pgbackrest/pgbackrest/commit/1152f7a7d64e69eed1d9e74b48a308f6c742c28a) تصحيح معاملات غير متطابقة في استدعاء tlsClientNew().
- إضافة الخيار `repo-azure-uri-style`.

  عيّن `repo-azure-uri-style` إلى `host` (الافتراضي) أو `path` لاختيار نمط URI لـ Azure. يستخدم Azurite عناوين بنمط المضيف عندما تبدو نقطة النهاية كاسم مضيف متعدد الأجزاء.

  الالتزام [`096829b`](https://github.com/pgbackrest/pgbackrest/commit/096829b3b257444162417662612e80d8cb2ac6ec)
- الإبلاغ عن أخطاء التحقق من ملفات النسخة الاحتياطية في `backup.info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

  كانت الأخطاء المكتشفة أثناء النسخ الاحتياطي، مثل المجاميع الاختبارية غير الصالحة للصفحات، لا تظهر إلا بواسطة `info` مع `set`. تُظهر الآن علامة في `backup.info` في المخرجات النصية وJSON أن النسخة تحتوي على أخطاء. ولا تزال التفاصيل تتطلب `set`.

  المشكلة [#1484](https://github.com/pgbackrest/pgbackrest/issues/1484); طلب الدمج [#1508](https://github.com/pgbackrest/pgbackrest/pull/1508); الالتزام [`34f7873`](https://github.com/pgbackrest/pgbackrest/commit/34f78734325743b4e34cb39224852e6debf49750)
- إضافة وقت بدء الاسترداد إلى سجل استعادة النسخ الاحتياطية المأخوذة أثناء تشغيل PostgreSQL. (*راجعه Tom Swartz، Stefan Fercot. اقترحه Tom Swartz.*)

  تسجّل الاستعادة الآن الوقت الذي سيبدأ منه الاسترداد، مما يوضح مقدار WAL الذي يجب إعادة تشغيله.

  المشكلة [#1507](https://github.com/pgbackrest/pgbackrest/issues/1507); طلب الدمج [#1518](https://github.com/pgbackrest/pgbackrest/pull/1518); الالتزام [`9e79f0e`](https://github.com/pgbackrest/pgbackrest/commit/9e79f0e64b661e944ce2b3897c366feea1544ac2)
- الإبلاغ عن الخطأ الأصلي وإعادات المحاولة عند فشل المهمة المحلية. (*راجعه Stefan Fercot.*)

  عندما تفشل مهمة محلية بعد محاولات الإعادة، يُبلَّغ الآن عن الخطأ الأول مع تتبع مكدسه، ثم أخطاء المحاولات اللاحقة. سابقًا كان يُعرض الخطأ الأخير فقط، وغالبًا ما كان فشلًا متسلسلًا مثل فقدان تزامن البروتوكول.

  [`136d309`](https://github.com/pgbackrest/pgbackrest/commit/136d309dd4bc1ada9f3d775f036b62292fda390b) السماح بتحديد تتبع مكدس لـ errorInternalThrow().

  [`ae40ed6`](https://github.com/pgbackrest/pgbackrest/commit/ae40ed6ec9cf77e577518b128518a5763767f589) إضافة المعامل jobRetry إلى HRN_CFG_LOAD().

  [`6af827c`](https://github.com/pgbackrest/pgbackrest/commit/6af827cbb1e78cd4c5d649ed4cb24c49a7204b8f) الإبلاغ عن الخطأ الأصلي وإعادات المحاولة عند فشل مهمة محلية.; طلب الدمج [#1521](https://github.com/pgbackrest/pgbackrest/pull/1521)
- إعادة تسمية خطأ مجموع تحقق الصفحات إلى قائمة أخطاء في المخرجات النصية لـ info. (*راجعه Stefan Fercot.*)

  أصبح الوسم في المخرجات النصية لـ `info` هو "error list" بدلًا من "page checksum error". فقد يحتوي الملف على خطأ محاذاة لا خطأ مجموع اختباري لصفحة.

  طلب الدمج [#1519](https://github.com/pgbackrest/pgbackrest/pull/1519); الالتزام [`9346895`](https://github.com/pgbackrest/pgbackrest/commit/9346895f5b61627b50d431f09447e08d8a50caa8)
- إضافة تلميحات إلى رسالة مهلة إعادة تطبيق WAL على خادم الاستعداد. (*راجعه Cynthia Shang، Stefan Fercot. اقترحه Leigh Downs.*)

  يتضمن انتهاء مهلة انتظار إعادة التشغيل على الاحتياطي الآن تلميحات للتحقق من عمل النسخ المتماثل وتعطيل `backup-standby` للنسخ من الأساسي.

  المشكلة [#1434](https://github.com/pgbackrest/pgbackrest/issues/1434); الالتزام [`b7ef12a`](https://github.com/pgbackrest/pgbackrest/commit/b7ef12a76f219881d0b24c715592af96fe5c9b8f)

**إصلاحات أخطاء التوثيق:**

- تصحيح اسم مضيف غير صحيح في دليل المستخدم. (*أصلحه Reid Thompson. راجعه David Steele.*)

  كان إعداد النسخ المتماثل يستخدم عنوان IP لـ pg-primary في `pg_hba.conf` بدلًا من عنوان IP لـ pg-standby.

  طلب الدمج [#1544](https://github.com/pgbackrest/pgbackrest/pull/1544); الالتزام [`1cb8ae1`](https://github.com/pgbackrest/pgbackrest/commit/1cb8ae15de5b4276682bdd9825ca97012cd43855)

**تحسينات التوثيق:**

- تحسين توثيق الخيارات.

  تصف مساعدة `buffer-size` الآن جميع العمليات التي تستخدمه، وأصبحت أوصاف `cmd-ssh` و`repo-host-cmd` و`pg-host-cmd` متسقة، ونُقل `archive-header-check` إلى قسم الأرشيف في مرجع الإعداد.

  [`3763624`](https://github.com/pgbackrest/pgbackrest/commit/376362475e3b3b13b70313d9002d4ff8b25b4b40) نقل الخيار archive-header-check إلى قسم مرجع الأرشيف.

  [`e1f6c06`](https://github.com/pgbackrest/pgbackrest/commit/e1f6c066b3da11fd21b1155c90370c3fa2da06b7) تحسين توثيق الخيار buffer-size.

  [`fa564ee`](https://github.com/pgbackrest/pgbackrest/commit/fa564ee1969229b5cf60d2479d8ace85325f4db3) تحسين توثيق الخيارات cmd-ssh وrepo-host-cmd وpg-host-cmd.

### ملاحظات إصدار v2.35 {#v235-release-notes}

*البروتوكول الثنائي*

*صدر في 23 أغسطس 2021*

**ملاحظة هامة**: تغيّر مستوى السجل للملفات المنسوخة في الأمرين `backup`/`restore` إلى `detail`. يجعل ذلك مستوى السجل `info` أقل ضجيجًا، لكن إذا كانت هذه الرسائل مطلوبة فعيّن مستوى السجل للأمرين `backup`/`restore` إلى `detail`

**إصلاحات الأخطاء:**

- اكتشاف الأخطاء في إنهاء الرفع متعدد الأجزاء في S3. (*راجعه Cynthia Shang. اختبره Marco Montagna. أبلغ عنه Marco Montagna، Lev Kokotov، Anderson A. Mallmann.*)

  قد يفشل إكمال التحميل متعدد الأجزاء حتى عندما يعيد S3 نجاحًا عبر HTTP. تُعامل الاستجابة التي تفتقد `ETag` الآن كفشل، وتُعاد محاولة المهمة.

  [`8e1807c`](https://github.com/pgbackrest/pgbackrest/commit/8e1807cdbe08a6e059ff79220247cf4b3c058979) اكتشاف الأخطاء عند إنهاء تحميل S3 متعدد الأجزاء.; المشكلة [#1116](https://github.com/pgbackrest/pgbackrest/issues/1116); المشكلة [#1290](https://github.com/pgbackrest/pgbackrest/issues/1290); المشكلة [#1433](https://github.com/pgbackrest/pgbackrest/issues/1433); طلب الدمج [#1438](https://github.com/pgbackrest/pgbackrest/pull/1438)

  [`25508a4`](https://github.com/pgbackrest/pgbackrest/commit/25508a48e0d3b0a3eabc6d1fe858b9c3dc12dc86) إضافة المساهمين الذين أُغفلوا في 8e187cdb.
- إصلاح اكتشاف الروابط الرمزية الدائرية. (*راجعه Stefan Fercot. أبلغ عنه Rohit Raveendran.*)

  كانت الروابط تُتبع قبل فحصها، وكان الرابط الدائري يدفع بناء manifest إلى استدعاء ذاتي لا ينتهي ثم التعطل.

  المشكلة [#1447](https://github.com/pgbackrest/pgbackrest/issues/1447); طلب الدمج [#1452](https://github.com/pgbackrest/pgbackrest/pull/1452); الالتزام [`43b8746`](https://github.com/pgbackrest/pgbackrest/commit/43b874628c86ec4fe297dbd5cab5bd3f62b8639b)
- تمرير خيارات `repo` المحددة فقط إلى الطرف البعيد. (*راجعه David Christensen، Cynthia Shang. أبلغ عنه Greg Sabino Mullane، David Christensen.*)

  كان يمكن لخيارات المستودعات الأخرى أن تسبب تعارضات على المضيف البعيد الذي يستخدم مستودعًا واحدًا فقط.

  طلب الدمج [#1480](https://github.com/pgbackrest/pgbackrest/pull/1480); الالتزام [`935de1e`](https://github.com/pgbackrest/pgbackrest/commit/935de1e7a06d60415c16cad137875b49346337c6)

**التحسينات:**

- البروتوكول الثنائي. (*راجعه Cynthia Shang.*)

  تتواصل العمليات المحلية والبعيدة الآن بتنسيق pack ثنائي بدلًا من JSON. الحزم أصغر وأسرع في الإنشاء والتحليل وذات أنواع صارمة. تُكتب كل رسالة في موضع واحد، مما يقلل احتمال أن يترك خطأ البروتوكول في حالة غير سليمة، ولا يوجد حد لحجم الرسائل.

  [`6a1c033`](https://github.com/pgbackrest/pgbackrest/commit/6a1c0337ddee9900dda58b7d2fa74d82c0586ed2) بروتوكول ثنائي.; طلب الدمج [#1424](https://github.com/pgbackrest/pgbackrest/pull/1424)

  [`2d5cbfc`](https://github.com/pgbackrest/pgbackrest/commit/2d5cbfc73142fa99df609aa23b64db5342e73c88) إصلاح تسربات الذاكرة التي أدخلها البروتوكول الثنائي في 6a1c0337.

  [`f716cb6`](https://github.com/pgbackrest/pgbackrest/commit/f716cb6f4f9765baa03f71b5563786d79d9f04a2) إصلاح استخدام الذاكرة بعد تحريرها الذي أدخله البروتوكول الثنائي في 6a1c0337.

  [`4fb6384`](https://github.com/pgbackrest/pgbackrest/commit/4fb6384f10f6cd26c422ab9b24feb5ae0ebeeee9) إصلاح مزيد من تسربات الذاكرة التي أدخلها البروتوكول الثنائي في 6a1c0337.
- إنشاء دليل البيانات تلقائيًا عند `restore`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Chris Bandy.*)

  كان فحص منقول من Perl يمنع الاستعادة من إنشاء دليل البيانات.

  المشكلة [#1445](https://github.com/pgbackrest/pgbackrest/issues/1445); طلب الدمج [#1454](https://github.com/pgbackrest/pgbackrest/pull/1454); الالتزام [`056a307`](https://github.com/pgbackrest/pgbackrest/commit/056a3070e0dba299389c7b5049878d40dd91ec9a)
- السماح بـ `restore` مع `--type=lsn`. (*ساهم به Stefan Fercot. راجعه Cynthia Shang. اقترحه James Coleman.*)

  عيّن `type=lsn` وحدد LSN في `target` للاسترداد إلى LSN على PostgreSQL >= 10.

  المشكلة [#1339](https://github.com/pgbackrest/pgbackrest/issues/1339); طلب الدمج [#1462](https://github.com/pgbackrest/pgbackrest/pull/1462); الالتزام [`563d117`](https://github.com/pgbackrest/pgbackrest/commit/563d117967ab9770f9f646c6186d0bc37121611f)
- تغيير مستوى تسجيل الملفات المنسوخة للأمرين `backup`/`restore` إلى detail. (*راجعه Stefan Fercot. اقترحه Jens Wilke.*)

  يقلل ذلك كثرة الرسائل في مستوى السجل `info`. عيّن مستوى السجل إلى `detail` لرؤية كل ملف منسوخ.

  المشكلة [#1277](https://github.com/pgbackrest/pgbackrest/issues/1277); طلب الدمج [#1455](https://github.com/pgbackrest/pgbackrest/pull/1455); الالتزام [`849ab34`](https://github.com/pgbackrest/pgbackrest/commit/849ab343aa10d66fbbd27cad407eff981c186d06)
- التكرار حلقيًا أثناء انتظار وصول LSN نقطة التحقق إلى LSN إعادة تطبيق WAL. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Fatih Mencutekin.*)

  على الخادم الاحتياطي، قد يتأخر LSN نقطة التحقق قليلًا عن LSN إعادة التشغيل حتى يُحدَّث `pg_control`. يواصل النسخ الاحتياطي الآن الفحص بدلًا من الفشل.

  المشكلة [#1450](https://github.com/pgbackrest/pgbackrest/issues/1450); طلب الدمج [#1460](https://github.com/pgbackrest/pgbackrest/pull/1460); الالتزام [`8fac1ac`](https://github.com/pgbackrest/pgbackrest/commit/8fac1ac50d28557d162fbb251fbbdcc3c9fb950c)
- تسجيل إجمالي ملفات `backup` وإجمالي الحجم/الملفات لـ `restore`. (*راجعه Cynthia Shang.*)

  يُسجَّل حجم النسخة الاحتياطية الآن في نهايتها، ويشمل الملفات المضافة إلى manifest بعد النسخ الرئيسي، مثل `backup_label` وWAL. وتسجّل الاستعادة الآن حجمها وإجمالي ملفاتها.

  طلب الدمج [#1489](https://github.com/pgbackrest/pgbackrest/pull/1489); الالتزام [`a0bdfa4`](https://github.com/pgbackrest/pgbackrest/commit/a0bdfa436c9e1c2723be905ebe5cef7809a26244)

**إصلاحات أخطاء التوثيق:**

- إصلاح أسماء مضيفات غير صحيحة في دليل المستخدم. (*راجعه Stefan Fercot. أبلغ عنه Greg Sabino Mullane.*)

  كانت بعض الأمثلة تعرض `pg1` بدلًا من اسم المضيف، وكانت كتلة التثبيت تثبّت الحزم على مضيف البناء بغض النظر عن المضيف المحدد.

  طلب الدمج [#1479](https://github.com/pgbackrest/pgbackrest/pull/1479); الالتزام [`155ef85`](https://github.com/pgbackrest/pgbackrest/commit/155ef85013088a1150a4c15b04af36420d06e9c3)

**تحسينات التوثيق:**

- تحديث توثيق المساهمة وإضافة قالب لطلبات الدمج. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  أصبح دليل المساهمة يتضمن جدول محتويات وأقسامًا لفهم مخرجات الاختبارات وتقديم طلب دمج. ويعرض GitHub الآن قالبًا لطلبات الدمج الجديدة.

  [`e3d05e2`](https://github.com/pgbackrest/pgbackrest/commit/e3d05e2b4aa80149219b6d49a3136b34fa268127) تحديث توثيق المساهمة وإضافة قالب لطلب الدمج.; طلب الدمج [#1469](https://github.com/pgbackrest/pgbackrest/pull/1469)

  [`71b654f`](https://github.com/pgbackrest/pgbackrest/commit/71b654fc29497319862fe01c3917bbc353cc6dd9) تصحيح الروابط وتحديث مثال العملية الابنة.; طلب الدمج [#1487](https://github.com/pgbackrest/pgbackrest/pull/1487)
- إعادة ترتيب توثيق النسخ الاحتياطي في دليل المستخدم. (*راجعه Cynthia Shang.*)

  نُقل قسما «خيار البدء السريع» و«مهلة الأرشيف» إلى «البدء السريع - إجراء النسخ الاحتياطي». وأُزيل قسم «خيار الإيقاف التلقائي» الذي ينطبق فقط على PostgreSQL <= 9.6.

  طلب الدمج [#1488](https://github.com/pgbackrest/pgbackrest/pull/1488); الالتزام [`6ab18dc`](https://github.com/pgbackrest/pgbackrest/commit/6ab18dc0fa42885aea8eb9405ab0a943c2d49a71)
- توضيح سلوك `--type` للأمر `restore` في مرجع الأوامر. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  يوضح المرجع الآن وجوب تحديد `set` عندما يكون الهدف قبل أحدث نسخة احتياطية ويكون `type` مختلفًا عن `time`.

  الالتزام [`a6691c6`](https://github.com/pgbackrest/pgbackrest/commit/a6691c6f615f90195aeb6c1c6657a6afd79a10d3)
- إصلاح أخطاء إملائية في التوثيق والتعليقات. (*ساهم به Eric Radman. راجعه David Steele.*)

  طلب الدمج [#1446](https://github.com/pgbackrest/pgbackrest/pull/1446); الالتزام [`23bdc3d`](https://github.com/pgbackrest/pgbackrest/commit/23bdc3deb62a622713064df3b0777110ebba8723)

**تحسينات مجموعة الاختبارات:**

- إضافة فحص لمسار الاختبار داخل مسار المستودع. (*راجعه Greg Sabino Mullane. اقترحه Greg Sabino Mullane.*)

  كان مسار اختبار داخل مسار المستودع يسبب إخفاقات غريبة لأن المستودع يُنسخ إلى مسار الاختبار. يُصدر `test.pl` الآن خطأ في هذه الحالة.

  المشكلة [#1472](https://github.com/pgbackrest/pgbackrest/issues/1472); طلب الدمج [#1474](https://github.com/pgbackrest/pgbackrest/pull/1474); الالتزام [`e32f9e1`](https://github.com/pgbackrest/pgbackrest/commit/e32f9e146b11389e3d16feba9665360b73737d66)
- إضافة تحليل شيفرة ثابت بـ CodeQL. (*راجعه Cynthia Shang.*)

  يعمل CodeQL الآن في CI. أُصلحت المشكلات التي وجدها، مثل استبدال `gmtime()`/`localtime()` بـ `gmtime_r()`/`localtime_r()`.

  طلب الدمج [#1457](https://github.com/pgbackrest/pgbackrest/pull/1457); الالتزام [`3c8819e`](https://github.com/pgbackrest/pgbackrest/commit/3c8819e10f9eff89195566e7e02f349373f5c4c7)
- تحديث الاختبارات لاستخدام الأنماط القياسية. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  [`3f9fbc3`](https://github.com/pgbackrest/pgbackrest/commit/3f9fbc3c24eab48e7ae2871484ea01273049e601) تحديث اختبار command/expire لاستخدام الأنماط القياسية.; طلب الدمج [#1420](https://github.com/pgbackrest/pgbackrest/pull/1420)

  [`03021c6`](https://github.com/pgbackrest/pgbackrest/commit/03021c6a17f1374e84ef42614fa1dd2a6be4b64d) تحديث اختبار command/stanza لاستخدام الأنماط القياسية.; طلب الدمج [#1426](https://github.com/pgbackrest/pgbackrest/pull/1426)

  [`8dd882b`](https://github.com/pgbackrest/pgbackrest/commit/8dd882badee76b038dc8b494a1112eb3e18ef678) تحديث اختبار info/infoArchive لاستخدام الأنماط القياسية.; طلب الدمج [#1436](https://github.com/pgbackrest/pgbackrest/pull/1436)

  [`ff95edd`](https://github.com/pgbackrest/pgbackrest/commit/ff95eddc369597c76a9ea70ffbada493ed4d1951) تحديث اختبار command/verify لاستخدام الأنماط القياسية.; طلب الدمج [#1435](https://github.com/pgbackrest/pgbackrest/pull/1435)

  [`17c9ed0`](https://github.com/pgbackrest/pgbackrest/commit/17c9ed0ef0380fb14fba9a5299b6618ca8c92c2e) تحديث اختبار command/info لاستخدام الأنماط القياسية.; طلب الدمج [#1432](https://github.com/pgbackrest/pgbackrest/pull/1432)

  [`bffb43e`](https://github.com/pgbackrest/pgbackrest/commit/bffb43ea3fe00f445a2fc3c44a07f105cee65b4b) تحديث اختبار command/check لاستخدام الأنماط القياسية.; طلب الدمج [#1431](https://github.com/pgbackrest/pgbackrest/pull/1431)

  [`fb2d111`](https://github.com/pgbackrest/pgbackrest/commit/fb2d111dcd75021313a64a348959482339bf7f2a) تحديث اختبار info/infoBackup لاستخدام الأنماط القياسية.; طلب الدمج [#1437](https://github.com/pgbackrest/pgbackrest/pull/1437)

  [`065a8c8`](https://github.com/pgbackrest/pgbackrest/commit/065a8c8454d2acdd72c0c71a24d6b8bc09669e18) استبدال تعريفات المعالج القبلي بثوابت نصية في اختبارات الوحدات.; طلب الدمج [#1440](https://github.com/pgbackrest/pgbackrest/pull/1440)

  [`c620811`](https://github.com/pgbackrest/pgbackrest/commit/c6208113bfce9d637ca3fd0b35ab28a819c1a83e) إضافة المعامل timeModified إلى الماكرو HRN_STORAGE_PUT().

  [`6a90d46`](https://github.com/pgbackrest/pgbackrest/commit/6a90d469094ee2697ae4c932349756a54136799d) تحديث اختبار info/manifest لاستخدام الأنماط القياسية.; طلب الدمج [#1444](https://github.com/pgbackrest/pgbackrest/pull/1444)

  [`62e8d97`](https://github.com/pgbackrest/pgbackrest/commit/62e8d97af03e7628d5710b17aad1cc31f83d7e69) تحديث اختبارات command/archive لاستخدام الأنماط القياسية.; طلب الدمج [#1449](https://github.com/pgbackrest/pgbackrest/pull/1449)

  [`8bb0b28`](https://github.com/pgbackrest/pgbackrest/commit/8bb0b28455d59ef884eab7ab25a91f988adbab81) تحديث اختباري command/control وcommand/command لاستخدام الأنماط القياسية.; طلب الدمج [#1456](https://github.com/pgbackrest/pgbackrest/pull/1456)

  [`f2ec4e0`](https://github.com/pgbackrest/pgbackrest/commit/f2ec4e00a4c4c388a8f1b094381fd566a3dc9aa7) إضافة معاملات التشفير إلى الماكرو TEST_STORAGE_GET().

  [`4ad0bbd`](https://github.com/pgbackrest/pgbackrest/commit/4ad0bbda53b34688146f14d130cf0e53c8dd650f) تحديث اختبارات command/backup لاستخدام الأنماط القياسية.; طلب الدمج [#1463](https://github.com/pgbackrest/pgbackrest/pull/1463)

  [`117ffe8`](https://github.com/pgbackrest/pgbackrest/commit/117ffe88965fd60ce3dcb328e9d28503870af05a) تحديث اختبارات command/help لاستخدام الأنماط القياسية.; طلب الدمج [#1464](https://github.com/pgbackrest/pgbackrest/pull/1464)

  [`ebe5848`](https://github.com/pgbackrest/pgbackrest/commit/ebe5848494d4e37a9c86f1fafb5b3453c1f425a6) تحديث اختباري command/local وcommand/remote لاستخدام الأنماط القياسية.; طلب الدمج [#1466](https://github.com/pgbackrest/pgbackrest/pull/1466)

  [`a6cdf5b`](https://github.com/pgbackrest/pgbackrest/commit/a6cdf5b22f0eed53f33bbd84478af0542c81af7d) تحديث اختبار command/repo لاستخدام الأنماط القياسية.; طلب الدمج [#1467](https://github.com/pgbackrest/pgbackrest/pull/1467)

  [`4992508`](https://github.com/pgbackrest/pgbackrest/commit/49925087644c76df005828eb27c24f503a09b20b) تحديث اختبار command/restore لاستخدام الأنماط القياسية.; طلب الدمج [#1468](https://github.com/pgbackrest/pgbackrest/pull/1468)

  [`4c9ddf5`](https://github.com/pgbackrest/pgbackrest/commit/4c9ddf5ef25d0f441e20e918f57c1ec79218cfdb) تحديث اختبارات storage لاستخدام الأنماط القياسية.; طلب الدمج [#1470](https://github.com/pgbackrest/pgbackrest/pull/1470)

  [`eeaab6a`](https://github.com/pgbackrest/pgbackrest/commit/eeaab6a3d192fc788c0f74aadbf4b3de5da52531) تحديث اختبارات config، باستثناء parse، لاستخدام الأنماط القياسية.; طلب الدمج [#1473](https://github.com/pgbackrest/pgbackrest/pull/1473)

  [`f653b59`](https://github.com/pgbackrest/pgbackrest/commit/f653b59664e757a0e3da63cc8462deafe2d9e0ef) تحديث اختبار db/db لاستخدام الأنماط القياسية.; طلب الدمج [#1486](https://github.com/pgbackrest/pgbackrest/pull/1486)

  [`e17865a`](https://github.com/pgbackrest/pgbackrest/commit/e17865a03a5451b82a101557d400ff223d104383) تحديث اختبار protocol/protocol لاستخدام الأنماط القياسية.; طلب الدمج [#1491](https://github.com/pgbackrest/pgbackrest/pull/1491)

  [`eca2fc6`](https://github.com/pgbackrest/pgbackrest/commit/eca2fc69589cd44f7c1a43206553984adde5cfb1) تحديث اختبار config/parse لاستخدام الأنماط القياسية.; طلب الدمج [#1492](https://github.com/pgbackrest/pgbackrest/pull/1492)

### ملاحظات إصدار v2.34 {#v234-release-notes}

*دعم PostgreSQL 14*

*صدر في 7 يونيو 2021*

**إصلاحات الأخطاء:**

- إصلاح مشكلات ملفات spool المتبقية من `restore` سابق. (*راجعه Cynthia Shang، Stefan Fercot. اختبره Floris van Nee. أبلغ عنه Floris van Nee.*)

  كان إشعار تركته استعادة سابقة في مسار spool قد يجعل `archive-get` يُبلغ عن فقدان مقطع WAL. عندما يُعثر على هذا الإشعار في الفحص الأول، يُحذف الآن وتُشغَّل العملية غير المتزامنة مجددًا. ويُبلَّغ عن خطأ عندما لا تستجيب العملية بدلًا من الإبلاغ عن فقدان المقطع.

  المشكلة [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); طلب الدمج [#1371](https://github.com/pgbackrest/pgbackrest/pull/1371); الالتزام [`f45e76f`](https://github.com/pgbackrest/pgbackrest/commit/f45e76fa2e8ce0f62317a74fdd51083d52659cd5)
- إصلاح مشكلة عند فحص روابط أعداد كبيرة من مساحات الجداول. (*راجعه Cynthia Shang. اختبره Avinash Vallarapu. أبلغ عنه Avinash Vallarapu.*)

  كان فحص الروابط يستهلك ذاكرة كثيرة مع عدد كبير من مساحات الجداول وقد يتعطل. الفحص الجديد أسرع بكثير ويستخدم ذاكرة أقل بكثير، ويكتشف أيضًا روابط الملفات المكررة.

  المشكلة [#1354](https://github.com/pgbackrest/pgbackrest/issues/1354); طلب الدمج [#1356](https://github.com/pgbackrest/pgbackrest/pull/1356); الالتزام [`eba013b`](https://github.com/pgbackrest/pgbackrest/commit/eba013b49b850e53d59795ac6358fcb3381048a3)
- تحرير الأطراف البعيدة التي لم تعد ضرورية حتى لا تنتهي مهلتها أثناء `restore`. (*راجعه Cynthia Shang. أبلغ عنه Francisco Miguel Biete Banon.*)

  كانت الاتصالات بالمضيفين البعيدين تُحفظ طوال الاستعادة وقد تنتهي مهلتها، فتُسجَّل في نهاية استعادة طويلة رسالة تحذير غير ضارة لكنها مشتتة. تُغلق الاتصالات الآن بعد تحميل manifest.

  المشكلة [#1368](https://github.com/pgbackrest/pgbackrest/issues/1368); طلب الدمج [#1374](https://github.com/pgbackrest/pgbackrest/pull/1374); الالتزام [`06fa185`](https://github.com/pgbackrest/pgbackrest/commit/06fa18582a405417c8ab4ba667cb01a13a5c3103)
- إصلاح `help` عندما يكون خيار صالح غير صالح للأمر المحدد. (*راجعه Stefan Fercot. أبلغ عنه Cynthia Shang.*)

  كان `help` يسبب خطأ تجزئة عند السؤال عن خيار غير صالح للأمر.

  طلب الدمج [#1375](https://github.com/pgbackrest/pgbackrest/pull/1375); الالتزام [`45f8355`](https://github.com/pgbackrest/pgbackrest/commit/45f83558ea862c6f496a27b886e1160e6303bbe8)

**الميزات:**

- إضافة دعم PostgreSQL 14. (*راجعه Cynthia Shang.*)

  لا يتطلب PostgreSQL 14 تغييرات شيفرة مقارنةً بـ PostgreSQL 13. ويمكن لإصدار الكتالوج الآن أن يتغير أثناء مرحلة beta/rc لـ PostgreSQL دون الحاجة إلى إصدار pgBackRest جديد.

  طلب الدمج [#1413](https://github.com/pgbackrest/pgbackrest/pull/1413); الالتزام [`2452c4d`](https://github.com/pgbackrest/pgbackrest/commit/2452c4d5a4c230b8e3c33d3bddf69e56dfbec284)
- إضافة مصادقة GCS تلقائية لمثيلات GCE. (*راجعه Jan Wieck. اختبره Daniel Farina.*)

  عيّن `repo-gcs-key-type=auto` للحصول على رمز المصادقة من بيانات المثيل الوصفية على مثيل GCE.

  [`7b71604`](https://github.com/pgbackrest/pgbackrest/commit/7b71604defa02d5ed9b7aa3407961cb59a52cc45) استخدام المتغير الموجود لمنفذ خادم اختبار GCS.

  [`26fefa6`](https://github.com/pgbackrest/pgbackrest/commit/26fefa6aeeae90bbb572ea57b605fb8fe526f1a0) فصل تحليل استجابة رمز GCS في دالة مستقلة.

  [`9af0331`](https://github.com/pgbackrest/pgbackrest/commit/9af033194abc4b1cd3f06c3a97fff71c966c3827) إضافة مصادقة GCS تلقائية لمثيلات GCE.; طلب الدمج [#1395](https://github.com/pgbackrest/pgbackrest/pull/1395)
- إضافة خيار `repo-retention-history` لإنهاء صلاحية السجل التاريخي للنسخ الاحتياطية. (*ساهم به Stefan Fercot. راجعه Cynthia Shang، David Steele.*)

  حدد عدد أيام الاحتفاظ بتاريخ النسخ الاحتياطية. يُحتفَظ افتراضيًا بالتاريخ كله، ولا يُحذف أبدًا تاريخ النسخ التي ما زالت في المستودع. عند انتهاء الاحتفاظ بملف manifest لنسخة كاملة، تُحذف أيضًا ملفات manifest لنسخها التفاضلية والتزايدية.

  طلب الدمج [#1389](https://github.com/pgbackrest/pgbackrest/pull/1389); الالتزام [`5b332b2`](https://github.com/pgbackrest/pgbackrest/commit/5b332b22b508d896abb64fa6abe26c78c83a29bc)
- إضافة خيار `db-exclude`. (*ساهم به Stefan Fercot. راجعه Cynthia Shang.*)

  تستثني الاستعادة قواعد البيانات المحددة بكتابتها كملفات متناثرة ومصفّرة. يظل PostgreSQL قادرًا على إجراء الاسترداد، ويمكن حذف القواعد بعده. مع `db-include`، لا ينطبق `db-exclude` إلا على قواعد النظام `template0` و`template1` و`postgres`.

  المشكلة [#986](https://github.com/pgbackrest/pgbackrest/issues/986); طلب الدمج [#1337](https://github.com/pgbackrest/pgbackrest/pull/1337); الالتزام [`292f836`](https://github.com/pgbackrest/pgbackrest/commit/292f836f1243e51d102bb4be202e7b21a7a386b1)

**التحسينات:**

- تغيير تسجيل انتهاء صلاحية الأرشيف من مستوى detail إلى info. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  طلب الدمج [#1416](https://github.com/pgbackrest/pgbackrest/pull/1416); الالتزام [`aceb956`](https://github.com/pgbackrest/pgbackrest/commit/aceb956815a87f0c19ea171de25d2c3842a6d806)
- إزالة مسار spool أرشيف الـ stanza عند `restore`. (*راجعه Cynthia Shang، Stefan Fercot.*)

  كان يمكن للملفات في مسار spool أن تتداخل مع العنقود الجديد؛ مثلًا، قد تجعله إقرارات `archive-push` القديمة يتجاوز أرشفة WAL.

  المشكلة [#1357](https://github.com/pgbackrest/pgbackrest/issues/1357); طلب الدمج [#1386](https://github.com/pgbackrest/pgbackrest/pull/1386); الالتزام [`320c6e1`](https://github.com/pgbackrest/pgbackrest/commit/320c6e1aad2cc9a8dabecb2bc91a9b34464de6ec)
- عدم كتابة الملفات ذريًا أو مزامنة المسارات أثناء نسخ `backup`. (*راجعه Stephen Frost، Stefan Fercot، Cynthia Shang.*)

  لا تلزم الكتابات الذرية لأن المجاميع الاختبارية تُفحص عند استئناف نسخة فاشلة، وتُزامَن جميع المسارات في نهاية النسخ الاحتياطي.

  طلب الدمج [#1373](https://github.com/pgbackrest/pgbackrest/pull/1373); الالتزام [`aa72c19`](https://github.com/pgbackrest/pgbackrest/commit/aa72c19a831fb0dd15a50a003fbaad427f335353)

**تحسينات التوثيق:**

- تحديث توثيق المساهمة. (*ساهم به Cynthia Shang. راجعه David Steele، Stefan Fercot.*)

  يتضمن دليل المساهمة مزيدًا من الأمثلة على كتابة الشيفرة وإضافة خيارات الإعداد والاختبار.

  طلب الدمج [#1400](https://github.com/pgbackrest/pgbackrest/pull/1400); الالتزام [`68faf14`](https://github.com/pgbackrest/pgbackrest/commit/68faf1482a42ea14f5b00a91e19bd5aedec275b8)
- دمج دليل مستخدم RHEL/CentOS في مستند واحد. (*راجعه Cynthia Shang.*)

  كان الدليل الثاني موجودًا أساسًا لتوثيق `stop-auto` لـ PostgreSQL <= 9.5 الذي انتهى دعمه الآن. ولا يزال الخيار موثقًا في المرجع.

  طلب الدمج [#1405](https://github.com/pgbackrest/pgbackrest/pull/1405); الالتزام [`ccac75e`](https://github.com/pgbackrest/pgbackrest/commit/ccac75e7de8754b39bb691ff8830a2839ea7a285)
- توضيح أن `repo-s3-role` ليس `ARN`. (*ساهم به Isaac Yuen. راجعه David Steele.*)

  طلب الدمج [#1365](https://github.com/pgbackrest/pgbackrest/pull/1365); الالتزام [`5bf1606`](https://github.com/pgbackrest/pgbackrest/commit/5bf160643b53699a28a8f0920c36d6ded767d249)

### ملاحظات إصدار v2.33 {#v233-release-notes}

*دعم المستودعات المتعددة وGCS*

*صدر في 5 أبريل 2021*

**إصلاحات الأخطاء:**

- إصلاح تحذيرات الخيارات التي تكسر `archive-get`/`archive-push` غير المتزامنين. (*راجعه Cynthia Shang. أبلغ عنه Lev Kokotov.*)

  كان تحذير خيار في العملية غير المتزامنة يُكتب إلى stdout مغلق، مما يجهض العملية. وبما أن الدور غير المتزامن قد يملك الآن خيارات صالحة مختلفة عن الدور الافتراضي، فقد أصبح ذلك أكثر تكرارًا. تُسجَّل تحذيرات الخيارات الآن للدور الافتراضي فقط.

  المشكلة [#1299](https://github.com/pgbackrest/pgbackrest/issues/1299); طلب الدمج [#1301](https://github.com/pgbackrest/pgbackrest/pull/1301); الالتزام [`3837e61`](https://github.com/pgbackrest/pgbackrest/commit/3837e61a7504b1e211e4b3a70cbe97343c1cf2e6)
- إصلاح تسريب للذاكرة أثناء نسخ الأرشيف في النسخ الاحتياطي. (*راجعه Cynthia Shang. أبلغ عنه Christian ROUX، Efremov Egor.*)

  كان نسخ WAL إلى النسخة الاحتياطية باستخدام `archive-copy` يسرّب الذاكرة، خصوصًا عندما يلزم إعادة ضغط WAL.

  المشكلة [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); الالتزام [`778adbf`](https://github.com/pgbackrest/pgbackrest/commit/778adbf19f71ceb90071f01197bf189d59b14df0)
- إصلاح فيض المكدس في توليد عبارة مرور التشفير. (*راجعه Cynthia Shang. أبلغ عنه bsiara.*)

  لم يكن في مخزن عبارة المرور المولّدة مكان للصفر الختامي. اكتُشف ذلك على arm64 مع musl libc.

  المشكلة [#1294](https://github.com/pgbackrest/pgbackrest/issues/1294); طلب الدمج [#1295](https://github.com/pgbackrest/pgbackrest/pull/1295); الالتزام [`d29855b`](https://github.com/pgbackrest/pgbackrest/commit/d29855bd0bf8b957fa8c06445d22e425c443a704)
- إصلاح `repo-ls` `/` على مستودعات S3. (*راجعه Cynthia Shang. أبلغ عنه Lesovsky Alexey.*)

  يُبلغ S3 عن `/` كملف دون الترويسات المتوقعة، مما كان يسبب خطأ. يُبلَّغ الآن عن `/` بأنه غير موجود على التخزين الذي لا يدعم المسارات.

  المشكلة [#1317](https://github.com/pgbackrest/pgbackrest/issues/1317); طلب الدمج [#1336](https://github.com/pgbackrest/pgbackrest/pull/1336); الالتزام [`b1d945e`](https://github.com/pgbackrest/pgbackrest/commit/b1d945ebb774c25676155af439b0558e8582bbe5)

**الميزات:**

- دعم المستودعات المتعددة. (*ساهم به Cynthia Shang، David Steele. راجعه Stefan Fercot، Stephen Frost.*)

  يمكن إعداد ما يصل إلى أربعة مستودعات، مثل مستودع محلي للاستعادة السريعة وآخر بعيد للتكرار الاحتياطي. يرسل `archive-push` ملفات WAL إلى جميع المستودعات، وتُجدول النسخ الاحتياطية لكل مستودع. تعمل بعض الأوامر مع جميع المستودعات، بينما تتطلب أخرى `repo`. لا يُشترط `repo` عندما لا يكون مضبوطًا إلا `repo1`.

  [`3408f1e`](https://github.com/pgbackrest/pgbackrest/commit/3408f1ee2ee3f774699a15de045e0afe3eaf9a26) تحسين دعم المستودعات المتعددة في الأمر expire.; طلب الدمج [#1289](https://github.com/pgbackrest/pgbackrest/pull/1289)

  [`e28f6f1`](https://github.com/pgbackrest/pgbackrest/commit/e28f6f11e97a80e9c1adf1a6eaeeabbfc991914f) يواصل expire العمل عند حدوث خطأ أثناء معالجة مستودع.; طلب الدمج [#1308](https://github.com/pgbackrest/pgbackrest/pull/1308)

  [`bec3e20`](https://github.com/pgbackrest/pgbackrest/commit/bec3e20b2cb061ef0413df24234ebe246ea53063) إضافة دعم المستودعات المتعددة إلى الأمر archive-get.; طلب الدمج [#1292](https://github.com/pgbackrest/pgbackrest/pull/1292)

  [`118d9e6`](https://github.com/pgbackrest/pgbackrest/commit/118d9e64fea71c2e049b52802e55f72f5793871b) تحسين دعم المستودعات المتعددة في الأمر restore.; طلب الدمج [#1300](https://github.com/pgbackrest/pgbackrest/pull/1300)

  [`065b2ff`](https://github.com/pgbackrest/pgbackrest/commit/065b2ff2300a9f06a8c32621fac521451ca942bd) إعادة تنظيم repoMin/Max في الأمر info.

  [`0ddc038`](https://github.com/pgbackrest/pgbackrest/commit/0ddc0380ff408f9ed6e8bcd4d328df500681ce77) إزالة مستودع restore الافتراضي من اختبارات التكامل.

  [`13dc8e6`](https://github.com/pgbackrest/pgbackrest/commit/13dc8e68d74fa9e06180e67b7e59994767b4a34d) جعل --repo اختياريًا للأمر backup.; طلب الدمج [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`a1280c4`](https://github.com/pgbackrest/pgbackrest/commit/a1280c41e530500e5bbde73a900683f6db207686) إعادة تنظيم تحذيرات الأمر archive-push لتعمل مثل archive-get.

  [`3b8f0ef`](https://github.com/pgbackrest/pgbackrest/commit/3b8f0ef7ae8a81ae969934fff4ad3da299454b24) إضافة تحمل أعطال الكتابة إلى الأمر archive-push.; طلب الدمج [#1316](https://github.com/pgbackrest/pgbackrest/pull/1316)

  [`95063f6`](https://github.com/pgbackrest/pgbackrest/commit/95063f6812279cd59380fd72e16e67b631582bd0) جعل --repo اختياريًا للأوامر المتبقية باستثناء stanza-delete.

  [`1dbb3bf`](https://github.com/pgbackrest/pgbackrest/commit/1dbb3bf50b94dcc9d53dfe1e5ad57a17bd6d38e8) دعم مستودعات متعددة.; طلب الدمج [#1227](https://github.com/pgbackrest/pgbackrest/pull/1227)

  [`31c7824`](https://github.com/pgbackrest/pgbackrest/commit/31c7824a4d84cbf5a0ba0938f4caa546fa67af0a) السماح بتشغيل أوامر stanza-* عن بُعد.; طلب الدمج [#1326](https://github.com/pgbackrest/pgbackrest/pull/1326)

  [`2789d3b`](https://github.com/pgbackrest/pgbackrest/commit/2789d3b6206c4de9299a3bc459e04cdab793abc9) تحسين تحمل الأعطال في الأمر info.; طلب الدمج [#1342](https://github.com/pgbackrest/pgbackrest/pull/1342)

  [`01b8e22`](https://github.com/pgbackrest/pgbackrest/commit/01b8e2258f6efa5386665c33cb5c267c154376fb) تحسين تحمل الأعطال في الأمر archive-push.; طلب الدمج [#1343](https://github.com/pgbackrest/pgbackrest/pull/1343)
- دعم GCS لتخزين المستودع. (*راجعه Cynthia Shang. اختبره Daniel Farina.*)

  عيّن `repo-type=gcs` لتخزين المستودع على GCS أو تخزين كائنات متوافق معه.

  [`dcb79ab`](https://github.com/pgbackrest/pgbackrest/commit/dcb79ab8fb18c63c2d56ecacd9d680b999ea044b) فك ترميز محارف JSON المهروبة بصيغة \u.

  [`1b4b353`](https://github.com/pgbackrest/pgbackrest/commit/1b4b3538cc218f66ed1e903c3caeade4b0ab1120) إعادة تسمية uri إلى path حيثما يناسب في وحدتي HTTP والتخزين.

  [`66a4ff4`](https://github.com/pgbackrest/pgbackrest/commit/66a4ff496afe63305cb1a437bcb52d1efc11edf7) ترميز المسار قبل تمريره إلى HttpRequest.

  [`d485609`](https://github.com/pgbackrest/pgbackrest/commit/d4856096587c72daee76f8ad8408db677a16d6dd) إضافة strNewEncode() وstrCatEncode() وbufNewDecode().

  [`abcbe0f`](https://github.com/pgbackrest/pgbackrest/commit/abcbe0f9c1804ecb1b93b811cfb0a362c17e1b85) دمج ملفات الوحدة encode في ملف واحد.

  [`edab2a0`](https://github.com/pgbackrest/pgbackrest/commit/edab2a0b89eabc5fd5ba6e795d938670bd5d3105) استخدام switch بدلًا من if-else لأنواع الترميز.

  [`f6c3262`](https://github.com/pgbackrest/pgbackrest/commit/f6c3262861252b24e7e0cffd6d67e0c5e3291f3e) عدم إتاحة دوال valid/validate خارج الوحدة encode.

  [`a1f4fd3`](https://github.com/pgbackrest/pgbackrest/commit/a1f4fd32a1790e569ccae3598cd9648bb25d13b6) إضافة ASSERT_MSG().

  [`00b60e5`](https://github.com/pgbackrest/pgbackrest/commit/00b60e564eef13f8adba0ab867fcde2c352669d6) إضافة ترميز base64url.

  [`54c4eb0`](https://github.com/pgbackrest/pgbackrest/commit/54c4eb0c10758879b4bf2b96efd2a1523ecccc21) جعل كائنات التخزين البعيد قابلة للكتابة.

  [`088662d`](https://github.com/pgbackrest/pgbackrest/commit/088662d986288843d1bfd118b724091c93df4569) دعم GCS لتخزين المستودعات.; المشكلة [#631](https://github.com/pgbackrest/pgbackrest/issues/631); المشكلة [#743](https://github.com/pgbackrest/pgbackrest/issues/743); طلب الدمج [#1320](https://github.com/pgbackrest/pgbackrest/pull/1320)
- إضافة خيار `archive-header-check`. (*راجعه Stephen Frost، Cynthia Shang. اقترحه Hans-Jürgen Schönig.*)

  تُفحص ترويسة WAL مقابل إصدار PostgreSQL ومعرّف النظام للتأكد من إرساله إلى stanza الصحيح. الفحص مفعّل افتراضيًا ويمكن تعطيله عند الحاجة، مثلًا لـ WAL المشفّر.

  طلب الدمج [#1298](https://github.com/pgbackrest/pgbackrest/pull/1298); الالتزام [`b6106f3`](https://github.com/pgbackrest/pgbackrest/commit/b6106f3c1f586b410c50c9da8dcea583cc157423)

**التحسينات:**

- تضمين قواعد البيانات النظامية المعاد إنشاؤها أثناء الاستعادة الانتقائية. (*ساهم به Stefan Fercot. راجعه Cynthia Shang.*)

  تملك قاعدة النظام (`template0` أو `template1` أو `postgres`) التي أُعيد إنشاؤها OID يجعلها تبدو كقاعدة مستخدم. تُستعاد هذه القواعد الآن دائمًا مهما كان OID الخاص بها.

  المشكلة [#986](https://github.com/pgbackrest/pgbackrest/issues/986); طلب الدمج [#1307](https://github.com/pgbackrest/pgbackrest/pull/1307); الالتزام [`6942ff5`](https://github.com/pgbackrest/pgbackrest/commit/6942ff569dd950a5146faa0bebfee69e241c4179)
- استثناء `content-length` من الترويسات الموقعة في S3. (*راجعه Cynthia Shang. اقترحه Brian P Bockelman.*)

  تعدّل بعض الخوادم الوكيلة ترويسة `content-length`، مما كان يفشل المصادقة عندما تكون موقعة.

  المشكلة [#1340](https://github.com/pgbackrest/pgbackrest/issues/1340); طلب الدمج [#1341](https://github.com/pgbackrest/pgbackrest/pull/1341); الالتزام [`7d7ac0e`](https://github.com/pgbackrest/pgbackrest/commit/7d7ac0e0eb63a02bbc1dd8bd8fc89c6008c740f8)
- دمج خيارات تخزين المستودع الأقل شيوعًا. (*راجعه Cynthia Shang.*)

  أُعيدت تسمية خيارات CA والمضيف والمنفذ والتحقق من TLS لـ S3 وAzure إلى `repo-storage-*`، مثل تغيير `repo1-s3-host` إلى `repo1-storage-host`. لا تزال الأسماء القديمة مقبولة.

  طلب الدمج [#1321](https://github.com/pgbackrest/pgbackrest/pull/1321); الالتزام [`d1aa765`](https://github.com/pgbackrest/pgbackrest/commit/d1aa765a9d5f290738c1de00c5ea99d5f6056ba5)
- السماح بقيمة افتراضية مخصصة لـ `config-path` عبر `./configure --with-configdir`. (*ساهم به Michael Schout. راجعه David Steele.*)

  يمكن لمعدّي الحزم ضبط قيمة افتراضية مختلفة لـ `config-path` عند البناء. دون هذا الخيار، تظل القيمة الافتراضية `/etc/pgbackrest`.

  [`6a717e0`](https://github.com/pgbackrest/pgbackrest/commit/6a717e032f1309ddc9dc955042b5e2ac2bc7324d) تعيين مسار الإعداد في البرنامج النصي configure.

  [`9243962`](https://github.com/pgbackrest/pgbackrest/commit/9243962b9504787c6f4af42318af6dc27094136d) السماح بقيمة افتراضية مخصصة لـ config-path باستخدام ./configure --with-configdir.; المشكلة [#1251](https://github.com/pgbackrest/pgbackrest/issues/1251); المشكلة [#1293](https://github.com/pgbackrest/pgbackrest/issues/1293); طلب الدمج [#1255](https://github.com/pgbackrest/pgbackrest/pull/1255)
- تسجيل عملية نسخ الأرشيف أثناء `backup`. (*راجعه Cynthia Shang، Stefan Fercot.*)

  المشكلة [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); طلب الدمج [#1328](https://github.com/pgbackrest/pgbackrest/pull/1328); الالتزام [`c862e96`](https://github.com/pgbackrest/pgbackrest/commit/c862e9654aff198167efeb897957bf93c1afe453)

**تحسينات التوثيق:**

- تحديث المرجع ليتضمن روابط لأمثلة دليل المستخدم. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  يربط مرجع الأوامر الآن بأقسام دليل المستخدم ذات الأمثلة، ووُضحت بعض الأوصاف، مثل `set` للأمر `expire`.

  طلب الدمج [#1353](https://github.com/pgbackrest/pgbackrest/pull/1353); الالتزام [`d372dd6`](https://github.com/pgbackrest/pgbackrest/commit/d372dd652c9a01b72444998d87f0f44464676803)
- تحديث توثيق الاستعادة الانتقائية مع التنبيهات. (*راجعه Cynthia Shang، Stefan Fercot.*)

  قد يفشل الاسترداد ما لم يُحدد `type=immediate`، لأن PostgreSQL يُبلغ عن الصفحات المصفّرة كأخطاء بعد بلوغ الاتساق. على PostgreSQL >= 13 يمكن استخدام `ignore_invalid_pages`، لكن يجب فحص السجلات بحثًا عن صفحات غير صالحة في قواعد البيانات المحددة.

  المشكلة [#796](https://github.com/pgbackrest/pgbackrest/issues/796); طلب الدمج [#1329](https://github.com/pgbackrest/pgbackrest/pull/1329); الالتزام [`92d12cc`](https://github.com/pgbackrest/pgbackrest/commit/92d12ccb9bd0787e30441794e2a2a4d4a4e0fe9c)
- إضافة توضيح `compress-type` إلى توثيق `archive-copy`. (*راجعه Cynthia Shang، Stefan Fercot.*)

  يجب إعادة ضغط WAL عندما يستخدم `archive-push` و`backup` نوعين مختلفين من `compress-type`، وقد يكون ذلك مكلفًا.

  المشكلة [#1319](https://github.com/pgbackrest/pgbackrest/issues/1319); طلب الدمج [#1327](https://github.com/pgbackrest/pgbackrest/pull/1327); الالتزام [`9506ffa`](https://github.com/pgbackrest/pgbackrest/commit/9506ffae39dd86d2c5454511026f1249097d96a2)
- إضافة القيم الافتراضية لـ `compress-level` لكل قيمة `compress-type`. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  القيم الافتراضية هي 9 لـ `bz2` و6 لـ `gz` و1 لـ `lz4` و3 لـ `zst`.

  المشكلة [#1242](https://github.com/pgbackrest/pgbackrest/issues/1242); طلب الدمج [#1346](https://github.com/pgbackrest/pgbackrest/pull/1346); الالتزام [`3e20608`](https://github.com/pgbackrest/pgbackrest/commit/3e206088e79c4a73a20b8f2fda1706c6b95fa188)
- إضافة ملاحظة حول وجوب تطابق إعدادات NFS المطلوبة مع PostgreSQL. (*ساهم به Cynthia Shang. راجعه David Steele.*)

  المشكلة [#871](https://github.com/pgbackrest/pgbackrest/issues/871); طلب الدمج [#1347](https://github.com/pgbackrest/pgbackrest/pull/1347); الالتزام [`7598762`](https://github.com/pgbackrest/pgbackrest/commit/75987621fab5f57d0e95b42eabd301731587c438)

### ملاحظات إصدار v2.32 {#v232-release-notes}

*أوامر المستودع*

*صدر في 8 فبراير 2021*

**إصلاحات الأخطاء:**

- إصلاح الاستئناف بعد حذف جزئي للنسخة الاحتياطية بسبب استئناف سابق. (*راجعه Cynthia Shang. أبلغ عنه Tom Swartz.*)

**الميزات:**

- إضافة الأمر `repo-ls`. (*راجعه Cynthia Shang. اختبره Stefan Fercot.*)
- إضافة الأمر `repo-get`. (*ساهم به Stefan Fercot، David Steele. راجعه Cynthia Shang.*)
- إضافة خيار `archive-mode-check`. (*ساهم به Stefan Fercot. راجعه David Steele. اختبره Michael Banck.*)

**التحسينات:**

- تحسين أداء `archive-get`. (*راجعه Cynthia Shang.*)

**تحسينات التوثيق:**

- تحسين توثيق الأمر `expire`. (*ساهم به Cynthia Shang. راجعه David Steele.*)

### ملاحظات إصدار v2.31 {#v231-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 7 ديسمبر 2020*

**إصلاحات الأخطاء:**

- السماح بـ `[` و`#` و`space` كأول محرف في أسماء قواعد البيانات. (*راجعه Stefan Fercot، Cynthia Shang. أبلغ عنه Jefferson Alexandre.*)
- إنشاء `standby.signal` على PostgreSQL 12 فقط عندما يكون نوع `restore` هو `standby`. (*أصلحه Stefan Fercot. راجعه David Steele. أبلغ عنه Keith Fiske.*)

**الميزات:**

- إنهاء صلاحية الملفات التاريخية. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- الإبلاغ عن أخطاء مجموع تحقق الصفحات في المخرجات `text` للأمر `info`. (*ساهم به Stefan Fercot. راجعه Cynthia Shang.*)
- إضافة خيار `repo-azure-endpoint`. (*راجعه Cynthia Shang. اختبره Brian Peterson. اقترحه Brian Peterson.*)
- إضافة خيار `pg-database`. (*راجعه Cynthia Shang.*)

**التحسينات:**

- تحسين مخرجات الأمر `info` عندما تُحدَّد stanza غير موجودة. (*ساهم به Stefan Fercot. راجعه Cynthia Shang، David Steele. اقترحه uspen.*)
- تحسين أداء قوائم الملفات الكبيرة في الأمرين `backup`/`restore`. (*راجعه Cynthia Shang. اختبره Oscar.*)
- إضافة إعادة محاولة لسكون PostgreSQL عند بدء نسخة احتياطية. (*راجعه Cynthia Shang. اقترحه Vitaliy Kukharik.*)

**تحسينات التوثيق:**

- استبدال توثيق RHEL/CentOS 6 بتوثيق RHEL/CentOS 8.

### ملاحظات إصدار v2.30 {#v230-release-notes}

*دعم PostgreSQL 13*

*صدر في 5 أكتوبر 2020*

**إصلاحات الأخطاء:**

- إصدار خطأ مع تلميحات عندما لا يستطيع مستخدم النسخ الاحتياطي قراءة `pg_settings`. (*راجعه Stefan Fercot، Cynthia Shang. أبلغ عنه Mohamed Insaf K.*)

**الميزات:**

- دعم PostgreSQL 13. (*راجعه Cynthia Shang.*)

**التحسينات:**

- تحسين تحديد إصدار PostgreSQL. (*راجعه Cynthia Shang، Stephen Frost.*)
- تحسين رسالة خطأ دليل العمل. (*راجعه Stefan Fercot.*)
- إضافة تلميح حول بدء الـ stanza عند عدم العثور على مقطع WAL. (*ساهم به David Christensen. راجعه David Steele.*)
- إضافة تلميح لعدم تطابق إصدار البروتوكول. (*راجعه Cynthia Shang. اقترحه loop-evgeny.*)

**تحسينات التوثيق:**

- إضافة ملاحظة بأن إصدارات pgBackRest يجب أن تتطابق عند التشغيل عن بُعد. (*راجعه Cynthia Shang. اقترحه loop-evgeny.*)
- نقل نص أمر info إلى المرجع ووضع رابط لدليل المستخدم. (*راجعه Cynthia Shang. اقترحه Christophe Courtois.*)
- تحديث مسار مستودع yum لدليل مستخدم CentOS/RHEL. (*ساهم به Heath Lord. راجعه David Steele.*)


### ملاحظات إصدار v2.29 {#v229-release-notes}

*بيانات اعتماد S3 تلقائية على AWS*

*صدر في 31 أغسطس 2020*

**إصلاحات الأخطاء:**

- كتم الأخطاء عند إغلاق العمليات `local`/`remote`. بما أن الأمر اكتمل فإن إطلاق خطأ يؤدي إلى نتيجة عكسية، مع الاستمرار في إصدار **تحذير** للإشارة إلى حدوث شيء غير معتاد. (*راجعه Cynthia Shang. أبلغ عنه argdenis.*)
- إصلاح مشكلة محرف `=` في أسماء الملفات أو قواعد البيانات. (*راجعه Bastian Wegge، Cynthia Shang. أبلغ عنه Brad Nicholson، Bastian Wegge.*)

**الميزات:**

- استرجاع بيانات اعتماد S3 المؤقتة تلقائيًا على مثيلات AWS. (*ساهم به David Steele، Stephen Frost. راجعه Cynthia Shang، Aleš Zelený، Jeanette Bromage. اختبره David Youatt.*)
- إضافة خيار `archive-mode` لتعطيل الأرشفة عند الاستعادة. (*راجعه Stephen Frost. اقترحه Stephen Frost.*)

**التحسينات:**

- دعم PostgreSQL 13 beta3. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.
- `list`/`remove` غير المتزامنين لتخزين S3/Azure. (*راجعه Cynthia Shang، Stephen Frost.*)
- تحسين استخدام الذاكرة لاكتشاف العلاقات غير المسجلة عند بناء الـ manifest. (*راجعه Cynthia Shang، Stephen Frost، Oscar. اختبره Brad Nicholson. اقترحه Oscar، Brad Nicholson.*)
- إغلاق واصفات الملفات استباقيًا بعد تفريع العملية غير المتزامنة. (*راجعه Stephen Frost، Cynthia Shang.*)
- تأخير إغلاق اتصال النسخ الاحتياطي البعيد إلى ما بعد فحص الأرشيف. (*ساهم به Floris van Nee. راجعه David Steele.*)
- تحسين مخرجات الأخطاء التفصيلية. (*راجعه Cynthia Shang.*)
- تحسين الإبلاغ عن أخطاء TLS. (*راجعه Cynthia Shang، Stephen Frost.*)

**إصلاحات أخطاء التوثيق:**

- إضافة `none` إلى مرجع خيار `compress-type` وإصلاح المثال. (*أبلغ عنه Ugo Bellavance، Don Seiler.*)
- إضافة نوع `azure` المفقود في مرجع خيار `repo-type`. (*أصلحه Don Seiler. راجعه David Steele.*)
- إصلاح خطأ إملائي في مرجع خيار `repo-cipher-type`. (*أصلحه Don Seiler. راجعه David Steele.*)

**تحسينات التوثيق:**

- توضيح أنه يجب تشغيل `expire` بانتظام عندما يكون `expire-auto` معطلًا. (*راجعه Douglas J Hunley. اقترحه Douglas J Hunley.*)

### ملاحظات إصدار v2.28 {#v228-release-notes}

*تخزين المستودع على Azure*

*صدر في 20 يوليو 2020*

**إصلاحات الأخطاء:**

- إصلاح عمل `restore` مع `--force` كما لو كان `--force --delta`. تسبب ذلك في استبدال `restore` للملفات بناءً على الطابع الزمني والحجم بدلًا من الكتابة فوقها، ما يعني أن بعض الملفات التي كان ينبغي تحديثها تُركت دون تغيير. لم يتأثر `restore` العادي و`restore` مع `--delta` بهذه المشكلة. (*راجعه Cynthia Shang.*)

**الميزات:**

- دعم Azure لتخزين المستودع. (*راجعه Cynthia Shang. اختبره Don Seiler.*)
- إضافة خيار `expire-auto`. يتيح ذلك تعطيل الانتهاء التلقائي للصلاحية بعد نسخة احتياطية ناجحة. (*ساهم به Stefan Fercot. راجعه Cynthia Shang، David Steele.*)

**التحسينات:**

- الرفع متعدد الأجزاء غير المتزامن في S3. (*راجعه Stephen Frost.*)
- إعادة محاولة تلقائية للأوامر `backup` و`restore` و`archive-get` و`archive-push`. (*راجعه Cynthia Shang.*)
- تعطيل توازي الاستعلامات في جلسات PostgreSQL المستخدمة للتحكم في النسخ الاحتياطي. (*راجعه Stefan Fercot.*)
- دعم PostgreSQL 13 beta2. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.
- تحسين التعامل مع حالة استجابة HTTP غير الصالحة. (*راجعه Cynthia Shang.*)
- تحسين الخطأ عند غياب خيار `pg1-path` للأمر `archive-get`. (*راجعه Cynthia Shang.*)
- إضافة تلميح عند تمكين دلتا المجموع الاختباري بعد تبديل الخط الزمني. (*راجعه Matt Bunter، Cynthia Shang.*)
- استخدام PostgreSQL بدلًا من `postmaster` حيثما كان ذلك مناسبًا. (*راجعه Cynthia Shang.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح مثال غير صحيح لخيار `repo-retention-full-type`. (*أبلغ عنه Höseyin Sönmez.*)
- إزالة الأوامر الداخلية من مراجع الأوامر بصيغتي HTML وman. (*أبلغ عنه Cynthia Shang.*)

**تحسينات التوثيق:**

- تحديث إصدارات PostgreSQL المستخدمة لبناء أدلة المستخدم. كذلك إضافة نطاقات إصدارات للإشارة إلى أن دليل المستخدم دقيق لنطاق من إصدارات PostgreSQL حتى لو بُني لإصدار محدد. (*راجعه Stephen Frost.*)
- تحديث الأسئلة الشائعة حول إنهاء صلاحية مجموعة نسخ احتياطية محددة. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تحديث الأسئلة الشائعة لتوضيح سلوك PITR الافتراضي. (*ساهم به Cynthia Shang. راجعه David Steele.*)

### ملاحظات إصدار v2.27 {#v227-release-notes}

*تحسينات انتهاء الصلاحية ومشغّلات الضغط*

*صدر في 26 مايو 2020*

**إصلاحات الأخطاء:**

- إصلاح مشكلة فحص ما إذا كانت روابط الملفات محتواة في روابط المسارات. (*راجعه Cynthia Shang. أبلغ عنه Christophe Cavallié.*)
- السماح بأن يكون `pg-path1` اختياريًا لـ `archive-push` المتزامن. (*راجعه Cynthia Shang. أبلغ عنه Jerome Peng.*)
- يتحقق الأمر `expire` الآن من وجود ملف توقف. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- التعامل مع عبارة السبب المفقودة في استجابة HTTP. (*راجعه Cynthia Shang. أبلغ عنه Tenuun.*)
- زيادة حجم المخزن المؤقت لعملية التفريغ (flush) في ضغط lz4. (*راجعه Cynthia Shang. أبلغ عنه Eric Radman.*)
- تجاهل خيارات `pg-host*` و`repo-host*` للأمر `remote`. (*راجعه Cynthia Shang. أبلغ عنه Pavel Suderevsky.*)
- إصلاح احتمال نقص خيارات `pg1-*` للأمر `remote`. (*راجعه Cynthia Shang. أبلغ عنه Andrew L'Ecuyer.*)

**الميزات:**

- الاحتفاظ الزمني بالنسخ الاحتياطية الكاملة. يتيح خيار `--repo-retention-full-type` الاحتفاظ بالنسخ الاحتياطية الكاملة بناءً على فترة زمنية محددة بالأيام. (*ساهم به Cynthia Shang، Pierre Ducroquet. راجعه David Steele.*)
- إنهاء صلاحية النسخ الاحتياطية عند الطلب. يتيح للمستخدم إزالة نسخة احتياطية محددة بغض النظر عن إعدادات الاحتفاظ. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- دعم ضغط Zstandard. لاحظ أن تعيين `compress-type=zst` سيجعل النسخ الاحتياطية والأرشيف الجديدة غير متوافقة (غير قابلة للاستعادة) مع الإصدارات السابقة من pgBackRest. (*راجعه Cynthia Shang.*)
- دعم ضغط bzip2. لاحظ أن تعيين `compress-type=bz2` سيجعل النسخ الاحتياطية والأرشيف الجديدة غير متوافقة (غير قابلة للاستعادة) مع الإصدارات السابقة من pgBackRest. (*ساهم به Stephen Frost. راجعه David Steele، Cynthia Shang.*)
- إضافة حالة تشغيل `backup`/`expire` إلى الأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

**التحسينات:**

- إنهاء صلاحية أرشيف WAL فقط عند استيفاء حد `repo-retention-archive`. كان WAL السابق لأول نسخة احتياطية كاملة تُنهى صلاحيته بعد أول نسخة كاملة سابقًا. أما الآن فيُحفظ وفق إعدادات الاحتفاظ. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة تنفيذ محلي لخوارزمية MD5 ليعمل S3 عند تمكين FIPS. (*راجعه Cynthia Shang، Stephen Frost. اقترحه Brian Almeida، John Kelly.*)
- دعم PostgreSQL 13 beta1. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك. (*راجعه Cynthia Shang.*)
- تخفيض القيمة الافتراضية لـ `buffer-size` إلى `1MiB`. (*راجعه Stephen Frost.*)
- إطلاق خطأ ودي للمستخدم إذا لم يُشغَّل `expire` على مضيف المستودع. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v2.26 {#v226-release-notes}

*TLS غير الحاجب*

*صدر في 20 أبريل 2020*

**إصلاحات الأخطاء:**

- إزالة التعبير الفرعي الفارغ من التعابير النمطية للـ manifest. لم تكن MacOS راضية عن ذلك رغم أن المنصات الأخرى بدت تعمل جيدًا. (*أصلحه David Raftis. راجعه David Steele.*)

**التحسينات:**

- تنفيذ TLS غير الحاجب. (*راجعه Cynthia Shang، Stephen Frost. اختبره Slava Moudry.*)
- قصر تحديد حجم النسخ على الملفات المسجلة في WAL فقط. كان السلوك السابق قد يؤدي إلى اقتطاع `postgresql.conf` أو `postgresql.auto.conf` في النسخة الاحتياطية. (*راجعه Cynthia Shang.*)
- خيارات keep-alive لـ TCP قابلة للإعداد. (*اقترحه Marc Cousin.*)
- إضافة خيار `io-timeout`. (*راجعه Cynthia Shang.*)

### ملاحظات إصدار v2.25 {#v225-release-notes}

*دعم ضغط LZ4*

*صدر في 26 مارس 2020*

**الميزات:**

- إضافة دعم ضغط lz4. لاحظ أن تعيين `compress-type=lz4` سيجعل النسخ الاحتياطية والأرشيف الجديدة غير متوافقة (غير قابلة للاستعادة) مع الإصدارات السابقة من pgBackRest. (*راجعه Cynthia Shang.*)
- إضافة خيار `--dry-run` إلى الأمر `expire`. استخدم dry-run لمعرفة النسخ الاحتياطية/الأرشيف التي سيزيلها الأمر `expire` دون إزالة أي شيء فعليًا. (*ساهم به Cynthia Shang، Luca Ferrari. راجعه David Steele. اقترحه Marc Cousin.*)

**التحسينات:**

- تحسين أداء بناء الـ manifest البعيد. (*اقترحه Jens Wilke.*)
- إصلاح اكتشاف خيارات keepalive على Linux. (*ساهم به Marc Cousin. راجعه David Steele.*)
- إضافة اكتشاف مضيف configure لتعيين علامات المعايير بشكل صحيح. (*ساهم به Marc Cousin. راجعه David Steele.*)
- إزالة خياري `compress`/`compress-level` من الأوامر التي لا تستخدمها. هذه الأوامر (مثل `restore` و`archive-get`) لم تستخدم خيارات الضغط قط لكنها سمحت بتمريرها في سطر الأوامر. ستُصدر الآن خطأً عند تمرير هذه الخيارات في سطر الأوامر. إذا حدثت هذه الأخطاء فأزل الخيارات غير المستخدمة. (*راجعه Cynthia Shang.*)
- قصر حجم نسخ ملف النسخة الاحتياطية على الحجم المُبلَّغ عنه عند بدء النسخ. إذا نما ملف أثناء النسخ الاحتياطي فسيُعاد بناؤه عبر إعادة تشغيل WAL أثناء الاسترداد لذا لا حاجة لنسخ البيانات الإضافية. (*راجعه Cynthia Shang.*)


### ملاحظات إصدار v2.24 {#v224-release-notes}

*الاختيار التلقائي لمجموعة النسخ الاحتياطية للهدف الزمني*

*صدر في 25 فبراير 2020*

**إصلاحات الأخطاء:**

- منع العمليات الميتة في أوامر الأرشفة غير المتزامنة. (*راجعه Stephen Frost. أبلغ عنه Adam Brusselback، ejberdecia.*)
- إصدار خطأ عندما لا تُشغَّل `archive-get`/`archive-push`/`restore` على مضيف PostgreSQL. (*راجعه Stephen Frost. أبلغ عنه Jesper St John.*)
- قراءة محتوى HTTP حتى eof عند عدم تحديد الحجم/الترميز. (*راجعه Cynthia Shang. أبلغ عنه Christian ROUX.*)
- إصلاح الاستئناف عندما تكون النسخة الاحتياطية القابلة للاستئناف قد أُنشئت بواسطة Perl. في هذه الحالة يجب تجاهل النسخة القابلة للاستئناف، لكن شيفرة C لم تكن قادرة على تحميل الـ manifest الجزئي الذي كتبه Perl لأن التنسيق يختلف قليلًا. أُضيفت فحوصات صلاحية لالتقاط هذه الحالة والمتابعة بسلاسة. (*أبلغ عنه Kacey Holston.*)

**الميزات:**

- الاختيار التلقائي لمجموعة النسخ الاحتياطية عند الاستعادة عندما يُحدَّد هدف زمني. يُنفَّذ الاختيار التلقائي فقط عندما لا يكون `--set` محددًا. إذا تعذر العثور على مجموعة نسخ احتياطية للوقت الهدف المعطى فستُستخدم مجموعة النسخ الاحتياطية الأحدث (الافتراضية). (*ساهم به Cynthia Shang. راجعه David Steele.*)

**التحسينات:**

- تخطي الملف المؤقت `pg_internal.init` أثناء النسخ الاحتياطي. (*راجعه Cynthia Shang. اقترحه Michael Paquier.*)
- إضافة مزيد من فحوصات الصلاحية إلى الـ manifest عند `backup`. (*راجعه Cynthia Shang.*)

**تحسينات التوثيق:**

- منع lock-bot من إضافة تعليقات إلى المشكلات المقفلة. (*اقترحه Christoph Berg.*)


### ملاحظات إصدار v2.23 {#v223-release-notes}

*إصلاح خطأ*

*صدر في 27 يناير 2020*

**إصلاحات الأخطاء:**

- إصلاح إفساد الملفات المفقودة للـ manifest. إذا أزال PostgreSQL ملفًا أثناء النسخ الاحتياطي (أو كان مفقودًا من خادم الاستعداد) فقد لا يُنسخ الملف التالي ولا يُحدَّث في الـ manifest. إذا حدث ذلك فستخطئ النسخة الاحتياطية عند استعادتها. (*راجعه Cynthia Shang. أبلغ عنه Vitaliy Kukharik.*)

**التحسينات:**

- استخدام `pkg-config` بدلًا من `xml2-config` لخيارات بناء libxml2. (*ساهم به David Steele، Adrian Vondendriesch.*)
- التحقق من تعيين المجاميع الاختبارية في الـ manifest عند `backup`/`restore`. (*راجعه Cynthia Shang.*)


### ملاحظات إصدار v2.22 {#v222-release-notes}

*إصلاح خطأ*

*صدر في 21 يناير 2020*

**إصلاحات الأخطاء:**

- إصلاح خطأ في تحويل الخط الزمني. الخط الزمني مطلوب للتحقق من مقاطع WAL في الأرشيف بعد نسخة احتياطية. كان التحويل يجري على الأساس `10` بدلًا من `16`، ما أدى إلى أخطاء عندما يكون الخط الزمني ≥ `0xA`. (*أبلغ عنه Lukas Ertl، Eric Veldhuyzen.*)


### ملاحظات إصدار v2.21 {#v221-release-notes}

*اكتمال الترحيل إلى C*

*صدر في 15 يناير 2020*

**إصلاحات الأخطاء:**

- إصلاح تجاهل الخيارات بواسطة الأوامر غير المتزامنة. لم تكن عمليات `archive-get`/`archive-push` غير المتزامنة تحمّل الخيارات المُعدّة في أقسام إعداد الأوامر، مثل `[global:archive-get]`. (*راجعه Cynthia Shang. أبلغ عنه Urs Kramer.*)
- إصلاح التعامل مع `\` في أسماء الملفات. لم تكن `\` تُهرَّب بشكل صحيح عند حساب المجموع الاختباري للـ manifest ما منع تحميل الـ manifest. وبما أن حالات `\` في أسماء ملفات العنقود ينبغي أن تكون نادرة إلى معدومة فلا يبدو أن هذه مشكلة خطيرة ميدانيًا.

**الميزات:**

- أصبح pgBackRest الآن بلغة C خالصة.
- إضافة خيار `pg-user`. يحدد اسم مستخدم قاعدة البيانات عند الاتصال بـ PostgreSQL. إذا لم يُحدَّد فسيتصل pgBackRest بمستخدم نظام التشغيل المحلي أو `PGUSER`، وهو السلوك السابق. (*ساهم به Mike Palmiotto. راجعه David Steele.*)
- السماح بـ URI بنمط المسار في مشغّل S3.

**التحسينات:**

- الأمر `backup` منفَّذ بالكامل بلغة C. (*راجعه Cynthia Shang.*)


### ملاحظات إصدار v2.20 {#v220-release-notes}

*إصلاحات أخطاء*

*صدر في 12 ديسمبر 2019*

**إصلاحات الأخطاء:**

- إصلاح archive-push/archive-get عندما يكون `PGDATA` رابطًا رمزيًا. حاولت هذه الأوامر استخدام `cwd()` كـ`PGDATA` لكن ذلك يتعارض مع المسار المُعد في pgBackRest إذا كان `PGDATA` رابطًا رمزيًا. إذا لم يطابق `cwd()` مسار pgBackRest فسيُجرى `chdir()` إلى المسار والتأكد من أن `cwd()` التالية تطابق نتيجة الاستدعاء الأول. (*أبلغ عنه Stephen Frost، Milosz Suchy.*)
- إصلاح قائمة المراجع عند إعادة بناء `backup.info` في الأمر `expire`. بما أن الأمر `backup` لا يزال يستخدم نسخة Perl من إعادة البناء فلن تظهر هذه المشكلة إلا إذا **1)** كانت هناك نسخة احتياطية مفقودة من `backup.info` و**2)** شُغِّل الأمر `expire` مباشرة بدلًا من تشغيله بعد `backup` كالمعتاد. هذا التركيب غير المرجح من الأحداث يعني أن هذه على الأرجح ليست مشكلة ميدانيًا.
- إصلاح خطأ تقسيم عند EOF غير متوقع في فك ضغط gzip. (*أبلغ عنه Stephen Frost.*)


### ملاحظات إصدار v2.19 {#v219-release-notes}

*ترحيلات إلى C وإصلاحات أخطاء*

*صدر في 12 نوفمبر 2019*

**إصلاحات الأخطاء:**

- إصلاح انتهاء مهلة الطرف البعيد في استعادة الدلتا. عند تنفيذ استعادة دلتا على عنقود لم يتغير إلى حد كبير قد تنتهي مهلة الطرف البعيد إذا لم تُجلب ملفات من المستودع خلال `protocol-timeout`. أُضيفت رسائل keep-alive لمنع انتهاء مهلة الطرف البعيد. (*أبلغ عنه James Sewell، Jens Wilke.*)
- إصلاح التعامل مع ترويسات HTTP المكررة. عندما تتكرر ترويسات HTTP ينبغي اعتبارها مكافئة لترويسة واحدة مفصولة بفواصل بدلًا من توليد خطأ، وهو ما كان السلوك السابق. (*أبلغ عنه donicrosby.*)

**التحسينات:**

- مخرجات JSON من الأمر `info` لم تعد منسّقة للعرض. يمكن لأنظمة المراقبة استيعاب JSON دون أسطر جديدة بسهولة أكبر. يمكن استخدام أدوات خارجية مثل `jq` للتنسيق للعرض عند الحاجة. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- الأمر `check` منفَّذ بالكامل بلغة C. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**تحسينات التوثيق:**

- توثيق كيفية المساهمة في pgBackRest. (*ساهم به Cynthia Shang، David Steele.*)
- توثيق الحد الأقصى للإصدار لخيار `auto-stop`. (*ساهم به Brad Nicholson. راجعه David Steele.*)

**تحسينات مجموعة الاختبارات:**

- إصلاح استخدام مسار اختبار الحاوية عندما يكون `--vm=none`. (*اقترحه Stephen Frost.*)
- إصلاح عدم تطابق المنطقة الزمنية في اختبار expect. (*اقترحه Stephen Frost.*)
- عدم توليد شيفرة libc المضمّنة تلقائيًا افتراضيًا. (*اقترحه Stephen Frost.*)


### ملاحظات إصدار v2.18 {#v218-release-notes}

*دعم PostgreSQL 12*

*صدر في 1 أكتوبر 2019*

**الميزات:**

- دعم PostgreSQL 12.
- إضافة خيار `set` للأمر `info` للمخرجات النصية المفصلة. تشمل التفاصيل الإضافية قواعد البيانات التي يمكن استخدامها للاستعادة الانتقائية وقائمة بمساحات الجداول والروابط الرمزية مع وجهاتها الافتراضية. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Stephen Frost، ejberdecia.*)
- إضافة نوع استعادة `standby`. يضيف نوع الاستعادة هذا تلقائيًا standby_mode=on إلى recovery.conf لـ PostgreSQL < 12 وينشئ `standby.signal` لـ PostgreSQL ≥ 12، منشئًا بذلك واجهة موحدة بين إصدارات PostgreSQL. (*راجعه Cynthia Shang.*)

**التحسينات:**

- الأمر `restore` منفَّذ بالكامل بلغة C. (*راجعه Cynthia Shang.*)

**تحسينات التوثيق:**

- توثيق العلاقة بين `db-timeout` و`protocol-timeout`. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه James Chanco Jr.*)
- إضافة توضيحات توثيقية بشأن مستودعات خوادم الاستعداد. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة أسئلة شائعة حول الاسترداد إلى نقطة زمنية القائم على الوقت. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v2.17 {#v217-release-notes}

*ترحيلات إلى C وإصلاحات أخطاء*

*صدر في 3 سبتمبر 2019*

**إصلاحات الأخطاء:**

- تحسين بطء بناء الـ manifest لكميات كبيرة جدًا من الجداول/المقاطع. (*أبلغ عنه Jens Wilke.*)
- إصلاح الاستثناءات للملفات الخاصة. (*أبلغ عنه CluelessTechnologist، Janis Puris، Rachid Broum.*)

**التحسينات:**

- الأوامر `stanza-create/update/delete` منفَّذة بالكامل بلغة C. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- الأمران `start`/`stop` منفَّذان بالكامل بلغة C. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إنشاء أدلة/ملفات السجلات بوضع `0750`/`0640`. (*اقترحه Damiano Albani.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح تثبيت حزمة `yum.p.o` عند تحديد حزمة مخصصة. (*أبلغ عنه Joe Ayers، John Harvey.*)

**تحسينات التوثيق:**

- بناء pgBackRest بصفة مستخدم دون صلاحيات إدارية. (*اقترحه Laurenz Albe.*)


### ملاحظات إصدار v2.16 {#v216-release-notes}

*ترحيلات إلى C وإصلاحات أخطاء*

*صدر في 5 أغسطس 2019*

**إصلاحات الأخطاء:**

- إعادة محاولة أخطاء `RequestTimeTooSkewed` في S3 بدلًا من الإنهاء الفوري. (*أبلغ عنه sean0101n، Tim Garton، Jesper St John، Aleš Zelený.*)
- إصلاح التعامل غير الصحيح مع استجابة `transfer-encoding` لطلب `HEAD`. (*أبلغ عنه Pavel Suderevsky.*)
- إصلاح انتهاكات النطاق التي كشفتها تحسينات gcc 9. (*أبلغ عنه Christian Lange، Ned T. Crigler.*)

**الميزات:**

- إضافة خيار `repo-s3-port` لتعيين منفذ خدمة S3 غير قياسي.

**التحسينات:**

- الأمر `local` لـ`backup` منفَّذ بالكامل بلغة C. (*ساهم به David Steele، Cynthia Shang.*)
- الأمر `check` منفَّذ جزئيًا بلغة C. (*راجعه Cynthia Shang.*)


### ملاحظات إصدار v2.15 {#v215-release-notes}

*تنفيذ expire بلغة C*

*صدر في 25 يونيو 2019*

**إصلاحات الأخطاء:**

- إصلاح احتفاظ الأرشيف الذي يُنهي الصلاحية بعدوانية أكثر من اللازم. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Mohamad El-Rifai.*)

**التحسينات:**

- الأمر `expire` منفَّذ بالكامل بلغة C. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- الأمر `local` للاستعادة منفَّذ بالكامل بلغة C.
- إزالة مستخدم PostgreSQL المرمّز بشكل ثابت ليعمل `$PGUSER`. (*اقترحه Julian Zhang، Janis Puris.*)
- احترام خيار `--prefix` في configure. (*اقترحه Daniel Westermann.*)
- إعادة تسمية خيار `repo-s3-verify-ssl` إلى `repo-s3-verify-tls`. الاسم الجديد مفضل لأن pgBackRest لا يدعم أي إصدارات من بروتوكول SSL (تُعتبر جميعها غير آمنة). سيستمر قبول الاسم القديم.

**تحسينات التوثيق:**

- إضافة أسئلة شائعة إلى التوثيق. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- استخدام `wal_level=replica` في التوثيق لـ PostgreSQL ≥ 9.6. (*اقترحه Patrick McLaughlin.*)


### ملاحظات إصدار v2.14 {#v214-release-notes}

*إصلاح خطأ وتحسينات*

*صدر في 20 مايو 2019*

**إصلاحات الأخطاء:**

- إصلاح خطأ تقسيم عندما يكون `process-max` > 8 لـ`archive-push`/`archive-get`. (*أبلغ عنه Jens Wilke.*)

**التحسينات:**

- تجاوز فحوصات قاعدة البيانات عند إصدار `stanza-delete` مع `force`. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه hatifnatt.*)
- إضافة سكربت `configure` لتحسين دعم المنصات المتعددة.

**ميزات التوثيق:**

- إضافة أدلة مستخدم لـ CentOS/RHEL 6/7.


### ملاحظات إصدار v2.13 {#v213-release-notes}

*إصلاحات أخطاء*

*صدر في 18 أبريل 2019*

**إصلاحات الأخطاء:**

- إصلاح القراءات ذات الطول الصفري التي تسبب مشكلات لمرشّحات الإدخال/الإخراج التي لم تتوقعها. (*أبلغ عنه brunre01، Jens Wilke، Tomasz Kontusz، guruguruguru.*)
- إصلاح موثوقية الإبلاغ عن الأخطاء من العمليات `local`/`remote`.
- إصلاح رسائل أخطاء Posix/CIFS التي تبلغ عن اسم ملف خاطئ عند الكتابة/المزامنة/الإغلاق.


### ملاحظات إصدار v2.12 {#v212-release-notes}

*تنفيذ archive-push بلغة C*

*صدر في 11 أبريل 2019*

**ملاحظة هامة**: يمنع تنفيذ TLS/SSL الجديد النقاط في أسماء حاويات S3 وفق RFC-2818. إصلاح أمني مطلوب للتحقق المتوافق من اسم المضيف.

**إصلاحات الأخطاء:**

- إصلاح مشكلات عندما ينتهي خيار مسار بـ /. (*أبلغ عنه Marc Cousin.*)
- إصلاح مشكلات عند تعيين `log-level-file=off` للأمر `archive-get`. (*أبلغ عنه Brad Nicholson.*)
- إصلاح شيفرة C للتعرف على تنسيق خيار `host:port` كما تفعل Perl. (*أبلغ عنه Kyle Nevins.*)
- إصلاح مشكلات خيارات التسجيل للأمرين `remote`/`local`.

**التحسينات:**

- الأمر `archive-push` منفَّذ بالكامل بلغة C.
- زيادة حد `process-max` إلى `999`. (*اقترحه Rakshitha-BR.*)
- تحسين رسالة الخطأ عندما يحتوي اسم حاوية S3 على نقاط.

**تحسينات التوثيق:**

- توضيح أن مخازن الكائنات المتوافقة مع S3 مدعومة. (*اقترحه Magnus Hagander.*)


### ملاحظات إصدار v2.11 {#v211-release-notes}

*تنفيذ archive-get بلغة C*

*صدر في 11 مارس 2019*

**إصلاحات الأخطاء:**

- إصلاح احتمال اقتطاع مقاطع WAL عندما يحدث خطأ في منتصف الكتابة. (*أبلغ عنه blogh.*)
- إصلاح فقدان الحد الأدنى/الأقصى لـ WAL في أمر info عند تحديد stanza. (*أصلحه Stefan Fercot. راجعه David Steele.*)
- إصلاح JSON غير المتوافق للخيارات المنتقلة من C إلى Perl. (*أبلغ عنه Leo Khomenko.*)

**التحسينات:**

- الأمر `archive-get` منفَّذ بالكامل بلغة C.
- تمكين keep-alive للمقابس في إصدارات Perl الأقدم. (*ساهم به Marc Cousin. راجعه David Steele.*)
- إصدار خطأ عند تمرير وسائط إلى أمر لا يقبل الوسائط. (*اقترحه Jason O'Donnell.*)
- إضافة تلميحات عند تعذر العثور على مقطع WAL في الأرشيف. (*اقترحه Hans-Jürgen Schönig.*)
- تحسين الخطأ عند تعذر العثور على اسم المضيف في شهادة. (*اقترحه James Badger.*)
- إضافة خيارات إضافية إلى `backup.manifest` لأغراض التنقيح. (*ساهم به blogh. راجعه David Steele.*)

**تحسينات التوثيق:**

- تحديث إصدار التوثيق الافتراضي إلى PostgreSQL 10.


### ملاحظات إصدار v2.10 {#v210-release-notes}

*إصلاحات أخطاء*

*صدر في 9 فبراير 2019*

**إصلاحات الأخطاء:**

- إضافة طريقة مشغّل S3 غير منفَّذة كانت مطلوبة لـ`archive-get`. (*أبلغ عنه mibiio.*)
- إصلاح الفحص لـ`pg-path` المُعد بشكل غير صحيح. (*أبلغ عنه James Chanco Jr.*)


### ملاحظات إصدار v2.09 {#v209-release-notes}

*تحسينات ثانوية وإصلاحات أخطاء*

*صدر في 30 يناير 2019*

**إصلاحات الأخطاء:**

- إصلاح مشكلة ملفات حالة غير متزامنة متعددة تسبب خطأً فادحًا. (*أبلغ عنه Vidhya Gurumoorthi، Joe Ayers، Douglas J Hunley.*)

**التحسينات:**

- الأمر `info` منفَّذ بالكامل بلغة C. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تبسيط الرسالة النصية للأمر `info` عندما لا توجد stanza. استبدال مسار المستودع بعبارة "the repository".
- إضافة علامة `_DARWIN_C_SOURCE` إلى Makefile لبناء MacOS. (*ساهم به Douglas J Hunley. راجعه David Steele.*)
- تحديث البحث عن العناوين في عميل TLS بلغة C لاستخدام طرق حديثة. (*اقترحه Bruno Friedmann.*)
- تضمين ترويسة متوافقة مع Posix من أجل `strcasecmp()` و`fd_set`. (*اقترحه ucando.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح مسار المستودع المرمّز بشكل ثابت. (*أبلغ عنه Heath Lord.*)

**تحسينات التوثيق:**

- توضيح أن التشفير يجري دائمًا من جانب العميل. (*اقترحه Bruce Burdick.*)
- إضافة أمثلة لبناء مضيف توثيق.
- السماح بـ `if` في متغيرات الـ manifest وقوائمه وعناصر قوائمه.


### ملاحظات إصدار v2.08 {#v208-release-notes}

*تحسينات ثانوية وإصلاحات أخطاء*

*صدر في 2 يناير 2019*

**إصلاحات الأخطاء:**

- إزالة طلب معلومات كائن S3 مباشرة بعد وضعه. (*أبلغ عنه Matt Kunkel.*)
- تصحيح `archive-get-queue-max` ليكون من النوع `size`. (*أبلغ عنه Ronan Dunklau.*)
- إضافة رسالة خطأ عندما لا يقابل `uid`/`gid` للمستخدم الحالي اسمًا. (*أبلغ عنه Camilo Aguilar.*)
- إصدار خطأ عند تحديد `--target-action=shutdown` لـ PostgreSQL < 9.5.

**التحسينات:**

- تعيين keepalives لـ TCP على اتصالات S3. (*اقترحه Ronan Dunklau.*)
- إعادة ترتيب المخرجات النصية للأمر `info` بحيث تُخرج أحدث نسخة احتياطية أخيرًا. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Ryan Lambert.*)
- تغيير ملكية الملفات فقط عند الحاجة.
- حجب ترويسة `authentication` عند إطلاق أخطاء S3. (*اقترحه Brad Nicholson.*)

**تحسينات التوثيق:**

- توضيح متى يسري `target-action` ودعم إصدارات PostgreSQL. (*اقترحه Keith Fiske.*)
- توضيح أنه يجب إعداد المنطقة/نقطة النهاية بشكل صحيح للحاوية. (*اقترحه Pritam Barhate.*)
- إضافة توثيق لبناء التوثيق.


### ملاحظات إصدار v2.07 {#v207-release-notes}

*دلتا المجموع الاختباري التلقائية للنسخ الاحتياطية*

*صدر في 16 نوفمبر 2018*

**إصلاحات الأخطاء:**

- إصلاح مشكلة عدم احترام `archive-push-queue-max` عند خطأ الاتصال. (*أبلغ عنه Lardière Sébastien.*)
- إصلاح حجم مقطع WAL الثابت المستخدم لتحديد ما إذا تم تجاوز `archive-push-queue-max`.
- إصلاح خطأ بعد فشل فتح ملف السجل عندما ينبغي أن تستمر المعالجة. (*أبلغ عنه vthriller.*)

**الميزات:**

- تمكين دلتا المجموع الاختباري للنسخ الاحتياطي تلقائيًا عند اكتشاف شذوذات (مثل تبديل الخط الزمني). (*ساهم به Cynthia Shang. راجعه David Steele.*)

**التحسينات:**

- إعادة محاولة جميع أخطاء `5xx` في S3 بدلًا من أخطاء `500` الداخلية فقط. (*اقترحه Craig A. James.*)


### ملاحظات إصدار v2.06 {#v206-release-notes}

*النسخ الاحتياطي بدلتا المجموع الاختباري ودعم PostgreSQL 11*

*صدر في 15 أكتوبر 2018*

**إصلاحات الأخطاء:**

- إصلاح نقص ترميز URI في مشغّل S3. (*أبلغ عنه Dan Farrell.*)
- إصلاح رسالة خطأ غير صحيحة للخيارات المكررة في ملفات الإعداد. (*أبلغ عنه Jesper St John.*)
- إصلاح إرجاع خطأ مُبلَّغ عنه بشكل خاطئ في تسجيل `info`. كان رمز الإرجاع 1 من `archive-get` يُسجَّل كرسالة خطأ على مستوى `info` لكنه كان يعمل بشكل صحيح خلاف ذلك.

**الميزات:**

- إضافة دلتا المجموع الاختباري للنسخ الاحتياطية التزايدية. تستخدم النسخ الاحتياطية بدلتا المجموع الاختباري المجاميع الاختبارية بدلًا من الطوابع الزمنية لتحديد ما إذا كانت الملفات قد تغيرت. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- دعم PostgreSQL 11، بما في ذلك حجم مقطع WAL قابل للإعداد.

**التحسينات:**

- تجاهل جميع الملفات في دليل مساحة جداول مرتبط عدا الدليل الفرعي الخاص بإصدار PostgreSQL الحالي. سابقًا كان يُولَّد خطأ إذا كانت هناك ملفات أخرى موجودة ولا يملكها مستخدم PostgreSQL.
- تحسين الأمر `info` لعرض نوع التشفير للـ stanza. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Douglas J Hunley.*)
- تحسين دعم المحارف الخاصة في أسماء الملفات.
- السماح بتحديد خيار `delta` في ملف إعداد pgBackRest. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**تحسينات التوثيق:**

- استخدام `command` في `authorized_hosts` لتحسين أمان SSH. (*اقترحه Stephen Frost، Magnus Hagander.*)
- إدراج القيم المسموح بها لخيار `buffer-size` في مرجع الإعداد. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Stéphane Schildknecht.*)


### ملاحظات إصدار v2.05 {#v205-release-notes}

*خيارات متغيرات البيئة واستبعاد العلاقات المؤقتة/غير المسجلة*

*صدر في 31 أغسطس 2018*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يمكن فيها أن تُخزَّن الروابط *النسبية* في `$PGDATA` في النسخة الاحتياطية بالمسار الخاطئ. لم تؤثر هذه المشكلة في الروابط المطلقة، وكانت روابط مساحات الجداول النسبية تُكتشف بفحوصات أخرى. (*أبلغ عنه Cynthia Shang.*)
- إزالة خيار `online` المنفَّذ بشكل غير كامل من الأمر `check`. يتعارض العمل أثناء توقف PostgreSQL مع الغرض من هذا الأمر، وهو التحقق مما إذا كانت الأرشفة والنسخ الاحتياطي يعملان بشكل صحيح. (*أبلغ عنه Jason O'Donnell.*)
- إصلاح مشكلة عدم تسجيل الأخطاء الصادرة من C عند استدعائها من Perl. كان pgBackRest ينتهي بشكل صحيح برمز الخطأ الصحيح لكنه يفتقر إلى رسالة خطأ تساعد في التنقيح. (*أبلغ عنه Douglas J Hunley.*)
- إصلاح مشكلة عند تحديد خيار منطقي (مثل `delta`) أكثر من مرة. (*أبلغ عنه Yogesh Sharma.*)

**الميزات:**

- السماح بتعيين أي خيار في متغير بيئة. يشمل ذلك الخيارات التي كان يمكن سابقًا تحديدها في سطر الأوامر فقط، مثل `stanza`، والخيارات السرية التي لم يكن يمكن تحديدها في سطر الأوامر، مثل `repo1-s3-key-secret`.
- استبعاد ملفات العلاقات (الجداول/الفهارس) المؤقتة وغير المسجلة من النسخ الاحتياطي. نُفِّذ باستخدام نفس منطق الرقعتين اللتين أضافتا هذه الميزة إلى PostgreSQL، [8694cc96](https://git.postgresql.org/pg/commitdiff/8694cc96b52a967a49725f32be7aa77fd3b6ac25) و[920a5e50](https://git.postgresql.org/pg/commitdiff/920a5e500a119b03356fb1fb64a677eb1aa5fc6f). يُمكَّن استبعاد العلاقات المؤقتة في PostgreSQL ≥ `9.0`. يُمكَّن استبعاد العلاقات غير المسجلة في PostgreSQL ≥ `9.1`، حيث قُدِّمت الميزة. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- السماح باستبعاد أدلة و/أو ملفات يختارها المستخدم من نسخة احتياطية. يمكن أن يؤدي سوء استخدام هذه الميزة إلى نسخ احتياطية غير متسقة لذا اقرأ توثيق `--exclude` بعناية قبل الاستخدام. (*راجعه Cynthia Shang.*)
- إضافة خيار `log-subprocess` للسماح بالتسجيل في ملف للعمليات الفرعية `local` و`remote`.
- دعم PostgreSQL 11 Beta 3.

**التحسينات:**

- السماح للملفات ذات الحجم الصفري في manifest النسخ الاحتياطي بالإشارة إلى manifest سابق بغض النظر عن فرق الطابع الزمني. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تحسين أداء `archive-get`/`archive-push` غير المتزامنين عبر فحص ملفات الحالة مباشرة. (*ساهم به Stephen Frost. راجعه David Steele.*)
- تحسين رسالة الخطأ عندما ينقص الأمر خيار `stanza`. (*اقترحه Sarah Conway.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح مستوى سجل غير صالح في مرجع خيار `log-path`. (*أبلغ عنه Camilo Aguilar.*)

**تحسينات التوثيق:**

- التوقف عن محاولة ترتيب المساهمين في `release.xml` حسب الاسم الأخير/الأول. كانت أسماء المساهمين تُعرض دائمًا في ملاحظات الإصدار كما أُعطيت تمامًا، لكننا حاولنا تعيين معرفات داخلية بناءً على الاسم الأخير/الأول وهو ما قد يصعب تحديده ولا معنى له في النهاية. مستوحى من محاضرة Christophe في PostgresOpen 2017 بعنوان "Human Beings Do Not Have a Primary Key". (*اقترحه Christophe Pettus.*)

**تحسينات مجموعة الاختبارات:**

- إصدار خطأ إذا جرى بناء LibC خارج بيئة الاختبار. لم تعد LibC مطلوبة لبناءات الإنتاج.


### ملاحظات إصدار v2.04 {#v204-release-notes}

*إصلاح خطأ حرج لاستئناف النسخ الاحتياطي*

*صدر في 5 يوليو 2018*

**ملاحظة هامة**: يصلح هذا الإصدار خطأً حرجًا في ميزة استئناف النسخ الاحتياطي. ينبغي اعتبار جميع النسخ الاحتياطية المستأنفة قبل هذا الإصدار غير متسقة. ستُستأنف نسخة احتياطية بعد فشل نسخة سابقة، ما لم يكن `resume=n` محددًا. يمكن تحديد النسخة الاحتياطية المستأنفة بفحص سجل النسخ الاحتياطي عن الرسالة "aborted backup of same type exists, will be cleaned to remove invalid files and resumed". إذا كانت الرسالة موجودة فلا تستخدم هذه النسخة الاحتياطية أو أي نسخة في نفس المجموعة للاستعادة، وافحص سجلات الاستعادة لمعرفة ما إذا كانت نسخة مستأنفة قد استُعيدت. إن كان كذلك فقد تكون هناك بيانات غير متسقة في العنقود.

**إصلاحات الأخطاء:**

- إصلاح خطأ حرج في الاستئناف أدى إلى نسخ احتياطية غير متسقة. أزال تراجع في `v0.82` مقارنة الطوابع الزمنية عند تحديد الملفات التي تُحفظ من النسخة الاحتياطية الملغاة عند الاستئناف. راجع الملاحظة أعلاه لمزيد من التفاصيل. (*أبلغ عنه David Youatt، Yogesh Sharma، Stephen Frost.*)
- إصلاح خطأ في الاستعادة الانتقائية عندما توجد قاعدة بيانات مستخدم واحدة فقط في العنقود. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Nj Baliyan.*)
- إصلاح تنسيق طابع زمني غير متوافق مع ISO-8601 في ترويسات التفويض لـ S3. كانت AWS وبعض البوابات متسامحة مع حشو خانة الساعات بمسافات بدلًا من الأصفار بينما لم تكن أخرى كذلك. (*أصلحه Andrew Schwartz. راجعه David Steele.*)

**الميزات:**

- دعم PostgreSQL 11 Beta 2.

**التحسينات:**

- تحسين عميل HTTP لتعيين `content-length` إلى 0 عندما لا يحدده الخادم. تُعين S3 (والبوابات) دائمًا `content-length` أو `transfer-encoding` لكن `HTTP 1.1` لا يشترط ذلك وقد لا تضمّ الخوادم الوكيلة (مثل HAProxy) أيًّا منهما. (*اقترحه Adam K. Sumner.*)
- تعيين `search_path = 'pg_catalog'` على اتصالات PostgreSQL. (*اقترحه Stephen Frost.*)

**تحسينات التوثيق:**

- إنشاء قسم جديد لوصف بناء pgBackRest والبناء على مضيف منفصل.
- إضافة نموذج سياسة S3 لتقييد امتيازات الحاوية. (*اقترحه Douglas J Hunley، Jason O'Donnell.*)


### ملاحظات إصدار v2.03 {#v203-release-notes}

*ملف تنفيذي واحد للنشر*

*صدر في 22 مايو 2018*

**إصلاحات الأخطاء:**

- إصلاح تجاوز محتمل للمخزن المؤقت في معالجة رسائل الخطأ. (*أبلغ عنه Lætitia.*)
- إصلاح أخذ قفل كتابة الأرشيف للأمر `archive-get` المتزامن. (*أبلغ عنه uspen.*)

**التحسينات:**

- تضمين دوال C المُصدَّرة ووحدات Perl مباشرة في الملف التنفيذي لـ pgBackRest.
- استخدام `time_t` بدلًا من `__time_t` لقابلية نقل أفضل. (*اقترحه Nick Floersch.*)
- طباعة إجمالي زمن التشغيل بالمللي ثانية عند انتهاء الأمر.


### ملاحظات إصدار v2.02 {#v202-release-notes}

*الحصول المتوازي غير المتزامن على الأرشيف وتضمينات الإعداد*

*صدر في 6 مايو 2018*

**إصلاحات الأخطاء:**

- إصلاح مزامنة الأدلة بشكل عودي عندما يجب مزامنة الدليل المحدد فقط. (*أبلغ عنه Craig A. James.*)
- إصلاح إطلاق `archive-copy` خطأ "path not found" للنسخ الاحتياطية incr/diff. (*أبلغ عنه yummyliu، Vitaliy Kukharik.*)
- إصلاح فشل بناء الـ manifest عندما يكون ملفان أو أكثر في `PGDATA` مرتبطين بنفس الدليل. (*أبلغ عنه Vitaliy Kukharik.*)
- إصلاح فشل استعادة الدلتا عندما يغيب ملف مرتبط.
- إصلاح عرض خيارات المفتاح/القيمة والقوائم في المساعدة. (*أبلغ عنه Clinton Adams.*)

**الميزات:**

- إضافة `archive-get` متوازٍ غير متزامن. تحافظ هذه الميزة على قائمة انتظار لمقاطع WAL للمساعدة في تقليل زمن الاستجابة عندما يطلب PostgreSQL مقطع WAL عبر restore_command.
- إضافة دعم ملفات إعداد إضافية لـ pgBackRest. يُحدَّد الدليل بخيار `--config-include-path`. إضافة خيار `--config-path` لتجاوز المسار الأساسي الافتراضي لخياري `--config` و`--config-include-path`. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة خيار `repo-s3-token` للسماح بإعداد رموز بيانات الاعتماد المؤقتة. لا يملك pgBackRest حاليًا طريقة لطلب بيانات اعتماد جديدة لذا يجب أن يكتمل الأمر بأكمله (مثل `backup` و`restore`) قبل انتهاء صلاحية بيانات الاعتماد. (*ساهم به Yogesh Sharma. راجعه David Steele.*)

**التحسينات:**

- تحديث الخيارات `archive-push-queue-max` و`manifest-save-threshold` و`buffer-size` لقبول قيم بوحدات `KB` أو `MB` أو `GB` أو `TB` أو `PB` حيث المضاعف قوة لـ `1024`. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- جعل مزامنة مسارات النسخ/الاستعادة أكثر كفاءة. قد يكون مسح الدليل بأكمله مكلفًا جدًا إذا كان هناك الكثير من الجداول الصغيرة. يحتوي manifest النسخة الاحتياطية على قائمة المسارات لذا استخدمها لتنفيذ المزامنة بدلًا من مسح مسار النسخ/الاستعادة.
- إظهار وسائط الأوامر إلى جانب خيارات الأوامر في رسالة السجل المعلوماتية الأولية.
- إعادة تسمية خيار archive-queue-max إلى archive-push-queue-max. يتسق ذلك مع خيار `archive-get-queue-max` الجديد. سيستمر قبول اسم الخيار القديم.

**إصلاحات أخطاء التوثيق:**

- تحديث التوثيق بدعم 32-بت والتنبيهات. أُضيف دعم 32-بت في v1.26. (*أبلغ عنه Viorel Tabara.*)

**تحسينات التوثيق:**

- إضافة أمثلة مراقبة باستخدام PostgreSQL وjq. (*اقترحه Stephen Frost، Brian Faherty.*)
- إضافة مثال لاستخدام قسم الأوامر في إعداد الأرشفة. (*اقترحه Christophe Courtois.*)
- إزالة التوثيق الذي يصف `info --output=json` بأنه تجريبي.
- تحديث وصف متقادم لخيار `spool-path`.

**ميزات مجموعة الاختبارات:**

- استخدام lcov لتقارير تغطية اختبارات وحدة C. تم التحويل من Devel::Cover لأنه لم يكن يُبلغ عن تغطية الفروع للتقارير المحولة من gcov. تغطية الفروع غير المكتملة لوحدة ما تولّد الآن خطأً. لا تُعرض تغطية اختبارات الوحدة في التقرير ما لم تكن غير مكتملة لتغطية التعليمات أو الفروع.


### ملاحظات إصدار v2.01 {#v201-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 19 مارس 2018*

**إصلاحات الأخطاء:**

- إصلاح الإبلاغ عن خياري `--target-action` و`--recovery-option` باعتبارهما غير صالحين عند الاستعادة بـ `--type=immediate`. (*أبلغ عنه Brad Nicholson.*)
- إصدار خطأ فورًا عند تمرير خيار حساس (مثل `repo1-s3-key`) في سطر الأوامر. بما أن pgBackRest لم يكن يمرر الخيارات الحساسة إلى العمليات الفرعية كان يُطلق خطأ غامض. الخطأ الجديد أوضح بكثير ويقدم تلميحات حول كيفية إصلاح المشكلة. تحديث توثيق الأوامر لحذف الخيارات الحساسة التي لا يمكن تحديدها في سطر الأوامر. (*أبلغ عنه Brad Nicholson.*)
- إصلاح مشكلة تمرير `--no-config` إلى Perl المضمّنة. (*أبلغ عنه Ibrahim Edib Kokdemir.*)
- إصلاح مشكلة كان فيها تحديد `log-level-stderr` > `warn` يسبب خطأ عملية `local`/`remote` عند الخروج بسبب مخرجات على stderr عندما لا يُتوقع أي منها. أصبحت القيمة القصوى لعملية `local`/`remote` الآن `error` إذ لا سبب لأن تُصدر هذه العمليات تحذيرات. (*أبلغ عنه Clinton Adams.*)
- إصلاح اختبار الـ manifest في الأمر `check` عند وجود مساحات جداول. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Thomas Flatley.*)

**التحسينات:**

- إصدار خطأ عند تعيين وسائط متعددة في ملف الإعداد لخيار لا يقبل وسائط متعددة. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إزالة أوامر sudo الزائدة من `src/Makefile`. (*ساهم به Adrian Vondendriesch. راجعه David Steele.*)

**تحسينات التوثيق:**

- إظهار الفهرس في الأمثلة للخيارات المفهرسة، أي `repo-*` و`pg-*`. (*اقترحه Stephen Frost.*)
- تبسيط جدول المحتويات في صفحة الأوامر عبر إدراج الأوامر فقط. (*اقترحه Stephen Frost.*)
- إزالة الإشارات إلى أن مكتبة C اختيارية.

**ميزات مجموعة الاختبارات:**

- إضافة بناء حزم CentOS/RHEL.
- استخدام clang للتحليل الثابت للشيفرة. لم يُعثر على شيء في البداية عدا بعض الدوال التي كان ينبغي تعليمها `__noreturn__`.


### ملاحظات إصدار v2.00 {#v200-release-notes}

*تحسينات أداء دفع الأرشفة*

*صدر في 23 فبراير 2018*

**الميزات:**

- الأمر `archive-push` مُبرمَج الآن جزئيًا بلغة C ما يسمح للأمر `archive_command` في PostgreSQL بالعمل أسرع بشكل ملحوظ عند معالجة رسائل الحالة من عملية الأرشفة غير المتزامنة. (*راجعه Cynthia Shang.*)

**التحسينات:**

- تحسين الأمر `check` للتحقق من إمكانية بناء manifest النسخ الاحتياطية. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تحسين أداء عميل HTTPS. يأخذ التخزين المؤقت الآن بايتات `pending` على المقبس في الحسبان (عند وجودها) بدلًا من الاعتماد كليًا على `select()`. في بعض الحالات لم تكن البايتات الأخيرة تُدفع حتى يُغلق الاتصال.
- تحسين أداء الحذف في S3. كان الثابت `S3_BATCH_MAX` قد استُبدل بقيمة ثابتة قدرها 2، ربما أثناء الاختبار.
- السماح بإعادة تعيين أي خيار غير خاص بسطر الأوامر إلى قيمته الافتراضية في سطر الأوامر. يتيح ذلك إعادة تعيين الخيارات في `pgbackrest.conf` إلى الافتراضي ما يقلل الحاجة إلى كتابة ملفات إعداد جديدة لاحتياجات محددة.
- مكتبة C مطلوبة الآن. يلغي ذلك التحميل المشروط ويسهّل تطوير ميزات مكتبية جديدة.
- الملف التنفيذي `pgbackrest` أصبح الآن ثنائي C بدلًا من Perl. يسمح ذلك لبعض الأوامر الحرجة زمنيًا (مثل `archive-push` غير المتزامن) بالعمل بسرعة أكبر.
- إعادة تسمية خيارات `db-*` إلى `pg-*` وخيارات `backup-*` إلى `repo-*` لتحسين الاتساق. خيارات `repo-*` مفهرسة الآن رغم أنه لا يُسمح حاليًا بواحد فقط.

**ميزات التوثيق:**

- جميع العناقيد في التوثيق مُهيّأة بالمجاميع الاختبارية.

**تحسينات التوثيق:**

- إدراج أسماء الخيارات المهملة في التوثيق ومساعدة سطر الأوامر.
- توضيح أنه يجب على المستخدم إنشاء حاويات S3. (*اقترحه David Youatt.*)


### ملاحظات إصدار v1.29 {#v129-release-notes}

*إصلاح خطأ حرج لاستئناف النسخ الاحتياطي*

*صدر في 5 يوليو 2018*

**ملاحظة هامة**: يصلح هذا الإصدار خطأً حرجًا في ميزة استئناف النسخ الاحتياطي. ينبغي اعتبار جميع النسخ الاحتياطية المستأنفة قبل هذا الإصدار غير متسقة. ستُستأنف نسخة احتياطية بعد فشل نسخة سابقة، ما لم يكن `resume=n` محددًا. يمكن تحديد النسخة الاحتياطية المستأنفة بفحص سجل النسخ الاحتياطي عن الرسالة "aborted backup of same type exists, will be cleaned to remove invalid files and resumed". إذا كانت الرسالة موجودة فلا تستخدم هذه النسخة الاحتياطية أو أي نسخة في نفس المجموعة للاستعادة، وافحص سجلات الاستعادة لمعرفة ما إذا كانت نسخة مستأنفة قد استُعيدت. إن كان كذلك فقد تكون هناك بيانات غير متسقة في العنقود.

**إصلاحات الأخطاء:**

- إصلاح خطأ حرج في الاستئناف أدى إلى نسخ احتياطية غير متسقة. أزال تراجع في `v0.82` مقارنة الطوابع الزمنية عند تحديد الملفات التي تُحفظ من النسخة الاحتياطية الملغاة عند الاستئناف. راجع الملاحظة أعلاه لمزيد من التفاصيل. (*أبلغ عنه David Youatt، Yogesh Sharma، Stephen Frost.*)
- إصلاح تنسيق طابع زمني غير متوافق مع ISO-8601 في ترويسات التفويض لـ S3. كانت AWS وبعض البوابات متسامحة مع حشو خانة الساعات بمسافات بدلًا من الأصفار بينما لم تكن أخرى كذلك. (*أصلحه Andrew Schwartz. راجعه David Steele.*)
- إصلاح مزامنة الأدلة بشكل عودي عندما يجب مزامنة الدليل المحدد فقط. (*أبلغ عنه Craig A. James.*)
- إصلاح الإبلاغ عن خياري `--target-action` و`--recovery-option` باعتبارهما غير صالحين عند الاستعادة بـ `--type=immediate`. (*أبلغ عنه Brad Nicholson.*)
- إصلاح إطلاق `archive-copy` خطأ "path not found" للنسخ الاحتياطية incr/diff. (*أبلغ عنه yummyliu، Vitaliy Kukharik.*)
- إصلاح فشل بناء الـ manifest عندما يكون ملفان أو أكثر في `PGDATA` مرتبطين بنفس الدليل. (*أبلغ عنه Vitaliy Kukharik.*)
- إصلاح فشل استعادة الدلتا عندما كان ملف مرتبط يغيب.
- إصلاح خطأ في الاستعادة الانتقائية عندما توجد قاعدة بيانات مستخدم واحدة فقط في العنقود. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Nj Baliyan.*)

**التحسينات:**

- تحسين عميل HTTP لتعيين `content-length` إلى 0 عندما لا يحدده الخادم. تُعين S3 (والبوابات) دائمًا `content-length` أو `transfer-encoding` لكن `HTTP 1.1` لا يشترط ذلك وقد لا تضمّ الخوادم الوكيلة (مثل HAProxy) أيًّا منهما. (*اقترحه Adam K. Sumner.*)
- تحسين أداء عميل HTTPS. يأخذ التخزين المؤقت الآن بايتات `pending` على المقبس في الحسبان (عند وجودها) بدلًا من الاعتماد كليًا على `select()`. في بعض الحالات لم تكن البايتات الأخيرة تُدفع حتى يُغلق الاتصال.
- تحسين أداء الحذف في S3. كان الثابت `S3_BATCH_MAX` قد استُبدل بقيمة ثابتة قدرها 2، ربما أثناء الاختبار.
- جعل مزامنة مسارات النسخ/الاستعادة أكثر كفاءة. قد يكون مسح الدليل بأكمله مكلفًا جدًا إذا كان هناك الكثير من الجداول الصغيرة. يحتوي manifest النسخة الاحتياطية على قائمة المسارات لذا استخدمها لتنفيذ المزامنة بدلًا من مسح مسار النسخ/الاستعادة. إزالة وظيفة مزامنة المسارات العودية لأنها لم تعد مستخدمة.

**إصلاحات أخطاء التوثيق:**

- تحديث التوثيق بدعم 32-بت والتنبيهات. أُضيف دعم 32-بت في v1.26. (*أبلغ عنه Viorel Tabara.*)

**تحسينات التوثيق:**

- توضيح أنه يجب على المستخدم إنشاء حاويات S3. (*اقترحه David Youatt.*)
- تحديث وصف متقادم لخيار `spool-path`.


### ملاحظات إصدار v1.28 {#v128-release-notes}

*حذف الـ stanza*

*صدر في 1 فبراير 2018*

**إصلاحات الأخطاء:**

- إصلاح تعذر استعادة قاعدة بيانات واحدة محتواة في مساحة جداول باستخدام --db-include. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Chiranjeevi Ravilla.*)
- ضمان اختيار `db-id` الأحدث عند مطابقة `archive.info` مع `backup.info`. يوفر ذلك مطابقة صحيحة في حال وجود تكرارات في `system-id` و`db-version` (مثلًا بعد التراجع عن `pg_upgrade`). (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Adam K. Sumner.*)
- إصلاح رسالة خطأ ثرثارة أكثر من اللازم عند الإبلاغ عن أمر غير صالح. (*أبلغ عنه Jason O'Donnell.*)

**الميزات:**

- إضافة الأمر `stanza-delete` لتنظيف الـ stanza غير المستخدمة. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Magnus Hagander.*)

**التحسينات:**

- تحسين الأمر `stanza-create` بحيث لا يصدر خطأ عندما تكون الـ stanza موجودة بالفعل. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**تحسينات التوثيق:**

- تحديث توثيق `stanza-create --force` للحث على الحذر عند الاستخدام. (*اقترحه Jason O'Donnell.*)


### ملاحظات إصدار v1.27 {#v127-release-notes}

*إصلاحات أخطاء وتوثيق*

*صدر في 19 ديسمبر 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت تكتم أخطاء المحلية للأمرين `backup` و`restore`. عندما يكون مضيف نسخ احتياطي موجودًا، ينبغي السماح بالنسخ الاحتياطي على مضيف النسخ الاحتياطي فقط وبالاستعادة على مضيف قاعدة البيانات فقط، ما لم يُنشأ إعداد بديل يتجاهل المضيف البعيد. (*أبلغ عنه Lardière Sébastien.*)
- إصلاح مشكلة عدم إنهاء صلاحية WAL على PostgreSQL 10. سببها تعبير نمطي معيب توقع أن تكون جميع الإصدارات الرئيسية لـ PostgreSQL بصيغة X.X. (*أبلغ عنه Adam Brusselback.*)
- إصلاح مشكلة عدم تمرير خيار `--no-config` إلى العمليات الابنة. كان ذلك يعني أن العمليات الابنة ستظل تقرأ ملف الإعداد المحلي وربما تسبب سلوكيات غير متوقعة.
- إصلاح الأمر `info` للقضاء على مخرجات `"db (prior)"` إذا لم توجد نسخ احتياطية أو أرشيفات لإصدار سابق من العنقود. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Stephen Frost.*)

**ميزات التوثيق:**

- توثيق العلاقة بين خياري `archive-copy` و`archive-check`. (*اقترحه Markus Nullmeier.*)
- تحسين التوثيق المرجعي لـ `archive-copy`.


### ملاحظات إصدار v1.26 {#v126-release-notes}

*تشفير المستودع*

*صدر في 21 نوفمبر 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة قد تسبب فشل نسخ manifests كبيرة أثناء الاستعادة. (*أبلغ عنه Craig A. James.*)
- إصلاح إزاحة WAL غير الصحيحة للمعماريات 32-بت. (*أصلحه Javier Wilson. راجعه David Steele.*)
- إصلاح مشكلة استرجاع WAL لإصدارات قواعد البيانات القديمة. بعد `stanza-upgrade` ينبغي أن يبقى من الممكن استعادة نسخ احتياطية من الإصدار السابق وإجراء الاسترداد بـ `archive-get`. لكن archive-get كان يفحص أحدث إصدار/معرّف لقاعدة البيانات فقط ويفشل. أيضًا تنظيف بعض المشكلات عندما يظهر نفس إصدار/معرّف قاعدة البيانات عدة مرات في السجل. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Clinton Adams.*)
- إصلاح مشكلة عدم تعيين المجموعات غير الصالحة للنسخ الاحتياطية بشكل صحيح عند الاستعادة. إذا لم يستطع النسخ الاحتياطي مقابلة مجموعة باسم فسيخزن المجموعة في الـ manifest كـ `false` ثم يستخدم إما مالك $PGDATA لتعيين المجموعة أثناء الاستعادة أو، عند تعذر ذلك، مجموعة المستخدم الحالي. لم يكن هذا المنطق يعمل بشكل صحيح لأن المجموعة المختارة كانت تستبدل المستخدم عند الاستعادة تاركة المجموعة غير محددة والمستخدم معيّنًا بشكل خاطئ إلى المجموعة. (*أبلغ عنه Jeff McCormick.*)
- إصلاح مشكلة تمرير الوسائط إلى الأطراف البعيدة. عندما كان يُحدَّد أكثر من قاعدة بيانات واحدة كانت تُمرَّر مسارات db1 ومنفذه ومسار مقبسه بغض النظر عن قاعدة البيانات المقصودة فعليًا. (*أبلغ عنه uspen.*)

**الميزات:**

- دعم تشفير المستودع. (*ساهم به Cynthia Shang، David Steele.*)

**التحسينات:**

- تعطيل مرشّح gzip عندما يكون `--compress-level-network=0`. كان المرشّح يُستخدم مع مستوى ضغط 0 ما يضيف عبئًا دون أي فائدة.
- تحسين أداء فك الضغط لمرشّح gzip.

**ميزات التوثيق:**

- إضافة قالب لتحسين المعلومات الأولية المجمعة لتقارير المشكلات. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**تحسينات التوثيق:**

- توضيح استخدام خيار `archive-timeout` ووصف كيفية اختلافه عن إعداد archive_timeout في PostgreSQL. (*ساهم به Cynthia Shang. راجعه David Steele. اقترحه Keith Fiske.*)

**ميزات مجموعة الاختبارات:**

- اختبارات مؤتمتة لمعمارية i386/i686 ذات 32-بت.


### ملاحظات إصدار v1.25 {#v125-release-notes}

*تحسينات أداء S3*

*صدر في 24 أكتوبر 2017*

**إصلاحات الأخطاء:**

- إصلاح تجاهل الإعدادات المخصصة لخيار `compress-level`. (*أبلغ عنه Jens Wilke.*)
- إزالة الخطأ عند اكتشاف خطوط زمنية متداخلة. الخطوط الزمنية المتداخلة صالحة في العديد من سيناريوهات الاسترداد إلى نقطة زمنية (PITR). (*أبلغ عنه blogh.*)
- إصلاح حالات عدم عرض `database-id` كعدد صحيح في مخرجات info بصيغة JSON. (*أصلحه Cynthia Shang. راجعه David Steele. أبلغ عنه Jason O'Donnell.*)

**الميزات:**

- تحسين أداء طلبات الإدراج على S3. يُستخدم أي جزء حرفي بادئ من تعبير مرشّح لتوليد بادئة بحث ما يساعد غالبًا على إبقاء الطلب صغيرًا بما يكفي لتجنب تحديد المعدل. (*اقترحه Mihail Shvein.*)

**ميزات مجموعة الاختبارات:**

- إضافة اختبارات أداء الإدخال/الإخراج.


### ملاحظات إصدار v1.24 {#v124-release-notes}

*استثناءات جديدة للنسخ الاحتياطي*

*صدر في 28 سبتمبر 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة إصدار تحذيرات بدلًا من رسائل سجل ذات أولوية أدنى أثناء تهيئة النسخ الاحتياطي من خادم الاستعداد. (*أبلغ عنه uspen.*)
- إصلاح مشكلة عدم تمرير بعض خيارات `db-*` (مثل `db-port`) إلى الأطراف البعيدة. (*أبلغ عنه uspen.*)

**الميزات:**

- استبعاد محتويات `pg_snapshots` و`pg_serial` و`pg_notify` و`pg_dynshmem` من النسخ الاحتياطي لأنه يُعاد بناؤها عند الإقلاع.
- استبعاد ملفات `pg_internal.init` من النسخ الاحتياطي لأنه يُعاد بناؤها عند الإقلاع.

**التحسينات:**

- فتح ملف السجل بعد انفصال العملية غير المتزامنة تمامًا عن العملية الرئيسية لمنع العملية الرئيسية من التسجيل في الملف أيضًا. (*اقترحه Jens Wilke.*)

**ميزات التوثيق:**

- إضافة إعداد SSH دون كلمة مرور.

**تحسينات التوثيق:**

- إعادة تسمية master إلى primary في التوثيق بما يتوافق مع عرف PostgreSQL.


### ملاحظات إصدار v1.23 {#v123-release-notes}

*خوادم استعداد متعددة ودعم PostgreSQL 10*

*صدر في 3 سبتمبر 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يمكن أن تسبب توقف عملية الضغط على الملفات المتنامية. (*أبلغ عنه Jesper St John، Aleksandr Rogozin.*)
- إصلاح مشكلة عدم إرسال رسائل keep-alive إلى الطرف البعيد من العملية المحلية. (*أبلغ عنه William Cox.*)

**الميزات:**

- يمكن إعداد ما يصل إلى سبعة خوادم استعداد للنسخ الاحتياطي من خادم الاستعداد. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- دعم PostgreSQL 10.
- السماح بـ `content-length` (إضافة إلى الترميز المجزأ) عند قراءة بيانات XML لتحسين التوافق مع بوابات S3 من جهات خارجية. (*اقترحه Victor Gdalevich.*)

**التحسينات:**

- زيادة مهلة HTTP لـ S3.
- إضافة إعادة محاولة HTTP لزيادة القدرة على تحمّل أخطاء شبكة S3 العابرة.

**إصلاحات أخطاء التوثيق:**

- إصلاح توليد المستندات لتضمين ملخصات الأقسام في صفحة الإعداد. (*أصلحه Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.22 {#v122-release-notes}

*إصلاح إعادة محاولة S3*

*صدر في 9 أغسطس 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة مصادقة في إعادة محاولة S3.


### ملاحظات إصدار v1.21 {#v121-release-notes}

*تحسين مخرجات info وخيار منفذ SSH*

*صدر في 8 أغسطس 2017*

**إصلاحات الأخطاء:**

- يُعاد الآن إنشاء الدليل `archive_status` عند الاستعادة لدعم PostgreSQL 8.3 الذي لا يعيد إنشاءه تلقائيًا مثل الإصدارات الأحدث. (*أبلغ عنه Stephen Frost.*)
- إصلاح مشكلة قد تترك دليل الأرشيف الفارغ لإصدار PostgreSQL قديم بعد `stanza-upgrade`. (*أصلحه Cynthia Shang. راجعه David Steele.*)

**الميزات:**

- تعديل الأمر `info` (بالمخرجات النصية وJSON معًا) لعرض معرّف الأرشيف والحد الأدنى/الأقصى لـ WAL الموجود حاليًا في الأرشيف لإصدار عنقود قاعدة البيانات الحالي والسابق إن وُجد. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة الخيارين `--backup-ssh-port` و`--db-ssh-port` لدعم منافذ SSH غير الافتراضية. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**التحسينات:**

- إعادة المحاولة عندما يعيد S3 خطأً داخليًا (500).

**إصلاحات أخطاء التوثيق:**

- إصلاح وصف `--online` بناءً على سياق الأمر.

**ميزات التوثيق:**

- إضافة إنشاء `/etc/pgbackrest.conf` إلى تعليمات التثبيت اليدوي.

**تحسينات التوثيق:**

- نقل خيارات المستودع إلى قسم منفصل في مساعدة الأوامر/سطر الأوامر. (*اقترحه Stephen Frost.*)


### ملاحظات إصدار v1.20 {#v120-release-notes}

*إصلاح خطأ حرج في 8.3/8.4*

*صدر في 27 يونيو 2017*

**ملاحظة هامة**: ينبغي على منشآت PostgreSQL 8.3 و8.4 التي تستخدم مساحات الجداول الترقية فورًا من أي إصدار v1 وتشغيل نسخة احتياطية كاملة. منع خطأٌ النسخ الاحتياطي لمساحات الجداول على هذين الإصدارين فقط. لا يتأثر PostgreSQL ≥ 9.0.

**إصلاحات الأخطاء:**

- إصلاح مشكلة منعت النسخ الاحتياطي لمساحات الجداول على PostgreSQL ≤ 8.4.
- إصلاح علامة مفقودة في بناء مكتبة C نتج عنها ثنائي غير متطابق على أنظمة 32-بت. (*أبلغ عنه Adrian Vondendriesch.*)

**الميزات:**

- إضافة الخيارين `s3-repo-ca-path` و`s3-repo-ca-file` لاستيعاب الأنظمة التي لا يجد فيها `IO::Socket::SSL` سلطات الشهادات تلقائيًا، مثل RHEL7، أو لتحميل سلطات شهادات مخصصة. (*اقترحه Scott Frazer.*)

**ميزات مجموعة الاختبارات:**

- إضافة بناء التوثيق إلى CI.


### ملاحظات إصدار v1.19 {#v119-release-notes}

*دعم S3*

*صدر في 12 يونيو 2017*

**إصلاحات الأخطاء:**

- إصلاح الأمر `info` بحيث يكون الحد الأدنى/الأقصى لأرشيف WAL المعروض لإصدار قاعدة البيانات الحالي. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- إصلاح الأمر `backup` بحيث يُعاد تعيين خيار `backup-standby` (وتجري النسخة الاحتياطية على الأساسي) إذا كان خادم الاستعداد غير مُعد و/أو غير قابل للوصول. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- إصلاح تحذيرات الإعداد المرفوعة من عملية بعيدة تسبب أخطاءً في العملية الرئيسية. (*أصلحه Cynthia Shang. راجعه David Steele.*)

**الميزات:**

- دعم مستودع Amazon S3. (*راجعه Cynthia Shang.*)

**إصلاحات أخطاء التوثيق:**

- تغيير الخيار غير الصالح `max-archive-mb` في مرجع الإعداد إلى `archive-queue-max`.
- إصلاح نقص `sudo` في قسم التثبيت. (*أصلحه Lætitia. راجعه David Steele.*)


### ملاحظات إصدار v1.18 {#v118-release-notes}

*ترقية الـ stanza وإعادة الهيكلة وتحسينات القفل*

*صدر في 12 أبريل 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها العمليات للقراءة فقط التي تستخدم عمليات عاملة محلية (أي `restore`) تُنشئ أقفال كتابة قد تتداخل مع `archive-push` المتوازي. (*أبلغ عنه Jens Wilke.*)

**الميزات:**

- إضافة الأمر stanza-upgrade لتوفير آلية لترقية stanza بعد الترقية إلى إصدار رئيسي جديد من PostgreSQL. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة تحقق من صلاحية `pgbackrest.conf` لعرض تحذيرات إذا كانت الخيارات غير صالحة أو ليست في القسم الصحيح. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**التحسينات:**

- تبسيط مخطط القفل. الآن العملية الرئيسية فقط ستحمل أقفال الكتابة (للأمرين `archive-push` و`backup`) وليس جميع العمليات العاملة المحلية والبعيدة كما كان سابقًا.
- عدم تعيين الطوابع الزمنية للملفات في أدلة النسخ الاحتياطي لتطابق الطوابع الزمنية في دليل العنقود. جرى ذلك في الأصل لتمكين استئناف النسخ الاحتياطي، لكن تلك العملية منفَّذة الآن بالمجاميع الاختبارية.
- تحسين رسالة الخطأ عندما يكتشف الأمر `restore` وجود `postmaster.pid`. (*اقترحه Yogesh Sharma.*)
- إعادة ترقيم رموز الإرجاع بين 25 و125 لتجنب تفسير PostgreSQL لبعضها كاستثناءات إشارات قاتلة. (*اقترحه Yogesh Sharma.*)


### ملاحظات إصدار v1.17 {#v117-release-notes}

*إصلاح خطأ مجموع تحقق الصفحات*

*صدر في 13 مارس 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها الصفحات المُهيّأة حديثًا (لكن غير المستخدمة) تسبب تحذيرات مجموع تحقق الصفحات. (*أبلغ عنه Stephen Frost.*)


### ملاحظات إصدار v1.16 {#v116-release-notes}

*تحسينات مجموع تحقق الصفحات والتكامل المستمر واختبار الحزم*

*صدر في 2 مارس 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها الجداول التي تتجاوز 1GB تُبلغ عن تحذيرات مجموع تحقق الصفحات بعد المقطع الأول. (*أبلغ عنه Stephen Frost.*)
- إصلاح مشكلة كانت فيها قواعد البيانات المنشأة بمساحة جداول غير افتراضية تثير تحذيرات زائفة عن عدم محاذاة `pg_filenode.map` و`pg_internal.init` للصفحات. (*أبلغ عنه blogh.*)

**ميزات مجموعة الاختبارات:**

- تكامل مستمر باستخدام `travis-ci`.
- بناء مؤتمت لحزم Debian لجميع التوزيعات المدعومة.


### ملاحظات إصدار v1.15 {#v115-release-notes}

*إعادة الهيكلة وإصلاحات أخطاء*

*صدر في 13 فبراير 2017*

**إصلاحات الأخطاء:**

- إصلاح تراجع قُدِّم في v1.13 قد يفشل معه النسخ الاحتياطي إذا أُزيلت ملفات (مثل حذف جداول) أثناء بناء الـ manifest. (*أبلغ عنه Navid Golpayegani.*)


### ملاحظات إصدار v1.14 {#v114-release-notes}

*إعادة الهيكلة وإصلاحات أخطاء*

*صدر في 13 فبراير 2017*

**إصلاحات الأخطاء:**

- إصلاح مشكلة عدم إعادة محاولة خطأ archive-push بل إعادة أخطاء إلى PostgreSQL إلى ما لا نهاية (ما لم يُحذف ملف `.error` يدويًا). (*أبلغ عنه Jens Wilke.*)
- إصلاح حالة تسابق في الأرشفة المتوازية كان فيها إنشاء مسارات جديدة يولّد خطأً عندما تحاول عمليات متعددة ذلك في الوقت نفسه. (*أبلغ عنه Jens Wilke.*)

**التحسينات:**

- تحسين أداء `wal archive min/max` الذي يوفره الأمر `info`. (*اقترحه Jens Wilke.*)

**ميزات التوثيق:**

- تحديث توثيق الأرشفة غير المتزامنة لوصف بشكل أدق كيف تعمل الطريقة الجديدة وكيف تختلف عن الطريقة القديمة. (*اقترحه Jens Wilke.*)


### ملاحظات إصدار v1.13 {#v113-release-notes}

*الأرشفة المتوازية وإنشاء الـ stanza وتحسين info وcheck*

*صدر في 5 فبراير 2017*

**ملاحظة هامة**: لم يعد تنفيذ الأرشفة غير المتزامنة الجديد ينسخ WAL إلى قائمة انتظار منفصلة. إذا بقي أي WAL في قائمة الانتظار القديمة بعد الترقية إلى `1.13` فسيُهمل **ولن** يُدفع إلى المستودع. لمنع هذه النتيجة، أوقف الأرشفة بتعيين `archive_command = false`. بعد ذلك أفرغ قائمة الانتظار غير المتزامنة بتشغيل `pgbackrest --stanza=[stanza-name] archive-push` وانتظر اكتمال العملية. تحقق من أن قائمة الانتظار في `[spool-path]/archive/[stanza-name]/out` فارغة. أخيرًا ثبّت `1.13` واستعد `archive_command` الأصلي. **ملاحظة هامة**: لم يعد الأمر `stanza-create` اختياريًا ويجب تنفيذه قبل إمكانية إجراء النسخ الاحتياطي أو الأرشفة على stanza **جديدة**. لا تتطلب الـ stanza الموجودة مسبقًا تنفيذ `stanza-create`.

**إصلاحات الأخطاء:**

- إصلاح إسناد const يولّد تحذير مُجمِّع في مكتبة C. (*أصلحه Adrian Vondendriesch. راجعه David Steele.*)
- إصلاح بعض مزامنات الأدلة التي فُقدت لخيار `--repo-sync`.
- إصلاح مشكلة كان يمكن فيها أن يسبب غياب مستخدم/مجموعة عند الاستعادة خطأ "uninitialized value" في `File->owner()`. (*أبلغ عنه Leonardo GG Avellar.*)
- إصلاح مشكلة عدم إخراج أخطاء عدم تطابق البروتوكول للقيمة المتوقعة.
- إصلاح رسالة سجل زائفة من `archive-get` كانت تشير إلى أن رمز الخروج 1 إنهاء غير طبيعي.

**الميزات:**

- تنفيذ محسّن متعدد العمليات للأرشفة غير المتزامنة.
- تحسين الأمر `stanza-create` بحيث يمكنه إصلاح المستودعات المعطلة في معظم الحالات وبه ما يكفي من المتانة لجعله إلزاميًا. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تحسين الأمر `check` ليعمل على خادم استعداد، رغم أن الفحوصات أساسية فقط لأن `pg_switch_xlog()` لا يمكن تنفيذها على نسخة متماثلة. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة نطاقات WAL للأرشيف والنسخ الاحتياطي إلى الأمر `info`.
- إضافة تحذير بتحديث `pg_tablespace.spclocation` عند إعادة تعيين مساحات الجداول في PostgreSQL < 9.2. (*ساهم به blogh. راجعه David Steele.*)
- إزالة متطلبات القفل البعيد للأوامر `archive-get` و`restore` و`info` و`check` لأنها عمليات للقراءة فقط. (*اقترحه Michael Vitale.*)

**التحسينات:**

- لا تُخرج لافتة ملف السجل حتى تُكتب أول مدخلة سجل. (*اقترحه Jens Wilke.*)
- تقليل احتمال أن تسبب الصفحات الممزقة إيجابية زائفة في مجاميع تحقق الصفحات عبر الترشيح على LSN بدء النسخ الاحتياطي.
- إزالة تحسين خاص بـ Intel من علامات بناء مكتبة C. (*ساهم به Adrian Vondendriesch. راجعه David Steele.*)
- إزالة خيار `--lock`. قُدِّم هذا الخيار قبل أن يصبح بإمكان دليل القفل التوضع خارج المستودع وهو الآن متقادم.
- إضافة خيار `--log-timestamp` للسماح بكتم الطوابع الزمنية في التسجيل. يُستخدم هذا في المقام الأول لتجنب المرشحات في التوثيق المؤتمت.
- إرجاع رمز خطأ مناسب عند تعذر تحويل مسار نسبي إلى مسار مطلق. (*اقترحه Yogesh Sharma.*)

**ميزات التوثيق:**

- إضافة توثيق لدليل المستخدم حول خيار `process-max`. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.12 {#v112-release-notes}

*مجاميع تحقق الصفحات والإعداد وإصلاحات أخطاء*

*صدر في 12 ديسمبر 2016*

**ملاحظة هامة**: في الإصدارات السابقة كان من الممكن تحديد خيارات في سطر الأوامر غير صالحة للأمر الحالي دون الحصول على خطأ. سيُولَّد الآن خطأ للخيارات غير الصالحة لذا من المهم فحص خيارات سطر الأوامر في بيئتك بعناية لمنع الاضطراب.

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها خيارات غير صالحة للأمر المحدد تُقدَّم في سطر الأوامر دون توليد خطأ. كانت الخيارات تُتجاهل ولا تسبب أي تغيير في السلوك، لكنها أدت إلى بعض الالتباس. ستولّد الخيارات غير الصالحة الآن خطأً. (*أبلغ عنه Nikhilchandra Kulkarni.*)
- إصلاح مشكلة عدم إنشاء روابط رمزية داخلية لمساحات الجداول في المستودع. ظهرت هذه المشكلة فقط عند محاولة تشغيل العناقيد في مكانها يدويًا باستخدام لقطات نظام الملفات ولم تؤثر في النسخ الاحتياطي والاستعادة العاديين.
- إصلاح مشكلة منعت إخراج الأخطاء إلى الطرفية قبل تهيئة نظام التسجيل، أي أثناء تحليل الخيارات. كانت رموز الخطأ تُعاد بدقة لذا لم يكن هذا سيجعل عملية تبدو ناجحة وهي ليست كذلك. (*أبلغ عنه Adrian Vondendriesch.*)
- إصلاح مشكلة عدم تمرير خيار `db-port` المحدد على خادم النسخ الاحتياطي إلى الطرف البعيد بشكل صحيح ما لم يكن من أول قاعدة بيانات مُعدّة. (*أبلغ عنه Michael Vitale.*)

**الميزات:**

- إضافة خيار `--checksum-page` للسماح لـ pgBackRest بالتحقق من مجاميع تحقق الصفحات في ملفات البيانات عندما تكون المجاميع ممكّنة على PostgreSQL >= 9.3. لاحظ أن هذه الوظيفة تتطلب مكتبة C قد لا تتوفر مبدئيًا في حزم نظام التشغيل. سيُمكَّن الخيار تلقائيًا عند وجود المكتبة وتمكين المجاميع على العنقود. (*اقترحه Stephen Frost.*)
- إضافة خيار `--repo-link` للسماح بكتم الروابط الرمزية الداخلية عندما يكون المستودع على نظام ملفات لا يدعم الروابط الرمزية. لا يؤثر هذا في أي وظيفة من وظائف pgBackRest، لكن الرابط الملائم `latest` لن يُنشأ وكذلك الروابط الرمزية الداخلية لمساحات الجداول، ما سيؤثر في القدرة على تشغيل العناقيد في مكانها يدويًا باستخدام لقطات نظام الملفات.
- إضافة خيار `--repo-sync` للسماح بتعطيل مزامنة الأدلة في المستودع لأنظمة الملفات التي لا تدعمها، مثل NTFS.
- إضافة مدخلة سجل يمكن التنبؤ بها للإشارة إلى أن أمرًا اكتمل بنجاح. مثلًا تنتهي نسخة احتياطية بنجاح بـ: `INFO: backup command end: completed successfully`. (*اقترحه Jens Wilke.*)

**التحسينات:**

- للتبسيط، يُنسخ ملف `pg_control` الآن مع بقية الملفات بدلًا من نسخه بمفرده في نهاية العملية. لا يتطلب الأمر `backup` هذا السلوك، وينسخ الأمر `restore` إلى ملف مؤقت يُعاد تسميته في نهاية الاستعادة.

**إصلاحات أخطاء التوثيق:**

- إصلاح مشكلة كتمت الاستثناءات في بناء PDF.
- إصلاح تراجع في روابط الأقسام قُدِّم في v1.10.

**ميزات التوثيق:**

- إضافة الاحتفاظ إلى قسم البدء السريع.


### ملاحظات إصدار v1.11 {#v111-release-notes}

*إصلاح خطأ في كفاءة الأرشفة غير المتزامنة*

*صدر في 17 نوفمبر 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها الأرشفة غير المتزامنة تنقل ملفًا واحدًا لكل تنفيذ بدلًا من نقل الملفات في دفعات. قُدِّم هذا التراجع في v1.09 وأثر في الكفاءة فقط، إذ أُرشفت جميع مقاطع WAL بشكل صحيح في الوضع غير المتزامن. (*أبلغ عنه Stephen Frost.*)


### ملاحظات إصدار v1.10 {#v110-release-notes}

*إنشاء الـ stanza وإصلاحات أخطاء ثانوية*

*صدر في 8 نوفمبر 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يمكن فيها أن تخطئ نسخة احتياطية إذا لم تُجرَ أي تغييرات على قاعدة بيانات بين نسختين احتياطيتين وتغيّر `pg_control` فقط.
- إصلاح مشكلة كانت فيها مسارات مساحات جداول ذات البادئة نفسها تسبب خطأ رابط غير صالح. (*أبلغ عنه Nikhilchandra Kulkarni.*)

**الميزات:**

- إضافة الأمر `stanza-create` لتنظيم عملية إنشاء الـ stanza في المستودع. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**التحسينات:**

- إزالة توجيهات `use lib` الزائدة من وحدات Perl. (*اقترحه Devrim Gündüz.*)


### ملاحظات إصدار v1.09 {#v109-release-notes}

*دعم 9.6 وقابلية الإعداد وإصلاحات أخطاء*

*صدر في 10 أكتوبر 2016*

**إصلاحات الأخطاء:**

- إصلاح الأمر `check` لمنع تسجيل رسالة خطأ إذا لم يكن دليل النسخ الاحتياطي موجودًا. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- إصلاح رسالة الخطأ لعرض أمر الأرشفة بشكل صحيح عند اكتشاف أمر أرشفة غير صالح. (*أبلغ عنه Jason O'Donnell.*)
- إصلاح مشكلة عدم بدء المؤرشف غير المتزامن إذا لم يكن لدى `archive-push` مساحة كافية لإدراج مقطع WAL جديد في قائمة الانتظار. كان ذلك يعني أن قائمة الانتظار لن تُفرغ أبدًا دون تدخل يدوي (مثل استدعاء `archive-push` مباشرة). يتلقى PostgreSQL الآن أخطاء عندما لا توجد مساحة كافية لتخزين مقاطع WAL جديدة لكن العملية غير المتزامنة ستبدأ مع ذلك بحيث تُحرر المساحة في نهاية المطاف. (*أبلغ عنه Jens Wilke.*)
- إصلاح انتهاء مهلة الطرف البعيد الذي كان يحدث عندما تولّد عملية محلية مجاميع اختبارية (أثناء الاستئناف أو الاستعادة) دون نسخ ملفات، ما يسمح للطرف البعيد بالخمول. (*أبلغ عنه Jens Wilke.*)

**الميزات:**

- ستُستخدم النسخ الاحتياطية غير الحصرية تلقائيًا على PostgreSQL 9.6.
- إضافة خيار `cmd-ssh` للسماح بتحديد عميل ssh. (*اقترحه Jens Wilke.*)
- إضافة خيار `log-level-stderr` للتحكم فيما إذا كانت رسائل سجل الطرفية تُرسل إلى `stderr` أو `stdout`. افتراضيًا هذا معيّن إلى `warn` ما يمثل تغييرًا في السلوك عن الإصدارات السابقة، رغم أنه قد يكون أكثر بديهية. تعيين `log-level-stderr=off` سيحفظ السلوك القديم. (*اقترحه Sascha Biberhofer.*)
- تعيين `application_name` إلى `"pgBackRest [command]"` لاتصالات قاعدة البيانات. (*اقترحه Jens Wilke.*)
- التحقق من أن archive_mode ممكّن عند تمكين خيار `archive-check`.

**التحسينات:**

- توضيح رسالة الخطأ عند تعذر الحصول على القفل الاستشاري لـ pgBackRest لتوضيح أنه ليس قفل نسخ احتياطي لـ PostgreSQL. (*اقترحه Jens Wilke.*)
- تضمين رقم إصدار pgBackRest في مخرجات سجل INFO عند بدء الأمر.
- تسجيل معرّف العملية في مخرجات سجل INFO لبدء/إيقاف العملية المحلية.

**ميزات التوثيق:**

- إضافة توثيق خيار `archive-timeout` إلى دليل المستخدم. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.08 {#v108-release-notes}

*إصلاحات أخطاء وتحسينات السجلات*

*صدر في 14 سبتمبر 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها العمليات المحلية لا تنفصل عند اكتمالها فكان يمكن أن تنتهي مهلتها لاحقًا. (*أبلغ عنه Todd Vernick.*)
- إصلاح مشكلة كان يمكن فيها لطبقة البروتوكول أن تنتهي مهلتها أثناء انتظار وصول مقاطع WAL إلى الأرشيف. (*أبلغ عنه Todd Vernick.*)

**التحسينات:**

- تخزين مخرجات سجل الملف مؤقتًا حتى يُنشأ الملف لإنشاء سجل أكثر اكتمالًا.


### ملاحظات إصدار v1.07 {#v107-release-notes}

*التحويل من الخيوط إلى العمليات وإصلاحات أخطاء*

*صدر في 7 سبتمبر 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة نسخ مساحات الجداول من الأساسي أثناء النسخ الاحتياطي من خادم الاستعداد.
- إصلاح الأمر `check` بحيث تُفحص معلومات النسخ الاحتياطي عن بُعد وليس محليًا فقط. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- إصلاح مشكلة عدم تعيين `retention-archive` تلقائيًا عندما يكون `retention-archive-type=diff`، ما أدى إلى انتهاء صلاحية أرشيف أقل عدوانية من المقصود. (*أصلحه Cynthia Shang. راجعه David Steele.*)

**الميزات:**

- تحويل خيوط Perl إلى عمليات لتحسين التوافق والأداء.
- استبعاد محتويات الدليل `$PGDATA/pg_replslot` بحيث لا تصبح خانات النسخ المتماثل على الأساسي جزءًا من النسخة الاحتياطية.
- تُملأ الآن الإعدادات `archive-start` و`archive-stop` في `backup.manifest` حتى عندما يكون `archive-check=n`. (*اقترحه Jens Wilke.*)
- تحذيرات إضافية عندما قد لا يكون لإعدادات احتفاظ الأرشيف الأثر المقصود أو تسمح بالاحتفاظ إلى أجل غير مسمى. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- دعم تجريبي للنسخ الاحتياطية غير الحصرية في PostgreSQL 9.6 rc1. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في مرشحات الإصدار اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.

**إصلاحات أخطاء التوثيق:**

- إصلاح مشكلات ثانوية في قابلية إعادة إنتاج التوثيق متعلقة بمسارات الثنائيات.

**ميزات التوثيق:**

- توثيق احتفاظ الأرشيف. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.06 {#v106-release-notes}

*النسخ الاحتياطي من خادم الاستعداد وإصلاحات أخطاء*

*صدر في 25 أغسطس 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان فيها رابط مساحة جداول يشير إلى رابط آخر لا ينتج خطأً بل يتخطى مساحة الجداول كليًا. (*أبلغ عنه Michael Vitale.*)
- إصلاح مشكلة كانت فيها خيارات لا ينبغي أن تسمح بقيم متعددة يمكن تحديدها عدة مرات في `pgbackrest.conf` دون إثارة خطأ. (*أبلغ عنه Michael Vitale.*)
- إصلاح مشكلة عدم زيادة خيار `protocol-timeout` تلقائيًا عند زيادة خيار `db-timeout`. (*أبلغ عنه Todd Vernick.*)

**الميزات:**

- النسخ الاحتياطي من عنقود خادم استعداد. لا يزال الاتصال بالعنقود الأساسي مطلوبًا لبدء/إيقاف النسخ الاحتياطي ونسخ الملفات التي لا يشملها النسخ المتماثل، لكن الغالبية العظمى من الملفات تُنسخ من خادم الاستعداد لتقليل الحمل على الأساسي.
- إعداد أكثر مرونة لقواعد البيانات. يمكن إعداد الأساسي وخادم الاستعداد معًا على خادم النسخ الاحتياطي وسيحدد pgBackRest تلقائيًا أيهما الأساسي. يعني ذلك عدم الحاجة إلى تغييرات إعداد للنسخ الاحتياطي بعد تجاوز الفشل من الأساسي إلى خادم الاستعداد عند استخدام خادم نسخ احتياطي منفصل.
- استبعاد أدلة أثناء النسخ الاحتياطي ينظفها PostgreSQL أو يعيد إنشاءها أو يصفّرها عند الإقلاع. تشمل `pgsql_tmp` و`pg_stat_tmp`. يستثنى الآن ملف `postgresql.auto.conf.tmp` إضافة إلى الملفات التي كانت مستثناة سابقًا: `backup_label.old` و`postmaster.opts` و`postmaster.pid` و`recovery.conf` و`recovery.done`.
- دعم تجريبي للنسخ الاحتياطية غير الحصرية في PostgreSQL 9.6 beta4. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.

**التحسينات:**

- تحسين رسالة الخطأ للروابط التي تشير إلى روابط عند بناء الـ manifest.
- إضافة تلميحات إلى رسالة الخطأ عند اكتشاف مسارات نسبية في `archive-push` أو `archive-get`.
- تحسين رسائل سجل النسخ الاحتياطي للإشارة إلى المضيف الذي تُنسخ منه الملفات.


### ملاحظات إصدار v1.05 {#v105-release-notes}

*إصلاح خطأ في فحص روابط مساحات الجداول*

*صدر في 9 أغسطس 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها مسارات مساحات جداول تحتوي $PGDATA كسلسلة فرعية تُحدَّد كأدلة فرعية من $PGDATA حتى عندما لم تكن كذلك. كذلك تحصين فحص المسارات النسبية قليلًا. (*أبلغ عنه Chris Fort.*)

**ميزات التوثيق:**

- إضافة توثيق لجدولة النسخ الاحتياطي باستخدام cron. (*ساهم به Cynthia Shang. راجعه David Steele.*)

**تحسينات التوثيق:**

- نقل قائمة الأعمال المعلقة من موقع pgBackRest الإلكتروني إلى ويكي مستودع GitHub. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.04 {#v104-release-notes}

*إصلاحات أخطاء متفرقة*

*صدر في 30 يوليو 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يُنشأ فيها طرف بعيد زائد قد يسبب انتهاء مهلة و/أو إطلاق تعارض أقفال للنسخ/الاستعادة بالخيوط. (*أبلغ عنه Michael Vitale.*)
- إصلاح مشكلة عدم اشتراط db-path للأمر `check` فكان يحدث فشل تحقق (assertion) عند غيابه بدلًا من رسالة خطأ مهذبة. (*أبلغ عنه Michael Vitale.*)
- إصلاح الأمر `check` لإطلاق خطأ عندما لا يطابق إصدار/معرّف قاعدة البيانات نظيره في الأرشيف. (*أصلحه Cynthia Shang. راجعه David Steele.*)
- إصلاح مشكلة كان يمكن فيها لطرف بعيد أن يحاول بدء طرفه البعيد الخاص عندما لا يكون خيار `backup-host` موجودًا في `pgbackrest.conf` على خادم قاعدة البيانات. (*أبلغ عنه Lardière Sébastien.*)
- إصلاح مشكلة نسخ محتويات `pg_xlog` احتياطيًا إذا كان الدليل رابطًا رمزيًا. لم يسبب ذلك أي مشكلات أثناء الاستعادة لكنه كان هدرًا للمساحة.
- إصلاح استدعاء `log()` غير صالح في إجراءات القفل.

**الميزات:**

- دعم تجريبي للنسخ الاحتياطية غير الحصرية في PostgreSQL 9.6 beta3. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.

**التحسينات:**

- كتم اللافتات على اتصالات بروتوكول SSH.
- تحسين رسائل الخطأ البعيدة لتحديد المضيف الذي أُثير فيه الخطأ.
- جميع أنواع الأطراف البعيدة تأخذ أقفالًا الآن. تعود الاستثناءات إلى عندما كان إطار الاختبار وpgBackRest يعملان على نفس الآلة الافتراضية ولم تعد تنطبق.

**ميزات التوثيق:**

- إضافة توضيح لسبب كون القيمة الافتراضية لخيار `backrest-user` هي `backrest`. (*اقترحه Michael Vitale.*)
- تحديث المعلومات حول توفر الحزم على المنصات المدعومة. (*اقترحه Michael Vitale.*)


### ملاحظات إصدار v1.03 {#v103-release-notes}

*الأمر check وإصلاحات أخطاء*

*صدر في 2 يوليو 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يمكن فيها أن تُحرم رسائل `keep-alives` من الإرسال بسبب الكثير من الملفات الصغيرة أثناء `backup` متعدد الخيوط. كانت أيضًا غائبة تمامًا عن استئناف `backup` أحادي/متعدد الخيوط وحساب المجاميع الاختبارية أثناء `restore`. (*أبلغ عنه Janice Parkinson، Chris Barber.*)
- إصلاح مشكلة رفض الأمر `expire` التشغيل عند استدعائه صراحة من سطر الأوامر إذا كان خيار `db-host` معيّنًا. لم تكن هذه مشكلة عندما كان `expire` يُشغَّل تلقائيًا بعد `backup` (*أبلغ عنه Chris Barber.*)
- إصلاح مشكلة تشغيل التحقق على archive_command حتى عندما يكون خيار `archive-check` معطلًا.

**الميزات:**

- إضافة الأمر `check` للتحقق من أن pgBackRest مُعد بشكل صحيح للأرشفة والنسخ الاحتياطي. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة خيار `protocol-timeout`. سابقًا كان `protocol-timeout` يُعيَّن كـ `db-timeout` + 30 ثانية.
- فشل إيقاف الأطراف البعيدة في نهاية النسخ الاحتياطي لم يعد يثير استثناءً. بدلًا من ذلك يُولَّد تحذير يوصي بقيمة `protocol-timeout` أعلى.
- دعم تجريبي للنسخ الاحتياطية غير الحصرية في PostgreSQL 9.6 beta2. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.

**التحسينات:**

- تحسين التعامل مع المستخدمين/المجموعات الملتقطة أثناء النسخ الاحتياطي وغير الموجودين على مضيف الاستعادة. أيضًا التعامل صراحة مع حالة عدم مقابلة مستخدم/مجموعة باسم.
- أصبح التعامل مع الخيارات أكثر صرامة بكثير الآن. سابقًا كان من الممكن لأمر استخدام خيار لم يُسند إليه صراحة. كان هذا صحيحًا بشكل خاص لخياري `backup-host` و`db-host` المستخدمين لتحديد المحلية.

**تحسينات التوثيق:**

- السماح باستخدام تاريخ ثابت للتوثيق لتوليد بناءات قابلة لإعادة الإنتاج. (*اقترحه Adrian Vondendriesch.*)
- إضافة توثيق الأرشفة غير المتزامنة إلى دليل المستخدم. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- أصبح موقع التثبيت الموصى به لوحدات pgBackRest الآن `/usr/share/perl5` إذ أُزيل `/usr/lib/perl5` من مسار البحث في إصدارات Perl الأحدث.
- إضافة تعليمات لإزالة الإصدارات السابقة من pgBackRest.


### ملاحظات إصدار v1.02 {#v102-release-notes}

*إصلاح خطأ لـ Perl 5.22*

*صدر في 2 يونيو 2016*

**إصلاحات الأخطاء:**

- إصلاح استخدام sprintf() بسبب قيود جديدة في Perl 5.22. لم تعد الوسائط غير المشار إليها في سلسلة التنسيق مسموحة. (*أصلحه Adrian Vondendriesch. راجعه David Steele.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح صياغة لم تكن متوافقة مع Perl 5.2X. (*أصلحه Christoph Berg، Adrian Vondendriesch. راجعه David Steele.*)
- إصلاح مسارات مطلقة كانت مستخدمة لشعار PDF. (*أبلغ عنه Adrian Vondendriesch.*)

**ميزات التوثيق:**

- فُصلت ملاحظات الإصدار الآن إلى أقسام بحيث تُميَّز الأخطاء والميزات وإعادة الهيكلة بوضوح. أُضيف قسم "ملاحظات إضافية" للتغييرات على التوثيق ومجموعة الاختبارات التي لا تؤثر في الشيفرة الأساسية.
- إضافة توليد صفحات الدليل man. (*ساهم به Adrian Vondendriesch، David Steele.*)
- كان سجل التغييرات آخر جزء من التوثيق يُعرض بصيغة Markdown فقط. كُتب محوّل بحيث يمكن إخراج المستند عبر العارضات القياسية. سيتموضع سجل التغييرات الآن على الموقع الإلكتروني وأُعيدت تسميته إلى "الإصدارات". (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v1.01 {#v101-release-notes}

*تحسين info والاستعادة الانتقائية ودعم 9.6*

*صدر في 17 مايو 2016*

**الميزات:**

- تحسين المخرجات النصية للأمر `info` لتشمل الطوابع الزمنية والأحجام وقائمة المراجع لجميع النسخ الاحتياطية. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- السماح بالاستعادة الانتقائية لقواعد البيانات من نسخة احتياطية لعنقود. يمكن أن تؤدي هذه الميزة إلى وفورات كبيرة في المساحة والوقت عند استعادة قواعد بيانات محددة فقط. لن تكون قواعد البيانات غير المستعادة قابلة للوصول لكن يجب إسقاطها يدويًا قبل إزالتها من الكتالوج المشترك. (*راجعه Cynthia Shang، Greg Smith، Stephen Frost. اقترحه Stephen Frost.*)
- دعم تجريبي للنسخ الاحتياطية غير الحصرية في PostgreSQL 9.6 beta1. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك. (*راجعه Cynthia Shang.*)


### ملاحظات إصدار v1.00 {#v100-release-notes}

*تنسيق مستودع جديد ومخطط إعداد جديد ودعم الروابط*

*صدر في 14 أبريل 2016*

**ملاحظة هامة**: يكسر هذا الإصدار الكاسر للتوافق (flag day) التوافق مع الإصدارات الأقدم من pgBackRest. تغيّر تنسيق الـ manifest والبنية على القرص ومخطط الإعداد وأسماء الملفات التنفيذية/المسارات كلها. يجب إنشاء مستودع جديد لحفظ النسخ الاحتياطية لهذا الإصدار من pgBackRest والإبقاء على مستودعك الأقدم مدةً في حال احتجت إلى استعادة. ستتطلب الاستعادة من المستودع السابق الإصدار السابق من pgBackRest، لكن بسبب تغييرات الأسماء يمكن تثبيت `1.00` وإصدار سابق من pgBackRest في الوقت نفسه. راجع الملاحظات أدناه لمعلومات أكثر تفصيلًا عما تغيّر.

**الميزات:**

- تنفيذ مخطط إعداد جديد ينبغي أن يكون أبسط بكثير في الاستخدام. راجع دليل المستخدم ومرجع الإعداد للتفاصيل، لكن للإعدادات البسيطة يمكن الآن وضع جميع الخيارات في قسم `stanza`. يمكن وضع الخيارات المشتركة بين الـ stanza في القسم `[global]`. لا يزال بالإمكان للإعدادات الأكثر تعقيدًا استخدام أقسام الأوامر رغم أن هذا ينبغي أن يكون حالة استخدام نادرة. (*اقترحه Michael Renner.*)
- يشير خيار `repo-path` الآن دائمًا إلى المستودع حيث تُخزن النسخ الاحتياطية والأرشيف، محليًا كان أو بعيدًا، لذا أُزيل خيار `repo-remote-path`. يمكن استخدام خيار `spool-path` الجديد لتعريف موقع لإدراج مقاطع WAL في قائمة انتظار عند الأرشفة غير المتزامنة. لم يعد المستودع المحلي مطلوبًا.
- اسم ملف الإعداد الافتراضي الآن `pgbackrest.conf` بدلًا من `pg_backrest.conf`. جرى ذلك للاتساق مع تغييرات التسمية الأخرى وأيضًا لمنع تحميل ملفات الإعداد القديمة عرضًا عند الانتقال إلى `1.00`. (*اقترحه Michael Renner، Stephen Frost.*)
- غُيّر اسم المستودع الافتراضي من `/var/lib/backup` إلى `/var/lib/pgbackrest`. (*اقترحه Michael Renner، Stephen Frost.*)
- تُخزن ملفات الأقفال الآن في `/tmp/pgbackrest` افتراضيًا. الموقع المفضل هذه الأيام هو `/run/pgbackrest` لكن ذلك سيتطلب سكربتات init ليست جزءًا من هذا الإصدار. يمكن استخدام خيار `lock-path` لإعداد دليل الأقفال.
- تُخزن ملفات السجلات الآن في `/var/log/pgbackrest` افتراضيًا ولم يعد يُلحق بها التاريخ بحيث يمكن إدارتها بـ `logrotate`. يمكن استخدام خيار `log-path` لإعداد دليل السجلات. (*اقترحه Stephen Frost.*)
- تغيير اسم الملف التنفيذي من `pg_backrest` إلى `pgbackrest`. (*اقترحه Michael Renner، Stephen Frost.*)
- جميع الملفات والأدلة المرتبطة من PGDATA مشمولة الآن في النسخة الاحتياطية. افتراضيًا ستُستعاد الروابط مباشرة إلى PGDATA كملفات أو أدلة. يمكن استخدام خيار `--link-all` لاستعادة جميع الروابط إلى مواقعها الأصلية. يمكن استخدام خيار `--link-map` لإعادة تعيين رابط إلى موقع جديد.
- إزالة خيار `--tablespace` واستبداله بخيار `--tablespace-map-all` الذي ينبغي أن يشير إلى وظيفته بوضوح أكبر.
- إضافة مستوى سجل `detail` الذي سيُخرج معلومات أكثر من `info` دون أن يكون مطنبًا مثل `debug`.


--------

## إصدارات ما قبل الاستقرار {#pre-stable-releases}


### ملاحظات إصدار v0.92 {#v092-release-notes}

*إصلاح مسار المستودع في سطر الأوامر*

*صدر في 6 أبريل 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كانت فيها العملية الرئيسية تمرر `--repo-remote-path` بدلًا من `--repo-path` إلى الطرف البعيد مسببة إنشاء ملفات الأقفال في دليل المستودع الافتراضي (`/var/lib/backup`)، ما ينتهي بالفشل عمومًا. كانت هذه مشكلة فقط عندما كان `--repo-remote-path` معرّفًا في سطر الأوامر بدلًا من `pg_backrest.conf`. (*أبلغ عنه Jan Wieck.*)


### ملاحظات إصدار v0.91 {#v091-release-notes}

*إصلاح خطأ مساحات الجداول وتحسينات طفيفة*

*صدر في 22 مارس 2016*

**إصلاح خطأ هام لمساحات الجداول**: قُدِّم بالخطأ تغيير على تنسيق المستودع في 0.90 ما يعني أن النسخة الاحتياطية على القرص لم تعد عنقود PostgreSQL صالحًا عندما احتوت النسخة مساحات جداول. أثّر هذا فقط في المستخدمين الذين نسخوا النسخ الاحتياطية مباشرة لاستعادة عناقيد PostgreSQL بدلًا من استخدام أمر الاستعادة. لكن الإصلاح يكسر التوافق مع النسخ الاحتياطية الأقدم التي تحتوي مساحات جداول بغض النظر عن طريقة استعادتها (سيرمي pgBackRest أخطاءً ويرفض الاستعادة). ينبغي أخذ نسخ احتياطية كاملة جديدة فورًا بعد تثبيت الإصدار 0.91 لأي عناقيد تحتوي مساحات جداول. إذا كانت هناك حاجة لاستعادة نسخ احتياطية أقدم فاستخدم إصدار pgBackRest الذي يطابق إصدار النسخة الاحتياطية.

**إصلاحات الأخطاء:**

- إصلاح عدم توافق المستودع المقدَّم في pgBackRest 0.90. (*أبلغ عنه Evan Benoit.*)

**الميزات:**

- نسخ `global/pg_control` أخيرًا أثناء النسخ الاحتياطي.
- كتابة ملفات `.info` و`.manifest` إلى مؤقت قبل نقلها إلى مواقعها النهائية مع fsync.
- إعادة تسمية خيار `--no-start-stop` إلى `--no-online`.

**ميزات مجموعة الاختبارات:**

- تحليل مصدر ثابت باستخدام Perl-Critic، يجتاز حاليًا بالمستوى gentle.


### ملاحظات إصدار v0.90 {#v090-release-notes}

*دعم 9.5 وتحسينات متفرقة وإصلاحات أخطاء ثانوية*

*صدر في 7 فبراير 2016*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان فيها تحديد `--no-archive-check` يرمي خطأ إعداد. (*أبلغ عنه Jason O'Donnell.*)
- إصلاح مشكلة كان يمكن فيها لملف WAL مؤقت متبقٍ بعد انهيار نظام في توقيت مناسب أن يفشل `archive-push` التالي.
- يمكن الآن تعيين خيار `retention-archive` بأمان إلى أقل من احتفاظ النسخ الاحتياطي (`retention-full` أو `retention-diff`) دون تحديد `archive-copy=n` أيضًا. سيُحفظ في الأرشيف WAL اللازم لجعل النسخ الاحتياطية الواقعة خارج احتفاظ الأرشيف متسقة. لكن في هذه الحالة لن تكون الاستعادة إلى نقطة زمنية (PITR) ممكنة للنسخ الاحتياطية الواقعة خارج احتفاظ الأرشيف.

**الميزات:**

- عند النسخ الاحتياطي لمساحات الجداول واستعادتها يعمل pgBackRest على الدليل الفرعي المنشأ لإصدار PostgreSQL الجاري العمل عليه فقط. وبما أن إصدارات متعددة يمكن أن تعيش في مساحة جداول (خاصة أثناء ترقية ثنائية) فهذا يمنع نسخ ملفات كثيرة أكثر من اللازم أثناء النسخ الاحتياطي ومحو إصدارات أخرى احتماليًا أثناء الاستعادة. ينطبق هذا على PostgreSQL >= 9.0 فقط — الإصدارات السابقة من PostgreSQL لم تكن تستطيع مشاركة دليل مساحة جداول.
- توليد خطأ عندما يكون `archive-check=y` لكن `archive_command` لا ينفّذ `pg_backrest`. (*ساهم به Jason O'Donnell. راجعه David Steele.*)
- تحسين رسالة الخطأ عندما لا يكون `repo-path` أو `repo-remote-path` موجودًا.
- إضافة فحوصات لخياري استعادة `--delta` و`--force` لضمان أن الوجهة دليل $PGDATA صالح. سيفحص pgBackRest عن وجود `PG_VERSION` أو `backup.manifest` (المتبقي من استعادة ملغاة). إذا لم يُعثر على أي من الملفين فسيُعطّل `--delta` و`--force` لكن الاستعادة ستتابع ما لم تكن هناك ملفات في دليل $PGDATA (أو أي أدلة مساحات جداول) وفي هذه الحالة ستُلغى العملية.
- عند `--set=latest` للاستعادة (الافتراضي) ستُخرج النسخة الاحتياطية الفعلية المستعادة إلى السجل.
- دعم مقاطع WAL الجزئية وإعداد `recovery_target_action` في PostgreSQL 9.5. إعداد `archive_mode = 'always'` غير مدعوم بعد.
- دعم إعداد استرداد `recovery_target = 'immediate'` المقدَّم في PostgreSQL 9.4.
- أُضيفت فحوصات مساحات الجداول التالية: مسارات أو ملفات في pg_tblspc، روابط نسبية في pg_tblspc، مساحات جداول في $PGDATA. الثلاثة كلها ستولّد أخطاء.


### ملاحظات إصدار v0.89 {#v089-release-notes}

*إصلاح خطأ المهلة واستعادة من مستودعات للقراءة فقط*

*صدر في 24 ديسمبر 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة انتهاء مهلة النسخ/الاستعادة الأطول تشغيلًا عند العمل البعيد وبالخيوط. تُستخدم الآن رسائل keepalive للتأكد من أن الطرف البعيد للعملية الرئيسية لا تنتهي مهلته بينما تقوم الأطراف البعيدة للخيوط بكل العمل. حُسّنت أيضًا رسالة الخطأ للمهل لتسهيل التنقيح. (*أبلغ عنه Stephen Frost.*)

**الميزات:**

- السماح بإجراء الاستعادة على مستودع للقراءة فقط باستخدام `--no-lock` و`--log-level-file=off`. لا يمكن استخدام خيار `--no-lock` إلا مع الاستعادة.


### ملاحظات إصدار v0.88 {#v088-release-notes}

*توثيق وإصلاحات أخطاء ثانوية*

*صدر في 22 نوفمبر 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة اشتراط الأمرين `start`/`stop` لخيار `--config`. (*أبلغ عنه Dmitry Didovicher.*)
- إصلاح مشكلة الكتابة فوق ملفات السجلات بدلًا من الإلحاق إليها. (*أبلغ عنه Stephen Frost، Dmitry Didovicher.*)
- إصلاح مشكلة عدم كون `backup-user` اختياريًا.

**الميزات:**

- لم تعد الروابط الرمزية تُنشأ في أدلة النسخ الاحتياطي في المستودع. كانت هذه الروابط يمكن أن تشير إلى أي مكان تقريبًا وأن تشكّل خطرًا محتملًا. لا يزال يُعاد إنشاء الروابط الرمزية أثناء الاستعادة. (*اقترحه Stephen Frost.*)
- إضافة رسائل أفضل لانتهاء صلاحية النسخ الاحتياطية. يُسجَّل انتهاء صلاحية النسخ الكاملة والتفاضلية في سطر واحد مع قائمة بجميع النسخ الاحتياطية التابعة المنتهية صلاحيتها.
- يُعيَّن احتفاظ الأرشيف تلقائيًا إلى احتفاظ النسخ الاحتياطي الكامل إذا لم يُعد صراحة.

**ميزات التوثيق:**

- إضافة توثيق في دليل المستخدم للاستعادة بالدلتا وانتهاء الصلاحية ومضيفات النسخ الاحتياطي المخصصة وبدء وإيقاف pgBackRest والنسخ المتماثل.


### ملاحظات إصدار v0.87 {#v087-release-notes}

*الموقع الإلكتروني ودليل المستخدم*

*صدر في 28 أكتوبر 2015*

**الميزات:**

- ملفا `backup_label.old` و`recovery.done` مستثنيان الآن من النسخ الاحتياطي.

**ميزات التوثيق:**

- إضافة دليل مستخدم جديد يغطي أساسيات pgBackRest وبعض الموضوعات المتقدمة بما فيها PITR. المزيد قادم، لكنها بداية. (*ساهم به David Steele، Stephen Frost. راجعه Michael Renner، Cynthia Shang، Eric Radman، Dmitry Didovicher.*)


### ملاحظات إصدار v0.85 {#v085-release-notes}

*أمرا البدء والإيقاف وإصلاحات أخطاء ثانوية*

*صدر في 8 أكتوبر 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة كان يمكن فيها إرجاع خطأ بعد نسخة احتياطية أو استعادة ناجحة تمامًا.
- إصلاح مشكلة فشل الاستئناف إذا تُركت ملفات مؤقتة في الدليل الجذري للنسخة الاحتياطية عند فشلها. كان هذا السيناريو مرجحًا إذا أُنهيت عملية النسخ الاحتياطي خلال مرحلة النسخ.

**الميزات:**

- إضافة الأمرين `stop` و`start` لمنع عمليات pgBackRest من العمل على نظام أُوقف فيه PostgreSQL أو يحتاج إلى إيقاف نشاطه مؤقتًا لسبب آخر.
- دعم تجريبي لـ PostgreSQL 9.5 beta1. قد يتعطل هذا الدعم عند تغير إصدار ملف التحكم أو الرقم السحري لـ WAL في الإصدارات المستقبلية لكن سيُحدَّث في كل إصدار من pgBackRest لمواكبة ذلك. تجتاز جميع اختبارات الانحدار عدا اختبارات `--target-resume` (هذه الوظيفة تغيرت في 9.5) ولا يوجد اختبار بعد لمقاطع WAL ذات `.partial`.


### ملاحظات إصدار v0.82 {#v082-release-notes}

*إعادة الهيكلة ومساعدة سطر الأوامر وإصلاحات أخطاء ثانوية*

*صدر في 14 سبتمبر 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة عدم حفظ النسخ الاحتياطية المضغوطة المستأنفة للملفات الموجودة.
- إصلاح مشكلة عدم ضمان الاستئناف وincr/diff أن النسخة الاحتياطية السابقة لها نفس إعدادات الضغط والروابط الصلبة.
- إصلاح مشكلة إمكانية بدء نسخة احتياطية باردة باستخدام `--no-start-stop` على عنقود PostgreSQL قيد التشغيل دون تحديد `--force`.
- إصلاح مشكلة إمكانية بدء خيط حتى عندما لا يُطلب أي خيط.
- إصلاح مشكلة عدم تحديث رقم إصدار pgBackRest في `backup.info` و`archive.info` بعد ترقية/تراجع.
- إصلاح مشكلة رمي الأمر `info` استثناءً عندما لا يحتوي المستودع على أي stanza. (*أبلغ عنه Stephen Frost.*)
- إصلاح مشكلة إخراج إشعارات `pg_stop_backup()` في PostgreSQL إلى `stderr`. (*أبلغ عنه Stephen Frost.*)

**الميزات:**

- دعم تجريبي لـ PostgreSQL 9.5 alpha2. قد يتعطل هذا الدعم عند تغير إصدار ملف التحكم أو الرقم السحري لـ WAL في الإصدارات المستقبلية لكن سيُحدَّث في كل إصدار من pgBackRest لمواكبة ذلك. تجتاز جميع اختبارات الانحدار عدا اختبارات `--target-resume` (هذه الوظيفة تغيرت في 9.5) ولا يوجد اختبار بعد لمقاطع WAL ذات `.partial`.

**التحسينات:**

- إعادة تسمية الخيار والقسم `recovery-setting` إلى `recovery-option` ليكون أكثر اتساقًا مع أعراف تسمية pgBackRest.
- إضافة تحميل ديناميكي للوحدات لتسريع الأوامر، خاصة الأرشفة غير المتزامنة.

**ميزات التوثيق:**

- تُستخرج مساعدة سطر الأوامر الآن من نفس مصدر XML المستخدم لبقية التوثيق وتتضمن تفاصيل أكثر بكثير.


### ملاحظات إصدار v0.80 {#v080-release-notes}

*دعم DBI والاستقرار وميزات الملاءمة*

*صدر في 9 أغسطس 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة تسببت في الإبلاغ عن الطابع الزمني المنسق لأقدم وأحدث النسخ الاحتياطية كالوقت الحالي من قبل الأمر `info`. تأثرت مخرجات `text` فقط -- أبلغت مخرجات `json` عن قيم epoch الصحيحة. (*أبلغ عنه Michael Renner.*)
- إصلاح مشكلة بروتوكول كانت تمنع تسجيل أخطاء ssh (خاصة عند الاتصال).

**الميزات:**

- يُنشأ المستودع الآن ويُحدَّث بأوضاع أدلة وملفات متسقة. افتراضيًا يُعيَّن `umask` إلى `0000` لكن يمكن تعطيل ذلك بإعداد `neutral-umask`. (*اقترحه Cynthia Shang.*)
- إضافة خيار `stop-auto` للسماح بإيقاف النسخ الاحتياطية الفاشلة تلقائيًا عند بدء نسخة احتياطية جديدة.
- إضافة خيار `db-timeout` لتحديد مقدار الوقت الذي سينتظره pgBackRest لعودة `pg_start_backup()` و`pg_stop_backup()`.
- إزالة ملف `pg_control` في بداية الاستعادة ونسخه مجددًا في النهاية تمامًا. يمنع ذلك احتمال أن يشغّل PostgreSQL عنقودًا لم تكتمل استعادته.
- إضافة فحوصات للتأكد من أن إعداد `db-path` متسق مع `db-port` عبر مقارنة `data_directory` كما يبلغ عنه العنقود بإعداد `db-path`، ومقارنة الإصدار كما يبلغ عنه العنقود بالقيمة المقروءة من `pg_control`. يُفحص إعداد `db-socket-path` للتأكد من أنه مسار مطلق.
- دعم تجريبي لـ PostgreSQL 9.5 alpha1. قد يتعطل هذا الدعم عند تغير إصدار ملف التحكم أو الرقم السحري لـ WAL في الإصدارات المستقبلية لكن سيُحدَّث في كل إصدار من pgBackRest لمواكبة ذلك. تجتاز جميع اختبارات الانحدار عدا اختبارات `--target-resume` (هذه الوظيفة تغيرت في 9.5) ولا يوجد اختبار بعد لمقاطع WAL ذات `.partial`.

**التحسينات:**

- الاستخدام الآن لـ `DBI` و`DBD::Pg` في Perl للاتصالات بـ PostgreSQL بدلًا من `psql`. أُزيل الإعدادان `cmd-psql` و`cmd-psql-option` واستُبدلا بـ `db-port` و`db-socket-path`. اتبع التعليمات في دليل التثبيت لتثبيت `DBD::Pg` على نظام التشغيل لديك.

**ميزات مجموعة الاختبارات:**

- إضافة إعدادات اختبار vagrant لأوبونتو 14.04 وCentOS 7.


### ملاحظات إصدار v0.78 {#v078-release-notes}

*إزالة تبعيات CPAN وتحسينات الاستقرار*

*صدر في 13 يوليو 2015*

**التحسينات:**

- إزالة التبعية على حزم CPAN للعمل متعدد الخيوط. رغم أنه قد لا تكون فكرة سيئة تحديث حزمتي `threads` و`Thread::Queue`، لم يعد ذلك ضروريًا.
- تعديل تراجع الانتظار لاستخدام متتالية فيبوناتشي بدلًا من هندسية. سيجعل ذلك زمن الانتظار ينمو بعدوانية أقل مع إعطاء قيم معقولة.

**ميزات مجموعة الاختبارات:**

- إضافة إعدادات اختبار vagrant لأوبونتو 12.04 وCentOS 6.


### ملاحظات إصدار v0.77 {#v077-release-notes}

*دعم CentOS/RHEL 6 وتحسينات البروتوكول*

*صدر في 30 يونيو 2015*

**الميزات:**

- إضافة مزامنة الملفات والأدلة إلى الكائن `File` لأمان إضافي أثناء النسخ/الاستعادة والأرشفة. (*اقترحه Andres Freund.*)
- إضافة دعم Perl 5.10.1 وOpenSSH 5.3 وهما الافتراضيان لـ CentOS/RHEL 6. (*اقترحه Eric Radman.*)
- تحسين رسالة الخطأ عند تشغيل النسخ الاحتياطي دون تعيين `archive_command` ودون تحديد `--no-archive-check`. (*اقترحه Eric Radman.*)


### ملاحظات إصدار v0.75 {#v075-release-notes}

*تنسيق مستودع جديد وأمر info ودعم تجريبي لـ 9.5*

*صدر في 14 يونيو 2015*

**ملاحظة هامة**: يكسر هذا الإصدار الكاسر للتوافق (flag day) التوافق مع الإصدارات الأقدم من pgBackRest. تغيّر تنسيق الـ manifest والبنية على القرص وأسماء الثنائيات كلها. يجب إنشاء مستودع جديد لحفظ النسخ الاحتياطية لهذا الإصدار من pgBackRest والإبقاء على مستودعك الأقدم مدةً في حال احتجت إلى استعادة. لم يتغير ملف `pg_backrest.conf` لكنك ستحتاج إلى تغيير أي إشارات إلى `pg_backrest.pl` في cron (أو غيره) إلى `pg_backrest` (دون الامتداد `.pl`).

**الميزات:**

- إضافة الأمر `info`.
- يستخدم التسجيل الآن مخرجات غير مخزّنة مؤقتًا. ينبغي أن يجعل ذلك ملفات السجلات التي تكتبها خيوط متعددة أقل فوضى. (*اقترحه Michael Renner.*)
- دعم تجريبي لـ PostgreSQL 9.5. قد يتعطل هذا الدعم عند تغير إصدار ملف التحكم أو الرقم السحري لـ WAL لكن سيُحدَّث في كل إصدار.

**التحسينات:**

- ترتيب ملفات أكثر كفاءة لـ`backup`. تُنسخ الملفات بترتيب حجم تنازلي بحيث لا ينتهي الأمر بخيط واحد ينسخ ملفًا كبيرًا في النهاية. كان هذا منفَّذًا بالفعل لـ`restore`.


### ملاحظات إصدار v0.70 {#v070-release-notes}

*تحسينات استقرار الأرشفة وتحسين التسجيل والمساعدة*

*صدر في 1 يونيو 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة فشل `archive-copy` على نسخة احتياطية incr/diff عندما يكون `hardlink=n`. في هذه الحالة لا يكون مسار `pg_xlog` موجودًا مسبقًا ويجب إنشاؤه. (*أبلغ عنه Michael Renner.*)
- إصلاح مشكلة في الأرشفة غير المتزامنة كانت فيها `archive-push` لا تعيد 0 بشكل صحيح عند بلوغ `archive-max-mb`، ونقل الفحص غير المتزامن إلى ما بعد النقل لتجنب الاضطرار إلى إزالة ملف التوقف مرتين. أيضًا إضافة اختبارات وحدة لهذه الحالة وتحسين رسائل الخطأ لتوضيح ما الذي حدث للمستخدم. (*أبلغ عنه Michael Renner.*)
- إصلاح مشكلة قفل كانت تسمح بعمليات متعددة من نفس النوع ضد stanza واحدة. بدت هذه حميدة من حيث سلامة البيانات لكنها سببت أخطاء زائفة أثناء الأرشفة وكان يمكن أن تؤدي إلى أخطاء في النسخ/الاستعادة. (*أبلغ عنه Michael Renner.*)

**الميزات:**

- السماح بأرشفة مقاطع WAL المكررة عندما يتطابق المجموع الاختباري. هذا ضروري لبعض سيناريوهات الاسترداد.
- السماح بالتعليقات/التعطيل في `pg_backrest.conf` باستخدام المحرف `#`. لا تُحترم إلا محارف `#` في أول محرف من السطر. (*اقترحه Michael Renner.*)
- تسجيل أفضل قبل `pg_start_backup()` لتوضيح متى تنتظر النسخة الاحتياطية نقطة تحقق. (*اقترحه Michael Renner.*)
- إصلاحات متنوعة لسلوك الأوامر والتسجيل. (*راجعه Michael Renner. اقترحه Michael Renner.*)

**التحسينات:**

- استبدال وحدة `JSON` بـ`JSON::PP` التي تأتي مع Perl الأساسية.

**إصلاحات أخطاء التوثيق:**

- إصلاحات مساعدة متنوعة. (*راجعه Michael Renner. أبلغ عنه Michael Renner.*)


### ملاحظات إصدار v0.65 {#v065-release-notes}

*تحسين الاستئناف وتسجيل الاستعادة واستعادات مدمجة*

*صدر في 11 مايو 2015*

**إصلاحات الأخطاء:**

- إصلاح مشكلة عدم كتابة مسار مطلق في `recovery.conf` عندما تُشغَّل الاستعادة بمسار نسبي.

**الميزات:**

- دعم أفضل للاستئناف. تُفحص الملفات المستأنفة للتأكد من عدم تعديلها ويُحفظ الـ manifest أكثر للاحتفاظ بالمجاميع الاختبارية مع تقدم النسخ الاحتياطي. مزيد من اختبارات الوحدة للتحقق من كل حالة استئناف.
- أصبح الاستئناف اختياريًا الآن. استخدم إعداد `resume` أو `--no-resume` من سطر الأوامر للتعطيل.
- مزيد من رسائل المعلومات أثناء الاستعادة. سابقًا كانت معظم رسائل الاستعادة بمستوى debug لذا لم يكن يُخرج الكثير في السجل.
- إضافة إعداد `tablespace` للسماح باستعادة مساحات الجداول إلى مسار `pg_tblspc`. ينتج ذلك استعادات مدمجة ملائمة للتطوير والتهيئة التجريبية وغيرها. حاليًا لا يمكن النسخ الاحتياطي لهذه الاستعادات إذ يتوقع pgBackRest روابط فقط في مسار `pg_tblspc`.


### ملاحظات إصدار v0.61 {#v061-release-notes}

*إصلاح خطأ للوجهة البعيدة غير المضغوطة*

*صدر في 21 أبريل 2015*

**إصلاحات الأخطاء:**

- إصلاح خطأ تخزين مؤقت قد يحدث على ملفات كبيرة عالية القابلية للضغط عند النسخ إلى وجهة بعيدة غير مضغوطة. اكتُشف الخطأ في شيفرة فك الضغط وأسفر عن نسخة احتياطية فاشلة بدلًا من إفساد لذا لا ينبغي أن يؤثر في النسخ الاحتياطية الناجحة المصنوعة بإصدارات سابقة.


### ملاحظات إصدار v0.60 {#v060-release-notes}

*دعم أفضل للإصدارات وتحسينات WAL*

*صدر في 19 أبريل 2015*

**إصلاحات الأخطاء:**

- دفع WAL المكرر يولّد الآن خطأً. كان هذا يعمل سابقًا فقط إذا كانت المجاميع الاختبارية معطلة.

**الميزات:**

- استخدام معرفات نظام قاعدة البيانات للتأكد من أن كل WAL في أرشيف متطابق. ينبغي أن يساعد ذلك في منع الإعدادات الخاطئة التي ترسل WAL من عناقيد متعددة إلى نفس الأرشيف.

**ميزات مجموعة الاختبارات:**

- اختبارات انحدار تعمل حتى PostgreSQL 8.3.


### ملاحظات إصدار v0.50 {#v050-release-notes}

*الاستعادة والمزيد*

*صدر في 25 مارس 2015*

**إصلاحات الأخطاء:**

- إصلاح المجاميع الاختبارية المعطلة والآن تعمل مع النسخ الاحتياطية العادية والمستأنفة. أدركنا أخيرًا أنه ينبغي فصل المجاميع الاختبارية ودلتات المجاميع وظيفيًا وقد بسّط ذلك عددًا من الأمور. أُنشئت المشكلة #28 لدلتات المجاميع.
- إصلاح مشكلة إمكانية استئناف نسخة احتياطية من نسخة ملغاة لم تكن مطابقة في النوع والنسخة الاحتياطية السابقة.

**الميزات:**

- إضافة وظيفة الاستعادة.
- يمكن الآن تعيين جميع الخيارات في سطر الأوامر ما يجعل `pg_backrest.conf` اختياريًا.
- يُنفَّذ الضغط/فك الضغط الآن دون خيوط ويُحسب المجموع الاختباري/الحجم في التدفق. يعني ذلك أن المجاميع الاختبارية للملفات لم تعد اختيارية.
- إضافة خيار `--no-start-stop` للسماح بالنسخ الاحتياطي عند إيقاف Postgres. إذا كان `postmaster.pid` موجودًا فسيُطلب `--force` لتشغيل النسخ الاحتياطي (رغم أنه إذا كان Postgres قيد التشغيل فستُنشأ على الأرجح نسخة احتياطية غير متسقة). أُضيف هذا الخيار في المقام الأول لغرض اختبار الوحدة، لكن قد تكون هناك تطبيقات له في العالم الحقيقي أيضًا.
- مجموع اختباري لـ`backup.manifest` لاكتشاف manifest فاسد/معدل.
- يشير الرابط `latest` دائمًا إلى آخر نسخة احتياطية. أُضيف هذا للتسهيل وتبسيط الاستعادة.

**ميزات مجموعة الاختبارات:**

- اختبارات وحدة أكثر شمولًا في جميع المجالات.


### ملاحظات إصدار v0.30 {#v030-release-notes}

*إعادة هيكلة النواة واختبارات الوحدة*

*صدر في 5 أكتوبر 2014*

**ميزات التوثيق:**

- إضافة توثيق كان مطلوبًا بشدة

**ميزات مجموعة الاختبارات:**

- اختبارات وحدة شاملة إلى حد بعيد لجميع العمليات الأساسية. لا شك أن هناك عملًا أكثر ينبغي عمله هنا، لكن هناك دائمًا عمل أكثر ينبغي عمله على اختبارات الوحدة.


### ملاحظات إصدار v0.19 {#v019-release-notes}

*تحسين الإبلاغ عن الأخطاء/معالجتها*

*صدر في 13 مايو 2014*

**إصلاحات الأخطاء:**

- العثور على خطأ خبيث وسحقه حيث كانت `file_copy()` مهيّأة افتراضيًا لتجاهل الأخطاء. كانت هناك أيضًا مشكلة في `file_exists()` تسبب فشل الاختبار عندما يكون الملف موجودًا فعلًا. معًا كان يمكن أن ينتج عنهما نسخ احتياطي فاسد دون أخطاء، رغم أنه غير مرجح جدًا.


### ملاحظات إصدار v0.18 {#v018-release-notes}

*إرجاع خطأ غير فادح عند فقدان الأرشيف*

*صدر في 13 أبريل 2014*

**إصلاحات الأخطاء:**

- يعيد الأمر `archive-get` الآن 1 عندما يكون ملف الأرشيف مفقودًا للتمايز عن الأخطاء الفادحة (فشل اتصال ssh، خطأ نسخ ملف، إلخ) يعرف PostgreSQL بذلك أن تدفق الأرشيف انتهى بشكل طبيعي. لكن هذا لا يأخذ في الحسبان الفجوات المحتملة في تدفق الأرشيف. (*أبلغ عنه Stephen Frost.*)


### ملاحظات إصدار v0.17 {#v017-release-notes}

*إصدار تحذير عند تعذر حذف أدلة الأرشيف*

*صدر في 3 أبريل 2014*

**إصلاحات الأخطاء:**

- إذا تعذر حذف دليل أرشيف ينبغي أن يكون فارغًا كان backrest يرمي خطأً. هناك إصلاح جيد لذلك قادم، لكن مؤقتًا غُيّر إلى تحذير بحيث تستمر المعالجة. كان هذا يؤثر في النسخ الاحتياطي إذ أحيانًا لم يكن ملف الأرشيف الأخير يُدفع إذا كان ملف الأرشيف الأول في دليل مختلف (مع بعض الحظ السيئ).


### ملاحظات إصدار v0.16 {#v016-release-notes}

*RequestTTY=yes لجلسات SSH*

*صدر في 1 أبريل 2014*

**إصلاحات الأخطاء:**

- إضافة `RequestTTY=yes` لجلسات ssh. على أمل أن يمنع هذا حالات الجمود العشوائية.


### ملاحظات إصدار v0.15 {#v015-release-notes}

*إضافة archive-get*

*صدر في 29 مارس 2014*

**الميزات:**

- إضافة وظيفة `archive-get` للمساعدة في الاستعادة.
- إضافة خيار لفرض نقطة تحقق عند بدء النسخ الاحتياطي، `start-fast=y`.


### ملاحظات إصدار v0.11 {#v011-release-notes}

*إصلاحات طفيفة*

*صدر في 26 مارس 2014*

**إصلاحات الأخطاء:**

- إزالة خيار `master_stderr_discard` على اتصالات SSH لقاعدة البيانات. حدثت حالات جمود متقطعة وقد تكون مرتبطة بمشكلات شوهدت في الأصل في شيفرة الملفات. (*أبلغ عنه Stephen Frost.*)
- تغيير تعارضات ملفات القفل للأمرين `backup` و`expire` إلى `ERROR`. كانت معيّنة إلى `DEBUG` بسبب نسخ ولصق من أقفال الأرشيف.


### ملاحظات إصدار v0.10 {#v010-release-notes}

*عمل النسخ الاحتياطي والأرشفة*

*صدر في 5 مارس 2014*

**الميزات:**

- لا توجد وظيفة استعادة، لكن أدلة النسخ الاحتياطي أدلة بيانات PostgreSQL متسقة. ستحتاج إما إلى فك ضغط الملفات أو إيقاف الضغط في النسخ الاحتياطي. النسخ الاحتياطية غير المضغوطة على نظام ملفات ZFS (أو ما شابه) خيار جيد لأنه يمكن استعادة النسخ الاحتياطية محليًا عبر لقطة لإنشاء نسخ احتياطية منطقية أو إجراء استرداد بيانات موضعي.
- الأرشفة أحادية الخيط. لم يشكل هذا مشكلة على قواعد بياناتنا متعددة التيرابايت ذات حجم كبير من عمليات الكتابة. نوصي بوحدة تخزين كبيرة لـ WAL أو استخدام الخيار غير المتزامن مع وحدة تخزين كبيرة قريبة.
- النسخ الاحتياطي متعدد الخيوط، لكن مكتبة `Net::OpenSSH` لا تبدو آمنة للخيوط 100% لذا ستجمُد أحيانًا نادرًا على خيط. توجد مهلة عملية شاملة تحل هذه المشكلة بقتل العملية. نعم، قبيح جدًا.
- تُفقد المجاميع الاختبارية على أي نسخة احتياطية مستأنفة. النسخة الاحتياطية النهائية فقط ستسجل المجموع عند استئنافات متعددة. تُسجل المجاميع من النسخ الاحتياطية السابقة بشكل صحيح وستعيد النسخة الكاملة تعيين كل شيء.
- يُكتب `backup.manifest` بصيغة `Storable` لأن `Config::IniFile` لا يبدو أنه يتعامل مع الملفات الكبيرة جيدًا. نتمنى بالتأكيد حفظها كنص مقروء بشريًا.

**ميزات التوثيق:**

- لا توثيق على الإطلاق (خارج الشيفرة). حسنًا، باستثناء ملاحظات الإصدار هذه.
