---
title: "サーバーコマンド（server）"
linkTitle: "server"
weight: 120
description: "pgBackRestの`server`コマンドのオプションと動作のリファレンス。"
icon: fa-solid fa-server
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/command.html#command-server"
---

pgBackRestサーバーは、SSHプロトコルを使用せずにリモートホストにアクセスできるようにします。

## コマンドオプション {#command-options}

### TLSサーバーアドレスオプション（`--tls-server-address`） {#tls-server-address-option---tls-server-address}

TLSサーバーのアドレスです。

サーバーがクライアントのリクエストを待ち受けるIPアドレスです。

```yaml
default: localhost
example: --tls-server-address=*
```

### TLSサーバー認可クライアントオプション（`--tls-server-auth`） {#tls-server-authorized-clients-option---tls-server-auth}

TLSサーバーで認可するクライアントです。

サーバーはクライアントの証明書を検証し、証明書のCN（Common Name）を`tls-server-auth`オプションでサーバーに設定した一覧と照合することで、クライアントを認可します。

`tls-server-auth`オプションにカンマ区切りの一覧を指定すると、クライアントのCNを必要な数のstanzaに対して認可できます。`tls-server-auth=client-cn=*`を指定すると、すべてのstanzaに対して認可できます。クライアントのCNにワイルドカードは指定できません。

```yaml
example: --tls-server-auth=client-cn=stanza1,stanza2
```

### TLSサーバー認証局オプション（`--tls-server-ca-file`） {#tls-server-certificate-authorities-option---tls-server-ca-file}

TLSサーバーの認証局です。

クライアント証明書が信頼できる認証局によって署名されていることを確認します。

```yaml
example: --tls-server-ca-file=/path/to/server.ca
```

### TLSサーバー証明書オプション（`--tls-server-cert-file`） {#tls-server-certificate-option---tls-server-cert-file}

TLSサーバーの証明書ファイルです。

サーバーの身元を示すためにクライアントに送信します。

```yaml
example: --tls-server-cert-file=/path/to/server.crt
```

### TLSサーバーキーオプション（`--tls-server-key-file`） {#tls-server-key-option---tls-server-key-file}

TLSサーバーのキーファイルです。

サーバー証明書が所有者によって送信されたことを証明します。

```yaml
example: --tls-server-key-file=/path/to/server.key
```

### TLSサーバーポートオプション（`--tls-server-port`） {#tls-server-port-option---tls-server-port}

TLSサーバーのポートです。

サーバーがクライアントのリクエストを待ち受けるポートです。

```yaml
default: 8432
allowed: [1, 65535]
example: --tls-server-port=8000
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

### プロセス優先度設定オプション（`--priority`） {#set-process-priority-option---priority}

プロセスの優先度を設定します。

カーネルのスケジューラーがプロセスに与える優先度（niceness）を定義します。正の値は優先度を下げ、負の値は優先度を上げます。通常、プロセスには自身の優先度を上げる権限がありません。

```yaml
allowed: [-20, 19]
example: --priority=19
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

### ログタイムスタンプオプション（`--log-timestamp`） {#log-timestamp-option---log-timestamp}

ログのタイムスタンプを有効にします。

コンソールとファイルのログでタイムスタンプを有効にします。このオプションは、ドキュメント生成などの特殊な状況では無効にします。

```yaml
default: y
example: --no-log-timestamp
```
