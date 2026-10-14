---
title: "スタンバイクラスター"
weight: 80
icon: fa-solid fa-clone
description: "スタンバイクラスターの設定、動作、リモートのプライマリーからのレプリケーション。"
module: [PATRONI]
categories: [タスク]
upstream_link: "https://patroni.readthedocs.io/en/latest/standby_cluster.html"
---

<a id="standby_cluster"></a>
Patroniは、「スタンバイクラスター」と呼ばれる機能を使用して、リモートのデータセンター（リージョン）へのカスケードレプリケーションも実行できます。この種類のクラスターには、次の要素があります。

- 「スタンバイリーダー」。リモートのノードからレプリケーションを行う点を除き、通常のクラスターリーダーとほぼ同じように動作します。
- スタンバイリーダーからレプリケーションを行うカスケードレプリカ。

スタンバイリーダーはDCS内のリーダーロックを保持し、更新します。リーダーロックが期限切れになると、カスケードレプリカは選出を行い、スタンバイの中から別のリーダーを選びます。

スタンバイクラスターと、そのレプリケーション元のプライマリークラスターの間には、これ以外の関係はありません。特に、同じDCSを使用する場合、同じDCSスコープを共有してはなりません。互いに知っているのはレプリケーション情報だけです。また、プライマリークラスターで実行した[patronictl_list](/ja/patroni/patronictl#patronictl_list)や[patronictl_topology](/ja/patroni/patronictl#patronictl_topology)の出力に、スタンバイクラスターは表示されません。

柔軟性を確保するため、[standby_cluster](/ja/patroni/standby_cluster#standby_cluster)セクションに[create_replica_methods](/ja/patroni/replica_bootstrap#custom_replica_creation)キーを指定することで、クラスターが「スタンバイモード」のときにレプリカを作成し、WALレコードをリカバリーする方法を指定できます。これは、クラスターを切り離して通常のクラスターとして動作させるときのレプリカ作成とは別のものです。通常のクラスターでの作成は、`postgresql`セクションの`create_replica_methods`で制御します。「スタンバイ」と「通常」の両方の`create_replica_methods`は、`postgresql`セクション内のキーを参照します。

このようなクラスターを構成するには、Patroniの構成に[standby_cluster](/ja/patroni/standby_cluster#standby_cluster)セクションを指定する必要があります。

```yaml
bootstrap:
    dcs:
        standby_cluster:
            host: 1.2.3.4
            port: 5432
            primary_slot_name: patroni
            create_replica_methods:
            - basebackup
```

これらのオプションはクラスターのブートストラップ時に一度だけ適用され、その後はDCSを通じてのみ変更できることに注意してください。

PatroniはリモートのプライマリーのPGDATA内に`postgresql.conf`または`postgresql.conf.backup`があることを想定しており、ベースバックアップ後に見つからなければ起動しません。リモートのプライマリーが別の場所に`postgresql.conf`を保存している場合、PGDATAへのコピーは利用者の責任で行ってください。

スタンバイクラスターでレプリケーションスロットを使用する場合は、プライマリークラスターにも対応するレプリケーションスロットを作成しなければなりません。スタンバイクラスターの実装では、自動的には作成されません。プライマリークラスターでPatroniの永続レプリケーションスロット機能を使用すると、`primary_slot_name`と同じ名前、または`primary_slot_name`が指定されていない場合はそのデフォルト値の名前を持つレプリケーションスロットを維持できます。

リモートサイトにプライマリーへ接続する単一のエンドポイントがない場合は、`standby_cluster.host`セクションにソースクラスターの全ホストを列挙できます。`standby_cluster.host`にカンマ区切りで複数のホストが含まれる場合、Patroniは次の処理を行います。

- スタンバイリーダーノードの`primary_conninfo`に`target_session_attrs=read-write`を追加します。
- `pg_rewind`を実行する必要があるかどうかを判断するときや、スタンバイクラスターの全ノードで`pg_rewind`を実行するときに、`target_session_attrs=read-write`を使用します。
- `pg_rewind`を正常に動作させるには、`data page checksums`（`initdb`の`--data-checksums`オプション）を有効にしてクラスターを初期化するか、`wal_log_hints`を`on`に設定する、あるいはその両方を行わなければならないことに注意してください。そうでなければ、`pg_rewind`は正しく動作しません。

別のスタンバイクラスターや、プライマリークラスターのスタンバイメンバーからスタンバイクラスターへレプリケーションすることも可能です。その場合は、`standby_cluster.host`セクションに単一のホストを定義する必要があります。ただし、この場合はスタンバイクラスターで`pg_rewind`の実行に失敗することに注意してください。

> [!WARNING]
> メンバー名（各ノードのPatroni構成の`name`フィールド）は、プライマリークラスターと、それに接続するすべてのスタンバイクラスターにわたって一意でなければなりません。
>
> Patroniはメンバー名を使用してプライマリー上の`synchronous_standby_names`を設定します。メンバー名は、`pg_stat_replication`内の各レプリケーション接続の`application_name`にもなります。スタンバイクラスターのノードとプライマリークラスターのメンバーが同じ名前を持つ場合、PostgreSQLには同一の`application_name`値を持つ接続が二つ見えることになります。この曖昧さにより、PostgreSQLが本来意図したプライマリークラスターのメンバーではなく、スタンバイクラスターの接続を使用して同期レプリケーションの要件を満たす可能性があります。その結果、正しいスタンバイにトランザクションが永続化されていないにもかかわらず、PostgreSQLが同期コミット済みとして早まって応答してしまいます。
>
> これは検出されない障害です。レプリケーションは継続し、エラーもログに記録されませんが、実際には有効な同期スタンバイがない状態でクラスターが動作しているため、プライマリーが障害を起こすとデータを失う可能性があります。
