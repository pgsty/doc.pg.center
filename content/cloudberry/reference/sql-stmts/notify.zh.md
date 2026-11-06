---
title: "NOTIFY"
description: "生成通知。"
weight: 1550
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/notify.md"
---

## 语法概要 {#synopsis}

```sql
NOTIFY <channel> [ , <payload> ]
```

## 说明 {#description}

`NOTIFY` 命令向当前数据库中先前对指定通道名执行过 `LISTEN <channel>` 的每个客户端应用发送通知事件，并可附带一个“载荷”字符串。通知对所有用户可见。

`NOTIFY` 为访问同一 Apache Cloudberry 的一组进程提供简单的进程间通信机制。通知可以附带载荷字符串，也可以利用数据库表将其他数据从通知方传递给监听方，从而构建传递结构化数据的更高层机制。

通知事件传递给客户端的信息包括通知通道名、通知会话的服务器进程 PID 和载荷字符串；未指定载荷时为空字符串。

数据库设计者负责定义数据库中使用的通道名及其含义。通道名通常与数据库中的某个表名相同，通知事件实质上表示：“我更改了这个表，看看有什么新内容。”但 `NOTIFY` 和 `LISTEN` 命令并不强制要求这种关联。例如，数据库设计者可以使用不同通道名表示单个表发生的不同类型的变化，也可以用载荷字符串区分各种情况。

使用 `NOTIFY` 表示某个表发生变化时，一种有用的编程技巧是将 `NOTIFY` 放入由表更新触发的语句触发器。这样，表发生变化时会自动发送通知，应用程序员不会意外忘记发送。

`NOTIFY` 与 SQL 事务之间有一些重要的交互。首先，在事务内执行 `NOTIFY` 时，只有事务提交后才会投递通知事件。这是合理的，因为如果事务中止，其中所有命令（包括 `NOTIFY`）都不会产生效果。但如果期望立即投递通知事件，这可能令人困惑。其次，如果监听会话在事务内收到通知信号，只有该事务完成（提交或中止）之后，通知事件才会投递给其连接的客户端。同样，这是因为如果在事务中投递通知后事务又中止，人们会希望以某种方式撤销通知，但服务器一旦将通知发给客户端就无法“收回”。因此，通知事件只在事务之间投递。这意味着，使用 `NOTIFY` 进行实时信号传递的应用应尽量缩短事务。

如果同一事务多次向同一通道名发送载荷字符串相同的通知，数据库服务器可以决定只投递一次通知。另一方面，Apache Cloudberry 始终将载荷字符串不同的通知分别投递。同样，来自不同事务的通知永远不会合并为一次通知。除丢弃后续重复通知外，`NOTIFY` 保证同一事务的通知按发送顺序投递，还保证不同事务的消息按事务提交顺序投递。

执行 `NOTIFY` 的客户端自身也监听同一通知通道是常见情况。此时，它会像其他所有监听会话一样收到通知事件。根据应用逻辑，这可能导致无用的工作，例如读取数据库表，却只发现该会话刚刚写入的更新。可以检查通知会话的服务器进程 PID（由通知事件消息提供）是否与自身会话 PID（可从 `libpq` 获取）相同，从而避免这种额外工作。如果相同，该通知事件只是自身操作返回的回声，可以忽略。

## 参数 {#parameters}

**`channel`**

通知通道的名称（任意标识符）。

**`payload`**

要随通知一起传递的“载荷”字符串。必须指定为简单字符串字面量。默认配置下，它必须小于 8000 字节。（如果需要传递二进制数据或大量信息，最好将其放入数据库表中，并发送记录的键。）

## 注意事项 {#notes}

有一个队列用于保存已经发送但尚未由所有监听会话处理的通知。如果队列已满，调用 `NOTIFY` 的事务将在提交时失败。队列很大（标准安装为 8GB），几乎能满足所有使用场景。不过，如果某会话执行 `LISTEN` 后进入一个持续很长时间的事务，就无法进行清理。当队列达到一半容量时，日志文件会出现警告，指出阻止清理的会话。此时应确保该会话结束当前事务，以便继续清理。

函数 `pg_notification_queue_usage()` 返回当前待处理通知占用队列的比例。

执行过 `NOTIFY` 的事务不能为两阶段提交进行准备。

### Pg_notify {#pg_notify}

也可以使用函数 `pg_notify(text, text)` 发送通知。该函数的第一个参数为通道名，第二个参数为载荷。如果需要使用非常量的通道名和载荷，该函数比 `NOTIFY` 命令更容易使用。

## 示例 {#examples}

在 `psql` 中配置并执行监听/通知序列：

```sql
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
NOTIFY virtual, 'This is the payload';
Asynchronous notification "virtual" with payload "This is the payload" received from server process with PID 8448.

LISTEN foo;
SELECT pg_notify('fo' || 'o', 'pay' || 'load');
Asynchronous notification "foo" with payload "payload" received from server process with PID 14728.
```

## 兼容性 {#compatibility}

SQL 标准中没有 `NOTIFY` 语句。

## 另请参阅 {#see-also}

[LISTEN](/cloudberry/reference/sql-stmts/listen/), [UNLISTEN](/cloudberry/reference/sql-stmts/unlisten/)
