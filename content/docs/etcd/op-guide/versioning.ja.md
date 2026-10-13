---
title: バージョン管理
weight: 4900
description: etcdでサポートされるバージョン
categories: [概念]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/versioning.md"
aliases: [/etcd/op-guide/versioning/]
---

このドキュメントでは、etcdプロジェクトでサポートされるバージョンについて説明します。

## サービスのバージョン管理とサポート対象バージョン {#service-versioning-and-supported-versions}

etcdのバージョンは、[セマンティックバージョニング](https://semver.org/)の用語に従い、**x.y.z**と表記します。**x**はメジャーバージョン、**y**はマイナーバージョン、**z**はパッチバージョンです。新しいマイナーバージョンでは、APIに機能が追加される場合があります。

etcdプロジェクトでは、現行バージョンとその前のリリースのリリースブランチを保守します。たとえば、v3.5が現行バージョンの場合、v3.4もサポートされます。v3.6がリリースされると、v3.4のサポートは終了します。

セキュリティー修正を含む適用可能な修正は、重大度と実現可能性に応じて、これら2つのリリースブランチにバックポートされる場合があります。必要に応じて、これらのブランチからパッチリリースを作成します。

この判断は、プロジェクトの[メンテナー](https://github.com/etcd-io/etcd/blob/main/OWNERS)が行います。

稼働中のetcdクラスターのバージョンは、`etcdctl`で確認できます。

```sh
etcdctl --endpoints=127.0.0.1:2379 endpoint status
```

## APIのバージョン管理 {#api-versioning}

`v3` APIのレスポンスは、3.0.0リリース以降は変更されない想定ですが、新機能は今後も追加されます。
