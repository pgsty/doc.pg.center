---
title: "pgBadger 13.2開発スナップショットのドキュメント"
linkTitle: "pgBadger"
weight: 40
description: "PostgreSQLとPgBouncerのログを高速に解析し、詳細で自己完結型のレポートを生成します"
search_keywords: [csvlog, jsonlog, logplex, stderr, syslog]
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [概念]
aliases: [/pgbadger/documentation/]
upstream_source: pgbadger
upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
upstream_link: "https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67"
cascade:
  upstream_source: pgbadger
  upstream_ref: "v13.2 development snapshot, commit f373ac6 (unreleased)"
  type: docs
  module: [PGBADGER]
---

このマニュアルは、[未リリースの開発スナップショット`f373ac6`](https://github.com/darold/pgbadger/tree/f373ac678c756f66a785c5ab4773d1f05f468d67)に基づいています。このコミットは2026-10-21（UTC）のもので、2025-12-29にリリースされた[安定版13.2](https://github.com/darold/pgbadger/releases/tag/v13.2)より後のものです。このスナップショットで説明する機能には、監視モードでのリモート側のフィルタリングや、エンコードされたデータベース別レポートディレクトリなどがあり、これらは13.2のリリースtarballには含まれません。

![pgBadgerロゴ](/img/pgbadger/logo.png "pgBadger")

**pgBadger**は、Perlで書かれた高速な単体動作のPostgreSQLログアナライザーです。PostgreSQLまたはPgBouncerのログを読み取り、詳細なHTML、テキスト、バイナリ、JSON、または生のCSVを出力します。HTMLレポートは自己完結型で、操作や拡大縮小が可能です。閲覧に必要なのはウェブブラウザーだけです。

## pgBadgerを選ぶ理由 {#why-pgbadger}

pgBadgerは、大きなログの解析と運用での利用を想定して設計されています。

- 単一のPerlプログラムであり、Perlコア以外の必須モジュールはありません。
- `stderr`、`syslog`、`csvlog`、`jsonlog`、RDS、Cloud SQL、logplex、Redshift、PgBouncerの入力を自動検出します。
- ローカルファイル、標準入力、SSH経由のリモートファイル、HTTP・FTP・SFTPのURLを直接読み取ります。
- gzip、bzip2、lz4、xz、zip、zstdの圧縮入力に対応します。
- 単一の大きなファイル、または多数の小さなファイルを並列に解析します。
- 日次、週次、および必要に応じた月次の増分レポートを生成します。
- 時刻、データベース、ユーザー、クライアント、アプリケーション、プロセス、セッション、クエリーパターンで絞り込めます。

## レポートの内容 {#report-coverage}

PostgreSQLのレポートには次の内容が含まれます。

- 全体の動作とクエリー統計。
- 低速、高頻度、時間消費の多い、待機中、キャンセルされたクエリー。
- 一時ファイル、チェックポイント、ロック、セッション、接続。
- テーブルごとのautovacuumとautoanalyzeの動作。
- 重大度と分類ごとのエラーとイベント。
- データベース、ユーザー、クライアント、アプリケーション、ステートメント種別ごとの分布。

PgBouncerを入力とする場合は、スループット、平均クエリー実行時間、同時セッション数、接続とセッションの分布、予約プールの使用量、および頻発するエラーとイベントのレポートが加わります。

## ドキュメントの構成 {#documentation-map}

次の順序でマニュアルを読むか、サイドバーから目的の作業へ直接移動してください。

1. pgBadgerとオプションモジュールを[ダウンロードしてインストール](/ja/pgbadger/download/)します。
2. 完全な[コマンドラインリファレンス](/ja/pgbadger/command-line/)を確認します。
3. 解析可能なプレフィックスを使って[PostgreSQLのログ出力](/ja/pgbadger/postgresql-logging/)を設定します。
4. 適切な[並列処理](/ja/pgbadger/parallel-processing/)モードを選択します。
5. [増分レポート](/ja/pgbadger/incremental-reports/)を安全に生成します。
6. [出力形式](/ja/pgbadger/output-formats/)を選び、[ローカルのサンプル](/ja/pgbadger/sample-reports/)を確認します。
7. [リリース履歴](/ja/pgbadger/releases/)、[サポート](/ja/pgbadger/support/)、[ライセンス](/ja/pgbadger/license/)を確認します。

## アップストリームへのリンク {#upstream-links}

- [プロジェクトのウェブサイト](https://pgbadger.darold.net/)
- [ソースコード](https://github.com/darold/pgbadger)
- [リリース](https://github.com/darold/pgbadger/releases)
- [Issueトラッカー](https://github.com/darold/pgbadger/issues)
