---
title: "在 Apache Cloudberry 中创建和管理模式"
linkTitle: "创建和管理模式"
description: "在 Apache Cloudberry 中，模式以逻辑方式组织数据库中的对象和数据。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-schemas.md"
---

模式允许数据库中存在多个同名对象（例如表），只要这些对象位于不同模式中，就不会发生冲突。

## 默认的“public”模式 {#the-default-public-schema}

每个数据库都有一个名为 *public* 的默认模式。如果不创建任何模式，则对象会在 *public* 模式中创建。所有数据库角色（用户）都拥有 *public* 模式中的 `CREATE` 和 `USAGE` 权限。创建模式时，需要向用户授予访问该模式的权限。

## 创建模式 {#create-a-schema}

使用 `CREATE SCHEMA` 命令创建新模式。例如：

```sql
=> CREATE SCHEMA myschema;
```

要在模式中创建或访问对象，请写出限定名称，由模式名和表名组成，两者之间用句点分隔。例如：

```sql
myschema.table
```

有关访问模式的信息，请参见[模式搜索路径](#schema-search-paths)。

可以创建归其他人所有的模式，例如，限制用户只能在明确定义的命名空间中执行操作。语法如下：

```sql
=> CREATE SCHEMA `schemaname` AUTHORIZATION `username`;
```

## 模式搜索路径 {#schema-search-paths}

要指定对象在数据库中的位置，请使用模式限定名称。例如：

```sql
=> SELECT * FROM myschema.mytable;
```

可以设置 `search_path` 配置参数，指定在可用模式中搜索对象的顺序。搜索路径中列出的第一个模式成为*默认模式*。如果未指定模式，则在默认模式中创建对象。

### 设置模式搜索路径 {#set-the-schema-search-path}

`search_path` 配置参数设置模式搜索顺序。`ALTER DATABASE` 命令设置搜索路径。例如：

```sql
=> ALTER DATABASE mydatabase SET search_path TO myschema, 
public, pg_catalog;
```

也可以使用 `ALTER ROLE` 命令为特定角色（用户）设置 `search_path`。例如：

```sql
=> ALTER ROLE sally SET search_path TO myschema, public, 
pg_catalog;
```

> [!TIP]
> 使用 Apache Cloudberry 时，建议：
>
> - 创建新对象时明确指定模式，以确保对象创建在预期的模式中。
> - 不要依赖 `search_path` 将新对象隐式引导到 `public` 以外的特定模式中。否则，数据库可能会将对象创建在意外的模式中。

### 查看当前模式 {#view-the-current-schema}

使用 `current_schema()` 函数查看当前模式。例如：

```sql
=> SELECT current_schema();
```

使用 `SHOW` 命令查看当前搜索路径。例如：

```sql
=> SHOW search_path;
```

## 删除模式 {#drop-a-schema}

使用 `DROP SCHEMA` 命令删除模式。例如：

```sql
=> DROP SCHEMA myschema;
```

默认情况下，必须先清空模式才能删除它。要删除模式及其全部对象（表、数据、函数等），请使用：

```sql
=> DROP SCHEMA myschema CASCADE;
```

## 系统模式 {#system-schemas}

每个数据库中都存在以下系统级模式：

- `pg_catalog` 包含系统目录表、内置数据类型、函数和操作符。即使没有在搜索路径中显式命名，它也始终属于模式搜索路径。
- `information_schema` 由一组标准化视图组成，这些视图包含数据库对象的信息。这些视图以标准化方式从系统目录表获取系统信息。
- `pg_toast` 存储超过页大小的记录等大对象。Apache Cloudberry 系统在内部使用此模式。
- `pg_bitmapindex` 存储位图索引对象，例如值列表。Apache Cloudberry 系统在内部使用此模式。
- `pg_aoseg` 存储 AO 表对象。Apache Cloudberry 系统在内部使用此模式。
- `gp_toolkit` 是一个管理模式，其中包含可以使用 SQL 命令访问的外部表、视图和函数。所有数据库用户都可以访问 `gp_toolkit`，以查看和查询系统日志文件及其他系统指标。