---
title: "3. 全局段"
linkTitle: "3. 全局段"
weight: 140
description: "进程安全、性能调优、调试和 HTTP 客户端设置"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [参考]
aliases:
  - /haproxy/configuration/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

“global” 段中的参数为进程级配置，通常与操作系统相关。这些参数通常只需一次性设置，一旦配置正确便无需再修改。部分参数在命令行中也有对应选项。

以下关键字在 “global” 段中受支持：

- 进程管理与安全

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

- 性能调优

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
  - tune.quic.cc.cubic.min-losses （已弃用）
  - tune.quic.cc-hystart （已弃用）
  - tune.quic.disable-tx-pacing （已弃用）
  - tune.quic.disable-udp-gso （已弃用）
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
  - tune.quic.frontend.max-data-size （已弃用）
  - tune.quic.frontend.max-idle-timeout （已弃用）
  - tune.quic.frontend.max-streams-bidi （已弃用）
  - tune.quic.frontend.max-tx-mem （已弃用）
  - tune.quic.frontend.stream-data-ratio （已弃用）
  - tune.quic.frontend.default-max-window-size （已弃用）
  - tune.quic.listen
  - tune.quic.max-frame-loss （已弃用）
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio （已弃用）
  - tune.quic.retry-threshold （已弃用）
  - tune.quic.socket-owner （已弃用）
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
  - tune.ssl.capture-cipherlist-size （已弃用）
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay （已弃用）
  - tune.ssl.ocsp-update.mindelay （已弃用）
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- 调试

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

## 3.1. 进程管理与安全 {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

用于提供设备检测服务的 51Degrees 数据文件路径。该文件应已解压，并可由 HAProxy 以相应权限访问。

请注意，此选项仅在 HAProxy 编译时包含 USE_51DEGREES 时可用。

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

要从数据集加载的 51Degrees 属性名称列表。完整名称列表可在 51Degrees 官网获取：<https://51degrees.com/resources/property-dictionary>

请注意，此选项仅在 HAProxy 编译时包含 USE_51DEGREES 时可用。

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

在包含 51Degrees 结果的响应头中，每个属性值后将追加一个字符。若未设置，则默认为“,”。

请注意，此选项仅在 HAProxy 编译时包含 USE_51DEGREES 时可用。

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

设置 51Degrees 转换器缓存的大小为 `<number>` 项。该缓存为 LRU 缓存，用于保留之前的设备检测及其结果。默认情况下，此缓存处于禁用状态。

请注意，此选项仅在 HAProxy 编译时包含 USE_51DEGREES 时可用。

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

启用（'on'）或禁用（'off'）检测过程中对性能图的使用。默认值取决于 51Degrees 库。

请注意，此选项仅在 HAProxy 使用 USE_51DEGREES 和 51DEGREES_VER=4 编译时可用。

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

启用（'on'）或禁用（'off'）检测过程中对预测图的使用。默认值取决于 51Degrees 库。

请注意，此选项仅在 HAProxy 使用 USE_51DEGREES 和 51DEGREES_VER=4 编译时可用。

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

设置检测允许的漂移值。

请注意，此选项仅在 HAProxy 使用 USE_51DEGREES 和 51DEGREES_VER=4 编译时可用。

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

设置检测可允许的差异值。

请注意，此选项仅在 HAProxy 使用 USE_51DEGREES 和 51DEGREES_VER=4 编译时可用。

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

启用（'on'）或禁用（'off'）检测过程中使用未匹配节点。默认值取决于 51Degrees 库。

请注意，此选项仅在 HAProxy 使用 USE_51DEGREES 和 51DEGREES_VER=4 编译时可用。

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

启用或禁用 ACME 调度器。

ACME 调度器在 HAProxy 启动时开始运行，它将遍历所有证书，并在 notAfter 值超过当前时间加上 (notAfter - notBefore) / 12 时启动 ACME 证书续订任务；若 notBefore 未定义，则使用 7 天作为阈值。调度器随后将休眠，并在 12 小时后唤醒。

默认值为 "auto"。

另请参阅：acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

当 "ca-file"、"ca-verify-file" 或 "crl-file" 指令使用相对路径时，指定获取 SSL CA 证书和 CRL 的默认目录。在 "ca-file"、"ca-verify-file" 和 "crl-file" 中指定的绝对路径具有优先权，并忽略 "ca-base"。

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

将当前目录切换至 `<jail dir>`，并在降权前在此处执行 chroot() 操作。
若存在未知漏洞被利用，此操作可显著提升安全性，使攻击者极难利用系统。
必须确保 `<jail dir>` 对任何用户均为空且不可写。
当以超级用户权限启动进程时，将直接执行 chroot()。
在 Linux 系统上，若以非特权身份启动，HAProxy 会尝试通过 unshare(CLONE_NEWUSER) 创建的新用户命名空间内执行 chroot()；若该机制不可用，chroot() 将以常规错误失败。

作为特殊情况，`<jail dir>` 可设置为 "auto"，此时 HAProxy 会创建一个匿名临时目录，将其删除，并 chroot 进入该目录。所生成的 jail 在文件系统中没有名称，且为空、只读，从而无需预先准备专用的 jail 目录。

以超级用户权限启动时，若未使用 chroot，将显示警告信息，以鼓励用户始终使用该机制。若因特定原因必须不使用 chroot（例如通过路径不便的 Unix 套接字访问服务器），仍可通过显式添加 "chroot /" 来静默警告，此举的优点在于配置中可见。

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

在执行软停止时，定义一个时间窗口，用于分散空闲连接的关闭以及活跃连接的关闭过程。接收到 SIGUSR1 信号且宽限期（如有）结束后，若未设置此选项，所有空闲连接将立即全部关闭；而活跃的 HTTP 或 HTTP2 连接将在收到下一个请求后结束，方法是向 HTTP 响应中添加 "Connection: close" 头，或在 HTTP2 情况下发送 GOAWAY 帧。当设置此选项时，连接关闭将在此设定的 `<time>` 时间内逐步进行。若将 close-spread-time 设置为 "infinite"，则在软停止期间将禁用活跃连接的逐步关闭。HTTP 响应中将不再添加 "Connection: close" 头（HTTP2 亦不再发送 GOAWAY 帧），空闲连接仅在达到其超时时间后才会关闭（基于配置中设置的各种超时参数）。

参数：

```text
<time>  是软停止期间分散关闭连接的时间窗口，默认单位为毫秒。
        若要禁用活跃连接的关闭，则设为 "infinite"。
```

若使用了 “hard-stop-after” 选项，建议将此设置的值设为低于该选项所用值，以便在进程停止前，所有连接都有机会优雅关闭。

另请参阅：grace、hard-stop-after、idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

定义一个由同一集群中多个节点共享的 ASCII 字符串密钥。该密钥可用于多种用途。它至少用于为本进程创建的所有 QUIC 连接派生无状态重置令牌。同样，该密钥也用于派生用于加密重试令牌的密钥。

如果未设置此参数，进程启动时将随机选择一个值。这允许使用依赖该值的功能，尽管存在一些限制。

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

在某些操作系统上，可以将线程组或线程绑定到特定的 CPU 集。
这意味着指定的线程将始终仅在指定的 CPU 上运行。“cpu-map” 指令用于为单个线程或线程组指定 CPU 集。第一个参数为线程组范围，可选地后接线程集。这些范围的格式如下：

```text
all | odd | even | number[-[number]]
```

`<number>` 必须是 1 到 32 或 64 之间的数字，具体取决于机器的字长。高于 'thread-groups' 的组 ID 以及超过机器字长的线程 ID 均被忽略。所有线程编号均相对于其所归属的组。可以使用连字符（'-'）分隔两个数字来指定一个范围。也可以使用 "all" 一次性指定所有线程，使用 "odd" 指定奇数线程，或使用 "even" 指定偶数线程，与 "thread" 绑定指令的用法一致。第二个及后续参数为 CPU 集合。每个 CPU 集合要么是起始于 0 的唯一编号（对应第一个 CPU），要么是两个此类编号之间用连字符（'-'）分隔的范围。这些 CPU 编号和范围可通过用逗号分隔或在同一条指令行中添加更多范围来重复指定。在 Linux 和 BSD 以外的操作系统中，最大 CPU 索引可能受限于 31 或 63。可以指定多个 "cpu-map" 指令，但当它们发生重叠时，后续的 "cpu-map" 指令将替换之前的指令。

范围可以部分定义。若省略上限，则用对应的最大值代替，该值为 32 或 64，具体取决于机器的字长。

在线程集前添加前缀 "auto:"，可让 HAProxy 自动通过递增线程和 CPU 集的方式将一组线程绑定到 CPU。该配置有效需满足两个集合的大小相同。无论 CPU 集声明顺序如何，绑定将从最低编号到最高编号依次进行。不支持同时使用带有 "auto:" 前缀的组和线程范围。仅支持一个范围，另一个必须为固定数值。

请注意，组范围仅出于历史原因而受支持。如今，单独的数字表示一个线程组，若未使用线程组，则该数字必须为 1；若指定线程范围或数字，且未使用线程组，则必须在前面加上 "1/"。最后，"1" 严格等同于 "1/all"，表示该组中的所有线程。

示例：

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

定义线程与 CPU 的绑定方式。当前支持以下取值：

- per-core：每个线程将绑定到单个核心的所有硬件线程。
- per-group：每个线程将绑定到该组的所有硬件线程。除非在 "cpu-policy" 中使用了 "threads-per-core 1"，否则这是默认设置。"per-group" 接受一个可选参数，用于指定如何分配 CPU。当 CPU 列表的大小超过每组允许的最大 CPU 数量，需在多个组之间拆分时，额外选项允许选择组如何绑定到这些 CPU：
  - auto：每个线程组仅被分配其专属的、连续的 CPU 核心，且不与其他组共享。这是默认选项，通常更优。
  - loose：每个组仍可使用列表中的任意 CPU。这通常导致更高的竞争，但在某些情况下有助于更好地应对运行在相同 CPU 上的寄生负载。
- auto："per-group" 将被使用，除非在 "cpu-policy" 中使用了 "threads-per-core 1"，此时将使用 "per-core"。这是默认设置。
- per-thread：每个线程仅绑定到一个硬件线程。如果在 "cpu-policy" 中使用了 "threads-per-core 1"，则每个线程将绑定到不同核心的一个硬件线程。
- per-ccx：每个线程将绑定到一个 CCX 的所有硬件线程。

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

选择要使用的 CPU 分配策略。

在多 CPU 系统中，存在多种原因可能导致未使用全部可用的 CPU 核心，或需要将核心分组为不同的线程组，以实现性能、延迟、成本或系统级资源管理的优化。虽然“cpu-set”指令已支持排除部分核心，但完成此操作后，仍需决定如何将剩余核心分配给线程及线程组。

该映射通常通过 "cpu-map" 指令完成，但在异构系统上维护可能尤为困难。

"cpu-policy" 指令用于在未使用 "cpu-map" 时，选择一组有限的分配策略之一。当前支持以下策略，默认策略为 "performance"：

- none 不执行特定的后选择操作。所有启用的 CPU 均可使用；若未设置线程数，将自动设为可用 CPU 数量，但每线程组最多不超过 32 个（32 位系统）或 64 个（64 位系统）。若未设置线程组数量，将设为 1。

- efficiency 与下方的 "group-by-ccx" 完全相同，但会剔除性能高于下一个性能较低核心 25% 以上的 CPU 核心集群。这些通常是“大”核或“性能”核。这意味着，若检测到多种类型的 CPU 核心，仅会使用高效的核心。在中等负载下，这种策略可能有意义，以便为应用程序或安全组件保留最强大的核心。一些现代 CPU 拥有大量此类高效核心，它们可协同提供可观的性能，同时功耗更低。

- first-usable-node：若 CPU 未在启动时被限制（例如使用 "taskset" 工具），且未设置 "nbthread" 指令，则将使用首个启用 CPU 的 NUMA 节点，并以此节点的 CPU 数量作为线程数。将启用单个线程组，包含全部线程，上限为 32 或 64，具体取决于系统。

- group-by-2-ccx：与下方的 "group-by-ccx" 相同，但每两个 CCX 创建一个组。当 CPU 拥有多个 CCX 且每个 CCX 的核心数量较少时，此选项可能有意义，可避免创建过多组，或在并非所有核心均被使用时略微平滑负载分布。请注意，当 CCX 间通信较慢时，可能产生极差的性能影响。通常不建议使用。

- group-by-2-clusters：与 "group-by-cluster" 相同，但每两个集群创建一个组。在每个 CPU 包含多个核心数量较少的集群时，此选项可能有意义，可避免创建过多组，或在并非所有核心均被使用时略微平滑分布。请注意，当集群间通信速度较慢时，可能导致性能显著下降。通常不建议使用。

- group-by-3-ccx：与下方的 "group-by-ccx" 相同，但每三个 CCX 创建一个组。在每个 CCX 核心数量较少的多 CCX CPU 上，这可以避免创建过多组，或在并非所有核心均被使用时略微平滑负载分布。请注意，当 CCX 间通信较慢时，可能产生极差的性能影响。通常不建议使用。

- group-by-3-clusters：与 "group-by-cluster" 相同，但每三个集群创建一个组。在每个集群包含少量核心的 CPU 上，此选项可避免创建过多组，或在并非所有核心均被使用时略微平滑负载分布。请注意，当集群间通信速度较慢时，可能产生极差的性能影响。通常不建议使用。

- group-by-4-ccx：与下方的 "group-by-ccx" 相同，但每四个 CCX 创建一个组。当 CPU 拥有多个 CCX 且每个 CCX 核心数量较少时，此选项可避免创建过多组，或在并非所有核心均被使用时略微平滑负载分布。请注意，当 CCX 间通信较慢时，可能产生极差的性能影响。通常不建议使用。

- group-by-4-clusters：与 "group-by-cluster" 相同，但每四个集群创建一个组。在每个集群包含少量核心的多集群 CPU 上，这可能有意义，以避免创建过多组，或在并非所有核心均被使用时略微平滑分布。请注意，当集群间通信较慢时，可能导致性能显著下降。通常不建议使用。

- group-by-ccx：若未设置 "nbthread" 或 "nbtgroups"，则为每个拥有可用 CPU 的 CPU 核心复合体（"CCX"）创建一个线程组，每个线程组包含的线程数与该 CCX 中的 CPU 数量相同。CCX 将具有类似快速访问最后一级缓存（"LLC"，通常为 L3 缓存）的 CPU 组合在一起。在大多数现代机器上，切勿将来自相距较远 CCX 的 CPU 混入同一线程组，这对性能至关重要。随后，每个线程组的所有线程将绑定到该 CCX 的所有 CPU，以确保组内通信始终局限于 CCX 内部，同时避免强制过强的绑定。每个线程组的线程数限制和线程组数量限制均会被遵守。此配置在多路处理器和 NUMA 系统上，以及具有较差跨 CCX 延迟的 CPU 上被推荐使用。

- group-by-cluster：若未设置 "nbthread" 或 "nbtgroups"，则为每个拥有可用 CPU 的 CPU 集群创建一个线程组，每个线程组包含的线程数与该集群的 CPU 数量相同。线程组内的所有线程均绑定到该集群的所有 CPU，以确保组内通信保持在集群内部，同时避免强制过强的绑定。将尊重每个线程组的线程数限制和线程组限制。在多路处理器和 NUMA 系统上，以及存在较差跨 CCX 延迟的 CPU 上，建议使用此配置。在大多数服务器设备中，集群与 CCX 相同，但在异构机器（如“性能”型与“效率”型，或“大核”与“小核”）上，集群通常仅由 CCX 的一部分组成，且该部分仅包含类型相同、频率差异最大不超过 ±5% 的 CPU。这一差异在现代开发人员和管理员用于验证配置的笔记本电脑和台式机上尤为明显。

- performance 与上述 "group-by-ccx" 完全一致，但会剔除由性能低于下一个更高效核心 80% 的核心组成的 CPU 集群。这类核心通常为“小核”或“高效核”，其加入通常无法带来显著性能提升，反而可能产生反效果（例如 TLS 握手）。通常情况下，将此类核心保留用于网络处理等其他任务更为有效。在开发系统中，也可用于运行辅助工具，如负载生成器和监控工具。这是默认策略。

- resource 此项类似于上述的 "group-by-cluster"，但仅使用最小且最高效的 CPU 集群，其余集群将被忽略。此选项可用于将资源使用量限制在仍能提供良好性能的最低水平，例如用于进一步降低功耗，或在某些租用系统中减少 sidecar 部署所需的内核数量，以便更轻松地缩减系统规模。请注意，若仅存在单一集群，该集群仍会被完全使用。

可选关键字 "threads-per-core" 可被添加。该关键字可接受两个值："1" 和 "auto"。若设置为 "1"，则每个核心仅创建一个线程，无论该核心具有多少个硬件线程。若设置为 "auto"，则每个硬件线程将创建一个线程。若未指定亲和性，且使用 threads-per-core 1，则默认亲和性为按核心。

另请参阅： "cpu-map"、"cpu-set"、"nbthread"

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

允许以符号方式描述运行的 CPU 集合。该指令支持以下关键字： - reset：重置，取消任何先前可能由服务管理器或 "taskset" 命令等继承的限制。 - drop-cpu `<set>`：不绑定到该集合中的 CPU。 - only-cpu `<set>`：不绑定到该集合外的 CPU。 - drop-node `<set>`：不绑定到该 NUMA 节点中的 CPU。 - only-node `<set>`：不绑定到不属于该 NUMA 节点的 CPU。 - drop-cluster `<set>`：不绑定到该硬件集群编号的 CPU。 - only-cluster `<set>`：不绑定到其他硬件集群编号的 CPU。 - drop-core `<set>`：不绑定到该硬件核心编号的 CPU。 - only-core `<set>`：不绑定到其他硬件核心编号的 CPU。 - drop-thread `<set>`：不绑定到该硬件线程编号的 CPU。 - only-thread `<set>`：不绑定到其他硬件线程编号的 CPU。

另请参阅："cpu-policy"

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

当使用 `crtfile` 或 `crt` 指令并指定相对路径时，指定用于获取 SSL 证书的默认目录。绝对路径配置优先，且会忽略 `crt-base`。

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

使进程在后台运行。这是推荐的运行模式。其效果等同于命令行参数 "-D"。可通过命令行参数 "-db" 禁用。在 systemd 模式下，此选项将被忽略。

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

默认情况下，HAProxy 会从进程启动位置加载所有由相对路径指定的文件。在某些情况下，可能需要强制所有相对路径从另一个位置开始，如同进程从该位置启动一般。此指令即为此目的而设计。技术上，HAProxy 在处理每个配置文件期间，会临时将工作目录切换至指定位置，处理完成后返回原始目录。该指令接收一个参数，用于指定加载路径不以斜杠（'/'）开头的文件时所采用的策略：- "current" 表示所有相对路径文件均从进程启动目录加载；这是默认行为。

    - "config"：所有相对路径文件均从配置文件所在目录加载。具体而言，若配置文件路径
      包含斜杠（'/'），则切换至最后一个斜杠及其之前的完整路径；否则使用当前目录。
      此模式便于将映射、错误页面文件、证书和 Lua 脚本打包为可整体移动的软件包。
      加载多个配置文件时，会为每个配置文件更新工作目录。

    - "parent"：所有相对路径文件均从配置文件所在目录的父目录加载。具体而言，若
      配置文件路径包含斜杠（'/'），则在最后一个斜杠及其之前的完整路径后追加 ".."，
      并切换至该目录；否则使用目录 ".."。此模式便于将映射、错误页面文件、证书和
      Lua 脚本打包为可整体移动的软件包，同时将各部分放在不同子目录中
      （例如 "config/"、"certs/"、"maps/" 等）。

    - "origin"：所有相对路径文件均从指定路径加载，该路径为必填参数。这可简化
      同一系统中并行运行的多个 HAProxy 实例的管理：各实例使用不同的路径前缀，
      其余配置段则可方便地随之移动。

每个 "default-path" 指令会立即替换之前的指令，并可能导致切换到不同的目录。虽然这通常能产生预期的行为，但使用多个 default-path 指令并非良好实践；若确实使用，应确保所有配置文件中的策略保持一致。

请注意：某些配置元素（如映射或证书）通过其配置路径进行唯一标识。采用可重定位布局后，多个元素可能产生相同的唯一名称，导致运行时更新变得困难，尤其是在从不同目录加载多个配置文件时。在采用相对路径之前，必须遵循严格的无冲突文件命名方案。一种稳健的做法是为所有文件名添加各自的站点名称前缀，或在目录级别实施该策略。

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

添加一段描述实例的文本。

请注意，必须转义某些字符（例如 #），且该文本将插入 HTML 页面，因此应避免使用 "\<" 和 "\>" 字符。

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

设置 API 加载的 DeviceAtlas JSON 数据文件路径。路径必须指向一个有效的 JSON 数据文件，且 HAProxy 进程可访问。

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

设置 API 返回信息的级别。该指令为可选指令，若未设置，默认值为 0。

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

设置用于检测请求期间是否使用了 DeviceAtlas 客户端组件的客户端 Cookie 名称。该指令为可选指令，若未设置，默认值为 DAPROPS。

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

设置 API 属性结果的字符分隔符。该指令为可选指令，若未设置，默认值为 \|。

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

默认情况下，DNS 解析器接受 IPv4 和 IPv6 地址。这一行为可通过服务器行上的 "resolve-prefer" 关键字以及 "do-resolve" 动作的 family 参数进行影响，但这些仅表示偏好，不会阻止在仅存在一种地址族时使用另一种。在某些双栈不可用的环境中，遇到仅支持 IPv6 的不可达 DNS 记录可能导致严重问题，因为它会替换此前本可继续工作到下一次请求的 IPv4 记录。全局选项 "dns-accept-family" 允许强制仅使用一种（或两种）地址族。该参数为以下单词的逗号分隔列表：- "ipv4"：查询并接受 IPv4 地址（"A" 记录） - "ipv6"：查询并接受 IPv6 地址（"AAAA" 记录） - "auto"：优先使用 IPv4，若系统存在默认网关则同时使用 IPv6。最后一次检查结果将被缓存 30 秒。

当仅使用单一地址族时，不会向解析器发送其他地址族的请求，且任何来自其他地址族的响应都将被忽略。自 3.3 版本起，默认值为 "auto"，该值在确认 IPv6 可路由后，会自动启用两个地址族；否则将仅使用 IPv4。另请参见："resolve-prefer"、"do-resolve"

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

此语句必须在使用某些标记为已弃用的指令之前出现，以消除警告并确保配置文件不会被拒绝。并非所有已弃用的指令都受此影响，仅限于没有替代解决方案的指令。

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

此指令必须在使用标记为实验性的指令之前出现，否则配置文件将被拒绝。请注意，受此选项涵盖的功能无法保证运行良好，可能在维护周期内发生中断。在下一个版本开发期间，开发者将以尽力而为的方式维护这些功能，并会采取合理措施避免其中断，但不作任何保证。因此，这些功能预期不会在下一个 LTS 版本发布后继续得到支持。希望尝试实验性功能的用户应尽快升级，以受益于该功能的改进。要判断此指令是否仍有必要，方法很简单：若该指令已启用但未被任何此类功能使用，系统将发出警告，建议将其关闭。因此，若无任何警告，则说明该指令仍需保留。

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

允许使用外部代理执行健康检查。出于安全考虑，默认情况下此功能已禁用。即使启用，若未同时启用“insecure-fork-wanted”，健康检查仍可能失败。如果所启动的程序使用了 setuid 可执行文件（实在不应如此），还可能需要在全局段中设置“insecure-setuid-wanted”。默认情况下，健康检查以干净环境启动，仅包含后端段中“external-check”命令定义的变量。在某些情况下，保留环境变量可能是有益的，例如当复杂脚本从环境中获取额外路径或信息时。可通过附加“preserve-env”关键字实现此目的。但在此情况下，强烈建议不要以 setuid 方式运行或以特权用户身份运行，以免检查程序暴露于潜在攻击。详见“option external-check”、“insecure-fork-wanted”和“insecure-setuid-wanted”获取更多细节。

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

设置进程所使用的文件描述符数量的上限，该上限不受系统限制的影响。尽管可使用 "ulimit-n" 和 "maxconn" 来强制设定值，但当二者未设置时，进程将受限于由 "ulimit -n -H" 报告的 RLIMIT_NOFILE 硬限制。然而，一些现代操作系统现在允许在此处设置极高的数值（高达十亿量级），这将导致常规使用场景下消耗过多内存。为此提供了 fd-hard-limit 设置，用于为此限制设置一个可能更低的上限。这意味着当系统施加的限制低于 `<number>` 时，将始终尊重系统限制；而当系统限制高于该值时，则使用指定的值。默认情况下，fd-hard-limit 设置为 1048576。该默认值可通过 DEFAULT_MAXFD 编译时变量进行修改，若 RLIMIT_NOFILE 硬限制极高，该变量可作为最大（内核）系统限制。在全局段中设置的 fd-hard-limit 可临时覆盖通过 DEFAULT_MAXFD 构建时提供的值。在以下示例中，未指定其他设置，maxconn 值将自动适应 "fd-hard-limit" 与 RLIMIT_NOFILE 限制中的较低者：

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

另请参阅：ulimit-n、maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

将进程的组 ID 更改为 `<number>`。建议该组 ID 专用于 HAProxy 或少量相似的守护进程。HAProxy 必须以属于该组的用户身份启动，或以超级用户权限启动。请注意，若 HAProxy 从具有附加组的用户启动，则仅当以超级用户权限启动时，才能移除这些附加组。另请参见“group”和“uid”。

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

定义 SIGUSR1 与实际软停止之间的延迟。

参数：

```text
<time>  是收到 SIGUSR1 信号后、开始执行软停止之前额外等待的延迟，默认单位为毫秒。
```

用于与旧式环境兼容，即在需要停止 HAProxy 进程时，某些外部组件需在监听器解除绑定前检测其状态。其原理是，内部 "stopping" 变量（由“stopping”样本提取函数报告）将被设为 true，但监听器将继续正常接收连接，直至延迟期结束，之后才执行常规的软停止。此机制不得与需要重载的进程一同使用，否则可能导致旧进程无法解除绑定，也可能阻止新进程启动，或引发其他问题。

示例：

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

请注意，更灵活且持久的方法是，由编排系统通过 CLI 设置全局变量，使用该变量响应外部检查，延迟后发送 SIGUSR1 信号。

示例：

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

另请参阅：hard-stop-after、monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

与 "gid" 类似，但使用 /etc/group 中组名 `<group name>` 对应的 GID。另请参阅 "gid" 和 "user"。

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

不拒绝携带有效载荷的 HTTP/1.0 GET/HEAD/DELETE 请求，不返回 413 Payload Too Large HTTP 响应。

尽管 HTTP/1.1 明确允许，但 HTTP/1.0 在此问题上表述不清，部分旧版服务器不期望存在有效载荷，且从不检查正文长度（通过 Content-Length 或 Transfer-Encoding 头）。这意味着某些中间设备可能正确处理 HTTP/1.0 的 GET/HEAD/DELETE 请求的有效载荷，而另一些则可能完全忽略。这可能导致安全问题，因为存在请求走私攻击的风险。因此，默认情况下，HAProxy 会拒绝带有有效载荷的 HTTP/1.0 GET/HEAD/DELETE 请求。

然而，某些旧版客户端可能存在兼容性问题。在此情况下，可设置此全局选项。

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

根据 HTTP/1.1 规范（RFC9112#6.1）规定，若同一消息中同时存在 Transfer-Encoding 头字段和 Content-Length 头字段，则当上游或下游链路中存在任何 HTTP/1.0 代理时，可能引发内容走私攻击，此时代理必须在响应后绝对关闭连接，以防止被利用。但此行为可能对某些非常老旧的客户端造成性能影响，尤其是当它们需为每个请求重新协商 TLS 连接时。该选项用于指示 HAProxy 不强制执行此规则，仅对消息进行净化处理，响应后保持连接存活。此操作仅在完全确定链路中不存在任何 HTTP/1.0 代理，且 HAProxy 之前的所有实现均完全符合 HTTP/1.1 规范中关于这些头字段的规则时方可进行。无论如何，HAProxy 仍将继续忽略并丢弃多余的 Content-Length 头，以避免对下一跳造成混淆。

当启用此选项以绕过旧版存在缺陷的客户端或服务器时，必须理解，无论是否需要该选项，此类违反规则的代理均存在风险：其消息可能被旧版代理截断，因为这些旧版代理会依据 Content-Length 字段并忽略 Transfer-Encoding，而未考虑编码块大小的累计值。因此，上述规则不仅关乎安全，也涉及清除可能因与旧版代理不兼容而导致通信故障的代理。

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

定义启用时对头名称 `<from>` 执行的大小写调整，将其转换为 `<to>` 后再发送至 HTTP/1 客户端或服务器。`<from>` 必须为小写，`<from>` 与 `<to>` 除大小写外不得存在差异。若需调整多个头名称，可重复使用该指令。禁止重复条目。若需调整的头名称较多，建议使用 "h1-case-adjust-file"。请注意，除非在代理中指定 "option h1-case-adjust-bogus-client" 或 "option h1-case-adjust-bogus-server"，否则不会应用任何转换。

由于 RFC7230 明确指出，头名称没有标准大小写形式，因此其大小写不敏感。
应用程序必须以不区分大小写的方式处理头名称。
但某些不合规的应用程序违反标准，错误地依赖浏览器通常使用的大小写形式。
这一问题在 HTTP/2 中变得尤为关键，因为所有头名称必须以小写形式传输，HAProxy 也遵循相同约定。
无论 HTTP 版本为何，所有头名称均以小写形式发送至客户端和服务器。

某些无法正确处理请求或响应的应用程序可能需要暂时使用此类变通方法，以调整发送给它们的头名称，直至应用程序修复为止。请注意，需要此类变通方法的应用程序可能易受内容走私攻击，必须绝对予以修复。

示例：

```text
global
  h1-case-adjust content-length Content-Length
```

参见“h1-case-adjust-file”、“option h1-case-adjust-bogus-client”和“option h1-case-adjust-bogus-server”。

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

定义一个包含键/值对列表的文件，用于在将某些头名称发送给 HTTP/1 客户端或服务器之前调整其大小写。文件 `<hdrs-file>` 每行必须包含两个头名称。第一个必须为小写，且两者除大小写外不得有任何差异。以 '#' 开头的行将被忽略，空行亦然。行首和行尾的制表符及空格将被去除。不允许重复条目。请注意，除非在代理中指定了 "option h1-case-adjust-bogus-client" 或 "option h1-case-adjust-bogus-server"，否则不会应用任何转换。

如果重复使用此指令，仅最后一个会被处理。当需要调整大量头名称时，可将其作为指令 "h1-case-adjust" 的替代方案。请阅读使用此功能相关的风险。

参见“h1-case-adjust”、“option h1-case-adjust-bogus-client”和“option h1-case-adjust-bogus-server”。

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

禁用向客户端通告对 h2 WebSocket 的支持。此设置可用于解决部分客户端在实现相对较新的 RFC8441 时出现的问题，例如 Firefox 88。若要允许客户端在 WebSocket 隧道中自动降级至 http/1.1，请在 bind 语句中通过指定 "alpn" 来启用 h2 支持，无需显式使用 "proto" 关键字。若此前已启用此设置，可通过在关键字前添加 "no" 来禁用。

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

定义允许执行干净的软停止的最大时间。

参数：

```text
<time>  是通过 SIGUSR1 信号收到软停止请求后，实例允许继续存活的最长时间，默认单位为毫秒。
```

这可用于确保实例在执行软停止时即使仍有连接保持打开也会退出（例如，当代理以 TCP 模式运行且超时时间较长时）。该设置在 TCP 模式和 HTTP 模式下均适用。

示例：

```text
global
  hard-stop-after 30s
```

另请参见：grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

启用按协议的保护机制，禁止与使用特权端口作为源端口的客户端通信。该端口范围依据 RFC 6335 定义。默认情况下，QUIC 协议的保护机制处于激活状态，因为此类行为具有可疑性，可能被用于伪造攻击或 DNS/NTP 放大攻击。

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

替换、减少或扩展定义为错误的状态码列表，这些错误将被计入终止码以及粘性表中的 "http_err_cnt" 计数器。默认的错误范围为 400 至 499，但在某些场景下，部分用户希望排除特定状态码，尤其是在追踪客户端错误时（例如，动态生成内容的系统中的 404）。另请参阅 "http-fail-codes" 和 "http_err_cnt"。

指定范围时若不包含 '+' 或 '-'，则将现有范围重新定义为新范围。以 '+' 开头的范围将扩展现有范围，使其包含指定范围，该范围可能与现有范围重叠，也可能不重叠。以 '-' 开头的范围将从现有范围中移除指定范围。范围由 100 至 599 之间的数字组成，可选地后接连字符 '-' 及另一个大于或等于首个数字的数字，用于表示范围的上限。同一 add/del/replace 操作中可使用逗号分隔多个范围。

示例：

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

替换、减少或扩展由终止码及粘性表中的 "http_fail_cnt" 计数器所定义的失败状态码列表。默认的失败状态码范围为 500 至 599，但排除 501 和 505，因为它们可能由客户端触发，通常表示服务器无法处理请求。部分用户在特定场景下希望排除某些状态码，例如在特定 SOAP 环境中排除 500，因为该状态码在该环境中并不表示服务器故障。语法与上文的 http-err-codes 完全相同。另请参见 "http-err-codes" 和 "http_fail_cnt"。

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

默认情况下，HAProxy 在启动后会尽力防止任何线程和进程的创建。在使用来源不明的 Lua 文件，或试验仍可能包含漏洞的开发版本时，这一点尤为重要，因为这些漏洞的可利用性尚不明确。总体而言，确保流量无法触发任何意外的后台活动，是一种良好的系统管理习惯。但此机制会阻止外部检查正常工作，也可能破坏某些特定的 Lua 脚本，这些脚本依赖于 fork 能力。该选项用于禁用此保护机制。请注意，禁用此保护机制是不良做法，因为一旦禁用，库或 HAProxy 本身中的漏洞将更容易被利用。此外，从 Lua 或其他任何位置进行 fork 操作并不可靠，因为子进程可能随机继承其他线程设置的锁，从而无法完成操作。因此，强烈建议永远不要使用此选项，并重新评估任何需要此类 fork 的工作负载，改用更安全的解决方案（例如使用代理程序替代外部检查）。该选项支持使用 "no" 前缀来禁用。也可通过在 HAProxy 命令行中使用 "-dI" 激活。

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

HAProxy 无需在运行时调用可执行文件（使用外部检查时除外，但强烈建议避免使用），且应默认将其自身隔离至空的 chroot 环境中。因此，几乎不存在允许调用 setuid 可执行文件而不让用户充分知晓风险的合理理由。当 HAProxy 需要调用外部检查和/或禁用 chroot 时，若库或 HAProxy 本身存在漏洞，可能导致外部程序被执行。在 Linux 系统上，可将进程锁定，使此类可执行文件上存在的 setuid 位被忽略。这能显著降低此类情况下的权限提升风险。HAProxy 默认执行此操作。若该行为导致外部检查出现问题（例如需要调用 "ping" 命令），则可通过在 global 段中显式添加该指令来禁用此保护。启用后，可通过在指令前添加 "no" 关键字将其重新关闭。

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

指定用于加载证书链以完成颁发者信息的目录。所有文件必须采用 PEM 格式。对于使用 "crt" 或 "crt-list" 加载的证书，若 PEM 文件中未包含证书链（也称为中间证书），当证书的颁发者与通过 "issuers-chain-path" 加载的链中首个证书相匹配时，HAProxy 将自动补全证书链。一个包含 PrivateKey+Certificate+IntermediateCA2+IntermediateCA1 的 "crt" 文件可替换为仅包含 PrivateKey+Certificate 的文件。若在 "issuers-chain-path" 目录中存在包含 IntermediateCA2+IntermediateCA1 的文件，HAProxy 将自动补全证书链。所有具有相同颁发者的其他证书将在内存中共享该证书链。

OCSP 功能可在未使用 .issuer 或 PEM 中未提供证书链时，使用完整的证书链。

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

允许 'jwt_verify' 转换器接受使用 "none" 算法的 JWT 令牌。设置此选项后，这些令牌始终被视为有效。
默认拒绝未签名的令牌，因为它们被认为不安全（参见 RFC8725
[第 3.1 节](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)）。

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

设置 jwt_decrypt_XXX 转换器中允许使用的算法列表。使用不支持或已禁用算法的 JWT 令牌将永远无法解密。指定的算法必须与 RFC7518 [第 4.1 节](https://www.rfc-editor.org/rfc/rfc7518#section-4.1) 中的格式一致，且以冒号分隔。特殊名称 "ALL" 可用于启用所有支持的算法（详见 "jwt_decrypt_jwk" 转换器以获取完整列表），也可在算法名称后附加 "!" 以显式禁用该算法。请注意，除非明确指定 "ALL"，否则使用此选项将禁用未在所提供列表中明确列出的任何算法。

示例：

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

设置 jwt_decrypt_XXX 转换器中允许的加密算法列表。使用不支持或已禁用的加密算法的 JWT 令牌将永远无法解密。指定的算法必须与 RFC7518 [第 5.1 节](https://www.rfc-editor.org/rfc/rfc7518#section-5.1) 中的格式一致，且以冒号分隔。特殊名称 "ALL" 可用于启用所有支持的算法（详见 "jwt_decrypt_jwk" 转换器以获取完整列表），也可在算法名称后附加 "!" 以显式禁用该算法。请注意，除非明确指定 "ALL"，否则使用此选项将禁用未在所提供列表中明确列出的任何算法。

示例：

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

当 "key" 指令使用相对路径时，指定获取 SSL 私钥的默认目录。若指定绝对路径，则优先生效并忽略 "key-base"。此选项仅在使用 crt-store 加载行时有效。

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

此设置必须用于在 HAProxy 编译时使用不支持 QUIC 的 OpenSSL 版本的情况下显式启用 QUIC 监听器绑定。它会激活 HAProxy 内部兼容性层，该层必须在构建时通过 USE_QUIC_OPENSSL_COMPAT=1 选项选定。此兼容性层支持大部分必要的 TLS 操作，但不支持 QUIC 0-RTT 功能。

此功能主要针对 OpenSSL 3.5.2 之前版本，因为这些版本尚未实现 QUIC API 或仅部分实现。尽管可在 3.5.2 及以上版本中仍激活兼容层，但此举可能并无必要。

若设置了 limited-quic 但构建时未选择兼容层，则该选项将被静默忽略，QUIC TLS 操作将依赖 TLS 库。

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

设置本地实例的对等节点名称。若指定了 "-L" 命令行参数，或在 "peers" 段定义之后使用，该设置将被忽略。在此情况下，配置解析期间将发出警告消息。

此选项还将设置 HAPROXY_LOCALPEER 环境变量。另请参阅管理指南中的 "-L" 以及下方的 "peers" 段。

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

添加一个全局 syslog 服务器。可以定义多个全局服务器。它们将接收进程启动和退出时的日志，以及所有配置了“log global”的代理产生的日志。有关更多详细信息，请参阅代理的“log”选项。

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

设置 syslog 头中的主机名字段。若设置了可选的“string”参数，头字段将设为字符串内容；否则使用系统的主机名。通常在未通过中间 syslog 服务器转发日志时使用，或用于自定义日志中打印的主机名。

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

将 syslog 头中的标签字段设置为该字符串。默认值为从命令行启动时的程序名称，通常为 "haproxy"。在同一个主机上运行多个进程时，有时需要区分它们。另请参见代理级别的 "log-tag" 指令。

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

此全局指令在共享上下文中加载并执行 Lua 文件，该上下文对所有线程可见。在该上下文中设置的任何变量均可被任意线程访问。这是加载 Lua 程序最简单且推荐的方式，但如果执行大量 Lua 调用，其扩展性将不佳，因为同一时间只有一个线程能在全局状态上运行。以这种方式加载的程序始终在 "core.thread" 变量中看到 0。该指令可多次使用。

可通过以下代码在 Lua 文件中访问参数。请注意，Lua 数组的索引从 1 开始。在文件中声明的“local”变量在整个文件中可用，但对其他文件不可见。

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

此全局指令将 Lua 文件加载并执行到每个启动的线程中。任何全局变量均具有线程局部可见性，因此每个线程可看到不同的值。因此强烈建议在通过此方式加载的程序中不要使用全局变量。每个线程都会加载并初始化一份独立副本，所有操作按顺序执行，且按线程编号从 1 到 nbthread 依次进行。若某些操作仅需执行一次，程序应检查 "core.thread" 变量以确定当前正在初始化的线程。通过此方式加载的程序将在所有线程上并发运行，具有高度可扩展性。这是推荐的加载简单函数的方式，用于注册样本提取、转换器、动作或服务，前提是已确认程序不依赖全局变量。为简化使用，即使仅使用一个线程或线程功能被禁用时，该指令依然可用（此时等效于 lua-load）。该指令可多次使用。

请参阅 lua-load 了解 args 的使用方法。

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

在 Lua 的 package.`<type>` 变量前添加指定字符串，并以分号结尾。`<type>` 必须为 "path" 或 "cpath"。若未指定 `<type>`，则默认值为 "path"。

Lua 的路径是用分号分隔的模式列表，用于指定 `require` 函数查找库源文件的方式。模式中的问号（?）将被模块名替换。路径按从左到右的顺序进行评估，这意味着后续添加的路径将优先被检查。

以指定以下路径为例：

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

当调用 `require "example"` 时，Lua 会首先尝试加载 /usr/share/haproxy-lua/example.lua 脚本，若该脚本不存在，则尝试加载 /usr/share/haproxy-lua/example/init.lua，若仍不存在，则尝试默认路径。

请参阅 <https://www.lua.org/pil/8.1.html> 以获取 Lua 文档中的详细信息。

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

主进程/工作进程模式。其效果等同于命令行参数 "-W"。

此关键字已弃用，请使用“-W”或“-Ws”以主进程/工作进程模式启动。

此模式将启动一个“主进程”，在读取配置后，由其派生一个“工作进程”来处理流量。主进程用作进程管理器，负责监控“工作进程”。

使用此模式时，可通过向主进程发送 SIGUSR2 信号直接重载 HAProxy。
重载操作将使主进程重新读取配置并派生新的工作进程。旧的工作进程将保留至其当前任务完成为止。

主进程/工作进程模式与前台模式或守护进程模式均兼容。

默认情况下，如果某个工作进程以错误的返回码退出（例如发生段错误），所有工作进程将被终止，主进程也将退出。建议在 systemd 单元文件中结合使用 Restart=on-failure，以便重新启动整个进程。若不希望出现此行为，必须使用关键字 "no-exit-on-failure"。

另请参见管理指南中的 "-W"。

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

在主进程/工作进程模式下，默认情况下，若某个工作进程以错误的返回码退出（例如发生段错误），所有工作进程将被终止，主进程也将退出。建议在 systemd 单元文件中结合使用 Restart=on-failure，以便重新启动整个进程。

此关键字可在工作进程崩溃时保持其余进程运行，而非终止所有进程。使用时需谨慎，因为该功能仅用于调试，可能导致主进程进入异常状态。

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

定义线程组中的最大线程数。除非使用 "thread-groups" 指令固定线程组数量，否则 HAProxy 会创建足够多的线程组以满足所请求的线程数量。最小值为 1，最大值为 64（在 64 位系统上），或 32（在 32 位系统上）。较低的值可减少由共享状态上的原子操作引起的竞争，但可能增加创建所有监听器和保持空闲后端连接所需的套接字数量。较高的值可降低这些开销，但会带来更高的 CPU 使用率（在竞争情况下），以及更低的连接速率。默认值为 16，该值是在多种测试系统（包括来自多个厂商的 x86_64 处理器，以及裸金属和虚拟化环境中的大型 Arm64 系统）上通过实验得出的最佳权衡。

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

在主进程/工作进程模式下，此选项用于限制工作进程可存活跨越的重载次数。若工作进程在重载后未退出，且其重载次数超过此数值，该工作进程将收到 SIGTERM 信号。此选项有助于控制工作进程的数量。参见管理指南中的“show proc”。

默认情况下，该值设为 50。

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

此设置仅在编译时启用了线程支持的情况下可用。它使 HAProxy 在 `<number>` 个线程上运行。“nbthread” 在 HAProxy 以前台模式启动时同样有效。在部分支持 CPU 亲和性的平台上，启动时默认的 “nbthread” 值会自动设置为进程绑定的 CPU 数量。这意味着可通过 “taskset” 或 “cpuset” 等命令从调用进程轻松调整线程数量。否则，该值默认为 1。默认值会在 "haproxy -vv" 的输出中报告。请注意，此处设置或自动检测的值受 “thread-hard-limit”（若已设置）的限制。

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

在运行于支持 NUMA 的平台时，此选项可使 "cpu-policy" 指令检查拓扑结构，从而确定最佳的 CPU 集合及对应的线程数量。然而，若在特定架构上应用的绑定并非最优，可通过指令 'no numa-cpu-mapping' 禁用此自动绑定。若配置中存在 'nbthread' 指令，或进程亲和性已通过 'cpu-map' 指令或 taskset 工具指定，或 'cpu-policy' 设置为其他值，则不会应用此自动绑定。参见 "cpu-map"、"cpu-policy"、"cpu-set"。

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

完全禁用 HAProxy 中的 ocsp-update 功能。任何 ocsp-update 配置都将被忽略。
默认值为 "off"。有关自动更新机制的更多信息，请参见选项 "ocsp-update"。

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

允许通过 HTTP 代理进行 OCSP 更新。此选项仅适用于 HTTP，不支持 HTTPS。

此选项将允许 OCSP 更新程序在向代理发送请求时使用绝对 URI。

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

设置同一 OCSP 响应自动更新之间的最大间隔时间。该时间以秒为单位，缺省值为 3600（1 小时）。必须设置为高于 "ocsp-update.mindelay" 的值。有关自动更新机制的更多信息，请参见选项 "ocsp-update"。

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

设置同一 OCSP 响应两次自动更新之间的最小间隔。该时间以秒为单位，缺省值为 300（5 分钟）。对于没有明确过期时间的 OCSP 响应尤为有用。必须设置为低于 "ocsp-update.maxdelay" 的值。有关自动更新机制的更多信息，请参见选项 "ocsp-update"。

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

设置配置中所有证书的默认 ocsp-update 模式。此全局选项可被 crt-list 的 "ocsp-update" 选项覆盖。该选项默认设置为 "off"。有关自动更新机制的更多信息，请参见选项 "ocsp-update"。

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

将所有守护进程的 PID 写入文件 `<pidfile>`，在守护进程模式下；或在主进程/工作进程模式下，将主进程的 PID 写入文件 `<pidfile>`。此选项等效于命令行参数 "-p"。写入文件必须对启动进程的用户可访问。另请参见 "daemon" 和 "master-worker"。

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

PROXY 协议 v2 实现中的一个缺陷存在于 HAProxy 2.1 及更早版本中，导致其在执行健康检查时发出 PROXY 命令而非 LOCAL 命令。该问题影响较小，但会干扰部分服务器的日志记录。遗憾的是，该缺陷发现较晚，且已发现某些可能仅在 HAProxy 上测试过其 PROXY 协议实现的服务器无法正确处理 LOCAL 命令，当 HAProxy 执行健康检查时，这些服务器将永久处于“down”状态。发生此情况时，可启用此全局选项，暂时恢复旧版（错误）行为，直至联系受影响组件的厂商并完成修复。该选项默认禁用，且对所有包含 "send-proxy-v2" 语句的服务器生效。

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

将环境变量 `<name>` 设置为值 `<value>`。若该变量已存在，则不会被覆盖。更改立即生效，使得配置文件中的下一行可读取新值。另请参见 "setenv"、"resetenv" 和 "unsetenv"。

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

执行一次最大文件描述符的打开操作，从而预先分配内核的数据结构。当 nbthread > 1 且 HAProxy 打开文件描述符时，可避免内核扩展数据结构所导致的短暂停顿。

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

移除所有环境变量，仅保留参数中指定的变量。此操作可在使用 setenv 或 unsetenv 设置新值前，创建一个干净且受控的环境。请注意，某些内部函数可能依赖特定环境变量，例如时间操作函数、OpenSSL 或外部检查功能。必须谨慎使用，且仅在完成全面验证后方可执行。更改立即生效，因此配置文件中的下一行将立即看到新的环境状态。参见“setenv”、“presetenv”和“unsetenv”。

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

指定在所有不以 '/' 开头的服务器状态文件名前添加的目录前缀。参见 "server-state-file"、"load-server-state-from-file" 和 "server-state-file-name"。

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

指定包含服务器状态的文件路径。若路径以斜杠（'/'）开头，则视为绝对路径；否则视为相对于通过 "server-state-base" 指定的目录（若已设置）或当前目录。在重载 HAProxy 前，可使用统计信息命令 "show servers state" 保存服务器的当前状态。该命令的输出必须写入 `<file>` 所指向的文件。启动时，在处理流量之前，HAProxy 将读取、加载并应用文件中所列且当前运行配置中可用的每个服务器的状态。参见 "server-state-base" 和 "show servers state"、"load-server-state-from-file" 以及 "server-state-file-name"

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

此选项用于在进程崩溃时选择核心转储行为。可用选项包括：

- on：若此前核心转储已被禁用，则在进程级别启用核心转储。

- off：禁用之前已启用的核心转储功能。

- libs：此选项启用核心转储，并嵌入用于调试所必需的二进制文件和库的副本。开发者可能要求启用此功能。启用后，HAProxy 将尝试将所依赖的库加载到内存中并予以保留。若进程崩溃，这些库将被转储至核心文件，无需再从文件系统中获取，也避免了库版本不匹配的风险。此功能会额外占用数兆字节至数十兆字节的内存，因此在小型系统上应避免使用。

此选项应默认禁用，仅在开发人员请求时启用。默认情况下处于禁用状态。若未指定参数，其默认值为“on”。若已启用，仍可通过在前缀添加“no”关键字或将其设置为“off”来强制禁用。该选项对性能或稳定性无影响，但会尽力重新启用可能因文件大小限制（ulimit -f）、核心文件大小限制（ulimit -c）或进程更改 UID/GID 后的“可转储性”（如 /proc/sys/fs/suid_dumpable 在 Linux 上）而被禁用的核心转储。核心转储仍可能受当前目录权限限制（请检查文件启动目录）、chroot 目录权限限制（可能需要临时禁用 chroot 指令或将其移至专用可写位置），或其他系统特定约束。例如，某些 Linux 发行版以一个系统上甚至未安装的可执行文件路径替换默认核心文件（请检查 /proc/sys/kernel/core_pattern）。通常，仅需将核心文件名设为“core”、“core.%p”或“/var/log/core/core.%p”即可解决该问题。在尝试启用此选项以等待罕见问题重现时，建议首先通过向“HAProxy”进程发送“kill -11”等命令来尝试获取核心转储，并验证其在进程终止时是否按预期生成。

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

设置进程级变量 `<var-name>` 为样本表达式 `<expr>` 的计算结果。变量 `<var-name>` 必须为进程级变量（使用 'proc.' 前缀）。其行为与 TCP 或 HTTP 规则中的 'set-var' 动作完全相同，但表达式在配置解析时即被计算，且变量立即被设置。表达式中允许使用的样本提取函数和转换器仅限于使用内部数据的类型，通常为 'int(value)' 或 'str(value)'。也可引用先前分配的变量。这些变量随后可在常规规则集中读取（及修改）。

示例：

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

设置进程级变量 `<var-name>` 为日志格式 `<fmt>` 求值后得到的字符串。变量 `<var-name>` 必须为进程级变量（使用 'proc.' 前缀）。其行为与 TCP 或 HTTP 规则中的 'set-var-fmt' 动作完全相同，但表达式在配置解析时即被求值，且变量立即被设置。表达式中允许使用的样本提取函数和转换器仅限于使用内部数据的类型，通常为 'int(value)' 或 'str(value)'。也可引用先前分配的变量。这些变量随后可在常规规则集中读取（及修改）。有关自定义日志格式语法的详细信息，请参见 [第 8.2.6 节](/zh/haproxy/configuration-logging/#section-8-2-6)。

示例：

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

设置在以非 root 用户（uid > 0）身份启动和运行，或以 uid 0（root）身份启动后切换至非 root 用户时必须保留的一组能力。默认情况下，uid 切换会导致所有权限丢失，但在透明代理过程中尝试从外部地址连接服务器，或绑定低于 1024 的端口时（例如使用 "tune.quic.fe.sock-per-conn default-on"），通常仍需保留部分权限，从而导致完全以 uid 0 运行的配置。设置能力通常更安全，因为仅保留所需的能力。该功能为操作系统特定功能，仅在构建时设置 USE_LINUX_CAP=1 时于 Linux 上启用。支持的能力列表取决于操作系统，当传递无效或空的能力名称时，错误消息中会列出可用的能力。可传递多个能力，以逗号分隔。常用能力中，"cap_net_raw" 允许透明绑定至外部地址，"cap_net_bind_service" 允许绑定至特权端口，可能被 QUIC 使用。若进程以相同非 root 用户身份启动和运行，所需能力应通过 setcap 在 HAProxy 二进制文件上设置，并配合此关键字使用。关于在 HAProxy 二进制文件上设置能力的详细信息，请参见管理指南第 13.1 节 Linux 能力支持。

示例：

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

将环境变量 `<name>` 设置为值 `<value>`。若该变量已存在，则将其覆盖。
更改立即生效，因此配置文件中的下一行将看到新值。
另请参见“presetenv”、“resetenv”和“unsetenv”。

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

当设置此指令时，将启用共享内存以存储统计信息计数器。`<name>` 用作 shm_open() 的参数，以在唯一位置打开共享内存。这也意味着该指令仅在支持 shm_open() 的系统上可用。当使用 SHM 存储统计信息时，所有前端、后端、监听器和服务器的可共享计数器将存储在 SHM 中，前提是它们已设置 GUID。重载 HAProxy 时，新进程将尝试扫描 SHM，查找可基于 GUID 和类型与配置中定义的对象关联的对象，目标是实现重载后部分计数器值的保留。另一方面，当 HAProxy 正常停止时，SHM 对象将被释放，这意味着计数器将被有效重置。也可以在启动新进程前手动删除文件，以强制重置计数器。

另请参见 "guid"、"guid-prefix" 和 "shm-stats-file-max-objects"

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

此设置定义了用于共享计数器的共享内存（shm）每线程组所能存储的最大对象数量。该值与共享内存的最大内存大小直接相关，用于预先映射共享内存至指定大小，以避免运行时重新映射。默认值为 2k，适用于大多数配置，且不会导致内存使用不当，但如需可轻松调整。若此值过低，无法注册预期存储于共享内存中的对象，HAProxy 在启动时将发出警告。此设置仅在定义了 "shm-stats-file" 时才有效。

参见 "thread-groups"

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

此设置仅在编译时启用了 OpenSSL 支持时可用。它用于设置默认字符串，描述在 SSL/TLS 握手过程中协商的加密算法列表（“加密套件”），适用于所有未显式定义加密套件的 "bind" 语句，支持至 TLSv1.2。该字符串的格式由 OpenSSL 手册页中的 "man 1 ciphers" 定义。有关背景信息和建议，请参阅例如 (<https://wiki.mozilla.org/Security/Server_Side_TLS>) 和 (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>)。对于 TLSv1.3 的加密套件配置，请参阅 "ssl-default-bind-ciphersuites" 关键字。有关更多详细信息，请参阅 "bind" 关键字。

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

本设置仅在编译时启用了 OpenSSL 支持且使用 OpenSSL 1.1.1 或更高版本构建 HAProxy 时可用。它用于设置默认字符串，描述在 TLSv1.3 握手过程中协商的加密算法列表（“加密套件”），适用于所有未显式定义加密套件的 "bind" 段。该字符串的格式由 OpenSSL 手册中的 "man 1 ciphers" 文档在“ciphersuites”章节中定义。对于 TLSv1.2 及更早版本的加密配置，请参阅 "ssl-default-bind-ciphers" 关键字。本设置可能接受 TLSv1.2 加密套件，但此行为未在文档中说明，不建议使用，因其可能存在不一致或缺陷。OpenSSL 的默认 TLSv1.3 加密套件为：
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3 仅支持 5 种加密套件：

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

请参阅“bind”关键字以获取更多信息。

示例：

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

此设置仅在编译时启用 OpenSSL 支持时可用。该设置用于为所有未显式定义签名算法列表的 "bind" 行设置默认字符串，以描述与客户端认证相关的签名算法列表。字符串格式为以冒号分隔的签名算法列表。每个签名算法可采用以下两种形式之一：TLS1.3 签名方案名称（"rsa_pss_rsae_sha256"）或公钥算法 + 哈希算法形式（"ECDSA+SHA256"）。列表中可同时包含两种形式。有关格式的更多信息，请参阅 SSL_CTX_set1_client_sigalgs(3)。签名算法列表亦可在 RFC8446 第 [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) 节以及 OpenSSL 的 ssl/t1_lib.c 文件中找到。该设置不适用于 TLSv1.1 及更早版本协议，因为这些版本中签名算法不单独协商。除非需要与中间设备兼容，否则不建议更改此设置。

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

此设置仅在编译时启用 OpenSSL 支持时可用。它用于设置在使用 ECDHE 进行 SSL/TLS 握手时协商的椭圆曲线算法列表（“曲线套件”）的默认描述字符串。字符串格式为以冒号分隔的曲线名称列表。请参阅“bind”关键字以获取更多信息。

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

此设置仅在编译时启用 OpenSSL 支持时可用。它会将默认的 ssl-options 强制应用于所有 "bind" 语句。请查阅 "bind" 关键字以了解可用选项。

示例：

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

本设置仅在编译时启用了 OpenSSL 支持时可用。它用于设置默认字符串，描述在 TLSv1.2 和 TLSv1.3 握手过程中协商的签名算法列表，适用于所有未显式定义自身签名算法的 "bind" 段。字符串格式为以冒号分隔的签名算法列表。每个签名算法可采用以下两种形式之一：TLSv1.3 签名方案名称（"rsa_pss_rsae_sha256"）或公钥算法 + 哈希算法形式（"ECDSA+SHA256"）。列表中可同时包含两种形式。有关格式的更多信息，请参见 SSL_CTX_set1_sigalgs(3)。签名算法列表亦可在 RFC8446 第 [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) 节及 OpenSSL 的 ssl/t1_lib.c 文件中找到。此设置不适用于 TLSv1.1 及更早版本的协议，因为在这些版本中签名算法并非独立协商。除非需要与中间设备兼容，否则不建议更改此设置。

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

此设置仅在编译时启用 OpenSSL 支持时可用。它用于设置默认字符串，描述在 SSL/TLS 握手过程中与服务器协商的加密算法列表，适用于所有未显式定义加密算法的 "server" 行，支持至 TLSv1.2。字符串格式由 OpenSSL 手册页中的 "man 1 ciphers" 定义。有关背景信息和建议，请参阅例如 (<https://wiki.mozilla.org/Security/Server_Side_TLS>) 和 (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>)。对于 TLSv1.3 的加密套件配置，请参阅 "ssl-default-server-ciphersuites" 关键字。有关更多信息，请参阅 "server" 关键字。

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

此设置仅在编译时启用了 OpenSSL 支持且使用 OpenSSL 1.1.1 或更高版本构建 HAProxy 时可用。它用于设置默认字符串，描述在与服务器进行 TLSv1.3 握手时协商的加密算法列表，适用于所有未显式定义加密算法的 "server" 行。该字符串的格式由 OpenSSL 手册页中 "man 1 ciphers" 的 "ciphersuites" 段落定义。对于 TLSv1.2 及更早版本的加密配置，请参阅 "ssl-default-server-ciphers" 关键字。有关更多信息，请参阅 "server" 关键字。

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

本设置仅在编译时启用 OpenSSL 支持时可用。它用于为所有未显式定义签名算法列表的 "server" 段设置默认字符串，该字符串描述与客户端认证相关的签名算法列表。字符串格式为以冒号分隔的签名算法列表。每个签名算法可采用两种形式之一：TLSv1.3 签名方案名称（"rsa_pss_rsae_sha256"）或公钥算法 + 哈希算法形式（“ECDSA+SHA256”）。列表中可同时包含两种形式。有关格式的更多信息，请参阅 SSL_CTX_set1_client_sigalgs(3)。签名算法列表亦可在 RFC8446 第 [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) 节以及 OpenSSL 的 ssl/t1_lib.c 文件中找到。此设置不适用于 TLSv1.1 及更早版本的协议，因为在这些版本中签名算法并非独立协商。除非需要与中间设备兼容，否则不建议更改此设置。

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

此设置仅在编译时启用 OpenSSL 支持时可用。它用于设置在使用 ECDHE 进行 SSL/TLS 握手时协商的椭圆曲线算法列表（“曲线套件”）的默认描述字符串。字符串格式为以冒号分隔的曲线名称列表。请参阅“server”关键字获取更多信息。

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

此设置仅在编译时启用 OpenSSL 支持时可用。它会将默认的 ssl-options 强制应用于所有 "server" 行。请参阅 "server" 关键字以查看可用选项。

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

当编译时启用了 OpenSSL 支持时，此设置才可用。它用于设置默认字符串，描述在 TLSv1.2 和 TLSv1.3 握手过程中协商的签名算法列表，适用于所有未显式定义签名算法的 "server" 行。字符串格式为以冒号分隔的签名算法列表。每个签名算法可采用以下两种形式之一：TLSv1.3 签名方案名称（"rsa_pss_rsae_sha256"）或公钥算法 + 哈希算法形式（"ECDSA+SHA256"）。列表中可同时包含两种形式。有关格式的更多信息，请参见 SSL_CTX_set1_sigalgs(3)。签名算法列表亦可在 RFC8446 第 [4.2.3](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3) 节以及 OpenSSL 的 ssl/t1_lib.c 文件中找到。此设置不适用于 TLSv1.1 及更早版本的协议，因为在这些版本中签名算法并非独立协商。除非需要与中间设备兼容，否则不建议更改此设置。

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

当编译时启用了 OpenSSL 支持时，此设置才可用。它用于设置在使用临时 Diffie-Hellman（DHE）密钥交换进行 SSL/TLS 握手时的默认 DH 参数，适用于所有未显式定义自身参数的 "bind" 语句。若在 bind 证书文件中发现了自定义 DH 参数，则该设置将被覆盖。如果既未通过 ssl-dh-param-file 指定自定义 DH 参数，也未在证书文件中直接设置，除非设置了 tune.ssl.default-dh-param，否则将不会使用 DHE 密码套件。在后一种情况下，将使用指定大小的预定义 DH 参数。自定义参数被认为更加安全，因此建议使用。可通过 OpenSSL 命令 "openssl dhparam `<size>`" 生成自定义 DH 参数，其中 size 至少应为 2048，因为 1024 位的 DH 参数已不再被视为安全。

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

此设置仅在编译时启用了 OpenSSL 支持时可用。它允许定义一个完整的命令行，该命令行将在初始化过程中加载加密证书时被调用。该命令可以是脚本或其他程序。命令将接收加密私钥路径作为第一个参数，随后是用户定义的“args”参数，并应将解密加密私钥所需的密码短语输出到标准输出。在初始化过程中每次加载新的加密私钥时，HAProxy 会首先尝试所有其他已知的密码短语进行解密，若均失败，则最终再次调用密码短语命令。

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

当编译时启用了 OpenSSL 支持且 OpenSSL 版本不低于 3.0 时，此设置才可用。它允许定义一个默认属性字符串，用于在获取算法时指定提供者。其行为与 OpenSSL propquery 选项相同，语法也一致（详见 <https://www.openssl.org/docs/man3.0/man7/property.html>）。例如，若已加载两个提供者（foo 提供者和默认提供者），则使用 propquery "?provider=foo" 可默认选择由 foo 提供者提供的算法实现，若未找到则回退至默认提供者的实现。

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

此设置仅在编译时启用了 OpenSSL 支持且 OpenSSL 版本不低于 3.0 时可用。该设置允许在初始化时加载一个提供者。若加载成功，HAProxy 可使用该提供者提供的任何功能。可在配置文件中指定多个 `ssl-provider` 选项，提供者将按其出现的顺序依次加载。

请注意，显式加载提供者会阻止 OpenSSL 自动加载“default”提供者。OpenSSL 还允许在配置文件（例如 openssl.cnf）中直接定义应加载的提供者，因此无需使用此 'ssl-provider' 选项来加载提供者。可使用 "show ssl providers" CLI 命令查看所有成功加载的提供者。

OpenSSL 提供者的默认搜索路径可在执行 "openssl version -a" 命令的输出中找到。若提供者位于其他目录，请设置 OPENSSL_MODULES 环境变量，该变量指定提供者所在目录。

另请参见 "ssl-propquery" 和 "ssl-provider-path"。

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

此设置仅在编译时启用了 OpenSSL 支持且 OpenSSL 版本不低于 3.0 时可用。它允许指定 OpenSSL 用于查找提供者时的搜索路径。其行为与 OPENSSL_MODULES 环境变量相同。该路径将用于后续所有 'ssl-provider' 选项，直至定义新的 'ssl-provider-path' 为止。参见 "ssl-provider"。

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

此设置用于配置 HAProxy 查找额外 SSL 文件的方式。默认情况下，HAProxy 会在文件名后添加新的扩展名（例如：使用 "foobar.crt" 加载 "foobar.crt.key"）。启用此选项后，HAProxy 会在添加新扩展名前移除原有扩展名（例如：使用 "foobar.crt" 加载 "foobar.key"）。

证书文件必须具有 ".crt" 扩展名，此选项才能生效。

此选项与捆绑扩展名（.ecdsa、.rsa、.dsa）不兼容，且不会尝试移除它们。

此选项默认已禁用。另请参见“ssl-load-extra-files”。

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

此设置会改变 HAProxy 在加载 SSL 证书时查找未指定文件的方式。该选项适用于与 "bind" 行及 "server" 行关联的证书，但部分额外文件对 "server" 行证书无功能性影响。

默认情况下，HAProxy 会自动发现配置中未指定的大量文件，若需要优化启动时间，可能需要禁用此行为。

"none"：仅加载配置中指定的文件。若文件不存在，不尝试加载证书捆绑包。在目录情况下，若证书文件的基名相同，则不会尝试进行证书捆绑。

"all"：这是默认行为，将尝试加载所有内容，包括证书包、sctl、OCSP、颁发者和密钥。

"bundle"：当配置中指定的文件不存在时，HAProxy 将尝试加载一个证书捆绑包。证书捆绑包仅在前端侧进行管理，对后端证书无效。

从 HAProxy 2.3 开始，证书包不再加载到同一个 OpenSSL 证书存储中，而是将每个证书加载到独立的存储中，这等效于声明多个 "crt"。要实现此功能，需使用 OpenSSL 1.1.1 或更高版本。这意味着证书包现在仅用于向后兼容，不再强制要求用于混合 RSA/ECC 绑定配置。

要将这些 PEM 文件关联为 HAProxy 识别的“证书捆绑包”，文件名必须按照以下方式命名：所有需捆绑的 PEM 文件必须具有相同的基名，并附加表示密钥类型的后缀。目前支持三种后缀：rsa、dsa 和 ecdsa。例如，若 [www.example.com](http://www.example.com) 包含两个 PEM 文件，分别为 RSA 文件和 ECDSA 文件，则文件名必须分别为 "example.pem.rsa" 和 "example.pem.ecdsa"。文件名的前缀部分可任意指定；仅后缀部分具有意义。要将此捆绑包加载至 HAProxy，仅需指定基名即可：

示例：bind :8443 ssl crt example.pem

请注意，后缀不会传递给 HAProxy；这会指示 HAProxy 查找证书捆绑包。

HAProxy 会将捆绑包中的所有 PEM 文件当作在多个 "crt" 中分别配置一样进行加载。

证书包加载不再影响目录加载，因为文件已分别加载。

在命令行界面中，证书包被视为独立文件，提交时必须包含证书包扩展名。

支持 OCSP 文件（.ocsp）、颁发者文件（.issuer）、证书透明度（.sctl）以及私钥（.key）的多证书捆绑。

"sctl"：对每个 crt 关键字尝试加载 "`<basename>`.sctl"。若为后端证书提供该文件，将尝试加载，但不会产生任何功能影响。

"ocsp": 为每个 crt 关键字尝试加载 "`<basename>`.ocsp"。若为后端证书提供该文件，将尝试加载，但不会产生任何功能影响。

"issuer": 若 OCSP 文件的颁发者未在 PEM 文件中提供，则尝试加载 "`<basename>`.issuer"。若为后端证书提供，将被加载，但不会产生任何功能影响。

key: 如果私钥未通过 PEM 文件提供，请尝试加载包含私钥的文件 "`<basename>`.key"。

默认行为为 "all"。

示例：

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

另请参阅：“crt”，[第 5.1 节](/zh/haproxy/bind-and-server-options/#section-5-1) 关于绑定选项，以及[第 5.2 节](/zh/haproxy/bind-and-server-options/#section-5-2) 关于服务器选项。

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

该指令允许选择如 <https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html> 所述的 OpenSSL 安全级别。安全级别将应用于 HAProxy 中的每个 SSL 上下文。仅支持 0 至 5 之间的数值。

默认值取决于所用 OpenSSL 版本、发行版以及库的编译方式。

该指令要求至少使用 OpenSSL 1.1.1 版本。

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

服务器端 SSL 验证的默认行为。若设置为 'none'，则不验证服务器证书。默认值为 'required'，除非通过命令行选项 '-dV' 强制指定。

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

自签名 CA，即 x509 根 CA，是证书链验证的锚点：作为服务器发送它毫无用处，客户端必须持有。标准配置需确保此类 CA 不包含在 PEM 文件中。此选项允许将此类 CA 保留在 PEM 文件中，但不发送给客户端。使用场景是提供 OCSP 发行者，无需 '.issuer' 文件，并可通过 'issuers-chain-path' 共享。此设置适用于所有无中间证书的证书。对 BoringSSL 无效，.issuer 字段被忽略，因 OCSP 位无需该信息。要求至少使用 OpenSSL 1.0.2。

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

启用或禁用统计信息最大值计数器的计算。若无需使用，禁用可略微提升性能。默认值为启用。

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

默认情况下，统计套接字最多允许 10 个并发连接。可以使用 "stats maxconn" 修改此值。

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

将 Unix 套接字绑定到 `<path>`，或将 TCPv4/v6 地址绑定到 `<address:port>`。连接至该套接字将返回各种统计信息输出，甚至允许发出某些命令以更改部分运行时设置。请参阅 [本指南第 9.3 节](/zh/haproxy/statistics-and-monitoring/#section-9-3)“Unix 套接字命令”以获取更多详细信息。

所有 "bind" 行支持的参数均受支持，例如用于限制某些用户或其访问权限。请参阅 [第 5.1 节](/zh/haproxy/bind-and-server-options/#section-5-1) 获取更多信息。

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

默认情况下，统计信息套接字的超时时间为 10 秒。可以使用“stats timeout”更改此值。该值必须以毫秒为单位指定，或后缀时间单位之一：{ us, ms, s, m, h, d }。

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

用于生成 HAProxy 统计信息文件的路径。HAProxy 启动时会将该文件中的值预加载至其内部计数器。使用 CLI 命令“dump stats-file”可生成此类统计信息文件。详情请参见管理手册。

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

激活用于对 HAProxy 二进制文件施加压力的备用代码。级别为 0 到 9 之间的整数。默认值 0 表示禁用所有压力执行。级别 1 到 9 将逐步增加对 HAProxy 二进制文件的压力。请注意，使用任何正值会显著影响性能。因此，除非出于调试目的且经开发者请求，否则不得启用。

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

在 setrlimit 失败时使进程在启动阶段失败。HAProxy 会根据已计算的结果尝试设置最佳的 setrlimit。若设置失败，将发出警告。此选项用于确保当这些限制失败时，HAProxy 明确失败。默认启用。可通过在选项前加上 "no" 关键字强制禁用。

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

此设置仅在编译时启用了线程支持的情况下可用。它用于列举将组成线程组 `<group>` 的线程列表。线程编号与组编号均从 1 开始。线程范围可通过单一线程编号指定，或通过指定下限和上限并以连字符 '-' 分隔来定义（例如 "1-16"）。未分配的线程将自动分配至未分配的线程组，且通过本指令定义的线程组不会接收超过所定义数量的线程。多次定义同一组将覆盖先前的定义，以最新定义为准。另请参见 "nbthread" 和 "thread-groups"。

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

此设置仅在编译时启用了线程支持的情况下可用。它可使 HAProxy 将其线程划分为 `<number>` 个独立的组。当前默认值为 1。通过线程组可减少线程间的共享以降低竞争，但需付出额外的配置成本。这也是使用超过 64 个线程的唯一方式，因为每个组最多可配置 64 个线程。组的最大数量在编译时配置，默认值为 16。参见“nbthread”。

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

此设置用于强制限制线程数量，无论是自动检测的，还是配置指定的。

在某些操作系统中，线程数量会自动检测，此时在通用且可移植的配置中，可能希望线程数量低于 CPU 核心数。实际上，尽管 "nbthread" 会强制设置线程数，若该值高于可用 CPU 数量，将触发警告并导致性能下降；而 thread-hard-limit 仅对最大值进行上限限制，自动将线程数量限制在不超过该值，但不会对低于该值的情况进行干预。若 "nbthread" 被强制设置为更高值，则 thread-hard-limit 优先生效，并发出警告，以便修复配置异常。默认情况下无限制。参见 "nbthread"。

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

将进程的用户 ID 更改为 `<number>`。建议该用户 ID 专用于 HAProxy 或少量相似的守护进程。HAProxy 必须以超级用户权限启动，才能切换至其他用户。参见“gid”和“user”。

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

设置每个进程的最大文件描述符数量为 `<number>`。默认情况下，该值会自动计算，因此建议不要使用此选项。若仅意图限制文件描述符数量，建议改用 "fd-hard-limit"。

请注意，动态服务器不参与此自动资源计算。若使用大量动态服务器，可能需要手动指定该值。

另请参阅：fd-hard-limit、maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group `<group>` ] [ gid `<gid>` ]

统一设定在 "bind" 语句中声明的 Unix 监听套接字的常用设置。此功能主要用于简化 Unix 套接字的声明，并降低出错风险，因为这些设置通常必需，但又与进程相关。`<prefix>` 设置可用于强制所有套接字路径相对于该目录。这可能用于访问另一个组件的 chroot 环境。请注意，这些路径在 HAProxy 执行 chroot 之前已被解析，因此均为绝对路径。`<mode>`、`<user>`、`<uid>`、`<group>` 和 `<gid>` 的含义与 "bind" 语句中同名设置完全相同。若两者均被指定，"bind" 语句具有优先权，即 "unix-bind" 设置可视为进程级默认设置。

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

移除参数中指定的环境变量。在某些操作过程中，用户环境偶尔会继承一些敏感信息，此功能可用于隐藏这些信息。未存在的变量将被静默忽略，因此操作完成后可确保这些变量均不存在。更改立即生效，配置文件中的下一行将无法再访问这些变量。参见“setenv”、“presetenv”和“resetenv”。

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

与 "uid" 类似，但使用 /etc/passwd 中用户名 `<user name>` 对应的 UID。另请参阅 "uid" 和 "group"。

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

仅允许使用字母、数字、连字符和下划线，与 DNS 名称规则一致。

此语句在高可用性配置中非常有用，当两个或多个进程或服务器共享同一 IP 地址时。通过在所有节点上设置不同的 node-name，即可立即识别出正在处理流量的服务器。

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

设置 WURFL 用户代理缓存大小。为加快查找速度，已处理的用户代理将被保留在 LRU 缓存中：

- "0" ：不使用缓存。
- `<size>`：LRU 缓存的元素数量。

请注意，此选项仅在 HAProxy 编译时将 USE_WURFL 设置为 1 时可用。

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

用于提供设备检测服务的 WURFL 数据文件路径。该文件必须对 HAProxy 可访问，并具备相应的权限。

请注意，此选项仅在 HAProxy 编译时将 USE_WURFL 设置为 1 时可用。

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

以空格分隔的 WURFL 功能、虚拟功能及属性名称列表，这些名称将用于注入的头中。功能和虚拟功能名称的完整列表可在 Scientiamobile 官网获取：

```text
https://www.scientiamobile.com/wurflCapability
```

有效的 WURFL 属性包括：

- wurfl_id 包含匹配设备的设备 ID。

- wurfl_root_id 包含匹配设备的设备根 ID。

- wurfl_isdevroot 用于判断匹配的设备是否为根设备。可能的取值为 "TRUE" 或 "FALSE"。

- wurfl_useragent 来自此特定 Web 请求的原始用户代理。

- wurfl_api_version 包含一个表示当前所用 Libwurfl API 版本的字符串。

- wurfl_info 一个包含已解析的 wurfl.xml 信息及其完整路径的字符串。

- wurfl_last_load_time 包含 WURFL 上次成功加载的 UNIX 时间戳。

- wurfl_normalized_useragent 已归一化的用户代理。

请注意，此选项仅在 HAProxy 编译时将 USE_WURFL 设置为 1 时可用。

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

用于分隔包含 WURFL 结果的响应头中各值的字符。若未设置，则默认使用逗号（,）。

请注意，此选项仅在 HAProxy 编译时将 USE_WURFL 设置为 1 时可用。

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

WURFL 补丁文件路径列表。请注意，补丁在启动期间加载，因此在 chroot 之前。

请注意，此选项仅在 HAProxy 编译时将 USE_WURFL 设置为 1 时可用。

## 3.2. 性能调优 {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

在某些情况下，尤其是在支持可变频率的处理器上处理低延迟，或在虚拟机中运行时，每当进程使用轮询器等待 I/O 操作，处理器可能长时间进入睡眠状态，或被分配给其他虚拟机，从而导致延迟显著升高。此选项通过在轮询器上始终使用空超时来防止处理器睡眠，从而提供解决方案。这可显著降低延迟（实测降低 30 至 100 微秒），但可能带来处理器过热的风险。该选项也可用于线程，但若线程绑定不当，可能导致严重冲突，造成性能下降，并在 "show info" 输出中显示 CPU 被窃取字段值过高，表明存在配置错误的线程。使用此选项时，务必避免让进程与网络中断共享同一处理器。同时，建议避免在共享同一核心的多个 CPU 线程上使用。该选项默认禁用。若已启用，仍可通过在选项前添加 "no" 关键字强制禁用。该选项对 "select" 和 "poll" 轮询器无效。

在无缝重载场景中，此选项会在旧进程中自动禁用；当多个进程在一段时间内仍保留以等待当前连接结束时，可避免过多的 CPU 竞争。

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

默认情况下，HAProxy 会将健康检查的起始时间分散到群组中所有服务器的最小健康检查间隔内。其原则是避免对运行在同一服务器上的服务造成过大的冲击。但当使用较长的检查间隔（10 秒或更长）时，群组中最后的服务器需要一段时间才会开始被测试，这可能带来问题。该参数用于强制设定首次检查与最后一次检查之间的延迟上限，即使服务器的检查间隔较大也适用。当服务器使用较短的检查间隔时，其间隔仍会被遵守。

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

设置 HAProxy 在停止为新请求压缩或降低当前请求压缩级别之前可达到的最大 CPU 使用率。其工作方式类似于 'maxcomprate'，但测量的是 CPU 使用率而非传入数据带宽。该值以 HAProxy 所用 CPU 的百分比表示。值为 100 时表示禁用限制。默认值为 100。设置较低的值可防止压缩操作拖慢整个进程并避免引入高延迟。

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

设置每个进程的输入压缩速率上限为 `<number>` 千字节每秒。对于每个流，若达到上限，则在流过程中降低压缩级别。若在流开始时即达到上限，则该流将完全不进行压缩。若未达到上限，压缩级别将提升至 tune.comp.maxlevel。值为零表示无限制，此为默认值。

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

设置每个进程的最大并发连接数为 `<number>`。这等价于命令行参数 "-n"。通过命令行参数 "-n" 提供的值将优先于全局段中设置的 maxconn 值。HAProxy 进程也可在编译时使用 SYSTEM_MAXCONN 变量，此时该变量作为系统级 maxconn 上限。同样，命令行参数 "-n" 可在运行时绕过已设置的 SYSTEM_MAXCONN 限制。当达到 maxconn 时，代理将停止接受新的连接。进程的软文件描述符限制（可通过 "ulimit -n" 命令获取）将根据提供的 maxconn 值自动调整。参见 "ulimit-n"。请注意：在某些平台上，"select" 轮询器无法可靠地使用超过 1024 个文件描述符。若你的平台仅支持 select 且启动时报告 "select FAILED"，需降低 maxconn 值直至正常工作（通常略低于 500）。若未设置 maxconn 值，系统将基于 "ulimit -nH" 命令报告的当前文件描述符限制自动计算该值（取硬限制与软限制中的最大值），随后自动值可能被 "fd-hard-limit" 和内存限制进一步缩减，若后者通过 "-m" 命令行选项强制启用。自动值还取决于缓冲区大小、压缩所用内存、SSL 缓存大小，以及是否启用 SSL 和相应的 maxsslconn（后者也可为自动值）。

另请参阅：fd-hard-limit、ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

设置每进程每秒最大连接数为 `<number>`。当达到此限制时，代理将停止接受连接。该设置可用于限制全局容量，而不受各前端容量的限制。请注意，此设置仅可用作服务保护措施，因为当达到限制时，前端之间未必能公平分配连接，因此建议同时将每个前端的连接数限制为接近其预期份额的值。此外，降低 tune.maxaccept 可提升公平性。

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

设置每个进程的最大管道数量为 `<number>`。目前，管道仅由基于内核的 TCP 拼接功能使用。由于管道包含两个文件描述符，因此“ulimit-n”值将相应增加。默认值为 maxconn/4，对于大多数高负载场景而言似乎已足够。拼接代码会动态分配和释放管道，并可在必要时回退至标准复制，因此将此值设置过低可能仅影响性能。

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

设置每进程每秒最大会话数为 `<number>`。当达到此限制时，代理将停止接受连接。该设置可用于限制全局容量，而不受各前端容量的限制。请注意，此设置仅可用作服务保护措施，因为达到限制时各前端之间未必能公平分配资源，因此建议同时将每个前端的容量限制为接近其预期份额的值。此外，降低 tune.maxaccept 可提升公平性。

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

设置每个进程的最大并发 SSL 连接数为 `<number>`。默认情况下，不存在 SSL 特定的限制，这意味着全局的 maxconn 设置将适用于所有连接。设置此限制可避免 OpenSSL 占用过多内存，从而在 malloc 返回 NULL 时导致崩溃（遗憾的是，OpenSSL 并未可靠地检查此类情况）。请注意，该限制同时适用于入站和出站连接，因此一个解密后又加密的连接计为 2 个 SSL 连接。如果未设置此值，但已施加内存限制，则该值将根据内存限制、maxconn、缓冲区大小、压缩所用内存、SSL 缓存大小以及前端、后端或两者中是否启用 SSL 自动计算得出。若在存在内存限制的情况下，maxconn 和 maxsslconn 均未指定，HAProxy 将自动调整这些值，以确保 100% 的连接均可通过 SSL 建立，且无风险，并考虑启用 SSL 的端点（前端、后端或两者）。

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

设置每进程每秒最大 SSL 会话数为 `<number>`。当达到此限制时，SSL 监听器将停止接受连接。该设置可用于限制全局 SSL CPU 使用率，而不受各前端容量的影响。请注意，此设置仅可用作服务保护措施，因为达到限制时各前端之间未必能公平分配资源，因此建议同时将每个前端的值限制在接近其预期份额的范围内。还请注意，会话数在进入 SSL 栈之前即被计入，而非之后，这同样可防止不良握手对栈造成影响。此外，降低 tune.maxaccept 可提升公平性。

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

设置每个进程可用于 zlib 的最大内存容量（单位：MB）。当达到最大值时，若内存不可用，后续流将不再进行压缩。设为 0 时表示无限制。默认值为 0。可通过 Unix 套接字执行 "show info" 命令，在 "MaxZlibMemUsage" 行查看该值（单位：字节），zlib 实际使用的内存为 "ZlibMemUsage"（单位：字节）。

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

禁用在内存不足或重载时尝试回收大量内存的几个时刻的内存缩减（"malloc_trim"）。缩减内存会强制系统分配器扫描所有未使用区域并释放它们。通常认为这是个良好动作，可在旧进程几乎不再使用内存时为新进程腾出更多可用内存。但处理数万至数十万并发连接的某些系统可能经历严重的内存碎片，导致此释放操作耗时极长。在此期间，进程不再处理任何流量，不再接受新连接，部分健康检查甚至可能失败，看门狗也可能触发并终止无响应的进程，留下巨大的核心转储文件。若发生此类情况，建议使用此选项禁用内存缩减，停止尝试对新进程保持友好。请注意，高级内存分配器通常不受此类问题影响。

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

禁用 Linux 上“epoll”事件轮询系统的使用。其效果等同于命令行参数 "-de"。下一个使用的轮询系统通常为 "poll"。参见 "nopoll"。

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

禁用在基于 Solaris 10 及更高版本的 SunOS 系统上使用事件端口事件轮询系统。其效果等同于命令行参数 "-dv"。后续使用的轮询系统通常为 "poll"。参见 "nopoll"。

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

禁用使用 getaddrinfo(3) 进行名称解析。等效于命令行参数 "-dG"。已弃用的 gethostbyname(3) 将被使用。

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

禁用在 BSD 上使用“kqueue”事件轮询系统。其效果等同于命令行参数“-dk”。下一个使用的轮询系统通常为“poll”。参见“nopoll”。

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

禁用 ktls 的使用。其效果等同于命令行参数 "-dT"。

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

禁用“poll”事件轮询系统的使用。其效果等同于命令行参数“-dp”。下一个使用的轮询系统将是“select”。由于“poll”在 HAProxy 支持的所有平台上均可用，因此应无需禁用它。另请参见“nokqueue”、“noepoll”和“noevports”。

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

禁用 SO_REUSEPORT 的使用——参见 socket(7)。其效果等同于命令行参数 "-dR"。

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

禁用 Linux 上套接字之间的内核 TCP 拼接功能。该选项等效于命令行参数 "-dS"。数据将改用传统的、更具可移植性的 recv/send 调用进行复制。内核 TCP 拼接仅适用于部分较新的 2.6 内核版本。2.6.25 至 2.6.28 之间的大多数版本存在缺陷，会导致转发损坏的数据，因此不得使用。当存在疑虑时，该选项可更方便地全局禁用内核拼接。另请参见 "option splice-auto"、"option splice-request" 和 "option splice-response"。

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

启用（on）或禁用（off）按功能的内存分析。该功能将记录进程内（包括库）任意位置的 malloc/calloc/realloc/free 调用使用统计信息，并可通过 CLI 命令 "show profiling" 报告。此功能主要用于观察到无法用内存池解释的异常内存使用、且需要更多信息的情况。性能开销通常约为 1%，在高度多线程的机器上可能略高，因此通常适用于生产环境。也可通过 CLI 命令 "set profiling memory" 在运行时实现相同效果，请参阅管理手册。

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

启用（'on'）或禁用（'off'）任务级 CPU 性能分析。设置为 'auto' 时，当线程在 "avg_loop_us" 活动字段中报告的平均延迟达到或超过 1000 微秒时，性能分析将自动开启；当延迟回落至 990 微秒以下时，性能分析将自动关闭（该值为最近 1024 次循环的平均值，因此不会快速波动，且能显著平滑短时峰值）。在系统过载、容器或虚拟机环境中，也可能偶尔自发触发，或在系统发生交换（swap）时触发（负载均衡器上绝对不应发生交换）。

当启用任务分析功能时，HAProxy 还可收集每个任务持有锁或等待锁所花费的时间，以及在池缓存未命中情况下等待内存分配成功所花费的时间。这些信息有时有助于理解延迟的某些成因。为此，可额外传递以下关键字：`lock`（启用锁时间收集）、`no-lock`（禁用锁时间收集）、`memory`（启用内存分配时间收集）或 `no-memory`（禁用内存分配时间收集）。默认情况下这些功能未启用，因为它们在高负载系统上可能带来不可忽略的 CPU 开销（3% 至 10%）。请注意，仅在实际运行分析时才会产生开销，因此在“auto”模式下，仅当 HAProxy 决定开启分析时才会出现该开销。

按任务进行 CPU 性能分析可方便地报告时间消耗位置以及各请求对其他请求的影响。启用该功能通常对整体性能的影响小于 1%，因此建议保持默认的 'auto' 值，仅在识别出问题时才启用。该功能需要系统支持带有时钟标识符 CLOCK_MONOTONIC 和 CLOCK_THREAD_CPUTIME_ID 的 clock_gettime(2) 系统调用，否则报告的时间将为零。可通过 CLI 使用 "set profiling" 动态更改此选项。

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

有时希望避免以精确间隔向服务器发送 agent 检查和健康检查，例如当多个逻辑服务器位于同一物理服务器上时。借助此参数，可在 0 至 +/- 50% 之间引入检查间隔的随机性。数值在 2 至 5 之间时，效果似乎较好。默认值仍为 0。

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

设置 OpenSSL 引擎为 `<name>`。可通过命令 "openssl engine" 获取 `<name>` 的有效值列表。该语句可多次使用，用于启用多个加密引擎。引用不支持的引擎将导致 HAProxy 无法启动。请注意，许多引擎在现代处理器上会导致 HTTPS 性能低于纯软件实现。可选命令 "algo" 使用 OpenSSL 函数 ENGINE_set_default_string() 设置引擎默认提供的算法。值 "ALL" 表示使用引擎进行所有加密操作。若未指定算法列表，则默认使用 "ALL"。可指定以逗号分隔的不同算法列表，包括：RSA、DSA、DH、EC、RAND、CIPHERS、DIGESTS、PKEY、PKEY_CRYPTO、PKEY_ASN1。此格式与 OpenSSL 配置文件所用格式相同：
<https://www.openssl.org/docs/man1.0.2/apps/config.html>

HAProxy 版本 2.6 已禁用默认构建中对引擎的支持。此选项仅在 HAProxy 编译时启用了相关支持后才可用。如需使用 ssl-engine，可使用 USE_ENGINE=1 标志重新编译 HAProxy。

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

向 SSL 上下文添加 SSL_MODE_ASYNC 模式。若使用支持异步的 SSL 引擎，此模式可启用异步 TLS I/O 操作。当前实现支持最多 32 个引擎。OpenSSL 的 ASYNC API 不支持移动读/写缓冲区，且与 HAProxy 的缓冲区管理机制不兼容。因此，异步模式在读/写操作中被禁用（仅在初始连接和重新协商握手阶段启用）。

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

启用（'on'）或禁用（'off'）applet 的零拷贝数据转发。默认情况下已启用。

另请参阅：tune.disable-zero-copy-forwarding。

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

设置每个进程可分配的缓冲区数量的硬性上限。默认值为 0，表示无限制。该限制会自动调整，以满足紧急情况下的预留缓冲区需求，从而避免用户进行复杂的计算。强制设置此值特别有助于限制进程可占用的内存总量，同时保持合理的运行行为。当达到此限制时，请求缓冲区的任务将等待其他缓冲区被释放后才能继续。在大多数情况下，等待时间极短且不可察觉，前提是限制值保持合理。然而，某些历史限制已削弱了该机制的可靠性，已知在持续资源短缺的特定情况下，部分任务可能冻结，直至超时，因此建议仅在绝对必要时才使用此设置。

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

设置每个线程在内存不足导致内存分配失败时，预先分配并仅用于该情况的缓冲区数量。最小值为 0，默认值为 4。除非核心开发者针对特定原因建议修改，否则用户无需更改此值。

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

设置缓冲区大小为指定值（以字节为单位）。较小的值可在相同内存占用下支持更多流，较大的值则有助于某些具有超大 Cookie 的应用正常运行。默认值为 16384，可在构建时修改。强烈建议不要更改此默认值，过低的值可能导致统计信息等部分服务失效，而高于默认值的设置会增加内存使用量，可能引发系统内存不足。若增大该值，至少应将全局 maxconn 参数按相同比例减小。此外，使用 HTTP/2 时，该值必须为 16384 或更大，且必须小于 256 MB（268435456 字节）。若 HTTP 请求的头块大小超过 (tune.bufsize - tune.maxrewrite)，HAProxy 将返回 HTTP 400（错误请求）错误。同理，若 HTTP 响应的头块大小超过该值，HAProxy 将返回 HTTP 502（错误网关）错误。请注意，使用此参数设置的值在 32 位机器上会自动向上取整至下一个 8 的倍数，在 64 位机器上则取整至下一个 16 的倍数。另请参阅：tune.bufsize.large、tune.bufsize.small。

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

设置大缓冲区的大小（以字节为单位）。默认情况下，大缓冲区支持未启用，必须显式设置此值以启用。

这些缓冲区专为某些特定场景设计，在不改变常规缓冲区大小的前提下，需缓冲更多数据。大缓冲区不会被隐式使用。另请参阅：tune.bufsize。

请注意，当配置较大的缓冲区时，每个线程在启动期间将为内部使用分配三个特殊的大缓冲区。

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

设置小缓冲区的大小（字节）。默认值为 1024。

这些缓冲区专为某些内存使用受限的特定场景设计，此时似乎无需分配完整的缓冲区。然而，若小缓冲区不足以满足需求，系统将自动重新分配，切换至标准大小的缓冲区。

目前，该功能仅由 HTTP/3 协议自动使用以发出响应头。
对于其他情况，可通过 "use-small-buffers" 选项为特定代理启用小缓冲区支持。另请参阅：tune.bufsize。

另请参阅：option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

设置 CLI 上传递给命令的有效负载的最大允许大小。

在命令行界面（CLI）中，命令行受缓冲区大小限制。这意味着所有命令及其参数必须能够容纳在缓冲区中以供处理，不包括可传递给命令行最后一个命令的有效负载。如有必要，该有效负载可分配至专用区域。其大小受此参数限制。默认值为 128KB。

尽管该值对大多数使用场景已足够高，但若进行修改，必须谨慎选择。过大的值可能影响 HAProxy 的性能。根据具体命令，过大的负载可能需要较长时间处理，甚至可能触发看门狗机制。

请参阅管理手册以获取 CLI 的详细信息。

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

设置最大压缩级别。压缩级别会影响压缩过程中的 CPU 使用率。每个使用压缩的流均会以该值初始化压缩算法。默认值为 1。

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

为支持动态后端，所有命名的 defaults 段在解析后均会保留在内存中。这是必要的，因为运行时添加的后端必须基于命名的 defaults 段进行配置。

如果默认配置实例数量较多，此操作可能消耗大量内存。在此情况下，若无需动态后端功能，可使用此选项在解析后强制删除 defaults 段。但必须保留被引用的 defaults 段，因为其中包含无法被引用代理复制的设置。例如，当 defaults 段定义了 TCP/HTTP 规则或 tcpcheck 规则集时即属此类情况。

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

禁用数据快速转发。该机制通过直接在侧边之间传递数据而不唤醒流来优化数据转发。通过此指令，可禁用此优化。请注意，该指令同时禁用任何内核 TCP 拼接以及零拷贝转发。此命令并非用于常规使用，通常仅在复杂调试会话中由开发者建议使用。

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

全局禁用数据的零拷贝转发。该机制通过避免使用通道缓冲区来优化数据快速转发。通过此指令，可禁用此项优化。请注意，该指令同时也会禁用任何内核 TCP 拼接功能。

另请参阅：tune.pt.zero-copy-forwarding、tune.applet.zero-copy-forwarding、tune.h1.zero-copy-fwd-recv、tune.h1.zero-copy-fwd-send、tune.h2.zero-copy-fwd-send、tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

在 HAProxy 的发展历程中，曾遇到若干由 Linux 内核 epoll 机制中的缺陷引发的复杂问题。此类问题通常极为罕见，且仅在报告者特定环境中可复现，通常只能通过禁用 epoll 并切换至 poll 模式来规避，这在高性能环境中并不理想。每次问题仅影响极少数（且罕见）的事件类型，因此提供屏蔽这些事件的能力，可构成更可接受的临时解决方案。本选项通过允许静默忽略若干不常见的事件，并以输入事件（报告未指定的入站事件）替代，实现此功能。其效果为避免在某些位置触发快速错误处理路径，仅使用通用处理路径。除非经专家指导，用于诊断或规避内核缺陷，否则不得使用此选项。

该选项接受一个参数，参数为以逗号分隔的单词列表，每个单词指定要屏蔽的事件。当前支持的事件列表如下：- "err"：屏蔽 EPOLLERR 事件 - "hup"：屏蔽 EPOLLHUP 事件 - "rdhup"：屏蔽 EPOLLRDHUP 事件

示例：

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

设置异步任务处理器（来自 event_hdl API）一次可处理的事件数量。`<number>` 应在 1 到 10000 之间。数值过大可能导致因任务在无中断情况下执行繁重工作而引发线程竞争；另一方面，数值过小则可能导致任务因每次运行无法处理足够事件而持续被重新调度，无法跟上事件生产者的节奏。默认值可在编译时强制指定，否则默认为 100。

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

若使用 DEBUG_FAIL_ALLOC 编译或以 "-dMfail" 启动，表示内存分配尝试失败的概率百分比。必须介于 0（无失败）至 100（完全失败）之间。此选项有助于调试，确保内存分配失败时能被妥善处理。未设置时，该比例为 0。但命令行选项 "-dMfail" 会自动将其设为 1% 的失败率，因此测试时无需修改配置。

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

启用（'on'）或禁用（'off'）支持该模式的文件描述符（FD）的边缘触发轮询模式。当前仅支持 epoll。在某些场景下，此功能可显著减少 epoll_ctl() 调用次数，并略微提升性能。此功能仍处于实验阶段，若存在缺陷可能导致连接冻结，且默认情况下已禁用。

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

设置最小 CPU 使用率，范围为 0 到 100，当连接出现过多异常事件时将被终止。此设置适用于已达到异常事件阈值限制的连接。在某些环境中，长时间连接可能在不造成性能影响的情况下表现异常，此时可能希望即使连接行为异常也予以保留，仅当 CPU 使用率较高时才开始终止此类连接。该参数允许指定：当 CPU 使用率处于或高于此水平时，达到异常事件阈值的连接将被主动终止；而当 CPU 使用率低于此水平时则不会终止。请注意，CPU 使用率按线程测量，因此单个异常连接可能被终止。默认值为 0，表示达到异常事件阈值的连接将自动被终止。经验法则为：将此值设为通常观测到的 CPU 使用率的两倍，或通常观测到的 CPU 使用率加上空闲使用率的一半（例如，若 CPU 通常达到 60%，则此处设为 80 可能合理）。若未设置 tune.h2.fe.glitches-threshold、tune.quic.fe.sec.glitches-threshold 或 tune.h1.fe.glitches-threshold，此参数无效。另请参见全局参数 "tune.h2.fe.glitches-threshold"、"tune.h1.fe.glitches-threshold" 和 "tune.quic.fe.sec.glitches-threshold"。

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

设置 HTTP/1 后端连接上允许的异常事件阈值，当异常事件数量超过该阈值时，该连接将被自动终止。这可实现对行为异常连接的自动关闭，而无需编写显式规则。默认值为 0，表示未设置阈值，因此不会因任何事件导致连接关闭。典型事件包括：尽管已通过 "accept-unsafe-violations-in-http-response" 接受，但仍格式错误的头。此处的非零值通常应设为数百或数千，以在不影响轻微异常服务器的前提下生效。也可通过使用 "tune.glitches.kill.cpu-usage" 实现仅在 CPU 使用率超过特定水平时才终止连接。请注意，当达到配置阈值的 75% 时，将尝试优雅关闭，方法是在适用的情况下通告 "Connection: close"。这确保了轻微异常的连接将在一段时间后停止使用，同时避免中断正在进行的传输。

另请参阅：tune.h1.fe.glitches-threshold、bc_glitches 以及 tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

设置 HTTP/1 前端连接上允许的错误事件阈值，当错误事件数量超过该阈值时，该连接将被自动终止。这可实现对行为异常连接的自动终止，而无需编写显式的规则。默认值为 0，表示未设置阈值，因此不会因任何事件导致连接关闭。典型事件包括：尽管已通过 "accept-unsafe-violations-in-http-request" 接受，但格式不正确的头。此处的非零值通常应设为数百或数千，以在不影响轻微不合规客户端的前提下生效。也可通过使用 "tune.glitches.kill.cpu-usage" 实现仅在 CPU 使用率超过特定水平时终止连接。请注意，当达到配置阈值的 75% 时，将尝试优雅关闭，在适用的情况下通告 "Connection: close"。这确保轻微不合规的客户端有机会建立新连接并继续正常工作，而不会触发硬关闭，从而避免中断正在进行的传输。

另请参阅：tune.h1.be.glitches-threshold、fc_glitches 和 tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

启用（'on'）或禁用（'off'）H1 多路复用器的数据零拷贝接收。默认启用。

另请参阅：tune.disable-zero-copy-forwarding、tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

启用（'on'）或禁用（'off'）H1 多路复用器的数据零拷贝发送。默认情况下已启用。

另请参阅：tune.disable-zero-copy-forwarding、tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

设置后端连接的异常事件阈值，当连接的异常事件次数达到该阈值时，连接将被自动终止。这可实现对行为异常连接的自动终止，而无需编写显式的规则。默认值为 0，表示未设置阈值，因此不会因任何事件导致连接关闭。请注意，某些 H2 服务器在长时间连接期间偶尔会产生少量异常事件，因此此处的非零值应设为数百或数千，以确保有效且不影响轻微异常的服务器。也可通过使用 "tune.glitches.kill.cpu-usage" 实现仅在 CPU 使用率超过特定水平时终止连接。请注意，当达到配置阈值的 75% 时，将尝试优雅关闭连接，方法是为未来流发送 GOAWAY 通知。这确保了轻微异常的连接将在一段时间后停止使用，同时避免中断正在进行的传输。

另请参阅：tune.h2.fe.glitches-threshold、bc_glitches 以及 tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

设置传出连接的 HTTP/2 初始窗口大小，即服务器在等待 HAProxy 确认前可响应的字节数。此设置仅影响负载内容，不影响头信息。未设置时，采用由 tune.h2.initial-window-size 定义的默认值。适度增大该值可提升下载速度或降低服务器 CPU 使用率，但可能导致客户端间不公平。建议改用 tune.h2.be.rxbuf，该设置不会引发不公平现象。此设置不影响资源使用。

另请参见：tune.h2.initial-window-size。

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

设置每个出站连接的 HTTP/2 最大并发流数（即单个连接上对服务器的未完成请求数量）。未设置时，将使用 tune.h2.max-concurrent-streams 的默认值。将该值设为低于默认值 100 可能会提升网站的响应速度，但会增加与服务器保持的已建立连接数量。当设置 "http-reuse" 为 "always" 时，建议降低此值，以避免在同一连接上混合过多不同客户端，因为若某个客户端较慢，一种称为“队首阻塞”的机制容易导致共享该连接的所有客户端下载速度出现级联下降（此时建议保持 tune.h2.be.initial-window-size 较低）。强烈建议不要提高此值；部分用户可能发现设置为较低值（通常为 1 至 5）更为理想。

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

设置后端连接上一次最多处理的 HTTP/2 入站帧数量。当处理非常大的缓冲区时，将其设置为较低值（几十到几百）可能有助于维持较低延迟，并在多个连接之间实现更好的公平性。默认值为 0，表示不施加任何限制。

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

设置出站连接的 HTTP/2 接收缓冲区大小，单位为字节。该大小将向上舍入至 tune.bufsize 的下一个倍数，并在所有上传数据的流（包括 HEADERS 和 DATA 帧）之间共享。无论如何，每个流始终会分配一个缓冲区，未使用的缓冲区中 7/8 的空间将在下载负载的流之间共享，从而显著提升上传性能，并避免在多个客户端共享后端连接且 http-reuse 设置为 "always" 时出现队首阻塞（HoL）。每个流的通告窗口大小会自动调整以反映可用空间，因此实际上无需手动调整 tune.h2.be.initial-window-size。若设置的大小不足以应对所有流，则将使用该最小值。默认值约为 1600k（100 个流，每个流 16kB 缓冲区）。

另请参阅：tune.h2.be.initial-window-size、tune.h2.fe.rxbuf、http-reuse。

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

设置前端连接上允许的异常事件次数阈值，当连接的异常事件次数达到该阈值时，连接将被自动终止。这可实现对行为异常连接的自动终止，而无需编写显式的规则。默认值为 0，表示未设置阈值，因此不会因任何事件导致连接关闭。请注意，某些 H2 客户端在长时间连接期间可能偶尔引发少量异常事件，因此此处的非零值应设为数百或数千，以在不影响轻微异常客户端的前提下有效发挥作用。也可通过使用 "tune.glitches.kill.cpu-usage" 实现仅在 CPU 使用率超过特定水平时才终止连接。请注意，当达到配置阈值的 75% 时，将尝试优雅关闭连接，方法是为未来流发送 GOAWAY 消息。这确保了轻微不合规的客户端有机会建立新连接并继续正常工作，而不会触发硬关闭，从而避免中断正在进行的传输。

另请参阅：tune.h2.be.glitches-threshold、fc_glitches 和 tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

设置传入连接的 HTTP/2 初始窗口大小，即客户端在等待 HAProxy 确认前可上传的字节数。此设置仅影响负载内容（即 POST 请求的正文），不影响头信息。未设置时，采用 tune.h2.initial-window-size 定义的默认值。适当增大该值可提升上传速度。默认值等于 tune.bufsize（16384），在 100 毫秒延迟下可支持每流至少 1.25 Mbps 的带宽，在 1 毫秒延迟下可支持 125 Mbps。该设置不影响资源使用。若设置过大，当页面与大文件上传并行访问时，可能导致客户端响应迟滞。建议改用 tune.h2.fe.rxbuf，该设置不会造成不公平性。

另请参见：tune.h2.initial-window-size。

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

设置每个入站连接的 HTTP/2 最大并发流数（即客户端单个连接上未完成的请求数量）。未设置时，将使用 `tune.h2.max-concurrent-streams` 定义的默认值。在高延迟网络上，对于包含大量小对象的复杂站点，设置大于默认值 100 的值有时可略微改善页面加载时间，但也可能导致客户端一次性占用更多资源，从而增加内存使用。默认值 100 通常已足够，建议不要更改此值。较高的并发度在处理大量连接且每个连接本身使用多个流时，会对处理负载和延迟产生影响，并可能降低拒绝服务攻击的门槛。该命令支持在数字之后添加以下可选参数：

- rq-load { `<number>` \| auto \| ignore }:

```text
可选参数 "rq-load" 允许根据执行线程的运行队列负载动态调整通告的并发数：
只要线程负载低于指定阈值，就通告配置的流数量上限。
当线程负载超过配置的限制时，通告的流数量上限将按超出比例的平方成反比降低。
目标负载设为 50 到 100 时，通常能在高负载下实现很好的调节效果。
除了显式指定数值，也可使用默认关键字 "ignore"，表示不根据线程的运行队列负载
调节通告的流数量上限；还可使用 "auto"，将该限制设为 "tune.runqueue-depth" 的值，
通常无需进一步调整配置即可获得良好效果。
```

- min `<number>`:

```text
设置使用 rq-load 时通告的最低并发数，即使这会导致负载超过配置的目标。
这样可以让站点在极高负载下仍保持良好的交互能力。最小值和默认值均为 1，
但 5 到 15 之间的值可能改善用户体验。
```

示例：

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

设置前端连接上一次最多处理的 HTTP/2 入站帧数量。当处理非常大的缓冲区时，将其设置为较低值（几十到几百）可能有助于保持低延迟，并在多个连接之间实现更好的公平性。默认值为 0，表示不施加限制。

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

设置前端连接上同时处理的 HTTP/2 RST_STREAM 的最大数量。当接收到指定数量的 RST_STREAM 帧后，连接处理器将被放入低优先级队列，并在所有其他任务之后处理。将此值设为非常低的数值（1 或几个单位）可能有助于显著降低 RST_STREAM 洪水带来的影响。RST_STREAM 在用户点击浏览器中的停止按钮时确实会发生，但由此引起的额外毫秒延迟通常难以察觉，不过通常能有效显著降低此类洪水造成的负载。默认值为零，表示不施加限制。

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

设置每个入站连接处理的 HTTP/2 最大总流数。达到此限制后，HAProxy 将发送一个优雅的 GOAWAY 帧，通知客户端在所有待处理流关闭后将关闭连接。实际上，客户端在收到该帧后通常会尽快关闭连接，并为后续请求建立新连接。在某些客户端长时间保持连接且导致服务器组内部负载失衡的情况下，这种行为有时是有用且期望的。例如，在某些高度动态的环境中，可能需要动态实例化新的负载均衡器以应对负载增加，而在负载下降后应停止这些实例，同时不中断已建立的连接。通过在此处设置限制，连接将具有有限的生命周期，并会被频繁重连，部分连接可能被建立到其他节点，从而实现现有资源的快速释放。

必须理解，此限制与上方的 "tune.h2.fe.max-concurrent-streams" 存在隐式关联。实际上，HAProxy 会始终接受客户端与前端之间可能正在传输的任何待处理流，因此所声明的限制值将始终自动增加 max-concurrent-streams 中配置的数值，该数值将作为硬性上限，任何不合规客户端超过此上限的行为都将导致连接被关闭。因此，在从日志中统计每个连接的请求数量时，可能观察到的数值介于 max-total-streams 与 (max-total-streams + max-concurrent-streams) 之间，具体取决于客户端创建流的速度。

默认值为 0，表示除协议本身隐含的限制外（2^30 ≈ 10.7 亿）不施加任何限制。数值接近 1000 时，可能已导致大多数客户端无感知延迟的情况下频繁重连。设置过低可能导致因频繁 TLS 重连而增加 CPU 使用率，同时加重页面加载时间。请注意，部分负载测试工具不支持重连，使用此设置时可能报告错误；因此在运行性能基准测试时可能需要禁用该设置。参见 "tune.h2.fe.max-concurrent-streams"。

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

设置传入连接的 HTTP/2 接收缓冲区大小，单位为字节。该大小将向上舍入至 tune.bufsize 的下一个倍数，并在所有上传数据的流（包括 HEADERS 和 DATA 帧）之间共享。无论如何，每个流始终会分配一个缓冲区，未使用的缓冲区中 7/8 的空间将在上传有效载荷的流之间共享，从而显著提升上传性能。每个流的通告窗口大小会自动调整以反映可用空间，因此实际使用中通常无需手动调整 tune.h2.fe.initial-window-size。若设置的值小于处理所有流所需的最小值，则将采用该最小值。默认值 1600k（100 个流，每个流 16kB 缓冲区）可支持客户端在 100ms RTT 下实现约 130 Mbps 的上传速度。

另请参见：tune.h2.fe.initial-window-size 和 tune.h2.be.rxbuf。

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

设置 HTTP/2 动态头表大小。默认值为 4096 字节，最大不得超过 65536 字节。较大的值可能有助于某些客户端发送更紧凑的请求，具体取决于其能力。每个 HTTP/2 连接都会消耗此数量的内存。建议不要更改此值。

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

设置 HTTP/2 初始窗口大小的默认值，适用于入站和出站连接。当未设置 tune.h2.fe.initial-window-size 时，该值用于入站连接；当未设置 tune.h2.be.initial-window-size 时，该值用于出站连接。此设置既作为每流的初始值，也作为每流的最小值。默认值为 16384（即 tune.bufsize），在 100 ms 网络延迟下，此值大致允许每流上传带宽不低于 1.25 Mbps，或在 1 ms 本地网络下不低于 125 Mbps。当接收缓冲区使用量低于 tune.h2.be.rxbuf 和 tune.h2.fe.rxbuf 所定义的上限时，未使用的缓冲区将在接收流之间共享。因此，通常无需更改此默认设置。由于更改此默认值会同时提高上传速度并加剧客户端间下载的不公平性，建议改用针对方向的设置 tune.h2.fe.initial-window-size 和 tune.h2.be.initial-window-size。

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

设置 H2 解复用器中将生成日志的错误级别。默认值为 "stream"，表示解复用器中遇到的任何解码错误都会触发日志输出。"connection" 值表示仅当错误导致连接失效时才生成日志。最后，"none" 表示任何解码错误都不会生成日志。建议至少设置为 "connection"，以便检测协议异常，即使在困难时期暂时切换至 "none" 也应如此。

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

设置每个连接的默认 HTTP/2 最大并发流数（即单个连接上未完成的请求数量）。当未设置 tune.h2.fe.max-concurrent-streams 时，该值用于入站连接；当未设置 tune.h2.be.max-concurrent-streams 时，该值用于出站连接。默认值为 100。影响因方向而异，请参阅上述两个设置以获取详细信息。建议不要使用此设置，而改用按方向设置的选项。设为零将禁用限制，单个客户端可创建尽可能多的流，只要 HAProxy 可分配即可。强烈建议不要修改此值。

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

设置 HAProxy 向对等节点通告其愿意接收的 HTTP/2 最大帧大小。默认值为 16384 与缓冲区大小（tune.bufsize）中的较大者。无论如何，HAProxy 不会通告支持超过缓冲区大小的帧大小。此设置的主要目的是在使用大缓冲区时，限制最大帧大小的设定。过大的帧大小可能影响性能，或导致某些对等节点行为异常。强烈建议不要更改此值。

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

启用（'on'）或禁用（'off'） H2 多路复用器的数据零拷贝发送。默认启用。

另请参阅：tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

设置捕获的 Cookie 的最大长度。此值为“capture cookie xxx len yyy”允许设置的最大值，任何超过该值的配置将自动截断至该值。务必不要将此值设置得过高，因为无论配置值为何，所有 Cookie 捕获均会按此大小分配内存（它们共享同一内存池）。该值按每个请求每响应计算，因此每连接分配的内存为该值的两倍。未指定时，默认限制为 63 个字符。建议不要修改此值。

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

设置日志中请求 URI 的最大长度。这可防止日志行中截断包含重要查询字符串的长请求 URI。此设置与 syslog 限制无关。若增大此限制，也应相应增加 'log ... len yyy' 参数。syslog 守护进程也可能需要特定的配置指令。默认值为 1024。

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

设置接收的 HTTP 消息中允许的最大头数量。当消息包含的头数量超过此值（包括首行）时，请求将被拒绝并返回“400 Bad Request”状态码，响应则返回“502 Bad Gateway”状态码。默认值为 101，该值足以满足所有使用场景，考虑到广泛部署的 Apache 服务器也采用相同的限制。在应用程序修复前，适当提高此限制可临时允许存在缺陷的应用程序正常运行。允许的取值范围为 1..32767。请注意，每个新头在每个流中会消耗 32 位内存，因此请勿将此限制设置得过高。

请注意，HTTP/1.1 是文本协议，因此在发送消息时并无特殊限制。消息解析阶段的限制已足够。HTTP/2 和 HTTP/3 为二进制协议，需要编码步骤。在对头进行编码以符合协议限制时，也设置了相应限制。该限制值足够大，但出于故意未予文档化。出于相同原因，解码的初始步骤也应用了相同的限制。

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

控制同一服务器的空闲连接池在多线程间的共享。可设置为在同一线程组内的所有线程中启用（'on'），在所有线程中启用（'full'），或禁用（'off'）。默认值为在同一线程组内的线程间共享连接池（'on'），以最小化对服务器的持久连接数量，并优化连接复用率。与其它线程组的线程共享连接池可能带来性能影响，因此默认不启用，但在优先考虑最大化连接复用时可能有用。为便于调试或在怀疑 HAProxy 在连接复用方面存在缺陷时，可方便地强制禁用多线程间的空闲连接池共享，并将此选项设为 'off'。强烈建议在禁用此选项时，为依赖连接复用以实现高性能的全部服务器设置保守的 "pool-low-conn" 值，否则随着线程数量增加，连接可能被频繁关闭。

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

设置 HAProxy 在认为空缓冲区可能与空闲流相关联之前等待的时长。该设置用于在转发大块和小块数据时，优化调整某些数据包大小。是否使用 splice() 或在 SSL 中发送大缓冲区，由该参数调节。值的单位为毫秒，范围在 0 到 65535 之间。值为 0 表示 HAProxy 不会尝试检测空闲流。默认值为 1000，该值似乎能正确识别终端用户暂停（例如，阅读页面后再点击）。不应更改此值。请查阅下方的 tune.ssl.maxrecord。

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

默认情况下，所有“bind”指令将创建单个分片，即一个由进程内所有线程监听的单一套接字。当线程数量较多时，这种做法效率不高，甚至可能在内核中引入显著开销，例如更新轮询状态或向各个线程分发事件。现代操作系统支持入站连接的负载均衡机制，该机制允许将多个套接字绑定到同一地址和端口，并将所有入站连接均匀地分发到这些套接字，使得每个线程仅看到其绑定套接字中等待的连接。这显著降低了内核侧开销，并提升了入站连接路径的性能。

通常通过在“bind”指令中使用“shards”设置来启用此功能，其默认值为 1，表示每个监听器在进程内唯一。在多处理器系统上，将默认设置更改为 “by-thread”（以确保每个线程始终创建一个监听套接字）或 “by-group”（以确保每个线程组始终创建一个监听套接字）可能更为便利。使用“by-thread”时请注意文件描述符的使用情况，因为每个监听器需要的套接字数量等于线程总数。此外，某些操作系统（如 FreeBSD）对同一地址的套接字数量有限制，最多不超过 256 个。

请注意，“by-group”在默认配置（仅涉及一个线程组）下等同于“by-process”，在不支持该机制的系统上将回退至共享同一套接字。默认设置为“by-group”，在不支持多绑定的系统或套接字族上将回退至“by-process”。

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

启用（'on' / 'fair'）或禁用（'off'）监听器的多队列接受机制，该机制将传入流量分散到所有“bind”指令允许运行的线程，而非由单个线程独占。此机制可实现更平滑的流量分发，并显著提升扩展性，尤其适用于因外部活动（例如网络中断与某一特定线程冲突）导致线程负载不均的环境。默认模式 'on' 通过采样选择连接数最少的线程，优化线程选择。当连接为长连接时，此模式通常为最佳选择，能够有效保持所有线程处于繁忙状态。第二种模式 'fair' 则不考虑当前负载水平，循环遍历所有线程。该模式更适合短连接场景，或在拥有大量线程的机器上使用，此时第一种模式找到负载最低线程的概率较低。最后，可通过设置 'off' 强制禁用负载均衡机制，用于故障排查，或在连接为短连接且操作系统已提供足够良好分发的情况下使用。默认值为 'on'。

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

明确告知 HAProxy 在将 HAProxy 样本对象推送至 Lua 时应如何处理。实际上，当使用原生转换器、从 Lua 脚本中提取样本或使用变量时（仅举几例），HAProxy 会将内部的 smp 类型转换为等效的 Lua 类型。由于历史实现原因，布尔值处理存在歧义：在执行 Lua → HAProxy smp 转换时，布尔值能正确保留；但在执行 HAProxy smp → Lua 转换时，布尔值被错误地转换为整数。这意味着，当从 Lua 中调用返回布尔值的样本提取或转换器时，会返回整数 0 或 1。不幸的是，在 Lua 中，布尔值与整数不可互换。因此，为避免歧义，"tune.lua.bool-sample-conversion" 必须显式设置为 "normal"（表示放弃历史行为以提升一致性）或 "pre-3.1-bug"（强制保留历史行为，防止现有脚本逻辑出现异常）。若未显式设置该选项，且配置中加载了 Lua 脚本，HAProxy 将发出警告，该选项将隐式默认为 "pre-3.1-bug"，以保持与历史行为一致。建议在确认正在使用的 Lua 脚本能够正确处理布尔类型的 HAProxy 样本后，将此选项设置为 "normal"。

该设置必须在任何 "lua-load" 或 "lua-load-per-thread" 指令之前设置才有效，否则将被忽略。

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

“burst” 执行超时适用于任何 Lua 处理器。如果处理器在超时到达前未能完成或主动让出控制权，将被中止，以防止线程争用，避免流量长时间无法被处理，并最终防止因看门狗触发而导致进程崩溃。与其它 Lua 超时机制不同，burst-timeout 不是基于 yield 累积的，而是确保单次 Lua 执行窗口内所花费的时间不超过配置的超时值。

此处“yield”表示 Lua 执行被有效中断，可能是通过显式调用 Lua 休眠函数（如 core.(m)sleep() 或 core.yield()），或因自动强制休眠（参见 tune.lua.forced-yield）所致，且将在相关任务被设置为重新调度时稍后恢复。并非所有 Lua 处理器均可休眠：必须区分可休眠处理器与不可休眠处理器。

对于可让出的处理器（任务、动作等），达到超时意味着 "tune.lua.forced-yield" 可能过高，降低该值可能改善情况，但也建议检查在 Lua 函数的关键点手动插入 yield 是否有助于缓解问题。这还可能表明处理器在某个无法中断的 Lua 库函数中花费了过多时间。

对于不可让出的处理器（Lua 转换器、样本提取），这可能仅表示处理器正在进行过多的计算，这可能是由于设计不当所致，因为此类处理器通常会阻塞请求执行流程，应尽快终止以确保请求处理得以继续。此处常见的解决方法是尝试进一步优化 Lua 函数以提升速度，因为减少 "tune.lua.forced-yield" 并无帮助。

此超时仅计算纯 Lua 运行时。若 Lua 执行 core.sleep，睡眠时间不计入超时。默认超时为 1000 ms。

请注意：如果从处理程序中启动了 Lua 垃圾回收周期（无论是显式请求还是在经过一段时间后由 Lua 自动触发），该垃圾回收周期所花费的时间也将被计入。

实际上，无法推断垃圾回收（GC）周期时间，因此在系统饱和时可能导致一些误报（此时 GC 难以跟上进度，并消耗了大部分可用执行时间）。如果出现这种情况，可参考以下解决方向：

    - 检查是否可通过优化脚本来减少 Lua 的内存占用
    - 微调 Lua 的 GC 参数，或手动触发 GC 周期，也可同时采用这两种方法
      （参见：https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage）
    - 增大 tune.lua.burst-timeout

将值设为 0 会完全禁用此保护机制。

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

该指令强制 Lua 引擎在每执行 `<number>` 条指令后进行一次 yield 操作。
这允许中断长时间运行的脚本，并使 HAProxy 调度器能够处理其他任务，例如接收连接或转发流量。
默认值为：使用 "lua-load-per-thread" 加载的脚本为 10000 条指令；使用 "lua-load" 加载的脚本为 MAX(500, 10000 / nbthread) 条指令（该值被证实为在兼顾性能的同时，有效避免多个线程竞争全局 Lua 锁所导致的线程争用问题的最优选择）。

如果 HAProxy 频繁执行某些 Lua 代码但需要更高的响应性，可降低此值。若 Lua 代码较长且其结果必须用于处理数据，可增加 `<number>`，但应谨慎设置，因为在多线程环境下可能增加竞争。

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

启用（'on'）或禁用（'off'）通过当前代理适用的日志记录器记录 Lua 脚本的输出，若存在适用的日志记录器。

默认值为 'on'。

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

启用（'on'）或禁用（'off'）通过 stderr 记录 Lua 脚本的输出。当设置为 'auto' 时，若满足以下任一条件，则通过 stderr 的日志记录将自动启用：

    - tune.lua.log.loggers 设置为 'off'
    - 脚本在非代理上下文中执行，且没有全局日志记录器
    - 脚本在代理上下文中执行，且未关联日志记录器

请注意，启用后，此日志记录将与通过 tune.lua.log.loggers 配置的日志记录并存。

默认值为 'auto'。

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

设置每个进程可用于 Lua 的最大内存容量（单位：兆字节）。默认值为 0，表示无限制。必须设置限制，以确保脚本中的缺陷不会导致系统内存耗尽。

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

选择在初始化 Lua 状态时加载的 Lua 标准库。参数为从以下集合中选取的库名称组成的逗号分隔列表：table、io、os、string、math、utf8、package、debug。可使用特殊值 "all" 或 "none" 替代列表。"none" 不能与库名称同时使用。默认值为 "all"。

无论此设置如何，基础库和协程库始终会被加载：base 提供 HAProxy 依赖的核心 Lua 函数，而 coroutine 是必需的，因为 HAProxy 用其自身的安全实现覆盖了 coroutine.create()。

请注意，无论此设置如何，HAProxy 默认已阻止 fork() 和新建线程操作，且仅可通过全局指令 "insecure-fork-wanted" 重新启用。进一步限制可加载库的集合可降低 Lua 脚本暴露的攻击面。具体包括：   - 省略 "os" 可防止使用 os.execute() 和 os.exit()   - 省略 "io" 可防止使用 io.open() 和 io.popen()   - 省略 "package" 可防止通过 require() 加载原生 C 模块   - 省略 "debug" 可防止通过 debug.getupvalue()、debug.getmetatable() 或 debug.sethook() 探查 HAProxy 内部结构

示例：

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

此设置必须在任何 "lua-load"、"lua-load-per-thread" 或 "lua-prepend-path" 指令之前设置，否则将返回解析错误。

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

这是 Lua 服务的执行超时。该设置有助于防止出现无限循环或在 Lua 中花费过多时间。此超时仅计算纯 Lua 运行时时间。若 Lua 执行了睡眠操作，该睡眠时间不计入超时。默认超时时间为 4s。

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

这是 Lua 会话的执行超时时间。该设置有助于防止出现无限循环或在 Lua 中花费过多时间。此超时仅计算纯 Lua 运行时时间。若 Lua 执行了睡眠操作，该睡眠时间不计入超时。默认超时时间为 4s。

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

用途与 "tune.lua.session-timeout" 相同，但此超时专门用于任务。默认情况下，该超时未设置，因为任务可能在 HAProxy 的整个生命周期内保持活跃。例如，用于检查服务器的任务。

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

设置每个线程上活跃健康检查数量的阈值，当超过该阈值时，线程将主动尝试寻找负载较低的线程来执行健康检查，或将其排队，直到该线程上正在运行的活跃健康检查数量减少。默认值为 0，表示未设置此类限制。在某些环境中，当使用大量线程运行极多昂贵的健康检查时，若负载分布不均，可能导致健康检查在启动时随机超时，尤其是在使用 OpenSSL 3.0 时，其健康检查的 CPU 消耗约为旧版本的 20 倍。此设置将有助于在所有线程间均衡健康检查负载。绝大多数配置无需调整此参数。请注意，过低的值可能导致健康检查执行缓慢时显著降低检查效率。

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

设置进程在切换至其他工作前可连续接受的最大连接数。在单进程模式下，较高的数值曾在高连接速率下带来更好的性能，但随着多队列机制的引入，这一情况已不再成立。该值对每个监听器独立生效，因此会考虑监听器绑定的进程数量。默认值为 4，该值表现最佳。若从旧配置中继承了显著更高的数值，可考虑将其移除，此举既能提升性能，又能降低响应时间。在多进程模式下，该值将除以监听器绑定进程数的两倍。将该值设为 -1 可完全禁用此限制。通常无需调整此值。

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

设置单次调用轮询系统时可处理的最大事件数。默认值会根据操作系统自动调整。观察发现，将该值降低至 200 以下会略微降低延迟，但会牺牲网络带宽；将该值提高至 200 以上则会以牺牲延迟为代价换取略增的带宽。配置的值必须小于或等于 1000000。

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

设置保留缓冲区空间的大小（以字节为单位）。保留空间用于头重写或追加。套接字的首次读取操作永远不会填满超过 bufsize - maxrewrite 的空间。历史上，该值默认为 bufsize 的一半，但这种设定并无太大意义，因为通常无需添加大量头。设置过高会阻碍大型请求或响应的处理；设置过低则会妨碍向已较大的请求或 POST 请求中添加新头。通常建议将其设为约 1024。若该值大于 bufsize 的一半，将自动调整为 bufsize 的一半。这意味着在调整 bufsize 时无需担心此值。

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

设置在规则集评估函数中可同时评估的最大规则数量，前提是这些规则支持中断（yielding）。实际上，配置中存在大量“tcp-request content”或“http-request”规则的情况并不少见。当大量规则与高 CPU 消耗的动作（例如：处理内容的动作）结合时，若评估未被中断，同一规则集中的所有规则均在同一个轮询循环中执行，可能导致线程争用。此选项确保对于面向内容的规则集（因内容检查已支持 yielding 的规则集），同一轮询循环中最多仅执行 `<number>` 条规则。其作用是强制评估函数中断，以便在下一个轮询循环中恢复评估。

受影响的规则集包括：

- tcp-request content
- tcp-response content
- http-request
- http-response

默认值为 50。

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

设置每个线程在本地缓存中保持热态且永不被其他线程回收的内存大小。对该内存的访问速度极快（无锁），在高线程竞争情况下，保持足够的内存大小对维持良好性能至关重要。该值以字节为单位，其默认值在构建时通过 CONFIG_HAP_POOL_CACHE_SIZE 配置，缺省值为 524288（512 kB）。在某些使用场景中，增大该值可能提升性能，特别是当性能分析显示内存分配压力较大时。经验表明，一个合适的值通常介于每个 CPU 核心 L2 缓存大小的 1 到 2 倍之间。值过大将因 CPU L3 缓存利用效率低下而对性能产生负面影响，并消耗更多内存。建议不要修改此值，或仅以小幅度逐步调整。若要完全禁用每个线程的 CPU 缓存，可设置极小值，但更推荐在命令行中使用 "-dMno-cache"。

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

调整内核的每个套接字缓冲区大小，使得当缓冲区中的数据量达到该值加上测量到的窗口大小时，报告套接字发送端已满。其原理是仅在套接字缓冲区中保留最少必需的字节数，并额外预留一小部分缓冲空间，以覆盖 HAProxy 尝试再次发送数据时可能传输的数据量。将该值设为较低值（通常约为 tune.bufsize）可显著降低系统缓冲区的内存占用，并减少因刷新缓冲数据而产生的应用层延迟。对于支持该特性的系统，此设置通常比 tune.sndbuf.client 和 tune.sndbuf.server 更为有效且准确。该设置按连接生效（根据配置，针对客户端连接或服务器连接），仅适用于 TCP 连接。默认值为 0，表示无限制。此功能仅在 Linux 系统上可用。

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

设置模式查找缓存的大小为 `<number>` 项。该缓存为 LRU 缓存，用于记忆先前的查找及其结果。它在 ACL 和映射中用于慢速模式查找，即使用 "sub"、"reg"、"dir"、"dom"、"end"、"bin" 匹配方法以及不区分大小写的字符串时。该设置适用于模式表达式，意味着它能够记忆配置行中指定的所有模式（包括从文件加载的模式）的查找结果。当通过 HTTP 动作或 CLI 更新条目时，缓存会自动失效。默认缓存大小为 10000 项，这使得在 32 位系统上每个进程/线程的内存占用约为 5 MB，在 64 位系统上约为 8 MB，因为缓存是线程/进程本地的。该缓存发生冲突的风险极低，约为缓存大小除以 2^64 的数量级。通常，在默认缓存大小为 10000 项、每秒处理 10000 个请求的情况下，暴力攻击在 60 年后导致单次冲突的概率为 1%，在 6 年后为 0.1%。该风险被认为远低于由老化组件引起的内存损坏风险。若此风险不可接受，可通过将该参数设为 0 来禁用缓存。

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

设置 HAProxy 在发送消息时一次性尝试处理的最大 stick-table 更新数量。获取这些更新的数据需要执行一些锁定操作，若未加限制，在多线程机器上可能造成较高的 CPU 消耗，也可能在旧进程与新进程之间的初始批量传输期间增加延迟。相反，过低的值也可能导致更高的 CPU 开销，并延长完成时间。默认值为 200，建议不要更改。

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

设置内核管道缓冲区大小为指定值（以字节为单位）。默认情况下，管道大小为系统默认值。但在使用 TCP 拼接时，增大管道大小有时可提升性能，特别是当怀疑管道未被填满且频繁调用 splice() 时。此设置会影响内核的内存占用，因此在未充分理解其影响前，不得更改。

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

此设置定义了 HAProxy 全局使用的文件描述符最大数量（以百分比表示），相对于 HAProxy 在无法复用连接且必须创建新连接时可使用的文件描述符上限。当空闲连接被终止时，该值用于控制可保留的空闲连接数量。默认值为 25（即文件描述符总量的四分之一），这意味着大约一半的最大前端连接数可以维持空闲连接。在一般情况下，超过此值通常并无实际意义，尤其是在以连接复用为目标时。

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

此设置用于定义 HAProxy 全局使用的文件描述符最大数量（以百分比表示），该数值相对于 HAProxy 在停止将连接放入空闲池以供复用之前可使用的文件描述符上限。默认值为 20。

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

启用（on）或禁用（off）透传多路复用器的数据零拷贝转发功能。需配合内核拼接（splicing）功能使用。默认启用。

另请参阅：tune.disable-zero-copy-forwarding、option splice-auto、option splice-request 和 option splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

定义 Cubic 拥塞控制算法真正将丢包事件视为拥塞事件所需的丢包数量。通常情况下，任何丢包事件均被视为拥塞所致，且足以使 Cubic 从较小的窗口重新开始。但实验表明，丢包可能由多种非拥塞原因引起，可简单归类为误判丢包，此时调整窗口大小并无实际效果，只会降低通信速率。信号质量差、报文乱序到达、客户端 CPU 使用率过高导致随机延迟，以及系统定时器精度不足等，均可能成为此类丢包的常见原因。该设置允许 Cubic 对误判丢包更具容忍度，通过调整两个 ACK 之间累计丢包数量以判定为丢包事件的最小值，其默认值为 1。实验中已观察到显著性能提升，但始终伴随重传所浪费带宽的增加，以及拥塞链路饱和风险的上升。值 2 可用于短时间内的指标对比。未经专家事先分析，切勿将该值设为超过 2。默认值和最小值均为 1。始终使用 1。

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

启用（on）或禁用（off）用于 QUIC 连接的 HyStart++（RFC 9406）算法，该算法可替代拥塞控制算法的慢启动阶段，避免造成高丢包率。默认情况下处于禁用状态。

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

设置单个 QUIC 帧被标记为丢失的上限。超过该上限时，连接被视为失败，并立即关闭。

默认值为 10。

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

设置前端或后端侧单个 QUIC 连接的拥塞控制器的默认最大窗口大小。值必须以整数形式书写，可选后缀为 'k'、'm' 或 'g'。取值范围必须在 10k 至 4g 之间。

QUIC 多路复用器在数据发送时，也使用当前的拥塞窗口大小来判断是否可以分配新的流缓冲区。因此，最大拥塞窗口大小同样作为该分配器的限制。

默认值为 480k。

另请参见 "quic-cc-algo" 绑定和服务器选项。

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

应用于计算数据包重排序阈值的比率。若设置过小，可能触发高数据包丢失检测。

默认值为 50。

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

设置前端或后端侧的 QUIC max_idle_timeout 传输参数。该参数遵循 HAProxy 的时间格式，单位为毫秒。此参数决定在连接于有效时间段内保持空闲后，经过多长时间将被静默关闭。两端均依赖于协商后的相同值：— 若两者均非空，则取两者中的最小值；— 若仅有一方非空，则取非空值；— 若两者均为空，则此功能被禁用。

默认值为 30 秒。

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

设置前端或后端侧每连接的故障阈值，当连接的故障次数达到该阈值时，连接将被自动终止。这可实现对行为异常连接的自动终止，而无需编写显式的规则。默认值为 0，表示未设置阈值，因此不会因任何事件导致连接关闭。请注意，某些 QUIC 客户端在长时间连接期间可能偶尔引发少量故障，因此此处的非零值建议设为数百或数千，以在不影响轻微异常客户端的前提下生效。也可通过使用 "tune.glitches.kill.cpu-usage" 实现仅在 CPU 使用率超过特定水平时终止连接。

另请参阅：fc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

动态启用所有已配置的 QUIC 监听器的重试功能，一旦达到此数量的半开连接。半开连接是指握手尚未成功完成或失败的连接。此设置需配置集群密钥方可生效，否则将被静默忽略（参见“cluster-secret”设置）。若强制使用 QUIC 重试（参见“quic-force-retry”设置），此设置也将被静默忽略。

默认值为 100。

有关 QUIC 重试的更多信息，请参见 <https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2>。

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

指定全局范围内 QUIC 前端连接在接收和发送操作中如何使用套接字。
连接可共享监听器套接字，或每个连接可分配独立的套接字。

默认值为 "default-on"。该选项用于为每个 QUIC 连接分配专用套接字。在处理大量 QUIC 流量时，此选项是实现最佳性能的首选方式。这也是确保 QUIC 连接在执行软停止时能正确处理且不丢失数据的唯一方法，同时可高效处理 sendto() 操作期间的瞬时错误情况。然而，该选项依赖于 UDP 网络栈的某些高级功能。如果系统平台被判定为不兼容，HAProxy 将在启动时自动切换至 "force-off" 模式。请注意，运行在特权端口上的 QUIC 监听器可能需要以 uid 0 身份运行，或需进行特定操作系统调优以允许目标 uid 绑定此类端口，例如使用系统能力。参见 "setcap" 全局指令。

“force-off” 值表示 QUIC 传输将在共享监听器套接字上进行。对于小流量场景，此选项可作为良好折衷方案，有助于降低文件描述符（FD）消耗。然而，由于在多个线程间共享监听器或同时使用大量 QUIC 连接时会导致更高的 CPU 使用率，性能无法达到最优。

此设置与每个“quic-socket”绑定选项同时生效。若全局调优中使用“default-on”模式，将对每个监听器生效，但“quic-socket listener”除外。若全局使用“force-off”模式，则将应用于每个监听器实例，无论其独立配置如何。

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

3.3 版本中已弃用此关键字，将在 3.5 版本中移除。该关键字属于对 QUIC 配置进行简化处理的一部分。新选项名为 "tune.quic.fe.sock-per-conn"，其中旧值 "connection" 对应 "default-on"，"listener" 对应 "force-off"。

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

此设置用于配置每个流中在途数据字节数的硬性上限。该值以相对于 QUIC 流 rxbuf 连接设置的百分比表示，结果向上取整至 bufsize。

默认值为 90。此值适用于最常见的 Web 场景，即上传仅针对一个或少数几个流进行，其余流仅用于下载。若流 rxbuf 连接限制保持在合理水平，可确保仅部分已打开的流能够分配至其最大容量。

当应用程序同时使用多个并行上传流且这些流之间存在不公平现象时，降低该比例可能更为合理，以提升公平性并减少每流的带宽占用。

参见："tune.quic.be.stream.rxbuf"、"tune.quic.fe.stream.rxbuf"、"tune.quic.be.stream.max-concurrent"、"tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

在前端，此值用作通告的 initial_max_streams_bidi 传输参数的值。该值被强制作为远程对等节点在连接生命周期内可同时打开的双向流的最大数量。这有效限制了并发 HTTP/3 客户端请求的数量。

默认值为 100。请注意，若减小该值，可能会限制接收流的缓冲能力，导致上传吞吐量下降。可通过增大 QUIC 流 rxbuf 连接设置来修正此问题。

在后端侧，HAProxy 会本地强制执行此设置，以限制通过单个连接复用的并发请求数量。该限制可能进一步受到对等节点流量控制的影响。为提升站点响应速度，可适当降低默认值 100，代价是增加后端连接的打开数量。与前端侧类似，此设置同样直接影响接收缓冲区能力，但此时是限制 HTTP 下载容量。当主要处理大于 "tune.bufsize" 的 HTTP 响应时，可适当增大 QUIC 流接收缓冲区设置。

参见："tune.quic.be.stream.rxbuf"、"tune.quic.fe.stream.rxbuf"、"tune.quic.be.stream.data-ratio"、"tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

设置单个 QUIC 连接可处理的最大请求数。达到此上限后，连接将被优雅关闭。在 HTTP/3 中，这表现为 GOAWAY 帧。当所有剩余传输完成后，连接最终关闭。

此设置通过 QUIC 流控制机制作为连接的硬性限制。若对等节点违反该限制，连接将立即关闭。

此设置可用于强制客户端定期打开新的连接，以持续发送请求，并避免长时间维持连接。然而，过低的值会增加客户端的延迟，并由于 TLS 握手导致双方 CPU 消耗上升。

默认值为 0，表示除 QUIC 协议编码限制（2^60，超过百亿亿）外，无其他特定限制。

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

此设置是 QUIC 前端连接中在途数据字节数的硬性上限。该值被复用为 initial_max_data 传输参数的取值。其直接影响对等节点的上传带宽，具体取决于延迟以及 HAProxy 中每个连接的内存消耗。

默认值为 0，表示将自动根据 max-concurrent 与 bufsize 的乘积生成该值。例如，当后端应用依赖高延迟网络上的大量上传时，可适当增大此值。

参见："tune.quic.be.stream.max-concurrent"、"tune.quic.fe.stream.max-concurrent"、"tune.quic.be.stream.data-ratio"、"tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

启用（on）或禁用（off）QUIC 发送的速率控制支持。默认情况下，该功能处于激活状态。速率控制的目的是平滑数据发送，以减少网络丢包。在大多数场景下，通过避免重传可显著提升网络吞吐量。然而，在带宽极高且延迟极低的网络中，禁用该功能可防止不必要的延迟并降低 CPU 消耗。

另请参见 "quic-cc-algo" 绑定和服务器选项。

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

启用（'on'）或禁用（'off'）QUIC 发送时的 UDP GSO 支持。默认情况下，该功能处于激活状态。此内核特性允许通过单个系统调用发送多个数据报，对大容量传输更为高效。当怀疑发送环节存在问题时，可依据开发人员建议禁用该功能。

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

在前端侧禁用 QUIC 传输协议。所有 QUIC 监听器仍会创建，但不会监听传入的数据报。因此，HAProxy 在前端侧不会处理任何 QUIC 流量。

默认值为 "on"。若怀疑 QUIC 流量存在问题，可使用此选项轻松切换 QUIC 监听器，而无需逐行修改配置。

另请参见 "quic_enabled" 样本提取。

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

设置传输层 QUIC 栈可用于发送的最大内存容量。该值同时作为飞行中字节数和多路复用器输出缓冲区的上限。请注意，为避免线程竞争，此限制并非严格强制执行，因此在某些情况下可能被超出。此外，每个连接始终可使用至少 2 个数据报的窗口，因此应配合使用适当的 maxconn 设置。

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

该关键字已在 3.3 版本中弃用，并将在 3.5 版本中移除。它是对 QUIC 配置进行简化处理的一部分。若使用，此设置仅对前端连接生效。

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

启用（'on'）或禁用（'off'）QUIC 多路复用器的数据零拷贝发送。默认启用。

另请参阅：tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

该配置选项的取值范围为 -20 至 19。其调度优先级按照 man 2 setpriority 文档所述进行应用。该优先级在配置解析完成后生效，因此仅工作进程或独立进程会应用此优先级。通常将其配置为高于执行配置解析的进程（tune.renice.startup）的优先级。

另请参见：tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

此配置选项的取值范围为 -20 至 19。它会应用调度优先级，具体行为参见 man 2 setpriority 文档。该优先级在应用其余配置之前生效，若需降低配置解析过程的优先级，此设置尤为有用。该优先级在独立进程或工作进程启动后、配置解析前应用。配置解析完成后，除非使用 tune.renice.runtime，否则将恢复之前的优先级。

另请参见：tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

对于非连接套接字的内核套接字接收缓冲区大小，可设置为此值。此设置可用于监听器模式下的 QUIC 以及前端的 log-forward。默认系统缓冲区有时可能过小，无法应对大量聚合流量的接收，导致部分数据丢失，可能引发重传（QUIC 情况下），并在高流量下可能减缓连接建立速度。该值以字节为单位，对每个套接字生效。在监听器模式下，套接字在所有连接间共享，套接字总数取决于 "bind" 行的 "shards" 值。无固定最优值，合适的值应为预期每连接大小乘以预期连接数。内核可能裁剪过大的值。另请参见 "tune.rcvbuf.client" 和 "tune.rcvbuf.server" 用于连接套接字的对应设置，以及 "tune.sndbuf.backend" 和 "tune.sndbuf.frontend" 用于发送设置。

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

强制将客户端或服务器端的内核套接字接收缓冲区大小设置为指定的字节数。该值适用于所有 TCP/HTTP 前端和后端。通常不应设置此值，使用默认值（0）可让内核根据可用内存自动调整该值。然而，在某些情况下，将其设置为非常低的值（例如 4096）可能有助于节省内核内存，防止其缓冲过多接收到的数据。不过，较低的值会显著增加 CPU 使用率。

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

HAProxy 使用一些提示来判断短读操作是否表示套接字缓冲区已结束。其中之一是：读取返回的字节数超过 `<recv_enough>`，该值默认为 10136（即 7 个 1448 字节的分段）。可通过此设置调整该默认值，以更好地应对包含大量短消息的负载，例如 telnet 或 SSH 会话。

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

设置环形缓冲区前方的写入队列数量。该设置可能影响调试会话期间的 CPU 使用率，值过低或过高均可能产生显著影响。开发人员通过实验确定了合适的取值，除非为解决特定问题而被明确指示，否则不应尝试更改。此设置不应在版本升级时保留在配置中，因为其最优值可能随时间演变。

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

设置运行任务时可同时处理的最大任务数量。默认值取决于线程数，通常在 35 到 280 之间，该范围往往能实现最高的请求速率和最低的延迟。增大该值在处理 I/O 时可能导致延迟增加，设置过小则会引入额外开销。线程数较多时，较低的值更有利。在尝试使用远大于默认值的设置时，建议同时启用 tune.sched.low-latency，并可能启用 tune.fd.edge-triggered，以将最大延迟控制在最低可能水平。

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

启用（on）或禁用（off）低延迟任务调度器。默认情况下，HAProxy 会逐类处理多个任务类别中的任务，这种方式效率最高。但在设置较大的 tune.runqueue-depth 值时，这可能会对请求或连接延迟产生可测量的影响。启用此低延迟设置后，若存在低优先级类别的任务，将始终优先于其他类别执行。这可以在大规模流量期间降低新请求或连接所经历的最大延迟，但会增加对大规模流量的影响。对于常规使用，建议保持该设置为关闭状态。默认值为 off。

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

对于非连接套接字，将内核套接字发送缓冲区大小设置为此值。该设置可用于后端的 Unix 套接字和 UDP 日志记录，以及前端监听器模式下的 QUIC。默认系统缓冲区有时可能过小，尤其在多个连接（或日志发送方）共享套接字时，可能导致部分数据丢失，甚至引发重传，从而在高流量下减缓新连接的建立速度。该值以字节为单位，对每个套接字生效。在监听器模式下，套接字由所有连接共享，套接字总数取决于 "bind" 行的 "shards" 值。不存在最优值，合适的值应为预期每连接大小乘以预期连接数。内核可能会裁剪过大的值。另请参见 "tune.sndbuf.client" 和 "tune.sndbuf.server" 的连接套接字对应设置，以及 "tune.rcvbuf.backend" 和 "tune.rcvbuf.frontend" 的接收设置。

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

强制将客户端或服务器端的内核套接字发送缓冲区大小设置为指定的字节数。该值适用于所有 TCP/HTTP 前端和后端。通常不应设置此值，使用默认值（0）可让内核根据可用内存自动调优该值。然而，在某些情况下，将其设置为极低值（例如 4096）有助于节省内核内存，防止其缓冲过多接收数据。但较低值会显著增加 CPU 使用率。另一种使用场景是防止因内核等待大量缓冲区数据被读取完毕后再通知 HAProxy，而导致极慢客户端出现写超时。有关更有效的设置以更精细地控制 Linux 系统上的内存使用和响应性，同时不影响性能，请参阅 tune.notsent-lowat.client 和 tune.notsent-lowat.server。

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

设置全局 SSL 会话缓存的大小，单位为块数。每块大小足以存储一个未包含对等节点证书的编码会话。若包含对等节点证书，编码会话将根据对等节点证书的大小占用多个块。每块约使用 200 字节内存（基于 `sizeof(struct sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE` 计算，用于 `shctx_init` 函数）。默认值可在编译时强制指定，否则默认为 20000。当缓存满时，将清除最不活跃的条目并重新分配。增大该值可减少此类清除操作，从而降低因 SSL 握手带来的 CPU 开销，确保所有用户尽可能长时间保持会话。所有条目在启动时即预先分配。将该值设为 0 可禁用 SSL 会话缓存。

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

设置用于捕获客户端 Hello 中加密套件列表、扩展列表、椭圆曲线列表及椭圆曲线点格式的最大缓冲区大小。若值为 0（默认值），则禁用捕获；否则，将为每个 SSL/TLS 连接分配一个缓冲区。

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

此设置用于配置证书压缩支持，该功能是 TLS 1.3 的扩展（RFC 8879）。

当设置为 "auto" 时，使用 TLS 库的默认值。

使用 "off" 时，会显式禁用该功能的支持。HAProxy 将不再尝试发送压缩证书，也不会接受压缩证书。

该关键字会同时配置后端和前端两侧。

该关键字由 OpenSSL \>= 3.2.0 支持。

默认值为 auto。

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

设置在使用 DHE 密钥交换时生成临时 Diffie-Hellman 密钥所用的 Diffie-Hellman 参数的最大尺寸。最终尺寸将尝试匹配服务器 RSA（或 DSA）密钥的尺寸（例如，2048 位 RSA 密钥对应 2048 位临时 DH 密钥），但不会超过此最大值。仅允许 1024 或更高数值。较高数值会增加 CPU 负载，且大于 1024 位的值不被 Java 7 及更早客户端支持。若通过证书文件直接提供静态 Diffie-Hellman 参数，或使用 ssl-dh-param-file 参数指定，则此值不生效。若未定义 default-dh-param 且未设置 ssl-dh-param-file，且给定前端的服务器 PEM 文件未指定其自身的 DH 参数，则该前端将无法使用 DHE 密码套件。

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

此选项禁用所有进程之间的 SSL 会话缓存共享。通常不应使用此选项，因为客户端随机命中某个进程会导致大量重协商。但在某些操作系统上，若无法使用任何 SSL 缓存同步方法时，可能需要启用此选项。此时，在 SSL 层之前添加基于哈希的首层负载均衡，可降低缺乏会话共享带来的影响。

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

设置每次调用 SSL_write() 时传递的最大字节数。默认值 0 表示无限制。与 tune.ssl.maxrecord 不同，此设置不会动态调整。较小的记录可能降低吞吐量，但在处理低开销客户端时可能是必需的。

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

此选项用于启用 TLS 密钥的日志记录。使用时应谨慎，因为它会增加每个 SSL 会话的内存消耗，可能导致性能下降。默认情况下已禁用。

这些样本提取应用于生成 SSLKEYLOGFILE，以在 Wireshark 中解密流量。

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

SSLKEYLOG 是一系列以如下格式排列的行：

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

客户端随机数由 %[ssl_fc_client_random,hex] 样本提取提供，密钥和标签可从下方数组中获取。需生成包含此数组中所有标签的 SSLKEYLOGFILE。

以下样本提取结果为十六进制字符串，无需进行转换。

```text
  SSLKEYLOGFILE 标签              |  密钥的样本提取表达式
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

这些获取操作适用于前端（fc）或后端（bc）侧，请将“xx”替换为“fc”或“bc”以使用正确的侧。

仅在使用 OpenSSL 1.1.1 时可用，且在 TLS 1.3 会话中具有实用价值。

若要生成 TLS < 1.3 时的 SSLKEYLOGFILE 内容，仅需以下这一行：

CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]

使用此类日志格式生成完整的密钥日志是可能的，尽管这并非 syslog 的理想选择。

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

HAProxy 还提供了上述格式作为预定义环境变量，可直接在 "log-format" 指令中使用：

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   前端（面向客户端）连接的密钥
$HAPROXY_KEYLOG_BC_LOG_FMT   后端（面向服务器）连接的密钥
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

每秒允许接受的 KeyUpdate 数量上限设为 `<limit>`，超过该值即视为洪水攻击并终止连接。处理 KeyUpdate 操作消耗大量 CPU 资源，且极少有必要接收大量此类消息。设置为 "0" 可禁用速率限制。默认值为 100。<a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

设置缓存 SSL 会话的有效时长。该时间以秒为单位，默认值为 300（5 分钟）。需要注意的是，这并不能保证会话一定持续那么久，因为当缓存已满时，即使会话的配置生命周期尚未到期，最长时间处于空闲状态的会话仍会被清除。此设置的实际意义在于防止会话被使用过久。

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

设置数据传输开始时传递给 SSL_write() 的最大字节数。
默认值 0 表示无限制。在 SSL/TLS 下，客户端必须接收到完整记录后才能解密数据。对于较大的记录，这意味着客户端可能需要下载最多 16kB 的数据才能开始处理。限制该值可改善位于高延迟或低带宽网络中的浏览器的页面加载时间。建议找到适合 1 或 2 个 TCP 段的最优值（通常在启用 TCP 时间戳时为 1448 字节，禁用时为 1460 字节），同时注意 SSL/TLS 会引入一定开销。测试中，1419 和 2859 为典型有效值。使用 "strace -e trace=write" 可查找最佳值。HAProxy 在检测到空闲流后将自动切换至该设置（参见上述 tune.idletimer）。另请参阅 tune.ssl.hard-maxrecord。

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

设置用于存储生成的证书的缓存大小为 `<number>` 项。该缓存为 LRU 缓存。由于动态生成 SSL 证书的开销较大，因此将其缓存。默认缓存大小为 1000 项。

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

定义前端连接在所有连接建立时，相对于最大并发连接数（maxconn）的流（stream）目标百分比。该指标适用于 HTTP/2 或 QUIC 等多路复用协议，其中每个连接可接收多个流。至少保证一个流，因此该百分比必须不低于 100%。在连接建立过程中，HAProxy 会动态通告额外的流，直至达到配置的上限，以维持目标比例。连接建立时，每个前端连接至少分配一个流；额外流根据目标百分比和配置的流限制进行分配。这确保了在不同负载条件下实现高效的流分配（低负载时分配更多流，高负载时分配较少流）。

每页包含大量对象的高动态站点可受益于较高的比率，从而实现每个连接多个流。平均使用较少流的站点（如 WebSocket、应用代码）可能更倾向于选择接近 120 或 150 的较小比率（比连接数多 20 至 50% 的流），以避免在持续负载下流数量过多。

默认值为 0，表示在此级别不强制执行，因此仅 H2 和 QUIC 配置生效（在默认设置下每连接 100 个流，相当于 10000%）。对于小型部署（maxconn 约为千级），此设置仍为推荐值。中等规模部署（连接数为数千至数万）通常将该比例设置在 1000 至 5000 之间，使在满负载时每连接可支持 10 至 50 个流。大规模部署（连接数为数十万至数百万）可能采用更低的值（120 至 200），以在满负载时平均支持每连接 1.2 至 2 个流。

与 HTTP/2 不同，QUIC 能够在连接生命周期内动态调整并发流的数量。然而，QUIC 的流量控制比 HTTP/2 更严格，因此在使用时建议指定足够大的值，以避免连接上产生额外延迟。此外，对于启用了 0-RTT 的 QUIC 监听器存在一项限制：在此情况下，向对等节点通告的初始值将忽略流弹性机制，而仅依赖 "tune.quic.fe.stream.max-concurrent" 设置。不过，在连接生命周期内，流弹性原则仍将在该初始通告之后继续生效。

监控后端的活跃流总数（包括队列）可提供一个实用的指标，用于判断可持续的目标负载，并有助于避免过度配置。

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

设置通过 "tcp-request" 或 "http-request" 规则中的 "track-sc\*" 动作，同时跟踪的连接或请求的 stick-counter 数量。默认值由宏 MAX_SESS_STK_CTR 在编译时设定，缺省值为 3。通过此设置可更改该值并忽略编译时传入的值，但不可设为超过 100 的数值。在将复杂配置迁移到 HAProxy 时可能需要增加此值，但用户应警惕其开销：每个条目占用每个连接 16 字节和每个请求 16 字节，所有请求即使未使用也需分配并清零。因此，值设为 10 会使每个请求的内存消耗增加 320 字节，并导致每次请求均需清空该内存，这会产生可测量的 CPU 影响。相反，当未使用 "track-sc" 规则时，该值可降低（0 为有效值，用于完全禁用 stick-counter）。

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

默认情况下，我们不会尝试使用其他线程组中的空闲连接。此行为可以更改。`<value>` 的有效值为：“none”（默认值），若使用该值，则不会尝试从其他线程组获取空闲连接；“restricted”，在此模式下，仅当使用无法创建新连接的协议（如反向 HTTP）或启用 strict-maxconn 时，才会尝试从其他线程组获取空闲连接；“full”，在此模式下，始终会检查其他线程组中是否存在空闲连接。请注意，从其他线程组使用连接可能带来性能开销，因此除非确实需要，否则不应启用。请注意，此行为现已由 tune.idle-pool.shared 控制，该关键字仅用于与旧配置的兼容性，未来将被弃用。

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

这五个配置项用于管理变量系统所使用的最大内存数量。“global”限制所有作用域可用的总内存数量。“proc”限制进程作用域的内存使用，“sess”限制会话作用域的内存使用，“txn”限制事务作用域的内存使用，而“reqres”则限制每个请求或响应处理所使用的内存。内存计数采用分层机制，即更粗粒度的限制包含更细粒度的限制：“proc”包含“sess”，“sess”包含“txn”，“txn”包含“reqres”。

例如，当 "tune.vars.sess-max-size" 限制为 100 时，"tune.vars.txn-max-size" 和 "tune.vars.reqres-max-size" 也不得超过 100。若创建一个包含 100 字节的变量 "txn.var"，所有可用空间将被耗尽。请注意，运行时超出限制不会导致错误消息，但数值可能被截断或损坏。务必准确规划存储所有变量所需的空间。

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

设置每个流在 zlib 初始化时的 memLevel 参数。该参数定义了为内部压缩状态分配的内存大小。值为 1 时使用最少内存，但速度较慢且压缩比降低；值为 9 时使用最大内存以获得最佳速度。可取值范围为 1 到 9。默认值为 8。

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

设置窗口大小（历史缓冲区的大小）作为每个流的 zlib 初始化参数。该参数值越大，压缩效果越好，但内存使用量也越高。取值范围为 8 到 15，默认值为 15。

## 3.3. 调试 {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

将全局匿名化密钥设置为 `<key>`，该密钥必须为 0 到 4294967295 之间的 32 位数字。当启用匿名化模式时，CLI 命令将默认使用此密钥。该密钥也可通过 CLI 命令 "set anon global-key" 在运行时设置。另请参阅管理手册中的命令行参数 "-dC"。

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

启用（'on'）或禁用（'off'）代码中事件计数器的更新。这些计数器在 CLI 命令 "debug counters" 中以类型 "CNT" 报告。仅当代码编译时 DEBUG_COUNTERS 的值设置为 1 或以上时，这些计数器才可用。当值为 1 时，计数器默认不更新（"debug.counters off"）；当值为 2 时，计数器默认更新（"debug.counters on"）。通常情况下，除非开发者要求，或怀疑其消耗异常高的 CPU 资源（此时需向开发者报告并附上计数器转储），否则不应更改此设置。也可通过 "debug counters" CLI 命令在运行时更改此状态。请参阅管理手册。

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

此指令会暂停配置解析器 `<timeout>` 毫秒。在开发或测试初始化脚本超时场景时非常有用，尤其适用于模拟极长的重载过程。该功能需要将 expose-experimental-directives 设置为启用状态。

`<timeout>` 是默认以毫秒为单位指定的超时值，但如果在数字后附加单位，则可使用任意其他单位，具体说明请参见本文档顶部。

示例：

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

通过跳过释放内存对象和监听器，可加快重载时旧进程的退出速度，因为这些资源在进程终止时将由操作系统自动回收。该优化带来的收益仅限于小幅提升（对于极大型配置，最多几百毫秒）。实际上，其主要用途是在发现 deinit() 代码中存在缺陷时，可绕过该问题。除非开发人员明确指示，否则不应使用此选项。

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

启动时不要显示任何消息。这等效于命令行参数 "-q"。

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

这允许调整在阻塞流量的卡住任务触发标准错误输出警告前的延迟时间。延迟以毫秒为单位，缺省值为 100 毫秒。允许的取值范围必须在 1 毫秒至 1000 毫秒之间（含）。较低的值会导致警告频繁触发，较高的值则很少触发。看门狗无论如何都会终止连续一秒钟内两次无响应的失控任务，因此 1000 毫秒的警告延迟通常不会触发任何警告。建议将该值保持在 10 毫秒至 100 毫秒之间，以检测可能影响用户体验的配置异常，例如导致响应时间过长或交互会话出现卡顿的情况。例如，一个设计不佳的 Lua 样本提取函数执行大量计算，或一个非常大的 map_reg 或 map_regm 映射文件且评估成本极高，都可能引发此类问题。作为对比，一次 TLS 握手耗时约为 1 至 2 毫秒，压缩一个 16 kB 的 HTTP 响应缓冲区大约耗时 1 毫秒。该输出包含被判定为问题任务的线程转储，包含回溯信息以及有助于判断时间消耗位置的上下文信息。

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

当设置此选项时，HAProxy 在处理配置并应用时若发出任何警告，将拒绝启动。这意味着关于参数组合不当的警告、关于无法设置过高限制的警告等，均会导致进程在启动期间以错误退出。少数启动后期的警告无法通过此选项捕获，例如在“daemon”或“master-worker”模式下更改组 ID 时无法丢弃附加组，或在 fork() 后无法标记进程为可转储。此选项不会捕获运行时发出的警告。建议对不常变更的配置设置此选项，以帮助发现细微错误，保持配置的整洁性与向前兼容性。请注意，"haproxy -c" 在此类情况下也会报告错误。此选项等效于命令行参数“-dW”。

## 3.4. HTTPClient 调优 {#section-3-4}

HTTPClient 是一个内部 HTTP 库，可被多个子系统使用，例如在 Lua 脚本中。HTTPClient 不参与数据路径，换句话说，它与通过 HAProxy 传输的 HTTP 流量无关。

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

禁用 httpclient 的 DNS 解析。阻止创建“default”解析器段。

默认值为 off。

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

该选项定义了 httpclient 尝试解析时所使用的解析器段。

默认选项为“default”解析器 ID。默认情况下，若未使用此选项，当该段未找到时将直接禁用解析。

然而，当此选项被显式启用时，若加载失败将触发配置错误。

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

此选项允许选择解析时使用的 IP 协议族，当网络中不可用 IPv6 时尤为方便。默认选项为 "ipv6"。

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

此选项用于配置当请求失败时，httpclient 尝试重试的次数。其功能与后端配置中的 "retries" 关键字相同。

默认值为 3。

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

此选项定义用于验证服务器证书的 ca-file。其参数与服务器行上的 "ca-file" 选项相同。

默认情况下，若未使用此选项，值为 "@system-ca"，表示尝试加载系统的 CA。若加载失败，httpclient 的 SSL 将被禁用。

然而，当此选项被显式启用时，若失败将触发配置错误。

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

与服务器行上的 verify 选项作用方式相同。指定为 "none" 时，不验证服务器证书。默认选项为 "required"。

默认情况下，若未使用此选项，值为“required”。若验证失败，httpclient 的 SSL 将被禁用。

然而，当此选项被显式启用时，若失败将触发配置错误。

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

设置默认情况下 httpclient 连接尝试的最大等待时间。

参数：

```text
<timeout> 是超时值，默认单位为毫秒；也可在数值后添加单位后缀，使用其他单位，
          详见本文开头的说明。
```

默认值为 5000 毫秒。
