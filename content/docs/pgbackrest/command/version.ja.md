---
title: "バージョンコマンド (version)"
linkTitle: "version"
weight: 200
description: "pgBackRestの`version`コマンドのオプションおよび動作に関するリファレンス。"
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [リファレンス]
aliases: [/pgbackrest/command/version/]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

pgBackRestのインストール済みバージョンを表示します。

## コマンドオプション {#command-options}

### 出力オプション (`--output`) {#output-option---output}

出力形式です。

次の出力形式をサポートします。

- `text` - インストールされたpgBackRestのバージョンをテキスト形式で表示します。
- `num` - pgBackRestのインストール済みバージョンを整数で表示します。

```yaml
default: text
example: --output=num
```
