---
title: "التكامل مع أدوات أخرى"
linkTitle: "تكامل الأدوات"
weight: 150
icon: fas fa-puzzle-piece
description: "تكامل Patroni مع أدوات النسخ الاحتياطي والتنسيق الخارجية."
module: [PATRONI]
categories: [مفهوم]
upstream_link: "https://patroni.readthedocs.io/en/latest/tools_integration.html"
---

<a id="tools_integration"></a>
يستطيع Patroni التكامل مع أدوات أخرى في مجموعتك التقنية. في هذا القسم ستجد قائمة أمثلة، وهي وإن لم تكن قائمة شاملة، فقد تزودك بأفكار حول كيفية تكامل Patroni مع أدوات أخرى.

--------

## Barman {#barman}

يوفر Patroni تطبيقًا باسم `patroni_barman` يتضمن منطقًا للتواصل مع `pg-backup-api`، بحيث تستطيع تنفيذ عمليات Barman عن بُعد.

يحتوي هذا التطبيق حاليًا على اثنين من الأوامر الفرعية: `recover` و`config-switch`.

### patroni_barman recover {#patroni_barman-recover}

يمكن استخدام الأمر الفرعي `recover` كطريقة تهيئة أولية مخصصة أو كطريقة إنشاء نسخة متماثلة مخصصة. يمكنك العثور على مزيد من المعلومات حول ذلك في [replica_imaging_and_bootstrap](/ar/patroni/replica_bootstrap#replica_imaging_and_bootstrap).

### patroni_barman config-switch {#patroni_barman-config-switch}

صُمم الأمر الفرعي `config-switch` ليُستخدم كاستدعاء راجع (callback) `on_role_change` في Patroni. على سبيل المثال، افترض أنك تبث سجلات WAL من أساسيك الحالي إلى مضيف Barman لديك. في حالة حدوث تجاوز أعطال في العنقود قد ترغب في بدء بث سجلات WAL من الأساسي الجديد. يمكنك تحقيق ذلك باستخدام `patroni_barman config-switch` كاستدعاء `on_role_change` الراجع.

> [!NOTE]
> يعتمد ذلك الأمر الفرعي على أمر `barman config-switch`، وهو المسؤول عن تجاوز إعداد خادم Barman بتطبيق نموذج معرّف مسبقًا فوقه. يتوفر هذا الأمر منذ Barman 3.10. فضلًا راجع وثائق Barman لمزيد من التفاصيل.

هذا مثال على كيفية إعداد Patroni لتطبيق نموذج إعداد في حال ترقية عقدة Patroni هذه إلى أساسي:

```yaml
postgresql:
    callbacks:
        on_role_change: >
            patroni_barman
                --api-url YOUR_API_URL
                config-switch
                --barman-server YOUR_BARMAN_SERVER_NAME
                --barman-model YOUR_BARMAN_MODEL_NAME
                --switch-when promoted
```

> [!NOTE]
> يتطلب `patroni_barman config-switch` أن يكون كلٌّ من Barman و`pg-backup-api` مضبوطين على مضيف Barman، ليتمكن من تنفيذ `barman config-switch` عن بُعد عبر واجهة برمجة تطبيقات النسخ الاحتياطي. كما يتطلب أن تكون نماذج Barman المطلوب تطبيقها مضبوطة مسبقًا. يستخدم المثال أعلاه مجموعة فرعية من المعاملات المتاحة. يمكنك الحصول على مزيد من المعلومات بتشغيل `patroni_barman config-switch --help`، وبمراجعة وثائق Barman.
