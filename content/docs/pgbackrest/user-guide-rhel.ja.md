---
title: "ユーザーガイド（RHEL）"
linkTitle: "ユーザーガイド（EL）"
weight: 30
description: "RHEL、Rocky、AlmaLinux向けのpgBackRestの設定と使用方法を手順に沿って説明します。"
icon: fa-brands fa-redhat
module: [PGBACKREST]
categories: [チュートリアル]
aliases: [/pgbackrest/user-guide-rhel/]
upstream_link: "https://pgbackrest.org/user-guide-rhel.html"
---

--------

## はじめに {#introduction}

このユーザーガイドは、各セクションが前のセクションを前提としているため、最初から順に読むことを想定しています。たとえば、[リストア](#restore-1)のセクションは、[クイックスタート](#quick-start)で行う設定を前提としています。pgBackRestを起動して運用できるようになった後は必要な箇所を参照できますが、初回は順に読み進めることをお勧めします。

このガイドの例はRHELとPostgreSQL 14を対象としていますが、どのUnixディストリビューションやPostgreSQLバージョンにも比較的容易に応用できます。OS固有のコマンドは、PostgreSQLクラスターの作成、起動、停止、削除に使うものだけです。pgBackRestのコマンドはどのUnixシステムでも同じですが、実行ファイルの場所は異なる場合があります。pgBackRestはPostgreSQLの各バージョンで一貫した動作を目指していますが、PostgreSQLのパス名、ファイル名、設定など、バージョン間の微妙な違いがこのガイドの例に現れる場合があります。

PostgreSQLの設定情報とドキュメントは、PostgreSQLの[マニュアル](http://www.postgresql.org/docs/14/static/index.html)を参照してください。

このユーザーガイドでは、ドキュメントの作成に少し変わった方法を採用しています。XMLソースからドキュメントをビルドする際、各コマンドを仮想マシンで実行します。そのため、記載された順序でコマンドが正しく動作することを高い確度で期待できます。必要に応じて出力を取得し、コマンドの下に表示しています。出力を載せていないのは、説明に関係しないか、説明の妨げになると判断したためです。

すべてのコマンドは、`root`と`postgres`の両ユーザーに対するsudo権限を持つ一般ユーザーで実行することを想定しています。各コマンドは対応するユーザーで直接実行することもでき、その場合は`sudo`の部分を取り除くだけで、ほかの変更は不要です。

--------

## 概念 {#concepts}

ここでは、pgBackRest、PostgreSQL、およびこのユーザーガイドに関係する概念を定義します。

### バックアップ {#backup}

バックアップとは、データベースクラスターの整合性のあるコピーです。リストアすることで、ハードウェア障害からの復旧、ポイントインタイムリカバリー、新しいスタンバイの起動に利用できます。

**フルバックアップ**：pgBackRestはデータベースクラスターの内容全体をバックアップにコピーします。データベースクラスターの最初のバックアップは必ずフルバックアップになります。pgBackRestはフルバックアップを常に直接リストアできます。フルバックアップの整合性は、そのバックアップ外のファイルに依存しません。

**差分バックアップ**：pgBackRestは、最後のフルバックアップ以降に変更されたデータベースクラスターのファイルだけをコピーします。差分バックアップのリストアでは、選択した差分バックアップの全ファイルと、その前のフルバックアップに含まれる変更のない該当ファイルをコピーします。差分バックアップはフルバックアップより少ないディスク容量で済みますが、リストアするには差分バックアップとフルバックアップの両方が有効でなければなりません。

**増分バックアップ**：pgBackRestは、最後のバックアップ（増分、差分、フルのいずれか）以降に変更されたデータベースクラスターのファイルだけをコピーします。増分バックアップには直前のバックアップ以降に変更されたファイルしか含まれないため、通常はフルバックアップや差分バックアップより大幅に小さくなります。差分バックアップと同様、増分バックアップのリストアには、依存先のバックアップも有効である必要があります。増分バックアップには最後のバックアップ以降のファイルしか含まれないため、リストアするには、前の差分バックアップまでさかのぼるすべての増分バックアップ、その差分バックアップ、およびその前のフルバックアップがすべて有効でなければなりません。差分バックアップが存在しない場合は、必ず存在する前のフルバックアップまでのすべての増分バックアップと、そのフルバックアップ自体が有効でなければなりません。

### リストア {#restore}

リストアとは、稼働するデータベースクラスターとして起動するシステムに、バックアップをコピーする操作です。正しくリストアするには、バックアップファイルと1つ以上のWALセグメントが必要です。

### 先行書き込みログ（WAL） {#write-ahead-log-wal}

WALは、コミット済みの変更が失われないことをPostgreSQLが保証するための仕組みです。トランザクションはWALに順次書き込まれ、その書き込みがディスクにフラッシュされるとコミットされたとみなされます。その後、バックグラウンドプロセスが変更をデータベースクラスターの本体ファイル（ヒープとも呼ばれます）に書き込みます。クラッシュ時にはWALを再生して、データベースの整合性を回復します。

WALは概念上は無限に続きますが、実際にはセグメントと呼ばれる16MBの個別ファイルに分割されます。WALセグメントの名前は`0000000100000A1E000000FE`という形式で、先頭の16進数8桁がタイムライン、続く16桁が論理シーケンス番号（LSN）を表します。

### 暗号化 {#encryption}

暗号化とは、適切なパスワード（パスフレーズとも呼ばれます）を指定しない限り認識できない形式にデータを変換する処理です。

pgBackRestはユーザーが指定したパスワードに基づいてリポジトリを暗号化し、リポジトリ内のデータへの不正アクセスを防ぎます。

--------

## pgBackRestのアップグレード {#upgrading-pgbackrest}


### pgBackRestをv2.xからv2.yにアップグレードする {#upgrading-pgbackrest-from-v2x-to-v2y}

v2.xからv2.yへのアップグレードは簡単です。リポジトリ形式は変わっていないため、ほとんどの環境では新しいバージョンのバイナリをインストールするだけで済みます。古いバージョンでサポートされていない新機能を使用していなければ、ダウングレードも可能です。

重要：

ローカルとリモートのpgBackRestのバージョンは完全に一致する必要があるため、同時にアップグレードすることをお勧めします。一致しない場合、バージョンが揃うまでWALアーカイブとバックアップは動作しません。その場合、次のエラーが報告されます：`[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`。

--------

## ビルド {#build}

pgBackRestはソースからビルドするより、パッケージからインストールすることをお勧めします。パッケージの詳細は[インストール](#installation)を参照してください。

ソースからビルドする場合は、本番環境ではなくビルド用ホストを使うことをお勧めします。ビルドに必要なツールの多くは、通常、本番環境にはインストールしないほうがよいものです。pgBackRestは単一の実行ファイルで構成されるため、ビルド後は簡単に別のホストにコピーできます。

build **⇒** pgBackRestのバージョン`2.59.3`を`/build`パスにダウンロードする

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** ビルドの依存パッケージをインストールする

```bash
sudo yum install meson gcc postgresql14-devel openssl-devel libxml2-devel \
       lz4-devel libzstd-devel bzip2-devel libssh2-devel systemd-devel
```

build **⇒** pgBackRestのビルドを設定してコンパイルする

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.59.3
ninja -C /build/pgbackrest
```

build **⇒** 必要に応じてスモークテストを実行し、pgBackRestが正しくビルドされたことを確認する

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               10.32s

Ok:                 1
       [filtered 6 lines of output]
```

--------

## インストール {#installation}

デモクラスターを配置してpgBackRestの例を実行するために、pg-primaryという新しいホストを作成します。

pgBackRestはソースからビルドするより、パッケージからインストールすることをお勧めします。パッケージからインストールする場合、このセクションの残りの手順は通常不要ですが、パッケージが一部のディレクトリを作成しなかったり、誤った権限を設定したりする可能性があります。その場合は、手動でディレクトリを作成したり権限を更新したりする必要がある場合があります。

pgBackRestのRHELパッケージは[yum.postgresql.org](http://yum.postgresql.org)から入手できます。

使用するディストリビューションやバージョン向けのパッケージがない場合は、[ソースからビルド](#build)し、ここに示す手順で手動インストールできます。

pg-primary **⇒** 依存パッケージをインストールする

```bash
sudo yum install postgresql-libs libssh2
```

pg-primary **⇒** ビルド用ホストからpgBackRestバイナリをコピーする

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRestには、ログディレクトリ、設定ディレクトリ、設定ファイルが必要です。

pg-primary **⇒** pgBackRestの設定ファイルとディレクトリを作成する

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

これでpgBackRestは正しくインストールされているはずですが、確認することをお勧めします。依存パッケージに不足があると、コマンドラインからpgBackRestを実行した際にエラーが発生します。

pg-primary **⇒** インストールが成功したことを確認する

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.59.3 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## クイックスタート {#quick-start}

クイックスタートでは、pgBackRestとPostgreSQLの基本設定を行い、`backup`、`restore`、`info`コマンドを紹介します。

### デモクラスターのセットアップ {#setup-demo-cluster}

デモクラスターの作成は任意ですが、このユーザーガイドのコマンド例がデモクラスターを参照するため、特に初めて使用する場合は作成を強くお勧めします。例では、デモクラスターがデフォルトのポート（5432）で稼働していることを前提としています。まだ設定が必要なため、クラスターの起動は後のセクションで行います。

pg-primary **⇒** デモクラスターを作成する

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

RHELではデフォルトでログファイル名に曜日を含めます。これではユーザーガイドの説明が少し複雑になるため、log_filenameを固定値に設定します。

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** log_filenameを設定する

```ini
log_filename = 'postgresql.log'
```

### クラスターのstanzaの設定 {#configure-cluster-stanza}

stanzaは、PostgreSQLデータベースクラスターの場所、バックアップ方法、アーカイブオプションなどを定義する設定です。ほとんどのデータベースサーバーにはPostgreSQLデータベースクラスターが1つしかないためstanzaも1つですが、バックアップサーバーにはバックアップ対象のデータベースクラスターごとにstanzaがあります。

stanzaにプライマリークラスターの名前を付けたくなるかもしれませんが、クラスターに含まれるデータベースを表す名前のほうが適切です。stanza名はプライマリーとすべてのレプリカで使うため、mainやprodのようなローカルクラスター名ではなく、appやdwのようにクラスターの実際の用途を表す名前を選ぶのが適切です。

「demo」はこのクラスターの目的を正確に表しているため、stanza名にも適しています。

pgBackRestは、PostgreSQLクラスターの基本データディレクトリの場所を知る必要があります。このパスはPostgreSQLに直接問い合わせることもできますが、リカバリー時にはPostgreSQLプロセスを利用できません。バックアップ時には、pgBackRestに指定された値をPostgreSQLが稼働しているパスと比較し、一致しなければエラーになります。`pg-path`がPostgreSQLの報告するdata_directoryと完全に一致していることを確認してください。

RHELではデフォルトでクラスターを`/var/lib/pgsql/[version]/data`に保存するため、正しいデータディレクトリのパスを容易に判断できます。

`/etc/pgbackrest/pgbackrest.conf`ファイルを作成する際は、データベース所有者（通常は`postgres`）に読み取り権限を付与する必要があります。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** PostgreSQLクラスターのデータディレクトリを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data
```

pgBackRestの設定ファイルはWindowsのINIファイルに似た形式を使用します。セクションは角括弧で囲んだテキストで表し、各セクションにキーと値のペアを記述します。`#`で始まる行は無視されるためコメントに使用できますが、値と同じ行の末尾にコメントを付けることはできません。引用符による囲みはサポートされず、キーと値の前後の空白は除去されます。同じセクションが複数回現れた場合は統合されます。

pgBackRestの設定ファイルは、次のいずれかの方法で読み込めます。

- `config`と`config-include-path`がデフォルトの場合：デフォルトの設定ファイルが存在すれば読み込み、デフォルトの設定インクルードパスに`*.conf`ファイルが存在すれば追加します。
- `config`オプションが指定されている場合：指定された設定ファイルだけを読み込みます。このファイルは存在する必要があります。
- `config-include-path`が指定されている場合：設定インクルードパスの`*.conf`ファイルを読み込みます。このパスは存在する必要があります。デフォルトの設定ファイルも、存在すれば読み込みます。指定した設定インクルードパスのファイルだけを読み込むには、`--no-config`オプションも指定します。
- `config`と`config-include-path`が指定されている場合：ユーザー指定の値を使って設定ファイルを読み込み、設定インクルードパスの`*.conf`ファイルを追加します。これらのファイルは存在する必要があります。
- `config-path`が指定されている場合：この設定は、設定ファイルのデフォルト配置先のベースパスと、デフォルトのconfig-include-path設定のベースパスの一方または両方を上書きします。ただし、configまたはconfig-include-pathオプションを明示的に設定した場合は、その設定が優先されます。

ファイルは1つの大きなファイルとして連結されますが、各ファイルは単独でも有効でなければなりません。つまり、キーと値を格納するセクションは、必要となる各ファイルで指定する必要があります。順序は関係ありませんが、セクションによる優先順位があります。優先順位は高い順に次のとおりです。

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

注：

`--config`、`--config-include-path`、`--config-path`はコマンドライン専用のオプションです。

pgBackRestは環境変数でも設定できます（下の例を参照）。これらの変数は[backup](/ja/docs/pgbackrest/command/backup/)、[restore](/ja/docs/pgbackrest/command/restore/)、[archive-push](/ja/docs/pgbackrest/command/archive-push/)などのコマンドに適用されます。

pg-primary **⇒** 環境変数で`log-path`を設定する

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.59.3 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### リポジトリの作成 {#create-the-repository}

リポジトリは、pgBackRestがバックアップを保存し、WALセグメントをアーカイブする場所です。

必要な容量を事前に見積もるのは難しい場合があります。まず何度かバックアップを取り、各種類（full/incr/diff）のバックアップサイズを記録するとともに、1日あたりのWAL生成量を測定するのが最善です。これで必要容量のおおよその見当が付きますが、もちろんデータベースの変化に伴って必要容量も変わる可能性があります。

このデモでは、PostgreSQLサーバーと同じホストにリポジトリを保存します。これは最も単純な構成で、従来のバックアップソフトウェアでデータベースホストをバックアップする場合に有用です。

pg-primary **⇒** pgBackRestのリポジトリを作成する

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

pgBackRestがリポジトリを見つけられるよう、リポジトリのパスを設定する必要があります。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** pgBackRestのリポジトリパスを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest
```

複数のリポジトリも設定できます。詳細は[複数のリポジトリ](#multiple-repositories)を参照してください。

### アーカイブの設定 {#configure-archiving}

稼働中のPostgreSQLクラスターをバックアップするには、WALアーカイブを有効にする必要があります。`%p`は、PostgreSQLがアーカイブ対象のWALセグメントの場所を指定する方法です。クラスターに明示的な書き込みがなくても、バックアップ中には*少なくとも*1つのWALセグメントが作成されます。

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** アーカイブを設定する

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

これらの変更後、バックアップを実行する前にPostgreSQLクラスターを再起動する必要があります。

pg-primary **⇒** デモクラスターを再起動する

```bash
sudo systemctl restart postgresql-14.service
```

`hot_standby`はデフォルトで有効になっており、すべてのクラスターで有効のままにしておくことをお勧めします。フェイルオーバー後にプライマリーをスタンバイとして再構築する場合など、どのクラスターも後でスタンバイとしてリストアされる可能性があり、この設定がないとスタンバイは読み取り専用接続を受け付けません。

WALセグメントをpgBackRestリポジトリにアーカイブするのに60秒（デフォルト）を超える時間がかかると予想される場合は、pgBackRestの`archive-timeout`オプションを増やすことをお勧めします。このオプションは、WALセグメントの切り替えを強制するPostgreSQLのarchive_timeoutオプションとは異なります。後者は、長時間操作がないデータベースに有用です。PostgreSQLのarchive_timeoutオプションの詳細は、PostgreSQLの[先行書き込みログ](https://www.postgresql.org/docs/current/static/runtime-config-wal.html)を参照してください。

`archive-push`コマンドには固有のオプションを設定できます。たとえば、バックアップの圧縮には影響を与えずに、圧縮レベルを下げてアーカイブを高速化できます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `archive-push`の圧縮レベルを低く設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

この設定方法はどのコマンドにも使用でき、`demo:archive-push`のように特定のstanzaだけを対象にすることもできます。

### 保持の設定 {#configure-retention}

pgBackRestは保持オプションに基づいてバックアップを期限切れにします。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** フルバックアップを2つ保持するよう設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

保持の詳細は[保持](#retention)を参照してください。

### リポジトリの暗号化の設定 {#configure-repository-encryption}

暗号化の例として、リポジトリに暗号方式とキーを設定します。リポジトリの種類（S3などのオブジェクトストア）が暗号化に対応している場合でも、暗号化は常にクライアント側で行います。

暗号キーには、長くランダムなパスフレーズを使用することが重要です。生成するには`openssl rand -base64 48`を実行する方法が適しています。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** pgBackRestリポジトリの暗号化を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

注：

上の例では、`info`コマンドがすべてのstanzaを読み込めるよう、暗号化設定を`[global]`セクションに記述しています。`stanza`オプションを指定しない場合、`info`コマンドは`[global]`セクションからのみ暗号化設定を読み込みます。stanzaごとに暗号化を設定した場合は、暗号化されたstanzaを読み込むために`stanza`オプションが必要です。

リポジトリを設定し、stanzaを作成して確認した後は、リポジトリの暗号化設定を変更できません。

### stanzaの作成 {#create-the-stanza}

stanzaを初期化するには、`stanza-create`コマンドを実行する必要があります。アーカイブとバックアップが正しく設定されていることを確認するため、`stanza-create`の後に`check`コマンドを実行することをお勧めします。

pg-primary **⇒** stanzaを作成して設定を確認する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1200-90682d35 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### 設定の確認 {#check-the-configuration}

`check`コマンドは、指定されたstanzaのアーカイブとバックアップについて、pgBackRestとarchive_commandが正しく設定されていることを検証します。コマンドを実行するホストに設定された、すべてのリポジトリとデータベースの確認を試みます。特にアーカイブの設定ミスにより、必要なWALセグメントがアーカイブに届かずバックアップが不完全になる問題を検出します。このコマンドはPostgreSQLホストまたはリポジトリホストで実行できます。スタンバイホストでも実行できますが、スタンバイでは`pg_switch_xlog()`/`pg_switch_wal()`を実行できないため、リポジトリの設定だけを検証します。

PostgreSQLにWALセグメントを強制的にアーカイブさせるため、`pg_create_restore_point('pgBackRest Archive Check')`と`pg_switch_xlog()`/`pg_switch_wal()`が呼び出されます。

pg-primary **⇒** 設定を確認する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1233-340209f5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000100000000/000000010000000000000001-dac4045f133f7305d6342d81e428e60050928bc4.gz' on repo1
P00   INFO: check command end: completed successfully
```

### パフォーマンスの調整 {#performance-tuning}

pgBackRestには、リポジトリの後方互換性を維持するため、デフォルトでは無効になっている性能関連のオプションがあります。ただし、新しいリポジトリを作成する場合は、次のオプションをお勧めします。既存のリポジトリにも使用できますが、古いバージョンのpgBackRestではそのリポジトリを読み込めなくなる点に注意してください。どのバージョンと互換性がなくなるかは、以下に示す各機能の導入時期によって異なります。

- `compress-type` - `backup`と`archive-push`コマンドで使用する圧縮アルゴリズムを決めます。デフォルトは`gz`（Gzip）ですが、はるかに高速で`gz`と同程度の圧縮率が得られる`zst`（Zstandard）をお勧めします。`compress-type`オプションは[v2.27](/ja/docs/pgbackrest/release/#v227-release-notes)から`zst`に対応しています。詳細は[圧縮形式](/ja/docs/pgbackrest/configuration/#compress-type-option---compress-type)を参照してください。
- `repo-bundle` - バックアップ時に小さなファイルをまとめ、容量を節約し、`backup`と`restore`の両コマンドを高速化します。特にS3などのオブジェクトストアで効果があります。`repo-bundle`オプションは[v2.39](/ja/docs/pgbackrest/release/#v239-release-notes)で導入されました。詳細は[ファイルのバンドル化](#file-bundling)を参照してください。
- `repo-block` - `diff`/`incr`の`backup`で、ファイル全体ではなく変更された部分だけを保存します。これにより容量を節約し、`backup`を高速化できます。`repo-block`オプションは[v2.46](/ja/docs/pgbackrest/release/#v246-release-notes)で導入されましたが、少なくとも[v2.52.1](/ja/docs/pgbackrest/release/#v2521-release-notes)をお勧めします。詳細は[ブロック単位の増分バックアップ](#block-incremental)を参照してください。

このほかにも、追加設定が必要なため、またはデフォルトが安全な値（ただし最適ではない値）であるため、デフォルトでは有効になっていない性能関連のオプションがあります。これらはpgBackRestのすべてのv2バージョンで利用できます。

- `process-max` - コマンドに使用するプロセス数を決めます。デフォルトは1ですが、この値が適切なことはほとんどありません。`process-max`の使い方はコマンドごとに異なるため、使用方法の詳細は各コマンドのドキュメントを参照してください。
- `archive-async` - WALファイルをまとめてリポジトリにアーカイブし、アーカイブを大幅に高速化します。スプールパスを作成する必要があるため、デフォルトでは無効です。詳細は[非同期アーカイブ](#asynchronous-archiving)を参照してください。
- `backup-standby` - プライマリーの負荷を減らすため、プライマリーではなくスタンバイでバックアップを実行します。追加設定と1つ以上のスタンバイホストが必要なため、デフォルトでは無効です。詳細は[スタンバイからのバックアップ](#backup-from-a-standby)を参照してください。

### バックアップの実行 {#perform-a-backup}

pgBackRestはデフォルトで、次の定期チェックポイントを待ってからバックアップを開始します。PostgreSQLのcheckpoint_timeoutとcheckpoint_segmentsの設定によっては、チェックポイントが完了してバックアップを開始できるまでにかなり時間がかかる場合があります。通常は、すぐにバックアップが始まるよう`start-fast=y`を設定することをお勧めします。これによりチェックポイントが強制されますが、バックアップは通常1日1回実行するため、追加のチェックポイントが性能に目立った影響を与えることはないはずです。ただし、非常に負荷の高いクラスターでは、必要に応じてコマンドラインで`--start-fast`を指定するほうがよい場合があります。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** バックアップの即時開始を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

PostgreSQLクラスターのバックアップを行うには、pgBackRestの`backup`コマンドを実行します。

pg-primary **⇒** デモクラスターをバックアップする

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-185647F
P00   INFO: full backup size = 25.2MB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

pgBackRestはデフォルトで増分バックアップの実行を試みます。ただし、増分バックアップには基となるフルバックアップが必要です。この例ではフルバックアップが存在しなかったため、pgBackRestは代わりにフルバックアップを実行しました。

`type`オプションでフルバックアップまたは差分バックアップを指定できます。

pg-primary **⇒** デモクラスターの差分バックアップを取る

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-185647F_20261002-185651D
P00   INFO: diff backup size = 9.2KB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1398-36e29fed --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

今回はフルバックアップがすでに存在していたため、警告はありませんでした。増分バックアップはフルバックアップ*または*差分バックアップを基にできますが、差分バックアップはフルバックアップを基にする必要があります。フルバックアップを実行するには、`backup`コマンドに`--type=full`を指定します。

オンラインバックアップ中、pgBackRestはバックアップの整合性に必要なWALセグメントがアーカイブされるのを待ちます。この待機時間は、デフォルトで60秒のpgBackRestの`archive-timeout`オプションで制御します。個々のセグメントのアーカイブにこの時間を超えることが分かっている場合は、この値を増やすことをお勧めします。

### バックアップのスケジュール {#schedule-a-backup}

cronなどのユーティリティで、バックアップをスケジュールできます。

次の例では2つのcronジョブを設定します。毎週日曜日の午前6:30にフルバックアップを実行し、月曜日から土曜日の午前6:30に差分バックアップを実行します。このcrontabを週の途中で初めて設定した場合、pgBackRestは差分バックアップのジョブが最初に実行されるときにフルバックアップを行い、翌日から差分バックアップを行います。

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

バックアップをスケジュールしたら、定期的に期限切れになるよう保持設定を行うことが重要です。[保持](#retention)を参照してください。

### バックアップ情報 {#backup-information}

バックアップの情報を取得するには、`info`コマンドを使用します。

pg-primary **⇒** デモクラスターの情報を取得する

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-185647F
            timestamp start/stop: 2026-10-02 18:56:47+00 / 2026-10-02 18:56:50+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup set size: 3.2MB, backup size: 3.2MB

        diff backup: 20261002-185647F_20261002-185651D
            timestamp start/stop: 2026-10-02 18:56:51+00 / 2026-10-02 18:56:52+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 25.2MB, database backup size: 9.2KB
            repo1: backup set size: 3.2MB, backup size: 864B
            backup reference total: 1 full
```

`info`コマンドは、単一のstanzaまたはすべてのstanzaを対象に動作します。デフォルトのテキスト出力では、指定したstanzaのバックアップ概要を人が読みやすい形式で表示します。この形式は、どのリリースでも変更される可能性があります。

機械処理用の出力には`--output=json`を使用します。JSON出力にはテキスト出力よりはるかに多くの情報が含まれ、バグが見つからない限り安定した形式を維持します。

実行を高速化するには、`--detail-level=progress`を指定して、進捗情報だけに出力を限定します。この場合、stanzaの可用性以外のすべての確認が省略される点に注意してください。

stanzaごとに個別のセクションがあり、`--stanza`オプションで単一のstanzaに出力を限定できます。stanzaの「`status`」は、そのstanzaの健全性を簡潔に示します。「`ok`」ならpgBackRestは正常に動作しています。複数のリポジトリがある場合、「`mixed`」は1つ以上のリポジトリでstanzaが正常でないことを示し、リポジトリごとに状態の詳細が表示されます。リポジトリで既知のエラーコードに該当しないエラーが発生した場合は、エラーコード「`other`」を使用し、完全なエラー詳細を表示します。「`wal archive min/max`」は、現在アーカイブに保存されているWALの最小値と最大値です。複数のリポジトリがある場合、`--repo`オプションを指定しない限り、全リポジトリを通して報告されます。アーカイブ保持ポリシーなどの理由で、途中に欠落がある場合もあります。

ホスト上で該当コマンドが実行中の場合は、「`status`」情報の横に「`backup/expire running`」や「`restore running`」が表示されます。テキスト出力にはリポジトリごとの進捗も表示され、JSON出力には「`repo`」配列が含まれます。

バックアップは古い順に表示されます。最も古いバックアップは*必ず*フルバックアップ（ラベル末尾の`F`で識別）ですが、最新のバックアップはフル、差分（末尾が`D`）、増分（末尾が`I`）のいずれかです。

「`timestamp start/stop`」は、バックアップが実行された期間を示します。「`timestamp stop`」は、ポイントインタイムリカバリーで使用するバックアップの選択に利用できます。ポイントインタイムリカバリーの詳細は、[ポイントインタイムリカバリー](#point-in-time-recovery)を参照してください。

「`wal start/stop`」は、リストア時にデータベースの整合性を回復するために必要なWALの範囲を示します。`backup`コマンドは、完了前にこの範囲のWALがアーカイブに存在することを確認します。

「`database size`」はデータベース全体の非圧縮サイズで、「`database backup size`」は実際にバックアップするデータベース内のデータ量です（フルバックアップでは両者は同じです）。

「`repo`」は、このバックアップを保存しているリポジトリを示します。「`backup set size`」には、このバックアップからデータベースをリストアするために必要な、このバックアップ自身と参照先バックアップのリポジトリ内の全ファイルが含まれます。一方、「`backup size`」には、このバックアップのファイルだけが含まれます（フルバックアップではこれらも同じです）。pgBackRestで圧縮を有効にしている場合、リポジトリのサイズは圧縮後のファイルサイズを表します。

「`backup reference total`」は、このバックアップのリストアに必要な追加バックアップの一覧の概要です。完全な参照一覧を表示するには、`--set`オプションを使用します。

### バックアップのリストア {#restore-a-backup}

バックアップはさまざまな障害に備えるためのもので、特に一般的なのはハードウェア障害とデータ破損です。データ破損を最も簡単に再現する方法は、PostgreSQLクラスターの重要なファイルを削除することです。

pg-primary **⇒** デモクラスターを停止し、`pg_control`ファイルを削除する

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres rm /var/lib/pgsql/14/data/global/pg_control
```

この重要なファイルがない状態でクラスターを起動すると、エラーになります。

pg-primary **⇒** 破損したデモクラスターの起動を試みる

```bash
sudo systemctl start postgresql-14.service
sudo systemctl status postgresql-14.service
```

```text
postgresql-14.service - PostgreSQL 14 database server
    Loaded: loaded (/usr/lib/systemd/system/postgresql-14.service, disabled)
    Active: failed (failed)
```

PostgreSQLクラスターのバックアップをリストアするには、pgBackRestの`restore`コマンドを実行します。クラスターを停止し（この例ではすでに停止しています）、PostgreSQLのデータディレクトリからすべてのファイルを削除する必要があります。

pg-primary **⇒** デモクラスターから古いファイルを削除する

```bash
sudo -u postgres find /var/lib/pgsql/14/data -mindepth 1 -delete
```

pg-primary **⇒** デモクラスターをリストアしてPostgreSQLを起動する

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo systemctl start postgresql-14.service
```

リストアにより欠落していた`pg_control`ファイルが復元されたため、今回はクラスターが正常に起動しました。

`restore`コマンドの詳細は[リストア](#restore-1)を参照してください。

--------

## 監視 {#monitoring}

監視は、どの本番システムでも重要です。多くのツールがあり、少し手を加えれば、そのいずれでもpgBackRestを監視できます。

pgBackRestはリポジトリの情報をJSON形式で出力できます。この情報には、各stanzaのすべてのバックアップの一覧とWALアーカイブ情報が含まれます。

### PostgreSQLでの監視 {#in-postgresql}

PostgreSQLの`COPY`コマンドを使うと、pgBackRestの情報をテーブルに読み込めます。次の例では、この処理をリアルタイムのクエリーに使える関数にまとめています。

pg-primary **⇒** PostgreSQL用のpgBackRest情報関数を読み込む

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

これで`monitor.pgbackrest_info()`関数を使って、stanzaの最後に成功したバックアップの時刻と、アーカイブされたWALを確認できます。

pg-primary **⇒** 最後に成功したバックアップの時刻とアーカイブされたWALを取得する

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 18:56:52+00 | 000000010000000000000005
(1 row)
```

--------

## バックアップ {#backup-1}

複数のリポジトリが設定されている場合、pgBackRestは`--repo`オプションを指定しない限り、最も優先順位の高いリポジトリ（例：`repo1`）にバックアップします。

pgBackRestにはスケジューラーが組み込まれていないため、cronなどのスケジュール機構から実行することをお勧めします。

詳細と例は[バックアップの実行](#perform-a-backup)を参照してください。

### ファイルのバンドル化 {#file-bundling}

リポジトリ内でファイルをまとめると、バックアップの時間を短縮し、リポジトリの容量もある程度節約できます。特に、S3などのオブジェクトストアやブロックサイズの大きなファイルシステムにリポジトリを保存する場合に効果があります。オブジェクトストアではファイルごとの作成時間が長く、非常に小さなファイルでも大きなファイルと同程度の保存コストがかかる場合があります。

ファイルのバンドル化は、`repo-bundle`オプションで有効にします。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-bundle`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

ファイルをバンドル化しないフルバックアップでは、バックアップパスに1000以上のファイルがありますが、バンドル化するとファイル総数は大幅に減ります。さらに、通常のバックアップでは長さゼロのファイルも個別に保存するのに対し、バンドル化ではマニフェストへの記録を除いて保存しないという利点もあります。

pg-primary **⇒** フルバックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** ファイル総数を確認する

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

`repo-bundle-size`と`repo-bundle-limit`オプションで調整できますが、ほとんどの場合はデフォルト値が最適なはずです。

ファイルのバンドル化は一般に効率的ですが、リポジトリからファイルを手動で取り出しにくくなるという欠点があります。フルバックアップのたびにバンドル内のファイル配置が変わるため、重複排除ストレージには適さない場合があります。また、ファイルバンドルの処理は中断位置から再開できないため、`repo-bundle-limit`を大きくしすぎないよう注意してください。

### ブロック単位の増分バックアップ {#block-incremental}

ブロック単位の増分バックアップでは、ファイル全体ではなく、前のバックアップ以降に変更された部分だけを保存して容量を節約します。

ブロック単位の増分バックアップは`repo-block`オプションで有効にし、すべてのバックアップ種類で有効にすると最も効果的です。ファイルのバンドル化も有効にする必要があります。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-block`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

### バックアップの注釈 {#backup-annotations}

バックアップに情報を記したキーと値のペアを付けられます。このオプションは複数回指定でき、複数の注釈を付けられます。

pg-primary **⇒** 注釈付きのフルバックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

注釈は、`info`コマンドで`--set`によりバックアップを指定した場合にテキスト出力に表示され、JSON出力には常に表示されます。

pg-primary **⇒** デモクラスターの情報を取得する

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                key: value
                source: demo backup
```

`backup`コマンドで付けた注釈は、後で`annotate`コマンドを使って追加、変更、削除できます。

pg-primary **⇒** バックアップの注釈を変更する

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## 保持 {#retention}

通常、[ポイントインタイムリカバリー](#point-in-time-recovery)の可能な期間を広げるには、できるだけ多くのバックアップを保持することが望ましいですが、ディスク容量などの実際の制約も考慮する必要があります。保持オプションは、不要になった古いバックアップを削除します。

pgBackRestは、保持方式に応じてフルバックアップをローテーションします。方式には個数または期間を指定できます。個数を指定した場合、期限切れの判定はバックアップの作成日時ではなく、保持すべき個数に基づきます。差分バックアップは個数に基づきますが、依存するフルバックアップが期限切れになると必ず一緒に期限切れになります。増分バックアップが保持設定により単独で期限切れになることはなく、関連するフルバックアップまたは差分バックアップとともに期限切れになります。詳細と例は[フルバックアップの保持](#full-backup-retention)と[差分バックアップの保持](#differential-backup-retention)を参照してください。

アーカイブされたWALは、デフォルトでは期限切れになっていないバックアップのために保持されます。推奨はしませんが、retention-archiveオプションでリポジトリごとにこの保持方針を変更できます。詳細と例は[アーカイブの保持](#archive-retention)を参照してください。

`expire`コマンドは、バックアップが成功するたびに自動実行され、ユーザーが実行することもできます。ユーザーが実行した場合、設定された各リポジトリの保持設定に従って期限切れ処理が行われます。`--repo`オプションを指定した場合、指定したリポジトリだけで期限切れ処理を行います。`--set`オプションで特定のバックアップセットに期限切れ処理を限定することもできます。この場合、`--repo`オプションを指定しない限り、すべてのリポジトリを検索してセットの条件に一致するものを期限切れにします。`expire`コマンドを実行すると、アーカイブの保持方針の確認とそれに基づく処理も毎回行われる点に注意してください。

### フルバックアップの保持 {#full-backup-retention}

`repo1-retention-full-type`は、`repo1-retention-full`オプションを、保持するフルバックアップの個数として解釈するか、保持日数として解釈するかを決めます。期限切れ処理には、新しいバックアップが完了している必要があります。つまり、`repo1-retention-full-type=count`かつ`repo1-retention-full=2`の場合は、3つのフルバックアップが保存された後に最も古いものが期限切れになります。`repo1-retention-full-type=time`かつ`repo1-retention-full=20`の場合は、少なくとも20日前のフルバックアップが1つ存在しなければ期限切れ処理は行われません。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-full`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

バックアップの設定は`repo1-retention-full=2`ですが、現在フルバックアップは1つしかないため、次のフルバックアップを実行しても、どのフルバックアップも期限切れになりません。

pg-primary **⇒** フルバックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 963 lines of output]
P00   INFO: repo1: remove expired backup 20261002-185706F
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185708F, start = 000000020000000000000008
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

一方、最も古いバックアップより前に生成されたWALセグメントがあるため、アーカイブは*期限切れになります*。これらはリカバリーには使えません。バックアップのリカバリーに利用できるのは、そのバックアップ以降に生成されたWALセグメントだけです。

pg-primary **⇒** フルバックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-185708F
P00   INFO: repo1: remove expired backup 20261002-185708F
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000008, stop = 000000020000000000000009
P00   INFO: expire command end: completed successfully
```

フルバックアップ`20261002-185647F`が期限切れになり、アーカイブの保持は、最も古いフルバックアップとなった`20261002-185711F`を基準に行われます。

### 差分バックアップの保持 {#differential-backup-retention}

`repo1-retention-diff`に、必要な差分バックアップの個数を設定します。差分バックアップは前のフルバックアップだけに依存するため、直近1日以上の差分バックアップを順次入れ替えながら保持できます。これにより、全体の容量を抑えながら、最近の時点へすばやくリストアできます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-diff`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=1

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

バックアップの設定は`repo1-retention-diff=1`のため、1つを期限切れにするには2つの差分バックアップを実行する必要があります。増分バックアップの期限切れ処理も示すため、増分バックアップを追加します。この例では、差分バックアップの期限切れに連動します。

pg-primary **⇒** 差分バックアップと増分バックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

ここで差分バックアップを実行すると、前の差分バックアップと増分バックアップが期限切れになり、差分バックアップが1つだけ残ります。

pg-primary **⇒** 差分バックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=2641-6abf9293 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-185713F_20261002-185715D, 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185715D
P00   INFO: expire command end: completed successfully
```

### アーカイブの保持 {#archive-retention}

pgBackRestはバックアップの期限切れ処理時にアーカイブ済みWALセグメントを自動削除します（デフォルトでは`repo1-retention-full`オプションに基づいてフルバックアップのWALを期限切れにします）。ただし、ディスク容量の節約のために、アーカイブをより積極的に期限切れにすることが有用な場合もあります。差分アーカイブの保持では、フルバックアップも差分バックアップとして扱われます。

アーカイブの期限切れ処理で、バックアップの整合性に必要なWALセグメントが削除されることはありません。ただし、ポイントインタイムリカバリー（PITR）は連続したWALストリームでしか機能しないため、通常のバックアップ期限切れ処理とは別にアーカイブを積極的に期限切れにする際は注意してください。実際には何も期限切れにせず、対象だけを確認するには、コマンドラインで`expire`コマンドに`dry-run`オプションを指定できます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-diff`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

pg-primary **⇒** 差分バックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261002-185713F_20261002-185719D
P00   INFO: diff backup size = 11.5KB, file total = 951
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** アーカイブを期限切れにする

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=2877-3548ad61 --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185711F, start = 00000002000000000000000A, stop = 00000002000000000000000B
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185717D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185719D, start = 000000020000000000000016
P00   INFO: repo1: 14-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

差分バックアップ`20261002-185713F_20261002-185717D`には、古いバックアップの整合性を回復するために保持しなければならないアーカイブ済みWALセグメントがあります。これらを使ってPITRでさらに先へ再生することはできません。`20261002-185713F_20261002-185717D`より後、`20261002-185713F_20261002-185719D`より前に生成されたWALセグメントは削除されます。新しいバックアップ`20261002-185713F_20261002-185719D`より後に生成されたWALセグメントは残り、PITRに利用できます。

差分アーカイブの保持ではフルバックアップも差分バックアップとして扱われるため、同じ設定でここからフルバックアップを実行すると、そのフルバックアップのアーカイブだけがPITR用に保持されます。

--------

## リストア {#restore-1}

restoreコマンドはデフォルトで、バックアップが存在する最初のリポジトリから最新のバックアップを自動選択します（[クイックスタート - バックアップのリストア](#restore-a-backup)を参照）。リポジトリの確認順序は`pgbackrest.conf`で決まります（たとえばrepo1をrepo2より先に確認します）。特定のリポジトリから選択するには、`--repo`オプション（例：`--repo=1`）を指定できます。最新以外のバックアップを使用するには、`--set`オプションを指定します。

PITR に `--type=time` または `--type=lsn` を指定する場合は、`--target` オプションで対象の時刻または LSN を指定する必要があります。`--set` を指定しない場合、設定済みのリポジトリを順に調べ、終了時刻が対象時刻より前のバックアップ、または終了 LSN が対象 LSN 以下のバックアップを選択します。一致するバックアップが見つからない場合、`--type=time` と `--type=lsn` のどちらでも pgBackRest はエラーを返し、最新のバックアップにフォールバックしません。`xid` など、その他の PITR の種類では、対象が最新のバックアップより前であれば `--set` オプションを指定する必要があります。詳細と例については、[ポイントインタイムリカバリ](#point-in-time-recovery)を参照してください。

PostgreSQLの推奨に従い、レプリケーションスロットは含めません。詳細はPostgreSQLドキュメントの[データディレクトリのバックアップ](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA)を参照してください。

以降のセクションでは、`restore`コマンドの追加機能を紹介します。

### ファイルの所有権 {#file-ownership}

通常のようにroot以外のユーザーで`restore`を実行した場合、リストアしたすべてのファイルはpgBackRestを実行するユーザーとグループに属します。既存ファイルの所有者が実行ユーザーやグループと異なり、所有権を変更できない場合はエラーになります。この場合、権限を持つユーザーがファイルの所有権を更新してから、リストアを再試行する必要があります。

`root`ユーザーで`restore`を実行した場合、pgBackRestはバックアップ時にマニフェストに記録した所有権の再現を試みます。マニフェストに保存されるのはユーザーとグループの**名前**だけなので、リストア先ホストに同じ名前が存在する必要があります。ローカルでユーザー名やグループ名が見つからない場合は、PostgreSQLのデータディレクトリのユーザーとグループを使用します。それらにも対応する名前がない場合は、最後に`root`を使用します。

### deltaオプション {#delta-option}

[クイックスタート](#quick-start)の[バックアップのリストア](#restore-a-backup)では、`restore`を実行する前にデータベースクラスターのディレクトリを空にする必要がありました。`delta`オプションを使うと、pgBackRestはデータベースクラスターのディレクトリ内でそのまま残せるファイルと、バックアップからリストアすべきファイルを自動で判別できます。また、バックアップのマニフェストにないファイルも*削除*するため、バックアップと異なる変更を取り除きます。この判別には、データベースクラスターのディレクトリ内の各ファイルについて計算した[SHA-1](https://en.wikipedia.org/wiki/SHA-1)暗号学的ハッシュを使用します。`SHA-1`ハッシュがバックアップに保存されたハッシュと一致しない場合、そのファイルをリストアします。`process-max`オプションと組み合わせると、非常に効率的に処理できます。リストア中はPostgreSQLサーバーが停止しているため、サーバーが稼働するバックアップ時より多くのプロセスを使用できます。

pg-primary **⇒** デモクラスターを停止し、deltaリストアを実行する

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/pgsql/14/data' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/base/13755/pg_internal.init'
       [filtered 996 lines of output]
```

pg-primary **⇒** PostgreSQLを再起動する

```bash
sudo systemctl start postgresql-14.service
```

### 選択したデータベースのリストア {#restore-selected-databases}

クラスターのバックアップから、特定のデータベースだけを選んでリストアしたい場合があります。性能上の理由や、クラスター全体のバックアップをリストアする容量がないマシンに、選択したデータベースを移動する場合などです。

この機能を示すため、test1とtest2の2つのデータベースを作成します。

pg-primary **⇒** テスト用データベースを2つ作成する

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

選択的なリストアでもリカバリーが機能することを示すため、各テスト用データベースにテーブルとデータを用意します。

pg-primary **⇒** 各データベースにテスト用テーブルを作成する

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

pgBackRestが新しいデータベースを認識できるよう、新しくバックアップを取ります。

pg-primary **⇒** バックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

選択的リストアを使う主な理由の1つは容量の節約です。リストア後のディスク使用量と比較できるよう、ここでtest1データベースのサイズを表示します。

pg-primary **⇒** test1データベースの使用容量を表示する

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.4M	/var/lib/pgsql/14/data/base/32768
```

リストアするデータベースが分からない場合は、`info`コマンドの`set`オプションを使って、バックアップセットに含まれるデータベースを調べます。

pg-primary **⇒** バックアップのデータベース一覧を表示する

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-185713F_20261002-185728I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 2.1MB
            backup reference list: 20261002-185713F, 20261002-185713F_20261002-185719D
            database list: postgres (13755), test1 (32768), test2 (32769)
```

クラスターを停止し、test2データベースだけをリストアします。組み込みデータベース（`template0`、`template1`、`postgres`）は常にリストアされます。

警告：

`--type=immediate`を指定しないと、リカバリーでエラーが発生する場合があります。整合性が確立された後は、PostgreSQLがフルページ書き込みの場合でもゼロ埋めページをエラーとして扱うためです。PostgreSQL ≥ 13では、ignore_invalid_pages設定で無効なページを無視できます。その場合は、リカバリー後にログを確認し、選択したデータベースで無効なページが報告されていないことを確かめることが重要です。

pg-primary **⇒** 最後のバックアップからtest2データベースだけを含めてリストアする

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo systemctl start postgresql-14.service
```

リカバリーが完了すると、test2データベースには以前に作成したすべてのテーブルとデータが含まれます。

pg-primary **⇒** test2データベースがリカバリーされたことを確認する

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

test1データベースは、リカバリー自体は成功していてもアクセスできません。データベース全体をゼロ埋めのスパースファイルとしてリストアしたためです。PostgreSQLはゼロ埋めファイルにWALを正常に適用できますが、重要なファイルにデータがないため、データベース全体としては無効です。これは意図した動作で、WALの再生中に適用された一部のデータだけを含む可能性があるデータベースを、誤って使用することを防ぎます。

pg-primary **⇒** test1データベースへの接続を試みるとエラーになる

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

test1データベースはゼロ埋めのスパースファイルとしてリストアされるため、必要な容量はリカバリー中に書き込まれるWALの量だけです。バックアップ中に生成され、リカバリー中に適用されるWALの量は大きくなることもありますが、通常はデータベース全体のサイズのごく一部です。この機能が特に役立つ大規模なデータベースでは、なおさらです。

選択的リストアでtest1データベースが使用するディスク容量は、データベース全体をリストアした場合より大幅に少ないことが分かります。

pg-primary **⇒** リカバリー後のtest1データベースの使用容量を表示する

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.0K	/var/lib/pgsql/14/data/base/32768
```

この時点で無効なtest1データベースに行える操作は、`drop database`だけです。リカバリーが完了してクラスターにアクセスできるようになるまでデータベースを削除できないため、pgBackRestは自動削除を行いません。

pg-primary **⇒** test1データベースを削除する

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

無効なtest1データベースを削除したので、test2と組み込みデータベースだけが残ります。

pg-primary **⇒** 残っているデータベースを一覧表示する

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
 13754 | template0
 13755 | postgres
 32769 | test2
(4 rows)
```

--------

## ポイントインタイムリカバリー {#point-in-time-recovery}

[クイックスタート](#quick-start)の[バックアップのリストア](#restore-a-backup)では、WALストリームの末尾まで再生するデフォルトのリカバリーを行いました。ハードウェア障害の場合は通常これが最適ですが、機械または人の操作に起因するデータ破損の場合は、ポイントインタイムリカバリー（PITR）のほうが適していることがよくあります。

ポイントインタイムリカバリー（PITR）では、バックアップから、指定したlsn、時刻、トランザクションID、またはリカバリーポイントまでWALを再生できます。一般的なリカバリーでは、時刻に基づく方式が最も有用でしょう。典型的な例は、誤って削除したテーブルやデータを復元する場合です。ここでは効果が分かりやすいテーブルの復元を例にしますが、削除されたデータもまったく同じ方法で復元できます。

pg-primary **⇒** 非常に重要なデータを持つテーブルを作成する

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

時刻はPostgreSQLが認識する値で表し、タイムゾーンのオフセットを含めることが重要です。これにより、意図しないタイムゾーン変換や、予想外のリカバリー結果の可能性を減らせます。

pg-primary **⇒** PostgreSQLから時刻を取得する

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 18:57:39.575732+00
```

時刻を記録したので、テーブルを削除します。実際には、テーブルが削除された正確な時刻を見つけるのは、この例よりはるかに困難です。正確な時刻が分からないこともありますが、履歴などを調べれば近い時刻を特定できるはずです。

pg-primary **⇒** 重要なテーブルを削除する

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

リストアするバックアップを誤って選ぶと、必要な目標時刻へのリカバリーは失敗します。これを示すために、`important_table`が存在しない状態で新しい増分バックアップを実行します。

pg-primary **⇒** 増分バックアップを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-185713F_20261002-185741I
            timestamp start/stop: 2026-10-02 18:57:41+00 / 2026-10-02 18:57:42+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

PostgreSQLは前方への再生しかできず、後方には戻れないため、このバックアップから失われたテーブルを復元することはできません。

pg-primary **⇒** 誤ったバックアップからのリカバリーを試みる

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-185713F_20261002-185741I --target-timeline=current \
       --type=time "--target=2026-10-02 18:57:39.575732+00" --target-action=promote restore
sudo systemctl start postgresql-14.service
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 11 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000100 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.01 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 4045) exited with exit code 1
LOG:  terminating any other active server processes
LOG:  database system is shut down
```

確実な方法は、目標時刻までリカバリーできるバックアップ、つまり指定した時刻より前に完了したバックアップを、pgBackRestに自動選択させることです。

注：

リストアの種類が`xid`または`name`の場合、pgBackRestはバックアップを自動選択できません。

pg-primary **⇒** デモクラスターを`2026-10-02 18:57:39.575732+00`の時点にリストアする

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 18:57:39.575732+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 18:57:39.575732+00'
recovery_target_action = 'promote'
```

pgBackRestが`postgresql.auto.conf`にリカバリー設定を生成したので、すぐにPostgreSQLを起動できます。`%f`はPostgreSQLが必要とするWALセグメントの指定、`%p`はそのコピー先の場所です。PostgreSQLのリカバリーが完了すると、テーブルが再び存在するようになり、クエリーを実行できます。

pg-primary **⇒** PostgreSQLを起動し、重要なテーブルが存在することを確認する

```bash
sudo systemctl start postgresql-14.service
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

PostgreSQLのログにも有用な情報があります。リカバリーが停止した時刻とトランザクションに加え、最後に適用したトランザクションの時刻も表示されます。

pg-primary **⇒** PostgreSQLのログ出力を確認する

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 5 lines of output]
LOG:  database system was interrupted; last known up at 2026-10-02 18:57:28 UTC
LOG:  restored log file "00000004.history" from archive
LOG:  starting point-in-time recovery to 2026-10-02 18:57:39.575732+00
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
       [filtered 2 lines of output]
LOG:  consistent recovery state reached at 0/19000100
LOG:  database system is ready to accept read-only connections
LOG:  recovery stopping before commit of transaction 743, time 2026-10-02 18:57:40.904112+00
LOG:  redo done at 0/1901E6C0 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
LOG:  last completed transaction was at log time 2026-10-02 18:57:38.228184+00
LOG:  selected new timeline ID: 5
LOG:  archive recovery complete
LOG:  database system is ready to accept connections
```

--------

## stanzaの削除 {#delete-a-stanza}

`stanza-delete`コマンドは、stanzaに関連するデータをリポジトリから削除します。

警告：

このコマンドは慎重に使用してください。指定したstanzaのすべてのバックアップとアーカイブを、pgBackRestリポジトリから完全に削除します。

stanzaを削除するには、次の手順を実行します。

- stanzaに関連付けられたPostgreSQLクラスターを停止します（または--forceでこの要件を無視します）。
- `stanza-delete`コマンドを実行するホストで、`stop`コマンドを実行します。
- `stanza-delete`コマンドを実行します。

コマンドが正常に完了したら、すべてのpgBackRest設定ファイルや環境変数からstanzaを削除するのはユーザーの責任です。

stanzaは一度に1つのリポジトリからしか削除できません。複数のリポジトリから削除するには、`--repo`オプションを指定し、リポジトリごとに`stanza-delete`コマンドを繰り返し実行してください。

pg-primary **⇒** 削除対象のPostgreSQLクラスターを停止する

```bash
sudo systemctl stop postgresql-14.service
```

pg-primary **⇒** 対象のstanzaについてpgBackRestを停止する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=4396-32c67a63 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** 1つのリポジトリからstanzaを削除する

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=4428-6f4dadb2 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## 複数のリポジトリ {#multiple-repositories}

[S3のサポート](#s3-compatible-object-store-support)に示すように、複数のリポジトリを設定できます。利点の1つは、高速なリストア用のローカルリポジトリと、冗長性のためのリモートリポジトリを併用できることです。

[`stanza-create`](/ja/docs/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/ja/docs/pgbackrest/command/stanza-upgrade/)など、一部のコマンドは設定済みのすべてのリポジトリを自動で処理します。一方、[`stanza-delete`](/ja/docs/pgbackrest/command/stanza-delete/)などのコマンドでは、`repo`オプションでリポジトリを指定する必要があります。

後方互換性を維持するため、`repo1`だけが設定されている場合は`repo`オプションは不要です。ただし、リポジトリが1つでも、たとえば`repo2`として設定されている場合は`repo`オプションが*必要です*。これは、後で新しいリポジトリを追加した際に、コマンドが動作しなくなることを防ぐためです。

`archive-push`コマンドは、設定済みのすべてのリポジトリのアーカイブに常にWALを送信します。あるリポジトリに接続できなくても、ほかのリポジトリへの送信は続きます。ただし、これを有効に機能させるには`archive-async=y`を有効にする必要があります。そうしないと、ほかのリポジトリは接続できないリポジトリよりWALセグメント1つ分しか先に進めません。また、いずれかのリポジトリにWALを送信できない場合、PostgreSQLはそのWALを`pg_wal`ディレクトリから削除しないため、ボリュームの空き容量がなくなる可能性があります。

バックアップはリポジトリごとに個別にスケジュールする必要があります。バックアップの種類や保持設定はリポジトリごとに異なるため、多くの場合これは望ましい動作です。同様に、リストアでもリポジトリを指定する必要があります。一般に、リカバリー時間が長くなっても、レイテンシーやコストの低いリポジトリをリストアに指定するほうが適しています。どのリポジトリが最も効率的かは、リストアのテストでしか判断できません。

--------

## Azure互換オブジェクトストアのサポート {#azure-compatible-object-store-support}

pgBackRestは、Azure互換オブジェクトストアへのリポジトリの配置をサポートします。リポジトリを保存するコンテナーは事前に作成する必要があり、pgBackRestは自動作成しません。コンテナーのルート（`/`）にもリポジトリを配置できますが、通常はサブパスに配置するほうが適しています。これにより、オブジェクトストアのログなどのデータも競合せずに同じコンテナーに保存できます。

警告：

階層型名前空間を有効にしないでください。期限切れ処理でエラーが発生します。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Azureを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

start-fast=y



[global:archive-push]

compress-level=3
```

`repo2-azure-key-type`オプションを`sas`に、`repo2-azure-key`オプションを共有アクセス署名トークンに設定すると、共有アクセス署名を使用できます。

コマンドは、リポジトリをローカルディスクに保存した場合とまったく同じように実行します。

pg-primary **⇒** stanzaを作成する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=4635-4a99c6c0 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

Azureではファイル作成に比較的時間がかかるため、[ファイルのバンドル化](#file-bundling)を有効にすると`backup`/`restore`の性能が向上します。

pg-primary **⇒** デモクラスターをバックアップする

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-185802F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## S3互換オブジェクトストアのサポート {#s3-compatible-object-store-support}

pgBackRestは、S3互換オブジェクトストアへのリポジトリの配置をサポートします。リポジトリを保存するバケットは事前に作成する必要があり、pgBackRestは自動作成しません。バケットのルート（`/`）にもリポジトリを配置できますが、通常はサブパスに配置するほうが適しています。これにより、オブジェクトストアのログなどのデータも競合せずに同じバケットに保存できます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** S3を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

start-fast=y



[global:archive-push]

compress-level=3
```

注：

リージョンとエンドポイントは、バケットの配置場所に合わせて設定する必要があります。ここに示す値は`us-east-1`リージョン用です。

pgBackRestを実行するロールを作成し、バケットの権限は可能な限り制限することをお勧めします。AWSのインスタンスにロールが関連付けられている場合、`repo3-s3-key-type=auto`にするとpgBackRestが一時的な認証情報を自動取得するため、`/etc/pgbackrest/pgbackrest.conf`にキーを明示的に設定する必要はありません。

このAmazon S3ポリシーの例では、すべての読み取りと書き込みを、指定のバケットとリポジトリパスに制限します。

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

コマンドは、リポジトリをローカルディスクに保存した場合とまったく同じように実行します。

pg-primary **⇒** stanzaを作成する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

S3ではファイル作成に比較的時間がかかるため、[ファイルのバンドル化](#file-bundling)を有効にすると`backup`/`restore`の性能が向上します。

pg-primary **⇒** デモクラスターをバックアップする

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-185820F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## SFTPのサポート {#sftp-support}

pgBackRestは、SFTPホストへのリポジトリの配置をサポートします。SFTPのファイル転送は比較的遅いため、`process-max`を増やしてファイル転送を並列化するとコマンドの性能が向上します。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** SFTPを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

SFTPを利用する場合、libssh2がOpenSSHに対してコンパイルされていれば、`repo4-sftp-public-key-file`は省略できます。

pg-primary **⇒** SFTPバックアップ用のSSHキーペアを生成する

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/pgsql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/pgsql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** pg-primaryのSFTPバックアップ用公開鍵をsftp-serverにコピーする

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/pgsql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

コマンドは、リポジトリをローカルディスクに保存した場合とまったく同じように実行します。

pg-primary **⇒** `repo4-sftp-host-key-check-type`のデフォルトが「strict」のため、sftp-serverのフィンガープリントをknown_hostsファイルに追加する

```bash
ssh-keyscan -H sftp-server >> /var/lib/pgsql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** stanzaを作成する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** デモクラスターをバックアップする

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-185837F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## GCS互換オブジェクトストアのサポート {#gcs-compatible-object-store-support}

pgBackRestは、GCS互換オブジェクトストアへのリポジトリの配置をサポートします。リポジトリを保存するバケットは事前に作成する必要があり、pgBackRestは自動作成しません。バケットのルート（`/`）にもリポジトリを配置できますが、通常はサブパスに配置するほうが適しています。これにより、オブジェクトストアのログなどのデータも競合せずに同じバケットに保存できます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** GCSを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

repo5-gcs-bucket=demo-bucket

repo5-gcs-key=/etc/pgbackrest/gcs-key.json

repo5-path=/demo-repo

repo5-type=gcs

start-fast=y



[global:archive-push]

compress-level=3
```

GCEで実行する場合は、`repo5-gcs-key-type=auto`を設定すると、インスタンスのサービスアカウントを使用して自動認証します。

コマンドは、リポジトリをローカルディスクに保存した場合とまったく同じように実行します。

GCSではファイル作成に比較的時間がかかるため、[ファイルのバンドル化](#file-bundling)を有効にすると`backup`/`restore`の性能が向上します。

--------

## リポジトリの目標時刻 {#target-time-for-repository}

目標時刻は、バージョン管理されたストレージ上のリポジトリをコマンドが読み込む際の時点を指定します。これにより、ある時点のリポジトリを読み込み、ユーザーの誤操作やマルウェアによって削除または破損されたデータを復元できます。

S3、GCS、Azureはストレージのバージョン管理に対応していますが、通常はデフォルトで有効になっていません。バージョン管理に加えて、S3ではオブジェクトロック、GCSやAzureでは論理削除を有効にすると有用な場合があります。

`repo-target-time`オプションを指定する場合は、`repo`オプションも指定する必要があります。すべてのリポジトリ種類がバージョン管理に対応するとは限らず、一般にリカバリーでは単一のリポジトリを対象にするのが妥当です。

ストレージのタイムスタンプとの比較は、指定したタイムスタンプ以下（<=）で行われ、指定したタイムスタンプのミリ秒部分は切り捨てられます。

この機能を示すため、S3リポジトリの`demo`stanzaを削除します。

pg-primary **⇒** S3リポジトリのstanzaを削除する

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

stanzaを削除すると、`info`コマンドはリポジトリがエラー状態であることを示します。

pg-primary **⇒** infoでエラーを確認する

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

ただし、ストレージはバージョン管理されているため、stanzaの削除前の時点のリポジトリを確認できます。状況によっては目標時刻の特定が難しい場合もありますが、この例では`backup.info`の削除時刻を調べることで、stanzaが削除された時刻を特定できます。

pg-primary **⇒** バケット内の`backup.info`のバージョンを一覧表示する

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
-------------------------------------------------------------------------------------
|                                ListObjectVersions                                 |
+--------+------------------------------------+-------------------------------------+
| Action |             Modified               |               Object                |
+--------+------------------------------------+-------------------------------------+
|  PUT   |  2026-10-02T18:58:20.631000+00:00  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T18:58:33.900000+00:00  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T18:58:45.634000+00:00  |  demo-repo/backup/demo/backup.info  |
+--------+------------------------------------+-------------------------------------+
```

これで、目標時刻を指定して`info`コマンドを実行すると、削除前のリポジトリを表示できます。

pg-primary **⇒** 目標時刻を指定してinfoを実行する

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 18:58:34+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (14): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-185820F
            timestamp start/stop: 2026-10-02 18:58:20+00 / 2026-10-02 18:58:33+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 4.2MB, backup size: 4.2MB
```

必要なバックアップが`info`コマンドで表示されれば、同じ目標時刻を使ってリストアできます。

pg-primary **⇒** 目標時刻を指定してリストアする

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 18:58:34+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=5686-f718513c --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 18:58:34+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-185820F, recovery will start at 2026-10-02 18:58:20
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00   INFO: write updated /var/lib/pgsql/14/data/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo systemctl start postgresql-14.service
```

--------

## 専用リポジトリホスト {#dedicated-repository-host}

[クイックスタート](#quick-start)で説明した構成は単純な構成に適していますが、企業での構成では通常、バックアップとWALアーカイブファイルを保存する専用リポジトリホストを用意します。これにより、バックアップとWALアーカイブをデータベースサーバーから分離し、データベースホストの障害による影響を減らせます。それでも、従来のバックアップソフトウェアでリポジトリホストをバックアップすることをお勧めします。

PostgreSQLホストでは、`pg1-path`をローカルのPostgreSQLクラスターのパスにする必要があり、`pg1-host`は設定しないことをお勧めします。リポジトリホストを設定する際は、pgbackrest設定ファイルの`pg-host`オプションで、プライマリーホストとスタンバイホスト（存在する場合）への接続を設定する必要があります。複数のPostgreSQLホストを認識するpgbackrest設定は、リポジトリホストのものだけにします。順序は関係なく、たとえばpg1-path/pg1-hostとpg2-path/pg2-hostは、どちらをプライマリーまたはスタンバイにしてもかまいません。

### インストール {#installation-1}

クラスターのバックアップを保存するため、repositoryという新しいホストを作成します。

注：

リポジトリホストにインストールするpgBackRestのバージョンは、PostgreSQLホストのバージョンと完全に一致する必要があります。

pgBackRestリポジトリの所有者として、`pgbackrest`ユーザーを作成します。どのユーザーでもリポジトリの所有者にできますが、混乱を避けるため、`postgres`が存在しても使用しないことをお勧めします。

注：

pgBackRestをパッケージからインストールすると、`/etc/logrotate.d/pgbackrest`のようなlogrotate設定が付属し、`su`ディレクティブ（例：`su postgres postgres`）により特定のユーザーでログをローテーションする場合があります。`/var/log/pgbackrest`のファイルは、pgBackRestを実行するユーザー（ここでは`pgbackrest`）が所有するため、`su`ディレクティブもそのユーザーに合わせて更新する必要があります。そうしないとlogrotateが権限エラーで失敗します。

repository **⇒** `pgbackrest`ユーザーを作成する

```bash
sudo groupadd pgbackrest
sudo adduser -gpgbackrest -n pgbackrest
```

pgBackRestはソースからビルドするより、パッケージからインストールすることをお勧めします。パッケージからインストールする場合、このセクションの残りの手順は通常不要ですが、パッケージが一部のディレクトリを作成しなかったり、誤った権限を設定したりする可能性があります。その場合は、手動でディレクトリを作成したり権限を更新したりする必要がある場合があります。

pgBackRestのRHELパッケージは[yum.postgresql.org](http://yum.postgresql.org)から入手できます。

使用するディストリビューションやバージョン向けのパッケージがない場合は、[ソースからビルド](#build)し、ここに示す手順で手動インストールできます。

repository **⇒** 依存パッケージをインストールする

```bash
sudo yum install postgresql-libs libssh2
```

repository **⇒** ビルド用ホストからpgBackRestバイナリをコピーする

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRestには、ログディレクトリ、設定ディレクトリ、設定ファイルが必要です。

repository **⇒** pgBackRestの設定ファイルとディレクトリを作成する

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

repository **⇒** pgBackRestのリポジトリを作成する

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### 設定 {#configuration}

pgBackRestは、クライアント証明書付きのTLSを使用してホスト間で通信できます。SSHも使用できます。[SSHの設定](/ja/docs/pgbackrest/user-guide/#setup-passwordless-ssh)を参照してください。

pgBackRestのクライアント証明書とサーバー証明書は、PostgreSQLと同じ方法で生成することを想定しています。証明書の生成手順の詳細は[TLSによる安全なTCP/IP接続](https://www.postgresql.org/docs/current/ssl-tcp.html)を参照してください。

リポジトリホストには、pg-primaryのホスト名、ユーザー、データベースパスを設定する必要があります。後でスタンバイを追加できるよう、プライマリーは`pg1`として設定します。

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-host`/`pg1-host-user`と`pg1-path`を設定する

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

データベースホストには、リポジトリのホスト名とユーザーを設定する必要があります。`repo1-host-user`オプションのデフォルトは`pgbackrest`です。`postgres`ユーザーがリポジトリホストでリストアを行う場合は、同じ`postgres`ユーザーにバックアップも許可しないことをお勧めします。ただし、`postgres`ユーザーが`pgbackrest`ユーザーと同じグループに属していれば、リポジトリを直接読み取ることはできます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-host`/`repo1-host-user`を設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

PostgreSQLの設定は[アーカイブの設定](#configure-archiving)を参照してください。

コマンドの実行方法は単一ホスト構成と同じですが、`backup`や`expire`など、一部のコマンドはデータベースホストではなくリポジトリホストから実行します。

### TLSサーバーの設定 {#setup-tls-server}

各ホストで、pgBackRestのTLSサーバーを設定して起動する必要があります。

repository **⇒** pgBackRestサーバーを設定する

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=pgbackrest
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

pg-primary **⇒** pgBackRestサーバーを設定する

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### stanzaの作成と確認 {#create-and-check-stanza}

新しいリポジトリにstanzaを作成します。

repository **⇒** stanzaを作成する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

データベースホストとリポジトリホストの両方で、設定が正しいことを確認します。`check`コマンドの詳細は[設定の確認](#check-the-configuration)を参照してください。

pg-primary **⇒** 設定を確認する

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

repository **⇒** 設定を確認する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### バックアップの実行 {#perform-a-backup-1}

PostgreSQLクラスターのバックアップを行うには、リポジトリホストでpgBackRestの`backup`コマンドを実行します。

repository **⇒** デモクラスターをバックアップする

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

リポジトリホストに新しいリポジトリを作成したため、増分バックアップをフルバックアップに変更するという警告が表示されました。

### バックアップのリストア {#restore-a-backup-1}

PostgreSQLクラスターをリストアするには、データベースホストでpgBackRestの`restore`コマンドを実行します。

pg-primary **⇒** デモクラスターを停止し、リストアしてPostgreSQLを再起動する

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo systemctl start postgresql-14.service
```

--------

## バックアップとリストアの並列実行 {#parallel-backup--restore}

pgBackRestは並列処理により、圧縮と転送の性能を向上させます。この機能で使用するプロセス数は、`--process-max`オプションで設定します。

通常、`backup`コマンドで使用するCPUは、利用可能なCPUの25%以内に抑えることをお勧めします。バックアップは定期的に行っていればそれほど高速である必要はなく、できる限りデータベースの性能に影響を与えないようにすることが望まれます。

restoreコマンドでは利用可能なすべてのCPUを使用でき、そうすることをお勧めします。リストア中はPostgreSQLクラスターが停止し、通常はホストでほかの重要な処理が行われていないためです。ホストに複数のクラスターがある場合は、それを考慮してリストアの並列度を設定してください。

repository **⇒** 単一プロセスでバックアップを実行する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** 複数の`backup`プロセスを使用するようpgBackRestを設定する

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository **⇒** 複数プロセスでバックアップを実行する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** デモクラスターのバックアップ情報を取得する

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (14): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-185937F
            timestamp start/stop: 2026-10-02 18:59:37+00 / 2026-10-02 18:59:40+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB

        full backup: 20261002-185941F
            timestamp start/stop: 2026-10-02 18:59:41+00 / 2026-10-02 18:59:43+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB
```

複数プロセスを使うことで、最後のバックアップの性能は向上しているはずです。非常に小さなバックアップでは違いが明確でない場合もありますが、データベースが大きくなるほど短縮できる時間も増えます。

--------

## 開始と停止 {#starting-and-stopping}

テストのためにスタンバイを昇格させたり、本番バックアップからテスト用クラスターをリストアしたりする場合、それらのクラスターがpgBackRestリポジトリに書き込めないようにしておくことをお勧めします。これは`stop`コマンドで行えます。

`stop`によってブロックされる書き込みコマンドは、`archive-push`、`backup`、`expire`、`stanza-create`、`stanza-upgrade`です。`stanza-delete`はこの規則の例外です（詳細は[stanzaの削除](#delete-a-stanza)を参照）。

pg-primary **⇒** pgBackRestの書き込みコマンドを停止する

```bash
sudo -u postgres pgbackrest stop
```

新たなpgBackRestの書き込みコマンドは実行されなくなります。

repository **⇒** バックアップを試みる

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

現在実行中のpgBackRest書き込みコマンドも終了するには、`--force`オプションを指定します。非同期のarchive-getも対象に含まれますが、PostgreSQLが必要とすれば再び実行されます。pgBackRestがすでに停止している場合、再度停止すると警告が出ます。

pg-primary **⇒** pgBackRestのサービスを再度停止する

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

pgBackRestの書き込みコマンドを再び許可するには、`start`コマンドを使用します。停止前に進行中だった書き込みコマンドが自動で再開されることはありませんが、新たに開始することは許可されます。

pg-primary **⇒** pgBackRestの書き込みコマンドを開始する

```bash
sudo -u postgres pgbackrest start
```

単一のstanzaについてのみpgBackRestを停止することもできます。

pg-primary **⇒** `demo`stanzaのpgBackRest書き込みコマンドを停止する

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

指定したstanzaでは、新たなpgBackRestの書き込みコマンドは実行されなくなります。

repository **⇒** バックアップを試みる

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

単一のstanzaのpgBackRest書き込みコマンドを開始する場合も、stanzaを指定する必要があります。

pg-primary **⇒** `demo`stanzaのpgBackRest書き込みコマンドを開始する

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## レプリケーション {#replication}

レプリケーションでは、単一のプライマリーからPostgreSQLクラスターの複数のコピー（スタンバイと呼びます）を作成できます。スタンバイは読み取り負荷の分散に利用でき、プライマリーホストの障害に備えた冗長性も提供します。

### インストール {#installation-2}

スタンバイを実行するため、pg-standbyという新しいホストを作成します。

pgBackRestはソースからビルドするより、パッケージからインストールすることをお勧めします。パッケージからインストールする場合、このセクションの残りの手順は通常不要ですが、パッケージが一部のディレクトリを作成しなかったり、誤った権限を設定したりする可能性があります。その場合は、手動でディレクトリを作成したり権限を更新したりする必要がある場合があります。

pgBackRestのRHELパッケージは[yum.postgresql.org](http://yum.postgresql.org)から入手できます。

使用するディストリビューションやバージョン向けのパッケージがない場合は、[ソースからビルド](#build)し、ここに示す手順で手動インストールできます。

pg-standby **⇒** 依存パッケージをインストールする

```bash
sudo yum install postgresql-libs libssh2
```

pg-standby **⇒** ビルド用ホストからpgBackRestバイナリをコピーする

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRestには、ログディレクトリ、設定ディレクトリ、設定ファイルが必要です。

pg-standby **⇒** pgBackRestの設定ファイルとディレクトリを作成する

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### ホットスタンバイ {#hot-standby}

ホットスタンバイは、WALアーカイブを使ってレプリケーションを行い、読み取り専用のクエリーを受け付けます。

pgBackRestの設定はpg-primaryとほぼ同じですが、WALストリームの末尾に達してもクラスターをリカバリーモードに保つため、リカバリーの種類に`standby`を使用します。

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** スタンバイのpgBackRestを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-standby **⇒** pgBackRestサーバーを設定する

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

PostgreSQLのリストア先パスを作成します。

pg-standby **⇒** PostgreSQLのパスを作成する

```bash
sudo -u postgres mkdir -p -m 700 /var/lib/pgsql/14/data
```

これで`restore`コマンドを使ってスタンバイを作成できます。

重要：

新しいプライマリーにする目的ではなく、レポート作成やテストなどのためにクラスターを昇格させる場合は、`--archive-mode=off`を使うか、`postgresql.conf`にarchive_mode=offを設定してアーカイブを無効にしてください。無効にしないと、リポジトリに不要なWALが混入し、リストアが難しくなる可能性があります。

pg-standby **⇒** デモのスタンバイクラスターをリストアする

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:04
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

この設定は、スタンバイがプライマリーに昇格した場合に備えたものです。

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** PostgreSQLを設定する

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** PostgreSQLを起動する

```bash
sudo systemctl start postgresql-14.service
```

PostgreSQLのログから、リカバリーについて有用な情報が得られます。特に、クラスターがスタンバイモードに入り、読み取り専用接続を受け付ける準備ができたことを確認してください。

pg-standby **⇒** PostgreSQLのログ出力で、成功を示すメッセージを確認する

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 4 lines of output]
LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
LOG:  database system was interrupted; last known up at 2026-10-02 18:59:41 UTC
LOG:  entering standby mode
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
       [filtered 3 lines of output]
```

レプリケーションが正しく設定されているかを簡単にテストするには、pg-primaryにテーブルを作成します。

pg-primary **⇒** プライマリーに新しいテーブルを作成する

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

続いて、pg-standbyで同じテーブルにクエリーを実行します。

pg-standby **⇒** スタンバイで新しいテーブルにクエリーを実行する

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

ここで失敗するのは、PostgreSQLがアーカイブからWALセグメントを取得してレプリケーションしているためです。変更を含むWALセグメントがpg-primaryから送信されるまで、その変更はスタンバイに現れません。

`pg_switch_wal()`を呼び出すと、現在のWALセグメントをアーカイブに手動で送信できます（以後の変更を格納する新しいWALセグメントが作成されます）。

pg-primary **⇒** `pg_switch_wal()`を呼び出す

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/2601E7C0    | 2026-10-02 19:00:10.880013+00
(1 row)
```

少し待つと、pg-standbyにテーブルが現れます。

pg-standby **⇒** スタンバイに新しいテーブルが存在することを確認する（数回の再試行が必要な場合があります）

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:11.954843+00
(1 row)
```

スタンバイがリポジトリにアクセスできる設定になっていることを確認します。

pg-standby **⇒** 設定を確認する

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1250-e6a5e2d8 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### ストリーミングレプリケーション {#streaming-replication}

ストリーミングレプリケーションは、WALアーカイブだけに頼らず、プライマリーに直接接続して、プライマリーで変更が行われるとすぐに適用します。そのため、プライマリーとスタンバイの間の遅延が大幅に減ります。

ストリーミングレプリケーションには、レプリケーション権限を持つユーザーが必要です。

pg-primary **⇒** レプリケーション用ユーザーを作成する

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

スタンバイがレプリケーション用ユーザーとして接続できるよう、`pg_hba.conf`を更新する必要があります。以下のIPアドレスは、必ずpg-standbyの実際のIPアドレスに置き換えてください。`pg_hba.conf`の変更後は再読み込みが必要です。

pg-primary **⇒** レプリケーション用ユーザーのエントリを`pg_hba.conf`に作成する

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /var/lib/pgsql/14/data/pg_hba.conf'
sudo systemctl reload postgresql-14.service
```

スタンバイにはプライマリーへの接続方法を知らせる必要があるため、pgBackRestでprimary_conninfoを設定します。

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** primary_conninfoを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

primary_conninfoにパスワードを設定することもできますが、`.pgpass`ファイルのほうが柔軟かつ安全です。

pg-standby **⇒** `.pgpass`ファイルにレプリケーションのパスワードを設定する。

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/pgsql/.pgpass'
sudo -u postgres chmod 600 /var/lib/pgsql/.pgpass
```

これで`restore`コマンドを使ってスタンバイを作成できます。

pg-standby **⇒** PostgreSQLを停止し、デモのスタンバイクラスターをリストアする

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:18
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

注：

primary_conninfoは、`pgbackrest.conf`で`recovery-option`として設定したため、`postgresql.auto.conf`ファイルに書き込まれています。既存の`postgresql.auto.conf`ファイルをそのまま残したい場合は、`restore`に`--type=preserve`オプションを指定できます。

RHELではデフォルトで、`postgresql.conf`ファイルをPostgreSQLのデータディレクトリに保存します。そのため、前回のリストアで`postgresql.conf`への変更が上書きされており、hot_standbyを再度有効にする必要があります。別の対処方法として、`postgresql.conf`をほかの場所に保存するか、pg-primaryホストでhot_standbyを有効にしておくこともできます。プライマリーではこの設定は無視されます。

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** hot_standbyを有効にする

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

hot_standby = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** PostgreSQLを起動する

```bash
sudo systemctl start postgresql-14.service
```

PostgreSQLのログで、ストリーミングレプリケーションが開始したことを確認できます。

pg-standby **⇒** PostgreSQLのログ出力で、成功を示すメッセージを確認する

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 12 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "000000070000000000000026" from archive
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

これでpg-primaryにテーブルを作成すると、`pg_switch_wal()`を呼び出さなくても、pg-standbyにすぐ現れます。

pg-primary **⇒** プライマリーに新しいテーブルを作成する

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.428653+00
(1 row)
```

pg-standby **⇒** スタンバイでテーブルにクエリーを実行する

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.605628+00
(1 row)
```

--------

## 複数のstanza {#multiple-stanzas}

pgBackRestは複数のstanzaをサポートします。最も一般的な用途は、複数のstanzaでリポジトリホストを共有することです。

### インストール {#installation-3}

新しいプライマリーを実行するため、pg-altという新しいホストを作成します。

pgBackRestはソースからビルドするより、パッケージからインストールすることをお勧めします。パッケージからインストールする場合、このセクションの残りの手順は通常不要ですが、パッケージが一部のディレクトリを作成しなかったり、誤った権限を設定したりする可能性があります。その場合は、手動でディレクトリを作成したり権限を更新したりする必要がある場合があります。

pgBackRestのRHELパッケージは[yum.postgresql.org](http://yum.postgresql.org)から入手できます。

使用するディストリビューションやバージョン向けのパッケージがない場合は、[ソースからビルド](#build)し、ここに示す手順で手動インストールできます。

pg-alt **⇒** 依存パッケージをインストールする

```bash
sudo yum install postgresql-libs libssh2
```

pg-alt **⇒** ビルド用ホストからpgBackRestバイナリをコピーする

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRestには、ログディレクトリ、設定ディレクトリ、設定ファイルが必要です。

pg-alt **⇒** pgBackRestの設定ファイルとディレクトリを作成する

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### 設定 {#configuration-1}

pgBackRestの設定はpg-primaryとほぼ同じですが、`demo-alt`stanzaを使うため、バックアップとアーカイブは別の場所に保存されます。

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** 新しいプライマリーのpgBackRestを設定する

```ini
[demo-alt]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo-alt

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-host`/`pg1-host-user`と`pg1-path`を設定する

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-alt **⇒** pgBackRestサーバーを設定する

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### デモクラスターのセットアップ {#setup-demo-cluster-1}

pg-alt **⇒** デモクラスターを作成する

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

pg-alt:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** PostgreSQLを設定する

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-alt **⇒** デモクラスターを起動する

```bash
sudo systemctl restart postgresql-14.service
```

### stanzaの作成と設定の確認 {#create-the-stanza-and-check-configuration}

stanzaを初期化するには、`stanza-create`コマンドを実行する必要があります。アーカイブとバックアップが正しく設定されていることを確認するため、`stanza-create`の後に`check`コマンドを実行することをお勧めします。

pg-alt **⇒** stanzaを作成して設定を確認する

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=929-571b66d7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=962-2cadc106 --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000001-5cb25be2e89d0324cc2a94cbc964295204118888.gz' on repo1
P00   INFO: check command end: completed successfully
```

リポジトリホストで`check`コマンドを実行すると、すべてのstanzaが確認されます。

repository **⇒** すべてのstanzaの設定を確認する

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1384-3bcda35c --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/000000070000000000000027-b36b790bcf0b1a9f54bc84458117feb77853d452.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000002-c303ffb17f8a111070459593520aa35640317a38.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## 非同期アーカイブ {#asynchronous-archiving}

非同期アーカイブは`archive-async`オプションで有効にします。このオプションにより、`archive-push`と`archive-get`の両コマンドが非同期に動作します。

スプールパスが必要です。各コマンドはここに一時的なデータを保存しますが、動作が大きく異なるため、スプールパスの使用方法は各セクションで詳しく説明します。

pg-primary **⇒** スプールディレクトリを作成する

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** スプールディレクトリを作成する

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

スプールパスを設定し、非同期アーカイブを有効にする必要があります。非同期アーカイブだけでもリモートストレージへの接続回数が減る利点がありますが、`process-max`を設定して処理を並列化すると、性能が大幅に向上します。通常のデータベース操作に影響が出るほど`process-max`を大きくしないようにしてください。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** スプールパスと非同期アーカイブを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** スプールパスと非同期アーカイブを設定する

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

注：

`process-max`は、バックアップとリストアでこの設定を使わないよう、コマンド別のセクションで設定します。これにより、`archive-push`と`archive-get`に異なる値を設定することもできます。

デモのためにストリーミングレプリケーションを切断し、PostgreSQLがrestore_commandを使ってWALを取得するようにします。

pg-primary **⇒** レプリケーションのパスワードを変更してストリーミングレプリケーションを切断する

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** スタンバイを再起動して接続を切断する

```bash
sudo systemctl restart postgresql-14.service
```

### アーカイブへの送信 {#archive-push}

非同期の`archive-push`コマンドは、WALのアーカイブ処理を別のプロセス（または複数のプロセス）に任せてスループットを向上させます。PostgreSQLが現在`archive_command`で要求しているセグメントの先を調べ、アーカイブ可能なWALセグメントを確認して処理します。WALセグメントは`pg_xlog`/`pg_wal`ディレクトリから直接アーカイブに転送され、`archive_command`が成功を返すのは、WALセグメントがアーカイブに安全に保存された後だけです。

スプールパスには、WALアーカイブの現在の状態を保存します。スプールディレクトリに書き込まれる状態ファイルは通常長さゼロで、使用する容量はごくわずか（最大でも数MB）、I/Oも非常に少ないはずです。このディレクトリの情報はすべて再作成できるため、クラスターを新しいハードウェアに移動する場合も、スプールディレクトリを保持する必要はありません。

重要：

非同期アーカイブの当初の実装では、圧縮と転送の前にWALセグメントをスプールディレクトリにコピーしていました。新しい実装では、`pg_xlog`ディレクトリからWALを直接コピーします。v1.12以前で非同期アーカイブを利用していた場合は、アップグレード前にv1.13のリリースノートをよく読んでください。

`[stanza]-archive-push-async.log`ファイルで、非同期プロセスの動作を監視できます。短時間に複数のWALセグメントを送信すると、動作のテストに適しています。

pg-primary **⇒** 並列の非同期アーカイブをテストする

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=6864-e51531e7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/00000007000000000000002D-7addc4d9a1861c1b8b68300ea3a7db01fbe08ae2.gz' on repo1
P00   INFO: check command end: completed successfully
```

これでログファイルに並列かつ非同期の処理が記録されます。

pg-primary **⇒** ログで結果を確認する

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6828-6cf1b924 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6866-2a936d60 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully
```

### アーカイブからの取得 {#archive-get}

非同期の`archive-get`コマンドは、WALのローカルキューを維持してスループットを向上させます。要求されたWALセグメントがキューにない場合は、キューを満たすだけの後続WALとともにリポジトリから取得します。キューの最大サイズは`archive-get-queue-max`で定義します。キューが半分未満になるたびに、追加のWALを取得して満たします。

非同期動作は、大量のWALを生成する環境や、リポジトリストレージ（S3などのオブジェクトストア）との接続のレイテンシーが高い環境で特に有用です。レイテンシーが高い場合は、`process-max`を増やすとよい場合があります。

`[stanza]-archive-get-async.log`ファイルで、非同期プロセスの動作を監視できます。

pg-standby **⇒** ログで結果を確認する

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=1919-a90112cb --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P01 DETAIL: found 000000070000000000000024 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000025 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000027 in the repo1: 14-1 archive
P01 DETAIL: found 000000070000000000000026 in the repo1: 14-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 31 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=1976-2ef79408 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P01 DETAIL: found 000000070000000000000028 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000029 in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002A in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002B in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002D in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002C in the repo1: 14-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 14 lines of output]
```

pg-primary **⇒** レプリケーションのパスワードを変更してストリーミングレプリケーションを修復する

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## スタンバイからのバックアップ {#backup-from-a-standby}

pgBackRestは、プライマリーの代わりにスタンバイでバックアップを実行できます。スタンバイからのバックアップには、pg-standbyホストの設定と`backup-standby`オプションの有効化が必要です。複数のスタンバイが設定されている場合は、最初に見つかった稼働中のスタンバイをバックアップに使用します。

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg2-host`/`pg2-host-user`と`pg2-path`を設定する

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

バックアップの実行には、プライマリーとスタンバイの両データベースが必要ですが、プライマリーの負荷を減らすため、ファイルの大半はスタンバイからコピーします。データベースホストの設定順序は任意です。pgBackRestがプライマリーとスタンバイを自動判別します。

repository **⇒** pg2からデモクラスターをバックアップする

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/log/postgresql.log (10.9KB, 0.42%) checksum dbfa988289c2ff32dcd198f19455165722870b43
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/global/pg_control (8KB, 0.73%) checksum 0a793efbb7bb2e255bbb2bfac8f612bc943c7f31
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/pg_hba.conf (4.5KB, 0.90%) checksum cfa97af1dab1b130f0a921fa2d10d76fe0c5f630
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/current_logfiles (26B, 0.91%) checksum 78a9f5c10960f0d91fcd313937469824861795a2
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/pg_logical/replorigin_checkpoint (8B, 0.91%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1263 lines of output]
```

この増分バックアップでは、大半のファイルをpg-standbyホストからコピーし、pg-primaryホストからは少数のファイルだけをコピーしていることが分かります。

pgBackRestがスタンバイから作成するバックアップは、プライマリーで実行したバックアップと同一です。そのために、pg-primaryホストでバックアップを開始・停止し、レプリケーションされるファイルだけをpg-standbyホストからコピーして、残りの少数のファイルをpg-primaryホストからコピーします。したがって、プライマリーデータベースのログと統計情報もバックアップに含まれます。

--------

## PostgreSQLのアップグレード {#upgrading-postgresql}

PostgreSQLを新しいメジャーバージョンにアップグレードしたら、直ちにすべてのpgBackRest設定の`pg-path`を新しいデータベースの場所に変更し、`stanza-upgrade`コマンドを実行する必要があります。ホストに複数のリポジトリが設定されている場合は、それぞれでstanzaをアップグレードします。データベースがオフラインの場合は、`--no-online`オプションを使用してください。

以下はPostgreSQLのアップグレードを網羅した手順ではありません。pgBackRestの再設定に必要な手順を示すため、プライマリーとスタンバイのアップグレードの大まかな流れを説明します。アップグレード前にバックアップを取ることをお勧めします。

pg-primary **⇒** 古いクラスターを停止する

```bash
sudo systemctl stop postgresql-14.service
```

スタンバイはアップグレードした新しいクラスターからリストアするため、スタンバイの古いクラスターも停止します。

pg-standby **⇒** 古いクラスターを停止する

```bash
sudo systemctl stop postgresql-14.service
```

新しいクラスターを作成してアップグレードします。

pg-primary **⇒** 新しいクラスターを作成してアップグレードする

```bash
sudo -u postgres /usr/pgsql-15/bin/initdb \
       -D /var/lib/pgsql/15/data -k -A peer
sudo -u postgres sh -c 'cd /var/lib/pgsql && \
       /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir=/usr/pgsql-14/bin \
       --new-bindir=/usr/pgsql-15/bin \
       --old-datadir=/var/lib/pgsql/14/data \
       --new-datadir=/var/lib/pgsql/15/data \
       --old-options=" -c config_file=/var/lib/pgsql/14/data/postgresql.conf" \
       --new-options=" -c config_file=/var/lib/pgsql/15/data/postgresql.conf"'
```

```text
       [filtered 41 lines of output]
Checking for extension updates                              ok
Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

新しいクラスターの設定とポートを設定します。

pg-primary:`/var/lib/pgsql/15/data/postgresql.conf` **⇒** PostgreSQLを設定する

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

すべてのシステムでpgBackRestの設定を更新し、新しいクラスターを参照させます。

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-path`を更新する

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg-path`を更新する

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-path`と`pg2-path`を更新し、スタンバイからのバックアップを無効にする

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-primary **⇒** hba設定をコピーする

```bash
sudo cp /var/lib/pgsql/14/data/pg_hba.conf \
       /var/lib/pgsql/15/data/pg_hba.conf
```

新しいクラスターを起動する前に、`stanza-upgrade`コマンドを実行する必要があります。

pg-primary **⇒** stanzaをアップグレードする

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=7454-62cfb155 --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/pgsql/15/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

新しいクラスターを起動し、正しくインストールされたことを確認します。

pg-primary **⇒** 新しいクラスターを起動する

```bash
sudo systemctl start postgresql-15.service
```

`check`コマンドを使って設定をテストします。

pg-primary **⇒** 設定を確認する

```bash
sudo systemctl status postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

古いクラスターを削除します。

pg-primary **⇒** 古いクラスターを削除する

```bash
sudo rm -rf /var/lib/pgsql/14/data
```

スタンバイに新しいPostgreSQLバイナリをインストールし、クラスターを作成します。

pg-standby **⇒** 古いクラスターを削除し、新しいクラスターを作成する

```bash
sudo rm -rf /var/lib/pgsql/14/data
sudo -u postgres mkdir -p -m 700 /usr/pgsql-15/bin
```

リポジトリホストで`check`を実行します。スタンバイクラスターは停止しているため、スタンバイが停止しているという警告は想定どおりです。このコマンドの実行により、リポジトリサーバーがスタンバイを認識し、プライマリーサーバーに対して正しく設定されていることを確認できます。

repository **⇒** 設定を確認する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 tls protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

新しいクラスターでフルバックアップを実行し、そのバックアップからスタンバイをリストアします。`incr`または`diff`を要求しても、バックアップの種類は自動で`full`に変更されます。

repository **⇒** フルバックアップを実行する

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** デモのスタンバイクラスターをリストアする

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
```

pg-standby **⇒** PostgreSQLを起動し、pgBackRestの設定を確認する

```bash
sudo systemctl start postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

スタンバイのリストアが完了したので、スタンバイからのバックアップを有効にできます。

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** スタンバイからのバックアップを再び有効にする

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```
