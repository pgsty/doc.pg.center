---
title: "pg_amproc"
description: "`pg_catalog` 模式中的 `pg_amproc` 表存储与索引访问方法操作符类关联的支持过程信息。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-amproc.md"
---

属于操作符类的每个支持过程在此表中各有一行。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`amprocfamily`|oid|`pg_opfamily.oid`|此条目所属的操作符族。|
|`amproclefttype`|oid|`pg_type.oid`|关联操作符左侧输入的数据类型。|
|`amprocrighttype`|oid|`pg_type.oid`|关联操作符右侧输入的数据类型。|
|`amprocnum`|smallint| |支持过程编号。|
|`amproc`|regproc|`pg_proc.oid`|过程的 OID。|
