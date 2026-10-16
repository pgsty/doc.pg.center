---
title: "دليل المستخدم (RHEL)"
linkTitle: "دليل المستخدم (EL)"
weight: 30
description: "دليل خطوة بخطوة لإعداد pgBackRest واستخدامه على أنظمة RHEL وRocky وAlmaLinux."
icon: fa-brands fa-redhat
module: [PGBACKREST]
categories: [دليل تعليمي]
upstream_link: "https://pgbackrest.org/user-guide-rhel.html"
---

--------

## المقدمة {#introduction}

هذا الدليل مُعدّ ليُتبع بالتسلسل من البداية إلى النهاية — إذ يعتمد كل قسم على سابقه. على سبيل المثال، يعتمد قسم [الاستعادة](#restore-1) على إعدادٍ يُجرى في قسم [البداية السريعة](#quick-start). وبمجرد أن يصبح pgBackRest قيد التشغيل يصبح التنقل بين الأقسام ممكنًا، لكن يُنصح باتباع ترتيب الدليل في المرة الأولى.

مع أن الأمثلة في هذا الدليل موجهة لأنظمة RHEL وPostgreSQL 14، فإن تطبيقها على أي توزيعة Unix وأي إصدار من PostgreSQL سيكون سهلًا إلى حد كبير. الأوامر الوحيدة الخاصة بنظام التشغيل هي أوامر إنشاء عناقيد PostgreSQL وبدئها وإيقافها وحذفها. ستكون أوامر pgBackRest نفسها على أي نظام Unix وإن كان موقع الملف التنفيذي قد يختلف. ورغم أن pgBackRest يسعى للعمل باتساق عبر إصدارات PostgreSQL، فهناك فروق دقيقة بين إصدارات PostgreSQL قد تظهر في هذا الدليل عند توضيح أمثلة معينة، مثل أسماء مسارات/ملفات PostgreSQL وإعداداته.

يمكن الاطلاع على معلومات التهيئة والوثائق الخاصة بـ PostgreSQL في [الدليل](http://www.postgresql.org/docs/14/static/index.html) الخاص بـ PostgreSQL.

يتبع هذا الدليل نهجًا جديدًا نوعًا ما في التوثيق. يُنفَّذ كل أمر على آلة افتراضية عند بناء الوثائق من مصدر XML. هذا يعني أنه يمكنك أن تثق بدرجة كبيرة بأن الأوامر تعمل بشكل صحيح بالترتيب المعروض. تُلتقط المخرجات وتُعرض أسفل الأمر عند الاقتضاء. وإذا لم تُضمَّن المخرجات فذلك لأنها اعتُبرت غير ذات صلة أو مشتتة للسرد.

جميع الأوامر مخصصة لتُنفَّذ بمستخدم عادي يملك صلاحيات sudo لمستخدمَي `root` و`postgres` معًا. ومن الممكن أيضًا تنفيذ الأوامر مباشرةً بمستخدميها المعنيين دون تعديل، وفي هذه الحالة يمكن حذف أوامر `sudo`.

--------

## المفاهيم {#concepts}

تُعرَّف المفاهيم التالية لصلتها بـ pgBackRest وPostgreSQL وهذا الدليل.

### النسخ الاحتياطي {#backup}

النسخة الاحتياطية هي نسخة متسقة من عنقود قاعدة بيانات يمكن استعادتها للتعافي من فشل عتادي، أو لإجراء الاستعادة إلى نقطة زمنية، أو لتشغيل خادم استعداد جديد.

**النسخة الاحتياطية الكاملة**: ينسخ pgBackRest كامل محتويات عنقود قاعدة البيانات إلى النسخة الاحتياطية. النسخة الاحتياطية الأولى للعنقود تكون دائمًا نسخة كاملة. يستطيع pgBackRest دائمًا استعادة نسخة كاملة مباشرةً. لا تعتمد النسخة الكاملة في اتساقها على أي ملفات خارجها.

**النسخة الاحتياطية التفاضلية**: ينسخ pgBackRest فقط ملفات عنقود قاعدة البيانات التي تغيرت منذ آخر نسخة كاملة. يستعيد pgBackRest النسخة التفاضلية بنسخ جميع الملفات في النسخة التفاضلية المختارة والملفات غير المتغيرة المناسبة من النسخة الكاملة السابقة. ميزة النسخة التفاضلية أنها تتطلب مساحة قرص أقل من النسخة الكاملة، غير أن النسختين التفاضلية والكاملة يجب أن تكونا كلتاهما صالحتين لاستعادة النسخة التفاضلية.

**النسخة الاحتياطية التزايدية**: ينسخ pgBackRest فقط ملفات عنقود قاعدة البيانات التي تغيرت منذ آخر نسخة احتياطية (التي قد تكون نسخة تزايدية أخرى، أو نسخة تفاضلية، أو نسخة كاملة). وبما أن النسخة التزايدية تضم فقط الملفات المتغيرة منذ النسخة السابقة، فهي عمومًا أصغر بكثير من النسخ الكاملة أو التفاضلية. وكما هو الحال مع النسخة التفاضلية، تعتمد النسخة التزايدية في استعادتها على صلاحية نسخ احتياطية أخرى. ولأن النسخة التزايدية لا تضم سوى الملفات منذ آخر نسخة احتياطية، فيجب أن تكون جميع النسخ التزايدية السابقة رجوعًا حتى التفاضلية السابقة، والنسخة التفاضلية السابقة، والنسخة الكاملة السابقة، كلها صالحة لإجراء استعادة النسخة التزايدية. وإذا لم توجد أي نسخة تفاضلية فيجب أن تكون جميع النسخ التزايدية السابقة رجوعًا حتى النسخة الكاملة السابقة — التي يجب أن تكون موجودة — وكذلك النسخة الكاملة نفسها صالحة لاستعادة النسخة التزايدية.

### الاستعادة {#restore}

الاستعادة هي فعل نسخ نسخة احتياطية إلى نظام ستُشغَّل عليه كعنقود قاعدة بيانات حي. تتطلب الاستعادة ملفات النسخة الاحتياطية ومقطع WAL واحدًا أو أكثر لتعمل بشكل صحيح.

### سجل الكتابة المسبقة (WAL) {#write-ahead-log-wal}

‏WAL هو الآلية التي يستخدمها PostgreSQL لضمان عدم فقدان أي تغييرات مُثبتة. تُكتب المعاملات تسلسليًا إلى WAL وتُعد المعاملة مُثبتة عندما تُدفع تلك الكتابات إلى القرص. بعد ذلك، تكتب عملية في الخلفية التغييرات إلى ملفات عنقود قاعدة البيانات الرئيسية (المعروفة أيضًا بالكومة heap). في حال حدوث انهيار، يُعاد تشغيل WAL لجعل قاعدة البيانات متسقة.

‏WAL غير محدود من الناحية النظرية، لكنه في الممارسة مقسم إلى ملفات فردية بحجم 16MB تسمى المقاطع. تتبع مقاطع WAL اصطلاح التسمية `0000000100000A1E000000FE` حيث تمثل أول 8 خانات سداسية عشرية الخط الزمني وتمثل الخانات الـ 16 التالية الرقم التسلسلي المنطقي (LSN).

### التشفير {#encryption}

التشفير هو عملية تحويل البيانات إلى صيغة غير قابلة للتمييز ما لم تُقدَّم كلمة المرور المناسبة (المشار إليها أيضًا بعبارة المرور passphrase).

سيشفّر pgBackRest المستودع استنادًا إلى كلمة مرور يقدمها المستخدم، وبذلك يمنع الوصول غير المصرح به إلى البيانات المخزنة داخل المستودع.

--------

## ترقية pgBackRest {#upgrading-pgbackrest}


### ترقية pgBackRest من v2.x إلى v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

الترقية من v2.x إلى v2.y مباشرة. لم يتغير تنسيق المستودع، فبالنسبة لمعظم التثبيتات لا يتعدى الأمر تثبيت الملفات التنفيذية للإصدار الجديد. ومن الممكن أيضًا الرجوع إلى إصدار أقدم إذا لم تكن قد استخدمت ميزات جديدة لا يدعمها الإصدار الأقدم.

مهم:

يجب أن تتطابق نسختا pgBackRest المحلية والبعيدة تطابقًا تامًا، لذا ينبغي ترقيتهما معًا. في حال عدم التطابق، لن تعمل أرشفة WAL والنسخ الاحتياطي حتى يتطابق الإصداران. في هذه الحالة سيُبلَّغ عن الخطأ التالي: `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.

--------

## البناء {#build}

يُفضَّل تثبيت pgBackRest من حزمة على البناء من المصدر. راجع [التثبيت](#installation) لمزيد من المعلومات عن الحزم.

عند البناء من المصدر من الأفضل استخدام مضيف بناء بدلًا من البناء في بيئة الإنتاج. كثير من الأدوات المطلوبة للبناء لا ينبغي عمومًا تثبيتها في بيئة الإنتاج. يتكون pgBackRest من ملف تنفيذي واحد فيسهل نسخه إلى مضيف جديد بعد بنائه.

build **⇒** تنزيل الإصدار `2.59.3` من pgBackRest إلى المسار `/build`

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** تثبيت تبعيات البناء

```bash
sudo yum install meson gcc postgresql14-devel openssl-devel libxml2-devel \
       lz4-devel libzstd-devel bzip2-devel libssh2-devel systemd-devel
```

build **⇒** تهيئة pgBackRest وتجميعه

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.59.3
ninja -C /build/pgbackrest
```

build **⇒** تشغيل اختبارات الدخان اختياريًا للتحقق من أن pgBackRest بُني بشكل صحيح

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               10.32s

Ok:                 1
       [filtered 6 lines of output]
```

--------

## التثبيت {#installation}

يُنشأ مضيف جديد باسم pg-primary ليحتوي عنقود العرض التوضيحي ويشغّل أمثلة pgBackRest.

يُفضَّل تثبيت pgBackRest من حزمة على البناء من المصدر. عند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. في هذه الحالة قد يلزم إنشاء الأدلة أو تحديث الصلاحيات يدويًا.

تتوفر حزم RHEL لـ pgBackRest على [yum.postgresql.org](http://yum.postgresql.org).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-primary **⇒** تثبيت التبعيات

```bash
sudo yum install postgresql-libs libssh2
```

pg-primary **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والتهيئة وملف تهيئة.

pg-primary **⇒** إنشاء ملف تهيئة pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

ينبغي الآن أن يكون pgBackRest مثبتًا بشكل صحيح لكن من الأفضل التحقق. إذا فاتت أي تبعية فستحصل على خطأ عند تشغيل pgBackRest من سطر الأوامر.

pg-primary **⇒** التأكد من نجاح التثبيت

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.59.3 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## البداية السريعة {#quick-start}

سيغطي قسم البداية السريعة التهيئة الأساسية لـ pgBackRest وPostgreSQL وسيقدم الأوامر `backup` و`restore` و`info`.

### إعداد عنقود العرض التوضيحي {#setup-demo-cluster}

إنشاء عنقود العرض التوضيحي اختياري لكنه موصى به بشدة، خاصة للمستخدمين الجدد، لأن أمثلة الأوامر في دليل المستخدم تشير إلى عنقود العرض التوضيحي؛ تفترض الأمثلة أن عنقود العرض يعمل على المنفذ الافتراضي (أي 5432). لن يُشغَّل العنقود حتى قسم لاحق لأنه ما زالت هناك بعض التهيئة المطلوبة.

pg-primary **⇒** إنشاء عنقود العرض التوضيحي

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

بشكل افتراضي يضم RHEL يوم الأسبوع في اسم ملف السجل. هذا يجعل دليل المستخدم أكثر تعقيدًا قليلًا لذا يُضبط log_filename على قيمة ثابتة.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** ضبط log_filename

```ini
log_filename = 'postgresql.log'
```

### تهيئة stanza العنقود {#configure-cluster-stanza}

الـ stanza هي تهيئة عنقود قاعدة بيانات PostgreSQL تحدد موقعه وكيفية أخذ نسخة احتياطية منه وخيارات الأرشفة وغير ذلك. لن يملك معظم خوادم قواعد البيانات سوى عنقود PostgreSQL واحد وبالتالي stanza واحدة، بينما ستملك خوادم النسخ الاحتياطي stanza لكل عنقود قاعدة بيانات يحتاج إلى نسخ احتياطي.

من المغري تسمية الـ stanza باسم العنقود الأساسي، لكن الاسم الأفضل هو ما يصف قواعد البيانات التي يحتويها العنقود. ولأن اسم الـ stanza سيُستخدم للأساسي وجميع النسخ المتماثلة، فمن الأنسب اختيار اسم يصف الوظيفة الفعلية للعنقود، مثل app أو dw، بدلًا من اسم العنقود المحلي، مثل main أو prod.

يصف الاسم 'demo' غرض هذا العنقود بدقة لذا سيشكل أيضًا اسم stanza جيدًا.

يحتاج pgBackRest إلى معرفة مكان الدليل الأساسي للبيانات لعنقود PostgreSQL. يمكن طلب المسار من PostgreSQL مباشرةً، لكن في سيناريو الاستعادة لن تكون عملية PostgreSQL متاحة. أثناء النسخ الاحتياطي ستُقارن القيمة المزودة إلى pgBackRest بالمسار الذي يعمل عليه PostgreSQL ويجب أن تتساويا وإلا سيرجع النسخ الاحتياطي خطأً. تأكد من أن `pg-path` يساوي تمامًا data_directory كما يبلغ عنه PostgreSQL.

بشكل افتراضي يخزن RHEL العناقيد في `/var/lib/pgsql/[version]/data` لذا يسهل تحديد المسار الصحيح لدليل البيانات.

عند إنشاء الملف `/etc/pgbackrest/pgbackrest.conf`، يجب منح مالك قاعدة البيانات (وهو عادة `postgres`) صلاحيات القراءة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة دليل بيانات عنقود PostgreSQL

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data
```

تتبع ملفات تهيئة pgBackRest اصطلاحًا شبيهًا بـ INI في Windows. تُحدد الأقسام بنص بين قوسين مربعين ويحتوي كل قسم على أزواج مفتاح/قيمة. الأسطر التي تبدأ بـ `#` تُهمل ويمكن استخدامها تعليقات، لكن التعليقات في نهاية السطر بعد قيمة على السطر نفسه غير مدعومة. الاقتباس غير مدعوم وتُقتطع الفراغات من المفاتيح والقيم. ستُدمج الأقسام إذا ظهرت أكثر من مرة.

هناك عدة طرق يمكن بها تحميل ملفات تهيئة pgBackRest:

- `config` و`config-include-path` افتراضيان: سيُحمَّل ملف التهيئة الافتراضي، إن وُجد، وستُلحق ملفات `*.conf` في مسار تضمين التهيئة الافتراضي، إن وُجدت.
- تحديد الخيار `config`: سيُحمَّل ملف التهيئة المحدد فقط ويُتوقع وجوده.
- تحديد `config-include-path`: ستُحمَّل ملفات `*.conf` في مسار تضمين التهيئة ويُشترط وجود المسار. سيُحمَّل ملف التهيئة الافتراضي إن وُجد. إذا رغبت في تحميل الملفات في مسار تضمين التهيئة المحدد فقط، فيمكن أيضًا تمرير الخيار `--no-config`.
- تحديد `config` و`config-include-path` معًا: باستخدام القيم التي حددها المستخدم، سيُحمَّل ملف التهيئة وستُلحق ملفات `*.conf` في مسار تضمين التهيئة. ويُتوقع وجود الملفات.
- تحديد `config-path`: يتجاوز هذا الإعداد المسار الأساسي للموقع الافتراضي لملف التهيئة و/أو المسار الأساسي لإعداد config-include-path الافتراضي، ما لم يُضبط خيار config و/أو config-include-path صراحةً.

تُسلسل الملفات وكأنها ملف واحد كبير ويجب أن يكون كل ملف صالحًا بذاته. هذا يعني أنه يجب تحديد الأقسام في كل ملف يلزم فيها تخزين مفتاح/قيمة. الترتيب لا يهم لكن هناك أسبقية بناءً على الأقسام. الأسبقية (من الأعلى إلى الأدنى):

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

ملاحظة:

‏`--config` و`--config-include-path` و`--config-path` خيارات متاحة من سطر الأوامر فقط.

يمكن أيضًا تهيئة pgBackRest باستخدام متغيرات البيئة (المثال أدناه)؛ وتنطبق هذه المتغيرات على أوامر مثل [backup](/ar/pgbackrest/command/backup/) و[restore](/ar/pgbackrest/command/restore/) و[archive-push](/ar/pgbackrest/command/archive-push/).

pg-primary **⇒** تهيئة `log-path` باستخدام البيئة

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.59.3 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### إنشاء المستودع {#create-the-repository}

المستودع هو المكان الذي يخزن فيه pgBackRest النسخ الاحتياطية ويؤرشف فيه مقاطع WAL.

قد يصعب تقدير المساحة التي ستحتاجها مسبقًا. أفضل ما يمكن فعله هو أخذ بعض النسخ الاحتياطية ثم تسجيل أحجام الأنواع المختلفة من النسخ (full/incr/diff) وقياس كمية WAL المولدة يوميًا. سيعطيك هذا فكرة عامة عن المساحة التي ستحتاجها، وإن كانت المتطلبات ستتغير على الأرجح مع مرور الوقت مع تطور قاعدة بياناتك بطبيعة الحال.

في هذا العرض التوضيحي سيُخزن المستودع على المضيف نفسه الذي يعمل عليه خادم PostgreSQL. هذا أبسط تهيئة وهي مفيدة في الحالات التي تُستخدم فيها برمجيات نسخ احتياطي تقليدية لأخذ نسخة احتياطية من مضيف قاعدة البيانات.

pg-primary **⇒** إنشاء مستودع pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

يجب تهيئة مسار المستودع ليعرف pgBackRest أين يجده.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار مستودع pgBackRest

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest
```

يمكن أيضًا تهيئة مستودعات متعددة. راجع [المستودعات المتعددة](#multiple-repositories) للتفاصيل.

### تهيئة الأرشفة {#configure-archiving}

يتطلب أخذ نسخة احتياطية من عنقود PostgreSQL قيد التشغيل تمكين أرشفة WAL. ‏`%p` هي طريقة PostgreSQL لتحديد موقع مقطع WAL المراد أرشفته. لاحظ أنه سيُنشأ *على الأقل* مقطع WAL واحد أثناء عملية النسخ الاحتياطي حتى لو لم تُجرَ أي كتابات صريحة إلى العنقود.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** تهيئة إعدادات الأرشفة

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

يجب إعادة تشغيل عنقود PostgreSQL بعد إجراء هذه التغييرات وقبل إجراء نسخ احتياطي.

pg-primary **⇒** إعادة تشغيل عنقود العرض التوضيحي

```bash
sudo systemctl restart postgresql-14.service
```

إعداد `hot_standby` ممكّن افتراضيًا وينبغي إبقاؤه كذلك على كل عنقود. يمكن استعادة أي عنقود كخادم استعداد لاحقًا، مثل أساسي يُعاد بناؤه كخادم استعداد بعد تجاوز الأعطال، ولن يقبل خادم الاستعداد اتصالات القراءة فقط بدونه.

عندما يُتوقع أن يستغرق وصول مقطع WAL مؤرشف إلى مستودع pgBackRest أكثر من 60 ثانية (الافتراضي)، ينبغي زيادة خيار `archive-timeout` في pgBackRest. لاحظ أن هذا الخيار ليس نفسه خيار archive_timeout في PostgreSQL الذي يُستخدم لفرض تبديل مقطع WAL؛ وهو مفيد لقواعد البيانات التي تمر بها فترات خمول طويلة. لمزيد من المعلومات عن خيار archive_timeout في PostgreSQL، راجع [سجل الكتابة المسبقة](https://www.postgresql.org/docs/current/static/runtime-config-wal.html) في وثائق PostgreSQL.

يمكن تهيئة الأمر `archive-push` بخيارات خاصة به. مثلًا، يمكن ضبط مستوى ضغط أدنى لتسريع الأرشفة دون التأثير في الضغط المستخدم للنسخ الاحتياطي.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `archive-push` لاستخدام مستوى ضغط أدنى

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

يمكن استخدام أسلوب التهيئة هذا مع أي أمر بل يمكنه استهداف stanza محددة، مثل `demo:archive-push`.

### تهيئة الاحتفاظ {#configure-retention}

ينهي pgBackRest صلاحية النسخ الاحتياطية استنادًا إلى خيارات الاحتفاظ.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة الاحتفاظ بـ 2 من النسخ الكاملة

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

يمكن الاطلاع على مزيد من المعلومات عن الاحتفاظ في قسم [الاحتفاظ](#retention).

### تهيئة تشفير المستودع {#configure-repository-encryption}

سيُهيأ المستودع بنوع شيفرة ومفتاح لعرض التشفير. يتم التشفير دائمًا من جهة العميل حتى لو كان نوع المستودع (مثل S3 أو أي مخزن كائنات آخر) يدعم التشفير.

من المهم استخدام عبارة مرور طويلة وعشوائية لمفتاح الشيفرة. طريقة جيدة لتوليد واحدة هي تشغيل: `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة تشفير مستودع pgBackRest

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

ملاحظة:

توضع إعدادات التشفير في القسم `[global]`، أعلاه، ليتمكن الأمر `info` من قراءة جميع الـ stanzas. بدون الخيار `stanza` يقرأ الأمر `info` إعدادات التشفير من القسم `[global]` فقط، لذا تتطلب إعدادات التشفير المهيأة لكل stanza استخدام الخيار `stanza` لقراءة stanza مشفرة.

بمجرد تهيئة المستودع وإنشاء الـ stanza والتحقق منها، لا يمكن تغيير إعدادات تشفير المستودع.

### إنشاء الـ stanza {#create-the-stanza}

يجب تشغيل الأمر `stanza-create` لتهيئة الـ stanza. يُوصى بتشغيل الأمر `check` بعد `stanza-create` لضمان تهيئة الأرشفة والنسخ الاحتياطي بشكل صحيح.

pg-primary **⇒** إنشاء الـ stanza والتحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1200-90682d35 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### التحقق من التهيئة {#check-the-configuration}

يتحقق الأمر `check` من أن pgBackRest وإعداد archive_command مهيآن بشكل صحيح للأرشفة والنسخ الاحتياطي للـ stanza المحددة. سيحاول التحقق من جميع المستودعات وقواعد البيانات المهيأة للمضيف الذي يُشغَّل عليه الأمر. يكشف عن سوء التهيئة، خصوصًا في الأرشفة، الذي ينتج نسخًا احتياطية غير مكتملة لأن مقاطع WAL المطلوبة لم تصل إلى الأرشيف. يمكن تشغيل الأمر على مضيف PostgreSQL أو على مضيف المستودع. يمكن أيضًا تشغيل الأمر على مضيف الاستعداد، لكن بما أنه لا يمكن تنفيذ `pg_switch_xlog()`/`pg_switch_wal()` على الاستعداد، فسيتحقق الأمر من تهيئة المستودع فقط.

لاحظ أنه يُستدعى `pg_create_restore_point('pgBackRest Archive Check')` و`pg_switch_xlog()`/`pg_switch_wal()` لإجبار PostgreSQL على أرشفة مقطع WAL.

pg-primary **⇒** التحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1233-340209f5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000100000000/000000010000000000000001-dac4045f133f7305d6342d81e428e60050928bc4.gz' on repo1
P00   INFO: check command end: completed successfully
```

### ضبط الأداء {#performance-tuning}

يملك pgBackRest عددًا من خيارات الأداء غير ممكّنة افتراضيًا حفاظًا على التوافق الرجعي في المستودع. لكن عند إنشاء مستودع جديد يُوصى بالخيارات التالية. يمكن استخدامها أيضًا على مستودع قائم مع التحفظ بأن الإصدارات الأقدم من pgBackRest لن تكون قادرة على قراءة المستودع. يعتمد عدم التوافق هذا على وقت إدخال الميزة، كما هو موضح في القائمة أدناه.

- `compress-type` - يحدد خوارزمية الضغط التي يستخدمها الأمران `backup` و`archive-push`. الافتراضي هو `gz` (Gzip) لكن يُوصى بـ `zst` (Zstandard) لأنه أسرع بكثير ويوفر ضغطًا مشابهًا لـ `gz`. يدعم خيار `compress-type` القيمة `zst` منذ [v2.27](/ar/pgbackrest/release/#v227-release-notes). راجع [نوع الضغط](/ar/pgbackrest/configuration/#compress-type-option---compress-type) لمزيد من التفاصيل.
- `repo-bundle` - يجمع الملفات الصغيرة أثناء النسخ الاحتياطي لتوفير المساحة وتحسين سرعة الأمرين `backup` و`restore`، خاصة على مخازن الكائنات مثل S3. قُدّم خيار `repo-bundle` في [v2.39](/ar/pgbackrest/release/#v239-release-notes). راجع [تجميع الملفات](#file-bundling) لمزيد من التفاصيل.
- `repo-block` - يخزن فقط أجزاء الملفات التي تغيرت بدلًا من الملف بأكمله أثناء `diff`/`incr` `backup`. هذا يوفر المساحة ويزيد سرعة الأمر `backup`. قُدّم خيار `repo-block` في [v2.46](/ar/pgbackrest/release/#v246-release-notes) لكن يُوصى بالإصدار [v2.52.1](/ar/pgbackrest/release/#v2521-release-notes) على الأقل. راجع [التزايدي بالكتل](#block-incremental) لمزيد من التفاصيل.

هناك خيارات أداء أخرى غير ممكّنة افتراضيًا لأنها تتطلب تهيئة إضافية أو لأن الافتراضي آمن (لكنه ليس الأمثل). هذه الخيارات متاحة في جميع إصدارات v2 من pgBackRest.

- `process-max` - يحدد عدد العمليات التي ستُستخدم للأوامر. الافتراضي هو 1، وهو ما لا يكون مناسبًا تقريبًا أبدًا. يستخدم كل أمر `process-max` بشكل مختلف لذا راجع وثائق كل أمر لتفاصيل الاستخدام.
- `archive-async` - يؤرشف ملفات WAL إلى المستودع على دفعات مما يزيد سرعة الأرشفة كثيرًا. غير ممكّن افتراضيًا لأنه يتطلب إنشاء مسار spool. راجع [الأرشفة غير المتزامنة](#asynchronous-archiving) لمزيد من التفاصيل.
- `backup-standby` - يجري النسخ الاحتياطي على خادم استعداد بدلًا من الأساسي لتقليل الحمل على الأساسي. غير ممكّن افتراضيًا لأنه يتطلب تهيئة إضافية ووجود مضيف استعداد واحد أو أكثر. راجع [النسخ الاحتياطي من خادم الاستعداد](#backup-from-a-standby) لمزيد من التفاصيل.

### إجراء نسخة احتياطية {#perform-a-backup}

بشكل افتراضي سينتظر pgBackRest نقطة التفتيش المجدولة التالية بانتظام قبل بدء النسخ الاحتياطي. بحسب إعدادَي checkpoint_timeout وcheckpoint_segments في PostgreSQL قد يمضي وقت غير قصير قبل اكتمال نقطة تفتيش وبدء النسخ الاحتياطي. عمومًا من الأفضل ضبط `start-fast=y` ليبدأ النسخ الاحتياطي فورًا. هذا يفرض نقطة تفتيش، لكن بما أن النسخ الاحتياطية تُجرى عادة مرة يوميًا فلن يكون لنقطة التفتيش الإضافية تأثير ملحوظ في الأداء. ومع ذلك، على العناقيد المشغولة جدًا قد يكون الأفضل تمرير `--start-fast` في سطر الأوامر عند الحاجة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة البدء السريع للنسخ الاحتياطي

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

لأخذ نسخة احتياطية من عنقود PostgreSQL شغّل pgBackRest بالأمر `backup`.

pg-primary **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-185647F
P00   INFO: full backup size = 25.2MB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

بشكل افتراضي سيحاول pgBackRest إجراء نسخة احتياطية تزايدية. لكن يجب أن تستند النسخة التزايدية إلى نسخة كاملة، ولما لم تكن هناك نسخة كاملة، أجرى pgBackRest نسخة كاملة بدلًا منها.

يمكن استخدام الخيار `type` لتحديد نسخة كاملة أو تفاضلية.

pg-primary **⇒** نسخة تفاضلية من عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-185647F_20261002-185651D
P00   INFO: diff backup size = 9.2KB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1398-36e29fed --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

لم يظهر تحذير هذه المرة لأن نسخة كاملة كانت موجودة مسبقًا. وبينما يمكن أن تستند النسخ التزايدية إلى نسخة كاملة *أو* تفاضلية، يجب أن تستند النسخ التفاضلية إلى نسخة كاملة. يمكن إجراء نسخة كاملة بتشغيل الأمر `backup` مع `--type=full`.

أثناء النسخ الاحتياطي أثناء تشغيل PostgreSQL ينتظر pgBackRest أرشفة مقاطع WAL المطلوبة لاتساق النسخة الاحتياطية. يحكم وقت الانتظار هذا خيار `archive-timeout` في pgBackRest الذي يبلغ افتراضيه 60 ثانية. إذا كان معروفًا أن أرشفة مقطع فردي تستغرق وقتًا أطول فينبغي زيادة هذا الخيار.

### جدولة النسخ الاحتياطي {#schedule-a-backup}

يمكن جدولة النسخ الاحتياطية بأدوات مثل cron.

في المثال التالي، تُهيأ مهمتا cron لتُشغَّلا؛ النسخ الاحتياطية الكاملة مجدولة الساعة 6:30 صباحًا كل أحد، والنسخ الاحتياطية التفاضلية مجدولة الساعة 6:30 صباحًا من الاثنين إلى السبت. إذا ثُبّتت هذه الـ crontab لأول مرة في منتصف الأسبوع، فسيجري pgBackRest نسخًا احتياطيًا كاملًا في المرة الأولى التي تُنفَّذ فيها المهمة التفاضلية، تتبعها في اليوم التالي نسخة احتياطية تفاضلية.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

بمجرد جدولة النسخ الاحتياطية من المهم تهيئة الاحتفاظ لتنتهي صلاحية النسخ الاحتياطية وفق جدول منتظم، راجع [الاحتفاظ](#retention).

### معلومات النسخ الاحتياطي {#backup-information}

استخدم الأمر `info` للحصول على معلومات عن النسخ الاحتياطية.

pg-primary **⇒** الحصول على معلومات عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-185647F
            timestamp start/stop: 2026-10-02 18:56:47+00 / 2026-10-02 18:56:50+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup set size: 3.2MB, backup size: 3.2MB

        diff backup: 20261002-185647F_20261002-185651D
            timestamp start/stop: 2026-10-02 18:56:51+00 / 2026-10-02 18:56:52+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 25.2MB, database backup size: 9.2KB
            repo1: backup set size: 3.2MB, backup size: 864B
            backup reference total: 1 full
```

يعمل الأمر `info` على stanza واحدة أو على جميع الـ stanzas. المخرجات النصية هي الافتراضية وتعطي ملخصًا مقروءًا للنسخ الاحتياطية للـ stanza أو الـ stanzas المطلوبة. هذا التنسيق قابل للتغيير مع أي إصدار.

للحصول على مخرجات قابلة للقراءة آليًا استخدم `--output=json`. تحتوي مخرجات JSON على معلومات أكثر بكثير من المخرجات النصية وتبقى مستقرة ما لم يُكتشف خطأ.

لتسريع التنفيذ، اقصر المخرجات على معلومات التقدم فقط بتحديد `--detail-level=progress`. لاحظ أن هذا يتخطى جميع الفحوص عدا فحص توفر الـ stanza.

لكل stanza قسم منفصل ويمكن قصر المخرجات على stanza واحدة بخيار `--stanza`. تعطي حالة '`status`' للـ stanza مؤشرًا موجزًا على صحتها. إذا كانت '`ok`' فذلك يعني أن pgBackRest يعمل بشكل طبيعي. في حال وجود مستودعات متعددة، فإن حالة '`mixed`' تشير إلى أن الـ stanza ليست في حالة صحية على مستودع واحد أو أكثر؛ وفي هذه الحالة ستُفصَّل حالة الـ stanza لكل مستودع. في الحالات التي يقع فيها خطأ على أحد المستودعات لا يُعد من رموز الأخطاء المعروفة، سيُستخدم رمز الخطأ '`other`' وستُقدَّم تفاصيل الخطأ الكاملة. يعرض '`wal archive min/max`' الحد الأدنى والأقصى لـ WAL المخزن حاليًا في الأرشيف، وفي حالة تعدد المستودعات سيُبلغ عنه عبر جميع المستودعات ما لم يُضبط الخيار `--repo`. لاحظ أنه قد تكون هناك فجوات بسبب سياسات الاحتفاظ بالأرشيف أو لأسباب أخرى.

ستظهر رسالتا '`backup/expire running`' و/أو '`restore running`' بجانب معلومات '`status`' إذا كان أي من تلك الأوامر قيد التشغيل حاليًا على المضيف. سيُبلَّغ أيضًا عن التقدم لكل مستودع في المخرجات النصية وستُضم مصفوفة '`repo`' إلى مخرجات JSON.

تُعرض النسخ الاحتياطية من الأقدم إلى الأحدث. ستكون النسخة الاحتياطية الأقدم *دائمًا* نسخة كاملة (يُشار إليها بـ `F` في نهاية التسمية) لكن الأحدث قد تكون كاملة أو تفاضلية (تنتهي بـ `D`) أو تزايدية (تنتهي بـ `I`).

تحدد '`timestamp start/stop`' الفترة الزمنية التي جرى فيها النسخ الاحتياطي. يمكن استخدام '`timestamp stop`' لتحديد النسخة الاحتياطية المراد استخدامها عند إجراء الاستعادة إلى نقطة زمنية. مزيد من المعلومات عن الاستعادة إلى نقطة زمنية في قسم [الاستعادة إلى نقطة زمنية](#point-in-time-recovery).

تحدد '`wal start/stop`' نطاق WAL المطلوب لجعل قاعدة البيانات متسقة عند الاستعادة. سيضمن الأمر `backup` وجود نطاق WAL هذا في الأرشيف قبل الاكتمال.

حجم '`database size`' هو الحجم الكلي غير المضغوط لقاعدة البيانات، بينما '`database backup size`' هي كمية البيانات في قاعدة البيانات المطلوب أخذ نسخة احتياطية منها فعليًا (ستكونان متماثلتين للنسخ الكاملة).

يشير '`repo`' إلى المستودع الذي تقع فيه هذه النسخة الاحتياطية. يضم '`backup set size`' جميع ملفات هذه النسخة الاحتياطية وأي نسخ مشار إليها في المستودع والمطلوبة لاستعادة قاعدة البيانات من هذه النسخة، بينما يضم '`backup size`' فقط ملفات هذه النسخة الاحتياطية (ستكونان أيضًا متماثلتين للنسخ الكاملة). تعكس أحجام المستودع أحجام الملفات المضغوطة إذا كان الضغط ممكّنًا في pgBackRest.

يلخص '`backup reference total`' قائمة النسخ الاحتياطية الإضافية المطلوبة لاستعادة هذه النسخة. استخدم الخيار `--set` لعرض قائمة المراجع الكاملة.

### استعادة نسخة احتياطية {#restore-a-backup}

تحميك النسخ الاحتياطية من عدد من سيناريوهات الكوارث، أكثرها شيوعًا الفشل العتادي وإتلاف البيانات. أسهل طريقة لمحاكاة إتلاف البيانات هي إزالة ملف مهم من عنقود PostgreSQL.

pg-primary **⇒** إيقاف عنقود العرض التوضيحي وحذف الملف `pg_control`

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres rm /var/lib/pgsql/14/data/global/pg_control
```

سيؤدي بدء العنقود بدون هذا الملف المهم إلى خطأ.

pg-primary **⇒** محاولة بدء عنقود العرض التوضيحي التالف

```bash
sudo systemctl start postgresql-14.service
sudo systemctl status postgresql-14.service
```

```text
postgresql-14.service - PostgreSQL 14 database server
    Loaded: loaded (/usr/lib/systemd/system/postgresql-14.service, disabled)
    Active: failed (failed)
```

لاستعادة نسخة احتياطية من عنقود PostgreSQL شغّل pgBackRest بالأمر `restore`. يجب إيقاف العنقود (وهو موقوف بالفعل في هذه الحالة) ويجب إزالة جميع الملفات من دليل بيانات PostgreSQL.

pg-primary **⇒** إزالة الملفات القديمة من عنقود العرض التوضيحي

```bash
sudo -u postgres find /var/lib/pgsql/14/data -mindepth 1 -delete
```

pg-primary **⇒** استعادة عنقود العرض التوضيحي وبدء PostgreSQL

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo systemctl start postgresql-14.service
```

نجح بدء العنقود هذه المرة لأن الاستعادة عوضت الملف `pg_control` المفقود.

مزيد من المعلومات عن الأمر `restore` في قسم [الاستعادة](#restore-1).

--------

## المراقبة {#monitoring}

المراقبة جزء مهم من أي نظام إنتاجي. هناك العديد من الأدوات المتاحة ويمكن مراقبة pgBackRest على أي منها بقليل من العمل.

يستطيع pgBackRest إخراج معلومات عن المستودع بصيغة JSON تتضمن قائمة بجميع النسخ الاحتياطية لكل stanza ومعلومات أرشيف WAL.

### داخل PostgreSQL {#in-postgresql}

يتيح أمر `COPY` في PostgreSQL تحميل معلومات pgBackRest إلى جدول. يغلّف المثال التالي ذلك المنطق في دالة يمكن استخدامها لإجراء استعلامات فورية.

pg-primary **⇒** تحميل دالة معلومات pgBackRest لـ PostgreSQL

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

الآن يمكن استخدام الدالة `monitor.pgbackrest_info()` لتحديد وقت آخر نسخة احتياطية ناجحة وWAL المؤرشف لكل stanza.

pg-primary **⇒** الاستعلام عن وقت آخر نسخة احتياطية ناجحة وWAL المؤرشف

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 18:56:52+00 | 000000010000000000000005
(1 row)
```

--------

## النسخ الاحتياطي {#backup-1}

عند تهيئة مستودعات متعددة، سيجري pgBackRest النسخ الاحتياطي إلى المستودع ذي الأولوية الأعلى (مثل `repo1`) ما لم يُحدد الخيار `--repo`.

لا يملك pgBackRest مجدولًا مدمجًا لذا من الأفضل تشغيله من cron أو آلية جدولة أخرى.

راجع [إجراء نسخة احتياطية](#perform-a-backup) لمزيد من التفاصيل والأمثلة.

### تجميع الملفات {#file-bundling}

تجميع الملفات معًا في المستودع يوفر الوقت أثناء النسخ الاحتياطي وبعض المساحة في المستودع. هذا ملحوظ بشكل خاص عندما يُخزن المستودع على مخزن كائنات مثل S3 أو على أنظمة ملفات بأحجام كتل كبيرة. وقت إنشاء الملف الواحد على مخازن الكائنات أعلى، وقد يكلف تخزين الملفات الصغيرة جدًا بقدر ما تكلفه الملفات الأكبر.

تُمكَّن ميزة تجميع الملفات بالخيار `repo-bundle`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-bundle`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

ستحتوي النسخة الكاملة بدون تجميع ملفات على 1000 ملف أو أكثر في مسار النسخ الاحتياطي، لكن مع التجميع يقل العدد الكلي للملفات كثيرًا. فائدة إضافية هي أن الملفات ذات الطول الصفري لا تُخزن (إلا في البيان manifest)، بينما في النسخ الاحتياطي العادي يُخزن كل ملف صفري الطول على حدة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** التحقق من العدد الكلي للملفات

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

يمكن استخدام الخيارين `repo-bundle-size` و`repo-bundle-limit` للضبط، وإن كان يُتوقع أن تكون القيم الافتراضية مثلى في معظم الحالات.

بينما يكون تجميع الملفات أكفأ عمومًا، فإن عيبه أن استرجاع الملفات يدويًا من المستودع أكثر صعوبة. وقد لا يكون مثاليًا للتخزين منزوع التكرار (deduplicated) لأن كل نسخة كاملة سترتب الملفات في الحزم بشكل مختلف. وأخيرًا، لا يمكن استئناف حزم الملفات، لذا احذر أن تضبط `repo-bundle-limit` على قيمة مرتفعة جدًا.

### التزايدي بالكتل {#block-incremental}

توفر النسخ الاحتياطية التزايدية بالكتل مساحة بتخزينها فقط الأجزاء المتغيرة من الملف منذ النسخة الاحتياطية السابقة بدلًا من تخزين الملف بأكمله.

تُمكَّن ميزة التزايدي بالكتل بالخيار `repo-block` وتعمل بأفضل حال عند تمكينها لجميع أنواع النسخ الاحتياطي. يجب أيضًا تمكين تجميع الملفات.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-block`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

### تعليقات النسخة الاحتياطية {#backup-annotations}

يمكن للمستخدمين إرفاق أزواج مفتاح/قيمة معلوماتية بالنسخة الاحتياطية. يمكن استخدام هذا الخيار عدة مرات لإرفاق تعليقات متعددة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة مع تعليقات

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

تُخرج التعليقات في المخرجات النصية للأمر `info` عند تحديد نسخة احتياطية بـ `--set` وتظهر دائمًا في مخرجات JSON.

pg-primary **⇒** الحصول على معلومات عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                key: value
                source: demo backup
```

يمكن إضافة التعليقات المرفقة بالأمر `backup` أو تعديلها أو إزالتها لاحقًا باستخدام الأمر `annotate`.

pg-primary **⇒** تغيير تعليقات النسخة الاحتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## الاحتفاظ {#retention}

من الأفضل عمومًا الاحتفاظ بأكبر عدد ممكن من النسخ الاحتياطية لتوفير نافذة أوسع لـ [الاستعادة إلى نقطة زمنية](#point-in-time-recovery)، لكن يجب أيضًا مراعاة الاعتبارات العملية مثل مساحة القرص. تزيل خيارات الاحتفاظ النسخ الاحتياطية الأقدم متى لم تعد ضرورية.

يجري pgBackRest تدوير النسخ الاحتياطية الكاملة بناءً على نوع الاحتفاظ الذي قد يكون عددًا أو فترة زمنية. عند تحديد عدد، فإن انتهاء الصلاحية لا يعني متى أُنشئت النسخ الاحتياطية بل كم منها يجب الاحتفاظ به. النسخ الاحتياطية التفاضلية قائمة على العدد لكنها ستنتهي صلاحيتها دائمًا عند انتهاء صلاحية النسخة الكاملة التي تعتمد عليها. لا تنتهي صلاحية النسخ التزايدية بواسطة الاحتفاظ بشكل مستقل — بل تنتهي دائمًا مع النسخة الكاملة أو التفاضلية المرتبطة بها. راجع قسمي [الاحتفاظ بالنسخ الكاملة](#full-backup-retention) و[الاحتفاظ بالنسخ التفاضلية](#differential-backup-retention) للتفاصيل والأمثلة.

يُحتفظ بـ WAL المؤرشف افتراضيًا للنسخ الاحتياطية التي لم تنتهِ صلاحيتها، ومع ذلك، رغم عدم التوصية بذلك، يمكن تعديل هذا الجدول لكل مستودع بخيارات retention-archive. راجع قسم [الاحتفاظ بالأرشيف](#archive-retention) للتفاصيل والأمثلة.

يُشغَّل الأمر `expire` تلقائيًا بعد كل نسخة احتياطية ناجحة ويمكن للمستخدم تشغيله أيضًا. عند تشغيله من المستخدم، سيحدث انتهاء الصلاحية كما تحدده إعدادات الاحتفاظ لكل مستودع مهيأ. إذا قُدّم الخيار `--repo` فسيحدث انتهاء الصلاحية على المستودع المحدد فقط. يمكن للمستخدم أيضًا قصر انتهاء الصلاحية على مجموعة نسخ احتياطية محددة بالخيار `--set`، وما لم يُحدد الخيار `--repo`، فسيُبحث في جميع المستودعات وستنتهي صلاحية أي نسخة تطابق معايير المجموعة. تجدر الإشارة إلى أن جدول الاحتفاظ بالأرشيف سيُفحص ويُنفَّذ في كل مرة يُشغَّل فيها الأمر `expire`.

### الاحتفاظ بالنسخ الكاملة {#full-backup-retention}

يحدد `repo1-retention-full-type` كيفية تفسير الخيار `repo1-retention-full`؛ إما كعدد النسخ الكاملة المطلوب الاحتفاظ بها أو عدد أيام الاحتفاظ بالنسخ الكاملة. يجب اكتمال نسخ احتياطية جديدة قبل حدوث انتهاء الصلاحية — أي أنه إذا كان `repo1-retention-full-type=count` و`repo1-retention-full=2` فستُخزن ثلاث نسخ كاملة قبل انتهاء صلاحية الأقدم منها، أو إذا كان `repo1-retention-full-type=time` و`repo1-retention-full=20` فيجب وجود نسخة كاملة واحدة عمرها 20 يومًا على الأقل قبل أن يمكن حدوث انتهاء الصلاحية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-full`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

النسخ الاحتياطي وفق `repo1-retention-full=2` لكن لا توجد حاليًا سوى نسخة كاملة واحدة لذا فإن النسخ الكامل التالي الذي سيُجرى لن يُنهِ صلاحية أي نسخة كاملة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 963 lines of output]
P00   INFO: repo1: remove expired backup 20261002-185706F
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185708F, start = 000000020000000000000008
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

*تنتهي* صلاحية الأرشيف لأن مقاطع WAL وُلدت قبل النسخة الاحتياطية الأقدم. هذه غير مفيدة للاستعادة — فقط مقاطع WAL المولدة بعد نسخة احتياطية يمكن استخدامها لاستعادة تلك النسخة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-185708F
P00   INFO: repo1: remove expired backup 20261002-185708F
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000008, stop = 000000020000000000000009
P00   INFO: expire command end: completed successfully
```

انتهت صلاحية النسخة الكاملة `20261002-185647F` وأصبح الاحتفاظ بالأرشيف مبنيًا على `20261002-185711F` التي هي الآن النسخة الكاملة الأقدم.

### الاحتفاظ بالنسخ التفاضلية {#differential-backup-retention}

اضبط `repo1-retention-diff` على عدد النسخ الاحتياطية التفاضلية المطلوب. تعتمد النسخ التفاضلية فقط على النسخة الكاملة السابقة لذا يمكن إنشاء مجموعة "متدحرجة" من النسخ التفاضلية لآخر يوم أو أكثر. هذا يسمح باستعادات سريعة إلى نقاط زمنية حديثة لكنه يقلل الاستهلاك الكلي للمساحة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=1

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

النسخ الاحتياطي وفق `repo1-retention-diff=1` لذا سيلزم إجراء نسختين تفاضليتين قبل انتهاء صلاحية إحداهما. تُضاف نسخة احتياطية تزايدية لعرض انتهاء صلاحية التزايدية، والتي تعتمد في هذه الحالة على انتهاء صلاحية التفاضلية.

pg-primary **⇒** إجراء نسخ احتياطية تفاضلية وتزايدية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

الآن سيؤدي إجراء نسخة احتياطية تفاضلية إلى إنهاء صلاحية النسختين التفاضلية والتزايدية السابقتين فلا تبقى سوى نسخة تفاضلية واحدة.

pg-primary **⇒** إجراء نسخة احتياطية تفاضلية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=2641-6abf9293 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-185713F_20261002-185715D, 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185715D
P00   INFO: expire command end: completed successfully
```

### الاحتفاظ بالأرشيف {#archive-retention}

مع أن pgBackRest يزيل مقاطع WAL المؤرشفة تلقائيًا عند إنهاء صلاحية النسخ الاحتياطية (الافتراضي يُنهي صلاحية WAL للنسخ الكاملة بناءً على خيار `repo1-retention-full`)، فقد يكون من المفيد إنهاء صلاحية الأرشيف بشكل أكثر عدوانية لتوفير مساحة القرص. لاحظ أن النسخ الكاملة تُعامل معاملة النسخ التفاضلية لأغراض الاحتفاظ التفاضلي بالأرشيف.

لن يزيل إنهاء صلاحية الأرشيف أبدًا مقاطع WAL المطلوبة لجعل نسخة احتياطية متسقة. لكن، بما أن الاستعادة إلى نقطة زمنية (PITR) تعمل فقط على تدفق WAL متصل، فيجب توخي الحذر عند إنهاء صلاحية الأرشيف عدوانيًا خارج عملية انتهاء صلاحية النسخ الاحتياطي المعتادة. لتحديد ما ستنتهي صلاحيته دون إنهاء صلاحية أي شيء فعليًا، يمكن تمرير خيار `dry-run` في سطر الأوامر مع الأمر `expire`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

pg-primary **⇒** إجراء نسخة احتياطية تفاضلية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261002-185713F_20261002-185719D
P00   INFO: diff backup size = 11.5KB, file total = 951
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** إنهاء صلاحية الأرشيف

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=2877-3548ad61 --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185711F, start = 00000002000000000000000A, stop = 00000002000000000000000B
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185717D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185719D, start = 000000020000000000000016
P00   INFO: repo1: 14-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

تملك النسخة الاحتياطية التفاضلية `20261002-185713F_20261002-185717D` مقاطع WAL مؤرشفة يجب الاحتفاظ بها لجعل النسخ الاحتياطية الأقدم متسقة رغم أنها لا يمكن تشغيلها للأمام أكثر مع PITR. تُزال مقاطع WAL المولدة بعد `20261002-185713F_20261002-185717D` لكن قبل `20261002-185713F_20261002-185719D`. تبقى مقاطع WAL المولدة بعد النسخة الاحتياطية الجديدة `20261002-185713F_20261002-185719D` ويمكن استخدامها لـ PITR.

بما أن النسخ الكاملة تُعد نسخًا تفاضلية لأغراض الاحتفاظ التفاضلي بالأرشيف، فإذا أُجريت الآن نسخة كاملة بالإعدادات نفسها، فلن يُحتفظ بالأرشيف إلا لتلك النسخة الكاملة لأغراض PITR.

--------

## الاستعادة {#restore-1}

يعود الأمر restore افتراضيًا تلقائيًا إلى اختيار أحدث نسخة احتياطية من أول مستودع توجد فيه نسخ احتياطية (راجع [البداية السريعة - استعادة نسخة احتياطية](#restore-a-backup)). الترتيب الذي تُفحص به المستودعات يفرضه `pgbackrest.conf` (مثلًا سيُفحص repo1 قبل repo2). للاختيار من مستودع محدد، يمكن تمرير الخيار `--repo` (مثل `--repo=1`). يمكن تمرير الخيار `--set` إذا رغبت في نسخة احتياطية غير الأحدث.

عند تحديد PITR بنوع `--type=time` أو `--type=lsn`، يجب تزويد الوقت أو LSN المستهدف بالخيار `--target`. إذا لم يُحدد `--set`، تُفحص المستودعات المهيأة بالترتيب بحثًا عن نسخة احتياطية وقت توقفها قبل الوقت المستهدف، أو LSN توقفها أقل من أو يساوي LSN المستهدف. إذا لم تُوجد أي نسخة مطابقة، يرفع pgBackRest خطأً لكل من `--type=time` و`--type=lsn`؛ فهو لا يرجع إلى أحدث نسخة احتياطية. لأنواع PITR الأخرى، مثل `xid`، يجب تزويد الخيار `--set` إذا كان الهدف قبل أحدث نسخة احتياطية. راجع [الاستعادة إلى نقطة زمنية](#point-in-time-recovery) لمزيد من التفاصيل والأمثلة.

لا تُضم خانات النسخ المتماثل (replication slots) بناءً على توصية PostgreSQL. راجع [أخذ نسخة احتياطية من دليل البيانات](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) في وثائق PostgreSQL لمزيد من المعلومات.

تقدم الأقسام التالية ميزات إضافية للأمر `restore`.

### ملكية الملفات {#file-ownership}

إذا شُغِّل `restore` بمستخدم غير root (وهو السيناريو المعتاد) فستكون ملكية جميع الملفات المستعادة للمستخدم/المجموعة التي تنفذ pgBackRest. إذا لم تكن ملكية الملفات الموجودة للمستخدم/المجموعة المنفذة فستكون النتيجة خطأً إذا تعذر تحديث الملكية إلى المستخدم/المجموعة المنفذة. في هذه الحالة سيلزم أن يقوم مستخدم ذو صلاحيات كافية بتحديث ملكية الملفات قبل إعادة محاولة الاستعادة.

إذا شُغِّل `restore` بالمستخدم `root` فسيحاول pgBackRest إعادة إنشاء الملكية المسجلة في البيان عند إجراء النسخة الاحتياطية. لا تُخزن في البيان سوى **أسماء** المستخدم/المجموعة لذا يجب وجود الأسماء نفسها على مضيف الاستعادة لكي يعمل هذا. إذا تعذر إيجاد اسم المستخدم/المجموعة محليًا فسيُستخدم مستخدم/مجموعة دليل بيانات PostgreSQL وأخيرًا `root` إذا تعذر ربط مستخدم/مجموعة دليل البيانات باسم.

### خيار delta {#delta-option}

تطلبت [استعادة نسخة احتياطية](#restore-a-backup) في [البداية السريعة](#quick-start) تنظيف دليل عنقود قاعدة البيانات قبل إجراء `restore`. يتيح خيار `delta` لـ pgBackRest تحديد الملفات في دليل عنقود قاعدة البيانات التي يمكن الحفاظ عليها والتي تحتاج إلى استعادة من النسخة الاحتياطية تلقائيًا — كما أنه *يزيل* الملفات غير الموجودة في بيان النسخة الاحتياطية لذا سيتخلص من التغييرات المتشعبة. يتم ذلك بحساب بصمة تشفيرية [SHA-1](https://en.wikipedia.org/wiki/SHA-1) لكل ملف في دليل عنقود قاعدة البيانات. إذا لم تطابق بصمة `SHA-1` البصمة المخزنة في النسخة الاحتياطية فسيُستعاد ذلك الملف. هذه العملية فعالة جدًا عند دمجها مع خيار `process-max`. وبما أن خادم PostgreSQL متوقف أثناء الاستعادة، يمكن استخدام عدد أكبر من العمليات مما قد يكون مرغوبًا فيه أثناء النسخ الاحتياطي عندما يكون خادم PostgreSQL قيد التشغيل.

pg-primary **⇒** إيقاف عنقود العرض التوضيحي وإجراء استعادة دلتا

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/pgsql/14/data' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/base/13755/pg_internal.init'
       [filtered 996 lines of output]
```

pg-primary **⇒** إعادة تشغيل PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

### استعادة قواعد بيانات محددة {#restore-selected-databases}

قد تكون هناك حالات يُستحسن فيها استعادة قواعد بيانات محددة بشكل انتقائي من نسخة احتياطية للعنقود. قد يكون ذلك لأسباب تتعلق بالأداء أو لنقل قواعد بيانات مختارة إلى جهاز لا توجد لديه مساحة كافية لاستعادة نسخة العنقود بأكملها.

لعرض هذه الميزة تُنشأ قاعدتا بيانات: test1 وtest2.

pg-primary **⇒** إنشاء قاعدتي بيانات للاختبار

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

ستُزوَّد كل قاعدة بيانات اختبار بجداول وبيانات لإثبات أن الاستعادة تعمل مع الاستعادة الانتقائية.

pg-primary **⇒** إنشاء جدول اختباري في كل قاعدة بيانات

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

تُجرى نسخة احتياطية جديدة ليعلم pgBackRest بقواعد البيانات الجديدة.

pg-primary **⇒** إجراء نسخة احتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

أحد الأسباب الرئيسية لاستخدام الاستعادة الانتقائية هو توفير المساحة. يُعرض هنا حجم قاعدة البيانات test1 ليمكن مقارنته باستخدام القرص بعد استعادة انتقائية.

pg-primary **⇒** إظهار المساحة التي تستخدمها قاعدة البيانات test1

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.4M	/var/lib/pgsql/14/data/base/32768
```

إذا لم تكن قاعدة البيانات المطلوب استعادتها معروفة، استخدم خيار `set` للأمر `info` لاكتشاف قواعد البيانات التي هي جزء من مجموعة النسخ الاحتياطي.

pg-primary **⇒** إظهار قائمة قواعد البيانات للنسخة الاحتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-185713F_20261002-185728I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 2.1MB
            backup reference list: 20261002-185713F, 20261002-185713F_20261002-185719D
            database list: postgres (13755), test1 (32768), test2 (32769)
```

أوقف العنقود واستعد قاعدة البيانات test2 فقط. قواعد البيانات المدمجة (`template0` و`template1` و`postgres`) تُستعاد دائمًا.

تحذير:

قد تُخطئ الاستعادة ما لم يُحدد `--type=immediate`. هذا لأن PostgreSQL بعد بلوغ الاتساق سيعلّم الصفحات المصفرة أخطاءً حتى مع الكتابة الكاملة للصفحة. في PostgreSQL ≥ 13 يمكن استخدام إعداد ignore_invalid_pages لتجاهل الصفحات غير الصالحة. في هذه الحالة من المهم فحص السجلات بعد الاستعادة لضمان عدم الإبلاغ عن أي صفحات غير صالحة في قواعد البيانات المختارة.

pg-primary **⇒** الاستعادة من آخر نسخة احتياطية مع تضمين قاعدة البيانات test2 فقط

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo systemctl start postgresql-14.service
```

بمجرد اكتمال الاستعادة ستحتوي قاعدة البيانات test2 على جميع الجداول والبيانات التي أُنشئت سابقًا.

pg-primary **⇒** إثبات أن قاعدة البيانات test2 قد استُعيدت

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

قاعدة البيانات test1، رغم نجاح الاستعادة، غير متاحة. هذا لأن قاعدة البيانات بأكملها استُعيدت كملفات متناثرة (sparse) مملوءة بالأصفار. يستطيع PostgreSQL تطبيق WAL على الملفات المصفرة بنجاح لكن قاعدة البيانات ككل لن تكون صالحة لأن الملفات الأساسية لا تحتوي على بيانات. هذا مقصود لمنع استخدام قاعدة البيانات عرضًا عندما قد تحتوي على بيانات جزئية طُبقت أثناء إعادة تشغيل WAL.

pg-primary **⇒** محاولة الاتصال بقاعدة البيانات test1 ستنتج خطأً

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

بما أن قاعدة البيانات test1 استُعيدت بملفات متناثرة (sparse) مملوءة بالأصفار فلن تتطلب سوى مساحة بقدر كمية WAL التي تُكتب أثناء الاستعادة. وبينما يمكن أن تكون كمية WAL المولدة أثناء النسخ الاحتياطي والمطبقة أثناء الاستعادة كبيرة، ستكون عمومًا جزءًا صغيرًا من الحجم الكلي لقاعدة البيانات، خاصة للقواعد الكبيرة التي يُرجح أن تكون هذه الميزة أنفع لها.

من الواضح أن قاعدة البيانات test1 تستخدم مساحة قرص أقل بكثير أثناء الاستعادة الانتقائية مما كانت ستستخدمه لو استُعيدت قاعدة البيانات بأكملها.

pg-primary **⇒** إظهار المساحة التي تستخدمها قاعدة البيانات test1 بعد الاستعادة

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.0K	/var/lib/pgsql/14/data/base/32768
```

في هذه المرحلة الإجراء الوحيد الممكن على قاعدة البيانات test1 غير الصالحة هو `drop database`. لا يحذف pgBackRest قاعدة البيانات تلقائيًا لأن ذلك لا يمكن إلا بعد اكتمال الاستعادة وإتاحة العنقود.

pg-primary **⇒** حذف قاعدة البيانات test1

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

الآن بعد حذف قاعدة البيانات test1 غير الصالحة لا تبقى سوى قاعدة البيانات test2 وقواعد البيانات المدمجة.

pg-primary **⇒** سرد قواعد البيانات المتبقية

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
 13754 | template0
 13755 | postgres
 32769 | test2
(4 rows)
```

--------

## الاستعادة إلى نقطة زمنية {#point-in-time-recovery}

أجرت [استعادة نسخة احتياطية](#restore-a-backup) في [البداية السريعة](#quick-start) استعادة افتراضية، وهي التشغيل حتى نهاية تدفق WAL. في حالة الفشل العتادي هذا عادة الخيار الأفضل، لكن لسيناريوهات إتلاف البيانات (سواء أكان مصدرها الإنسان أم الآلة) غالبًا ما تكون الاستعادة إلى نقطة زمنية (PITR) أنسب.

تتيح الاستعادة إلى نقطة زمنية (PITR) تشغيل WAL من نسخة احتياطية إلى lsn محدد أو وقت محدد أو معرف معاملة أو نقطة استعادة. لسيناريوهات الاستعادة الشائعة يمكن القول إن الاستعادة القائمة على الوقت هي الأكثر فائدة. سيناريو نموذجي للاستعادة هو استعادة جدول أُسقط عرضًا أو بيانات حُذفت عرضًا. استعادة جدول مسقط أكثر إثارة لذلك هو المثال المعطى هنا، لكن البيانات المحذوفة ستُستعاد بالطريقة نفسها تمامًا.

pg-primary **⇒** إنشاء جدول ببيانات مهمة جدًا

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

من المهم تمثيل الوقت كما يحسبه PostgreSQL وتضمين انزياحات المنطقة الزمنية. هذا يقلل احتمال تحويلات مناطق زمنية غير مقصودة ونتيجة استعادة غير متوقعة.

pg-primary **⇒** الحصول على الوقت من PostgreSQL

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 18:57:39.575732+00
```

الآن بعد تسجيل الوقت يُسقط الجدول. في الممارسة إيجاد الوقت الدقيق الذي أُسقط فيه الجدول أصعب كثيرًا مما في هذا المثال. قد لا يكون إيجاد الوقت الدقيق ممكنًا، لكن قليلًا من العمل الاستقصائي ينبغي أن يقرّبك منه.

pg-primary **⇒** إسقاط الجدول المهم

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

إذا اختيرت النسخة الاحتياطية الخاطئة للاستعادة فستفشل الاستعادة إلى الهدف الزمني المطلوب. لعرض ذلك تُجرى نسخة احتياطية تزايدية جديدة غير موجود فيها `important_table`.

pg-primary **⇒** إجراء نسخة احتياطية تزايدية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-185713F_20261002-185741I
            timestamp start/stop: 2026-10-02 18:57:41+00 / 2026-10-02 18:57:42+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

لن تكون استعادة الجدول المفقود من هذه النسخة الاحتياطية ممكنة لأن PostgreSQL يستطيع التشغيل للأمام فقط لا للخلف.

pg-primary **⇒** محاولة الاستعادة من نسخة احتياطية غير صحيحة

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-185713F_20261002-185741I --target-timeline=current \
       --type=time "--target=2026-10-02 18:57:39.575732+00" --target-action=promote restore
sudo systemctl start postgresql-14.service
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 11 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000100 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.01 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 4045) exited with exit code 1
LOG:  terminating any other active server processes
LOG:  database system is shut down
```

طريقة موثوقة هي السماح لـ pgBackRest باختيار نسخة احتياطية قادرة على الاستعادة إلى الهدف الزمني تلقائيًا، أي نسخة احتياطية انتهت قبل الوقت المحدد.

ملاحظة:

لا يستطيع pgBackRest اختيار نسخة احتياطية تلقائيًا عندما يكون نوع الاستعادة `xid` أو `name`.

pg-primary **⇒** استعادة عنقود العرض التوضيحي إلى `2026-10-02 18:57:39.575732+00`

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 18:57:39.575732+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 18:57:39.575732+00'
recovery_target_action = 'promote'
```

ولّد pgBackRest إعدادات الاستعادة في `postgresql.auto.conf` ليتمكن PostgreSQL من البدء فورًا. ‏`%f` هي طريقة PostgreSQL لتحديد مقطع WAL الذي يحتاجه، و`%p` هو الموقع الذي يجب نسخه إليه. بمجرد أن ينهي PostgreSQL الاستعادة سيوجد الجدول مجددًا ويمكن الاستعلام عنه.

pg-primary **⇒** بدء PostgreSQL والتحقق من وجود الجدول المهم

```bash
sudo systemctl start postgresql-14.service
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

يحتوي سجل PostgreSQL أيضًا على معلومات قيمة. سيشير إلى الوقت والمعاملة التي توقفت عندها الاستعادة وأيضًا يعطي وقت آخر معاملة طُبقت.

pg-primary **⇒** فحص مخرجات سجل PostgreSQL

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 5 lines of output]
LOG:  database system was interrupted; last known up at 2026-10-02 18:57:28 UTC
LOG:  restored log file "00000004.history" from archive
LOG:  starting point-in-time recovery to 2026-10-02 18:57:39.575732+00
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
       [filtered 2 lines of output]
LOG:  consistent recovery state reached at 0/19000100
LOG:  database system is ready to accept read-only connections
LOG:  recovery stopping before commit of transaction 743, time 2026-10-02 18:57:40.904112+00
LOG:  redo done at 0/1901E6C0 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
LOG:  last completed transaction was at log time 2026-10-02 18:57:38.228184+00
LOG:  selected new timeline ID: 5
LOG:  archive recovery complete
LOG:  database system is ready to accept connections
```

--------

## حذف stanza {#delete-a-stanza}

يزيل الأمر `stanza-delete` البيانات الموجودة في المستودع المرتبطة بـ stanza.

تحذير:

استخدم هذا الأمر بحذر — سيزيل نهائيًا جميع النسخ الاحتياطية والأرشيفات من مستودع pgBackRest للـ stanza المحددة.

لحذف stanza:

- أوقف عنقود PostgreSQL المرتبط بالـ stanza (أو استخدم --force للتجاوز).
- شغّل الأمر `stop` على المضيف الذي سيُشغَّل عليه الأمر `stanza-delete`.
- شغّل الأمر `stanza-delete`.

بمجرد اكتمال الأمر بنجاح، تقع على عاتق المستخدم مسؤولية إزالة الـ stanza من جميع ملفات تهيئة pgBackRest و/أو متغيرات البيئة.

لا يمكن حذف stanza إلا من مستودع واحد في كل مرة. لحذف الـ stanza من مستودعات متعددة، كرر الأمر `stanza-delete` لكل مستودع مع تحديد الخيار `--repo`.

pg-primary **⇒** إيقاف عنقود PostgreSQL المطلوب إزالته

```bash
sudo systemctl stop postgresql-14.service
```

pg-primary **⇒** إيقاف pgBackRest للـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=4396-32c67a63 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** حذف الـ stanza من مستودع واحد

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=4428-6f4dadb2 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## المستودعات المتعددة {#multiple-repositories}

يمكن تهيئة مستودعات متعددة كما هو معروض في [دعم S3](#s3-compatible-object-store-support). من الفوائد المحتملة القدرة على امتلاك مستودع محلي للاستعادات السريعة ومستودع بعيد للتكرار.

بعض الأوامر، مثل [`stanza-create`](/ar/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/ar/pgbackrest/command/stanza-upgrade/)، ستعمل تلقائيًا مع جميع المستودعات المهيأة، بينما ستتطلب أوامر أخرى، مثل [`stanza-delete`](/ar/pgbackrest/command/stanza-delete/)، تحديد مستودع باستخدام خيار `repo`.

لاحظ أن خيار `repo` غير مطلوب عندما يكون `repo1` وحده مهيأ حفاظًا على التوافق الرجعي. لكن خيار `repo` *مطلوب* عندما يكون مستودع واحد مهيأ مثل `repo2`. هذا لمنع انكسار الأوامر إذا أُضيف مستودع جديد لاحقًا.

سيدفع الأمر `archive-push` دائمًا WAL إلى الأرشيف في جميع المستودعات المهيأة. عندما يتعذر الوصول إلى مستودع، سيبقى دفع WAL إلى المستودعات الأخرى. لكن لكي يعمل هذا بفعالية، يجب تمكين `archive-async=y`؛ وإلا فلن تتقدم المستودعات الأخرى على المستودع غير المتاح إلا بمقطع WAL واحد. لاحظ أيضًا أنه إذا تعذر دفع WAL إلى أي مستودع، فلن يزيله PostgreSQL من الدليل `pg_wal`، مما قد يتسبب في نفاد مساحة وحدة التخزين.

يجب جدولة النسخ الاحتياطية لكل مستودع على حدة. في كثير من الحالات هذا مرغوب لأن أنواع النسخ الاحتياطي والاحتفاظ ستختلف باختلاف المستودع. وبالمثل، يجب أن تحدد الاستعادات مستودعًا. عمومًا من الأفضل تحديد مستودع للاستعادات ذي زمن استجابة/تكلفة منخفضين حتى لو كان ذلك يعني وقت استعادة أطول. فقط اختبار الاستعادة يمكنه تحديد المستودع الذي سيكون أكفأ.

--------

## دعم مخزن الكائنات المتوافق مع Azure {#azure-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن كائنات متوافقة مع Azure. يجب إنشاء الحاوية المستخدمة لتخزين المستودع مسبقًا — لن يفعل pgBackRest ذلك تلقائيًا. يمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادةً وضعه في مسار فرعي حتى يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

تحذير:

لا تمكّن "hierarchical namespace" لأن هذا سيسبب أخطاء أثناء انتهاء الصلاحية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة Azure

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

start-fast=y



[global:archive-push]

compress-level=3
```

يمكن استخدام توقيعات الوصول المشترك بضبط خيار `repo2-azure-key-type` على `sas` وضبط خيار `repo2-azure-key` على رمز توقيع الوصول المشترك.

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

pg-primary **⇒** إنشاء الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=4635-4a99c6c0 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

وقت إنشاء الملفات في Azure بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).

pg-primary **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-185802F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## دعم مخزن الكائنات المتوافق مع S3 {#s3-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن كائنات متوافقة مع S3. يجب إنشاء الحاوية المستخدمة لتخزين المستودع مسبقًا — لن يفعل pgBackRest ذلك تلقائيًا. يمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادةً وضعه في مسار فرعي حتى يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة S3

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

start-fast=y



[global:archive-push]

compress-level=3
```

ملاحظة:

ستحتاج المنطقة (region) والنقطة الطرفية (endpoint) إلى تهيئة ليشيرا إلى مكان الحاوية. القيم المعطاة هنا هي لمنطقة `us-east-1`.

ينبغي إنشاء دور (role) لتشغيل pgBackRest وضبط صلاحيات الحاوية بأكبر قدر ممكن من التقييد. إذا كان الدور مرتبطًا بمثيل في AWS فسيسترد pgBackRest تلقائيًا اعتمادات مؤقتة عندما يكون `repo3-s3-key-type=auto`، ما يعني أن المفاتيح لا تحتاج إلى ضبط صريح في `/etc/pgbackrest/pgbackrest.conf`.

سيقيد نموذج سياسة Amazon S3 هذا جميع عمليات القراءة والكتابة بالحاوية ومسار المستودع.

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

pg-primary **⇒** إنشاء الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

وقت إنشاء الملفات في S3 بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).

pg-primary **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-185820F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## دعم SFTP {#sftp-support}

يدعم pgBackRest وضع المستودعات على مضيفات SFTP. نقل الملفات عبر SFTP بطيء نسبيًا لذا تستفيد الأوامر من زيادة `process-max` لموازاة نقل الملفات.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة SFTP

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

عند استخدام SFTP، إذا جُمِّع libssh2 مع OpenSSH فالخيار `repo4-sftp-public-key-file` اختياري.

pg-primary **⇒** توليد زوج مفاتيح SSH للنسخ الاحتياطي عبر SFTP

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/pgsql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/pgsql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** نسخ المفتاح العام للنسخ الاحتياطي عبر SFTP من pg-primary إلى sftp-server

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/pgsql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

pg-primary **⇒** إضافة بصمة sftp-server إلى ملف known_hosts لأن الافتراضي لـ `repo4-sftp-host-key-check-type` هو "strict"

```bash
ssh-keyscan -H sftp-server >> /var/lib/pgsql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** إنشاء الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-185837F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## دعم مخزن الكائنات المتوافق مع GCS {#gcs-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن كائنات متوافقة مع GCS. يجب إنشاء الحاوية المستخدمة لتخزين المستودع مسبقًا — لن يفعل pgBackRest ذلك تلقائيًا. يمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادةً وضعه في مسار فرعي حتى يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة GCS

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

repo5-gcs-bucket=demo-bucket

repo5-gcs-key=/etc/pgbackrest/gcs-key.json

repo5-path=/demo-repo

repo5-type=gcs

start-fast=y



[global:archive-push]

compress-level=3
```

عند التشغيل في GCE اضبط `repo5-gcs-key-type=auto` للمصادقة تلقائيًا باستخدام حساب خدمة المثيل.

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

وقت إنشاء الملفات في GCS بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).

--------

## الوقت المستهدف للمستودع {#target-time-for-repository}

يحدد الوقت المستهدف الوقت الذي تستخدمه الأوامر لقراءة مستودع على تخزين يدعم تعدد الإصدارات. هذا يسمح للأمر بقراءة المستودع كما كان عند نقطة زمنية من أجل استعادة بيانات حُذفت أو أُتلفت بخطأ بشري أو ببرمجيات خبيثة.

التخزين الذي يدعم تعدد الإصدارات مدعوم من S3 وGCS وAzure لكنه غير ممكّن افتراضيًا عمومًا. إضافة إلى تمكين الإصدارات، قد يكون من المفيد تمكين قفل الكائنات (object locking) لـ S3 والحذف الناعم (soft delete) لـ GCS أو Azure.

عند تحديد خيار `repo-target-time` فيجب أيضًا تزويد خيار `repo`. من المرجح ألا تدعم جميع أنواع المستودعات الإصدارات، وعمومًا من المنطقي استهداف مستودع واحد للاستعادة.

لاحظ أن المقارنات مع الطابع الزمني للتخزين هي <= للطابع الزمني المزود، وتُقتطع المللي ثواني من الطابع الزمني عند تزويده.

لعرض هذه الميزة تُحذف الـ stanza `demo` في مستودع S3.

pg-primary **⇒** حذف الـ stanza في مستودع S3

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

بمجرد حذف الـ stanza سيعرض الأمر `info` المستودع في حالة خطأ.

pg-primary **⇒** خطأ في info

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

لكن، بما أن التخزين يدعم تعدد الإصدارات، يمكن النظر إلى المستودع في وقت سابق لحذف الـ stanza. قد يكون إيجاد الوقت المستهدف صعبًا بحسب الموقف، لكن في هذه الحالة يمكن تحديد وقت حذف الـ stanza بفحص متى حُذف `backup.info`.

pg-primary **⇒** سرد إصدارات `backup.info` في الحاوية

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
-------------------------------------------------------------------------------------
|                                ListObjectVersions                                 |
+--------+------------------------------------+-------------------------------------+
| Action |             Modified               |               Object                |
+--------+------------------------------------+-------------------------------------+
|  PUT   |  2026-10-02T18:58:20.631000+00:00  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T18:58:33.900000+00:00  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T18:58:45.634000+00:00  |  demo-repo/backup/demo/backup.info  |
+--------+------------------------------------+-------------------------------------+
```

الآن يمكن تشغيل الأمر `info` بوقت مستهدف سيعرض المستودع كما كان قبل حذفه.

pg-primary **⇒** info مع وقت مستهدف

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 18:58:34+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (14): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-185820F
            timestamp start/stop: 2026-10-02 18:58:20+00 / 2026-10-02 18:58:33+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 4.2MB, backup size: 4.2MB
```

إذا عُرضت النسخة الاحتياطية المطلوبة بالأمر `info` فيمكن استعادتها باستخدام الوقت المستهدف نفسه.

pg-primary **⇒** الاستعادة بوقت مستهدف

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 18:58:34+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=5686-f718513c --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 18:58:34+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-185820F, recovery will start at 2026-10-02 18:58:20
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00   INFO: write updated /var/lib/pgsql/14/data/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo systemctl start postgresql-14.service
```

--------

## مضيف مستودع مخصص {#dedicated-repository-host}

التهيئة الموصوفة في [البداية السريعة](#quick-start) مناسبة للتثبيتات البسيطة، لكن في التهيئات المؤسسية يكون المألوف أكثر امتلاك مضيف مستودع مخصص تُخزن عليه النسخ الاحتياطية وملفات أرشيف WAL. هذا يفصل النسخ الاحتياطية وأرشيف WAL عن خادم قاعدة البيانات فتكون لأعطال مضيف قاعدة البيانات تأثير أقل. ويظل من الجيد استخدام برمجيات نسخ احتياطي تقليدية لأخذ نسخة احتياطية من مضيف المستودع.

على مضيفات PostgreSQL، يُشترط أن يكون `pg1-path` مسار عنقود PostgreSQL المحلي وألا يُهيأ أي `pg1-host`. عند تهيئة مضيف مستودع، يجب أن يملك ملف تهيئة pgbackrest خيار `pg-host` مهيأ للاتصال بالمضيفين الأساسي والاستعداد (إن وُجد). مضيف المستودع هو وحده الذي ينبغي أن تكون تهيئة pgbackrest فيه على دراية بأكثر من مضيف PostgreSQL واحد. الترتيب لا يهم، مثلًا يمكن أن يكون pg1-path/pg1-host وpg2-path/pg2-host للأساسي أو للاستعداد.

### التثبيت {#installation-1}

يُنشأ مضيف جديد باسم repository لتخزين النسخ الاحتياطية للعنقود.

ملاحظة:

يجب أن يتطابق إصدار pgBackRest المثبت على مضيف المستودع تطابقًا تامًا مع الإصدار المثبت على مضيف PostgreSQL.

يُنشأ المستخدم `pgbackrest` ليكون مالكًا لمستودع pgBackRest. يمكن لأي مستخدم أن يملك المستودع لكن من الأفضل عدم استخدام `postgres` (إن وُجد) تجنبًا للالتباس.

ملاحظة:

عند تثبيت pgBackRest من حزمة، قد تُوفر تهيئة logrotate مثل `/etc/logrotate.d/pgbackrest` تدير تدوير السجلات كمستخدم محدد عبر التوجيه `su` (مثل `su postgres postgres`). وبما أن الملفات في `/var/log/pgbackrest` يملكها المستخدم الذي يشغل pgBackRest (وهو هنا `pgbackrest`)، فيجب تحديث توجيه `su` ليطابق هذا المستخدم وإلا سيفشل logrotate بخطأ صلاحيات.

repository **⇒** إنشاء المستخدم `pgbackrest`

```bash
sudo groupadd pgbackrest
sudo adduser -gpgbackrest -n pgbackrest
```

يُفضَّل تثبيت pgBackRest من حزمة على البناء من المصدر. عند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. في هذه الحالة قد يلزم إنشاء الأدلة أو تحديث الصلاحيات يدويًا.

تتوفر حزم RHEL لـ pgBackRest على [yum.postgresql.org](http://yum.postgresql.org).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

repository **⇒** تثبيت التبعيات

```bash
sudo yum install postgresql-libs libssh2
```

repository **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والتهيئة وملف تهيئة.

repository **⇒** إنشاء ملف تهيئة pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

repository **⇒** إنشاء مستودع pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### التهيئة {#configuration}

يمكن لـ pgBackRest استخدام TLS مع شهادات العميل لتمكين الاتصال بين المضيفين. من الممكن أيضًا استخدام SSH، راجع [إعداد SSH](/ar/pgbackrest/user-guide/#setup-passwordless-ssh).

يتوقع pgBackRest أن تُولَّد شهادات العميل/الخادم بالطريقة نفسها التي تُولَّد بها في PostgreSQL. راجع [اتصالات TCP/IP الآمنة بـ TLS](https://www.postgresql.org/docs/current/ssl-tcp.html) لتعليمات مفصلة عن توليد الشهادات.

يجب تهيئة مضيف المستودع بمضيف/مستخدم pg-primary ومسار قاعدة البيانات. سيُهيأ الأساسي كـ `pg1` للسماح بإضافة خادم استعداد لاحقًا.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg1-host`/`pg1-host-user` و`pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

يجب تهيئة مضيف قاعدة البيانات بمضيف/مستخدم المستودع. الافتراضي لخيار `repo1-host-user` هو `pgbackrest`. إذا كان المستخدم `postgres` يجري الاستعادات على مضيف المستودع فمن الأفضل عدم السماح أيضًا للمستخدم `postgres` بإجراء النسخ الاحتياطي. لكن يمكن للمستخدم `postgres` قراءة المستودع مباشرة إذا كان في المجموعة نفسها التي ينتمي إليها المستخدم `pgbackrest`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-host`/`repo1-host-user`

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

يمكن الاطلاع على تهيئة PostgreSQL في قسم [تهيئة الأرشفة](#configure-archiving).

تُشغَّل الأوامر كما في تهيئة المضيف الواحد باستثناء أن بعض الأوامر مثل `backup` و`expire` تُشغَّل من مضيف المستودع بدلًا من مضيف قاعدة البيانات.

### إعداد خادم TLS {#setup-tls-server}

يجب تهيئة خادم pgBackRest TLS وبدء تشغيله على كل مضيف.

repository **⇒** إعداد خادم pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=pgbackrest
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

pg-primary **⇒** إعداد خادم pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### إنشاء stanza والتحقق منها {#create-and-check-stanza}

أنشئ الـ stanza في المستودع الجديد.

repository **⇒** إنشاء الـ stanza

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

تحقق من أن التهيئة صحيحة على مضيفي قاعدة البيانات والمستودع كليهما. مزيد من المعلومات عن الأمر `check` في [التحقق من التهيئة](#check-the-configuration).

pg-primary **⇒** التحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

repository **⇒** التحقق من التهيئة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### إجراء نسخة احتياطية {#perform-a-backup-1}

لأخذ نسخة احتياطية من عنقود PostgreSQL شغّل pgBackRest بالأمر `backup` على مضيف المستودع.

repository **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

بما أن مستودعًا جديدًا أُنشئ على مضيف المستودع، أُصدر التحذير عن تغير النسخة الاحتياطية التزايدية إلى نسخة كاملة.

### استعادة نسخة احتياطية {#restore-a-backup-1}

لإجراء استعادة لعنقود PostgreSQL شغّل pgBackRest بالأمر `restore` على مضيف قاعدة البيانات.

pg-primary **⇒** إيقاف عنقود العرض التوضيحي والاستعادة وإعادة تشغيل PostgreSQL

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo systemctl start postgresql-14.service
```

--------

## النسخ الاحتياطي / الاستعادة المتوازية {#parallel-backup--restore}

يقدم pgBackRest معالجة متوازية لتحسين أداء الضغط والنقل. يُضبط عدد العمليات المستخدمة لهذه الميزة بالخيار `--process-max`.

عمومًا من الأفضل عدم استخدام أكثر من 25% من وحدات المعالجة المتاحة للأمر `backup`. لا يلزم أن تعمل النسخ الاحتياطية بذلك الحد من السرعة ما دامت تُجرى بانتظام، وينبغي ألا تؤثر عملية النسخ الاحتياطي في أداء قاعدة البيانات إن أمكن على الإطلاق.

يستطيع أمر الاستعادة ويجب أن يستخدم جميع وحدات المعالجة المتاحة لأن العنقود PostgreSQL يكون متوقفًا أثناء الاستعادة ولا يوجد عمومًا عمل مهم آخر يجري على المضيف. إذا كان المضيف يحتوي على عناقيد متعددة فيجب أخذ ذلك في الحسبان عند ضبط توازي الاستعادة.

repository **⇒** إجراء نسخة احتياطية بعملية واحدة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest لاستخدام عمليات `backup` متعددة

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository **⇒** إجراء نسخة احتياطية بعمليات متعددة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** الحصول على معلومات النسخ الاحتياطي لعنقود العرض التوضيحي

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (14): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-185937F
            timestamp start/stop: 2026-10-02 18:59:37+00 / 2026-10-02 18:59:40+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB

        full backup: 20261002-185941F
            timestamp start/stop: 2026-10-02 18:59:41+00 / 2026-10-02 18:59:43+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB
```

ينبغي أن يتحسن أداء النسخة الاحتياطية الأخيرة باستخدام عمليات متعددة. للنسخ الاحتياطية الصغيرة جدًا قد لا يكون الفرق واضحًا جدًا، لكن مع زيادة حجم قاعدة البيانات ستزيد وفورات الوقت أيضًا.

--------

## البدء والإيقاف {#starting-and-stopping}

إذا رُقّي خادم استعداد لأغراض الاختبار، أو استُعيد عنقود اختبار من نسخة احتياطية إنتاجية، فمن الجيد منع تلك العناقيد من الكتابة إلى مستودعات pgBackRest. يمكن تحقيق ذلك بالأمر `stop`.

الأوامر التي تكتب ويحجبها `stop` هي: `archive-push` و`backup` و`expire` و`stanza-create` و`stanza-upgrade`. لاحظ أن `stanza-delete` استثناء من هذه القاعدة (راجع [حذف stanza](#delete-a-stanza) لمزيد من التفاصيل).

pg-primary **⇒** إيقاف أوامر الكتابة في pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

لن تعمل أوامر الكتابة الجديدة في pgBackRest بعد الآن.

repository **⇒** محاولة إجراء نسخة احتياطية

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

حدد الخيار `--force` لإنهاء أي أوامر كتابة pgBackRest قيد التشغيل حاليًا. يشمل ذلك archive-get غير المتزامن (وإن كان سيعمل مجددًا إذا طلبه PostgreSQL). إذا كان pgBackRest موقوفًا بالفعل فسيولّد الإيقاف مجددًا تحذيرًا.

pg-primary **⇒** إيقاف خدمات pgBackRest مجددًا

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

ابدأ أوامر كتابة pgBackRest مجددًا بالأمر `start`. أوامر الكتابة التي كانت قيد التنفيذ قبل الإيقاف لن تبدأ تلقائيًا مجددًا، لكنها الآن مسموح لها بالبدء.

pg-primary **⇒** بدء أوامر الكتابة في pgBackRest

```bash
sudo -u postgres pgbackrest start
```

من الممكن أيضًا إيقاف pgBackRest لـ stanza واحدة.

pg-primary **⇒** إيقاف أوامر الكتابة في pgBackRest للـ stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

لن تعمل أوامر الكتابة الجديدة في pgBackRest للـ stanza المحددة بعد الآن.

repository **⇒** محاولة إجراء نسخة احتياطية

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

يجب أيضًا تحديد الـ stanza عند بدء أوامر الكتابة في pgBackRest لـ stanza واحدة.

pg-primary **⇒** بدء أوامر الكتابة في pgBackRest للـ stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## النسخ المتماثل {#replication}

يتيح النسخ المتماثل إنشاء نسخ متعددة من عنقود PostgreSQL (تسمى خوادم الاستعداد) من أساسي واحد. خوادم الاستعداد مفيدة لموازنة عمليات القراءة ولتوفير التكرار في حال فشل المضيف الأساسي.

### التثبيت {#installation-2}

يُنشأ مضيف جديد باسم pg-standby لتشغيل خادم الاستعداد.

يُفضَّل تثبيت pgBackRest من حزمة على البناء من المصدر. عند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. في هذه الحالة قد يلزم إنشاء الأدلة أو تحديث الصلاحيات يدويًا.

تتوفر حزم RHEL لـ pgBackRest على [yum.postgresql.org](http://yum.postgresql.org).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-standby **⇒** تثبيت التبعيات

```bash
sudo yum install postgresql-libs libssh2
```

pg-standby **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والتهيئة وملف تهيئة.

pg-standby **⇒** إنشاء ملف تهيئة pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### الاستعداد الساخن {#hot-standby}

يجري خادم الاستعداد الساخن النسخ المتماثل باستخدام أرشيف WAL ويسمح باستعلامات القراءة فقط.

تهيئة pgBackRest شبيهة جدًا بتهيئة pg-primary باستثناء أن نوع الاستعادة `standby` سيُستخدم لإبقاء العنقود في وضع الاستعادة عند بلوغ نهاية تدفق WAL.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest على خادم الاستعداد

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-standby **⇒** إعداد خادم pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

أنشئ المسار حيث سيُستعاد PostgreSQL.

pg-standby **⇒** إنشاء مسار PostgreSQL

```bash
sudo -u postgres mkdir -p -m 700 /var/lib/pgsql/14/data
```

الآن يمكن إنشاء خادم الاستعداد بالأمر `restore`.

مهم:

إذا كان المقصود ترقية العنقود دون أن يصبح الأساسي الجديد (مثلًا لأغراض التقارير أو الاختبار)، استخدم `--archive-mode=off` أو اضبط archive_mode=off في `postgresql.conf` لتعطيل الأرشفة. إذا لم تُعطَّل الأرشفة فقد يُلوَّث المستودع بـ WAL يجعل الاستعادات أصعب.

pg-standby **⇒** استعادة عنقود العرض التوضيحي للاستعداد

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:04
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

هذه التهيئة تحسبًا لأن يُرقّى خادم الاستعداد إلى أساسي.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** تهيئة PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** بدء PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

يعطي سجل PostgreSQL معلومات قيمة عن الاستعادة. لاحظ خصوصًا أن العنقود دخل وضع الاستعداد وهو جاهز لقبول اتصالات القراءة فقط.

pg-standby **⇒** فحص مخرجات سجل PostgreSQL بحثًا عن رسائل سجل تشير إلى النجاح

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 4 lines of output]
LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
LOG:  database system was interrupted; last known up at 2026-10-02 18:59:41 UTC
LOG:  entering standby mode
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
       [filtered 3 lines of output]
```

طريقة سهلة لاختبار أن النسخ المتماثل مهيأ بشكل صحيح هي إنشاء جدول على pg-primary.

pg-primary **⇒** إنشاء جدول جديد على الأساسي

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

ثم الاستعلام عن الجدول نفسه على pg-standby.

pg-standby **⇒** الاستعلام عن الجدول الجديد على خادم الاستعداد

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

إذن ما الذي حدث؟ بما أن PostgreSQL يسحب مقاطع WAL من الأرشيف لإجراء النسخ المتماثل، لن تُرى التغييرات على خادم الاستعداد حتى يُدفع مقطع WAL الذي يحتوي تلك التغييرات من pg-primary.

يمكن فعل ذلك يدويًا باستدعاء `pg_switch_wal()` الذي يدفع مقطع WAL الحالي إلى الأرشيف (يُنشأ مقطع WAL جديد ليحتوي التغييرات اللاحقة).

pg-primary **⇒** استدعاء `pg_switch_wal()`

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/2601E7C0    | 2026-10-02 19:00:10.880013+00
(1 row)
```

الآن بعد تأخير قصير سيظهر الجدول على pg-standby.

pg-standby **⇒** الآن يوجد الجدول الجديد على خادم الاستعداد (قد يتطلب محاولات قليلة)

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:11.954843+00
(1 row)
```

تحقق من تهيئة خادم الاستعداد للوصول إلى المستودع.

pg-standby **⇒** التحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1250-e6a5e2d8 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### النسخ المتماثل بالبث {#streaming-replication}

بدلًا من الاعتماد كليًا على أرشيف WAL، يجري النسخ المتماثل بالبث اتصالًا مباشرًا بالأساسي ويطبق التغييرات فور حدوثها على الأساسي. هذا ينتج تأخرًا أقل بكثير بين الأساسي وخادم الاستعداد.

يتطلب النسخ المتماثل بالبث مستخدمًا يملك صلاحية النسخ المتماثل (replication).

pg-primary **⇒** إنشاء مستخدم النسخ المتماثل

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

يجب تحديث الملف `pg_hba.conf` للسماح لخادم الاستعداد بالاتصال كمستخدم النسخ المتماثل. احرص على استبدال عنوان IP أدناه بعنوان IP الفعلي لخادم pg-standby. ستكون هناك حاجة إلى إعادة تحميل بعد تعديل ملف `pg_hba.conf`.

pg-primary **⇒** إنشاء مدخلة `pg_hba.conf` لمستخدم النسخ المتماثل

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /var/lib/pgsql/14/data/pg_hba.conf'
sudo systemctl reload postgresql-14.service
```

يحتاج خادم الاستعداد إلى معرفة كيفية الاتصال بالأساسي لذا سيُهيأ إعداد primary_conninfo في pgBackRest.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** ضبط primary_conninfo

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

من الممكن تهيئة كلمة مرور في إعداد primary_conninfo لكن استخدام ملف `.pgpass` أكثر مرونة وأمانًا.

pg-standby **⇒** تهيئة كلمة مرور النسخ المتماثل في ملف `.pgpass`.

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/pgsql/.pgpass'
sudo -u postgres chmod 600 /var/lib/pgsql/.pgpass
```

الآن يمكن إنشاء خادم الاستعداد بالأمر `restore`.

pg-standby **⇒** إيقاف PostgreSQL واستعادة عنقود العرض التوضيحي للاستعداد

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:18
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

ملاحظة:

كُتب إعداد primary_conninfo في ملف `postgresql.auto.conf` لأنه هُيّئ كـ `recovery-option` في `pgbackrest.conf`. يمكن استخدام الخيار `--type=preserve` مع `restore` لإبقاء ملف `postgresql.auto.conf` القائم في مكانه إذا فُضِّل ذلك السلوك.

بشكل افتراضي يخزن RHEL ملف `postgresql.conf` في دليل بيانات PostgreSQL. ذلك يعني أن التغيير الذي أُجري على `postgresql.conf` استُبدل بآخر استعادة ويجب تمكين إعداد hot_standby مجددًا. حلول أخرى لهذه المشكلة هي تخزين ملف `postgresql.conf` في مكان آخر أو تمكين إعداد hot_standby على مضيف pg-primary حيث سيُهمَل.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** تمكين hot_standby

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

hot_standby = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** بدء PostgreSQL

```bash
sudo systemctl start postgresql-14.service
```

سيؤكد سجل PostgreSQL أن النسخ المتماثل بالبث قد بدأ.

pg-standby **⇒** فحص مخرجات سجل PostgreSQL بحثًا عن رسائل سجل تشير إلى النجاح

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 12 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "000000070000000000000026" from archive
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

الآن عند إنشاء جدول على pg-primary سيظهر على pg-standby سريعًا ودون الحاجة إلى استدعاء `pg_switch_wal()`.

pg-primary **⇒** إنشاء جدول جديد على الأساسي

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.428653+00
(1 row)
```

pg-standby **⇒** الاستعلام عن الجدول على خادم الاستعداد

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.605628+00
(1 row)
```

--------

## عدة stanzas {#multiple-stanzas}

يدعم pgBackRest عدة stanzas. الاستخدام الأكثر شيوعًا هو مشاركة مضيف مستودع بين عدة stanzas.

### التثبيت {#installation-3}

يُنشأ مضيف جديد باسم pg-alt لتشغيل الأساسي الجديد.

يُفضَّل تثبيت pgBackRest من حزمة على البناء من المصدر. عند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. في هذه الحالة قد يلزم إنشاء الأدلة أو تحديث الصلاحيات يدويًا.

تتوفر حزم RHEL لـ pgBackRest على [yum.postgresql.org](http://yum.postgresql.org).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-alt **⇒** تثبيت التبعيات

```bash
sudo yum install postgresql-libs libssh2
```

pg-alt **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والتهيئة وملف تهيئة.

pg-alt **⇒** إنشاء ملف تهيئة pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### التهيئة {#configuration-1}

تهيئة pgBackRest متطابقة تقريبًا مع تهيئة pg-primary باستثناء أن الـ stanza `demo-alt` ستُستخدم فتُخزن النسخ الاحتياطية والأرشيف في موقع منفصل.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest على الأساسي الجديد

```ini
[demo-alt]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo-alt

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg1-host`/`pg1-host-user` و`pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-alt **⇒** إعداد خادم pgBackRest

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### إعداد عنقود العرض التوضيحي {#setup-demo-cluster-1}

pg-alt **⇒** إنشاء عنقود العرض التوضيحي

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

pg-alt:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** تهيئة إعدادات PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-alt **⇒** بدء عنقود العرض التوضيحي

```bash
sudo systemctl restart postgresql-14.service
```

### إنشاء الـ stanza والتحقق من التهيئة {#create-the-stanza-and-check-configuration}

يجب تشغيل الأمر `stanza-create` لتهيئة الـ stanza. يُوصى بتشغيل الأمر `check` بعد `stanza-create` لضمان تهيئة الأرشفة والنسخ الاحتياطي بشكل صحيح.

pg-alt **⇒** إنشاء الـ stanza والتحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=929-571b66d7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=962-2cadc106 --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000001-5cb25be2e89d0324cc2a94cbc964295204118888.gz' on repo1
P00   INFO: check command end: completed successfully
```

إذا شُغِّل الأمر `check` من مضيف المستودع فستُفحص جميع الـ stanzas.

repository **⇒** التحقق من التهيئة لجميع الـ stanzas

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1384-3bcda35c --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/000000070000000000000027-b36b790bcf0b1a9f54bc84458117feb77853d452.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000002-c303ffb17f8a111070459593520aa35640317a38.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## الأرشفة غير المتزامنة {#asynchronous-archiving}

تُمكَّن الأرشفة غير المتزامنة بخيار `archive-async`. يمكّن هذا الخيار التشغيل غير المتزامن للأمرين `archive-push` و`archive-get` معًا.

مسار spool مطلوب. ستخزن الأوامر البيانات العابرة هنا، لكن كل أمر يعمل بشكل مختلف تمامًا لذا يوصف استخدام مسار spool بالتفصيل في كل قسم.

pg-primary **⇒** إنشاء دليل spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** إنشاء دليل spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

يجب تهيئة مسار spool وتمكين الأرشفة غير المتزامنة. تمنح الأرشفة غير المتزامنة تلقائيًا بعض الفائدة بتقليل عدد الاتصالات التي تُجرى بالتخزين البعيد، لكن ضبط `process-max` يمكن أن يحسن الأداء جذريًا بموازاة العمليات. احرص ألا تضبط `process-max` على قيمة مرتفعة جدًا لدرجة تؤثر في عمليات قاعدة البيانات العادية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار spool والأرشفة غير المتزامنة

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار spool والأرشفة غير المتزامنة

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

ملاحظة:

هُيّئ `process-max` باستخدام أقسام الأوامر حتى لا يُستخدم الخيار مع backup وrestore. هذا يسمح أيضًا بقيم مختلفة للأمرين `archive-push` و`archive-get`.

لأغراض العرض التوضيحي سيُكسر النسخ المتماثل بالبث لإجبار PostgreSQL على أخذ WAL باستخدام restore_command.

pg-primary **⇒** كسر النسخ المتماثل بالبث بتغيير كلمة مرور النسخ المتماثل

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** إعادة تشغيل خادم الاستعداد لقطع الاتصال

```bash
sudo systemctl restart postgresql-14.service
```

### الدفع إلى الأرشيف {#archive-push}

يزيح الأمر `archive-push` غير المتزامن أرشفة WAL إلى عملية منفصلة (أو عمليات متعددة) لتحسين الإنتاجية. يعمل بطريقة "النظر إلى الأمام" ليرى أي مقاطع WAL جاهزة للأرشفة تجاوزًا للطلب الذي يقدمه PostgreSQL حاليًا عبر `archive_command`. تُنقل مقاطع WAL إلى الأرشيف مباشرةً من الدليل `pg_xlog`/`pg_wal` ولا يُرجع `archive_command` النجاح إلا بعد تخزين مقطع WAL بأمان في الأرشيف.

يحمل مسار spool الحالة الحالية لأرشفة WAL. ملفات الحالة المكتوبة في دليل spool صفرية الطول عادةً وينبغي أن تستهلك قدرًا أدنى من المساحة (بضعة ميغابايت على الأكثر) وقليلًا جدًا من الإدخال/الإخراج. جميع المعلومات في هذا الدليل يمكن إعادة إنشائها لذا ليس من الضروري الحفاظ على دليل spool إذا نُقل العنقود إلى عتاد جديد.

مهم:

في التنفيذ الأصلي للأرشفة غير المتزامنة، كانت مقاطع WAL تُنسخ إلى دليل spool قبل الضغط والنقل. التنفيذ الجديد ينسخ WAL مباشرةً من الدليل `pg_xlog`. إذا استُخدمت الأرشفة غير المتزامنة في v1.12 أو قبلها، فاقرأ ملاحظات إصدار v1.13 بعناية قبل الترقية.

يمكن استخدام الملف `[stanza]-archive-push-async.log` لمراقبة نشاط العملية غير المتزامنة. طريقة جيدة لاختبار ذلك هي دفع عدد من مقاطع WAL بسرعة.

pg-primary **⇒** اختبار الأرشفة غير المتزامنة المتوازية

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=6864-e51531e7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/00000007000000000000002D-7addc4d9a1861c1b8b68300ea3a7db01fbe08ae2.gz' on repo1
P00   INFO: check command end: completed successfully
```

الآن سيحتوي ملف السجل على نشاط متواز غير متزامن.

pg-primary **⇒** فحص النتائج في السجل

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6828-6cf1b924 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6866-2a936d60 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully
```

### الجلب من الأرشيف {#archive-get}

يحافظ الأمر `archive-get` غير المتزامن على قائمة انتظار محلية لـ WAL لتحسين الإنتاجية. إذا لم يُوجد مقطع WAL في قائمة الانتظار فسيُجلب من المستودع مع ما يكفي من WAL المتتالية لملء قائمة الانتظار. الحجم الأقصى لقائمة الانتظار يحدده `archive-get-queue-max`. كلما كانت قائمة الانتظار أقل من نصف امتلائها سيُجلب المزيد من WAL لملئها.

التشغيل غير المتزامن أنفع ما يكون في البيئات التي تولد الكثير من WAL أو لديها اتصال عالي زمن الاستجابة بتخزين المستودع (أي S3 أو غيره من مخازن الكائنات). في حالة الاتصال عالي زمن الاستجابة قد تكون زيادة `process-max` فكرة جيدة.

يمكن استخدام الملف `[stanza]-archive-get-async.log` لمراقبة نشاط العملية غير المتزامنة.

pg-standby **⇒** فحص النتائج في السجل

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=1919-a90112cb --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P01 DETAIL: found 000000070000000000000024 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000025 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000027 in the repo1: 14-1 archive
P01 DETAIL: found 000000070000000000000026 in the repo1: 14-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 31 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=1976-2ef79408 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P01 DETAIL: found 000000070000000000000028 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000029 in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002A in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002B in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002D in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002C in the repo1: 14-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 14 lines of output]
```

pg-primary **⇒** إصلاح النسخ المتماثل بالبث بتغيير كلمة مرور النسخ المتماثل

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## النسخ الاحتياطي من خادم الاستعداد {#backup-from-a-standby}

يستطيع pgBackRest إجراء النسخ الاحتياطية على خادم استعداد بدلًا من الأساسي. تتطلب النسخ الاحتياطية من خادم الاستعداد تهيئة المضيف pg-standby وتمكين خيار `backup-standby`. إذا هُيّئ أكثر من خادم استعداد واحد فسيُستخدم لأخذ النسخة الاحتياطية أول خادم استعداد قيد التشغيل يُعثر عليه.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg2-host`/`pg2-host-user` و`pg2-path`

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

تُطلب قاعدتا البيانات الأساسية والاستعداد معًا لإجراء النسخ الاحتياطي، مع أن الغالبية العظمى من الملفات ستُنسخ من خادم الاستعداد لتقليل الحمل على الأساسي. يمكن تهيئة مضيفي قاعدة البيانات بأي ترتيب. سيحدد pgBackRest تلقائيًا أيهما الأساسي وأيهما الاستعداد.

repository **⇒** أخذ نسخة احتياطية من عنقود العرض التوضيحي من pg2

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/log/postgresql.log (10.9KB, 0.42%) checksum dbfa988289c2ff32dcd198f19455165722870b43
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/global/pg_control (8KB, 0.73%) checksum 0a793efbb7bb2e255bbb2bfac8f612bc943c7f31
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/pg_hba.conf (4.5KB, 0.90%) checksum cfa97af1dab1b130f0a921fa2d10d76fe0c5f630
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/current_logfiles (26B, 0.91%) checksum 78a9f5c10960f0d91fcd313937469824861795a2
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/pg_logical/replorigin_checkpoint (8B, 0.91%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1263 lines of output]
```

يُظهر هذا النسخ الاحتياطي التزايدي أن معظم الملفات تُنسخ من المضيف pg-standby وأن عددًا قليلًا فقط يُنسخ من المضيف pg-primary.

ينشئ pgBackRest نسخة احتياطية لخادم استعداد متطابقة مع نسخة احتياطية أُجريت على الأساسي. يفعل ذلك ببدء/إيقاف النسخ الاحتياطي على المضيف pg-primary، ونسخ الملفات التي يشملها النسخ المتماثل فقط من المضيف pg-standby، ثم نسخ الملفات القليلة المتبقية من المضيف pg-primary. هذا يعني أن السجلات والإحصاءات من قاعدة البيانات الأساسية ستُضم إلى النسخة الاحتياطية.

--------

## ترقية PostgreSQL {#upgrading-postgresql}

فور ترقية PostgreSQL إلى إصدار رئيسي أحدث، يجب ضبط `pg-path` لجميع تهيئات pgBackRest على موقع قاعدة البيانات الجديد وتشغيل الأمر `stanza-upgrade`. إذا هُيّئ أكثر من مستودع واحد على المضيف فستُرقّى الـ stanza على كل منها. إذا كانت قاعدة البيانات غير متصلة فاستخدم الخيار `--no-online`.

التعليمات التالية ليست المقصود منها دليلًا شاملًا لترقية PostgreSQL، بل تحدد العملية العامة لترقية أساسي وخادم استعداد بقصد عرض الخطوات المطلوبة لإعادة تهيئة pgBackRest. يُوصى بأخذ نسخة احتياطية قبل الترقية.

pg-primary **⇒** إيقاف العنقود القديم

```bash
sudo systemctl stop postgresql-14.service
```

أوقف العنقود القديم على خادم الاستعداد لأنه سيُستعاد من العنقود المرقى حديثًا.

pg-standby **⇒** إيقاف العنقود القديم

```bash
sudo systemctl stop postgresql-14.service
```

أنشئ العنقود الجديد وأجرِ الترقية.

pg-primary **⇒** إنشاء عنقود جديد وإجراء الترقية

```bash
sudo -u postgres /usr/pgsql-15/bin/initdb \
       -D /var/lib/pgsql/15/data -k -A peer
sudo -u postgres sh -c 'cd /var/lib/pgsql && \
       /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir=/usr/pgsql-14/bin \
       --new-bindir=/usr/pgsql-15/bin \
       --old-datadir=/var/lib/pgsql/14/data \
       --new-datadir=/var/lib/pgsql/15/data \
       --old-options=" -c config_file=/var/lib/pgsql/14/data/postgresql.conf" \
       --new-options=" -c config_file=/var/lib/pgsql/15/data/postgresql.conf"'
```

```text
       [filtered 41 lines of output]
Checking for extension updates                              ok
Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

هيئ إعدادات العنقود الجديد ومنفذه.

pg-primary:`/var/lib/pgsql/15/data/postgresql.conf` **⇒** تهيئة PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

حدّث تهيئة pgBackRest على جميع الأنظمة لتشير إلى العنقود الجديد.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg1-path`

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg-path`

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg1-path` و`pg2-path` وتعطيل النسخ الاحتياطي من خادم الاستعداد

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-primary **⇒** نسخ تهيئة hba

```bash
sudo cp /var/lib/pgsql/14/data/pg_hba.conf \
       /var/lib/pgsql/15/data/pg_hba.conf
```

قبل بدء العنقود الجديد، يجب تشغيل الأمر `stanza-upgrade`.

pg-primary **⇒** ترقية الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=7454-62cfb155 --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/pgsql/15/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

ابدأ العنقود الجديد وتأكد من تثبيته بنجاح.

pg-primary **⇒** بدء العنقود الجديد

```bash
sudo systemctl start postgresql-15.service
```

اختبر التهيئة باستخدام الأمر `check`.

pg-primary **⇒** التحقق من التهيئة

```bash
sudo systemctl status postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

أزل العنقود القديم.

pg-primary **⇒** إزالة العنقود القديم

```bash
sudo rm -rf /var/lib/pgsql/14/data
```

ثبّت ملفات PostgreSQL الثنائية الجديدة على خادم الاستعداد وأنشئ العنقود.

pg-standby **⇒** إزالة العنقود القديم وإنشاء العنقود الجديد

```bash
sudo rm -rf /var/lib/pgsql/14/data
sudo -u postgres mkdir -p -m 700 /usr/pgsql-15/bin
```

شغّل `check` على مضيف المستودع. التحذير بشأن كون خادم الاستعداد متوقفًا متوقع لأن عنقود الاستعداد متوقف. تشغيل هذا الأمر يبين أن خادم المستودع على دراية بخادم الاستعداد ومهيأ بشكل صحيح للخادم الأساسي.

repository **⇒** التحقق من التهيئة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 tls protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

أجرِ نسخة احتياطية كاملة على العنقود الجديد ثم استعد خادم الاستعداد من النسخة الاحتياطية. سيتغير نوع النسخة الاحتياطية تلقائيًا إلى `full` إذا طُلب `incr` أو `diff`.

repository **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** استعادة عنقود العرض التوضيحي للاستعداد

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
```

pg-standby **⇒** بدء PostgreSQL والتحقق من تهيئة pgBackRest

```bash
sudo systemctl start postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

يمكن تمكين النسخ الاحتياطي من خادم الاستعداد الآن بعد أن استُعيد خادم الاستعداد.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** إعادة تمكين النسخ الاحتياطي من خادم الاستعداد

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```
