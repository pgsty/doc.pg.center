---
title: "CHECKPOINT"
description: "强制执行一次预写式日志检查点。"
weight: 460
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/checkpoint.md"
---

## 概要 {#synopsis}

```sql
CHECKPOINT
```

## 描述 {#description}

检查点是预写式日志序列中的一个位置，到达这一位置时，所有数据文件都已更新，以反映日志中的信息。所有数据文件都会被刷写到磁盘。

`CHECKPOINT` 命令会在发出时强制立即执行一次检查点，而不等待系统调度的常规检查点。`CHECKPOINT` 并非设计用于正常运行期间。

如果在恢复期间运行，`CHECKPOINT` 命令将强制执行一个重启点，而不是写入一个新的检查点。

只有超级用户才能调用 `CHECKPOINT`。

## 兼容性 {#compatibility}

`CHECKPOINT` 命令是 Apache Cloudberry 的扩展。
