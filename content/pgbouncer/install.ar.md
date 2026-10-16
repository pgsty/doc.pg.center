---
title: "بناء PgBouncer وتثبيته"
linkTitle: "التثبيت"
weight: 40
description: "تعليمات بناء PgBouncer وتثبيته"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [درس تعليمي]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/README.md"
---

--------

## البناء {#building}

يمكن بناء PgBouncer بنظام البناء القائم على Autoconf أو بنظام البناء [Meson] الأحدث
وما زال تجريبيًا. يظل Autoconf هو الخيار الموصى به حاليًا
لبناء الإصدارات الإنتاجية وتجهيز الحزم. من المتوقع أن يصبح البناء بـ Meson
هو الافتراضي وأن يُزال البناء بـ Autoconf في
إصدار مستقبلي، لذا فإن اختباره والإبلاغ عن أي مشكلات فيه أمر مرحَّب به جدًا.
يعتمد البناء على بعض الأمور:

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ لدعم TLS
* مصرِّف C يدعم C11
* (اختياري) [c-ares] كبديل عن evdns الخاص بـ Libevent
* (اختياري) مكتبات LDAP
* (اختياري) مكتبات PAM

يتطلب البناء بـ Meson إضافةً إلى ذلك [Meson] 0.58+ و[Ninja]؛ ويتطلب البناء
بـ Autoconf [GNU Make] 3.81+.

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

عندما تُثبَّت التبعيات، ابنِ باستخدام Autoconf:

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

أو باستخدام Meson (تجريبي):

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

إذا كنت تبني من Git، أو كنت تبني من أجل Windows، فراجع
تعليمات البناء المنفصلة أدناه.

--------

## دعم الاستعلام عن DNS {#dns-lookup-support}

يجري PgBouncer عمليات الاستعلام عن أسماء المضيفين وقت الاتصال بدلًا من مرة واحدة
فقط وقت تحميل الإعداد. يتطلب ذلك تنفيذًا غير متزامن لـ DNS. يعرض الجدول التالي
الخلفيات (backends) المدعومة وترتيب فحصها:

| backend (الخلفية)             | متوازٍ | EDNS0 (1) | /etc/hosts | استعلام SOA (2) | ملاحظة                                    |
|-------------------------------|---------|-----------|------------|-----------------|-------------------------------------------|
| c-ares                        | نعم     | نعم       | نعم        | نعم             | خلل في IPv6+CNAME في <=1.10               |
| evdns, libevent 2.x           | نعم     | لا        | نعم        | لا              | لا يتحقق من تحديثات /etc/hosts            |
| getaddrinfo_a, glibc 2.9+     | نعم     | نعم (3)   | نعم        | لا              | غير متاح على الأنظمة غير glibc            |
| getaddrinfo, libc             | لا      | نعم (3)   | نعم        | لا              | يتطلب pthreads                            |

1. يُتطلب EDNS0 ليكون هناك أكثر من 8 عناوين خلف اسم مضيف واحد.
2. يلزم استعلام SOA لإعادة فحص أسماء المضيفين عند تغيّر الرقم التسلسلي للمنطقة.
3. لتمكين EDNS0، أضِف `options edns0` إلى `/etc/resolv.conf`.

‏c-ares هو التنفيذ الأكمل من حيث الميزات ويوصى به لمعظم الاستخدامات
وللحزم الثنائية (إذا توفرت نسخة حديثة بما يكفي).
كما أن evdns المدمج في Libevent مناسب لكثير من الاستخدامات،
مع القيود المذكورة. أما الخلفيات الأخرى فهي في معظمها خيارات
قديمة لم تعد تخضع لكثير من الاختبار في الوقت الراهن.

افتراضيًا، يُستخدم c-ares إذا أمكن العثور عليه. يمكن فرض استخدامه
باستخدام `-Dcares=enabled` (في configure: `--with-cares`) أو تعطيله باستخدام
`-Dcares=disabled` (في configure: `--without-cares`). وإذا لم يُستخدم c-ares
(لعدم العثور عليه أو لتعطيله)، فإنه يُستخدم Libevent. حدِّد `-Devdns=false`
(في configure: `--disable-evdns`) لتعطيل استخدام evdns الخاص بـ Libevent
والرجوع إلى تنفيذ قائم على libc.

--------

## ميزات اختيارية {#optional-features}

تُكتشف ميزات PAM وLDAP وsystemd تلقائيًا بواسطة meson: خياراتها `-Dpam`
و`-Dldap` و`-Dsystemd` تملك القيمة الافتراضية `auto`، لذا تُبنى كل ميزة عندما
تكون مكتباتها موجودة. افرض تفعيل ميزة بـ `-D<feature>=enabled` أو تعطيلها بـ
`-D<feature>=disabled`. البناء بـ Autoconf لا يكتشفها تلقائيًا؛ فعِّلها صراحةً
باستخدام `--with-pam` أو `--with-ldap` أو `--with-systemd`.

--------

## مصادقة PAM {#pam-authentication}

عند البناء مع دعم PAM، يتوفر نوع مصادقة عام جديد هو `pam`
للتحقق من المستخدمين عبر PAM.

--------

## مصادقة LDAP {#ldap-authentication}

عند البناء مع دعم LDAP، يتوفر نوع مصادقة عام جديد هو `ldap`
للتحقق من المستخدمين عبر LDAP.

--------

## تكامل systemd {#systemd-integration}

يتيح دعم systemd استخدام `Type=notify` (أو `Type=notify-reload` إذا كنت تستخدم
systemd 253 أو أحدث) بالإضافة إلى تفعيل المقابس (socket activation). راجع
`etc/pgbouncer.service` و`etc/pgbouncer.socket` لأمثلة.

--------

## البناء من Git {#building-from-git}

يتطلب البناء بـ Autoconf أن تولّد ملفات الترويسة والإعداد
قبل أن تتمكن من تشغيل `configure`:

	$ git clone --branch pgbouncer_1_26_0 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

ستُثبَّت جميع الملفات تحت `/usr/local` افتراضيًا. يمكنك
تمرير خيار واحد أو أكثر من خيارات سطر الأوامر إلى `configure`. شغّل
`./configure --help` لسرد الخيارات المتاحة ومتغيرات البيئة
التي تخصص الإعداد.

حزم إضافية مطلوبة للبناء بـ Autoconf من Git: autoconf,
automake, libtool, pandoc

مع البناء بـ Meson يمكنك البناء مباشرةً من نسخة مستودع (checkout)؛
ويُطلب pandoc لبناء صفحات الدليل (man pages):

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

شغّل `meson configure build` لسرد خيارات `-D` المتاحة.

--------

## الاختبار {#testing}

راجع [ملف `README.md` في دليل الاختبار][1] لمعرفة كيفية تشغيل الاختبارات.

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/test/README.md

--------

## البناء على Windows {#building-on-windows}

بيئة البناء الوحيدة المدعومة على Windows هي MinGW. أما Cygwin
وVisual $ANYTHING فغير مدعومين.

للبناء على MinGW، قم بعملية البناء المعتادة بـ Autoconf:

	$ ./configure
	$ make

أو البناء التجريبي بـ Meson:

	$ meson setup build
	$ meson compile -C build

في حال البناء المتقاطع (cross-compiling) من Unix باستخدام Autoconf:

	$ ./configure --host=i586-mingw32msvc

خيار البناء LDAP غير مدعوم حاليًا على Windows.

--------

## التشغيل على Windows {#running-on-windows}

يتم التشغيل من سطر الأوامر كالمعتاد، باستثناء أن الخيارين `-d` (التشغيل كبرنامج خلفي
daemon) و`-u` (تبديل المستخدم) لن يعملا.

لتشغيل PgBouncer كخدمة Windows، تحتاج إلى ضبط المعامل
`service_name` لتعيين اسم للخدمة. ثم:

	$ pgbouncer -regservice config.ini

لإزالة تثبيت الخدمة:

	$ pgbouncer -unregservice config.ini

لاستخدام سجل أحداث Windows، اضبط `syslog = 1` في ملف الإعداد.
لكن قبل ذلك، يجب عليك تسجيل `pgbevent.dll`:

	$ regsvr32 pgbevent.dll

لإلغاء تسجيله، نفّذ ما يلي:

	$ regsvr32 /u pgbevent.dll
