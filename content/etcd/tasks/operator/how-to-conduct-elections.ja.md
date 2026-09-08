---
title: etcdクラスターでリーダー選出を行う方法
description: etcdctlクライアントを使用してリーダー選出を行う手順
weight: 900
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## 前提条件 {#prerequisites}

- [`etcd`](/ja/etcd/install/)と[`etcdctl`](/ja/etcd/install/)がインストールされていることを確認します。
- 稼働中のetcdクラスターを確認します。

## リーダー選出を行う {#conduct-leader-election}

`etcdctl`コマンドは、etcdクラスターでリーダー選出を行うために使用します。一度にリーダーになれるクライアントが1つだけであることを保証します。

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### オプション {#options}

- `--endpoints : $ENDPOINTS`

各etcdクラスターメンバーのアドレス。

- `election-name`文字列

選出を識別する文字列です。リーダーの地位を競うすべての参加者は、同じ選出名を使用する必要があります。

- `leader-name`文字列

新しいリーダーの提案値。

### 例 {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
