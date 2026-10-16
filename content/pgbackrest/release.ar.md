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

تتكون أرقام إصدارات pgBackRest من جزأين: رئيسي وثانوي. قد *يكسر* الإصدار الرئيسي التوافق مع الإصدار الرئيسي السابق، لكن إصدارات v2 متوافقة تمامًا مع مستودعات v1 وستقبل جميع خيارات v1. يمكن أن تتضمن الإصدارات الثانوية إصلاحات أخطاء وميزات لكنها لا تغيّر تنسيق المستودع وتسعى إلى تجنّب تغيير الخيارات والتسميات. يمكن العثور على توثيق إصدار v1 [هنا](https://pgbackrest.org/1). قد تتضمن ملاحظات الإصدار أيضًا قسم "ملاحظات إضافية" لكن التغييرات في هذا القسم تخص التوثيق أو مجموعة الاختبارات فقط وليس لها تأثير مباشر على قاعدة شيفرة pgBackRest.


--------

## الإصدار المستقر الموثّق {#current-stable-release}

يغطي هذا التوثيق المطابق الإصدار v2.59.3. راجع [سجل إصدارات المنبع](https://pgbackrest.org/release.html) للإصدارات الأحدث.

### ملاحظات إصدار v2.59.3 {#v2593-release-notes}

*خلل المفاتيح الفرعية الضعيفة للتشفير*

*صدر في 4 أكتوبر 2026*

**ملاحظة هامة**: في الإصدارات السابقة كان من الممكن أن تُولَّد مفاتيح فرعية للتشفير وأملاح ضعيفة إذا حدث خطأ أثناء الوصول إلى بيانات العشوائية الخاصة بالنظام. راجع [المفاتيح الفرعية والأملاح الضعيفة للتشفير](/ar/pgbackrest/news/#weak-encryption) لمزيد من المعلومات.

**إصلاحات الأخطاء:**

- إصلاح خطأ محتمل في المجموع الاختباري عند تحميل ملفات المعلومات والـ manifest المشفّرة. (*أصلحه j0uinim. راجعه David Steele.*)
- إصلاح احتمال توليد مفاتيح فرعية/أملاح ضعيفة للتشفير. (*أصلحه j0uinim. راجعه David Steele، Stefan Fercot، Douglas J Hunley.*)


--------

## الإصدارات المستقرة {#stable-releases}


### ملاحظات إصدار v2.59.2 {#v2592-release-notes}

*دعم PostgreSQL 19beta4*

*صدر في 27 سبتمبر 2026*

**إصلاحات الأخطاء:**

- إصلاح خريطة الكتل الفارغة عندما يُقتطع ملف إلى الصفر أثناء النسخ الاحتياطي. (*راجعه Douglas J Hunley. أبلغ عنه JPCOSTA78.*)
- تعطيل إعادة محاولة القراءة عند تمرير مرشّحات إلى المشغّل. (*راجعه Douglas J Hunley. أبلغ عنه megamaced.*)
- إصلاح التقسيم إلى صفحات لإدراج إصدارات S3. (*راجعه Douglas J Hunley، guruguruguru. أبلغ عنه guruguruguru.*)
- تعيين ترويسة إصدار Azure لمصادقة SAS. (*راجعه Douglas J Hunley. أبلغ عنه Florian Helmberger.*)
- إصلاح تعطّل `archive-push` غير المتزامن عند وجود ملف تاريخ نسخ احتياطي بحجم صفري. (*أصلحه Andrew Kroh. راجعه David Steele، Douglas J Hunley.*)
- إصلاح الأمر `annotate` على مستودع بعيد مشفّر. (*أصلحه Douglas J Hunley. راجعه David Steele.*)

**الميزات:**

- دعم PostgreSQL 19beta4.



### ملاحظات إصدار v2.59.1 {#v2591-release-notes}

*دعم PostgreSQL 19beta3*

*صدر في 17 أغسطس 2026*

**إصلاحات الأخطاء:**

- إصلاح التعليق عندما يكون مخزن القطع المؤقت أصغر من المخزن المؤقت للإدخال. (*راجعه Andrew Pogrebnoi، Douglas J Hunley. أبلغ عنه crajac66.*)
- مقارنة وسم النسخة الاحتياطية الجديد بمجموعة النسخ الاحتياطية الكاملة الخاصة بها فقط. (*راجعه Douglas J Hunley. أبلغ عنه Anton Glushakov.*)
- إصلاح نقص ملفات مطلوبة للبناء في الأرشيفات المصدرية التي يولّدها GitHub. (*أبلغ عنه aardvarkzed.*)

**الميزات:**

- دعم PostgreSQL 19beta3. (*ساهم به Lardière Sébastien. راجعه David Steele.*)

**تحسينات التوثيق:**

- توثيق استثناء النقاط في أسماء حاويات S3 عندما يكون `repo-s3-uri-style=path`.
- إزالة إعداد `hot_standby` الصريح من دليل المستخدم.


### ملاحظات إصدار v2.59.0 {#v2590-release-notes}

*دعم PostgreSQL 19beta2*

*صدر في 20 يوليو 2026*

**ملاحظة لمعدّي الحزم**: تتوفر الآن حزمة توزيع (tarball) جديدة تبسّط عملية البناء عبر توفير توثيق HTML وصفحة دليل man وشيفرة مولّدة مسبقًا. تُرفق الحزمة بكل إصدار كأصل وتحمل الاسم `pgbackrest-{version}.tar.gz`. راجع `README.md` داخل الحزمة للتفاصيل. يرجى استخدام حزمة التوزيع الجديدة لتجنّب أدوات البناء الإضافية المطلوبة لتوليد الشيفرة في الإصدارات المستقبلية. راجع [حزمة التوزيع الجديدة](/ar/pgbackrest/news/#distribution-tarball) لمزيد من المعلومات. **ملاحظة لمعدّي الحزم**: توجد تبعية اختيارية جديدة على `libsystemd`. **ملاحظة هامة**: ابتداءً من هذا الإصدار، لا يجوز افتراضيًا تشغيل سوى الأمر `restore` بصلاحيات root. استخدم `allow-root` لتشغيل أوامر أخرى بصلاحيات root (لكن هذا غير موصى به).

**إصلاحات الأخطاء:**

- إصلاح قيام `expire` بحذف نسخة احتياطية قيد التنفيذ على مضيف آخر. (*راجعه Douglas J Hunley. أبلغ عنه Dmitrii.*)
- إصلاح عدم إنفاذ `archive-push-queue-max` عندما يخطئ ملف WAL. (*راجعه Stefan Fercot. أبلغ عنه vut12.*)
- إصلاح فشل `archive-get` غير المتزامن أثناء الاسترداد عبر تبديل الخط الزمني. (*راجعه Douglas J Hunley. أبلغ عنه Jimmy Yih.*)
- إصلاح تجاوز محتمل للمخزن المؤقت في وحدة الأخطاء. (*أصلحه Christophe Pettus. راجعه David Steele.*)
- إصلاح مشكلة استخدام-بعد-التحرير (use-after-free) في عميل البروتوكول المتوازي. (*راجعه Douglas J Hunley. أبلغ عنه Georgy Shelkovy.*)
- إصلاح فيض الكومة عند تعيين خيار pg دون pg1. (*راجعه Douglas J Hunley. أبلغ عنه Naveen.*)

**الميزات:**

- دعم PostgreSQL 19beta2. (*راجعه Stefan Fercot.*)
- إضافة خيار `archive-expire-before` لتنظيف أرشيف WAL. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- إضافة حذف دفعي لتخزين Azure. (*راجعه Douglas J Hunley، Crispy.*)
- إضافة دعم S3 Outposts. (*ساهم به Shiva Kumar Ambigi. راجعه David Steele، Roberto Mello.*)
- إضافة مصادقة العمليات لـ S3. (*راجعه Andrew Charlton. اقترحه Andrew Charlton.*)

**التحسينات:**

- إعادة الاتصال بتخزين SFTP بعد أن يقطع الخادم اتصالًا خاملًا. (*راجعه Stefan Fercot. اقترحه mustafa0x، tisserat.*)
- إضافة تخزين مؤقت للمستخدم/المجموعة لتسريع بناء الـ manifest. (*ساهم به Gunnar Lindholm. راجعه David Steele.*)
- إضافة تقدم النسخ الاحتياطي لكل مستودع إلى مخرجات الأمر `info`. (*ساهم به Will Morland. راجعه David Steele، Stefan Fercot.*)
- إضافة فحوصات `backup.info` إلى الأمر `verify`. (*ساهم به Denis Garsh. راجعه David Steele، Douglas J Hunley.*)
- السماح بإعداد نقطة نهاية STS لـ S3. (*ساهم به Simon Gratton. راجعه David Steele.*)
- إضافة `archive-push-batch-size` لتحديد كمية WAL المدفوعة في كل تشغيل غير متزامن. (*راجعه Stefan Fercot.*)
- الخروج من `archive-push` غير المتزامن عند أول خطأ. (*راجعه Stefan Fercot. اقترحه Lardière Sébastien.*)
- تقوية تحليل استجابات HTTP المجزّأة. (*ساهم به Shubham. راجعه David Steele.*)
- إصدار خطأ عند التشغيل بصلاحيات root ما لم يُمكَّن `allow-root`. (*راجعه Douglas J Hunley.*)
- تقليل عمليات البحث الثنائي عند بناء الـ manifest. (*ساهم به Gunnar Lindholm. راجعه David Steele.*)
- تحسين أداء seek أثناء استعادة دلتا التزايدي بالكتل. (*راجعه David Christensen، Douglas J Hunley.*)
- تجميع ملفات النسخة الاحتياطية بالترتيب بدلًا من المسح بحثًا عن تطابق أفضل. (*راجعه Stefan Fercot.*)
- الإبلاغ عن الخطأ الكامن عندما يفشل استعلام في الاكتمال. (*راجعه Andrew Pogrebnoi. اقترحه Marco Fontana.*)
- الإبلاغ عن الخطأ الفعلي عند فشل طلب بيانات اعتماد S3. (*راجعه Douglas J Hunley. اقترحه Mitchell Grice.*)
- الإبلاغ عن أخطاء مسار spool للأمر `archive-push` في سجل PostgreSQL. (*راجعه Douglas J Hunley. اقترحه Don Seiler.*)
- التلميح إلى أن pgBackRest قد يكون قديمًا عند وجود إصدار غير مدعوم.
- إضافة تكامل إشعارات systemd. (*ساهم به Andrew Jackson. راجعه David Steele.*)
- كتم أخطاء `unused parameter` في فحوصات المُجمِّع في meson. (*ساهم به Jörg Plate. راجعه David Steele.*)
- أصبح C11 الآن الحد الأدنى لمعيار C. (*راجعه Mohammad Ali Nazir Kosar.*)

**تحسينات التوثيق:**

- جعل خيار `stanza` داخليًا لأوامر `repo-*`. (*راجعه Stefan Fercot.*)
- توثيق أن info يقرأ إعدادات التشفير من القسم العام. (*راجعه Stefan Fercot. اقترحه Ron Johnson.*)
- توثيق أن `expire-auto` يستخدم إعداد الأمر `backup`. (*راجعه Stefan Fercot. اقترحه Lardière Sébastien.*)
- توثيق تعديل توجيه `su` في logrotate للمستخدم المخصص. (*راجعه Douglas J Hunley. اقترحه lkanbus.*)
- توثيق أن التعليقات في نهاية السطر غير مدعومة في ملفات الإعداد. (*راجعه Douglas J Hunley. اقترحه Alex Richman.*)

**تحسينات مجموعة الاختبارات:**

- إصلاح تعارضات المجموعات في Alpine داخل حاويات CI. (*ساهم به Artur Zakirov. راجعه David Steele.*)


### ملاحظات إصدار v2.58.0 {#v2580-release-notes}

*تحسينات تخزين الكائنات*

*صدر في 19 يناير 2026*

**ملاحظة هامة**: ارتفعت القيم الدنيا لخيار `repo-storage-upload-chunk-size`. وهي تمثل الآن الحد الأدنى المسموح به من قبل المزوّدين.

**إصلاحات الأخطاء:**

- إصلاح جمود ناتج عن التسجيل داخل معالج الإشارات. (*أصلحه Maxim Michkov. راجعه David Steele.*)

**الميزات:**

- دعم HTTP لـ S3 وGCS وAzure. (*ساهم به Will Morland. راجعه David Steele.*)
- السماح بإنهاء صلاحية أقدم نسخة احتياطية كاملة بغض النظر عن الاحتفاظ الحالي. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Ron Johnson.*)
- دعم الهويات المُدارة في Azure. (*ساهم به Moiz Ibrar، Matthew Mols. راجعه David Steele.*)
- دعم ***تجريبي*** لهوية pod في EKS لـ S3. (*ساهم به Pierre BOUTELOUP. راجعه David Steele.*)
- السماح بإعداد مجموعات تشفير TLS. (*ساهم به Gunnar "Nick" Bluth. راجعه David Steele.*)
- السماح بتعيين أولوية العملية. (*راجعه Douglas J Hunley.*)

**التحسينات:**

- السماح بالنقاط في أسماء حاويات S3 عند استخدام URI بنمط المسار. (*ساهم به Joakim Hindersson. راجعه David Steele.*)
- اشتراط TLS >= 1.2 ما لم يُعطَّل التحقق. (*راجعه Douglas J Hunley، Gunnar "Nick" Bluth.*)
- تحجيم قطع S3/GCS/Azure ديناميكيًا للرفعات الكبيرة. (*راجعه Douglas J Hunley. اقترحه Timothée Peignier.*)
- تحسين حجم قطع S3/GCS/Azure للملفات الصغيرة. (*راجعه Douglas J Hunley.*)
- إزالة دعم PostgreSQL `9.5`. (*راجعه Douglas J Hunley.*)
- تحسين تسجيل القيمة الافتراضية للخيارات ذات التبعية غير المحلولة. (*راجعه Stefan Fercot.*)

**تحسينات التوثيق:**

- إزالة إعداد `max_wal_senders`/`wal_level` الصريح من دليل المستخدم. (*اقترحه Jamie Nguyen.*)
- توضيح أن التجميع مفيد لأنظمة الملفات ذات أحجام الكتل الكبيرة. (*اقترحه Ron Johnson.*)


### ملاحظات إصدار v2.57.0 {#v2570-release-notes}

*منع الروابط الرمزية في المستودع*

*صدر في 18 أكتوبر 2025*

**إصلاحات الأخطاء:**

- إلغاء تداخل مهل HTTP/TLS/المقابس. (*راجعه David Christensen.*)
- إصلاح خطأ تقسيم محتمل في رسالة خطأ مجموع تحقق الصفحات. (*أصلحه Zsolt Parragi. راجعه David Steele.*)

**الميزات:**

- إضافة خيار `repo-symlink` لمنع إنشاء الروابط الرمزية في المستودع. (*راجعه Douglas J Hunley. اقترحه Ron Johnson.*)

**التحسينات:**

- إضافة إعادة محاولة HTTP لأخطاء 408 و429. (*راجعه David Christensen.*)


### ملاحظات إصدار v2.56.0 {#v2560-release-notes}

*تحسينات معلومات التقدم*

*صدر في 21 يوليو 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة في إنهاء الصلاحية عند الطلب عندما لا توجد نسخ احتياطية في مستودع. (*راجعه Stefan Fercot. أبلغ عنه Anup Gupta.*)

**الميزات:**

- إضافة تقدم الاستعادة إلى مخرجات الأمر `info`. (*ساهم به Denis Garsh، Maxim Michkov. راجعه David Steele.*)
- إضافة مستوى تفصيل للتقدم فقط لمخرجات الأمر `info`. (*ساهم به Denis Garsh. راجعه David Steele، Stefan Fercot.*)

**التحسينات:**

- إعادة محاولة القراءات الفاشلة على مخازن الكائنات. (*راجعه David Christensen.*)
- إصلاح القيم الافتراضية في مساعدة سطر الأوامر. (*راجعه David Christensen، Chris Bandy.*)

**تحسينات التوثيق:**

- وصف القيم المنفصلة للخيارات في قائمة حيثما كان ذلك مناسبًا. (*ساهم به Anton Kurochkin. راجعه David Steele.*)
- إصلاح "أقل من" في مخرجات المساعدة لخيار `archive-mode`. (*ساهم به Anton Kurochkin. راجعه David Steele.*)


### ملاحظات إصدار v2.55.1 {#v2551-release-notes}

*إصلاحات أخطاء*

*صدر في 5 مايو 2025*

**إصلاحات الأخطاء:**

- التراجع عن "حساب content-md5 على S3 فقط عند الحاجة". (*راجعه David Christensen. أبلغ عنه Frank Brendel.*)
- إصلاح فحص الحدود الدنيا لمفاتيح الخيارات. (*راجعه David Christensen، Wolfgang Walther. أبلغ عنه Wolfgang Walther.*)


### ملاحظات إصدار v2.55.0 {#v2550-release-notes}

*تحسينات التحقق ودعم PostgreSQL 18*

*صدر في 21 أبريل 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة استعادة التزايدي بالكتل على مستودع غير افتراضي. (*راجعه David Christensen، Aleksander Łukasz. أبلغ عنه Aleksander Łukasz.*)
- عدم تعيين `recovery_target_timeline=current` لـ PostgreSQL < 12. (*راجعه Stefan Fercot.*)
- إصلاح تسجيل نطاق الأرشيف في expire. (*راجعه Stefan Fercot. أبلغ عنه Aleš Zelený.*)
- إصلاح الإبلاغ عن الأخطاء للاستعلامات دون نتائج. (*راجعه Stefan Fercot. أبلغ عنه Susantha Bathige.*)

**الميزات:**

- التحقق من الخط الزمني الهدف للاسترداد. (*راجعه Stefan Fercot.*)
- السماح بالتحقق من نسخة احتياطية محددة. (*ساهم به Maxim Michkov. راجعه David Steele.*)
- إضافة دعم خاصية الدفع من الطالب (requester pays) في S3/GCS. (*ساهم به Timothée Peignier. راجعه David Steele.*)
- دعم PostgreSQL 18. (*راجعه Stefan Fercot.*)
- السماح بالاتصالات بـ PostgreSQL عبر مقابس النطاق المجردة. (*راجعه Chris Bandy. اقترحه Chris Bandy.*)
- إضافة مخرجات رقمية للأمر `version`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

**التحسينات:**

- السماح للأمر `backup` بالعمل على مستودعات بعيدة. (*راجعه Stefan Fercot.*)
- استخدام lz4 لضغط البروتوكول. (*راجعه Stefan Fercot.*)
- حساب `content-md5` على S3 فقط عند الحاجة. (*راجعه David Christensen.*)
- إصدار تحذير عند استبدال قيمة خيار متعدد المفاتيح. (*راجعه David Christensen، Stefan Fercot.*)
- إضافة تسجيل تفصيلي لمسار الأرشيف المنتهي صلاحيته. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- إزالة دعم PostgreSQL `9.4`. (*راجعه Stefan Fercot.*)
- إزالة بناء autoconf/make. (*راجعه David Christensen.*)

**تحسينات التوثيق:**

- إصلاح توثيق تحديد عدة stanza باستخدام `tls-server-auth`. (*راجعه David Christensen، Stefan Fercot. اقترحه Terry MacAndrew.*)
- توضيح انتهاء صلاحية النسخ الاحتياطية التزايدية. (*راجعه Stefan Fercot.*)
- توضيح متطلب تطابق إصدارات pgBackRest المحلية/البعيدة. (*ساهم به Greg Clough. راجعه David Steele.*)
- إضافة أسئلة شائعة حول تصدير عنقود مكتفٍ ذاتيًا. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- إضافة تنبيه حول `--tablespace-map-all` فيما يخص إنشاء مساحات الجداول. (*راجعه Stefan Fercot، Christophe Courtois. اقترحه Christophe Courtois.*)
- توضيح سلوك `--repo-retention-full-type`. (*راجعه Antoine Beaupré. اقترحه Antoine Beaupré.*)
- تغيير توصية `--process-max` لمخازن الكائنات إلى `--repo-bundle`. (*راجعه Stefan Fercot.*)
- تحديث `unix_socket_directory` إلى `unix_socket_directories`. (*ساهم به hyunkyu han. راجعه David Steele.*)
- التوصية بعدم وضع `spool-path` داخل `pg_xlog`/`pg_wal`. (*راجعه Martín Marqués، Don Seiler. اقترحه Martín Marqués.*)


### ملاحظات إصدار v2.54.2 {#v2542-release-notes}

*إصلاح خطأ*

*صدر في 20 يناير 2025*

**إصلاحات الأخطاء:**

- إصلاح مشكلة بعد تعطيل التجميع مع تمكين التزايدي بالكتل. (*راجعه David Christensen.*)

**تحسينات التوثيق:**

- توضيح سلوك ملفات الإعداد المتعددة. (*راجعه Paul Bierly. اقترحه Paul Bierly.*)


### ملاحظات إصدار v2.54.1 {#v2541-release-notes}

*إصلاح خطأ*

*صدر في 16 ديسمبر 2024*

**إصلاحات الأخطاء:**

- إصلاح مشكلة محاولة الأمرين `version`/`help` تحميل `pgbackrest.conf`. (*راجعه Stefan Fercot. أبلغ عنه Bradford Boyle، Julian.*)

**تحسينات مجموعة الاختبارات:**

- تثبيت الأرشفة غير المتزامنة في اختبارات التكامل. (*ساهم به Viktor Kurilko. راجعه David Steele.*)


### ملاحظات إصدار v2.54.0 {#v2540-release-notes}

*الوقت المستهدف للتخزين ذي الإصدارات*

*صدر في 21 أكتوبر 2024*

**ملاحظة لمعدّي الحزم**: هذا آخر إصدار ميزات يدعم بناء autoconf/make. يرجى الانتقال إلى meson إن لم تكن قد فعلت ذلك بالفعل. ستواصل إصدارات الترقيعات 2.54.X (إن وُجدت) دعم autoconf/make.

**إصلاحات الأخطاء:**

- إصلاح أداء استعلامات PostgreSQL لمجموعات البيانات الكبيرة. (*أصلحه Thibault Vincent، David Steele. راجعه David Christensen، Antoine Millet. أبلغ عنه Antoine Millet.*)

**الميزات:**

- السماح بقراءة المستودعات على التخزين ذي الإصدارات عند وقت مستهدف. (*راجعه Stefan Fercot، David Christensen.*)
- السماح للنسخة الاحتياطية المطلوبة من خادم الاستعداد بالمتابعة دون وجود خادم استعداد. (*راجعه Stefan Fercot.*)

**التحسينات:**

- تلخيص قائمة مراجع النسخ الاحتياطية في المخرجات النصية للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- تحديث رمز web-id عند كل مصادقة S3. (*ساهم به Brent Graveland. راجعه David Steele.*)
- عرض القيم الحالية للخيارات المفهرسة بشكل صحيح في المساعدة. (*راجعه David Christensen.*)
- حفظ `backup.info` فقط عند تغيّر محتواه. (*راجعه Stefan Fercot.*)
- إزالة قيد القراءة المتوازية للملفات أثناء الاستعادة. (*راجعه David Christensen.*)
- تحسين رسائل أخطاء SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)

**ميزات التوثيق:**

- إضافة قسم ضبط الأداء إلى دليل المستخدم. (*راجعه Stefan Fercot.*)

**تحسينات التوثيق:**

- توضيح مصدر `data_directory`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Matthias.*)
- منطق أفضل لتحديد متى يجب أن يكون الملخص بأحرف صغيرة. (*اقترحه Daniel Westermann.*)


### ملاحظات إصدار v2.53.1 {#v2531-release-notes}

*دعم PostgreSQL 17*

*صدر في 19 أغسطس 2024*

**إصلاحات الأخطاء:**

- إصلاح الأذونات عند تشغيل `restore` بصلاحيات المستخدم root. (*راجعه Stefan Fercot. أبلغ عنه Will M.*)
- إصلاح خطأ تقسيم عند تأخر أخطاء الاتصال. (*راجعه David Christensen. أبلغ عنه Anton Glushakov.*)
- تخطي فحص التكرار للمستودع المحلي في SFTP. (*أصلحه Reid Thompson. راجعه David Steele. أبلغ عنه Anton Kurochkin.*)

**التحسينات:**

- دعم PostgreSQL 17.


### ملاحظات إصدار v2.53 {#v253-release-notes}

*النسخ الاحتياطي المتزامن*

*صدر في 22 يوليو 2024*

**ملاحظة هامة**: تغيّرت القيمة الافتراضية لخيار `log-level-stderr` من `warn` إلى `off`. يسهّل هذا التقاط الأخطاء عند إعادة توجيه `stdout` فقط. للحفاظ على السلوك السابق عيّن `log-level-stderr=warn`. **ملاحظة لمعدّي الحزم**: أصبحت مكتبة lz4 مطلوبة الآن لبناء meson. **ملاحظة لمعدّي الحزم**: أصبح دعم المُجمِّع للدالتين `__builtin_clzl()` و`__builtin_bswap64()` مطلوبًا الآن لبناء meson.

**إصلاحات الأخطاء:**

- إصلاح فشل إعادة التسمية في SFTP عندما يكون الملف موجودًا بالفعل. (*أصلحه Reid Thompson. راجعه David Steele. أبلغ عنه ahmed112212.*)

**الميزات:**

- السماح بتشغيل النسخ الاحتياطي بشكل متزامن على مستودعات مختلفة. (*راجعه Reid Thompson، Stefan Fercot.*)
- دعم SANs القائمة على IP للتحقق من شهادات TLS. (*ساهم به David Christensen. راجعه David Steele.*)

**التحسينات:**

- جعل القيمة الافتراضية لخيار `log-level-stderr` هي `off`. (*راجعه Greg Sabino Mullane، Stefan Fercot.*)
- السماح بأحجام بديلة لمقاطع WAL لـ PostgreSQL ≤ 10. (*ساهم به Viktor Kurilko. راجعه David Steele.*)
- إضافة تلميح لفحص سجل التفويض في SFTP. (*ساهم به Vitalii Zurian. راجعه Reid Thompson، David Steele.*)

**تحسينات التوثيق:**

- توضيح سلوك `archive-push` مع المستودعات المتعددة. (*راجعه Stefan Fercot.*)


### ملاحظات إصدار v2.52.1 {#v2521-release-notes}

*إصلاح خطأ*

*صدر في 25 يونيو 2024*

**إصلاحات الأخطاء:**

- إصلاح مشكلة الملفات الأكبر على النسخة المتماثلة مقارنة بالأساسي. (*راجعه Stefan Fercot. أبلغ عنه Nicolas Lassimonne.*)


### ملاحظات إصدار v2.52 {#v252-release-notes}

*دعم PostgreSQL 17beta1*

*صدر في 27 مايو 2024*

**ملاحظة لمعدّي الحزم**: أصبح نظام بناء pgBackRest الآن meson. لن يحصل بناء autoconf/make على أي ميزات جديدة وسيُزال بعد بضعة إصدارات.

**الميزات:**

- إضافة دعم الحذف الدفعي في GCS. (*راجعه Reid Thompson.*)
- دعم التشفير `SSE-C` في S3. (*راجعه Tim Jones. اقترحه Tim Jones.*)
- دعم PostgreSQL 17beta1. (*راجعه Stefan Fercot.*)

**التحسينات:**

- السماح بتعطيل التبعيات الاختيارية بشكل صريح في بناء meson. (*ساهم به Michael Schout. راجعه David Steele.*)
- إيجاد python ديناميكيًا في بناء meson. (*ساهم به Michael Schout. راجعه David Steele.*)
- وسم هدف بناء `pgbackrest` في meson بأنه قابل للتثبيت. (*ساهم به Bradford Boyle. راجعه David Steele.*)

**تحسينات التوثيق:**

- تحديث توثيق `start`/`stop` ليعكس الوظائف الفعلية. (*راجعه Stefan Fercot.*)


### ملاحظات إصدار v2.51 {#v251-release-notes}

*نظام البناء meson*

*صدر في 25 مارس 2024*

**إصلاحات الأخطاء:**

- تخطي الملفات ذات الطول الصفري لاستعادة دلتا التزايدي بالكتل. (*راجعه Sebastian Krause، René Højbjerg Larsen. أبلغ عنه Sebastian Krause.*)
- إصلاح تراجع الأداء في قائمة التخزين. (*راجعه Stephen Frost. أبلغ عنه Maksym Boguk.*)
- إصلاح تسجيل التقدم عندما يتغير حجم الملف أثناء النسخ الاحتياطي. (*راجعه Stephen Frost. أبلغ عنه samkingno.*)

**التحسينات:**

- تحسين الدعم للاتصالات ثنائية المكدس. (*راجعه Stephen Frost. اقترحه Timothée Peignier.*)
- جعل meson نظام البناء الأساسي. (*راجعه Stephen Frost.*)
- اكتشاف الملفات التي لم تتغير أثناء النسخ الاحتياطي التزايدي غير القائم على الدلتا. (*راجعه Stephen Frost.*)
- منع استرداد غير صالح عند إزالة `backup_label`. (*راجعه Stephen Frost.*)
- تحسين التعامل مع قائمة انتظار مقاطع WAL في `archive-push`. (*راجعه Stephen Frost.*)
- قصر وظيفة الاستئناف على النسخ الاحتياطية الكاملة. (*راجعه Stephen Frost، Stefan Fercot.*)
- تحديث وظيفة الاستئناف للتزايدي بالكتل. (*راجعه Stephen Frost.*)
- السماح باستخدام `--version` و`--help` لعرض الإصدار والمساعدة. (*راجعه Greg Sabino Mullane. اقترحه Greg Sabino Mullane.*)
- إضافة تتبع خلفي مفصّل إلى بناء autoconf/make. (*راجعه Stephen Frost.*)

**تحسينات التوثيق:**

- تحديث الإشارات إلى `recovery.conf`. (*راجعه Stefan Fercot. اقترحه Stephen Frost.*)


### ملاحظات إصدار v2.50 {#v250-release-notes}

*تحسينات الأداء وإصلاحات أخطاء*

*صدر في 22 يناير 2024*

**إصلاحات الأخطاء:**

- إصلاح القراءة الناقصة في استعادة التزايدي بالكتل. (*راجعه Stephen Frost، Brent Graveland. أبلغ عنه Adol Rodriguez، Brent Graveland.*)
- إصلاح فيض يخفي تقدم النسخ الاحتياطي في مخرجات `info`. (*أصلحه Robert Donovan. راجعه Joe Wildish.*)

**التحسينات:**

- الحفاظ على الملفات الجزئية أثناء استعادة دلتا التزايدي بالكتل. (*راجعه Stephen Frost.*)
- إضافة دعم أحجام صفحات بديلة وقت التجميع. (*ساهم به Viktor Kurilko. راجعه David Steele.*)
- تخطي الملفات المقتطعة أثناء النسخ الاحتياطي عند التجميع. (*ساهم به Georgy Shelkovy. راجعه David Steele.*)
- تحسين رسائل أخطاء تخزين SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)


### ملاحظات إصدار v2.49 {#v249-release-notes}

*إزالة دعم PostgreSQL 9.3*

*صدر في 27 نوفمبر 2023*

**إصلاحات الأخطاء:**

- إصلاح تراجع في عمليات إعادة المحاولة. (*راجعه Stephen Frost. أبلغ عنه Norman Adkins، Tanel Suurhans، Jordan English، Timothée Peignier.*)
- إصلاح الحذف العودي للمسارات في مشغّل تخزين SFTP. (*أصلحه Reid Thompson. راجعه Stephen Frost. أبلغ عنه Luc.*)

**التحسينات:**

- إزالة دعم PostgreSQL `9.3`. (*راجعه Stephen Frost.*)

**ميزات التوثيق:**

- توثيق خيارات المشرفين. (*راجعه Stefan Fercot.*)
- تحديث توثيق الاسترداد إلى نقطة زمنية لـ PostgreSQL >= 13.

**تحسينات مجموعة الاختبارات:**

- السماح بتشغيل اختبار الوحدة `config/load` دون تثبيت `libssh2`. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Wu Ning.*)


### ملاحظات إصدار v2.48 {#v248-release-notes}

*وسوم تخزين المستودع*

*صدر في 25 سبتمبر 2023*

**إصلاحات الأخطاء:**

- إصلاح مشكلة استعادة التزايدي بالكتل دون قائمة كتل. (*راجعه Stephen Frost، Burak Yurdakul. أبلغ عنه Burak Yurdakul.*)

**الميزات:**

- إضافة خيار `--repo-storage-tag` لإنشاء وسوم الكائنات. (*راجعه Stephen Frost، Stefan Fercot، Timothée Peignier.*)
- إضافة فحص المضيفين المعروفين لمشغّل تخزين SFTP. (*ساهم به Reid Thompson. راجعه Stephen Frost، David Steele.*)
- دعم الاتصالات ثنائية المكدس. (*راجعه Stephen Frost.*)
- إضافة حجم النسخة الاحتياطية المكتمل/الإجمالي إلى مخرجات JSON للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

**التحسينات:**

- الأمر `check` متعدد الـ stanza. (*راجعه Stephen Frost.*)
- إعادة محاولة قراءات `pg_control` حتى يصبح المجموع الاختباري صالحًا. (*راجعه Stefan Fercot، Stephen Frost.*)
- تحسين فحص مقاطع WAL بعد نسخة احتياطية ناجحة. (*راجعه Stephen Frost.*)
- تحسين أداء الأجزاء المتعددة في GCS. (*راجعه Reid Thompson.*)
- السماح بتشغيل الأمر `archive-get` عندما تكون الـ stanza متوقفة. (*راجعه Tom Swartz، David Christensen، Reid Thompson.*)
- قبول التلدة (~) البادئة في مسارات المفاتيح العامة/الخاصة لـ SFTP. (*ساهم به Reid Thompson. راجعه David Steele.*)
- إعادة تحميل بيانات اعتماد GCS قبل تجديد رمز المصادقة. (*راجعه Stephen Frost. اقترحه Daniel Farina.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح مثال مرجع الإعداد لخيار `tls-server-address`. (*أصلحه Hartmut Goebel. راجعه David Steele.*)
- إصلاح مثال مرجع الأوامر لخيار `filter`.

**تحسينات مجموعة الاختبارات:**

- السماح بتشغيل اختبار الوحدة `storage/sftp` دون تثبيت `libssh2`. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Wu Ning.*)


### ملاحظات إصدار v2.47 {#v247-release-notes}

*تحسينات الأداء وإصلاحات أخطاء*

*صدر في 24 يوليو 2023*

**إصلاحات الأخطاء:**

- الحفاظ على معلومات التزايدي بالكتل في الـ manifest أثناء النسخ الاحتياطي بالدلتا. (*راجعه Stephen Frost. أبلغ عنه Francisco Miguel Biete Banon.*)
- إصلاح أسماء ملفات التزايدي بالكتل في الأمر `verify`. (*راجعه Reid Thompson. أبلغ عنه Francisco Miguel Biete Banon.*)
- إصلاح النسخ الاحتياطي الدلتي التلقائي الزائف عند النسخ من خادم الاستعداد. (*راجعه Stephen Frost. أبلغ عنه krmozejko، Don Seiler.*)
- تخطي `recovery.signal` لـ PostgreSQL >= 12 عندما يكون `type=none` للاسترداد. (*راجعه Stefan Fercot. أبلغ عنه T.Anastacio.*)
- إصلاح توليد الاسم الفريد للنسخ الاحتياطي diff/incr. (*أصلحه Andrey Sokolov. راجعه David Steele.*)
- إصلاح انتهاء صلاحية الأرشيف الزمني عندما لا تنتهي صلاحية أي نسخة احتياطية. (*راجعه Stefan Fercot.*)

**التحسينات:**

- تحسين أداء مشغّل تخزين SFTP. (*ساهم به Stephen Frost، Reid Thompson. راجعه David Steele.*)
- إضافة إزاحة المنطقة الزمنية إلى مخرجات التاريخ/الوقت للأمر `info`. (*راجعه Stefan Fercot، Philip Hurst. اقترحه Philip Hurst.*)
- مركزنة معالجة الأخطاء للميزات غير المدعومة. (*راجعه Stefan Fercot.*)

**تحسينات التوثيق:**

- توضيح تفضيل التثبيت من الحزم في دليل المستخدم. (*راجعه Stefan Fercot. اقترحه dr-kd.*)


### ملاحظات إصدار v2.46 {#v246-release-notes}

*النسخ الاحتياطي التزايدي بالكتل وتخزين SFTP*

*صدر في 22 مايو 2023*

**الميزات:**

- النسخ الاحتياطي التزايدي بالكتل. (*راجعه John Morris، Stephen Frost، Stefan Fercot.*)
- دعم SFTP لتخزين المستودع. (*ساهم به Reid Thompson. راجعه Stephen Frost، David Steele.*)
- دعم PostgreSQL 16. (*راجعه Stefan Fercot.*)

**التحسينات:**

- السماح بتخطي فحوصات ترويسة الصفحة. (*راجعه David Christensen. اقترحه David Christensen.*)
- تجنّب `chown()` على ملفات الاسترداد أثناء الاستعادة. (*راجعه Stefan Fercot، Marcelo Henrique Neppel. اقترحه Marcelo Henrique Neppel.*)
- إضافة تفاصيل إعادة المحاولة للأخطاء في إعادة محاولات HTTP.

**تحسينات التوثيق:**

- إضافة تحذير حول استخدام `type=none` للاسترداد. (*راجعه Stefan Fercot.*)
- إضافة ملاحظة حول تشغيل `stanza-create` على مستودعات أُنشئت بالفعل.


### ملاحظات إصدار v2.45 {#v245-release-notes}

*النسخ الاحتياطي التزايدي بالكتل (BETA)*

*صدر في 20 مارس 2023*

**إصلاحات الأخطاء:**

- تخطي كتابة `recovery.signal` افتراضيًا لاستعادة النسخ الاحتياطية المأخوذة أثناء توقف PostgreSQL. (*راجعه Stefan Fercot. أبلغ عنه Marcel Borger.*)

**الميزات:**

- النسخ الاحتياطي التزايدي بالكتل (BETA). (*راجعه John Morris، Stephen Frost، Stefan Fercot.*)

**التحسينات:**

- الإبقاء على فهرس مجموعة واحد فقط تكون جميع قيمه افتراضية. (*راجعه Stefan Fercot.*)

**تحسينات التوثيق:**

- إضافة تعليمات صريحة للترقية بين إصدارات `2.x`. (*ساهم به Christophe Courtois. راجعه David Steele.*)
- إزالة الإشارات إلى SSH التي أصبحت متقادمة عند إدخال TLS.


### ملاحظات إصدار v2.44 {#v244-release-notes}

*إزالة دعم PostgreSQL 9.0/9.1/9.2*

*صدر في 30 يناير 2023*

**التحسينات:**

- إزالة دعم PostgreSQL `9.0`/`9.1`/`9.2`. (*راجعه Stefan Fercot.*)
- إصدار خطأ أثناء الاستعادة عندما لا تطابق أي نسخة احتياطية إصدار PostgreSQL الحالي. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Soulou.*)
- إضافة فحص نطاق `compress-level` لكل `compress-type`. (*راجعه Stefan Fercot. اقترحه gkleen، ViperRu.*)

**تحسينات التوثيق:**

- إضافة تحذير حول تمكين "مساحة الأسماء الهرمية" في تخزين Azure. (*راجعه Stefan Fercot. اقترحه Vojtech Galda، Pluggi، asjonos.*)
- إضافة استبدال الأسطر الجديدة في مثال المراقبة. (*راجعه Stefan Fercot. اقترحه rudonx، gmustdie، Ivan Shelestov.*)
- توضيح سلوك `target-action` على إصدارات PostgreSQL المختلفة. (*ساهم به Chris Bandy. راجعه David Steele، Anton Kurochkin، Stefan Fercot. اقترحه Anton Kurochkin، Chris Bandy.*)
- تحديثات وتوضيحات لصفحة الفهرس. (*راجعه Stefan Fercot.*)
- إضافة الوضع الداكن إلى الموقع الإلكتروني. (*اقترحه Stephen Frost.*)


### ملاحظات إصدار v2.43 {#v243-release-notes}

*إصلاح خطأ*

*صدر في 28 نوفمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح مرجع مفقود في النسخ الاحتياطي diff/incr. (*راجعه Stefan Fercot. أبلغ عنه Marcel Borger، ulfedf، jaymefSO.*)

**التحسينات:**

- إضافة تلميح عند تحديد خيار دون فهرس. (*راجعه Stefan Fercot.*)


### ملاحظات إصدار v2.42 {#v242-release-notes}

*إصلاحات أخطاء*

*صدر في 22 نوفمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح تسريب للذاكرة في تجميع الملفات للأمرين `backup`/`restore`. (*راجعه John Morris، Oscar. أبلغ عنه Oscar.*)
- إصلاح خطأ في البروتوكول عند قراءة ناقصة لملف بعيد. (*راجعه Stephen Frost.*)

**التحسينات:**

- عدم تخزين المراجع للملفات ذات الطول الصفري عند التجميع. (*راجعه Stefan Fercot.*)
- استخدام أوصاف أكثر عمومية للدالتين `pg_start_backup()`/`pg_stop_backup()`. (*راجعه Greg Sabino Mullane، David Christensen. اقترحه Greg Sabino Mullane.*)

**تحسينات مجموعة الاختبارات:**

- تحديث خيار `--psql-bin` في `test.pl` ليطابق مساعدة سطر الأوامر. (*ساهم به Koshi Shibagaki. راجعه David Steele.*)


### ملاحظات إصدار v2.41 {#v241-release-notes}

*التعليقات التوضيحية للنسخ الاحتياطية*

*صدر في 19 سبتمبر 2022*

**إصلاحات الأخطاء:**

- إصلاح استخدام انتهاء صلاحية زمني غير صحيح للمستودعات غير الافتراضية. (*راجعه Stefan Fercot. أبلغ عنه Adam Brusselback.*)
- إصلاح مشكلة عند إدراج الأدلة بشكل عودي مع مرشّح. (*راجعه Stephen Frost. أبلغ عنه Efremov Egor.*)

**الميزات:**

- تعليقات توضيحية مفتاح/قيمة للنسخ الاحتياطية. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Adam Berlin.*)

**التحسينات:**

- دعم `--set` في مخرجات JSON للأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Anton Kurochkin.*)
- السماح بإعداد حجم قطعة الرفع لمخازن الكائنات. (*راجعه Stefan Fercot. اقترحه Anton Glushakov.*)
- تحديث الطوابع الزمنية لملف archive.info بعد نسخة احتياطية ناجحة. (*راجعه Stefan Fercot. اقترحه Alex Richman.*)
- نقل فحص الخط الزمني لخادم الاستعداد إلى ما بعد نقطة التحقق. (*راجعه Stefan Fercot، Keith Fiske. اقترحه Keith Fiske.*)
- تحسين رسالة التحذير عند استئناف النسخ الاحتياطي. (*اقترحه Cynthia Shang.*)

**تحسينات التوثيق:**

- إضافة المسار المطلق للأمر `kill` في `pgbackrest.service`. (*اقترحه Don Seiler.*)


### ملاحظات إصدار v2.40 {#v240-release-notes}

*دعم OpenSSL 3*

*صدر في 18 يوليو 2022*

**ملاحظة لمعدّي الحزم**: أُضيف بناء تجريبي بـ meson لكن على معدّي الحزم الاستمرار في استخدام بناء autoconf/make للمستقبل المنظور.

**التحسينات:**

- دعم OpenSSL 3. (*راجعه Stephen Frost.*)
- إنشاء لقطة عند إدراج محتويات مسار. (*راجعه John Morris، Stephen Frost.*)
- فرض `target-timeline=current` عندما يكون `type=immediate` للاستعادة. (*راجعه Stephen Frost.*)
- اقتطاع الملفات أثناء `restore` بالدلتا عندما تكون أكبر من المتوقع. (*راجعه Stephen Frost.*)
- تعطيل الحفظ التزايدي للـ manifest عندما يكون `resume=n`. (*ساهم به Reid Thompson. راجعه David Steele.*)
- تعيين نسبة اكتمال النسخة الاحتياطية إلى الصفر قبل بدء النسخ. (*ساهم به Reid Thompson. راجعه David Steele.*)
- استخدام علامة `IsTruncated` في S3 لتحديد استمرار الإدراج. (*راجعه John Morris، Soulou. اقترحه Christian Montagne.*)

**إصلاحات أخطاء التوثيق:**

- تخطي الخيارات الداخلية في مرجع الإعداد. (*أبلغ عنه Francisco Miguel Biete Banon.*)

**تحسينات التوثيق:**

- إضافة رابط إلى إعداد PostgreSQL في قسم مضيف المستودع. (*راجعه Stefan Fercot. اقترحه Julien Cigar.*)

**تحسينات مجموعة الاختبارات:**

- إضافة بناء Meson تجريبي. (*راجعه Eli Schwartz، Sam Bassaly.*)
- السماح بتمرير أي مسار إلى خيار `--test-path`. (*ساهم به Andrey Sokolov. راجعه David Steele.*)
- إصلاح خطأ التجميع عند تعريف `DEBUG_EXEC_TIME` دون `DEBUG`. (*ساهم به Andrey Sokolov. راجعه David Steele.*)


### ملاحظات إصدار v2.39 {#v239-release-notes}

*التحقق وتجميع الملفات*

*صدر في 16 مايو 2022*

**إصلاحات الأخطاء:**

- إصلاح خطأ مُطلق من `FINALLY()` يسبب حلقة لا نهائية. (*راجعه Stephen Frost.*)
- إصدار خطأ عند جميع إخفاقات القفل عدا احتجاز عملية أخرى للقفل. (*راجعه Reid Thompson، Geir Råness. أبلغ عنه Geir Råness.*)

**الميزات:**

- تجميع ملفات النسخ الاحتياطي لتحسين دعم الملفات الصغيرة. (*راجعه Reid Thompson، Stefan Fercot، Chris Bandy.*)
- أمر verify للتحقق من صحة محتويات مستودع. (*ساهم به Cynthia Shang، Reid Thompson. راجعه David Steele، Stefan Fercot.*)
- دعم PostgreSQL 15. (*راجعه Stefan Fercot.*)
- إظهار نسبة اكتمال النسخة الاحتياطية في مخرجات `info`. (*ساهم به Reid Thompson. راجعه David Steele.*)
- الاختيار التلقائي للنسخة الاحتياطية للأمر `restore` مع `--type=lsn`. (*ساهم به Reid Thompson. راجعه Stefan Fercot، David Steele.*)
- كتم تحذير WAL الموجود مسبقًا عندما يكون `archive-mode-check` معطلًا. (*ساهم به Reid Thompson. راجعه David Steele.*)
- إضافة دعم AWS IMDSv2. (*ساهم به Nuno Pires. راجعه David Steele.*)

**التحسينات:**

- السماح بتغيير خيار `repo-hardlink` بعد نسخة احتياطية كاملة. (*راجعه Reid Thompson.*)
- زيادة دقة تسجيل نسبة الاكتمال للأمرين `backup` و`restore`. (*ساهم به Reid Thompson. راجعه David Steele.*)
- تحسين التحقق من المسارات لأوامر `repo-*`. (*ساهم به Reid Thompson. راجعه David Steele.*)
- تحسين الأمر `stop` ليأخذ خيار `stanza` في الحسبان. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه ragaoua.*)
- تحسين رسالة الخطأ لمفتاح `repo-azure-key` غير الصالح. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Seth Daniel.*)
- إضافة تلميح لفحص السجل عند خطأ غير متزامن في `archive-get`/`archive-push`. (*راجعه Reid Thompson.*)
- إضافة `ClockError` لانحراف الساعة غير المتوقع وتغييرات المنطقة الزمنية. (*راجعه Greg Sabino Mullane، Stefan Fercot. اقترحه Greg Sabino Mullane.*)
- تجريد الامتدادات من الـ manifest التاريخي قبل عرضه في رسالة الخطأ. (*راجعه Stefan Fercot.*)
- إضافة user:group إلى خطأ أذونات القفل. (*راجعه Reid Thompson.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح إشارة غير صحيحة إلى `stanza-update` في دليل المستخدم. (*أصلحه Abubakar Mohammed. راجعه David Steele.*)
- إصلاح مثال خيار `repo-gcs-key-type` في مرجع الإعداد. (*راجعه Reid Thompson.*)
- إصلاح مثال `tls-server-auth` وإضافة توضيحات. (*راجعه Reid Thompson.*)

**تحسينات التوثيق:**

- تبسيط الرسائل حول الإصدارات المدعومة في التوثيق. (*راجعه Stefan Fercot، Reid Thompson، Greg Sabino Mullane.*)
- إضافة أوصاف أنواع الخيارات. (*ساهم به Reid Thompson. راجعه David Steele.*)
- إضافة أسئلة شائعة حول أنواع النسخ الاحتياطي وسرعة الاستعادة. (*ساهم به David Christensen. راجعه Reid Thompson.*)
- توثيق الفرع الأساسي المطلوب لطلبات الدمج. (*ساهم به David Christensen. راجعه Reid Thompson.*)


### ملاحظات إصدار v2.38 {#v238-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 6 مارس 2022*

**ملاحظة هامة**: حجم المستودع الذي يبلّغ عنه الأمر `info` يعتمد الآن بالكامل على ما كتبه pgBackRest في التخزين. سابقًا، في حالات معينة، كان بإمكان pgBackRest اكتشاف ما إذا كان التخزين يطبّق ضغطًا إضافيًا لكن هذا لم يعد مدعومًا.

**إصلاحات الأخطاء:**

- إعادة محاولة الأخطاء في الحذف الدفعي للملفات في S3. (*راجعه Reid Thompson. أبلغ عنه Alex Richman.*)
- السماح بمطابقة غير حساسة لحالة الأحرف لقيم ترويسة `connection` في HTTP. (*راجعه Reid Thompson. أبلغ عنه Rémi Vidier.*)

**الميزات:**

- إضافة دعم التشفير من جانب الخادم في AWS S3 باستخدام KMS. (*ساهم به Christoph Berg. راجعه David Steele، Tharindu Amila.*)
- إضافة خيار `archive-missing-retry`. (*راجعه Stefan Fercot.*)
- إضافة مرشّح نوع النسخة الاحتياطية إلى الأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)

**التحسينات:**

- إعادة المحاولة عند فشل التحقق من الصفحات أثناء `backup`. (*راجعه Stephen Frost، David Christensen.*)
- التعامل مع خوادم TLS التي لا تغلق الاتصالات بسلاسة. (*راجعه Rémi Vidier، David Christensen، Stephen Frost.*)
- إضافة قيم LSN للنسخ الاحتياطية إلى مخرجات الأمر `info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- تجريد الشرطات المائلة الختامية تلقائيًا لمسارات `repo-ls`. (*ساهم به David Christensen. راجعه David Steele.*)
- عدم إعادة محاولة الأخطاء القاتلة. (*راجعه Reid Thompson.*)
- إزالة دعم PostgreSQL `8.3`/`8.4`. (*راجعه Reid Thompson، Stefan Fercot.*)
- إزالة المنطق الذي كان يحاول تحديد الضغط الإضافي لنظام الملفات. (*راجعه Reid Thompson، Stefan Fercot.*)

**إصلاحات أخطاء التوثيق:**

- نقل خيارات `repo` في توثيق TLS إلى القسم `global`. (*أبلغ عنه Anton Kurochkin.*)
- إزالة خيار `backup-standby` غير المستخدم من أوامر الـ stanza. (*أبلغ عنه Stefan Fercot.*)
- إصلاح أخطاء إملائية في المساعدة وملاحظات الإصدار. (*أصلحه Daniel Gustafsson. راجعه David Steele.*)

**تحسينات التوثيق:**

- إضافة فحص الحياة إلى إعداد خدمة systemd. (*اقترحه Yogesh Sharma.*)
- إضافة أسئلة شائعة تشرح لاحقة أرشيف WAL. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- الإشارة إلى أن خانات النسخ المتماثل لا تُستعاد. (*ساهم به Reid Thompson. راجعه David Steele، Stefan Fercot. اقترحه Christophe Courtois.*)


### ملاحظات إصدار v2.37 {#v237-release-notes}

*خادم TLS*

*صدر في 3 يناير 2022*

**ملاحظة هامة**: إذا لم يتمكن الأمر `restore` من إيجاد نسخة احتياطية تطابق الهدف الزمني المحدد فسيُطلق خطأ، بينما كان يُسجَّل تحذير سابقًا.

**إصلاحات الأخطاء:**

- إصلاح تعيين روابط دلتا `restore` عندما يكون المسار/الملف موجودًا بالفعل. (*راجعه Reid Thompson. أبلغ عنه Younes Alhroub.*)
- إصلاح تسريب المقابس عند إعادة محاولة الاتصال. (*راجعه Reid Thompson. أبلغ عنه James Coleman.*)

**الميزات:**

- إضافة خادم TLS. (*راجعه Stephen Frost، Reid Thompson، Andrew L'Ecuyer.*)
- إضافة خيار `--cmd`. (*ساهم به Reid Thompson. راجعه Stefan Fercot، David Steele. اقترحه Virgile CREVON.*)

**التحسينات:**

- فحص الأرشيف فور بدء النسخ الاحتياطي. (*راجعه Reid Thompson، David Christensen.*)
- إضافة فحوصات الخط الزمني ونقطة التحقق إلى النسخ الاحتياطي. (*راجعه Stefan Fercot، Reid Thompson.*)
- التحقق من أن العناقيد حية ومُعدّة بشكل صحيح أثناء النسخ الاحتياطي. (*راجعه Stefan Fercot.*)
- إصدار خطأ عندما يعجز `restore` عن إيجاد نسخة احتياطية تطابق الهدف الزمني. (*راجعه Reid Thompson، Douglas J Hunley. اقترحه Douglas J Hunley.*)
- تحليل البروتوكول/المنفذ في نقاط نهاية S3/Azure. (*ساهم به Reid Thompson. راجعه David Steele.*)
- إضافة تحذير عندما يتجاوز `checkpoint_timeout` قيمة `db-timeout`. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- إضافة الفعل إلى مخرجات أخطاء HTTP. (*ساهم به Christoph Berg. راجعه David Steele.*)
- السماح بوسائط y/n لخيارات سطر الأوامر المنطقية. (*ساهم به Reid Thompson. راجعه David Steele.*)
- جعل تسجيل حجم النسخة الاحتياطية يطابق مخرجات الأمر `info` تمامًا. (*ساهم به Reid Thompson. راجعه David Steele. اقترحه Mahomed Hussein.*)

**تحسينات التوثيق:**

- عرض القيمة الافتراضية لخيارات الحجم والقيم المسموح بها بالوحدات المناسبة. (*راجعه Reid Thompson.*)
- إصلاح أخطاء إملائية وتحسين توثيق خيار `tablespace-map-all`. (*راجعه Reid Thompson. اقترحه Reid Thompson.*)
- إزالة عبارة متقادمة حول الدعم المستقبلي للمستودعات المتعددة. (*اقترحه David Christensen.*)


### ملاحظات إصدار v2.36 {#v236-release-notes}

*إصلاحات أخطاء ثانوية وتحسينات*

*صدر في 1 نوفمبر 2021*

**إصلاحات الأخطاء:**

- السماح بـ "global" كبادئة لـ stanza. (*راجعه Stefan Fercot. أبلغ عنه Younes Alhroub.*)
- إصلاح خطأ تقسيم عند وجود ملف مفتاح GCS غير صالح. (*راجعه Stephen Frost. أبلغ عنه Henrik Feldt.*)

**التحسينات:**

- السماح لخيار `link-map` بإنشاء روابط جديدة. (*راجعه Don Seiler، Stefan Fercot، Chris Bandy. اقترحه Don Seiler.*)
- زيادة الحد الأقصى للفهرس المسموح به لخياري `pg`/`repo` إلى 256. (*راجعه Cynthia Shang.*)
- إضافة مصادقة `WebIdentity` لـ AWS S3. (*راجعه James Callahan، Reid Thompson، Benjamin Blattberg، Andrew L'Ecuyer.*)
- الإبلاغ عن أخطاء التحقق من ملفات النسخة الاحتياطية في `backup.info`. (*ساهم به Stefan Fercot. راجعه David Steele.*)
- إضافة وقت بدء الاسترداد إلى سجل استعادة النسخ الاحتياطية المأخوذة أثناء تشغيل PostgreSQL. (*راجعه Tom Swartz، Stefan Fercot. اقترحه Tom Swartz.*)
- الإبلاغ عن الخطأ الأصلي وإعادات المحاولة عند فشل المهمة المحلية. (*راجعه Stefan Fercot.*)
- إعادة تسمية خطأ مجموع تحقق الصفحات إلى قائمة أخطاء في المخرجات النصية لـ info. (*راجعه Stefan Fercot.*)
- إضافة تلميحات إلى رسالة مهلة إعادة تطبيق WAL على خادم الاستعداد. (*راجعه Cynthia Shang، Stefan Fercot. اقترحه Leigh Downs.*)


### ملاحظات إصدار v2.35 {#v235-release-notes}

*البروتوكول الثنائي*

*صدر في 23 أغسطس 2021*

**ملاحظة هامة**: تغيّر مستوى السجل للملفات المنسوخة في الأمرين `backup`/`restore` إلى `detail`. يجعل ذلك مستوى السجل `info` أقل ضجيجًا، لكن إذا كانت هذه الرسائل مطلوبة فعيّن مستوى السجل للأمرين `backup`/`restore` إلى `detail`

**إصلاحات الأخطاء:**

- اكتشاف الأخطاء في إنهاء الرفع متعدد الأجزاء في S3. (*راجعه Cynthia Shang، Marco Montagna. أبلغ عنه Marco Montagna، Lev Kokotov، Anderson A. Mallmann.*)
- إصلاح اكتشاف الروابط الرمزية الدائرية. (*راجعه Stefan Fercot. أبلغ عنه Rohit Raveendran.*)
- تمرير خيارات `repo` المحددة فقط إلى الطرف البعيد. (*راجعه David Christensen، Cynthia Shang. أبلغ عنه Greg Sabino Mullane، David Christensen.*)

**التحسينات:**

- البروتوكول الثنائي. (*راجعه Cynthia Shang.*)
- إنشاء دليل البيانات تلقائيًا عند `restore`. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Chris Bandy.*)
- السماح بـ `restore` مع `--type=lsn`. (*ساهم به Stefan Fercot. راجعه Cynthia Shang. اقترحه James Coleman.*)
- تغيير مستوى تسجيل الملفات المنسوخة للأمرين `backup`/`restore` إلى detail. (*راجعه Stefan Fercot. اقترحه Jens Wilke.*)
- التكرار حلقيًا أثناء انتظار وصول LSN نقطة التحقق إلى LSN إعادة تطبيق WAL. (*ساهم به Stefan Fercot. راجعه David Steele. اقترحه Fatih Mencutekin.*)
- تسجيل إجمالي ملفات `backup` وإجمالي الحجم/الملفات لـ `restore`. (*راجعه Cynthia Shang.*)

**إصلاحات أخطاء التوثيق:**

- إصلاح أسماء مضيفات غير صحيحة في دليل المستخدم. (*راجعه Stefan Fercot. أبلغ عنه Greg Sabino Mullane.*)

**تحسينات التوثيق:**

- تحديث توثيق المساهمة وإضافة قالب لطلبات الدمج. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إعادة ترتيب توثيق النسخ الاحتياطي في دليل المستخدم. (*راجعه Cynthia Shang.*)
- توضيح سلوك `--type` للأمر `restore` في مرجع الأوامر. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إصلاح أخطاء إملائية في التوثيق والتعليقات. (*ساهم به Eric Radman. راجعه David Steele.*)

**تحسينات مجموعة الاختبارات:**

- إضافة فحص لمسار الاختبار داخل مسار المستودع. (*راجعه Greg Sabino Mullane. اقترحه Greg Sabino Mullane.*)
- إضافة تحليل شيفرة ثابت بـ CodeQL. (*راجعه Cynthia Shang.*)
- تحديث الاختبارات لاستخدام الأنماط القياسية. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v2.34 {#v234-release-notes}

*دعم PostgreSQL 14*

*صدر في 7 يونيو 2021*

**إصلاحات الأخطاء:**

- إصلاح مشكلات ملفات spool المتبقية من `restore` سابق. (*راجعه Cynthia Shang، Stefan Fercot، Floris van Nee. أبلغ عنه Floris van Nee.*)
- إصلاح مشكلة عند فحص روابط أعداد كبيرة من مساحات الجداول. (*راجعه Cynthia Shang، Avinash Vallarapu. أبلغ عنه Avinash Vallarapu.*)
- تحرير الأطراف البعيدة التي لم تعد ضرورية حتى لا تنتهي مهلتها أثناء `restore`. (*راجعه Cynthia Shang. أبلغ عنه Francisco Miguel Biete Banon.*)
- إصلاح `help` عندما يكون خيار صالح غير صالح للأمر المحدد. (*راجعه Stefan Fercot. أبلغ عنه Cynthia Shang.*)

**الميزات:**

- إضافة دعم PostgreSQL 14. (*راجعه Cynthia Shang.*)
- إضافة مصادقة GCS تلقائية لمثيلات GCE. (*راجعه Jan Wieck، Daniel Farina.*)
- إضافة خيار `repo-retention-history` لإنهاء صلاحية السجل التاريخي للنسخ الاحتياطية. (*ساهم به Stefan Fercot. راجعه Cynthia Shang، David Steele.*)
- إضافة خيار `db-exclude`. (*ساهم به Stefan Fercot. راجعه Cynthia Shang.*)

**التحسينات:**

- تغيير تسجيل انتهاء صلاحية الأرشيف من مستوى detail إلى info. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إزالة مسار spool أرشيف الـ stanza عند `restore`. (*راجعه Cynthia Shang، Stefan Fercot.*)
- عدم كتابة الملفات ذريًا أو مزامنة المسارات أثناء نسخ `backup`. (*راجعه Stephen Frost، Stefan Fercot، Cynthia Shang.*)

**تحسينات التوثيق:**

- تحديث توثيق المساهمة. (*ساهم به Cynthia Shang. راجعه David Steele، Stefan Fercot.*)
- دمج دليل مستخدم RHEL/CentOS في مستند واحد. (*راجعه Cynthia Shang.*)
- توضيح أن `repo-s3-role` ليس `ARN`. (*ساهم به Isaac Yuen. راجعه David Steele.*)


### ملاحظات إصدار v2.33 {#v233-release-notes}

*دعم المستودعات المتعددة وGCS*

*صدر في 5 أبريل 2021*

**إصلاحات الأخطاء:**

- إصلاح تحذيرات الخيارات التي تكسر `archive-get`/`archive-push` غير المتزامنين. (*راجعه Cynthia Shang. أبلغ عنه Lev Kokotov.*)
- إصلاح تسريب للذاكرة أثناء نسخ الأرشيف في النسخ الاحتياطي. (*راجعه Cynthia Shang. أبلغ عنه Christian ROUX، Efremov Egor.*)
- إصلاح فيض المكدس في توليد عبارة مرور التشفير. (*راجعه Cynthia Shang. أبلغ عنه bsiara.*)
- إصلاح `repo-ls` `/` على مستودعات S3. (*راجعه Cynthia Shang. أبلغ عنه Lesovsky Alexey.*)

**الميزات:**

- دعم المستودعات المتعددة. (*ساهم به Cynthia Shang، David Steele. راجعه Stefan Fercot، Stephen Frost.*)
- دعم GCS لتخزين المستودع. (*راجعه Cynthia Shang، Daniel Farina.*)
- إضافة خيار `archive-header-check`. (*راجعه Stephen Frost، Cynthia Shang. اقترحه Hans-Jürgen Schönig.*)

**التحسينات:**

- تضمين قواعد البيانات النظامية المعاد إنشاؤها أثناء الاستعادة الانتقائية. (*ساهم به Stefan Fercot. راجعه Cynthia Shang.*)
- استثناء `content-length` من الترويسات الموقعة في S3. (*راجعه Cynthia Shang. اقترحه Brian P Bockelman.*)
- دمج خيارات تخزين المستودع الأقل شيوعًا. (*راجعه Cynthia Shang.*)
- السماح بقيمة افتراضية مخصصة لـ `config-path` عبر `./configure --with-configdir`. (*ساهم به Michael Schout. راجعه David Steele.*)
- تسجيل عملية نسخ الأرشيف أثناء `backup`. (*راجعه Cynthia Shang، Stefan Fercot.*)

**تحسينات التوثيق:**

- تحديث المرجع ليتضمن روابط لأمثلة دليل المستخدم. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- تحديث توثيق الاستعادة الانتقائية مع التنبيهات. (*راجعه Cynthia Shang، Stefan Fercot.*)
- إضافة توضيح `compress-type` إلى توثيق `archive-copy`. (*راجعه Cynthia Shang، Stefan Fercot.*)
- إضافة القيم الافتراضية لـ `compress-level` لكل قيمة `compress-type`. (*ساهم به Cynthia Shang. راجعه David Steele.*)
- إضافة ملاحظة حول وجوب تطابق إعدادات NFS المطلوبة مع PostgreSQL. (*ساهم به Cynthia Shang. راجعه David Steele.*)


### ملاحظات إصدار v2.32 {#v232-release-notes}

*أوامر المستودع*

*صدر في 8 فبراير 2021*

**إصلاحات الأخطاء:**

- إصلاح الاستئناف بعد حذف جزئي للنسخة الاحتياطية بسبب استئناف سابق. (*راجعه Cynthia Shang. أبلغ عنه Tom Swartz.*)

**الميزات:**

- إضافة الأمر `repo-ls`. (*راجعه Cynthia Shang، Stefan Fercot.*)
- إضافة الأمر `repo-get`. (*ساهم به Stefan Fercot، David Steele. راجعه Cynthia Shang.*)
- إضافة خيار `archive-mode-check`. (*ساهم به Stefan Fercot. راجعه David Steele، Michael Banck.*)

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
- إضافة خيار `repo-azure-endpoint`. (*راجعه Cynthia Shang، Brian Peterson. اقترحه Brian Peterson.*)
- إضافة خيار `pg-database`. (*راجعه Cynthia Shang.*)

**التحسينات:**

- تحسين مخرجات الأمر `info` عندما تُحدَّد stanza غير موجودة. (*ساهم به Stefan Fercot. راجعه Cynthia Shang، David Steele. اقترحه uspen.*)
- تحسين أداء قوائم الملفات الكبيرة في الأمرين `backup`/`restore`. (*راجعه Cynthia Shang، Oscar.*)
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

- استرجاع بيانات اعتماد S3 المؤقتة تلقائيًا على مثيلات AWS. (*ساهم به David Steele، Stephen Frost. راجعه Cynthia Shang، David Youatt، Aleš Zelený، Jeanette Bromage.*)
- إضافة خيار `archive-mode` لتعطيل الأرشفة عند الاستعادة. (*راجعه Stephen Frost. اقترحه Stephen Frost.*)

**التحسينات:**

- دعم PostgreSQL 13 beta3. قد تكسر التغييرات في إصدارات ملف التحكم/الكتالوج/WAL في الإصدارات التجريبية اللاحقة التوافق، لكن سيُحدَّث pgBackRest مع كل إصدار لمواكبة ذلك.
- `list`/`remove` غير المتزامنين لتخزين S3/Azure. (*راجعه Cynthia Shang، Stephen Frost.*)
- تحسين استخدام الذاكرة لاكتشاف العلاقات غير المسجلة عند بناء الـ manifest. (*راجعه Cynthia Shang، Stephen Frost، Brad Nicholson، Oscar. اقترحه Oscar، Brad Nicholson.*)
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

- دعم Azure لتخزين المستودع. (*راجعه Cynthia Shang، Don Seiler.*)
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

- تنفيذ TLS غير الحاجب. (*راجعه Slava Moudry، Cynthia Shang، Stephen Frost.*)
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
