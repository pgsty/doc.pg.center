---
title: DocumentDB 1.2 发布说明
description: DocumentDB 1.2 的新功能、获取渠道、可能导致现有部署无法启动的容器变更，以及从 1.0 升级的方法。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/getting-started/release-notes-1.2.md
weight: 80
translation_source_sha256: b07e6011f6ad408b0a6ed7b0ea8839a773e5e01088d4181c41ba8c291ead5ca0
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
---

[DocumentDB v1.2-0](https://github.com/documentdb/documentdb/releases/tag/v1.2-0) 于 **2026-11-12** 发布，是 1.0 之后的下一个版本。项目没有发布 1.1，其变更随 1.2 一同发布。[变更日志](https://github.com/documentdb/documentdb/blob/v1.2-0/CHANGELOG.md)列出了引擎变更。

## 获取渠道 {#where-to-get-it}

| 渠道 | 1.2 版本 | 平台 |
| --- | --- | --- |
| [Linux 软件包](/documentdb/getting-started/prebuilt-packages/) | 软件包 `1.2.0`，扩展 `1.2-0` | Ubuntu 24.04 和 RHEL 兼容发行版 9，PostgreSQL 17 和 18，amd64 和 arm64 |
| [容器镜像](/documentdb/documentdb-local/) | `pg15-1.2.0` 至 `pg18-1.2.0`；`latest` 和 `1.2` 指向 `pg17-1.2.0` | Linux amd64 和 arm64 |
| [PGDG APT 仓库](/documentdb/getting-started/prebuilt-packages/#pgdg-extension-packages) | 软件包 `1.2-0-1.pgdg…`，扩展 `1.2-0`（仅含扩展） | Debian 13 和 14、Ubuntu 26.04（包括 amd64 和 arm64）和 26.10（amd64），PostgreSQL 15 至 18 |

SQL 扩展版本为 `1.2-0`，`hello` 在 `internal.documentdb_versions` 中报告该版本。

<span id="what-s-new-since-1-0"></span>

## 相比 1.0 的新增功能 {#whats-new-since-10}

- **排序规则**现已支持 `distinct`、`findAndModify` 和 `update`，包括在多文档更新和 upsert 中为每项更新指定排序规则。显式指定 `simple` 排序规则等同于不指定排序规则。对于使用排序规则的索引，写入和索引读取会拒绝需要截断的值。排序规则支持默认仍关闭；参见[排序规则](/documentdb/postgres-api/configuration/#collation)。
- **用户与角色。** `dropUser` 和 `updateUser` 拒绝长度达到或超过 64 字节的用户名，避免超长名称删除或修改以其前 63 字节为名称的用户（[#734](https://github.com/documentdb/documentdb/issues/734)）。`rolesInfo`、`usersInfo` 和 `connectionStatus` 返回自定义角色元数据；admin 和 root 用户可看到所有自定义角色，其他用户只能看到其继承的角色。
- **`unit: "day"` 的 `$dateTrunc`** 使用 PostgreSQL 的 `date_bin`，使时间分桶严格按日历日划分，与参考日期对齐，并遵循时区边界。超出 PostgreSQL 范围的步长和结果会被拒绝。将 `documentdb.enable_date_trunc_day_with_pg_bin` 设为 `off` 可恢复旧行为。
- **唯一索引。** 降序唯一索引现在会检查 null 值与缺失值的冲突，包括复合键和使用排序规则的索引（由 `documentdb.enable_unique_null_missing_semantics` 控制，默认开启）。
- **`collMod`** 可在键模式和当前名称均匹配时重命名索引。
- **`bson_build_document`** 接受 `timestamptz` 值，并将其写为毫秒精度的 BSON 日期。
- **查询规划。** `$elemMatch` 谓词和 `$lookup` 的内侧使用已收集的统计信息进行估算；没有规划器统计信息的动态游标查询跳过并行计划。默认开启 `$unwind` 之前的字段剪枝，以及多键复合索引上 `$group` 的排序下推。
- **修复**关联 `$lookup` 重新扫描 `$densify` 阶段时的崩溃和错误结果、null 等值条件位于复合索引排序键之间时的排序和分组结果错误，以及索引项较大时 RUM 叶节点分裂可能溢出的问题。
- **网关指标重命名。** 如果导出网关指标，需要将 `db.client.*` 名称改为 `docdb.gateway.*`：例如，`db.client.operations` 改为 `docdb.gateway.operations`，`db.client.operation.duration` 改为 `docdb.gateway.operation.duration`。请更新使用旧名称的仪表盘和告警。新增指标覆盖身份验证尝试、游标、会话和事务。
- **移除的设置。** 移除 `enableSkipDottedFieldIndexTerms` 和 `enable_ordered_operator_scans` 设置，其控制的行为现在始终开启。

## 容器镜像变更 {#container-image-changes}

以下两项变更可能导致现有 `docker run` 命令或 Compose 文件无法启动容器：

- **必须提供密码。** 未设置 `PASSWORD` 或 `--password` 时，容器会在启动时退出，不再使用公开的默认密码创建 admin 用户。短期本地评估可通过 `DOCUMENTDB_ALLOW_DEFAULT_PASSWORD=true` 恢复该默认值。设置 `--create-user false` 时，只有加载数据才需要密码。在已有数据卷上，admin 用户保留创建时使用的密码。
- **`TLS_MODE` 只接受一个值。** 空的 `TLS_MODE` 或 `allowTLS,requireTLS` 之类的列表会被拒绝。

镜像还包含以下变更：

- `--password` 不再留在容器进程列表中。`--password` 和 `PASSWORD` 仍可通过 `docker inspect` 查看。
- `--log-level` 设置网关的日志级别；`quiet` 仍会显示错误。
- 较新的镜像在启动时更新已有数据卷上的扩展。

## 升级 {#upgrading}

- **软件包：** 1.0 安装可原地升级。先升级软件包，再运行 `sudo documentdb-setup --pg-version <major> --yes`；该命令重启 PostgreSQL 一次并更新扩展，同时保留 admin 用户。参见[升级](/documentdb/linux-packages/#upgrading)。
- **容器：** 在 1.0 数据卷上启动 1.2 镜像，启动时会更新扩展。该数据卷不支持回退到 1.0。参见[升级镜像](/documentdb/documentdb-local/#upgrading-the-image)。
- **候选发布版：** 曾运行候选发布版的主机和数据卷没有受支持的升级路径。

## 报告问题 {#report-issues}

请在 [documentdb/documentdb](https://github.com/documentdb/documentdb/issues) 提交问题，注明 DocumentDB 和 PostgreSQL 版本，并提供软件包版本或 `docker logs` 中的 `Release Version` 行。
