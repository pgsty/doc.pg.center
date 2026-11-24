---
type: docs
upstream_link: ""
search_keywords: ["SET NAMES", "caching_sha2_password", "mysql_native_password", "mysql_clear_password", "SCRAM", "pg_hba.conf", "mysql.port", "mysql.database", "mysql.max_allowed_packet", "mysql.require_secure_transport", "shared_preload_libraries", "flush_auth_cache", "database_compatibility_mode", "halo_mysql_password_encryption", "旧配置"]
title: 构建与配置
description: 编译配套的 OpenHalo 18 内核与 aux_mysql 二进制、初始化实例、配置认证与 TLS，以及管理 mysql.* GUC 参数。
weight: 40
---

本页说明仅适用于 **[PGSTY OpenHalo 18 分支](/openhalo/18/)**，不适用于历史 PG14 openHalo 或商业 Halo Database 1.0.16。部署前请核对确切源码提交或扩展版本：源码标签 `v18.6.1`（`2627e6f`，已纳入验收通过提交 `6a93e8f`）搭载 `aux_mysql 1.9`，而早期标签 `v18.6`（`60e7a22`）搭载 `aux_mysql 1.5`，且 `18.6.1` 多平台二进制安装包仍待完成包级验收。

## 编译配套的内核与扩展 {#build}

OpenHalo 18 使用 **GNU make**（源码树内或 VPATH 树外构建）或针对匹配 OpenHalo 18 头文件的 PGXS 路径编译。**不支持 Meson**，执行 Meson 配置会立即显式报错退出，防止产出残缺安装。顶层执行 `make && make install` 会同时编译并安装 PostgreSQL 18.6 内核与 `contrib/aux_mysql`；原生 PostgreSQL 18 二进制无法加载 `aux_mysql`。

在 Enterprise Linux 9 / 10 环境下安装构建工具链与依赖库：

```sh
sudo dnf install -y gcc make bison flex perl readline-devel zlib-devel libicu-devel openssl-devel
```

- **ICU（`libicu-devel`）** 为必需依赖。
- **OpenSSL（`openssl-devel`）** 强烈建议启用：它提供 TLS 连接以及 `caching_sha2_password` 所需的 RSA-OAEP 公钥密码交换。若未启用 `--with-openssl`，MySQL 协议密码登录将只能依赖明文 `mysql_clear_password`。
- 在精简的 EL10 容器中构建和初始化测试实例前，请确认已安装 `bison`、`perl-FindBin` 及 `openssl` 命令行工具。

在干净、已核验身份的源码树（例如源码标签 `v18.6.1` 即 `2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`，或固定验收提交 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`）中执行：

```sh
./configure --prefix=/opt/openhalo18 --with-openssl --enable-depend
make -j"$(nproc)"
sudo make install
```

用于调试验收的构建额外加上 `--enable-debug --enable-cassert`，并使用独立的构建目录与安装前缀 `--prefix`。涉及节点或回调头文件变更时务必开启 `--enable-depend`（或清理重编）：严禁把新编译的 `aux_mysql.so` 链接到陈旧内核目标文件，所有第三方扩展也必须基于同一套 OpenHalo 18 头文件重新编译并独立验证。

## 初始化实例与安装 aux_mysql {#initialize}

使用非特权操作系统服务账户（如 `postgres`）执行 `initdb` 与 `pg_ctl`，切勿使用 `root`：

```sh
sudo install -d -o postgres -g postgres /var/lib/openhalo18
sudo -iu postgres /opt/openhalo18/bin/initdb -D /var/lib/openhalo18/data
```

OpenHalo 18 生成的 `postgresql.conf.sample` 默认已预加载 `aux_mysql` 并开启 MySQL 监听。启动前检查 `/var/lib/openhalo18/data/postgresql.conf`：

```ini
listen_addresses = 'localhost'
port = 5432
unix_socket_directories = '/tmp'
shared_preload_libraries = 'aux_mysql'
mysql.listener_on = on
mysql.port = 3306
mysql.database = 'postgres'
mysql.halo_mysql_version = '5.7.32-log'
```

在 `shared_preload_libraries` 中保留 `aux_mysql` 及其他需要预加载的扩展（未通过 `shared_preload_libraries` 预加载而动态加载 `aux_mysql` 会直接报错）。启动实例后，建议通过 PostgreSQL 连接在 `mysql.database` 中显式创建扩展：

```sh
sudo -iu postgres /opt/openhalo18/bin/pg_ctl \
  -D /var/lib/openhalo18/data -l /var/lib/openhalo18/server.log start
sudo -iu postgres /opt/openhalo18/bin/psql -X -h /tmp -d postgres \
  -c 'CREATE EXTENSION aux_mysql;'
```

若目标数据目录中已存在旧版 `aux_mysql`，请检查 `extversion` 并执行[就地 `ALTER EXTENSION` 升级](/openhalo/18/migration/#upgrade)——切勿在有业务表的数据库中执行 `DROP EXTENSION aux_mysql CASCADE`。

**自动创建扩展与显式安装的规则：**

- `mysql.auto_create_extension = on`（默认）时，首次通过 MySQL 协议登录的**超级用户**会在握手完成前同步执行 `CREATE EXTENSION IF NOT EXISTS aux_mysql`。
- 仅启动数据库或仅通过 PostgreSQL 端口（`5432`）连接，**不会**自动创建任何扩展 SQL 对象。
- 普通业务账号在扩展尚未安装时无法自动触发安装，连接会报错并提示先由超级用户安装。
- 流复制备库与 `pg_upgrade` 期间自动安装会被自动禁用。若主动执行 `DROP EXTENSION` 后不希望下次超级用户 MySQL 连接重新装回，需设置 `mysql.auto_create_extension = off` 并重启。
- 由于 `aux_mysql` 会在 `mysql.database`（默认 `postgres`）内注册数据库级布尔赋值转换，无关的原生 PostgreSQL 应用宜放在**未安装 `aux_mysql` 的其他 PostgreSQL 数据库**中。

## 认证、TLS 与客户端连接 {#authentication}

MySQL 协议与 PostgreSQL 协议共用同一套 PostgreSQL 角色（`pg_authid`）、SCRAM-SHA-256 / MD5 密码校验信息与 `pg_hba.conf` 规则：同一个密码可同时登录 `5432` 与 `3306`。

通过管理员 `psql` 创建最小权限应用账号及同名业务模式：

```sql
CREATE ROLE app LOGIN;
\password app
GRANT CONNECT ON DATABASE postgres TO app;
CREATE SCHEMA app AUTHORIZATION app;
```

也可在超级用户 MySQL 会话中执行 `CREATE USER app IDENTIFIED BY '...';` 再按需授予模式权限。

在 `pg_hba.conf` 中添加匹配规则时，数据库列必须填写**承载模式的 PostgreSQL 数据库名**（`mysql.database = 'postgres'` 时填 `postgres`，**而不是** MySQL 模式名 `app`）：

```text
host    postgres    app    127.0.0.1/32    scram-sha-256
```

`pg_hba.conf` 按首条命中生效，修改后执行 `pg_ctl reload` 生效。`3306` 端口仅支持 `scram-sha-256`、`md5`、`password`、`trust`、`reject` 五种 `pg_hba.conf` 认证方法——其余方法（`peer`、`ident`、`cert`、`gss`、`ldap`、`pam` 等）均返回 `1045`（`28000`），且当规则为 `scram-sha-256` 时会拒绝仍存储 `md5` 密钥的角色。如需强制 MySQL 连接使用 TLS，请在 `postgresql.conf` 中设置 `ssl = on` 并在 `pg_hba.conf` 中使用 `hostssl` 规则（不存在 `mysql.require_secure_transport` 参数）。开放远程连接还需调整 `listen_addresses`（或 `mysql.listen_addresses`）、重启实例，并收紧客户端网段与防火墙策略。随后即可使用标准 MySQL 客户端登录：

```sh
mysql --host=127.0.0.1 --port=3306 --user=app --password --database=app
```

**`caching_sha2_password` 与 `mysql_clear_password` 工作机制：**

- **`caching_sha2_password`（默认）**：由于 PostgreSQL 存储的是 SCRAM/MD5 校验串，既无法离线推导出 MySQL 的 `SHA256(SHA256(password))`（stage2 摘要），也无法推导出 `mysql_native_password` 所需的 `SHA1(SHA1(password))`（因此不支持 `mysql_native_password` 挑战-响应），每个用户在实例启动后（或缓存淘汰后）的**首次登录**会走完整认证路径——通过 TLS（`ssl = on` / `hostssl`）或使用服务端自动生成的 RSA 密钥对（数据目录下的 `mysql_rsa_private_key.pem`）做 RSA-OAEP 加密传输，与 `pg_authid` 校验通过后将 `(stage2, sha256(rolpassword))` 写入共享内存；后续连接直接命中快速挑战-响应路径。
- **缓存自动失效与手动清空**：执行 `ALTER ROLE ... PASSWORD` 或 `\password` 修改密码后，`rolpassword` 摘要立即变化，旧缓存自动失效而无需重启。超级用户也可执行 `SELECT mysql.flush_auth_cache();` 手动清空全部快速认证缓存。
- **旧驱动与 `mysql_clear_password`**：Connector/J `8.4`、`go-sql-driver/mysql` `1.9`、PyMySQL 及 MySQL 8+ 命令行原生支持 `caching_sha2_password`。当设置 `mysql.default_authentication_plugin = 'mysql_clear_password'` 时，初始握手包通告 `mysql_native_password` 并立即由服务端下发 `AuthSwitchRequest`（`0xfe`）切换至 `mysql_clear_password`，从而使旧版 MySQL 5.7 客户端或驱动（例如验收实测通过的 Connector/J `5.1.49`，配合 TLS、客户端明文插件开关与 `connectionCollation=utf8mb4_general_ci`）顺利完成认证；启用 `mysql_clear_password` 时请务必配合 `hostssl`。

## 参数参考 {#parameters}

| 参数 | 默认值 | PG 上下文 | 取值范围与运行影响 |
| --- | --- | --- | --- |
| `mysql.listener_on` | `on` | `postmaster`（需重启） | 启动时启用或关闭 MySQL TCP 监听器。 |
| `mysql.port` | `3306` | `postmaster`（需重启） | MySQL TCP 监听端口（`0..65535`）；设为 `0` 关闭监听。不创建 MySQL Unix 套接字。 |
| `mysql.listen_addresses` | 继承 `listen_addresses` | `postmaster`（需重启） | MySQL 监听绑定地址列表；未设置时跟随 PostgreSQL `listen_addresses`。 |
| `mysql.database` | `'postgres'` | `sighup`（重载生效） | 新建 MySQL 连接接入的 PostgreSQL 数据库，MySQL 的各个数据库均为其中的模式。放行普通用户前须先建库并安装 `aux_mysql`。 |
| `mysql.auto_create_extension` | `on` | `postmaster`（需重启） | 首次超级用户 MySQL 连接时同步执行 `CREATE EXTENSION IF NOT EXISTS aux_mysql`（备库与 `pg_upgrade` 期间自动禁用）。 |
| `mysql.halo_mysql_version` | `'5.7.32-log'` | `sighup`（重载生效） | 用于握手、`VERSION()` 与 `@@version`；决定握手字符集编号（低于 `8.0` 报 `45`，`8.0+` 报 `255`）及 `/*!NNNNN ... */` 可执行注释版本门槛。**不代表**已安装的 `aux_mysql` 版本。 |
| `mysql.default_authentication_plugin` | `'caching_sha2_password'` | `sighup`（重载生效） | 向新建 MySQL 连接通告的认证插件：`caching_sha2_password` 或 `mysql_clear_password`。 |
| `mysql.auth_cache_size` | `1024` | `postmaster`（需重启） | `caching_sha2_password` 共享内存快速认证缓存容量（`0..1000000`）；`0` 禁用缓存，每次登录均走完整 TLS/RSA 认证。 |
| `mysql.rsa_private_key_file` | `'mysql_rsa_private_key.pem'` | `postmaster`（需重启） | 非 TLS 连接用于 `caching_sha2_password` 公钥交换的 RSA 私钥路径（相对 `$PGDATA`），文件缺失时启动自动生成。 |
| `mysql.max_allowed_packet` | `67108864`（`64 MiB`） | `sighup`（重载生效） | 入站 MySQL 命令包与累计 `COM_STMT_SEND_LONG_DATA` 数据的字节上限（`1024..1073741823`）。通过 `@@max_allowed_packet` 读取，禁止从 MySQL 会话执行 `SET` 修改。 |
| `mysql.statement_rollback` | `on` | `user`（会话可设） | 在显式事务内用隐藏保存点包裹每条语句，使报错语句仅回滚自身；设为 `off` 时恢复 PostgreSQL 报错中止整笔事务的行为（适合超过 64 条写语句的大事务）。 |
| `mysql.default_collation` | `'case_insensitive'` | `user`（会话可设） | 未声明列/表 `COLLATE` 的新建字符列使用的 `mysql` 模式排序规则（`1.9` 中 `case_insensitive` 映射为 `utf8mb4_general_ci`）；空串 `''` 使用 PG 数据库默认排序规则。 |
| `mysql.parser` | `'mysql'` | `user`（会话可设） | MySQL 协议连接使用的 SQL 解析方言：`'mysql'` 或 `'postgres'`（兼容隐藏别名 `'postgresql'`）。`5432` 原生 PG 连接始终使用 PostgreSQL SQL。 |
{.wide .expand}

通过 PostgreSQL 连接（`5432`）查询 `pg_settings` 与 `pg_extension`，可核对实时生效值、是否等待重启以及实际安装的 `aux_mysql` SQL 版本：

```sql
SELECT name, setting, context, pending_restart
FROM pg_settings
WHERE name LIKE 'mysql.%'
ORDER BY name;

SELECT extname, extversion
FROM pg_extension
WHERE extname = 'aux_mysql';
```

## 会话初始化与诊断检查 {#session}

通过 MySQL 连接（`3306`）检查会话实际字符集、排序规则、`sql_mode`、隔离级别与告警：

```sql
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';
SELECT @@character_set_client, @@character_set_connection,
       @@character_set_results, @@collation_connection;
SHOW WARNINGS;
SELECT @@sql_mode, @@autocommit, @@transaction_isolation, @@transaction_read_only;
```

执行 `SET NAMES` 后请检查 `SHOW WARNINGS`：例如请求 `SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'` 会成功返回并发出 `1105` 告警，同时将 `@@collation_connection` 设为实际生效的 `'utf8mb4_general_ci'`；而直接执行 `SET collation_connection = 'utf8mb4_unicode_ci'` 仅原样回显字符串且不发告警、不启用对应规则。关于哪些 `sql_mode` 标志与系统变量真正生效、哪些仅回显，请核对[接受的语法设置与实际生效行为](/openhalo/18/compatibility/#accepted-vs-implemented)。

## 不可沿用的旧版与外部产品参数 {#old-settings}

| 参数来源 | 废弃或外部专有参数 | OpenHalo 18 处置方式 |
| --- | --- | --- |
| OpenHalo PG14（`1.0`） | `database_compat_mode`、`standard_parserengine_auxiliary` | **删除。** 由监听端口区分协议，MySQL 连接方言由 `mysql.parser` 控制。 |
| OpenHalo PG14（`1.0`） | `mysql.ci_collation`、`halo_mysql_ci_collation` | **删除。** 大小写敏感性完全由列/表排序规则及 `mysql.default_collation` 决定。 |
| PG18 早期研究版 | `halo_mysql.*` 参数前缀 | **改名**为正式 `mysql.*` 参数（`check_pg14_config.py` 会自动检出）。 |
| `v18.6.1` 前根 README 旧稿 | `mysql.require_secure_transport`、`mysql.explicit_defaults_for_timestamp`、`mysql.table_access_method_Startup`、`mysql.table_access_method_Convert` | **删除（实际不存在的 GUC）。** 强制 TLS 请使用 `ssl = on` 搭配 `pg_hba.conf` 的 `hostssl`；表访问方法请使用 `default_table_access_method` 或 DDL `ENGINE=<am>` / `ENCRYPTION='Y'`。 |
| OpenHalo PG14（`1.0`） | `--with-uuid=ossp` 编译要求、`password_encryption = 'mysql_native_password'` | **删除。** `mysql.uuid()` 已改用内核 `gen_random_uuid()`；角色密码使用标准 PostgreSQL `scram-sha-256`，由 `3306` 的 `caching_sha2_password` 校验。 |
| 商业 Halo 1.0.16 | `cluster_net_services`、`mysql.default_tenant`、`plmyssql`、`hsql -p 1921`、`mysql.on_error_rollback`、`mysql.multi_table_delete_methond`、`mysql.skip_utf8_verify` | **切勿使用。** 属于商业 Halo Database 1.0.16 专有参数，在 `pgsty/openhalo` 中不存在。 |
{.wide .expand}

迁移旧实例配置时，请始终以全新 OpenHalo 18 `initdb` 生成的配置为起点，并先运行 [PG14 配置预检工具](/openhalo/18/migration/#pg14)。
