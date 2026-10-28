---
title: "etcd 3.7 ドキュメント"
linkTitle: "etcd 3.7"
description: "開発者、運用担当者、アップグレード、API、内部実装に関するetcd 3.7の公式ガイド。"
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [概念]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcdは、強い整合性を備えた分散キー・バリューストアです。これらのガイドでは、etcdのインストールと運用、APIを使用したアプリケーションの構築、設計の理解、性能の測定、3.7リリース系列でのクラスターのアップグレードとダウングレードについて説明します。

ローカルの単一メンバークラスターを作成する場合は[クイックスタート](/ja/etcd/quickstart/)、サポートされるインストール方法については[インストール](/ja/etcd/install/)、本番環境へのデプロイについては[運用ガイド](/ja/etcd/op-guide/)から始めてください。

## etcd v3.7.3 {#etcd-v3-7-3}

現在のメンテナンスリリースは[v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3)です。この版のインストール、Docker、Kubernetesの例は、このリリースを対象としています。

- MVCCストアの`Hash`と`Restore`の間、およびキーのみを返す`RangeStream`操作のデータ競合を修正し、リーダーが`MsgApp`メッセージを逆順で送信することによるレプリケーション性能のリグレッションを修正します。
- Go 1.26.10でビルドし、OpenTelemetryと`golang.org/x/net`の依存関係を更新して、報告されたセキュリティ問題に対処します。
- `client/pkg/v3/logutil`の`NewJournalWriter`を非推奨とし、v3.8での削除を予定しています。

変更の全容は[アップストリームの変更履歴](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22)を参照してください。
