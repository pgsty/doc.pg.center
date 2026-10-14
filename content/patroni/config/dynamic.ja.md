---
title: "動的構成設定"
linkTitle: "動的構成"
weight: 10
icon: fa-solid fa-sliders
description: "動的な構成設定は DCS に保存され、クラスター全体に適用されます。"
module: [PATRONI]
categories: [リファレンス]
upstream_link: "https://patroni.readthedocs.io/en/latest/dynamic_configuration.html"
---

<a id="dynamic"></a>
動的構成は DCS (分散構成ストア) に保存され、すべてのクラスター ノードに適用されます。

動的構成を変更するには、[patronictl_edit_config](/ja/patroni/patronictl#patronictl_edit_config) ツールまたは Patroni [REST API](/ja/patroni/rest_api#rest_api) を使用できます。

- **loop_wait**: ループがスリープする秒数。デフォルト値: 10、可能な最小値: 1
- **ttl**: リーダー ロックを取得する TTL (秒単位)。これは、自動フェイルオーバー プロセスが開始されるまでの時間と考えてください。デフォルト値: 30、可能な最小値: 20
- **retry_timeout**: DCS および PostgreSQL 操作の再試行のタイムアウト (秒単位)。この値より短い DCS やネットワークの問題が発生しても、Patroni はリーダーをデモートしません。デフォルト値: 10、可能な最小値: 3

> [!WARNING]
> **loop_wait**、**retry_timeout**、**ttl** の値を変更する際は、次のルールに従う必要があります。
>
> ```python
> loop_wait + 2 * retry_timeout <= ttl
> ```

- **maximum_lag_on_failover**: フォロワーがリーダーの選出に参加するために許容される最大遅延バイト数。
- **primary_race_backoff**: プライマリーからの WAL レプリケーションがまだ進行中の場合、スタンバイでのリーダーの競争を `primary_race_backoff` 秒延期します。これにより、Patroni が一時的に応答しなくなることによって引き起こされる不必要なフェイルオーバーを最小限に抑えることができます。デフォルト値: 0 (無効)。
- **maximum_lag_on_syncnode**: 同期フォロワーが異常な候補とみなされ、健全な非同期フォロワーによってスワップされるまでに、同期フォロワーが遅れる可能性がある最大バイト数。 Patroni は、複数のフォロワーがある場合は最大レプリカ lsn を使用します。それ以外の場合は、リーダーの現在の wal lsn を使用します。デフォルトは -1 です。値が 0 以下に設定されている場合、Patroni は同期の異常なフォロワーを交換するアクションを実行しません。トランザクション量が多いときに Patroni が同期フォロワーを頻繁にスワップしないように、十分大きな値を設定してください。
- **max_timelines_history**: DCS に保持されるタイムライン履歴アイテムの最大数。デフォルト値: 0。 0 に設定すると、完全な履歴が DCS に保存されます。
- **primary_start_timeout**: フェイルオーバーがトリガーされる前にプライマリーが障害から回復できる時間 (秒単位)。デフォルトは 300 秒です。 0 に設定すると、可能であればクラッシュが検出された直後にフェイルオーバーが実行されます。非同期レプリケーションを使用する場合、フェイルオーバーによりトランザクションが失われる可能性があります。プライマリー障害における最悪の場合のフェイルオーバー時間は loop_wait + primary_start_timeout + loop_wait ですが、primary_start_timeout が 0 の場合は loop_wait のみです。耐久性と可用性のトレードオフに応じて値を設定します。
- **primary_stop_timeout**: Postgres を停止するときに Patroni が待機できる秒数。synchronous_mode が有効な場合にのみ有効です。 \> 0 に設定され、synchronous_mode が有効になっている場合、primary_stop_timeout で設定された値を超えて停止操作が実行されている場合、Patroni は postmaster に SIGKILL を送信します。耐久性と可用性のトレードオフに応じて値を設定します。パラメーターが設定されていない場合、または \<= 0 に設定されている場合、primary_stop_timeout は適用されません。
- **synchronous_mode**: 同期レプリケーション モードをオンにします。可能な値: `off`、`on`、`quorum`。このモードでは、リーダーが `synchronous_standby_names` の管理を担当し、最後に知られたリーダー、または同期レプリカの 1 つだけがリーダー レースに参加できます。同期モードでは、Patroni がトランザクションの耐久性を確保できない場合、書き込みの可用性が失われるという代償として、正常にコミットされたトランザクションがフェイルオーバー時に失われることはありません。詳細については、[レプリケーションモードのドキュメント](/ja/patroni/replication_modes#replication_modes) を参照してください。
- **synchronous_mode_strict**: 使用可能な同期レプリカがない場合に同期レプリケーションを無効にせず、プライマリーへのすべてのクライアント書き込みをブロックします。優先順位に基づく同期モード（`synchronous_mode: on`）では、適切な同期スタンバイがない場合、Patroni 4.1.5 は `synchronous_standby_names` を `*` に設定します。詳細については、[レプリケーションモードのドキュメント](/ja/patroni/replication_modes#replication_modes) を参照してください。
- **synchronous_node_count**: [synchronous_mode](/ja/patroni/replication_modes#synchronous_mode) が有効な場合、このパラメーターは Patroni によって使用され、同期スタンバイ インスタンスの正確な数を管理し、メンバーの参加と脱退に応じて DCS の状態と PostgreSQL の `synchronous_standby_names` パラメーターを調整します。パラメーターが対象となるノードの数よりも大きい値に設定されている場合、パラメーターは自動的に調整されます。デフォルトは `1` です。
- **failsafe_mode**: [DCS フェールセーフ モード](/ja/patroni/dcs_failsafe_mode#dcs_failsafe_mode) を有効にします。デフォルトは `false` です。
- **postgresql**:
  - **use_pg_rewind**: pg_rewind を使用するかどうか。デフォルトは `false` です。クラスターは `data page checksums` (`initdb` の `--data-checksums` オプション) で初期化するか、`wal_log_hints` を `on` に設定する必要があります。そうしないと、`pg_rewind` は機能しないことに注意してください。
  - **use_slots**: レプリケーション スロットを使用するかどうか。 PostgreSQL 9.4+ ではデフォルトは `true` です。
  - **recovery_conf**: フォロワーの構成時に recovery.conf に書き込まれる追加の構成設定。 PostgreSQL 12 には recovery.conf はもうありませんが、Patroni が透過的に処理するため、このセクションを引き続き使用できます。
  - **parameters**: `{max_connections: 100, wal_level: "replica", max_wal_senders: 10, wal_log_hints: "on"}` 形式の Postgres の構成パラメーター (GUC)。これらの多くは、レプリケーションが機能するために必要です。
  - **parameters_primary**: (オプション) プライマリーのロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** にマージされ、同じパラメーターのベース値を上書きします。
  - **parameters_replica**: (オプション) レプリカのロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** にマージされ、同じパラメーターのベース値を上書きします。
  - **parameters_standby_leader**: (オプション) standby_leader のロール固有のパラメーターをオーバーライドします。これらの値は、ベースの **parameters** にマージされ、同じパラメーターのベース値を上書きします。
  - **pg_hba**: Patroni が `pg_hba.conf` を生成するために使用する行のリスト。 `hba_file` PostgreSQL パラメータがデフォルト以外の値に設定されている場合、Patroni はこのパラメータを無視します。
    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: レプリケーションにはこのような行が必要です。
  - **pg_hba_primary**: (オプション) プライマリーのロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。
  - **pg_hba_replica**: (オプション) レプリカのロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。
  - **pg_hba_standby_leader**: (オプション) standby_leader のロール固有の pg_hba エントリ。これらは **pg_hba** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_hba** が使用されます。
  - **pg_ident**: Patroni が `pg_ident.conf` を生成するために使用する行のリスト。 `ident_file` PostgreSQL パラメータがデフォルト以外の値に設定されている場合、Patroni はこのパラメータを無視します。
    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (オプション) プライマリーのロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。
  - **pg_ident_replica**: (オプション) レプリカのロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。
  - **pg_ident_standby_leader**: (オプション) standby_leader のロール固有の pg_ident エントリ。これらは **pg_ident** を完全に置き換えます (マージなし)。定義されていない場合は、**pg_ident** が使用されます。
- **standby_cluster**: このセクションが定義されている場合、スタンバイ クラスターをブートストラップします。
  - **host**: リモートノードのアドレス
  - **port**: リモート ノードのポート
  - **primary_slot_name**: レプリケーションに使用するリモート ノードのスロット。このパラメータはオプションであり、デフォルト値はインスタンス名から導出されます (関数 `slot_name_from_member_name` を参照)。
  - **create_replica_methods**: リモート プライマリーからスタンバイ リーダーをブートストラップするために使用できるメソッドの順序付きリスト。[postgresql_settings](/ja/patroni/config/yaml#postgresql_settings) で定義されたリストとは異なる場合があります。
  - **restore_command**: WAL レコードをリモート プライマリーからスタンバイ クラスターのノードに復元するコマンド。[postgresql_settings](/ja/patroni/config/yaml#postgresql_settings) で定義されたリストと異なる場合があります。
  - **archive_cleanup_command**: スタンバイ リーダーのクリーンアップ コマンド
  - **recovery_min_apply_delay**: WAL レコードをスタンバイ リーダーに実際に適用するまでの待機時間
- **member_slots_ttl**: レプリカのシャットダウン時の物理レプリケーション スロットの保持時間。デフォルト値: `30min`。以前の動作を維持したい場合は、これを `0` に設定します (メンバー キーの有効期限が DCS から切れると、スロットはすぐに削除されます)。この機能は、PostgreSQL 11 以降でのみ動作します。
- **slots**: 永続的なレプリケーション スロットを定義します。これらのスロットは、スイッチオーバー/フェイルオーバー中に保持されます。存在しない永続スロットは Patroni によって作成されます。 PostgreSQL 11 以降では、すべてのノードに永続的な物理スロットが作成され、その位置は **loop_wait** 秒ごとに進められます。 11 よりも古い PostgreSQL バージョンの場合、永続的な物理レプリケーション スロットは現在のプライマリーでのみ維持されます。論理スロットは再起動によってプライマリーからスタンバイにコピーされ、その後 (必要に応じて) **loop_wait** 秒ごとに位置が進みます。論理スロット ファイルのコピーは、`libpq` 接続経由で、rewind またはスーパーユーザーの資格情報を使用して実行されます (**postgresql.authentication** セクションを参照)。レプリカ上の論理スロットの位置が以前のプライマリーより少し遅れている可能性が常にあります。そのため、アプリケーションは、フェイルオーバー後に一部のメッセージを 2 回受信する可能性に備えておく必要があります。最も簡単な方法は、`confirmed_flush_lsn` を追跡することです。永久レプリケーション スロットを有効にするには、**postgresql.use_slots** を `true` に設定する必要があります。永続的な論理レプリケーション スロットが定義されている場合、Patroni は `hot_standby_feedback` を自動的に有効にします。論理レプリケーション スロットのフェイルオーバーは、PostgreSQL 9.6 以前では安全でなく、PostgreSQL バージョン 10 にはいくつかの重要な機能が欠けているため、この機能は PostgreSQL 11+ でのみ動作します。
  - **my_slot_name**: 永続レプリケーション スロットの名前。永続スロット名が現在のノードの名前と一致する場合、そのスロットはこのノードには作成されません。 Patroni メンバーの名前と一致する名前の永続的な物理レプリケーション スロットを追加すると、Patroni は、対応するメンバーが応答しなくなった場合でも、作成されたスロットが削除されないことを保証します (通常であればこの状況では Patroni によってスロットが削除されるところです)。これは、メンバーによって使用されるレプリケーション スロットを一時的な障害時に持続させたい場合や、既存のメンバーを新しい Patroni クラスターにインポートする場合 (詳細については [スタンドアロンを Patroni クラスターに変換する](/ja/patroni/existing_data#existing_data) を参照) など、状況によっては便利ですが、Patroni の通常の機能への影響を考慮し、スロットが不要になった時点でこれらの名前の衝突が DCS に残存しないよう、オペレーターは注意を払う必要があります。
    - **type**: スロット タイプ。 `physical` または `logical` の可能性があります。スロットが論理スロットの場合は、`database` と `plugin` を追加で定義する必要があります。スロットが物理的な場合は、オプションで `cluster_type` を定義できます。
    - **database**: 論理スロットを作成するデータベース名。
    - **plugin**: 論理スロットのプラグイン名。
    - **cluster_type**: スロットを作成するクラスターのタイプ (`primary` または `standby`)。スロットはこのタイプのクラスターでのみ作成され、それ以外のクラスターでは作成されないか、既存のスロットが削除されます。
- **ignore_slots**: Patroni が一致するスロットを無視するレプリケーション スロット プロパティのセットのリスト。この構成/機能などは、一部のレプリケーション スロットが Patroni の外部で管理されている場合に役立ちます。一致するプロパティの任意のサブセットが、スロットを無視させる原因になります。
  - **name**: レプリケーション スロットの名前。
  - **type**: スロット タイプ。 `physical` または `logical` を指定できます。スロットが論理スロットの場合は、`database` や `plugin` を追加で定義できます。
  - **database**: データベース名 (`logical` スロットと一致する場合)。
  - **plugin**: 論理デコード プラグイン (`logical` スロットに一致する場合)。

注: **slots** はハッシュマップですが、**ignore_slots** は配列です。たとえば:

```yaml
slots:
  permanent_logical_slot_name:
    type: logical
    database: my_db
    plugin: test_decoding
  permanent_physical_slot_name:
    type: physical
  ...
ignore_slots:
  - name: ignored_logical_slot_name
    type: logical
    database: my_db
    plugin: test_decoding
  - name: ignored_physical_slot_name
    type: physical
  ...
```

注: PostgreSQL v11 以降を実行すると、Patroni はリーダーになる可能性のあるすべてのノードで物理レプリケーション スロットを維持するため、レプリカ ノードは他のノードで必要になる可能性がある場合に WAL セグメントを予約したままにします。ノードが存在せず、DCS 内のメンバー キーの有効期限が切れた場合、対応するレプリケーション スロットは `member_slots_ttl` の後に削除されます (デフォルト値は `30min`)。ニーズに応じて保持期間を増減できます。あるいは、クラスター トポロジが静的 (名前が変更されない固定数のノード) の場合は、レプリカが一時的に停止している間にスロットの削除や WAL ファイルのリサイクルを回避するために、ノードの名前に対応する名前を使用して永続的な物理レプリケーション スロットを構成できます。

```yaml
slots:
  node_name1:
    type: physical
  node_name2:
    type: physical
  node_name3:
    type: physical
  ...
```

> [!WARNING]
> 永続レプリケーション スロットは、`primary`/`standby_leader` からレプリカ ノードにのみ同期されます。つまり、アプリケーションはリーダー ノードからのみそれらを使用することになっています。これらをレプリカ ノードで使用すると、クラスター内の他のすべてのノードで `pg_wal` が無制限に増加します。この規則の例外は、Patroni メンバー名 (Patroni によって作成および維持される) に一致する物理スロットです。これらはノード間のレプリケーションに使用されるため、すべてのノード間で同期されます。

> [!WARNING]
> `nostream` タグをスタンバイに設定すると、ノード自体とそのすべてのカスケード レプリカ (存在する場合) 上の永続論理レプリケーション スロットのコピーと同期が無効になります。
