---
title: "設定リファレンス"
linkTitle: "設定"
weight: 50
description: "アーカイブ、バックアップ、リポジトリ、クラウドストレージのオプションを含む、pgBackRestの全設定を網羅したリファレンス。"
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/configuration.html"
---

--------

## はじめに {#introduction}

pgBackRestはコマンドラインパラメーターだけでも使用できますが、構成が複雑な場合や多数のオプションを設定する場合は、設定ファイルの方が実用的です。設定ファイルのデフォルトの場所は`/etc/pgbackrest/pgbackrest.conf`です。この場所にファイルがない場合は、旧デフォルトの`/etc/pgbackrest.conf`を確認します。

次のオプション型を使用します。

**文字列**：通常は識別子やパスワードなどを表すテキスト文字列です。

コマンドラインの例：`--stanza=demo`<br/>設定ファイルの例：`repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**パス**：ディレクトリ構造内の場所を一意に識別します。パスは/で始める必要があり、連続する//は使用できません。末尾には/を付けません。

コマンドラインの例：`--repo1-path=/var/lib/pgbackrest`<br/>設定ファイルの例：`repo1-path=/var/lib/pgbackrest`

**真偽値**：オプションを有効または無効にします。有効な引数値はy/nのみです。

コマンドラインの例：`--start-fast`、`--no-start-fast`、`--start-fast=y`、`--start-fast=n`<br/>設定ファイルの例：`start-fast=y`、`start-fast=n`

**整数**：ポート、保持数や再試行回数、許可する並列プロセス数などに使用します。

コマンドラインの例：`--compress-level=3`<br/>設定ファイルの例：`pg1-port=5432`

**サイズ**：バッファーサイズやディスク使用量などに使用します。サイズはバイト（デフォルト）、または1024の累乗を倍率とするKiB、MiB、GiB、TiB、PiBで指定できます。たとえば、5368709120の代わりに、大文字と小文字を区別しない5GiB（または5GB、5g）を使用できます。2.5GiBのような小数値は指定できないため、代わりに2560MiBを使用してください。

コマンドラインの例：`--archive-get-queue-max=1GiB`<br/>設定ファイルの例：`buffer-size=2MiB`

**時間**：秒単位の時間です。

コマンドラインの例：`--io-timeout=90`<br/>設定ファイルの例：`db-timeout=600`

**リスト**：オプションを複数回指定できます。

コマンドラインの例：`--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`

設定ファイルの例（それぞれ別の行に記述）：

```ini
db-exclude=db1
db-exclude=db2
db-exclude=db5
```

**キー/値**：`key=value`形式でオプションを複数回指定できます。

コマンドラインの例：`--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`

設定ファイルの例（それぞれ別の行に記述）：

```ini
tablespace-map=ts_01=/db/ts_01
tablespace-map=ts_02=/db/ts_02
```

--------

## アーカイブオプション {#archive-options}

`archive`セクションでは、`archive-push`コマンドと`archive-get`コマンドのオプションを定義します。

### 非同期アーカイブオプション（`--archive-async`） {#asynchronous-archiving-option---archive-async}

WALセグメントを非同期に送信/取得します。

`archive-push`コマンドと`archive-get`コマンドの非同期処理を有効にします。

非同期処理では接続の再利用と並列処理が可能なため、効率が向上します。詳細は`spool-path`、`archive-get-queue-max`、`archive-push-queue-max`の各オプションを参照してください。

```text
default: n
example: archive-async=y
```

### アーカイブ取得キューの最大サイズオプション（`--archive-get-queue-max`） {#maximum-archive-get-queue-size-option---archive-get-queue-max}

pgBackRestのarchive-getキューの最大サイズです。

`archive-async`が有効な場合の`archive-get`キューの最大サイズを指定します。キューは`spool-path`に格納され、PostgreSQLへのWALの提供を高速化するために使用されます。

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### 欠落WALセグメントの再試行オプション（`--archive-missing-retry`） {#retry-missing-wal-segment-option---archive-missing-retry}

欠落したWALセグメントの取得を再試行します。

非同期モードの`archive-get`コマンドが以前に欠落を報告したWALセグメントの取得を再試行します。これにより、以前のリストアでスプールパスに残された通知が使用され、一貫性が確保される前にリカバリーが失敗する事態を防ぎます。

このオプションを無効にすると、PostgreSQLはアーカイブ内のWALの末尾に到達したことをより確実に認識し、プライマリーからのストリーミングに切り替えられます。再試行が有効な場合は、WALが継続的にアーカイブされると、PostgreSQLはストリーミングに切り替えずにアーカイブからのWAL取得を続けます。

このオプションを無効にする場合は、stanzaのスプールパスが空であることを必ず確認してください。リストア時にスプールパスが設定されていれば、`restore`コマンドが自動的に空にします。それ以外の場合は、ユーザーがスプールパスを空にする必要があります。

```text
default: y
example: archive-missing-retry=n
```

### アーカイブ送信バッチサイズオプション（`--archive-push-batch-size`） {#archive-push-batch-size-option---archive-push-batch-size}

非同期処理の1回の実行で送信するWALの最大量です。

非同期モードでは、`archive-push`プロセスは準備ができているすべてのWALセグメントを1回の実行で送信します。`archive-push-queue-max`は各実行の開始時にのみ確認されるため、非常に多くのセグメントを処理する実行では、再確認までの間にキューが上限を大幅に超えて増大することがあります。

このオプションは1回の実行で処理するWALの量を制限します。プロセスは終了後、次の`archive-push`によって再び起動され、その際にキューが再確認されます。値を小さくするとキューの確認頻度が高くなりますが、非同期プロセスの起動頻度も高くなります。値はWALセグメント単位で切り捨てられますが、常に少なくとも1つのセグメントは処理されます。

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### アーカイブ送信キューの最大サイズオプション（`--archive-push-queue-max`） {#maximum-archive-push-queue-size-option---archive-push-queue-max}

PostgreSQLのアーカイブキューの最大サイズです。

上限に達すると、次の処理が行われます。

- pgBackRestはWALのアーカイブが成功したことをPostgreSQLに通知した後、**そのWALを破棄します**。
- PostgreSQLのログに警告が出力されます。

この場合、アーカイブログの連続性が失われ、その時点より後へのPITRはできなくなります。完全なリストア機能を取り戻すには、新しいバックアップが必要です。

非同期モードでは、キューの上限を再び超えるまでの間にWALが断続的に送信されることを防ぐため、キュー全体を破棄します。

非同期モードでは、この上限は各`archive-push`実行の開始時にのみ確認されるため、1回の実行中にキューが上限を超えて増大することがあります。キューをより頻繁に確認するには、`archive-push-batch-size`を小さくしてください。

この機能は、ログボリュームが満杯になってPostgreSQLが完全に停止することを防ぐためのものです。PostgreSQLを停止させるよりは、バックアップを失う方を選びます。

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

非推奨の名前：archive-queue-max

### アーカイブタイムアウトオプション（`--archive-timeout`） {#archive-timeout-option---archive-timeout}

アーカイブのタイムアウトです。

各WALセグメントがpgBackRestのアーカイブリポジトリに到達するまで待機する最大時間を秒単位で設定します。このタイムアウトは、バックアップの一貫性に必要なWALセグメントのアーカイブを待つ際に、`check`コマンドと`backup`コマンドに適用されます。

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## バックアップオプション {#backup-options}

`backup`セクションでは、バックアップに関する設定を定義します。

### バックアップ注釈オプション（`--annotation`） {#backup-annotation-option---annotation}

ユーザー定義のキー/値ペアでバックアップに注釈を付けます。

バックアップに情報を示すキー/値ペアを付加できます。このオプションを複数回指定して、複数の注釈を付けられます。

注釈は、`--set`でバックアップを指定した場合に`info`コマンドのテキスト出力に表示されます。JSON出力には常に表示されます。

```text
example: annotation=source="Sunday backup for website database"
```

### アーカイブ確認オプション（`--archive-check`） {#check-archive-option---archive-check}

バックアップの完了前に、WALセグメントがアーカイブに存在することを確認します。

バックアップの一貫性を確保するために必要なすべてのWALセグメントが、WALアーカイブに存在することを確認します。別のアーカイブ方法を使用していない限り、デフォルトのままにしておくことを推奨します。

`archive-copy`が有効な場合は、このオプションを有効にする必要があります。

```text
default: y
example: archive-check=n
```

### アーカイブコピーオプション（`--archive-copy`） {#copy-archive-option---archive-copy}

一貫性の確保に必要なWALセグメントをバックアップにコピーします。

この念には念を入れたオプションは、一貫性に必要なWALセグメントをバックアップに直接格納することで、WALセグメントのアーカイブの破損に備えます。WALセグメントは引き続きアーカイブにも格納されるため、このオプションは追加の容量を使用します。

このオプションを使用する場合は、`archive-push`コマンドと`backup`コマンドで同じ`compress-type`（例：`lz4`）を使用することを推奨します。異なる場合、WALセグメントはバックアップで使用する`compress-type`で再圧縮する必要があり、バックアップ中に生成されたWALの量によっては、かなりの負荷がかかります。

リストア時にはWALセグメントが`pg_xlog/pg_wal`内に存在し、PostgreSQLは`restore_command`の呼び出しよりも優先してこれらを使用します。

`archive-copy`が有効な場合は、`archive-check`オプションを有効にする必要があります。

```text
default: n
example: archive-copy=y
```

### アーカイブモード確認オプション（`--archive-mode-check`） {#check-archive-mode-option---archive-mode-check}

PostgreSQLの`archive_mode`設定を確認します。

このオプションはデフォルトで有効で、PostgreSQLの`archive_mode=always`を禁止します。

スタンバイサーバーから送信されたWALセグメントは、プライマリーから送信されたWALセグメントと論理的には同じでも、チェックサムが異なる場合があります。競合を避けるため、複数のソースからのアーカイブを無効にすることを推奨します。

注意：

このオプションを無効にする場合は、`archive-push`コマンドを通じてリポジトリに書き込むアーカイバーが1つだけであることを必ず確認してください。

```text
default: y
example: archive-mode-check=n
```

### スタンバイからのバックアップオプション（`--backup-standby`） {#backup-from-standby-option---backup-standby}

スタンバイクラスターからバックアップします。

プライマリークラスターの負荷を軽減するには、スタンバイからのバックアップを有効にします。このオプションでは、プライマリーとスタンバイの両方のホストを設定する必要があります。

次のモードをサポートします。

- `y` - バックアップにスタンバイを必須とします。
- `prefer` - スタンバイが利用可能ならスタンバイから、そうでなければプライマリーからバックアップします。
- `n` - プライマリーからのみバックアップします。

```text
default: n
example: backup-standby=y
```

### ページチェックサムオプション（`--checksum-page`） {#page-checksums-option---checksum-page}

データページのチェックサムを検証します。

クラスターのバックアップ中に、pgBackRestがすべてのデータページのチェックサムを検証するようにします。クラスターでデータページのチェックサムが有効になっている場合、このオプションは自動的に有効になります。

デフォルトでは、チェックサムの検証に失敗してもバックアップは中止されません。ログ（デフォルト設定ではコンソールにも）に警告を出力し、無効なページの一覧をバックアップマニフェストに保存します。代わりにバックアップを終了するには、`checksum-page-error=y`を設定します。

```text
example: checksum-page=n
```

### パス/ファイルの除外オプション（`--exclude`） {#pathfile-exclusions-option---exclude}

パス/ファイルをバックアップから除外します。

すべての除外指定は`$PGDATA`を基準とします。除外指定が/で終わる場合は、指定ディレクトリ内のファイルのみを除外します。たとえば、`--exclude=junk/`は`$PGDATA/junk`ディレクトリ内のすべてのファイルを除外しますが、ディレクトリ自体は含めます。除外指定が/で終わらない場合は、ファイルが除外指定に完全一致するか、除外指定の末尾に/を付けたものに一致すれば除外します。たとえば、`--exclude=junk`は`$PGDATA/junk`ディレクトリとその中のすべてのファイルを除外します。

**この機能は慎重に使用してください。重要なものを容易に除外できてしまい、バックアップの一貫性を損なう危険があります。必ずリストアをテストしてください！**

除外されたすべてのファイルは、除外ルールとともに`info`レベルでログに記録されます。除外されたファイルの一覧を必ず確認し、意図しないものが除外されていないことを確かめてください。

注記：

差分リストアでは除外指定は考慮されません。バックアップで除外されたファイル/ディレクトリは、差分リストア時に*削除*されます。

このオプションを、バックアップからPostgreSQLのログを除外するために使用しないでください。PostgreSQLの`log_directory`設定でログを`PGDATA`ディレクトリの外に移動すれば、リストア後もログを保持できるという利点があります。

コマンドラインまたは設定ファイルで複数の除外指定が可能です。

```text
example: exclude=junk/
```

### 自動期限切れ処理オプション（`--expire-auto`） {#expire-auto-option---expire-auto}

バックアップの成功後に`expire`コマンドを自動実行します。

この設定はデフォルトで有効です。無効にすると、すべてのバックアップとアーカイブが無期限に保持され、リポジトリの空き容量がなくなる可能性があるため、注意してください。これを防ぐには、`expire`コマンドを定期的に実行する必要があります。

バックアップの成功後に`expire`を自動実行する場合は、`backup`コマンドの設定を使用するため、`expire`コマンドのセクション（例：`[global:expire]`）だけに設定したオプションは適用されません。`expire`専用の設定を適用するには、このオプションを無効にし、`expire`コマンドを個別に実行してください。

```text
default: y
example: expire-auto=y
```

### マニフェスト保存しきい値オプション（`--manifest-save-threshold`） {#manifest-save-threshold-option---manifest-save-threshold}

バックアップ中のマニフェスト保存しきい値です。

バックアップ中にマニフェストを保存する頻度を定義します。マニフェストにはチェックサムが保存され、再開機能を効率的に動作させられるため、その保存は重要です。実際に使用するしきい値は、バックアップサイズの1%と`manifest-save-threshold`のうち大きい方です。

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### 再開オプション（`--resume`） {#resume-option---resume}

失敗したバックアップの再開を許可します。

再開機能を有効にするかどうかを定義します。同じ種類のバックアップが以前に失敗した場合、再開によってバックアップの実行に必要な時間を大幅に短縮できます。ただし、処理が複雑になるため、この機能を必要としない環境では無効にする方が望ましい場合があります。

```text
default: y
example: resume=n
```

### 高速開始オプション（`--start-fast`） {#start-fast-option---start-fast}

チェックポイントを強制し、バックアップを速やかに開始します。

バックアップ開始関数の`fast`パラメーターに`y`を渡してチェックポイントを強制し、バックアップを直ちに開始します。そうしない場合、バックアップは次の通常のチェックポイントの後に開始します。

```text
default: n
example: start-fast=y
```

--------

## 一般オプション {#general-options}

`general`セクションでは、多くのコマンドに共通するオプションを定義します。

### rootでの実行許可オプション（`--allow-root`） {#allow-run-as-root-option---allow-root}

rootユーザーによるコマンドの実行を許可します。

デフォルトでは、ファイルの所有権を慎重に管理するように設計された`restore`コマンドのみをrootユーザーで実行できます。ほかのコマンドをrootで実行すると、たとえばリポジトリ内にroot所有のファイルが作成され、PostgreSQLユーザーがアクセスできなくなって、後続のコマンドが失敗するおそれがあります。

それでもコマンドをrootで実行する場合は、このオプションを有効にします。ただし、リポジトリとPostgreSQLクラスターを所有するユーザーとしてpgBackRestを実行する方がはるかに適切です。

```text
default: n
example: allow-root=y
```

### バッファーサイズオプション（`--buffer-size`） {#buffer-size-option---buffer-size}

I/O処理のバッファーサイズです。

コピー、圧縮、暗号化などの処理に使用するバッファーサイズです。使用するバッファーの数はオプションによって異なり、各処理で追加のメモリを使用する場合があります。たとえば、`gz`圧縮では256KiBのメモリを追加で使用する場合があります。

指定できる値は、`16KiB`、`32KiB`、`64KiB`、`128KiB`、`256KiB`、`512KiB`、`1MiB`、`2MiB`、`4MiB`、`8MiB`、`16MiB`です。

```text
default: 1MiB
example: buffer-size=2MiB
```

### pgBackRestコマンドオプション（`--cmd`） {#pgbackrest-command-option---cmd}

pgBackRestコマンドです。

pgBackRestは、たとえば`restore`コマンドがrestore_command設定を生成する際に、コマンド文字列を生成することがあります。この場合、`cmd`オプションを指定しない限り、pgBackRestプロセスの実行に使用したコマンドが使われます。

注意：

pgBackRestコマンドをラッパー経由で実行すると、予測できない動作を引き起こす可能性があるため、推奨しません。

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### SSHクライアントコマンドオプション（`--cmd-ssh`） {#ssh-client-command-option---cmd-ssh}

SSHクライアントのコマンドです。

別のSSHクライアントを使用したい場合や、`ssh`コマンドが$PATHに含まれていない場合に、使用するSSHクライアントコマンドを指定します。

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### 圧縮オプション（`--compress`） {#compress-option---compress}

ファイル圧縮を使用します。

バックアップファイルは、コマンドラインの圧縮ツールと互換性があります。

このオプションは現在非推奨です。代わりに`compress-type`オプションを使用してください。

```text
default: y
example: compress=n
```

### 圧縮レベルオプション（`--compress-level`） {#compress-level-option---compress-level}

ファイルの圧縮レベルです。

`compress-type`が`none`でない場合、または`compress=y`（非推奨）の場合に、ファイル圧縮に使用するレベルを設定します。

```text
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: compress-level=9
```

### ネットワーク圧縮レベルオプション（`--compress-level-network`） {#network-compress-level-option---compress-level-network}

ネットワークの圧縮レベルです。

`compress-type=none`で、コマンドがリポジトリと同じホストで実行されない場合のネットワーク圧縮レベルを設定します。圧縮によってネットワークトラフィックを削減します。`compress-type`が`none`でない場合は、ファイルを1回だけ圧縮するように、`compress-level-network`設定を無視して代わりに`compress-level`を使用します。

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### 圧縮形式オプション（`--compress-type`） {#compress-type-option---compress-type}

ファイルの圧縮形式です。

次の圧縮形式をサポートします。

- `none` - 圧縮なし
- `bz2` - bzip2圧縮形式
- `gz` - gzip圧縮形式
- `lz4` - lz4圧縮形式（一部のプラットフォームでは利用不可）
- `zst` - Zstandard圧縮形式（一部のプラットフォームでは利用不可）

```text
default: gz
example: compress-type=none
```

### データベースタイムアウトオプション（`--db-timeout`） {#database-timeout-option---db-timeout}

データベースクエリーのタイムアウトです。

データベースに対するクエリーのタイムアウトを秒単位で設定します。これには、それぞれかなりの時間がかかる可能性があるバックアップの開始/停止関数も含まれます。そのため、これらの関数が速やかに戻ることがわかっている場合（つまり、`start-fast=y`を設定し、バックアップ中にデータベースクラスターが多数のWALセグメントを生成しないことがわかっている場合）を除き、タイムアウトは長めにしておくことを推奨します。

注記：

`db-timeout`オプションは、`protocol-timeout`オプションより小さくする必要があります。

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### 差分処理オプション（`--delta`） {#delta-option---delta}

チェックサムを使用してリストアまたはバックアップします。

リストア時には、デフォルトでPostgreSQLのデータディレクトリとテーブルスペースディレクトリが存在し、空であることを想定します。このオプションは、チェックサムを使用して差分リストアを実行します。

バックアップ時には、このオプションによってタイムスタンプの代わりにチェックサムを使用し、ファイルをコピーするかどうかを判定します。

```text
default: n
example: delta=y
```

### I/Oタイムアウトオプション（`--io-timeout`） {#io-timeout-option---io-timeout}

I/Oのタイムアウトです。

接続および読み取り/書き込み処理に使用する、秒単位のタイムアウトです。

読み取り/書き込み処理全体がこのタイムアウト内に完了する必要はありませんが、わずか1バイトでも、*何らかの*進展が必要です。

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### ロックパスオプション（`--lock-path`） {#lock-path-option---lock-path}

ロックファイルを保存するパスです。

ロックパスは、pgBackRestが競合する処理の同時実行を防ぐためのロックファイルを作成する場所です。

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### 固定umaskオプション（`--neutral-umask`） {#neutral-umask-option---neutral-umask}

固定のumaskを使用します。

umaskを0000に設定し、リポジトリ内のファイルやディレクトリが適切な権限で作成されるようにします。デフォルトのディレクトリ権限は0750、ファイル権限は0640です。

代わりに実行ユーザーのumaskを使用するには、設定ファイルに`neutral-umask=n`、またはコマンドラインに`--no-neutral-umask`を指定します。

```text
default: y
example: neutral-umask=n
```

### プロセス優先度設定オプション（`--priority`） {#set-process-priority-option---priority}

プロセスの優先度を設定します。

カーネルのスケジューラーがプロセスに与える優先度（niceness）を定義します。正の値は優先度を下げ、負の値は優先度を上げます。通常、プロセスには自身の優先度を上げる権限がありません。

```text
allowed: [-20, 19]
example: priority=19
```

### 最大プロセス数オプション（`--process-max`） {#process-maximum-option---process-max}

圧縮/転送に使用する最大プロセス数です。

各プロセスが圧縮と転送を実行することでコマンドを高速化しますが、データベースのパフォーマンスに影響するほど`process-max`を高く設定しないでください。

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### プロトコルタイムアウトオプション（`--protocol-timeout`） {#protocol-timeout-option---protocol-timeout}

プロトコルのタイムアウトです。

ローカルまたはリモートのプロセスが、プロトコル層で新しいメッセージの受信を待つタイムアウトを秒単位で設定します。これにより、プロセスがメッセージを無期限に待ち続けることを防ぎます。

注記：

`protocol-timeout`オプションは、`db-timeout`オプションより大きくする必要があります。

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### キープアライブオプション（`--sck-keep-alive`） {#keep-alive-option---sck-keep-alive}

キープアライブを有効にします。

ソケット接続でキープアライブメッセージを有効にします。

```text
default: y
example: sck-keep-alive=n
```

### スプールパスオプション（`--spool-path`） {#spool-path-option---spool-path}

一時的なデータを保存するパスです。

このパスは、非同期の`archive-push`コマンドと`archive-get`コマンドのデータを保存するために使用します。

非同期の`archive-push`コマンドは、アーカイブへのWALの保存が成功すると確認応答を（失敗時にはエラーを）スプールパスに書き込み、フォアグラウンドプロセスがPostgreSQLに速やかに通知できるようにします。確認応答ファイルは非常に小さく、成功時は0バイト、エラー時も数百バイトです。

非同期の`archive-get`コマンドは、PostgreSQLの要求時にWALをすぐに提供できるよう、スプールパスにWALをキューイングします。スプールパスが`pg_xlog`/`pg_wal`と同じファイルシステム上にあると、PostgreSQLへのファイル移動が最も効率的です。ただし、スプールパスを`pg_xlog`/`pg_wal`ディレクトリの*内部*に配置すると、`pg_rewind`などのPostgreSQLユーティリティーに問題が生じる可能性があるため、推奨しません。

スプールパスに保存されたデータは再起動後も保持でき、保持することが望ましいため、厳密には一時データではありません。ただし、スプールパス内のデータが失われても問題はありません。pgBackRestは、`archive-push`では各WALセグメントが安全にアーカイブされていることを再確認し、`archive-get`ではキューを再構築するだけです。

スプールパスは、NFSやCIFSなどのリモートファイルシステムではなく、ローカルのPosix互換ファイルシステム上に置くことを想定しています。

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### キープアライブ回数オプション（`--tcp-keep-alive-count`） {#keep-alive-count-option---tcp-keep-alive-count}

キープアライブの回数です。

接続が切れたと判断するまでに、応答がなくても許容するTCPキープアライブメッセージの数を指定します。

このオプションは、`TCP_KEEPCNT`ソケットオプションをサポートするシステムで利用できます。

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### キープアライブ待機時間オプション（`--tcp-keep-alive-idle`） {#keep-alive-idle-option---tcp-keep-alive-idle}

キープアライブの待機時間です。

ネットワーク通信がない状態で、オペレーティングシステムがTCPキープアライブメッセージを送信するまでの時間を秒単位で指定します。

このオプションは、`TCP_KEEPIDLE`ソケットオプションをサポートするシステムで利用できます。

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### キープアライブ間隔オプション（`--tcp-keep-alive-interval`） {#keep-alive-interval-option---tcp-keep-alive-interval}

キープアライブの送信間隔です。

応答のないTCPキープアライブメッセージを再送信するまでの時間を秒単位で指定します。

このオプションは、`TCP_KEEPINTVL`ソケットオプションをサポートするシステムで利用できます。

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### TLSv1.2暗号スイートオプション（`--tls-cipher-12`） {#tlsv12-cipher-suites-option---tls-cipher-12}

許可するTLSv1.2暗号スイートです。

pgBackRestクライアントとサーバー間のすべてのTLS接続は暗号化されます。デフォルトでは、オブジェクトストア（例：S3）への接続も暗号化されます。

注記：

どのトランスポート接続でも、セキュリティーの最低要件はTLSv1.2です。

必要に応じて、受け入れる暗号スイートを調整できます。特別なセキュリティー要件がなければ、例に示す値が妥当な選択です。未設定（デフォルト）の場合は、使用するOpenSSLライブラリのデフォルトが適用されます。

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### TLSv1.3暗号スイートオプション（`--tls-cipher-13`） {#tlsv13-cipher-suites-option---tls-cipher-13}

許可するTLSv1.3暗号スイートです。

pgBackRestクライアントとサーバー間のすべてのTLS接続は暗号化されます。デフォルトでは、オブジェクトストア（例：S3）への接続も暗号化されます。

注記：

どのトランスポート接続でも、セキュリティーの最低要件はTLSv1.2です。

必要に応じて、受け入れる暗号スイートを調整できます。未設定（デフォルト）の場合は、使用するOpenSSLライブラリのデフォルトが適用されます。

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## ログオプション {#log-options}

`log`セクションでは、ログに関する設定を定義します。

注意：

traceレベルのログには、キーやパスワードなどの機密情報が露出する可能性があります。慎重に使用してください！

### コンソールログレベルオプション（`--log-level-console`） {#console-log-level-option---log-level-console}

コンソールに出力するログのレベルです。

次のログレベルをサポートします。

- `off` - ログを一切記録しません（非推奨）
- `error` - エラーのみを記録します
- `warn` - 警告とエラーを記録します
- `info` - 情報、警告、エラーを記録します
- `detail` - 詳細、情報、警告、エラーを記録します
- `debug` - デバッグ、詳細、情報、警告、エラーを記録します
- `trace` - トレース（非常に詳細なデバッグ）、デバッグ、情報、警告、エラーを記録します

```text
default: warn
example: log-level-console=error
```

### ファイルログレベルオプション（`--log-level-file`） {#file-log-level-option---log-level-file}

ファイルに記録するログのレベルです。

次のログレベルをサポートします。

- `off` - ログを一切記録しません（非推奨）
- `error` - エラーのみを記録します
- `warn` - 警告とエラーを記録します
- `info` - 情報、警告、エラーを記録します
- `detail` - 詳細、情報、警告、エラーを記録します
- `debug` - デバッグ、詳細、情報、警告、エラーを記録します
- `trace` - トレース（非常に詳細なデバッグ）、デバッグ、情報、警告、エラーを記録します

```text
default: info
example: log-level-file=debug
```

### 標準エラーログレベルオプション（`--log-level-stderr`） {#std-error-log-level-option---log-level-stderr}

stderrに出力するログのレベルです。

`stdout`（`log-level-console`で指定）の代わりに`stderr`へ出力するログレベルを指定します。`stderr`にはタイムスタンプとプロセスを出力しません。

次のログレベルをサポートします。

- `off` - ログを一切記録しません（非推奨）
- `error` - エラーのみを記録します
- `warn` - 警告とエラーを記録します
- `info` - 情報、警告、エラーを記録します
- `detail` - 詳細、情報、警告、エラーを記録します
- `debug` - デバッグ、詳細、情報、警告、エラーを記録します
- `trace` - トレース（非常に詳細なデバッグ）、デバッグ、情報、警告、エラーを記録します

```text
default: off
example: log-level-stderr=error
```

### ログパスオプション（`--log-path`） {#log-path-option---log-path}

ログファイルを保存するパスです。

ログパスは、pgBackRestがログファイルを保存する場所です。`log-level-file=off`の場合、ログパスは不要です。

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### サブプロセスログオプション（`--log-subprocess`） {#log-subprocesses-option---log-subprocess}

サブプロセスでのログ記録を有効にします。

このプロセスが作成するすべてのサブプロセスで、`log-level-file`で指定したログレベルによるファイルへのログ記録を有効にします。

```text
default: n
example: log-subprocess=y
```

### ログタイムスタンプオプション（`--log-timestamp`） {#log-timestamp-option---log-timestamp}

ログのタイムスタンプを有効にします。

コンソールとファイルのログでタイムスタンプを有効にします。このオプションは、ドキュメント生成などの特殊な状況では無効にします。

```text
default: y
example: log-timestamp=n
```

--------

## メンテナー向けオプション {#maintainer-options}

メンテナー向けオプションは、PostgreSQLのフォークをサポートするためのものです。適切な設定はフォークのメンテナーが決定し、そのフォークのユーザーに伝えることを推奨します。

警告：

これらのオプションを不適切に使用すると、予期しない動作やデータ破損を引き起こす可能性があります。

必要なオプションを指定してpgBackRestをテストする責任は、フォークのメンテナーにあります。pgBackRestは、いかなるフォークとの互換性も保証しません。

### WALヘッダー確認オプション（`--archive-header-check`） {#check-wal-headers-option---archive-header-check}

WALヘッダー内のPostgreSQLバージョン/識別子を確認します。

このオプションはデフォルトで有効で、WALヘッダーをPostgreSQLのバージョンおよびシステム識別子と照合し、WALが正しいstanzaにコピーされることを確認します。これは、`pg_control`とstanzaの照合、およびWALのコピー元が`pg_control`の存在するPostgreSQLデータディレクトリと同じであることの確認に加えて実行されます。

したがって、この確認の無効化は比較的安全ですが、WALが暗号化されている場合など、必要な場合に限って行ってください。

```text
default: y
example: archive-header-check=n
```

### ページヘッダー確認オプション（`--page-header-check`） {#page-header-check-option---page-header-check}

PostgreSQLのページヘッダーを確認します。

このオプションはデフォルトで有効で、ページヘッダーの確認を追加します。

ページが暗号化されている場合など、必要な場合を除き、このオプションの無効化は避けてください。

```text
default: y
example: page-header-check=n
```

### PostgreSQLバージョン強制指定オプション（`--pg-version-force`） {#force-postgresql-version-option---pg-version-force}

PostgreSQLのバージョンを強制指定します。

`pg_control`またはWALヘッダーを読み取って自動検出したバージョンの代わりに、指定したPostgreSQLバージョンを使用します。これは主に、これらの値がリリース版とは異なるPostgreSQLのフォークや開発版で役立ちます。PostgreSQLが`server_version_num`で報告するバージョンは、強制指定したバージョンと一致する必要があります。

警告：

このオプションは慎重に使用してください。`pg_control`とWALヘッダーは引き続き、指定バージョンで想定される形式、つまり公式のオープンソース版PostgreSQLの形式で読み取られます。フォークや開発版が、pgBackRestの依存するフィールドの形式を変更していると、予期しない動作が生じます。一般に、このオプションが想定どおりに動作するのは、フォークが独自の構造体メンバーをすべて標準のPostgreSQLメンバーの*後ろ*に追加している場合に限られます。

```text
example: pg-version-force=15
```

--------

## リポジトリオプション {#repository-options}

`repository`セクションでは、リポジトリを設定するためのオプションを定義します。

**インデックス**：複数のリポジトリを設定できるように、すべての`repo-`オプションにはインデックスが付きます。たとえば、1つのリポジトリは`repo1-path`、`repo1-host`などのオプションで設定します。複数のリポジトリが設定されていて、コマンドに`--repo`オプションを指定しない場合、リポジトリは優先度の高い順（例：repo1、次にrepo2）に処理されます。

`repo-retention-*`オプションは、バックアップの保持期間を定義します。期限切れ処理は、完了したバックアップ数が保持上限を超えた場合にのみ行われます。つまり、`repo1-retention-full-type`を`count`（デフォルト）に、`repo1-retention-full`を2に設定した場合、最も古いバックアップが期限切れになるには、完了したバックアップが3つ必要です。`repo1-retention-full-type`を`time`に設定した場合、`repo1-retention-full`は日数を表すため、期限切れ処理が行われるには、少なくともその日数分のフルバックアップが必要です。常に保持数+1個のバックアップに十分な容量を確保してください。

### Azureリポジトリアカウントオプション（`--repo-azure-account`） {#azure-repository-account-option---repo-azure-account}

Azureリポジトリのアカウントです。

リポジトリの保存に使用するAzureアカウントです。

```text
example: repo1-azure-account=pg-backup
```

### Azureリポジトリコンテナーオプション（`--repo-azure-container`） {#azure-repository-container-option---repo-azure-container}

Azureリポジトリのコンテナーです。

リポジトリの保存に使用するAzureコンテナーです。

`repo-path=/`を設定するとpgBackRestリポジトリをコンテナーのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのAzureが生成するコンテンツもコンテナーに保存できるようにすることを推奨します。

```text
example: repo1-azure-container=pg-backup
```

### Azureリポジトリエンドポイントオプション（`--repo-azure-endpoint`） {#azure-repository-endpoint-option---repo-azure-endpoint}

Azureリポジトリのエンドポイントです。

Blobサービスへの接続に使用するエンドポイントです。Azure Governmentを使用しない限り、通常はデフォルトで適切です。

独自の構成やテスト構成では、`repo-storage-ca-file`、`repo-storage-ca-path`、`repo-storage-host`、`repo-storage-port`、`repo-storage-verify-tls`の各オプションが役立つ場合があります。

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### Azureリポジトリキーオプション（`--repo-azure-key`） {#azure-repository-key-option---repo-azure-key}

Azureリポジトリのキーです。

`repo-azure-key-type`オプションに応じた共有キーまたは共有アクセス署名です。

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### Azureリポジトリキー種別オプション（`--repo-azure-key-type`） {#azure-repository-key-type-option---repo-azure-key-type}

Azureリポジトリのキー種別です。

次の認証方式をサポートします。

- `shared` - 共有キー
- `sas` - 共有アクセス署名
- `auto` - AzureマネージドIDを使用して自動的に認可

```text
default: shared
example: repo1-azure-key-type=sas
```

### AzureリポジトリURI形式オプション（`--repo-azure-uri-style`） {#azure-repository-uri-style-option---repo-azure-uri-style}

AzureのURI形式です。

次のURI形式をサポートします。

- `host` - `account.endpoint`ホストに接続します。
- `path` - `endpoint`ホストに接続し、URIの先頭にアカウントを付加します。

```text
default: host
example: repo1-azure-uri-style=path
```

### ブロック増分バックアップオプション（`--repo-block`） {#block-incremental-backup-option---repo-block}

ブロック増分バックアップを有効にします。

ブロック増分バックアップは、ファイルを個別にバックアップ可能なブロックに分割することで、より細かな単位でのバックアップを可能にします。リポジトリの容量を節約し、リポジトリからファイル全体を読み取らずに個々のブロックを取得できるため、差分リストアのパフォーマンスが向上する可能性があります。

注記：

`repo-block`を有効にする前に、`repo-bundle`オプションを有効にする必要があります。

ファイルのブロックサイズは、ファイルのサイズと古さに基づいて決まります。一般に、古いファイルや大きいファイルには、より大きなブロックサイズが使われます。ファイルが十分に古い場合は、ブロック増分バックアップの対象になりません。

ブロック増分バックアップは、フルバックアップを含むすべてのバックアップ種類で有効にすると最も効率的です。フルバックアップは少し大きくなりますが、後続の差分バックアップと増分バックアップは、フルバックアップが生成したブロックマップを使用して容量を節約できます。

```text
default: n
example: repo1-block=y
```

### リポジトリバンドルオプション（`--repo-bundle`） {#repository-bundles-option---repo-bundle}

リポジトリ内でファイルをまとめます。

小さいファイルをバンドル（結合）し、リポジトリに書き込むファイルの総数を減らします。ファイル数を減らすと、一般に書き込みが効率化され、S3などのオブジェクトストアで特に効果があります。また、長さ0のファイルはマニフェスト以外には保存しないため、時間と容量を節約できます。

```text
default: n
example: repo1-bundle=y
```

### リポジトリバンドル対象サイズ上限オプション（`--repo-bundle-limit`） {#repository-bundle-limit-option---repo-bundle-limit}

ファイルをバンドルする際のサイズ上限です。

バンドルに含めるファイルのサイズ上限です。このサイズより大きいファイルは個別に保存します。

バンドルされたファイルはバックアップの再開時に再利用できないため、このオプションは再開可能なファイルを制御します。つまり、値を大きくすると再開可能なファイルが少なくなります。

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### リポジトリバンドルサイズオプション（`--repo-bundle-size`） {#repository-bundle-size-option---repo-bundle-size}

ファイルバンドルの目標サイズです。

1つのバンドルに追加するファイルの目標サイズを定義します。非圧縮のバンドルサイズは最大で`repo-bundle-size`+`repo-bundle-limit`になるため、このオプションにファイルシステムの最大許容サイズを設定しないでください。

再試行時にはバンドル全体を処理し直す必要があるため、一般に、このオプションを大きくしすぎるのは適切ではありません。

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### リポジトリ暗号化パスフレーズオプション（`--repo-cipher-pass`） {#repository-cipher-passphrase-option---repo-cipher-pass}

リポジトリの暗号化パスフレーズです。

リポジトリ内のファイルの暗号化/復号に使用するパスフレーズです。

注記：

`stanza`オプションなしで実行した場合、`info`コマンドは`global`セクションからのみ暗号化設定を読み取ります。暗号化設定をstanzaごとに設定している場合は、暗号化されたstanzaを読み取るために、`stanza`オプションを指定して`info`コマンドを実行してください。

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### リポジトリ暗号方式オプション（`--repo-cipher-type`） {#repository-cipher-type-option---repo-cipher-type}

リポジトリの暗号化に使用する暗号方式です。

次の暗号方式をサポートします。

- `none` - リポジトリを暗号化しません
- `aes-256-cbc` - 鍵長256ビットのAdvanced Encryption Standard

リポジトリの種類（例：S3）が暗号化をサポートしていても、暗号化は常にクライアント側で実行されます。

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### GCSリポジトリバケットオプション（`--repo-gcs-bucket`） {#gcs-repository-bucket-option---repo-gcs-bucket}

GCSリポジトリのバケットです。

リポジトリの保存に使用するGCSバケットです。

`repo-path=/`を設定するとpgBackRestリポジトリをバケットのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのGCSが生成するコンテンツもバケットに保存できるようにすることを推奨します。

```text
example: repo1-gcs-bucket=/pg-backup
```

### GCSリポジトリエンドポイントオプション（`--repo-gcs-endpoint`） {#gcs-repository-endpoint-option---repo-gcs-endpoint}

GCSリポジトリのエンドポイントです。

ストレージサービスへの接続に使用するエンドポイントです。ローカルのGCSサーバーや別のエンドポイントを使用するように変更できます。

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### GCSリポジトリキーオプション（`--repo-gcs-key`） {#gcs-repository-key-option---repo-gcs-key}

GCSリポジトリのキーです。

`repo-gcs-key-type`オプションに応じたトークン、サービスキーファイル、または外部アカウントの認証情報ファイルです。

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### GCSリポジトリキー種別オプション（`--repo-gcs-key-type`） {#gcs-repository-key-type-option---repo-gcs-key-type}

GCSリポジトリのキー種別です。

次の認証方式をサポートします。

- `auto` - インスタンスのサービスアカウントを使用して認証します。
- `service` - ローカルに保存したキーでサービスアカウントを使用します。
- `token` - `fakegcs`などを使用するローカルテスト用です。
- `web-id` - Workload Identity Federationを使用して認証します。

`repo-gcs-key-type=service`の場合、認証トークンの更新時に認証情報を再読み込みします。

`repo-gcs-key-type=web-id`の場合、`repo-gcs-key`には外部アカウントの認証情報ファイルを指定する必要があります。認証トークンの更新時にWebアイデンティティトークンが再読み込みされます。

`service_account_impersonation_url`はサポートしません。`credential_source.file`のみをサポートし、`credential_source.format`を指定する場合、型は`text`である必要があります。

```text
default: service
example: repo1-gcs-key-type=auto
```

### GCSリポジトリプロジェクトIDオプション（`--repo-gcs-user-project`） {#gcs-repository-project-id-option---repo-gcs-user-project}

GCSのプロジェクトIDです。

リクエストの課金先を決定するために使用するGCSプロジェクトIDです。

```text
example: repo1-gcs-user-project=my-project
```

### リポジトリハードリンクオプション（`--repo-hardlink`） {#repository-hardlink-option---repo-hardlink}

リポジトリ内のバックアップ間でファイルをハードリンクします。

差分バックアップと増分バックアップのファイルを、それらのフルバックアップにハードリンクすることを有効にします。これにより、ファイルシステム上では各バックアップがフルバックアップであるように見えます。ただし、ハードリンクされたファイルを変更すると、セット内のすべてのバックアップに影響する可能性があるため、注意してください。

```text
default: n
example: repo1-hardlink=y
```

非推奨の名前：hardlink

### リポジトリホストオプション（`--repo-host`） {#repository-host-option---repo-host}

リモート操作時のリポジトリホストです。

ローカルにマウントされたファイルシステムにバックアップおよびアーカイブする場合、この設定は不要です。

```text
example: repo1-host=repo1.domain.com
```

非推奨の名前：backup-host

### リポジトリホスト認証局ファイルオプション（`--repo-host-ca-file`） {#repository-host-certificate-authority-file-option---repo-host-ca-file}

リポジトリホストの認証局ファイルです。

リポジトリホストへの接続に、システムのデフォルト以外のCAファイルを使用します。

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### リポジトリホスト認証局パスオプション（`--repo-host-ca-path`） {#repository-host-certificate-authority-path-option---repo-host-ca-path}

リポジトリホストの認証局パスです。

リポジトリホストへの接続に、システムのデフォルト以外のCAパスを使用します。

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### リポジトリホスト証明書ファイルオプション（`--repo-host-cert-file`） {#repository-host-certificate-file-option---repo-host-cert-file}

リポジトリホストの証明書ファイルです。

クライアントの身元を証明するためにリポジトリホストに送信します。

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### リポジトリホストコマンドオプション（`--repo-host-cmd`） {#repository-host-command-option---repo-host-cmd}

リポジトリホストのpgBackRestコマンドです。

pgBackRestコマンドのパスがローカルホストとリポジトリホストで異なる場合にのみ必要です。未定義の場合、リポジトリホストのコマンドにはローカルと同じコマンドを設定します。

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

非推奨の名前：backup-cmd

### リポジトリホスト設定オプション（`--repo-host-config`） {#repository-host-configuration-option---repo-host-config}

pgBackRestリポジトリホストの設定ファイルです。

リポジトリホスト上の設定ファイルの場所を設定します。リポジトリホストの設定ファイルがローカルの設定ファイルと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

非推奨の名前：backup-config

### リポジトリホスト追加設定パスオプション（`--repo-host-config-include-path`） {#repository-host-configuration-include-path-option---repo-host-config-include-path}

pgBackRestリポジトリホストの追加設定パスです。

リポジトリホスト上の追加設定パスの場所を設定します。リポジトリホストの追加設定パスがローカルの追加設定パスと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### リポジトリホスト設定パスオプション（`--repo-host-config-path`） {#repository-host-configuration-path-option---repo-host-config-path}

pgBackRestリポジトリホストの設定パスです。

リポジトリホスト上の設定パスの場所を設定します。リポジトリホストの設定パスがローカルの設定パスと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### リポジトリホストキーファイルオプション（`--repo-host-key-file`） {#repository-host-key-file-option---repo-host-key-file}

リポジトリホストのキーファイルです。

クライアント証明書が所有者によって送信されたことを証明します。

```text
example: repo1-host-key-file=/path/to/client.key
```

### リポジトリホストポートオプション（`--repo-host-port`） {#repository-host-port-option---repo-host-port}

`repo-host`が設定されている場合のリポジトリホストのポートです。

リポジトリホストのプロトコルにデフォルト以外のポートを指定するには、このオプションを使用します。

注記：

`repo-host-type=ssh`の場合、`repo-host-port`にデフォルト値はありません。この場合、ポートは`cmd-ssh`で指定したコマンドの設定に従います。

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

非推奨の名前：backup-ssh-port

### リポジトリホストプロトコル種別オプション（`--repo-host-type`） {#repository-host-protocol-type-option---repo-host-type}

リポジトリホストのプロトコル種別です。

次のプロトコル種別をサポートします。

- `ssh` - Secure Shell。
- `tls` - pgBackRest TLSサーバー。

```text
default: ssh
example: repo1-host-type=tls
```

### リポジトリホストユーザーオプション（`--repo-host-user`） {#repository-host-user-option---repo-host-user}

`repo-host`が設定されている場合のリポジトリホストのユーザーです。

リポジトリホスト上の操作に使用するユーザーを定義します。`postgres`ユーザーではなく、`pgbackrest`などの別のユーザーを使用することを推奨します。リポジトリホストでPostgreSQLを実行する場合は、`postgres`ユーザーを`pgbackrest`グループに追加することで、リポジトリの内容を誤って破損させずに読み取り権限を与えられます。

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

非推奨の名前：backup-user

### リポジトリパスオプション（`--repo-path`） {#repository-path-option---repo-path}

バックアップとアーカイブを保存するパスです。

リポジトリは、pgBackRestがバックアップを保存し、WALセグメントをアーカイブする場所です。

必要な容量を事前に見積もるのは難しい場合があります。まずいくつかバックアップを取得し、各種類（full/incr/diff）のバックアップサイズを記録して、1日当たりに生成されるWALの量を測定するのが最善です。これにより、必要な容量のおおよその見当が付きます。ただし、データベースの変化に伴い、必要量も時間とともに変わる可能性があります。

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### アーカイブ保持オプション（`--repo-retention-archive`） {#archive-retention-option---repo-retention-archive}

連続したWALを何回分のバックアップに相当する期間保持するかを指定します。

注記：

バックアップの一貫性を確保するために必要なWALセグメントは、このオプションの設定にかかわらず、そのバックアップが期限切れになるまで常に保持されます。

この値が未設定で、`repo-retention-full-type`が`count`（デフォルト）の場合、期限切れ処理の対象アーカイブを決める値は、`repo-retention-archive-type`が`full`（または`diff`）なら、それに対応する`repo-retention-full`（または`repo-retention-diff`）の値がデフォルトになります。これにより、すでに期限切れになったバックアップのWALだけが期限切れになります。`repo-retention-full-type`が`time`の場合は、`repo-retention-full`の設定を満たして保持された最も古いフルバックアップより前のアーカイブを削除することがデフォルトになります。

`repo-retention-archive-type`を`incr`に設定した場合は、このオプションを設定する必要があります。ディスク容量に余裕がない場合は、この設定を`repo-retention-archive-type`と組み合わせ、WALセグメントを積極的に期限切れにできます。ただし、WALが期限切れになったバックアップからPITRを実行できなくなるため、**推奨しません**。

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

非推奨の名前：retention-archive

### アーカイブ保持種別オプション（`--repo-retention-archive-type`） {#archive-retention-type-option---repo-retention-archive-type}

WALの保持に使用するバックアップの種類です。

次のバックアップ種別をサポートします。

- `full` - pgBackRestは`repo-retention-archive`で定義した数のフルバックアップに対応するアーカイブログを保持します。
- `diff` - （差分）`repo-retention-archive`で定義した数のフルバックアップと差分バックアップに対応するアーカイブログを保持します。つまり、最後に取得したバックアップがフルバックアップであれば、repo-retentionの計算では差分バックアップとして数えます。
- `incr` - （増分）`repo-retention-archive`で定義した数のフルバックアップ、差分バックアップ、増分バックアップに対応するアーカイブログを保持します。

この設定はデフォルトから変更しないことを推奨します。デフォルトでは、フルバックアップの期限切れに伴ってのみWALを期限切れにします。

```text
default: full
example: repo1-retention-archive-type=diff
```

非推奨の名前：retention-archive-type

### 差分バックアップ保持オプション（`--repo-retention-diff`） {#differential-retention-option---repo-retention-diff}

保持する差分バックアップの数です。

差分バックアップが期限切れになると、それに関連するすべての増分バックアップも期限切れになります。未定義の場合は、依存するフルバックアップが期限切れになるまで、すべての差分バックアップを保持します。

期限切れ処理では、フルバックアップも差分バックアップの数に含まれます。このため、ほとんどの場合、保持が必要な差分バックアップの数はわずかに少なくなります。

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

非推奨の名前：retention-diff

### フルバックアップ保持オプション（`--repo-retention-full`） {#full-retention-option---repo-retention-full}

フルバックアップの保持数/保持期間です。

フルバックアップが期限切れになると、それに関連するすべての差分バックアップと増分バックアップも期限切れになります。このオプションが未定義の場合は警告を出力します。無期限の保持が必要な場合は、最大値を設定してください。

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

非推奨の名前：retention-full

### フルバックアップ保持種別オプション（`--repo-retention-full-type`） {#full-retention-type-option---repo-retention-full-type}

フルバックアップの保持種別です。

`repo-retention-full`設定が、保持する期間（日数）とフルバックアップの数のどちらを表すかを決定します。

次の保持種別をサポートします。

- `time` - `repo-retention-full`以上の日数が経過したバックアップが少なくともほかに1つ存在する場合に、`repo-retention-full`より古いフルバックアップをリポジトリから削除します。たとえば、`repo-retention-full`が30（日）で、25日前と35日前の2つのフルバックアップがある場合、どちらも期限切れにはなりません。35日前のバックアップを期限切れにすると25日前のバックアップだけが残り、古いバックアップを期限切れにする前に少なくとも30日前のバックアップを1つ確保するという30日間の保持ポリシーに違反するためです。`repo-retention-archive-type`と`repo-retention-archive`を明示的に設定していない限り、残っている最も古いフルバックアップより前のアーカイブ済みWALは自動的に期限切れになります。
- `count` - `repo-retention-full`を超えるフルバックアップを期限切れにします。たとえば、`repo-retention-full`が`4`で、5つ目のフルバックアップが完了すると、数を4に保つために最も古いフルバックアップを期限切れにします。

保持の計算に含めるには、バックアップが正常に完了している必要があります。たとえば、`repo-retention-full-type`が`count`で、`repo-retention-full`が`2`の場合、最も古いバックアップを期限切れにするには、完了したフルバックアップが3つ必要です。

```text
default: count
example: repo1-retention-full-type=time
```

### バックアップ履歴保持オプション（`--repo-retention-history`） {#backup-history-retention-option---repo-retention-history}

バックアップ履歴マニフェストを保持する日数です。

バックアップが完了すると、バックアップマニフェストのコピーを`backup.history`パスに保存します。これらのファイルは、バックアップやWALの増加量を経時的に測定するなどのデータ分析に役立つため、デフォルトでは期限切れになりません。

バックアップ履歴マニフェストを保持する日数を定義するには、`repo-retention-history`を設定します。期限切れになっていないバックアップは、常にバックアップ履歴に保持されます。期限切れになっていないバックアップの履歴だけを保持するには、`repo-retention-history=0`を指定します。

フルバックアップの履歴マニフェストが期限切れになると、そのフルバックアップに関連するすべての差分バックアップと増分バックアップの履歴マニフェストも期限切れになります。

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### S3リポジトリバケットオプション（`--repo-s3-bucket`） {#s3-repository-bucket-option---repo-s3-bucket}

S3リポジトリのバケットです。

リポジトリの保存に使用するS3バケットです。

`repo-path=/`を設定するとpgBackRestリポジトリをバケットのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのAWSが生成するコンテンツもバケットに保存できるようにすることを推奨します。

```text
example: repo1-s3-bucket=pg-backup
```

### S3リポジトリエンドポイントオプション（`--repo-s3-endpoint`） {#s3-repository-endpoint-option---repo-s3-endpoint}

S3リポジトリのエンドポイントです。

選択したリージョンに対して有効なAWSエンドポイントを使用してください。

独自の構成やテスト構成では、`repo-storage-ca-file`、`repo-storage-ca-path`、`repo-storage-host`、`repo-storage-port`、`repo-storage-verify-tls`の各オプションが役立つ場合があります。

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### S3リポジトリアクセスキーオプション（`--repo-s3-key`） {#s3-repository-access-key-option---repo-s3-key}

S3リポジトリのアクセスキーです。

このバケットへのアクセスに使用するAWSキーです。

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### S3リポジトリシークレットアクセスキーオプション（`--repo-s3-key-secret`） {#s3-repository-secret-access-key-option---repo-s3-key-secret}

S3リポジトリのシークレットアクセスキーです。

このバケットへのアクセスに使用するAWSシークレットキーです。

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### S3リポジトリキー種別オプション（`--repo-s3-key-type`） {#s3-repository-key-type-option---repo-s3-key-type}

S3リポジトリのキー種別です。

次の認証方式をサポートします。

- `shared` - 共有キー
- `auto` - 一時認証情報を自動取得
- `web-id` - ウェブID認証情報を自動取得
- `pod-id` - EKS Pod Identityの認証情報を自動取得
- `process` - プロセスを実行して認証情報を取得

```text
default: shared
example: repo1-s3-key-type=auto
```

### S3リポジトリKMSキーIDオプション（`--repo-s3-kms-key-id`） {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

S3リポジトリのKMSキーです。

指定したAWS Key Management Serviceのキーを使用して、S3のサーバー側暗号化を有効にします。

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3認証プロセスコマンドオプション（`--repo-s3-process-cmd`） {#s3-authentication-process-command-option---repo-s3-process-cmd}

S3の認証プロセスコマンドです。

一時的なS3認証情報を取得するために実行するコマンド（および任意の引数）です。リストの最初の要素がコマンドで、残りの要素はパラメーターとして渡します。

プロセスは、`AccessKeyId`、`SecretAccessKey`、`SessionToken`、`Expiration`フィールドを含むJSONを出力する必要があります。認証情報は有効期限の前に自動更新されます。形式の詳細は、[プロセス認証情報プロバイダー](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output)を参照してください。

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### S3リポジトリリージョンオプション（`--repo-s3-region`） {#s3-repository-region-option---repo-s3-region}

S3リポジトリのリージョンです。

バケットを作成したAWSリージョンです。

```text
example: repo1-s3-region=us-east-1
```

### S3リポジトリのリクエスタ支払いオプション（`--repo-s3-requester-pays`） {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

S3リポジトリのリクエスタ支払いです。

S3のリクエスタ支払いを有効にします。

```text
default: n
example: repo1-s3-requester-pays=n
```

### S3リポジトリロールオプション（`--repo-s3-role`） {#s3-repository-role-option---repo-s3-role}

S3リポジトリのロールです。

`repo-s3-key-type=auto`の場合に、一時認証情報の取得に使用するAWSロール名（完全なARNではありません）です。

```text
example: repo1-s3-role=authrole
```

### S3リポジトリサービスオプション（`--repo-s3-service`） {#s3-repository-service-option---repo-s3-service}

S3の署名サービスです。

SigV4認証で使用するS3署名サービスです。標準のS3エンドポイントでは、デフォルトは`s3`です。S3 Outpostsエンドポイントを使用する場合は、`s3-outposts`に設定します。

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### S3リポジトリSSEカスタマーキーオプション（`--repo-s3-sse-customer-key`） {#s3-repository-sse-customer-key-option---repo-s3-sse-customer-key}

S3リポジトリのSSEカスタマーキーです。

指定したカスタマーキーを使用して、S3のサーバー側暗号化を有効にします。

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3リポジトリSTSエンドポイントオプション（`--repo-s3-sts-host`） {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

S3リポジトリのSTSエンドポイントです。

`repo-s3-key-type=web-id`を設定した場合に、一時認証情報の取得に使用するSTSエンドポイントです。リージョン別STSを使用するには、リージョン別エンドポイント（例：`sts.us-east-1.amazonaws.com`）を設定します。GovCloudや中国リージョンで必要になる場合や、レイテンシーを低減するために使用する場合があります。

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### S3リポジトリセキュリティートークンオプション（`--repo-s3-token`） {#s3-repository-security-token-option---repo-s3-token}

S3リポジトリのセキュリティートークンです。

一時認証情報とともに使用するAWSセキュリティートークンです。

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### S3リポジトリURI形式オプション（`--repo-s3-uri-style`） {#s3-repository-uri-style-option---repo-s3-uri-style}

S3のURI形式です。

次のURI形式をサポートします。

- `host` - `bucket.endpoint`ホストに接続します。
- `path` - `endpoint`ホストに接続し、URIの先頭にバケットを付加します。

```text
default: host
example: repo1-s3-uri-style=path
```

### SFTPリポジトリホストオプション（`--repo-sftp-host`） {#sftp-repository-host-option---repo-sftp-host}

SFTPリポジトリのホストです。

リポジトリが存在するSFTPホストです。

```text
example: repo1-sftp-host=sftprepo.domain
```

### SFTPリポジトリホストフィンガープリントオプション（`--repo-sftp-host-fingerprint`） {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

SFTPリポジトリホストのフィンガープリントです。

SFTPリポジトリホストのフィンガープリントの生成方法は、`repo-sftp-host-key-hash-type`と一致させてください。`awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`でフィンガープリントを生成します。sshホストキーは通常、`/etc/ssh`ディレクトリにあります。

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### SFTPホストキー確認方式オプション（`--repo-sftp-host-key-check-type`） {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

SFTPのホストキー確認方式です。

次のSFTPホストキー確認方式をサポートします。

- `strict` - pgBackRestは~/.ssh/known_hostsファイルにホストキーを自動追加せず、ホストキーが変更されたホスト、または既知のホストファイルで見つからないホストへの接続を拒否します。このオプションでは、新しいホストをすべて手動で追加する必要があります。
- `accept-new` - pgBackRestは新しいホストキーをユーザーの既知のホストファイルに自動追加しますが、ホストキーが変更されたホストへの接続は許可しません。
- `fingerprint` - pgBackRestは、`repo-sftp-host-fingerprint`オプションで指定したフィンガープリントとホストキーを照合します。
- `none` - ホストキーを確認しません。

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### SFTPリポジトリホストキーハッシュ種別オプション（`--repo-sftp-host-key-hash-type`） {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

SFTPリポジトリのホストキーハッシュ種別です。

SSHの開始時に、リモートシステムのホストキーのダイジェスト計算に使用するハッシュ種別を指定します。指定可能な値は`md5`、`sha1`、`sha256`ですが、`sha256`は新しいバージョンの`libssh2`でのみサポートされます。

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### SFTPリポジトリホストポートオプション（`--repo-sftp-host-port`） {#sftp-repository-host-port-option---repo-sftp-host-port}

SFTPリポジトリホストのポートです。

SFTPリポジトリホストのポートです。

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### SFTPリポジトリホストユーザーオプション（`--repo-sftp-host-user`） {#sftp-repository-host-user-option---repo-sftp-host-user}

SFTPリポジトリホストのユーザーです。

リポジトリの保存に使用するホスト上のユーザーです。

```text
example: repo1-sftp-host-user=pg-backup
```

### SFTP既知ホストファイルオプション（`--repo-sftp-known-host`） {#sftp-known-hosts-file-option---repo-sftp-known-host}

SFTPの既知のホストファイルです。

認証時に一致するSFTPホストを探す既知のホストファイルです。未指定の場合、pgBackRestはデフォルトで`~/.ssh/known_hosts`、`~/.ssh/known_hosts2`、`/etc/ssh/ssh_known_hosts`、`/etc/ssh/ssh_known_hosts2`を検索します。1つ以上のファイルパスを設定した場合は、それらを検索して一致を確認します。ファイルパスは絶対パス、または先頭がチルダのパスである必要があります。`repo-sftp-known-host`オプションを複数回指定することで、検索する既知のホストファイルを複数指定できます。既知のホストファイルによる確認を使用するには、`repo-sftp-host-fingerprint`を指定してはいけません。`repo-sftp-host-check-type`オプションも参照してください。

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### SFTPリポジトリ秘密鍵ファイルオプション（`--repo-sftp-private-key-file`） {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

SFTPの秘密鍵ファイルです。

認証に使用するSFTP秘密鍵ファイルです。

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### SFTPリポジトリ秘密鍵パスフレーズオプション（`--repo-sftp-private-key-passphrase`） {#sftp-repository-private-key-passphrase-option---repo-sftp-private-key-passphrase}

SFTP秘密鍵のパスフレーズです。

秘密鍵へのアクセスに使用するパスフレーズです。SSHの公開鍵/秘密鍵ペアを作成する際の任意の機能です。

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### SFTPリポジトリ公開鍵ファイルオプション（`--repo-sftp-public-key-file`） {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

SFTPの公開鍵ファイルです。

認証に使用するSFTP公開鍵ファイルです。OpenSSLに対してコンパイルした場合は任意ですが、別のライブラリに対してコンパイルした場合は必須です。

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### リポジトリストレージCAファイルオプション（`--repo-storage-ca-file`） {#repository-storage-ca-file-option---repo-storage-ca-file}

リポジトリストレージのCAファイルです。

ストレージ（例：S3、Azure）の証明書に、システムのデフォルト以外のCAファイルを使用します。

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

非推奨の名前：repo-azure-ca-file, repo-s3-ca-file

### リポジトリストレージTLS CAパスオプション（`--repo-storage-ca-path`） {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

リポジトリストレージのCAパスです。

ストレージ（例：S3、Azure）の証明書に、システムのデフォルト以外のCAパスを使用します。

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

非推奨の名前：repo-azure-ca-path, repo-s3-ca-path

### リポジトリストレージホストオプション（`--repo-storage-host`） {#repository-storage-host-option---repo-storage-host}

リポジトリストレージのホストです。

ストレージ（例：S3、Azure）のエンドポイントとは異なるホストに接続します。通常はテストに使用します。

```text
example: repo1-storage-host=127.0.0.1
```

非推奨の名前：repo-azure-host, repo-s3-host

### リポジトリストレージポートオプション（`--repo-storage-port`） {#repository-storage-port-option---repo-storage-port}

リポジトリストレージのポートです。

ストレージ（例：S3、Azure）のエンドポイント（ホストを指定した場合はそのホスト）への接続に使用するポートです。

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

非推奨の名前：repo-azure-port, repo-s3-port

### リポジトリストレージのプリフェッチオプション（`--repo-storage-prefetch`） {#repository-storage-prefetch-option---repo-storage-prefetch}

リポジトリストレージのプリフェッチです。

S3などのオブジェクトストアから読み取る際に、先行して発行するリクエスト数を指定します。真の並行処理ではありませんが、リクエストの送信に伴う遅延を減らします。

最初の読み取りはプリフェッチできないため、読み取りごとの未完了リクエスト数はプリフェッチ数より1つ多くなります。

```text
default: 3
allowed: [0, 1024]
example: repo1-storage-prefetch=7
```

### リポジトリストレージの読み飛ばしオプション（`--repo-storage-read-over`） {#repository-storage-read-over-option---repo-storage-read-over}

リポジトリストレージの読み飛ばしです。

バンドルには、すでに存在するファイルなど、リストア時に不要なデータが含まれる場合があります。このオプションは、新しい読み取りリクエストをオブジェクトストアに送らず、読み取りを続けて不要なデータを読み飛ばします。新しい読み取りリクエストの遅延は、進行中の読み取りを続ける場合より大きいため、通常はこちらの方が高速です。ほとんどのストレージクラスで費用も抑えられます。

```text
default: 64KiB
allowed: [0B, 1MiB]
example: repo1-storage-read-over=128KiB
```

### リポジトリストレージタグオプション（`--repo-storage-tag`） {#repository-storage-tag-option---repo-storage-tag}

リポジトリストレージのタグです。

リポジトリがオブジェクトストア（例：S3）の場合に、オブジェクトに付加するタグを指定します。このオプションを繰り返して、複数のタグを追加できます。

pgBackRestにはこれらのタグを変更する機能がないため、リポジトリ全体でタグを統一するには、`stanza-create`を実行する前に正しく設定してください。

```text
example: repo1-storage-tag=key1=value1
```

### リポジトリストレージアップロードチャンクサイズオプション（`--repo-storage-upload-chunk-size`） {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

リポジトリストレージのアップロードチャンクサイズです。

S3などのオブジェクトストアでは、ファイルが大きすぎてメモリに格納できない場合に、チャンクに分けてアップロードできます。ファイルをメモリに格納できる場合でも、アップロードに使用するメモリ量を制限する方がメモリ効率は高くなります。

チャンクサイズを大きくすると、アップロードリクエストを最小限に抑え、チャンク分割せずに1回のリクエストでアップロードできるファイルが増えるため、一般にパフォーマンスが向上します。一方、メモリ使用量は増加します。チャンクバッファーはプロセスごとに割り当てる必要があるため、`process-max`の値が大きいほど、全体のメモリ消費量も増えます。

有効なチャンクサイズは、ストレージの種類やプラットフォームによって異なります。たとえば、AWS S3の最小チャンクサイズは5MiBです。チャンクサイズの呼び方もストレージの種類によって異なるため、最小値/最大値を調べる際は、AWS S3では「part size」、GCSでは「chunk size」、Azureでは「block size」を使用してください。

ファイルが1GiB（PostgreSQLがデフォルトで作成する最大サイズ）より大きい場合、ファイルのアップロードを完了するために、許容される最大値までチャンクサイズを段階的に増やします。

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### リポジトリストレージ証明書検証オプション（`--repo-storage-verify-tls`） {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

リポジトリストレージの証明書を検証します。

このオプションでは、ストレージ（例：S3、Azure）サーバーのTLS証明書の検証を有効/無効にできます。無効化は、テストや自己署名証明書を使用する場合に限ってください。

```text
default: y
example: repo1-storage-verify-tls=n
```

非推奨の名前：repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### リポジトリシンボリックリンクオプション（`--repo-symlink`） {#repository-symlink-option---repo-symlink}

リポジトリ内にシンボリックリンクを作成します。

`latest`とテーブルスペースのシンボリックリンクの作成を有効にします。これらのシンボリックリンクは、スナップショットを使ってリポジトリ内でその場でリカバリーする場合に最も役立ちますが、そのような利用は一般的ではありません。

大多数のユーザーには役立たないと考えられる機能ですが、従来の動作を維持するため、デフォルトで有効になっています。ただし、シンボリックリンクをサポートしないPosixに似たストレージでは、無効にすると役立つ場合があります。

```text
default: y
example: repo1-symlink=n
```

### リポジトリ対象時刻オプション（`--repo-target-time`） {#target-time-for-repository-option---repo-target-time}

リポジトリの対象時刻です。

対象時刻は、コマンドがバージョン管理されたストレージ上のリポジトリを読み取る際の時点を定義します。これにより、ある時点の状態のリポジトリを読み取り、ユーザーの誤操作やマルウェアによって削除または破損したデータをリカバリーできます。

S3、GCS、Azureはストレージのバージョン管理をサポートしますが、通常はデフォルトで有効になっていません。バージョン管理の有効化に加え、S3ではオブジェクトロック、GCSやAzureでは論理削除を有効にすると役立つ場合があります。

`repo-target-time`オプションを指定する場合は、`repo`オプションも指定する必要があります。すべてのリポジトリ種類がバージョン管理をサポートするとは限らず、一般にリカバリーでは単一のリポジトリを対象とするのが妥当です。

ストレージのタイムスタンプとの比較は、指定したタイムスタンプ以下（<=）で行い、タイムスタンプにミリ秒を指定しても切り捨てられます。

```text
example: repo-target-time=2024-08-08 12:12:12+00
```

### リポジトリ種別オプション（`--repo-type`） {#repository-type-option---repo-type}

リポジトリに使用するストレージの種類です。

次のリポジトリ種類をサポートします。

- `azure` - Azure Blob Storage Service
- `cifs` - `posix`と同様ですが、リンクとディレクトリのfsyncを無効にします
- `gcs` - Google Cloud Storage
- `posix` - Posix準拠のファイルシステム
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

NFSマウントを`posix`リポジトリとして使用する場合、PostgreSQLのドキュメントに記載されたものと同じ規則がpgBackRestにも適用されます。[データベースクラスターの作成 - ファイルシステム](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM)を参照してください。

```text
default: posix
example: repo1-type=cifs
```

--------

## リストアオプション {#restore-options}

`restore`セクションでは、バックアップのリストアに使用する設定を定義します。

### アーカイブモードオプション（`--archive-mode`） {#archive-mode-option---archive-mode}

リストアしたクラスターでアーカイブを維持または無効にします。

このオプションでは、リストアしたクラスターのアーカイブを維持または無効にできます。作業のためにクラスターを昇格させる必要があるものの、新しいプライマリーにする意図がない場合に役立ちます。この場合、そのクラスターからWALをリポジトリに送信するのは適切ではありません。

次のモードをサポートします。

- `off` - `archive_mode=off`を設定してアーカイブを無効にします。
- `preserve` - 現在の`archive_mode`設定を維持します。

**注記**：このオプションはPostgreSQL < 12では利用できません。

```text
default: preserve
example: archive-mode=off
```

### データベース除外オプション（`--db-exclude`） {#exclude-database-option---db-exclude}

指定したデータベースを除外してリストアします。

除外したデータベースは、容量を節約しつつPostgreSQLがリカバリーを実行できるように、ゼロで埋めたスパースファイルとしてリストアします。リカバリー後、これらのデータベースにはアクセスできませんが、`drop database`コマンドで削除できます。`--db-exclude`オプションを複数回指定して、除外するデータベースを複数指定できます。

`--db-include`オプションと組み合わせた場合、`--db-exclude`は標準のシステムデータベース（`template0`、`template1`、`postgres`）にのみ適用されます。

```text
example: db-exclude=db_main
```

### 対象データベースオプション（`--db-include`） {#include-database-option---db-include}

指定したデータベースのみをリストアします。

この機能では、選択したデータベースのみをリストアできます。明示的に含めなかったデータベースは、容量を節約しつつPostgreSQLがリカバリーを実行できるように、ゼロで埋めたスパースファイルとしてリストアします。リカバリー後、含めなかったデータベースにはアクセスできませんが、`drop database`コマンドで削除できます。

注記：

組み込みデータベース（`template0`、`template1`、`postgres`）は、明示的に除外しない限り常にリストアします。

`--db-include`オプションを複数回指定して、含めるデータベースを複数指定できます。

詳細と注意事項は、[選択したデータベースのリストア](/ja/pgbackrest/user-guide/#restore-selected-databases)を参照してください。

```text
example: db-include=db_main
```

### 全リンクリストアオプション（`--link-all`） {#link-all-option---link-all}

すべてのシンボリックリンクをリストアします。

デフォルトでは、シンボリックリンクされたディレクトリとファイルは、$PGDATA内の通常のディレクトリとファイルとしてリストアします。元のバックアップを取得したシステムとは異なるシステムで、元のリンク先にシンボリックリンクをリストアするのは安全でない可能性があるためです。このオプションは、バックアップを取得した元のシステムと同じ状態ですべてのシンボリックリンクをリストアします。

```text
default: n
example: link-all=y
```

### リンクマッピングオプション（`--link-map`） {#link-map-option---link-map}

シンボリックリンクのリンク先を変更します。

リストア時に、シンボリックリンクのリンク先ファイルまたはパスを変更できます。バックアップを生成した元のシステムとはストレージ構成が異なるシステムへのリストアに役立ちます。

```text
example: link-map=pg_xlog=/data/xlog
```

### リカバリー設定オプション（`--recovery-option`） {#recovery-option---recovery-option}

`postgresql.auto.conf`または`recovery.conf`のオプションを設定します。

`postgresql.auto.conf`または`recovery.conf`のオプションの詳細は、[サーバーの設定](https://www.postgresql.org/docs/current/runtime-config.html)を参照してください（使用しているPostgreSQLバージョンを必ず選択してください）。このオプションは複数回使用できます。

PostgreSQL >= 12では、オプションを`postgresql.auto.conf`に書き込みます。それ以外のすべてのバージョンでは、`recovery.conf`に書き込みます。

注記：

`restore_command`オプションは自動生成されますが、このオプションで上書きできます。pgBackRestが処理するように設計されているため、独自の`restore_command`を指定する場合は注意してください。リカバリー対象のオプション（recovery_target_name、recovery_target_timeなど）はpgBackRestが自動生成するため、このオプションで設定しないでください。

pgBackRestは`postgresql.auto.conf`または`recovery.conf`ファイルを書き込んだ後にPostgreSQLを起動しないため、手動で再起動する前に、いつでも`postgresql.auto.conf`または`recovery.conf`を編集/確認できます。

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### テーブルスペースマッピングオプション（`--tablespace-map`） {#tablespace-map-option---tablespace-map}

テーブルスペースを指定したディレクトリにリストアします。

リストア時にテーブルスペースを新しい場所に移動します。レプリカ上でテーブルスペースの場所が異なる場合や、アップグレード後のシステムのマウントポイントが異なる場合に役立ちます。

テーブルスペースの場所はpg_tablespaceに保存されていないため、テーブルスペースを移動しても問題ありません。ただし、テーブルスペースを`data_directory`に移動することは推奨せず、問題が生じる可能性があります。テーブルスペースの移動については、http://www.databasesoup.com/2013/11/moving-tablespaces.html が参考になります。

```text
example: tablespace-map=ts_01=/db/ts_01
```

### 全テーブルスペースマッピングオプション（`--tablespace-map-all`） {#map-all-tablespaces-option---tablespace-map-all}

すべてのテーブルスペースを指定したディレクトリにリストアします。

デフォルトでは、テーブルスペースを元の場所にリストアします。この動作は`tablespace-map`オプションでテーブルスペースごとに変更できますが、すべてのテーブルスペースを一度に新しいディレクトリに再マッピングする方が望ましい場合もあります。バックアップを生成した元のシステムとストレージ構成が異なる可能性がある、開発環境やステージング環境で特に役立ちます。

指定したパスは、バックアップ内のすべてのテーブルスペースを作成する際の親パスになります。

注意：

バックアップの開始後に作成されたテーブルスペースはマッピングされません。テーブルスペースのマッピングが必要な場合は、テーブルスペースの作成後に新しいバックアップを取得してください。

```text
example: tablespace-map-all=/data/tablespace
```

--------

## サーバーオプション {#server-options}

`server`セクションでは、TLSサーバーの設定に使用するオプションを定義します。

### TLSサーバーアドレスオプション（`--tls-server-address`） {#tls-server-address-option---tls-server-address}

TLSサーバーのアドレスです。

サーバーがクライアントのリクエストを待ち受けるIPアドレスです。

```text
default: localhost
example: tls-server-address=*
```

### TLSサーバー認可クライアントオプション（`--tls-server-auth`） {#tls-server-authorized-clients-option---tls-server-auth}

TLSサーバーで認可するクライアントです。

サーバーはクライアントの証明書を検証し、証明書のCN（Common Name）を`tls-server-auth`オプションでサーバーに設定した一覧と照合することで、クライアントを認可します。

`tls-server-auth`オプションにカンマ区切りの一覧を指定すると、クライアントのCNを必要な数のstanzaに対して認可できます。`tls-server-auth=client-cn=*`を指定すると、すべてのstanzaに対して認可できます。クライアントのCNにワイルドカードは指定できません。

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### TLSサーバー認証局オプション（`--tls-server-ca-file`） {#tls-server-certificate-authorities-option---tls-server-ca-file}

TLSサーバーの認証局です。

クライアント証明書が信頼できる認証局によって署名されていることを確認します。

```text
example: tls-server-ca-file=/path/to/server.ca
```

### TLSサーバー証明書オプション（`--tls-server-cert-file`） {#tls-server-certificate-option---tls-server-cert-file}

TLSサーバーの証明書ファイルです。

サーバーの身元を示すためにクライアントに送信します。

```text
example: tls-server-cert-file=/path/to/server.crt
```

### TLSサーバーキーオプション（`--tls-server-key-file`） {#tls-server-key-option---tls-server-key-file}

TLSサーバーのキーファイルです。

サーバー証明書が所有者によって送信されたことを証明します。

```text
example: tls-server-key-file=/path/to/server.key
```

### TLSサーバーポートオプション（`--tls-server-port`） {#tls-server-port-option---tls-server-port}

TLSサーバーのポートです。

サーバーがクライアントのリクエストを待ち受けるポートです。

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## stanzaオプション {#stanza-options}

stanzaは、特定のPostgreSQLデータベースクラスターのバックアップ設定を定義します。stanzaセクションには、データベースクラスターのパスを定義する必要があり、リモートのデータベースクラスターの場合はホスト/ユーザーも必要です。また、グローバル設定のどのセクションも上書きして、stanza固有の設定を定義できます。

**インデックス**：複数のPostgreSQLホストを設定できるように、すべての`pg-`オプションにはインデックスが付きます。たとえば、単一のプライマリーは`pg1-path`、`pg1-port`などのオプションで設定します。スタンバイを設定する場合は、リポジトリホスト上の`pg-`オプションに`pg2-`というインデックスを付けます（例：pg2-host、pg2-pathなど）。

### PostgreSQLデータベースオプション（`--pg-database`） {#postgresql-database-option---pg-database}

PostgreSQLのデータベースです。

PostgreSQLへの接続に使用するデータベース名です。通常はデフォルトが最適ですが、このデータベースが存在しない環境もあります。

従来の動作を維持するため、環境変数`PGDATABASE`の設定は無視されます。

```text
default: postgres
example: pg1-database=backupdb
```

### PostgreSQLホストオプション（`--pg-host`） {#postgresql-host-option---pg-host}

リモート操作時のPostgreSQLホストです。

PostgreSQLホストとリポジトリホストが異なる場合のバックアップに使用します。

```text
example: pg1-host=db.domain.com
```

非推奨の名前：db-host

### PostgreSQLホスト認証局ファイルオプション（`--pg-host-ca-file`） {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

PostgreSQLホストの認証局ファイルです。

PostgreSQLホストへの接続に、システムのデフォルト以外のCAファイルを使用します。

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### PostgreSQLホスト認証局パスオプション（`--pg-host-ca-path`） {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

PostgreSQLホストの認証局パスです。

PostgreSQLホストへの接続に、システムのデフォルト以外のCAパスを使用します。

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### PostgreSQLホスト証明書ファイルオプション（`--pg-host-cert-file`） {#postgresql-host-certificate-file-option---pg-host-cert-file}

PostgreSQLホストの証明書ファイルです。

クライアントの身元を証明するためにPostgreSQLホストに送信します。

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### PostgreSQLホストコマンドオプション（`--pg-host-cmd`） {#postgresql-host-command-option---pg-host-cmd}

PostgreSQLホストのpgBackRestコマンドです。

pgBackRestコマンドのパスがローカルホストとPostgreSQLホストで異なる場合にのみ必要です。未定義の場合、PostgreSQLホストのコマンドにはローカルと同じコマンドを設定します。

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

非推奨の名前：db-cmd

### PostgreSQLホスト設定オプション（`--pg-host-config`） {#postgresql-host-configuration-option---pg-host-config}

pgBackRestデータベースホストの設定ファイルです。

PostgreSQLホスト上の設定ファイルの場所を設定します。PostgreSQLホストの設定ファイルがローカルの設定ファイルと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

非推奨の名前：db-config

### PostgreSQLホスト追加設定パスオプション（`--pg-host-config-include-path`） {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

pgBackRestデータベースホストの追加設定パスです。

PostgreSQLホスト上の追加設定パスの場所を設定します。PostgreSQLホストの追加設定パスがローカルの追加設定パスと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### PostgreSQLホスト設定パスオプション（`--pg-host-config-path`） {#postgresql-host-configuration-path-option---pg-host-config-path}

pgBackRestデータベースホストの設定パスです。

PostgreSQLホスト上の設定パスの場所を設定します。PostgreSQLホストの設定パスがローカルの設定パスと異なる場所にある場合にのみ必要です。

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### PostgreSQLホストキーファイルオプション（`--pg-host-key-file`） {#postgresql-host-key-file-option---pg-host-key-file}

PostgreSQLホストのキーファイルです。

クライアント証明書が所有者によって送信されたことを証明します。

```text
example: pg1-host-key-file=/path/to/client.key
```

### PostgreSQLホストポートオプション（`--pg-host-port`） {#postgresql-host-port-option---pg-host-port}

`pg-host`が設定されている場合のPostgreSQLホストのポートです。

PostgreSQLホストのプロトコルにデフォルト以外のポートを指定するには、このオプションを使用します。

注記：

`pg-host-type=ssh`の場合、`pg-host-port`にデフォルト値はありません。この場合、ポートは`cmd-ssh`で指定したコマンドの設定に従います。

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

非推奨の名前：db-ssh-port

### PostgreSQLホストプロトコル種別オプション（`--pg-host-type`） {#postgresql-host-protocol-type-option---pg-host-type}

PostgreSQLホストのプロトコル種別です。

次のプロトコル種別をサポートします。

- `ssh` - Secure Shell。
- `tls` - pgBackRest TLSサーバー。

```text
default: ssh
example: pg1-host-type=tls
```

### PostgreSQLホストユーザーオプション（`--pg-host-user`） {#postgresql-host-user-option---pg-host-user}

`pg-host`が設定されている場合のPostgreSQLホストへのログインユーザーです。

このユーザーはリモートのpgBackRestプロセスも所有し、PostgreSQLへの接続を開始します。正しく動作させるには、PostgreSQLデータベースクラスターの所有者を使用してください。通常はデフォルトの`postgres`です。

```text
default: postgres
example: pg1-host-user=db_owner
```

非推奨の名前：db-user

### PostgreSQLパスオプション（`--pg-path`） {#postgresql-path-option---pg-path}

PostgreSQLのデータディレクトリです。

PostgreSQLが報告する`data_directory`と同じ値を設定してください。この値はさまざまな場所から読み取れますが、リストアやオフラインバックアップ時にそれらを利用できない場合に備えて、設定しておくことが賢明です。

`pg-path`オプションは、オンラインバックアップのたびにPostgreSQLが報告する値と照合されるため、常に最新の値であるはずです。

```text
example: pg1-path=/data/db
```

非推奨の名前：db-path

### PostgreSQLポートオプション（`--pg-port`） {#postgresql-port-option---pg-port}

PostgreSQLのポートです。

PostgreSQLが使用しているポートです。ほとんどのPostgreSQLクラスターはデフォルトのポートを使用するため、通常は指定する必要がありません。

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

非推奨の名前：db-port

### PostgreSQLソケットパスオプション（`--pg-socket-path`） {#postgresql-socket-path-option---pg-socket-path}

PostgreSQLのunixソケットパスです。

PostgreSQLの起動時に指定したunixソケットディレクトリです。pgBackRestはOSの標準の場所を自動検索するため、`postgresql.conf`の`unix_socket_directories`設定でソケットディレクトリを明示的に変更した場合を除き、通常はこの設定を指定する必要がありません。

```text
example: pg1-socket-path=/var/run/postgresql
```

非推奨の名前：db-socket-path

### PostgreSQLデータベースユーザーオプション（`--pg-user`） {#postgresql-database-user-option---pg-user}

PostgreSQLのデータベースユーザーです。

PostgreSQLへの接続に使用するデータベースユーザー名です。未指定の場合、pgBackRestはローカルのOSユーザーまたは`PGUSER`で接続します。

```text
example: pg1-user=backupuser
```
