---
title: "ライセンスとクレジット"
linkTitle: "ライセンス"
weight: 110
description: "PostgreSQLのライセンス条項、著作者、およびバンドルされているサードパーティコンポーネント"
search_keywords: []
icon: fa-solid fa-scale-balanced
module: [PGBADGER]
categories: [リファレンス]
aliases: [/pgbadger/license/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/LICENSE"
upstream_name: "pgBadger LICENSE"
---

pgBadgerは、PostgreSQLライセンスに基づいて配布される無料のオープンソースソフトウェアです。著作権およびライセンス通知を保持することを条件として、無償で使用、コピー、変更、配布することができます。

## PostgreSQLライセンス {#postgresql-license}

Copyright (c) 2012-2026, Gilles Darold

Permission to use, copy, modify, and distribute this software and its documentation for any purpose, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and this paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL Darold BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF Darold HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Darold SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN “AS IS” BASIS, AND Darold HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

## 著者とデザインのクレジット {#credits}

- pgBadgerは、Gilles Daroldによるオリジナル作品です。
- pgBadgerロゴは、Damien Cazeilsによるオリジナルの作品です。
- pgBadger v4.xのデザインは、「Art is code」社が制作しました。
- このウェブサイトはGilles Daroldの作品です。
- 貢献者の名前は、アップストリームのChangeLog各所に記載されています。

## 埋め込みリソースとレポートリソース {#third-party-resources}

`SQL::Beautify` Perlモジュールの修正バージョンがpgBadgerに埋め込まれています。この作品の著作権は © 2009 Jonas Kramerにあり、Artistic License 2.0に基づいて公開されています。

生成されたレポートリソースには、次のような独自の通知があります。

| コンポーネント | ライセンス |
|---|---|
| bean.js、Bootstrap、jQuery、Underscore | MIT |
| jqPlot | MITまたはGPL-2.0(ユーザーの選択) |
| Font Awesomeフォント | SIL Open Font License 1.1 |
| Font Awesome CSS | MIT |

リソースのライセンス条項全文は`resources/LICENSE`にあります。サンプルレポートには、生成時の著作権通知とリソースのバージョンが含まれます。
