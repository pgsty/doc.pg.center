---
title: "pg_attribute"
description: "`pg_catalog` 模式中的 `pg_attribute` 表存储表列的信息。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-attribute.md"
---

数据库中每张表的每一列在 `pg_attribute` 中都恰好对应一行。（索引以及所有在 `pg_class` 中有条目的对象也都有属性条目。）术语“属性”等同于“列”。

在已删除列的 `pg_attribute` 条目中，`atttypid` 会重置为零，但 `attlen` 和其他从 `pg_type` 复制的字段仍然有效。这种安排是为了处理以下情况：已删除列的数据类型后来也被删除，因此不再有对应的 `pg_type` 行。`attlen` 和其他字段可用于解释表中一行的内容。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`attrelid`|oid|`pg_class.oid`|此列所属的表。|
|`attname`|name| |列名。|
|`atttypid`|oid|`pg_type.oid`|此列的数据类型。|
|`attstattarget`|integer| |控制 `ANALYZE` 为此列收集统计信息的详细程度。零表示不收集统计信息，负值表示使用系统默认统计目标。正值的确切含义取决于数据类型。对于标量数据类型，它既是要收集的“高频值”的目标数量，也是要创建的直方图桶的目标数量。|
|`attlen`|smallint| |此列数据类型的 `pg_type.typlen` 的副本。|
|`attnum`|smallint| |列号。普通列从 1 开始编号。系统列（例如 `ctid`）使用任意指定的负数编号。|
|`attndims`|integer| |如果此列为数组类型，则为数组维数；否则为 `0`。（目前并不强制检查数组维数，因此任何非零值实际上都表示这是一个数组。）|
|`attcacheoff`|integer| |存储时始终为 `-1`；装入内存中的行描述符后，可能更新为此属性在行内的偏移量缓存。|
|`atttypmod`|integer| |记录创建表时提供的类型相关数据（例如 `varchar` 列的最大长度）。它会传递给类型相关的输入函数和长度强制转换函数。对于不需要此信息的类型，该值通常为 `-1`。|
|`attbyval`|boolean| |此列数据类型的 `pg_type.typbyval` 的副本。|
|`attstorage`|char| |通常是此列数据类型的 `pg_type.typstorage` 的副本。对于支持 TOAST 的数据类型，可以在创建列之后修改此值以控制存储策略。|
|`attalign`|char| |此列数据类型的 `pg_type.typalign` 的副本。|
|`attnotnull`|boolean| |表示非空约束。|
| `attcompression` | char | |此列的压缩类型。有效值为 `n`（不压缩）、`r`（游程编码）、`z`（zlib）和 `s`（snappy）。|
|`atthasdef`|boolean| |此列具有默认表达式或生成表达式，此时 `pg_attrdef` 目录中会有对应条目来实际定义该值。（检查 `attgenerated` 可确定它是默认表达式还是生成表达式。）|
|`atthasmissing`|boolean| |此列具有一个值，供该列在数据行中完全缺失时使用；在行创建之后添加带有非易失性 `DEFAULT` 值的列时，就会出现这种情况。实际使用的值存储在 `attmissingval` 列中。|
|`attidentity`|char| |若为零字节（''），则不是标识列。否则，`a` 表示总是生成，`d` 表示默认生成。|
|`attgenerated`|char| |若为零字节（''），则不是生成列。否则，`s` 表示存储式。（将来可能增加其他值。）|
|`attisdropped`|boolean| |此列已删除，不再有效。已删除的列在物理上仍存在于表中，但解析器会忽略它，因此无法通过 SQL 访问。|
|`attislocal`|boolean| |此列在关系中本地定义。注意，一列可以同时由本地定义并从父表继承。|
|`attinhcount`|integer| |此列的直接祖先数量。祖先数量非零的列既不能删除，也不能重命名。|
|`attcollation`|oid|`pg_collation.oid`|为此列定义的排序规则；如果此列的数据类型不支持排序规则，则为零。|
|`attacl`|aclitem[]| |专门授予此列的列级访问权限（如果有）。|
|`attoptions`|text[]| |属性级选项，以“keyword=value”字符串表示。|
|`attfdwoptions`|text[]| |属性级外部数据包装器选项，以“keyword=value”字符串表示。|
|`attmissingval`|anyarray| |此列包含一个单元素数组，其中的值供该列在数据行中完全缺失时使用；在行创建之后添加带有非易失性 `DEFAULT` 值的列时，就会出现这种情况。只有 `atthasmissing` 为 `true` 时才使用此值。如果没有这样的值，此列为 NULL。|
