---
title: "pg_shdepend"
description: "`pg_shdepend` 系统目录表记录数据库对象与角色等共享对象之间的依赖关系。"
weight: 340
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-shdepend.md"
---

这些信息使 Apache Cloudberry 能够在尝试删除这些对象之前，确保没有对象引用它们。另请参阅 [pg_depend](/cloudberry/reference/sys-catalogs/sys-tables/pg-depend/)，它为单个数据库内的对象依赖关系提供类似功能。与大多数系统目录不同，`pg_shdepend` 由 Cloudberry 系统中的所有数据库共享：每个系统只有一份 `pg_shdepend`，而不是每个数据库一份。

在所有情况下，`pg_shdepend` 条目都表示：除非同时删除依赖对象，否则不能删除被引用对象。不过，依赖关系还分为几种子类型，由 `deptype` 标识：

- **SHARED_DEPENDENCY_OWNER (o)** — 被引用对象（必须是角色）是依赖对象的所有者。
- **SHARED_DEPENDENCY_ACL (a)** — 依赖对象的 ACL（访问控制列表）中提到了被引用对象（必须是角色）。
- **SHARED_DEPENDENCY_PIN (p)** — 没有依赖对象；这种条目表示系统本身依赖被引用对象，因此绝不能删除该对象。这种条目仅在系统初始化时创建。依赖对象对应的列均为零。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`dbid`|oid|pg_database.oid|依赖对象所在数据库的 OID；对于共享对象，此值为零。|
|`classid`|oid|pg_class.oid|依赖对象所在系统目录的 OID。|
|`objid`|oid|任意 OID 列|具体依赖对象的 OID。|
|`objsubid`|integer| |对于表列，此值是列号。对于其他所有对象类型，此列为零。|
|`refclassid`|oid|pg_class.oid|被引用对象所在系统目录的 OID（必须是共享目录）。|
|`refobjid`|oid|任意 OID 列|具体被引用对象的 OID。|
|`deptype`|char| |定义此依赖关系具体语义的代码。|
