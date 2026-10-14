---
title: 数据损坏
weight: 5000
description: etcd 数据损坏和恢复
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/data_corruption.md"
---

etcd 内置了自动数据损坏检测机制，以防止成员状态发生不一致。

> [!NOTE]
> 在 etcd 3.7 中，请使用以下功能门控和时长标志。原有的实验性数据损坏检查标志已被移除；请参阅[配置选项](/zh/etcd/op-guide/configuration/#feature-gates)。

## 启用数据损坏检测 {#enabling-data-corruption-detection}

数据损坏检测可通过以下方式执行：
* 初始检查，通过 `--feature-gates=InitialCorruptCheck=true` 标志启用。
* 定期检查包括：
  * 已压缩的修订版本哈希，通过 `--feature-gates=CompactHashCheck=true` 标志启用。
  * 最新修订版本哈希，通过 `--corrupt-check-time` 标志启用。

引导过程中将执行初始检查。
成员将比较其持久化状态与其他成员的状态，若发现不匹配则退出。

两个周期性检查将在已运行的集群中由领导者执行。
领导者将比较其持久化状态与其他成员的状态，若发现不一致则触发 CORRUPT ALARM。
两项检查目的相同，但均建议启用，以在性能与检测时间之间取得平衡。
* 压缩修订版本哈希检查 - 需要定期执行压缩，性能开销极小，可处理缓慢的跟随者。
* 最新修订版本哈希检查 - 性能开销较高，无法处理缓慢的跟随者或频繁的压缩。

### 压缩修订版本哈希检查 {#compacted-revision-hash-check}

启用 `--feature-gates=CompactHashCheck=true` 标志后，每分钟执行一次检查。
可使用 `--compact-hash-check-time` 标志调整检查频率，格式为：`1m` - 每分钟，`1h` - 每小时。
该检查将压缩功能扩展为同时计算校验和，以便在集群成员之间进行比对。
不会引起额外的数据库扫描，因此开销极低，但要求集群定期执行压缩。

### 最新修订版本哈希检查 {#latest-revision-hash-check}

通过 `--corrupt-check-time` 标志启用，需以如下格式提供执行周期：`1m` - 每分钟，`1h` - 每小时。
由于性能开销较高，建议周期为数小时。
运行检查需在指定修订版本下扫描整个 etcd 内容以计算校验和。

## 恢复损坏的成员 {#restoring-a-corrupted-member}

恢复损坏的成员有三种方法：
* 清除成员持久化状态
* 替换成员
* 恢复整个集群

成员恢复后，可移除 CORRUPT ALARM 告警。

### 清除成员持久化状态 {#purge-member-persistent-state}

可按以下步骤清除成员状态：
1. 停止 etcd 实例。
2. 备份 etcd 数据目录。
3. 将 etcd 数据目录中的 `snap` 子目录移出。
6. 使用 `--initial-cluster-state=existing` 启动 `etcd`，并在 `--initial-cluster` 中列出集群成员。

预计 etcd 成员将从领导者下载最新的快照。

### 替换成员 {#replace-member}

可按以下步骤替换成员：
1. 停止 etcd 实例。
2. 备份 etcd 数据目录。
3. 删除数据目录。
4. 运行 `etcdctl member remove` 从集群中移除该成员。
5. 运行 `etcdctl member add` 将其重新添加。
6. 使用 `--initial-cluster-state=existing` 启动 `etcd`，并在 `--initial-cluster` 中列出集群成员。

### 恢复整个集群 {#restore-whole-cluster}

可通过从当前领导者保存快照，并将快照恢复到所有成员来恢复集群。
对领导者执行 `etcdctl snapshot save`，并参照 [恢复集群过程](/zh/etcd/op-guide/recovery/)。
