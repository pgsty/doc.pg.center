---
title: "CREATE FUNCTION"
description: "定义一个新函数。"
weight: 630
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-function.md"
---

## 概要 {#synopsis}

```sql
CREATE [OR REPLACE] FUNCTION <name>    
    ( [ [<argmode>] [<argname>] <argtype> [ { DEFAULT | = } <default_expr> ] [, ...] ] )
      [ RETURNS <rettype> 
        | RETURNS TABLE ( <column_name> <column_type> [, ...] ) ]
  { LANGUAGE <lang_name>
    | TRANSFORM { FOR TYPE <type_name> } [, ... ]
    | WINDOW
    | { IMMUTABLE | STABLE | VOLATILE }
    | [ NOT ] LEAKPROOF
    | { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT }
    | { [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER }
    | EXECUTE ON { ANY | COORDINATOR | ALL SEGMENTS | INITPLAN }
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST <execution_cost>
    | ROWS <result_rows>
    | SUPPORT <support_function>
    | SET <configuration_parameter> { TO <value> | = <value> | FROM CURRENT }
    | AS '<definition>'
    | AS '<obj_file>', '<link_symbol>' 
    [ WITH ({ DESCRIBE = <describe_function> } [, ...] ) ]
  } ...
```

## 描述 {#description}

`CREATE FUNCTION` 定义一个新函数。`CREATE OR REPLACE FUNCTION` 要么创建一个新函数，要么替换现有定义。要定义函数，用户必须对该语言具有 `USAGE` 权限。

如果包含模式名，则函数创建在指定的模式中；否则创建在当前模式中。新函数的名称不能与同一模式中具有相同输入参数类型的任何现有函数重名。不过，参数类型不同的函数可以共用同一个名称（重载）。

要更新现有函数的当前定义，请使用 `CREATE OR REPLACE FUNCTION`。不能用这种方式更改函数的名称或参数类型（这样做实际上会创建一个新的、不同的函数）。此外，`CREATE OR REPLACE FUNCTION` 也不允许更改现有函数的返回类型。要更改返回类型，必须删除并重新创建该函数。（使用 `OUT` 参数时，这意味着除非删除该函数，否则不能更改任何 `OUT` 参数的类型。）

当使用 `CREATE OR REPLACE FUNCTION` 替换现有函数时，该函数的所有者和权限不会改变。所有其他函数属性都按命令中指定或隐含的值重新赋值。你必须是该函数的所有者才能替换它（包括是所有者角色的成员）。

如果先删除再重新创建函数，新函数与旧函数不是同一个实体；你必须删除引用旧函数的现有对象（规则、视图、触发器等）。使用 `CREATE OR REPLACE FUNCTION` 可以在不破坏引用该函数的对象的前提下更改函数定义。此外，[ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) 可用于更改现有函数的大多数辅助属性。

创建函数的用户成为该函数的所有者。

要能够创建函数，你必须对参数类型和返回类型具有 `USAGE` 权限。

有关创建函数的更多信息，请参阅 PostgreSQL 文档中的[用户定义函数](https://www.postgresql.org/docs/12/xfunc.html)一节。

**VOLATILE 与 STABLE 函数的使用限制**

为防止数据在 Apache Cloudberry 的各个 Segment 之间失去同步，任何被归类为 `STABLE` 或 `VOLATILE` 的函数，只要包含 SQL 或以任何方式修改数据库，就不能在 Segment 层面运行。例如，`random()` 或 `timeofday()` 之类的函数不允许在 Apache Cloudberry 中对分布式数据运行，因为它们可能导致各 Segment 实例之间的数据不一致。

为确保数据一致性，`VOLATILE` 和 `STABLE` 函数可以安全地用在在 Coordinator 上求值并运行的语句中。例如，下列语句（没有 `FROM` 子句的语句）总是在 Coordinator 上运行：

```sql
SELECT setval('myseq', 201);
SELECT foo();
```

如果语句带有包含分布表的 `FROM` 子句，而 `FROM` 子句中使用的函数只是返回一组行，则可能允许在 Segment 上执行：

```sql
SELECT * FROM foo();
```

此规则的一个例外是返回表引用（`rangeFuncs`）的函数，或使用 `refCursor` 数据类型的函数。请注意，在 Apache Cloudberry 中，任何种类的函数都不能返回 `refcursor`。

**函数易变性与 EXECUTE ON 属性**

易变性属性（`IMMUTABLE`、`STABLE`、`VOLATILE`）和 `EXECUTE ON` 属性指定函数执行的两个不同方面。一般而言，易变性表示函数在何时运行，而 `EXECUTE ON` 表示函数在何处运行。

例如，用 `IMMUTABLE` 属性定义的函数可以在查询规划时运行，而带有 `VOLATILE` 属性的函数必须对查询中的每一行运行。带有 `EXECUTE ON COORDINATOR` 属性的函数只在 Coordinator Segment 上运行，带有 `EXECUTE ON ALL SEGMENTS` 属性的函数则在所有主 Segment 实例上运行（不包括 Coordinator）。

**函数与复制表**

只对复制表运行 `SELECT` 命令的用户定义函数可以在 Segment 上运行。使用 `DISTRIBUTED REPLICATED` 子句创建的复制表会在每个 Segment 上存储其全部行。函数在 Segment 上读取这些表是安全的，但对复制表的更新必须在 Coordinator 实例上运行。

## 参数 {#parameters}

**`name`**

要创建的函数的名称（可以是模式限定的）。

**`argmode`**

参数的模式：`IN`、`OUT`、`INOUT` 或 `VARIADIC`。如果省略，默认为 `IN`。只有 `OUT` 参数可以跟在声明为 `VARIADIC` 的参数之后。此外，`OUT` 和 `INOUT` 参数不能与 `RETURNS TABLE` 记法一起使用。

**`argname`**

参数的名称。某些语言（目前仅 SQL 和 PL/pgSQL）允许在函数体中使用该名称。对于其他语言，就函数本身而言，输入参数的名称只是额外的说明文档；但你可以在调用函数时使用输入参数名来提高可读性。无论如何，输出参数的名称都很重要，因为它定义了结果行类型中的列名。（如果省略输出参数的名称，系统会选择一个默认列名。）

**`argtype`**

函数参数的数据类型（可以是模式限定的），如果有参数的话。参数类型可以是基础类型、复合类型或域类型，也可以引用表中某一列的类型。

根据实现语言的不同，也可能允许指定诸如 `cstring` 之类的伪类型。伪类型表示实际的参数类型要么没有被完整指定，要么在普通 SQL 数据类型的集合之外。

写成 `table_name.column_name%TYPE` 即可引用某一列的类型。使用这一特性有时有助于使函数独立于表定义的变化。

**`default_expr`**

在未指定该参数时用作默认值的表达式。该表达式必须能够强制转换为该参数的参数类型。只有输入参数（包括 `INOUT`）可以有默认值。参数列表中跟在带默认值参数之后的每个输入参数也必须有默认值。

**`rettype`**

返回的数据类型（可以是模式限定的）。返回类型可以是基础类型、复合类型或域类型，也可以引用表中某一列的类型。根据实现语言的不同，也可能允许指定诸如 `cstring` 之类的伪类型。如果函数不应返回值，请将返回类型指定为 `void`。

当存在 `OUT` 或 `INOUT` 参数时，可以省略 `RETURNS` 子句。如果写出该子句，它必须与输出参数所隐含的结果类型一致：如果有多个输出参数，则为 `RECORD`；如果只有一个输出参数，则与该输出参数的类型相同。

`SETOF` 修饰符表示函数将返回一组项，而不是单个项。

写成 `table_name.column_name%TYPE` 即可引用某一列的类型。

**`column_name`**

`RETURNS TABLE` 语法中输出列的名称。这实际上是声明具名 `OUT` 参数的另一种方式，只不过 `RETURNS TABLE` 还隐含了 `RETURNS SETOF`。

**`column_type`**

`RETURNS TABLE` 语法中输出列的数据类型。

**`lang_name`**

实现该函数所用语言的名称。可以是 `SQL`、`C`、`internal`，或用户定义的过程语言的名称，例如 `plpgsql`。用单引号括起名称的写法已被弃用，并且要求大小写匹配。

**`TRANSFORM { FOR TYPE type_name } [, ... ] }`**

列出对该函数的调用应应用哪些转换。转换用于在 SQL 类型与语言特定的数据类型之间进行转换。过程语言实现通常把有关内置类型的知识硬编码在代码中，因此不需要在此列出这些类型。如果某个过程语言实现不知道如何处理某种类型，并且没有提供转换，它将回退到默认的数据类型转换行为，但这取决于具体实现。

**`WINDOW`**

`WINDOW` 表示该函数是窗口函数，而不是普通函数。目前这仅对用 C 编写的函数有用。替换现有函数定义时，不能更改 `WINDOW` 属性。

**`IMMUTABLE`**<br />
**`STABLE`**<br />
**`VOLATILE`**

这些属性向查询优化器说明函数的行为。最多只能指定其中一个。如果这些属性都没有出现，则默认假定为 `VOLATILE`。由于 Apache Cloudberry 目前对 `VOLATILE` 函数的使用有限制，如果函数确实是 `IMMUTABLE` 的，就必须作此声明，才能不受限制地使用它。

`IMMUTABLE` 表示该函数不能修改数据库，并且在给定相同参数值时总是返回相同的结果。它不做数据库查找，也不以其他方式使用未直接出现在其参数列表中的信息。如果给出此选项，则任何参数全为常量的函数调用都可以立即被函数值替换。

`STABLE` 表示该函数不能修改数据库，并且在一次表扫描内，对相同的参数值会一致地返回相同的结果，但其结果可能在不同 SQL 语句之间发生变化。这适用于结果依赖于数据库查找、参数变量（例如当前时区）等的函数。另请注意，`current_timestamp()` 函数族属于稳定函数，因为它们的值在一个事务内不会改变。

`VOLATILE` 表示函数值即使在一次表扫描内也可能改变，因此不能进行任何优化。从这个意义上说，易变的数据库函数相对较少，例如 `random()`、`timeofday()`。但请注意，任何有副作用的函数都必须归类为易变的，即使其结果相当可预测，也是如此，以防止对它的调用被优化掉；例如 `setval()`。

**`LEAKPROOF`**

`LEAKPROOF` 表示该函数没有副作用。除了通过返回值之外，它不会泄露有关其参数的任何信息。例如，对某些参数值抛出错误消息而对另一些不抛出的函数，或者在任何错误消息中包含参数值的函数，都不是防泄漏的。这会影响系统如何对用 `security_barrier` 选项创建的视图或启用了行级安全的表执行查询。为防止数据被无意暴露，系统会先强制执行安全策略和安全屏障视图中的条件，再执行查询本身中包含非防泄漏函数的用户提供的条件。被标记为防泄漏的函数和操作符被认为是可信的，可以先于安全策略和安全屏障视图中的条件执行。此外，不接受参数的函数，或者没有从安全屏障视图或表中获得任何参数的函数，即使没有标记为防泄漏，也可以先于安全条件执行。参见 [CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/)。此选项只能由超级用户设置。

**`CALLED ON NULL INPUT`**<br />
**`RETURNS NULL ON NULL INPUT`**<br />
**`STRICT`**

`CALLED ON NULL INPUT`（默认值）表示当某些参数为空值时，函数仍会被正常调用。此时由函数作者负责在必要时检查空值并作出适当响应。

`RETURNS NULL ON NULL INPUT` 或 `STRICT` 表示只要任何参数为空值，函数总是返回空值。如果指定了此参数，则存在空值参数时不会运行该函数，而是自动假定结果为空值。

**`[EXTERNAL] SECURITY INVOKER`**<br />
**`[EXTERNAL] SECURITY DEFINER`**

`SECURITY INVOKER`（默认值）表示函数以调用它的用户的权限运行。

`SECURITY DEFINER` 指定函数以创建它的用户的权限运行。

为符合 SQL，允许使用关键字 `EXTERNAL`，但它是可选的，因为与 SQL 不同，这一特性适用于所有函数，而不仅仅是外部函数。

**`EXECUTE ON ANY`**<br />
**`EXECUTE ON COORDINATOR`**<br />
**`EXECUTE ON ALL SEGMENTS`**<br />
**`EXECUTE ON INITPLAN`**

`EXECUTE ON` 属性指定函数在查询执行过程中被调用时在何处（Coordinator 还是 Segment 实例）运行。

`EXECUTE ON ANY`（默认值）表示函数可以在 Coordinator 或任一 Segment 实例上运行，且无论在何处运行，都返回相同的结果。函数在何处运行由 Apache Cloudberry 决定。

`EXECUTE ON COORDINATOR` 表示函数必须只在 Coordinator 实例上运行。

`EXECUTE ON ALL SEGMENTS` 表示每次调用时，函数都必须在所有主 Segment 实例上运行，但不在 Coordinator 上运行。函数的总体结果是所有 Segment 实例结果的 `UNION ALL`。

`EXECUTE ON INITPLAN` 表示函数包含一条向 Segment 实例派发查询的 SQL 命令，在可能的情况下，需要 Apache Cloudberry 在 Coordinator 实例上进行特殊处理。

> **注意** `EXECUTE ON INITPLAN` 仅支持用在 `CREATE TABLE AS` 或 `INSERT` 命令的 `FROM` 子句中的函数，例如下列命令中的 `get_data()` 函数。

```sql
CREATE TABLE t AS SELECT * FROM get_data();

INSERT INTO t1 SELECT * FROM get_data();
```

Apache Cloudberry 不支持在查询的 `WITH` 子句（即 CTE，公共表表达式）中使用的函数带有 `EXECUTE ON INITPLAN` 属性。例如，在下面这个 CTE 中为函数 `get_data()` 指定 `EXECUTE ON INITPLAN` 是不受支持的。

```sql
WITH tbl_a AS (SELECT * FROM get_data() )
    SELECT * from tbl_a
    UNION
    SELECT * FROM tbl_b;
```

有关使用 `EXECUTE ON` 属性的信息，请参见[注解](#notes)。

**`PARALLEL`**

`PARALLEL UNSAFE` 表示函数不能在并行模式下执行，SQL 语句中只要出现这样的函数就会强制使用串行执行计划。这是默认值。`PARALLEL RESTRICTED` 表示函数可以在并行模式下执行，但执行仅限于并行组领导者。`PARALLEL SAFE` 表示函数可以在并行模式下不受限制地安全运行。

如果函数会修改任何数据库状态，或者会对事务做出更改（例如使用子事务），或者会访问序列或试图对设置做持久性更改（例如 `setval()`），则应将其标记为并行不安全。如果函数访问临时表、客户端连接状态、游标、预备语句，或系统无法在并行模式下同步的其他后端本地状态，则应将其标记为并行受限（例如，`setseed()` 只能由组领导者执行，因为其他进程所做的更改不会反映在领导者中）。一般来说，如果函数实际上是受限或不安全的却被标记为安全，或者实际上是不安全的却被标记为受限，那么在并行查询中使用它时可能会抛出错误或产生错误的结果。C 语言函数若被错误标记，理论上可能表现出完全未定义的行为，因为系统无法保护自己免受任意 C 代码的影响，但在大多数情况下，结果不会比其他函数更糟。如果拿不准，应将函数标记为 `UNSAFE`，这也是默认值。

**`COST execution_cost`**

一个正数，指明该函数的估计执行代价，单位为 [cpu_operator_cost](https://www.postgresql.org/docs/12/runtime-config-query.html)。如果函数返回一个集合，execution_cost 指明的是每个返回行的代价。如果未指定代价，C 语言函数和内部函数默认为 1 个单位，其他语言的函数默认为 100 个单位。较大的值会使规划器尽量避免对该函数进行不必要的频繁求值。

**`ROWS result_rows`**

一个正数，给出规划器应预计该函数返回的估计行数。只有在函数被声明为返回集合时才允许使用。默认假定为 1000 行。

**`SUPPORT support_function`**

用于此函数的规划器支持函数的名称（可以是模式限定的）。使用此选项必须是超级用户。

**`configuration_parameter`**<br />
**`value`**

`SET` 子句在进入函数时把一个值应用于会话配置参数，并在函数退出时将该配置参数恢复为先前的值。`SET FROM CURRENT` 把运行 `CREATE FUNCTION` 时该参数的当前值保存下来，作为进入函数时要应用的值。

如果函数附带了 `SET` 子句，那么在函数内部针对同一变量执行的 `SET LOCAL` 命令，其效果被限制在该函数内：函数退出时，配置参数先前的值仍会被恢复。不过，普通的 `SET` 命令（不带 `LOCAL`）会覆盖 `SET` 子句，就像它会覆盖先前的 `SET LOCAL` 命令一样：除非当前事务被回滚，否则这类命令的效果会在函数退出后继续保持。

有关允许的参数名称和取值的更多信息，请参见 [SET](/cloudberry/reference/sql-stmts/set/)。

**`definition`**

一个定义该函数的字符串常量；其含义取决于所用语言。它可以是内部函数名称、对象文件的路径、SQL 命令，或用过程语言编写的文本。

使用美元引用（参见 PostgreSQL 文档中的[美元引用的字符串常量](https://www.postgresql.org/docs/12/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING)）来书写函数定义字符串，通常比使用普通的单引号语法更有帮助。如果不使用美元引用，函数定义中的任何单引号或反斜线都必须通过双写来转义。

**`obj_file, link_symbol`**

当 C 语言源代码中的函数名与 SQL 函数的名称不同时，这种形式的 `AS` 子句用于动态可加载的 C 语言函数。字符串 obj_file 是包含动态可加载对象的文件名，其解释方式与 [LOAD](/cloudberry/reference/sql-stmts/load/) 命令相同。字符串 link_symbol 是函数在 C 语言源代码中的名称。如果省略链接符号，则假定它与正在定义的 SQL 函数名称相同。所有函数的 C 名称都必须不同，因此必须为重载的 SQL 函数指定不同的 C 名称（例如，把参数类型作为 C 名称的一部分）。

当重复的 `CREATE FUNCTION` 调用引用同一个对象文件时，该文件在每个会话中只加载一次。要卸载并重新加载该文件（例如在开发期间），请启动一个新会话。

将共享库放在相对于 `$libdir`（位于 `$GPHOME/lib`）的位置，或通过动态库路径（由 `dynamic_library_path` 服务器配置参数设置）来定位共享库，会使新安装位于不同位置时的版本升级更为简单。

**`describe_function`**

在解析调用此函数的查询时要运行的回调函数的名称。该回调函数返回一个指明结果类型的元组描述符。

## 重载 {#overloading}

Apache Cloudberry 允许函数重载；也就是说，只要输入参数类型不同，同一个名称就可以用于多个不同的函数。无论你是否使用这一能力，在某些用户不信任其他用户的数据库中调用函数时，都需要采取安全预防措施；更多信息请参阅 PostgreSQL 文档中的[函数](https://www.postgresql.org/docs/12/typeconv-func.html)。

如果两个函数具有相同的名称和输入参数类型（不考虑任何 `OUT` 参数），则认为它们是同一个函数。因此，例如下面这些声明会冲突：

```sql
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, out text) ...
```

参数类型列表不同的函数在创建时不会被视为冲突，但如果提供了默认值，则在使用时可能发生冲突。例如，考虑：

```sql
CREATE FUNCTION foo(int) ...
CREATE FUNCTION foo(int, int default 42) ...
```

调用 `foo(10)` 会失败，因为无法确定应该调用哪个函数。

## 注解 {#notes}

自定义函数的任何已编译代码（共享库文件）都必须放在 Apache Cloudberry 集群中每台主机（Coordinator 和所有 Segment）上的相同位置。该位置还必须在 `LD_LIBRARY_PATH` 中，以便服务器能够找到这些文件。建议在 Apache Cloudberry 集群的所有 Coordinator Segment 实例上，将共享库放在相对于 `$libdir`（位于 `$GPHOME/lib`）的位置，或通过动态库路径（由 `dynamic_library_path` 服务器配置参数设置）来定位。

输入参数和返回值允许使用完整的 SQL 类型语法。不过，`CREATE FUNCTION` 会丢弃带圆括号的类型修饰符（例如 `numeric` 类型的精度字段）。因此，例如 `CREATE FUNCTION foo (varchar(10)) ...` 与 `CREATE FUNCTION foo (varchar) ...` 完全等同。

用 `CREATE OR REPLACE FUNCTION` 替换现有函数时，更改参数名称受到限制。不能更改已经分配给任何输入参数的名称（但可以给先前没有名称的参数补上名称）。如果输出参数多于一个，也不能更改输出参数的名称，因为那样会改变描述函数结果的匿名复合类型的列名。这些限制是为了确保函数被替换时，对该函数的现有调用不会停止工作。

如果函数被声明为带有 `VARIADIC` 参数的 `STRICT` 函数，则严格性检查测试的是可变参数数组作为一个整体是否非空。如果该数组含有空值元素，仍会调用该函数。

**对分布式数据的查询中使用函数**

在某些情况下，如果 `FROM` 子句中指定的表的数据分布在 Apache Cloudberry 的各个 Segment 上，Apache Cloudberry 不支持在查询中使用函数。例如，下面这条 SQL 查询包含函数 `func()`：

```sql
SELECT func(a) FROM table1;
```

如果同时满足以下所有条件，则不支持在该查询中使用该函数：

- 表 `table1` 的数据分布在 Apache Cloudberry 的各个 Segment 上。
- 函数 `func()` 读取或修改分布表中的数据。
- 函数 `func()` 返回多于一行，或者接受一个来自 `table1` 的参数（`a`）。

如果有任何一个条件不满足，则该函数是受支持的。具体来说，只要下列任一条件成立，该函数就是受支持的：

- 函数 `func()` 不访问分布表中的数据，或者访问的数据只位于 Apache Cloudberry Coordinator 上。
- 表 `table1` 是仅位于 Coordinator 的表。
- 函数 `func()` 只返回一行，并且只接受常量值作为输入参数。如果该函数可以改为不需要输入参数，则它是受支持的。

**使用 EXECUTE ON 属性**

大多数通过运行查询来访问表的函数只能在 Coordinator 上运行。不过，只对复制表运行 `SELECT` 查询的函数可以在 Segment 上运行。如果函数访问哈希分布表或随机分布表，则应使用 `EXECUTE ON COORDINATOR` 属性定义该函数。否则，在复杂查询中使用该函数时，可能返回不正确的结果。没有该属性时，规划器优化可能会认为把函数调用下推到 Segment 实例上是有益的。

用 `EXECUTE ON COORDINATOR` 或 `EXECUTE ON ALL SEGMENTS` 属性定义的函数有以下限制：

- 该函数必须是返回集合的函数。
- 该函数不能出现在查询的 `FROM` 子句中。
- 该函数不能出现在带有 `FROM` 子句的查询的 `SELECT` 列表中。
- 包含该函数的查询会从 GPORCA 回退到 Postgres 规划器。

属性 `EXECUTE ON INITPLAN` 表示函数包含一条向 Segment 实例派发查询的 SQL 命令，需要 Apache Cloudberry 在 Coordinator 实例上进行特殊处理。在可能的情况下，Apache Cloudberry 按以下方式在 Coordinator 实例上处理该函数。

1. 首先，Apache Cloudberry 在 Coordinator 实例上将该函数作为 InitPlan 节点的一部分运行，并暂时保存函数的输出。
2. 然后，在查询计划的 MainPlan 中，该函数在 EntryDB（在 Coordinator 实例上运行的一种特殊查询执行器（QE））中被调用，Apache Cloudberry 返回将函数作为 InitPlan 节点的一部分运行时捕获的数据。该函数不会在 MainPlan 中运行。

这个简单的示例在 CTAS 命令中使用函数 `get_data()`，利用表 `country` 中的数据创建一个表。该函数包含一条从表 `country` 检索数据的 `SELECT` 命令，并使用了 `EXECUTE ON INITPLAN` 属性。

```sql
CREATE TABLE country( 
  c_id integer, c_name text, region int) 
  DISTRIBUTED RANDOMLY;

INSERT INTO country VALUES (11,'INDIA', 1 ), (22,'CANADA', 2), (33,'USA', 3);

CREATE OR REPLACE FUNCTION get_data()
  RETURNS TABLE (
   c_id integer, c_name text
   )
AS $$
  SELECT
    c.c_id, c.c_name
  FROM
    country c;
$$
LANGUAGE SQL EXECUTE ON INITPLAN;

CREATE TABLE t AS SELECT * FROM get_data() DISTRIBUTED RANDOMLY;
```

如果使用 `EXPLAIN ANALYZE VERBOSE` 查看该 CTAS 命令的查询计划，计划会显示该函数是作为 InitPlan 节点的一部分运行的，并且列出的切片之一被标记为 `entry db`。不带该函数的简单 CTAS 命令的查询计划没有 InitPlan 节点，也没有 `entry db` 切片。

如果函数不包含 `EXECUTE ON INITPLAN` 属性，则 CTAS 命令会返回错误 `function cannot execute on a QE slice`。

当函数使用 `EXECUTE ON INITPLAN` 属性时，使用该函数的命令（例如 `CREATE TABLE t AS SELECT * FROM get_data()`）会先把函数的结果收集到 Coordinator Segment 上，然后在插入数据时再把结果重新分布到各个 Segment 实例。如果函数返回大量数据，Coordinator 在收集和重新分布数据时可能成为瓶颈。如果改写该函数，使其在用户定义函数中运行 CTAS 命令，并将表名用作输入参数，性能可能会得到改善。在这个示例中，函数运行一条 CTAS 命令，不需要 `EXECUTE ON INITPLAN` 属性。运行 `SELECT` 命令会使用这个运行 CTAS 命令的函数创建表 `t1`。

```sql
CREATE OR REPLACE FUNCTION my_ctas(_tbl text) RETURNS VOID AS
$$
BEGIN
  EXECUTE format('CREATE TABLE %s AS SELECT c.c_id, c.c_name FROM country c DISTRIBUTED RANDOMLY', _tbl);
END
$$
LANGUAGE plpgsql;

SELECT my_ctas('t1');
```

## 示例 {#examples}

使用 SQL 函数将两个整数相加：

```sql
CREATE FUNCTION add(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
```

在 PL/pgSQL 中使用参数名将一个整数加 1：

```sql
CREATE OR REPLACE FUNCTION increment(i integer) RETURNS 
integer AS $$
        BEGIN
                RETURN i + 1;
        END;
$$ LANGUAGE plpgsql;
```

返回一个包含多个输出参数的记录：

```sql
CREATE FUNCTION dup(in int, out f1 int, out f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

你也可以用一个显式命名的复合类型，以更冗长的方式做同样的事情：

```sql
CREATE TYPE dup_result AS (f1 int, f2 text);

CREATE FUNCTION dup(int) RETURNS dup_result
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

返回多列的另一种方法是使用 `TABLE` 函数：

```sql
CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;

SELECT * FROM dup(42);
```

不过，`TABLE` 函数与前面的示例不同，因为它实际返回的是一组记录，而不只是一条记录。

为 PL/pgSQL 函数增大每个查询默认的 Segment 主机内存：

```sql
CREATE OR REPLACE FUNCTION function_with_query() RETURNS 
SETOF text AS $$
        BEGIN
                RETURN QUERY
                EXPLAIN ANALYZE SELECT * FROM large_table;
        END;
$$ LANGUAGE plpgsql
SET statement_mem='256MB';
```

使用多态类型返回一个 `ENUM` 数组：

```sql
CREATE TYPE rainbow AS ENUM('red','orange','yellow','green','blue','indigo','violet');
CREATE FUNCTION return_enum_as_array( anyenum, anyelement, anyelement ) 
    RETURNS TABLE (ae anyenum, aa anyarray) AS $$
    SELECT $1, array[$2, $3] 
$$ LANGUAGE SQL STABLE;

SELECT * FROM return_enum_as_array('red'::rainbow, 'green'::rainbow, 'blue'::rainbow);
```

这个函数用 `EXECUTE ON ALL SEGMENTS` 定义，以便在所有主 Segment 实例上运行。`SELECT` 命令运行该函数，返回它在每个 Segment 实例上的运行时间。

```sql
CREATE FUNCTION run_on_segs (text) returns setof text as $$
  begin 
    return next ($1 || ' - ' || now()::text ); 
  end;
 $$ language plpgsql VOLATILE EXECUTE ON ALL SEGMENTS;

SELECT run_on_segs('my test');
```

这个函数在 parts 表中查找零件名称。parts 表是复制表，因此该函数既可以在 Coordinator 上运行，也可以在主 Segment 上运行。

```sql
CREATE OR REPLACE FUNCTION get_part_name(partno int) RETURNS text AS
$$
DECLARE
   result text := ' ';
BEGIN
    SELECT part_name INTO result FROM parts WHERE part_id = partno;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

如果在 Coordinator 上运行 `SELECT get_part_name(100);`，该函数在 Coordinator 上运行。（Coordinator 实例会把查询定向到某一个主 Segment。）如果 orders 是分布表，并且你运行下面的查询，则 `get_part_name()` 函数在主 Segment 上运行。

```sql
`SELECT order_id, get_part_name(orders.part_no) FROM orders;`
```

## 安全地编写 security definer 函数 {#writing-security-definer-functions-safely}

由于 `SECURITY DEFINER` 函数以创建它的用户的权限执行，因此必须小心确保该函数不会被滥用。出于安全考虑，应将 `search_path` 设置为排除任何可被不受信任用户写入的模式。这可以防止恶意用户创建对象来遮蔽该函数所使用的对象。在这方面尤其重要的是临时表模式：默认情况下它最先被搜索，而且通常任何人都可以写入。一种安全的安排是强制最后才搜索临时模式。为此，请把 `pg_temp` 写成 `search_path` 中的最后一项。下面这个函数演示了安全的用法：

```sql
CREATE FUNCTION check_password(uname TEXT, pass TEXT)
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
BEGIN
        SELECT  (pwd = $2) INTO passed
        FROM    pwds
        WHERE   username = $1;

        RETURN passed;
END;
$$  LANGUAGE plpgsql
    SECURITY DEFINER
    -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
    SET search_path = admin, pg_temp;
```

早期版本的 Apache Cloudberry 中没有 `SET` 选项，因此较旧的函数可能包含相当复杂的逻辑来保存、设置和恢复 `search_path`。为此目的，使用 `SET` 选项要容易得多。

另一点需要记住的是，默认情况下，新创建的函数会把执行权限授予 `PUBLIC`（更多信息请参见 [GRANT](/cloudberry/reference/sql-stmts/grant/)）。通常你会希望只允许部分用户使用 security definer 函数。为此，必须先撤销默认的 `PUBLIC` 权限，然后有选择地授予 `EXECUTE` 权限。为避免出现新函数对所有人可访问的时间窗口，请在同一个事务中创建该函数并设置权限。例如：

```sql
BEGIN;
CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER;
REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins;
COMMIT;
```

## 兼容性 {#compatibility}

`CREATE FUNCTION` 在 SQL:1999 及更高版本中有定义。Apache Cloudberry 的版本与之类似，但并不完全兼容。这些属性不可移植，可用的各种语言也不可移植。

为与某些其他数据库系统兼容，argmode 可以写在 argname 之前或之后，但只有前一种写法符合标准。

对于参数默认值，SQL 标准只规定了带有 `DEFAULT` 关键字的语法。带 `=` 的语法用于 T-SQL 和 Firebird。

## 另见 {#see-also}

[ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/)、[DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/)、[GRANT](/cloudberry/reference/sql-stmts/grant/)、[LOAD](/cloudberry/reference/sql-stmts/load/)、[REVOKE](/cloudberry/reference/sql-stmts/revoke/)、createlang
