---
title: "تحويل مثيل مستقل إلى عنقود Patroni"
linkTitle: "تحويل عنقود قائم"
weight: 140
icon: fa-solid fa-truck-moving
description: "الإجراء الخاص بتحويل بيانات PostgreSQL القائمة إلى عنقود Patroni."
module: [PATRONI]
categories: [مهمة]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
يصف هذا القسم عملية تحويل مثيل PostgreSQL مستقل إلى عنقود Patroni.

لنشر عنقود Patroni دون استخدام مثيل PostgreSQL قائم مسبقًا، راجع [التشغيل والتهيئة](/ar/patroni/readme#running_configuring) بدلاً من ذلك.

--------

## الإجراء {#procedure}

تجد أدناه نظرة عامة على خطوات تحويل عنقود Postgres قائم إلى عنقود يديره Patroni. نفترض في هذه الخطوات أن جميع العقد التي تشكل جزءًا من العنقود القائم قيد التشغيل حاليًا، وأنك *لا* تنوي تغيير تهيئة Postgres أثناء إجراء الترحيل. الخطوات:

1.  أنشئ مستخدمي Postgres كما هو موضح في قسم [المصادقة](/ar/patroni/config/yaml#postgresql_settings) من تهيئة Patroni. يمكنك العثور على أوامر SQL نموذجية لإنشاء المستخدمين في كتلة الشيفرة أدناه، وعليك فيها استبدال أسماء المستخدمين وكلمات المرور وفقًا لبيئتك. إذا كان لديك المستخدمون المعنيون بالفعل، فيمكنك تخطي هذه الخطوة.

    ``` sql
    -- Patroni superuser
    -- Replace PATRONI_SUPERUSER_USERNAME and PATRONI_SUPERUSER_PASSWORD accordingly
    CREATE USER PATRONI_SUPERUSER_USERNAME WITH SUPERUSER ENCRYPTED PASSWORD 'PATRONI_SUPERUSER_PASSWORD';

    -- Patroni replication user
    -- Replace PATRONI_REPLICATION_USERNAME and PATRONI_REPLICATION_PASSWORD accordingly
    CREATE USER PATRONI_REPLICATION_USERNAME WITH REPLICATION ENCRYPTED PASSWORD 'PATRONI_REPLICATION_PASSWORD';

    -- Patroni rewind user, if you intend to enable use_pg_rewind in your Patroni configuration
    -- Replace PATRONI_REWIND_USERNAME and PATRONI_REWIND_PASSWORD accordingly
    CREATE USER PATRONI_REWIND_USERNAME WITH ENCRYPTED PASSWORD 'PATRONI_REWIND_PASSWORD';
    GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO PATRONI_REWIND_USERNAME;
    ```

2.  نفّذ الخطوات التالية على جميع عقد Postgres. نفّذ جميع الخطوات على عقدة واحدة قبل الانتقال إلى العقدة التالية. ابدأ بالعقدة الرئيسية، ثم انتقل إلى كل عقدة استعداد:

    1.  إذا كنت تشغّل Postgres عبر systemd، فعطّل وحدة Postgres في systemd. يُنفَّذ ذلك لأن Patroni يتولى إدارة بدء تشغيل daemon الخاص بـ Postgres وإيقافه.
    2.  أنشئ ملف تهيئة YAML لـ Patroni. يمكنك استخدام [أدوات توليد التهيئة والتحقق منها في Patroni](/ar/patroni/config#validate_generate_config) لذلك.
        - **ملاحظة (خاصة بالعقدة الرئيسية):** إذا كنت تستخدم فتحات نسخ متماثل للنسخ المتماثل بين أعضاء العنقود، فيُوصى بتمكين `use_slots` وضبط فتحات النسخ المتماثل القائمة كفتحات دائمة عبر عنصر التهيئة `slots`. كن واعيًا بأن Patroni ينشئ تلقائيًا فتحات نسخ متماثل للنسخ المتماثل بين الأعضاء، ويحذف فتحات النسخ المتماثل التي لا يتعرف عليها عندما يكون `use_slots` ممكنًا. تتمثل فكرة استخدام الفتحات الدائمة هنا في السماح لفتحاتك القائمة بالبقاء أثناء إجراء الترحيل إلى Patroni. راجع [إعدادات التهيئة الديناميكية](/ar/patroni/config/dynamic#dynamic) للتفاصيل.
    3.  شغّل Patroni باستخدام وحدة خدمة `patroni` في systemd. يكتشف تلقائيًا أن Postgres قيد التشغيل بالفعل ويبدأ في مراقبة المثيل.

3.  سلّم "إجراء بدء التشغيل" الخاص بـ Postgres إلى Patroni. للقيام بذلك تحتاج إلى إعادة تشغيل أعضاء العنقود عبر الأمر [patronictl restart cluster-name member-name](/ar/patroni/patronictl#patronictl_restart_parameters). لتقليل زمن التوقف إلى الحد الأدنى، قد ترغب في تقسيم هذه الخطوة إلى:

    1.  إعادة تشغيل فورية لعقد الاستعداد.
    2.  إعادة تشغيل مجدولة للعقدة الرئيسية ضمن نافذة صيانة.

4.  إذا ضبطت فتحات دائمة في الخطوة `2.2.`، فعليك إزالتها من تهيئة `slots` عبر الأمر [patronictl edit-config cluster-name](/ar/patroni/patronictl#patronictl_edit_config_parameters) بمجرد أن يلحق `restart_lsn` الخاص بالفتحات التي أنشأها Patroni بـ `restart_lsn` الخاص بالفتحات الأصلية للأعضاء المقابلين. بإزالة الفتحات من تهيئة `slots` ستسمح لـ Patroni بحذف الفتحات الأصلية من عنقودك عندما لا تبقى حاجة إليها. تجد أدناه استعلامًا نموذجيًا للتحقق من `restart_lsn` الخاص بفتحتين، لتتمكن من المقارنة بينهما:

    ``` sql
    -- Assume original_slot_for_member_x is the name of the slot in your original
    -- cluster for replicating changes to member X, and slot_for_member_x is the
    -- slot created by Patroni for that purpose. You need restart_lsn of
    -- slot_for_member_x to be >= restart_lsn of original_slot_for_member_x
    SELECT slot_name,
           restart_lsn
    FROM pg_replication_slots
    WHERE slot_name IN (
        'original_slot_for_member_x',
        'slot_for_member_x'
    )
    ```

<a id="major_upgrade"></a>

## ترقية كبرى لإصدار PostgreSQL {#major-upgrade-of-postgresql-version}

إجراء الترقية الكبرى باستخدام `pg_upgrade` هو:

1.  أوقف Patroni
2.  رقِّ الملفات التنفيذية لـ PostgreSQL ونفّذ [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) على العقدة الرئيسية
3.  حدّث patroni.yml
4.  أزل مفتاح initialize من DCS أو امسح حالة العنقود الكاملة من DCS. يمكن تحقيق الخيار الثاني بتنفيذ [patronictl remove cluster-name](/ar/patroni/patronictl#patronictl_remove_parameters). وهذا ضروري لأن عنقود PostgreSQL الجديد يُهيَّأ بواسطة initdb، وهو ما يمنحه معرّف نظام PostgreSQL جديدًا.
5.  إذا مسحت حالة العنقود في الخطوة السابقة، فقد ترغب في نسخ patroni.dynamic.json من دليل البيانات القديم إلى الجديد. سيساعدك ذلك على الاحتفاظ ببعض معاملات PostgreSQL التي كنت قد ضبطتها سابقًا.
6.  شغّل Patroni على العقدة الرئيسية.
7.  رقِّ الملفات التنفيذية لـ PostgreSQL، وحدّث patroni.yml، وامسح data_dir على عقد الاستعداد.
8.  شغّل Patroni على عقد الاستعداد وانتظر اكتمال النسخ المتماثل.

لا يدعم PostgreSQL تشغيل pg_upgrade على عقد الاستعداد. إذا كنت تعرف ما تفعله، فيمكنك تجربة إجراء rsync الموصوف في <https://www.postgresql.org/docs/current/pgupgrade.html> بدلاً من مسح data_dir على عقد الاستعداد. لكن الطريقة الأكثر أمانًا هي ترك Patroni يقوم بالنسخ المتماثل للبيانات نيابةً عنك.

--------

## الأسئلة الشائعة {#faq}

- أثناء بدء تشغيل Patroni، يُبلغ Patroni عن عدم قدرته على الارتباط بمنفذ PostgreSQL.

  عليك التحقق من `listen_addresses` و`port` في `postgresql.conf` ومن `postgresql.listen` في `patroni.yml`. ولا تنسَ أن `pg_hba.conf` يجب أن يسمح بمثل هذا الوصول.

- بعد مطالبة Patroni بإعادة تشغيل العقدة، يعرض PostgreSQL رسالة الخطأ `could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory`

  قد يعني ذلك أمورًا مختلفة تبعًا لطريقة إدارتك لتهيئة PostgreSQL. إذا حددت `postgresql.config_dir`، فإن Patroni يولّد `pg_hba.conf` استنادًا إلى الإعدادات في قسم [bootstrap](/ar/patroni/config/yaml#bootstrap_settings) فقط عند تهيئة عنقود جديد من الصفر. في هذا السيناريو لم يكن `PGDATA` فارغًا، ولذلك لم تحدث أي تهيئة أولية. يجب أن يكون هذا الملف موجودًا مسبقًا.
