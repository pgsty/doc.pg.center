---
title: 如何在事务中进行多次写操作
description: 事务性写操作指南
weight: 500
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-transactional-write.md"
aliases: [/etcd/tasks/developer/how-to-transactional-write/]
---

## 先决条件 {#prerequisites}

* 安装 [`etcd` 和 `etcdctl`](/zh/docs/etcd/install/)。
* 运行中的 `etcd` 集群。

## 术语 {#terminology}

以下是本文中使用的部分关键术语的定义，这些术语将在 [Example](#example) 示例中出现。

| 术语 | 定义 |
| --- | --- |
| [etcdctl](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#etcdctl) | 用于与 etcd 服务器交互的命令行工具。 |
| [`txn`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#txn-options) 命令 | `txn` 命令是“事务”的缩写。它从标准输入读取多个 etcd 请求，并将其作为单个原子事务执行。事务包含一组条件、一组在所有条件均为真时执行的请求，以及一组在任一条件为假时执行的请求。有关更多信息，请参阅 [etcdctl 键值命令](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#key-value-commands)。 |
| `compare` | 事务（`txn`）中的 `compare` 子句用作条件检查，用于判断事务操作是否应继续执行。它确保仅当键值存储的当前状态符合预期条件时才应用变更，从而维护数据一致性，并在并发环境中防止冲突。要了解该命令的结构，请参阅下方 [执行事务](#2-perform-a-transaction) 章节。 |

## 事务 {#transactions}

`txn` 以事务方式处理所有请求：

```bash
etcdctl txn --help
```

事务允许在 etcd 中原子性地执行多个操作，确保所有操作均被应用或全部不被应用。这在执行相关更新时对于维护数据一致性至关重要。有关事务的更多信息，请参见 [API 文档](/zh/docs/etcd/learning/api/#transaction)。

### 示例 {#example}

考虑一种场景：需要在单个事务中更新用户的电子邮件和电话号码。这可确保两项更新同时生效。

![05_etcdctl_transaction_2024101213](/docs/etcd/tasks/img/transactional-write.gif)

#### 0. 使用的变量和标志 {#0-variables-and-flags-used}

| 变量 |
| :--- |
| `/users/{<user_id>/email` : 表示用户电子邮件地址的 etcd 键。|
| `/users/<user_id>/phone` : 表示用户电话号码的 etcd 键。|
| **标志** |
| [`--interactive`](https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#options-3) : 用于允许手动输入事务数据的标志。 |

#### 1. 初始化数据设置 {#1-set-up-initial-data}

首先，创建一个带有初始数据的用户。

   ```shell
   etcdctl put /users/12345/email "old.address@johndoe.com"
   etcdctl put /users/12345/phone "123-456-7890"
   ```

#### 2. 执行事务 {#2-perform-a-transaction}

在单个事务中更新用户的电子邮件和电话号码。

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

* **Compare**：检查当前邮箱是否为 "<old.address@johndoe.com>"。这确保事务仅在数据符合预期时才继续执行。
* **Success**：如果比较结果为真，更新邮箱和电话号码。
* **Failure**：如果比较失败，获取当前邮箱以了解事务未执行的原因。

### 重要考虑事项 {#important-considerations}

* **原子性**：事务确保电子邮件和电话号码同时更新。如果初始条件（比较）不满足，则不会应用任何更新。
* **一致性**：使用事务可维持数据一致性，尤其是在处理多个相关更新时。
* **避免在单个事务中对同一键多次写入**：在单个事务中不要对同一键写入多个值，这可能导致意外结果。每个键在事务中应仅更新一次。
