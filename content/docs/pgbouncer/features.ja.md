---
title: "機能"
weight: 10
description: "PgBouncer の機能 — プーリングモードと SQL 向け互換性"
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
  : クライアントにサーバー接続が割り当てられるのは、トランザクション中に限られます。PgBouncer がトランザクションの終了を検知すると、サーバーはプールに戻されます。このモードでは、PostgreSQL のセッションベースの機能の一部が動作しなくなります。アプリケーションが、破損を引き起こす機能を使用しないよう協力する場合にのみ利用できます。互換性のない機能については、以下の表を参照してください。

  **ステートメントプーリング**
  : 最も攻撃的な方法です。これはトランザクションプーリングの一種ですが、複数文のトランザクションを許可しない点が特徴です。これはクライアント上で「autocommit」モードを強制することを目的としており、主に PL/Proxy を対象としています。

- メモリ要件が低く（デフォルトで接続あたり 2 kB）、これは PgBouncer が一度に完全なパケットを確認する必要がないためです。

- 単一のバックエンドサーバーに固定されません。接続先データベースは異なるホストに配置できます。

- ほとんどの設定をオンラインで再構成できます。

- クライアント接続を切断せずにオンラインで再起動またはアップグレードできます。

--------

## プーリングモードのSQL機能マップ {#sql-feature-map-for-pooling-modes}

次の表は、さまざまな PostgreSQL 機能と PgBouncer のプールモードとの互換性を示しています。注意してください。「トランザクション」プールモードは、*設計上* サーバーに対するクライアントの期待を破るため、アプリケーションが非対応機能を使用しないよう協力する場合にのみ使用可能です。

| 機能                             | セッションプーリング       | トランザクションプーリング       |
|----------------------------------|:--------------------------:|:----------------------------------:|
| スタートアップパラメータ [^0] | はい                       | はい                               |
| SET/RESET                        | はい                       | いいえ                             |
| LISTEN                           | はい                       | いいえ                             |
| NOTIFY                           | はい                       | はい                               |
| WITHOUT HOLD カーソル            | はい                       | はい                               |
| WITH HOLD カーソル               | はい                       | いいえ                             |
| プロトコルレベルのプリペアドプラン | はい                       | はい [^1]                 |
| PREPARE / DEALLOCATE             | はい                       | いいえ                             |
| ON COMMIT DROP 一時テーブル      | はい                       | はい                               |
| PRESERVE/DELETE ROWS 一時テーブル | はい                       | いいえ                             |
| キャッシュプランのリセット       | はい                       | はい                               |
| LOAD ステートメント              | はい                       | いいえ                             |
| セッションレベルのアドバイザリロック | はい                       | いいえ                             |

[^0]: 起動パラメータは、`client_encoding`、`DateStyle`、`IntervalStyle`、`Timezone`、`standard_conforming_strings`、および `application_name` です。PgBouncer はこれらの変更を検出できるため、クライアントに対して一貫性を保証できます。これらのパラメータを超えて PgBouncer がサポートする必要がある場合は、[`track_extra_parameters`](/ja/docs/pgbouncer/config/#track_extra_parameters) および [`ignore_startup_parameters`](/ja/docs/pgbouncer/config/#ignore_startup_parameters) を参照してください。

[^1]: この機能を有効にするには、[`max_prepared_statements`](/ja/docs/pgbouncer/config/#max_prepared_statements) を 0 以外の値に変更する必要があります。
