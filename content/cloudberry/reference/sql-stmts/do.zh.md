---
title: "DO"
description: "将匿名代码块作为临时匿名函数执行。"
weight: 990
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/do.md"
---

## 概要 {#synopsis}

```sql
DO [ LANGUAGE <lang_name> ] <code>
```

## 描述 {#description}

`DO` 执行匿名代码块，换言之，执行用过程语言编写的临时匿名函数。

该代码块被视为一个无参数、返回 `void` 的函数体，仅解析和执行一次。

可选的 `LANGUAGE` 子句可以出现在代码块之前或之后。

匿名块是一种过程语言结构，支持即时创建和运行过程代码，而无需将代码作为数据库对象持久存储在系统目录中。匿名块的概念类似于 UNIX shell 脚本，可以将多个手工输入的命令组合起来，作为一个步骤运行。顾名思义，匿名块没有名称，因此其他对象无法引用它。虽然是动态构建的，匿名块仍可以很方便地作为脚本存储在操作系统文件中，以便重复执行。

匿名块是标准的过程语言块，使用并遵循该过程语言的语法和规则，包括变量声明与作用域、执行、异常处理及语言用法。

匿名块的编译和执行合并为一个步骤；用户定义函数的定义每次更改后，都需要在使用前重新定义该函数。

## 参数 {#parameters}

**`code`**

要执行的过程语言代码。与 `CREATE FUNCTION` 命令一样，必须指定为字符串字面量。推荐使用美元符引用的字面量。

**`lang_name`**

编写代码所用的过程语言名称。默认为 `plpgsql`。

## 注意事项 {#notes}

所用过程语言必须已通过 `CREATE EXTENSION` 安装到当前数据库中。PL/pgSQL 随 Apache Cloudberry 安装，并默认注册到每个用户创建的数据库中。PL/Python 和 PL/Perl 默认已安装，但未注册。其他语言既未安装，也未注册。pg_language 系统目录包含数据库中已注册语言的信息。

用户必须拥有该过程语言的 `USAGE` 权限；如果语言不受信任，则必须是超级用户。这与使用该语言创建函数的权限要求相同。

如果在事务块中执行 `DO`，过程代码不能执行事务控制语句。只有 `DO` 在自己的事务中执行时，才允许事务控制语句。

匿名块不支持函数易变性或 `EXECUTE ON` 属性。

## 示例 {#examples}

下面的 PL/pgSQL 示例将模式 `public` 中所有视图的全部权限授予角色 `webuser`：

```sql
DO $$DECLARE r record;
BEGIN
    FOR r IN SELECT table_schema, table_name FROM information_schema.tables
             WHERE table_type = 'VIEW' AND table_schema = 'public'
    LOOP
        EXECUTE 'GRANT ALL ON ' || quote_ident(r.table_schema) || '.' || quote_ident(r.table_name) || ' TO webuser';
    END LOOP;
END$$;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `DO` 语句。

## 另见 {#see-also}

[CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/)
