---
title: PgAudit
linkTitle: pgaudit
description: IvorySQL v5.6 文档：PgAudit。
type: docs
weight: 430
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/5.8.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 概述 {#overview}

PgAudit 是一个审计扩展，可以为 DDL、DML、DCL 等关键操作生成可追溯的日志记录。通过审计日志，数据库管理员能够满足合规要求、及时发现异常行为，并在出现问题时快速定位责任主体与影响范围。

## 2. 功能特点 {#key-features}

- **全面审计能力**：记录 `SELECT`、`INSERT`、`UPDATE`、`DELETE`、DDL 命令以及权限变更等操作，帮助构建完整的操作轨迹。

- **灵活的审计维度**：支持全局审计、角色审计与对象审计，可按用户、角色、模式或具体操作类型进行精细化配置。

- **平滑集成**：复用 PostgreSQL 标准日志子系统，可与 `syslog`、`logrotate` 等工具联动，兼容现有日志采集与分析方案。

- **合规支撑**：提供结构化审计日志，便于生成符合金融、政企等行业规范的审计报告。

- **安全增强**：通过记录和分析数据库活动，及时发现未授权访问、异常 DML 或潜在数据泄露风险。

- **运维优化**：辅助回放操作行为、定位性能瓶颈，支撑 SQL 优化与问题排查。

## 3. 安装部署 {#installation-and-deployment}

### 3.1. 环境准备 {#prerequisites}

- 已安装的 IvorySQL 数据库。

- 编译工具链：`gcc`、`make`、`tar` 等。

- 数据库管理员权限，用于修改 `ivorysql.conf` 并重启数据库实例。

### 3.2. 编译安装 PgAudit {#compile-and-install-pgaudit}

以 PgAudit 18.0 为例：

```
wget https://github.com/pgaudit/pgaudit/archive/refs/tags/18.0.tar.gz
tar -xf 18.0.tar.gz
cd pgaudit-18.0
make install USE_PGXS=1 PG_CONFIG=$PGHOME/bin/pg_config
```

上述命令依赖环境变量 `PGHOME` 指向安装好的 IvorySQL 主目录。安装成功后，`pgaudit.so` 会被放置到 IvorySQL 的扩展目录中。

### 3.3. 注册扩展前的基础配置 {#baseline-configuration-before-registering-the-extension}

修改 `ivorysql.conf`，启用插件并设置常用参数：

```
shared_preload_libraries = 'pgaudit'   # 需实例重启生效
pgaudit.log = 'read, write, ddl'       # 审计范围示例，可按需调整
```

重启数据库实例，使共享库配置生效。

### 3.4. 创建扩展并验证 {#create-the-extension-and-verify}

``` sql
CREATE EXTENSION IF NOT EXISTS pgaudit;
SELECT name,
       default_version,
       installed_version,
       comment
  FROM pg_available_extensions
 WHERE name = 'pgaudit';
```

若返回的 `installed_version` 与期望版本一致，说明扩展安装成功。

## 4. 使用 {#usage}

执行如下sql示例：

``` sql
CREATE TABLE audit_demo(id serial PRIMARY KEY, info text);
INSERT INTO audit_demo(info) VALUES ('pgaudit test');
SELECT * FROM audit_demo;
UPDATE audit_demo SET info = 'pgaudit update' WHERE id = 1;
DELETE FROM audit_demo WHERE id = 1;
```

在数据库服务器上查看审计日志：

```
tail -f $PGDATA/log/*.log | grep 'AUDIT:'
```

```
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE SEQUENCE,SEQUENCE,public.audit_demo_id_seq,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE TABLE,TABLE,public.audit_demo,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,CREATE INDEX,INDEX,public.audit_demo_pkey,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.113 CST [11451] LOG:  AUDIT: SESSION,1,1,DDL,ALTER SEQUENCE,SEQUENCE,public.audit_demo_id_seq,"CREATE TABLE audit_demo(id serial PRIMARY KEY, info text)",<not logged>
2025-10-31 15:56:32.117 CST [11451] LOG:  AUDIT: SESSION,2,1,WRITE,INSERT,,,INSERT INTO audit_demo(info) VALUES ('pgaudit test'),<not logged>
2025-10-31 15:56:32.121 CST [11451] LOG:  AUDIT: SESSION,3,1,READ,SELECT,,,SELECT * FROM audit_demo,<not logged>
2025-10-31 15:56:32.122 CST [11451] LOG:  AUDIT: SESSION,4,1,WRITE,UPDATE,,,UPDATE audit_demo SET info = 'pgaudit update' WHERE id = 1,<not logged>
2025-10-31 15:56:32.127 CST [11451] LOG:  AUDIT: SESSION,5,1,WRITE,DELETE,,,DELETE FROM audit_demo WHERE id = 1,<not logged>
```

若想记录参数的值，打开\`pgaudit.log_parameter = 'on'\`，效果如下：

```
ivorysql=# SHOW pgaudit.log_parameter;
pgaudit.log_parameter
-----------------------
on
(1 row)
```
