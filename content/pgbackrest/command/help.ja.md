---
title: "ヘルプコマンド (help)"
linkTitle: "help"
weight: 70
description: "pgBackRestの`help`コマンドのオプションおよび動作に関するリファレンス。"
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/command.html#command-help"
---

3つのレベルのヘルプが用意されています。コマンドが指定されない場合は、一般のヘルプが表示されます。コマンドが指定された場合（例：`pgbackrest help backup`）、そのコマンドの詳細な説明と有効なオプションの一覧が表示されます。コマンドに加えてオプションが指定された場合（例：`pgbackrest help backup type`）、そのオプションがコマンドに適用される際の詳細な説明が表示されます。

## コマンドオプション {#command-options}

### ヘルプ表示オプション (`--help`) {#display-help-option---help}

ヘルプを表示します。

ヘルプを表示します。`help`コマンドが指定されていなくても同様に機能し、`--version`オプションを上書きします。

```yaml
default: n
example: --help
```

### バージョン表示オプション (`--version`) {#display-version-option---version}

バージョンを表示します。

バージョン情報を表示します。`version`または`help`コマンドが指定されていなくても同様です。

```yaml
default: n
example: --version
```
