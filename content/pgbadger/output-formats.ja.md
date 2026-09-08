---
title: "出力形式"
linkTitle: "出力形式"
weight: 70
description: "HTML、テキスト、バイナリ、JSON、生のCSVから出力形式を選び、中間ファイルを統合します"
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [リファレンス]
aliases: [/docs/pgbadger/output-formats/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadgerは、ファイル名の拡張子または`-x` / `--extension`から出力形式を選びます。`-o` / `--outfile`を複数回指定すると、1回の解析から複数形式を生成できます。

| 形式 | 一般的な拡張子 | 主な用途 |
|---|---|---|
| HTML | `.html` | グラフ付きで、人が読みやすく操作可能なレポート |
| テキスト | `.txt` | ターミナルでの確認とプレーンテキストによる保存 |
| バイナリ | `.bin` | 統合可能な中間統計とレポートの再生成 |
| JSON | `.json` | 他のソフトウェアとの連携。`JSON::XS`が必要 |
| 生のCSV | 選択した出力ファイル | `--dump-raw-csv`による行単位の抽出 |

## HTMLとテキスト {#html-and-text}

デフォルトの出力先は`out.html`です。

```console
$ pgbadger postgresql.log -o report.html
```

通常、HTMLには単独での閲覧に必要なスクリプト、スタイル、フォント、レポートデータが埋め込まれます。`-X` / `--extra-files`を指定すると、共通のJavaScriptとCSSを増分レポートの外に配置します。これらのアセットはHTMLのディレクトリツリーとともに保持してください。

テキスト出力を明示的に生成します。

```console
$ pgbadger -x text -o report.txt postgresql.log
```

出力ファイル名に`-`を指定すると、対応する形式を標準出力に書き出せます。

## バイナリの中間データ {#binary-format}

バイナリ出力では、解析と表示を分離します。追記され続ける1日分のログから、1時間ごとの差分を生成できます。

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

1つ以上のバイナリファイルを統合して、新しいレポートを生成します。

```console
$ pgbadger -o sunday.html sunday/*.bin
```

サーバーが1時間ごとにログファイルを作成する場合は、ローテーションごとにバイナリファイルを作成し、必要に応じて累積HTMLを再生成します。

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

互換性のあるpgBadgerバージョンのバイナリファイルをまとめて保持してください。長期間使用しているレポートディレクトリをアップグレードする前に、リリースノートで増分形式の互換性を確認してください。

## JSON {#json-format}

JSON出力は、監視やレポート処理パイプラインなどのプログラムによる利用を想定しています。

```console
$ pgbadger -o report.json postgresql.log
```

まず`JSON::XS`をインストールしてください。ファイルサイズや生成時間より読みやすさを優先する場合は、`--prettify-json`を追加します。

## 生データとクエリーのエクスポート {#raw-exports}

コマンドリファレンスでは、専用のエクスポート機能も提供されています。

- `--dump-raw-csv`はログを解析し、レポートを生成せずに行単位のCSVを書き出します。
- `--csv-separator`は生のCSVの区切り文字を変更します。
- `--dump-all-queries`はバインドパラメーターを置換した後のすべてのクエリーを出力します。
- `--normalized-only`は正規化したクエリーを書き出します。
- `--query-numbering`はクエリーのテキスト出力に番号を付けます。

これらのモードの出力には、アプリケーションのSQL、識別子、ユーザー、クライアントアドレス、リテラル値が含まれる場合があります。共有前に出力を確認し、目的の分析にリテラルが不要であれば`--anonymize`を使用してください。
