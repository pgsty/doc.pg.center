---
title: "LISTEN"
description: "监听通知。"
weight: 1510
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/listen.md"
---

## 概要 {#synopsis}

```sql
LISTEN <channel>
```

## 描述 {#description}

`LISTEN` 将当前会话注册为名为 channel 的通知通道的监听者。如果当前会话已经注册为该通知通道的监听者，则不执行任何操作。

当本会话或连接到同一数据库的其他会话调用 `NOTIFY <channel>` 命令时，所有当前监听该通知通道的会话都会收到通知，并各自通知与之连接的客户端应用程序。

可以使用 `UNLISTEN` 命令取消会话在指定通知通道上的注册。会话结束时，其监听注册会自动清除。

客户端应用程序检测通知事件的方法取决于所使用的 PostgreSQL 应用编程接口。使用 `libpq` 库时，应用程序像普通 SQL 命令一样发出 `LISTEN`，然后必须定期调用 `PQnotifies()` 函数，检查是否收到了通知事件。其他接口（例如 `libpgtcl`）提供更高层次的通知事件处理方法；实际上，使用 `libpgtcl` 时，应用程序开发者甚至不应直接发出 `LISTEN` 或 `UNLISTEN`。详情请参考所用接口的文档。

[NOTIFY](/cloudberry/reference/sql-stmts/notify/) 更详细地讨论了 `LISTEN` 和 `NOTIFY` 的用法。

## 参数 {#parameters}

**`channel`**

通知通道的名称（任意标识符）。

## 注意事项 {#notes}

`LISTEN` 在事务提交时生效。如果在事务中执行 `LISTEN` 或 `UNLISTEN`，而该事务随后回滚，则监听的通知通道集合不会改变。

执行过 `LISTEN` 的事务不能为两阶段提交做准备。

## 示例 {#examples}

从 `psql` 配置并执行监听和通知操作：

```sql
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

## 兼容性 {#compatibility}

SQL 标准中没有 `LISTEN` 语句。

## 另见 {#see-also}

[NOTIFY](/cloudberry/reference/sql-stmts/notify/), [UNLISTEN](/cloudberry/reference/sql-stmts/unlisten/)
