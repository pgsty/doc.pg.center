---
title: 排序规则与语言支持
linkTitle: 排序规则与区域设置
description: 查阅排序规则映射、Unicode 比较行为与区域设置限制。
weight: 50
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/locales.md
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

## 排序规则与语言支持 {#collations-and-language-support}

排序规则规定数据的排序顺序和呈现格式。Babelfish 将 SQL Server 排序规则映射为自身提供的相近规则，预定义了符合各地语言习惯的 Unicode 字符串比较与排序规则，并提供将 SQL Server 数据库排序规则转换为最接近的 Babelfish 排序规则的方法。不同语言和地区都有相应的区域排序规则。

某些排序规则指定了与客户端编码对应的代码页。Babelfish 会根据每个输出列的排序规则，自动将服务器编码转换为客户端编码。

有关 PostgreSQL 排序规则行为的详细信息，参见 [PostgreSQL 文档](https://www.postgresql.org/docs/13/collation.html)。

Babelfish 支持**确定性**和**非确定性**排序规则：

- 确定性排序规则仅当两个字符的字节序列完全相同时，才认为它们相等。例如，`x` 不等于 `X`。确定性排序规则区分大小写（cs），也区分重音（as）。
- 非确定性排序规则不要求字节完全匹配。不区分大小写（ci）就是一种非确定性特征。若希望 `x` 与 `X` 相等，应选择支持不区分大小写的非确定性排序规则。

Babelfish 与 SQL Server 都通过命名约定表达排序规则的属性：

| 属性   | 说明                                            |
| ----------- | ------------------------------------------------------ |
| `ai`        | 不区分重音                                     |
| `as`        | 区分重音                                       |
| `bin`       | BIN 按码点顺序排序，将首字符作为 wchar 处理。码点顺序是一种高效的确定性排序规则。 |
| `bin2`      | BIN2 按码点顺序排序。码点顺序是一种高效的确定性排序规则。 |
| `ci`        | 不区分大小写                                       |
| `cs`        | 区分大小写                                         |
| `pref`      | 使用 `pref` 可让大写字母排在小写字母之前。在区分大小写的比较中，如果没有其他差异，同一字母的大写形式优先。ICU 通过 `colCaseFirst=upper` 支持大写优先，但不适用于 `ci_as`。`pref` 只能用于确定性的 `cs_as` 排序规则。  |

原文对应的 PostgreSQL 版本不支持在非确定性排序规则上使用 `LIKE`，但 Babelfish 为 `ci_as` 提供了支持。Babelfish 不支持在 `ai` 排序规则上使用 `LIKE`，也不支持非确定性排序规则上的模式匹配操作。

以下参数决定 Babelfish 的排序规则行为：

| 参数             | 说明                                   |
| --------------------- | --------------------------------------------- |
| `server_collation_name`  | 服务器级和数据库级使用的默认排序规则。默认值为 `sql_latin1_general_cp1_ci_as`。创建用于 Babelfish 的 PostgreSQL 集群时，可从下表选择排序规则。创建 Babelfish 数据库后，不要修改 `server_collation_name`。  |
| `default_locale`      | 为所有不绑定区域设置的排序规则（名称中不包含语言）指定语言和地区，默认 `en-US`。如果所选排序规则已隐含区域设置，则忽略此参数。数据库创建后可以修改，但不会改变现有排序规则的区域设置。 |

以下排序规则可用于 `server_collation_name` 或列定义。注意，服务器默认排序规则仅支持不区分大小写的规则。

| 排序规则名称        | 说明                                         |
| --------------------- | --------------------------------------------- |
| `bbf_unicode_general_ci_as` | 面向 UTF-8、不区分大小写的排序规则，尽可能适应多语言环境。 |
| `bbf_unicode_cp1250_ci_as` | 适用于 [Windows-1250 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1250.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1251_ci_as` | 适用于 [Windows-1251 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1251.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1_ci_as` | 适用于 [Windows-1252 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1252.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1253_ci_as` | 适用于 [Windows-1253 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1253.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1254_ci_as` | 适用于 [Windows-1254 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1254.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1255_ci_as` | 适用于 [Windows-1255 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1255.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1256_ci_as` | 适用于 [Windows-1256 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1256.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1257_ci_as` | 适用于 [Windows-1257 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1257.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp1258_ci_as` | 适用于 [Windows-1258 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1258.txt) 的不区分大小写排序规则。 |
| `bbf_unicode_cp874_ci_as` | 适用于 [Windows-874 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit874.txt) 的不区分大小写排序规则。 |
| `sql_latin1_general_cp1250_ci_as` | 与 `bbf_unicode_cp1250_ci_as` 相同。 |
| `sql_latin1_general_cp1251_ci_as` | 与 `bbf_unicode_cp1251_ci_as` 相同。 |
| `sql_latin1_general_cp1_ci_as` | 与 `bbf_unicode_cp1_ci_as` 相同。 |
| `sql_latin1_general_cp1253_ci_as` | 与 `bbf_unicode_cp1253_ci_as` 相同。 |
| `sql_latin1_general_cp1254_ci_as` | 与 `bbf_unicode_cp1254_ci_as` 相同。 |
| `sql_latin1_general_cp1255_ci_as` | 与 `bbf_unicode_cp1255_ci_as` 相同。 |
| `sql_latin1_general_cp1256_ci_as` | 与 `bbf_unicode_cp1256_ci_as` 相同。 |
| `sql_latin1_general_cp1257_ci_as` | 与 `bbf_unicode_cp1257_ci_as` 相同。 |
| `sql_latin1_general_cp1258_ci_as` | 与 `bbf_unicode_cp1258_ci_as` 相同。 |
| `sql_latin1_general_cp874_ci_as` | 与 `bbf_unicode_cp874_ci_as` 相同。 |
| `latin1_general_ci_as` | 与 `sql_latin1_general_cp1_ci_as` 相同。 |
| `arabic_ci_as` | 支持阿拉伯语。 |
| `chinese_prc_ci_as`  | 支持中文（中国）。  |
| `cyrillic_general_ci_as` | 支持西里尔文字。 |
| `estonian_ci_as` | 支持爱沙尼亚语。  |
| `finnish_swedish_ci_as` | 支持芬兰语。  |
| `french_ci_as` | 支持法语。 |
| `greek_ci_as` | 支持希腊语。 |
| `hebrew_ci_as` | 支持希伯来语。 |
| `japanese_ci_as` | 支持日语。 |
| `korean_wansung_ci_as` | 支持韩语（字典排序）。 |
| `modern_spanish_ci_as` | 支持现代西班牙语。 |
| `mongolian_ci_as` | 支持蒙古语。 |
| `polish_ci_as` | 支持波兰语。 |
| `thai_ci_as` | 支持泰语。 |
| `traditional_spanish_ci_as` | 支持西班牙语（传统排序）。 |
| `turkish_ci_as`  | 支持土耳其语。 |
| `ukrainian_ci_as`   | 支持乌克兰语。   |
| `vietnamese_ci_as`  | 支持越南语。 |

列定义还可以使用上述规则中区分大小写或不区分重音的变体，以及以下二进制排序规则：

| 排序规则名称            | 说明                              |
| ------------------------- | ---------------------------------- |
| `latin1_general_bin2`     | 适用于 [Windows-1252 单字节字符编码](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/bestfit1252.txt) 的二进制排序规则。 |
| `latin1_general_100_bin2` | 与 `latin1_general_bin2` 相同。 |
| `latin1_general_140_bin2` | 与 `latin1_general_bin2` 相同。 |
| `latin1_general_90_bin2`  | 与 `latin1_general_bin2` 相同。 |

如果希望在同一数据库中支持多个区域设置，可以在列定义中使用以下排序规则：

| 语言   | 确定性版本 | 非确定性版本         |
| --------- | --------------------- | --------------------------------- |
| `arabic`    | `arabic_cs_as`  | `arabic_ci_as`, `arabic_ci_ai`    |
| `chinese`   | `chinese_prc_cs_as`  | `chinese_prc_ci_as`, `chinese_prc_ci_ai`  |
| `cyrillic_general`  | `cyrillic_general_cs_as` | `cyrillic_general_ci_as`, `cyrillic_general_ci_ai` |
| `estonian`  |`estonian_cs_as` | `estonian_ci_as`, `estonian_ci_ai` | 
| `finnish_swedish` | `finnish_swedish_cs_as` | `finnish_swedish_ci_as`, `finnish_swedish_ci_ai` | 
| `french`    | `french_cs_as`        | `french_ci_as`, `french_ci_ai`    |
| `greek`     | `greek_cs_as`    | `greek_ci_as`, `greek_ci_ai`   |
| `hebrew`   | `hebrew_cs_as`    | `hebrew_ci_as`, `hebrew_ci_ai` |
| `japanese` | `japanese_cs_as`  |  `japanese_ci_as`,  `japanese_ci_ai` |
| `korean_wamsung`    | `korean_wamsung_cs_as`  | `korean_wamsung_ci_as`, `korean_wamsung_ci_ai` |
| `modern_spanish`  | `modern_spanish_cs_as` | `modern_spanish_cs_as`, `modern_spanish_ci_ai` |
| `mongolian` | `mongolian_cs_as`     | `mongolian_ci_as`, `mongolian_ci_ai` |
| `polish`  | `polish_cs_as`        | `polish_ci_as`, `polish_ci_ai` |
| `thai`    | `thai_cs_as`          | `thai_ci_as`, `thai_ci_ai` |
| `traditional_spanish` | `traditional_spanish_cs_as` | `traditional_spanish_ci_as`, `traditional_spanish_ci_ai` |
| `turkish`   | `turkish_cs_as`       | `turkish_ci_as`, `turkish_ci_ai`  |
| `ukranian`  | `ukranian_cs_as`      | `ukranian_ci_as`, `ukranian_ci_ai` |
| `vietnamese` | `vietnamese_cs_as` | `vietnamese_ci_as`, `vietnamese_ci_ai` |

### 管理排序规则 {#managing-collations}

ICU 库提供排序规则版本跟踪，以便 ICU 更新后，对依赖这些规则的索引重建索引。以下查询可找出当前数据库中需要刷新的排序规则，以及依赖这些规则的对象：

```sql
SELECT 	pg_describe_object(refclassid, refobjid, refobjsubid) AS "Collation", 
	pg_describe_object(classid, objid, objsubid) AS "Object" 
FROM 	pg_depend d JOIN pg_collation c 
	ON refclassid = 'pg_collation'::regclass 
		AND refobjid = c.oid 
WHERE 	c.collversion < > pg_collation_actual_version(c.oid) 
ORDER BY 1, 2;
```

预定义排序规则存储在 `sys.fn_helpcollations` 表中。以下命令可显示排序规则的信息，例如 LCID、style 和 collate 标志。使用 `psql` 连接 PostgreSQL 端口（默认 `5432`），执行：

```sql
postgres=# SET search_path = public, pg_temp, sys;
SET
postgres=# \dO
```

或者连接 T-SQL 端口（默认 `1433`），执行：

```sql
SELECT * FROM fn_helpcollations();
```

### 排序规则的限制与行为 {#collation.limitations}

Babelfish 使用 ICU 库支持排序规则。下面列出一些已知限制和行为差异。

### 在非确定性排序规则中使用 CHARINDEX() {#using-charindex-with-a-non-deterministic-collation}

注意：以下限制仅适用于 Babelfish 1.x.x，已在 2.1.0 版本中解决。

在该旧版本中，适用排序规则为非确定性规则时，无法使用 `CHARINDEX()`。Babelfish 默认使用不区分大小写的非确定性排序规则，因此可能出现运行时错误：“nondeterministic collations are not supported for substring searches”。可以采用以下两种变通办法：

- 显式将表达式转换为区分大小写的排序规则，并对两个参数都应用 `LOWER()` 或 `UPPER()`，统一大小写。例如，将 `SELECT CHARINDEX('x', a) from t1` 改为 `SELECT CHARINDEX(LOWER('x'), LOWER(a collate sql_latin1_general_cp1_cs_as)) from t1`。
- 创建名为 `f_charindex()` 的 SQL 函数，用它替代 `CHARINDEX()` 调用：

```sql
create function f_charindex(@s1 varchar(max), @s2 varchar(max)) returns int
as
begin
declare @i int = 1
while len(@s2) >= len(@s1)
begin
   if lower(@s1) = lower(substring(@s2,1,len(@s1))) return @i
   set @i += 1
   set @s2 = substring(@s2,2,999999999)
end
return 0
end
go
```

#### Unicode 排序规则 {#unicode-sorting-rules}

在 SQL Server 中，以 `SQL_` 开头的“SQL”排序规则，对 Unicode 数据（`nchar` 和 `nvarchar`）与非 Unicode 数据（`char` 和 `varchar`）采用不同的排序方式。Babelfish 数据库始终采用 UTF-8 编码，不论数据类型如何，都统一使用 Unicode 排序规则。

#### 二级相等排序规则 {#secondary-equal-collations}

ICU 默认的 Unicode 二级相等（`ci_as`）排序规则，将标点符号和其他非字母数字字符排在数字之前，将数字排在字母之前。不过，标点与特殊字符内部的相对顺序，可能与 SQL Server 对应规则不同。

#### 三级排序规则 {#tertiary-collations}

`sql_latin1_general_pref_cp1_ci_as` 等 SQL 排序规则支持 `TERTIARY_WEIGHTS` 函数，可以让在 `ci_as` 下相等的字符串按大写优先排序：`ABC`、`ABc`、`AbC`、`Abc`、`aBC`、`aBc`、`abC`，最后是 `abc`。因此，分析函数 `DENSE_RANK() OVER (ORDER BY column)` 会赋予这些字符串相同名次，但在分区内按大写优先排列。

在 Babelfish 中，可为 `ORDER BY` 添加 `COLLATE` 子句，指定带 `@colCaseFirst=upper` 的三级 `cs_as` 排序规则，得到相近结果。但 `colCaseFirst` 修饰符只适用于三级相等的字符串，而不是 `ci_as` 的二级相等。因此，单个 ICU 排序规则无法模拟 SQL 的三级排序规则。建议的变通方式是让 `GROUP BY` 和 `ORDER BY` 使用不同排序规则。

#### PostgreSQL 每种排序规则仅支持一个版本 {#postgresql-supports-exactly-one-version-of-each-collation}

PostgreSQL 对每种排序规则只支持一个版本。SQL Server 则可以同时支持同一种规则的多个版本，通常通过在名称中添加 `_80`、`_100` 等版本后缀区分。

#### 字符展开 {#character-expansion}

字符展开会在一级比较中，将单个字符视为与某个字符序列相等。SQL Server 默认的 `ci_as` 排序规则支持字符展开；ICU 则只在不区分重音的排序规则中支持。

PostgreSQL 的字符重排选项比 ICU 更受限，无法让特殊字符的排列顺序与 SQL Server 完全一致。

需要字符展开时，必须使用 `ai` 排序规则比较，但原文对应版本的 `LIKE` 不支持这类规则。采用默认 `ci_as` 的列可以使用 `LIKE`，且不执行字符展开，这通常符合预期；同时，仍可在等值比较中显式指定 `ci_ai`，以进行字符展开。如果在 `ci_as` 列上显式使用 `ci_ai` 创建表达式索引，优化器便可利用它高效执行等值比较和分组。

#### char 与 varchar 编码 {#char-and-varchar-encoding}

对 `char` 或 `varchar` 使用以 SQL 开头的排序规则时，ASCII 127 以上字符的顺序由该规则的具体代码页决定。因此，同一 SQL 排序规则下，`char`、`varchar` 与 `nchar`、`nvarchar` 字符串的排序结果可能不同。

PostgreSQL 使用数据库编码存储所有字符串，因此会将字符转换为 UTF-8，再按 Unicode 规则排序。

SQL 排序规则对 `nchar` 和 `nvarchar` 使用 Unicode 规则。Babelfish 在服务器上将所有字符串存为 UTF-8，因此 `nchar`、`nvarchar` 与 `char`、`varchar` 都按同一套 Unicode 规则排序。

#### 补充字符 {#supplementary-character}

SQL Server 的 `NCHAR`、`UNICODE` 和 `LEN` 函数支持 Unicode 基本多文种平面（BMP）以外的码点，而非 SC 排序规则通过代理对处理补充字符。对于 Unicode 数据类型，SQL Server 使用 UCS-2 时最多可表示 65,535 个字符；使用补充字符时，可以覆盖完整 Unicode 范围（原文记为 1,114,111 个字符）。数据库对象名等元数据不支持补充字符。名称中不含 SC 的排序规则，在 UTF-16 与 UCS-2 编码下的行为也不同。

#### 区分假名 {#kana-sensitive}

若排序规则区分日语平假名（Hiragana）与片假名（Katakana），则称为区分假名（KS）。ICU 支持日语排序标准 `JIS X 4061`。现已废弃的区域修饰符 `colhiraganaQ [on | off]` 可能提供类似 KS 的功能，但原文对应的 Babelfish 版本不提供与 SQL Server 同名的 KS 排序规则。

#### 区分宽度 {#width-sensitive}

若排序规则区分单字节的半角字符与双字节的同一全角字符，则称为区分宽度（WS）。原文对应的 Babelfish 版本不提供与 SQL Server 同名的 WS 排序规则。

#### 区分异体字选择符 {#variation-selector-sensitivity}

区分异体字选择符（VSS）的排序规则，会在日语排序规则 `Japanese_Bushu_Kakusu_140` 和 `Japanese_XJIS_140` 中区分表意文字异体字选择符。异体字序列由基础字符和附加选择符构成；不选择 `_vss` 选项时，比较不会考虑选择符。

原文对应的 Babelfish 版本不提供 VSS 排序规则。

#### bin 与 bin2 {#bin-and-bin2}

`bin2` 按码点顺序排序。UTF-8 的逐字节二进制顺序保持 Unicode 码点顺序，因此它也很可能具有最佳性能。如果应用可以接受 Unicode 码点顺序，应考虑 `bin2`，但客户端显示的顺序可能不符合当地语言习惯。

Unicode 会不断增加新的小写字符映射，因此不同 ICU 版本中的 `lower` 函数行为可能不同。这是排序规则版本管理的一般问题，并非 `bin2` 独有。Babelfish 提供 `bbf_latin1_general_bin2`，按 Unicode 码点顺序排序。

BIN 排序规则只将第一个字符作为 wchar 排序，其余字符逐字节比较，实际上遵循各自编码的码点顺序。这不符合 Unicode 排序规则，因此 Babelfish 不支持。
