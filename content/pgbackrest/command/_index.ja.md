---
title: "コマンドリファレンス"
linkTitle: "コマンド"
weight: 40
description: "バックアップ、復元、アーカイブ、および管理操作のすべてのオプションを含む pgBackRest コマンド リファレンス。"
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [リファレンス]
aliases: [/docs/pgbackrest/command/]
upstream_link: "https://pgbackrest.org/command.html"
---

## 導入 {#introduction}

コマンドは、さまざまな pgBackRest 関数を実行するために使用されます。ここでは、コマンド オプションが網羅的にリストされています。つまり、コマンドに適用される各オプションは、1 つ以上の他のコマンドに適用される場合でも、そのコマンドとともにリストされます。これには、`pgbackrest.conf` で構成できるすべてのオプションが含まれます。

`pgbackrest.conf` で構成された非ブール型オプションは、`reset-` プレフィックスを使用してコマンドラインでデフォルトにリセットできます。この機能は、バックアップをリポジトリ ホストに直接復元するために使用できます。通常、pgBackRest はデータベース ホストがリモートにあり、復元をリモートで実行できないことがわかるため、エラーが発生します。コマンドラインに `--reset-pg1-host` を追加すると、pgBackRest はリモート データベース ホストを無視し、ローカルに復元します。特定のパス (データベース ホストで使用されているパスではない) で復元を強制的に実行するには、新しい `--pg1-path` を渡すことが必要な場合があります。

`no-` プレフィックスは、コマンドラインでブール型オプションを false に設定するために使用できます。

`PGBACKREST_` プレフィックスと、`-` を `_` に置き換えるすべて大文字のオプション名を使用して、任意のオプションを環境変数に設定できます。 `pg1-path` は `PGBACKREST_PG1_PATH` になり、`stanza` は `PGBACKREST_STANZA` になります。ブール値オプションは、設定ファイル内にあるものと同じように表現されます。 `PGBACKREST_COMPRESS="n"` および `reset-*` のバリアントは許可されません。コマンドラインまたは構成ファイルで複数回指定できるオプションは、値をコロンで区切ることで表すことができます。 `PGBACKREST_DB_INCLUDE="db1:db2"`。

コマンドライン オプションは、構成ファイル オプションをオーバーライドする環境オプションをオーバーライドします。

オプションの種類については、[構成の概要](/ja/pgbackrest/configuration/#introduction)を参照してください。

## コマンド {#commands}

|コマンド |概要 |
|-----------------------------------------------------------------|------------------------------------------------------------------------------------|
| [**`annotate`**](/ja/pgbackrest/command/annotate/) |バックアップの作成後に、バックアップの注釈を追加、変更、または削除します。                  |
| [**`archive-get`**](/ja/pgbackrest/command/archive-get/) |復元、PITR、またはレプリカのリカバリのために、アーカイブされた WAL セグメントをフェッチします。                     |
| [**`archive-push`**](/ja/pgbackrest/command/archive-push/) | PostgreSQL から WAL セグメントを受け入れ、構成されたリポジトリにプッシュします。           |
| [**`backup`**](/ja/pgbackrest/command/backup/) |ターゲット リポジトリ (デフォルトでは最も優先度の高いリポジトリ) にバックアップを作成します。      |
| [**`check`**](/ja/pgbackrest/command/check/) |スタンザのバックアップ/アーカイブ構成と WAL アーカイブの健全性を検証します。                  |
| [**`expire`**](/ja/pgbackrest/command/expire/) |構成された保持ポリシーに基づいて、バックアップとアーカイブされた WAL を期限切れにします。                 |
| [**`help`**](/ja/pgbackrest/command/help/) |コマンドおよびオプションのヘルプを一般、コマンド、またはオプションのレベルで表示します。                      |
| [**`info`**](/ja/pgbackrest/command/info/) |スタンザとバックアップのステータス/メタデータをテキストまたは JSON 形式で表示します。                       |
| [**`repo-get`**](/ja/pgbackrest/command/repo-get/) |管理、調査、テストのためにリポジトリ ファイル (`cat` など) を読み取ります。      |
| [**`repo-ls`**](/ja/pgbackrest/command/repo-ls/) |管理、調査、テストのためにリポジトリ ファイル/パス (`ls` など) をリストします。 |
| [**`restore`**](/ja/pgbackrest/command/restore/) |オプションのポイントインタイムリカバリを使用して、バックアップ (デフォルトでは最新) から復元します。           |
| [**`server`**](/ja/pgbackrest/command/server/) | SSH を使用しないリモート ホスト アクセスには、pgBackRest TLS サーバーを実行します。                       |
| [**`server-ping`**](/ja/pgbackrest/command/server-ping/) | pgBackRest TLS サーバーに ping を実行して、接続が受け入れられていることを確認します。                     |
| [**`stanza-create`**](/ja/pgbackrest/command/stanza-create/) |構成されているすべてのリポジトリにスタンザ メタデータを作成します。                                  |
| [**`stanza-delete`**](/ja/pgbackrest/command/stanza-delete/) |スタンザのすべてのバックアップとアーカイブを完全に削除します。                               |
| [**`stanza-upgrade`**](/ja/pgbackrest/command/stanza-upgrade/) | PostgreSQL メジャー バージョンのアップグレード後にスタンザ メタデータをアップグレードします。                       |
| [**`start`**](/ja/pgbackrest/command/start/) |前回の `stop` の後に pgBackRest プロセスが実行できるようにします。                           |
| [**`stop`**](/ja/pgbackrest/command/stop/) |新しい pgBackRest プロセスを防止し、オプションで実行中のプロセスを強制停止します。                |
| [**`verify`**](/ja/pgbackrest/command/verify/) |リポジトリ内のバックアップおよびアーカイブ データが有効であることを確認します。                         |
| [**`version`**](/ja/pgbackrest/command/version/) |インストールされている pgBackRest のバージョンを表示します。                                               |
{.full-width}
