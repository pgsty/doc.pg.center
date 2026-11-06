---
title: "pg_rewrite"
description: "`pg_rewrite` 系统目录表存储表和视图的重写规则。"
weight: 320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-rewrite.md"
---

如果一个表在此目录中有任何规则，其 `pg_class.relhasrules` 就必须为 true。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID|
|`rulename`|name||规则名称|
|`ev_class`|oid|pg_class.oid|此规则所属的表|
|`ev_type`|char||规则对应的事件类型：1 = SELECT，2 = UPDATE，3 = INSERT，4 = DELETE|
|`ev_enabled`|char||控制规则在哪种会话复制角色模式下触发。始终为 O，表示规则在 origin 模式下触发。|
|`is_instead`|boolean||如果规则是 `INSTEAD` 规则，则为 true|
|`ev_qual`|pg_node_tree||规则限定条件的表达式树（以 `nodeToString()` 形式表示）|
|`ev_action`|pg_node_tree||规则动作的查询树（以 `nodeToString()` 形式表示）|
