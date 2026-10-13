---
title: "停止コマンド（stop）"
linkTitle: "stop"
weight: 180
description: "pgBackRestの`stop`コマンドのオプションと動作のリファレンス。"
icon: fa-solid fa-stop
module: [PGBACKREST]
categories: [リファレンス]
aliases: [/pgbackrest/command/stop/]
upstream_link: "https://pgbackrest.org/command.html#command-stop"
---

新しいpgBackRestプロセスの実行を許可しません。デフォルトでは、実行中のプロセスは正常に完了するまで継続できます。実行中のプロセスを終了するには、`--force`オプションを使用します。

stopコマンドの完了後にpgBackRestプロセスを実行すると、エラーが返されます。詳細と例は、[開始と停止](/ja/docs/pgbackrest/user-guide/#starting-and-stopping)を参照してください。

## コマンドオプション {#command-options}

### 強制オプション（`--force`） {#force-option---force}

すべてのpgBackRestプロセスを強制的に停止します。

このオプションは、実行中のすべてのpgBackRestプロセスにTERMシグナルを送信し、終了処理を行って直ちに停止させます。別のシステムで開始され、現在のシステム上でリモートプロセスが動作しているプロセスも停止します。たとえば、バックアップサーバーでバックアップを開始した後、データベースサーバーで`stop --force`を実行すると、バックアップサーバー上のバックアッププロセスも停止します。

```yaml
default: n
example: --force
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

### stanzaオプション（`--stanza`） {#stanza-option---stanza}

stanzaを定義します。

stanzaは、PostgreSQLデータベースクラスターの場所、バックアップ方法、アーカイブオプションなどを定義する設定です。ほとんどのデータベースサーバーにはPostgreSQLデータベースクラスターが1つだけ存在し、stanzaも1つになります。一方、バックアップサーバーには、バックアップが必要なデータベースクラスターごとにstanzaがあります。

stanzaにはプライマリークラスターにちなんだ名前を付けたくなりますが、クラスターに含まれるデータベースを表す名前の方が適しています。stanza名はプライマリーとすべてのレプリカで使用するため、mainやprodなどのローカルクラスター名よりも、appやdwなど、クラスターの実際の役割を表す名前を選ぶ方が適切です。

```yaml
example: --stanza=main
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
