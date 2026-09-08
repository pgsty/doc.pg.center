---
title: etcdクラスターとアプリケーションのアップグレード
weight: 6500
description: etcdクラスターとアプリケーションのアップグレードに関するドキュメント一覧
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrading-etcd.md"
aliases: [/etcd/upgrades/upgrading-etcd/]
---

このセクションには、etcdクラスターとアプリケーションのアップグレードに関するドキュメントをまとめています。

## アップグレード方針 {#upgrade-policy}

アップグレードを始める前に、etcdでサポートされるアップグレードは次の2つの場合だけであることに注意してください。

* **パッチアップグレード：** 同じマイナーバージョン内でのパッチリリース間のアップグレードです（例：3.7.0 - 3.7.1）。
* **マイナーアップグレード：** マイナーバージョンを1つずつ上げるアップグレードです（例：3.6 - 3.7）。マイナーバージョンを飛ばすアップグレードはサポートされず、失敗する可能性が高くなります。次のマイナーバージョンにアップグレードする前に、最新のパッチバージョンに更新してください。

## etcd v3.xクラスターのアップグレード {#upgrading-an-etcd-v3x-cluster}

* [etcdを3.0から3.1にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_1/)
* [etcdを3.1から3.2にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_2/)
* [etcdを3.2から3.3にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_3/)
* [etcdを3.3から3.4にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_4/)
* [etcdを3.4から3.5にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_5/)
* [etcdを3.5から3.6にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_6/)
* [etcdを3.6から3.7にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_7/)

## etcd v2.3からのアップグレード {#upgrading-from-etcd-v23}

* [v2.3クラスターをv3.0にアップグレード](/ja/docs/etcd/upgrades/upgrade_3_0/)
