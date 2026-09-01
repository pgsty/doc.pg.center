---
title: "PgBouncer 1.25.2 ドキュメント"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer - PostgreSQL 専用の軽量コネクションプーラー
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [概念]
aliases: [/docs/pgbouncer/]
upstream_source: pgbouncer
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  type: docs
  module: [PGBOUNCER]
---

**pgbouncer** は PostgreSQL のコネクションプーラーです。任意の対象アプリケーションは、実際のサーバーのように **pgbouncer** に接続できます。このとき、**pgbouncer** は実際に接続先のサーバーに接続するか、既存の接続を再利用します。

**pgbouncer** の目的は、PostgreSQL への新しい接続を開く際のパフォーマンスへの影響を低減することです。

接続プールのトランザクションセマンティクスを損なわないようにするため、**pgbouncer** は接続をローテーションする際に複数のプール方式をサポートしています。

- **セッションプーリング**: 最も丁寧な方法です。クライアントが接続すると、クライアントが接続を維持している間はサーバー接続が割り当てられます。クライアントが切断すると、サーバー接続はプールに戻されます。これがデフォルトの方法です。
- **トランザクションプーリング**: サーバー接続は、クライアントがトランザクションを実行している間のみ割り当てられます。PgBouncer がトランザクションの終了を検知すると、サーバー接続はプールに戻されます。
- **ステートメントプーリング**: 一番攻撃的な方法です。クエリの実行が完了すると、サーバー接続はすぐにプールに戻されます。このモードではマルチステートメントトランザクションは許可されません。
