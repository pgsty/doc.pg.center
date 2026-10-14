---
title: "サポート対象プラットフォーム"
weight: 4800
description: "主なアーキテクチャーとオペレーティングシステムに対するetcdのサポート"
categories: [リファレンス]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/supported-platform.md"
---

## サポート階層 {#support-tiers}

etcdはさまざまなプラットフォームで動作しますが、保証の内容はプラットフォームのサポート階層によって異なります。

- **階層1**：[etcdメンテナー][etcd maintainers]が完全にサポートします。機能テストと堅牢性テストを含むすべてのテストに合格することを保証します。
- **階層2**：統合テストとエンドツーエンドテストへの合格を保証しますが、機能テストや堅牢性テストに合格するとは限りません。
- **階層3**：ビルドできることを保証します。簡単なテストしか行っていない、またはテストしていない可能性があるため、*不安定*なものとして扱うことを推奨します。

## 現在のサポート状況 {#current-support}

次の表は、現在サポートされているプラットフォームと、それぞれのetcdサポート階層を示します。

| アーキテクチャー | オペレーティングシステム | サポート階層 | メンテナー |
|:------------:|:----------------:|:------------:|:--------------------:|
| AMD64 | Linux | 1 | [etcdメンテナー][etcd maintainers] |
| ARM64 | Linux | 1 | [etcdメンテナー][etcd maintainers] |
| AMD64 | Darwin | 3 | |
| ARM64 | Darwin | 3 | |
| AMD64 | Windows | 3 | |
| ppc64le | Linux | 3 | |
| s390x | Linux | 3 | |

表にないプラットフォームはサポート対象外です。

## 新しいプラットフォームのサポート {#supporting-a-new-platform}

新しいプラットフォームの「公式」メンテナーとしてetcdに貢献する場合、プラットフォームのサポートを継続して担うとともに、サポート階層に応じて次の要件を満たすetcdの継続的インテグレーション（CI）を構築しなければなりません。

| etcdの継続的インテグレーション | 階層1 | 階層2 | 階層3 |
|---------------------------------------|:-------:|:-------:|:-------:|
| ビルドの成功 | &check; | &check; | &check; |
| 単体テストの合格 | &check; | &check; | |
| 統合テストとエンドツーエンドテストの合格 | &check; | &check; | |
| 堅牢性テストの合格 | &check; | | |

ARM64向けの階層2のCIを構築した例は、[etcd PR #12928][]を参照してください。

## サポート対象外のプラットフォーム {#unsupported-platforms}

サポート対象外のプラットフォームでetcdサーバーを誤って実行することを防ぐため、環境変数`ETCD_UNSUPPORTED_ARCH`に対象アーキテクチャーが設定されていない限り、etcdは警告メッセージを表示して直ちに終了します。

> [!WARNING]
> **32ビットシステム**
>   etcdには、Goランタイムのバグによる32ビットシステムでの**既知の問題**があります。
>   詳しくは、[Goのissue #599][go-issue]と[atomicパッケージのバグに関する注記][go-atomic]を参照してください。
>
>   [go-atomic]: https://golang.org/pkg/sync/atomic/#pkg-note-BUG
>   [go-issue]: https://github.com/golang/go/issues/599

[etcd maintainers]: https://github.com/etcd-io/etcd/blob/main/OWNERS
[etcd PR #12928]: https://github.com/etcd-io/etcd/pull/12928
