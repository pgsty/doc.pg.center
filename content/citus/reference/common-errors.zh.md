---
title: 常见错误消息
description: 了解如何解决常见的 Citus 错误，以便可以维护可靠的分布式 PostgreSQL 应用程序。
weight: 120
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/common-errors?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

使用 Citus 分布式数据库时，可能遇到与连接、事务、约束和分布式操作有关的错误。本参考介绍开发和生产环境中的常见错误及其解决方法，帮助排查问题并构建稳健的分布式应用。

## 无法接收查询结果 {#couldnt-receive-query-results}

协调节点无法连接工作节点时，会出现此错误。

```sql
SELECT 1 FROM companies WHERE id = 2928;
```

```text
ERROR: connection to the remote node localhost:5432 failed with the following error: could not connect to server: Connection refused
Is the server running on host "localhost" (127.0.0.1) and accepting
TCP/IP connections on port 5432?
```

### 解决方法 {#resolution}

检查工作节点是否接受连接，以及 Azure DNS 是否正确解析。

## 因参与分布式死锁而取消事务 {#canceling-the-transaction-since-it-was-involved-in-a-distributed-deadlock}

死锁不仅会发生在单节点数据库，也会发生在分布式数据库。跨多个节点执行的查询可能形成死锁。Citus 能识别分布式死锁，并通过中止其中一个查询来解除死锁。

将行分布到多个工作节点，再并发执行两个更新冲突的事务，即可观察这一行为：

```sql
CREATE TABLE lockme (id int, x int);
SELECT create_distributed_table('lockme', 'id');

-- id=1 goes to one worker, and id=2 another
INSERT INTO lockme VALUES (1,1), (2,2);

--------------- TX 1 ----------------  --------------- TX 2 ----------------
BEGIN;
                                       BEGIN;
UPDATE lockme SET x = 3 WHERE id = 1;
                                       UPDATE lockme SET x = 4 WHERE id = 2;
UPDATE lockme SET x = 3 WHERE id = 2;
                                       UPDATE lockme SET x = 4 WHERE id = 1;
```

```text
ERROR: canceling the transaction since it was involved in a distributed deadlock
```

### 解决方法 {#resolution-1}

检测并解除死锁是分布式事务正常处理过程的一部分。应用可以重试查询或采取其他措施。

## 无法连接服务器：无法分配所请求的地址 {#couldnt-connect-to-server-cant-assign-requested-address}

```sql
WARNING: connection error: localhost:9703
DETAIL: could not connect to server: Cannot assign requested address
```

当协调节点没有更多可用套接字来响应工作节点请求时，会出现此错误。

### 解决方法 {#resolution-2}

配置操作系统以复用 TCP 套接字。在协调节点的 shell 中执行：

```bash
sysctl -w net.ipv4.tcp_tw_reuse=1
```

该设置允许在协议安全的情况下，将 TIME_WAIT 状态的套接字复用于新连接。默认值为 0，即禁用。

## SSL 错误：证书验证失败 {#ssl-error-certificate-verify-failed}

从 Citus 8.1 开始，节点间通信默认要求使用 SSL。首次安装 Citus 时，如果 PostgreSQL 服务器尚未启用 SSL，安装过程会启用它，包括创建并自签名一个 SSL 证书。

不过，如果根证书颁发机构文件存在（通常为 `~/.postgresql/root.crt`），连接时就会使用该 CA 验证证书，而验证会失败。PostgreSQL 的 [SSL 支持](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBQ-SSL-CERTIFICATES)文档提醒：

> 为兼容早期 PostgreSQL 版本，如果存在根 CA 文件，sslmode=require 的行为就与 verify-ca 相同，即根据 CA 验证服务器证书。不建议依赖这种行为；需要验证证书的应用应始终使用 verify-ca 或 verify-full。

### 解决方法 {#resolution-3}

可选方案包括为证书签名、关闭 SSL 或删除根证书。此外，未借助 `local_hostname` 设置时，节点也可能无法连接自身。

## 无法连接任何活动分片放置 {#couldnt-connect-to-any-active-placements}

工作节点的所有可用连接槽位被占满后，新的连接会失败。

```sql
WARNING: connection error: hostname:5432
ERROR: could not connect to any active placements
```

### 解决方法 {#resolution-4}

此错误最常见于向 Citus 并行复制数据。COPY 命令会为每个分片打开一个连接。向包含 N 个分片的目标并发运行 M 次复制，会产生 M*N 个连接。可以减少目标分布式表的分片数，或减少并行运行的 `\copy` 命令数量。

## 剩余连接槽位仅供非复制超级用户连接使用 {#remaining-connection-slots-are-reserved-for-nonreplication-superuser-connections}

PostgreSQL 耗尽可用于并发客户端请求的连接时，会出现此错误。

### 解决方法 {#resolution-5}

[max_connections](https://www.postgresql.org/docs/current/static/runtime-config-connection.html#GUC-MAX-CONNECTIONS) GUC 控制连接上限，通常默认为 100。每个连接都会消耗资源，因此需要合理调整。提高 `max_connections` 时，也应提高[内存限制](https://www.postgresql.org/docs/current/static/runtime-config-resource.html#RUNTIME-CONFIG-RESOURCE-MEMORY)。

[PgBouncer](https://pgbouncer.github.io/) 可以让超出连接上限的请求排队，也有助于缓解此问题。（`cloud_topic` 内置了 PgBouncer 实例。）

## PgBouncer 无法连接服务器 {#pgbouncer-cant-connect-to-server}

在自托管的 Citus 集群中，此错误表示协调节点没有响应 PgBouncer。

### 解决方法 {#resolution-6}

尝试使用 psql 直接连接服务器，确认服务器正在运行并接受连接。

## 关系 *foo* 不是分布式表 {#relation-foo-isnt-distributed}

当前版本的 Citus 不再出现此错误。过去，在同一个查询中连接本地表和分布式表会触发它。

### 解决方法 {#resolution-7}

升级到 Citus 10.0 或更高版本。

## 不支持的子句类型 {#unsupported-clause-type}

当前版本的 Citus 不再出现此错误。过去，使用不等式条件执行连接时会触发它：

```sql
SELECT *
 FROM identified_event ie
 JOIN field_calculator_watermark w ON ie.org_id = w.org_id
WHERE w.org_id = 42
  AND ie.version > w.version
LIMIT 10;
```

```text
ERROR: unsupported clause type
```

### 解决方法 {#resolution-8}

升级到 Citus 7.2 或更高版本。

## 事务中执行首个修改命令后无法打开新连接 {#cant-open-new-connections-after-the-first-modification-command-within-a-transaction}

除少数特殊的分片修复场景外，当前版本的 Citus 不再出现此错误。过去，在事务中更新行后再执行需要新建协调节点到工作节点连接的命令，会触发它。

```sql
BEGIN;
-- run modification command that uses one connection
DELETE FROM http_request
 WHERE site_id = 8
   AND ingest_time < now() - '1 week'::interval;

-- now run a query that opens connections to more workers
SELECT count(*) FROM http_request;
```

```sql
ERROR: cannot open new connections after the first modification command within a transaction
```

### 解决方法 {#resolution-9}

升级到 Citus 7.2 或更高版本。

## 无法创建唯一性约束 {#cant-create-uniqueness-constraint}

作为分布式系统，Citus 只有在唯一索引或主键约束包含表的分布列时，才能保证唯一性。分片划分保证各分片包含互不重叠的分区列值，因此每个工作节点的索引可以在本地强制执行其负责的那部分约束。

尝试在非分布列上创建唯一索引会报错：

```sql
ERROR: creating unique indexes on non-partition columns is currently unsupported
```

如果要对非分布列强制保证唯一性，Citus 就必须在每次 INSERT 时检查所有分片，这违背了可扩展性的目标。

### 解决方法 {#resolution-10}

对非分布列实现唯一性约束有两种方式：

- 创建包含目标列（*C*）和分布列（*D*）的复合唯一索引或主键。这个条件弱于仅对 *C* 保证唯一，但可以保证每个 *D* 值对应的 *C* 值互不重复。例如，多租户系统按 `company_id` 分布时，这种方式可以保证 *C* 在每家公司内部唯一。
- 使用参考表而非哈希分布表。参考表会在所有节点上保存完整副本，因此这种方式仅适用于小表。

## 函数 create_distributed_table 不存在 {#function-create_distributed_table-doesnt-exist}

```sql
SELECT create_distributed_table('foo', 'id');
/*
ERROR:  function create_distributed_table(unknown, unknown) does not exist
LINE 1: SELECT create_distributed_table('foo', 'id');
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
*/
```

### 解决方法 {#resolution-11}

如果基本的 `user_defined_functions` 不可用，请检查 Citus 扩展是否正确安装。在 psql 中运行 `\dx` 可以列出已安装的扩展。

一种可能的原因是在 PostgreSQL 服务器上新建了数据库：新数据库需要重新安装扩展。正确操作方式参见 `create_db`。

## UPDATE 查询中的 STABLE 函数不能以列引用作为参数调用 {#stable-functions-used-in-update-queries-cant-be-called-with-column-references}

每个 PostgreSQL 函数都有[易变性](https://www.postgresql.org/docs/current/static/xfunc-volatility.html)标记，说明函数能否更新数据库，以及相同输入下返回值是否可能随时间变化。`STABLE` 函数保证在一条语句内，对所有行给定相同参数时返回相同结果；`IMMUTABLE` 函数则保证相同参数永远返回相同结果。

非不可变函数可能给分布式系统带来麻烦，因为它们在不同分片上执行的时间略有差异，就可能产生细微的结果变化。节点间数据库配置的差异，也可能与这些函数相互作用而造成问题。

最常见的触发方式之一是使用 PostgreSQL 的 `timestamp` 类型，它与 `timestamptz` 不同，不记录时区。解释 timestamp 列时需要参考数据库时区，而时区可能在查询之间改变，因此操作 timestamp 的函数并非不可变。

Citus 不允许在分布式查询中，对列应用稳定函数来过滤结果。例如：

```sql
-- foo_timestamp is timestamp, not timestamptz
UPDATE foo SET ... WHERE foo_timestamp < now();
```

```sql
ERROR: STABLE functions used in UPDATE queries cannot be called with column references
```

本例中，timestamp 与 timestamp 之间的比较运算符 `<` 不是不可变的。

### 解决方法 {#resolution-12}

在分布式 UPDATE 语句中，避免对列使用稳定函数。尤其在处理时间时，应使用 `timestamptz` 而非 `timestamp`。时间戳包含时区后，计算就具有不可变性。

## 相关内容 {#related-content}

- [诊断查询](/citus/operations/diagnostic-queries/)
- [常见问题](/citus/overview/faq-citus/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
