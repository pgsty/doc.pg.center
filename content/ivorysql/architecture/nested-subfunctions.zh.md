---
title: 嵌套子函数
linkTitle: 嵌套子函数
description: IvorySQL v5.6 文档：嵌套子函数。
type: docs
weight: 650
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/6.3.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#objective}

- 嵌套子函数：定义在函数、存储过程或匿名块内部的函数或存储过程，也称为 subproc 或 inner 函数。

- 父函数：承载嵌套函数的外层函数、存储过程或匿名块，执行过程中负责实际触发子函数调用。

## 2. 实现说明 {#implementation-notes}

### 2.1. 嵌套子函数语法识别 {#syntax-recognition-for-nested-subfunctions}

#### 2.1.1. 识别嵌套写法 {#detecting-nested-definitions}

当 `DECLARE` 块里出现 `function …​ is/as begin …​ end` 结构时，`pl_gram.y` 会调用 `plisql_build_subproc_function()`（对应创建普通函数，这一阶段相当于在 `pg_proc` 中更新 catalog 中的注册信息）：

1.  在 `PLiSQL_function` 的 `subprocfuncs[]` 数组中创建 `PLiSQL_subproc_function` 结构，记录名称、参数、返回类型、属性等，获得一个下标 `fno` 作为该子函数的标识。

2.  调用 `plisql_check_subprocfunc_properties()` 校验声明与定义的合法组合。

#### 2.1.2. 数据项保存 {#storing-datum-entries}

保存到父函数的 `datum` 表：编译期的 `PLiSQL_function→datums` 描述子函数里的变量、记录字段，`PLiSQL_execstate→datums` 保存着执行过程中的变量。

#### 2.1.3. 保存多态函数模板 {#preserving-polymorphic-templates}

如果子函数里使用了多态参数，在语法阶段保存到 `subprocfunc→src`，同时将 `has_poly_argument` 设成 `true`，执行时按不同实参类型重新编译。

### 2.2. 父函数重新编译 {#recompiling-the-parent-program}

1.  父函数的 `PLiSQL_function` 结构多了一个 `subprocfuncs` 数组，里面每个元素就是刚才创建的 `PLiSQL_subproc_function`。

2.  子函数结构体 `PLiSQL_subproc_function` 有一个哈希表指针 `HTAB *poly_tab`，默认为空。当子函数里使用了多态函数时，`has_poly_argument` 为 `true`，则会在初次编译时初始化 `poly_tab`。`poly_tab` 的 key 是 `PLiSQL_func_hashkey`，记录着子函数的 `fno`、输入参数类型等； value 是编译好的 `PLiSQL_function *`（`plisql` 函数的执行上下文）。

### 2.3. 调用时解析 {#name-resolution-during-invocation}

1.  编译过程中，`pg` 解析器会生成一个 `ParseState` 结构，`plisql_subprocfunc_ref()` 会通过 `ParseState→p_subprocfunc_hook()` 找到父函数的 `PLiSQL_function`，调用 `plisql_ns_lookup()` 找到所有同名子函数的 `fno`，根据参数个数、类型找到最合适的多态函数。

2.  `FuncExpr` 结构构造时会对子函数进行标记，方便后期执行阶段识别：`function_from = FUNC_FROM_SUBPROCFUNC`，`parent_func` 指向父级 `PLiSQL_function`，`funcid = fno`。

3.  `plisql_call_handler()` 当 `function_from == FUNC_FROM_SUBPROCFUNC`，会用 `parent_func + fno` 找到对应的 `PLiSQL_subproc_function`：

    1.  如果不是多态：直接复用 `subprocfunc→function` 里的动作树。

    2.  如果是多态：先在 `poly_tab` 查有没有编译结果；没有就调用 `plisql_dynamic_compile_subproc()` 编译，放进 `poly_tab` 缓存。

4.  子函数开始执行之前，`plisql_init_subprocfunc_globalvar()` 会把父函数的 `datum` 表中有关的变量 fork 一份，这样子函数可以获取到父函数的变量值，也不会污染父函数的变量空间；执行后由 `plisql_assign_out_subprocfunc_globalvar()` 把需要回写的变量更新到父函数的 `datum` 表。

## 3. 模块设计 {#module-design}

### 3.1. PL/iSQL 语法扩展 {#plisql-grammar-extensions}

- `pl_gram.y` 新增子过程声明、嵌套定义的产生式，并在创建过程中记录 `lastoutvardno`、子过程信息等元数据。

- 支持在子函数内引用父过程变量、子过程以及自定义类型。

当 DECLARE 块内出现 `function …​ is/as begin …​ end` 结构时，`pl_gram.y` 会调用 `plisql_build_subproc_function()` 进行编译：

1.  在 `PLiSQL_function` 的 `subprocfuncs[]` 中创建 `PLiSQL_subproc_function` 结构，记录名称、参数、返回类型和属性，分配下标 `fno` 作为子函数标识。

2.  调用 `plisql_check_subprocfunc_properties()` 校验声明与定义属性组合是否合法，防止重复或缺失声明造成的语义错误。

### 3.2. 数据项保存 {#datum-storage}

父函数的 Datum 表在编译期和执行期分别缓存子函数能访问的变量：

1.  `PLiSQL_function→datums` 保存子函数编译阶段可见的变量与记录字段信息。

2.  `PLiSQL_execstate→datums` 在执行阶段持有实时的变量数值，实现运行期访问。

### 3.3. 多态函数模板 {#polymorphic-templates}

若子函数包含多态参数，语法阶段会：

1.  将子函数源文本拷贝到 `subprocfunc→src`。

2.  设置 `has_poly_argument = true`，为后续按实参类型动态编译做好准备。

### 3.4. 父函数重新编译 {#parent-recompilation}

- 父函数的 `PLiSQL_function` 结构新增 `subprocfuncs` 数组，每个元素对应一个 `PLiSQL_subproc_function`。

- `PLiSQL_subproc_function` 持有 `HTAB *poly_tab` 指针；当 `has_poly_argument` 为 `true` 时，在首次编译时初始化该缓存，键为 `PLiSQL_func_hashkey`（子函数 `fno` + 实参类型），值为编译后的 `PLiSQL_function`。

### 3.5. 解析器钩子 {#parser-hooks}

编译期间 PostgreSQL 解析器会构造 `ParseState`，`plisql_subprocfunc_ref()` 通过 `ParseState→p_subprocfunc_hook()` 连接父函数，调用 `plisql_ns_lookup()` 找到同名子函数的全部 `fno`，并依据参数个数与类型挑选最佳候选，实现重载分发。

### 3.6. FuncExpr 标记 {#funcexpr-annotation}

构造 `FuncExpr` 时会标记嵌套调用信息，便于执行阶段识别：

- `function_from = FUNC_FROM_SUBPROCFUNC`。

- `parent_func` 指向父级 `PLiSQL_function`。

- `funcid = fno`，用于快速定位子函数定义。

### 3.7. 嵌套函数查找机制 {#nested-subfunction-lookup}

- `plisql_subprocfunc_ref()` 作为 `ParseState→p_subprocfunc_hook` 实现入口，复用名称空间查询逻辑。

- `plisql_get_subprocfunc_detail()` 依据参数数量、类型与命名匹配规则挑选最优候选，是嵌套函数重载的关键。

### 3.8. 执行路径 {#execution-path}

1.  `plisql_call_handler()` 判断 `function_from` 后，通过 `parent_func + fno` 找到目标 `PLiSQL_subproc_function`。

2.  对普通子函数，直接复用 `subprocfunc→function` 缓存；

3.  对多态子函数，先查询 `poly_tab`，未命中时调用 `plisql_dynamic_compile_subproc()` 动态编译并写入缓存。

### 3.9. 变量同步 {#variable-synchronization}

- `plisql_init_subprocfunc_globalvar()` 在子函数执行前拷贝父函数 Datum 表中的相关变量，保证子函数读取到外层最新状态。

- `plisql_assign_out_subprocfunc_globalvar()` 在返回前回写 OUT/INOUT 变量，确保父子函数数据一致性且互不污染。

### 3.10. PSQL 端语句发送 {#statement-dispatch-in-psql}

- `psqlscan.l` 调整 `proc_func_define_level` 和 `begin_depth` 的入栈/出栈逻辑，确保嵌套函数体整体发送至 SQL 端。

- 只有当嵌套层级回到 0 且遇到分号时，才触发发送，避免子函数块被拆分。

### 3.11. SQL 层返回值获取 {#retrieving-return-information-on-the-sql-side}

- 普通函数通过 `funcid` 访问 `pg_proc`；嵌套函数依赖 `FuncExpr.parent_func` 承载的 `PLiSQL_function`。

- 为此实现一组函数指针（`plisql_register_internal_func()` 注册）供 SQL 层回调，按需获取嵌套函数名称、返回类型与 OUT 参数信息。
