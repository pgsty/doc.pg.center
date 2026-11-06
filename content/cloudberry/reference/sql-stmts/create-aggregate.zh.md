---
title: "CREATE AGGREGATE"
description: "定义一个新的聚合函数。"
weight: 530
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-aggregate.md"
---

## 概要 {#synopsis}

```sql
CREATE [ OR REPLACE ] AGGREGATE <name> ( [ <argmode> ] [ <argname> ] <arg_data_type> [ , ... ] ) (
    SFUNC = <sfunc>,
    STYPE = <state_data_type>
    [ , SSPACE = <state_data_size> ]
    [ , FINALFUNC = <ffunc> ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = <combinefunc> ]
    [ , SERIALFUNC = <serialfunc> ]
    [ , DESERIALFUNC = <deserialfunc> ]
    [ , INITCOND = <initial_condition> ]
    [ , MSFUNC = <msfunc> ]
    [ , MINVFUNC = <minvfunc> ]
    [ , MSTYPE = <mstate_data_type> ]
    [ , MSSPACE = <mstate_data_size> ]
    [ , MFINALFUNC = <mffunc> ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = <minitial_condition> ]
    [ , SORTOP = <sort_operator> ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
    [ , REPSAFE = <boolean> ]
  )
  
  CREATE [ OR REPLACE ] AGGREGATE <name> ( [ [ <argmode> ] [ <argname> ] <arg_data_type> [ , ... ] ]
      ORDER BY [ <argmode> ] [ <argname> ] <arg_data_type> [ , ... ] ) (
    SFUNC = <sfunc>,
    STYPE = <state_data_type>
    [ , SSPACE = <state_data_size> ]
    [ , FINALFUNC = <ffunc> ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = <combinefunc> ]
    [ , INITCOND = <initial_condition> ]
    [ , PARALLEL = { SAFE | RESTRICTED | UNSAFE } ]
    [ , REPSAFE = <boolean> ]
    [ , HYPOTHETICAL ]
  )
  -- or the old syntax
  
  CREATE [ OR REPLACE ] AGGREGATE <name> (
    BASETYPE = <base_type>,
    SFUNC = <sfunc>,
    STYPE = <state_data_type>
    [ , SSPACE = <state_data_size> ]
    [ , FINALFUNC = <ffunc> ]
    [ , FINALFUNC_EXTRA ]
    [ , FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , COMBINEFUNC = <combinefunc> ]
    [ , SERIALFUNC = <serialfunc> ]
    [ , DESERIALFUNC = <deserialfunc> ]
    [ , INITCOND = <initial_condition> ]
    [ , MSFUNC = <msfunc> ]
    [ , MINVFUNC = <minvfunc> ]
    [ , MSTYPE = <mstate_data_type> ]
    [ , MSSPACE = <mstate_data_size> ]
    [ , MFINALFUNC = <mffunc> ]
    [ , MFINALFUNC_EXTRA ]
    [ , MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE } ]
    [ , MINITCOND = <minitial_condition> ]
    [ , SORTOP = <sort_operator> ]
    [ , REPSAFE = <boolean> ]
  )
```

## 描述 {#description}

`CREATE AGGREGATE` 定义一个新的聚合函数。`CREATE OR REPLACE AGGREGATE` 要么定义一个新的聚合函数，要么替换现有定义。Apache Cloudberry 已经提供了一些基本且常用的聚合函数，例如 `count()`、`min()`、`max()`、`sum()`、`avg()` 等。如果你定义了新类型，或者需要一个尚未提供的聚合函数，可以使用 `CREATE AGGREGATE` 来提供所需的功能。

替换现有定义时，不得更改参数类型、结果类型和直接参数的数量。此外，新定义必须与旧定义属于同一种类（普通聚集、有序集聚集或假想集聚集）。

如果给出了模式名（例如 `CREATE AGGREGATE myschema.myagg ...`），则该聚合函数会创建在指定的模式中。否则，它会创建在当前模式中。

聚合函数由其名称和输入数据类型标识。如果同一模式中的两个聚合函数作用于不同的输入类型，它们可以同名。聚合函数的名称和输入数据类型还必须不同于同一模式中每个普通函数的名称和输入数据类型。这一行为与普通函数名的重载完全相同。参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

简单的聚合函数由一个或两个普通函数构成：一个状态转移函数 sfunc，以及一个可选的最终计算函数 ffunc。

这些函数的用法如下：

```sql
sfunc( internal-state, next-data-values ) ---> next-internal-state
ffunc( internal-state ) ---> aggregate-value
```

Apache Cloudberry 会创建一个数据类型为 state_data_type 的临时变量，用来保存聚合函数的当前内部状态。对于每个输入行，都会先计算聚集参数值，然后以当前状态值和新的参数值调用状态转移函数，以计算新的内部状态值。所有行处理完毕后，会调用一次最终函数来计算聚集的返回值。如果没有最终函数，则原样返回最终的状态值。

聚合函数可以提供一个初始条件，即内部状态值的初始值。它在数据库中以 `text` 类型的值指定和存储，但必须是状态值数据类型的某个常量的合法外部表示。如果未提供，则状态值初始为空值。

如果状态转移函数被声明为 `STRICT`，则不能用空输入调用它。使用这样的转移函数时，聚集的执行行为如下。任何输入值中含有空值的行都会被忽略（不会调用该函数，并保留之前的状态值）。如果初始状态值为空，则在第一个所有输入值都非空的行上，第一个参数值会取代状态值，并在之后每个所有输入值都非空的行上调用转移函数。这对于实现 `max()` 之类的聚集很有用。注意，只有当 state_data_type 与第一个 arg_data_type 相同时，才有这一行为。当这两种类型不同时，你必须提供非空的初始条件，或者使用非严格的转移函数。

如果状态转移函数没有被声明为 `STRICT`，则每个输入行上都会无条件地调用它，并且它必须自行处理空输入和空状态值。这使聚集的作者能够完全控制聚集对空值的处理方式。

如果最终函数被声明为 `STRICT`，则当最终状态值为空时不会调用它；而是自动返回空结果。（这是 `STRICT` 函数的正常行为。）无论如何，最终函数都可以选择返回空值。例如，`avg()` 的最终函数在发现输入行数为零时会返回空值。

有时，将最终函数声明为不仅接收状态值，还接收与聚集输入值相对应的额外参数，会很有用。这样做的主要原因是：最终函数是多态的，而状态值的数据类型不足以确定结果类型。这些额外参数总是以 `NULL` 传入（因此在使用 `FINALFUNC_EXTRA` 选项时，最终函数不能是严格的），但它们仍然是有效的参数。例如，最终函数可以利用 `get_fn_expr_argtype` 来识别当前调用中的实际参数类型。

聚集可以选择支持*移动聚集模式*，如 PostgreSQL 文档中的[移动聚集模式](https://www.postgresql.org/docs/12/xaggr.html#XAGGR-MOVING-AGGREGATES)所述。这要求指定 `MSFUNC`、`MINVFUNC` 和 `MSTYPE` 函数，并可选择指定 `MSSPACE`、`MFINALFUNC`、`MFINALFUNC_EXTRA`、`MFINALFUNC_MODIFY` 和 `MINITCOND` 函数。除 `MINVFUNC` 外，这些函数的工作方式与对应的不带 `M` 的简单聚合函数相同；它们定义了该聚集的一种单独实现，其中包含一个逆向转移函数。

参数列表中带有 `ORDER BY` 的语法会创建一种称为*有序集聚集*的特殊聚集；如果指定了 `HYPOTHETICAL`，则会创建*假想集聚集*。这类聚集以依赖于顺序的方式对已排序值的分组进行操作，因此指定输入排序顺序是调用中不可缺少的一部分。此外，它们还可以有*直接*参数，即每次聚集只求值一次、而不是对每个输入行求值一次的参数。假想集聚集是有序集聚集的一个子类，其中要求某些直接参数在数量和数据类型上与被聚集的参数列相匹配。这使得这些直接参数的值可以作为一个额外的“假想”行，加入聚集输入行的集合。

聚集可以选择支持部分聚集。这要求指定 `COMBINEFUNC` 参数。如果 state_data_type 是 internal，通常还应提供 `SERIALFUNC` 和 `DESERIALFUNC` 参数，以便能够进行并行聚集。注意，聚集还必须被标记为 `PARALLEL SAFE`，才能启用并行聚集。

行为类似于 `min()` 或 `max()` 的聚集，有时可以通过查看索引而不是扫描每个输入行来优化。如果该聚集可以这样优化，请通过指定*排序操作符*来表明。基本要求是：该聚集必须产生由该操作符所诱导的排序顺序中的第一个元素；换句话说：

```sql
SELECT agg(col) FROM tab;
```

必须等价于：

```sql
SELECT col FROM tab ORDER BY col USING sortop LIMIT 1;
```

进一步的假设是：该聚合函数忽略空输入，并且当且仅当不存在非空输入时才产生空结果。通常，数据类型的 `<` 操作符是 `min()` 的合适排序操作符，而 `>` 是 `max()` 的合适排序操作符。注意，除非指定的操作符是 B-树索引操作符类中“小于”或“大于”策略的成员，否则这种优化实际上永远不会生效。

要能够创建聚合函数，你必须在参数类型、状态类型和返回类型上具有 `USAGE` 权限，并在支持函数上具有 `EXECUTE` 权限。

你可以将 `combinefunc` 指定为优化聚集执行的一种方法。指定 `combinefunc` 后，聚集可以先在 Segment 上并行运行，然后再在 Coordinator 上运行。执行两级聚集时，`sfunc` 在 Segment 上运行以生成部分聚集结果，`combinefunc` 在 Coordinator 上运行，以聚集来自各 Segment 的部分结果。如果执行单级聚集，则所有行都会发送到 Coordinator，并对这些行应用 `sfunc`。

单级聚集和两级聚集是等价的执行策略。查询计划中可以实现任何一种聚集。实现 `combinefunc` 和 `sfunc` 函数时，你必须确保：在 Segment 实例上调用 `sfunc`、再在 Coordinator 上调用 `combinefunc`，所产生的结果与单级聚集相同；单级聚集会将所有行发送到 Coordinator，然后仅对这些行应用 `sfunc`。

## 参数 {#parameters}

**`name`**

要创建的聚合函数的名称（可带模式限定）。

**`argmode`**

参数的模式：`IN` 或 `VARIADIC`。（聚合函数不支持 `OUT` 参数。）如果省略，默认为 `IN`。只有最后一个参数可以标记为 `VARIADIC`。

**`argname`**

参数的名称。目前这仅用于文档目的。如果省略，则该参数没有名称。

**`arg_data_type`**

该聚合函数所操作的输入数据类型。要创建零参数的聚合函数，请在参数说明列表的位置写 `*`。（此类聚集的一个例子是 `count(*)`。）

**`base_type`**

在 `CREATE AGGREGATE` 的旧语法中，输入数据类型由 `basetype` 参数指定，而不是写在聚集名称旁边。注意，这种语法只允许一个输入参数。要用这种语法定义零参数的聚合函数，请将 `basetype` 指定为 `"ANY"`（而不是 `*`）。有序集聚集不能用旧语法定义。

**`sfunc`**

对每个输入行调用的状态转移函数的名称。对于普通的 N 参数聚合函数，状态转移函数 `sfunc` 必须接收 N+1 个参数，第一个参数的类型为 state_data_type，其余参数与该聚集声明的输入数据类型相匹配。该函数必须返回 state_data_type 类型的值。该函数接收当前状态值和当前输入数据值，并返回下一个状态值。

对于有序集（包括假想集）聚集，状态转移函数只接收当前状态值和被聚集的参数，不接收直接参数。除此之外，情况相同。

**`state_data_type`**

聚集状态值的数据类型。

**`state_data_size`**

聚集状态值的近似平均大小（以字节为单位）。如果省略该参数或其值为零，则会基于 state_data_type 使用默认估计值。规划器使用该值来估计分组聚集查询所需的内存。只有当估计哈希表能放入 `work_mem` 时，规划器才会考虑对这类查询使用哈希聚集；因此，该参数的值较大会妨碍使用哈希聚集。

**`ffunc`**

在遍历完所有输入行之后，用于计算聚集结果的最终函数的名称。该函数必须接收一个类型为 state_data_type 的参数。聚集的返回数据类型定义为该函数的返回类型。如果未指定 `ffunc`，则最终状态值会被用作聚集结果，返回类型为 state_data_type。

对于有序集（包括假想集）聚集，最终函数不仅接收最终状态值，还接收所有直接参数的值。

如果指定了 `FINALFUNC_EXTRA`，则除了最终状态值和任何直接参数之外，最终函数还会接收额外的 NULL 值，它们对应于该聚集的常规（被聚集的）参数。这主要用于在定义多态聚集时，能够正确解析聚集的结果类型。

**`FINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE }`**

此选项指定最终函数是否为不修改其参数的纯函数。`READ_ONLY` 表示它不会修改；另外两个值表示它可能会更改转移状态值。更多细节见下文的[注解](#notes)。默认值为 `READ_ONLY`，但有序集聚集除外，其默认值为 `READ_WRITE`。

**`combinefunc`**

可以选择指定 combinefunc 函数，使聚合函数支持部分聚集。如果提供了它，则 combinefunc 必须把两个 state_data_type 值合并起来（每个值包含对某个输入值子集进行聚集得到的结果），产生一个新的 state_data_type 值，表示对这两组输入一起进行聚集的结果。可以把这个函数看作一种 sfunc：它不是处理单个输入行并将其加入正在运行的聚集状态，而是将另一个聚集状态加入正在运行的状态。

combinefunc 必须声明为接收两个 state_data_type 类型的参数，并返回一个 state_data_type 类型的值。该函数也可以选择声明为“严格”（strict）。在这种情况下，只要任一输入状态为空，就不会调用该函数；另一个状态将被视为正确结果。

对于 state_data_type 为 `internal` 的聚合函数，combinefunc 不能是严格的。在这种情况下，combinefunc 必须确保正确处理空状态，并确保返回的状态被正确存储在聚集内存上下文中。

在 Apache Cloudberry 中，如果聚合函数的结果以分段方式计算，则会对各个内部状态调用合并函数，将它们合并为最终的内部状态。

注意，在 Segment 内以哈希聚集模式运行时也会调用此函数。因此，如果调用的聚合函数没有合并函数，则永远不会选择哈希聚集。由于哈希聚集效率很高，请尽可能考虑定义合并函数。

**`serialfunc`**

state_data_type 为 `internal` 的聚合函数，只有具备 serialfunc 函数时才能参与并行聚集；该函数必须把聚集状态序列化为一个 `bytea` 值，以便传输给另一个进程。该函数必须接收一个 `internal` 类型的参数，并返回 `bytea` 类型。同时还需要相应的 deserialfunc。

**`deserialfunc`**

将之前序列化的聚集状态反序列化回 state_data_type。该函数必须接收 `bytea` 和 `internal` 两个类型的参数，并产生 `internal` 类型的结果。（注意：第二个 `internal` 参数未被使用，但出于类型安全的原因是必需的。）

**`initial_condition`**

状态值的初始设置。它必须是 state_data_type 数据类型所接受形式的字符串常量。如果未指定，则状态值初始为空值。

**`msfunc`**

在移动聚集模式下，对每个输入行调用的前向状态转移函数的名称。它与常规转移函数完全相同，只是其第一个参数和结果的类型为 mstate_data_type，这可能与 state_data_type 不同。

**`minvfunc`**

在移动聚集模式下使用的逆向状态转移函数的名称。该函数的参数类型和结果类型与 msfunc 相同，但它用于从当前聚集状态中移除一个值，而不是向其中添加一个值。逆向转移函数必须与前向状态转移函数具有相同的严格性属性。

**`mstate_data_type`**

使用移动聚集模式时，聚集状态值的数据类型。

**`mstate_data_size`**

使用移动聚集模式时，聚集状态值的近似平均大小（以字节为单位）。其作用与 state_data_size 相同。

**`mffunc`**

使用移动聚集模式时，在遍历完所有输入行之后，用于计算聚集结果的最终函数的名称。其作用与 ffunc 相同，只是它的第一个参数的类型为 mstate_data_type，并且额外的占位参数通过写 `MFINALFUNC_EXTRA` 来指定。由 mffunc 或 mstate_data_type 确定的聚集结果类型，必须与聚集常规实现所确定的类型一致。

**`MFINALFUNC_MODIFY = { READ_ONLY | SHAREABLE | READ_WRITE }`**

此选项与 `FINALFUNC_MODIFY` 类似，但它描述的是移动聚集最终函数的行为。

**`minitial_condition`**

使用移动聚集模式时，状态值的初始设置。其作用与 initial_condition 相同。

**`sort_operator`**

`min()` 或 `max()` 类聚集所关联的排序操作符。这只是一个操作符名称（可带模式限定）。假定该操作符的输入数据类型与该聚集相同（该聚集必须是单参数的普通聚集）。

**`PARALLEL = { SAFE | RESTRICTED | UNSAFE }`**

`PARALLEL SAFE`、`PARALLEL RESTRICTED` 和 `PARALLEL UNSAFE` 的含义与 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/) 中相同。如果聚集被标记为 `PARALLEL UNSAFE`（这是默认值！）或 `PARALLEL RESTRICTED`，则不会考虑对其进行并行化。注意，规划器不会查看聚集的支持函数的并行安全标记，只会查看聚集本身的标记。

**`REPSAFE = boolean`**

指定该聚集能否在复制的切片上安全执行。与顺序无关的聚集在此上下文中被视为安全。默认值为 `false`。

设置 `REPSAFE = true` 会指示优化器执行额外的优化，这些优化专门用于抑制某些广播 Motion。

> **注意** 为与顺序相关的聚集错误地设置 `REPSAFE = true`，可能产生不正确的结果。

**`HYPOTHETICAL`**

仅用于有序集聚集，此标志指定按照假想集聚集的要求处理聚集参数：也就是说，最后几个直接参数必须与被聚集的（`WITHIN GROUP`）参数的数据类型相匹配。`HYPOTHETICAL` 标志对运行时行为没有影响，只影响聚集参数的数据类型和排序规则在解析时的确定。

`CREATE AGGREGATE` 的参数可以按任意顺序书写，而不必拘泥于上文所示的顺序。

## 注解 {#notes}

用于定义新聚合函数的普通函数必须先行定义。

如果 Apache Cloudberry 服务器配置参数 `gp_enable_multiphase_agg` 的值为 `off`，则 Postgres 规划器只会执行单级聚集。Pivotal Query Optimizer 没有与之等价的参数。

自定义函数的任何已编译代码（共享库文件）必须放在 Apache Cloudberry 阵列中每台主机（Coordinator 和所有 Segment）上的同一位置。该位置还必须位于 `LD_LIBRARY_PATH` 中，以便服务器能够找到这些文件。

在 Apache Cloudberry 的早期版本中，存在有序聚集的概念。从版本 6 起，任何聚集都可以作为有序聚集调用，语法如下：

```sql
name ( arg [ , ... ] [ORDER BY sortspec [ , ...]] )
```

`ORDERED` 关键字为向后兼容而被接受，但会被忽略。

在 Apache Cloudberry 的早期版本中，`COMBINEFUNC` 选项称为 `PREFUNC`。为向后兼容，它仍被接受，作为 `COMBINEFUNC` 的同义词。

## 示例 {#example}

下面这个简单的示例创建了一个计算两列之和的聚合函数。

创建聚合函数之前，先创建两个函数，分别用作该聚合函数的 `sfunc` 和 `combinefunc` 函数。

该函数在聚合函数中被指定为 `sfunc` 函数。

```sql
CREATE FUNCTION mysfunc_accum(numeric, numeric, numeric) 
  RETURNS numeric
   AS 'select $1 + $2 + $3'
   LANGUAGE SQL
   RETURNS NULL ON NULL INPUT;
```

该函数在聚合函数中被指定为 `combinefunc` 函数。

```sql
CREATE FUNCTION mycombine_accum(numeric, numeric )
  RETURNS numeric
   AS 'select $1 + $2'
   LANGUAGE SQL
   RETURNS NULL ON NULL INPUT;
```

下面的 `CREATE AGGREGATE` 命令创建将两列相加的聚合函数。

```sql
CREATE AGGREGATE agg_twocols(numeric, numeric) (
   SFUNC = mysfunc_accum,
   STYPE = numeric,
   COMBINEFUNC = mycombine_accum,
   INITCOND = 0 );
```

下面的命令创建一个表，向其中添加一些行，并运行该聚合函数。

```sql
CREATE TABLE t1 (a int, b int) DISTRIBUTED BY (a);
INSERT INTO t1 VALUES
   (10, 1),
   (20, 2),
   (30, 3);
SELECT agg_twocols(a, b) FROM t1;
```

有关创建聚集的更多示例，请参阅 PostgreSQL 文档中的[用户定义的聚集](https://www.postgresql.org/docs/12/xaggr.html)。

## 兼容性 {#compatibility}

`CREATE AGGREGATE` 是 Apache Cloudberry 的语言扩展。SQL 标准没有提供用户定义的聚合函数。

## 另见 {#see-also}

[ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/)、[DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/)、[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)
