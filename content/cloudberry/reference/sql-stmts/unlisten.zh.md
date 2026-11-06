---
title: "UNLISTEN"
description: "停止监听通知。"
weight: 1770
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/unlisten.md"
---

## 概要 {#synopsis}

```sql
UNLISTEN { <channel> | * }
```

## 描述 {#description}

`UNLISTEN` 用于移除现有的 `NOTIFY` 事件注册。`UNLISTEN` 取消当前 Apache Cloudberry 会话作为名为 channel 的通知通道监听者的现有注册。特殊通配符 `*` 取消当前会话的所有监听注册。

[NOTIFY](/cloudberry/reference/sql-stmts/notify/) 更详细地讨论了 `LISTEN` 和 `NOTIFY` 的用法。

## 参数 {#parameters}

**`channel`**

通知通道的名称（任意标识符）。

**`*`**

清除本会话当前的所有监听注册。

## 注意事项 {#notes}

可以对未监听的通道取消监听，不会产生警告或错误。

每个会话结束时，都会自动执行 `UNLISTEN *`。

执行过 `UNLISTEN` 的事务不能为两阶段提交做准备。

## 示例 {#examples}

进行注册：

```sql
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

执行 `UNLISTEN` 后，后续 `NOTIFY` 消息会被忽略：

```sql
UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

## 兼容性 {#compatibility}

SQL 标准中没有 `UNLISTEN` 语句。

## 另见 {#see-also}

[LISTEN](/cloudberry/reference/sql-stmts/listen/), [NOTIFY](/cloudberry/reference/sql-stmts/notify/)
