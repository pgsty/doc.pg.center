---
title: "使用 PL/pgSQL"
description: "PL/pgSQL 是一种可加载的过程语言，Apache Cloudberry 默认会安装并注册该语言。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-pgsql.md"
---

它为标准 SQL 增加了执行复杂计算和使用控制结构的能力。

## PL/pgSQL 的优势 {#benefits-of-plpgsql}

- **SQL 集成**：设计目标是便于与 SQL 一起使用。
- **可移植性**：用 PL/pgSQL 编写的函数可以在 Apache Cloudberry 运行的任何平台上使用。
- **性能**：将多个 SQL 语句组合到单个代码块中，从而减少客户端与服务器之间的通信开销。

## PL/pgSQL 函数的结构 {#structure-of-plpgsql-functions}

PL/pgSQL 函数与标准 SQL 函数的区别在于，函数体按代码块组织。

```sql
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
END [ label ];
```

- **声明**：定义代码块中使用的变量。
- **语句**：实际的过程代码。
- **BEGIN/END**：界定代码块。

### 示例：创建简单函数 {#example-create-a-simple-function}

```sql
CREATE OR REPLACE FUNCTION sales_tax(subtotal real)
RETURNS real AS $$
BEGIN
    RETURN subtotal * 0.06;
END;
$$ LANGUAGE plpgsql;
```

## 匿名代码块 {#anonymous-blocks}

可以使用 `DO` 命令运行 PL/pgSQL 代码，而无需创建持久函数。这对于管理任务或一次性脚本很有用。

```sql
DO $$
DECLARE
    counter integer := 0;
BEGIN
    WHILE counter < 5 LOOP
        RAISE NOTICE 'Counter: %', counter;
        counter := counter + 1;
    END LOOP;
END $$;
```

## 声明 {#declarations}

可以使用标准 SQL 数据类型声明变量，也可以使用 `%TYPE` 和 `%ROWTYPE` 引用现有数据库对象。

- `%TYPE`：复制变量或表列的数据类型。

    ```sql
    user_id users.id%TYPE;
    ```

- `%ROWTYPE`：创建与表行结构匹配的复合变量。

    ```sql
    user_row users%ROWTYPE;
    ```

## 控制结构 {#control-structures}

PL/pgSQL 支持多种控制结构：

- **IF-THEN-ELSE**：条件执行。
- **LOOP、WHILE、FOR**：迭代执行。
- **EXCEPTION**：错误处理。

```sql
IF v_count > 0 THEN
    UPDATE users SET active = true WHERE id = v_user_id;
ELSE
    INSERT INTO users (id, active) VALUES (v_user_id, true);
END IF;
```

## 游标 {#cursors}

游标允许逐行遍历查询结果集。

```sql
DECLARE
    curs1 CURSOR FOR SELECT * FROM users;
    row_var users%ROWTYPE;
BEGIN
    OPEN curs1;
    LOOP
        FETCH curs1 INTO row_var;
        EXIT WHEN NOT FOUND;
        -- Process row_var
    END LOOP;
    CLOSE curs1;
END;
```
