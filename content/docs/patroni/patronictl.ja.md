---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "patronictl の設定、構文、およびサブコマンドに関するコマンド リファレンス。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/patroni/patronictl/]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
Patroni には [patronictl](/ja/docs/patroni/patronictl#patronictl) という名前のコマンドライン インターフェイスがあり、これは基本的に Patroni の REST API および DCS と対話するために使用されます。これは、クラスター内での操作の実行を容易にすることを目的としており、人間またはスクリプトで簡単に使用できます。

<a id="patronictl_configuration"></a>

--------

## 構成 {#configuration}

[patronictl](/ja/docs/patroni/patronictl#patronictl) は、構成の 3 セクションを使用します。

- **ctl**: Patroni REST API に対して認証する方法、およびサーバー ID を検証する方法。詳細については、[ctl設定](/ja/docs/patroni/config/yaml#patronictl_settings) を参照してください。
- **restapi**: Patroni REST API に対して認証する方法、およびサーバー ID を検証する方法。 `ctl` 構成が十分でない場合にのみ使用されます。 [patronictl](/ja/docs/patroni/patronictl#patronictl) は、主に `restapi.authentication` セクション (`ctl.authentication` が欠落している場合) と `restapi.cafile` 設定 (`ctl.cacert` が欠落している場合) に関係します。詳細については、[REST API 設定](/ja/docs/patroni/config/yaml#restapi_settings) を参照してください。
- DCS (例: **etcd**): Patroni によって使用される DCS に接続して認証する方法。

これらの構成オプションは、環境変数または構成ファイルから取得できます。 [環境構成の設定](/ja/docs/patroni/config/env#env) または [YAML 構成設定](/ja/docs/patroni/config/yaml#yaml) の上記のセクションを探して、環境変数または構成ファイルを通じてそれらのオプションを設定する方法を理解してください。

環境変数の使用を選択した場合、それは簡単なアプローチです。 Patronictl は環境変数を読み取り、その値を使用します。

構成ファイルの使用を選択した場合、使用するファイルについて [patronictl](/ja/docs/patroni/patronictl#patronictl) に通知するさまざまな方法があります。デフォルトでは、[patronictl](/ja/docs/patroni/patronictl#patronictl) は `patronictl.yaml` という名前の構成ファイルをロードしようとします。この構成ファイルは、システムに応じて次のパスのいずれかにあると想定されます。

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (ローミング): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (ローミングなし): `C:\Users\<user>\AppData\Local\patroni`

次のいずれかの方法でその動作をオーバーライドできます。

- カスタム構成ファイルへのパスを使用して環境変数 `PATRONICTL_CONFIG_FILE` を設定します。
- [patronictl](/ja/docs/patroni/patronictl#patronictl) の `-c` / `--config-file` コマンドライン引数をカスタム構成ファイルへのパスとともに使用します。

> [!NOTE]
> `patroni` デーモンが実行されているのと同じホストで [patronictl](/ja/docs/patroni/patronictl#patronictl) を実行している場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) に必要なすべての構成セクションがファイルに含まれていれば、同じ構成ファイルを使用することができます。

<a id="patronictl_usage"></a>

--------

## 使用法 {#usage}

[patronictl](/ja/docs/patroni/patronictl#patronictl) は、いくつかの便利な操作を公開します。このセクションでは、それぞれについて説明することを目的としています。

[patronictl](/ja/docs/patroni/patronictl#patronictl) の各サブコマンドに入る前に、[patronictl](/ja/docs/patroni/patronictl#patronictl) 自体に次のコマンドライン引数があることに注意してください。

`-c` / `--config-file` 前に説明したように、[patronictl](/ja/docs/patroni/patronictl#patronictl) の構成ファイルへのパスを提供するために使用されます。

`-d` / `--dcs-url` / `--dcs` Patroni によって使用される DCS に接続文字列を提供します。

この引数は、[patronictl](/ja/docs/patroni/patronictl#patronictl) 構成から DCS および `namespace` 設定をオーバーライドするか、構成に欠落している場合に定義するために使用できます。

値は `DCS://HOST:PORT/NAMESPACE` の形式である必要があります。たとえば、`localhost` 上で実行されている etcd v3 に、Patroni クラスターが `service` 名前空間に格納された状態で接続するには、`etcd3://localhost:2379/service` を指定します。引数の値に欠落している部分は、構成に存在する値またはそのデフォルトに置き換えられます。

`-k` / `--insecure` REST API サーバー SSL 証明書の検証をバイパスするフラグ。

これは、[patronictl](/ja/docs/patroni/patronictl#patronictl) からコマンドを実行するための概要です。

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> これは概要の構文です。
>
> - 角括弧内のオプションは省略可能です。
> - 中括弧内のオプションは、「セットの 1 つを選択する」操作を表します。
> - `[, ... ]` が付いたオプションは複数回指定できます。
> - 大文字で書かれたものは、値を与える必要があるリテラルを表します。
>
> 次のサブセクションで [patronictl](/ja/docs/patroni/patronictl#patronictl) サブコマンドを説明するときに、これと同じ構文を使用します。また、以下のサブセクションでサブコマンドを説明する場合、コマンドの概要は、上記の概要の `SUBCOMMAND` を置き換えるものと見なす必要があります。

次のサブセクションでは、[patronictl](/ja/docs/patroni/patronictl#patronictl) によって実装される各コマンドの説明を見つけることができます。例として、Patroni の GitHub リポジトリに存在する構成ファイル (ファイル `postgres0.yml`、`postgres1.yml`、および `postgres2.yml`) を使用します。

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### 書式 {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### 説明 {#description}

`patronictl demote-cluster` は、通常の Patroni クラスターを [スタンバイ クラスター](/ja/docs/patroni/standby_cluster#standby_cluster) に変換します。

このコマンドは、提供されたリモート プライマリー接続オプションから構築された `standby_cluster` セクションを使用して動的構成にパッチを適用し、リーダーがスタンバイ リーダーとして実行されるまで待機します。 構成を変更する前に現在のクラスター トポロジを出力します。 `--force` が使用されていない場合は確認を求めます。

`--host`、`--port`、または `--restore-command` の少なくとも 1 つを指定する必要があります。

<a id="patronictl_demote_cluster_parameters"></a>

#### パラメータ {#parameters}

`CLUSTER_NAME`: Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--host`: リモート ノードのアドレス。

`--port`: リモート ノードのポート。

`--restore-command`: リモート プライマリーから WAL レコードを復元するコマンド。

`--primary-slot-name`: レプリケーションに使用するリモート ノード上のレプリケーション スロットの名前。

`--force`: クラスターを降格するときに確認プロンプトをスキップするフラグ。

スクリプトに便利です。

<a id="patronictl_demote_cluster_examples"></a>

#### 例 {#examples}

クラスターをリモートのプライマリー エンドポイントに従うスタンバイ クラスターに降格します。

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### 書式 {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### 説明 {#description-1}

`patronictl dsn` は、Patroni クラスターの 1 つのメンバーの接続文字列を取得します。

複数のメンバーがこのコマンドのパラメーターに一致する場合、プライマリー ノードを優先してそのうちの 1 つが選択されます。

<a id="patronictl_dsn_parameters"></a>

#### パラメータ {#parameters-1}

`CLUSTER_NAME`: Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`-r` / `--role` 指定されたロールを持つメンバーを選択します。

役割は次のいずれかになります。

- `leader`: 通常の Patroni クラスターまたはスタンバイ Patroni クラスターのリーダー。または
- `primary`: 通常の Patroni クラスターのリーダー。または
- `standby-leader`: スタンバイ Patroni クラスターのリーダー。または
- `replica`: Patroni クラスターのレプリカ。または
- `standby`: `replica` と同じ。または
- `any`: 任意のロール。このパラメータを省略した場合と同じです。または

`-m` / `--member` 指定された名前を持つクラスターのメンバーを選択します。

`MEMBER_NAME` はメンバーの名前です。

`--group` 指定された Citus グループに属するメンバーを選択します。

`CITUS_GROUP` は、Citus グループの ID です。

<a id="patronictl_dsn_examples"></a>

#### 例 {#examples-1}

プライマリー ノードの DSN を取得します。

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

`postgresql1` という名前のノードの DSN を取得します。

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### 書式 {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### 説明 {#description-2}

`patronictl edit-config` はクラスターの動的構成を変更し、それによって DCS を更新します。

> [!NOTE]
> TTY を通じて呼び出される場合、コマンドはページャーを通じて動的構成の差分を表示しようとします。デフォルトでは、`less` または `more` のいずれかを使用しようとします。別のページャーが必要な場合は、`PAGER` 環境変数を目的のページャーに設定します。

<a id="patronictl_edit_config_parameters"></a>

#### パラメータ {#parameters-2}

`CLUSTER_NAME`: Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループの動的構成を変更します。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`citus.group` 構成が存在する場合は、そこからそれを取得しようとします。

`CITUS_GROUP` は、Citus グループの ID です。

`-q` / `--quiet` 構成の差分の表示をスキップするフラグ。

`-s` / `--set` 指定された動的構成オプションを指定された値で設定します。

`CONFIG` は、YAML ツリー内の動的構成パスの名前であり、レベルは `.` で結合されます。

`VALUE` は `CONFIG` の値です。 `null` の場合、`CONFIG` は動的構成から削除されます。

`-p` / `--pg` 指定された動的 Postgres 構成オプションを指定された値で設定します。

これは本質的に、`-s` / `--set` の短縮形であり、`CONFIG` の先頭に `postgresql.parameters.` が付加されます。

`PG_CONFIG` は、設定する Postgres 構成の名前です。

`PG_VALUE` は `PG_CONFIG` の値です。 `null` の場合、`PG_CONFIG` は動的構成から削除されます。

`--apply` 指定されたファイルから動的構成を適用します。

これは、`CONFIG_FILE` の構成ごとに 1 つずつ、複数の `-s` / `--set` オプションを指定するのと似ています。

`CONFIG_FILE` は、適用する動的構成を含むファイルへのパス (YAML 形式) です。 `stdin` から読み取りたい場合は、`-` を使用します。

`--replace` DCS の動的構成を、指定されたファイルで指定された動的構成に置き換えます。

`CONFIG_FILE` は、有効にする新しい動的構成を含むファイルへのパス (YAML 形式) です。 `stdin` から読み取りたい場合は、`-` を使用します。

`--force` 動的構成を変更するときに確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_edit_config_examples"></a>

#### 例 {#examples-2}

`max_connections` Postgres GUC を変更します。

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

`loop_wait` および `ttl` 設定を変更します。

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

`maximum_lag_on_failover` 設定を動的構成から削除します。

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### 書式 {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### 説明 {#description-3}

`patronictl failover` は、クラスター内で手動フェイルオーバーを実行します。

これは、クラスターが正常でない場合に使用するように設計されています。例:

- リーダーはいません。または
- 同期クラスターでは使用できる同期スタンバイはありません。

同期モードが有効な場合は、非同期ノードにフェイルオーバーすることもできます。

> [!NOTE]
> 正常なクラスターで `patronictl failover` を実行することを妨げるものはありません。ただし、そのような場合には `patronictl switchover` を使用することをお勧めします。

> [!WARNING]
> フェイルオーバーをトリガーすると、プロモートされたレプリカがプライマリーと比較してどの程度最新であるかによって、データ損失が発生する可能性があります。

<a id="patronictl_failover_parameters"></a>

#### パラメータ {#parameters-3}

`CLUSTER_NAME`: Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループでフェイルオーバーを実行します。

`CITUS_GROUP` は、Citus グループの ID です。

`--candidate` フェイルオーバー時に昇格されるノード。

`CANDIDATE_NAME` は、昇格するノードの名前です。

`--force` フェイルオーバーの実行時に確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_failover_examples"></a>

#### 例 {#examples-3}

ノード `postgresql2` にフェイルオーバーします。

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### 書式 {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### 説明 {#description-4}

`patronictl flush` は、スケジュールされたイベントがあればそれを破棄します。

<a id="patronictl_flush_parameters"></a>

#### パラメータ {#parameters-4}

`CLUSTER_NAME` Patroni クラスターの名前。

`MEMBER_NAME` 指定された Patroni メンバーのスケジュールされたイベントを破棄します。

複数のメンバーを指定できます。メンバーが指定されていない場合は、すべてのメンバーが考慮されます。

> [!NOTE]
> スケジュールされた再起動イベントを破棄する場合にのみ使用されます。

`restart` スケジュールされた再起動イベントを破棄します。

`switchover` スケジュールされたスイッチオーバー イベントを破棄します。

`--group` 指定された Citus グループからスケジュールされたイベントを破棄します。

`CITUS_GROUP` は、Citus グループの ID です。

`-r` / `--role` 指定されたロールを持つメンバーのスケジュールされたイベントを破棄します。

役割は次のいずれかになります。

- `leader`: 通常の Patroni クラスターまたはスタンバイ Patroni クラスターのリーダー。または
- `primary`: 通常の Patroni クラスターのリーダー。または
- `standby-leader`: スタンバイ Patroni クラスターのリーダー。または
- `replica`: Patroni クラスターのレプリカ。または
- `standby`: `replica` と同じ。または
- `any`: 任意のロール。このパラメータを省略した場合と同じです。

> [!NOTE]
> スケジュールされた再起動イベントを破棄する場合にのみ使用されます。

`--force` フラッシュの実行時に確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_flush_examples"></a>

#### 例 {#examples-4}

スケジュールされたスイッチオーバー イベントを破棄します。

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

すべてのスタンバイ ノードのスケジュールされた再起動を破棄します。

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

ノード `postgresql0` および `postgresql1` のスケジュールされた再起動を破棄します。

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### 書式 {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### 説明 {#description-5}

`patronictl history` は、クラスターからのフェイルオーバーおよびスイッチオーバー イベントの履歴を表示します (存在する場合)。

出力には次の情報が含まれます。

`TL` イベントが発生した時点の Postgres タイムライン。

`LSN` イベントが発生した時点の Postgres LSN。

`Reason` Postgres `.history` ファイルから取得された理由。

`Timestamp` イベントが発生した時刻。

`New Leader` イベント中に昇格した Patroni メンバー。

<a id="patronictl_history_parameters"></a>

#### パラメータ {#parameters-5}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループからのイベントの履歴を表示します。

`CITUS_GROUP` は、Citus グループの ID です。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`citus.group` 構成が存在する場合は、そこからそれを取得しようとします。

`-f` / `--format` 出力内のイベントのリストをフォーマットする方法。

形式は次のいずれかになります。

- `pretty`: 履歴を美しいテーブルとして出力します。または
- `tsv`: `\t` で区切られた列を含む表形式の情報として履歴を出力します。または
- `json`: 履歴を JSON 形式で出力します。または
- `yaml`: YAML 形式で履歴を出力します。

デフォルトは `pretty` です。

<a id="patronictl_history_examples"></a>

#### 例 {#examples-5}

イベントの履歴を表示します。

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

イベントの履歴を YAML 形式で表示します。

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### 書式 {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### 説明 {#description-6}

`patronictl list` は、Patroni クラスターとそのメンバーに関する情報を示します。

出力には次の情報が含まれます。

`Cluster` Patroni クラスターの名前。

`Member` Patroni メンバーの名前。

`Host` メンバーが配置されているホスト。

`Role` メンバーの現在の役割。

次のいずれかになります:

- `Leader`: 通常の Patroni クラスターの現在のリーダー。または
- `Standby Leader`: Patroni スタンバイ クラスターの現在のリーダー。または
- `Sync Standby`: 同期モードが有効になっている Patroni クラスターの同期スタンバイ。または
- `Replica`: Patroni クラスターの通常のスタンバイ。

`State` Patroni メンバーの Postgres の現在の状態。

考えられる状態の例をいくつか示します。

- `running`: Postgres が現在稼働している場合。
- `streaming`: レプリカであり、Postgres が現在プライマリー ノードから WAL をストリーミングしている場合。
- `in archive recovery`: レプリカであり、Postgres が現在アーカイブから WAL をフェッチしている場合。
- `stopped`: Postgres がシャットダウンされていた場合。
- `crashed`: Postgres がクラッシュした場合。

`TL` Patroni メンバー内の現在の Postgres タイムライン。

`Receive LSN` メンバーのストリーミング レプリケーションによって受信され、ディスクに同期された最後の先行書き込みログの場所 (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`)。

`Receive Lag` メンバーの `Receive LSN` 位置とその上流との間のレプリケーション ラグ (MB 単位)。

`Replay LSN` メンバーのリカバリ中に再生された最後の先行書き込みログの場所 (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`)。

`Replay Lag` メンバーの `Replay LSN` 位置とその上流との間のレプリケーション ラグ (MB 単位)。

それに加えて、次の情報が出力に含まれる場合があります。

`System identifier` Postgres システム識別子。

> [!NOTE]
> テーブルヘッダーに表示されます。
>
> 出力形式が `pretty` の場合にのみ表示されます。

`Group` Citus グループ ID。

> [!NOTE]
> テーブルヘッダーに表示されます。
>
> Citus クラスターの場合にのみ表示されます。

`Pending restart` `*` は、一部の Postgres 構成を有効にするためにノードの再起動が必要であることを示します。空の値は、ノードを再起動する必要がないことを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> 次の場合に表示されます。
>
> - `pretty` または `tsv` 形式で出力し、拡張出力が有効な場合。または
> - ノードの再起動が必要な場合。

`Scheduled restart` Patroni メンバーによって管理される Postgres インスタンスの再起動がスケジュールされたタイムスタンプ。空の値は、メンバーにスケジュールされた再起動がないことを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> 次の場合に表示されます。
>
> - `pretty` または `tsv` 形式で出力し、拡張出力が有効な場合。または
> - ノードにスケジュールされた再起動がある場合。

`Tags` Patroni メンバーに設定されたタグが含まれます。空の値は、タグが設定されていないか、タグがデフォルト値で設定されていることを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> 次の場合に表示されます。
>
> - `pretty` または `tsv` 形式で出力し、拡張出力が有効な場合。または
> - ノードにカスタム タグ、またはデフォルト以外の値を持つデフォルト タグがある場合。

`Scheduled switchover` Patroni クラスターのスイッチオーバーがスケジュールされている場合のタイムスタンプ。

> [!NOTE]
> テーブルのフッターに表示されます。
>
> スケジュールされたスイッチオーバーがある場合にのみ表示され、出力形式は `pretty` です。

`Maintenance mode`

> クラスター監視が現在一時停止されている場合。
>
> > [!NOTE]
> > テーブルのフッターに表示されます。
> >
> > クラスターが一時停止されており、出力形式が `pretty` の場合にのみ表示されます。

<a id="patronictl_list_parameters"></a>

#### パラメータ {#parameters-6}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループのメンバーに関する情報を表示します。

`CITUS_GROUP` は、Citus グループの ID です。

`-e` / `--extended` 拡張情報を表示します。

値が空であっても、`Pending restart`、`Scheduled restart`、`Tags` 属性を強制的に表示します。

> [!NOTE]
> `pretty` および `tsv` 出力形式にのみ適用されます。

`-t` / `--timestamp` クラスターとそのメンバーに関する情報を出力する前にタイムスタンプを出力します。

`-f` / `--format` 出力内のクラスターメンバーのリストをフォーマットする方法。

形式は次のいずれかになります。

- `pretty`: クラスターメンバーを美しいテーブルとして出力します。または
- `tsv`: `\t` で区切られた列を含む表形式の情報としてクラスターメンバーを出力します。または
- `json`: クラスターメンバーを JSON 形式で出力します。または
- `yaml`: YAML 形式でクラスターメンバーを出力します。

デフォルトは `pretty` です。

`-W` 2 秒ごとに情報を自動的に更新します。

`-w` / `--watch` 指定した間隔で情報を自動的に更新します。

`TIME` は、更新間の間隔 (秒単位) です。

<a id="patronictl_list_examples"></a>

#### 例 {#examples-6}

クラスターに関する情報を`pretty` 形式で表示します。

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

拡張列を使用して、クラスターに関する情報を `pretty` 形式で表示します。

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

クラスターに関する情報を実行のタイムスタンプとともに YAML 形式で表示します。

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### 書式 {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### 説明 {#description-7}

`patronictl pause` は、Patroni クラスターを一時的にメンテナンス モードにし、自動フェイルオーバーを無効にします。

<a id="patronictl_pause_parameters"></a>

#### パラメータ {#parameters-7}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループを一時停止します。

`CITUS_GROUP` は、Citus グループの ID です。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`citus.group` 構成が存在する場合は、そこからそれを取得しようとします。

`--wait` すべての Patroni メンバーが一時停止されるまで待ってから、呼び出し元に制御を返します。

<a id="patronictl_pause_examples"></a>

#### 例 {#examples-7}

クラスターをメンテナンス モードにし、すべてのノードが一時停止されるまで待ちます。

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### 書式 {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### 説明 {#description-8}

`patronictl promote-cluster` は、スタンバイ クラスターを通常の Patroni クラスターに変換します。

このコマンドは、動的構成から `standby_cluster` セクションを削除し、リーダーがプライマリーとして実行されるまで待機します。 構成を変更する前に現在のクラスター トポロジを出力します。 `--force` が使用されていない場合は確認を求めます。

<a id="patronictl_promote_cluster_parameters"></a>

#### パラメータ {#parameters-8}

`CLUSTER_NAME`: Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--force`: クラスターを昇格するときに確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_promote_cluster_examples"></a>

#### 例 {#examples-8}

スタンバイ クラスターを通常の Patroni クラスターとして実行するように昇格します。

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### 書式 {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### 説明 {#description-9}

`patronictl query` は、Patroni クラスターのメンバーに対して SQL コマンドまたはスクリプトを実行します。

<a id="patronictl_query_parameters"></a>

#### パラメータ {#parameters-9}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループをクエリーします。

`CITUS_GROUP` は、Citus グループの ID です。

`-r` / `--role` 指定されたロールを持つメンバーを選択します。

役割は次のいずれかになります。

- `leader`: 通常の Patroni クラスターまたはスタンバイ Patroni クラスターのリーダー。または
- `primary`: 通常の Patroni クラスターのリーダー。または
- `standby-leader`: スタンバイ Patroni クラスターのリーダー。または
- `replica`: Patroni クラスターのレプリカ。または
- `standby`: `replica` と同じ。または
- `any`: 任意のロール。このパラメータを省略した場合と同じです。

`-m` / `--member` 指定された名前のメンバーを選択します。

`MEMBER_NAME` は、選択されるメンバーの名前です。

`-d` / `--dbname` 接続してクエリーを実行するデータベース。

`DBNAME` はデータベースの名前です。指定しない場合、デフォルトの `USERNAME` が使用されます。

`-U` / `--username` データベースに接続するユーザー。

`USERNAME` ユーザーの名前。指定しない場合、デフォルトは `patronictl query` を実行しているオペレーティング システム ユーザーになります。

`--password` 接続ユーザーのパスワードの入力を求めます。

Patroni は `libpq` を使用するため、代わりに `~/.pgpass` ファイルを作成するか、`PGPASSWORD` 環境変数を設定できます。

`--format` クエリーの出力をフォーマットする方法。

形式は次のいずれかになります。

- `pretty`: クエリー出力を美しいテーブルとして出力します。または
- `tsv`: `\t` で区切られた列を含む表形式の情報としてクエリー出力を出力します。または
- `json`: クエリー出力を JSON 形式で出力します。または
- `yaml`: クエリー出力を YAML 形式で出力します。

デフォルトは `tsv` です。

`-f` / `--file` クエリーを実行するコマンドのソースとしてファイルを使用します。

`FILE_NAME` はソース ファイルへのパスです。

`-c` / `--command` クエリーで指定された SQL コマンドを実行します。

`SQL_COMMAND` は、実行される SQL コマンドです。

`--delimiter` `tsv` 形式で情報を出力する場合の区切り文字。省略した場合は `\t`。

`-W` 2 秒ごとにクエリーを自動的に再実行します。

`-w` / `--watch` 指定された間隔でクエリーを自動的に再実行します。

`TIME` は、再実行の間隔 (秒単位) です。

<a id="patronictl_query_examples"></a>

#### 例 {#examples-9}

`postgres` ユーザーとして SQL コマンドを実行し、パスワードを要求します。

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

`postgres` ユーザーとして SQL コマンドを実行し、`libpq` 環境変数からパスワードを取得します。

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

SQL コマンドを実行し、2 秒ごとに `pretty` 形式で出力します。

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

データベース `test` で SQL コマンドを実行し、出力を YAML 形式で出力します。

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

メンバー `postgresql2` に対して SQL コマンドを実行します。

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

いずれかのスタンバイで SQL コマンドを実行します。

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### 書式 {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### 説明 {#description-10}

`patronictl reinit` は、Patroni クラスターのレプリカ メンバーによって管理される Postgres スタンバイ インスタンスを再構築します。

<a id="patronictl_reinit_parameters"></a>

#### パラメータ {#parameters-10}

`CLUSTER_NAME` Patroni クラスターの名前。

`MEMBER_NAME` Postgres インスタンスが再構築されるレプリカ メンバーの名前。

複数のレプリカ メンバーを指定できます。メンバーが指定されていない場合、コマンドは何も行いません。

`--group` 指定された Citus グループのレプリカ メンバーを再構築します。

`CITUS_GROUP` は、Citus グループの ID です。

`--wait` Postgres スタンバイ ノードの再初期化が完了するまで待ちます。

`--force` Postgres スタンバイ インスタンスを再構築するときに確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

`--from-leader` リーダーからベースバックアップを直接取得するためのフラグ。

<a id="patronictl_reinit_examples"></a>

#### 例 {#examples-10}

Patroni クラスターのすべてのレプリカ メンバーの再構築を要求し、すぐに呼び出し元に制御を返します。

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

`postgresql2` の再構築をリクエストし、完了するまで待ちます。

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

`postgresql2` の再構築をリクエストし、リーダーから直接ベースバックアップを取得します。

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### 書式 {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### 説明 {#description-11}

`patronictl reload` は、1 つ以上の Patroni メンバーのローカル構成のリロードを要求します。

また、何も変更されていない場合でも、管理対象の Postgres インスタンスで `pg_ctl reload` がトリガーされます。

<a id="patronictl_reload_parameters"></a>

#### パラメータ {#parameters-11}

`CLUSTER_NAME` Patroni クラスターの名前。

`MEMBER_NAME` 指定された Patroni メンバーのローカル構成のリロードを要求します。

複数のメンバーを指定できます。メンバーが指定されていない場合は、すべてのメンバーが考慮されます。

`--group` 指定された Citus グループのメンバーのリロードを要求します。

`CITUS_GROUP` は、Citus グループの ID です。

`-r` / `--role` 指定されたロールを持つメンバーを選択します。

役割は次のいずれかになります。

- `leader`: 通常の Patroni クラスターまたはスタンバイ Patroni クラスターのリーダー。または
- `primary`: 通常の Patroni クラスターのリーダー。または
- `standby-leader`: スタンバイ Patroni クラスターのリーダー。または
- `replica`: Patroni クラスターのレプリカ。または
- `standby`: `replica` と同じ。または
- `any`: 任意のロール。このパラメータを省略した場合と同じです。

`--force` ローカル構成のリロードを要求するときに確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_reload_examples"></a>

#### 例 {#examples-11}

Patroni クラスターのすべてのメンバーのローカル構成のリロードを要求します。

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### 書式 {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### 説明 {#description-12}

`patronictl remove` は、DCS からクラスターの情報を削除します。

インタラクティブなアクションです。

> [!WARNING]
> この操作は、DCS から Patroni クラスターの情報を破棄します。

<a id="patronictl_remove_parameters"></a>

#### パラメータ {#parameters-12}

`CLUSTER_NAME` Patroni クラスターの名前。

`--group` 指定された Citus グループに関連する Patroni クラスターに関する情報を削除します。

`CITUS_GROUP` は、Citus グループの ID です。

`-f` / `--format` 確認を求めるプロンプトが表示されるときに、出力内のメンバーのリストをフォーマットする方法。

形式は次のいずれかになります。

- `pretty`: メンバーを美しいテーブルとして出力します。または
- `tsv`: `\t` で区切られた列を含む表形式の情報としてメンバーを出力します。または
- `json`: メンバーを JSON 形式で出力します。または
- `yaml`: メンバーを YAML 形式で出力します。

デフォルトは `pretty` です。

<a id="patronictl_remove_examples"></a>

#### 例 {#examples-12}

Patroni クラスター `batman` に関する情報を DCS から削除します。

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### 書式 {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### 説明 {#description-13}

`patronictl restart` は、Patroni クラスターのメンバーによって管理される Postgres インスタンスの再起動を要求します。

再起動はすぐに実行することも、後で実行するようにスケジュールすることもできます。

<a id="patronictl_restart_parameters"></a>

#### パラメータ {#parameters-13}

`CLUSTER_NAME` Patroni クラスターの名前。

`--group` 指定された Citus グループに関連する Patroni クラスターを再起動します。

`CITUS_GROUP` は、Citus グループの ID です。

`-r` / `--role` 指定されたロールを持つメンバーを選択します。

役割は次のいずれかになります。

- `leader`: 通常の Patroni クラスターまたはスタンバイ Patroni クラスターのリーダー。または
- `primary`: 通常の Patroni クラスターのリーダー。または
- `standby-leader`: スタンバイ Patroni クラスターのリーダー。または
- `replica`: Patroni クラスターのレプリカ。または
- `standby`: `replica` と同じ。または
- `any`: 任意のロール。このパラメータを省略した場合と同じです。

`--any` 指定されたフィルターに一致するノードの中からランダムな 1 つのノードを再起動します。

`--pg-version` 管理対象 Postgres インスタンスのバージョンが指定されたバージョンより古いメンバーのみを選択します。

`PG_VERSION` は、比較する Postgres バージョンです。

`--pending` `Pending restart` のフラグが付いているメンバーのみを選択します。

`--timeout`: 指定されたタイムアウトを超えて再起動がかかる場合は再起動を中止し、問題がプライマリーにある場合はレプリカにフェイルオーバーします。

`TIMEOUT` は、再起動を中止するまでに待機する秒数です。

`--scheduled` 指定されたタイムスタンプで再起動が行われるようにスケジュールします。

`TIMESTAMP` は、再起動が行われるときのタイムスタンプです。明確な形式で、できればタイムゾーンを使用して指定してください。リテラル `now` を使用して、再起動をすぐに実行することもできます。

`--force` 再起動操作を要求するときに確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_restart_examples"></a>

#### 例 {#examples-13}

クラスターのすべてのメンバーをすぐに再起動します。

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

クラスターのランダムなメンバーをすぐに再起動します。

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

`2023-09-13T18:00-03:00` で再起動が行われるようにスケジュールします。

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### 書式 {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### 説明 {#description-14}

`patronictl resume` は、Patroni クラスターのメンテナンス モードを解除し、自動フェイルオーバーを再度有効にします。

<a id="patronictl_resume_parameters"></a>

#### パラメータ {#parameters-14}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループを再開します。

`CITUS_GROUP` は、Citus グループの ID です。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`citus.group` 構成が存在する場合は、そこからそれを取得しようとします。

`--wait` すべての Patroni メンバーの一時停止が解除されるまで待ってから、呼び出し元に制御を返します。

<a id="patronictl_resume_examples"></a>

#### 例 {#examples-14}

クラスターをメンテナンス モードから解除します。

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### 書式 {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### 説明 {#description-15}

`patronictl show-config` は、DCS に保存されているクラスターの動的構成を示します。

<a id="patronictl_show_config_parameters"></a>

#### パラメータ {#parameters-15}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループの動的構成を表示します。

`CITUS_GROUP` は、Citus グループの ID です。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`citus.group` 構成が存在する場合は、そこからそれを取得しようとします。

<a id="patronictl_show_config_examples"></a>

#### 例 {#examples-15}

クラスター `batman` の動的構成を表示します。

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### 書式 {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### 説明 {#description-16}

`patronictl switchover` はクラスター内でスイッチオーバーを実行します。

これは、クラスターが正常な場合に使用されるように設計されています。例:

- リーダーがいます。
- 同期クラスターでは使用可能な同期スタンバイがあります。

> [!NOTE]
> クラスターが正常でない場合は、代わりに `patronictl failover` に興味があるかもしれません。

<a id="patronictl_switchover_parameters"></a>

#### パラメータ {#parameters-16}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループでスイッチオーバーを実行します。

`CITUS_GROUP` は、Citus グループの ID です。

`--leader` / `--primary` スイッチオーバー時に降格されるリーダーを示します。

`LEADER_NAME` は、クラスター内の現在のリーダーの名前と一致させるべきです。

`--candidate` スイッチオーバー時に昇格され、プライマリーの役割を担うノード。

`CANDIDATE_NAME` は、昇格するノードの名前です。

`--scheduled` 指定されたタイムスタンプでスイッチオーバーが発生するようにスケジュールします。

`TIMESTAMP` は、スイッチオーバーが発生するときのタイムスタンプです。明確な形式で、できればタイムゾーンを使用して指定してください。リテラル `now` を使用してスイッチオーバーを即時に実行することもできます。

`--force` スイッチオーバーの実行時に確認プロンプトをスキップするためのフラグ。

スクリプトに便利です。

<a id="patronictl_switchover_examples"></a>

#### 例 {#examples-16}

ノード `postgresql2` にスイッチオーバーします。

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

`postgresql0` と `postgresql2` の間のスイッチオーバーが `2023-09-13T18:00:00-03:00` で発生するようにスケジュールします。

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### 書式 {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### 説明 {#description-17}

`patronictl topology` は、Patroni クラスターとそのメンバーに関する情報をツリー ビュー アプローチで表示します。

出力には次の情報が含まれます。

`Cluster` Patroni クラスターの名前。

> [!NOTE]
> テーブルヘッダーに表示されます。

`System identifier` Postgres システム識別子。

> [!NOTE]
> テーブルヘッダーに表示されます。

`Member` Patroni メンバーの名前。

> [!NOTE]
> この列の情報は、レプリケーション接続に関するメンバーのツリー ビューとして表示されます。

`Host` メンバーが配置されているホスト。

`Role` メンバーの現在の役割。

次のいずれかになります:

- `Leader`: 通常の Patroni クラスターの現在のリーダー。または
- `Standby Leader`: Patroni スタンバイ クラスターの現在のリーダー。または
- `Sync Standby`: 同期モードが有効になっている Patroni クラスターの同期スタンバイ。または
- `Replica`: Patroni クラスターの通常のスタンバイ。

`State` Patroni メンバーの Postgres の現在の状態。

考えられる状態の例をいくつか示します。

- `running`: Postgres が現在稼働している場合。
- `streaming`: レプリカであり、Postgres が現在プライマリー ノードから WAL をストリーミングしている場合。
- `in archive recovery`: レプリカであり、Postgres が現在アーカイブから WAL をフェッチしている場合。
- `stopped`: Postgres がシャットダウンされていた場合。
- `crashed`: Postgres がクラッシュした場合。

`TL` Patroni メンバー内の現在の Postgres タイムライン。

`Receive LSN` メンバーのストリーミング レプリケーションによって受信され、ディスクに同期された最後の先行書き込みログの場所 (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`)。

`Receive Lag` メンバーの `Receive LSN` 位置とその上流との間のレプリケーション ラグ (MB 単位)。

`Replay LSN` メンバーのリカバリ中に再生された最後の先行書き込みログの場所 (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`)。

`Replay Lag` メンバーの `Replay LSN` 位置とその上流との間のレプリケーション ラグ (MB 単位)。

それに加えて、次の情報が出力に含まれる場合があります。

`Group` Citus グループ ID。

> [!NOTE]
> テーブルヘッダーに表示されます。
>
> Citus クラスターの場合にのみ表示されます。

`Pending restart` `*` は、一部の Postgres 構成を有効にするためにノードの再起動が必要であることを示します。空の値は、ノードを再起動する必要がないことを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> ノードの再起動が必要な場合に表示されます。

`Scheduled restart` Patroni メンバーによって管理される Postgres インスタンスの再起動がスケジュールされたタイムスタンプ。空の値は、メンバーにスケジュールされた再起動がないことを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> ノードにスケジュールされた再起動がある場合に表示されます。

`Tags` Patroni メンバーに設定されたタグが含まれます。空の値は、タグが設定されていないか、タグがデフォルト値で設定されていることを示します。

> [!NOTE]
> メンバー属性として表示されます。
>
> ノードにカスタム タグがある場合、またはデフォルト以外の値を持つデフォルト タグがある場合に表示されます。

`Scheduled switchover` Patroni クラスターのスイッチオーバーがスケジュールされている場合のタイムスタンプ。

> [!NOTE]
> テーブルのフッターに表示されます。
>
> スケジュールされたスイッチオーバーがある場合にのみ表示されます。

`Maintenance mode`

> クラスター監視が現在一時停止されている場合。
>
> > [!NOTE]
> > テーブルのフッターに表示されます。
> >
> > クラスターが一時停止されている場合にのみ表示されます。

<a id="patronictl_topology_parameters"></a>

#### パラメータ {#parameters-17}

`CLUSTER_NAME` Patroni クラスターの名前。

指定しない場合、[patronictl](/ja/docs/patroni/patronictl#patronictl) は、`scope` 構成が存在する場合は、そこからそれを取得しようとします。

`--group` 指定された Citus グループのメンバーに関する情報を表示します。

`CITUS_GROUP` は、Citus グループの ID です。

`-W` 2 秒ごとに情報を自動的に更新します。

`-w` / `--watch` 指定した間隔で情報を自動的に更新します。

`TIME` は、更新間の間隔 (秒単位) です。

<a id="patronictl_topology_examples"></a>

#### 例 {#examples-17}

クラスター `batman` のトポロジを表示します -- `postgresql1` と `postgresql2` は `postgresql0` からレプリケートされています。

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### 書式 {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### 説明 {#description-18}

`patronictl version` は、[patronictl](/ja/docs/patroni/patronictl#patronictl) アプリケーションのバージョンを取得します。それに加えて、Patroni クラスターとそのメンバーに関するバージョン情報も含まれる場合があります。

<a id="patronictl_version_parameters"></a>

#### パラメータ {#parameters-18}

`CLUSTER_NAME` Patroni クラスターの名前。

`MEMBER_NAME` Patroni クラスターのメンバーの名前。

`--group` 指定された Citus グループを持つ Patroni クラスターを対象とします。

`CITUS_GROUP` は、Citus グループの ID です。

<a id="patronictl_version_examples"></a>

#### 例 {#examples-18}

[patronictl](/ja/docs/patroni/patronictl#patronictl) のバージョンのみを取得します。

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

[patronictl](/ja/docs/patroni/patronictl#patronictl) とクラスター `batman` のすべてのメンバーのバージョンを取得します。

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

[patronictl](/ja/docs/patroni/patronictl#patronictl) と、クラスター `batman` のメンバー `postgresql1` および `postgresql2` のバージョンを取得します。

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
