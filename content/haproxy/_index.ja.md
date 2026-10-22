---
title: "HAProxy 3.4.7-57ドキュメント"
linkTitle: HAProxy
weight: 50
description: "HAProxy 3.4の入門・設定・管理マニュアルを全文収録した日本語Markdown版"
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [リファレンス]
upstream_source: haproxy
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy
  type: docs
  module: [HAPROXY]
---

**HAProxy**は、高可用性、TCPとHTTPの負荷分散、アプリケーショントラフィックの管理を実現する、無料で高速かつ信頼性の高いリバースプロキシです。このコンポーネントでは、HAProxy 3.4の主要な3つのマニュアルの日本語訳全文を、OINK用に階層のない一連のMarkdownページへ再構成しています。

この版は、公式英語マニュアルのメンテナンスブランチのスナップショット`3.4.7-57`に対応しています。最新の安定版リリースは`3.4.7`（`v3.4.7`）です。このスナップショットには、そのリリース後のドキュメントの変更も含まれます。正確なソースはコミット[`0faeaeda6cdb`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3)です。

## マニュアルの選択 {#choose-a-manual}

- [入門ガイド](/ja/haproxy/load-balancing/) — 負荷分散の概念、HAProxyのアーキテクチャ、機能、サイジング、リリース、エコシステムに関する9つのトピック。
- [設定マニュアル](/ja/haproxy/http-fundamentals/) — プロキシ、ACL、サンプル、ログ、フィルター、すべてのオプション群を網羅した12章。
- [管理ガイド](/ja/haproxy/prerequisites/) — 起動、リロード、リソース、ログ、統計、ランタイムCLI、デバッグ、セキュリティに関する13章。
{.cards}

## 収録範囲 {#edition-coverage}

| マニュアル | アップストリームの原文 | このサイトでの構成 |
| --- | ---: | ---: |
| 入門ガイド | 1,695行 | 同一階層の9トピックページ |
| 設定マニュアル | 33,246行 | 同一階層の12章ページ |
| 管理ガイド | 5,305行 | 同一階層の13章ページ |

本文34ページはいずれもHAProxyコンポーネントのルート直下に配置しています。リンクを持たない3つの区切り用プレースホルダーで各マニュアルを区分し、ディレクトリ階層やページ送りの経由先を増やさずにサイドバーへ表示しています。

元のマニュアル全文は、上記リンクが指すアップストリームの固定リビジョンから取得できます。[アップストリームのライセンス通知](/third_party/haproxy/LICENSE)と[GPLv2の本文](/third_party/haproxy/GPL-2.0)も、マニュアルとともに公開しています。各ページには、レビュー済みの簡体字中国語版も用意されています。
