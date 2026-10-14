---
title: "トランザクションで複数の書き込みを行う方法"
description: "トランザクションによる書き込みのガイド"
weight: 500
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
---

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/etcd/install/)がインストールされていること。
* `etcd`クラスターが稼働していること。

## 用語 {#terminology}

以下の[例](#example)で使用する主な用語を定義します。

| 用語 | 定義 |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | etcdサーバーを操作するコマンドラインツール。 |
| [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options)コマンド | `txn`は「transaction」の略です。複数のetcdリクエストを標準入力から読み込み、単一の不可分なトランザクションとして適用します。トランザクションは、条件のリスト、すべての条件が真の場合に適用するリクエストのリスト、いずれかの条件が偽の場合に適用するリクエストのリストで構成されます。詳細は[etcdctlのキー・バリューコマンド](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands)を参照してください。|
| `compare` | トランザクション（`txn`）内の`compare`句は、その処理を実行するかどうかを決める条件判定です。キー・バリューストアの現在の状態が期待する条件に一致する場合にのみ変更を適用することで、データの整合性を維持し、並行処理での競合を防ぎます。コマンドの構成は、以下の[トランザクションの実行](#2-perform-a-transaction)を参照してください。|

## トランザクション {#transactions}

`txn`を使用して、すべてのリクエストを1つのトランザクションで処理します。

```bash
etcdctl txn --help
```

etcdのトランザクションでは、複数の操作を不可分に実行し、すべての操作を適用するか、どれも適用しないかのいずれかとなることを保証します。これは、関連する更新を行う際のデータ整合性の維持に不可欠です。トランザクションの詳細は[APIドキュメント](/ja/etcd/learning/api/#transaction)を参照してください。

### 例 {#example}

ユーザーのメールアドレスと電話番号を1つのトランザクションで更新する場合を考えます。これにより、両方の更新がまとめて適用されることを保証します。

![etcdctlによるトランザクションの実行例](/etcd/tasks/img/transactional-write.gif)

#### 0. 使用する変数とフラグ {#0-variables-and-flags-used}

| 変数 |
| :--- |
| `/users/{<user_id>/email`：ユーザーのメールアドレスを表すetcdキー。|
| `/users/<user_id>/phone`：ユーザーの電話番号を表すetcdキー。|
| **フラグ** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3)：トランザクションのデータを手動で入力できるようにするフラグ。|

#### 1. 初期データの設定 {#1-set-up-initial-data}

まず、初期データを持つユーザーを作成します。

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. トランザクションの実行 {#2-perform-a-transaction}

ユーザーのメールアドレスと電話番号を1つのトランザクションで更新します。

   ```shell
   etcdctl txn --interactive

   compares:
   value("/users/12345/email") = "old.address@johndoe.com"

   success requests (get, put, delete):
   put /users/12345/email "new.address@johndoe.com"
   put /users/12345/phone "098-765-4321"

   failure requests (get, put, delete):
   get /users/12345/email
   ```

* **比較**：現在のメールアドレスが「<old.address@johndoe.com>」であるかを確認します。これにより、データが期待どおりの場合にのみトランザクションを実行します。
* **成功**：比較結果が真なら、メールアドレスと電話番号の両方を更新します。
* **失敗**：比較に失敗した場合は、現在のメールアドレスを取得し、トランザクションが実行されなかった理由を確認します。

### 重要な注意点 {#important-considerations}

* **原子性**：トランザクションにより、メールアドレスと電話番号がまとめて更新されることを保証します。最初の条件（比較）を満たさなければ、どちらの更新も適用されません。
* **整合性**：トランザクションを使用すると、特に複数の関連する更新を扱う場合に、データの整合性を維持できます。
* **同じキーへの複数回のputを避ける**：予期しない結果を招く可能性があるため、1つのトランザクション内で同じキーに複数の値をputしないでください。各キーの更新は、1トランザクションにつき1回にすることを推奨します。
