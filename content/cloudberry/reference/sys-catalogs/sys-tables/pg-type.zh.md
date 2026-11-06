---
title: "pg_type"
description: "`pg_type` 系统目录表存储数据类型的信息。"
weight: 430
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-type.md"
---

基本类型（标量类型）使用 `CREATE TYPE` 创建，域使用 `CREATE DOMAIN` 创建。数据库中的每个表都会自动创建一个复合类型，用于表示该表的行结构。也可以使用 `CREATE TYPE AS` 创建复合类型。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |行标识符（隐藏属性；必须显式选择）|
|`typname`|name| |数据类型名称|
|`typnamespace`|oid|pg_namespace.oid|包含此类型的名字空间的 OID|
|`typowner`|oid|pg_authid.oid|类型的所有者|
|`typlen`|smallint| |对于定长类型，`typlen` 是该类型内部表示的字节数。而对于变长类型，`typlen` 为负数。`-1` 表示“varlena”类型（具有长度字的类型），`-2` 表示以空字符结尾的 C 字符串。|
|`typbyval`|boolean| |决定内部例程是按值还是按引用传递此类型的值。如果 `typlen` 不是 1、2 或 4（在 Datum 为 8 字节的机器上还包括 8），`typbyval` 最好为 false。变长类型始终按引用传递。请注意，即使长度允许按值传递，`typbyval` 也可以为 false。|
|`typtype`|char| |`b` 表示基本类型，`c` 表示复合类型，`d` 表示域，`e` 表示枚举类型，`p` 表示伪类型，`r` 表示范围类型。另请参阅 `typrelid` 和 `typbasetype`。|
|`typcategory`|char| |数据类型的任意分类，解析器据此决定优先采用哪些隐式类型转换。|
|`typispreferred`|boolean| |如果此类型在其 `typcategory` 中是首选类型转换目标，则为 true|
|`typisdefined`|boolean| |如果类型已定义，则为 true；如果这是尚未定义的类型的占位条目，则为 false。为 false 时，只有类型名称、名字空间和 OID 可以信赖。|
|`typdelim`|char| |解析数组输入时，用于分隔此类型的两个值的字符。请注意，分隔符与数组元素的数据类型关联，而不是与数组的数据类型关联。|
|`typrelid`|oid|pg_class.oid|如果这是复合类型（参见 `typtype`），此列指向定义相应表的 `pg_class` 条目。（对于独立的复合类型，`pg_class` 条目实际上并不表示表，但仍需要它供该类型的 `pg_attribute` 条目链接。）对于非复合类型，此值为零。|
| `typsubscript` | regproc | pg_proc.oid |此类型的下标处理函数的 OID；如果不支持下标，则为零。|
|`typelem`|oid|pg_type.oid|如果不为 `0`，则标识 `pg_type` 中的另一行。此时，当前类型可以像数组一样使用下标访问，得到类型为 `typelem` 的值。“真正的”数组类型是变长的（`typlen` = `-1`），但某些定长类型（`typlen` > `0`）的 `typelem` 也不为零，例如 `name` 和 `point`。如果定长类型具有 `typelem`，其内部表示就必须仅由若干个 `typelem` 数据类型的值组成，不能包含其他数据。变长数组类型具有由数组子例程定义的头部。|
|`typarray`|oid|pg_type.oid|如果不为 0，则标识 `pg_type` 中的另一行，该行是以此类型为元素类型的“真正的”数组类型。使用 `pg_type.typarray` 可找到与特定类型关联的数组类型。|
|`typinput`|regproc|pg_proc.oid|输入转换函数（文本格式）|
|`typoutput`|regproc|pg_proc.oid|输出转换函数（文本格式）|
|`typreceive`|regproc|pg_proc.oid|输入转换函数（二进制格式）；如果没有，则为 0|
|`typsend`|regproc|pg_proc.oid|输出转换函数（二进制格式）；如果没有，则为 0|
|`typmodin`|regproc|pg_proc.oid|类型修饰符输入函数；如果此类型不支持修饰符，则为 0|
|`typmodout`|regproc|pg_proc.oid|类型修饰符输出函数；为 0 表示使用标准格式|
|`typanalyze`|regproc|pg_proc.oid|自定义 `ANALYZE` 函数；为 0 表示使用标准函数|
|`typalign`|char| |存储此类型的值时所需的对齐方式。这适用于磁盘存储以及 Apache Cloudberry 内部对此值的大多数表示形式。连续存储多个值时（例如磁盘上完整行的表示），会在此类型的数据项之前插入填充，使其从指定边界开始。对齐的参照点是序列中第一个数据项的起始位置。可能的值包括：<br/><br/>`c` = char 对齐（无需对齐）。<br/><br/>`s` = short 对齐（在大多数机器上为 2 字节）。<br/><br/>`i` = int 对齐（在大多数机器上为 4 字节）。<br/><br/>`d` = double 对齐（在许多机器上为 8 字节，但并非所有机器都如此）。|
|`typstorage`|char| |对于 varlena 类型（`typlen` = -1），此字段表示该类型是否支持 TOAST，以及此类型的属性应采用的默认策略。可能的值包括：<br/><br/>`p`：值必须始终按原样存储。<br/><br/>`e`：值可以存储在辅助关系中（如果该关系有辅助关系，参见 `pg_class.reltoastrelid`）。<br/><br/>`m`：值可以压缩后内联存储。<br/><br/>`x`：值可以压缩后内联存储，也可以存放在辅助存储中。<br/><br/>请注意，`m` 列也可以移到辅助存储中，但只能作为最后手段（会先移动 `e` 和 `x` 列）。|
|`typnotnull`|boolean| |表示类型上的非空约束。仅用于域。|
|`typbasetype`|oid|pg_type.oid|标识域所基于的类型。如果此类型不是域，则为零。|
|`typtypmod`|integer| |域使用 `typtypmod` 记录要应用于其基本类型的 `typmod`（如果基本类型不使用 `typmod`，则为 -1）。如果此类型不是域，则为 -1。|
|`typndims`|integer| |基于数组的域的数组维数（如果 `typbasetype` 是数组类型）。对于基于数组类型的域以外的类型，此值为零。|
|`typcollation`|oid|pg_collation.oid|指定类型的排序规则。如果类型不支持排序规则，则为零。对于支持排序规则的基本类型，此值为 `DEFAULT_COLLATION_OID`。对于基于可排序类型的域，如果为其指定了其他排序规则，则可以具有相应的排序规则 OID。|
|`typdefaultbin`|pg_node_tree| |如果非空，则为此类型默认表达式的 `nodeToString()` 表示。仅用于域。|
|`typdefault`|text| |如果类型没有关联的默认值，则为空。如果 `typdefaultbin` 非空，`typdefault` 必须包含 `typdefaultbin` 所表示默认表达式的人类可读版本。如果 `typdefaultbin` 为空而 `typdefault` 非空，则 `typdefault` 是此类型默认值的外部表示，可将其传入此类型的输入转换函数以生成常量。|
|`typacl`|ARRAY| |访问权限；详情参见 [GRANT](/cloudberry/reference/sql-stmts/grant/) 和 [REVOKE](/cloudberry/reference/sql-stmts/revoke/)。|

下表列出系统定义的 `typcategory` 值。今后新增到此列表的值也将使用大写 ASCII 字母。所有其他 ASCII 字符都保留给用户定义的类别。

|代码|类别|
|----|--------|
|A|数组类型|
|B|布尔类型|
|C|复合类型|
|D|日期／时间类型|
|E|枚举类型|
|G|几何类型|
|I|网络地址类型|
|N|数值类型|
|P|伪类型|
|R|范围类型|
|S|字符串类型|
|T|时间跨度类型|
|U|用户定义的类型|
|V|位串类型|
|X|`unknown` 类型|
