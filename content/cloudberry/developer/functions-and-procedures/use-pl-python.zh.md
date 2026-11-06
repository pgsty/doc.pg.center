---
title: "使用 PL/Python"
description: "PL/Python 是一种嵌入式过程语言，允许使用 Python 编程语言编写 PostgreSQL 函数。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-python.md"
---

Apache Cloudberry 支持使用 Python 3 的 PL/Python。

使用 PL/Python 可以：

- 用 Python 编写函数，并从 SQL 调用这些函数。
- 使用 Python 丰富的标准库和第三方模块。
- 通过 `plpy` 模块访问数据库。

## 启用 PL/Python {#enable-plpython}

要使用 PL/Python，必须在数据库中启用它。Apache Cloudberry 使用不受信任的 `plpython3u` 语言，该语言提供对系统的完全访问权限。

1. 使用 `psql` 连接数据库。

    ```bash
    psql -d <database_name>
    ```

2. 创建 `plpython3u` 扩展。

    ```sql
    CREATE EXTENSION plpython3u;
    ```

    > [!NOTE]
    > 由于 PL/Python 是不受信任的语言（后缀为 `u`），只有数据库超级用户才能使用它创建函数。这是因为它允许访问文件系统和其他系统资源。

## 编写 PL/Python 函数 {#write-plpython-functions}

使用标准 SQL `CREATE FUNCTION` 语法定义 PL/Python 函数。函数体是 Python 代码。

```sql
CREATE FUNCTION py_max (a integer, b integer)
RETURNS integer
AS $$
    if a > b:
        return a
    return b
$$ LANGUAGE plpython3u;
```

### 参数和结果 {#arguments-and-results}

- 参数以与参数名匹配的变量形式传入。
- 也可以通过 `args` 列表访问参数。
- 返回值会自动处理。Python 的 `None` 会映射为 SQL 的 `NULL`。

### 数据类型映射 {#data-type-mapping}

Apache Cloudberry 会自动将 SQL 类型映射为 Python 类型。

| SQL 类型 | Python 类型 |
| :--- | :--- |
| `boolean` | `bool` |
| `integer`、`bigint` | `int` |
| `real`、`double precision` | `float` |
| `text`、`varchar` | `str` |
| `bytea` | `bytes` |
| `Array` | `list` |
| `Composite Type` | 输入为 `dict`，输出为 `tuple`/`dict` |

返回复合类型的示例：

```sql
CREATE TYPE type_record AS (first text, second int4);

CREATE FUNCTION return_composite()
RETURNS type_record
AS $$
    return {'first': 'hello', 'second': 42}
$$ LANGUAGE plpython3u;
```

## 内置函数 {#built-in-functions}

`plpy` 模块提供了与数据库交互的方法。

- `plpy.execute(query [, limit])`：执行 SQL 查询。
- `plpy.prepare(query, argtypes)`：准备查询执行计划。
- `plpy.info(msg)`、`plpy.error(msg)`：记录消息。

使用 `plpy.execute` 的示例：

```sql
CREATE FUNCTION get_user_name(id int)
RETURNS text
AS $$
    res = plpy.execute(f"SELECT username FROM users WHERE id = {id}")
    if res:
        return res[0]['username']
    return None
$$ LANGUAGE plpython3u;
```

## 安装 Python 模块 {#install-python-modules}

可以在 PL/Python 函数中使用第三方 Python 模块。必须在集群的所有主机（Coordinator 和 Segment）上安装该模块。

在每台主机上使用 `pip` 安装模块：

```bash
gpssh -f <hostfile> "pip3 install <module_name>"
```

然后即可在函数中导入该模块：

```sql
CREATE FUNCTION use_numpy()
RETURNS float
AS $$
    import numpy as np
    return np.mean([1, 2, 3, 4])
$$ LANGUAGE plpython3u;
```
