---
title: "Patroni REST API"
weight: 40
icon: fa-solid fa-book
description: "Patroni REST API エンドポイントと操作動作のリファレンス。"
module: [PATRONI]
categories: [リファレンス]
aliases: [/patroni/rest_api/]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
Patroni には豊富な REST API があり、リーダー レース中に Patroni 自体によって使用されたり、failovers/switchovers/reinitialize/restarts/reloads を実行するために [patronictl](/ja/docs/patroni/patronictl#patronictl) ツールによって使用されたり、HTTP ヘルス チェックを実行するために HAProxy またはその他の種類のロード バランサーによって使用されたり、もちろん監視にも使用できます。以下に、Patroni REST API エンドポイントのリストを示します。

--------

## ヘルスチェックエンドポイント {#health-check-endpoints}

すべてのヘルス チェック `GET` リクエストに対して、Patroni は、ノードのステータスと HTTP ステータス コードを含む JSON ドキュメントを返します。 JSON ドキュメントが必要ない場合、または必要ない場合は、`GET` の代わりに `HEAD` メソッドまたは `OPTIONS` メソッドの使用を検討してください。

- Patroni REST API に対する次のリクエストは、Patroni ノードがリーダー ロック付きのプライマリーとして実行されている場合にのみ、HTTP ステータス コード **200** を返します。

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader`: Patroni ノードが [スタンバイクラスタ](/ja/docs/patroni/standby_cluster#standby_cluster) のリーダーとして実行されている場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /leader`: Patroni ノードにリーダー ロックがある場合、HTTP ステータス コード **200** を返します。前の 2 つのエンドポイントとの主な違いは、PostgreSQL が `primary` として実行されているか、`standby_leader` として実行されているかが考慮されていないことです。

- `GET /replica`: レプリカのヘルスチェックエンドポイント。 Patroni ノードが `running` 状態にあり、ロールが `replica` で、`noloadbalance` タグが設定されていない場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /replica?replication_state=<required state>`: レプリカ チェック エンドポイント。 `replica` からのチェックに加えて、レプリケーションの状態が必要な状態と一致するかどうかもチェックします。主に `replication_state=streaming` で使用し、アーカイブ リカバリでまだ追いついていないレプリカを除外するのに役立ちます。

- `GET /replica?lag=<max-lag>`: レプリカ チェック エンドポイント。 `replica` からのチェックに加えて、レプリケーションの遅延もチェックし、指定された値を下回っている場合にのみステータス コード **200** を返します。 DCS のキー cluster.last_leader_operation は、パフォーマンス上の理由から、リーダー wal の位置とレプリカのレイテンシの計算に使用されます。 max-lag はバイト (整数) または人間が判読できる値で指定できます。 16kB、64MB、1GB。

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2`: レプリカ チェック エンドポイント。さらに、ユーザー定義タグ `key1` および `key2` と、yaml 構成管理の **tags** セクション内のそれぞれの値もチェックされます。タグがインスタンスに対して定義されていない場合、または yaml 設定内の値がクエリー値と一致しない場合は、HTTP ステータス コード 503 が返されます。

次のリクエストでは、リーダーまたはスタンバイ リーダーのステータスをチェックしているため、Patroni はユーザー定義のタグを適用せず、無視されます。

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only`: 上記のエンドポイントと似ていますが、プライマリーも含まれます。

- `GET /synchronous` または `GET /sync`: Patroni ノードが同期スタンバイとして実行されている場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /read-only-sync`: 上記のエンドポイントと似ていますが、プライマリーも含まれます。

- `GET /quorum`: この Patroni ノードがプライマリーの `synchronous_standby_names` にクォーラム ノードとしてリストされている場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /read-only-quorum`: 上記のエンドポイントと似ていますが、プライマリーも含まれます。

- `GET /asynchronous` または `GET /async`: Patroni ノードが非同期スタンバイとして実行されている場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /asynchronous?lag=<max-lag>` または `GET /async?lag=<max-lag>`: 非同期スタンバイ チェック エンドポイント。 `asynchronous` または `async` からのチェックに加えて、レプリケーションの遅延もチェックし、指定された値を下回っている場合にのみステータス コード **200** を返します。 DCS のキー cluster.last_leader_operation は、パフォーマンス上の理由から、リーダー wal の位置とレプリカのレイテンシの計算に使用されます。 max-lag はバイト (整数) または人間が判読できる値で指定できます。 16kB、64MB、1GB。

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health`: PostgreSQL が稼働している場合にのみ、HTTP ステータス コード **200** を返します。

- `GET /liveness`: Patroni ハートビート ループが適切に実行されている場合は HTTP ステータス コード **200** を返し、最後の実行がプライマリーで `ttl` 秒以上前である場合、またはレプリカで `2*ttl` を超えている場合は **503** を返します。 `livenessProbe` に使用できます。

- `GET /readiness?lag=<max-lag>&mode=apply|write`: Patroni ノードがリーダーとして実行されている場合、または PostgreSQL が稼働中でレプリケートしており、リーダーからそれほど離れていない場合は、HTTP ステータス コード **200** を返します。 lag パラメーターは、スタンバイがどれだけ遅れを許容できるかを設定します。デフォルトは `maximum_lag_on_failover` です。ラグはバイト単位、または人間が判読できる値 (16kB、64MB、1GB など) で指定できます。 Mode は、WAL を再生 (適用) する必要があるか、受信するだけ (書き込み) する必要があるかを設定します。デフォルトは適用です。

Kubernetes `readinessProbe` として使用すると、新しく開始されたポッドがリーダーに追いついた場合にのみ準備が完了するようになります。これを PodDisruptionBudget と組み合わせると、ノードのローリング再起動中にリーダーが早期に終了するのを防ぐことができます。また、レプリケーションに対応できないレプリカが読み取り専用トラフィックを処理しないようにします。リーダー選挙 (OpenShift) に ​​Kubernetes エンドポイントを使用できない場合、エンドポイントは `readinessProbe` に使用できます。

`liveness` エンドポイントは非常に軽量であり、SQL は実行されません。プローブは、リーダー キーの有効期限が切れる頃に失敗し始めるように構成する必要があります。デフォルト値 `ttl` (`30s`) を使用すると、プローブの例は次のようになります。

```yaml
readinessProbe:
  httpGet:
    scheme: HTTP
    path: /readiness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
livenessProbe:
  httpGet:
    scheme: HTTP
    path: /liveness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

--------

## 監視エンドポイント {#monitoring-endpoint}

`GET /patroni` は、リーダー レース中に Patroni によって使用されます。監視システムでも使用できます。このエンドポイントによって生成される JSON ドキュメントは、ヘルス チェック エンドポイントによって生成される JSON と同じ構造を持っています。

**例:** 正常なクラスター

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "primary",
  "server_version": 160004,
  "xlog": {
    "location": 67395656
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "dcs_last_seen": 1692356718,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**例:** ロック解除されたクラスター

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "received_location": 67419744,
    "replayed_location": 67419744,
    "replayed_timestamp": null,
    "paused": false
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**例:** [DCS フェイルセーフ モード](/ja/docs/patroni/dcs_failsafe_mode#dcs_failsafe_mode) が有効になっているロック解除されたクラスター

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "failsafe_mode_is_active": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**例:** [一時停止モード](/ja/docs/patroni/pause#pause) が有効になっているクラスター

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "pause": true,
  "dcs_last_seen": 1724874295,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

`GET /metrics` エンドポイントを通じて、Patroni メトリクスを Prometheus 形式で取得します。

``` bash
$ curl http://localhost:8008/metrics

# HELP patroni_version Patroni semver without periods. \
# TYPE patroni_version gauge
patroni_version{scope="batman",name="patroni1"} 040000
# HELP patroni_postgres_running Value is 1 if Postgres is running, 0 otherwise.
# TYPE patroni_postgres_running gauge
patroni_postgres_running{scope="batman",name="patroni1"} 1
# HELP patroni_postmaster_start_time Epoch seconds since Postgres started.
# TYPE patroni_postmaster_start_time gauge
patroni_postmaster_start_time{scope="batman",name="patroni1"} 1724873966.352526
# HELP patroni_primary Value is 1 if this node is the leader, 0 otherwise.
# TYPE patroni_primary gauge
patroni_primary{scope="batman",name="patroni1"} 1
# HELP patroni_xlog_location Current location of the Postgres transaction log, 0 if this node is not the leader.
# TYPE patroni_xlog_location counter
patroni_xlog_location{scope="batman",name="patroni1"} 22320573386952
# HELP patroni_standby_leader Value is 1 if this node is the standby_leader, 0 otherwise.
# TYPE patroni_standby_leader gauge
patroni_standby_leader{scope="batman",name="patroni1"} 0
# HELP patroni_replica Value is 1 if this node is a replica, 0 otherwise.
# TYPE patroni_replica gauge
patroni_replica{scope="batman",name="patroni1"} 0
# HELP patroni_sync_standby Value is 1 if this node is a sync standby replica, 0 otherwise.
# TYPE patroni_sync_standby gauge
patroni_sync_standby{scope="batman",name="patroni1"} 0
# HELP patroni_quorum_standby Value is 1 if this node is a quorum standby replica, 0 otherwise.
# TYPE patroni_quorum_standby gauge
patroni_quorum_standby{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_received_location Current location of the received Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_received_location counter
patroni_xlog_received_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_location Current location of the replayed Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_replayed_location counter
patroni_xlog_replayed_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_timestamp Current timestamp of the replayed Postgres transaction log, 0 if null.
# TYPE patroni_xlog_replayed_timestamp gauge
patroni_xlog_replayed_timestamp{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_paused Value is 1 if the Postgres xlog is paused, 0 otherwise.
# TYPE patroni_xlog_paused gauge
patroni_xlog_paused{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_streaming Value is 1 if Postgres is streaming, 0 otherwise.
# TYPE patroni_postgres_streaming gauge
patroni_postgres_streaming{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_in_archive_recovery Value is 1 if Postgres is replicating from archive, 0 otherwise.
# TYPE patroni_postgres_in_archive_recovery gauge
patroni_postgres_in_archive_recovery{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_server_version Version of Postgres (if running), 0 otherwise.
# TYPE patroni_postgres_server_version gauge
patroni_postgres_server_version{scope="batman",name="patroni1"} 160004
# HELP patroni_cluster_unlocked Value is 1 if the cluster is unlocked, 0 if locked.
# TYPE patroni_cluster_unlocked gauge
patroni_cluster_unlocked{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_is_active Value is 1 if failsafe mode is active, 0 otherwise.
# TYPE patroni_failsafe_mode_is_active gauge
patroni_failsafe_mode_is_active{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_enabled Value is 1 if failsafe_mode is enabled, 0 otherwise.
# TYPE patroni_failsafe_mode_enabled gauge
patroni_failsafe_mode_enabled{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_member Value is 1 if this node is a member of failsafe, 0 otherwise.
# TYPE patroni_failsafe_member gauge
patroni_failsafe_member{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_timeline Postgres timeline of this node (if running), 0 otherwise.
# TYPE patroni_postgres_timeline gauge
patroni_postgres_timeline{scope="batman",name="patroni1"} 24
# HELP patroni_dcs_last_seen Epoch timestamp when DCS was last contacted successfully by Patroni.
# TYPE patroni_dcs_last_seen gauge
patroni_dcs_last_seen{scope="batman",name="patroni1"} 1724874235
# HELP patroni_pending_restart Value is 1 if the node needs a restart, 0 otherwise.
# TYPE patroni_pending_restart gauge
patroni_pending_restart{scope="batman",name="patroni1"} 1
# HELP patroni_is_paused Value is 1 if auto failover is disabled, 0 otherwise.
# TYPE patroni_is_paused gauge
patroni_is_paused{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_state Numeric representation of Postgres state.
# Values: 0=initdb, 1=initdb_failed, 2=custom_bootstrap, 3=custom_bootstrap_failed, 4=creating_replica, 5=running, 6=starting, 7=bootstrap_starting, 8=start_failed, 9=restarting, 10=restart_failed, 11=stopping, 12=stopped, 13=stop_failed, 14=crashed
# TYPE patroni_postgres_state gauge
patroni_postgres_state{scope="batman",name="patroni1"} 5
# HELP patroni_failover_priority Failover priority of this node.
# TYPE patroni_failover_priority gauge
patroni_failover_priority{scope="batman",name="patroni1"} 1
```

### PostgreSQL 状態値 {#postgresql-state-values}

`patroni_postgres_state` メトリックは、現在の PostgreSQL インスタンスの状態を数値で表します。これは、時間の経過に伴う状態変化を追跡する必要があるシステムの監視と警告に役立ちます。数値は、`PostgresqlState.get_metrics_description()` 静的メソッドを使用して生成されます。

|値 |州名 |説明 |
|------|----------------------|----------------------|
| 0 | initdb |新しいクラスターを初期化しています |
| 1 | initdb_failed |新しいクラスターの初期化に失敗しました |
| 2 |カスタムブートストラップ |カスタム ブートストラップ スクリプトの実行 |
| 3 |カスタムブートストラップ失敗 |カスタム ブートストラップ スクリプトが失敗しました |
| 4 |レプリカの作成 |プライマリーからレプリカを作成 |
| 5 |実行中 | PostgreSQL は正常に実行されています。 |
| 6 |開始 | PostgreSQL が起動中です |
| 7 |ブートストラップ_開始中 |カスタムブートストラップ後に開始 |
| 8 |開始失敗 | PostgreSQL の開始に失敗しました |
| 9 |再起動 | PostgreSQL が再起動中です |
| 10 |再起動失敗 | PostgreSQL の再起動に失敗しました |
| 11 |停止 | PostgreSQL は停止しています |
| 12 |停止しました | PostgreSQL は停止しています |
| 13 |停止失敗 | PostgreSQL 停止に失敗しました |
| 14 |クラッシュした | PostgreSQL がクラッシュしました |

PostgreSQL 状態値

> [!NOTE]
> これらの数値は固定されており、既存の監視システムとの下位互換性を維持するために変更されることはありません。将来的に新しい状態が追加された場合、既存の数値を変更することなく、新しい数値が割り当てられます。

--------

## クラスターステータスエンドポイント {#cluster-status-endpoints}

- `GET /cluster` エンドポイントは、現在のクラスター トポロジと状態を説明する JSON ドキュメントを生成します。

``` bash
$ curl -s http://localhost:8008/cluster | jq .
{
  "members": [
    {
      "name": "patroni1",
      "role": "leader",
      "state": "running",
      "api_url": "http://10.89.0.4:8008/patroni",
      "host": "10.89.0.4",
      "port": 5432,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      }
    },
    {
      "name": "patroni2",
      "role": "replica",
      "state": "streaming",
      "api_url": "http://10.89.0.6:8008/patroni",
      "host": "10.89.0.6",
      "port": 5433,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      },
      "receive_lag": 0,
      "receive_lsn": "0/4000060",
      "replay_lag": 0,
      "replay_lsn": "0/4000060",
      "lag": 0,
      "lsn": "0/4000060"
    }
  ],
  "scope": "demo",
  "scheduled_switchover": {
    "at": "2023-09-24T10:36:00+02:00",
    "from": "patroni1",
    "to": "patroni3"
  }
}
```

- `GET /history` エンドポイントは、クラスターのスイッチオーバー/フェイルオーバーの履歴を表示します。この形式は、`pg_wal` ディレクトリ内の履歴ファイルの内容とよく似ています。唯一の違いは、新しいタイムラインがいつ作成されたかを示すタイムスタンプ フィールドです。

``` bash
$ curl -s http://localhost:8008/history | jq .
[
  [
    1,
    25623960,
    "no recovery target specified",
    "2019-09-23T16:57:57+02:00"
  ],
  [
    2,
    25624344,
    "no recovery target specified",
    "2019-09-24T09:22:33+02:00"
  ],
  [
    3,
    25624752,
    "no recovery target specified",
    "2019-09-24T09:26:15+02:00"
  ],
  [
    4,
    50331856,
    "no recovery target specified",
    "2019-09-24T09:35:52+02:00"
  ]
]
```

<a id="config_endpoint"></a>

--------

## 構成エンドポイント {#config-endpoint}

`GET /config`: 動的構成の現在のバージョンを取得します。

``` bash
$ curl -s http://localhost:8008/config | jq .
{
  "ttl": 30,
  "loop_wait": 10,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "100"
    }
  }
}
```

`PATCH /config`: 既存の構成を変更します。

``` bash
$ curl -s -XPATCH -d \
    '{"loop_wait":5,"ttl":20,"postgresql":{"parameters":{"max_connections":"101"}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "101"
    }
  }
}
```

上記の REST API 呼び出しは、既存の構成にパッチを適用し、新しい構成を返します。

ノードがこの構成を処理したことを確認してみましょう。まず、5 秒ごとにログ行の出力を開始する必要があります (loop_wait=5)。 "max_connections" の変更には再起動が必要なため、"pending_restart" フラグを公開する必要があります。

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "database_system_identifier": "6287881213849985952",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "xlog": {
    "location": 2197818976
  },
  "timeline": 1,
  "dcs_last_seen": 1724874545,
  "database_system_identifier": "7408277255830290455",
  "pending_restart": true,
  "pending_restart_reason": {
    "max_connections": {
      "old_value": "100",
      "new_value": "101"
    }
  },
  "patroni": {
    "version": "4.0.0",
    "scope": "batman",
    "name": "patroni1"
  },
  "state": "running",
  "role": "primary",
  "server_version": 160004
}
```

パラメータの削除:

一部の設定を削除 (リセット) したい場合は、`null` を使用してパッチを適用するだけです。

``` bash
$ curl -s -XPATCH -d \
    '{"postgresql":{"parameters":{"max_connections":null}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5
    }
  }
}
```

上記の呼び出しにより、動的構成から `postgresql.parameters.max_connections` が削除されます。

`PUT /config`: 既存の動的構成の完全な書き換えを無条件に実行することも可能です。

``` bash
$ curl -s -XPUT -d \
    '{"maximum_lag_on_failover":1048576,"retry_timeout":10,"postgresql":{"use_slots":true,"use_pg_rewind":true,"parameters":{"hot_standby":"on","wal_level":"hot_standby","unix_socket_directories":".","max_wal_senders":5}},"loop_wait":3,"ttl":20}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5
    },
    "use_pg_rewind": true
  },
  "loop_wait": 3
}
```

--------

## スイッチオーバーおよびフェイルオーバーのエンドポイント {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### スイッチオーバー {#switchover}

`/switchover` エンドポイントは、クラスターが正常な場合 (リーダーがある場合) にのみ機能します。また、特定の時間にスイッチオーバーをスケジュールすることもできます。

`/switchover` エンドポイントを呼び出す場合、`/failover` エンドポイントとは異なり、候補を指定できますが、必須ではありません。候補者が指定されていない場合、リーダーが退任した後、クラスターの適格なすべてのノードがリーダー レースに参加します。

`POST` リクエストの JSON 本文で、`leader` フィールドを指定する必要があります。 `candidate` フィールドと `scheduled_at` フィールドはオプションであり、特定の時間にスイッチオーバーをスケジュールするために使用できます。

状況に応じて、リクエストは異なる HTTP ステータス コードと本文を返す場合があります。スイッチオーバーまたはフェイルオーバーが正常に完了すると、ステータス コード **200** が返されます。スイッチオーバーが正常にスケジュールされた場合、Patroni は HTTP ステータス コード **202** を返します。何か問題が発生した場合、エラー ステータス コード (**400**、**412**、または **503** のいずれか) が応答本文の詳細とともに返されます。

`DELETE /switchover` を使用して、現在スケジュールされているスイッチオーバーを削除できます。

**例:** 正常なスタンバイへのスイッチオーバーを実行します

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**例:** 特定のノードへのスイッチオーバーを実行します

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**例:** は、特定の時間にリーダーからクラスター内の他の正常なスタンバイへのスイッチオーバーをスケジュールします。

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### フェイルオーバー {#failover}

`/failover` エンドポイントは、正常なノードがない場合に手動フェイルオーバーを実行するために使用できます (たとえば、すべての同期スタンバイが昇格できるほど正常でない場合は非同期スタンバイに)。ただし、クラスターにリーダーがない必要はありません。正常なクラスターでもフェイルオーバーを実行できます。

`POST` リクエストの JSON 本文で、`candidate` フィールドを指定する必要があります。 `leader` フィールドが指定されている場合、代わりにスイッチオーバーがトリガーされます。

**例:**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!WARNING]
> このエンドポイントを使用する場合は、[十分注意してください](/ja/docs/patroni/rest_api#failover_healthcheck) を使用します。これにより、特定の状況でデータ損失が発生する可能性があります。ほとんどの場合、[スイッチオーバーエンドポイント](/ja/docs/patroni/rest_api#switchover_api) は管理者のニーズを満たします。

`POST /switchover` エンドポイントと `POST /failover` エンドポイントは、それぞれ [patronictl_switchover](/ja/docs/patroni/patronictl#patronictl_switchover) と [patronictl_failover](/ja/docs/patroni/patronictl#patronictl_failover) によって使用されます。

`DELETE /switchover` は [patronictl flush cluster-name switchover](/ja/docs/patroni/patronictl#patronictl_flush_parameters) によって使用されます。

|                              |フェイルオーバー |切り替え |
|----------------------------|----------|-------------------------------------|
|引出線の指定が必要です |いいえ |はい |
|候補を指定する必要があります |はい |いいえ |
|一時停止中でも実行可能 |はい |はい (特定の候補者のみ) |
|スケジュール可能 |いいえ |はい (一時停止中でない場合) |

フェイルオーバー/スイッチオーバーの比較

<a id="failover_healthcheck"></a>

### 健全なスタンバイ {#healthy-standby}

スイッチオーバー中にリーダー レースに参加できるようにするため、またはフェイルオーバー/スイッチオーバーの候補としてリーダーになるために、クラスターのメンバーが合格する必要があるチェックがいくつかあります。

- Patroni API 経由でアクセス可能です。
- には `nofailover` タグが `true` に設定されていません。
- ウォッチドッグが完全に機能します (構成で必要な場合)。
- 正常なクラスターでのスイッチオーバーまたは自動フェイルオーバーの場合は、最大レプリケーション ラグ (`maximum_lag_on_failover` [構成パラメータ](/ja/docs/patroni/config/dynamic#dynamic)) を超えません。
- 正常なクラスターでのスイッチオーバーまたは自動フェイルオーバーの場合、`check_timeline` [構成パラメータ](/ja/docs/patroni/config/dynamic#dynamic) が `true` に設定されている場合は、クラスターのタイムラインよりも小さいタイムライン番号を設定しないでください。
- [同期モード](/ja/docs/patroni/replication_modes#synchronous_mode) の :
  - スイッチオーバーの場合 (候補がある場合とない場合の両方): `/sync` キー メンバーにリストされます。
  - 正常なクラスターと異常なクラスターの両方でのフェイルオーバーの場合、このチェックは省略されます。

> [!WARNING]
> リーダーのないクラスターで手動フェイルオーバーが行われる場合、候補者は次の場合でも昇格できます。 - 同期モードが有効な場合、候補者は `/sync` キー メンバーに含まれていません。 - その遅延が、許容される最大レプリケ​​ーション遅延を超えています。 - 最後の既知のクラスター タイムラインよりも小さいタイムライン番号が付いています。

<a id="restart_endpoint"></a>

--------

## エンドポイントを再起動します {#restart-endpoint}

- `POST /restart`: `POST /restart` 呼び出しを実行すると、特定のノードで Postgres を再起動できます。 `POST` リクエストの JSON 本体では、オプションでいくつかの再起動条件を指定できます。
  - **restart_pending**: ブール値、`true` に設定すると、Patroni は、PostgreSQL 構成にいくつかの変更を適用するために、再起動が保留中の場合にのみ PostgreSQL を再起動します。
  - **role**: ノードの現在のロールが POST リクエストのロールと一致する場合にのみ再起動を実行します。
  - **postgres_version**: postgres の現在のバージョンが POST リクエストで指定されたバージョンよりも小さい場合にのみ再起動を実行します。
  - **timeout**: PostgreSQL が接続の受け入れを開始するまで待機する必要がある時間。 `primary_start_timeout` をオーバーライドします。
  - **schedule**: タイムゾーン付きのタイムスタンプ。将来のどこかで再起動をスケジュールします。
- `DELETE /restart`: スケジュールされた再起動を削除します

`POST /restart` エンドポイントと `DELETE /restart` エンドポイントは、それぞれ [patronictl_restart](/ja/docs/patroni/patronictl#patronictl_restart) と [patronictl flush cluster-name restart](/ja/docs/patroni/patronictl#patronictl_flush_parameters) によって使用されます。

<a id="reload_endpoint"></a>

--------

## エンドポイントのリロード {#reload-endpoint}

`POST /reload` 呼び出しは、Patroni に構成ファイルを再読み込みして適用するように命令します。これは、`SIGHUP` シグナルを Patroni プロセスに送信するのと同じです。再起動が必要な Postgres パラメーターの一部 (**shared_buffers** など) を変更した場合でも、`POST /restart` エンドポイントを呼び出すか、[patronictl_restart](/ja/docs/patroni/patronictl#patronictl_restart) を使用して、明示的に Postgres の再起動を行う必要があります。

リロード エンドポイントは [patronictl_reload](/ja/docs/patroni/patronictl#patronictl_reload) によって使用されます。

--------

## エンドポイントを再初期化する {#reinitialize-endpoint}

`POST /reinitialize`: 指定されたノード上の PostgreSQL データ ディレクトリを再初期化します。レプリカ上でのみ実行が許可されます。呼び出されると、データ ディレクトリが削除され、`pg_basebackup` または代替の [レプリカ作成方法](/ja/docs/patroni/replica_bootstrap#custom_replica_creation) が開始されます。

Patroni が、障害が発生した Postgres を回復 (再起動) しようとするループ内にある場合、呼び出しは失敗する可能性があります。この問題を解決するには、リクエスト本文に `{"force":true}` を指定します。

リクエスト本文で {"from-leader":true} を指定すると、リーダー ノードからベースバックアップを直接取得できます。これは、すべてのレプリカ ノードに障害が発生したときに再初期化を実行する場合に便利です。

再初期化エンドポイントは [patronictl_reinit](/ja/docs/patroni/patronictl#patronictl_reinit) によって使用されます。
