---
title: "増分レポート"
linkTitle: "増分レポート"
weight: 60
description: "日次・週次レポートの生成、保持期間の管理、出力の再生成、月次集計の追加を行います"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [タスク]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

増分モードでは、解析した統計をバイナリ形式で保存し、1日ごとのHTMLレポート、1週間ごとの累積レポート、およびそれらを結ぶカレンダー形式の目次を生成します。同じログエントリーを重複して数えずに、ローテーションされたログを繰り返し処理するための機能です。

## 日次・週次レポートを生成する {#daily-and-weekly}

日次のログローテーション後にpgBadgerを実行し、永続的な出力ディレクトリを指定します。

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I`は増分モードを有効にし、`-O`はバイナリ状態、カレンダーの目次、生成したレポートを保持するディレクトリを指定します。pgBadgerはそのディレクトリに増分処理の状態を維持するため、状態ファイルを意図的に別の場所に置きたい場合を除き、`--last-parsed`は不要です。

バイナリ状態を元のディレクトリに保持しつつ、HTMLには別のディレクトリを使用できます。

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

バイナリファイルは、将来の再生成に使用する元データとして扱ってください。レポートの再生成が重要な場合は、これらをバックアップするか、元のログを保持してください。

## 保持期間 {#retention}

指定した週数分だけを保持します。

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

それより古い週や日のディレクトリは自動的に削除されます。唯一のレポート履歴にこの方針を適用する前に、本番以外のコピーでテストしてください。

## 共通アセットを別ファイルに書き出す {#shared-assets}

デフォルトでは、HTMLレポートにJavaScriptとCSSが埋め込まれます。多数の増分レポートを含むディレクトリでは、`-X` / `--extra-files`を指定すると共通アセットを別に書き出し、出力の重複を減らせます。

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

すべてのレポートと、バージョン別のリソースディレクトリを一緒に移動する必要があります。

## 既存レポートを再生成する {#rebuild}

pgBadgerのアップグレード後、またはレポート生成の修正を適用した後は、保持しているバイナリデータからHTMLを再生成します。

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

元のレポートをデータベースごとに生成した場合は、再度`-E` / `--explode`を指定してください。

> 長いオプション名の`--rebuild`を使用してください。現在のコマンドリファレンスでは、`-R`は`--retention`を意味します。`-R`を再生成の短縮オプションとして扱うと、誤ったオプションが適用されます。

## 月次レポートを追加する {#monthly-reports}

日次・週次レポートは自動的に生成されます。月次集計は、履歴が大きいと処理コストが高くなるため、明示的に実行します。

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

生成した月がカレンダーの目次に追加されます。同じコマンドを再実行すると、利用可能なバイナリデータからその月を再生成します。データベース別の履歴を対象とする場合は、再度`-E`を指定してください。

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

完全なコマンドリファレンスには、より特殊なスケジュールに対応する`--day-report YYYY-MM-DD`、`--no-week`、`--noreport`、`--start-monday`、`--iso-week-number`も記載されています。

同梱の[増分レポートのサンプル](/third_party/pgbadger/examples/report/index.html)を開くと、ネットワーク接続なしでカレンダー、週へのリンク、日次レポートの階層を確認できます。
