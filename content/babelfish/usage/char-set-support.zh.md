---
title: T-SQL 与 PostgreSQL 的字符集支持
linkTitle: 字符集
description: 理解字符串编码、代码页，以及 T-SQL 与 PostgreSQL 的长度计算差异。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/char_set_support.md
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

## T-SQL 与 PostgreSQL 的字符集支持 {#character-set-support-in-tsql-and-postgresql}

### 字符串编码 {#string-encoding}

T-SQL 和 PostgreSQL 都支持多种客户端及服务器端字符串编码。不过，PostgreSQL 在同一连接中只使用一种客户端编码和一种服务器端编码，而 T-SQL 的每个字符串都可以根据其排序规则的代码页指定自己的编码。

在 T-SQL 中，`VARCHAR` 和 `CHAR` 的客户端编码由排序规则的代码页决定；`NVARCHAR` 和 `NCHAR` 的客户端编码则始终为 `UTF-16`。例如，声明为 `VARCHAR(10) COLLATE sql_latin1_general_cp1_ci_as` 的字符串，会在客户端使用该排序规则的 `WIN1252` 代码页进行编码。`WIN1252` 使用十分广泛，因此获得了特殊缩写 `cp1`，即“代码页 1”。它是每字符一个字节的编码，只能表示 256 个字符。

在 Unicode 出现之前，各地区逐步形成了自己的代码页，以容纳当地语言所需的字符；每种编码中的码点顺序也反映当地习惯的字符排序方式。因此，只用一个字节就能表示世界上大部分地区的字符，并通过高效的逐字节比较进行排序。但这种方法无法处理不区分大小写或重音的比较；大量不同编码也让客户端应用更加复杂，最终促成了 Unicode 的发展。`NVARCHAR` 与 `NCHAR` 使用 `UTF-16` 表示 Unicode 字符串，一种编码即可涵盖全球文字和表情符号等新字符。Unicode 将字符编码与字符的排序、比较分离开来。

Babelfish 在服务器端将所有字符串存为 `UTF-8`，并在客户端与服务器交换数据时，自动在 `UTF-8` 与相应代码页编码或 `UTF-16` 之间转换，以模拟 T-SQL 的字符串编码行为。

### T-SQL 与 PostgreSQL 如何解释字符串最大长度 {#how-maximum-string-length-is-interpreted-in-tsql-and-postgresql}

在 PostgreSQL 中，`VARCHAR(n)` 表示最多容纳 `n` 个字符，`CHAR(n)` 表示固定为 `n` 个字符；在 T-SQL 中，这里的单位则是字节。对于西方语言和常见的欧洲代码页，由于每字符占一个字节，两者没有差别。但韩文、日文、中文等语言使用变长编码，情况便不同了。

T-SQL 在 `INSERT` 或 `UPDATE` 时对字符串编码，以检查是否满足最大长度约束。因此，对于变长编码，Babelfish 必须先把字符串转换为客户端编码，按字节检查最大长度，之后才能以 `UTF-8` 存入服务器。

T-SQL 这种解释方式带来了一个特殊结果：即使使用变长编码，定长类型 `CHAR(n)` 也只能存储恰好 `n` 字节的字符串。这使它在韩文、日文和中文等语言中显得不够灵活，也可能不太实用。

### PostgreSQL 方言中的 sys.varchar 与 sys.sysname {#behavior-of-sysvarchar-and-syssysname-data-types-in-the-postgresql-dialect}

从 Babelfish 2.2 起，建议使用 T-SQL 方言执行 `CREATE TABLE`。在 T-SQL 方言中，声明为 `VARCHAR(n)` 的列会解析为 `sys.varchar` 类型，默认排序规则与显式指定 `COLLATE DATABASE_DEFAULT` 相同。
