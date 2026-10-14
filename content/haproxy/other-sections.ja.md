---
title: "12. その他のセクション"
linkTitle: "12. その他のセクション"
weight: 230
description: "トレース、ユーザー、メール送信先、エラー、リング、証明書、ACME、グローバルヘルスチェック"
icon: fa-solid fa-ellipsis
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/other-sections/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 12"
---



以下のセクションは使用頻度が低く、通常は少数のパラメーターだけをサポートします。セクション同士に暗黙の関係はありません。いずれも単一のキーワードで開始します。"global"セクションより前に置くことはできません。SSL関連など、一部のサポートはビルドオプションによる場合があります。

## 12.1. トレース {#section-12-1}


デバッグのために、HAProxyのサブシステムでトレースを有効にできます。特定のサブシステムのデバッグメッセージを出力する、問題の診断に非常に有効なツールです。トレースはCLIで動的に設定できます。また、専用の"traces"セクションで、一部の設定を設定ファイルにあらかじめ定義できます。詳しくは管理ガイドを参照してください。あくまで複雑なデバッグ作業で使う開発者向けツールです。出力が多く、負荷もあるため、慎重に使ってください。開発者向けツールであるため、このセクションの後方互換性は保証しません。

<a id="entry-12-1-traces"></a>


**`traces`**


```haproxy
traces
```


新しいtracesセクションを開始します。"traces"セクションは一つでも複数でも構いません。すべてのディレクティブを宣言順に評価し、後の指定が前の指定を上書きします。

<a id="entry-12-1-trace"></a>


**`trace <source> <args...>`**


```haproxy
trace <source> <args...>
```


"trace"サブシステムを設定します。それぞれを管理マニュアルで説明しており、構文もまったく同じです。"trace"コマンドが生成する出力は、このセクションの解析時に出力します。通常はエラーや警告ですが、一部の不完全なコマンドは、指定可能な選択肢を一覧表示する場合があります。このコマンドは通常の利用を想定しておらず、一般には、複雑なデバッグ作業中に開発者が使用を勧めます。トレースレベルや詳細度によっては、有効化により全体の性能が大幅に低下することを覚えておいてください。文の構文は管理マニュアルを参照してください。

例：

```text
ring buf1
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h1.traces

ring buf2
  size 10485760 # 10MB
  format timed
  backing-file /tmp/h2.traces

traces
  trace h1 sink buf1 level developer verbosity complete start now
  trace h2 sink buf1 level developer verbosity complete start now
```


## 12.2. ユーザー一覧 {#section-12-2}


認証と認可を受けたユーザーだけを許可することで、frontend/backend/listenセクションやhttp統計へのアクセスを制御できます。そのためには、少なくとも一つのuserlistを作成し、ユーザーを定義する必要があります。

<a id="entry-12-2-userlist"></a>


**`userlist <listname>`**


```haproxy
userlist <listname>
```


`<listname>`という名前の新しいuserlistを作成します。独立した顧客の認証・認可データを保存するため、複数の独立したuserlistを使えます。

<a id="entry-12-2-group"></a>


**`group <groupname> [users <user>,<user>,(...)]`**


```haproxy
group <groupname> [users <user>,<user>,(...)]
```


現在のuserlistにグループ`<groupname>`を追加します。"users"キーワードに続けて、名前をカンマで区切った一覧を指定すると、このグループにユーザーを所属させることもできます。

<a id="entry-12-2-user"></a>


**`user <username> [password|insecure-password <password>]`**


```haproxy
user <username> [password|insecure-password <password>]
                [groups <group>,<group>,(...)]
```


現在のuserlistにユーザー`<username>`を追加します。安全な（暗号化された）パスワードと、安全でない（暗号化されていない）パスワードの両方を使えます。暗号化パスワードはcrypt(3)関数で評価するため、システムの機能に応じて対応アルゴリズムが異なります。たとえば、現在のGlibcベースのLinuxは、MD5、SHA-256、SHA-512に加えて、従来のDESによるパスワード暗号化方式もサポートします。

注意：暗号化パスワードを使うと、リクエスト数とアルゴリズムによってはCPU使用率が大幅に増えることがあります。ハッシュを使う方式では、各リクエストのパスワードを、設定ファイルの値と比較する前に、選択したアルゴリズムで処理しなければなりません。現在のほとんどのアルゴリズムは、総当たり攻撃に耐えるため、意図的に計算コストを高くしています。平文パスワードにソルトを付けて一度ハッシュするだけでなく、何千回も繰り返します。これはすぐにHAProxy全体のCPU消費の大きな要因となり、アプリケーションのクラッシュを招くことさえあります。

ハッシュ関数の高いCPU使用率への対処方法として、ハッシュ関数のラウンド数（SHA系アルゴリズム）を減らすか、対応するアルゴリズムなら関数の"cost"を下げる方法があります。

補足として、musl（Alpine Linuxなど）の実装は、ハッシュ計算でglibcの実装より遅いことが知られているため、この点も考慮するとよいでしょう。

すべてのパスワードは通常の引数として扱うため、[セクション2.2](/ja/haproxy/configuration-basics/#section-2-2)の引用とエスケープの規則が適用されます。したがって、パスワードを単一引用符で囲むことを推奨します。

例：

```text
userlist L1
  group G1 users tiger,scott
  group G2 users xdb,scott

  user tiger password $6$k6y3o.eP$JlKBx9za9667qe4(...)xHSwRv6J.C0/D7cV91
  user scott insecure-password 'elgato'
  user xdb insecure-password 'hello'

userlist L2
  group G1
  group G2

  user tiger password $6$k6y3o.eP$JlKBx(...)xHSwRv6J.C0/D7cV91 groups G1
  user scott insecure-password 'elgato' groups G1,G2
  user xdb insecure-password 'hello' groups G2
```


両方の一覧は、機能的に同じである点に注意してください。

## 12.3. メール送信先 {#section-12-3}


サーバーの状態が変わると、メールでアラートを送信できます。設定すると、mailersセクションで指定した各送信先へアラートを送ります。メールはLuaを通じて送信します（examples/lua/mailers.luaを参照）。

<a id="entry-12-3-mailers"></a>


**`mailers <mailersect>`**


```haproxy
mailers <mailersect>
```


`<mailersect>`という名前の新しいメール送信先一覧を作成します。一つ以上のプロキシから参照する、独立したセクションです。

<a id="entry-12-3-mailer"></a>


**`mailer <mailername> <ip>:<port>`**


```haproxy
mailer <mailername> <ip>:<port>
```


mailersセクション内にメール送信先を定義します。

例：

```text
global
    # mailers.lua file as provided in the git repository
    # adjust path as needed
    lua-load examples/lua/mailers.lua

mailers mymailers
    mailer smtp1 192.168.0.1:587
    mailer smtp2 192.168.0.2:587

backend mybackend
    mode tcp
    balance roundrobin

    email-alert mailers mymailers
    email-alert from test1@horms.org
    email-alert to test2@horms.org

    server srv1 192.168.0.30:80
    server srv2 192.168.0.31:80
```


<a id="entry-12-3-timeout-mail"></a>


**`timeout mail <time>`**


```haproxy
timeout mail <time>
```


メール／接続を作成し、メールサーバーへ送信するために使える時間を定義します。未指定の場合、デフォルトは10秒です。最初のTCPハンドシェイクで少なくとも二つのSYN-ACKパケットを送れるよう、この値を4秒より大きくすることを推奨します。

例：

```text
mailers mymailers
    timeout mail 20s
    mailer smtp1 192.168.0.1:587
```


## 12.4. HTTPエラー {#section-12-4}


HTTPエラーのグループをグローバルに複数宣言し、後で任意のプロキシセクションに取り込めます。同じグループを複数箇所から参照でき、全体でも一部だけでも取り込めます。

<a id="entry-12-4-http-errors"></a>


**`http-errors <name>`**


```haproxy
http-errors <name>
```


`<name>`という名前の新しいhttp-errorsグループを作成します。一つ以上のプロキシが名前で参照できる、独立したセクションです。

<a id="entry-12-4-errorfile"></a>


**`errorfile <code> <file>`**


```haproxy
errorfile <code> <file>
```


ファイルの内容をHTTPエラーコードに関連付けます。

引数：

```text
<code>    HTTPステータスコードです。現在、HAProxyが生成できるのは、
          200、400、401、403、404、405、407、408、410、425、429、500、
          501、502、503、504です。

<file>    完全なHTTPレスポンスを含むファイルを指定します。HTMLのエラーページと
          混同しないよう、一般的な慣例に従い、ファイル名に".http"を付けることを
          推奨します。また、ファイルはchrootの前に読み込むため、絶対パスを
          推奨します。
```


詳細は[セクション4](/ja/haproxy/proxies/)の"errorfile"キーワードを参照してください。

例：

```text
http-errors website-1
    errorfile 400 /etc/haproxy/errorfiles/site1/400.http
    errorfile 404 /etc/haproxy/errorfiles/site1/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug

http-errors website-2
    errorfile 400 /etc/haproxy/errorfiles/site2/400.http
    errorfile 404 /etc/haproxy/errorfiles/site2/404.http
    errorfile 408 /dev/null  # work around Chrome pre-connect bug
```


## 12.5. リング {#section-12-5}


ログサーバーやトレースの出力先として使う、リングバッファーをグローバルに宣言できます。

<a id="entry-12-5-ring"></a>


**`ring <ringname>`**


```haproxy
ring <ringname>
```


`<ringname>`という名前の新しいリングバッファーを作成します。

<a id="entry-12-5-backing-file"></a>


**`backing-file <path>`**


```haproxy
backing-file <path>
```


リングの保存先を、通常のメモリ割り当てから、RAMにマッピングしたファイルに置き換えます。低速なクライアントをCLIに接続せずに、事後解析用のトレースやログを収集するのに便利です。新しい内容が古い内容を自動的に置き換えるため、常に最新の内容を利用できます。リングに書き込んだ内容は、プロセスの停止後にファイルから見えるようになります（通常は書き込み後すぐに見えますが、同期書き込みではないため保証はありません）。

このオプションを使うと、保存領域の先頭に置く"struct ring"のサイズ分だけ、利用可能な総領域が減ります。この構造体は内容の復元に必要です。ファイルは、起動ユーザーの所有権、モード0600、"size"ディレクティブで設定したサイズで作成します。ディレクティブの解析時（したがって設定チェック時にも）、既存の空でないファイルは、まず接尾辞".bak"を付けた名前に変更し、以前の".bak"ファイルは削除します。これにより、プロセスを即座にリロードや再起動しても、貴重なデバッグ情報を消さずに済み、管理者が新しい".bak"ファイルを見つけて、必要なら保管する時間を確保できます。したがって、クラッシュ直後は`<path>`のファイルに最新情報があり、サービスを再起動した後は"`<path>`.bak"にあります。必要な総保存容量はリングサイズの倍になります。ファイルのローテーション失敗は黙って無視するため、バックアップファイルが不要なら、書き込み権限のないディレクトリーにファイルを置くだけで防げます。

警告：この機能は安定性とセキュリティに影響します。第一に、低速なデバイス（物理ハードディスクなど）をリングの保存先にすると、アクセス時に体感できる遅延が生じ、多数のスレッドが競合するとパニックさえ起こる可能性があります。第二に、外部プロセスが領域を変更すると、haproxyがクラッシュしたり、自身のメモリの一部をトレースで上書きしたりする可能性があります。第三に、リングが埋まる前にファイルシステムが満杯になると、リングへの書き込みでプロセスがクラッシュする場合があります。

このリング内の情報は構造化されており、テキストエディターで直接読めるものではありません（大部分がかろうじて読めそうに見えても同じです）。このファイルの出力は、開発者だけを対象としています。

<a id="entry-12-5-description"></a>


**`description <text>`**


```haproxy
description <text>
```


リングの説明を指定する任意の文字列です。CLIに表示します。デフォルトでは、このフィールドに`<name>`を再利用します。

<a id="entry-12-5-format"></a>


**`format <format>`**


```haproxy
format <format>
```


リングバッファーにイベントを保存する形式です。

引数：

```text
<format> syslogメッセージの生成時に使うログ形式です。次のいずれかです。

  iso     ISO形式の日付と、その後のテキストだけを含むメッセージです。
          PID、プロセス名、システム名は省略します。ローカルのログサーバーで
          使うことを想定しています。

  local   rfc3164のsyslogメッセージ形式と同様ですが、hostnameフィールドを
          除去します。デフォルトです。
          注意："log-send-hostname"で、デフォルトをrfc3164に切り替えます。

  raw     テキストだけを含むメッセージです。レベル、PID、日付、時刻、
          プロセス名、システム名は省略します。コンテナー内や開発中など、
          重要度が使用するファイルディスクリプター（stdout/stderr）だけで
          決まる場合を想定しています。デフォルトです。

  rfc3164 RFC3164のsyslogメッセージ形式です。
          (https://tools.ietf.org/html/rfc3164)

  rfc5424 RFC5424のsyslogメッセージ形式です。
          (https://tools.ietf.org/html/rfc5424)

  short   '<3>'のように山括弧で囲んだレベルと、その後のテキストだけを
          含むメッセージです。PID、日付、時刻、プロセス名、システム名は
          省略します。ローカルのログサーバーで使うことを想定しています。
          systemdのロガーが受け付ける形式と互換性があります。

 priority '<63>'のようにレベルとsyslog facilityを組み合わせて山括弧で囲んだ値と、
          その後のテキストだけを含むメッセージです。PID、日付、時刻、
          プロセス名、システム名は省略します。ローカルのログサーバーで
          使うことを想定しています。

  timed   '<3>'のように山括弧で囲んだレベルと、その後のISO形式の日付、
          テキストだけを含むメッセージです。PID、プロセス名、システム名は
          省略します。ローカルのログサーバーで使うことを想定しています。
```


<a id="entry-12-5-maxlen"></a>


**`maxlen <length>`**


```haproxy
maxlen <length>
```


形式を整えたヘッダーを含め、リングに保存するイベントメッセージの最大長です。`<length>`より長いメッセージは、その長さに切り詰めます。

<a id="entry-12-5-server"></a>


**`server <name> <address> [param*]`**


```haproxy
server <name> <address> [param*]
```


リングバッファーからメッセージを転送するsyslog TCPサーバーを設定します。5.2にあるすべての"server"パラメーターをサポートしますが、一部は"ring"セクションには関係しません。重要なのは、一つのリングに複数のサーバーを追加する理由はほとんどないことです。すべてのサーバーがリング内容のまったく同じコピーを受け取るため、リングは最も遅いサーバーの速度で進みます。一つでも応答しないサーバーがあると、古いメッセージを削除できず、新しいメッセージをリングへ挿入できなくなることがあります。複数のサーバーへ送る正しい方法は、同じリングに複数のサーバーを接続することではなく、ログサーバーごとに別のリングを使うことです。送信プロトコルの設定には、専用のサーバーディレクティブ"log-proto"を使います。

<a id="entry-12-5-size"></a>


**`size <size>`**


```haproxy
size <size>
```


リングバッファーのサイズをバイトで指定します。任意で、デフォルトはBUFSIZEです。

<a id="entry-12-5-timeout-connect"></a>


**`timeout connect <timeout>`**


```haproxy
timeout connect <timeout>
```


サーバーへの接続試行が成功するまで待つ時間の上限を設定します。

引数：

```text
<timeout> タイムアウト値です。デフォルトではミリ秒ですが、この文書の冒頭で
          説明したとおり、数値に単位を付ければ、他の単位でも指定できます。
```


<a id="entry-12-5-timeout-server"></a>


**`timeout server <timeout>`**


```haproxy
timeout server <timeout>
```


送信待ちのデータが出力バッファーにとどまる時間の上限を設定します。

引数：

```text
<timeout> タイムアウト値です。デフォルトではミリ秒ですが、この文書の冒頭で
          説明したとおり、数値に単位を付ければ、他の単位でも指定できます。
```


例：

```text
global
    log ring@myring local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    server mysyslogsrv 127.0.0.1:6514 log-proto octet-count
```


## 12.6. ログ転送 {#section-12-6}


ログ転送セクションを一つ以上宣言できます。HAProxyは、受信したすべてのログメッセージを、ログサーバーの一覧へ転送します。

<a id="entry-12-6-log-forward"></a>


**`log-forward <name>`**


```haproxy
log-forward <name>
```


`<name>`で識別する新しいログ転送プロキシを作成します。

<a id="entry-12-6-backlog"></a>


**`backlog <conns>`**


```haproxy
backlog <conns>
```


接続を受け入れる際の、希望するリッスンバックログのおおよそのサイズを、システムへ示します。

<a id="entry-12-6-bind"></a>


**`bind <addr> [param*]`**


```haproxy
bind <addr> [param*]
```


転送対象のメッセージを受信する、ストリームログリスナーを設定します。5.1の"bind"パラメーターをSSL関連も含めてサポートしますが、"alpn"などはTCP上のsyslogには関係しない場合があります。リスナーは、rfc-6587で定義する"Octet Counting"と"Non-Transparent-Framing"の両モードをサポートします。

<a id="entry-12-6-dgram-bind"></a>


**`dgram-bind <addr> [param*]`**


```haproxy
dgram-bind <addr> [param*]
```


転送対象のメッセージを受信する、データグラムログリスナーを設定します。アドレスはIPv4またはIPv6形式で、その後にポートが必須です。5.1の"bind"パラメーターのうち、"interface"、"namespace"、"transparent"などをサポートします。それ以外はUDP/syslogには関係しないため、黙って無視します。

<a id="entry-12-6-log-global"></a>


**`log global`**


```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    <facility> [<level> [<minlevel>]]
```


転送先のログサーバーを設定します。詳細はプロキシのドキュメントを参照してください。形式を指定しない場合、HAProxyは受信ログの形式を維持しようとします。設定したfacilityは、受信メッセージにfacilityがなく、送信形式で必須である場合を除き、無視します。入力形式にタイムスタンプがなく、出力形式にそのフィールドがある場合、HAProxyはローカルの日付を使います。

例：

```text
global
   log stderr format iso local7

ring myring
    description "My local buffer"
    format rfc5424
    maxlen 1200
    size 32764
    timeout connect 5s
    timeout server 10s
    # syslog tcp server
    server mysyslogsrv 127.0.0.1:514 log-proto octet-count

log-forward sylog-loadb
    dgram-bind 127.0.0.1:1514
    bind 127.0.0.1:1514
    # all messages on stderr
    log global
    # all messages on local tcp syslog server
    log ring@myring local0
    # load balance messages on 4 udp syslog servers
    log 127.0.0.1:10001 sample 1:4 local0
    log 127.0.0.1:10002 sample 2:4 local0
    log 127.0.0.1:10003 sample 3:4 local0
    log 127.0.0.1:10004 sample 4:4 local0
```


<a id="entry-12-6-maxconn"></a>


**`maxconn <conns>`**


```haproxy
maxconn <conns>
```


ログ転送プロキシの同時接続数の上限を設定します。デフォルトは10です。

<a id="entry-12-6-timeout-client"></a>


**`timeout client <timeout>`**


```haproxy
timeout client <timeout>
```


クライアント側の最大無通信時間を設定します。

<a id="entry-12-6-option-assume-rfc6587-ntf"></a>


**`option assume-rfc6587-ntf`**


```haproxy
option assume-rfc6587-ntf
```


受信するTCPログストリームを、常に非透過フレーミングとして扱うようHAProxyに指示します。フレーミング処理を単純化し、メッセージを一貫して扱えるようにします。特に、先頭文字が正しく形成されていない場合に便利です。

<a id="entry-12-6-option-dont-parse-log"></a>


**`option dont-parse-log`**


```haproxy
option dont-parse-log
```


syslogメッセージを解析・再構成せずに中継します。従来の形式に従わないメッセージの転送に便利です。元のメッセージ内容を保持するため、転送先ログターゲットのformat raw設定と併用するべきです。

<a id="entry-12-6-option-host"></a>


**`option host { replace | fill | keep | append }`**


```haproxy
option host { replace | fill | keep | append }
```


送信するrfc3164またはrfc5424メッセージのsyslog hostnameフィールドについて、log-forwardセクションで使うホスト処理方針を設定します。

      replace 入力メッセージのhostnameフィールドに値がある場合は、
              送信者の送信元IPアドレスで置き換えます。
              hostnameフィールドに値がない場合（rfc5424入力が'-'の場合や、
              rfc3164またはrfc5424に準拠しないメッセージの場合）も、
              送信者の送信元IPアドレスをhostnameフィールドに使います。

      fill    入力メッセージのhostnameフィールドに値がある場合は、維持します。
              値がない場合（rfc5424入力が'-'の場合や、rfc3164またはrfc5424に
              準拠しないメッセージの場合）は、送信者の送信元IPアドレスを
              hostnameフィールドに使います。
              （デフォルトです）


      keep    入力メッセージのhostnameフィールドに値がある場合は、維持します。
              値がない場合は、'localhost'（rfc3164）または'-'（rfc5424）に設定します。

      append  入力メッセージのhostnameフィールドに値がある場合は、
              カンマと、それに続けて送信者のIPアドレスを追加します。
              値がない場合は、送信者の送信元IPアドレスを使います。

上記のすべてのオプションで、送信者の送信元IPアドレスを取得できない場合（UNIX/ABNSソケットなど）は、結果的に"keep"の方針になります。

このオプションが関係するのは、転送先のログ形式がrfc3164またはrfc5424の場合だけです。それ以外では、設定しても見える効果はありません。

## 12.7. 証明書ストレージ {#section-12-7}


HAProxyは、設定で使う証明書を読み込み、保持するため、内部ストレージ機構を使います。"crt-store"セクションで、証明書の定義と、そこへ読み込むファイルを設定できます。証明書の定義は、設定内の他の場所で使うより前に記述しなければなりません。

crt-store [`<name>`]

"crt-store"は、任意で名前を引数に取ります。名前を指定した場合、そのストアの各証明書は、"@`<name>`/`<crt>`"または"@`<name>`/`<alias>`"で参照しなければなりません。

証明書ストレージ内のファイルは、CLIで動的に更新することもできます。管理ガイドの[セクション9.3](/ja/haproxy/statistics-and-monitoring/#section-9-3)にある"set ssl cert"を参照してください。

"crt-store"セクションは、次のキーワードをサポートします。

- crt-base
- key-base
- load

<a id="entry-12-7-crt-base"></a>


**`crt-base <dir>`**


```haproxy
crt-base <dir>
```


"crt"ディレクティブに相対パスを使う場合、SSL証明書を取得するデフォルトのディレクトリーを指定します。絶対パスを指定すると、そちらを優先し、"crt-base"を無視します。crt-store内で使う場合は、globalセクションのcrt-baseを無視します。

<a id="entry-12-7-key-base"></a>


**`key-base <dir>`**


```haproxy
key-base <dir>
```


"key"ディレクティブに相対パスを使う場合、SSL秘密鍵を取得するデフォルトのディレクトリーを指定します。絶対パスを指定すると、そちらを優先し、"key-base"を無視します。crt-store内で使う場合は、globalセクションのkey-baseを無視します。

<a id="entry-12-7-load"></a>


**`load [crt <filename>] [param*]`**


```haproxy
load [crt <filename>] [param*]
```


証明書ストレージにSSLファイルを読み込みます。パラメーター一覧は「12.7.1. 読み込みオプション」を参照してください。

例：

```text
crt-store
    load crt "site1.crt" key "site1.key" ocsp "site1.ocsp" alias "site1"
    load crt "site2.crt" key "site2.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"

crt-store web
    crt-base /etc/ssl/certs/
    key-base /etc/ssl/private/
    load crt "site3.crt" alias "site3"
    load crt "site4.crt" key "site4.key"

frontend in2
    bind *:443 ssl crt "@/site1" crt "site2.crt"  crt "@web/site3" crt "@web/site4.crt"
```


### 12.7.1. 読み込みオプション {#section-12-7-1}


証明書ストレージにSSLファイルを読み込みます。loadキーワードは、以下に示す複数のパラメーターを取れます。これらのキーワードはcrt-listでも使えます。

<a id="entry-12-7-1-crt"></a>


**`crt <filename>`**


```haproxy
crt <filename>
```


必須の引数で、PEMを読み込みます。PEMには公開証明書が必須で、中間証明書や秘密鍵を含めることもできます。このファイルに秘密鍵がない場合は、"key"キーワードで指定できます。

<a id="entry-12-7-1-acme"></a>


**`acme <string>`**


```haproxy
acme <string>
```


指定した証明書のACMEプロトコルを設定します。実験的機能で、globalセクションに"expose-experimental-directives"が必要です。

crt-storeで"acme"キーワードを使うと、ディスク上に既存の証明書がなくても起動できます。ACME証明書を生成するまで、代わりに一時的な鍵ペアを使います。この動作はcrt-store専用で、crt-list行やssl-f-use行では、先にcrt-storeを宣言しない限り、同じことはできません。

[セクション12.8](/ja/haproxy/other-sections/#section-12-8)（"ACME"）と、このセクションの"domains"も参照してください。

<a id="entry-12-7-1-alias"></a>


**`alias <string>`**


```haproxy
alias <string>
```


任意の引数です。証明書に別名を付け、設定内でその名前で参照できるようにします。設定内の他の場所から別名を呼び出す場合は、接頭辞'@/'を付けなければなりません。

<a id="entry-12-7-1-domains"></a>


**`domains <string>`**


```haproxy
domains <string>
```


ACME証明書で使うドメインの一覧を設定します。最初のドメインをCNに使います。一覧ではドメインをカンマで区切ります。

[セクション12.8](/ja/haproxy/other-sections/#section-12-8)（"ACME"）と、このセクションの"acme"も参照してください。

例：

```text
load crt "example.com.pem" acme LE domains "bar.example.com,foo.example.com"
```


<a id="entry-12-7-1-ips"></a>


**`ips <string>`**


```haproxy
ips <string>
```


ACME証明書にIP SANとして含めるIPアドレスの一覧を設定します。一覧ではIPアドレスをカンマで区切ります。

IPアドレスを含む証明書の生成には、"shortlived"プロファイルが必要な場合があります。

[セクション12.8](/ja/haproxy/other-sections/#section-12-8)（"ACME"）と、このセクションの"acme"、"domains"も参照してください。

例：

```text
load crt "server.pem" acme LE ips "192.0.2.1,2001:db8::1"
```


<a id="entry-12-7-1-key"></a>


**`key <filename>`**


```haproxy
key <filename>
```


任意の引数です。PEM形式の秘密鍵を読み込みます。"crt"ですでに秘密鍵を定義している場合は、上書きします。

<a id="entry-12-7-1-ocsp"></a>


**`ocsp <filename>`**


```haproxy
ocsp <filename>
```


任意の引数で、DER形式のOCSPレスポンスを読み込みます。CLIで更新できます。

<a id="entry-12-7-1-issuer"></a>


**`issuer <filename>`**


```haproxy
issuer <filename>
```


任意の引数です。PEM形式のOCSP発行者証明書を読み込みます。OCSPレスポンスがどの証明書に適用されるかを識別するには、発行者の証明書が必要です。"crt"ファイルにない場合は、この引数で別のファイルから読み込めます。

<a id="entry-12-7-1-sctl"></a>


**`sctl <filename>`**


```haproxy
sctl <filename>
```


任意の引数です。Certificate Transparency（RFC6962）のTLS拡張を有効にします。ファイルには、RFCで規定する有効なSigned Certificate Timestamp Listが必須です。基本構文を確認するためにファイルを解析しますが、署名は検証しません。

<a id="entry-12-7-1-ocsp-update"></a>


**`ocsp-update [ off | on ]`**


```haproxy
ocsp-update [ off | on ]
```


'on'でOCSPレスポンスの自動更新を有効にし、それ以外で無効にします。デフォルトは'off'です。bind行でOCSP自動更新を有効にするには、crt-storeのこのオプション、またはglobalオプション"tune.ocsp-update.mode"を使えます。同じ証明書を複数のcrt-listで使い、'ocsp-update'の値が異なる場合は、エラーになります。同様に、bind行でglobalオプションを継承する証明書に、crt-listで互換性のない'ocsp-update'を明示的に設定した場合も、同じエラーになります。

例：

crt-listで有効にする設定例です。

haproxy.cfg:

```text
frontend fe
    bind :443 ssl crt-list haproxy.list
```


haproxy.list:

```text
server_cert.pem [ocsp-update on] foo.bar
```


crt-storeで有効にする設定例です。

haproxy.cfg:

```text
crt-store
  load crt foobar.pem ocsp-update on

frontend fe
    bind :443 ssl crt foobar.pem
```


このオプションが'on'の場合、フロントエンドの証明書にOCSP URIが見つかるたびに、OCSPレスポンスの取得を試みます。このモードの唯一の制限は、OCSP certidを構築するために、証明書の発行者が分かっている必要があることです。各OCSPレスポンスを少なくとも一時間に一度更新し、有効期限がその一時間より早い場合は、さらに頻繁に更新します。ただし、有効期間が非常に短いレスポンスや、'Next Update'がまったくないレスポンスを更新しすぎないよう、最短更新間隔は5分です。この固定の下限により、自動更新が'on'の場合、初期化時に読み込んだOCSPレスポンスは、期限がnow+5mより前でも、少なくとも5分経過するまで更新しません。初期化時に読み込むレスポンスは有効でなければならず（有効期限が未来であること）、初期化後のそれほど短い時間に期限切れになる可能性は低いため、通常は大きな問題にはならないはずです。一方、OCSP URIがあり、OCSPレスポンスがない証明書では、このオプションを'on'にすると、初期化直後に自動取得します。デフォルトの最短・最長間隔（それぞれ5分と1時間）は、globalオプション"ocsp-update.maxdelay"と"ocsp-update.mindelay"で設定できます。

自動更新タスク、またはCLIの"update ssl ocsp-response"によってOCSPレスポンスを更新するたびに、専用のログ行を出力します。専用形式のヘッダー"`<OCSP-UPDATE>`"に続けて、対応するフロントエンド証明書のパス、数値の更新ステータス、テキストの更新ステータス、そのレスポンスの更新失敗回数、更新成功回数というOCSP固有の情報を出力します。エラーコードとメッセージの全一覧は、CLIの"show ssl ocsp-updates"を参照してください。この行は、更新の成功・失敗にかかわらず出力します。OCSPリクエスト／レスポンスは、dontlog-normalを設定したhttp_clientインスタンスで送受信し、OCSPレスポンダーに到達できない場合などのエラー時には、通常のHTTPログ形式を使います。そのようなエラーが起きると、通常のOCSPログ（テキストステータスはおそらく"HTTP error"）とともに、HTTP関連情報を含む別のログ行を出力します。つまり、OCSPレスポンダーに到達できない場合など、純粋なHTTPエラーでは、通常のHTTPログ形式の行も追加で出力します。以下に、まずOCSP更新に成功したログ行、次に異なる二行を含むHTTPエラーの例を示します（読みやすさのため、行を分割し、URLを短くしています）。

```text
<133>Mar  6 11:16:53 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/foo.pem 1 \
        "Update successful" 0 1

<133>Mar  6 11:18:55 haproxy[14872]: <OCSP-UPDATE> /path_to_cert/bar.pem 2 \
        "HTTP error" 1 0
<133>Mar  6 11:18:55 haproxy[14872]: -:- [06/Mar/2023:11:18:52.200] \
        <OCSP-UPDATE> -/- 2/0/-1/-1/3009 503 217 - - SC-- 0/0/0/0/3 0/0 {} \
        "GET http://127.0.0.1:12345/MEMwQT HTTP/1.1"
```


トラブルシューティング：Let's Encrypt証明書でよくあるエラーとして、DNSがIPv6アドレスを返すのに、システムに有効な送信用IPv6ルートがない場合があります。その場合は、適切なルートを作成するか、globalセクションに"httpclient.resolvers.prefer ipv4"を設定できます。"OCSP response check failure"の場合は、指定した発行者証明書が有効か確認してください。「汎用的な」エラーメッセージの後の括弧内に、さらに詳しいメッセージが表示されることもあります。"OCSP response check failure"や"Error during insertion"で起こり得ます。

<a id="entry-12-7-1-jwt"></a>


**`jwt [ off | on ]`**


```haproxy
jwt [ off | on ]
```


'on'にすると、この証明書を"jwt_verify_cert"、"jwt_decrypt_cert"、"jwt_decrypt"コンバーターによるJWT検証または復号に使えます。デフォルトは'off'です。

証明書で'on'にすると、CLIの"del ssl cert"は動作しません。証明書を削除するには、SSLハンドシェイクにもJWT検証にも使われていない必要があります。

このオプションは、CLIの"add ssl jwt"と"del ssl jwt"で実行時に変更できます。"show ssl jwt"も参照してください。

<a id="entry-12-7-1-generate-dummy"></a>


**`generate-dummy [ off | on ]`**


```haproxy
generate-dummy [ off | on ]
```


'on'にすると、解析時に秘密鍵とその自己署名証明書を生成できます。たとえば、テスト中に使える証明書がない場合に便利です。"keytype"、"bits"、"curves"で秘密鍵を調整できます。未指定時のデフォルトは'off'です（"keytype"、"bits"、"curves"も参照）。

<a id="entry-12-7-1-keytype"></a>


**`keytype [ RSA | ECDSA ]`**


```haproxy
keytype [ RSA | ECDSA ]
```


解析時に自己署名証明書を生成するための秘密鍵の型を選べます。その証明書で"generate-dummy"を'on'にした場合に使います。未指定時のデフォルトは'RSA'です（"generate-dummy"も参照）。

<a id="entry-12-7-1-bits"></a>


**`bits <number>`**


```haproxy
bits <number>
```


自己署名証明書で"generate-dummy"が'on'、"keytype"が'RSA'の場合、RSA自己署名証明書を生成するビット数を設定します。未指定時のデフォルトは2048です（"generate-dummy"も参照）。

<a id="entry-12-7-1-curves"></a>


**`curves <string>`**


```haproxy
curves <string>
```


自己署名証明書で"generate-dummy"が'on'、"keytype"が'ECDSA'の場合、曲線を設定します。デフォルトは'P-384'です。

## 12.8. ACME {#section-12-8}


acme `<name>`

ACMEプロトコルは"acme"セクションで設定できます。セクションは"`<name>`"を引数に取り、証明書をこのセクションに関連付けるために使います。

ACMEセクションでは、HAProxyをACMEv2クライアントとして設定できます。実験的機能であるため、使うにはglobalセクションに"expose-experimental-directives"が必須です。

HAProxyのwikiにガイドがあります。
<https://github.com/haproxy/wiki/wiki/ACME:--native-haproxy>

現在の制限： <a id="entry-12-8-the-feature-is"></a>

**`- 現在、この機能が対応するチャレンジはhttp-01、dns-01、dns-persist-01に限られます`**


```haproxy
- 現在、この機能が対応するチャレンジはhttp-01、dns-01、dns-persist-01に限られます
```


http-01はHAProxyがすべて処理しますが、dns-01とdns-persist-01には、DNSプロバイダーのAPIと通信するため、dataplaneAPIまたは別のサードパーティーツールが必要です。dns-persist-01ではTXTエントリーを一度設定すればよいため、ツールを使わず手動で設定することもできます。
<a id="entry-12-8-it-is-possible"></a>


**`- ディスク上に既存の証明書がなくても起動できます。そのためには、`**


```haproxy
- ディスク上に既存の証明書がなくても起動できます。そのためには、
```


証明書をcrt-storeで設定しなければなりません。crt-storeで"acme"キーワードを使うと、ACME証明書を生成するまで一時的な鍵ペアを使います。
<a id="entry-12-8-the-current-haproxy"></a>


**`- 現在のHAProxyのアーキテクチャーはノンブロッキングモデルであり、ディスクへのアクセスは`**


```haproxy
- 現在のHAProxyのアーキテクチャーはノンブロッキングモデルであり、ディスクへのアクセスは
```


設定の読み込み後には行わない前提です。イベントループをブロックし、同じスレッドのトラフィックを止める可能性があるためです。つまり、HAProxyが生成した証明書と鍵は、外部から統計ソケットの"dump ssl cert"を使って書き出す必要があります。dataplaneAPI、またはadmin/cli/ディレクトリーにあるhaproxy-dump-certsスクリプトで、証明書の書き出しを自動化できます。

ACMEスケジューラーはHAProxyの起動時に開始し、証明書を順に確認します。notAfterがcurtime + (notAfter - notBefore) / 12を過ぎた場合、またはnotBeforeが未定義なら7日を基準に、ACME更新タスクを開始します。その後、スケジューラーは休止し、12時間後に起動します。"acme renew"で更新タスクを手動で開始することもできます。管理ガイドの"acme status"も参照してください。

ACMEセクションでは、次のキーワードを使えます。

<a id="entry-12-8-account-key"></a>


**`account-key <filename>`**


```haproxy
account-key <filename>
```


アカウント鍵のパスを設定します。鍵はHAProxyの起動前に生成する必要があります。accountキーワードがなければ、acmeセクションは、セクション名を使った"`<name>`.account.key"を読み込もうとします。ファイルがなければ、acmeセクションのパラメーターを使ってHAProxyが生成します。

opensslでRSA秘密鍵を手動生成することもできます。

```text
openssl genrsa -out account.key 2048
```


ECDSA鍵の場合：

```text
openssl ecparam -name secp384r1 -genkey -noout -out account.key
```


<a id="entry-12-8-acme-vars"></a>


**`acme-vars <string>`**


```haproxy
acme-vars <string>
```


外部のDNS設定ツール（dataplaneAPIなど）へ、"dpapi"出力先を通じて任意の変数を渡します。意味はツール固有なので、DNS設定ツールのドキュメントを参照してください。

このキーワードが意味を持つのは、チャレンジの型が"dns-01"または"dns-persist-01"の場合だけです。

関連項目："challenge"、"provider-name"

<a id="entry-12-8-bits"></a>


**`bits <number>`**


```haproxy
bits <number>
```


RSA証明書を生成するビット数を設定します。デフォルトは2048です。マシンの性能に対して大きすぎる値を設定すると、警告が出る場合があります（"warn-blocked-traffic-after"で設定できますが、トラフィックを長時間ブロックするとwatchdogが作動する可能性があります）。

<a id="entry-12-8-challenge"></a>


**`challenge <string>`**


```haproxy
challenge <string>
```


チャレンジの型を引数に取り、http-01、dns-01、dns-persist-01のいずれかでなければなりません。未指定時のデフォルトはhttp-01です。

dns-persist-01はdraft-ietf-acme-dns-persistを実装します。dns-01とは異なり、"\_validation-persist.`<domain>`"に静的なTXTレコードを使います。一度設定すれば、更新のたびに変わることはありません。レコードにはアカウントURIが必須で、任意のポリシーも含められます。このチャレンジでは、更新のたびにDNSプロバイダーAPIへの書き込み権限を必要としません。

<a id="entry-12-8-challenge-ready"></a>


**`challenge-ready <value>[,<value>]*`**


```haproxy
challenge-ready <value>[,<value>]*
```


dns-01チャレンジの検証準備ができたことをACMEサーバーへ通知する前に、満たさなければならない条件を設定します。次の値を指定できます。

```text
cli  - マスターCLIまたは統計ソケットのCLIコマンド
       "acme challenge_ready <crt> domain <domain>"で、オペレーターが
       準備完了を通知するのを待ちます。これにより、HAProxyが先へ進む前に、
       外部のDNS設定ツールがTXTレコードを設定済みであることを確認できます。

dns  - 権威ネームサーバーではなく、設定した"default" resolversセクションで
       "_acme-challenge.<domain>"のTXTレコードを解決し、DNSの事前確認を
       行います。TXTレコードが期待するトークンと一致するまで、チャレンジを
       送信しません。したがって、リゾルバー側のDNSキャッシュの影響を受ける
       場合があります。解決試行の間隔は"dns-delay"で制御します。
       CLIコマンドとは独立しており、人の操作は不要です。

       dns-01では、"_acme-challenge.<domain>"のTXTレコードを解決し、
       期待するトークンと一致しなければなりません。dns-persist-01では、
       "_validation-persist.<domain>"のTXTレコードを解決し、
       存在することだけを確認します。

delay - 先へ進む前に、"dns-delay"だけ最初に待ちます。"dns"がなければ、
        遅延時間が過ぎた後にチャレンジを送信します。"dns"と組み合わせると、
        DNS事前確認を開始する前に、最初の待ち時間を適用します。

none - 準備完了の条件を設けず、外部の確認を待たずに、ACMEサーバーへ
       直ちにチャレンジを送信します。他の条件とは組み合わせられません。
```


複数の値をカンマで組み合わせられます。複数の条件を指定した場合、まずCLIの確認（"cli"）を待ち、次に最初の遅延（"delay"）を適用し、最後にDNS事前確認（"dns"）を行います。

このオプションは、dns-01とdns-persist-01のチャレンジだけに対応します。

"challenge"が"dns-01"で、このオプションを設定しない場合、デフォルトは"cli"です。

"challenge"が"dns-persist-01"で、このオプションを設定しない場合、デフォルトは"dns,delay"です。

"challenge"が"dns-persist-01"の場合、challenge-ready条件を評価する前に、まず、すぐに先へ進めるかを判断するDNS確認を必ず行います。"\_validation-persist.`<domain>`"のTXTレコードは一度設定すれば更新の間も変わらないため、HAProxyは更新時に、そのレコードがすでに存在するかを確認します。すべてのドメインで成功すると、challenge-readyの手順（cli、delay、dns）を経ずに、直ちにチャレンジを送信します。確認に失敗すると、通常のchallenge-readyの流れに戻ります。

例：

```shell
# Wait for CLI confirmation, then verify DNS propagation
challenge-ready cli,dns
```


<a id="entry-12-8-contact"></a>


**`contact <string>`**


```haproxy
contact <string>
```


CA内でアカウント鍵に関連付ける連絡先メールアドレスです。

<a id="entry-12-8-curves"></a>


**`curves <string>`**


```haproxy
curves <string>
```


鍵の型がECDSAの場合に、曲線を設定します。デフォルトはP-384です。

<a id="entry-12-8-directory"></a>


**`directory <string>`**


```haproxy
directory <string>
```


このacmeセクションが使うCAのディレクトリーURLを設定します。デフォルトURLがないため、必須です。

例：

```text
directory https://acme-staging-v02.api.letsencrypt.org/directory
```


<a id="entry-12-8-dns-delay"></a>


**`dns-delay <time>`**


```haproxy
dns-delay <time>
```


"challenge-ready"の"delay"条件と"dns"条件で使う遅延を設定します。値は、HAProxyの時間形式（"5m"、"300s"など）で指定します。デフォルトは30秒です。

役割は、使う"challenge-ready"条件によって異なります。

```text
delay     - DNS事前確認を行わず、この遅延時間が過ぎた後にチャレンジを送信します。

dns       - 連続するDNS解決試行の間隔です。
            初回の確認は、最初の待ち時間を設けず、直ちに行います。

dns+delay - 初回のDNS解決試行までの待ち時間と、その後の再試行の間隔です。
```


名前解決は権威ネームサーバーではなく、設定した"default" resolversセクションを通じて行います。したがって、リゾルバー側のDNSキャッシュの影響が残る場合があります。

<a id="entry-12-8-dns-timeout"></a>


**`dns-timeout <time>`**


```haproxy
dns-timeout <time>
```


"challenge-ready"に"dns"を含める場合、チャレンジを中止する前にTXTレコードの解決に成功するまでの制限時間を設定します。値は、HAProxyの時間形式（"10m"、"600s"など）で指定します。デフォルトは600秒です。

タイマーは、最初の"dns-delay"の後、初回のDNS解決を開始した時点から動きます。次の解決試行がタイムアウト後になる場合、エラーとしてチャレンジを中止します。これにより、DNSの伝播に失敗しても、再試行が無限に続くことを防ぎます。

関連項目："dns-delay"

<a id="entry-12-8-keytype"></a>


**`keytype <string>`**


```haproxy
keytype <string>
```


生成する鍵の型を設定します。"RSA"または"ECDSA"を指定できます。ECDSAの"curves"と、RSAの"bits"数も設定できます。デフォルトではEC384鍵を生成します。

<a id="entry-12-8-map"></a>


**`map <map>`**


```haproxy
map <map>
```


トークン（キー）とサムプリント（値）を保存するマップを設定します。複数のアカウントを使う場合、チャレンジへ応答するのに便利です。acmeタスクは、チャレンジの検証前にエントリーを追加し、タスクの終了時に削除します。

<a id="entry-12-8-profile"></a>


**`profile <string>`**


```haproxy
profile <string>
```


newOrderリクエストに"profile"フィールドを含め、CAへ特定の証明書プロファイルを要求します。draft-ietf-acme-profilesを実装します。

プロファイル名は、CA固有の短い識別子（"classic"、"shortlived"など）です。設定すると、名前をそのままnewOrderのJSONペイロードで送信します。CAは、そのプロファイルに未対応なら、要求を無視することも、エラーを返すこともできます。未設定ならprofileフィールドを含めず、CAはデフォルトの発行ポリシーを使います。

Let's Encryptのプロファイルについては、<https://letsencrypt.org/docs/profiles/>を参照してください。

例：

```shell
# Request short-lived certificates
profile shortlived
```


<a id="entry-12-8-provider-name"></a>


**`provider-name <string>`**


```haproxy
provider-name <string>
```


外部のDNS設定ツール（dataplaneAPIなど）へ"dpapi"出力先を通じて渡す、DNSプロバイダー名を設定します。受け付ける値はツール固有なので、DNS設定ツールのドキュメントを参照してください。

このキーワードが意味を持つのは、チャレンジの型が"dns-01"または"dns-persist-01"の場合だけです。

関連項目："challenge"、"acme-vars"

<a id="entry-12-8-reuse-key"></a>


**`reuse-key { on | off }`**


```haproxy
reuse-key { on | off }
```


"on"にすると、HAProxyは新しい秘密鍵を生成せず、以前の鍵を保持します。秘密鍵のローテーションを推奨します。このオプションを有効にする場合は、定期的に手動で鍵を再生成することを推奨します。

2048を超えるRSA鍵は生成に時間がかかり、生成中のスレッドを遅くする可能性があるため、その場合に便利です。

ACMEサーバーのキャッシュを使う場合、同じ鍵の利用が役立つことがあります。現在の鍵に対応する有効な証明書を取得しやすくなります。

デフォルト設定は"off"です。

例：

```text
global
    expose-experimental-directives
    httpclient.resolvers.prefer ipv4

frontend in
    bind *:80
    bind *:443 ssl
    http-request return status 200 content-type text/plain lf-string "%[path,field(-1,/)].%[path,field(-1,/),map(virt@acme)]\n" if { path_beg '/.well-known/acme-challenge/' }
    ssl-f-use crt "foo.example.com.pem.rsa"   acme LE1 domains "foo.example.com.pem,bar.example.com"
    ssl-f-use crt "foo.example.com.pem.ecdsa" acme LE2 domains "foo.example.com.pem,bar.example.com"

acme LE1
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype RSA
    bits 2048
    map virt@acme

acme LE2
    directory https://acme-staging-v02.api.letsencrypt.org/directory
    account-key /etc/haproxy/letsencrypt.account.key
    contact john.doe@example.com
    challenge http-01
    keytype ECDSA
    curves P-384
    map virt@acme
```


<a id="entry-12-8-eab-key-id"></a>


**`eab-key-id <filename>`**


```haproxy
eab-key-id <filename>
```


EAB鍵IDファイルのパスを設定します。認証情報はCAが提供し、HAProxyを起動する前に、指定したパスに置かなければなりません。アカウント作成時にだけ使います。

ファイルには、プレーンなASCII文字列が必須です。

EAB認証情報が必要なのは、ACMEアカウントの初回作成時だけです。その後は、設定から削除するか、ファイルを空にできます。空のファイルは黙って無視します。末尾の改行以外の空白文字は無視しません。

関連項目："eab-mac-key"、"eab-mac-alg"

<a id="entry-12-8-eab-mac-key"></a>


**`eab-mac-key <filename>`**


```haproxy
eab-mac-key <filename>
```


EAB MAC鍵ファイルのパスを設定します。認証情報はCAが提供し、HAProxyを起動する前に、指定したパスに置かなければなりません。アカウント作成時にだけ使います。

ファイルには、base64urlで符号化したMAC鍵が必須です。

EAB認証情報が必要なのは、ACMEアカウントの初回作成時だけです。その後は、設定から削除するか、ファイルを空にできます。空のファイルは黙って無視します。末尾の改行以外の空白文字は無視しません。

関連項目："eab-key-id"、"eab-mac-alg"

<a id="entry-12-8-eab-mac-alg"></a>


**`eab-mac-alg { HS256 | HS384 | HS512 }`**


```haproxy
eab-mac-alg { HS256 | HS384 | HS512 }
```


EAB署名に使うMACアルゴリズムを設定します。デフォルトはHS256です。EAB MAC鍵は、指定したMACアルゴリズムをサポートできる十分な長さが必要です。すべてのCAがHS256以外のアルゴリズムに対応するわけではありません。

関連項目："eab-key-id"、"eab-mac-key"

## 12.9. ヘルスチェック {#section-12-9}


設定全体のサーバーから利用できるヘルスチェックを、グローバルに複数宣言できます。ローカルのプロキシ設定を上書きします。

<a id="entry-12-9-healthcheck"></a>


**`healthcheck <name>`**


```haproxy
healthcheck <name>
```


`<name>`という名前の新しいヘルスチェックを作成します。名前は一意でなければなりません。特定のhealth-checkセクションを参照するため、server行でこの名前を使います。

<a id="entry-12-9-type"></a>


**`type <type>`**


```haproxy
type <type>
```


ヘルスチェックの型を定義します。必須のパラメーターです。次の型をサポートします。

    * tcp-check
    * httpchk
    * ssl-hello-chk
    * smtpchk
    * pgsql-check
    * redis-check
    * mysql-check
    * ldap-check
    * spop-check

各型は、対応するプロキシオプションにパラメーターがあれば、同じものを使います。たとえば"httpchk"では、メソッドやURIなどを指定できます。

例：

```text
   healthcheck my-http-check
type httpchk GET /health HTTP/1.1 %[srv_name]
```


関連項目："option tcp-check"、"option httpchk"、"option ssl-hello-chk"、"option smtpchk"、"option mysql-check"、"option pgsql-check"、"option redis-check"、"option ldap-check"、"option spop-check"

<a id="entry-12-9-http-check-comment"></a>


**`http-check comment <string>`**


```haproxy
http-check comment <string>
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
http-check disable-on-404
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
http-check send-state
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
http-check unset-var(<var-name>)
```


"httpchk"ヘルスチェックに、個別のhttp-checkルールを追加します。対応するプロキシディレクティブと同じ構文を使います。詳細は、対応するプロキシのドキュメントを参照してください。

<a id="entry-12-9-tcp-check-comment"></a>


**`tcp-check comment <string>`**


```haproxy
tcp-check comment <string>
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
tcp-check unset-var(<var-name>)
```


"tcp-check"ヘルスチェックに、個別のtcp-checkルールを追加します。対応するプロキシディレクティブと同じ構文を使います。詳細は、対応するプロキシのドキュメントを参照してください。
