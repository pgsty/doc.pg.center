---
title: Babelfish 互操作性
linkTitle: 双协议互操作
description: 混用两种 SQL 方言时，核对模式、权限、事务语义与升级影响。
weight: 40
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/interoperability.md
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

## Babelfish 互操作指南 {#guidance-on-babelfish-interoperability}

Babelfish 通过 TDS 端口提供 T-SQL 方言，在 PostgreSQL 之上实现 T-SQL 语义。也可以通过标准 PostgreSQL 端口，使用 PostgreSQL SQL 语句访问 Babelfish 数据库。在 Babelfish 上下文中执行 PostgreSQL 语句或进行 PostgreSQL 访问时，两者可能相互干扰，影响语法、语义，以及与未来 Babelfish 版本的兼容性。遇到这类场景，需要留意模式名称、标识符、权限、事务语义、多结果集、默认排序规则和未来升级等方面的问题。

## Babelfish 与 PostgreSQL 的互操作 {#babelfishpostgresql-interoperability}

Babelfish for PostgreSQL 提供两个数据库访问端点：TDS 端口（默认 1433）提供具有 T-SQL 语法和语义的接口；PostgreSQL 端口（默认 5432）提供具有 PostgreSQL SQL 语法和语义的接口。

术语说明：本文中，*TDS* 与 *T-SQL*、*PostgreSQL* 与 *PostgreSQL SQL* 分别作为同义词使用，既指 SQL 方言，也指相应的数据库连接。

本文所说的 Babelfish 数据库，是为在 T-SQL 方言中模拟 SQL Server 多数据库环境而创建的 PostgreSQL 数据库，其中包含 `master`、`tempdb` 和一个或多个用户数据库。它的默认名称为 `babelfish_db`。TDS 连接始终位于这个数据库中，只是在 T-SQL 中看不到这一点。每个 PostgreSQL 实例只能有一个 Babelfish 数据库。

Babelfish 数据库归根结底是 PostgreSQL 数据库，因此技术上可以通过 PostgreSQL 端口访问并执行 PostgreSQL SQL。不过，这种访问方式涉及一些复杂问题，需要谨慎处理。

最简单的办法是完全避免通过 PostgreSQL 访问 Babelfish 数据库。但使用 PostgreSQL 功能也有合理理由：例如，Babelfish 尚不支持某项 T-SQL 功能时，或许可以用 PostgreSQL 原生能力实现，以完成应用迁移。

只要执行上下文并非纯粹的 TDS/T-SQL，也就是在 Babelfish 上下文中执行了 PostgreSQL SQL，就需要考虑互操作问题，包括：

- 在 PostgreSQL 连接中，对 Babelfish 创建的对象（表、视图、过程等）执行 PostgreSQL 语句。
- 在 TDS 连接中，对 PostgreSQL 创建的对象执行 T-SQL，或者从 T-SQL 调用 PostgreSQL 内置函数。根据用户反馈，后一类场景更常见。

在这两种情况下，访问或执行由另一种 SQL 方言创建的对象时，会话中的 SQL 方言实际上会暂时、透明地切换；访问表不属于这一切换情形。

应用出现上述情况时，可能需要考虑下面一项或多项因素。用户有责任判断混合 SQL 方言的应用是否按预期工作，也应预料到未来升级 Babelfish 时可能出现问题，并可能需要自行解决。

- **模式名称**

  Babelfish 将各个 SQL Server 数据库展开为 PostgreSQL 数据库（默认 `babelfish_db`）中的模式，以模拟 SQL Server 的多数据库结构。例如，在 T-SQL 中创建的表 `mydb.dbo.mytable` 和过程 `yourdb.dbo.yourproc`，在 PostgreSQL 中必须分别写为 `mydb_dbo.mytable` 和 `yourdb_dbo.yourproc`，参见[单数据库与多数据库模式](/zh/babelfish/installation/single-multiple/)。此外，SQL Server 和 PostgreSQL 对未指定模式名的对象采用不同的名称解析规则。在 PostgreSQL 连接中操作 Babelfish 数据库时，必须考虑这些差异。

- **标识符**

  PostgreSQL 的标识符长度上限为 63 个字符，SQL Server 则支持 128 个字符；PostgreSQL 对索引名称的唯一性要求也更严格。Babelfish 通过在标识符后追加、或用一个 32 字符的哈希值替换其中一部分来应对这些限制。T-SQL 用户看不到这一处理，但在 PostgreSQL 中，对象名称会包含该哈希值。

  例如，表 `t1` 上名为 `ix1` 的索引，内部名称为 `ix1t1a5111d2a1767bc43a700e9f2162be019`。Babelfish 将索引名、表名以及小写索引名的 MD5 哈希串拼接起来。

- **权限**

  为实现 SQL Server 权限模型，Babelfish 创建 PostgreSQL 角色，以表示 SQL Server 数据库主体等概念。这些由 Babelfish 管理的 PostgreSQL 结构在 T-SQL 中不可见，但在 PostgreSQL 连接中可见。

  不应通过 PostgreSQL 修改这些角色，也不应通过 PostgreSQL 授予或撤销 Babelfish 创建的对象上的权限。即使技术上可以这样做，也可能让实例无法兼容未来版本，导致升级失败；还可能造成当前或未来版本的权限配置异常，因为 PostgreSQL 侧的操作会干扰安全相关 T-SQL 语句的预期结果。

  对于通过 TDS 连接、使用 T-SQL 创建的表或其他 SQL 对象，Babelfish 保证同一用户通过 PostgreSQL 端口连接时，无需额外执行 PostgreSQL 语句即可获得相同的访问权限，但仍须考虑模式名称等差异。反过来则没有保证：在 PostgreSQL 中创建的对象，可能在 TDS 连接中不可见、不可访问，或以不同权限访问。因此，需要通过 PostgreSQL 访问的模式和对象应当用 T-SQL 创建。

- **事务语义**

  T-SQL 与 PostgreSQL SQL 的语义大体相同，但事务回滚和错误处理存在明显差异。例如，发生约束违例时，T-SQL 默认只回滚出错的语句，然后继续执行下一条语句，当前事务仍保持打开；PostgreSQL SQL 则会回滚整个事务并退出代码块。

  通过 TDS 连接执行 T-SQL 时，采用 T-SQL 事务语义；通过 PostgreSQL 连接执行 PostgreSQL 语句时，采用 PostgreSQL 事务语义。但在同一连接中混用两种方言时，原则上会忽略 T-SQL 事务语义，仅使用 PostgreSQL 语义。因此，同一个 T-SQL 过程在 PostgreSQL 上下文中执行时，行为可能不同。

- **多个结果集**

  T-SQL 支持从批处理或过程向客户端返回多个结果集，PostgreSQL 则不支持：对于过程，PostgreSQL 不支持返回结果集；对于批处理，只发送第一个结果集。因此，在 PostgreSQL 上下文中执行 T-SQL 过程或批处理，可能得不到预期结果。

- **默认排序规则**

  T-SQL 与 PostgreSQL SQL 的默认排序规则不同，可能造成语义差异。例如，在 Babelfish T-SQL 中，默认排序规则不区分大小写，所以 `'a' = 'A'` 为真；而 PostgreSQL SQL 的默认排序规则区分大小写，该表达式为假。

- **未来的 Babelfish 升级**

  用户将部分迁移后的 T-SQL 应用改用 PostgreSQL 实现，最常见的原因是绕过 Babelfish 尚未支持的 T-SQL 功能。如果未来 Babelfish 开始支持这些功能，现有应用可能与新版本不兼容，导致升级后的实例不能正常工作，或升级本身失败。

## 互操作场景 {#interoperability-scenarios}

- 最简单的起点是完全没有互操作：将应用纵向拆分为 T-SQL 和 PostgreSQL 两部分，各自使用独立用户和模式，彼此不交互。应用同时建立到 Babelfish 数据库的 TDS 连接，以及到另一个 PostgreSQL 数据库的 PostgreSQL 连接。两者完全分离、不相互干扰，因此数据库层面没有互操作问题。但如果两条连接使用同一用户名，仍可能存在依赖。
- 更常见的变体是 PostgreSQL 连接访问 Babelfish 数据库，但只操作 PostgreSQL 创建的对象，而 T-SQL 只操作 Babelfish 创建的对象。这本身不会造成干扰，但实际中通常需要两种上下文交换信息，例如共同访问一张表。这样的表应由 T-SQL 创建，而不是 PostgreSQL；除此之外，这一场景通常没有问题。需要考虑模式名称、标识符和权限。
- 另一种预计问题较少的场景是 PostgreSQL 连接只读取 Babelfish 创建的表，需要考虑模式名称、标识符和权限。如果还读取视图，则还需考虑视图内部引用的模式名和标识符。
- 如果 PostgreSQL 连接还修改 Babelfish 创建的表，或执行 DDL 修改这些对象，则还需要考虑事务语义。
- 更复杂的情况是 PostgreSQL 连接直接、或通过 PostgreSQL 过程执行 T-SQL 过程，或者修改带有 Babelfish 触发器的 Babelfish 表。用户需要仔细验证最终语义。

## 互操作示例 {#interoperability-examples}

**不受支持的语句**

假设某个 T-SQL 存储过程有 100 条语句，其中 99 条受到 Babelfish 完整支持，只有 1 条不受支持。如果能把这条语句重写为 PostgreSQL 过程，并从 T-SQL 中调用，便可能完成迁移。但实际中，也可能只有把其余过程一并改写为 PostgreSQL，才能实现这条语句。用户需要决定用 T-SQL 还是 PostgreSQL，以及重写、重构或重新设计的范围。

**表分区**

原文所述 Babelfish 版本不支持 SQL Server 表分区。可以尝试先在 Babelfish 中创建表，再通过 PostgreSQL 修改表、添加分区。分区是原则上不改变功能语义的性能特性，因此理论上可行。但如果未来 Babelfish 支持 T-SQL 风格的分区，这种做法可能产生兼容性问题。

**全文搜索**

可以尝试重构应用，将全文搜索封装在 PostgreSQL 存储过程中，再从 T-SQL 调用，以迁移需要全文搜索的应用。同样需要考虑未来 Babelfish 版本的兼容性。

**PostGIS 扩展**

对于使用 T-SQL 地理空间功能的应用，可以考虑 PostGIS 扩展。但可能需要更大范围的重构，并设计在 T-SQL 与 PostGIS 之间传递数据的机制；也要考虑未来兼容性。

**XML 处理**

对于使用 XML 的 T-SQL 应用，如果能将 XML 功能拆分为 PostgreSQL 过程和函数，或许可以工作。这类变通方案可能十分复杂，也需要考虑未来兼容性。
