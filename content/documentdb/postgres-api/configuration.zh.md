---
title: 配置
description: 用于配置 DocumentDB 1.0 的服务器 GUC 和网关环境变量，包括必需的扩展 RUM 索引库、排序规则和角色管理标志。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/postgres-api/configuration.md
weight: 30
translation_source_sha256: a75b19f7a5f8a77a1df8583f7eea82787c4bbafa852e18657cced00e92b0ba57
translation_review: AI-assisted bilingual review; 2026-11-07
---

DocumentDB 的配置分为两层：PostgreSQL 扩展通过 `postgresql.conf` 中的 GUC 参数配置，网关进程通过环境变量或 JSON 配置文件配置。本页介绍 DocumentDB 1.0 中最常调整的设置。

<span id="extension-gu-cs"></span>

## 扩展 GUC 参数 {#extension-gucs}

`pg_documentdb` 以 `documentdb.` 为前缀，将调优参数和功能开关提供为 PostgreSQL GUC 参数。可以在 `postgresql.conf` 中设置，也可以通过 `SET` 在会话级设置，或通过 `ALTER ROLE ... SET` 在角色/数据库级设置。

### 模式验证 {#schema-validation}

| GUC | 默认值 | 描述 |
| --- | --- | --- |
| `documentdb.enableSchemaValidation` | `on` | 在写入操作上强制执行集合 `$jsonSchema` 的验证器。当 `off` 时，集合的验证器会被存储但不强制执行。 |
{.fields}

对于设置了 `validator` 的集合，当其 `validationLevel` 不是 `off` 且 `validationAction` 为 `error` 时，会在 `insert`、`update`、`findAndModify` 和聚合输出阶段（`$merge`、`$out`）执行验证。（写入路径不会拒绝 `validationAction` 为 `warn` 的设置；写入时指定 `bypassDocumentValidation` 会跳过验证，参见 `documentdb.enableBypassDocumentValidation`。）

### RUM 索引库 {#rum-index-library}

| GUC | 默认值 | 描述 |
| --- | --- | --- |
| `documentdb.rum_library_load_option` | `require_documentdb_extended_rum` | 要求在每个受支持的 PostgreSQL 主版本上都安装 DocumentDB 扩展的 RUM 库（`pg_documentdb_extended_rum`）。在 `postgresql.conf` 中设置，并重启 PostgreSQL 以使更改生效。 |
{.fields}

包安装向导和容器启动会处理所需的扩展设置。对于手动配置的 PostgreSQL 实例，需同时创建 `documentdb` 和 `documentdb_extended_rum`；`CREATE EXTENSION documentdb CASCADE` 不会自动创建 `documentdb_extended_rum`。在创建索引前，请遵循 [包安装指南](/documentdb/getting-started/packages/)。

在包和容器安装中请保持默认值：它们也会设置 `documentdb.alternate_index_handler_name = 'extended_rum'`，而使用 `none` 时索引构建会导致服务器崩溃（且不带上游 `rum` 库的 PostgreSQL 18 镜像无法启动）。在自行构建的服务器上，`none` 会加载上游 `rum` 库，该库必须已安装。`prefer_documentdb_extended_rum` 仅在扩展库加载但缺少其索引处理器时回退到 `rum`；若库本身缺失，PostgreSQL 仍无法启动。

### 非阻塞唯一索引构建 {#non-blocking-unique-index-builds}

| GUC | 默认值 | 说明 |
| --- | --- | --- |
| `documentdb.enableNonBlockingUniqueIndexBuild` | `on` | 使用 `CREATE INDEX CONCURRENTLY` 构建唯一有序索引，再通过后处理注册排他约束、验证现有行，从而避免长时间持有写锁。 |
{.fields}

启用后，在现有集合上创建唯一有序索引，不再会在整个构建期间持续阻塞并发写入。

### 排序规则 {#collation}

| GUC | 默认值 | 描述 |
| --- | --- | --- |
| `documentdb_core.enableCollation` | `off` | 在查询中接受 `collation` 选项。它由 `pg_documentdb_core` 定义，因此使用 `documentdb_core.` 前缀，且可按会话设置。 |
{.fields}

当 `off` 时，`find`、`aggregate` 和 `count` 拒绝 `collation` 选项，提示 "collation is not supported in the find command yet."（或使用 `aggregate` / `count` 替代 `find`）。`delete` 也遵循该标志。`distinct`、`findAndModify` 和 `update` 无论标志是否开启，均拒绝 `collation`。

当该标志开启时，部分聚合阶段仍拒绝排序规则，包括 `$bucket`、`$bucketAuto`、`$densify`、`$fill`、`$geoNear`、`$merge`、`$setWindowFields` 和 `$sortByCount`。

### 默认关闭的功能标志 {#off-by-default-feature-flags}

这些开关控制的功能在关闭时不会生效，也不会给出提示；命令仍然成功，表现为没有预期效果，而不是报错。

| GUC | 默认值 | 说明 |
| --- | --- | --- |
| `documentdb.enableCompactVacuumFull` | `off` | 允许 `compact` 使用 `mode: "full"`，执行阻塞式 `VACUUM FULL`，将空间归还操作系统。为 `off` 时，该模式不执行任何工作，只返回 `{ "ok": 1, "bytesFreed": 0 }`。默认的 `standard` 模式执行普通 `VACUUM`，通常允许并发读写，不受此开关影响。 |
| `documentdb.enablePreImages` | `off` | 允许使用集合选项 `changeStreamPreAndPostImages`。为 `off` 时，`create` 和 `collMod` 会拒绝该选项。 |
| `documentdb.indexBuildsScheduledOnBgWorker` | `off` | 使用 PostgreSQL 后台工作进程处理后台索引构建队列，替代 pg_cron 作业。pg_cron 已配置且正常工作时，应保持 `off`；pg_cron 无法执行该作业时，应开启，否则队列中的索引构建任务永远不会开始。 |
{.fields}

### 角色管理标志 {#role-management-flags}

与上述标志不同，这两个标志会直接抛出错误而非导致效果缺失，因此调用方会立即看到失败。

| GUC | 默认值 | 描述 |
| --- | --- | --- |
| `documentdb.enableRoleCrud` | `off` | 通过数据平面启用自定义角色。当 `on` 时，`createRole` 创建角色并将其记录在 `documentdb_api_catalog.roles` 表中，`dropRole` 仅删除记录在该表中的角色。当 `off` 时，`create_role`、`drop_role` 和 `roles_info` 在执行任何操作前即抛出错误，例如 "The CreateRole command is currently unsupported." `update_role` 无论何种情况均未实现，始终抛出 "UpdateRole command is not supported in preview." |
| `documentdb.enableRolesAdminDBCheck` | `on` | 要求通过线协议角色命令在 `admin` 数据库上执行，否则抛出 "CreateRole must be called from 'admin' database." 用户管理命令由 `documentdb.enableUsersAdminDBCheck` 单独控制，其默认值为 `off`。 |
{.fields}

## 网关配置 {#gateway-configuration}

网关（`pg_documentdb_gw`）从 JSON 配置文件和/或 `DOCUMENTDB_*` 环境变量读取其设置。环境变量会覆盖 JSON 文件，这使得它们在 systemd 管理和容器部署中更为方便。

> [!NOTE]

> 网关服务的软件包包含 systemd 单元及各主版本的 `gateway.env` 文件，作为发布文件提供（`documentdb-gateway`，以及提供单元模板的 `documentdb-common`）。下文的 `DOCUMENTDB_*` 设置适用于这套软件包服务、直接运行的 `documentdb-gateway` 可执行文件（`documentdb-local` 容器镜像会在内部配置它），以及自行安装单元的下游软件包。使用软件包安装时，`documentdb-setup` 会写入 `/etc/documentdb/local/<major>/gateway.env` 中的受管配置块；块外的编辑会保留，但每次重新运行向导都会重建受管块。

| 环境变量 | 用途 |
| --- | --- |
| `DOCUMENTDB_PG_URL_FILE` | 包含 PostgreSQL 连接 URL 的文件路径，在启动时读取。对于包管理安装，URL 中不得包含密码——网关通过本地 Unix 套接字使用 peer/trust 认证连接。 |
| `DOCUMENTDB_LISTEN_ADDR` | 网关监听的地址，格式为 `host:port` 或 `:port`（例如 `:10260`）。 |
| `DOCUMENTDB_TLS_CERT_FILE` | TLS 证书文件路径。 |
| `DOCUMENTDB_TLS_KEY_FILE` | TLS 私钥文件路径。 |
| `DOCUMENTDB_TLS_AUTO_GENERATE` | 当 `true` 时，若未提供证书/密钥文件，则自动创建自签名证书。 |
| `DOCUMENTDB_TLS_STATE_DIR` | 自动创建的证书/密钥写入并重启时重新读取的目录（默认为 `/var/lib/documentdb-gateway/tls`）。当该目录不可写时——如 `documentdb-local` 容器镜像中——网关将回退到 `$HOME/.local/state` 下的用户级状态目录，并记录所选路径。 |
| `DOCUMENTDB_LOG_LEVEL` | 网关追踪订阅者的日志级别（例如 `info`，`debug`）。 |

对于 systemd 管理的安装，这些通常通过单元的 `EnvironmentFile` 设置（例如 `gateway.env`）。

### 连接性检查 {#connectivity-check}

网关二进制文件提供一个 `check` 子命令，用作安装后的连接性探测：

```bash
documentdb-gateway check [--config <path>]
```

该命令连接配置的 PostgreSQL 后端，执行与服务启动流程相同的启动校验，并报告已安装的 `documentdb` 扩展版本。成功时退出码为 `0`，失败时为 `1`，并在标准错误中输出便于阅读的说明和提示，适合用于安装后的冒烟测试和健康检查。
