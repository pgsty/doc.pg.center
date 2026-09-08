---
title: "ライセンスとクレジット"
linkTitle: "ライセンス"
weight: 110
description: "PostgreSQL のライセンス条項、著作者、およびバンドルされているサードパーティ コンポーネント"
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [リファレンス]
aliases: [/docs/pgbadger/license/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE"
upstream_name: "pgBadger LICENSE"
---

pgBadger は、PostgreSQL ライセンスに基づいて配布される無料のオープンソース ソフトウェアです。著作権およびライセンス通知を保持することを条件として、無償で使用、コピー、変更、配布することができます。

## PostgreSQLライセンス {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## 著者とデザインのクレジット {#credits}

- pgBadger は、Gilles Darold によるオリジナル作品です。
- pgBadger ロゴは、Damien Cazeils によるオリジナルの作品です。
- pgBadger v4.x のデザインは、「Art is code」会社から提供されました。
- このウェブサイトは Gilles Darold の作品です。
- 貢献者は、上流の ChangeLog 全体にクレジットされます。

## 埋め込みリソースとレポート リソース {#third-party-resources}

`SQL::Beautify` Perl モジュールの修正バージョンが pgBadger に埋め込まれています。この作品の著作権は © 2009 Jonas Kramer にあり、Artistic License 2.0 に基づいて公開されています。

生成されたレポート リソースには、次のような独自の通知があります。

|コンポーネント |ライセンス |
|---|---|
| bean.js, Bootstrap, jQuery, Underscore |MIT |
| jqPlot | MIT または GPL-2.0、ユーザーの選択 |
|Font Awesomeフォント | SIL Open Font License 1.1 |
|Font Awesome CSS |MIT |

ローカル ソース スナップショットには、完全なアップストリーム `resources/LICENSE` が保持されます。バンドルされたサンプル レポートは過去に生成された成果物であり、元の埋め込み通知とリソースのバージョンが保持されます。

## ドキュメントのスナップショット {#documentation-snapshot}

このpgsql.cc版では、アップストリームのドキュメントが Hugo ページに再編成され、ナビゲーションと中国語での読解支援が追加され、忠実度が重要な場合には正確なコマンド ヘルプと ChangeLog テキストが保存されます。 pgBadger のソース ドキュメントは PostgreSQL ライセンスの下に残ります。元のプロジェクト名、作成者、上流リンクは保持されます。

