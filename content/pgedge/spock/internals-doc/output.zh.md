---
title: "Spock 输出插件"
description: "Spock 的逻辑解码输出插件及其协议、过滤钩子和调试方法。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/OUTPUT.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



这是 `spock` 的[逻辑解码](http://www.postgresql.org/docs/current/static/logicaldecoding.html)[输出插件](http://www.postgresql.org/docs/current/static/logicaldecoding-output-plugin.html)。它从 PostgreSQL 数据库中提取变更流，通过定义明确、传输高效的协议，经由网络发送给客户端。多种应用都可以读取这个协议。

`spock_output` 主要为逻辑流复制提供数据，其他应用也可以读取它的变更流。输出格式紧凑，便于快速解码。插件还支持通过钩子在上游过滤数据，只发送所需信息。

一次只复制一个数据库。还可以按表和复制来源选择其中一部分。设计上也便于将来支持按 WHERE 条件过滤。

收集变更无须触发器、外部定时进程或其他守护进程。插件使用 PostgreSQL 9.4 起支持的[复制槽](http://www.postgresql.org/docs/current/static/logicaldecoding-explanation.html#AEN66446) 积累变更，再通过 [PostgreSQL 流复制协议](http://www.postgresql.org/docs/current/static/protocol-replication.html) 发送。

与块级物理流复制相比，`spock_output` 的变更流可以跨 PostgreSQL 版本使用，非 PostgreSQL 客户端也可以读取。

逻辑解码只传输已更改的行。索引变更和 VACUUM 活动等不会通过网络发送。

复制槽让变更流可以在故障后可靠恢复。客户端断开或崩溃后可以重新连接，从最后处理的消息继续重放。断开期间的服务端变更会一直积累，等到客户端重连再发送。因此，即使没有客户端连接，服务器仍会占用资源以保留这些变更。

# 为什么需要另一个输出插件？ {#why-another-output-plugin}

[`DESIGN.md`](/zh/pgedge/spock/internals-doc/design/) 讨论了为什么用 `wal2json` 等通用逻辑解码插件向下游提供逻辑复制数据并不理想，主要原因是性能。

# 架构与交互过程 {#architecture-and-high-level-interaction}

客户端使用 PostgreSQL 网络协议连接数据库，设置 `replication=database`，随后用 [`CREATE_REPLICATION_SLOT ... LOGICAL ...` 或 `START_REPLICATION SLOT ... LOGICAL ...` 命令](http://www.postgresql.org/docs/current/static/logicaldecoding-walsender.html) 启动变更流。PostgreSQL 的 walsender 进程会加载输出插件。也可以通过普通连接调用 [SQL 函数](http://www.postgresql.org/docs/current/static/logicaldecoding-sql.html) 使用插件，主要用于调试。

客户端通过 `START_REPLICATION SLOT ... LOGICAL ...` 的参数声明支持的 `spock` 协议版本、是否要求二进制格式等。

插件处理完连接参数后，连接进入流复制协议模式。它沿用了 `COPY` 命令的协议，也称为 COPY BOTH 模式。PostgreSQL 随后调用插件中的函数，将事务流交给插件解码，转换为网络消息。变更流会持续到客户端断开连接。

启动之后，客户端只需定期发出反馈，以便复制槽丢弃不再需要的变更历史。客户端*必须*反馈，否则服务器的 `pg_xlog` 最终会写满，导致服务停止。


# 用法 {#usage}

客户端与服务器按以下顺序交互。

* 客户端通过 PostgreSQL 前后端协议连接服务器。
    * 连接选项必须包含 `replication=database` 和 `dbname=[...]`。
    * 客户端库可使用 `libpq`，也可使用其他支持复制子协议的库。
    * 认证和协议加密采用与普通连接相同的机制。
* 客户端发送 `IDENTIFY_SYSTEM`。
    * 服务器返回一行系统标识信息。
* 若是首次设置，客户端发送 `CREATE_REPLICATION_SLOT slotname LOGICAL 'spock'`。
    * 服务器返回成功信息和快照标识符。
    * 客户端此时可以让本连接保持空闲，在其他连接上使用该快照标识符。
* 客户端发送 `START_REPLICATION SLOT slotname LOGICAL 0/0 (...options...)`，开始流式传输。之后重复以下过程。
    * 服务器发出 `spock` 消息块，封装在复制协议的 `CopyData` 消息中。
    * 客户端接收并解包消息，再解码 `spock` 消息块。
    * 客户端不时向服务器发送备库状态更新，确认重放进度。
* 循环持续到客户端在前后端协议层正常终止连接，或连接因其他原因断开。

 `IDENTIFY_SYSTEM`、`CREATE_REPLICATION_SLOT` 和 `START_REPLICATION` 的具体定义见[复制协议文档](http://www.postgresql.org/docs/current/static/protocol-replication.html)。

## 建立复制连接 {#make-a-replication-connection}

使用 `spock` 插件前，先通过选定的客户端库建立 PostgreSQL 前后端协议连接，并传入 `replication=database`。`database` 是固定字面量。实际数据库名另按通常方式通过 `dbname` 传入。`replication` 是和 `user`、`dbname` 同级的连接参数，不属于 GUC 配置项，也不能放在连接的 `options` 中。

`libpq` 连接串示例：

    'user=postgres replication=database sslmode=verify-full dbname=mydb'

创建逻辑槽时，插件名填 `'spock'`。

详见复制协议文档。

## 获取系统标识 {#get-system-identity}

如需查看系统信息，可使用 `IDENTIFY_SYSTEM` 命令。

	  systemid       | timeline |  xlogpos  | dbname | dboid
    ---------------------+----------+-----------+--------+-------
     6153224364663410513 |        1 | 0/C429C48 | testd  | 16385
    (1 row)

详见复制协议文档。

## 按需创建复制槽 {#create-the-slot-if-required}

如果应用在首次使用时自行创建复制槽，且从未连接过本系统上的这个数据库，就需要先建槽。复制槽会一直记录客户端的重放状态，即使客户端断开也是如此。

应用可自行命名复制槽，最长 63 个字符。强烈建议在名称中明确标识应用及其运行主机。

插件名使用 `spock`。

例如：

    CREATE_REPLICATION_SLOT "reporting_host_42" LOGICAL "spock";

`CREATE_REPLICATION_SLOT` 返回快照标识符。通过 [`SET TRANSACTION SNAPSHOT`](http://www.postgresql.org/docs/current/static/sql-set-transaction.html) 可查看建槽瞬间的数据库状态。槽输出的第一条变更紧接在该快照之后，适合用来克隆数据库的初始状态。仅关心后续变更的应用可忽略快照。只有执行 `CREATE_REPLICATION_SLOT` 的连接仍然打开且未执行其他命令时，此快照才有效。

## 发送复制参数 {#send-replication-parameters}

客户端发送以下命令：

    START_REPLICATION SLOT "the_slot_name" LOGICAL (
	'Expected_encoding', 'UTF8',
	'Max_proto_major_version', '1',
	'Min_proto_major_version', '1',
	...moreparams...
    );

这会启动复制。

参数决定插件是否接受复制请求，以及是否按预期格式输出变更。`spock` 参数见单独的 `spock` 协议文档。

## 处理启动消息 {#process-the-startup-message}

`spock_output` 首先发送包含启动消息的 `CopyData`。消息中的键值对描述上游输出插件的能力、插件版本、PostgreSQL 版本、所选元组格式等。

如果下游客户端无法接受应答，可以在此时正常关闭连接。随后可以通知用户，或根据启动消息调整参数并重新连接。

## 读取变更流 {#consume-the-change-stream}

`spock_output` 开始连续发送 `CopyData` 协议消息，每条封装一条 `spock` 消息。消息格式详见协议文档。

这些消息描述事务边界、变更行等信息。

当客户端断开、上游服务器重启、管理员终止上游 walsender、网络故障或连接因其他原因中断时，变更流才会结束。

客户端应定期向服务器反馈已重放到的位置。服务器据此可释放原本为重新发送变更而保留的资源。详见复制协议文档中的[热备反馈消息](http://www.postgresql.org/docs/current/static/protocol-replication.html)。

## 正常断开连接 {#disconnect-gracefully}

使用客户端库通常的关闭连接方法即可，无须额外操作。一般建议在断开前再发送一次最终的备库状态消息。

# 测试 {#tests}

`spock_output` 附带两组测试：`pg_regress` 回归测试和用于验证协议的 Python 测试。

`pg_regress` 测试检查非法参数的处理及基本功能。构建农场可在源码树中运行 `make check`。采用外部 PGXS 构建时，也可对已有 PostgreSQL 安装运行 `make clean installcheck`。

Python 测试在协议层检查扩展发送的数据，校验消息结构、顺序和内容，覆盖面较广。可使用 SQL 层逻辑解码接口，也可使用包含 https://github.com/psycopg/psycopg2/pull/322 改动的 psycopg2 通过 walsender 流复制协议运行。测试也覆盖内部二进制格式。详见 `test/README.md`。

在非 UTF-8 编码的实例上，测试可能失败。二进制协议载荷中的文本用了其他编码，psql 无法将其识别为需要解码的文本。测试只使用 7 位 ASCII *应该*能避开这个问题。

# 转发变更集 {#changeset-forwarding}

将 `spock_output` 配合可在下游应用变更的客户端使用，就能在多个 PostgreSQL 服务器之间进行级联复制。

有两种转发模式。

* 全部转发。无论事务来自直接上游，还是来自更上游的节点，都会复制，并发送事务中的所有行。在 PostgreSQL 9.4 上，这是唯一可用的模式。

  不设置行过滤钩子或事务过滤钩子即可使用此模式。

* 过滤转发。只有客户端提供的事务过滤钩子要求跳过时，才不复制该事务。对于保留的事务，若配置了行过滤钩子，被它排除的行变更也不会复制。

  安装事务过滤钩子、行过滤钩子或两者即可启用（见「钩子」）。

服务器会启用变更集来源信息，并在启动应答中将 `forward_changeset_origins` 设为 true。随后按协议约定，在各事务的 `BEGIN` 之后发送来源消息。为节省带宽，直接来自当前上游的事务省略该消息。因此，若 `forward_changeset_origins` 为 true，未注明来源的事务必定来自运行解码插件的直接上游。

结合钩子选择要转发的事务，客户端就能构建各种拓扑，其中一例便是双向复制。

# 选择性复制 {#selective-replication}

配置行过滤钩子，可以在服务器端过滤复制流，只复制部分变更。


# 钩子 {#hooks}

`spock_output` 提供多个扩展点，应用程序可在这些位置调整或替换其行为。

钩子可以使用贯穿逻辑解码会话的内存上下文。必要时也可切换到寿命更长的上下文，此时须自行负责清理。各类钩子的实际调用上下文见下文。

## 钩子设置函数 {#hook-setup-function}

下游必须通过客户端参数 `hooks.setup_function` 提供一个可从 SQL 调用的服务端函数，名称须包含模式。该函数的 SQL 签名如下。

    CREATE OR REPLACE FUNCTION funcname(hooks internal, memory_context internal)
    RETURNS void STABLE
    LANGUAGE c AS 'MODULE_PATHNAME';

系统会检查权限。运行输出插件的用户必须有权调用该函数。函数名*必须*包含模式，并按普通限定标识符解析。

第一个参数指向新分配的钩子函数指针结构。设置函数负责填充该结构，不能释放它。

若钩子需要跨调用保存私有数据，设置函数应从第二个参数取得 `MemoryContext` 指针，通过 `MemoryContextAlloc` 在该上下文中分配数据结构，并将指针存入 `hooks->hooks_private_data`。后续调用即可访问它。逻辑解码内存上下文销毁时会自动释放该结构，不要在其中存放需要手动清理的资源。

除设置钩子和启动钩子外，其余钩子都在短期内存上下文中调用。若要在返回后保留已分配的数据，须切换到传给设置函数的内存上下文，并在那里分配。

各钩子有自己的 C 签名，详见下文。指针必须直接指向相应函数。客户端不希望设置的钩子须保留为空指针。

示例见 `examples/hooks`。参数结构定义在 `spock_output/hooks.h` 中，安装扩展时该文件会装入 PostgreSQL 源码树。

每启用一个钩子，启动应答中就会增加一个参数。客户端必须检查这些参数来确认启用情况，不能仅凭未见报错就判断启用成功。

钩子在执行逻辑解码的后端进程中调用。除启动钩子外，钩子看到的系统目录是待检查事务或行变更发生时的状态。访问未设 `user_catalog_table` 关系选项的非目录表是不安全的。因此，从钩子调用任意函数或用户定义的过程也不安全。


## 启动钩子 {#startup-hook}

开始逻辑解码时调用启动钩子。

启动钩子可通过 in_params 检查客户端传给输出插件的参数，*不得修改*这些参数。

启动钩子可向初始为 NIL 的 out_params 列表追加参数，随启动参数消息返回给客户端。每项必须是 `DefElem`，`defname` 为参数名，arg 为 `String` 值，可用 `makeDefElem(...)` 创建。参数项及其内容须分配在逻辑解码内存上下文中。

通过 walsender 解码时，启动钩子只调用一次，会话结束时可能不会调用清理钩子。

通过 SQL 接口解码时，一条数据库连接可启动多个解码会话，启动钩子会被多次调用。相邻两次启动之间保证会调用清理钩子。

启用成功时，启动应答中的 `hooks.startup_hook_enabled` 为 true。

与其他钩子不同，启动钩子看到的是数据库当前状态的快照，能够安全地访问所有表。

启动钩子的调用上下文寿命与解码会话相同，就是传给钩子设置函数的上下文。

## 事务过滤钩子 {#transaction-filter-hook}

事务过滤钩子可以根据事务的来源节点将整个事务排除在解码和复制之外。

其参数 `const TxFilterHookArgs *` 包含以下内容。

* 客户端提供的钩子参数（如有）。
* 事务来源的 `RepOriginId`。

钩子必须返回布尔值。true 表示保留并发给客户端，false 表示丢弃。注意，这与底层逻辑解码事务过滤钩子的布尔值含义相反。

钩子函数*不得*释放参数结构，也不得修改其内容。

仅 PostgreSQL 9.5 及以上版本会调用事务过滤钩子，9.4 会忽略它。

同一事务中单项变更的来源可能不同于整个事务，详见「来源过滤」。若事务被过滤掉，其中的所有变更也会被过滤掉，不论各自的来源如何。

启用成功时，启动应答中的 `hooks.transaction_filter_enabled` 为 true。

在该钩子中分配的内存会在调用结束时释放。

## 行过滤钩子 {#row-filter-hook}

每行调用一次行过滤钩子。传入的信息包括表、事务来源和行来源。

其参数 `const RowFilterHookArgs*` 包含以下内容。

* 客户端提供的钩子参数（如有）。
* 受变更影响的 `Relation`。
* 变更类型：I 表示插入，U 表示更新，D 表示删除。

返回 true 保留该行变更并将其发给客户端，返回 false 则丢弃。

函数*不得*释放参数结构，也不得修改其内容。

若要排除整个事务，用事务过滤钩子比逐行过滤效率更高。

启用成功时，启动应答中的 `hooks.row_filter_enabled` 为 true。

在该钩子中分配的内存会在调用结束时释放。

## 关闭钩子 {#shutdown-hook}

解码会话结束时会调用关闭钩子，但基于复制协议的 walsender 会话可能直接终止，不能指望它必定执行。它主要用于 SQL 解码接口反复启动会话时的清理。

除非显式切换到 `TopMemoryContext` 等寿命更长的上下文，否则无须编写钩子来释放内存。在钩子上下文中分配的内存会随解码会话结束自动释放。

# 限制 {#limitations}

上文介绍了逻辑解码及 `spock_output` 的优点。下述限制同时适用于 `spock_output` 和本文所述版本的 PostgreSQL 逻辑解码。

主要限制如下。

## 通信主要是单向的 {#mostly-one-way-communication}

按协议规定，复制开始后，下游只能向上游发送重放进度消息。若要重新初始化复制，须先断开连接。

如需向上游传回其他信息，客户端可另建普通 libpq 连接，向表写数据或调用函数。应用也可建立反向复制连接，专门把信息从下游送往上游。

详见协议文档的「协议流程」。

## 全局对象与共享目录的变更 {#doesnt-replicate-global-objectsshared-catalog-changes}

PostgreSQL 将一些跨数据库的对象存入*共享目录*。例如：

* 角色（用户和组）
* 用户和数据库上的安全标签

`spock_output` 无法复制这些对象。管理它们的 DDL 无法在单个数据库中捕获，这里的逻辑解码也不处理 DDL。

全局对象的变更须通过外部手段同步。

## 物理备库故障切换 {#physical-replica-failover}

在本文所述实现中，复制槽状态不会随物理复制传到备库，所以逻辑解码无法自动跟随物理故障切换。提升流复制备库后，需要为逻辑复制客户端手工重建复制槽并重新连接。这是该版本 PostgreSQL 核心的限制。

也没有内置机制保证故障主库上的逻辑复制槽未越过刚提升的物理备库。客户端可能已从旧主库收到某些变更，但它们还没传到物理备库。*即使物理流复制采用同步模式*，这种情况也可能发生，尽管概率很低：PostgreSQL 会先发送复制数据，只延迟事务提交在主库上的可见时间。要完全避免它，需要支持备库间的严格顺序。

按此设计，要通过逻辑复制完成故障切换，就不能在候选节点中混用物理备库。逻辑复制客户端必须为候选逻辑副本维护复制槽，若有多个候选节点，应保证提升进度最靠前的一个。

## 仅能复制完整事务 {#can-only-replicate-complete-transactions}

此处的逻辑解码仅在事务提交之后才能复制它。这样可以跳过已回滚事务，但大事务必须先在上游完成，才能在下游开始，因而会增加复制延迟。

## 每次只复制一个事务 {#replicates-only-one-transaction-at-a-time}

逻辑解码按提交顺序串行处理事务，spock_output 无法交错重放并发事务。重放大事务时，排在后面的小事务要等待，延迟可能很高。

## 插入和更新需要唯一索引 {#unique-index-required-for-inserts-or-updates}

要复制 `INSERT` 或 `UPDATE`，表必须有 `PRIMARY KEY` 或 `UNIQUE` 索引（只能包含列，且不能是部分索引），从而提供 `REPLICA IDENTITY`。否则 `spock_output` 无法确定要发送哪个旧键，接收方也就无法识别被更新的元组。

## UNLOGGED 表的复制限制 {#unlogged-tables-arent-replicated}

`UNLOGGED` 表不将数据写入 WAL，因此逻辑复制和物理复制都不能复制其内容。要复制 `UNLOGGED` 表，需要使用基于触发器的方案。

## `UPDATE` 中常包含未改动的字段 {#unchanged-fields-are-often-sent-in-update}

更新元组时没有记录每个字段是否变脏，因此逻辑解码通常无法判断具体改了哪些字段。只有对于可由 TOAST 处理、且足够大而实际存入外部 TOAST 表的变长字段，才可能识别并省略未改动的值。

# 故障排查与调试 {#troubleshooting-and-debugging}

## 预览复制槽中的待处理数据 {#non-destructively-previewing-pending-data-on-a-slot}

使用 `spock_output` 的 JSON 模式可查看槽中待处理的事务，同时保留它们供正常使用该槽的客户端接收。宜使用逻辑解码的 SQL 接口，它比 `pg_recvlogical` 更便于精细控制。

只有槽上没有其他客户端连接时才能预览。

用 `spock_slot_peek_changes` 查看变更流，槽的消费位置不会前移。排查下游错误时，这种方法尤其方便，可以直接阅读 JSON 格式的事务内容。调用时仍须向输出插件提供最低限度的必需参数。

以下面的设置为例：

    CREATE TABLE discard_test(blah text);
    SELECT 'init' FROM pg_create_logical_replication_slot('demo_slot', 'spock_output');
    INSERT INTO discard_test(blah) VALUES('one');
    INSERT INTO discard_test(blah) VALUES('two1'),('two2'),('two3');
    INSERT INTO discard_test(blah) VALUES('three1'),('three2');

可以这样预览变更流：

     SELECT location, xid, data
     FROM spock_slot_peek_changes('demo_slot', NULL, NULL,
              'min_proto_version', '1', 'max_proto_version', '1',
              'startup_params_format', '1', 'proto_format', 'json');

两个 `NULL` 分别表示不按指定 LSN 或变更条数停止。所有待处理数据解码完毕，或查询被取消时，解码才会停止。

首先输出键值形式的启动消息，随后输出变更数据行，例如：

     location  | xid  |                                            data
     0/4E8AAF0 | 5562 | {"action":"B", has_catalog_changes:"f", xid:"5562", first_lsn:"0/4E8AAF0", commit_time:"2015-11-13 14:26:21.404425+08"}
     0/4E8AAF0 | 5562 | {"action":"I","relation":["public","discard_test"],"newtuple":{"blah":"one"}}
     0/4E8AB70 | 5562 | {"action":"C", final_lsn:"0/4E8AB30", end_lsn:"0/4E8AB70"}
     0/4E8ABA8 | 5563 | {"action":"B", has_catalog_changes:"f", xid:"5563", first_lsn:"0/4E8ABA8", commit_time:"2015-11-13 14:26:32.015611+08"}
     0/4E8ABA8 | 5563 | {"action":"I","relation":["public","discard_test"],"newtuple":{"blah":"two1"}}
     0/4E8ABE8 | 5563 | {"action":"I","relation":["public","discard_test"],"newtuple":{"blah":"two2"}}
     0/4E8AC28 | 5563 | {"action":"I","relation":["public","discard_test"],"newtuple":{"blah":"two3"}}
     0/4E8ACA8 | 5563 | {"action":"C", final_lsn:"0/4E8AC68", end_lsn:"0/4E8ACA8"}
     ....

输出依次是变更的 LSN（日志序列号）、执行该变更的顶层事务 ID，以及 JSON 格式的变更数据。

可以根据 xid 的变化及 B（开始）、C（提交）消息识别事务边界，I 表示单行插入。如果已知复制来源、提交时间戳等信息，也会一并显示。

关于预览函数，参见 http://www.postgresql.org/docs/current/static/functions-admin.html 。

若需要二进制格式，可配合 `spock_slot_peek_binary_changes` 与 `native` 协议，但这种形式对排查问题通常帮助较小。

# 手工丢弃槽中的变更 {#manually-discarding-a-change-from-a-slot}

有时确实需要手工清除复制槽中的一项或多项变更，通常是因为下游重放代码发生错误，需要执行恢复操作。

可先用预览函数找出希望丢弃到哪个 LSN（日志序列号）。详见上文「预览复制槽中的待处理数据」。

丢弃只能从当前流位置开始，到指定位置为止。如果预览发现前面仍有需要保留的变更，必须先让下游重放完应保留的部分并发送确认。无法直接从待处理变更流中裁掉中间一段。

预览并确认目标 LSN 后，调用 `spock_slot_get_changes` 并指定 `upto_lsn`，可从槽中消费目标位置之前的变更，不含目标位置本身。之后从该位置恢复重放。

例如，要丢弃上例的第一个事务 5562，并从事务 5563 的 BEGIN 所在 LSN `0/4E8ABA8` 开始解码，可以执行：

      SELECT location, xid, data
      FROM spock_slot_get_changes('demo_slot', '0/4E8ABA8', NULL,
               'min_proto_version', '1', 'max_proto_version', '1',
               'startup_params_format', '1', 'proto_format', 'json');

此处用 `_get_changes` 取代 `_peek_changes`，并将 `upto_lsn` 从 `NULL` 改为 `'0/4E8ABA8'`。





---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/internals-doc/OUTPUT.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
