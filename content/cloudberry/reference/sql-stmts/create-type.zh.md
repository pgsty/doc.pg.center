---
title: "CREATE TYPE"
description: "定义新的数据类型。"
weight: 910
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-type.md"
---

## 语法概要 {#synopsis}

```sql
CREATE TYPE <name> AS 
    ( [ <attribute_name> <data_type> [ COLLATE <collation> ] [, ... ] ] )

CREATE TYPE <name> AS ENUM 
    ( [ '<label>' [, ... ] ] )

CREATE TYPE <name> AS RANGE (
    SUBTYPE = <subtype>
    [ , SUBTYPE_OPCLASS = <subtype_operator_class> ]
    [ , COLLATION = <collation> ]
    [ , CANONICAL = <canonical_function> ]
    [ , SUBTYPE_DIFF = <subtype_diff_function> ]
)

CREATE TYPE <name> (
    INPUT = <input_function>,
    OUTPUT = <output_function>
    [, RECEIVE = <receive_function>]
    [, SEND = <send_function>]
    [, TYPMOD_IN = <type_modifier_input_function> ]
    [, TYPMOD_OUT = <type_modifier_output_function> ]
    [, ANALYZE = <analyze_function>]
    [, INTERNALLENGTH = {<internallength> | VARIABLE}]
    [, PASSEDBYVALUE]
    [, ALIGNMENT = <alignment>]
    [, STORAGE = <storage>]
    [, LIKE = <like_type>
    [, CATEGORY = <category>]
    [, PREFERRED = <preferred>]
    [, DEFAULT = <default>]
    [, ELEMENT = <element>]
    [, DELIMITER = <delimiter>]
    [, COLLATABLE = <collatable>]
    [, COMPRESSTYPE = <compression_type>]
    [, COMPRESSLEVEL = <compression_level>]
    [, BLOCKSIZE = <blocksize>] )

CREATE TYPE <name>
```

## 说明 {#description}

`CREATE TYPE` 注册一个可在当前数据库中使用的新数据类型。定义类型的用户成为其所有者。

如果给出模式名，则在指定模式中创建类型，否则在当前模式中创建。类型名必须不同于同一模式中已有的任何类型或域的名称，也必须不同于同一模式中已有表的名称。

`CREATE TYPE` 有五种形式，如上面的语法概要所示，分别创建*复合类型*、*枚举类型*、*范围类型*、*基础类型*或*壳类型*。前四种将在下文依次说明。壳类型只是稍后要定义的类型的占位符；执行只带类型名、不带其他参数的 `CREATE TYPE` 即可创建。创建范围类型和基础类型时需要用壳类型进行前向引用，相关小节将进一步说明。

**复合类型**

第一种 `CREATE TYPE` 形式创建复合类型。复合类型由属性名称和数据类型列表定义。如果属性的数据类型支持排序规则，还可以指定属性的排序规则。复合类型本质上与表的行类型相同，但如果只想定义类型，使用 `CREATE TYPE` 就无须创建实际的表。例如，独立的复合类型可用作函数的参数类型或返回类型。

创建复合类型需要对所有属性类型具有 `USAGE` 权限。

**枚举类型**

第二种 `CREATE TYPE` 形式创建枚举（`ENUM`）类型，详见 PostgreSQL 文档中的[枚举类型](https://www.postgresql.org/docs/12/datatype-enum.html)。`ENUM` 类型接受一个用引号括起的标签列表，每个标签的长度必须小于 `NAMEDATALEN` 字节（64）。

可以创建没有标签的枚举类型，但在通过 [ALTER TYPE](/cloudberry/reference/sql-stmts/alter-type/) 添加至少一个标签之前，该类型不能用于保存值。

**范围类型**

第三种 `CREATE TYPE` 形式创建新的范围类型，详见“范围类型”。

范围类型的子类型可以是任何具有关联 B-树 操作符类的类型（该操作符类用于确定范围类型中值的顺序）。通常使用子类型默认的 B-树 操作符类确定顺序；要使用非默认操作符类，请通过 subtype_opclass 指定其名称。如果子类型支持排序规则，并希望在范围排序中使用非默认规则，请通过 collation 选项指定所需排序规则。

可选的 canonical 函数必须接受一个正在定义的范围类型的参数，并返回同一类型的值。它用于在适用时将范围值转换为规范形式。更多信息请参阅“定义新的范围类型”。创建规范化函数有些棘手，因为必须先定义它，才能声明范围类型。为此，必须先创建壳类型：它是一个只有名称和所有者、没有其他属性的占位类型。执行不带其他参数的 `CREATE TYPE name` 命令即可。然后用壳类型作为参数和结果类型声明函数，最后再用同一名称声明范围类型。这会自动用有效的范围类型替换壳类型条目。

可选的 subtype_diff_function 必须接受两个子类型值作为参数，并返回表示这两个给定值之差的 double precision 值。虽然它是可选的，但提供此函数可以大幅提高范围类型列上 GiST 索引的效率。更多信息请参阅“定义新的范围类型”。

**基础类型**

第四种 `CREATE TYPE` 形式创建新的基础类型（标量类型）。只有超级用户才能创建新的基础类型。（此限制是因为错误的类型定义可能扰乱服务器，甚至使其崩溃。）

参数可以按任意顺序出现，不限于语法中显示的顺序，而且大多数参数是可选的。定义类型之前，必须先注册两个或更多函数（使用 `CREATE FUNCTION`）。支持函数 input_function 和 output_function 是必需的，而 receive_function、send_function、type_modifier_input_function、type_modifier_output_function 和 analyze_function 是可选的。这些函数通常必须用 C 或其他底层语言编写。在 Apache Cloudberry 中，任何用于实现数据类型的函数都必须定义为 `IMMUTABLE`。

input_function 将类型的外部文本表示转换为该类型操作符和函数使用的内部表示。output_function 执行相反的转换。输入函数可以声明为接受一个 `cstring` 类型参数，也可以接受类型分别为 `cstring`、`oid`、`integer` 的三个参数。第一个参数是作为 C 字符串的输入文本；第二个参数是类型自身的 OID（数组类型除外，它接收的是元素类型的 OID）；第三个参数是目标列的 `typmod`（如果已知，否则传入 `-1`）。输入函数必须返回该数据类型自身的值。通常应将输入函数声明为 `STRICT`；否则，在读取 `NULL` 输入值时，会以 `NULL` 作为第一个参数调用它。此时，除非报错，函数仍必须返回 `NULL`。（此情况主要用于支持域的输入函数，因为它们可能需要拒绝 `NULL` 输入。）输出函数必须声明为接受一个新数据类型的参数，并返回 `cstring` 类型。对于 `NULL` 值，不会调用输出函数。

可选的 receive_function 将类型的外部二进制表示转换为内部表示。如果不提供此函数，该类型就不能用于二进制输入。选择二进制表示时，应兼顾转换为内部形式的低开销和合理的可移植性。（例如，标准整数数据类型使用网络字节序作为外部二进制表示，而内部表示使用机器的本机字节序。）接收函数应执行充分的检查，确保值有效。接收函数可以声明为接受一个 `internal` 类型参数，也可以接受类型分别为 `internal`、`oid`、`integer` 的三个参数。第一个参数是指向保存所接收字节串的 `StringInfo` 缓冲区的指针；可选参数与文本输入函数相同。接收函数必须返回该数据类型自身的值。通常应将接收函数声明为 `STRICT`；否则，在读取 NULL 输入值时，会以 `NULL` 作为第一个参数调用它。此时，除非报错，函数仍必须返回 `NULL`。（此情况主要用于支持域的接收函数，因为它们可能需要拒绝 `NULL` 输入。）类似地，可选的 send_function 将内部表示转换为外部二进制表示。如果不提供此函数，该类型就不能用于二进制输出。发送函数必须声明为接受一个新数据类型的参数，并返回 `bytea` 类型。对于 `NULL` 值，不会调用发送函数。

输入和输出函数必须先于新类型创建，那么如何将其结果或参数声明为新类型？应先将类型定义为壳类型，也就是只有名称和所有者、没有其他属性的占位类型。执行不带其他参数的 `CREATE TYPE name` 命令即可。然后可以引用壳类型定义 I/O 函数。最后，用包含完整定义的 `CREATE TYPE` 将壳条目替换为完整有效的类型定义，此后即可正常使用新类型。

如果类型支持修饰符，就需要可选的 type_modifier_input_function 和 type_modifier_output_function。修饰符是附加在类型声明上的可选约束，例如 `char(5)` 或 `numeric(30,2)`。虽然 Apache Cloudberry 允许用户定义类型接受一个或多个简单常量或标识符作为修饰符，但这些信息必须能编码为单个非负整数，才能存储在系统目录中。Apache Cloudberry 以 `cstring` 数组的形式将声明的修饰符传给 type_modifier_input_function。修饰符输入函数必须检查值是否有效，无效时抛出错误。值有效时，修饰符输入函数返回一个非负整数，Apache Cloudberry 将其保存为列的 `typmod`。如果定义类型时未提供 type_modifier_input_function，就不允许使用类型修饰符。type_modifier_output_function 将内部整数 `typmod` 值转换回适合向用户显示的形式。修饰符输出函数必须返回 `cstring` 值，即要原样追加到类型名称后的字符串。例如，`numeric` 的函数可能返回 `(30,2)`。type_modifier_output_function 是可选的；未指定时，默认显示格式为用括号括起的已存储 `typmod` 整数值。

可选的 analyze_function 为该数据类型的列收集类型专用的统计信息。默认情况下，如果类型有默认 B-树 操作符类，`ANALYZE` 会尝试使用该类型的“等于”和“小于”操作符收集统计信息。对于非标量类型，这种行为可能不合适，因此可以指定自定义分析函数覆盖它。分析函数必须声明为接受一个 `internal` 类型参数，并返回 `boolean` 结果。

虽然新类型内部表示的细节只需由 I/O 函数及为该类型创建的其他函数了解，但仍必须向 Apache Cloudberry 声明内部表示的若干属性。最重要的是 internallength。基础数据类型可以是定长的，此时 internallength 为正整数；也可以是变长的，此时将 internallength 设为 `VARIABLE`。（内部通过将 `typlen` 设为 `-1` 来表示。）所有变长类型的内部表示都必须以一个 4 字节整数开头，该整数给出此类型值的总长度。

可选标志 `PASSEDBYVALUE` 表示该数据类型的值按值传递，而不是按引用传递。如果类型的内部表示大于 `Datum` 类型的大小（多数机器上为 4 字节，少数机器上为 8 字节），就不能按值传递。

alignment 参数指定数据类型所需的存储对齐方式。允许值分别对应 1、2、4 或 8 字节边界对齐。注意，变长类型的对齐要求至少为 4，因为其第一个组成部分必然是 `int4`。

storage 参数用于选择变长数据类型的存储策略。（定长类型只允许 `plain`。）`plain` 指定该类型数据始终存储在行内且不压缩。`extended` 指定系统先尝试压缩较长的数据值，如果仍然过长，则将其移出主表行。`external` 允许将值移出主表，但系统不会尝试压缩。`main` 允许压缩，但尽量避免将值移出主表。（如果无法通过其他方式让一行容纳得下，采用此策略的数据项仍可能被移出主表，但相较于 `extended` 和 `external` 数据项，会优先将其保留在主表中。）

除 `plain` 之外的所有 storage 值都意味着该数据类型的函数能够处理经过 TOAST 的值，详见 PostgreSQL 文档中的 [TOAST](https://www.postgresql.org/docs/12/storage-toast.html) 和 [TOAST 注意事项](https://www.postgresql.org/docs/12/xtypes.html#XTYPES-TOAST)。指定的其他值仅决定可使用 TOAST 的数据类型列的默认 TOAST 存储策略；用户可以通过 `ALTER TABLE SET STORAGE` 为各列选择其他策略。

like_type 参数提供了另一种指定数据类型基本表示属性的方法：从已有类型复制。`internallength`、`passedbyvalue`、`alignment` 和 `storage` 的值都会从指定类型复制。（可以在 `LIKE` 子句之外显式指定某些值来覆盖它们，但通常不建议这样做。）当新类型的底层实现在某种程度上借用了已有类型时，这种指定表示的方法尤其有用。

*category* 和 *preferred* 参数可用于控制 Apache Cloudberry 在存在歧义时采用哪种隐式类型转换。每种数据类型都属于一个以单个 ASCII 字符命名的类别，并且在其类别中要么是“首选”类型，要么不是。如果该规则有助于解析重载函数或操作符，解析器会优先转换为首选类型（但仅限于同一类别中的其他类型）。如果某个类型与任何其他类型之间都没有隐式转换，保留默认设置即可。不过，对于一组存在隐式转换的相关类型，通常可以将它们全部标为同一类别，并选择一两个“最通用”的类型作为该类别的首选类型。当把用户定义类型加入已有的内置类别（例如数值或字符串类型）时，*category* 参数尤其有用。也可以创建完全由用户定义的新类型类别。应选择大写字母以外的任意 ASCII 字符作为此类类别的名称。

如果希望该数据类型的列默认使用空值以外的值，可以指定默认值。使用 `DEFAULT` 关键字指定。（特定列上显式的 `DEFAULT` 子句可以覆盖此默认值。）

要表明类型是数组，请用 `ELEMENT` 关键字指定数组元素类型。例如，要定义 4 字节整数（int4）的数组，请指定 `ELEMENT = int4`。数组类型的更多详情见下文。

可以将 `delimiter` 设为特定字符，以指定由此类型组成的数组在外部表示中各值之间的分隔符。默认分隔符是逗号（,）。注意，分隔符与数组元素类型关联，而不是与数组类型本身关联。

如果可选布尔参数 collatable 为 true，则该类型的列定义和表达式可以通过 `COLLATE` 子句携带排序规则信息。实际使用这些信息需要由操作该类型的函数实现；仅将类型标记为支持排序规则，并不会自动使用排序规则信息。

**数组类型**

每次创建用户定义类型时，Apache Cloudberry 都会自动创建关联的数组类型，其名称是在元素类型名前加下划线，并在必要时截断，以保持长度小于 `NAMEDATALEN` 字节。（如果生成的名称与已有类型名冲突，会重复此过程，直到找到不冲突的名称。）这个隐式创建的数组类型是变长的，使用内置输入和输出函数 `array_in` 与 `array_out`。数组类型会跟随其元素类型的所有者或模式变更，并在元素类型被删除时一并删除。

既然系统会自动生成正确的数组类型，为什么还需要 `ELEMENT` 选项？`ELEMENT` 唯一有用的场景是：正在创建一种定长类型，其内部恰好是若干相同项组成的数组，并且除了为整个类型提供的操作外，还希望允许通过下标直接访问这些项。例如，`point` 类型由两个浮点数表示，分别可以通过 `point[0]` 和 `point[1]` 访问。注意，此功能只适用于内部形式恰好是一系列相同定长字段的定长类型。支持下标的变长类型必须采用 `array_in` 和 `array_out` 使用的通用内部表示。由于历史原因，定长数组类型的下标从零开始，而变长数组从一开始。

## 参数 {#parameters}

**`name`**

要创建的类型名称（可用模式限定）。

**`attribute_name`**

复合类型的属性（列）名称。

**`data_type`**

用作复合类型某列的已有数据类型名称。

**`collation`**

要与复合类型的列或范围类型关联的已有排序规则名称。

**`label`**

表示枚举类型某个值所关联文本标签的字符串字面量。

**`subtype`**

范围类型所表示范围的元素类型名称。

**`subtype_operator_class`**

子类型的 B-树 操作符类名称。

**`canonical_function`**

范围类型的规范化函数名称。

**`subtype_diff_function`**

子类型的差值函数名称。

**`input_function`**

将数据从类型的外部文本形式转换为内部形式的函数名称。

**`output_function`**

将数据从类型的内部形式转换为外部文本形式的函数名称。

**`receive_function`**

将数据从类型的外部二进制形式转换为内部形式的函数名称。

**`send_function`**

将数据从类型的内部形式转换为外部二进制形式的函数名称。

**`type_modifier_input_function`**

将类型修饰符数组转换为内部形式的函数名称。

**`type_modifier_output_function`**

将类型修饰符的内部形式转换为外部文本形式的函数名称。

**`analyze_function`**

对该数据类型执行统计分析的函数名称。

**`internallength`**

指定新类型内部表示长度的数值常量，单位为字节。默认假定为变长。

**`alignment`**

数据类型的存储对齐要求。必须为 `char`、`int2`、`int4` 或 `double` 之一。默认值为 `int4`。

**`storage`**

数据类型的存储策略。必须为 `plain`、`external`、`extended` 或 `main` 之一。默认值为 `plain`。

**`like_type`**

新类型要采用相同表示方式的已有数据类型名称。internallength、passedbyvalue、alignment 和 storage 的值会从该类型复制，除非在此 `CREATE TYPE` 命令的其他位置显式指定值来覆盖。

**`category`**

此类型的类别代码（单个 ASCII 字符）。默认值为 '`U`'，表示用户定义类型。其他标准类别代码可在“`pg_type` 类别代码”中找到。也可以将未使用的 ASCII 字符分配给自己创建的自定义类别。

**`preferred`**

如果此类型是其类型类别中的首选类型，则为 `true`，否则为 `false`。默认值为 `false`。在已有类型类别中创建新的首选类型时应谨慎，这可能导致意外的行为变化。

**`default`**

数据类型的默认值。省略时默认为空值。

**`element`**

正在创建的类型是数组；此参数指定数组元素的类型。

**`delimiter`**

由此类型组成的数组中各值之间使用的分隔字符。

**`collatable`**

如果此类型的操作可以使用排序规则信息，则为 True。默认值为 false。

**`compression_type`**

设为 `ZLIB`（默认值）、`ZSTD` 或 `RLE_TYPE`，以指定此类型的列使用的压缩类型。

**`compression_level`**

对于 Zstd 压缩，可设为 1（压缩最快）到 19（压缩比最高）之间的整数。对于 zlib 压缩，有效范围为 1 到 9。对于 `RLE_TYPE`，压缩级别可设为 1（压缩最快）到 4（压缩比最高）之间的整数。默认压缩级别为 1。

**`blocksize`**

设置列中每个块的大小，单位为字节。`BLOCKSIZE` 必须在 8192 到 2097152 字节之间，且为 8192 的倍数。默认块大小为 32768。

## 注意事项 {#notes}

用户定义类型名不能以下划线（_）开头，且最多只能有 62 个字符（一般为 `NAMEDATALEN - 2`，而其他名称允许 `NAMEDATALEN - 1` 个字符）。以下划线开头的类型名保留给内部创建的数组类型。

Apache Cloudberry 不支持为行类型或复合类型添加存储选项。

表级和列级定义的存储选项会覆盖标量类型定义的默认存储选项。

类型一经创建就不限制其使用，因此创建基础类型或范围类型等同于向所有用户授予类型定义中所列函数的执行权限。（所以要求类型创建者拥有这些函数。）对于适合类型定义的函数，这通常不是问题。但如果类型设计要求在与外部形式相互转换时使用“秘密”信息，就应慎重考虑。

使用 `pg_type.typarray` 可以找到与给定类型关联的数组类型。

## 示例 {#examples}

此例创建复合类型，并在函数定义中使用它：

```sql
CREATE TYPE compfoo AS (f1 int, f2 text);

CREATE FUNCTION getfoo() RETURNS SETOF compfoo AS $$
    SELECT fooid, fooname FROM foo
$$ LANGUAGE SQL;
```

此例创建枚举类型 `mood`，并在表定义中使用它。

```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');
CREATE TABLE person (
    name text,
    current_mood mood
);
INSERT INTO person VALUES ('Moe', 'happy');
SELECT * FROM person WHERE current_mood = 'happy';
 name | current_mood 
------+--------------
 Moe  | happy
(1 row)
```

此例创建范围类型：

```sql
CREATE TYPE float8_range AS RANGE (subtype = float8, subtype_diff = float8mi);
```

此例创建基础数据类型 `box`，然后在表定义中使用它：

```sql
CREATE TYPE box;

CREATE FUNCTION my_box_in_function(cstring) RETURNS box AS 
... ;

CREATE FUNCTION my_box_out_function(box) RETURNS cstring AS 
... ;

CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function
);

CREATE TABLE myboxes (
    id integer,
    description box
);
```

如果 `box` 的内部结构是由四个 `float4` 元素组成的数组，则可以改用：

```sql
CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function,
    ELEMENT = float4
);
```

这样就可以通过下标访问 box 值的各个数值组成部分。该类型的其他行为与之前相同。

此例创建大对象类型，并在表定义中使用它：

```sql
CREATE TYPE bigobj (
    INPUT = lo_filein, OUTPUT = lo_fileout,
    INTERNALLENGTH = VARIABLE
);

CREATE TABLE big_objs (
    id integer,
    obj bigobj
    );
```

## 兼容性 {#compatibility}

`CREATE TYPE` 命令的第一种形式创建复合类型，符合 SQL 标准。其他形式是 Apache Cloudberry 的扩展。SQL 标准中的 `CREATE TYPE` 语句还定义了 Apache Cloudberry 尚未实现的其他形式。

允许创建不含属性的复合类型，是 Apache Cloudberry 对标准的特有偏离（类似于 `CREATE TABLE` 的同类情况）。

## 另请参阅 {#see-also}

[ALTER TYPE](/cloudberry/reference/sql-stmts/alter-type/), [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/), [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [DROP TYPE](/cloudberry/reference/sql-stmts/drop-type/)
