---
title: "数据分布与倾斜"
description: "Apache Cloudberry 依赖数据在各 Segment 之间均匀分布。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/distribution-and-skew.md"
---

在 MPP 无共享环境中，查询的整体响应时间由所有 Segment 完成处理所需的时间决定。系统速度受最慢的 Segment 限制。如果数据发生倾斜，数据较多的 Segment 就需要更长时间才能完成。因此，各个 Segment 的行数应大致相等，处理量也应大致相同。如果某个 Segment 需要处理的数据远多于其他 Segment，就可能导致性能下降或内存不足。

连接大型表时，合理的数据分布至关重要。执行连接要求匹配的行位于同一个 Segment 上。如果数据没有按同一个连接列分布，就会将其中一张表所需的行动态重分布到其他 Segment。有时会执行广播 Motion，即各个 Segment 将自己的行发送给所有其他 Segment，而不是执行重分布 Motion；后者由各个 Segment 重新对数据进行 hash，并根据 hash 键将行发送到相应的 Segment。

## 本地（同位）连接 {#local-co-located-joins}

采用能够将表行均匀分布到所有 Segment、并支持本地连接的 hash 分布，可以显著提升性能。如果待连接的行位于同一个 Segment 上，大部分处理就可以在该 Segment 实例内部完成。这称为*本地*或*同位*连接。本地连接尽可能减少数据移动；各个 Segment 独立运行，无需在 Segment 之间传输网络流量或通信。

对于经常连接的大型表，应按相同的列进行分布，以实现本地连接。本地连接要求连接两侧按相同的列（且顺序相同）分布，*并且*连接表时使用分布子句中的所有列。分布列还必须具有相同的数据类型：某些不同数据类型的值看起来表示相同，但存储方式不同，计算出的 hash 值也不同，因此会存储到不同的 Segment 上。

## 数据倾斜 {#data-skew}

分布键选择不当，或对表执行单元组插入、复制操作，都可能导致数据分布不均，从而产生数据倾斜。数据倾斜存在于表级，往往是查询性能不佳和内存不足的根本原因。数据倾斜不仅影响扫描（读取）性能，也会影响所有其他查询执行操作，例如连接和分组操作。

初次加载数据后，务必*验证*数据分布，以*确保*数据均匀分布。增量加载后*持续*验证数据分布同样重要。

以下查询显示每个 Segment 的行数，以及最大和最小行数之间的差异：

```sql
SELECT 'Example Table' AS "Table Name", 
    max(c) AS "Max Seg Rows", min(c) AS "Min Seg Rows", 
    (max(c)-min(c))*100.0/max(c) AS "Percentage Difference Between Max & Min" 
FROM (SELECT count(*) c, gp_segment_id FROM facts GROUP BY 2) AS a;
```

`gp_toolkit` 模式提供了两个视图，可用于检查数据倾斜。

- `gp_toolkit.gp_skew_coefficients` 视图通过计算各 Segment 上存储数据的变异系数（CV），展示数据分布倾斜情况。`skccoeff` 列显示变异系数（CV），其计算方式为标准差除以平均值。该指标同时考虑一组数据的平均值以及围绕平均值的波动程度。值越低越好，值越高则表示数据倾斜越严重。
- `gp_toolkit.gp_skew_idle_fractions` 视图通过计算表扫描期间系统空闲部分的占比，展示数据分布倾斜情况，这也是计算倾斜的指标。`siffraction` 列显示表扫描期间系统的空闲占比，可用于判断数据分布不均或查询处理倾斜。例如，0.1 表示倾斜度为 10%，0.5 表示倾斜度为 50%，依此类推。对于倾斜度超过 10% 的表，应评估其分布策略。

### 复制表的注意事项 {#considerations-for-replicated-tables}

创建复制表（使用 `CREATE TABLE` 的 `DISTRIBUTED REPLICATED` 子句）时，Apache Cloudberry 会将每一行分发到每个 Segment 实例。由于各个 Segment 上的行完全相同，复制表的数据分布是均匀的。如果通过查询复制表的 `gp_segment_id` 系统列来验证数据是否均匀分布，查询会失败，因为 Apache Cloudberry 不允许查询引用复制表的系统列。

## 处理倾斜 {#process-skew}

如果过多的数据流向一个或少数几个 Segment，并由其处理，就会产生处理倾斜。它往往是 Apache Cloudberry 性能和稳定性问题的根源，可能出现在连接、排序、聚合以及各种 OLAP 操作中。处理倾斜发生在查询运行过程中，不像数据倾斜那样容易检测。

如果发生故障的是个别 Segment，而非某台主机上的所有 Segment，就可能存在处理倾斜问题。目前，识别处理倾斜需要手动进行。首先检查是否存在溢出文件。如果有倾斜，但尚不足以导致溢出，就不会成为性能问题。如果确定存在倾斜，再找出导致倾斜的查询。

几乎所有处理倾斜问题都需要通过改写查询来解决。创建临时表可以消除倾斜。可以让临时表随机分布，强制执行两阶段聚合。
