---
title: "pg_amop"
description: "`pg_catalog` 模式中的 `pg_amop` 表存储与索引访问方法操作符类关联的操作符信息。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-amop.md"
---

操作符类中的每个成员操作符在此表中各有一行。

条目的 `amopmethod` 必须与其所属操作符族的 `opfmethod` 一致（在这里包含 `amopmethod`，是出于性能考虑而有意对目录结构进行的反规范化）。此外，`amoplefttype` 和 `amoprighttype` 必须与所引用的 `pg_operator` 条目中的 `oprleft` 和 `oprright` 字段一致。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`amopfamily`|oid| `pg_opfamily.oid` |此条目所属的操作符族。|
|`amoplefttype`|oid|`pg_type.oid`|操作符左侧输入的数据类型。|
|`amoprighttype`|oid|`pg_type.oid`|操作符右侧输入的数据类型。|
|`amopstrategy`|smallint| |操作符策略编号。|
|`amoppurpose`|char| |操作符用途：`s` 表示搜索，`o` 表示排序。|
|`amopopr`|oid|`pg_operator.oid`|操作符的 OID。|
|`amopmethod`|oid|`pg_am.oid`|操作符族的索引访问方法。|
|`amopsortfamily`|oid|`pg_opfamily.oid`|如果是排序操作符，则为此条目排序所依据的 B-树操作符族；如果是搜索操作符，则为零。|
