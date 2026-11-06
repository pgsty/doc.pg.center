---
title: "创建与管理 Apache Cloudberry 数据库"
linkTitle: "创建与管理数据库"
description: "一个 Apache Cloudberry 系统就是一个 Apache Cloudberry 实例。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/database-basic/create-and-manage-database.md"
---

多个 Apache Cloudberry 系统可以同时运行，但客户端通常只能连接其中一个系统。

一个 Apache Cloudberry 系统中可以有多个数据库。这与某些数据库管理系统（如 Oracle）不同；在这些系统中，数据库实例*就是*数据库。虽然可以在一个 Apache Cloudberry 系统中创建多个数据库，但客户端程序一次只能连接和访问一个数据库，不能跨数据库查询。

## 模板数据库与默认数据库 {#about-template-and-default-databases}

Apache Cloudberry 提供了模板数据库和默认数据库：*template1*、*template0* 和 *postgres*。

默认情况下，新建数据库都基于 *template1* 数据库。除非指定其他模板，否则 Apache Cloudberry 会使用 *template1* 创建数据库。不建议在 *template1* 中创建对象，因为使用默认模板数据库创建的每个数据库都会包含这些对象。

Apache Cloudberry 在内部使用另一个数据库模板 *template0*。不要删除或修改 *template0*。可以使用 *template0* 创建一个完全干净的数据库，其中只包含 Apache Cloudberry 在初始化时预定义的标准对象。

首次连接 Apache Cloudberry 时，可以使用 *postgres* 数据库。Apache Cloudberry 将 *postgres* 用作管理连接的默认数据库。

## 创建数据库 {#create-a-database}

`CREATE DATABASE` 命令用于创建新数据库。例如：

```sql
=> CREATE DATABASE <new_dbname>;
```

要创建数据库，必须具有创建数据库的权限，或是 Apache Cloudberry 超级用户。如果没有相应权限，就无法创建数据库。请联系 Apache Cloudberry 管理员，由其授予你所需的权限或代为创建数据库。

也可以使用客户端程序 `createdb` 创建数据库。例如，在命令行终端中运行以下命令，会使用给定的主机名和端口连接 Apache Cloudberry，并创建名为 *mydatabase* 的数据库：

```shell
$ createdb -h coordinator_host -p 5432 mydatabase
```

主机名和端口必须与已安装的 Apache Cloudberry 系统的主机名和端口一致。

某些对象（如角色）由 Apache Cloudberry 系统中的所有数据库共享。其他对象（如你创建的表）仅在创建它们的数据库中可见。

> [!WARNING] 警告
> `CREATE DATABASE` 命令不具备事务性。

### 克隆数据库 {#clone-a-database}

默认情况下，新数据库通过克隆标准系统数据库模板 *template1* 创建。创建新数据库时，可以使用任何数据库作为模板，从而“克隆”或复制现有数据库及其中的所有对象和数据。例如：

```sql
=> CREATE DATABASE <new_dbname> TEMPLATE <old_dbname>;
```

### 创建由其他用户拥有的数据库 {#create-a-database-with-a-different-owner}

创建数据库时，可以指定其他用户作为数据库所有者：

```sql
=> CREATE DATABASE <new_dbname> WITH <owner=new_user>;
```

## 查看数据库列表 {#view-the-list-of-databases}

如果使用 `psql` 客户端程序，可以通过 `\l` 元命令显示 Apache Cloudberry 系统中的数据库和模板列表。如果使用其他客户端程序且具有超级用户权限，可以从 `pg_database` 系统目录表中查询数据库列表。例如：

```sql
=> SELECT datname from pg_database;
```

## 修改数据库 {#alter-a-database}

`ALTER DATABASE` 命令用于修改数据库的所有者、名称、默认配置等属性。例如，以下命令通过设置默认模式搜索路径（`search_path` 配置参数）来修改数据库：

```sql
=> ALTER DATABASE mydatabase SET search_path TO myschema, public, pg_catalog;
```

要修改数据库，必须是数据库所有者或超级用户。

## 删除数据库 {#drop-a-database}

`DROP DATABASE` 命令用于删除数据库。它会移除该数据库的系统目录条目，并删除磁盘上存放数据的数据库目录。只有数据库所有者或超级用户才能删除数据库，而且当你或其他用户仍连接该数据库时，不能将其删除。删除数据库前，请先连接 `postgres`（或其他数据库）。例如：

```sql
=> \c postgres
=> DROP DATABASE mydatabase;
```

也可以使用客户端程序 `dropdb` 删除数据库。例如，以下命令使用给定的主机名和端口连接 Apache Cloudberry，并删除数据库 *mydatabase*：

```shell
$ dropdb -h coordinator_host -p 5432 mydatabase
```

> [!WARNING] 警告
> 删除数据库的操作无法撤销。

`DROP DATABASE` 命令不具备事务性。
