---
title: "機能"
weight: 10
description: "PgBouncer の機能 — プーリングモードと SQL 互換性"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [概念]
aliases: [/pgbouncer/features/]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- 接続をローテートする際の幾つかのレベルの厳しさ：

  **セッションプーリング**
  : 最も丁寧な方法です。クライアントが接続すると、そのクライアントが接続を維持している間は、サーバー接続が常に割り当てられます。クライアントが切断すると、そのサーバー接続はプールに戻されます。このモードは、すべての PostgreSQL 機能をサポートしています。

  **トランザクションプーリング**
  : クライアントにサーバー接続が割り当てられるのは、トランザクション中に限られます。PgBouncer がトランザクションの終了を検知すると、サーバーはプールに戻されます。このモードでは、PostgreSQL のセッションベースの機能の一部が動作しなくなります。アプリケーションが、動作しない機能を使用しないよう協力する場合にのみ利用できます。互換性のない機能については、以下の表を参照してください。

  **ステートメントプーリング**
  : 最も攻撃的な方法です。これはトランザクションプーリングの一種ですが、複数文のトランザクションを許可しない点が特徴です。これはクライアント上で「autocommit」モードを強制することを目的としており、主に PL/Proxy を対象としています。

- メモリ要件が低く（デフォルトで接続あたり 2 kB）、これは PgBouncer が一度に完全なパケットを確認する必要がないためです。

- 単一のバックエンドサーバーに固定されません。接続先データベースは異なるホストに配置できます。

- ほとんどの設定をオンラインで再構成できます。

- [`so_reuseport`](/ja/docs/pgbouncer/config/#so_reuseport) を使った複数プロセスによる[ローリング再起動およびアップグレード](/ja/docs/pgbouncer/usage/#shutdown-wait_for_clients)をサポートしています。従来のオンライン再起動（`-R`）は 1.26.0 で削除されました。

--------

## プーリングモードのSQL機能マップ {#sql-feature-map-for-pooling-modes}

次の表は、さまざまな PostgreSQL 機能と PgBouncer のプーリングモードとの互換性を示しています。なお、「トランザクション」プーリングは*設計上*、サーバーに対するクライアントの期待を破るものであり、アプリケーションが動作しない機能を使用しないよう協力する場合にのみ使用できます。

| 機能                             | セッションプーリング       | トランザクションプーリング       |
|----------------------------------|:--------------------------:|:----------------------------------:|
| スタートアップパラメータ [^0] | はい                       | はい                               |
| SET/RESET                        | はい                       | 追跡対象のパラメータの場合 [^0] |
| LISTEN                           | はい                       | 不可                               |
| NOTIFY                           | はい                       | はい                               |
| WITHOUT HOLD カーソル            | はい                       | はい                               |
| WITH HOLD カーソル               | はい                       | 不可                               |
| プロトコルレベルのプリペアドプラン | はい                       | はい [^1]                 |
| PREPARE / DEALLOCATE             | はい                       | 不可                               |
| ON COMMIT DROP 一時テーブル      | はい                       | はい                               |
| PRESERVE/DELETE ROWS 一時テーブル | はい                       | 不可                               |
| キャッシュプランのリセット       | はい                       | はい                               |
| LOAD ステートメント              | はい                       | 不可                               |
| セッションレベルのアドバイザリロック | はい                       | 不可                               |

[^0]: 1.26.0 以降、PgBouncer はクライアントが変更可能な、サーバーが報告するすべてのパラメータを追跡します：`application_name`、`client_encoding`、`DateStyle`、`default_transaction_read_only`（PostgreSQL 14+）、`IntervalStyle`、`scram_iterations`（PostgreSQL 16+）、`search_path`（PostgreSQL 18+）、`session_authorization`、`standard_conforming_strings`、`TimeZone`。サーバーが報告しないパラメータについては、スタートアップ値のみが追跡され、後続の `SET` による変更は追跡されません。詳細および拡張機能が提供するパラメータについては、[`track_extra_parameters`](/ja/docs/pgbouncer/config/#track_extra_parameters) および [`ignore_startup_parameters`](/ja/docs/pgbouncer/config/#ignore_startup_parameters) を参照してください。

[^1]: プロトコルレベルのプリペアドステートメントのサポートは、[`max_prepared_statements`](/ja/docs/pgbouncer/config/#max_prepared_statements) が 0 以外の値に設定されている場合に有効になります。デフォルトは 200 であり、0 に設定するとこのサポートは無効になります。SQL レベルの `PREPARE` / `DEALLOCATE` は、追跡が有効になっている場合の `DEALLOCATE ALL` と `DISCARD ALL` を除き、トランザクションプーリングとは互換性がありません。
