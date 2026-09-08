---
title: "バージョン コマンド (version)"
linkTitle: "version"
weight: 200
description: "pgBackRest `version` コマンドのオプションおよび動作に関するリファレンス。"
icon: fa-solid fa-tag
module: [PGBACKREST]
categories: [リファレンス]
aliases: [/docs/pgbackrest/command/version/]
upstream_link: "https://pgbackrest.org/command.html#command-version"
---

pgBackRest のインストール済みバージョンを表示します。

## コマンドオプション {#command-options}

### 出力オプション (`--output`) {#output-option---output}

出力形式。

次の出力形式がサポートされています：

- `text` - インストールされた pgBackRest のバージョンをテキスト形式で表示します。
- `num` - pgBackRest のインストール済みバージョンを整数で表示します。

```yaml
default: text
example: --output=num
```
