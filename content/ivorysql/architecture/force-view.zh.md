---
title: Force View
linkTitle: Force View
description: IvorySQL v5.6 文档：Force View。
type: docs
weight: 660
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/6.3.8.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

- Force View 提供 Oracle 兼容的 `CREATE [OR REPLACE] FORCE VIEW` 与 `ALTER VIEW …​ COMPILE` 行为，允许开发者先落地视图占位，再在依赖补齐后恢复正常执行。

- 系统将原始 SQL 及标识符大小写模式写入专属目录项，依赖恢复时可自动或手动编译为普通视图，且保持 Oracle 风格的告警与错误提示。

## 2. 实现说明 {#implementation-description}

PG在删除基表时，如果有视图依赖于此基表，则不允许删除，需要使用cascade 关键字全部删除；Oracle删除基表时，允许直接删除基表，而保留force view并将force view 转为无效状态，且创建普通视图后，也可以删除此视图的基表，但把视图转为无效状态。

为了支持新的语法，需要增加对应的语法规则。且FORCE VIEW的状态在多个session之间是共享的，新增一张系统表用来存储FORCE VIEW的相关信息。

### 2.1. 语法与解析入口 {#grammar-and-parsing-entry-points}

#### 2.1.1. Force View 语法支持 {#force-view-syntax-support}

- `src/backend/oracle_parser/ora_gram.y` 注册 Force View 关键字。

- 语法阶段为 `ViewStmt→force` 赋值，并在 `AlterTableStmt` 阶段生成 `AT_ForceViewCompile` 选项。

- 解析阶段保留 `ViewStmt→stmt_literal`，后续占位时需要复用原始文本。

```
/* Insert or update the pg_force_view catalog as needed */
if (need_store)
{
    ......

    StoreForceViewQuery(address.objectId, stmt->replace, ident_case, stmt->stmt_literal ? stmt->stmt_literal : queryString);
}
```

#### 2.1.2. AST 字段扩展 {#ast-field-extensions}

- `src/include/nodes/parsenodes.h` 为 `ViewStmt` 增加 `bool force`、`char *stmt_literal` 字段。

- `AT_ForceViewCompile` 在 `parsenodes.h` 与 `tablecmds.c` 成对定义，确保 `ALTER VIEW …​ COMPILE` 进入 AlterTable 流程。

- `parse_analyze` 仍按普通路径执行，Force 模式只在解析报错后介入。

#### 2.1.3. 解析入口 {#parsing-entry}

- `DefineView()`（`src/backend/commands/view.c`）统一处理普通与 Force 视图。

- 代码在 `PG_TRY/PG_CATCH` 包裹下先尝试普通解析，捕获语义错误后根据 `stmt→force` 决定是否进入Force View 流程。

- 成功解析继续调用 `StoreViewQuery()` 写入 `_RETURN` 规则，失败则进入 Force View 分支，保证视图对象仍然存在。

### 2.2. Force View 元数据 {#force-view-metadata}

#### 2.2.1. `pg_force_view` 目录 {#pg_force_view-catalog}

- `src/include/catalog/pg_force_view.h` 定义目录表，字段包含视图 OID (`fvoid`)、标识符大小写模式 (`ident_case`)、原始 SQL 文本 (`source`)。

- 唯一索引 `pg_force_view_fvoid_index` 搭配 syscache `FORCEVIEWOID`（`src/include/catalog/syscache_info.h`）实现按视图 OID 查找。

- 目录表开启 TOAST，长 SQL 文本不会被截断，可覆盖复杂迁移脚本。

```
CATALOG(pg_force_view,9120,ForceViewRelationId)
{
    /* oid of force view */
    Oid         fvoid;

    /* see IDENT_CASE__xxx constants below */
    char        ident_case;

#ifdef CATALOG_VARLEN           /* variable-length fields start here */

    /* sql definition */
    text        source;
#endif
} FormData_pg_force_view;
```

#### 2.2.2. 视图状态 {#view-state}

- `bool rel_is_force_view(Oid relid)` 位于 `src/backend/commands/view.c`，通过判断 `_RETURN` 规则是否存在确认视图是否处于 Force 状态。

- Force View 仍登记为 `relkind = RELKIND_VIEW`，避免额外兼容分支。

- `pg_class.relhasrules` 在占位状态设置为 `false`，配合作为判断依据。

### 2.3. 创建与替换流程 {#creation-and-replacement-flow}

#### 2.3.1. 普通 view {#normal-view}

- `DefineView()` 在解析成功后调用 `DefineVirtualRelation()` 写入 `pg_class`、`pg_attribute` 等结构。

- `StoreViewQuery()` 生成 `_RETURN` 规则并维护依赖关系。

- 该路径不会触及 `pg_force_view`，视图完成后立即可用。

#### 2.3.2. Force view {#force-view}

- `CreateForceVirtualPlaceholder()`（`src/backend/commands/view.c`）负责生成或复用占位视图：

- 若视图不存在，调用 `DefineVirtualRelation()` 建立基础对象，但不写入 `_RETURN` 规则。

- 若已有 Force View，复用当前记录，更新列定义或清理旧元数据。

- 若已有普通视图且声明了 `OR REPLACE`，调用 `make_view_invalid()` 失效原视图，再写入新的占位定义。

- `StoreForceViewQuery()` 将 `stmt_literal` 与当前 `ivorysql.identifier_case_switch` 持久化到 `pg_force_view`，以便后续恢复大小写语义。

- 视图占位完成后向客户端返回 `WARNING: View created with compilation errors`，提示仍处于不可用状态。

### 2.4. 依赖失效与回退 {#dependency-invalidations-and-rollback}

#### 2.4.1. 主动失效逻辑 {#active-invalidation-logic}

- `make_view_invalid()` 在依赖对象被 DROP/ALTER 等操作影响时调用。

- 函数删除 `_RETURN` 规则、清理 `pg_depend` 依赖、重置 `pg_class.relhasrules` 并清空 `pg_attribute` 列信息。

- 同步生成 `CREATE FORCE VIEW …​ AS <pg_get_viewdef>` 文本写入 `pg_force_view`，`ident_case` 设置为 `IDENT_CASE_UNDEFINE` 表示该文本由系统构造。

#### 2.4.2. 失效后的可见行为 {#observable-behavior-after-invalidation}

- 视图仍然存在并可在元数据中枚举，但实际访问会触发 Force 判定。

- `_RETURN` 缺失导致执行器在打开视图时调用 `compile_force_view()`，若编译仍失败则抛出 `view "<schema>.<name>" has errors`。

- 用户可通过 `ALTER VIEW …​ COMPILE` 或再次 `CREATE OR REPLACE FORCE VIEW` 来恢复。

### 2.5. 自动与主动编译 {#automatic-and-manual-compilation}

#### 2.5.1. 自动编译触发点 {#automatic-compilation-triggers}

- `parse_relation.c` 的 `addRangeTableEntry()` 和 `parse_clause.c` 的目标关系打开逻辑在判定 Force View 后调用 `compile_force_view()`。

- 该函数重新执行 `raw_parser` 与 `parse_analyze`，成功则再安装 `_RETURN` 规则，失败直接终止当前语句。

#### 2.5.2. 主动编译 {#manual-compilation}

- `AT_ForceViewCompile` 在 `tablecmds.c` Phase 2 阶段执行，先申请 `AccessExclusiveLock` 再调用 `compile_force_view()`。

- 成功编译返回常规 `ALTER VIEW` 完成信息；失败打印 `WARNING: View altered with compilation errors`，视图仍保持占位。

#### 2.5.3. 列校验与元数据更新 {#column-checks-and-metadata-updates}

- `compile_force_view()` 读取 `pg_force_view.source` 并构造 `ViewStmt`，随后调用 `compile_force_view_internal()`。

- 函数通过 `checkViewColumns()` 比对旧列，允许新增列但禁止类型不兼容的替换；新增列由 `AT_AddColumnToView()` 完成。

- `_RETURN` 规则由 `StoreViewQuery()` 重新生成，最后 `DeleteForceView()` 删除目录项，视图恢复为普通状态。
