---
title: PostgreSQL 钩子
linkTitle: PostgreSQL 钩子
description: 逐项查看 Babelfish 使用的 PostgreSQL 钩子声明及其作用。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/postgresql-hooks.md
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

## PostgreSQL 钩子 {#postgresql-hooks}

Babelfish 使用协议钩子，在 PostgreSQL 服务器中实现 TDS 协议。钩子是默认值为 NULL 的函数指针。将指针改为非 NULL 值后，钩子便会中断服务器的默认行为，调用所指定的函数。借助钩子，Babelfish 可以改变服务器行为，而不必修改社区版 PostgreSQL 的核心代码。

本节介绍 Babelfish 使用的钩子及其作用。

### 关系名称查找 {#relation-name-lookup}

```C
typedef Oid (*relname_lookup_hook_type) (const char *relname, Oid relnamespace);
```

当服务器需要替换 PostgreSQL 原生的关系名称查找逻辑时，便会调用此钩子。Babelfish 用它覆盖 PostgreSQL 的行为，实现 SQL Server 风格的关系名称。

### 排序规则查找 {#collation-lookup-code}

```C
typedef Oid (*CLUSTER_COLLATION_OID_hook_type)(void);
```

当调用 `CLUSTER_COLLATION_OID`、需要把控制权交给可加载插件时，便会调用此钩子。Babelfish 用它控制 PostgreSQL 服务器管理 SQL Server 排序规则的方式。

### 预处理排序规则参数 {#preprocessing-collation-parameters}

```C
typedef void (*PreCreateCollation_hook_type) (char collprovider,
                                              bool collisdeterministic,
                                              int32 collencoding,
                                              const char **collcollate, 
                                              const char **collctype,
                                              const char *collversion);
```

此钩子在服务器创建排序规则之前预处理相关参数。Babelfish 用它实现 PostgreSQL 与 SQL Server 在区域设置方面的差异。

### 管理排序规则名称 {#manage-collation-names}

```C
typedef const char * (*TranslateCollation_hook_type) (const char *collname, 
						      Oid collnamespace, 
						      int32 encoding);
```

处理 SQL Server 专用排序规则时，此钩子用于执行第二次定制的排序规则查找。

### 处理 AS 子句 {#managing-as-clauses}

```C
typedef bool (*check_lang_as_clause_hook_type)(const char *lang, 
					       List *as, 
					       char **prosrc_str_p, 
					       char **probin_str_p);
```

此钩子允许扩展语言处理 `AS` 子句。

### 修改 CREATE FUNCTION 语句 {#modify-create-function-statements}

```C
typedef void (*write_stored_proc_probin_hook_type)(CreateFunctionStmt *stmt, 
						   Oid languageOid, 
						   char** probin_str_p);
```

此钩子用于干预过程代码的存储方式。T-SQL 在内部使用 JSON 存储过程，Babelfish 通过此钩子实现这一行为。

### 修改序列值 {#modify-sequence-values}

```C
typedef void (*pltsql_sequence_validate_increment_hook_type) 
	      (int64 increment_by, int64 max_value, int64 min_value);

typedef void (*pltsql_sequence_datatype_hook_type) (ParseState *pstate, 
		Oid *newtypid, bool for_identity, DefElem *as_type, 
		DefElem **max_value, DefElem **min_value);
```

此钩子使 PostgreSQL 服务器的序列处理行为与 SQL Server 相对应。

### 处理缓存重置 {#handling-cache-resets}

```C
typedef void (*pltsql_resetcache_hook_type) ();
```

此钩子用于调整缓存重置行为。在 Babelfish 中，这与 `IDENTITY` 值密切相关。

### 管理属性（列）选项 {#managing-attribute-column-options}

```C
typedef bool (*check_extended_attoptions_hook_type) (Node *options);
```

不同扩展和协议需要不同的列选项。此钩子用于为这些选项定义验证方法。

### 进入过程 {#procedure-entry}

```C
typedef void (*non_tsql_proc_entry_hook_type) (int, int);
```

此钩子管理进入过程时需要执行的操作。

### 转换规划器中的条件节点 {#transforming-planner-qual-nodes}

```C
typedef Node* (*planner_node_transformer_hook_type) (PlannerInfo *root, 
		Node *expr, int kind);
```

此钩子转换查询规划器内部的条件（qual）节点。条件实质上是查询执行期间使用的“过滤器”，例如 `foo = 10`。

### 解析分析前后的钩子 {#pre-parse-and-post-parse-analyze-hook}

```C
typedef void (*pre_parse_analyze_hook_type) (ParseState *pstate, 
					     RawStmt *parseTree);
```

可以在解析前后调用这些钩子：使用 `pre_parse_analyze_hook` 改变解析之前的服务器行为，使用 `post_parse_analyze_hook` 改变解析之后的行为。

### 处理 RETURNING 限定项 {#hook-into-returning-qualifiers}

```C
typedef void (*pre_transform_returning_hook_type) (CmdType command,
				List *returningList, 
				ParseState *pstate);
```

此钩子处理输出子句返回列表中的限定项。

### UPDATE 转换 {#update-transformations}

```C
typedef Node* (*pre_output_clause_transformation_hook_type) (ParseState *pstate, 
				UpdateStmt *stmt, CmdType 
				command);
```

此钩子对输出子句中的 `UpdateStmt` 执行自连接转换。

### 在输出中读取全局变量 {#reading-global-variables-on-output}

```C
typedef bool (*get_output_clause_status_hook_type) (void);
```

此钩子用于在输出子句中读取包含相关信息的全局变量。

### 在 INSERT 转换后接管处理 {#hook-into-insert-statements-after-transformation}

```C
typedef void (*post_transform_insert_row_hook_type) (List *icolumns, 
				List *exprList);
```

此钩子允许插件在插入行语句之后取得控制权。

### 比较目标列表项（TLE） {#target-list-entry-tle-comparison}

```C
typedef bool (*tle_name_comparison_hook_type)(const char *tlename, 
				const char *identifier);
```

此钩子管理目标列表项的处理方式。目标列表是组成表的列和表达式的列表，例如 `SELECT` 语句中指定的选择项。

### 管理强制类型转换路径 {#manage-path-coercion}

```C
typedef CoercionPathType (*find_coercion_pathway_hook_type) (Oid sourceTypeId,
					Oid targetTypeId,
					CoercionContext ccontext,
					Oid *funcid);
```

此钩子用于确认 T-SQL 是否存在从 `sourceTypeId` 到 `targetTypeId` 的隐式强制类型转换路径。

### 处理数据类型优先级 {#handle-data-type-precedence}

```C
typedef bool (*determine_datatype_precedence_hook_type) (
						Oid typeId1, 
						Oid typeId2);
```

此钩子控制数据类型优先级的处理。在 Babelfish 中，优先级顺序如下：

- <code>sys.sql_variant</code>
- <code>sys.datetimeoffset</code>
- <code>sys.datetime2</code>
- <code>sys.datetime</code>
- <code>sys.smalldatetime</code>
- <code>pg_catalog.date</code>
- <code>pg_catalog.time</code>
- <code>pg_catalog.float8</code>
- <code>pg_catalog.float4</code>
- <code>pg_catalog.numeric</code>
- <code>sys.fixeddecimal</code>
- <code>sys.money</code>
- <code>sys.smallmoney</code>
- <code>pg_catalog.int8</code>
- <code>pg_catalog.int4</code>
- <code>pg_catalog.int2</code>
- <code>sys.tinyint</code>
- <code>sys.bit</code>
- <code>sys.ntext</code>
- <code>pg_catalog.text</code>
- <code>sys.image</code>
- <code>sys.timestamp</code>（当时尚不支持）
- <code>sys.uniqueidentifier</code>
- <code>sys.nvarchar</code>
- <code>sys.nchar</code>
- <code>sys.varchar</code>
- <code>pg_catalog.varchar</code>
- <code>pg_catalog.char</code>
- <code>sys.bpchar</code>
- <code>pg_catalog.bpchar</code>
- <code>sys.bbf_varbinary</code>
- <code>sys.varbinary</code>
- <code>sys.bbf_binary</code>
- <code>sys.binary</code>

### 查找参数定义 {#finding-parameter-definitions}

```C
typedef Node * (*lookup_param_hook_type)(ParseState *pstate, ColumnRef *cref);
```

此钩子控制参数定义的查找过程。

### 控制函数查找 {#controlling-function-lookups}

```C
typedef FuncCandidateList (*func_select_candidate_hook_type) (
					int nargs, 
					Oid *input_typeids, 
					FuncCandidateList candidates, 
					bool unknowns_resolved);
```

此钩子管理不同的函数查找行为，例如处理重载或数据类型。

### 管理函数参数 {#managing-function-arguments}

```C
typedef void (*make_fn_arguments_from_stored_proc_probin_hook_type)(
					ParseState *pstate,
					List *fargs,
					Oid *actual_arg_types,
					Oid *declared_arg_types,
					Oid funcid);
```

此钩子使用 `probin`（`pg_proc` 的一个内部字段）对接函数参数。

### 转换目标列表 {#transforming-the-target-list}

```C
typedef void (*pre_transform_target_entry_hook_type)(
					ResTarget *res, 
					ParseState *pstate, 
					ParseExprKind exprKind);
```

此钩子用于处理目标列表，例如表或 `SELECT` 语句中的列列表。

### 解析目标列表中的未知项 {#resolve-unknown-entries-in-the-target-list}

```C
typedef void (*resolve_target_list_unknowns_hook_type)(ParseState *pstate, 
					List *targetlist);
```

此钩子处理目标列表中的未知项。在列没有指定名称时，SQL Server 与 PostgreSQL 的行为有所不同。

### 管理默认类型修饰符 {#managing-default-typmods}

```C
typedef void (*check_or_set_default_typmod_hook_type)(TypeName * typeName, 
					int32 *typmod, 
					bool is_cast);
```

此钩子控制类型修饰符（typmod）的默认行为。类型修饰符用于修饰数据类型，例如 `varchar(20)` 中指定的长度。

### 控制标识列的数据类型 {#control-the-data-type-of-identity-columns}

```C
typedef void (*pltsql_identity_datatype_hook_type) (ParseState *pstate,
```

此钩子管理标识列（identity column）的数据类型。

### 控制列定义 {#control-column-definitions}

```C
typedef void (*post_transform_column_definition_hook_type) (
					ParseState *pstate, 	
					RangeVar* relation, 
					ColumnDef *column, 
					List **alist);
```

此钩子在初始转换之后处理列定义。

### 扩展后端解析器的钩子 {#hooks-to-extend-the-backend-parser}

```C
typedef List * (*raw_parser_hook_type) (const char *str);
```

此钩子控制原始解析器的行为。

### 重新处理类型修饰符表达式 {#re-processing-typmod-expressions}

```C
typedef List * (*rewrite_typmod_expr_hook_type) (List *expr_list);
```

此钩子定义 Babelfish 类型修饰符的重写行为。

### 验证数值类型的类型修饰符 {#validate-typmods-for-numeric-types}

```C
typedef void (*validate_numeric_typmods_hook_type) (List **typmods, 
			bool isNumeric, 
			void* yyscanner);
```

此钩子验证数值类型的类型修饰符。

### 处理递归 CTE {#handling-recursive-ctes}

```C
typedef bool (*check_recursive_cte_hook_type) (WithClause *with_clause);
```

此钩子直接调整 PostgreSQL 解析器和 SQL 语法的行为，允许 `WITH` 子句中的名称使用 `TIME` 或 `ORDINALITY`。

### 处理不同的标识符长度 {#handling-different-lengths-of-identifiers}

```C
typedef bool (*truncate_identifier_hook_type)(char *ident, int len, bool warn);
```

此钩子用于截断标识符名称。SQL Server 的标识符可以比 PostgreSQL 的更长（原文举例称 `name` 数据类型限制为 255 字节；此处保留该历史文档的表述）。

### 在执行函数前调用代码 {#calling-code-before-a-function-is-executed}

```C
typedef void (*pre_function_call_hook_type) (const char *funcName);
```

此钩子在调用函数之前更改函数名称。在 Babelfish 中，函数名中的某些字符会替换为下划线。

### 启动协议支持 {#launching-protocol-support}

```C
typedef void (*listen_init_hook_type)(void);
```

此钩子用于启动协议支持。

### 控制字符串截断错误 {#control-string-truncation-errors}

```C
typedef bool (*suppress_string_truncation_error_hook_type)();
```

此钩子控制错误的处理方式。Babelfish 代码中的许多位置都需要服务器截断字符串。

### 把 C 字符串转换为名称 {#convert-c-strings-to-names}

```C
typedef Name (*cstr_to_name_hook_type)(char *s, int len);
```

此钩子处理 `name` 数据类型。该类型的长度有限，因此需要相应的截断规则。

### 处理运行时变量 {#handling-runtime-variables}

```C
typedef void (*guc_push_old_value_hook_type) (
				struct config_generic *gconf, 
				GucAction action);
```

此钩子用于临时修改 GUC（PostgreSQL 的运行时变量）。

### 检查配置变量 {#checking-configuration-variables}

```C
typedef	void(*validate_set_config_function_hook_type) (char *name, char *value);
```

此钩子处理 Babelfish 专用变量。Babelfish 的变量可能不支持社区版 PostgreSQL 中相同的取值。

### 控制计划失效 {#controlling-plan-invalidation}

```C
typedef void (*plansource_complete_hook_type) (CachedPlanSource *plansource);
typedef bool (*plansource_revalidate_hook_type) (CachedPlanSource *plansource);
```

此钩子控制执行计划的存储和失效。

在 T-SQL 内部，乃至普通连接中，通常都会预先生成并保存执行计划，以加快后续执行。有时需要使这些计划失效并重新生成。例如，删除一列后，所有引用该列的计划都必须移除，因为计划所引用的数据库对象已不存在。修改配置变量时也可能需要这样处理。
