---
title: agens 客户端
linkTitle: agens 客户端
description: agens 是交互式终端客户端。
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/agens.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


`agens` 是交互式终端客户端。它就是 PostgreSQL 的 `psql`，只是换用 AgensGraph 名称，并新增了五个描述图的元命令。

因为它就是 `psql`，[PostgreSQL 的 `psql` 参考](https://www.postgresql.org/docs/18/app-psql.html)记录了每个选项、变量和其他所有元命令。这里不重复这些内容。本页只讲两件事：只在这里出现的图元命令，以及属于 AgensGraph 的两个环境细节。

## 同一程序的两个名称 {#the-same-program-under-two-names}

构建过程用同一份源码生成两个二进制文件并都安装。唯一区别是品牌：各自打印的名称，以及帮助中的 bug 报告和主页行。

```shell
agens --version
psql --version
```

```
agens (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
psql (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

比较两份帮助文本可以看到全部差异：

```shell
diff <(agens --help) <(psql --help)
```

```
1c1
< agens is the AgensGraph interactive terminal.
---
> psql is the PostgreSQL interactive terminal.
4c4
<   agens [OPTION]... [DBNAME [USERNAME]]
---
>   psql [OPTION]... [DBNAME [USERNAME]]
62,63c62,63
< Report bugs to <inquiry@skaiworldwide.com>.
< AgensGraph home page: <https://skaiworldwide.com/>
---
> Report bugs to <pgsql-bugs@lists.postgresql.org>.
> PostgreSQL home page: <https://www.postgresql.org/>
```

由此带来两个结果，而且都能省事。

**你了解的 `psql` 知识全部适用。**相同的选项、同一个 `~/.psqlrc`、同一组 `PG*` 环境变量，以及相同的 `\copy`、`\watch`、`\gexec`、`\timing`、`\x`、`\pset`、Tab 补全和变量插值。

```shell
agens -d docs -c "SHOW agversion;"
```

```
 agversion
------------
 2.18.6.1
```

**图元命令在两个二进制文件中都有。**二者由同一组对象构建，所以这个安装中的 `psql` 会像 `agens` 一样列出图。如果你的路径上已有 `psql`，不需要为了描述图而切换客户端。

服务端工具遵循同一模式，只有一对改名：

| AgensGraph 名称 | PostgreSQL 名称 | 差异 |
| --- | --- | --- |
| `agens` | `psql` | 仅品牌。二者都安装。 |
| `ag_ctl` | `pg_ctl` | 仅品牌。二者都安装。 |

其他每个工具都保留 PostgreSQL 名称，且只有这个名称。它们是 `initdb`、`postgres`、`pg_dump`、`pg_dumpall`、`pg_restore`、`pg_basebackup`、`pg_upgrade`、`pg_controldata`、`pg_checksums`、`pg_rewind`、`pg_waldump`、`createdb`、`dropdb`、`createuser`、`dropuser`、`vacuumdb`、`reindexdb`、`clusterdb`、`pgbench`、`ecpg` 及其余工具。没有 `ag_dump`，也没有 `ag_basebackup`。[服务端工具](/zh/agensgraph/operations/tools/)介绍它们对图做什么。

## 图元命令 {#graph-meta-commands}

五个元命令描述图。`+` 为每个命令增加列，模式可以缩小列出的范围。

| 命令 | 列出 |
| --- | --- |
| `\dG[+] [PATTERN]` | 图。 |
| `\dGl[+] [PATTERN]` | 标签，两类都包括。 |
| `\dGv[+] [PATTERN]` | 顶点标签，随后逐个描述。 |
| `\dGe[+] [PATTERN]` | 边标签，随后逐个描述。 |
| `\dGi[+] [PATTERN]` | 属性索引。 |

大小写有意义。`\dG` 列出图；`\dg` 是 PostgreSQL 自身命令，列出角色。

这五个是完整集合，且都不出现在 `\?` 中。其他 `\d` 命令可用的 `x` 和 `S` 修饰符不能直接跟在 `\dG` 后：

```psql
\dGx moviekb
```

```
invalid command \dGx
```

`x` 在四个子命令上可用，所以 `\dGvx` 会以扩展模式打印列表。

下面的示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 列出数据库中的图 {#list-the-graphs-in-a-database}

```psql
\dG moviekb
```

```
 List of graphs
  Name   | Owner
---------+-------
 moviekb | agens
```

`+` 增加图的访问权限和注释。图是模式，所以这些权限是模式权限。授予之前它们为空，因此先授予一个权限以看到列被填充：

```sql
GRANT USAGE ON SCHEMA moviekb TO PUBLIC;
```

```psql
\dG+ moviekb
```

```
                  List of graphs
  Name   | Owner | Access privileges | Description
---------+-------+-------------------+-------------
 moviekb | agens | agens=UC/agens   +|
         |       | =U/agens          |
```

随后撤销它，让示例数据集回到原状：

```sql
REVOKE USAGE ON SCHEMA moviekb FROM PUBLIC;
```

不带模式时，`\dG` 列出数据库中的每个图。

### 列出图的标签 {#list-a-graphs-labels}

`\dGl` 把两类标签列在一起，按图、种类、名称排序：

```psql
\dGl moviekb.*
```

```
            List of labels
  Graph  |    Name    |  Type  | Owner
---------+------------+--------+-------
 moviekb | acted_in   | edge   | agens
 moviekb | ag_edge    | edge   | agens
 moviekb | directed   | edge   | agens
 moviekb | related_to | edge   | agens
 moviekb | ag_vertex  | vertex | agens
 moviekb | movie      | vertex | agens
 moviekb | person     | vertex | agens
```

`ag_vertex` 和 `ag_edge` 在列表中，因为每个图都有它们。见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

`+` 增加标签的磁盘大小和注释。大小来自标签表的 `pg_table_size`，因此反映你实际加载的数据：

```psql
\dGl+ moviekb.*
```

```
                                     List of labels
  Graph  |    Name    |  Type  | Owner |    Size    |            Description
---------+------------+--------+-------+------------+------------------------------------
 moviekb | acted_in   | edge   | agens | 16 kB      |
 moviekb | ag_edge    | edge   | agens | 8192 bytes | base edge label of graph moviekb
 moviekb | directed   | edge   | agens | 16 kB      |
 moviekb | related_to | edge   | agens | 16 kB      |
 moviekb | ag_vertex  | vertex | agens | 8192 bytes | base vertex label of graph moviekb
 moviekb | movie      | vertex | agens | 16 kB      |
 moviekb | person     | vertex | agens | 16 kB      |
```

### 描述顶点标签 {#describe-the-vertex-labels}

`\dGv` 把列表缩小到顶点标签，然后像 `\d` 打印表脚注一样，为每个标签打印一个块。块中包含标签的属性索引、约束、它继承的标签以及继承它的标签：

```psql
\dGv moviekb.*
```

```
            List of labels
  Graph  |   Name    |  Type  | Owner
---------+-----------+--------+-------
 moviekb | ag_vertex | vertex | agens
 moviekb | movie     | vertex | agens
 moviekb | person    | vertex | agens

Vertex label "moviekb.ag_vertex"
--
Child labels: moviekb.movie,
              moviekb.person

Vertex label "moviekb.movie"
--
Inherits: moviekb.ag_vertex

Vertex label "moviekb.person"
--
Inherits: moviekb.ag_vertex
```

带索引和约束的标签会同时显示二者：

```cypher
CREATE GRAPH demo;
SET graph_path = demo;
CREATE VLABEL book;
CREATE PROPERTY INDEX ON book (title);
CREATE CONSTRAINT book_isbn_uq ON book ASSERT isbn IS UNIQUE;
```

```psql
\dGv demo.book
```

```
        List of labels
 Graph | Name |  Type  | Owner
-------+------+--------+-------
 demo  | book | vertex | agens

Vertex label "demo.book"
--
Property Indexes:
    "book_title_idx" btree (title)
Constraints:
    "book_isbn_uq" ASSERT (isbn) IS UNIQUE
Inherits: demo.ag_vertex
```

注意这个块**不**显示标签的列。要查看 `id`、`properties` 和任何提升列，请对表使用 `\d`，因为标签是表：

```psql
\d moviekb.movie
```

```
                                                          Table "moviekb.movie"
   Column   |  Type   | Collation | Nullable |                                          Default
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('moviekb.movie'::cstring), nextval('moviekb.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
Inherits: moviekb.ag_vertex
```

### 描述边标签 {#describe-the-edge-labels}

`\dGe` 是边标签版的 `\dGv`，块形状相同：

```psql
\dGe moviekb.acted_in
```

```
          List of labels
  Graph  |   Name   | Type | Owner
---------+----------+------+-------
 moviekb | acted_in | edge | agens

Edge label "moviekb.acted_in"
--
Inherits: moviekb.ag_edge
```

`\dGl` 是唯一不打印这些块的命令。它只是两类标签的汇总，没有更多内容。

### 列出属性索引 {#list-the-property-indexes}

`\dGi` 读取 `ag_property_indexes`，显示每个索引的 Cypher 定义，也就是重新创建它时你要输入的语句。没有属性索引的图不列出内容：

```psql
\dGi moviekb.*
```

```
No matching property indexes found.
```

```psql
\dGi demo.*
```

```
                                                List of property indexes
 Graph | LabelName |   IndexName    | Unique | Owner |                             Indexdef
-------+-----------+----------------+--------+-------+------------------------------------------------------------------
 demo  | book      | book_title_idx | f      | agens | CREATE PROPERTY INDEX book_title_idx ON book USING btree (title)
```

`+` 增加索引大小和注释：

```psql
\dGi+ demo.*
```

```
                                                             List of property indexes
 Graph | LabelName |   IndexName    | Unique | Owner |                             Indexdef                             |    Size    | Description
-------+-----------+----------------+--------+-------+------------------------------------------------------------------+------------+-------------
 demo  | book      | book_title_idx | f      | agens | CREATE PROPERTY INDEX book_title_idx ON book USING btree (title) | 8192 bytes |
```

唯一约束不是属性索引，不出现在这里。它显示在所属标签的 `\dGv` 或 `\dGe` 块中，并在 `\d` 中显示为排他约束。

```psql
DROP GRAPH demo CASCADE;
```

```
NOTICE:  drop cascades to 4 other objects
DETAIL:  drop cascades to sequence demo.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to vlabel book
DROP GRAPH
```

### 用模式缩小列表 {#narrow-a-listing-with-a-pattern}

这里的模式就是 PostgreSQL 的 `\d` 模式语言，作用于用点分隔的两个名称部分。该语言有 `*` 和 `?` 通配符、字符类，以及阻止大小写折叠的双引号。

两个部分指什么因命令而异，这个差异很容易让人踩坑：

| 命令 | *first*`.`*second* 的含义 |
| --- | --- |
| `\dG` | 图名。没有第二部分。 |
| `\dGl`、`\dGv`、`\dGe` | 先是图名，然后是**标签**名。 |
| `\dGi` | 先是图名，然后是**索引**名。 |

因此 `\dGi moviekb.movie` 找不到结果，因为 `movie` 会与索引名匹配：

```psql
\dGi moviekb.movie
```

```
No matching property indexes found.
```

请改用索引名，或使用 `moviekb.*` 并读取 `LabelName` 列。模式没有匹配项时会说明这一点，这并不是错误：

```psql
\dGv nosuchgraph.*
```

```
No matching labels found.
```

## AGDATA {#agdata}

`AGDATA` 指定数据目录，作用与 `PGDATA` 相同。恰好三个程序读取它：`initdb`、`pg_ctl` 和 `ag_ctl`。其他工具都不读取，包括 `agens`、`psql`、`pg_dump` 和 `pg_basebackup`。因此，如果希望一个变量被所有工具尊重，仍应设置 `PGDATA`。

导出一次后，这三个程序都不再需要 `-D`：

```shell
export AGDATA=/tmp/agensdata
ag_ctl status
```

```
ag_ctl: no server running
```

同时读取两个变量的程序之间优先级不同，所以同时设置前请先确认：

| 程序 | 顺序 |
| --- | --- |
| `initdb` | `-D`、`AGDATA`、`PGDATA`。 |
| `pg_ctl` 与 `ag_ctl` | `-D`、`PGDATA`、`AGDATA`。 |

`initdb` 决定目录后也会在自己的环境中设置 `AGDATA`，结尾提示使用 `ag_ctl`：

```shell
env -u PGDATA AGDATA=/tmp/agensdata initdb -U agens --no-sync
```

```
Success. You can now start the database server using:

    ag_ctl -D /tmp/agensdata -l logfile start
```

两个变量都未设置且没有 `-D` 时，消息只提到 `PGDATA`。`AGDATA` 其实同样可用：

```shell
ag_ctl status
```

```
ag_ctl: no database directory specified and environment variable PGDATA unset
Try "ag_ctl --help" for more information.
```

[部署](/zh/agensgraph/operations/deployment/)介绍数据目录应放在哪里，以及如何从 init 系统启动服务端。

## 另见 {#see-also}

- [服务端工具](/zh/agensgraph/operations/tools/)——`ag_ctl`、`pg_dump`、`pg_upgrade` 与图
- [示例数据集](/zh/agensgraph/get-started/example-dataset/)——上述列表示例描述的图
- [系统目录](/zh/agensgraph/system-catalogs/catalogs/)——这些命令查询的 `ag_graph`、`ag_label` 和 `ag_property_indexes`
- [服务端设置](/zh/agensgraph/reference/guc/)——会话运行 Cypher 前需要的 `graph_path`
- [PostgreSQL: psql](https://www.postgresql.org/docs/18/app-psql.html)——每个选项和其他所有元命令
- [PostgreSQL: pg_ctl](https://www.postgresql.org/docs/18/app-pg-ctl.html)——`ag_ctl` 的来源
