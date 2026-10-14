---
title: "コマンドリファレンス"
linkTitle: "コマンド"
weight: 40
description: "バックアップ、リストア、アーカイブ、管理操作の全オプションを網羅したpgBackRestのコマンドリファレンス。"
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [リファレンス]
upstream_link: "https://pgbackrest.org/command.html"
---

## はじめに {#introduction}

コマンドは、pgBackRestのさまざまな機能を実行するために使用します。ここでは、各コマンドのオプションを網羅しています。複数のコマンドに適用されるオプションも、該当する各コマンドのページに記載しています。`pgbackrest.conf`で設定できるオプションもすべて含まれます。

`pgbackrest.conf`に設定した非ブール型のオプションは、コマンドラインで`reset-`接頭辞を使用するとデフォルト値に戻せます。この機能を使うと、リポジトリホスト上で直接バックアップをリストアできます。通常、pgBackRestはデータベースホストがリモートにあることを認識し、リモートでのリストアはできないためエラーになります。コマンドラインに`--reset-pg1-host`を追加すると、リモートのデータベースホストを無視してローカルにリストアします。データベースホストで使用していたパスではなく、特定のパスにリストアするには、`--pg1-path`に新しい値を指定する必要がある場合があります。

コマンドラインで`no-`接頭辞を使用すると、ブール型のオプションを偽に設定できます。

すべてのオプションは、`PGBACKREST_`接頭辞に、`-`を`_`に置き換えた大文字のオプション名を続けることで、環境変数に設定できます。たとえば、`pg1-path`は`PGBACKREST_PG1_PATH`、`stanza`は`PGBACKREST_STANZA`になります。ブール型のオプションは、`PGBACKREST_COMPRESS="n"`のように設定ファイルと同じ形式で表し、`reset-*`形式は使用できません。コマンドラインや設定ファイルで複数回指定できるオプションは、`PGBACKREST_DB_INCLUDE="db1:db2"`のように値をコロンで区切って表せます。

コマンドラインのオプションは環境変数のオプションより優先され、環境変数のオプションは設定ファイルのオプションより優先されます。

オプションの型については、[構成の概要](/ja/pgbackrest/configuration/#introduction)を参照してください。

## コマンド {#commands}

| コマンド | 概要 |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [**`annotate`**](/ja/pgbackrest/command/annotate/) | バックアップの作成後に注釈を追加、変更、削除します。 |
| [**`archive-get`**](/ja/pgbackrest/command/archive-get/) | リストア、PITR、レプリカのリカバリーに使用する、アーカイブ済みWALセグメントを取得します。 |
| [**`archive-push`**](/ja/pgbackrest/command/archive-push/) | PostgreSQLからWALセグメントを受け取り、設定したリポジトリに送信します。 |
| [**`backup`**](/ja/pgbackrest/command/backup/) | 対象リポジトリにバックアップを作成します。デフォルトでは最も優先度の高いリポジトリを使用します。 |
| [**`check`**](/ja/pgbackrest/command/check/) | stanzaのバックアップ・アーカイブ設定と、WALアーカイブの正常性を検証します。 |
| [**`expire`**](/ja/pgbackrest/command/expire/) | 設定した保持ポリシーに基づき、バックアップとアーカイブ済みWALを期限切れとして削除します。 |
| [**`help`**](/ja/pgbackrest/command/help/) | 全般、コマンド、オプションの各レベルでヘルプを表示します。 |
| [**`info`**](/ja/pgbackrest/command/info/) | stanzaとバックアップの状態・メタデータをテキストまたはJSON形式で表示します。 |
| [**`repo-get`**](/ja/pgbackrest/command/repo-get/) | 管理、調査、テストのため、`cat`と同様にリポジトリ内のファイルを読み取ります。 |
| [**`repo-ls`**](/ja/pgbackrest/command/repo-ls/) | 管理、調査、テストのため、`ls`と同様にリポジトリ内のファイル・パスを一覧表示します。 |
| [**`restore`**](/ja/pgbackrest/command/restore/) | バックアップからリストアします。デフォルトでは最新のバックアップを使用し、ポイントインタイムリカバリーも指定できます。 |
| [**`server`**](/ja/pgbackrest/command/server/) | SSHを使わずにリモートホストにアクセスするため、pgBackRestのTLSサーバーを実行します。 |
| [**`server-ping`**](/ja/pgbackrest/command/server-ping/) | pgBackRestのTLSサーバーにpingを送信し、接続を受け付けていることを確認します。 |
| [**`stanza-create`**](/ja/pgbackrest/command/stanza-create/) | 設定したすべてのリポジトリにstanzaのメタデータを作成します。 |
| [**`stanza-delete`**](/ja/pgbackrest/command/stanza-delete/) | stanzaのすべてのバックアップとアーカイブを完全に削除します。 |
| [**`stanza-upgrade`**](/ja/pgbackrest/command/stanza-upgrade/) | PostgreSQLのメジャーバージョンアップグレード後にstanzaのメタデータを更新します。 |
| [**`start`**](/ja/pgbackrest/command/start/) | `stop`によって停止したpgBackRestプロセスの実行を再び許可します。 |
| [**`stop`**](/ja/pgbackrest/command/stop/) | 新しいpgBackRestプロセスの実行を禁止し、指定に応じて実行中のプロセスを強制停止します。 |
| [**`verify`**](/ja/pgbackrest/command/verify/) | リポジトリ内のバックアップとアーカイブデータが有効であることを検証します。 |
| [**`version`**](/ja/pgbackrest/command/version/) | インストールされているpgBackRestのバージョンを表示します。 |
{.full-width}
