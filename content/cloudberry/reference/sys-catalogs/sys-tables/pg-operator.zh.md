---
title: "pg_operator"
description: "`pg_operator` 系统目录表存储操作符的信息，包括内置操作符和使用 `CREATE OPERATOR` 定义的操作符。"
weight: 230
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-operator.md"
---

未使用的列包含零。例如，前缀操作符的 `oprleft` 为零。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`oprname`|name| |操作符名称。|
|`oprnamespace`|oid|pg_namespace.oid|包含此操作符的名字空间的 OID。|
|`oprowner`|oid|pg_authid.oid|操作符的所有者。|
|`oprkind`|char| |`b` = 中缀（两侧），`l` = 前缀（左侧），`r` = 后缀（右侧）。|
|`oprcanmerge`|boolean| |此操作符支持归并连接。|
|`oprcanhash`|boolean| |此操作符支持哈希连接。|
|`oprleft`|oid|pg_type.oid|左操作数的类型。|
|`oprright`|oid|pg_type.oid|右操作数的类型。|
|`oprresult`|oid|pg_type.oid|结果的类型。|
|`oprcom`|oid|pg_operator.oid|此操作符的交换操作符（如果有）。|
|`oprnegate`|oid|pg_operator.oid|此操作符的否定操作符（如果有）。|
|`oprcode`|regproc|pg_proc.oid|实现此操作符的函数。|
|`oprrest`|regproc|pg_proc.oid|此操作符的限制选择率估算函数。|
|`oprjoin`|regproc|pg_proc.oid|此操作符的连接选择率估算函数。|
