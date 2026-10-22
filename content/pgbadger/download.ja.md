---
title: "ダウンロードとインストール"
linkTitle: "ダウンロードとインストール"
weight: 20
description: "公式リリース、パッケージ、要件、ソースからのインストール"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [チュートリアル]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

## 配布経路を選ぶ {#distribution-channels}

| 配布経路 | 用途 | 場所 |
|---|---|---|
| 公式リリース | ソースのtarballとリリースノート | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPMパッケージ | RPMを使用するLinuxディストリビューション | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntuパッケージ | APTを使用するLinuxディストリビューション | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| 開発用ソース | 未リリースの最新コード | [darold/pgbadger](https://github.com/darold/pgbadger) |

2026-10-23時点で確認した最新の安定版は、2025-12-29にリリースされた[pgBadger 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2)です。以下のリリースtarballを使う例では、このバージョンをインストールします。このマニュアルは未リリースの開発スナップショットも対象にしています。新しい動作を再現するには、以下の特定コミットに固定したチェックアウトを使用してください。

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
$ git checkout --detach f373ac678c756f66a785c5ab4773d1f05f468d67
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

このチェックアウトは、ここで説明している未リリースの開発スナップショット[`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67)に対応します。コミット日時は2026-10-21（UTC）です。安定版13.2より新しいものですが、新たな安定版ではありません。開発版のコードには、リリースノートにまだ記載されていない変更が含まれる場合があります。本番環境向けのパッケージ作成には、タグ付きのアーカイブを優先してください。

## インストールを確認する {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

続いて、[コマンドラインリファレンス](/ja/pgbadger/command-line/)と[PostgreSQLのログ設定](/ja/pgbadger/postgresql-logging/)を参照してください。
