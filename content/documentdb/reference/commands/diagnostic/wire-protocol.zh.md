---
title: 线协议命令支持与通用字段
description: 与源码关联的 DocumentDB 线协议命令清单、共享选项、兼容性响应以及提供方依赖的命令。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/api-reference/commands/diagnostic/wire-protocol.md
weight: 100
translation_source_sha256: 8eedbad23fd8d67dcbf0744dedf91ee18cf55c8e41574627387628905179077b
translation_review: AI-assisted bilingual review; 2026-11-07
---

本参考文档描述了默认的开源 DocumentDB 网关和后端。受服务器功能或集群版本检查保护的功能在已发布的软件包或你的部署中不一定已启用。自定义网关/后端实现可能暴露不同的行为。

## Shell 与线协议语法 {#shell-and-wire-syntax}

```javascript
db.flights.find({ status: "Delayed" }).batchSize(20).maxTimeMS(5000)
```

示例在有等效选项时优先使用 mongosh 辅助函数。选项说明涵盖底层线协议命令，而非辅助函数的参数名称或返回结构。某些辅助函数使用聚合而非同名命令。当没有等效辅助函数或需要 DocumentDB 特定选项时，使用原始 `runCommand` 或 `adminCommand` 请求。

在原始请求中，应将命令名称置于首位。驱动程序添加 `$db`；Shell 辅助函数将参数转换为命令文档，并可自动添加会话元数据。Shell 方法如 `createIndex()` 不一定对应拼写相同的线协议命令。

## 航空公司示例数据集 {#airline-example-dataset}

示例使用了 [Postgres Pro 演示数据库](https://postgrespro.com/education/demodb) 的小型面向文档改编版本，其发布者以 MIT 许可证分发该数据库。2025 年 9 月 1 日的模式提供了航空公司、航班、航线、机场和机票航段的概念。以下文档和值是原创示例数据，并非从可下载数据库或实时航班信息复制而来。

`bookings` 数据库包含一个 `flights` 集合。每个文档将航班与其航线信息合并，并嵌入其票段，因此示例无需关联查询：

| 文档字段 | 映射 |
| --- | --- |
| `_id` | 航班标识符，对应 `flights.flight_id`。 |
| `route_no`, `departure_airport`, `arrival_airport` | 与航班一同存储的航线信息，遵循源数据的 `timetable` 视图。 |
| `scheduled_departure`, `scheduled_arrival` | 使用 `ISODate()` 创建的 BSON 日期，而非日期字符串。 |
| `status` | 航班状态，如 `Scheduled` 或 `Delayed`。 |
| `segments` | 嵌入的机票航段，包含 `ticket_no`、`fare_conditions` 和 `price`。父文档标识其所属航班。 |
| `delay_minutes`, `seat_capacity`, `route_vector` | 针对示例的特定添加项，用于数值更新、聚合和受控的向量索引；这些并非源数据 `flights` 表的列。 |

机场插入示例使用 `airports` 集合，每个源 `airport_code` 映射为文档的 `_id`。

在空的 `bookings.flights` 集合中运行一次此设置：

```javascript
db = db.getSiblingDB("bookings")
db.flights.insertMany(
  [
    {
      _id: 101, route_no: "PG0101", departure_airport: "SVO", arrival_airport: "LED",
      scheduled_departure: ISODate("2025-09-01T08:00:00Z"),
      scheduled_arrival: ISODate("2025-09-01T09:30:00Z"),
      seat_capacity: 160, delay_minutes: 0, status: "Scheduled",
      segments: [
        { ticket_no: "0005432000101", fare_conditions: "Economy", price: 12000 },
        { ticket_no: "0005432000102", fare_conditions: "Economy", price: 8000 }
      ],
      route_vector: [1, 0, 0]
    },
    {
      _id: 102, route_no: "PG0102", departure_airport: "SVO", arrival_airport: "KZN",
      scheduled_departure: ISODate("2025-09-01T09:00:00Z"),
      scheduled_arrival: ISODate("2025-09-01T10:30:00Z"),
      seat_capacity: 120, delay_minutes: 12, status: "Delayed",
      segments: [{ ticket_no: "0005432000103", fare_conditions: "Business", price: 18000 }],
      route_vector: [0, 1, 0]
    },
    {
      _id: 103, route_no: "PG0103", departure_airport: "LED", arrival_airport: "KZN",
      scheduled_departure: ISODate("2025-09-01T10:00:00Z"),
      scheduled_arrival: ISODate("2025-09-01T12:00:00Z"),
      seat_capacity: 100, delay_minutes: 0, status: "Scheduled",
      segments: [{ ticket_no: "0005432000104", fare_conditions: "Business", price: 10000 }],
      route_vector: [0, 0, 1]
    },
    {
      _id: 104, route_no: "PG0104", departure_airport: "SVO", arrival_airport: "LED",
      scheduled_departure: ISODate("2025-09-01T18:00:00Z"),
      scheduled_arrival: ISODate("2025-09-01T19:30:00Z"),
      seat_capacity: 160, delay_minutes: 5, status: "Delayed",
      segments: [{ ticket_no: "0005432000105", fare_conditions: "Economy", price: 12000 }],
      route_vector: [1, 0, 0]
    }
  ],
  { ordered: true }
)
```

选择 `bookings` 作为集合示例的当前数据库。每次独立的更新或删除操作均从这四个文档开始。其他机场、索引、角色或临时集合的设置将在相关页面中说明。不访问集合的诊断和认证命令无数据集依赖。无需 SQL 导入。

## 常见请求字段 {#common-request-fields}

| 参数 | 描述 |
| --- | --- |
| **`$db`** | (必需) 指定目标逻辑数据库的字符串；由驱动程序提供。 |
| **`maxTimeMS`** | (可选) 指定请求执行预算的毫秒数。`0` 不设置显式超时。后端是否应用语句超时取决于命令执行路径；它并非对兼容处理程序的通用控制。 |
| **`lsid`** | (可选) 指定逻辑会话 ID 的文档，通常为 `{ id: <BSON UUID> }`。用于游标/会话所有权和事务解析。 |
| **`txnNumber`** | (可选) 指定事务/重试序号的 BSON int64。请使用驱动程序的 BSON int64 类型，而非 32 位整数或 double。 |
| **`autocommit`** | (可选) 布尔值，当 `false` 时标识多命令事务。 |
| **`startTransaction`** | (可选) 布尔值，当 `true` 时在首次操作时启动事务。 |
| **`readConcern`** | (可选) 指定读隔离请求的文档或 null；受下述约束限制。 |
| **`comment`** | (可选) 包含 `traceparent` 和可选 `tracestate` 的 JSON 对象字符串。当配置了追踪提供者且上下文有效时，网关将其用作请求的追踪父级。 |
{.fields}

通用元数据在命令执行前处理。个别命令可能施加额外限制；请参阅其参数说明。

多命令事务需要 `lsid` 和 BSON int64 类型的 `txnNumber`，且 `autocommit: false`。仅在首次操作时设置 `startTransaction: true`。后续操作必须使用匹配的会话和事务标识符。

### 读关注级别 {#read-concern}

启用读关注级别验证后，支持的 `level` 字符串包括 `local`、`available`、`majority`、`linearizable` 和 `snapshot`。`snapshot` 为事务选择 PostgreSQL 的可重复读隔离；其他已识别的读关注级别映射到 PostgreSQL 的读已提交快照，为每个语句提供已提交数据的一致视图。

| 参数 | 描述 |
| --- | --- |
| **`level`** | (可选) 指定已识别级别的字符串，或使用 `null` 表示未指定级别。未知或大小写不同的字符串将被拒绝。 |
{.fields}

未知的读关注级别子字段和无效类型将导致失败。禁用验证的旧配置解析更为宽松。

## 路由命令清单 {#routed-command-inventory}

以下清单涵盖具有显式分发器分支的公共命令。认证命令在普通命令执行前处理。

| 命令 | 参考和默认行为 |
| --- | --- |
| `find` | [查询和游标选项](/documentdb/reference/commands/query-and-write/find/)。 |
| `insert` | [批量插入选项](/documentdb/reference/commands/query-and-write/insert/)。 |
| `update` | [命令级与单次更新选项](/documentdb/reference/commands/query-and-write/update/)。 |
| `delete` | [命令级与单次删除选项](/documentdb/reference/commands/query-and-write/delete/)。 |
| `findAndModify` | [原子修改选项](/documentdb/reference/commands/query-and-write/findandmodify/)。 |
| `getMore` | [游标续传](/documentdb/reference/commands/query-and-write/getmore/)。 |
| `killCursors` | [游标终止](/documentdb/reference/commands/query-and-write/killcursors/)。 |
| `aggregate` | [聚合流水线命令选项](/documentdb/reference/commands/aggregation/aggregate/)。 |
| `count` | [计数选项](/documentdb/reference/commands/aggregation/count/)。 |
| `distinct` | [去重选项](/documentdb/reference/commands/aggregation/distinct/)。 |
| `create` | [集合和视图创建](/documentdb/reference/commands/administration/create/)。 |
| `collMod` | [集合、视图和索引修改](/documentdb/reference/commands/administration/collmod/)。 |
| `drop`, `dropDatabase` | [集合和数据库删除](/documentdb/reference/commands/administration/drop/)。 |
| `renameCollection` | [同数据库重命名](/documentdb/reference/commands/administration/renamecollection/)。 |
| `listCollections` | [集合元数据游标](/documentdb/reference/commands/administration/listcollections/)。 |
| `listDatabases` | [数据库列表](/documentdb/reference/commands/administration/listdatabases/)。 |
| `createIndex`, `createIndexes` | [索引创建](/documentdb/reference/commands/indexing/createindexes/)。 |
| `listIndexes` | [索引元数据游标](/documentdb/reference/commands/indexing/listindexes/)。 |
| `dropIndexes` | [索引删除](/documentdb/reference/commands/indexing/dropindexes/)。 |
| `reIndex` | 某些提供方可能支持。重建索引请使用 [`collMod.index.reindex`](/documentdb/reference/commands/administration/collmod/)。 |
| `createSearchIndexes` | 某些提供方可能支持。对于向量索引，请使用 [`createIndexes`](/documentdb/reference/commands/indexing/createindexes/)。 |
| `explain` | [支持的读操作和详细程度](/documentdb/reference/commands/diagnostic/explain/)。 |
| `collStats` | [集合统计信息](/documentdb/reference/commands/diagnostic/collstats/)。 |
| `dbStats` | [数据库统计信息](/documentdb/reference/commands/diagnostic/dbstats/)。 |
| `currentOp` | [操作检查](/documentdb/reference/commands/diagnostic/currentop/)。 |
| `killOp` | [操作取消](/documentdb/reference/commands/diagnostic/killop/)。 |
| `compact` | [维护模式和试运行](/documentdb/reference/commands/diagnostic/compact/)。 |
| `validate` | [集合验证标志](/documentdb/reference/commands/diagnostic/validate/)。 |
| `createUser`, `updateUser`, `dropUser`, `usersInfo`, `grantRolesToUser`, `revokeRolesFromUser` | [受控用户操作](/documentdb/reference/commands/security/user-commands/)。 |
| `createRole`, `dropRole`, `rolesInfo`, `grantRolesToRole`, `revokeRolesFromRole` | [受控角色操作](/documentdb/reference/commands/security/role-commands/)。 |
| `updateRole`, `grantPrivilegesToRole`, `revokePrivilegesFromRole` | [其他依赖部署提供方的角色变更](/documentdb/reference/commands/security/role-commands/#provider-dependent-role-mutations)。 |
| `killSessions` | [会话终止](/documentdb/reference/commands/sessions/session-commands/)。 |
| `commitTransaction`, `abortTransaction` | [事务命令](/documentdb/reference/commands/sessions/transaction-commands/)。 |
| `shardCollection`, `reshardCollection`, `unshardCollection`, `getShardMap` | [分片字段](/documentdb/reference/commands/sharding/sharding-commands/)。 |
| `enableSharding` | [无操作数据库分片标记](/documentdb/reference/commands/sharding/sharding-commands/#other-sharding-commands)。 |
| `balancerStart`, `balancerStatus`, `balancerStop`, `listShards`, `moveCollection` | [某些提供方可能支持](/documentdb/reference/commands/sharding/sharding-commands/#other-sharding-commands)。 |

线协议别名中，名称解析器显式识别的有：`buildinfo` 对应 `buildInfo`，`dbstats` 对应 `dbStats`，`findandmodify` 对应 `findAndModify`，`ismaster` 对应 `isMaster`，`reindex` 对应 `reIndex`，`dbhash` 对应 `dbHash`。仅后端使用的拼写不会自动成为可用的网关别名。

## SDK 和驱动程序命令 {#sdk-and-driver-commands}

这些命令主要用于 SDK 和驱动程序的握手、兼容性检查以及会话清理。

| 命令 | 参考和默认行为 |
| --- | --- |
| `hello`, `isMaster` | [握手字段](/documentdb/reference/commands/diagnostic/hello/)。 |
| `ping`, `buildInfo`, `getCmdLineOpts`, `getLog`, `hostInfo`, `isdbgrid`, `whatsmyuri`, `getDefaultRWConcern` | [兼容性响应及其限制](/documentdb/reference/commands/diagnostic/compatibility/)。 |
| `endSessions` | [会话清理](/documentdb/reference/commands/sessions/session-commands/)。 |

## 其他依赖部署提供方的命令 {#additional-provider-dependent-commands}

以下 127 个额外的命令名称由请求类型解析器识别。其具体实现和选项支持取决于提供方。一个被识别或声明的名称本身并不保证该命令可用。

### 管理、查询和遗留命令 {#administrative-query-and-legacy-commands}

`appendOplogNote`, `applyOps`, `authSchemaUpgrade`, `authenticate`, `availableQueryOptions`, `checkShardingIndex`, `cleanupOrphaned`, `clone`, `cloneCollection`, `cloneCollectionAsCapped`, `connPoolStats`, `connPoolSync`, `convertToCapped`, `copydb`, `copydbgetnonce`, `copydbsaslstart`, `createUniqueOrCompoundIndexOnNestedPath`, `currentOpCtx`, `customAction`, `dataSize`, `dbHash`, `diagLogging`, `driverOIDTest`, `dropAllRolesFromDatabase`, `dropAllUsersFromDatabase`, `eval`, `features`, `filemd5`, `forceerror`, `fsync`, `fsyncUnlock`, `geoNear`, `geoSearch`, `getDatabaseVersion`, `getDiagnosticData`, `getFreeMonitoringStatus`, `getLastError`, `getLastRequestStatistics`, `getNonce`, `getPrevError`, `getShardVersion`, `group`, `handshake`, `invalidateUserCache`, `lockInfo`, `logRotate`, `mapReduce`, `mapreduce.shardedfinish`, `mergeChunks`, `moveChunk`, `parallelCollectionScan`, `planCacheListPlans`, `planCacheListQueryShapes`, `profile`, `reSync`, `refreshSessionsInternal`, `repairCursor`, `repairDatabase`, `resetError`, `setFeatureCompatibilityVersion`, `setFreeMonitoring`, `setParameter`, `setShardVersion`, `shardConnPoolStats`, `shardingState`, `shutdown`, `splitChunk`, `splitVector`, `startSession`, `top`, `touch`, `unsetSharding`, 和 `writebacklisten`。

`getnonce` 由 `listCommands` 宣告，但名称解析器识别的是 `getNonce`。请检查提供方的命令拼写和可用性。

### 副本集命令 {#replica-set-commands}

`replSetAbortPrimaryCatchUp`, `replSetDeclareElectionWinner`, `replSetElect`, `replSetFreeze`, `replSetFresh`, `replSetGetConfig`, `replSetGetRBID`, `replSetGetStatus`, `replSetHeartbeat`, `replSetInitiate`, `replSetMaintenance`, `replSetReconfig`, `replSetRequestVotes`, `replSetResizeOplog`, `replSetStepDown`, `replSetStepUp`, `replSetSyncFrom`, 和 `replSetUpdatePosition`。

### 内部协议命令 {#internal-protocol-commands}

`_cloneCatalogData`, `_cloneCollectionOptionsFromPrimaryShard`, `_configsvrAddShard`, `_configsvrAddShardToZone`, `_configsvrBalancerStart`, `_configsvrBalancerStatus`, `_configsvrBalancerStop`, `_configsvrCommitChunkMerge`, `_configsvrCommitChunkMigration`, `_configsvrCommitChunkSplit`, `_configsvrCommitMovePrimary`, `_configsvrCreateCollection`, `_configsvrCreateDatabase`, `_configsvrDropCollection`, `_configsvrDropDatabase`, `_configsvrEnableSharding`, `_configsvrMoveChunk`, `_configsvrMovePrimary`, `_configsvrRemoveShard`, `_configsvrRemoveShardFromZone`, `_configsvrShardCollection`, `_configsvrUpdateZoneKeyRange`, `_flushDatabaseCacheUpdates`, `_flushRoutingTableCacheUpdates`, `_getNextSessionMods`, `_getUserCacheGeneration`, `_isSelf`, `_mergeAuthzCollections`, `_migrateClone`, `_movePrimary`, `_recvChunkAbort`, `_recvChunkCommit`, `_recvChunkStart`, `_recvChunkStatus`, `_shardsvrShardCollection`, 和 `_transferMods`。

命令的可用性需要同时具备名称识别和可执行的实现。请检查你的提供方支持的命令。

## 源码关联 {#source-correlation}

命令页面中提到的所有源码路径均对应上文所列的修订版本。网关路径相对于 `pg_documentdb_gw/documentdb_gateway_core/src/` 而言。

| 源码 | 用于验证 |
| --- | --- |
| [网关分发](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb_gw/documentdb_gateway_core/src/processor/process.rs) 和 [命令名称解析](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb_gw/documentdb_gateway_core/src/requests/request_type.rs) | 命令分发、已识别名称和别名。 |
| [默认 PostgreSQL 适配器](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb_gw/documentdb_gateway_core/src/postgres/documentdb_data_client.rs) | 转发至后端实现和提供方依赖的命令入口点的字段。 |
| [共享请求解析](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb_gw/documentdb_gateway_core/src/requests/common_fields.rs) | 会话、事务、超时、读关注和注解元数据。 |
| [通用后端字段](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb/src/commands/commands_common.c) | 共享选项的回退解析。 |
| [读取解析器](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb/src/aggregation/bson_aggregation_pipeline.c) 和 [元数据查询解析器](https://github.com/documentdb/documentdb/blob/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb/src/aggregation/bson_aggregation_metadata_queries.c) | 读取和元数据命令字段、类型和功能开关。 |
| [后端命令实现](https://github.com/documentdb/documentdb/tree/f027bf1b2fc5ac1e83bfccf97ecc50b69835c758/pg_documentdb/src/commands) | 写入、索引、管理、诊断、用户和角色解析器。 |

范围仅限顶层线协议命令及其选项文档，而非对每个聚合阶段、表达式运算符、PostgreSQL API 或部署特定扩展的全新审计。
