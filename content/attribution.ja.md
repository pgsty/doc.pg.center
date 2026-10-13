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

pig.centerは、6つのアップストリームプロジェクトが作成したドキュメントを再公開しています。各ドキュメントページの末尾には、原著作物、著作権者、ライセンス、およびこのページの該当セクションへのリンクを記載した1行の帰属表示があります。

このページはその記録です。何を、いつ、どの固定リビジョンから、どのライセンスのもとでインポートしたか、また完全なアップストリームの通知をどこに保存しているかを示します。

> [!NOTE]
> 英語、簡体字中国語、フランス語は、6つのドキュメント集をすべて収録しています。日本語、ドイツ語、ロシア語では完成した翻訳を公開しています。未翻訳のページへのリンクは、対応する英語ページに切り替わります。

> [!NOTE]
> pig.centerは独立したコミュニティドキュメントプロジェクトです。以下の各プロジェクトやPostgreSQL Global Development Groupとの提携や承認を示すものではなく、それらの公式出版物でもありません。

## 概要 {#summary}

| コンポーネント | アップストリームの著作物 | 固定バージョン | ライセンス | 保存されている通知 |
|---|---|---|---|---|
| [Patroni](/ja/docs/patroni/) | [Patroniドキュメント](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [アップストリームの`LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ja/docs/pgbackrest/) | [pgBackRestドキュメント](https://pgbackrest.org/) | v2.59.2（英語 / 簡体字中国語）；v2.59.1（その他の翻訳） | [MIT](https://opensource.org/license/mit) | [アップストリームの`LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ja/docs/pgbouncer/) | [PgBouncerドキュメント](https://www.pgbouncer.org/) | v1.26.0（英語 / 簡体字中国語） | [ISC](https://opensource.org/license/isc-license-txt) | [アップストリームの`COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/ja/docs/pgbadger/) | [pgBadgerドキュメント](https://pgbadger.darold.net/) | v13.2、コミット`a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ja/docs/haproxy/) | [HAProxy 3.4マニュアル](https://docs.haproxy.org/3.4/) | v3.4.4、コミット`7f03ae6` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ja/docs/etcd/) | [etcd v3.7ドキュメント](https://etcd.io/docs/v3.7/) | v3.7、コミット`8245979` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [アップストリームの`LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

各ドキュメント集は単なるミラーではなく、**編集を加えたもの**です。見出し、アンカー、相互リンク、コードシグネチャ、ページの分類、ナビゲーションをこの版に合わせて再構成し、アップストリームの本文自体は保持しています。ページ末尾の帰属表示にその旨を記載し、閲覧中のページのサイト内変更履歴へリンクしています。

## Patroni {#patroni}

2026-08-15に、**v4.1.5**の[Patroniドキュメント](https://patroni.readthedocs.io/en/latest/)からインポートし、簡体字中国語訳も同時に作成しました。

Patroniの著作権表示はcopyright (c) 2025 Compose, Zalando SE, Patroni Contributorsです。[MIT License](https://opensource.org/license/mit)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/patroni/patroni/blob/master/LICENSE)に保存されています。

## pgBackRest {#pgbackrest}

2026-08-15に[pgBackRestドキュメントサイト](https://pgbackrest.org/)からインポートしました。
英語版と簡体字中国語版は2026-10-04に**v2.59.2**へ更新しました。
その他の既存の翻訳は**v2.59.1**のままで、最終更新日は2026-08-30です。

pgBackRestの著作権表示はcopyright (c) 2015-2026 The PostgreSQL Global Development Group and David Steeleです。[MIT License](https://opensource.org/license/mit)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)に保存されています。

## PgBouncer {#pgbouncer}

2026-08-15に、**v1.25.2**の[PgBouncerドキュメントサイト](https://www.pgbouncer.org/)からインポートし、簡体字中国語訳も同時に作成しました。

英語版と簡体字中国語版は2026-10-04に
[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0)へ更新しました。
それぞれ`pigsty.io`と`pigsty.cc`の校正済みマニュアルを使用しています。
リファレンスの説明をこのリリースの実装と照合し、アップストリーム文書の4種類の誤りを修正しました。
その他の言語版はv1.25.2のドキュメントスナップショットを維持しています。

PgBouncerの著作権表示はcopyright (c) 2007-2009 Marko Kreen, Skype Technologies OÜです。[ISC License](https://opensource.org/license/isc-license-txt)のもとで配布されています。完全なライセンス本文は[アップストリーム](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT)に保存されています。

## pgBadger {#pgbadger}

2026-08-15に、<https://pgbadger.darold.net/>と[`darold/pgbadger`](https://github.com/darold/pgbadger)のコミット[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae)からインポートしました。当時の最新公開リリースはv13.2でした。

pgBadgerの著作権表示はcopyright (c) 2012-2026 Gilles Daroldです。[PostgreSQL License](https://opensource.org/license/postgresql)のもとで配布されています。完全なライセンス本文は、オフラインのサンプルとともに[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE)として保存されており、サイトリポジトリの`sources/pgbadger/upstream/LICENSE`にもあります。

> [!IMPORTANT]
> pgBadgerには、Artistic License 2.0のもとで改変された`SQL::Beautify`モジュールが組み込まれています。また、生成レポートのリソースには、MIT、GPL-2.0、SIL Open Font License 1.1のコンポーネントが含まれます。アップストリームの完全なリソース一覧は[`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES)に保存されています。
> ここで公開している[サンプルレポート](/ja/docs/pgbadger/sample-reports/)は過去に生成された成果物であり、元の埋め込み通知を保持しています。

## HAProxy {#haproxy}

2026-08-16に公式HAProxy 3.4保守リポジトリからインポートし、2026-08-30にタグ`v3.4.4`、コミット[`7f03ae65c286`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0)へ更新しました。英語本文は、合計40,128行の`doc/intro.txt`、`doc/configuration.txt`、`doc/management.txt`の全マニュアルを基に、34の閲覧用ページに再構成しています。

HAProxyの著作権表示はcopyright 2000-2026 Willy Tarreauです。[GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)のもとで配布されています。HAProxy自身によるライセンスの説明、OpenSSL例外、および完全なGPLv2本文を、[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE)と[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0)で公開しています。

> [!WARNING]
> HAProxyを基にしたページには、このサイトのCC BY 4.0ライセンスは**適用されません**。HAProxyのGPLv2の条件が適用されます。

## etcd {#etcd}

公式etcd v3.7ドキュメントからインポートし、2026-08-30にコミット[`824597935df6`](https://github.com/etcd-io/website/commit/824597935df6e95992ef61c07e3222f4f796ca6c)へ更新しました。固定したソースツリーは[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7)です。

etcdドキュメントの著作権表示はcopyright 2013-present etcd Authorsです。本文は[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)、コードとコードサンプルは[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)のもとでライセンスされています。完全な通知は[アップストリーム](https://github.com/etcd-io/website/blob/main/LICENSE)に保存されています。

## このサイト {#site}

pig.centerのために新たに作成した文章（案内ページ、簡体字中国語・フランス語の完全版、公開済みの日本語・ドイツ語・ロシア語訳、編集上の注記、ランディングページ）は、上記のアップストリームライセンスがそのページに適用される場合を除き、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)のもとで公開しています。

ホームページに表示されるPostgreSQLの象（Slonik）はPostgreSQLプロジェクト自身のマークです。[postgresql.orgのウェブサイトリポジトリ](https://git.postgresql.org/gitweb/?p=pgweb.git)から取得し、PostgreSQLを示すために[PostgreSQLの商標およびロゴポリシー](https://www.postgresql.org/about/policies/trademarks/)に従って改変せずに再公開しています。このマークはPostgreSQL Community Association of Canadaのものであり、ここでの使用は承認を意味しません。

このサイトは、[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)のもとで公開されているHugoテーマ、[OINK](https://oink.pgsty.com/) v1.2.0で構築されています。テーマ自身と同梱依存関係の通知は、モジュールのソースに含まれています。

このページの帰属表示に関する修正は、[サイトリポジトリ](https://github.com/pgsty/pig.center/issues)へお寄せください。
