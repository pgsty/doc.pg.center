---
title: 函数
description: DocumentDB 1.0 中由 pg_documentdb 扩展暴露的 PostgreSQL 函数参考，包括 CRUD、模式、索引、诊断、用户和角色管理。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/postgres-api/functions.md
weight: 20
translation_source_sha256: 7cd3688e8d7642a32a0c5d083821518328788cf272dea75316802b542dc67248
translation_review: AI-assisted bilingual review; 2026-11-07
---

`pg_documentdb` 通过 `documentdb_api` 模式中的 PostgreSQL 函数公开其公共 API。`pg_documentdb_gw` 处理的 MongoDB 线协议命令被实现为这些函数的轻量级包装器，因此你可直接从任何 PostgreSQL 客户端（例如 `psql`、`psycopg`、JDBC）调用它们。

所有 BSON 参数都编码为 PostgreSQL 的 `bson` 值（由 `pg_documentdb_core` 扩展提供）。例如，可以在 `psql` 中通过 `'{ ... }'::documentdb_core.bson` 这样的类型转换传入 BSON 参数字面量。

> **本页描述 DocumentDB 1.0**（扩展版本 `1.0-0`）。

> **下文函数签名的读法。** 参数名与扩展在 `pg_documentdb/sql/udfs/` 中的实际声明一致，可直接用于 `p_database_name => 'mydb'` 这样的命名参数调用。这些标识符未加引号，PostgreSQL 会将其转换为小写：源码中的 `commandSpec` 在 `\df documentdb_api.*` 输出中显示为 `commandspec`；源码中的 `int8`/`bool`/`float8` 则显示为 `bigint`/`boolean`/`double precision`。调用时两种写法都可使用。类型名没有加模式限定：`bson` 和 `bsonsequence` 位于 `documentdb_core` 中。具有**两个或更多** `OUT` 参数的函数返回 `record`，应通过 `SELECT * FROM ...` 调用；只有一个 `OUT` 参数的函数直接返回该参数的类型，使用普通的 `SELECT fn(...)` 即可。少数线协议入口是 PostgreSQL `PROCEDURE`，必须通过 `CALL` 调用，下文会分别注明。

## CRUD 操作 {#crud-operations}

用于创建、读取、更新和删除文档的函数。

| 函数 | 描述 |
| --- | --- |
| `documentdb_api.insert(p_database_name text, p_insert bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, OUT p_result bson, OUT p_success boolean)` | 执行 MongoDB `insert` 命令。 |
| `documentdb_api.update(p_database_name text, p_update bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, OUT p_result bson, OUT p_success boolean)` | 执行 MongoDB `update` 命令。 |
| `documentdb_api.delete(p_database_name text, p_delete bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, OUT p_result bson, OUT p_success boolean)` | 执行 MongoDB `delete` 命令。 |
| `documentdb_api.find_and_modify(p_database_name text, p_message bson, p_transaction_id text DEFAULT NULL, OUT p_result bson, OUT p_success boolean)` | 执行 MongoDB `findAndModify` 命令。 |
| `documentdb_api.insert_one(p_database_name text, p_collection_name text, p_document bson, p_transaction_id text DEFAULT NULL)` | 方便的包装函数，通过数据库和集合名称插入单个文档，并返回 `insert` 响应。 |
| `documentdb_api_internal.insert_one(p_collection_id bigint, p_shard_key_value bigint, p_document bson, p_transaction_id text)` | **已弃用且不可用。** 实现为一个始终抛出 `insert_one is deprecated and should not be called` 的占位符。请使用上方的公共 `documentdb_api.insert_one`。 |
| `CALL documentdb_api.bulkWrite(p_command bson, p_ops bsonsequence DEFAULT NULL, p_ns_info bsonsequence DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | **1.0 版本未实现。** `PROCEDURE` 存在，但每次调用均抛出 `bulkWrite is not yet implemented`，且在事务内部调用时也会被拒绝。 |
| `documentdb_api.find_cursor_first_page(database text, commandSpec bson, cursorId int8 DEFAULT 0, OUT cursorPage bson, OUT continuation bson, OUT persistConnection bool, OUT cursorId int8)` | 为 `find` 命令打开游标并返回其第一页。省略 `cursorId` 由服务器自动生成。 |
| `documentdb_api.aggregate_cursor_first_page(database text, commandSpec bson, cursorId int8 DEFAULT 0, OUT cursorPage bson, OUT continuation bson, OUT persistConnection bool, OUT cursorId int8)` | 为 `aggregate` 命令打开游标并返回其第一页。省略 `cursorId` 由服务器自动生成。 |
| `documentdb_api.list_collections_cursor_first_page(database text, commandSpec bson, cursorId int8 DEFAULT 0, OUT cursorPage bson, OUT continuation bson, OUT persistConnection bool, OUT cursorId int8)` | 返回 `listCollections` 结果。尽管名称如此，结果始终为单个批次——请参见下方说明。 |
| `documentdb_api.list_indexes_cursor_first_page(database text, commandSpec bson, cursorId int8 DEFAULT 0, OUT cursorPage bson, OUT continuation bson, OUT persistConnection bool, OUT cursorId int8)` | 返回 `listIndexes` 结果。始终为单个批次——请参见下方说明。 |
| `documentdb_api.cursor_get_more(database text, getMoreSpec bson, continuationSpec bson, OUT cursorPage bson, OUT continuation bson)` | 返回现有游标（`getMore`）的下一页。 |
| `documentdb_api.count_query(database text, countSpec bson, OUT document bson)` | 执行 MongoDB `count` 命令。 |
| `documentdb_api.distinct_query(database text, distinctSpec bson, OUT document bson)` | 执行 MongoDB `distinct` 命令。 |
| `documentdb_api.collection(p_database_name text, p_collection_name text, OUT shard_key_value bigint, OUT object_id bson, OUT document bson)` | 读取集合原始行的返回集合的函数，使用时有两项限制，见下文说明。 |
{.fields}

> **四个 `*_cursor_first_page` 函数都声明为 `STRICT`。** 如果给 `cursorId` 显式传入 `NULL`（使用预备语句的客户端无法省略位置参数时可能这样做），会返回一行所有列均为 `NULL` 的结果，不报错，也不创建游标。请省略该参数，不要绑定 `NULL`。

> **`list_collections_cursor_first_page` 和 `list_indexes_cursor_first_page` 忽略 `cursorId`。** 两者均硬编码为单批次查询，因此 `OUT cursorId` 始终返回 `0`，`OUT continuation` 始终返回 `NULL`；结果无法通过 `cursor_get_more` 继续。只有 `find` 和 `aggregate` 会产生可继续的游标。

> **`documentdb_api.collection` 仅作为 FROM 子句中的表函数，且名称必须为字面量。** 计划器钩子会将 `SELECT * FROM documentdb_api.collection('mydb', 'users')` 重写为对底层表的扫描。如果任一名称参数不是常量（即列引用、相关子查询或 PL/pgSQL 变量），则跳过重写，直接调用会引发 `Collection function should be only used in a FROM clause`。指定一个不存在的集合是允许的——它会被重写为空扫描，并返回零行。

### 写入过程 {#write-procedures}

`insert`、`update` 和 `delete` 也作为 `PROCEDURE` 暴露。`delete` 具有 `_txn_proc` 形式，但没有 `_bulk` 形式。

| 过程 | 描述 |
| --- | --- |
| `CALL documentdb_api.insert_bulk(p_database_name text, p_insert bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | 插入文档，每个子批处理完成后提交，而非作为一个整体提交。 |
| `CALL documentdb_api.update_bulk(p_database_name text, p_update bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | `update` 的等效形式，对应 `insert_bulk`。 |
| `CALL documentdb_api.insert_txn_proc(p_database_name text, p_insert bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | 插入文档，不为每条语句开启子事务。 |
| `CALL documentdb_api.update_txn_proc(p_database_name text, p_update bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | `update` 的等效形式，对应 `insert_txn_proc`。 |
| `CALL documentdb_api.delete_txn_proc(p_database_name text, p_delete bson, p_insert_documents bsonsequence DEFAULT NULL, p_transaction_id text DEFAULT NULL, INOUT p_result bson DEFAULT NULL, INOUT p_success boolean DEFAULT NULL)` | `delete` 的等效形式，对应 `insert_txn_proc`。 |
{.fields}

> **这些过程均不可在显式事务块内调用。** 当检测到打开的事务时，每个过程都会引发类似 `the insert procedure cannot be used in transactions. Please use the insert function instead`（`ERRCODE_DOCUMENTDB_OPERATIONNOTSUPPORTEDINTRANSACTION`）的错误。它们之间的区别仅在于提交粒度，而非事务支持：`_bulk` 按子批处理提交，`_txn_proc` 跳过每条语句的子事务。在事务内部，请使用普通的 `insert`/`update`/`delete` 函数。

> **网关默认不使用这些过程。** 它们受网关设置控制，默认为 `false` — `enableWriteProcedures` 选择 `_txn_proc` 变体，`enableWriteProceduresWithBatchCommit` 选择 `_bulk` 变体（仅限插入和更新）——即使启用，网关也仅在事务外的写操作中使用它们。默认情况下，所有线协议写操作均通过 `documentdb_api.insert` / `documentdb_api.update` / `documentdb_api.delete` 执行。

## 集合与数据库管理 {#collection-and-database-management}

用于管理集合、视图、数据库和分片的函数。

| 函数 | 描述 |
| --- | --- |
| `documentdb_api.create_collection(p_database_name text, p_collection_name text)` | 创建一个空集合，不带任何选项。若成功创建则返回 `true`，若已存在则返回 `false`。 |
| `documentdb_api.create_collection_view(dbname text, createSpec bson)` | 支持线协议 `create` 命令：从完整的 BSON 规范创建集合 **或** 视图。接受创建选项，如 `viewOn`/`pipeline`、`validator` 和 `validationLevel`，这些选项无法通过上述两个参数的 `create_collection` 表达。（`coll_mod` 可在现有集合上更改相同选项。）`changeStreamPreAndPostImages` 还需要 `documentdb.enablePreImages` GUC，其默认值为 `off`。 |
| `documentdb_api.drop_collection(p_database_name text, p_collection_name text, p_write_concern bson DEFAULT NULL, p_collection_uuid uuid DEFAULT NULL, p_track_changes bool DEFAULT true)` | 删除一个集合。 |
| `documentdb_api.rename_collection(p_database_name text, p_collection_name text, p_target_name text, p_drop_target bool DEFAULT false)` | 使用显式参数重命名一个集合。 |
| `documentdb_api.rename_collection(p_commandspec bson)` | 接受线协议 `renameCollection` BSON 规范的重载形式。这是网关调用的形式。 |
| `documentdb_api.drop_database(p_database_name text, p_write_concern bson DEFAULT NULL)` | 删除一个数据库及其所有集合。 |
| `documentdb_api.list_databases(p_list_databases_spec bson)` | 返回所有数据库的信息。 |
| `documentdb_api.shard_collection(p_database_name text, p_collection_name text, p_shard_key bson, p_is_reshard bool DEFAULT true)` | 在指定键上对集合进行分片或重新分片。这是网关调用的形式。**首次分片时请传递 `p_is_reshard => false`** —— 详见下方说明。 |
| `documentdb_api.shard_collection(p_shard_key_spec bson)` | 单参数重载，接收整个请求作为 BSON。 |
| `documentdb_api.reshard_collection(p_shard_key_spec bson)` | 对已分片的集合进行重新分片。 |
| `documentdb_api.unshard_collection(p_shard_key_spec bson)` | 从分片集合中移除分片键，使其恢复为单个未分片的表。 |
| `documentdb_api.coll_mod(p_database_name text, p_collection_name text, p_spec bson)` | 执行 MongoDB `collMod` 命令。在现有集合上更改集合选项 —— `viewOn`、`pipeline`、`validator`、`expireAfterSeconds`、`changeStreamPreAndPostImages`。 |
| `documentdb_api.compact(p_spec bson)` | 执行 MongoDB `compact` 命令。`mode` 可为 `standard`（默认，普通 `VACUUM`）、`full`（`VACUUM FULL`）或 `updateStats`（`ANALYZE`）。`full` 需要一个默认关闭的 GUC —— 详见下方说明。 |
{.fields}

> **分片键必须使用哈希方式。** 分片键文档中的每个值都必须是字符串 `"hashed"`；其他值会报错 `only shard keys that use hashed are supported`，如果是其他字符串，则报错 `Shard key value provided is invalid`。因此，首次分片的调用形式为 `SELECT documentdb_api.shard_collection('mydb', 'users', '{ "value": "hashed" }'::documentdb_core.bson, false);`。

> **`shard_collection` 默认为重新分片。** `p_is_reshard` 默认为 `true`，因此在尚未分片的集合上使用自然的三参数调用会因 `Collection <db>.<coll> is not sharded`（`ERRCODE_DOCUMENTDB_NAMESPACENOTSHARDED`）而失败。对于初始分片，请显式传递 `false`。

> **分片操作会重写整个集合。** `shard_collection`、`reshard_collection` 和 `unshard_collection` 都会建立影子表并重新插入所有文档，因此执行期间应预留大约两倍于集合大小的磁盘空间，运行时间也会与集合大小成正比。这些操作都不会为此发出警告。

> **`compact` 的 `mode: "full"` 模式要求启用 `documentdb.enableCompactVacuumFull`，而该参数默认为 `off`。** 参数关闭时，`full` 压实只返回 `{ "ok": 1, "bytesFreed": 0 }`，不回收任何空间，也没有错误或警告。开启该参数后才会执行阻塞式 `VACUUM FULL`。`standard` 和 `updateStats` 模式始终执行。`bytesFreed` 是清理前后集合磁盘占用的实测减少量，因此 `standard` 压实通常报告 `0`：普通 `VACUUM` 使空间可以复用，但很少缩小文件。（在通过 `ALTER EXTENSION documentdb UPDATE` 将模式更新到 `1.0-0` 之前，`bytesFreed` 仍使用旧的膨胀估算值。）`dryRun: true` 不执行清理，只将该估算值作为 `estimatedBytesFreed` 返回。

## 索引管理 {#index-management}

| 函数 | 描述 |
| --- | --- |
| `documentdb_api_internal.create_indexes_non_concurrently(p_database_name text, p_arg bson, p_skip_check_collection_create boolean DEFAULT false)` | 在前台创建索引，期间会阻塞写入。在默认 `p_skip_check_collection_create => false` 下，如果数据表未在当前事务中创建，则会引发异常，因此对现有集合的直接调用需要 `p_skip_check_collection_create => true`。下面的后台路径在创建集合本身时会内部调用它。 |
| `documentdb_api.create_indexes_background(p_database_name text, p_index_spec bson, OUT retval bson, OUT ok boolean, OUT requests bson)` | 验证索引规范并**排队**构建，然后立即返回——它不会等待索引构建完成。 |
| `documentdb_api_internal.check_build_index_status(p_arg bson, OUT retval bson, OUT ok boolean, OUT complete boolean)` | 报告 `create_indexes_background` 加入队列的构建任务状态，参数为该调用返回的 `requests` 文档。 |
| `CALL documentdb_api.drop_indexes(p_database_name text, p_arg bson, INOUT retval bson DEFAULT NULL)` | 通过线协议 `dropIndexes` 命令删除索引。实现为一个 `PROCEDURE`。 |
{.fields}

### 从 SQL 构建索引 {#building-an-index-from-sql}

`createIndexes` 协议需要两次调用。网关会自动完成两部分工作；直接通过 SQL 调用时，必须显式执行。请先创建集合：如果 `create_indexes_background` 需要自行创建集合，索引就会在本次调用中直接构建，无需执行步骤 2。

步骤 1：将构建任务加入队列，然后**提交**：

```sql
SELECT ok, requests FROM documentdb_api.create_indexes_background(
    'mydb',
    '{ "createIndexes": "users", "indexes": [ { "key": { "email": 1 }, "name": "email_1" } ] }'::documentdb_core.bson
);
COMMIT;
```

```text
 ok |                                     requests
----+----------------------------------------------------------------------------------
 t  | { "indexRequest" : { "cmdType" : "C", "ids" : [ { "$numberInt" : "42009" } ] } }
```

提交是必需的。请求通过在当前事务内的普通表中插入行来排队，而处理队列的工作者运行在不同的后端中——在你提交之前，它无法看到该行，因此构建永远不会开始。不自动提交的客户端（`psycopg`、JDBC）必须在此处显式提交。

**索引尚不可用。** 步骤 2 —— 将整个 `requests` 文档传递给 `check_build_index_status`，每次尝试之间提交，并在 `ok` 时停止：

```sql
SELECT ok, complete, retval FROM documentdb_api_internal.check_build_index_status(
    '{ "indexRequest" : { "cmdType" : "C", "ids" : [ { "$numberInt" : "42009" } ] } }'::documentdb_core.bson
);
```

**先检查 `ok`，再检查 `complete`。** 构建失败时也会报告 `complete = true`，同时返回 `ok = false`，原因位于 `retval`。请求不再位于队列中时也会报告完成：实现将“不在队列中”视为成功，因此删除索引时会特意保留对应的队列记录。只根据 `complete` 退出循环，会把因死锁失败的构建误报为成功。应持续轮询，直到 `ok` 为假（失败），或 `complete` 为真且 `ok` 仍为真（成功）；重要场景还应通过 `listIndexes` 确认。

在每次尝试之间提交的原因与步骤 1 相同，此外，保持事务打开会阻塞工作者正在尝试运行的 `CREATE INDEX CONCURRENTLY`。上游测试套件将所有这些封装在一个轮询过程 `documentdb_test_helpers.create_indexes_background` 中，值得作为参考实现阅读。

还有两个行为容易被忽略：

- **格式错误的索引规范不会引发 SQL 错误。** `create_indexes_background` 返回 `ok = false`，原因在 `retval` 中，`requests` 为空，因此仅监控异常的脚本会将被拒绝的构建误报为成功。（`NULL` 规范或只读服务器会引发异常。）
- **必须有执行者处理队列。** 默认情况下，这是一个由 `documentdb_api_internal.schedule_background_index_build_jobs` 调度的 pg_cron 作业运行 `documentdb_api_internal.build_index_concurrently`；设置 `documentdb.indexBuildsScheduledOnBgWorker` 会将工作移至后台工作者。如果两者均未运行——例如当 `cron.use_background_workers` 为 `off` 且 pg_cron 无法通过经过安全加固的 `pg_hba.conf` 所规定的认证时——已排队的构建永远不会启动，任何轮询完成状态的请求（包括网关）都会无限期等待。

## 诊断与管理命令 {#diagnostic-and-administration-commands}

支持诊断和管理线协议命令的函数。

| 函数 | 描述 |
| --- | --- |
| `documentdb_api.coll_stats(p_database_name text, p_collection_name text, p_scale float8 DEFAULT 1)` | 返回集合（`collStats`）的存储和索引统计信息。 |
| `documentdb_api.db_stats(p_database_name text, p_scale float8 DEFAULT 1, p_freestorage bool DEFAULT false)` | 返回数据库（`dbStats`）的存储统计信息。 |
| `documentdb_api.validate(database text, validateSpec bson, OUT document bson)` | 验证集合的索引（`validate`）。 |
| `documentdb_api.connection_status(p_spec bson)` | 返回当前连接的认证和角色信息（`connectionStatus`）。 |
| `documentdb_api.kill_op(p_command_spec bson)` | 通过操作 ID 取消正在运行的操作（`killOp`）。 |
| `documentdb_api.current_op_command(p_spec bson, OUT document bson)` | 实现 `currentOp` 线协议命令。`$currentOp` 聚合流水线阶段使用内部的 `documentdb_api_internal.current_op_aggregation(p_spec bson, OUT document bson)` 返回集合的辅助函数。 |
{.fields}

## 用户管理 {#user-management}

用于创建、更新和管理数据库用户的函数。由线协议 `createUser`、`dropUser`、`updateUser` 和 `usersInfo` 命令支持。

| 函数 | 描述 |
| --- | --- |
| `documentdb_api.create_user(p_spec bson)` | 创建新用户。 |
| `documentdb_api.drop_user(p_spec bson)` | 删除现有用户。 |
| `documentdb_api.update_user(p_spec bson)` | 更新现有用户（密码、角色等）。 |
| `documentdb_api.users_info(p_spec bson)` | 返回一个或多个用户的详细信息。 |
{.fields}

## 角色管理 {#role-management}

用于自定义角色的函数。由线协议 `createRole`、`dropRole`、`rolesInfo` 和 `updateRole` 命令支持。

`create_role`、`drop_role` 和 `roles_info` 受 `documentdb.enableRoleCrud` 控制，该参数默认关闭。因此，在默认构建中，它们会在执行任何工作之前报错 "The CreateRole command is currently unsupported." 或相应错误。开启后，`create_role` 会创建角色，向其授予父角色，并在 `documentdb_api_catalog.roles` 表中记录该角色。非空的 `privileges` 数组会报错 "Privileges on a collection are currently unsupported."，因此自定义角色只能继承内置角色。`documentdb.enableRolesAdminDBCheck` 开启时（默认状态），无论通过 SQL 还是线协议调用，角色函数都要求参数文档包含 `"$db": "admin"`：缺少时会报错 "The required $db property is missing."，其他数据库也会被拒绝。关闭此检查后，这两个要求都不会强制执行。

| 函数 | 说明 |
| --- | --- |
| `documentdb_api.create_role(p_spec bson)` | 创建自定义角色。 |
| `documentdb_api.drop_role(p_spec bson)` | 删除自定义角色。尝试删除内置角色会报错 "Cannot drop built-in role"；角色未记录在 `documentdb_api_catalog.roles` 中时会报错 "The specified role '...' does not exist."。 |
| `documentdb_api.update_role(p_spec bson)` | 未实现。函数体只有 `ereport(ERROR)`，因此无论参数文档或 `enableRoleCrud` 如何，每次调用都会报错 "UpdateRole command is not supported in preview."。 |
| `documentdb_api.roles_info(p_spec bson)` | 返回一个或多个角色的信息。 |
{.fields}

## 工具函数 {#utility-functions}

| 函数 | 描述 |
| --- | --- |
| `documentdb_api.binary_version()` | 返回 `pg_documentdb` 共享库的运行时二进制版本。 |
| `documentdb_api.binary_extended_version()` | 返回包含构建元数据的扩展二进制版本。 |
{.fields}

## 示例 {#example}

要直接从 `psql` 调用其中任意一个函数：

```sql
SELECT * FROM documentdb_api.insert(
    'mydb',
    '{ "insert": "users", "documents": [ { "name": "alice" } ] }'::documentdb_core.bson
);
```

由于 `insert` 声明了两个 `OUT` 参数，`SELECT *` 会将其作为名为 `p_result` 和 `p_success` 的列返回。若移除 `*`，则它们将合并为单一复合值。

更多完整示例（游标、聚合、分片）请参见 [API 参考](/documentdb/reference/)。
