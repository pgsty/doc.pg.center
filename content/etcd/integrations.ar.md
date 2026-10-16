---
title: المكتبات والأدوات
weight: 1300
description: قائمة بأدوات etcd ومكتبات العملاء
icon: fa-solid fa-puzzle-piece
categories: [مرجع]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/integrations.md"
---

لاحظ أن مكتبات وأدوات الأطراف الخارجية (غير المستضافة على https://github.com/etcd-io) المذكورة أدناه لا يختبرها فريق etcd ولا يصونها. قبل استخدامها، يوصى المستخدمون بقراءتها وفحصها.

## الأدوات {#tools}

- [etcdctl](https://github.com/etcd-io/etcd/tree/main/etcdctl) - عميل سطر أوامر لـ etcd
- [etcd-dump](https://npmjs.org/package/etcd-dump) - أداة سطر أوامر لتفريغ/استعادة etcd.
- [etcd-fs](https://github.com/xetorthio/etcd-fs) - نظام ملفات FUSE لـ etcd
- [etcddir](https://github.com/rekby/etcddir) - مزامنة فورية بين etcd ودليل محلي. يعمل مع Windows و Linux.
- [etcd-browser](https://github.com/henszey/etcd-browser) - محرر مفتاح/قيمة يعمل عبر الويب لـ etcd باستخدام AngularJS
- [etcd-lock](https://github.com/datawisesystems/etcd-lock) - تنفيذ لانتخاب الرئيس والقفل الموزع للقراءة/الكتابة باستخدام etcd - يدعم الإصدار v2
- [etcd-console](https://github.com/matishsiao/etcd-console) - محرر مفتاح/قيمة يعمل عبر الويب لـ etcd باستخدام PHP
- [etcd-viewer](https://github.com/nikfoundas/etcd-viewer) - محرر/عارض لمخزن المفتاح-القيمة في etcd مكتوب بلغة Java
- [etcdtool](https://github.com/mickep76/etcdtool) - تصدير/استيراد/تحرير دليل etcd بصيغة JSON/YAML/TOML والتحقق من صحة الدليل باستخدام مخطط JSON
- [etcdloadtest](https://github.com/sinsharat/etcdloadtest) - عميل اختبار تحميل يعمل من سطر الأوامر لإصدار etcd 3.0 وما بعده.
- [etcd-tui](https://github.com/olamilekan000/etcd-tui) - واجهة مستخدم حديثة تعمل في الطرفية (TUI) للتفاعل مع قاعدة بيانات etcd الخاصة بك. تنقّل بين المفاتيح، واعرض القيم، ورشّح البيانات، وأدر عنقود etcd مباشرة من الطرفية.
- [etcdfinder](https://etcdfinder.github.io) - واجهة ويب حديثة وفائقة السرعة لـ etcd مع بحث فوري. تدعم كلًا من etcd v2 و v3.
- [lucas](https://github.com/ringtail/lucas) - عارض مفتاح-قيمة يعمل عبر الويب لعناقيد kubernetes etcd3.0+.
- [etcd-manager](https://etcdmanager.io) - أداة واجهة رسومية وعميل حديثة وفعالة ومتعددة المنصات ومجانية لـ etcd 3.x. متاحة لأنظمة Windows و Linux و Mac.
- [etcd-backup-restore](https://github.com/gardener/etcd-backup-restore) - أداة للنسخ الاحتياطي والاستعادة الدوريين والتزايديين لـ etcd.
- [etcd-druid](https://github.com/gardener/etcd-druid) - عامل تشغيل (operator) في Kubernetes لنشر عناقيد etcd وإدارة عمليات اليوم الثاني (day-2).
- [etcdadm](https://github.com/kubernetes-sigs/etcdadm) - أداة سطر أوامر لتشغيل عنقود etcd.
- [etcd-defrag](https://github.com/ahrtr/etcd-defrag) - أداة أسهل استخدامًا وأكثر ذكاءً لإزالة تجزئة etcd.
- [etcdhelper](https://github.com/tsonglew/intellij-etcdhelper) - إضافة (plugin) لمنصة IntelliJ مخصصة لـ etcd.

## المكتبات {#libraries}

تدرج الأقسام التالية مكتبات عملاء etcd حسب اللغة.

### Go {#go}

- [etcd/client/v3](https://github.com/etcd-io/etcd/tree/main/client/v3) - عميل Go الرسمي المُصان للإصدار v3
- [go-etcd](https://github.com/coreos/go-etcd) - العميل الرسمي المهمل. قد يكون مفيدًا للإصدارات الأقدم (<2.0.0) من etcd.
- [encWrapper](https://github.com/lumjjb/etcd/tree/enc_wrapper/clientwrap/encwrapper) - encWrapper هو غلاف تشفير لواجهة برمجة تطبيقات Keys/KV في عميل etcd.

### Java {#java}

- [coreos/jetcd](https://github.com/etcd-io/jetcd) - يدعم الإصدار v3
- [justinsb/jetcd](https://github.com/justinsb/jetcd)
- [cdancy/etcd-rest](https://github.com/cdancy/etcd-rest) - يستخدم jclouds لتوفير تنفيذ كامل لواجهة برمجة تطبيقات الإصدار v2.
- [IBM/etcd-java](https://github.com/IBM/etcd-java)

### Scala {#scala}

- [maciej/etcd-client](https://github.com/maciej/etcd-client) - يدعم الإصدار v2. عميل غير متزامن بالكامل مبني على Akka HTTP
- [eiipii/etcdhttpclient](https://bitbucket.org/eiipii/etcdhttpclient) - يدعم الإصدار v2. عميل HTTP غير متزامن مبني على Netty و Scala Futures.
- [mingchuno/etcd4s](https://github.com/mingchuno/etcd4s) - يدعم الإصدار v3 باستخدام gRPC مع دعم اختياري لـ Akka Stream.

### Perl {#perl}

- [hexfusion/perl-net-etcd](https://github.com/hexfusion/perl-net-etcd) - يدعم واجهة HTTP لبوابة grpc في الإصدار v3
- [robn/p5-etcd](https://github.com/robn/p5-etcd) - يدعم الإصدار v2

### Python {#python}

- [kragniz/python-etcd3](https://github.com/kragniz/python-etcd3) - عميل للإصدار v3
- [jplana/python-etcd](https://github.com/jplana/python-etcd) - يدعم الإصدار v2
- [russellhaering/txetcd](https://github.com/russellhaering/txetcd) - مكتبة Python تعتمد Twisted
- [cholcombe973/autodock](https://github.com/cholcombe973/autodock) - أداة أتمتة لنشر Docker
- [lisael/aioetcd](https://github.com/lisael/aioetcd) - (Python 3.4+) عميل يعتمد على coroutine الخاصة بـ asyncio (يدعم الإصدار v2)
- [txaio-etcd](https://github.com/crossbario/txaio-etcd) - مكتبة عميل غير متزامنة لإصدارات etcd v3 فقط، لـ Twisted (حاليًا) و asyncio (مستقبلًا)
- [dims/etcd3-gateway](https://github.com/dims/etcd3-gateway) - مكتبة لواجهة etcd v3 API تستخدم بوابة HTTP لـ grpc
- [aioetcd3](https://github.com/gaopeiliang/aioetcd3) - (Python 3.6+) واجهة etcd v3 API لـ asyncio
- [Revolution1/etcd3-py](https://github.com/Revolution1/etcd3-py) - (python2.7 و python3.5+) عميل Python لـ etcd v3، يستخدم gRPC-JSON-Gateway

### Node {#node}

- [mixer/etcd3](https://github.com/mixer/etcd3) - يدعم الإصدار v3
- [stianeikeland/node-etcd](https://github.com/stianeikeland/node-etcd) - يدعم الإصدار v2 (مع Coffeescript)
- [lavagetto/nodejs-etcd](https://github.com/lavagetto/nodejs-etcd) - يدعم الإصدار v2
- [deedubs/node-etcd-config](https://github.com/deedubs/node-etcd-config) - يدعم الإصدار v2

### Ruby {#ruby}

- [iconara/etcd-rb](https://github.com/iconara/etcd-rb)
- [jpfuentes2/etcd-ruby](https://github.com/jpfuentes2/etcd-ruby)
- [ranjib/etcd-ruby](https://github.com/ranjib/etcd-ruby) - يدعم الإصدار v2
- [davissp14/etcdv3-ruby](https://github.com/davissp14/etcdv3-ruby) - يدعم الإصدار v3

### C {#c}

- [apache/celix/etcdlib](https://github.com/apache/celix/tree/master/libs/etcdlib) - يدعم الإصدار v2
- [jdarcy/etcd-api](https://github.com/jdarcy/etcd-api) - يدعم الإصدار v2
- [shafreeck/cetcd](https://github.com/shafreeck/cetcd) - يدعم الإصدار v2

### C++ {#c-1}

- [edwardcapriolo/etcdcpp](https://github.com/edwardcapriolo/etcdcpp) - يدعم الإصدار v2
- [suryanathan/etcdcpp](https://github.com/suryanathan/etcdcpp) - يدعم الإصدار v2 (مع waits)
- [nokia/etcd-cpp-api](https://github.com/nokia/etcd-cpp-api) - يدعم الإصدار v2
- [etcd-cpp-apiv3/etcd-cpp-apiv3](https://github.com/etcd-cpp-apiv3/etcd-cpp-apiv3) - يدعم الإصدار v3

### Clojure {#clojure}

- [aterreno/etcd-clojure](https://github.com/aterreno/etcd-clojure)
- [dwwoelfel/cetcd](https://github.com/dwwoelfel/cetcd) - يدعم الإصدار v2
- [rthomas/clj-etcd](https://github.com/rthomas/clj-etcd) - يدعم الإصدار v2

### Erlang {#erlang}

- [marshall-lee/etcd.erl](https://github.com/marshall-lee/etcd.erl) - يدعم الإصدار v2
- [zhongwencool/eetcd](https://github.com/zhongwencool/eetcd) - يدعم الإصدار v3+ (GRPC فقط)

### Elixir {#elixir}

- [team-telnyx/etcdex](https://github.com/team-telnyx/etcdex) - يدعم الإصدار v3+ (GRPC فقط)

### .NET {#net}

- [wangjia184/etcdnet](https://github.com/wangjia184/etcdnet) - يدعم الإصدار v2
- [drusellers/etcetera](https://github.com/drusellers/etcetera)
- [shubhamranjan/dotnet-etcd](https://github.com/shubhamranjan/dotnet-etcd) - يدعم الإصدار v3+ (GRPC فقط)
- [SimplifyNet/Etcd.Microsoft.Extensions.Configuration](https://github.com/SimplifyNet/Etcd.Microsoft.Extensions.Configuration)

### PHP {#php}

- [linkorb/etcd-php](https://github.com/linkorb/etcd-php)
- [activecollab/etcd](https://github.com/activecollab/etcd)
- [ouqiang/etcd-php](https://github.com/ouqiang/etcd-php) - عميل لبوابة gRPC للإصدار v3

### Haskell {#haskell}

- [wereHamster/etcd-hs](https://github.com/wereHamster/etcd-hs)

### R {#r}

- [ropensci/etseed](https://github.com/ropensci/etseed)

### Nim {#nim}

- [etcd_client](https://github.com/FedericoCeratto/nim-etcd-client)

### Tcl {#tcl}

- [efrecon/etcd-tcl](https://github.com/efrecon/etcd-tcl) - يدعم الإصدار v2، باستثناء wait.

### Rust {#rust}

- [jimmycuadra/rust-etcd](https://github.com/jimmycuadra/rust-etcd) - يدعم الإصدار v2

### Gradle {#gradle}

- [gradle-etcd-rest-plugin](https://github.com/cdancy/gradle-etcd-rest-plugin) - يدعم الإصدار v2

### Lua {#lua}

- [api7/lua-resty-etcd](https://github.com/api7/lua-resty-etcd) - يدعم الإصدارين v2 و v3 (واجهة HTTP لبوابة grpc)

## أدوات النشر {#deployment-tools}

### تكاملات Chef {#chef-integrations}

- [coderanger/etcd-chef](https://github.com/coderanger/etcd-chef)

### كتب وصفات Chef {#chef-cookbooks}

- [spheromak/etcd-cookbook](https://github.com/spheromak/etcd-cookbook)

### إصدارات BOSH {#bosh-releases}

- [cloudfoundry-community/etcd-boshrelease](https://github.com/cloudfoundry-community/etcd-boshrelease)
- [cloudfoundry/cf-release](https://github.com/cloudfoundry/cf-release/tree/master/jobs/etcd)

## مشاريع تستخدم etcd {#projects-using-etcd}

- [مستخدمو Raft في etcd](https://github.com/etcd-io/raft/blob/main/README.md#notable-users) - مشاريع تستخدم تنفيذ مكتبة raft الخاص بـ etcd.
- [Apache APISIX](https://github.com/apache/apisix) - بوابة API تستخدم etcd كمخزن للتهيئة.
- [apache/celix](https://github.com/apache/celix) - تنفيذ لمواصفة OSGi مُكيَّف للغتين C و C++
- [binocarlos/yoda](https://github.com/binocarlos/yoda) - etcd + ZeroMQ
- [blox/blox](https://github.com/blox/blox) - مجموعة من المشاريع مفتوحة المصدر لإدارة الحاويات وتنسيقها مع AWS ECS
- [calavera/active-proxy](https://github.com/calavera/active-proxy) - وكيل HTTP يُهيأ بواسطة etcd
- [chain/chain](https://github.com/chain/chain) - برمجية مصممة لتشغيل شبكات بلوكشين مُرخَّصة (permissioned) عالية القابلية للتوسع والاتصال بها
- [derekchiang/etcdplus](https://github.com/derekchiang/etcdplus) - مجموعة من بدائيات المزامنة الموزعة المبنية فوق etcd
- [go-discover](https://github.com/flynn/go-discover) - اكتشاف الخدمات بلغة Go
- [gleicon/goreman](https://github.com/gleicon/goreman/tree/etcd) - فرع من نسخة Go المطابقة لـ Foreman مع دعم etcd
- [garethr/hiera-etcd](https://github.com/garethr/hiera-etcd) - الواجهة الخلفية hiera لـ Puppet باستخدام etcd
- [mattn/etcd-vim](https://github.com/mattn/etcd-vim) - تنفيذ SET و GET للمفاتيح من داخل vim
- [mattn/etcdenv](https://github.com/mattn/etcdenv) - سطر shebang بصيغة «env» مع تكامل مع etcd
- [kelseyhightower/confd](https://github.com/kelseyhightower/confd) - إدارة ملفات تهيئة التطبيقات المحلية باستخدام قوالب وبيانات من etcd
- [configdb](https://git.autistici.org/ai/configdb/tree/master) - تجريد علائقي عبر REST فوق واجهات خلفية لقواعد البيانات أيًا كان نوعها، موجه لتخزين التهيئات والجرد.
- [kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) - مدير عناقيد الحاويات الذي قدمته Google.
- [mailgun/vulcand](https://github.com/mailgun/vulcand) - وكيل HTTP يستخدم etcd كواجهة خلفية للتهيئة.
- [duedil-ltd/discodns](https://github.com/duedil-ltd/discodns) - خادم أسماء DNS بسيط يستخدم etcd كقاعدة بيانات للأسماء والسجلات.
- [skynetservices/skydns](https://github.com/skynetservices/skydns) - خادم DNS متوافق مع معايير RFC
- [xordataexchange/crypt](https://github.com/xordataexchange/crypt) - تخزين القيم في etcd بأمان باستخدام تشفير GPG
- [spf13/viper](https://github.com/spf13/viper) - مكتبة تهيئة بلغة Go، تقرأ القيم من متغيرات البيئة ENV و pflags والملفات و etcd مع تشفير اختياري
- [lytics/metafora](https://github.com/lytics/metafora) - مكتبة مهام موزعة بلغة Go
- [ryandoyle/nss-etcd](https://github.com/ryandoyle/nss-etcd) - وحدة NSS لمكتبة GNU libc لحل الأسماء من etcd.
- [Gru](https://github.com/dnaeon/gru) - التنسيق (orchestration) أصبح سهلًا مع Go
- [Vitess](http://vitess.io/) - Vitess هو نظام عنقدة قواعد البيانات للتوسع الأفقي في MySQL.
- [lclarkmichalek/etcdhcp](https://github.com/lclarkmichalek/etcdhcp) - خادم DHCP يستخدم etcd للتخزين الدائم والتنسيق.
- [openstack/networking-vpp](https://github.com/openstack/networking-vpp) - مشغل شبكة يبرمج [مستوى بيانات FD.io VPP](https://wiki.fd.io/view/VPP) لتوفير الشبكة الافتراضية السحابية لـ [OpenStack](https://www.openstack.org/)
- [OpenStack](https://github.com/openstack/governance/blob/master/reference/base-services.rst) - يمكن لخدمات OpenStack الاعتماد على etcd كخدمة أساسية.
- [CoreDNS](https://github.com/coredns/coredns/tree/master/plugin/etcd) - CoreDNS هو خادم DNS يسلسل الإضافات (plugins)، وهو جزء من CNCF و Kubernetes
- [Uber M3](https://github.com/m3db/m3) - M3: منصة مقاييس مفتوحة المصدر واسعة النطاق من Uber مخصصة لـ Prometheus
- [Rook](https://github.com/rook/rook) - تنسيق التخزين لـ Kubernetes
- [Patroni](https://github.com/zalando/patroni) - قالب للتوافرية العالية لـ PostgreSQL مع ZooKeeper أو etcd أو Consul
- [Trillian](https://github.com/google/trillian) - ينفّذ Trillian شجرة Merkle يُقدَّم محتواها من طبقة تخزين بيانات، للسماح بالتوسع إلى أشجار ضخمة للغاية.
- [purpleidea/mgmt](https://github.com/purpleidea/mgmt) - إدارة تهيئة موزعة، معتمدة على الأحداث، ومتوازية من الجيل التالي!
- [Portworx/kvdb](https://docs.portworx.com/concepts/internal-kvdb/) - قاعدة kvdb الداخلية لتخزين تهيئة عنقود Portworx.
- [Apache Pulsar](https://pulsar.apache.org/) - Apache Pulsar هي منصة مراسلة وبث مفتوحة المصدر وموزعة، مبنية من أجل السحابة.
