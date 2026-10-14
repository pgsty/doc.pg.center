---
title: "3. Секция global"
linkTitle: "3. Секция global"
weight: 140
description: "Безопасность процессов, настройка производительности, отладка и параметры HTTP-клиента"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [Справочник]
aliases:
  - /haproxy/configuration/global/
  - /docs/haproxy/configuration/global/
  - /haproxy/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

Параметры секции "global" действуют на весь процесс и часто зависят от ОС. Обычно их задают один раз, и после правильной настройки менять их не требуется. У некоторых есть эквиваленты в командной строке.

В секции "global" поддерживаются следующие ключевые слова:

- Управление процессами и безопасность

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

- Настройка производительности

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
  - tune.quic.cc.cubic.min-losses (устарело)
  - tune.quic.cc-hystart (устарело)
  - tune.quic.disable-tx-pacing (устарело)
  - tune.quic.disable-udp-gso (устарело)
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
  - tune.quic.frontend.max-data-size (устарело)
  - tune.quic.frontend.max-idle-timeout (устарело)
  - tune.quic.frontend.max-streams-bidi (устарело)
  - tune.quic.frontend.max-tx-mem (устарело)
  - tune.quic.frontend.stream-data-ratio (устарело)
  - tune.quic.frontend.default-max-window-size (устарело)
  - tune.quic.listen
  - tune.quic.max-frame-loss (устарело)
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio (устарело)
  - tune.quic.retry-threshold (устарело)
  - tune.quic.socket-owner (устарело)
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
  - tune.ssl.capture-cipherlist-size (устарело)
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay (устарело)
  - tune.ssl.ocsp-update.mindelay (устарело)
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- Debugging

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

## 3.1. Управление процессами и безопасность {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

Путь к файлу данных 51Degrees для определения устройств. Файл следует распаковать и предоставить HAProxy необходимые права доступа к нему.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES.

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

Список имён свойств 51Degrees, которые нужно загрузить из набора данных. Полный список имён доступен на сайте 51Degrees: <https://51degrees.com/resources/property-dictionary>

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES.

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

Символ, добавляемый после каждого значения свойства в заголовке ответа с результатами 51Degrees. Если не задан, используется ','.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES.

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

Задаёт размер кэша преобразователя 51Degrees: `<number>` записей. Этот кэш LRU хранит результаты предыдущих определений устройств. По умолчанию кэш отключён.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES.

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

Включает ('on') или отключает ('off') использование графа производительности при определении устройства. Значение по умолчанию зависит от библиотеки 51Degrees.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES и 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

Включает ('on') или отключает ('off') использование прогнозного графа при определении устройства. Значение по умолчанию зависит от библиотеки 51Degrees.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES и 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

Задаёт допустимую величину смещения при определении устройства.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES и 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

Задаёт допустимую величину различия при определении устройства.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES и 51DEGREES_VER=4.

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

Включает ('on') или отключает ('off') использование несовпавших узлов при определении устройства. Значение по умолчанию зависит от библиотеки 51Degrees.

Обратите внимание: этот параметр доступен только в том случае, если HAProxy собран с USE_51DEGREES и 51DEGREES_VER=4.

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

Включает или отключает планировщик ACME.

Планировщик ACME запускается при старте HAProxy. Он перебирает сертификаты и запускает задачу обновления ACME, когда значение notAfter оказывается раньше curtime + (notAfter - notBefore) / 12; если notBefore не определено, используется интервал 7 дней. Затем планировщик переходит в режим ожидания и просыпается через 12 часов.

Значение по умолчанию — "auto".

См. также: acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

Задаёт каталог по умолчанию для загрузки сертификатов центров сертификации SSL и списков отзыва CRL, когда в директивах "ca-file", "ca-verify-file" или "crl-file" указан относительный путь. Абсолютные пути в "ca-file", "ca-verify-file" и "crl-file" имеют приоритет; "ca-base" в этом случае игнорируется.

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

Меняет текущий каталог на `<jail dir>` и выполняет в нём chroot() перед сбросом привилегий. Это повышает безопасность при эксплуатации неизвестной уязвимости, поскольку существенно затрудняет атакующему дальнейшее воздействие на систему. Важно убедиться, что каталог `<jail dir>` пуст и никому не доступен для записи. Если процесс запущен с правами суперпользователя, chroot() выполняется напрямую. В Linux при запуске без привилегий haproxy пытается выполнить его в новом пользовательском пространстве имён, созданном с помощью unshare(CLONE_NEWUSER); если этот механизм недоступен, chroot() завершается обычной ошибкой.

В качестве особого случая для `<jail dir>` можно указать "auto". Тогда haproxy создаёт анонимный временный каталог, удаляет ссылку на него и выполняет chroot в этот каталог. Полученная изолированная среда не имеет имени в файловой системе, пуста и доступна только для чтения; отдельный каталог для неё подготавливать не требуется.

Если при запуске с правами суперпользователя chroot не используется, выводится предупреждение, призывающее всегда применять этот механизм. Если есть веская причина отказаться от chroot, например доступ к серверу через сокет UNIX с неудобным путём, предупреждение можно отключить, явно добавив "chroot /". Преимущество такой записи в том, что она видна в конфигурации.

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

Задаёт временной интервал, по которому распределяется закрытие простаивающих и активных соединений при плавной остановке. После получения SIGUSR1 и окончания льготного периода, если он задан, при отсутствии этого параметра все простаивающие соединения закрываются сразу. Активные соединения HTTP или HTTP2 завершаются после получения следующего запроса: в ответ HTTP добавляется строка "Connection: close", а в случае HTTP2 отправляется кадр GOAWAY. Если параметр задан, закрытие соединений распределяется по указанному интервалу `<time>`. Если close-spread-time имеет значение "infinite", закрытие активных соединений при плавной остановке отключается. Заголовок "Connection: close" больше не добавляется в ответы HTTP, а GOAWAY не отправляется для HTTP2; простаивающие соединения закрываются только по истечении их тайм-аутов, определяемых соответствующими параметрами конфигурации.

Аргументы:

```text
<time>  — временной интервал (по умолчанию в миллисекундах), на протяжении
        которого распределяется закрытие соединений при мягкой остановке;
        значение "infinite" отключает активное закрытие соединений.
```

Если используется параметр "hard-stop-after", для этого параметра рекомендуется задать меньшее значение, чтобы все соединения успели корректно закрыться до остановки процесса.

См. также: grace, hard-stop-after, idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

Задаёт общий секрет в виде строки ASCII для нескольких узлов одного кластера. Он может применяться для разных целей. В частности, из него выводятся токены сброса без сохранения состояния для всех соединений QUIC, созданных этим процессом, а также секреты для шифрования токенов Retry.

Если этот параметр не задан, при запуске процесса выбирается случайное значение. Это позволяет использовать зависящие от него возможности, хотя и с некоторыми ограничениями.

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

В некоторых операционных системах группу потоков или отдельный поток можно привязать к определённому набору CPU. Это означает, что указанные потоки никогда не будут выполняться на других CPU. Директива "cpu-map" задаёт наборы CPU для отдельных потоков или групп потоков. Первый аргумент — диапазон групп потоков, за которым можно указать набор потоков. Эти диапазоны имеют следующий формат:

```text
all | odd | even | number[-[number]]
```

`<number>` должен быть числом от 1 до 32 или 64 в зависимости от разрядности машинного слова. Идентификаторы групп, превышающие 'thread-groups', и идентификаторы потоков, превышающие разрядность машинного слова, игнорируются. Все номера потоков отсчитываются относительно группы, к которой они принадлежат. Диапазон можно задать двумя такими числами, разделёнными дефисом ('-'). Можно также указать все потоки сразу с помощью "all", только потоки с нечётными номерами с помощью "odd" или с чётными номерами с помощью "even", как и в директиве привязки "thread". Второй и последующие аргументы — наборы CPU. Каждый набор CPU задаётся либо одним номером, начиная с 0 для первого CPU, либо диапазоном из двух таких номеров, разделённых дефисом ('-'). Номера и диапазоны CPU можно перечислять через запятую или передавать дополнительные диапазоны как новые аргументы в той же строке. В операционных системах, отличных от Linux и BSD, максимальный индекс CPU может быть ограничен значением 31 или 63. Можно задать несколько директив "cpu-map", но каждая из них заменяет предыдущие в той части, где они пересекаются.

Диапазоны можно задавать частично: верхнюю границу можно опустить. Тогда вместо неё используется соответствующее максимальное значение — 32 или 64 в зависимости от разрядности машинного слова.

Перед набором потоков можно добавить префикс "auto:", чтобы HAProxy автоматически привязывал потоки к CPU, последовательно увеличивая номера потоков и CPU в наборах. Оба набора должны иметь одинаковый размер. Независимо от порядка объявления наборов CPU привязка выполняется от меньшего номера к большему. С префиксом "auto:" нельзя одновременно задавать диапазон групп и диапазон потоков. Поддерживается только один диапазон; второй элемент должен быть фиксированным числом.

Обратите внимание: диапазоны групп поддерживаются по историческим причинам. Сейчас отдельное число обозначает группу потоков; если группы потоков не используются, оно должно быть равно 1. При указании номера или диапазона потоков без использования групп потоков перед ним необходимо добавить "1/". Запись "1" полностью эквивалентна "1/all" и обозначает все потоки группы.

Примеры:

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

Определяет способ привязки потоков к CPU. Сейчас поддерживаются следующие значения:

- per-core: каждый поток привязывается ко всем аппаратным потокам одного ядра.
- per-group: каждый поток привязывается ко всем аппаратным потокам группы. Это значение по умолчанию,
  если в "cpu-policy" не задано "threads-per-core 1". "per-group" принимает необязательный аргумент,
  определяющий распределение CPU. Когда список CPU превышает максимально допустимое число CPU в группе
  и его нужно разделить между несколькими группами, дополнительный параметр позволяет выбрать способ
  привязки групп к этим CPU:
  - auto: каждой группе потоков выделяется соразмерная доля последовательных ядер CPU, которые
    используются только ею и не разделяются с другими группами. Это значение по умолчанию, поскольку
    обычно оно обеспечивает более оптимальную работу.
  - loose: каждой группе по-прежнему разрешается использовать любой CPU из списка. Обычно это
    усиливает конкуренцию за ресурсы, но иногда помогает лучше справляться с посторонней нагрузкой
    на тех же CPU.
- auto: обычно используется "per-group". Если в "cpu-policy" задано "threads-per-core 1",
  используется "per-core". Это значение по умолчанию.
- per-thread: каждый поток привязывается только к одному аппаратному потоку. Если в "cpu-policy"
  задано "threads-per-core 1", каждый поток привязывается к одному аппаратному потоку отдельного ядра.
- per-ccx: каждый поток привязывается ко всем аппаратным потокам одного CCX.

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

Выбирает политику распределения CPU.

В системах с несколькими CPU может быть много причин не использовать все доступные ядра или распределять их по разным группам потоков: производительность, задержки, стоимость или управление ресурсами всей системы. Директива "cpu-set" уже позволяет исключить часть CPU, но после этого нужно решить, как распределить оставшиеся между потоками и группами потоков.

Обычно это распределение задаётся директивой "cpu-map", однако в неоднородных системах поддерживать такую настройку может быть особенно трудно.

Если "cpu-map" не используется, директива "cpu-policy" позволяет выбрать вместо него одну из нескольких политик распределения. Сейчас поддерживаются следующие политики; по умолчанию используется "performance":

- none: дополнительный отбор не выполняется. Можно использовать все включённые CPU. Если число
  потоков не задано, оно принимается равным числу доступных CPU, но не более 32 в 32-битных системах
  или 64 в 64-битных системах на одну группу потоков. Если число групп потоков не задано, используется 1.

- efficiency: работает так же, как описанная ниже "group-by-ccx", но исключает кластеры CPU из ядер,
  производительность которых более чем на 25% превышает производительность следующего, менее
  производительного типа. Обычно это ядра "big" или "performance". Таким образом, при обнаружении
  нескольких типов ядер CPU используется только энергоэффективный. Это может быть полезно при
  умеренной нагрузке, когда самые мощные ядра нужно оставить приложению или компоненту безопасности.
  Некоторые современные CPU имеют много таких энергоэффективных ядер, которые вместе обеспечивают
  приемлемую производительность при меньшем энергопотреблении.

- first-usable-node: если набор CPU ранее не был ограничен при запуске, например утилитой "taskset",
  и директива "nbthread" не задана, используется первый узел NUMA с включёнными CPU. Число этих CPU
  принимается за число потоков. Для всех них включается одна группа потоков с ограничением в 32
  или 64 в зависимости от системы.

- group-by-2-ccx: работает так же, как описанная ниже "group-by-ccx", но создаёт одну группу на каждые два
  CCX. Это может быть полезно для CPU с большим числом CCX, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между CCX производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-2-clusters: работает так же, как описанная "group-by-cluster", но создаёт одну группу на каждые два
  кластера. Это может быть полезно для CPU с большим числом кластеров, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между кластерами производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-3-ccx: работает так же, как описанная ниже "group-by-ccx", но создаёт одну группу на каждые три
  CCX. Это может быть полезно для CPU с большим числом CCX, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между CCX производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-3-clusters: работает так же, как описанная "group-by-cluster", но создаёт одну группу на каждые три
  кластера. Это может быть полезно для CPU с большим числом кластеров, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между кластерами производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-4-ccx: работает так же, как описанная ниже "group-by-ccx", но создаёт одну группу на каждые четыре
  CCX. Это может быть полезно для CPU с большим числом CCX, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между CCX производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-4-clusters: работает так же, как описанная "group-by-cluster", но создаёт одну группу на каждые четыре
  кластера. Это может быть полезно для CPU с большим числом кластеров, в каждом из которых мало ядер,
  чтобы не создавать слишком много групп или немного выровнять распределение, когда используются
  не все ядра. Обратите внимание: при медленном обмене между кластерами производительность может
  существенно ухудшиться. Обычно эту политику использовать не рекомендуется.

- group-by-ccx: если не заданы ни "nbthread", ни "nbtgroups", для каждого комплекса ядер CPU
  ("CCX") с доступными CPU создаётся одна группа потоков с числом потоков, равным числу CPU. CCX
  объединяет CPU с одинаково быстрым доступом к кэшу последнего уровня ("LLC"), обычно к L3.
  В большинстве современных систем для производительности критически важно не объединять CPU из
  удалённых CCX в одну группу потоков. Все потоки группы привязываются ко всем CPU этого CCX,
  чтобы обмен внутри группы оставался локальным для CCX без чрезмерно жёсткой привязки.
  Соблюдаются ограничения на число потоков в группе и на число групп потоков. Эта политика
  рекомендуется для многосокетных систем и систем NUMA, а также для CPU с большими задержками
  обмена между CCX.

- group-by-cluster: если не заданы ни "nbthread", ни "nbtgroups", для каждого кластера CPU с
  доступными CPU создаётся одна группа потоков с числом потоков, равным числу CPU. Все потоки
  группы привязываются ко всем CPU кластера, чтобы обмен внутри группы оставался локальным для
  кластера без чрезмерно жёсткой привязки. Соблюдаются ограничения на число потоков в группе
  и на число групп потоков. Эта политика рекомендуется для многосокетных систем и систем NUMA,
  а также для CPU с большими задержками обмена между CCX. В большинстве серверных систем
  кластеры и CCX совпадают, но в неоднородных системах ("performance" и "efficiency" либо "big"
  и "little") кластер обычно включает лишь часть CCX с очень похожими CPU: одного типа и
  с разницей частот не более +/-5%. Это различие заметно на современных ноутбуках и настольных
  компьютерах, на которых разработчики и администраторы проверяют конфигурации.

- performance: работает так же, как описанная выше "group-by-ccx", но исключает кластеры CPU из
  ядер, производительность которых составляет менее 80% от производительности следующего, более
  производительного типа. Обычно это ядра "little" или "efficient": их добавление, как правило,
  не даёт существенного выигрыша и легко может ухудшить результат, например при рукопожатиях TLS.
  Часто гораздо эффективнее оставить такие ядра для других задач, например обработки сети.
  В системах разработки на них также можно запускать вспомогательные средства, например
  генераторы нагрузки и средства мониторинга. Это политика по умолчанию.

- resource: работает так же, как описанная выше "group-by-cluster", но использует только самый
  маленький и энергоэффективный кластер CPU, игнорируя все остальные. Это позволяет ограничить
  использование ресурсов необходимым минимумом, при котором ещё сохраняется приемлемая
  производительность. Например, можно дополнительно снизить энергопотребление или сократить
  число ядер для вспомогательного процесса sidecar в арендованной системе, чтобы было проще
  уменьшить выделенные ей ресурсы. Обратите внимание: если кластер всего один, он всё равно используется целиком.

Можно добавить необязательное ключевое слово "threads-per-core". Оно принимает значения "1" и "auto". При значении 1 создаётся только один поток на ядро независимо от числа аппаратных потоков этого ядра. При значении auto создаётся по одному потоку на каждый аппаратный поток. Если привязка явно не задана и используется threads-per-core 1, по умолчанию применяется привязка per-core.

См. также: "cpu-map", "cpu-set", "nbthread"

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

Позволяет символически описать наборы CPU для выполнения. Директива поддерживает следующие ключевые слова: - reset отменяет все прежние ограничения, которые могли быть унаследованы, например, от диспетчера служб или команды "taskset". - drop-cpu `<set>` не привязывает к CPU из этого набора - only-cpu `<set>` не привязывает к CPU вне этого набора - drop-node `<set>` не привязывает к CPU этого узла NUMA - only-node `<set>` не привязывает к CPU других узлов NUMA - drop-cluster `<set>` не привязывает к CPU аппаратного кластера с этим номером - only-cluster `<set>` не привязывает к CPU аппаратных кластеров с другими номерами - drop-core `<set>` не привязывает к CPU аппаратного ядра с этим номером - only-core `<set>` не привязывает к CPU аппаратных ядер с другими номерами - drop-thread `<set>` не привязывает к CPU аппаратного потока с этим номером - only-thread `<set>` не привязывает к CPU аппаратных потоков с другими номерами См. также: "cpu-policy"

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

Задаёт каталог по умолчанию для загрузки сертификатов SSL, когда в директивах "crtfile" или "crt" используется относительный путь. Заданные абсолютные пути имеют приоритет; "crt-base" в этом случае игнорируется.

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

Переводит процесс в фоновый режим через fork. Это рекомендуемый режим работы. Он эквивалентен аргументу командной строки "-D" и может быть отключён аргументом "-db". В режиме systemd этот параметр игнорируется.

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

По умолчанию HAProxy загружает все файлы с относительными путями из каталога, в котором был запущен процесс. В некоторых случаях желательно принудительно отсчитывать относительные пути от другого каталога, как если бы процесс был запущен из него. Для этого и предназначена эта директива. Технически она временно выполняет chdir() в указанный каталог при обработке каждого конфигурационного файла и возвращается в исходный каталог после обработки каждого файла. Аргумент задаёт политику загрузки файлов, путь к которым не начинается с косой черты ('/'): - "current" означает, что все файлы с относительными путями загружаются из каталога запуска процесса; это значение по умолчанию.

    - "config" означает, что все файлы с относительными путями следует загружать из каталога конфигурационного файла. Точнее, если путь к конфигурационному файлу содержит косую черту ('/'), для перехода используется вся часть пути до последней косой черты; иначе используется текущий каталог. Этот режим удобен для объединения таблиц соответствий, файлов ошибок, сертификатов и сценариев Lua в перемещаемые пакеты. При загрузке нескольких конфигурационных файлов каталог обновляется для каждого из них.

    - "parent" означает, что все файлы с относительными путями следует загружать из родительского каталога по отношению к каталогу конфигурационного файла. Точнее, если путь к конфигурационному файлу содержит косую черту ('/'), к части пути до последней косой черты добавляется ".."; полученный путь используется для перехода. В противном случае используется каталог "..". Этот режим удобен для объединения таблиц соответствий, файлов ошибок, сертификатов и сценариев Lua в перемещаемые пакеты, где каждая часть находится в своём подкаталоге, например "config/", "certs/", "maps/" и т. д.

    - "origin" означает, что все файлы с относительными путями следует загружать из каталога, путь к которому обязательно должен быть указан. Это упрощает управление несколькими экземплярами HAProxy, работающими параллельно в одной системе: у каждого экземпляра может быть собственный префикс, а остальные секции остаются легко перемещаемыми.

Каждая директива "default-path" немедленно заменяет предыдущую и может привести к переходу в другой каталог. Хотя это должно давать ожидаемый результат, использовать несколько директив default-path не рекомендуется. Если они всё же используются, следует придерживаться согласованной политики во всех конфигурационных файлах.

Предупреждение: некоторые элементы конфигурации, например таблицы соответствий или сертификаты, однозначно определяются заданным для них путём. При использовании перемещаемой структуры несколько элементов могут получить одно и то же уникальное имя, что затруднит их обновление во время работы, особенно если несколько конфигурационных файлов загружаются из разных каталогов. Перед переходом на относительные пути необходимо строго придерживаться схемы именования файлов без коллизий. Надёжным решением может быть добавление к именам всех файлов префикса с именем соответствующего сайта либо применение такого префикса на уровне каталогов.

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

Добавляет текст с описанием экземпляра.

Обратите внимание: некоторые символы, например #, необходимо экранировать. Поскольку этот текст вставляется в страницу HTML, следует избегать символов "\<" и "\>".

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

Задаёт путь к файлу данных DeviceAtlas в формате JSON, который загружает API. Путь должен указывать на корректный файл данных JSON, доступный процессу HAProxy.

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

Задаёт уровень информации, возвращаемой API. Директива необязательна; если она не задана, по умолчанию используется 0.

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

Задаёт имя клиентского cookie, используемого для определения устройства, если при запросе применялся клиентский компонент DeviceAtlas. Директива необязательна; если она не задана, по умолчанию используется DAPROPS.

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

Задаёт символ-разделитель для результатов свойств API. Директива необязательна; если она не задана, по умолчанию используется \|.

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

По умолчанию резолверы DNS принимают адреса IPv4 и IPv6. На выбор можно влиять ключевым словом "resolve-prefer" в строках server и аргументом семейства в действии "do-resolve", однако это только предпочтение: оно не запрещает использовать другое семейство, если доступно только оно. В средах, где невозможно использовать оба стека, недоступная запись DNS только с адресом IPv6 может вызвать серьёзные проблемы: она заменит прежнюю запись IPv4, которая, возможно, продолжала бы работать до следующего запроса. Глобальный параметр "dns-accept-family" позволяет принудительно использовать только одно семейство адресов или оба. Аргумент — список следующих слов через запятую: - "ipv4": запрашивать и принимать адреса IPv4 (записи "A") - "ipv6": запрашивать и принимать адреса IPv6 (записи "AAAA") - "auto": использовать IPv4, а также IPv6, если в системе для него есть шлюз по умолчанию. Результат последней проверки кэшируется на 30 секунд.

Если используется одно семейство, запросы к резолверам для другого семейства не отправляются, а любые ответы для него игнорируются. Начиная с 3.3 значение по умолчанию — "auto": оба семейства включаются только после подтверждения возможности маршрутизации IPv6; иначе используется только IPv4. См. также: "resolve-prefer", "do-resolve"

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

Эта директива должна находиться перед использованием некоторых директив, помеченных как устаревшие, чтобы отключить предупреждения и предотвратить отклонение конфигурационного файла. Это касается не всех устаревших директив, а только тех, для которых нет альтернативного решения.

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

Эта директива должна находиться перед использованием директив, помеченных как экспериментальные; иначе конфигурационный файл будет отклонён. Обратите внимание: для возможностей, на которые распространяется этот параметр, корректная работа не гарантируется; они могут перестать работать в течение цикла сопровождения. Пока разрабатывается следующая версия, разработчики будут поддерживать их по мере возможностей и прилагать разумные усилия, чтобы не нарушить их работу, но без гарантий. Поэтому поддержка этих возможностей после выхода следующего выпуска LTS не предполагается. Пользователям экспериментальных возможностей следует оперативно обновляться, чтобы получать внесённые улучшения. Определить, нужна ли ещё эта директива, просто: если она включена, но ни одна такая возможность её не использует, выводится предупреждение с предложением отключить её. Если предупреждения нет, директива всё ещё нужна.

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

Разрешает использовать внешний агент для проверок работоспособности. По соображениям безопасности по умолчанию это отключено. Даже после включения проверки могут завершаться неудачей, если также не включён "insecure-fork-wanted". Если запускаемая программа использует исполняемый файл с setuid, чего ей действительно не следует делать, в секции global может также потребоваться "insecure-setuid-wanted". По умолчанию проверки запускаются с чистым окружением, содержащим только переменные, определённые командой "external-check" в секции backend. Иногда желательно сохранить окружение, например если сложные сценарии получают из него дополнительные пути или сведения. Для этого можно добавить ключевое слово "preserve-env". Однако в таком случае настоятельно рекомендуется не запускать программу с setuid или от привилегированного пользователя, поскольку это открывает возможности для атак на программу проверки. Подробности см. в "option external-check", "insecure-fork-wanted" и "insecure-setuid-wanted".

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

Задаёт верхнюю границу числа файловых дескрипторов, используемых процессом, независимо от системных лимитов. Значение можно принудительно задать через "ulimit-n" и "maxconn"; если они не заданы, процесс ограничивается жёстким лимитом RLIMIT_NOFILE, который показывает "ulimit -n -H". Однако некоторые современные ОС допускают здесь чрезвычайно большие значения, порядка 1 миллиарда, что при обычной работе потребовало бы слишком много RAM. Параметр fd-hard-limit позволяет установить для этого лимита, возможно, более низкую верхнюю границу. Если системные лимиты ниже `<number>`, они всегда соблюдаются; если выше, используется заданное значение. По умолчанию fd-hard-limit равен 1048576. Это значение можно изменить переменной времени компиляции DEFAULT_MAXFD, которая может служить максимальным системным лимитом ядра при чрезмерно большом жёстком лимите RLIMIT_NOFILE. Параметр fd-hard-limit в секции global позволяет временно переопределить значение DEFAULT_MAXFD, заданное при сборке. В следующем примере другие параметры не заданы, и maxconn автоматически подстраивается под меньшее из значений "fd-hard-limit" и лимита RLIMIT_NOFILE:

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

См. также: ulimit-n, maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

Меняет идентификатор группы процесса на `<number>`. Рекомендуется выделить эту группу для HAProxy или небольшого набора схожих демонов. HAProxy должен запускаться от пользователя, входящего в эту группу, либо с правами суперпользователя. Обратите внимание: если пользователь запуска имеет дополнительные группы, HAProxy сможет отказаться от них только при запуске с правами суперпользователя. См. также "group" и "uid".

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

Задаёт задержку между SIGUSR1 и фактической плавной остановкой.

Аргументы:

```text
<time>  — дополнительная задержка (по умолчанию в миллисекундах) после
        получения сигнала SIGUSR1, которую нужно выждать перед переходом
        к мягкой остановке.
```

Используется для совместимости с устаревшими средами, где процесс haproxy нужно остановить, но внешние компоненты должны обнаружить его состояние до освобождения слушающих сокетов. Внутренняя переменная "stopping", которую возвращает одноимённая функция извлечения образца "stopping", переключается в true. При этом слушающие сокеты продолжают принимать соединения без изменений до истечения задержки, после чего начинается обычная плавная остановка. Это нельзя использовать для процессов, конфигурация которых перезагружается: старый процесс не сможет освободить сокеты, что может помешать запуску нового или вызвать другие проблемы.

Пример:

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

Обратите внимание: более гибкий и устойчивый подход — чтобы система оркестрации задавала глобальную переменную через CLI, использовала её при ответах на внешние проверки, а затем после задержки отправляла сигнал SIGUSR1.

Пример:

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

См. также: hard-stop-after, monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

Аналогичен "gid", но использует GID группы с именем `<group name>` из /etc/group. См. также "gid" и "user".

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

Не отклоняет запросы HTTP/1.0 GET/HEAD/DELETE с полезной нагрузкой ответом HTTP 413 Payload Too Large.

Хотя HTTP/1.1 явно разрешает такую полезную нагрузку, HTTP/1.0 не даёт однозначного ответа, и некоторые старые серверы не ожидают её и вообще не проверяют длину тела по заголовкам Content-Length или Transfer-Encoding. Поэтому одни промежуточные узлы могут правильно обработать полезную нагрузку запросов HTTP/1.0 GET/HEAD/DELETE, а другие — полностью её проигнорировать. Это создаёт риск для безопасности, поскольку возможна атака с подменой границ запросов. Поэтому по умолчанию HAProxy отклоняет запросы HTTP/1.0 GET/HEAD/DELETE с полезной нагрузкой.

Однако это может создавать проблемы для некоторых старых клиентов. В таком случае можно задать этот глобальный параметр.

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

Если где-либо в цепочке до или после узла есть агент HTTP/1.0, одновременное наличие полей Transfer-Encoding и Content-Length в одном сообщении создаёт серьёзный риск атаки с подменой границ содержимого. Согласно спецификации HTTP/1.1 (RFC9112#6.1), в такой ситуации агент обязан закрыть соединение после ответа, чтобы исключить эксплуатацию этой уязвимости. Однако это может снизить производительность некоторых очень старых клиентов, особенно если им приходится заново согласовывать соединение TLS для каждого запроса. Этот параметр позволяет попросить HAProxy не применять такое правило: сообщение очищается, но соединение остаётся открытым после ответа. Это допустимо только при полной уверенности, что в цепочке нет агентов HTTP/1.0 и все реализации перед HAProxy полностью соблюдают правила HTTP/1.1 для этих полей заголовков. В любом случае HAProxy продолжает игнорировать и удалять лишний заголовок Content-Length, чтобы не вводить следующий узел в заблуждение.

При включении этого параметра для обхода ошибки старого клиента или сервера важно понимать: независимо от того, нужен ли этот параметр, сообщения такого агента, нарушающего правило, могут быть усечены старыми агентами, которые учитывают Content-Length и игнорируют Transfer-Encoding. Причина в том, что не учитывается общий объём данных, которыми закодированы размеры блоков. Поэтому приведённое выше правило касается не только безопасности, но и отказа от агентов, у которых могут возникать проблемы обмена из-за несовместимости со старыми реализациями.

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

Задаёт преобразование регистра имени заголовка `<from>` в `<to>` перед отправкой клиентам или серверам HTTP/1, если такое преобразование включено. `<from>` должен быть в нижнем регистре, а `<from>` и `<to>` должны различаться только регистром. Если нужно изменить несколько имён заголовков, директиву можно повторять. Дубликаты запрещены. Если имён много, удобнее может быть "h1-case-adjust-file". Обратите внимание: преобразование не применяется, пока для прокси не задано "option h1-case-adjust-bogus-client" или "option h1-case-adjust-bogus-server".

Стандартного регистра имён заголовков нет: как указано в RFC7230, они нечувствительны к регистру. Поэтому приложения должны обрабатывать их без учёта регистра. Однако некоторые некорректные приложения нарушают стандарты и ошибочно полагаются на регистр, который чаще всего используют браузеры. Для HTTP/2 эта проблема критична, поскольку все имена заголовков должны передаваться в нижнем регистре; HAProxy следует тому же правилу. Все имена заголовков отправляются клиентам и серверам в нижнем регистре независимо от версии HTTP.

Для приложений, которые неправильно обрабатывают запросы или ответы, могут временно потребоваться такие обходные меры, меняющие регистр отправляемых им имён заголовков, пока приложение не будет исправлено. Обратите внимание: приложение, которому нужны такие обходные меры, может быть уязвимо к атакам с подменой границ содержимого и обязательно должно быть исправлено.

Пример:

```text
global
  h1-case-adjust content-length Content-Length
```

См. "h1-case-adjust-file", "option h1-case-adjust-bogus-client" и "option h1-case-adjust-bogus-server".

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

Задаёт файл со списком пар ключ/значение для изменения регистра некоторых имён заголовков перед отправкой клиентам или серверам HTTP/1. В файле `<hdrs-file>` каждая строка должна содержать 2 имени заголовка. Первое должно быть в нижнем регистре, а оба имени должны различаться только регистром. Строки, начинающиеся с '#', игнорируются, как и пустые строки. Начальные и конечные табуляции и пробелы удаляются. Дубликаты запрещены. Обратите внимание: преобразование не применяется, пока для прокси не задано "option h1-case-adjust-bogus-client" или "option h1-case-adjust-bogus-server".

Если директива повторяется, обрабатывается только последняя. Она служит альтернативой "h1-case-adjust", когда нужно изменить регистр многих имён заголовков. Прочитайте описание рисков, связанных с её использованием.

См. "h1-case-adjust", "option h1-case-adjust-bogus-client" и "option h1-case-adjust-bogus-server".

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

Отключает объявление клиентам о поддержке WebSocket по h2. Это позволяет обойти проблемы клиентов с реализацией относительно нового RFC8441, например Firefox
88. Чтобы клиенты могли автоматически перейти на http/1.1 для туннеля WebSocket, задайте поддержку h2 в строке bind с помощью "alpn" без явного ключевого слова "proto". Если эта директива была включена ранее, её можно отключить, добавив перед ключевым словом "no".

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

Задаёт максимальное время, отведённое на корректную плавную остановку.

Аргументы:

```text
<time>  — максимальное время (по умолчанию в миллисекундах), в течение
        которого экземпляр продолжит работу после получения запроса
        мягкой остановки через сигнал SIGUSR1.
```

Позволяет гарантировать завершение экземпляра, даже если во время плавной остановки остаются открытые соединения, например при больших тайм-аутах прокси в режиме tcp. Применяется в режимах TCP и HTTP.

Пример:

```text
global
  hard-stop-after 30s
```

См. также: grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

Включает или отключает для каждого протокола защиту, запрещающую обмен с клиентами, которые используют привилегированные порты в качестве порта источника. Диапазон этих портов определён в RFC 6335. По умолчанию защита включена для QUIC, поскольку такое поведение подозрительно и может применяться для подмены источника или атак с усилением DNS/NTP.

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

Заменяет, сокращает или расширяет список кодов состояния, считающихся ошибкой для кодов завершения и счётчика "http_err_cnt" в таблицах привязок. По умолчанию ошибками считаются коды от 400 до 499. Однако некоторые пользователи предпочитают исключать отдельные коды в определённых условиях, особенно при учёте ошибок клиентов, например 404 в системах с динамически создаваемым содержимым. См. также "http-fail-codes" и "http_err_cnt".

Диапазон без '+' или '-' заменяет существующий диапазон новым. Диапазон с начальным '+' добавляется к существующему независимо от того, пересекаются они или нет. Диапазон с начальным '-' удаляется из существующего. Диапазон задаётся числом от 100 до 599, после которого можно указать "-" и ещё одно число, не меньше первого, как верхнюю границу. Для одной операции добавления, удаления или замены можно указать несколько диапазонов через запятую.

Пример:

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

Заменяет, сокращает или расширяет список кодов состояния, считающихся сбоем для кодов завершения и счётчика "http_fail_cnt" в таблицах привязок. По умолчанию это коды от 500 до 599, кроме 501 и 505, которые могут быть вызваны клиентами. Обычно коды сбоев указывают на неспособность сервера обработать запрос. Некоторые пользователи предпочитают исключать коды в тех условиях, где известно, что они не относятся к сбоям, например 500 в некоторых средах SOAP, где этот код не означает ошибку сервера. Синтаксис точно такой же, как у описанного выше http-err-codes. См. также "http-err-codes" и "http_fail_cnt".

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

По умолчанию HAProxy старается предотвратить любое создание потоков и процессов после запуска. Это особенно важно при использовании файлов Lua неизвестного происхождения и при работе с разрабатываемыми версиями, в которых ещё могут быть ошибки с неясными возможностями эксплуатации. В целом полезно гарантировать, что трафик не сможет вызвать непредвиденную фоновую активность. Однако эта защита мешает работе внешних проверок и может нарушать работу некоторых специфических сценариев Lua, которым необходим fork. Этот параметр отключает защиту. Обратите внимание: отключать её нежелательно, поскольку тогда уязвимость в библиотеке или самом HAProxy будет легче эксплуатировать. Кроме того, fork из Lua или любого другого места ненадёжен: дочерний процесс может случайно унаследовать блокировку, установленную другим потоком, и никогда не завершить операцию. Поэтому настоятельно рекомендуется никогда не использовать этот параметр, а задачи, требующие fork, пересмотреть и перенести на более безопасное решение, например использовать агентов вместо внешних проверок. Параметр поддерживает префикс "no" для отключения. Его также можно включить аргументом "-dI" в командной строке haproxy.

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

HAProxy не требуется запускать исполняемые файлы во время работы, кроме внешних проверок, от которых настоятельно рекомендуется отказаться. Более того, предполагается его изоляция в пустом chroot. Поэтому практически нет обоснованной причины разрешать запуск исполняемого файла с setuid без полного понимания пользователем рисков. Если HAProxy требуется вызывать внешние проверки или отключить chroot, эксплуатация уязвимости в библиотеке или самом HAProxy может привести к запуску внешней программы. В Linux процесс можно ограничить так, чтобы бит setuid любого такого исполняемого файла игнорировался. Это существенно снижает риск повышения привилегий; именно так HAProxy действует по умолчанию. Если это мешает внешней проверке, например использующей команду "ping", защиту можно отключить, явно добавив эту директиву в секцию global. Если директива включена, её можно снова отключить, добавив перед ней ключевое слово "no".

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

Задаёт каталог для загрузки цепочек сертификатов, используемых при достраивании цепочки издателя. Все файлы должны быть в формате PEM. Если для сертификата, загруженного через "crt" или "crt-list", цепочка сертификатов не включена в PEM, HAProxy достроит её, когда издатель сертификата соответствует первому сертификату цепочки, загруженной через "issuers-chain-path". Такие сертификаты цепочки также обычно называют промежуточными. Файл "crt" с PrivateKey+Certificate+IntermediateCA2+IntermediateCA1 можно заменить файлом с PrivateKey+Certificate. HAProxy достроит цепочку, если в каталоге "issuers-chain-path" есть файл с IntermediateCA2+IntermediateCA1. Все остальные сертификаты с тем же издателем будут совместно использовать эту цепочку в памяти.

Возможности OCSP могут использовать достроенную цепочку, если .issuer не использовался или цепочка не была предоставлена в PEM.

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

Разрешает JWT-токены с алгоритмом "none" в преобразователе 'jwt_verify'. При включении этой опции такие токены всегда считаются действительными. По умолчанию неподписанные токены отклоняются как небезопасные (см. RFC8725 [раздел 3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)).

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

Задаёт список алгоритмов, разрешённых в преобразователях jwt_decrypt_XXX. Токены JWT с неподдерживаемыми или отключёнными алгоритмами никогда не расшифровываются. Алгоритмы должны быть указаны в формате из [раздела 4.1](https://www.rfc-editor.org/rfc/rfc7518#section-4.1) RFC7518 и разделены двоеточиями. Специальное имя "ALL" включает все поддерживаемые алгоритмы; полный список см. в описании преобразователя "jwt_decrypt_jwk". К имени алгоритма можно добавить '!', чтобы явно отключить его. Обратите внимание: если "ALL" не указан, этот параметр отключает все алгоритмы, которые не перечислены явно.

Примеры:

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

Задаёт список алгоритмов шифрования, разрешённых в преобразователях jwt_decrypt_XXX. Токены JWT с неподдерживаемыми или отключёнными алгоритмами шифрования никогда не расшифровываются. Алгоритмы должны быть указаны в формате из [раздела 5.1](https://www.rfc-editor.org/rfc/rfc7518#section-5.1) RFC7518 и разделены двоеточиями. Специальное имя "ALL" включает все поддерживаемые алгоритмы; полный список см. в описании преобразователя "jwt_decrypt_jwk". К имени алгоритма можно добавить '!', чтобы явно отключить его. Обратите внимание: если "ALL" не указан, этот параметр отключает все алгоритмы, которые не перечислены явно.

Примеры:

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

Задаёт каталог по умолчанию для загрузки закрытых ключей SSL, когда в директивах "key" используется относительный путь. Заданные абсолютные пути имеют приоритет; "key-base" в этом случае игнорируется. Этот параметр работает только со строкой load в crt-store.

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

Этот параметр необходимо использовать для явного включения слушающих сокетов QUIC, если haproxy собран с версией OpenSSL без поддержки QUIC. Он активирует внутренний слой совместимости haproxy, который должен быть выбран при сборке с помощью USE_QUIC_OPENSSL_COMPAT=1. Этот слой поддерживает большинство необходимых операций TLS, но не поддерживает QUIC 0-RTT.

Эта возможность предназначена прежде всего для OpenSSL до версии 3.5.2, где API QUIC отсутствовал или был реализован лишь частично. Слой совместимости можно включить и для версии 3.5.2 или новее, но, вероятно, это не требуется.

Если limited-quic задан, но слой совместимости не был выбран при сборке, параметр игнорируется без сообщения, а операции QUIC TLS выполняются средствами библиотеки TLS.

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

Задаёт имя локального экземпляра среди узлов peers. Оно игнорируется, если указан аргумент командной строки "-L" или директива использована после определений секций "peers". В таких случаях при разборе конфигурации выводится предупреждение.

Этот параметр также задаёт переменную окружения HAPROXY_LOCALPEER. См. также "-L" в руководстве по управлению и секцию "peers" ниже.

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

Добавляет глобальный сервер syslog. Можно задать несколько таких серверов. Они получают записи о запуске и завершении, а также все журналы прокси, настроенных с "log global". Подробности см. в описании параметра "log" для прокси.

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

Задаёт поле имени хоста в заголовке syslog. Если указан необязательный параметр "string", полю присваивается содержимое этой строки; иначе используется имя хоста системы. Обычно это нужно, если журналы не пересылаются через промежуточный сервер syslog, либо для изменения имени хоста, выводимого в журнале.

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

Задаёт этой строкой поле тега в заголовке syslog. По умолчанию используется имя программы при запуске из командной строки, обычно "haproxy". Иногда это полезно для различения нескольких процессов на одном хосте. См. также директиву "log-tag" для отдельных прокси.

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Эта глобальная директива загружает и выполняет файл Lua в общем контексте, видимом всем потокам. Любая переменная, заданная в таком контексте, видна из любого потока. Это самый простой и рекомендуемый способ загрузки программ Lua, но при большом числе вызовов Lua он плохо масштабируется: с глобальным состоянием одновременно может работать только один поток. Программа, загруженная таким способом, всегда видит 0 в переменной "core.thread". Директиву можно использовать несколько раз.

Аргументы args доступны в файле Lua через приведённый ниже код в теле файла. Не забывайте, что индексы массивов Lua начинаются с 1. Переменная "local", объявленная в файле, доступна во всём этом файле и недоступна в других файлах.

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

Эта глобальная директива загружает и выполняет файл Lua в каждом запущенном потоке. Глобальные переменные видимы только внутри потока, поэтому каждый поток может видеть своё значение. В программах, загруженных таким способом, настоятельно рекомендуется не использовать глобальные переменные. Для каждого потока загружается и инициализируется отдельная копия; всё выполняется последовательно, по возрастанию номеров потоков от 1 до nbthread. Если какие-то операции нужно выполнить только один раз, программе следует проверить переменную "core.thread", чтобы определить, какой поток инициализируется. Загруженные таким способом программы выполняются параллельно во всех потоках и хорошо масштабируются. Это рекомендуемый способ загрузки простых функций, регистрирующих методы извлечения образцов, преобразователи, действия или службы, когда точно известно, что программа не зависит от глобальных переменных. Для простоты директива доступна и при использовании одного потока, и даже при отключённой поддержке потоков; в последнем случае она эквивалентна lua-load. Директиву можно использовать несколько раз.

Об использовании args см. lua-load.

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

Добавляет указанную строку с последующей точкой с запятой в начало переменной Lua package.`<type>`. `<type>` должен быть "path" или "cpath". Если `<type>` не задан, по умолчанию используется "path".

Пути Lua — списки шаблонов, разделённых точкой с запятой. Они определяют, как функция `require` пытается найти исходный файл библиотеки. Знаки вопроса (?) в шаблоне заменяются именем модуля. Путь проверяется слева направо, поэтому пути, добавленные в начало позже, проверяются раньше.

Например, если указать следующий путь:

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

При вызове `require "example"` Lua сначала пытается загрузить /usr/share/haproxy-lua/example.lua как сценарий. Если его нет, проверяется /usr/share/haproxy-lua/example/init.lua, а если нет и этого файла — пути по умолчанию.

Подробности см. в документации Lua: <https://www.lua.org/pil/8.1.html>.

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

Режим master-worker. Эквивалентен аргументу командной строки "-W".

Это ключевое слово устарело; для запуска в режиме master-worker используйте "-W" или "-Ws".

В этом режиме запускается главный процесс "master", который после чтения конфигурации создаёт через fork рабочий процесс "worker" для обработки трафика. Главный процесс выполняет роль диспетчера процессов, следящего за рабочими процессами "workers".

В этом режиме HAProxy можно перезагрузить напрямую, отправив главному процессу сигнал SIGUSR2. При перезагрузке главный процесс повторно читает конфигурацию и создаёт через fork новый рабочий процесс. Прежний рабочий процесс остаётся до завершения своих задач.

Режим master-worker совместим как с работой на переднем плане, так и с режимом демона.

По умолчанию, если рабочий процесс завершается с кодом ошибки, например из-за ошибки сегментации, все рабочие процессы принудительно завершаются, а главный процесс выходит. Это удобно сочетать с Restart=on-failure в файле модуля systemd для повторного запуска всех процессов. Чтобы отключить такое поведение, необходимо использовать ключевое слово "no-exit-on-failure".

См. также "-W" в руководстве по управлению.

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

В режиме master-worker по умолчанию, если рабочий процесс завершается с кодом ошибки, например из-за ошибки сегментации, все рабочие процессы принудительно завершаются, а главный процесс выходит. Это удобно сочетать с Restart=on-failure в файле модуля systemd для повторного запуска всех процессов.

Это ключевое слово позволяет оставить остальные процессы работающими после аварийного завершения рабочего процесса, вместо того чтобы завершать их все. Использовать его нужно осторожно: оно предназначено только для отладки и может привести главный процесс в нештатное состояние.

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

Задаёт максимальное число потоков в группе. Если число групп потоков не зафиксировано директивой "thread-groups", haproxy создаёт столько групп, сколько нужно для запрошенного числа потоков. Минимальное значение — 1, максимальное — 64 в 64-битных системах или 32 в 32-битных. Меньшие значения снижают конкуренцию за общее состояние при атомарных операциях, но могут увеличить число сокетов, необходимых для всех слушателей и для хранения простаивающих соединений с бэкендами. Большие значения уменьшают эти затраты, но увеличивают использование CPU при конкуренции за ресурсы и снижают скорость установления соединений. Значение по умолчанию — 16: это лучший компромисс, выявленный экспериментально на разных системах, включая процессоры x86_64 нескольких производителей и большие системы Arm64, как на физическом оборудовании, так и под гипервизорами.

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

В режиме master-worker этот параметр ограничивает число перезагрузок, которые может пережить рабочий процесс. Если после перезагрузки он не завершился и число пережитых перезагрузок превысило указанное значение, процесс получает SIGTERM. Это помогает контролировать число рабочих процессов. См. также "show proc" в руководстве по управлению.

По умолчанию это значение равно 50.

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

Этот параметр доступен только при сборке с поддержкой потоков. Он запускает HAProxy с `<number>` потоками. "nbthread" работает и при запуске HAProxy на переднем плане. На некоторых платформах с поддержкой привязки к CPU значение "nbthread" по умолчанию автоматически принимается равным числу CPU, к которым процесс привязан при запуске. Поэтому число потоков можно легко регулировать из вызывающего процесса командами вроде "taskset" или "cpuset". В остальных случаях по умолчанию используется 1. Значение по умолчанию показывается в выводе "haproxy -vv". Обратите внимание: заданные здесь или автоматически определённые значения ограничиваются параметром "thread-hard-limit", если он задан.

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

При работе на платформе с поддержкой NUMA позволяет директиве "cpu-policy" изучить топологию, выбрать оптимальный набор CPU и соответствующее число потоков. Если на конкретной архитектуре полученная привязка неоптимальна, её можно отключить записью 'no numa-cpu-mapping'. Автоматическая привязка также не применяется, если в конфигурации есть директива 'nbthread', если привязка процесса уже задана, например директивой 'cpu-map' или утилитой taskset, либо если cpu-policy задано любое другое значение. См. также "cpu-map", "cpu-policy", "cpu-set".

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

Полностью отключает ocsp-update в HAProxy. Любая конфигурация ocsp-update игнорируется. Значение по умолчанию — "off". Подробности о механизме автоматического обновления см. в описании параметра "ocsp-update".

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

Разрешает использовать прокси HTTP для обновлений OCSP. Работает только с HTTP; HTTPS не поддерживается. Этот параметр позволяет средству обновления OCSP отправлять абсолютный URI в запросе к прокси.

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

Задаёт максимальный интервал между двумя автоматическими обновлениями одного ответа OCSP. Время задаётся в секундах; по умолчанию — 3600 (1 час). Значение должно быть больше "ocsp-update.mindelay". Подробности о механизме автоматического обновления см. в описании параметра "ocsp-update".

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

Задаёт минимальный интервал между двумя автоматическими обновлениями одного ответа OCSP. Время задаётся в секундах; по умолчанию — 300 (5 минут). Особенно полезно для ответов OCSP без явно заданного срока действия. Значение должно быть меньше "ocsp-update.maxdelay". Подробности о механизме автоматического обновления см. в описании параметра "ocsp-update".

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

Задаёт режим ocsp-update по умолчанию для всех сертификатов, используемых в конфигурации. Этот глобальный параметр может быть переопределён параметром "ocsp-update" в crt-list. По умолчанию он имеет значение "off". Подробности о механизме автоматического обновления см. в описании параметра "ocsp-update".

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

Записывает идентификаторы всех демонов в файл `<pidfile>` в режиме демона либо PID главного процесса в файл `<pidfile>` в режиме master-worker. Эквивалентен аргументу командной строки "-p". Файл должен быть доступен пользователю, запускающему процесс. См. также "daemon" и "master-worker".

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

В реализации протокола PROXY v2 в HAProxy вплоть до версии 2.1 была ошибка: для проверок работоспособности отправлялась команда PROXY вместо LOCAL. Это малозначительное отклонение, но оно вносит путаницу в журналы некоторых серверов. К сожалению, ошибку обнаружили очень поздно. Выяснилось, что некоторые серверы, возможно проверявшие свою реализацию протокола PROXY только с HAProxy, неправильно обрабатывают команду LOCAL и при проверках HAProxy постоянно остаются в состоянии "down". В этом случае можно включить глобальный параметр, возвращающий прежнее ошибочное поведение, на время обращения к поставщикам затронутых компонентов и получения исправлений. По умолчанию параметр отключён и действует на все серверы с директивой "send-proxy-v2".

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

Задаёт переменной окружения `<name>` значение `<value>`. Если переменная уже существует, она не перезаписывается. Изменения вступают в силу немедленно: следующая строка конфигурационного файла уже видит новое значение. См. также "setenv", "resetenv" и "unsetenv".

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

Однократно открывает максимальный файловый дескриптор, вызывая предварительное выделение структур данных ядра. Это предотвращает краткие паузы, возникающие при nbthread\>1, когда HAProxy открывает файловый дескриптор и ядру требуется расширить свои структуры данных.

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

Удаляет все переменные окружения, кроме указанных в аргументе. Позволяет получить чистое управляемое окружение перед установкой новых значений через setenv или unsetenv. Обратите внимание: некоторые внутренние функции могут использовать переменные окружения, например функции работы со временем, а также OpenSSL и внешние проверки. Применять этот параметр необходимо крайне осторожно и только после полной проверки. Изменения вступают в силу немедленно: следующая строка конфигурационного файла уже видит новое окружение. См. также "setenv", "presetenv" и "unsetenv".

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

Задаёт префикс каталога, добавляемый перед именами всех файлов состояния серверов, которые не начинаются с '/'. См. также "server-state-file", "load-server-state-from-file" и "server-state-file-name".

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

Задаёт путь к файлу состояния серверов. Если путь начинается с косой черты ('/'), он считается абсолютным; иначе — относительным к каталогу "server-state-base", если он задан, либо к текущему каталогу. Перед перезагрузкой HAProxy текущее состояние серверов можно сохранить командой статистики "show servers state". Вывод этой команды должен быть записан в файл `<file>`. При запуске, до начала обработки трафика, HAProxy прочитает, загрузит и применит состояние каждого сервера, который найден в файле и присутствует в текущей рабочей конфигурации. См. также "server-state-base", "show servers state", "load-server-state-from-file" и "server-state-file-name"

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

Позволяет выбрать поведение при создании дампа памяти после аварийного завершения процесса. Доступны следующие варианты:

- on: включает создание дампов памяти на уровне процесса, если оно ранее было отключено.

- off: отключает ранее включённое создание дампов памяти.

- libs: включает создание дампов памяти со встроенной копией исполняемых файлов и библиотек, необходимых для отладки. Это может потребоваться разработчикам. В этом случае haproxy пытается загрузить в память библиотеки, от которых он зависит, и сохранить их там. Если процесс аварийно завершится, они попадут в дамп памяти, поэтому их больше не потребуется извлекать из файловой системы и не будет риска их несоответствия дампу. Для этого требуется от нескольких мегабайт до нескольких десятков мегабайт дополнительной RAM, поэтому на небольших системах этот режим лучше не использовать.

Этот параметр лучше оставить отключённым по умолчанию и включать только по запросу разработчика. По умолчанию он отключён. Без аргумента используется значение "on". Если параметр включён, его всё равно можно принудительно отключить, добавив перед ним ключевое слово "no" или задав значение "off". Он не влияет ни на производительность, ни на стабильность, но настойчиво пытается снова включить создание дампов памяти, которое могло быть отключено ограничением размера файла (ulimit -f), ограничением размера дампа (ulimit -c) или запретом создания дампа процесса после изменения его UID/GID (например, /proc/sys/fs/suid_dumpable в Linux). Создание дампов всё ещё могут ограничивать права доступа к текущему каталогу (следует проверить, из какого каталога запускается файл), права доступа к каталогу chroot (может потребоваться временно отключить директиву chroot или перенести его в отдельный каталог, доступный для записи) либо другие ограничения конкретной системы. Например, некоторые варианты Linux известны тем, что заменяют путь к файлу дампа по умолчанию путём к исполняемому файлу, которого даже нет в системе (следует проверить /proc/sys/kernel/core_pattern). Часто проблему решает простая запись "core", "core.%p" или "/var/log/core/core.%p". При включении этого параметра в ожидании повторного проявления редкой проблемы часто полезно сначала попытаться получить такой дамп, например отправив "kill -11" процессу "haproxy", и проверить, что при завершении он оставляет дамп в ожидаемом месте.

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

Задаёт переменной уровня процесса '`<var-name>`' результат вычисления выражения образца `<expr>`. Переменная '`<var-name>`' может быть только переменной уровня процесса (с префиксом 'proc.'). Работает точно так же, как действие 'set-var' в правилах TCP или HTTP, но выражение вычисляется при разборе конфигурации и переменная задаётся немедленно. В выражении разрешены только функции извлечения образцов и преобразователи, использующие внутренние данные, обычно 'int(value)' или 'str(value)'. Можно также ссылаться на ранее выделенные переменные. Затем эти переменные будут доступны для чтения и изменения из обычных наборов правил.

Пример:

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

Задаёт переменной уровня процесса '`<var-name>`' строку, полученную при вычислении формата журнала `<fmt>`. Переменная '`<var-name>`' может быть только переменной уровня процесса (с префиксом 'proc.'). Работает точно так же, как действие 'set-var-fmt' в правилах TCP или HTTP, но выражение вычисляется при разборе конфигурации и переменная задаётся немедленно. В выражении разрешены только функции извлечения образцов и преобразователи, использующие внутренние данные, обычно 'int(value)' или 'str(value)'. Можно также ссылаться на ранее выделенные переменные. Затем эти переменные будут доступны для чтения и изменения из обычных наборов правил. Подробности о синтаксисе пользовательского формата журнала см. в [разделе 8.2.6](/ru/docs/haproxy/configuration-logging/#section-8-2-6).

Пример:

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

Задаёт список полномочий, которые должны сохраняться при запуске и работе от имени пользователя без прав root (uid \> 0) либо при запуске с uid 0 (root) и последующем переходе к пользователю без прав root. По умолчанию при смене uid теряются все права, но некоторые из них часто нужны при соединении с сервером с чужого адреса во время прозрачного проксирования либо при привязке к порту ниже 1024, например при использовании "tune.quic.fe.sock-per-conn default-on". В результате такие конфигурации целиком работают с uid 0. Назначение полномочий обычно безопаснее, поскольку сохраняются только необходимые полномочия. Эта возможность зависит от ОС и включена только в Linux, если при сборке задано USE_LINUX_CAP=1. Список поддерживаемых полномочий также зависит от ОС и перечисляется в сообщении об ошибке, выводимом при передаче неверного или пустого имени полномочия. Можно передать несколько полномочий, разделённых запятыми. Из часто используемых полномочий "cap_net_raw" разрешает прозрачную привязку к чужому адресу, а "cap_net_bind_service" разрешает привязку к привилегированному порту и может использоваться QUIC. Если процесс запускается и работает от имени одного и того же пользователя без прав root, необходимые полномочия следует задать исполняемому файлу haproxy с помощью setcap вместе с этим ключевым словом. Подробнее о назначении полномочий исполняемому файлу haproxy см. в главе 13.1 о поддержке полномочий Linux в руководстве по управлению.

Пример:

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

Задаёт переменной окружения `<name>` значение `<value>`. Если переменная существует, она перезаписывается. Изменения вступают в силу немедленно: следующая строка конфигурационного файла уже видит новое значение. См. также "presetenv", "resetenv" и "unsetenv".

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

Эта директива включает использование разделяемой памяти для хранения статистических счётчиков. `<name>` передаётся как аргумент shm_open() для открытия разделяемой памяти в уникальном месте. Это также означает, что директива доступна только в системах с поддержкой shm_open(). При использовании SHM для статистики все счётчики фронтендов, бэкендов, слушателей и серверов, которые могут совместно использоваться, хранятся в SHM при условии, что для них задан GUID. При перезагрузке haproxy новый процесс пытается найти в SHM объекты, которые можно сопоставить с объектами конфигурации по GUID и типу, чтобы сохранить значения некоторых счётчиков при перезагрузке. При корректной остановке haproxy объекты SHM, напротив, освобождаются, то есть счётчики фактически сбрасываются. Для принудительного сброса можно также вручную удалить файл перед запуском нового процесса.

См. также "guid", "guid-prefix" и "shm-stats-file-max-objects"

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

Задаёт максимальное число объектов, которые разделяемая память для общих счётчиков может хранить для каждой группы потоков. Значение напрямую связано с максимальным размером разделяемой памяти и используется для предварительного отображения shm заданного размера, чтобы избежать повторного отображения во время работы. По умолчанию используется 2k, что должно подходить для большинства конфигураций без риска чрезмерного использования памяти; при необходимости значение легко изменить. При запуске haproxy выдаст ошибку, если значение слишком мало для регистрации объектов, которые должны храниться в разделяемой памяти. Параметр имеет значение только при заданном "shm-stats-file".

См. также "thread-groups"

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов шифрования (наборов шифров), согласуемых при рукопожатии SSL/TLS вплоть до TLSv1.2, для всех строк "bind", где такой список не задан явно. Формат строки определён в "man 1 ciphers" из справочных страниц OpenSSL. Справочную информацию и рекомендации см., например, в (<https://wiki.mozilla.org/Security/Server_Side_TLS>) и (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Для настройки шифров TLSv1.3 см. ключевое слово "ssl-default-bind-ciphersuites". Подробнее см. описание ключевого слова "bind".

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL и использовании OpenSSL 1.1.1 или новее для сборки HAProxy. Он задаёт строку по умолчанию со списком алгоритмов шифрования (наборов шифров), согласуемых при рукопожатии TLSv1.3, для всех строк "bind", где такой список не задан явно. Формат строки определён в разделе "ciphersuites" страницы "man 1 ciphers" из справочных страниц OpenSSL. Для настройки шифров TLSv1.2 и более ранних версий см. ключевое слово "ssl-default-bind-ciphers". Этот параметр может принимать наборы шифров TLSv1.2, однако такое поведение не документировано и не рекомендуется, поскольку оно может быть непоследовательным или ошибочным. Наборы шифров TLSv1.3 по умолчанию в OpenSSL:
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 поддерживает только 5 наборов шифров:

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

Подробнее см. описание ключевого слова "bind".

Пример:

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

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов подписи для аутентификации клиента для всех строк "bind", где такой список не задан явно. Формат строки — список алгоритмов подписи, разделённых двоеточиями. Каждый алгоритм подписи можно записать в одной из двух форм: имя схемы подписи TLS1.3 ("rsa_pss_rsae_sha256") либо алгоритм открытого ключа + алгоритм хеширования ("ECDSA+SHA256"). Список может содержать обе формы. Подробнее о формате см. SSL_CTX_set1_client_sigalgs(3). Список алгоритмов подписи также приведён в разделе [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) RFC8446 и в файле ssl/t1_lib.c в OpenSSL. Этот параметр неприменим к TLSv1.1 и более ранним версиям протокола, поскольку в них алгоритмы подписи отдельно не согласуются. Изменять этот параметр не рекомендуется, если не требуется совместимость с промежуточным сетевым устройством.

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов эллиптических кривых (набором кривых), согласуемых при рукопожатии SSL/TLS с ECDHE. Формат строки — список имён кривых, разделённых двоеточиями. Подробнее см. описание ключевого слова "bind".

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт параметры ssl-options по умолчанию, принудительно применяемые ко всем строкам "bind". Доступные параметры см. в описании ключевого слова "bind".

Пример:

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов подписи, согласуемых при рукопожатии TLSv1.2 и TLSv1.3, для всех строк "bind", где такой список не задан явно. Формат строки — список алгоритмов подписи, разделённых двоеточиями. Каждый алгоритм подписи можно записать в одной из двух форм: имя схемы подписи TLS1.3 ("rsa_pss_rsae_sha256") либо алгоритм открытого ключа + алгоритм хеширования ("ECDSA+SHA256"). Список может содержать обе формы. Подробнее о формате см. SSL_CTX_set1_sigalgs(3). Список алгоритмов подписи также приведён в разделе [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) RFC8446 и в файле ssl/t1_lib.c в OpenSSL. Этот параметр неприменим к TLSv1.1 и более ранним версиям протокола, поскольку в них алгоритмы подписи отдельно не согласуются. Изменять этот параметр не рекомендуется, если не требуется совместимость с промежуточным сетевым устройством.

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов шифрования, согласуемых при рукопожатии SSL/TLS с сервером вплоть до TLSv1.2, для всех строк "server", где такой список не задан явно. Формат строки определён в "man 1 ciphers" из справочных страниц OpenSSL. Справочную информацию и рекомендации см., например, в (<https://wiki.mozilla.org/Security/Server_Side_TLS>) и (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>). Для настройки шифров TLSv1.3 см. ключевое слово "ssl-default-server-ciphersuites". Подробнее см. описание ключевого слова "server".

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL и использовании OpenSSL 1.1.1 или новее для сборки HAProxy. Он задаёт строку по умолчанию со списком алгоритмов шифрования, согласуемых при рукопожатии TLSv1.3 с сервером, для всех строк "server", где такой список не задан явно. Формат строки определён в разделе "ciphersuites" страницы "man 1 ciphers" из справочных страниц OpenSSL. Для настройки шифров TLSv1.2 и более ранних версий см. ключевое слово "ssl-default-server-ciphers". Подробнее см. описание ключевого слова "server".

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов подписи для аутентификации клиента для всех строк "server", где такой список не задан явно. Формат строки — список алгоритмов подписи, разделённых двоеточиями. Каждый алгоритм подписи можно записать в одной из двух форм: имя схемы подписи TLS1.3 ("rsa_pss_rsae_sha256") либо алгоритм открытого ключа + алгоритм хеширования ("ECDSA+SHA256"). Список может содержать обе формы. Подробнее о формате см. SSL_CTX_set1_client_sigalgs(3). Список алгоритмов подписи также приведён в разделе [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) RFC8446 и в файле ssl/t1_lib.c в OpenSSL. Этот параметр неприменим к TLSv1.1 и более ранним версиям протокола, поскольку в них алгоритмы подписи отдельно не согласуются. Изменять этот параметр не рекомендуется, если не требуется совместимость с промежуточным сетевым устройством.

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов эллиптических кривых (набором кривых), согласуемых при рукопожатии SSL/TLS с ECDHE. Формат строки — список имён кривых, разделённых двоеточиями. Подробнее см. описание ключевого слова "server".

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт параметры ssl-options по умолчанию, принудительно применяемые ко всем строкам "server". Доступные параметры см. в описании ключевого слова "server".

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт строку по умолчанию со списком алгоритмов подписи, согласуемых при рукопожатии TLSv1.2 и TLSv1.3, для всех строк "server", где такой список не задан явно. Формат строки — список алгоритмов подписи, разделённых двоеточиями. Каждый алгоритм подписи можно записать в одной из двух форм: имя схемы подписи TLS1.3 ("rsa_pss_rsae_sha256") либо алгоритм открытого ключа + алгоритм хеширования ("ECDSA+SHA256"). Список может содержать обе формы. Подробнее о формате см. SSL_CTX_set1_sigalgs(3). Список алгоритмов подписи также приведён в разделе [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) RFC8446 и в файле ssl/t1_lib.c в OpenSSL. Этот параметр неприменим к TLSv1.1 и более ранним версиям протокола, поскольку в них алгоритмы подписи отдельно не согласуются. Изменять этот параметр не рекомендуется, если не требуется совместимость с промежуточным сетевым устройством.

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он задаёт параметры DH по умолчанию, используемые при рукопожатии SSL/TLS с обменом ключами на основе эфемерного алгоритма Диффи — Хеллмана (DHE), для всех строк "bind", где они не заданы явно. Их переопределяют пользовательские параметры DH из файла сертификата bind, если они там есть. Если пользовательские параметры DH не заданы ни с помощью ssl-dh-param-file, ни непосредственно в файле сертификата, шифры DHE не используются, если не задан tune.ssl.default-dh-param. В последнем случае используются предопределённые параметры DH указанного размера. Пользовательские параметры считаются более безопасными, поэтому рекомендуется использовать их. Пользовательские параметры DH можно создать командой OpenSSL "openssl dhparam `<size>`", где размер следует выбирать не менее 2048, поскольку 1024-битные параметры DH больше не следует считать безопасными.

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

Этот параметр доступен только при сборке с поддержкой OpenSSL. Он позволяет задать полную командную строку, вызываемую при загрузке зашифрованного сертификата во время инициализации. Команда может быть сценарием или любой другой программой. Первым параметром ей передаётся путь к зашифрованному закрытому ключу, затем заданные пользователем параметры "args"; ей следует вывести в стандартный вывод парольную фразу, позволяющую расшифровать закрытый ключ. Для каждого нового зашифрованного закрытого ключа, загружаемого при инициализации, HAProxy сначала пробует расшифровать его всеми другими уже известными парольными фразами и снова вызывает команду получения парольной фразы, только если ни одна из них не подошла.

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL версии не ниже 3.0. Он позволяет задать строку свойств по умолчанию, используемую при получении алгоритмов у провайдеров. Работает так же, как параметр openssl propquery, и использует тот же синтаксис (описан в <https://www.openssl.org/docs/man3.0/man7/property.html>). Например, если загружены два провайдера, foo и default, запрос propquery "?provider=foo" позволяет по умолчанию выбирать реализации алгоритмов из провайдера foo и обращаться к реализации провайдера default, если нужная реализация не найдена.

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL версии не ниже 3.0. Он позволяет загрузить провайдер во время инициализации. При успешной загрузке HAProxy может использовать любые возможности, предоставляемые этим провайдером. В конфигурационном файле можно задать несколько параметров 'ssl-provider'. Провайдеры загружаются в порядке их появления.

Обратите внимание: явная загрузка провайдера не позволяет OpenSSL автоматически загрузить провайдер 'default'. OpenSSL также позволяет задать провайдеры, которые следует загрузить, непосредственно в своём конфигурационном файле (например, openssl.cnf), поэтому для их загрузки необязательно использовать параметр 'ssl-provider'. Команда CLI "show ssl providers" позволяет показать все успешно загруженные провайдеры.

Путь поиска провайдеров OpenSSL по умолчанию можно найти в выводе команды "openssl version -a". Если провайдер находится в другом каталоге, можно задать переменную окружения OPENSSL_MODULES, указав в ней каталог с провайдером.

См. также "ssl-propquery" и "ssl-provider-path".

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

Этот параметр доступен только при сборке с поддержкой OpenSSL версии не ниже 3.0. Он позволяет задать путь, по которому OpenSSL ищет провайдеры. Работает так же, как переменная окружения OPENSSL_MODULES. Используется для всех последующих параметров 'ssl-provider' до задания нового 'ssl-provider-path'. См. также "ssl-provider".

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

Этот параметр позволяет настроить способ поиска дополнительных файлов SSL в HAProxy. По умолчанию HAProxy добавляет новое расширение к имени файла (например, для "foobar.crt" загружает "foobar.crt.key"). При включённом параметре HAProxy удаляет расширение перед добавлением нового (например, для "foobar.crt" загружает "foobar.key").

Для работы этого параметра файл crt должен иметь расширение ".crt".

Этот параметр несовместим с расширениями пакетов сертификатов (.ecdsa, .rsa. .dsa) и не пытается удалять их.

По умолчанию этот параметр отключён. См. также "ssl-load-extra-files".

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

Этот параметр изменяет способ поиска файлов, не указанных явно, при загрузке сертификатов SSL в HAProxy. Он применяется к сертификатам строк "bind" и "server", однако некоторые дополнительные файлы не влияют на работу сертификатов строк "server".

По умолчанию HAProxy автоматически находит множество файлов, не указанных в конфигурации. Для сокращения времени запуска это поведение можно отключить.

"none": загружать только файлы, указанные в конфигурации. Не пытаться загружать пакет сертификатов, если файл отсутствует. При загрузке каталога не пытаться объединять сертификаты с одинаковым базовым именем в пакет.

"all": поведение по умолчанию; пытаться загрузить всё: пакеты сертификатов, sctl, ocsp, issuer, key.

"bundle": если файл, указанный в конфигурации, отсутствует, HAProxy пытается загрузить пакет сертификатов. Пакеты сертификатов поддерживаются только на стороне фронтенда и не работают для сертификатов бэкенда.

Начиная с HAProxy 2.3 пакеты больше не загружаются в одно хранилище сертификатов OpenSSL: каждый сертификат загружается в отдельное хранилище, что эквивалентно объявлению нескольких "crt". Для этого требуется OpenSSL 1.1.1. Следовательно, пакеты теперь используются только для обратной совместимости и больше не обязательны для гибридной конфигурации bind с RSA/ECC.

Чтобы объединить эти файлы PEM в пакет сертификатов, распознаваемый HAProxy, их нужно назвать следующим образом: все файлы PEM в пакете должны иметь одинаковое базовое имя и суффикс, обозначающий тип ключа. Сейчас поддерживаются три суффикса: rsa, dsa и ecdsa. Например, если у [www.example.com](http://www.example.com) есть два файла PEM, RSA и ECDSA, они должны называться "example.pem.rsa" и "example.pem.ecdsa". Первая часть имени файла произвольна; имеет значение только суффикс. Для загрузки этого пакета в HAProxy следует указать только базовое имя:

Пример: bind :8443 ssl crt example.pem

Обратите внимание: суффикс не передаётся HAProxy; это указывает HAProxy, что нужно искать пакет сертификатов.

HAProxy загружает все файлы PEM пакета так, будто каждый из них задан отдельно в нескольких "crt".

Загрузка пакетов больше не влияет на загрузку каталога, поскольку файлы загружаются отдельно.

В CLI пакеты представлены отдельными файлами, и для применения изменений в них требуется расширение пакета.

При объединении нескольких сертификатов в пакет поддерживаются файлы OCSP (.ocsp), файлы издателя (.issuer), Certificate Transparency (.sctl) и закрытые ключи (.key).

"sctl": пытаться загрузить "`<basename>`.sctl" для каждого ключевого слова crt. Если файл указан для сертификата бэкенда, он загружается, но не влияет на работу.

"ocsp": пытаться загрузить "`<basename>`.ocsp" для каждого ключевого слова crt. Если файл указан для сертификата бэкенда, он загружается, но не влияет на работу.

"issuer": пытаться загрузить "`<basename>`.issuer", если издатель файла OCSP не указан в файле PEM. Если файл указан для сертификата бэкенда, он загружается, но не влияет на работу.

"key": если закрытый ключ отсутствует в файле PEM, пытаться загрузить файл "`<basename>`.key", содержащий закрытый ключ.

Поведение по умолчанию — "all".

Пример:

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

См. также: "crt", [раздел 5.1](/ru/docs/haproxy/bind-and-server-options/#section-5-1) о параметрах bind и [раздел 5.2](/ru/docs/haproxy/bind-and-server-options/#section-5-2) о параметрах server.

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

Эта директива позволяет выбрать уровень безопасности OpenSSL, описанный в <https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html>. Уровень безопасности применяется ко всем контекстам SSL в HAProxy. Поддерживаются только значения от 0 до 5.

Значение по умолчанию зависит от версии OpenSSL, дистрибутива и способа сборки библиотеки.

Для этой директивы требуется OpenSSL версии не ниже 1.1.1.

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

Поведение проверки SSL по умолчанию на стороне серверов. Если задано 'none', сертификаты серверов не проверяются. Значение по умолчанию — 'required', если оно не переопределено параметром командной строки '-dV'.

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

CA, выпустивший сертификат для самого себя, он же корневой CA x509, служит якорем для проверки цепочки: серверу нет смысла отправлять его, а у клиента он должен быть. Стандартная конфигурация не должна включать такой CA в файл PEM. Этот параметр позволяет оставить такой CA в файле PEM, не отправляя его клиенту. Это позволяет предоставить издателя для ocsp без файла '.issuer' и использовать его совместно с 'issuers-chain-path'. Это касается всех сертификатов без промежуточных сертификатов. Для BoringSSL параметр бесполезен: .issuer игнорируется, поскольку механизму ocsp он не нужен. Требуется OpenSSL версии не ниже 1.0.2.

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

Включает или отключает вычисление максимальных значений статистических счётчиков. Если они не нужны, их отключение может немного повысить производительность. По умолчанию — on.

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

По умолчанию сокет статистики ограничен 10 одновременными соединениями. Изменить это значение можно с помощью "stats maxconn".

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

Привязывает сокет UNIX к `<path>` или адрес TCPv4/v6 к `<address:port>`. Соединения с этим сокетом позволяют получать различные статистические данные и даже выполнять некоторые команды для изменения параметров во время работы. Подробнее см. [раздел 9.3](/ru/docs/haproxy/statistics-and-monitoring/#section-9-3) «Команды Unix-сокета» руководства по управлению.

Поддерживаются все параметры строк "bind", например для ограничения доступа некоторым пользователям или ограничения их прав доступа. Подробнее см. [раздел 5.1](/ru/docs/haproxy/bind-and-server-options/#section-5-1).

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

Тайм-аут сокета статистики по умолчанию составляет 10 секунд. Изменить его можно с помощью "stats timeout". Значение должно передаваться в миллисекундах либо с суффиксом единицы времени из набора { us, ms, s, m, h, d }.

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

Путь к созданному файлу stats-file haproxy. При запуске haproxy предварительно загружает значения из него во внутренние счётчики. Для создания такого файла stats-file используется команда CLI "dump stats-file". Подробнее см. руководство по управлению.

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

Включает альтернативный код для стрессовой нагрузки на исполняемый файл haproxy. Уровень — целое число от 0 до 9. Значение по умолчанию 0 отключает любое выполнение стрессового кода. Уровни от 1 до 9 увеличивают стрессовую нагрузку на исполняемый файл haproxy. Обратите внимание: любое положительное значение может существенно снизить производительность. Поэтому этот режим никогда не следует включать, кроме как для отладки по запросу разработчика.

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

Вызывает отказ при запуске процесса в случае неудачного вызова setrlimit. HAProxy пытается установить наилучшие ограничения setrlimit согласно расчётам. Если это не удаётся, он выводит предупреждение. Этот параметр обеспечивает явный отказ HAProxy при невозможности установить эти ограничения. По умолчанию включён. Его всё равно можно принудительно отключить, добавив перед ним ключевое слово "no".

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

Этот параметр доступен только при сборке с поддержкой потоков. Он перечисляет потоки, которые входят в группу потоков `<group>`. Нумерация потоков и групп начинается с 1. Диапазоны потоков задаются либо отдельными номерами, либо нижней и верхней границами, разделёнными дефисом '-' (например, "1-16"). Нераспределённые потоки автоматически назначаются группам потоков, которые ещё не распределены; группы, заданные этой директивой, никогда не получают больше потоков, чем указано. Повторное определение одной и той же группы заменяет предыдущие определения новым. См. также "nbthread" и "thread-groups".

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

Этот параметр доступен только при сборке с поддержкой потоков. Он разбивает потоки HAProxy на `<number>` независимых групп. В настоящее время значение по умолчанию — 1. Группы потоков позволяют уменьшить объём совместно используемых данных между потоками и тем самым снизить конкуренцию за ресурсы ценой некоторой дополнительной настройки. Это также единственный способ использовать больше 64 потоков, поскольку в каждой группе можно настроить до 64 потоков. Максимальное число групп задаётся при компиляции и по умолчанию равно 16. См. также "nbthread".

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

Этот параметр задаёт предел числа потоков, определённого автоматически или заданного в конфигурации. Особенно полезен в ОС с автоматическим определением числа потоков, когда в универсальных переносимых конфигурациях требуется меньше потоков, чем CPU. Параметр "nbthread" задаёт число потоков, которое при превышении числа доступных CPU приводит к предупреждению и низкой производительности, тогда как thread-hard-limit лишь ограничивает максимальное значение и автоматически не допускает превышения этого числа потоков, но не увеличивает меньшие значения. Если "nbthread" принудительно задан выше этого предела, приоритет имеет thread-hard-limit, а предупреждение позволяет исправить ошибку конфигурации. По умолчанию ограничения нет. См. также "nbthread".

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

Изменяет идентификатор пользователя процесса на `<number>`. Рекомендуется выделить этот идентификатор пользователя для HAProxy или небольшой группы сходных демонов. Для возможности перехода к другому пользователю HAProxy должен быть запущен с правами суперпользователя. См. также "gid" и "user".

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

Задаёт максимальное число файловых дескрипторов на процесс равным `<number>`. По умолчанию оно вычисляется автоматически, поэтому использовать этот параметр не рекомендуется. Если нужно лишь ограничить число файловых дескрипторов, лучше использовать "fd-hard-limit".

Обратите внимание: динамические серверы не учитываются в этом автоматическом расчёте ресурсов. Если их много, может потребоваться задать значение вручную.

См. также: fd-hard-limit, maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group
`<group>` ] [ gid `<gid>` ]

Задаёт общие параметры слушающих сокетов UNIX, объявленных в директивах "bind". Это в основном упрощает объявление таких сокетов UNIX и снижает риск ошибок, поскольку эти параметры обычно необходимы, но зависят от процесса. Параметр `<prefix>` позволяет принудительно сделать все пути сокетов относительными к этому каталогу. Это может понадобиться для доступа к chroot другого компонента. Обратите внимание: эти пути разрешаются до перехода самого HAProxy в chroot, поэтому они абсолютные. Параметры `<mode>`, `<user>`, `<uid>`, `<group>` и `<gid>` имеют тот же смысл, что и одноимённые параметры директивы "bind". Если заданы оба варианта, приоритет имеет директива "bind", то есть параметры "unix-bind" можно считать значениями по умолчанию для всего процесса.

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

Удаляет переменные окружения, указанные в аргументах. Это может быть полезно для сокрытия конфиденциальной информации, иногда наследуемой из окружения пользователя во время некоторых операций. Несуществующие переменные молча игнорируются, поэтому после операции гарантированно не остаётся ни одной из указанных переменных. Изменения вступают в силу немедленно: следующая строка конфигурационного файла уже не видит эти переменные. См. также "setenv", "presetenv" и "resetenv".

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

Аналогично "uid", но используется UID пользователя с именем `<user name>` из /etc/passwd. См. также "uid" и "group".

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

Как и в именах DNS, разрешены только буквы, цифры, дефис и подчёркивание.

Эта директива полезна в конфигурациях HA, где два или более процесса или сервера используют один IP-адрес. Разные значения node-name на всех узлах позволяют сразу определить, какой сервер обрабатывает трафик.

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

Задаёт размер кэша агентов пользователя WURFL. Для ускорения поиска уже обработанные агенты пользователя хранятся в кэше LRU:

- "0" : кэш не используется.
- `<size>` : размер кэша lru в элементах.

Обратите внимание: этот параметр доступен только при сборке HAProxy с USE_WURFL=1.

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

Путь к файлу данных WURFL для служб распознавания устройств. HAProxy следует иметь доступ к этому файлу с соответствующими правами.

Обратите внимание: этот параметр доступен только при сборке HAProxy с USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

Разделённый пробелами список характеристик WURFL, виртуальных характеристик и имён свойств, которые предполагается использовать в добавляемых заголовках. Полный список имён характеристик и виртуальных характеристик доступен на сайте Scientiamobile:

```text
https://www.scientiamobile.com/wurflCapability
```

Допустимые свойства WURFL:

- wurfl_id: содержит идентификатор распознанного устройства.

- wurfl_root_id: содержит корневой идентификатор распознанного устройства.

- wurfl_isdevroot: указывает, является ли распознанное устройство корневым. Возможные значения — "TRUE" и "FALSE".

- wurfl_useragent: исходный агент пользователя, переданный в этом веб-запросе.

- wurfl_api_version: содержит строку с текущей используемой версией API Libwurfl.

- wurfl_info: строка с информацией о разобранном файле wurfl.xml и его полном пути.

- wurfl_last_load_time: содержит временную метку UNIX последней успешной загрузки WURFL.

- wurfl_normalized_useragent: нормализованный агент пользователя.

Обратите внимание: этот параметр доступен только при сборке HAProxy с USE_WURFL=1.

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

Символ для разделения значений в заголовке ответа с результатами WURFL. Если не задан, по умолчанию используется запятая (',').

Обратите внимание: этот параметр доступен только при сборке HAProxy с USE_WURFL=1.

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

Список путей к файлам исправлений WURFL. Обратите внимание: исправления загружаются при запуске, то есть до перехода в chroot.

Обратите внимание: этот параметр доступен только при сборке HAProxy с USE_WURFL=1.

## 3.2. Настройка производительности {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

В некоторых ситуациях, особенно при работе с малой задержкой на процессорах с переменной частотой или внутри виртуальных машин, всякий раз, когда процесс ожидает ввода-вывода через механизм опроса, процессор засыпает либо надолго передаётся другой VM, что вызывает чрезмерно высокие задержки. Этот параметр решает проблему, предотвращая засыпание процессора за счёт постоянного использования нулевого тайм-аута в механизмах опроса. Это значительно сокращает задержку (наблюдалось снижение на 30–100 микросекунд), но создаёт риск перегрева процессора. Параметр можно использовать и с потоками; тогда неверно привязанные потоки могут сильно конкурировать, ухудшая производительность и повышая значения полей CPU stolen в выводе "show info", которые указывают на неправильно настроенные потоки. При использовании этого параметра важно не запускать процесс на том же процессоре, где обрабатываются сетевые прерывания. Также лучше не использовать его для нескольких потоков CPU, разделяющих одно ядро. По умолчанию параметр отключён. Если он включён, его всё равно можно принудительно отключить, добавив перед ним ключевое слово "no". Механизмы опроса "select" и "poll" игнорируют этот параметр.

При бесшовной перезагрузке этот параметр автоматически отключается в старых процессах; это позволяет избежать чрезмерной конкуренции за CPU, когда несколько процессов некоторое время продолжают работать, ожидая завершения текущих соединений.

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

По умолчанию HAProxy пытается распределить начало проверок работоспособности в пределах наименьшего интервала проверок среди всех серверов группы. Это позволяет избежать чрезмерной нагрузки на службы, работающие на одном сервере. Но при больших интервалах проверок (10 секунд или больше) последние серверы группы начинают проверяться с задержкой, что может стать проблемой. Этот параметр задаёт верхнюю границу задержки между первой и последней проверкой, даже если интервалы проверок серверов больше. Однако если серверы используют меньшие интервалы, они соблюдаются.

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

Задаёт максимальное использование CPU, при достижении которого HAProxy прекращает сжатие новых запросов или снижает уровень сжатия текущих запросов. Работает как 'maxcomprate', но измеряет использование CPU вместо пропускной способности входящих данных. Значение выражается в процентах CPU, используемого HAProxy. Значение 100 отключает ограничение. Значение по умолчанию — 100. Меньшее значение не позволяет сжатию замедлять весь процесс и создавать высокие задержки.

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

Задаёт максимальную скорость входящих данных для сжатия на процесс равной `<number>` килобайт в секунду. Если максимум достигнут, уровень сжатия каждого потока снижается во время его обработки. Если максимум достигнут в начале потока, этот поток совсем не сжимается. Если максимум не достигнут, уровень сжатия повышается вплоть до tune.comp.maxlevel. Нулевое значение означает отсутствие ограничения; это значение по умолчанию.

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

Задаёт максимальное число одновременных соединений на процесс равным `<number>`. Эквивалентно аргументу командной строки "-n". Значение, переданное аргументом "-n", имеет приоритет над maxconn в секции global. Процесс HAProxy также может быть собран с переменной времени компиляции SYSTEM_MAXCONN, которая тогда служит системным максимумом maxconn. Аргумент командной строки "-n" также позволяет во время работы обойти ограничение SYSTEM_MAXCONN, если оно задано. При достижении maxconn прокси прекращают принимать соединения. Мягкий предел файловых дескрипторов процесса (его можно узнать командой "ulimit -n") автоматически подстраивается под заданный maxconn. См. также "ulimit-n". Примечание: на некоторых платформах механизм опроса "select" не может надёжно использовать больше 1024 файловых дескрипторов. Если платформа поддерживает только select и при запуске сообщает "select FAILED", нужно уменьшать maxconn, пока запуск не станет успешным (обычно до значения чуть ниже 500). Если maxconn не задан, он автоматически вычисляется по текущим ограничениям файловых дескрипторов, выводимым командой "ulimit -nH" (берётся максимум из жёсткого и мягкого значений). Затем автоматически выбранное значение может быть уменьшено параметром "fd-hard-limit" и ограничением памяти, если оно задано параметром командной строки "-m". Автоматическое значение также зависит от размера буфера, памяти для сжатия, размера кэша SSL, использования SSL и соответствующего maxsslconn, который тоже может выбираться автоматически.

См. также: fd-hard-limit, ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

Задаёт максимальное число соединений в секунду на процесс равным `<number>`. При достижении предела прокси прекращают принимать соединения. Параметр позволяет ограничить общую производительность независимо от возможностей каждого фронтенда. Следует учитывать, что он пригоден только как мера защиты службы: при достижении предела ресурсы не обязательно распределяются между фронтендами справедливо, поэтому полезно также ограничить каждый фронтенд значением, близким к его ожидаемой доле. Кроме того, уменьшение tune.maxaccept может повысить справедливость распределения.

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

Задаёт максимальное число каналов на процесс равным `<number>`. Сейчас каналы используются только для tcp splicing средствами ядра. Поскольку канал содержит два файловых дескриптора, значение "ulimit-n" соответственно увеличивается. Значение по умолчанию — maxconn/4, чего, по-видимому, более чем достаточно для большинства случаев интенсивного использования. Код splice динамически выделяет и освобождает каналы и может вернуться к обычному копированию, поэтому слишком низкое значение может повлиять лишь на производительность.

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

Задаёт максимальное число сеансов в секунду на процесс равным `<number>`. При достижении предела прокси прекращают принимать соединения. Параметр позволяет ограничить общую производительность независимо от возможностей каждого фронтенда. Следует учитывать, что он пригоден только как мера защиты службы: при достижении предела ресурсы не обязательно распределяются между фронтендами справедливо, поэтому полезно также ограничить каждый фронтенд значением, близким к его ожидаемой доле. Кроме того, уменьшение tune.maxaccept может повысить справедливость распределения.

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

Задаёт максимальное число одновременных соединений SSL на процесс равным `<number>`. По умолчанию отдельного ограничения для SSL нет, то есть глобальное значение maxconn применяется ко всем соединениям. Этот предел не позволяет openssl использовать слишком много памяти и аварийно завершаться, когда malloc возвращает NULL (к сожалению, он не всегда надёжно проверяет такие ситуации). Обратите внимание: ограничение касается как входящих, так и исходящих соединений, поэтому одно соединение, которое расшифровывается, а затем шифруется, учитывается как 2 соединения SSL. Если значение не задано, но есть ограничение памяти, оно автоматически вычисляется по этому ограничению, maxconn, размеру буфера, памяти для сжатия, размеру кэша SSL и использованию SSL во фронтендах, бэкендах или с обеих сторон. Если при ограничении памяти не заданы ни maxconn, ни maxsslconn, HAProxy автоматически подбирает их так, чтобы 100% соединений могли безопасно использовать SSL, с учётом сторон, где он включён (фронтенд, бэкенд или обе).

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

Задаёт максимальное число сеансов SSL в секунду на процесс равным `<number>`. При достижении предела слушатели SSL прекращают принимать соединения. Параметр позволяет ограничить общее использование CPU для SSL независимо от возможностей каждого фронтенда. Следует учитывать, что он пригоден только как мера защиты службы: при достижении предела ресурсы не обязательно распределяются между фронтендами справедливо, поэтому полезно также ограничить каждый фронтенд значением, близким к его ожидаемой доле. Следует также учитывать, что сеансы учитываются до попадания в стек SSL, а не после, что защищает стек и от некорректных рукопожатий. Кроме того, уменьшение tune.maxaccept может повысить справедливость распределения.

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

Задаёт максимальный объём RAM в мегабайтах на процесс, доступный zlib. При достижении максимума последующие потоки не сжимаются, пока RAM недоступна. Значение 0 означает отсутствие ограничения. Значение по умолчанию — 0. В сокете UNIX значение доступно в байтах в выводе "show info" в строке "MaxZlibMemUsage"; используемая zlib память указана в "ZlibMemUsage" в байтах.

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

Отключает возврат памяти системе ("malloc_trim") в некоторых ситуациях, когда предпринимаются попытки освободить много памяти: при её нехватке или при перезагрузке. Такой возврат заставляет системный распределитель памяти просмотреть все неиспользуемые области и освободить их. Обычно это полезно, поскольку новому процессу остаётся больше доступной памяти, а старый едва ли будет активно её использовать. Но в некоторых системах с десятками или сотнями тысяч одновременных соединений сильная фрагментация памяти может сделать освобождение чрезвычайно длительным. В это время трафик через процесс больше не проходит, новые соединения не принимаются, некоторые проверки работоспособности могут завершаться неудачей, а сторожевой таймер может сработать и завершить неотвечающий процесс, оставив огромный дамп памяти. Если это происходит, рекомендуется использовать этот параметр, чтобы отключить возврат памяти и прекратить попытки уступать её новому процессу. Обратите внимание: современные распределители памяти обычно не страдают от такой проблемы.

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

Отключает систему опроса событий "epoll" в Linux. Эквивалентно аргументу командной строки "-de". Следующей системой опроса обычно становится "poll". См. также "nopoll".

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

Отключает систему опроса событий event ports в системах SunOS на основе Solaris 10 и новее. Эквивалентно аргументу командной строки "-dv". Следующей системой опроса обычно становится "poll". См. также "nopoll".

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

Отключает getaddrinfo(3) для разрешения имён. Эквивалентно аргументу командной строки "-dG". Используется устаревшая функция gethostbyname(3).

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

Отключает систему опроса событий "kqueue" в BSD. Эквивалентно аргументу командной строки "-dk". Следующей системой опроса обычно становится "poll". См. также "nopoll".

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

Отключает ktls. Эквивалентно аргументу командной строки "-dT".

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

Отключает систему опроса событий "poll". Эквивалентно аргументу командной строки "-dp". Следующей системой опроса становится "select". Отключать "poll" никогда не должно требоваться, поскольку он доступен на всех платформах, поддерживаемых HAProxy. См. также "nokqueue", "noepoll" и "noevports".

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

Отключает SO_REUSEPORT; см. socket(7). Эквивалентно аргументу командной строки "-dR".

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

Отключает tcp splicing средствами ядра между сокетами в Linux. Эквивалентно аргументу командной строки "-dS". После этого данные копируются обычными, более переносимыми вызовами recv/send. tcp splicing средствами ядра доступен лишь в некоторых самых новых вариантах ядра 2.6. Большинство версий от 2.6.25 до 2.6.28 содержат ошибки и пересылают повреждённые данные, поэтому их нельзя использовать. Этот параметр упрощает глобальное отключение splicing при сомнениях. См. также "option splice-auto", "option splice-request" и "option splice-response".

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

Включает ('on') или отключает ('off') профилирование памяти по функциям. Оно собирает статистику вызовов malloc/calloc/realloc/free во всём процессе, включая библиотеки; она доступна в CLI по команде "show profiling". В основном это предназначено для случаев необычного использования памяти, которое нельзя объяснить пулами и для которого нужны дополнительные сведения. Потеря производительности обычно составляет около 1%, возможно немного больше на машинах с большим числом потоков, поэтому механизм обычно подходит для использования в рабочей среде. Того же результата можно добиться во время работы командой CLI "set profiling memory"; см. руководство по управлению.

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

Включает ('on') или отключает ('off') профилирование CPU по задачам. При значении 'auto' профилирование автоматически включается для потока, когда его средняя задержка достигает 1000 микросекунд или больше, согласно полю активности "avg_loop_us", и автоматически отключается, когда задержка становится ниже 990 микросекунд. Это значение усредняется по последним 1024 циклам, поэтому меняется медленно и существенно сглаживает короткие всплески. Профилирование может также время от времени самопроизвольно включаться в перегруженных системах, контейнерах или виртуальных машинах либо при использовании системой подкачки, чего на балансировщике нагрузки категорически нельзя допускать.

При включённом профилировании задач HAProxy может также собирать время, которое каждая задача проводит с удерживаемой блокировкой или в ожидании блокировки, а также время ожидания успешного выделения памяти при промахе кэша пула. Иногда это помогает понять причины задержек. Для этого можно дополнительно передать ключевые слова "lock" (включить сбор времени блокировок), "no-lock" (отключить его), "memory" (включить сбор времени выделения памяти) или "no-memory" (отключить его). По умолчанию сбор этих данных не включён, поскольку на сильно нагруженных системах он может заметно влиять на использование CPU (3-10%). Обратите внимание: накладные расходы возникают только при фактически работающем профилировании, поэтому в режиме "auto" они появляются только тогда, когда HAProxy решает включить его.

Профилирование CPU по задачам удобно для определения, на что расходуется время и как одни запросы влияют на другие. Его включение обычно влияет на общую производительность менее чем на 1%, поэтому рекомендуется оставить значение по умолчанию 'auto', чтобы оно работало только при обнаружении проблемы. Для этой возможности нужна система с поддержкой системного вызова clock_gettime(2) с идентификаторами часов CLOCK_MONOTONIC и CLOCK_THREAD_CPUTIME_ID; в противном случае указанное время будет нулевым. Параметр можно изменить во время работы командой "set profiling" в CLI.

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

Иногда желательно не отправлять агентские проверки и проверки работоспособности серверам через строго одинаковые интервалы, например когда много логических серверов находятся на одном физическом сервере. Этот параметр позволяет добавить случайное отклонение интервала проверок в пределах от 0 до +/- 50%. Значения от 2 до 5, по-видимому, дают хорошие результаты. Значение по умолчанию остаётся 0.

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

Задаёт механизм OpenSSL равным `<name>`. Список допустимых значений `<name>` можно получить командой "openssl engine". Директиву можно использовать несколько раз, что включит несколько криптографических механизмов. Указание неподдерживаемого механизма не позволит HAProxy запуститься. Обратите внимание: многие механизмы дают более низкую производительность HTTPS, чем чисто программная реализация на современных процессорах. Необязательная команда "algo" задаёт алгоритмы по умолчанию, предоставляемые ENGINE, с помощью функции OPENSSL ENGINE_set_default_string(). Значение "ALL" использует механизм для всех криптографических операций. Если список algo не задан, используется "ALL". Можно задать разделённый запятыми список алгоритмов, в том числе RSA, DSA, DH, EC, RAND, CIPHERS, DIGESTS, PKEY, PKEY_CRYPTO, PKEY_ASN1. Этот же формат используется в конфигурационном файле openssl:
<https://www.openssl.org/docs/man1.0.2/apps/config.html>

В HAProxy версии 2.6 поддержка криптографических механизмов отключена в сборке по умолчанию. Этот параметр доступен только при сборке HAProxy с соответствующей поддержкой. Если требуется ssl-engine, HAProxy можно пересобрать с флагом USE_ENGINE=1.

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

Добавляет режим SSL_MODE_ASYNC в контекст SSL. Это включает асинхронные операции ввода-вывода TLS при использовании механизмов SSL с поддержкой асинхронной работы. Текущая реализация поддерживает не более 32 механизмов. API ASYNC в OpenSSL не поддерживает перемещение буферов чтения/записи и несовместим с управлением буферами HAProxy. Поэтому асинхронный режим отключён для операций чтения/записи: он включён только во время начального рукопожатия и повторного согласования.

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

Включает ('on') или отключает ('off') пересылку данных без копирования для апплетов. По умолчанию включена.

См. также: tune.disable-zero-copy-forwarding.

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

Задаёт жёсткий предел числа буферов, которые можно выделить на процесс. Значение по умолчанию — ноль, то есть без ограничения. Предел автоматически корректируется с учётом буферов, зарезервированных для аварийных ситуаций, поэтому пользователю не нужны сложные расчёты. Явное задание этого значения особенно полезно для ограничения памяти процесса с сохранением нормального поведения. При достижении предела задача, запрашивающая буфер, ожидает освобождения другого буфера. Обычно ожидание очень короткое и незаметное, если ограничения остаются разумными. Однако некоторые исторические ограничения ослабляли этот механизм от версии к версии. Известно, что в определённых ситуациях длительной нехватки некоторые задачи могут зависать до истечения тайм-аута, поэтому безопаснее не использовать этот параметр без строгой необходимости.

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

Задаёт число буферов на поток, которые предварительно выделяются и резервируются исключительно для условий нехватки памяти, приводящих к неудачному выделению памяти. Минимальное значение — 0, значение по умолчанию — 4. Изменять его нет причин, если только один из основных разработчиков не рекомендует это по совершенно конкретной причине.

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

Задаёт размер буфера в байтах. Меньшие значения позволяют большему числу потоков одновременно работать при том же объёме RAM, а большие — работать приложениям с очень большими cookie. Значение по умолчанию — 16384, его можно изменить при сборке. Настоятельно рекомендуется оставить значение по умолчанию: слишком малые значения нарушают работу некоторых служб, например статистики, а значения выше значения по умолчанию увеличивают потребление памяти и могут привести к её исчерпанию в системе. Как минимум глобальный параметр maxconn следует уменьшить во столько раз, во сколько увеличен этот размер. Кроме того, при использовании HTTP/2 значение обязательно должно быть не меньше 16384. Оно также должно быть меньше 256 MB (268435456 байт). Если блок заголовков запроса HTTP больше (tune.bufsize - tune.maxrewrite), HAProxy возвращает ошибку HTTP 400 (Bad Request). Аналогично, если блок заголовков ответа HTTP больше этого размера, HAProxy возвращает HTTP 502 (Bad
Gateway). Обратите внимание: заданное этим параметром значение автоматически округляется вверх до ближайшего числа, кратного 8 на 32-битных машинах или 16 на 64-битных. См. также: tune.bufsize.large, tune.bufsize.small.

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

Задаёт размер больших буферов в байтах. По умолчанию поддержка больших буферов отключена; её нужно явно включить, задав это значение.

Эти буферы предназначены для отдельных ситуаций, когда нужно буферизовать больше данных, не меняя размер обычных буферов. Большие буферы не используются неявно. См. также: tune.bufsize.

Обратите внимание: при настройке больших буферов во время запуска для каждого потока выделяются три специальных больших буфера для внутреннего использования.

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

Задаёт размер малых буферов в байтах. Значение по умолчанию — 1024.

Эти буферы предназначены для отдельных ситуаций, когда потребление памяти ограничено, а выделение полного буфера кажется ненужным. Если малого буфера всё же недостаточно, автоматически выполняется повторное выделение памяти для перехода к буферу стандартного размера.

Сейчас малые буферы автоматически используются только протоколом HTTP/3 для отправки заголовков ответа. В остальных случаях их поддержку можно включить для отдельных прокси параметром "use-small-buffers". См. также: tune.bufsize.

См. также: option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

Задаёт максимально допустимый размер полезной нагрузки, передаваемой команде в CLI.

В CLI длина командной строки ограничена размером буфера. Поэтому все команды и их аргументы должны помещаться в буфер для обработки, кроме полезной нагрузки, которую можно передать последней команде строки. При необходимости эта нагрузка может размещаться в отдельной области памяти. Её размер ограничивается этим параметром. Значение по умолчанию — 128KB.

Хотя этого значения должно хватать для большинства случаев, при изменении его нужно выбирать осторожно. Слишком большое значение может повлиять на производительность HAProxy. В зависимости от команды обработка огромной полезной нагрузки может занять достаточно много времени и привести к срабатыванию сторожевого таймера.

Подробности о CLI см. в руководстве по управлению.

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

Задаёт максимальный уровень сжатия. Уровень сжатия влияет на использование CPU при сжатии. Это значение влияет на использование CPU при сжатии. Каждый поток со сжатием инициализирует алгоритм сжатия этим значением. Значение по умолчанию — 1.

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

Для поддержки динамических бэкендов все именованные секции defaults теперь сохраняются в памяти после разбора. Это необходимо, поскольку конфигурация бэкенда, добавленного во время работы, должна основываться на именованной секции defaults.

Это может потреблять много памяти при большом числе экземпляров defaults. В таком случае, если динамические бэкенды не нужны, этим параметром можно принудительно удалять секции defaults после разбора. Однако секции defaults, на которые есть ссылки и которые содержат параметры, не копируемые ссылающимися на них прокси, по-прежнему обязательно сохранять. Например, это касается секций defaults, определяющих правила TCP/HTTP или набор правил tcpcheck.

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

Отключает ускоренную пересылку данных. Этот механизм оптимизирует пересылку, передавая данные напрямую с одной стороны на другую без пробуждения потока. Директива позволяет отключить эту оптимизацию. Обратите внимание: она также отключает любое tcp splicing средствами ядра и пересылку без копирования. Команда не предназначена для обычного использования; как правило, разработчики рекомендуют её лишь во время сложной отладки.

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

Глобально отключает пересылку данных без копирования. Этот механизм оптимизирует ускоренную пересылку, обходясь без буфера канала. Директива позволяет отключить эту оптимизацию. Обратите внимание: она также отключает любое tcp splicing средствами ядра.

См. также: tune.pt.zero-copy-forwarding, tune.applet.zero-copy-forwarding,
tune.h1.zero-copy-fwd-recv, tune.h1.zero-copy-fwd-send, tune.h2.zero-copy-fwd-send,
tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

За время существования HAProxy встречались некоторые сложные проблемы, вызванные ошибками механизма epoll в ядре Linux. Обычно они очень редки и невоспроизводимы вне среды автора сообщения; обойти их иногда можно только отключением epoll и переходом на poll, что не очень подходит для сред с высокой производительностью. Каждый раз проблемы затрагивают лишь совершенно определённые и редкие типы событий, а возможность их маскирования может стать более приемлемым обходным решением. Этот параметр предоставляет такую возможность: он позволяет молча игнорировать некоторые необычные события и заменять их входным событием, сообщающим о неопределённом входящем событии. В результате в некоторых местах не используются быстрые пути обработки ошибок, а применяются только обычные пути. Параметр никогда не следует использовать, если специалист не предложил это для диагностики или обхода ошибки ядра.

Параметр принимает один аргумент: разделённый запятыми список слов, каждое из которых обозначает маскируемое событие. Сейчас поддерживаются следующие события: - "err": маскировать событие EPOLLERR - "hup": маскировать события EPOLLHUP - "rdhup": маскировать события EPOLLRDHUP

Пример:

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

Задаёт число событий, которые обработчик асинхронной задачи (из API event_hdl) может обработать за один раз. `<number>` следует выбирать в пределах от 1 до 10000. Большое число может вызвать конкуренцию между потоками, поскольку задача выполняет тяжёлую работу без прерываний; малое, напротив, может приводить к постоянному повторному планированию задачи, поскольку за один запуск она обрабатывает недостаточно событий и не успевает за их производителем. Значение по умолчанию можно задать при сборке; иначе оно равно 100.

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

При сборке с DEBUG_FAIL_ALLOC или запуске с "-dMfail" задаёт вероятность неудачи попытки выделения памяти в процентах. Она должна находиться в пределах от 0 (без неудач) до 100 (без успехов). Это полезно для отладки и проверки корректной обработки отказов выделения памяти. Если не задана, доля равна 0. Однако параметр командной строки "-dMfail" автоматически устанавливает частоту отказов 1%, поэтому для тестирования необязательно менять конфигурацию.

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

Включает ('on') или отключает ('off') режим опроса по фронту события для поддерживающих его FD. Сейчас он поддерживается только с epoll. Он может заметно сократить число вызовов epoll_ctl() и немного повысить производительность в некоторых сценариях. Режим всё ещё экспериментальный: при наличии ошибок он может приводить к зависанию соединений и по умолчанию отключён.

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

Задаёт минимальное использование CPU от 0 до 100, при котором соединения со слишком большим числом нарушений будут принудительно закрываться. Это касается соединений, достигших предела glitches-threshold. В средах, где очень долгие соединения часто ведут себя некорректно, но не влияют на производительность, может быть желательно сохранять их, пока они не вредят, и начинать закрывать только при высокой загрузке CPU. Параметр задаёт, что соединение, достигшее порога нарушений, принудительно закрывается при использовании CPU на этом уровне или выше, но никогда не закрывается при меньшем уровне. Обратите внимание: использование CPU измеряется для каждого потока, поэтому может быть закрыто даже одно некорректно работающее соединение. Значение по умолчанию — ноль: соединение, достигшее glitches-threshold, автоматически закрывается. В качестве ориентира можно задать значение, равное удвоенному обычному использованию CPU либо обычному использованию CPU плюс половина незанятой доли (например, если CPU обычно достигает 60%, значение 80 может быть разумным). Параметр не действует без tune.h2.fe.glitches-threshold, tune.quic.fe.sec.glitches-threshold или tune.h1.fe.glitches-threshold. См. также глобальные параметры "tune.h2.fe.glitches-threshold", "tune.h1.fe.glitches-threshold" и "tune.quic.fe.sec.glitches-threshold".

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

Задаёт порог числа нарушений в соединении HTTP/1 с бэкендом, по достижении которого соединение автоматически принудительно закрывается. Это позволяет закрывать некорректно работающие соединения без явных правил. Значение по умолчанию — ноль: порог не задан, поэтому никакое событие не приводит к закрытию соединения. Типичные события — неверно оформленные заголовки, которые всё же были приняты благодаря "accept-unsafe-violations-in-http-response". Ненулевое значение, вероятно, следует выбирать в сотнях или тысячах, чтобы механизм работал эффективно, не затрагивая серверы с небольшими отклонениями. С помощью "tune.glitches.kill.cpu-usage" можно также закрывать соединения только при достижении определённого уровня использования CPU. Обратите внимание: при 75% заданного порога предпринимается попытка плавного закрытия путём перехода в режим закрытия соединения и объявления "Connection: close", когда это применимо. Это гарантирует, что соединение с небольшими ошибками через некоторое время перестанет использоваться без риска прервать текущую передачу данных.

См. также: tune.h1.fe.glitches-threshold, bc_glitches и tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

Задаёт порог числа нарушений в соединении HTTP/1 с фронтендом, по достижении которого соединение автоматически принудительно закрывается. Это позволяет закрывать некорректно работающие соединения без явных правил. Значение по умолчанию — ноль: порог не задан, поэтому никакое событие не приводит к закрытию соединения. Типичные события — неверно оформленные заголовки, которые всё же были приняты благодаря "accept-unsafe-violations-in-http-request". Ненулевое значение, вероятно, следует выбирать в сотнях или тысячах, чтобы механизм работал эффективно, не затрагивая клиентов с небольшими отклонениями. С помощью "tune.glitches.kill.cpu-usage" можно также закрывать соединения только при достижении определённого уровня использования CPU. Обратите внимание: при 75% заданного порога предпринимается попытка плавного закрытия путём перехода в режим закрытия соединения и объявления "Connection: close", когда это применимо. Это позволяет клиенту с небольшими отклонениями от протокола создать новое соединение и продолжить работу без помех, не вызывая принудительного закрытия с риском прерывания текущей передачи данных.

См. также: tune.h1.be.glitches-threshold, fc_glitches и tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

Включает ('on') или отключает ('off') приём данных без копирования для мультиплексора H1. По умолчанию включён.

См. также: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

Включает ('on') или отключает ('off') отправку данных без копирования для мультиплексора H1. По умолчанию включена.

См. также: tune.disable-zero-copy-forwarding, tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

Задаёт порог числа нарушений в соединении с бэкендом, по достижении которого соединение автоматически принудительно закрывается. Это позволяет закрывать некорректно работающие соединения без явных правил. Значение по умолчанию — ноль: порог не задан, поэтому никакое событие не приводит к закрытию соединения. Следует учитывать, что некоторые серверы H2 иногда вызывают несколько нарушений за время долгого соединения, поэтому ненулевое значение, вероятно, следует выбирать в сотнях или тысячах, чтобы механизм работал эффективно, не затрагивая серверы с небольшими отклонениями. С помощью "tune.glitches.kill.cpu-usage" можно также закрывать соединения только при достижении определённого уровня использования CPU. Обратите внимание: при 75% заданного порога предпринимается попытка плавного закрытия путём объявления GOAWAY для будущего потока. Это гарантирует, что соединение с небольшими ошибками через некоторое время перестанет использоваться без риска прервать текущую передачу данных.

См. также: tune.h2.fe.glitches-threshold, bc_glitches и tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

Задаёт начальный размер окна HTTP/2 для исходящих соединений: число байт, которые сервер может отправить в ответ до ожидания подтверждения от HAProxy. Параметр влияет только на полезную нагрузку, а не на заголовки. Если не задан, применяется общее значение по умолчанию tune.h2.initial-window-size. Небольшое увеличение может ускорить загрузки или уменьшить использование CPU на серверах ценой несправедливого распределения ресурсов между клиентами. Вместо этого лучше использовать tune.h2.be.rxbuf, который не вызывает такого неравенства. На использование ресурсов параметр не влияет.

См. также: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

Задаёт максимальное число одновременных потоков HTTP/2 на исходящее соединение, то есть число незавершённых запросов в одном соединении с сервером. Если не задан, применяется значение по умолчанию tune.h2.max-concurrent-streams. Значение ниже значения по умолчанию 100 может улучшить отзывчивость сайта ценой большего числа установленных соединений с серверами. При значении "always" параметра "http-reuse" рекомендуется уменьшить это число, чтобы не смешивать слишком много разных клиентов в одном соединении: если один клиент медленнее других, механизм «блокировки начала очереди» может каскадно снижать скорость загрузки для всех клиентов, разделяющих соединение (в таком случае tune.h2.be.initial-window-size следует держать низким). Настоятельно рекомендуется не увеличивать это значение; в некоторых случаях оптимальны малые значения, обычно 1..5.

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

Задаёт максимальное число входящих кадров HTTP/2, обрабатываемых за один раз в соединении с бэкендом. При очень больших буферах полезно задать малое значение, от нескольких десятков до нескольких сотен, чтобы сохранить низкую задержку и более справедливое распределение ресурсов между соединениями. Значение по умолчанию — ноль, то есть ограничение не применяется.

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

Задаёт размер буфера приёма HTTP/2 для исходящих соединений в байтах. Размер округляется вверх до ближайшего числа, кратного tune.bufsize, и разделяется между всеми потоками, отправляющими данные (кадры HEADERS и DATA). В любом случае каждому потоку всегда предоставляется один буфер, а 7/8 неиспользуемых буферов разделяются между потоками, получающими полезную нагрузку. Это значительно повышает производительность отправки данных и устраняет блокировку начала очереди (HoL) в соединениях с бэкендом, разделяемых несколькими клиентами при значении "always" параметра http-reuse. Объявляемое окно каждого потока автоматически подстраивается под доступное пространство, поэтому на практике менять tune.h2.be.initial-window-size не должно требоваться. Если задан размер меньше необходимого для всех потоков, используется этот минимум. Значение по умолчанию — около 1600k (100 потоков с буферами по 16kB).

См. также: tune.h2.be.initial-window-size, tune.h2.fe.rxbuf, http-reuse.

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

Задаёт порог числа нарушений в соединении с фронтендом, по достижении которого соединение автоматически принудительно закрывается. Это позволяет закрывать некорректно работающие соединения без явных правил. Значение по умолчанию — ноль: порог не задан, поэтому никакое событие не приводит к закрытию соединения. Следует учитывать, что некоторые клиенты H2 иногда вызывают несколько нарушений за время долгого соединения, поэтому ненулевое значение, вероятно, следует выбирать в сотнях или тысячах, чтобы механизм работал эффективно, не затрагивая клиентов с небольшими отклонениями. С помощью "tune.glitches.kill.cpu-usage" можно также закрывать соединения только при достижении определённого уровня использования CPU. Обратите внимание: при 75% заданного порога предпринимается попытка плавного закрытия путём объявления GOAWAY для будущего потока. Это позволяет клиенту с небольшими отклонениями от протокола создать новое соединение и продолжить работу без помех, не вызывая принудительного закрытия с риском прерывания текущей передачи данных.

См. также: tune.h2.be.glitches-threshold, fc_glitches и tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

Задаёт начальный размер окна HTTP/2 для входящих соединений: число байт, которые клиент может отправить до ожидания подтверждения от HAProxy. Параметр влияет только на полезную нагрузку, то есть тело запросов POST, а не на заголовки. Если не задан, применяется общее значение по умолчанию tune.h2.initial-window-size. Увеличение может ускорить отправку данных. Значение по умолчанию равно tune.bufsize (16384) и обеспечивает пропускную способность не менее 1.25 Mbps на поток при времени ping 100 ms и 125 Mbps при времени ping 1 ms. На использование ресурсов оно не влияет. Слишком большие значения могут снижать отзывчивость для клиентов, которые обращаются к страницам одновременно с отправкой больших объёмов данных. Вместо этого лучше использовать tune.h2.fe.rxbuf, который не вызывает неравенства в распределении ресурсов.

См. также: tune.h2.initial-window-size.

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

Задаёт максимальное число одновременных потоков HTTP/2 на входящее соединение, то есть число незавершённых запросов в одном соединении от клиента. Если не задан, применяется значение по умолчанию tune.h2.max-concurrent-streams. Значение выше значения по умолчанию 100 иногда может немного ускорить загрузку страниц сложных сайтов с множеством небольших объектов в сетях с высокой задержкой, но также увеличивает использование памяти, позволяя клиенту выделять больше ресурсов одновременно. Значение по умолчанию 100 обычно подходит, и менять его не рекомендуется. Больший параллелизм также влияет на вычислительную нагрузку и задержки при большом числе соединений, каждое из которых использует много потоков, и может снижать порог для атак отказа в обслуживании. После числа команда поддерживает следующие необязательные аргументы:

- rq-load { `<number>` \| auto \| ignore }:

```text
Необязательный аргумент "rq-load" позволяет динамически изменять объявляемый
уровень параллелизма в зависимости от загрузки очереди выполнения текущего
потока: пока загрузка потока остаётся ниже указанного порога, объявляется
настроенный предел числа потоков HTTP. Когда загрузка потока выполнения
превышает настроенный предел, объявляемый предел числа потоков HTTP
уменьшается пропорционально квадрату коэффициента превышения. Целевые
уровни загрузки от 50 до 100 обычно обеспечивают очень хорошее ограничение
при высокой нагрузке. Вместо явного числа ключевое слово также принимает
"ignore" — значение по умолчанию, при котором загрузка очереди выполнения
потока не учитывается при ограничении объявляемого числа потоков HTTP, —
и "auto", которое устанавливает предел равным значению "tune.runqueue-depth".
Последнее обычно даёт хорошие результаты без дальнейшей подстройки
конфигурации.
```

- min `<number>`:

```text
Задаёт минимальный объявляемый уровень параллелизма при использовании rq-load,
даже если это приводит к более высокой загрузке, чем заданная целевая.
Это позволяет сохранить хорошую отзывчивость сайта при очень высокой
нагрузке. Минимальное значение и значение по умолчанию — 1, но значения
от 5 до 15 могут улучшить удобство работы пользователей.
```

Пример:

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

Задаёт максимальное число входящих кадров HTTP/2, обрабатываемых за один раз в соединении с фронтендом. При очень больших буферах полезно задать малое значение, от нескольких десятков до нескольких сотен, чтобы сохранить низкую задержку и более справедливое распределение ресурсов между соединениями. Значение по умолчанию — ноль, то есть ограничение не применяется.

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

Задаёт максимальное число входящих RST_STREAM HTTP/2, обрабатываемых за один раз в соединении с фронтендом. После получения указанного числа кадров RST_STREAM обработчик соединения помещается в очередь с низким приоритетом и обрабатывается после всех остальных задач. Очень малое значение, 1 или несколько единиц, может значительно уменьшить последствия массовой отправки кадров RST_STREAM. Такие RST_STREAM возникают и при нажатии пользователем кнопки остановки в браузере, но дополнительные несколько миллисекунд из-за смены очереди обычно незаметны и при этом эффективно снижают нагрузку от такого наплыва кадров. Значение по умолчанию — ноль, то есть ограничение не применяется.

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

Задаёт максимальное общее число потоков HTTP/2, обрабатываемых на входящее соединение. При достижении предела HAProxy отправляет кадр GOAWAY для плавного закрытия, сообщая клиенту, что соединение будет закрыто после завершения всех ожидающих потоков. На практике клиенты обычно закрывают соединение как можно быстрее после получения кадра и устанавливают новое для следующих запросов. Иногда это полезно и желательно, если клиенты очень долго остаются подключёнными и вызывают неравномерное распределение нагрузки в группе серверов. Например, в некоторых очень динамичных средах новые балансировщики нагрузки создаются на лету при росте нагрузки, а после её снижения их следует останавливать, не разрывая установленные соединения. При задании предела соединения имеют ограниченный срок жизни и часто обновляются; некоторые новые соединения могут устанавливаться с другими узлами, поэтому существующие ресурсы быстро освобождаются.

Следует понимать, что этот предел неявно связан с указанным выше "tune.h2.fe.max-concurrent-streams". HAProxy всегда принимает к обработке любые возможные ожидающие потоки, которые могут находиться в пути между клиентом и фронтендом, поэтому объявляемый предел всегда автоматически увеличивается на значение max-concurrent-streams. Полученное значение служит жёстким пределом: его превышение клиентом, не соблюдающим протокол, приводит к закрытию соединения. Поэтому при подсчёте запросов на соединение по журналам может наблюдаться любое число от max-total-streams до (max-total-streams +
max-concurrent-streams) в зависимости от скорости создания потоков клиентом.

Значение по умолчанию — ноль: ограничений сверх установленных протоколом нет (2^30 ~=
1.07 миллиарда). Значения около 1000 уже могут вызывать частое обновление соединений без заметной задержки для большинства клиентов. Слишком малое значение может повысить использование CPU из-за частых повторных соединений TLS и увеличить время загрузки страниц. Обратите внимание: некоторые инструменты нагрузочного тестирования не поддерживают повторные соединения и могут сообщать об ошибках с этим параметром, поэтому при измерении производительности его может потребоваться отключить. См. также "tune.h2.fe.max-concurrent-streams".

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

Задаёт размер буфера приёма HTTP/2 для входящих соединений в байтах. Размер округляется вверх до ближайшего числа, кратного tune.bufsize, и разделяется между всеми потоками, отправляющими данные (кадры HEADERS и DATA). В любом случае каждому потоку всегда предоставляется один буфер, а 7/8 неиспользуемых буферов разделяются между потоками, отправляющими полезную нагрузку, что значительно повышает производительность отправки данных. Объявляемое окно каждого потока автоматически подстраивается под доступное пространство, поэтому на практике менять tune.h2.fe.initial-window-size не должно требоваться. Если задан размер меньше необходимого для всех потоков, используется этот минимум. Значение по умолчанию 1600k (100 потоков с буферами по 16kB) обеспечивает клиенту скорость отправки примерно 130 Mbps при RTT 100ms.

См. также: tune.h2.fe.initial-window-size и tune.h2.be.rxbuf.

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

Задаёт размер динамической таблицы заголовков HTTP/2. По умолчанию — 4096 байт, максимум — 65536 байт. Большее значение может помочь некоторым клиентам отправлять более компактные запросы в зависимости от их возможностей. Этот объём памяти расходуется на каждое соединение HTTP/2. Менять значение не рекомендуется.

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

Задаёт значение начального размера окна HTTP/2 по умолчанию для входящих и исходящих соединений. Оно используется для входящих соединений, если не задан tune.h2.fe.initial-window-size, и для исходящих, если не задан tune.h2.be.initial-window-size. Параметр задаёт как начальное значение, так и минимум на поток. Значение по умолчанию — 16384 (tune.bufsize), что при отправке данных примерно обеспечивает пропускную способность не менее 1.25 Mbps на поток в сети со временем ping 100 ms либо 125 Mbps в локальной сети с задержкой в 1 миллисекунду. Когда буферов приёма используется меньше максимума, в пределах tune.h2.be.rxbuf и tune.h2.fe.rxbuf, неиспользуемые буферы разделяются между принимающими потоками. Поэтому менять это значение по умолчанию обычно нет смысла. Поскольку его изменение одновременно повышает скорость отправки и усиливает неравенство между клиентами при получении данных, рекомендуется вместо него использовать отдельные параметры сторон: tune.h2.fe.initial-window-size и tune.h2.be.initial-window-size.

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

Задаёт уровень ошибок демультиплексора H2, при котором создаётся запись журнала. По умолчанию — "stream": любая ошибка декодирования в демультиплексоре вызывает запись журнала. Значение "connection" означает, что журналируется только то, что делает соединение недействительным. Наконец, "none" означает, что ни одна ошибка декодирования не вызывает записи журнала. Для обнаружения аномалий протокола рекомендуется задать как минимум "connection", даже если в трудные периоды приходится временно переключаться на "none".

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

Задаёт максимальное число одновременных потоков HTTP/2 на соединение по умолчанию, то есть число незавершённых запросов в одном соединении. Используется для входящих соединений, если не задан tune.h2.fe.max-concurrent-streams, и для исходящих, если не задан tune.h2.be.max-concurrent-streams. Значение по умолчанию — 100. Влияние зависит от стороны; подробнее см. два параметра выше. Рекомендуется отказаться от этого параметра в пользу отдельных параметров сторон. Нулевое значение отключает ограничение, и один клиент может создать столько потоков, сколько HAProxy способен выделить. Настоятельно рекомендуется не менять это значение.

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

Задаёт максимальный размер кадра HTTP/2, который HAProxy сообщает одноранговым узлам как допустимый для приёма. По умолчанию используется большее из 16384 и размера буфера (tune.bufsize). В любом случае HAProxy не объявляет поддержку кадров больше буферов. Основная цель параметра — ограничить максимальный размер кадра при больших буферах. Слишком большие кадры могут повлиять на производительность или вызвать некорректное поведение некоторых одноранговых узлов. Настоятельно рекомендуется не менять значение.

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

Включает ('on') или отключает ('off') отправку данных без копирования для мультиплексора H2. По умолчанию включена.

См. также: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

Задаёт максимальную длину захватываемых cookie. Это максимальное значение, разрешённое для "capture cookie xxx
len yyy"; любое большее значение автоматически усекается до него. Важно не задавать слишком большое значение, поскольку каждый захват cookie всё равно выделяет такой объём независимо от своей настройки: все захваты используют один пул. Этот объём выделяется отдельно на запрос и на ответ, поэтому на соединение расходуется вдвое больше памяти. Если не задано, ограничение составляет 63 символа. Менять значение не рекомендуется.

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

Задаёт максимальную длину URI запроса в журналах. Это предотвращает усечение длинных URI запросов с полезными строками параметров в записях журнала. Параметр не связан с ограничениями syslog. При увеличении предела можно также увеличить параметр 'log ... len yyy'. Демону syslog тоже могут потребоваться специальные директивы конфигурации. Значение по умолчанию — 1024.

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

Задаёт максимальное число заголовков в получаемых сообщениях HTTP. Если число заголовков сообщения, включая первую строку, превышает это значение, запрос отклоняется с кодом состояния "400 Bad
Request", а ответ — с "502 Bad Gateway". Значение по умолчанию — 101; его достаточно для всех случаев, поскольку широко распространённый сервер Apache использует тот же предел. Увеличение может временно позволить работать приложению с ошибками до его исправления. Допустимый диапазон — 1..32767. Следует учитывать, что каждый новый заголовок расходует 32bits памяти на каждый поток, поэтому не следует повышать предел слишком сильно.

Обратите внимание: HTTP/1.1 — текстовый протокол, поэтому при отправке сообщения отдельного ограничения нет. Ограничения при разборе достаточно. HTTP/2 и HTTP/3 — двоичные протоколы, требующие этапа кодирования. При кодировании заголовков также устанавливается предел для соблюдения ограничений протоколов. Он достаточно велик, но намеренно не документирован. По той же причине этот предел применяется и на первых этапах декодирования.

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

Управляет совместным использованием пулов простаивающих соединений потоками для одного сервера. Его можно включить для всех потоков одной группы ('on'), для всех потоков ('full') или отключить ('off'). По умолчанию пулы совместно используются потоками одной группы ('on'), чтобы сократить число постоянных соединений с сервером и повысить долю повторного использования соединений. Совместное использование потоками других групп может влиять на производительность и по умолчанию отключено, но полезно, если максимальное повторное использование соединений приоритетно. Для отладки или при подозрении на ошибку HAProxy в повторном использовании соединений удобно принудительно отключить совместное использование пула несколькими потоками, задав "off". Настоятельно не рекомендуется отключать этот параметр без консервативного значения "pool-low-conn" для всех серверов, чья высокая производительность зависит от повторного использования соединений; иначе с ростом числа потоков соединения могут закрываться очень часто.

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

Задаёт время, после которого HAProxy считает, что пустой буфер, вероятно, связан с простаивающим потоком. Это позволяет оптимально менять размеры некоторых пакетов при чередовании пересылки больших и малых объёмов данных. Параметр влияет на решение использовать splice() или отправлять большие буферы по SSL. Значение задаётся в миллисекундах от 0 до 65535. Ноль означает, что HAProxy не пытается обнаруживать простаивающие потоки. Значение по умолчанию — 1000; оно, по-видимому, правильно обнаруживает паузы пользователя, например чтение страницы перед щелчком. Причин для изменения этого значения быть не должно. См. ниже tune.ssl.maxrecord.

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

Обычно все строки "bind" создают один шард: один сокет, который слушают все потоки процесса. При большом числе потоков это не очень эффективно и может создавать значительные накладные расходы ядра при обновлении состояния опроса или распределении событий между потоками. Современные ОС поддерживают балансировку входящих соединений: несколько сокетов могут быть привязаны к одному адресу и порту, а все входящие соединения равномерно распределяются между ними, поэтому каждый поток видит только соединения, ожидающие в сокете, к которому он привязан. Это значительно сокращает накладные расходы ядра и повышает производительность при обработке входящих соединений. В HAProxy это обычно включается параметром "shards" строк "bind" со значением по умолчанию 1, при котором каждому слушателю в процессе соответствует единственный сокет. В системах с множеством процессоров удобнее изменить значение по умолчанию на "by-thread", чтобы всегда создавать один слушающий сокет на поток, либо на "by-group", чтобы создавать один слушающий сокет на группу потоков. При "by-thread" следует учитывать использование файловых дескрипторов: каждому слушателю нужно столько сокетов, сколько потоков. Кроме того, некоторые ОС, например FreeBSD, ограничивают число сокетов на одном адресе значением 256. Обратите внимание: "by-group" остаётся эквивалентом "by-process" в конфигурациях по умолчанию с одной группой потоков и возвращается к общему сокету в системах без поддержки этого механизма. Значение по умолчанию — "by-group" с переходом на "by-process" для систем или семейств сокетов, не поддерживающих множественные привязки.

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

Включает ('on' / 'fair') или отключает ('off') приём соединений слушателем с несколькими очередями. Он распределяет входящий трафик между всеми потоками, на которых разрешено работать строке "bind", вместо приёма только для себя. Это даёт более плавное распределение трафика и гораздо лучше масштабируется, особенно если потоки нагружены неравномерно из-за внешней активности, например сетевых прерываний на одном из потоков. Режим по умолчанию "on" оптимизирует выбор потока, выбирая из выборки поток с наименьшим числом соединений. Часто это лучший выбор для долгих соединений, поскольку он поддерживает занятость всех потоков. Второй режим, "fair", последовательно обходит все потоки независимо от их текущей нагрузки. Он может лучше подходить для коротких соединений или машин с очень большим числом потоков, где вероятность найти самый свободный поток в первом режиме мала. Наконец, "off" позволяет принудительно отключить перераспределение для устранения неполадок либо для коротких соединений, когда считается, что ОС уже достаточно хорошо распределяет их. Значение по умолчанию — "on".

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

Явно задаёт haproxy способ обработки объектов образцов haproxy при передаче в Lua. Например, при использовании встроенных преобразователей, функций извлечения образцов или переменных из сценария Lua haproxy преобразует внутренний тип smp в соответствующий тип Lua. Из-за исторической реализации обработка логических значений неоднозначна: при преобразовании Lua -\> haproxy smp логические значения сохраняются правильно, но при преобразовании haproxy smp -\> Lua они ошибочно преобразовывались в целые числа. Поэтому функция извлечения образца или преобразователь, возвращающий логическое значение, при использовании из Lua возвращал целое число 0 или 1. К сожалению, в Lua логические значения и целые числа не взаимозаменяемы. Во избежание неоднозначности параметр "tune.lua.bool-sample-conversion" должен быть явно задан либо как "normal", отказавшись от прежнего поведения ради согласованности, либо как "pre-3.1-bug", сохранив прежнее поведение, чтобы не нарушить логику существующих сценариев. Если параметр не задан явно, а из конфигурации загружается сценарий Lua, haproxy выводит предупреждение, и неявно применяется "pre-3.1-bug" для сохранения прежнего поведения. Рекомендуется задать "normal", предварительно убедившись, что используемые сценарии Lua правильно обрабатывают образцы bool haproxy как логические значения.

Чтобы параметр учитывался, он должен быть задан до любой директивы "lua-load" или "lua-load-per-thread"; иначе он игнорируется.

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

Тайм-аут выполнения "burst" применяется к любому обработчику Lua. Если обработчик не завершится или не уступит выполнение до достижения тайм-аута, он будет прерван, чтобы предотвратить конкуренцию между потоками, слишком долгое необслуживание трафика и в конечном счёте аварийное завершение процесса при срабатывании сторожевого таймера. В отличие от других тайм-аутов Lua, суммируемых между уступками выполнения, burst-timeout ограничивает время одного непрерывного окна выполнения Lua заданным тайм-аутом.

Уступка выполнения здесь означает, что выполнение Lua фактически прерывается либо явным вызовом функции, уступающей выполнение, например core.(m)sleep() или core.yield(), либо автоматической принудительной уступкой (см. tune.lua.forced-yield). Оно возобновится позднее, когда соответствующая задача будет запланирована заново. Не все обработчики Lua могут уступать выполнение: следует различать обработчики с такой возможностью и без неё.

Для обработчиков, способных уступать выполнение, например задач и действий, достижение тайм-аута может означать, что "tune.lua.forced-yield" слишком велик для системы и его уменьшение улучшит ситуацию. Можно также проверить, помогают ли явные уступки выполнения в ключевых точках функции Lua. Это может указывать и на то, что обработчик слишком долго находится в определённой библиотечной функции Lua, которую нельзя прервать.

Для обработчиков, неспособных уступать выполнение, например преобразователей Lua и функций извлечения образцов, это может означать слишком большой объём вычислений из-за неудачного проектирования: такие обработчики часто блокируют ход выполнения запроса и от них ожидается быстрое завершение, чтобы его обработка могла продолжиться. Обычно стоит попытаться оптимизировать функцию Lua по скорости, поскольку уменьшение "tune.lua.forced-yield" не поможет.

Этот тайм-аут учитывает только чистое время выполнения Lua. Если Lua вызывает core.sleep, время сна не учитывается. Тайм-аут по умолчанию — 1000ms.

Примечание: если обработчик запускает цикл GC Lua, явно либо автоматически по инициативе Lua через некоторое время, длительность цикла GC также учитывается.

Время цикла GC невозможно определить, поэтому на насыщенных системах возможны ложные срабатывания: GC не успевает за нагрузкой и занимает большую часть доступного времени выполнения. В таком случае можно попробовать следующие решения:

    - проверить, можно ли оптимизировать сценарий, чтобы уменьшить потребление памяти Lua
    - настроить параметры GC Lua и / или явно запрашивать циклы GC
      (см.: https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage)
    - увеличить tune.lua.burst-timeout

Значение 0 полностью отключает эту защиту.

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

Эта директива заставляет механизм Lua уступать выполнение через каждые `<number>` выполненных инструкций. Это позволяет прерывать длинный сценарий и даёт планировщику HAProxy возможность обрабатывать другие задачи, например принимать соединения или пересылать трафик. Значение по умолчанию — 10000 инструкций для сценариев, загруженных через "lua-load-per-thread", и MAX(500, 10000 / nbthread) инструкций для сценариев, загруженных через "lua-load". Экспериментально это оказалось оптимальным для производительности с учётом предотвращения конкуренции нескольких потоков за глобальную блокировку Lua.

Если HAProxy часто выполняет код Lua, но требуется большая отзывчивость, значение можно уменьшить. Если код Lua достаточно длинный и его результат совершенно необходим для обработки данных, `<number>` можно увеличить, но значение следует выбирать разумно: в многопоточной среде оно может усилить конкуренцию за ресурсы.

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

Включает ('on') или отключает ('off') запись вывода сценариев LUA через средства ведения журнала текущего прокси, если они есть.

По умолчанию — 'on'.

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

Включает ('on') или отключает ('off') запись вывода сценариев LUA через stderr. При значении 'auto' запись через stderr условно включается ('on'), если выполняется хотя бы одно из условий:

    - tune.lua.log.loggers имеет значение 'off'
    - сценарий выполняется вне контекста прокси и глобального средства ведения журнала нет
    - сценарий выполняется в контексте прокси, к которому не подключено средство ведения журнала

Обратите внимание: при включении эта запись дополняет ведение журнала, настроенное через tune.lua.log.loggers.

По умолчанию — 'auto'.

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

Задаёт максимальный объём RAM в мегабайтах на процесс, доступный Lua. По умолчанию — ноль, то есть без ограничения. Важно задать предел, чтобы ошибка сценария не привела к исчерпанию памяти системы.

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

Выбирает стандартные библиотеки Lua, загружаемые при инициализации состояния Lua. Аргумент — разделённый запятыми список имён библиотек из набора table, io, os, string, math, utf8, package, debug. Вместо списка можно использовать специальные значения "all" и "none". Значение "none" нельзя сочетать с именами библиотек. Значение по умолчанию — "all".

Библиотеки base и coroutine всегда загружаются независимо от этого параметра: base предоставляет основные функции Lua, необходимые HAProxy, а coroutine требуется, поскольку HAProxy заменяет coroutine.create() собственной безопасной реализацией.

Обратите внимание: fork() и создание новых потоков уже заблокированы в HAProxy по умолчанию независимо от этого параметра и могут быть снова включены только глобальной директивой "insecure-fork-wanted". Ограничение набора загружаемых библиотек дополнительно уменьшает поверхность атаки, доступную сценариям Lua. В частности: - исключение "os" запрещает os.execute() и os.exit() - исключение "io" запрещает io.open() и io.popen() - исключение "package" запрещает загрузку нативных модулей C через require() - исключение "debug" запрещает изучение внутреннего состояния HAProxy через debug.getupvalue(), debug.getmetatable() или debug.sethook()

Примеры:

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

Этот параметр должен быть задан до любой директивы "lua-load", "lua-load-per-thread" или "lua-prepend-path"; иначе возвращается ошибка разбора.

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

Тайм-аут выполнения служб Lua. Полезен для предотвращения бесконечных циклов или чрезмерно долгой работы Lua. Учитывает только чистое время выполнения Lua. Если Lua переходит в сон, время сна не учитывается. Тайм-аут по умолчанию — 4s.

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

Тайм-аут выполнения сеансов Lua. Полезен для предотвращения бесконечных циклов или чрезмерно долгой работы Lua. Учитывает только чистое время выполнения Lua. Если Lua переходит в сон, время сна не учитывается. Тайм-аут по умолчанию — 4s.

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

Назначение то же, что у "tune.lua.session-timeout", но тайм-аут предназначен для задач. По умолчанию он не задан, поскольку задача может существовать всё время работы HAProxy, например задача проверки серверов.

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

Задаёт число активных проверок на поток, выше которого поток активно пытается найти менее нагруженный поток для проверки работоспособности либо ставит её в очередь до уменьшения числа выполняемых на нём проверок. Значение по умолчанию — ноль: такого ограничения нет. Параметр может понадобиться в средах с чрезвычайно большим числом дорогих проверок и множеством потоков, если нагрузка распределяется неравномерно и проверки работоспособности могут случайно достигать тайм-аута при запуске. Типичный случай — OpenSSL 3.0, где проверки работоспособности примерно в 20 раз сильнее нагружают CPU, чем в более ранних версиях. В результате работа по проверкам выравнивается между всеми потоками. Для подавляющего большинства конфигураций менять параметр не нужно. Обратите внимание: слишком малые значения могут значительно замедлить проверки работоспособности, если они выполняются медленно.

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

Задаёт максимальное число соединений, которые процесс может принять подряд перед переходом к другой работе. В однопроцессном режиме большие числа раньше повышали производительность при высокой интенсивности соединений, но с несколькими очередями это больше не так. Значение применяется отдельно к каждому слушателю с учётом числа процессов, к которым он привязан. Значение по умолчанию — 4, показавшее лучшие результаты. Если из старой конфигурации унаследовано значительно большее значение, его имеет смысл удалить: это повысит производительность и уменьшит время ответа. В многопроцессном режиме оно делится на удвоенное число процессов, к которым привязан слушатель. Значение -1 полностью отключает ограничение. Обычно подстраивать это значение не должно требоваться.

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

Задаёт максимальное число событий, обрабатываемых за один вызов системы опроса. Значение по умолчанию подбирается под ОС. Замечено, что уменьшение ниже 200 обычно немного снижает задержку ценой пропускной способности сети, а увеличение выше 200 обычно повышает задержку ради небольшого роста пропускной способности. Заданное значение должно быть не больше 1000000.

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

Задаёт размер зарезервированного пространства буфера в байтах. Оно используется для изменения или добавления заголовков. Первые чтения из сокетов никогда не заполняют больше bufsize-maxrewrite. Исторически значение по умолчанию составляло половину bufsize, хотя это не очень разумно, поскольку редко требуется добавлять много заголовков. Слишком большое значение не позволяет обрабатывать большие запросы или ответы. Слишком малое не позволяет добавлять заголовки в уже большие запросы или запросы POST. Обычно разумно выбрать около 1024. Если значение больше половины bufsize, оно автоматически уменьшается до этой половины. Поэтому при изменении bufsize об этом беспокоиться не нужно.

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

Задаёт максимальное число правил, вычисляемых за один раз функциями обработки наборов правил, если они поддерживают уступку выполнения. Например, нередки конфигурации с множеством правил "tcp-request content" или "http-request". Большое число правил в сочетании с действиями, требующими много CPU, например работающими с содержимым, может вызвать конкуренцию между потоками: если вычисление не прерывается, все правила набора выполняются в одном цикле опроса. Для наборов правил, ориентированных на содержимое и уже поддерживающих уступку выполнения при его проверке, параметр гарантирует выполнение не более `<number>` правил в одном цикле опроса. Он принудительно заставляет функцию вычисления уступить выполнение, чтобы продолжить обработку в следующем цикле опроса.

Затрагиваемые наборы правил:

- "tcp-request content"
- "tcp-response content"
- "http-request"
- "http-response"

Значение по умолчанию — 50.

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

Задаёт объём памяти на поток, который сохраняется готовым к использованию в локальном кэше и никогда не может быть освобождён другими потоками. Доступ к этой памяти очень быстрый, без блокировок, а достаточный объём критичен для производительности при сильной конкуренции потоков. Значение выражается в байтах; значение по умолчанию задаётся при сборке через CONFIG_HAP_POOL_CACHE_SIZE и составляет 524288 (512 kB). Большее значение может повысить производительность в некоторых сценариях, особенно когда профили показывают высокую нагрузку на выделение памяти. По опыту, удачное значение находится между размером кэша L2 одного ядра CPU и удвоенным этим размером. Слишком большие значения ухудшают производительность из-за неэффективного использования кэшей L3 в CPU и потребляют больше памяти. Рекомендуется не менять значение либо увеличивать его небольшими шагами. Для полного отключения кэшей CPU на поток может подойти очень малое значение, но лучше использовать "-dMno-cache" в командной строке.

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

Подстраивает буферизацию ядра на сокет так, чтобы сторона отправки сокета считалась заполненной, когда объём буферизованных данных равен этому значению плюс измеренный размер окна. Принцип — оставлять в буферах сокета лишь строго необходимый минимум байт и небольшой запас, соответствующий объёму, который будет отправлен до следующей попытки отправки haproxy. Малое значение, обычно около tune.bufsize, значительно снижает потребление памяти системными буферами и задержку приложения при отправке буферизованных данных. В поддерживающих системах этот параметр обычно эффективнее и точнее, чем tune.sndbuf.client и tune.sndbuf.client. Применяется на соединение, от клиента или к серверу в зависимости от параметра, и используется только для TCP. Значение по умолчанию — ноль, то есть без ограничения. Доступен только в Linux.

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

Задаёт размер кэша поиска шаблонов равным `<number>` записей. Это кэш LRU, запоминающий предыдущие поиски и их результаты. Он используется ACL и таблицами соответствий для медленного поиска шаблонов: методов "sub", "reg", "dir", "dom", "end", "bin" и строк без учёта регистра. Применяется к выражениям шаблонов, поэтому запоминает результат поиска среди всех шаблонов строки конфигурации, включая загруженные из файлов. Записи, обновлённые действиями HTTP или через CLI, автоматически становятся недействительными. Размер кэша по умолчанию — 10000 записей, что ограничивает объём памяти примерно 5 MB на процесс/поток в 32-битных системах и 8 MB на процесс/поток в 64-битных, поскольку кэши локальны для потока/процесса. Риск коллизии очень мал, порядка размера кэша, делённого на 2^64. Обычно при 10000 запросов в секунду и кэше по умолчанию из 10000 записей вероятность одной коллизии от атаки перебором составляет 1% за 60 лет или 0.1% за 6 лет. Это считается гораздо ниже риска повреждения памяти из-за старения компонентов. Если такой риск неприемлем, кэш можно отключить значением 0.

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

Задаёт максимальное число обновлений stick-table, которые haproxy пытается обработать за один раз при отправке сообщений. Получение данных обновлений требует блокировок, которые без ограничения могут сильно нагружать CPU на машинах с множеством потоков и увеличивать задержку трафика при начальной пакетной передаче между старым и новым процессом. Малые значения, напротив, тоже могут увеличить накладные расходы CPU и время завершения. Значение по умолчанию — 200, менять его не рекомендуется.

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

Задаёт размер буфера канала ядра в байтах. По умолчанию каналы имеют стандартный для системы размер. Иногда при TCP splicing увеличение каналов повышает производительность, особенно если предполагается, что каналы не заполняются и выполняется много вызовов splice(). Это влияет на потребление памяти ядром, поэтому значение нельзя менять без понимания последствий.

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

Задаёт максимальное число файловых дескрипторов, используемых HAProxy глобально, в процентах от максимума доступных HAProxy дескрипторов, при котором начинается принудительное закрытие простаивающих соединений, если соединение нельзя использовать повторно и нужно создать новое. Значение по умолчанию — 25: четверть файловых дескрипторов означает, что примерно половина максимально допустимых соединений с фронтендом может поддерживать простаивающее соединение с другой стороны. При ориентации на повторное использование соединений большее значение, вероятно, обычно не имеет смысла.

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

Задаёт максимальное число файловых дескрипторов, используемых HAProxy глобально, в процентах от максимума доступных HAProxy дескрипторов, при котором прекращается добавление соединений в пул простаивающих соединений для повторного использования. Значение по умолчанию — 20.

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

Включает ('on') или отключает ('off') пересылку данных без копирования для транзитного мультиплексора. Для её использования также должно быть настроено splicing средствами ядра. По умолчанию включена.

См. также: tune.disable-zero-copy-forwarding, option splice-auto, option splice-request и option
splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

Определяет число потерянных пакетов, необходимое алгоритму управления перегрузкой Cubic для признания события потери. Обычно любое событие потери считается результатом перегрузки, и его достаточно, чтобы Cubic снова начал с меньшего окна. Но эксперименты показывают, что у потерь бывают разные причины, совершенно не связанные с перегрузкой: такие потери можно считать ложными, а изменение окна лишь замедляет связь, не давая другого эффекта. Частые причины — слабый радиосигнал, доставка не по порядку, высокое использование CPU клиента со случайными задержками и неточность системного таймера. Этот параметр делает Cubic немного терпимее к ложным потерям, изменяя минимальное суммарное число потерь между двумя ACKs, которое считается событием потери; по умолчанию оно равно 1. Экспериментально наблюдались значительные улучшения, но всегда с ростом пропускной способности, расходуемой на повторные передачи, и риска насыщения перегруженных каналов. Значение 2 можно кратковременно использовать для сравнения метрик. Нельзя превышать 2 без предварительного анализа ситуации специалистом. Значение по умолчанию и минимум — 1. Всегда используйте 1.

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

Включает ('on') или отключает ('off') алгоритм HyStart++ (RFC 9406) для соединений QUIC вместо фазы медленного старта алгоритмов управления перегрузкой, которые могут вызывать большие потери пакетов. По умолчанию отключён.

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

Задаёт предел числа раз, когда один кадр QUIC может быть отмечен как потерянный. При превышении соединение считается неисправным и немедленно закрывается.

Значение по умолчанию — 10.

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

Задаёт максимальный размер окна по умолчанию для контроллера перегрузки одного соединения QUIC на стороне фронтенда или бэкенда. Значение должно быть целым числом с необязательным суффиксом 'k', 'm' или 'g' и находиться в пределах от 10k до 4g.

Мультиплексор QUIC также использует текущий размер окна перегрузки, чтобы определить, можно ли выделить новые буферы потоков при отправке данных. Поэтому максимальный размер окна перегрузки ограничивает и этот распределитель памяти.

Значение по умолчанию — 480k.

См. также параметры "quic-cc-algo" для bind и server.

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

Коэффициент, применяемый к вычисленному порогу переупорядочения пакетов. Слишком малое значение может привести к обнаружению большого числа потерянных пакетов.

Значение по умолчанию — 50.

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

Задаёт транспортный параметр QUIC max_idle_timeout на стороне фронтенда или бэкенда. Использует формат времени HAProxy и выражается в миллисекундах. Определяет время, после которого соединение молча закрывается, если оставалось неактивным в течение соответствующего периода. Обе стороны используют одно согласованное значение: - минимум двух параметров, если оба ненулевые, - максимум, если ненулевым является только один, - если оба параметра нулевые, механизм отключён.

Значение по умолчанию — 30s.

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

Задаёт порог числа нарушений на соединение на стороне фронтенда или бэкенда, по достижении которого соединение автоматически принудительно закрывается. Это позволяет закрывать некорректно работающие соединения без явных правил. Значение по умолчанию — ноль: порог не задан, поэтому никакое событие не приводит к закрытию соединения. Следует учитывать, что некоторые клиенты QUIC иногда вызывают несколько нарушений за время долгого соединения, поэтому ненулевое значение, вероятно, следует выбирать в сотнях или тысячах, чтобы механизм работал эффективно, не затрагивая клиентов с небольшими отклонениями. С помощью "tune.glitches.kill.cpu-usage" можно также закрывать соединения только при достижении определённого уровня использования CPU.

См. также: fc_glitches, tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

Динамически включает Retry для всех настроенных слушателей QUIC при достижении указанного числа полуоткрытых соединений. Полуоткрытое соединение — соединение, рукопожатие которого ещё не завершилось успешно или неудачей. Для работы параметра должен быть задан секрет кластера; иначе он молча игнорируется (см. "cluster-secret"). Параметр также молча игнорируется при принудительном использовании QUIC Retry (см. "quic-force-retry").

Значение по умолчанию — 100.

Подробнее о QUIC retry см. <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2>.

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

Глобально задаёт способ использования сокета соединениями QUIC фронтенда для приёма и отправки. Соединения могут совместно использовать сокет слушателя либо выделять собственный сокет для каждого соединения.

Значение по умолчанию — "default-on": для каждого соединения QUIC выделяется отдельный сокет. Этот вариант предпочтителен для наилучшей производительности при большом трафике QUIC. Это также единственный способ гарантировать корректную мягкую остановку без потери данных для соединений QUIC и эффективную обработку временных ошибок sendto(). Однако он зависит от некоторых расширенных возможностей сетевого стека UDP. Если платформа считается несовместимой, haproxy при запуске автоматически переключается в режим "force-off". Обратите внимание: слушатели QUIC на привилегированных портах могут требовать работы с uid 0 либо настройки ОС, разрешающей целевому uid привязываться к таким портам, например системных полномочий. См. также глобальную директиву "setcap".

Значение "force-off" означает, что передача QUIC выполняется через общий сокет слушателя. Это может быть хорошим компромиссом при небольшом трафике, поскольку снижает потребление FD. Но производительность не будет оптимальной из-за более высокого использования CPU, если слушатели разделяются многими потоками или одновременно используется много соединений QUIC.

Этот параметр применяется совместно с параметрами bind "quic-socket". При глобальном режиме "default-on" он включается для каждого слушателя, кроме настроенных с "quic-socket
listener". Однако глобальное значение "force-off" применяется ко всем экземплярам слушателей независимо от их индивидуальной конфигурации.

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Новый параметр называется "tune.quic.fe.sock-per-conn"; прежнее значение "connection" соответствует "default-on", а "listener" — "force-off".

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

Позволяет задать жёсткий предел числа байт данных в пути по каждому потоку. Выражается в процентах относительно параметра rxbuf потоков соединения QUIC; результат округляется вверх до bufsize.

Значение по умолчанию — 90. Оно подходит для наиболее частого веб-сценария, где данные отправляются лишь по одному или нескольким потокам, а остальные используются только для получения данных. Если предел rxbuf потоков соединения остаётся разумным, это гарантирует, что лишь часть открытых потоков может выделить свой максимальный объём памяти.

Если приложение использует много параллельных потоков отправки и сталкивается с несправедливым распределением ресурсов между ними, имеет смысл уменьшить этот коэффициент, повысив справедливость и снизив пропускную способность на поток.

См. также: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

На стороне фронтенда используется как объявляемое значение транспортного параметра initial_max_streams_bidi. Задаёт максимальное число двунаправленных потоков, которые удалённый одноранговый узел вправе открыть одновременно за время соединения. Фактически ограничивает число одновременных запросов HTTP/3 клиента.

Значение по умолчанию — 100. Обратите внимание: его уменьшение может ограничить возможности буферизации потоков при приёме и ухудшить пропускную способность отправки данных. Это можно исправить увеличением параметра rxbuf потоков соединения QUIC.

На стороне бэкенда haproxy локально ограничивает число одновременных запросов, мультиплексируемых в одном соединении. Управление потоком у однорангового узла может дополнительно снизить этот предел. Может потребоваться уменьшить значение по умолчанию 100 для улучшения отзывчивости сайта ценой большего числа открытых соединений с бэкендом. Как и на стороне фронтенда, параметр напрямую влияет на возможности буферизации Rx, но здесь ограничивает получение данных HTTP. Параметр rxbuf потоков QUIC можно увеличить, если большинство ответов HTTP больше "tune.bufsize".

См. также: "tune.quic.be.stream.rxbuf", "tune.quic.fe.stream.rxbuf",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

Задаёт максимальное число запросов, обслуживаемых одним соединением QUIC. При достижении общего числа начинается плавное завершение соединения. В HTTP/3 это означает отправку кадра GOAWAY. Окончательно соединение закрывается после завершения всех оставшихся передач данных.

Применяется как жёсткий предел соединения через механизм управления потоком QUIC. Если одноранговый узел нарушает его, соединение немедленно закрывается.

Позволяет заставить клиентов время от времени открывать новые соединения для продолжения отправки запросов, избегая чрезмерно долгого сохранения соединений. Однако малые значения увеличивают задержку на стороне клиента и использование CPU с обеих сторон из-за рукопожатий TLS.

Значение по умолчанию — 0: отдельного ограничения сверх ограничения кодирования протокола QUIC нет (2^60, более миллиарда миллиардов).

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

Жёсткий предел числа байт данных в пути по соединению QUIC фронтенда. Используется как значение транспортного параметра initial_max_data. Напрямую влияет на пропускную способность отправки однорангового узла в зависимости от задержки и на потребление памяти одним соединением в haproxy.

По умолчанию — 0: значение должно автоматически вычисляться как произведение max-concurrent и bufsize. Его можно увеличить, например если приложение бэкенда зависит от отправки больших объёмов данных в сетях с высокой задержкой.

См. также: "tune.quic.be.stream.max-concurrent", "tune.quic.fe.stream.max-concurrent",
"tune.quic.be.stream.data-ratio", "tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

Включает ('on') или отключает ('off') равномерную отправку данных QUIC. По умолчанию включена. Цель — сгладить отправку данных и уменьшить потери в сети. В большинстве сценариев это значительно повышает пропускную способность, избегая повторных передач. Но в сетях с очень высокой пропускной способностью и низкой задержкой отключение может быть полезно для предотвращения нежелательной задержки и уменьшения использования CPU.

См. также параметры "quic-cc-algo" для bind и server.

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

Включает ('on') или отключает ('off') поддержку UDP GSO для отправки QUIC. По умолчанию включена. Эта возможность ядра позволяет отправлять несколько датаграмм одним системным вызовом, что эффективнее при больших передачах. При подозрении на проблему отправки может быть полезно отключить её по рекомендации разработчиков.

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

Отключает транспортный протокол QUIC на стороне фронтенда. Все слушатели QUIC по-прежнему создаются, но не принимают входящие датаграммы. Поэтому haproxy не обрабатывает трафик QUIC на стороне фронтенда.

Значение по умолчанию — "on". При подозрении на проблему с трафиком QUIC параметр позволяет легко переключать слушатели QUIC, не меняя каждую отдельную строку конфигурации.

См. также функцию извлечения образца "quic_enabled".

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

Задаёт максимальный объём памяти, доступный стеку QUIC для отправки на транспортном уровне. Ограничивает как байты в пути, так и выходные буферы мультиплексора. Обратите внимание: для предотвращения конкуренции потоков предел не соблюдается строго и иногда может быть превышен. Кроме того, каждое соединение всегда может использовать окно не менее 2 датаграмм, поэтому вместе с этим параметром следует задать подходящий maxconn.

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

Это ключевое слово объявлено устаревшим в 3.3 и будет удалено в 3.5. Это часть упрощения конфигурации QUIC. Если параметр используется, он применяется только к соединениям фронтенда.

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

Включает ('on') или отключает ('off') отправку данных без копирования для мультиплексора QUIC. По умолчанию включена.

См. также: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

Этот параметр конфигурации принимает значения от -20 до 19. Задаёт приоритет планирования согласно man 2 setpriority. Приоритет применяется после разбора конфигурации, то есть только рабочим или самостоятельным процессом. Обычно он задаёт более высокий приоритет, чем у процесса, разбирающего конфигурацию (tune.renice.startup).

См. также: tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

Этот параметр конфигурации принимает значения от -20 до 19. Задаёт приоритет планирования согласно man 2 setpriority. Приоритет применяется перед остальной конфигурацией, что полезно для снижения приоритета её разбора. Он применяется к самостоятельному или рабочему процессу до разбора конфигурации. После разбора прежний приоритет восстанавливается, если не используется tune.renice.runtime.

См. также: tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

Задаёт размер буфера приёма сокета ядра для неподключённых сокетов. Может использоваться для QUIC в режиме слушателя и log-forward на фронтенде. Системные буферы по умолчанию иногда слишком малы для сокетов, принимающих большой суммарный трафик, что вызывает потери и, в случае QUIC, возможные повторные передачи, а также может замедлять установление соединений при высокой нагрузке. Значение выражается в байтах и применяется к каждому сокету. В режиме слушателя сокеты разделяются всеми соединениями, а их общее число зависит от "shards" строки "bind". Единого удачного значения нет: оно соответствует ожидаемому размеру на соединение, умноженному на ожидаемое число соединений. Ядро может уменьшать большие значения. См. также аналоги для подключённых сокетов "tune.rcvbuf.client" и "tune.rcvbuf.server", а также параметры отправки "tune.sndbuf.backend" и "tune.sndbuf.frontend".

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

Принудительно задаёт размер буфера приёма сокета ядра на стороне клиента или сервера указанным значением в байтах. Применяется ко всем фронтендам и бэкендам TCP/HTTP. Обычно его никогда не следует задавать: размер по умолчанию 0 позволяет ядру автоматически подбирать значение по доступной памяти. Однако иногда очень малые значения, например 4096, помогают экономить память ядра, не позволяя буферизовать слишком много принятых данных. При этом малые значения значительно повышают использование CPU.

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

HAProxy использует несколько признаков, чтобы определить, что короткое чтение означает конец данных в буферах сокета. Один из них — чтение возвращает больше `<recv_enough>` байт; по умолчанию это 10136 (7 сегментов по 1448). Этим параметром можно изменить значение по умолчанию для лучшей работы с нагрузками, содержащими много коротких сообщений, например сеансами telnet или SSH.

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

Задаёт число очередей записи перед кольцевыми буферами. Это может влиять на использование CPU трассировками во время отладки; и слишком малые, и слишком большие значения могут сильно влиять на него. Удачное значение определено разработчиками экспериментально, и менять его нет причин, если только это не предложено для решения конкретной проблемы. Такую настройку не следует сохранять в конфигурации при обновлении версий, поскольку оптимальное значение может меняться со временем.

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

Задаёт максимальное число задач, обрабатываемых за один раз при выполнении задач. Значение по умолчанию зависит от числа потоков, но находится между 35 и 280: такие значения обычно дают наибольшую интенсивность запросов и наименьшие задержки. Увеличение может добавить задержку при вводе-выводе, а слишком малое значение — дополнительные накладные расходы. При большем числе потоков полезны меньшие значения. При экспериментах со значительно большими значениями может быть полезно также включить tune.sched.low-latency и, возможно, tune.fd.edge-triggered, чтобы максимально снизить наибольшую задержку.

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

Включает ('on') или отключает ('off') планировщик задач с низкой задержкой. По умолчанию HAProxy обрабатывает задачи нескольких классов по одному классу за раз, поскольку это наиболее эффективно. Но при больших значениях tune.runqueue-depth это может заметно влиять на задержку запросов или соединений. При включении этого параметра задачи классов с более низким приоритетом, если они есть, всегда выполняются раньше остальных. Это уменьшает максимальную задержку новых запросов или соединений на фоне большого трафика, но сильнее влияет на этот большой трафик. Для обычного использования лучше оставить параметр выключенным. Значение по умолчанию — off.

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

Задаёт размер буфера отправки сокета ядра для неподключённых сокетов. Используется для ведения журнала через сокет UNIX и UDP на стороне бэкенда и для QUIC в режиме слушателя на фронтенде. Системные буферы по умолчанию иногда слишком малы для сокетов, разделяемых множеством соединений или отправителей журналов, что вызывает потери, возможные повторные передачи и замедляет установление новых соединений при высоком трафике. Значение выражается в байтах и применяется к каждому сокету. В режиме слушателя сокеты разделяются всеми соединениями, а их общее число зависит от "shards" строки "bind". Единого удачного значения нет: оно соответствует ожидаемому размеру на соединение, умноженному на ожидаемое число соединений. Ядро может уменьшать большие значения. См. также аналоги для подключённых сокетов "tune.sndbuf.client" и "tune.sndbuf.server", а также параметры приёма "tune.rcvbuf.backend" и "tune.rcvbuf.frontend".

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

Принудительно задаёт размер буфера отправки сокета ядра на стороне клиента или сервера указанным значением в байтах. Применяется ко всем фронтендам и бэкендам TCP/HTTP. Обычно его никогда не следует задавать: размер по умолчанию 0 позволяет ядру автоматически подбирать значение по доступной памяти. Однако иногда очень малые значения, например 4096, помогают экономить память ядра, не позволяя буферизовать слишком много принятых данных. При этом малые значения значительно повышают использование CPU. Ещё один случай использования — предотвращение тайм-аутов записи с чрезвычайно медленными клиентами, когда ядро ждёт чтения большой части буфера перед повторным уведомлением HAProxy. См. также tune.notsent-lowat.client и tune.notsent-lowat.server: в Linux они позволяют эффективнее и точнее управлять памятью и отзывчивостью без потери производительности.

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

Задаёт размер глобального кэша сеансов SSL в блоках. Блок достаточно велик для закодированного сеанса без сертификата однорангового узла. Сеанс с таким сертификатом хранится в нескольких блоках в зависимости от размера сертификата. Блок использует примерно 200 байт памяти согласно расчёту `sizeof(struct sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE` для функции `shctx_init`. Значение по умолчанию можно задать при сборке; иначе оно равно 20000. При заполнении кэша дольше всех неиспользуемые записи удаляются и назначаются заново. Большие значения сокращают такие удаления и число сильно нагружающих CPU рукопожатий SSL, позволяя всем пользователям сохранять сеансы как можно дольше. Все записи предварительно выделяются при запуске. Значение 0 отключает кэш сеансов SSL.

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

Задаёт максимальный размер буфера для захвата списка шифров client hello, списка расширений, списка эллиптических кривых и форматов точек эллиптических кривых. При значении 0, используемом по умолчанию, захват отключён; иначе для каждого соединения SSL/TLS выделяется буфер.

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

Позволяет настроить поддержку сжатия сертификатов — расширения TLS 1.3 (RFC 8879).

При "auto" используется значение по умолчанию библиотеки TLS.

При "off" выполняется попытка явно отключить поддержку этой возможности. HAProxy больше не пытается отправлять сжатые сертификаты и не принимает их.

Настраивает стороны бэкенда и фронтенда.

Это ключевое слово поддерживается OpenSSL \>= 3.2.0.

Значение по умолчанию — auto.

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

Задаёт максимальный размер параметров Диффи — Хеллмана для генерации эфемерного или временного ключа при обмене DHE. Конечный размер стремится совпасть с размером ключа RSA или DSA сервера, например временный ключ DH в 2048 бит для ключа RSA в 2048 бит, но не превышает этот максимум. Разрешены только значения 1024 или выше. Большие значения повышают нагрузку CPU; значения больше 1024 бит не поддерживаются клиентами Java 7 и более ранними. Параметр не используется, если статические параметры Диффи — Хеллмана заданы непосредственно в файле сертификата либо через ssl-dh-param-file. Если не определены ни default-dh-param, ни ssl-dh-param-file и файл PEM сервера данного фронтенда не содержит собственных параметров DH, шифры DHE недоступны для этого фронтенда.

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

Отключает совместное использование кэша сеансов SSL всеми процессами. Обычно параметр не следует использовать: попадание клиентов в случайный процесс вызывает много повторных согласований. Но он может требоваться в ОС, где нельзя использовать ни один способ синхронизации кэша SSL. Тогда первый уровень балансировки на основе хеша перед слоем SSL может уменьшить последствия отсутствия совместного использования сеансов.

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

Задаёт максимальное число байт, передаваемых SSL_write() за один раз. Значение по умолчанию 0 означает отсутствие ограничения. В отличие от tune.ssl.maxrecord этот параметр не подстраивается динамически. Меньшие записи могут снизить пропускную способность, но могут требоваться для клиентов с малым объёмом ресурсов.

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

Включает запись ключей TLS в журнал. Использовать следует осторожно: расходуется больше памяти на сеанс SSL и может снижаться производительность. По умолчанию отключено.

Эти функции извлечения образцов следует использовать для создания SSLKEYLOGFILE, необходимого для расшифровки трафика в wireshark.

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

SSLKEYLOG представляет собой последовательность строк следующего формата:

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

Значение ClientRandom предоставляет функция извлечения образца %[ssl_fc_client_random,hex]; секрет и метку Label можно найти в таблице ниже. Нужно создать SSLKEYLOGFILE со всеми метками из этой таблицы.

Следующие функции извлечения образцов возвращают шестнадцатеричные строки, которым не требуется преобразование.

```text
  Метка SSLKEYLOGFILE             |  Извлечение образцов секретов
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

Эти функции извлечения существуют для стороны фронтенда (fc) или бэкенда (bc); для нужной стороны следует заменить "xx" на "fc" или "bc".

Доступно только с OpenSSL 1.1.1 и полезно для сеанса TLS1.3.

Для создания содержимого SSLKEYLOGFILE с TLS \< 1.3 нужна только эта строка:

"CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]"

Полный журнал ключей можно создать следующим log-format, хотя для syslog это неидеально:

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

HAProxy также предоставляет эти форматы как предопределённые переменные окружения, которые можно напрямую использовать в директиве "log-format":

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   ключи соединения фронтенда (со стороны клиента)
$HAPROXY_KEYLOG_BC_LOG_FMT   ключи соединения бэкенда (со стороны сервера)
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

Ограничивает принимаемое число KeyUpdate в секунду значением `<limit>`, после которого это считается
потоком избыточных обновлений и соединение принудительно закрывается. Обработка KeyUpdate требует много CPU, и мало
оснований получать их в большом числе. Значение "0" отключает ограничение интенсивности. Значение по умолчанию
— 100. <a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

Задаёт срок действия кэшированного сеанса SSL. Время выражается в секундах; по умолчанию — 300 (5 min). Следует понимать, что это не гарантирует сохранение сеансов на такой срок: при заполнении кэша дольше всех неиспользуемые сеансы удаляются независимо от заданного срока действия. Главная польза параметра — предотвращение слишком долгого использования сеансов.

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

Задаёт максимальное число байт, передаваемых SSL_write() в начале передачи данных. Значение по умолчанию 0 означает отсутствие ограничения. При SSL/TLS клиент может расшифровать данные только после получения полной записи. При больших записях ему может потребоваться загрузить до 16kB данных перед началом обработки. Ограничение может ускорить загрузку страниц в браузерах в сетях с высокой задержкой или низкой пропускной способностью. Рекомендуется подобрать оптимальные значения, помещающиеся в 1 или 2 сегмента TCP: обычно 1448 байт в Ethernet с включёнными временными метками TCP или 1460 при отключённых. Следует учитывать накладные расходы SSL/TLS. Типичные значения 1419 и 2859 показали хорошие результаты в тестах. Для выбора лучшего значения используется "strace -e trace=write". HAProxy автоматически переключается на этот параметр после обнаружения простаивающего потока (см. выше tune.idletimer). См. также tune.ssl.hard-maxrecord.

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

Задаёт размер кэша созданных сертификатов равным `<number>` записей. Это кэш LRU. Динамическое создание сертификата SSL затратно, поэтому сертификаты кэшируются. Размер кэша по умолчанию — 1000 записей.

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

Задаёт целевой процент потоков на соединение фронтенда относительно максимального числа одновременных соединений (maxconn), когда все соединения установлены. Метрика применяется к мультиплексируемым протоколам, например HTTP/2 и QUIC, где каждое соединение может получать несколько потоков. Всегда гарантируется хотя бы один, поэтому процент должен быть не меньше 100%. При установлении соединений HAProxy динамически объявляет дополнительные потоки до заданного предела, сохраняя целевое соотношение. При установлении каждое соединение фронтенда получает хотя бы один поток; дополнительные назначаются по целевому проценту и настроенным ограничениям потоков. Это обеспечивает эффективное распределение потоков при меняющейся нагрузке: больше при низкой, меньше при высокой.

Очень динамичные сайты с множеством объектов на странице выигрывают от высоких коэффициентов, позволяющих использовать много потоков на соединение. Сайты с меньшим средним числом потоков, например WebSocket или код приложения, могут предпочесть малые коэффициенты около 120 или 150: потоков на 20–50% больше, чем соединений. Это предотвращает чрезмерное число потоков при длительной нагрузке.

Значение по умолчанию — 0: на этом уровне ограничение не применяется, действуют лишь настройки H2 и QUIC. При значении по умолчанию 100 потоков на соединение это соответствует 10000%. Это остаётся рекомендуемым вариантом для небольших развёртываний, где maxconn около тысячи. Конфигурации среднего размера, от нескольких тысяч до десятков тысяч соединений, обычно задают коэффициент от 1000 до 5000, позволяющий от 10 до 50 потоков на соединение при полной нагрузке. Крупные развёртывания, от сотен тысяч до миллионов соединений, могут использовать меньшие значения от 120 до 200, в среднем от 1.2 до 2 потоков на соединение при полной нагрузке.

В отличие от HTTP/2, QUIC способен динамически менять число одновременных потоков за время соединения. Однако управление потоком QUIC строже, чем в HTTP/2, поэтому лучше задавать достаточно большие значения, чтобы избежать дополнительной задержки соединения. Есть также ограничение для слушателей QUIC с включённым 0-RTT: начальное значение, объявляемое одноранговому узлу, игнорирует эластичность потоков и зависит только от "tune.quic.fe.stream.max-concurrent". Но после этого начального объявления эластичность потоков продолжает действовать за время соединения.

Мониторинг общего числа активных потоков на бэкендах, включая очереди, даёт практический показатель устойчивой целевой нагрузки и помогает избежать избыточного выделения ресурсов.

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

Задаёт число счётчиков привязок, одновременно отслеживаемых соединением или запросом действиями "track-sc\*" в правилах "tcp-request" или "http-request". Значение по умолчанию задаётся при сборке макросом MAX_SESS_STK_CTR и равно 3. Параметр позволяет изменить его, игнорируя значение сборки, но нельзя задать больше 100. Увеличение может понадобиться при переносе сложных конфигураций в haproxy, однако следует учитывать затраты: каждая запись занимает 16 байт на соединение и 16 байт на запрос; для всех запросов эту память нужно выделять и обнулять, даже когда она не используется. Поэтому значение 10 увеличивает расход памяти на запрос на 320 байт и заставляет очищать её при каждом запросе, что заметно влияет на CPU. Если правил "track-sc" нет, значение, напротив, можно уменьшить; 0 допустим для полного отключения счётчиков привязок.

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

По умолчанию попыток использовать простаивающие соединения других групп потоков нет, но это можно изменить. Допустимые значения `<value>`: "none", значение по умолчанию, не пытается использовать простаивающие соединения других групп; "restricted" пытается получить простаивающее соединение другого потока только при протоколах, которые не могут создавать новые соединения, например reverse http, а также при strict-maxconn; "full" всегда ищет простаивающие соединения в других группах потоков. Обратите внимание: соединения других групп могут снижать производительность, поэтому использовать их не следует без действительной необходимости. Теперь это поведение управляется tune.idle-pool.shared; это ключевое слово оставлено лишь для совместимости со старыми конфигурациями и будет объявлено устаревшим.

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

Эти пять параметров помогают управлять максимальным объёмом памяти системы переменных. "global" ограничивает общую память всех областей действия; "proc" — память области процесса; "sess" — области сеанса; "txn" — области транзакции; "reqres" — обработки каждого запроса или ответа. Учёт памяти иерархический: более общие ограничения включают более узкие. "proc" включает "sess", "sess" — "txn", а "txn" — "reqres".

Например, при ограничении "tune.vars.sess-max-size" до 100 значения "tune.vars.txn-max-size" и "tune.vars.reqres-max-size" тоже не могут превышать 100. Переменная "txn.var" со 100 байтами занимает всё доступное пространство. Обратите внимание: превышение ограничений во время работы не вызывает сообщения об ошибке, но значения могут усекаться или повреждаться. Поэтому следует точно планировать пространство для хранения всех переменных.

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

Задаёт параметр memLevel при инициализации zlib для каждого потока. Он определяет, сколько памяти следует выделить для внутреннего состояния сжатия. Значение 1 использует минимум памяти, но работает медленно и снижает степень сжатия; 9 использует максимум памяти для оптимальной скорости. Допустимы значения от 1 до 9. Значение по умолчанию — 8.

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

Задаёт размер окна, то есть буфера истории, как параметр инициализации zlib для каждого потока. Большие значения улучшают сжатие ценой потребления памяти. Допустимы значения от 8 до 15. Значение по умолчанию — 15.

## 3.3. Отладка {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

Задаёт глобальный ключ анонимизации `<key>`, который должен быть 32-битным числом от 0 до 4294967295. Он используется по умолчанию командами CLI при включённом режиме анонимизации. Его можно также задать во время работы командой CLI "set anon global-key". См. также аргумент командной строки "-dC" в руководстве по управлению.

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

Включает ('on') или отключает ('off') обновление счётчиков событий в коде. Они выводятся под типом "CNT" командой CLI "debug counters". Счётчики доступны только при сборке с DEBUG_COUNTERS не меньше 1. При значении 1 они по умолчанию не обновляются ("debug.counters off"), а при 2 обновляются ("debug.counters on"). Обычно менять параметр нет причин, если только этого не просит разработчик или не подозревается необычно большое использование CPU; в последнем случае необходимо отправить разработчикам сообщение с дампом счётчиков. Состояние можно также изменить во время работы командой CLI "debug counters". См. руководство по управлению.

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

Приостанавливает разбор конфигурации на `<timeout>` миллисекунд. Полезно для разработки или проверки тайм-аутов сценариев инициализации, особенно для имитации очень долгой перезагрузки. Требует заданного expose-experimental-directives.

`<timeout>` — значение тайм-аута, по умолчанию в миллисекундах. Можно использовать любую другую единицу, добавив её суффиксом к числу, как объясняется в начале документа.

Пример:

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

Ускоряет выход старого процесса при перезагрузке, пропуская освобождение объектов памяти и слушателей: ОС сама возвращает их при завершении процесса. Выигрыш невелик — максимум порядка нескольких сотен миллисекунд для огромных конфигураций. Основной случай использования — обнаруженная ошибка кода deinit(), которую таким образом можно обойти. Лучше не использовать параметр без указания разработчиков.

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

Не выводит никаких сообщений при запуске. Эквивалентно аргументу командной строки "-q".

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

Позволяет задать задержку, после которой зависшая задача, блокирующая трафик, вызывает предупреждение в стандартном потоке ошибок. Задержка выражается в миллисекундах; по умолчанию — 100 ms. Допустимые значения должны находиться в пределах от 1 ms до 1000 ms включительно. Малые значения вызывают частые предупреждения, большие — редкие. В любом случае сторожевой таймер завершает вышедшую из-под контроля задачу, которая дважды по одной секунде не отвечает, поэтому задержка предупреждения 1000 ms обычно не вызывает предупреждений. Рекомендуется оставаться в пределах от 10 до 100ms для обнаружения ошибок конфигурации, ухудшающих работу пользователя долгими ответами или рывками интерактивных сеансов. Например, это может вызывать неудачно спроектированная функция извлечения образца Lua с тяжёлыми вычислениями либо очень большой файл таблицы соответствий map_reg или map_regm с высокой стоимостью вычисления. Для сравнения: рукопожатие TLS может занимать от одной до двух миллисекунд, а сжатие буфера ответа HTTP размером 16kB — около одной миллисекунды. Вывод содержит дамп потока проблемной задачи с трассировкой стека и контекстом, помогающим понять, на что расходуется время.

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

При заданном параметре HAProxy отказывается запускаться, если при разборе и применении конфигурации выдано хотя бы одно предупреждение. Предупреждения о неверных сочетаниях параметров, слишком высоких ограничениях, которые не удалось установить, и тому подобном завершают процесс с ошибкой при запуске. Некоторые поздние предупреждения запуска перехватить нельзя, например невозможность удалить дополнительные группы при смене идентификатора группы в режимах "daemon" или "master-worker" либо невозможность разрешить создание дампа процесса после fork(). Параметр не перехватывает предупреждения во время работы. Настоятельно рекомендуется включать его для редко изменяемых конфигураций: это помогает обнаруживать неочевидные ошибки и сохранять конфигурацию чистой и совместимой с будущими версиями. Обратите внимание: "haproxy -c" в таком случае тоже сообщает об ошибках. Параметр эквивалентен аргументу командной строки "-dW".

## 3.4. Настройка HTTPClient {#section-3-4}

HTTPClient — внутренняя библиотека HTTP, доступная различным подсистемам, например сценариям LUA. Она не используется в тракте данных и не связана с трафиком HTTP, проходящим через HAProxy.

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

Отключает разрешение DNS httpclient. Предотвращает создание секции resolvers "default".

Значение по умолчанию — off.

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

Определяет секцию resolvers, с которой httpclient пытается разрешать имена.

По умолчанию используется идентификатор resolvers "default". Если параметр не задан, при отсутствии секции разрешение имён просто отключается.

Однако при явном включении этого параметра неудачная загрузка вызывает ошибку конфигурации.

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

Позволяет выбрать семейство IP при разрешении имён, что удобно, если в сети нет IPv6. По умолчанию — "ipv6".

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

Позволяет настроить число повторных попыток httpclient при неудачном запросе. Работает так же, как ключевое слово "retries" в бэкенде.

Значение по умолчанию — 3.

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

Определяет ca-file, который следует использовать для проверки сертификата сервера. Принимает те же параметры, что "ca-file" в строке server.

По умолчанию, если параметр не задан, используется "@system-ca", пытающийся загрузить системные CA. При неудаче SSL для httpclient отключается.

Однако при явном включении этого параметра неудача вызывает ошибку конфигурации.

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

Работает так же, как параметр verify строк server. При 'none' сертификаты серверов не проверяются. По умолчанию — "required".

По умолчанию, если параметр не задан, используется "required". При неудаче SSL для httpclient отключается.

Однако при явном включении этого параметра неудача вызывает ошибку конфигурации.

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

Задаёт максимальное время ожидания попытки соединения по умолчанию для httpclient.

Аргументы:

```text
<timeout> — значение тайм-аута, по умолчанию в миллисекундах. Можно использовать
            и другую единицу измерения, добавив её к числу в качестве суффикса,
            как объясняется в начале этого документа.
```

Значение по умолчанию — 5000ms.
