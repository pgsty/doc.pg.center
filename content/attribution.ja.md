---
title: "帰属とライセンス"
linkTitle: "帰属"
description: "このサイトの各ページの出典、著作権者、ライセンス、および完全な通知の保存場所。"
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

PG.CENTERは、6つのアップストリームプロジェクトが作成したドキュメントを再公開しています。各ドキュメントページの末尾には、原著作物、著作権者、ライセンス、およびこのページの該当セクションへのリンクを記載した1行の帰属表示があります。

このページはその記録です。何を、いつ、どの固定リビジョンから、どのライセンスのもとでインポートしたか、また完全なアップストリームの通知をどこに保存しているかを示します。

> [!NOTE]
> PG.CENTERは独立したコミュニティドキュメントプロジェクトです。以下の各プロジェクトやPostgreSQL Global Development Groupとの提携や承認を示すものではなく、それらの公式出版物でもありません。

## 概要 {#summary}

| コンポーネント | アップストリームの著作物 | 固定バージョン | ライセンス | 保存されている通知 |
|---|---|---|---|---|
| [Patroni](/ja/patroni/) | [Patroniドキュメント](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [アップストリームの`LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ja/pgbackrest/) | [pgBackRestドキュメント](https://pgbackrest.org/) | v2.59.3 | [MIT](https://opensource.org/license/mit) | [アップストリームの`LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ja/pgbouncer/) | [PgBouncerドキュメント](https://www.pgbouncer.org/) | v1.26.0 | [ISC](https://opensource.org/license/isc-license-txt) | [アップストリームの`COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/ja/pgbadger/) | [pgBadgerドキュメント](https://pgbadger.darold.net/) | v13.2、コミット`a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ja/haproxy/) | [HAProxy 3.4マニュアル](https://docs.haproxy.org/3.4/) | ドキュメントスナップショット3.4.6-66、コミット`16acce1`、安定版3.4.6 | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ja/etcd/) | [etcd v3.7ドキュメント](https://etcd.io/docs/v3.7/) | v3.7、コミット`d20f8ae` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [アップストリームの`LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

各ドキュメント集は単なるミラーではなく、**編集を加えたもの**です。見出し、アンカー、相互リンク、コードシグネチャ、ページの分類、ナビゲーションをこの版に合わせて再構成し、アップストリームの本文自体は保持しています。ページ末尾の帰属表示にその旨を記載し、閲覧中のページのサイト内変更履歴へリンクしています。

## Patroni {#patroni}

2026-08-15に、**v4.1.5**の[Patroniドキュメント](https://patroni.readthedocs.io/en/latest/)からインポートしました。

Patroniの著作権表示はcopyright (c) 2025 Compose, Zalando SE, Patroni Contributorsです。[MIT License](https://opensource.org/license/mit)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/patroni/patroni/blob/master/LICENSE)に保存されています。

## pgBackRest {#pgbackrest}

2026-08-15に[pgBackRestドキュメントサイト](https://pgbackrest.org/)からインポートし、
2026-10-13に**v2.59.3**へ更新しました。

pgBackRestの著作権表示はcopyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steeleです。[MIT License](https://opensource.org/license/mit)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)に保存されています。

## PgBouncer {#pgbouncer}

2026-08-15に、**v1.25.2**の[PgBouncerドキュメントサイト](https://www.pgbouncer.org/)からインポートし、
2026-10-13に[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0)へ更新しました。

PgBouncerの著作権表示はcopyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜです。[ISC License](https://opensource.org/license/isc-license-txt)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT)に保存されています。

## pgBadger {#pgbadger}

2026-08-15に、<https://pgbadger.darold.net/>と[`darold/pgbadger`](https://github.com/darold/pgbadger)のコミット[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae)からインポートしました。当時の最新公開リリースはv13.2でした。

pgBadgerの著作権表示はcopyright (c) 2012-2026 Gilles Daroldです。[PostgreSQL License](https://opensource.org/license/postgresql)のもとで配布されています。完全なライセンス本文は、オフラインのサンプルとともに[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE)として保存されており、サイトリポジトリの`static/third_party/pgbadger/LICENSE`にもあります。

> [!IMPORTANT]
> pgBadgerには、Artistic License 2.0のもとで改変された`SQL::Beautify`モジュールが組み込まれています。また、生成レポートのリソースには、MIT、GPL-2.0、SIL Open Font License 1.1のコンポーネントが含まれます。アップストリームの完全なリソース一覧は[`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES)に保存されています。
> ここで公開している[サンプルレポート](/ja/pgbadger/sample-reports/)は過去に生成された成果物であり、元の埋め込み通知を保持しています。

## HAProxy {#haproxy}

2026-08-16にインポートし、2026-10-13に公式HAProxy 3.4メンテナンスリポジトリのドキュメントスナップショット`3.4.6-66`、コミット[`16acce1dac1d`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=16acce1dac1dcf1ad5d654204af3a5d45d0e3de8)へ更新しました。最新の安定版リリースは3.4.6、タグ`v3.4.6`です。このスナップショットには、リリース後のマニュアルの変更も含まれます。英語本文は、完全な`doc/intro.txt`、`doc/configuration.txt`、`doc/management.txt`から作成しています。それぞれ1,695行、33,216行、5,305行、合計40,216行を、本文34ページに再構成しています。

HAProxyの著作権表示はcopyright 2000-2026 Willy Tarreauです。[GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)のもとで配布されています。HAProxy自身によるライセンスの説明、OpenSSL例外、および完全なGPLv2本文を、[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE)と[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0)で公開しています。

> [!WARNING]
> HAProxyを基にしたページには、このサイトのCC BY 4.0ライセンスは**適用されません**。HAProxyのGPLv2の条件が適用されます。

## etcd {#etcd}

公式etcd v3.7ドキュメントからインポートし、2026-10-13にコミット[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc)へ更新しました。固定したソースツリーは[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7)です。

etcdドキュメントの著作権表示はcopyright 2013-present etcd Authorsです。本文は[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)、コードとコードサンプルは[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)のもとでライセンスされています。完全な通知は[アップストリーム](https://github.com/etcd-io/website/blob/main/LICENSE)に保存されています。

## このサイト {#site}

PG.CENTERのために新たに作成した文章は、上記のアップストリームライセンスがそのページに適用される場合を除き、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)のもとで公開しています。

ホームページに表示されるPostgreSQLの象（Slonik）はPostgreSQLプロジェクト自身のマークです。[postgresql.orgのウェブサイトリポジトリ](https://git.postgresql.org/gitweb/?p=pgweb.git)から取得し、PostgreSQLを示すために[PostgreSQLの商標およびロゴポリシー](https://www.postgresql.org/about/policies/trademarks/)に従って改変せずに再公開しています。このマークはPostgreSQL Community Association of Canadaのものであり、ここでの使用は承認を意味しません。

このサイトは、[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)のもとで公開されているHugoテーマ、[OINK](https://oink.pgsty.com/) v1.2.0で構築されています。テーマ自身と同梱依存関係の通知は、モジュールのソースに含まれています。

このページの帰属表示に関する修正は、[サイトリポジトリ](https://github.com/pgsty/doc.pg.center/issues)へお寄せください。
