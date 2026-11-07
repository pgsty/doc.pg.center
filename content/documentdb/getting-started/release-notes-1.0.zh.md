---
title: DocumentDB 1.0 发布说明
description: DocumentDB 1.0 的新功能、获取方式、从 0.117 升级方法，以及随版本发布的已知问题。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/getting-started/release-notes-1.0.md
weight: 80
translation_source_sha256: 9d3cf7a937102326000ef130fdaa5e7694bc4bb3356b00394e9de8a2ef4c0709
translation_review: AI-assisted bilingual review; 2026-11-07
---

[DocumentDB v1.0-0](https://github.com/documentdb/documentdb/releases/tag/v1.0-0) 于 **2026-10-19** 发布。它基于与第二个发布候选版本 v1.0-RC2 相同的提交。[变更日志](https://github.com/documentdb/documentdb/blob/v1.0-0/CHANGELOG.md) 列出了引擎的变更内容。

## 获取方式 {#where-to-get-it}

| 通道 | 1.0 版本 | 平台 |
| --- | --- | --- |
| [Linux 软件包](/documentdb/getting-started/prebuilt-packages/) | 软件包 `1.0.0`，扩展 `1.0-0` | Ubuntu 24.04 和 RHEL 兼容版本 9，PostgreSQL 17 和 18，amd64 和 arm64 |
| [容器镜像](/documentdb/documentdb-local/) | `pg15-1.0.0` 至 `pg18-1.0.0`；`latest` 为 `pg17-1.0.0` | Linux amd64 和 arm64 |
| [Kubernetes Operator](/documentdb/kubernetes-operator/) | Operator `1.0.0`，运行引擎 `1.0-0` | Kubernetes 1.33+ 且启用了 `ImageVolume` 特性门控（从 1.35 开始默认开启，1.36 GA） |

SQL 扩展版本在所有位置均为 `1.0-0`，`hello` 在 `internal.documentdb_versions` 中报告该版本。

<span id="what-s-new-since-0-117"></span>

## 相较于 0.117 的新功能 {#whats-new-since-0117}

- **容器镜像中的使用情况遥测。** `documentdb-local` 镜像在启动和每小时向 Scarf 报告其版本、平台和 CPU 架构，该功能默认开启。原生软件包不发送任何信息。请参阅 [使用情况遥测](/documentdb/documentdb-local/#usage-telemetry) 以关闭此功能。
- **安全修复。** `find` 和 `aggregate` 在使用 `batchSize: 0` 时现在会检查调用者是否可读集合。`$merge` 和 `$out` 现在需要对目标集合具有插入或更新权限，而不仅仅是读取权限。`createUser` 和 `updateUser` 拒绝未通过 SASLprep 检查的密码。
- **排序规则** 现在与 `count` 和 `$stdDevPop`、`$stdDevSamp`、`$median` 及 `$percentile` 累加器兼容，并适用于符号类型。排序规则仍默认关闭；请参阅 [已知问题](#known-issues)。
- **自定义角色。** 启用 `documentdb.enableRoleCrud`（默认关闭）后，`createRole` 和 `dropRole` 会在角色目录中维护自定义角色。`updateRole` 仍不支持。
- **`compact`** 将 `bytesFreed` 报告为磁盘上大小的实际变化量。
- **网关。** 网关默认运行在新的 v2 运行时上。现在在后端连接或连接池失败时返回可重试或特定错误码，而非 `InternalError`；当 PostgreSQL 在启动时不可达时，网关会以错误退出，而不是触发 panic。
- **崩溃与正确性修复**，包括系统变量上的 `$getField`/`$setField`/`$unsetField`，无排序时的 `$firstN`/`$lastN`，`$facet` 内部的 `$documents`，`$near`/`$geoNear` 在 `2dsphere` 索引上的排序，并发执行 `dropIndexes` 时的死锁，以及多个 RUM 索引扫描和清理修复。
- **容器行为。** `--init-data-path` 脚本中的错误现在会停止容器。当卷的锁显示为 1.0 容器写入时，过期的 `postmaster.pid` 仅在下次启动时移除；否则容器拒绝启动。如果容器内的 PostgreSQL 停止运行，容器将退出。TOAST 压缩默认设置为 `lz4`，`--disable-extended-rum` 已弃用且被忽略。请参阅 [容器生命周期](/documentdb/documentdb-local/#container-lifecycle)。
- **软件包。** 设置向导设置 `default_toast_compression = 'lz4'`；通过 `sudo` 传递 `DOCUMENTDB_TOAST_COMPRESSION=pglz` 或 `default`，以保留其他设置。

## 升级 {#upgrading}

- **软件包：** 0.116 和 0.117 的安装可直接升级：升级软件包，重启 PostgreSQL 以加载新库，然后更新扩展。请参阅 [升级](/documentdb/linux-packages/#upgrading)。
- **容器：** 1.0 镜像在现有卷上不会更新扩展。请使用 `mongodump` 和 `mongorestore` 将数据移至新卷。请参阅 [升级镜像](/documentdb/documentdb-local/#upgrading-the-image)。
- **发布候选版本：** 不支持升级运行过 RC 的主机和卷。请在全新主机或新卷上启动 1.0。

## 已知问题 {#known-issues}

- **设置过程创建的管理员无法创建或删除用户或角色**（[#752](https://github.com/documentdb/documentdb/issues/752)）。以设置过程或容器创建的管理员用户执行 `createUser`，或在启用 `documentdb.enableRoleCrud` 后执行 `createRole`，都会失败并报错 `User is not authorized to perform this action`。使用软件包安装时，请改为在主机上管理用户：

  ```bash
  printf 'Password for app: '; IFS= read -r -s APP_PASSWORD; echo
  printf '%s' "$APP_PASSWORD" | sudo documentdb-gateway-admin create-user --username app \
    --password-stdin --roles '[{"role":"readAnyDatabase","db":"admin"}]'
  sudo documentdb-gateway-admin drop-user --username app
  ```

- **在分组视图上使用 `distinct` 或 `count` 可能导致服务器崩溃。** 在聚合流水线以 `$group` 结尾且包含累加器（如 `$sum`）的视图上使用 `distinct`，或在该类视图上执行包含查询的 `count`，会导致 PostgreSQL 后端崩溃。PostgreSQL 重启并断开所有其他会话。
- **较新的容器镜像不会升级现有卷** ([#773](https://github.com/documentdb/documentdb/issues/773))。镜像从未运行 `ALTER EXTENSION ... UPDATE`，且对现有卷中更改的 `--password` 被忽略。
- **1.0 版本的容器可能拒绝使用旧容器所用的卷。** 如果卷中仍存在旧容器的 `postmaster.pid`，1.0 镜像会报告该文件存在并拒绝启动。请先停止旧容器：对于 0.116 和 0.117 版本，`docker stop` 会移除该文件。0.114 及更早版本的镜像通常不会干净地停止 PostgreSQL，通常会留下该文件。一旦没有其他进程使用该卷，使用 `-e DOCUMENTDB_FORCE_REMOVE_STALE_POSTMASTER_PID=true` 重新创建容器，然后再重新创建一次，但不带该变量，因为该变量在每次启动时都会跳过使用中检查。
- **单文档更新可能遗漏匹配项。** 使用 `multi: false` 或 `findAndModify` 的更新，若其过滤条件使用了除 `_id` 以外的字段，在 PostgreSQL 以通用计划执行时可能报告无匹配项；随后使用 `upsert` 会插入重复文档。在默认设置下这种情况较为罕见；在 PostgreSQL 配置中设置 `plan_cache_mode = force_custom_plan` 可避免该问题。
- **开销很大的 `$replaceAll` 或 `$regexFindAll` 调用可能超过 `maxTimeMS` 时限。** 对大字符串执行开销很大的调用可能在 `maxTimeMS` 过期后仍持续运行，且无法取消。
- **写操作可能被重复应用** ([#767](https://github.com/documentdb/documentdb/issues/767))。如果后端连接在写操作提交后但在回复前断开，网关会重试该操作，因此即使设置了 `retryWrites=false`，非幂等更新（如 `$inc`）仍可能被应用两次。
- **`$lookup` 在具有通配符索引的集合上可能失败** ([#769](https://github.com/documentdb/documentdb/issues/769))，出现 `Unrecognized BSON data type code 0`。
- **排序规则默认关闭。** `find`、`aggregate`、`count` 和 `delete` 与 `collation` 一起使用时，若未开启 `documentdb_core.enableCollation`，会因不支持而失败。`distinct`、`findAndModify` 和 `update` 完全不支持 `collation`。
- **容器日志中的无害错误。** 健康检查每约 30 秒记录一次 `FATAL: database "documentdb" does not exist`，启动日志中记录一次 `Failed to accept a TCP connection (IPv6)` 错误。两者均不影响服务器。
- **不起作用的容器选项。** `--log-level` 和 `--enable-telemetry` 会被验证但无任何效果，而包含空格的 `--data-path` 会失败。
- **尚未解决的打包与容器问题：**
  - [#771](https://github.com/documentdb/documentdb/issues/771)：包移除、清除、升级和重新运行路径可能导致堆栈停止或卡住。
  - [#759](https://github.com/documentdb/documentdb/issues/759)：容器初始化、运行时和快速启动路径存在缺口。
  - [#758](https://github.com/documentdb/documentdb/issues/758)：容器设置默认不安全。
  - [#735](https://github.com/documentdb/documentdb/issues/735)：在 RPM 卸载并重新安装后，网关状态所有权未被保留。
  - [#685](https://github.com/documentdb/documentdb/issues/685)：`--password` 参数在容器进程列表中可被读取；应改用 `-e PASSWORD`。
  - [#389](https://github.com/documentdb/documentdb/issues/389)：Debian 包缺少版权文件。

## 报告问题 {#report-issues}

在 [documentdb/documentdb](https://github.com/documentdb/documentdb/issues) 中提交问题，提供 DocumentDB 和 PostgreSQL 版本，以及软件包版本或 `docker logs` 输出中的 `Release Version` 行。
