---
title: "RESET"
description: "将运行时系统配置参数的值恢复为默认值。"
weight: 1610
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/reset.md"
---

## 概要 {#synopsis}

```sql
RESET <configuration_parameter>

RESET ALL
```

## 描述 {#description}

`RESET` 将系统配置参数恢复为默认值。`RESET` 等效于以下命令：

``` sql
SET <configuration_parameter> TO DEFAULT
```

详情见 [SET](/cloudberry/reference/sql-stmts/set/)。

默认值是指当前会话从未对该参数发出过 `SET` 时，该参数本应具有的值。此值的实际来源可能是编译时内置的默认值、Coordinator 的 `postgresql.conf` 配置文件、命令行选项，或按数据库、按用户设置的默认值。这与“参数在会话开始时的值”有细微区别：如果值来自配置文件，就会重置为配置文件当前指定的值。更多信息见“服务器配置参数”。

`RESET` 的事务行为与 `SET` 相同：事务回滚会撤销其效果。

## 参数 {#parameters}

**`configuration_parameter`**

可设置的运行时系统配置参数名称。详情见“服务器配置参数”。

**`ALL`**

将所有可设置的运行时配置参数重置为默认值。

## 示例 {#examples}

将配置参数 `statement_mem` 设为默认值：

```sql
RESET statement_mem; 
```

## 兼容性 {#compatibility}

`RESET` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[SET](/cloudberry/reference/sql-stmts/set/), [SHOW](/cloudberry/reference/sql-stmts/show/)
