---
title: "CREATE EXTENSION"
description: "在 Apache Cloudberry 中注册一个扩展。"
weight: 590
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-extension.md"
---

## 概要 {#synopsis}

```sql
CREATE EXTENSION [ IF NOT EXISTS ] <extension_name>
  [ WITH ] [ SCHEMA <schema_name> ]
           [ VERSION <version> ]
           [ FROM <old_version> ]
           [ CASCADE ]
```

## 描述 {#description}

`CREATE EXTENSION` 将一个新的扩展加载到当前数据库中。不能已经加载了同名的扩展。

加载扩展本质上就是运行扩展脚本文件。该脚本通常会创建新的 SQL 对象，例如函数、数据类型、操作符和索引支持方法。`CREATE EXTENSION` 还会记录所有已创建对象的标识，以便在发出 `DROP EXTENSION` 时可以再次删除它们。

加载扩展需要与创建其组成对象相同的权限。对于大多数扩展，这意味着需要超级用户或数据库所有者权限。运行 `CREATE EXTENSION` 的用户在之后的权限检查中成为该扩展的所有者，同时也是扩展脚本所创建的任何对象的所有者。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果已存在同名的扩展，不抛出错误。这种情况下 Apache Cloudberry 会发出一条提示。注意，不保证现有的扩展与根据当前可用的脚本文件本应创建的扩展有任何相似之处。

**`extension_name`**

要安装的扩展的名称。Apache Cloudberry 将使用文件 `SHAREDIR/extension/<extension_name>.control` 中的详细信息创建扩展。

`SHAREDIR` 是安装的共享数据目录，例如 `/usr/local/cloudberry/share/postgresql`。命令 `pg_config --sharedir` 会显示该目录。

**`schema_name`**

安装扩展对象所在的模式的名称，前提是该扩展允许其内容被重新定位。所指定的模式必须已经存在。如果未指定，并且扩展的控制文件也没有指定模式，则使用当前的默认对象创建模式。

如果扩展在其控制文件中指定了 schema 参数，则该模式不能被 `SCHEMA` 子句覆盖。通常，如果给出了 `SCHEMA` 子句且与扩展的 `schema` 参数冲突，就会引发错误。但是，如果同时给出了 `CASCADE` 子句，则在冲突时会忽略 schema_name。所给出的 schema_name 用于安装任何在其控制文件中未指定模式的所需扩展。

请记住，扩展本身不被视为位于任何模式之内：扩展具有不带限定的名称，这些名称在整个数据库范围内必须唯一。但属于扩展的对象可以位于模式之内。

**`version`**

要安装的扩展版本。可以写成标识符或字符串字面量。默认版本是扩展控制文件中指定的版本。

**`old_version`**

仅当尝试安装一个取代*旧式*模块的扩展时，才指定 `FROM old_version`；旧式模块是一组未打包为扩展的对象。此选项使 `CREATE EXTENSION` 运行另一个安装脚本，该脚本把现有对象吸收到扩展中，而不是创建新对象。请确保 `SCHEMA` 指定包含这些已有对象的模式。
old_version 所使用的值由扩展的作者决定，如果有多个版本的旧式模块可以升级为扩展，该值可能会有所不同。

**`CASCADE`**

自动安装此扩展所依赖的、尚未安装的任何扩展。会递归检查依赖的扩展，这些依赖也会被自动安装。如果指定了 `SCHEMA` 子句，则该模式适用于该扩展以及所安装的所有依赖扩展。所指定的其他选项不会应用于自动安装的依赖扩展；特别是，始终选择它们的默认版本。

## 注解 {#notes}

在使用 `CREATE EXTENSION` 将扩展加载到数据库之前，必须先安装该扩展的支持文件。这些支持文件必须安装在所有 Apache Cloudberry 主机上的同一位置。有关创建新扩展的信息，参见 PostgreSQL 文档[将相关对象打包为扩展](https://www.postgresql.org/docs/12/extend-extensions.html)。

可以通过 pg_available_extensions 或 pg_available_extension_versions 系统视图识别当前可供加载的扩展。

> **注意：** 以超级用户身份安装扩展需要信任扩展的作者以安全的方式编写了扩展安装脚本。恶意用户不难创建特洛伊木马对象，破坏编写不够谨慎的扩展脚本之后的执行，从而使该用户获得超级用户权限。不过，特洛伊木马对象只有在脚本执行期间位于 `search_path` 中时才有危害，也就是说，它们位于扩展的安装目标模式中，或位于其所依赖的某个扩展的模式中。因此，在处理脚本未经仔细审查的扩展时，一条好的经验法则是只把它们安装到从未向、也不会向任何不受信任的用户授予 `CREATE` 权限的模式中。对它们所依赖的任何扩展也是如此。

Apache Cloudberry 随附的扩展被认为能够抵御这类安装时攻击，但少数依赖其他扩展的扩展除外。正如这些扩展的文档所述，它们应当安装到安全的模式中，或者安装到与其所依赖扩展相同的模式中，或者两者兼有。

## 示例 {#examples}

将 `hstore` 扩展安装到当前数据库中，并把它的对象放在模式 `addons` 中：

```sql
CREATE EXTENSION hstore SCHEMA addons;
```

完成同样操作的另一种方式：

```sql
SET search_path = addons;
CREATE EXTENSION hstore;
```

## 兼容性 {#compatibility}

`CREATE EXTENSION` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER EXTENSION](/cloudberry/reference/sql-stmts/alter-extension/)、[DROP EXTENSION](/cloudberry/reference/sql-stmts/drop-extension/)
