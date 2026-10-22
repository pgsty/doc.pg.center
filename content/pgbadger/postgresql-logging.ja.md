---
title: "PostgreSQLのログ設定"
linkTitle: "PostgreSQLのログ"
weight: 40
description: "pgBadger用にクエリーログ、log_line_prefix、ロケール、関連する統計を設定します"
search_keywords: [--prefix, lc_messages, log_autovacuum_min_duration, log_checkpoints, log_connections, log_disconnections, log_duration, log_error_verbosity, log_line_prefix, log_lock_waits, log_min_duration_statement, log_statement, log_temp_files, prefix, stderr, syslog]
icon: fa-solid fa-database
module: [PGBADGER]
categories: [タスク]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadgerでレポートできるのは、PostgreSQLがログに書き出した情報だけです。まず解析可能なプレフィックスと、目的に応じたステートメントのログ出力方針を設定し、次に分析したい運用イベントを追加してください。

## クエリーログの最小構成 {#minimum-query-logging}

クエリー本文と実行時間を記録するには、実行時間に基づくステートメントのログ出力を有効にします。

```postgresql
log_min_duration_statement = 0
```

`0`を指定すると、完了したすべてのステートメントが記録されます。負荷の高いサーバーでは、ログ量を抑えるためにミリ秒単位のしきい値を高く設定してください。本番環境で低いしきい値を有効にする前に、処理負荷とストレージ使用量の増加を測定してください。

クエリー本文が不要で、実行時間とクエリー数だけが必要な場合は、次を使用します。

```postgresql
log_min_duration_statement = -1
log_duration = on
```

最も遅いクエリーやクエリーの合計実行時間のレポートが必要な場合は、`log_min_duration_statement`を使用してください。

## 必須のプレフィックスフィールド {#required-prefix-fields}

独自の`log_line_prefix`には、次の両方を含める必要があります。

- 時刻フィールド：`%t`、`%m`、または`%n`。
- プロセスまたはセッションのフィールド：`%p`または`%c`。

最小限の`stderr`用プレフィックスは次のとおりです。

```postgresql
log_line_prefix = '%t [%p]: '
```

ユーザー、データベース、アプリケーション、クライアントも記録すると、より有用なプレフィックスになります。

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

出力先がsyslogの場合、同等のプレフィックスでは、syslog自身が付与するタイムスタンプとプロセスのフィールドを省略します。

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

次のキーの順序もサポートされています。

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

プレフィックスがpgBadgerで認識される形式に該当しない場合は、正確な値を`--prefix`で渡してください。簡略化したり、`postgresql.conf`と異なる値を入力し直したりしないでください。

## 推奨するイベント設定 {#recommended-event-settings}

レポートに含めたいイベントの種類を有効にします。

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

これらの設定により、大量のログが出力される場合があります。特に`log_temp_files = 0`と`log_autovacuum_min_duration = 0`では、該当するすべてのイベントを記録します。ワークロードと保持容量に合わせて調整してください。

## サーバーメッセージを英語にする {#message-locale}

パーサーは英語のPostgreSQLサーバーメッセージを認識します。次のいずれかを使用してください。

```postgresql
lc_messages = 'en_US.UTF-8'
```

または：

```postgresql
lc_messages = 'C'
```

`fr_FR.UTF-8`などのロケールは、アップストリームのパーサーではサポートされていません。

## ステートメント設定の競合を避ける {#statement-setting-conflicts}

`log_min_duration_statement`、`log_duration`、`log_statement = 'all'`を同時に有効にしないでください。同じ実行が複数回記録されると、pgBadgerのカウンターが過大になり、ログ量も大幅に増加します。

| 目的 | 推奨設定 |
|---|---|
| クエリー本文と実行時間 | `log_min_duration_statement = 0`または目的に応じたしきい値 |
| 実行時間と件数のみ | `log_min_duration_statement = -1`、`log_duration = on` |
| 幅広いステートメント監査 | `log_statement`を独立したログ方針として扱い、pgBadgerの統計のために3つの設定をすべて組み合わせないでください |

PostgreSQLの設定を再読み込みした後、大規模な解析を実行する前に実際のログを数件確認してください。タイムスタンプ、プロセス・セッション識別子、ユーザー、データベース、アプリケーション、クライアントの各フィールドが選択した形式と一致することを確認します。
