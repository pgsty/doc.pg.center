---
title: "ダウンロードとインストール"
linkTitle: "ダウンロードとインストール"
weight: 20
description: "公式リリース、パッケージ、要件、ソースからのインストール"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [チュートリアル]
upstream_link: "https://github.com/darold/pgbadger/blob/0514893e97296695c77755fa36c59288c3afef3e/README.md"
upstream_name: "pgBadger README.md"
---

## 配布経路を選ぶ {#distribution-channels}

| 配布経路 | 用途 | 場所 |
|---|---|---|
| 公式リリース | ソースのtarballとリリースノート | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPMパッケージ | RPMを使用するLinuxディストリビューション | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntuパッケージ | APTを使用するLinuxディストリビューション | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| 開発用ソース | 未リリースの最新コード | [darold/pgbadger](https://github.com/darold/pgbadger) |
{.wide .expand}

2026-11-21に確認した最新の安定版は、2026-11-03にリリースされた[pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3)です。以下のリリースアーカイブの例も、固定チェックアウトも、このドキュメント対象リリースをインストールします。

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

pgBadgerがアーカイブのメタデータを読み取れるよう、`xz`ユーティリティーは`--robot`に対応している必要があります。lz4ログは`--content-size`を指定して圧縮してください。これにより、pgBadgerが非圧縮時のサイズを判断できます。

## 公式tarballからインストールする {#install-from-tarball}

リリースアーカイブをダウンロードし、Perlの標準ツールチェーンでビルドしてインストールします。

```console
$ tar xzf pgbadger-13.3.tar.gz
$ cd pgbadger-13.3
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

## 固定ソースからインストールする {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach 0514893e97296695c77755fa36c59288c3afef3e
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

このチェックアウトは、[ドキュメント対象のv13.3リリース](https://github.com/darold/pgbadger/releases/tag/v13.3)に対応し、`0514893e97296695c77755fa36c59288c3afef3e`に固定されています。
## インストールを確認する {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

続いて、[コマンドラインリファレンス](/ja/pgbadger/command-line/)と[PostgreSQLのログ設定](/ja/pgbadger/postgresql-logging/)を参照してください。
