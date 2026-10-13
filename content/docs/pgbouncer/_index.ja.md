---
title: "PgBouncer 1.26.0 ドキュメント"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer - PostgreSQL 用の軽量コネクションプーラー
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [概念]
aliases: [/pgbouncer/]
upstream_source: pgbouncer
upstream_ref: v1.26.0
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  upstream_ref: v1.26.0
  type: docs
  module: [PGBOUNCER]
---

本マニュアルは、2026-09-23 にリリースされた [PgBouncer 1.26.0](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0) に基づいています。以前のバージョンからの変更点については、[リリースノート](/ja/docs/pgbouncer/changelog/#pgbouncer-126x)を参照してください。

**pgbouncer** は PostgreSQL のコネクションプーラーです。任意の対象アプリケーションは、PostgreSQL サーバーと同じように **pgbouncer** に接続できます。**pgbouncer** は、実際のサーバーへの接続を作成するか、既存の接続を再利用します。

**pgbouncer** の目的は、PostgreSQL への新しい接続を開く際のパフォーマンスへの影響を低減することです。

コネクションプーリングのトランザクションセマンティクスを損なわないようにするため、**pgbouncer** は接続をローテーションする際に複数のプーリング方式をサポートしています。

- **セッションプーリング**: 最も丁寧な方法です。クライアントが接続すると、クライアントが接続を維持している間はサーバー接続が割り当てられます。クライアントが切断すると、サーバー接続はプールに戻されます。これがデフォルトの方法です。
- **トランザクションプーリング**: サーバー接続は、トランザクション中のみクライアントに割り当てられます。PgBouncer がトランザクションの終了を検知すると、サーバー接続はプールに戻されます。
- **ステートメントプーリング**: 最も攻撃的な方法です。クエリの実行が完了すると、サーバー接続はすぐにプールに戻されます。このモードではマルチステートメントトランザクションは許可されません。
