---
title: "مرجع سطر الأوامر"
linkTitle: "سطر الأوامر"
weight: 30
description: "صيغة أوامر pgBadger الكاملة، والخيارات، والمدخلات البعيدة، ورموز الإرجاع، والأمثلة"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [مرجع]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## الاستخدام والخيارات {#usage-and-options}

الاستخدام: pgbadger [options] logfile [...]

```text
محلل سجلات PostgreSQL مع تقارير ومخططات مفصلة تمامًا.
```

المعاملات:

```text
قد يكون logfile ملف سجل واحدًا، أو قائمة ملفات، أو أمر صدفة
يعيد قائمة ملفات. إذا أردت تمرير محتوى السجل من stdin
فاستخدم - اسمًا للملف. لاحظ أن المدخل من stdin لن يعمل مع csvlog.
```

الخيارات:

```text
-a | --average minutes : عدد الدقائق لبناء مخططات المتوسط للاستعلامات
                         والاتصالات. الافتراضي 5 دقائق.
-A | --histo-average min: عدد الدقائق لبناء المدرجات التكرارية
                         للاستعلامات. الافتراضي 60 دقيقة.
-b | --begin datetime  : تاريخ/وقت البدء للبيانات المطلوب تحليلها في السجل
                         (طابع زمني أو وقت)
-c | --dbclient host   : التقرير فقط عن إدخالات مضيف العميل المعطى.
-C | --nocomment       : إزالة التعليقات مثل /* ... */ من الاستعلامات.
-d | --dbname database : التقرير فقط عن إدخالات قاعدة البيانات المعطاة.
-D | --dns-resolv      : استبدال عناوين IP للعملاء بأسماء DNS الخاصة بها.
                         حذار أن هذا قد يبطئ pgBadger كثيرًا.
-e | --end datetime    : تاريخ/وقت الانتهاء للبيانات المطلوب تحليلها في السجل
                         (طابع زمني أو وقت)
-E | --explode         : تفكيك التقرير الرئيسي بتوليد تقرير
                         لكل قاعدة بيانات. المعلومات العامة غير المتعلقة بقاعدة
                         بيانات تضاف إلى تقرير قاعدة بيانات postgres.
-f | --format logtype  : القيم الممكنة: syslog, syslog2, stderr, jsonlog,
                         csv, pgbouncer, logplex, rds and redshift. استخدم هذا
                         الخيار عندما لا يستطيع pgBadger كشف تنسيق
                         السجل.
-G | --nograph         : تعطيل المخططات في مخرجات HTML. ممكنة افتراضيًا.
-h | --help            : عرض هذه الرسالة والخروج.
-H | --html-outdir path: المسار إلى الدليل الذي يجب كتابة تقارير HTML فيه
                         في الوضع التزايدي، وتبقى الملفات الثنائية في الدليل
                         المحدد بالخيار -O, --outdir.
-i | --ident name      : اسم البرنامج المستخدم هويةً لـ syslog. الافتراضي: postgres
-I | --incremental     : استخدام الوضع التزايدي، ستولَّد التقارير
                         يوميًا في دليل منفصل، ويجب ضبط --outdir.
-j | --jobs number     : عدد المهام التي تعمل في الوقت نفسه على ملف سجل
                         واحد. تعمل كمهمة واحدة افتراضيًا أو عند العمل مع
                         تنسيق csvlog.
-J | --Jobs number     : عدد ملفات السجلات المطلوب تحليلها بالتوازي. تُعالَج
                         ملفًا واحدًا في كل مرة افتراضيًا.
-l | --last-parsed file: السماح بالتحليل التزايدي للسجلات بتسجيل
                         آخر تاريخ/وقت وآخر سطر حُللا. مفيد إذا أردت مراقبة
                         الأخطاء منذ آخر تشغيل أو إذا أردت تقريرًا
                         واحدًا لكل يوم مع سجل يُدوَّر كل أسبوع.
-L | --logfile-list file: ملف يحوي قائمة ملفات السجلات المطلوب تحليلها.
-m | --maxlength size  : الطول الأقصى للاستعلام، سيقتصر على
                         الحجم المعطى. حجم البتر الافتراضي هو 100000.
-M | --no-multiline    : عدم جمع التعليمات متعددة الأسطر تجنبًا للفضلات
                         لا سيما الأخطاء التي تولد تقريرًا ضخمًا.
-N | --appname name    : التقرير فقط عن إدخالات اسم التطبيق المعطى
-o | --outfile filename: تحديد اسم ملف المخرجات. يعتمد الافتراضي
                         على تنسيق المخرجات: out.html أو out.txt أو out.bin
                         أو out.json. يمكن استخدام هذا الخيار مرات عدة
                         لإخراج عدة تنسيقات. لاستخدام مخرجات json، يجب
                         تثبيت وحدة Perl المسماة JSON::XS، ولتفريغ
                         المخرجات إلى stdout، استخدم - اسمًا للملف.
-O | --outdir path     : الدليل الذي يجب حفظ ملفات المخرجات فيه.
-p | --prefix string   : قيمة log_line_prefix المخصصة لديك كما
                         هي معرفة في postgresql.conf. لا تستخدمها إلا إذا لم تكن
                         تستخدم أحد البادئات القياسية المحددة في وثائق
                         pgBadger، مثل أن تتضمن بادئتك متغيرات إضافية مثل IP
                         العميل أو اسم التطبيق. يجب أن تحوي متتاليات تهريب
                         للوقت (%t أو %m أو %n) وللعمليات (%p أو %c).
                         انظر الأمثلة أدناه.
-P | --no-prettify     : تعطيل منسق تجميل استعلامات SQL.
-q | --quiet           : عدم طباعة أي شيء إلى stdout، ولا حتى شريط
                         تقدم.
-Q | --query-numbering : إضافة ترقيم الاستعلامات إلى المخرجات عند استخدام
                         الخيارين --dump-all-queries أو --normalized-only.
-r | --remote-host ip  : تحديد المضيف الذي يجب تنفيذ أمر cat فيه على
                         ملف السجل البعيد لتحليل الملف محليًا.
-R | --retention N     : عدد الأسابيع المطلوب الاحتفاظ بها في الوضع
                         التزايدي. الافتراضي 0، أي معطل. يستخدم لتحديد عدد الأسابيع
                         المطلوب الاحتفاظ بها في دليل المخرجات. تُزال أدلة الأسابيع والأيام
                         الأقدم تلقائيًا.
-s | --sample number   : عدد نماذج الاستعلامات المطلوب تخزينها. الافتراضي: 3.
-S | --select-only     : التقرير فقط عن استعلامات SELECT.
-t | --top number      : عدد الاستعلامات المطلوب تخزينها/عرضها. الافتراضي: 20.
-T | --title string    : تغيير عنوان صفحة تقرير HTML.
-u | --dbuser username : التقرير فقط عن إدخالات المستخدم المعطى.
-U | --exclude-user username : استبعاد إدخالات المستخدم المحدد من
                         التقرير. يمكن استخدامه مرات عدة.
-v | --verbose         : تمكين الوضع المطول أو وضع التصحيح. معطل افتراضيًا.
-V | --version         : عرض إصدار pgBadger والخروج.
-w | --watch-mode      : الإبلاغ عن الأخطاء فقط كما يمكن أن يفعل logwatch.
-W | --wide-char       : ترميز مخرجات HTML للاستعلامات إلى UTF8 لتجنب
                         رسالة Perl "Wide character in print".
-x | --extension       : تنسيق المخرجات. القيم: text أو html أو bin أو json.
                         الافتراضي: html
-X | --extra-files     : في الوضع التزايدي، السماح لـ pgBadger بكتابة ملفات CSS و
                         JS في دليل المخرجات كملفات منفصلة.
-z | --zcat exec_path  : تحديد المسار الكامل لبرنامج zcat. استخدمه إذا
                         لم يكن zcat أو bzcat أو unzip في مسارك.
-Z | --timezone +/-XX  : تحديد عدد الساعات من GMT للمنطقة الزمنية.
                         استخدمه لضبط التاريخ/الوقت في مخططات JavaScript.
                         يمكن أن تكون القيمة عددًا صحيحًا، مثل: 2، أو عشريًا،
                         مثل: 2.5.
--anonymize            : إخفاء كل القيم الحرفية في الاستعلامات، ومفيد لإخفاء
                         البيانات السرية.
--charset              : يستخدم لضبط ترميز HTML المستخدم.
                         الافتراضي: utf-8.
--command CMD          : الأمر المطلوب تنفيذه لجلب إدخالات السجل على
                         stdin. سيفتح pgBadger أنبوبًا إلى الأمر
                         ويحلل إدخالات السجل التي يولدها الأمر.
--csv-separator        : يستخدم لضبط فاصل حقول CSV، الافتراضي: ,
--day-report YYYY-MM-DD: إنشاء تقرير HTML عن اليوم المحدد.
                         يتطلب أدلة مخرجات تزايديًا ووجود
                         جميع ملفات البيانات الثنائية اللازمة
--disable-autovacuum   : عدم توليد تقرير autovacuum.
--disable-checkpoint   : عدم توليد تقرير checkpoint/restartpoint.
--disable-connection   : عدم توليد تقرير الاتصالات.
--disable-error        : عدم توليد تقرير الأخطاء.
--disable-hourly       : عدم توليد التقرير الساعي.
--disable-lock         : عدم توليد تقرير الأقفال.
--disable-query        : عدم توليد تقارير الاستعلامات (الأبطأ، الأكثر
                         تكرارًا، استعلامات المستخدمين وقواعد البيانات، ...).
--disable-session      : عدم توليد تقرير الجلسات.
--disable-temporary    : عدم توليد تقرير الملفات المؤقتة.
--disable-type         : عدم توليد تقرير الاستعلامات بحسب النوع أو قاعدة
                         البيانات أو المستخدم.
--dump-all-queries     : تفريغ جميع الاستعلامات الموجودة في ملف السجل مع استبدال
                         معاملات الربط المضمنة في الاستعلامات في
                         مواضع العناصر النائبة الخاصة بها.
--dump-raw-csv         : تحليل السجل وتفريغ المعلومات إلى تنسيق
                         CSV. لا تُجرى معالجة أخرى، ولا يوجد تقرير.
--enable-checksum      : يستخدم لإضافة مجموع md5 تحت كل تقرير استعلام.
--exclude-appname name : استبعاد إدخالات اسم التطبيق المحدد من
                         التقرير. مثال: "pg_dump". يمكن استخدامه
                         مرات عدة.
--exclude-client name  : استبعاد إدخالات السجل لعنوان IP للعميل المحدد.
                         يمكن استخدامه مرات عدة.
--exclude-db name      : استبعاد إدخالات قاعدة البيانات المحددة من
                         التقرير. مثال: "postgres". يمكن استخدامه مرات
                         عدة.
--exclude-file filename: مسار الملف الذي يحوي كل تعبير نمطي يستخدم
                         لاستبعاد استعلامات من التقرير. تعبير نمطي واحد في كل
                         سطر.
--exclude-line regex   : استبعاد أي إدخال سجل سيطابق التعبير النمطي
                         المعطى. يمكن استخدامه مرات عدة.
--exclude-query regex  : أي استعلام يطابق التعبير النمطي المعطى سيستبعد
                         من التقرير. مثل: "^(VACUUM|COMMIT)"
                         يمكنك استخدام هذا الخيار مرات عدة.
--exclude-time  regex  : أي طابع زمني يطابق التعبير النمطي المعطى
                         سيستبعد من التقرير. مثال: "2013-04-12 .*"
                         يمكنك استخدام هذا الخيار مرات عدة.
--explain-url URL      : استخدمه لتجاوز عنوان URL لأداة explain
                         الرسومية. الافتراضي: https://explain.depesz.com/
--histogram-query VAL  : استخدام حدود مخصصة للمدرج التكراري لأزمنة الاستعلامات.
                        الحدود الافتراضية بالمللي ثانية:
                     0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: استخدام حدود مخصصة للمدرج التكراري لأزمنة الجلسات.
                        الحدود الافتراضية بالمللي ثانية:
                     0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: مسار الملف الذي يحوي كل تعبير نمطي للاستعلامات
                         المطلوب تضمينها في التقرير. تعبير نمطي واحد في كل
                         سطر.
--include-query regex  : أي استعلام لا يطابق التعبير النمطي المعطى
                         سيستبعد من التقرير. يمكنك استخدام هذا
                         الخيار مرات عدة. مثل: "(tbl1|tbl2)".
--include-pid PID      : التقرير فقط عن الأحداث المتعلقة بـ pid للجلسة (%p).
                         يمكن استخدامه مرات عدة.
--include-session ID   : التقرير فقط عن الأحداث المتعلقة بمعرّف الجلسة (%c).
                         يمكن استخدامه مرات عدة.
--include-time  regex  : لن يضم في التقرير إلا الطوابع الزمنية المطابقة
                         للتعبير النمطي المعطى. مثال: "2013-04-12 .*"
                         يمكنك استخدام هذا الخيار مرات عدة.
--iso-week-number      : في الوضع التزايدي، تبدأ أسابيع التقويم يوم
                         الاثنين وتحترم رقم الأسبوع ISO 8601، ضمن المدى
                         من 01 إلى 53، حيث الأسبوع 1 هو أول أسبوع
                         يضم 4 أيام على الأقل في السنة الجديدة.
--keep-comments        : عدم إزالة التعليقات من الاستعلامات الموحدة نمطيًا. قد
                         يكون ذلك مفيدًا إذا أردت التمييز بين
                         الاستعلامات الموحدة نمطيًا نفسها.
--journalctl command   : الأمر المستخدم لاستبدال ملف سجل PostgreSQL بـ
                         استدعاء journalctl. أساسًا قد يكون:
                            journalctl -u postgresql-9.5
--log-duration         : إجبار pgBadger على ربط إدخالات السجل المولدة
                         بواسطة log_duration = on و log_statement = 'all'
--log-timezone +/-XX   : تحديد عدد الساعات من GMT للمنطقة الزمنية
                         التي يجب استخدامها لضبط التاريخ/الوقت المقروء من
                         ملف السجل قبل تحليله. استخدام هذا الخيار
                         يجعل البحث في السجلات بتاريخ/وقت أكثر صعوبة.
                         يمكن أن تكون القيمة عددًا صحيحًا، مثل: 2، أو عشريًا،
                         مثل: 2.5.
--month-report YYYY-MM : إنشاء تقرير HTML تراكمي عن الشهر
                         المحدد. يتطلب أدلة مخرجات تزايديًا و
                         وجود جميع ملفات البيانات الثنائية اللازمة
--noexplain            : عدم معالجة الأسطر المولدة بواسطة auto_explain.
--no-fork              : عدم تفريع أي عملية، لغرض التصحيح.
--no-process-info      : تعطيل تغيير عنوان العملية للمساعدة على تمييز
                         عملية pgbadger، فبعض الأنظمة لا تدعم ذلك.
--no-progressbar       : تعطيل شريط التقدم.
--noreport             : لن تُنشأ أي تقارير في الوضع التزايدي.
--no-week              : إعلام pgbadger بعدم بناء التقارير الأسبوعية في
                         الوضع التزايدي. مفيد إذا استغرق ذلك وقتًا طويلًا.
--normalized-only      : تفريغ جميع الاستعلامات الموحدة نمطيًا فقط إلى out.txt
--pgbouncer-only       : إظهار القوائم المتعلقة بـ PgBouncer فقط في الترويسة.
--pid-dir path         : تحديد المسار الذي يجب تخزين ملف pid فيه.
                         الافتراضي /tmp
--pid-file file        : تحديد اسم ملف pid لإدارة التنفيذ
                         المتزامن لـ pgBadger. الافتراضي: pgbadger.pid
--pie-limit num        : بيانات المخطط الدائري الأقل من num% ستظهر مجموعًا بدلًا من ذلك.
--prettify-json        : استخدمه إذا أردت تجميل مخرجات json.
--rebuild              : يستخدم لإعادة بناء جميع تقارير html في أدلة المخرجات
                         التزايدي حيث توجد ملفات بيانات ثنائية.
--start-monday         : في الوضع التزايدي، تبدأ أسابيع التقويم يوم
                         الأحد. استخدم هذا الخيار للبدء يوم الاثنين.
--tempdir DIR          : تحديد الدليل الذي ستكتب فيه الملفات المؤقتة
                         الافتراضي: File::Spec->tmpdir() || '/tmp'
```

يستطيع pgBadger تحليل ملف سجل بعيد باستخدام اتصال ssh دون كلمة مرور.
استخدم -r أو --remote-host لتحديد عنوان IP للمضيف أو اسمه. وتوجد أيضًا
بعض الخيارات الإضافية للتحكم الكامل في اتصال ssh.

```text
--ssh-identity file      مسار ملف الهوية المطلوب استخدامه.
--ssh-option  options    قائمة خيارات -o المستخدمة لاتصال ssh.
                         الخيارات المستخدمة دائمًا:
                             -o ConnectTimeout=$ssh_timeout
                             -o PreferredAuthentications=hostbased,publickey
--ssh-port port          منفذ ssh المطلوب استخدامه للاتصال. الافتراضي: 22.
--ssh-program ssh        مسار برنامج ssh المطلوب استخدامه. الافتراضي: ssh.
--ssh-timeout second     مهلة فشل اتصال ssh. الافتراضي: 10 ثوانٍ.
--ssh-user username      اسم دخول الاتصال. الافتراضي هو المستخدم الجاري.
```

يضيف `--ssh-sudo` البادئة `sudo` إلى أوامر سرد الملفات البعيدة وقراءة السجلات. يجب أن يكون مستخدم SSH البعيد قادرًا على تشغيل تلك الأوامر عبر `sudo` دون مطالبة تفاعلية.

يمكن أيضًا تحديد ملف السجل المطلوب تحليله باستخدام URI، والبروتوكولات المدعومة هي
http[s] و[s]ftp. وسيُستخدم الأمر curl لتنزيل الملف، وسيجري
تحليل الملف أثناء التنزيل. بروتوكول ssh مدعوم أيضًا وسيعمل
باستخدام أمر ssh كما في حالة المضيف البعيد. انظر الأمثلة أدناه.

رموز الإرجاع:

```text
0: عند النجاح
1: الانقطاع بسبب خطأ
2: إذا قوطع مثلًا باستخدام ctr+c
3: ملف pid موجود مسبقًا أو تعذر إنشاؤه
4: لم يُعطَ أي ملف سجل في سطر الأوامر
```

أمثلة:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# بادئة سطر السجل مع مخرجات سجل stderr
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# بادئة سطر السجل مع مخرجات سجل syslog
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# استخدام 8 أنوية المعالجة لدي لتحليل ملفي ذي 10GB أسرع، أسرع بكثير
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

استخدم صيغة URI لملف السجل البعيد:

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

يمكنك الجمع بين سجل PostgreSQL محلي وملف سجل pgbouncer بعيد للتحليل:

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

الإبلاغ عن الأخطاء كل أسبوع عبر مهمة cron:

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

توليد تقرير كل أسبوع باستخدام السلوك التزايدي:

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

يفترض هذا أن ملف السجل وتقرير HTML يُدوَّران أيضًا كل أسبوع.

أو الأفضل، استخدم التقارير التزايدية المولَّدة تلقائيًا:

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

سيولِّد هذا تقريرًا لكل يوم ولكل أسبوع.

في الوضع التزايدي، يمكنك أيضًا تحديد عدد الأسابيع التي تُحفظ في
التقارير:

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

إذا كان لديك تشغيل pg_dump عند الساعة 23:00 و13:00 كل يوم لمدة نصف ساعة، فيمكنك
استخدام pgBadger على النحو التالي لاستبعاد هذه الفترات من التقرير:

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

يستبعد هذا التعبير كل ساعة مطابقة بالكامل، بما في ذلك الوقت الواقع خارج نصف ساعة النسخ الاحتياطي. ضيِّق نمط الدقائق إذا كان ينبغي استبعاد فترة النسخ الاحتياطي فقط.

سيساعد هذا في تجنب ظهور عبارات COPY، كما يولدها pg_dump، في أعلى
قائمة أبطأ الاستعلامات. يمكنك أيضًا استخدام --exclude-appname "pg_dump" لحل
هذه المشكلة بطريقة أبسط.

يمكنك أيضًا تحليل مخرجات journalctl وكأنها ملف سجل:

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

أو الأسوأ، استدعاؤه من مضيف بعيد:

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

لا تحتاج إلى تحديد أي ملف سجل في سطر الأوامر، لكن إذا كانت لديك ملفات سجلات
PostgreSQL أخرى تريد تحليلها، فيمكنك إضافتها كالمعتاد.

لإعادة بناء جميع تقارير html التزايدية لاحقًا، اتبع ما يلي:

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

سيحدِّث هذا أيضًا جميع ملفات الموارد (JS وCSS). استخدم -E أو --explode
إذا كانت التقارير قد بُنيت باستخدام هذا الخيار.

يدعم pgBadger أيضًا سجلات Heroku PostgreSQL بصيغة logplex:

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

سيقوم هذا ببث سجل Heroku PostgreSQL إلى pgbadger عبر stdin.

يستطيع pgBadger الكشف تلقائيًا عن سجلات RDS وcloudwatch الخاصة بـ PostgreSQL
بصيغة rds:

```text
pgbadger -f rds -o rds_out.html rds.log
```

كل سجل CloudSQL Postgresql هو سجل PostgreSQL عادي إلى حد كبير، لكنه مغلف
بصيغة JSON. يكتشفه pgBadger تلقائيًا، لكن في حال احتجت إلى فرض
صيغة السجل فاستخدم `jsonlog`:

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

الحال هنا كحال امتداد jsonlog؛ صيغة json مختلفة،
لكن pgBadger يستطيع تحليل الصيغتين كلتيهما.

يدعم pgBadger أيضًا السجلات التي ينتجها مشغِّل CloudNativePG Postgres لـ Kubernetes:

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

لإنشاء تقرير تراكمي على مدار شهر استخدم الأمر:

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

سيضيف هذا رابطًا إلى اسم الشهر في عرض التقويم الخاص بالتقارير
التزايدية للاطلاع على تقرير شهر مايو 2019.
استخدم -E أو --explode إذا كانت التقارير قد بُنيت باستخدام هذا الخيار.
