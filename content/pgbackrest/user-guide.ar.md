---
title: "دليل المستخدم (Debian/Ubuntu)"
linkTitle: "دليل المستخدم (Deb)"
weight: 20
description: "دليل خطوة بخطوة لإعداد pgBackRest واستخدامه على نظامي Debian وUbuntu."
icon: fa-brands fa-ubuntu
module: [PGBACKREST]
categories: [درس تعليمي]
upstream_link: "https://pgbackrest.org/user-guide.html"
---

--------

## مقدمة {#introduction}

يُقصد بهذا الدليل أن يُتابَع بالتسلسل من البداية إلى النهاية — فكل قسم يعتمد على القسم السابق له. فعلى سبيل المثال، يعتمد قسم [الاستعادة](#restore-1) على إعدادٍ يجري في قسم [البدء السريع](#quick-start). وبمجرد أن يصبح pgBackRest قيد التشغيل يصبح التنقل بين الأقسام ممكنًا، غير أن متابعة الدليل بترتيبه هي الموصى بها في القراءة الأولى.

مع أن الأمثلة في هذا الدليل موجهة إلى Debian/Ubuntu وPostgreSQL 17، فمن السهل إلى حدٍ ما تطبيق الأمثلة على أي توزيعة Unix وأي إصدار من PostgreSQL. الأوامر الوحيدة الخاصة بنظام التشغيل هي أوامر إنشاء عناقيد PostgreSQL وبدء تشغيلها وإيقافها وحذفها. وستكون أوامر pgBackRest نفسها على أي نظام Unix وإن كان موقع الملف التنفيذي قد يختلف. وبينما يسعى pgBackRest إلى العمل باتساق عبر إصدارات PostgreSQL، فهناك فروق دقيقة بين إصدارات PostgreSQL قد تظهر في هذا الدليل عند توضيح أمثلة معينة، مثل أسماء المسارات/الملفات والإعدادات الخاصة بـ PostgreSQL.

يمكن الاطلاع على معلومات الإعداد والتوثيق الخاص بـ PostgreSQL في [الدليل](http://www.postgresql.org/docs/17/static/index.html) الرسمي لـ PostgreSQL.

يتّبع هذا الدليل نهجًا جديدًا نوعًا ما في التوثيق. فكل أمر يُشغَّل على آلة افتراضية عند بناء التوثيق من المصدر بصيغة XML. وهذا يعني أنه يمكنك أن تثق ثقة عالية بأن الأوامر تعمل بشكل صحيح بالترتيب المعروض. ويُلتقط المخرَج ويُعرض أسفل الأمر عند الحاجة. وإذا لم يُضمَّن المخرَج فلأنه اعتُبر غير ذي صلة أو مشتتًا للسياق.

جميع الأوامر مخصصة للتشغيل باعتبار مستخدم عادي يتمتع بصلاحيات sudo لكلا المستخدمين `root` و`postgres`. ومن الممكن أيضًا تشغيل الأوامر مباشرة باعتبار مستخدميها المعنيين دون أي تعديل، وفي هذه الحالة يمكن الاستغناء عن أوامر `sudo`.


--------

## المفاهيم {#concepts}

تُعرَّف المفاهيم التالية كما هي ذات صلة بـ pgBackRest وPostgreSQL وهذا الدليل.


### النسخ الاحتياطي {#backup}

النسخة الاحتياطية هي نسخة متسقة من عنقود قاعدة بيانات يمكن استعادتها للتعافي من عطل عتادي، أو لإجراء الاستعادة إلى نقطة زمنية محددة (Point-In-Time Recovery)، أو لتشغيل استعداد جديد.

**النسخة الاحتياطية الكاملة**: ينسخ pgBackRest كامل محتويات عنقود قاعدة البيانات إلى النسخة الاحتياطية. النسخة الاحتياطية الأولى لعنقود قاعدة البيانات تكون دائمًا نسخة كاملة. ويستطيع pgBackRest دائمًا استعادة النسخة الكاملة استعادةً مباشرة. ولا تعتمد النسخة الاحتياطية الكاملة في اتساقها على أي ملفات خارجها.

**النسخة الاحتياطية التفاضلية**: ينسخ pgBackRest فقط ملفات عنقود قاعدة البيانات التي تغيّرت منذ آخر نسخة احتياطية كاملة. ويستعيد pgBackRest النسخة التفاضلية بنسخ جميع الملفات الموجودة في النسخة التفاضلية المختارة مع الملفات غير المتغيرة المناسبة من النسخة الكاملة السابقة. وميزة النسخة التفاضلية أنها تتطلب مساحة قرص أقل من النسخة الكاملة، غير أن النسخة التفاضلية والنسخة الكاملة يجب أن تكون كلتاهما صالحتين لاستعادة النسخة التفاضلية.

**النسخة الاحتياطية التزايدية**: ينسخ pgBackRest فقط ملفات عنقود قاعدة البيانات التي تغيّرت منذ آخر نسخة احتياطية (التي قد تكون نسخة تزايدية أخرى أو نسخة تفاضلية أو نسخة كاملة). ولأن النسخة التزايدية لا تتضمن سوى الملفات المتغيرة منذ النسخة الاحتياطية السابقة، فهي عمومًا أصغر بكثير من النسخ الكاملة أو التفاضلية. وكما هو الحال مع النسخة التفاضلية، تعتمد النسخة التزايدية في استعادتها على صلاحية نسخ احتياطية أخرى. فبما أن النسخة التزايدية لا تتضمن سوى الملفات منذ آخر نسخة احتياطية، فإن جميع النسخ التزايدية السابقة وصولًا إلى التفاضلية السابقة، والنسخة التفاضلية السابقة، والنسخة الكاملة السابقة يجب أن تكون جميعها صالحة لإجراء استعادة النسخة التزايدية. وإذا لم توجد نسخة تفاضلية فإن جميع النسخ التزايدية السابقة وصولًا إلى النسخة الكاملة السابقة — التي يجب أن تكون موجودة — والنسخة الكاملة نفسها يجب أن تكون صالحة لاستعادة النسخة التزايدية.


### الاستعادة {#restore}

الاستعادة هي عملية نسخ نسخة احتياطية إلى نظام سيُشغَّل فيه العنقود كعنقود قاعدة بيانات حي. وتتطلب الاستعادة ملفات النسخة الاحتياطية ومقطع WAL واحدًا أو أكثر لكي تعمل بشكل صحيح.


### سجل الكتابة المسبقة (WAL) {#write-ahead-log-wal}

WAL هو الآلية التي يستخدمها PostgreSQL لضمان عدم فقدان أي تغييرات مثبَّتة (committed). تُكتب المعاملات تسلسليًا إلى WAL وتُعد المعاملة مثبَّتة عندما تُدفع هذه الكتابات إلى القرص. وبعد ذلك تكتب عملية في الخلفية التغييرات إلى ملفات عنقود قاعدة البيانات الرئيسية (المعروف أيضًا بالكومة heap). وفي حال وقوع انهيار، يُعاد تشغيل WAL لإعادة قاعدة البيانات إلى حالة متسقة.

WAL غير محدود من الناحية المفاهيمية لكنه عمليًا مقسّم إلى ملفات منفردة بحجم 16MB تسمى المقاطع. وتتبع مقاطع WAL اصطلاح التسمية `0000000100000A1E000000FE` حيث تمثل أول 8 خانات سداسية عشرية الخط الزمني (timeline) وتمثل الخانات الـ 16 التالية الرقم التسلسلي المنطقي (LSN).


### التشفير {#encryption}

التشفير هو عملية تحويل البيانات إلى صيغة غير قابلة للتمييز ما لم تُقدَّم كلمة المرور المناسبة (ويشار إليها أيضًا بعبارة المرور).

سيشفّر pgBackRest المستودع استنادًا إلى كلمة مرور يوفرها المستخدم، وبذلك يمنع الوصول غير المصرح به إلى البيانات المخزنة داخل المستودع.


--------

## ترقية pgBackRest {#upgrading-pgbackrest}



### ترقية pgBackRest من الإصدار v2.x إلى v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

الترقية من v2.x إلى v2.y عملية مباشرة. لم تتغير صيغة المستودع، لذا فبالنسبة لمعظم التثبيتات لا يتعدى الأمر مجرد تثبيت الملفات التنفيذية للإصدار الجديد. ومن الممكن أيضًا الرجوع إلى إصدار أقدم إذا لم تكن قد استخدمت ميزات جديدة لا يدعمها الإصدار الأقدم.

هام:

يجب أن يتطابق إصدار pgBackRest المحلي مع البعيد تطابقًا تامًا، لذا ينبغي ترقيتهما معًا. وفي حال عدم التطابق، لن تعمل أرشفة WAL والنسخ الاحتياطي حتى يتطابق الإصداران. وفي هذه الحالة سيُبلَّغ عن الخطأ التالي: `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.


--------

## البناء {#build}

تثبيت pgBackRest من حزمة أفضل من البناء من المصدر. راجع [التثبيت](#installation) لمزيد من المعلومات عن الحزم.

عند البناء من المصدر من الأفضل استخدام مضيف مخصص للبناء بدلًا من البناء في بيئة الإنتاج. وكثير من الأدوات المطلوبة للبناء لا ينبغي عمومًا تثبيتها في بيئة الإنتاج. ويتألف pgBackRest من ملف تنفيذي واحد لذا يسهل نسخه إلى مضيف جديد بمجرد بنائه.

build **⇒** تنزيل الإصدار `2.59.3` من pgBackRest إلى المسار `/build`

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** تثبيت تبعيات البناء

```bash
sudo apt-get install python3-distutils meson gcc libpq-dev libssl-dev libxml2-dev \
       pkg-config liblz4-dev libzstd-dev libbz2-dev libz-dev libssh2-1-dev libsystemd-dev
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
1/1 smoke OK               11.07s


       [filtered 7 lines of output]
```

--------

## التثبيت {#installation}

يُنشأ مضيف جديد باسم pg-primary ليحتوي على العنقود التجريبي ولتشغيل أمثلة pgBackRest.

تثبيت pgBackRest من حزمة أفضل من البناء من المصدر. وعند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. وفي هذه الحالة قد يلزم إنشاء الأدلة يدويًا أو تحديث الصلاحيات.

تتوفر حزم Debian/Ubuntu الخاصة بـ pgBackRest عبر [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-primary **⇒** تثبيت التبعيات

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-primary **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والإعداد وملف إعداد.

pg-primary **⇒** إنشاء ملف إعداد pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

يفترض الآن أن pgBackRest مثبت بشكل صحيح لكن من الأفضل التحقق من ذلك. فإذا فاتت أية تبعية فستحصل على خطأ عند تشغيل pgBackRest من سطر الأوامر.

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

## البدء السريع {#quick-start}

سيغطي قسم البدء السريع التهيئة الأساسية لـ pgBackRest وPostgreSQL وسيقدّم الأوامر `backup` و`restore` و`info`.


### إعداد العنقود التجريبي {#setup-demo-cluster}

إنشاء العنقود التجريبي اختياري لكنه موصى به بشدة، خصوصًا للمستخدمين الجدد، لأن أوامر الأمثلة في دليل المستخدم تشير إلى العنقود التجريبي؛ وتفترض الأمثلة أن العنقود التجريبي يعمل على المنفذ الافتراضي (أي 5432). ولن يُشغَّل العنقود إلا في قسم لاحق لأنه ما زالت هناك بعض التهيئة الواجب إجراؤها.

pg-primary **⇒** إنشاء العنقود التجريبي

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 102:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

### تهيئة stanza العنقود {#configure-cluster-stanza}

الـ stanza هي تهيئة عنقود قاعدة بيانات PostgreSQL التي تحدد مكانه، وكيفية أخذ نسخه الاحتياطية، وخيارات الأرشفة، وغير ذلك. ستحتوي معظم خوادم قواعد البيانات على عنقود PostgreSQL واحد وبالتالي stanza واحدة، بينما تحتوي خوادم النسخ الاحتياطي على stanza لكل عنقود قاعدة بيانات يحتاج إلى نسخ احتياطي.

قد يغريك تسمية الـ stanza باسم العنقود الأساسي، لكن الاسم الأفضل هو ما يصف قواعد البيانات التي يحتويها العنقود. ولأن اسم الـ stanza سيُستخدم للأساسي وجميع النسخ المتماثلة، فمن الأنسب اختيار اسم يصف الوظيفة الفعلية للعنقود، مثل app أو dw، بدلًا من اسم العنقود المحلي، مثل main أو prod.

يصف الاسم 'demo' غرض هذا العنقود بدقة لذا سيكون اسمًا جيدًا للـ stanza أيضًا.

يحتاج pgBackRest إلى معرفة مكان الدليل الأساسي لبيانات عنقود PostgreSQL. يمكن طلب المسار من PostgreSQL مباشرة لكن في سيناريو الاستعادة لن تكون عملية PostgreSQL متاحة. وأثناء النسخ الاحتياطي تُقارن القيمة المقدمة إلى pgBackRest بالمسار الذي يعمل عليه PostgreSQL ويجب أن تتطابقا وإلا أعاد النسخ الاحتياطي خطأ. احرص على أن يساوي `pg-path` قيمة data_directory تمامًا كما يبلغ عنها PostgreSQL.

يخزن Debian/Ubuntu العناقيد افتراضيًا في `/var/lib/postgresql/[version]/[cluster]` لذا يسهل تحديد المسار الصحيح لدليل البيانات.

عند إنشاء الملف `/etc/pgbackrest/pgbackrest.conf`، يجب منح مالك قاعدة البيانات (وهو عادة `postgres`) صلاحيات القراءة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة دليل بيانات عنقود PostgreSQL

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo
```

تتبع ملفات إعداد pgBackRest اصطلاحًا يشبه ملفات INI في Windows. تُحدَّد الأقسام بنص بين أقواس مربعة ويحتوي كل قسم على أزواج المفتاح/القيمة. وتُهمل الأسطر التي تبدأ بـ `#` ويمكن استخدامها تعليقات، لكن التعليقات في نهاية السطر بعد قيمة على السطر نفسه غير مدعومة. وعلامات الاقتباس غير مدعومة وتُحذف الفراغات من المفاتيح والقيم. وتُدمج الأقسام إذا ظهرت أكثر من مرة.

هناك طرق متعددة لتحميل ملفات إعداد pgBackRest:

- `config` و`config-include-path` افتراضيان: سيُحمَّل ملف الإعداد الافتراضي إن وُجد، وستُلحق ملفات `*.conf` في مسار تضمين الإعداد الافتراضي إن وُجدت.
- تحديد الخيار `config`: سيُحمَّل ملف الإعداد المحدد وحده ويُتوقع وجوده.
- تحديد `config-include-path`: ستُحمَّل ملفات `*.conf` في مسار تضمين الإعداد ويكون وجود المسار مطلوبًا. وسيُحمَّل ملف الإعداد الافتراضي إن وُجد. وإذا رغبت في تحميل الملفات الموجودة في مسار تضمين الإعداد المحدد فقط فيمكن أيضًا تمرير الخيار `--no-config`.
- تحديد `config` و`config-include-path`: باستخدام القيم التي حددها المستخدم، سيُحمَّل ملف الإعداد وستُلحق ملفات `*.conf` في مسار تضمين الإعداد. ويُتوقع وجود الملفات.
- تحديد `config-path`: يتجاوز هذا الإعداد المسار الأساسي للموقع الافتراضي لملف الإعداد و/أو المسار الأساسي لإعداد config-include-path الافتراضي ما لم يُضبط خيار config و/أو config-include-path صراحةً.

تُسلسَل الملفات كما لو كانت ملفًا واحدًا كبيرًا ويجب أن يكون كل ملف صالحًا بذاته. وهذا يعني أن الأقسام يجب تحديدها في كل ملف حيث يلزم تخزين مفتاح/قيمة. الترتيب لا يهم لكن هناك أسبقية قائمة على الأقسام. والأسبقية (من الأعلى إلى الأدنى) هي:

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

ملاحظة:

الخيارات `--config` و`--config-include-path` و`--config-path` خيارات لسطر الأوامر فقط.

يمكن أيضًا تهيئة pgBackRest باستخدام متغيرات البيئة (المثال أدناه)؛ وتنطبق هذه المتغيرات على أوامر مثل [backup](/ar/pgbackrest/command/backup/) و[restore](/ar/pgbackrest/command/restore/) و[archive-push](/ar/pgbackrest/command/archive-push/).

pg-primary **⇒** تهيئة `log-path` باستخدام متغيرات البيئة

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

قد يصعب تقدير المساحة التي ستحتاجها مسبقًا. أفضل ما يمكن فعله هو أخذ بعض النسخ الاحتياطية ثم تسجيل حجم الأنواع المختلفة من النسخ (full/incr/diff) وقياس مقدار WAL المتولد يوميًا. سيمنحك هذا فكرة عامة عن المساحة التي ستحتاجها، مع أن المتطلبات ستتغير على الأرجح بمرور الوقت مع تطور قاعدة بياناتك بالطبع.

في هذا العرض التوضيحي سيُخزَّن المستودع على المضيف نفسه الذي يعمل عليه خادم PostgreSQL. وهذه أبسط تهيئة، وهي مفيدة في الحالات التي تُستخدم فيها برمجيات نسخ احتياطي تقليدية لأخذ نسخة احتياطية من مضيف قاعدة البيانات.

pg-primary **⇒** إنشاء مستودع pgBackRest

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

يجب تهيئة مسار المستودع لكي يعرف pgBackRest أين يجده.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار مستودع pgBackRest

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest
```

يمكن أيضًا تهيئة مستودعات متعددة. راجع [المستودعات المتعددة](#multiple-repositories) للتفاصيل.


### تهيئة الأرشفة {#configure-archiving}

يتطلب أخذ نسخة احتياطية من عنقود PostgreSQL قيد التشغيل تمكين أرشفة WAL. و`%p` هي الطريقة التي يحدد بها PostgreSQL موقع مقطع WAL المطلوب أرشفته. ولاحظ أنه سيُنشأ مقطع WAL واحد *على الأقل* أثناء عملية النسخ الاحتياطي حتى لو لم تُجرَ أي كتابات صريحة إلى العنقود.

pg-primary:`/etc/postgresql/17/demo/postgresql.conf` **⇒** تهيئة إعدادات الأرشفة

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

يجب إعادة تشغيل عنقود PostgreSQL بعد إجراء هذه التغييرات وقبل تنفيذ نسخ احتياطي.

pg-primary **⇒** إعادة تشغيل العنقود التجريبي

```bash
sudo pg_ctlcluster 17 demo restart
```

الإعداد `hot_standby` ممكَّن افتراضيًا وينبغي تركه على هذه الحالة في كل عنقود. فأي عنقود قد يُستعاد لاحقًا كاستعداد، مثل أساسي يُعاد بناؤه كاستعداد بعد تجاوز الأعطال، ولن يقبل الاستعداد اتصالات القراءة فقط بدونه.

عندما يُتوقع أن يستغرق وصول أرشفة مقطع WAL إلى مستودع pgBackRest أكثر من 60 ثانية (الافتراضي)، ينبغي زيادة خيار pgBackRest `archive-timeout`. ولاحظ أن هذا الخيار ليس نفسه خيار archive_timeout في PostgreSQL الذي يُستخدم لفرض تبديل مقطع WAL؛ وهو مفيد لقواعد البيانات التي تمر بها فترات خمول طويلة. لمزيد من المعلومات عن خيار archive_timeout في PostgreSQL راجع وثائق [سجل الكتابة المسبقة](https://www.postgresql.org/docs/current/static/runtime-config-wal.html) في PostgreSQL.

يمكن تهيئة الأمر `archive-push` بخيارات خاصة به. فعلى سبيل المثال، يمكن ضبط مستوى ضغط أدنى لتسريع الأرشفة دون التأثير في الضغط المستخدم للنسخ الاحتياطي.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `archive-push` لاستخدام مستوى ضغط أدنى

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

يمكن استخدام أسلوب التهيئة هذا مع أي أمر، بل ويمكن أن يستهدف stanza محددة، مثل `demo:archive-push`.


### تهيئة الاحتفاظ {#configure-retention}

ينهي pgBackRest صلاحية النسخ الاحتياطية استنادًا إلى خيارات الاحتفاظ.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة الاحتفاظ بنسختين احتياطيتين كاملتين

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

يمكن الاطلاع على مزيد من المعلومات عن الاحتفاظ في قسم [الاحتفاظ](#retention).


### تهيئة تشفير المستودع {#configure-repository-encryption}

سيُهيَّأ المستودع بنوع تشفير ومفتاح لعرض التشفير توضيحيًا. ويُنفَّذ التشفير دائمًا من جهة العميل حتى لو كان نوع المستودع (مثل S3 أو أي مخزن كائنات آخر) يدعم التشفير.

من المهم استخدام عبارة مرور طويلة وعشوائية لمفتاح التشفير. وطريقة جيدة لتوليد واحدة هي تشغيل: `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة تشفير مستودع pgBackRest

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

ملاحظة:

وُضعت إعدادات التشفير في القسم `[global]` أعلاه كي يستطيع الأمر `info` قراءة جميع الـ stanzas. فبدون الخيار `stanza` يقرأ الأمر `info` إعدادات التشفير من القسم `[global]` فقط، لذا فإن إعدادات التشفير المهيأة لكل stanza تتطلب الخيار `stanza` لقراءة stanza مشفرة.

بمجرد تهيئة المستودع وإنشاء الـ stanza والتحقق منها، لا يمكن تغيير إعدادات تشفير المستودع.


### إنشاء الـ stanza {#create-the-stanza}

يجب تشغيل الأمر `stanza-create` لتهيئة الـ stanza إنشائيًا. ويوصى بتشغيل الأمر `check` بعد `stanza-create` لضمان تهيئة الأرشفة والنسخ الاحتياطي بشكل صحيح.

pg-primary **⇒** إنشاء الـ stanza والتحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=415-9c2d1500 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### التحقق من التهيئة {#check-the-configuration}

يتحقق الأمر `check` من أن pgBackRest وإعداد archive_command مهيآن بشكل صحيح للأرشفة والنسخ الاحتياطي للـ stanza المحددة. وسيحاول التحقق من جميع المستودعات وقواعد البيانات المهيأة للمضيف الذي يُشغَّل عليه الأمر. وهو يكشف سوء التهيئة، لا سيما في الأرشفة، الذي ينتج عنه نسخ احتياطية غير مكتملة لأن مقاطع WAL المطلوبة لم تصل إلى الأرشيف. ويمكن تشغيل الأمر على مضيف PostgreSQL أو مضيف المستودع. ويمكن أيضًا تشغيله على مضيف الاستعداد، غير أنه ولأنه لا يمكن تنفيذ `pg_switch_xlog()`/`pg_switch_wal()` على الاستعداد، فسيختبر الأمر تهيئة المستودع فقط.

لاحظ أنه تُستدعى `pg_create_restore_point('pgBackRest Archive Check')` و`pg_switch_xlog()`/`pg_switch_wal()` لإجبار PostgreSQL على أرشفة مقطع WAL.

pg-primary **⇒** التحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=424-7270037b --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000100000000/000000010000000000000001-e8eb01b8d8aaf321d368dc8edf5b559247841eb1.gz' on repo1
P00   INFO: check command end: completed successfully
```

### ضبط الأداء {#performance-tuning}

يوفر pgBackRest عددًا من خيارات الأداء غير الممكَّنة افتراضيًا حفاظًا على التوافق مع الإصدارات السابقة في المستودع. غير أنه عند إنشاء مستودع جديد يوصى بالخيارات التالية. ويمكن أيضًا استخدامها على مستودع قائم مع التحفظ بأن إصدارات pgBackRest الأقدم لن تكون قادرة على قراءة المستودع. ويعتمد هذا التعارض على وقت إدخال الميزة كما هو مُشار إليه في القائمة أدناه.

- `compress-type` - يحدد خوارزمية الضغط التي يستخدمها الأمران `backup` و`archive-push`. الافتراضي هو `gz` (Gzip) لكن يوصى بـ `zst` (Zstandard) لأنه أسرع بكثير ويوفر ضغطًا مشابهًا لـ `gz`. ويُدعم `zst` في خيار `compress-type` منذ [v2.27](/ar/pgbackrest/release/#v227-release-notes). راجع [نوع الضغط](/ar/pgbackrest/configuration/#compress-type-option---compress-type) لمزيد من التفاصيل.
- `repo-bundle` - يجمع الملفات الصغيرة أثناء النسخ الاحتياطي لتوفير المساحة وتحسين سرعة الأمرين `backup` و`restore`، خصوصًا على مخازن الكائنات مثل S3. قُدِّم خيار `repo-bundle` في [v2.39](/ar/pgbackrest/release/#v239-release-notes). راجع [تجميع الملفات](#file-bundling) لمزيد من التفاصيل.
- `repo-block` - يخزن أثناء تنفيذ الأمر `backup` من نوع `diff`/`incr` الأجزاء المتغيرة من الملفات فقط بدلًا من الملف بأكمله. يوفر هذا المساحة ويرفع سرعة `backup`. قُدِّم خيار `repo-block` في [v2.46](/ar/pgbackrest/release/#v246-release-notes) لكن يوصى بـ [v2.52.1](/ar/pgbackrest/release/#v2521-release-notes) على الأقل. راجع [النسخ التزايدي بالكتل](#block-incremental) لمزيد من التفاصيل.

هناك خيارات أداء أخرى غير ممكَّنة افتراضيًا لأنها تتطلب تهيئة إضافية أو لأن القيمة الافتراضية آمنة (لكنها ليست مثالية). وتتوفر هذه الخيارات في جميع إصدارات v2 من pgBackRest.

- `process-max` - يحدد عدد العمليات التي ستُستخدم للأوامر. الافتراضي هو 1، وهو ما لا يكون مناسبًا تقريبًا أبدًا. ويستخدم كل أمر `process-max` بطريقة مختلفة فارجع إلى توثيق كل أمر لتفاصيل الاستخدام.
- `archive-async` - يؤرشف ملفات WAL إلى المستودع على شكل دفعات مما يزيد سرعة الأرشفة زيادة كبيرة. وهو غير ممكَّن افتراضيًا لأنه يتطلب إنشاء مسار spool. راجع [الأرشفة غير المتزامنة](#asynchronous-archiving) لمزيد من التفاصيل.
- `backup-standby` - ينفذ النسخ الاحتياطي على الاستعداد بدلًا من الأساسي لتقليل الحمل على الأساسي. وهو غير ممكَّن افتراضيًا لأنه يتطلب تهيئة إضافية ووجود مضيف استعداد واحد أو أكثر. راجع [النسخ الاحتياطي من الاستعداد](#backup-from-a-standby) لمزيد من التفاصيل.


### إجراء نسخة احتياطية {#perform-a-backup}

بشكل افتراضي سينتظر pgBackRest نقطة التحقق الدورية المجدولة التالية قبل بدء النسخ الاحتياطي. وبحسب إعدادَي checkpoint_timeout وcheckpoint_segments في PostgreSQL قد يمضي وقت غير قصير قبل اكتمال نقطة التحقق وبدء النسخ الاحتياطي. وعمومًا من الأفضل ضبط `start-fast=y` بحيث يبدأ النسخ الاحتياطي فورًا. يفرض هذا نقطة تحقق، لكن بما أن النسخ الاحتياطية تُشغَّل عادة مرة واحدة يوميًا فلا ينبغي لنقطة تحقق إضافية أن يكون لها تأثير ملحوظ في الأداء. ومع ذلك، على العناقيد المزدحمة جدًا قد يكون الأنسب تمرير `--start-fast` في سطر الأوامر عند الحاجة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة البدء السريع للنسخ الاحتياطي

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

pg-primary **⇒** أخذ نسخة احتياطية من العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=451-67e8eca3 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-190624F
P00   INFO: full backup size = 22MB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=451-67e8eca3 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

سيحاول pgBackRest افتراضيًا إجراء نسخة احتياطية تزايدية. غير أن النسخة التزايدية يجب أن تستند إلى نسخة كاملة، ولما لم تكن ثمة نسخة كاملة نفّذ pgBackRest نسخة كاملة بدلًا منها.

يمكن استخدام الخيار `type` لتحديد نسخة احتياطية كاملة أو تفاضلية.

pg-primary **⇒** نسخة احتياطية تفاضلية من العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-190624F_20261002-190626D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=477-af59c897 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

لم يظهر تحذير هذه المرة لأن نسخة كاملة كانت موجودة سلفًا. وبينما يمكن أن تستند النسخ التزايدية إلى نسخة كاملة *أو* تفاضلية، يجب أن تستند النسخ التفاضلية إلى نسخة كاملة. ويمكن إجراء نسخة كاملة بتشغيل الأمر `backup` مع `--type=full`.

أثناء النسخ الاحتياطي أثناء تشغيل PostgreSQL ينتظر pgBackRest أرشفة مقاطع WAL المطلوبة لاتساق النسخة الاحتياطية. ويحكم زمن الانتظار هذا خيارُ pgBackRest `archive-timeout` الذي تبلغ قيمته الافتراضية 60 ثانية. فإذا كان معلومًا أن أرشفة مقطع منفرد تستغرق وقتًا أطول فينبغي زيادة هذا الخيار.


### جدولة نسخة احتياطية {#schedule-a-backup}

يمكن جدولة النسخ الاحتياطية بأدوات مثل cron.

في المثال التالي، تُهيَّأ مهمتا cron للتشغيل؛ إذ تُجدوَل النسخ الكاملة عند الساعة 6:30 صباح كل يوم أحد، مع جدولة النسخ التفاضلية عند الساعة 6:30 صباحًا من الاثنين إلى السبت. فإذا ثُبِّت هذا الـ crontab لأول مرة في منتصف الأسبوع، فسينفذ pgBackRest نسخة كاملة في أول مرة تُشغَّل فيها مهمة النسخ التفاضلي، تتبعها في اليوم التالي نسخة تفاضلية.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

بمجرد جدولة النسخ الاحتياطية من المهم تهيئة الاحتفاظ بحيث تنتهي صلاحية النسخ الاحتياطية وفق جدول منتظم، راجع [الاحتفاظ](#retention).


### معلومات النسخ الاحتياطي {#backup-information}

استخدم الأمر `info` للحصول على معلومات عن النسخ الاحتياطية.

pg-primary **⇒** الحصول على معلومات العنقود التجريبي

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-190624F
            timestamp start/stop: 2026-10-02 19:06:24+00 / 2026-10-02 19:06:26+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 22MB, database backup size: 22MB
            repo1: backup set size: 2.9MB, backup size: 2.9MB

        diff backup: 20261002-190624F_20261002-190626D
            timestamp start/stop: 2026-10-02 19:06:26+00 / 2026-10-02 19:06:28+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 22MB, database backup size: 8.3KB
            repo1: backup set size: 2.9MB, backup size: 448B
            backup reference total: 1 full
```

يعمل الأمر `info` على stanza واحدة أو على جميع الـ stanzas. والمخرَج النصي هو الافتراضي ويعطي ملخصًا مقروءًا للنسخ الاحتياطية للـ stanza المطلوبة. وهذه الصيغة قابلة للتغيير مع أي إصدار.

للحصول على مخرَج قابل للقراءة آليًا استخدم `--output=json`. ويحتوي مخرَج JSON على معلومات أكثر بكثير من المخرَج النصي ويُحافَظ على ثباته ما لم يُكتشف خطأ.

لتسريع التنفيذ، حدّ المخرَج بمعلومات التقدم فقط بتحديد `--detail-level=progress`. ولاحظ أن هذا يتخطى جميع الفحوص ما عدا فحص توافر الـ stanza.

لكل stanza قسم منفصل ويمكن حصر المخرَج في stanza واحدة بالخيار `--stanza`. وتعطي '`status`' الخاصة بالـ stanza مؤشرًا موجزًا على صحة الـ stanza. فإذا كانت '`ok`' فإن pgBackRest يعمل بشكل طبيعي. وإذا وُجدت مستودعات متعددة، فإن الحالة '`mixed`' تشير إلى أن الـ stanza ليست في حالة سليمة على مستودع واحد أو أكثر؛ وفي هذه الحالة تُفصَّل حالة الـ stanza لكل مستودع. وفي الحالات التي يقع فيها على مستودع خطأ ليس من رموز الأخطاء المعروفة، فسيُستخدم رمز الخطأ '`other`' وتُقدَّم تفاصيل الخطأ الكاملة. ويُظهر '`wal archive min/max`' الحد الأدنى والأقصى لـ WAL المخزَّن حاليًا في الأرشيف، وفي حالة تعدد المستودعات يُبلَّغ عنه عبر جميع المستودعات ما لم يُضبط الخيار `--repo`. ولاحظ أنه قد توجد فجوات بسبب سياسات الاحتفاظ بالأرشيف أو لأسباب أخرى.

ستظهر رسالتا '`backup/expire running`' و/أو '`restore running`' بجانب معلومات '`status`' إذا كان أي من تلك الأوامر يعمل حاليًا على المضيف. وسيُبلَّغ أيضًا عن التقدم لكل مستودع في المخرَج النصي وستُضمَّن مصفوفة '`repo`' في مخرَج JSON.

تُعرض النسخ الاحتياطية من الأقدم إلى الأحدث. ستكون النسخة الأقدم *دائمًا* نسخة كاملة (يُدلَّل عليها بحرف `F` في نهاية التسمية) أما النسخة الأحدث فقد تكون كاملة أو تفاضلية (تنتهي بـ `D`) أو تزايدية (تنتهي بـ `I`).

تحدد '`timestamp start/stop`' الفترة الزمنية التي جرى فيها النسخ الاحتياطي. ويمكن استخدام '`timestamp stop`' لتحديد النسخة الاحتياطية الواجب استخدامها عند إجراء الاستعادة إلى نقطة زمنية محددة. ويمكن الاطلاع على مزيد من المعلومات عن الاستعادة إلى نقطة زمنية محددة في قسم [الاستعادة إلى نقطة زمنية محددة](#point-in-time-recovery).

تحدد '`wal start/stop`' نطاق WAL المطلوب لجعل قاعدة البيانات متسقة عند الاستعادة. وسيضمن الأمر `backup` وجود نطاق WAL هذا في الأرشيف قبل الاكتمال.

الحجم '`database size`' هو الحجم الكامل غير المضغوط لقاعدة البيانات، بينما '`database backup size`' هو مقدار البيانات في قاعدة البيانات التي سيؤخذ نسخ احتياطي منها فعليًا (وسيكونان متساويين في النسخ الكاملة).

يشير '`repo`' إلى المستودع الذي تقع فيه هذه النسخة الاحتياطية. ويشمل '`backup set size`' جميع ملفات هذه النسخة وأي نسخ مشار إليها في المستودع والمطلوبة لاستعادة قاعدة البيانات من هذه النسخة، بينما يشمل '`backup size`' فقط الملفات الموجودة في هذه النسخة (وسيكونان متساويين أيضًا في النسخ الكاملة). وتعكس أحجام المستودع الأحجام المضغوطة للملفات إذا كان الضغط ممكَّنًا في pgBackRest.

يلخص '`backup reference total`' قائمة النسخ الاحتياطية الإضافية المطلوبة لاستعادة هذه النسخة. واستخدم الخيار `--set` لعرض قائمة المراجع الكاملة.


### استعادة نسخة احتياطية {#restore-a-backup}

يمكن للنسخ الاحتياطية أن تحميك من عدد من سيناريوهات الكوارث، أكثرها شيوعًا العطل العتادي وتلف البيانات. وأسهل طريقة لمحاكاة تلف البيانات هي حذف ملف مهم من عنقود PostgreSQL.

pg-primary **⇒** إيقاف العنقود التجريبي وحذف الملف `pg_control`

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres rm /var/lib/postgresql/17/demo/global/pg_control
```

سيؤدي تشغيل العنقود دون هذا الملف المهم إلى حدوث خطأ.

pg-primary **⇒** محاولة تشغيل العنقود التجريبي التالف

```bash
sudo pg_ctlcluster 17 demo start
```

```text
Error: /usr/lib/postgresql/17/bin/pg_ctl /usr/lib/postgresql/17/bin/pg_ctl start -D /var/lib/postgresql/17/demo -l /var/log/postgresql/postgresql-17-demo.log -s -o  -c config_file="/etc/postgresql/17/demo/postgresql.conf"  exited with status 1:
postgres: could not find the database system
Expected to find it in the directory "/var/lib/postgresql/17/demo",
but could not open file "/var/lib/postgresql/17/demo/global/pg_control": No such file or directory
Examine the log output.
```

لاستعادة نسخة احتياطية من عنقود PostgreSQL شغّل pgBackRest بالأمر `restore`. ويجب أن يكون العنقود متوقفًا (وهو متوقف بالفعل في هذه الحالة) ويجب إزالة جميع الملفات من دليل بيانات PostgreSQL.

pg-primary **⇒** إزالة الملفات القديمة من العنقود التجريبي

```bash
sudo -u postgres find /var/lib/postgresql/17/demo -mindepth 1 -delete
```

pg-primary **⇒** استعادة العنقود التجريبي وتشغيل PostgreSQL

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo pg_ctlcluster 17 demo start
```

نجح تشغيل العنقود هذه المرة لأن الاستعادة عوّضت الملف `pg_control` المفقود.

يمكن الاطلاع على مزيد من المعلومات عن الأمر `restore` في قسم [الاستعادة](#restore-1).


--------

## المراقبة {#monitoring}

المراقبة جزء مهم من أي نظام إنتاجي. وهناك العديد من الأدوات المتاحة، ويمكن مراقبة pgBackRest على أي منها بجهد بسيط.

يستطيع pgBackRest إخراج معلومات عن المستودع بصيغة JSON تشمل قائمة بجميع النسخ الاحتياطية لكل stanza ومعلومات أرشيف WAL.


### داخل PostgreSQL {#in-postgresql}

يتيح أمر `COPY` في PostgreSQL تحميل معلومات pgBackRest إلى جدول. ويغلّف المثال التالي هذا المنطق في دالة يمكن استخدامها لإجراء استعلامات فورية.

pg-primary **⇒** تحميل دالة معلومات pgBackRest لـ PostgreSQL

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
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
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

يمكن الآن استخدام الدالة `monitor.pgbackrest_info()` لتحديد وقت آخر نسخة احتياطية ناجحة وWAL المؤرشف لكل stanza.

pg-primary **⇒** الاستعلام عن وقت آخر نسخة احتياطية ناجحة وWAL المؤرشف

```bash
sudo -u postgres cat \
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
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
       /var/lib/postgresql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 19:06:28+00 | 000000010000000000000005
(1 row)
```

### استخدام jq {#using-jq}

jq هي أداة مساعدة لسطر الأوامر تستطيع استخراج البيانات من JSON بسهولة.

pg-primary **⇒** تثبيت الأداة المساعدة jq

```bash
sudo apt-get install jq
```

يمكن الآن استخدام jq للاستعلام عن وقت آخر نسخة احتياطية ناجحة لكل stanza.

pg-primary **⇒** الاستعلام عن وقت آخر نسخة احتياطية ناجحة

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .backup[-1] | .timestamp.stop'
```

```text
1790967988
```

أو آخر WAL مؤرشف.

pg-primary **⇒** الاستعلام عن آخر WAL مؤرشف

```bash
sudo -u postgres pgbackrest --output=json --stanza=demo info | \
       jq '.[0] | .archive[-1] | .max'
```

```text
"000000010000000000000005"
```

ملاحظة:

تتطلب هذه الصياغة jq v1.5.

ملاحظة:

قد تقرّب jq الأعداد الكبيرة مثل معرفات النظام. فاختبر استعلاماتك بعناية.


--------

## النسخ الاحتياطي {#backup-1}

عند تهيئة مستودعات متعددة، سيأخذ pgBackRest النسخ الاحتياطي إلى المستودع ذي الأولوية الأعلى (مثل `repo1`) ما لم يُحدد الخيار `--repo`.

لا يتضمن pgBackRest مجدولًا مدمجًا لذا من الأفضل تشغيله من cron أو أي آلية جدولة أخرى.

راجع [إجراء نسخة احتياطية](#perform-a-backup) لمزيد من التفاصيل والأمثلة.


### تجميع الملفات {#file-bundling}

يوفر تجميع الملفات معًا في المستودع الوقتَ أثناء النسخ الاحتياطي وبعضَ المساحة في المستودع. ويكون ذلك أوضح بشكل خاص عندما يُخزَّن المستودع على مخزن كائنات مثل S3 أو على أنظمة ملفات ذات أحجام كتل كبيرة. فزمن إنشاء كل ملف على مخازن الكائنات أعلى، وقد يكلف تخزين الملفات الصغيرة جدًا بقدر ما يكلفه تخزين الملفات الأكبر.

تُمكَّن ميزة تجميع الملفات بالخيار `repo-bundle`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-bundle`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

ستحتوي النسخة الكاملة دون تجميع الملفات على 1000 ملف أو أكثر في مسار النسخ الاحتياطي، لكن مع التجميع ينخفض العدد الإجمالي للملفات انخفاضًا كبيرًا. وميزة إضافية هي أن الملفات صفرية الطول لا تُخزَّن (إلا في البيان)، بينما يُخزَّن في النسخ الاحتياطي العادي كل ملف صفري الطول على حدة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** التحقق من إجمالي عدد الملفات

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

يمكن استخدام الخيارين `repo-bundle-size` و`repo-bundle-limit` للضبط، مع أن القيم الافتراضية ينبغي أن تكون مثالية في معظم الحالات.

وبينما يكون تجميع الملفات أكثر كفاءة عمومًا، فإن عائبه أن استرجاع الملفات من المستودع يدويًا أكثر صعوبة. وقد لا يكون مثاليًا للتخزين المنزوع التكرار لأن كل نسخة كاملة سترتب الملفات في الحزم بشكل مختلف. وأخيرًا، لا يمكن استئناف حزم الملفات، فاحرص على ألا تضبط `repo-bundle-limit` بقيمة مرتفعة جدًا.


### النسخ التزايدي بالكتل {#block-incremental}

توفر النسخ الاحتياطية التزايدية بالكتل المساحة بتخزين أجزاء الملف التي تغيرت منذ النسخة الاحتياطية السابقة فقط بدلًا من تخزين الملف بأكمله.

تُمكَّن ميزة التزايد بالكتل بالخيار `repo-block` وتعمل بأفضل حال عند تمكينها لجميع أنواع النسخ الاحتياطي. ويجب أيضًا تمكين تجميع الملفات.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-block`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

### التعليقات التوضيحية للنسخ الاحتياطي {#backup-annotations}

يمكن للمستخدمين إرفاق أزواج مفتاح/قيمة معلوماتية بالنسخة الاحتياطية. ويمكن استخدام هذا الخيار عدة مرات لإرفاق تعليقات توضيحية متعددة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة مع تعليقات توضيحية

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

تُخرَج التعليقات التوضيحية في المخرَج النصي للأمر `info` عند تحديد نسخة احتياطية بـ `--set`، وتظهر دائمًا في مخرَج JSON.

pg-primary **⇒** الحصول على معلومات العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-190643F
            timestamp start/stop: 2026-10-02 19:06:43+00 / 2026-10-02 19:06:44+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22MB, database backup size: 22MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                key: value
                source: demo backup
```

يمكن إضافة التعليقات التوضيحية المرفقة بالأمر `backup` أو تعديلها أو إزالتها لاحقًا باستخدام الأمر `annotate`.

pg-primary **⇒** تغيير التعليقات التوضيحية للنسخة الاحتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-190643F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (17): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-190643F
            timestamp start/stop: 2026-10-02 19:06:43+00 / 2026-10-02 19:06:44+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 22MB, database backup size: 22MB
            repo1: backup size: 2.9MB
            database list: postgres (5)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## الاحتفاظ {#retention}

من الأفضل عمومًا الاحتفاظ بأكبر عدد ممكن من النسخ الاحتياطية لتوفير نافذة أوسع لـ [الاستعادة إلى نقطة زمنية محددة](#point-in-time-recovery)، لكن يجب أيضًا مراعاة الاعتبارات العملية مثل مساحة القرص. وتزيل خيارات الاحتفاظ النسخ الاحتياطية الأقدم بمجرد ألا تكون هناك حاجة إليها.

ينفذ pgBackRest تدوير النسخ الكاملة استنادًا إلى نوع الاحتفاظ الذي قد يكون عددًا أو فترة زمنية. وعند تحديد عدد، لا يهتم انتهاء الصلاحية بتوقيت إنشاء النسخ الاحتياطية بل بعدد النسخ الواجب الاحتفاظ بها. والنسخ التفاضلية قائمة على العدد لكنها ستنتهي صلاحيتها دائمًا عند انتهاء صلاحية النسخة الكاملة التي تعتمد عليها. أما النسخ التزايدية فلا تنتهي صلاحيتها بالاحتفاظ باستقلال — بل تنتهي صلاحيتها دائمًا مع نسختها الكاملة أو التفاضلية ذات الصلة. راجع القسمين [الاحتفاظ بالنسخ الاحتياطية الكاملة](#full-backup-retention) و[الاحتفاظ بالنسخ الاحتياطية التفاضلية](#differential-backup-retention) للتفاصيل والأمثلة.

يُحتفظ افتراضيًا بـ WAL المؤرشف للنسخ الاحتياطية التي لم تنتهِ صلاحيتها، ومع ذلك يمكن تعديل هذا الجدول لكل مستودع بخيارات retention-archive وإن لم يكن ذلك موصى به. راجع قسم [الاحتفاظ بالأرشيف](#archive-retention) للتفاصيل والأمثلة.

يُشغَّل الأمر `expire` تلقائيًا بعد كل نسخة احتياطية ناجحة ويمكن أيضًا للمستخدم تشغيله. وعند تشغيله من المستخدم، يقع انتهاء الصلاحية كما تحدده إعدادات الاحتفاظ لكل مستودع مهيأ. وإذا قُدِّم الخيار `--repo` فسيقع انتهاء الصلاحية على المستودع المحدد فقط. ويمكن أيضًا للمستخدم حصر انتهاء الصلاحية في مجموعة نسخ احتياطية محددة بالخيار `--set`، وما لم يُحدد الخيار `--repo` فستُفتَّش جميع المستودعات وستنتهي صلاحية أي منها كان مطابقًا لمعايير المجموعة. وينبغي التنبه إلى أن جدول الاحتفاظ بالأرشيف سيُفحص ويُنفَّذ في كل مرة يُشغَّل فيها الأمر `expire`.


### الاحتفاظ بالنسخ الاحتياطية الكاملة {#full-backup-retention}

يحدد `repo1-retention-full-type` كيفية تفسير الخيار `repo1-retention-full`؛ إما كعدد النسخ الكاملة الواجب الاحتفاظ بها أو عدد أيام الاحتفاظ بالنسخ الكاملة. ويجب أن تكتمل النسخ الاحتياطية الجديدة قبل وقوع انتهاء الصلاحية — أي أنه إذا كان `repo1-retention-full-type=count` و`repo1-retention-full=2` فستُخزَّن ثلاث نسخ كاملة قبل انتهاء صلاحية الأقدم منها، أو إذا كان `repo1-retention-full-type=time` و`repo1-retention-full=20` فيجب أن توجد نسخة كاملة عمرها 20 يومًا على الأقل قبل أن يمكن أن يقع انتهاء الصلاحية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-full`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

الاحتفاظ `repo1-retention-full=2` لكن لا توجد حاليًا سوى نسخة كاملة واحدة لذا لن تنتهي صلاحية أي نسخة كاملة عند تشغيل النسخة الكاملة التالية.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 975 lines of output]
P00   INFO: repo1: remove expired backup 20261002-190641F
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190643F, start = 000000020000000000000008
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

تنتهي صلاحية الأرشيف *فعلًا* لأن مقاطع WAL وُلدت قبل النسخة الاحتياطية الأقدم. وهذه غير مفيدة للاسترداد — فلا يمكن استخدام إلا مقاطع WAL المتولدة بعد نسخة احتياطية لاسترداد تلك النسخة.

pg-primary **⇒** إجراء نسخة احتياطية كاملة

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-190643F
P00   INFO: repo1: remove expired backup 20261002-190643F
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000008, stop = 00000002000000000000000A
P00   INFO: expire command end: completed successfully
```

انتهت صلاحية النسخة الكاملة `20261002-190624F` وأصبح الاحتفاظ بالأرشيف مبنيًا على `20261002-190646F` التي هي الآن النسخة الكاملة الأقدم.


### الاحتفاظ بالنسخ الاحتياطية التفاضلية {#differential-backup-retention}

اضبط `repo1-retention-diff` على عدد النسخ التفاضلية المطلوب. وتعتمد النسخ التفاضلية على النسخة الكاملة السابقة فقط لذا يمكن إنشاء مجموعة تفاضلية «متجددة» لآخر يوم أو أكثر. يسمح هذا باستعادات سريعة إلى نقاط زمنية حديثة لكنه يقلل الاستهلاك الكلي للمساحة.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

الاحتفاظ `repo1-retention-diff=1` لذا سيلزم إجراء نسختين تفاضليتين قبل انتهاء صلاحية إحداهما. وتُضاف نسخة احتياطية تزايدية لعرض انتهاء صلاحية النسخ التزايدية توضيحيًا، وهو في هذه الحالة يعتمد على انتهاء صلاحية النسخة التفاضلية.

pg-primary **⇒** إجراء نسختين احتياطيتين تفاضلية وتزايدية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

الآن سيؤدي إجراء نسخة احتياطية تفاضلية إلى إنهاء صلاحية النسختين التفاضلية والتزايدية السابقتين بحيث لا تبقى سوى نسخة تفاضلية واحدة.

pg-primary **⇒** إجراء نسخة احتياطية تفاضلية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=956-fb652d58 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-190648F_20261002-190650D, 20261002-190648F_20261002-190651I
P00   INFO: repo1: remove expired backup 20261002-190648F_20261002-190651I
P00   INFO: repo1: remove expired backup 20261002-190648F_20261002-190650D
P00   INFO: expire command end: completed successfully
```

### الاحتفاظ بالأرشيف {#archive-retention}

مع أن pgBackRest يزيل مقاطع WAL المؤرشفة تلقائيًا عند إنهاء صلاحية النسخ الاحتياطية (والافتراضي هو إنهاء صلاحية WAL للنسخ الكاملة استنادًا إلى الخيار `repo1-retention-full`)، فقد يكون من المفيد إنهاء صلاحية الأرشيف بوتيرة أكثر عدوانية لتوفير مساحة القرص. ولاحظ أن النسخ الكاملة تُعامل معاملة النسخ التفاضلية لأغراض الاحتفاظ التفاضلي بالأرشيف.

لن يزيل إنهاء صلاحية الأرشيف أبدًا مقاطع WAL المطلوبة لجعل نسخة احتياطية متسقة. ومع ذلك، وبما أن الاستعادة إلى نقطة زمنية محددة (PITR) لا تعمل إلا على تدفق WAL متصل، فينبغي توخي الحذر عند إنهاء صلاحية الأرشيف بوتيرة عدوانية خارج عملية انتهاء صلاحية النسخ الاحتياطية المعتادة. ولتحديد ما ستنتهي صلاحيته دون إنهاء صلاحية أي شيء فعليًا، يمكن تقديم الخيار `dry-run` في سطر الأوامر مع الأمر `expire`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-retention-diff`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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
P00   INFO: new backup label = 20261002-190648F_20261002-190654D
P00   INFO: diff backup size = 8.3KB, file total = 963
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** إنهاء صلاحية الأرشيف

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=1037-f7b8ca1a --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190646F, start = 00000002000000000000000B, stop = 00000002000000000000000B
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F_20261002-190652D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 17-1 archive retention on backup 20261002-190648F_20261002-190654D, start = 000000020000000000000016
P00   INFO: repo1: 17-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 17-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

تحتوي النسخة التفاضلية `20261002-190648F_20261002-190652D` على مقاطع WAL مؤرشفة يجب الاحتفاظ بها لجعل النسخ الاحتياطية الأقدم متسقة حتى وإن لم يعد بالإمكان تقديمها إلى الأمام أكثر مع PITR. وتُزال مقاطع WAL المتولدة بعد `20261002-190648F_20261002-190652D` وقبل `20261002-190648F_20261002-190654D`. وتبقى مقاطع WAL المتولدة بعد النسخة الجديدة `20261002-190648F_20261002-190654D` ويمكن استخدامها لـ PITR.

ولأن النسخ الكاملة تُعد نسخًا تفاضلية لأغراض الاحتفاظ التفاضلي بالأرشيف، فإذا أُجريت الآن نسخة كاملة بالإعدادات نفسها فلن يُحتفظ لأجل PITR إلا بالأرشيف الخاص بتلك النسخة الكاملة.


--------

## الاستعادة {#restore-1}

يختار الأمر restore افتراضيًا وبشكل تلقائي أحدث نسخة احتياطية من أول مستودع توجد فيه نسخ احتياطية (راجع [البدء السريع - استعادة نسخة احتياطية](#restore-a-backup)). ويحدد الترتيب الذي تُفحص به المستودعات الملفُ `pgbackrest.conf` (مثلًا سيُفحص repo1 قبل repo2). وللاختيار من مستودع محدد، يمكن تمرير الخيار `--repo` (مثل `--repo=1`). ويمكن تمرير الخيار `--set` إذا رُغبت في نسخة احتياطية غير الأحدث.

عند تحديد استعادة إلى نقطة زمنية بنوع `--type=time` أو `--type=lsn`، يجب تقديم الوقت المستهدف أو LSN المستهدف بالخيار `--target`. وإذا لم يُحدد `--set`، تُفحص المستودعات المهيأة بالترتيب بحثًا عن نسخة احتياطية وقت إيقافها قبل الوقت المستهدف، أو كان LSN إيقافها أقل من أو يساوي LSN المستهدف. فإذا لم يُعثر على نسخة مطابقة، يطلق pgBackRest خطأً في الحالتين `--type=time` و`--type=lsn` معًا؛ فهو لا يرتد إلى أحدث نسخة احتياطية. أما أنواع PITR الأخرى، مثل `xid`، فيجب تقديم الخيار `--set` إذا كان الهدف قبل أحدث نسخة احتياطية. راجع [الاستعادة إلى نقطة زمنية محددة](#point-in-time-recovery) لمزيد من التفاصيل والأمثلة.

لا تُضمَّن خانات النسخ المتماثل تبعًا لتوصية PostgreSQL. راجع [أخذ نسخة احتياطية من دليل البيانات](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) في وثائق PostgreSQL لمزيد من المعلومات.

تقدّم الأقسام التالية ميزات إضافية للأمر `restore`.


### ملكية الملفات {#file-ownership}

إذا شُغِّل `restore` باعتبار مستخدم غير الجذر (وهو السيناريو المعتاد) فإن ملكية جميع الملفات المستعادة ستعود إلى المستخدم/المجموعة التي تنفذ pgBackRest. وإذا كانت ملكية الملفات الموجودة ليست للمستخدم/المجموعة المنفذة فسينتج خطأ إذا تعذر تحديث الملكية إلى المستخدم/المجموعة المنفذة. وفي هذه الحالة سيلزم أن يحدّث ملكية الملفات مستخدم ذو صلاحيات كافية قبل إعادة محاولة الاستعادة.

أما إذا شُغِّل `restore` باعتبار المستخدم `root` فسيحاول pgBackRest إعادة إنشاء الملكية المسجلة في البيان وقت أخذ النسخة الاحتياطية. ولا تُخزَّن في البيان سوى **أسماء** المستخدم/المجموعة لذا يجب أن توجد الأسماء نفسها على مضيف الاستعادة لكي ينجح ذلك. وإذا تعذر العثور على اسم المستخدم/المجموعة محليًا فسيُستخدم المستخدم/المجموعة لدليل بيانات PostgreSQL، وأخيرًا `root` إذا تعذر ربط مستخدم/مجموعة دليل البيانات باسم.


### خيار الدلتا {#delta-option}

تطلب قسم [استعادة نسخة احتياطية](#restore-a-backup) في [البدء السريع](#quick-start) تنظيف دليل عنقود قاعدة البيانات قبل تنفيذ `restore`. ويتيح الخيار `delta` لـ pgBackRest أن يحدد تلقائيًا أي الملفات في دليل عنقود قاعدة البيانات يمكن الاحتفاظ بها وأيها يحتاج إلى استعادة من النسخة الاحتياطية — وهو أيضًا *يزيل* الملفات غير الموجودة في بيان النسخة الاحتياطية وبذلك يتخلص من التغييرات المتباينة. ويتم ذلك بحساب بصمة تشفيرية [SHA-1](https://en.wikipedia.org/wiki/SHA-1) لكل ملف في دليل عنقود قاعدة البيانات. فإذا لم تطابق بصمة `SHA-1` البصمة المخزنة في النسخة الاحتياطية فسيُستعاد ذلك الملف. وهذه العملية فعالة جدًا عند دمجها مع الخيار `process-max`. ولأن خادم PostgreSQL متوقف أثناء الاستعادة، يمكن استخدام عدد أكبر من العمليات مما قد يكون مرغوبًا أثناء نسخ احتياطي يعمل فيه خادم PostgreSQL.

pg-primary **⇒** إيقاف العنقود التجريبي وتنفيذ استعادة دلتا

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/postgresql/17/demo' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/postgresql/17/demo/base/1/pg_internal.init'
       [filtered 769 lines of output]
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/113 - exists and matches backup (bundle 20261002-190648F/1/2665832, 8KB, 88.00%) checksum 1cd643347b87a472ff001ae124e4b532ce998d2f
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/1/112 - exists and matches backup (bundle 20261002-190648F/1/2665920, 8KB, 88.03%) checksum 2cbd5cf8fb22ef627eb539776c5ec7457bdb2890
P01 DETAIL: restore file /var/lib/postgresql/17/demo/PG_VERSION - exists and matches backup (bundle 20261002-190648F/1/2666008, 3B, 88.03%) checksum ad48103e4fc71796e9708cafc43adeed0d1076b7
P01 DETAIL: restore file /var/lib/postgresql/17/demo/base/5/2608_fsm - exists and matches backup (bundle 20261002-190648F/1/2666032, 24KB, 88.14%) checksum e807fe622bbfccc5e9ad7f453ecb4f0eaccb75e2
P01 DETAIL: restore file /var/lib/postgresql/17/demo/postgresql.auto.conf - exists and matches backup (bundle 20261002-190648F/1/2666272, 229B, 88.14%) checksum e1b0002d9a33d70466c5a348f4e0c1f1f80639f6
       [filtered 233 lines of output]
```

pg-primary **⇒** إعادة تشغيل PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

### استعادة قواعد بيانات محددة {#restore-selected-databases}

قد توجد حالات يُرغب فيها في استعادة قواعد بيانات محددة انتقائيًا من نسخة احتياطية للعنقود. وقد يُفعل ذلك لأسباب تتعلق بالأداء أو لنقل قواعد بيانات مختارة إلى آلة لا تتوفر لديها مساحة كافية لاستعادة نسخة العنقود كاملة.

لعرض هذه الميزة توضيحيًا تُنشأ قاعدتا بيانات: test1 وtest2.

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

ستُزوَّد كل قاعدة بيانات اختبارية بجداول وبيانات لعرض أن الاسترداد يعمل مع الاستعادة الانتقائية.

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

تُنفَّذ نسخة احتياطية جديدة لكي يكون pgBackRest على علم بقواعد البيانات الجديدة.

pg-primary **⇒** إجراء نسخة احتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

أحد الأسباب الرئيسية لاستخدام الاستعادة الانتقائية هو توفير المساحة. ويُعرض هنا حجم قاعدة البيانات test1 بحيث يمكن مقارنته باستخدام القرص بعد استعادة انتقائية.

pg-primary **⇒** عرض المساحة المستخدمة من قاعدة البيانات test1

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
7.4M	/var/lib/postgresql/17/demo/base/32768
```

إذا لم تكن قاعدة البيانات المطلوب استعادتها معروفة، فاستخدم خيار `set` للأمر `info` لاستكشاف قواعد البيانات التي تشكل جزءًا من مجموعة النسخ الاحتياطي.

pg-primary **⇒** عرض قائمة قواعد البيانات للنسخة الاحتياطية

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-190648F_20261002-190702I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 1.9MB
            backup reference list: 20261002-190648F, 20261002-190648F_20261002-190654D
            database list: postgres (5), test1 (32768), test2 (32769)
```

أوقف العنقود واستعد قاعدة البيانات test2 وحدها. وتُستعاد قواعد البيانات المدمجة (`template0` و`template1` و`postgres`) دائمًا.

تحذير:

قد يفشل الاسترداد بخطأ ما لم يُحدد `--type=immediate`. وسبب ذلك أنه بعد بلوغ الاتساق سيعتبر PostgreSQL الصفحات المملوءة بالأصفار أخطاءً حتى في حالة كتابة الصفحة الكاملة. وفي PostgreSQL ≥ 13 يمكن استخدام إعداد ignore_invalid_pages لتجاهل الصفحات غير الصالحة. وفي هذه الحالة من المهم فحص السجلات بعد الاسترداد لضمان عدم الإبلاغ عن أي صفحات غير صالحة في قواعد البيانات المختارة.

pg-primary **⇒** الاستعادة من آخر نسخة احتياطية بتضمين قاعدة البيانات test2 فقط

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

بمجرد اكتمال الاسترداد ستحتوي قاعدة البيانات test2 على جميع الجداول والبيانات التي أُنشئت سابقًا.

pg-primary **⇒** البرهنة على أن قاعدة البيانات test2 استُردت

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

قاعدة البيانات test1، رغم نجاح استردادها، غير متاحة. وسبب ذلك أن قاعدة البيانات بأكملها استُعيدت كملفات متناثرة (sparse) مملوءة بالأصفار. ويستطيع PostgreSQL تطبيق WAL بنجاح على الملفات المصفَّرة لكن قاعدة البيانات ككل لن تكون صالحة لأن الملفات المفتاحية لا تحتوي على بيانات. وهذا مقصود لمنع استخدام قاعدة البيانات عرضًا حين قد تحتوي على بيانات جزئية طُبقت أثناء إعادة تشغيل WAL.

pg-primary **⇒** محاولة الاتصال بقاعدة البيانات test1 ستنتج خطأً

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

ولأن قاعدة البيانات test1 تُستعاد بملفات متناثرة (sparse) مملوءة بالأصفار فلن تتطلب سوى مساحة بقدر مقدار WAL المكتوب أثناء الاسترداد. ومع أن مقدار WAL المتولد أثناء النسخ الاحتياطي والمطبق أثناء الاسترداد قد يكون كبيرًا، فإنه سيكون عمومًا جزءًا صغيرًا من الحجم الكلي لقاعدة البيانات، خصوصًا لقواعد البيانات الكبيرة التي يُرجَّح أن تكون هذه الميزة أنفع ما تكون لها.

من الواضح أن قاعدة البيانات test1 تستخدم مساحة قرص أقل بكثير أثناء الاستعادة الانتقائية مما كانت ستستخدمه لو استُعيدت قاعدة البيانات بأكملها.

pg-primary **⇒** عرض المساحة المستخدمة من قاعدة البيانات test1 بعد الاسترداد

```bash
sudo -u postgres du -sh /var/lib/postgresql/17/demo/base/32768
```

```text
8.0K	/var/lib/postgresql/17/demo/base/32768
```

في هذه المرحلة الإجراء الوحيد الممكن على قاعدة البيانات test1 غير الصالحة هو `drop database`. ولا يحذف pgBackRest قاعدة البيانات تلقائيًا لأن ذلك لا يمكن حتى يكتمل الاسترداد ويصبح العنقود متاحًا.

pg-primary **⇒** حذف قاعدة البيانات test1

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

الآن بعد حذف قاعدة البيانات test1 غير الصالحة لم يبقَ سوى قاعدة البيانات test2 وقواعد البيانات المدمجة.

pg-primary **⇒** سرد قواعد البيانات المتبقية

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
     4 | template0
     5 | postgres
 32769 | test2
(4 rows)
```

--------

## الاستعادة إلى نقطة زمنية محددة {#point-in-time-recovery}

نفّذ قسم [استعادة نسخة احتياطية](#restore-a-backup) في [البدء السريع](#quick-start) استردادًا افتراضيًا، أي التشغيل حتى نهاية تدفق WAL بالكامل. وفي حالة العطل العتادي هذا عادة الخيار الأفضل، لكن في سيناريوهات تلف البيانات (سواء كان مصدرها الآلة أم الإنسان) تكون الاستعادة إلى نقطة زمنية محددة (PITR) أنسب في الغالب.

تتيح الاستعادة إلى نقطة زمنية محددة (PITR) تشغيل WAL من نسخة احتياطية إلى lsn محدد أو وقت محدد أو معرف معاملة محدد أو نقطة استرداد محددة. وفي سيناريوهات الاسترداد الشائعة تُعد الاستعادة القائمة على الوقت الأكثر فائدة على الأرجح. وسيناريو الاسترداد النموذجي هو استعادة جدول حُذف عرضًا أو بيانات حُذفت عرضًا. واسترداد جدول محذوف أكثر إثارة للاهتمام لذا هو المثال المعطى هنا، لكن البيانات المحذوفة ستُسترد بالطريقة نفسها تمامًا.

pg-primary **⇒** إنشاء جدول يحتوي على بيانات مهمة جدًا

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

من المهم تمثيل الوقت كما يحسبه PostgreSQL وتضمين إزاحات المنطقة الزمنية. فهذا يقلل احتمال التحويلات غير المقصودة بين المناطق الزمنية ونتيجة استرداد غير متوقعة.

pg-primary **⇒** الحصول على الوقت من PostgreSQL

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 19:07:12.060959+00
```

الآن بعد تسجيل الوقت يُحذف الجدول. وعمليًا العثور على الوقت الدقيق الذي حُذف فيه الجدول أصعب بكثير مما هو في هذا المثال. وقد لا يكون العثور على الوقت الدقيق ممكنًا، لكن بعض العمل الاستقصائي ينبغي أن يقربك منه.

pg-primary **⇒** حذف الجدول المهم

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

إذا اختيرت النسخة الاحتياطية الخاطئة للاستعادة فسيفشل الاسترداد إلى الهدف الزمني المطلوب. ولتوضيح ذلك تُنفَّذ نسخة احتياطية تزايدية جديدة غير موجود فيها `important_table`.

pg-primary **⇒** إجراء نسخة احتياطية تزايدية

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-190648F_20261002-190713I
            timestamp start/stop: 2026-10-02 19:07:13+00 / 2026-10-02 19:07:14+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

لن يكون ممكنًا استرداد الجدول المفقود من هذه النسخة الاحتياطية لأن PostgreSQL لا يستطيع التشغيل إلا إلى الأمام، لا إلى الخلف.

pg-primary **⇒** محاولة الاسترداد من نسخة احتياطية غير صحيحة

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-190648F_20261002-190713I --target-timeline=current \
       --type=time "--target=2026-10-02 19:07:12.060959+00" --target-action=promote restore
sudo pg_ctlcluster 17 demo start
```

```text
       [filtered 13 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000120 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.03 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 1437) exited with exit code 1
LOG:  terminating any other active server processes
       [filtered 3 lines of output]
```

الطريقة الموثوقة هي تمكين pgBackRest من اختيار نسخة احتياطية قادرة على الاسترداد إلى الهدف الزمني تلقائيًا، أي نسخة انتهت قبل الوقت المحدد.

ملاحظة:

لا يستطيع pgBackRest اختيار نسخة احتياطية تلقائيًا عندما يكون نوع الاستعادة `xid` أو `name`.

pg-primary **⇒** استعادة العنقود التجريبي إلى `2026-10-02 19:07:12.060959+00`

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 19:07:12.060959+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 19:07:12.060959+00'
recovery_target_action = 'promote'
```

ولّد pgBackRest إعدادات الاسترداد في `postgresql.auto.conf` فيمكن تشغيل PostgreSQL فورًا. و`%f` هي الطريقة التي يحدد بها PostgreSQL مقطع WAL الذي يحتاجه، و`%p` هي الموقع الذي يجب نسخه إليه. وبمجرد أن ينهي PostgreSQL الاسترداد سيوجد الجدول مجددًا ويمكن الاستعلام عنه.

pg-primary **⇒** تشغيل PostgreSQL والتحقق من وجود الجدول المهم

```bash
sudo pg_ctlcluster 17 demo start
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

يحتوي سجل PostgreSQL أيضًا على معلومات قيّمة. فسيشير إلى الوقت والمعاملة التي توقف عندها الاسترداد وسيعطي أيضًا وقت آخر معاملة طُبقت.

pg-primary **⇒** فحص مخرَج سجل PostgreSQL

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 7 lines of output]
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
LOG:  starting point-in-time recovery to 2026-10-02 19:07:12.060959+00
LOG:  restored log file "00000003.history" from archive
LOG:  redo starts at 0/19000028
       [filtered 2 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "00000004000000000000001A" from archive
LOG:  recovery stopping before commit of transaction 748, time 2026-10-02 19:07:13.389359+00
LOG:  redo done at 0/1901CC00 system usage: CPU: user: 0.00 s, system: 0.01 s, elapsed: 0.07 s
LOG:  last completed transaction was at log time 2026-10-02 19:07:10.778316+00
LOG:  restored log file "000000040000000000000019" from archive
LOG:  selected new timeline ID: 5
       [filtered 5 lines of output]
```

--------

## حذف الـ stanza {#delete-a-stanza}

يزيل الأمر `stanza-delete` البيانات الموجودة في المستودع المرتبطة بالـ stanza.

تحذير:

استخدم هذا الأمر بحذر — فسيزيل نهائيًا جميع النسخ الاحتياطية والأرشيفات من مستودع pgBackRest الخاص بالـ stanza المحددة.

لحذف stanza:

- أوقف تشغيل عنقود PostgreSQL المرتبط بالـ stanza (أو استخدم --force لتجاوز ذلك).
- شغّل الأمر `stop` على المضيف الذي سيُشغَّل عليه الأمر `stanza-delete`.
- شغّل الأمر `stanza-delete`.

بمجرد اكتمال الأمر بنجاح، تصبح مسؤولية إزالة الـ stanza من جميع ملفات إعداد pgBackRest و/أو متغيرات البيئة على المستخدم.

لا يمكن حذف الـ stanza إلا من مستودع واحد في كل مرة. ولحذف الـ stanza من مستودعات متعددة، كرر الأمر `stanza-delete` لكل مستودع مع تحديد الخيار `--repo`.

pg-primary **⇒** إيقاف عنقود PostgreSQL المطلوب إزالته

```bash
sudo pg_ctlcluster 17 demo stop
```

pg-primary **⇒** إيقاف pgBackRest للـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=1568-4c984637 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** حذف الـ stanza من مستودع واحد

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=1576-48368d9e --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## المستودعات المتعددة {#multiple-repositories}

يمكن تهيئة مستودعات متعددة كما هو معروض في [دعم S3](#s3-compatible-object-store-support). ومن الفوائد المحتملة القدرة على امتلاك مستودع محلي لاستعادات سريعة ومستودع بعيد للتكرار.

بعض الأوامر، مثل [`stanza-create`](/ar/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/ar/pgbackrest/command/stanza-upgrade/)، ستعمل تلقائيًا مع جميع المستودعات المهيأة، بينما ستتطلب أخرى، مثل [`stanza-delete`](/ar/pgbackrest/command/stanza-delete/)، تحديد مستودع باستخدام الخيار `repo`.

لاحظ أن الخيار `repo` غير مطلوب عندما يكون `repo1` وحده مهيأ، حفاظًا على التوافق مع الإصدارات السابقة. لكن الخيار `repo` *مطلوب* عندما يكون مستودع واحد مهيأ باسم مثل `repo2`. وهذا لمنع انكسار الأوامر إذا أُضيف مستودع جديد لاحقًا.

سيدفع الأمر `archive-push` WAL إلى الأرشيف في جميع المستودعات المهيأة دائمًا. وعندما يتعذر الوصول إلى مستودع، سيستمر دفع WAL إلى المستودعات الأخرى. غير أنه لكي يعمل ذلك بفعالية، يجب تمكين `archive-async=y`؛ وإلا فلن تستطيع المستودعات الأخرى التقدم على المستودع غير القابل للوصول إلا بمقطع WAL واحد. ولاحظ أيضًا أنه إذا تعذر دفع WAL إلى أي مستودع، فلن يزيله PostgreSQL من الدليل `pg_wal`، مما قد يتسبب في نفاد مساحة وحدة التخزين.

يجب جدولة النسخ الاحتياطية لكل مستودع على حدة. وفي حالات كثيرة هذا مرغوب لأن أنواع النسخ الاحتياطي والاحتفاظ ستختلف باختلاف المستودع. وبالمثل، يجب أن تحدد الاستعادات مستودعًا. ومن الأفضل عمومًا تحديد للاستعادة مستودع ذي زمن استجابة/تكلفة منخفضين حتى لو عنى ذلك وقت استرداد أطول. ولا يمكن تحديد أي المستودعات سيكون الأكثر كفاءة إلا باختبار الاستعادة.


--------

## دعم مخازن الكائنات المتوافقة مع Azure {#azure-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن الكائنات المتوافقة مع Azure. ويجب إنشاء الحاوية المستخدمة لتخزين المستودع مسبقًا — فلن يفعل ذلك pgBackRest تلقائيًا. ويمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادة وضعه في مسار فرعي بحيث يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

تحذير:

لا تمكّن «مساحة الأسماء الهرمية» (hierarchical namespace) لأن ذلك سيسبب أخطاء أثناء انتهاء الصلاحية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة Azure

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

يمكن استخدام توقيعات الوصول المشترك بضبط الخيار `repo2-azure-key-type` على `sas` والخيار `repo2-azure-key` على رمز توقيع الوصول المشترك.

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

pg-primary **⇒** إنشاء الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1657-1f40c982 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

زمن إنشاء الملفات في Azure بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).

pg-primary **⇒** أخذ نسخة احتياطية من العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1666-1ab08562 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-190727F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1666-1ab08562 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## دعم مخازن الكائنات المتوافقة مع S3 {#s3-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن الكائنات المتوافقة مع S3. ويجب إنشاء الحاوية (bucket) المستخدمة لتخزين المستودع مسبقًا — فلن يفعل ذلك pgBackRest تلقائيًا. ويمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادة وضعه في مسار فرعي بحيث يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة S3

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

يجب تهيئة المنطقة ونقطة النهاية وفقًا لموقع الحاوية. والقيم المعطاة هنا هي لمنطقة `us-east-1`.

ينبغي إنشاء دور لتشغيل pgBackRest وضبط صلاحيات الحاوية بأكبر قدر ممكن من التقييد. فإذا كان الدور مرتبطًا بمثيل في AWS فسيسترد pgBackRest تلقائيًا بيانات اعتماد مؤقتة عندما يكون `repo3-s3-key-type=auto`، مما يعني أنه لا حاجة إلى ضبط المفاتيح صراحةً في `/etc/pgbackrest/pgbackrest.conf`.

ستقيد سياسة Amazon S3 النموذجية هذه جميع عمليات القراءة والكتابة على الحاوية ومسار المستودع.

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

زمن إنشاء الملفات في S3 بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).

pg-primary **⇒** أخذ نسخة احتياطية من العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1767-6031c435 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-190741F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1767-6031c435 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## دعم SFTP {#sftp-support}

يدعم pgBackRest وضع المستودعات على مضيفات SFTP. ونقل الملفات عبر SFTP بطيء نسبيًا لذا تستفيد الأوامر من زيادة `process-max` لموازاة نقل الملفات.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة SFTP

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

عند استخدام SFTP، إذا جُمعت libssh2 مقابل OpenSSH فإن `repo4-sftp-public-key-file` يكون اختياريًا.

pg-primary **⇒** توليد زوج مفاتيح SSH للنسخ الاحتياطي عبر SFTP

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** نسخ المفتاح العام للنسخ الاحتياطي عبر SFTP من pg-primary إلى sftp-server

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

تُشغَّل الأوامر تمامًا كما لو كان المستودع مخزنًا على قرص محلي.

pg-primary **⇒** إضافة بصمة sftp-server إلى ملف known_hosts لأن القيمة الافتراضية للخيار `repo4-sftp-host-key-check-type` هي "strict"

```bash
ssh-keyscan -H sftp-server >> /var/lib/postgresql/.ssh/known_hosts 2>/dev/null
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

pg-primary **⇒** أخذ نسخة احتياطية من العنقود التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1859-efaa8e87 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-190759F
P00   INFO: full backup size = 29.2MB, file total = 1265
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1859-efaa8e87 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## دعم مخازن الكائنات المتوافقة مع GCS {#gcs-compatible-object-store-support}

يدعم pgBackRest وضع المستودعات في مخازن الكائنات المتوافقة مع GCS. ويجب إنشاء الحاوية المستخدمة لتخزين المستودع مسبقًا — فلن يفعل ذلك pgBackRest تلقائيًا. ويمكن وضع المستودع في جذر الحاوية (`/`) لكن من الأفضل عادة وضعه في مسار فرعي بحيث يمكن أيضًا تخزين سجلات مخزن الكائنات أو بيانات أخرى في الحاوية دون تعارض.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة GCS

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



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

repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub

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

زمن إنشاء الملفات في GCS بطيء نسبيًا لذا يُحسَّن أداء `backup`/`restore` بتمكين [تجميع الملفات](#file-bundling).


--------

## الوقت المستهدف للمستودع {#target-time-for-repository}

يحدد الوقت المستهدف الوقت الذي تستخدمه الأوامر لقراءة مستودع على تخزين يدعم تعدد الإصدارات. يسمح هذا للأمر بقراءة المستودع كما كان عند نقطة زمنية معينة لاسترداد بيانات حُذفت أو تلفت بفعل خطأ المستخدم أو برمجيات خبيثة.

تدعم S3 وGCS وAzure التخزين الذي يدعم تعدد الإصدارات لكنه غير ممكَّن افتراضيًا عمومًا. وبالإضافة إلى تمكين تعدد الإصدارات، قد يكون من المفيد تمكين قفل الكائنات في S3 والحذف القابل للاسترجاع في GCS أو Azure.

عند تحديد الخيار `repo-target-time` يجب أيضًا تقديم الخيار `repo`. ومن المرجح ألا تدعم جميع أنواع المستودعات الإصدارات، وعمومًا من المنطقي استهداف مستودع واحد للاسترداد.

لاحظ أن المقارنات بالطابع الزمني للتخزين تكون بأقل من أو يساوي (<=) الطابع الزمني المقدم، وأن المللي ثانية تُقتطع من الطابع الزمني عند تقديمه.

لعرض هذه الميزة توضيحيًا تُحذف الـ stanza `demo` من مستودع S3.

pg-primary **⇒** حذف الـ stanza في مستودع S3

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

بمجرد حذف الـ stanza سيعرض الأمر `info` المستودع في حالة خطأ.

pg-primary **⇒** خطأ عند تنفيذ info

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

غير أنه بما أن التخزين يدعم تعدد الإصدارات، يمكن النظر إلى المستودع في وقت سابق لحذف الـ stanza. وقد يكون العثور على الوقت المستهدف صعبًا بحسب الموقف، لكن في هذه الحالة يمكن تحديد وقت حذف الـ stanza بفحص متى حُذف `backup.info`.

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
-----------------------------------------------------------------------------
|                            ListObjectVersions                             |
+--------+----------------------------+-------------------------------------+
| Action |         Modified           |               Object                |
+--------+----------------------------+-------------------------------------+
|  PUT   |  2026-10-02T19:07:41.474Z  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T19:07:56.815Z  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T19:08:04.878Z  |  demo-repo/backup/demo/backup.info  |
+--------+----------------------------+-------------------------------------+
```

الآن يمكن تشغيل الأمر `info` بوقت مستهدف سيعرض المستودع كما كان قبل حذفه.

pg-primary **⇒** info بوقت مستهدف

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 19:07:57+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (17): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-190741F
            timestamp start/stop: 2026-10-02 19:07:41+00 / 2026-10-02 19:07:56+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 3.8MB, backup size: 3.8MB
```

إذا عرض الأمر `info` النسخة الاحتياطية المطلوبة فيمكن استعادتها باستخدام الوقت المستهدف نفسه.

pg-primary **⇒** الاستعادة بوقت مستهدف

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 19:07:57+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=1953-a0a01a5a --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/postgresql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 19:07:57+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-190741F, recovery will start at 2026-10-02 19:07:41
P00   INFO: remove invalid files/links/paths from '/var/lib/postgresql/17/demo'
P00   INFO: write updated /var/lib/postgresql/17/demo/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo pg_ctlcluster 17 demo start
```

--------

## مضيف مستودع مخصص {#dedicated-repository-host}

التهيئة الموصوفة في [البدء السريع](#quick-start) مناسبة للتثبيتات البسيطة، لكن في تهيئات المؤسسات من المعتاد أكثر وجود مضيف مستودع مخصص تُخزَّن فيه النسخ الاحتياطية وملفات أرشيف WAL. يفصل هذا النسخ الاحتياطية وأرشيف WAL عن خادم قاعدة البيانات بحيث يكون لأعطال مضيف قاعدة البيانات تأثير أقل. ويظل من الجيد استخدام برمجيات نسخ احتياطي تقليدية لأخذ نسخة احتياطية من مضيف المستودع.

على مضيفات PostgreSQL، يجب أن يكون `pg1-path` هو مسار عنقود PostgreSQL المحلي وألا يُهيَّأ أي `pg1-host`. وعند تهيئة مضيف مستودع، يجب أن يحتوي ملف إعداد pgbackrest على الخيار `pg-host` مهيأ للاتصال بمضيف الأساسي ومضيفات الاستعداد (إن وُجدت). ومضيف المستودع هو الوحيد الذي ينبغي أن يكون إعداد pgbackrest فيه على علم بأكثر من مضيف PostgreSQL. والترتيب لا يهم، فمثلًا يمكن أن يكون pg1-path/pg1-host للأساسي أو للاستعداد وكذلك pg2-path/pg2-host.


### التثبيت {#installation-1}

يُنشأ مضيف جديد باسم repository لتخزين النسخ الاحتياطية للعنقود.

ملاحظة:

يجب أن يطابق إصدار pgBackRest المثبت على مضيف المستودع تمامًا الإصدار المثبت على مضيف PostgreSQL.

يُنشأ المستخدم `pgbackrest` ليكون مالكًا لمستودع pgBackRest. يمكن لأي مستخدم أن يملك المستودع لكن من الأفضل عدم استخدام `postgres` (إن كان موجودًا) تجنبًا للالتباس.

ملاحظة:

عند تثبيت pgBackRest من حزمة، قد تُوفَّر تهيئة logrotate مثل `/etc/logrotate.d/pgbackrest` تدير تدوير السجلات باعتبار مستخدم محدد عبر التوجيه `su` (مثل `su postgres postgres`). وبما أن ملكية الملفات في `/var/log/pgbackrest` تعود إلى المستخدم الذي يشغل pgBackRest (وهو هنا `pgbackrest`)، فيجب تحديث التوجيه `su` ليطابق هذا المستخدم وإلا سيفشل logrotate بخطأ في الصلاحيات.

repository **⇒** إنشاء المستخدم `pgbackrest`

```bash
sudo adduser --disabled-password --gecos "" pgbackrest
```

تثبيت pgBackRest من حزمة أفضل من البناء من المصدر. وعند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. وفي هذه الحالة قد يلزم إنشاء الأدلة يدويًا أو تحديث الصلاحيات.

تتوفر حزم Debian/Ubuntu الخاصة بـ pgBackRest عبر [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

repository **⇒** تثبيت التبعيات

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

repository **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والإعداد وملف إعداد.

repository **⇒** إنشاء ملف إعداد pgBackRest والأدلة

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

### إعداد SSH بدون كلمة مرور {#setup-passwordless-ssh}

يستطيع pgBackRest استخدام SSH بدون كلمة مرور لتمكين التواصل بين المضيفين. ومن الممكن أيضًا استخدام TLS، راجع [إعداد TLS](/ar/pgbackrest/user-guide-rhel/#configuration).

repository **⇒** إنشاء زوج مفاتيح مضيف المستودع

```bash
sudo -u pgbackrest mkdir -m 750 /home/pgbackrest/.ssh
sudo -u pgbackrest ssh-keygen -f /home/pgbackrest/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

pg-primary **⇒** إنشاء زوج مفاتيح مضيف pg-primary

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

تبادَل المفاتيح بين repository وpg-primary.

repository **⇒** نسخ المفتاح العام لـ pg-primary إلى repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-primary cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-primary **⇒** نسخ المفتاح العام لـ repository إلى pg-primary

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

اختبر إمكانية إجراء اتصالات من repository إلى pg-primary وبالعكس.

repository **⇒** اختبار الاتصال من repository إلى pg-primary

```bash
sudo -u pgbackrest ssh postgres@pg-primary
```

pg-primary **⇒** اختبار الاتصال من pg-primary إلى repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

ملاحظة:

هُيّئ ssh بحيث لا يسمح إلا بتشغيل pgBackRest عبر ssh بدون كلمة مرور. يعزز هذا الأمن في حال اختراق أحد حسابات الخدمة.


### التهيئة {#configuration}

يجب تهيئة مضيف المستودع بمضيف/مستخدم pg-primary ومسار قاعدة البيانات. وسيُهيَّأ الأساسي بالاسم `pg1` للسماح بإضافة استعداد لاحقًا.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg1-host`/`pg1-host-user` و`pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

يجب تهيئة مضيف قاعدة البيانات بمضيف/مستخدم المستودع. والقيمة الافتراضية للخيار `repo1-host-user` هي `pgbackrest`. فإذا كان المستخدم `postgres` ينفذ الاستعادات على مضيف المستودع فمن الأفضل ألا يُسمح للمستخدم `postgres` أيضًا بأداء النسخ الاحتياطي. ومع ذلك، يستطيع المستخدم `postgres` قراءة المستودع مباشرة إذا كان في المجموعة نفسها التي للمستخدم `pgbackrest`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `repo1-host`/`repo1-host-user`

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

يمكن الاطلاع على تهيئة PostgreSQL في قسم [تهيئة الأرشفة](#configure-archiving).

تُشغَّل الأوامر بالطريقة نفسها كما في تهيئة المضيف الواحد باستثناء أن بعض الأوامر مثل `backup` و`expire` تُشغَّل من مضيف المستودع بدلًا من مضيف قاعدة البيانات.


### إنشاء الـ stanza والتحقق منه {#create-and-check-stanza}

أنشئ الـ stanza في المستودع الجديد.

repository **⇒** إنشاء الـ stanza

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

تحقق من صحة التهيئة على مضيفي قاعدة البيانات والمستودع معًا. ويمكن الاطلاع على مزيد من المعلومات عن الأمر `check` في [التحقق من التهيئة](#check-the-configuration).

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

repository **⇒** أخذ نسخة احتياطية من العنقود التجريبي

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

ولأنه أُنشئ مستودع جديد على مضيف المستودع فقد صدر التحذير الخاص بتحول النسخة الاحتياطية التزايدية إلى نسخة كاملة.


### استعادة نسخة احتياطية {#restore-a-backup-1}

لاستعادة عنقود PostgreSQL شغّل pgBackRest بالأمر `restore` على مضيف قاعدة البيانات.

pg-primary **⇒** إيقاف العنقود التجريبي واستعادته وإعادة تشغيل PostgreSQL

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo pg_ctlcluster 17 demo start
```

--------

## النسخ الاحتياطي / الاستعادة بالتوازي {#parallel-backup--restore}

يوفر pgBackRest معالجة متوازية لتحسين أداء الضغط والنقل. ويُضبط عدد العمليات المستخدمة لهذه الميزة بالخيار `--process-max`.

من الأفضل عادة عدم استخدام أكثر من 25% من وحدات المعالجة المتاحة للأمر `backup`. فليس من الضروري أن تعمل النسخ الاحتياطية بهذه السرعة ما دامت تُنفَّذ بانتظام، وينبغي ألا تؤثر عملية النسخ الاحتياطي في أداء قاعدة البيانات، إن أمكن على الإطلاق.

يستطيع الأمر restore ويجب أن يستخدم جميع وحدات المعالجة المتاحة لأن عنقود PostgreSQL يكون متوقفًا أثناء الاستعادة ولا يوجد عمومًا عمل مهم آخر يجري على المضيف. فإذا كان المضيف يحتوي على عناقيد متعددة فينبغي أخذ ذلك في الحسبان عند ضبط توازي الاستعادة.

repository **⇒** تنفيذ نسخة احتياطية بعملية واحدة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest لاستخدام عمليات `backup` متعددة

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

repository **⇒** تنفيذ نسخة احتياطية بعمليات متعددة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** الحصول على معلومات النسخ الاحتياطي للعنقود التجريبي

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (17): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-190844F
            timestamp start/stop: 2026-10-02 19:08:44+00 / 2026-10-02 19:08:48+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 29.2MB, database backup size: 29.2MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB

        full backup: 20261002-190850F
            timestamp start/stop: 2026-10-02 19:08:50+00 / 2026-10-02 19:08:52+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 29.2MB, database backup size: 29.2MB
            repo1: backup set size: 3.8MB, backup size: 3.8MB
```

ينبغي أن يكون أداء النسخة الاحتياطية الأخيرة أفضل باستخدام عمليات متعددة. فبالنسبة للنسخ الاحتياطية الصغيرة جدًا قد لا يكون الفرق واضحًا جدًا، لكن مع زيادة حجم قاعدة البيانات تزيد أيضًا وفورات الوقت.


--------

## التشغيل والإيقاف {#starting-and-stopping}

إذا رُقّي استعداد لأغراض الاختبار، أو استُعيد عنقود اختباري من نسخة احتياطية إنتاجية، فمن الجيد منع هذه العناقيد من الكتابة إلى مستودعات pgBackRest. ويمكن تحقيق ذلك بالأمر `stop`.

الأوامر التي تكتب ويحجبها `stop` هي: `archive-push` و`backup` و`expire` و`stanza-create` و`stanza-upgrade`. ولاحظ أن `stanza-delete` استثناء من هذه القاعدة (راجع [حذف الـ stanza](#delete-a-stanza) لمزيد من التفاصيل).

pg-primary **⇒** إيقاف أوامر الكتابة في pgBackRest

```bash
sudo -u postgres pgbackrest stop
```

لن تعمل أوامر الكتابة الجديدة في pgBackRest بعد الآن.

repository **⇒** محاولة أخذ نسخة احتياطية

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

حدد الخيار `--force` لإنهاء أي أوامر كتابة في pgBackRest تعمل حاليًا. ويشمل ذلك archive-get غير المتزامن (مع أنه سيعمل مجددًا إذا طلبه PostgreSQL). فإذا كان pgBackRest متوقفًا بالفعل فإن إيقافه مجددًا سيولد تحذيرًا.

pg-primary **⇒** إيقاف خدمات pgBackRest مجددًا

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

شغّل أوامر الكتابة في pgBackRest مجددًا بالأمر `start`. فلن تبدأ أوامر الكتابة التي كانت قيد التنفيذ قبل الإيقاف تلقائيًا من جديد، لكن يُسمح لها الآن بالبدء.

pg-primary **⇒** تشغيل أوامر الكتابة في pgBackRest

```bash
sudo -u postgres pgbackrest start
```

من الممكن أيضًا إيقاف pgBackRest لكل stanza على حدة.

pg-primary **⇒** إيقاف أوامر الكتابة في pgBackRest للـ stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

لن تعمل أوامر الكتابة الجديدة في pgBackRest للـ stanza المحددة بعد الآن.

repository **⇒** محاولة أخذ نسخة احتياطية

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 ssh protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

يجب أيضًا تحديد الـ stanza عند تشغيل أوامر الكتابة في pgBackRest لكل stanza على حدة.

pg-primary **⇒** تشغيل أوامر الكتابة في pgBackRest للـ stanza `demo`

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## النسخ المتماثل {#replication}

يتيح النسخ المتماثل إنشاء نسخ متعددة من عنقود PostgreSQL (تسمى الاستعدادات) من أساسي واحد. وتفيد الاستعدادات في موازنة عمليات القراءة وتوفير التكرار في حال فشل المضيف الأساسي.


### التثبيت {#installation-2}

يُنشأ مضيف جديد باسم pg-standby لتشغيل الاستعداد.

تثبيت pgBackRest من حزمة أفضل من البناء من المصدر. وعند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. وفي هذه الحالة قد يلزم إنشاء الأدلة يدويًا أو تحديث الصلاحيات.

تتوفر حزم Debian/Ubuntu الخاصة بـ pgBackRest عبر [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-standby **⇒** تثبيت التبعيات

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-standby **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والإعداد وملف إعداد.

pg-standby **⇒** إنشاء ملف إعداد pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### إعداد SSH بدون كلمة مرور {#setup-passwordless-ssh-1}

يستطيع pgBackRest استخدام SSH بدون كلمة مرور لتمكين التواصل بين المضيفين. ومن الممكن أيضًا استخدام TLS، راجع [إعداد TLS](/ar/pgbackrest/user-guide-rhel/#configuration).

pg-standby **⇒** إنشاء زوج مفاتيح مضيف pg-standby

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

تبادَل المفاتيح بين repository وpg-standby.

repository **⇒** نسخ المفتاح العام لـ pg-standby إلى repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-standby cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-standby **⇒** نسخ المفتاح العام لـ repository إلى pg-standby

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

اختبر إمكانية إجراء اتصالات من repository إلى pg-standby وبالعكس.

repository **⇒** اختبار الاتصال من repository إلى pg-standby

```bash
sudo -u pgbackrest ssh postgres@pg-standby
```

pg-standby **⇒** اختبار الاتصال من pg-standby إلى repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

### الاستعداد الساخن {#hot-standby}

ينفذ الاستعداد الساخن النسخ المتماثل باستخدام أرشيف WAL ويسمح باستعلامات القراءة فقط.

تهيئة pgBackRest مشابهة جدًا لتهيئة pg-primary باستثناء أنه سيُستخدم نوع الاسترداد `standby` لإبقاء العنقود في وضع الاسترداد عند بلوغ نهاية تدفق WAL.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest على الاستعداد

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

يجب إنشاء العنقود التجريبي (رغم أنه سيُستبدل عند الاستعادة) لكي تُنشأ ملفات تهيئة PostgreSQL.

pg-standby **⇒** إنشاء العنقود التجريبي

```bash
sudo pg_createcluster 17 demo
```

الآن يمكن إنشاء الاستعداد بالأمر `restore`.

هام:

إذا كان المقصود ترقية العنقود دون أن يصبح الأساسي الجديد (مثلًا لأغراض التقارير أو الاختبار)، فاستخدم `--archive-mode=off` أو اضبط archive_mode=off في `postgresql.conf` لتعطيل الأرشفة. فإذا لم تُعطَّل الأرشفة فقد يتلوث المستودع بـ WAL يمكن أن يجعل الاستعادات أكثر صعوبة.

pg-standby **⇒** استعادة عنقود الاستعداد التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:30
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:56
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_time = '2026-10-02 19:07:12.060959+00'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:10
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 19:07:57+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:37
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:09:08
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

هذه التهيئة تحسبًا لحالة ترقية الاستعداد إلى أساسي.

pg-standby:`/etc/postgresql/17/demo/postgresql.conf` **⇒** تهيئة PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

pg-standby **⇒** تشغيل PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

يعطي سجل PostgreSQL معلومات قيّمة عن الاسترداد. ولاحظ بوجه خاص أن العنقود دخل وضع الاستعداد وأصبح جاهزًا لقبول اتصالات القراءة فقط.

pg-standby **⇒** فحص مخرَج سجل PostgreSQL بحثًا عن رسائل السجل الدالة على النجاح

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 6 lines of output]
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
LOG:  entering standby mode
LOG:  redo starts at 0/24000028
LOG:  restored log file "000000070000000000000025" from archive
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

pg-standby **⇒** الاستعلام عن الجدول الجديد على الاستعداد

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

إذن، ما الذي حدث؟ بما أن PostgreSQL يسحب مقاطع WAL من الأرشيف لأداء النسخ المتماثل، فلن تظهر التغييرات على الاستعداد حتى يُدفع مقطع WAL الذي يحتوي على تلك التغييرات من pg-primary.

يمكن فعل ذلك يدويًا باستدعاء `pg_switch_wal()` التي تدفع مقطع WAL الحالي إلى الأرشيف (ويُنشأ مقطع WAL جديد ليحتوي التغييرات اللاحقة).

pg-primary **⇒** استدعاء `pg_switch_wal()`

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/26019600    | 2026-10-02 19:09:16.993398+00
(1 row)
```

الآن وبعد تأخير قصير سيظهر الجدول على pg-standby.

pg-standby **⇒** الآن يوجد الجدول الجديد على الاستعداد (قد يتطلب بضع محاولات)

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:09:22.793715+00
(1 row)
```

تحقق من تهيئة الاستعداد للوصول إلى المستودع.

pg-standby **⇒** التحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=654-6b53cbe6 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### النسخ المتماثل التدفقي {#streaming-replication}

بدلًا من الاعتماد على أرشيف WAL وحده، يقيم النسخ المتماثل التدفقي اتصالًا مباشرًا بالأساسي ويطبق التغييرات بمجرد حدوثها على الأساسي. وينتج عن ذلك تأخر أقل بكثير بين الأساسي والاستعداد.

يتطلب النسخ المتماثل التدفقي مستخدمًا يتمتع بصلاحية النسخ المتماثل.

pg-primary **⇒** إنشاء مستخدم النسخ المتماثل

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

يجب تحديث الملف `pg_hba.conf` للسماح للاستعداد بالاتصال باعتباره مستخدم النسخ المتماثل. واحرص على استبدال عنوان IP أدناه بعنوان IP الفعلي لـ pg-standby. وستكون هناك حاجة إلى إعادة تحميل بعد تعديل الملف `pg_hba.conf`.

pg-primary **⇒** إنشاء إدخال `pg_hba.conf` لمستخدم النسخ المتماثل

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /etc/postgresql/17/demo/pg_hba.conf'
sudo pg_ctlcluster 17 demo reload
```

يحتاج الاستعداد إلى معرفة كيفية الاتصال بالأساسي لذا سيُهيَّأ إعداد primary_conninfo في pgBackRest.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** ضبط primary_conninfo

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository
```

من الممكن تهيئة كلمة مرور في إعداد primary_conninfo لكن استخدام ملف `.pgpass` أكثر مرونة وأمنًا.

pg-standby **⇒** تهيئة كلمة مرور النسخ المتماثل في ملف `.pgpass`

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/postgresql/.pgpass'
sudo -u postgres chmod 600 /var/lib/postgresql/.pgpass
```

الآن يمكن إنشاء الاستعداد بالأمر `restore`.

pg-standby **⇒** إيقاف PostgreSQL واستعادة عنقود الاستعداد التجريبي

```bash
sudo pg_ctlcluster 17 demo stop
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/postgresql/17/demo/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:30
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:06:56
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:07:16
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_time = '2026-10-02 19:07:12.060959+00'
# Removed by pgBackRest restore on 2026-10-02 19:08:10 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:10
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 19:07:57+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:08:37
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:09:25
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

ملاحظة:

كُتب إعداد primary_conninfo في الملف `postgresql.auto.conf` لأنه هُيّئ باعتباره `recovery-option` في `pgbackrest.conf`. ويمكن استخدام الخيار `--type=preserve` مع `restore` لإبقاء الملف `postgresql.auto.conf` الموجود في مكانه إذا كان هذا السلوك مفضلًا.

pg-standby **⇒** تشغيل PostgreSQL

```bash
sudo pg_ctlcluster 17 demo start
```

سيؤكد سجل PostgreSQL أن النسخ المتماثل التدفقي قد بدأ.

pg-standby **⇒** فحص مخرَج سجل PostgreSQL بحثًا عن رسائل السجل الدالة على النجاح

```bash
sudo -u postgres cat /var/log/postgresql/postgresql-17-demo.log
```

```text
       [filtered 13 lines of output]
LOG:  consistent recovery state reached at 0/25000050
LOG:  database system is ready to accept read-only connections
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

الآن عندما يُنشأ جدول على pg-primary سيظهر على pg-standby بسرعة ودون الحاجة إلى استدعاء `pg_switch_wal()`.

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
 Important Data | 2026-10-02 19:09:32.302145+00
(1 row)
```

pg-standby **⇒** الاستعلام عن الجدول على الاستعداد

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:09:32.491307+00
(1 row)
```

--------

## الـ stanzas المتعددة {#multiple-stanzas}

يدعم pgBackRest تعدد الـ stanzas. والاستخدام الأكثر شيوعًا هو مشاركة مضيف مستودع بين عدة stanzas.


### التثبيت {#installation-3}

يُنشأ مضيف جديد باسم pg-alt لتشغيل الأساسي الجديد.

تثبيت pgBackRest من حزمة أفضل من البناء من المصدر. وعند التثبيت من حزمة لا تكون بقية التعليمات في هذا القسم مطلوبة عمومًا، لكن من الممكن أن تتخطى الحزمة إنشاء أحد الأدلة أو تطبق صلاحيات غير صحيحة. وفي هذه الحالة قد يلزم إنشاء الأدلة يدويًا أو تحديث الصلاحيات.

تتوفر حزم Debian/Ubuntu الخاصة بـ pgBackRest عبر [apt.postgresql.org](https://www.postgresql.org/download/linux/ubuntu/).

إذا لم تُوفَّر حزم لتوزيعتك/إصدارك فيمكنك [البناء من المصدر](#build) ثم التثبيت يدويًا كما هو موضح هنا.

pg-alt **⇒** تثبيت التبعيات

```bash
sudo apt-get install postgresql-client libxml2 libssh2-1
```

pg-alt **⇒** نسخ الملف التنفيذي لـ pgBackRest من مضيف البناء

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

يتطلب pgBackRest أدلة للسجلات والإعداد وملف إعداد.

pg-alt **⇒** إنشاء ملف إعداد pgBackRest والأدلة

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### إعداد SSH بدون كلمة مرور {#setup-passwordless-ssh-2}

يستطيع pgBackRest استخدام SSH بدون كلمة مرور لتمكين التواصل بين المضيفين. ومن الممكن أيضًا استخدام TLS، راجع [إعداد TLS](/ar/pgbackrest/user-guide-rhel/#configuration).

pg-alt **⇒** إنشاء زوج مفاتيح مضيف pg-alt

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/postgresql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/postgresql/.ssh/id_rsa \
       -t rsa -b 4096 -N ""
```

تبادَل المفاتيح بين repository وpg-alt.

repository **⇒** نسخ المفتاح العام لـ pg-alt إلى repository

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@pg-alt cat /var/lib/postgresql/.ssh/id_rsa.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

pg-alt **⇒** نسخ المفتاح العام لـ repository إلى pg-alt

```bash
(echo -n 'no-agent-forwarding,no-X11-forwarding,no-port-forwarding,' && \
       echo -n 'command="/usr/bin/pgbackrest ${SSH_ORIGINAL_COMMAND#* }" ' && \
       sudo ssh root@repository cat /home/pgbackrest/.ssh/id_rsa.pub) | \
       sudo -u postgres tee -a /var/lib/postgresql/.ssh/authorized_keys
```

اختبر إمكانية إجراء اتصالات من repository إلى pg-alt وبالعكس.

repository **⇒** اختبار الاتصال من repository إلى pg-alt

```bash
sudo -u pgbackrest ssh postgres@pg-alt
```

pg-alt **⇒** اختبار الاتصال من pg-alt إلى repository

```bash
sudo -u postgres ssh pgbackrest@repository
```

### التهيئة {#configuration-1}

تهيئة pgBackRest مطابقة تقريبًا لتهيئة pg-primary باستثناء أنه ستُستخدم الـ stanza `demo-alt` بحيث تُخزَّن النسخ الاحتياطية والأرشيف في موقع منفصل.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة pgBackRest على الأساسي الجديد

```ini
[demo-alt]

pg1-path=/var/lib/postgresql/17/demo



[global]

log-level-file=detail

repo1-host=repository
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg1-host`/`pg1-host-user` و`pg1-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

### إعداد العنقود التجريبي {#setup-demo-cluster-1}

pg-alt **⇒** إنشاء العنقود التجريبي

```bash
sudo -u postgres /usr/lib/postgresql/17/bin/initdb \
       -D /var/lib/postgresql/17/demo -k -A peer
sudo pg_createcluster 17 demo
```

```text
Configuring already existing cluster (configuration: /etc/postgresql/17/demo, data: /var/lib/postgresql/17/demo, owner: 102:103)
Ver Cluster Port Status Owner    Data directory              Log file
17  demo    5432 down   postgres /var/lib/postgresql/17/demo /var/log/postgresql/postgresql-17-demo.log
```

pg-alt:`/etc/postgresql/17/demo/postgresql.conf` **⇒** تهيئة إعدادات PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on
```

pg-alt **⇒** تشغيل العنقود التجريبي

```bash
sudo pg_ctlcluster 17 demo restart
```

### إنشاء الـ stanza والتحقق من التهيئة {#create-the-stanza-and-check-configuration}

يجب تشغيل الأمر `stanza-create` لتهيئة الـ stanza إنشائيًا. ويوصى بتشغيل الأمر `check` بعد `stanza-create` لضمان تهيئة الأرشفة والنسخ الاحتياطي بشكل صحيح.

pg-alt **⇒** إنشاء الـ stanza والتحقق من التهيئة

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=386-f644abb9 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=396-8c7be3ca --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000001-ef9bc7e061e42fae1596a4f23d34fdb78ee324d0.gz' on repo1
P00   INFO: check command end: completed successfully
```

إذا شُغِّل الأمر `check` من مضيف المستودع فستُفحص جميع الـ stanzas.

repository **⇒** التحقق من التهيئة لجميع الـ stanzas

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1284-38748c52 --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/000000070000000000000027-f89bb62652ecba95477379768079564b0243a0d3.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/17-1/0000000100000000/000000010000000000000002-de2b6314bf64b956ede5fad9e01f3d5f0200faff.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## الأرشفة غير المتزامنة {#asynchronous-archiving}

تُمكَّن الأرشفة غير المتزامنة بالخيار `archive-async`. يتيح هذا الخيار التشغيل غير المتزامن للأمرين `archive-push` و`archive-get` معًا.

مسار spool مطلوب. ستخزن الأوامر البيانات العابرة هنا لكن طريقة عمل كل أمر مختلفة إلى حد كبير لذا يُوصف استخدام مسار الـ spool بالتفصيل في كل قسم.

pg-primary **⇒** إنشاء دليل الـ spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** إنشاء دليل الـ spool

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

يجب تهيئة مسار الـ spool وتمكين الأرشفة غير المتزامنة. توفر الأرشفة غير المتزامنة تلقائيًا بعض الفائدة بتقليل عدد الاتصالات بالتخزين البعيد، لكن ضبط `process-max` يمكن أن يحسن الأداء تحسينًا جذريًا بموازاة العمليات. واحرص على ألا تضبط `process-max` بقيمة مرتفعة حد التأثير في عمليات قاعدة البيانات العادية.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار الـ spool والأرشفة غير المتزامنة

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة مسار الـ spool والأرشفة غير المتزامنة

```ini
[demo]

pg1-path=/var/lib/postgresql/17/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

ملاحظة:

هُيّئ `process-max` باستخدام أقسام الأوامر بحيث لا يستخدمه backup وrestore. ويسمح هذا أيضًا بقيم مختلفة لـ `archive-push` و`archive-get`.

لأغراض العرض التوضيحي سيُكسر النسخ المتماثل التدفقي لإجبار PostgreSQL على أخذ WAL باستخدام restore_command.

pg-primary **⇒** كسر النسخ المتماثل التدفقي بتغيير كلمة مرور النسخ المتماثل

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** إعادة تشغيل الاستعداد لكسر الاتصال

```bash
sudo pg_ctlcluster 17 demo restart
```

### الدفع إلى الأرشيف {#archive-push}

ينقل الأمر `archive-push` غير المتزامن أرشفة WAL إلى عملية منفصلة (أو عمليات) لتحسين الإنتاجية. ويعمل عبر «الاستباق» لرؤية مقاطع WAL الجاهزة للأرشفة إلى ما بعد الطلب الذي يقدمه PostgreSQL حاليًا عبر `archive_command`. وتُنقل مقاطع WAL إلى الأرشيف مباشرة من الدليل `pg_xlog`/`pg_wal` ولا يُعيد `archive_command` النجاح إلا بعد تخزين مقطع WAL بأمان في الأرشيف.

يحتفظ مسار الـ spool بالحالة الحالية لأرشفة WAL. وملفات الحالة المكتوبة في دليل الـ spool صفرية الطول عادةً وينبغي أن تستهلك مقدارًا ضئيلًا من المساحة (بضعة ميغابايت على الأكثر) وقليلًا جدًا من الإدخال/الإخراج. ويمكن إعادة إنشاء جميع المعلومات في هذا الدليل لذا ليس من الضروري الحفاظ على دليل الـ spool إذا نُقل العنقود إلى عتاد جديد.

هام:

في التنفيذ الأصلي للأرشفة غير المتزامنة، كانت مقاطع WAL تُنسخ إلى دليل الـ spool قبل الضغط والنقل. أما التنفيذ الجديد فينسخ WAL مباشرة من الدليل `pg_xlog`. فإذا كانت الأرشفة غير المتزامنة مستخدمة في v1.12 أو قبلها فاقرأ ملاحظات إصدار v1.13 بعناية قبل الترقية.

يمكن استخدام الملف `[stanza]-archive-push-async.log` لمراقبة نشاط العملية غير المتزامنة. وطريقة جيدة لاختبار ذلك هي دفع عدد من مقاطع WAL بسرعة.

pg-primary **⇒** اختبار الأرشفة غير المتزامنة بالتوازي

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
P00   INFO: check command begin 2.59.3: --exec-id=2590-c51c0441 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --repo1-host=repository --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/17-1/0000000700000000/00000007000000000000002D-1ed494e7471557cb0563baa2af44d9e1252e424f.gz' on repo1
P00   INFO: check command end: completed successfully
```

الآن سيحتوي ملف السجل على نشاط متوازٍ غير متزامن.

pg-primary **⇒** التحقق من النتائج في السجل

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2576-267f2388 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/postgresql/17/demo/pg_wal] --archive-async --exec-id=2594-5115f5d8 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00   INFO: archive-push:async command end: completed successfully
```

### الجلب من الأرشيف {#archive-get}

يحافظ الأمر `archive-get` غير المتزامن على قائمة انتظار محلية لـ WAL لتحسين الإنتاجية. فإذا لم يُعثر على مقطع WAL في قائمة الانتظار جُلب من المستودع مع قدر كافٍ من WAL المتتالي لملء قائمة الانتظار. ويحدد `archive-get-queue-max` الحجم الأقصى لقائمة الانتظار. وكلما كانت قائمة الانتظار أقل من نصف ممتلئة جُلب المزيد من WAL لملئها.

التشغيل غير المتزامن أنفع ما يكون في البيئات التي تولد قدرًا كبيرًا من WAL أو ذات اتصال عالي زمن الاستجابة بتخزين المستودع (أي S3 أو غيره من مخازن الكائنات). وفي حالة الاتصال عالي زمن الاستجابة قد تكون زيادة `process-max` فكرة جيدة.

يمكن استخدام الملف `[stanza]-archive-get-async.log` لمراقبة نشاط العملية غير المتزامنة.

pg-standby **⇒** التحقق من النتائج في السجل

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=871-5afe1731 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P02 DETAIL: found 000000070000000000000025 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000024 in the repo1: 17-1 archive
P02 DETAIL: found 000000070000000000000026 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000027 in the repo1: 17-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00   INFO: archive-get:async command end: completed successfully
       [filtered 14 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=924-87ccaa43 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/postgresql/17/demo --process-max=2 --repo1-host=repository --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P02 DETAIL: found 000000070000000000000029 in the repo1: 17-1 archive
P01 DETAIL: found 000000070000000000000028 in the repo1: 17-1 archive
P02 DETAIL: found 00000007000000000000002A in the repo1: 17-1 archive
P01 DETAIL: found 00000007000000000000002B in the repo1: 17-1 archive
P02 DETAIL: found 00000007000000000000002C in the repo1: 17-1 archive
P01 DETAIL: found 00000007000000000000002D in the repo1: 17-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00   INFO: archive-get:async command end: completed successfully
       [filtered 15 lines of output]
```

pg-primary **⇒** إصلاح النسخ المتماثل التدفقي بتغيير كلمة مرور النسخ المتماثل

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## النسخ الاحتياطي من الاستعداد {#backup-from-a-standby}

يستطيع pgBackRest تنفيذ النسخ الاحتياطية على الاستعداد بدلًا من الأساسي. تتطلب النسخ الاحتياطية من الاستعداد تهيئة المضيف pg-standby وتمكين الخيار `backup-standby`. فإذا هُيّئ أكثر من استعداد واحد فسيُستخدم للنسخ الاحتياطي أول استعداد قيد التشغيل يُعثر عليه.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** تهيئة `pg2-host`/`pg2-host-user` و`pg2-path`

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/17/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/17/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

كلٌّ من قاعدتي بيانات الأساسي والاستعداد مطلوب لأداء النسخ الاحتياطي، مع أنه ستُنسخ الغالبية العظمى من الملفات من الاستعداد لتقليل الحمل على الأساسي. ويمكن تهيئة مضيفي قاعدة البيانات بأي ترتيب. فسيحدد pgBackRest تلقائيًا أيهما الأساسي وأيهما الاستعداد.

repository **⇒** أخذ نسخة احتياطية من العنقود التجريبي من pg2

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
P03 DETAIL: backup file pg-standby:/var/lib/postgresql/17/demo/base/5/2658 (128KB, 8.47%) checksum 6bcdcabc7aaf3e4919655612f77833a1612baf01
P01 DETAIL: backup file pg-primary:/var/lib/postgresql/17/demo/global/pg_control (8KB, 8.99%) checksum aa003dff0afea4b06a88d00138da8e948a563345
P04 DETAIL: backup file pg-standby:/var/lib/postgresql/17/demo/base/5/1247 (120KB, 16.93%) checksum fa2fb6657bf9785e320a8a5516851de78d7a7a33
P01 DETAIL: match file from prior backup pg-primary:/var/lib/postgresql/17/demo/pg_logical/replorigin_checkpoint (8B, 16.93%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1277 lines of output]
```

تُظهر هذه النسخة الاحتياطية التزايدية أن معظم الملفات منسوخة من المضيف pg-standby وأن عددًا قليلًا فقط منسوخ من المضيف pg-primary.

ينشئ pgBackRest نسخة احتياطية من الاستعداد مطابقة للنسخة الاحتياطية المنفذة على الأساسي. ويفعل ذلك ببدء/إيقاف النسخ الاحتياطي على المضيف pg-primary، ونسخ الملفات التي يشملها النسخ المتماثل فقط من المضيف pg-standby، ثم نسخ الملفات القليلة المتبقية من المضيف pg-primary. وهذا يعني أن السجلات والإحصاءات من قاعدة البيانات الأساسية ستُضمَّن في النسخة الاحتياطية.


--------

## ترقية PostgreSQL {#upgrading-postgresql}

فور ترقية PostgreSQL إلى إصدار رئيسي أحدث، يجب ضبط `pg-path` في جميع تهيئات pgBackRest على موقع قاعدة البيانات الجديد وتشغيل الأمر `stanza-upgrade`. فإذا كان هناك أكثر من مستودع مهيأ على المضيف فستُرقَّى الـ stanza على كل منها. وإذا كانت قاعدة البيانات متوقفة عن العمل فاستخدم الخيار `--no-online`.

التعليمات التالية ليست دليلًا شاملًا لترقية PostgreSQL، بل تحدد الخطوط العريضة للعملية العامة لترقية أساسي واستعداد بقصد عرض الخطوات المطلوبة لإعادة تهيئة pgBackRest. ويوصى بأخذ نسخة احتياطية قبل الترقية.

pg-primary **⇒** إيقاف العنقود القديم

```bash
sudo pg_ctlcluster 17 demo stop
```

أوقف العنقود القديم على الاستعداد لأنه سيُستعاد من العنقود المرقى حديثًا.

pg-standby **⇒** إيقاف العنقود القديم

```bash
sudo pg_ctlcluster 17 demo stop
```

أنشئ العنقود الجديد ونفّذ الترقية.

pg-primary **⇒** إنشاء العنقود الجديد وتنفيذ الترقية

```bash
sudo -u postgres /usr/lib/postgresql/18/bin/initdb \
       -D /var/lib/postgresql/18/demo -k -A peer
sudo pg_createcluster 18 demo
sudo -u postgres sh -c 'cd /var/lib/postgresql && \
       /usr/lib/postgresql/18/bin/pg_upgrade \
       --old-bindir=/usr/lib/postgresql/17/bin \
       --new-bindir=/usr/lib/postgresql/18/bin \
       --old-datadir=/var/lib/postgresql/17/demo \
       --new-datadir=/var/lib/postgresql/18/demo \
       --old-options=" -c config_file=/etc/postgresql/17/demo/postgresql.conf" \
       --new-options=" -c config_file=/etc/postgresql/18/demo/postgresql.conf"'
```

```text
       [filtered 44 lines of output]
Checking for extension updates                                ok
Upgrade Complete
----------------
Some statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

هيّئ إعدادات العنقود الجديد ومنفذه.

pg-primary:`/etc/postgresql/18/demo/postgresql.conf` **⇒** تهيئة PostgreSQL

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on
```

حدّث تهيئة pgBackRest على جميع الأنظمة لتشير إلى العنقود الجديد.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg1-path`

```ini
[demo]

pg1-path=/var/lib/postgresql/18/demo



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg-path`

```ini
[demo]

pg1-path=/var/lib/postgresql/18/demo

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

spool-path=/var/spool/pgbackrest



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** ترقية `pg1-path` و`pg2-path` وتعطيل النسخ الاحتياطي من الاستعداد

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/18/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/18/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```

pg-primary **⇒** نسخ تهيئة hba

```bash
sudo cp /etc/postgresql/17/demo/pg_hba.conf \
       /etc/postgresql/18/demo/pg_hba.conf
```

قبل تشغيل العنقود الجديد، يجب تشغيل الأمر `stanza-upgrade`.

pg-primary **⇒** ترقية الـ stanza

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=3025-70610f0d --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/postgresql/18/demo --repo1-host=repository --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

شغّل العنقود الجديد وتأكد من نجاح تثبيته.

pg-primary **⇒** تشغيل العنقود الجديد

```bash
sudo pg_ctlcluster 18 demo start
```

اختبر التهيئة باستخدام الأمر `check`.

pg-primary **⇒** التحقق من التهيئة

```bash
sudo pg_lsclusters
sudo -u postgres pgbackrest --stanza=demo check
```

أزل العنقود القديم.

pg-primary **⇒** إزالة العنقود القديم

```bash
sudo pg_dropcluster 17 demo
```

ثبّت الملفات التنفيذية الجديدة لـ PostgreSQL على الاستعداد وأنشئ العنقود.

pg-standby **⇒** إزالة العنقود القديم وإنشاء العنقود الجديد

```bash
sudo pg_dropcluster 17 demo
sudo pg_createcluster 18 demo
```

شغّل `check` على مضيف المستودع. التحذير المتعلق بتوقف الاستعداد متوقع لأن عنقود الاستعداد متوقف. ويبين تشغيل هذا الأمر أن خادم المستودع على علم بالاستعداد ومهيأ بشكل صحيح للخادم الأساسي.

repository **⇒** التحقق من التهيئة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 ssh protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

نفّذ نسخة احتياطية كاملة على العنقود الجديد ثم استعد الاستعداد من النسخة الاحتياطية. وسيُغيَّر نوع النسخ الاحتياطي تلقائيًا إلى `full` إذا طُلب `incr` أو `diff`.

repository **⇒** تنفيذ نسخة احتياطية كاملة

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** استعادة عنقود الاستعداد التجريبي

```bash
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
```

pg-standby **⇒** تشغيل PostgreSQL والتحقق من تهيئة pgBackRest

```bash
sudo pg_ctlcluster 18 demo start
sudo -u postgres pgbackrest --stanza=demo check
```

يمكن الآن تمكين النسخ الاحتياطي من الاستعداد بعد أن استُعيد الاستعداد.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** إعادة تمكين النسخ الاحتياطي من الاستعداد

```ini
[demo]

pg1-host=pg-primary

pg1-path=/var/lib/postgresql/18/demo

pg2-host=pg-standby

pg2-path=/var/lib/postgresql/18/demo



[demo-alt]

pg1-host=pg-alt

pg1-path=/var/lib/postgresql/17/demo



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y
```
