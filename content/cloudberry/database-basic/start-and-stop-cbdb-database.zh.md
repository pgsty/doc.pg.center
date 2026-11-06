---
title: "启动与停止 Apache Cloudberry"
linkTitle: "启动与停止数据库"
description: "在 Apache Cloudberry 数据库管理系统（DBMS）中，数据库服务器实例（Coordinator 和所有 Segment）需要在系统的所有主机上协调启动或停止，使其能够作为统一的 DBMS 协同工作。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/database-basic/start-and-stop-cbdb-database.md"
---

由于 Apache Cloudberry 系统分布在多台机器上，其启动和停止过程与普通 PostgreSQL 数据库管理系统（DBMS）不同。

分别使用 `gpstart` 和 `gpstop` 实用程序启动和停止 Apache Cloudberry。这些实用程序位于 Apache Cloudberry Coordinator 主机上的 `$GPHOME/bin` 目录中。

> [!TIP] 提示
> 不要使用 `kill` 命令结束任何 Postgres 进程，应使用数据库命令 `pg_cancel_backend()`。

执行 `kill -9` 或 `kill -11` 可能导致数据库损坏，并使根本原因分析无法进行。

## 启动 Apache Cloudberry {#start-apache-cloudberry}

在 Coordinator 实例上运行 `gpstart` 实用程序，启动已初始化的 Apache Cloudberry 系统。

使用 `gpstart` 实用程序，可以启动已通过 `gpinitsystem` 实用程序初始化、随后通过 `gpstop` 实用程序停止的 Apache Cloudberry 系统。`gpstart` 实用程序通过启动 Apache Cloudberry 集群中的所有 `postgres` 实例来启动 Apache Cloudberry。`gpstart` 负责协调和并行执行这一过程。

在 Coordinator 主机上运行 `gpstart`，启动 Apache Cloudberry：

```shell
$ gpstart
```

## 重启 Apache Cloudberry {#restart-apache-cloudberry}

停止 Apache Cloudberry 系统，然后重新启动。

为 `gpstop` 实用程序指定 `-r` 选项，可以先停止 Apache Cloudberry，待关闭完成后再重新启动。

要重启 Apache Cloudberry，请在 Coordinator 主机上输入以下命令：

```shell
$ gpstop -r
```

## 仅重新加载配置文件更改 {#reload-configuration-file-changes-only}

在不中断系统运行的情况下，重新加载对 Apache Cloudberry 配置文件所做的更改。

`gpstop` 实用程序可以在不中断服务的情况下，重新加载对 `pg_hba.conf` 配置文件和 Coordinator 的 `postgresql.conf` 文件中*运行时*参数所做的更改。活动会话重新连接数据库后才会应用这些更改。许多服务器配置参数需要完整重启系统（`gpstop -r`）才能生效。

使用 `gpstop` 实用程序，在不关闭 Apache Cloudberry 系统的情况下重新加载配置文件更改：

```shell
$ gpstop -u
```

## 以维护模式启动 Coordinator {#start-the-coordinator-in-maintenance-mode}

只启动 Coordinator，以执行维护或管理任务，而不影响 Segment 上的数据。例如，可以在维护模式下仅连接 Coordinator 实例上的数据库，并修改系统目录设置。

1. 运行 `gpstart`，并指定 `-m` 选项：

    ```shell
    $ gpstart -m
    ```

2. 以维护模式连接 Coordinator，维护系统目录。例如：

    ```shell
    $ PGOPTIONS='-c gp_role=utility' psql postgres
    ```

3. 完成管理任务后，停止处于维护模式的 Coordinator，然后以生产模式重新启动。

    ```shell
    $ gpstop -m
    $ gpstart
    ```

    > [!WARNING] 警告
    > 不正确地使用维护模式连接可能导致系统状态不一致。建议由技术支持人员执行此操作。

## 停止 Apache Cloudberry {#stop-apache-cloudberry}

`gpstop` 实用程序用于停止或重启 Apache Cloudberry 系统，始终在 Coordinator 主机上运行。启动后，`gpstop` 会停止系统中的所有 `postgres` 进程，包括 Coordinator 和所有 Segment 实例。`gpstop` 实用程序默认可使用多个并行工作线程来停止构成 Apache Cloudberry 集群的 Postgres 实例。要立即停止 Apache Cloudberry，请使用快速模式。

> [!TIP] 提示
> 不建议使用立即关闭模式。此模式会停止所有数据库进程，不会让数据库服务器完成事务处理，也不会清理任何临时工作文件或正在使用的工作文件。

- 停止 Apache Cloudberry：

    ```shell
    $ gpstop
    ```

- 以快速模式停止 Apache Cloudberry：

    ```shell
    $ gpstop -M fast
    ```

    默认情况下，如果仍有客户端连接数据库，就不允许关闭 Apache Cloudberry。使用 `-M fast` 选项可以在关闭前回滚所有进行中的事务，并终止所有连接。

## 停止客户端进程 {#stop-client-processes}

Apache Cloudberry 为每个客户端连接启动一个新的后端进程。具有 `SUPERUSER` 权限的 Apache Cloudberry 用户可以取消或终止这些客户端后端进程。

使用 `pg_cancel_backend()` 函数取消后端进程，会结束某个特定的排队中或正在执行的客户端查询。使用 `pg_terminate_backend()` 函数终止后端进程，则会终止客户端与数据库的连接。

`pg_cancel_backend()` 函数有两种签名：

- `pg_cancel_backend( pid int4 )`
- `pg_cancel_backend( pid int4, msg text )`

`pg_terminate_backend()` 函数也有两种类似的签名：

- `pg_terminate_backend( pid int4 )`
- `pg_terminate_backend( pid int4, msg text )`

如果提供 `msg`，Apache Cloudberry 会将该文本包含在返回给客户端的取消消息中。`msg` 的长度限制为 128 字节，超出部分会被 Apache Cloudberry 截断。

`pg_cancel_backend()` 和 `pg_terminate_backend()` 函数在成功时返回 `true`，否则返回 `false`。

要取消或终止后端进程，必须先确定该后端的进程 ID。可以从 `pg_stat_activity` 视图的 `pid` 列中获取进程 ID。例如，要查看与所有正在执行和排队中的查询相关的进程信息：

```sql
SELECT usename, pid, state, query, datname
     FROM pg_stat_activity;
```

查询输出示例（部分）：

```sql
usename |  pid     | state  |         query          | datname
---------+-------------------+--------+------------------------+---------
  sammy  |   31861  | idle   | SELECT * FROM testtbl; | testdb
  billy  |   31905  | active | SELECT * FROM topten;  | testdb
```

通过输出确定查询或客户端连接对应的进程 ID（`pid`）。

例如，要取消上方示例输出中标识的等待中的查询，并将 `'Admin canceled long-running query.'` 包含在返回给客户端的消息中：

```sql
=# SELECT pg_cancel_backend(31905 ,'Admin canceled long-running query.');

ERROR:  canceling statement due to user request: "Admin canceled long-running query."
```
