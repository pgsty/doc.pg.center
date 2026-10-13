---
title: システムの制限
weight: 3625
description: "etcdの制限：リクエストとストレージ"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/dev-guide/limit.md"
aliases: [/etcd/dev-guide/limit/]
---

## リクエストサイズの上限 {#request-size-limit}

etcdは、メタデータで一般的な小さなキー・バリューペアを処理するように設計されています。大きなリクエストも処理できますが、他のリクエストのレイテンシーが増加する可能性があります。デフォルトでは、各リクエストの最大サイズは1.5 MiBです。この上限は、etcdサーバーの`--max-request-bytes`フラグで設定できます。

## ストレージサイズの上限 {#storage-size-limit}

ストレージサイズのデフォルトの上限は2 GiBで、`--quota-backend-bytes`フラグで設定できます。通常の環境で推奨される最大サイズは8 GiBです。設定値がこのサイズを超えると、etcdは起動時に警告を出します。
