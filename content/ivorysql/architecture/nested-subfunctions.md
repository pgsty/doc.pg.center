---
title: Nested Subfunctions
linkTitle: Nested Subfunctions
description: 'IvorySQL v5.6 documentation: Nested Subfunctions.'
type: docs
weight: 650
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/6.3.7.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Objective {#objective}

- Nested subfunctions refer to functions or procedures defined inside another function, stored procedure, or anonymous block; they are also called subprocs or inner functions.

- Parent functions are the outer functions, stored procedures, or anonymous blocks that host nested subfunctions and are responsible for invoking them during execution.

## 2. Implementation Notes {#implementation-notes}

### 2.1. Syntax Recognition for Nested Subfunctions {#syntax-recognition-for-nested-subfunctions}

#### 2.1.1. Detecting Nested Definitions {#detecting-nested-definitions}

When a `DECLARE` block contains a `function …​ is/as begin …​ end` construct, `pl_gram.y` calls `plisql_build_subproc_function()` (similar to creating a regular function and updating the entry in `pg_proc`):

1.  Create a `PLiSQL_subproc_function` entry in the parent `` PLiSQL_function’s `subprocfuncs[] `` array to store the name, arguments, return type, and other attributes, and record the index `fno` as the identifier of this subfunction.

2.  Call `plisql_check_subprocfunc_properties()` to validate the combination of declaration and definition attributes.

#### 2.1.2. Storing Datum Entries {#storing-datum-entries}

Nested subfunctions share the parent’s datum table. During compilation, `PLiSQL_function→datums` describes variables and record fields inside the subfunction, while `PLiSQL_execstate→datums` keeps the runtime values.

#### 2.1.3. Preserving Polymorphic Templates {#preserving-polymorphic-templates}

If the subfunction uses polymorphic parameters, the parser stores its source code in `subprocfunc→src` and sets `has_poly_argument` to `true` so that the executor can recompile it for each distinct argument type.

### 2.2. Recompiling the Parent Program {#recompiling-the-parent-program}

1.  The parent `PLiSQL_function` gains a `subprocfuncs` array, each element being the `PLiSQL_subproc_function` created earlier.

2.  Each `PLiSQL_subproc_function` has a `HTAB *poly_tab` pointer that is initialized on the first compilation when `has_poly_argument` is `true`. The hash key is `PLiSQL_func_hashkey`, which records the subfunction’s `fno` and input argument types; the value is the compiled `PLiSQL_function *` execution context.

### 2.3. Name Resolution During Invocation {#name-resolution-during-invocation}

1.  PostgreSQL builds a `ParseState` structure during compilation. `plisql_subprocfunc_ref()` locates the parent `PLiSQL_function` through `ParseState→p_subprocfunc_hook()` and calls `plisql_ns_lookup()` to gather all `fno` values for subfunctions sharing the same name, then selects the best match based on argument count and types.

2.  When `FuncExpr` nodes are created, the subfunction call is tagged for later execution: `function_from = FUNC_FROM_SUBPROCFUNC`, `parent_func` points to the parent `PLiSQL_function`, and `funcid = fno`.

3.  In `plisql_call_handler()`, when `function_from == FUNC_FROM_SUBPROCFUNC`, the runtime fetches the appropriate `PLiSQL_subproc_function` via the pair `(parent_func, fno)`:

    1.  For non-polymorphic subfunctions, reuse the precompiled action tree stored in `subprocfunc→function`.

    2.  For polymorphic subfunctions, probe `poly_tab`; if there is no cached plan, call `plisql_dynamic_compile_subproc()` to compile one and store it in the cache.

4.  Before execution, `plisql_init_subprocfunc_globalvar()` forks relevant entries from the parent’s datum table so the subfunction can access the latest parent variables without polluting the parent scope. After execution, `plisql_assign_out_subprocfunc_globalvar()` writes back the necessary variables.

## 3. Module Design {#module-design}

### 3.1. PL/iSQL Grammar Extensions {#plisql-grammar-extensions}

- `pl_gram.y` adds productions for subprocedure declarations and nested definitions, and records metadata such as `lastoutvardno` and subprocedure descriptors.

- Nested subfunctions can reference variables from the parent scope, other subprocedures, and user-defined types.

Whenever a `function …​ is/as begin …​ end` construct is seen inside a `DECLARE` block, `pl_gram.y` invokes `plisql_build_subproc_function()`:

1.  Insert a `PLiSQL_subproc_function` entry into the parent `PLiSQL_function→subprocfuncs[]`, storing the name, arguments, return type, and other attributes, and assign an index `fno`.

2.  Call `plisql_check_subprocfunc_properties()` to verify that declarations and definitions are consistent and to prevent duplicate or missing declarations from introducing semantic errors.

### 3.2. Datum Storage {#datum-storage}

The parent program’s datum tables hold the variables accessible to nested subfunctions during compilation and execution:

1.  `PLiSQL_function→datums` preserves the variable and record metadata visible during compilation.

2.  `PLiSQL_execstate→datums` carries the live values at runtime.

### 3.3. Polymorphic Templates {#polymorphic-templates}

When a subfunction contains polymorphic arguments, the parser will:

1.  Copy the subfunction source text into `subprocfunc→src`.

2.  Set `has_poly_argument = true` to prepare for dynamic recompilation based on actual argument types.

### 3.4. Parent Recompilation {#parent-recompilation}

- The parent `PLiSQL_function` includes a `subprocfuncs` array, with each element corresponding to a `PLiSQL_subproc_function`.

- Each `PLiSQL_subproc_function` maintains an optional `HTAB *poly_tab`; when `has_poly_argument` is `true`, the cache is initialized on the first compile. Keys are `PLiSQL_func_hashkey` (subfunction `fno` plus argument types), and values are the compiled `PLiSQL_function` plans.

### 3.5. Parser Hooks {#parser-hooks}

During compilation, PostgreSQL creates a `ParseState`. `plisql_subprocfunc_ref()` plugs into `ParseState→p_subprocfunc_hook`, reusing the namespace lookup logic to gather candidates. `plisql_get_subprocfunc_detail()` then chooses the best match based on argument count, types, and named parameters, enabling overloaded dispatch.

### 3.6. FuncExpr Annotation {#funcexpr-annotation}

When constructing `FuncExpr` nodes, the compiler attaches metadata so the executor can recognize nested calls:

- `function_from = FUNC_FROM_SUBPROCFUNC`.

- `parent_func` references the owning `PLiSQL_function`.

- `funcid = fno`, enabling direct lookup of the subfunction definition.

### 3.7. Nested Subfunction Lookup {#nested-subfunction-lookup}

- `plisql_subprocfunc_ref()` implements `ParseState→p_subprocfunc_hook` and reuses the namespace search to find nested subfunctions.

- `plisql_get_subprocfunc_detail()` applies matching rules for argument count, type, and naming to pick the optimal overload.

### 3.8. Execution Path {#execution-path}

1.  `plisql_call_handler()` checks `function_from`; if it is a nested subfunction, the handler locates `PLiSQL_subproc_function` via `(parent_func, fno)`.

2.  For regular subfunctions, reuse the cached plan stored in `subprocfunc→function`.

3.  For polymorphic subfunctions, consult `poly_tab`; on a miss, call `plisql_dynamic_compile_subproc()` to build and cache a specialized plan.

### 3.9. Variable Synchronization {#variable-synchronization}

- `plisql_init_subprocfunc_globalvar()` copies the relevant entries from the parent datum table before the subfunction runs to expose the latest state.

- `plisql_assign_out_subprocfunc_globalvar()` writes back OUT/INOUT variables after execution to keep parent and child scopes consistent without mutual pollution.

### 3.10. Statement Dispatch in psql {#statement-dispatch-in-psql}

- `psqlscan.l` adjusts the push/pop logic of `proc_func_define_level` and `begin_depth` so the nested subfunction body is transmitted to the SQL engine as a whole.

- Statements are sent only when the nesting depth returns to zero and a semicolon is reached, avoiding partial dispatch of subfunction blocks.

### 3.11. Retrieving Return Information on the SQL Side {#retrieving-return-information-on-the-sql-side}

- Regular functions obtain metadata via `funcid` from `pg_proc`; nested subfunctions rely on `FuncExpr.parent_func`, which holds the parent `PLiSQL_function`.

- A set of callback pointers (registered through `plisql_register_internal_func()`) allows the SQL layer to fetch nested subfunction names, return types, and OUT parameter information on demand.
