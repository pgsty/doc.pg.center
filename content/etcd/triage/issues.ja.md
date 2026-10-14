---
title: "Issueのトリアージガイドライン"
weight: 8100
description: "etcdのIssueをトリアージするためのガイドライン"
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/triage/issues.md"
---

## 目的 {#purpose}

Issueの管理を迅速に行います。

`etcd`のIssueは https://github.com/etcd-io/etcd/issues に一覧があり、
ラベルで分類されています。たとえば、バグと判断されたIssueには、
最終的に`area/bug `ラベルが付けられます。新しいIssueには当初ラベルがありませんが、
通常は`etcd`のメンテナーや活発に活動する貢献者が調査結果に基づいて追加します。
ラベルの詳細な一覧は https://github.com/kubernetes/kubernetes/labels を参照してください。

便利なIssue検索へのリンクをいくつか挙げます。
* [バグ](https://github.com/etcd-io/etcd/labels/area%2Fbug)
* [協力者募集中](https://github.com/etcd-io/etcd/labels/Help%20Wanted)
* [長期間トリアージされていないIssue](https://github.com/etcd-io/etcd/issues?utf8=%E2%9C%93&q=is%3Aopen+sort%3Aupdated-asc+)
* [Issueトリアージミーティング](https://etcd.io/community/#community-meetings)

## 対象範囲 {#scope}

このガイドラインは、`etcd`に新たに報告されたIssueをトリアージするための基本文書です。IssueやPRの管理への協力は誰でも歓迎しますが、ここで説明する作業と責任は、`etcd`のメンテナーや活発に活動する貢献者を想定しています。

## Issueがバグかどうかの確認 {#validate-if-an-issue-is-a-bug}

報告された問題が実際にバグかどうかを確認します。バグでない場合は調査結果をコメントし、軽微なIssueならクローズします。軽微でない場合は、報告者からの返答を待ち、異議がないかを確認します。報告者が30日以内に返答しなければ、Issueをクローズします。問題を再現できない場合や追加情報が必要な場合は、報告者に向けてコメントを残します。

## 動きのないIssue {#inactive-issues}

報告者からの情報が不足しているIssueは、60日以内に情報が提供されなければクローズすることを推奨します。

## 重複するIssue {#duplicate-issues}

Issueが重複している場合は、その旨と元のIssueへの参照をコメントし、クローズします。

## etcdに属さないIssue {#issues-that-dont-belong-to-etcd}

`etcd`が使用している他のプロジェクトの問題が報告されることがあります。たとえば、`grpc`や`golang`の問題です。このような場合は、適切なプロジェクトでIssueを作成するよう報告者に依頼することを推奨します。メンテナーと報告者が追跡のために残す必要があると考える場合を除き、Issueをクローズします。

## 重要なラベルの確認 {#verify-important-labels-are-in-place}

Issueに該当領域のラベルが付き、適切な担当者が割り当てられ、マイルストーンが決まっていることを確認します。必要なラベルが欠けていれば追加します。権限不足でラベルを付けられない場合や適切なラベルを判断できない場合は、無理に対応する必要はありません。必要に応じてメンテナーに連絡してください。

## 必要に応じた担当者への確認 {#poke-issue-owner-if-needed}

開発者が担当しているIssueで30日経ってもPRが作成されていない場合は、担当者に連絡し、PRの作成、または必要に応じて担当を外れることを依頼します。
