---
title: "10. تسهيل إدارة الإعداد"
linkTitle: "10. إدارة الإعداد"
weight: 340
description: "تقنيات لتسهيل صيانة إعدادات HAProxy الكبيرة"
icon: fa-solid fa-screwdriver-wrench
module: [HAPROXY]
categories: [مهمة]
aliases:
  - /haproxy/management/configuration-management/
upstream_link: "https://docs.haproxy.org/3.4/management.html"
upstream_name: "HAProxy 3.4 Management Guide"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 10"
---

من الشائع جدًا أن تتشارك عقدتا HAProxy المكونتان لعنقود واحد الإعداد نفسه تمامًا مع
اختلاف بضعة عناوين فقط. وبدلًا من الاضطرار إلى صيانة إعداد مكرَّر لكل عقدة، وهو ما
سينحرف حتمًا عن نظيره مع الوقت، يمكن تضمين متغيرات البيئة في الإعداد. وهكذا يمكن
لإعدادات متعددة أن تتشارك الملف نفسه تمامًا مع اختلاف بضعة متغيرات بيئة على مستوى
النظام فقط. بدأ ذلك في الإصدار 1.5 حيث لم يكن مسموحًا بتضمين متغيرات البيئة إلا في
العناوين، ثم ذهب الإصدار 1.6 أبعد من ذلك بدعم متغيرات البيئة في كل مكان. الصياغة هي
نفسها المستخدمة في صدفة UNIX؛ إذ يبدأ المتغير بعلامة دولار ('\$') يليها قوس مجعد
فاتح ('{') ثم اسم المتغير ويُختَم بقوس مجعد مغلق ('}'). باستثناء العناوين، لا
تُفسَّر متغيرات البيئة إلا في الوسائط المحاطة بعلامات اقتباس مزدوجة (وكان ذلك ضروريًا
حتى لا تنكسر الإعدادات القائمة التي تستخدم تعابير نمطية تتضمن رمز الدولار).

تتيح متغيرات البيئة أيضًا كتابة إعدادات يُتوقع أن تعمل على مواقع مختلفة لا يتغير فيها
سوى العنوان بسهولة. كما يمكنها أن تسهم في إخراج كلمات المرور من بعض الإعدادات. المثال
التالي يوضح ملف "site1.env" الذي يُحمِّله سكربت التهيئة عند بدء التشغيل:

```shell
$ cat site1.env
LISTEN=192.168.1.1
CACHE_PFX=192.168.11
SERVER_PFX=192.168.22
LOGGER=192.168.33.1
STATSLP=admin:pa$$w0rd
ABUSERS=/etc/haproxy/abuse.lst
TIMEOUT=10s

$ cat haproxy.cfg
global
    log "${LOGGER}:514" local0

defaults
    mode http
    timeout client "${TIMEOUT}"
    timeout server "${TIMEOUT}"
    timeout connect 5s

frontend public
    bind "${LISTEN}:80"
    http-request reject if { src -f "${ABUSERS}" }
    stats uri /stats
    stats auth "${STATSLP}"
    use_backend cache if { path_end .jpg .css .ico }
    default_backend server

backend cache
    server cache1 "${CACHE_PFX}.1:18080" check
    server cache2 "${CACHE_PFX}.2:18080" check

backend server
    server cache1 "${SERVER_PFX}.1:8080" check
    server cache2 "${SERVER_PFX}.2:8080" check
```
