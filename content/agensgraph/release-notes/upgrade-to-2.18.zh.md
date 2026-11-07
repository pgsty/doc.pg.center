---
title: 升级到 2.18
linkTitle: 升级到 2.18
description: 检查应用兼容性后，用 pg_upgrade 或转储重载把 AgensGraph 2.17 升级到 2.18。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/upgrade-to-2.18.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


<!-- check-examples: skip because the examples act on two clusters and on a graph
     the reader names. The walkthrough page carries a transcript of a real run. -->

# 升级到 2.18

AgensGraph 2.18 基于 PostgreSQL 18，因此迁移到它是主版本升级：数据目录格式变了，2.17 数据目录不能由 2.18 二进制启动。你有两条路线——复用现有数据文件且速度较快的 `pg_upgrade`，或者转储后重载。

选择任一条之前，先阅读[变化说明](/zh/agensgraph/release-notes/2.18/#migrating-to-218)并检查应用。若干变化会破坏在 2.17 上可用的查询，而升级工具一个也发现不了。

## 先检查应用 {#check-your-application-first}

对照你的代码库逐项检查。每一项都是把在 2.17 上工作的代码变成 2.18 上错误或不同结果的变化。

* **名为 `xor`、`current_graph` 或 `current_property_graph` 的标识符**——现在是保留字。改名，或用**双引号**引用（`MATCH (n:"xor")`）；反引号在这里不是引用字符。`let` 和 `finish` 作为变量名、`let` 作为标签也会被拒绝；`CREATE VLABEL insert;` 需要引用，尽管模式写法 `MATCH (n:insert)` 仍可用。完整位置矩阵见[关键字](/zh/agensgraph/appendix/keywords/)。
* **`call(...)` 或 `(call { ... })`**——字面名为 `call` 的函数，或变量为 `call`、带属性映射且无标签的点模式。两者含义都变了；请引用名称。
* **不是布尔值的条件**——`WHERE n.count`、`FILTER n.name`。它们过去按非零或非空选择，现在抛出转换错误。加 `::boolean` 或显式比较。
* **对顶点、边或路径执行 `collect()`**——现在返回原生数组，而不是 jsonb 快照数组。解析旧 jsonb 形式的客户端代码必须修改；读取收集元素属性的代码开始正常工作。
* **对顶点或边执行 `min()` / `max()`**——现在有歧义，因此是错误。使用 `min(v::jsonb)` 或 `min(id(v))`。
* **`range()`、`toStringList`、`toIntegerList`、`toFloatList`**——返回类型变化。
* **带 `SKIP` 或 `LIMIT` 的 `WITH … WHERE`**——现在在过滤后分页，结果集会变化。
* **图上的行级安全**——RLS 现在真正作用于图写入。如果标签上有策略，请重新测试：过去能漏过的写入会被拒绝。
* **对标签执行 `ALTER TABLE`**——任何结构性修改都被拒绝。使用标签 DDL，或设置 `enable_graph_ddl`。
* **`EXPLAIN` 回归基线**——元素上的 `count()`、属性读取和可变长度遍历节点的计划文本已变化。
* **两侧排序规则不同的外键**——任一侧为非确定性排序规则时被拒绝（`42P21`）。2.17 可以创建它。两侧使用*同一个*非确定性排序规则仍然可以；两个不同的确定性排序规则也可以。`NOT VALID` 不会推迟检查；标签列上的外键同样被拒绝。这不只是应用变化：2.17 转储恢复的表会**没有该约束**。升级前找出这些列对——见[带非确定性排序规则的外键](#foreign-keys-with-a-nondeterministic-collation)。

## 带非确定性排序规则的外键 {#foreign-keys-with-a-nondeterministic-collation}

在转储或升级前，在 **2.17** 集群的每个数据库中运行：

```sql
SELECT c.conrelid::regclass AS referencing, c.conname, fa.attname AS col,
       fc.collname AS referencing_collation, pc.collname AS referenced_collation
  FROM pg_constraint c
  CROSS JOIN LATERAL unnest(c.conkey, c.confkey) AS k(fkatt, pkatt)
  JOIN pg_attribute fa ON fa.attrelid = c.conrelid AND fa.attnum = k.fkatt
  JOIN pg_attribute pa ON pa.attrelid = c.confrelid AND pa.attnum = k.pkatt
  JOIN pg_collation fc ON fc.oid = fa.attcollation
  JOIN pg_collation pc ON pc.oid = pa.attcollation
 WHERE c.contype = 'f'
   AND fa.attcollation <> pa.attcollation
   AND NOT (fc.collisdeterministic AND pc.collisdeterministic);
```

每一行都是 2.18 会拒绝的约束。在 2.17 上让两列使用相同排序规则，再转储。这个条件与服务端应用的相同，也读取同一个目录列，因此选出的约束不多也不少。

> [!WARNING]
> 两条路线都不会警告你。`pg_upgrade --check` 以 `*Clusters are compatible*` 结束，随后升级重建约束时失败。转储重载更糟：恢复报告成功，表到达时**没有外键**，之后引用空对象的行会被接受。

## 路线 1：使用 pg_upgrade {#route-1-using-pg_upgrade}

`pg_upgrade` 创建新集群目录并复用既有用户数据文件，因此不重写数据。图存储为普通模式和表，所以图数据与关系数据的迁移方式完全相同。

### 开始之前 {#before-you-begin}

* **把 2.18 安装到独立位置。** 不要覆盖 2.17 安装：`pg_upgrade` 需要两套二进制，保留 2.17 也是回滚的前提。
* **磁盘空间。** 默认复制数据文件，需要第二份空间。`--link` 改用硬链接——几乎即时，额外空间很小——但两个数据目录必须在同一文件系统，而且新服务端一旦启动，回滚不再可能。
* **在 2.18 安装中安装 2.17 集群使用的相同外部模块**，例如 `pgvector`。AgensGraph 自身图特性内置于服务端，没有图扩展需要重建。
* **带普通列的标签会阻止升级。** `pg_upgrade` 调用 `pg_dump --binary-upgrade`；后者拒绝带有 `id`、`start`、`end` 和 `properties` 之外列的图标签，而不是静默破坏物理列布局。开始前找出它们：

  ```sql
  SELECT c.relname, a.attname
  FROM pg_catalog.ag_label l
    JOIN pg_class c ON c.oid = l.relid
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
  WHERE a.attname NOT IN ('id', 'start', 'end', 'properties');
  ```

  升级前删除这些列，或把数据移到别处。
* 所有命令都以拥有数据目录的操作系统用户运行。

以下命令使用这些变量：

```shell
export OLD=/usr/local/agensgraph-2.17
export NEW=/usr/local/agensgraph-2.18
export OLDDATA=$OLD/data
export NEWDATA=$NEW/data
```

### 第 1 步：停止旧服务端 {#step-1-stop-the-old-server}

`pg_upgrade` 运行时两个集群都必须停止。

```shell
$OLD/bin/ag_ctl -D $OLDDATA stop
```

### 第 2 步：初始化新集群 {#step-2-initialize-the-new-cluster}

使用与旧集群相同的超级用户、编码和区域设置，并匹配数据校验和设置。

```shell
$NEW/bin/initdb -D $NEWDATA -U postgres --encoding=UTF8 --no-data-checksums
```

> [!WARNING]
> **对多数升级，`--no-data-checksums` 不是可选项。** PostgreSQL 18 默认启用数据页校验和，PostgreSQL 17 默认关闭。除非你的 2.17 集群初始化时带了 `-k`，两个集群会不一致，`pg_upgrade` 在做任何事之前停止：
>
>     Performing Consistency Checks
>     -----------------------------
>     Checking cluster versions                                     ok
>
>     old cluster does not use data checksums but the new one does
>     Failure, exiting
>
> 初始化前检查你的情况：
>
>     $OLD/bin/pg_controldata -D $OLDDATA | grep checksum
>
> 如果输出 `Data page checksum version: 0`，传入 `--no-data-checksums`。如果输出 `1`，不要传该标志。开启校验和是独立操作——见 [`pg_checksums`](https://www.postgresql.org/docs/18/app-pgchecksums.html)——值得做，但应在升级之后，而不是作为升级的一部分。

### 第 3 步：检查兼容性 {#step-3-check-compatibility}

`--check` 验证两个集群且不修改任何内容。

```shell
$NEW/bin/pg_upgrade \
  -b $OLD/bin -B $NEW/bin \
  -d $OLDDATA -D $NEWDATA \
  -U postgres --check
```

成功检查以 `*Clusters are compatible*` 结束。

> [!WARNING]
> 绿色检查不代表升级会成功。它不查找[带非确定性排序规则的外键](#foreign-keys-with-a-nondeterministic-collation)，而第 4 步会在重建约束时失败。请自己运行那条查询。

用 `-U` 传入数据库超级用户。默认 `pg_upgrade` 以操作系统用户连接，而它通常不是数据库角色。

### 第 4 步：执行升级 {#step-4-run-the-upgrade}

同一命令去掉 `--check`：

```shell
$NEW/bin/pg_upgrade \
  -b $OLD/bin -B $NEW/bin \
  -d $OLDDATA -D $NEWDATA \
  -U postgres
```

它以 `Upgrade Complete` 结束。给检查和升级都加 `--link`，可以用硬链接替代复制。

### 第 5 步：启动新服务端 {#step-5-start-the-new-server}

```shell
$NEW/bin/ag_ctl -D $NEWDATA -l $NEW/logfile start
```

确认已在新服务端上，并且图已经迁移：

```sql
SELECT version();
```

```cypher
SET graph_path = <your graph>;
MATCH (n) RETURN count(n);
```

### 第 6 步：升级后任务 {#step-6-post-upgrade-tasks}

其中三项是 AgensGraph 特有的，且没有一项可选。

**重建统计信息。** `pg_upgrade` 不迁移优化器统计信息；重建之前计划会很差：

```shell
$NEW/bin/vacuumdb -U postgres --all --analyze-in-stages
```

**重新收集图元数据。** `ag_graphmeta` 驱动规划器扫描裁剪。二进制升级会把它留空并把图标记无效；每个图重建一次之前，裁剪不会启用：

```sql
SET graph_path = <your graph>;
SELECT regather_graphmeta();
```

检查是否生效：

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

**重新调整边标签统计目标。** 2.18 把新边标签 `start` 和 `end` 列的统计目标从 10000 降到 1000。2.17 创建的标签保留旧值，并在每次边连接上付出很高的规划代价——大标签上可达数百毫秒。对每个边标签执行：

```sql
ALTER TABLE <graph>.<elabel> ALTER COLUMN start SET STATISTICS 1000;
ALTER TABLE <graph>.<elabel> ALTER COLUMN "end" SET STATISTICS 1000;
ANALYZE <graph>.<elabel>;
```

确认升级集群正常后，用 `pg_upgrade` 在运行目录中生成的脚本删除旧数据文件：

```shell
./delete_old_cluster.sh
```

### 回滚 {#rolling-back}

在复制模式下，且运行 `delete_old_cluster.sh` 之前，2.17 数据目录未被动过。停止新服务端并启动旧服务端：

```shell
$NEW/bin/ag_ctl -D $NEWDATA stop
$OLD/bin/ag_ctl -D $OLDDATA -l $OLD/logfile start
```

使用 `--link` 升级后，新服务端一旦启动回滚就不可能，因为两个集群共享数据文件。请从备份恢复。

## 路线 2：转储并重载 {#route-2-dump-and-reload}

更慢，但它重写所有内容，运行时不需要第二份二进制。

```shell
$OLD/bin/pg_dumpall -U postgres -f cluster.sql
# start the 2.18 cluster, then:
$NEW/bin/psql -U postgres -d postgres -f cluster.sql
```

> [!WARNING]
> `psql` 不会在错误处停止，即使语句失败也以 0 退出。新服务端拒绝的任何内容——例如[带非确定性排序规则的外键](#foreign-keys-with-a-nondeterministic-collation)——只是输出中的一行，恢复会继续并遗漏它。相信恢复前先读日志。

要让恢复改为停止，请把角色与数据分开导出。角色不能在 `ON_ERROR_STOP` 下恢复：`pg_dumpall` 会为已存在于新集群的 bootstrap 超级用户写 `CREATE ROLE`，而 `--clean --if-exists` 只是把失败移到当前连接角色的 `DROP ROLE`。

```shell
$OLD/bin/pg_dumpall -U postgres --globals-only -f globals.sql
$OLD/bin/pg_dump    -U postgres -Fc -d mydb -f mydb.dump       # once per database
# start the 2.18 cluster, then:
$NEW/bin/psql -U postgres -d postgres -f globals.sql           # roles; errors here are benign
$NEW/bin/createdb -U postgres mydb
$NEW/bin/pg_restore -U postgres --exit-on-error -d mydb mydb.dump
```

两点须知：

* **恢复可能需要 `enable_graph_ddl`。** 带普通列的标签转储会在 `ALTER TABLE … ADD COLUMN` 语句周围输出 `SET enable_graph_ddl = on`。该设置任意角色可写，因此普通用户可以恢复——除非该角色被 `ALTER ROLE … SET` 强制关闭。
* **上文的图元数据与统计信息任务仍然适用。**

## 不支持降级 {#downgrading-is-not-supported}

如果任何图使用[提升列](/zh/agensgraph/querying/typed-columns/)，2.18 转储不能恢复到 2.17。转储中的 `CREATE VLABEL` 写法会被 2.17 解析器拒绝；在纯文本流中，这条语句之后的内容全部丢失。如果需要退路，请保留升级前取得的 2.17 备份。

还要注意 `pg_dump` 和 `pg_restore` 不检查 AgensGraph 版本。只有 PostgreSQL 的 `server_version` 范围检查适用。因此版本不匹配会在恢复中途表现为解析失败，而不是一开始被拒绝。

## 实例 {#a-worked-example}

[升级演练](/zh/agensgraph/release-notes/upgrade-walkthrough/)在小型集群上执行完整流程，包含真实命令和输出。
