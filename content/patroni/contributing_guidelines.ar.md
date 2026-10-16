---
title: "إرشادات المساهمة"
linkTitle: "المساهمة"
weight: 200
icon: fa-solid fa-users
description: "سير عمل المساهمة وقنوات الدعم وإرشادات التطوير."
module: [PATRONI]
categories: [مهمة]
upstream_link: "https://patroni.readthedocs.io/en/latest/contributing_guidelines.html"
---

<a id="contributing_guidelines"></a>

--------

## الدردشة {#chatting}

إذا كان لديك سؤال، أو كنت تبحث عن مساعدة تفاعلية في استكشاف الأخطاء وإصلاحها، أو أردت الدردشة مع مستخدمي Patroni الآخرين، فانضم إلينا في القناة [\#patroni](https://postgresteam.slack.com/archives/C9XPYG92A) في [PostgreSQL Slack](https://pgtreats.info/slack-invite).

<a id="reporting_bugs"></a>

--------

## الإبلاغ عن الأخطاء {#reporting-bugs}

قبل الإبلاغ عن خطأ يرجى التأكد من **إعادة إنتاجه مع أحدث إصدار من Patroni**! كما يرجى التحقق مرة أخرى مما إذا كانت المشكلة موجودة بالفعل في [متتبع المشكلات](https://github.com/patroni/patroni/issues) لدينا.

--------

## تشغيل الاختبارات {#running-tests}

متطلبات تشغيل اختبارات behave:

1.  يلزم تثبيت حزم PostgreSQL بما فيها وحدات [contrib](https://www.postgresql.org/docs/current/contrib.html).
2.  يجب أن تكون ملفات PostgreSQL الثنائية متوفرة في `PATH` لديك. قد تحتاج إلى إضافتها إلى المسار بشيء مثل `PATH=/usr/lib/postgresql/11/bin:$PATH python -m behave`.
3.  إذا أردت الاختبار مع DCS خارجية (مثل Etcd وConsul وZookeeper) فستحتاج إلى تثبيت الحزم وتشغيل الخدمات المقابلة وقبولها اتصالات غير مشفرة/غير محمية على localhost والمنفذ الافتراضي. في حالة Etcd أو Consul، يمكن لمجموعة اختبارات behave بدء تشغيلها إذا كانت الملفات الثنائية متوفرة في `PATH`.

ثبّت التبعيات:

``` bash
# You may want to use Virtualenv or specify pip3.
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

بعد تثبيت جميع التبعيات، يمكنك تشغيل مجموعات الاختبارات المختلفة:

``` bash
# You may want to use Virtualenv or specify python3.

# Run flake8 to check syntax and formatting:
python setup.py flake8

# Run the pytest suite in tests/:
python setup.py test

# Moreover, you may want to run tests in different scopes for debugging purposes,
# the -s option include print output during test execution.
# Tests in pytest typically follow the pattern: FILEPATH::CLASSNAME::TESTNAME.
pytest -s tests/test_api.py
pytest -s tests/test_api.py::TestRestApiHandler
pytest -s tests/test_api.py::TestRestApiHandler::test_do_GET

# Run the behave (https://behave.readthedocs.io/en/latest/) test suite in features/;
# modify DCS as desired (raft has no dependencies so is the easiest to start with):
DCS=raft python -m behave
```

--------

## الاختبار باستخدام tox {#testing-with-tox}

لتشغيل اختبارات tox تحتاج فقط إلى تثبيت تبعية واحدة (غير Python)

``` bash
pip install "tox>=4"
```

إذا كنت ترغب في تشغيل اختبارات `behave` القائمة على Docker فستحتاج أيضًا إلى تثبيت Docker.

تهيئة Tox في `tox.ini` تحتوي على "بيئات" لتشغيل المهام التالية:

- lint: فحص كود Python مع `flake8`
- test: اختبارات الوحدة لجميع مفسرات python المتاحة مع `pytest`، وتوليد تقارير HTML إذا اكتُشف TTY، وإلا تقارير XML
- dep: اكتشاف تعارضات تبعيات الحزمة باستخدام `pipdeptree`
- type: الفحص النوعي الساكن مع `pyright`
- black: تنسيق الكود مع `black`
- docker-build: بناء صورة docker المستخدمة لبيئة `behave`
- docker-cmd: تشغيل أي أمر تختاره بالصورة أعلاه
- docker-behave-etcd: تشغيل tox لاختبارات behave بالصورة أعلاه
- py\*behave: تشغيل behave بمفسرات python المتاحة (دون docker، ومع أن هذا هو ما يُستدعى داخل حاويات docker)
- docs: بناء الوثائق مع `sphinx`

### تشغيل tox {#running-tox}

لتشغيل قائمة البيئات الافتراضية؛ dep وlint وtest وdocs، فقط شغّل:

``` bash
tox
```

يمكن تشغيل بيئات `test` بالتسمية `test`:

``` bash
tox -m test
```

يمكن تشغيل اختبارات `behave` الخاصة بـ docker بالتسمية `behave`:

``` bash
tox -m behave
```

وبالمثل، فلـ docs التسمية `docs`.

يمكن تشغيل جميع البيئات الأخرى بأسماء البيئات الخاصة بها:

``` bash
tox -e lint
tox -e py39-test-lin
```

من الممكن أيضًا اختيار قوائم بيئات جزئية باستخدام `factors`. مثلًا، إذا أردت تشغيل جميع البيئات لـ python 3.10:

``` bash
tox -f py310
```

هذا مكافئ لتشغيل جميع البيئات المدرجة أدناه:

``` bash
$ tox -l -f py310
py310-test-lin
py310-test-mac
py310-test-win
py310-type-lin
py310-type-mac
py310-type-win
py310-behave-etcd-lin
py310-behave-etcd-win
py310-behave-etcd-mac
py310-behave-etcd3-lin
py310-behave-etcd3-win
py310-behave-etcd3-mac
```

يمكنك عرض جميع مجموعات البيئات المهيأة مع tox (\>=v4) هكذا

``` bash
tox l
```

ستحاول بيئتا `test` و`docs` فتح ملفات مخرجات HTML عند اكتمال المهمة، إذا شُغّل tox مع طرفية نشطة. هذا مقصود لمنفعة المطوّر الذي يشغّل هذه البيئة محليًا. سيحاول تشغيل `open` على mac و`xdg-open` على Linux. لاستخدام أمر مختلف اضبط متغير البيئة `OPEN_CMD` على اسم الأمر أو مساره. إذا فشلت هذه الخطوة فلن تفشل عملية التشغيل ككل. إذا أردت تعطيل هذه الميزة فاضبط متغير البيئة `OPEN_CMD` على أمر عدم التنفيذ `:`.

``` bash
OPEN_CMD=: tox -m docs
```

### اختبارات behave {#behave-tests}

اختبارات behave مع `-m behave` ستبني صور docker بناءً على إصدار PG_MAJOR من 12 حتى 18 ثم تشغّل جميع اختبارات behave. قد يستغرق ذلك وقتًا طويلًا للتشغيل لذا قد ترغب في حصر النطاق على إصدار معين من Postgres أو على مجموعة ميزات أو خطوات محددة.

لتحديد إصدار postgres ضمّن الاسم الكامل لبيئة بناء الصورة التابعة التي تريدها ثم اسم بيئة behave. مثلًا إذا أردت Postgres 14 فاستخدم:

``` bash
tox -e pg14-docker-build,pg14-docker-behave-etcd-lin
```

أما إذا أردت اختبار ميزة محددة فيمكنك تمرير وسائط موضعية إلى behave. سيشغّل هذا سيناريو اختبار ميزة المراقب (watchdog) في behave مع جميع إصدارات Postgres.

``` bash
tox -m behave -- features/watchdog.feature
```

بالطبع يمكنك الجمع بين الاثنين.

--------

## المساهمة بطلب سحب {#contributing-a-pull-request}

1.  انسخ المستودع (fork)، وطوّر تغييرات الكود واختبرها.
2.  اعكس التغييرات في وثائق المستخدم.
3.  أرسل طلب سحب مع وصف واضح لهدف التغييرات. اربط مشكلة موجودة إذا لزم الأمر.

ستتلقى ملاحظات حول طلب السحب في أقرب وقت ممكن.

نتمنى لك تطويرًا ممتعًا لـ Patroni ;-)
