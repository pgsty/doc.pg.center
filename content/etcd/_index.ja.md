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
upstream_source: etcd-20261121
categories: [概念]
search_keywords: [v3.7.4, "Go 1.26.11", force-new-cluster, NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7"
cascade:
  upstream_source: etcd-20261121
  type: docs
  module: [ETCD]
---

etcdは、強い整合性を備えた分散キー・バリューストアです。これらのガイドでは、etcdのインストールと運用、APIを使用したアプリケーションの構築、設計の理解、性能の測定、3.7リリース系列でのクラスターのアップグレードとダウングレードについて説明します。

ローカルの単一メンバークラスターを作成する場合は[クイックスタート](/ja/etcd/quickstart/)、サポートされるインストール方法については[インストール](/ja/etcd/install/)、本番環境へのデプロイについては[運用ガイド](/ja/etcd/op-guide/)から始めてください。

## etcd v3.7.4 {#etcd-v3-7-4}

現在のメンテナンスリリースは、2026年11月19日に公開された[v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4)です。この版のインストール、Docker、Kubernetesの例は、このリリースを対象としています。

- バックエンドの一貫性インデックスがWALより先にある場合の`--force-new-cluster`による復旧を修正します。
- 競合状態を避けるため、アラームストアにアトミックポインターを使用します。
- レガシーv2メンバー属性のWALエントリーを再生中に発生する起動時パニックを修正します。
- Go 1.26.11でビルドします。

[固定したアップストリームのchangelog](https://github.com/etcd-io/etcd/blob/1ce5a2b779143279c89ed8c7e33a42e51fb697fa/CHANGELOG/CHANGELOG-3.7.md#v374-tbc)を参照してください。見出しはまだ「TBC」ですが、公開済みのリリースタグが利用可能性を示しています。

## etcd v3.7.3 {#etcd-v3-7-3}

以前のメンテナンスリリースは[v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3)でした。

- MVCCストアの`Hash`と`Restore`の間、およびキーのみを返す`RangeStream`操作のデータ競合を修正し、リーダーが`MsgApp`メッセージを逆順で送信することによるレプリケーション性能のリグレッションを修正します。
- Go 1.26.10でビルドし、OpenTelemetryと`golang.org/x/net`の依存関係を更新して、報告されたセキュリティ問題に対処します。
- `client/pkg/v3/logutil`の`NewJournalWriter`を非推奨とし、v3.8での削除を予定しています。

変更の全容は[アップストリームの変更履歴](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22)を参照してください。
