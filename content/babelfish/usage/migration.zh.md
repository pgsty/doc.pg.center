---
title: 迁移到 Babelfish
linkTitle: 迁移指南
description: 评估兼容性，迁移模式与数据，测试应用并准备生产运行。
weight: 60
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/migration.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

## 迁移到 Babelfish {#migrating-to-babelfish}

Babelfish 提供了一条从需要商业许可的 Microsoft SQL Server 迁移到功能完备的开源产品 PostgreSQL 的路径。

本节介绍如何着手迁移到 Babelfish。

### 创建 Babelfish 实例 {#create-a-babelfish-instance}

首先[安装 Babelfish](/zh/babelfish/installation/compiling-babelfish-from-source/)，并确认能够使用 SSMS 或 `sqlcmd` 等客户端建立连接。

对于 Linux 用户，建议使用 Microsoft SQL Server Linux 发行版提供的 `sqlcmd` 检查连通性。也可以使用 [Babelfish 文档](/zh/babelfish/usage/command-line/)中介绍的 FreeTDS 命令行客户端，但它不属于官方支持范围。

实例准备好后，就可以继续下一步。

### 使用 Babelfish Compass 评估兼容性 {#assess-the-compatibility-with-babelfish-using-babelfish-compass}

Babelfish 提供名为 Babelfish Compass 的评估工具，帮助判断应用的复杂程度和迁移的可行性。第一步是运行 Compass 评估：对 DDL（数据定义语言）执行分析，了解 Babelfish 支持哪些 T-SQL 代码，并找出迁移后执行之前需要修改的部分。

从[发布页面](https://github.com/babelfish-for-postgresql/babelfish_compass/releases/latest)下载 Babelfish Compass，并参阅[用户指南](https://github.com/babelfish-for-postgresql/babelfish_compass/blob/main/BabelfishCompass_UserGuide.pdf)。

### 反向生成 SQL Server 模式 {#reverse-engineering-the-sql-server-schema}

评估完成后，将现有 SQL Server 模式迁移到新集群。为所有准备迁移的 SQL Server 用户数据库生成 DDL 语句。

可以使用 SQL Server Management Studio（SSMS）反向生成 DDL：在 SSMS 中选中数据库，使用该工具的脚本生成功能。

不要忘记启用触发器、登录名、所有者和权限的导出。SSMS 默认不导出这些内容。

### 部署模式并迁移数据 {#deploying-the-schema-and-migrating-the-data}

Babelfish 实现了大部分 T-SQL 语句，因此移植生成的 DDL 应当相对容易。

使用 `sqlcmd` 或 SSMS，在新的 Babelfish 服务器上运行 DDL，重建模式。随后即可把数据从原服务器迁移到新服务器。

### 重新配置客户端应用 {#reconfiguring-client-applications}

成功迁移模式和数据后，将客户端应用改为连接 Babelfish 实例。把应用指向新数据源，然后运行测试。

对于客户端而言，Babelfish 应表现为普通的 SQL Server，应用应能正常工作。不过，仍建议进行充分测试。

### 投入生产 {#moving-to-production}

对应用测试结果满意后，即可将 Babelfish 数据库投入生产。注意，从开始迁移数据到开始使用 Babelfish 数据库之间会产生停机时间。缩短停机时间较为复杂，超出了本文档的范围。

### 性能考量 {#performance-considerations}

SQL 在不同平台上的性能可能不同，因此迁移时可能需要调优。这里毕竟是从一种数据库管理系统转向另一种系统，性能不一定相同。

合理调整数据库参数确实有帮助，但未必能解决所有性能问题。换句话说，应做好为获得良好性能而重写查询的准备。

### 通过 PostgreSQL 访问数据 {#accessing-the-data-in-postgresql}

前文介绍了如何让 Microsoft SQL Server 应用使用 Babelfish。由于数据实际存储在 PostgreSQL 数据库中，也可以通过 PostgreSQL 协议访问，使用任何 PostgreSQL 客户端即可。务必连接 PostgreSQL 端口（默认 5432），而不是 TDS 端口（默认 1433）。

对象名称保持不变，但通过 PostgreSQL 访问迁移后的 SQL Server 用户数据库时，模式名称可能不同，具体取决于 [`migration_mode`](/zh/babelfish/installation/single-multiple/) 配置：

- 在 `single-db` 迁移模式下，无论通过 TDS 还是 PostgreSQL 协议连接，迁移后的用户数据库模式名称都相同。
- 在 `multi-db` 迁移模式下，模式名称由 TDS 连接中使用的数据库名和模式名组合而成。例如，通过 TDS 在数据库 `d1` 的模式 `s1` 中创建表 `t1` 后，通过 PostgreSQL 协议访问时，应写为 `d1_s1.t1`。
