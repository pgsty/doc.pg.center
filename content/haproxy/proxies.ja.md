---
title: "4. プロキシ"
linkTitle: "4. プロキシ"
weight: 150
description: "デフォルト設定、フロントエンド、バックエンド、リスナー、プロキシキーワード、アクションのリファレンス"
icon: fa-solid fa-right-left
module: [HAPROXY]
categories: [リファレンス]
aliases:
  - /haproxy/configuration/proxies/
upstream_link: "https://docs.haproxy.org/3.4/configuration.html"
upstream_name: "HAProxy 3.4 Configuration Manual"
upstream_ref: "v3.4.6-66-g16acce1dac1d, chapter 4"
---

プロキシの設定は、次のセクションに記述できます。

- defaults [`<name>`] [ from `<defaults_name>` ]
- frontend `<name>` [ from `<defaults_name>` ]
- backend `<name>` [ from `<defaults_name>` ]
- listen `<name>` [ from `<defaults_name>` ]

"frontend"セクションは、クライアント接続を受け付けるリッスンソケットの集合を記述します。

"backend"セクションは、受け付けた接続を転送するためにプロキシが接続するサーバーの集合を記述します。

"listen"セクションは、フロントエンドとバックエンドの両方を1つのセクションにまとめた完全なプロキシを定義します。通常、TCPのみのトラフィックに有用です。

"defaults"セクションは、すべての設定をドキュメント記載の値にリセットし、後続のセクションで使う新しい値をあらかじめ設定します。"frontend"、"backend"、"listen"の各セクションは、必ずdefaultsセクションから初期設定を取得します。デフォルトでは、新しく作成するセクションより前に現れる最後のdefaultsセクションを使います。セクション行の任意のキーワード"from"の後に名前を指定すれば、初期設定の取得元となる特定の"defaults"セクションを明示できます。"defaults"セクションに名前は必須ではありませんが、読みやすさのために名前を付けることを推奨します。また、デフォルトの直前のセクション以外を指定するには、名前を付ける必要があります。"defaults"セクションの名前は任意なので、デフォルトの名前チェックは非常に緩く、重複も許されます。ただし、"defaults"セクションがほかのセクションから参照される場合、その名前はすべてのプロキシ名に課される構文に従い、defaultsセクション間で一意でなければなりません。現在何が許されているかにかかわらず、一般にセクション名の重複を避け、プロキシ名と同じ構文に従うことを推奨します。将来のバージョンでは、この規則が強制される可能性があります。また、defaultsセクションをあるプロキシが明示的に使用し、同時に別のプロキシが最後に定義されたセクションとして暗黙的に使用すると、警告が出ます。常に明示的な参照を使うか、暗黙的な使用専用の共通defaultsセクションを最後に追加して、両方の使い方を混在させないことを強く推奨します。

defaultsセクション自体が別のdefaultsセクションから初期設定を取得し、複数階層にわたって設定を継承することも可能です。これは、デフォルト設定の組をまとめた設定プロファイル（TCP用とHTTP用、短いタイムアウト用と長いタイムアウト用など）を作るのに便利ですが、継承関係がすぐに追いにくくなることがあります。

デフォルトでは、名前付きdefaultsセクションは設定解析後も保持されます。これにより、バックエンドを動的に作成するときに再利用できます。この動作は"tune.defaults.purge"キーワードでグローバルに変更できます。

すべてのプロキシ名は、英大文字と英小文字、数字、'-'（ダッシュ）、'\_'（アンダースコア）、'.'（ドット）、':'（コロン）で構成しなければなりません。ACL名は大文字と小文字を区別するため、"www"と"WWW"は異なるプロキシです。

従来は、一定の条件（フロントエンド／バックエンドの機能が同じでない場合など）を満たせば、プロキシ名の重複が認められていました。しかし、ログに多くの問題を生じさせ、CLI操作、スティックテーブルの命名、統計情報の取得にも混乱を招いていました。現在は、それぞれの機能にかかわらず、2つのプロキシには異なる名前を付ける必要があります。

現在、主に2つのプロキシモードをサポートしています。レイヤー4とも呼ばれる"tcp"と、レイヤー7とも呼ばれる"http"です。レイヤー4モードでは、HAProxyは両端の間で双方向のトラフィックを単に転送します。レイヤー7モードでは、HAProxyがプロトコルを解析し、任意の条件に基づいてリクエストやレスポンスの任意の内容を許可、ブロック、切り替え、追加、変更、削除できます。

HTTPモードでは、接続上を流れるリクエストとレスポンスに適用する処理は、フロントエンドとバックエンドのHTTPオプションの組み合わせによって決まります。HAProxyは3つの接続モードをサポートしています。

- KAL：接続維持（"option http-keep-alive"）。デフォルトのモードです。すべてのリクエストとレスポンスを処理し、レスポンスから次のリクエストまでの間も接続を開いたままアイドル状態に保ちます。

- SCL：サーバー側を切断（"option http-server-close"）。レスポンスの終わりを受信するとサーバー側の接続を閉じますが、クライアント側の接続は開いたままにします。

- CLO：切断（"option httpclose"）。レスポンスの終わりで接続を閉じ、両方向に"Connection: close"を付加します。

フロントエンドとバックエンドを通過する接続に実際に適用されるモードは、次の表に従い両方のプロキシのモードから決まります。要するに、モードの関係は対称であり、接続維持が最も弱く、切断が最も強いオプションです。

                   バックエンドのモード

```text
                | KAL | SCL | CLO
            ----+-----+-----+----
            KAL | KAL | SCL | CLO
            ----+-----+-----+----
   モード     SCL | SCL | SCL | CLO
            ----+-----+-----+----
            CLO | CLO | CLO | CLO
```

TCPフロントエンドをHTTPバックエンドにつなぐことも可能です。HTTPトラフィックだけを扱う場合には意味がありませんが、同じフロントエンドで複数のプロトコルを扱うために使えます。この場合、クライアント接続はまず生のTCP接続として処理され、その後HTTPにアップグレードされます。アップグレード前は、生データに対してコンテンツ処理を実行します。アップグレード後は、データを解析してHTXと呼ばれる内部表現で保存するため、生の表現には依存できなくなります。元に戻す方法はありません。

アップグレードには、その場で行うアップグレードと、ストリームを破棄するアップグレードの2種類があります。前者はTCPからHTTP/1へのアップグレードです。HTTP/1ではリクエスト処理が直列に行われるため、アプリケーションストリームを維持できます。後者はTCPからHTTP/2へのアップグレードです。HTTP/2は多重化プロトコルなので、アプリケーションストリームをどのHTTP/2ストリームにも対応付けられず、破棄されます。その後、HAProxyが下位層のH2マルチプレクサーで新しいHTTP/2ストリームを受信すると、新しいアプリケーションストリームが作成されます。この違いによってデータの処理方法が大きく変わるため、理解しておくことが重要です。HTTP/1へのアップグレードでは、生データに対してすでに行ったコンテンツ処理が失われたり再実行されたりすることはありません。一方、HTTP/2へのアップグレードでは、アプリケーションストリームが別々になり、各ストリームに対してすべてのフロントエンドルールが必ず評価されます。また、前述のとおり最初のTCPストリームは破棄されますが、それはフロントエンドルールが評価された後です。

TCPプロキシからHTTP処理を行う際には、もう1つ重要な点があります。HAProxyはtcp-request contentルールからHTTP/1をその場で解析できますが、HTTP/2ではできません。解析できるのはHTTP/2のプリフェイスだけです。これは、TCPでHTTPコンテンツを解析するうえで大きな制約です。具体的には、受信データがHTTPかどうかしか分かりません。たとえば、HTTP/1では簡単にできるHostヘッダーの値に基づくバックエンドの選択ができません。ただし、この欠点を緩和する方法はあります。

HTTPへのアップグレード方法は2つあります。従来からの方法は、HTTPバックエンドを選択することです。バックエンドが設定されるとアップグレードが行われます。このため、その場で行うアップグレードでは、HTTPデータ処理にバックエンドの設定だけが考慮されます。ストリームを破棄するアップグレードでは、アプリケーションストリームが破棄されるため、その処理は停止します。この方法では、前述のとおりHTTP/2接続でバックエンドを選択する際にできることが非常に限られ、ストリームが破棄されるため、あまり意味もありません。もう1つの方法は、"switch-mode http"アクションを使い、tcp-request contentルールの評価中にアップグレードすることです。この場合、フロントエンドのコンテキストでアップグレードするため、そのフロントエンドでHTTPディレクティブを定義できます。その場で行うアップグレードでは、できるだけ早い段階からHTTP解析のすべての機能を使えます。HTTPフロントエンドに近い動作です。ストリームを破棄するアップグレードでは、限られた情報からバックエンドを選んでも意味がない点を除き、何も変わりません。当然、この方法を推奨します。したがって、tcp-request contentルールでリクエストのプロトコルを調べ、HTTPへアップグレードするだけで十分です。残りのHTTP操作はすべて、フロントエンドのhttp-requestルールセットに移せます。ただし、tcp-request contentルールが各ストリームで引き続き評価されることは変えられません。

## 4.1. プロキシキーワード一覧表 {#section-4-1}

以下のキーワードをサポートしています。多くは、限られた種類のセクションでのみ使用できます。一部のキーワードは、分かりにくい、または機能に制限のある古い構文を引き継いでおり、代わりに推奨される新しいキーワードがあるため、"deprecated"（非推奨）と記されています。"(\*)"の付いたキーワードは、"no option contstats"のように"no"を前に付けて、任意に意味を反転できます。これは、デフォルトで有効なオプションを特定のインスタンスで無効にする必要がある場合に役立ちます。また、これらのオプションには"default"を前に付けることもでき、先行する"defaults"セクションでの指定にかかわらずデフォルト設定に戻せます。defaultsセクションでサポートされ、"(!)"の付いたキーワードは、名前付きdefaultsセクションでのみ使用でき、名前のないセクションでは使用できません。

注意：危険で推奨されない一部のディレクティブは、以下の表には意図的に掲載していません。これらのディレクティブの説明自体はありますが、表から除外することも、使用を思いとどまらせるための手段です。

```text
 キーワード                              defaults   frontend   listen    backend
------------------------------------+----------+----------+---------+---------
acl                                       X (!)      X         X         X
backlog                                   X          X         X         -
balance                                   X          -         X         X
be-unpublished                            -          -         X         X
bind                                      -          X         X         -
capture cookie                            -          X         X         -
capture request header                    -          X         X         -
capture response header                   -          X         X         -
clitcpka-cnt                              X          X         X         -
clitcpka-idle                             X          X         X         -
clitcpka-intvl                            X          X         X         -
compression                               X          X         X         X
cookie                                    X          -         X         X
crt                                       -          X         X         -
declare capture                           -          X         X         -
default-server                            X          -         X         X
default_backend                           X          X         X         -
description                               -          X         X         X
disabled                                  X          X         X         X
dispatch                    (deprecated)  -          -         X         X
email-alert from                          X          X         X         X
email-alert level                         X          X         X         X
email-alert mailers                       X          X         X         X
email-alert myhostname                    X          X         X         X
email-alert to                            X          X         X         X
enabled                                   X          X         X         X
errorfile                                 X          X         X         X
errorfiles                                X          X         X         X
errorloc                                  X          X         X         X
errorloc302                               X          X         X         X
-- キーワード -------------------------- defaults - frontend - listen -- backend -
errorloc303                               X          X         X         X
error-log-format                          X          X         X         -
external-check command                    X          -         X         X
external-check path                       X          -         X         X
force-persist                             -          -         X         X
force-be-switch                           -          X         X         -
filter                                    -          X         X         X
fullconn                                  X          -         X         X
guid                                      -          X         X         X
hash-balance-factor                       X          -         X         X
hash-preserve-affinity                    X          -         X         X
hash-type                                 X          -         X         X
http-after-response                       X (!)      X         X         X
http-check comment                        X          -         X         X
http-check connect                        X          -         X         X
http-check disable-on-404                 X          -         X         X
http-check expect                         X          -         X         X
http-check send                           X          -         X         X
http-check send-state                     X          -         X         X
http-check set-var                        X          -         X         X
http-check unset-var                      X          -         X         X
http-error                                X          X         X         X
http-request                              X (!)      X         X         X
http-response                             X (!)      X         X         X
http-reuse                                X          -         X         X
http-send-name-header                     X          -         X         X
id                                        -          X         X         X
ignore-persist                            -          -         X         X
load-server-state-from-file               X          -         X         X
log                                  (*)  X          X         X         X
log-format                                X          X         X         -
log-format-sd                             X          X         X         -
log-tag                                   X          X         X         X
log-steps                                 X          X         X         -
max-keep-alive-queue                      X          -         X         X
max-session-srv-conns                     X          X         X         -
maxconn                                   X          X         X         -
mode                                      X          X         X         X
monitor fail                              -          X         X         -
monitor-uri                               X          X         X         -
option abortonclose                  (*)  X          X         X         X
option allbackups                    (*)  X          -         X         X
option checkcache                    (*)  X          -         X         X
option clitcpka                      (*)  X          X         X         -
option contstats                     (*)  X          X         X         -
option disable-h2-upgrade            (*)  X          X         X         -
option dontlog-normal                (*)  X          X         X         -
option dontlognull                   (*)  X          X         X         -
-- キーワード -------------------------- defaults - frontend - listen -- backend -
option external-check                     X          -         X         X
option forwardfor                         X          X         X         X
option forwarded                     (*)  X          -         X         X
option h1-case-adjust-bogus-client   (*)  X          X         X         -
option h1-case-adjust-bogus-server   (*)  X          -         X         X
option http-buffer-request           (*)  X          X         X         X
option http-drop-request-trailers    (*)  X          -         -         X
option http-drop-response-trailers   (*)  X          -         X         -
option http-ignore-probes            (*)  X          X         X         -
option http-keep-alive               (*)  X          X         X         X
option http-no-delay                 (*)  X          X         X         X
option http-pretend-keepalive        (*)  X          -         X         X
option http-restrict-req-hdr-names        X          X         X         X
option http-server-close             (*)  X          X         X         X
option http-use-proxy-header         (*)  X          X         X         -
option httpchk                            X          -         X         X
option httpclose                     (*)  X          X         X         X
option httplog                            X          X         X         -
option httpslog                           X          X         X         -
option idle-close-on-response        (*)  X          X         X         -
option independent-streams           (*)  X          X         X         X
option ldap-check                         X          -         X         X
option log-health-checks             (*)  X          -         X         X
option log-separate-errors           (*)  X          X         X         -
option logasap                       (*)  X          X         X         -
option mysql-check                        X          -         X         X
option nolinger                      (*)  X          X         X         X
option originalto                         X          X         X         X
option persist                       (*)  X          -         X         X
option pgsql-check                        X          -         X         X
option prefer-last-server            (*)  X          -         X         X
option redispatch                    (*)  X          -         X         X
option redis-check                        X          -         X         X
option smtpchk                            X          -         X         X
option socket-stats                  (*)  X          X         X         -
option splice-auto                   (*)  X          X         X         X
option splice-request                (*)  X          X         X         X
option splice-response               (*)  X          X         X         X
option spop-check                         X          -         X         X
option srvtcpka                      (*)  X          -         X         X
option ssl-hello-chk                      X          -         X         X
-- キーワード -------------------------- defaults - frontend - listen -- backend -
option tcp-check                          X          -         X         X
option tcp-smart-accept              (*)  X          X         X         -
option tcp-smart-connect             (*)  X          -         X         X
option tcpka                              X          X         X         X
option tcplog                             X          X         X         -
option transparent      (deprecated) (*)  X          -         X         X
option use-small-buffers             (*)  X          -         X         X
persist rdp-cookie                        X          -         X         X
quic-initial                              X (!)      X         X         -
rate-limit sessions                       X          X         X         -
redirect                                  -          X         X         X
-- キーワード -------------------------- defaults - frontend - listen -- backend -
retries                                   X          -         X         X
retry-on                                  X          -         X         X
server                                    -          -         X         X
server-state-file-name                    X          -         X         X
server-template                           -          -         X         X
source                                    X          -         X         X
srvtcpka-cnt                              X          -         X         X
srvtcpka-idle                             X          -         X         X
srvtcpka-intvl                            X          -         X         X
stats admin                               -          X         X         X
stats auth                                X          X         X         X
stats enable                              X          X         X         X
stats hide-version                        X          X         X         X
stats http-request                        -          X         X         X
stats realm                               X          X         X         X
stats refresh                             X          X         X         X
stats scope                               X          X         X         X
stats show-desc                           X          X         X         X
stats show-legends                        X          X         X         X
stats show-node                           X          X         X         X
stats show-version                        X          X         X         X
stats uri                                 X          X         X         X
-- キーワード -------------------------- defaults - frontend - listen -- backend -
stick match                               -          -         X         X
stick on                                  -          -         X         X
stick store-request                       -          -         X         X
stick store-response                      -          -         X         X
stick-table                               -          X         X         X
tcp-check comment                         X          -         X         X
tcp-check connect                         X          -         X         X
tcp-check expect                          X          -         X         X
tcp-check send                            X          -         X         X
tcp-check send-lf                         X          -         X         X
tcp-check send-binary                     X          -         X         X
tcp-check send-binary-lf                  X          -         X         X
tcp-check set-var                         X          -         X         X
tcp-check unset-var                       X          -         X         X
tcp-request connection                    X (!)      X         X         -
tcp-request content                       X (!)      X         X         X
tcp-request inspect-delay                 X (!)      X         X         X
tcp-request session                       X (!)      X         X         -
tcp-response content                      X (!)      -         X         X
tcp-response inspect-delay                X (!)      -         X         X
timeout check                             X          -         X         X
timeout client                            X          X         X         -
timeout client-fin                        X          X         X         -
timeout client-hs                         X          X         X         -
timeout connect                           X          -         X         X
timeout http-keep-alive                   X          X         X         X
timeout http-request                      X          X         X         X
timeout queue                             X          -         X         X
timeout server                            X          -         X         X
timeout server-fin                        X          -         X         X
timeout tarpit                            X          X         X         X
timeout tunnel                            X          -         X         X
transparent                 (deprecated)  X          -         X         X
unique-id-format                          X          X         X         X
unique-id-header                          X          X         X         -
use_backend                               -          X         X         -
use-fcgi-app                              -          -         X         X
use-server                                -          -         X         X
------------------------------------+----------+----------+---------+---------
 キーワード                              defaults   frontend   listen    backend
```

## 4.2. アルファベット順のキーワードリファレンス {#section-4-2}

このセクションでは、各キーワードとその使い方を説明します。

<a id="entry-4-2-acl"></a>

**`acl <aclname> <criterion> [flags] [operator] <value> ...`**

```haproxy
acl <aclname> <criterion> [flags] [operator] <value> ...
```

アクセスリストを宣言または補完します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

このディレクティブは名前付きdefaultsセクションでのみ使用でき、名前のないセクションでは使用できません。defaultsセクションで定義されたACLは、そのセクションを使用するほかのセクションからは参照できません。

例：

```text
acl invalid_src  src          0.0.0.0/7 224.0.0.0/3
acl invalid_src  src_port     0:1023
acl local_dst    hdr(host) -i localhost
```

ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-backlog"></a>

**`backlog <conns>`**

```haproxy
backlog <conns>
```

想定するリスナーのバックログサイズをヒントとしてシステムに伝えます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<conns>   保留中の接続数です。OSによって、確認応答済みの接続数、
          未確認の接続数、またはその両方を表します。
```

このオプションは、QUICを含むストリームリスナーでのみ意味を持ちます。ただし、QUICインスタンスでの動作は同じではありません。

QUIC以外のすべてのリスナーでは、SYNフラッド攻撃への対策として、システムのSYNバックログサイズを増やす方法があります。システムによっては、システムパラメーターで調整できる場合、まったく調整できない場合、listen()システムコール時にアプリケーションから渡されるヒントを使う場合があります。デフォルトでは、HAProxyはフロントエンドのmaxconn値をlisten()システムコールに渡します。この値を利用できるシステムでは、別の値を指定できると役立つことがあるため、このbacklogパラメーターが用意されています。

Linux 2.4では、システムはこのパラメーターを無視します。Linux 2.6ではヒントとして使われ、システムは指定値を上回る最小の2の累乗まで受け付けますが、一定の上限（通常32768）を超えることはありません。

QUICリスナーでは、backlogは、進行中のハンドシェイクの最大数と、受け付けを待つ接続数の両方に共通の上限を設定します。ハンドシェイク段階は主にリモートピアとのネットワーク遅延に依存しますが、次の段階はhaproxyの負荷だけに依存します。どちらかの上限に達すると、haproxyは受信したINITIALパケットの破棄を始め、過剰な接続が減り始めるまで、新しい接続を一切割り当てないようにします。この状況により、ブラウザーが通知なしでHTTPのバージョンを下げ、TCPに切り替える可能性があります。

"maxconn"および対象OSのチューニングガイドも参照してください。

<a id="entry-4-2-balance"></a>

**`balance <algorithm> [ <arguments> ]`**

```haproxy
balance <algorithm> [ <arguments> ]
balance url_param <param> [check_post]
```

バックエンドで使用する負荷分散アルゴリズムを定義します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<algorithm> は、負荷分散時にサーバーを選択するアルゴリズムです。
            接続先固定の情報がない場合、または接続を別のサーバーに
            再割り当てする場合にのみ適用します。
            <algorithm> には、次のいずれかを指定できます。

  roundrobin  重みに従い、各サーバーを順番に使用します。
              サーバーの処理時間が均等に分布している場合に、最も
              滑らかで公平に分散するアルゴリズムです。動的な方式で、
              たとえばスロースタートのために、稼働中のサーバーの
              重みを調整できます。設計上、バックエンドごとに稼働できる
              サーバー数は4095台までです。一部の大規模なサーバー群では、
              ごく短時間停止したサーバーが復旧しても、再びサーバー群に
              組み込まれてトラフィックを受け取り始めるまで、数百件の
              リクエストを要する場合があります。非常にまれですが、
              正常な動作です。実際に遭遇しても心配しないよう、ここで
              説明しています。注意：LOGモードのバックエンドでは
              重みを無視します。

  static-rr   重みに従い、各サーバーを順番に使用します。
              roundrobinに似ていますが、静的な方式のため、稼働中に
              サーバーの重みを変更しても効果はありません。一方で、
              サーバー数には設計上の上限がありません。サーバーが
              復旧すると、マップ全体の再計算後、必ずただちにサーバー群に
              再び組み込まれます。CPU使用量もわずかに少なくなります
              （約-1%）。このアルゴリズムはLOGモードでは使えません。

  leastconn   接続数が最も少ないサーバーに接続を割り当てます。
              同じ負荷のサーバー群内ではラウンドロビンで割り当て、
              すべてのサーバーが使われるようにします。LDAP、SQL、TSEなど、
              非常に長いセッションを想定する場合に推奨しますが、HTTPの
              ように短いセッションを使うプロトコルにはあまり適しません。
              動的な方式なので、たとえばスロースタートのために、
              稼働中のサーバーの重みを調整できます。待ち行列を最小限に
              抑えるため、確立済みの接続数に加え、待機中の接続数も
              考慮します。このアルゴリズムはLOGモードでは使えません。

  first       接続を受け入れる空きがある最初のサーバーに割り当てます。
              サーバーは数値の識別子が小さい順に選びます
              （サーバーパラメーター"id"を参照）。デフォルトの識別子は、
              サーバー群内での順序です。サーバーがmaxconnの値に達すると、
              次のサーバーを使います。maxconnを設定せずにこの方式を
              使用しても意味がありません。常に最小限の台数だけを使い、
              負荷の低い時間帯には余分なサーバーの電源を切れるように
              することが目的です。サーバーの重みは無視します。HTTPにも
              役立つ場合はありますが、RDPやIMAPのような長いセッションで
              より効果があります。効率よく利用するには、クラウドの
              コントローラーがサーバーの使用状況を定期的に調べ、未使用なら
              電源を切ることを推奨します。また、バックエンドの待ち行列を
              定期的に調べ、増加したら新たなサーバーの電源を入れます。
              あるいは、"http-check send-state"で負荷をサーバーに
              通知できます。このアルゴリズムはLOGモードでは使えません。

  hash        引数に通常のサンプル式を受け取ります。リクエストごとに式を
              評価し、設定されたhash-typeに従ってハッシュを計算します。
              ハッシュ値を稼働中のサーバーの重みの合計で割り、リクエストを
              受け取るサーバーを決めます。"source"、"uri"、"hdr()"、
              "url_param()"、"rdp-cookie"の代わりに使うことで、
              コンバーターの利用、評価方法の細かな調整、たとえば
              ローカル変数からのデータ取得が可能です。データを取得
              できない場合は、ラウンドロビンを適用します。デフォルトでは
              静的な方式なので、稼働中にサーバーの重みを変えても効果は
              ありませんが、"hash-type"で動作を変更できます。
              LOGモードのバックエンドでは使えません。
              代わりに"log-hash"を使ってください。

  source      送信元IPアドレスのハッシュを計算し、稼働中のサーバーの重みの
              合計で割って、リクエストを受け取るサーバーを決めます。
              サーバーの停止や復旧がない限り、同じクライアントIPアドレスは
              常に同じサーバーに到達します。稼働中のサーバー数の変化に
              よってハッシュ結果が変わると、多くのクライアントが別の
              サーバーに振り分けられます。通常はcookieを挿入できない
              TCPモードで使用します。インターネット上で、セッションcookieを
              拒否するクライアントの接続先を可能な限り固定する用途にも
              使えます。デフォルトでは静的な方式なので、稼働中にサーバーの
              重みを変えても効果はありませんが、"hash-type"で動作を
              変更できます。前述の"hash"オプションも参照してください。
              LOGモードのバックエンドでは使えません。

  uri         URIの左側（疑問符より前）、または"whole"パラメーターを
              指定した場合はURI全体のハッシュを計算し、稼働中のサーバーの
              重みの合計で割ります。その結果からリクエストを受け取る
              サーバーを決めます。サーバーの停止や復旧がない限り、同じURIは
              常に同じサーバーに振り分けられます。キャッシュヒット率を
              最大限に高めるため、キャッシュプロキシやアンチウイルス
              プロキシで使用します。HTTPバックエンドでのみ使用できます。
              デフォルトでは静的な方式なので、稼働中にサーバーの重みを
              変えても効果はありませんが、"hash-type"で動作を変更できます。

              このアルゴリズムには、任意指定の"len"と"depth"という
              二つのパラメーターがあり、どちらも後ろに正の整数を指定します。
              URIの先頭部分だけで負荷を分散したい場合に役立ちます。
              "len"は、ハッシュの計算対象とするURI先頭からの文字数です。
              URIは通常"/"で始まるため、"len"に1を指定しても
              意味があることはほとんどありません。

              "depth"は、ハッシュの計算に使うディレクトリの最大階層数を
              指定します。リクエスト中のスラッシュごとに一階層と数えます。
              両方のパラメーターを指定した場合は、どちらかの上限に
              達した時点で評価を終了します。

              "path-only"を指定すると、ハッシュのキーはパスの最初の'/'
              から始まります。絶対URIのauthority部分を無視し、HTTP/1と
              HTTP/2のURIで同じハッシュが得られるようにできます。
              前述の"hash"オプションも参照してください。

  url_param   引数で指定したURLパラメーターを、各HTTP GETリクエストの
              クエリー文字列から探します。

              修飾子"check_post"を指定した場合、URLの疑問符('?')以降の
              クエリー文字列にパラメーターが見つからなければ、HTTP POSTの
              リクエストエンティティ内を探します。通知されたデータ量を
              受信するか、リクエストバッファーが満杯になるまで、メッセージ
              本文の解析は開始しません。まれにチャンク形式の転送を使う
              場合は、最初のチャンクだけを調べます。パラメーターの値が
              チャンクの境界で分断されていると、振り分けられるとしても
              ランダムになることがあります。このキーワードは以前、
              任意指定の<max_wait>パラメーターに対応していましたが、
              現在は無視します。

              パラメーターに続いて等号('=')と値が見つかった場合、
              値のハッシュを計算して稼働中のサーバーの重みの合計で割り、
              リクエストを受け取るサーバーを決めます。

              リクエスト内のユーザー識別子を追跡し、サーバーの停止や復旧が
              ない限り、同じユーザーIDを常に同じサーバーに送るために
              使います。値またはパラメーターが見つからない場合は、
              ラウンドロビンを適用します。HTTPバックエンドでのみ使用
              できます。デフォルトでは静的な方式なので、稼働中にサーバーの
              重みを変えても効果はありませんが、"hash-type"で動作を
              変更できます。前述の"hash"オプションも参照してください。

  hdr(<name>) 各HTTPリクエストからHTTPヘッダー<name>を探します。
              同等のACL関数'hdr()'と同様、括弧内のヘッダー名は
              大文字と小文字を区別しません。ヘッダーがない場合や値が
              入っていない場合は、代わりにroundrobinを適用します。

              任意指定の'use_domain_only'パラメーターを使うと、'Host'などの
              特定のヘッダーで、主要なドメイン部分だけをハッシュの対象に
              できます。たとえばHostの値が"haproxy.1wt.eu"の場合は、
              "1wt"だけを対象とします。

              デフォルトでは静的な方式なので、稼働中にサーバーの重みを
              変えても効果はありませんが、"hash-type"で動作を変更できます。
              前述の"hash"オプションも参照してください。

  random
  random(<draws>)
              乱数をコンシステントハッシュ関数のキーとして使用します。
              サーバーの重みを反映し、動的な重みの変更やサーバーの追加が
              ただちに反映されます。大規模なサーバー群や、サーバーを頻繁に
              追加、削除する構成では、roundrobinやleastconnで生じうる
              特定サーバーへのアクセス集中を避けられるため、ランダムな
              負荷分散が役立つ場合があります。hash-balance-factorで、
              さらに分散の公平性を改善できます。特にサーバーごとの
              応答時間の変動が大きい場合に有効です。引数<draws>を指定する
              場合は、一以上の整数でなければなりません。これは、
              抽出したサーバーの中から最も負荷の低いものを選ぶまでに
              行う抽出回数を示します。二台から負荷の低いほうを選ぶだけで、
              公平性が大幅に改善することが実証されています。サーバー群で
              最も負荷の高いサーバーを常に避け、コンシステントハッシュの
              リストの不均等な分布による偏りも排除できるためです。
              Nを大きくすると、負荷の高い順にN-1台を除外できますが、
              性能は低下します。値を非常に大きくするとleastconnに近い
              結果になりますが、処理ははるかに遅くなります。
              また、負荷が非常に低い大規模なサーバー群や、完全に均衡した
              状態では、負荷を比較しても同じ値になることがよくあります。
              測定したすべてのサーバーの負荷が等しい場合は、直前の一秒間の
              リクエストレートを比較します。これにより、roundrobinと同様に
              時間を通じてサーバーの使用をより均等にし、コンシステント
              ハッシュの偏りを緩和できます。デフォルト値は2で、通常は
              非常に良好な分散と性能を示します。サーバーごとに毎秒数件未満の
              リクエストしかない大規模な構成では、3や4に増やすと役立つ
              場合があります。このアルゴリズムはPower of Two Random Choices
              とも呼ばれ、次の文書で説明されています。
              http://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf

              LOGモードのバックエンドではサーバーの負荷という概念がないため、
              抽出回数は無視し、一回だけランダムに選択します。大規模な
              サーバー群や、利用可能なサーバー群への追加、削除が頻繁な構成では、
              roundrobinで生じうる特定サーバーへのアクセス集中を避けられるため、
              ログをランダムに振り分けることが役立つ場合があります。

  rdp-cookie
  rdp-cookie(<name>)
              受信したTCPリクエストごとにRDP cookie <name>を探して
              ハッシュを計算します。省略時は"mstshash"を使います。
              同等のACL関数'req.rdp_cookie()'と同様、大文字と小文字を
              区別しません。同じユーザーやセッションIDを常に同じサーバーに
              送れるため、限定的な接続先固定の方法として役立ちます。
              cookieが見つからない場合は、通常のroundrobinを使用します。

              これを機能させるには、フロントエンドで、リクエストバッファーに
              RDP cookieがすでに存在することを保証する必要があります。
              そのためには、'tcp-request content accept'ルールと
              'req.rdp_cookie_cnt' ACLを組み合わせて使用しなければなりません。

              デフォルトでは静的な方式なので、稼働中にサーバーの重みを
              変えても効果はありませんが、"hash-type"で動作を変更できます。
              前述の"hash"オプションも参照してください。

  log-hash    引数にコンバーターのカンマ区切りリストを受け取ります。
              入力ログメッセージに順番に適用し、結果を文字列に変換して、
              設定されたhash-typeに従ってハッシュを計算します。そのハッシュを
              使い、ログバックエンドに定義したサーバーから送信先を選びます。
              文字列コンバーターで最終的なログメッセージからキーを抽出し、
              ハッシュによって同じサーバーに固定できるようにすることが
              目的です。現在は"map-based"ハッシュだけに対応しています。
              LOGモードのバックエンドでのみ使用できます。それ以外では、
              代わりに"hash"を使ってください。

  sticky      できる限り同じサーバーに固定します。利用可能なサーバーの
              リストの先頭にあるサーバーが、すべてのログメッセージを
              受け取ります。そのサーバーがDOWNになると、リストの次の
              サーバーが引き継ぎます。DOWNだったサーバーがUPに戻ると、
              リストの末尾に追加します。このため、固定先のサーバーが
              DOWNになるまで接続先は変わりません。

<arguments> は、一部のアルゴリズムで必要になる場合がある任意の引数リストです。
            現在、任意指定の引数に対応するのは"url_param"、"uri"、
            "log-hash"のみです。
```

ほかのアルゴリズム、モード、オプションを何も設定していない場合、バックエンドの負荷分散アルゴリズムは"random"になります。アルゴリズムは、各バックエンドにつき1回だけ設定できます。

NTLMのように同じ接続を必要とする認証方式では、URIに基づくアルゴリズムを使ってはなりません。後続のリクエストが別のバックエンドサーバーにルーティングされ、NTLMが依存する誤った前提が成り立たなくなるためです。

TCP/HTTPの例：

```text
balance roundrobin
balance url_param userid
balance url_param session_id check_post 64
balance hdr(User-Agent)
balance hdr(host)
balance hdr(Host) use_domain_only
balance hash req.cookie(clientid)
balance hash var(req.client_id)
balance hash req.hdr_ip(x-forwarded-for,-1),ipmask(24)
```

LOGバックエンドの例：

```text
global
  log backend@mylog-rrb local0 # send all logs to mylog-rrb backend
  log backend@mylog-hash local0 # send all logs to mylog-hash backend

backend mylog-rrb
  mode log
  balance roundrobin

  server s1 udp@127.0.0.1:514 # will receive 50% of log messages
  server s2 udp@127.0.0.1:514

backend mylog-hash
  mode log

  # extract "METHOD URL PROTO" at the end of the log message,
  # and let haproxy hash it so that log messages generated from
  # similar requests get sent to the same syslog server:
  balance log-hash 'field(-2,\")'

  # server list here
  server s1 127.0.0.1:514
  #...
```

注意："check_post"拡張を"url_param"と併用する際は、以下の注意点と制限を考慮する必要があります。

    - すべてのPOSTリクエストが検討対象となります。パラメーターが、バイナリデータを含む可能性のあるボディーやエンティティー内にあるかどうかを判断する方法がないためです。したがって、ボディーにURLパラメーターがないPOSTリクエストを検討対象から除くために、別の方法が必要になることがあります（acl http_endを参照）。

    - リクエストバッファーのサイズより大きな`<max_wait>`の値を使っても意味はなく、役に立ちません。バッファーサイズはビルド時に設定され、デフォルトは16 kBです。

    - Content-Encodingはサポートされていません。パラメーターの検索はおそらく失敗します。また、負荷分散はラウンドロビンにフォールバックします。

    - Expect: 100-continueはサポートされていません。負荷分散はラウンドロビンにフォールバックします。

    - Transfer-Encoding (RFC7230 3.3.1)は最初のチャンクでのみサポートされています。パラメーター値の全体が最初のチャンクに含まれていない場合、サーバーの選択は未定義になります（実際には、最初のチャンクに実際に現れた量によって定義されます）。

    - この機能は100、411、または501応答の生成をサポートしていません。

    - 場合によっては、"check_post"を指定すると、メッセージ本文の内容全体を走査しようとする可能性があります。通常、線形空白または制御文字が見つかると、URLパラメーターリストと思われる部分の終わりを示すため、走査は終了します。SGML型のメッセージ本文では、おそらく問題になりません。

関連項目: "dispatch", "cookie", "transparent", "hash-type"

<a id="entry-4-2-be-unpublished"></a>

**`be-unpublished`**

```haproxy
be-unpublished
```

バックエンドを非公開状態で開始するように指示します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

実際には、他のプロキシが現在のプロキシを参照するuse_backendおよびdefault_backendルールは無視され、次のコンテンツスイッチングルールが評価されます。ただし、"force-be-switch"ルールを用いることでこれをバイパスできます。

この状態は無効状態に似ていますが、いくつかの違いがあります。まず、非公開バックエンドは完全に初期化され、サーバーのヘルスチェックもアクティブなままです。最後に、CLI上の"publish backend"コマンドにより、バックエンドを公開することができます。管理マニュアルを参照してください。

関連項目: "force-be-switch"

<a id="entry-4-2-bind"></a>

**`bind [<address>]:<port_range> [, ...] [param*]`**

```haproxy
bind [<address>]:<port_range> [, ...] [param*]
bind /<path> [, ...] [param*]
```

フロントエンドで1つ以上のリスニングアドレスおよび/またはポートを定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<address>     は省略可能で、ホスト名、IPv4アドレス、IPv6アドレス、または'*'を
              指定できます。フロントエンドがリッスンするアドレスを指定します。
              未指定の場合、システムのすべてのIPv4アドレスでリッスンします。
              '*'またはシステムの特殊アドレス"0.0.0.0"を指定した場合も同じです。
              IPv6でこれに相当するアドレスは'::'です。UDPで複数のアドレスに
              バインドする場合、応答時に正しいネットワークインターフェースと
              送信元アドレスを使用するには、OSの特定の機能が必要です。
              つまり、QUICリスナーを複数のアドレスにバインドするのは、
              十分に新しいシステムで実行する場合に限ってください。

              アドレスの前にアドレスファミリーの接頭辞を付けると、アドレスの
              形式にかかわらずファミリーを指定できます。スラッシュ('/')を
              含まないUNIXソケットのパスを指定する場合などに役立ちます。
              現在、次の接頭辞をサポートしています。
                - 'ipv4@'  -> 常にIPv4アドレスとして扱います。
                - 'ipv6@'  -> 常にIPv6アドレスとして扱います。
                - 'udp@'   -> IPv4またはIPv6アドレスとして解決し、UDPを
                  使用します。現在、このリスナーをサポートしているのは
                  log-forwardセクションだけです。
                - 'udp4@'  -> 常にIPv4アドレスとして扱い、UDPを使用します。
                  現在、このリスナーをサポートしているのは
                  log-forwardセクションだけです。
                - 'udp6@'  -> 常にIPv6アドレスとして扱い、UDPを使用します。
                  現在、このリスナーをサポートしているのは
                  log-forwardセクションだけです。
                - 'unix@'  -> ローカルUNIXソケットのパスとして扱います。
                - 'abns@'  -> 抽象名前空間のアドレスとして扱います（Linuxのみ）。
                - 'abnsz@'  -> 抽象名前空間のアドレスとして扱います（Linuxのみ）が、
                   明示的にゼロ終端します。つまり、sun_pathを埋めるための\0の
                   パディングを行いません。haproxyがデフォルトで使用する
                   abnsの命名規則を実装していないプログラムとの接続に役立ちます。
                - 'fd@<n>' -> 親から継承したファイルディスクリプター<n>を使用します。
                  fdはバインド済みでなければなりません。すでにリッスンしていても、
                  まだリッスンしていなくてもかまいません。
                - 'sockpair@<n>'-> fd@と似ていますが、接続済みのUNIXソケットまたは
                  socketpairのfdを使用する必要があります。bindはUNIXソケット経由で
                  FDを受信するまで待ち、それをaccept()のFDと同じように使用します。
                  使用には注意を払うことを推奨します。
                - 'quic4@' -> IPv4アドレスとして解決し、UDPを使用します。
                  大量のトラフィックで最良の性能を得るには、
                  "tune.quic.fe.sock-per-conn
                  default-on"を維持することを推奨します。そうしない場合、
                  QUIC接続はリスナーソケット上で多重化されます。別の方法として、
                  QUICリスナーのインスタンスを複数のスレッドに分けて複製できます。
                  たとえば"shards"キーワードを使うと、少なくともスレッド間の
                  競合を減らせます。
                - 'quic6@' -> IPv6アドレスとして解決し、UDPを使用します。
                  IPv4上のQUICについて述べた性能上の注意は、こちらにも当てはまります。
                - 'rhttp@' [ 実験的 ] -> リバースHTTPに使用します。
                  アドレスには'<backend>/<server>'形式でサーバーを指定する
                  必要があります。このサーバーを使ってリモートアドレスへの接続を
                  作成します。リスナーは"nbconn"個の接続を維持しようとします。
                  これは実験的な機能であり、このbindより前の行に
                  "expose-experimental-directives"を記述する必要があります。

              アドレスパラメーターでは環境変数を参照することもできます。
              環境変数についてはセクション2.3を参照してください。

<port_range>  は、上記のIPアドレスでプロキシが接続を受け付ける、単一のTCPポート
              またはポート範囲です。TCPリスナーではポートの指定が必須です。
              IPv6アドレスの場合、ポートは常に最後のコロン(':')の後の数値です。
              次のいずれかの形式で指定できます。
               - 数値のポート（例：'80'）
               - 下限と上限を明示した、ダッシュ区切りのポート範囲
                 （例：'2000-2100'）。両端の値も範囲に含みます。

              ポート範囲には特に注意する必要があります。<address:port>の組ごとに
              ソケットを一つ（つまりファイルディスクリプターを一つ）消費するため、
              単純な範囲指定でも大量のディスクリプターを消費し、ソケットが
              枯渇しやすくなります。また、同じシステムで動作するすべての
              インスタンスを通して、各<address:port>の組を使えるのは一度だけです。
              1024未満のポートへのバインドでは、通常、プログラムの起動時に
              特別な権限が必要です。この権限は'uid'パラメーターとは無関係です。

<path>        はスラッシュ('/')で始まるUNIXソケットのパスで、TCPのリッスンポートの
              代わりに指定します。HAProxyは、この場所にあるソケットでUNIX接続を
              受け付けます。パスはスラッシュで始める必要があり、デフォルトでは
              絶対パスです。globalセクションの"unix-bind"で定義した接頭辞からの
              相対パスにすることもできます。接頭辞とソケットパスを合わせた長さは、
              システムのUNIXソケットの上限を超えることができません。
              この上限は一般に107文字です。

<param*>      は、同じ行で宣言したすべてのソケットに共通するパラメーターのリストです。
              多数のパラメーターがあり、使用できるものはOSやビルドオプションに
              よって異なります。専用のセクションで詳しく説明しています。
              詳細はセクション5を参照してください。
```

コンマで区切られたaddress:portの組み合わせのリストを指定できます。フロントエンドはこれらのすべてのアドレスでリッスンします。フロントエンドでリッスン可能なアドレスおよびポートの数に固定の上限はなく、またフロントエンド内の"bind"文の数にも上限はありません。

例：

```text
listen http_proxy
    bind :80,:443
    bind 10.0.0.1:10080,10.0.0.1:10443
    bind /var/run/ssl-frontend.sock user root mode 600 accept-proxy

listen http_https_proxy
    bind :80
    bind :443 ssl crt /etc/haproxy/site.pem

listen http_https_proxy_explicit
    bind ipv6@:80
    bind ipv4@public_ssl:443 ssl crt /etc/haproxy/site.pem
    bind unix@ssl-frontend.sock user root mode 600 accept-proxy

listen external_bind_app1
    bind "fd@${FD_APP1}"

listen h3_quic_proxy
    bind quic4@10.0.0.1:8888 ssl crt /etc/mycrt
```

注意： Linuxの抽象名前空間ソケットに関して、"abns"HAProxyソケットはsun_pathの全長をアドレス長として使用します。他のプログラム（例: socat）はデフォルトで文字列長のみを使用します。socatの抽象ソケット定義に",unix-tightsocklen=0"オプションを渡すことでHAProxyと互換性を持たせることができます。または、"abnsz"HAProxyソケットファミリを使用してください。

"source"、"option forwardfor"、"unix-bind"、PROXYプロトコルのドキュメント、およびbindオプションについて説明する[セクション5](/ja/haproxy/bind-and-server-options/)も参照してください。

<a id="entry-4-2-capture-cookie"></a>

**`capture cookie <name> len <length>`**

```haproxy
capture cookie <name> len <length>
```

リクエストおよびレスポンスの両方でCookieをキャプチャし、ログに記録します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<name>    キャプチャするCookie名の先頭部分です。名前を完全一致させるには、
          名前の末尾に等号（'='）を付けます。ログには完全な名前が記録されるため、
          Cookieの名前と値の両方を変更するアプリケーションサーバー
          （ASPSESSIONXXXなど）で役立ちます。

<length>  ログに記録する最大文字数です。標準の"name=value"形式で、
          Cookie名、等号、値をすべて含みます。文字列が<length>を超える場合、
          右側が切り詰められます。
```

最初のCookieだけをキャプチャします。"cookie"リクエストヘッダーと"set-cookie"レスポンスヘッダーの両方を監視します。通常、ユーザーのCookieはログインページでしか変わらないため、ユーザー間でセッションの混線や盗用を引き起こすアプリケーションのバグを調べるのに特に役立ちます。

クライアントがCookieを提示しなかった場合、関連するログカラムには"-"が報告されます。サーバーがリクエストに対してCookieを割り当てなかった場合、レスポンスカラムには"-"が報告されます。

キャプチャはフロントエンドでのみ実行されます。これは、特定のフロントエンドに対してバックエンドによってログフォーマットが変化しないようにするためです。将来的に変更される可能性があります。また、フロントエンド内に"capture cookie"ステートメントは1つしか指定できません。最大キャプチャ長はグローバル"tune.http.cookielen"設定で設定され、デフォルトは63文字です。"defaults"セクションでキャプチャを指定することはできません。

例：

```text
capture cookie ASPSESSION len 32
```

"capture request header"、"capture response header"、およびログについて説明する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-capture-request-header"></a>

**`capture request header <name> len <length>`**

```haproxy
capture request header <name> len <length>
```

指定されたリクエストヘッダーの最後の出現をキャプチャし、ログに記録します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<name>    キャプチャするヘッダーの名前です。ヘッダー名は大文字と小文字を
          区別しませんが、通常は各単語の最初の文字を大文字にして、
          リクエストに現れる形で記述します。ログにはヘッダー名は表示されず、
          値だけが記録されますが、ログ内の位置は維持されます。

<length>  値から抽出してログに記録する最大文字数です。
          文字列が<length>を超える場合、右側が切り詰められます。
```

ヘッダーの最後の出現箇所の値を完全にキャプチャします。値は波括弧（'{}'）で囲んでログに追加されます。複数のヘッダーをキャプチャする場合は縦棒（'\|'）で区切り、設定で宣言した順序で表示します。存在しないヘッダーは空文字列としてログに記録します。リクエストヘッダーのキャプチャの一般的な用途には、仮想ホスティング環境の"Host"フィールド、アップロードをサポートする場合の"Content-length"、実際のユーザーとロボットをすばやく区別するための"User-agent"、プロキシ環境でリクエストの送信元を調べるための"X-Forwarded-For"があります。

"User-agent"などのヘッダーをキャプチャすると、空白もログに記録され、ログ解析が難しくなる場合があります。ログパーサーが波括弧を手掛かりに処理できるほど賢くないと分かっている場合は、記録する内容に注意してください。

キャプチャするリクエストヘッダーの数にも長さにも制限はありませんが、ストリームあたりのメモリー使用量を抑えるには、数を少なく、長さを短くしておくのが賢明です。同じフロントエンドでログ形式を一貫させるため、ヘッダーキャプチャはフロントエンドでのみ宣言できます。"defaults"セクションでキャプチャを指定することはできません。

例：

```text
capture request header Host len 15
capture request header X-Forwarded-For len 15
capture request header Referer len 15
```

"capture cookie"、"capture response header"、およびログについて説明する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-capture-response-header"></a>

**`capture response header <name> len <length>`**

```haproxy
capture response header <name> len <length>
```

指定したレスポンスヘッダーの最後の出現箇所をキャプチャし、ログに記録します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<name>    キャプチャするヘッダーの名前です。ヘッダー名は大文字と小文字を
          区別しませんが、通常は各単語の最初の文字を大文字にして、
          レスポンスに現れる形で記述します。ログにはヘッダー名は表示されず、
          値だけが記録されますが、ログ内の位置は維持されます。

<length>  値から抽出してログに記録する最大文字数です。
          文字列が<length>を超える場合、右側が切り詰められます。
```

ヘッダーの最後の出現箇所の値を完全にキャプチャします。結果は波括弧（'{}'）で囲み、キャプチャしたリクエストヘッダーの後にログへ追加します。複数のヘッダーをキャプチャする場合は縦棒（'\|'）で区切り、設定で宣言した順序で表示します。存在しないヘッダーは空文字列としてログに記録します。レスポンスヘッダーのキャプチャの一般的な用途には、返却予定のバイト数を示す"Content-length"ヘッダーや、リダイレクトを追跡するための"Location"ヘッダーがあります。

キャプチャするレスポンスヘッダーの数にも長さにも制限はありませんが、ストリームあたりのメモリー使用量を抑えるには、数を少なく、長さを短くしておくのが賢明です。同じフロントエンドでログ形式を一貫させるため、ヘッダーキャプチャはフロントエンドでのみ宣言できます。"defaults"セクションでキャプチャを指定することはできません。

例：

```text
capture response header Content-length len 9
capture response header Location len 15
```

"capture cookie"、"capture request header"、およびログについて説明する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-clitcpka-cnt"></a>

**`clitcpka-cnt <count>`**

```haproxy
clitcpka-cnt <count>
```

クライアント側で接続を切断する前に、TCPが送信するkeepaliveプローブの最大数を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<count>   キープアライブプローブの最大数です。
```

このキーワードはソケットオプションTCP_KEEPCNTに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_probes）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option clitcpka"、"clitcpka-idle"、"clitcpka-intvl"。

<a id="entry-4-2-clitcpka-idle"></a>

**`clitcpka-idle <timeout>`**

```haproxy
clitcpka-idle <timeout>
```

クライアント側でTCP keepaliveパケットの送信を有効にした場合に、TCPがkeepaliveプローブの送信を開始するまでに接続がアイドル状態を維持する必要がある時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<timeout> TCPがキープアライブプローブを送信し始めるまでに必要な、
          接続のアイドル時間です。デフォルトの単位は秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に単位を付ければ
          ほかの単位でも指定できます。
```

このキーワードはソケットオプションTCP_KEEPIDLEに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_time）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option clitcpka"、"clitcpka-cnt"、"clitcpka-intvl"。

<a id="entry-4-2-clitcpka-intvl"></a>

**`clitcpka-intvl <timeout>`**

```haproxy
clitcpka-intvl <timeout>
```

クライアント側の個々のkeepaliveプローブ間の時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<timeout> 個々のキープアライブプローブの間隔です。
          デフォルトの単位は秒ですが、本ドキュメントの冒頭で
          説明したように、数値の後に単位を付ければ
          ほかの単位でも指定できます。
```

このキーワードはソケットオプションTCP_KEEPINTVLに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_intvl）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option clitcpka"、"clitcpka-cnt"、"clitcpka-idle"。

<a id="entry-4-2-compression-algo"></a>

**`compression algo <algorithm> ...`**

```haproxy
compression algo <algorithm> ...
compression algo-req <algorithm>
compression algo-res <algorithm>
compression type <mime type> ...
```

HTTP圧縮を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
algo     レスポンスでサポートする圧縮アルゴリズムのリストを続けます
         （従来のキーワード）。
algo-req リクエストに使用する圧縮アルゴリズムを続けます
         （指定できるのは単一のアルゴリズムのみです）。
algo-res レスポンスでサポートする圧縮アルゴリズムのリストを続けます。
type     レスポンスで圧縮するMIMEタイプのリストを続けます
         （従来のキーワード）。
type-req リクエストで圧縮するMIMEタイプのリストを続けます。
type-res レスポンスで圧縮するMIMEタイプのリストを続けます。
```

現在サポートされているアルゴリズムは次のとおりです。

```text
identity     主にデバッグ用で、圧縮機能の開発時に役立ちました。
             Identityはデータを一切変更しません。

gzip         gzip圧縮を適用します。この設定は、zlibまたはlibslzの
             サポートを組み込んでビルドした場合にのみ使用できます。

deflate      "gzip"と同様ですが、deflateアルゴリズムとzlib形式を使用します。
             このアルゴリズムは多くのブラウザーでサポートが曖昧であり、
             最近のブラウザーではまったくサポートされていません。
             実験以外の用途では使用しないことを強く推奨します。
             この設定は、zlibまたはlibslzのサポートを組み込んで
             ビルドした場合にのみ使用できます。

raw-deflate  zlibラッパーを伴わない"deflate"と同じで、ブラウザーが
             "deflate"を要求した場合の代替として使用します。
             主要なブラウザーはすべて対応しており、標準には違反するものの、
             少なくともMSIEおよび一部のバージョンのSafariでは
             "deflate"より良好に動作することが知られています。
             "deflate"と併用せず、どちらか一方を使用してください。
             両方とも同じAccept-Encodingトークンに反応するためです。
             この設定は、zlibまたはlibslzのサポートを組み込んで
             ビルドした場合にのみ使用できます。
```

圧縮はAccept-Encodingリクエストヘッダーに応じて有効になります。identityでは、このヘッダーを考慮しません。バックエンドサーバーがHTTP圧縮をサポートしている場合、これらのディレクティブは何も行いません。HAProxyは圧縮済みのレスポンスを認識し、再度圧縮しません。バックエンドサーバーがHTTP圧縮をサポートせず、リクエストにAccept-Encodingヘッダーがある場合、HAProxyは該当するレスポンスを圧縮します。

次の場合、圧縮は無効になります。\* リクエストが"Accept-Encoding"ヘッダーでサポートされる圧縮アルゴリズムを通知していない \* レスポンスメッセージがHTTP/1.1以上でない \* HTTPステータスコードが200、201、202、203のいずれでもない \* レスポンスに"Content-Length"ヘッダーも、最後の値が"chunked"である"Transfer-Encoding"もない \* レスポンスに"Content-Type"ヘッダーがあり、その最初の値が"multipart"で始まる \* レスポンスの"Cache-control"ヘッダーに"no-transform"の値がある \* User-Agentが"Mozilla/4"に一致する。ただし、XP SP2のMSIE 6、またはMSIE 7以降は除く \* レスポンスに、すでに圧縮されていることを示す"Content-Encoding"ヘッダーがある（compression offloadを参照） \* レスポンスに無効な"ETag"ヘッダーまたは複数のETagヘッダーがある \* ペイロードサイズが最小サイズより小さい（compression minsize-resを参照）

注意：圧縮ではWarningヘッダーは送出されません。

例：

```text
compression algo gzip
compression type text/html text/plain
```

関連項目: "compression offload"、"compression direction"、"compression minsize-req"および"compression minsize-res"

<a id="entry-4-2-compression-minsize-req"></a>

**`compression minsize-req <size>`**

```haproxy
compression minsize-req <size>
compression minsize-res <size>
```

圧縮を適用するペイロードの最小サイズをバイト単位で設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

このサイズ未満のペイロードは圧縮されず、圧縮の効果が大きくないデータに対する不要なCPUオーバーヘッドを回避します。"minsize-req"はリクエストに、"minsize-res"はレスポンスに適用されます。デフォルト値は0です。

<a id="entry-4-2-compression-offload"></a>

**`compression offload`**

```haproxy
compression offload
```

HAProxyを圧縮オフローダーとしてのみ動作させます。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

"offload"設定によりHAProxyはAccept-Encodingヘッダーを削除し、バックエンドサーバーがレスポンスを圧縮しないようにします。すべての圧縮処理がHAProxyの配置されている一か所に集中するため、この設定を使わないことを強く推奨します。ただし、一部の配置構成では、無効にできない不具合のあるHTTP圧縮実装を持つゲートウェイの前段にHAProxyが配置される場合があります。その場合、HAProxyでゲートウェイが無効なペイロードを出力するのを防げます。設定でヘッダーを単に削除しても機能しません。ヘッダーの解析より前に適用され、HAProxy自身の圧縮を妨げるためです。このような状況では、"offload"設定を使用することを推奨します。

この設定がdefaultsセクションで使用された場合、警告が発行され、オプションは無視されます。

参照："compression type"、"compression algo"、"compression direction"。

<a id="entry-4-2-compression-direction"></a>

**`compression direction <direction> (deprecated)`**

```haproxy
compression direction <direction> (deprecated)
```

HAProxyがリクエストとレスポンスの両方を圧縮できるようにします。有効な値は"request"（リクエストのみ圧縮）、"response"（レスポンスのみ圧縮）、"both"（両方圧縮）です。デフォルト値は"response"です。

このディレクティブは、従来の"filter compression"が有効な場合にのみ関係があります。明示的なcomp-reqとcomp-resフィルターでは、圧縮方向の指定が冗長になるためです。

使用可能なコンテキスト: http

参照："compression type"、"compression algo"、"compression offload"。

<a id="entry-4-2-cookie"></a>

**`cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]`**

```haproxy
cookie <name> [ rewrite | insert | prefix ] [ indirect ] [ nocache ]
              [ postonly ] [ preserve ] [ httponly ] [ secure ]
              [ domain <domain> ]* [ maxidle <idle> ] [ maxlife <life> ]
              [ dynamic ] [ attr <value> ]*
```

バックエンドでCookieに基づく接続先の固定を有効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<name>    接続先を固定するために監視、変更、挿入するcookieの名前です。
          このcookieは、レスポンスの"Set-Cookie"ヘッダーでクライアントに
          送信し、クライアントは以後のすべてのリクエストの"Cookie"ヘッダーで
          送り返します。アプリケーションが使う可能性のあるcookieと
          名前が競合しないよう、特に注意して選ぶことを推奨します。また、HTTP/HTTPS
          など、同じクライアントが複数のバックエンドを利用する場合は、
          バックエンド間で接続先を固定したくなければ、すべての
          バックエンドで異なるcookie名を使うよう注意してください。

rewrite   サーバーがcookieを発行し、HAProxyがその値を書き換えて
          サーバーの識別子を設定することを示します。"Set-cookie"と
          "Cache-control"ヘッダーの複雑な組み合わせの管理を
          アプリケーションに任せる場合に便利です。接続先固定用のcookieを
          発行すべきかどうかを、アプリケーションで判断できます。
          すべてのレスポンスを監視する想定なので、HTTPトンネルモードでは
          動作しません。アプリケーションの動作が非常に複雑、または不正常な
          場合を除き、新規構築で最初からこのモードを使うことは勧めません。
          "insert"および"prefix"とは併用できません。

insert    クライアントが、そのサーバーにアクセスできるcookieをまだ
          持っていない場合に、HAProxyがサーバーのレスポンスに
          接続先固定用のcookieを挿入することを示します。

          "preserve"を併用しない場合、サーバーが同名のcookieを発行すると、
          処理前に削除します。このため、既存の"rewrite"モードの構成から
          移行する用途にも使えます。cookieはセッションcookieとなり、
          クライアントのディスクには保存されません。デフォルトでは、
          "indirect"を追加しない限り、クライアントが送るcookieは
          サーバーにも渡されます。キャッシュの影響を考慮すると、通常は
          "nocache"または"postonly"を追加するのがよいでしょう（後述）。
          "insert"は"rewrite"および"prefix"と併用できません。

prefix    接続先固定専用のcookieを使う代わりに、既存のcookieに情報を
          追加することを示します。クライアントがcookieを一つしか扱えず、
          アプリケーションがすでにそれを必要としているような特殊な環境で、
          必要になる場合があります。サーバーが<name>という名前のcookieを
          設定するたびに、その先頭にサーバーの識別子と区切り文字を付けます。
          クライアントからのすべてのリクエストでは、この接頭辞を取り除き、
          サーバーが自身の発行したcookieをそのまま受け取れるようにします。
          すべてのリクエストとレスポンスが変更対象となるため、
          トンネルモードでは動作しません。"prefix"は"rewrite"および
          "insert"と併用できません。注意："indirect"と"prefix"を
          併用しないことを強く推奨します。併用すると、サーバーによる
          cookieの更新がクライアントに送られません。

indirect  リクエストを処理したサーバーに対応する有効なcookieを
          クライアントがすでに持っている場合、新たなcookieを発行しません。
          サーバー自身がそのcookieを設定した場合は、"preserve"も
          指定していなければ削除します。"insert"モードではさらに、
          サーバーに転送するリクエストからcookieを取り除き、
          アプリケーションから接続先固定の仕組みが完全に見えなくなります。
          注意："indirect"と"prefix"を併用しないことを強く推奨します。
          併用すると、サーバーによるcookieの更新がクライアントに送られません。

nocache   クライアントとHAProxyの間にキャッシュがある場合、insertモードと
          併用することを推奨します。cookieを挿入する必要があるときに、
          キャッシュ可能なレスポンスにキャッシュ不可の印を付けます。
          たとえば、キャッシュ可能なホームページに接続先固定用のcookieを
          すべて追加すると、全クライアントが外側のキャッシュからページを
          取得し、同じcookieを共有してしまいます。その結果、一台の
          サーバーに他よりはるかに多くのトラフィックが集中するため、
          この指定は重要です。"insert"と"postonly"も参照してください。

postonly  POSTリクエストへのレスポンスにのみcookieを挿入します。
          POSTのレスポンスはキャッシュされないため、接続先固定用のcookieが
          キャッシュに入ることを確実に防ぐ、"nocache"の代替手段となります。
          大半のサイトは、通常ログインリクエストである最初のPOSTまでは
          接続先固定を必要としません。このため、接続先固定用のcookieが
          キャッシュに入る危険を避けつつ、キャッシュを最適化できる
          非常に効率的な方法です。
          "insert"と"nocache"も参照してください。

preserve  "insert"または"indirect"、あるいはその両方との組み合わせでのみ
          使用できます。接続先固定用のcookieをサーバー自身が発行できるように
          します。レスポンスにcookieがある場合、HAProxyは変更しません。
          たとえば、ログアウト要求の後に接続先固定を解除したい場合に
          役立ちます。そのためには、サーバーから無効な値（空など）または
          過去の日付を持つcookieを発行するだけで済みます。
          ヘルスチェックの"disable-on-404"と組み合わせると、ユーザーが
          ログアウト後に確実にサーバーを離れるため、完全な
          グレースフルシャットダウンが可能です。

httponly  cookieを挿入する際、HAProxyが"HttpOnly"属性を追加します。
          この属性により、ユーザーエージェントがcookieをHTTP以外の
          コンポーネントと共有しないようにします。
          属性の詳細はRFC6265を参照してください。

secure    cookieを挿入する際、HAProxyが"Secure"属性を追加します。
          この属性により、ユーザーエージェントが安全でない通信路で
          このcookieを送信しないようにします。つまり、このフラグ付きで
          受け取ったcookieは、SSL/TLS接続でのみ送信します。
          属性の詳細はRFC6265を参照してください。

domain    cookieを挿入するドメインを指定できます。有効なドメイン名を
          パラメーターとしてちょうど一つ指定する必要があります。
          ドメイン名がドットで始まる場合、ブラウザーはその名前で終わる
          すべてのホストでcookieを使えます。このオプションを繰り返して、
          複数のドメイン名を指定することもできます。一部のブラウザーでは
          ドメイン数の上限が低い場合があるため、注意してください。
          参考までに、MSIE 6またはFirefox 2に10ドメインを送った場合は、
          期待どおりに動作します。

maxidle   一定の未使用時間が経過した、挿入済みのcookieを無視できるように
          します。insertモードのcookieでのみ動作します。クライアントに
          cookieを送る際、その発行日時も送信します。その後cookieが
          提示されたとき、発行日時からパラメーターで指定した時間（秒）を
          超えていれば無視します。超えていなければ、クライアントに
          レスポンスを送る際に、必要に応じて日時を更新します。
          ブラウザーを閉じないユーザーが同じサーバーに長くとどまるのを
          防ぐのに、特に有効です（サーバー群の規模を変更した後など）。
          このオプションを設定した状態でcookieに日時がない場合は、常に
          受け入れますが、レスポンスでは更新します。これにより、管理者が
          自分のサイトにアクセスする手段を維持できます。現在より24時間を
          超えて未来の日時を持つcookieは無視します。この動作により、
          ユーザーをサイトから追い出す危険を避けながら、管理者が
          タイムゾーンの問題を修正できます。

maxlife   使用中かどうかにかかわらず、一定の有効期間を過ぎた挿入済みの
          cookieを無視できるようにします。insertモードのcookieでのみ
          動作します。初めてクライアントにcookieを送る際、その発行日時も
          送信します。その後cookieが提示されたとき、発行日時から
          パラメーターで指定した時間（秒）を超えていれば無視します。
          リクエスト中のcookieに日時がない場合は、受け入れて日時を設定します。
          現在より24時間を超えて未来の日時を持つcookieは無視します。
          この動作により、ユーザーをサイトから追い出す危険を避けながら、
          管理者がタイムゾーンの問題を修正できます。maxidleとは異なり、
          この日時は更新せず、最初の訪問日時だけを使用します。
          maxidleとmaxlifeは同時に使用できます。ブラウザーを閉じない
          ユーザーが同じサーバーに長くとどまるのを防ぐのに、特に有効です
          （サーバー群の規模を変更した後など）。一定時間の経過後に必ず
          再割り当てを行う点で、maxidleより強い制約です。

dynamic   動的なcookieを有効にします。サーバーのIPアドレスとポート、
          バックエンドの"dynamic-cookie-key"で指定した秘密鍵に基づいて、
          サーバーごとにセッションcookieを動的に生成します。
          IPアドレスが変わるたびに再生成し、IPv4/IPv6でのみ生成します。

attr      cookieを挿入する際、HAProxyが追加の属性を付けます。
          属性値には、制御文字と";"以外の任意の文字を使用できます。
          このオプションは繰り返し指定できます。
```

HTTPバックエンドごとに接続先を固定するクッキーは1つだけ指定でき、defaultsセクションで宣言できます。クッキーの値は、"server"ステートメントの"cookie"キーワードの後に指定された値になります。特定のサーバーにクッキーが宣言されていない場合、クッキーは設定されません。

例：

```text
cookie JSESSIONID prefix
cookie SRV insert indirect nocache
cookie SRV insert postonly indirect
cookie SRV insert indirect nocache maxidle 30m maxlife 8h
```

参照："balance source"、"capture cookie"、"server"、"ignore-persist"。

<a id="entry-4-2-declare-capture"></a>

**`declare capture [ request | response ] len <length>`**

```haproxy
declare capture [ request | response ] len <length>
```

キャプチャスロットを宣言します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<length> キャプチャーに許可する長さです。
```

この宣言はフロントエンドまたはlistenセクションでのみ利用可能ですが、予約されたスロットはバックエンドでも使用できます。"request"キーワードはリクエストで使用するキャプチャスロットを割り当て、"response"キーワードはレスポンスで使用するキャプチャスロットを割り当てます。

関連項目："capture-req"、"capture-res"（サンプルコンバーター）、"capture.req.hdr"、"capture.res.hdr"（サンプル取得）、"http-request capture"および"http-response capture"。

<a id="entry-4-2-default-server"></a>

**`default-server [param*]`**

```haproxy
default-server [param*]
```

バックエンド内のサーバーのデフォルトオプションを変更します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<param*>  このサーバーのパラメーターの一覧です。"default-server"
          キーワードには多数のオプションがあり、専用のセクションで
          詳しく説明しています。詳細はセクション5を
          参照してください。
```

例：

```text
default-server inter 1000 weight 13
```

関連項目："server"、およびサーバーオプションに関する[セクション5](/ja/haproxy/bind-and-server-options/)。

<a id="entry-4-2-default-backend"></a>

**`default_backend <backend>`**

```haproxy
default_backend <backend>
```

どの"use_backend"ルールにも一致しなかった場合に使用するバックエンドを指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<backend> 使用するバックエンドの名前です。
```

"use_backend"キーワードを使用してフロントエンドとバックエンド間でコンテンツスイッチングを行う場合、どのルールにも一致しなかったときに使用するバックエンドを指定しておくと便利なことがよくあります。一般に、振り分け先が決まらないすべてのリクエストを受け取る動的バックエンドです。

バックエンドが無効化または非公開になっている場合、そのバックエンドを対象とするdefault_backendルールは無視され、ストリーム処理は元のプロキシのままになります。

例：

```text
use_backend     dynamic  if  url_dyn
use_backend     static   if  url_css url_img extension_img
default_backend dynamic
```

参照："use_backend"。

<a id="entry-4-2-description"></a>

**`description <string>`**

```haproxy
description <string>
```

listen、フロントエンド、またはバックエンドの説明を記述します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

引数：文字列

HAProxyのHTML統計ページで関連オブジェクトを説明する文を追加できます。説明は、該当オブジェクト名の右側に表示されます。`<string>`引数内でバックスラッシュによるスペースのエスケープは必要ありません。

<a id="entry-4-2-disabled"></a>

**`disabled`**

```haproxy
disabled
```

プロキシ、フロントエンド、またはバックエンドを無効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

"disabled"キーワードは、主にリッスンポートを解放するため、またはサービスを一時的に無効にするために、インスタンスを無効にします。インスタンス自体は作成され、設定も検査されますが、"stopped"状態で作成され、統計にもその状態で表示されます。トラフィックを受信せず、ヘルスチェックやログも送信しません。"defaults"セクションに"disabled"キーワードを追加すると、多数のインスタンスを一括で無効にできます。

デフォルトでは、無効化されたバックエンドはコンテンツスイッチングの対象にできません。ただし、"force-be-switch"を使用すると、トラフィックの一部はこの制限を無視できます。

参照："enabled"、"force-be-switch"。

<a id="entry-4-2-dispatch"></a>

**`dispatch <address>:<port>   (deprecated)`**

```haproxy
dispatch <address>:<port>   (deprecated)
```

デフォルトサーバーのアドレスを設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<address> デフォルトサーバーのIPv4アドレスです。代わりに、名前解決可能な
          ホスト名も使用できますが、この名前は起動時に解決されます。

<ports>   必須のポート指定です。すべての接続はこのポートに送られます。
          通常のサーバーで使用できるポートオフセットは使用できません。
```

"dispatch"キーワードは、他のサーバーが接続を受け付けられない場合に使用するデフォルトサーバーを指定します。過去には、接続先を固定しない接続を補助的なロードバランサーに転送するために使用されていました。単純な構文のため、単純なTCPリレーにも使われていました。設定を明確にするため、このキーワードを使わず、代わりに"server"ディレクティブを使用することを推奨します。

このキーワードは、内部的な制限（SSLやアイドル接続などをサポートしない）のため、3.3で非推奨となり、3.5で削除される予定です。使用すると警告が発生しますが、グローバルセクションで"expose-deprecated-directives"ディレクティブを有効にすると、この警告を抑制できます。

このディレクティブを使わずに実行する正しい方法は、同じアドレスとポートを持つサーバーを単に宣言することです。"dispatch"ディレクティブが他のサーバーと混在している場合、これらのサーバーは、負荷分散アルゴリズムで決して選ばれないよう、重みをゼロに設定することを推奨します。

例：

```text
backend deprecated_setup
    dispatch 192.168.100.100:80 # external load balancer's address
    server s1 192.168.100.1:80 cookie S1 check
    server s2 192.168.100.2:80 cookie S2 check

backend modern_setup
    server external_lb 192.168.100.100:80
    server s1 192.168.100.1:80 cookie S1 check weight 0
    server s2 192.168.100.2:80 cookie S2 check weight 0
```

参照："server"。

<a id="entry-4-2-dynamic-cookie-key"></a>

**`dynamic-cookie-key <string>`**

```haproxy
dynamic-cookie-key <string>
```

バックエンドの動的Cookieの秘密鍵を設定します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：使用する秘密鍵。

動的クッキーが有効化されている場合（クッキーの"dynamic"ディレクティブを参照）、各サーバーに対して、サーバーのIPアドレス、TCPポート、およびシークレットキーのハッシュを使用して動的クッキーが作成されます（"server"行で明示的に指定されていない場合）。これにより、サーバーが動的に追加または削除されても、複数のロードバランサー間でセッションの接続先を固定できます。

<a id="entry-4-2-enabled"></a>

**`enabled`**

```haproxy
enabled
```

プロキシ、フロントエンド、またはバックエンドを有効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

"enabled"キーワードは、defaultsで"disabled"に設定されている場合に、インスタンスを明示的に有効化するために使用されます。使用されることは非常にまれです。

参照："disabled"。

<a id="entry-4-2-errorfile"></a>

**`errorfile <code> <file>`**

```haproxy
errorfile <code> <file>
```

HAProxyが生成するエラーの代わりにファイルの内容を返します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<code>    HTTPステータスコードです。現在、HAProxyは200、400、401、403、404、
          405、407、408、410、413、414、425、429、431、500、501、502、503、504を
          生成できます。

<file>    完全なHTTPレスポンスを格納したファイルを指定します。
          レスポンスをHTMLエラーページと混同しないよう、一般的な慣例に従って
          ファイル名に".http"を付けることを推奨します。また、chrootの実行前に
          ファイルが読み込まれるため、絶対パスの使用を推奨します。
```

このキーワードは、サーバーが返すエラーを書き換えることを意図しているわけではなく、HAProxyが検出して返すエラーを対象とすることを理解することが重要です。そのため、対応するエラーは少数に限定されます。

"monitor-uri"ルールに一致するリクエストには、コード200が返されます。

ファイルはHAProxyの起動時に解析され、HTTP仕様に従って有効な内容でなければなりません。設定されたバッファーサイズ（BUFSIZE、通常は16 kB）を超えないことを推奨します。超えると内部エラーが返されます。また、すべてのサーバーがダウンしたときにクライアントとHAProxyの間でループが起き、画像の代わりにエラーが返されることを避けるため、ローカルコンテンツ（たとえば画像）への参照を含めないことも賢明です。最後に、"http-after-response"ルールが動作する余地を確保するため、レスポンスは(tune.bufsize - tune.maxrewrite)を超えることはできません（"tune.maxrewrite"を参照）。

ファイルは設定と同時に読み込まれ、メモリに保持されます。このため、プロセスがchrootされた後でもエラーが返され続け、プロセス実行中にファイルの変更は反映されません。これらのファイルを作成する簡単な方法は、403ステータスコードに関連付け、ブロックされたURLにリクエストを送信することです。

参照："http-error"、"errorloc"、"errorloc302"、"errorloc303"。

例：

```text
errorfile 400 /etc/haproxy/errorfiles/400badreq.http
errorfile 408 /dev/null  # work around Chrome pre-connect bug
errorfile 403 /etc/haproxy/errorfiles/403forbid.http
errorfile 503 /etc/haproxy/errorfiles/503sorry.http

```

<a id="entry-4-2-errorfiles"></a>

**`errorfiles <name> [<code> ...]`**

```haproxy
errorfiles <name> [<code> ...]
```

`<name>` http-errorsセクションで定義されたエラーファイルのすべて、または一部をインポートします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<name>  既存のhttp-errorsセクションの名前です。

<code>  HTTPステータスコードです。複数のステータスコードを列挙できます。
        現在、HAProxyは200、400、401、403、404、405、407、408、410、
        413、414、425、429、431、500、501、502、503、504を生成できます。
```

名前が`<name>`のhttp-errorsセクションで定義されたエラーが、現在のプロキシにインポートされます。ステータスコードが指定されていない場合、http-errorsセクションのすべてのエラーファイルがインポートされます。そうでない場合、列挙されたステータスコードに関連するエラーファイルのみがインポートされます。これらのエラーファイルは、プロキシで既に定義されたカスタムエラーを上書きし、その後に定義されたもので上書きされる場合もあります。機能的には、"errorfile"ディレクティブを使ってすべてのエラーファイルを手動で宣言することとまったく同じです。

関連項目："http-error"、"errorfile"、"errorloc"、"errorloc302"、"errorloc303"、およびhttp-errorsに関する[セクション12.4](/ja/haproxy/other-sections/#section-12-4)。

例：

```text
errorfiles generic
errorfiles site-1 403 404

```

<a id="entry-4-2-errorloc"></a>

**`errorloc <code> <url>`**

```haproxy
errorloc <code> <url>
errorloc302 <code> <url>
```

HAProxyが生成するエラーの代わりに、URLへのHTTPリダイレクトを返します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<code>    HTTPステータスコードです。現在、HAProxyは200、400、401、403、404、
          405、407、408、410、413、414、425、429、431、500、501、502、503、504を
          生成できます。

<url>     "Location"ヘッダーの正確な内容です。同じサイトでホストされる
          エラーページへの相対URI、または別のサイトのエラーページを示す
          絶対URIを指定できます。相対URI自体が同じエラー（500など）を
          生成し得る場合、リダイレクトループを避けるため、特に注意することを
          推奨します。
```

このキーワードは、サーバーが返すエラーを書き換えることを意図しているわけではなく、HAProxyが検出して返すエラーを対象とすることを理解することが重要です。そのため、対応するエラーは少数に限定されます。

"monitor-uri"ルールに一致するリクエストには、コード200が返されます。

両方のキーワードはHTTP 302ステータスコードを返す点に注意してください。これはクライアントに指定されたURLを同じHTTPメソッドで取得するように通知します。POSTなどのGET以外のメソッドの場合、クライアントに送られたURLがGET以外を許可していないことがあり、大きな問題になる場合があります。この問題を回避するには、"errorloc303"を使用してください。これはHTTP 303ステータスコードを返し、URLをGETリクエストで取得しなければならないことをクライアントに示します。

参照："http-error"、"errorfile"、"errorloc303"。

<a id="entry-4-2-errorloc303"></a>

**`errorloc303 <code> <url>`**

```haproxy
errorloc303 <code> <url>
```

HAProxyが生成するエラーの代わりに、URLへのHTTPリダイレクトを返します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<code>    HTTPステータスコードです。現在、HAProxyは200、400、401、403、404、
          405、407、408、410、413、414、425、429、431、500、501、502、503、504を
          生成できます。

<url>     "Location"ヘッダーの正確な内容です。同じサイトでホストされる
          エラーページへの相対URI、または別のサイトのエラーページを示す
          絶対URIを指定できます。相対URI自体が同じエラー（500など）を
          生成し得る場合、リダイレクトループを避けるため、特に注意することを
          推奨します。
```

このキーワードは、サーバーが返すエラーを書き換えることを意図しているわけではなく、HAProxyが検出して返すエラーを対象とすることを理解することが重要です。そのため、対応するエラーは少数に限定されます。

"monitor-uri"ルールに一致するリクエストには、コード200が返されます。

両方のキーワードはHTTP 303ステータスコードを返す点に注意してください。これはクライアントに指定されたURLを同じHTTP GETメソッドで取得するように通知します。これにより、"errorloc"と302コードに関連する一般的な問題が解決されます。HTTP/1.1以前に設計された非常に古いブラウザーでは対応していない可能性がありますが、現時点でそのような問題は報告されていません。

参照："http-error"、"errorfile"、"errorloc"、"errorloc302"。

<a id="entry-4-2-email-alert-from"></a>

**`email-alert from <emailaddr>`**

```haproxy
email-alert from <emailaddr>
```

メールアラートのエンベロープおよびヘッダーで使用する送信元メールアドレスを宣言します。このアドレスがメールアラートの送信元になります。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<emailaddr> メールアラートの送信元に使うメールアドレスです。
```

"email-alert mailers"と"email-alert to"も設定されている必要があり、これらが設定されていると、プロキシでメールアラートの送信が有効になります。

関連項目："email-alert level"、"email-alert mailers"、"email-alert myhostname"、"email-alert to"、およびmailersに関する[セクション12.3](/ja/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-level"></a>

**`email-alert level <level>`**

```haproxy
email-alert level <level>
```

メールアラートの送信対象となるメッセージの最大ログレベルを宣言します。
これはメールアラートの送信をフィルタリングする役割を果たします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<level> 次の8つのsyslogレベルのいずれかです。
          emerg alert crit err warning notice info  debug
        上記のsyslogレベルは、低いものから高いものへ順に並んでいます。
```

デフォルトのレベルはalertです。

"email-alert from"、"email-alert mailers"および"email-alert to"も設定されている必要があり、これらが設定されていると、プロキシでメールアラートの送信が有効になります。

次の場合にアラートが送信されます。

- 一時停止していないサーバーがダウンと判定され、`<level>`がalert以下の場合
- 一時停止中のサーバーがダウンと判定され、`<level>`がnotice以下の場合
- サーバーが稼働中と判定されるかdrain状態に入り、`<level>`がnotice以下の場合
- "option log-health-checks"が有効で、`<level>`がinfo以下であり、ヘルスチェックのステータス更新が発生した場合

関連項目："email-alert from"、"email-alert mailers"、"email-alert myhostname"、"email-alert to"、およびmailersに関する[セクション12.3](/ja/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-mailers"></a>

**`email-alert mailers <mailersect>`**

```haproxy
email-alert mailers <mailersect>
```

メールアラートの送信に使用するmailersを宣言します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<mailersect> メールアラートの送信に使うmailersセクションの名前です。
```

"email-alert from"と"email-alert to"も設定されている必要があり、これらが設定されていると、プロキシでメールアラートの送信が有効になります。

関連項目："email-alert from"、"email-alert level"、"email-alert myhostname"、"email-alert to"、およびmailersに関する[セクション12.3](/ja/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-myhostname"></a>

**`email-alert myhostname <hostname>`**

```haproxy
email-alert myhostname <hostname>
```

mailersとの通信に使用する宛先ホスト名アドレスを宣言します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<hostname> メールサーバーとの通信に使うホスト名です。
```

デフォルトではシステムのホスト名を使用します。

"email-alert from"、"email-alert mailers"および"email-alert to"も設定されている必要があり、これらが設定されていると、プロキシでメールアラートの送信が有効になります。

関連項目："email-alert from"、"email-alert level"、"email-alert mailers"、"email-alert to"、およびmailersに関する[セクション12.3](/ja/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-email-alert-to"></a>

**`email-alert to <emailaddr>`**

```haproxy
email-alert to <emailaddr>
```

メールアラートのエンベロープの宛先アドレスとヘッダーのToアドレスの両方を指定します。メールアラートの送信先となるアドレスです。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<emailaddr> メールアラートの宛先に使うメールアドレスです。
```

"email-alert mailers"と"email-alert to"も設定されている必要があり、これらが設定されていると、プロキシでメールアラートの送信が有効になります。

関連項目："email-alert from"、"email-alert level"、"email-alert mailers"、"email-alert myhostname"、およびmailersに関する[セクション12.3](/ja/haproxy/other-sections/#section-12-3)。

<a id="entry-4-2-error-log-format"></a>

**`error-log-format <fmt>`**

```haproxy
error-log-format <fmt>
```

フロントエンド側の接続エラー時に使用するログ形式文字列を指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

このディレクティブは、エラー、タイムアウト、再試行、再振り分け、またはHTTPステータスコード5xxに関連する情報を含むログに使用するログフォーマット文字列を指定します。このフォーマットは、"log-separate-errors"オプションの対象となるすべてのログ行に使用され、[セクション8.2.5](/ja/haproxy/configuration-logging/#section-8-2-5)で説明される接続エラーも含みます。

このディレクティブがdefaultsセクションで使用される場合、以降のすべてのフロントエンドは同じログフォーマットを使用します。カスタムログフォーマット文字列について詳しくは[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)を参照してください。

"error-log-format"ディレクティブは、それより前の"error-log-format"ディレクティブを上書きします。

<a id="entry-4-2-force-persist"></a>

**`force-persist { if | unless } <condition>`**

```haproxy
force-persist { if | unless } <condition>
```

ダウンしたサーバーへ接続先を強制的に固定する条件を宣言します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

デフォルトでは、リクエストはダウン状態のサーバーに配信されません。"option persist"を使用すると強制的に配信できますが、これは無条件に作用し、"option redispatch"が設定されている場合は有効なサーバーへ再振り分けされます。そのため、メンテナンス作業のために人為的にダウン状態とされたサーバーへ一部のリクエストを強制的に届ける方法は、ほとんどありません。

"force-persist"文では、ACLに基づくさまざまな条件を宣言できます。条件を満たすと、リクエストはサーバーのダウン状態を無視し、そのサーバーへの接続を試みます。これにより、ヘルスチェックにはまだエラーを返すサーバーを起動し、特別に設定したブラウザーでサービスをテストできます。便利な方法として、特定の送信元IPアドレスや特定のCookieを利用できます。Cookieには、テストページからブラウザー上で簡単に追加や削除ができる利点もあります。サービスを確認した後は、ヘルスチェックに有効なレスポンスを返すことで、一般にサービスを公開できます。

接続先の強制的な固定は、"if"条件が満たされた場合、または"unless"条件が満たされない場合に有効になります。これを使用すると、最終的な再振り分けは常に無効になります。

関連項目："option redispatch"、"ignore-persist"、"persist"、およびACLの使用方法に関する[セクション7](/ja/haproxy/acls-and-samples/)。

<a id="entry-4-2-external-check-command"></a>

**`external-check command <command>`**

```haproxy
external-check command <command>
```

external-checkの実行時に起動する実行可能ファイルです。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<command> 実行する外部コマンドです。
```

コマンドに渡す引数は次のとおりです。

`<proxy_address>` `<proxy_port>` `<server_address>` `<server_port>`

`<proxy_address>`および`<proxy_port>`は、IPv4、IPv6、またはUNIXソケットである最初のリスナーから得られます。UNIXソケットリスナーの場合、proxy_addressはソケットのパスとなり、`<proxy_port>`は文字列"NOT_USED"になります。バックエンドセクションではリスナーを特定できないため、`<proxy_address>`および`<proxy_port>`はともに文字列値"NOT_USED"を持ちます。

一部の値は環境変数でも渡されます。

環境変数：

```text
HAPROXY_PROXY_ADDR      最初のbindアドレス（存在する場合）。"backend"セクションなど、
                        該当しない場合は空です。

HAPROXY_PROXY_ID        バックエンドのIDです。

HAPROXY_PROXY_NAME      バックエンド名です。

HAPROXY_PROXY_PORT      最初のbindポート（存在する場合）。"backend"セクションや
                        UNIXソケットなど、該当しない場合は空です。

HAPROXY_SERVER_ADDR     サーバーのアドレスです。

HAPROXY_SERVER_CURCONN  サーバーの現在の接続数です。

HAPROXY_SERVER_ID       サーバーのIDです。

HAPROXY_SERVER_MAXCONN  サーバーの最大接続数です。

HAPROXY_SERVER_NAME     サーバー名です。

HAPROXY_SERVER_PORT     サーバーのポート（存在する場合）。UNIXソケットの場合は空です。

HAPROXY_SERVER_SSL      SSLを使用しない場合は"0"、使用する場合は"1"です。

HAPROXY_SERVER_PROTO    このサーバーで使用するプロトコルです。"cli"（haproxy CLI）、
                        "syslog"（syslog TCPサーバー）、"peers"（peers TCPサーバー）、
                        "h1"（HTTP/1.xサーバー）、"h2"（HTTP/2サーバー）、
                        "tcp"（その他のTCPサーバー）のいずれかです。

PATH                    コマンド実行時に使用するPATH環境変数は、
                        "external-check path"で設定できます。
```

コマンドが実行され、終了ステータスがゼロであれば、チェックは成功と見なされます。それ以外の場合は、チェックは失敗と見なされます。

例：

```text
external-check command /bin/true
```

参照："external-check"、"option external-check"、"external-check path"。

<a id="entry-4-2-external-check-path"></a>

**`external-check path <path>`**

```haproxy
external-check path <path>
```

external-checkの実行時に使用するPATH環境変数の値です。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<path> 外部コマンドの実行時に使うパスです。
```

デフォルトのパスは""です。

例：

```text
external-check path "/usr/bin:/bin"
```

参照："external-check"、"option external-check"、"external-check command"。

<a id="entry-4-2-force-be-switch"></a>

**`force-be-switch { if | unless } <condition>`**

```haproxy
force-be-switch { if | unless } <condition>
```

バックエンドインスタンスが無効化または非公開の場合でも、コンテンツスイッチングで選択できるようにします。管理者は、外部に公開する前にサービスへのトラフィックをテストするためにこのルールを使用できます。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

参照："be-unpublished"、"disabled"。

<a id="entry-4-2-filter"></a>

**`filter <name> [param*]`**

```haproxy
filter <name> [param*]
```

プロキシに接続されたフィルターリストに、フィルター`<name>`を追加します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

引数：

```text
<name>     フィルター名です。公式にサポートされるフィルターは
           セクション9に記載されています。

<param*>   フィルター<name>が受け付けるパラメーターのリストです。
           これらのパラメーターの解析はフィルターが行います。
           サポートされるパラメーターの詳細は、対応するフィルターの
           ドキュメント（セクション9）を参照してください。
```

同じプロキシでフィルター行を複数回使用できます。必要に応じて同じフィルターを複数回参照できます。

例：

```text
listen
  bind *:80

  filter trace name BEFORE-HTTP-COMP
  filter compression
  filter trace name AFTER-HTTP-COMP

  compression algo gzip
  compression offload

  server srv1 192.168.0.1:80
```

関連項目: [セクション9](/ja/haproxy/filters/)。

<a id="entry-4-2-fullconn"></a>

**`fullconn <conns>`**

```haproxy
fullconn <conns>
```

サーバーがmaxconnに達するバックエンド負荷を指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<conns>   サーバーに最大接続数を使わせるための、
          バックエンド上の接続数です。
```

サーバーに"maxconn"パラメーターが指定されている場合、その同時接続数はこの値を超えません。さらに"minconn"パラメーターが指定されている場合、バックエンドの負荷に応じた動的な制限を示します。このサーバーは常に少なくとも`<minconn>`個の接続を受け入れ、`<maxconn>`を超えることはなく、バックエンドの同時接続数が`<conns>`を下回る場合、制限は両方の値の間で連続的に変化します。これにより、通常の負荷時にはサーバーの負荷を制限しつつ、高い負荷時には許容負荷を引き上げ、極端な負荷時にもサーバーを過負荷にしないようにできます。

この値を正確に設定するのは難しいため、HAProxyは自動的に、このバックエンドに分岐する可能性のあるすべてのフロントエンドのmaxconnの合計の10%を設定します（"use_backend"および"default_backend"ルールに基づく）。これにより、設定を省略しても安全です。ただし、動的な名前を含む"use_backend"は、一致するかどうかを判断できないため、カウントされません。

例：

```shell
# The servers will accept between 100 and 1000 concurrent connections each
# and the maximum of 1000 will be reached when the backend reaches 10000
# connections.
backend dynamic
   fullconn   10000
   server     srv1   dyn1:80 minconn 100 maxconn 1000
   server     srv2   dyn2:80 minconn 100 maxconn 1000
```

参照："maxconn"、"server"。

<a id="entry-4-2-guid"></a>

**`guid <string>`**

```haproxy
guid <string>
```

このプロキシの、大文字と小文字を区別するグローバルに一意なIDを指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

`<string>`は、すべてのHAProxy設定において、オブジェクトの種類にかかわらず一意でなければなりません。ユーザーが命名ポリシーを選択できるよう、形式は指定されていません。唯一の制限は長さで、127文字を超えることはできません。すべての英数字および'.'、':'、'-'、'\_'の各文字が有効です。関連項目："shm-stats-file"。

<a id="entry-4-2-hash-balance-factor"></a>

**`hash-balance-factor <factor>`**

```haproxy
hash-balance-factor <factor>
```

負荷上限付きコンシステントハッシュの分散係数を指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 不可 \| 可

引数：

```text
<factor> サーバーに送る同時リクエストの最大数を制御します。
         すべての稼働中サーバーの平均同時リクエスト数に対する
         割合を、パーセントで表します。
```

"hash-type consistent"を使用するサーバーに"hash-balance-factor"を指定すると、一部のハッシュバケットがほかのバケットよりはるかに多くのリクエストを受け取っても、一つのサーバーに同時にリクエストが集中しすぎるのを防ぐアルゴリズムを有効にします。`<factor>`を0（デフォルト）にすると、この機能は無効になります。それ以外では、`<factor>`は100より大きいパーセント値です。たとえば、`<factor>`が150の場合、どのサーバーの負荷も平均の1.5倍を超えることは許されません。サーバーの重みを使用している場合は、その重みも考慮します。

最初の候補のサーバーが不適格な場合、アルゴリズムはリクエストのハッシュに基づいて別のサーバーを選択し、余力のあるサーバーが見つかるまで続けます。`<factor>`を高い値に設定するとサーバー間の不均衡をより大きく許容し、`<factor>`を低い値に設定すると平均的にチェックするサーバーが多くなるため、パフォーマンスに影響します。妥当な値は125から200です。

この設定は、内部でコンシステントハッシュの仕組みを利用する"balance random"でも使用されます。

参照："balance"、"hash-type"。

<a id="entry-4-2-hash-preserve-affinity"></a>

**`hash-preserve-affinity { always | maxconn | maxqueue }`**

```haproxy
hash-preserve-affinity { always | maxconn | maxqueue }
```

サーバーが飽和状態またはキューが満杯の状態にあるときに、ハッシュ負荷分散を使用してストリームをサーバーに割り当てる方法を指定します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

次の値を指定できます。

    - "always"  : これはデフォルトの戦略です。サーバーが現在飽和しているかどうかにかかわらず、ハッシュに基づいてストリームがサーバーに割り当てられます。

    - "maxconn" : この戦略を選択すると、"maxconn"が設定されていて現在飽和しているサーバーはスキップされ、ハッシュリングをたどって別のサーバーが選択されます。"maxconn"を設定していないサーバーには影響しません。すべてのサーバーが飽和している場合、リクエストはハッシュリング上で最初に選択されたサーバーの直前にある最後のサーバーのキューに入れられます。

    - "maxqueue": この戦略を選択すると、"maxconn"が設定され、"maxqueue"がゼロ以外の値に設定されていて（キューサイズに制限がある）、現在キューが満杯のサーバーはスキップされます。ハッシュリングをたどって別のサーバーが選択されます。"maxconn"と"maxqueue"の双方の設定がそろっていないサーバーには影響しません。

参照："maxconn"、"maxqueue"、"hash-balance-factor"。

<a id="entry-4-2-hash-type"></a>

**`hash-type <method> <function> <modifier>`**

```haproxy
hash-type <method> <function> <modifier>
```

ハッシュをサーバーに対応付ける方法を指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<method> は、<function>で計算したハッシュからサーバーを選択する方法です。

  map-based   ハッシュテーブルは、稼働中のすべてのサーバーを含む静的な配列です。
              ハッシュの分布は非常に均等で、重みも考慮します。ただし静的なので、
              サーバーの稼働中に重みを変更しても無視されます。つまり、
              スロースタートは行われません。また、配列内の位置によってサーバーを
              選ぶため、サーバー数が変わると対応付けの大半が変わります。
              サーバーが稼働または停止したときや、サーバー群にサーバーを追加した
              ときに、ほとんどの接続が別のサーバーへ再分配されるということです。
              これは、たとえばキャッシュを使う場合に不都合となることがあります。

  consistent  ハッシュテーブルは、各サーバーを多数の位置に配置したツリーです。
              ツリー内でハッシュキーを検索し、最も近いサーバーを選びます。
              このハッシュ方式は動的で、サーバーの稼働中の重み変更をサポートする
              ため、スロースタート機能と併用できます。サーバーが稼働または停止した
              際に、そのサーバーとの対応付けだけが移動するという利点があります。
              サーバー群にサーバーを追加しても、再分配されるのは対応付けのごく一部だけ
              なので、キャッシュに最適な方式です。ただし、原理上、分布が非常に
              均等になることはなく、より均等にするためにサーバーの重みやIDの
              調整が必要になる場合があります。複数のロードバランサーで同じ分布を
              得るには、各サーバーのIDを、すべてのロードバランサーで完全に
              揃えることが重要です。
              注意：ハッシュ関数を指定しない場合、consistentハッシュはsdbmと
              avalancheを使用します。

<function> は、使用するハッシュ関数です。

   sdbm   この関数は、もともとsdbmデータベースライブラリー（ndbmを
          パブリックドメインとして再実装したもの）用に作られました。
          ビットをよくかき混ぜるため、キーの分布が改善し、分割が少なくなることが
          分かっています。分布のよい汎用ハッシュ関数としても適していますが、
          サーバーの重みの合計が64の倍数の場合は例外です。この場合は、
          avalanche修飾子の適用が役立つことがあります。

   djb2   この関数は、何年も前にDan Bernsteinがcomp.lang.cで最初に提案しました。
          特定のワークロードでは、sdbmよりもよい分布になることが研究で
          示されています。一般にテキスト入力には適していますが、数字だけの
          入力や、サーバーの重みの合計が33の倍数になる場合には、avalanche修飾子も
          使用しないと、分布が極端に悪くなることがあります。

   wt6    この関数は、以前にほかの関数を試験していた際に、HAProxy用に設計されました。
          ほかの関数ほど分布は均等ではありませんが、入力データの集合やサーバー数の
          影響をはるかに受けにくくなっています。コンシステントハッシュや、送信元
          IPアドレス、URLパラメーター内の訪問者識別子などの数値データをハッシュする
          場合には、sdbm+avalancheやdjb2+avalancheの代わりに使う価値があります。

   crc32  Ethernet、gzip、PNGなどで使用される、最も一般的なCRC32の実装です。
          ほかの関数より低速ですが、特に文字列に使用すると、分布がよくなったり、
          結果が予測されにくくなったりする場合があります。

   none   キーをハッシュせず、そのままハッシュ値として使用します。この目的の
          コンバーターで明示的にキーをハッシュし、haproxyにその結果を直接使用させる
          場合に役立ちます。キーが文字列でなければ文字列に変換し、それを整数として
          解析して、その値をキーとして使います。入力キーの型によっては、
          この処理に適さないものもあります（IPアドレスなど）。

<modifier> は、キーのハッシュ後に適用する、省略可能な処理を指定します。

   avalanche   このディレクティブは、上記ハッシュ関数の結果をそのまま使うべきではなく、
               まず4バイトの完全なavalancheハッシュを適用する必要があることを指定します。
               この処理の目的は、前のハッシュで得られたビットを混ぜ、入力が
               限られた値を含む場合や、サーバー数がハッシュの構成要素のいずれかの
               倍数（SDBMでは64、DJB2では33）である場合に、望ましくない影響を
               防ぐことです。avalancheを有効にすると、結果が予測されにくくなる
               傾向がありますが、元の関数を使った場合ほど分布は均等ではなくなります。
               ワークロードによっては試験が必要になることがあります。
               このハッシュは、Bob Jenkinsが提案した多数のハッシュの一つです。
```

デフォルトのハッシュタイプは"map-based"であり、ほとんどの用途で推奨されます。デフォルトの関数は"sdbm"です。関数はハッシュ対象となる値の範囲に基づいて選ぶことを推奨します。

参照："balance"、"hash-balance-factor"、"hash-preserve-affinity"、"server"。

<a id="entry-4-2-http-after-response"></a>

**`http-after-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-after-response <action> <options...> [ { if | unless } <condition> ]
```

すべてのレイヤー7レスポンス（サーバー、アプレット/サービス、内部レスポンス）のアクセス制御です。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

http-after-responseステートメントはレイヤー7処理に適用されるルールセットを定義します。ルールは、フロントエンド、listen、またはバックエンドセクションで宣言された順序に従って評価されます。これらのルールはレスポンスに適用されるため、バックエンドのルールが先に適用され、その後フロントエンドのルールが適用されます。どのルールにも、任意でACLに基づく条件を後置できます。その場合、条件が真と評価されたときにのみルールが評価されます。

http-responseルールとは異なり、これらはサーバーからのレスポンスだけでなく、HAProxyが生成するすべてのレスポンスにも適用されます。これらのルールは、データ転送フェーズの前、レスポンス解析の最後に評価されます。

条件はアクションが実行される直前に評価され、アクションは正確に1回実行されます。したがって、条件の評価に使われる要素がアクションによって変更されても問題ありません。また、同じ条件を複数のアクションで共有できるため、最初のアクションが条件の評価結果を変えるだけで、残りのアクションを暗黙的に無効にできます。これは、変数が空の場合に、さまざまなソースから値を割り当てようとするときなどに利用されます。インスタンスあたりの"http-after-response"ステートメントの数に制限はありません。

構文における"http-after-response"の直後の最初のキーワードはルールのアクションであり、必要に応じてアクションに応じた数の引数が続くことがあります。対応するアクションおよびそれぞれの構文は、[セクション4.3](/ja/haproxy/proxies/#section-4-3)「アクション」に記載されています（"HTTP Aft"にチェックがあるアクションを参照してください）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

注意：リクエスト解析の初期段階で発生したエラーは、HTTP解析を行う前に、より低いレベルでマルチプレクサーが処理します。したがって、これらのエラーに対してはhttp-after-responseルールセットは評価されません。

例：

```text
http-after-response set-header Strict-Transport-Security "max-age=31536000"
http-after-response set-header Cache-Control "no-store,no-cache,private"
http-after-response set-header Pragma "no-cache"

```

<a id="entry-4-2-http-check-comment"></a>

**`http-check comment <string>`**

```haproxy
http-check comment <string>
```

後続のhttp-checkルールのコメントを定義します。ルールが失敗した場合にログに記録されます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<string>  後続のhttp-checkルールが失敗した場合に、
          ログに追加するコメントメッセージです。
```

connect、send、expectルールにのみ使用できます。わかりやすいエラー報告を作成するのに役立ちます。

参照："option httpchk"、"http-check connect"、"http-check send"、"http-check expect"。

<a id="entry-4-2-http-check-connect"></a>

**`http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]`**

```haproxy
http-check connect [default] [port <expr>] [addr <ip>] [send-proxy]
                   [via-socks4] [ssl] [sni <sni>] [alpn <alpn>] [linger]
                   [proto <name>] [comment <msg>]
```

HTTPヘルスチェックを実行するため、新しい接続を開きます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

default      server行のデフォルトオプションを使用してヘルスチェックを行います。
             サーバーオプションは、再定義されていない場合にのみ使用します。

port <expr>  設定しない場合、チェック用ポートまたはサーバーのポートを使用します。
             HAProxyが接続を開く宛先を指定します。
             <port>は1から65535までの有効なTCPポートの整数値、または
             サンプル取得式でなければなりません。

addr <ip>    ヘルスチェックを行うIPアドレスを定義します。

send-proxy   PROXYプロトコル文字列を送信します。

via-socks4   アップストリームのsocks4プロキシを使用する発信ヘルスチェックを有効にします。

ssl          暗号化された接続を開きます。

sni <sni>    SSL経由のヘルスチェックに使用するSNIを指定します。

alpn <alpn>  ALPNで通知するプロトコルを定義します。プロトコルのリストは
             "h2,http/1.1"など、プロトコル名のカンマ区切りリストです。
             設定しない場合、サーバーのALPNを使用します。

proto <name> この接続に使用するマルチプレクサーのプロトコルを強制します。
             HTTP muxプロトコルであり、バックエンド側で使用可能でなければ
             なりません。利用可能なプロトコルの一覧はhaproxy -vvで表示されます。

linger       単一のRSTを使用せず、接続を正常に閉じます。
```

tcp-checkヘルスチェックと同様に、HTTPヘルスチェックを実行するための接続を設定できます。このディレクティブは、複数のリクエスト/レスポンスをやり取りするシナリオを記述するときにも使用することを推奨します。このシナリオでは、異なるポートやサーバーを使う場合もあります。

server行にもserver portディレクティブにもTCPポートが設定されていない場合、http-checkシーケンスの最初のステップとして"http-check connect"でポートを指定しなければなりません。

http-checkルールセットでは'connect'が必須であり、ルールセットは'connect'ルールで開始しなければなりません。管理者が自分の操作を理解したうえで実行するようにすることが目的です。

connectでルールセットを開始しなければならない場合でも、その前にset-var、unset-var、commentルールを置くことができます。

例：

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option httpchk

http-check connect
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399
http-check connect port 443 ssl sni haproxy.1wt.eu
http-check send meth GET uri / ver HTTP/1.1 hdr host haproxy.1wt.eu
http-check expect status 200-399

server www 10.0.0.1 check port 80
```

参照："option httpchk"、"http-check send"、"http-check expect"。

<a id="entry-4-2-http-check-disable-on-404"></a>

**`http-check disable-on-404`**

```haproxy
http-check disable-on-404
```

ヘルスチェックへのHTTP/404レスポンスを受けた場合に、メンテナンスモードを有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

このオプションを設定すると、HTTPコード404を返すサーバーを以後の負荷分散から除外しますが、接続先が固定された接続は引き続き受け付けます。Web管理者がサーバーをグレースフルシャットダウンするための便利な方法です。また、このモード中にサーバーの障害を検出しても、alertではなくnoticeだけを生成します。サーバーが再び2xxまたは3xxを返すと、直ちにサーバー群へ戻します。このモードのサーバーは、統計ページの状態欄に"NOLB"と表示されます。このオプションは"httpchk"オプションと組み合わせた場合にのみ動作します。"http-check expect"と併用すると、このオプションが優先され、404レスポンスは引き続きソフトストップとして扱われます。すでに停止しているサーバーは、404を返しても停止したままです。このオプションは稼働中のサーバーに対してのみ評価します。

参照："option httpchk"、"http-check expect"。

<a id="entry-4-2-http-check-expect"></a>

**`http-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
http-check expect [min-recv <int>] [comment <msg>]
                  [ok-status <st>] [error-status <st>] [tout-status <st>]
                  [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                  [!] <match> <pattern>
```

HTTPヘルスチェックでレスポンスの内容や特定のステータスコードを考慮するようにします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

min-recv  省略可能で、現在のexpectルールの評価に必要な最小データ量を定義できます。
          受信バイト数がこの下限未満の場合、チェックは追加のデータを待ちます。
          このオプションは、曖昧な一致ルールを解決したり、まだ不完全と分かっている
          内容に対して高コストの正規表現による照合を行わないようにするために
          使用できます。完全一致の文字列を使用する場合、文字列の長さとこの
          パラメーターのうち、小さい方を使用します。-1を設定すると、この
          パラメーターは無視されます。expectルールに一致しない場合、チェックは
          追加のデータを待ちます。0を設定すると、評価結果は常に確定的になります。

ok-status <st>     省略可能で、expectルールの評価が成功し、かつtcp-checkルールセットの
                   最後のルールである場合に、チェックの状態を設定できます。
                   "L7OK"、"L7OKC"、"L6OK"、"L4OK"をサポートします。
                     - L7OK : レイヤー7のチェックに成功
                     - L7OKC: レイヤー7のチェックに条件付きで成功し、サーバーをNOLB状態に設定
                     - L6OK : レイヤー6のチェックに成功
                     - L4OK : レイヤー4のチェックに成功
                   デフォルトでは"L7OK"を使用します。

error-status <st>  省略可能で、expectルールの評価中にエラーが発生した場合に、
                   チェックの状態を設定できます。"L7OKC"、"L7RSP"、"L7STS"、
                   "L6RSP"、"L4CON"をサポートします。
                     - L7OKC: レイヤー7のチェックに条件付きで成功し、サーバーをNOLB状態に設定
                     - L7RSP: レイヤー7の無効なレスポンス - プロトコルエラー
                     - L7STS: レイヤー7のレスポンスエラー。HTTP 5xxなど
                     - L6RSP: レイヤー6の無効なレスポンス - プロトコルエラー
                     - L4CON: レイヤー1-4の接続の問題
                   デフォルトでは"L7RSP"を使用します。

tout-status <st>   省略可能で、expectルールの評価中にタイムアウトが発生した場合に、
                   チェックの状態を設定できます。"L7TOUT"、"L6TOUT"、"L4TOUT"を
                   サポートします。
                     - L7TOUT: レイヤー7（HTTP/SMTP）のタイムアウト
                     - L6TOUT: レイヤー6（SSL）のタイムアウト
                     - L4TOUT: レイヤー1-4のタイムアウト
                   デフォルトでは"L7TOUT"を使用します。

on-success <fmt>   省略可能で、expectルールの評価が成功し、かつtcp-checkルールセットの
                   最後のルールである場合に、ログに記録する情報メッセージを変更できます。
                   <fmt>はカスタムログ形式文字列です（セクション8.2.6を参照）。

on-error <fmt>     省略可能で、expectルールの評価中にエラーが発生した場合に、
                   ログに記録する情報メッセージを変更できます。<fmt>はカスタムログ形式
                   文字列です（セクション8.2.6を参照）。

status-code <expr> 省略可能で、成功時またはエラー時にログに記録するチェックの
                   ステータスコードを設定できます。<expr>はサンプル取得の後に
                   コンバーターを続けた、標準的なHAProxyの式です。

<match>   レスポンス内で特定のパターンを検索する方法を示すキーワードです。
          "status"、"rstatus"、"hdr"、"fhdr"、"string"、"rstring"のいずれかです。
          キーワードの前に感嘆符（"!"）を付けると、一致を否定できます。
          感嘆符とキーワードの間には空白を入れられます。
          サポートされるキーワードの詳細は後述します。

<pattern> 検索するパターンです。文字列、正規表現、または複数の引数を持つ
          より複雑なパターンを指定できます。文字列パターンに空白が含まれる場合、
          通常のバックスラッシュ（'\'）でエスケープする必要があります。
```

デフォルトでは、"option httpchk"はレスポンスステータス2xxおよび3xxを有効とみなし、それ以外を無効とみなします。"http-check expect"を使用すると、有効または無効とみなす内容を定義します。バックエンド内では、"http-check"ステートメントは1つだけサポートされています。サーバーが応答しない、またはタイムアウトした場合、チェックは明らかに失敗します。利用可能な一致条件は次のとおりです：

```text
status <codes>:  <codes>文字列を解析して得られるステータスコードを照合します。
                  ステータスコードまたはコード範囲のカンマ区切りリストでなければ
                  なりません。レスポンスのステータスコードがリスト内のいずれかの
                  コードに一致するか、いずれかの範囲に含まれる場合、ヘルスチェックの
                  レスポンスは有効とみなします。"status"キーワードの前に"!"を
                  付けた場合、ステータスコードが一致するとレスポンスは無効とみなします。

rstatus <regex>: HTTPステータスコードを正規表現で照合します。レスポンスの
                  ステータスコードが式に一致する場合、ヘルスチェックのレスポンスは
                  有効とみなします。"rstatus"キーワードの前に"!"を付けた場合、
                  ステータスコードが一致するとレスポンスは無効とみなします。
                  主に複数のコードの確認に使用します。

hdr  { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  HTTPレスポンスヘッダーを指定したヘッダーパターンで照合します。
                  名前のパターンは必須ですが、値のパターンは省略可能です。
                  値のパターンを指定しない場合、ヘッダーの存在だけを確認します。
                  <meth>は、ヘッダー名またはヘッダー値に適用する照合方法です。
                  サポートする照合方法は、"str"（完全一致）、"beg"（前方一致）、
                  "end"（後方一致）、"sub"（部分文字列の一致）、"reg"（正規表現による一致）
                  です。指定しない場合、完全一致を使用します。"name-lf"パラメーターを
                  使用すると、<name>をカスタムログ形式文字列として評価します
                  （セクション8.2.6を参照）。"value-lf"パラメーターを使用すると、
                  <value>をログ形式文字列として評価します。これらのパラメーターは
                  正規表現による照合方法と併用できません。最後に、ヘッダー値は
                  カンマ区切りリストとして扱います。ヘッダー名の照合では
                  大文字と小文字を区別しません。

fhdr { name | name-lf } [ -m <meth> ] <name>
     [ { value | value-lf } [ -m <meth> ] <value>:
                  HTTPレスポンスヘッダーを指定した完全なヘッダーパターンで照合します。
                  ヘッダー値全体を照合し、カンマを区切り文字として扱わない点を除き、
                  "hdr"キーワードとまったく同じ動作をします。

string <string>: HTTPレスポンス本文に、指定した文字列が完全一致で含まれるかを調べます。
                  レスポンス本文にその文字列がそのまま含まれる場合、ヘルスチェックの
                  レスポンスは有効とみなします。"string"キーワードの前に"!"を
                  付けた場合、本文にこの文字列が含まれるとレスポンスは無効とみなします。
                  動的ページの末尾に必須の語があるかを調べたり、チェック対象ページに
                  特定のエラー（スタックトレースなど）が現れたときに、
                  障害を検出するために使用できます。

rstring <regex>: HTTPレスポンス本文を正規表現で照合します。レスポンス本文が式に
                  一致する場合、ヘルスチェックのレスポンスは有効とみなします。
                  "rstring"キーワードの前に"!"を付けた場合、本文が式に一致すると
                  レスポンスは無効とみなします。動的ページの末尾に必須の語があるかを
                  調べたり、チェック対象ページに特定のエラー（スタックトレースなど）が
                  現れたときに、障害を検出するために使用できます。

string-lf <fmt>: HTTPレスポンス本文をカスタムログ形式文字列（セクション8.2.6を参照）で
                  照合します。ログ形式の規則に従う<fmt>の評価結果の文字列が
                  レスポンス本文に含まれる場合、ヘルスチェックのレスポンスは
                  有効とみなします。前に"!"を付けた場合、本文にその文字列が
                  含まれるとレスポンスは無効とみなします。
```

レスポンスは、グローバルな"tune.bufsize"オプションで定義されたサイズに制限されることに注意してください。デフォルトは16384バイトです。したがって、"string"または"rstring"を使用する場合、大きすぎるレスポンスには必須のパターンが含まれない可能性があります。大きなレスポンスがどうしても必要な場合は、グローバル変数を設定してデフォルトの最大サイズを変更できます。ただし、特に正規表現を使う場合、非常に大きなレスポンスの解析でCPUサイクルを浪費することがある点を念頭に置いてください。より小さなリソースをチェック対象にする方が常に望ましいです。

http-checkルールセットでは、最後のexpectルールは暗黙的に定義されることがあります。最後の"http-check send"の後にexpectルールが指定されていない場合、2xxまたは3xxステータスコードに一致する暗黙のexpectルールが定義されます。"http-check"ルールがまったくなく、"option httpchk"だけが設定されている場合にも、このルールが定義されます。

最後に、"http-check expect"が"http-check disable-on-404"と組み合わせられている場合、サーバーが404を返したときは後者が優先されます。

例：

```shell
# only accept status 200 as valid
http-check expect status 200,201,300-310

# be sure a sessid coookie is set
http-check expect hdr name "set-cookie" value -m beg "sessid="

# consider SQL errors as errors
http-check expect ! string SQL\ Error

# consider status 5xx only as errors
http-check expect ! rstatus ^5

# check that we have a correct hexadecimal tag before /html
http-check expect rstring <!--tag:[0-9a-f]*--></html>
```

参照："option httpchk"、"http-check connect"、"http-check disable-on-404"、"http-check send"。

<a id="entry-4-2-http-check-send"></a>

**`http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]`**

```haproxy
http-check send [meth <method>] [{ uri <uri> | uri-lf <fmt> }>] [ver <version>]
                [hdr <name> <fmt>]* [{ body <string> | body-lf <fmt> }]
                [comment <msg>]
```

HTTPヘルスチェック中に送信するリクエストに、ヘッダーのリスト、本文、またはその両方を追加できます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

meth <method>  リクエストに使用する任意のHTTPメソッドです。設定しない場合、
               "OPTIONS"メソッドを使用します。通常、サーバー側の処理が少なく、
               ログから簡単に除外できるためです。どのメソッドでも使用できますが、
               標準外のメソッドを考案することは推奨されません。

uri <uri>      任意の指定で、HTTPリクエストが参照するURIを文字列<uri>に設定します。
               デフォルトは"/"で、ほぼすべてのサーバーでデフォルトでアクセス可能ですが、
               他のどのURIにも変更できます。クエリー文字列も使用できます。

uri-lf <fmt>   任意の指定で、カスタムログ形式<fmt>（セクション8.2.6を参照）を
               使用してHTTPリクエストが参照するURIを設定します。デフォルトは"/"で、
               ほぼすべてのサーバーでデフォルトでアクセス可能ですが、
               他のどのURIにも変更できます。クエリー文字列も使用できます。

ver <version>  任意のHTTPバージョン文字列です。デフォルトは"HTTP/1.0"ですが、
               HTTP 1.0では正常に動作しないサーバーもあるため、HTTP/1.1への
               変更が役立つ場合があります。HTTP/1.1ではHostフィールドが必須なので、
               "hdr"引数で追加してください。

hdr <name> <fmt>  <name>で名前を指定し、<fmt>で値を定義したHTTPヘッダーフィールドを
                  追加します。値はセクション8.2.6で説明するカスタムログ形式の
                  規則に従います。

body <string>  HTTPヘルスチェックで送信するリクエストに、<string>で定義した
               本文を追加します。定義した場合、"Content-Length"ヘッダーも
               リクエストに自動的に追加されます。

body-lf <fmt>  HTTPヘルスチェックで送信するリクエストに、カスタムログ形式<fmt>
               （セクション8.2.6を参照）で定義した本文を追加します。定義した場合、
               "Content-Length"ヘッダーもリクエストに自動的に追加されます。
```

"option httpchk"ディレクティブで定義されたリクエスト行に加えて、これはHTTPヘルスチェック中に送信するリクエストにヘッダーと任意の本文を追加する正しい方法です。本文が定義されている場合、対応する"Content-Length"ヘッダーが自動的に追加されます。したがって、"http-check send"で指定するリクエストには、このヘッダーや"Transfer-encoding"ヘッダーを含めないことを推奨します。含まれている場合は無視されます。"option httpchk"行のバージョン文字列の後にヘッダーを追加する従来の方法は、現在非推奨です。

また、"http-check send"はHTTP keep-aliveをサポートしていません。hdrエントリーでConnectionヘッダーがすでに設定されていない限り、"Connection: close"ヘッダーが自動的に追加されることに留意してください。

Hostヘッダーとリクエストのauthorityが両方定義されている場合、自動的に同期されることに注意してください。HTTPリクエストを送信する際、リクエストにHostヘッダーが挿入されると、それに応じてリクエストのauthorityが更新されます。したがって、Hostヘッダーの値が、設定したリクエストのauthorityを上書きする場合があっても驚かないでください。

また、現在のところ、HTTP/1.1以上のリクエストにはHostヘッダーが自動的に追加されないことに注意してください。明示的に追加することを推奨します。

参照："option httpchk"、"http-check send-state"、"http-check expect"。

<a id="entry-4-2-http-check-send-state"></a>

**`http-check send-state`**

```haproxy
http-check send-state
```

HTTPヘルスチェックで状態ヘッダーの送出を有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

このオプションが設定されている場合、HAProxyは各サーバーがHAProxyによってどのように認識されているかを示すパラメーターのリストを含む特別なヘッダー"X-Haproxy-Server-State"を常に送信します。たとえば、HAProxyにアクセスできない状態でサーバーを操作し、オペレーターがHAProxyからまだ稼働中と認識されているか、またはファーム内で最後のサーバーかを確認する必要がある場合に使用できます。

ヘッダーはセミコロンで区切られたフィールドで構成され、最初のフィールドは単語（"UP"、"DOWN"、"NOLB"）です。その後に、状態遷移までに必要なチェックの総数に対する有効なチェック数が、統計インターフェースと同じ形式で続く場合があります。続くフィールドは"`<variable>`=`<value>`"の形式で、統計インターフェースに表示される値を順不同で示します：- 変数"address"は、バックエンドサーバーのアドレスを含みます。これはサーバー宣言の`<address>`フィールドに対応します。UNIXドメインソケットの場合、値は"unix"になります。

    - 変数"port"は、バックエンドサーバーのポートを含みます。これはサーバー宣言の`<port>`フィールドに対応します。UNIXドメインソケットの場合、値は"unix"になります。

    - 変数"name"は、バックエンド名、スラッシュ（"/"）、サーバー名の順に含みます。サーバーが複数のバックエンドでチェックされる場合に使用できます。

    - 変数"node"は、グローバルな"node"変数で設定されたHAProxyノード名を含みます。未指定の場合はシステムのホスト名が使用されます。

    - 変数"weight"は、サーバーの重みを示し、スラッシュ（"/"）の後にファームの合計重み（使用可能なサーバーのみをカウント）が続きます。これにより、このサーバーに障害が発生したときに他のサーバーが負荷を処理できるかどうかを把握できます。

    - 変数"scur"は、サーバー上の現在の同時接続数を示し、スラッシュ（"/"）の後に同じバックエンドのすべてのサーバーの接続数の合計が続きます。

    - 変数"qcur"は、サーバーのキューにある現在のリクエスト数を示します。

アプリケーションサーバーが受信するヘッダーの例：

```shell
>>>  X-Haproxy-Server-State: UP 2/3; name=bck/srv2; node=lb1; weight=1/2; \
       scur=13/22; qcur=0
```

参照："option httpchk"、"http-check disable-on-404"、"http-check send"。

<a id="entry-4-2-http-check-set-var"></a>

**`http-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
http-check set-var(<var-name>[,<cond>...]) <expr>
http-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

この操作は変数の内容を設定します。変数はインラインで宣言されます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<var-name>   変数の名前です。使用できるスコープは"proc"、"sess"、"check"のみです。
             詳細は、変数について説明するセクション2.8を参照してください。

 <cond>      変数を実際に設定するために、すべて真でなければならない条件の集合です
             （"ifnotempty"、"ifgt"など）。指定可能な条件の完全な一覧は、
             set-varコンバーターの説明を参照してください。

 <expr>      サンプル取得式です。後ろにコンバーターを続けることもできます。

 <fmt>       カスタムログ形式で表した値です（セクション8.2.6のカスタムログ形式を参照）。
```

例：

```text
http-check set-var(check.port) int(1234)
http-check set-var-fmt(check.port) "name=%H"

```

<a id="entry-4-2-http-check-unset-var"></a>

**`http-check unset-var(<var-name>)`**

```haproxy
http-check unset-var(<var-name>)
```

変数のスコープ内でその変数への参照を解放します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<var-name>   変数名です。使用できるスコープは"proc"、"sess"、"check"
             のみです。変数の詳細はセクション2.8を参照してください。
```

例：

```text
http-check unset-var(check.port)

```

<a id="entry-4-2-http-error-status"></a>

**`http-error status <code> [content-type <type>]`**

```haproxy
http-error status <code> [content-type <type>]
           [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

               file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
           [ hdr `<name>` `<fmt>` ]*

HAProxyが生成するエラーの代わりに使用するカスタムエラーメッセージを定義します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
status <code>        HTTPステータスコードです。指定する必要があります。
                     現在、HAProxyは200、400、401、403、404、405、407、408、410、413、
                     414、425、429、431、500、501、502、503、504を生成できます。

content-type <type>  "text/plain"など、レスポンスのコンテンツタイプです。
                     errorfileを設定した場合やペイロードが空の場合、このパラメーターは
                     無視されるため、省略することを推奨します。それ以外の場合は、
                     定義する必要があります。

default-errorfiles   現在のプロキシで、ステータス<code>に対して定義済みの
                     エラーメッセージをリセットします。バックエンドで使用した場合、
                     定義されていればフロントエンドのエラーメッセージを使用します。
                     フロントエンドで使用した場合、デフォルトのエラーメッセージを使用します。

errorfile <file>     完全なHTTPレスポンスを格納したファイルを指定します。
                     レスポンスをHTMLエラーページと混同しないよう、一般的な慣例に従って
                     ファイル名に".http"を付けることを推奨します。また、chrootの
                     実行前にファイルを読み込むため、絶対パスの使用を推奨します。

errorfiles <name>    ステータスコード<code>のエラーメッセージをインポートするために
                     使用するhttp-errorsセクションを指定します。そのようなメッセージが
                     見つからない場合、プロキシのエラーメッセージを考慮します。

file <file>          レスポンスのペイロードに使用するファイルを指定します。ファイルが
                     空でない場合、そのコンテンツタイプを"content-type"の引数として
                     設定する必要があります。空の場合、"content-type"引数はすべて
                     無視されます。<file>はそのままの文字列として扱います。

string <str>         レスポンスのペイロードに使用する、そのままの文字列を指定します。
                     コンテンツタイプは、常に"content-type"の引数として設定する必要があります。

lf-file <file>       レスポンスのペイロードに使用するファイルを指定します。ファイルが
                     空でない場合、そのコンテンツタイプを"content-type"の引数として
                     設定する必要があります。空の場合、"content-type"引数はすべて
                     無視されます。<file>はカスタムログ形式として評価します
                     （セクション8.2.6を参照）。

lf-string <str>      レスポンスのペイロードに使用するログ形式文字列を指定します。
                     コンテンツタイプは、常に"content-type"の引数として設定する必要があります。

hdr <name> <fmt>     <name>で名前を指定し、<fmt>で値を定義したHTTPヘッダーフィールドを
                     レスポンスに追加します。値はカスタムログ形式の規則に従います
                     （セクション8.2.6を参照）。errorfileを使用する場合、
                     このパラメーターは無視されます。
```

このディレクティブは、"errorfile"の代わりにカスタムエラーメッセージを定義するために使用できます。"errorfile"ディレクティブと同様に、HAProxyが検出して返すエラーに使用します。errorfileを定義した場合はHAProxyの起動時に解析され、HTTP標準に準拠していなければなりません。生成するレスポンスは、設定されたバッファーサイズ（BUFFSIZE）を超えてはなりません。超えると内部エラーを返します。また、http-after-responseルールでこれらのエラーを書き換えることを検討している場合は、予約済みのバッファー領域を利用できるようにしておくことを推奨します（"tune.maxrewrite"を参照）。

ファイルは設定と同時に読み込み、メモリーに保持します。このため、プロセスがchrootされてもエラーを返し続け、プロセスの実行中はファイルの変更を反映しません。

注意：リクエスト解析の初期段階で発生する400/408/500エラーは、下位のマルチプレクサーで処理します。このレベルではカスタム形式に対応していません。そのため、"errorfile"ディレクティブで定義した静的なエラーメッセージのみを使用できます。ただし、この制限があるのは、リクエストヘッダーの解析中、または二つのトランザクションの間だけです。

"errorfile"、"errorfiles"、"errorloc"、"errorloc302"、"errorloc303"、およびhttp-errorsに関する[セクション12.4](/ja/haproxy/other-sections/#section-12-4)も参照してください。

<a id="entry-4-2-http-request"></a>

**`http-request <action> [options...] [ { if | unless } <condition> ]`**

```haproxy
http-request <action> [options...] [ { if | unless } <condition> ]
```

レイヤー7リクエストのアクセス制御です。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

http-request文は、レイヤー7の処理に適用するルールセットを定義します。ルールはfrontend、listen、backendセクションで宣言順に評価します。各ルールの後には、任意でACLに基づく条件を付けられます。その場合は、条件が真と評価されたときにのみ、そのルールを評価します。

条件はアクションを実行する直前に評価し、アクションは一度だけ実行します。そのため、アクションが条件の一部として検査される要素を変更しても問題ありません。また、複数のアクションが同じ条件に依存することもできるため、条件の評価結果を変える最初のアクションだけで、残りのアクションを暗黙に無効にできます。たとえば、変数が空の場合に、さまざまな取得元から値を代入しようとする際に利用します。インスタンスごとの"http-request"文の数に制限はありません。

構文中の"http-request"直後のキーワードはルールのアクションで、その後に必要に応じてアクションの引数を指定します。引数の数はアクションによって異なります。対応するアクションとそれぞれの構文は、[セクション4.3](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙しています（"HTTP Req"にチェックが付いているアクションを参照）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

例：

```text
acl nagios src 192.168.129.3
acl local_net src 192.168.0.0/16
acl auth_ok http_auth(L1)

http-request allow if nagios
http-request allow if local_net auth_ok
http-request auth realm Gimme if local_net auth_ok
http-request deny
```

例：

```text
acl key req.hdr(X-Add-Acl-Key) -m found
acl add path /addacl
acl del path /delacl

acl myhost hdr(Host) -f myhost.lst

http-request add-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key add
http-request del-acl(myhost.lst) %[req.hdr(X-Add-Acl-Key)] if key del
```

例：

```text
acl value  req.hdr(X-Value) -m found
acl setmap path /setmap
acl delmap path /delmap

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-request set-map(map.lst) %[src] %[req.hdr(X-Value)] if setmap value
http-request del-map(map.lst) %[src]                     if delmap
```

"stats http-request"、ユーザーリストに関する[セクション12.2](/ja/haproxy/other-sections/#section-12-2)、およびACLの使用に関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

<a id="entry-4-2-http-response"></a>

**`http-response <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
http-response <action> <options...> [ { if | unless } <condition> ]
```

レイヤー7レスポンスのアクセス制御です。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

http-response文は、レイヤー7の処理に適用するルールセットを定義します。ルールはfrontend、listen、backendセクションで宣言順に評価します。レスポンスに適用するため、まずバックエンドのルールを適用し、その後にフロントエンドのルールを適用します。各ルールの後には、任意でACLに基づく条件を付けられます。その場合は、条件が真と評価されたときにのみ、そのルールを評価します。

条件はアクションを実行する直前に評価し、アクションは一度だけ実行します。そのため、アクションが条件の一部として検査される要素を変更しても問題ありません。また、複数のアクションが同じ条件に依存することもできるため、条件の評価結果を変える最初のアクションだけで、残りのアクションを暗黙に無効にできます。たとえば、変数が空の場合に、さまざまな取得元から値を代入しようとする際に利用します。インスタンスごとの"http-response"文の数に制限はありません。

構文中の"http-response"直後のキーワードはルールのアクションで、その後に必要に応じてアクションの引数を指定します。引数の数はアクションによって異なります。対応するアクションとそれぞれの構文は、[セクション4.3](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙しています（"HTTP Res"にチェックが付いているアクションを参照）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

例：

```text
acl key_acl res.hdr(X-Acl-Key) -m found

acl myhost hdr(Host) -f myhost.lst

http-response add-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
http-response del-acl(myhost.lst) %[res.hdr(X-Acl-Key)] if key_acl
```

例：

```text
acl value  res.hdr(X-Value) -m found

use_backend bk_appli if { hdr(Host),map_str(map.lst) -m found }

http-response set-map(map.lst) %[src] %[res.hdr(X-Value)] if value
http-response del-map(map.lst) %[src]                     if ! value
```

"http-request"、ユーザーリストに関する[セクション12.2](/ja/haproxy/other-sections/#section-12-2)、およびACLの使用に関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

<a id="entry-4-2-http-reuse"></a>

**`http-reuse { never | safe | aggressive | always }`**

```haproxy
http-reuse { never | safe | aggressive | always }
```

アイドル状態のHTTP接続をリクエスト間でどのように共有できるかを宣言します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

HTTPリクエストごとにバックエンドサーバーへの接続を新たに確立するコストを避けるため、HAProxyは使用後のアイドル接続を開いたまま保持しようとします。この接続はサーバーごとに、プールと呼ばれるリストに格納し、共通の主要属性の組み合わせでグループ化します。後続のHTTPリクエストでは、対応するプールから同じ属性を持つ互換性のある接続を検索し、新しい接続を確立する代わりに、その接続を再利用します。

サーバーで保持するアイドル接続数の上限は、serverキーワード"pool-max-conn"で指定できます。未使用の接続は、"pool-purge-delay"の間隔で定期的に削除します。

特定のリクエストでアイドル接続を再利用できるかどうかを判断する際には、次の接続属性を使用します。

- 送信元と宛先のアドレス
- プロキシプロトコル
- TOSおよびmarkソケットオプション
- 接続名。"pool-conn-name"式があれば、その評価結果で決まります。なければ"sni"式を使用し、そのデフォルトは"req.hdr(host),field(1,:)"です。つまり、受信したリクエストの"Host"ヘッダーフィールドから、コロンとポート番号を除いた値を使用します。

追加の制限により、接続の検索や再利用を行わない場合もあります。これは、キーワードの引数で指定する再利用方針で決まります。

    - "never"：アイドル接続をセッション間で共有しません。このモードを明示的に指定して、defaultsセクションから継承した別の方針を取り消したり、トラブルシューティングに使用したりできます。
                 たとえば、古い不具合のあるアプリケーションが、同じ接続上の複数のリクエストは同じクライアントから来るとみなし、そのアプリケーションを修正できない場合は、一つのバックエンドで接続の共有を無効にすることが望ましい場合があります。
                 その例としては、トンネルモードでCookieを挿入し、最初のリクエストより後のリクエストを検査しない古いHAProxyが考えられます。

    - "safe"：デフォルトであり、推奨する方針です。セッションの最初のリクエストは必ず専用の接続で送信し、後続のリクエストだけをほかの既存接続に振り分けられます。これにより、リクエストの送信中にサーバーが接続を閉じても、ブラウザーは利用者に通知せずにリトライするかどうかを判断できます。通常のkeep-aliveとまったく同じなので、副作用はないはずです。
                 ヘッドオブラインブロッキングのあるプロトコルを使う接続（h2またはfcgiを使用するバックエンド）には、特別な処理もあります。この場合、一つ以上のストリームを処理している間、使用中の接続は同じセッションのストリームを処理するために予約します。処理するストリームがなくなると接続を解放し、再利用できるようになります。

    - "aggressive"：このモードは、すべてのサーバーが必ずしも把握されておらず、最初のリクエストの大半を既存接続で送れると有益なWebサービス環境で役立つ場合があります。この場合、最初のリクエストの送信に使用できる既存接続は、すでに一度以上再利用され、サーバーが接続の再利用に正しく対応していると確認できたものに限られます。
                 クライアントが時折失敗するリクエストをリトライできると確信でき、積極的な接続の再利用による利点が、まれな接続失敗の欠点を大きく上回る場合にのみ使用すべきです。

    - "always"：このモードを推奨するのは、接続の解放直後にサーバーへの経路が既存接続を切断することはないと分かっている場合だけです。セッションの最初のリクエストを既存接続で送れます。バックエンドがキャッシュサーバー群であれば、各サーバーの動作が一貫しやすく接続の共有が有益なので、"safe"より性能を大きく向上させられる場合があります。
                 このモードでは、使えない接続が利用可能な状態で残らないように、"http-keep-alive"タイムアウトを短く保つことを推奨します。多くの場合、"aggressive"と同程度の性能向上が得られますが、リスクは増えます。"aggressive"より状況が改善する場合にのみ使用すべきです。

NTLMのような、接続に依存する不適切な認証方式を使う接続は、可能であれば専用とマークし、共有しません。ただし、多重化できるプロトコルを使用し、再利用モードのレベルをデフォルトの"safe"より高くしている場合は、接続がすでに共有されていることを妨げるものがないため、この限りではありません。

処理後のアイドル接続を開いたまま保持するか閉じるかは、"tune.pool-low-fd-ratio"（デフォルト：20%）と"tune.pool-high-fd-ratio"（デフォルト：25%）にも従います。これらは、ファイルディスクリプターの総数に対してアイドル接続が使用する割合を示します。前者のしきい値を超えるとHAProxyはレスポンス後の接続の保持を控え、後者を超えるとアイドル接続を積極的に切断します。グローバルの"maxconn"が低すぎる場合や、フロントエンドではHTTP/2またはHTTP/3のトラフィックが多く接続数が少ない一方、バックエンドではHTTP/1接続を使用する場合など、アイドル接続の割合が非常に高い構成では、開いたまま保持する接続が少なすぎて、再利用率が低くなることがあります。この場合は、これらのしきい値を調整するか、単にグローバルの"maxconn"を増やすことが望ましい場合があります。

まれに、ホスト名で送信TLS接続を区別し（フォワードプロキシなど）、リクエストの多くが異なるホストを宛先とする場合は、再利用率が非常に低くなります。この仕組みは、リソースを使い果たさずにサービスを提供するために必要な平均接続数を継続的に測定するため、あまり使わない接続の自動削除が、再利用の機会より先に働きます。そのような場合、"pool-low-conn"を想定する平均アイドル接続数に近い値にすると、より多くの接続を保持できることがあります。スレッドがほかのスレッドの接続を取得して利用可能な接続プールを縮小する代わりに、自分で接続を確立するよう促すためです。

ローカルのサーバーが、複数のホスト名やワイルドカードに対応する一つの証明書を使って複数のサイトを運用している場合は、"server"行に"no-sni-auto"を指定するだけのほうが効果的な場合があります。一つのHost名専用に接続を予約するのを避けられ、再利用率が大きく上がります。ただし、サーバーによってはHostとSNIの照合を過度に行い、後続のリクエストを拒否することがあるため、このオプションには事前の確認が必要です。デフォルトの動作（"sni-auto"）は、そのようなサーバーでも安全に動作することを優先します。

スレッドグループを明示的に有効にしている場合、アイドル接続を使えるのは同じグループのスレッド間だけであることに注意が必要です。そのため、グループ間の負荷の偏りによって、より多くのアイドル接続が必要となり、再利用率が低くなる場合があります。この場合も同じ対策を適用できます（グローバルの"maxconn"を増やすか、プールの割合を増やす）。

"option http-keep-alive"、"pool-conn-name"、"pool-max-conn"、"pool-purge-delay"、"server maxconn"、"sni"、"thread-groups"、"tune.pool-high-fd-ratio"、"tune.pool-low-fd-ratio"も参照してください。

<a id="entry-4-2-http-send-name-header"></a>

**`http-send-name-header [<header>]`**

```haproxy
http-send-name-header [<header>]
```

リクエストにサーバー名を追加します。`<header>`で指定されたヘッダー文字列を使用します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<header>  サーバー名の送信に使うヘッダー文字列です。
```

"http-send-name-header"文は、リクエストをネットワークに送信する直前に、`<header>`という名前のヘッダーフィールドを、送信先サーバーの名前に設定します。すでに存在する同名のヘッダーはすべて削除します。リトライや再振り分けの際にもヘッダーフィールドを更新し、常に接続を試みているサーバーを示します。接続の確立手順の非常に遅い段階でこのヘッダーを変更するため、すでに変更済みのヘッダーに予期しない影響が生じる場合があります。たとえば、connection、content-length、transfer-encodingなどの転送に関わるヘッダーに使用すると、無効なリクエストをサーバーへ送る可能性が高くなります。そのため、host、content-length、transfer-encoding、connectionというヘッダー名は禁止されています。

参照："server"。

<a id="entry-4-2-id"></a>

**`id <value>`**

```haproxy
id <value>
```

プロキシに永続的なIDを設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

引数：なし

プロキシに永続的なIDを設定します。このIDは一意で、正の値でなければなりません。設定しなければ、未使用のIDを自動的に割り当てます。従来の動作により、1は明示的に設定しない限り使用しません。したがって、自動割り当てされる最小値は2です。このIDは現在、統計でのみ返します。

<a id="entry-4-2-ignore-persist"></a>

**`ignore-persist { if | unless } <condition>`**

```haproxy
ignore-persist { if | unless } <condition>
```

接続先の固定を無視する条件を宣言します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

デフォルトでは、Cookieによる接続先の固定を有効にしている場合、そのCookieを含むすべてのリクエストは無条件で同じ接続先を使用します（対象のサーバーが正常に稼働していることが前提です）。

"ignore-persist"文では、ACLに基づくさまざまな条件を宣言できます。条件を満たすと、リクエストは接続先の固定を無視します。接続先の固定が不要なことが多い静的ファイルへのリクエストを負荷分散する際に役立つ場合があります。また、特定のUser-Agent（Webクローラーのボットなど）について、接続先の固定を完全に無効にするためにも使用できます。

"if"条件を満たした場合、または"unless"条件を満たさない場合に、接続先の固定を無視します。

例：

```text
acl url_static  path_beg         /static /images /img /css
acl url_static  path_end         .gif .png .jpg .css .js
ignore-persist  if url_static
```

"force-persist"、"cookie"、およびACLの使用に関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

<a id="entry-4-2-load-server-state-from-file"></a>

**`load-server-state-from-file { global | local | none }`**

```haproxy
load-server-state-from-file { global | local | none }
```

HAProxyのシームレスなリロードを可能にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

このディレクティブは、前の実行プロセスのサーバー状態を保存したファイルをHAProxyに指定します。これにより、新しいプロセスは起動時のトラフィック処理前に、リロードがなかったかのように、以前の状態をサーバーに適用できます。"load-server-state-from-file"ディレクティブの目的は、使用するファイルをHAProxyに伝えることです。現在の引数は2つだけで、状態の読み込みを無効にするか、すべてのバックエンドとサーバーを含むファイルから状態を読み込むかを指定します。状態ファイルは、統計ソケットで"show servers state"コマンドを実行し、その出力をリダイレクトして生成できます。

ファイル形式にはバージョンがあり、厳密に定められています。理解するには、"show servers state"コマンドのドキュメントを参照してください（管理ガイドの第9.3章）。

引数：

```text
global     グローバルディレクティブ"server-state-file"が指すファイルの内容を
           読み込みます。

local      "server-state-file-name"ディレクティブが設定されていれば、それが指す
           ファイルの内容を読み込みます。設定されていなければ、バックエンド名を
           ファイル名として使用します。

none       このバックエンドの状態を一切読み込みません。
```

注意：- サーバーのIPアドレスはデフォルトでリロードをまたいで保持しますが、サーバーの"init-addr"設定で優先順位を変更できます。つまり、実行中にCLIで変更したIPアドレスは保持され、状態ファイルを使用している場合は、ローカルリゾルバー（/etc/hostsなど）の変更が反映されない可能性があります。

    - サーバーの重みは、以前と新しい設定ファイルの間で変更されていない限り、前の実行プロセスから適用します。

例：最小構成

      global
       stats socket /tmp/socket
       server-state-file /tmp/server_state

      defaults
       load-server-state-from-file global

      backend bk
       server s1 127.0.0.1:22 check weight 11
       server s2 127.0.0.1:22 check weight 12

その後、次のコマンドを実行できます。

```text
socat /tmp/socket - <<< "show servers state" > /tmp/server_state
```

ファイル/tmp/server_stateの内容は、次のようになります。

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

例：最小構成

    global
     stats socket /tmp/socket
     server-state-base /etc/haproxy/states

    defaults
     load-server-state-from-file local

    backend bk
     server s1 127.0.0.1:22 check weight 11
     server s2 127.0.0.1:22 check weight 12

その後、次のコマンドを実行できます。

```text
socat /tmp/socket - <<< "show servers state bk" > /etc/haproxy/states/bk
```

ファイル/etc/haproxy/states/bkの内容は、次のようになります。

```shell
1
# <field names skipped for the doc example>
1 bk 1 s1 127.0.0.1 2 0 11 11 4 6 3 4 6 0 0
1 bk 2 s2 127.0.0.1 2 0 12 12 4 6 3 4 6 0 0
```

参照："server-state-file"、"server-state-file-name"、"show servers state"。

<a id="entry-4-2-log-global"></a>

**`log global`**

```haproxy
log global
log <target> [len <length>] [format <format>] [sample <ranges>:<sample_size>]
    [profile <prof>] <facility> [<level> [<minlevel>]]
no log
```

インスタンスごとのイベントとトラフィックのログ記録を有効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

プレフィックス：

```text
no         ロガー一覧を空にする必要がある場合に使用することを推奨します。
           たとえば、デフォルトのロガー一覧を継承したくない場合です。
           この接頭辞には引数を指定できません。
```

引数：

```text
global     は、インスタンスのログパラメーターがグローバル設定と同じ場合に
           使用することを推奨します。これが最も一般的な使い方です。"global"は、
           すべてのlog引数を"global"セクション内のlogエントリーの引数で置き換えます。
           インスタンスごとに使用できる"log global"文は一つだけで、
           この形式ではほかのパラメーターを指定できません。

<target>   はログの送信先を指定します。"global"セクションのログと同じ形式を使い、
           次のいずれかを指定できます。

           - IPv4アドレス。必要に応じて、コロン(':')とUDPポートを後ろに付けます。
             ポートを指定しない場合、デフォルトで514（標準のsyslogポート）を
             使用します。

           - IPv6アドレスの後ろにコロン(':')を付け、必要に応じてUDPポートを
             指定します。ポートを指定しない場合、デフォルトで514
             （標準のsyslogポート）を使用します。

           - UNIXドメインソケットへのファイルシステム上のパス。chroot
             （chroot内からそのパスへアクセスできること）とuid/gid
             （そのパスに適切に書き込めること）に注意してください。

           - "fd@<number>"形式のファイルディスクリプター番号。パイプ、端末、
             ソケットを指すことができます。この場合、ログをバッファリングせず、
             ログごとにwritev()を一回呼び出します。多少のコストはかかりますが、
             ほとんどのワークロードで許容できます。この方法で送ったメッセージは
             切り詰められませんが、破棄されることはあります。その場合はDroppedLogs
             カウンターが増加します。PIPE_BUF以下のサイズのメッセージなら、パイプでも
             writev()の呼び出しは不可分です。POSIXはPIPE_BUFを少なくとも512にすることを
             推奨しており、最近のほとんどのOSでは4096バイトです。これより大きい
             メッセージには、ほかのプロセスのメッセージが混在する可能性があります。
             例外的にデバッグ目的では、ファイルディスクリプターをファイルに向ける
             こともできます。ただし、ノンブロッキング呼び出しが無視されるため、
             HAProxyは大幅に遅くなります。また、プロセスを再起動せずにこのファイルを
             空にしたり、ローテーションしたりする方法もありません。設定したsyslog形式は
             維持されるので、出力はTCP syslogサーバーでの使用に適しています。
             下記の"short"と"raw"形式も参照してください。

           - "stdout" / "stderr"。それぞれ"fd@1"と"fd@2"の別名です。上記を
             参照してください。

           - "ring@<name>"形式のリングバッファー。メモリー上のリングバッファーに
             対応し、CLIの"show events"コマンドでアクセスできます。このコマンドは、
             既存のリングとそのサイズも一覧表示します。リロードや再起動で内容は
             失われますが、補助的に使えばすぐにログを確認できるため、
             トラブルシューティングに役立ちます。リングについてはセクション12.5を
             参照してください。

           - "backend@<name>"形式のログバックエンド。対応するログバックエンドに
             ログメッセージを送信し、そのバックエンドが自身の負荷分散設定に従って
             適切なサーバーにメッセージを送ります。ログバックエンドは、"mode log"を
             設定したbackendセクションです（詳細は"mode"を参照）。

           - "tcp@"、"tcp6@"、"tcp4@"、"uxst@"など、ストリームアドレスの明示的な
             接頭辞。指定のアドレスを送信先とするストリーム転送サーバーを備えた
             リングバッファーを暗黙的に割り当てます。

           アドレスパラメーターでは環境変数を参照することもできます。
           環境変数についてはセクション2.3を参照してください。

<length>   は、省略可能なログ行の最大長です。この値より長い行は、送信前に
           切り詰められます。これは、ログ行の長さに対するsyslogサーバーの動作が
           一様ではないためです。すべてのサーバーがデフォルト値の1024をサポート
           していますが、それより長い行を単に破棄するサーバーもあれば、記録する
           サーバーもあります。長い行をサポートするサーバーでは、長い行が
           切り詰められないよう、この値を設定するとよい場合があります。同様に、長い行を
           破棄するサーバーでは、送信前に切り詰めておくことを推奨します。
           指定できる値は80から65535までで、両端を含みます。通常の用途では一般に
           デフォルト値の1024で十分です。長いキャプチャーやJSON形式のログなど、
           特定の用途では、より大きい値が必要になる場合があります。リクエストURIが
           切り詰められる場合、"tune.http.logurilen"も増やす必要があるかもしれません。

<ranges>   は、サンプリングするログを指定する、カンマ区切りの範囲リストです。
           ログサーバーに送るログの負荷を分散するために使います。範囲の境界値を
           ゼロにすることはできず、1から数えます。サンプルのサイズまたは周期
           （ログの件数）は、<sample_size>パラメーターで設定する必要があります。

<sample_size>
           は、ログ記録の負荷を分散するときに考慮するサンプルのサイズで、ログの
           件数で指定します。syslogサーバーに送るログの負荷を分散するために使います。
           このサイズは、各範囲の上限のうち最大の値以上でなければなりません。
           （<ranges>パラメーターも参照してください）。

<format> は、syslogメッセージの生成時に使用するログ形式です。
         次のいずれかを指定できます。

  local     rfc3164のsyslogメッセージ形式と似ていますが、ホスト名フィールドを
            除きます。これがデフォルトです。
            注意："log-send-hostname"オプションを指定すると、デフォルトは
            rfc3164に切り替わります。

  rfc3164   RFC3164のsyslogメッセージ形式です。
            (https://tools.ietf.org/html/rfc3164)

  rfc5424   RFC5424のsyslogメッセージ形式です。
            (https://tools.ietf.org/html/rfc5424)

  priority  '<63>'のようにレベルとsyslogファシリティーだけを山括弧で囲み、
            その後ろに本文を続けたメッセージです。PID、日付、時刻、プロセス名、
            システム名は省略します。ローカルのログサーバーで使うことを
            想定しています。

  short     '<3>'のようにレベルだけを山括弧で囲み、その後ろに本文を続けた
            メッセージです。PID、日付、時刻、プロセス名、システム名は省略します。
            ローカルのログサーバーで使うことを想定しています。この形式は、
            systemdのロガーが受け付ける形式と互換性があります。

  timed     '<3>'のようにレベルだけを山括弧で囲み、その後ろにISO形式の日付と
            本文を続けたメッセージです。PID、プロセス名、システム名は省略します。
            ローカルのログサーバーで使うことを想定しています。

  iso       ISO形式の日付と、その後ろに続く本文だけを含むメッセージです。
            PID、プロセス名、システム名は省略します。ローカルのログサーバーで
            使うことを想定しています。

  raw       本文だけを含むメッセージです。レベル、PID、日付、時刻、プロセス名、
            システム名は省略します。コンテナー内や開発中の使用を想定しています。
            その場合、重大度は使用するファイルディスクリプター（stdout/stderr）
            だけで決まります。

<prof>     は、省略可能な"log-profile"セクションの名前です。ログの組み立て時に
           このセクションを参照し、一部のログオプションを上書きします。
           詳細は"8.3.5. ログプロファイル"を参照してください。

<facility> は、標準の24種類のsyslogファシリティーのいずれかでなければなりません。

               kern   user   mail   daemon auth   syslog lpr    news
               uucp   cron   auth2  ftp    ntp    audit  alert  cron2
               local0 local1 local2 local3 local4 local5 local6 local7

           "short"と"raw"形式ではファシリティーを無視しますが、位置が決まった
           フィールドとして指定する必要はあります。この場合は、ローカルでの
           使用のみを想定していることが明確になるよう、"daemon"の使用を推奨します。

<level>    は省略可能で、送信するメッセージを絞り込むために指定できます。
           デフォルトでは、すべてのメッセージを送信します。レベルを指定すると、
           そのレベル以上の重大度を持つメッセージだけを送信します。
           最小レベルも任意で指定できます。指定した場合、それより重大なレベルで
           出力されたログのレベルを、このレベルに抑えます。一部のデフォルトの
           syslog設定で、"emerg"メッセージがすべての端末に送られるのを防ぐために
           使います。次の八つのレベルがあります。

             emerg  alert  crit   err    warning notice info  debug
```

接続のどの情報をログに記録するかを決めるのはフロントエンドであり、コンテンツスイッチングの場合はバックエンドのログエントリーが無視されることに注意してください。接続は"info"レベルで記録します。

ただし、バックエンドでのログの宣言は、サーバーの状態変化をどのように、どこへ記録するかを定義します。サーバーが稼働状態になるときは"notice"、終了シグナルとサービスの最終的な終了は"warning"、サーバーのダウンは"alert"レベルで記録します。

注意：RFC3164に従い、メッセージは送出前に1024バイトに切り詰められます。

例：

```text
log global
log stdout format short daemon          # send log to systemd
log stdout format raw daemon            # send everything to stdout
log stderr format raw daemon notice     # send important events to stderr
log 127.0.0.1:514 local0 notice         # only send important events
log tcp@127.0.0.1:514 local0 notice notice  # same but limit output
                                            # level and send in tcp
log "${LOCAL_SYSLOG}:514" local0 notice   # send to local server
```

<a id="entry-4-2-log-format"></a>

**`log-format <fmt>`**

```haproxy
log-format <fmt>
```

トラフィックログに使用するカスタムログ形式文字列を指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

このディレクティブは、この行を使用するフロントエンドを通過するトラフィックのすべてのログに用いる、ログ形式の文字列を指定します。defaultsセクションで使用すると、それ以降のすべてのフロントエンドが同じログ形式を使用します。カスタムログ形式の文字列について詳しく説明した[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)を参照してください。

接続エラーの場合だけに使用する専用のlog-formatも定義できます。"error-log-format"オプションを参照してください。

"log-format"ディレクティブは、以前の"option tcplog"、"log-format"、"option httplog"、"option httpslog"ディレクティブを上書きします。

<a id="entry-4-2-log-format-sd"></a>

**`log-format-sd <fmt>`**

```haproxy
log-format-sd <fmt>
```

RFC5424のstructured-dataを生成するために使用するカスタムログ形式文字列を指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

このディレクティブは、この行を使用するフロントエンドを通過するトラフィックのすべてのログに用いる、RFC5424のstructured-dataのログ形式文字列を指定します。defaultsセクションで使用すると、それ以降のすべてのフロントエンドが同じログ形式を使用します。ログ形式の文字列について詳しく説明した[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)を参照してください。

RFC5424のstructured-data部分について詳しくは、<https://tools.ietf.org/html/rfc5424#section-6.3>を参照してください。

注意：このログ形式文字列は、ログ形式を"rfc5424"に設定したロガーでのみ使用します。

例：

```text
log-format-sd [exampleSDID@1234\ bytes=\"%B\"\ status=\"%ST\"]
```

<a id="entry-4-2-log-steps"></a>

**`log-steps <steps>`**

```haproxy
log-steps <steps>
```

トランザクション処理のどの段階でログを生成するかを指定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

TCP/HTTPトランザクションの処理中、HAProxyは処理のさまざまな段階（accept、connect、request、response、close）でログを生成できます。

デフォルトでは、HAProxyはログ形式の式で使用するすべての項目を取得できるようになった時点で、トランザクションごとに一つのログを出力します。このため、"option logasap"を使用しない限り、実際には通常、トランザクションの終了時（HTTPではレスポンスの終了後、TCPでは接続の終了後）にログを出力します。

"log-steps"ディレクティブは、ログを出力する正確な時点を細かく指定でき、同じトランザクションで複数のログを出力することもできます。特別な値'all'で利用可能なすべてのログ生成箇所を有効にすると、acceptからcloseまでトランザクションを追跡できます。また、ログを生成する箇所の名前をコンマで区切って個別に指定し、出力の時点を選択して有効にすることもできます。

一般的なログの発生元は、accept、connect、request、response、closeです。

例：

```text
frontend myfront
    option httplog
    log-steps accept,close         #only log accept and close for the txn
```

ログ生成の段階として指定した箇所（accept、closeなど）は、log-profilesの'on'ディレクティブの後でそのまま使用できます。"log-steps"とlog-profilesを組み合わせると、トランザクションの処理中にHAProxyが自動生成するログを細かく制御できます。

この設定はフロントエンドでのみ有効で、バックエンドでは無視されます。

参照："log-profile"。

<a id="entry-4-2-log-tag"></a>

**`log-tag <string>`**

```haproxy
log-tag <string>
```

すべての送信ログに使用するログタグを指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

syslogヘッダーのtagフィールドを、この文字列に設定します。デフォルトではglobalセクションのlog-tagを使用し、設定されていなければコマンドラインから起動したプログラム名（通常は"HAProxy"）を使用します。同じホスト上の複数プロセスや、同じプロセス内の顧客ごとのインスタンスを区別する際に役立つ場合があります。バックエンドでは、サーバーの稼働状態やダウン状態への変化に関するログにこのタグを使用します。たとえば、defaultsセクションで収容する顧客に対応したlog-tagを設定し、その顧客のすべてのフロントエンドとバックエンドを続けて記述した後、新しいdefaultsセクションで別の顧客の設定を始めると便利です。グローバルの"log-tag"ディレクティブも参照してください。

<a id="entry-4-2-max-keep-alive-queue"></a>

**`max-keep-alive-queue <value>`**

```haproxy
max-keep-alive-queue <value>
```

keep-alive接続を維持するサーバーキューの最大サイズを設定します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

HTTPキープアライブは、可能な限り同じサーバー接続を再利用しようとしますが、逆効果になる場合もあります。たとえば、一つのサーバーに接続が多数あり、ほかのサーバーはアイドル状態である場合です。特に静的コンテンツを配信するサーバーで当てはまります。

この設定は、キューに入っている接続数のしきい値を定めます。その値に達すると、HAProxyは同じサーバーの再利用を試みるのをやめ、別のサーバーの検索を優先します。デフォルトの-1は、制限がないことを意味します。0は、keep-aliveリクエストをキューに入れないことを意味します。低遅延で到達できる非常に近いサーバーで、keep-aliveの切断による影響が小さい場合は、小さい値を推奨します（ローカルの静的コンテンツサーバーでは、たとえば10以下を使用できます）。遅延の大きいリモートサーバーでは、その遅延や別のサーバーを選ぶコストを補うために、より大きい値が必要な場合があります。

401レスポンスに続いて同じサーバーに固定されるレスポンスには影響しません。キューで待つ必要があっても、引き続き同じサーバーに送られます。

"option http-server-close"、"option prefer-last-server"、serverの"maxconn"、およびCookieによる接続先の固定も参照してください。

<a id="entry-4-2-max-session-srv-conns"></a>

**`max-session-srv-conns <nb>`**

```haproxy
max-session-srv-conns <nb>
```

特定のクライアントセッションについて、アイドル状態で保持できる送信接続数の上限を設定します。デフォルトは5です（ビルド時に定義するMAX_SRV_LISTと厳密に同じ値です）。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

<a id="entry-4-2-maxconn"></a>

**`maxconn <conns>`**

```haproxy
maxconn <conns>
```

フロントエンドの最大同時接続数を固定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<conns>   フロントエンドが処理のために受け付ける最大同時接続数です。
          超過した接続は、システムによってソケットのリッスンキューに置かれ、
          既存の接続が閉じられると
          処理されます。
```

システムが対応していれば、大規模なサイトでは、この上限を非常に高くすると役立つ場合があります。クライアントの接続試行を応答がないままにせず、HAProxyで接続キューを管理できるためです。この値はグローバルのmaxconnを超えないようにすべきです。また、接続にはtune.bufsize（デフォルトで16kB）のバッファーが二つと、その他のデータが含まれ、確立した接続一つあたり約33kBのRAMを消費することにも注意してください。つまり、RAMを1GB搭載した中規模のシステムは、適切に調整すれば約20000-25000の同時接続を処理できます。

また、`<conns>`を大きな値に設定すると、サーバーの容量ではその負荷を受け止められない場合があります。そのため、通常はサーバーに妥当な接続数の上限を設定するのが賢明です。

この値をデフォルトのゼロにすると、グローバルの"maxconn"の値を使用します。

"server"、globalセクションの"maxconn"、"fullconn"も参照してください。

<a id="entry-4-2-mode"></a>

**`mode { tcp|http|log|spop }`**

```haproxy
mode { tcp|http|log|spop }
```

インスタンスの動作モードまたはプロトコルを設定します。使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可 引数：

```text
tcp       インスタンスは純粋なTCPモードで動作します。クライアントとサーバーの間に
          全二重接続を確立し、レイヤー7の検査は行いません。これがデフォルトの
          モードです。SSL、SSH、SMTPなどには、このモードの使用を推奨します。

http      インスタンスはHTTPモードで動作します。サーバーに接続する前に、
          クライアントのリクエストを詳細に解析します。RFCに準拠しないリクエストは
          すべて拒否します。レイヤー7のフィルタリング、処理、切り替えが可能です。
          HAProxyの価値の大部分は、このモードによってもたらされます。

haterm    フロントエンドはhaterm HTTPベンチマークモードで動作します。
          バックエンドではサポートしていません。詳細はdoc/haterm.txtを参照してください。

log       backendセクションで使用すると、そのバックエンドはログバックエンドになります。
          "backend@<name>"構文を使用すれば、どの"log"ディレクティブでも
          ログの送信先として指定できます。ログメッセージは、"balance"キーワードで
          設定できる負荷分散設定に従って、バックエンドのサーバーに分配されます。
          サーバーアドレスに"udp@"プレフィックスを付けると、ログバックエンドで
          UDPサーバーを使用できます。一般的なバックエンドおよびサーバーの機能は
          サポートしますが、TCPやHTTPに固有の機能はサポートしません。

spop      backendセクションで使用すると、そのバックエンドはspopバックエンドになります。
          バックエンドにSPOAサーバーが含まれる場合、このモードが必須です。
          ただし、モードがtcpでも、このようなサーバーを検出すると、
          自動的にspopモードに変換されます。

```

コンテンツスイッチングを行う場合、フロントエンドとバックエンドは同じモード（通常はHTTP）でなければなりません。そうでなければ、設定を拒否します。

例：

```text
defaults http_instances
    mode http

```

<a id="entry-4-2-monitor-fail"></a>

**`monitor fail { if | unless } <condition>`**

```haproxy
monitor fail { if | unless } <condition>
```

監視用HTTPリクエストに失敗を報告する条件を追加します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
if <cond>     条件を満たす場合、監視リクエストは失敗し、それ以外の場合は成功します。
              条件には、すべての条件を満たした場合に必ず失敗させる複合テストを
              記述することを推奨します。たとえば、バックエンドとそのバックアップの
              両方でサーバー数が少ないという条件です。

unless <cond> 条件を満たす場合にのみ監視リクエストは成功し、それ以外の場合は失敗します。
              この条件には、バックエンドのリスト内に、稼働中のサーバーが最低限必要な数以上
              存在するかを調べるテストなどを使用できます。
```

この文は、監視リクエストへのレスポンスで障害を報告させる条件を追加します。デフォルトでは、外部コンポーネントが監視専用のURIに問い合わせると、200レスポンスを返します。上記の条件のいずれかを満たすと、HAProxyは200の代わりに503を返します。HAProxyが報告する可用性に基づいて複数サイト間の経路広告を決定する外部コンポーネントに、サイトの障害を報告する際に非常に役立ちます。その場合、"nbsrv"条件を含むACLを使用します。"monitor fail"はHTTPモードでのみ動作します。必要に応じて、両方のステータスメッセージを"errorfile"または"errorloc"で調整できます。

例：

```text
frontend www
   mode http
   acl site_dead nbsrv(dynamic) lt 2
   acl site_dead nbsrv(static)  lt 2
   monitor-uri   /site_alive
   monitor fail  if site_dead
```

参照："monitor-uri"、"errorfile"、"errorloc"。

<a id="entry-4-2-monitor-uri"></a>

**`monitor-uri <uri>`**

```haproxy
monitor-uri <uri>
```

外部コンポーネントの監視リクエストが使用するURIを捕捉します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<uri>     リクエストの転送をせずに、HAProxyのヘルス状態を返すために
          捕捉する正確なURIです。
```

フロントエンドが`<uri>`を参照するHTTPリクエストを受信すると、HAProxyは転送もログへの記録も行わず、"monitor fail"で定義した障害条件に応じて、"HTTP/1.0 200 OK"または"HTTP/1.0 503 Service unavailable"を返します。通常、前段のHTTP監視プローブは、これだけで、リクエストをバックエンドサーバーへ転送せずにサービスが正常に稼働していると判断できます。HTTPメソッド、バージョン、すべてのヘッダーは無視しますが、リクエストは少なくともHTTPとして有効でなければなりません。このキーワードは、HTTPモードのフロントエンドでのみ使用できます。

監視リクエストは、リクエストの解析直後、"http-request"よりも前という、非常に早い段階で処理します。それより前に適用するルールセットはtcp-requestだけです。また、監視リクエストはログに記録できず、これは意図した動作です。監視用のURIは一つだけ設定でき、複数の"monitor-uri"文がある場合は最後の文で使用するURIを定義します。このURIは、HAProxyの正常性を上位のコンポーネントに報告するためだけに使用します。ただし、"monitor fail"とACLで条件を任意の数だけ追加し、考えられるどのようなチェックにも結果を合わせられます（通常はバックエンドで利用可能なサーバー数です）。

注意：`<uri>`がスラッシュ（'/'）で始まる場合、リクエストのURIではなくパスと照合します。HTTP/2リクエストをmonitor-uriと一致させるための回避策です。HTTP/2では、クライアントは絶対URIだけを送信することが推奨されています。

例：

```shell
# Use /haproxy_test to report HAProxy's status
frontend www
    mode http
    monitor-uri /haproxy_test
```

参照："monitor fail"。

<a id="entry-4-2-option-abortonclose"></a>

**`option abortonclose`**

```haproxy
option abortonclose
no option abortonclose
```

クライアントが接続を閉じたときに、未開始の処理を早期に中止する機能を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

TCP接続は、方向ごとに独立して閉じられます。一方の方向だけを閉じた接続は、一般に「ハーフクローズ」と呼びます。HTTPが主に「クローズモード」で動作し、接続ごとに一つのリクエストと一つのレスポンスをやり取りしてから閉じていた頃は、スクリプトで動作するクライアントが、リクエストを送信し、送信側を閉じてレスポンスを待ち、接続終了の通知を受けて処理を終えることがよくありました。しかし、keep-aliveやより高度なプロトコルの登場によって、このような動作はほぼ見られなくなりました。レスポンスを受信する前にクライアントが閉じるのは、基本的に、利用者が転送を中断したい場合か、タイムアウトが発生して接続が閉じられる場合だけです。

この二つの状況（ハーフクローズと中断）は、サーバー側（ここではHAProxyのリスナー）から区別できません。クライアントが中断しても接続を維持し、リクエストの処理を続けると、多くのリソースを消費するため問題になります。特に、利用者が「再読み込み」ボタンを押した結果の切断であれば、以前のリクエストが中断されないまま新しいリクエストがキューに入ることになります。逆に、このようなハーフクローズの状況で常に処理を中断すると、多くのTCPアプリケーションや、内部ネットワークで古いエージェントと通信する一部のHTTPアプリケーションも動作しなくなります。

"abortonclose"オプションで、望む動作を選択できます。- フロントエンドに指定すると、ハーフクローズされた接続で待機中のTLSハンドシェイクを処理しません。これは、HAProxyのアクティブノードからバックアップノードへのVRRPフェイルオーバーのような高負荷時に、利用者がHTTPSリクエスト中に「再読み込み」を押すことで発生する場合があります。すべてのクライアントが新しいノードに同時に再接続し、全員がコストの高い完全なTLSハンドシェイクを行う必要があります。数秒以上かかると、一部の利用者は断念する可能性が高く、そのハンドシェイクのためにCPUを浪費しても意味がありません。TLSハンドシェイクのCPUコストを考慮すると、インターネットに公開するフロントエンドでは、このオプションを有効にしておくことを推奨します。受信TLS接続では、これがデフォルトです。

    - バックエンドに指定すると、ハーフクローズされた接続では、まだサーバーへ送っていないリクエスト（キューで待機中、または接続を試みているもの）の中断を試みます。
      サーバーがすでにリクエストを処理している場合は、サーバーへの接続もハーフクローズに切り替え、同じ状況をサーバーに通知します。その後どう処理するかはサーバーが決定します。HTTPモードのバックエンドでは、これがデフォルトです。

インターネットに公開するTLSエンドポイントとHTTPサービスでは、このオプションを有効にし、純粋なTCPサービスや外部に公開しない旧来の環境では無効にすることを推奨します。HTTPバックエンドではデフォルトで有効です。バックエンドセクション自体、または継承元の"defaults"セクションで、前に"no"キーワードを付けると明示的に無効にできます。また、TLSリスナーでもデフォルトで有効です。フロントエンド、または継承元の"defaults"セクションで"no option abortonclose"を指定すると、同様に明示的に無効にできます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"timeout queue"と、serverの"maxconn"および"maxqueue"パラメーターも参照してください。

<a id="entry-4-2-option-accept-invalid-http-request"></a>

**`option accept-invalid-http-request     (deprecated)`**

```haproxy
option accept-invalid-http-request     (deprecated)
no option accept-invalid-http-request  (deprecated)
```

HTTPリクエスト解析の制約緩和を有効または無効にします。

"accept-invalid-http-request"キーワードは非推奨です。代わりに"option accept-unsafe-violations-in-http-request"を使用してください。

<a id="entry-4-2-option-accept-invalid-http-response"></a>

**`option accept-invalid-http-response     (deprecated)`**

```haproxy
option accept-invalid-http-response     (deprecated)
no option accept-invalid-http-response  (deprecated)
```

HTTPレスポンス解析の制約緩和を有効または無効にします。

"accept-invalid-http-response"キーワードは非推奨です。代わりに"option accept-unsafe-violations-in-http-response"を使用してください。

<a id="entry-4-2-option-accept-unsafe-violations-in-http-request"></a>

**`option accept-unsafe-violations-in-http-request`**

```haproxy
option accept-unsafe-violations-in-http-request
no option accept-unsafe-violations-in-http-request
```

HTTPリクエスト解析の制約緩和を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

デフォルトでは、HAProxyはメッセージの解析について各HTTP RFCに準拠します。つまり、解析は厳格で、不正な形式のメッセージにはクライアントへエラーを返します。このようなメッセージは、主にサーバーの弱点を悪用し、セキュリティフィルターを回避する攻撃に使われるため、これは望ましい動作です。不具合のあるブラウザーが、設定や実装などの理由でこれらのRFCに従わず、問題がすぐに修正されない場合もあります。その場合、このオプションを指定してHAProxyのパーサーを緩和し、一部の無効なリクエストを受け付けられます。歴史的な理由から、ルールの大半はH1の解析に関するものです。新しいHTTPバージョンはより整っている傾向があり、アプリケーションもそのプロトコルにより厳密に従います。

このオプションを設定すると、次の規則が適用されます。

    * H1でのみ、ヘッダー名にNULL文字を含む無効な文字があっても拒否しません。ただし、そのヘッダーは削除します。

    * H1でのみ、ヘッダー値のNULL文字が許可されます。

    * H1でのみ、URI内の127を超える文字を受け付けます。URIに使用できる文字はRFC3986で厳密に定められており、0-31、32（空白）、34（'"'）、60（'<'）、62（'>'）、92（'&#92;'）、94（'^'）、96（'`'）、123（'{'）、124（'|'）、125（'}'）、127（削除）、およびそれより大きい文字は通常、許可されません。
      H1では、(0..32)の範囲の文字と127は常に拒否します。127を含まず、それを超えるすべての文字も、このオプションを有効にした場合を除いて拒否します。その他の文字(33..126)は一切検査しません。

    * H1とH2では、フラグメント参照（パスの後の'#'）を含むURLを受け付けます。

    * H1でのみ、CONNECTリクエストのauthorityを検査しません。

    * H1でのみ、authorityとHostヘッダーの値の照合を行いません。

    * H1でのみ、HTTPバージョンの検査を緩和します。バージョンを指定しないHTTP/0.9のGETリクエスト、異なるプロトコル名（RTSPなど）、およびメジャーバージョンとマイナーバージョンの両方に複数桁を使う表記を許可します。

    * H1でのみ、有効な"Sec-Websocket-Key"ヘッダーフィールドを提示しないWebSocket（RFC6455）リクエストを受け付けます。

このオプションは、アプリケーションの不具合を隠し、セキュリティ上の抜け穴を生むため、決してデフォルトで有効にすべきではありません。問題を確認した後にのみ導入すべきです。

このオプションを有効にすると、不正であっても受け入れたH1リクエストを取得し、後からUNIX統計ソケットの"show errors"リクエストで解析できるようにします。問題が解決したかどうかの確認にも役立ちます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"option accept-unsafe-violations-in-http-response"と、統計ソケットの"show errors"も参照してください。

<a id="entry-4-2-option-accept-unsafe-violations-in-http-response"></a>

**`option accept-unsafe-violations-in-http-response`**

```haproxy
option accept-unsafe-violations-in-http-response
no option accept-unsafe-violations-in-http-response
```

HTTPレスポンス解析の制約緩和を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

"option accept-unsafe-violations-in-http-request"と同様に、このオプションを使うとHTTPレスポンスの解析規則を緩和できます。信頼できる旧式サーバーからの一部の不正なレスポンスを受け入れる場合に限って有効にするべきです。歴史的な理由から、規則のほとんどはH1の解析に関するものです。新しいHTTPバージョンはより整備されている傾向があり、アプリケーションもそのプロトコルにより厳密に従います。

このオプションを設定すると、次の規則が適用されます。

    * H1でのみ、3桁より長くても値が16ビットに収まるステータスコードは拒否しません。

    * H1でのみ、ヘッダー名にNULL文字を含む無効な文字があっても拒否しません。ただし、そのヘッダーは削除します。

    * H1でのみ、ヘッダー値のNULL文字が許可されます。

    * H1でのみ、Transfer-Encodingヘッダーの空の値や、複数の"chunked"値を受け付けます。

    * H1でのみ、authorityとHostヘッダーの値の照合を行いません。

    * H1でのみ、HTTPバージョンの検査を緩和します。
      異なるプロトコル名（RTSPなど）と、メジャーおよびマイナーバージョンの
      両方に複数桁の数値を使用できるようになります。

    * H1でのみ、有効な"Sec-Websocket-Accept"ヘッダーフィールドを提示しないWebSocket（RFC6455）レスポンスを受け付けます。

このオプションは、アプリケーションの不具合を隠し、セキュリティ上の抜け穴を生むため、決してデフォルトで有効にすべきではありません。問題を確認した後にのみ導入すべきです。

このオプションを有効にすると、レスポンスの誤ったヘッダー名も受け付けますが、レスポンス全体をキャプチャし、後からUNIX統計ソケットの"show errors"リクエストで解析できるようにします。これは、問題が解決したことの確認にも役立ちます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"option accept-unsafe-violations-in-http-request"と、統計ソケットの"show errors"も参照してください。

<a id="entry-4-2-option-allbackups"></a>

**`option allbackups`**

```haproxy
option allbackups
no option allbackups
```

すべてのバックアップサーバーを同時に使用するか、最初のサーバーのみを使用します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

デフォルトでは、通常のサーバーがすべてダウンすると、最初の稼働中のバックアップサーバーがすべてのトラフィックを受け取ります。一つでは足りないため、複数のバックアップを同時に使用したほうがよい場合もあります。"option allbackups"を有効にすると、通常のサーバーがすべて利用できないときに、すべてのバックアップサーバー間で負荷分散します。同じ負荷分散アルゴリズムを使用し、サーバーの重みも考慮します。そのため、バックアップサーバー間の優先順位はなくなります。

このオプションは主に、アプリケーションが完全に停止しているときに「お詫び」ページを返すための、静的なサーバー群で使用します。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

<a id="entry-4-2-option-checkcache"></a>

**`option checkcache`**

```haproxy
option checkcache
no option checkcache
```

すべてのサーバーレスポンスを解析し、キャッシュ可能なCookieを含むレスポンスを遮断します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

一部の高水準フレームワークは、いたるところでアプリケーションのCookieを設定し、レスポンスのキャッシュ方法を開発者が十分に制御できるとは限りません。キャッシュ可能なオブジェクトとともにセッションCookieが返されると、同じキャッシュを経由するユーザー間で、セッションが混同されたり盗まれたりする危険が高まります。状況によっては、機密性の高いセッション情報を外部に流してしまうより、レスポンスをブロックするほうがよい場合があります。

"checkcache"オプションは、すべてのサーバーレスポンスを詳細に検査し、キャッシュの可否についてHTTP仕様に厳密に準拠しているかを確認します。レスポンスの"Cache-control"、"Pragma"、"Set-cookie"ヘッダーを注意深く検査し、クライアント側のプロキシがCookieをキャッシュするリスクがないか確認します。このオプションを有効にすると、クライアントに送れるのは次のレスポンスだけです：- "Set-Cookie"ヘッダーがないもの。- ステータスコードが200、203、204、206、300、301、404、405、410、414、501以外で、サーバーが"Cache-control: public"ヘッダーフィールドを設定していないもの。- GET、HEAD、OPTIONS、TRACE以外のメソッドを使用したリクエストへのレスポンスで、サーバーが'Cache-Control: public'ヘッダーフィールドを設定していないもの。- 'Pragma: no-cache'ヘッダーを持つもの。- 'Cache-control: private'ヘッダーを持つもの。- 'Cache-control: no-store'ヘッダーを持つもの。- 'Cache-control: max-age=0'ヘッダーを持つもの。- 'Cache-control: s-maxage=0'ヘッダーを持つもの。- 'Cache-control: no-cache'ヘッダーを持つもの。- 'Cache-control: no-cache="set-cookie"'ヘッダーを持つもの。- 'Cache-control:
no-cache="set-cookie,'ヘッダーを持つもの（set-cookieの後にほかのフィールドを指定できます）。 - 鮮度情報（"max-age"または"s-maxage"を持つ"Cache-control"、または"Expires"ヘッダー）も検証子（"ETag"または"Last-Modified"ヘッダー）も持たないもの。仕様に準拠したキャッシュは、このようなレスポンスを保存しないためです。

レスポンスがこれらの要件を満たさない場合、"http-response deny"ルールによる拒否と同様にブロックされ、"HTTP 502 bad gateway"になります。セッション状態には"PH--"が表示され、プロキシがヘッダー処理中にレスポンスをブロックしたことを示します。さらに、修正が必要であることを管理者に知らせるため、ログにアラートが出力されます。

アプリケーションへの影響が大きいため、本番環境に導入する前に、このオプションを有効にしてアプリケーションを十分にテストするべきです。また、危険につながる可能性のあるアプリケーションの動作を報告するので、本番環境で使わない場合でも、テスト中は常に有効にしておくのがよい方法です。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

<a id="entry-4-2-option-clitcpka"></a>

**`option clitcpka`**

```haproxy
option clitcpka
no option clitcpka
```

クライアント側のTCP keepaliveパケットの送信を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

クライアントとサーバーの間にファイアウォールなどのセッションを認識するコンポーネントがあり、プロトコルが長いアイドル期間を含む非常に長いセッションを使う場合（リモートデスクトップなど）、途中のコンポーネントが、長時間アイドル状態にあったセッションを期限切れにするおそれがあります。

ソケットレベルのTCP keep-aliveを有効にすると、システムは接続の相手側へ定期的にパケットを送信し、接続を維持します。keep-aliveプローブの間隔はシステムだけが制御し、オペレーティングシステムとその調整パラメーターの両方に依存します。

キープアライブパケットは、アプリケーションレベルでは送信も受信もされないことを理解する必要があります。それを認識するのはネットワークスタックだけです。そのため、プロキシの片側ですでにキープアライブを使って接続を維持していても、そのキープアライブパケットがプロキシの反対側に転送されることはありません。

これはHTTP keep-aliveとは関係がありません。

"clitcpka"オプションを使うと、接続のクライアント側でTCPキープアライブプローブの送信を有効にします。HAProxyとクライアントの間でセッションの期限切れが見られる場合に役立つはずです。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option srvtcpka"、"option tcpka"。

<a id="entry-4-2-option-contstats"></a>

**`option contstats`**

```haproxy
option contstats
```

トラフィック統計の継続的な更新を有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

デフォルトでは、統計の計算に使うカウンターは、ストリームが終了したときだけ増加します。小さなオブジェクトを配信する場合は十分に機能しますが、大きな画像やアーカイブなどの大きなオブジェクト、または音声や映像のストリーミングでは、HAProxyのカウンターから作ったグラフがハリネズミのようにとがった形になります。このオプションを有効にすると、ストリームの途中でもカウンターを頻繁に、通常は5秒ごとに増加させるため、多くの場合、滑らかなグラフを作れます。再集計は頻繁に通る処理経路に直接影響し、セッション数が非常に多いと大量の起床処理が発生して性能がわずかに低下する可能性があるため、デフォルトでは有効にしていません。

<a id="entry-4-2-option-disable-h2-upgrade"></a>

**`option disable-h2-upgrade`**

```haproxy
option disable-h2-upgrade
no option disable-h2-upgrade
```

HTTP/1.xクライアント接続からの暗黙的なHTTP/2へのアップグレードを有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

デフォルトでは、あるHTTP接続で最初に受信したリクエストがHTTP/2の接続プリフェイス（文字列"PRI \*
HTTP/2.0&#92;r&#92;n&#92;r&#92;nSM&#92;r&#92;n&#92;r&#92;n"）に一致すると、HAProxyはHTTP/1.xクライアント接続をHTTP/2接続へ暗黙にアップグレードできます。これにより、SSLを使わない接続でもHTTP/1.xとHTTP/2のクライアントをサポートできます。暗黙のアップグレードを無効にするには、このオプションを使用しなければなりません。このアップグレードはHTTPプロキシだけがサポートするため、このオプションも同様です。また、bind行に"proto h2"を指定すると、平文接続でHTTP/2を強制することもできます。このオプションは、すべてのbind行に適用します。特定のbind行で暗黙のHTTP/2アップグレードを無効にするには、"proto h1"を使用できます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

<a id="entry-4-2-option-dontlog-normal"></a>

**`option dontlog-normal`**

```haproxy
option dontlog-normal
no option dontlog-normal
```

正常に成功した接続のログ記録を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

毎秒数千の接続を扱う大規模なサイトでは、ログ記録が大きな負担になることがあります。ログを無効にせざるを得ず、本番環境の問題をデバッグできないサイトさえあります。このオプションを設定すると、エラー、タイムアウト、再試行、再振り分けのいずれも起きていない正常な接続を、ログに記録しません。これにより、異常を記録するためのディスク領域を確保できます。HTTPモードではレスポンスのステータスコードを確認し、5xxの応答コードは引き続き記録します。

複雑な問題を解決する手掛かりは、この設定では記録されない通常のログにあることが多いため、このオプションの使用は強く非推奨とします。ログを分ける必要がある場合は、代わりに"log-separate-errors"オプションを参照してください。

"log"、"dontlognull"、"log-separate-errors"、およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-dontlognull"></a>

**`option dontlognull`**

```haproxy
option dontlognull
no option dontlognull
```

データのない接続のログ記録を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

環境によっては、各種システムが稼働しているかを確認するため、定期的に接続するコンポーネントがあります。別のロードバランサーや監視システムが、その例です。デフォルトでは、単純なポートのプローブやスキャンでもログが生成されます。このような接続でログが埋まりすぎる場合は、"dontlognull"オプションを有効にすると、データを一切転送していない接続を記録しないようにできます。通常、この種のプローブが該当します。ただし、エラーは引き続きクライアントへ返し、統計にも計上します。これも望ましくない場合は、代わりにoption http-ignore-probesを使用できます。

一般に、管理できない環境（インターネットなど）では、このオプションを使用しないことを推奨します。使用すると、スキャンやその他の悪意のある活動がログに記録されなくなるためです。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"log"、"http-ignore-probes"、"monitor-uri"、およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-external-check"></a>

**`option external-check`**

```haproxy
option external-check
```

サーバーのヘルスチェックに外部プロセスを使用します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

外部コマンドを使って、サーバーの正常性を確認できます。"external-check command"で指定した実行ファイルを実行することで実現します。

グローバル設定の"external-check"を設定する必要があります。

参照："external-check"、"external-check command"、"external-check path"。

<a id="entry-4-2-option-forwarded"></a>

**`option forwarded [ proto ]`**

```haproxy
option forwarded [ proto ]
                 [ host | host-expr <host_expr> ]
                 [ by | by-expr <by_expr> ] [ by_port | by_port-expr <by_port_expr>]
                 [ for | for-expr <for_expr> ] [ for_port | for_port-expr <for_port_expr>]
no option forwarded
```

サーバーに送信するリクエストへのrfc 7239 forwardedヘッダーの挿入を有効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<host_expr>     任意指定の引数で、独自のサンプル式を指定します。
                その結果を'host'パラメーターの値に使用します。

<by_expr>       任意指定の引数で、独自のサンプル式を指定します。
                その結果を'by'パラメーターのnodename値に使用します。

<for_expr>      任意指定の引数で、独自のサンプル式を指定します。
                その結果を'for'パラメーターのnodename値に使用します。

<by_port_expr>  任意指定の引数で、独自のサンプル式を指定します。
                その結果を'by'パラメーターのnodeport値に使用します。

<for_port_expr> 任意指定の引数で、独自のサンプル式を指定します。
                その結果を'for'パラメーターのnodeport値に使用します。

```

HAProxyはリバースプロキシとして動作するため、サーバーではリクエストの一部の情報（送信元のクライアントIPアドレス、使用したプロトコルなど）が失われます。

この制限への一般的な対処方法は、よく知られたx-forward-forやx-forward-\* 系のヘッダーを使い、このコンテキストの一部を背後のサーバーやアプリケーションに伝えることです。この方法は機能しており、広く導入されていますが、IETFが公式にサポートするものではなく、相互運用性やセキュリティの問題の原因になることがあります。

これを解決するため、IETFが新しいHTTP拡張としてforwardedヘッダー（RFC7239）を定めました。詳細は<https://www.rfc-editor.org/rfc/rfc7239.html>を参照してください。

この一つのヘッダーで多数の詳細情報を伝えられ、特に重要な点として、プロキシを連鎖させたときの問題を解決できます（RFCは、連鎖した複数のプロキシが、既存のヘッダーにそれぞれの値を追加することを認めています）。

このオプションはdefaults、listen、backendセクションに指定できますが、frontendセクションでは無視されます。

option forwardedを引数なしで設定すると、デフォルトの暗黙の動作を使用します。デフォルトではprotoパラメーターを有効にし、元のクライアントIPを挿入します。

同等の明示的な手動設定は次のようになります。

```text
option forwarded proto for
```

'by'キーワードは、forwardedヘッダーの'by'パラメーター（"nodename"）を有効にします。リクエストを扱うプロキシの情報を埋め込めます。'by'の値には、プロキシのIP（宛先アドレス）を設定します。UNIXリスナーなど、利用できない場合は、'by'を"unknown"に設定します。

'by-expr'キーワードは、forwardedヘッダーの'by'パラメーター（"nodename"）を有効にします。リクエストを扱うプロキシの情報を埋め込めます。'by'の値には、サンプル式`<by_expr>`の結果が有効であればその結果を設定し、そうでなければ"unknown"を設定します。

'for'キーワードは、forwardedヘッダーの'for'パラメーター（"nodename"）を有効にします。リクエストを送るクライアントの情報を埋め込めます。'for'の値には、クライアントのIP（送信元アドレス）を設定します。UNIXリスナーなど、利用できない場合は、'for'を"unknown"に設定します。

'for-expr'キーワードは、forwardedヘッダーの'for'パラメーター（"nodename"）を有効にします。リクエストを送るクライアントの情報を埋め込めます。'for'の値には、サンプル式`<for_expr>`の結果が有効であればその結果を設定し、そうでなければ"unknown"を設定します。

'by_port'キーワードは、'by'パラメーターに"nodeport"情報を渡すために使用します。'by_port'には'by'または'by-expr'の設定が必要で、なければ無視されます。"nodeport"には、利用可能であればプロキシのポート（宛先ポート）を設定し、利用できなければ無視します。

'by_port-expr'キーワードは、'by'パラメーターに"nodeport"情報を渡します。'by_port-expr'には'by'または'by-expr'の設定が必要で、なければ無視します。"nodeport"には、サンプル式`<by_port_expr>`の結果が有効であればその結果を設定し、そうでなければ無視します。

'for_port'キーワードは、'for'パラメーターに"nodeport"情報を渡すために使用します。'for_port'には'for'または'for-expr'の設定が必要で、なければ無視されます。"nodeport"には、利用可能であればクライアントのポート（送信元ポート）を設定し、利用できなければ無視します。

'for_port-expr'キーワードは、'for'パラメーターに"nodeport"情報を渡します。'for_port-expr'には'for'または'for-expr'の設定が必要で、なければ無視します。"nodeport"には、サンプル式`<for_port_expr>`の結果が有効であればその結果を設定し、そうでなければ無視します。

例：

```shell
# Those servers want the ip address and protocol of the client request
# Resulting header would look like this:
#   forwarded: proto=http;for=127.0.0.1
backend www_default
    mode http
    option forwarded
    #equivalent to: option forwarded proto for

# Those servers want the requested host and hashed client ip address
# as well as client source port (you should use seed for xxh32 if ensuring
# ip privacy is a concern)
# Resulting header would look like this:
#   forwarded: host="haproxy.org";for="_000000007F2F367E:60138"
backend www_host
    mode http
    option forwarded host for-expr src,xxh32,hex for_port

# Those servers want custom data in host, for and by parameters
# Resulting header would look like this:
#   forwarded: host="host.com";by=_haproxy;for="[::1]:10"
backend www_custom
    mode http
    option forwarded host-expr str(host.com) by-expr str(_haproxy) for for_port-expr int(10)

# Those servers want random 'for' obfuscated identifiers for request
# tracing purposes while protecting sensitive IP information
# Resulting header would look like this:
#   forwarded: for=_000000002B1F4D63
backend www_for_hide
    mode http
    option forwarded for-expr rand,hex
```

参照："option forwardfor"、"option originalto"。

<a id="entry-4-2-option-forwardfor"></a>

**`option forwardfor [ except <network> ] [ header <name> ] [ if-none ]`**

```haproxy
option forwardfor [ except <network> ] [ header <name> ] [ if-none ]
```

サーバーに送信するリクエストへのX-Forwarded-Forヘッダーの挿入を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<network> 任意の引数です。<network>に一致する送信元について、
          このオプションを無効にします。
<name>    別の"X-Forwarded-For"ヘッダー名を指定するための
          任意の引数です。
```

HAProxyはリバースプロキシとして動作するため、サーバーから見るクライアントのアドレスはHAProxyのIPアドレスになります。サーバーのログにクライアントのIPアドレスを記録したい場合、これが問題になることがあります。解決するには、HAProxyからサーバーに送るすべてのリクエストに、広く知られたHTTPヘッダー"X-Forwarded-For"を追加できます。このヘッダーの値は、クライアントのIPアドレスを表します。常に既存のヘッダー一覧の末尾に追加するため、サーバーは、このヘッダーの最後の出現箇所だけを常に使用するよう設定しなければなりません。この標準的なヘッダーの使用を有効にする方法は、サーバーのマニュアルを参照してください。クライアントがすでにこのヘッダーを付けている可能性もあるため、最後の出現箇所だけを使用しなければなりません。

"header"キーワードを使うと、既定の"X-Forwarded-For"を置き換える別のヘッダー名を指定できます。別のアプリケーション（stunnelなど）がすでに付けた"X-Forwarded-For"ヘッダーがあり、それを保持する必要がある場合に便利です。また、バックエンドサーバーが"X-Forwarded-For"ヘッダーを使わず、別のヘッダーを必要とする場合にも使えます（たとえば、Zeus Web Serversは"X-Cluster-Client-IP"を必要とします）。

クライアントから直接アクセスする場合と、リバースプロキシ経由でアクセスする場合とで、同じHAProxyインスタンスを共有することがあります。たとえば、SSLリバースプロキシでHTTPSトラフィックを復号する場合です。"except"キーワードの後にネットワークアドレスを指定すると、既知の送信元アドレスまたはネットワークに対して、ヘッダーの追加を無効にできます。この場合、そのネットワークに一致する送信元IPからのリクエストには、このヘッダーを追加しません。プライベートネットワークや127.0.0.1での使用が一般的です。IPv4とIPv6の両方をサポートします。

別の方法として、"if-none"キーワードを指定すると、ヘッダーが存在しない場合にだけ追加します。HAProxyに届くヘッダーをエンドユーザーが制御できるとセキュリティ上の問題になる可能性があるため、完全に信頼できる環境でのみ使用するべきです。

このオプションはフロントエンドとバックエンドのどちらでも指定できます。少なくとも一方で使用していれば、ヘッダーを追加します。両方でheaderサブ引数を定義している場合は、バックエンドの設定がフロントエンドより優先されます。"if-none"引数については、フロントエンドかバックエンドの少なくとも一方が指定していなければ、その側がヘッダーの追加を必須としているため、そちらが優先されます。

例：

```shell
# Public HTTP address also used by stunnel on the same machine
frontend www
    mode http
    option forwardfor except 127.0.0.1  # stunnel already adds the header

# Those servers want the IP Address in X-Client
backend www
    mode http
    option forwardfor header X-Client
```

参照："option httpclose"、"option http-server-close"、"option http-keep-alive"。

<a id="entry-4-2-option-h1-case-adjust-bogus-client"></a>

**`option h1-case-adjust-bogus-client`**

```haproxy
option h1-case-adjust-bogus-client
no option h1-case-adjust-bogus-client
```

仕様に準拠しないクライアントに送信するHTTP/1ヘッダーの大文字・小文字の調整を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

RFC7230が規定するとおり、ヘッダー名は大文字と小文字を区別しないため、標準となる大文字・小文字の表記はありません。アプリケーションは、大文字と小文字を区別せずに扱わなければなりません。しかし、標準に違反し、ブラウザーがよく使う大文字・小文字の表記に誤って依存するアプリケーションもあります。HTTP/2では、すべてのヘッダー名を小文字で交換しなければならず、HAProxyも同じ規則に従うため、この問題は重大になります。HTTPのバージョンに関係なく、クライアントとサーバーには、すべてのヘッダー名を小文字で送ります。

HAProxyがHTTP/1レスポンスを受信すると、ヘッダー名を小文字に変換し、その表記で処理してクライアントに送ります。クライアントがHTTPの標準に違反し、HAProxyからのレスポンスを処理できないと分かっている場合は、このオプションを有効にし、globalディレクティブ"h1-case-adjust"または"h1-case-adjust-file"で表記を変えるヘッダーの一覧を指定すると、レスポンスを整形してクライアントへ送る際に、小文字のヘッダー名を別の表記に変換できます。このような回避策が必要なクライアントはコンテンツスマグリング攻撃に弱い可能性があり、必ず修正しなければならないため、クライアントを修正するまでの一時的な回避策としてのみ使用しなければなりません。

このオプションは、標準に準拠したクライアントには影響しません。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option h1-case-adjust-bogus-server"、"h1-case-adjust"、"h1-case-adjust-file"。

<a id="entry-4-2-option-h1-case-adjust-bogus-server"></a>

**`option h1-case-adjust-bogus-server`**

```haproxy
option h1-case-adjust-bogus-server
no option h1-case-adjust-bogus-server
```

仕様に準拠しないサーバーに送信するHTTP/1ヘッダーの大文字・小文字の調整を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

RFC7230が規定するとおり、ヘッダー名は大文字と小文字を区別しないため、標準となる大文字・小文字の表記はありません。アプリケーションは、大文字と小文字を区別せずに扱わなければなりません。しかし、標準に違反し、ブラウザーがよく使う大文字・小文字の表記に誤って依存するアプリケーションもあります。HTTP/2では、すべてのヘッダー名を小文字で交換しなければならず、HAProxyも同じ規則に従うため、この問題は重大になります。HTTPのバージョンに関係なく、クライアントとサーバーには、すべてのヘッダー名を小文字で送ります。

HAProxyがHTTP/1リクエストを受信すると、ヘッダー名を小文字に変換し、その表記で処理してサーバーに送ります。サーバーがHTTPの標準に違反し、HAProxyからのリクエストを処理できないと分かっている場合は、このオプションを有効にし、globalディレクティブ"h1-case-adjust"または"h1-case-adjust-file"で表記を変えるヘッダーの一覧を指定すると、リクエストを整形してサーバーへ送る際に、小文字のヘッダー名を別の表記に変換できます。このような回避策が必要なサーバーはコンテンツスマグリング攻撃に弱い可能性があり、必ず修正しなければならないため、サーバーを修正するまでの一時的な回避策としてのみ使用しなければなりません。

このオプションは、標準に準拠したサーバーには影響しません。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option h1-case-adjust-bogus-client"、"h1-case-adjust"、"h1-case-adjust-file"。

<a id="entry-4-2-option-http-buffer-request"></a>

**`option http-buffer-request`**

```haproxy
option http-buffer-request
no option http-buffer-request
```

処理を進める前にHTTPリクエスト本文全体を待つ機能を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

判断を下す前に、HTTPリクエストのボディを待ちたい場合があります。たとえば、"balance url_param"はこれを行います。最初の用途は、サーバーへ接続する前に、低速なクライアントからのリクエストをバッファーに格納することです。もう一つは、リクエストのボディの内容に基づいて、振り分け先を決めることです。フロントエンドまたはバックエンドにこのオプションを設定すると、ボディ全体を受信するかリクエストバッファーがいっぱいになるまで、HTTPの処理を待機させます。フロントエンドとバックエンドの間でバッファリングしない転送を期待するなど、HTTPを不適切に使うアプリケーションでは、望ましくない副作用が起きる可能性があります。そのため、デフォルトで使用することは明確に避けるべきです。

参照："option http-no-delay"、"timeout http-request"、"http-request wait-for-body"。

<a id="entry-4-2-option-http-drop-request-trailers"></a>

**`option http-drop-request-trailers`**

```haproxy
option http-drop-request-trailers
no option http-drop-request-trailers
```

サーバーへの送信時に、リクエストからHTTPトレーラーを削除します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 不可 \| 可

引数：なし

このオプションを有効にすると、リクエスト内のHTTPトレーラーを、サーバーへ送信する前にすべて削除します。

RFC9110#section-6.5.1は、トレーラーフィールドをヘッダーフィールドに統合できると規定しています。意図して行うべき処理ですが、アプリケーションによっては問題になることがあります。特に、悪意のあるクライアントがセキュリティ上重要なヘッダーフィールドをトレーラー部分に隠し、途中のコンポーネントが特別な確認なしにヘッダーへ統合する場合です。その場合、バックエンドでこのオプションを有効にすると、サーバーへ送信する前に、リクエスト内で見つかったトレーラーフィールドをすべて破棄します。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option http-drop-response-trailers"。

<a id="entry-4-2-option-http-drop-response-trailers"></a>

**`option http-drop-response-trailers`**

```haproxy
option http-drop-response-trailers
no option http-drop-response-trailers
```

クライアントへの送信時に、レスポンスからHTTPトレーラーを削除します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

このオプションは"option http-drop-request-trailers"と似ていますが、レスポンスをクライアントに送る前に、そのトレーラーフィールドを破棄するために使用しなければなりません。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option http-drop-request-trailers"。

<a id="entry-4-2-option-http-ignore-probes"></a>

**`option http-ignore-probes`**

```haproxy
option http-ignore-probes
no option http-ignore-probes
```

データのない接続とリクエストのタイムアウトのログ記録を有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

最近、一部のブラウザーが"pre-connect"機能を実装し始めました。利用者が訪問するかもしれない場合に備え、最近訪れたWebサイトに投機的に接続する機能です。その結果、Webサイトへの接続が多数確立され、先にタイムアウトすると408 Request Timeout、ブラウザーが先に閉じると400 Bad Requestになります。これらはログを埋め、エラーカウンターを増加させます。すでに"option dontlognull"がありますが、この場合には不十分です。代わりに、このオプションは次の処理を行います。- 閉じるまでに何も受信しなかった接続では、400/408メッセージをクライアントに送らないようにします。- この状況ではログを一切出さないようにします。- エラーカウンターを一切増加させないようにします。

このようにして、何も送られない接続を通知なしで無視します。ただし、実際の問題も隠すため、必要であることが明らかな場合を除き、使用しないほうがよいでしょう。リクエストを受信できず408になる最も一般的な理由は、クライアントとVPNなどの途中の要素でMTUが一致せず、大きすぎるパケットが遮断されることです。この問題は、POSTリクエストや大きなCookieを含むGETでよく見られます。検出する唯一の手段がログであることも多くあります。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"log"、"dontlognull"、"errorfile"、およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-http-keep-alive"></a>

**`option http-keep-alive`**

```haproxy
option http-keep-alive
no option http-keep-alive
```

HTTP/1.x接続で、クライアントからサーバーまでのHTTP keep-aliveを有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

既定では、HAProxyはHTTP/1.xの持続的接続をキープアライブモードで扱います。各接続についてリクエストとレスポンスを処理し、その後、両側の接続をアイドル状態のまま保持します。このモードは、"option http-server-close"や"option httpclose"などのオプションで変更できます。このオプションを使うとキープアライブモードに戻せるため、defaultsセクションで別のモードが使われている場合に便利です。

"option http-keep-alive"を設定すると、クライアント側とサーバー側の両方でHTTPキープアライブモードを有効にします。サーバーへのアイドル接続を保持する代わりに、クライアント側（低速なネットワーク）の遅延を最小にし、サーバー側で最も速くセッションを再利用できます。一般に、小さなオブジェクトでは、"http-server-close"オプションに比べて約二倍のリクエストレートを達成できます。このオプションが役立つ主な状況は、次の二つです。

    - サーバーがHTTPに準拠せず、リクエストではなく接続を認証する場合
      （NTLM認証など）

    - サーバーから対象のオブジェクトを取得するコストと比べて、サーバーへの接続を確立するコストが大きい場合です。

最後のケースは、サーバーがキャッシュ用の高速な静的サーバーである場合に起こり得ます。

現在、ログにはリクエストが同じセッションから来たかどうかは示されません。ログに記録される受け入れ日時は前のリクエストの終了時刻に対応し、リクエスト時間は新しいリクエストを待っていた時間に対応します。キープアライブのリクエスト時間にも、"timeout http-keep-alive"、またはそれが未設定なら"timeout http-request"で定義したタイムアウトが適用されます。

このオプションは、以前の"option httpclose"または"option http-server-close"を無効にし、置き換えます。

"option httpclose"、"option http-server-close"、"option prefer-last-server"、"option http-pretend-keepalive"も参照してください。

<a id="entry-4-2-option-http-no-delay"></a>

**`option http-no-delay`**

```haproxy
option http-no-delay
no option http-no-delay
```

HTTPでは性能よりも対話の遅延を低く抑えることを優先するよう、システムに指示します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

HTTPでは、各ペイロードは単方向で、双方向のやり取りという概念はありません。どのエージェントも、妥当に短い遅延の範囲で、データをある程度キューに格納することが想定されています。ごくまれに、HTTPプロトコルを不適切に使い、単一のリクエスト中に両方向で多数のデータチャンクを交互に送り、ペイロードの段階で高度な双方向性を期待するサーバー間アプリケーションがあります。これはHTTPの仕様ではまったくサポートせず、大半のプロキシやサーバーでは動作しません。このようなアプリケーションがHAProxyを経由すると、動作はしますが、性能を優先するネットワークの最適化により、大きな遅延が発生します。パケットを満杯にしてから送るため、十分なデータがそろうまで待つようシステムに指示するためです。典型的な遅延は往復ごとに約200 msです。これは異常な使い方でのみ起きます。CONNECTリクエストやWebSocketなど、通常の使い方には影響しません。

接続が使用するフロントエンドまたはバックエンドのどちらかに"option http-no-delay"を指定すると、やり取りをできる限り速くするため、この種の最適化をすべて無効にします。ただし、別の場所で動作しなくなる可能性があるため、機能を保証するものではありません。それでも、HAProxy経由で動作する場合は、可能な限り速く動作します。このオプションをデフォルトで決して使用すべきではありません。また、このような不具合のあるアプリケーションが見つからない限り、一切使用すべきではありません。使用すると帯域とCPUの使用量が増え、遅延が大きい環境では性能が大幅に低下する可能性があります。

参照："option http-buffer-request"。

<a id="entry-4-2-option-http-pretend-keepalive"></a>

**`option http-pretend-keepalive`**

```haproxy
option http-pretend-keepalive
no option http-pretend-keepalive
```

サーバーへのHTTP/1.x接続で、HAProxyがkeepaliveを通知するかどうかを定義します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

"option http-server-close"または"option httpclose"を使う場合、HAProxyはサーバーに転送するHTTP/1.xリクエストに、"Connection: close"ヘッダーを追加します。ところが一部のサーバーは、このヘッダーを見ると、まったく無関係であるにもかかわらず、長さが不明なレスポンスにチャンク転送符号化を使わなくなります。その結果、クライアントやキャッシュは、レスポンスが不完全であることに気付かずに受信し、完全なものとみなす可能性があります。

"option http-pretend-keepalive"を設定すると、HAProxyは接続を維持するとサーバーに思わせます。これにより、サーバーは前述の望ましくない異常な動作に切り替わらなくなります。HAProxyはレスポンス全体を受け取ると、"option httpclose"と同じようにサーバーとの接続を閉じます。その結果、クライアントは通常のレスポンスを取得し、サーバー側の接続も正しく閉じられます。

このオプションは、デフォルトでは有効にしないことを推奨します。大半のサーバーは、最後のパケットの後に自ら接続を閉じるほうが効率的で、バッファーも少し早く解放できるためです。また、ネットワーク上のパケットが増えることで、全体の最大性能がわずかに低下する可能性があります。ただし、有効にすると、HAProxyの処理は少し減ります。したがって、構成全体でHAProxyがボトルネックになっている場合は、CPUサイクルをいくらか節約できるかもしれません。

このオプションはbackendセクションとlistenセクションで設定できます。frontendセクションで使用すると無視され、起動時に警告を出します。バックエンドに関係するオプションなので、フロントエンドで設定する実質的な理由はありません。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option httpclose"、"option http-server-close"、"option http-keep-alive"。

<a id="entry-4-2-option-http-restrict-req-hdr-names"></a>

**`option http-restrict-req-hdr-names { preserve | delete | reject }`**

```haproxy
option http-restrict-req-hdr-names { preserve | delete | reject }
```

"[a-zA-Z0-9-]"以外の文字を含むHTTPリクエストヘッダー名に対するHAProxyの方針を設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
preserve  フィルタリングを無効にします。FastCGIアプリケーションを設定していない
          HTTPプロキシのデフォルトモードです。

delete    名前に"[a-zA-Z0-9-]"の文字集合に含まれない文字があるリクエストヘッダーを
          削除します。FastCGIアプリケーションを設定したHTTPバックエンドの
          デフォルトモードです。

reject    ヘッダー名に"[a-zA-Z0-9-]"の文字集合に含まれない文字がある場合、
          403-Forbiddenレスポンスでリクエストを拒否します。
```

このオプションは、リクエストのヘッダー名を英数字とハイフン（[A-Za-z0-9-]）に制限するために使用できます。ヘッダー名の一部の文字を扱えない、HTTPに準拠していないサーバーと相互運用するために、必須となる場合があります。FastCGIアプリケーションでも、ヘッダー名の英数字以外の文字をすべてアンダースコア（'\_'）に置き換えるため、必須となる場合があります。その結果、ヘッダー名を取り違えさせてルールを回避することが容易になります。たとえば、"X-Forwarded-For"と"X_Forwarded-For"は、FastCGIではどちらも"HTTP_X_FORWARDED_FOR"に変換します。

このオプションはプロキシごとに、http-requestルールの評価後に評価されます。

<a id="entry-4-2-option-http-server-close"></a>

**`option http-server-close`**

```haproxy
option http-server-close
no option http-server-close
```

サーバー側のHTTP/1.x接続のクローズを有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

デフォルトでは、HAProxyはHTTP/1.xの持続的接続をキープアライブモードで扱います。各接続でリクエストとレスポンスを処理し、両側の接続をアイドル状態のまま保持します。"option http-server-close"や"option httpclose"などのオプションで、このモードを変更できます。"option http-server-close"を設定すると、クライアント側ではHTTPキープアライブとパイプライン処理をサポートしたまま、サーバー側でHTTP接続を閉じるモードを有効にします。これにより、クライアント側（低速なネットワーク）の遅延を最小にし、サーバー側で最も速くセッションを再利用して、"option httpclose"と同様にサーバーのリソースを節約します。また、RFC7230の要件に準拠していれば、キープアライブをサポートしないサーバーに対しても、クライアント側ではキープアライブモードでサービスを提供できます。ただし、一部のサーバーはリクエスト内に"Connection: close"を見ると、これらの要件に常に従うとは限りません。その場合、キープアライブは一切使用されません。"option http-pretend-keepalive"を有効にすると回避できます。

現在、ログにはリクエストが同じセッションから来たかどうかは示されません。ログに記録される受け入れ日時は前のリクエストの終了時刻に対応し、リクエスト時間は新しいリクエストを待っていた時間に対応します。キープアライブのリクエスト時間にも、"timeout http-keep-alive"、またはそれが未設定なら"timeout http-request"で定義したタイムアウトが適用されます。

このオプションはフロントエンドとバックエンドの両方で設定できます。接続を保持するフロントエンドまたはバックエンドの少なくとも一方で有効になっていれば、有効になります。それ以前の"option httpclose"や"option http-keep-alive"は無効化され、このオプションに置き換わります。フロントエンドとバックエンドのオプションが異なる場合の組み合わせについては、[4節](/ja/haproxy/proxies/)「プロキシ」を確認してください。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option httpclose"、"option http-pretend-keepalive"、"option http-keep-alive"。

<a id="entry-4-2-option-http-use-proxy-header"></a>

**`option http-use-proxy-header`**

```haproxy
option http-use-proxy-header
no option http-use-proxy-header
```

Connectionの代わりに、非標準のProxy-Connectionヘッダーを使用します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

RFC7230は、HTTP/1.1エージェントが持続的接続と非持続的接続のどちらを望むかを示すために、Connectionヘッダーを使わなければならないと明記しています。しかし、ブラウザーとプロキシは、プロキシ経由の接続ではこのヘッダーを無視し、代わりに文書化されていない非標準のProxy-Connectionヘッダーを使います。ブラウザーとこの種のプロキシの間にロードバランサーを置くと、HAProxyの解釈とクライアントとプロキシの合意が異なるため、問題が起きます。

このオプションをフロントエンドで設定すると、HAProxyはプロキシを介したリクエストを検出したときに、その非標準ヘッダーを使うよう自動的に切り替えられます。ここでは、URIが'/'でも'\*'でも始まらないリクエストを、プロキシを介したリクエストと定義します。HTTPトンネルモードとは互換性がありません。このオプションを指定できるのはフロントエンドだけで、そのリクエストの処理全体に影響します。

また、このオプションを設定した場合、認証が必要なリクエストがプロキシ経由のものであれば、自動的にプロキシ認証ヘッダーを使うよう切り替えます。これにより、既存のプロキシの前段で認証を確認または強制できます。

通常、プロキシの前段以外では、このオプションは使用しないことを推奨します。

参照："option httpclose"、"option http-server-close"。

<a id="entry-4-2-option-httpchk"></a>

**`option httpchk`**

```haproxy
option httpchk
option httpchk <uri>
option httpchk <method> <uri>
option httpchk <method> <uri> <version>
option httpchk <method> <uri> <version> <host>
```

サーバーの稼働状態の確認にHTTPプロトコルを使用します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<method>  リクエストで使用する、省略可能なHTTPメソッドです。設定しない場合、
          "OPTIONS"メソッドを使用します。通常、サーバー側の処理が少なく、
          ログから簡単に除外できるためです。どのメソッドでも使用できますが、
          標準外のメソッドを考案することは推奨されません。

<uri>     HTTPリクエストで参照するURIです。デフォルトは" / "で、ほぼすべての
          サーバーでデフォルトでアクセス可能ですが、他のどのURIにも変更できます。
          クエリー文字列も使用できます。

<version> 省略可能なHTTPバージョン文字列です。デフォルトは"HTTP/1.0"ですが、
          HTTP 1.0では正常に動作しないサーバーもあるため、HTTP/1.1への変更が
          役立つ場合があります。HTTP/1.1ではHostフィールドが必須です。

<host>    省略可能なHTTP Hostヘッダーの値です。デフォルトでは設定しません。
          ログ形式文字列です。
```

既定では、サーバーのヘルスチェックはTCP接続の確立を試みるだけです。"option httpchk"を指定すると、TCP接続の確立後に完全なHTTPリクエストを送信します。2xxと3xxのレスポンスは正常と見なし、それ以外は応答がない場合も含めて、すべてサーバーの障害と見なします。

"http-check"ディレクティブと組み合わせると、HTTPヘルスチェックで送信するリクエストや、レスポンスを照合するルールをカスタマイズできます。TCPヘルスチェックの"tcp-check"ディレクティブと同様に、送信と応答検証のシーケンスを設定することもできます。

HTTPヘルスチェック用の接続を開く際は、既定ではサーバーの設定を使用します。ただし、"http-check connect"ルールを使ってサーバーのパラメーターを上書きすることもできます。

"httpchk"オプションは必ずしもHTTPバックエンドを必要とせず、通常のTCPバックエンドでも機能します。inetdデーモンを使い、専用ポートにバインドした単純なスクリプトを確認する場合に特に便利です。ただし、内部では常にHTXマルチプレクサーを使用します。そのため、リクエストの形式とレスポンスの解析には厳密な規則が適用されます。

例：

```shell
# Relay HTTPS traffic to Apache instance and check service availability
# using HTTP request "OPTIONS * HTTP/1.1" on port 80.
backend https_relay
    mode tcp
    option httpchk OPTIONS * HTTP/1.1
    http-check send hdr Host www
    server apache1 192.168.1.1:443 check port 80
```

関連項目: "option ssl-hello-chk"、"option smtpchk"、"option mysql-check"、"option pgsql-check"、"http-check"、およびserverオプションの"check"、"port"、"inter"を参照してください。

<a id="entry-4-2-option-httpclose"></a>

**`option httpclose`**

```haproxy
option httpclose
no option httpclose
```

HTTP/1.x接続のクローズを有効または無効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

既定では、HAProxyはHTTP/1.xの持続的接続をキープアライブモードで扱います。各接続についてリクエストとレスポンスを処理し、その後、両側の接続をアイドル状態のまま保持します。このモードは、"option http-server-close"や"option httpclose"などのオプションで変更できます。

"option httpclose"を設定すると、HAProxyは設定した場所に応じて、クライアントまたはサーバーとの接続を閉じます。クライアント接続にはフロントエンド、サーバー接続にはバックエンドの設定を適用します。リスナーで設定した場合は、クライアントとサーバーの両方の接続に適用します。各方向で"Connection: close"ヘッダーがすでに設定されているかを確認し、なければ追加します。

このオプションは"option http-pretend-keepalive"と組み合わせることもできます。その場合、"Connection: close"リクエストヘッダーの送信は無効になりますが、レスポンス全体を受信した後には接続を閉じます。

以前の"option http-server-close"または"option http-keep-alive"を無効にし、置き換えます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option http-server-close"。

<a id="entry-4-2-option-httplog"></a>

**`option httplog [ clf ]`**

```haproxy
option httplog [ clf ]
```

HTTPリクエスト、ストリームの状態、タイマーのログ記録を有効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
clf       "clf"引数を追加すると、出力形式はHAProxyのデフォルトのHTTP形式ではなく
          CLF形式になります。CLF形式しかサポートせず、拡張もできない特定の
          ログアナライザーにHAProxyのログを渡す必要がある場合に使用できます。
```

既定のログ出力形式は情報が乏しく、送信元と宛先のアドレス、およびインスタンス名しか含みません。"option httplog"を指定すると、各ログ行に含まれる情報が大幅に増えます。HTTPリクエスト、接続タイマー、ストリーム状態、接続数、取得したヘッダーとCookie、フロントエンド・バックエンド・サーバーの名前、そしてもちろん送信元アドレスとポートなどが含まれますが、これらに限りません。

"option httplog"だけを指定すると、デフォルトで設定されていた'clf'モードを自動的に解除します。

"option httplog"は、それより前のすべての"log-format"ディレクティブを上書きします。

ログについては、[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-httpslog"></a>

**`option httpslog`**

```haproxy
option httpslog
```

HTTPSリクエスト、ストリームの状態、タイマーのログ記録を有効にします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

デフォルトのログ出力形式は情報が乏しく、送信元と宛先のアドレス、およびインスタンス名だけを含みます。"option httpslog"を指定すると、各ログ行に含まれる情報が大幅に増えます。HTTPリクエスト、接続タイマー、ストリーム状態、接続数、取得したヘッダーとCookie、フロントエンド・バックエンド・サーバーの名前、SSL証明書の検証とSSLハンドシェイクの状態、そしてもちろん送信元アドレスとポートなどを含みますが、これらに限りません。

"option httpslog"は、それより前のすべての"log-format"ディレクティブを上書きします。

ログについては、[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-idle-close-on-response"></a>

**`option idle-close-on-response`**

```haproxy
option idle-close-on-response
no option idle-close-on-response
```

ソフトストップの進行中は、アイドル状態のフロントエンド接続を閉じないようにします。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

デフォルトでは、ソフト停止中にアイドル接続を閉じます。環境によっては、プロキシと通信するクライアントが、後でリクエストを送るためにアイドル接続を用意していることがあります。書き込みエラー時に適切な再試行を行わないと、HAProxyのリロード中にエラーが起きる可能性があります。適切な実装では接続や書き込みのエラー時に再試行するべきですが、このオプションは、バージョン2.4より前のHAProxyとの後方互換性を保つために導入しました。実際、v2.4より前のHAProxyは、最後のリクエストとレスポンスを待ち、閉じる前に"connection: close"ヘッダーを追加して、接続を再利用できなくなることをクライアントに通知していました。

実際の例では、AWSでHAProxyの前段にALBを配置した環境で、この動作が確認されました。結果として、HAProxyのリロード中にALBが502を返しました。

このオプションを使うと、接続が長時間アイドル状態のままである場合に、古いプロセスの数が増える可能性があることに注意してください。頻繁にリロードする場合は、クライアントタイムアウトや"hard-stop-after"パラメーターを、それに応じて調整する必要があるかもしれません。

参照："timeout client"、"timeout client-fin"、"timeout http-request"、"hard-stop-after"。

<a id="entry-4-2-option-independent-streams"></a>

**`option independent-streams`**

```haproxy
option independent-streams
no option independent-streams
```

両方向で独立したタイムアウト処理を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

既定では、ソケットからデータを送信すると、そのソケットの書き込みタイムアウトと読み取りタイムアウトの両方を更新します。ソケットで通信が行われていると見なし、データを受信すべきかどうかを推測するほかの手段がないためです。

このデフォルトの動作は、ほぼすべてのアプリケーションにとって望ましいものですが、無効にして、受信データがある場合だけ読み取りタイムアウトを更新したい状況もあります。telnetセッションのように、タイムアウトが長く、やり取りするデータが少ないストリームが該当します。サーバーが突然消えると、送信データがシステムのソケットバッファーに蓄積し、両方のタイムアウトが正しく更新されます。サーバーが受信していないと知る手段がないため、タイムアウトしません。しかし、基盤となるプロトコルが送信したデータを常にエコーする場合は、読み取りタイムアウトだけで問題を検出できます。より多くのデータをやり取りするプロトコルでは、データがソケットバッファー内に長く蓄積しないため、この問題は起きません。

このオプションをフロントエンドで設定すると、クライアントへのデータ送信に伴う読み取りタイムアウトの更新を無効にします。この用途はおそらくあまりありません。バックエンドで設定すると、サーバーへのデータ送信に伴う読み取りタイムアウトの更新を無効にします。この設定により、低速回線からの大きなHTTP POSTは通常失敗するようになるため、注意して使用してください。

参照："timeout client"、"timeout server"、"timeout tunnel"。

<a id="entry-4-2-option-ldap-check"></a>

**`option ldap-check`**

```haproxy
option ldap-check
```

サーバーの確認にLDAPv3ヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

サーバーがTCP接続を受け入れるかだけでなく、LDAPv3で正しく通信するかを確認できます。このオプションを設定すると、LDAPv3の匿名のシンプルバインドメッセージをサーバーに送り、レスポンスを解析してLDAPv3のバインドレスポンスメッセージを探します。

LDAPレスポンスのresultCodeが成功を示す場合にのみ、サーバーを有効とみなします（<http://tools.ietf.org/html/rfc4511#section-4.1.9>）。

bindリクエストのログ記録はサーバーによって異なります。設定方法はサーバーのドキュメントを参照してください。

例：

```text
option ldap-check
```

参照："option httpchk"。

<a id="entry-4-2-option-log-health-checks"></a>

**`option log-health-checks`**

```haproxy
option log-health-checks
no option log-health-checks
```

ヘルスチェックの状態更新のログ記録を有効または無効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

デフォルトでは、サーバーがUP状態のときは失敗したヘルスチェック、DOWN状態のときは成功したヘルスチェックを記録するため、追加情報の量は限られます。

このオプションを有効にすると、ヘルスチェックのステータスやサーバーの正常性の変化がすべて記録されます。そのため、サーバーがクラッシュする前に時々チェックに失敗していたことや、有効なHTTPステータスを返さなくなった正確な時点、続いてポートが接続を拒否し始めた時点、最後にサーバーがまったく応答しなくなった時点を把握できます。

ヘルスチェックに起因しない状態の変更（CLIでの有効化や無効化など）は、このオプションでは意図的にログに記録しません。

関連項目: "option httpchk"、"option ldap-check"、"option mysql-check"、"option pgsql-check"、"option redis-check"、"option smtpchk"、"option tcp-check"、"log"、およびログについて説明する[8節](/ja/haproxy/configuration-logging/)を参照してください。

<a id="entry-4-2-option-log-separate-errors"></a>

**`option log-separate-errors`**

```haproxy
option log-separate-errors
no option log-separate-errors
```

完全には成功しなかった接続のログレベルを変更します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

ログの中からエラーを見つけることは、必ずしも簡単ではありません。このオプションを使うと、HAProxyは、エラー、タイムアウト、再試行、再振り分け、HTTPの5xxステータスコードなど、関心を引く可能性のある情報を含むログのレベルを上げます。レベルは"info"から"err"に変わります。これにより、大半のsyslogデーモンで、別のファイルにも記録できます。ただし、元のファイルから削除しないよう注意してください。非常に重要な情報となる順序が分からなくなるためです。

このオプションを使うと、毎秒数千の接続を扱う大規模なサイトで、通常のトラフィックを循環バッファーに記録し、量の少ないエラーログだけをアーカイブできます。

"log"、"dontlognull"、"dontlog-normal"、およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-logasap"></a>

**`option logasap`**

```haproxy
option logasap
no option logasap
```

早期のログ記録を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

デフォルトでは、log-format文字列の定義に使用するすべてのログ形式のエイリアスとサンプル取得が値を返したとき、またはストリームが終了したときに、ログを出力します。これにより、組み込みのlog-format文字列で、転送時間やバイト数をログメッセージに含められます。

大きなファイルの転送やRDPなど、長時間続く接続を扱う場合、リクエストや接続がログに現れるまで時間がかかることがあります。"option logasap"を使うと、mode tcpではサーバーへの接続が確立した時点、mode httpではサーバーがヘッダー全体を送った時点で、直ちにログメッセージを作成します。ログでは、総バイト数はメッセージを作成するまでに転送したデータ量だけとなり、総時間も、残りの接続存続時間や転送時間を含まなくなるため、それらの情報が欠けます。HTTPの場合、少なくとも転送予定のバイト数がログに分かるよう、Content-Lengthレスポンスヘッダーを取得しておくのがよい方法です。

例：

```text
listen http_proxy 0.0.0.0:80
    mode http
    option httplog
    option logasap
    log 192.168.2.200 local3
```

```text
    >>> Feb  6 12:14:14 localhost \
          haproxy[14389]: 10.0.1.2:33317 [06/Feb/2009:12:14:14.655] http-in \
          static/srv1 9/10/7/14/+30 200 +243 - - ---- 3/1/1/1/0 1/0 \
          "GET /image.iso HTTP/1.0"
```

"option httplog"、"capture response header"、およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-mysql-check"></a>

**`option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]`**

```haproxy
option mysql-check [ user <username> [ { post-41 | pre-41 | post-80 } ] ]
```

サーバーの確認にMySQLヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<username> MySQLサーバーへの接続時に使用するユーザー名です。
post-41    v4.1以降のクライアントと互換性のあるチェックを送信します（デフォルト）。
pre-41     v4.1より前のクライアントと互換性のあるチェックを送信します。
post-80    CLIENT_PLUGIN_AUTHケーパビリティーを設定し、認証プラグインを
           mysql_native_passwordにした、v8.0以降のクライアントと互換性のある
           チェックを送信します。ヘルスチェック用ユーザーをmysql_native_password認証で
           作成したMySQL 8.0+サーバーに接続する場合、このオプションを使用してください。例：
             CREATE USER 'haproxy'@'%' IDENTIFIED WITH mysql_native_password BY '';
```

ユーザー名を指定した場合、チェックではMySQLセッションを正しく閉じるため、Client Authenticationパケット一つとQUITパケット一つの、計二つのMySQLパケットを送ります。続いて、MySQLのHandshake InitializationパケットやErrorパケットを解析します。基本的ですが有用なテストで、サーバーにエラーや接続中断を発生させません。ただし、ロックされておらず、権限を持ち、パスワードを設定していないユーザーが必要です。必要に応じてリソースを制限し、権限を抑えた基本的なMySQLユーザーを作成するには、次のようにします。

```text
CREATE USER '<username>'@'<ip_of_haproxy|network_of_haproxy/netmask>'
/*!50701 WITH MAX_QUERIES_PER_HOUR 1 MAX_UPDATES_PER_HOUR 0 */
/*M!100201 MAX_STATEMENT_TIME 0.0001 */;
```

ユーザー名を指定しない場合（非推奨であり、推奨しません）、チェックではMysqlのHandshake InitializationパケットまたはErrorパケットを解析するだけで、何も送信しません。チェックが頻繁すぎる場合や、トラフィックが十分にない場合に、ロックアウトが発生することが報告されています。この場合は、MySQLの"max_connect_errors"の値を確認する必要があります。前の接続が中断した後、MySQLの"max_connect_errors"未満の試行回数で接続に成功すると、そのホストのエラー数がゼロに戻るためです。HAProxyを実行するサーバーがブロックされた場合、解除する唯一の方法は"FLUSH HOSTS"文です。

データベースの存在や整合性は確認しないことに注意してください。これらを確認するには、たとえばxinetdを使う外部チェックを利用できます。

このチェックにはMySQL \>=3.22が必要です。古いバージョンにはTCPチェックを使用してください。

受信側のMySQLサーバーは通常、IPアドレスに基づく権限の照合や接続のログ記録など、さまざまな目的でクライアントのIPアドレスを知る必要があります。可能であれば、"source"キーワードの"usesrc"引数を使い、サーバーへの接続時にクライアントのIPアドレスを送信元として使うのが賢明な場合がよくあります。これには、透過プロキシ機能を組み込んでビルドしておくことと、MySQLサーバーがHAProxyの稼働するマシンを経由してクライアントへルーティングすることが必要です。

参照："option httpchk"。

<a id="entry-4-2-option-nolinger"></a>

**`option nolinger`**

```haproxy
option nolinger
no option nolinger
```

クローズ直後のセッションリソースの解放を有効または無効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

クライアントやサーバーが正常な手順を踏まずに接続を切断した場合（物理的に切断された場合など）、セッションのタイムアウトが発生してセッションを閉じます。ただし、システム内ではしばらくFIN_WAIT1状態のまま残り、リソースを使用するため、新しい接続を確立する能力が制限される可能性があります。

このような場合、"option nolinger"を有効にすると、ソケットを閉じたときに保留中のデータをシステムが直ちに削除するよう強制できます。その結果、TCP RSTを送信し、保留中のデータを切り捨て、セッションをシステムのテーブルから即座に削除します。クライアントから見た一般的な影響は、リダイレクトやエラーレスポンスなど、最後のデータブロックとともに接続を閉じた場合に、レスポンスが切り詰められることです。サーバー側では、トンネル内でクライアントの中断を転送する際に、送信元ポートを直ちに解放できる場合があります。どちらの場合もTCPリセットを送信しますが、セッションを即座に破棄するため、再送は行いません。パケット損失のあるネットワークでは、特に損失が発生する側にファイアウォールがあると、問題が増える可能性があります。ファイアウォールがリセットを受信して処理し、自身のセッションを削除した結果、相手側からの再送も含め、そのセッションの以後のトラフィックをすべて遮断する場合があるためです。相手側がリセットを受信できなかった場合、以後RSTを一切受信できず、ファイアウォールに多数の遮断パケットが記録される可能性があります。

以上の理由から、最後の手段としてどうしても必要な場合を除き、このオプションを使用しないことを強く推奨します。ほとんどの場合、"client-fin"または"server-fin"タイムアウトを使えば、より信頼できる動作で同様の結果を得られます。Linuxでは、bindまたはserverの"tcp-ut"設定を使うこともできます。

このオプションは、必要な側に応じて、フロントエンドとバックエンドのどちらでも使用できます。クライアント向けにはフロントエンドで、サーバー向けにはバックエンドで使用してください。技術的には"defaults"セクションでもサポートされますが、使用してはならないセクションに誤って継承され、問題を引き起こすおそれがあるため、そこで使用してはなりません。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"timeout client-fin"、"timeout server-fin"、bindまたはserverの"tcp-ut"キーワードも参照してください。

<a id="entry-4-2-option-originalto"></a>

**`option originalto [ except <network> ] [ header <name> ]`**

```haproxy
option originalto [ except <network> ] [ header <name> ]
```

サーバーに送信するリクエストへのX-Original-Toヘッダーの挿入を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<network> 任意の引数です。<network>に一致する送信元について、
          このオプションを無効にします。
<name>    別の"X-Original-To"ヘッダー名を指定するための
          任意の引数です。
```

HAProxyは透過モードで動作できるため、クライアントからの各リクエストをプロキシに転送し、HAProxy自体も複雑なSQUID環境へ各リクエストを中継できますが、SO_ORIGINAL_DSTで取得した宛先ホストの情報は失われます。宛先IPアドレスに基づくアクセスルールを使いたい場合、これは問題になります。解決するには、HAProxyからサーバーに送るすべてのリクエストに、新しいHTTPヘッダー"X-Original-To"を追加できます。このヘッダーの値は、元の宛先IPアドレスを表します。このヘッダーの最後の出現箇所だけを常に使うよう、設定しなければなりません。クライアントがすでにこのヘッダーを付けている可能性もあるため、最後の出現箇所だけを使用しなければなりません。

"header"キーワードを使うと、既定の"X-Original-To"を置き換える別のヘッダー名を指定できます。別のアプリケーションがすでに付けた"X-Original-To"ヘッダーがあり、それを保持する必要がある場合に便利です。また、バックエンドサーバーが"X-Original-To"ヘッダーを使わず、別のヘッダーを必要とする場合にも使えます。

クライアントから直接アクセスする場合と、リバースプロキシ経由でアクセスする場合とで、同じHAProxyインスタンスを共有することがあります。たとえば、SSLリバースプロキシでHTTPSトラフィックを復号する場合です。"except"キーワードの後にネットワークアドレスを指定すると、既知の宛先アドレスまたはネットワークに対して、ヘッダーの追加を無効にできます。この場合、そのネットワークに一致する宛先IPには、このヘッダーを追加しません。プライベートネットワークや127.0.0.1での使用が一般的です。IPv4とIPv6の両方をサポートします。

このオプションはフロントエンドとバックエンドのどちらでも指定できます。少なくとも一方で使用していれば、ヘッダーを追加します。両方でheaderサブ引数を定義している場合は、バックエンドの設定がフロントエンドより優先されます。

例：

```shell
# Original Destination address
frontend www
    mode http
    option originalto except 127.0.0.1

# Those servers want the IP Address in X-Client-Dst
backend www
    mode http
    option originalto header X-Client-Dst
```

参照："option httpclose"、"option http-server-close"。

<a id="entry-4-2-option-persist"></a>

**`option persist`**

```haproxy
option persist
no option persist
```

ダウンしたサーバーに接続先を強制的に固定する機能を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

停止したサーバーを参照するCookieを含むHTTPリクエストがバックエンドに届くと、デフォルトでは、別のサーバーへ振り分け直します。どうしても必要な場合は、"option persist"を使って、まず停止したサーバーにリクエストを送るよう強制できます。典型的な用途は、サーバーが極端に高負荷で、稼働と停止を繰り返している場合です。この場合、利用者は、正しく処理されることを期待して、セッションを開始したサーバーに引き続き振り分けられます。サーバーが完全に停止し、まったく接続できない場合に、最終的には利用可能な別のサーバーへクライアントを振り分けられるよう、"option redispatch"との併用を推奨します。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option redispatch"、"retries"、"force-persist"。

<a id="entry-4-2-option-pgsql-check-user"></a>

**`option pgsql-check user <username>`**

```haproxy
option pgsql-check user <username>
```

サーバーの確認にPostgreSQLヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<username> PostgreSQLサーバーへの接続時に使う
           ユーザー名です。
```

このチェックは、PostgreSQLのStartupMessageを送信し、AuthenticationリクエストまたはErrorResponseメッセージを待ちます。基本的ですが有用なテストで、サーバーにエラーや接続中断を発生させません。このチェックは"mysql-check"と同一です。

参照："option httpchk"。

<a id="entry-4-2-option-prefer-last-server"></a>

**`option prefer-last-server`**

```haproxy
option prefer-last-server
no option prefer-last-server
```

負荷分散された複数のリクエストを同じサーバーに維持できるようにします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

使用する負荷分散アルゴリズムが非決定的で、前のリクエストを送ったサーバーへの接続をHAProxyがまだ保持している場合、同じセッションの後続リクエストを、できるだけ同じサーバーへ送りたいことがあります。ただし、HAProxyが保証なしに適用を試みる優先方針を示すだけなので、接続先の固定とは異なります。実際の用途は、サーバーへのキープアライブ接続です。このオプションを使うと、HAProxyは、別のサーバーへ振り分け直して接続を閉じる代わりに、そのサーバーに関連付けられた同じ接続の再利用を試みます。静的ファイルを配信するサーバーで有用な場合があります。ハッシュアルゴリズムとの併用には、あまり意味がありません。非決定的な負荷分散アルゴリズムでは、HAProxyはすでに、401を返すサーバーや407（認証が必要）を返すプロキシに、自動的に接続を固定しようとします。これは、不完全なNTLM認証チャレンジを使うために必須であり、不具合のあるアプリケーションのトラブルシューティングにも大いに役立ちます。このような環境でも、ほかのレスポンスのたびにトラフィックを振り分け直すことを避けるため、option prefer-last-serverが望ましい場合があります。

どの負荷分散アルゴリズムが決定的とみなされるか、ここで明確にしておくと役立つでしょう。決定的なアルゴリズムは、利用可能なサーバーの集合が変わらない限り、同じクライアントデータに対して常に同じサーバーを選択します。一般に、受信リクエストのハッシュや検索によって対象のサーバーを選びますが、常にそうとは限りません。たとえば、"static-rr"も、サーバーの静的な重みに基づいて選択し、予測できるため、決定的とみなせます。"sticky"アルゴリズムは、再度訪れるクライアントに決定的な振り分けを提供します。

非決定的なアルゴリズムは、サーバーの動的な状態や単純な順番の切り替えに基づいてサーバーを選択するため、連続する二つのリクエストが同じサーバーに届く保証はありません。option prefer-last-serverは、特にこれらのアルゴリズム向けに設計されています。roundrobinやleastconnがその例です。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option http-keep-alive"。

<a id="entry-4-2-option-redispatch"></a>

**`option redispatch`**

```haproxy
option redispatch
option redispatch <interval>
no option redispatch
```

接続失敗時のセッションの再分配を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<interval> 接続の再試行時に再分配する頻度を制御する、省略可能な整数値です。
           正の値PはP回目の再試行ごとに再分配し、負の値Nは最後の再試行から
           数えたN番目の再試行で再分配することを示します。たとえば、デフォルトの-1は、
           最後の再試行で再分配する従来の動作を維持します。正の値1は毎回の
           再試行で再分配し、正の値3は3回目の再試行ごとに再分配することを示します。
           値0で再分配を無効にできます。

```

HTTPモードでは、Cookieが指定するサーバーが停止すると、クライアントがそのサーバーに固定されたままになる可能性があります。たとえば、"option persist"や"force-persist"を使っている場合です。クライアントはCookieを消去できないため、サービスにアクセスできなくなります。

"option redispatch"を指定すると、プロキシはCookieまたは一貫性ハッシュに基づく接続先の固定を解除し、稼働中のサーバーに再配分できます。

稼働系サーバーは、利用可能なサーバー一覧の一部から選択します。停止状態でもメンテナンス状態でもない稼働系サーバー（つまり、ヘルスチェックを行わないもの、またはチェックで"up"と確認されたもの）を、次の順序で選択します。

```text
1. 稼働中のバックアップ以外のサーバーがあれば、そのいずれか。または、

2. "allbackups"オプションが設定されていなければ、一覧の最初の
   バックアップサーバー。または、

3. "allbackups"オプションが設定されていれば、任意のバックアップサーバー。
```

リトライが発生すると、HAProxyは直前とは別のサーバーの選択を試みます。新しいサーバーは、現在のサーバー一覧から選択します。

ただし、再試行の間に一覧が更新されると、接続がバックアップサーバーへ振り分けられることがあります。たとえば、再試行が多数発生し、その間に、サーバーの停止を確認して一覧から除き、バックアップサーバーの一覧に切り替えるだけの時間が経過する場合です。

接続が複数回失敗した場合に、別のサーバーへの接続を再試行することもできます。当然ながら、"retries"をゼロ以外の値に設定しておく必要があります。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option persist"、"force-persist"、"retries"。

<a id="entry-4-2-option-redis-check"></a>

**`option redis-check`**

```haproxy
option redis-check
```

サーバーの確認にredisヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

サーバーがTCP接続を受け入れるかだけでなく、REDISプロトコルで正しく通信するかを確認できます。このオプションを設定すると、PING redisコマンドをサーバーに送り、レスポンスを解析して"+PONG"レスポンスメッセージを探します。

例：

```text
option redis-check
```

参照："option httpchk"、"option tcp-check"、"tcp-check expect"。

<a id="entry-4-2-option-smtpchk"></a>

**`option smtpchk`**

```haproxy
option smtpchk
option smtpchk <hello> <domain>
```

サーバーの確認にSMTPヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<hello>   省略可能な引数です。使用する"hello"コマンドを指定します。
          "HELO"（SMTP用）または"EHLO"（ESMTP用）を指定できます。
          それ以外の値はすべて、デフォルトのコマンド（"HELO"）に変換されます。

<domain>  サーバーに提示するドメイン名です。helloコマンドを指定した場合にのみ
          指定でき、その場合は必須です。デフォルトでは"localhost"を使用します。
```

"option smtpchk"を設定すると、ヘルスチェックはTCP接続の後にSMTPコマンドを送信する形になります。このコマンドは、既定では"HELO localhost"です。サーバーの返すコードを解析し、"2"で始まるコードだけを正常と見なします。それ以外の応答は、応答がない場合も含めてすべてエラーとなり、サーバーの停止を示します。

このテストは、SMTPサーバーまたはリレーで使用することを想定しています。リクエストによっては、サーバーが接続試行のたびにログを記録しない場合もあるため、動作を改善できるよう試すとよいでしょう。設定を調整するより、ポート25にtelnetで接続するほうが簡単なことがよくあります。

受信SMTPサーバーは通常、スパムのフィルタリング、なりすましの防止、ログ記録など、さまざまな目的でクライアントのIPアドレスを知る必要があります。可能であれば、"source"キーワードの"usesrc"引数を使い、サーバーへの接続時にクライアントのIPアドレスを送信元として使うのが賢明な場合がよくあります。これには、透過プロキシ機能を組み込んでビルドしておく必要があります。

例：

```text
option smtpchk HELO mydomain.org
```

参照："option httpchk"、"source"。

```haproxy
option socket-stats
no option socket-stats
```

ソケットごとに個別の統計を収集・提供する機能を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

<a id="entry-4-2-option-splice-auto"></a>

**`option splice-auto`**

```haproxy
option splice-auto
no option splice-auto
```

両方向のソケットで、自動的なカーネルアクセラレーションを有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

フロントエンドまたはバックエンドのどちらかでこのオプションを有効にすると、HAProxyは、クライアントとサーバーの間で、どちらの方向にもデータを転送する際に、カーネルのTCPスプライシングを使うかどうかを自動的に判断します。ヒューリスティックを使い、カーネルのスプライシングで性能が向上するかを見積もります。両方向は独立に扱います。過剰な使用を抑えるため、ヒューリスティックはあまり積極的には適用しません。このオプションには、コンパイル時にスプライシングを有効にしておく必要があります。globalオプション"nosplice"で、全体で無効にすることもできます。spliceはパイプを使うため、十分な数の空きパイプが必要です。

重要な注意： カーネルによるTCPスプライシングは、カーネル2.6.25で初めて登場したLinux固有の機能です。データをユーザー空間にコピーせずにソケット間で転送する、カーネルによる高速化機能で、性能の向上とCPUサイクルの節約に明確な効果があります。初期の実装の多くには不具合があり、データを破損させたり、非効率だったりするため、デフォルトでは有効にしていません。使用には細心の注意を払うべきです。実装が正しく動作するかを検出することはできませんが、正しく動く実装を初めて提供したバージョンは2.6.29です。判断に迷う場合は、globalキーワード"nosplice"で、スプライシングを全体で無効にできます。

例：

```text
option splice-auto
```

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"option splice-request"、"option splice-response"、グローバルオプション"nosplice"と"maxpipes"も参照してください。

<a id="entry-4-2-option-splice-request"></a>

**`option splice-request`**

```haproxy
option splice-request
no option splice-request
```

リクエスト用ソケットで、自動的なカーネルアクセラレーションを有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

フロントエンドまたはバックエンドのどちらかでこのオプションを有効にすると、HAProxyは可能な限りカーネルのTCPスプライシングを使い、クライアントからサーバーへデータを転送します。空きパイプがなくなった場合は、recv/send方式を使うこともあります。このオプションには、コンパイル時にスプライシングを有効にしておく必要があります。globalオプション"nosplice"で、全体で無効にすることもできます。spliceはパイプを使うため、十分な数の空きパイプが必要です。

重要な注意：使用上の制限は"option splice-auto"を参照してください。

例：

```text
option splice-request
```

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"option splice-auto"、"option splice-response"、グローバルオプション"nosplice"と"maxpipes"も参照してください。

<a id="entry-4-2-option-splice-response"></a>

**`option splice-response`**

```haproxy
option splice-response
no option splice-response
```

レスポンス用ソケットで、自動的なカーネルアクセラレーションを有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

フロントエンドまたはバックエンドのどちらかでこのオプションを有効にすると、HAProxyは可能な限りカーネルのTCPスプライシングを使い、サーバーからクライアントへデータを転送します。空きパイプがなくなった場合は、recv/send方式を使うこともあります。このオプションには、コンパイル時にスプライシングを有効にしておく必要があります。globalオプション"nosplice"で、全体で無効にすることもできます。spliceはパイプを使うため、十分な数の空きパイプが必要です。

重要な注意：使用上の制限は"option splice-auto"を参照してください。

例：

```text
option splice-response
```

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

"option splice-auto"、"option splice-request"、グローバルオプション"nosplice"と"maxpipes"も参照してください。

<a id="entry-4-2-option-spop-check"></a>

**`option spop-check`**

```haproxy
option spop-check
```

サーバーの確認にSPOPヘルスチェックを使用します。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

サーバーがTCP接続を受け入れるかだけでなく、SPOPプロトコルで正しく通信するかを確認できます。このオプションを設定すると、HAProxyとサーバーの間でHELLOハンドシェイクを行い、レスポンスを解析してエラーが報告されていないことを確認します。

例：

```text
option spop-check
```

参照："option httpchk"。

<a id="entry-4-2-option-srvtcpka"></a>

**`option srvtcpka`**

```haproxy
option srvtcpka
no option srvtcpka
```

サーバー側のTCP keepaliveパケットの送信を有効または無効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

クライアントとサーバーの間にファイアウォールなどのセッションを認識するコンポーネントがあり、プロトコルが長いアイドル期間を含む非常に長いセッションを使う場合（リモートデスクトップなど）、途中のコンポーネントが、長時間アイドル状態にあったセッションを期限切れにするおそれがあります。

ソケットレベルのTCP keep-aliveを有効にすると、システムは接続の相手側へ定期的にパケットを送信し、接続を維持します。keep-aliveプローブの間隔はシステムだけが制御し、オペレーティングシステムとその調整パラメーターの両方に依存します。

キープアライブパケットは、アプリケーションレベルでは送信も受信もされないことを理解する必要があります。それを認識するのはネットワークスタックだけです。そのため、プロキシの片側ですでにキープアライブを使って接続を維持していても、そのキープアライブパケットがプロキシの反対側に転送されることはありません。

これはHTTP keep-aliveとは関係がありません。

"srvtcpka"オプションを使うと、接続のサーバー側でTCPキープアライブプローブの送信を有効にします。HAProxyとサーバーの間でセッションの期限切れが見られる場合に役立つはずです。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option clitcpka"、"option tcpka"。

<a id="entry-4-2-option-ssl-hello-chk"></a>

**`option ssl-hello-chk`**

```haproxy
option ssl-hello-chk
```

サーバーの確認にSSLv3 client helloヘルスチェックを使用します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

SSLベースのプロトコルをHAProxy経由でTCPモードで中継する場合、サーバーがTCP接続を受け入れるかだけでなく、SSLで正しく通信するかを確認できます。"option ssl-hello-chk"を設定すると、サーバーへの接続が確立した後に、純粋なSSLv3のClient Helloメッセージを送り、レスポンスを解析してSSLのServer Helloメッセージを探します。レスポンスにこのServer Helloメッセージが含まれる場合だけ、サーバーを有効とみなします。

これまでにテストしたサーバーは、すべてSSLv3のClient Helloメッセージに正しく応答します。また、そのほとんどはHelloメッセージだけを含むリクエストをログにすら記録しないため、好都合です。

このチェックはSSLメッセージを組み立てるため、HAProxyにSSLサポートが組み込まれていなくても動作します。SSLサポートがある場合は、このチェックの代わりに、組み込みのSSLヘルスチェックを使うのが最善です。

参照："option httpchk"、"check-ssl"。

<a id="entry-4-2-option-tcp-check"></a>

**`option tcp-check`**

```haproxy
option tcp-check
```

tcp-checkのsend/expectシーケンスを使用してヘルスチェックを実行します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

このヘルスチェック方式は、"tcp-check"コマンドの一覧と組み合わせて、送信と期待値の確認からなるヘルスチェックのシーケンスに対応するためのものです。

TCPチェックは現在、4種類の動作モードをサポートします。- "tcp-check"ディレクティブがない場合: ヘルスチェックは接続試行だけを行います。これが引き続きデフォルトのモードです。

    - "tcp-check send"または"tcp-check send-binary"だけが指定されている場合:
      接続の開始とともに文字列を送信するために使用します。
      一部のプロトコルでは、たとえば"QUIT"メッセージを送ることで、
      ヘルスチェックのたびにサーバーが接続エラーを記録するのを防げます。
      この場合も、チェック結果は接続を開始できるかどうか
      だけによって決まります。

    - "tcp-check expect"だけが指定されている場合: バナーのテストに使います。
      接続を開き、HAProxyはサーバーが何らかの内容を提示するのを待ちます。
      その内容は、指定したルールを満たさなければなりません。
      チェックの結果は、内容とルールが一致するかどうかによって決まります。
      POP、IMAP、SMTP、FTP、SSH、TELNETに適しています。

    - "tcp-check send"と"tcp-check expect"の両方を指定した場合: Hello型のプロトコルをテストするために使用します。HAProxyがメッセージを送り、サーバーが応答すると、そのレスポンスを解析します。チェックの結果は、レスポンスの内容とルールの照合に基づきます。バインドやリクエストとレスポンスのモデルが必要なプロトコルによく適しています。LDAP、MySQL、Redis、SSLなどが該当しますが、これらにはすでに、各プロトコルをより深く理解する専用のチェックがあります。このモードでは、複数の問い合わせを送り、複数の回答を解析できます。

第5のモードでは、スクリプトのさまざまな段階にコメントを挿入できます。

作成する各tcp-checkルールには、"comment"ディレクティブの後に文字列を指定できます。この文字列をログに記録し、デバッグモードでは標準エラー出力にも表示します。利用者に分かりやすいエラー報告に役立ちます。もちろん、"comment"は省略可能です。

ヘルスチェックの実行中は、"tcp-check set-var"操作でデータサンプルを保存するための変数スコープが利用できます。"tcp-check unset-var"を使えば、それらの変数を解放できます。

例：

```shell
# perform a POP check (analyze only server's banner)
option tcp-check
tcp-check expect string +OK\ POP3\ ready comment POP\ protocol

# perform an IMAP check (analyze only server's banner)
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready comment IMAP\ protocol

# look for the redis master server after ensuring it speaks well
# redis protocol, then it exits properly.
# (send a command then analyze the response 3 times)
option tcp-check
tcp-check comment PING\ phase
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check comment role\ check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check comment QUIT\ phase
tcp-check send QUIT\r\n
tcp-check expect string +OK

HTTPリクエストを組み立て、そのレスポンスを解析します
（解析前に複数のヘッダーを送信します）
option tcp-check
tcp-check comment forge\ and\ send\ HTTP\ request
tcp-check send HEAD\ /\ HTTP/1.1\r\n
tcp-check send Host:\ www.mydomain.com\r\n
tcp-check send User-Agent:\ HAProxy\ tcpcheck\r\n
tcp-check send \r\n
tcp-check expect rstring HTTP/1\..\ (2..|3..) comment check\ HTTP\ response

```

参照："tcp-check connect"、"tcp-check expect"、"tcp-check send"。

<a id="entry-4-2-option-tcp-smart-accept"></a>

**`option tcp-smart-accept`**

```haproxy
option tcp-smart-accept
no option tcp-smart-accept
```

acceptシーケンスでACKパケットを1つ節約する機能を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：なし

HTTP接続要求が届くと、システムはHAProxyに代わって確認応答を返します。続いてクライアントが直ちにリクエストを送り、システムはHAProxyに新しい接続を通知する間に、そのリクエストにも確認応答を返します。その後、HAProxyがリクエストを読み取り、レスポンスを返します。リクエストへの確認応答はHAProxyがレスポンスを送る際に一緒に返せるため、システムが送信するTCP ACKが一つ余分であることになります。

このため、HTTPモードでは、HAProxyは、サポートするプラットフォーム（現在は少なくともLinux）で、この不要なACKを送らないようシステムに自動的に要求します。レスポンスの到着に想定以上の時間がかかっても、システムは40 ms後にACKを送るため、問題が生じることはないはずです。

複雑なネットワークのデバッグでは、この最適化を無効にしたい場合があります。遅延ACKがあると、パケットがどこで遅れているかを特定する際に、トラブルシューティングが複雑になるためです。"no option tcp-smart-accept"を指定すると、通常の動作に戻せます。

HTTP以外のプロキシでも、"option tcp-smart-accept"を指定するだけで強制的に有効にできます。たとえば、SMTPのようにサーバーが最初に送信するサービスでも、意味を持つ場合があります。

defaultsセクションでこのオプションを強制的に設定することは避けるよう推奨します。判断に迷う場合は、前に"default"キーワードを付けて自動設定値に戻すか、"no"キーワードで無効にすることを検討してください。

参照："option tcp-smart-connect"。

<a id="entry-4-2-option-tcp-smart-connect"></a>

**`option tcp-smart-connect`**

```haproxy
option tcp-smart-connect
no option tcp-smart-connect
```

connectシーケンスでACKパケットを1つ節約する機能を有効または無効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

特定のシステム（少なくともLinux）では、接続要求に対して空のACKを直ちに送る代わりに、バッファー内のリクエストを直接送るよう、HAProxyがカーネルに要求できます。これによりネットワーク上のパケットを一つ減らせるため、性能が向上します。また、受信接続と同時にリクエストを取得できるため、一部のサーバーにも有用です。

この機能は、バックエンドで"option tcp-smart-connect"を設定すると有効になります。ネットワークのトラブルシューティングが複雑になるため、デフォルトでは有効にしていません。

これを有効にする意味があるのは、HTTPのようにクライアントが最初に送信するプロトコルだけです。それ以外で、ACKの代わりに送るデータがなければ、通常のACKを送信します。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

参照："option tcp-smart-accept"。

<a id="entry-4-2-option-tcpka"></a>

**`option tcpka`**

```haproxy
option tcpka
```

両側のTCP keepaliveパケットの送信を有効または無効にします。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

クライアントとサーバーの間にファイアウォールなどのセッションを認識するコンポーネントがあり、プロトコルが長いアイドル期間を含む非常に長いセッションを使う場合（リモートデスクトップなど）、途中のコンポーネントが、長時間アイドル状態にあったセッションを期限切れにするおそれがあります。

ソケットレベルのTCP keep-aliveを有効にすると、システムは接続の相手側へ定期的にパケットを送信し、接続を維持します。keep-aliveプローブの間隔はシステムだけが制御し、オペレーティングシステムとその調整パラメーターの両方に依存します。

キープアライブパケットは、アプリケーションレベルでは送信も受信もされないことを理解する必要があります。それを認識するのはネットワークスタックだけです。そのため、プロキシの片側ですでにキープアライブを使って接続を維持していても、そのキープアライブパケットがプロキシの反対側に転送されることはありません。

これはHTTP keep-aliveとは関係がありません。

"tcpka"オプションを使うと、接続のクライアント側とサーバー側の両方で、TCPキープアライブプローブの送信を有効にします。ただし、両側に適用する意味があるのは、"defaults"または"listen"セクションだけです。フロントエンドで使用するとクライアント側だけ、バックエンドで使用するとサーバー側だけにキープアライブを適用します。このため、設定をフロントエンドとバックエンドに分けている場合は、"option clitcpka"と"option srvtcpka"を明示的に使用することを強く推奨します。

参照："option clitcpka"、"option srvtcpka"。

<a id="entry-4-2-option-tcplog"></a>

**`option tcplog [clf]`**

```haproxy
option tcplog [clf]
```

ストリームの状態とタイマーを含む、TCP接続の詳細なログ記録を有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
clf       "clf"引数を追加すると、出力形式はHAProxyのデフォルトのTCP形式ではなく
          CLF形式になります。CLF形式しかサポートせず、拡張もできない特定の
          ログアナライザーにHAProxyのログを渡す必要がある場合に使用できます。
          この形式はHTTP形式を想定しているため、一部の値は事前に設定されます。
          httpリクエストはTCP、レスポンスコードは000と表示されます。
```

デフォルトのログ出力形式は情報が乏しく、送信元と宛先のアドレス、およびインスタンス名だけを含みます。"option tcplog"を指定すると、各ログ行に含まれる情報が大幅に増えます。接続タイマー、ストリーム状態、接続数、フロントエンド・バックエンド・サーバーの名前、そしてもちろん送信元アドレスとポートなどを含みますが、これらに限りません。このオプションは、TCPだけを扱うプロキシで、クライアントとサーバーのどちらが切断したりタイムアウトしたりしたかを調べるために役立ちます。通常のHTTPプロキシでは、さらに情報が豊富な"option httplog"を使うほうがよいでしょう。

"option tcplog"は、それより前のすべての"log-format"ディレクティブを上書きします。

"option httplog"およびログに関する[セクション8](/ja/haproxy/configuration-logging/)も参照してください。

<a id="entry-4-2-option-transparent"></a>

**`option transparent        (deprecated)`**

```haproxy
option transparent        (deprecated)
no option transparent     (deprecated)
```

クライアント側の透過プロキシを有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

このオプションは、レイヤー3のロードバランサーにレイヤー7での接続先の固定を提供するために導入しました。リモートアドレス宛ての受信接続をローカルプロセス（ここではHAProxy）に転送するOSの機能を使い、当初要求されたアドレスをそのプロセスに知らせる仕組みです。このオプションを使うと、Cookieのないセッションは、受信リクエストの元の宛先IPアドレス（別の機器のアドレスに一致するはずです）に転送します。一方、Cookieを含むリクエストは、引き続き適切なサーバーに転送します。

よくある誤解とは異なり、このオプションによって、HAProxyが接続確立時にクライアントのIPをサーバーへ提示することはありません。

内部的な技術上の制約がいくつもあったため、このオプションは3.3以降、非推奨になりました。使用すると警告を出しますが、どうしても必要な場合は、globalキーワード"expose-deprecated-directives"で警告を抑止できます。

正しい方法は、アドレス0.0.0.0のサーバーを宣言することです。そのサーバーが、期待する宛先アドレスへの接続を担当します。また、対象サーバーへのアイドル接続も適切に処理します。

例：

```shell
# option transparent  ## before 3.3
server transparent 0.0.0.0
```

"source"キーワードの"usesrc"引数、および"bind"キーワードの"transparent"オプションも参照してください。

option use-small-buffers [ queue \| l7-retries \| check ]\*

指定されたカテゴリで小さいバッファーのサポートを有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

このオプションを使うと、メモリーを節約するため、さまざまな箇所で小さなバッファーのサポートを有効にできます。パラメーターを指定しないデフォルトでは、使用できるすべての箇所で、可能な限り小さなバッファーを使います。次の箇所に使用を限定することもできます。

- queue：設定すると、接続がキューに入る際に、リクエストが十分小さければ、小さいバッファーに保存します。
- l7-retries：設定すると、L7リトライが有効な場合に、小さいバッファーでリクエストを保存します。
- check：設定すると、ヘルスチェックリクエストに小さいバッファーを使用します。

有効にすると小さなバッファーを使いますが、使用可能な場合に限ります。データが大きすぎる場合は、自動的に通常のバッファーを使用します。小さなバッファーのサイズは、global設定"tune.bufsize.small"で変更できます。

"defaults"セクションでこのオプションを有効にしている場合、特定のインスタンスで前に"no"キーワードを付けると無効にできます。

tune.bufsize.smallも参照してください。

<a id="entry-4-2-persist-rdp-cookie"></a>

**`persist rdp-cookie`**

```haproxy
persist rdp-cookie
persist rdp-cookie(<name>)
```

RDP Cookieに基づく接続先の固定を有効にします。

使用可能なコンテキスト：tcp

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<name>    確認するRDP Cookieの名前です。省略可能で、省略すると
          デフォルトのCookie名"msts"を使います。現在、
          この名前を変更する正当な理由はありません。
```

この文は、RDP Cookieに基づく接続先の固定を有効にします。RDP Cookieには、既知のサーバーの一覧からサーバーを見つけるために必要な情報がすべて含まれています。そのため、このオプションをバックエンドで設定すると、リクエストを解析し、RDP Cookieが見つかった場合はデコードします。Cookieが既知のサーバーに一致し、そのサーバーがまだUP状態である場合（または"option persist"が設定されている場合）、接続をそのサーバーに転送します。

これはTCPバックエンドでのみ意味を持ちます。ただし、動作させるには、リクエストバッファーにRDP Cookieが存在することを確認できるだけの時間、フロントエンドで待機している必要があります。これは、"rdp-cookie"負荷分散方式と同じ要件です。そのため、すべての文を一つの"listen"セクションにまとめることを強く推奨します。

また、ターミナルサーバーがこのRDP Cookieを送信するのは、"token redirection mode"に設定されている場合だけです。これは、"IP address redirection"オプションが無効であることを意味します。この点を理解することが重要です。

例：

```text
listen tse-farm
    bind :3389
    # wait up to 5s for an RDP cookie in the request
    tcp-request inspect-delay 5s
    tcp-request content accept if RDP_COOKIE
    # apply RDP cookie persistence
    persist rdp-cookie
    # if server is unknown, let's balance on the same cookie.
    # alternatively, "balance leastconn" may be useful too.
    balance rdp-cookie
    server srv1 1.1.1.1:3389
    server srv2 1.1.1.2:3389
```

"balance rdp-cookie"、"tcp-request"、"req.rdp_cookie" ACLも参照してください。

<a id="entry-4-2-quic-initial"></a>

**`quic-initial <action> [ { if | unless } <condition> ]`**

```haproxy
quic-initial <action> [ { if | unless } <condition> ]
```

受信したQUIC Initialパケットに対して、アクションを実行します。"tcp-request connection"とは異なり、接続を構成する要素の生成や、SSLハンドシェイクの開始と完了より前に実行するため、接続試行を拒否する場合に効率的です。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 不可

引数：

```text
<action>    条件が適用される場合に実行するアクションを定義します。後述します。

<condition> レイヤー4のみを対象とする、標準的なACLに基づく条件です
            （セクション7を参照）。ただし、QUIC initialルールは、一部のレイヤー4の
            サンプル取得メソッドにとっても早すぎる段階で実行されます。
            設定時に警告は出ませんが、クラッシュはしないものの、実行時の動作が
            未規定になる可能性があります。現在サポートされているのは、内部サンプルと
            レイヤー4の"src*"、"dst*"だけであると考えてください。

```

このアクションは、QUICパケットの解析の早い段階で実行します。そのため、サポートするアクションは最小限で、次のものだけです。- accept - dgram-drop - reject - send-retry

<a id="entry-4-2-rate-limit-sessions"></a>

**`rate-limit sessions <rate>`**

```haproxy
rate-limit sessions <rate>
```

フロントエンドで毎秒受け付ける新しいセッション数の上限を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<rate>    <rate>パラメーターは、フロントエンドで毎秒受け付ける
          新規セッションの最大数を表す整数です。
```

フロントエンドの毎秒の新規セッション数が指定した値に達すると、レートが再び上限を下回るまで、新しい接続の受け入れを停止します。その間、保留中のセッションはソケットのバックログ（システムのバッファー）内に保持され、HAProxyは待機中のセッションがあることさえ認識しません。負荷の高いサービスに非常に低い上限を適用する場合は、"backlog"キーワードでソケットのバックログを増やすことが適切な場合があります。

この機能は、接続を使った攻撃や、負荷に弱いサーバーに対するサービスの不正利用を遮断する際に、特に効果的です。セッションレートをミリ秒ごとに測定するため、極めて正確です。また、上限は直ちに適用し、しきい値の検出に待ち時間は一切必要ありません。

例：SMTPの接続レートを毎秒最大10に制限します。

```haproxy
listen smtp
    mode tcp
    bind :25
    rate-limit sessions 10
    server smtp1 127.0.0.1:1025
```


注意： 最大レートに達してもフロントエンドの状態は変わりませんが、"socket-stats"オプションを有効にしている場合、そのソケットは統計に"WAITING"として表示されます。

"backlog"キーワードと"fe_sess_rate" ACL条件も参照してください。

<a id="entry-4-2-redirect-location"></a>

**`redirect location <loc> [code <code>] <option> [{if | unless} <condition>]`**

```haproxy
redirect location <loc> [code <code>] <option> [{if | unless} <condition>]
redirect prefix   <pfx> [code <code>] <option> [{if | unless} <condition>]
redirect scheme   <sch> [code <code>] <option> [{if | unless} <condition>]
```

if/unlessによる条件の一致または不一致に応じて、HTTPリダイレクトを返します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

ifでは条件に一致した場合、unlessでは一致しない場合に、HTTPリクエストに対してリダイレクトのレスポンスを返します。条件を指定しなければ、無条件にリダイレクトします。

引数：

```text
<loc>     "redirect location"では、<loc>の正確な値をHTTPの"Location"ヘッダーに
          設定します。"http-request"ルールで使用する場合、<loc>の値はカスタムログ
          形式の規則に従い、動的な値を含めることができます
          （セクション8.2.6のカスタムログ形式を参照）。

<pfx>     "redirect prefix"では、<pfx>と完全なURIパスを連結して"Location"ヘッダーを
          作成します。"drop-query"オプションを指定しない限り、クエリー文字列も
          含みます（後述）。特殊なケースとして、<pfx>が正確に"/"である場合、
          元のURIの前には何も挿入しません。これにより、たとえばCookieの挿入のために、
          同じURLへリダイレクトできます。"http-request"ルールで使用する場合、
          <pfx>の値はカスタムログ形式の規則に従い、動的な値を含めることができます
          （セクション8.2.6のカスタムログ形式を参照）。

<sch>     "redirect scheme"では、<sch>、"://"、"Host"ヘッダーの最初の値、
          URIパスを順に連結して"Location"ヘッダーを作成します。"drop-query"
          オプションを指定しない限り、クエリー文字列も含みます（後述）。パスが
          見つからない場合や、パスが"*"の場合は、代わりに"/"を使用します。
          "Host"ヘッダーが見つからない場合、空のホスト部分を返します。
          最近のブラウザーの大半は、これを同じホストへのリダイレクトと解釈します。
          このディレクティブは、主にHTTPからHTTPSへのリダイレクトに使用します。
          "http-request"ルールで使用する場合、<sch>の値はカスタムログ形式の規則に
          従い、動的な値を含めることができます（セクション8.2.6のカスタムログ形式を参照）。

<code>    コードは省略可能で、要求するHTTPリダイレクトの種類を示します。
          サポートされるコードは301、302、303、307、308のみで、指定しない場合は
          デフォルトで302を使用します。301は"Moved permanently"を意味し、
          ブラウザーはLocationをキャッシュすることがあります。302は"Moved temporarily"を
          意味し、ブラウザーはリダイレクトをキャッシュすべきではないことを示します。
          303は、ブラウザーがGETメソッドで移動先を取得する点を除いて302と同じです。
          307は302と同様ですが、同じメソッドを再使用する必要があることを明示します。
          同様に、同じメソッドを使用する必要がある場合、301の代わりに308を使用します。

<option>  リダイレクトの動作を調整するために、複数のオプションを指定できます。

  - "drop-query"
    プレフィックスに基づくリダイレクトでこのキーワードを使用すると、移動先には
    クエリー文字列を一切含めません。たとえば、暗号化されていないページへユーザーを
    誘導する場合に役立ちます。location型のリダイレクトには効果がありません。

  - "append-slash"
    このキーワードは"drop-query"と併用でき、末尾が'/'でないURLを使用する
    ユーザーを、末尾に'/'を付けた同じURLへリダイレクトします。
    検索エンジンに単一のURLだけを認識させるのに役立ちます。
    この用途では、戻りコード301が推奨されます。

  - "ignore-empty"
    このキーワードは、ログ形式の式で移動先を生成する場合にのみ効果があります
    （つまり、http-requestまたはhttp-responseで使用する場合）。式の結果が空なら、
    ルールを通知なしにスキップすることを指定します。主な用途は、単純なmapを使って
    既知のパスを一括でリダイレクトできるようにすることです。

  - "set-cookie NAME[=value]"
    NAME（必要に応じて"=value"も）を含む"Set-Cookie"ヘッダーをレスポンスに
    追加します。たとえば特定の種類のDoSから保護するため、ユーザーがすでに
    訪問済みであることを示す用途に使う場合があります。ほかのCookieオプションは
    追加しないため、セッションCookieになります。ブラウザーは、等号を伴わない
    Cookie名だけの指定と、等号を伴うCookieを区別します。

  - "set-cookie-fmt <fmt>"
    上のオプションと同じですが、"Set-Cookie"ヘッダーにはログ形式文字列<fmt>の
    評価結果を設定します。設定解析時に特別なチェックは行わないため、
    "NAME[=value]"形式を守るよう注意してください。

  - "clear-cookie NAME[=]"
    NAME（必要に応じて"="も）を含む"Set-Cookie"ヘッダーを追加しますが、
    "Max-Age"属性をゼロに設定します。これにより、ブラウザーにこのCookieの削除を
    指示します。たとえばログアウトページで役立ちます。Cookie "NAME"を削除しても、
    "NAME=value"として設定したCookieは削除されません。ブラウザーが両者を区別する
    ため、その場合はCookie "NAME="を削除する必要があります。

  - "keep-query"
    locationに基づくリダイレクトでこのキーワードを使用すると、元のURIにクエリー
    文字列があれば、移動先に追加します。クエリー文字列が見つからなければ、
    何も追加しません。移動先にすでにクエリー文字列がある場合は、
    '&'区切りで元のクエリー文字列を追加します。

```

例: ログインURLだけをHTTPSに移します。

```haproxy
acl clear      dst_port  80
acl secure     dst_port  8080
acl login_page url_beg   /login
acl logout     url_beg   /logout
acl uid_given  url_reg   /login?userid=[^&]+
acl cookie_set hdr_sub(cookie) SEEN=1

redirect prefix   https://mysite.com set-cookie SEEN=1 if !cookie_set
redirect prefix   https://mysite.com           if login_page !secure
redirect prefix   http://mysite.com drop-query if login_page !uid_given
redirect location http://mysite.com/           if !login_page secure
redirect location / clear-cookie USERID=       if logout
```



例: '/'のない記事へのリクエストにリダイレクトを返します。

```haproxy
acl missing_slash path_reg ^/article/[^/]*$
redirect code 301 prefix / drop-query append-slash if missing_slash
```


例：HAProxyがSSLを処理する場合に、すべてのHTTPトラフィックをHTTPSにリダイレクトします。

```haproxy
redirect scheme https if !{ ssl_fc }
```


例: すべてのホストのうち、接頭辞'www.'が付いていないものにそれを追加します。

```haproxy
http-request redirect code 301 location      \
  http://www.%[hdr(host)]%[capture.req.uri]  \
  unless { hdr_beg(host) -i www }
```


例: 古いURLだけを新しいURLへ恒久的にリダイレクトします。

```haproxy
http-request redirect code 301 location               \
  %[path,map_str(old-blog-articles.map)] ignore-empty
```


ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-retries"></a>

**`retries <value>`**

```haproxy
retries <value>
```

失敗後にサーバーに対して行う再試行の回数を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<value>   障害の後、サーバーへのリクエストまたは接続試行を
          再試行する回数です。
```

既定では、再試行は新しい接続の試行にのみ適用されます。ただし、"retry-on"ディレクティブを使用すると、ほかの条件（空のレスポンス、望ましくないステータスコードなど）でも再試行が発生する場合があります。それぞれが一回の試行として数えられ、試行の合計回数がここで指定した値に達すると、エラーが返されます。

再起動中のサーバーに直ちに再接続することを避けるため、同じサーバーへ再試行する前に、min("timeout connect", 一秒)の待ち時間を設けます。

"option redispatch"を設定すると、Cookieが別のサーバーを参照していても、一部の再試行をほかのサーバーで行うことがあります。"option redispatch"に引数を渡さない限り、既定では最後の再試行だけが対象です。

参照："option redispatch"。

<a id="entry-4-2-retry-on"></a>

**`retry-on [space-delimited list of keywords]`**

```haproxy
retry-on [space-delimited list of keywords]
```

失敗したリクエストの自動再試行を、どのような場合に試みるかを指定します。この設定が有効なのは"mode"がhttpの場合だけで、それ以外では通知なしで無視します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
 <keywords>  キーワードまたはHTTPステータスコードの空白区切りリストです。
             各項目は、リクエストの再試行を望む障害イベントの種類を表します。
             この設定を変更する前に、末尾の注意事項を読んでください。
             次のキーワードをサポートします。

   none              再試行しません。

   conn-failure      接続またはSSLハンドシェイクが失敗し、リクエストを送信できなかった
                     場合に再試行します。これがデフォルトです。

   empty-response    リクエストの一部を送信した後、サーバーから何も受信しないまま
                     サーバー接続が閉じられた場合に再試行します。この種類の障害は、
                     サーバー側のリクエストタイムアウト、ネットワーク状態の悪化、
                     リクエスト処理中のサーバーのクラッシュや再起動などで起こり得ます。

   junk-response     サーバーが完全なHTTPレスポンスとはみなせない内容を返した場合に
                     再試行します。不完全なレスポンスヘッダーやHTTP以外の内容も
                     含みます。通常、このような場合の再試行は推奨されません。
                     設定の問題（誤ったサーバーポート）や、サーバーに害を及ぼす
                     リクエスト（バッファーオーバーフロー攻撃など）が原因の可能性が
                     あるためです。

   response-timeout  リクエストに対するサーバーの応答を待つ間に、サーバータイムアウトが
                     発生した場合です。ネットワーク状態の悪化、経路上で期限切れに
                     なったアイドル接続の再利用、リクエスト処理の極端な高コストなどが
                     原因になり得ます。フルスキャンなど、負荷の高いデータベース処理を
                     行うサーバーで、このような場合に再試行することは一般に
                     推奨されません。サービス拒否攻撃を増幅する可能性があるためです。

   0rtt-rejected     早期データで送信され、サーバーに拒否されたリクエストを再試行します。
                     一般に、これらのリクエストは安全に再試行できるとみなされます。

   <status>          次のいずれかのHTTPステータスコードです。"401" (Unauthorized)、
                     "403" (Forbidden)、"404" (Not Found)、"408" (Request Timeout)、
"421" (Misdirected Request)、"425" (Too Early)、
"429" (Too Many Requests)、"500" (Server Error)、
"501" (Not Implemented)、"502" (Bad Gateway)、
"503" (Service Unavailable)、"504" (Gateway Timeout)。

   all-retryable-errors
                     再試行可能とみなされるすべてのエラーでリクエストを再試行します。
                     現在、"conn-failure"、"empty-response"、"junk-response"、
                     "response-timeout"、"0rtt-rejected"、"500"、"502"、"503"、
                     "504"を有効にします。
```

このディレクティブを使用すると、以前の設定はすべて新しい設定に置き換わります。累積はしません。

"none"と"conn-failure"以外を使うと、バッファーを割り当ててリクエスト全体をコピーする必要があるため、メモリーと性能に影響します。単一のバッファーに収まらないリクエストは、決して再試行しません（globalのtune.bufsize設定を参照してください）。

リクエストで渡す一意のトランザクションIDなど、リプレイを防ぐ仕組みをアプリケーションが備えているか、同じリクエストを再実行しても影響がないことを確認しなければなりません。そうでなければ、retry-onに"conn-failure"と"none"以外の値を使うことは非常に危険です。静的ファイルのサーバーとキャッシュは、一般に、どの種類の再試行に対しても安全とみなされます。ステータスコードを使うと、メモリー不足やファイルシステムの問題など、異常な動作をするサーバーを早く離れるために役立つ場合があります。ただし、その場合は、直ちに別のサーバーへ接続を振り分け直すのがよいこともあります（"option redispatch"を参照してください）。最後に、障害の原因の多くはリクエストそのものであり、サーバーの異常を引き起こすリクエストを再試行すると、そのサーバーの状況、あるいは再振り分けの場合はサービス全体の状況を、さらに悪化させることが多い点を理解することが重要です。

再送されたリクエストをアプリケーションがどのように扱うかを正確に把握していない限り、このディレクティブは使用しないことを推奨します。

デフォルトは"conn-failure"です。

例：

```text
retry-on 503 504
```

参照："retries"、"option redispatch"、"tune.bufsize"。

<a id="entry-4-2-server"></a>

**`server <name> <address>[:[port]] [param*]`**

```haproxy
server <name> <address>[:[port]] [param*]
```

バックエンド内のサーバーを宣言します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<name>    このサーバーに割り当てる内部名です。ログとアラートに表示されます。
          "http-send-name-header"を設定している場合、サーバーに送信する
          リクエストヘッダーにも追加されます。この名前はbackendセクション内で
          一意でなければなりません。

<address> サーバーのIPv4またはIPv6アドレスです。代わりに名前解決可能なホスト名も
          使用できますが、この名前は起動時に解決されます。アドレス"0.0.0.0"と
          "*"には特別な意味があり、クライアント接続と同じIPアドレスへ接続を転送する
          ことを示します。クライアントの接続を捕捉し、HAProxyが元の宛先アドレスに
          転送する必要がある透過プロキシ構成で役立ちます。"transparent"キーワードと
          ほぼ同じ動作ですが、サーバーを使用すると同時接続数を制限し、統計を報告できます。
          必要に応じて、アドレスの前にアドレスファミリーのプレフィックスを付け、
          アドレスの形式によらずファミリーを強制できます。スラッシュ（'/'）を
          含まないUNIXソケットのパスを指定する場合などに役立ちます。
          現在サポートするプレフィックスは次のとおりです。
                - 'ipv4@'  -> 常にIPv4アドレスとして扱います。
                - 'ipv6@'  -> 常にIPv6アドレスとして扱います。
                - 'unix@'  -> ローカルUNIXソケットのパスとして扱います。
                - 'abns@'  -> 抽象名前空間のアドレスとして扱います（Linuxのみ）。
                - 'abnsz@'  -> 抽象名前空間のアドレスとして扱います（Linuxのみ）が、
                   明示的にゼロ終端します。つまり、sun_pathを埋めるための\0の
                   パディングは行いません。haproxyがデフォルトで使用するabnsの
                   命名規則を実装していないプログラムとの接続に役立ちます。
                - 'sockpair@' -> 接続済みUNIXソケットまたはsocketpairのFDです。
                  接続時に、バックエンドは接続済みソケットのペアを作成し、その一方を
                  このFD経由で渡します。bind側は、受け取ったソケットをクライアントの
                  FDとして使用します。慎重に使用することを推奨します。
                - 'quic4@' [ 実験的 ] -> IPv4アドレスとして解決し、UDPを使用します。
                  バックエンド側のQUICは、主に実行時のサーバー削除ができなくなるため、
                  実験的とみなされます。使用するにはグローバルキーワード
                  "expose-experimental-directives"が必要です。
                - 'quic6@' [ 実験的 ] -> IPv6アドレスとして解決し、UDPを使用します。
                  同様に実験的とみなされます。
                - 'rhttp@' [ 実験的 ] -> リバースHTTPコンテキストのパッシブサーバー用の
                  カスタムアドレスファミリーです。実験的な機能であり、このserverより
                  前の行に"expose-experimental-directives"を指定する必要があります。
          アドレスパラメーターで環境変数を参照することもできます。環境変数については
          セクション2.3を参照してください。"init-addr"設定で、起動時のIPアドレスの
          解決方法を変更できます。

<port>    省略可能なポート指定です。設定すると、すべての接続をこのポートに送ります。
          設定しない場合、クライアントが接続したポートと同じポートを使用します。
          ポートの前に"+"または"-"を付けることもできます。この場合、その値を
          クライアントのポートに加算して、サーバーのポートを決定します。

<param*>  このサーバーのパラメーターのリストです。"server"キーワードは多数の
          オプションを受け付け、専用のセクションで詳しく説明しています。
          詳細はセクション5を参照してください。
```

例：

```text
server first  10.1.1.1:1080 cookie first  check inter 1000
server second 10.1.1.2:1080 cookie second check inter 1000
server transp ipv4@
server backup "${SRV_BACKUP}:1080" backup
server www1_dc1 "${LAN_DC1}.101:80"
server www1_dc2 "${LAN_DC2}.101:80"
```

注意： Linuxの抽象名前空間ソケットに関して、"abns"HAProxyソケットはsun_pathの全長をアドレス長として使用します。他のプログラム（例: socat）はデフォルトで文字列長のみを使用します。socatの抽象ソケット定義に",unix-tightsocklen=0"オプションを渡すことでHAProxyと互換性を持たせることができます。または、"abnsz"HAProxyソケットファミリを使用してください。

"default-server"、"http-send-name-header"、およびserverオプションに関する[セクション5](/ja/haproxy/bind-and-server-options/)も参照してください。

<a id="entry-4-2-server-state-file-name"></a>

**`server-state-file-name [ { use-backend-name | <file> } ]`**

```haproxy
server-state-file-name [ { use-backend-name | <file> } ]
```

読み込み、ロードし、このバックエンドで使用可能なサーバーに適用するサーバー状態ファイルを設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

これは、"load-server-state-from-file"ディレクティブが"local"に設定されている場合にのみ適用されます。`<file>`が指定されていない場合、"use-backend-name"が使用されている場合、またはこのディレクティブが設定されていない場合は、バックエンド名を使用します。`<file>`がスラッシュ'/'で始まる場合は絶対パスと見なします。それ以外の場合は、globalディレクティブ"server-state-base"に`<file>`を連結します。

例：下記の最小限の設定では、HAProxyはサーバー状態ファイル'/etc/haproxy/states/bk'を探します。

    global
      server-state-file-base /etc/haproxy/states

    backend bk
      load-server-state-from-file

参照："server-state-base"、"load-server-state-from-file"、"show servers state"。

<a id="entry-4-2-server-template"></a>

**`server-template <prefix> <num | range> <fqdn>[:<port>] [params*]`**

```haproxy
server-template <prefix> <num | range> <fqdn>[:<port>] [params*]
```

共通のパラメーターでサーバーを初期化するテンプレートを設定します。サーバーの名前は、`<prefix>`と\<num \| range\>パラメーターから作成します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<prefix>  作成するサーバー名のプレフィックスです。

<num | range>
          <num>を指定すると、このテンプレートは<num>個のサーバーを初期化し、
          サーバー名の接尾辞に1から<num>までを使用します。
          <num_low>-<num_high>の数値範囲を指定して、サーバー名の接尾辞に
          <num_low>から<num_high>までを使用することもできます。

<fqdn>    このテンプレートで初期化するすべてのサーバーのFQDNです。

<port>    "server"の<port>引数と同じ意味です（"server"キーワードを参照）。

<params*>
          "server"キーワードがサポートする、その他のサーバーパラメーターです。
```

例：

```shell
# Initializes 3 servers with srv1, srv2 and srv3 as names,
# google.com as FQDN, and health-check enabled.
server-template srv 1-3 google.com:80 check

# or
server-template srv 3 google.com:80 check

# would be equivalent to:
server srv1 google.com:80 check
server srv2 google.com:80 check
server srv3 google.com:80 check


```

<a id="entry-4-2-source"></a>

**`source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]`**

```haproxy
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | client | clientip } ]
source <addr>[:<port>] [usesrc { <addr2>[:<port2>] | hdr_ip(<hdr>[,<occ>]) } ]
source <addr>[:<port>] [interface <name>]
```

発信接続の送信元アドレスを設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<addr>    HAProxyがサーバーに接続する前にバインドするIPv4アドレスです。
          このアドレスはヘルスチェックの送信元にも使用します。

          デフォルト値0.0.0.0は、宛先に到達するために最適なアドレスをシステムが
          選択することを意味します。必要に応じて、アドレスの前にアドレスファミリーの
          プレフィックスを付け、アドレスの形式によらずファミリーを強制できます。
          スラッシュ（'/'）を含まないUNIXソケットのパスを指定する場合などに役立ちます。
          現在サポートするプレフィックスは次のとおりです。
            - 'ipv4@' -> 常にIPv4アドレスとして扱います。
            - 'ipv6@' -> 常にIPv6アドレスとして扱います。
            - 'unix@' -> ローカルUNIXソケットのパスとして扱います。
            - 'abns@' -> 抽象名前空間のアドレスとして扱います（Linuxのみ）。
            - 'abnsz@'  -> ゼロ終端した抽象名前空間のアドレスとして扱います（Linuxのみ）。

          アドレスパラメーターで環境変数を参照することもできます。
          環境変数についてはセクション2.3を参照してください。

<port>    省略可能なポートです。通常は不要ですが、非常に特殊な状況で役立つ場合が
          あります。デフォルト値のゼロは、システムが空きポートを選択することを
          意味します。バックエンドではポート範囲をサポートしません。
          ポート範囲を強制したい場合は、各"server"行で指定する必要があります。

<addr2>   完全透過プロキシモードで接続を転送する際に、サーバーに提示するIPアドレスです。
          現在、パッチを適用した一部のLinuxカーネルでのみサポートします。このアドレスを
          指定すると、サーバーに接続するクライアントはこのアドレスで提示されますが、
          ヘルスチェックには引き続きアドレス<addr>を使用します。

<port2>   完全透過プロキシモードで接続を転送する際に、サーバーに提示する省略可能な
          ポートです（上の<addr2>を参照）。デフォルト値のゼロは、システムが
          空きポートを選択することを意味します。

<hdr>     バインドするIPアドレスを取得するHTTPヘッダーの名前です。複数のIPアドレスを
          含められる、カンマ区切りのヘッダーリストの名前です。デフォルトでは最後の
          出現箇所を使用します。X-Forwarded-Forヘッダーと組み合わせ、前段のプロキシ
          （通常はStunnel）から見たクライアントのIPアドレスへ自動的にバインドする
          ためのものです。最後以外の出現箇所を使用するには、下記の<occ>パラメーターを
          参照してください。ヘッダー（または出現箇所）が見つからない場合、バインドを
          行わず、プロキシのデフォルトIPアドレスを使用します。また、ほかのHTTPヘッダーと
          同様に、ヘッダー名は大文字と小文字を区別しません。

<occ>     複数の値を持つヘッダーで使用する値の出現番号です。"hdr_ip(<hdr>)"と
          組み合わせ、送信元IPアドレスに使用する出現箇所を指定します。正の値は
          最初から数えた位置を示し、1が最初です。負の値は最後からの相対位置を示し、
          -1が最後です。インフラの入口で設定したX-Forwarded-Forヘッダーを、
          複数のプロキシ層を経た後で使用する必要がある場合に役立ちます。
          指定しない場合、-1とみなします。ゼロを指定すると、この機能を無効にします。

<name>    発信トラフィックをバインドする、省略可能なインターフェース名です。
          この機能をサポートするシステム（現在はLinuxのみ）では、ルーティングテーブルに
          基づいてシステムが選ぶインターフェースでなくても、サーバー宛てのすべての
          トラフィックをこのインターフェースにバインドできます。
          極めて慎重に使用することを推奨します。このオプションにはroot権限が必要です。
```

"source"キーワードは、特定のアドレスからしかサーバーへの接続が許可されない、複雑な環境で役立ちます。たとえば、パブリックゲートウェイを経由する際にプライベートアドレスを使う必要があり、システムが適切な送信元アドレスを自動的に選べないと分かっている場合に必要になることがあります。

一部のパッチを適用したLinuxカーネルで利用できる拡張を、省略可能な"usesrc"キーワードから使用できます。システム自体には属していないIPアドレスで、サーバーへ接続できるようにします。これを"完全透過プロキシモード"と呼びます。動作させるには、接続先のサーバーが、このアドレスへの戻りのトラフィックを、HAProxyを実行するマシン経由でルーティングしなければなりません。また、通常、そのマシンでIP転送を有効にしておく必要があります。

この"完全透過プロキシ"モードでは、サーバーに提示するIPアドレスを、特定のアドレスに固定できます。ただし、実際にはあまり使われません。より一般的なのは、クライアントのIPアドレスを提示するようHAProxyに指示する使い方です。これには、次の二つの方法があります。

    - クライアントのIPアドレスとポートを提示します。最も透過的なモードですが、
      同じ接続が異なる状態で二度観測される可能性があるため、マシンで
      IP接続追跡が有効な場合は問題を起こすことがあります。
      ただし、すべてのクライアントの範囲を使用できるため、
      送信側のアドレスとポートの組み合わせが64kに制限されないという
      大きな利点があります。

    - クライアントのIPアドレスだけを提示し、空きポートを選びます。この方法も適切ですが、透過性は少し下がります（下流のファイアウォールのログが上流のものと一致しません）。同時接続数が通常の64kポートに制限される欠点もあります。ただし、上流と下流でポートが異なるため、同じセッションの再利用によって、マシン内のIP接続追跡が混乱することはありません。

このオプションは、バックエンド内のすべてのサーバーに対する既定の送信元を設定します。"defaults"セクションでも指定できます。サーバーの"source"オプションを使えば、サーバーごとに送信元アドレスをさらに細かく指定できます。詳細は[5節](/ja/haproxy/bind-and-server-options/)を参照してください。

"usesrc"を動作させるには、root権限、または対応システムでは"cap_net_raw"ケーパビリティが必要です。グローバルディレクティブ"setcap"も参照してください。

例：

```text
backend private
    # Connect to the servers using our 192.168.1.200 source address
    source 192.168.1.200

backend transparent_ssl1
    # Connect to the SSL farm from the client's source address
    source 192.168.1.200 usesrc clientip

backend transparent_ssl2
    # Connect to the SSL farm from the client's source address and port
    # not recommended if IP conntrack is present on the local machine.
    source 192.168.1.200 usesrc client

backend transparent_ssl3
    # Connect to the SSL farm from the client's source address. It
    # is more conntrack-friendly.
    source 192.168.1.200 usesrc clientip

backend transparent_smtp
    # Connect to the SMTP farm from the client's source address/port
    # with Tproxy version 4.
    source 0.0.0.0 usesrc clientip

backend transparent_http
    # Connect to the servers using the client's IP as seen by previous
    # proxy.
    source 0.0.0.0 usesrc hdr_ip(x-forwarded-for,-1)
```

関連項目: [5節](/ja/haproxy/bind-and-server-options/)のサーバーオプション"source"、[www.balabit.com](http://www.balabit.com)のLinuxカーネル用Tproxyパッチ、"bind"キーワードを参照してください。

<a id="entry-4-2-srvtcpka-cnt"></a>

**`srvtcpka-cnt <count>`**

```haproxy
srvtcpka-cnt <count>
```

サーバー側で接続を切断するまでに、TCPが送信するkeepaliveプローブの最大数を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<count>   キープアライブプローブの最大数です。
```

このキーワードはソケットオプションTCP_KEEPCNTに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_probes）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option srvtcpka"、"srvtcpka-idle"、"srvtcpka-intvl"。

<a id="entry-4-2-srvtcpka-idle"></a>

**`srvtcpka-idle <timeout>`**

```haproxy
srvtcpka-idle <timeout>
```

サーバー側でTCPキープアライブパケットの送信を有効にしている場合、TCPがプローブの送信を始めるまでに必要な、接続のアイドル時間を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> TCPがキープアライブプローブを送信し始めるまでに必要な、
          接続のアイドル時間です。デフォルトの単位は秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に単位を付ければ
          ほかの単位でも指定できます。
```

このキーワードはソケットオプションTCP_KEEPIDLEに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_time）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option srvtcpka"、"srvtcpka-cnt"、"srvtcpka-intvl"。

<a id="entry-4-2-srvtcpka-intvl"></a>

**`srvtcpka-intvl <timeout>`**

```haproxy
srvtcpka-intvl <timeout>
```

サーバー側の個々のkeepaliveプローブ間の時間を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> 個々のキープアライブプローブの間隔です。
          デフォルトの単位は秒ですが、本ドキュメントの冒頭で
          説明したように、数値の後に単位を付ければ
          ほかの単位でも指定できます。
```

このキーワードはソケットオプションTCP_KEEPINTVLに対応しています。このキーワードが指定されない場合、システム全体のTCPパラメーター（tcp_keepalive_intvl）が使用されます。この設定の利用可能性はオペレーティングシステムに依存します。Linuxで動作することが知られています。

参照："option srvtcpka"、"srvtcpka-cnt"、"srvtcpka-idle"。

<a id="entry-4-2-stats-admin"></a>

**`stats admin { if | unless } <cond>`**

```haproxy
stats admin { if | unless } <cond>
```

if/unlessによる条件の一致または不一致に応じて、統計の管理者レベルを有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

このステートメントは、if/unlessによる条件の一致または不一致に応じて、統計の管理者レベルを有効にします。

adminレベルでは、Webインターフェースからサーバーを有効化・無効化できます。安全上の理由から、統計ページは既定では読み取り専用です。セクションに"stats scope"ディレクティブが設定されている場合は、それらが指定したプロキシだけが状態の変更を受け入れ、それ以外へのアクセスは拒否されます。

現在、POSTリクエストのサイズは、バッファーサイズから予約領域を引いた値に制限されています。そのため、サーバーの一覧が長すぎるとリクエストを処理できません。一度に変更するサーバーを少数にすることを推奨します。

これらの管理用POSTリクエストは、CSRF攻撃を受けやすくなっています。Origin（OriginがなければReferer）がHostヘッダーに一致することを確認して部分的に軽減していますが、攻撃を完全に防ぐには不十分です。完全に防御する方法はありません。公開インターフェースへの露出を避け、アクセスできる利用者を制限することを推奨します。

例：

```shell
# statistics admin level only for localhost
backend stats_localhost
    stats enable
    stats admin if LOCALHOST
```

例：

```shell
# statistics admin level always enabled because of the authentication
backend stats_auth
    stats enable
    stats auth  admin:AdMiN123
    stats admin if TRUE
```

例：

```shell
# statistics admin level depends on the authenticated user
userlist stats-auth
    group admin    users admin
    user  admin    insecure-password 'AdMiN123'
    group readonly users haproxy
    user  haproxy  insecure-password 'haproxy'

backend stats_auth
    stats enable
    acl AUTH       http_auth(stats-auth)
    acl AUTH_ADMIN http_auth_group(stats-auth) admin
    stats http-request auth unless AUTH
    stats admin if AUTH_ADMIN
```

関連項目: "stats enable"、"stats auth"、"stats http-request"、"stats scope"、userlistsについては[12.2節](/ja/haproxy/other-sections/#section-12-2)、ACLの使用については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-ssl-f-use"></a>

**`ssl-f-use [<sslbindconf> ...]*`**

```haproxy
ssl-f-use [<sslbindconf> ...]*
```

現在のフロントエンドに証明書を割り当てます。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<sslbindconf>は、bind行の次のキーワードをサポートします
（セクション5.1「bindオプション」を参照）。

- allow-0rtt
- alpn
- ca-file
- ca-verify-file
- ciphers
- ciphersuites
- client-sigalgs
- crl-file
- curves
- ecdhe
- ktls
- no-alpn
- no-ca-names
- npn
- sigalgs
- ssl-min-ver
- ssl-max-ver
- verify

sslbindconfは、crt-storeのloadキーワードの次のキーワードもサポートします
（セクション12.7.1「loadオプション」を参照）。

- crt
- key
- ocsp
- issuer
- sctl
- ocsp-update
```

フロントエンド名の先頭に@を付けた名前（例：'@frontend1'）で自動作成されるcrt-listに、証明書`<crtname>`を割り当てます。

この暗黙的なcrt-listは、現在のフロントエンドのすべての"ssl" bind行に割り当てられます。

統計ソケットのcrt-listコマンドはこのcrt-listにも作用するため、証明書やSSLオプションを置き換えたり、削除したり、追加したりできます。

例：

```text
frontend https
    bind :443 ssl
    bind quic4@:443 ssl
    ssl-f-use crt foobar.pem.rsa sigalgs "RSA-PSS+SHA256"
    ssl-f-use crt test.foobar.pem
    ssl-f-use crt test2.foobar.crt key test2.foobar.key ocsp test2.foobar.ocsp ocsp-update on
```

参照："crt-list"、"crt"。

<a id="entry-4-2-stats-auth"></a>

**`stats auth <user>:<passwd>`**

```haproxy
stats auth <user>:<passwd>
```

認証付きの統計を有効にし、アカウントにアクセスを許可します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<user>    アクセスを許可するユーザー名です。

<passwd>  このユーザーに対応する平文のパスワードです。
```

この文は、デフォルトの設定で統計を有効にし、宣言したユーザーだけにアクセスを制限します。必要なユーザー数だけ許可するため、何度でも指定できます。有効なアカウントを使わずに統計へアクセスしようとすると、"401 Forbidden"レスポンスを返し、ブラウザーが有効なユーザー名とパスワードの入力を求めるようにします。ブラウザーに返す認証領域は、"stats realm"で設定できます。

認証方式はHTTP Basic認証なので、パスワードはネットワーク上を平文で流れます。このパスワードに機密性の高いものを使うべきではなく、他のアカウントと共用すべきでもないことを利用者に意識してもらうため、設定ファイルでも平文のパスワードを使用する設計にしています。

"stats scope"で、レポートに表示するプロキシの範囲を絞り込むこともできます。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats enable"、"stats realm"、"stats scope"、"stats uri"。

<a id="entry-4-2-stats-enable"></a>

**`stats enable`**

```haproxy
stats enable
```

デフォルト設定で統計の報告を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

この文は、ビルド時に定義したデフォルトの設定で統計の表示を有効にします。特に指定しない限り、次の設定を使います。- stats uri : /haproxy?stats - stats realm: "HAProxy Statistics" - stats auth : 認証なし - stats scope: 制限なし

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats realm"、"stats uri"。

<a id="entry-4-2-stats-hide-version"></a>

**`stats hide-version`**

```haproxy
stats hide-version
```

統計を有効にし、HAProxyのバージョン表示を隠します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

統計ページでは、統計とともに有用な状態情報を表示でき、その中にはHAProxyのバージョンも含まれます。ただし、正確なバージョンを誰にでも知らせると、既知の弱点を狙った攻撃を助ける可能性があるため、一般に危険と考えられます。"stats hide-version"文は、統計レポートからバージョンを除きます。公開サイトや、ログイン名・パスワードが弱いサイトで推奨される設定であり、既定の動作でもあります。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats enable"、"stats realm"、"stats uri"、"stats show-version"。

<a id="entry-4-2-stats-http-request"></a>

**`stats http-request { allow | deny | auth [realm <realm>] }`**

```haproxy
stats http-request { allow | deny | auth [realm <realm>] }
             [ { if | unless } <condition> ]
```

統計のアクセス制御です。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

"http-request"と同様に、これらのオプションを使うと統計へのアクセスを細かく制御できます。各オプションの後にはif/unlessとACLを指定できます。最初に条件が一致したオプション（または条件のないオプション）で評価を終了します。"deny"では403エラーを返し、"allow"では通常の処理を行い、"auth"では401/407エラーコードを返すため、クライアントにはユーザー名とパスワードの入力が求められるはずです。

インスタンスあたりのhttp-requestステートメント数に固定の上限はありません。

"http-request"、ユーザーリストに関する[セクション12.2](/ja/haproxy/other-sections/#section-12-2)、およびACLの使用に関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

<a id="entry-4-2-stats-realm"></a>

**`stats realm <realm>`**

```haproxy
stats realm <realm>
```

統計を有効にし、認証レルムを設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<realm>   ブラウザーに通知するHTTP Basic認証のレルム名です。
          ブラウザーは、有効なユーザー名とパスワードの入力を求める
          ポップアップに、この名前を
          表示します。
```

レルムは単一の単語として読み取るため、含まれる空白は逆スラッシュ（'&#92;'）でエスケープしてください。

この文は認証だけに関係するため、"stats auth"と組み合わせた場合にのみ有用です。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats enable"、"stats uri"。

<a id="entry-4-2-stats-refresh"></a>

**`stats refresh <delay>`**

```haproxy
stats refresh <delay>
```

自動更新付きの統計を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<delay>   レポートページを参照するブラウザーに返す、推奨の更新間隔です。
          秒単位で指定します。ブラウザーは自由に別の間隔を適用できますが、
          通常は指定に従い、この秒数ごとにページを更新します。このドキュメントの
          冒頭で説明したように、値の後ろに単位を付ければ、デフォルト以外の
          時間単位でも更新間隔を指定できます。
```

この文は、ロードバランサーの稼働状況を常時表示する監視画面で役立ちます。設定すると、HTMLレポートのページに"refresh"/"stop refresh"リンクを追加し、ページを自動更新するかどうかを利用者が選べるようにします。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats enable"、"stats realm"、"stats uri"。

<a id="entry-4-2-stats-scope"></a>

**`stats scope { <name> | "." }`**

```haproxy
stats scope { <name> | "." }
```

統計を有効にし、アクセス範囲を制限します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<name>    表示対象のlisten、frontend、backendセクションの名前です。
          特別な名前"."（単一のドット）は、
          この指定が記述されているセクションを表します。
```

この文を指定すると、この文で列挙したセクションだけがレポートに表示されます。それ以外はすべて非表示となり、adminモードで状態を変更しようとしても拒否されます。複数のセクションを表示する必要がある場合は、必要な回数だけこの文を指定できます。名前の確認は単純な文字列比較で行い、指定したセクション名が実際に存在するかどうかは一切確認しません。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats enable"、"stats realm"、"stats uri"、"stats admin"。

<a id="entry-4-2-stats-show-desc"></a>

**`stats show-desc [ <desc> ]`**

```haproxy
stats show-desc [ <desc> ]
```

統計ページでの説明の表示を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

    `<desc>`    表示する説明です。省略可能です。指定しない場合は、
              globalセクションの説明を自動的に使用します。

顧客に共用サービスを提供し、顧客ごとにnodeやdescriptionを変えることが望ましい場合に有用な文です。

この文だけでも統計の表示を有効にできますが、分かりにくい既定のパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。既定では説明を表示しません。

例：

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-desc Master node for Europe, Asia, Africa
    stats uri       /admin?stats
    stats refresh   5s
```

"show-node"、"stats enable"、"stats uri"、globalセクションの"description"も参照してください。

<a id="entry-4-2-stats-show-legends"></a>

**`stats show-legends`**

```haproxy
stats show-legends
```

統計ページでの追加情報の表示を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

統計ページに追加情報を表示します。- cap: 機能（プロキシ）- mode: tcp、http、healthのいずれか（プロキシ）- id: SNMP ID（プロキシ、ソケット、サーバー）- IP（ソケット、サーバー）- cookie（バックエンド、サーバー）

この文だけでも統計の表示を有効にできますが、分かりにくい既定のパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。既定の動作では、この情報を表示しません。

参照："stats enable"、"stats uri"。

<a id="entry-4-2-stats-show-modules"></a>

**`stats show-modules`**

```haproxy
stats show-modules
```

統計ページでの追加統計モジュールの表示を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

行の末尾に新しい列を追加し、追加の統計値をツールチップとして表示します。

この文だけでも統計の表示を有効にできますが、分かりにくい既定のパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。既定の動作では、この情報を表示しません。

参照："stats enable"、"stats uri"。

<a id="entry-4-2-stats-show-node"></a>

**`stats show-node [ <name> ]`**

```haproxy
stats show-node [ <name> ]
```

統計ページでのホスト名の表示を有効にします。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<name>    表示する名前です。省略可能で、未指定の場合は、
          globalセクションのノード名を自動的に使います。
```

この文は、顧客に共有サービスを提供し、顧客ごとの統計ページでノード名や説明を変えたい場合に役立ちます。既定の動作では、ホスト名を表示しません。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats show-node Europe-1
    stats uri       /admin?stats
    stats refresh   5s
```

"show-desc"、"stats enable"、"stats uri"、globalセクションの"node"も参照してください。

<a id="entry-4-2-stats-show-version"></a>

**`stats show-version`**

```haproxy
stats show-version
```

統計を有効にし、HAProxyのバージョンを表示します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：なし

統計ページでは、統計とともに有用な状態情報を表示でき、その中にはHAProxyのバージョンも含まれます。ただし、正確なバージョンを誰にでも知らせると、既知の弱点を狙った攻撃を助ける可能性があり、一般に危険と考えられるため、既定では無効になっています。"stats show-version"は、この情報の表示を有効にします。公開サイトや、ログイン名・パスワードが弱いサイトには推奨しません。

参照："stats auth"、"stats enable"、"stats realm"、"stats uri"、"stats hide-version"。

<a id="entry-4-2-stats-uri"></a>

**`stats uri <prefix>`**

```haproxy
stats uri <prefix>
```

統計を有効にし、アクセス用のURIプレフィックスを定義します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<prefix>  統計ページにリダイレクトするURIの接頭辞です。
          クエリー文字列の一部を表すために、
          疑問符（'?'）を含めることもできます。
```

統計のURIは、中継するトラフィックから取り出して処理するため、通常のアプリケーション内のページのように見えます。選んだURIがアプリケーションに決して現れないことを確認するよう、強く推奨します。そうでなければ、そのURIをアプリケーション内で利用することはできなくなります。

HAProxyに組み込まれる既定のURIは"/haproxy?stats"ですが、ビルド時に変更される可能性があるため、ここで常に明示的に指定するほうがよいでしょう。一般に、途中のプロキシが結果をキャッシュしないよう、URIに疑問符を含めるのがよい方法です。また、この接頭辞で始まる文字列はすべて統計リクエストとして受け入れられるため、疑問符を付けることで、有効なURIが同じ語で始まるのを避けやすくなります。

URIの接頭辞に"/"を使い、その文を専用の"listen"インスタンスに置くと、とても便利な場合があります。これにより、アドレスやポートを統計専用にしやすくなります。

この文だけでも統計の表示を有効にできますが、分かりにくいデフォルトのパラメーターに依存しないよう、ほかの設定もすべて指定することを推奨します。

例：

```shell
# public access (limited to this backend only)
backend public_www
    server srv1 192.168.0.1:80
    stats enable
    stats hide-version
    stats scope   .
    stats uri     /admin?stats
    stats realm   HAProxy\ Statistics
    stats auth    admin1:AdMiN123
    stats auth    admin2:AdMiN321

# internal monitoring access (unlimited)
backend private_monitoring
    stats enable
    stats uri     /admin?stats
    stats refresh 5s
```

参照："stats auth"、"stats enable"、"stats realm"。

<a id="entry-4-2-stick-match"></a>

**`stick match <pattern> [table <table>] [{if | unless} <cond>]`**

```haproxy
stick match <pattern> [table <table>] [{if | unless} <cond>]
```

ユーザーをサーバーに固定する、リクエストパターンの一致条件を定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<pattern>  セクション7.3で説明するサンプル式のルールです。スティックテーブルで
           一致するエントリーを探すために、着信リクエストまたは接続のどの要素を
           解析するかを記述します。このルールは必須です。

<table>    省略可能なスティックテーブル名です。指定しない場合、同じバックエンドの
           テーブルを使用します。スティックテーブルは"stick-table"ステートメントで
           宣言します。

<cond>     省略可能な一致条件です。ほかの条件を満たす場合（または満たさない場合）にのみ、
           特定の基準で照合できます。たとえば、通常は送信元IPアドレスで照合し、
           リクエストが既知のプロキシを経由する場合に限って、そのIPアドレスを含む
           ヘッダーで照合するために使用できます。
```

プロトコルやアプリケーションによっては複雑なスティッキー処理のルールが必要で、Cookieやハッシュに単純に依存できるとは限りません。"stick match"文は、受信したリクエストや接続からスティッキー処理の判定基準を取り出すルールを記述します。使用可能なパターンと変換ルールの完全な一覧は、[7節](/ja/haproxy/acls-and-samples/)を参照してください。

テーブルは、"stick-table"文で宣言しなければならず、パターンと互換性のある型でなければなりません。デフォルトでは、同じバックエンド内のテーブルを使います。"table"キーワードで参照すると、ほかのバックエンドと共有することもできます。別のテーブルを参照する場合、バックエンド内のサーバーIDを使います。デフォルトでは、サーバーIDの付番は各バックエンドで1から始まるため、サーバーの並び順だけで対応できます。ただし、不確かな場合は、サーバーの"id"設定でIDを明示的に指定することを強く推奨します。

"if"または"unless"の後に条件を指定することで、"stick match"文を適用する条件を制限できます。ACLに基づく条件については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

"stick match"文の数に上限はありません。適用されて一致した最初の文により、そのエントリーを作成したリクエストで使ったサーバーと同じサーバーに、リクエストを振り分けます。このように、複数の照合をフォールバックとして使用できます。

stickルールは接続先を固定するCookieの後に確認するため、Cookieによってすでにサーバーを選択している場合、接続先の固定に影響しません。これにより、Cookieを挿入するとともにIPアドレスでも照合し、HTTPとHTTPSの間で同じ接続先を維持することが、とても簡単になります。

例：

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

関連項目: "stick-table"、"stick on"、スティックテーブルについては[11節](/ja/haproxy/stick-tables-and-peers/)、ACLとサンプル取得については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-stick-on"></a>

**`stick on <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick on <pattern> [table <table>] [{if | unless} <condition>]
```

ユーザーをサーバーに関連付けるリクエストパターンを定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

注意： この形式は、同じ引数を指定した"stick match"の後に"stick store-request"を置くことと完全に同じです。詳細は両方のキーワードを参照してください。保守しやすい設定を書くための便宜として提供しているだけです。

例：

```shell
# The following form ...
stick on src table pop if !localhost

# ...is strictly equivalent to this one:
stick match src table pop if !localhost
stick store-request src table pop if !localhost


# Use cookie persistence for HTTP, and stick on source address for HTTPS as
# well as HTTP without cookie. Share the same table between both accesses.
backend http
    mode http
    balance roundrobin
    stick on src table https
    cookie SRV insert indirect nocache
    server s1 192.168.1.1:80 cookie s1
    server s2 192.168.1.1:80 cookie s2

backend https
    mode tcp
    balance roundrobin
    stick-table type ip size 200k expire 30m
    stick on src
    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

"stick match"、"stick store-request"、およびスティックテーブルに関する[セクション11](/ja/haproxy/stick-tables-and-peers/)も参照してください。

<a id="entry-4-2-stick-store-request"></a>

**`stick store-request <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-request <pattern> [table <table>] [{if | unless} <condition>]
```

スティックテーブルにエントリーを作成するためのリクエストパターンを定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<pattern>  セクション7.3で説明するサンプル式のルールです。サーバーが選択された後に、
           着信リクエストまたは接続のどの要素を解析、抽出してテーブルに格納するかを
           記述します。

<table>    省略可能なスティックテーブル名です。指定しない場合、同じバックエンドの
           テーブルを使用します。スティックテーブルは"stick-table"ステートメントで
           宣言します。

<cond>     省略可能な格納条件です。特定の条件を満たす場合（または満たさない場合）にのみ、
           特定の基準を格納できます。たとえば、通常は送信元IPアドレスを格納し、
           リクエストが既知のプロキシを経由する場合に限って、そのIPアドレスを含む
           ヘッダーを変換した形式で格納するために使用できます。
```

プロトコルやアプリケーションによっては、接続先を固定するために複雑なルールが必要で、Cookieやハッシュだけには頼れない場合があります。"stick store-request"文は、リクエストのどの部分をいつ抽出するかを決めるルールを記述します。抽出したものを接続先の固定に使うテーブルへ保存し、後のリクエストで"stick match"文によって照合するためです。当然ながら、抽出する部分には意味があり、後のリクエストで一致する可能性がなければなりません。たとえば、クライアントのIPアドレスを保存することは、多くの場合、適切です。URLパラメーター内のIDを保存することも適切です。送信元ポートを保存しても、偶然一致するだけなので、ほとんど意味がありません。使用できるパターンと変換ルールの全一覧は、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

テーブルは、"stick-table"文で宣言しなければならず、パターンと互換性のある型でなければなりません。デフォルトでは、同じバックエンド内のテーブルを使います。"table"キーワードで参照すると、ほかのバックエンドと共有することもできます。別のテーブルを参照する場合、バックエンド内のサーバーIDを使います。デフォルトでは、サーバーIDの付番は各バックエンドで1から始まるため、サーバーの並び順だけで対応できます。ただし、不確かな場合は、サーバーの"id"設定でIDを明示的に指定することを強く推奨します。

"if"または"unless"の後に条件を指定することで、"stick store-request"文を適用する条件を制限できます。この条件はリクエストの解析中に評価されるため、どの判定基準でも使用できます。ACLに基づく条件については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

"stick store-request"文の数に上限はありませんが、リクエストまたはレスポンスごとに、同時に保存できる数は8に制限されます。ルール数に関係なく、リクエストまたはレスポンスから抽出した判定基準を、最大8個保存できます。一致した最初の8個だけを保持します。これを使うと、別のプロトコルやアクセス方法でも利用者を認識できる可能性を高めるため、複数のテーブルへ同時にデータを追加できます。同じテーブルに複数のstore-requestルールを指定することもでき、優先度の高い順に並べることで、最も適切な判定基準を選べます。各テーブルでは、最初に抽出した判定基準だけを保存します。同じテーブルを参照する後続のstore-requestルールはすべてスキップし、そのACLも評価しません。

"store-request"ルールは、サーバーへの接続が確立した後に評価します。これにより、実際にリクエストを処理したサーバーがテーブルに記録されます。

例：

```shell
# forward SMTP users to the same server they just used for POP in the
# last 30 minutes
backend pop
    mode tcp
    balance roundrobin
    stick store-request src
    stick-table type ip size 200k expire 30m
    server s1 192.168.1.1:110
    server s2 192.168.1.1:110

backend smtp
    mode tcp
    balance roundrobin
    stick match src table pop
    server s1 192.168.1.1:25
    server s2 192.168.1.1:25
```

関連項目: "stick-table"、"stick on"、スティックテーブルについては[11節](/ja/haproxy/stick-tables-and-peers/)、ACLとサンプル取得については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-stick-store-response"></a>

**`stick store-response <pattern> [table <table>] [{if | unless} <condition>]`**

```haproxy
stick store-response <pattern> [table <table>] [{if | unless} <condition>]
```

スティックテーブルにエントリーを作成するためのレスポンスパターンを定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<pattern>  セクション7.3で説明するサンプル式のルールです。サーバーが選択された後に、
           レスポンスまたは接続のどの要素を解析、抽出してテーブルに格納するかを
           記述します。

<table>    省略可能なスティックテーブル名です。指定しない場合、同じバックエンドの
           テーブルを使用します。スティックテーブルは"stick-table"ステートメントで
           宣言します。

<cond>     省略可能な格納条件です。特定の条件を満たす場合（または満たさない場合）にのみ、
           特定の基準を格納できます。たとえば、レスポンスがSSL server helloである
           場合にのみ、SSLセッションIDを格納するために使用できます。
```

プロトコルやアプリケーションによっては、接続先を固定するために複雑なルールが必要で、Cookieやハッシュだけには頼れない場合があります。"stick store-response"文は、レスポンスのどの部分をいつ抽出するかを決めるルールを記述します。抽出したものを接続先の固定に使うテーブルへ保存し、後のリクエストで"stick match"文によって照合するためです。当然ながら、抽出する部分には意味があり、後のリクエストで一致する可能性がなければなりません。レスポンスのヘッダー内で見つかったIDを保存することは適切です。使用できるパターンと変換ルールの全一覧は、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

テーブルは、"stick-table"文で宣言しなければならず、パターンと互換性のある型でなければなりません。デフォルトでは、同じバックエンド内のテーブルを使います。"table"キーワードで参照すると、ほかのバックエンドと共有することもできます。別のテーブルを参照する場合、バックエンド内のサーバーIDを使います。デフォルトでは、サーバーIDの付番は各バックエンドで1から始まるため、サーバーの並び順だけで対応できます。ただし、不確かな場合は、サーバーの"id"設定でIDを明示的に指定することを強く推奨します。

"if"または"unless"の後に条件を指定することで、"stick store-response"文を適用する条件を制限できます。この条件はレスポンスの解析中に評価されるため、どの判定基準でも使用できます。ACLに基づく条件については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

"stick store-response"文の数に上限はありませんが、リクエストまたはレスポンスごとに、同時に保存できる数は8に制限されます。ルール数に関係なく、リクエストまたはレスポンスから抽出した判定基準を、最大8個保存できます。一致した最初の8個だけを保持します。これを使うと、別のプロトコルやアクセス方法でも利用者を認識できる可能性を高めるため、複数のテーブルへ同時にデータを追加できます。同じテーブルに複数のstore-responseルールを指定することもでき、優先度の高い順に並べることで、最も適切な判定基準を選べます。各テーブルでは、最初に抽出した判定基準だけを保存します。同じテーブルを参照する後続のstore-responseルールはすべてスキップし、そのACLも評価しません。ただし、store-requestルールが参照しているテーブルを、store-responseルールでも使用できます。つまり、各テーブルは、リクエストから厳密に一つ、レスポンスから厳密に一つの要素を同時に学習できます。

テーブルには、リクエストを実際に処理したサーバーが格納されます。

例：

```shell
# Learn SSL session ID from both request and response and create affinity.
backend https
    mode tcp
    balance roundrobin
    # maximum SSL session ID length is 32 bytes.
    stick-table type binary len 32 size 30k expire 30m

    acl clienthello req.ssl_hello_type 1
    acl serverhello res.ssl_hello_type 2

    # use tcp content accepts to detects ssl client and server hello.
    tcp-request inspect-delay 5s
    tcp-request content accept if clienthello

    # no timeout on response inspect delay by default.
    tcp-response content accept if serverhello

    # SSL session ID (SSLID) may be present on a client or server hello.
    # Its length is coded on 1 byte at offset 43 and its value starts
    # at offset 44.

    # Match and learn on request if client hello.
    stick on req.payload_lv(43,1) if clienthello

    # Learn on response if server hello.
    stick store-response resp.payload_lv(43,1) if serverhello

    server s1 192.168.1.1:443
    server s2 192.168.1.1:443
```

関連項目: "stick-table"、"stick on"、スティックテーブルについては[11節](/ja/haproxy/stick-tables-and-peers/)、ACLとパターン抽出については[7節](/ja/haproxy/acls-and-samples/)を参照してください。

<a id="entry-4-2-stick-table-type"></a>

**`stick-table type <type> size <size> [expire <expire>] [args...]`**

```haproxy
stick-table type <type> size <size> [expire <expire>] [args...]
```

現在のセクションのスティックテーブルを設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 可

スティックテーブルを宣言して設定するために使用します。詳細とサポートされる引数の一覧は、[11.1節](/ja/haproxy/stick-tables-and-peers/#section-11-1)を参照してください。必須なのは型とサイズだけです。

<a id="entry-4-2-tcp-check-comment"></a>

**`tcp-check comment <string>`**

```haproxy
tcp-check comment <string>
```

後続のtcp-checkルールのコメントを定義します。ルールが失敗した場合にログに記録されます。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<string>  後続のtcp-checkルールが失敗した場合に、
          ログに追加するコメントメッセージです。
```

connect、send、expectルールにのみ使用できます。わかりやすいエラー報告を作成するのに役立ちます。

参照："option tcp-check"、"tcp-check connect"、"tcp-check send"、"tcp-check expect"。

<a id="entry-4-2-tcp-check-connect"></a>

**`tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]`**

```haproxy
tcp-check connect [default] [port <expr>] [addr <ip>] [send-proxy] [via-socks4]
                  [ssl] [sni <sni>] [alpn <alpn>] [linger]
                  [proto <name>] [comment <msg>]
```

新しい接続を開きます。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

default      server行のデフォルトオプションを使用してヘルスチェックを行います。
             サーバーオプションは、再定義されていない場合にのみ使用します。

port <expr>  設定しない場合、チェック用ポートまたはサーバーのポートを使用します。
             HAProxyが接続を開く宛先を指定します。
             <port>は1から65535までの有効なTCPポートの整数値、または
             サンプル取得式でなければなりません。

addr <ip>    ヘルスチェックを行うIPアドレスを定義します。

send-proxy   PROXYプロトコル文字列を送信します。

via-socks4   アップストリームのsocks4プロキシを使用する発信ヘルスチェックを有効にします。

ssl          暗号化された接続を開きます。

sni <sni>    SSL経由のヘルスチェックに使用するSNIを指定します。

alpn <alpn>  ALPNで通知するプロトコルを定義します。プロトコルのリストは
             "http/1.1,http/1.0"（引用符なし）など、プロトコル名のカンマ区切りリストです。
             設定しない場合、サーバーのALPNを使用します。

proto <name> この接続に使用するマルチプレクサーのプロトコルを強制します。
             TCP muxプロトコルであり、バックエンド側で使用可能でなければ
             なりません。利用可能なプロトコルの一覧はhaproxy -vvで表示されます。

linger       単一のRSTを使用せず、接続を正常に閉じます。
```

アプリケーションが複数のTCPポートを使用する場合や、HAProxyが一つのバックエンドで多数のサービスを負荷分散する場合は、サーバーが稼働していると判断する前に、すべてのサービスを個別に確認することが適切です。

server行にもserver portディレクティブにもTCPポートを設定していない場合、'tcp-check connect port `<port>`'をシーケンスの最初の手順にしなければなりません。

tcp-checkルールセットには'connect'が必要で、先頭も'connect'ルールでなければなりません。管理者が操作の内容を理解していることを確実にするためです。

connectでルールセットを開始しなければならない場合でも、その前にset-var、unset-var、commentルールを置くことができます。

例：

```shell
# check HTTP and HTTPs services on a server.
# first open port 80 thanks to server line port directive, then
# tcp-check opens port 443, ciphered and run a request on it:
option tcp-check
tcp-check connect
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
tcp-check connect port 443 ssl
tcp-check send GET\ /\ HTTP/1.0\r\n
tcp-check send Host:\ haproxy.1wt.eu\r\n
tcp-check send \r\n
tcp-check expect rstring (2..|3..)
server www 10.0.0.1 check port 80

# check both POP and IMAP from a single server:
option tcp-check
tcp-check connect port 110 linger
tcp-check expect string +OK\ POP3\ ready
tcp-check connect port 143
tcp-check expect string *\ OK\ IMAP4\ ready
server mail 10.0.0.1 check
```

参照："option tcp-check"、"tcp-check send"、"tcp-check expect"。

<a id="entry-4-2-tcp-check-expect"></a>

**`tcp-check expect [min-recv <int>] [comment <msg>]`**

```haproxy
tcp-check expect [min-recv <int>] [comment <msg>]
                 [ok-status <st>] [error-status <st>] [tout-status <st>]
                 [on-success <fmt>] [on-error <fmt>] [status-code <expr>]
                 [!] <match> <pattern>
```

汎用ヘルスチェック中に収集・解析するデータを指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

min-recv  省略可能で、現在のexpectルールの評価に必要な最小データ量を定義できます。
          受信バイト数がこの下限未満の場合、チェックは追加のデータを待ちます。
          このオプションは、曖昧な一致ルールを解決したり、まだ不完全と分かっている
          内容に対して高コストの正規表現による照合を行わないようにするために
          使用できます。完全一致の文字列（stringまたはbinary）を使用する場合、文字列の長さとこの
          パラメーターのうち、小さい方を使用します。-1を設定すると、この
          パラメーターは無視されます。expectルールに一致しない場合、チェックは
          追加のデータを待ちます。0を設定すると、評価結果は常に確定的になります。

ok-status <st>     省略可能で、expectルールの評価が成功し、かつtcp-checkルールセットの
                   最後のルールである場合に、チェックの状態を設定できます。
                   "L7OK"、"L7OKC"、"L6OK"、"L4OK"をサポートします。
                     - L7OK : レイヤー7のチェックに成功
                     - L7OKC: レイヤー7のチェックに条件付きで成功し、サーバーをNOLB状態に設定
                     - L6OK : レイヤー6のチェックに成功
                     - L4OK : レイヤー4のチェックに成功
                   デフォルトでは"L7OK"を使用します。

error-status <st>  省略可能で、expectルールの評価中にエラーが発生した場合に、
                   チェックの状態を設定できます。"L7OKC"、"L7RSP"、"L7STS"、
                   "L6RSP"、"L4CON"をサポートします。
                     - L7OKC: レイヤー7のチェックに条件付きで成功し、サーバーをNOLB状態に設定
                     - L7RSP: レイヤー7の無効なレスポンス - プロトコルエラー
                     - L7STS: レイヤー7のレスポンスエラー。HTTP 5xxなど
                     - L6RSP: レイヤー6の無効なレスポンス - プロトコルエラー
                     - L4CON: レイヤー1-4の接続の問題
                   デフォルトでは"L7RSP"を使用します。

tout-status <st>   省略可能で、expectルールの評価中にタイムアウトが発生した場合に、
                   チェックの状態を設定できます。"L7TOUT"、"L6TOUT"、"L4TOUT"を
                   サポートします。
                     - L7TOUT: レイヤー7（HTTP/SMTP）のタイムアウト
                     - L6TOUT: レイヤー6（SSL）のタイムアウト
                     - L4TOUT: レイヤー1-4のタイムアウト
                   デフォルトでは"L7TOUT"を使用します。

on-success <fmt>   省略可能で、expectルールの評価が成功し、かつtcp-checkルールセットの
                   最後のルールである場合に、ログに記録する情報メッセージを変更できます。
                   <fmt>はカスタムログ形式です（セクション8.2.6を参照）。

on-error <fmt>     省略可能で、expectルールの評価中にエラーが発生した場合に、
                   ログに記録する情報メッセージを変更できます。<fmt>はカスタムログ形式です（セクション8.2.6を参照）。

status-code <expr> 省略可能で、成功時またはエラー時にログに記録するチェックの
                   ステータスコードを設定できます。<expr>はサンプル取得の後に
                   コンバーターを続けた、標準的なHAProxyの式です。

<match>   レスポンス内で特定のパターンを検索する方法を示すキーワードです。
          "string"、"rstring"、"binary"、"rbinary"のいずれかです。
          キーワードの前に感嘆符（"!"）を付けると、一致を否定できます。
          感嘆符とキーワードの間には空白を入れられます。
          サポートされるキーワードの詳細は後述します。

<pattern> 検索するパターンです。文字列または正規表現を指定できます。
          パターンに空白が含まれる場合、通常のバックスラッシュ（'\'）で
          エスケープする必要があります。照合をbinaryに設定した場合、パターンは
          偶数桁の16進数の並びで渡す必要があります。二桁ごとに一バイトを表します。
          16進数の数字には大文字と小文字のどちらも使用できます。
```

使用可能な一致方法は、意図的に対応するhttp-checkのものと似せてあります。

```text
string <string>: レスポンスバッファー内で文字列の完全一致を調べます。
                  レスポンスバッファーにその文字列がそのまま含まれる場合、ヘルスチェックの
                  レスポンスは有効とみなします。"string"キーワードの前に"!"を付けた場合、
                  本文にその文字列が含まれるとレスポンスは無効とみなします。
                  プロトコルのレスポンス内で必須のパターンを探したり、プロトコルの
                  バナーに特定のエラーが現れたときに、障害を検出するために使用できます。

rstring <regex>: レスポンスバッファーを正規表現で照合します。レスポンスバッファーが
                  式に一致する場合、ヘルスチェックのレスポンスは有効とみなします。
                  "rstring"キーワードの前に"!"を付けた場合、本文が式に一致すると
                  レスポンスは無効とみなします。

string-lf <fmt>: レスポンスバッファーをカスタムログ形式で照合します。
                  セクション8.2.6で説明するカスタムログ形式の規則に従った<fmt>の
                  評価結果の文字列が、レスポンスバッファーに含まれる場合、
                  ヘルスチェックのレスポンスは有効とみなします。前に"!"を付けた場合、
                  バッファーにその文字列が含まれるとレスポンスは無効とみなします。

binary <hexstring>: レスポンスバッファー内で、16進数形式の文字列の完全一致を調べます。
                     レスポンスバッファーにその16進数文字列がそのまま含まれる場合、
                     ヘルスチェックのレスポンスは有効とみなします。
                     バイナリープロトコルのデータの照合が目的です。

rbinary <regex>: "rstring"と同様に、レスポンスバッファーを正規表現で照合します。
                  ただし、NULバイトも含めてレスポンスバッファーを16進数形式に変換します。
                  これにより、あらゆる正規表現エンジンで任意のバイナリー内容を照合できます。
                  16進数への変換後のサイズは、元のレスポンスの二倍になります。
                  そのため、照合するパターンは、レスポンスバッファーのサイズの
                  最大で半分までの範囲で動作するようにすることを推奨します。

binary-lf <hexfmt>: レスポンスバッファーを、16進数形式のカスタムログ形式で照合します。
                     カスタムログ形式の規則（セクション8.2.6を参照）に従った<fmt>の
                     評価結果の16進数文字列が、レスポンスバッファーに含まれる場合、
                     ヘルスチェックのレスポンスは有効とみなします。前に"!"を付けた場合、
                     バッファーにその16進数文字列が含まれるとレスポンスは無効とみなします。
                     レスポンスバッファーとの照合前に、16進数文字列をバイナリー文字列へ
                     変換します。
```

レスポンスのサイズは、globalオプション"tune.bufsize"で定義した値に制限され、デフォルトは16384バイトである点に注意してください。そのため、レスポンスが大きすぎると、"string"、"rstring"、またはバイナリーを使う場合に、必須のパターンが含まれない可能性があります。大きなレスポンスがどうしても必要な場合は、global変数を設定して、デフォルトの最大サイズを変更できます。ただし、非常に大きなレスポンスの解析は、特に正規表現を使う場合にCPUサイクルを浪費する可能性があり、常に小さなリソースを対象にチェックするほうがよい点を忘れないでください。また、現在のチェックでは、レスポンス内のヌル文字より後にある文字列や正規表現の一致を見つけることはできません。同様に、ヌル文字との照合を要求することもできません。

例：

```shell
# perform a POP check
option tcp-check
tcp-check expect string +OK\ POP3\ ready

# perform an IMAP check
option tcp-check
tcp-check expect string *\ OK\ IMAP4\ ready

# look for the redis master server
option tcp-check
tcp-check send PING\r\n
tcp-check expect string +PONG
tcp-check send info\ replication\r\n
tcp-check expect string role:master
tcp-check send QUIT\r\n
tcp-check expect string +OK

```

"option tcp-check"、"tcp-check connect"、"tcp-check send"、"tcp-check send-binary"、"http-check expect"、tune.bufsizeも参照してください。

<a id="entry-4-2-tcp-check-send"></a>

**`tcp-check send <data> [comment <msg>]`**

```haproxy
tcp-check send <data> [comment <msg>]
tcp-check send-lf <fmt> [comment <msg>]
```

汎用ヘルスチェック中に問い合わせとして送信する文字列、またはカスタムログ形式を指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

<data>         汎用ヘルスチェックセッションで送信する文字列です。

<fmt>          評価後に汎用ヘルスチェックセッションで送信するカスタムログ形式です
               （セクション8.2.6を参照）。
```

例：

```shell
# look for the redis master server
option tcp-check
tcp-check send info\ replication\r\n
tcp-check expect string role:master
```

"option tcp-check"、"tcp-check connect"、"tcp-check expect"、"tcp-check send-binary"、tune.bufsizeも参照してください。

<a id="entry-4-2-tcp-check-send-binary"></a>

**`tcp-check send-binary <hexstring> [comment <msg>]`**

```haproxy
tcp-check send-binary <hexstring> [comment <msg>]
tcp-check send-binary-lf <hexfmt> [comment <msg>]
```

生のTCPヘルスチェックでバイナリの問い合わせとして送信する、16進数字の文字列または16進数字のカスタムログ形式を指定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
comment <msg>  ルールの評価が失敗した場合に報告するメッセージを定義します。

<hexstring>    バイナリーに変換した後、汎用ヘルスチェックセッションで送信する
               16進数の文字列です。

<hexfmt>       評価してバイナリーに変換した後、汎用ヘルスチェックセッションで
               送信する16進数のカスタムログ形式です（セクション8.2.6を参照）。
```

例：

```shell
# redis check in binary
option tcp-check
tcp-check send-binary 50494e470d0a # PING\r\n
tcp-check expect binary 2b504F4e47 # +PONG

```

"option tcp-check"、"tcp-check connect"、"tcp-check expect"、"tcp-check send"、tune.bufsizeも参照してください。

<a id="entry-4-2-tcp-check-set-var"></a>

**`tcp-check set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
tcp-check set-var(<var-name>[,<cond>...]) <expr>
tcp-check set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

この操作は変数の内容を設定します。変数はインラインで宣言されます。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<var-name>   変数の名前です。使用できるスコープは"proc"、"sess"、"check"のみです。
             詳細は、変数について説明するセクション2.8を参照してください。

 <cond>      変数を実際に設定するために、すべて真でなければならない条件の集合です
             （"ifnotempty"、"ifgt"など）。指定可能な条件の完全な一覧は、
             set-varコンバーターの説明を参照してください。

 <expr>      サンプル取得式です。後ろにコンバーターを続けることもできます。

 <fmt>       カスタムログ形式の規則で表した値です（セクション8.2.6のカスタムログ形式を参照）。
```

例：

```text
tcp-check set-var(check.port) int(1234)
tcp-check set-var-fmt(check.name) "%H"

```

<a id="entry-4-2-tcp-check-unset-var"></a>

**`tcp-check unset-var(<var-name>)`**

```haproxy
tcp-check unset-var(<var-name>)
```

変数のスコープ内でその変数への参照を解放します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<var-name>   変数名です。使用できるスコープは"proc"、"sess"、"check"
             のみです。変数の詳細はセクション2.8を参照してください。
```

例：

```text
tcp-check unset-var(check.port)

```

<a id="entry-4-2-tcp-request-connection"></a>

**`tcp-request connection <action> <options...> [ { if | unless } <condition> ]`**

```haproxy
tcp-request connection <action> <options...> [ { if | unless } <condition> ]
```

レイヤー4の条件に応じて、着信接続に対してアクションを実行します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 不可

引数：

```text
<action>    条件に一致した場合に実行するアクションを定義します。
            以下を参照してください。

<condition> レイヤー4専用の標準的なACLベースの条件です（セクション7参照）。
```

新しい受信接続を受け入れた直後に、条件を評価して、接続を受け入れるか、破棄するか、カウンターを追跡するかを決められます。まだ接続から何も読み取っておらず、バッファーも割り当てていないため、これらの条件にはデータの内容を使えません。非常に小さなオーバーヘッドで、さまざまな送信元からの接続を選別し、極めて速く受け入れたり破棄したりするために使用します。判断のために内容を検査する必要がある場合は、代わりに"tcp-request content"文を使用しなければなりません。

"tcp-request connection"ルールは、宣言されたとおりの順序で評価されます。一致するルールがない場合、またはルール自体がない場合、既定のアクションは受信接続を受け入れることです。追加できるルール数に特別な上限はありません。どのルールにも、省略可能なACLに基づく条件を後置できます。その場合は、条件が真と評価されたときだけルールを評価します。

条件はアクションを実行する直前に評価し、アクションは厳密に一度だけ実行します。そのため、条件の一部として確認する要素をアクションが変更しても、問題はありません。また、複数のアクションが同じ条件に依存する場合、条件の評価結果を変える最初のアクションだけで、残りのアクションを暗黙に無効にできます。たとえば、変数が空の場合に、さまざまな取得元から値を割り当てようとする際に使用します。

構文中で"tcp-request connection"の直後にあるキーワードがルールのアクションで、その後にアクションに応じた数の引数が続く場合があります。サポートされるアクションと、それぞれの構文は、[4.3節](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙されています（"TCP RqCon"にチェックが付いたアクションを参照してください）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

"if/unless"条件は省略可能です。アクションに条件が設定されていなければ、無条件に実行します。これは"track-sc\*"アクションや、既定のアクションを拒否に変更する場合などに便利です。

例: 許可リスト内のホストからの接続をすべて受け入れ、頻度が高すぎる接続は数えずに拒否し、受け入れた接続を追跡します。その結果、不正利用を行う送信元からの接続レートに上限が設けられます。

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection reject if { src_conn_rate gt 10 }
        tcp-request connection track-sc0 src

例: 許可リスト内のホストからの接続をすべて受け入れ、それ以外の接続を数え、頻度が高すぎるものを拒否します。その結果、不正利用に当たる接続は、頻度を下げない限りブロックされます。

        tcp-request connection accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request connection track-sc0 src
        tcp-request connection reject if { sc0_conn_rate gt 10 }

例：既知のすべてのプロキシからのトラフィックで、PROXYプロトコルを有効にします。

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }

ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

参照："tcp-request session"、"tcp-request content"、"stick-table"。

<a id="entry-4-2-tcp-request-content"></a>

**`tcp-request content <action> [{if | unless} <condition>]`**

```haproxy
tcp-request content <action> [{if | unless} <condition>]
```

レイヤー4-7の条件に応じて、新しいセッションに対してアクションを実行します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

引数：

```text
<action>    条件に一致した場合に実行するアクションを定義します。
            以下を参照してください。

<condition> レイヤー4-7の標準的なACLベースの条件です（セクション7参照）。
```

リクエストの内容は、リクエスト処理の初期段階である"TCP content inspection"（TCPコンテンツ検査）で解析できます。この段階では、リクエストの内容が更新されるたびにACLベースのルールを評価し、"accept"、"reject"、"switch-mode"のいずれかのルールが一致するか、どのルールにも一致せずにTCPリクエストの検査待機時間が満了するまで続けます。

これらのルールと"tcp-request connection"ルールの最初の違いは、"tcp-request content"ルールでは、内容を使って判断できることです。多くの場合、プロトコルの識別や妥当性を判断します。二つ目は、内容に基づくルールをフロントエンドとバックエンドの両方で使用できることです。クライアントとHTTPキープアライブを使う場合、すべてのtcp-request contentルールを再び評価します。そのため、HAProxyは、スティッキーカウンターを"tcp-request connection"と"tcp-request content"のどちらのルールで割り当てたかを記録し、HTTPリクエストの処理後に、内容に関係するものをすべてクリアします。これにより、次のリクエストで再びルールを評価するときに、カウンターも再評価できます。ルールがL7の情報を追跡する場合や、L7に基づくACLを条件としている場合は、リクエストごとに追跡対象が変わる可能性があるため、特に重要です。

コンテンツに基づくルールは、宣言されたとおりの順序で評価されます。一致するルールがない場合、またはルール自体がない場合、既定のアクションは内容を受け入れることです。追加できるルール数に特別な上限はありません。

必須ではありませんが、"tcp-request connection"ルールではtrack-sc0、フロントエンドの"tcp-request content"ルールではtrack-sc1、バックエンドの"tcp-request content"ルールではtrack-sc2を使うことを推奨します。設定が読みやすくなり、トラブルシューティングも容易になるためです。ただし、これはあくまで指針であり、どのカウンターもどこででも使用できます。

構文中で"tcp-request content"の直後にあるキーワードがルールのアクションで、その後にアクションに応じた数の引数が続く場合があります。サポートされるアクションと、それぞれの構文は、[4.3節](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙されています（"TCP RqCnt"にチェックが付いたアクションを参照してください）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

"if/unless"条件は省略可能です。アクションに条件が設定されていなければ、無条件に実行します。これは"track-sc\*"アクションや、既定のアクションを拒否に変更する場合などに便利です。

レイヤー7の内容に*依存しない*情報を追跡するには、特にHTTPフロントエンドで、"tcp-request session"ルールを使うことを推奨します。一部のHTTP処理はセッションレベルで行われ、リクエストが早い段階で拒否される場合があります。その場合、コンテンツレベルでの追跡に支障が出る可能性があります。このような信頼性に欠ける使い方をできる限り防ぐため、起動時に警告を出します。

HTTP固有のACLマッチは、必要なデータを抽出する前にバッファーの内容を事前に解析できるため、TCPプロキシでも"tcp-request content"ルールでレイヤー7の内容を照合できます。バッファー内の内容を有効なHTTPメッセージとして解析できない場合、ACLは一致しません。ここで使用するパーサーは、ほかのすべてのHTTP処理で使用するものとまったく同じなので、解析結果が異なる危険はありません。HTTPフロントエンドまたはHTTPバックエンドでは、接続処理の初期段階で、セッションレベルでHTTPを解析するため、ルールの初回評価時にはHTTPの内容が必ずすぐに利用できます。ただし、このようなプロキシでは"http-request"ルールを使用する方がはるかに自然であり、推奨されます。

ルールの処理時に情報が存在すれば、レイヤー7の情報を追跡することもできます。追跡するデータがまだ利用できない場合、ルール処理エンジンは検査待機時間が満了するまで待つことができます。

例：

```text
tcp-request content use-service lua.deny if { src -f /etc/haproxy/blacklist.lst }
```

例：

```text
tcp-request content set-var(sess.my_var) src
tcp-request content set-var-fmt(sess.from) %[src]:%[src_port]
tcp-request content unset-var(sess.my_var2)
```

例：

```shell
# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (Only works for HTTP/1 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 30s
tcp-request content accept if is_host_com
tcp-request content reject

# Accept HTTP requests containing a Host header saying "example.com"
# and reject everything else. (works for HTTP/1 and HTTP/2 connections)
acl is_host_com hdr(Host) -i example.com
tcp-request inspect-delay 5s
tcp-request content switch-mode http if HTTP
tcp-request content reject   # non-HTTP traffic is implicit here
...
http-request reject unless is_host_com
```

例：

```shell
# reject SMTP connection if client speaks first
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content reject if content_present

# Forward HTTPS connection only if client speaks
tcp-request inspect-delay 30s
acl content_present req.len gt 0
tcp-request content accept if content_present
tcp-request content reject
```

例：

```shell
# Track the last IP(stick-table type string) from X-Forwarded-For
tcp-request inspect-delay 10s
tcp-request content track-sc0 hdr(x-forwarded-for,-1)
# Or track the last IP(stick-table type ip|ipv6) from X-Forwarded-For
tcp-request content track-sc0 req.hdr_ip(x-forwarded-for,-1)
```

例：

```shell
# track request counts per "base" (concatenation of Host+URL)
tcp-request inspect-delay 10s
tcp-request content track-sc0 base table req-rate
```

例：フロントエンドごと、バックエンドごとにカウンターを追跡し、バックエンドが不正利用を検出してgpc0を設定した場合に、その利用者をフロントエンドでブロックします。

        frontend http
            # Use General Purpose Counter 0 in SC0 as a global abuse counter
            # protecting all our sites
            stick-table type ip size 1m expire 5m store gpc0
            tcp-request connection track-sc0 src
            tcp-request connection reject if { sc0_get_gpc0 gt 0 }
            ...
            use_backend http_dynamic if { path_end .php }

        backend http_dynamic
            # if a source makes too fast requests to this dynamic site (tracked
            # by SC1), block it globally in the frontend.
            stick-table type ip size 1m expire 5m store http_req_rate(10s)
            acl click_too_fast sc1_http_req_rate gt 10
            acl mark_as_abuser sc0_inc_gpc0(http) gt 0
            tcp-request content track-sc1 src
            tcp-request content reject if click_too_fast mark_as_abuser

ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

"tcp-request connection"、"tcp-request session"、"tcp-request inspect-delay"、"http-request"も参照してください。

<a id="entry-4-2-tcp-request-inspect-delay"></a>

**`tcp-request inspect-delay <timeout>`**

```haproxy
tcp-request inspect-delay <timeout>
```

コンテンツ検査中にデータを待つ最大許容時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

HAProxyを主にTCPリレーとして使う場合、解析せずにあらゆる種類のプロトコルをサーバーに通す危険性が懸念されることがよくあります。リクエストの内容を解析するには、まずデータの転送を保留し、その後に解析しなければなりません。この文は、指定した時間を上限としてデータの転送を保留できるようにするだけです。

TCPの内容検査は、接続がフロントエンドに到達した直後のごく早い段階に適用され、次に接続がバックエンドへ転送された直後のごく早い段階にも適用されます。そのため、両方にtcp-requestルールがある場合、接続にはフロントエンドで最初の待機時間が発生し、バックエンドで2回目の待機時間が発生する可能性があります。

内容検査では、HAProxyは新しいチャンクが到着するたびに、データが部分的であることを考慮してすべてのルールを評価します。前述の待機時間内にどのルールも一致しない場合、待機時間の終了時に最後の検査を行い、このときは内容が確定したものとして扱います。待機時間を設定しない場合、HAProxyはまったく待機せず、利用できる情報に基づいて直ちに判定を適用します。当然ながら、これではあまり役に立たない可能性が高く、競合が生じる可能性もあるため、このような設定は推奨しません。

接続エラーまたはシャットダウンが発生した場合や、リクエストバッファーがいっぱいになった場合は、検査の待機時間が短くなります。

ルールが一致するとすぐにリクエストを解放し、通常どおり処理を続けます。どのルールにも一致せずにタイムアウトに達した場合、既定の方針では、そのまま通過させます。

ほとんどのプロトコルでは、クライアントの大半が接続直後にリクエスト全体を送信するため、数秒の設定で十分です。TCPの再送に備えて3秒以上を加えれば、それ以上は必要ありません。一部のプロトコルでは、たとえばクライアントがサーバーより先に送信しないことを保証する場合（SMTPなど）や、サーバーへデータを渡す前にクライアントからの送信を待つ場合（SSLなど）に、大きな値を使用する意味がある場合があります。クライアントのタイムアウトは、少なくとも検査の待機時間をカバーしなければなりません。そうでなければ、先にタイムアウトします。クライアントが接続を閉じた場合やバッファーがいっぱいになった場合、内容がそれ以上変わることはないため、待機時間は直ちに終了します。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のdefaultsセクションでは使用できません。プロキシは、自身のdefaultsセクションからこの値を継承します。

参照："tcp-request content accept"、"tcp-request content reject"、"timeout client"。

<a id="entry-4-2-tcp-request-session"></a>

**`tcp-request session <action> [{if | unless} <condition>]`**

```haproxy
tcp-request session <action> [{if | unless} <condition>]
```

レイヤー5の条件に応じて、検証済みのセッションに対してアクションを実行します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 可 \| 可 \| 不可

引数：

```text
<action>    条件に一致した場合に実行するアクションを定義します。
            以下を参照してください。

<condition> レイヤー5専用の標準的なACLベースの条件です（セクション7参照）。
```

セッションが検証された後（つまり、すべてのハンドシェイクが完了した後）に、条件を評価して、そのセッションを受け入れるか、破棄するか、カウンターを追跡するかを判断できます。この段階ではまだバッファーが割り当てられておらず、処理を待機させることもできないため、条件にはデータの内容を使用できません。主な用途は、初期段階の情報を変数へコピーすること（セッション内では変数にアクセスできるため）や、ハンドシェイク後に収集した情報を追跡することです。後者には、SSLレベルの要素（SNI、暗号、クライアント証明書のCN）やPROXYプロトコルヘッダーの情報（たとえば、この方法で転送された送信元の追跡）があります。抽出した情報は、変数へコピーすることも、"track-sc"ルールで追跡することもできます。もちろん、ほかのルールセットと同じように、受け入れるか拒否するかを判断することもできます。ここで行う操作のほとんどは"tcp-request content"ルールでも実行できますが、HTTPではこれらのルールが新しいリクエストごとに評価されるため、それが常に許容できるとは限りません。たとえば、ルールが評価のたびにカウンターを増やす場合があります。また、送信元IPアドレスから位置情報で国を特定し、セッション全体で使用する変数へ代入した後、すべてのリクエストでHTTPヘッダーから送信元アドレスを書き換えることもできます。判断するために内容を検査する必要がある場合は、代わりに"tcp-request content"文を使用しなければなりません。

"tcp-request session"ルールは、宣言されたとおりの順序で評価されます。一致するルールがない場合、またはルール自体がない場合、既定のアクションは受信セッションを受け入れることです。追加できるルール数に特別な上限はありません。

構文中で"tcp-request session"の直後にあるキーワードがルールのアクションで、その後にアクションに応じた数の引数が続く場合があります。サポートされるアクションと、それぞれの構文は、[4.3節](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙されています（"TCP RqSes"にチェックが付いたアクションを参照してください）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

"if/unless"条件は省略可能です。アクションに条件が設定されていなければ、無条件に実行します。これは"track-sc\*"アクションや、既定のアクションを拒否に変更する場合などに便利です。

例: 既定では元の送信元アドレスを追跡し、ローカルプロキシからの接続については、PROXYプロトコルのヘッダーで通知されたアドレスを追跡します。最初の接続レベルのルールは、これらの接続に対してPROXYプロトコルの受信を有効にします。二番目のルールは、必要に応じてデコードした後に、保持すると決めたアドレスを追跡します。

        tcp-request connection expect-proxy layer4 if { src -f proxies.lst }
        tcp-request session track-sc0 src

例: 許可リスト内のホストからのセッションをすべて受け入れ、頻度が高すぎるセッションは数えずに拒否し、受け入れたセッションを追跡します。その結果、不正利用を行う送信元からのセッションレートに上限が設けられます。

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session reject if { src_sess_rate gt 10 }
        tcp-request session track-sc0 src

例: 許可リスト内のホストからのセッションをすべて受け入れ、それ以外のセッションを数え、頻度が高すぎるものを拒否します。その結果、不正利用に当たるセッションは、頻度を下げない限りブロックされます。

        tcp-request session accept if { src -f /etc/haproxy/whitelist.lst }
        tcp-request session track-sc0 src
        tcp-request session reject if { sc0_sess_rate gt 10 }

ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

参照："tcp-request connection"、"tcp-request content"、"stick-table"。

<a id="entry-4-2-tcp-response-content"></a>

**`tcp-response content <action> [{if | unless} <condition>]`**

```haproxy
tcp-response content <action> [{if | unless} <condition>]
```

レイヤー4-7の条件に応じて、セッションのレスポンスに対してアクションを実行します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 不可 \| 可 \| 可

引数：

```text
<action>    条件に一致した場合に実行するアクションを定義します。
            以下を参照してください。

<condition> レイヤー4-7の標準的なACLベースの条件です（セクション7参照）。
```

レスポンスの内容は、レスポンス処理の初期段階である"TCPコンテンツ検査"で解析できます。この段階では、レスポンスの内容が更新されるたびにACLに基づくルールを評価します。評価は、終端となるルールが一致するか、設定されているTCPレスポンスの検査待機時間が、どのルールにも一致せずに満了するまで続きます。

通常、これらの判断ではプロトコルの識別や妥当性を考慮します。

コンテンツに基づくルールは、宣言されたとおりの順序で評価されます。一致するルールがない場合、またはルール自体がない場合、既定のアクションは内容を受け入れることです。追加できるルール数に特別な上限はありません。

構文中で"tcp-response content"の直後にあるキーワードがルールのアクションで、その後にアクションに応じた数の引数が続く場合があります。サポートされるアクションと、それぞれの構文は、[4.3節](/ja/haproxy/proxies/#section-4-3)「アクション」に列挙されています（"TCP RsCnt"にチェックが付いたアクションを参照してください）。

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のセクションでは使用できません。defaultsセクションで定義したルールは、関連付けられたプロキシセクションのルールより先に評価されます。曖昧さを避けるため、この場合、フロントエンド機能を持つプロキシとバックエンド機能を持つプロキシが、同じdefaultsセクションを使用することはできません。つまり、listenセクションは、このようなルールを定義したdefaultsセクションを使用できません。

"if/unless"条件は省略可能です。アクションに条件が設定されていなければ、無条件に実行します。これは、既定のアクションを拒否に変更する場合などに便利です。

複数の種類のアクションをサポートしています。

"tcp-response content"ルールでレイヤー7の内容を照合することもできますが、その場合は完全なレスポンスがバッファーに格納されていることを確認する必要があります。そうでなければ、どの内容にも一致しません。これを実現する最もよい方法は、検査期間中にHTTPプロトコルを検出することです。

ACLの使用方法については、[セクション7](/ja/haproxy/acls-and-samples/)を参照してください。

参照："tcp-request content"、"tcp-response inspect-delay"。

<a id="entry-4-2-tcp-response-inspect-delay"></a>

**`tcp-response inspect-delay <timeout>`**

```haproxy
tcp-response inspect-delay <timeout>
```

コンテンツ検査中にレスポンスを待つ最大許容時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可(!) \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

このディレクティブは、名前付きのdefaultsセクションでのみ使用でき、無名のdefaultsセクションでは使用できません。プロキシは、自身のdefaultsセクションからこの値を継承します。

参照："tcp-response content"、"tcp-request inspect-delay"。

<a id="entry-4-2-timeout-check"></a>

**`timeout check <timeout>`**

```haproxy
timeout check <timeout>
```

追加のチェックタイムアウトを設定します。ただし、接続がすでに確立された後にのみ適用されます。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

設定すると、HAProxyはチェックの接続タイムアウトとしてmin("timeout connect", "inter")を使用し、追加の読み取りタイムアウトとして"timeout check"を使用します。"min"を使用するのは、*非常に*長い"timeout connect"を設定している場合（たとえば、キューやtarpitのために必要だった場合）に、チェックが遅くならないようにするためです。（"timeout queue"と"timeout tarpit"を使用すれば常に回避できるため、これほど長い接続タイムアウトを設定する妥当な理由はないことにも注意してください。）

"timeout check"が設定されていない場合、HAProxyはチェック全体（接続+読み取り）のタイムアウトに"inter"を使用します。これは\<1.3.15のすべてのバージョンとまったく同じ動作です。

ほとんどの場合、チェック用のリクエストは通常のリクエストよりはるかに単純で、短時間で処理できます。また、応答の遅いサーバーを除外したい場合もあるため、このタイムアウトは"timeout server"より小さくするべきです。

このパラメーターはバックエンド専用ですが、"defaults"セクションで一度指定して、すべてに適用できます。実際、これは設定を忘れないための最も簡単な方法の1つです。

参照："timeout connect"、"timeout queue"、"timeout server"、"timeout tarpit"。

<a id="entry-4-2-timeout-client"></a>

**`timeout client <timeout>`**

```haproxy
timeout client <timeout>
```

クライアント側の最大無通信時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

非アクティブ時のタイムアウトは、クライアントからの確認応答またはデータ送信を待っている場合に適用されます。HTTPモードでは、クライアントがリクエストを送信する最初の段階と、レスポンスでサーバーが送信したデータを読み取っている間に、このタイムアウトを特に考慮することが重要です。ただし、最初の段階については、Slowlorisのような攻撃からHAProxyをよりよく保護するために、"timeout http-request"を設定する方が望ましいです。値の単位はデフォルトではミリ秒ですが、このドキュメントの冒頭で説明したように、数値の後ろに単位を付ければほかの単位も使用できます。TCPモードでは（HTTPモードでも程度は小さいものの）、デバッグが複雑になる状況を避けるため、クライアントのタイムアウトをサーバーのタイムアウトと同じ値にすることを強く推奨します。1つまたは複数のTCPパケットの損失に対応できるよう、3秒の倍数を少し上回るタイムアウト（4秒や5秒など）を指定するのがよい方法です。長時間続くストリームと短時間のストリームが混在する場合（WebSocketとHTTPなど）、トンネルでは"timeout client"と"timeout server"より優先される"timeout tunnel"と、半分閉じた接続用の"timeout client-fin"の利用を検討する価値があります。

このパラメーターはフロントエンド専用ですが、"defaults"セクションで一度指定すれば、すべてに適用できます。実際、設定し忘れを防ぐ最も簡単な方法の一つです。タイムアウトを指定しないと無期限になり、推奨されません。この使い方も受け入れられ、動作しますが、システム側のタイムアウトも設定されていない場合、期限切れのセッションがシステム内に蓄積するおそれがあるため、起動時に警告を出します。

参照："timeout server"、"timeout tunnel"、"timeout http-request"。

<a id="entry-4-2-timeout-client-fin"></a>

**`timeout client-fin <timeout>`**

```haproxy
timeout client-fin <timeout>
```

半クローズ状態の接続の、クライアント側の無通信タイムアウトを設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

非アクティブ時のタイムアウトは、すでに一方向が閉じられており、クライアントからの確認応答またはデータ送信を待っている場合に適用されます。このタイムアウトは、一方向が閉じられた接続だけに適用される点で"timeout client"と異なります。クライアントが正常に切断しない場合に、接続がFIN_WAIT状態のまま長く残るのを防ぐうえで特に役立ちます。この問題は、RDPやWebSocketのような長時間続く接続で特によく発生します。接続の一方向が閉じられると、このタイムアウトが"timeout tunnel"より優先される場合があることに注意してください。GOAWAYフレームを送信した後のアイドル状態のHTTP/2接続にも適用されます。これは多くの場合、接続が速やかに終了することを期待していることを示します。

このパラメーターはフロントエンド専用ですが、"defaults"セクションで一度指定すれば、すべてに適用できます。既定では未設定のため、片方向だけ閉じた接続にはほかのタイムアウト（timeout.clientまたはtimeout.tunnel）を使用します。

参照："timeout client"、"timeout server-fin"、"timeout tunnel"。

<a id="entry-4-2-timeout-client-hs"></a>

**`timeout client-hs <timeout>`**

```haproxy
timeout client-hs <timeout>
```

クライアントのTLSハンドシェイクが完了するまで待つ最大時間を設定します。TCP接続とQUIC接続の両方で使用できます。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

このハンドシェイクタイムアウトを設定しない場合、代わりにクライアントタイムアウトを使用します。

<a id="entry-4-2-timeout-connect"></a>

**`timeout connect <timeout>`**

```haproxy
timeout connect <timeout>
```

サーバーへの接続試行が成功するまで待つ最大時間を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

サーバーがHAProxyと同じLANにあれば、接続はすぐに確立するはずです（数ミリ秒未満）。いずれにせよ、一回または複数回のTCPパケット損失に対応できるよう、タイムアウトを3秒の倍数より少し長く設定するのがよい方法です（たとえば4または5秒）。既定では、queueとtarpitのタイムアウトが指定されていない場合、接続タイムアウトはそれらの初期値も同じ値に設定します。

このパラメーターはバックエンド専用ですが、"defaults"セクションで一度指定すれば、すべてに適用できます。実際、設定し忘れを防ぐ最も簡単な方法の一つです。タイムアウトを指定しないと無期限になり、推奨されません。この使い方も受け入れられ、動作しますが、システム側のタイムアウトも設定されていない場合、失敗したセッションがシステム内に蓄積するおそれがあるため、起動時に警告を出します。

参照："timeout check"、"timeout queue"、"timeout server"、"timeout tarpit"。

<a id="entry-4-2-timeout-http-keep-alive"></a>

**`timeout http-keep-alive <timeout>`**

```haproxy
timeout http-keep-alive <timeout>
```

新しいHTTPリクエストの到着を待つ最大許容時間を設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

既定では、キープアライブ中に新しいリクエストを待つ時間は"timeout http-request"で設定します。ただし、これが常に便利とは限りません。接続を早く解放するためにキープアライブのタイムアウトを非常に短くしたい場合もあれば、キープアライブのタイムアウトは長くしつつ、リクエストが届き始めてからのタイムアウトは短く保ちたい場合もあります。

"http-keep-alive"タイムアウトは、これらの要件に対応します。レスポンスの送信後、新しいHTTPリクエストが届き始めるまでの待ち時間を定義します。リクエストの最初のバイトを検出した後は、"http-request"タイムアウトを使ってリクエスト全体の到着を待ちます。新しいリクエストの前にある空行は、タイムアウトを更新せず、新しいリクエストとしても数えません。

この二つのタイムアウトには、もう一つ違いがあります。timeout http-keep-alive中に接続が期限切れになった場合は、エラーを返さず、接続を閉じるだけです。リクエストがそろうのを待っている間に"http-request"で期限切れになった場合は、フロントエンドに"option http-ignore-probes"が設定されていない限り、接続を閉じる前にHTTP 408エラーをクライアントへ返します。

一般に、"timeout http-keep-alive"は、短時間の接続が大量に発生するサイトで、クライアントがそれ以外には何も行わない接続を長く開いたままにするのを防ぐ用途に適しています。HTTP/1.1では、値を数十から数百ミリ秒に設定することで実現できます。これにより、クライアントがページをリクエストした後、クライアントの次の動作を待つために接続を開いたままにせず、接続を閉じます。この場合、ブラウザーが新たに動作すると、TCPレイヤーやSSLレイヤーで新しいハンドシェイクが発生します。よくある用途は、HTTPSページへのリダイレクトだけを提供するHTTPサイトです。このような接続は、faviconの取得に使われる可能性がある場合を除いて再利用されないため、アイドル状態で長く維持しない方がよいでしょう。

逆の用途もあります。クライアントがアイドル接続を長時間（たとえば30秒から一分間）再利用できるようにしたいものの、非常に低コストな攻撃を避けるため、最初のリクエストにはそれほど長く待ちたくないサイトもあります。その場合、http-keep-aliveタイムアウトには大きな値を設定し、http-requestは小さい値（数秒）のままにします。

非常に小さな値を設定すると、パイプライン化されていない追加のリクエストは、別の接続で処理される可能性が高くなります。同じ接続で処理されるには、リクエストが実際にパイプライン化されている必要がありますが、HTTP/1.1ではこれは非常にまれです（レスポンスを待たずにリクエストを続けて送信することを指します）。ほとんどのHTTP/1.1実装は、リクエストを送信し、レスポンスを待ってから次のリクエストを送信します。数十万のクライアントがあるサイトでは、HTTP/1.1用にここで小さな値を設定すると、ハンドシェイクの計算コストが増える代わりに、使用するメモリーとソケットを減らせる利点があります。

HTTP/2を扱う場合、小さな値の設定には特に注意が必要です。HTTP/2は、TCPレイヤーやSSLレイヤーの再接続に伴うオーバーヘッドを減らすため、1つの接続上でリクエストを多重化する仕組みです。このプロトコルは制御フレームも使用し、TCP接続が早期に閉じられるとうまく処理できません。ごくまれに、HAProxyから出た後の転送中のデータが破棄され、レスポンスが途中で切れることがあります（この場合、HAProxyはエラーをログに記録することさえできません）。HTTP/2接続の小さめの初期値としては、4秒程度を推奨します。これにより、最新のkeep-alive実装の大半が、使われなくなった接続を不必要に開いたままにするのを防ぎながら、後続のリクエストではその接続を再利用できます。ただし、必要に応じて調整すべきであり、これはあくまで初期値です。

このパラメーターを設定しない場合、"http-request"タイムアウトが適用されます。両方とも設定しない場合は、さらに下のレベルで"timeout client"が引き続き適用されます。効果を得るにはフロントエンドに設定することを推奨します。ただし、フロントエンドがTCPモードの場合は、HTTPバックエンドのタイムアウトが使用されます。

参照："timeout http-request"、"timeout client"。

<a id="entry-4-2-timeout-http-request"></a>

**`timeout http-request <timeout>`**

```haproxy
timeout http-request <timeout>
```

完全なHTTPリクエストを待つ最大許容時間を設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

DoS対策として、クライアントのタイムアウトには影響を与えずに、HTTPリクエスト全体の受信に許容する最大時間を短くする必要がある場合があります。これにより、接続を確立したまま何も送信しない行為を防ぐことができます。クライアントのタイムアウトは非アクティブ時のタイムアウトであり、攻撃者が時々1文字ずつ送信すればタイムアウトしないため、このような不正利用を十分に防げません。HTTPリクエストのタイムアウトでは、クライアントがどのような速度で入力しても、時間内に完了しないリクエストは中止されます。タイムアウトすると、問題を通知するためHTTP 408レスポンスをクライアントへ送信し、接続を閉じます。ログには終了コード"cR"が記録されます。一部の最近のブラウザーには、この標準的で十分に文書化された動作に問題があるため、"option http-ignore-probes"または"errorfile 408 /dev/null"を使用して408コードを隠す必要がある場合があります。詳細は、[セクション8.5](/ja/haproxy/configuration-logging/#section-8-5)の終了コード"cR"の説明を参照してください。

既定では、このタイムアウトはリクエストのヘッダー部分だけに適用され、データには適用されません。空行を受信すると、それ以降は使用しません。"option http-buffer-request"と組み合わせると、リクエストのボディにも適用されます。"timeout http-keep-alive"が設定されていないキープアライブ接続では、二番目のリクエストを待つ際に再び使用します。

ほとんどのクライアントは接続直後にリクエスト全体を送るため、通常は数秒に設定すれば十分です。TCPの再送を考慮して3秒以上を加えれば、それ以上は必要ありません。非常に小さい値（たとえば50 ms）でも、ローカルネットワークではパケット損失がなければ通常は機能します。ただし、その場合はtelnetを使ってHTTPリクエストを手入力することができなくなります。

このパラメーターを設定しない場合、受信リクエストの各チャンクの間には、引き続きクライアントタイムアウトが適用されます。有効にするにはフロントエンドで設定するべきですが、フロントエンドがTCPモードの場合は、HTTPバックエンドのタイムアウトを使用します。

"errorfile"、"http-ignore-probes"、"timeout http-keep-alive"、"timeout client"、"option http-buffer-request"も参照してください。

<a id="entry-4-2-timeout-queue"></a>

**`timeout queue <timeout>`**

```haproxy
timeout queue <timeout>
```

接続スロットが空くまでキューで待つ最大時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

サーバーのmaxconnに達すると、接続はサーバー専用、またはバックエンド全体で共有するキューで待機します。無期限に待たないよう、キューで待機中のリクエストにはタイムアウトが適用されます。タイムアウトに達すると、そのリクエストが処理される見込みはほぼないと判断して破棄し、クライアントに503エラーを返します。

"timeout queue"文で、リクエストがキュー内で待機できる最大時間を指定できます。指定しない場合、"timeout queue"パラメーターのない旧バージョンとの後方互換性のため、バックエンドの接続タイムアウト（"timeout connect"）と同じ値を使用します。

参照："timeout connect"。

<a id="entry-4-2-timeout-server"></a>

**`timeout server <timeout>`**

```haproxy
timeout server <timeout>
```

サーバー側の最大無通信時間を設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

非アクティブ時のタイムアウトは、サーバーからの確認応答またはデータ送信を待っている場合に適用されます。HTTPモードでは、サーバーがヘッダーを送信する必要のあるレスポンスの最初の段階に、このタイムアウトを特に考慮することが重要です。これは、リクエストに対するサーバーの処理時間を直接表すためです。ここに設定する値を決めるには、多くの場合、まず許容できないと考える応答時間を設定し、ログで応答時間の分布を確認して、それに合わせて値を調整するのがよい方法です。

値の単位はデフォルトではミリ秒ですが、このドキュメントの冒頭で説明したように、数値の後ろに単位を付ければほかの単位も使用できます。TCPモードでは（HTTPモードでも程度は小さいものの）、デバッグが複雑になる状況を避けるため、クライアントのタイムアウトをサーバーのタイムアウトと同じ値にすることを強く推奨します。想定するサーバーの応答時間にかかわらず、少なくとも1つまたは複数のTCPパケットの損失に対応できるよう、3秒の倍数を少し上回るタイムアウト（最低でも4秒や5秒など）を指定するのがよい方法です。長時間続くストリームと短時間のストリームが混在する場合（WebSocketとHTTPなど）、トンネルでは"timeout client"と"timeout server"より優先される"timeout tunnel"の利用を検討する価値があります。

このパラメーターはバックエンド専用ですが、"defaults"セクションで一度指定すれば、すべてに適用できます。実際、設定し忘れを防ぐ最も簡単な方法の一つです。タイムアウトを指定しないと無期限になり、推奨されません。この使い方も受け入れられ、動作しますが、システム側のタイムアウトも設定されていない場合、期限切れのセッションがシステム内に蓄積するおそれがあるため、起動時に警告を出します。

参照："timeout client"、"timeout tunnel"。

<a id="entry-4-2-timeout-server-fin"></a>

**`timeout server-fin <timeout>`**

```haproxy
timeout server-fin <timeout>
```

半クローズ状態の接続の、サーバー側の無通信タイムアウトを設定します。

使用可能なコンテキスト：tcp, http, log

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

非アクティブ時のタイムアウトは、すでに一方向が閉じられており、サーバーからの確認応答またはデータ送信を待っている場合に適用されます。このタイムアウトは、一方向が閉じられた接続だけに適用される点で"timeout server"と異なります。リモートサーバーが正常に切断しない場合に、接続がFIN_WAIT状態のまま長く残るのを防ぐうえで特に役立ちます。この問題は、RDPやWebSocketのような長時間続く接続で特によく発生します。接続の一方向が閉じられると、このタイムアウトが"timeout tunnel"より優先される場合があることに注意してください。この設定は機能を網羅するために用意されていますが、ほとんどの状況では必要ないはずです。

このパラメーターはバックエンド専用ですが、"defaults"セクションで一度指定すれば、すべてに適用できます。既定では未設定のため、片方向だけ閉じた接続にはほかのタイムアウト（timeout.serverまたはtimeout.tunnel）を使用します。

参照："timeout client-fin"、"timeout server"、"timeout tunnel"。

<a id="entry-4-2-timeout-tarpit"></a>

**`timeout tarpit <timeout>`**

```haproxy
timeout tarpit <timeout>
```

tarpitされた接続を維持する時間を設定します。

使用可能なコンテキスト: http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<timeout> tarpitの継続時間です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

"http-request tarpit"で接続にtarpitを適用すると、その接続を一定時間、何も処理せずに開いたまま保持し、その後に閉じます。"timeout tarpit"は、開いたまま保持する時間を定義します。

既定の単位はミリ秒ですが、このドキュメントの冒頭で説明したように、数値の後に単位を付ければ、ほかの単位でも指定できます。省略した場合は、"timeout tarpit"パラメーターがなかった旧バージョンとの後方互換性のため、バックエンドの接続タイムアウト（"timeout connect"）と同じ値を使用します。

参照："timeout connect"。

<a id="entry-4-2-timeout-tunnel"></a>

**`timeout tunnel <timeout>`**

```haproxy
timeout tunnel <timeout>
```

トンネルのクライアント側とサーバー側の最大無通信時間を設定します。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：

```text
<timeout> タイムアウト値です。デフォルトの単位はミリ秒ですが、
          本ドキュメントの冒頭で説明したように、数値の後に
          単位を付ければ、ほかの単位でも
          指定できます。
```

トンネルのタイムアウトは、クライアントとサーバーの間に双方向接続が確立され、その接続が両方向とも非アクティブのままになった場合に適用されます。接続がトンネルになると、このタイムアウトはクライアントとサーバーの両方のタイムアウトより優先されます。TCPでは、どちらの接続にもアナライザーが接続されていなくなった時点で、このタイムアウトを使用します（TCP内容ルールで受け入れられた場合など）。HTTPでは、接続がアップグレードされた場合（WebSocketプロトコルへ切り替える場合や、CONNECTリクエストをプロキシへ転送する場合など）、またはkeepalive/closeオプションを指定していない場合の最初のレスポンスの後に、このタイムアウトを使用します。

このタイムアウトは通常、長時間続く接続と併せて使用するため、"timeout client-fin"も設定するのが一般に適切です。これにより、クライアントが突然ネットワークからいなくなって接続を閉じる処理に確認応答を返さない場合や、シャットダウンを送信した後、未完了のデータに確認応答を返さなくなった場合に対応できます。これは、ファイアウォールのあるパケット損失の多いネットワークで発生することがあり、大量のセッションがFIN_WAIT状態にあることで検出できます。

既定の単位はミリ秒ですが、このドキュメントの冒頭で説明したように、数値の後に単位を付ければ、ほかの単位でも指定できます。通常のアイドル時間としてどれくらいを想定していても、一回または複数回のTCPパケット損失に対応できるよう、タイムアウトを3秒の倍数より少し長く設定するのがよい方法です（たとえば、最低でも4または5秒）。

このパラメーターはバックエンド専用ですが、"defaults"セクションで一度指定して、すべてに適用できます。実際、これは設定を忘れないための最も簡単な方法の1つです。

例：

```text
defaults http
    option http-server-close
    timeout connect 5s
    timeout client 30s
    timeout client-fin 30s
    timeout server 30s
    timeout tunnel  1h    # timeout to use with WebSocket and CONNECT
```

参照："timeout client"、"timeout client-fin"、"timeout server"。

<a id="entry-4-2-transparent"></a>

**`transparent (deprecated)`**

```haproxy
transparent (deprecated)
```

クライアント側の透過プロキシを有効にします。

使用可能なコンテキスト：tcp, http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 不可 \| 可 \| 可

引数：なし

このキーワードは、レイヤー3ロードバランサーにレイヤー7での接続先の固定を提供するために導入されました。リモートアドレスへの着信接続をローカルプロセス（ここではHAProxy）にリダイレクトするOSの機能を使用し、最初に要求されたアドレスをそのプロセスに通知する仕組みです。このオプションを使用すると、Cookieのないセッションは、着信リクエストの元の宛先IPアドレス（ほかの機器のアドレスと一致しているはずです）へ転送され、Cookieのあるリクエストは引き続き適切なサーバーへ転送されます。

"transparent"キーワードは非推奨です。代わりに"option transparent"を使用してください。

よくある誤解とは異なり、このオプションによって、HAProxyが接続確立時にクライアントのIPをサーバーへ提示することはありません。

参照："option transparent"。

<a id="entry-4-2-unique-id-format"></a>

**`unique-id-format <fmt>`**

```haproxy
unique-id-format <fmt>
```

各リクエストに一意のIDを生成します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 可

引数：

```text
<fmt>   カスタムログ形式の文字列です（セクション8.2.6参照）。
```

このキーワードは、カスタムログ形式を使用してリクエストごとにIDを作成します。一意のIDは、複雑なインフラストラクチャーの多数のコンポーネントを通るリクエストを追跡するのに役立ちます。作成したIDは、カスタムログ形式文字列で%IDエイリアスを使用してログに記録することもできます。

形式は、組み合わせたときに一意になることが保証される要素で構成することを推奨します。たとえば、複数のHAProxyインスタンスが関わる場合、ノード名を含めることが重要になる場合があります。着信接続の送信元と宛先のアドレスおよびポートをログに記録する必要があることもよくあります。同じ接続上で複数のリクエストを処理できるため、リクエストカウンターを含めると、それらを区別するのに役立つ場合があります。同様に、タイムスタンプはカウンターが一巡した場合の重複を防ぐのに役立つ場合があります。プロセスIDを記録すると、サービスの再起動後の衝突を防げます。

多くのフィールドでは、表記が短くなりログの容量を節約できるため、16進表記を推奨します。

通常の接続では、フロントエンドで設定した形式を使って一意のIDを生成します。ヘルスチェックでは、tcp-checkまたはhttp-checkルールセット内で"unique-id"取得処理を使う際に、バックエンドの形式を使用します。

例：

```text
unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid

次を生成します：

       7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A
```

参照："unique-id-header"。

<a id="entry-4-2-unique-id-header"></a>

**`unique-id-header <name>`**

```haproxy
unique-id-header <name>
```

HTTPリクエストに一意のIDヘッダーを追加します。

使用可能なコンテキスト: http

使用可能なセクション：defaults \| frontend \| listen \| backend 可 \| 可 \| 可 \| 不可

引数：

```text
<name>   ヘッダー名です。
```

unique-id-formatを使って、サーバーへ送信するHTTPリクエストにunique-idヘッダーを追加します。unique-id-formatがなければ動作しません。

例：

```text
    unique-id-format %{+X}o\ %ci:%cp_%fi:%fp_%Ts_%rt:%pid
    unique-id-header X-Unique-ID

    次を生成します：

       X-Unique-ID: 7F000001:8296_7F00001E:1F90_4F7B0A69_0003:790A

関連項目： "unique-id-format"
```

<a id="entry-4-2-use-backend"></a>

**`use_backend <backend> [{if | unless} <condition>]`**

```haproxy
use_backend <backend> [{if | unless} <condition>]
```

if/unlessによるACL条件の一致または不一致に応じて、特定のバックエンドへ切り替えます。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 可 \| 可 \| 不可

引数：

```text
<backend>   有効なbackendまたは"listen"セクションの名前、またはバックエンド名に
            解決されるカスタムログ形式です（セクション8.2.6のカスタムログ形式を参照）。

<condition> セクション7で説明する、ACLで構成した条件です。
            省略した場合、ルールは無条件に適用されます。
```

コンテンツスイッチングでは、接続がフロントエンドに到着し、いくつかの条件に応じて各バックエンドへ振り分けられます。条件とバックエンドの関係は"use_backend"キーワードで記述します。通常はHTTP処理で使用しますが、純粋なTCPでも使用できます。その場合、ステートレスACL（送信元アドレスの検証など）で内容を使用せずに処理する方法と、"tcp-request"ルールと組み合わせてペイロードの到着を待つ方法があります。

"use_backend"ルールはいくつでも指定できます。これらのルールはすべて宣言順に評価され、最初に一致したルールがバックエンドを割り当てます。そのバックエンドが停止していると見なされる場合も同じです。ただし、一致したルールの対象が無効化されている、または公開されていないバックエンドである場合は、そのルールを無視して評価を続けます。

最初の形式では、条件を満たす場合にバックエンドを使用します。2番目の形式では、条件を満たさない場合にバックエンドを使用します。有効な条件がない場合、"default_backend"で定義したバックエンドを、無効化または公開解除されていない限り使用します。デフォルトのバックエンドが利用できない場合、"listen"セクションでは同じセクション内のサーバーを使用します。フロントエンドの場合は、どのサーバーも使用せず、503 service unavailableレスポンスを返します。

TCPフロントエンドからHTTPバックエンドに切り替えることもできます。この場合、フロントエンドですでにHTTPプロトコルであることを確認していれば、直ちにバックエンドの処理に進みます。そうでなければ、バックエンドは完全なHTTPリクエストの到着を待ちます。この機能は、一つのポートで複数のプロトコルを解析する必要があり、その中にHTTPが含まれるフロントエンドに便利です。

`<backend>`が単純な名前の場合、設定時に解決され、指定したバックエンドが存在しないとエラーを報告します。一方、`<backend>`がカスタムログ形式の場合、設定時には検査できないため、バックエンド名を実行時に動的に解決します。結果のバックエンド名がどの有効なバックエンドにも対応しない場合、ほかのルールは評価せず、代わりにdefault_backendディレクティブを適用します。動的なバックエンド名を使用する場合、リクエストから許可されていないバックエンドを強制的に選択できないように、ほかのバックエンドが使用していない接頭辞を使うことを強く推奨します。

明示的な名前を指定した"use_backend"ルールは、バックエンドの"fullconn"設定を計算するために、フロントエンドとバックエンドの関連を検出する際にも使用されます。動的な名前では、この処理はできません。

"default_backend"、"tcp-request"、"fullconn"、"log-format"、およびACLに関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

<a id="entry-4-2-use-fcgi-app"></a>

**`use-fcgi-app <name>`**

```haproxy
use-fcgi-app <name>
```

バックエンドに使用するFastCGIアプリケーションを定義します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<name>    使用するFastCGIアプリケーションの名前です。
```

詳細は、FastCGIアプリケーションの設定に関する[セクション10.1](/ja/haproxy/fastcgi/#section-10-1)を参照してください。

<a id="entry-4-2-use-server"></a>

**`use-server <server> if <condition>`**

```haproxy
use-server <server> if <condition>
use-server <server> unless <condition>
```

if/unlessで指定したACL条件の一致または不一致が成立する場合に限り、特定のサーバーを使用します。

使用可能なコンテキスト：tcp, http

使用可能なセクション: defaults \| frontend \| listen \| backend 不可 \| 不可 \| 可 \| 可

引数：

```text
<server>    同じbackendセクション内の有効なサーバーの名前、
            またはサーバー名に評価されるカスタムログ形式の文字列です
            （セクション8.2.6参照）。

<condition> セクション7で説明する、ACLで構成された条件です。
```

既定では、バックエンドに届いた接続は、設定したアルゴリズムに従って利用可能なサーバー間で負荷分散されます。ただし、Cookieなどで接続先を固定する仕組みを使用しており、それがリクエスト内に見つかった場合は除きます。

あるサーバー専用のバックエンドを宣言せずに、特定のリクエストをそのサーバーへ転送したい場合があります。これは"use-server"ルールで実現できます。これらのルールは"redirect"ルールの後、Cookieの評価前に評価され、Cookieより優先されます。"use-server"ルールはいくつでも指定できます。すべてのルールを宣言順に評価し、最初に一致したルールがサーバーを割り当てます。

ルールが停止中のサーバーを指定し、"option persist"が使われておらず、force-persistルールも成立していない場合は、そのルールを無視します。一致するルールが見つかるまで、後続のルールの評価を続けます。

最初の形式では、条件を満たす場合にサーバーを使用します。2番目の形式では、条件を満たさない場合にサーバーを使用します。有効な条件がない場合、処理を続行し、ほかの接続先の固定の仕組みに従ってサーバーを割り当てます。

ルールが一致してもCookieの処理は引き続き行われますが、サーバーは割り当てないことに注意してください。これにより、接頭辞付きCookieから接頭辞を除去できます。

"use-server"文はHTTPモードとTCPモードの両方で動作するため、コンテンツに基づく検査に適しています。たとえば、暗黙のTLSを使用するプロトコルでは、TLSのSNIフィールドに従ってサーバー群の中からサーバーを選択できます（"req.ssl_sni"も参照）。また、これらのサーバーの重みをゼロに設定すると、ほかのトラフィックには使用されなくなります。

例：

```shell
# intercept incoming TLS requests based on the SNI field
use-server www if { req.ssl_sni -i www.example.com }
server     www 192.168.0.1:443 weight 0
use-server mail if { req.ssl_sni -i mail.example.com }
server     mail 192.168.0.1:465 weight 0
use-server imap if { req.ssl_sni -i imap.example.com }
server     imap 192.168.0.1:993 weight 0
# all the rest is forwarded to this server
server  default 192.168.0.2:443 check
```

`<server>`が単純な名前であれば、設定内の既存サーバーと照合し、指定したサーバーが存在しない場合はエラーを報告します。カスタムログ形式であれば、設定解析時には確認しません。実行時に有効なサーバー名を解決できず、そのuse-serverルールの条件であるACLが真を返した場合は、ほかのuse-serverルールを適用せず、負荷分散に切り替えます。

"use_backend"、serverに関する[セクション5](/ja/haproxy/bind-and-server-options/)、およびACLに関する[セクション7](/ja/haproxy/acls-and-samples/)も参照してください。

## 4.3. アクションキーワードの一覧表 {#section-4-3}

リクエストまたはレスポンスの処理のさまざまな段階で、複数のルールセットを評価します。各ルールセット内のルールでは、省略可能な条件が満たされた場合に、アクションを実行できます。

多数のアクションが標準で用意されており、内容の変更、処理の受け入れやブロック、内部状態の変更などを行えます。また、Luaで新しいアクションを定義することもできます。その場合、名前には必ず"lua."の接頭辞が付きます。

以前は特定のルールセットでしか使えないアクションもありましたが、現在は多くのアクションを複数のルールセットで使用できます。このセクションの一覧では、次のルールセットの略称にチェックを付けて、サポートされる各アクションをどこで使用できるかを示します。

- QUIC Ini：アクションは"quic-initial"ルールで有効です。
- TCP RqCon：アクションは"tcp-request connection"ルールで有効です。
- TCP RqSes：アクションは"tcp-request session"ルールで有効です。
- TCP RqCnt：アクションは"tcp-request content"ルールで有効です。
- TCP RsCnt：アクションは"tcp-response content"ルールで有効です。
- HTTP Req：アクションは"http-request"ルールで有効です。
- HTTP Res：アクションは"http-response"ルールで有効です。
- HTTP Aft：アクションは"http-after-response"ルールで有効です。

同じ略語を、後述のリファレンスの[セクション4.4](/ja/haproxy/proxies/#section-4-4)でも使用します。

```text
 キーワード                QUIC: Ini   TCP: RqCon RqSes RqCnt RsCnt   HTTP: Req Res Aft
----------------------+-----------+-----------+-----+-----+------+----------+---+----
accept                         X           X     X     X     X            -   -   -
add-acl                        -           -     -     -     -            X   X   -
add-header                     -           -     -     -     -            X   X   X
add-headers-bin                -           -     -     -     -            X   X   X
allow                          -           -     -     -     -            X   X   X
attach-srv                     -           -     X     -     -            -   -   -
auth                           -           -     -     -     -            X   -   -
cache-store                    -           -     -     -     -            -   X   -
cache-use                      -           -     -     -     -            X   -   -
capture                        -           -     -     X     -            X   X   X
close                          -           -     -     -     X            -   -   -
del-acl                        -           -     -     -     -            X   X   -
del-header                     -           -     -     -     -            X   X   X
del-headers-bin                -           -     -     -     -            X   X   X
del-map                        -           -     -     -     -            X   X   X
deny                           -           -     -     -     -            X   X   -
dgram-drop                     X           -     -     -     -            -   -   -
disable-l7-retry               -           -     -     -     -            X   -   -
do-log                         X           X     X     X     X            X   X   X
do-resolve                     -           -     -     X     -            X   -   -
early-hint                     -           -     -     -     -            X   -   -
expect-netscaler-cip           -           X     -     -     -            -   -   -
expect-proxy layer4            -           X     -     -     -            -   -   -
normalize-uri                  -           -     -     -     -            X   -   -
pause                          -           -     -     -     -            X   X   -
redirect                       -           -     -     -     -            X   X   -
reject                         X           X     X     X     X            X   -   -
replace-header                 -           -     -     -     -            X   X   X
replace-path                   -           -     -     -     -            X   -   -
replace-pathq                  -           -     -     -     -            X   -   -
replace-uri                    -           -     -     -     -            X   -   -
replace-value                  -           -     -     -     -            X   X   X
return                         -           -     -     -     -            X   X   -
sc-add-gpc                     -           X     X     X     X            X   X   X
--キーワード---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-sc-inc-gpc                     -           X     X     X     X            X   X   X
sc-inc-gpc0                    -           X     X     X     X            X   X   X
sc-inc-gpc1                    -           X     X     X     X            X   X   X
sc-set-gpt                     -           X     X     X     X            X   X   X
sc-set-gpt0                    -           X     X     X     X            X   X   X
send-retry                     X           -     -     -     -            -   -   -
send-spoe-group                -           -     -     X     X            X   X   -
set-bandwidth-limit            -           -     -     X     X            X   X   -
set-bc-mark                    -           -     -     X     -            X   -   -
set-bc-tos                     -           -     -     X     -            X   -   -
set-dst                        -           X     X     X     -            X   -   -
set-dst-port                   -           X     X     X     -            X   -   -
set-fc-mark                    -           X     X     X     X            X   X   -
set-fc-tos                     -           X     X     X     X            X   X   -
set-header                     -           -     -     -     -            X   X   X
set-headers-bin                -           -     -     -     -            X   X   X
set-log-level                  -           -     -     X     X            X   X   X
set-map                        -           -     -     -     -            X   X   X
set-mark (deprecated)          -           X     X     X     X            X   X   -
set-method                     -           -     -     -     -            X   -   -
set-nice                       -           -     -     X     X            X   X   -
set-path                       -           -     -     -     -            X   -   -
set-pathq                      -           -     -     -     -            X   -   -
set-priority-class             -           -     -     X     -            X   -   -
set-priority-offset            -           -     -     X     -            X   -   -
--キーワード---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-set-query                      -           -     -     -     -            X   -   -
set-retries                    -           -     -     X     -            X   -   -
set-src                        -           X     X     X     -            X   -   -
set-src-port                   -           X     X     X     -            X   -   -
set-status                     -           -     -     -     -            -   X   X
set-timeout                    -           -     -     -     -            X   X   -
set-tos (deprecated)           -           X     X     X     X            X   X   -
set-uri                        -           -     -     -     -            X   -   -
set-var                        -           X     X     X     X            X   X   X
set-var-fmt                    -           X     X     X     X            X   X   X
silent-drop                    -           X     X     X     X            X   X   -
strict-mode                    -           -     -     -     -            X   X   X
switch-mode                    -           -     -     X     -            -   -   -
tarpit                         -           -     -     -     -            X   -   -
track-sc0                      -           X     X     X     -            X   X   -
track-sc1                      -           X     X     X     -            X   X   -
track-sc2                      -           X     X     X     -            X   X   -
unset-var                      -           X     X     X     X            X   X   X
use-service                    -           -     -     X     -            X   -   -
wait-for-body                  -           -     -     -     -            X   X   -
wait-for-handshake             -           -     -     -     -            X   -   -
--キーワード---------------QUIC--Ini---TCP--RqCon-RqSes-RqCnt-RsCnt---HTTP--Req-Res-Aft-
```

## 4.4. アルファベット順のアクションリファレンス {#section-4-4}

このセクションでは、各アクションとその使い方を詳しく説明します。ルールセットを示す用語と記号には、前述の[4.3節](/ja/haproxy/proxies/#section-4-3)と同じものを使います。

<a id="entry-4-4-accept"></a>

**`accept`**

```haproxy
accept
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| - \| - \| -

ルールの評価を停止し、リクエストまたはレスポンスがチェックを通過できるようにします。このアクションは終端となるため、現在のセクションでは、同じルールセットに含まれる後続のルールは評価されません。"allow"アクションとの違いは、歴史的な互換性のため、TCPおよびQUICルールでは"accept"、HTTPルールでは"allow"を使うことだけです。後述の"allow"アクションも参照してください。

<a id="entry-4-4-add-acl"></a>

**`add-acl(<file-name>) <key fmt>`**

```haproxy
add-acl(<file-name>) <key fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

ACLに新しいエントリーを追加します。ACLはファイルから読み込まれていなければなりません（ダミーの空ファイルでも構いません）。更新するACLのファイル名を丸括弧内で渡します。引数は`<key fmt>`の1つです。これは[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)で説明するカスタムログ形式の規則に従い、新しいエントリーの内容を収集します。値の重複を避けるため、挿入前にACLを検索します。統計ソケットの"add acl"コマンドに相当しますが、HTTPリクエストを契機に実行できます。

<a id="entry-4-4-add-header"></a>

**`add-header <name> <fmt>`**

```haproxy
add-header <name> <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

`<name>`で指定した名前と、カスタムログ形式の規則に従う`<fmt>`で定義した値を持つHTTPヘッダーフィールドを追加します（[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)のカスタムログ形式を参照）。接続固有の情報（クライアントのSSL証明書など）をサーバーへ渡したり、複数のヘッダーを1つにまとめたりする場合に特に役立ちます。このルールは処理を終了させないため、ほかの同様のルールも追加できます。ヘッダーは直ちに追加されるので、あるルールで前のルールが追加したヘッダーを再利用できる場合があります。

<a id="entry-4-4-add-headers-bin"></a>

**`add-headers-bin <expr> [ prefix <str> ]`**

```haproxy
add-headers-bin <expr> [ prefix <str> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

"add-header"アクションの変種で、ヘッダーの名前と値をvarintでエンコードしたバイナリー文字列として渡します。varint形式については、"req.hdrs_bin"サンプル取得を参照してください。ヘッダー名を事前に知らなくても、複数のヘッダーを一度に設定したい場合に役立ちます。これらのヘッダーはHTTPパーサーで検証されていないため、不正なメッセージを送信する原因となる可能性があり、最悪の場合はリクエストスマグリング攻撃につながる可能性があります。挿入するヘッダー数も重要です。tune.http.maxhdrによって制限されるためです。オプションのprefixを指定すると、エンコードされた文字列のうち、`<str>`で始まるヘッダーだけを設定します。

例：

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request add-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-allow"></a>

**`allow`**

```haproxy
allow
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

ルールの評価を停止し、リクエストがチェックを通過できるようにします。このアクションは終端となるため、現在のセクションでは、同じルールセットに含まれる後続のルールは評価されません。"accept"アクションとの違いは、歴史的な互換性のため、TCPルールでは"accept"、HTTPルールでは"allow"を使うことだけです。前述の"accept"アクションも参照してください。

<a id="entry-4-4-attach-srv"></a>

**`attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]`**

```haproxy
attach-srv <srv> [name <expr>] [ EXPERIMENTAL ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| X \| - \| -
\| - \| - \| -

HTTP/2接続が正しく確立された後に、その接続を捕捉するために使用します。接続の向きをバックエンド側へ反転し、サーバー`<srv>`のアイドルプールに挿入します。'rhttp@'アドレスを持つサーバーでのみ使用できます。

接続は、`<expr>`の評価結果で定義される名前で、サーバーのアイドルプールに挿入されます。この名前は、"pool-conn-name"または"sni"パラメーターが適用されるリクエストで照合されます。詳細は"http-reuse"を参照してください。

リバースHTTPは現在も活発に開発されており、今後、設定方法が変わる可能性があります。そのため、内部では実験的機能として扱われており、このディレクティブより前の行に"expose-experimental-directives"が記載されていなければなりません。

非常によく似た、別の独立したプロトコルも開発中です。
<https://www.ietf.org/archive/id/draft-bt-httpbis-reverse-http-00.html>を参照してください。

<a id="entry-4-4-auth"></a>

**`auth [realm <realm>]`**

```haproxy
auth [realm <realm>]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

ルールの評価を停止し、直ちにHTTP 401または407エラーコードを返して、有効なユーザー名とパスワードの提示を求めます。これ以降の"http-request"ルールは評価されません。省略可能な"realm"パラメーターもサポートされており、レスポンスで返す認証領域（通常はアプリケーション名）を設定します。

対応するプロキシのエラーメッセージを使用します。このメッセージは、"errorfile"または"http-error"ディレクティブでカスタマイズできます。401レスポンスでは、WWW-Authenticateヘッダーのすべての出現箇所を削除し、認証領域"`<realm>`"に対するBasic認証チャレンジを含む新しいヘッダーに置き換えます。407レスポンスでは、Proxy-Authenticateヘッダーに同じ処理を行います。エラーメッセージを変更してはならない場合は、代わりに"http-request return"ルールの使用を検討してください。

例：

```text
acl auth_ok http_auth_group(L1) G1
http-request auth unless auth_ok

```

<a id="entry-4-4-cache-store"></a>

**`cache-store <name>`**

```haproxy
cache-store <name>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| -

http-responseをキャッシュ内に格納します。この段階でレスポンスヘッダーを格納するため、ほかのhttp-responseアクションで、レスポンスの格納前にも格納後にもヘッダーを変更できます。このアクションは、キャッシュ格納フィルターを設定します。

キャッシュの設定については、[セクション6.2](/ja/haproxy/cache/#section-6-2)を参照してください。

<a id="entry-4-4-cache-use"></a>

**`cache-use <name>`**

```haproxy
cache-use <name>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

キャッシュ`<name>`から、キャッシュされたオブジェクトを返すことを試みます。このディレクティブはキャッシュのハッシュ値を計算するため、キャッシュへの保存にも必須です。保存と配信の両方に条件を使いたい場合は、このディレクティブの後に条件を置くのがよい方法です。

キャッシュの設定については、[セクション6.2](/ja/haproxy/cache/#section-6-2)を参照してください。

<a id="entry-4-4-capture"></a>

**`capture <sample> [ len <length> | id <id> ]`**

```haproxy
capture <sample> [ len <length> | id <id> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| X \| X

リクエストまたはレスポンスのバッファーからサンプル式`<sample>`をキャプチャし、最大`<len>`文字の文字列に変換します。結果の文字列は、次の"capture"スロット（リクエスト用またはレスポンス用）に格納されるため、キャプチャしたHTTPヘッダーの隣に表示される場合があります。その後、自動的にログへ出力されます。また、サンプル取得メソッドで抽出して、ヘッダーなどへ渡すこともできます。このサイズの領域が各キャプチャに対してストリームの存続期間全体にわたって割り当てられるため、長さを制限することを推奨します。長さを指定できるのは"http-request"ルールだけであることに注意してください。このスロットが存在するのは、宣言したセクション内だけです。このルールを、別のフロントエンドのバックエンドとしても使われる"listen"セクションに置いた場合、そのフロントエンドから来るストリームでは無視されます。 詳細は、[セクション7.3](/ja/haproxy/acls-and-samples/#section-7-3)（サンプルの取得）、"capture request header"、"capture response header"を参照してください。

"len"の代わりに"id"キーワードを使用すると、アクションはキャプチャした文字列を、すでに宣言されているキャプチャスロットへ格納しようとします。バックエンドでキャプチャを実行する場合に役立ちます。スロットIDは、前の"http-request capture"ディレクティブまたは"declare capture"キーワードで宣言できます。

バックエンドでこのアクションを使用する場合、関連するフロントエンドに必要なキャプチャスロットがあることを十分に確認してください。ない場合、このルールは実行時に無視されます。HAProxyは実行時にバックエンド名を動的に解決できるため、設定の解析時には検出できません。

<a id="entry-4-4-close"></a>

**`close`**

```haproxy
close
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| X
\| - \| - \| -

サーバーとの接続を直ちに閉じるために使用します。これ以降の"tcp-response content"ルールは評価されません。主な目的は、アプリケーションプロトコルが長いタイムアウトの満了を待つことを想定している場合に、やり取りを終えたクライアントとサーバーの接続を強制的に終了させることです。特定のプロトコルでサーバーのリソースを大量に消費する、アイドル接続をなくすことを目指しています。

<a id="entry-4-4-del-acl"></a>

**`del-acl(<file-name>) <key fmt>`**

```haproxy
del-acl(<file-name>) <key fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

ACLからエントリーを削除します。ACLはファイルから読み込まれていなければなりません（ダミーの空ファイルでも構いません）。更新するACLのファイル名を丸括弧内で渡します。引数は`<key fmt>`の1つです。これは[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)のカスタムログ形式の規則に従い、削除するエントリーの内容を収集します。統計ソケットの"del acl"コマンドに相当しますが、HTTPリクエストまたはレスポンスを契機に実行できます。

<a id="entry-4-4-del-header"></a>

**`del-header <name> [ -m <meth> ]`**

```haproxy
del-header <name> [ -m <meth> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

`<name>`で指定した名前を持つHTTPヘッダーフィールドをすべて削除します。`<meth>`は、ヘッダー名に適用する照合方法です。サポートされる照合方法は、"str"（完全一致）、"beg"（前方一致）、"end"（後方一致）、"sub"（部分文字列一致）、"reg"（正規表現による一致）です。省略した場合は完全一致を使用します。

<a id="entry-4-4-del-headers-bin"></a>

**`del-headers-bin <expr> [ -m <meth> ]`**

```haproxy
del-headers-bin <expr> [ -m <meth> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

`<expr>`で指定した名前を持つHTTPヘッダーフィールドをすべて削除します。`<expr>`は、削除するすべてのヘッダー名をvarintでエンコードしたバイナリー文字列を返さなければなりません。エンコードの説明と例は"add-headers-bin"と"set-headers-bin"を参照してください。`<meth>`は照合方法で、すべてのヘッダー名に適用します。使用できる照合方法は"str"（完全一致）、"beg"（接頭辞一致）、"end"（接尾辞一致）、"sub"（部分文字列一致）です。"reg"（正規表現一致）は、実行時の性能が予測できないため、使用できません。指定しない場合、完全一致を使用します。

<a id="entry-4-4-del-map"></a>

**`del-map(<map-name>) <key fmt>`**

```haproxy
del-map(<map-name>) <key fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

MAPからエントリーを削除します。`<map-name>`は、マップとACLの名前についてセクション2.7で説明する形式に従わなければなりません。更新するMAPの名前を丸括弧内で渡します。引数は`<key fmt>`の1つです。これは[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)のカスタムログ形式の規則に従い、削除するエントリーの内容を収集します。引数は"file name"の1つです。統計ソケットの"del map"コマンドに相当しますが、HTTPリクエストまたはレスポンスを契機に実行できます。

<a id="entry-4-4-deny"></a>

**`deny [ { status | deny_status } <code> ] [ content-type <type> ]`**

```haproxy
deny [ { status | deny_status } <code> ] [ content-type <type> ]
     [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

       file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
     [ hdr `<name>` `<fmt>` ]*

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

ルールの評価を停止し、リクエストまたはレスポンスを直ちに拒否します。デフォルトでは、リクエストにはHTTP 403エラー、レスポンスには502を返しますが、返すレスポンスは"return"アクションと同じ構文でカスタマイズできます。詳細は後述の"return"を参照してください。互換性のため、引数を指定しない場合、または"deny_status"だけを指定した場合、"default-errorfiles"引数が暗黙に指定されます。つまり、"deny [deny_status `<status>`]"は"deny [status `<status>`] default-errorfiles"の別名です。このアクションは処理を終了させるため、現在のセクションでは、同じルールセットの後続ルールを評価しません。高度な構文については"return"アクションも参照してください。

<a id="entry-4-4-dgram-drop"></a>

**`dgram-drop`**

```haproxy
dgram-drop
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

QUIC initialパケットの受信を通知せずに無視します。無視しなければ、新しいQUIC接続のインスタンスが作成され、SSLハンドシェイクが実行されます。

<a id="entry-4-4-disable-l7-retry"></a>

**`disable-l7-retry`**

```haproxy
disable-l7-retry
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

接続障害以外の理由でリクエストが失敗した場合、そのリクエストの再試行をすべて無効にします。たとえば、失敗したPOSTリクエストを再試行させないために役立ちます。

<a id="entry-4-4-do-log"></a>

**`do-log [profile <log_profile>]`**

```haproxy
do-log [profile <log_profile>]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| X \| X

このアクションは、プロキシでのログ出力を手動で実行します。つまり、プロキシのログオプション（"log-format"などの形式指定オプションを含む）が考慮されますが、プロキシがトランザクションの処理中に自動生成するログには干渉しません。

"log-profile"を使うと、このアクションを使用できる各コンテキストで、ログをどのように出力するかを詳細に記述できます。具体的には、'on'キーワードの後に'quic-init'、'tcp-req-conn'、'tcp-req-sess'、'tcp-req-cont'、'tcp-res-cont'、'http-req'、'http-res'、'http-after-res'のいずれかを指定します。

また、"%OG"ログ形式エイリアスを使用した場合にも、正しく報告されます。

省略可能な"profile"引数でlog-profileセクションの名前を指定すると、このdo-logアクション専用に使用できます。その場合、既定で適用される現在のロガーに関連付けられたプロファイルの代わりに使用します。

例：

```text
log-profile my-dft-prof
  on tcp-req-conn format "Connect: %ci"

log-profile my-local-prof
  on tcp-req-conn format "Local Connect: %ci"

frontend myfront
  log stdout format rfc5424 profile my-dft-prof local0
  log-format "log generated using proxy logformat, from '%OG'"
  acl local src 127.0.0.1
  # on connection use either log-profile from the logger (my-dft-prof) or
  # explicit my-local-prof if source ip is localhost
  tcp-request connection do-log if !local
  tcp-request connection do-log profile my-local-prof if local
  # on content use proxy logformat, since no override was specified
  # in my-dft-prof
  tcp-request content do-log
```

<a id="entry-4-4-do-resolve"></a>

**`do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>`**

```haproxy
do-resolve(<var>,<resolvers>[,ipv4|ipv6]) <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

このアクションは、`<expr>`の出力に対してDNS名前解決を行い、結果を変数`<var>`に格納します。`<resolvers>`が指すDNS resolversセクションを使用します。省略可能な引数'ipv4'または'ipv6'を使うと、名前解決で優先するファミリーを選択できます。特定のファミリーの使用を厳密に強制するには、globalキーワード"dns-accept-family"も参照してください。

DNS名前解決の実行中、クライアント側の接続は一時停止し、名前解決の完了を待ちます。IPアドレスが見つかると、`<var>`へ格納します。何らかのエラーが発生した場合、`<var>`は設定しません。このアクションを使用すると、リクエスト内の情報（Hostヘッダーなど）に基づいて、実行時にサーバーのIPアドレスを調べることができます。このアクションでサーバーのIPアドレスを調べて"set-dst"アクションで使用する場合、バックエンドのサーバーIPアドレスは0.0.0.0に設定しなければなりません。do-resolveアクションのパラメーターはホストのみを受け取るため、文字列からポートを除去しなければなりません。

例：

```text
resolvers mydns
  nameserver local 127.0.0.53:53
  nameserver google 8.8.8.8:53
  timeout retry   1s
  hold valid 10s
  hold nx 3s
  hold other 3s
  hold obsolete 0s
  accepted_payload_size 8192

frontend fe
  bind 10.42.0.1:80
  http-request do-resolve(txn.myip,mydns,ipv4) hdr(Host),host_only
  http-request capture var(txn.myip) len 40

  # return 503 when the variable is not set,
  # which mean DNS resolution error
  use_backend b_503 unless { var(txn.myip) -m found }

  default_backend be

backend b_503
  # dummy backend used to return 503.
  # one can use the errorfile directive to send a nice
  # 503 error page to end users

backend be
  # rule to prevent HAProxy from reconnecting to services
  # on the local network (forged DNS name used to scan the network)
  http-request deny if { var(txn.myip) -m ip 127.0.0.0/8 10.0.0.0/8 }
  http-request set-dst var(txn.myip)
  server clear 0.0.0.0:0
```

注意：HAProxyがネットワークのスキャンに使われたり、さらに悪い場合には自分自身へのループを起こしたりしないように、"protection"ルールを忘れずに設定してください。

<a id="entry-4-4-early-hint"></a>

**`early-hint <name> <fmt>`**

```haproxy
early-hint <name> <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

ほかのどのレスポンスよりも先に、HTTP 103 Early Hintsレスポンスを作成します。このレスポンスに、`<name>`で指定した名前と、カスタムログ形式の規則に従う`<fmt>`で定義した値を持つHTTPヘッダーフィールドを追加します（[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)のカスタムログ形式を参照）。HTMLドキュメントの描画に必要なリソースを事前に読み込むため、Linkヘッダーをクライアントへ渡す場合に特に役立ちます。

詳細はRFC 8297を参照してください。

<a id="entry-4-4-expect-netscaler-cip-layer4"></a>

**`expect-netscaler-cip layer4`**

```haproxy
expect-netscaler-cip layer4
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

クライアント側の接続で、ソケットから1バイトも読み取る前にNetScaler Client IP insertionプロトコルのヘッダーを受信するよう設定します。"bind"行に"accept-netscaler-cip"キーワードを指定するのと同等ですが、TCPルールを使用すると、ACLで指定した特定のIPアドレス範囲についてだけPROXYプロトコルを受け入れられます。公開ホストからのトラフィックが複数のロードバランサーの層を通る場合に便利です。

<a id="entry-4-4-expect-proxy-layer4"></a>

**`expect-proxy layer4`**

```haproxy
expect-proxy layer4
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| - \| - \| -
\| - \| - \| -

クライアント側の接続を、ソケットから一バイトでも読み取る前にPROXYプロトコルのヘッダーを受信するよう設定します。"bind"行に"accept-proxy"キーワードを指定するのと同じですが、TCPルールを使う場合は、ACLによって特定のIPアドレス範囲からだけPROXYプロトコルを受け入れることができます。公開ホストからのトラフィックが、複数段のロードバランサーを通過する場合に便利です。

<a id="entry-4-4-normalize-uri"></a>

**`normalize-uri <normalizer>`**

```haproxy
normalize-uri <normalizer>
normalize-uri fragment-encode
normalize-uri fragment-strip
normalize-uri path-merge-slashes
normalize-uri path-strip-dot
normalize-uri path-strip-dotdot [ full ]
normalize-uri percent-decode-unreserved [ strict ]
normalize-uri percent-to-uppercase [ strict ]
normalize-uri query-sort-by-name
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

リクエストのURIを正規化します。

HAProxy 2.4のURI正規化は、現在、実験的な技術プレビューとして利用できます。そのため、呼び出せるようにするには、先にglobalディレクティブ'expose-experimental-directives'を指定する必要があります。問題を修正するために正規化処理の動作が変更され、その結果、利用環境でリクエストを正しく処理できなくなる可能性があることを想定しておくべきです。

各ノーマライザーは1種類の正規化だけを処理するため、対応するバックエンドに適した正規化の程度を細かく選択できます。

たとえば、"path-strip-dotdot"ノーマライザーは、要求されたURIをローカルファイルシステム内のパスへ直接対応付ける静的ファイルサーバーで役立つ場合があります。ただし、パス内のセグメント数が特定の数であることを前提とするAPIでは、ルーティングを壊す可能性があります。

一部の正規化処理は、壊れたURIに対して安全でない変換を行う可能性があることに注意が必要です。また、それぞれは安全な正規化処理でも、組み合わせ方が不適切だと、安全でない変換になる可能性があります。

たとえば、壊れたURIにエスケープされていないパーセント記号が含まれていると、"percent-decode-unreserved"正規化処理が予期しない結果を返すことがあります。そのようなURIの例が"/%%36%36"です。これは"/%66"にデコードされ、さらに"/f"と同等になります。"strict"オプションを指定すれば、このような壊れたURIへのリクエストを安全に拒否できます。

次の正規化処理を使用できます。

- fragment-encode："#"を"%23"にエンコードします。

  不具合のあるクライアントがパス部分の'#'を正しくエンコードしないことが分かっている場合を除き、"fragment-strip"ノーマライザーを優先することを推奨します。

  例：

  - /#foo -\> /%23foo

- fragment-strip：URIの"fragment"コンポーネントを削除します。

  RFC 3986#3.5では、URIの"fragment"部分を送信すべきではなく、リソースの取得後にユーザーエージェントが処理すべきとされています。

  フラグメントがリクエストのパスの一部と解釈されないように、この正規化処理を最初に適用することを推奨します。

  例：

  - /#foo -\> /

- path-strip-dot："path"コンポーネント内の"/./"セグメントを削除します（RFC 3986#6.2.2.3）。

  パーセントエンコードされたドット（"%2E"）を含むセグメントは検出しません。それが望ましくない場合は、先に"percent-decode-unreserved"正規化処理を使用してください。

  例：

  - /. -\> /
  - /./bar/ -\> /bar/
  - /a/./a -\> /a/a
  - /.well-known/ -\> /.well-known/（変更なし）

- path-strip-dotdot："path"部分の"/../"セグメントを正規化します（RFC 3986#6.2.2.3）。

  親ディレクトリへのアクセスを試みるセグメントを、その直前のセグメントと統合します。

  空のセグメントは特別扱いしません。それが望ましくない場合は、先に"merge-slashes"正規化処理を使用してください。

  パーセントエンコードされたドット（"%2E"）を含むセグメントは検出しません。それが望ましくない場合は、先に"percent-decode-unreserved"正規化処理を使用してください。

  例：

  - /foo/../ -\> /
  - /foo/../bar/ -\> /bar/
  - /foo/bar/../ -\> /foo/
  - /../bar/ -\> /../bar/
  - /bar/../../ -\> /../
  - /foo//../ -\> /foo/
  - /foo/%2E%2E/ -\> /foo/%2E%2E/

  "full"オプションを指定すると、先頭の"../"も削除されます。

  例：

  - /../bar/ -\> /bar/
  - /bar/../../ -\> /

- path-merge-slashes："path"部分で隣り合うスラッシュを単一のスラッシュにまとめます。

  例：

  - // -\> /
  - /foo//bar -\> /foo/bar

- percent-decode-unreserved：パーセントエンコードされた非予約文字を、通常の文字表現にデコードします（RFC 3986#6.2.2.2）。

  非予約文字には、すべての英字、すべての数字、"-"、"."、"\_"、"~"が含まれます。

  例：

  - /%61dmin -\> /admin
  - /foo%3Fbar=baz -\> /foo%3Fbar=baz（変更なし）
  - /%%36%36 -\> /%66（安全ではありません）
  - /%ZZ -\> /%ZZ

  "strict"オプションを指定した場合は、無効な並びがあるとHTTP 400 Bad Requestを返します。

  例：

  - /%%36%36 -\> HTTP 400
  - /%ZZ -\> HTTP 400

- percent-to-uppercase：パーセントエンコードされた並びの英字を大文字にします（RFC 3986#6.2.2.1）。

  例：

  - /%6f -\> /%6F
  - /%zz -\> /%zz

  "strict"オプションを指定した場合は、無効な並びがあるとHTTP 400 Bad Requestを返します。

  例：

  - /%zz -\> HTTP 400

- query-sort-by-name: クエリー文字列のパラメーターを名前順に並べ替えます。パラメーターは'&'で区切られていると想定します。短い名前が長い名前より先になり、同じ名前のパラメーターは相対的な順序を保ちます。

  例：

  - /?c=3&a=1&b=2 -\> /?a=1&b=2&c=3
  - /?aaa=3&a=1&aa=2 -\> /?a=1&aa=2&aaa=3
  - /?a=3&b=4&a=1&b=5&a=2 -\> /?a=3&a=1&a=2&b=4&b=5

<a id="entry-4-4-pause"></a>

**`pause { <timeout> | <expr> }`**

```haproxy
pause { <timeout> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

指定したミリ秒数だけメッセージの解析を一時停止します。タイムアウトはミリ秒で指定できます。また、このドキュメントの冒頭で説明したように、数値の後ろに単位を付ければほかの単位も使用できます。式を記述することもできます。この式は、ミリ秒単位のタイムアウトとして解釈される数値を返さなければなりません。式の評価に失敗した場合や、不正な値を返した場合、アクションを無視し、評価を続行します。

このアクションはデバッグに使えますが、特定の条件に基づいて一部のクライアントを遅くするためにも使えます。たとえば、"track-sc"ルールで追跡し、リクエストレートが高すぎるクライアントに遅延を加えることができます。

<a id="entry-4-4-redirect"></a>

**`redirect <rule>`**

```haproxy
redirect <rule>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

リダイレクトルールに基づいてHTTPリダイレクトを実行します。"redirect"文とまったく同じですが、ほかの"http-request"ルールまたは"http-response"ルールの途中で処理されるリダイレクトルールを挿入し、これらのルールではカスタムログ形式を使用する点が異なります。レスポンスで許可されるリダイレクトは"location"タイプだけです。さらに、レスポンス中にリダイレクトを実行すると、サーバーからHAProxyへの転送を中断するため、ペイロードはクライアントへ転送されません。HTTP/1では、これにより一部の接続が閉じられる場合があります。このアクションは処理を終了させるため、現在のセクションでは、同じルールセットの後続ルールを評価しません。ルールの構文は"redirect"キーワードを参照してください。

<a id="entry-4-4-reject"></a>

**`reject`**

```haproxy
reject
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| X \| X \| X \| X
\| X \| - \| -

ルールの評価を停止し、レスポンスを一切送信せずに接続を直ちに閉じます。HTTPルールでは、"tcp-request content reject"ルールと同様に動作します。HTTP/2接続を強制的に直ちに閉じる場合に役立ちます。

"tcp-request connection"ルールで拒否した接続は、セッションになることもないため、統計では"denied connections"として別に集計します。セッションのレート制限の対象にはならず、ログにも記録しません。これらのルールは、大規模なDDoS攻撃中などに見られる、極端に高い接続レートをフィルタリングするためだけに使用すべきだからです。このような極端な状況では、各イベントをログに記録するだけでもシステムが破綻し、フィルタリング能力が大幅に低下します。どうしてもログを記録したい場合は、"tcp-request session"ルールもログを記録しないため、代わりに"tcp-request content"ルールを使用することを推奨します。

"tcp-response content"ルールで使用すると、サーバー接続を閉じ、レスポンスを中止します。一般に、機密情報の漏洩を防ぐために使用します。通常は、"wait-for-body"アクションと組み合わせて内容を検査した後に使用します。

このアクションは"quic-initial"ルールでも使用できます。新しく開いたQUIC接続を、SSLハンドシェイクを一切処理せずに直ちに閉じ、CONNECTION_REFUSEDエラーコードでクライアントに通知します。

<a id="entry-4-4-replace-header"></a>

**`replace-header <name> <match-regex> <replace-fmt>`**

```haproxy
replace-header <name> <match-regex> <replace-fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

ヘッダーフィールド`<name>`のすべての出現箇所について、その値を`<match-regex>`と照合します。照合では大文字と小文字を区別します。一致した値は、全体を`<replace-fmt>`に置き換えます。`<replace-fmt>`では書式指定文字を使用でき、"http-request add-header"の`<fmt>`引数と同様に動作します。バックスラッシュ（'&#92;'）の後に数値を続ける、標準的な後方参照もサポートされます。

このアクションは、含まれる値の数に関係なく、ヘッダー行全体を対象にします。そのため、If-Modified-SinceやSet-Cookieのように、値にカンマを含むことが自然なヘッダーの処理に適しています。AcceptやCache-Controlのように、カンマで区切った値の一覧を含むヘッダーは、代わりに"replace-value"アクションで処理するべきです。"replace-value"アクションも参照してください。

例：

```shell
http-request replace-header Cookie foo=([^;]*);(.*) foo=\1;ip=%bi;\2

# applied to:
Cookie: foo=foobar; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# outputs:
Cookie: foo=foobar;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT;

# assuming the backend IP is 192.168.1.20

http-request replace-header User-Agent curl foo

# applied to:
User-Agent: curl/7.47.0

# outputs:
User-Agent: foo
```

例：

```shell
http-response replace-header Set-Cookie (C=[^;]*);(.*) \1;ip=%bi;\2

# applied to:
Set-Cookie: C=1; expires=Tue, 14-Jun-2016 01:40:45 GMT

# outputs:
Set-Cookie: C=1;ip=192.168.1.20; expires=Tue, 14-Jun-2016 01:40:45 GMT

# assuming the backend IP is 192.168.1.20.

```

<a id="entry-4-4-replace-path"></a>

**`replace-path <match-regex> <replace-fmt>`**

```haproxy
replace-path <match-regex> <replace-fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

"replace-header"と同様に動作しますが、ヘッダーの代わりにリクエストのパス部分を対象にします。パス部分は、省略可能なスキームとオーソリティーの後に最初に現れる'/'から始まり、疑問符の直前で終わります。そのため、この置換でスキーム、オーソリティー、クエリー文字列が変わることはありません。

正規表現の評価は、一部のACLより高コストになる場合があります。そのため、置換がまれにしか起きない場合は、条件に一致しなければ評価そのものを行わずに済むよう、条件を付けると有利なことがあります。

例：

```shell
# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-path (.*) /foo\1

# strip /foo: turn /foo/bar?q=1 into /bar?q=1
http-request replace-path /foo/(.*) /\1
# or more efficient if only some requests match:
http-request replace-path /foo/(.*) /\1 if { url_beg /foo/ }

```

<a id="entry-4-4-replace-pathq"></a>

**`replace-pathq <match-regex> <replace-fmt>`**

```haproxy
replace-pathq <match-regex> <replace-fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

"http-request replace-path"と同じ動作ですが、クエリー文字列がある場合はパスにそれを含む点が異なります。したがって、パスとクエリー文字列の両方を置き換えます。

例：

```shell
# suffix /foo: turn /bar?q=1 into /bar/foo?q=1:
http-request replace-pathq ([^?]*)(\?(.*))? \1/foo\2

```

<a id="entry-4-4-replace-uri"></a>

**`replace-uri <match-regex> <replace-fmt>`**

```haproxy
replace-uri <match-regex> <replace-fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

"replace-header"と同様に動作しますが、ヘッダーの代わりにリクエストのURI部分を対象にします。URI部分には、スキーム、オーソリティー、クエリー文字列が含まれる場合があります。それらも照合対象の値の一部として扱います。

正規表現の評価は、一部のACLより高コストになる場合があります。そのため、置換がまれにしか起きない場合は、条件に一致しなければ評価そのものを行わずに済むよう、条件を付けると有利なことがあります。

重要な注意：HTTP/1.xでは歴史的に、ブラウザーが送信するリクエストの大半は"origin form"を使用します。これはURI部分にスキームもauthorityも含まない点で"absolute form"と異なります。主に、プロキシへ送信するリクエスト、手動で作成したリクエスト、一部のアプリケーションが送信するリクエストだけが絶対形式を使用します。そのため、HTTP/1.xでは、"/"で始まるルールの"replace-uri"は通常、ほとんどの場合に問題なく動作します。しかしHTTP/2では、HTTP/1クライアントがプロキシとの通信に使用するものと同じ形の絶対URIだけを送信することがクライアントに推奨されています。そのため、このような部分的なreplace-uriルールは、HTTP/1では動作してもHTTP/2では失敗する場合があります。スキームとauthorityにも任意で一致できるようにルールを変更するか、replace-pathを使用する必要があります。

例：

```shell
# rewrite all "http" absolute requests to "https":
http-request replace-uri ^http://(.*) https://\1

# prefix /foo: turn /bar?q=1 into /foo/bar?q=1:
http-request replace-uri ([^/:]*://[^/]*)?(.*) \1/foo\2

```

<a id="entry-4-4-replace-value"></a>

**`replace-value <name> <match-regex> <replace-fmt>`**

```haproxy
replace-value <name> <match-regex> <replace-fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

"replace-header"と同様に動作しますが、ヘッダー全体ではなく、ヘッダーフィールド`<name>`のカンマで区切られた各値に対して正規表現を照合します。複数の値を持つことが許されるすべてのヘッダーに適しています。たとえば、リクエストのAcceptヘッダーや、リクエストまたはレスポンスのCache-Controlが該当します。

例：

```shell
http-request replace-value X-Forwarded-For ^192\.168\.(.*)$ 172.16.\1

# applied to:
X-Forwarded-For: 192.168.10.1, 192.168.13.24, 10.0.0.37

# outputs:
X-Forwarded-For: 172.16.10.1, 172.16.13.24, 10.0.0.37
```

例：

```shell
http-after-response replace-value Cache-control ^public$ private

# applied to:
Cache-Control: max-age=3600, public

# outputs:
Cache-Control: max-age=3600, private

```

<a id="entry-4-4-return"></a>

**`return [ status <code> ] [ content-type <type> ]`**

```haproxy
return [ status <code> ] [ content-type <type> ]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

         file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

ルールの評価を停止し、レスポンスを直ちに返します。レスポンスに使用するステータスコードは、デフォルトでは200です。"status"の引数として任意で指定できます。レスポンスのcontent-typeも、"content-type"の引数として指定できます。最後に、レスポンス自体を定義できます。使用するerrorfileを指定した完全なHTTPレスポンスでも、使用するファイルまたは文字列を指定したレスポンスペイロードでも構いません。レスポンスは、次の規則に従って作成します。

- 使用するerrorfileもペイロードも定義されていない場合は、ダミーのレスポンスを返します。考慮されるのは"status"引数だけで、[200, 599]の範囲内の任意のコードを指定できます。"content-type"引数は、指定されていても無視されます。

- "default-errorfiles"引数が指定されている場合は、プロキシのerrorfilesを使用します。"status"引数が定義されている場合、その値はHAProxyが扱うステータスコード（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503、504）のいずれかでなければなりません。"content-type"引数は、指定されていても無視されます。

- "errorfile"引数で特定のerrorfileが定義されている場合は、完全なHTTPレスポンスを含むそのファイルを返します。考慮されるのは"status"引数だけで、その値はHAProxyが扱うステータスコード（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503、504）のいずれかでなければなりません。"content-type"引数は、指定されていても無視されます。

- "errorfiles"引数でhttp-errorsセクションが指定されている場合は、そのセクション内の対応するファイルを返します。このファイルには完全なHTTPレスポンスが含まれます。考慮されるのは"status"引数だけで、その値はHAProxyが扱うステータスコード（200、400、403、404、405、408、410、413、414、425、429、431、500、501、502、503、504）のいずれかでなければなりません。"content-type"引数は、指定されていても無視されます。

- "file"または"lf-file"引数を指定すると、ファイルの内容をレスポンスペイロードとして使用します。
  ファイルが空でない場合、そのcontent-typeを"content-type"の引数として設定しなければなりません。
  空の場合、"content-type"引数は無視します。"lf-file"引数では、ファイルの内容をカスタムログ形式として評価します
  （[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)を参照）。"file"引数では、生の内容として扱います。

- "string"または"lf-string"引数が指定されている場合は、定義した文字列をレスポンスのペイロードとして使用します。コンテンツタイプは、必ず"content-type"の引数として設定しなければなりません。"lf-string"引数では、文字列をカスタムログ形式として評価します（[8.2.6節](/ja/haproxy/configuration-logging/#section-8-2-6)を参照）。"string"引数では、そのままの文字列として扱います。

レスポンスがerrorfileに基づいていない場合、"hdr"引数を使ってHTTPヘッダーフィールドを追加できます。それ以外の場合は、すべての"hdr"引数を無視します。各引数のヘッダー名は`<name>`で指定し、値は`<fmt>`で定義します。この書式は、[8.2.6節](/ja/haproxy/configuration-logging/#section-8-2-6)に記載されたカスタムログ形式の規則に従います。

生成されるレスポンスは、バッファーより小さくなければなりません。また、errorfileまたはrawファイルを読み込む際に警告を出さないようにするには、ヘッダー書き換え用に予約されたバッファー領域も空けておくべきです。

このアクションで処理を確定します。つまり、現在のセクションでは、同じルールセットの後続ルールを評価しません。

例：

```text
http-request return errorfile /etc/haproxy/errorfiles/200.http \
    if { path /ping }

http-request return content-type image/x-icon file /var/www/favicon.ico  \
    if { path /favicon.ico }

http-request return status 403 content-type text/plain    \
    lf-string "Access denied. IP %[src] is blacklisted."  \
    if { src -f /etc/haproxy/blacklist.lst }

```

<a id="entry-4-4-sc-add-gpc"></a>

**`sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-add-gpc(<idx>,<sc-id>) { <int> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

このアクションは、`<sc-id>`で指定したスティッキーカウンターに関連付けられた配列の、インデックス`<idx>`にある汎用カウンターを、整数`<int>`の値または式`<expr>`の整数評価結果だけ増やします。整数と式の値は、符号なし32ビット値に制限されます。エラーが発生すると、このアクションは通知せずに失敗し、アクションの評価を続行します。`<idx>`は0から99まで、`<sc-id>`は0から2までの整数です。このインデックスにGPCが格納されていない場合も、通知せずに失敗します。値がゼロでも、テーブル内のエントリーをリフレッシュします。'gpc_rate'は、gpc値の平均増加率を反映するよう自動的に調整されます。

このアクションは、配列のdata_typesである'gpc'と'gpc_rate'にのみ適用されます。従来の'gpc0'、'gpc1'、'gpc0_rate'、'gpc1_rate'には適用されません。従来のデータ型に対応する同等の機能はありませんが、値が常に1であれば、'sc-inc-gpc()'、'sc-inc-gpc0()'、'sc-inc-gpc1()'を参照してください。値を減らす方法もありませんが、代わりに'sc-set-gpt()'を使って、汎用タグに正確な値を保存できます。

このアクションの主な用途は、スコアや総量を集計することです（サーバーまたはWAFが報告する送信元IPごとの推定危険度、アップロードした総バイト数など）。

<a id="entry-4-4-sc-inc-gpc"></a>

**`sc-inc-gpc(<idx>,<sc-id>)`**

```haproxy
sc-inc-gpc(<idx>,<sc-id>)
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

このアクションは、`<sc-id>`で指定したスティッキーカウンターに関連付けられた配列の、インデックス`<idx>`にある汎用カウンターを増やします。エラーが発生すると、このアクションは通知せずに失敗し、アクションの評価を続行します。`<idx>`は0から99まで、`<sc-id>`は0から2までの整数です。このインデックスにGPCが格納されていない場合も、通知せずに失敗します。このアクションは、配列の'gpc'および'gpc_rate'というdata_typesだけに適用されます（従来の'gpc0'、'gpc1'、'gpc0_rate'、'gpc1_rate'というdata_typesには適用されません）。

<a id="entry-4-4-sc-inc-gpc0"></a>

**`sc-inc-gpc0(<sc-id>)`**

```haproxy
sc-inc-gpc0(<sc-id>)
sc-inc-gpc1(<sc-id>)
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

このアクションは、`<sc-id>`で指定したスティッキーカウンターに対応するGPC0またはGPC1カウンターを増加させます。エラーが発生した場合は通知せずに失敗し、アクションの評価は続行されます。

<a id="entry-4-4-sc-set-gpt"></a>

**`sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt(<idx>,<sc-id>) { <int> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

このアクションは、`<sc-id>`で指定したスティッキーカウンターに関連付けられた配列の、インデックス`<idx>`にある32ビット符号なしGPTを、`<int>`/`<expr>`の値に設定します。期待される結果は真偽値です。

エラーが発生した場合、このアクションは通知せずに失敗し、アクションの評価は続行されます。`<idx>`は0から99の整数、`<sc-id>`は0から2の整数です。そのインデックスにGPTが格納されていない場合も、通知せずに失敗します。

このアクションは'gpt'配列のdata_typeにのみ適用され、従来の'gpt0' data-typeには適用されません。

<a id="entry-4-4-sc-set-gpt0"></a>

**`sc-set-gpt0(<sc-id>) { <int> | <expr> }`**

```haproxy
sc-set-gpt0(<sc-id>) { <int> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

このアクションは、`<sc-id>`で指定したスティッキーカウンターと`<int>`/`<expr>`の値に従って、32ビット符号なしGPT0タグを設定します。期待される結果は真偽値です。エラーが発生した場合、このアクションは通知せずに失敗し、アクションの評価は続行されます。このアクションは"sc-set-gpt(0,`<sc-id>`)"の別名です。"sc-set-gpt"アクションも参照してください。

<a id="entry-4-4-send-retry"></a>

**`send-retry`**

```haproxy
send-retry
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft X \| - \| - \| - \| -
\| - \| - \| -

このアクションは、トークンを持たないクライアントのInitialパケットに対して、Retryパケットの送信を強制します。接続を構成する要素を生成してハンドシェイクを開始する前に、クライアントアドレスを確実に検証するために役立ちます。

<a id="entry-4-4-send-spoe-group"></a>

**`send-spoe-group <engine-name> <group-name>`**

```haproxy
send-spoe-group <engine-name> <group-name>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

このアクションは、SPOEメッセージのグループの送信を開始するために使用します。そのためには、メッセージの送信に使うSPOEエンジンと、送信するSPOEグループを定義しなければなりません。当然ながら、SPOEエンジンは既存のSPOEフィルターを参照する必要があります。SPOEフィルター行でエンジン名が指定されていない場合は、SPOEエージェント名を使用しなければなりません。

引数：

```text
<engine-name>  SPOEエンジン名です。

<group-name>   エンジン設定で指定された
               SPOEグループ名です。

```

<a id="entry-4-4-set-bandwidth-limit"></a>

**`set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]`**

```haproxy
set-bandwidth-limit <name> [limit {<expr> | <size>}] [period {<expr> | <time>}]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

このアクションは、帯域幅制限フィルター`<name>`を有効にします。フィルターの種類に応じて、アップロード方向またはダウンロード方向に適用されます。`<name>`がストリーム単位の帯域幅制限フィルターを参照する場合に限り、独自の上限と期間を定義できます。set-bandwidth-limitルールを実行すると、まずフィルターのすべての設定をデフォルト値に戻してから有効にします。そのため、同じフィルターに対して複数の"set-bandwidth-limit"アクションを実行した場合、最後のアクションだけが考慮されます。同じストリームで複数の帯域幅制限フィルターを有効にできます。

帯域制限フィルターはdefaultsセクションで定義できないため、このアクションもdefaultsセクションでは使用できません。また、制限されるのはHTTPペイロードの転送だけで、HTTPヘッダーは対象に含みません。

引数：

```text
<expr>  サンプル取得の後にコンバーターを続けた、標準的なHAProxyの式です。
        結果は整数に変換されます。"limit"パラメーターではバイト単位のサイズ、
        "period"パラメーターではミリ秒単位の時間として解釈します。

<size>  数値です。HAProxyのサイズ形式に従い、バイト単位で表します。

<time>  数値です。HAProxyの時間形式に従い、ミリ秒単位で表します。
```

例：

```text
http-request set-bandwidth-limit global-limit
http-request set-bandwidth-limit my-limit limit 1m period 10s
```

帯域制限フィルターの設定については、[セクション9.7](/ja/haproxy/filters/#section-9-7)を参照してください。

<a id="entry-4-4-set-bc-mark"></a>

**`set-bc-mark { <mark> | <expr> }`**

```haproxy
set-bc-mark { <mark> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

対応するプラットフォームで、バックエンド接続（サーバーへ送信するすべてのパケット）のNetfilter/IPFW MARKを、`<mark>`または`<expr>`で渡した値に設定します。この値は符号なし32ビット値で、netfilter/ipfw、ルーティングテーブル、またはDTraceによるパケット監視で照合できます。`<mark>`は10進形式でも16進形式（"0x"接頭辞付き）でも指定できます。代わりに`<expr>`も使用できます。これはサンプル取得とその後に続くコンバーターで構成される標準のHAProxy式で、整数型に解決されなければなりません。このアクションは、特定のパケットに異なる経路を強制する場合に役立ちます（大量のダウンロードに、より安価なネットワーク経路を使用する場合など）。Linuxカーネル2.6.32以降で動作し、管理者権限が必要です。FreeBSDとOpenBSDでも動作します。マークは、バックエンド/サーバー接続の存続期間全体（接続からクローズまで）にわたって設定されます。

<a id="entry-4-4-set-bc-tos"></a>

**`set-bc-tos { <tos> | <expr> }`**

```haproxy
set-bc-tos { <tos> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

対応するプラットフォームで、バックエンド接続（サーバーへ送信するすべてのパケット）のTOSまたはDSCPフィールドを、`<tos>`または`<expr>`で渡した値に設定します。この値は、IP TOSフィールドの8ビット全体を表します。DSCPまたはTOSで使用するのは上位6ビットだけで、下位2ビットは常に0であることに注意してください。代わりに`<expr>`も使用できます。これはサンプル取得とその後に続くコンバーターで構成される標準のHAProxy式で、整数型に解決されなければなりません。このアクションは、リクエスト内の情報に基づいて、内部ルーターのルーティング動作を調整するために使用できます。tosは、バックエンド/サーバー接続の存続期間全体（接続からクローズまで）にわたって設定されます。

詳細はRFC 2474、2597、3260、4594を参照してください。

<a id="entry-4-4-set-dst"></a>

**`set-dst <expr>`**

```haproxy
set-dst <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

宛先IPアドレスを、指定した式の値に設定するために使用します。HAProxyの前段のプロキシが宛先IPを書き換えるものの、正しいIPをHTTPヘッダーで渡す場合や、プライバシーのためにIPをマスクしたい場合に便利です。新しいアドレスとポートに接続するには、バックエンドのサーバーアドレスとして'0.0.0.0:0'を使用してください。

引数：

```text
<expr>  サンプル取得の後にコンバーターを続けて構成する、
        標準的なHAProxyの式です。
```

例：

```text
http-request set-dst hdr(x-dst)
http-request set-dst dst,ipmask(24)
```

set-dstは、アドレスファミリーが許す限り、可能であれば元の宛先ポートを保持します。それ以外の場合、宛先ポートは0になります。

<a id="entry-4-4-set-dst-port"></a>

**`set-dst-port <expr>`**

```haproxy
set-dst-port <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

宛先ポートを、指定した式の値に設定するために使用します。新しいアドレスとポートに接続するには、バックエンドのサーバーアドレスとして'0.0.0.0:0'を使用してください。

引数：

```text
<expr>  サンプル取得の後にコンバーターを続けて構成する、
        標準的なHAProxyの式です。
```

例：

```text
http-request set-dst-port hdr(x-port)
http-request set-dst-port int(4000)
```

set-dst-portは、アドレスファミリーがポートをサポートする限り、可能であれば元の宛先アドレスを保持します。そうでなければ、ポートを書き換える前に、宛先アドレスをIPv4の"0.0.0.0"に強制的に設定します。

<a id="entry-4-4-set-fc-mark"></a>

**`set-fc-mark { <mark> | <expr> }`**

```haproxy
set-fc-mark { <mark> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

対応するプラットフォームで、クライアントへ送信するすべてのパケットのNetfilter/IPFW MARKを、`<mark>`または`<expr>`で渡した値に設定します。この値は符号なし32ビット値で、netfilter/ipfw、ルーティングテーブル、またはDTraceによるパケット監視で照合できます。`<mark>`は10進形式でも16進形式（"0x"接頭辞付き）でも指定できます。代わりに`<expr>`も使用できます。これはサンプル取得とその後に続くコンバーターで構成される標準のHAProxy式で、整数型に解決されなければなりません。このアクションは、特定のパケットに異なる経路を強制する場合に役立ちます（大量のダウンロードに、より安価なネットワーク経路を使用する場合など）。Linuxカーネル2.6.32以降で動作し、管理者権限が必要です。FreeBSDとOpenBSDでも動作します。

<a id="entry-4-4-set-fc-tos"></a>

**`set-fc-tos { <tos | <expr> }`**

```haproxy
set-fc-tos { <tos | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

対応するプラットフォームで、クライアントへ送信するパケットのTOSまたはDSCPフィールドを、`<tos>`または`<expr>`で渡した値に設定します。この値は、IP TOSフィールドの8ビット全体を表します。DSCPまたはTOSで使用するのは上位6ビットだけで、下位2ビットは常に0であることに注意してください。代わりに`<expr>`も使用できます。これはサンプル取得とその後に続くコンバーターで構成される標準のHAProxy式で、整数型に解決されなければなりません。このアクションは、リクエスト内の情報に基づいて、境界ルーターのルーティング動作を調整するために使用できます。

詳細はRFC 2474、2597、3260、4594を参照してください。

<a id="entry-4-4-set-header"></a>

**`set-header <name> <fmt>`**

```haproxy
set-header <name> <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

"add-header"アクションと同じですが、ヘッダーがすでに存在する場合は、先に削除します。外部のユーザーにヘッダーを操作させてはならないセキュリティ情報をサーバーに渡す場合や、外部情報を隠すために"Server"などの特定のレスポンスヘッダーを強制的に設定する場合に便利です。新しい値は削除前に計算されるため、既存のヘッダーに値を連結することもできます。

例：

```text
http-request set-header X-Haproxy-Current-Date %T
http-request set-header X-SSL                  %[ssl_fc]
http-request set-header X-SSL-Session_ID       %[ssl_fc_session_id,hex]
http-request set-header X-SSL-Client-Verify    %[ssl_c_verify]
http-request set-header X-SSL-Client-DN        %{+Q}[ssl_c_s_dn]
http-request set-header X-SSL-Client-CN        %{+Q}[ssl_c_s_dn(cn)]
http-request set-header X-SSL-Issuer           %{+Q}[ssl_c_i_dn]
http-request set-header X-SSL-Client-NotBefore %{+Q}[ssl_c_notbefore]
http-request set-header X-SSL-Client-NotAfter  %{+Q}[ssl_c_notafter]
```

<a id="entry-4-4-set-headers-bin"></a>

**`set-headers-bin <expr> [ prefix <str> ]`**

```haproxy
set-headers-bin <expr> [ prefix <str> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

"set-header"アクションの変種で、ヘッダーの名前と値をvarintでエンコードしたバイナリー文字列として渡します。varint形式については、"req.hdrs_bin"サンプル取得を参照してください。ヘッダー名を事前に知らなくても、複数のヘッダーを一度に設定したい場合に役立ちます。これらのヘッダーはHTTPパーサーで検証されていないため、不正なメッセージを送信する原因となる可能性があり、最悪の場合はリクエストスマグリング攻撃につながる可能性があります。挿入するヘッダー数も重要です。tune.http.maxhdrによって制限されるためです。オプションのprefixを指定すると、エンコードされた文字列のうち、`<str>`で始まるヘッダーだけを設定します。

例：

```shell
# This would reset the Accept/UA/Host headers to their initial values
http-request set-var(txn.oldheaders) req.hdrs_bin
http-request del-header Accept
http-request del-header User-Agent
http-request del-header Host
http-request set-headers-bin var(txn.oldheaders)

```

<a id="entry-4-4-set-log-level"></a>

**`set-log-level <level>`**

```haproxy
set-log-level <level>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| X

特定の条件を満たしたときに、現在のリクエストのログレベルを変更するために使用します。有効なレベルは、syslogの8レベル（"log"キーワードを参照）と、そのリクエストのログ出力を無効にする特別なレベル"silent"です。このルールは評価を終了しないため、最後に一致したルールが優先されます。ほかの機器から来るヘルスチェックのログ出力を無効にするのに役立ちます。

<a id="entry-4-4-set-map"></a>

**`set-map(<map-name>) <key fmt> <value fmt>`**

```haproxy
set-map(<map-name>) <key fmt> <value fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

マップに新しいエントリーを追加します。`<map-name>`は、マップとACLの名前についてセクション2.7で説明する形式に従わなければなりません。更新するMAPの名前を丸括弧内で渡します。引数は2つです。`<key fmt>`は[セクション8.2.6](/ja/haproxy/configuration-logging/#section-8-2-6)で説明するカスタムログ形式の規則に従い、マップのキーを収集します。`<value fmt>`もカスタムログ形式の規則に従い、新しいエントリーの内容を収集します。値の重複を避けるため、挿入前にマップを検索します。統計ソケットの"set map"コマンドに相当しますが、HTTPリクエストを契機に実行できます。

<a id="entry-4-4-set-mark"></a>

**`set-mark <mark> (deprecated)`**

```haproxy
set-mark <mark> (deprecated)
```

これは"set-fc-mark"のエイリアスです（代わりにこちらを使用することを推奨します）。

<a id="entry-4-4-set-method"></a>

**`set-method <fmt>`**

```haproxy
set-method <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

リクエストメソッドを、書式文字列`<fmt>`の評価結果で書き換えます。何かを直すより壊す可能性のほうが高いため、これが必要となる妥当な理由はごく少ないはずです。

<a id="entry-4-4-set-nice"></a>

**`set-nice <nice>`**

```haproxy
set-nice <nice>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| X
\| X \| X \| -

処理中の現在のリクエスト/レスポンスの"nice"値を設定します。同時に処理しているほかのリクエストとの関係にだけ影響します。デフォルト値は0ですが、"bind"行の"nice"設定で変更できます。指定できる範囲は-1024..1024です。値が大きいほど、そのリクエストはほかのリクエストに処理を譲ります。値が小さいほど、ほかのリクエストより優先されます。一部のリクエストの処理を高速化したり、重要でないリクエストの優先度を下げたりする場合に役立ちます。事前に試さずにこの設定を使用すると、大幅な速度低下が発生する可能性があります。

<a id="entry-4-4-set-path"></a>

**`set-path <fmt>`**

```haproxy
set-path <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

    リクエストのパスを、書式文字列`<fmt>`の評価結果で書き換えます。クエリー文字列があれば、そのまま保持します。パスの前にスキームとオーソリティーがあれば、それらも保持します。リクエストにパスがない場合（"*"）は、それを書式の評価結果で置き換えます。たとえば、パスの前にディレクトリ要素を追加するために使用できます。"http-request set-query"と"http-request set-uri"も参照してください。

例：

```shell
# prepend the host name before the path
http-request set-path /%[hdr(host)]%[path]

```

<a id="entry-4-4-set-pathq"></a>

**`set-pathq <fmt>`**

```haproxy
set-pathq <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

"http-request set-path"と同じですが、クエリー文字列も書き換えます。疑問符を含めてクエリー文字列を削除するために使用できます（"http-request set-query"ではできません）。

<a id="entry-4-4-set-priority-class"></a>

**`set-priority-class <expr>`**

```haproxy
set-priority-class <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

現在のリクエストのキュー優先度クラスを設定するために使用します。値には、-2047..2047の範囲の整数に変換されるサンプル式を指定しなければなりません。この範囲を超える結果は切り詰められます。優先度クラスは、キュー内のリクエストを処理する順序を決定します。値が小さいほど優先度が高くなります。

<a id="entry-4-4-set-priority-offset"></a>

**`set-priority-offset <expr>`**

```haproxy
set-priority-offset <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

現在のリクエストの、キュー優先度タイムスタンプのオフセットを設定します。値は、-524287..524287の範囲の整数に変換されるサンプル式でなければなりません。この範囲外の結果は切り詰められます。リクエストをキューに入れると、まず優先度クラスで順序を決め、次に指定したミリ秒単位のオフセットで調整した現在のタイムスタンプで順序を決めます。値が小さいほど優先度が高くなります。結果のタイムスタンプは、524,287ms（8m44s287ms）の範囲を扱える精度でしか追跡しないことに注意してください。リクエストが長時間キュー内で待機し、調整後のタイムスタンプがこの値を超えると、最優先と誤認されます。そのため、オフセットと組み合わせたときにこの上限を超えない値へ"timeout queue"を設定することが重要です。

<a id="entry-4-4-set-query"></a>

**`set-query <fmt>`**

```haproxy
set-query <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

最初の疑問符（"?"）の後にあるリクエストのクエリー文字列を、形式文字列`<fmt>`の評価結果で書き換えます。疑問符より前の部分は変更しません。リクエストに疑問符がなく、新しい値が空でない場合、URIの末尾に疑問符を追加し、その後に新しい値を追加します。疑問符がすでにある場合、値が空でも疑問符は決して削除しません。クエリー文字列のパラメーターを追加または削除するために使用できます。

参照："http-request set-query"、"http-request set-uri"。

例：

```shell
# replace "%3D" with "=" in the query string
http-request set-query %[query,regsub(%3D,=,g)]

```

<a id="entry-4-4-set-retries"></a>

**`set-retries <int> | <epxr>`**

```haproxy
set-retries <int> | <epxr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

このアクションは、現在のストリームに限って、指定済みの"retries"値を上書きします。[0, 100]の範囲の整数値、または式を指定できます。式は[0, 100]の範囲の整数を返さなければなりません。

このアクションはバックエンド側でだけ意味を持つため、このルールを使用できるのはバックエンド機能を持つプロキシだけです。"defaults"セクションでも使用できません。リスナーでこのアクションを使用すると、フロントエンドのコンテキストで評価します。そのため、retriesの値を維持するのは、たとえばuse-backendルールなどによってストリームが別のバックエンドへ振り分けられない場合だけです。振り分けられる場合は、選択したバックエンドのデフォルトのretries値を設定します。

例：

```text
tcp-request content set-retries 3
http-request set-retries var(txn.retries)
```

<a id="entry-4-4-set-src"></a>

**`set-src <expr>`**

```haproxy
set-src <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

送信元IPアドレスを、指定した式の値に設定するために使用します。HAProxyの前段のプロキシが送信元IPを書き換えるものの、正しいIPをHTTPヘッダーで渡す場合や、プライバシーのために送信元IPをマスクしたい場合に便利です。それ以降の"src"取得処理の呼び出しは、すべてこの値を返します（例を参照）。

引数：

```text
<expr>  サンプル取得の後にコンバーターを続けて構成する、
        標準的なHAProxyの式です。
```

参照："option forwardfor"。

例：

```shell
http-request set-src hdr(x-forwarded-for)
http-request set-src src,ipmask(24)

# After the masking this will track connections
# based on the IP address with the last byte zeroed out.
http-request track-sc0 src
```

set-srcは、アドレスファミリーが許す限り、可能であれば元の送信元ポートを保持します。それ以外の場合、送信元ポートは0になります。

<a id="entry-4-4-set-src-port"></a>

**`set-src-port <expr>`**

```haproxy
set-src-port <expr>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| - \| -

指定した式の値を送信元ポートアドレスに設定するために使用します。

引数：

```text
<expr>  サンプル取得の後にコンバーターを続けて構成する、
        標準的なHAProxyの式です。
```

例：

```text
http-request set-src-port hdr(x-port)
http-request set-src-port int(4000)
```

set-src-portは、アドレスファミリーがポートをサポートする限り、可能であれば元の送信元アドレスを保持します。そうでなければ、ポートを書き換える前に、送信元アドレスをIPv4の"0.0.0.0"に強制的に設定します。

<a id="entry-4-4-set-status"></a>

**`set-status <status> [reason <str>]`**

```haproxy
set-status <status> [reason <str>]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| - \| X \| X

レスポンスのステータスコードを`<status>`に置き換えます。この値は100から999の整数でなければなりません。省略可能な`<str>`で独自の理由句を指定できます。指定しない場合は、そのコードの既定の理由句を使用します。理由句が存在するのはHTTP/1.xだけで、ほかのバージョンのプロトコルでは無視されます。

例：

```shell
# return "431 Request Header Fields Too Large"
http-response set-status 431
# return "503 Slow Down", custom reason
http-response set-status 503 reason "Slow Down".

```

<a id="entry-4-4-set-timeout"></a>

**`set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }`**

```haproxy
set-timeout { client | connect | queue | server | tarpit | tunnel } { <timeout> | <expr> }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

このアクションは、指定した"client"、"connect"、"queue"、"server"、"tarpit"、"tunnel"のタイムアウトを、現在のストリームについてだけ上書きします。1つのタイムアウトを変更しても、ほかのタイムアウトには影響しません。設定の解析時に相互に継承される場合も同じです（最後の例を参照）。タイムアウトはミリ秒で指定できます。また、このドキュメントの冒頭で説明したように、数値の後ろに単位を付ければほかの単位も使用できます。式を記述することもできます。この式は、ミリ秒単位のタイムアウトとして解釈される数値を返さなければなりません。

connect、queue、server、tunnelのタイムアウトはバックエンド側でだけ意味を持つため、このルールを使用できるのはバックエンド機能を持つプロキシだけです。同様に、clientタイムアウトはフロントエンド側でだけ意味を持ちます。Tarpitタイムアウトは両側で使用できます。期待する結果を得るには、タイムアウト値はゼロであってはなりません。リスナーでこのアクションを使用すると、フロントエンドのコンテキストで評価します。そのため、バックエンド側のタイムアウトの独自の値を維持するのは、たとえばuse-backendルールなどによってストリームが別のバックエンドへ振り分けられない場合だけです。振り分けられる場合は、選択したバックエンドのデフォルト値を設定します。

例：

```text
http-request set-timeout tunnel 5s
http-request set-timeout server req.hdr(host),map_int(host.lst)
```

例：

```text
http-response set-timeout tunnel 5s
http-response set-timeout server res.hdr(X-Refresh-Seconds),mul(1000)
```

例：

```text
defaults
  # This will set both tarpit and queue timeout to 5s as they are not
  # defined
  timeout connect 5s
  timeout client 30s
  timeout server 30s

listen foo
  # This will only change the connect timeout to 10s without affecting
  # queue or tarpit timeouts
  http-request set-timeout connect 10s
```

<a id="entry-4-4-set-tos"></a>

**`set-tos <tos> (deprecated)`**

```haproxy
set-tos <tos> (deprecated)
```

これは"set-fc-tos"のエイリアスです（代わりにこちらを使用することを推奨します）。

<a id="entry-4-4-set-uri"></a>

**`set-uri <fmt>`**

```haproxy
set-uri <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

リクエストURIを、形式文字列`<fmt>`の評価結果で書き換えます。スキーム、authority、パス、クエリー文字列をすべて一度に置き換えます。プロキシの手前でホストを書き換えたり、パスとクエリー文字列の間で一部を移動するなど、URIに複雑な変更を行ったりするために使用できます。絶対URIを設定すると、HTTP/1.1サーバーへそのまま送信します。それが意図した動作でない場合、ホスト、パス、クエリー文字列のいずれか、または複数を個別に設定することを推奨します。"http-request set-path"と"http-request set-query"も参照してください。

<a id="entry-4-4-set-var"></a>

**`set-var(<var-name>[,<cond>...]) <expr>`**

```haproxy
set-var(<var-name>[,<cond>...]) <expr>
set-var-fmt(<var-name>[,<cond>...]) <fmt>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

変数の内容を設定するために使用します。変数はインラインで宣言されます。

引数：

```text
<var-name>   変数の名前です。親ストリームの変数は設定できません。
             詳細は、変数について説明するセクション2.8を参照してください。

 <cond>      変数を実際に設定するために、すべて真でなければならない条件の集合です
             （"ifnotempty"、"ifgt"など）。指定可能な条件の完全な一覧は、
             set-varコンバーターの説明を参照してください。

 <expr>      サンプル取得の後にコンバーターを続けた、標準的なHAProxyの式です。

 <fmt>       カスタムログ形式の規則で表した値です
             （セクション8.2.6のカスタムログ形式を参照）。
```

HTTPルールではすべてのスコープを使用できますが、"tcp-request connection"や"tcp-request session"のように内容へアクセスできないルールセットでは、"proc"と"sess"スコープだけを使用できます。

例：

```text
http-request set-var(req.my_var) req.fhdr(user-agent),lower
http-request set-var-fmt(txn.from) %[src]:%[src_port]

```

<a id="entry-4-4-silent-drop"></a>

**`silent-drop [ rst-ttl <ttl> ]`**

```haproxy
silent-drop [ rst-ttl <ttl> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| -

ルールの評価を停止し、クライアントへ通知しないようにするシステム依存の方法で、クライアント側の接続を突然消滅させます。rst-ttl引数なしで呼び出した場合は、TCP_REPAIRを使い、クライアントにFINやRSTパケットを返さずに済むよう試みます。これに失敗した場合（主に権限不足によるもの）は、TTLを1にしたRSTパケットを送る方法に切り替えます。

これにより、HAProxyには接続が存在しなくても、クライアントからは引き続き接続が確立しているように見え、リソースを節約できます。ただし、HAProxyとクライアントの間にあるステートフルな機器（ファイアウォール、プロキシ、ロードバランサー）も、セッションテーブル内に確立済みの接続を維持します。

オプションのrst-ttlは、この動作を変更します。TCP_REPAIRを使用せず、設定可能なTTLを持つRSTパケットを送信します。適切な値を設定すると、RSTパケットはローカルのインフラストラクチャーを通過して、ファイアウォールやほかのシステム内の接続を削除しますが、クライアントに到達する前に消失します。その後のクライアントからのパケットは、手前の機器ですでに破棄されるようになります。これらのローカルRSTはローカルのリソースを保護しますが、クライアントのリソースは保護しません。この操作の影響を十分に理解していない限り、使用してはなりません。

<a id="entry-4-4-strict-mode"></a>

**`strict-mode { on | off }`**

```haproxy
strict-mode { on | off }
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| X

後続のルールに対して、厳密な書き換えモードを有効または無効にします。これより前に宣言したルールには影響せず、リクエストを書き換えるルールだけに適用されます。厳密モードが有効な場合、書き換えに何らかの失敗があると内部エラーを発生させます。無効な場合、こうしたエラーは通知せずに無視します。厳密な書き換えモードの目的は、一部の書き換えを任意にする一方、リクエスト処理を続行するために必須の書き換えも指定できるようにすることです。

既定では、厳密な書き換えモードが有効です。この値は、ルールセットの評価が終わるとリセットされます。たとえば、フロントエンドでモードを変更しても、HAProxyがバックエンドのルール評価を開始すると、既定のモードに戻ります。

<a id="entry-4-4-switch-mode-http"></a>

**`switch-mode http [ proto <name> ]`**

```haproxy
switch-mode http [ proto <name> ]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| - \| - \| -

このアクションは、接続をアップグレードします。現在対応しているのはHTTPへのアップグレードだけです。プロトコルは任意で指定できます。このアクションを使用できるのは、フロントエンド機能を持つプロキシだけです。接続のアップグレードは直ちに実行され、後続の"tcp-request content"ルールは評価しません。バックエンドのモードに依存する暗黙のアップグレードよりも、この方法を優先することを推奨します。この方法を使用すると、警告を出さずにフロントエンドへHTTPディレクティブを設定できます。これらのディレクティブは、HTTPへのアップグレードが実行された場合に条件付きで評価されます。ただし、HTTPバックエンドを選択しなければならないことに変わりはありません。HTTP接続をTCPサーバーへ振り分けることは、アップグレードしたかどうかにかかわらず、引き続き対応していません。

HTTPアップグレードの詳細は、プロキシに関する[セクション4](/ja/haproxy/proxies/)を参照してください。

<a id="entry-4-4-tarpit"></a>

**`tarpit [ { status | deny_status } <code>] [content-type <type>]`**

```haproxy
tarpit [ { status | deny_status } <code>] [content-type <type>]
       [ { default-errorfiles | errorfile <file> | errorfiles <name> |
```

           file `<file>` | lf-file `<file>` | string `<str>` | lf-string `<fmt>` } ]
       [ hdr `<name>` `<fmt>` ]*

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

ルールの評価を停止し、"timeout tarpit"で指定した待機時間（未設定の場合は"timeout connect"）の間、応答せずにリクエストを直ちにブロックします。その時間が経過してもクライアントが接続している場合、tarpitの対象になったと気付かれないよう、レスポンスを返します。ログには"PT"フラグを記録します。tarpitルールの目的は、同時リクエスト数に制限のあるロボットを、攻撃中に遅くすることです。非常に単純なロボットに対しては大きな効果が得られる場合があり、"deny"ルールと比べてファイアウォールの負荷を大幅に減らします。しかし、"正しく"開発されたロボットに対しては、HAProxyと手前のファイアウォールに膨大な数の同時接続を処理させることになり、状況が悪化する可能性があります。デフォルトではHTTP 500エラーを返します。ただし、レスポンスは"http-request return"ルールと同じ構文でカスタマイズできます。詳細は"http-request return"を参照してください。

互換性のため、引数が定義されていない場合、または"deny_status"だけが指定されている場合は、"default-errorfiles"引数が暗黙に指定されます。つまり、"http-request tarpit [deny_status `<status>`]"は"http-request tarpit [status `<status>`] default-errorfiles"の別名です。これ以降の"http-request"ルールは評価されません。"http-request return"と"http-request silent-drop"も参照してください。

<a id="entry-4-4-track-sc0"></a>

**`track-sc0 <key> [table <table>]`**

```haproxy
track-sc0 <key> [table <table>]
track-sc1 <key> [table <table>]
track-sc2 <key> [table <table>]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| -
\| X \| X \| -

現在のリクエストから、スティッキーカウンターの追跡を有効にします。これらのルールは評価を停止せず、デフォルトのアクションも変更しません。同じ接続で同時に追跡できるカウンター数は、グローバル設定の"tune.stick-counters"で指定します。ビルド時にMAX_SESS_STKCTRを設定している場合、その値がデフォルトになり（haproxy -vvで表示されます）、設定していない場合のデフォルトは3です。そのため、track-scの番号は0から(tune.stick-counters-1)までです。最初に実行する"track-sc0"ルールは、指定したテーブルのカウンターを1番目の組として追跡することを有効にします。最初に実行する"track-sc1"ルールは、指定したテーブルのカウンターを2番目の組として追跡することを有効にします。最初に実行する"track-sc2"ルールは、指定したテーブルのカウンターを3番目の組として追跡することを有効にします。1番目の組をフロントエンド単位のカウンターに、2番目の組をバックエンド単位のカウンターに使用することを推奨します。ただし、これは指針にすぎず、すべての組をどこでも使用できます。

引数：

```text
<key>   必須で、セクション7.3で説明するサンプル式のルールです。
        着信接続、リクエスト、またはレスポンスのどの要素を解析、抽出、結合し、
        カウンターを更新するテーブルエントリーの選択に使用するかを記述します。

<table> デフォルトのテーブルの代わりに使用する、省略可能なテーブルです。
        デフォルトは現在のプロキシで宣言したstick-tableです。指定すると、
        セッションが終了するまで、そのキーの一致と更新に関するすべてのカウンターの
        処理を、そのテーブルで行います。
```

"track-sc\*"ルールを実行すると、テーブル内でキーを検索し、見つからない場合はそのキー用のエントリーを割り当てます。その後、セッションの存続期間全体にわたって、そのエントリーへのポインターを保持します。エントリーのカウンターは、できるだけ頻繁に、セッションのカウンターを更新するたびに更新し、セッションの終了時にも必ず更新します。カウンターを更新するのは、追跡を開始した後に発生したイベントだけです。例外として、接続カウンターとリクエストカウンターは、有用な情報を反映するよう必ず更新します。

エントリーが同時接続数のカウンターを追跡する場合、そのエントリーを追跡している間は一つの接続として数えられ、その間エントリーが期限切れになることはありません。また、カウンターを追跡すると、それを使うすべてのACLチェックに対してテーブル検索が一回だけ行われるため、単にキーを確認する場合よりも性能面で有利です。

<a id="entry-4-4-unset-var"></a>

**`unset-var(<var-name>)`**

```haproxy
unset-var(<var-name>)
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| X \| X \| X \| X
\| X \| X \| X

変数の設定を解除します。`<var-name>`の詳細は、"set-var"アクションを参照してください。

例：

```text
http-request unset-var(req.my_var)

```

<a id="entry-4-4-use-service"></a>

**`use-service <service-name>`**

```haproxy
use-service <service-name>
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| X \| -
\| X \| - \| -

このアクションは、使用するルールセットに応じて、設定済みのTCPサービスまたはHTTPサービスを実行し、リクエストに応答します。このルールは終端となり、同じルールセット内の後続のルールは評価されません。

サービスは、有効なレスポンスを返すことも、何も応答せずに直ちに接続を閉じることもできます。HTTPサービスで有効な応答となるには、有効なHTTPレスポンスでなければなりません。HTTPサービス用のPrometheusエクスポーターなど、組み込みのサービスに加えて、Luaで独自のTCPサービスやHTTPサービスを記述することもできます。

引数：

```text
<service-name>  必須です。呼び出すサービスです。
```

例：

```text
http-request use-service prometheus-exporter if { path /metrics }

```

<a id="entry-4-4-wait-for-body-time"></a>

**`wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]`**

```haproxy
wait-for-body time <time> [ at-least <bytes> ] [use-large-buffer]
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| X \| -

次の条件のいずれかが成立するまで、リクエストまたはレスポンスの処理を遅らせます。

- リクエスト本文全体を受信した場合、処理は通常どおり進みます。
- "at-least"引数が指定され、`<bytes>`がゼロでない場合に、`<bytes>`バイトを受信したとき。この場合、処理は通常どおり進みます。
- リクエストバッファーがいっぱいになった場合。この場合、処理は通常どおり進みます。このバッファーのサイズは"tune.bufsize"オプションで決まります。
- リクエストが`<time>`ミリ秒を超えて待機した場合。この場合、HAProxyはクライアントに408 "Request Timeout"エラーを返し、リクエストの処理を停止します。ただし、ほかの条件のいずれかが先に成立した場合は、ボディ全体をまだ受信していなくても、このタイムアウトは発生しません。

通常のバッファーではメッセージのボディを格納するには小さすぎる場合、"use-large-buffer"オプションを設定して、大きなバッファーを割り当てることができます。使用するには、globalオプション"tune.bufsize.large"が定義されていなければなりません。

このアクションは、"option http-buffer-request"の代わりに使用できます。

引数：

```text
<time>    必須です。本文を待つ最大時間です。HAProxyの時間形式に従い、
          ミリ秒単位で表します。

<bytes>   省略可能です。待機を終了するために受信する必要があるペイロードの
          最小サイズです。HAProxyのサイズ形式に従い、バイト単位で表します。
          0（デフォルト）は制限なしを意味します。
```

例：

```text
http-request wait-for-body time 1s at-least 1k if METH_POST
```

参照："option http-buffer-request"、"tune.bufsize.large"。

<a id="entry-4-4-wait-for-handshake"></a>

**`wait-for-handshake`**

```haproxy
wait-for-handshake
```

使用可能なセクション： QUIC Ini\| TCP RqCon\| RqSes\| RqCnt\| RsCnt\| HTTP Req\| Res\| Aft - \| - \| - \| - \| -
\| X \| - \| -

SSLハンドシェイクが完了するまで、リクエストの処理を遅らせます。主に、early dataが有効だと確認できるまでその処理を遅らせるために役立ちます。
