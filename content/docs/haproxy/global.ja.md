---
title: "3. globalセクション"
linkTitle: "3. globalセクション"
weight: 140
description: "プロセスのセキュリティ、パフォーマンス調整、デバッグ、HTTPクライアントの設定"
icon: fa-solid fa-earth-americas
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/global/
  - /docs/haproxy/configuration/global/
  - /haproxy/global/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 3"
---

"global" セクションのパラメーターはプロセス全体に適用され、多くはOSに依存します。通常は最初にまとめて設定し、正しく設定できれば変更する必要はありません。一部には対応するコマンドラインオプションがあります。

"global" セクションでは、次のキーワードを使用できます。

- プロセス管理とセキュリティ

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

- パフォーマンス調整

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
  - tune.quic.cc.cubic.min-losses (非推奨)
  - tune.quic.cc-hystart (非推奨)
  - tune.quic.disable-tx-pacing (非推奨)
  - tune.quic.disable-udp-gso (非推奨)
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
  - tune.quic.frontend.max-data-size (非推奨)
  - tune.quic.frontend.max-idle-timeout (非推奨)
  - tune.quic.frontend.max-streams-bidi (非推奨)
  - tune.quic.frontend.max-tx-mem (非推奨)
  - tune.quic.frontend.stream-data-ratio (非推奨)
  - tune.quic.frontend.default-max-window-size (非推奨)
  - tune.quic.listen
  - tune.quic.max-frame-loss (非推奨)
  - tune.quic.mem.tx-max
  - tune.quic.reorder-ratio (非推奨)
  - tune.quic.retry-threshold (非推奨)
  - tune.quic.socket-owner (非推奨)
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
  - tune.ssl.capture-cipherlist-size (非推奨)
  - tune.ssl.certificate-compression
  - tune.ssl.default-dh-param
  - tune.ssl.force-private-cache
  - tune.ssl.hard-maxrecord
  - tune.ssl.keylog
  - tune.ssl.keyupdate-rate-limit
  - tune.ssl.lifetime
  - tune.ssl.maxrecord
  - tune.ssl.ssl-ctx-cache-size
  - tune.ssl.ocsp-update.maxdelay (非推奨)
  - tune.ssl.ocsp-update.mindelay (非推奨)
  - tune.takeover-other-tg-connections
  - tune.vars.global-max-size
  - tune.vars.proc-max-size
  - tune.vars.reqres-max-size
  - tune.vars.sess-max-size
  - tune.vars.txn-max-size
  - tune.zlib.memlevel
  - tune.zlib.windowsize

- デバッグ

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

## 3.1. プロセス管理とセキュリティ {#section-3-1}

<a id="entry-3-1-51degrees-data-file"></a>

**`51degrees-data-file <file path>`**

```haproxy
51degrees-data-file <file path>
```

デバイス検出サービスを提供する51Degreesデータファイルのパスです。ファイルは解凍し、適切な権限でHAProxyからアクセスできる状態にしておくことを推奨します。

このオプションは、HAProxyをUSE_51DEGREES付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-property-name-list"></a>

**`51degrees-property-name-list [<string> ...]`**

```haproxy
51degrees-property-name-list [<string> ...]
```

データセットから読み込む51Degreesプロパティ名の一覧です。名前の完全な一覧は、51DegreesのWebサイトを参照してください。<https://51degrees.com/resources/property-dictionary>

このオプションは、HAProxyをUSE_51DEGREES付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-property-separator"></a>

**`51degrees-property-separator <char>`**

```haproxy
51degrees-property-separator <char>
```

51Degreesの結果を含むレスポンスヘッダーで、各プロパティ値の末尾に追加する文字です。未設定の場合は ',' になります。

このオプションは、HAProxyをUSE_51DEGREES付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-cache-size"></a>

**`51degrees-cache-size <number>`**

```haproxy
51degrees-cache-size <number>
```

51Degreesコンバーターのキャッシュサイズを `<number>` エントリーに設定します。このLRUキャッシュは、過去のデバイス検出とその結果を記憶します。デフォルトでは、このキャッシュは無効です。

このオプションは、HAProxyをUSE_51DEGREES付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-use-performance-graph"></a>

**`51degrees-use-performance-graph { on | off }`**

```haproxy
51degrees-use-performance-graph { on | off }
```

検出処理でパフォーマンスグラフを使用するかどうかを、有効 ('on') または無効 ('off') に設定します。デフォルト値は51Degreesライブラリによって異なります。

このオプションは、HAProxyをUSE_51DEGREESおよび51DEGREES_VER=4付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-use-predictive-graph"></a>

**`51degrees-use-predictive-graph { on | off }`**

```haproxy
51degrees-use-predictive-graph { on | off }
```

検出処理で予測グラフを使用するかどうかを、有効 ('on') または無効 ('off') に設定します。デフォルト値は51Degreesライブラリによって異なります。

このオプションは、HAProxyをUSE_51DEGREESおよび51DEGREES_VER=4付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-drift"></a>

**`51degrees-drift <number>`**

```haproxy
51degrees-drift <number>
```

検出時に許容するドリフト値を設定します。

このオプションは、HAProxyをUSE_51DEGREESおよび51DEGREES_VER=4付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-difference"></a>

**`51degrees-difference <number>`**

```haproxy
51degrees-difference <number>
```

検出時に許容する差分値を設定します。

このオプションは、HAProxyをUSE_51DEGREESおよび51DEGREES_VER=4付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-51degrees-allow-unmatched"></a>

**`51degrees-allow-unmatched { on | off }`**

```haproxy
51degrees-allow-unmatched { on | off }
```

検出処理で一致しないノードを使用するかどうかを、有効 ('on') または無効 ('off') に設定します。デフォルト値は51Degreesライブラリによって異なります。

このオプションは、HAProxyをUSE_51DEGREESおよび51DEGREES_VER=4付きでコンパイルした場合にのみ使用できます。

<a id="entry-3-1-acme-scheduler"></a>

**`acme.scheduler { auto | off }`**

```haproxy
acme.scheduler { auto | off }
```

ACMEスケジューラーを有効または無効にします。

ACMEスケジューラーはHAProxyの起動時に開始されます。証明書を順に調べ、notAfter値が curtime + (notAfter - notBefore) / 12 を過ぎている場合、またはnotBeforeが定義されていない場合は7日を基準として、ACME更新タスクを開始します。その後、スケジューラーはスリープし、12時間後に起動します。

デフォルト値は "auto" です。

関連項目: acme

<a id="entry-3-1-ca-base"></a>

**`ca-base <dir>`**

```haproxy
ca-base <dir>
```

"ca-file"、"ca-verify-file"、または "crl-file" ディレクティブに相対パスを指定した場合に、SSL CA証明書とCRLを取得するデフォルトディレクトリを指定します。"ca-file"、"ca-verify-file"、および "crl-file" に絶対パスを指定した場合は、そちらが優先され、"ca-base" は無視されます。

<a id="entry-3-1-chroot"></a>

**`chroot { <jail dir> | auto }`**

```haproxy
chroot { <jail dir> | auto }
```

権限を降格する前に、カレントディレクトリを `<jail dir>` に変更してそこでchroot()を実行します。未知の脆弱性を悪用された場合でも、攻撃者がシステムを悪用することを非常に困難にするため、セキュリティが向上します。`<jail dir>` が空であり、誰も書き込めないことを確認することが重要です。スーパーユーザー権限でプロセスを起動した場合は、chroot()を直接実行します。Linux上で権限を持たずに起動した場合、haproxyはunshare(CLONE_NEWUSER)で作成した新しいユーザー名前空間の内部から実行を試みます。この仕組みを利用できない場合、chroot()は通常のエラーで失敗します。

特別な指定として、`<jail dir>` を "auto" にできます。この場合、haproxyは名前のない一時ディレクトリを作成してリンクを削除し、その中にchrootします。作成された隔離先はファイルシステム上に名前を持たず、空で読み取り専用になるため、専用の隔離ディレクトリを用意する必要がありません。

スーパーユーザー権限で起動し、chrootを使用していない場合は、この仕組みを常に使用するよう促すため、警告を表示します。chrootを使用できないやむを得ない理由（たとえば、都合の悪いパスにあるUNIXソケット経由でサーバーにアクセスする場合）があるときは、明示的に "chroot /" を追加すれば警告を抑制できます。この方法には、その指定が設定上で確認できるという利点があります。

<a id="entry-3-1-close-spread-time"></a>

**`close-spread-time <time>`**

```haproxy
close-spread-time <time>
```

ソフト停止時に、アイドル接続とアクティブな接続の切断を分散させる時間枠を定義します。SIGUSR1を受信し、猶予期間があればその終了後、このオプションが未設定なら、アイドル接続はすべて一度に切断されます。アクティブなHTTPまたはHTTP2接続は、次のリクエストを受信した後、HTTPレスポンスに "Connection: close" 行を追加するか、HTTP2の場合はGOAWAYフレームを送信して終了します。このオプションを設定すると、接続の切断は指定した `<time>` にわたって分散されます。close-spread-timeを "infinite" に設定すると、ソフト停止時のアクティブな接続の切断が無効になります。HTTPレスポンスに "Connection: close" ヘッダー（HTTP2ではGOAWAY）が追加されなくなり、アイドル接続はタイムアウトに達したときにだけ切断されます（設定で指定した各種タイムアウトに基づきます）。

引数:

```text
<time>  ソフトストップ処理中の接続終了を分散させる時間枠です
        （デフォルトの単位はミリ秒）。能動的な接続終了を無効にする場合は
        "infinite"を指定します。
```

"hard-stop-after" オプションを使用する場合は、プロセスが停止する前にすべての接続が正常に終了できるよう、この設定値を "hard-stop-after" の値より小さくすることを推奨します。

関連項目: grace, hard-stop-after, idle-close-on-response

<a id="entry-3-1-cluster-secret"></a>

**`cluster-secret <secret>`**

```haproxy
cluster-secret <secret>
```

同じクラスターに属する複数のノード間で共有する、ASCII文字列のシークレットを定義します。さまざまな用途に使用できます。少なくとも、このプロセスが生成するすべてのQUIC接続のステートレスリセットトークンの導出に使用されます。Retryトークンを暗号化するシークレットの導出にも使用されます。

このパラメーターを設定しない場合、プロセスの起動時にランダムな値が選ばれます。これにより、この値に依存する機能を、一定の制限付きで使用できます。

<a id="entry-3-1-cpu-map"></a>

**`cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]`**

```haproxy
cpu-map [auto:]<thread-group>[/<thread-set>] <cpu-set>[,...] [...]
```

一部のOSでは、スレッドグループやスレッドを特定のCPUセットにバインドできます。これは、指定したスレッドがほかのCPUで実行されなくなることを意味します。"cpu-map" ディレクティブは、個々のスレッドまたはスレッドグループにCPUセットを指定します。最初の引数はスレッドグループの範囲で、必要に応じてその後にスレッドセットを指定します。範囲は次の形式で表します。

```text
all | odd | even | number[-[number]]
```

`<number>` は、マシンのワードサイズに応じて1から32または64までの数値でなければなりません。'thread-groups' を超えるグループIDと、マシンのワードサイズを超えるスレッドIDは無視されます。スレッド番号はすべて、所属するグループ内での相対番号です。このような2つの数値をダッシュ ('-') で区切って範囲を指定できます。"thread" bindディレクティブと同様に、"all" ですべてのスレッドをまとめて、"odd" で奇数番号だけを、"even" で偶数番号だけを指定することもできます。2番目以降の引数はCPUセットです。各CPUセットには、最初のCPUを0とする単一の番号、またはこのような2つの番号をダッシュ ('-') で区切った範囲を指定します。CPU番号や範囲は、コンマで区切るか、同じ行に別の引数として追加の範囲を渡すことで、複数指定できます。LinuxおよびBSD以外のOSでは、CPUインデックスの最大値が31または63に制限されることがあります。複数の "cpu-map" ディレクティブを指定できますが、範囲が重なる場合は、後の "cpu-map" ディレクティブが前の指定を置き換えます。

範囲を部分的に定義し、上限を省略することもできます。この場合、マシンのワードサイズに応じた最大値である32または64が上限になります。

スレッドセットの前にプレフィックス "auto:" を付けると、HAProxyがスレッドとCPUセットを順に進めながら、スレッドの集合をCPUに自動でバインドします。有効な指定にするには、両方の集合の要素数が同じでなければなりません。CPUセットの宣言順序にかかわらず、下限から上限に向かってバインドされます。"auto:" プレフィックスとともにグループとスレッドの両方に範囲を指定することはできません。範囲を指定できるのは一方だけで、もう一方は固定の番号でなければなりません。

グループの範囲指定は、歴史的な理由からサポートされています。現在では、番号だけを指定するとスレッドグループを表し、thread-groupsを使用していない場合は1でなければなりません。また、スレッドグループを使用せずにスレッドの範囲や番号を指定する場合は、その前に "1/" を付ける必要があります。なお、"1" は "1/all" と完全に同じ意味で、グループ内のすべてのスレッドを表します。

例:

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

スレッドをCPUにバインドする方法を定義します。現在、次の値を指定できます。

- per-core: 各スレッドを、1つのコアのすべてのハードウェアスレッドにバインドします。
- per-group: 各スレッドを、グループ内のすべてのハードウェアスレッドにバインドします。"cpu-policy" で "threads-per-core 1" を使用していない場合のデフォルトです。"per-group" には、CPUの割り当て方法を指定する任意の引数を追加できます。CPUの一覧がグループごとに許可される最大CPU数を超え、複数のグループに分割する必要がある場合、追加のオプションでグループをそれらのCPUにバインドする方法を選べます。
  - auto: 各スレッドグループには、そのグループ専用でほかのグループとは共有しない、連続したCPUコアを公平に割り当てます。通常はより効率的なため、これがデフォルトです。
  - loose: 各グループが、一覧内のどのCPUも引き続き使用できます。通常は競合が増えますが、同じCPUで動作するほかの負荷に、よりうまく対処できる場合があります。
- auto: "cpu-policy" で "threads-per-core 1" を使用している場合は "per-core"、それ以外の場合は "per-group" を使用します。これがデフォルトです。
- per-thread: 1つのスレッドを1つのハードウェアスレッドだけにバインドします。"cpu-policy" で "threads-per-core 1" を使用している場合、各スレッドはそれぞれ異なるコアの1つのハードウェアスレッドにバインドされます。
- per-ccx: 各スレッドを、1つのCCX内のすべてのハードウェアスレッドにバインドします。

<a id="entry-3-1-cpu-policy"></a>

**`cpu-policy <policy> [threads-per-core 1 | auto]`**

```haproxy
cpu-policy <policy> [threads-per-core 1 | auto]
```

使用するCPU割り当てポリシーを選択します。

複数CPUのシステムでは、パフォーマンス、レイテンシー、コスト、システム全体のリソース管理など、利用可能なCPUコアをすべて使用しない理由や、別々のスレッドグループにまとめる理由が数多くあります。"cpu-set" ディレクティブで一部を除外できますが、その後、残りのCPUをスレッドとスレッドグループにどう割り当てるかを決める必要があります。

この対応付けは通常 "cpu-map" ディレクティブで行いますが、異なる種類のCPUが混在するシステムでは、保守が特に難しくなることがあります。

"cpu-policy" ディレクティブは、"cpu-map" を使用していない場合に、代わりに使用する割り当てポリシーをいくつかの候補から選びます。現在は次のポリシーをサポートしており、デフォルトは "performance" です。

- none: 特別な追加選択は行いません。有効なCPUをすべて使用できます。スレッド数が未設定の場合は、利用可能なCPU数に設定しますが、スレッドグループごとに、32ビットシステムでは32、64ビットシステムでは64を超えないようにします。スレッドグループ数が未設定の場合は1に設定します。

- efficiency: 後述の "group-by-ccx" と同じですが、性能がすぐ下の種類のコアより25%を超えて高いコアからなるCPUクラスターを除外します。通常は "big" コアや "performance" コアが該当します。つまり、複数の種類のCPUコアを検出した場合は、効率のよい種類だけを使用します。負荷が中程度で、最も高性能なコアをアプリケーションやセキュリティコンポーネントで使えるようにしておく必要がある場合に有効です。最近のCPUには、このような高効率のCPUコアを多数備え、消費電力を抑えながら、全体として十分な性能を発揮できるものがあります。

- first-usable-node: 起動時にCPUがあらかじめ制限されておらず（たとえば "taskset" ユーティリティによる制限）、"nbthread" ディレクティブも未設定の場合、有効なCPUが存在する最初のNUMAノードを使用し、そのCPU数をスレッド数として使用します。システムに応じて32または64という上限の範囲内で、それらすべてを含む単一のスレッドグループを有効にします。

- group-by-2-ccx: 後述の "group-by-ccx" と同じですが、2つのCCXごとにグループを作成します。コア数の少ないCCXを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。CCX間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-2-clusters: "group-by-cluster" と同じですが、2つのクラスターごとにグループを作成します。コア数の少ないクラスターを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。クラスター間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-3-ccx: 後述の "group-by-ccx" と同じですが、3つのCCXごとにグループを作成します。コア数の少ないCCXを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。CCX間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-3-clusters: "group-by-cluster" と同じですが、3つのクラスターごとにグループを作成します。コア数の少ないクラスターを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。クラスター間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-4-ccx: 後述の "group-by-ccx" と同じですが、4つのCCXごとにグループを作成します。コア数の少ないCCXを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。CCX間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-4-clusters: "group-by-cluster" と同じですが、4つのクラスターごとにグループを作成します。コア数の少ないクラスターを多数持つCPUで、グループが増えすぎるのを避けたり、全コアを使用しない場合の分布を少し均したりするのに役立つことがあります。クラスター間の通信が遅い場合、性能に非常に悪い影響を与える可能性があります。一般には推奨しません。

- group-by-ccx: "nbthread" と "nbtgroups" のどちらも未設定の場合、利用可能なCPUを持つCPUコアコンプレックス ("CCX") ごとにスレッドグループを作成し、それぞれにCPU数と同じ数のスレッドを作成します。CCXは、最終レベルキャッシュ ("LLC")、通常はL3キャッシュへのアクセスが同程度に速いCPUをまとめたものです。最近のほとんどのマシンでは、離れたCCXのCPUを同じスレッドグループに混在させないことが、性能上きわめて重要です。グループ内の全スレッドを、そのCCXのすべてのCPUにバインドすることで、バインドを厳密にしすぎずに、グループ内通信をCCX内に収めます。グループごとのスレッド数の上限とスレッドグループ数の上限は守られます。マルチソケットシステムやNUMAシステム、CCX間のレイテンシーが大きいCPUで推奨します。

- group-by-cluster: "nbthread" と "nbtgroups" のどちらも未設定の場合、利用可能なCPUを持つCPUクラスターごとにスレッドグループを作成し、それぞれにCPU数と同じ数のスレッドを作成します。グループ内の全スレッドを、そのクラスターのすべてのCPUにバインドすることで、バインドを厳密にしすぎずに、グループ内通信をクラスター内に収めます。グループごとのスレッド数の上限とスレッドグループ数の上限は守られます。マルチソケットシステムやNUMAシステム、CCX間のレイテンシーが大きいCPUで推奨します。ほとんどのサーバーマシンではクラスターとCCXは同じですが、異種CPUが混在するマシン（"performance" と "efficiency"、または "big" と "little"）では、一般にクラスターはCCXの一部で、非常によく似たCPUだけ（種類が同じで、周波数差が最大 +/-5%）から構成されます。この違いは、開発者や管理者が構成を検証するために使用する最近のノートPCやデスクトップマシンで確認できます。

- performance: 前述の "group-by-ccx" と同じですが、性能がすぐ上の種類のコアの80%未満であるコアからなるCPUクラスターを除外します。通常は "little" コアや "efficient" コアが該当し、これらを追加しても大きな改善は得られず、簡単に逆効果になることがあります（TLSハンドシェイクなど）。多くの場合、このようなコアはネットワーク処理などの別のタスクに残しておく方がはるかに効果的です。開発用システムでは、負荷生成ツールや監視ツールなどの補助ツールにも使用できます。これがデフォルトのポリシーです。

- resource: 前述の "group-by-cluster" と同じですが、最も小さく効率のよいCPUクラスターだけを使用し、ほかはすべて無視します。十分な性能を維持しつつ、リソース使用量を必要最小限に抑えるために使用できます。たとえば、消費電力をさらに減らしたり、レンタルシステムのサイドカー構成で必要なコア数を最小限にして、システムをより容易に縮小したりする用途です。クラスターが1つしかない場合は、それをすべて使用します。

任意のキーワード "threads-per-core" を追加できます。指定できる値は "1" と "auto" の2つです。1に設定すると、コアのハードウェアスレッド数にかかわらず、コアごとに1つのスレッドだけを作成します。autoに設定すると、ハードウェアスレッドごとに1つのスレッドを作成します。アフィニティーが未指定でthreads-per-core 1を使用する場合、デフォルトのアフィニティーはper-coreになります。

関連項目: "cpu-map", "cpu-set", "nbthread"

<a id="entry-3-1-cpu-set"></a>

**`cpu-set <directive>...`**

```haproxy
cpu-set <directive>...
```

実行するCPUの集合を記号的に記述できます。このディレクティブは次のキーワードをサポートします。- reset: サービスマネージャーや "taskset" コマンドなどから継承した既存の制限をすべて解除します。- drop-cpu `<set>`: この集合に含まれるCPUにはバインドしません。- only-cpu `<set>`: この集合に含まれないCPUにはバインドしません。- drop-node `<set>`: このNUMAノードに属するCPUにはバインドしません。- only-node `<set>`: このNUMAノードに属さないCPUにはバインドしません。- drop-cluster `<set>`: このハードウェアクラスター番号のCPUにはバインドしません。- only-cluster `<set>`: ほかのハードウェアクラスター番号のCPUにはバインドしません。- drop-core `<set>`: このハードウェアコア番号のCPUにはバインドしません。- only-core `<set>`: ほかのハードウェアコア番号のCPUにはバインドしません。- drop-thread `<set>`: このハードウェアスレッド番号のCPUにはバインドしません。- only-thread `<set>`: ほかのハードウェアスレッド番号のCPUにはバインドしません。関連項目: "cpu-policy"

<a id="entry-3-1-crt-base"></a>

**`crt-base <dir>`**

```haproxy
crt-base <dir>
```

"crtfile" または "crt" ディレクティブに相対パスを指定した場合に、SSL証明書を取得するデフォルトディレクトリを指定します。絶対パスを指定した場合は、そちらが優先され、"crt-base" は無視されます。

<a id="entry-3-1-daemon"></a>

**`daemon`**

```haproxy
daemon
```

プロセスをforkしてバックグラウンドに移します。これが推奨される動作モードです。コマンドライン引数 "-D" と同じです。コマンドライン引数 "-db" で無効にできます。systemdモードでは、このオプションは無視されます。

<a id="entry-3-1-default-path"></a>

**`default-path { current | config | parent | origin <path> }`**

```haproxy
default-path { current | config | parent | origin <path> }
```

デフォルトでは、HAProxyは相対パスで指定されたすべてのファイルを、プロセスを起動した場所から読み込みます。状況によっては、すべての相対パスの起点を別の場所に変更し、その場所でプロセスを起動したかのように扱いたいことがあります。このディレクティブはそのためのものです。内部的には、各設定ファイルの処理中に指定した場所へ一時的にchdir()し、各ファイルの処理後に元のディレクトリに戻ります。スラッシュ ('/') で始まらないパスのファイルを読み込む際のポリシーを、引数で指定します。- "current" は、相対パスのファイルをすべて、プロセスを起動したディレクトリから読み込むことを示します。これがデフォルトです。

    - "config" は、相対パスのファイルをすべて、設定ファイルがあるディレクトリから読み込むことを示します。具体的には、設定ファイルのパスにスラッシュ ('/') が含まれる場合、最後のスラッシュまでの最長の部分を移動先ディレクトリとして使用し、それ以外の場合はカレントディレクトリを使用します。このモードは、マップ、エラーファイル、証明書、Luaスクリプトを、移動可能なパッケージとしてまとめるのに便利です。複数の設定ファイルを読み込む場合は、それぞれについてディレクトリを更新します。

    - "parent" は、相対パスのファイルをすべて、設定ファイルがあるディレクトリの親ディレクトリから読み込むことを示します。具体的には、設定ファイルのパスにスラッシュ ('/') が含まれる場合、最後のスラッシュまでの最長の部分に ".." を追加したものを移動先ディレクトリとして使用し、それ以外の場合は ".." を使用します。このモードは、マップ、エラーファイル、証明書、Luaスクリプトを移動可能なパッケージとしてまとめつつ、各要素を別々のサブディレクトリ（"config/"、"certs/"、"maps/" など）に置く場合に便利です。

    - "origin" は、相対パスのファイルをすべて、指定した必須のパスから読み込むことを示します。同じシステムで異なるHAProxyインスタンスを並行して実行し、インスタンスごとに異なるプレフィックスを使用しながら、ほかのセクションを容易に移動できるようにしている場合、管理を簡単にするために使用できます。

"default-path" ディレクティブは、直前までの指定をただちに置き換え、別のディレクトリへの移動を伴う場合があります。これによって常に意図した動作になるはずですが、複数のdefault-pathディレクティブを使用することは好ましい方法ではありません。使用する場合は、すべての設定ファイルでポリシーを統一するべきです。

警告： マップや証明書などの一部の設定要素は、設定したパスによって一意に識別されます。移動可能な配置にすると、複数の要素が同じ一意名を持つ可能性があり、実行時の更新が難しくなります。特に、異なるディレクトリから複数の設定ファイルを読み込む場合に問題になります。相対パスを採用する前に、衝突を起こさない厳密なファイル命名規則を守ることが不可欠です。堅牢な方法として、すべてのファイル名にそれぞれのサイト名をプレフィックスとして付けるか、ディレクトリ単位で同様にすることが考えられます。

<a id="entry-3-1-description"></a>

**`description <text>`**

```haproxy
description <text>
```

インスタンスを説明するテキストを追加します。

一部の文字（# など）はエスケープが必要です。また、このテキストはhtmlページに挿入されるため、"\<" と "\>" の使用は避けることを推奨します。

<a id="entry-3-1-deviceatlas-json-file"></a>

**`deviceatlas-json-file <path>`**

```haproxy
deviceatlas-json-file <path>
```

APIが読み込むDeviceAtlas JSONデータファイルのパスを設定します。パスは有効なJSONデータファイルを指し、HAProxyプロセスからアクセスできなければなりません。

<a id="entry-3-1-deviceatlas-log-level"></a>

**`deviceatlas-log-level <value>`**

```haproxy
deviceatlas-log-level <value>
```

APIが返す情報のレベルを設定します。このディレクティブは任意で、未設定の場合のデフォルトは0です。

<a id="entry-3-1-deviceatlas-properties-cookie"></a>

**`deviceatlas-properties-cookie <name>`**

```haproxy
deviceatlas-properties-cookie <name>
```

リクエストでDeviceAtlasのクライアント側コンポーネントを使用した場合に、検出に使うクライアントCookieの名前を設定します。このディレクティブは任意で、未設定の場合のデフォルトはDAPROPSです。

<a id="entry-3-1-deviceatlas-separator"></a>

**`deviceatlas-separator <char>`**

```haproxy
deviceatlas-separator <char>
```

APIのプロパティ結果に使う区切り文字を設定します。このディレクティブは任意で、未設定の場合のデフォルトは \| です。

<a id="entry-3-1-dns-accept-family"></a>

**`dns-accept-family <family>[,...]`**

```haproxy
dns-accept-family <family>[,...]
```

デフォルトでは、DNSリゾルバーはIPv4とIPv6の両方のアドレスを受け入れます。server行の "resolve-prefer" キーワードや "do-resolve" アクションのfamily引数で優先度を変えられますが、これは優先度にすぎず、もう一方のファミリーしかない場合にその使用を禁止するものではありません。デュアルスタックを使用できない環境では、到達不能なIPv6だけのDNSレコードに遭遇すると、次のリクエストまで機能し続けた可能性のある従来のIPv4レコードが置き換えられるため、大きな問題を引き起こすことがあります。グローバルオプション "dns-accept-family" では、一方（または両方）のアドレスファミリーだけを使用するよう強制できます。引数は次の単語をコンマで区切った一覧です。- "ipv4": IPv4アドレス（"A" レコード）を問い合わせ、受け入れます。- "ipv6": IPv6アドレス（"AAAA" レコード）を問い合わせ、受け入れます。- "auto": IPv4を使用し、IPv6については、システムにそのデフォルトゲートウェイがあれば使用します。最後の確認結果は30秒間キャッシュされます。

一方のファミリーだけを使用する場合、もう一方のファミリーについてリゾルバーにリクエストを送信せず、そのファミリーの応答はすべて無視します。3.3以降のデフォルト値は "auto" で、IPv6でルーティングできることを確認できた場合にだけ両方のファミリーを有効にし、それ以外の場合はIPv4だけを使用します。関連項目: "resolve-prefer", "do-resolve"

<a id="entry-3-1-expose-deprecated-directives"></a>

**`expose-deprecated-directives`**

```haproxy
expose-deprecated-directives
```

非推奨とされた一部のディレクティブを使用する前に、この文を記述しなければなりません。これにより、警告を抑制し、設定ファイルが拒否されないようにします。すべての非推奨ディレクティブが対象ではなく、代替手段がないものだけが対象です。

<a id="entry-3-1-expose-experimental-directives"></a>

**`expose-experimental-directives`**

```haproxy
expose-experimental-directives
```

実験的とされたディレクティブを使用する前に、この文を記述しなければなりません。そうしないと設定ファイルは拒否されます。このオプションの対象となる機能は、正常な動作が保証されず、保守期間中に動作しなくなる可能性があります。開発者は次のバージョンの開発中、ベストエフォートで保守し、機能を壊さないよう合理的な努力を尽くしますが、保証はしません。このため、これらの機能は次のLTSリリースの公開後までサポートされることを想定していません。実験的な機能を試すユーザーは、その機能の改善を利用できるよう、速やかにアップグレードすることが期待されます。このディレクティブがまだ必要かどうかは簡単に確認できます。有効にしていても対象の機能で使用されていない場合は、無効にするよう勧める警告が出ます。したがって、警告がなければ、まだ必要であることを意味します。

<a id="entry-3-1-external-check"></a>

**`external-check [preserve-env]`**

```haproxy
external-check [preserve-env]
```

外部エージェントによるヘルスチェックを許可します。セキュリティ上の予防措置として、デフォルトでは無効です。有効にしても、"insecure-fork-wanted" も有効にしないと、チェックが失敗することがあります。起動したプログラムがsetuid実行ファイルを使用する場合（本来は使用すべきではありません）、globalセクションで "insecure-setuid-wanted" も設定する必要があるかもしれません。デフォルトでは、チェックは、backendセクションの "external-check" コマンドで定義した変数だけを含む、初期化された環境で開始します。ただし、複雑なスクリプトが追加のパスや情報を環境から取得する場合など、環境を保持したいこともあります。その場合は "preserve-env" キーワードを追加します。ただし、この場合はチェックプログラムが攻撃にさらされる可能性があるため、setuidでも特権ユーザーとしても実行しないことを強く推奨します。詳細は "option external-check"、"insecure-fork-wanted"、および "insecure-setuid-wanted" を参照してください。

<a id="entry-3-1-fd-hard-limit"></a>

**`fd-hard-limit <number>`**

```haproxy
fd-hard-limit <number>
```

システムの制限にかかわらず、プロセスが使用するファイルディスクリプター数の最大値に上限を設定します。"ulimit-n" と "maxconn" で値を強制できますが、それらが未設定の場合、プロセスは "ulimit -n -H" で報告されるRLIMIT_NOFILE設定のハードリミットに制限されます。しかし、最近のOSには、ここにきわめて大きな値（10億程度）を許容するものがあり、通常の用途ではRAMを消費しすぎてしまいます。fd-hard-limit設定は、この上限をより低く制限するために用意されています。つまり、システムが課す上限が `<number>` より低ければ常にそれに従い、システムの上限が高ければ指定した値を使用します。fd-hard-limitのデフォルト値は1048576です。このデフォルトは、コンパイル時変数DEFAULT_MAXFDで変更できます。RLIMIT_NOFILEのハードリミットがきわめて大きい場合、この値をシステム（カーネル）の最大上限として使用できます。globalセクションでfd-hard-limitを設定すると、ビルド時にDEFAULT_MAXFDで指定した値を一時的に上書きできます。次の例ではほかの設定を指定しておらず、maxconn値は "fd-hard-limit" とRLIMIT_NOFILEの上限のうち、小さい方に自動的に合わせられます。

```text
global
    # use as many FDs as possible but no more than 50000
    fd-hard-limit 50000
```

関連項目: ulimit-n, maxconn

<a id="entry-3-1-gid"></a>

**`gid <number>`**

```haproxy
gid <number>
```

プロセスのグループIDを `<number>` に変更します。このグループIDは、HAProxy専用、または同種の少数のデーモンだけで使用することを推奨します。HAProxyは、このグループに属するユーザー、またはスーパーユーザー権限で起動しなければなりません。補助グループを持つユーザーからHAProxyを起動した場合、それらのグループを外せるのは、スーパーユーザー権限で起動した場合だけです。"group" と "uid" も参照してください。

<a id="entry-3-1-grace"></a>

**`grace <time>`**

```haproxy
grace <time>
```

SIGUSR1から実際のソフト停止までの遅延時間を定義します。

引数:

```text
<time>  SIGUSR1シグナルを受信してからソフトストップ処理に進むまでに
        待機する追加の遅延時間です（デフォルトの単位はミリ秒）。
```

これは、haproxyプロセスを停止する必要がある一方、リスナーのバインドを解除する前に、外部コンポーネントが状態を検出する必要のある従来の環境との互換性のために使用します。内部の "stopping" 変数（"stopping" サンプル取得関数が報告する変数）をtrueにしますが、遅延時間が経過するまで、リスナーはそれまでどおり接続の受け入れを続けます。その後、通常のソフト停止を実行します。リロードされるプロセスで使用してはなりません。古いプロセスがバインドを解除できなくなり、新しいプロセスの起動を妨げたり、ほかの問題を引き起こしたりする可能性があるためです。

例:

```shell
global
  grace 10s

# Returns 200 OK until stopping is set via SIGUSR1
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { stopping }
```

より柔軟で長期的にも使える方法として、オーケストレーションシステムがCLIからグローバル変数を設定し、その変数を外部チェックへの応答に使用して、一定時間後にSIGUSR1シグナルを送信することが考えられます。

例:

```shell
# Returns 200 OK until proc.stopping is set to non-zero. May be done
# from HTTP using set-var(proc.stopping) or from the CLI using:
# > set var proc.stopping int(1)
frontend ext-check
  bind :9999
  monitor-uri /ext-check
  monitor fail if { var(proc.stopping) -m int gt 0 }
```

関連項目: hard-stop-after, monitor

<a id="entry-3-1-group"></a>

**`group <group name>`**

```haproxy
group <group name>
```

"gid" と同様ですが、/etc/groupにあるグループ名 `<group name>` のGIDを使用します。"gid" と "user" も参照してください。

<a id="entry-3-1-h1-accept-payload-with-any-method"></a>

**`h1-accept-payload-with-any-method`**

```haproxy
h1-accept-payload-with-any-method
```

ペイロードを含むHTTP/1.0のGET/HEAD/DELETEリクエストを、HTTPレスポンス413 Payload Too Largeで拒否しないようにします。

HTTP/1.1では明示的に許可されていますが、HTTP/1.0ではこの点が明確ではなく、一部の古いサーバーはペイロードを想定せず、本文の長さを（Content-LengthやTransfer-Encodingヘッダーで）調べることもありません。そのため、HTTP/1.0のGET/HEAD/DELETEリクエストのペイロードを正しく処理する中継機器がある一方で、完全に無視するものもあります。これによりリクエストスマグリング攻撃が可能となり、セキュリティ上の問題につながることがあります。したがって、デフォルトでは、HAProxyはペイロードを含むHTTP/1.0のGET/HEAD/DELETEリクエストを拒否します。

ただし、一部の古いクライアントでは、それが問題になることがあります。その場合は、このグローバルオプションを設定できます。

<a id="entry-3-1-h1-do-not-close-on-insecure-transfer-encoding"></a>

**`h1-do-not-close-on-insecure-transfer-encoding`**

```haproxy
h1-do-not-close-on-insecure-transfer-encoding
```

HTTP/1.1仕様（RFC9112#6.1）が規定するように、同じメッセージにTransfer-EncodingヘッダーフィールドとContent-Lengthヘッダーフィールドの両方がある場合、上流または下流の経路のどこかにHTTP/1.0エージェントが存在すると、コンテンツスマグリング攻撃を運んでしまう重大な危険があります。この場合、悪用を防ぐために、エージェントはレスポンス後に必ず接続を切断しなければなりません。しかし、一部の非常に古いクライアントでは、特にリクエストごとにTLS接続を再ネゴシエーションする必要がある場合、性能に影響することがあります。このオプションは、この規則の強制をHAProxyに行わせず、メッセージを適切に整えるだけにして、レスポンス後も接続を維持するためのものです。これを行えるのは、経路にHTTP/1.0エージェントが存在せず、HAProxyより前にあるすべての実装が、これらのヘッダーフィールドに適用される規則についてHTTP/1.1に完全に準拠していると確実に判断できる場合だけです。いずれの場合も、HAProxyは次のホップを混乱させないよう、余分なContent-Lengthヘッダーを引き続き無視して削除します。

古い不正なクライアントやサーバーを回避するためにこのオプションを有効にする場合、このオプションが必要かどうかにかかわらず、規則に違反するエージェントのメッセージには切り詰められる危険があることを理解することが重要です。古いエージェントがContent-Lengthを参照してTransfer-Encodingを無視すると、チャンクサイズを符号化した部分の累積長が計上されないためです。このように、上記の規則はセキュリティだけの問題ではなく、古いエージェントとの非互換性によって通信に支障が出る可能性のあるエージェントを排除するためのものでもあります。

<a id="entry-3-1-h1-case-adjust"></a>

**`h1-case-adjust <from> <to>`**

```haproxy
h1-case-adjust <from> <to>
```

有効にした場合に、HTTP/1クライアントまたはサーバーへ送信する前に、ヘッダー名 `<from>` を `<to>` に変更する大文字・小文字の調整を定義します。`<from>` は小文字でなければならず、`<from>` と `<to>` は大文字・小文字以外に違いがあってはなりません。複数のヘッダー名を調整する場合は、繰り返し指定できます。重複するエントリーは許可されません。多数のヘッダー名を調整する場合は、"h1-case-adjust-file" の方が便利なことがあります。プロキシで "option h1-case-adjust-bogus-client" または "option h1-case-adjust-bogus-server" を指定しない限り、変換は適用されません。

RFC7230が規定するとおり、ヘッダー名は大文字・小文字を区別しないため、標準の表記はありません。したがって、アプリケーションは大文字・小文字を区別せずに処理しなければなりません。しかし、一部の不正なアプリケーションは標準に違反し、ブラウザーで最も一般的な大文字・小文字の使い方に誤って依存しています。HTTP/2では、すべてのヘッダー名を小文字で交換しなければならないため、この問題が深刻になります。HAProxyも同じ慣例に従い、HTTPバージョンにかかわらず、すべてのヘッダー名を小文字でクライアントとサーバーに送信します。

リクエストやレスポンスを正しく処理できないアプリケーションでは、修正が済むまでの間、送信されるヘッダー名を調整するこのような回避策を、一時的に使用する必要があるかもしれません。このような回避策を必要とするアプリケーションは、コンテンツスマグリング攻撃に対して脆弱である可能性があり、必ず修正しなければなりません。

例:

```text
global
  h1-case-adjust content-length Content-Length
```

"h1-case-adjust-file"、"option h1-case-adjust-bogus-client"、および "option h1-case-adjust-bogus-server" を参照してください。

<a id="entry-3-1-h1-case-adjust-file"></a>

**`h1-case-adjust-file <hdrs-file>`**

```haproxy
h1-case-adjust-file <hdrs-file>
```

HTTP/1クライアントまたはサーバーに送信する前に、一部のヘッダー名の大文字・小文字を調整するための、キーと値のペアの一覧を含むファイルを定義します。ファイル `<hdrs-file>` には、行ごとに2つのヘッダー名を記述しなければなりません。最初の名前は小文字で、両者は大文字・小文字以外に違いがあってはなりません。'#' で始まる行は、空行と同様に無視されます。先頭と末尾のタブとスペースは取り除かれます。重複するエントリーは許可されません。プロキシで "option h1-case-adjust-bogus-client" または "option h1-case-adjust-bogus-server" を指定しない限り、変換は適用されません。

このディレクティブを繰り返し指定した場合、最後のものだけを処理します。多数のヘッダー名を調整する場合の、"h1-case-adjust" ディレクティブの代替です。使用に伴うリスクを確認してください。

"h1-case-adjust"、"option h1-case-adjust-bogus-client"、および "option h1-case-adjust-bogus-server" を参照してください。

<a id="entry-3-1-h2-workaround-bogus-websocket-clients"></a>

**`h2-workaround-bogus-websocket-clients`**

```haproxy
h2-workaround-bogus-websocket-clients
```

h2のWebSocketサポートをクライアントに通知しないようにします。Firefox 88など、比較的新しいRFC8441の実装に問題のあるクライアントへの対処に使用できます。クライアントがWebSocketトンネルを自動的にhttp/1.1に切り替えられるようにするには、bind行で明示的な "proto" キーワードを使わずに、"alpn" でh2のサポートを指定してください。この文が以前に有効化されていた場合は、キーワードの前に "no" を付けることで無効にできます。

<a id="entry-3-1-hard-stop-after"></a>

**`hard-stop-after <time>`**

```haproxy
hard-stop-after <time>
```

正常なソフト停止に許容する最大時間を定義します。

引数:

```text
<time>  SIGUSR1シグナルによるソフトストップを受信した後、
        インスタンスが動作し続ける最大時間です（デフォルトの単位はミリ秒）。
```

ソフト停止中に接続が開いたままでも、インスタンスが確実に終了するようにするために使用できます（たとえば、tcpモードのプロキシに長いタイムアウトを設定している場合）。TCPモードとHTTPモードの両方に適用されます。

例:

```text
global
  hard-stop-after 30s
```

関連項目: grace

<a id="entry-3-1-harden-reject-privileged-ports-tcp"></a>

**`harden.reject-privileged-ports.tcp { on | off }`**

```haproxy
harden.reject-privileged-ports.tcp { on | off }
harden.reject-privileged-ports.quic { on | off }
```

送信元ポートに特権ポートを使用するクライアントとの通信を禁止する保護を、プロトコルごとに切り替えます。このポート範囲はRFC 6335に従って定義されます。QUICプロトコルでは、この動作は不審であり、なりすましやDNS/NTP増幅攻撃に使われる可能性があるため、デフォルトで保護が有効です。

<a id="entry-3-1-http-err-codes"></a>

**`http-err-codes [+-]<range>[,...] [...]`**

```haproxy
http-err-codes [+-]<range>[,...] [...]
```

終了コードとスティックテーブルの "http_err_cnt" カウンターがエラーと見なすステータスコードの一覧を、置換、縮小、または拡張します。エラーのデフォルト範囲は400から499ですが、状況によっては、特にクライアントエラーを追跡するときに、特定のコードを除外したい場合があります（動的にコンテンツを生成するシステムの404など）。"http-fail-codes" と "http_err_cnt" も参照してください。

範囲を '+' も '-' も付けずに指定すると、既存の範囲を新しい範囲に置き換えます。'+' で始まる範囲は、指定した範囲も含むように既存の範囲を拡張します。指定する範囲は、既存の範囲と重なっていてもいなくてもかまいません。'-' で始まる範囲は、既存の範囲から指定した範囲を取り除きます。範囲は100から599までの数値で表し、必要に応じて、その後に "-" と、最初の数値以上の別の数値を指定して、範囲の上限を表します。同じ追加・削除・置換操作について、複数の範囲をコンマで区切れます。

例:

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

終了コードとスティックテーブルの "http_fail_cnt" カウンターが障害と見なすステータスコードの一覧を、置換、縮小、または拡張します。障害のデフォルト範囲は、クライアントによって発生しうる501と505を除く500から599で、通常はサーバーがリクエストを処理できなかったことを示します。特定の状況で関係がないと分かっているコードは、除外したい場合があります。たとえば、一部のSOAP環境では500はサーバーの障害を意味しません。構文は、前述のhttp-err-codesとまったく同じです。"http-err-codes" と "http_fail_cnt" も参照してください。

<a id="entry-3-1-insecure-fork-wanted"></a>

**`insecure-fork-wanted`**

```haproxy
insecure-fork-wanted
```

デフォルトでは、HAProxyは起動後のスレッドやプロセスの作成を徹底して防ごうとします。これは、出所が不確かなLuaファイルを使用する場合や、悪用できるか不明なバグが残っている可能性のある開発版を試す場合に、特に重要です。また一般に、トラフィックによって予期しないバックグラウンド動作が引き起こされないようにすることは、適切な運用上の配慮です。しかし、この保護によって外部チェックが動作しなくなり、forkできることに明確に依存する一部の特殊なLuaスクリプトが壊れる可能性があります。このオプションは、その保護を無効にするためのものです。無効にするとライブラリやHAProxy自体の脆弱性を悪用しやすくなるため、無効化は望ましくありません。また、Luaなどからのforkは信頼できません。forkされたプロセスが、別のスレッドが保持するロックを偶然引き継ぎ、処理を完了できなくなる可能性があるためです。そのため、このオプションは決して使用せず、そのようなforkが必要な処理を見直して、より安全な方法（外部チェックではなくエージェントを使用するなど）に移すことを強く推奨します。このオプションは、無効にするための "no" プレフィックスをサポートします。haproxyのコマンドラインで "-dI" を指定して有効にすることもできます。

<a id="entry-3-1-insecure-setuid-wanted"></a>

**`insecure-setuid-wanted`**

```haproxy
insecure-setuid-wanted
```

HAProxyは、外部チェックを使用する場合を除き、実行時に実行ファイルを呼び出す必要はありません（外部チェックは使用しないことを強く推奨します）。さらに、空のchroot内に自身を隔離することが想定されています。そのため、ユーザーがリスクを十分に理解しないままsetuid実行ファイルの呼び出しを許可する正当な理由は、基本的にありません。HAProxyが外部チェックを呼び出したり、chrootを無効にしたりする必要がある状況では、ライブラリやHAProxy自体の脆弱性が悪用されると、外部プログラムが実行される可能性があります。Linuxでは、プロセスを制限して、そのような実行ファイルに設定されたsetuidビットを無視させることができます。これにより、そのような状況での権限昇格のリスクが大幅に減ります。HAProxyはデフォルトでこの制限を行います。これが外部チェックで問題になる場合（"ping" コマンドを必要とする場合など）は、globalセクションにこのディレクティブを明示的に追加して、保護を無効にできます。有効にした後は、前に "no" キーワードを付けて再び無効にできます。

<a id="entry-3-1-issuers-chain-path"></a>

**`issuers-chain-path <dir>`**

```haproxy
issuers-chain-path <dir>
```

発行者の補完に使う証明書チェーンを読み込むディレクトリを指定します。すべてのファイルはPEM形式でなければなりません。"crt" または "crt-list" で読み込んだ証明書について、PEMに証明書チェーン（一般に中間証明書とも呼ばれます）が含まれていない場合、証明書の発行者が "issuers-chain-path" で読み込んだチェーンの最初の証明書と一致すれば、HAProxyがチェーンを補完します。PrivateKey+Certificate+IntermediateCA2+IntermediateCA1を含む "crt" ファイルは、PrivateKey+Certificateに置き換えられます。"issuers-chain-path" ディレクトリにIntermediateCA2+IntermediateCA1を含むファイルがあれば、HAProxyがチェーンを補完します。同じ発行者を持つほかのすべての証明書は、メモリ内のチェーンを共有します。

OCSP機能は、.issuerを使用していない場合やPEMにチェーンが含まれていない場合に、補完されたチェーンを使用できます。

<a id="entry-3-1-jwt-allow-none-alg"></a>

**`jwt.allow_none_alg`**

```haproxy
jwt.allow_none_alg
```

'jwt_verify'コンバーターで"none"アルゴリズムのJWTトークンを許可します。このオプションを設定すると、これらのトークンは常に有効とみなされます。デフォルトでは、署名のないトークンは安全でないとみなして拒否します（RFC8725の[セクション3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1)を参照）。

<a id="entry-3-1-jwt-decrypt-alg-list"></a>

**`jwt.decrypt_alg_list <list>`**

```haproxy
jwt.decrypt_alg_list <list>
```

jwt_decrypt_XXXコンバーターで許可するアルゴリズムの一覧を設定します。未サポートまたは無効なアルゴリズムを使用するJWTトークンは、決して復号されません。指定するアルゴリズムは、RFC7518の[4.1節](https://www.rfc-editor.org/rfc/rfc7518#section-4.1)と同じ形式で、コロンで区切らなければなりません。特別な名前 "ALL" を使用すると、サポートされるすべてのアルゴリズムを有効にできます（完全な一覧は "jwt_decrypt_jwk" コンバーターを参照してください）。アルゴリズム名に '!' を追加すると、明示的に無効にできます。"ALL" を指定しない限り、このオプションを使用すると、指定した一覧に明記されていないアルゴリズムはすべて無効になります。

例:

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

jwt_decrypt_XXXコンバーターで許可する暗号化アルゴリズムの一覧を設定します。未サポートまたは無効な暗号化アルゴリズムを使用するJWTトークンは、決して復号されません。指定するアルゴリズムは、RFC7518の[5.1節](https://www.rfc-editor.org/rfc/rfc7518#section-5.1)と同じ形式で、コロンで区切らなければなりません。特別な名前 "ALL" を使用すると、サポートされるすべてのアルゴリズムを有効にできます（完全な一覧は "jwt_decrypt_jwk" コンバーターを参照してください）。アルゴリズム名に '!' を追加すると、明示的に無効にできます。"ALL" を指定しない限り、このオプションを使用すると、指定した一覧に明記されていないアルゴリズムはすべて無効になります。

例:

```shell
# Enable only AES GCM encrypting algorithms
jwt.decrypt_enc_list A128GCM:A192GCM:A256GCM
```

<a id="entry-3-1-key-base"></a>

**`key-base <dir>`**

```haproxy
key-base <dir>
```

"key" ディレクティブに相対パスを指定した場合に、SSL秘密鍵を取得するデフォルトディレクトリを指定します。絶対パスを指定した場合は、そちらが優先され、"key-base" は無視されます。このオプションは、crt-storeのload行でのみ機能します。

<a id="entry-3-1-limited-quic"></a>

**`limited-quic`**

```haproxy
limited-quic
```

QUICをサポートしないバージョンのOpenSSLでhaproxyをコンパイルした場合、QUICリスナーのバインドを明示的に有効にするには、この設定を使用しなければなりません。これにより、haproxy内部の互換レイヤーが有効になります。このレイヤーは、ビルド時にUSE_QUIC_OPENSSL_COMPAT=1で選択しておかなければなりません。この互換レイヤーは、必要なTLS操作の大部分をサポートしますが、QUIC 0-RTT機能はサポートしません。

この機能は主に、QUIC APIが未実装または一部しか実装されていない、バージョン3.5.2より前のOpenSSLを対象としています。3.5.2以降でも互換レイヤーを有効にできますが、おそらく不要です。

limited-quicを設定しても、ビルド時に互換レイヤーを選択していなかった場合、このオプションは通知なく無視され、QUICのTLS操作はTLSライブラリに依存します。

<a id="entry-3-1-localpeer"></a>

**`localpeer <name>`**

```haproxy
localpeer <name>
```

ローカルインスタンスのピア名を設定します。コマンドライン引数 "-L" を指定した場合、または "peers" セクションの定義より後に使用した場合は無視されます。その場合、設定の解析中に警告メッセージが出ます。

このオプションは、環境変数HAPROXY_LOCALPEERも設定します。管理ガイドの "-L" と、後述の "peers" セクションも参照してください。

<a id="entry-3-1-log"></a>

**`log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]`**

```haproxy
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [max level [min level]]
```

グローバルなsyslogサーバーを追加します。複数のグローバルサーバーを定義できます。これらは起動と終了のログに加え、"log global" を設定したプロキシからのすべてのログを受信します。詳細は、プロキシの "log" オプションを参照してください。

<a id="entry-3-1-log-send-hostname"></a>

**`log-send-hostname [<string>]`**

```haproxy
log-send-hostname [<string>]
```

syslogヘッダーのhostnameフィールドを設定します。任意の "string" パラメーターを指定した場合はその文字列の内容を、指定しなかった場合はシステムのホスト名を使用します。一般には、中間のsyslogサーバーを経由してログを中継しない場合や、ログに出力するホスト名を単に変更したい場合に使用します。

<a id="entry-3-1-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

syslogヘッダーのtagフィールドを、この文字列に設定します。デフォルトはコマンドラインから起動した際のプログラム名で、通常は "haproxy" です。同じホストで動作する複数のプロセスを区別するのに便利な場合があります。プロキシごとの "log-tag" ディレクティブも参照してください。

<a id="entry-3-1-lua-load"></a>

**`lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

このグローバルディレクティブは、すべてのスレッドから見える共有コンテキストにLuaファイルを読み込んで実行します。このコンテキストで設定した変数は、どのスレッドからも見えます。Luaプログラムを読み込む最も簡単な推奨方法ですが、グローバル状態で同時に実行できるのは1つのスレッドだけなので、Luaの呼び出しが多い場合はスケールしにくくなります。この方法で読み込んだプログラムでは、"core.thread" 変数は常に0になります。このディレクティブは複数回使用できます。

ファイル本体で次のコードを使用すると、Luaファイルから引数を参照できます。Lua配列のインデックスは1から始まることに注意してください。ファイル内で宣言した "local" 変数は、そのファイル全体で使用でき、ほかのファイルからは使用できません。

     local args = table.pack(...)

<a id="entry-3-1-lua-load-per-thread"></a>

**`lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]`**

```haproxy
lua-load-per-thread <file> [ <arg1> [ <arg2> [ ... ] ] ]
```

このグローバルディレクティブは、起動する各スレッドにLuaファイルを読み込んで実行します。グローバル変数もスレッド内でのみ見えるため、スレッドごとに異なる値が見えることがあります。このため、この方法で読み込むプログラムでは、グローバル変数を使用しないことを強く推奨します。各スレッドに独立したコピーを読み込んで初期化し、すべてをスレッド番号1からnbthreadの順に逐次実行します。一度だけ実行する必要のある処理がある場合、プログラムで "core.thread" 変数を調べ、どのスレッドを初期化しているかを確認することを推奨します。この方法で読み込んだプログラムはすべてのスレッドで並行して動作し、非常に高いスケーラビリティーを得られます。プログラムがグローバル変数に依存しないと確認できた場合、サンプル取得、コンバーター、アクション、サービスを登録する単純な関数を読み込むための推奨方法です。簡便さのため、使用するスレッドが1つだけの場合や、スレッドを無効にしている場合でも、このディレクティブを使用できます（後者の場合はlua-loadと同等です）。このディレクティブは複数回使用できます。

引数の使用方法はlua-loadを参照してください。

<a id="entry-3-1-lua-prepend-path"></a>

**`lua-prepend-path <string> [<type>]`**

```haproxy
lua-prepend-path <string> [<type>]
```

指定した文字列の後にセミコロンを付け、Luaのpackage.`<type>` 変数の先頭に追加します。`<type>` は "path" または "cpath" のいずれかでなければなりません。`<type>` を省略した場合のデフォルトは "path" です。

Luaのパスは、`require` 関数がライブラリのソースファイルを探す方法を指定するパターンを、セミコロンで区切った一覧です。パターン内の疑問符 (?) は、モジュール名に置き換えられます。パスは左から右へ評価します。したがって、後から先頭に追加したパスほど、先に調べられます。

たとえば、次のパスを指定した場合:

```text
lua-prepend-path /usr/share/haproxy-lua/?/init.lua
lua-prepend-path /usr/share/haproxy-lua/?.lua
```

`require "example"` を呼び出すと、Luaは最初に/usr/share/haproxy-lua/example.luaスクリプトの読み込みを試みます。そのファイルがなければ/usr/share/haproxy-lua/example/init.luaを、それもなければデフォルトのパスを試みます。

詳細は、Luaドキュメントの <https://www.lua.org/pil/8.1.html> を参照してください。

<a id="entry-3-1-master-worker"></a>

**`master-worker (deprecated)`**

```haproxy
master-worker (deprecated)
```

マスターワーカーモードです。コマンドライン引数 "-W" と同じです。

このキーワードは非推奨です。"-W" または "-Ws" を使用してマスターワーカーモードで起動してください。

このモードでは "master" を起動し、設定を読み込んだ後に "worker" をforkしてトラフィックを処理します。マスターは、"workers" を監視するプロセスマネージャーとして機能します。

このモードでは、マスターにSIGUSR2シグナルを送信することで、HAProxyを直接リロードできます。リロード時にはマスターが設定を再び読み込み、新しいワーカーをforkします。以前のワーカーは、処理中の仕事が完了するまで維持されます。

マスターワーカーモードは、フォアグラウンドモードとデーモンモードのどちらとも併用できます。

デフォルトでは、たとえばセグメンテーション違反などでワーカーが異常な終了コードを返して終了すると、すべてのワーカーを強制終了し、マスターも終了します。この動作をsystemdのユニットファイルのRestart=on-failureと組み合わせると、プロセス全体を再起動できて便利です。この動作が不要な場合は、"no-exit-on-failure" キーワードを使用しなければなりません。

管理ガイドの "-W" も参照してください。

<a id="entry-3-1-master-worker-no-exit-on-failure"></a>

**`master-worker no-exit-on-failure`**

```haproxy
master-worker no-exit-on-failure
```

マスターワーカーモードでは、デフォルトで、たとえばセグメンテーション違反などでワーカーが異常な終了コードを返して終了すると、すべてのワーカーを強制終了し、マスターも終了します。この動作をsystemdのユニットファイルのRestart=on-failureと組み合わせると、プロセス全体を再起動できて便利です。

このキーワードは、ワーカーがクラッシュしたときに、すべてを強制終了する代わりに、残りのプロセスを生かしておけるようにします。デバッグのみを目的としたもので、マスタープロセスを異常な状態にする可能性があるため、注意して使用する必要があります。

<a id="entry-3-1-max-threads-per-group"></a>

**`max-threads-per-group <number>`**

```haproxy
max-threads-per-group <number>
```

スレッドグループ内の最大スレッド数を定義します。"thread-groups" ディレクティブでスレッドグループ数を固定していない限り、haproxyは要求されたスレッド数を満たすのに必要な数だけスレッドグループを作成します。最小値は1、最大値は64です（64ビットシステムの場合。32ビットシステムでは32です）。小さい値は、共有状態へのアトミック操作による競合を減らしますが、すべてのリスナーの作成や、アイドル状態のバックエンド接続の保持に必要なソケット数を増やすことがあります。大きい値はこれらのコストを減らしますが、競合時のCPU使用率が高まり、接続レートが低下します。デフォルト値は16です。これは、複数のベンダーのx86_64プロセッサーや大規模なArm64システムを含むさまざまなシステムで、ベアメタルとハイパーバイザーの両方について行った実験で、最もよいバランスが得られた値です。

<a id="entry-3-1-mworker-max-reloads"></a>

**`mworker-max-reloads <number>`**

```haproxy
mworker-max-reloads <number>
```

マスターワーカーモードで、ワーカーがリロード後も存続できる回数を制限します。リロード後にワーカーが終了せず、リロード回数がこの値を超えた場合、そのワーカーにSIGTERMを送信します。このオプションは、ワーカー数を制御するのに役立ちます。管理ガイドの "show proc" も参照してください。

この値のデフォルトは50です。

<a id="entry-3-1-nbthread"></a>

**`nbthread <number>`**

```haproxy
nbthread <number>
```

この設定は、スレッドのサポートを組み込んでビルドした場合にのみ使用できます。HAProxyを `<number>` 個のスレッドで実行します。"nbthread" は、HAProxyをフォアグラウンドで起動した場合にも機能します。CPUアフィニティーをサポートする一部のプラットフォームでは、デフォルトの "nbthread" 値を、起動時にプロセスがバインドされているCPUの数に自動設定します。そのため、呼び出し元プロセスから "taskset" や "cpuset" などのコマンドを使って、スレッド数を簡単に調整できます。それ以外の場合のデフォルト値は1です。デフォルト値は "haproxy -vv" の出力に表示されます。ここで設定した値や自動検出した値には、"thread-hard-limit" が設定されていれば、その上限が適用されます。

<a id="entry-3-1-numa-cpu-mapping"></a>

**`numa-cpu-mapping`**

```haproxy
numa-cpu-mapping
```

NUMAを認識するプラットフォームで実行する場合、"cpu-policy" ディレクティブがトポロジーを調べ、使用する最適なCPUの集合と対応するスレッド数を決められるようにします。ただし、特定のアーキテクチャーで適用されたバインドが最適でない場合は、'no numa-cpu-mapping' で無効にできます。この自動バインドは、設定に 'nbthread' がある場合、'cpu-map' ディレクティブやtasksetユーティリティなどでプロセスのアフィニティーをすでに指定している場合、またはcpu-policyをほかの値に設定している場合にも適用されません。"cpu-map"、"cpu-policy"、および "cpu-set" も参照してください。

<a id="entry-3-1-ocsp-update-disable"></a>

**`ocsp-update.disable [ on | off ]`**

```haproxy
ocsp-update.disable [ on | off ]
```

HAProxyのocsp-updateを完全に無効にします。ocsp-updateに関する設定はすべて無視されます。デフォルトは "off" です。自動更新の仕組みについては、"ocsp-update" オプションを参照してください。

<a id="entry-3-1-ocsp-update-httpproxy"></a>

**`ocsp-update.httpproxy <address>[:port]`**

```haproxy
ocsp-update.httpproxy <address>[:port]
```

OCSPの更新にHTTPプロキシを使用できるようにします。HTTPでのみ機能し、HTTPSはサポートしません。このオプションにより、OCSP更新処理が、プロキシへのリクエストで絶対URIを送信できるようになります。

<a id="entry-3-1-ocsp-update-maxdelay"></a>

**`ocsp-update.maxdelay <number>`**

```haproxy
ocsp-update.maxdelay <number>
tune.ssl.ocsp-update.maxdelay <number> (deprecated)
```

同じOCSPレスポンスに対する自動更新の最大間隔を設定します。時間は秒単位で指定し、デフォルトは3600（1時間）です。"ocsp-update.mindelay" より大きい値に設定しなければなりません。自動更新の仕組みについては、"ocsp-update" オプションを参照してください。

<a id="entry-3-1-ocsp-update-mindelay"></a>

**`ocsp-update.mindelay <number>`**

```haproxy
ocsp-update.mindelay <number>
tune.ssl.ocsp-update.mindelay <number> (deprecated)
```

同じOCSPレスポンスに対する自動更新の最小間隔を設定します。時間は秒単位で指定し、デフォルトは300（5分）です。明示的な有効期限がないOCSPレスポンスに特に有用です。"ocsp-update.maxdelay" より小さい値に設定しなければなりません。自動更新の仕組みについては、"ocsp-update" オプションを参照してください。

<a id="entry-3-1-ocsp-update-mode"></a>

**`ocsp-update.mode [ on | off ]`**

```haproxy
ocsp-update.mode [ on | off ]
```

設定で使用するすべての証明書について、デフォルトのocsp-updateモードを設定します。このグローバルオプションは、crt-listの "ocsp-update" オプションで上書きできます。デフォルトは "off" です。自動更新の仕組みについては、"ocsp-update" オプションを参照してください。

<a id="entry-3-1-pidfile"></a>

**`pidfile <pidfile>`**

```haproxy
pidfile <pidfile>
```

デーモンモードではすべてのデーモンのPIDをファイル `<pidfile>` に書き込み、マスターワーカーモードではマスタープロセスのPIDをファイル `<pidfile>` に書き込みます。このオプションは、コマンドライン引数 "-p" と同じです。ファイルは、プロセスを起動するユーザーからアクセスできなければなりません。"daemon" と "master-worker" も参照してください。

<a id="entry-3-1-pp2-never-send-local"></a>

**`pp2-never-send-local`**

```haproxy
pp2-never-send-local
```

HAProxyのバージョン2.1まで存在したPROXYプロトコルv2実装のバグにより、ヘルスチェックでLOCALコマンドの代わりにPROXYコマンドが送信されていました。これはごく軽微な問題ですが、一部のサーバーのログを混乱させます。残念ながら、このバグの発見が遅く、PROXYプロトコル実装をHAProxyに対してしか試験していなかった可能性のある一部のサーバーが、LOCALコマンドを正しく処理できず、HAProxyによるチェックで "down" のままになることが判明しました。その場合、影響を受けるコンポーネントのベンダーに連絡して修正されるまでの間、このグローバルオプションを有効にして、以前の誤った動作に戻せます。このオプションはデフォルトで無効で、"send-proxy-v2" を指定したすべてのサーバーに作用します。

<a id="entry-3-1-presetenv"></a>

**`presetenv <name> <value>`**

```haproxy
presetenv <name> <value>
```

環境変数 `<name>` を値 `<value>` に設定します。変数がすでに存在する場合は、上書きしません。変更はただちに有効になり、設定ファイルの次の行から新しい値を参照できます。"setenv"、"resetenv"、および "unsetenv" も参照してください。

<a id="entry-3-1-prealloc-fd"></a>

**`prealloc-fd`**

```haproxy
prealloc-fd
```

最大のファイルディスクリプターを一度だけ開き、カーネルのデータ構造を事前に割り当てます。これにより、nbthread\>1の場合に、HAProxyがファイルディスクリプターを開くためにカーネルがデータ構造を拡張する際の短い停止を防ぎます。

<a id="entry-3-1-resetenv"></a>

**`resetenv [<name> ...]`**

```haproxy
resetenv [<name> ...]
```

引数で指定したものを除き、すべての環境変数を削除します。setenvやunsetenvで新しい値を設定する前に、整理された管理可能な環境にできます。時刻を操作する関数などの内部関数に加え、OpenSSLや外部チェックも、環境変数を使用することがある点に注意してください。使用には細心の注意を払い、十分に検証した後でなければなりません。変更はただちに有効になり、設定ファイルの次の行から新しい環境を参照できます。"setenv"、"presetenv"、および "unsetenv" も参照してください。

<a id="entry-3-1-server-state-base"></a>

**`server-state-base <directory>`**

```haproxy
server-state-base <directory>
```

先頭が '/' でないすべてのサーバー状態ファイル名に付ける、ディレクトリプレフィックスを指定します。"server-state-file"、"load-server-state-from-file"、および "server-state-file-name" も参照してください。

<a id="entry-3-1-server-state-file"></a>

**`server-state-file <file>`**

```haproxy
server-state-file <file>
```

サーバーの状態を含むファイルのパスを指定します。パスがスラッシュ ('/') で始まる場合は絶対パスとして扱い、それ以外の場合は、"server-state-base" が設定されていればそのディレクトリ、未設定ならカレントディレクトリからの相対パスとして扱います。HAProxyをリロードする前に、statsコマンド "show servers state" でサーバーの現在の状態を保存できます。このコマンドの出力は、`<file>` が指すファイルに書き込まなければなりません。起動時には、トラフィックを処理する前に、ファイルに記載され、現在の稼働設定にも存在する各サーバーの状態を、HAProxyが読み込んで適用します。"server-state-base"、"show servers state"、"load-server-state-from-file"、および "server-state-file-name" も参照してください。

<a id="entry-3-1-set-dumpable"></a>

**`set-dumpable [ on | off | libs ]`**

```haproxy
set-dumpable [ on | off | libs ]
```

プロセスがクラッシュしたときのコアダンプの動作を選択します。使用できるオプションは次のとおりです。

- on: コアダンプが無効になっていた場合、プロセス単位で有効にします。

- off: 有効になっているコアダンプを無効にします。

- libs: デバッグに必要なバイナリーとライブラリのコピーを含めて、コアダンプを有効にします。開発者からこの設定を求められることがあります。この場合、haproxyは依存するライブラリをメモリに読み込み、そのまま保持しようとします。プロセスがクラッシュすると、それらもコアに出力されるため、ファイルシステムから取得する必要がなく、コアと一致しない危険もなくなります。追加で数メガバイトから数十メガバイトのRAMを使用するため、小規模なシステムでは使わない方がよいでしょう。

このオプションは通常は無効のままとし、開発者から求められた場合にだけ有効にすることを推奨します。デフォルトでは無効です。引数を付けずに指定した場合のデフォルトは "on" です。有効にした後でも、"no" キーワードを前に付けるか "off" を指定すれば、強制的に無効にできます。パフォーマンスや安定性には影響しませんが、ファイルサイズの制限 (ulimit -f)、コアサイズの制限 (ulimit -c)、UID/GID変更後のプロセスの "dumpability"（Linuxの/proc/sys/fs/suid_dumpableなど）によって無効になっていた可能性のあるコアダンプを、できる限り再度有効にしようとします。それでも、カレントディレクトリの権限（どのディレクトリから起動しているかを確認してください）、chroot先ディレクトリの権限（chrootディレクティブを一時的に無効にするか、専用の書き込み可能な場所に変更する必要がある場合があります）、その他のシステム固有の制約によって、コアダンプが制限されることがあります。たとえば、一部のLinuxでは、デフォルトのコアファイルを、システムにインストールされてすらいない実行ファイルへのパスに置き換えていることで知られています（/proc/sys/kernel/core_patternを確認してください）。多くの場合、単に "core"、"core.%p"、または "/var/log/core/core.%p" と書けば問題を解決できます。まれな問題が再発するのを待つためにこのオプションを有効にする場合は、最初にたとえば "haproxy" プロセスへ "kill -11" を実行してダンプの取得を試し、終了時に期待した場所へコアが残ることを確認しておくとよいでしょう。

<a id="entry-3-1-set-var"></a>

**`set-var <var-name> <expr>`**

```haproxy
set-var <var-name> <expr>
```

プロセス全体の変数 '`<var-name>`' を、サンプル式 `<expr>` を評価した結果に設定します。変数 '`<var-name>`' は、'proc.' プレフィックスを使うプロセス全体の変数でなければなりません。TCPルールやHTTPルールの 'set-var' アクションと同じように動作しますが、式は設定の解析時に評価され、変数はただちに設定されます。式で使用できるサンプル取得関数とコンバーターは、通常は 'int(value)' や 'str(value)' など、内部データを使用するものだけです。すでに確保された変数も参照できます。これらの変数は、その後、通常のルールセットから読み取ったり変更したりできます。

例:

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

プロセス全体の変数 '`<var-name>`' を、ログ形式 `<fmt>` を評価して得られた文字列に設定します。変数 '`<var-name>`' は、'proc.' プレフィックスを使うプロセス全体の変数でなければなりません。TCPルールやHTTPルールの 'set-var-fmt' アクションと同じように動作しますが、式は設定の解析時に評価され、変数はただちに設定されます。式で使用できるサンプル取得関数とコンバーターは、通常は 'int(value)' や 'str(value)' など、内部データを使用するものだけです。すでに確保された変数も参照できます。これらの変数は、その後、通常のルールセットから読み取ったり変更したりできます。カスタムログ形式の構文については、[8.2.6節](/ja/docs/haproxy/configuration-logging/#section-8-2-6)を参照してください。

例:

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

root以外のユーザー (uid \> 0) として起動・実行する場合、またはuid 0 (root) で起動してからroot以外のユーザーに切り替える場合に、保持しなければならないケーパビリティーの一覧を設定します。デフォルトでは、uidを切り替えるとすべての権限を失います。しかし、透過プロキシで別のアドレスを送信元としてサーバーに接続する場合や、1024未満のポートにバインドする場合、たとえば "tune.quic.fe.sock-per-conn default-on" を使用する場合には、一部の権限が必要になることが多く、全体をuid 0で実行する構成になってしまいます。ケーパビリティーの設定は、必要なものだけを保持するため、通常はより安全な代替手段です。この機能はOSに依存し、ビルド時にUSE_LINUX_CAP=1を設定したLinuxでのみ有効です。サポートするケーパビリティーの一覧もOSに依存し、無効な名前や空の名前を渡したときのエラーメッセージに列挙されます。複数のケーパビリティーをコンマで区切って指定できます。よく使われるものでは、"cap_net_raw" は別のアドレスへの透過的なバインドを許可し、"cap_net_bind_service" は特権ポートへのバインドを許可してQUICで使用できます。同じroot以外のユーザーでプロセスを起動・実行する場合は、このキーワードに加えて、setcapでhaproxyバイナリーファイルに必要なケーパビリティーを設定することを推奨します。haproxyバイナリーのケーパビリティー設定については、管理ガイドの13.1章「Linuxケーパビリティーのサポート」を参照してください。

例:

```text
global
    setcap cap_net_bind_service,cap_net_admin
```

<a id="entry-3-1-setenv"></a>

**`setenv <name> <value>`**

```haproxy
setenv <name> <value>
```

環境変数 `<name>` を値 `<value>` に設定します。変数がすでに存在する場合は、上書きします。変更はただちに有効になり、設定ファイルの次の行から新しい値を参照できます。"presetenv"、"resetenv"、および "unsetenv" も参照してください。

<a id="entry-3-1-shm-stats-file"></a>

**`shm-stats-file <name>`**

```haproxy
shm-stats-file <name>
```

このディレクティブを設定すると、統計カウンターの保存に共有メモリを使用するようになります。`<name>` はshm_open()の引数として使用し、一意の場所にある共有メモリを開きます。そのため、このディレクティブはshm_open()をサポートするシステムでのみ使用できます。統計にSHMを使用する場合、GUIDが設定されていることを条件に、フロントエンド、バックエンド、リスナー、サーバーの共有可能なカウンターをすべてSHMに保存します。haproxyをリロードすると、新しいプロセスはGUIDと型に基づいて、設定で定義したオブジェクトと関連付けられるオブジェクトをSHMから探します。これにより、リロード時に一部のカウンターの値を保持することを目指します。一方、haproxyを正常に停止すると、SHMオブジェクトを解放するため、カウンターは実際にリセットされます。新しいプロセスを起動する前にファイルを手動で削除し、強制的にリセットすることもできます。

"guid"、"guid-prefix"、および "shm-stats-file-max-objects" も参照してください。

<a id="entry-3-1-shm-stats-file-max-objects"></a>

**`shm-stats-file-max-objects <number>`**

```haproxy
shm-stats-file-max-objects <number>
```

共有カウンター用の共有メモリに保存できるオブジェクト数の、スレッドグループごとの上限を定義します。これはSHMの最大メモリサイズに直接関係し、実行時の再マッピングを避けるため、SHMを所定のサイズであらかじめマッピングするために使用します。デフォルトは2kで、ほとんどの構成で不適切なメモリ使用量になる危険を避けながら利用できるはずですが、必要に応じて簡単に変更できます。この値が小さすぎて、共有メモリに保存する予定のオブジェクトを登録できない場合、haproxyは起動時に問題を報告します。"shm-stats-file" を定義した場合にのみ意味があります。

"thread-groups" も参照してください。

<a id="entry-3-1-ssl-default-bind-ciphers"></a>

**`ssl-default-bind-ciphers <ciphers>`**

```haproxy
ssl-default-bind-ciphers <ciphers>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "bind" 行について、TLSv1.2までのSSL/TLSハンドシェイクでネゴシエーションする暗号アルゴリズムの一覧（暗号スイート）を表す、デフォルトの文字列を設定します。文字列の形式は、OpenSSLのmanページの "man 1 ciphers" で定義されています。背景情報や推奨事項については、たとえば (<https://wiki.mozilla.org/Security/Server_Side_TLS>) と (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>) を参照してください。TLSv1.3の暗号設定については、"ssl-default-bind-ciphersuites" キーワードを参照してください。詳細は "bind" キーワードを参照してください。

<a id="entry-3-1-ssl-default-bind-ciphersuites"></a>

**`ssl-default-bind-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-bind-ciphersuites <ciphersuites>
```

この設定は、OpenSSLのサポートを組み込み、OpenSSL 1.1.1以降を使ってHAProxyをビルドした場合にのみ使用できます。独自の指定を明示していないすべての "bind" 行について、TLSv1.3ハンドシェイクでネゴシエーションする暗号アルゴリズムの一覧（暗号スイート）を表す、デフォルトの文字列を設定します。文字列の形式は、OpenSSLのmanページ "man 1 ciphers" の "ciphersuites" 節で定義されています。TLSv1.2以前の暗号設定については、"ssl-default-bind-ciphers" キーワードを参照してください。この設定はTLSv1.2の暗号スイートを受け入れることもありますが、文書化されていない動作であり、一貫性がなかったりバグがあったりする可能性があるため、推奨しません。OpenSSLのデフォルトのTLSv1.3暗号スイートは次のとおりです。
"TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256"

TLSv1.3がサポートする暗号スイートは、次の5つだけです。

- TLS_AES_128_GCM_SHA256
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_CCM_SHA256
- TLS_AES_128_CCM_8_SHA256

詳細は "bind" キーワードを参照してください。

例:

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

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "bind" 行について、クライアント認証に関する署名アルゴリズムの一覧を表す、デフォルトの文字列を設定します。形式は、署名アルゴリズムをコロンで区切った一覧です。各署名アルゴリズムは、TLS1.3の署名方式名 ("rsa_pss_rsae_sha256")、または公開鍵アルゴリズム + ダイジェストの形式 ("ECDSA+SHA256") のいずれかで指定できます。両方の形式を同じ一覧に含められます。形式の詳細は、SSL_CTX_set1_client_sigalgs(3)を参照してください。署名アルゴリズムの一覧は、RFC8446の[4.2.3節](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)と、OpenSSLのssl/t1_lib.cファイルにもあります。TLSv1.1以前では、署名アルゴリズムを個別にネゴシエーションしないため、この設定は適用されません。中間装置との互換性が必要な場合を除き、この設定の変更は推奨しません。

<a id="entry-3-1-ssl-default-bind-curves"></a>

**`ssl-default-bind-curves <curves>`**

```haproxy
ssl-default-bind-curves <curves>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。ECDHEを使うSSL/TLSハンドシェイクでネゴシエーションする楕円曲線アルゴリズムの一覧（曲線スイート）を表す、デフォルトの文字列を設定します。形式は、曲線名をコロンで区切った一覧です。詳細は "bind" キーワードを参照してください。

<a id="entry-3-1-ssl-default-bind-options"></a>

**`ssl-default-bind-options [<option>]...`**

```haproxy
ssl-default-bind-options [<option>]...
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。すべての "bind" 行に強制するデフォルトのssl-optionsを設定します。使用できるオプションは、"bind" キーワードを参照してください。

例:

```text
global
   ssl-default-bind-options ssl-min-ver TLSv1.0 no-tls-tickets
```

<a id="entry-3-1-ssl-default-bind-sigalgs"></a>

**`ssl-default-bind-sigalgs <sigalgs>`**

```haproxy
ssl-default-bind-sigalgs <sigalgs>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "bind" 行について、TLSv1.2とTLSv1.3のハンドシェイクでネゴシエーションする署名アルゴリズムの一覧を表す、デフォルトの文字列を設定します。形式は、署名アルゴリズムをコロンで区切った一覧です。各署名アルゴリズムは、TLS1.3の署名方式名 ("rsa_pss_rsae_sha256")、または公開鍵アルゴリズム + ダイジェストの形式 ("ECDSA+SHA256") のいずれかで指定できます。両方の形式を同じ一覧に含められます。形式の詳細は、SSL_CTX_set1_sigalgs(3)を参照してください。署名アルゴリズムの一覧は、RFC8446の[4.2.3節](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)と、OpenSSLのssl/t1_lib.cファイルにもあります。TLSv1.1以前では、署名アルゴリズムを個別にネゴシエーションしないため、この設定は適用されません。中間装置との互換性が必要な場合を除き、この設定の変更は推奨しません。

<a id="entry-3-1-ssl-default-server-ciphers"></a>

**`ssl-default-server-ciphers <ciphers>`**

```haproxy
ssl-default-server-ciphers <ciphers>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "server" 行について、TLSv1.2までのサーバーとのSSL/TLSハンドシェイクでネゴシエーションする暗号アルゴリズムの一覧を表す、デフォルトの文字列を設定します。文字列の形式は、OpenSSLのmanページの "man 1 ciphers" で定義されています。背景情報や推奨事項については、たとえば (<https://wiki.mozilla.org/Security/Server_Side_TLS>) と (<https://mozilla.github.io/server-side-tls/ssl-config-generator/>) を参照してください。TLSv1.3の暗号設定については、"ssl-default-server-ciphersuites" キーワードを参照してください。詳細は "server" キーワードを参照してください。

<a id="entry-3-1-ssl-default-server-ciphersuites"></a>

**`ssl-default-server-ciphersuites <ciphersuites>`**

```haproxy
ssl-default-server-ciphersuites <ciphersuites>
```

この設定は、OpenSSLのサポートを組み込み、OpenSSL 1.1.1以降を使ってHAProxyをビルドした場合にのみ使用できます。独自の指定を明示していないすべての "server" 行について、サーバーとのTLSv1.3ハンドシェイクでネゴシエーションする暗号アルゴリズムの一覧を表す、デフォルトの文字列を設定します。文字列の形式は、OpenSSLのmanページ "man 1 ciphers" の "ciphersuites" 節で定義されています。TLSv1.2以前の暗号設定については、"ssl-default-server-ciphers" キーワードを参照してください。詳細は "server" キーワードを参照してください。

<a id="entry-3-1-ssl-default-server-client-sigalgs"></a>

**`ssl-default-server-client-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-client-sigalgs <sigalgs>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "server" 行について、クライアント認証に関する署名アルゴリズムの一覧を表す、デフォルトの文字列を設定します。形式は、署名アルゴリズムをコロンで区切った一覧です。各署名アルゴリズムは、TLS1.3の署名方式名 ("rsa_pss_rsae_sha256")、または公開鍵アルゴリズム + ダイジェストの形式 ("ECDSA+SHA256") のいずれかで指定できます。両方の形式を同じ一覧に含められます。形式の詳細は、SSL_CTX_set1_client_sigalgs(3)を参照してください。署名アルゴリズムの一覧は、RFC8446の[4.2.3節](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)と、OpenSSLのssl/t1_lib.cファイルにもあります。TLSv1.1以前では、署名アルゴリズムを個別にネゴシエーションしないため、この設定は適用されません。中間装置との互換性が必要な場合を除き、この設定の変更は推奨しません。

<a id="entry-3-1-ssl-default-server-curves"></a>

**`ssl-default-server-curves <curves>`**

```haproxy
ssl-default-server-curves <curves>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。ECDHEを使うSSL/TLSハンドシェイクでネゴシエーションする楕円曲線アルゴリズムの一覧（曲線スイート）を表す、デフォルトの文字列を設定します。形式は、曲線名をコロンで区切った一覧です。詳細は "server" キーワードを参照してください。

<a id="entry-3-1-ssl-default-server-options"></a>

**`ssl-default-server-options [<option>]...`**

```haproxy
ssl-default-server-options [<option>]...
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。すべての "server" 行に強制するデフォルトのssl-optionsを設定します。使用できるオプションは、"server" キーワードを参照してください。

<a id="entry-3-1-ssl-default-server-sigalgs"></a>

**`ssl-default-server-sigalgs <sigalgs>`**

```haproxy
ssl-default-server-sigalgs <sigalgs>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "server" 行について、TLSv1.2とTLSv1.3のハンドシェイクでネゴシエーションする署名アルゴリズムの一覧を表す、デフォルトの文字列を設定します。形式は、署名アルゴリズムをコロンで区切った一覧です。各署名アルゴリズムは、TLS1.3の署名方式名 ("rsa_pss_rsae_sha256")、または公開鍵アルゴリズム + ダイジェストの形式 ("ECDSA+SHA256") のいずれかで指定できます。両方の形式を同じ一覧に含められます。形式の詳細は、SSL_CTX_set1_sigalgs(3)を参照してください。署名アルゴリズムの一覧は、RFC8446の[4.2.3節](https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3)と、OpenSSLのssl/t1_lib.cファイルにもあります。TLSv1.1以前では、署名アルゴリズムを個別にネゴシエーションしないため、この設定は適用されません。中間装置との互換性が必要な場合を除き、この設定の変更は推奨しません。

<a id="entry-3-1-ssl-dh-param-file"></a>

**`ssl-dh-param-file <file>`**

```haproxy
ssl-dh-param-file <file>
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。独自の指定を明示していないすべての "bind" 行について、一時的なDiffie-Hellman (DHE) 鍵交換を使用するSSL/TLSハンドシェイクで使う、デフォルトのDHパラメーターを設定します。bindの証明書ファイルにカスタムDHパラメーターがあれば、それが優先されます。ssl-dh-param-fileでも証明書ファイルへの直接指定でもカスタムDHパラメーターを指定していない場合、tune.ssl.default-dh-paramを設定しない限り、DHE暗号は使用されません。後者を設定した場合は、指定したサイズの定義済みDHパラメーターを使用します。カスタムパラメーターの方が安全であることが知られているため、その使用を推奨します。OpenSSLコマンド "openssl dhparam `<size>`" でカスタムDHパラメーターを生成できます。1024ビットのDHパラメーターはもはや安全とは見なせないため、サイズは少なくとも2048にすることを推奨します。

<a id="entry-3-1-ssl-passphrase-cmd"></a>

**`ssl-passphrase-cmd <cmd> <args> ...`**

```haproxy
ssl-passphrase-cmd <cmd> <args> ...
```

この設定は、OpenSSLのサポートを組み込んでビルドした場合にのみ使用できます。初期化中に暗号化された証明書を読み込むときに呼び出す、完全なコマンドラインを定義できます。コマンドには、スクリプトなど任意のプログラムを使用できます。最初の引数には暗号化された秘密鍵のパス、その後にユーザー定義の "args" パラメーターが渡されます。プログラムは、その暗号化された秘密鍵を復号できるパスフレーズを標準出力に出力すべきです。初期化中に新しい暗号化された秘密鍵を読み込むたびに、HAProxyはまず、すでに分かっているほかのすべてのパスフレーズで秘密鍵の復号を試みます。どれも成功しなかった場合に、パスフレーズコマンドを再度呼び出します。

<a id="entry-3-1-ssl-propquery"></a>

**`ssl-propquery <query>`**

```haproxy
ssl-propquery <query>
```

この設定は、OpenSSLのサポートを組み込んでビルドし、OpenSSLのバージョンが少なくとも3.0である場合にのみ使用できます。プロバイダーからアルゴリズムを取得するときに使用する、デフォルトのプロパティ文字列を定義できます。opensslのpropqueryオプションと同じように動作し、同じ構文に従います（<https://www.openssl.org/docs/man3.0/man7/property.html> を参照してください）。たとえば、fooとdefaultの両プロバイダーを読み込んでいる場合、propquery "?provider=foo" を指定すると、デフォルトでfooプロバイダーのアルゴリズム実装を選び、見つからなければdefaultプロバイダーの実装にフォールバックします。

<a id="entry-3-1-ssl-provider"></a>

**`ssl-provider <name>`**

```haproxy
ssl-provider <name>
```

この設定は、OpenSSLのサポートを組み込んでビルドし、OpenSSLのバージョンが少なくとも3.0である場合にのみ使用できます。初期化中にプロバイダーを読み込めます。読み込みに成功すると、そのプロバイダーが提供する機能をHAProxyで使用できるようになります。設定ファイルには複数の 'ssl-provider' オプションを指定でき、記述した順にプロバイダーを読み込みます。

プロバイダーを明示的に読み込むと、OpenSSLは 'default' プロバイダーを自動的に読み込まなくなります。OpenSSLでは、読み込むプロバイダーを設定ファイル（openssl.cnfなど）に直接定義することもできるため、プロバイダーを読み込むのに必ずしも 'ssl-provider' オプションが必要なわけではありません。CLIコマンド "show ssl providers" で、正常に読み込まれたすべてのプロバイダーを表示できます。

OpenSSLプロバイダーのデフォルトの検索パスは、"openssl version -a" コマンドの出力で確認できます。プロバイダーが別のディレクトリにある場合は、環境変数OPENSSL_MODULESに、そのプロバイダーがあるディレクトリを設定できます。

"ssl-propquery" と "ssl-provider-path" も参照してください。

<a id="entry-3-1-ssl-provider-path"></a>

**`ssl-provider-path <path>`**

```haproxy
ssl-provider-path <path>
```

この設定は、OpenSSLのサポートを組み込んでビルドし、OpenSSLのバージョンが少なくとも3.0である場合にのみ使用できます。OpenSSLがプロバイダーを探す際の検索パスを指定できます。環境変数OPENSSL_MODULESと同じように動作します。後続の 'ssl-provider' オプションに対して、新しい 'ssl-provider-path' を定義するまで使用されます。"ssl-provider" も参照してください。

<a id="entry-3-1-ssl-load-extra-del-ext"></a>

**`ssl-load-extra-del-ext`**

```haproxy
ssl-load-extra-del-ext
```

HAProxyが追加のSSLファイルを検索する方法を設定できます。デフォルトでは、HAProxyはファイル名に新しい拡張子を追加します（例: "foobar.crt" に対して "foobar.crt.key" を読み込みます）。このオプションを有効にすると、新しい拡張子を追加する前に既存の拡張子を削除します（例: "foobar.crt" に対して "foobar.key" を読み込みます）。

このオプションが機能するには、crtファイルの拡張子が ".crt" でなければなりません。

このオプションは、バンドルの拡張子 (.ecdsa, .rsa. .dsa) に対応せず、それらを削除しようとはしません。

このオプションはデフォルトで無効です。"ssl-load-extra-files" も参照してください。

<a id="entry-3-1-ssl-load-extra-files"></a>

**`ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*`**

```haproxy
ssl-load-extra-files <none|all|bundle|sctl|ocsp|issuer|key>*
```

SSL証明書の読み込み中に、明示していないファイルをHAProxyが探す方法を変更します。このオプションは "bind" 行と "server" 行の両方に関連付けられた証明書に適用されますが、一部の追加ファイルは、"server" 行の証明書では機能上の効果を持ちません。

デフォルトでは、HAProxyは設定で指定していない多数のファイルを自動検出します。起動時間を最適化するために、この動作を無効にしたい場合があります。

"none": 設定で指定したファイルだけを読み込みます。ファイルが存在しない場合も、証明書バンドルを読み込もうとはしません。ディレクトリの場合、証明書のベース名が同じでも、バンドルにまとめようとはしません。

"all": これがデフォルトの動作です。バンドル、sctl、ocsp、issuer、keyをすべて読み込もうとします。

"bundle": 設定で指定したファイルが存在しない場合、HAProxyは 「証明書バンドル」を読み込もうとします。証明書バンドルを扱うのはフロントエンド側だけで、バックエンド証明書では機能しません。

HAProxy 2.3以降では、バンドルを同じOpenSSL証明書ストアに読み込まず、各証明書を別のストアに読み込みます。これは、複数の "crt" を宣言することと同じです。この動作にはOpenSSL 1.1.1が必要です。つまり、バンドルは現在では後方互換性のためだけに使用され、RSA/ECCを併用するbind設定には、もはや必須ではありません。

これらのPEMファイルを、HAProxyが認識する 「証明書バンドル」にまとめるには、次の命名規則に従わなければなりません。バンドルに含めるすべてのPEMファイルは同じベース名を持ち、鍵の種類を示す接尾辞を付ける必要があります。現在サポートする接尾辞は、rsa、dsa、ecdsaの3つです。たとえば、[www.example.com](http://www.example.com)にRSAファイルとECDSAファイルの2つのPEMファイルがある場合、名前は "example.pem.rsa" と "example.pem.ecdsa" にしなければなりません。ファイル名の最初の部分は任意で、接尾辞だけが重要です。このバンドルをHAProxyに読み込むには、ベース名だけを指定します。

例: bind :8443 ssl crt example.pem

接尾辞はHAProxyに渡さない点に注意してください。これによって、HAProxyに証明書バンドルを探すよう指示します。

HAProxyは、バンドル内のすべてのPEMファイルを、複数の "crt" に個別に設定したかのように読み込みます。

各ファイルを個別に読み込むため、バンドルの読み込みは、ディレクトリの読み込みに影響しなくなりました。

CLIでは、バンドルは別々のファイルとして扱われ、コミットにはバンドルの拡張子が必要です。

複数証明書のバンドルでは、OCSPファイル (.ocsp)、発行者ファイル (.issuer)、証明書の透明性 (.sctl)、および秘密鍵 (.key) をサポートします。

"sctl": crtキーワードごとに "`<basename>`.sctl" の読み込みを試みます。バックエンド証明書に指定した場合も読み込みますが、機能上の効果はありません。

"ocsp": crtキーワードごとに "`<basename>`.ocsp" の読み込みを試みます。バックエンド証明書に指定した場合も読み込みますが、機能上の効果はありません。

"issuer": OCSPファイルの発行者がPEMファイルに含まれていない場合、"`<basename>`.issuer" の読み込みを試みます。バックエンド証明書に指定した場合も読み込みますが、機能上の効果はありません。

"key": PEMファイルに秘密鍵が含まれていない場合、秘密鍵を含むファイル "`<basename>`.key" の読み込みを試みます。

デフォルトの動作は "all" です。

例:

```text
ssl-load-extra-files bundle sctl
ssl-load-extra-files sctl ocsp issuer
ssl-load-extra-files none
```

関連項目: "crt"、bindオプションについての[5.1節](/ja/docs/haproxy/bind-and-server-options/#section-5-1)、serverオプションについての[5.2節](/ja/docs/haproxy/bind-and-server-options/#section-5-2)。

<a id="entry-3-1-ssl-security-level"></a>

**`ssl-security-level <number>`**

```haproxy
ssl-security-level <number>
```

<https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html> で説明されているOpenSSLのセキュリティレベルを選択できます。このレベルは、HAProxy内のすべてのSSLコンテキストに適用されます。サポートする値は0から5までだけです。

デフォルト値は、OpenSSLのバージョン、ディストリビューション、およびライブラリのコンパイル方法によって異なります。

このディレクティブには、少なくともOpenSSL 1.1.1が必要です。

<a id="entry-3-1-ssl-server-verify"></a>

**`ssl-server-verify [none|required]`**

```haproxy
ssl-server-verify [none|required]
```

サーバー側のSSL検証のデフォルト動作を指定します。'none' を指定すると、サーバー証明書を検証しません。コマンドラインオプション '-dV' で強制しない限り、デフォルトは 'required' です。

<a id="entry-3-1-ssl-skip-self-issued-ca"></a>

**`ssl-skip-self-issued-ca`**

```haproxy
ssl-skip-self-issued-ca
```

自己発行CA、つまりx509ルートCAは、証明書チェーンの検証の基点です。クライアントが持っていなければならないため、サーバーから送信しても意味がありません。標準的な設定では、このようなCAをPEMファイルに含めないようにする必要があります。このオプションを使うと、クライアントには送信せずに、PEMファイル内にこのようなCAを残せます。用途は、'.issuer' ファイルを必要とせずにocsp用の発行者を提供し、'issuers-chain-path' と共有できるようにすることです。これは、中間証明書を持たないすべての証明書に関係します。BoringSSLではocspの処理に発行者が不要で、.issuerを無視するため、効果はありません。少なくともOpenSSL 1.0.2が必要です。

<a id="entry-3-1-stats-calculate-max-counters"></a>

**`stats calculate-max-counters [on|off]`**

```haproxy
stats calculate-max-counters [on|off]
```

統計の最大値カウンターの計算を有効または無効にします。必要なければ、無効にすることで性能が少し向上する可能性があります。デフォルトはonです。

<a id="entry-3-1-stats-maxconn"></a>

**`stats maxconn <connections>`**

```haproxy
stats maxconn <connections>
```

デフォルトでは、統計ソケットの同時接続数は10に制限されています。"stats maxconn" でこの値を変更できます。

<a id="entry-3-1-stats-socket"></a>

**`stats socket [<address:port>|<path>] [param*]`**

```haproxy
stats socket [<address:port>|<path>] [param*]
```

UNIXソケットを `<path>` に、またはTCPv4/v6アドレスを `<address:port>` にバインドします。このソケットへの接続では、各種の統計情報の出力を取得でき、一部の実行時設定を変更するコマンドも発行できます。詳細は、管理ガイドの[9.3節](/ja/docs/haproxy/statistics-and-monitoring/#section-9-3)「Unixソケットコマンド」を参照してください。

"bind" 行でサポートするすべてのパラメーターに対応しています。たとえば、アクセスできるユーザーや、そのアクセス権を制限できます。詳細は、[5.1節](/ja/docs/haproxy/bind-and-server-options/#section-5-1)を参照してください。

<a id="entry-3-1-stats-timeout"></a>

**`stats timeout <timeout, in milliseconds>`**

```haproxy
stats timeout <timeout, in milliseconds>
```

統計ソケットのデフォルトのタイムアウトは10秒です。"stats timeout" でこの値を変更できます。値はミリ秒で指定するか、{ us, ms, s, m, h, d } のいずれかの時間単位を接尾辞として付けなければなりません。

<a id="entry-3-1-stats-file"></a>

**`stats-file <path>`**

```haproxy
stats-file <path>
```

生成したhaproxyのstats-fileへのパスを指定します。haproxyは起動時に、内部カウンターへ値を事前に読み込みます。このstats-fileは、CLIコマンド "dump stats-file" で生成します。詳細は管理マニュアルを参照してください。

<a id="entry-3-1-stress-level"></a>

**`stress-level <level>`**

```haproxy
stress-level <level>
```

haproxyバイナリーにストレスをかける代替コードを有効にします。レベルは0から9までの整数です。デフォルト値の0では、ストレスをかける実行をすべて無効にします。レベル1から9に従って、haproxyバイナリーへのストレスを強めます。正のレベルを使用すると、性能が大幅に低下する場合があります。そのため、デバッグ目的で開発者からの依頼がある場合を除き、決して有効にすべきではありません。

<a id="entry-3-1-strict-limits"></a>

**`strict-limits`**

```haproxy
strict-limits
```

setrlimitが失敗したとき、起動時にプロセスを失敗させます。HAProxyは、計算結果に従って最適なsetrlimitの設定を試みます。失敗すると警告を出力します。このオプションは、これらの制限の設定に失敗した場合に、HAProxyが明示的に失敗することを保証します。デフォルトで有効です。前に "no" キーワードを付けると、強制的に無効にできます。

<a id="entry-3-1-thread-group"></a>

**`thread-group <group> [<thread-range>...]`**

```haproxy
thread-group <group> [<thread-range>...]
```

この設定は、スレッドのサポートを組み込んでビルドした場合にのみ使用できます。スレッドグループ `<group>` を構成するスレッドの一覧を列挙します。スレッド番号とグループ番号は1から始まります。スレッド範囲は、スレッド番号を個別に指定するか、下限と上限をダッシュ '-' で区切って指定します（例: "1-16"）。未割り当てのスレッドは、未割り当てのスレッドグループに自動的に割り当てられます。このディレクティブで定義したスレッドグループには、定義したスレッド以外は決して追加されません。同じグループを複数回定義すると、新しい定義で以前の定義を上書きします。"nbthread" と "thread-groups" も参照してください。

<a id="entry-3-1-thread-groups"></a>

**`thread-groups <number>`**

```haproxy
thread-groups <number>
```

この設定は、スレッドのサポートを組み込んでビルドした場合にのみ使用できます。HAProxyのスレッドを、独立した `<number>` 個のグループに分割します。現在のデフォルト値は1です。スレッドグループを使うと、設定の手間は増えますが、スレッド間の共有を減らして競合を抑えられます。グループごとに最大64スレッドを設定できるため、64を超えるスレッドを使用する唯一の方法でもあります。グループ数の上限はコンパイル時に設定され、デフォルトは16です。"nbthread" も参照してください。

<a id="entry-3-1-thread-hard-limit"></a>

**`thread-hard-limit <number>`**

```haproxy
thread-hard-limit <number>
```

検出された、または設定されたスレッド数に上限を設けます。スレッド数を自動検出するOSで、汎用的かつ移植性のある設定を使いながら、CPU数より少ないスレッド数にしたい場合に特に役立ちます。"nbthread" はスレッド数を強制し、使用可能なCPU数を超えると警告が出て性能が低下します。一方、thread-hard-limitは最大値に上限を設けるだけで、スレッド数をその値以下に自動的に制限し、それより小さい値は増やしません。"nbthread" により大きな値を強制した場合は、thread-hard-limitが優先され、設定の不整合を修正できるように警告を出力します。デフォルトでは制限はありません。"nbthread" も参照してください。

<a id="entry-3-1-uid"></a>

**`uid <number>`**

```haproxy
uid <number>
```

プロセスのユーザーIDを `<number>` に変更します。このユーザーIDは、HAProxy専用、または同種の少数のデーモン専用にすることを推奨します。別のユーザーIDに切り替えるには、HAProxyをスーパーユーザー権限で起動しなければなりません。"gid" と "user" も参照してください。

<a id="entry-3-1-ulimit-n"></a>

**`ulimit-n <number>`**

```haproxy
ulimit-n <number>
```

プロセスごとのファイルディスクリプター数の上限を `<number>` に設定します。デフォルトでは自動計算するため、このオプションは使用しないことを推奨します。単にファイルディスクリプター数を制限するだけなら、代わりに "fd-hard-limit" を使用する方が適切です。

この自動リソース計算には、動的サーバーを含めない点に注意してください。多数の動的サーバーを使用する場合は、この値を手動で指定する必要があるかもしれません。

関連項目: fd-hard-limit、maxconn

unix-bind [ prefix `<prefix>` ] [ mode `<mode>` ] [ user `<user>` ] [ uid `<uid>` ] [ group
`<group>` ] [ gid `<gid>` ]

"bind" 文で宣言するUNIXリスニングソケットに共通の設定を定めます。これらの設定は通常必要ですが、プロセス固有でもあるため、主にUNIXソケットの宣言を簡単にし、誤りの危険を減らすために使用します。`<prefix>` を使うと、すべてのソケットパスをそのディレクトリからの相対パスに強制できます。別のコンポーネントのchrootにアクセスするために必要になることがあります。これらのパスは、HAProxy自身がchrootする前に解決されるため、絶対パスになります。`<mode>`、`<user>`、`<uid>`、`<group>`、`<gid>` は、いずれも "bind" 文の同名の設定と同じ意味です。両方に指定した場合は "bind" 文が優先されます。したがって、"unix-bind" の設定は、プロセス全体のデフォルト設定と見なせます。

<a id="entry-3-1-unsetenv"></a>

**`unsetenv [<name> ...]`**

```haproxy
unsetenv [<name> ...]
```

引数に指定した環境変数を削除します。一部の操作でユーザーの環境から継承されることがある、機密情報を隠すのに役立ちます。存在しなかった変数は警告せずに無視するため、操作後には、指定した変数がどれも残らないことが保証されます。変更は直ちに有効になり、設定ファイルの次の行では、これらの変数を参照できなくなります。"setenv"、"presetenv"、"resetenv" も参照してください。

<a id="entry-3-1-user"></a>

**`user <user name>`**

```haproxy
user <user name>
```

"uid" と同様ですが、/etc/passwdからユーザー名 `<user name>` のUIDを取得して使用します。"uid" と "group" も参照してください。

<a id="entry-3-1-node"></a>

**`node <name>`**

```haproxy
node <name>
```

DNS名と同様に、英字、数字、ハイフン、アンダースコアだけを使用できます。

この文は、複数のプロセスまたはサーバーが同じIPアドレスを共有するHA構成で役立ちます。すべてのノードに異なるノード名を設定すると、どのサーバーがトラフィックを処理しているか、すぐに分かるようになります。

<a id="entry-3-1-wurfl-cache-size"></a>

**`wurfl-cache-size <size>`**

```haproxy
wurfl-cache-size <size>
```

WURFLのユーザーエージェントキャッシュのサイズを設定します。検索を高速にするため、処理済みのユーザーエージェントをLRUキャッシュに保持します。

- "0" : キャッシュを使用しません。
- `<size>` : LRUキャッシュのサイズを要素数で指定します。

このオプションは、HAProxyをUSE_WURFL=1でコンパイルした場合にのみ使用できます。

<a id="entry-3-1-wurfl-data-file"></a>

**`wurfl-data-file <file path>`**

```haproxy
wurfl-data-file <file path>
```

デバイス検出サービスに使用するWURFLデータファイルのパスを指定します。HAProxyがアクセスできるよう、ファイルには適切な権限を設定すべきです。

このオプションは、HAProxyをUSE_WURFL=1でコンパイルした場合にのみ使用できます。

<a id="entry-3-1-wurfl-information-list"></a>

**`wurfl-information-list [<capability>]*`**

```haproxy
wurfl-information-list [<capability>]*
```

挿入するヘッダーで使用する予定の、WURFLの機能、仮想機能、プロパティ名をスペースで区切った一覧です。機能と仮想機能の名前の完全な一覧は、ScientiamobileのWebサイトにあります。

```text
https://www.scientiamobile.com/wurflCapability
```

有効なWURFLプロパティは次のとおりです。

- wurfl_id 一致したデバイスのデバイスIDを格納します。

- wurfl_root_id 一致したデバイスのデバイスルートIDを格納します。

- wurfl_isdevroot 一致したデバイスがルートデバイスかどうかを示します。値は "TRUE" または "FALSE" です。

- wurfl_useragent このWebリクエストで送られてきた元のユーザーエージェントです。

- wurfl_api_version 現在使用中のLibwurfl APIのバージョンを表す文字列を格納します。

- wurfl_info 解析したwurfl.xmlの情報と、その完全なパスを含む文字列です。

- wurfl_last_load_time WURFLを最後に正常に読み込んだ時刻のUNIXタイムスタンプを格納します。

- wurfl_normalized_useragent 正規化したユーザーエージェントです。

このオプションは、HAProxyをUSE_WURFL=1でコンパイルした場合にのみ使用できます。

<a id="entry-3-1-wurfl-information-list-separator"></a>

**`wurfl-information-list-separator <char>`**

```haproxy
wurfl-information-list-separator <char>
```

WURFLの結果を含むレスポンスヘッダーで、値を区切る文字です。指定しない場合は、デフォルトでコンマ (',') を使用します。

このオプションは、HAProxyをUSE_WURFL=1でコンパイルした場合にのみ使用できます。

<a id="entry-3-1-wurfl-patch-file"></a>

**`wurfl-patch-file [<file path>]`**

```haproxy
wurfl-patch-file [<file path>]
```

WURFLパッチファイルのパスの一覧です。パッチは起動時、つまりchrootする前に読み込む点に注意してください。

このオプションは、HAProxyをUSE_WURFL=1でコンパイルした場合にのみ使用できます。

## 3.2. 性能のチューニング {#section-3-2}

<a id="entry-3-2-busy-polling"></a>

**`busy-polling`**

```haproxy
busy-polling
```

状況によっては、特に可変周波数に対応するプロセッサーで低遅延を求める場合や、仮想マシン内で実行する場合、プロセスがポーラーでI/Oを待つたびに、プロセッサーがスリープに戻ったり、長時間ほかのVMに割り当てられたりして、遅延が過度に大きくなることがあります。このオプションは、ポーラーのタイムアウトを常にゼロにすることで、プロセッサーのスリープを防ぎます。プロセッサーが過熱する危険を伴いますが、遅延を大幅に減らせます（30から100マイクロ秒の短縮が観測されています）。スレッドと併用することもできますが、スレッドのバインドが不適切だと激しい競合が生じ、性能が悪化して、"show info" 出力のCPU stolenフィールドが大きな値になります。これによって、設定が不適切なスレッドを判別できます。このオプションを使用するときは、ネットワーク割り込みと同じプロセッサーでプロセスを実行しないことが重要です。同じコアを共有する複数のCPUスレッドでの使用も避けた方がよいでしょう。デフォルトで無効です。有効にした場合も、前に "no" キーワードを付けると強制的に無効にできます。"select" と "poll" ポーラーは、このオプションを無視します。

シームレスなリロードでは、古いプロセスに対してこのオプションを自動的に無効にします。現在の接続の終了を待って複数のプロセスがしばらく残る間に、CPUの競合が過度に発生するのを避けるためです。

<a id="entry-3-2-max-spread-checks"></a>

**`max-spread-checks <delay in milliseconds>`**

```haproxy
max-spread-checks <delay in milliseconds>
```

デフォルトでは、HAProxyは、サーバー群のすべてのサーバーで最も短いヘルスチェック間隔の中に、ヘルスチェックの開始時刻を分散させようとします。同じサーバーで稼働するサービスに、一斉に負荷をかけるのを避けるためです。ただし、チェック間隔が長い場合（10秒以上）、サーバー群の最後のサーバーでテストが始まるまで時間がかかり、問題になることがあります。このパラメーターは、各サーバーのチェック間隔が長くても、最初と最後のチェックの間の遅延に上限を設けます。ただし、サーバーの間隔がそれより短い場合は、その間隔を守ります。

<a id="entry-3-2-maxcompcpuusage"></a>

**`maxcompcpuusage <number>`**

```haproxy
maxcompcpuusage <number>
```

新しいリクエストの圧縮を停止したり、処理中のリクエストの圧縮レベルを下げたりする前に、HAProxyが使用できるCPU使用率の上限を設定します。'maxcomprate' と同様に動作しますが、入力データの帯域幅ではなくCPU使用率を測定します。値は、HAProxyが使用するCPUの割合をパーセントで表します。100を指定すると制限を無効にします。デフォルト値は100です。より低い値を設定すると、圧縮処理によってプロセス全体が遅くなったり、高い遅延が生じたりすることを防げます。

<a id="entry-3-2-maxcomprate"></a>

**`maxcomprate <number>`**

```haproxy
maxcomprate <number>
```

プロセスごとの圧縮への入力速度の上限を、毎秒 `<number>` キロバイトに設定します。各ストリームで上限に達すると、そのストリームの処理中に圧縮レベルを下げます。ストリームの開始時点で上限に達している場合は、そのストリームをまったく圧縮しません。上限に達していない場合は、tune.comp.maxlevelまで圧縮レベルを上げます。ゼロは制限なしを意味し、これがデフォルト値です。

<a id="entry-3-2-maxconn"></a>

**`maxconn <number>`**

```haproxy
maxconn <number>
```

プロセスごとの同時接続数の上限を `<number>` に設定します。コマンドライン引数 "-n" と同等です。コマンドライン引数 "-n" で指定した値は、globalセクションのmaxconnより優先されます。HAProxyプロセスは、コンパイル時変数SYSTEM_MAXCONNを指定してコンパイルすることもでき、その場合は、これをシステムのmaxconnの上限として使用します。このSYSTEM_MAXCONNの制限も、コマンドライン引数 "-n" で実行時に回避できます。maxconnに達すると、プロキシは接続の受け付けを停止します。プロセスのファイルディスクリプター数のソフトリミット（"ulimit -n" コマンドで取得できます）は、指定したmaxconnに応じて自動調整します。"ulimit-n" も参照してください。注意： 一部のプラットフォームでは、"select" ポーラーは1024を超えるファイルディスクリプターを確実に扱うことができません。プラットフォームがselectだけに対応し、起動時に "select FAILED" と表示する場合は、動作するまでmaxconnを下げる必要があります（通常は500を少し下回る値です）。maxconnを設定しない場合は、"ulimit -nH" コマンドが示す現在のファイルディスクリプター数の制限を基に、自動計算します（ハードリミットとソフトリミットの大きい方を使用します）。その自動計算値は、"fd-hard-limit" と、コマンドラインオプション "-m" で強制した場合のメモリー制限によって、さらに小さくなることがあります。自動計算値は、バッファーサイズ、圧縮用に割り当てるメモリー、SSLキャッシュのサイズ、SSLを使用するかどうか、および関連するmaxsslconn（これも自動計算できます）にも依存します。

関連項目: fd-hard-limit、ulimit-n

<a id="entry-3-2-maxconnrate"></a>

**`maxconnrate <number>`**

```haproxy
maxconnrate <number>
```

プロセスごとの毎秒の接続数の上限を `<number>` に設定します。この制限に達すると、プロキシは接続の受け付けを停止します。各フロントエンドの容量に関係なく、全体の容量を制限できます。ただし、この制限はサービスを保護する手段としてしか使用できません。制限に達した際に、フロントエンド間で必ずしも公平に分配されるとは限らないため、各フロントエンドにも、想定する割り当てに近い値の制限を設けるとよいでしょう。また、tune.maxacceptを下げると公平性が改善する場合があります。

<a id="entry-3-2-maxpipes"></a>

**`maxpipes <number>`**

```haproxy
maxpipes <number>
```

プロセスごとのパイプ数の上限を `<number>` に設定します。現在、パイプを使用するのは、カーネルによるTCPスプライシングだけです。パイプには2つのファイルディスクリプターが含まれるため、"ulimit-n" の値も、それに応じて増えます。デフォルト値はmaxconn/4で、ほとんどの高負荷用途でも十分な値と考えられます。スプライス処理はパイプを動的に割り当て、解放し、通常のコピーにフォールバックできるため、この値が低すぎても、影響は性能に限られます。

<a id="entry-3-2-maxsessrate"></a>

**`maxsessrate <number>`**

```haproxy
maxsessrate <number>
```

プロセスごとの毎秒のセッション数の上限を `<number>` に設定します。この制限に達すると、プロキシは接続の受け付けを停止します。各フロントエンドの容量に関係なく、全体の容量を制限できます。ただし、この制限はサービスを保護する手段としてしか使用できません。制限に達した際に、フロントエンド間で必ずしも公平に分配されるとは限らないため、各フロントエンドにも、想定する割り当てに近い値の制限を設けるとよいでしょう。また、tune.maxacceptを下げると公平性が改善する場合があります。

<a id="entry-3-2-maxsslconn"></a>

**`maxsslconn <number>`**

```haproxy
maxsslconn <number>
```

プロセスごとの同時SSL接続数の上限を `<number>` に設定します。デフォルトではSSL固有の制限はなく、すべての接続にglobalのmaxconn設定を適用します。この制限を設定すると、opensslがメモリーを使いすぎて、mallocがNULLを返したときにクラッシュするのを防げます（残念ながら、opensslはこのような状態を確実には確認しません）。制限は受信接続と送信接続の両方に適用されるため、復号した後に暗号化する1つの接続は、2つのSSL接続として数える点に注意してください。この値を設定せず、メモリー制限を強制している場合は、メモリー制限、maxconn、バッファーサイズ、圧縮用に割り当てるメモリー、SSLキャッシュのサイズ、およびフロントエンド、バックエンド、または両方でのSSLの使用状況を基に、自動計算します。メモリー制限があり、maxconnもmaxsslconnも指定しない場合、HAProxyは、100%の接続を安全にSSLで処理できるように、これらの値を自動調整します。その際は、SSLを有効にしている側（フロントエンド、バックエンド、両方）を考慮します。

<a id="entry-3-2-maxsslrate"></a>

**`maxsslrate <number>`**

```haproxy
maxsslrate <number>
```

プロセスごとの毎秒のSSLセッション数の上限を `<number>` に設定します。この制限に達すると、SSLリスナーは接続の受け付けを停止します。各フロントエンドの容量に関係なく、SSLによる全体のCPU使用量を制限できます。ただし、この制限はサービスを保護する手段としてしか使用できません。制限に達した際に、フロントエンド間で必ずしも公平に分配されるとは限らないため、各フロントエンドにも、想定する割り当てに近い値の制限を設けるとよいでしょう。また、セッションを数えるのは、SSLスタックに入った後ではなく、入る前です。そのため、不正なハンドシェイクからもスタックを保護できます。tune.maxacceptを下げると、公平性が改善する場合もあります。

<a id="entry-3-2-maxzlibmem"></a>

**`maxzlibmem <number>`**

```haproxy
maxzlibmem <number>
```

zlibが使用できるRAMの上限を、プロセスごとにメガバイト単位で設定します。上限に達すると、RAMが利用可能になるまで、新しいストリームを圧縮しません。0を指定すると制限はありません。デフォルト値は0です。UNIXソケットで "show info" を実行すると、"MaxZlibMemUsage" 行にこの値をバイト単位で表示します。zlibが使用しているメモリーは、"ZlibMemUsage" にバイト単位で表示します。

<a id="entry-3-2-no-memory-trimming"></a>

**`no-memory-trimming`**

```haproxy
no-memory-trimming
```

大量のメモリーの回収を試みるいくつかのタイミング（メモリー不足時やリロード時）で、メモリートリミング ("malloc_trim") を無効にします。メモリーのトリミングは、システムのアロケーターに、未使用領域をすべて走査して解放させます。古いプロセスがそのメモリーを大きく使用する可能性は低いため、新しいプロセスに利用可能なメモリーを多く残す、好ましい動作と一般には考えられます。しかし、数万から数十万の同時接続を扱うシステムでは、メモリーの断片化が激しく、この解放操作に極めて長い時間がかかることがあります。その間、プロセスを通るトラフィックはすべて止まり、新しい接続も受け付けなくなり、一部のヘルスチェックも失敗する可能性があります。さらに、ウォッチドッグが作動して応答しないプロセスを強制終了し、巨大なコアダンプを残すこともあります。このような事象が発生する場合は、このオプションでトリミングを無効にして、新しいプロセスのためにメモリーを解放しようとする動作を止めることを推奨します。高度なメモリーアロケーターでは、通常この問題は発生しません。

<a id="entry-3-2-noepoll"></a>

**`noepoll`**

```haproxy
noepoll
```

Linuxで "epoll" イベントポーリングシステムの使用を無効にします。コマンドライン引数 "-de" と同等です。次に使用するポーリングシステムは、通常 "poll" です。"nopoll" も参照してください。

<a id="entry-3-2-noevports"></a>

**`noevports`**

```haproxy
noevports
```

Solaris 10以降から派生したSunOSシステムで、event portsイベントポーリングシステムの使用を無効にします。コマンドライン引数 "-dv" と同等です。次に使用するポーリングシステムは、通常 "poll" です。"nopoll" も参照してください。

<a id="entry-3-2-nogetaddrinfo"></a>

**`nogetaddrinfo`**

```haproxy
nogetaddrinfo
```

名前解決でのgetaddrinfo(3)の使用を無効にします。コマンドライン引数 "-dG" と同等です。非推奨のgethostbyname(3)を使用します。

<a id="entry-3-2-nokqueue"></a>

**`nokqueue`**

```haproxy
nokqueue
```

BSDで "kqueue" イベントポーリングシステムの使用を無効にします。コマンドライン引数 "-dk" と同等です。次に使用するポーリングシステムは、通常 "poll" です。"nopoll" も参照してください。

<a id="entry-3-2-noktls"></a>

**`noktls`**

```haproxy
noktls
```

ktlsの使用を無効にします。コマンドライン引数 "-dT" と同等です。

<a id="entry-3-2-nopoll"></a>

**`nopoll`**

```haproxy
nopoll
```

"poll" イベントポーリングシステムの使用を無効にします。コマンドライン引数 "-dp" と同等です。次に使用するポーリングシステムは "select" です。"poll" は、HAProxyがサポートするすべてのプラットフォームで使用できるため、無効にする必要はないはずです。"nokqueue"、"noepoll"、"noevports" も参照してください。

<a id="entry-3-2-noreuseport"></a>

**`noreuseport`**

```haproxy
noreuseport
```

SO_REUSEPORTの使用を無効にします。socket(7)を参照してください。コマンドライン引数 "-dR" と同等です。

<a id="entry-3-2-nosplice"></a>

**`nosplice`**

```haproxy
nosplice
```

Linuxで、ソケット間のカーネルTCPスプライシングの使用を無効にします。コマンドライン引数 "-dS" と同等です。データは、従来の、より移植性の高いrecv/send呼び出しでコピーするようになります。カーネルTCPスプライシングは、カーネル2.6の中でもごく新しい一部の版に限られます。2.6.25から2.6.28までのほとんどの版には不具合があり、破損したデータを転送するため、使用してはいけません。このオプションを使うと、疑わしい場合にカーネルスプライシングを全体で簡単に無効にできます。"option splice-auto"、"option splice-request"、"option splice-response" も参照してください。

<a id="entry-3-2-profiling-memory"></a>

**`profiling.memory { on | off }`**

```haproxy
profiling.memory { on | off }
```

関数ごとのメモリープロファイリングを有効 ('on') または無効 ('off') にします。ライブラリを含むプロセス内のあらゆる場所でのmalloc/calloc/realloc/free呼び出しの使用統計を保持し、CLIの "show profiling" コマンドで報告します。主に、プールでは説明できない異常なメモリー使用量が見られ、追加の情報が必要なときに使用します。性能への影響は通常1%程度で、スレッドが非常に多いマシンでは、もう少し大きくなる可能性があります。そのため、通常は本番環境でも使用できます。CLIの "set profiling memory" コマンドで、実行時にも同じ操作ができます。管理マニュアルを参照してください。

<a id="entry-3-2-profiling-tasks"></a>

**`profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*`**

```haproxy
profiling.tasks { auto | on | off | lock | no-lock | memory | no-memory }*
```

タスクごとのCPUプロファイリングを有効 ('on') または無効 ('off') にします。'auto' を指定すると、アクティビティの "avg_loop_us" フィールドで報告される平均遅延が1000マイクロ秒以上になったスレッドで、自動的にプロファイリングを有効にします。遅延が990マイクロ秒未満に戻ると、自動的に無効にします（この値は直近1024ループの平均なので、急には変化せず、短いスパイクを大きく平滑化する傾向があります）。過負荷のシステム、コンテナー、仮想マシンや、システムがスワップするときにも、時折自動的に作動することがあります（ロードバランサーでは、スワップは絶対に発生してはいけません）。

タスクのプロファイリングが有効な場合、HAProxyは、各タスクがロックを保持する時間やロックを待つ時間、さらにプールキャッシュにヒットしない場合に、メモリー割り当てが成功するまで待つ時間も収集できます。遅延の原因の一部を理解するのに役立つことがあります。そのためには、追加のキーワード "lock"（ロック時間の収集を有効化）、"no-lock"（無効化）、"memory"（メモリー割り当て時間の収集を有効化）、"no-memory"（無効化）を指定できます。高負荷のシステムでは、無視できないCPUへの影響（3-10%）があるため、デフォルトでは有効にしません。この負荷が発生するのは、プロファイリングが実際に動作している間だけです。したがって、"auto" モードでは、HAProxyがプロファイリングを有効にすると判断したときだけ発生します。

タスクごとのCPUプロファイリングは、どこに時間を費やし、どのリクエストがどのほかのリクエストにどのような影響を与えるかを報告するのに、とても便利です。有効にしても、全体の性能への影響は通常1%未満です。そのため、問題を検出したときだけ動作するよう、デフォルトの 'auto' のままにすることを推奨します。この機能には、クロック識別子CLOCK_MONOTONICとCLOCK_THREAD_CPUTIME_IDを指定したclock_gettime(2)システムコールに対応するシステムが必要です。対応していなければ、報告する時間はゼロになります。このオプションは、CLIの "set profiling" で実行時に変更できます。

<a id="entry-3-2-spread-checks"></a>

**`spread-checks <0..50, in percent>`**

```haproxy
spread-checks <0..50, in percent>
```

たとえば、多数の論理サーバーが同じ物理サーバー上にある場合など、エージェントチェックやヘルスチェックを厳密な間隔で送信するのを避けたいことがあります。このパラメーターを使うと、チェック間隔に0から+/- 50%のランダムな変動を加えられます。2から5までの値で、よい結果が得られるようです。デフォルト値は0のままです。

<a id="entry-3-2-ssl-engine"></a>

**`ssl-engine <name> [algo <comma-separated list of algorithms>]`**

```haproxy
ssl-engine <name> [algo <comma-separated list of algorithms>]
```

OpenSSLエンジンを `<name>` に設定します。`<name>` に指定できる値の一覧は、"openssl engine" コマンドで取得できます。この文は複数回使用でき、その場合は複数の暗号エンジンを有効にします。サポートしていないエンジンを参照すると、HAProxyは起動できません。最近のプロセッサーでは、多くのエンジンが、純粋なソフトウェア処理よりもHTTPSの性能を低下させる点に注意してください。オプションのコマンド "algo" は、OpenSSL関数ENGINE_set_default_string()を使って、ENGINEが提供するデフォルトのアルゴリズムを設定します。"ALL" を指定すると、すべての暗号処理にそのエンジンを使用します。algoの一覧を指定しない場合も、"ALL" を使用します。異なるアルゴリズムをコンマで区切って指定でき、RSA、DSA、DH、EC、RAND、CIPHERS、DIGESTS、PKEY、PKEY_CRYPTO、PKEY_ASN1などを含められます。これは、opensslの設定ファイルと同じ形式です: <https://www.openssl.org/docs/man1.0.2/apps/config.html>

HAProxyバージョン2.6では、デフォルトのビルドでエンジンのサポートを無効にしました。このオプションは、対応するサポートを組み込んでHAProxyをビルドした場合にのみ使用できます。ssl-engineが必要な場合は、USE_ENGINE=1フラグを指定してHAProxyを再ビルドできます。

<a id="entry-3-2-ssl-mode-async"></a>

**`ssl-mode-async`**

```haproxy
ssl-mode-async
```

SSLコンテキストにSSL_MODE_ASYNCモードを追加します。非同期処理に対応するSSLエンジンを使用する場合、非同期TLS I/O操作を有効にします。現在の実装は、最大32エンジンをサポートします。OpenSSLのASYNC APIは、読み取り/書き込みバッファーの移動をサポートせず、HAProxyのバッファー管理と互換性がありません。そのため、読み取り/書き込み操作では非同期モードを無効にします（有効になるのは、初回と再ネゴシエーションのハンドシェイク中だけです）。

<a id="entry-3-2-tune-applet-zero-copy-forwarding"></a>

**`tune.applet.zero-copy-forwarding { on | off }`**

```haproxy
tune.applet.zero-copy-forwarding { on | off }
```

アプレットで、データのゼロコピー転送を有効 ('on') または無効 ('off') にします。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding。

<a id="entry-3-2-tune-buffers-limit"></a>

**`tune.buffers.limit <number>`**

```haproxy
tune.buffers.limit <number>
```

プロセスごとに割り当てられるバッファー数に、厳密な上限を設定します。デフォルト値はゼロで、無制限を意味します。緊急時のために予約するバッファー数を満たすよう、制限は自動的に再調整されるため、ユーザーが複雑な計算をする必要はありません。この値を強制すると、適切な動作を維持しながら、プロセスが使用するメモリー量を制限するのに特に役立ちます。上限に達すると、バッファーを要求したタスクは、別のバッファーが解放されるまで待ちます。制限が妥当な範囲であれば、通常この待ち時間は非常に短く、体感できません。しかし、過去からのいくつかの制約によって、バージョンを重ねる中でこの仕組みは弱まりました。バッファー不足が続く一部の状況では、タイムアウトするまでタスクが停止することが分かっているため、絶対に必要な場合を除き、使用を避けた方が安全です。

<a id="entry-3-2-tune-buffers-reserve"></a>

**`tune.buffers.reserve <number>`**

```haproxy
tune.buffers.reserve <number>
```

メモリー不足で割り当てに失敗する状況でのみ使用するため、事前に割り当てて予約するバッファー数を、スレッドごとに設定します。最小値は0で、デフォルトは4です。コア開発者が非常に具体的な理由で変更を提案する場合を除き、ユーザーがこの値を変更する理由はありません。

<a id="entry-3-2-tune-bufsize"></a>

**`tune.bufsize <size>`**

```haproxy
tune.bufsize <size>
```

バッファーのサイズをバイト単位で設定します。小さな値にすると、同じRAM容量でより多くのストリームを共存させられます。大きな値にすると、非常に大きなCookieを使う一部のアプリケーションが動作できるようになります。デフォルト値は16384で、ビルド時に変更できます。この値は、デフォルトから変更しないことを強く推奨します。値が非常に小さいと、統計など一部のサービスが動作しなくなり、デフォルトより大きいと、メモリー使用量が増え、システムがメモリー不足に陥る可能性があります。少なくとも、この値を増やした倍率に応じて、globalのmaxconnを同じ倍率で減らすべきです。また、HTTP/2を使用するには、この値が16384以上でなければなりません。さらに、256 MB（268435456 バイト）未満でなければなりません。HTTPリクエストのヘッダーブロックが (tune.bufsize - tune.maxrewrite) より大きい場合、HAProxyはHTTP 400 (Bad Request) エラーを返します。同様に、HTTPレスポンスのヘッダーブロックがこのサイズより大きい場合は、HTTP 502 (Bad Gateway) を返します。このパラメーターで指定した値は、32ビットマシンでは8の倍数、64ビットマシンでは16の倍数へ、自動的に切り上げる点に注意してください。関連項目: tune.bufsize.large、tune.bufsize.small。

<a id="entry-3-2-tune-bufsize-large"></a>

**`tune.bufsize.large <size>`**

```haproxy
tune.bufsize.large <size>
```

大きなバッファーのサイズをバイト単位で設定します。デフォルトでは、大きなバッファーのサポートは無効で、この値を設定して明示的に有効にしなければなりません。

これらのバッファーは、通常のバッファーサイズを変更せずに、より多くのデータをバッファーに保持する必要がある、特定の状況向けに設計されています。大きなバッファーが暗黙的に使用されることはありません。関連項目: tune.bufsize。

大きなバッファーを設定すると、起動時にスレッドごとに、内部処理用の特別な大きなバッファーを3つ割り当てる点に注意してください。

<a id="entry-3-2-tune-bufsize-small"></a>

**`tune.bufsize.small <size>`**

```haproxy
tune.bufsize.small <size>
```

小さなバッファーのサイズをバイト単位で設定します。デフォルト値は1024です。

これらのバッファーは、メモリー消費が限られ、通常サイズのバッファーを割り当てる必要はなさそうな、特定の状況向けに設計されています。ただし、小さなバッファーでは足りない場合は、自動的に再割り当てし、標準サイズのバッファーに切り替えます。

現時点で自動的に使用するのは、レスポンスヘッダーを送信するHTTP/3プロトコルだけです。それ以外では、"use-small-buffers" オプションで、特定のプロキシに対して小さなバッファーのサポートを有効にできます。関連項目: tune.bufsize。

関連項目: option use-small-buffers

<a id="entry-3-2-tune-cli-max-payload-size"></a>

**`tune.cli.max-payload-size <size>`**

```haproxy
tune.cli.max-payload-size <size>
```

CLIのコマンドに渡すペイロードで、許容するサイズの上限を設定します。

CLIでは、コマンドラインの長さはバッファーサイズに制限されます。つまり、すべてのコマンドとその引数は、処理するためにバッファーに収まらなければなりません。ただし、コマンドラインの最後のコマンドに渡せるペイロードは除きます。このペイロードには、必要に応じて専用の領域を割り当てられ、そのサイズをこのパラメーターで制限します。デフォルト値は128KBです。

ほとんどの用途には十分な値のはずですが、変更する場合は慎重に選ばなければなりません。非常に大きな値は、HAProxyの性能に影響する可能性があります。コマンドによっては、巨大なペイロードの処理にかなり時間がかかり、ウォッチドッグを作動させるおそれがあります。

CLIの詳細は、管理マニュアルを参照してください。

<a id="entry-3-2-tune-comp-maxlevel"></a>

**`tune.comp.maxlevel <number>`**

```haproxy
tune.comp.maxlevel <number>
```

圧縮レベルの上限を設定します。圧縮レベルは、圧縮時のCPU使用量に影響します。この値は、圧縮時のCPU使用量に影響します。圧縮を使う各ストリームは、この値で圧縮アルゴリズムを初期化します。デフォルト値は1です。

<a id="entry-3-2-tune-defaults-purge"></a>

**`tune.defaults.purge`**

```haproxy
tune.defaults.purge
```

動的バックエンドをサポートするため、現在は、名前付きのdefaultsセクションをすべて解析後もメモリーに保持します。実行時に追加するバックエンドは、名前付きのdefaultsを基に設定しなければならないため、これが必要です。

defaultsのインスタンス数が多い場合、かなりのメモリーを消費する可能性があります。このような場合で、動的バックエンドが不要なら、このオプションを使用して、解析後にdefaultsセクションを強制的に削除できます。ただし、参照元のプロキシがコピーできない設定を含む、参照されているdefaultsセクションは、引き続き保持しなければなりません。たとえば、defaultsセクションでTCP/HTTPルールやtcpcheckのルールセットを定義する場合が該当します。

<a id="entry-3-2-tune-disable-fast-forward"></a>

**`tune.disable-fast-forward`**

```haproxy
tune.disable-fast-forward
```

データの高速転送を無効にします。高速転送は、ストリームを起こさずに、一方から他方へ直接データを渡すことで転送を最適化する仕組みです。このディレクティブで、その最適化を無効にできます。カーネルTCPスプライシングとゼロコピー転送もすべて無効にする点に注意してください。このコマンドは通常の使用を意図したものではなく、一般には、複雑なデバッグ作業で開発者が提案する場合にだけ使用します。

<a id="entry-3-2-tune-disable-zero-copy-forwarding"></a>

**`tune.disable-zero-copy-forwarding`**

```haproxy
tune.disable-zero-copy-forwarding
```

データのゼロコピー転送を全体で無効にします。ゼロコピー転送は、チャネルのバッファーを使用しないことで、データの高速転送を最適化する仕組みです。このディレクティブで、その最適化を無効にできます。カーネルTCPスプライシングもすべて無効にする点に注意してください。

関連項目: tune.pt.zero-copy-forwarding、tune.applet.zero-copy-forwarding、tune.h1.zero-copy-fwd-recv、tune.h1.zero-copy-fwd-send、tune.h2.zero-copy-fwd-send、tune.quic.zero-copy-fwd-send

<a id="entry-3-2-tune-epoll-mask-events"></a>

**`tune.epoll.mask-events <event[,...]>`**

```haproxy
tune.epoll.mask-events <event[,...]>
```

HAProxyの歴史の中で、Linuxカーネルのepollの仕組みの不具合による、複雑な問題がいくつか発生しました。通常は非常にまれで、報告者の環境以外では再現せず、epollを無効にしてpollへ切り替えることでしか回避できない場合があります。これは、高性能を求める環境では満足できる方法ではありません。問題は毎回、ごく特定の、まれなイベントの種類にだけ影響するため、それらをマスクできれば、より受け入れやすい回避策になる可能性があります。このオプションは、一部のまれなイベントを警告せずに無視し、入力イベント（種類を特定しない着信イベントを通知するもの）に置き換えることで、それを可能にします。その結果、一部の場所で高速なエラー処理経路を避け、通常の経路だけを使用します。カーネルの不具合を診断または回避するために専門家から指示された場合を除き、決して使用すべきではありません。

このオプションは、マスクするイベントを表す単語をコンマで区切った一覧を、1つの引数として受け取ります。現在サポートするイベントは次のとおりです: - "err": EPOLLERRイベントをマスクします - "hup": EPOLLHUPイベントをマスクします - "rdhup": EPOLLRDHUPイベントをマスクします

例:

```shell
# mask all non-traffic epoll events:
tune.epoll.mask-events err,hup,rdhup
```

<a id="entry-3-2-tune-events-max-events-at-once"></a>

**`tune.events.max-events-at-once <number>`**

```haproxy
tune.events.max-events-at-once <number>
```

非同期タスクハンドラー（event_hdl API）が、一度に処理できるイベント数を設定します。`<number>` は1から10000までにすべきです。値が大きいと、タスクが中断せずに重い処理を行い、スレッドの競合を引き起こす可能性があります。一方、値が小さいと、実行のたびに十分な数のイベントを消費できず、イベントの生成側に追いつけないため、タスクの再スケジュールが繰り返される可能性があります。デフォルト値は、ビルド時に強制できます。そうしなければ、100になります。

<a id="entry-3-2-tune-fail-alloc"></a>

**`tune.fail-alloc`**

```haproxy
tune.fail-alloc
```

DEBUG_FAIL_ALLOCを指定してコンパイルした場合、または "-dMfail" を指定して起動した場合に、メモリー割り当ての試行が失敗する確率をパーセントで指定します。0（失敗しない）から100（成功しない）まででなければなりません。デバッグや、メモリー割り当ての失敗を適切に処理できることの確認に役立ちます。指定しなければ、比率は0です。ただし、コマンドラインオプション "-dMfail" は、失敗率を自動的に1%にするため、テストのために設定を変更する必要はありません。

<a id="entry-3-2-tune-fd-edge-triggered"></a>

**`tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]`**

```haproxy
tune.fd.edge-triggered { on | off }  [ EXPERIMENTAL ]
```

対応するFDで、エッジトリガー方式のポーリングを有効 ('on') または無効 ('off') にします。現在サポートするのはepollだけです。epoll_ctl()の呼び出し数を大幅に減らし、状況によっては性能を少し改善する場合があります。まだ実験的な機能で、不具合が残っていると接続が停止するおそれがあり、デフォルトでは無効です。

<a id="entry-3-2-tune-glitches-kill-cpu-usage"></a>

**`tune.glitches.kill.cpu-usage <number>`**

```haproxy
tune.glitches.kill.cpu-usage <number>
```

不具合が多すぎる接続を強制終了する、CPU使用率の下限を0から100までで設定します。対象は、glitches-thresholdの制限に達した接続です。非常に長く続く接続が、性能に影響を与えずに不正な動作をすることが多い環境では、悪影響がない間はその動作にかかわらず接続を維持し、CPUが忙しくなってから強制終了したい場合があります。このパラメーターは、不具合数のしきい値に達した接続を、CPU使用率が指定した値以上なら積極的に強制終了し、それ未満なら決して強制終了しないように指定します。CPU使用率はスレッドごとに測定するため、不正に動作する接続が1つだけでも強制終了される場合があります。デフォルトはゼロで、glitches-thresholdに達した接続は自動的に強制終了されます。目安として、通常観測するCPU使用率の2倍、または通常のCPU使用率にアイドル分の半分を加えた値を設定します（たとえば、通常のCPU使用率が60%なら、80を設定することが考えられます）。tune.h2.fe.glitches-threshold、tune.quic.fe.sec.glitches-threshold、tune.h1.fe.glitches-thresholdのいずれも設定していなければ、このパラメーターは効果がありません。globalの "tune.h2.fe.glitches-threshold"、"tune.h1.fe.glitches-threshold"、"tune.quic.fe.sec.glitches-threshold" も参照してください。

<a id="entry-3-2-tune-h1-be-glitches-threshold"></a>

**`tune.h1.be.glitches-threshold <number>`**

```haproxy
tune.h1.be.glitches-threshold <number>
```

HTTP/1バックエンド接続の不具合数のしきい値を設定し、しきい値に達した後は接続を自動的に強制終了します。不正に動作する接続に対して、明示的なルールを書かずに自動的に強制終了できます。デフォルト値はゼロで、しきい値を設定しないことを意味し、どのイベントも接続の切断を引き起こしません。典型的なイベントには、形式が不正でも "accept-unsafe-violations-in-http-response" によって受け入れたヘッダーがあります。ゼロ以外を指定するなら、多少の不具合があるサーバーに影響を与えずに効果を得られるよう、数百または数千程度にすべきでしょう。"tune.glitches.kill.cpu-usage" を使い、CPU使用率が一定の水準を超えたときだけ接続を強制終了することもできます。設定したしきい値の75%で、接続をクローズモードに切り替え、該当する場合は"Connection: close"を通知し、穏やかな切断を試みる点に注意してください。これによって、多少の不具合がある接続は、進行中の転送を中断する危険を冒さずに、しばらくすると使用されなくなります。

関連項目: tune.h1.fe.glitches-threshold、bc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-fe-glitches-threshold"></a>

**`tune.h1.fe.glitches-threshold <number>`**

```haproxy
tune.h1.fe.glitches-threshold <number>
```

HTTP/1フロントエンド接続の不具合数のしきい値を設定し、しきい値に達した後は接続を自動的に強制終了します。不正に動作する接続に対して、明示的なルールを書かずに自動的に強制終了できます。デフォルト値はゼロで、しきい値を設定しないことを意味し、どのイベントも接続の切断を引き起こしません。典型的なイベントには、形式が不正でも "accept-unsafe-violations-in-http-request" によって受け入れたヘッダーがあります。ゼロ以外を指定するなら、多少の不具合があるクライアントに影響を与えずに効果を得られるよう、数百または数千程度にすべきでしょう。"tune.glitches.kill.cpu-usage" を使い、CPU使用率が一定の水準を超えたときだけ接続を強制終了することもできます。設定したしきい値の75%で、接続をクローズモードに切り替え、該当する場合は"Connection: close"を通知し、穏やかな切断を試みる点に注意してください。これによって、仕様に多少違反するクライアントも、新しい接続を確立して影響なく動作を続ける機会を得られます。進行中の転送を中断する危険がある、強制的な切断を引き起こさずに済みます。

関連項目: tune.h1.be.glitches-threshold、fc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h1-zero-copy-fwd-recv"></a>

**`tune.h1.zero-copy-fwd-recv { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-recv { on | off }
```

H1マルチプレクサーで、データのゼロコピー受信を有効 ('on') または無効 ('off') にします。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding、tune.h1.zero-copy-fwd-send

<a id="entry-3-2-tune-h1-zero-copy-fwd-send"></a>

**`tune.h1.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h1.zero-copy-fwd-send { on | off }
```

H1マルチプレクサーで、データのゼロコピー送信を有効 ('on') または無効 ('off') にします。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding、tune.h1.zero-copy-fwd-recv

<a id="entry-3-2-tune-h2-be-glitches-threshold"></a>

**`tune.h2.be.glitches-threshold <number>`**

```haproxy
tune.h2.be.glitches-threshold <number>
```

バックエンド接続の不具合数のしきい値を設定し、そこに達した接続を自動的に強制終了します。不正に動作する接続に対して、明示的なルールを書かずに自動的に強制終了できます。デフォルト値はゼロで、しきい値を設定しないことを意味し、どのイベントも接続の切断を引き起こしません。一部のH2サーバーは、長く続く接続で時折、少数の不具合を起こす場合があります。そのため、ゼロ以外を指定するなら、多少の不具合があるサーバーに影響を与えずに効果を得られるよう、数百または数千程度にすべきでしょう。"tune.glitches.kill.cpu-usage" を使い、CPU使用率が一定の水準を超えたときだけ接続を強制終了することもできます。設定したしきい値の75%で、将来のストリームに対するGOAWAYを通知し、穏やかな切断を試みる点に注意してください。これによって、多少の不具合がある接続は、進行中の転送を中断する危険を冒さずに、しばらくすると使用されなくなります。

関連項目: tune.h2.fe.glitches-threshold、bc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-be-initial-window-size"></a>

**`tune.h2.be.initial-window-size <number>`**

```haproxy
tune.h2.be.initial-window-size <number>
```

送信接続のHTTP/2初期ウィンドウサイズを設定します。これは、サーバーがHAProxyからの確認応答を待たずに応答できるバイト数です。この設定は、ヘッダーには影響せず、ペイロードの内容にだけ影響します。指定しない場合は、tune.h2.initial-window-sizeで設定した共通のデフォルト値を適用します。この値を少し増やすと、クライアント間で不公平が生じる代わりに、ダウンロードを高速化したり、サーバーのCPU使用量を減らしたりできる場合があります。不公平を生じさせないtune.h2.be.rxbufを、代わりに使用する方が適切です。この設定は、リソース使用量には影響しません。

関連項目: tune.h2.initial-window-size。

<a id="entry-3-2-tune-h2-be-max-concurrent-streams"></a>

**`tune.h2.be.max-concurrent-streams <number>`**

```haproxy
tune.h2.be.max-concurrent-streams <number>
```

送信接続ごとのHTTP/2同時ストリーム数の上限（サーバーへの1つの接続で、応答待ちのリクエスト数）を設定します。指定しない場合は、tune.h2.max-concurrent-streamsで設定したデフォルトを適用します。デフォルトの100より小さくすると、サーバーに対して維持する確立済み接続は増えますが、サイトの応答性が改善する可能性があります。"http-reuse" が "always" の場合は、同じ接続に異なるクライアントを混在させすぎないよう、この値を減らすことを推奨します。あるクライアントがほかより遅いと、「先頭ブロッキング」と呼ばれる仕組みが、その接続を共有する全クライアントのダウンロード速度に連鎖的な影響を及ぼしやすいためです（この場合、tune.h2.be.initial-window-sizeを低く保ってください）。この値を増やさないことを強く推奨します。低い値（通常は1..5）で動作させるのが最適な場合もあります。

<a id="entry-3-2-tune-h2-be-max-frames-at-once"></a>

**`tune.h2.be.max-frames-at-once <number>`**

```haproxy
tune.h2.be.max-frames-at-once <number>
```

バックエンド接続で一度に処理する、HTTP/2受信フレーム数の上限を設定します。非常に大きなバッファーを扱う場合は、小さな値（数十から数百）にすると、遅延を低く保ち、複数の接続間の公平性を改善するのに役立ちます。デフォルト値はゼロで、制限を設けないことを意味します。

<a id="entry-3-2-tune-h2-be-rxbuf"></a>

**`tune.h2.be.rxbuf <size>`**

```haproxy
tune.h2.be.rxbuf <size>
```

送信接続のHTTP/2受信バッファーサイズを、バイト単位で設定します。サイズはtune.bufsizeの倍数へ切り上げ、データをアップロードするすべてのストリームで共有します（HEADERSフレームとDATAフレームの両方が対象です）。どの場合も、各ストリームには必ず1つのバッファーを与え、未使用バッファーの7/8を、ペイロードをダウンロードするストリーム間で共有します。これによって、アップロード性能を大幅に改善し、http-reuseが "always" のとき、複数のクライアントで共有するバックエンド接続の先頭ブロッキング (HoL) を回避できます。通知するストリームごとのウィンドウは、空き領域を反映して自動調整するため、実際にはtune.h2.be.initial-window-sizeを変更する必要はないはずです。すべてのストリームを処理するのに必要なサイズより小さい値を設定した場合は、その最小サイズを使用します。デフォルト値は約1600kです（各16kBのバッファーを持つ100ストリーム）。

関連項目: tune.h2.be.initial-window-size、tune.h2.fe.rxbuf、http-reuse。

<a id="entry-3-2-tune-h2-fe-glitches-threshold"></a>

**`tune.h2.fe.glitches-threshold <number>`**

```haproxy
tune.h2.fe.glitches-threshold <number>
```

フロントエンド接続の不具合数のしきい値を設定し、そこに達した接続を自動的に強制終了します。不正に動作する接続に対して、明示的なルールを書かずに自動的に強制終了できます。デフォルト値はゼロで、しきい値を設定しないことを意味し、どのイベントも接続の切断を引き起こしません。一部のH2クライアントは、長く続く接続で時折、少数の不具合を起こす場合があります。そのため、ゼロ以外を指定するなら、多少の不具合があるクライアントに影響を与えずに効果を得られるよう、数百または数千程度にすべきでしょう。"tune.glitches.kill.cpu-usage" を使い、CPU使用率が一定の水準を超えたときだけ接続を強制終了することもできます。設定したしきい値の75%で、将来のストリームに対するGOAWAYを通知し、穏やかな切断を試みる点に注意してください。これによって、仕様に多少違反するクライアントも、新しい接続を確立して影響なく動作を続ける機会を得られます。進行中の転送を中断する危険がある、強制的な切断を引き起こさずに済みます。

関連項目: tune.h2.be.glitches-threshold、fc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-h2-fe-initial-window-size"></a>

**`tune.h2.fe.initial-window-size <number>`**

```haproxy
tune.h2.fe.initial-window-size <number>
```

受信接続のHTTP/2初期ウィンドウサイズを設定します。これは、クライアントがHAProxyからの確認応答を待たずにアップロードできるバイト数です。この設定は、ヘッダーには影響せず、ペイロードの内容（POSTリクエストの本文）にだけ影響します。指定しない場合は、tune.h2.initial-window-sizeで設定した共通のデフォルト値を適用します。この値を増やすと、アップロードを高速化できる場合があります。デフォルト値はtune.bufsize (16384) と等しく、pingの往復時間が100ミリ秒ならストリームごとに少なくとも1.25 Mbps、1ミリ秒なら125 Mbpsの帯域幅を実現できます。リソース使用量には影響しません。大きすぎる値を使用すると、大容量のアップロードと並行してページにアクセスする際に、クライアントの応答性が低下する可能性があります。不公平を生じさせないtune.h2.fe.rxbufを、代わりに使用する方が適切です。

関連項目: tune.h2.initial-window-size。

<a id="entry-3-2-tune-h2-fe-max-concurrent-streams"></a>

**`tune.h2.fe.max-concurrent-streams <number> [args...]`**

```haproxy
tune.h2.fe.max-concurrent-streams <number> [args...]
```

受信接続ごとのHTTP/2同時ストリーム数の上限（クライアントからの1つの接続で、応答待ちのリクエスト数）を設定します。指定しない場合は、tune.h2.max-concurrent-streamsで設定したデフォルトを適用します。デフォルトの100より大きくすると、遅延の大きいネットワークで、小さなオブジェクトが多数ある複雑なサイトのページ読み込み時間が、多少改善する場合があります。一方、クライアントが一度により多くのリソースを割り当てられるため、メモリー使用量が増える可能性もあります。デフォルト値の100は通常適切で、この値は変更しないことを推奨します。同時実行数が多いと、多数のストリームを使う接続を大量に扱う際の処理負荷と遅延にも影響し、サービス拒否攻撃を仕掛けやすくするおそれがあります。このコマンドは、数値の後に次のオプション引数を指定できます。

- rq-load { `<number>` \| auto \| ignore }:

```text
省略可能な引数"rq-load"を使用すると、処理を実行するスレッドのランキューの負荷に応じて、
通知する同時実行数を動的に調整できます。スレッドの負荷が指定されたしきい値未満である限り、
設定されたストリーム数の上限を通知します。スレッドの負荷が設定された上限を超えると、
通知するストリーム数の上限は、超過比率の二乗に比例して引き下げられます。
目標負荷を50から100の範囲に設定すると、高負荷時に一般的に非常に良好な抑制効果が得られます。
明示的な数値を指定する代わりに、"ignore"を指定することもできます。これがデフォルトであり、
通知するストリーム数の上限を抑制する際に、スレッドのランキューの負荷を考慮しないことを意味します。
また、"auto"を指定すると、上限を"tune.runqueue-depth"の値に設定します。
通常は、設定をさらに調整しなくても良好な結果が得られます。
```

- min `<number>`:

```text
rq-loadを使用する場合に、通知する同時実行数の最小値を設定します。
結果として設定された目標より高い負荷になっても、この最小値は維持されます。
これにより、負荷が非常に高いサイトでも良好な応答性を維持できます。
最小値およびデフォルト値は1ですが、5から15の値を設定すると利用者の操作感を改善できます。
```

例:

```text
tune.h2.fe.max-concurrent-streams 100 rq-load auto min 15
```

<a id="entry-3-2-tune-h2-fe-max-frames-at-once"></a>

**`tune.h2.fe.max-frames-at-once <number>`**

```haproxy
tune.h2.fe.max-frames-at-once <number>
```

フロントエンド接続で一度に処理する、HTTP/2受信フレーム数の上限を設定します。非常に大きなバッファーを扱う場合は、小さな値（数十から数百）にすると、遅延を低く保ち、複数の接続間の公平性を改善するのに役立ちます。デフォルト値はゼロで、制限を設けないことを意味します。

<a id="entry-3-2-tune-h2-fe-max-rst-at-once"></a>

**`tune.h2.fe.max-rst-at-once <number>`**

```haproxy
tune.h2.fe.max-rst-at-once <number>
```

フロントエンド接続で一度に処理する、HTTP/2受信RST_STREAM数の上限を設定します。指定した数のRST_STREAMフレームを受信すると、接続ハンドラーを優先度の低いキューに移し、ほかのすべてのタスクの後に処理します。非常に小さな値（1または数個）にすると、RST_STREAMの大量送信による影響を大幅に減らすのに役立ちます。ユーザーがブラウザーの停止ボタンをクリックしたときにもRST_STREAMは発生しますが、キューに入れ直すことで増える数ミリ秒の遅延は、通常体感できません。一方、この処理は、大量送信による負荷を大幅に減らすのに通常有効です。デフォルト値はゼロで、制限を設けないことを意味します。

<a id="entry-3-2-tune-h2-fe-max-total-streams"></a>

**`tune.h2.fe.max-total-streams <number>`**

```haproxy
tune.h2.fe.max-total-streams <number>
```

受信接続ごとに処理する、HTTP/2ストリームの総数の上限を設定します。上限に達すると、HAProxyは穏やかな切断のためのGOAWAYフレームを送信し、保留中のすべてのストリームが閉じた後に接続を閉じることをクライアントに通知します。実際には、クライアントはこれを受信すると、できるだけ早く接続を閉じ、次のリクエスト用に新しい接続を確立する傾向があります。クライアントが非常に長く接続し続け、サーバー群の中で偏りを生じさせる場合などに、これが有用で望ましいことがあります。たとえば、非常に動的な環境では、負荷の増加に対応して新しいロードバランサーを随時作成し、負荷が下がったら、確立済みの接続を切らずに停止したい場合があります。ここで上限を設定すると、接続の寿命が制限されて頻繁に更新され、その一部は別のノードに確立される可能性があるため、既存のリソースが速やかに解放されます。

この上限と、前述の "tune.h2.fe.max-concurrent-streams" には、暗黙の関係があることを理解することが重要です。HAProxyは、クライアントとフロントエンドの間ですでに送信中になっている可能性がある、保留中のストリームを常に受け入れて処理します。そのため、通知する上限には、max-concurrent-streamsで設定した値を必ず自動的に加えます。この値を厳密な上限とし、仕様に違反するクライアントがこれを超えた場合は接続を閉じます。したがって、ログから接続ごとのリクエスト数を数えると、クライアントがストリームを作成する速度によって、max-total-streamsから (max-total-streams + max-concurrent-streams) までの値が観測されます。

デフォルト値はゼロで、プロトコルに由来する上限 (2^30 ~= 10.7億) 以外の制限を設けません。1000程度の値でも、ほとんどのクライアントに体感できる遅延を生じさせずに、頻繁な接続の更新を促せます。値が小さすぎると、頻繁なTLS再接続によってCPU使用量が増え、ページの読み込み時間も増加する可能性があります。一部の負荷テストツールは再接続に対応せず、この設定でエラーを報告する場合があるため、性能ベンチマークを実行するときは無効にする必要があるかもしれません。"tune.h2.fe.max-concurrent-streams" も参照してください。

<a id="entry-3-2-tune-h2-fe-rxbuf"></a>

**`tune.h2.fe.rxbuf <size>`**

```haproxy
tune.h2.fe.rxbuf <size>
```

受信接続のHTTP/2受信バッファーサイズを、バイト単位で設定します。サイズはtune.bufsizeの倍数へ切り上げ、データをアップロードするすべてのストリームで共有します（HEADERSフレームとDATAフレームの両方が対象です）。どの場合も、各ストリームには必ず1つのバッファーを与え、未使用バッファーの7/8を、ペイロードをアップロードするストリーム間で共有することで、アップロード性能を大幅に改善できます。通知するストリームごとのウィンドウは、空き領域を反映して自動調整するため、実際にはtune.h2.fe.initial-window-sizeを変更する必要はないはずです。すべてのストリームを処理するのに必要なサイズより小さい値を設定した場合は、その最小サイズを使用します。デフォルト値の1600k（各16kBのバッファーを持つ100ストリーム）では、RTTが100msのクライアントに対して、約130 Mbpsのアップロード速度を実現できます。

関連項目: tune.h2.fe.initial-window-size、tune.h2.be.rxbuf。

<a id="entry-3-2-tune-h2-header-table-size"></a>

**`tune.h2.header-table-size <number>`**

```haproxy
tune.h2.header-table-size <number>
```

HTTP/2の動的ヘッダーテーブルのサイズを設定します。デフォルトは4096バイトで、65536バイトを超えることはできません。大きな値にすると、一部のクライアントは、対応状況によって、より小さなリクエストを送信できる場合があります。このメモリー量は、HTTP/2接続ごとに消費します。変更しないことを推奨します。

<a id="entry-3-2-tune-h2-initial-window-size"></a>

**`tune.h2.initial-window-size <number>`**

```haproxy
tune.h2.initial-window-size <number>
```

受信接続と送信接続の両方について、HTTP/2初期ウィンドウサイズのデフォルト値を設定します。受信接続ではtune.h2.fe.initial-window-sizeを指定していない場合に、送信接続ではtune.h2.be.initial-window-sizeを指定していない場合に、この値を使用します。初期値と、ストリームごとの最小値の両方に使用します。デフォルト値は16384 (tune.bufsize) で、アップロードでは、pingの往復時間が100ミリ秒のネットワークでストリームごとに少なくとも約1.25 Mbps、1ミリ秒のローカルネットワークで125 Mbpsの帯域幅を実現できます。tune.h2.be.rxbufとtune.h2.fe.rxbufで定めた制限の範囲で、使用中の受信バッファー数が上限に達していない場合、未使用のバッファーを受信ストリーム間で共有します。そのため、通常はこのデフォルト設定を変更する意味はありません。この値を変更すると、アップロード速度が上がる一方、ダウンロード時にクライアント間の不公平も増すため、代わりに、接続方向別のtune.h2.fe.initial-window-sizeとtune.h2.be.initial-window-sizeを使用することを推奨します。

<a id="entry-3-2-tune-h2-log-errors"></a>

**`tune.h2.log-errors { none | connection | stream }`**

```haproxy
tune.h2.log-errors { none | connection | stream }
```

H2デマルチプレクサーで、ログを生成するエラーのレベルを設定します。デフォルトは "stream" で、デマルチプレクサーで発生したすべてのデコードエラーについて、ログを出力します。"connection" は、接続を無効にするエラーだけをログに出力します。"none" は、どのデコードエラーについてもログを出力しません。問題が深刻な間は一時的に "none" に切り替える必要があるとしても、プロトコルの異常を検出するため、少なくとも "connection" に設定することを推奨します。

<a id="entry-3-2-tune-h2-max-concurrent-streams"></a>

**`tune.h2.max-concurrent-streams <number>`**

```haproxy
tune.h2.max-concurrent-streams <number>
```

接続ごとのHTTP/2同時ストリーム数の上限（1つの接続で応答待ちのリクエスト数）のデフォルト値を設定します。受信接続ではtune.h2.fe.max-concurrent-streamsを指定していない場合に、送信接続ではtune.h2.be.max-concurrent-streamsを指定していない場合に、この値を使用します。デフォルト値は100です。接続の方向によって影響が異なるため、詳細は前述の両設定を参照してください。この設定は使用せず、方向別の設定に切り替えることを推奨します。ゼロを指定すると制限を無効にし、単一のクライアントが、HAProxyで割り当てられるだけのストリームを作成できるようになります。この値を変更しないことを強く推奨します。

<a id="entry-3-2-tune-h2-max-frame-size"></a>

**`tune.h2.max-frame-size <number>`**

```haproxy
tune.h2.max-frame-size <number>
```

HAProxyが受信可能として相手に通知する、HTTP/2フレームサイズの上限を設定します。デフォルト値は、16384とバッファーサイズ (tune.bufsize) の大きい方です。いずれの場合も、HAProxyはバッファーより大きなフレームサイズへの対応を通知しません。主な用途は、大きなバッファーを使用するときに、最大フレームサイズの設定を制限することです。フレームサイズが大きすぎると、性能に影響したり、一部の相手が不正に動作したりする可能性があります。この値を変更しないことを強く推奨します。

<a id="entry-3-2-tune-h2-zero-copy-fwd-send"></a>

**`tune.h2.zero-copy-fwd-send { on | off }`**

```haproxy
tune.h2.zero-copy-fwd-send { on | off }
```

H2マルチプレクサーで、データのゼロコピー送信を有効 ('on') または無効 ('off') にします。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-http-cookielen"></a>

**`tune.http.cookielen <number>`**

```haproxy
tune.http.cookielen <number>
```

キャプチャーするCookieの長さの上限を設定します。"capture cookie xxx len yyy" に指定できる最大値となり、それより大きい値は、この値に自動的に切り詰めます。すべてのCookieキャプチャーは、個別の設定値に関係なく、このサイズのメモリーを割り当てるため（同じプールを共有します）、大きすぎる値を設定しないことが重要です。この値はリクエストとレスポンスそれぞれに適用するため、接続ごとに割り当てるメモリーは、この値の2倍です。指定しない場合、上限は63文字です。この値を変更しないことを推奨します。

<a id="entry-3-2-tune-http-logurilen"></a>

**`tune.http.logurilen <number>`**

```haproxy
tune.http.logurilen <number>
```

ログに記録するリクエストURIの長さの上限を設定します。重要なクエリ文字列を含む長いリクエストURIが、ログ行で切り詰められるのを防ぎます。syslogの制限とは関係ありません。この上限を増やす場合は、'log ... len yyy' パラメーターも増やすことができます。syslogデーモンにも、専用の設定ディレクティブが必要になる場合があります。デフォルト値は1024です。

<a id="entry-3-2-tune-http-maxhdr"></a>

**`tune.http.maxhdr <number>`**

```haproxy
tune.http.maxhdr <number>
```

受信するHTTPメッセージで許容するヘッダー数の上限を設定します。先頭行を含めたヘッダー数がこの値を超えるメッセージは、リクエストなら "400 Bad Request"、レスポンスなら "502 Bad Gateway" のステータスコードで拒否します。デフォルト値は101です。広く使用されているApacheサーバーも同じ上限を採用していることから、あらゆる用途に十分な値です。不具合のあるアプリケーションが修正されるまでの間、一時的に動作させるために、この上限を増やすと役立つ場合があります。使用できる範囲は1..32767です。ヘッダーを追加するたびに、ストリームごとに32ビットのメモリーを消費するため、この上限を大きくしすぎないでください。

HTTP/1.1はテキストプロトコルなので、メッセージ送信時には特別な制限はありません。メッセージの解析時に制限すれば十分です。HTTP/2とHTTP/3はバイナリープロトコルで、エンコード処理が必要です。プロトコルで定められた制約を守るため、ヘッダーのエンコード時にも上限を設けます。この上限は十分に大きいものの、意図的に文書化していません。同じ理由で、デコードの初期段階にも同じ上限を適用します。

<a id="entry-3-2-tune-idle-pool-shared"></a>

**`tune.idle-pool.shared { full | on | off }`**

```haproxy
tune.idle-pool.shared { full | on | off }
```

同じサーバーのアイドル接続プールを、スレッド間で共有するかどうかを制御します。同じスレッドグループの全スレッドで共有する 'on'、すべてのスレッドで共有する 'full'、無効にする 'off' を指定できます。デフォルトでは、サーバーへの持続接続数を最小限にし、接続の再利用率を最適化するため、同じスレッドグループのスレッド間で共有します ('on')。ほかのスレッドグループとの共有は、性能に影響する可能性があるため、デフォルトでは有効にしませんが、接続の再利用を最大化することを優先する場合には役立ちます。デバッグのためや、HAProxyの接続再利用に不具合が疑われるときは、このオプションを "off" にして、複数スレッド間のアイドルプール共有を強制的に無効にすると便利な場合があります。このオプションを無効にする前に、高い性能を得るために接続の再利用に依存するすべてのサーバーで、"pool-low-conn" に保守的な値を設定することを強く推奨します。そうしないと、スレッド数が増えるにつれて、接続が非常に頻繁に閉じられる可能性があります。

<a id="entry-3-2-tune-idletimer"></a>

**`tune.idletimer <timeout>`**

```haproxy
tune.idletimer <timeout>
```

空のバッファーが、おそらくアイドル状態のストリームに関連付いているとHAProxyが判断するまでの時間を設定します。大きなデータと小さなデータを交互に転送するときに、一部のパケットサイズを最適に調整するために使用します。splice()を使うかどうか、SSLで大きなバッファーを送信するかどうかの判断を、このパラメーターで調節します。値はミリ秒単位で、0から65535までです。ゼロを指定すると、HAProxyはアイドルストリームを検出しようとしません。デフォルトは1000で、エンドユーザーの操作の間（たとえば、クリックする前にページを読む時間）を適切に検出できるようです。この値を変更する理由はないはずです。後述のtune.ssl.maxrecordを参照してください。

<a id="entry-3-2-tune-listener-default-shards"></a>

**`tune.listener.default-shards { by-process | by-thread | by-group }`**

```haproxy
tune.listener.default-shards { by-process | by-thread | by-group }
```

通常、すべての "bind" 行は、単一のシャード、つまりプロセスの全スレッドが待ち受ける単一のソケットを作成します。スレッドが多いと効率が悪く、ポーリング状態の更新や各スレッドへのイベント配信で、カーネルに大きな負荷を生じさせることもあります。最近のOSは、受信接続の負荷分散をサポートします。同じアドレスとポートに複数のソケットをバインドできるようにし、受信接続を各ソケットへ均等に振り分けることで、各スレッドは、自分がバインドされているソケットで待つ接続だけを扱います。これによって、カーネル側の負荷を大きく減らし、受信接続の処理性能を向上させます。HAProxyでは通常、"bind" 行の "shards" 設定で有効にします。このデフォルトは1で、各リスナーがプロセス内で単一になることを意味します。プロセッサーが多いシステムでは、デフォルトを "by-thread" にしてスレッドごとに常に1つのリスニングソケットを作るか、"by-group" にしてスレッドグループごとに常に1つ作る方が便利な場合があります。"by-thread" では、各リスナーにスレッド数と同じ数のソケットが必要になるため、ファイルディスクリプターの使用量に注意してください。また、一部のOS（FreeBSDなど）では、同じアドレスのソケット数は256以下に制限されます。"by-group" は、スレッドグループが単一のデフォルト構成では "by-process" と同等です。この仕組みに対応していないシステムでは、同じソケットを共有する動作にフォールバックします。デフォルトは "by-group" で、複数のバインドをサポートしないシステムやソケットファミリーでは、"by-process" にフォールバックします。

<a id="entry-3-2-tune-listener-multi-queue"></a>

**`tune.listener.multi-queue { on | fair | off }`**

```haproxy
tune.listener.multi-queue { on | fair | off }
```

リスナーの複数キューによる接続受け付けを、有効 ('on' / 'fair') または無効 ('off') にします。リスナー自身だけで受け付ける代わりに、"bind" 行で実行を許可されたすべてのスレッドに、受信トラフィックを分散します。これによって、より均等にトラフィックを分散し、拡張性を大きく改善できます。特に、外部の処理（たとえば、あるスレッドと競合するネットワーク割り込み）によって、スレッドごとの負荷が不均一になり得る環境で有効です。デフォルトの "on" モードは、サンプルの中から接続数が最も少ないスレッドを選び、割り当てを最適化します。長く続く接続では、全スレッドを稼働させ続けられるため、最適な選択となることが多いでしょう。もう1つの "fair" モードは、その時点の負荷にかかわらず、すべてのスレッドを順に選びます。短命な接続や、スレッドが非常に多く、最初のモードでは最も負荷の低いスレッドを見つける確率が低いマシンに、より適している場合があります。最後に、トラブルシューティングや、接続が短命で、OSがすでに十分よく分散していると判断できる状況では、"off" で再分散の仕組みを強制的に無効にできます。デフォルトは "on" です。

<a id="entry-3-2-tune-lua-bool-sample-conversion"></a>

**`tune.lua.bool-sample-conversion { normal | pre-3.1-bug }`**

```haproxy
tune.lua.bool-sample-conversion { normal | pre-3.1-bug }
```

HAProxyのサンプルオブジェクトをLuaへ渡すときに、どのように扱うかを明示的に指定します。たとえば、Luaスクリプトからネイティブのコンバーター、サンプル取得関数、変数などを使用するとき、HAProxyは内部のsmp型を対応するLuaの型へ変換します。従来の実装では、真偽値の扱いに曖昧さがあります。LuaからHAProxyのsmpへの変換では真偽値を正しく保持しますが、HAProxyのsmpからLuaへの変換では、誤って整数へ変換していました。つまり、真偽値を返すサンプル取得関数やコンバーターをLuaから使用すると、整数の0または1を返していました。残念ながら、Luaでは真偽値と整数を相互に置き換えられません。そのため、曖昧さを避けるには、"tune.lua.bool-sample-conversion" を、"normal"（従来の動作を廃して一貫性を高めます）、または "pre-3.1-bug"（従来の動作を強制して、既存のスクリプトのロジックが不正に動作するのを防ぎます）に、明示的に設定しなければなりません。明示的に設定せず、設定ファイルからLuaスクリプトを読み込むと、HAProxyは警告を出力し、従来の動作に合わせて、暗黙に "pre-3.1-bug" をデフォルトとします。使用中のLuaスクリプトが、HAProxyのboolサンプルを真偽値として正しく扱っていることを確認した後に、このオプションを "normal" に設定することを推奨します。

この設定を有効にするには、すべての "lua-load" または "lua-load-per-thread" ディレクティブより前に指定しなければなりません。そうしないと無視されます。

<a id="entry-3-2-tune-lua-burst-timeout"></a>

**`tune.lua.burst-timeout <timeout>`**

```haproxy
tune.lua.burst-timeout <timeout>
```

「バースト」実行タイムアウトは、すべてのLuaハンドラーに適用します。タイムアウトするまでにハンドラーが終了または処理を譲渡しなければ、処理を中止します。スレッドの競合や、トラフィックを処理できない時間が長くなりすぎること、最終的にはウォッチドッグの作動によるプロセスのクラッシュを防ぐためです。処理の譲渡をまたいで時間を累積する、ほかのLuaタイムアウトとは異なり、burst-timeoutは、Luaの1回の実行区間が設定したタイムアウトを超えないことを保証します。

ここでいう処理の譲渡とは、core.(m)sleep()やcore.yield()のようにLuaの処理を譲渡する関数を明示的に呼び出すか、自動的な強制譲渡（tune.lua.forced-yieldを参照）によって、Luaの実行を実際に中断することです。関連するタスクが再スケジュールされると、後で実行を再開します。すべてのLuaハンドラーが処理を譲渡できるわけではないため、譲渡できるハンドラーと、できないハンドラーを区別する必要があります。

処理を譲渡できるハンドラー（タスク、アクションなど）でタイムアウトする場合、そのシステムに対して "tune.lua.forced-yield" が大きすぎる可能性があります。小さくすると改善する場合がありますが、Lua関数内の要所に手動の処理譲渡を追加すると効果があるかどうかを確認するのもよいでしょう。また、中断できない特定のLuaライブラリ関数に、ハンドラーが時間をかけすぎている可能性もあります。

処理を譲渡できないハンドラー（Luaコンバーター、サンプル取得関数）では、単純に計算量が多すぎることを示している場合があります。このようなハンドラーは、リクエストの実行をブロックすることが多いため、リクエスト処理が先に進めるよう、すぐに終了することが期待されます。その点から、設計が不適切なのかもしれません。この場合は、"tune.lua.forced-yield" を小さくしても効果がないため、Lua関数をより高速に動作するよう最適化するのが、一般的な解決方法です。

このタイムアウトでは、Luaが実際に実行している時間だけを数えます。Luaがcore.sleepを実行した場合、スリープ時間は含めません。デフォルトのタイムアウトは1000msです。

注意： ハンドラーからGCサイクルを開始すると（明示的に要求した場合も、しばらくしてLuaが自動的に開始した場合も）、GCサイクルの時間も含めます。

GCサイクルの時間を差し引く方法がないため、飽和したシステムでは、誤検知を引き起こす場合があります（GCが追いつくのに苦労し、利用可能な実行時間の大半を消費するためです）。そのような場合は、次のような解決方法が考えられます。

    - スクリプトを最適化してLuaのメモリー使用量を減らせるか確認します。
    - LuaのGCパラメーターを細かく調整するか、手動のGCサイクルを要求します。両方を行うこともできます。
      （参照: https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage ）
    - tune.lua.burst-timeoutを増やします。

0を設定すると、この保護を完全に無効にします。

<a id="entry-3-2-tune-lua-forced-yield"></a>

**`tune.lua.forced-yield <number>`**

```haproxy
tune.lua.forced-yield <number>
```

このディレクティブは、Luaエンジンが `<number>` 個の命令を実行するたびに、処理を強制的に譲渡させます。長いスクリプトを中断し、HAProxyのスケジューラーが、接続の受け付けやトラフィックの転送など、ほかのタスクを処理できるようにします。デフォルト値は、"lua-load-per-thread" で読み込むスクリプトでは10000命令、"lua-load" で読み込むスクリプトではMAX(500, 10000 / nbthread)命令です（複数のスレッドがグローバルなLuaロックを奪い合う競合を避けながら性能を確保する、最適な値であることが分かっています）。

HAProxyが頻繁にLuaコードを実行し、より高い応答性が必要なら、この値を小さくできます。Luaコードがかなり長く、その結果がデータの処理に絶対に必要なら、`<number>` を増やせます。ただし、マルチスレッドでは競合が増える可能性があるため、値は慎重に設定すべきです。

<a id="entry-3-2-tune-lua-log-loggers"></a>

**`tune.lua.log.loggers { on | off }`**

```haproxy
tune.lua.log.loggers { on | off }
```

現在のプロキシに適用されるロガーがあれば、そのロガーを通じたLuaスクリプトの出力の記録を、有効 ('on') または無効 ('off') にします。

デフォルトは 'on' です。

<a id="entry-3-2-tune-lua-log-stderr"></a>

**`tune.lua.log.stderr { on | auto | off }`**

```haproxy
tune.lua.log.stderr { on | auto | off }
```

stderrを通じたLuaスクリプトの出力の記録を、有効 ('on') または無効 ('off') にします。'auto' の場合は、次のいずれかに当てはまるときに、stderrへの記録を 'on' にします。

    - tune.lua.log.loggersが 'off' に設定されている場合。
    - プロキシ外のコンテキストでスクリプトを実行し、グローバルロガーがない場合。
    - プロキシのコンテキストでスクリプトを実行し、ロガーが関連付けられていない場合。

有効にすると、tune.lua.log.loggersで設定したログに加えて、このログも出力する点に注意してください。

デフォルトは 'auto' です。

<a id="entry-3-2-tune-lua-maxmem"></a>

**`tune.lua.maxmem <number>`**

```haproxy
tune.lua.maxmem <number>
```

Luaが使用できるRAMの上限を、プロセスごとにメガバイト単位で設定します。デフォルトはゼロで、無制限を意味します。スクリプトの不具合によってシステムがメモリー不足にならないよう、上限を設定することが重要です。

<a id="entry-3-2-tune-lua-openlibs"></a>

**`tune.lua.openlibs [all | none | <lib>[,<lib>...]]`**

```haproxy
tune.lua.openlibs [all | none | <lib>[,<lib>...]]
```

Luaの状態を初期化するときに読み込む、Lua標準ライブラリを選択します。引数は、table、io、os、string、math、utf8、package、debugから選んだライブラリ名を、コンマで区切った一覧です。一覧の代わりに、特別な値 "all" または "none" を使用できます。"none" とライブラリ名を組み合わせることはできません。デフォルト値は "all" です。

baseとcoroutineライブラリは、この設定に関係なく常に読み込みます。baseはHAProxyが依存するLuaの基本関数を提供し、coroutineは、HAProxyがcoroutine.create()を独自の安全な実装で上書きするために必要です。

この設定に関係なく、HAProxyではfork()と新しいスレッドの作成を、すでにデフォルトで禁止しています。再び有効にできるのは、globalの "insecure-fork-wanted" ディレクティブだけです。読み込むライブラリを制限すると、Luaスクリプトにさらす攻撃対象をさらに減らせます。具体的には: - "os" を除くと、os.execute()とos.exit()を防ぎます - "io" を除くと、io.open()とio.popen()を防ぎます - "package" を除くと、require()によるネイティブCモジュールの読み込みを防ぎます - "debug" を除くと、debug.getupvalue()、debug.getmetatable()、debug.sethook()によるHAProxy内部の調査を防ぎます

例:

```text
tune.lua.openlibs none                    # only base + coroutine
tune.lua.openlibs string,math,table,utf8  # safe subset, no I/O or OS
tune.lua.openlibs all                     # default, load everything
```

この設定は、すべての "lua-load"、"lua-load-per-thread"、"lua-prepend-path" ディレクティブより前に指定しなければなりません。そうしないと、解析エラーを返します。

<a id="entry-3-2-tune-lua-service-timeout"></a>

**`tune.lua.service-timeout <timeout>`**

```haproxy
tune.lua.service-timeout <timeout>
```

Luaサービスの実行タイムアウトです。無限ループや、Luaで時間をかけすぎることを防ぐのに役立ちます。Luaが実際に実行している時間だけを数えます。Luaがスリープした場合、その時間は含めません。デフォルトのタイムアウトは4sです。

<a id="entry-3-2-tune-lua-session-timeout"></a>

**`tune.lua.session-timeout <timeout>`**

```haproxy
tune.lua.session-timeout <timeout>
```

Luaセッションの実行タイムアウトです。無限ループや、Luaで時間をかけすぎることを防ぐのに役立ちます。Luaが実際に実行している時間だけを数えます。Luaがスリープした場合、その時間は含めません。デフォルトのタイムアウトは4sです。

<a id="entry-3-2-tune-lua-task-timeout"></a>

**`tune.lua.task-timeout <timeout>`**

```haproxy
tune.lua.task-timeout <timeout>
```

用途は "tune.lua.session-timeout" と同じですが、このタイムアウトはタスク専用です。タスクは、HAProxyの稼働期間中ずっと存在することがあるため、デフォルトではタイムアウトを設定しません。サーバーをチェックするタスクなどが、その例です。

<a id="entry-3-2-tune-max-checks-per-thread"></a>

**`tune.max-checks-per-thread <number>`**

```haproxy
tune.max-checks-per-thread <number>
```

スレッドごとの実行中チェック数を設定します。この数を超えると、スレッドはヘルスチェックを実行するために、負荷の低いスレッドを積極的に探すか、自分で実行中のチェック数が減るまでキューで待機させます。デフォルト値はゼロで、この制限を設けないことを意味します。非常に多数の高コストのチェックを多くのスレッドで実行し、負荷が不均等で、起動時のヘルスチェックが不規則にタイムアウトするような環境で、必要になる場合があります。典型例は、古い版よりヘルスチェックのCPU負荷が約20倍になるOpenSSL 3.0を使用する場合です。これによって、すべてのスレッド間でヘルスチェックの処理量を均等化しようとします。大半の構成では、このパラメーターを変更する必要はありません。チェックの実行が遅い場合、値が小さすぎると、ヘルスチェックが大幅に遅くなる可能性がある点に注意してください。

<a id="entry-3-2-tune-maxaccept"></a>

**`tune.maxaccept <number>`**

```haproxy
tune.maxaccept <number>
```

プロセスがほかの処理へ切り替える前に、続けて受け付けられる接続数の上限を設定します。単一プロセスモードでは、以前は、接続頻度が高いときに値を大きくすると性能が上がりましたが、複数キューでは、もはやそうではありません。この値はリスナーごとに適用され、リスナーがバインドされているプロセス数を考慮します。最もよい結果が得られた4をデフォルトとします。古い設定から大幅に大きな値を引き継いでいる場合は、削除することで、性能と応答時間の両方が改善する可能性があります。マルチプロセスモードでは、リスナーがバインドされているプロセス数の2倍で割ります。-1を指定すると、制限を完全に無効にします。通常は、この値を調整する必要はないはずです。

<a id="entry-3-2-tune-maxpollevents"></a>

**`tune.maxpollevents <number>`**

```haproxy
tune.maxpollevents <number>
```

ポーリングシステムを呼び出したときに、一度に処理できるイベント数の上限を設定します。デフォルト値は、OSに合わせた値です。200より小さくすると、ネットワーク帯域幅を犠牲にして遅延がわずかに減り、200より大きくすると、遅延を犠牲にして帯域幅がわずかに増える傾向が観測されています。設定値は1000000以下でなければなりません。

<a id="entry-3-2-tune-maxrewrite"></a>

**`tune.maxrewrite <number>`**

```haproxy
tune.maxrewrite <number>
```

予約するバッファー領域のサイズを、バイト単位で設定します。予約領域は、ヘッダーの書き換えや追加に使用します。ソケットからの最初の読み取りは、bufsize-maxrewriteを超えてバッファーを埋めることはありません。従来のデフォルトはbufsizeの半分でしたが、大量のヘッダーを追加することはまれなので、あまり意味はありません。大きすぎると、大きなリクエストやレスポンスを処理できなくなります。小さすぎると、すでに大きなリクエストやPOSTリクエストに、新しいヘッダーを追加できなくなります。一般には、1024程度にするのが適切です。bufsizeの半分より大きい場合は、自動的にその半分へ再調整します。そのため、bufsizeを変更するときに心配する必要はありません。

<a id="entry-3-2-tune-max-rules-at-once"></a>

**`tune.max-rules-at-once <number>`**

```haproxy
tune.max-rules-at-once <number>
```

処理の譲渡に対応するルールセット評価関数で、一度に評価できるルール数の上限を設定します。たとえば、"tcp-request content" や "http-request" ルールを大量に含む設定は、珍しくありません。評価を中断しなければ、同じポーリングループ内で、あるルールセットのすべてのルールを評価します。そのため、多数のルールと、CPU負荷の高いアクション（コンテンツを処理するものなど）を組み合わせると、スレッドの競合が生じる可能性があります。このオプションは、コンテンツを扱うルールセット（コンテンツ検査のため、すでに処理の譲渡に対応するもの）について、同じポーリングループで実行するルール数が `<number>` を超えないことを保証します。具体的には、評価関数に処理を強制的に譲渡させ、次のポーリングループで評価を再開させます。

対象のルールセットは次のとおりです。

- "tcp-request content"
- "tcp-response content"
- "http-request"
- "http-response"

デフォルト値は50です。

<a id="entry-3-2-tune-memory-hot-size"></a>

**`tune.memory.hot-size <number>`**

```haproxy
tune.memory.hot-size <number>
```

スレッドごとに、ローカルキャッシュで即座に使用できる状態に保持し、ほかのスレッドが決して回収できないメモリー量を設定します。このメモリーへのアクセスは、ロック不要で非常に高速です。スレッド間の競合が極端に激しい状況で、よい性能を保つには、十分な量を確保することが不可欠です。値はバイト単位で、デフォルト値は、ビルド時にCONFIG_HAP_POOL_CACHE_SIZEで設定します。そのデフォルトは524288 (512 kB) です。特に、性能プロファイルでメモリー割り当てへの負荷が大きいことが分かる場合など、一部の用途では、大きな値にすると性能が向上する可能性があります。経験上、CPUコアごとのL2キャッシュサイズの1倍から2倍が、適切な値です。大きすぎる値は、CPUのL3キャッシュを非効率に使用して性能を低下させ、メモリーの消費量も増やします。この値は変更しないか、少しずつ増やすことを推奨します。スレッドごとのCPUキャッシュを完全に無効にするには、非常に小さな値でも機能する場合がありますが、コマンドラインで "-dMno-cache" を使用する方が適切です。

<a id="entry-3-2-tune-notsent-lowat-client"></a>

**`tune.notsent-lowat.client <size>`**

```haproxy
tune.notsent-lowat.client <size>
tune.notsent-lowat.server <size>
```

カーネルがソケットごとに行うバッファリングを調整し、バッファー内のデータ量が、この値と測定したウィンドウサイズの合計に達すると、ソケットの送信側がいっぱいであることを通知するようにします。ソケットバッファーには、必要最小限のバイト数に加え、HAProxyが再び送信を試みるまでに送信する分に相当する、小さな余裕だけを残すという考え方です。小さい値（通常はtune.bufsize程度）を設定すると、システムバッファーのメモリー使用量と、バッファー内のデータを送り出すことで生じるアプリケーションレベルの遅延を、大幅に減らせます。対応するシステムでは、通常、tune.sndbuf.clientとtune.sndbuf.clientより、効果的で正確な設定になります。接続ごとに適用し（設定に応じて、クライアントからの接続、またはサーバーへの接続）、TCP接続でのみ使用します。デフォルトはゼロで、無制限を意味します。Linuxでのみ利用できます。

<a id="entry-3-2-tune-pattern-cache-size"></a>

**`tune.pattern.cache-size <number>`**

```haproxy
tune.pattern.cache-size <number>
```

パターン検索キャッシュのサイズを `<number>` エントリーに設定します。過去の検索と結果を記憶するLRUキャッシュです。ACLとマップが行う、処理の遅いパターン検索で使用します。具体的には、"sub"、"reg"、"dir"、"dom"、"end"、"bin" の照合方法と、大文字と小文字を区別しない文字列を対象とします。パターン式に適用するため、設定の同じ行で指定したすべてのパターン（ファイルから読み込んだものも含みます）の中から検索した結果を、記憶できます。HTTPアクションやCLIで更新したエントリーは、自動的に無効にします。キャッシュサイズのデフォルトは10000エントリーです。キャッシュはスレッドまたはプロセスごとに保持するため、そのメモリー使用量は、32ビットシステムではプロセスまたはスレッドごとに約5 MB、64ビットシステムでは約8 MBに収まります。このキャッシュには、ごくわずかな衝突のリスクがあり、その程度はキャッシュサイズを2^64で割った値です。通常、毎秒10000リクエスト、デフォルトの10000エントリーのキャッシュサイズでは、総当たり攻撃によって1回の衝突が生じる確率は、60年後に1%、または6年後に0.1%です。これは、部品の経年劣化によってメモリーが破損するリスクより、はるかに小さいと考えられます。受け入れられない場合は、このパラメーターを0にすると、キャッシュを無効にできます。

<a id="entry-3-2-tune-peers-max-updates-at-once"></a>

**`tune.peers.max-updates-at-once <number>`**

```haproxy
tune.peers.max-updates-at-once <number>
```

メッセージの送信時に、HAProxyが一度に処理を試みる、スティックテーブルの更新数の上限を設定します。更新するデータの取得には、いくつかのロック操作が必要です。制限しないと、スレッド数の多いマシンではCPU負荷が高くなり、古いプロセスと新しいプロセス間の初回の一括転送中に、トラフィックの遅延が増える場合もあります。一方、小さすぎる値でも、CPUのオーバーヘッドが増え、完了までの時間が長くなる場合があります。デフォルト値は200で、変更しないことを推奨します。

<a id="entry-3-2-tune-pipesize"></a>

**`tune.pipesize <size>`**

```haproxy
tune.pipesize <size>
```

カーネルのパイプバッファーのサイズを、このサイズ（バイト単位）に設定します。デフォルトでは、システム標準のパイプサイズを使用します。ただし、TCPスプライシングを使用する場合、パイプサイズを大きくすると、性能が向上することがあります。特に、パイプが埋まらず、splice()を何度も呼び出していると疑われる場合が該当します。カーネルのメモリー使用量に影響するため、影響を理解していない場合は変更してはいけません。

<a id="entry-3-2-tune-pool-high-fd-ratio"></a>

**`tune.pool-high-fd-ratio <number>`**

```haproxy
tune.pool-high-fd-ratio <number>
```

接続を再利用できず、新しい接続を作成する必要があるときに、アイドル接続の終了を開始する、HAProxy全体のファイル記述子使用数の上限を設定します。値は、HAProxyが使用できるファイル記述子の最大数に対する割合（パーセント）です。デフォルトは25です（ファイル記述子の4分の1を使うと、フロント側の最大接続数のおよそ半分について、バックエンド側にアイドル接続を保持できます。接続の再利用を目的とする一般的な場合、これ以上にしても、おそらくあまり意味はありません）。

<a id="entry-3-2-tune-pool-low-fd-ratio"></a>

**`tune.pool-low-fd-ratio <number>`**

```haproxy
tune.pool-low-fd-ratio <number>
```

再利用のために、接続をアイドルプールへ追加するのをやめる、HAProxy全体のファイル記述子使用数の上限を設定します。値は、HAProxyが使用できるファイル記述子の最大数に対する割合（パーセント）です。デフォルトは20です。

<a id="entry-3-2-tune-pt-zero-copy-forwarding"></a>

**`tune.pt.zero-copy-forwarding { on | off }`**

```haproxy
tune.pt.zero-copy-forwarding { on | off }
```

パススルー・マルチプレクサーで、データのゼロコピー転送を有効 ('on') または無効 ('off') にします。使用するには、カーネルのスプライシングも設定する必要があります。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding、option splice-auto、option splice-request、option splice-response

<a id="entry-3-2-tune-quic-be-cc-cubic-min-losses"></a>

**`tune.quic.be.cc.cubic-min-losses <number>`**

```haproxy
tune.quic.be.cc.cubic-min-losses <number>
tune.quic.fe.cc.cubic-min-losses <number>
```

Cubic輻輳制御アルゴリズムが、実際に損失イベントとみなすために必要な、損失パケット数を定義します。通常、損失イベントはすべて輻輳の結果とみなし、それだけで、Cubicは小さいウィンドウから再開します。しかし実験によると、輻輳とはまったく関係のない、さまざまな原因で損失が生じることがあります。これは、単に見かけ上の損失と呼べるもので、ウィンドウを調整しても、通信を遅くする以外の効果はありません。よくある原因としては、無線の電波状態の悪化、順序が入れ替わった配送、クライアントのCPU負荷が高いことによる不規則な遅延、システムタイマーの精度不足などが挙げられます。この設定では、2つのACKの間に累積した損失を、損失イベントとみなすための最小数（デフォルトは1）を変更し、見かけ上の損失に対して、Cubicを少し寛容にできます。実験では、大幅な改善が観測された例もありますが、常に、再送で無駄になる帯域幅の増加と、輻輳したリンクを飽和させるリスクの増加を伴いました。値2は、いくつかの指標を比較するために、短時間使用できます。専門家が事前に状況を分析していない限り、決して2を超える値にしないでください。デフォルト値と最小値は1です。常に1を使用してください。

<a id="entry-3-2-tune-quic-cc-cubic-min-losses"></a>

**`tune.quic.cc.cubic.min-losses <number> (deprecated)`**

```haproxy
tune.quic.cc.cubic.min-losses <number> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-cc-hystart"></a>

**`tune.quic.be.cc.hystart { on | off }`**

```haproxy
tune.quic.be.cc.hystart { on | off }
tune.quic.fe.cc.hystart { on | off }
```

QUIC接続で、HyStart++ (RFC 9406) アルゴリズムを有効 ('on') または無効 ('off') にします。これは、多くのパケット損失を引き起こす可能性がある、輻輳制御アルゴリズムのスロースタート段階の代わりに使用します。デフォルトでは無効です。

<a id="entry-3-2-tune-quic-cc-hystart"></a>

**`tune.quic.cc-hystart { on | off } (deprecated)`**

```haproxy
tune.quic.cc-hystart { on | off } (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-cc-max-frame-loss"></a>

**`tune.quic.be.cc.max-frame-loss <number>`**

```haproxy
tune.quic.be.cc.max-frame-loss <number>
tune.quic.fe.cc.max-frame-loss <number>
```

同じQUICフレームを、損失したと判定できる回数の上限を設定します。超えると、その接続は失敗したものとみなし、直ちに閉じます。

デフォルト値は10です。

<a id="entry-3-2-tune-quic-max-frame-loss"></a>

**`tune.quic.max-frame-loss <number> (deprecated)`**

```haproxy
tune.quic.max-frame-loss <number> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-cc-max-win-size"></a>

**`tune.quic.be.cc.max-win-size <size>`**

```haproxy
tune.quic.be.cc.max-win-size <size>
tune.quic.fe.cc.max-win-size <size>
```

フロントエンド側またはバックエンド側の、単一のQUIC接続の輻輳制御器に対する、最大ウィンドウサイズのデフォルト値を設定します。値は整数で記述し、任意で接尾辞 'k'、'm'、'g' を付けられます。10kから4gの範囲でなければなりません。

QUICマルチプレクサーも、データ送信時に新しいストリームバッファーを割り当てられるか判断するため、現在の輻輳ウィンドウサイズを使用します。そのため、最大輻輳ウィンドウサイズは、このアロケーターの上限としても機能します。

デフォルト値は480kです。

bindとserverの "quic-cc-algo" オプションも参照してください。

<a id="entry-3-2-tune-quic-frontend-default-max-window-size"></a>

**`tune.quic.frontend.default-max-window-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.default-max-window-size <size> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-cc-reorder-ratio"></a>

**`tune.quic.be.cc.reorder-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.cc.reorder-ratio <0..100, in percent>
tune.quic.fe.cc.reorder-ratio <0..100, in percent>
```

計算したパケット並べ替えしきい値に適用する比率です。小さすぎると、多数のパケット損失を検出する場合があります。

デフォルト値は50です。

<a id="entry-3-2-tune-quic-reorder-ratio"></a>

**`tune.quic.reorder-ratio <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.reorder-ratio <0..100, in percent> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-max-idle-timeout"></a>

**`tune.quic.be.max-idle-timeout <timeout>`**

```haproxy
tune.quic.be.max-idle-timeout <timeout>
tune.quic.fe.max-idle-timeout <timeout>
```

フロントエンド側またはバックエンド側で、QUICのmax_idle_timeoutトランスポートパラメーターを設定します。HAProxyの時間形式に従い、ミリ秒単位で表します。接続が実効的な期間にわたって非アクティブであった場合に、通知せずに接続を閉じるまでの時間を決定します。両方のエンドポイントが、次のようにネゴシエートした同じ値を使用します。- 両方のパラメーターがゼロでなければ、両者の最小値 - 片方だけがゼロでなければ、両者の最大値 - 両方のパラメーターがゼロなら、この機能を無効にします。

デフォルト値は30sです。

<a id="entry-3-2-tune-quic-frontend-max-idle-timeout"></a>

**`tune.quic.frontend.max-idle-timeout <timeout> (deprecated)`**

```haproxy
tune.quic.frontend.max-idle-timeout <timeout> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-sec-glitches-threshold"></a>

**`tune.quic.be.sec.glitches-threshold <number>`**

```haproxy
tune.quic.be.sec.glitches-threshold <number>
tune.quic.fe.sec.glitches-threshold <number>
```

フロントエンド側またはバックエンド側の接続ごとに、異常の回数のしきい値を設定します。このしきい値に達すると、接続を自動的に終了します。これにより、明示的なルールを書かずに、不正な動作をする接続を自動的に終了できます。デフォルト値はゼロです。しきい値を設定しないことを意味し、どのイベントでも接続を閉じません。QUICクライアントによっては、長時間維持した接続で、ときどき少数の異常を引き起こすことがあります。そのため、多少の不具合があるクライアントに影響を与えずに効果を得るには、ゼロ以外の値を設定する場合、数百や数千程度にすべきでしょう。"tune.glitches.kill.cpu-usage" を使用すると、CPU使用率が一定の水準を超えた場合にのみ、接続を終了することもできます。

関連項目: fc_glitches、tune.glitches.kill.cpu-usage

<a id="entry-3-2-tune-quic-frontend-glitches-threshold"></a>

**`tune.quic.frontend.glitches-threshold <number> (deprecated)`**

```haproxy
tune.quic.frontend.glitches-threshold <number> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-fe-sec-retry-threshold"></a>

**`tune.quic.fe.sec.retry-threshold <number>`**

```haproxy
tune.quic.fe.sec.retry-threshold <number>
```

半開接続の数がこの値に達すると、設定したすべてのQUICリスナーについて、Retry機能を動的に有効にします。半開接続とは、ハンドシェイクがまだ成功も失敗もしていない接続です。この設定を機能させるには、クラスターシークレットを設定する必要があります。設定していない場合は、通知せずに無視します（"cluster-secret" の設定を参照）。QUIC Retryの使用を強制している場合も、通知せずに無視します（"quic-force-retry" を参照）。

デフォルト値は100です。

QUIC Retryの詳細は、<https://www.rfc-editor.org/rfc/rfc9000.html#section-8.1.2> を参照してください。

<a id="entry-3-2-tune-quic-retry-threshold"></a>

**`tune.quic.retry-threshold <number> (deprecated)`**

```haproxy
tune.quic.retry-threshold <number> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-fe-sock-per-conn"></a>

**`tune.quic.fe.sock-per-conn { default-on | force-off }`**

```haproxy
tune.quic.fe.sock-per-conn { default-on | force-off }
```

QUICのフロントエンド接続で、受信と送信にソケットをどのように使用するかを、グローバルに指定します。各接続がリスナーのソケットを共有するか、それぞれの接続で専用のソケットを割り当てられます。

デフォルト値は "default-on" です。QUIC接続ごとに、専用のソケットを割り当てます。QUICトラフィックが大量にある場合に、最もよい性能を得るために推奨する選択肢です。また、QUIC接続でデータを失わずにソフトストップを適切に実行し、sendto()操作中の一時的なエラーを効率的に処理できるようにする、唯一の方法でもあります。ただし、UDPネットワークスタックの高度な機能に依存します。プラットフォームに互換性がないと判断した場合、HAProxyは起動時に、自動的に "force-off" モードへ切り替えます。特権ポートで動作するQUICリスナーでは、uid 0での実行が必要になる場合や、対象uidにそのポートへのバインドを許可するため、システムケーパビリティなど、OS固有の調整が必要になる場合がある点に注意してください。globalの "setcap" ディレクティブも参照してください。

値 "force-off" は、共有するリスナーのソケットで、QUICの転送を行うことを意味します。FDの消費量を減らせるため、トラフィックが少ない場合には、適切な妥協点となり得ます。ただし、多数のスレッド間でリスナーを共有する場合や、多数のQUIC接続を同時に使用できる場合は、CPU使用率が高くなるため、性能は最適になりません。

この設定は、各bindの "quic-socket" オプションと組み合わせて適用します。グローバルな調整で "default-on" モードを使用すると、"quic-socket listener" を指定したものを除き、各リスナーで有効にします。一方、グローバルに "force-off" を使用すると、個別の設定に関係なく、すべてのリスナーのインスタンスに適用します。

<a id="entry-3-2-tune-quic-socket-owner"></a>

**`tune.quic.socket-owner { connection | listener } (deprecated)`**

```haproxy
tune.quic.socket-owner { connection | listener } (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。新しいオプションの名前は "tune.quic.fe.sock-per-conn" です。従来の値 "connection" は "default-on" に、"listener" は "force-off" に対応します。

<a id="entry-3-2-tune-quic-be-stream-data-ratio"></a>

**`tune.quic.be.stream.data-ratio <0..100, in percent>`**

```haproxy
tune.quic.be.stream.data-ratio <0..100, in percent>
tune.quic.fe.stream.data-ratio <0..100, in percent>
```

この設定は、各ストリームで転送中のデータバイト数の、厳密な上限を設定できます。QUICストリームの接続単位のrxbuf設定に対する割合（パーセント）で表し、その結果をbufsizeの単位で切り上げます。

デフォルト値は90です。アップロードは1つまたは少数のストリームでのみ行い、残りはダウンロードにのみ使用する、最も一般的なWebの利用形態に適しています。ストリームの接続単位のrxbuf上限が妥当な水準であれば、開いているストリームのうち、一部だけが最大容量まで割り当てられるようにします。

多数のアップロード用ストリームを並行して使用し、ストリーム間の不公平が問題になっているアプリケーションでは、この比率を下げて、公平性を高め、ストリームごとの帯域幅を減らすことが、適切な場合があります。

関連項目: "tune.quic.be.stream.rxbuf"、"tune.quic.fe.stream.rxbuf"、"tune.quic.be.stream.max-concurrent"、"tune.quic.fe.stream.max-concurrent"

<a id="entry-3-2-tune-quic-frontend-stream-data-ratio"></a>

**`tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)`**

```haproxy
tune.quic.frontend.stream-data-ratio  <0..100, in percent> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-stream-max-concurrent"></a>

**`tune.quic.be.stream.max-concurrent <number>`**

```haproxy
tune.quic.be.stream.max-concurrent <number>
tune.quic.fe.stream.max-concurrent <number>
```

フロントエンド側では、通知するinitial_max_streams_bidiトランスポートパラメーターの値として使用します。接続の存続期間中、リモートピアが同時に開くことを許可する、双方向ストリーム数の上限として適用します。実質的に、HTTP/3クライアントの同時リクエスト数を制限します。

デフォルト値は100です。小さくすると、ストリームの受信バッファリング能力を制限し、アップロードのスループットが低下する場合がある点に注意してください。QUICストリームの接続単位のrxbuf設定を増やすと、改善できます。

バックエンド側では、単一の接続で多重化する同時リクエスト数を制限するため、HAProxyがローカルで適用します。ピアのフロー制御によって、さらに制限される場合があります。サイトの応答性を高めるため、開くバックエンド接続数が増えることと引き換えに、デフォルト値の100を下げる必要がある場合があります。フロントエンド側と同様、この設定は受信バッファリング能力にも直接影響しますが、こちらではHTTPのダウンロード能力を制限します。主に "tune.bufsize" より大きいHTTPレスポンスを扱う場合は、QUICストリームのrxbuf設定を増やせます。

関連項目: "tune.quic.be.stream.rxbuf"、"tune.quic.fe.stream.rxbuf"、"tune.quic.be.stream.data-ratio"、"tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-fe-stream-max-total"></a>

**`tune.quic.fe.stream.max-total <number>`**

```haproxy
tune.quic.fe.stream.max-total <number>
```

単一のQUIC接続で処理できるリクエスト数の上限を設定します。この総数に達すると、接続の正常な終了処理を開始します。HTTP/3では、GOAWAYフレームに相当します。残っている転送がすべて完了すると、最後に接続を閉じます。

この設定は、QUICのフロー制御機構を通じて、接続に対する厳密な上限として適用します。ピアが違反した場合は、直ちに接続を閉じます。

この設定を使用すると、クライアントがリクエストの送信を続けるために、ときどき新しい接続を開くよう強制し、接続を長く維持しすぎることを防げます。ただし、値が小さいと、TLSハンドシェイクによって、クライアント側の遅延と、両側のCPU消費量が増えます。

デフォルト値は0です。QUICプロトコルの符号化による制限（2^60、10億の10億倍を超える数）以外に、特別な制限を設けないことを意味します。

<a id="entry-3-2-tune-quic-frontend-max-streams-bidi"></a>

**`tune.quic.frontend.max-streams-bidi <number> (deprecated)`**

```haproxy
tune.quic.frontend.max-streams-bidi <number> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-stream-rxbuf"></a>

**`tune.quic.be.stream.rxbuf <size>`**

```haproxy
tune.quic.be.stream.rxbuf <size>
tune.quic.fe.stream.rxbuf <size>
```

この設定は、QUICのフロントエンド接続で転送中のデータバイト数の、厳密な上限です。initial_max_dataトランスポートパラメーターの値として再利用します。遅延に応じて、ピアのアップロード帯域幅に直接影響し、HAProxyの接続ごとのメモリー消費量にも直接影響します。

デフォルト値は0です。max-concurrentとbufsizeの積から、自動的に生成しなければならないことを意味します。たとえば、バックエンドのアプリケーションが、遅延の大きなネットワークで大量のアップロードを行う場合は、増やせます。

関連項目: "tune.quic.be.stream.max-concurrent"、"tune.quic.fe.stream.max-concurrent"、"tune.quic.be.stream.data-ratio"、"tune.quic.fe.stream.data-ratio"

<a id="entry-3-2-tune-quic-frontend-max-data-size"></a>

**`tune.quic.frontend.max-data-size <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-data-size <size> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-tx-pacing"></a>

**`tune.quic.be.tx.pacing { on | off }`**

```haproxy
tune.quic.be.tx.pacing { on | off }
tune.quic.fe.tx.pacing { on | off }
```

QUIC送信のペーシング機能を、有効 ('on') または無効 ('off') にします。デフォルトで有効です。ペーシングの目的は、データの送信を平準化して、ネットワーク上の損失を減らすことです。大半の状況では、再送を避けることで、ネットワークのスループットが大幅に向上します。ただし、帯域幅が非常に大きく、遅延の小さいネットワークでは、意図しない遅延を防ぎ、CPU消費量を減らすため、無効にするとよい場合があります。

bindとserverの "quic-cc-algo" オプションも参照してください。

<a id="entry-3-2-tune-quic-disable-tx-pacing"></a>

**`tune.quic.disable-tx-pacing (deprecated)`**

```haproxy
tune.quic.disable-tx-pacing (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-be-tx-udp-gso"></a>

**`tune.quic.be.tx.udp-gso { on | off }`**

```haproxy
tune.quic.be.tx.udp-gso { on | off }
tune.quic.fe.tx.udp-gso { on | off }
```

QUIC送信のUDP GSO機能を、有効 ('on') または無効 ('off') にします。デフォルトで有効です。このカーネル機能は、単一のシステムコールで複数のデータグラムを送信でき、大量の転送で効率がよくなります。送信に問題があると疑われる場合、開発者の提案に従って無効にするとよい場合があります。

<a id="entry-3-2-tune-quic-disable-udp-gso"></a>

**`tune.quic.disable-udp-gso (deprecated)`**

```haproxy
tune.quic.disable-udp-gso (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-listen"></a>

**`tune.quic.listen { on | off }`**

```haproxy
tune.quic.listen { on | off }
```

フロントエンド側のQUICトランスポートプロトコルを無効にします。QUICリスナーはすべて作成しますが、着信データグラムを待ち受けません。そのため、HAProxyはフロントエンド側のQUICトラフィックを処理しません。

デフォルト値は "on" です。QUICトラフィックに問題があると疑われる場合、このオプションを使用すると、個々の設定行を変更せずに、QUICリスナーを簡単に切り替えられます。

サンプル取得関数 "quic_enabled" も参照してください。

<a id="entry-3-2-tune-quic-mem-tx-max"></a>

**`tune.quic.mem.tx-max <size>`**

```haproxy
tune.quic.mem.tx-max <size>
```

QUICスタックがトランスポート層で送信に使用できる、メモリー量の上限を設定します。転送中のバイト数と、マルチプレクサーの出力バッファーの、両方の上限として機能します。スレッドの競合を避けるため、この上限は厳密には適用しないので、状況によっては超える場合がある点に注意してください。また、各接続は常に、少なくとも2つのデータグラムのウィンドウを使用できるため、適切なmaxconnと組み合わせて使用すべきです。

<a id="entry-3-2-tune-quic-frontend-max-tx-mem"></a>

**`tune.quic.frontend.max-tx-mem <size> (deprecated)`**

```haproxy
tune.quic.frontend.max-tx-mem <size> (deprecated)
```

このキーワードは3.3で非推奨となり、3.5で削除します。QUIC設定を整理する作業の一環です。使用した場合は、フロントエンドの接続にのみ適用します。

<a id="entry-3-2-tune-quic-zero-copy-fwd-send"></a>

**`tune.quic.zero-copy-fwd-send { on | off }`**

```haproxy
tune.quic.zero-copy-fwd-send { on | off }
```

QUICマルチプレクサーで、データのゼロコピー送信を有効 ('on') または無効 ('off') にします。デフォルトで有効です。

関連項目: tune.disable-zero-copy-forwarding

<a id="entry-3-2-tune-renice-runtime"></a>

**`tune.renice.runtime <number>`**

```haproxy
tune.renice.runtime <number>
```

この設定オプションは、-20から19までの値を受け付けます。man 2 setpriorityに記載された、スケジューリング優先度を適用します。設定の解析後に適用するため、ワーカーまたは単独で動作するプロセスだけが、この優先度を適用します。通常は、設定の解析を行うプロセス（tune.renice.startup）より、高い優先度になるように設定します。

関連項目: tune.renice.startup

<a id="entry-3-2-tune-renice-startup"></a>

**`tune.renice.startup <number>`**

```haproxy
tune.renice.startup <number>
```

この設定オプションは、-20から19までの値を受け付けます。man 2 setpriorityに記載された、スケジューリング優先度を適用します。残りの設定を適用する前に、この優先度を適用するため、設定の解析時に優先度を下げたい場合に役立ちます。設定の解析前に、単独で動作するプロセスまたはワーカーに適用します。設定を解析した後は、tune.renice.runtimeを使用していなければ、以前の優先度に戻します。

関連項目: tune.renice.runtime

<a id="entry-3-2-tune-rcvbuf-backend"></a>

**`tune.rcvbuf.backend  <size>`**

```haproxy
tune.rcvbuf.backend  <size>
tune.rcvbuf.frontend <size>
```

接続されていないソケットの、カーネルの受信バッファーサイズを、このサイズに固定します。フロントエンドで、リスナーモードのQUICとlog-forwardに使用できます。システムのデフォルトのバッファーは、集約された大量のトラフィックを受信するソケットには小さすぎる場合があります。その場合、損失や、QUICでは再送が生じる可能性があり、トラフィックが多いときに、接続の確立が遅くなる場合があります。値はバイト単位で、各ソケットに適用します。リスナーモードでは、すべての接続でソケットを共有し、ソケットの総数は、"bind" 行の "shards" の値で決まります。一律に適切な値はありません。接続ごとに想定するサイズに、想定する接続数を掛けた値が、適切な値になります。大きな値は、カーネルが縮小する場合があります。接続されたソケットに対応する "tune.rcvbuf.client" と "tune.rcvbuf.server"、および送信側の設定である "tune.sndbuf.backend" と "tune.sndbuf.frontend" も参照してください。

<a id="entry-3-2-tune-rcvbuf-client"></a>

**`tune.rcvbuf.client <size>`**

```haproxy
tune.rcvbuf.client <size>
tune.rcvbuf.server <size>
```

クライアント側またはサーバー側の、カーネルのソケット受信バッファーサイズを、指定したバイト数に固定します。すべてのTCP/HTTPフロントエンドとバックエンドに適用します。通常は決して設定すべきではありません。デフォルトのサイズ (0) では、利用できるメモリー量に応じて、カーネルが値を自動調整します。ただし、非常に小さい値（たとえば4096）に設定すると、受信したデータを大量にバッファリングするのを防ぎ、カーネルのメモリーを節約できる場合があります。ただし、値を小さくすると、CPU使用率が大幅に増えます。

<a id="entry-3-2-tune-recv-enough"></a>

**`tune.recv_enough <size>`**

```haproxy
tune.recv_enough <size>
```

HAProxyは、短い読み取りがソケットバッファーの終わりを示すことを検出するため、いくつかの手掛かりを使用します。そのうちの1つが、読み取りで `<recv_enough>` バイトを超えるデータが返ることです。デフォルトは10136（1448ずつの7セグメント）です。この設定でデフォルト値を変更すると、telnetやSSHセッションなど、多数の短いメッセージを扱う処理に、より適切に対応できます。

<a id="entry-3-2-tune-ring-queues"></a>

**`tune.ring.queues <number>`**

```haproxy
tune.ring.queues <number>
```

リングバッファーの前に設ける、書き込みキューの数を設定します。デバッグ中のトレースのCPU使用率に影響する場合があり、値が小さすぎても大きすぎても、大きな影響が生じる可能性があります。適切な値は、開発者が実験で決定しているため、特定の問題への対処を試みるために指示された場合を除き、変更を試みる理由はないはずです。最適な値は時とともに変わる可能性があるため、バージョンアップ後も設定に残すべきではありません。

<a id="entry-3-2-tune-runqueue-depth"></a>

**`tune.runqueue-depth <number>`**

```haproxy
tune.runqueue-depth <number>
```

タスクを実行するとき、一度に処理できるタスク数の上限を設定します。デフォルト値はスレッド数に応じて決まりますが、35から280の範囲にあり、最も高いリクエスト処理速度と、最も小さい遅延が得られる傾向があります。大きくすると、I/Oの処理に遅延が生じる場合があり、小さすぎると、余分なオーバーヘッドが生じる場合があります。スレッド数が多い場合は、小さい値が有利です。かなり大きな値を試す場合は、最大遅延を可能な限り抑えるため、tune.sched.low-latencyと、場合によってはtune.fd.edge-triggeredも有効にすると、役立つ場合があります。

<a id="entry-3-2-tune-sched-low-latency"></a>

**`tune.sched.low-latency { on | off }`**

```haproxy
tune.sched.low-latency { on | off }
```

低遅延タスクスケジューラーを、有効 ('on') または無効 ('off') にします。デフォルトでは、最も効率がよいため、HAProxyは複数のクラスのタスクを、クラスごとにまとめて処理します。しかし、tune.runqueue-depthを大きな値にして実行すると、リクエストや接続の遅延に、測定できるほどの影響が出る場合があります。この低遅延設定を有効にすると、優先度の低いクラスのタスクが存在する場合、常に、ほかのタスクより先に実行します。大量のトラフィックがある中でも、新しいリクエストや接続が受ける最大遅延を減らせますが、その大量のトラフィックへの影響は大きくなります。通常の用途では、無効のままにしておく方が適切です。デフォルト値はoffです。

<a id="entry-3-2-tune-sndbuf-backend"></a>

**`tune.sndbuf.backend  <size>`**

```haproxy
tune.sndbuf.backend  <size>
tune.sndbuf.frontend <size>
```

接続されていないソケットの、カーネルの送信バッファーサイズを、このサイズに固定します。バックエンド側のUNIXソケットとUDPログ、およびフロントエンド側のリスナーモードのQUICに使用できます。システムのデフォルトのバッファーは、多くの接続（またはログ送信元）で共有するソケットには小さすぎる場合があります。その場合、損失や再送が生じる可能性があり、トラフィックが多いときに、新しい接続の確立が遅くなります。値はバイト単位で、各ソケットに適用します。リスナーモードでは、すべての接続でソケットを共有し、ソケットの総数は、"bind" 行の "shards" の値で決まります。一律に適切な値はありません。接続ごとに想定するサイズに、想定する接続数を掛けた値が、適切な値になります。大きな値は、カーネルが縮小する場合があります。接続されたソケットに対応する "tune.sndbuf.client" と "tune.sndbuf.server"、および受信側の設定である "tune.rcvbuf.backend" と "tune.rcvbuf.frontend" も参照してください。

<a id="entry-3-2-tune-sndbuf-client"></a>

**`tune.sndbuf.client <size>`**

```haproxy
tune.sndbuf.client <size>
tune.sndbuf.server <size>
```

クライアント側またはサーバー側の、カーネルのソケット送信バッファーサイズを、指定したバイト数に固定します。すべてのTCP/HTTPフロントエンドとバックエンドに適用します。通常は決して設定すべきではありません。デフォルトのサイズ (0) では、利用できるメモリー量に応じて、カーネルが値を自動調整します。ただし、非常に小さい値（たとえば4096）に設定すると、受信したデータを大量にバッファリングするのを防ぎ、カーネルのメモリーを節約できる場合があります。ただし、値を小さくすると、CPU使用率が大幅に増えます。もう1つの用途は、極端に遅いクライアントで、カーネルがバッファーの大部分を読み取られるまで待ってから、HAProxyに再び通知するために発生する、書き込みタイムアウトを防ぐことです。Linuxで性能を損なわずに、メモリー使用量と応答性を、より細かく制御できる効果的な設定については、tune.notsent-lowat.clientとtune.notsent-lowat.serverも参照してください。

<a id="entry-3-2-tune-ssl-cachesize"></a>

**`tune.ssl.cachesize <number>`**

```haproxy
tune.ssl.cachesize <number>
```

グローバルなSSLセッションキャッシュのサイズを、ブロック数で設定します。ブロックは、ピア証明書を含まない、符号化されたセッションを格納するのに十分な大きさです。ピア証明書を含む、符号化されたセッションは、その証明書のサイズに応じて、複数のブロックに格納します。ブロックは、約200バイトのメモリーを使用します（`sizeof(struct sh_ssl_sess_hdr) + SHSESS_BLOCK_MIN_SIZE` という、`shctx_init` 関数で使用する計算に基づきます）。デフォルト値は、ビルド時に指定できます。指定しなければ、20000です。キャッシュがいっぱいになると、最も長く使用されていないエントリーを削除し、再割り当てします。値を大きくすると、各ユーザーのセッションを可能な限り長く保持できるため、このような削除と、CPU負荷の高いSSLハンドシェイクの回数が減ります。すべてのエントリーは、起動時に事前割り当てします。値を0にすると、SSLセッションキャッシュを無効にします。

<a id="entry-3-2-tune-ssl-capture-buffer-size"></a>

**`tune.ssl.capture-buffer-size <number>`**

```haproxy
tune.ssl.capture-buffer-size <number>
tune.ssl.capture-cipherlist-size <number> (deprecated)
```

Client Helloの暗号リスト、拡張リスト、楕円曲線リスト、楕円曲線点の形式をキャプチャーするために使用する、バッファーの最大サイズを設定します。値が0（デフォルト値）の場合は、キャプチャーを無効にします。それ以外の場合は、SSL/TLS接続ごとにバッファーを割り当てます。

<a id="entry-3-2-tune-ssl-certificate-compression"></a>

**`tune.ssl.certificate-compression { auto | off }`**

```haproxy
tune.ssl.certificate-compression { auto | off }
```

この設定は、TLS 1.3の拡張である、証明書圧縮機能 (RFC 8879) を設定できます。

"auto" に設定すると、TLSライブラリのデフォルト値を使用します。

"off" では、この機能を明示的に無効にしようとします。HAProxyは、圧縮した証明書の送信も、受け入れも試みなくなります。

バックエンド側とフロントエンド側の両方を設定します。

このキーワードは、OpenSSL \>= 3.2.0で対応しています。

デフォルト値はautoです。

<a id="entry-3-2-tune-ssl-default-dh-param"></a>

**`tune.ssl.default-dh-param <number>`**

```haproxy
tune.ssl.default-dh-param <number>
```

DHE鍵交換で、一時的なDiffie-Hellman鍵を生成するために使用する、Diffie-Hellmanパラメーターの最大サイズを設定します。最終的なサイズは、サーバーのRSA（またはDSA）鍵のサイズに合わせようとしますが（たとえば、2048ビットのRSA鍵に対して、2048ビットの一時DH鍵）、この最大値は超えません。1024以上の値だけを指定できます。大きな値はCPU負荷を増やし、1024ビットを超える値には、Java 7以前のクライアントが対応していません。静的なDiffie-Hellmanパラメーターを、証明書ファイル内に直接指定するか、ssl-dh-param-fileパラメーターで指定した場合、この値は使用しません。default-dh-paramとssl-dh-param-fileのどちらも定義せず、対象のフロントエンドのサーバーPEMファイルにも、独自のDHパラメーターを指定しなければ、そのフロントエンドではDHE暗号を使用できません。

<a id="entry-3-2-tune-ssl-force-private-cache"></a>

**`tune.ssl.force-private-cache`**

```haproxy
tune.ssl.force-private-cache
```

このオプションは、すべてのプロセス間でのSSLセッションキャッシュの共有を無効にします。クライアントがランダムなプロセスに到達することで、多数の再ネゴシエーションが必要になるため、通常は使用すべきではありません。ただし、SSLキャッシュの同期方法をいずれも使用できない、一部のOSでは、必要になる場合があります。この場合、SSLの層の手前に、ハッシュに基づくロードバランシングの層を追加すると、セッションを共有できない影響を抑えられる場合があります。

<a id="entry-3-2-tune-ssl-hard-maxrecord"></a>

**`tune.ssl.hard-maxrecord <number>`**

```haproxy
tune.ssl.hard-maxrecord <number>
```

SSL_write()に一度に渡す、バイト数の上限を設定します。デフォルト値の0は、無制限を意味します。tune.ssl.maxrecordとは異なり、この設定は動的には調整しません。レコードを小さくすると、スループットが低下する場合がありますが、メモリー消費量の小さいクライアントを扱う際に、必要になることがあります。

<a id="entry-3-2-tune-ssl-keylog"></a>

**`tune.ssl.keylog { on | off }`**

```haproxy
tune.ssl.keylog { on | off }
```

このオプションは、TLS鍵のログ記録を有効にします。SSLセッションごとのメモリー消費量が増え、性能が低下する可能性があるため、注意して使用すべきです。デフォルトでは無効です。

Wiresharkでトラフィックを復号するために必要なSSLKEYLOGFILEの生成には、これらのサンプル取得関数を使用すべきです。

<https://tlswg.org/sslkeylogfile/draft-ietf-tls-keylogfile.html>

SSLKEYLOGは、次の形式の行が並んだものです。

```text
<Label> <space> <ClientRandom> <space> <Secret>
```

ClientRandomは、サンプル取得関数 %[ssl_fc_client_random,hex] が提供します。secretとLabelは、以下の表で確認できます。この表のすべてのラベルを含むSSLKEYLOGFILEを生成する必要があります。

以下のサンプル取得関数は、16進数の文字列を返すため、変換する必要はありません。

```text
  SSLKEYLOGFILEのラベル           |  シークレットのサンプル取得
  --------------------------------|-----------------------------------------
  CLIENT_EARLY_TRAFFIC_SECRET     |  %[ssl_xx_client_early_traffic_secret]
  CLIENT_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_client_handshake_traffic_secret]
  SERVER_HANDSHAKE_TRAFFIC_SECRET |  %[ssl_xx_server_handshake_traffic_secret]
  CLIENT_TRAFFIC_SECRET_0         |  %[ssl_xx_client_traffic_secret_0]
  SERVER_TRAFFIC_SECRET_0         |  %[ssl_xx_server_traffic_secret_0]
  EXPORTER_SECRET                 |  %[ssl_xx_exporter_secret]
  EARLY_EXPORTER_SECRET           |  %[ssl_xx_early_exporter_secret]
```

これらの取得関数は、フロントエンド (fc) 側とバックエンド (bc) 側にあります。"xx" を "fc" または "bc" に置き換え、適切な側を使用してください。

OpenSSL 1.1.1でのみ利用でき、TLS1.3セッションで役立ちます。

TLS \< 1.3でSSLKEYLOGFILEの内容を生成するには、次の行だけが必要です。

"CLIENT_RANDOM %[ssl_fc_client_random,hex] %[ssl_fc_session_key,hex]"

syslogには理想的ではありませんが、次のようなlog-formatで、完全な鍵ログを生成できます。

```text
log-format "CLIENT_EARLY_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_early_traffic_secret]\n
            CLIENT_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_client_handshake_traffic_secret]\n
            SERVER_HANDSHAKE_TRAFFIC_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_server_handshake_traffic_secret]\n
            CLIENT_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_client_traffic_secret_0]\n
            SERVER_TRAFFIC_SECRET_0 %[ssl_bc_client_random,hex] %[ssl_bc_server_traffic_secret_0]\n
            EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_exporter_secret]\n
            EARLY_EXPORTER_SECRET %[ssl_bc_client_random,hex] %[ssl_bc_early_exporter_secret]"
```

HAProxyは、上記の形式を、"log-format" ディレクティブで直接使用できる、定義済みの環境変数としても提供します。

```shell
$HAPROXY_KEYLOG_FC_LOG_FMT   フロントエンド（クライアント側）の接続鍵
$HAPROXY_KEYLOG_BC_LOG_FMT   バックエンド（サーバー側）の接続鍵
```

<a id="entry-3-2-tune-ssl-keyupdate-rate-limit"></a>

**`tune.ssl.keyupdate-rate-limit <limit>`**

```haproxy
tune.ssl.keyupdate-rate-limit <limit>
```

毎秒受け入れるKeyUpdateの数を `<limit>` に制限し、超えると、フラッドとみなして接続を終了します。KeyUpdateの処理はCPU負荷が高く、大量に受信する理由はほとんどありません。値 "0" を使用すると、レート制限を無効にします。デフォルト値は100です。<a id="entry-3-2-tune-ssl-lifetime"></a>

**`tune.ssl.lifetime <timeout>`**

```haproxy
tune.ssl.lifetime <timeout>
```

キャッシュしたSSLセッションが、有効でいられる時間を設定します。秒単位で表し、デフォルトは300 (5 min) です。キャッシュがいっぱいになると、設定した存続期間に関係なく、最も長く使用されていないセッションを削除するため、その時間だけセッションが維持されることを保証しないと、理解することが重要です。この設定の実際の役割は、セッションを長く使用しすぎることを防ぐことです。

<a id="entry-3-2-tune-ssl-maxrecord"></a>

**`tune.ssl.maxrecord <number>`**

```haproxy
tune.ssl.maxrecord <number>
```

データ転送の開始時に、SSL_write()に渡すバイト数の上限を設定します。デフォルト値の0は、無制限を意味します。SSL/TLSでは、クライアントはレコード全体を受信して初めて、データを復号できます。レコードが大きい場合、処理を開始する前に、最大16kBのデータをダウンロードしなければならないことがあります。値を制限すると、遅延が大きい、または帯域幅の小さいネットワーク上のブラウザーで、ページの読み込み時間が改善する場合があります。SSL/TLSにオーバーヘッドがあることを考慮しながら、1または2 TCPセグメント（通常、EthernetでTCPタイムスタンプを有効にすると1448バイト、無効にすると1460バイト）に収まる、最適な値を見つけることを推奨します。一般的な値である1419と2859は、テストでよい結果が得られました。"strace -e trace=write" を使用して、最適な値を見つけてください。HAProxyは、アイドル状態のストリームを検出すると、自動的にこの設定へ切り替えます（上記のtune.idletimerを参照）。tune.ssl.hard-maxrecordも参照してください。

<a id="entry-3-2-tune-ssl-ssl-ctx-cache-size"></a>

**`tune.ssl.ssl-ctx-cache-size <number>`**

```haproxy
tune.ssl.ssl-ctx-cache-size <number>
```

生成した証明書を格納するキャッシュのサイズを、`<number>` エントリーに設定します。これはLRUキャッシュです。SSL証明書の動的な生成は負荷が高いため、キャッシュします。キャッシュサイズのデフォルトは1000エントリーです。

<a id="entry-3-2-tune-streams-elasticity"></a>

**`tune.streams-elasticity <number>`**

```haproxy
tune.streams-elasticity <number>
```

すべての接続が確立しているときに、最大同時接続数 (maxconn) に対して、フロントエンド接続ごとに割り当てるストリーム数の、目標割合を定義します。この指標は、HTTP/2やQUICなど、各接続が複数のストリームを受け取れる、多重化プロトコルに適用します。常に少なくとも1つを保証するため、割合は100%以上でなければなりません。接続の設定中に、HAProxyは目標の比率を保ちながら、設定した上限まで、追加のストリームを動的に通知します。接続の確立時には、各フロントエンド接続に、少なくとも1つのストリームを割り当てます。追加のストリームは、目標割合と、設定したストリームの上限に基づいて割り当てます。これにより、負荷の変化に応じた、効率的なストリームの割り当てを実現します（負荷が低ければストリームを多くし、高ければ少なくします）。

ページごとのオブジェクトが多い、動的なサイトでは、比率を大きくすると、接続ごとに多くのストリームを使用できるため、有利です。平均して使用するストリームが少ないサイト（WebSocket、アプリケーションコード）では、120や150に近い、小さい比率（接続数より20から50%多いストリーム数）が適している場合があります。負荷が継続する状況で、ストリーム数が過剰になるのを防げます。

デフォルト値は0で、このレベルでは制限を適用しないことを意味します。そのため、H2とQUICの設定だけを適用します（接続ごとに100ストリームというデフォルト設定では、10000%に相当します）。小規模な構成（maxconnが千程度）では、引き続きこの設定を推奨します。中規模の構成（数千から数万の接続）では、通常、比率を1000から5000の間に設定し、最大負荷時に、接続ごとに10から50のストリームを使用できるようにします。大規模な構成（数十万から数百万の接続）では、より小さい値（120から200）を使用し、最大負荷時に、接続ごとに平均1.2から2のストリームを使用できるようにする場合があります。

HTTP/2とは異なり、QUICは、接続の存続期間中に、同時ストリーム数を動的に調整できます。ただし、QUICのフロー制御はHTTP/2より厳格なため、QUICを使用する場合は、接続に余分な遅延が生じないよう、十分に大きな値を指定する方が適切です。また、0-RTTを有効にしたQUICリスナーには、制限があります。この場合、ピアに通知する初期値は、ストリームの弾力的な割り当てを無視し、"tune.quic.fe.stream.max-concurrent" の設定だけに従います。ただし、この初期通知が終わった後、接続の存続期間中は、ストリームの弾力的な割り当てが引き続き機能します。

キュー内のものを含む、バックエンドのアクティブなストリームの総数を監視すると、持続可能な目標負荷の実用的な指標となり、過剰なリソース割り当てを避けるのに役立ちます。

<a id="entry-3-2-tune-stick-counters"></a>

**`tune.stick-counters <number>`**

```haproxy
tune.stick-counters <number>
```

接続またはリクエストが、"tcp-request" または "http-request" ルールの "track-sc\*" アクションで、同時に追跡できるスティックカウンターの数を設定します。デフォルト値は、ビルド時にマクロMAX_SESS_STK_CTRで設定し、標準では3です。この設定で、ビルド時に渡した値を無視して変更できますが、100を超える値には設定できません。複雑な設定をHAProxyへ移植するときに、増やす必要がある場合がありますが、そのコストには注意が必要です。各エントリーは、接続ごとに16バイト、リクエストごとに16バイトを使用します。使用しない場合でも、すべてのリクエストについて、この領域をすべて割り当て、ゼロで初期化する必要があります。そのため、値を10にすると、リクエストごとのメモリー消費量が320バイト増え、リクエストごとにそのメモリーを消去するため、測定できるほどのCPUへの影響があります。一方、"track-sc" ルールを使用しない場合は、値を小さくできます（0も有効で、スティックカウンターを完全に無効にします）。

<a id="entry-3-2-tune-takeover-other-tg-connections"></a>

**`tune.takeover-other-tg-connections <value>`**

```haproxy
tune.takeover-other-tg-connections <value>
```

デフォルトでは、ほかのスレッドグループのアイドル接続を、使用しようとはしません。ただし、この動作は変更できます。`<value>` に指定できる値は、次のとおりです。デフォルトの "none" では、ほかのスレッドグループのアイドル接続を、使用しようとはしません。"restricted" では、reverse httpなど、新しい接続を作成できないプロトコルを使用している場合、またはstrict-maxconnを使用している場合にのみ、ほかのスレッドからアイドル接続を取得しようとします。"full" では、常に、ほかのスレッドグループでアイドル接続を探します。ほかのスレッドグループの接続を使用すると、性能が低下する場合があるため、本当に必要な場合以外は使用すべきではありません。現在、この動作はtune.idle-pool.sharedが制御します。このキーワードは、古い設定との互換性のためだけに残しており、今後、非推奨にする予定です。

<a id="entry-3-2-tune-vars-global-max-size"></a>

**`tune.vars.global-max-size <size>`**

```haproxy
tune.vars.global-max-size <size>
tune.vars.proc-max-size <size>
tune.vars.reqres-max-size <size>
tune.vars.sess-max-size <size>
tune.vars.txn-max-size <size>
```

これら5つの調整設定は、変数システムが使用するメモリー量の上限を管理するのに役立ちます。"global" は、すべてのスコープで使用できるメモリーの総量を制限します。"proc" はプロセススコープ、"sess" はセッションスコープ、"txn" はトランザクションスコープ、"reqres" は各リクエストまたはレスポンスの処理で使用するメモリーを制限します。メモリーの集計は階層的であり、広い範囲の上限には、狭い範囲の使用量を含めます。つまり、"proc" は "sess" を、"sess" は "txn" を、"txn" は "reqres" を含みます。

たとえば、"tune.vars.sess-max-size" を100に制限すると、"tune.vars.txn-max-size" と "tune.vars.reqres-max-size" も、100を超えられません。100バイトを含む変数 "txn.var" を作成すると、使用できる領域をすべて消費します。実行時に上限を超えても、エラーメッセージは出ませんが、値が切り詰められたり、破損したりする可能性がある点に注意してください。そのため、すべての変数を格納するのに必要な領域を、必ず正確に見積もってください。

<a id="entry-3-2-tune-zlib-memlevel"></a>

**`tune.zlib.memlevel <number>`**

```haproxy
tune.zlib.memlevel <number>
```

各ストリームのzlib初期化時に使用する、memLevelパラメーターを設定します。圧縮処理の内部状態に、どの程度のメモリーを割り当てるかを定義します。値1は、メモリー使用量が最小ですが、速度が遅く、圧縮率も下がります。値9は、最適な速度のために、最大のメモリーを使用します。1から9までの値を指定できます。デフォルト値は8です。

<a id="entry-3-2-tune-zlib-windowsize"></a>

**`tune.zlib.windowsize <number>`**

```haproxy
tune.zlib.windowsize <number>
```

各ストリームのzlib初期化パラメーターとして、ウィンドウサイズ（履歴バッファーのサイズ）を設定します。値を大きくすると、メモリー使用量が増える代わりに、圧縮率が向上します。8から15までの値を指定できます。デフォルト値は15です。

## 3.3. デバッグ {#section-3-3}

<a id="entry-3-3-anonkey"></a>

**`anonkey <key>`**

```haproxy
anonkey <key>
```

グローバルな匿名化キーを `<key>` に設定します。キーは、0から4294967295までの、32ビットの数値でなければなりません。匿名化モードを有効にした場合、CLIコマンドがデフォルトで使用するキーです。実行時に、CLIコマンド "set anon global-key" で設定することもできます。管理マニュアルの、コマンドライン引数 "-dC" も参照してください。

<a id="entry-3-3-debug-counters"></a>

**`debug.counters { on | off }`**

```haproxy
debug.counters { on | off }
```

コード内のイベントカウンターの更新を、有効 ('on') または無効 ('off') にします。CLIコマンド "debug counters" で、種類 "CNT" として表示するカウンターです。これらのカウンターは、DEBUG_COUNTERSを1以上に設定してビルドした場合にのみ利用できます。値1では、デフォルトでカウンターを更新せず（"debug.counters off"）、値2では、デフォルトで更新します（"debug.counters on"）。通常は、開発者に依頼された場合や、異常に多くのCPUを消費していると疑われる場合を除き、変更する理由はありません（後者の場合は、カウンターのダンプを添えて、開発者に報告する必要があります）。CLIコマンド "debug counters" で、実行時に状態を変更することもできます。管理マニュアルを参照してください。

<a id="entry-3-3-force-cfg-parser-pause"></a>

**`force-cfg-parser-pause <timeout>`**

```haproxy
force-cfg-parser-pause <timeout>
```

このコマンドは、設定パーサーを `<timeout>` ミリ秒間、一時停止します。開発や、初期化スクリプトのタイムアウトのテスト、特に、非常に長いリロードを模擬する場合に役立ちます。expose-experimental-directivesを設定する必要があります。

`<timeout>` は、デフォルトではミリ秒単位で指定する、タイムアウト値です。ただし、この文書の冒頭で説明したように、数値に単位を付けると、ほかの単位でも指定できます。

例:

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

メモリーオブジェクトとリスナーの解放を省略し、リロード時の古いプロセスの終了を速めます。これらはすべて、プロセスの終了時にOSが回収するためです。改善はわずかです（非常に大きな設定でも、せいぜい数百ミリ秒程度）。実際の主な用途は、deinit()コードに不具合が見つかった場合に、それを回避することです。開発者から指示されない限り、使用しない方が適切です。

<a id="entry-3-3-quiet"></a>

**`quiet`**

```haproxy
quiet
```

起動時にメッセージを一切表示しません。コマンドライン引数 "-q" と同じです。

<a id="entry-3-3-warn-blocked-traffic-after"></a>

**`warn-blocked-traffic-after <time>`**

```haproxy
warn-blocked-traffic-after <time>
```

動けなくなったタスクがトラフィックをブロックしている場合に、標準エラー出力へ警告を出すまでの、待ち時間を調整できます。待ち時間はミリ秒単位で表し、デフォルトは100 msです。指定できる値は、1 ms以上1000 ms以下でなければなりません。小さい値では警告が頻繁に出て、大きい値ではまれにしか出ません。いずれにしても、ウォッチドッグは、1秒間応答しない状態が2回続く暴走タスクを終了するため、1000 msの待ち時間では、通常、警告は出ません。長い応答時間や、対話型セッションのぎこちない動きなど、ユーザー体験を損なう可能性がある、設定の異常を検出するため、10から100msの間の値を使用することを推奨します。たとえば、重い計算を行う、設計の不適切なLuaのサンプル取得関数や、評価コストが非常に高い、巨大なmap_regまたはmap_regmのマップファイルが、こうした問題を引き起こす場合があります。比較すると、TLSハンドシェイクは1から2ミリ秒、16kBのHTTPレスポンスバッファーの圧縮は約1ミリ秒かかる場合があります。出力には、問題を起こしたタスクのスレッドダンプと、バックトレース、時間を費やしている場所の特定に役立つコンテキストを含みます。

<a id="entry-3-3-zero-warning"></a>

**`zero-warning`**

```haproxy
zero-warning
```

このオプションを設定すると、HAProxyは、設定の処理と適用中に警告が出た場合、起動を拒否します。つまり、パラメーターの不適切な組み合わせや、設定できなかった非常に高い上限などに関する警告があると、プロセスは起動中にエラーで終了します。起動の遅い段階で出る、一部の警告は検出できません。たとえば、"daemon" モードや "master-worker" モードでグループIDを変更するときに、補助グループの破棄に失敗した場合や、fork()後にプロセスをダンプ可能に設定できなかった場合です。実行時に出る警告も検出しません。微妙な誤りの検出や、明快で将来のバージョンにも対応できる設定の維持に役立つため、頻繁に変更しない設定では、このオプションを指定することを強く推奨します。このような場合、"haproxy -c" もエラーを報告する点に注意してください。このオプションは、コマンドライン引数 "-dW" と同じです。

## 3.4. HTTPClientの調整 {#section-3-4}

HTTPClientは、内部のHTTPライブラリです。さまざまなサブシステムから、たとえばLuaスクリプト内で使用できます。HTTPClientはデータの転送経路では使用しません。つまり、HAProxyを通過するHTTPトラフィックとは関係ありません。

<a id="entry-3-4-httpclient-resolvers-disabled"></a>

**`httpclient.resolvers.disabled <on|off>`**

```haproxy
httpclient.resolvers.disabled <on|off>
```

httpclientのDNS名前解決を無効にします。"default" resolversセクションを作成しないようにします。

デフォルト値はoffです。

<a id="entry-3-4-httpclient-resolvers-id"></a>

**`httpclient.resolvers.id <resolvers id>`**

```haproxy
httpclient.resolvers.id <resolvers id>
```

このオプションは、httpclientが名前解決を試みるために使用する、resolversセクションを定義します。

デフォルトの選択は、resolvers ID "default" です。このオプションを使用しないデフォルトの場合は、セクションが見つからなければ、単に名前解決を無効にします。

一方、このオプションを明示的に有効にした場合は、読み込みに失敗すると、設定エラーになります。

<a id="entry-3-4-httpclient-resolvers-prefer"></a>

**`httpclient.resolvers.prefer <ipv4|ipv6>`**

```haproxy
httpclient.resolvers.prefer <ipv4|ipv6>
```

このオプションは、名前解決で使用したいIPファミリーを選択できます。ネットワークでIPv6を使用できない場合に便利です。デフォルトの選択は "ipv6" です。

<a id="entry-3-4-httpclient-retries"></a>

**`httpclient.retries <number>`**

```haproxy
httpclient.retries <number>
```

このオプションは、リクエストが失敗した場合に、httpclientが再試行する回数を設定できます。backendの "retries" キーワードと同じ動作です。

デフォルト値は3です。

<a id="entry-3-4-httpclient-ssl-ca-file"></a>

**`httpclient.ssl.ca-file <cafile>`**

```haproxy
httpclient.ssl.ca-file <cafile>
```

このオプションは、サーバー証明書の検証に使用する、ca-fileを定義します。server行の "ca-file" オプションと、同じパラメーターを受け付けます。

このオプションを使用しないデフォルトの場合、値は "@system-ca" で、システムのCAを読み込もうとします。失敗すると、httpclientのSSLを無効にします。

一方、このオプションを明示的に有効にした場合は、失敗すると設定エラーになります。

<a id="entry-3-4-httpclient-ssl-verify"></a>

**`httpclient.ssl.verify [none|required]`**

```haproxy
httpclient.ssl.verify [none|required]
```

server行のverifyオプションと同じ動作です。'none' を指定すると、サーバー証明書を検証しません。デフォルトの選択は "required" です。

このオプションを使用しないデフォルトの場合、値は "required" です。失敗すると、httpclientのSSLを無効にします。

一方、このオプションを明示的に有効にした場合は、失敗すると設定エラーになります。

<a id="entry-3-4-httpclient-timeout-connect"></a>

**`httpclient.timeout.connect <timeout>`**

```haproxy
httpclient.timeout.connect <timeout>
```

httpclientの接続試行について、デフォルトの最大待ち時間を設定します。

引数:

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          このドキュメントの冒頭で説明したように、数値の末尾に単位を付けることで
          他の単位でも指定できます。
```

デフォルト値は5000msです。
