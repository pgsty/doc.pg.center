---
title: "pg_depend"
description: "`pg_depend` 系统目录表记录数据库对象之间的依赖关系。"
weight: 180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-depend.md"
---

这些信息让 `DROP` 命令能够确定执行 `DROP CASCADE` 时还必须删除哪些对象，或在使用 `DROP RESTRICT` 时阻止删除。另见 [pg_shdepend](/cloudberry/reference/sys-catalogs/sys-tables/pg-shdepend/)，它对涉及 Cloudberry 系统共享对象的依赖关系提供类似功能。

在所有情况下，`pg_depend` 条目都表示：若不同时删除依赖对象，就不能删除被引用对象。不过，`deptype` 标识了几种不同的子类型：

- **DEPENDENCY_NORMAL (n)** — 独立创建的对象之间的普通依赖关系。删除依赖对象不会影响被引用对象。只有指定 `CASCADE` 才能删除被引用对象，此时依赖对象也会一并删除。例如：表列对其数据类型具有普通依赖。
- **DEPENDENCY_AUTO (a)** — 依赖对象可以独立于被引用对象删除；如果被引用对象被删除，则无论使用 `RESTRICT` 还是 `CASCADE` 模式，依赖对象都应自动删除。例如：表上的命名约束自动依赖于该表，因此删除表时该约束也会删除。
- **DEPENDENCY_INTERNAL (i)** — 依赖对象是在创建被引用对象时一同创建的，实际上只是其内部实现的一部分。直接对依赖对象执行 `DROP` 会被明确禁止（应改为对被引用对象执行 `DROP`）。对被引用对象执行 `DROP` 时，无论是否指定 `CASCADE`，都会传播到依赖对象并将其删除。如果依赖对象因为它依赖的某个其他对象被移除而必须删除，则该删除操作会转换为删除被引用对象，因此依赖对象的 `NORMAL` 和 `AUTO` 依赖表现得如同被引用对象的依赖。例如：视图的 `ON SELECT` 规则内部依赖于视图，不能在保留视图的同时删除该规则。规则的依赖（如它引用的表）表现得如同视图的依赖。
- **DEPENDENCY_PARTITION_PRI (P)**、**DEPENDENCY_PARTITION_SEC (S)** — 依赖对象是在创建被引用对象时一同创建的，实际上只是其内部实现的一部分；但与 `INTERNAL` 不同，这里有多个被引用对象。只有其中至少一个被引用对象被删除时，才能删除依赖对象；只要删除其中任意一个，无论是否指定 `CASCADE`，依赖对象都应删除。与 `INTERNAL` 的另一处区别是，删除依赖对象所依赖的其他对象时，不会自动删除任何通过分区依赖引用的对象。因此，如果删除操作没有通过其他路径级联到这些对象中的至少一个，就会被拒绝。（多数情况下，依赖对象的所有非分区依赖都与至少一个通过分区依赖引用的对象共享，因此该限制不会阻止级联删除。）主要分区依赖和次要分区依赖的行为相同，只是在错误信息中优先使用主要依赖；因此，具有分区依赖的对象应有一个主要分区依赖，以及一个或多个次要分区依赖。注意，分区依赖是在对象通常具有的依赖之外额外添加的，而不是替代后者。这简化了 `ATTACH/DETACH PARTITION` 操作：只需添加或移除分区依赖即可。例如：子分区索引同时对它所在的分区表和父分区索引建立分区依赖，因此删除其中任意一个时，子分区索引都会删除，其他情况下则不会。对父索引的依赖是主要依赖，因此用户尝试删除子分区索引时，错误信息会建议改为删除父索引，而不是删除表。
- **DEPENDENCY_EXTENSION (e)** — 被引用对象是一个扩展，依赖对象是该扩展的成员（见 `pg_extension`）。只有对被引用对象执行 `DROP EXTENSION` 才能删除依赖对象。此依赖类型在功能上与 `INTERNAL` 相同，但为使语义清晰并简化 pg_dump 而单独区分。
- **DEPENDENCY_AUTO_EXTENSION (x)** — 被引用对象是一个扩展，但依赖对象不是该扩展的成员（因此 pg_dump 不应忽略它）；不过，没有该扩展，依赖对象就无法工作，因此扩展被删除时也应自动删除它。依赖对象也可以单独删除。此依赖类型在功能上与 `AUTO` 相同，但为使语义清晰并简化 pg_dump 而单独区分。
- **DEPENDENCY_PIN (p)** — 没有依赖对象；此类条目表示系统自身依赖于被引用对象，因此绝不能删除该对象。此类条目只在系统初始化时创建。依赖对象对应的各列均为零。

注意，两个对象之间完全可能由多个 `pg_depend` 条目关联。例如：子分区索引对其所在的分区表具有分区依赖，同时对该表中被索引的每一列具有自动依赖。这表示多种依赖语义的并集。只要任一依赖满足自动删除条件，就可以不指定 `CASCADE` 而删除依赖对象。另一方面，所有依赖对哪些对象必须一起删除的限制，都必须得到满足。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`classid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid|依赖对象所在系统目录的对象标识符。|
|`objid`|oid|任意 OID 列|具体依赖对象的对象标识符。|
|`objsubid`|integer| |对于表列，此值为列号（`objid` 和 `classid` 指向表本身）。对于其他所有对象类型，此列为零。|
|`refclassid`|oid|[pg_class](/cloudberry/reference/sys-catalogs/sys-tables/pg-class/).oid|被引用对象所在系统目录的对象标识符。|
|`refobjid`|oid|任意 OID 列|具体被引用对象的对象标识符。|
|`refobjsubid`|integer| |对于表列，此值为被引用列的列号（`refobjid` 和 `refclassid` 指向表本身）。对于其他所有对象类型，此列为零。|
|`deptype`|char| |定义此依赖关系具体语义的代码。|
