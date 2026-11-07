---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16；2026-11-07 文档快照"
upstream_notice: /zh/attribution/#halodb
title: 配置 MySQL 兼容
linkTitle: 配置与连接
description: 启用 Halo MySQL 端点、安装 aux_mysql、创建用户并使用 mysql 客户端连接。
weight: 30
---

当前 Halo Database 文档与开源 OpenHalo README 使用的配置参数不同。请根据实际运行的二进制选择对应小节。

## Halo 16：当前模式配置 {#halo-16}

在 `$PGDATA/postgresql.conf` 中加入 MySQL 监听器和默认数据库：

```conf
cluster_net_services = ':3306:mysql'
mysql.default_tenant = 'mysql'
```

两个参数都是启动参数。重启服务，创建数据库，并在该数据库中安装兼容扩展：

```sh
pg_ctl restart
psql -c "CREATE DATABASE mysql;"
psql -d mysql -c "CREATE EXTENSION aux_mysql CASCADE;"
```

官方说明指出，`aux_mysql` 还会顺带安装 `plmyssql`。所有需要运行 MySQL 兼容语法的数据库都应安装该扩展。

## 创建登录角色 {#user}

通过 PostgreSQL 兼容管理端口连接目标数据库，并使用 MySQL 原生密码加密方式创建角色：

```sh
hsql -h /var/run/halo -p 1921 -U halo -d mysql
```

```sql
SET password_encryption = 'mysql_native_password';
CREATE USER mysqltest SUPERUSER PASSWORD 'replace-with-a-secret';
```

`SUPERUSER` 是官方冒烟示例的写法，可以让演示立即运行。实际应用应使用独立的最小权限角色，明确授予数据库、schema 和表权限。不要复制示例密码，也不要仅为了协议兼容给应用账户授予超级用户权限。

## 使用 MySQL 客户端连接 {#connect}

使用 MySQL 兼容端口，并显式指定目标数据库：

```sh
mysql -h 127.0.0.1 -P 3306 -u mysqltest -D mysql -p
```

连接后可以先检查对外报告的兼容版本，再执行简单查询：

```sql
SELECT VERSION();
SELECT 1;
```

`mysql.default_tenant` 是 MySQL 模式的默认租户数据库。用于配置的数据库必须已经创建，并且在通过 MySQL 端点使用前安装 `aux_mysql`。

## MySQL 模式参数 {#parameters}

官方的 [MySQL 引擎参数参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql-engine-parameters)说明，`mysql.max_allowed_packet` 是这一组参数中唯一可以在线修改的参数；其余参数修改后都需要重启。

| 参数 | 文档默认值 | 用途 |
| --- | --- | --- |
| `mysql.default_tenant` | 无，必须配置 | MySQL 模式的默认数据库。 |
| `mysql.max_allowed_packet` | `64MB` | 协议数据包最大值；可以用 `SET` 修改当前会话值。 |
| `mysql.explicit_defaults_for_timestamp` | `off` | 控制 `TIMESTAMP` 的自动默认值行为。 |
| `mysql.on_error_rollback` | `on` | MySQL 模式发生错误后自动回滚当前事务。 |
| `mysql.halo_mysql_version` | `5.7.32-log` | 向 MySQL 客户端报告的版本字符串，不会改变服务端二进制版本。 |
| `mysql.column_name_case_control` | `0` | 保留列名大小写；`1` 转小写，`2` 转大写。 |
| `mysql.support_multiple_table_update` | `on` | 开启 MySQL 风格的多表 `UPDATE`。 |
| `mysql.multi_table_delete_methond` | `1` | 选择文档定义的多表 `DELETE` 兼容模式；参数名中的拼写是上游原名。 |
| `mysql.create_trigger_for_auto_increment` | `on` | 为 `AUTO_INCREMENT` 行为创建所需触发器。 |
| `mysql.skip_utf8_verify` | `off` | 开启后跳过 UTF-8 合法性校验。 |

兼容参数会改变应用可见行为。部署时记录实际参数值，修改后重新测试迁移和应用查询。

## OpenHalo 源码树：旧版配置 {#openhalo-legacy}

固定版本的开源 [OpenHalo README](https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md) 使用以下参数名：

```conf
database_compat_mode = 'mysql'
mysql.listener_on = true
mysql.port = 3306
```

这些名称属于源码树中的旧版本，不要与 Halo 16 的 `cluster_net_services` 配置混用。启动前请检查当前 OpenHalo 二进制随附的 `postgresql.conf.sample`。

原始的源码编译与远程登录流程保留在[编译与配置 OpenHalo](/openhalo/quick-start/)。其中的 `listen_addresses` 和 `pg_hba.conf` 示例属于 PostgreSQL 管理设置，不能代替 MySQL 监听器配置。

## 资料来源 {#sources}

本页为 [Halo Database MySQL 兼容参考](https://doc.halodbtech.com/multi-mode-compatibility/modes)的原创摘要。上游未明确公开文档许可证；版本、版权与引用方式见[来源说明](/attribution/#halodb)。
