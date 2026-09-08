---
title: "ダウンロードとインストール"
linkTitle: "ダウンロードとインストール"
weight: 20
description: "公式リリース、パッケージ、要件、ソースからのインストール"
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [チュートリアル]
aliases: [/docs/pgbadger/download/]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## 配布経路を選ぶ {#distribution-channels}

| 配布経路 | 用途 | 場所 |
|---|---|---|
| 公式リリース | ソースのtarballとリリースノート | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPMパッケージ | RPMを使用するLinuxディストリビューション | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntuパッケージ | APTを使用するLinuxディストリビューション | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| 開発用ソース | 未リリースの最新コード | [darold/pgbadger](https://github.com/darold/pgbadger) |

このサイトのドキュメントスナップショットは、13.2のソースツリーに基づいています。ダウンロード前に必ずリリースページを確認してください。ローカルのスナップショットは意図的に固定されていますが、アップストリームのリリースは引き続き更新されます。

## 要件 {#requirements}

HTMLレポートを使用する場合に必要なのは、次のものだけです。

- 新しいPerlディストリビューション。
- 埋め込みJavaScriptグラフを描画するウェブブラウザー。

オプション機能には、次の依存関係が追加で必要です。

| 機能 | 依存関係 |
|---|---|
| PostgreSQLのCSVログを解析 | `Text::CSV_XS` |
| JSON出力を書き出す | `JSON::XS` |
| `.gz`、`.bz2`、`.lz4`、`.xz`、`.zip`、`.zst`の入力を読む | 対応する`zcat`、`bzcat`、`lz4cat`、`xz`、`unzip`、`zstdcat`ユーティリティー |

DebianまたはUbuntuでJSONサポートをインストールします。

```console
$ sudo apt-get install libjson-xs-perl
```

RPMベースのシステムの場合：

```console
$ sudo yum install perl-JSON-XS
```

展開プログラムのパスを変更するには、`--zcat`を使用します。独自のコマンドを1つ指定すると、同じ実行内で異なる圧縮形式を混在させることはできなくなります。

## 公式tarballからインストールする {#install-from-tarball}

リリースアーカイブをダウンロードし、Perlの標準ツールチェーンでビルドしてインストールします。

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

デフォルトの`site`レイアウトでは、プログラムを`/usr/local/bin/pgbadger`、マニュアルページを`/usr/local/share/man/man1/pgbadger.1`にインストールします。

ディストリビューションと同様に`/usr`配下にインストールする場合は、次のようにMakefileを生成します。

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl`も、アップストリームでサポートされているレイアウトです。管理下のシステムにインストールする前に、生成されるパスを確認してください。

## 開発版のコードをインストールする {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

開発版のコードには、リリースノートにまだ記載されていない変更が含まれる場合があります。本番環境向けのパッケージを再現可能に作成するには、タグ付きのアーカイブを使用してください。

## インストールを確認する {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

続いて、[コマンドラインリファレンス](command-line/)と[PostgreSQLのログ設定](postgresql-logging/)を参照してください。
