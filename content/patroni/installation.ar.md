---
title: "التثبيت"
weight: 20
icon: fa-solid fa-cloud-arrow-down
description: "تعليمات تثبيت Patroni وترقيته عبر المنصات المدعومة."
module: [PATRONI]
categories: [درس تعليمي]
upstream_link: "https://patroni.readthedocs.io/en/latest/installation.html"
---

<a id="installation"></a>

--------

## المتطلبات المسبقة لنظام Mac OS {#pre-requirements-for-mac-os}

لتثبيت المتطلبات على جهاز Mac، شغّل ما يلي:

```bash
brew install postgresql etcd haproxy libyaml python
```

<a id="psycopg2_install_options"></a>

--------

## Psycopg {#psycopg}

بدءًا من [psycopg2-2.8](https://www.psycopg.org/articles/2019/04/04/psycopg-28-released/) لن تُثبَّت النسخة الثنائية من psycopg2 افتراضيًا بعد الآن. ويتطلب تثبيتها من الشيفرة المصدرية مترجم C وحزم تطوير postgres+python. وبما أنه في عالم python لا يمكن تحديد التبعية بصيغة `psycopg2 OR psycopg2-binary`، فسيكون عليك أن تقرر كيفية تثبيتها.

هناك بعض الخيارات المتاحة:

1.  استخدم مدير الحزم الخاص بتوزيعتك

```bash
sudo apt-get install python3-psycopg2  # install psycopg2 module on Debian/Ubuntu
sudo yum install python3-psycopg2      # install psycopg2 on RedHat/Fedora/CentOS
```

2.  حدد أحد `psycopg3` أو `psycopg2` أو `psycopg2-binary` في [قائمة التبعيات](/ar/patroni/installation#extras) عند تثبيت Patroni باستخدام pip.

<a id="extras"></a>

--------

## التثبيت العام عبر pip {#general-installation-for-pip}

يمكن تثبيت Patroni باستخدام pip:

```bash
pip install patroni[dependencies]
```

حيث يمكن أن تكون `dependencies` فارغة، أو أن تتكون من واحد أو أكثر مما يلي:

etcd or etcd3  
وحدة `python-etcd` لاستخدام Etcd كمخزن إعداد موزع (DCS)

consul  
وحدة `py-consul` لاستخدام Consul كـ DCS

zookeeper  
وحدة `kazoo` لاستخدام Zookeeper كـ DCS

exhibitor  
وحدة `kazoo` لاستخدام Exhibitor كـ DCS (نفس التبعيات الخاصة بـ Zookeeper)

kubernetes  
وحدة [kubernetes](/ar/patroni/kubernetes#kubernetes) لاستخدام Kubernetes كـ DCS في Patroni

raft  
وحدة `pysyncobj` لاستخدام تنفيذ Raft بلغة python كـ DCS

aws  
`boto3` لاستخدام استدعاءات AWS الرجعية

jsonlogger  
وحدة `python-json-logger` لتمكين [تسجيل السجلات](/ar/patroni/config/yaml#log_settings) بصيغة json

systemd  
`systemd-python` لاستخدام تكامل sd_notify

all  
جميع ما سبق (باستثناء عائلة psycopg)

psycopg3  
وحدة `psycopg[binary]>=3.0.0`

psycopg2  
وحدة `psycopg2>=2.5.4`

psycopg2-binary  
وحدة `psycopg2-binary`

على سبيل المثال، الأمر اللازم لتثبيت Patroni مع psycopg3 وتبعيات Etcd كـ DCS واستدعاءات AWS الرجعية هو:

```bash
pip install patroni[psycopg3,etcd3,aws]
```

لاحظ أن الأدوات الخارجية التي تُستدعى في سكربتات إنشاء النسخ المتماثلة أو التهيئة الأولية المخصصة (أي WAL-E) يجب تثبيتها بشكل مستقل عن Patroni.

<a id="package_installation"></a>

--------

## التثبيت من الحزم على Linux {#package-installation-on-linux}

قد تتوفر حزم Patroni لنظام التشغيل الخاص بك، ينتجها مجتمع Postgres من أجل:

- RHEL وRockyLinux وAlmaLinux؛
- Debian وUbuntu؛
- SUSE Enterprise Linux.

يمكنك أيضًا العثور على حزم للتبعيات المباشرة لـ Patroni، مثل وحدات python التي قد لا تكون متوفرة في مستودعات نظام التشغيل الرسمية.

لمزيد من المعلومات راجع وثائق [مستودع PGDG](https://www.postgresql.org/download/linux/).

إذا كنت تستخدم نظام تشغيل مشتقًا من RedHat Enterprise Linux فقد تحتاج أيضًا إلى حزم من EPEL، راجع وثائق [مستودع EPEL](https://docs.fedoraproject.org/en-US/epel/).

بعد تثبيت مستودع PGDG لنظام التشغيل الخاص بك يمكنك تثبيت patroni.

> [!NOTE]
> لا تُصان حزم Patroni من قبل مطوري Patroni، بل من قبل مجتمع Postgres. إذا كنت بحاجة إلى دعم فجرّب أولًا التواصل عبر [Postgres slack](http://pgtreats.info/slack-invite).

### التثبيت على الأنظمة المشتقة من Debian {#installing-on-debian-derivatives}

مع تثبيت مستودع PGDG (راجع [أعلاه](/ar/patroni/installation#package_installation))، ثبّت Patroni عبر apt بتنفيذ:

```bash
apt-get install patroni
```

### التثبيت على الأنظمة المشتقة من RedHat {#installing-on-redhat-derivatives}

مع تثبيت مستودع PGDG (راجع [أعلاه](/ar/patroni/installation#package_installation))، ثبّت patroni مع DCS من نوع etcd عبر dnf على RHEL 9 (والمشتقات) بتنفيذ:

```bash
dnf install patroni patroni-etcd
```

يمكنك تثبيت etcd من PGDG إذا كانت توزيعتك المشتقة من RedHat لا توفر الحزم. على العقد التي ستستضيف DCS نفّذ:

```bash
dnf install 'dnf-command(config-manager)'
dnf config-manager --enable pgdg-rhel9-extras
dnf install etcd
```

يمكنك استبدال إصدار RHEL بـ `8` في المستودع للحصول على `pgdg-rhel8-extras` إذا لزم الأمر. ولا يزال اسم المستودع `pgdg-rhelN-extras` على RockyLinux وAlmaLinux وOracle Linux وغيرها...

### التثبيت على SUSE Enterprise Linux {#installing-on-suse-enterprise-linux}

قد تحتاج إلى تمكين مستودعات SUSE PackageHub لبعض التبعيات. راجع وثائق [SUSE PackageHub](https://packagehub.suse.com/how-to-use/).

بالنسبة إلى SLES 15 مع تثبيت مستودع PGDG (راجع [أعلاه](/ar/patroni/installation#package_installation))، يمكنك تثبيت patroni باستخدام:

```bash
zypper install patroni patroni-etcd
```

مع تمكين مستودع SUSE PackageHub يمكنك أيضًا تثبيت etcd:

```bash
SUSEConnect -p PackageHub/15.5/x86_64
zypper install etcd
```

--------

## الترقية {#upgrading}

ترقية patroni عملية بسيطة جدًا؛ حدّث تثبيت البرنامج فقط وأعد تشغيل daemon الخاص بـ Patroni على كل عقدة في العنقود.

غير أن إعادة تشغيل daemon الخاص بـ Patroni ستؤدي إلى إعادة تشغيل قاعدة بيانات Postgres. وفي بعض الحالات قد يتسبب ذلك في حدوث تجاوز أعطال للعقدة الرئيسية في عنقودك، ولذلك يُوصى بوضع العنقود في وضع الصيانة إلى أن يكتمل إعادة تشغيل daemon الخاص بـ Patroni.

لوضع العنقود في وضع الصيانة، شغّل الأمر التالي على إحدى عقد patroni:

```bash
patronictl pause --wait
```

ثم على كل عقدة في العنقود، نفّذ ترقية الحزم المطلوبة لنظام التشغيل الخاص بك:

```bash
apt-get update && apt-get install patroni
```

أعد تشغيل عملية daemon الخاص بـ patroni على كل عقدة:

```bash
systemctl restart patroni
```

ثم أخيرًا استأنف مراقبة Postgres باستخدام patroni لإخراجه من وضع الصيانة:

```bash
patronictl resume --wait
```

سيكون العنقود الآن جاهزًا للعمل بالكامل بالإصدار الجديد من Patroni.
