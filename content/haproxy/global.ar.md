---
title: "3. القسم العام"
linkTitle: "3. القسم العام"
weight: 140
description: "أمان العمليات، وضبط الأداء، وتصحيح الأخطاء، وإعدادات عميل HTTP"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [مرجع]
aliases:
  - /haproxy/configuration/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.7-57-g0faeaeda6cdb, chapter 3"
---

المعاملات في قسم «global» تنطبق على العملية بأكملها وكثيرًا ما تكون خاصة بنظام التشغيل. تُضبط عمومًا
مرة واحدة وإلى الأبد ولا تحتاج إلى تغييرها متى صارت صحيحة. لبعضها ما يقابلها من خيارات سطر الأوامر.

تُدعم الكلمات المفتاحية التالية في قسم «global»:

- إدارة العمليات والأمان

  - 51degrees-allow-unmatched
  - 51degrees-cache-size
  - 51degrees-data-file
  - 51degrees-difference
  - 51degrees-drift
  - 51degrees-property-name-list
  - 51degrees-property-separator
  - 51degrees-use-performance-graph
  - 51degrees-use-predictive-graph
  - ca-base
  - chroot
  - cluster-secret
  - cpu-affinity
  - cpu-map
  - cpu-policy
  - cpu-set
  - crt-base
  - daemon
  - default-path
  - description
  - deviceatlas-json-file
  - deviceatlas-log-level
  - deviceatlas-properties-cookie
  - deviceatlas-separator
  - dns-accept-family
  - expose-deprecated-directives
  - expose-experimental-directives
  - external-check
  - fd-hard-limit
  - gid
  - grace
  - group
  - h1-accept-payload-with-any-method
  - h1-case-adjust
  - h1-case-adjust-file
  - h1-do-not-close-on-insecure-transfer-encoding
  - h2-workaround-bogus-websocket-clients
  - hard-stop-after
  - harden.reject-privileged-ports.tcp
  - harden.reject-privileged-ports.quic
  - insecure-fork-wanted
  - insecure-setuid-wanted
  - issuers-chain-path
  - jwt.allow_none_alg
  - jwt.decrypt_alg_list
  - jwt.decrypt_enc_list
  - key-base
  - limited-quic
  - localpeer
  - log
  - log-send-hostname
  - log-tag
  - lua-load
  - lua-load-per-thread
  - lua-prepend-path
  - max-threads-per-group
  - mworker-max-reloads
  - nbthread
  - node
  - numa-cpu-mapping
  - ocsp-update.disable
  - ocsp-update.maxdelay
  - ocsp-update.mindelay
  - ocsp-update.httpproxy
  - ocsp-update.mode
  - pidfile
  - pp2-never-send-local
  - presetenv
  - prealloc-fd
  - resetenv
  - set-dumpable
  - set-var
  - setenv
  - ssl-default-bind-ciphers
  - ssl-default-bind-ciphersuites
  - ssl-default-bind-client-sigalgs
  - ssl-default-bind-curves
  - ssl-default-bind-options
  - ssl-default-bind-sigalgs
  - ssl-default-server-ciphers
  - ssl-default-server-ciphersuites
  - ssl-default-server-client-sigalgs
  - ssl-default-server-curves
  - ssl-default-server-options
  - ssl-default-server-sigalgs
  - ssl-dh-param-file
  - ssl-propquery
  - ssl-provider
  - ssl-provider-path
  - ssl-security-level
  - ssl-server-verify
  - ssl-skip-self-issued-ca
  - stats
  - stats-file
  - strict-limits
  - uid
  - ulimit-n
  - unix-bind
  - unsetenv
  - user
  - wurfl-cache-size
  - wurfl-data-file
  - wurfl-information-list
  - wurfl-information-list-separator

- ضبط الأداء

  - busy-polling
  - max-spread-checks
  - maxcompcpuusage
  - maxcomprate
  - maxconn
  - maxconnrate
  - maxpipes
  - maxsessrate
  - maxsslconn
  - maxsslrate
  - maxzlibmem
  - no-memory-trimming
  - noepoll
  - noevports
  - nogetaddrinfo
  - nokqueue
  - noktls
  - nopoll
  - noreuseport
  - nosplice
  - profiling.memory
  - profiling.tasks
  - server-state-base
  - server-state-file
  - spread-checks
  - ssl-engine
  - ssl-mode-async
  - tune.applet.zero-copy-forwarding
  - tune.buffers.limit
  - tune.buffers.reserve
  - tune.bufsize
  - tune.bufsize.large
  - tune.bufsize.small
  - tune.cli.max-payload-size
  - tune.comp.maxlevel
  - tune.defaults.purge
  - tune.disable-fast-forward
  - tune.disable-zero-copy-forwarding
  - tune.epoll.mask-events
  - tune.events.max-events-at-once
  - tune.fail-alloc
  - tune.fd.edge-triggered
  - tune.h1.be.glitches-threshold
  - tune.h1.fe.glitches-threshold
  - tune.h1.zero-copy-fwd-recv
  - tune.h1.zero-copy-fwd-send
  - tune.h2.be.glitches-threshold
  - tune.h2.be.initial-window-size
  - tune.h2.be.max-concurrent-streams
  - tune.h2.be.max-frames-at-once
  - tune.h2.be.rxbuf
  - tune.h2.fe.glitches-threshold
  - tune.h2.fe.initial-window-size
  - tune.h2.fe.max-concurrent-streams
  - tune.h2.fe.max-frames-at-once
  - tune.h2.fe.max-rst-at-once
  - tune.h2.fe.max-total-streams
  - tune.h2.fe.rxbuf
  - tune.h2.header-table-size
  - tune.h2.initial-window-size
  - tune.h2.max-concurrent-streams
  - tune.h2.max-frame-size
  - tune.h2.zero-copy-fwd-send
  - tune.http.cookielen
  - tune.http.logurilen
  - tune.http.maxhdr
  - tune.idle-pool.shared
  - tune.idletimer
  - tune.lua.bool-sample-conversion
  - tune.lua.burst-timeout
  - tune.lua.forced-yield
  - tune.lua.log.loggers
  - tune.lua.log.stderr
  - tune.lua.maxmem
  - tune.lua.openlibs
  - tune.lua.service-timeout
  - tune.lua.session-timeout
  - tune.lua.task-timeout
  - tune.max-checks-per-thread
  - tune.maxaccept
  - tune.maxpollevents
  - tune.maxrewrite
  - tune.max-rules-at-once
  - tune.memory.hot-size
  - tune.pattern.cache-size
  - tune.peers.max-updates-at-once
  - tune.pipesize
  - tune.pool-high-fd-ratio
  - tune.pool-low-fd-ratio
  - tune.pt.zero-copy-forwarding
  - tune.quic.be.cc.cubic-min-losses
  - tune.quic.be.cc.hystart
  - tune.quic.be.cc.max-frame-loss
  - tune.quic.be.cc.max-win-size
  - tune.quic.be.cc.reorder-ratio
  - tune.quic.be.max-idle-timeout
  - tune.quic.be.sec.glitches-threshold
  - tune.quic.be.stream.data-ratio
  - tune.quic.be.stream.max-concurrent
  - tune.quic.be.stream.rxbuf
  - tune.quic.be.tx.pacing
  - tune.quic.be.tx.udp-gso
  - tune.quic.cc.cubic.min-losses (مهجور)
  - tune.quic.cc-hystart (مهجور)
  - tune.quic.disable-tx-pacing (مهجور)
  - tune.quic.disable-udp-gso (مهجور)
  - tune.quic.fe.cc.cubic-min-losses
  - tune.quic.fe.cc.hystart
  - tune.quic.fe.cc.max-frame-loss
  - tune.quic.fe.cc.max-win-size
  - tune.quic.fe.cc.reorder-ratio
  - tune.quic.fe.max-idle-timeout
  - tune.quic.fe.sec.glitches-threshold
  - tune.quic.fe.sec.retry-threshold
  - tune.quic.fe.sock-per-conn
  - tune.quic.fe.stream.data-ratio
  - tune.quic.fe.stream.max-concurrent
  - tune.quic.fe.stream.max-total
  - tune.quic.fe.stream.rxbuf
  - tune.quic.fe.tx.pacing
  - tune.quic.fe.tx.udp-gso
  - tune.quic.frontend.max-data-size (مهجور)
  - tune.quic.frontend.max-idle-timeout (مهجور)
  - tune.quic.frontend.max-streams-bidi (مهجور)
  - tune.quic.frontend.max-tx-mem (مهجور)
  - tune.quic.frontend.stream-data-ratio (مهجور)
  - tune.quic.frontend.default-max-window-size (مهجور)
  - tune.quic.listen
  - tune.quic.max-frame-loss (مهجور)
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio (مهجور)
  - tune.quic.retry-threshold (مهجور)
  - tune.quic.socket-owner (مهجور)
  - tune.quic.zero-copy-fwd-send
  - tune.renice.runtime
  - tune.renice.startup
  - tune.rcvbuf.backend
  - tune.rcvbuf.client
  - tune.rcvbuf.frontend
  - tune.rcvbuf.server
  - tune.recv_enough
  - tune.ring.queues
  - tune.runqueue-depth
  - tune.sched.low-latency
  - tune.sndbuf.backend
  - tune.sndbuf.client
  - tune.sndbuf.frontend
  - tune.sndbuf.server
  - tune.streams-elasticity
  - tune.stick-counters
  - tune.ssl.cachesize
  - tune.ssl.capture-buffer-size
  - tune.ssl.capture-cipherlist-size (مهجور)
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay (مهجور)
  - tune.ssl.ocsp-update.mindelay (مهجور)
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- تصحيح الأخطاء

  - anonkey
  - debug.counters
  - force-cfg-parser-pause
  - quiet
  - warn-blocked-traffic-after
  - zero-warning

- HTTPClient

  - httpclient.resolvers.disabled
  - httpclient.resolvers.id
  - httpclient.resolvers.prefer
  - httpclient.retries
  - httpclient.ssl.ca-file
  - httpclient.ssl.verify
  - httpclient.timeout.connect

## 3.1. إدارة العمليات والأمان {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

مسار ملف بيانات 51Degrees لتوفير خدمات اكتشاف الأجهزة. يجب أن يكون الملف مفكوك الضغط ومتاحًا
لـ HAProxy بالصلاحيات المناسبة.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES.

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

قائمة بأسماء خصائص 51Degrees التي ستُحمَّل من مجموعة البيانات. تتوفر القائمة الكاملة للأسماء
على موقع 51Degrees الإلكتروني: <https://51degrees.com/resources/property-dictionary>

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES.

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

محرف سيُلحق بكل قيمة خاصية في ترويسة استجابة تحوي نتائج 51Degrees. إن لم يُضبط فسيُعين
إلى ','.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES.

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

يضبط حجم ذاكرة التخزين المؤقت لمحوّل 51Degrees إلى `<number>` من المدخلات. هذه ذاكرة
تخزين مؤقت LRU تتذكر عمليات اكتشاف الأجهزة السابقة ونتائجها. افتراضيًا، تكون هذه الذاكرة معطلة.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES.

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

يُفعّل ('on') أو يعطّل ('off') استخدام مخطط الأداء في عملية الاكتشاف. تعتمد القيمة الافتراضية
على مكتبة 51Degrees.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES و
51DEGREES_VER=4.

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

يُفعّل ('on') أو يعطّل ('off') استخدام المخطط التنبؤي في عملية الاكتشاف. تعتمد القيمة
الافتراضية على مكتبة 51Degrees.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES و
51DEGREES_VER=4.

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

يضبط قيمة الانحراف التي يمكن لعملية الاكتشاف السماح بها.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES و
51DEGREES_VER=4.

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

يضبط قيمة الفرق التي يمكن لعملية الاكتشاف السماح بها.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES و
51DEGREES_VER=4.

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

يُفعّل ('on') أو يعطّل ('off') استخدام العقد غير المطابَقة في عملية الاكتشاف. تعتمد القيمة
الافتراضية على مكتبة 51Degrees.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_51DEGREES و
51DEGREES_VER=4.

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

يُفعّل أو يعطّل مجدول ACME.

يبدأ مجدول ACME عند إقلاع HAProxy، إذ يمرّ على الشهادات ويبدأ مهمة تجديد ACME عندما تصبح
قيمة notAfter متجاوزة لـ curtime + (notAfter - notBefore) / 12، أو بعد 7 أيام إن لم تكن
notBefore معرّفة. بعدها ينام المجدول ويستيقظ بعد 12 ساعة.

القيمة الافتراضية هي «auto».

انظر أيضًا: acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

يعيّن دليلًا افتراضيًا لجلب شهادات SSL CA وملفات CRL منه عند استخدام مسار نسبي مع التوجيهات
«ca-file» أو «ca-verify-file» أو «crl-file». المواقع المطلقة المحددة في «ca-file»
و«ca-verify-file» و«crl-file» لها الأولوية وتتجاهل «ca-base».

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

يغيّر الدليل الحالي إلى `<jail dir>` وينفّذ chroot() هناك قبل التخلي عن الامتيازات. هذا يرفع
مستوى الأمان في حال استغلال ثغرة مجهولة، إذ سيجعل من الصعب جدًا على المهاجم اختراق النظام. من
المهم التأكد من أن `<jail dir>` فارغ وغير قابل للكتابة لأي كان. عندما تُبدأ العملية بامتيازات
المستخدم الفائق، يُنفَّذ chroot() مباشرة. وعلى Linux، عند البدء دون امتيازات، يحاول haproxy
تنفيذه من داخل نطاق أسماء مستخدمين جديد أُنشئ بـ unshare(CLONE_NEWUSER)؛ فإن لم تكن هذه
الآلية متاحة فسيفشل chroot() بالخطأ المعتاد.

وكحالة خاصة، يمكن ضبط `<jail dir>` إلى «auto»، وفي هذه الحالة ينشئ haproxy دليلًا مؤقتًا
مجهولًا، ويفك ارتباطه، وينفّذ chroot إليه. السجن الناتج بلا اسم في نظام الملفات، وفارغ، وللقراءة
فقط، مما يغني عن تجهيز دليل سجن مخصص.

عند البدء بامتيازات المستخدم الفائق، سيُعرض تحذير إن لم يُستخدم chroot، تشجيعًا للمستخدمين على
استخدام هذه الآلية دائمًا. إن وُجد لأي سبب داعٍ قوي لعدم استخدام chroot (مثل الوصول إلى خادم عبر
مقبس UNIX بمسار غير ملائم)، يبقى من الممكن كتم التحذير بإضافة «chroot /» صريحة، وميزتها أنها
ظاهرة في التهيئة.

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

يحدد نافذة زمنية تُوزَّع خلالها عملية إغلاق الاتصالات الخاملة والنشطة في حالة الإيقاف السلس
(soft-stop). بعد استقبال إشارة SIGUSR1 وانتهاء فترة السماح (إن وُجدت)، ستُغلق جميع الاتصالات
الخاملة دفعة واحدة إن لم يُضبط هذا الخيار، وستُنهى اتصالات HTTP أو HTTP2 النشطة بعد استقبال
الطلب التالي، إما بإلحاق سطر «Connection: close» بالاستجابة، أو بإرسال إطار GOAWAY في حالة
HTTP2. عند ضبط هذا الخيار، ستُوزَّع عملية إغلاق الاتصالات على مدى `<time>` المحدد. وإذا ضُبط
close-spread-time إلى «infinite»، فسيُعطَّل إغلاق الاتصالات النشطة أثناء الإيقاف السلس. لن
تُضاف ترويسة «Connection: close» إلى استجابات HTTP بعد ذلك (أو GOAWAY لـ HTTP2)، ولن تُغلق
الاتصالات الخاملة إلا عند بلوغ مهلتها الزمنية (استنادًا إلى المهلات المختلفة المضبوطة في
التهيئة).

الوسائط:

```text
<time>  هو نافذة زمنية (بالميلي ثانية افتراضيًا) تُوزَّع خلالها عملية إغلاق
        الاتصالات أثناء عملية الإيقاف السلس، أو "infinite" إذا كان ينبغي تعطيل
        إغلاق الاتصالات النشطة.
```

يوصى بضبط هذا الإعداد إلى قيمة أدنى من القيمة المستخدمة في خيار «hard-stop-after» إن كان
مستخدمًا، بحيث تُتاح لجميع الاتصالات فرصة الإغلاق السلس قبل توقف العملية.

انظر أيضًا: grace، hard-stop-after، idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

يحدد سرًا على شكل سلسلة ASCII مشتركًا بين عدة عقد تنتمي إلى العنقود نفسه. يمكن استخدامه
لأغراض مختلفة. فهو يستخدم على الأقل لاشتقاق رموز إعادة التعيين عديمة الحالة لجميع اتصالات QUIC
التي تُنشئها هذه العملية. وكذلك الحال لاشتقاق الأسرار المستخدمة لتشفير رموز Retry.

إن لم يُضبط هذا المعامل، فستُختار قيمة عشوائية عند إقلاع العملية. هذا يسمح باستخدام الميزات
المعتمدة عليه، وإن كان ذلك مع بعض القيود.

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

على بعض أنظمة التشغيل، يمكن ربط مجموعة خيوط أو خيط بمجموعة CPU محددة. هذا يعني أن الخيوط
المعنية لن تعمل أبدًا على وحدات CPU الأخرى. يحدد توجيه «cpu-map» مجموعات CPU لخيوط فردية أو
لمجموعات خيوط. الوسيطة الأولى هي نطاق مجموعة خيوط، يتبعه اختياريًا مجموعة خيوط. لهذه النطاقات
التنسيق التالي:

```text
all | odd | even | number[-[number]]
```

يجب أن يكون `<number>` رقمًا بين 1 و32 أو 64، بحسب حجم كلمة الآلة. تُتجاهل أي معرفات مجموعات
تتجاوز 'thread-groups' وأي معرفات خيوط تتجاوز حجم كلمة الآلة. جميع أرقام الخيوط نسبية إلى
المجموعة التي تنتمي إليها. يمكن تحديد نطاق برقمين من هذا النوع مفصولين بشرطة ('-'). كما يمكن
تحديد جميع الخيوط دفعة واحدة باستخدام «all»، أو الأرقام الفردية فقط باستخدام «odd»، أو الأرقام
الزوجية باستخدام «even»، تمامًا كما مع توجيه الربط «thread». الوسيطة الثانية وما يليها هي مجموعات
CPU. كل مجموعة CPU هي إما رقم فريد يبدأ من 0 لأول CPU، أو نطاق برقمين من هذا النوع مفصولين
بشرطة ('-'). يمكن تكرار أرقام ونطاقات CPU هذه بفصلها بفواصل أو بتمرير نطاقات إضافية كوسائط
جديدة على السطر نفسه. خارج نظامي التشغيل Linux وBSD، قد يوجد قيد على أقصى فهرس CPU بـ 31 أو
63. يمكن تحديد عدة توجيهات «cpu-map»، لكن كل توجيه «cpu-map» سيحل محل السابقة عند تداخلهما.

يمكن تعريف النطاقات جزئيًا. يمكن حذف الحد الأعلى. في هذه الحالة يُستبدل بأقصى قيمة مقابلة،
32 أو 64 بحسب حجم كلمة الآلة.

يمكن إضافة البادئة «auto:» قبل مجموعة الخيوط للسماح لـ HAProxy بربط مجموعة من الخيوط تلقائيًا
بـ CPU بزيادة الخيوط ومجموعات CPU تدريجيًا. ليكون ذلك صحيحًا، يجب أن تكون المجموعتان بالحجم
نفسه. وبغض النظر عن ترتيب التصريح بمجموعات CPU، سيجري الربط من الحد الأدنى إلى الحد الأعلى.
لا يُدعم وجود نطاق مجموعة ونطاق خيوط معًا ببادئة «auto:». يُدعم نطاق واحد فقط، ويجب أن يكون
الآخر رقمًا ثابتًا.

لاحظ أن نطاقات المجموعات مدعومة لأسباب تاريخية. حاليًا، يشير الرقم المنفرد إلى مجموعة خيوط
ويجب أن يكون 1 إن لم تكن مجموعات الخيوط مستخدمة، كما أن تحديد نطاق خيوط أو رقم يستلزم وضع
«1/» قبله إن لم تكن مجموعات الخيوط مستخدمة. وأخيرًا، «1» يكافئ تمامًا «1/all» ويشير إلى جميع
الخيوط في المجموعة.

أمثلة:

```shell
cpu-map 1/all 0-3 # bind all threads of the first group on the
                  # first 4 CPUs

cpu-map 1/1- 0-   # will be replaced by "cpu-map 1/1-64 0-63"
                  # or "cpu-map 1/1-32 0-31" depending on the machine's
                  # word size.

# all these lines bind thread 1 to the cpu 0, the thread 2 to cpu 1
# and so on.
cpu-map auto:1/1-4   0-3
cpu-map auto:1/1-4   0-1 2-3
cpu-map auto:1/1-4   3 2 1 0
cpu-map auto:1/1-4   3,2,1,0

# bind each thread to exactly one CPU using all/odd/even keyword
cpu-map auto:1/all   0-63
cpu-map auto:1/even  0-31
cpu-map auto:1/odd   32-63

# invalid cpu-map because thread and CPU sets have different sizes.
cpu-map auto:1/1-4   0    # invalid
cpu-map auto:1/1     0-3  # invalid

# map 40 threads of those 4 groups to individual CPUs
cpu-map auto:1/1-10   0-9
cpu-map auto:2/1-10   10-19
cpu-map auto:3/1-10   20-29
cpu-map auto:4/1-10   30-39

# Map 80 threads to one physical socket and 80 others to another socket
# without forcing assignment. These are split into 4 groups since no
# group may have more than 64 threads.
cpu-map 1/1-40   0-39,80-119    # node0, siblings 0 & 1
cpu-map 2/1-40   0-39,80-119
cpu-map 3/1-40   40-79,120-159  # node1, siblings 0 & 1
cpu-map 4/1-40   40-79,120-159

```

<a id="entry-3-1-cpu-affinity"></a>

**`cpu-affinity <affinity>`**

```haproxy
cpu-affinity <affinity>
```

يحدد الكيفية التي تريد بها ربط الخيوط بوحدات المعالجة (CPU). يقبل حاليًا القيم التالية:

- per-core: سيُربط كل خيط بجميع الخيوط المادية لنواة واحدة.
- per-group: سيُربط كل خيط بجميع الخيوط المادية للمجموعة. هذا هو الافتراضي ما لم يُستخدم
  "threads-per-core 1" في «cpu-policy». يقبل «per-group» وسيطة اختيارية لتحديد كيفية تخصيص
  وحدات CPU. عندما تكون قائمة وحدات CPU أكبر من العدد الأقصى المسموح به من وحدات CPU لكل
  مجموعة ويجب تقسيمها بين مجموعات متعددة، يتيح خيار إضافي اختيار كيفية ربط المجموعات
  بتلك الوحدات:
  - auto: لن تُخصص لكل مجموعة خيوط سوى حصة عادلة من أنوية CPU المتجاورة المخصصة لها وغير
    المشتركة مع المجموعات الأخرى. هذا هو الافتراضي لأنه عمومًا أكثر ملاءمة للأداء.
  - loose: سيبقى مسموحًا لكل مجموعة باستخدام أي CPU في القائمة. هذا يسبب عادةً مزيدًا من
    التنافس، لكنه قد يساعد أحيانًا على التعامل بشكل أفضل مع الأحمال الطفيلية العاملة على
    وحدات CPU نفسها.
- auto: ستُستخدم «per-group»، ما لم يُستخدم "threads-per-core 1" في «cpu-policy»، وفي هذه
  الحالة ستُستخدم «per-core». هذا هو الافتراضي.
- per-thread: سيربط ذلك خيطًا واحدًا بخيط مادي واحد فقط. إذا استُخدم "threads-per-core 1"
  في «cpu-policy»، فسيُربط كل خيط بخيط مادي واحد من نواة مختلفة.
- per-ccx: سيُربط كل خيط بجميع الخيوط المادية لـ CCX.

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

يحدد سياسة تخصيص CPU التي سيتم استخدامها.

على الأنظمة متعددة وحدات CPU، قد توجد أسباب عديدة لعدم استخدام جميع أنوية CPU المتاحة، و/أو
لتجميعها في مجموعات خيوط مختلفة، لأجل الأداء أو زمن الاستجابة أو التكلفة أو إدارة الموارد على
مستوى النظام كله. يتيح توجيه «cpu-set» بالفعل إقصاء عدد منها، لكن بعد ذلك من الضروري تحديد
كيفية إسناد الباقي إلى الخيوط ومجموعات الخيوط.

يجري هذا الربط عادةً باستخدام توجيه «cpu-map»، وإن كان قد يصعب الحفاظ عليه خصوصًا على الأنظمة
غير المتجانسة.

يختار توجيه «cpu-policy» من بين عدد صغير من سياسات التخصيص أيها تُستخدم بدلًا من ذلك، حين لا
يُستخدم «cpu-map». السياسات التالية مدعومة حاليًا، و«performance» هي الافتراضية:

- none لا يجري أي انتقاء لاحق معين. ستكون جميع وحدات CPU الممكَّنة قابلة للاستخدام، وإذا لم
  يكن عدد الخيوط مضبوطًا فسيُضبط على عدد وحدات CPU المتاحة لكن بما لا يتجاوز 32 على الأنظمة
  32-بت أو 64 على الأنظمة 64-بت، لكل مجموعة خيوط. أما عدد مجموعات الخيوط، إن لم يكن مضبوطًا،
  فسيُضبط على 1.

- efficiency مطابق تمامًا لـ «group-by-ccx» أدناه، باستثناء أن عناقيد CPU المؤلفة من أنوية
  يفوق أداؤها بنسبة تزيد على 25% أداء النواة الأقل أداءً التالية تُقصى. هذه عادةً أنوية «big»
  أو «performance». هذا يعني أنه إذا اكتُشف أكثر من نوع واحد من أنوية CPU، فلن يُستخدم إلا
  النوع الموفّر للطاقة. قد يكون لذلك معنى مع الأحمال المعتدلة حين يلزم إتاحة الأنوية الأقوى للتطبيق أو
  لمكوّن أمان. بعض وحدات CPU الحديثة تحوي عددًا كبيرًا من هذه الأنوية الموفّرة للطاقة التي يمكنها
  مجتمعةً تقديم مستوى أداء لائق مع استهلاك طاقة أقل.

- first-usable-node إذا لم تكن وحدات CPU قد قُيدت سابقًا عند الإقلاع (باستخدام أداة «taskset»
  مثلًا)، وإذا لم يكن توجيه «nbthread» مضبوطًا، فستُستخدم أول عقدة NUMA بها وحدات CPU ممكَّنة،
  ويُستخدم هذا العدد من وحدات CPU كعدد للخيوط. ستُمكَّن مجموعة خيوط واحدة بها جميعها، ضمن حد
  32 أو 64 بحسب النظام.

- group-by-2-ccx مماثل لـ «group-by-ccx» أدناه لكنه ينشئ مجموعة كل اثنين من CCX. قد يكون لذلك
  معنى على وحدات CPU تحمل العديد من CCX ذات الأنوية القليلة، لتجنب إنشاء مجموعات كثيرة، أو
  لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه آثار
  أداء سيئة للغاية عندما يكون التواصل بين مجمعات CCX بطيئًا. لا يوصى بهذا عمومًا.

- group-by-2-clusters مماثل لـ «group-by-cluster» لكنه ينشئ مجموعة كل اثنين من العناقيد. قد
  يكون لذلك معنى على وحدات CPU تحمل العديد من العناقيد ذات الأنوية القليلة، لتجنب إنشاء مجموعات
  كثيرة، أو لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه
  آثار أداء سيئة للغاية عندما يكون التواصل بين العناقيد بطيئًا. لا يوصى بهذا عمومًا.

- group-by-3-ccx مماثل لـ «group-by-ccx» أدناه لكنه ينشئ مجموعة كل ثلاثة من CCX. قد يكون لذلك
  معنى على وحدات CPU تحمل العديد من CCX ذات الأنوية القليلة، لتجنب إنشاء مجموعات كثيرة، أو
  لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه آثار
  أداء سيئة للغاية عندما يكون التواصل بين مجمعات CCX بطيئًا. لا يوصى بهذا عمومًا.

- group-by-3-clusters مماثل لـ «group-by-cluster» لكنه ينشئ مجموعة كل ثلاثة من العناقيد. قد
  يكون لذلك معنى على وحدات CPU تحمل العديد من العناقيد ذات الأنوية القليلة، لتجنب إنشاء مجموعات
  كثيرة، أو لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه
  آثار أداء سيئة للغاية عندما يكون التواصل بين العناقيد بطيئًا. لا يوصى بهذا عمومًا.

- group-by-4-ccx مماثل لـ «group-by-ccx» أدناه لكنه ينشئ مجموعة كل أربعة من CCX. قد يكون لذلك
  معنى على وحدات CPU تحمل العديد من CCX ذات الأنوية القليلة، لتجنب إنشاء مجموعات كثيرة، أو
  لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه آثار
  أداء سيئة للغاية عندما يكون التواصل بين مجمعات CCX بطيئًا. لا يوصى بهذا عمومًا.

- group-by-4-clusters مماثل لـ «group-by-cluster» لكنه ينشئ مجموعة كل أربعة من العناقيد. قد
  يكون لذلك معنى على وحدات CPU تحمل العديد من العناقيد ذات الأنوية القليلة، لتجنب إنشاء مجموعات
  كثيرة، أو لتنعيم التوزيع قليلًا حين لا تكون كل الأنوية مستخدمة. يُرجى ملاحظة أنه قد يترتب عليه
  آثار أداء سيئة للغاية عندما يكون التواصل بين العناقيد بطيئًا. لا يوصى بهذا عمومًا.

- group-by-ccx إذا لم يُضبط «nbthread» ولم يُضبط «nbtgroups»، فتُنشأ مجموعة خيوط واحدة لكل مركّب
  أنوية CPU («CCX») به وحدات CPU متاحة، في كل منها بعدد من الخيوط يساوي عدد وحدات CPU. يجمع
  CCX وحدات CPU ذات وصول متقارب السرعة إلى ذاكرة التخزين المؤقت من المستوى الأخير («LLC»)،
  وهي عادةً ذاكرة L3. على معظم الآلات الحديثة، يكون حرجًا للأداء ألا تُخلط وحدات CPU من مجمعات
  CCX متباعدة في مجموعة الخيوط نفسها. تُربط عندئذٍ جميع خيوط المجموعة بجميع وحدات CPU في CCX
  بحيث تبقى اتصالات ما داخل المجموعة محلية على CCX دون فرض ربط شديد الصرامة. تُحترم حدود
  الخيوط لكل مجموعة وحدود مجموعات الخيوط. يوصى بهذا على الأنظمة متعددة المقابس وأنظمة NUMA،
  وكذلك على وحدات CPU ذات أزمنة استجابة سيئة بين مجمعات CCX.

- group-by-cluster إذا لم يُضبط «nbthread» ولم يُضبط «nbtgroups»، فتُنشأ مجموعة خيوط واحدة لكل
  عنقود CPU به وحدات CPU متاحة، في كل منها بعدد من الخيوط يساوي عدد وحدات CPU. تُربط جميع
  خيوط المجموعة بجميع وحدات CPU في العنقود بحيث تبقى اتصالات ما داخل المجموعة محلية على العنقود
  دون فرض ربط شديد الصرامة. تُحترم حدود الخيوط لكل مجموعة وحدود مجموعات الخيوط. يوصى بهذا على
  الأنظمة متعددة المقابس وأنظمة NUMA، وكذلك على وحدات CPU ذات أزمنة استجابة سيئة بين مجمعات
  CCX. على معظم آلات الخوادم، العناقيد ومجمعات CCX الشيء نفسه، لكن على الآلات غير المتجانسة
  («performance» مقابل «efficiency» أو «big» مقابل «little»)، سيتكون العنقود عمومًا من جزء فقط
  من CCX مؤلف من وحدات CPU متشابهة جدًا فقط (النوع نفسه، بفارق تردد أقصاه +/-5%). يظهر الفرق
  على الحواسيب المحمولة وسطح المكتب الحديثة التي يستخدمها المطورون والمديرون للتحقق من
  الإعدادات.

- performance مطابق تمامًا لـ «group-by-ccx» أعلاه، باستثناء أن عناقيد CPU المؤلفة من أنوية
  يقل أداؤها عن 80% من أداء النواة الأكثر أداءً التالية تُقصى. هذه عادةً أنوية «little» أو
  «efficient»، التي لا تجلب إضافتها عمومًا مكاسب تُذكر وقد تأتي بسهولة بنتائج عكسية (مثل
  مصافحات TLS). كثيرًا ما يكون إبقاء مثل هذه الأنوية لمهام أخرى كمعالجة الشبكة أكثر فعالية
  بكثير. وعلى أنظمة التطوير، يمكن أيضًا استخدامها لتشغيل أدوات مساعدة مثل مولّدات الأحمال
  وأدوات المراقبة. هذه هي السياسة الافتراضية.

- resource هذا مشابه لـ «group-by-cluster» أعلاه، باستثناء أن أصغر عناقيد CPU وأكثرها كفاءة
  فقط سيُستخدم، بينما تُتجاهل جميع العناقيد الأخرى. يمكن استخدام هذا لتقييد استهلاك الموارد
  بالحد الأدنى الصارم الذي يظل يقدم أداءً لائقًا، مثلًا لمحاولة خفض استهلاك الطاقة أكثر أو
  تقليل عدد الأنوية اللازمة على بعض الأنظمة المستأجرة لإعداد sidecar، لتسهيل تقليص حجم النظام
  أكثر. لاحظ أنه إن وُجد عنقود واحد فقط، فسيظل يُستخدم بالكامل.

يمكن إضافة كلمة مفتاحية اختيارية هي «threads-per-core». تقبل قيمتين: «1» و«auto». إذا ضُبطت
على 1، فلن يُنشأ إلا خيط واحد لكل نواة، بصرف النظر عن عدد الخيوط المادية في النواة. وإذا ضُبطت
على auto، فسيُنشأ خيط واحد لكل خيط مادي. وإذا لم يُحدد أي انتماء، واستُخدمت threads-per-core
1، فسيكون الانتماء الافتراضي per-core.

انظر أيضًا: «cpu-map»، «cpu-set»، «nbthread»

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

يسمح بوصف رمزي لمجموعات CPU التي سيجري العمل عليها. يدعم هذا التوجيه الكلمات المفتاحية
التالية: - reset يلغي هذا أي قيد سابق ربما ورثته العملية من مدير خدمات أو من أمر «taskset»
مثلًا. - drop-cpu `<set>` لا ترتبط بوحدات CPU في هذه المجموعة - only-cpu `<set>` لا ترتبط
بوحدات CPU خارج هذه المجموعة - drop-node `<set>` لا ترتبط بوحدات CPU تنتمي إلى عقدة NUMA
هذه - only-node `<set>` لا ترتبط بوحدات CPU لا تنتمي إلى عقدة NUMA هذه - drop-cluster
`<set>` لا ترتبط بوحدات CPU في رقم هذا العنقود المادي - only-cluster `<set>` لا ترتبط
بوحدات CPU في رقم عنقود مادي آخر - drop-core `<set>` لا ترتبط بوحدات CPU في رقم هذه النواة
المادية - only-core `<set>` لا ترتبط بوحدات CPU في رقم نواة مادية أخرى - drop-thread
`<set>` لا ترتبط بوحدات CPU في رقم هذا الخيط المادي - only-thread `<set>` لا ترتبط بوحدات
CPU في رقم خيط مادي آخر. انظر أيضًا: «cpu-policy»

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

يعيّن دليلًا افتراضيًا لجلب شهادات SSL منه عند استخدام مسار نسبي مع توجيهات «crtfile» أو
«crt». المواقع المطلقة المحددة لها الأولوية وتتجاهل «crt-base».

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

يجعل العملية تتفرع إلى الخلفية. هذا هو وضع التشغيل الموصى به. يكافئ الوسيط «-D» في سطر
الأوامر. يمكن تعطيله بوسيط سطر الأوامر «-db». يُتجاهل هذا الخيار في وضع systemd.

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

افتراضيًا يحمّل HAProxy جميع الملفات المحددة بمسار نسبي من الموقع الذي بدأت منه العملية. في
بعض الحالات قد يكون من المرغوب إجبار جميع المسارات النسبية على أن تبدأ من موقع مختلف تمامًا
كما لو أن العملية بدأت من تلك المواقع. هذا ما صُنع من أجله هذا التوجيه. تقنيًا، سينفذ chdir()
مؤقتًا إلى الموقع المعين أثناء معالجة كل ملف تهيئة، وسيعود إلى الدليل الأصلي بعد معالجة كل
ملف. يأخذ وسيطة تدل على السياسة المراد استخدامها عند تحميل الملفات التي لا يبدأ مسارها بشرطة مائلة
('/'): - تشير «current» إلى أن جميع الملفات النسبية تُحمَّل من الدليل الذي بدأت منه العملية؛
وهذا هو الافتراضي.

    - تشير "config" إلى أن جميع الملفات النسبية يجب أن تُحمَّل من الدليل
      الحاوي لملف التهيئة. وتحديدًا، إذا كان ملف التهيئة
      يحتوي على شرطة مائلة ('/')، فسيُستخدم أطول جزء حتى آخر
      شرطة مائلة دليلًا يُتحول إليه، وإلا فيُستخدم الدليل
      الحالي. هذا الوضع ملائم لتجميع الخرائط وملفات الأخطاء
      والشهادات وسكربتات Lua معًا حزمًا قابلة للنقل. عند
      تحميل عدة ملفات تهيئة، يُحدَّث الدليل لكل واحد منها.

    - تشير "parent" إلى أن جميع الملفات النسبية يجب أن تُحمَّل من
      الدليل الأصل للدليل الحاوي لملف التهيئة. وتحديدًا،
      إذا كان ملف التهيئة يحتوي على شرطة مائلة ('/')، فسيُلحق ".."
      بأطول جزء حتى آخر شرطة مائلة ليُستخدم دليلًا يُتحول إليه،
      وإلا فالدليل هو "..". هذا الوضع ملائم لتجميع الخرائط
      وملفات الأخطاء والشهادات وسكربتات Lua معًا حزمًا قابلة
      للنقل، لكن بحيث يقع كل جزء في دليل فرعي مختلف
      (مثل "config/"، "certs/"، "maps/"، ...).

    - تشير "origin" إلى أن جميع الملفات النسبية يجب أن تُحمَّل من
      المسار المعين (الإلزامي). قد يُستخدم هذا لتسهيل إدارة
      عدة نسخ HAProxy مختلفة تعمل بالتوازي على نظام واحد،
      حيث تستخدم كل نسخة بادئة مختلفة لكن بقية الأقسام
      تبقى قابلة للنقل بسهولة.

يحل كل توجيه «default-path» محل أي توجيه سابق فورًا وقد يؤدي إلى التحول إلى دليل مختلف. ومع
أن هذا ينبغي دائمًا أن ينتج السلوك المرغوب، فإن استخدام عدة توجيهات default-path ليس ممارسة
جيدة أبدًا، وإن استُخدمت، فينبغي أن تظل السياسة متسقة عبر جميع ملفات التهيئة.

تحذير: بعض عناصر التهيئة مثل الخرائط أو الشهادات تُعرَّف بشكل فريد بمسارها المهيأ. باستخدام
تخطيط قابل للنقل، يصبح من الممكن أن ينتهي بعضها بالاسم الفريد نفسه، مما يصعّب تحديثها في وقت
التشغيل، خصوصًا عند تحميل عدة ملفات تهيئة من دلائل مختلفة. من الضروري الالتزام بنظام تسمية
ملفات صارم خالٍ من التصادمات قبل اعتماد المسارات النسبية. قد يتمثل نهج متين في إسباق أسماء
جميع الملفات بأسماء مواقعها المعنية، أو بفعل ذلك على مستوى الدليل.

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

يضيف نصًا يصف المثيل (instance).

يُرجى ملاحظة أنه من المطلوب تهريب بعض المحارف (# مثلًا)، وأن هذا النص يُدرج في صفحة html
لذا ينبغي عليك تجنب استخدام المحرفين "\<" و"\>".

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

يضبط مسار ملف بيانات JSON الخاص بـ DeviceAtlas الذي ستحمّله الـ API. يجب أن يكون المسار ملف
بيانات JSON صالحًا ومتاحًا لعملية HAProxy.

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

يضبط مستوى المعلومات التي تُعيدها الـ API. هذا التوجيه اختياري ومضبوط على 0 افتراضيًا إن لم
يُضبط.

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

يضبط اسم ملف تعريف الارتباط (cookie) الخاص بالعميل المستخدم للاكتشاف إن كان مكوّن DeviceAtlas
من جهة العميل قد استُخدم أثناء الطلب. هذا التوجيه اختياري ومضبوط على DAPROPS افتراضيًا إن لم
يُضبط.

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

يضبط محرف الفصل لنتائج خصائص الـ API. هذا التوجيه اختياري ومضبوط على \| افتراضيًا إن لم
يُضبط.

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

افتراضيًا، تقبل محللات DNS عناوين IPv4 وIPv6 معًا. يمكن التأثير في ذلك بالكلمات المفتاحية
«resolve-prefer» على أسطر الخوادم وكذلك بوسيطة العائلة للإجراء «do-resolve»، لكن ذلك مجرد
تفضيل لا يمنع استخدام العائلة الأخرى عندما تكون وحدها. في بعض البيئات التي لا يمكن فيها استخدام
المكدس المزدوج (dual-stack)، قد يؤدي التعثر بسجل DNS يقتصر على IPv6 ويشير إلى عنوان يتعذر الوصول إليه إلى
متاعب كبيرة لأنه سيحل محل سجل IPv4 سابق كان ربما سيواصل العمل حتى الطلب التالي. يتيح الخيار
العام «dns-accept-family» فرض استخدام عائلة عنوان واحدة فقط (أو كلتيهما). الوسيطة قائمة مفصولة
بفواصل من الكلمات التالية: - "ipv4": الاستعلام عن عناوين IPv4 وقبولها (سجلات "A") - "ipv6":
الاستعلام عن عناوين IPv6 وقبولها (سجلات "AAAA") - "auto": استخدام IPv4، وIPv6 إذا كان للنظام
بوابة افتراضية له. تُخزَّن نتيجة الفحص الأخير لمدة 30 ثانية.

عند استخدام عائلة واحدة، لن يُرسل أي طلب إلى المحللات من أجل العائلة الأخرى، وستُتجاهل أي
استجابة للعائلة الأخرى. القيمة الافتراضية منذ 3.3 هي «auto»، التي تمكن العائلتين فعليًا فقط
متى ثبت أن IPv6 قابل للتوجيه، وإلا تلتزم بـ IPv4. انظر أيضًا: «resolve-prefer»، «do-resolve»

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

يجب أن يظهر هذا التصريح قبل استخدام بعض التوجيهات الموسومة بأنها مهملة (deprecated) لكتم
التحذيرات والتأكد من أن ملف التهيئة لن يُرفض. ليست جميع التوجيهات المهملة معنية، بل فقط تلك التي
لا حل بديل لها.

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

يجب أن يظهر هذا التصريح قبل استخدام التوجيهات الموسومة بأنها تجريبية (experimental) وإلا
فسيُرفض ملف التهيئة. يُرجى ملاحظة أن الميزات التي يغطيها هذا الخيار غير مضمونة العمل جيدًا وقد
تتعطل خلال دورة الصيانة. سيتولى المطورون صيانتها بوضع بذل أقصى جهد أثناء العمل على الإصدار التالي، وسيبذلون أي جهد معقول لتجنب تعطيلها لكن دون ضمان. لهذه الأسباب، لا يُتوقع دعم هذه
الميزات بعد إصدار الإصدارة LTS التالية. يُتوقع من المستخدمين الراغبين في تجربة الميزات التجريبية
أن يترقوا بسرعة للاستفادة من التحسينات المُدخلة على تلك الميزة. لمعرفة ما إذا كان هذا التوجيه لا
يزال لازمًا، الأمر سهل: إن مُكِّن دون أن تستخدمه أي ميزة من هذا القبيل، فسيُصدر تحذير يقترح
إيقافه. فبلا أي تحذير، يعني ذلك أنه لا يزال لازمًا.

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

يسمح باستخدام وكيل خارجي لإجراء فحوصات الصحة. هذا معطل افتراضيًا كاحتياط أمني، وحتى عند
تمكينه، قد تفشل الفحوصات ما لم يُمكَّن «insecure-fork-wanted» كذلك. إذا كان البرنامج المطلق
يستخدم ملفًا تنفيذيًا setuid (وهذا ما لا ينبغي فعلًا)، فقد تحتاج أيضًا إلى ضبط
«insecure-setuid-wanted» في القسم العام. افتراضيًا، تبدأ الفحوصات ببيئة نظيفة لا تحوي سوى
المتغيرات المعرّفة في أمر «external-check» في قسم الواجهة الخلفية. قد يكون من المرغوب أحيانًا
الحفاظ على البيئة مع ذلك، مثلًا عندما تسترجع السكربتات المعقدة مساراتها أو معلوماتها الإضافية
منها. يمكن فعل ذلك بإلحاق الكلمة المفتاحية «preserve-env». لكن في هذه الحالة يوصى بشدة بعدم
التشغيل بـ setuid ولا كمستخدم مميز، إذ يعرض ذلك برنامج الفحص لهجمات محتملة. انظر «option
external-check» و«insecure-fork-wanted» و«insecure-setuid-wanted» لتفاصيل إضافية.

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

يضبط حدًا أعلى لأقصى عدد من واصفات الملفات ستستخدمه العملية، بمعزل عن حدود النظام. فبينما
يمكن استخدام «ulimit-n» و«maxconn» لفرض قيمة، حين لا يكونان مضبوطين، ستتقيد العملية بالحد
الصلب لإعداد RLIMIT_NOFILE كما يذكره «ulimit -n -H». لكن بعض أنظمة التشغيل الحديثة تسمح الآن
بقيم ضخمة للغاية هنا (في حدود المليار)، وهي ستستهلك من RAM أكثر بكثير مما ينبغي للاستخدام
الاعتيادي. وُفر إعداد fd-hard-limit لفرض سقف أقل لهذا الحد عند الحاجة. هذا يعني أنه سيحترم دائمًا
الحدود المفروضة من النظام عندما تكون أدنى من `<number>`، لكن ستُستخدم القيمة المحددة إن كانت
حدود النظام أعلى. افتراضيًا يُضبط fd-hard-limit على 1048576. يمكن تغيير هذا الافتراضي عبر
متغير وقت التجميع DEFAULT_MAXFD، الذي يمكن أن يعمل كحد أقصى للنظام (النواة) إن كان الحد الصلب
لـ RLIMIT_NOFILE ضخمًا للغاية. يتيح ضبط fd-hard-limit في القسم العام تجاوز القيمة المقدمة عبر
DEFAULT_MAXFD وقت البناء مؤقتًا. في المثال أدناه، لم يُحدد أي إعداد آخر وستتكيف قيمة maxconn
تلقائيًا مع الأدنى من «fd-hard-limit» وحد RLIMIT_NOFILE:

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

انظر أيضًا: ulimit-n، maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

يغيّر معرف المجموعة للعملية إلى `<number>`. يوصى بأن يكون معرف المجموعة مخصصًا لـ HAProxy أو
لمجموعة صغيرة من الخدمات المماثلة. يجب بدء HAProxy بمستخدم ينتمي إلى هذه المجموعة، أو
بامتيازات المستخدم الفائق. لاحظ أنه إذا بُدئ HAProxy من مستخدم له مجموعات تكميلية، فلن يكون
قادرًا على التخلي عن هذه المجموعات إلا إذا بُدئ بامتيازات المستخدم الفائق. انظر أيضًا «group»
و«uid».

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

يحدد تأخيرًا بين إشارة SIGUSR1 والإيقاف السلس الفعلي.

الوسائط:

```text
<time>  هو تأخير إضافي (بالميلي ثانية افتراضيًا) بعد استقبال إشارة SIGUSR1
        يُنتظر انقضاؤه قبل المتابعة بعملية الإيقاف السلس.
```

يُستخدم هذا للتوافق مع البيئات القديمة التي تحتاج فيها عملية haproxy إلى التوقف لكن بعض
المكونات الخارجية تحتاج إلى رصد الحالة قبل فك ارتباط المستمعين. المبدأ هو أن المتغير الداخلي
«stopping» (الذي تُبلغ عنه دالة جلب العينة «stopping») سيتحول إلى true، لكن المستمعين سيواصلون
قبول الاتصالات دون إزعاج حتى انقضاء التأخير، وبعدها يجري الإيقاف السلس الاعتيادي. يجب عدم
استخدام هذا مع العمليات التي يجري إعادة تحميلها، وإلا فسيمنع العملية القديمة من فك الارتباط،
وقد يمنع العملية الجديدة من البدء، أو يسبب متاعب ببساطة.

مثال:

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

يُرجى ملاحظة أن نهجًا أكثر مرونة ومتانة يتمثل بدلًا من ذلك في أن يضبط نظام تنسيق متغيرًا عامًا
من واجهة سطر الأوامر، ويستخدم ذلك المتغير للرد على الفحوصات الخارجية، ثم يرسل إشارة SIGUSR1
بعد تأخير.

مثال:

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

انظر أيضًا: hard-stop-after، monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

مماثل لـ «gid» لكنه يستخدم GID لاسم المجموعة `<group name>` من ‎/etc/group. انظر أيضًا «gid»
و«user».

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

لا يرفض طلبات HTTP/1.0 من نوع GET/HEAD/DELETE ذات الحمولة باستجابة HTTP بالخطأ 413 Payload
Too Large.

بينما يكون هذا مسموحًا به صراحةً في HTTP/1.1، فإن HTTP/1.0 غير واضح في هذه النقطة، وبعض
الخوادم القديمة لا تتوقع أي حمولة ولا تبحث أبدًا عن طول المتن (عبر ترويستي Content-Length أو
Transfer-Encoding). هذا يعني أن بعض الوسطاء قد يعالجون الحمولة معالجةً سليمة لطلبات HTTP/1.0
من نوع GET/HEAD/DELETE، بينما قد يتجاهلها بعضهم الآخر تمامًا. قد يؤدي ذلك إلى مشكلات أمنية
لأن هجوم تهريب الطلبات يصبح ممكنًا. لذلك، يرفض HAProxy افتراضيًا طلبات HTTP/1.0 من نوع
GET/HEAD/DELETE ذات الحمولة.

غير أن ذلك قد يشكل مشكلة مع بعض العملاء القدامى. في هذه الحالة، يمكن ضبط هذا الخيار العام.

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

كما تُلزم مواصفة HTTP/1.1 (RFC9112#6.1)، فإن وجود حقل ترويسة Transfer-Encoding وحقل ترويسة
Content-Length معًا في الرسالة نفسها يمثل خطرًا جديًا بنقل هجوم تهريب المحتوى إن وُجد أي وكيل
HTTP/1.0 في أي مكان من سلسلة المنبع أو المصب، وعند مواجهة ذلك، يجب على الوكيل إغلاق الاتصال
إغلاقًا قاطعًا بعد الاستجابة لمنع أي استغلال. لكن قد يكون لذلك أثر في الأداء على بعض العملاء
القدامى جدًا، خصوصًا إن كان عليهم إعادة التفاوض على اتصال TLS لكل طلب. وجود هذا الخيار هو
للطلب من HAProxy ألا يفرض هذه القاعدة، والاكتفاء بتنقية الرسالة مع إبقاء الاتصال حيًّا بعد
الاستجابة. لا يجوز فعل ذلك إلا عند اليقين التام من عدم وجود أي وكلاء HTTP/1.0 في السلسلة، ومن
أن جميع التنفيذات الواقعة قبل HAProxy في السلسلة متوافقة تمامًا مع HTTP/1.1 فيما يخص القواعد المطبقة على
حقول الترويسة هذه. وفي كل الأحوال، سيواصل HAProxy تجاهل وإسقاط ترويسة Content-Length الزائدة
كي لا يرتبك الطرف التالي.

عند تمكين هذا الخيار للتحايل على عميل أو خادم قديم معطوب، من المهم فهم أنه بصرف النظر عن
الحاجة إلى هذا الخيار من عدمها، فإن أي وكيل يخالف هذه القاعدة يواجه خطر اقتطاع رسائله من قبل
وكلاء قدامى يعتبرون Content-Length ويتجاهلون Transfer-Encoding، لأن الحجم التراكمي لتمثيلات أحجام
القطع المرمّزة لا يُحتسب. وعليه، فالقاعدة أعلاه ليست مسألة أمن فحسب، بل أيضًا مسألة التخلص من
الوكلاء الذين قد يواجهون متاعب تواصل بسبب عدم التوافق مع الأقدم منهم.

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

يحدد تعديل حالة الأحرف الذي سيُطبَّق، عند التمكين، على اسم الترويسة `<from>` لتغييره إلى
`<to>` قبل إرساله إلى عملاء أو خوادم HTTP/1. يجب أن يكون `<from>` بأحرف صغيرة، ويجب ألا
يختلف `<from>` و`<to>` إلا في حالة الأحرف. يمكن تكراره إذا لزم تعديل عدة أسماء ترويسات. لا
يُسمح بالمدخلات المكررة. إذا كان لا بد من تعديل الكثير من أسماء الترويسات، فقد يكون استخدام
«h1-case-adjust-file» أكثر ملاءمة. يُرجى ملاحظة أنه لن تُطبَّق أي تحويلات ما لم يُحدد «option
h1-case-adjust-bogus-client» أو «option h1-case-adjust-bogus-server» في وكيل (proxy).

لا توجد حالة أحرف قياسية لأسماء الترويسات لأنها، كما تنص RFC7230، غير حساسة لحالة الأحرف.
لذا يجب أن تعالجها التطبيقات بطريقة غير حساسة لحالة الأحرف. لكن بعض التطبيقات المعيبة تنتهك
المعايير وتعتمد خطأً على الحالات الأكثر شيوعًا لدى المتصفحات. تصبح هذه المشكلة حرجة مع HTTP/2
لأن جميع أسماء الترويسات يجب أن تُتبادل بأحرف صغيرة، ويتبع HAProxy الاتفاقية نفسها. تُرسل جميع
أسماء الترويسات بأحرف صغيرة إلى العملاء والخوادم، بغض النظر عن إصدار HTTP.

قد تتطلب التطبيقات التي تفشل في معالجة الطلبات أو الاستجابات معالجةً سليمة أن تستخدم مؤقتًا
مثل هذه الحلول الترقيعية لتعديل أسماء الترويسات المرسلة إليها إلى أن يُصلح التطبيق. يُرجى
ملاحظة أن التطبيق الذي يتطلب مثل هذه الحلول قد يكون عرضة لهجمات تهريب المحتوى ويجب إصلاحه
إصلاحًا حتميًا.

مثال:

```text
global
  h1-case-adjust content-length Content-Length
```

انظر «h1-case-adjust-file» و«option h1-case-adjust-bogus-client» و«option
h1-case-adjust-bogus-server».

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

يحدد ملفًا يحوي قائمة من أزواج مفتاح/قيمة تُستخدم لتعديل حالة أحرف بعض أسماء الترويسات قبل
إرسالها إلى عملاء أو خوادم HTTP/1. يجب أن يحوي الملف `<hdrs-file>` اسمي ترويسة في كل سطر.
يجب أن يكون الأول بأحرف صغيرة وألا يختلفا إلا في حالة الأحرف. تُتجاهل الأسطر التي تبدأ بـ
'#'، مثل الأسطر الفارغة تمامًا. تُحذف علامات الجدولة والمسافات في البداية والنهاية. لا يُسمح
بالمدخلات المكررة. يُرجى ملاحظة أنه لن تُطبَّق أي تحويلات ما لم يُحدد «option
h1-case-adjust-bogus-client» أو «option h1-case-adjust-bogus-server» في وكيل.

إذا كُرر هذا التوجيه، فلن يُعالج سوى الأخير منه. إنه بديل لتوجيه «h1-case-adjust» إذا لزم
تعديل الكثير من أسماء الترويسات. يُرجى قراءة المخاطر المرتبطة باستخدامه.

انظر «h1-case-adjust» و«option h1-case-adjust-bogus-client» و«option h1-case-adjust-bogus-server».

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

يعطّل هذا الإعلان عن دعم h2 websockets للعملاء. يمكن استخدامه للتغلب على العملاء الذين
يواجهون مشكلات عند تنفيذ معيار RFC8441 الحديث نسبيًا، مثل Firefox 88. للسماح للعملاء
بالتراجع تلقائيًا إلى http/1.1 لنفق websocket، حدد دعم h2 على سطر الربط باستخدام «alpn» دون
كلمة «proto» المفتاحية الصريحة. إذا كان هذا التصريح مفعّلًا سابقًا، فيمكن تعطيله بوضع البادئة
«no» قبل الكلمة المفتاحية.

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

يحدد أقصى وقت مسموح به لإجراء إيقاف سلس نظيف.

الوسائط:

```text
<time>  هو أقصى وقت (بالميلي ثانية افتراضيًا) يبقى خلاله المثيل حيًا عند
        استقبال طلب إيقاف سلس عبر إشارة SIGUSR1.
```

يمكن استخدام هذا لضمان أن المثيل سينتهي حتى لو بقيت اتصالات مفتوحة أثناء إيقاف سلس (مثلًا
مع مهلات طويلة لوكيل في وضع tcp). ينطبق هذا في وضعي TCP وHTTP معًا.

مثال:

```text
global
  hard-stop-after 30s
```

انظر أيضًا: grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

يبدّل حمايةً لكل بروتوكول تمنع التواصل مع العملاء الذين يستخدمون منافذ مميزة كمنفذ مصدر لهم.
هذا النطاق من المنافذ معرّف وفق RFC 6335. افتراضيًا، الحماية نشطة لبروتوكول QUIC لأن هذا
السلوك مريب وقد يُستخدم لهجوم انتحال (spoofing) أو هجوم تضخيم DNS/NTP.

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

يستبدل قائمة رموز الحالة التي تُعرّف الخطأ كما تعتبرها رموز الإنهاء والعداد «http_err_cnt» في
جداول stick، أو يقلّصها أو يوسّعها. النطاق الافتراضي للأخطاء هو من 400 إلى 499، لكن في سياقات
معينة يفضل بعض المستخدمين استبعاد رموز محددة، خصوصًا عند تتبع أخطاء العملاء (مثل 404 على
الأنظمة ذات المحتوى المولّد ديناميكيًا). انظر أيضًا «http-fail-codes» و«http_err_cnt».

النطاق المحدد دون '+' أو '-' يعيد تعريف النطاق الموجود بالنطاق الجديد. النطاق الذي يبدأ بـ
'+' يوسّع النطاق الموجود ليشمل أيضًا النطاق المحدد، الذي قد يتداخل مع الموجود أو لا. النطاق
الذي يبدأ بـ '-' يزيل النطاق المحدد من النطاق الموجود. يتكون النطاق من رقم بين 100 و599،
يتبعه اختياريًا "-" ثم رقم آخر أكبر من الأول أو يساويه للدلالة على الحد الأعلى للنطاق. يمكن
فصل نطاقات متعددة بفواصل لعملية إضافة/حذف/استبدال واحدة.

مثال:

```text
http-err-codes 400,402-444,446-480,490   # sets exactly these codes
http-err-codes 400-499 -450 +500         # sets 400 to 500 except 450
http-err-codes -450-459                  # removes 450 to 459 from range
http-err-codes +501,505                  # adds 501 and 505 to range
```

<a id="entry-3-1-http-fail-codes"></a>

**`http-fail-codes [+-]<range>[,...] [...]`**

```haproxy
http-fail-codes [+-]<range>[,...] [...]
```

يستبدل قائمة رموز الحالة التي تُعرّف الفشل كما تعتبرها رموز الإنهاء والعداد «http_fail_cnt»
في جداول stick، أو يقلّصها أو يوسّعها. النطاق الافتراضي للفشل هو من 500 إلى 599 باستثناء 501
و505 اللذين يمكن أن يثيرهما العملاء. وتدل رموز الفشل عادةً على فشل الخادم في معالجة الطلب. يفضل بعض
المستخدمين استبعاد رموز معينة في سياقات معينة يُعرف أنها غير ذات صلة، مثل 500 في بعض بيئات
SOAP لأنه لا يدل على خلل في الخادم هناك. الصياغة مطابقة تمامًا لصياغة http-err-codes أعلاه.
انظر أيضًا «http-err-codes» و«http_fail_cnt».

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

افتراضيًا، يحاول HAProxy جاهدًا منع إنشاء أي خيط أو عملية بعد بدئه. هذا مهم على وجه الخصوص
عند استخدام ملفات Lua غير مؤكدة المصدر، وعند تجربة إصدارات التطوير التي قد تظل تحوي أخطاء غير
مؤكدة القابلية للاستغلال. وعمومًا، من العادات الجيدة التأكد من عدم إمكان تحريك أي نشاط خلفي غير
متوقع بواسطة حركة البيانات. لكن هذا يمنع الفحوصات الخارجية من العمل، وقد يعطل بعض نصوص Lua
المحددة جدًا التي تعتمد فعليًا على القدرة على التفريع (fork). وجود هذا الخيار هو لتعطيل هذه
الحماية. لاحظ أن تعطيلها فكرة سيئة، إذ إن ثغرة في مكتبة أو في HAProxy نفسه ستكون أسهل استغلالًا
متى عُطّلت. إضافةً إلى ذلك، فالتفريع من Lua أو من أي مكان آخر غير موثوق لأن العملية المتفرعة قد
تتضمن عشوائيًا قفلًا ضبطه خيط آخر فلا تتمكن أبدًا من إنهاء عملية. لذا يوصى بشدة بعدم استخدام
هذا الخيار أبدًا، وإعادة النظر في أي عبء عمل يتطلب مثل هذا التفريع ونقله إلى حل أكثر أمانًا
(مثل الوكلاء بدلًا من الفحوصات الخارجية). يدعم هذا الخيار بادئة «no» لتعطيله. يمكن أيضًا
تفعيله بالخيار «-dI» على سطر أوامر haproxy.

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

لا يحتاج HAProxy إلى استدعاء ملفات تنفيذية في وقت التشغيل (إلا عند استخدام الفحوصات الخارجية
التي يُوصى بشدة بعدم استخدامها)، بل يُتوقع منه حتى أن يعزل نفسه في chroot فارغ. وعليه، لا
يوجد عمليًا سبب وجيه للسماح باستدعاء ملف تنفيذي setuid دون إدراك المستخدم التام للمخاطر. في
موقف يحتاج فيه HAProxy إلى استدعاء فحوصات خارجية و/أو تعطيل chroot، قد يؤدي استغلال ثغرة في
مكتبة أو في HAProxy نفسه إلى تنفيذ برنامج خارجي. على Linux يمكن قفل العملية بحيث تُتجاهل أي
بتة setuid موجودة على مثل هذا الملف التنفيذي. هذا يقلل كثيرًا من خطر تصعيد الامتيازات في مثل
هذا الموقف. هذا ما يفعله HAProxy افتراضيًا. في حال سبّب هذا مشكلةً لفحص خارجي (مثل فحص يحتاج
إلى أمر «ping»)، يمكن تعطيل هذه الحماية بإضافة هذا التوجيه صراحةً في القسم العام. وإذا مُكِّن،
يمكن إعادة تعطيله بوضع البادئة «no» قبله.

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

يعيّن دليلًا لتحميل سلسلة الشهادات لإكمال المُصدر. يجب أن تكون جميع الملفات بصيغة PEM. بالنسبة
للشهادات المحمّلة بـ «crt» أو «crt-list»، إذا لم تكن سلسلة الشهادة مضمنة في PEM (المعروفة
أيضًا بالشهادة الوسيطة)، فسيكمل HAProxy السلسلة إذا كان مُصدر الشهادة يقابل أول شهادة من
السلسلة المحمّلة عبر «issuers-chain-path». يمكن استبدال ملف «crt» مكوَّنٍ من
PrivateKey+Certificate+IntermediateCA2+IntermediateCA1 بـ PrivateKey+Certificate. سيكمل HAProxy
السلسلة إذا وُجد ملف بالصيغة IntermediateCA2+IntermediateCA1 في دليل «issuers-chain-path».
ستتشارك جميع الشهادات الأخرى ذات المُصدر نفسه السلسلة نفسها في الذاكرة.

تستطيع ميزات OCSP استخدام السلسلة المكتملة حين لم يُستخدم ‎.issuer، أو حين لم تُوفر سلسلة في
PEM.

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

يسمح بالرموز الموقّعة JWT بخوارزمية «none» في المحوّل 'jwt_verify'. ستُعتبر دائمًا صالحة عند
ضبط هذا الخيار. افتراضيًا تُرفض الرموز غير الموقّعة لأنها تعد غير آمنة (انظر RFC8725
[القسم 3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)).

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

يضبط قائمة الخوارزميات المسموح بها في المحوّلات jwt_decrypt_XXX. لن يُفك تشفير رموز JWT التي تستخدم
خوارزميات غير مدعومة أو معطلة أبدًا. يجب أن تكون للخوارزميات المحددة الصيغة نفسها الواردة في
[القسم 4.1](https://www.rfc-editor.org/rfc/rfc7518#section-4.1) من RFC7518 ويجب فصلها بنقطتين
رأسيتين. يمكن استخدام الاسم الخاص «ALL» لتمكين جميع الخوارزميات المدعومة (انظر المحوّل
«jwt_decrypt_jwk» للقائمة الكاملة)، ويمكن إلحاق '!' باسم خوارزمية لتعطيلها صراحةً. يُرجى
ملاحظة أنه ما لم يُحدد «ALL»، فإن استخدام هذا الخيار سيعطّل أي خوارزمية غير مذكورة صراحةً في
القائمة المقدمة.

أمثلة:

```shell
# Enable all algorithms but the "ECDH-ES" one
jwt.decrypt_alg_list ALL:!ECDH-ES

# Only enable ECDH-ES algorithms
jwt.decrypt_alg_list ECDH-ES:ECDH-ES+A128KW:ECDH-ES+A192KW:ECDH-ES+A256KW
```

<a id="entry-3-1-jwt-decrypt-enc-list"></a>

**`jwt.decrypt_enc_list <list>`**

```haproxy
jwt.decrypt_enc_list <list>
```

يضبط قائمة خوارزميات التشفير المسموح بها في المحوّلات jwt_decrypt_XXX. لن يُفك تشفير رموز JWT
التي تستخدم خوارزميات تشفير غير مدعومة أو معطلة أبدًا. يجب أن تكون للخوارزميات المحددة الصيغة
نفسها الواردة في [القسم 5.1](https://www.rfc-editor.org/rfc/rfc7518#section-5.1) من RFC7518
ويجب فصلها بنقطتين رأسيتين. يمكن استخدام الاسم الخاص «ALL» لتمكين جميع الخوارزميات المدعومة
(انظر المحوّل «jwt_decrypt_jwk» للقائمة الكاملة)، ويمكن إلحاق '!' باسم خوارزمية لتعطيلها
صراحةً. يُرجى ملاحظة أنه ما لم يُحدد «ALL»، فإن استخدام هذا الخيار سيعطّل أي خوارزمية غير
مذكورة صراحةً في القائمة المقدمة.

أمثلة:

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

يعيّن دليلًا افتراضيًا لجلب مفاتيح SSL الخاصة منه عند استخدام مسار نسبي مع توجيهات «key».
المواقع المطلقة المحددة لها الأولوية وتتجاهل «key-base». يعمل هذا الخيار فقط مع سطر تحميل
crt-store.

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

يجب استخدام هذا الإعداد لتمكين روابط مستمعي QUIC صراحةً عندما يُجمَّع haproxy بإصدار من
OpenSSL بلا دعم QUIC. يفعّل طبقة توافق داخلية في haproxy يجب أن تكون قد اختيرت وقت البناء مع
USE_QUIC_OPENSSL_COMPAT=1. تدعم طبقة التوافق هذه معظم عمليات TLS الضرورية، لكن دون قدرة
QUIC 0-RTT.

هذه الميزة موجهة بالأساس إلى OpenSSL قبل الإصدار 3.5.2، حيث لم تكن QUIC API منفذة أو كانت
منفذة جزئيًا فقط. يمكن مع ذلك تفعيل طبقة التوافق للإصدار 3.5.2 وما بعده، لكن هذا غير ضروري
على الأرجح.

إذا ضُبط limited-quic لكن طبقة التوافق لم تُختر وقت البناء، فسيُتجاهل الخيار بصمت وتعتمد عمليات
QUIC TLS على مكتبة TLS.

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

يضبط اسم النظير للمثيل المحلي. سيُتجاهل إذا حُدد وسيط سطر الأوامر «-L» أو إذا استُخدم بعد
تعريفات أقسام «peers». في مثل هذه الحالات، ستُرسل رسالة تحذير أثناء تحليل التهيئة.

سيضبط هذا الخيار أيضًا متغير البيئة HAPROXY_LOCALPEER. انظر أيضًا «-L» في دليل الإدارة وقسم
«peers» أدناه.

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

يضيف خادم syslog عامًا. يمكن تعريف عدة خوادم عامة. ستستقبل سجلات البدء والانتهاء، فضلًا عن
جميع السجلات من الوكلاء المهيئين بـ «log global». انظر خيار «log» للوكلاء لمزيد من التفاصيل.

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

يضبط حقل اسم المضيف في ترويسة syslog. إذا ضُبطت الوسيطة الاختيارية «string» فستُضبط الترويسة
على محتوى السلسلة، وإلا فسيُستخدم اسم مضيف النظام. يُستخدم عمومًا إذا لم تكن تُرحِّل السجلات
عبر خادم syslog وسيط، أو لمجرد تخصيص اسم المضيف المطبوع في السجلات.

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

يضبط حقل الوسم في ترويسة syslog إلى هذه السلسلة. افتراضيًا يكون اسم البرنامج كما أُطلق من سطر
الأوامر، وهو عادةً «haproxy». قد يفيد ذلك أحيانًا في التمييز بين عدة عمليات تعمل على المضيف
نفسه. انظر أيضًا توجيه «log-tag» الخاص بكل وكيل.

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

يحمّل هذا التوجيه العام ملف Lua وينفذه في السياق المشترك المرئي لجميع الخيوط. أي متغير يُضبط
في مثل هذا السياق مرئي من أي خيط. هذه هي أسهل طريقة موصى بها لتحميل برامج Lua، لكنها لن تتوسع
جيدًا إذا أُجري عدد كبير من استدعاءات Lua، إذ لا يمكن أن يعمل على الحالة العامة سوى خيط واحد
في كل مرة. سيرى البرنامج المحمّل بهذه الطريقة القيمة 0 دائمًا في المتغير «core.thread». يمكن
استخدام هذا التوجيه مرات عديدة.

تتاح الوسائط (args) في ملف lua باستخدام الشيفرة أدناه في متن الملف. لا تنسَ أن مصفوفات Lua
تبدأ من الفهرس 1. المتغير «local» المعرّف في ملف متاح في الملف كله وغير متاح في الملفات
الأخرى.

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

يحمّل هذا التوجيه العام ملف Lua وينفذه في كل خيط يبدأ. أي متغير عام له رؤية محلية بالخيط بحيث
قد يرى كل خيط قيمة مختلفة. لذا يوصى بشدة بعدم استخدام المتغيرات العامة في البرامج المحمّلة
بهذه الطريقة. تُحمَّل نسخة مستقلة وتُهيَّأ لكل خيط، ويجري كل شيء تتابعيًا وبالترتيب العددي
للخيوط من 1 إلى nbthread. إذا كانت بعض العمليات يجب أن تُنفَّذ مرة واحدة فقط، فينبغي للبرنامج
فحص المتغير «core.thread» ليعرف أي خيط يجري تهيئته. ستعمل البرامج المحمّلة بهذه الطريقة
بالتوازي على جميع الخيوط وستكون قابلة للتوسع بدرجة عالية. هذه هي الطريقة الموصى بها لتحميل
الدوال البسيطة التي تسجّل دوال جلب العينات أو المحوّلات أو الإجراءات أو الخدمات، متى تأكد أن
البرنامج لا يعتمد على متغيرات عامة. وتبسيطًا للأمر، يتاح التوجيه حتى لو استُخدم خيط واحد وحتى
لو كانت الخيوط معطلة (وفي هذه الحالة سيكافئ lua-load). يمكن استخدام هذا التوجيه مرات عديدة.

انظر lua-load لاستخدام الوسائط.

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

يضيف السلسلة المعطاة متبوعةً بفاصلة منقوطة إلى مقدمة متغير package.`<type>` في Lua. يجب أن
يكون `<type>` إما «path» أو «cpath». إن لم يُعطَ `<type>` فالافتراضي هو «path».

مسارات Lua قوائم أنماط مفصولة بفواصل منقوطة تحدد كيفية محاولة الدالة `require` العثور على
الملف المصدر لمكتبة. ستُستبدل علامات الاستفهام (?) داخل النمط باسم الوحدة. يُقيَّم المسار من
اليسار إلى اليمين. يعني هذا أن المسارات التي تُضاف لاحقًا إلى المقدمة سيجري فحصها في وقت
أبكر.

كمثال، بتحديد المسار التالي:

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

عند استدعاء `require "example"` ستحاول Lua أولًا تحميل السكربت ‎/usr/share/haproxy-lua/example.lua،
فإن لم يوجد ستُجرى محاولة ‎/usr/share/haproxy-lua/example/init.lua ثم المسارات الافتراضية إن لم
يوجد ذاك أيضًا.

انظر <https://www.lua.org/pil/8.1.html> للتفاصيل ضمن وثائق Lua.

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

وضع master-worker. يكافئ الوسيط «-W» في سطر الأوامر.

هذه الكلمة المفتاحية مهملة، يُرجى البدء في وضع master-worker باستخدام «-W» أو «-Ws».

سيطلق هذا الوضع «master» سيُفرّع «worker» بعد قراءة التهيئة لمعالجة حركة البيانات. يُستخدم
الـ master كمدير عمليات يراقب «workers».

باستخدام هذا الوضع، يمكنك إعادة تحميل HAProxy مباشرة بإرسال إشارة SIGUSR2 إلى الـ master.
تطلب إعادة التحميل من الـ master قراءة التهيئة مجددًا وتفريع worker جديد. سيُحتفظ بالـ worker
السابق حتى نهاية مهامه.

وضع master-worker متوافق مع الوضع الأمامي أو وضع الخدمة (daemon) كليهما.

افتراضيًا، إذا انتهى worker برمز إرجاع سيئ، في حالة خطأ تجزئة (segfault) مثلًا، فستُقتل جميع
الـ workers وسيغادر الـ master. من الملائم دمج هذا السلوك مع Restart=on-failure في ملف وحدة
systemd لإعادة إطلاق العملية بأكملها. إن لم ترغب في هذا السلوك، فيجب عليك استخدام الكلمة
المفتاحية «no-exit-on-failure».

انظر أيضًا «-W» في دليل الإدارة.

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

في وضع master-worker، افتراضيًا، إذا انتهى worker برمز إرجاع سيئ، في حالة خطأ تجزئة (segfault)
مثلًا، فستُقتل جميع الـ workers وسيغادر الـ master. من الملائم دمج هذا السلوك مع
Restart=on-failure في ملف وحدة systemd لإعادة إطلاق العملية بأكملها.

تسمح هذه الكلمة المفتاحية بإبقاء العمليات المتبقية حيةً عند انهيار worker بدلًا من قتل كل
شيء. يجب استخدامها بحذر إذ إنها مخصصة للتصحيح فقط وقد تضع العملية الرئيسية في حالة غير
طبيعية.

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

يحدد العدد الأقصى للخيوط في مجموعة خيوط. ما لم يكن عدد مجموعات الخيوط مثبتًا بتوجيه
«thread-groups»، فسينشئ haproxy من مجموعات الخيوط ما يلزم لتلبية العدد المطلوب من الخيوط.
الحد الأدنى للقيمة هو 1، والحد الأقصى هو 64 (على الأنظمة 64-بت، أو 32 على الأنظمة 32-بت).
القيم الأدنى تقلل التنافس الناجم عن العمليات الذرية على الحالات المشتركة، لكنها قد تزيد عدد
المقابس اللازمة لإنشاء جميع المستمعين ولحمل اتصالات الواجهة الخلفية الخاملة. القيم الأعلى
ستخفض هذه التكاليف على حساب استخدام أعلى لوحدة المعالجة في حالات التنافس، ومعدلات اتصال أدنى.
القيمة الافتراضية هي 16، وهي توفر أفضل موازنة وُجدت تجريبيًا على أنظمة مختلفة خضعت للاختبار،
بما فيها معالجات x86_64 من عدة مصنّعين، وأنظمة Arm64 كبيرة، على الأجهزة الفيزيائية وعلى
برامج مراقبة الأجهزة الافتراضية (hypervisors) معًا.

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

في وضع master-worker، يحدد هذا الخيار عدد المرات التي يمكن لـ worker أن ينجو فيها من إعادة
تحميل. إذا لم يغادر الـ worker بعد إعادة تحميل، فمتى صار عدد مرات إعادة تحميله أكبر من هذا
العدد، سيتلقى الـ worker إشارة SIGTERM. يساعد هذا الخيار على إبقاء عدد الـ workers تحت
السيطرة. انظر أيضًا «show proc» في دليل الإدارة.

افتراضيًا تُضبط هذه القيمة على 50.

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

هذا الإعداد متاح فقط عندما يكون دعم الخيوط قد ضُمّن عند البناء. يجعل HAProxy يعمل على
`<number>` من الخيوط. يعمل «nbthread» أيضًا عندما يُبدأ HAProxy في المقدمة. على بعض المنصات
الداعمة لانتماء CPU، تُضبط قيمة «nbthread» الافتراضية تلقائيًا على عدد وحدات CPU المرتبطة بها
العملية عند الإقلاع. هذا يعني أنه يمكن بسهولة ضبط عدد الخيوط من العملية المستدعية باستخدام
أوامر مثل «taskset» أو «cpuset». وإلا فالقيمة الافتراضية هي 1. تُذكر القيمة الافتراضية في خرج
«haproxy -vv». لاحظ أن القيم المضبوطة هنا أو المكتشفة تلقائيًا تخضع للحد المضبوط بواسطة
«thread-hard-limit» (إن ضُبط).

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

عند العمل على منصة واعية بـ NUMA، يمكّن هذا توجيهَ «cpu-policy» من فحص الطوبولوجيا واستنتاج
أفضل مجموعة من وحدات CPU لاستخدامها والعدد المقابل من الخيوط. لكن إذا كان الربط المطبق غير
أمثل على معمارية معينة، فيمكن تعطيله بالتصريح 'no numa-cpu-mapping'. لا يُطبق هذا الربط
التلقائي أيضًا إذا وُجد تصريح 'nbthread' في التهيئة، أو إذا كان انتماء العملية محددًا سلفًا،
عبر توجيه 'cpu-map' أو أداة taskset مثلًا، أو إذا ضُبط cpu-policy على أي قيمة أخرى. انظر أيضًا
«cpu-map» و«cpu-policy» و«cpu-set».

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

يعطّل ocsp-update كليًا في HAProxy. ستُتجاهل أي تهيئة ocsp-update. الافتراضي هو «off». انظر
الخيار «ocsp-update» لمزيد من المعلومات عن آلية التحديث التلقائي.

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

يسمح باستخدام وكيل HTTP لتحديثات OCSP. يعمل هذا مع HTTP فقط، ولا يُدعم HTTPS. سيسمح هذا
الخيار لمحدّث OCSP بإرسال URI مطلقة في الطلب إلى الوكيل.

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

يضبط أقصى فاصل بين تحديثين تلقائيين لاستجابة OCSP نفسها. يُعبر عن هذا الزمن بالثواني
والافتراضي 3600 (ساعة واحدة). يجب ضبطه على قيمة أعلى من «ocsp-update.mindelay». انظر الخيار
«ocsp-update» لمزيد من المعلومات عن آلية التحديث التلقائي.

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

يضبط أدنى فاصل بين تحديثين تلقائيين لاستجابة OCSP نفسها. يُعبر عن هذا الزمن بالثواني
والافتراضي 300 (5 دقائق). وهو مفيد على وجه الخصوص لاستجابات OCSP التي ليس لها أوقات انتهاء
صريحة. يجب ضبطه على قيمة أدنى من «ocsp-update.maxdelay». انظر الخيار «ocsp-update» لمزيد من
المعلومات عن آلية التحديث التلقائي.

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

يضبط وضع ocsp-update الافتراضي لجميع الشهادات المستخدمة في التهيئة. يمكن أن تتجاوزه خيارات
«ocsp-update» في crt-list. يُضبط هذا الخيار على «off» افتراضيًا. انظر الخيار «ocsp-update»
لمزيد من المعلومات عن آلية التحديث التلقائي.

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

يكتب معرفات جميع الخدمات في الملف `<pidfile>` في وضع daemon، أو يكتب معرف العملية الرئيسية في
الملف `<pidfile>` في وضع master-worker. يكافئ هذا الخيار الوسيط «-p» في سطر الأوامر. يجب أن
يكون الملف متاحًا للمستخدم الذي يبدأ العملية. انظر أيضًا «daemon» و«master-worker».

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

كان هناك خطأ في تنفيذ البروتوكول PROXY v2 في HAProxy حتى الإصدار 2.1، يتسبب في إرسال أمر
PROXY بدلًا من أمر LOCAL لفحوصات الصحة. هذه مسألة طفيفة جدًا لكنها تربك سجلات بعض الخوادم.
وللأسف اكتُشف الخطأ متأخرًا جدًا وكشف أن بعض الخوادم التي ربما اختبرت تنفيذها لبروتوكول
PROXY مقابل HAProxy فقط تفشل في معالجة أمر LOCAL كما ينبغي، وتبقى بصفة دائمة في حالة «down»
عندما يفحصها HAProxy. عند حدوث ذلك، يمكن تمكين هذا الخيار العام للعودة إلى السلوك الأقدم
(المعيب) إلى أن يُتصل بمورّدي المكونات المتأثرة ويُصلحوها. هذا الخيار معطل افتراضيًا ويعمل على
جميع الخوادم التي تحمل تصريح «send-proxy-v2».

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

يضبط متغير البيئة `<name>` إلى القيمة `<value>`. إن كان المتغير موجودًا فلن يُستبدل. تسري
التغييرات فورًا بحيث يرى السطر التالي في ملف التهيئة القيمة الجديدة. انظر أيضًا «setenv»
و«resetenv» و«unsetenv».

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

يجري فتحًا لمرة واحدة لأقصى واصف ملف، ما يؤدي إلى حجز مسبق لهياكل بيانات النواة. هذا يمنع
التوقفات القصيرة عندما يكون nbthread\>1 ويفتح HAProxy واصف ملف يتطلب من النواة توسيع هياكل
بياناتها.

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

يزيل جميع متغيرات البيئة باستثناء المحدد منها في الوسائط. يسمح باستخدام بيئة نظيفة مضبوطة
قبل تعيين قيم جديدة بـ setenv أو unsetenv. يُرجى ملاحظة أن بعض الدوال الداخلية قد تستخدم بعض
متغيرات البيئة، مثل دوال معالجة الوقت، وكذلك OpenSSL أو حتى الفحوصات الخارجية. يجب استخدام
هذا بحذر بالغ وبعد تحقق كامل فقط. تسري التغييرات فورًا بحيث يرى السطر التالي في ملف التهيئة
البيئة الجديدة. انظر أيضًا «setenv» و«presetenv» و«unsetenv».

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

يحدد بادئة الدليل التي ستُضاف إلى مقدمة أسماء جميع ملفات حالة الخوادم التي لا تبدأ بـ '/'. انظر
أيضًا «server-state-file» و«load-server-state-from-file» و«server-state-file-name».

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

يحدد المسار إلى الملف الحاوي حالة الخوادم. إذا بدأ المسار بشرطة مائلة ('/')، فيُعد مطلقًا، وإلا
فيُعد نسبيًا إلى الدليل المحدد بـ «server-state-base» (إن ضُبط) أو إلى الدليل الحالي. قبل
إعادة تحميل HAProxy، يمكن حفظ الحالة الحالية للخوادم باستخدام أمر الإحصاءات «show servers
state». يجب كتابة خرج هذا الأمر في الملف المشار إليه بـ `<file>`. عند الإقلاع، وقبل معالجة
حركة البيانات، سيقرأ HAProxy حالة كل خادم موجود في الملف ومتاح في تهيئته الجارية الحالية
ويحمّلها ويطبقها. انظر أيضًا «server-state-base» و«show servers state» و«load-server-state-from-file»
و«server-state-file-name»

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

يساعد هذا الخيار في اختيار سلوك تفريغ اللب (core dump) في حال انهيار العملية. الخيارات المتاحة
هي:

- on يفعّل هذا تفريغ اللب على مستوى العملية إن كان قد عُطّل سابقًا.

- off يعطّل هذا تفريغًا للب كان مفعّلًا سابقًا.

- libs يفعّل هذا تفريغ اللب مع نسخة مضمّنة من الملفات الثنائية والمكتبات اللازمة للتصحيح.
  قد يطلب ذلك المطوّرون. في هذه الحالة سيحاول haproxy تحميل المكتبات التي يعتمد عليها إلى
  الذاكرة والاحتفاظ بها بعناية. إذا انهارت العملية، ستُفرَّغ في اللب فلا حاجة بعد لاسترجاعها
  من نظام الملفات ولا خطر من عدم مطابقتها للب. يستهلك هذا من بضعة ميغابايتات إلى بضعة عشرات
  من الميغابايتات من ذاكرة RAM إضافية، فالأفضل عدم استخدامه على الأنظمة الصغيرة.

من الأفضل ترك هذا الخيار معطلًا افتراضيًا وتمكينه فقط بناءً على طلب مطوّر. افتراضيًا يكون
معطلًا. من دون وسيطة، يكون الافتراضي «on». إذا مُكِّن، فلا يزال بالإمكان تعطيله قسرًا بوضع
الكلمة المفتاحية «no» قبله أو بضبطه على «off». ليس له أثر في الأداء ولا في الاستقرار، لكنه
سيجهد في إعادة تمكين تفريغات اللب التي ربما عُطّلت بقيود حجم الملف (ulimit -f) أو قيود حجم اللب
(ulimit -c) أو «قابلية التفريغ» لعملية بعد تغيير UID/GID لها (مثل ‎/proc/sys/fs/suid_dumpable
على Linux). قد تظل تفريغات اللب مقيدة بصلاحيات الدليل الحالي (تحقق من أي دليل يُبدأ منه الملف)،
أو بصلاحيات دليل chroot (قد يلزم تعطيل توجيه chroot مؤقتًا أو نقله إلى موقع قابل للكتابة
مخصص)، أو بأي قيد آخر خاص بالنظام. مثلًا، تشتهر بعض توزيعات Linux باستبدال ملف اللب الافتراضي
بمسار إلى ملف تنفيذي غير مثبت على النظام أصلًا (تحقق من
‎/proc/sys/kernel/core_pattern). غالبًا ما تحل كتابة «core» أو «core.%p» أو
«/var/log/core/core.%p» ببساطة المشكلة. عند محاولة تمكين هذا الخيار انتظارًا لظهور مشكلة نادرة
مجددًا، من الجيد عادةً أن تحاول أولًا الحصول على مثل هذا التفريغ بإرسال «kill -11» مثلًا إلى
عملية «haproxy» والتحقق من أنها تترك لبًّا في المكان المتوقع عند موتها.

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

يضبط المتغير على مستوى العملية '`<var-name>`' على نتيجة تقييم تعبير العينة `<expr>`. لا يمكن
للمتغير '`<var-name>`' أن يكون إلا متغيرًا على مستوى العملية (باستخدام البادئة 'proc.'). يعمل
تمامًا مثل الإجراء 'set-var' في قواعد TCP أو HTTP، باستثناء أن التعبير يُقيَّم وقت تحليل
التهيئة وأن المتغير يُضبط فورًا. دوال جلب العينات والمحوّلات المسموح بها في التعبير هي فقط تلك
التي تستخدم بيانات داخلية، مثل 'int(value)' أو 'str(value)' عادةً. يمكن أيضًا الإشارة إلى
متغيرات مخصصة سابقًا. ستكون هذه المتغيرات عندئذٍ قابلة للقراءة (والتعديل) من مجموعات القواعد
الاعتيادية.

مثال:

```text
global
    set-var proc.current_state str(primary)
    set-var proc.prio int(100)
    set-var proc.threshold int(200),sub(proc.prio)
```

<a id="entry-3-1-set-var-fmt"></a>

**`set-var-fmt <var-name> <fmt>`**

```haproxy
set-var-fmt <var-name> <fmt>
```

يضبط المتغير على مستوى العملية '`<var-name>`' على السلسلة الناتجة عن تقييم صيغة السجل
`<fmt>`. لا يمكن للمتغير '`<var-name>`' أن يكون إلا متغيرًا على مستوى العملية (باستخدام
البادئة 'proc.'). يعمل تمامًا مثل الإجراء 'set-var-fmt' في قواعد TCP أو HTTP، باستثناء أن
التعبير يُقيَّم وقت تحليل التهيئة وأن المتغير يُضبط فورًا. دوال جلب العينات والمحوّلات
المسموح بها في التعبير هي فقط تلك التي تستخدم بيانات داخلية، مثل 'int(value)' أو 'str(value)'
عادةً. يمكن أيضًا الإشارة إلى متغيرات مخصصة سابقًا. ستكون هذه المتغيرات عندئذٍ قابلة للقراءة
(والتعديل) من مجموعات القواعد الاعتيادية. يُرجى مراجعة [القسم
8.2.6](/ar/haproxy/configuration-logging/#section-8-2-6) لتفاصيل صياغة تنسيقات السجل المخصصة.

مثال:

```text
global
    set-var-fmt proc.current_state "primary"
    set-var-fmt proc.bootid        "%pid|%t"
```

<a id="entry-3-1-setcap"></a>

**`setcap <name>[,<name>...]`**

```haproxy
setcap <name>[,<name>...]
```

يضبط قائمة بالقدرات (capabilities) التي يجب الحفاظ عليها عند البدء والعمل إما كمستخدم غير جذر
(uid \> 0)، أو عند البدء بـ uid 0 (الجذر) ثم التحويل إلى مستخدم غير جذر. افتراضيًا تُفقد جميع
الأذونات عند تحويل uid، لكن بعضها يلزم كثيرًا عند محاولة الاتصال بخادم من عنوان خارجي أثناء
العمل وكيلاً شفافًا (transparent proxying)، أو عند الارتباط بمنفذ أدنى من 1024، مثلًا عند استخدام
«tune.quic.fe.sock-per-conn default-on»، مما يؤدي إلى إعدادات تعمل بكاملها تحت uid 0. ضبط
القدرات عمومًا بديل أكثر أمانًا، إذ لن يُحفظ سوى القدرات المطلوبة. الميزة خاصة بنظام التشغيل
ولا تُمكَّن إلا على Linux عند ضبط USE_LINUX_CAP=1 وقت البناء. قائمة القدرات المدعومة تعتمد أيضًا
على نظام التشغيل وتُعدَّد برسالة الخطأ المعروضة عند تمرير اسم قدرة غير صالح أو فارغ. يمكن تمرير
قدرات متعددة مفصولة بفواصل. من بين الشائع استخدامها، تتيح «cap_net_raw» الارتباط بعنوان خارجي
بشفافية، وتتيح «cap_net_bind_service» الارتباط بمنفذ مميز وقد تستخدمها QUIC. إذا بدأت العملية
وعملت تحت المستخدم غير الجذر نفسه، فينبغي ضبط القدرات اللازمة على الملف الثنائي لـ haproxy
بأداة setcap مع هذه الكلمة المفتاحية. لمزيد من التفاصيل حول ضبط القدرات على الملف الثنائي لـ
haproxy، يُرجى مراجعة الفصل 13.1 دعم قدرات Linux في دليل الإدارة.

مثال:

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

يضبط متغير البيئة `<name>` إلى القيمة `<value>`. إن كان المتغير موجودًا، فسيُستبدل. تسري
التغييرات فورًا بحيث يرى السطر التالي في ملف التهيئة القيمة الجديدة. انظر أيضًا «presetenv»
و«resetenv» و«unsetenv».

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

عند ضبط هذا التوجيه، يمكّن استخدام الذاكرة المشتركة لتخزين عدادات الإحصاءات. يُستخدم `<name>`
كوسيطة إلى shm_open() لفتح الذاكرة المشتركة في موقع فريد. يعني ذلك أيضًا أن التوجيه متاح فقط
على الأنظمة الداعمة لـ shm_open(). عند استخدام SHM للإحصاءات، ستُخزن جميع العدادات القابلة
للمشاركة للواجهات الأمامية والخلفية والمستمعين والخوادم في SHM، بشرط أن يكون لها GUID مضبوط.
عند إعادة تحميل haproxy، ستحاول العملية الجديدة مسح SHM بحثًا عن كائنات يمكن ربطها بالكائنات
المعرّفة في التهيئة استنادًا إلى GUID والنوع، والهدف هو القدرة على الحفاظ على قيم بعض العدادات
عبر إعادة التحميل. ومن جهة أخرى، عند إيقاف haproxy إيقافًا سليمًا، تُحرَّر كائنات SHM، ما يعني
إعادة ضبط العدادات فعليًا. يمكن أيضًا إزالة الملف يدويًا قبل بدء عملية جديدة لفرض إعادة
الضبط.

انظر أيضًا «guid» و«guid-prefix» و«shm-stats-file-max-objects»

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

يحدد هذا الإعداد العدد الأقصى للكائنات التي تستطيع الذاكرة المشتركة المستخدمة للعدادات
المشتركة تخزينها لكل مجموعة خيوط. وهو مرتبط مباشرةً بالحجم الأقصى لذاكرة shm ويُستخدم لإجراء
تعيين مسبق لـ shm بحجم معين لتجنب إعادة التعيين وقت التشغيل. الافتراضي هو 2k، وهو ما
ينبغي أن يناسب معظم الإعدادات دون المخاطرة باستخدام ذاكرة غير ملائم، لكن يمكن تغييره بسهولة إن
لزم. سيشتكي haproxy أثناء الإقلاع إن كانت هذه القيمة منخفضة أكثر من اللازم لتسجيل الكائنات
المتوقع تخزينها في الذاكرة المشتركة. لا يكون ذا صلة إلا عندما يكون «shm-stats-file» معرّفًا.

انظر أيضًا «thread-groups»

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التشفير («cipher suite») التي يُتفاوض عليها خلال مصافحة SSL/TLS حتى
TLSv1.2 لجميع أسطر «bind» التي لا تحدد قوائمها صراحةً. صيغة السلسلة معرّفة في «man 1 ciphers»
من صفحات دليل OpenSSL. للمعلومات الخلفية والتوصيات انظر مثلًا
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) و
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). لضبط تشفير TLSv1.3، يُرجى
مراجعة الكلمة المفتاحية «ssl-default-bind-ciphersuites». يُرجى مراجعة الكلمة المفتاحية «bind»
لمزيد من المعلومات.

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء واستُخدم OpenSSL 1.1.1 أو
أحدث لبناء HAProxy. يعيّن السلسلة الافتراضية التي تصف قائمة خوارزميات التشفير («cipher
suite») التي يُتفاوض عليها خلال مصافحة TLSv1.3 لجميع أسطر «bind» التي لا تحدد قوائمها صراحةً.
صيغة السلسلة معرّفة في «man 1 ciphers» من صفحات دليل OpenSSL تحت القسم «ciphersuites». لضبط
التشفير لـ TLSv1.2 وما قبله، يُرجى مراجعة الكلمة المفتاحية «ssl-default-bind-ciphers». قد
يقبل هذا الإعداد حزم تشفير TLSv1.2 لكن هذا سلوك غير موثق وغير موصى به لأنه قد يكون غير متسق
أو معيبًا. حزم تشفير TLSv1.3 الافتراضية في OpenSSL هي:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

يدعم TLSv1.3 فقط 5 حزم تشفير:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

يُرجى مراجعة الكلمة المفتاحية «bind» لمزيد من المعلومات.

مثال:

```text
global
    ssl-default-bind-ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

<a id="entry-3-1-ssl-default-bind-client-sigalgs"></a>

**`ssl-default-bind-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-client-sigalgs <sigalgs>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التوقيع المتعلقة بمصادقة العملاء لجميع أسطر «bind» التي لا تحدد قوائمها
صراحةً. صيغة السلسلة قائمة خوارزميات توقيع مفصولة بنقطتين رأسيتين. يمكن لكل خوارزمية توقيع أن
تتخذ إحدى صيغتين: أسماء مخططات توقيع TLS1.3 ("rsa_pss_rsae_sha256") أو صيغة خوارزمية المفتاح
العمومي + البصمة ("ECDSA+SHA256"). يمكن للقائمة أن تحوي الصيغتين معًا. لمزيد من المعلومات عن
الصيغة، انظر SSL_CTX_set1_client_sigalgs(3). تتوفر أيضًا قائمة خوارزميات التوقيع في RFC8446
[القسم 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) وفي OpenSSL في الملف
ssl/t1_lib.c. لا ينطبق هذا الإعداد على TLSv1.1 والإصدارات الأقدم من البروتوكول لأن خوارزميات
التوقيع لا يُتفاوض عليها بشكل منفصل في هذه الإصدارات. لا يوصى بتغيير هذا الإعداد ما لم تكن التوافقية
مع صندوق وسيط (middlebox) مطلوبة.

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات المنحنيات الإهليلجية («curve suite») التي يُتفاوض عليها خلال مصافحة SSL/TLS
مع ECDHE. صيغة السلسلة قائمة بأسماء منحنيات مفصولة بنقطتين رأسيتين. يُرجى مراجعة الكلمة
المفتاحية «bind» لمزيد من المعلومات.

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن خيارات ssl افتراضية
تُفرض على جميع أسطر «bind». يُرجى مراجعة الكلمة المفتاحية «bind» للاطلاع على الخيارات
المتاحة.

مثال:

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التوقيع التي يُتفاوض عليها خلال مصافحة TLSv1.2 وTLSv1.3 لجميع أسطر
«bind» التي لا تحدد قوائمها صراحةً. صيغة السلسلة قائمة خوارزميات توقيع مفصولة بنقطتين رأسيتين.
يمكن لكل خوارزمية توقيع أن تتخذ إحدى صيغتين: أسماء مخططات توقيع TLS1.3
("rsa_pss_rsae_sha256") أو صيغة خوارزمية المفتاح العمومي + البصمة ("ECDSA+SHA256"). يمكن
للقائمة أن تحوي الصيغتين معًا. لمزيد من المعلومات عن الصيغة، انظر SSL_CTX_set1_sigalgs(3).
تتوفر أيضًا قائمة خوارزميات التوقيع في RFC8446
[القسم 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) وفي OpenSSL في الملف
ssl/t1_lib.c. لا ينطبق هذا الإعداد على TLSv1.1 والإصدارات الأقدم من البروتوكول لأن خوارزميات
التوقيع لا يُتفاوض عليها بشكل منفصل في هذه الإصدارات. لا يوصى بتغيير هذا الإعداد ما لم تكن التوافقية
مع صندوق وسيط (middlebox) مطلوبة.

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التشفير التي يُتفاوض عليها خلال مصافحة SSL/TLS حتى TLSv1.2 مع الخادم،
لجميع أسطر «server» التي لا تحدد قوائمها صراحةً. صيغة السلسلة معرّفة في «man 1 ciphers» من
صفحات دليل OpenSSL. للمعلومات الخلفية والتوصيات انظر مثلًا
(<https://wiki.mozilla.org/Security/Server_Side_TLS>) و
(<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). لضبط تشفير TLSv1.3، يُرجى
مراجعة الكلمة المفتاحية «ssl-default-server-ciphersuites». يُرجى مراجعة الكلمة المفتاحية
«server» لمزيد من المعلومات.

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء واستُخدم OpenSSL 1.1.1 أو
أحدث لبناء HAProxy. يعيّن السلسلة الافتراضية التي تصف قائمة خوارزميات التشفير التي يُتفاوض
عليها خلال مصافحة TLSv1.3 مع الخادم، لجميع أسطر «server» التي لا تحدد قوائمها صراحةً. صيغة
السلسلة معرّفة في «man 1 ciphers» من صفحات دليل OpenSSL تحت القسم «ciphersuites». لضبط
التشفير لـ TLSv1.2 وما قبله، يُرجى مراجعة الكلمة المفتاحية «ssl-default-server-ciphers».
يُرجى مراجعة الكلمة المفتاحية «server» لمزيد من المعلومات.

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التوقيع المتعلقة بمصادقة العملاء لجميع أسطر «server» التي لا تحدد قوائمها
صراحةً. صيغة السلسلة قائمة خوارزميات توقيع مفصولة بنقطتين رأسيتين. يمكن لكل خوارزمية توقيع أن
تتخذ إحدى صيغتين: أسماء مخططات توقيع TLS1.3 ("rsa_pss_rsae_sha256") أو صيغة خوارزمية المفتاح
العمومي + البصمة ("ECDSA+SHA256"). يمكن للقائمة أن تحوي الصيغتين معًا. لمزيد من المعلومات عن
الصيغة، انظر SSL_CTX_set1_client_sigalgs(3). تتوفر أيضًا قائمة خوارزميات التوقيع في RFC8446
[القسم 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) وفي OpenSSL في الملف
ssl/t1_lib.c. لا ينطبق هذا الإعداد على TLSv1.1 والإصدارات الأقدم من البروتوكول لأن خوارزميات
التوقيع لا يُتفاوض عليها بشكل منفصل في هذه الإصدارات. لا يوصى بتغيير هذا الإعداد ما لم تكن التوافقية
مع صندوق وسيط (middlebox) مطلوبة.

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات المنحنيات الإهليلجية («curve suite») التي يُتفاوض عليها خلال مصافحة SSL/TLS
مع ECDHE. صيغة السلسلة قائمة بأسماء منحنيات مفصولة بنقطتين رأسيتين. يُرجى مراجعة الكلمة
المفتاحية «server» لمزيد من المعلومات.

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن خيارات ssl افتراضية
تُفرض على جميع أسطر «server». يُرجى مراجعة الكلمة المفتاحية «server» للاطلاع على الخيارات
المتاحة.

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن السلسلة الافتراضية التي
تصف قائمة خوارزميات التوقيع التي يُتفاوض عليها خلال مصافحة TLSv1.2 وTLSv1.3 لجميع أسطر
«server» التي لا تحدد قوائمها صراحةً. صيغة السلسلة قائمة خوارزميات توقيع مفصولة بنقطتين
رأسيتين. يمكن لكل خوارزمية توقيع أن تتخذ إحدى صيغتين: أسماء مخططات توقيع TLS1.3
("rsa_pss_rsae_sha256") أو صيغة خوارزمية المفتاح العمومي + البصمة ("ECDSA+SHA256"). يمكن
للقائمة أن تحوي الصيغتين معًا. لمزيد من المعلومات عن الصيغة، انظر SSL_CTX_set1_sigalgs(3).
تتوفر أيضًا قائمة خوارزميات التوقيع في RFC8446
[القسم 4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) وفي OpenSSL في الملف
ssl/t1_lib.c. لا ينطبق هذا الإعداد على TLSv1.1 والإصدارات الأقدم من البروتوكول لأن خوارزميات
التوقيع لا يُتفاوض عليها بشكل منفصل في هذه الإصدارات. لا يوصى بتغيير هذا الإعداد ما لم تكن التوافقية
مع صندوق وسيط (middlebox) مطلوبة.

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يعيّن معاملات DH الافتراضية
التي تُستخدم خلال مصافحة SSL/TLS عند استخدام تبادل المفاتيح المؤقت Diffie-Hellman (DHE)،
لجميع أسطر «bind» التي لا تحدد معاملاتها صراحةً. ستتجاوزها معاملات DH المخصصة الموجودة في ملف
شهادة الربط إن وُجدت. إن لم تُحدد معاملات DH مخصصة لا باستخدام ssl-dh-param-file ولا بضبطها
مباشرةً في ملف الشهادة، فلن تُستخدم حزم تشفير DHE، إلا إذا ضُبط tune.ssl.default-dh-param. في
هذه الحالة الأخيرة ستُستخدم معاملات DH معرفة مسبقًا بالحجم المحدد. المعروف أن المعاملات
المخصصة أكثر أمانًا ولذا يوصى باستخدامها. يمكن توليد معاملات DH مخصصة باستخدام أمر OpenSSL
«openssl dhparam `<size>`»، حيث يجب أن يكون الحجم 2048 على الأقل، إذ لا ينبغي اعتبار معاملات
DH بحجم 1024-بت آمنة بعد الآن.

التوافق: `OpenSSL >= 1.1.1`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء. يسمح بتعريف سطر أوامر كامل
سيُستدعى عند تحميل شهادة مشفرة أثناء التهيئة. قد يكون الأمر سكربتًا أو أي برنامج آخر.
سيُزوَّد بمسار المفتاح الخاص المشفر كمعامل أول ثم بمعاملات «args» التي يحددها المستخدم، وعليه
أن يطبع عبارة المرور التي تتيح فك تشفير المفتاح الخاص المشفر على الخرج القياسي. لكل مفتاح خاص
مشفر جديد يُحمَّل أثناء التهيئة، سيجرب HAProxy أولًا كل عبارة مرور أخرى معروفة سابقًا لفك
تشفير المفتاح الخاص، وسيستدعي أمر عبارة المرور مجددًا في النهاية إن لم تنجح أي منها.

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء وعندما يكون إصدار OpenSSL
3.0 على الأقل. يسمح بتعريف سلسلة خصائص افتراضية تُستخدم عند جلب الخوارزميات من الموفرين
(providers). يعمل بالطريقة نفسها التي يعمل بها خيار openssl propquery ويتبع الصياغة نفسها
(الموصوفة في <https://www.openssl.org/docs/man3.0/man7/property.html>). مثلًا، إذا كان لديك
موفران محمّلان، الموفر foo والموفر الافتراضي، فإن propquery "?provider=foo" تتيح اختيار تنفيذات
الخوارزميات التي يوفرها الموفر foo افتراضيًا، والرجوع إلى تنفيذ الموفر الافتراضي إن لم
يُوجد.

التوافق: `OpenSSL >= 3.0.0`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء وعندما يكون إصدار OpenSSL
3.0 على الأقل. يسمح بتحميل موفر (provider) أثناء التهيئة. إذا نجح التحميل، فقد تُستخدم أي
قدرات يوفرها الموفر المحمّل من قبل HAProxy. يمكن تحديد عدة خيارات 'ssl-provider' في ملف تهيئة
واحد. ستُحمَّل الموفرات بترتيب ظهورها.

يُرجى ملاحظة أن تحميل موفر صراحةً يمنع OpenSSL من تحميل الموفر 'default' تلقائيًا. كذلك يسمح
OpenSSL بتعريف الموفرات الواجب تحميلها مباشرةً في ملف تهيئته (openssl.cnf مثلًا)، فليس من
الضروري استخدام خيار 'ssl-provider' هذا لتحميل الموفرات. يمكن استخدام أمر واجهة سطر الأوامر
«show ssl providers» لعرض جميع الموفرات التي حُمّلت بنجاح.

يمكن العثور على مسار البحث الافتراضي لموفر OpenSSL في خرج الأمر «openssl version -a». إذا كان
الموفر في دليل آخر، فيمكنك ضبط متغير البيئة OPENSSL_MODULES، الذي يأخذ الدليل الذي يمكن العثور
فيه على موفرك.

انظر أيضًا «ssl-propquery» و«ssl-provider-path».

التوافق: `OpenSSL >= 3.0.0`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

هذا الإعداد متاح فقط عندما يكون دعم OpenSSL قد ضُمّن عند البناء وعندما يكون إصدار OpenSSL
3.0 على الأقل. يسمح بتحديد مسار البحث الذي سيستخدمه OpenSSL للبحث عن الموفرات. يعمل بالطريقة
نفسها التي يعمل بها متغير البيئة OPENSSL_MODULES. سيُستخدم لأي خيار 'ssl-provider' لاحق أو إلى
أن يُعرَّف 'ssl-provider-path' جديد. انظر أيضًا «ssl-provider».

التوافق: `OpenSSL >= 3.0.0`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

يسمح هذا الإعداد بضبط الطريقة التي يجري بها HAProxy البحث عن ملفات SSL الإضافية. افتراضيًا
يضيف HAProxy امتدادًا جديدًا إلى اسم الملف. (مثال: مع "foobar.crt" يحمّل "foobar.crt.key").
بتمكين هذا الخيار، يزيل HAProxy الامتداد قبل إضافة الامتداد الجديد (مثال: مع "foobar.crt"
يحمّل "foobar.key").

يجب أن يكون لملف crt امتداد «.crt» ليعمل هذا الخيار.

هذا الخيار غير متوافق مع امتدادات الحزم (.ecdsa, .rsa. .dsa) ولن يحاول إزالتها.

هذا الخيار معطل افتراضيًا. انظر أيضًا «ssl-load-extra-files».

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

يغيّر هذا الإعداد الطريقة التي سيبحث بها HAProxy عن الملفات غير المحددة أثناء تحميل شهادات
SSL. ينطبق هذا الخيار على الشهادات المرتبطة بأسطر «bind» وكذلك أسطر «server»، لكن بعض الملفات
الإضافية لن يكون لها أي أثر وظيفي على شهادات أسطر «server».

افتراضيًا، يكتشف HAProxy تلقائيًا الكثير من الملفات غير المحددة في التهيئة، وقد ترغب في تعطيل
هذا السلوك إذا أردت تحسين زمن الإقلاع.

«none»: يحمّل فقط الملفات المحددة في التهيئة. لا يحاول تحميل حزمة شهادات إن لم يكن الملف
موجودًا. في حالة دليل، لن يحاول تجميع الشهادات في حزمة إن كان لها اسم الأساس نفسه.

«all»: هذا هو السلوك الافتراضي، سيحاول تحميل كل شيء: الحزم وsctl وocsp وissuer وkey.

«bundle»: عندما لا يكون ملف محدد في التهيئة موجودًا، سيحاول HAProxy تحميل «حزمة شهادات» (cert
bundle). تُدار حزم الشهادات على جانب الواجهة الأمامية فقط ولن تعمل لشهادات الواجهة الخلفية.

بدءًا من HAProxy 2.3، لا تُحمَّل الحزم في مخزن شهادات OpenSSL نفسه، بل يحمّل كل شهادة في مخزن
منفصل، وهو ما يكافئ التصريح بعدة «crt». يتطلب ذلك OpenSSL 1.1.1. ما يعني أن الحزم تستخدم الآن
للتوافق مع الإصدارات السابقة فقط ولم تعد إلزامية لعمل تهيئة ربط هجينة RSA/ECC.

لربط ملفات PEM هذه في «حزمة شهادات» يتعرّف عليها HAProxy، يجب تسميتها بالطريقة التالية: يجب
أن يكون لجميع ملفات PEM المراد تجميعها اسم الأساس نفسه، مع لاحقة تدل على نوع المفتاح. حاليًا،
تُدعم ثلاث لاحقات: rsa وdsa وecdsa. مثلًا، إذا كان [www.example.com](http://www.example.com)
يملك ملفي PEM، ملف RSA وملف ECDSA، فيجب تسميتهما "example.pem.rsa" و"example.pem.ecdsa".
الجزء الأول من اسم الملف اعتباطي؛ اللاحقة وحدها هي المهمة. لتحميل هذه الحزمة في HAProxy، حدد
اسم الأساس فقط:

مثال: bind :8443 ssl crt example.pem

لاحظ أن اللاحقة لا تُمرر إلى HAProxy؛ هذا يخبر HAProxy بالبحث عن حزمة شهادات.

سيحمّل HAProxy جميع ملفات PEM في الحزمة وكأنها مهيأة بشكل منفصل في عدة «crt».

لم يعد لتحميل الحزم أي أثر على تحميل الدلائل لأن الملفات تُحمَّل بشكل منفصل.

على واجهة سطر الأوامر، تُرى الحزم ملفات منفصلة، ويلزم امتداد الحزمة لتثبيتها (commit).

تُدعم ملفات OCSP ‎(.ocsp) وملفات المُصدر ‎(.issuer) وشفافية الشهادات (Certificate Transparency)
‎(.sctl) والمفاتيح الخاصة ‎(.key) مع التجميع متعدد الشهادات.

«sctl»: يحاول تحميل "`<basename>`.sctl" لكل كلمة مفتاحية crt. إن قُدِّم لشهادة واجهة خلفية،
فسيُحمَّل لكن دون أي أثر وظيفي.

«ocsp»: يحاول تحميل "`<basename>`.ocsp" لكل كلمة مفتاحية crt. إن قُدِّم لشهادة واجهة خلفية،
فسيُحمَّل لكن دون أي أثر وظيفي.

«issuer»: يحاول تحميل "`<basename>`.issuer" إن لم يكن مُصدر ملف OCSP مقدَّمًا في ملف PEM. إن
قُدِّم لشهادة واجهة خلفية، فسيُحمَّل لكن دون أي أثر وظيفي.

«key»: إن لم يقدّم ملف PEM المفتاح الخاص، فحاول تحميل ملف "`<basename>`.key" يحوي مفتاحًا
خاصًا.

السلوك الافتراضي هو «all».

مثال:

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

انظر أيضًا: «crt»، و[القسم 5.1](/ar/haproxy/bind-and-server-options/#section-5-1) حول خيارات
الربط و[القسم 5.2](/ar/haproxy/bind-and-server-options/#section-5-2) حول خيارات الخادم.

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

يسمح هذا التوجيه باختيار مستوى أمان OpenSSL كما هو موصوف في
<https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html> سيُطبَّق مستوى
الأمان على كل سياقات SSL في HAProxy. تُدعم القيم بين 0 و5 فقط.

تعتمد القيمة الافتراضية على إصدار OpenSSL لديك والتوزيعة وكيف جُمِّعت المكتبة.

يتطلب هذا التوجيه OpenSSL 1.1.1 على الأقل.

التوافق: `OpenSSL >= 1.1.1`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

السلوك الافتراضي للتحقق من SSL على جانب الخوادم. إذا حُدد 'none'، فلا يُتحقق من شهادات الخوادم.
الافتراضي هو 'required' إلا إذا فُرض باستخدام خيار سطر الأوامر '-dV'.

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

شهادة جهة التصديق ذاتية الإصدار، المعروفة بشهادة الجذر x509 root CA، هي مرساة التحقق من السلسلة:
لا فائدة من أن يرسلها الخادم، إذ يجب أن تكون لدى العميل. تحتاج التهيئة القياسية إلى عدم تضمين مثل هذه
الشهادة في ملف PEM. يتيح لك هذا الخيار إبقاء مثل هذه الشهادة في ملف PEM دون إرسالها إلى العميل.
حالة الاستخدام هي توفير مُصدر لـ ocsp دون الحاجة إلى ملف '.issuer' والقدرة على مشاركته مع
'issuers-chain-path'. يخص هذا جميع الشهادات بلا شهادات وسيطة. لا فائدة منه مع BoringSSL، إذ
يُتجاهل .issuer لأن أجزاء ocsp لا تحتاجه. يتطلب OpenSSL 1.0.2 على الأقل.

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

يُفعّل أو يعطّل حساب عدادات الإحصاءات القصوى (max counters). إن لم تكن بحاجة إليها، فقد يزيد
تعطيلها الأداء قليلًا. الافتراضي هو «on» (مُمكَّن).

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

افتراضيًا، مقبس الإحصاءات مقيد بـ 10 اتصالات متزامنة. يمكن تغيير هذه القيمة بـ «stats
maxconn».

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

يربط مقبس UNIX بـ `<path>` أو عنوان TCPv4/v6 بـ `<address:port>`. ستعيد الاتصالات بهذا المقبس
مخرجات إحصاءات متنوعة، بل وتسمح بإصدار بعض الأوامر لتغيير بعض إعدادات وقت التشغيل. يُرجى
مراجعة [القسم 9.3](/ar/haproxy/statistics-and-monitoring/#section-9-3) «أوامر مقبس Unix» من
دليل الإدارة لمزيد من التفاصيل.

تُدعم جميع المعاملات التي تدعمها أسطر «bind»، مثلًا لتقييد الوصول لبعض المستخدمين أو حقوق
وصولهم. يُرجى مراجعة [القسم 5.1](/ar/haproxy/bind-and-server-options/#section-5-1) لمزيد من
المعلومات.

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

المهلة الافتراضية على مقبس الإحصاءات مضبوطة على 10 ثوانٍ. يمكن تغيير هذه القيمة بـ «stats
timeout». يجب تمرير القيمة بالميلي ثانية، أو أن تُلحق بوحدة زمنية من بين { us, ms, s, m, h,
d }.

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

المسار إلى ملف إحصاءات haproxy مولَّد. عند الإقلاع سيحمّل haproxy القيم مسبقًا إلى عداداته
الداخلية. استخدم أمر واجهة سطر الأوامر «dump stats-file» لإنتاج مثل هذا الملف. انظر دليل
الإدارة لمزيد من التفاصيل.

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

يُفعّل شيفرة بديلة لإخضاع الملف الثنائي لـ haproxy للإجهاد. المستوى عدد صحيح من 0 إلى 9.
القيمة الافتراضية 0 تعطّل أي تنفيذ إجهاد. المستويات من 1 إلى 9 سترفع ضغط الإجهاد على الملف
الثنائي لـ haproxy. لاحظ أن استخدام أي مستوى موجب قد يضر بالأداء ضررًا كبيرًا. وعليه، لا ينبغي
تفعيله أبدًا إلا لغرض التصحيح وبطلب من مطوّر.

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

يجعل العملية تفشل عند الإقلاع عندما يفشل setrlimit. يحاول HAProxy ضبط أفضل setrlimit وفقًا لما
حُسب. إذا فشل، فسيُصدر تحذيرًا. وجود هذا الخيار هو لضمان فشل صريح لـ HAProxy عند فشل هذه
الحدود. وهو مُمكَّن افتراضيًا. ولا يزال بالإمكان تعطيله قسرًا بوضع الكلمة المفتاحية «no»
قبله.

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

هذا الإعداد متاح فقط عندما يكون دعم الخيوط قد ضُمّن عند البناء. يعدّد قائمة الخيوط التي ستؤلف
مجموعة الخيوط `<group>`. تبدأ أرقام الخيوط وأرقام المجموعات من 1. تُعرَّف نطاقات الخيوط إما
باستخدام رقم خيط مفرد دفعة واحدة، أو بتحديد الحدين الأدنى والأعلى مفصولين بشرطة '-' (مثل
"1-16"). ستُسند الخيوط غير المسندة تلقائيًا إلى مجموعات الخيوط غير المسندة، ولن تستقبل مجموعات
الخيوط المعرّفة بهذا التوجيه خيوطًا أكثر من المعرّف أبدًا. تعريف المجموعة نفسها مرات عدة يلغي
التعريفات السابقة بالجديد. انظر أيضًا «nbthread» و«thread-groups».

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

هذا الإعداد متاح فقط عندما يكون دعم الخيوط قد ضُمّن عند البناء. يجعل HAProxy يقسم خيوطه إلى
`<number>` من المجموعات المستقلة. حاليًا، القيمة الافتراضية هي 1. تتيح مجموعات الخيوط تقليل
المشاركة بين الخيوط للحد من التنافس، مقابل بعض الجهد الإضافي في التهيئة. وهي أيضًا الطريقة
الوحيدة لاستخدام أكثر من 64 خيطًا إذ يمكن تهيئة ما يصل إلى 64 خيطًا لكل مجموعة. يُضبط العدد
الأقصى للمجموعات وقت التجميع والافتراضي 16. انظر أيضًا «nbthread».

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

يُستخدم هذا الإعداد لفرض حد على عدد الخيوط، سواء المكتشف أو المهيأ. وهو مفيد على وجه الخصوص
على أنظمة التشغيل التي يُكتشف فيها عدد الخيوط تلقائيًا، حيث يُرغب في عدد خيوط أدنى من عدد
وحدات CPU في التهيئات العامة والقابلة للنقل. فبينما يفرض «nbthread» عددًا من الخيوط ينتج عنه
تحذير وأداء سيئ إن تجاوز وحدات CPU المتاحة، سيكتفي thread-hard-limit بتحديد القيمة القصوى ويحد
العدد تلقائيًا بألا يتجاوز هذه القيمة، لكنه لا يرفع القيم الأدنى. إذا فُرض «nbthread» على قيمة
أعلى، فتكون الغلبة لـ thread-hard-limit، ويُصدر تحذير بحيث يمكن إصلاح شذوذ التهيئة. افتراضيًا لا
يوجد حد. انظر أيضًا «nbthread».

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

يغيّر معرف المستخدم للعملية إلى `<number>`. يوصى بأن يكون معرف المستخدم مخصصًا لـ HAProxy أو
لمجموعة صغيرة من الخدمات المماثلة. يجب بدء HAProxy بامتيازات المستخدم الفائق لكي يتمكن من
التحويل إلى معرف آخر. انظر أيضًا «gid» و«user».

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

يضبط العدد الأقصى لواصفات الملفات لكل عملية إلى `<number>`. افتراضيًا يُحسب تلقائيًا، لذا
يوصى بعدم استخدام هذا الخيار. إن كان المقصود مجرد تقييد عدد واصفات الملفات، فاستخدام
«fd-hard-limit» أفضل.

لاحظ أن الخوادم الديناميكية لا تؤخذ في الحسبان في هذا الحساب التلقائي للموارد. عند استخدام
عدد كبير منها، قد يلزم تحديد هذه القيمة يدويًا.

انظر أيضًا: fd-hard-limit، maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group
`<group>` ] [ gid `<gid>` ]

يثبّت إعدادات مشتركة لمقابس UNIX الاستماعية المصرّح بها في تصريحات «bind». يُستخدم هذا بالأساس
لتبسيط التصريح بمقابس UNIX هذه وتقليل خطر الأخطاء، إذ إن هذه الإعدادات مطلوبة غالبًا لكنها خاصة
بالعملية كذلك. يمكن استخدام إعداد `<prefix>` لإجبار جميع مسارات المقابس على أن تكون نسبية إلى
ذلك الدليل. قد يلزم ذلك للوصول إلى chroot مكوّن آخر. لاحظ أن هذه المسارات تُحل قبل أن ينفّذ
HAProxy chroot على نفسه، فهي مطلقة. الإعدادات `<mode>` و`<user>` و`<uid>` و`<group>`
و`<gid>` جميعها بالمعنى نفسه لنظيراتها المستخدمة في تصريح «bind». إذا حُدد كلاهما، فلتصريح
«bind» الأولوية، ما يعني أن إعدادات «unix-bind» يمكن اعتبارها إعدادات افتراضية على مستوى
العملية.

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

يزيل متغيرات البيئة المحددة في الوسائط. قد يفيد هذا في إخفاء بعض المعلومات الحساسة التي
تُورَّث أحيانًا من بيئة المستخدم أثناء بعض العمليات. المتغيرات التي لم تكن موجودة تُتجاهل
بصمت بحيث يكون من المؤكد بعد العملية عدم بقاء أي من هذه المتغيرات. تسري التغييرات فورًا بحيث
لن يرى السطر التالي في ملف التهيئة هذه المتغيرات. انظر أيضًا «setenv» و«presetenv»
و«resetenv».

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

مماثل لـ «uid» لكنه يستخدم UID لاسم المستخدم `<user name>` من ‎/etc/passwd. انظر أيضًا «uid»
و«group».

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

لا يُسمح إلا بالحروف والأرقام والشرطة والشرطة السفلية، كما في أسماء DNS.

يفيد هذا التصريح في تهيئات التوافرية العالية حيث تتقاسم عمليتان أو أكثر أو خادمان أو أكثر
عنوان IP نفسه. بضبط اسم عقدة مختلف على جميع العقد، يصبح من السهل تمييز الخادم الذي يعالج حركة
البيانات فورًا.

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

يضبط حجم ذاكرة التخزين المؤقت لوكيل المستخدم (Useragent) في WURFL. للبحث الأسرع، يُحفظ وكلاء
المستخدم المعالجون سلفًا في ذاكرة تخزين مؤقت LRU:

- "0" : لا تُستخدم أي ذاكرة تخزين مؤقت.
- `<size>` : حجم ذاكرة التخزين المؤقت lru بالعناصر.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_WURFL=1.

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

مسار ملف بيانات WURFL لتوفير خدمات اكتشاف الأجهزة. يجب أن يكون الملف متاحًا لـ HAProxy
بالصلاحيات المناسبة.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

قائمة مفصولة بمسافات بقدرات WURFL والقدرات الافتراضية وأسماء الخصائص التي نعتزم استخدامها في
الترويسات المحقونة. تتوفر القائمة الكاملة لأسماء القدرات والقدرات الافتراضية على موقع
Scientiamobile الإلكتروني:

```text
https://www.scientiamobile.com/wurflCapability
```

خصائص WURFL الصالحة هي:

- wurfl_id يحوي معرف الجهاز للجهاز المطابق.

- wurfl_root_id يحوي معرف جذر الجهاز للجهاز المطابق.

- wurfl_isdevroot يخبر ما إذا كان الجهاز المطابق جهازًا جذريًا. القيم الممكنة هي "TRUE" أو
  "FALSE".

- wurfl_useragent وكيل المستخدم الأصلي القادم مع طلب الويب المعين هذا.

- wurfl_api_version يحوي سلسلة تمثل إصدار Libwurfl API المستخدم حاليًا.

- wurfl_info سلسلة تحوي معلومات عن ملف wurfl.xml المحلَّل ومساره الكامل.

- wurfl_last_load_time يحوي الطابع الزمني لـ UNIX لآخر مرة حُمِّل فيها WURFL بنجاح.

- wurfl_normalized_useragent وكيل المستخدم المُطبَّع (normalized).

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

محرف سيُستخدم لفصل القيم في ترويسة استجابة تحوي نتائج WURFL. إن لم يُضبط فستُستخدم فاصلة
(',') افتراضيًا.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_WURFL=1.

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

قائمة بمسارات ملفات رقع WURFL. لاحظ أن الرقع تُحمَّل أثناء الإقلاع، أي قبل chroot.

يُرجى ملاحظة أن هذا الخيار متاح فقط عندما يكون HAProxy قد جُمِّع مع USE_WURFL=1.
## 3.2. ضبط الأداء {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

في بعض الحالات، خاصة عند التعامل مع زمن استجابة منخفض على معالجات تدعم ترددًا متغيرًا أو
عند التشغيل داخل الأجهزة الافتراضية، في كل مرة تنتظر فيها العملية إدخالًا/إخراجًا (I/O)
باستخدام poller، يعود المعالج إلى وضع السكون أو يُتاح لجهاز افتراضي آخر لفترة طويلة، مما
يسبب أزمنة استجابة مرتفعة للغاية. يوفر هذا الخيار حلًا يمنع المعالج من النوم عبر استخدام
مهلة صفرية (null) على pollers في كل الأوقات. وينتج عن ذلك تقليص كبير في زمن الاستجابة
(لوحظ انخفاض بين 30 و100 ميكروثانية) مقابل خطر تعريض المعالج لارتفاع الحرارة. بل يمكن
استخدامه مع الخيوط، وفي هذه الحالة قد تتعارض الخيوط المربوطة بشكل غير صحيح بشدة، مما يؤدي
إلى أداء أسوأ وقيم مرتفعة لحقول CPU المسروقة (stolen) في مخرجات "show info"، مما يشير إلى
الخيوط التي يُساء إعدادها. من المهم ألا يُسمح بتشغيل العملية على المعالج نفسه الذي توجد
عليه مقاطعات الشبكة عند استخدام هذا الخيار. ومن الأفضل أيضًا تجنب استخدامه على عدة خيوط
CPU تتشارك النواة (core) نفسها. هذا الخيار معطل افتراضيًا. وإذا كان قد مُكن، فلا يزال
بالإمكان تعطيله قسرًا عبر تزويده بالبادئة المفتاحية "no". وتتجاهله pollers‏ "select"
و"poll".

يُعطل هذا الخيار تلقائيًا على العمليات القديمة في سياق إعادة التحميل السلسة؛ إذ يتجنب
تعارضات CPU المفرطة عندما تبقى عمليات متعددة لفترة من الوقت بانتظار انتهاء اتصالاتها
الحالية.

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

افتراضيًا، يحاول HAProxy نشر بدء فحوصات الصحة عبر أصغر فاصل زمني للفحص بين جميع الخوادم
في المجموعة (farm). والمبدأ هو تجنب إثقال الخدمات العاملة على الخادم نفسه. لكن عند
استخدام فترات فحص كبيرة (10 ثوانٍ أو أكثر)، تستغرق آخر الخوادم في المجموعة بعض الوقت قبل
أن يبدأ اختبارها، وقد يكون ذلك مشكلة. يُستخدم هذا المعامل لفرض حد أعلى للتأخير بين أول
فحص وآخر فحص، حتى إذا كانت فترات الفحص لدى الخوادم أكبر. وعندما تعمل الخوادم بفترات أقصر،
فسيتم احترام فتراتها رغم ذلك.

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

يحدد أقصى استخدام لوحدة المعالجة (CPU) يمكن أن يبلغه HAProxy قبل التوقف عن ضغط الطلبات
الجديدة أو خفض مستوى الضغط للطلبات الجارية. وهو يعمل مثل 'maxcomprate' لكنه يقيس استخدام
CPU بدلًا من عرض نطاق البيانات الواردة. تُعبر القيمة عن نسبة مئوية من استخدام CPU من قبل
HAProxy. القيمة 100 تعطل الحد. القيمة الافتراضية هي 100. تعيين قيمة أدنى سيمنع عمل الضغط
من إبطاء العملية بأكملها ومن إدخال أزمنة استجابة عالية.

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

يحدد أقصى معدل ضغط للمدخلات لكل عملية إلى `<number>` كيلوبايت في الثانية. لكل تدفق، إذا
بلغ الحد الأقصى، فسيُخفض مستوى الضغط أثناء التدفق. وإذا بلغ الحد الأقصى عند بداية تدفق،
فلن يُضغط التدفق إطلاقًا. وإذا لم يُبلغ الحد الأقصى، فسيُرفع مستوى الضغط حتى
tune.comp.maxlevel. تعني القيمة صفر عدم وجود حد، وهي القيمة الافتراضية.

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

يحدد أقصى عدد اتصالات متزامنة لكل عملية إلى `<number>`. وهو يعادل وسيطة سطر الأوامر
"-n". فالقيمة المقدمة في وسيطة سطر الأوامر عبر "-n" تتقدم على قيمة maxconn المعينة في
القسم العام (global). كما يمكن تجميع عملية HAProxy مع متغير التجميع SYSTEM_MAXCONN،
الذي يعمل حينها كحد أقصى نظامي لـ maxconn. ومرة أخرى، تسمح وسيطة سطر الأوامر "-n" في وقت
التشغيل بتجاوز حد SYSTEM_MAXCONN إن كان معينًا. ستتوقف البروكسيات عن قبول الاتصالات عند
بلوغ maxconn. يُعدل حد الواصفات الناعم للملفات للعملية (يمكن الحصول عليه بأمر "ulimit
-n") تلقائيًا وفق قيمة maxconn المقدمة. انظر أيضًا "ulimit-n". ملاحظة: لا يستطيع poller
باسم "select" استخدام أكثر من 1024 واصف ملف بشكل موثوق على بعض المنصات. إذا كانت منصتك
لا تدعم سوى select وتعرض "select FAILED" عند الإقلاع، فستحتاج إلى خفض maxconn حتى يعمل
(أقل قليلًا من 500 عمومًا). وإذا لم تُعيَّن قيمة maxconn، فستُحسب تلقائيًا استنادًا إلى
حدود الواصفات الحالية للملفات التي يذكرها أمر "ulimit -nH" (نأخذ القيمة العظمى بين
القيمتين الصلبة والناعمة)، ثم قد تُخفض القيمة التلقائية بواسطة "fd-hard-limit" وبحد
الذاكرة إن كان مفروضًا عبر خيار سطر الأوامر "-m". كما تعتمد القيمة التلقائية على حجم
المخزن المؤقت، والذاكرة المخصصة للضغط، وحجم تخزين SSL المؤقت، وعلى استخدام SSL من عدمه
وعلى maxsslconn المقترن به (الذي يمكن أن يكون تلقائيًا هو أيضًا).

انظر أيضًا: fd-hard-limit, ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

يحدد أقصى عدد اتصالات في الثانية لكل عملية إلى `<number>`. ستتوقف البروكسيات عن قبول
الاتصالات عند بلوغ هذا الحد. ويمكن استخدامه للحد من السعة الكلية بغض النظر عن سعة كل
واجهة أمامية. ومن المهم ملاحظة أن هذا لا يصلح إلا كإجراء لحماية الخدمة، إذ لن يكون
التوزيع عادلًا بالضرورة بين الواجهات الأمامية عند بلوغ الحد، لذا فمن الجيد أيضًا تحديد حد
لكل واجهة أمامية بقيمة قريبة من الحصة المتوقعة لها. كما أن خفض tune.maxaccept قد يحسن
الإنصاف.

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

يحدد أقصى عدد أنابيب (pipes) لكل عملية إلى `<number>`. حاليًا، لا تستخدم الأنابيب إلا في
وصل TCP المعتمد على النواة (kernel-based tcp splicing). وبما أن الأنبوب يحتوي واصفي ملف،
فستُرفع قيمة "ulimit-n" تبعًا لذلك. القيمة الافتراضية هي maxconn/4، التي تبدو أكثر من
كافية لمعظم الاستخدامات المكثفة. يخصص كود الوصل (splice) الأنابيب ويطلقها ديناميكيًا،
ويمكنه الرجوع إلى النسخ القياسي، لذا فإن ضبط هذه القيمة منخفضة جدًا قد يؤثر على الأداء
فقط.

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

يحدد أقصى عدد جلسات في الثانية لكل عملية إلى `<number>`. ستتوقف البروكسيات عن قبول
الاتصالات عند بلوغ هذا الحد. ويمكن استخدامه للحد من السعة الكلية بغض النظر عن سعة كل
واجهة أمامية. ومن المهم ملاحظة أن هذا لا يصلح إلا كإجراء لحماية الخدمة، إذ لن يكون
التوزيع عادلًا بالضرورة بين الواجهات الأمامية عند بلوغ الحد، لذا فمن الجيد أيضًا تحديد حد
لكل واجهة أمامية بقيمة قريبة من الحصة المتوقعة لها. كما أن خفض tune.maxaccept قد يحسن
الإنصاف.

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

يحدد أقصى عدد اتصالات SSL متزامنة لكل عملية إلى `<number>`. لا يوجد افتراضيًا أي حد خاص
بـ SSL، ما يعني أن إعداد maxconn العام سيُطبق على جميع الاتصالات. ويساعد ضبط هذا الحد على تجنب
استخدام openssl لذاكرة كثيرة ثم انهيارها عندما تعيد malloc القيمة NULL (لأنها لا تتحقق
من هذه الحالات بشكل موثوق للأسف). لاحظ أن الحد ينطبق على الاتصالات الواردة والصادرة
معًا، فيُحتسب الاتصال الذي يُفك تشفيره ثم يعاد تشفيره كاتصالي SSL. وإذا لم تُعيَّن هذه
القيمة لكن فُرض حد للذاكرة، فستُحسب هذه القيمة تلقائيًا استنادًا إلى حد الذاكرة،
وmaxconn، وحجم المخزن المؤقت، والذاكرة المخصصة للضغط، وحجم تخزين SSL المؤقت، واستخدام
SSL في الواجهات الأمامية أو الخلفية أو كليهما. وإذا لم يُحدد maxconn ولا maxsslconn مع
وجود حد للذاكرة، فسيعدل HAProxy هذه القيم تلقائيًا بحيث يمكن إجراء 100% من الاتصالات عبر
SSL دون مخاطرة، وسيراعي الجوانب التي مُكن فيها (الواجهة الأمامية، أو الخلفية، أو كلاهما).

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

يحدد أقصى عدد جلسات SSL في الثانية لكل عملية إلى `<number>`. ستتوقف مستمعات SSL عن قبول
الاتصالات عند بلوغ هذا الحد. ويمكن استخدامه للحد من استخدام SSL الإجمالي لوحدة CPU بغض
النظر عن سعة كل واجهة أمامية. ومن المهم ملاحظة أن هذا لا يصلح إلا كإجراء لحماية الخدمة،
إذ لن يكون التوزيع عادلًا بالضرورة بين الواجهات الأمامية عند بلوغ الحد، لذا فمن الجيد
أيضًا تحديد حد لكل واجهة أمامية بقيمة قريبة من الحصة المتوقعة لها. ومن المهم أيضًا ملاحظة
أن الجلسات تُحتسب قبل دخولها رصة SSL لا بعده، مما يحمي الرصة أيضًا من المصافحات المعطوبة.
كما أن خفض tune.maxaccept قد يحسن الإنصاف.

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

يحدد أقصى كمية من ذاكرة RAM بالميغابايت لكل عملية يمكن أن تستخدمها zlib. عند بلوغ الكمية
القصوى، لن تُضغط التدفقات المستقبلية طالما لا تتوفر ذاكرة RAM. وعند تعيينها 0، فلا يوجد
حد. القيمة الافتراضية هي 0. تتوفر القيمة بالبايت على مقبس UNIX عبر "show info" في سطر
"MaxZlibMemUsage"، والذاكرة التي تستخدمها zlib هي "ZlibMemUsage" بالبايت.

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

يعطل تقليم الذاكرة ("malloc_trim") في بعض اللحظات التي تُبذل فيها محاولات لاستعادة قدر
كبير من الذاكرة (عند ندرة الذاكرة أو عند إعادة التحميل). يفرض تقليم الذاكرة على مخصص
ذاكرة النظام مسح جميع المناطق غير المستخدمة وتحريرها. ويعتبر هذا عمومًا إجراء لطيفًا
لترك مزيد من الذاكرة المتاحة لعملية جديدة بينما من غير المرجح أن تستفيد منه العملية
القديمة بشكل كبير. لكن بعض الأنظمة التي تتعامل مع عشرات إلى مئات الآلاف من الاتصالات
المتزامنة قد تعاني تجزئة ذاكرة كبيرة قد تجعل عملية التحرير هذه طويلة للغاية. وخلال ذلك
الوقت، لا يمر أي قدر إضافي من حركة البيانات عبر العملية، ولا تُقبل اتصالات جديدة بعد ذلك،
وقد تفشل بعض فحوصات الصحة، بل قد ينطلق المراقب (watchdog) ويقتل العملية غير المستجيبة
تاركًا ملف تفريغ (core dump) ضخمًا. إذا حدث ذلك في أي وقت، فيُقترح استخدام هذا الخيار لتعطيل
التقليم والتوقف عن محاولة اللطف مع العملية الجديدة. لاحظ أن مخصصات الذاكرة المتقدمة لا
تعاني عادة من مثل هذه المشكلة.

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

يعطل استخدام نظام استطلاع الأحداث "epoll" على Linux. وهو يعادل وسيطة سطر الأوامر "-de".
وسيكون نظام الاستطلاع التالي المستخدم عمومًا هو "poll". انظر أيضًا "nopoll".

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

يعطل استخدام نظام استطلاع الأحداث المعتمد على منافذ الأحداث (event ports) على أنظمة
SunOS المشتقة من Solaris 10 وما بعده. وهو يعادل وسيطة سطر الأوامر "-dv". وسيكون نظام
الاستطلاع التالي المستخدم عمومًا هو "poll". انظر أيضًا "nopoll".

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

يعطل استخدام getaddrinfo(3) لحل الأسماء. وهو يعادل وسيطة سطر الأوامر "-dG". وسيُستخدم
gethostbyname(3) المهمل.

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

يعطل استخدام نظام استطلاع الأحداث "kqueue" على BSD. وهو يعادل وسيطة سطر الأوامر "-dk".
وسيكون نظام الاستطلاع التالي المستخدم عمومًا هو "poll". انظر أيضًا "nopoll".

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

يعطل استخدام ktls. وهو يعادل وسيطة سطر الأوامر "-dT".

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

يعطل استخدام نظام استطلاع الأحداث "poll". وهو يعادل وسيطة سطر الأوامر "-dp". وسيكون نظام
الاستطلاع التالي المستخدم هو "select". لا ينبغي أبدًا الحاجة إلى تعطيل "poll" لأنه متاح
على جميع المنصات التي يدعمها HAProxy. انظر أيضًا "nokqueue" و"noepoll" و"noevports".

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

يعطل استخدام SO_REUSEPORT - انظر socket(7). وهو يعادل وسيطة سطر الأوامر "-dR".

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

يعطل استخدام وصل TCP في النواة بين المقابس على Linux. وهو يعادل وسيطة سطر الأوامر
"-dS". وستُنسخ البيانات عندئذ باستخدام استدعاءات recv/send التقليدية الأكثر قابلية
للنقل. وصل TCP في النواة محدود على بعض إصدارات نواة 2.6 الحديثة جدًا. فمعظم الإصدارات
بين 2.6.25 و2.6.28 معيبة وستمرر بيانات تالفة، لذا يجب عدم استخدامها. يسهل هذا الخيار
تعطيل وصل النواة عالميًا عند الشك. انظر أيضًا "option splice-auto" و"option
splice-request" و"option splice-response".

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

يفعل ('on') أو يعطل ('off') تنميط الذاكرة لكل دالة. سيحتفظ هذا بإحصاءات استخدام استدعاءات
malloc/calloc/realloc/free في أي مكان في العملية (بما في ذلك المكتبات) وستُعرض على واجهة
CLI باستخدام الأمر "show profiling". الغرض منه أساسًا استخدامه عند ملاحظة استخدام غير
طبيعي للذاكرة لا يمكن تفسيره بالمجموعات (pools) والحاجة إلى معلومات إضافية. سيكون تأثير
الأداء عادة حوالي 1%، وربما أكثر قليلًا على الأجهزة كثيرة الخيوط، لذا فهو مناسب عمومًا
للاستخدام في الإنتاج. يمكن تحقيق الأمر نفسه في وقت التشغيل على واجهة CLI باستخدام الأمر
"set profiling memory"، يرجى الرجوع إلى دليل الإدارة.

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

يفعل ('on') أو يعطل ('off') تنميط CPU لكل مهمة. وعند التعيين إلى 'auto' يشتغل التنميط
تلقائيًا على خيط عندما يبدأ معاناته من متوسط زمن استجابة 1000 ميكروثانية أو أعلى كما
يُذكر في حقل النشاط "avg_loop_us"، وينطفئ تلقائيًا عندما يعود زمن الاستجابة إلى ما دون
990 ميكروثانية (هذه القيمة متوسط على آخر 1024 حلقة لذا فهي لا تتغير بسرعة وتميل إلى تمهيد
القمم القصيرة بشكل ملحوظ). كما قد ينطلق من تلقاء نفسه من حين لآخر على الأنظمة المثقلة، أو
الحاويات، أو الأجهزة الافتراضية، أو عند تبديل النظام إلى الذاكرة الافتراضية (swap) (ما لا
يجب أن يحدث إطلاقًا على موازن حمل).

عندما يكون تنميط المهام مفعلًا، يستطيع HAProxy أيضًا جمع الوقت الذي تقضيه كل مهمة وهي
تحمل قفلًا أو تنتظر قفلًا، وكذلك الوقت المستغرق في انتظار نجاح تخصيص ذاكرة عند عدم وجود
عنصر في ذاكرة المجموعة المؤقتة (pool cache). قد يساعد هذا أحيانًا في فهم أسباب معينة لزمن
الاستجابة. ولأجل ذلك، يمكن تمرير الكلمات المفتاحية الإضافية "lock" (لتفعيل جمع وقت
الأقفال)، و"no-lock" (لتعطيله)، و"memory" (لتفعيل جمع وقت تخصيص الذاكرة) أو "no-memory"
(لتعطيله). وهي غير مفعلة افتراضيًا لأن أثرها قد يكون غير مهمل على CPU في الأنظمة عالية
التحميل (3-10%). لاحظ أن العبء لا يؤخذ إلا عند تشغيل التنميط فعليًا، بحيث عند التشغيل في
وضع "auto" لن يظهر إلا عندما يقرر HAProxy تشغيله.

يمكن أن يكون تنميط CPU لكل مهمة مناسبًا جدًا لعرض أين يُصرف الوقت وأي الطلبات لها أي
تأثير على أي طلب آخر. سيؤثر تفعيله عادة على أداء العملية الكلي بأقل من 1%، لذا يوصى بتركه
على القيمة الافتراضية 'auto' بحيث لا يعمل إلا عند تحديد مشكلة. تتطلب هذه الميزة نظامًا
يدعم استدعاء النظام clock_gettime(2) بمعرفات الساعة CLOCK_MONOTONIC
وCLOCK_THREAD_CPUTIME_ID، وإلا فسيكون الوقت المُبلغ عنه صفرًا. يمكن تغيير هذا الخيار في
وقت التشغيل باستخدام "set profiling" على واجهة CLI.

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

أحيانًا يُستحسن تجنب إرسال فحوصات الوكيل وفحوصات الصحة إلى الخوادم على فترات زمنية
دقيقة، مثلًا عندما توجد خوادم منطقية كثيرة على الخادم المادي نفسه. وبمساعدة هذا المعامل،
يصبح ممكنًا إضافة بعض العشوائية إلى فترة الفحص بين 0 و+/- 50%. تبدو القيمة بين 2 و5 جيدة
النتائج. تبقى القيمة الافتراضية 0.

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

يعين محرك OpenSSL إلى `<name>`. يمكن الحصول على قائمة القيم الصالحة لـ `<name>` باستخدام
الأمر "openssl engine". يمكن استخدام هذا التصريح عدة مرات، وسيمكن ببساطة محركات تشفير
متعددة. الإشارة إلى محرك غير مدعوم ستمنع HAProxy من الإقلاع. لاحظ أن محركات كثيرة ستؤدي
إلى أداء HTTPS أدنى من البرمجيات الصرفة مع المعالجات الحديثة. يضبط الأمر الاختياري
"algo" الخوارزميات الافتراضية التي سيوفرها ENGINE باستخدام دالة OPENSSL‏
ENGINE_set_default_string(). القيمة "ALL" تستخدم المحرك لجميع عمليات التشفير. وإذا لم
تُحدد قائمة خوارزميات فستُستخدم قيمة "ALL". يمكن تحديد قائمة مفصولة بفواصل لخوارزميات
مختلفة، بما فيها: RSA, DSA, DH, EC, RAND, CIPHERS, DIGESTS, PKEY, PKEY_CRYPTO,
PKEY_ASN1. هذا هو التنسيق نفسه الذي يستخدمه ملف إعداد openssl:
<https://www.openssl.org/docs/man1.0.2/apps/config.html>

عطل HAProxy الإصدار 2.6 دعم المحركات في البناء الافتراضي. لا يتوفر هذا الخيار إلا عندما
يكون HAProxy مبنيًا بدعم له. وفي حالة الحاجة إلى ssl-engine يمكن إعادة بناء HAProxy
بالعلامة USE_ENGINE=1.

التوافق: `OpenSSL >= 1.1.1`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

يضيف وضع SSL_MODE_ASYNC إلى سياق SSL. يفعل هذا عمليات إدخال/إخراج TLS غير المتزامنة إذا
استخدمت محركات SSL قادرة على عدم التزامن. التنفيذ الحالي يدعم 32 محركًا كحد أقصى. لا
تدعم Openssl ASYNC API نقل مخازن القراءة/الكتابة وهي غير متوافقة مع إدارة المخازن المؤقتة
لدى HAProxy. لذا فإن الوضع غير المتزامن معطل في عمليات القراءة/الكتابة (لا يفعل إلا أثناء
المصافحات الأولية ومصافحات إعادة التفاوض).

التوافق: `OpenSSL >= 1.1.1`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

يفعل ('on') أو يعطل ('off') التمرير دون نسخ (zero-copy) للبيانات من أجل التطبيقات
الصغيرة (applets). وهو مفعل افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding.

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

يضع حدًا صارمًا على عدد المخازن المؤقتة التي يمكن تخصيصها لكل عملية. القيمة الافتراضية
صفر وتعني عدم وجود حد. سيعاد ضبط الحد تلقائيًا لتلبية المخازن المؤقتة المحجوزة للحالات
الطارئة بحيث لا يضطر المستخدم إلى إجراء حسابات معقدة. قد يكون فرض هذه القيمة مفيدًا بشكل
خاص للحد من كمية الذاكرة التي قد تستهلكها العملية مع الإبقاء على سلوك سليم. عند بلوغ هذا
الحد، تنتظر المهمة التي تطلب مخزنًا مؤقتًا تحرير مخزن آخر أولاً. معظم الوقت يكون زمن
الانتظار قصيرًا جدًا وغير محسوس ما دامت الحدود معقولة. لكن بعض القيود التاريخية أضعفت هذه
الآلية عبر الإصدارات ومن المعلوم أنه في حالات معينة من النقص المستمر، قد تتجمد بعض المهام
حتى انقضاء مهلتها، لذا فمن الأسلم تجنب استخدام هذا عندما لا يكون ضروريًا تمامًا.

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

يحدد عدد المخازن المؤقتة لكل خيط التي تخصص مسبقًا وتحجز للاستخدام فقط خلال حالات ندرة
الذاكرة التي تؤدي إلى فشل تخصيص الذاكرة. الحد الأدنى 0 والافتراضي 4. لا سبب يدفع مستخدمًا
إلى تغيير هذه القيمة، إلا إذا اقترح مطور أساسي تغييرها لسبب محدد جدًا.

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

يضبط حجم المخزن المؤقت إلى هذا الحجم (بالبايت). تسمح القيم الأدنى بتعايش تدفقات أكثر في
الكمية نفسها من ذاكرة RAM، وتسمح القيم الأعلى بعمل بعض التطبيقات ذات الكوكيز الكبيرة
جدا. القيمة الافتراضية 16384 ويمكن تغييرها وقت البناء. يوصى بشدة بعدم تغيير هذا عن القيمة
الافتراضية، فالقيم المنخفضة جدًا ستكسر بعض الخدمات مثل الإحصاءات، والقيم الأكبر من الحجم
الافتراضي ستزيد استخدام الذاكرة، مما قد يتسبب في نفاد ذاكرة النظام. على الأقل ينبغي خفض
المعامل العام maxconn بالعامل نفسه الذي زيد به هذا المعامل. إضافة إلى ذلك، فإن استخدام
HTTP/2 يوجب أن تكون هذه القيمة 16384 أو أكثر. كما يجب أن تكون القيمة أقل من 256 ميغابايت
(268435456 بايت). إذا كانت كتلة ترويسة طلب HTTP أكبر من (tune.bufsize - tune.maxrewrite)،
فيرجع HAProxy خطأ HTTP 400 (Bad Request). وبالمثل إذا كانت كتلة ترويسة استجابة HTTP أكبر
من هذا الحجم، فسيرجع HAProxy خطأ HTTP 502 (Bad Gateway). لاحظ أن القيمة المعينة باستخدام
هذا المعامل ستقرب تلقائيًا إلى المضاعف الأعلى التالي للعدد 8 على الأجهزة 32-بت و16 على
الأجهزة 64-بت. انظر أيضًا: tune.bufsize.large, tune.bufsize.small.

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

يحدد الحجم بالبايت للمخازن المؤقتة الكبيرة. افتراضيًا، لا يكون دعم المخازن المؤقتة
الكبيرة مفعلًا، ويجب تفعيله صراحة بتعيين هذه القيمة.

صممت هذه المخازن المؤقتة لتستخدم في بعض السياقات المحددة التي يجب فيها تخزين مزيد من
البيانات مؤقتًا دون تغيير حجم المخازن المؤقتة العادية. لا تستخدم المخازن الكبيرة ضمنيًا.
انظر أيضًا: tune.bufsize.

لاحظ أنه عند إعداد المخازن المؤقتة الكبيرة، ستخصص ثلاثة مخازن كبيرة خاصة لكل خيط أثناء
الإقلاع للاستخدام الداخلي.

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

يحدد الحجم بالبايت للمخازن المؤقتة الصغيرة. القيمة الافتراضية هي 1024.

صممت هذه المخازن المؤقتة لتستخدم في بعض السياقات المحددة التي يكون فيها استهلاك الذاكرة
مقتصدًا لكن يبدو تخصيص مخزن كامل غير ضروري. وإذا لم يكن المخزن الصغير كافيًا مع ذلك،
فتُجرى إعادة تخصيص تلقائيًا للانتقال إلى مخزن مؤقت بالحجم القياسي.

في الوقت الحالي، يستخدمه تلقائيًا بروتوكول HTTP/3 فقط لإصدار ترويسات الاستجابة. وخلاف
ذلك، يمكن تفعيل دعم المخازن الصغيرة لبروكسيات محددة عبر الخيار "use-small-buffers". انظر
أيضًا: tune.bufsize.

انظر أيضًا: option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

يحدد الحجم الأقصى المسموح به للحمولة الممررة إلى أمر على واجهة CLI.

على واجهة CLI، يتقيد سطر الأوامر بحجم المخزن المؤقت. ويعني ذلك أن جميع الأوامر ووسائطها
يجب أن تتسع في مخزن مؤقت لمعالجتها، باستثناء الحمولة التي يمكن تمريرها إلى آخر أمر في
سطر الأوامر. يمكن تخصيص هذه الحمولة في منطقة مخصصة عند الضرورة. حجمها محدود بهذا
المعامل. القيمة الافتراضية هي 128KB.

ومع أنها ينبغي أن تكون عالية بما يكفي لأكثر الاستخدامات، إذا غُيرت هذه القيمة فيجب
اختيارها بعناية. القيمة الضخمة قد تؤثر على أداء HAProxy. وبحسب الأمر، قد تستغرق الحمولة
الضخمة وقتًا طويلًا في المعالجة وربما تؤدي إلى انطلاق المراقب (watchdog).

يرجى الرجوع إلى دليل الإدارة لتفاصيل واجهة CLI.

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

يحدد أقصى مستوى للضغط. يؤثر مستوى الضغط في استخدام CPU أثناء الضغط. تؤثر هذه القيمة في
استخدام CPU أثناء الضغط. يهيئ كل تدفق يستخدم الضغط خوارزمية الضغط بهذه القيمة. القيمة
الافتراضية هي 1.

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

لدعم الواجهات الخلفية الديناميكية، تُبقى الآن جميع أقسام defaults المسماة في الذاكرة بعد
التحليل. هذا ضروري لأن الواجهة الخلفية المضافة في وقت التشغيل يجب أن تستند إلى قسم
defaults مسمى من أجل إعدادها.

قد يستهلك هذا ذاكرة كبيرة إذا كان عدد مثيلات defaults كبيرًا. في هذه الحالة وإذا كانت
ميزة الواجهة الخلفية الديناميكية غير ضرورية، يمكن استخدام هذا الخيار لفرض حذف قسم
defaults بعد التحليل. يبقى مع ذلك إلزاميًا الإبقاء على أقسام defaults المشار إليها التي
تحتوي إعدادات لا تستطيع البروكسيات المشيرة إليها نسخها. فمثلًا، هذه هي الحالة إذا كان قسم
defaults يعرّف قواعد TCP/HTTP أو مجموعة قواعد tcpcheck.

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

يعطل التمرير السريع للبيانات. وهي آلية لتحسين تمرير البيانات عبر تمريرها مباشرة من جانب
إلى الآخر دون إيقاظ التدفق. وبفضل هذا التوجيه، يمكن تعطيل هذا التحسين. لاحظ أنه يعطل أيضًا
أي وصل TCP في النواة وكذلك التمرير دون نسخ. هذا الأمر ليس معنيًا بالاستخدام الاعتيادي،
ولن يقترحه عمومًا إلا المطورون خلال جلسات تصحيح معقدة.

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

يعطل عالميًا التمرير دون نسخ للبيانات. وهي آلية لتحسين التمرير السريع للبيانات عبر تجنب
استخدام مخزن القناة المؤقت. وبفضل هذا التوجيه، يمكن تعطيل هذا التحسين. لاحظ أنه يعطل أي
وصل TCP في النواة أيضًا.

انظر أيضًا: tune.pt.zero-copy-forwarding, tune.applet.zero-copy-forwarding,
tune.h1.zero-copy-fwd-recv, tune.h1.zero-copy-fwd-send, tune.h2.zero-copy-fwd-send,
tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

على امتداد تاريخ HAProxy، ظهرت بعض المشكلات المعقدة التي سببتها علل في آلية epoll في نواة
Linux. وهي عادة نادرة جدًا ولا يمكن إعادة إنتاجها خارج بيئة المبلغ، وقد لا يمكن التعامل
معها إلا بتعطيل epoll والانتقال إلى poll بدلًا منه، وهو غير مُرضٍ في بيئات الأداء العالي.
في كل مرة، تؤثر المشكلات في أنواع أحداث محددة جدًا (ونادرة) فقط، وتوفير إمكانية حجبها قد
يشكل حلًا أكثر قبولًا. يوفر هذا الخيار هذه الإمكانية بالسماح بتجاهل بعض الأحداث غير
الشائعة بصمت واستبدالها بإدخال (يبلغ عن حدث وارد غير محدد). والأثر هو تجنب مسارات معالجة
الأخطاء السريعة في أماكن معينة واستخدام المسارات المشتركة فقط. يجب عدم استخدام هذا مطلقًا
إلا بدعوة من خبير لتشخيص علة في النواة أو التحايل عليها.

يأخذ الخيار وسيطة واحدة وهي قائمة كلمات محددة بفواصل يشير كل منها إلى حدث سيُحجب. قائمة
الأحداث المدعومة حاليًا هي: - "err": حجب حدث EPOLLERR - "hup": حجب أحداث EPOLLHUP -
"rdhup": حجب أحداث EPOLLRDHUP

مثال:

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

يحدد عدد الأحداث التي يمكن معالجتها دفعة واحدة بواسطة معالج مهام غير متزامن (من API
باسم event_hdl). يجب أن يقع `<number>` بين 1 و10000. العدد الكبير قد يسبب تنازع الخيوط
نتيجة قيام المهمة بعمل ثقيل دون انقطاع، ومن جهة أخرى، العدد الصغير قد يؤدي إلى إعادة
جدولة المهمة باستمرار لأنها لا تستطيع استهلاك أحداث كافية في كل تشغيل ولا تستطيع مواكبة
منتج الأحداث. يمكن فرض القيمة الافتراضية وقت البناء، وإلا فهي 100.

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

إذا جُمّع مع DEBUG_FAIL_ALLOC أو شُغل مع "-dMfail"، يعطي نسبة احتمالات فشل محاولة تخصيص.
يجب أن تكون بين 0 (لا فشل) و100 (لا نجاح). هذا مفيد للتصحيح والتأكد من التعامل بلطف مع
إخفاقات الذاكرة. عند عدم التعيين، تكون النسبة 0. غير أن خيار سطر الأوامر "-dMfail" يعينها
تلقائيًا إلى نسبة فشل 1% بحيث لا يكون من الضروري تغيير الإعداد من أجل الاختبار.

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

يفعل ('on') أو يعطل ('off') وضع الاستطلاع المحفّز بالحواف (edge-triggered) للواصفات التي
تدعمه. لا يدعم هذا حاليًا إلا مع epoll. قد يقلل بشكل ملموس عدد استدعاءات epoll_ctl() ويحسن
الأداء قليلًا في سيناريوهات معينة. هذا لا يزال تجريبيًا، فقد يؤدي إلى تجمد الاتصالات إذا
كانت العلل لا تزال موجودة، وهو معطل افتراضيًا.

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

يحدد الحد الأدنى لاستخدام CPU بين 0 و100، وعنده تُقتل الاتصالات التي تُظهر اختلالات
(glitches) كثيرة جدًا. ينطبق هذا على الاتصالات التي بلغت حد اختلالاتها (glitches-threshold). في البيئات التي تتصرف فيها الاتصالات الطويلة جدًا غالبًا بشكل سيئ دون التسبب
في أي أثر على الأداء، قد يكون من المرغوب الإبقاء عليها بغض النظر عن سلوكها السيئ ما دامت
لا تؤذي، والبدء في قتل مثل هذه الاتصالات فقط عندما تصبح وحدة CPU مشغولة. يسمح هذا
المعامل بتحديد أن الاتصال الذي يبلغ حد الاختلالات سيُقتل فعليًا عندما يكون استخدام CPU
عند هذا المستوى أو أعلى، لكنه لن يُقتل أبدًا عندما يكون أدنى منه. لاحظ أن استخدام CPU يقاس لكل
خيط، فقد يُقتل اتصال واحد سيء السلوك. الافتراضي صفر، ما يعني أن الاتصال الذي يبلغ حد
الاختلالات سيُقتل تلقائيًا. قاعدة تقريبية مفيدة هي تعيين هذه القيمة إلى ضعف استخدام CPU
الملاحظ عادة، أو استخدام CPU الملاحظ عادة زائد نصف الخامل (أي إذا كانت وحدة CPU تبلغ
غالبًا 60%، فتعيين 80 هنا يمكن أن يكون منطقيًا). ليس لهذا المعامل أي أثر دون
tune.h2.fe.glitches-threshold أو tune.quic.fe.sec.glitches-threshold أو
tune.h1.fe.glitches-threshold. انظر أيضًا المعاملات العامة "tune.h2.fe.glitches-threshold" و"tune.h1.fe.glitches-threshold" و"tune.quic.fe.sec.glitches-threshold".

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

يحدد حد عدد الاختلالات على اتصال واجهة خلفية HTTP/1، وبعده يُقتل ذلك الاتصال تلقائيًا.
يتيح هذا قتل الاتصالات سيئة السلوك تلقائيًا دون الحاجة إلى كتابة قواعد صريحة لها. القيمة
الافتراضية صفر، ما يدل على عدم تعيين أي حد بحيث لا يسبب أي حدث إغلاق الاتصال. تشمل
الأحداث النموذجية الترويسات المنسقة بشكل غير صحيح التي قُبلت مع ذلك بواسطة "accept-unsafe-violations-in-http-response". أي قيمة غير صفرية هنا ينبغي غالبًا أن تكون بمئات أو
آلاف لتكون فعالة دون التأثير في الخوادم المعيبة قليلًا. من الممكن أيضًا قتل الاتصالات فقط
عندما يتجاوز استخدام CPU مستوى معينًا، باستخدام "tune.glitches.kill.cpu-usage". لاحظ أن
إغلاقًا رشيقًا يُحاول عند 75% من الحد المكون عبر الإعلان عن "Connection: close" حيث ينطبق
ذلك. يضمن هذا أن الاتصال المعيب قليلًا سيتوقف عن الاستخدام بعد بعض الوقت دون المخاطرة
بمقاطعة عمليات النقل الجارية.

انظر أيضًا: tune.h1.fe.glitches-threshold, bc_glitches، وtune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

يحدد حد عدد الاختلالات على اتصال واجهة أمامية HTTP/1 وبعده يُقتل ذلك الاتصال تلقائيًا.
يتيح هذا قتل الاتصالات سيئة السلوك تلقائيًا دون الحاجة إلى كتابة قواعد صريحة لها. القيمة
الافتراضية صفر، ما يدل على عدم تعيين أي حد بحيث لا يسبب أي حدث إغلاق الاتصال. تشمل
الأحداث النموذجية الترويسات المنسقة بشكل غير صحيح التي قُبلت مع ذلك بواسطة "accept-unsafe-violations-in-http-request". أي قيمة غير صفرية هنا ينبغي غالبًا أن تكون بمئات أو
آلاف لتكون فعالة دون التأثير في العملاء المعيبين قليلًا. من الممكن أيضًا قتل الاتصالات
فقط عندما يتجاوز استخدام CPU مستوى معينًا، باستخدام "tune.glitches.kill.cpu-usage". لاحظ
أن إغلاقًا رشيقًا يُحاول عند 75% من الحد المكون عبر الإعلان عن "Connection: close" حيث
ينطبق ذلك. يضمن هذا أن يحصل العميل غير المتوافق قليلًا على فرصة إنشاء اتصال جديد ومواصلة
العمل دون تأثر دون إطلاق الإغلاق القاسي أبدًا وبالتالي دون المخاطرة بمقاطعة عمليات النقل
الجارية.

انظر أيضًا: tune.h1.be.glitches-threshold, fc_glitches، وtune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

يفعل ('on') أو يعطل ('off') الاستقبال دون نسخ للبيانات من أجل مُضاعِف H1 (multiplexer).
وهو مفعل افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

يفعل ('on') أو يعطل ('off') الإرسال دون نسخ للبيانات من أجل مُضاعِف H1. وهو مفعل
افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

يحدد حد عدد الاختلالات على اتصال واجهة خلفية، وعنده يُقتل ذلك الاتصال تلقائيًا. يتيح هذا
قتل الاتصالات سيئة السلوك تلقائيًا دون الحاجة إلى كتابة قواعد صريحة لها. القيمة الافتراضية
صفر، ما يدل على عدم تعيين أي حد بحيث لا يسبب أي حدث إغلاق الاتصال. احترس من أن بعض خوادم
H2 قد تسبب أحيانًا بعض الاختلالات على اتصال طويل الأمد، فأي قيمة غير صفرية هنا ينبغي
غالبًا أن تكون بمئات أو آلاف لتكون فعالة دون التأثير في الخوادم المعيبة قليلًا. من
الممكن أيضًا قتل الاتصالات فقط عندما يتجاوز استخدام CPU مستوى معينًا، باستخدام
"tune.glitches.kill.cpu-usage". لاحظ أن إغلاقًا رشيقًا يُحاول عند 75% من الحد المكون عبر
الإعلان عن GOAWAY لتدفق مستقبلي. يضمن هذا أن الاتصال المعيب قليلًا سيتوقف عن الاستخدام
بعد بعض الوقت دون المخاطرة بمقاطعة عمليات النقل الجارية.

انظر أيضًا: tune.h2.fe.glitches-threshold, bc_glitches، وtune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

يحدد حجم النافذة الأولي لـ HTTP/2 للاتصالات الصادرة، وهو عدد البايتات التي يستطيع الخادم
الرد بها قبل انتظار إشعار استلام من HAProxy. يؤثر هذا الإعداد في محتوى الحمولة فقط لا
الترويسات. عند عدم التعيين، تنطبق القيمة الافتراضية المشتركة التي يحددها
tune.h2.initial-window-size. قد يكون من المنطقي زيادة هذه القيمة قليلًا للسماح بتنزيلات
أسرع أو لتقليل استخدام CPU على الخوادم، على حساب خلق عدم إنصاف بين العملاء. من الأفضل
استخدام tune.h2.be.rxbuf بدلًا منه، إذ لا يسبب أي عدم إنصاف. وهو لا يؤثر في استخدام
الموارد.

انظر أيضًا: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

يحدد العدد الأقصى لتدفقات HTTP/2 المتزامنة لكل اتصال صادر (أي عدد الطلبات المعلقة على
اتصال واحد بخادم). عند عدم التعيين، ينطبق الافتراضي الذي يحدده
tune.h2.max-concurrent-streams. القيمة الأصغر من الافتراضي 100 قد تحسن استجابة الموقع على
حساب الحفاظ على مزيد من الاتصالات المنشأة مع الخوادم. عندما يكون إعداد "http-reuse"
معينًا إلى "always"، يوصى بتخفيض هذه القيمة حتى لا يختلط عملاء كثر مختلفون على الاتصال
نفسه، لأنه إذا كان عميل أبطأ من الآخرين، فستميل آلية معروفة باسم "head of line blocking"
إلى إحداث أثر متسلسل على سرعة التنزيل لجميع العملاء المتشاركين اتصالًا واحدًا (أبقِ
tune.h2.be.initial-window-size منخفضًا في هذه الحالة). يوصى بشدة بعدم زيادة هذه القيمة؛ قد
يرى البعض أن تشغيلها عند قيم منخفضة (1..5 نموذجيًا) هو الأمثل.

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

يحدد العدد الأقصى لإطارات HTTP/2 الواردة التي ستعالج دفعة واحدة على اتصال واجهة خلفية.
قد يكون من المفيد تعيين هذا إلى قيمة منخفضة (بضع عشرات إلى بضع مئات) عند التعامل مع
مخازن مؤقتة كبيرة جدًا من أجل الحفاظ على زمن استجابة منخفض وإنصاف أفضل بين اتصالات
متعددة. القيمة الافتراضية صفر، ما يعني عدم فرض أي حد.

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

يحدد حجم مخزن الاستقبال لـ HTTP/2 للاتصالات الصادرة، بالبايت. سيقرب هذا الحجم إلى
المضاعف الأعلى التالي لـ tune.bufsize وسيُشارك بين جميع التدفقات التي ترفع بيانات (إطارات
HEADERS وDATA معًا). وفي كل الأحوال، سيُمنح مخزن واحد دائمًا لكل تدفق، وسيُشارك 7/8 من
المخازن غير المستخدمة بين التدفقات المنزِّلة للحمولة، مما يسمح بتحسين أداء الرفع بشكل
ملحوظ وتجنب حجب رأس القائمة (HoL) على اتصالات الواجهة الخلفية المشتركة بين عملاء متعددين
عندما يكون http-reuse معينًا إلى "always". تُعدل النافذة المعلنة لكل تدفق تلقائيًا لتعكس
المساحة المتاحة بحيث لا ينبغي عمليًا الحاجة إلى لمس
tune.h2.be.initial-window-size. إذا عُيِّن أقل من الحجم اللازم للتعامل مع جميع التدفقات،
فسيُستخدم هذا الحد الأدنى. القيمة الافتراضية هي حوالي 1600k (100 تدفق بمخازن 16kB لكل
منها).

انظر أيضًا: tune.h2.be.initial-window-size, tune.h2.fe.rxbuf, http-reuse.

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

يحدد حد عدد الاختلالات على اتصال واجهة أمامية، وعنده يُقتل ذلك الاتصال تلقائيًا. يتيح هذا
قتل الاتصالات سيئة السلوك تلقائيًا دون الحاجة إلى كتابة قواعد صريحة لها. القيمة الافتراضية
صفر، ما يدل على عدم تعيين أي حد بحيث لا يسبب أي حدث إغلاق الاتصال. احترس من أن بعض عملاء
H2 قد يسببون أحيانًا بعض الاختلالات على اتصال طويل الأمد، فأي قيمة غير صفرية هنا ينبغي
غالبًا أن تكون بمئات أو آلاف لتكون فعالة دون التأثير في العملاء المعيبين قليلًا. من
الممكن أيضًا قتل الاتصالات فقط عندما يتجاوز استخدام CPU مستوى معينًا، باستخدام
"tune.glitches.kill.cpu-usage". لاحظ أن إغلاقًا رشيقًا يُحاول عند 75% من الحد المكون عبر
الإعلان عن GOAWAY لتدفق مستقبلي. يضمن هذا أن يحصل العميل غير المتوافق قليلًا على فرصة
إنشاء اتصال جديد ومواصلة العمل دون تأثر دون إطلاق الإغلاق القاسي أبدًا وبالتالي دون
المخاطرة بمقاطعة عمليات النقل الجارية.

انظر أيضًا: tune.h2.be.glitches-threshold, fc_glitches، وtune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

يحدد حجم النافذة الأولي لـ HTTP/2 للاتصالات الواردة، وهو عدد البايتات التي يستطيع العميل
رفعها قبل انتظار إشعار استلام من HAProxy. يؤثر هذا الإعداد في محتوى الحمولة فقط (أي متن
طلبات POST)، لا الترويسات. عند عدم التعيين، تنطبق القيمة الافتراضية المشتركة التي يحددها
tune.h2.initial-window-size. قد يكون من المنطقي زيادة هذه القيمة للسماح بعمليات رفع أسرع.
القيمة الافتراضية تساوي tune.bufsize (16384) وتسمح بعرض نطاق 1.25 ميغابت في الثانية على
الأقل لكل تدفق عبر زمن ping يبلغ 100 ms، و125 ميغابت في الثانية لزمن ping يبلغ 1 ms. وهو
لا يؤثر في استخدام الموارد. استخدام قيم كبيرة جدًا قد يجعل العملاء يعانون نقصًا في
الاستجابة إذا جرى الوصول إلى الصفحات بالتوازي مع عمليات رفع كبيرة. من الأفضل استخدام
tune.h2.fe.rxbuf بدلًا منه، إذ لا يسبب أي عدم إنصاف.

انظر أيضًا: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

يحدد العدد الأقصى لتدفقات HTTP/2 المتزامنة لكل اتصال وارد (أي عدد الطلبات المعلقة على
اتصال واحد من عميل). عند عدم التعيين، ينطبق الافتراضي الذي يحدده
tune.h2.max-concurrent-streams. القيمة الأكبر من الافتراضي 100 قد تحسن أحيانًا قليلًا زمن
تحميل الصفحات للمواقع المعقدة ذات الكائنات الصغيرة الكثيرة على الشبكات عالية زمن
الاستجابة، لكنها قد تؤدي أيضًا إلى استخدام مزيد من الذاكرة بالسماح للعميل بتخصيص مزيد من
الموارد دفعة واحدة. القيمة الافتراضية 100 جيدة عمومًا ويوصى بعدم تغييرها. التزامن الأعلى
له أيضًا أثر في حمل المعالجة وزمن الاستجابة عند التعامل مع أعداد كبيرة من الاتصالات التي
تستخدم هي نفسها تدفقات كثيرة، وقد يخفض الحاجز أمام هجمات حجب الخدمة. يدعم الأمر الوسائط
الاختيارية التالية بعد العدد:

- rq-load { `<number>` \| auto \| ignore }:

```text
الوسيطة الاختيارية "rq-load" تسمح بضبط التزامن المعلن ديناميكيًا بناءً على
حمل قائمة التنفيذ (run-queue) للخيط المنفذ: فما دام حمل الخيط دون العتبة
المشار إليها، سيُعلن عن حد التدفقات المكون. وعندما يتجاوز حمل الخيط الحد
المكون، ينخفض حد التدفقات المعلن تناسبيًا مع مربع نسبة التجاوز. مستويات
الحمل المستهدفة بين 50 و100 توفر عمومًا ضبطًا جيدًا جدًا تحت الأحمال
الثقيلة. وبدلًا من تحديد رقم صريح، تقبل الكلمة المفتاحية "ignore"، وهي
القيمة الافتراضية، ما يعني أن حمل قائمة تنفيذ الخيط لن يؤخذ في الحسبان
لتلطيف حد التدفقات المعلن، و"auto" التي تضبط الحد على قيمة
"tune.runqueue-depth"، وتعطي عمومًا نتائج جيدة دون الحاجة إلى مزيد من
تغيير الإعداد.
```

- min `<number>`:

```text
يحدد هذا الحد الأدنى لمستوى التزامن المعلن عند استخدام rq-load، حتى لو
أدى ذلك إلى حمل أعلى من الهدف المكون. يتيح هذا الحفاظ على مستوى جيد من
التفاعلية على موقع تحت حمل ثقيل جدًا. القيمة الدنيا والافتراضية هي 1، لكن
القيم بين 5 و15 يمكن أن تحسن تجربة المستخدم.
```

مثال:

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

يحدد العدد الأقصى لإطارات HTTP/2 الواردة التي ستعالج دفعة واحدة على اتصال واجهة أمامية.
قد يكون من المفيد تعيين هذا إلى قيمة منخفضة (بضع عشرات إلى بضع مئات) عند التعامل مع
مخازن مؤقتة كبيرة جدًا من أجل الحفاظ على زمن استجابة منخفض وإنصاف أفضل بين اتصالات
متعددة. القيمة الافتراضية صفر، ما يعني عدم فرض أي حد.

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

يحدد العدد الأقصى لإطارات RST_STREAM الواردة لـ HTTP/2 التي ستعالج دفعة واحدة على اتصال
واجهة أمامية. بعد استقبال العدد المحدد من إطارات RST_STREAM، سيوضع معالج الاتصال في قائمة
أولوية منخفضة ويعالج بعد جميع المهام الأخرى. قد يكون من المفيد تعيين هذا إلى قيمة منخفضة
جدا (1 أو بضع وحدات) للحد بشكل ملحوظ من آثار فيضانات RST_STREAM. تحدث RST_STREAM عندما
ينقر المستخدم على زر التوقف في متصفحه، لكن المللي ثواني الإضافية القليلة التي تسببها
إعادة الإدراج هذه في الطابور غير ملحوظة عمومًا، لكنها فعالة عمومًا في خفض الحمل الناتج عن مثل
هذه الفيضانات بشكل ملحوظ. القيمة الافتراضية صفر، ما يعني عدم فرض أي حد.

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

يحدد العدد الأقصى لإجمالي التدفقات المعالجة لكل اتصال وارد لـ HTTP/2. عند بلوغ هذا الحد،
سيرسل HAProxy إطار GOAWAY رشيقًا يعلم العميل بأنه سيغلق الاتصال بعد إغلاق جميع التدفقات
المعلقة. عمليًا، يميل العملاء إلى الإغلاق بأسرع ما يمكن عند استقبال هذا، وإنشاء اتصال
جديد للطلبات التالية. قد يكون فعل هذا مفيدًا ومرغوبًا أحيانًا في مواقف يبقى فيها العملاء
متصلين لفترة طويلة جدًا ويسببون بعض عدم التوازن داخل المجموعة. فمثلًا، في بعض البيئات
شديدة الديناميكية، من الممكن إنشاء موازنات حمل جديدة أثناء التشغيل للتكيف مع زيادة الحمل،
وأنه عند انخفاض الحمل ينبغي إيقافها دون قطع الاتصالات المنشأة. بتعيين حد هنا، ستكون
للاتصالات مدة حياة محدودة وستتجدد بشكل متكرر، وقد تُنشأ بعض هذه الاتصالات مع عقد أخرى، بحيث تُحرر
الموارد الموجودة بسرعة.

من المهم فهم أن هناك علاقة ضمنية بين هذا الحد و"tune.h2.fe.max-concurrent-streams"
أعلاه. ففي الواقع، سيوافق HAProxy دائمًا على معالجة أي تدفقات معلقة يحتمل أن تكون في
الطريق بين العميل والواجهة الأمامية، لذا سيرفع الحد المعلن دائمًا تلقائيًا بمقدار القيمة
المكونة في max-concurrent-streams، وستُستخدم هذه القيمة حدًا صارمًا تؤدي مخالفته من عميل غير
متوافق إلى إغلاق الاتصال. وهكذا عند عد الطلبات لكل اتصال من السجلات، قد يُلاحظ أي عدد بين
max-total-streams و(max-total-streams + max-concurrent-streams) بحسب سرعة إنشاء العميل
للتدفقات.

القيمة الافتراضية صفر، وهي لا تفرض أي حد يتجاوز ما يفرضه البروتوكول (2^30 ~= 1.07
مليار). القيم حول 1000 قد تسبب بالفعل تجديدًا متكررًا للاتصالات دون إحداث أي زمن استجابة
محسوس لأغلب العملاء. تعيينه منخفضًا جدًا قد يؤدي إلى زيادة استخدام CPU بسبب إعادة اتصالات
TLS المتكررة، إضافة إلى زيادة زمن تحميل الصفحات. يرجى ملاحظة أن بعض أدوات اختبار الحمل لا
تدعم إعادة الاتصال وقد تبلغ عن أخطاء مع هذا الإعداد؛ لذا قد يلزم تعطيله عند إجراء قياسات
الأداء. انظر أيضًا "tune.h2.fe.max-concurrent-streams".

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

يحدد حجم مخزن الاستقبال لـ HTTP/2 للاتصالات الواردة، بالبايت. سيقرب هذا الحجم إلى المضاعف
الأعلى التالي لـ tune.bufsize وسيُشارك بين جميع التدفقات التي ترفع بيانات (إطارات HEADERS
وDATA معًا). وفي كل الأحوال، سيُمنح مخزن واحد دائمًا لكل تدفق، وسيُشارك 7/8 من المخازن غير
المستخدمة بين التدفقات التي ترفع الحمولة، مما يسمح بتحسين أداء الرفع بشكل ملحوظ. تُعدل
النافذة المعلنة لكل تدفق تلقائيًا لتعكس المساحة المتاحة بحيث لا ينبغي عمليًا الحاجة إلى
لمس tune.h2.fe.initial-window-size. إذا عُيِّن أقل من الحجم اللازم للتعامل مع جميع
التدفقات، فسيُستخدم هذا الحد الأدنى. القيمة الافتراضية 1600k (100 تدفق بمخازن 16kB لكل
منها) تسمح تقريبًا بسرعة رفع تبلغ 130 ميغابت في الثانية لعميل بزمن RTT يبلغ 100ms.

انظر أيضًا: tune.h2.fe.initial-window-size وtune.h2.be.rxbuf.

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

يحدد حجم جدول ترويسات HTTP/2 الديناميكي. الافتراضي 4096 بايت ولا يمكن أن يتجاوز 65536
بايت. القيمة الأكبر قد تساعد عملاء معينين على إرسال طلبات أكثر إحكامًا، بحسب قدراتهم.
تُستهلك هذه الكمية من الذاكرة لكل اتصال HTTP/2. يوصى بعدم تغييرها.

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

يحدد القيمة الافتراضية لحجم النافذة الأولي لـ HTTP/2، على الاتصالات الواردة والصادرة
معًا. تُستخدم هذه القيمة للاتصالات الواردة عندما لا يكون tune.h2.fe.initial-window-size
معينًا، وللاتصالات الصادرة عندما لا يكون tune.h2.be.initial-window-size معينًا. يستخدم
هذا الإعداد قيمةً أولية وحدًا أدنى لكل تدفق في آن واحد. القيمة الافتراضية تساوي 16384
(tune.bufsize)، التي تسمح للرفع تقريبًا بعرض نطاق 1.25 ميغابت في الثانية على الأقل لكل
تدفق عبر شبكة يبلغ زمن ping فيها 100 ms، أو 125 ميغابت في الثانية عبر شبكة محلية زمن
ping فيها 1-ms. عندما تكون مخازن الاستقبال المستخدمة أقل من الحد الأقصى، ضمن الحدود التي
يحددها tune.h2.be.rxbuf وtune.h2.fe.rxbuf، ستُشارك المخازن غير المستخدمة بين التدفقات
المستقبلة. وعليه فلا فائدة عادة من تغيير هذا الإعداد الافتراضي. وبما أن تغيير هذه القيمة
الافتراضية سيزيد سرعات الرفع ويسبب مزيدًا من عدم الإنصاف بين العملاء في التنزيل، يوصى
باستخدام الإعدادين المخصصين للجانب tune.h2.fe.initial-window-size
وtune.h2.be.initial-window-size بدلًا من ذلك.

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

يحدد مستوى الأخطاء في فاك التركيب (demultiplexer) لـ H2 الذي سيولد سجلًا. الافتراضي هو
"stream"، ما يعني أن أي خطأ فك ترميز يقع في فاك التركيب سيؤدي إلى إصدار سجل. القيمة
"connection" تشير إلى أن السجلات التي تؤدي إلى إبطال الاتصال فقط ستنتج سجلًا. وأخيرًا،
تشير "none" إلى أن أي خطأ فك ترميز لن ينتج أي سجل. يوصى بتعيين "connection" على الأقل من
أجل اكتشاف شذوذ البروتوكول، حتى لو كان هذا يعني التحويل المؤقت إلى "none" خلال الفترات
الصعبة.

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

يحدد العدد الافتراضي الأقصى لتدفقات HTTP/2 المتزامنة لكل اتصال (أي عدد الطلبات المعلقة
على اتصال واحد). تُستخدم هذه القيمة للاتصالات الواردة عندما لا يكون
tune.h2.fe.max-concurrent-streams معينًا، وللاتصالات الصادرة عندما لا يكون
tune.h2.be.max-concurrent-streams معينًا. القيمة الافتراضية 100. يختلف الأثر بحسب الجانب
فيرجى الاطلاع على الإعدادين أعلاه لمزيد من التفاصيل. يوصى بعدم استخدام هذا الإعداد
والانتقال إلى الإعدادين المخصصين لكل جانب بدلًا منه. القيمة صفر تعطل الحد فيستطيع عميل
واحد إنشاء تدفقات بقدر ما يستطيع HAProxy تخصيصه. يوصى بشدة بعدم تغيير هذه القيمة.

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

يحدد الحجم الأقصى لإطار HTTP/2 الذي يعلن HAProxy استعداده لاستقباله من نظرائه. القيمة
الافتراضية هي الأكبر بين 16384 وحجم المخزن المؤقت (tune.bufsize). وفي كل الأحوال، لن يعلن
HAProxy دعم أحجام إطارات أكبر من المخازن المؤقتة. الغرض الرئيسي من هذا الإعداد هو السماح
بتحديد إعداد الحجم الأقصى للإطار عند استخدام مخازن مؤقتة كبيرة. أحجام الإطارات الكبيرة
جدًا قد تؤثر في الأداء أو تجعل بعض الأقران يتصرفون بشكل غير سليم. يوصى بشدة بعدم تغيير هذه القيمة.

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

يفعل ('on') أو يعطل ('off') الإرسال دون نسخ للبيانات من أجل مُضاعِف H2. وهو مفعل
افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

يحدد الطول الأقصى للكوكيز الملتقطة. هذه هي القيمة القصوى التي يسمح لـ "capture cookie
xxx len yyy" بأخذها، وأي قيمة أعلى ستُقلم تلقائيًا إلى هذه. من المهم عدم تعيين قيمة عالية
جدًا لأن جميع التقاطات الكوكيز تخصص هذا الحجم مهما كانت قيمتها المكونة (إنها تتشارك
المجموعة نفسها). هذه القيمة لكل طلب ولكل استجابة، فالذاكرة المخصصة هي ضعف هذه القيمة لكل
اتصال. عند عدم التحديد، يُضبط الحد على 63 حرفًا. يوصى بعدم تغيير هذه القيمة.

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

يحدد الطول الأقصى لـ URI الطلب في السجلات. يمنع هذا قلم URIs الطلبات الطويلة ذات سلاسل
الاستعلام القيمة في أسطر السجل. لا علاقة لهذا بحدود syslog. إذا زدت هذا الحد، فقد ترغب
أيضًا في زيادة المعامل 'log ... len yyy'. قد يحتاج عامل syslog لديك أيضًا إلى توجيهات
إعداد محددة. القيمة الافتراضية هي 1024.

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

يحدد العدد الأقصى للترويسات المسموح بها في رسائل HTTP المستقبلة. عندما تأتي رسالة بعدد
ترويسات أكبر من هذه القيمة (بما في ذلك السطر الأول)، تُرفض برمز حالة "400 Bad Request"
للطلب، أو "502 Bad Gateway" للاستجابة. القيمة الافتراضية هي 101، وهي كافية لجميع
الاستخدامات، نظرًا إلى أن خادم Apache المنتشر على نطاق واسع يستخدم الحد نفسه. قد يكون
من المفيد رفع هذا الحد مؤقتًا للسماح لتطبيق معيب بالعمل إلى أن يُصلح. النطاق المقبول هو
1..32767. ضع في ذهنك أن كل ترويسة جديدة تستهلك 32bits من الذاكرة لكل تدفق، فلا ترفع هذا
الحد كثيرًا.

لاحظ أن HTTP/1.1 بروتوكول نصي، فلا حد خاص عند إرسال الرسالة. الحد أثناء تحليل الرسالة
كافٍ. أما HTTP/2 وHTTP/3 فبروتوكولان ثنائيان ويتطلبان خطوة ترميز. يُضبط حد أيضًا عند ترميز
الترويسات للامتثال للقيود التي يفرضها البروتوكولان. هذا الحد كبير بما يكفي لكنه غير موثق
عن قصد. يطبق الحد نفسه على الخطوات الأولى لفك الترميز للسبب نفسه.

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

يتحكم في مشاركة مجموعات الاتصالات الخاملة بين الخيوط للخادم نفسه. يمكن تفعيلها لجميع
الخيوط في مجموعة الخيوط نفسها ('on')، أو تفعيلها لجميع الخيوط ('full')، أو تعطيلها
('off'). الافتراضي هو مشاركتها بين الخيوط في مجموعة الخيوط نفسها ('on')، من أجل تقليل
عدد الاتصالات الدائمة بخادم، وتحسين معدل إعادة استخدام الاتصالات. المشاركة مع خيوط من
مجموعات خيوط أخرى قد تؤثر في الأداء، وهي غير مفعلة افتراضيًا، لكنها قد تكون مفيدة إذا
كان تعظيم إعادة استخدام الاتصالات أولوية. للمساعدة في التصحيح أو عند الاشتباه بعطل في
HAProxy حول إعادة استخدام الاتصالات، قد يكون من الملائم تعطيل مشاركة مجموعة الخمول هذه
بين خيوط متعددة قسرًا، وفرض هذا الخيار إلى "off". يوصى بشدة بعدم تعطيل هذا الخيار دون
تعيين قيمة متحفظة على "pool-low-conn" لجميع الخوادم التي تعتمد على إعادة استخدام
الاتصالات لتحقيق مستوى أداء عالٍ، وإلا فقد تُغلق الاتصالات كثيرًا جدًا مع ازدياد عدد
الخيوط.

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

يحدد المدة التي بعدها سيعتبر HAProxy أن مخزنًا مؤقتًا فارغًا مرتبط على الأرجح بتدفق خامل.
يُستخدم هذا لضبط أحجام بعض الحزم على النحو الأمثل أثناء تمرير البيانات الكبيرة والصغيرة
بالتناوب. قرار استخدام splice() أو إرسال مخازن مؤقتة كبيرة في SSL يتأثر بهذا المعامل.
القيمة بالمللي ثانية بين 0 و65535. القيمة صفر تعني أن HAProxy لن يحاول اكتشاف التدفقات
الخاملة. الافتراضي 1000، الذي يبدو صحيح الكشف عن وقفات المستخدم النهائي (مثلًا قراءة
صفحة قبل النقر). لا ينبغي أن يكون هناك سبب لتغيير هذه القيمة. يرجى فحص tune.ssl.maxrecord
أدناه.

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

عاديًا، تنشئ جميع أسطر "bind" شظية (shard) واحدة، أي مقبسًا واحدًا تستمع إليه جميع خيوط
العملية. مع خيوط كثيرة، هذا غير فعال جدًا، وقد يسبب حتى عبئًا إضافيًا كبيرًا في النواة لتحديث
حالة الاستطلاع أو حتى توزيع الأحداث على الخيوط المختلفة. تدعم أنظمة التشغيل الحديثة
موازنة الاتصالات الواردة، وهي آلية تقوم على السماح بربط مقابس متعددة بالعنوان والمنفذ
نفسهما، وتوزيع جميع الاتصالات الواردة بالتساوي على هذه المقابس بحيث لا يرى كل خيط سوى
الاتصالات المنتظرة في المقبس المرتبط به. هذا يقلل بشكل كبير الحمل في جانب النواة ويزيد
الأداء في مسار الاتصالات الواردة. يفعل هذا عادة في HAProxy باستخدام إعداد "shards" على
أسطر "bind"، وقيمته الافتراضية 1، ما يعني أن كل مستمع سيكون فريدًا في العملية. على الأنظمة
كثيرة المعالجات، قد يكون أنسب تغيير الإعداد الافتراضي إلى "by-thread" من أجل إنشاء مقبس
استماع واحد لكل خيط دائمًا، أو "by-group" من أجل إنشاء مقبس استماع واحد لكل مجموعة خيوط
دائمًا. احترس من استخدام الواصفات مع "by-thread" لأن كل مستمع سيحتاج مقابس بعدد الخيوط.
كما أن بعض أنظمة التشغيل (مثل FreeBSD) تتقيد بما لا يزيد عن 256 مقبسًا على العنوان نفسه.
لاحظ أن "by-group" سيبقى مكافئًا لـ "by-process" في الإعدادات الافتراضية التي تنطوي على
مجموعة خيوط واحدة، وسيرجع إلى مشاركة المقبس نفسه على الأنظمة التي لا تدعم هذه الآلية.
الافتراضي هو "by-group" مع رجوع إلى "by-process" للأنظمة أو عائلات المقابس التي لا تدعم
الارتباطات المتعددة.

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

يفعل ('on' / 'fair') أو يعطل ('off') القبول متعدد الطوابير للمستمع الذي يوزع حركة البيانات
الواردة على جميع الخيوط التي يسمح لسطر "bind" بالعمل عليها بدل أخذها لنفسه. يوفر هذا
توزيعًا أكثر سلاسة لحركة البيانات ويتوسع أفضل بكثير، خاصة في البيئات التي قد تكون فيها
الخيوط محملة بشكل غير متساوٍ بسبب نشاط خارجي (تقاطع مقاطعات الشبكة مع خيط واحد مثلًا).
الوضع الافتراضي، "on"، يحسن اختيار الخيط بأخذ عينة واختيار الأقل اتصالات فيها. وهو غالبًا
الخيار الأفضل عندما تكون الاتصالات طويلة العمر لأنه ينجح في إبقاء جميع الخيوط مشغولة.
وضع ثانٍ، "fair"، يدور بدلًا من ذلك عبر جميع الخيوط بغض النظر عن مستوى حملها اللحظي. قد
يكون أنسب للاتصالات قصيرة العمر، أو على الأجهزة ذات الأعداد الكبيرة جدًا من الخيوط حيث
احتمال إيجاد الخيط الأقل حملًا بالوضع الأول منخفض. وأخيرًا يمكن تعطيل آلية إعادة التوزيع
قسرًا باستخدام "off" لاستكشاف الأعطال، أو للمواقف التي تكون فيها الاتصالات قصيرة العمر
ويُقدَّر أن نظام التشغيل يوفر بالفعل توزيعًا جيدًا كفاية. الافتراضي هو "on".

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

يخبر haproxy صراحة كيف ينبغي التعامل مع كائنات عينات haproxy عند دفعها إلى Lua. ففي
الواقع، عند الاستفادة من المحولات الأصلية أو عمليات جلب العينات أو المتغيرات من نص Lua
البرمجي (على سبيل المثال لا الحصر)، يحول haproxy النوع الداخلي smp إلى نوع Lua مكافئ.
وبسبب التنفيذ التاريخي، هناك غموض حول التعامل مع القيم المنطقية: عند إجراء تحويل Lua
-\> haproxy smp، تُحفظ القيم المنطقية بشكل صحيح، لكن عند إجراء تحويل haproxy smp -\> Lua،
حُولت القيم المنطقية إلى أعداد صحيحة بالخطأ. هذا يعني أن عملية جلب عينة أو محولًا يعيد
قيمة منطقية سيعيد العدد الصحيح 0 أو 1 عند الاستفادة منه من Lua. وللأسف، في Lua، القيم
المنطقية والأعداد الصحيحة غير قابلة للتبديل. وهكذا، لتجنب الغموض، يجب تعيين
"tune.lua.bool-sample-conversion" صراحة إلى إما "normal" (ما يعني ترك السلوك التاريخي
لأجل اتساق أفضل) أو "pre-3.1-bug" (فرض السلوك التاريخي لمنع منطق النصوص الموجودة من
التصرف السيئ). إذا لم يعين الخيار صراحة وحُمل نص Lua من الإعداد، فسيصدر haproxy تحذيرًا،
وسيعود الخيار ضمنيًا إلى "pre-3.1-bug" لمطابقة السلوك التاريخي. يوصى بتعيين هذا الخيار
إلى "normal" بعد التأكد من أن نصوص Lua المستخدمة تتعامل بشكل صحيح مع عينات haproxy
المنطقية كقيم منطقية.

يجب تعيين هذا الإعداد قبل أي توجيه "lua-load" أو "lua-load-per-thread" ليؤخذ في الحسبان،
وإلا فهو متجاهَل.

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

تنطبق مهلة التنفيذ "burst" على أي معالج Lua. إذا أخفق المعالج في الانتهاء أو التخلي عن
التنفيذ (yield) قبل بلوغ المهلة، فسيُجهض لمنع تنازع الخيوط، ولمنع توقف خدمة حركة البيانات
لفترة طويلة جدًا، ونهائيًا لمنع انهيار العملية بسبب انطلاق المراقب (watchdog). بخلاف
مهل lua الأخرى التراكمية مع التخلي عن التنفيذ، ستضمن burst-timeout أن الوقت المقضي في
نافذة تنفيذ lua واحدة لا يتجاوز المهلة المكونة.

التخلي عن التنفيذ (yield) هنا يعني أن تنفيذ lua يُقاطع فعليًا إما عبر استدعاء صريح لدالة
تخلي مثل core.(m)sleep() أو core.yield()، أو إثر تخلي قسري تلقائي (انظر
tune.lua.forced-yield)، وأنه سيستأنف لاحقًا عندما توضع المهمة ذات الصلة لإعادة الجدولة.
ليست جميع معالجات lua قادرة على التخلي: علينا التمييز بين المعالجات القادرة على التخلي
وغير القادرة عليه.

بالنسبة للمعالجات القادرة على التخلي (المهام، الإجراءات..)، بلوغ المهلة يعني أن
"tune.lua.forced-yield" قد يكون مرتفعًا جدًا للنظام، وتخفيضه قد يحسن الوضع، لكن قد يكون
من الجيد أيضًا فحص ما إذا كانت إضافة عمليات تخلٍّ يدوية عند بعض النقاط الرئيسية داخل دالة lua
تساعد أم لا. قد يشير هذا أيضًا إلى أن المعالج يقضي وقتًا طويلاً في دالة مكتبة lua محددة
لا يمكن مقاطعتها.

بالنسبة للمعالجات غير القادرة على التخلي (محولات lua، عمليات جلب العينات)، قد يشير هذا
ببساطة إلى أن المعالج يقوم بحسابات كثيرة جدًا، ما قد ينجم عن تصميم غير مناسب بما أن هذه
المعالجات، التي كثيرًا ما تسد تدفق تنفيذ الطلب، يُتوقع أن تنتهي سريعًا للسماح بمرور
معالجة الطلب. نهج حل شائع هنا هو محاولة تحسين دالة lua للسرعة بشكل أفضل لأن خفض
"tune.lua.forced-yield" لن يساعد.

لا تحتسب هذه المهلة سوى زمن تشغيل lua الصرف. إذا نفذت lua أمر core.sleep، فلا يؤخذ وقت
النوم في الحسبان. المهلة الافتراضية هي 1000ms.

ملاحظة: إذا بُدئت دورة جامع المهملات (GC) لـ lua من المعالج (إما بطلب صريح أو تلقائيًا
بواسطة lua بعد بعض الوقت)، فسيؤخذ زمن دورة GC في الحسبان أيضًا.

في الواقع، لا سبيل لاستنتاج زمن دورة GC، لذا قد يؤدي هذا إلى بعض الإيجابيات الزائفة على
الأنظمة المشبعة (حيث يصعب على GC مواكبة الوضع ويستهلك معظم زمن التنفيذ المتاح). إذا كان
هذا هو الحال، فإليك بعض مسارات الحل:

    - فحص ما إذا كان يمكن تحسين النص البرمجي لتقليل أثر ذاكرة lua
    - ضبط دقيق لمعاملات GC لـ lua و/أو طلب دورات GC يدوية
      (انظر: https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage)
    - زيادة tune.lua.burst-timeout

تعيين القيمة إلى 0 يعطل هذه الحماية تمامًا.

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

يجبر هذا التوجيه محرك Lua على تنفيذ تخلي عن التنفيذ (yield) كل `<number>` تعليمة
منفذة. يتيح هذا مقاطعة نص برمجي طويل ويسمح لمجدول HAProxy بمعالجة مهام أخرى مثل قبول
الاتصالات أو تمرير حركة البيانات. القيمة الافتراضية هي 10000 تعليمة للنصوص المحملة
باستخدام "lua-load-per-thread" وMAX(500, 10000 / nbthread) تعليمة للنصوص المحملة
باستخدام "lua-load" (وجد أنها القيمة المثلى للأداء مع الحرص على عدم خلق تنازع خيوط مع
خيوط متعددة تتنافس على قفل lua العام).

إذا كان HAProxy ينفذ كود Lua كثيرًا لكن مطلوب مزيد من الاستجابة، يمكن خفض هذه القيمة.
وإذا كان كود Lua طويلًا نوعًا ما ونتيجته مطلوبة تمامًا لمعالجة البيانات، يمكن زيادة
`<number>`، لكن ينبغي ضبط القيمة بحكمة لأنه في سياق تعدد الخيوط قد يزيد التنازع.

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

يفعل ('on') أو يعطل ('off') تسجيل مخرجات نصوص LUA عبر المسجلات المنطبقة على البروكسي
الحالي، إن وجدت.

الافتراضي 'on'.

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

يفعل ('on') أو يعطل ('off') تسجيل مخرجات نصوص LUA عبر stderr. عند التعيين إلى 'auto'،
يكون التسجيل عبر stderr مفعلًا شرطيًا 'on' عند أي من:

    - tune.lua.log.loggers معين إلى 'off'
    - ينفذ النص البرمجي في سياق غير بروكسي بلا مسجل عام
    - ينفذ النص البرمجي في سياق بروكسي بلا مسجل مرفق

يرجى الملاحظة أنه عند التفعيل، هذا التسجيل إضافة إلى التسجيل المكون عبر
tune.lua.log.loggers.

الافتراضي 'auto'.

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

يحدد أقصى كمية من ذاكرة RAM بالميغابايت لكل عملية يمكن أن تستخدمها Lua. افتراضيًا هي
صفر ما يعني عدم وجود حد. من المهم تعيين حد لضمان أن عطلًا في نص برمجي لن يؤدي إلى نفاد
ذاكرة النظام.

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

يحدد مكتبات Lua القياسية التي تُحمَّل عند تهيئة حالة Lua. الوسيطة قائمة أسماء مكتبات
مفصولة بفواصل مأخوذة من المجموعة التالية: table, io, os, string, math, utf8, package,
debug. يمكن استخدام القيمتين الخاصتين "all" و"none" بدلًا من قائمة. لا يمكن جمع "none"
مع أسماء مكتبات. القيمة الافتراضية هي "all".

تُحمَّل مكتبتا base وcoroutine دائمًا بغض النظر عن هذا الإعداد: فـ base توفر دوال Lua
الأساسية التي يعتمد عليها HAProxy، وcoroutine مطلوبة لأن HAProxy يستبدل
coroutine.create() بتنفيذ آمن خاص به.

لاحظ أن fork() وإنشاء خيط جديد محجوبان افتراضيًا في HAProxy بغض النظر عن هذا الإعداد،
ولا يمكن إعادة تفعيلهما إلا عبر التوجيه العام "insecure-fork-wanted". حصر مجموعة
المكتبات المحملة يقلل كذلك مساحة الهجوم المكشوفة أمام نصوص Lua. على وجه الخصوص: - استبعاد
"os" يمنع os.execute() وos.exit() - استبعاد "io" يمنع io.open() وio.popen() - استبعاد "package"
يمنع تحميل وحدات C الأصلية عبر require() - استبعاد "debug" يمنع تفحص داخل HAProxy عبر
debug.getupvalue() أو debug.getmetatable() أو debug.sethook()

أمثلة:

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

يجب تعيين هذا الإعداد قبل أي توجيه "lua-load" أو "lua-load-per-thread" أو
"lua-prepend-path"، وإلا يُرجع خطأ تحليل.

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

هذه مهلة التنفيذ لخدمات Lua. وهي مفيدة لمنع الحلقات اللانهائية أو قضاء وقت طويل جدًا في
Lua. لا تحتسب هذه المهلة سوى زمن تشغيل lua الصرف. إذا نفذت lua أمر نوم، فلا يؤخذ النوم في
الحسبان. المهلة الافتراضية هي 4s.

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

هذه مهلة التنفيذ لجلسات Lua. وهي مفيدة لمنع الحلقات اللانهائية أو قضاء وقت طويل جدًا في
Lua. لا تحتسب هذه المهلة سوى زمن تشغيل lua الصرف. إذا نفذت lua أمر نوم، فلا يؤخذ النوم في
الحسبان. المهلة الافتراضية هي 4s.

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

الغرض هو نفسه "tune.lua.session-timeout"، لكن هذه المهلة مخصصة للمهام. افتراضيًا، لا
تكون هذه المهلة معينة لأنه قد تظل مهمة حية طوال مدة حياة HAProxy. فمثلًا، مهمة تستخدم
لفحص الخوادم.

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

يحدد عدد الفحوصات النشطة لكل خيط والذي بعده سيحاول الخيط فعليًا البحث عن خيط أقل تحميلًا
لتشغيل فحص الصحة، أو وضعه في قائمة الانتظار حتى يتناقص عدد الفحوصات النشطة العاملة عليه.
القيمة الافتراضية صفر، ما يعني عدم تعيين مثل هذا الحد. قد يكون مطلوبًا في بيئات معينة
تشغّل عددًا كبيرًا للغاية من الفحوصات المكلفة مع خيوط كثيرة عندما يبدو الحمل غير متساو
وقد يؤدي إلى انتهاء مهلة فحوصات الصحة عشوائيًا عند الإقلاع، خصوصًا عند استخدام OpenSSL 3.0
الذي يستهلك على فحوصات الصحة ما يقارب 20 مرة من CPU أكثر من الإصدارات الأقدم. ستكون
النتيجة محاولة تسوية عمل فحوصات الصحة عبر جميع الخيوط. الغالبية العظمى من الإعدادات لا
تحتاج إلى لمس هذا المعامل. يرجى الملاحظة أن القيم المنخفضة جدًا قد تبطئ فحوصات الصحة
بشكل ملحوظ إذا كانت الفحوصات بطيئة التنفيذ.

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

يحدد العدد الأقصى للاتصالات المتتالية التي قد تقبلها عملية على التوالي قبل الانتقال إلى
عمل آخر. في وضع العملية الواحدة، كانت الأرقام الأعلى تعطي أداءً أفضل عند معدلات اتصال
عالية، لكن هذا لم يعد الحالة مع الطوابير المتعددة (multi-queue). تنطبق هذه القيمة على كل
مستمع على حدة، بحيث يؤخذ عدد العمليات التي يرتبط بها المستمع في الحسبان. القيمة الافتراضية
لهذه القيمة 4 التي أظهرت أفضل النتائج. إذا وُرثت قيمة أعلى بشكل ملحوظ من إعداد قديم، فقد
يستحق الأمر إزالتها لأنها سترفع الأداء وتخفض زمن الاستجابة معًا. في وضع العمليات
المتعددة، تُقسم على ضعف عدد العمليات التي يرتبط بها المستمع. تعيين هذه القيمة إلى -1 يعطل
التقييد تمامًا. لا ينبغي عادة الحاجة إلى تعديل هذه القيمة.

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

يحدد الكمية القصوى للأحداث التي يمكن معالجتها دفعة واحدة في استدعاء واحد لنظام
الاستطلاع. القيمة الافتراضية متكيفة مع نظام التشغيل. لوحظ أن خفضها إلى ما دون 200 يميل
إلى خفض زمن الاستجابة قليلًا على حساب عرض نطاق الشبكة، وأن رفعها فوق 200 يميل إلى مقايضة
زمن الاستجابة بعرض نطاق زاد قليلًا. يجب أن تكون القيمة المكونة أقل من أو تساوي 1000000.

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

يضبط مساحة المخزن المؤقت المحجوزة إلى هذا الحجم بالبايت. تُستخدم المساحة المحجوزة لإعادة
كتابة الترويسات أو إلحاقها. لن تملأ القراءات الأولى على المقابس أكثر من bufsize-maxrewrite
أبدًا. تاريخيًا كانت قيمتها الافتراضية نصف bufsize، رغم أن ذلك لا معنى كبير له إذ نادرًا
ما توجد أعداد كبيرة من الترويسات المطلوب إضافتها. تعيينها مرتفعة جدًا يمنع معالجة الطلبات
أو الاستجابات الكبيرة. وتعيينها منخفضة جدًا يمنع إضافة ترويسات جديدة إلى طلبات كبيرة فعلًا
أو إلى طلبات POST. من الحكمة عمومًا تعيينها إلى حوالي 1024. يعاد ضبطها تلقائيًا إلى نصف
bufsize إذا كانت أكبر من ذلك. يعني هذا أنك لا تقلق بشأنها عند تغيير bufsize.

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

يحدد العدد الأقصى للقواعد التي يمكن تقييمها دفعة واحدة في دوال تقييم مجموعات القواعد،
بشرط أن تدعم التخلي عن التنفيذ (yielding). ففي الواقع، ليس من النادر رؤية إعدادات تحوي
عددًا كبيرًا من قواعد "tcp-request content" أو "http-request" مثلًا. عدد كبير من القواعد
مقترنًا بإجراءات متطلبة للCPU (مثلًا: إجراءات تعمل على المحتوى) قد يخلق تنازع خيوط لأن
جميع قواعد مجموعة قواعد معينة تُقيم تحت حلقة الاستطلاع نفسها إذا لم تُقاطع عملية التقييم.
يضمن هذا الخيار ألا يُنفذ أكثر من عدد `<number>` من القواعد تحت حلقة الاستطلاع نفسها
لمجموعات القواعد الموجهة للمحتوى (تلك التي تدعم التخلي بالفعل بسبب فحص المحتوى). ما يفعله
هو إجبار دالة التقييم على التخلي، بحيث تعود في حلقة الاستطلاع التالية لمواصلة التقييم.

مجموعات القواعد المتأثرة هي:

- "tcp-request content"
- "tcp-response content"
- "http-request"
- "http-response"

القيمة الافتراضية هي 50.

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

يحدد كمية الذاكرة لكل خيط التي ستبقى ساخنة في الذاكرة المؤقتة المحلية ولن يمكن للخيوط
الأخرى استردادها أبدًا. الوصول إلى هذه الذاكرة سريع جدًا (بلا أقفال)، ووجود ما يكفي منها
أمر حاسم للحفاظ على مستوى أداء جيد تحت تنازع خيوط أقصى. تُعبر القيمة بالبايت، والقيمة
الافتراضية تكون مهيأة وقت البناء عبر CONFIG_HAP_POOL_CACHE_SIZE التي تبلغ افتراضيًا
524288 (512 kB). القيمة الأكبر قد ترفع الأداء في بعض سيناريوهات الاستخدام، خاصة عندما
تظهر ملامح الأداء أن تخصيص الذاكرة مضغوط كثيرًا. تظهر التجربة أن قيمة جيدة تقع بين مرة
إلى مرتين حجم الذاكرة المؤقتة L2 لكل نواة CPU. القيم الكبيرة جدًا سيكون لها أثر سلبي على
الأداء بجعل استخدام ذاكرات L3 المؤقتة في وحدات CPU غير فعال، وستستهلك كميات أكبر من
الذاكرة. يوصى بعدم تغيير هذه القيمة، أو بالمضي في زيادات صغيرة. ومن أجل تعطيل ذاكرات
CPU المؤقتة لكل خيط تمامًا، يمكن أن تنفع قيمة صغيرة جدًا، لكن من الأفضل استخدام
"-dMno-cache" على سطر الأوامر.

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

يعدل التخزين المؤقت للنواة لكل مقبس بحيث يبلغ أن جانب الإرسال في المقبس ممتلئ بمجرد أن
تساوي كمية البيانات المخزنة هذه القيمة زائد حجم النافذة المقيس. والمبدأ هو ترك الحد الأدنى
الصارم اللازم من البايتات في مخازن المقابس، زائد هامش صغير يقابل ما كان سيُرسل بحلول وقت
محاولة haproxy الإرسال مجددًا. تعيين هذا إلى قيمة منخفضة (حوالي tune.bufsize نموذجيًا)
يسمح بتقليل استهلاك الذاكرة في مخازن النظام بشكل ملحوظ، وتقليل زمن الاستجابة على مستوى
التطبيق الناجم عن تفريغ البيانات المخزنة. يمثل هذا عمومًا إعدادًا أكثر فاعلية ودقة من
tune.sndbuf.client وtune.sndbuf.client على الأنظمة التي تدعمه. ينطبق هذا لكل اتصال (اتصال
من عميل أو اتصال بخادم بحسب الإعداد) ولا تستخدمه إلا اتصالات TCP. الافتراضي صفر، ما يعني
عدم وجود حد. هذا متاح على Linux فقط.

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

يحدد حجم ذاكرة البحث عن الأنماط المؤقتة إلى `<number>` مدخلاً. هذه ذاكرة LRU مؤقتة
تتذكر عمليات البحث السابقة ونتائجها. تستخدمها ACLs والخرائط في عمليات البحث البطيئة عن
الأنماط، أي تلك التي تستخدم طرق المطابقة "sub" و"reg" و"dir" و"dom" و"end" و"bin" وكذلك
السلاسل غير الحساسة لحالة الأحرف. تنطبق على تعبيرات الأنماط ما يعني أنها ستكون قادرة على
حفظ نتيجة بحث بين جميع الأنماط المحددة على سطر إعداد واحد (بما في ذلك جميع تلك المحملة من
ملفات). تلغي تلقائيًا صلاحية المدخلات التي تُحدث باستخدام إجراءات HTTP أو على واجهة CLI.
حجم الذاكرة المؤقتة الافتراضي 10000 مدخل، ما يحد أثرها بنحو 5 ميغابايت لكل عملية/خيط على
الأنظمة 32-بت و8 ميغابايت لكل عملية/خيط على الأنظمة 64-بت، لأن الذاكرات المؤقتة محلية
لكل خيط/عملية. هناك خطر تصادم منخفض جدًا في هذه الذاكرة المؤقتة، وهو من رتبة حجم الذاكرة
مقسومًا على 2^64. نموذجيًا، عند 10000 طلب في الثانية مع الحجم الافتراضي للذاكرة المؤقتة
البالغ 10000 مدخل، توجد فرصة 1% لأن يسبب هجوم قوة غاشمة تصادمًا واحدًا بعد 60 عامًا، أو
0.1% بعد 6 أعوام. هذا يعتبر أدنى بكثير من خطر إتلاف ذاكرة تسببه مكونات هرمة. إن لم يكن
هذا مقبولًا، يمكن تعطيل الذاكرة المؤقتة بتعيين هذا المعامل إلى 0.

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

يحدد العدد الأقصى لتحديثات جداول الثبات (stick-table) التي سيحاول haproxy معالجتها دفعة
واحدة عند إرسال الرسائل. يتطلب استرجاع بيانات هذه التحديثات بعض عمليات القفل التي قد تكون
كثيفة الاستهلاك للCPU على الأجهزة كثيرة الخيوط إذا تركت بلا حد، وقد يزيد كذلك زمن استجابة
حركة البيانات خلال النقل الأولي المحزم بين عملية أقدم وعملية أحدث. وبالمقابل، القيم
المنخفضة قد تسبب أيضًا حمل CPU أعلى، وتستغرق وقتًا أطول للاكتمال. القيمة الافتراضية 200
ويقترح عدم تغييرها.

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

يضبط حجم مخزن الأنبوب في النواة إلى هذا الحجم (بالبايت). افتراضيًا، الأنابيب بالحجم
الافتراضي للنظام. لكن أحيانًا عند استخدام وصل TCP، يمكن تحسين الأداء بزيادة أحجام
الأنابيب، خاصة إذا اشتبه في أن الأنابيب لا تمتلئ وأن استدعاءات كثيرة لـ splice() تُنفذ.
يؤثر هذا في مقدار الذاكرة التي تستهلكها النواة، لذا يجب عدم تغيير هذا إن لم تكن الآثار مفهومة.

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

يحدد هذا الإعداد العدد الأقصى لواصفات الملفات (بالنسبة المئوية) المستخدمة من HAProxy
عالميًا مقابل العدد الأقصى لواصفات الملفات التي يستطيع HAProxy استخدامها قبل أن نبدأ قتل
الاتصالات الخاملة عندما لا يمكننا إعادة استخدام اتصال وعلينا إنشاء اتصال جديد. الافتراضي
هو 25 (ربع واصفات الملفات سيعني أن نحو نصف الاتصالات الأمامية القصوى يمكن أن يبقي خلفه
اتصالًا خاملًا، وأي تجاوز لهذا لا معنى له كثيرًا في الحالة العامة عند استهداف إعادة
استخدام الاتصالات).

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

يحدد هذا الإعداد العدد الأقصى لواصفات الملفات (بالنسبة المئوية) المستخدمة من HAProxy
عالميًا مقابل العدد الأقصى لواصفات الملفات التي يستطيع HAProxy استخدامها قبل أن نتوقف عن
وضع الاتصالات في مجموعة الخمول لإعادة الاستخدام. الافتراضي هو 20.

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

يفعل ('on') أو يعطل ('off') التمرير دون نسخ للبيانات من أجل مُضاعِف العبور المباشر (pass-
through). لكي يُستخدم، يجب إعداد وصل النواة (kernel splicing) أيضًا. وهو مفعل افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding, option splice-auto, option splice-request
وoption splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

يعرف كم حزمة مفقودة تلزم خوارزمية التحكم في الازدحام Cubic لتعتبر حدث فقدان حقيقيًا.
عاديًا، يعتبر أي حدث فقدان نتيجة ازدحام وهو كافٍ لكي يعيد Cubic البدء من نافذة أصغر. لكن
التجارب تظهر أنه يمكن أن تكون هناك مجموعة أسباب للفقدان لا يسببها الازدحام إطلاقًا ويمكن
ببساطة وصفها بالفقدان الزائف، والتي لن يكون لتعديل النافذة عليها أي أثر سوى إبطاء
الاتصال. ضعف إشارة الراديو، والتسليم خارج الترتيب، والاستخدام العالي للCPU على عميل يسبب
تأخيرات عشوائية، وكذلك عدم دقة مؤقت النظام، يمكن أن تكون من الأسباب الشائعة لهذا. يسمح
هذا الإعداد بجعل Cubic أكثر تسامحًا قليلًا مع الفقدان الزائف، عبر تغيير الحد الأدنى لعدد
الفقدانات المتراكمة بين ACK اثنين لتعتبر حدث فقدان، وقيمته الافتراضية 1. لوحظت بعض
المكاسب المهمة تجريبيًا، لكنها دائمًا مصحوبة بتفاقم عرض النطاق المهدر في إعادة الإرسال،
وزيادة خطر تشبع الوصلات المزدحمة. يمكن استخدام القيمة 2 لفترات قصيرة لمقارنة بعض
القياسات. لا تتجاوز 2 أبدًا دون تحليل مسبق من خبير للوضع. القيمة الافتراضية والدنيا هي 1.
استخدم 1 دائمًا.

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

يفعل ('on') أو يعطل ('off') خوارزمية HyStart++ (RFC 9406) لاتصالات QUIC المستخدمة بديلًا
عن مرحلة البدء البطيء لخوارزميات التحكم في الازدحام التي قد تسبب فقدان حزم مرتفعًا. وهي
معطلة افتراضيًا.

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

يحدد الحد الأقصى لعدد المرات التي يمكن فيها وسم إطار QUIC واحد بأنه مفقود. إذا جرى تجاوزه، يعتبر الاتصال فاشلًا
ويغلق فورًا.

القيمة الافتراضية هي 10.

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

يحدد الحجم الأقصى الافتراضي للنافذة لمتحكم الازدحام لاتصال QUIC واحد على جانب الواجهة
الأمامية أو الخلفية. يجب كتابة القيمة كعدد صحيح مع لاحقة اختيارية 'k' أو 'm' أو 'g'.
ويجب أن تقع بين 10k و4g.

يستخدم مُضاعِف QUIC أيضًا حجم نافذة الازدحام الحالية لتحديد ما إذا كان يستطيع تخصيص
مخازن تدفق جديدة عند إصدار البيانات. وعليه، يخدم حجم نافذة الازدحام القصوى حدًا على هذا
المخصص أيضًا.

القيمة الافتراضية هي 480k.

انظر أيضًا خياري bind وserver باسم "quic-cc-algo".

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

النسبة المطبقة على عتبة إعادة ترتيب الحزم المحسوبة. قد تطلق اكتشاف فقدان حزم مرتفعًا
عندما تكون صغيرة جدًا.

القيمة الافتراضية هي 50.

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

يحدد معاملات النقل max_idle_timeout لـ QUIC على جانب الواجهة الأمامية أو الخلفية. يتبع
تنسيق الوقت لدى HAProxy ويعبر عنه بالمللي ثانية. يحدد هذا فترة الوقت التي بعدها يغلق
اتصال بصمت إذا ظل خاملًا خلال فترة زمنية فعالة. يعتمد الطرفان على القيمة المتفاوض عليها
نفسها: - الحد الأدنى للمعاملين إذا لم يكن أي منهما صفريًا، - الحد الأقصى إذا كان واحد
منهما فقط غير صفري، - إذا كان المعاملان صفريين، فهذه الميزة معطلة.

القيمة الافتراضية هي 30s.

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

يحدد حد عدد الاختلالات لكل اتصال على جانب الواجهة الأمامية أو الخلفية، وعنده يُقتل ذلك
الاتصال تلقائيًا. يتيح هذا قتل الاتصالات سيئة السلوك تلقائيًا دون الحاجة إلى كتابة قواعد
صريحة لها. القيمة الافتراضية صفر، ما يدل على عدم تعيين أي حد بحيث لا يسبب أي حدث إغلاق
الاتصال. احترس من أن بعض عملاء QUIC قد يسببون أحيانًا بعض الاختلالات على اتصال طويل
الأمد، فأي قيمة غير صفرية هنا ينبغي غالبًا أن تكون بمئات أو آلاف لتكون فعالة دون التأثير
في العملاء المعيبين قليلًا. من الممكن أيضًا قتل الاتصالات فقط عندما يتجاوز استخدام CPU
مستوى معينًا، باستخدام "tune.glitches.kill.cpu-usage".

انظر أيضًا: fc_glitches, tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

يفعل ميزة Retry ديناميكيًا لجميع مستمعات QUIC المكونة بمجرد بلوغ هذا العدد من الاتصالات
نصف المفتوحة. الاتصال نصف المفتوح هو اتصال لم تكتمل مصافحته بنجاح أو تفشل بعد. لكي تكون
وظيفية، يحتاج هذا الإعداد إلى تعيين سر عنقود (cluster secret)، وإلا فسيُتجاهل بصمت (انظر
إعداد "cluster-secret"). سيُتجاهل هذا الإعداد بصمت أيضًا إذا كان استخدام QUIC Retry
مفروضًا (انظر "quic-force-retry").

القيمة الافتراضية هي 100.

انظر <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2> لمزيد من المعلومات حول
QUIC retry.

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

يحدد عالميًا كيف ستستخدم اتصالات الواجهة الأمامية لـ QUIC المقابس لعمليات الاستقبال/
الإرسال. تستطيع الاتصالات مشاركة مقبس المستمع أو يمكن لكل اتصال تخصيص مقبسه الخاص.

القيمة الافتراضية هي "default-on". تستخدم هذه لتخصيص مقبس مخصص لكل اتصال QUIC. هذا
الخيار هو المفضل لتحقيق أفضل أداء مع حركة QUIC كبيرة. وهو أيضًا السبيل الوحيد لضمان تنفيذ
التوقف الرشيق دون فقدان بيانات لاتصالات QUIC والتعامل بكفاءة مع حالات الأخطاء العابرة أثناء عملية
sendto(). لكن هذا يعتمد على بعض الميزات المتقدمة من رصة شبكة UDP. إذا اعتبرت
منصتك غير متوافقة، فسيحوّل haproxy تلقائيًا إلى وضع "force-off" عند الإقلاع. يرجى الملاحظة
أن مستمعات QUIC العاملة على منافذ تتطلب امتيازات قد تتطلب العمل بـ uid 0، أو بعض الضبط الخاص
بنظام التشغيل للسماح للـ uid الهدف بربط مثل هذه المنافذ، مثل قدرات النظام (system
capabilities). انظر أيضًا التوجيه العام "setcap".

تشير القيمة "force-off" إلى أن عمليات نقل QUIC ستحدث على مقبس المستمع المشترك. قد يكون
هذا الخيار حل وسط جيدًا لحركة صغيرة لأنه يسمح بتقليل استهلاك FD. لكن، لن يكون الأداء
أمثلًا بسبب استخدام CPU أعلى إذا كانت المستمعات مشتركة عبر خيوط كثيرة أو إذا كان يمكن
استخدام عدد كبير من اتصالات QUIC في آن واحد.

يطبق هذا الإعداد مقترنًا مع كل خيارات bind باسم "quic-socket". إذا استخدم وضع "default-on" في الضبط العام، فسيُفعل لكل مستمع، باستثناء تلك التي تحمل "quic-socket listener". أما
إذا استخدم "force-off" عالميًا، فيطبق على كل مثيل مستمع بغض النظر عن إعداده الفردي.

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. الخيار الأحدث اسمه "tune.quic.fe.sock-per-conn"، مع مقابلة
القيمة القديمة "connection" بـ "default-on" و"listener" بـ "force-off".

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

يتيح هذا الإعداد ضبط الحد الصارم لعدد بايتات البيانات قيد الإرسال على كل تدفق. يعبر عنه
كنسبة مئوية بالنسبة إلى إعداد اتصال rxbuf لتدفقات QUIC، مع تقريب الناتج صعودًا إلى bufsize.

القيمة الافتراضية هي 90. وهذا مناسب لسيناريو الويب الأكثر تكرارًا، حيث ينفذ الرفع لتدفق
واحد أو بضعة تدفقات فقط، بينما تستخدم البقية للتنزيل حصرًا. إذا بقي حد اتصال rxbuf
للتدفقات عند مستوى معقول، فإنه يضمن أن جزءًا فقط من التدفقات المفتوحة يستطيع التخصيص إلى
سعته القصوى.

في حالة تطبيق يستخدم تدفقات رفع كثيرة بالتوازي ويعاني عدم إنصاف بين هذه التدفقات، قد يكون
من المنطقي خفض هذه النسبة، لزيادة الإنصاف وتقليل عرض النطاق لكل تدفق.

انظر أيضًا: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

على جانب الواجهة الأمامية، يستخدم هذا كقيمة لمعامل النقل initial_max_streams_bidi
المعلن. يفرض هذا كعدد أقصى للتدفقات ثنائية الاتجاه التي سيصرح للنظير البعيد بفتحها
بالتزامن خلال مدة حياة الاتصال. يحد هذا فعليًا من عدد طلبات HTTP/3 المتزامنة من العميل.

القيمة الافتراضية هي 100. لاحظ أنك إذا خفضته، فقد يقيد قدرات التخزين المؤقت للتدفقات عند
الاستقبال، ما يؤدي إلى أداء رفع ضعيف. يمكن تصحيح ذلك بزيادة إعداد اتصال rxbuf لتدفقات
QUIC.

على جانب الواجهة الخلفية، يفرض هذا محليًا بواسطة haproxy للحد من عدد الطلبات المتزامنة
المضاعفة على اتصال واحد. قد يقيد هذا كذلك بواسطة التحكم بالتدفق لدى النظير. قد يلزم خفض
القيمة الافتراضية 100 لتحسين استجابة موقع على حساب عدد أعلى من اتصالات الواجهة الخلفية
المفتوحة. وعلى غرار جانب الواجهة الأمامية، يؤثر هذا الإعداد أيضًا مباشرة في قدرة التخزين
المؤقت للاستقبال (Rx)، لكنه يحد هذه المرة من قدرة تنزيل HTTP. يمكن زيادة إعداد rxbuf
لتدفقات QUIC عند التعامل غالبًا مع استجابات HTTP أكبر من "tune.bufsize".

انظر أيضًا: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

يحدد العدد الأقصى للطلبات التي يمكن التعامل معها بواسطة اتصال QUIC واحد. عند بلوغ هذا
الإجمالي، سيغلق الاتصال بإيقاف رشيق. في HTTP/3، يترجم هذا إلى إطار GOAWAY. يغلق الاتصال
أخيرًا عند اكتمال جميع عمليات النقل المتبقية.

يطبق هذا الإعداد كحد صارم على الاتصال عبر آلية التحكم بالتدفق لـ QUIC. إذا خالفه النظير،
سيغلق الاتصال فورًا.

يمكن استخدام هذا الإعداد لإجبار العملاء على فتح اتصالات جديدة من حين لآخر لمواصلة إصدار
الطلبات وتجنب الحفاظ على الاتصالات لأوقات كثيرة. لكن القيم المنخفضة ستزيد زمن الاستجابة
على جانب العميل، وكذلك استهلاك CPU على الجانبين بسبب مصافحات TLS.

القيمة الافتراضية هي 0 ما يعني عدم وجود حد محدد خارج قيد ترميز بروتوكول QUIC (2^60، أكثر
من مليار مليار).

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

هذا الإعداد هو الحد الصارم لعدد بايتات البيانات قيد الإرسال على اتصال واجهة أمامية QUIC.
يعاد استخدامه كقيمة لمعامل النقل initial_max_data. يؤثر مباشرة في عرض نطاق الرفع للنظير
بحسب زمن الاستجابة واستهلاك الذاكرة لكل اتصال في haproxy.

افتراضيًا، تعين القيمة إلى 0، ما يشير إلى أنه يجب توليدها تلقائيًا كحاصل ضرب max-concurrent في bufsize. يمكن زيادتها مثلًا إذا كان تطبيق واجهة خلفية يعتمد على عمليات رفع
ضخمة عبر شبكات عالية زمن الاستجابة.

انظر أيضًا: "tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

يفعل ('on') أو يعطل ('off') دعم الـ pacing لإصدار QUIC. افتراضيًا، هو نشط. الغرض من
الـ pacing هو تمهيد إصدار البيانات لتقليل فقدان الشبكة. في معظم السيناريوهات، سيرفع أداء
الشبكة بشكل ملحوظ عبر تجنب إعادة الإرسال. لكن، قد يكون من المفيد تعطيله للشبكات ذات عرض
النطاق المرتفع جدًا وزمن الاستجابة المنخفض لمنع تأخير غير مرغوب وتقليل استهلاك CPU.

انظر أيضًا خياري bind وserver باسم "quic-cc-algo".

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

يفعل ('on') أو يعطل ('off') دعم UDP GSO لإصدار QUIC. افتراضيًا، هو نشط. تسمح ميزة النواة
هذه بإصدار عدة مخططات بيانات عبر استدعاء نظام واحد وهو أكثر كفاءة للنقل الكبير. قد يكون
من المفيد تعطيلها بناء على اقتراح المطورين عند الاشتباه بمشكلة في الإصدار.

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

يعطل بروتوكول نقل QUIC على جانب الواجهة الأمامية. ستظل جميع مستمعات QUIC تنشأ، لكنها لن
تستمع للمخططات الواردة. ومن ثم، لن تعالج أي حركة QUIC بواسطة haproxy على جانب الواجهة
الأمامية.

القيمة الافتراضية هي "on". إذا اشتبه بمشكلة مع حركة QUIC، يمكن استخدام هذا الخيار
لتبديل مستمعات QUIC بسهولة دون العبث بكل سطر إعداد فردي.

انظر أيضًا عملية جلب العينة "quic_enabled".

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

يحدد الكمية القصوى من الذاكرة القابلة للاستخدام من رصة QUIC في طبقة النقل للإصدار. يخدم
هذا حدًا لبايتات قيد الإرسال ومخازن مخرجات المُضاعِف معًا. لاحظ أنه لمنع تنازع الخيوط لا
يفرض هذا الحد فرضًا صارمًا فقد يتجاوز في بعض المناسبات. أيضًا، سيكون كل اتصال قادرًا
دائمًا على استخدام نافذة لا تقل عن 2 مخطط بيانات، لذا ينبغي استخدام maxconn مناسب
بالاقتران معه.

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

أُهملت هذه الكلمة المفتاحية في الإصدار 3.3 وستُزال في 3.5. وهي جزء من عملية التبسيط
المطبقة على إعداد QUIC. إذا استخدمت، فلن يطبق هذا الإعداد إلا على اتصالات الواجهة
الأمامية.

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

يفعل ('on') أو يعطل ('off') الإرسال دون نسخ للبيانات من أجل مُضاعِف QUIC. وهو مفعل
افتراضيًا.

انظر أيضًا: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

يأخذ خيار الإعداد هذا قيمة بين -20 و19. يطبق أولوية جدولة كما هو موثق في man 2
setpriority. تطبق هذه الأولوية بعد تحليل الإعداد، ما يعني أن العامل أو العملية المستقلة
فقط ستطبقها. يكوَّن عادة لتعيين أولوية أعلى من عملية تقوم بتحليل الإعداد
(tune.renice.startup).

انظر أيضًا: tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

يأخذ خيار الإعداد هذا قيمة بين -20 و19. يطبق أولوية جدولة كما هو موثق في man 2
setpriority. تطبق هذه الأولوية قبل تطبيق بقية الإعداد، وقد يكون هذا مفيدًا إذا أردت خفض
الأولوية لتحليل الإعداد. يطبق هذا على العملية المستقلة أو العامل قبل تحليل الإعداد. بعد
تحليل الإعداد، تستعاد الأولوية السابقة إلا إذا استخدم tune.renice.runtime.

انظر أيضًا: tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

يضبط حجم مخزن استقبال مقبس النواة على المقابس غير المتصلة إلى هذا الحجم. يمكن استخدام
هذا لـ QUIC في وضع المستمع ولـ log-forward على الواجهة الأمامية. قد تكون مخازن النظام
الافتراضية صغيرة أحيانًا على المقابس المستقبلة لحركة مجمعة كثيرة، مما يسبب بعض الفقدان
وربما إعادة إرسال (في حالة QUIC)، وربما إبطاء إنشاء الاتصالات تحت الحمل الكبير. تعبر
القيمة بالبايت، وتطبق على كل مقبس. في وضع المستمع، تُشارك المقابس بين جميع الاتصالات،
ويعتمد العدد الكلي للمقابس على قيمة "shards" لسطر "bind". لا توجد قيمة صالحة للجميع،
فالقيمة الجيدة تقابل حجمًا متوقعًا لكل اتصال مضروبًا في العدد المتوقع للاتصالات. قد تقلم
النواة القيم الكبيرة. انظر أيضًا "tune.rcvbuf.client" و"tune.rcvbuf.server" لنظيريهما
على المقابس المتصلة، وكذلك "tune.sndbuf.backend" و"tune.sndbuf.frontend" لإعداد
الإرسال.

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

يفرض حجم مخزن استقبال مقبس النواة على جانب العميل أو الخادم إلى القيمة المحددة بالبايت.
تنطبق هذه القيمة على جميع الواجهات الأمامية والخلفية لـ TCP/HTTP. لا ينبغي عادة تعيينها
أبدًا، والحجم الافتراضي (0) يترك للنواة ضبط هذه القيمة تلقائيًا بحسب كمية الذاكرة
المتاحة. لكن قد يساعد أحيانًا تعيينها إلى قيم منخفضة جدًا (مثل 4096) من أجل توفير ذاكرة
النواة بمنعها من تخزين كميات كبيرة جدًا من البيانات المستقبلة مؤقتًا. القيم الأدنى سترفع
استخدام CPU بشكل ملحوظ مع ذلك.

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

يستخدم HAProxy بعض التلميحات لاكتشاف أن قراءة قصيرة تدل على نهاية مخازن المقبس. أحدها أن
عملية قراءة تعيد أكثر من `<recv_enough>` بايت، وقيمتها الافتراضية 10136 (7 مقاطع بـ 1448
لكل منها). قد تغير هذه القيمة الافتراضية بهذا الإعداد للتعامل بشكل أفضل مع أعباء عمل
تنطوي على رسائل قصيرة كثيرة مثل جلسات telnet أو SSH.

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

يحدد عدد طوابير الكتابة أمام المخازن الحلقية (ring buffers). قد يكون لهذا أثر في استخدام
CPU للتتبعات خلال جلسات التصحيح، وقيمة منخفضة جدًا أو كبيرة جدًا كليهما قد يكون لها أثر
مهم. حددت القيمة الجيدة تجريبيًا من قبل المطورين ولا ينبغي أن يكون هناك سبب لمحاولة
تغييرها إلا بتعليمات بذلك لمعالجة مشكلات محددة. لا ينبغي ترك مثل هذا الإعداد في الإعداد
عبر ترقيات الإصدارات لأن قيمته المثلى قد تتطور بمرور الوقت.

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

يحدد الكمية القصوى للمهام التي يمكن معالجتها دفعة واحدة عند تشغيل المهام. تعتمد القيمة
الافتراضية على عدد الخيوط لكنها تقع بين 35 و280، التي تميل إلى إظهار أعلى معدلات الطلبات
وأدنى أزمنة الاستجابة. زيادتها قد تسبب زمن استجابة عند التعامل مع عمليات الإدخال/الإخراج،
وجعلها صغيرة جدًا قد يسبب حملًا إضافيًا. أعداد الخيوط الأعلى تستفيد من القيم الأدنى. عند
التجريب بقيم أكبر بكثير، قد يكون من المفيد تفعيل tune.sched.low-latency أيضًا وربما
tune.fd.edge-triggered للحد من أقصى زمن استجابة إلى أدنى قدر ممكن.

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

يفعل ('on') أو يعطل ('off') مجدول المهام منخفض زمن الاستجابة. افتراضيًا يعالج HAProxy
المهام من عدة فئات فئة واحدة في كل مرة لأن هذا هو الأكثر كفاءة. لكن عند التشغيل بقيم
كبيرة لـ tune.runqueue-depth قد يكون لهذا أثر مقيس على زمن استجابة الطلبات أو الاتصالات.
عندما يكون إعداد زمن الاستجابة المنخفض هذا مفعلًا، ستُنفذ مهام الفئات ذات الأولوية الأدنى
دائمًا قبل غيرها إذا وُجدت. سيسمح هذا بخفض أقصى زمن استجابة تعانيه الطلبات أو الاتصالات
الجديدة في وسط حركة ضخمة، على حساب أثر أكبر على هذه الحركة الكبيرة. للاستخدام الاعتيادي
من الأفضل تركه معطلًا. القيمة الافتراضية معطلة (off).

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

يضبط حجم مخزن إرسال مقبس النواة على المقابس غير المتصلة إلى هذا الحجم. يمكن استخدام هذا
لمقبس UNIX وتسجيل UDP على جانب الواجهة الخلفية، ولـ QUIC في وضع المستمع على الواجهة
الأمامية. قد تكون مخازن النظام الافتراضية صغيرة أحيانًا على المقابس المشتركة بين اتصالات
كثيرة (أو مرسلي سجلات)، مما يسبب بعض الفقدان وربما إعادة إرسال، وإبطاء إنشاء اتصالات
جديدة تحت الحركة العالية. تعبر القيمة بالبايت، وتطبق على كل مقبس. في وضع المستمع، تُشارك
المقابس بين جميع الاتصالات، ويعتمد العدد الكلي للمقابس على قيمة "shards" لسطر "bind". لا
توجد قيمة صالحة للجميع، فالقيمة الجيدة تقابل حجمًا متوقعًا لكل اتصال مضروبًا في العدد
المتوقع للاتصالات. قد تقلم النواة القيم الكبيرة. انظر أيضًا "tune.sndbuf.client"
و"tune.sndbuf.server" لنظيريهما على المقابس المتصلة، وكذلك "tune.rcvbuf.backend"
و"tune.rcvbuf.frontend" لإعداد الاستقبال.

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

يفرض حجم مخزن إرسال مقبس النواة على جانب العميل أو الخادم إلى القيمة المحددة بالبايت.
تنطبق هذه القيمة على جميع الواجهات الأمامية والخلفية لـ TCP/HTTP. لا ينبغي عادة تعيينها
أبدًا، والحجم الافتراضي (0) يترك للنواة ضبط هذه القيمة تلقائيًا بحسب كمية الذاكرة
المتاحة. لكن قد يساعد أحيانًا تعيينها إلى قيم منخفضة جدًا (مثل 4096) من أجل توفير ذاكرة
النواة بمنعها من تخزين كميات كبيرة جدًا من البيانات المستقبلة مؤقتًا. القيم الأدنى سترفع
استخدام CPU بشكل ملحوظ مع ذلك. حالة استخدام أخرى هي منع مهلات الكتابة مع عملاء بطيئين
للغاية بسبب انتظار النواة قراءة جزء كبير من المخزن قبل إخطار HAProxy مجددًا. انظر أيضًا
tune.notsent-lowat.client وtune.notsent-lowat.server لإعدادات أكثر فاعلية للتحكم بدقة
أكبر في استخدام الذاكرة والاستجابة على Linux دون الإضرار بالأداء.

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

يحدد حجم تخزين جلسات SSL العام المؤقت، بعدد الكتل. الكتلة كبيرة بما يكفي لاحتواء جلسة
مرمزة دون شهادة النظير. أما الجلسة المرمزة مع شهادة النظير فتخزن في كتل متعددة بحسب حجم
شهادة النظير. تستهلك الكتلة ما يقارب 200 بايت من الذاكرة (استنادًا إلى حساب `sizeof(struct
sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE` المستخدم لدالة `shctx_init`). يمكن فرض القيمة
الافتراضية وقت البناء، وإلا فهي 20000. عندما يمتلئ التخزين المؤقت، تُمحى المدخلات الأكثر
خمولًا ويعاد تخصيصها. القيم الأعلى تقلل حدوث مثل هذا المحي، وبالتالي عدد مصافحات SSL
الكثيفة الاستهلاك للCPU عبر ضمان احتفاظ جميع المستخدمين بجلستهم أطول ما يمكن. تخصص جميع
المدخلات مسبقًا عند الإقلاع. تعيين هذه القيمة إلى 0 يعطل تخزين جلسات SSL المؤقت.

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

يحدد الحجم الأقصى للمخزن المستخدم لالتقاط قائمة خوارزميات التشفير في رسالة hello
العميل، وقائمة الامتدادات، وقائمة المنحنيات الإهليلجية، وصيغ نقاط المنحنى الإهليلجي. إذا
كانت القيمة 0 (القيمة الافتراضية) فالالتقاط معطل، وإلا خُصص مخزن لكل اتصال SSL/TLS.

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

يتيح هذا الإعداد ضبط دعم ضغط الشهادات وهو امتداد (RFC 8879) لـ TLS 1.3.

عند التعيين إلى "auto" يستخدم القيمة الافتراضية لمكتبة TLS.

مع "off" يحاول تعطيل دعم الميزة صراحة. لن يحاول HAProxy بعد الآن إرسال شهادات مضغوطة ولا
قبول شهادات مضغوطة.

يضبط جانبي الواجهة الخلفية والأمامية معًا.

تدعم OpenSSL \>= 3.2.0 هذه الكلمة المفتاحية.

القيمة الافتراضية هي auto.

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

يحدد الحجم الأقصى لمعاملات Diffie-Hellman المستخدمة لتوليد مفتاح Diffie-Hellman المؤقت/
الزائل في حالة تبادل مفاتيح DHE. سيحاول الحجم النهائي مطابقة حجم مفتاح RSA (أو DSA)
للخادم (مثلًا مفتاح DH مؤقت بحجم 2048 بت لمفتاح RSA بحجم 2048 بت)، لكنه لن يتجاوز هذه
القيمة القصوى. لا يسمح إلا بالقيم 1024 أو أعلى. القيم الأعلى سترفع حمل CPU، والقيم الأكبر
من 1024 بت غير مدعومة من عملاء Java 7 والأقدم. لا تستخدم هذه القيمة إذا زودت معاملات
Diffie-Hellman الثابتة إما مباشرة في ملف الشهادة أو باستخدام المعامل ssl-dh-param-file.
إذا لم يكن هناك default-dh-param ولا ssl-dh-param-file معرفين، وإذا لم يحدد ملف PEM
الخاص بخادم واجهة أمامية معينة معاملات DH الخاصة به، فستكون خوارزميات تشفير DHE غير
متاحة لهذه الواجهة الأمامية.

التوافق: `OpenSSL >= 1.1.1`. غير مدعوم مع `AWS-LC`.

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

يعطل هذا الخيار مشاركة تخزين جلسات SSL بين جميع العمليات. لا ينبغي استخدامه عادة لأنه
سيجبر على إعادة تفاوض كثيرة بسبب وصول العملاء إلى عملية عشوائية. لكنه قد يكون مطلوبًا على
بعض أنظمة التشغيل التي لا يمكن فيها استخدام أي من طرق مزامنة تخزين SSL المؤقت. في هذه
الحالة، قد يحد إضافة طبقة أولى من موازنة الحمل المعتمدة على التجزئة قبل طبقة SSL من أثر
غياب مشاركة الجلسات.

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

يحدد الكمية القصوى من البايتات الممررة إلى SSL_write() في أي وقت. القيمة الافتراضية 0
تعني عدم وجود حد. وعلى عكس tune.ssl.maxrecord لن يعدل هذا الإعداد ديناميكيًا. السجلات
الأصغر قد تخفض الإنتاجية، لكنها قد تكون مطلوبة عند التعامل مع عملاء محدودي الموارد.

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

يفعل هذا الخيار تسجيل مفاتيح TLS. ينبغي استخدامه بحذر لأنه سيستهلك مزيدًا من الذاكرة لكل
جلسة SSL وقد يخفض الأداء. هذا معطل افتراضيًا.

ينبغي استخدام عمليات جلب العينات هذه لتوليد SSLKEYLOGFILE المطلوب لفك تشفير حركة البيانات
مع wireshark.

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

SSLKEYLOG سلسلة من الأسطر المنسقة بهذه الطريقة:

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

يوفر ClientRandom من خلال عملية جلب العينة %[ssl_fc_client_random,hex]، أما السر
وLabel فيمكن إيجادهما في الجدول أدناه. تحتاج إلى توليد SSLKEYLOGFILE بجميع التسميات في
هذا الجدول.

عمليات جلب العينات التالية سلاسل سداسية عشرية ولا تحتاج إلى تحويل.

```text
  تسمية SSLKEYLOGFILE             |  عمليات جلب العينات للأسرار
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

توجد عمليات الجلب هذه للواجهة الأمامية (fc) أو الخلفية (bc)، استبدل "xx" بـ "fc" أو "bc"
لاستخدام الجانب الصحيح.

هذا متاح مع OpenSSL 1.1.1 فقط، ومفيد مع جلسات TLS1.3.

إذا أردت توليد محتوى SSLKEYLOGFILE مع TLS \< 1.3، فلا تحتاج سوى هذا السطر:

"CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]"

يمكن توليد سجل مفاتيح كامل بتنسيق سجل (log-format) بهذه الطرق، رغم أن هذا ليس مثاليًا
لـ syslog:

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

يوفر HAProxy أيضًا التنسيقات أعلاه كمتغيرات بيئة معرفة مسبقًا يمكن استخدامها مباشرة في
توجيه "log-format":

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   مفاتيح اتصالات الواجهة الأمامية (المواجهة للعميل)
$HAPROXY_KEYLOG_BC_LOG_FMT   مفاتيح اتصالات الواجهة الخلفية (المواجهة للخادم)
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

يحد كمية رسائل KeyUpdate في الثانية التي نرضى بقبولها إلى `<limit>` قبل اعتبار الأمر
فيضانًا، وقتل الاتصال. التعامل مع KeyUpdate مكلف للCPU، ولا سبب وجيهًا لاستقبال الكثير
منها. استخدام قيمة "0" يعطل تحديد المعدل. القيمة الافتراضية هي 100. <a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

يحدد كم يمكن لجلسة SSL مخزنة مؤقتًا أن تبقى صالحة. يعبر عن هذا الوقت بالثواني وقيمته
الافتراضية 300 (5 دقائق). من المهم فهم أنه لا يضمن بقاء الجلسات هذه المدة، لأنه إذا امتلأ
التخزين المؤقت، ستُمحى الجلسات الأطول خمولًا رغم مدة حياتها المكونة. الفائدة الحقيقية من هذا
الإعداد هي منع استخدام الجلسات لمدة طويلة جدًا.

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

يحدد الكمية القصوى من البايتات الممررة إلى SSL_write() في بداية نقل البيانات. القيمة
الافتراضية 0 تعني عدم وجود حد. عبر SSL/TLS، لا يستطيع العميل فك تشفير البيانات إلا بعد
استقباله سجلًا كاملًا. فمع السجلات الكبيرة، يعني هذا أن العملاء قد يضطرون إلى تنزيل ما
يصل إلى 16kB من البيانات قبل البدء في معالجتها. تحديد القيمة قد يحسن أزمنة تحميل الصفحات
على المتصفحات الواقعة عبر شبكات عالية زمن الاستجابة أو منخفضة عرض النطاق. يقترح إيجاد قيم
مثلى تتسع في مقطع TCP واحد أو مقطعين (عمومًا 1448 بايت عبر Ethernet مع تفعيل طوابع زمن
TCP، أو 1460 عند تعطيل الطوابع الزمنية)، مع وضع في الذهن أن SSL/TLS يضيف بعض الحمل. أعطت
القيم النموذجية 1419 و2859 نتائج جيدة خلال الاختبارات. استخدم "strace -e trace=write"
لإيجاد القيمة الأفضل. سينتقل HAProxy تلقائيًا إلى هذا الإعداد بعد اكتشاف تدفق خامل (انظر
tune.idletimer أعلاه). انظر أيضًا tune.ssl.hard-maxrecord.

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

يحدد حجم الذاكرة المؤقتة المستخدمة لتخزين الشهادات المولدة إلى `<number>` مدخلاً. هذه
ذاكرة LRU مؤقتة. ولأن توليد شهادة SSL ديناميكيًا مكلف، فإنها تخزن مؤقتًا. حجم الذاكرة
المؤقتة الافتراضي 1000 مدخل.

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

يعرف نسبة مستهدفة من التدفقات لكل اتصال واجهة أمامية بالنسبة إلى العدد الأقصى للاتصالات
المتزامنة (maxconn) عندما تنشأ جميع الاتصالات. ينطبق هذا القياس على البروتوكولات المضاعفة
مثل HTTP/2 أو QUIC، حيث قد يستقبل كل اتصال تدفقات متعددة. يضمن واحد على الأقل دائمًا، لذا
يجب أن تكون النسبة 100% على الأقل. خلال إنشاء الاتصال، يعلن HAProxy ديناميكيًا عن تدفقات
إضافية حتى الحد المكون، محافظًا على النسبة المستهدفة. عند إنشاء الاتصال، يستقبل كل اتصال
واجهة أمامية تدفقًا واحدًا على الأقل؛ وتخصص التدفقات الإضافية بناء على النسبة المستهدفة
وحدود التدفقات المكونة. يضمن هذا تخصيصًا فعالًا للتدفقات تحت أحمال متغيرة (تدفقات أكثر
عند الأحمال المنخفضة، وأقل عند الأحمال العالية).

تستفيد المواقع شديدة الديناميكية ذات الكائنات الكثيرة في كل صفحة من النسب العالية، ما
يمكن من تدفقات كثيرة لكل اتصال. أما المواقع التي تستخدم تدفقات أقل في المتوسط (WebSocket،
كود التطبيقات) فقد تفضل نسبًا صغيرة أقرب إلى 120 أو 150 (20 إلى 50% تدفقات أكثر من
الاتصالات) لمنع أعداد تدفقات مفرطة تحت الأحمال المستمرة.

القيمة الافتراضية هي 0، ما يعني عدم فرض أي حد على هذا المستوى، فتطبق إعدادات H2 وQUIC
فقط (مع الإعداد الافتراضي البالغ 100 تدفق لكل اتصال، يقابل هذا 10000%). يبقى هذا الإعداد
الموصى به لبيئات النشر الصغيرة (maxconn حول الألف). بيئات النشر متوسطة الحجم (بضعة آلاف إلى عشرات
آلاف الاتصالات) تضبط النسبة نموذجيًا بين 1000 و5000، ما يسمح بـ 10 إلى 50 تدفقًا لكل
اتصال عند الحمل الكامل. أما بيئات النشر واسعة النطاق (large-scale) (مئات الآلاف إلى ملايين
الاتصالات) فقد تستخدم قيمًا أدنى (120 إلى 200) لدعم 1.2 إلى 2 تدفق لكل اتصال في المتوسط
عند الحمل الكامل.

بخلاف HTTP/2، يستطيع QUIC تعديل عدد التدفقات المتزامنة ديناميكيًا خلال مدة حياة الاتصال.
لكن، التحكم بتدفق QUIC أصرم من HTTP/2، لذا يفضل عند استخدامه تحديد قيم كبيرة بما يكفي لمنع
زمن استجابة إضافي على الاتصال. هناك أيضًا قيد لمستمعات QUIC مع تفعيل 0-RTT. في هذه
الحالة، ستتجاهل القيمة الأولية المعلنة للنظير مرونة التدفقات وستعتمد حصرًا على إعداد
"tune.quic.fe.stream.max-concurrent". لكن، سيبقى مبدأ مرونة التدفقات ساريًا بعد هذا
الإعلان الأولي خلال مدة حياة الاتصال.

مراقبة العدد الكلي للتدفقات النشطة على الواجهات الخلفية، بما في ذلك الطوابير، توفر مؤشرًا
عمليًا لحمل مستهدف مستدام وتساعد على تجنب التخصيص الزائد.

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

يحدد عدد عدادات الثبات (stick-counters) التي يمكن تتبعها في آن واحد بواسطة اتصال أو طلب
عبر إجراءات "track-sc\*" في قواعد "tcp-request" أو "http-request". القيمة الافتراضية تضبط
وقت البناء بالماكرو MAX_SESS_STK_CTR، وقيمتها الافتراضية 3. بهذا الإعداد يمكن تغيير القيمة
وتجاهل القيمة الممررة وقت البناء، لكن لا يمكن تعيينها إلى قيمة أكبر من 100. قد تكون زيادة
هذه القيمة مطلوبة عند نقل إعدادات معقدة إلى haproxy، لكن يحذر المستخدمون من التكاليف: كل
مدخل يأخذ 16 بايت لكل اتصال و16 بايت لكل طلب، وجميعها يجب تخصيصها وتصفيرها لجميع الطلبات
حتى عندما لا تستخدم. وعليه فإن قيمة 10 ستنفخ استهلاك الذاكرة لكل طلب بمقدار 320 بايت
وستجعل هذه الذاكرة تمحى لكل طلب، ما له آثار مقيسة على CPU. وبالمقابل، عندما لا تستخدم
قواعد "track-sc"، يمكن خفض القيمة (و0 قيمة صالحة لتعطيل عدادات الثبات كليًا).

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

افتراضيًا، لن نحاول استخدام الاتصالات الخاملة من مجموعات الخيوط الأخرى. لكن يمكن تغيير
هذا. القيم الصالحة لـ `<value>` هي: "none"، الافتراضية، إذا استخدمت فلن تبذل أي محاولة
لاستخدام اتصالات خاملة من مجموعات خيوط أخرى، و"restricted" حيث سنحاول فقط الحصول على
اتصال خامل من خيط آخر إذا كنا نستخدم بروتوكولات لا تستطيع إنشاء اتصالات جديدة، مثل reverse
http، وكذلك عند استخدام strict-maxconn، و"full" حيث سنبحث دائمًا في مجموعات الخيوط الأخرى
عن اتصالات خاملة. لاحظ أن استخدام اتصالات من مجموعات خيوط أخرى قد يسبب عقوبات أداء، لذا
لا ينبغي استخدامه إلا عند الحاجة الفعلية. لاحظ أن هذا السلوك يتحكم فيه الآن
tune.idle-pool.shared، وهذه الكلمة المفتاحية موجودة فقط للتوافق مع الإعدادات الأقدم،
وستهمَل.

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

تساعد إعدادات tune الخمسة هذه على إدارة الكمية القصوى من الذاكرة المستخدمة من نظام
المتغيرات. يحد "global" الكمية الكلية للذاكرة المتاحة لجميع النطاقات. ويحد "proc" الذاكرة
لنطاق العملية، ويحد "sess" الذاكرة لنطاق الجلسة، و"txn" لنطاق المعاملة، ويحد "reqres"
الذاكرة لمعالجة كل طلب أو استجابة. محاسبة الذاكرة هرمية، ما يعني أن الحدود الأكثر خشونة
تضم الأدق: فـ "proc" يضم "sess"، و"sess" يضم "txn"، و"txn" يضم "reqres".

فمثلًا، عندما يحد "tune.vars.sess-max-size" إلى 100، فلن يستطيع "tune.vars.txn-max-size"
و"tune.vars.reqres-max-size" تجاوز 100 أيضًا. إذا أنشأنا متغير "txn.var" يحوي 100 بايت،
تكون جميع المساحة المتاحة قد استهلكت. لاحظ أن تجاوز الحدود في وقت التشغيل لن يؤدي إلى رسالة
خطأ، لكن القيم قد تُقلم أو تتلف. لذا تأكد من التخطيط بدقة لمقدار المساحة اللازمة لتخزين
جميع متغيراتك.

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

يحدد المعامل memLevel في تهيئة zlib لكل تدفق. يحدد كم ينبغي تخصيص ذاكرة لحالة الضغط
الداخلية. القيمة 1 تستخدم أدنى ذاكرة لكنها بطيئة وتخفض نسبة الضغط، والقيمة 9 تستخدم أقصى
ذاكرة للسرعة المثلى. يمكن أن تكون قيمة بين 1 و9. القيمة الافتراضية هي 8.

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

يحدد حجم النافذة (حجم المخزن التاريخي) كمعامل في تهيئة zlib لكل تدفق. القيم الأكبر لهذا
المعامل تنتج ضغطًا أفضل على حساب استخدام الذاكرة. يمكن أن تكون قيمة بين 8 و15. القيمة
الافتراضية هي 15.

## 3.3. التصحيح {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

يعين هذا مفتاح إخفاء الهوية العام إلى `<key>`، ويجب أن يكون عددًا بحجم 32 بت بين 0
و4294967295. هذا هو المفتاح الذي سيستخدم افتراضيًا بواسطة أوامر CLI عندما يكون وضع إخفاء
الهوية مفعلًا. يمكن أيضًا تعيين هذا المفتاح في وقت التشغيل من أمر CLI باسم "set anon
global-key". انظر أيضًا وسيطة سطر الأوامر "-dC" في دليل الإدارة.

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

يفعل ('on') أو يعطل ('off') تحديث عدادات الأحداث في الكود. هذه هي العدادات المبلغة عنها
تحت النوع "CNT" في أمر CLI باسم "debug counters". لا تتوفر هذه العدادات إلا إذا بني الكود
مع DEBUG_COUNTERS بتعيين قيمة 1 أو أعلى. فبالقيمة 1، لا تعدل العدادات افتراضيًا
("debug.counters off")، وبالقيمة 2 تعدل افتراضيًا ("debug.counters on"). لا يوجد عاديًا سبب
لتغيير هذا الإعداد إلا بطلب من مطور، أو إلا إذا اشتبه في أنه يستهلك كميات غير طبيعية من
CPU (وفي هذه الحالة يلزم تقرير إلى المطورين مع تفريغ للعدادات). من الممكن أيضًا تغيير هذه
الحالة في وقت التشغيل باستخدام أمر CLI باسم "debug counters". يرجى الرجوع إلى دليل
الإدارة.

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

يوقف هذا الأمر محلل الإعداد لمدة `<timeout>` مللي ثانية. هذا مفيد للتطوير أو لاختبار
مهل نصوص الإقلاع، خصوصًا لمحاكاة إعادة تحميل طويلة جدًا. يتطلب أن يكون expose-experimental-directives معينًا.

`<timeout>` هي قيمة المهلة محددة بالمللي ثانية افتراضيًا، ولكن يمكن أن تكون بأي وحدة
أخرى إذا أُلحقت وحدة القياس بالرقم، كما هو موضح في أعلى هذا المستند.

مثال:

```text
global
    expose-experimental-directives
    force-cfg-parser-pause 10s
```

<a id="entry-3-3-quick-exit"></a>

**`quick-exit`**

```haproxy
quick-exit
```

يسرع هذا خروج العملية القديمة عند إعادة التحميل عبر تخطي تحرير كائنات الذاكرة
والمستمعات، بما أن كل هذه يستردها نظام التشغيل عند موت العملية. المكاسب هامشية فقط (في
رتبة بضع مئات من المللي ثانية للإعدادات الضخمة على الأكثر). الاستخدام الرئيسي المستهدف في
الواقع هو عند اكتشاف عطل في كود deinit()، إذ يتيح هذا تجاوزه. من الأفضل عدم استخدام هذا
إلا بتعليمات من المطورين.

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

لا تعرض أي رسالة خلال الإقلاع. وهو يعادل وسيطة سطر الأوامر "-q".

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

يتيح هذا ضبط التأخير الذي بعده ستسبب مهمة عالقة تسد حركة البيانات إصدار تحذير على مخرج
الخطأ القياسي. يعبر عن التأخير بالمللي ثانية وقيمته الافتراضية 100 ms. يجب أن تكون القيم
المسموح بها بين 1 ms و1000 ms شاملة الطرفين. القيم الأدنى ستطلق تحذيرات بشكل متكرر
والأعلى نادرًا. سيقتل المراقب (watchdog) مهمة هاربة تفشل في الاستجابة مرتين لمدة ثانية على
أي حال، فتأخير تحذير 1000 ms لن يطلق عاديًا أي تحذير. يوصى بالبقاء مع قيم بين 10
و100ms لاكتشاف شذوذات الإعداد التي قد تخفض تجربة المستخدم، مسببة أزمنة استجابة طويلة أو
تقطيعًا في الجلسات التفاعلية. فمثلًا، دالة جلب عينة Lua سيئة التصميم تقوم بحسابات ثقيلة،
أو ملف خريطة map_reg أو map_regm كبير جدًا بتكلفة تقييم عالية جدًا قد يسببا مثل هذا
العناء. للمقارنة، تستطيع مصافحة TLS التهام ما بين واحد واثنين من المللي ثانية، وضغط مخزن
استجابة HTTP بحجم 16kB يستغرق حوالي مللي ثانية واحدة. يحوي المخرج تفريغًا لخيوط المهمة
المسببة للمشكلة مع تتبع خلفي (backtrace) وبعض السياق يساعد على تحديد أين يصرف الوقت.

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

عندما يكون هذا الخيار معينًا، سيرفض HAProxy الإقلاع إذا صدر أي تحذير أثناء معالجة الإعداد
وتطبيقه. ويعني هذا أن التحذيرات بشأن مجموعات سيئة من المعاملات، والتحذيرات بشأن حدود
عالية جدًا تعذر تعيينها، وما إلى ذلك، تجعل العملية تخرج بخطأ خلال الإقلاع. لا يستطيع هذا
الخيار التقاط بعض تحذيرات الإقلاع المتأخرة، مثل الفشل في إسقاط المجموعات التكميلية عند
تغيير معرف المجموعة في وضعي "daemon" أو "master-worker"، أو الفشل في وسم العملية قابلة
للتفريغ بعد fork(). لا يلتقط هذا الخيار التحذيرات الصادرة في وقت التشغيل. يوصى بشدة
بتعيين هذا الخيار على الإعدادات التي لا تتغير كثيرًا، لأنه يساعد على اكتشاف الأخطاء
الدقيقة والإبقاء على الإعداد نظيفًا ومتوافقًا مع المستقبل. لاحظ أن "haproxy -c" سيبلغ عن
الأخطاء أيضًا في مثل هذه الحالة. هذا الخيار يعادل وسيطة سطر الأوامر "-dW".

## 3.4. ضبط HTTPClient {#section-3-4}

HTTPClient مكتبة HTTP داخلية، يمكن استخدامها من مختلف الأنظمة الفرعية، مثلًا في نصوص LUA
البرمجية. لا يستخدم HTTPClient في مسار البيانات، أي أنه لا علاقة له بحركة HTTP المارة عبر
HAProxy.

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

يعطل حل DNS للـ httpclient. يمنع إنشاء قسم resolvers باسم "default".

القيمة الافتراضية هي off.

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

يعرف هذا الخيار قسم resolvers الذي سيحاول httpclient الحل من خلاله.

الخيار الافتراضي هو معرف resolvers باسم "default". افتراضيًا، إذا لم يستخدم هذا الخيار،
فسيتم ببساطة تعطيل الحل إذا لم يعثر على القسم.

لكن، عندما يفعل هذا الخيار صراحة فسيطلق خطأ إعداد إذا أخفق في التحميل.

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

يتيح هذا الخيار اختيار أي عائلة IP تريد عند الحل، وهو ملائم عندما لا يتوفر IPv6 على
شبكتك. الخيار الافتراضي هو "ipv6".

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

يتيح هذا الخيار ضبط عدد محاولات إعادة المحاولة للـ httpclient عندما يفشل طلب. يفعل هذا
الأمر نفسه الذي تفعله الكلمة المفتاحية "retries" في واجهة خلفية.

القيمة الافتراضية هي 3.

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

يعرف هذا الخيار ملف ca الذي ينبغي استخدامه للتحقق من شهادة الخادم. يأخذ المعاملات نفسها
التي يأخذها خيار "ca-file" على سطر الخادم.

افتراضيًا وعندما لا يستخدم هذا الخيار، تكون القيمة "@system-ca" التي تحاول تحميل CA الخاص
بالنظام. إذا فشل فستعطل SSL للـ httpclient.

لكن، عندما يفعل هذا الخيار صراحة فسيطلق خطأ إعداد إذا فشل.

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

يعمل بالطريقة نفسها التي يعمل بها خيار verify على أسطر الخوادم. إذا حدد إلى 'none'، فلن
يتم التحقق من شهادات الخوادم. الخيار الافتراضي هو "required".

افتراضيًا وعندما لا يستخدم هذا الخيار، تكون القيمة "required". إذا فشل فستعطل SSL للـ
httpclient.

لكن، عندما يفعل هذا الخيار صراحة فسيطلق خطأ إعداد إذا فشل.

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

يحدد أقصى وقت لانتظار محاولة اتصال افتراضيًا للـ httpclient.

الوسائط:

```text
<timeout> هي قيمة المهلة محددة بالمللي ثانية افتراضيًا، ولكن يمكن أن
          تكون بأي وحدة أخرى إذا أُلحقت وحدة القياس بالرقم، كما هو موضح
          في أعلى هذا المستند.
```

القيمة الافتراضية هي 5000ms.
