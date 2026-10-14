---
title: "レプリカのイメージングとブートストラップ"
linkTitle: "レプリカのブートストラップ"
weight: 60
icon: fa-solid fa-boxes-stacked
description: "レプリカのイメージング、ブートストラップ、およびカスタム レプリカ作成のワークフロー。"
module: [PATRONI]
categories: [タスク]
upstream_link: "https://patroni.readthedocs.io/en/latest/replica_bootstrap.html"
---

<a id="replica_imaging_and_bootstrap"></a>
Patroni を使用すると、新しいレプリカの作成をカスタマイズできます。また、新しい空のクラスターがブートストラップされるときに何が起こるかの定義もサポートします。 2 つの区別は明確に定義されています。Patroni は、`initialize` キーがクラスターの DCS に存在する場合にのみレプリカを作成します。 `initialize` キーがない場合、Patroni は初期化キー ロックを取得する最初のノードで排他的にブートストラップを呼び出します。

<a id="custom_bootstrap"></a>

--------

## ブートストラップ {#bootstrap}

PostgreSQL は、新しいクラスターを初期化するための `initdb` コマンドを提供し、 Patroni はデフォルトでそれを呼び出します。場合によっては、特に既存のクラスターのコピーとして新しいクラスターを作成する場合、組み込みメソッドをカスタム アクションに置き換える必要があります。 Patroni は、新しいクラスターをブートストラップするためのユーザー定義スクリプトの実行をサポートし、クラスターの名前とデータ ディレクトリへのパスなど、いくつかの必要な引数を指定します。これは、Patroni 構成の `bootstrap` セクションで構成されます。たとえば:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script> [param1 [, ...]]
        keep_existing_recovery_conf: False
        no_params: False
        recovery_conf:
            recovery_target_action: promote
            recovery_target_timeline: latest
            restore_command: <method_specific_restore_command>
```

各カスタムブートストラップメソッドは、`method`で名前を指定し、その名前のセクションで`command`を定義しなければなりません。特別な `initdb` メソッドを使用してデフォルトの動作をトリガーできます。この場合、`method` パラメーターは完全に省略できます。 `command`には、絶対パス、Patroniの作業ディレクトリを基準とした相対パス、または`PATH`で利用可能なコマンド名を指定できます。構成ファイルで定義された固定パラメーターに加えて、Patroni はクラスター固有のパラメーターを 2 つ提供します。

`--scope`  
ブートストラップされるクラスターの名前

`--datadir`  
ブートストラップされるクラスター インスタンスのデータ ディレクトリへのパス

これら 2 つの追加フラグの受け渡しを無効にするには、特別な `no_params` パラメーターを `True` に設定します。

ブートストラップ スクリプトが `0` を返した場合、Patroni は、それによって生成された PostgreSQL インスタンスを構成して起動しようとします。中間ステップのいずれかが失敗するか、スクリプトがゼロ以外の値を返した場合、Patroni はブートストラップが失敗したものとみなし、その後クリーンアップして初期化ロックを解放し、別のノードにブートストラップの機会を与えます。

`recovery_conf` ブロックがカスタム ブートストラップ メソッドと同じセクションで定義されている場合、Patroni は、新しくブートストラップされたインスタンスを開始する前に `recovery.conf` を生成します (または、PostgreSQL \>= 12 を実行している場合は、Postgres 構成にリカバリ設定を設定します)。通常、このようなリカバリー構成には、`promote`に設定した`recovery_target_action`とともに、少なくとも1つの`recovery_target_*`パラメーターを含めることを推奨します。

`keep_existing_recovery_conf` が定義され、`True` に設定されている場合、Patroni は既存の `recovery.conf` ファイルが存在する場合は削除しません (PostgreSQL \<= 11)。同様に、その場合、Patroni は、既存の `recovery.signal` または `standby.signal` が存在する場合は削除しません。また、構成されたリカバリ設定 (PostgreSQL \>= 12) をオーバーライドすることもありません。これは、適切なリカバリ構成を生成する pgBackRest などのツールを使用してバックアップからブートストラップする場合に便利です。

それに加えて、カスタム ブートストラップ メソッド設定で指定された追加のキーと値のペアは、引数として `--name=value` 形式で `command` に渡されます。たとえば:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script>
        arg1: value1
        arg2: value2
```

この構成では、`command`が追加の`--arg1=value1 --arg2=value2`コマンドライン引数を付けて呼び出されます。

> [!NOTE]
> ブートストラップメソッドは連鎖して実行されません。また、指定したメソッドが失敗してもデフォルトのメソッドにフォールバックしません。

たとえば、次のような構成を使用して、Barman バックアップから新しい Patroni クラスターをブートストラップできます。

```yaml
bootstrap:
    method: barman
    barman:
        keep_existing_recovery_conf: true
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
```

> [!NOTE]
> `patroni_barman recover` では、バックアップ API を介してリモート `barman recover` を実行できるように、Barman ホストに Barman と `pg-backup-api` の両方が構成されている必要があります。上の例では、使用可能なパラメータのサブセットを使用しています。 `patroni_barman recover --help` を実行すると、詳細情報を取得できます。

<a id="custom_replica_creation"></a>

--------

## レプリカの構築 {#building-replicas}

Patroni は、新しいレプリカを作成するために、実証済みの `pg_basebackup` を使用します。実行中のコピー元PostgreSQLインスタンスが必要であり、古いバックアップファイルを削除する機能は組み込まれていません。 `WAL-E`、`pgBackRest`、`Barman` などの他のバックアップ ソリューションを好んだり、単に独自のスクリプトを使用したりする人もいます。これらすべてのユースケースに対応するために、Patroni は新しいレプリカのクローンを作成するためのカスタム スクリプトの実行をサポートしています。これらは `postgresql` 構成ブロックで構成されます。

```yaml
postgresql:
    create_replica_methods:
        - <method name>
    <method name>:
        command: <command name>
        keep_data: True
        no_params: True
        no_leader: 1
```

例: wal_e

```yaml
postgresql:
    create_replica_methods:
        - wal_e
        - basebackup
    wal_e:
        command: patroni_wale_restore
        no_leader: 1
        envdir: '{{WALE_ENV_DIR}}'
        use_iam: 1
    basebackup:
        max-rate: '100M'
```

例: pgbackrest

```yaml
postgresql:
    create_replica_methods:
        - pgbackrest
        - basebackup
    pgbackrest:
        command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
        keep_data: True
        no_params: True
    basebackup:
        max-rate: '100M'
```

例: Barman

```yaml
postgresql:
    create_replica_methods:
        - barman
        - basebackup
    barman:
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
    basebackup:
        max-rate: '100M'
```

> [!NOTE]
> `patroni_barman recover` では、バックアップ API を介してリモート `barman recover` を実行できるように、Barman ホストに Barman と `pg-backup-api` の両方が構成されている必要があります。上の例では、使用可能なパラメータのサブセットを使用しています。 `patroni_barman recover --help` を実行すると、詳細情報を取得できます。

`create_replica_methods` は、使用可能なレプリカ作成メソッドとその実行順序を定義します。 Patroni は、0 を返す最初のもので停止します。各メソッドには、構成ファイル内に個別のセクションを用意し、実行するコマンドと渡すカスタムパラメーターを記載することを推奨します。すべてのパラメータは `--name=value` 形式で渡されます。ユーザー定義のパラメーターの他に、Patroni はクラスター固有のパラメーターをいくつか提供します。

`--scope`  
このレプリカが属するクラスター

`--datadir`  
レプリカのデータ ディレクトリへのパス

`--role`  
常に 'replica'

`--connstring`  
クローン作成元のクラスター メンバーに接続するための接続文字列 (プライマリーまたは他のレプリカ)。接続文字列内のユーザーは、SQL およびレプリケーション プロトコル コマンドを実行できます。

特別な`no_leader`パラメーターを有効にすると、実行中のリーダーまたはレプリカがない場合でも、Patroni がレプリカ作成メソッドを呼び出すことができます。その場合、接続文字列には空の文字列が渡されます。これは、以前に実行していたクラスターをバイナリ バックアップから復元する場合に便利です。

特別な`keep_data`パラメーターを有効にすると、復元を呼び出す前に PGDATA フォルダーをクリーンアップしないように Patroni に指示します。

特別な`no_params`パラメーターを有効にすると、カスタムコマンドへのクラスター固有のパラメーターの自動追加が無効になります。ユーザー定義のパラメーターは引き続き渡されます。

`basebackup` メソッドは特殊なケースです。`create_replica_methods` が空の場合に使用されますが、`create_replica_methods` メソッドの中に明示的にリストすることは可能です。このメソッドは、`pg_basebackup` を使用して新しいレプリカを初期化し、`clonefrom` タグが付いたレプリカがない限り、ベース バックアップはリーダーから取得されます。その場合、そのようなレプリカの 1 つが pg_basebackup のオリジンとして使用されます。設定なしで動作します。ただし、`basebackup` 構成セクションを指定することは可能です。他のメソッド設定と同じルールが適用されます。つまり、長い (-- 付き) オプションのみを指定する必要があります。Patroniは、接続設定の上書きや、tar形式またはクライアント側で圧縮されたバックアップを作成するオプションを受け付けません。PostgreSQL 15以降では、`compress: server-gzip`または`compress: server-zstd`によるサーバー側の圧縮をサポートしています。Patroniは、自身が制御するオプションやサーバー側の圧縮以外の圧縮設定を除外しますが、すべてのオプション名と値を完全に検証するわけではありません。また、WAL フォルダーにシンボリックリンクが使用されている場合、レプリカの構築または再初期化後にシンボリックリンクが保持されるように、オプションとして正しい `--waldir` パスを指定するのはユーザーの責任であることに注意してください。ただし、このオプションは v10 以降でのみサポートされています。

`basebackup` パラメータは、マップ (キーと値のペア) または要素のリストとして指定できます。各要素は、キーと値のペアまたは単一のキー (値を受け取らないオプションの場合、たとえば `--verbose`) のいずれかになります。これら 2 つの例を見てみましょう。

```yaml
postgresql:
    basebackup:
        max-rate: '100M'
        checkpoint: 'fast'
```

そして

```yaml
postgresql:
    basebackup:
        - verbose
        - max-rate: '100M'
        - waldir: /pg-wal-mount/external-waldir
```

すべてのレプリカ作成メソッドが失敗した場合、Patroni は次のイベント ループ サイクル中にすべてのメソッドを順番に再試行します。
