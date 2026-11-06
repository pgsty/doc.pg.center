---
title: "识别并缓解堆表性能问题"
description: "诊断和缓解批量变更后因提示位更新和 WAL 记录导致的堆表首次扫描缓慢问题。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/identify-and-mitigate-heap-table-performance-issues.md"
---

**症状**：

堆表执行批量数据加载、修改或删除任务后，首次扫描元组时速度很慢或一直挂起。

**潜在原因**：

当工作负载涉及堆表中的批量数据加载、修改或删除时，如果启用了校验和（`data_check_sums=true`）或记录了提示位（`wal_log_hints=true`），操作后的首次扫描可能生成大量 WAL 数据，导致任务缓慢或挂起。

受影响的工作负载包括：从备份恢复、使用 `gpcopy` 或 `COPY` 加载数据、集群扩容、`CTAS`/`INSERT`/`UPDATE`/`DELETE` 操作，以及修改元组的 `ALTER TABLE` 操作。

**说明**：

Apache Cloudberry 使用提示位标记事务创建或删除的元组。设置提示位后，可以无需执行开销很高的 `pg_xact` 和 `pg_subtrans` 提交日志查找，就能帮助确定元组的可见性。

元组创建或删除后首次扫描该元组时，会更新每个元组的提示位。由于提示位按元组逐一检查和设置，即使是读操作也可能产生大量写入。对堆表启用数据校验和（默认行为）时，提示位更新始终会写入 WAL。

**解决方案**：

如果恢复或加载的是一个主要由堆表组成的完整数据库，可以选择对整个数据库运行 `VACUUM`。

或者，如果可以识别受影响的单个表，则有以下两种选择：

1. 安排维护窗口，并对批量加载、更新或删除过数据的特定表运行 `VACUUM`。此操作应扫描所有元组，设置提示位并将其写入 WAL，从而提前承担性能开销。

2. 对每个表运行 `SELECT count(*) FROM <table-name>`。此操作同样会扫描所有元组，并设置提示位、将其写入 WAL。

作为常规工作负载的一部分进行后续扫描时，通常不需要再生成提示位或与其对应的整页镜像 WAL 记录。
