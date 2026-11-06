---
title: "存储过程和用户定义函数"
description: "Apache Cloudberry 提供了强大的扩展数据库功能的能力，支持使用存储过程（SP）和用户定义函数（UDF）。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/overview.md"
---

## 用户定义函数（UDF） {#user-defined-functions-udfs}

用户定义函数（UDF）返回值，可在查询中使用。它们可以将复杂的逻辑和计算封装为可复用的组件。

Apache Cloudberry 支持使用多种过程语言编写 UDF：

- **PL/Python**：使用 Python 3 编写函数。借助不受信任的 `plpython3u` 语言，可以访问系统调用和外部库。
- **[PL/Java](https://github.com/cloudberry-contrib/pljava)**：使用 Java 编写函数，适合复杂计算以及与现有 Java 库集成。
- **PL/Perl**：使用 Perl 编写函数，利用 Perl 强大的字符串处理能力。
- **[PL/Container](https://github.com/cloudberry-contrib/plcontainer)**：在 Docker 容器中安全运行 Python 和 R 函数。这为运行不受信任的代码提供了隔离和安全性。
- **[PL/R](https://github.com/cloudberry-contrib/plr)**：使用 R 统计计算语言编写函数，适合高级数据分析和统计建模。

## 存储过程 {#stored-procedures}

存储过程与函数类似，但不返回值。存储过程通过 `CALL` 命令调用，可以在过程体中执行事务控制（例如 `COMMIT`、`ROLLBACK`）；函数中不允许这样做。

## 支持的语言 {#supported-languages}

| 语言 | 扩展 | 是否受信任 | 描述 |
| :--- | :--- | :--- | :--- |
| **SQL** | 内置 | 是 | 使用标准 SQL 查询编写函数。 |
| **PL/pgSQL** | 内置 | 是 | PostgreSQL 数据库系统的过程语言。 |
| **PL/Python** | `plpython3u` | 否 | Python 3 过程语言。 |
| **PL/Java** | `pljava` | 是 | Java 过程语言。 |
| **PL/Perl** | `plperl` | 是 | Perl 过程语言。 |
| **PL/R** | `plr` | 否 | R 过程语言。 |
| **PL/Container** | `plcontainer` | 是（安全） | 在 Docker 容器中运行 Python/R。 |
