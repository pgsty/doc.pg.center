---
title: "PgBouncer コマンドの使用法"
linkTitle: "使用法"
weight: 30
description: "PgBouncer コマンドライン使用法および管理コンソール"
icon: fa-solid fa-bell-concierge
module: [PGBOUNCER]
categories: [タスク]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/doc/usage.md"
---

--------

## 概要 {#synopsis}

    pgbouncer [-d][-v][-u user] <pgbouncer.ini>
    pgbouncer -V|-h

Windows では、次のオプションが利用可能です：

    pgbouncer.exe [-v][-u user] <pgbouncer.ini>
    pgbouncer.exe -V|-h

Windows サービスの設定に追加で使用できるオプション：

    pgbouncer.exe --regservice   <pgbouncer.ini>
    pgbouncer.exe --unregservice <pgbouncer.ini>

--------

## 説明 {#description}

**pgbouncer** は PostgreSQL のコネクションプーラーです。任意の対象アプリケーションは、**pgbouncer** にあたかも PostgreSQL サーバーであるかのように接続できます。このとき、**pgbouncer** は実際のサーバーへの接続を作成するか、既存の接続を再利用します。

**pgbouncer** の目的は、PostgreSQL への新しい接続を開く際のパフォーマンスへの影響を低減することです。

接続プーリングのトランザクションセマンティクスを損なわないようにするため、**pgbouncer** は接続をローテーションする際に複数のプーリング方式をサポートしています。

セッションプーリング

: 最も丁寧な方法です。クライアントが接続すると、クライアントが接続を維持している間はそのクライアントにサーバー接続が割り当てられます。クライアントが切断すると、そのサーバー接続はプールに戻されます。これがデフォルトの方法です。

トランザクションプーリング

: クライアントにサーバー接続が割り当てられるのは、トランザクション中のみです。
    PgBouncer がトランザクションの終了を検知すると、サーバー接続はプールに戻されます。

ステートメントプーリング

: 最も積極的な方法です。クエリの実行が完了した直後に、サーバー接続はプールに戻されます。複数文のトランザクションは破損するため、このモードでは許可されません。

**pgbouncer** の管理インターフェースは、特別な「仮想」データベース **pgbouncer** に接続した際に利用可能ないくつかの新しい `SHOW` コマンドで構成されています。

バージョン 1.26.0 以降、PgBouncer はログイン時に `pgbouncer.version`、`pgbouncer.pool_mode`、`pgbouncer.max_prepared_statements` の `ParameterStatus` 値をクライアントに送信します。ドライバーはこれらの値を使用して PgBouncer を検出し、動作を適応させることができます。オプションの [`login_notify_message`](/ja/pgbouncer/config/#login_notify_message) 設定は、ログイン成功後にウェルカム NOTICE を送信します。

--------

## クイックスタート {#quick-start}

基本的な設定と使用方法は以下の通りです。

1. pgbouncer.ini ファイルを作成します。詳細は **pgbouncer(5)** を参照してください。簡単な例：

        [databases]
        template1 = host=localhost port=5432 dbname=template1

        [pgbouncer]
        listen_port = 6432
        listen_addr = localhost
        auth_type = md5
        auth_file = userlist.txt
        logfile = pgbouncer.log
        pidfile = pgbouncer.pid
        admin_users = someuser

2. 接続を許可するユーザーを記載した `userlist.txt` ファイルを作成します：

        "someuser" "same_password_as_in_server"

3. **pgbouncer** を起動します：

        $ pgbouncer -d pgbouncer.ini

4. アプリケーション（または **psql** クライアント）が PostgreSQL サーバーに直接接続するのではなく、
    **pgbouncer** に接続するようにしてください。

        $ psql -p 6432 -U someuser template1

5. **pgbouncer** を管理するには、特別な管理データベース **pgbouncer** に接続し、`SHOW HELP;` を実行して開始します：

        $ psql -p 6432 -U someuser pgbouncer
        pgbouncer=# SHOW HELP;
        NOTICE:  Console usage
        DETAIL:
          SHOW [HELP|CONFIG|DATABASES|POOLS|CLIENTS|SERVERS|SOCKETS|LISTS|VERSION|...]
          SET key = arg
          RELOAD
          PAUSE
          RESUME
          SHUTDOWN
          [...]

6. pgbouncer.ini ファイルに変更を加えた場合、次のように再読み込みできます：

        pgbouncer=# RELOAD;

--------

## コマンドラインスイッチ {#command-line-switches}

`-d`、`--daemon`
: バックグラウンドで実行します。これを行わない場合、プロセスはフォアグラウンドで実行されます。

    デーモンモードでは、`pidfile` に加えて `logfile` または `syslog` を設定する必要があります。バックグラウンドに移行後は、stderr へのログ出力は行われません。

    注意：Windows では動作しません。**pgbouncer** は Windows 上でサービスとして実行する必要があります。

`-u` _USERNAME_、`--user=` _USERNAME_
: 起動時に指定されたユーザーに切り替えます。

`-v`、`--verbose`
: 出力の詳細度を増加します。複数回使用できます。

`-q`、`--quiet`
: 静黙モード：stderr へのログ出力を抑制します。ログの詳細度には影響しません。stderr が使用されなくなるだけです。init.d スクリプトでの利用を想定しています。

`-V`、`--version`
: バージョンを表示。

`-h`、`--help`
: 短いヘルプを表示します。

`--regservice`
: Win32: PgBouncer を Windows サービスとして実行するように登録します。**service_name** 設定パラメーターの値が、登録時の名前として使用されます。

`--unregservice`
: Win32: Windows サービスの登録を解除します。

--------

## 管理コンソール {#admin-console}

管理コンソールは、データベース **pgbouncer** に通常通り接続することで利用できます。

    $ psql -p 6432 pgbouncer

設定パラメーター **admin_users** または **stats_users** にリストされたユーザーのみが、管理コンソールにログインできます（`auth_type=any` の場合は例外で、任意のユーザーが stats_user としてログインできます）。

さらに、ユーザー名 **pgbouncer** は、ログインが Unix ソケット経由で行われ、クライアントの Unix ユーザー UID が実行中のプロセスと同一の場合、パスワードなしでログインが許可されます。

管理コンソールは現在、シンプルなクエリプロトコルのみをサポートしています。
すべてのコマンドに拡張クエリプロトコルを使用するドライバは、これに対応していません。

### SHOW コマンド {#show-commands}

**SHOW** コマンドは情報を出力します。各コマンドの説明は以下の通りです。

#### SHOW STATS {#show-stats}

統計情報を表示します。このコマンドおよび関連コマンドでは、合計値はプロセス起動以降の値であり、平均値は `stats_period` ごとに更新されます。

database
: 統計情報はデータベースごとに表示されます。

total_xact_count
: **pgbouncer** がプールしている SQL トランザクションの合計数。

total_query_count
: **pgbouncer** がプールしている SQL コマンドの合計数。

total_server_assignment_count
: サーバーがクライアントに割り当てられた合計回数

total_received
: **pgbouncer** が受信したネットワークトラフィックの合計バイト数。

total_sent
: **pgbouncer** が送信したネットワークトラフィックの合計バイト数。

total_xact_time
: **pgbouncer** が PostgreSQL に接続してトランザクション（トランザクション内でのアイドル状態またはクエリの実行のいずれか）に費やした合計マイクロ秒数。

total_query_time
: **pgbouncer** が PostgreSQL にアクティブに接続してクエリを実行している間に費やした合計マイクロ秒数。

total_wait_time
: クライアントがサーバー接続を待つ時間（マイクロ秒単位）。クライアント接続がバックエンド接続に割り当てられたときに更新されます。

total_client_parse_count
: クライアントが作成したプリペアドステートメントの合計数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

total_server_parse_count
: サーバー上で **pgbouncer** が作成したプリペアドステートメントの合計数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

total_bind_count
: クライアントが実行準備を済ませ、**pgbouncer** が PostgreSQL に転送したプリペアドステートメントの合計数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

total_client_login_count
: 成功したクライアントログインの合計数。

avg_xact_count
: 直近の統計期間における 1 秒あたりの平均トランザクション数。

avg_query_count
: 直近の統計期間における 1 秒あたりの平均クエリ数。

avg_server_assignment_count
: 直近の統計期間における、サーバーがクライアントに割り当てられた 1 秒あたりの平均回数。

avg_recv
: クライアントからの平均受信バイト数（1 秒あたり）。

avg_sent
: クライアントへの平均送信バイト数（1 秒あたり）。

avg_xact_time
: 平均トランザクション実行時間（マイクロ秒単位）。

avg_query_time
: 平均クエリ実行時間（マイクロ秒単位）。

avg_wait_time
: クライアントがサーバーを待つ時間（現在の `stats_period` の間にバックエンドに割り当てられたクライアントの待機時間の平均）をマイクロ秒単位で示します。

avg_client_parse_count
: クライアントが作成したプリペアドステートメントの 1 秒あたりの平均数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

avg_server_parse_count
: サーバー上で **pgbouncer** が作成したプリペアドステートメントの 1 秒あたりの平均数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

avg_bind_count
: クライアントが実行準備を済ませ、**pgbouncer** が PostgreSQL に転送したプリペアドステートメントの 1 秒あたりの平均数。名前付きプリペアドステートメント追跡モードでのみ適用されます。`max_prepared_statements` を参照してください。

avg_client_login_count
: 1 秒あたりの成功したクライアントログインの平均数。

#### SHOW STATS_TOTALS {#show-stats_totals}

**SHOW STATS** の **total_** フィールドに対応する、データベースごとの累積統計を表示します。出力の列名からは **total_** プレフィックスが省かれます。たとえば、**total_query_count** は **query_count** という列名になります。


#### SHOW STATS_AVERAGES {#show-stats_averages}

**SHOW STATS** のうち、平均値（**avg_**）を示すサブセット。

#### SHOW TOTALS {#show-totals}

**SHOW STATS** と同様ですが、すべてのデータベースにわたって集計されています。

#### SHOW SERVERS {#show-servers}

type
: S、サーバー用。

user
: **pgbouncer** がサーバーへの接続に使用するユーザー名。

database
: データベース名。

replication
: サーバー接続がレプリケーションを使用するかどうか。**none**、**logical**、**physical** のいずれかになります。

state
: PgBouncer サーバー接続の状態。以下のいずれか：**active**、
    **idle**、**used**、**tested**、**new**、**active_cancel**、
    **being_canceled**。

addr
: PostgreSQL サーバーの IP アドレス。

port
: PostgreSQL サーバーのポート。

local_addr
: ローカルマシン上の接続開始アドレス。

local_port
: ローカルマシン上の接続開始ポート。

connect_time
: 接続が確立された時。

request_time
: 最終リクエストが発行された時刻。

wait
: サーバー接続には使用されません。

wait_us
: サーバー接続には使用されません。

close_needed
: 設定ファイルの再読み込みや DNS 更新により接続情報が変更された場合、または **RECONNECT** が発行された場合に、接続ができるだけ早く閉じられるときは 1 になります。

ptr
: この接続に対する内部オブジェクトのアドレス。

link
: このサーバーが紐付けられているクライアント接続のアドレス。

remote_pid
: サーバーのバックエンドプロセスの PID。Unix ソケット経由で接続された場合、OS がプロセスID情報を取得できる場合はその OS の PID を使用する。そうでない場合は、サーバーが送信したキャンセルパケットから抽出する。PostgreSQL がサーバーの場合、これは PID であるべきだが、別の PgBouncer がサーバーの場合、ランダムな数値となる。

tls
: TLS 接続情報の文字列、TLS を使用しない場合は空。

application_name
: クライアント接続で設定された `application_name` を含む文字列、
    またはその設定が行われていない場合、または関連する接続が存在しない場合に空。

prepared_statements
: サーバー上で準備されたプリペアドステートメントの数。この数は `max_prepared_statements` 設定によって制限されます。

id
: サーバーの固有ID。


#### SHOW CLIENTS {#show-clients}

type
: C、クライアント用。

user
: クライアント接続ユーザー。

database
: データベース名。

replication
: クライアント接続がレプリケーションを使用するかどうか。**none**、**logical**、**physical** のいずれか。

state
: クライアント接続の状態。以下のいずれか：**active**（サーバー接続と紐づけられたクライアント接続）、**idle**（処理待ちのクエリのないクライアント接続）、**waiting**、**active_cancel_req**、または **waiting_cancel_req**。

addr
: クライアントの IP アドレス。

port
: クライアントのソースポート。

local_addr
: ローカルマシン上の接続終端アドレス。

local_port
: ローカルマシン上の接続終端ポート。

connect_time
: 接続時刻のタイムスタンプ。

request_time
: 最後のクライアント要求のタイムスタンプ。

wait
: 現在の待機時間（秒単位）。

wait_us
: 現在の待機時間のマイクロ秒部分。

close_needed
: クライアントには使用されません

ptr
: この接続に対する内部オブジェクトのアドレス。

link
: クライアントが紐付けられているサーバー接続のアドレス。

remote_pid
: クライアントが Unix ソケット経由で接続している場合、OS がプロセス ID を取得できる場合に限り、プロセス ID を表示します。

tls
: TLS 接続情報の文字列、TLS を使用しない場合は空。

application_name
: クライアントがこの接続で設定した `application_name` を含む文字列。設定されていない場合は空。

prepared_statements
: クライアントが準備したプリペアドステートメントの数

id
: クライアントの固有ID。

#### SHOW POOLS {#show-pools}

各 (database, user) の組に対して新しいプールエントリが作成されます。

database
: データベース名。

user
: ユーザー名。

cl_active
: サーバー接続に紐付けられているか、処理待ちのクエリがないアイドル状態にあるクライアント接続。

cl_waiting
: クエリを送信したが、まだサーバー接続を取得していないクライアント接続。

cl_active_cancel_req
: クエリのキャンセルをサーバーに転送済みで、サーバーの応答を待機しているクライアント接続。

cl_waiting_cancel_req
: まだクエリのキャンセルをサーバーに転送していないクライアント接続。

sv_active
: クライアントに紐付けられているサーバー接続。

sv_active_cancel
: 現在、キャンセル要求を転送中のサーバー接続。

sv_being_canceled
: 通常であればアイドル状態になれるはずのサーバーですが、このサーバー上のクエリをキャンセルするために送信された進行中のキャンセル要求がすべて完了するまで、アイドル状態への移行を待機しています。

sv_idle
: クライアントクエリに即座に利用可能な、使用されていないサーバー接続。

sv_used
: `server_check_delay` を超えてアイドル状態が続いているサーバー接続。再び使用するには、事前に `server_check_query` を実行する必要があります。

sv_tested
: 現在 `server_reset_query` または `server_check_query` を実行中のサーバー接続。

sv_login
: 現在ログイン処理中のサーバー接続。

maxwait
: キュー内の最初（最も古い）クライアントが待機した時間（秒単位）。
    この値が増加し始めた場合は、現在のサーバーのプールがリクエストを十分に迅速に処理できていないことを示します。
    原因は、サーバーの過負荷、または **pool_size** 設定が小さすぎることのいずれかの可能性があります。

maxwait_us
: 最大待機時間のマイクロ秒部分。

pool_mode
: 使用中のプーリングモード。

load_balance_hosts
: プールのホストにコンマ区切りのリストが含まれている場合、使用される load_balance_hosts。

#### SHOW PEER_POOLS {#show-peer_pools}

各設定されたピアごとに、新しい peer_pool エントリが作成されます。

peer_id
: 設定されたピアエントリの ID。

cl_active_cancel_req
: クエリのキャンセルをサーバーに転送済みで、サーバーの応答を待機しているクライアント接続。

cl_waiting_cancel_req
: まだクエリのキャンセルをサーバーに転送していないクライアント接続。

sv_active_cancel
: 現在、キャンセル要求を転送中のサーバー接続。

sv_login
: 現在ログイン処理中のサーバー接続。

#### SHOW LISTS {#show-lists}

次の内部リストとそれぞれの要素数を、リストごとに 1 行ずつ、**list** 列と **items** 列に表示します：

databases
: データベース数。

users
: ユーザー数。

peers
: 設定されたピアの数。

pools
: プール数。

peer_pools
: ピアプール数。

free_clients
: クライアントの空き数。切断されたクライアントであり、将来のクライアントの再利用のために割り当てられたメモリを保持しているため、メモリの再割り当てを回避できる。

used_clients
: 使用中のクライアント数。

login_clients
: **login** 状態のクライアント数。

free_servers
: 空きサーバーの数。これらのサーバーは切断されていますが、PgBouncer は将来のサーバー用に再利用できるよう、それらに割り当てられたメモリを保持しています。

used_servers
: 使用中のサーバー数。

dns_names
: キャッシュ内の DNS 名の数。

dns_zones
: キャッシュ内の DNS ゾーン数。

dns_queries
: 進行中の DNS クエリの数。

dns_pending
: 使用されません

#### SHOW USERS {#show-users}

name
: ユーザー名

pool_size
: ユーザーが上書きした pool_size。設定されていない場合は空文字列。

reserve_pool_size
: ユーザーの上書き設定による reserve_pool_size。設定されていない場合は空文字列。

pool_mode
: ユーザーが上書きした pool_mode の値、または設定されていない場合は NULL。

max_user_connections
: ユーザーの max_user_connections 設定。この特定のユーザーに対してこの設定が指定されていない場合、デフォルト値が表示されます。

current_connections
: このユーザーがすべてのサーバーに対して開いているサーバー接続の現在の数。

max_user_client_connections
: ユーザーの max_user_client_connections 設定。この特定のユーザーに対してこの設定が指定されていない場合、デフォルト値が表示されます。

current_client_connections
: このユーザーが PgBouncer に対して開いているクライアント接続の現在の数。

#### SHOW DATABASES {#show-databases}

name
: 設定されたデータベースエントリの名前。

host
: PgBouncer が接続するホスト。

port
: PgBouncer が接続するポート。

database
: PgBouncer が接続する実際のデータベース名。

force_user
: ユーザーが接続文字列に含まれている場合、クライアントユーザーに関係なく、PgBouncer と PostgreSQL の接続は指定されたユーザーに強制されます。

pool_size
: サーバー接続の最大数。

min_pool_size
: サーバー接続の最小数。

reserve_pool_size
: このデータベースに対する追加接続数の最大値。

server_lifetime
: このデータベースのサーバー接続の最大有効期間

pool_mode
: データベースの上書き pool_mode、またはデフォルトが使用される場合の NULL。

load_balance_hosts
: データベースの load_balance_hosts は、ホストにコンマ区切りのリストが含まれている場合に使用されます。

max_connections
: **max_db_connections** によって（グローバルまたはデータベースごとに）設定された、このデータベースに対して許可されるサーバー接続数の最大値。

current_connections
: このデータベースの現在のサーバー接続数。

max_client_connections
: このデータベースで許可されるクライアント接続の最大数。グローバルまたはデータベースごとの max_db_client_connections で設定された値。

current_client_connections
: このデータベースの現在のクライアント接続数。

paused
: このデータベースが現在一時停止されている場合は 1、それ以外の場合は 0。

disabled
: このデータベースが現在無効になっている場合は 1、それ以外の場合は 0。

#### SHOW PEERS {#show-peers}

peer_id
: 設定されたピアエントリの ID。

host
: PgBouncer が接続するホスト。

port
: PgBouncer が接続するポート。

pool_size
: このピアへのサーバー接続の最大数

#### SHOW SOCKETS, SHOW ACTIVE_SOCKETS {#show-sockets-show-active_sockets}

ソケット、またはアクティブなソケットのみに関する低レベルの情報を表示します。
これは **SHOW CLIENTS** および **SHOW SERVERS** で表示される情報に加えて、他のより低レベルな情報も含みます。

#### SHOW CONFIG {#show-config}

現在の設定値を1行に1つずつ表示し、以下の列を用います。

key
: 設定変数名

value
: 設定値

default
: 設定のデフォルト値

changeable
: **yes** または **no** で、変数を実行中に変更できるかどうかを示します。
    **no** の場合、変数は起動時のみ変更可能です。実行中に変更するには **SET** を使用します。

#### SHOW MEM {#show-mem}

さまざまな内部メモリ割り当ての現在のサイズに関する低レベルの情報を表示します。表示される情報は変更される可能性があります。

#### SHOW DNS_HOSTS {#show-dns_hosts}

DNS キャッシュ内のホスト名を表示します。

hostname
: ホスト名。

ttl
: 次回の照会までの秒数。

addrs
: コンマ区切りのアドレスリスト。

#### SHOW DNS_ZONES {#show-dns_zones}

キャッシュ内の DNS ゾーンを表示します。

zonename
: ゾーン名。

serial
: 現在のシリアル。

count
: このゾーンに属するホスト名。


#### SHOW VERSION {#show-version}

PgBouncer のバージョン文字列を表示します。

#### SHOW STATE {#show-state}

PgBouncer の状態設定を表示します。現在の状態は **active** と **paused** です。

### プロセス制御コマンド {#process-controlling-commands}

#### PAUSE [db] {#pause-db}

PgBouncer はすべてのサーバーとの接続を切断しようとします。各サーバー接続の切断は、サーバープールのプーリングモードに従って、その接続が解放されるのを待機します（トランザクションプーリングモードではトランザクションの完了まで、ステートメントモードではステートメントの完了まで、セッションプーリングモードではクライアントの切断まで待機します）。すべてのサーバー接続が切断されるまで、このコマンドは戻りません。データベースの再起動時に使用します。

データベース名が指定された場合、そのデータベースのみが一時停止されます。

一時停止されたデータベースへの新しいクライアント接続は、**RESUME** が呼び出されるまで待機します。

#### DISABLE db {#disable-db}

指定されたデータベースへの新しいクライアント接続をすべて拒否します。

#### ENABLE db {#enable-db}

前の **DISABLE** コマンドの後に新しいクライアント接続を許可します。

#### RECONNECT [db] {#reconnect-db}

指定されたデータベース、またはすべてのデータベースのオープンなサーバー接続を、（プーリングモードに従って）解放された後に閉じます。ライフタイムがまだ満了していなくても閉じられます。新しいサーバー接続はすぐに作成でき、プールサイズの設定に従って必要に応じて接続されます。

このコマンドは、サーバー接続の設定が変更された場合に有用です。たとえば、新しいサーバーへの段階的なスイッチオーバーを実行する際に使用します。pgbouncer.ini の接続文字列を変更して再読み込みした場合（**RELOAD** を参照）や、DNS 解決が変更された場合、このコマンドを実行する必要はありません。そのような場合、同様の処理が自動的に実行されるためです。このコマンドが必要となるのは、PgBouncer の下流で接続をルーティングしているものがある場合に限ります。

このコマンドを実行した後、一部のサーバー接続が古い宛先に、別のサーバー接続が新しい宛先に向かう状態が長期間続く可能性があります。これは、読み取り専用レプリカ間で読み取り専用トラフィックを切り替える場合や、マルチマスターレプリケーション構成のノード間で切り替える場合にのみ適切であると考えられます。すべての接続を同時に切り替える必要がある場合は、代わりに **PAUSE** が推奨されます。待機せずにサーバー接続を閉じる必要がある場合（たとえば、段階的なスイッチオーバーではなく緊急フェイルオーバーのシナリオ）は、**KILL** の検討もしてください。

#### KILL [db] {#kill-db}

指定されたデータベースまたはすべてのデータベース（管理データベースを除く）のすべてのクライアント接続とサーバー接続を即座に切断します。

KILL が実行されたデータベースへの新しいクライアント接続は、**RESUME** が呼び出されるまで待機します。

#### KILL_CLIENT id {#kill_client-id}

指定されたクライアント接続を、そのクライアントに対するすべてのサーバー接続とともに即座に切断します。切断対象のクライアントは、`SHOW CLIENTS` コマンドで確認できる `id` 値によって識別されます。

コマンドの例は `KILL_CLIENT 1234` のようになります。

#### RESUME [db] {#resume-db}

前の **KILL** または **PAUSE** コマンドからの作業を再開します。

#### SHUTDOWN {#shutdown}

PgBouncer プロセスは終了します。

#### SHUTDOWN WAIT_FOR_SERVERS {#shutdown-wait_for_servers}

新しい接続の受付を停止し、すべてのサーバーが解放された後にシャットダウンします。
これは **PAUSE** と **SHUTDOWN** を実行するのと基本的に同じですが、
**PAUSE** を待つ間も新しい接続の受付を停止し、
サーバー接続を待機しているクライアントを積極的に切断する点が異なります。
UNIX ソケットはシャットダウン中に開いたままになりますが、
PgBouncer 管理コンソールへの接続のみを受け付けます。

#### SHUTDOWN WAIT_FOR_CLIENTS {#shutdown-wait_for_clients}

新しい接続の受付を停止し、既存のすべてのクライアントが切断されたらプロセスをシャットダウンします。UNIX ソケットはシャットダウン中に開いたままになりますが、pgbouncer 管理コンソールへの接続のみを受け付けます。このコマンドは、以下の手順に従って2つの PgBouncer プロセスをゼロダウンタイムでローリング再起動する際に使用できます。

1. `so_reuseport` を使用して、同じポートで 2 つ以上の PgBouncer プロセスを実行します
    （[ピアリングの設定](/ja/pgbouncer/config/#section-peers)は推奨されますが、必須ではありません）。
    再起動時のダウンタイムをゼロにするため、これらのプロセスを 1 つずつ再起動します。これにより、1 つのプロセスを再起動している間も、他のプロセスが接続を受け入れ続けます。
2. 最初に再起動するプロセスを選択します。これを A と呼びます。
3. プロセス A に `SHUTDOWN WAIT_FOR_CLIENTS` を実行します（または `SIGTERM` を送信します）。
4. すべてのクライアントが再接続するようにします。クライアント側のプーラーが `server_idle_timeout`（または同様の設定）によって再接続を引き起こすまでしばらく待つことで実現できます。クライアント側のプーラーが使用されていない場合は、クライアントを再起動することで実現できます。すべてのクライアントが再接続すると、プロセス A は自動的に終了します。接続しているクライアントがもういないためです。
5. プロセス A を再度起動します。
6. 残りの各プロセスに対してステップ 3、4、5 を 1 つずつ繰り返し、すべてのプロセスを再起動するまで続けます。


#### RELOAD {#reload}

PgBouncer プロセスは設定ファイルを再読み込みし、変更可能な設定を更新します。これにはメイン設定ファイルおよび設定 `auth_file` と `auth_hba_file` で指定されたファイルが含まれます。

PgBouncer は、設定ファイルの再読み込みによってデータベース定義の接続パラメーターが変更されたことを検出します。既存のサーバー接続は、プーリングモードに従って次回接続を解放するタイミングで古い宛先に対して閉じられ、新しいサーバー接続は即座に更新された接続パラメーターを使用します。

#### WAIT_CLOSE [db] {#wait_close-db}

指定されたデータベースまたはすべてのデータベースのすべてのサーバー接続が "close_needed" 状態を解除するまで待機します（**SHOW SERVERS** を参照）。これは **RECONNECT** や **RELOAD** の後に呼び出すことで、たとえばスイッチオーバースクリプトで、それぞれの設定変更が完全に有効になるまで待機するために使用できます。

### その他のコマンド {#other-commands}

#### SET key = arg {#set-key--arg}

設定値を変更します（詳細は **SHOW CONFIG** を参照）。たとえば：

    SET log_connections = 1;
    SET server_check_query = 'select 2';

（このコマンドは PgBouncer 管理コンソールで実行され、PgBouncer の設定を変更します。**SET** コマンドを他のデータベースで実行しても、他の SQL コマンドと同様に PostgreSQL バックエンドに渡されます。）

### シグナル {#signals}

SIGHUP
: 設定の再読み込み。管理コンソール上で **RELOAD** コマンドを実行したのと同じです。

SIGTERM
: スーパーセーフシャットダウン。既存のすべてのクライアントの切断を待ちますが、新しい接続は受け付けません。これは管理コンソール上で **SHUTDOWN WAIT_FOR_CLIENTS** を実行することと同じです。シャットダウンがすでに進行中の状態でこのシグナルを受け取った場合、「スーパーセーフシャットダウン」の代わりに「即時シャットダウン」がトリガーされます。PgBouncer 1.23.0 より前のバージョンでは、このシグナルは「即時シャットダウン」を引き起こしていました。

SIGINT
: セーフシャットダウン。管理コンソールで **SHUTDOWN WAIT_FOR_SERVERS** を実行したのと同じです。
    シャットダウンがすでに進行中の間にこのシグナルを受け取った場合、「セーフシャットダウン」の代わりに「即時シャットダウン」がトリガーされます。

SIGQUIT
: 即時シャットダウン。管理コンソールで **SHUTDOWN** を実行したのと同じです。

SIGUSR1
: 管理コンソールで **PAUSE** を実行したのと同じです。

SIGUSR2
: 管理コンソールで **RESUME** を実行したのと同じです。

### Libevent 設定 {#libevent-settings}

Libevent のドキュメントより：

> 環境変数 EVENT_NOEPOLL、EVENT_NOKQUEUE、EVENT_NODEVPOLL、EVENT_NOPOLL または EVENT_NOSELECT をそれぞれ設定することで、epoll、kqueue、devpoll、poll または select のサポートを無効にできます。
>
> 環境変数 EVENT_SHOW_METHOD を設定すると、libevent は使用するカーネル通知メソッドを表示します。

--------

## 関連項目 {#see-also}

pgbouncer(5) - 設定項目の説明のマニュアルページ

<https://www.pgbouncer.org/>
