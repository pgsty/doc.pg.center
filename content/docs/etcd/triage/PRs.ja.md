---
title: PRの管理
weight: 8200
description: "etcdのプルリクエストを管理するためのガイドライン"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/PRs.md"
aliases: [/etcd/triage/prs/]
---

## 目的 {#purpose}

PRの管理を迅速にすること。

`etcd`のPRは https://github.com/etcd-io/etcd/pulls に一覧表示されています。
PRにはさまざまなラベル、マイルストーン、レビュアーなどを設定できます。ラベルの詳細な一覧は、次のページを参照してください。
https://github.com/kubernetes/kubernetes/labels

便利なPR検索の例を以下に示します。
* [etcd-v3.4マイルストーンのオープンPR](https://github.com/etcd-io/etcd/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+milestone%3Aetcd-v3.4)
* [調査中のPR](https://github.com/etcd-io/etcd/labels/Investigating)

## 対象範囲 {#scope}

このガイドラインは、`etcd`でPRを管理する際の基本となるドキュメントです。PRの管理への協力はどなたでも歓迎しますが、このドキュメントで扱う作業と責任は、`etcd`のメンテナーと積極的に活動するコントリビューターを想定しています。

## 動きのないPRへの対応 {#handle-inactive-prs}
レビューコメントに15日間対応がない場合は、PRの作成者に確認を促してください。PRの作成者から90日間返信がない場合は、可能であれば新しいコミットでPRを更新してください。それができなければ、動きのないPRは180日後にクローズするべきです。

## 必要に応じてレビュアーに確認を促す {#poke-reviewer-if-needed}

レビュアーは適時に応答していますが、全員が忙しいことを考慮し、レビューを依頼してすぐに応答がなくても、しばらく待ってください。10日間応答がなければ、PRへのコメントの追加、メールの送信、Slackでのメッセージ送信によって連絡して構いません。

## 重要なラベルが付いていることを確認する {#verify-important-labels-are-in-place}

PRに適切なレビュアーが追加されていることを確認してください。また、マイルストーンが指定されていることも確認してください。これらの項目やその他の重要なラベルが不足していれば追加してください。適切なラベルを判断できない場合は、必要に応じてメンテナーに対応を依頼するコメントを残してください。
