---
title: "pg_aggregate"
description: "`pg_catalog` 模式中的 `pg_aggregate` 表存储聚合函数的信息。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-aggregate.md"
---

聚合函数对一组值（通常是满足查询条件的每一行中某一列的值）进行操作，并返回由这些值计算出的单个值。典型的聚合函数有 `sum`、`count` 和 `max`。`pg_aggregate` 中的每个条目都是 `pg_proc` 中某个条目的扩展。`pg_proc` 条目记录聚合的名称、输入和输出数据类型，以及与普通函数类似的其他信息。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`aggfnoid`|regproc|`pg_proc.oid`|聚合函数的 OID。|
|`aggkind`|char| |聚合种类：`n` 表示*普通*聚合，`o` 表示*有序集*聚合，`h` 表示*假想集*聚合。|
|`aggnumdirectargs`|smallint| |有序集或假想集聚合的直接（非聚合）参数个数，一个可变参数数组计为一个参数。如果等于 `pronargs`，该聚合必须是可变参数聚合，且可变参数数组同时描述聚合参数和末尾的直接参数。普通聚合始终为零。|
|`aggtransfn`|regproc|`pg_proc.oid`|转移函数的 OID。|
|`aggfinalfn`|regproc|`pg_proc.oid`|最终函数的 OID（没有则为零）。|
|`aggcombinefn`|regproc|`pg_proc.oid`|合并函数的 OID（没有则为零）。|
|`aggserialfn`|regproc|`pg_proc.oid`|将 transtype 转换为 `bytea` 的序列化函数的 OID（没有则为零）。|
|`aggdeserialfn`|regproc|`pg_proc.oid`|将 `bytea` 转换为 transtype 的反序列化函数的 OID（没有则为零）。|
|`aggmtransfn`|regproc|`pg_proc.oid`|移动聚合模式下前向转移函数的 OID（没有则为零）。|
|`aggminvtransfn`|regproc|`pg_proc.oid`|移动聚合模式下逆向转移函数的 OID（没有则为零）。|
|`aggmfinalfn`|regproc|`pg_proc.oid`|移动聚合模式下最终函数的 OID（没有则为零）。|
|`aggfinalextra`|bool| |为真时，向 `aggfinalfn` 传递额外的虚拟参数。|
|`aggmfinalextra`|bool| |为真时，向 `aggmfinalfn` 传递额外的虚拟参数。|
|`aggfinalmodify`|char| |指示 `aggfinalfn` 是否修改转移状态。|
|`aggmfinalmodify`|char| |指示 `aggmfinalfn` 是否修改转移状态。|
|`aggsortop`|oid|`pg_operator.oid`|关联的排序操作符的 OID（没有则为零）。|
|`aggtranstype`|oid|`pg_type.oid`|聚合函数内部转移（状态）数据的数据类型。|
|`aggtransspace`|integer| |转移状态数据的近似平均大小（字节）；零表示使用默认估算值。|
|`aggmtranstype`|oid|`pg_type.oid`|移动聚合模式下聚合函数内部转移（状态）数据的数据类型（没有则为零）。|
|`aggmtransspace`|integer| |移动聚合模式下转移状态数据的近似平均大小（字节）；零表示使用默认估算值。|
|`agginitval`|text| |转移状态的初始值。这是一个文本字段，包含初始值的外部字符串表示。如果此字段为 NULL，转移状态的起始值也是 NULL。|
|`aggminitval`|text| |移动聚合模式下转移状态的初始值。这是一个文本字段，包含初始值的外部字符串表示。如果此字段为 NULL，转移状态的起始值也是 NULL。|
| `aggrepsafeexec` | bool | |如果该聚合可以安全地并行执行，则为真。|
