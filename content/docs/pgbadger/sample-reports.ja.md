---
title: "サンプルレポート"
linkTitle: "サンプルレポート"
weight: 80
description: "完全なpgBadgerレポート、エラーのみのレポート、増分レポートを開きます"
search_keywords: [--anonymize, anonymize]
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [リファレンス]
aliases: [/pgbadger/sample-reports/]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

サンプルの内容は2022年5月にpgBadger 11.8で生成されました。レポートのナビゲーション、グラフ、スタイル、スクリプトはオフラインで利用できます。

| サンプル | 紹介する内容 | ローカルコピー |
|---|---|---|
| 完全版レポート | PostgreSQLの動作とPgBouncerの統計 | [完全版レポートを開く](/third_party/pgbadger/examples/sample.html) |
| 増分レポート | カレンダー形式の目次、週次集計、日次ページ | [増分レポートの目次を開く](/third_party/pgbadger/examples/report/index.html) |
| エラーとイベント | エラーと運用イベントに限定したレポート | [エラーレポートを開く](/third_party/pgbadger/examples/errors.html) |

## 完全版レポート {#complete-report}

完全版レポートは自己完結型のHTMLドキュメントです。上部のナビゲーションから、全体統計、クエリー、セッション、接続、一時ファイル、チェックポイント、autovacuumの動作、ロック、PgBouncer専用のグラフを確認できます。

このデータはデモ用であり、現在のベンチマークではありません。値、PostgreSQLのバージョン、埋め込まれたpgBadgerのUIは、レポート生成時点のものです。

## 増分レポートの階層 {#incremental-hierarchy}

増分レポートのサンプルでは、リンク構造を完全に保持しています。

```text
report/
├── index.html
├── 2012/
│   ├── week-49/index.html
│   ├── week-50/index.html
│   └── 12/06 … 12/index.html
└── 11/
    ├── pgbadger.min.css
    ├── pgbadger.min.js
    └── 同梱のグラフとUIのアセット
```

最上位の目次は2つの週次レポートと7つの日次レポートにリンクしています。相対リンクをすべて保持しているため、`index.html`だけを移動するとサンプルが壊れます。ディレクトリツリー全体をまとめて保持してください。

## セキュリティとプライバシー {#security-and-privacy}

実際のレポートには、SQLテキスト、バインド値、データベース名やユーザー名、アプリケーション名、クライアントアドレス、エラーの詳細、ワークロードのパターンが含まれる場合があります。レポートを公開する前に、次を実施してください。

- リテラルが不要な場合は`--anonymize`を使用します。
- レポート生成前に対象の包含・除外フィルターを適用します。
- コマンドラインだけでなく、最終的なHTMLやエクスポートしたデータを確認します。
- レポートの保存場所を、運用ログと同じように慎重に保護します。
