---
title: "アーカイブ送信コマンド（archive-push）"
linkTitle: "archive-push"
weight: 30
description: "pgBackRestの`archive-push`コマンドのオプションと動作のリファレンス。"
icon: fa-solid fa-cloud-arrow-up
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/command.html#command-archive-push"
---

PostgreSQLからWALセグメントを受け取り、インデックス付きの`repo-path`オプションで定義された各リポジトリにアーカイブします（リポジトリの設定については、[リポジトリ](/ja/pgbackrest/configuration/#repository-options)セクションを参照）。WALセグメントは、`archive-async`の値に応じて、直ちにアーカイブに送信されるか、ローカルに保存されます。複数のリポジトリが設定されている場合、`archive-push`はできる限り多くのリポジトリへの送信を試みます。

`archive-push`は、PostgreSQLに設定して呼び出すことを想定しています。例は、[アーカイブの設定](/ja/pgbackrest/user-guide/#configure-archiving)を参照してください。

## コマンドオプション {#command-options}

### 非同期アーカイブオプション（`--archive-async`） {#asynchronous-archiving-option---archive-async}

WALセグメントを非同期に送信/取得します。

`archive-push`コマンドと`archive-get`コマンドの非同期処理を有効にします。

非同期処理では接続の再利用と並列処理が可能なため、効率が向上します。詳細は`spool-path`、`archive-get-queue-max`、`archive-push-queue-max`の各オプションを参照してください。

```yaml
default: n
example: --archive-async
```

### アーカイブ確認オプション（`--archive-check`） {#check-archive-option---archive-check}

バックアップの完了前に、WALセグメントがアーカイブに存在することを確認します。

バックアップの一貫性を確保するために必要なすべてのWALセグメントが、WALアーカイブに存在することを確認します。別のアーカイブ方法を使用していない限り、デフォルトのままにしておくことを推奨します。

`archive-copy`が有効な場合は、このオプションを有効にする必要があります。

```yaml
default: y
example: --no-archive-check
```

### アーカイブモード確認オプション（`--archive-mode-check`） {#check-archive-mode-option---archive-mode-check}

PostgreSQLの`archive_mode`設定を確認します。

このオプションはデフォルトで有効で、PostgreSQLの`archive_mode=always`を禁止します。

スタンバイサーバーから送信されたWALセグメントは、プライマリーから送信されたWALセグメントと論理的には同じでも、チェックサムが異なる場合があります。競合を避けるため、複数のソースからのアーカイブを無効にすることを推奨します。

注意：

このオプションを無効にする場合は、`archive-push`コマンドを通じてリポジトリに書き込むアーカイバーが1つだけであることを必ず確認してください。

```yaml
default: y
example: --no-archive-mode-check
```

### アーカイブ送信バッチサイズオプション（`--archive-push-batch-size`） {#archive-push-batch-size-option---archive-push-batch-size}

非同期処理の1回の実行で送信するWALの最大量です。

非同期モードでは、`archive-push`プロセスは準備ができているすべてのWALセグメントを1回の実行で送信します。`archive-push-queue-max`は各実行の開始時にのみ確認されるため、非常に多くのセグメントを処理する実行では、再確認までの間にキューが上限を大幅に超えて増大することがあります。

このオプションは1回の実行で処理するWALの量を制限します。プロセスは終了後、次の`archive-push`によって再び起動され、その際にキューが再確認されます。値を小さくするとキューの確認頻度が高くなりますが、非同期プロセスの起動頻度も高くなります。値はWALセグメント単位で切り捨てられますが、常に少なくとも1つのセグメントは処理されます。

```yaml
default: 16GiB
allowed: [1MiB, 4PiB]
example: --archive-push-batch-size=1GiB
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

```yaml
allowed: [0B, 4PiB]
example: --archive-push-queue-max=1TiB
```

非推奨の名前：archive-queue-max

### アーカイブタイムアウトオプション（`--archive-timeout`） {#archive-timeout-option---archive-timeout}

アーカイブのタイムアウトです。

各WALセグメントがpgBackRestのアーカイブリポジトリに到達するまで待機する最大時間を秒単位で設定します。このタイムアウトは、バックアップの一貫性に必要なWALセグメントのアーカイブを待つ際に、`check`コマンドと`backup`コマンドに適用されます。

```yaml
default: 1m
allowed: [100ms, 1d]
example: --archive-timeout=30
```

## 一般オプション {#general-options}

### rootでの実行許可オプション（`--allow-root`） {#allow-run-as-root-option---allow-root}

rootユーザーによるコマンドの実行を許可します。

デフォルトでは、ファイルの所有権を慎重に管理するように設計された`restore`コマンドのみをrootユーザーで実行できます。ほかのコマンドをrootで実行すると、たとえばリポジトリ内にroot所有のファイルが作成され、PostgreSQLユーザーがアクセスできなくなって、後続のコマンドが失敗するおそれがあります。

それでもコマンドをrootで実行する場合は、このオプションを有効にします。ただし、リポジトリとPostgreSQLクラスターを所有するユーザーとしてpgBackRestを実行する方がはるかに適切です。

```yaml
default: n
example: --allow-root
```

### バッファーサイズオプション（`--buffer-size`） {#buffer-size-option---buffer-size}

I/O処理のバッファーサイズです。

コピー、圧縮、暗号化などの処理に使用するバッファーサイズです。使用するバッファーの数はオプションによって異なり、各処理で追加のメモリを使用する場合があります。たとえば、`gz`圧縮では256KiBのメモリを追加で使用する場合があります。

指定できる値は、`16KiB`、`32KiB`、`64KiB`、`128KiB`、`256KiB`、`512KiB`、`1MiB`、`2MiB`、`4MiB`、`8MiB`、`16MiB`です。

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### pgBackRestコマンドオプション（`--cmd`） {#pgbackrest-command-option---cmd}

pgBackRestコマンドです。

pgBackRestは、たとえば`restore`コマンドがrestore_command設定を生成する際に、コマンド文字列を生成することがあります。この場合、`cmd`オプションを指定しない限り、pgBackRestプロセスの実行に使用したコマンドが使われます。

注意：

pgBackRestコマンドをラッパー経由で実行すると、予測できない動作を引き起こす可能性があるため、推奨しません。

```yaml
default: [path of executed pgbackrest binary]
example: --cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### SSHクライアントコマンドオプション（`--cmd-ssh`） {#ssh-client-command-option---cmd-ssh}

SSHクライアントのコマンドです。

別のSSHクライアントを使用したい場合や、`ssh`コマンドが$PATHに含まれていない場合に、使用するSSHクライアントコマンドを指定します。

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### 圧縮オプション（`--compress`） {#compress-option---compress}

ファイル圧縮を使用します。

バックアップファイルは、コマンドラインの圧縮ツールと互換性があります。

このオプションは現在非推奨です。代わりに`compress-type`オプションを使用してください。

```yaml
default: y
example: --no-compress
```

### 圧縮レベルオプション（`--compress-level`） {#compress-level-option---compress-level}

ファイルの圧縮レベルです。

`compress-type`が`none`でない場合、または`compress=y`（非推奨）の場合に、ファイル圧縮に使用するレベルを設定します。

```yaml
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

example: --compress-level=9
```

### ネットワーク圧縮レベルオプション（`--compress-level-network`） {#network-compress-level-option---compress-level-network}

ネットワークの圧縮レベルです。

`compress-type=none`で、コマンドがリポジトリと同じホストで実行されない場合のネットワーク圧縮レベルを設定します。圧縮によってネットワークトラフィックを削減します。`compress-type`が`none`でない場合は、ファイルを1回だけ圧縮するように、`compress-level-network`設定を無視して代わりに`compress-level`を使用します。

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### 圧縮形式オプション（`--compress-type`） {#compress-type-option---compress-type}

ファイルの圧縮形式です。

次の圧縮形式をサポートします。

- `none` - 圧縮なし
- `bz2` - bzip2圧縮形式
- `gz` - gzip圧縮形式
- `lz4` - lz4圧縮形式（一部のプラットフォームでは利用不可）
- `zst` - Zstandard圧縮形式（一部のプラットフォームでは利用不可）

```yaml
default: gz
example: --compress-type=none
```

### 設定ファイルオプション（`--config`） {#config-option---config}

pgBackRestの設定ファイルです。

デフォルトとは異なる設定ファイルを指定するには、このオプションを使用します。

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### 追加設定パスオプション（`--config-include-path`） {#config-include-path-option---config-include-path}

追加のpgBackRest設定ファイルへのパスです。

指定した場所にある拡張子`.conf`の設定ファイルをpgBackRest設定ファイルと連結し、1つの設定ファイルとして扱います。

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### 設定パスオプション（`--config-path`） {#config-path-option---config-path}

pgBackRest設定ファイルの基準パスです。

この設定は、`--config`と`--config-include-path`の各オプションがコマンドラインで明示的に設定されていない場合に、それらのデフォルトの基準パスを上書きします。

たとえば、`--config-path=/conf/pgbackrest`だけを渡すと、`--config`のデフォルトは`/conf/pgbackrest/pgbackrest.conf`に、`--config-include-path`のデフォルトは`/conf/pgbackrest/conf.d`に設定されます。

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### I/Oタイムアウトオプション（`--io-timeout`） {#io-timeout-option---io-timeout}

I/Oのタイムアウトです。

接続および読み取り/書き込み処理に使用する、秒単位のタイムアウトです。

読み取り/書き込み処理全体がこのタイムアウト内に完了する必要はありませんが、わずか1バイトでも、*何らかの*進展が必要です。

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### ロックパスオプション（`--lock-path`） {#lock-path-option---lock-path}

ロックファイルを保存するパスです。

ロックパスは、pgBackRestが競合する処理の同時実行を防ぐためのロックファイルを作成する場所です。

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### 固定umaskオプション（`--neutral-umask`） {#neutral-umask-option---neutral-umask}

固定のumaskを使用します。

umaskを0000に設定し、リポジトリ内のファイルやディレクトリが適切な権限で作成されるようにします。デフォルトのディレクトリ権限は0750、ファイル権限は0640です。

代わりに実行ユーザーのumaskを使用するには、設定ファイルに`neutral-umask=n`、またはコマンドラインに`--no-neutral-umask`を指定します。

```yaml
default: y
example: --no-neutral-umask
```

### プロセス優先度設定オプション（`--priority`） {#set-process-priority-option---priority}

プロセスの優先度を設定します。

カーネルのスケジューラーがプロセスに与える優先度（niceness）を定義します。正の値は優先度を下げ、負の値は優先度を上げます。通常、プロセスには自身の優先度を上げる権限がありません。

```yaml
allowed: [-20, 19]
example: --priority=19
```

### 最大プロセス数オプション（`--process-max`） {#process-maximum-option---process-max}

圧縮/転送に使用する最大プロセス数です。

各プロセスが圧縮と転送を実行することでコマンドを高速化しますが、データベースのパフォーマンスに影響するほど`process-max`を高く設定しないでください。

```yaml
default: 1
allowed: [1, 999]
example: --process-max=4
```

### プロトコルタイムアウトオプション（`--protocol-timeout`） {#protocol-timeout-option---protocol-timeout}

プロトコルのタイムアウトです。

ローカルまたはリモートのプロセスが、プロトコル層で新しいメッセージの受信を待つタイムアウトを秒単位で設定します。これにより、プロセスがメッセージを無期限に待ち続けることを防ぎます。

> **注記：** `protocol-timeout`オプションは、`db-timeout`オプションより大きくする必要があります。

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### キープアライブオプション（`--sck-keep-alive`） {#keep-alive-option---sck-keep-alive}

キープアライブを有効にします。

ソケット接続でキープアライブメッセージを有効にします。

```yaml
default: y
example: --no-sck-keep-alive
```

### スプールパスオプション（`--spool-path`） {#spool-path-option---spool-path}

一時的なデータを保存するパスです。

このパスは、非同期の`archive-push`コマンドと`archive-get`コマンドのデータを保存するために使用します。

非同期の`archive-push`コマンドは、アーカイブへのWALの保存が成功すると確認応答を（失敗時にはエラーを）スプールパスに書き込み、フォアグラウンドプロセスがPostgreSQLに速やかに通知できるようにします。確認応答ファイルは非常に小さく、成功時は0バイト、エラー時も数百バイトです。

非同期の`archive-get`コマンドは、PostgreSQLの要求時にWALをすぐに提供できるよう、スプールパスにWALをキューイングします。スプールパスが`pg_xlog`/`pg_wal`と同じファイルシステム上にあると、PostgreSQLへのファイル移動が最も効率的です。ただし、スプールパスを`pg_xlog`/`pg_wal`ディレクトリの*内部*に配置すると、`pg_rewind`などのPostgreSQLユーティリティーに問題が生じる可能性があるため、推奨しません。

スプールパスに保存されたデータは再起動後も保持でき、保持することが望ましいため、厳密には一時データではありません。ただし、スプールパス内のデータが失われても問題はありません。pgBackRestは、`archive-push`では各WALセグメントが安全にアーカイブされていることを再確認し、`archive-get`ではキューを再構築するだけです。

スプールパスは、NFSやCIFSなどのリモートファイルシステムではなく、ローカルのPosix互換ファイルシステム上に置くことを想定しています。

```yaml
default: /var/spool/pgbackrest
example: --spool-path=/backup/db/spool
```

### stanzaオプション（`--stanza`） {#stanza-option---stanza}

stanzaを定義します。

stanzaは、PostgreSQLデータベースクラスターの場所、バックアップ方法、アーカイブオプションなどを定義する設定です。ほとんどのデータベースサーバーにはPostgreSQLデータベースクラスターが1つだけ存在し、stanzaも1つになります。一方、バックアップサーバーには、バックアップが必要なデータベースクラスターごとにstanzaがあります。

stanzaにはプライマリークラスターにちなんだ名前を付けたくなりますが、クラスターに含まれるデータベースを表す名前の方が適しています。stanza名はプライマリーとすべてのレプリカで使用するため、mainやprodなどのローカルクラスター名よりも、appやdwなど、クラスターの実際の役割を表す名前を選ぶ方が適切です。

```yaml
example: --stanza=main
```

### キープアライブ回数オプション（`--tcp-keep-alive-count`） {#keep-alive-count-option---tcp-keep-alive-count}

キープアライブの回数です。

接続が切れたと判断するまでに、応答がなくても許容するTCPキープアライブメッセージの数を指定します。

このオプションは、`TCP_KEEPCNT`ソケットオプションをサポートするシステムで利用できます。

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### キープアライブ待機時間オプション（`--tcp-keep-alive-idle`） {#keep-alive-idle-option---tcp-keep-alive-idle}

キープアライブの待機時間です。

ネットワーク通信がない状態で、オペレーティングシステムがTCPキープアライブメッセージを送信するまでの時間を秒単位で指定します。

このオプションは、`TCP_KEEPIDLE`ソケットオプションをサポートするシステムで利用できます。

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### キープアライブ間隔オプション（`--tcp-keep-alive-interval`） {#keep-alive-interval-option---tcp-keep-alive-interval}

キープアライブの送信間隔です。

応答のないTCPキープアライブメッセージを再送信するまでの時間を秒単位で指定します。

このオプションは、`TCP_KEEPINTVL`ソケットオプションをサポートするシステムで利用できます。

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### TLSv1.2暗号スイートオプション（`--tls-cipher-12`） {#tlsv12-cipher-suites-option---tls-cipher-12}

許可するTLSv1.2暗号スイートです。

pgBackRestクライアントとサーバー間のすべてのTLS接続は暗号化されます。デフォルトでは、オブジェクトストア（例：S3）への接続も暗号化されます。

> **注記：** どのトランスポート接続でも、セキュリティーの最低要件はTLSv1.2です。

必要に応じて、受け入れる暗号スイートを調整できます。特別なセキュリティー要件がなければ、例に示す値が妥当な選択です。未設定（デフォルト）の場合は、使用するOpenSSLライブラリのデフォルトが適用されます。

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### TLSv1.3暗号スイートオプション（`--tls-cipher-13`） {#tlsv13-cipher-suites-option---tls-cipher-13}

許可するTLSv1.3暗号スイートです。

pgBackRestクライアントとサーバー間のすべてのTLS接続は暗号化されます。デフォルトでは、オブジェクトストア（例：S3）への接続も暗号化されます。

> **注記：** どのトランスポート接続でも、セキュリティーの最低要件はTLSv1.2です。

必要に応じて、受け入れる暗号スイートを調整できます。未設定（デフォルト）の場合は、使用するOpenSSLライブラリのデフォルトが適用されます。

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## ログオプション {#log-options}

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

```yaml
default: warn
example: --log-level-console=error
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

```yaml
default: info
example: --log-level-file=debug
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

```yaml
default: off
example: --log-level-stderr=error
```

### ログパスオプション（`--log-path`） {#log-path-option---log-path}

ログファイルを保存するパスです。

ログパスは、pgBackRestがログファイルを保存する場所です。`log-level-file=off`の場合、ログパスは不要です。

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### サブプロセスログオプション（`--log-subprocess`） {#log-subprocesses-option---log-subprocess}

サブプロセスでのログ記録を有効にします。

このプロセスが作成するすべてのサブプロセスで、`log-level-file`で指定したログレベルによるファイルへのログ記録を有効にします。

```yaml
default: n
example: --log-subprocess
```

### ログタイムスタンプオプション（`--log-timestamp`） {#log-timestamp-option---log-timestamp}

ログのタイムスタンプを有効にします。

コンソールとファイルのログでタイムスタンプを有効にします。このオプションは、ドキュメント生成などの特殊な状況では無効にします。

```yaml
default: y
example: --no-log-timestamp
```

## メンテナー向けオプション {#maintainer-options}

### WALヘッダー確認オプション（`--archive-header-check`） {#check-wal-headers-option---archive-header-check}

WALヘッダー内のPostgreSQLバージョン/識別子を確認します。

このオプションはデフォルトで有効で、WALヘッダーをPostgreSQLのバージョンおよびシステム識別子と照合し、WALが正しいstanzaにコピーされることを確認します。これは、`pg_control`とstanzaの照合、およびWALのコピー元が`pg_control`の存在するPostgreSQLデータディレクトリと同じであることの確認に加えて実行されます。

したがって、この確認の無効化は比較的安全ですが、WALが暗号化されている場合など、必要な場合に限って行ってください。

```yaml
default: y
example: --no-archive-header-check
```

### PostgreSQLバージョン強制指定オプション（`--pg-version-force`） {#force-postgresql-version-option---pg-version-force}

PostgreSQLのバージョンを強制指定します。

`pg_control`またはWALヘッダーを読み取って自動検出したバージョンの代わりに、指定したPostgreSQLバージョンを使用します。これは主に、これらの値がリリース版とは異なるPostgreSQLのフォークや開発版で役立ちます。PostgreSQLが`server_version_num`で報告するバージョンは、強制指定したバージョンと一致する必要があります。

警告：

このオプションは慎重に使用してください。`pg_control`とWALヘッダーは引き続き、指定バージョンで想定される形式、つまり公式のオープンソース版PostgreSQLの形式で読み取られます。フォークや開発版が、pgBackRestの依存するフィールドの形式を変更していると、予期しない動作が生じます。一般に、このオプションが想定どおりに動作するのは、フォークが独自の構造体メンバーをすべて標準のPostgreSQLメンバーの*後ろ*に追加している場合に限られます。

```yaml
example: --pg-version-force=15
```

## リポジトリオプション {#repository-options}

### Azureリポジトリコンテナーオプション（`--repo-azure-container`） {#azure-repository-container-option---repo-azure-container}

Azureリポジトリのコンテナーです。

リポジトリの保存に使用するAzureコンテナーです。

`repo-path=/`を設定するとpgBackRestリポジトリをコンテナーのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのAzureが生成するコンテンツもコンテナーに保存できるようにすることを推奨します。

```yaml
example: --repo1-azure-container=pg-backup
```

### Azureリポジトリキー種別オプション（`--repo-azure-key-type`） {#azure-repository-key-type-option---repo-azure-key-type}

Azureリポジトリのキー種別です。

次の認証方式をサポートします。

- `shared` - 共有キー
- `sas` - 共有アクセス署名
- `auto` - AzureマネージドIDを使用して自動的に認可

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### AzureリポジトリURI形式オプション（`--repo-azure-uri-style`） {#azure-repository-uri-style-option---repo-azure-uri-style}

AzureのURI形式です。

次のURI形式をサポートします。

- `host` - `account.endpoint`ホストに接続します。
- `path` - `endpoint`ホストに接続し、URIの先頭にアカウントを付加します。

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### リポジトリ暗号方式オプション（`--repo-cipher-type`） {#repository-cipher-type-option---repo-cipher-type}

リポジトリの暗号化に使用する暗号方式です。

次の暗号方式をサポートします。

- `none` - リポジトリを暗号化しません
- `aes-256-cbc` - 鍵長256ビットのAdvanced Encryption Standard

リポジトリの種類（例：S3）が暗号化をサポートしていても、暗号化は常にクライアント側で実行されます。

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### GCSリポジトリバケットオプション（`--repo-gcs-bucket`） {#gcs-repository-bucket-option---repo-gcs-bucket}

GCSリポジトリのバケットです。

リポジトリの保存に使用するGCSバケットです。

`repo-path=/`を設定するとpgBackRestリポジトリをバケットのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのGCSが生成するコンテンツもバケットに保存できるようにすることを推奨します。

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### GCSリポジトリエンドポイントオプション（`--repo-gcs-endpoint`） {#gcs-repository-endpoint-option---repo-gcs-endpoint}

GCSリポジトリのエンドポイントです。

ストレージサービスへの接続に使用するエンドポイントです。ローカルのGCSサーバーや別のエンドポイントを使用するように変更できます。

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
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

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### GCSリポジトリプロジェクトIDオプション（`--repo-gcs-user-project`） {#gcs-repository-project-id-option---repo-gcs-user-project}

GCSのプロジェクトIDです。

リクエストの課金先を決定するために使用するGCSプロジェクトIDです。

```yaml
example: --repo1-gcs-user-project=my-project
```

### リポジトリホストオプション（`--repo-host`） {#repository-host-option---repo-host}

リモート操作時のリポジトリホストです。

ローカルにマウントされたファイルシステムにバックアップおよびアーカイブする場合、この設定は不要です。

```yaml
example: --repo1-host=repo1.domain.com
```

非推奨の名前：backup-host

### リポジトリホスト認証局ファイルオプション（`--repo-host-ca-file`） {#repository-host-certificate-authority-file-option---repo-host-ca-file}

リポジトリホストの認証局ファイルです。

リポジトリホストへの接続に、システムのデフォルト以外のCAファイルを使用します。

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### リポジトリホスト認証局パスオプション（`--repo-host-ca-path`） {#repository-host-certificate-authority-path-option---repo-host-ca-path}

リポジトリホストの認証局パスです。

リポジトリホストへの接続に、システムのデフォルト以外のCAパスを使用します。

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### リポジトリホスト証明書ファイルオプション（`--repo-host-cert-file`） {#repository-host-certificate-file-option---repo-host-cert-file}

リポジトリホストの証明書ファイルです。

クライアントの身元を証明するためにリポジトリホストに送信します。

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### リポジトリホストコマンドオプション（`--repo-host-cmd`） {#repository-host-command-option---repo-host-cmd}

リポジトリホストのpgBackRestコマンドです。

pgBackRestコマンドのパスがローカルホストとリポジトリホストで異なる場合にのみ必要です。未定義の場合、リポジトリホストのコマンドにはローカルと同じコマンドを設定します。

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

非推奨の名前：backup-cmd

### リポジトリホスト設定オプション（`--repo-host-config`） {#repository-host-configuration-option---repo-host-config}

pgBackRestリポジトリホストの設定ファイルです。

リポジトリホスト上の設定ファイルの場所を設定します。リポジトリホストの設定ファイルがローカルの設定ファイルと異なる場所にある場合にのみ必要です。

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

非推奨の名前：backup-config

### リポジトリホスト追加設定パスオプション（`--repo-host-config-include-path`） {#repository-host-configuration-include-path-option---repo-host-config-include-path}

pgBackRestリポジトリホストの追加設定パスです。

リポジトリホスト上の追加設定パスの場所を設定します。リポジトリホストの追加設定パスがローカルの追加設定パスと異なる場所にある場合にのみ必要です。

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### リポジトリホスト設定パスオプション（`--repo-host-config-path`） {#repository-host-configuration-path-option---repo-host-config-path}

pgBackRestリポジトリホストの設定パスです。

リポジトリホスト上の設定パスの場所を設定します。リポジトリホストの設定パスがローカルの設定パスと異なる場所にある場合にのみ必要です。

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### リポジトリホストキーファイルオプション（`--repo-host-key-file`） {#repository-host-key-file-option---repo-host-key-file}

リポジトリホストのキーファイルです。

クライアント証明書が所有者によって送信されたことを証明します。

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### リポジトリホストポートオプション（`--repo-host-port`） {#repository-host-port-option---repo-host-port}

`repo-host`が設定されている場合のリポジトリホストのポートです。

リポジトリホストのプロトコルにデフォルト以外のポートを指定するには、このオプションを使用します。

> **注記：** `repo-host-type=ssh`の場合、`repo-host-port`にデフォルト値はありません。この場合、ポートは`cmd-ssh`で指定したコマンドの設定に従います。

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

非推奨の名前：backup-ssh-port

### リポジトリホストプロトコル種別オプション（`--repo-host-type`） {#repository-host-protocol-type-option---repo-host-type}

リポジトリホストのプロトコル種別です。

次のプロトコル種別をサポートします。

- `ssh` - Secure Shell。
- `tls` - pgBackRest TLSサーバー。

```yaml
default: ssh
example: --repo1-host-type=tls
```

### リポジトリホストユーザーオプション（`--repo-host-user`） {#repository-host-user-option---repo-host-user}

`repo-host`が設定されている場合のリポジトリホストのユーザーです。

リポジトリホスト上の操作に使用するユーザーを定義します。`postgres`ユーザーではなく、`pgbackrest`などの別のユーザーを使用することを推奨します。リポジトリホストでPostgreSQLを実行する場合は、`postgres`ユーザーを`pgbackrest`グループに追加することで、リポジトリの内容を誤って破損させずに読み取り権限を与えられます。

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

非推奨の名前：backup-user

### リポジトリパスオプション（`--repo-path`） {#repository-path-option---repo-path}

バックアップとアーカイブを保存するパスです。

リポジトリは、pgBackRestがバックアップを保存し、WALセグメントをアーカイブする場所です。

必要な容量を事前に見積もるのは難しい場合があります。まずいくつかバックアップを取得し、各種類（full/incr/diff）のバックアップサイズを記録して、1日当たりに生成されるWALの量を測定するのが最善です。これにより、必要な容量のおおよその見当が付きます。ただし、データベースの変化に伴い、必要量も時間とともに変わる可能性があります。

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### S3リポジトリバケットオプション（`--repo-s3-bucket`） {#s3-repository-bucket-option---repo-s3-bucket}

S3リポジトリのバケットです。

リポジトリの保存に使用するS3バケットです。

`repo-path=/`を設定するとpgBackRestリポジトリをバケットのルートに保存できますが、通常は`/repo`などの接頭辞を指定し、ログなどのAWSが生成するコンテンツもバケットに保存できるようにすることを推奨します。

```yaml
example: --repo1-s3-bucket=pg-backup
```

### S3リポジトリエンドポイントオプション（`--repo-s3-endpoint`） {#s3-repository-endpoint-option---repo-s3-endpoint}

S3リポジトリのエンドポイントです。

選択したリージョンに対して有効なAWSエンドポイントを使用してください。

独自の構成やテスト構成では、`repo-storage-ca-file`、`repo-storage-ca-path`、`repo-storage-host`、`repo-storage-port`、`repo-storage-verify-tls`の各オプションが役立つ場合があります。

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### S3リポジトリキー種別オプション（`--repo-s3-key-type`） {#s3-repository-key-type-option---repo-s3-key-type}

S3リポジトリのキー種別です。

次の認証方式をサポートします。

- `shared` - 共有キー
- `auto` - 一時認証情報を自動取得
- `web-id` - ウェブID認証情報を自動取得
- `pod-id` - EKS Pod Identityの認証情報を自動取得
- `process` - プロセスを実行して認証情報を取得

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### S3リポジトリKMSキーIDオプション（`--repo-s3-kms-key-id`） {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

S3リポジトリのKMSキーです。

指定したAWS Key Management Serviceのキーを使用して、S3のサーバー側暗号化を有効にします。

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3認証プロセスコマンドオプション（`--repo-s3-process-cmd`） {#s3-authentication-process-command-option---repo-s3-process-cmd}

S3の認証プロセスコマンドです。

一時的なS3認証情報を取得するために実行するコマンド（および任意の引数）です。リストの最初の要素がコマンドで、残りの要素はパラメーターとして渡します。

プロセスは、`AccessKeyId`、`SecretAccessKey`、`SessionToken`、`Expiration`フィールドを含むJSONを出力する必要があります。認証情報は有効期限の前に自動更新されます。形式の詳細は、[プロセス認証情報プロバイダー](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output)を参照してください。

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### S3リポジトリリージョンオプション（`--repo-s3-region`） {#s3-repository-region-option---repo-s3-region}

S3リポジトリのリージョンです。

バケットを作成したAWSリージョンです。

```yaml
example: --repo1-s3-region=us-east-1
```

### S3リポジトリのリクエスタ支払いオプション（`--repo-s3-requester-pays`） {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

S3リポジトリのリクエスタ支払いです。

S3のリクエスタ支払いを有効にします。

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### S3リポジトリロールオプション（`--repo-s3-role`） {#s3-repository-role-option---repo-s3-role}

S3リポジトリのロールです。

`repo-s3-key-type=auto`の場合に、一時認証情報の取得に使用するAWSロール名（完全なARNではありません）です。

```yaml
example: --repo1-s3-role=authrole
```

### S3リポジトリサービスオプション（`--repo-s3-service`） {#s3-repository-service-option---repo-s3-service}

S3の署名サービスです。

SigV4認証で使用するS3署名サービスです。標準のS3エンドポイントでは、デフォルトは`s3`です。S3 Outpostsエンドポイントを使用する場合は、`s3-outposts`に設定します。

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### S3リポジトリSTSエンドポイントオプション（`--repo-s3-sts-host`） {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

S3リポジトリのSTSエンドポイントです。

`repo-s3-key-type=web-id`を設定した場合に、一時認証情報の取得に使用するSTSエンドポイントです。リージョン別STSを使用するには、リージョン別エンドポイント（例：`sts.us-east-1.amazonaws.com`）を設定します。GovCloudや中国リージョンで必要になる場合や、レイテンシーを低減するために使用する場合があります。

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### S3リポジトリURI形式オプション（`--repo-s3-uri-style`） {#s3-repository-uri-style-option---repo-s3-uri-style}

S3のURI形式です。

次のURI形式をサポートします。

- `host` - `bucket.endpoint`ホストに接続します。
- `path` - `endpoint`ホストに接続し、URIの先頭にバケットを付加します。

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### SFTPリポジトリホストオプション（`--repo-sftp-host`） {#sftp-repository-host-option---repo-sftp-host}

SFTPリポジトリのホストです。

リポジトリが存在するSFTPホストです。

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### SFTPリポジトリホストフィンガープリントオプション（`--repo-sftp-host-fingerprint`） {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

SFTPリポジトリホストのフィンガープリントです。

SFTPリポジトリホストのフィンガープリントの生成方法は、`repo-sftp-host-key-hash-type`と一致させてください。`awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`でフィンガープリントを生成します。sshホストキーは通常、`/etc/ssh`ディレクトリにあります。

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### SFTPホストキー確認方式オプション（`--repo-sftp-host-key-check-type`） {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

SFTPのホストキー確認方式です。

次のSFTPホストキー確認方式をサポートします。

- `strict` - pgBackRestは~/.ssh/known_hostsファイルにホストキーを自動追加せず、ホストキーが変更されたホスト、または既知のホストファイルで見つからないホストへの接続を拒否します。このオプションでは、新しいホストをすべて手動で追加する必要があります。
- `accept-new` - pgBackRestは新しいホストキーをユーザーの既知のホストファイルに自動追加しますが、ホストキーが変更されたホストへの接続は許可しません。
- `fingerprint` - pgBackRestは、`repo-sftp-host-fingerprint`オプションで指定したフィンガープリントとホストキーを照合します。
- `none` - ホストキーを確認しません。

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### SFTPリポジトリホストキーハッシュ種別オプション（`--repo-sftp-host-key-hash-type`） {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

SFTPリポジトリのホストキーハッシュ種別です。

SSHの開始時に、リモートシステムのホストキーのダイジェスト計算に使用するハッシュ種別を指定します。指定可能な値は`md5`、`sha1`、`sha256`ですが、`sha256`は新しいバージョンの`libssh2`でのみサポートされます。

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### SFTPリポジトリホストポートオプション（`--repo-sftp-host-port`） {#sftp-repository-host-port-option---repo-sftp-host-port}

SFTPリポジトリホストのポートです。

SFTPリポジトリホストのポートです。

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### SFTPリポジトリホストユーザーオプション（`--repo-sftp-host-user`） {#sftp-repository-host-user-option---repo-sftp-host-user}

SFTPリポジトリホストのユーザーです。

リポジトリの保存に使用するホスト上のユーザーです。

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### SFTP既知ホストファイルオプション（`--repo-sftp-known-host`） {#sftp-known-hosts-file-option---repo-sftp-known-host}

SFTPの既知のホストファイルです。

認証時に一致するSFTPホストを探す既知のホストファイルです。未指定の場合、pgBackRestはデフォルトで`~/.ssh/known_hosts`、`~/.ssh/known_hosts2`、`/etc/ssh/ssh_known_hosts`、`/etc/ssh/ssh_known_hosts2`を検索します。1つ以上のファイルパスを設定した場合は、それらを検索して一致を確認します。ファイルパスは絶対パス、または先頭がチルダのパスである必要があります。`repo-sftp-known-host`オプションを複数回指定することで、検索する既知のホストファイルを複数指定できます。既知のホストファイルによる確認を使用するには、`repo-sftp-host-fingerprint`を指定してはいけません。`repo-sftp-host-check-type`オプションも参照してください。

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### SFTPリポジトリ秘密鍵ファイルオプション（`--repo-sftp-private-key-file`） {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

SFTPの秘密鍵ファイルです。

認証に使用するSFTP秘密鍵ファイルです。

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### SFTPリポジトリ公開鍵ファイルオプション（`--repo-sftp-public-key-file`） {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

SFTPの公開鍵ファイルです。

認証に使用するSFTP公開鍵ファイルです。OpenSSLに対してコンパイルした場合は任意ですが、別のライブラリに対してコンパイルした場合は必須です。

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### リポジトリストレージCAファイルオプション（`--repo-storage-ca-file`） {#repository-storage-ca-file-option---repo-storage-ca-file}

リポジトリストレージのCAファイルです。

ストレージ（例：S3、Azure）の証明書に、システムのデフォルト以外のCAファイルを使用します。

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

非推奨の名前：repo-azure-ca-file, repo-s3-ca-file

### リポジトリストレージTLS CAパスオプション（`--repo-storage-ca-path`） {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

リポジトリストレージのCAパスです。

ストレージ（例：S3、Azure）の証明書に、システムのデフォルト以外のCAパスを使用します。

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

非推奨の名前：repo-azure-ca-path, repo-s3-ca-path

### リポジトリストレージホストオプション（`--repo-storage-host`） {#repository-storage-host-option---repo-storage-host}

リポジトリストレージのホストです。

ストレージ（例：S3、Azure）のエンドポイントとは異なるホストに接続します。通常はテストに使用します。

```yaml
example: --repo1-storage-host=127.0.0.1
```

非推奨の名前：repo-azure-host, repo-s3-host

### リポジトリストレージポートオプション（`--repo-storage-port`） {#repository-storage-port-option---repo-storage-port}

リポジトリストレージのポートです。

ストレージ（例：S3、Azure）のエンドポイント（ホストを指定した場合はそのホスト）への接続に使用するポートです。

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

非推奨の名前：repo-azure-port, repo-s3-port

### リポジトリストレージのプリフェッチオプション（`--repo-storage-prefetch`） {#repository-storage-prefetch-option---repo-storage-prefetch}

リポジトリストレージのプリフェッチです。

S3などのオブジェクトストアから読み取る際に、先行して発行するリクエスト数を指定します。真の並行処理ではありませんが、リクエストの送信に伴う遅延を減らします。

最初の読み取りはプリフェッチできないため、読み取りごとの未完了リクエスト数はプリフェッチ数より1つ多くなります。

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### リポジトリストレージの読み飛ばしオプション（`--repo-storage-read-over`） {#repository-storage-read-over-option---repo-storage-read-over}

リポジトリストレージの読み飛ばしです。

バンドルには、すでに存在するファイルなど、リストア時に不要なデータが含まれる場合があります。このオプションは、新しい読み取りリクエストをオブジェクトストアに送らず、読み取りを続けて不要なデータを読み飛ばします。新しい読み取りリクエストの遅延は、進行中の読み取りを続ける場合より大きいため、通常はこちらの方が高速です。ほとんどのストレージクラスで費用も抑えられます。

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

### リポジトリストレージタグオプション（`--repo-storage-tag`） {#repository-storage-tag-option---repo-storage-tag}

リポジトリストレージのタグです。

リポジトリがオブジェクトストア（例：S3）の場合に、オブジェクトに付加するタグを指定します。このオプションを繰り返して、複数のタグを追加できます。

pgBackRestにはこれらのタグを変更する機能がないため、リポジトリ全体でタグを統一するには、`stanza-create`を実行する前に正しく設定してください。

```yaml
example: --repo1-storage-tag=key1=value1
```

### リポジトリストレージアップロードチャンクサイズオプション（`--repo-storage-upload-chunk-size`） {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

リポジトリストレージのアップロードチャンクサイズです。

S3などのオブジェクトストアでは、ファイルが大きすぎてメモリに格納できない場合に、チャンクに分けてアップロードできます。ファイルをメモリに格納できる場合でも、アップロードに使用するメモリ量を制限する方がメモリ効率は高くなります。

チャンクサイズを大きくすると、アップロードリクエストを最小限に抑え、チャンク分割せずに1回のリクエストでアップロードできるファイルが増えるため、一般にパフォーマンスが向上します。一方、メモリ使用量は増加します。チャンクバッファーはプロセスごとに割り当てる必要があるため、`process-max`の値が大きいほど、全体のメモリ消費量も増えます。

有効なチャンクサイズは、ストレージの種類やプラットフォームによって異なります。たとえば、AWS S3の最小チャンクサイズは5MiBです。チャンクサイズの呼び方もストレージの種類によって異なるため、最小値/最大値を調べる際は、AWS S3では「part size」、GCSでは「chunk size」、Azureでは「block size」を使用してください。

ファイルが1GiB（PostgreSQLがデフォルトで作成する最大サイズ）より大きい場合、ファイルのアップロードを完了するために、許容される最大値までチャンクサイズを段階的に増やします。

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### リポジトリストレージ証明書検証オプション（`--repo-storage-verify-tls`） {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

リポジトリストレージの証明書を検証します。

このオプションでは、ストレージ（例：S3、Azure）サーバーのTLS証明書の検証を有効/無効にできます。無効化は、テストや自己署名証明書を使用する場合に限ってください。

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

非推奨の名前：repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

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

```yaml
default: posix
example: --repo1-type=cifs
```

## stanzaオプション {#stanza-options}

### PostgreSQLパスオプション（`--pg-path`） {#postgresql-path-option---pg-path}

PostgreSQLのデータディレクトリです。

PostgreSQLが報告する`data_directory`と同じ値を設定してください。この値はさまざまな場所から読み取れますが、リストアやオフラインバックアップ時にそれらを利用できない場合に備えて、設定しておくことが賢明です。

`pg-path`オプションは、オンラインバックアップのたびにPostgreSQLが報告する値と照合されるため、常に最新の値であるはずです。

```yaml
example: --pg1-path=/data/db
```

非推奨の名前：db-path
