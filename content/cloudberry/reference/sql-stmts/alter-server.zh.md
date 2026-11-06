---
title: "ALTER SERVER"
description: "修改外部服务器的定义。"
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-server.md"
---

## 概要 {#synopsis}

```sql
ALTER SERVER <name> [ VERSION '<new_version>' ]
    [ OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ] ) ]

ALTER SERVER <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
                
ALTER SERVER <name> RENAME TO <new_name>
```

## 说明 {#description}

`ALTER SERVER` 用于修改外部服务器的定义。该命令的第一种形式修改服务器的版本字符串或通用选项。Apache Cloudberry 要求至少提供一个子句。该命令的第二种和第三种形式分别修改服务器的所有者或名称。

要修改服务器，你必须是该服务器的所有者。要修改所有者，你必须：

- 拥有该服务器。
- 是新所属角色的直接或间接成员。
- 拥有该服务器的外部数据包装器上的 `USAGE` 权限。

超级用户自动满足所有这些条件。

## 参数 {#parameters}

**`name`**

现有服务器的名称。

**`new_version`**

新的服务器版本。

**`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`**

修改服务器的选项。`ADD`、`SET` 和 `DROP` 指定要执行的操作。如果未显式指定操作，则默认操作为 `ADD`。选项名称必须唯一。Apache Cloudberry 使用服务器的外部数据包装器库来验证名称和值。

**`new_owner`**

指定外部服务器的新所有者。

**`new_name`**

指定外部服务器的新名称。

## 示例 {#examples}

通过添加连接选项来修改名为 `foo` 的服务器的定义：

```sql
ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');
```

修改名为 `foo` 的服务器的 `host` 选项，并设置服务器版本：

```sql
ALTER SERVER foo VERSION '9.1' OPTIONS (SET host 'baz');
```

## 兼容性 {#compatibility}

`ALTER SERVER` 符合 ISO/IEC 9075-9（SQL/MED）。`OWNER TO` 和 `RENAME` 形式是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/)、[DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/)
