---
title: 空字符串转NULL功能
linkTitle: 空字符串转null
description: IvorySQL v5.6 文档：空字符串转NULL功能。
type: docs
weight: 690
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/CN/modules/ROOT/pages/6.3.11.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs
upstream_modified: true
---

## 1. 目的 {#purpose}

在Oracle数据库中，空字符串('')被视为NULL值，这是Oracle的一个重要特性。为了兼容Oracle的这一行为，IvorySQL提供了空字符串转NULL功能。当启用该功能后，SQL语句中的空字符串将自动转换为NULL值，从而保证Oracle应用程序在IvorySQL上的行为一致性。

## 2. 实现说明 {#implementation}

参数 `ivorysql.enable_emptystring_to_NULL` 对应的GUC变量为 `enable_emptystring_to_NULL`。

在文件 `ora_scan.l` 中可以看到对这个变量的使用：

``` c
case xe:
    yylval->str = litbufdup(yyscanner);
    if (strcmp(yylval->str, "") == 0 &&
        ORA_PARSER == compatible_db &&
        enable_emptystring_to_NULL)
    {
        return NULL_P;
    }
    return SCONST;
```

其中 `xe` 代表被引号包围的字符串：

```
<xe> extended quoted strings (support backslash escape sequences)
```

上面代码的逻辑是，在词法分析时如果遇到空字符串，在空转NULL功能启用的情况下，返回 `NULL_P`，否则返回 `SCONST`。

在语法分析文件 `ora_gram.y` 里，对语句 `insert into abc values('');` 是这样解析的：

``` c
values_clause:
    VALUES '(' expr_list ')'
    {
        SelectStmt *n = makeNode(SelectStmt);

        n->valuesLists = list_make1($3);
        $$ = (Node *) n;
    }

expr_list:      a_expr
        {
            $$ = list_make1($1);
        }

a_expr:       c_expr                      { $$ = $1; }

c_expr:       AexprConst                  { $$ = $1; }

AexprConst: Iconst
       | Sconst
           {
               $$ = makeStringConst($1, @1);
           }
       | NULL_P
           {
               $$ = makeNullAConst(@1);
           }
```

以上代码对词法分析时返回的 `NULL_P` 或者 `SCONST` 分别构建对应的节点进行处理。
