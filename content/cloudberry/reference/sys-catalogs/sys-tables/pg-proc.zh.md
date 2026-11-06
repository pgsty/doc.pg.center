---
title: "pg_proc"
description: "`pg_proc` 系统目录表存储函数（或过程）的信息，包括内置函数和使用 `CREATE FUNCTION` 定义的函数。"
weight: 260
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-proc.md"
---

此表不仅包含普通函数的数据，还包含聚合函数和窗口函数的数据。如果 `proisagg` 为真，`pg_aggregate` 中应有对应的行。

对于编译型函数，无论是内置函数还是动态加载的函数，`prosrc` 都包含函数的 C 语言名称（链接符号）。对于目前已知的其他所有语言类型，`prosrc` 包含函数的源文本。除动态加载的 C 函数外，`probin` 不使用；对于动态加载的 C 函数，它给出包含该函数的共享库文件名。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性，必须显式选择）。|
|`proname`|name| |函数名称。|
|`pronamespace`|oid|pg_namespace.oid|包含此函数的名字空间的 OID。|
|`proowner`|oid|pg_authid.oid|函数的所有者。|
|`prolang`|oid|pg_language.oid|函数的实现语言或调用接口。|
|`procost`|real| |估算的执行代价（以 cpu_operator_cost 为单位）；如果 `proretset` 为 `true`，则表示每个返回行的代价。|
|`prorows`|real| |估算的结果行数（若非 `proretset`，则为零）。|
|`provariadic`|oid|pg_type.oid|可变参数数组中元素的数据类型；如果函数没有可变参数，则为零。|
|`prosupport`|regproc|pg_proc.oid|此函数的规划器支持函数。|
|`prokind`|char| |`f` 表示普通函数，`p` 表示过程，`a` 表示聚合函数，`w` 表示窗口函数。|
|`prosecdef`|boolean| |函数以定义者的权限执行（例如 'setuid' 函数）。|
|`proleakproof`|boolean| |函数没有副作用，除了返回值之外，不会泄露任何有关参数的信息。任何可能因参数值而抛出错误的函数都不是防泄漏函数。|
|`proisstrict`|boolean| |只要任一调用参数为 NULL，函数就返回 NULL，此时实际上根本不会调用该函数。非严格函数必须能够处理 NULL 输入。|
|`proretset`|boolean| |函数返回集合（指定数据类型的多个值）。|
|`provolatile`|char| |指示函数结果是否仅取决于输入参数，还是受外部因素影响。`i` = *不可变*（相同输入始终得到相同结果），`s` = *稳定*（给定输入的结果在一次扫描期间不会改变），`v` = *易失*（结果可能随时改变，或函数有副作用）。|
|`proparallel`|char| |指示函数能否安全地在并行后端中运行，还是只能在非并行模式下运行。||
|`pronargs`|smallint| |参数个数。|
|`pronargdefaults`|smallint| |具有默认值的参数个数。|
|`prorettype`|oid|pg_type.oid|返回值的数据类型；对于过程，则为 NULL。|
|`proargtypes`|ARRAY|pg_type.oid|包含函数参数数据类型的数组。它只包含输入参数（包括 `INOUT` 和 `VARIADIC` 参数），因此表示函数的调用签名。|
|`proallargtypes`|ARRAY|pg_type.oid|包含函数参数数据类型的数组。它包含所有参数（包括 `OUT` 和 `INOUT` 参数）；但如果所有参数都是 `IN` 参数，此字段为 NULL。注意，此数组下标从 1 开始，而由于历史原因，`proargtypes` 的下标从 0 开始。|
|`proargmodes`|ARRAY| |包含函数参数模式的数组：`i` = `IN`，`o` = `OUT`，`b` = `INOUT`，`v` = `VARIADIC`。如果所有参数都是 IN 参数，此字段为 NULL。注意，下标对应 `proallargtypes` 中的位置，而非 `proargtypes` 中的位置。|
|`proargnames`|ARRAY| |包含函数参数名称的数组。未命名的参数在数组中表示为空字符串。如果所有参数都没有名称，此字段为 NULL。注意，下标对应 `proallargtypes` 中的位置，而非 `proargtypes` 中的位置。|
|`proargdefaults`|pg_node_tree| |参数默认值的表达式树（以 `nodeToString()` 表示）。这是一个包含 `pronargdefaults` 个元素的列表，对应最后 N 个输入参数（即 `proargtypes` 中最后 N 个位置）。如果没有参数具有默认值，此字段为 NULL。|
|`protrftypes`|ARRAY| |需要应用转换的类型。|
|`prosrc`|text| |告诉函数处理器如何调用函数。根据实现语言和调用约定，它可能是解释型语言函数的实际源代码、链接符号、文件名或其他任何内容。|
|`probin`|text| |有关如何调用函数的附加信息，其解释方式同样取决于语言。|
|`prosqlbody`|pg_node_tree| |如果 `prolang` 为 `sql`，且 `prokind` 不是 `a`（例如，它是普通函数或过程，而不是聚合函数），此字段包含函数或过程预先解析的 SQL 函数体。这主要供数据库内部使用。对于使用其他语言的函数，此字段为 NULL。|
|`proconfig`|ARRAY| |函数对运行时配置变量的局部设置。|
|`proacl`|ARRAY| |由 `GRANT`/`REVOKE` 指定的函数访问权限。|
|`prodataaccess`|char| |指示函数的 SQL 数据访问模式。可能的值为：`c` = CONTAINS SQL，`n` = NO SQL，`r` = READS SQL DATA，`m` = MODIFIES SQL DATA。|
|`proexeclocation`|char| |调用函数时的执行位置：`m` — 仅在 Coordinator 上，`a` — 任意 Segment 实例，`s` — 所有 Segment 实例，`i` — initplan。|
