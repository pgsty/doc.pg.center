---
title: 安全
linkTitle: 安全
description: AgensGraph 的安全模型就是 PostgreSQL 的安全模型。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/security.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


AgensGraph 的安全模型就是 PostgreSQL 的安全模型。角色、`pg_hba.conf`、TLS、`GRANT` 和行级安全的工作方式完全相同；[PostgreSQL 客户端认证](https://www.postgresql.org/docs/18/client-authentication.html)与[数据库角色](https://www.postgresql.org/docs/18/user-manag.html)章节是参考手册。

本页补充的是这些机制如何落到图上。图是模式，标签是表，因此 Cypher 查询需要的授权并不总是你直觉猜到的那组。

## 认证 {#authentication}

数据目录中的 `pg_hba.conf` 决定谁可以从哪里连接哪个数据库，以及如何连接。规则自上而下匹配，第一条匹配的规则获胜。

```
# TYPE  DATABASE  USER      ADDRESS          METHOD
local   all       all                        peer
host    mydb      appuser   10.0.0.0/24      scram-sha-256
hostssl mydb      analyst   0.0.0.0/0        scram-sha-256
host    all       all       0.0.0.0/0        reject
```

编辑后重新加载：

```shell
ag_ctl -D $AGDATA reload
```

服务端可被访问前，三件事必须做对：

**替换默认 `trust` 规则。** `initdb` 为本地连接写入 `trust`，意味着任何拥有 shell 账户的人都可以以任意角色连接，包括超级用户。本地 Unix socket 连接使用 `peer`，网络连接使用 `scram-sha-256`。

**使用 `scram-sha-256`，不使用 `md5`。** 在创建或修改密码前设置 `password_encryption = scram-sha-256`，确保存储的验证器是强版本。

**网络连接要求 TLS。** 规则使用 `hostssl`，并在 `postgresql.conf` 中设置 `ssl = on` 并提供证书和密钥。客户端的 `sslmode=verify-full` 才能真正防止劫持；`require` 只加密。

可用方法是 PostgreSQL 的完整集合——`peer`、`scram-sha-256`、`cert`、`ldap`、`gss`、`sspi`、`pam`、`radius`、`ident`、`trust`、`reject`——选项也相同。参见 [PostgreSQL 认证方法章节](https://www.postgresql.org/docs/18/auth-methods.html)。

连接被拒绝时，服务端日志会说明原因，而且比客户端看到的错误更具体。修改规则前先查看日志。

## 角色 {#roles}

角色是集群级的——属于服务端，不属于某个数据库——带 `LOGIN` 的角色就是其他系统所说的用户。

```sql
CREATE ROLE appuser LOGIN PASSWORD 'secret';
CREATE ROLE readonly;                       -- a group, no LOGIN
GRANT readonly TO appuser;
```

运维上重要的属性是 `SUPERUSER`、`CREATEDB`、`CREATEROLE`、`REPLICATION` 和 `BYPASSRLS`；这些都不应授予应用角色。`ALTER ROLE … SET` 可以为角色固定设置，这是强制 `graph_path` 或让除维护角色外所有人都保持 `enable_graph_dml` 关闭的干净方式：

```sql
ALTER ROLE appuser SET graph_path = moviekb;
ALTER ROLE appuser SET enable_graph_dml = off;
```

## 图上的权限 {#permissions-on-a-graph}

图是模式，每个标签是表，所以授权都是普通授权。意外来自别处：Cypher 查询接触的对象多于它点名的标签。

### 读取 {#reading}

读取需要图模式上的 `USAGE`，以及它接触的每个标签上的 `SELECT`。按下面的顺序可以看清每条授权何时变得必要。先只给模式：

```sql
CREATE ROLE analyst;
GRANT USAGE ON SCHEMA moviekb TO analyst;
```

```psql
SET ROLE analyst;
```

现在 Cypher 读取会以表权限错误失败，并点名标签：

```cypher
MATCH (m:movie) RETURN count(m);
```

```
ERROR:  permission denied for table movie
```

授予标签后即可工作：

```psql
RESET ROLE;
GRANT SELECT ON moviekb.movie TO analyst;
SET ROLE analyst;
```

```cypher
MATCH (m:movie) RETURN count(m);
```

```
 count
-------
 18
```

**无标签模式还需要 `ag_vertex`。** `MATCH (n)` 扫描图的 `ag_vertex` 父表及其下的每个标签，因此能读 `movie` 却不能读 `ag_vertex` 的角色仍然不能执行它：

```cypher
MATCH (n) RETURN count(n);
```

```
ERROR:  permission denied for table ag_vertex
```

无标签边同理需要 `ag_edge`。因此对只读分析角色，应跨模式授权，而不是逐标签授权：

```psql
RESET ROLE;
```

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA moviekb TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb GRANT SELECT ON TABLES TO analyst;
```

正是 `ALTER DEFAULT PRIVILEGES` 让下个月创建的标签也可读。

### 写入 {#writing}

创建顶点或边需要标签上的 `INSERT`，**还需要标签 id 序列上的 `USAGE`**。第二项很容易漏。只授予 `INSERT`：

```psql
RESET ROLE;
```

```sql
GRANT INSERT ON moviekb.movie TO analyst;
```

```psql
SET ROLE analyst;
```

```cypher
CREATE (:movie {title: 'X'});
```

```
ERROR:  permission denied for sequence movie_id_seq
```

加上序列后写入成功：

```psql
RESET ROLE;
```

```sql
GRANT USAGE ON SEQUENCE moviekb.movie_id_seq TO analyst;
```

`SET` 和 `REMOVE` 需要标签上的 `UPDATE`。`DELETE` 需要标签上的 `DELETE`。`DETACH DELETE` 还需要 `ag_edge` 上的授权，因为它通过该父表找到要删除的边：

```
ERROR:  permission denied for table ag_edge
```

点名 `ag_edge` 或 `ag_vertex` 的错误是缺少图父标签授权，不是行级安全的结果——值得知道，因为很容易误读。

读写整个图的角色可以使用这组授权：

```sql
GRANT USAGE ON SCHEMA moviekb TO appuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA moviekb TO appuser;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA moviekb TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb GRANT USAGE ON SEQUENCES TO appuser;
```

### 创建标签 {#creating-labels}

创建标签需要图模式上的 `CREATE`。创建图需要数据库上的 `CREATE`。

## 行级安全 {#row-level-security}

行级安全作用于标签，因此策略可以限制角色能看到和写入哪些顶点或边：

```sql
ALTER TABLE moviekb.movie ENABLE ROW LEVEL SECURITY;

CREATE POLICY movie_visible ON moviekb.movie
  FOR SELECT TO analyst
  USING ((properties->>'genre') = 'Sci-Fi');
```

> [!WARNING]
> **重新测试你在 2.17 上有过的任何 RLS 策略。** 2.18 之前，策略没有正确作用于图写入：`UPDATE` 或 `DELETE` 策略的 `USING` 子句被挂在一个永远不会被扫描的关系上，因此什么都没有过滤——完全没有 `DELETE` 策略的角色也能删除行。`INSERT` 策略检查的是错误的行，边创建则完全没有检查，所以启用行安全的边标签接受每次插入。
>
> 2.18 会完整执行这些策略。这是正确行为，也意味着应用今天执行的写入之后可能被拒绝。请在升级前测试，而不是之后。参见[版本说明](/zh/agensgraph/release-notes/2.18/#stricter-validation)。

两条实践说明：

* 策略表达式读取标签列，因此可以作用于 `properties`，也可以作用于更快的[提升列](/zh/agensgraph/querying/typed-columns/)，让策略使用索引。
* `BYPASSRLS` 和表所有权都会跳过策略。应用角色二者都不应有。

## 属于安全姿态的两个设置 {#two-settings-that-are-part-of-the-security-posture}

`enable_graph_dml` 和 `enable_graph_ddl` 默认关闭，分别控制用 SQL 而不是 Cypher 写入和重塑标签。保持关闭可以让应用留在 Cypher 路径上，让图自身的检查运行——例如检查边端点存在。

它们并不构成图完整性的全部，也不应这样理解。`COPY` 写标签时不参考任何一个设置。无论设置是什么，在每条路径上都成立的是：一行的 id 指向存储它的标签；会破坏这一点的写入会被拒绝，无论它来自 Cypher、`INSERT`、`UPDATE`、`COPY` 还是复制应用。

维护工作期间打开它们，完成后关闭；也可以用 `ALTER ROLE … SET` 按角色固定为关闭。

`cypher_allow_unsafe_ddl` 同理。参见[服务器设置](/zh/agensgraph/reference/guc/)。

## 静态加密 {#encryption-at-rest}

AgensGraph 本身不加密数据文件。请使用文件系统或块设备加密；如果有透明数据加密要求，使用 [Agens TDE](https://tech.skaiworldwide.com/docs/en/agens-tde/16/)。`pgcrypto` 覆盖列级加密，而属性是普通 `jsonb` 值，可以像其他列一样保存 `pgcrypto` 密文。
