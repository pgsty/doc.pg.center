---
title: "pg_cursors"
description: "`pg_cursors` 视图列出当前可用的游标。"
weight: 160
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-views/pg-cursors.md"
---

可以通过以下方式之一来定义游标：

- 通过 DECLARE SQL 语句
- 通过前端／后端协议中的 Bind 消息
- 通过服务器编程接口（SPI）

    请注意，Apache Cloudberry 不支持通过 SPI 定义或访问并行检索游标。

除非声明了 `WITH HOLD`，否则游标仅在定义它的事务存续期间存在。不可保持的游标仅在创建它的事务结束前出现在此视图中。

> [!NOTE]
> Apache Cloudberry 不支持可保持的并行检索游标。

|名称|类型|引用|说明|
|----|----|----------|-----------|
|`name`|text| |游标名称。|
|`statement`|text| |声明此游标时提交的原始查询字符串。|
|`is_holdable`|boolean| |如果游标可保持（即声明它的事务提交后仍可访问），则为 `true`；否则为 `false`。<br/><br/>> **注意** Apache Cloudberry 不支持可保持的并行检索游标，此类游标的该值始终为 `false`。|
|`is_binary`|boolean| |如果声明游标时指定了 `BINARY`，则为 `true`；否则为 `false`。|
|`is_scrollable`|boolean| |如果游标可滚动（即允许以非顺序方式检索行），则为 `true`；否则为 `false`。<br/><br/>> **注意** Apache Cloudberry 不支持可滚动游标，此值始终为 `false`。|
|`creation_time`|timestamptz| |声明游标的时间。|
|`is_parallel`|boolean| |如果声明游标时指定了 `PARALLEL RETRIEVE`，则为 `true`；否则为 `false`。|
