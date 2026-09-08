---
title: "単独インスタンスをPatroniクラスターに移行する"
linkTitle: "既存クラスターの移行"
weight: 140
icon: fa-solid fa-truck-moving
description: "既存のPostgreSQLデータをPatroniクラスターに移行する手順。"
module: [PATRONI]
categories: [タスク]
aliases: [/docs/patroni/existing_data/]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
このセクションでは、単独のPostgreSQLインスタンスをPatroniクラスターに移行する手順を説明します。

既存のPostgreSQLインスタンスを使用せずにPatroniクラスターを構築する場合は、[実行と設定](/ja/patroni/readme#running_configuring)を参照してください。

--------

## 手順 {#procedure}

既存のPostgresクラスターをPatroni管理のクラスターに移行する手順の概要を以下に示します。既存クラスターのすべてのノードが稼働中であり、移行中にPostgresの設定を変更する予定が*ない*ことを前提とします。

1. Patroni設定の[authentication](/ja/patroni/config/yaml#postgresql_settings)セクションの説明に従い、Postgresユーザーを作成します。以下のコードブロックにユーザー作成用のSQLコマンド例を示します。ユーザー名とパスワードを環境に合わせて置き換えてください。必要なユーザーがすでに存在する場合は、この手順を省略できます。

    ``` sql
    -- Patroni superuser
    -- Replace PATRONI_SUPERUSER_USERNAME and PATRONI_SUPERUSER_PASSWORD accordingly
    CREATE USER PATRONI_SUPERUSER_USERNAME WITH SUPERUSER ENCRYPTED PASSWORD 'PATRONI_SUPERUSER_PASSWORD';

    -- Patroni replication user
    -- Replace PATRONI_REPLICATION_USERNAME and PATRONI_REPLICATION_PASSWORD accordingly
    CREATE USER PATRONI_REPLICATION_USERNAME WITH REPLICATION ENCRYPTED PASSWORD 'PATRONI_REPLICATION_PASSWORD';

    -- Patroni rewind user, if you intend to enable use_pg_rewind in your Patroni configuration
    -- Replace PATRONI_REWIND_USERNAME and PATRONI_REWIND_PASSWORD accordingly
    CREATE USER PATRONI_REWIND_USERNAME WITH ENCRYPTED PASSWORD 'PATRONI_REWIND_PASSWORD';
    GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO PATRONI_REWIND_USERNAME;
    ```

2. すべてのPostgresノードで以下の手順を実行します。1つのノードですべての手順を終えてから次のノードへ進んでください。最初にプライマリーノードを処理し、その後各スタンバイノードを処理します。

    1.  systemd経由でPostgresを実行している場合は、Postgresのsystemdユニットを無効にします。以後はPatroniがPostgresデーモンの起動と停止を管理するためです。
    2.  PatroniのYAML設定ファイルを作成します。[Patroni設定の生成・検証ツール](/ja/patroni/config#validate_generate_config)を使用できます。
        - **注意（プライマリーノード固有）：** クラスターメンバー間のレプリケーションでレプリケーションスロットを使用している場合は、`use_slots`を有効にし、`slots`設定項目で既存のスロットを永続スロットとして設定することを推奨します。`use_slots`を有効にすると、Patroniはメンバー間のレプリケーション用スロットを自動作成し、認識していないスロットを削除する点に注意してください。ここで永続スロットを使用する目的は、Patroniへの移行中も既存のスロットを保持することです。詳細は[動的設定](/ja/patroni/config/dynamic#dynamic)を参照してください。
    3.  `patroni`のsystemdサービスユニットでPatroniを起動します。Postgresがすでに稼働していることを自動検出し、インスタンスの監視を開始します。

3. Postgresの「起動処理」をPatroniに引き継ぎます。そのために、[patronictl restart cluster-name member-name](/ja/patroni/patronictl#patronictl_restart_parameters)コマンドでクラスターメンバーを再起動する必要があります。停止時間を最小限にするには、この手順を次のように分けるとよいでしょう。

    1.  スタンバイノードを直ちに再起動します。
    2.  プライマリーノードの再起動をメンテナンス時間帯に予約します。

4. 手順`1.2.`で永続スロットを設定した場合、Patroniが作成したスロットの`restart_lsn`が対応するメンバーの元のスロットの`restart_lsn`に追いついたら、[patronictl edit-config cluster-name](/ja/patroni/patronictl#patronictl_edit_config_parameters)コマンドでそれらを`slots`設定から削除してください。`slots`設定から削除することで、元のスロットが不要になった際にPatroniがクラスターから削除できるようになります。以下は2つのスロットの`restart_lsn`を確認し、比較するクエリーの例です。

    ``` sql
    -- Assume original_slot_for_member_x is the name of the slot in your original
    -- cluster for replicating changes to member X, and slot_for_member_x is the
    -- slot created by Patroni for that purpose. You need restart_lsn of
    -- slot_for_member_x to be >= restart_lsn of original_slot_for_member_x
    SELECT slot_name,
           restart_lsn
    FROM pg_replication_slots
    WHERE slot_name IN (
        'original_slot_for_member_x',
        'slot_for_member_x'
    )
    ```

<a id="major_upgrade"></a>

## PostgreSQLのメジャーバージョンアップグレード {#major-upgrade-of-postgresql-version}

現在、メジャーアップグレードを実行できる唯一の方法は次のとおりです。

1. Patroniを停止します。
2. プライマリーノードでPostgreSQLのバイナリを更新し、[pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html)を実行します。
3. patroni.ymlを更新します。
4. DCSからinitializeキーを削除するか、クラスターの状態全体をDCSから削除します。後者は[patronictl remove cluster-name](/ja/patroni/patronictl#patronictl_remove_parameters)を実行することで実施できます。pg_upgradeはinitdbを実行し、新しいPostgreSQLシステム識別子を持つデータベースを作成するため、この処理が必要です。
5. 前の手順でクラスターの状態を削除した場合は、古いデータディレクトリのpatroni.dynamic.jsonを新しいディレクトリにコピーするとよいでしょう。以前に設定したPostgreSQLパラメーターの一部を保持できます。
6. プライマリーノードでPatroniを起動します。
7. スタンバイノードでPostgreSQLのバイナリとpatroni.ymlを更新し、data_dirを消去します。
8. スタンバイノードでPatroniを起動し、レプリケーションの完了を待ちます。

PostgreSQLは、スタンバイノードでのpg_upgradeの実行をサポートしていません。処理内容を十分理解している場合は、スタンバイノードのdata_dirを消去する代わりに、<https://www.postgresql.org/docs/current/pgupgrade.html>で説明されているrsyncの手順を試すこともできます。ただし、最も安全な方法はPatroniにデータをレプリケーションさせることです。

--------

## よくある質問 {#faq}

- Patroniの起動時に、PostgreSQLのポートにバインドできないというエラーが出ます。

  `postgresql.conf`の`listen_addresses`と`port`、および`patroni.yml`の`postgresql.listen`を確認する必要があります。`pg_hba.conf`でこのアクセスを許可することも忘れないでください。

- Patroniにノードの再起動を要求すると、PostgreSQLが`could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory`というエラーを表示します。

  PostgreSQL設定の管理方法に応じて、いくつかの原因が考えられます。`postgresql.config_dir`を指定している場合、Patroniが[bootstrap](/ja/patroni/config/yaml#bootstrap_settings)セクションの設定から`pg_hba.conf`を生成するのは、新しいクラスターをブートストラップするときだけです。この状況では`PGDATA`が空でなかったため、ブートストラップは行われていません。このファイルを事前に用意する必要があります。
