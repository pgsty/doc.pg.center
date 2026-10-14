---
title: "レプリケーションモード"
weight: 70
icon: fa-solid fa-share-nodes
description: "Patroniが管理する非同期・同期レプリケーションモード。"
module: [PATRONI]
categories: [概念]
upstream_link: "https://patroni.readthedocs.io/en/latest/replication_modes.html"
---

<a id="replication_modes"></a>
PatroniはPostgreSQLのストリーミングレプリケーションを使用します。ストリーミングレプリケーションの詳細は[Postgresのドキュメント](http://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION)を参照してください。デフォルトでは、PatroniはPostgreSQLに非同期レプリケーションを設定します。レプリケーション方式の選択は業務上の要件によって異なります。非同期と同期の両方式、および他の高可用性ソリューションを検討し、最適なものを判断してください。

--------

## 非同期モードの永続性 {#asynchronous-mode-durability}

非同期モードでは、可用性を確保するために、コミット済みトランザクションの一部が失われることを許容します。プライマリーサーバーに障害が発生した場合や、その他の理由で利用不能になった場合、Patroniは十分に正常なスタンバイを自動的にプライマリーへ昇格させます。そのスタンバイにレプリケーションされていないトランザクションは、プライマリー上の「分岐したタイムライン」に残り、事実上リカバリーできません[^1]。

失われる可能性があるトランザクション量は、`maximum_lag_on_failover`パラメーターで制御します。プライマリーのトランザクションログ位置をリアルタイムには取得しないため、フェイルオーバー時に失われるデータ量の実際の最悪値は、`maximum_lag_on_failover`バイトのトランザクションログに、直近の`ttl`秒間（平均では`loop_wait`/2秒間）に書き込まれた量を加えたものです。ただし、通常の定常状態でのレプリケーション遅延は1秒を大幅に下回ります。

デフォルトでは、Patroniはリーダー選出時にレプリカの現在のタイムラインを考慮しません。これは状況によっては望ましくない動作です。`check_timeline`を`true`に設定すると、タイムラインがクラスターで最後に確認されたものより古いノードや、タイムラインを特定できないノードが新しいリーダーになることを防げます。

--------

## PostgreSQLの同期レプリケーション {#postgresql-synchronous-replication}

Patroniでは、Postgresの[同期レプリケーション](http://www.postgresql.org/docs/current/static/warm-standby.html#SYNCHRONOUS-REPLICATION)を使用できます。同期レプリケーションでは、接続元のクライアントに成功を返す前に、書き込みがセカンダリーに保存されたことを確認し、クラスター全体の整合性を確保します。その代償として、書き込みのレイテンシーが増加し、スループットが低下します。このスループットはネットワーク性能の影響を受けます。

ホスティング型のデータセンター環境（AWS、Rackspaceなど、または自分で制御できないネットワーク）では、同期レプリケーションにより書き込み性能の変動が大幅に増加します。リーダーからフォロワーに到達できなくなると、リーダーは実質的に読み取り専用になります。

簡単な同期レプリケーションのテストを有効にするには、YAML設定ファイルの`parameters`セクションに次の行を追加します。

```yaml
synchronous_commit: "on"
synchronous_standby_names: "*"
```

PostgreSQLの同期レプリケーションを使用する場合は、ホスト1台が故障しても書き込み可用性を確保できるよう、少なくとも3つのPostgresデータノードを使用してください。

PostgreSQLの同期レプリケーションを使用しても、あらゆる状況でトランザクションが一切失われないことを保証するわけではありません。プライマリーと現在同期レプリカとして動作しているセカンダリーが同時に故障すると、すべてのトランザクションを保持しているとは限らない3つ目のノードが昇格します。

<a id="synchronous_mode"></a>

--------

## 同期モード {#synchronous-mode}

コミット済みトランザクションの損失を許容できない場合は、Patroniの[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)を有効にできます。[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)を有効にすると、クライアントにコミット成功を返した可能性があるすべてのトランザクションをスタンバイが保持していると確信できない限り、Patroniはそのスタンバイを昇格させません[^2]。つまり、一部のサーバーが利用可能でも、システムへの書き込みができない場合があります。システム管理者は、トランザクションが失われる場合でも、手動フェイルオーバーコマンドでスタンバイを昇格させることができます。

[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)を有効にしても、あらゆる状況で複数ノードにコミットが永続化されることを保証するわけではありません。適切なスタンバイが利用できない場合も、プライマリーは書き込みを受け付けますが、そのレプリケーションは保証しません。このモードでプライマリーが故障すると、スタンバイは昇格しません。以前のプライマリーのホストが復帰すると、管理者が手動フェイルオーバーを行っていない限り、自動的に昇格します。この動作により、2ノードのクラスターでも同期モードを使用できます。

[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)が有効で厳密モードが無効な状態で、唯一の同期スタンバイがクラッシュすると、Patroniの次の処理サイクルでプライマリーを単独動作モードへ切り替えるまで、コミットはブロックされます。書き込みの遅延は最悪で`ttl`秒、平均で`loop_wait`/2秒です。スタンバイを手動で停止または再起動する場合は、コミット処理が中断されません。PostgreSQLの停止を開始する前に、スタンバイは同期スタンバイの役割から自身を外すようプライマリーに通知します。

各書き込みが少なくとも2つのノードに永続保存されることを必ず保証する必要がある場合は、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)に加えて`synchronous_mode_strict`を有効にしてください。このパラメーターは、同期スタンバイの候補が存在しない場合にPatroniがプライマリーの同期レプリケーションを無効にすることを防ぎます。同期コミットは同期レプリカが利用可能になるまでブロックされます。`synchronous_commit`が`off`または`local`のトランザクションは、この待機を回避します。

優先順位に基づく同期モード（`synchronous_mode: on`）で厳密モードが有効であり、適切な同期スタンバイが利用できない場合、Patroni 4.1.5は`synchronous_standby_names`を`*`に設定し、警告`"No standbys available!"`を出力します。これにより、コミットは同期スタンバイを待ち続けます。このワイルドカードは、確認応答の送信元を`/sync`に以前記録されていたメンバー名に限定しません。

`nosync`タグをtrueに設定すると、Patroniはそのスタンバイを同期スタンバイの選択対象から除外します。低速なネットワーク経由で接続されており、同期スタンバイになると性能が低下するスタンバイには、この設定を推奨します。`nostream`タグをtrueに設定しても同じ効果があります。

同期モードは、`patronictl edit-config`コマンドまたはPatroniのRESTインターフェースで有効・無効を切り替えられます。手順は[動的設定](/ja/patroni/config/dynamic#dynamic)を参照してください。

注意：PostgreSQLの同期レプリケーションの実装上、`synchronous_mode_strict`を使用していてもトランザクションが失われる可能性があります。クライアントのタイムアウトによるキャンセルパケットやバックエンド障害により、レプリケーションの確認を待っているPostgreSQLバックエンドがキャンセルされると、そのトランザクションの変更は他のバックエンドから見えるようになります。これらの変更はまだレプリケーションされていないため、スタンバイが昇格すると失われる可能性があります。

--------

## 同期レプリケーション係数 {#synchronous-replication-factor}

Patroniは`synchronous_node_count`パラメーターで同期スタンバイデータベースの数を管理します。デフォルトは`1`です。[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)が`off`の場合、このパラメーターは効果を持ちません。有効な場合は、Patroniが`synchronous_node_count`に基づいて同期スタンバイデータベースの正確な数を管理し、メンバーの参加・離脱に合わせてDCSの状態とPostgreSQLの`synchronous_standby_names`を調整します。適格なノードが不足している場合、Patroniが使用する同期スタンバイは要求された数より少なくなることがあります。ただし、厳密なクォーラムモードでは、コミットは設定された数のスタンバイからの確認応答を待ち続けます。

--------

## 同期ノードの最大遅延 {#maximum-lag-on-synchronous-node}

デフォルトでは、Patroniは他のノードの方が先に進んでいても、`pg_stat_replication`ビューで`synchronous`とされているノードを維持します。これは`synchronous_standby_names`の変更回数を最小限にするためです。この動作を変更するには、`maximum_lag_on_syncnode`パラメーターを使用できます。レプリカを「同期」とみなせる遅延量の上限を制御します。

スタンバイが複数ある場合、Patroniはレプリカの最大LSNを使用します。それ以外の場合は、リーダーの現在のWAL LSNを使用します。デフォルトは`-1`で、値が`0`以下の場合、Patroniは正常でない同期スタンバイを入れ替えません。トランザクション量が多いときに同期スタンバイが頻繁に入れ替わらないよう、十分大きな値を設定してください。

--------

## 同期モードの実装 {#synchronous-mode-implementation}

同期モードでは、PatroniはDCSの`/sync`キーに、最新のプライマリーと現在の同期スタンバイデータベースを含む同期状態を保持します。この状態を厳密な順序制約に従って更新し、次の不変条件を保証します。

- 書き込みトランザクションを受け付けられるノードは、常に最新のリーダーとして記録されていなければなりません。PatroniのクラッシュやPostgreSQLが停止しない状況は、この不変条件に違反する原因になります。
- DCSの`/sync`キーに同期スタンバイとして公開されている限り、そのノードはPostgreSQLでも同期スタンバイに設定されていなければなりません。
- リーダーでも現在の同期スタンバイでもないノードは、自動的に自身を昇格させることができません。

同期スタンバイの集合が空でない場合、Patroniは`synchronous_node_count`に基づき、1つ以上の同期スタンバイノードを`synchronous_standby_names`に設定します。

PatroniはHAループの反復ごとに同期スタンバイの選択を見直します。現在の同期スタンバイが接続されており、同期状態の解除を要求していなければ、その選択を維持します。それ以外の場合は、同期可能なクラスターメンバーのうち、レプリケーションが最も先に進んでいるものを選びます。

### 例: {#example}

#### DCSの`/config`キー {#config-key-in-dcs}

```yaml
synchronous_mode: on
synchronous_node_count: 2
...
```

#### DCSの`/sync`キー {#sync-key-in-dcs}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2"
}
```

#### postgresql.conf {#postgresqlconf}

```ini
synchronous_standby_names = 'FIRST 2 (node1,node2)'
```

上記の例では、同期していると確認されているのは`node1`と`node2`だけであり、プライマリー（`node0`）が故障した場合に自動昇格が許可されるのも、これらのノードだけです。

<a id="quorum_mode"></a>

--------

## クォーラムコミットモード {#quorum-commit-mode}

PostgreSQL v10以降、Patroniはクォーラムに基づく同期レプリケーションをサポートしています。

このモードでは、Patroniは最後に確認されたプライマリー、クォーラムに必要なノード数、現在クォーラムへの投票資格があるノードを含む同期状態をDCSに保持します。定常状態では、投票ノードはリーダーとすべての同期スタンバイです。この状態を、ノードの昇格と`synchronous_standby_names`に関する厳密な順序制約に従って更新します。その結果、クォーラムを構成できる投票ノードのどの部分集合にも、最後に成功したコミットを保持するノードが少なくとも1つ含まれることを常に保証します。

PatroniはHAループの反復ごとに、ノードの可用性と要求されたクラスター設定に基づいて、同期スタンバイとクォーラムの選択を見直します。PostgreSQL 9.6より新しいバージョンでは、適格なすべてのノードを、レプリケーションがリーダーに追いつき次第、同期スタンバイに追加します。

クォーラムコミットでは、あるスタンバイへのレプリケーション遅延が増えても、他のスタンバイが補えるため、通常の運用中も含めて最悪時のレイテンシーを減らせます。

クォーラムに基づく同期モードを有効にするには、`patronictl edit-config`コマンドまたはPatroniのRESTインターフェースで、[synchronous_mode](/ja/patroni/replication_modes#synchronous_mode)を`quorum`に設定します。手順は[動的設定](/ja/patroni/config/dynamic#dynamic)を参照してください。

`synchronous_node_count`、`maximum_lag_on_syncnode`、`synchronous_mode_strict`などの他のパラメーターは、`synchronous_mode=on`の場合と同様に機能します。

クォーラムコミットモードで同期スタンバイの集合が空であり、厳密モードで`N`台のスタンバイからの確認応答が必要な場合、Patroni 4.1.5は`synchronous_standby_names`を`ANY N (*)`に設定します。

### 例: {#example-1}

#### DCSの`/config`キー {#config-key-in-dcs-1}

```yaml
synchronous_mode: quorum
synchronous_node_count: 2
...
```

#### DCSの`/sync`キー {#sync-key-in-dcs-1}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2,node3",
    "quorum": 1
}
```

#### postgresql.conf {#postgresqlconf-1}

```ini
synchronous_standby_names = 'ANY 2 (node1,node2,node3)'
```

上記の例でプライマリー（`node0`）が故障した場合、`node1`、`node2`、`node3`のうち2つは最新のトランザクションを受信していますが、それがどのノードかは分かりません。`node1`が最新のトランザクションを受信しているかを判断するには、`node2`と`node3`のうち**少なくとも**1つ（`/sync`キーの`quorum=1`）のLSNと比較する必要があります。そのうち少なくとも1つより`node1`が遅れていなければ、`node1`を昇格してもユーザーに見えるデータ損失が生じないことを保証できます。

[^1]: データ自体は残っていますが、復元にはデータリカバリーの専門家による手作業が必要です。`use_pg_rewind`で巻き戻しを許可している場合、故障したプライマリーをクラスターに再参加させるために、分岐したタイムラインは自動的に消去されます。ただし、`use_pg_rewind`が正しく動作するには、`data page checksums`（`initdb`の`--data-checksums`オプション）を有効にしてクラスターを初期化するか、`wal_log_hints`を`on`に設定するか、その両方が必要です。

[^2]: クライアントは、PostgreSQLの`synchronous_commit`設定でトランザクションごとに動作を変更できます。`synchronous_commit`が`off`または`local`のトランザクションは、フェイルオーバーで失われる可能性がありますが、レプリケーション遅延によってブロックされません。
