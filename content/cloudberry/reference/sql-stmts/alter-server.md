---
title: "ALTER SERVER"
description: "Changes the definition of a foreign server."
weight: 300
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-server.md"
---

## Synopsis {#synopsis}

```sql
ALTER SERVER <name> [ VERSION '<new_version>' ]
    [ OPTIONS ( [ ADD | SET | DROP ] <option> ['<value>'] [, ... ] ) ]

ALTER SERVER <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
                
ALTER SERVER <name> RENAME TO <new_name>
```

## Description {#description}

`ALTER SERVER` changes the definition of a foreign server. The first form of the command changes the version string or the generic options of the server. Apache Cloudberry requires at least one clause. The second and third forms of the command change the owner or the name of the server.

To alter the server, you must be the owner of the server. To alter the owner you must:

- Own the server.
- Be a direct or indirect member of the new owning role.
- Have `USAGE` privilege on the server's foreign-data wrapper.

Superusers automatically satisfy all of these criteria.

## Parameters {#parameters}

**`name`**

The name of an existing server.

**`new_version`**

The new server version.

**`OPTIONS ( [ ADD | SET | DROP ] option ['value'] [, ... ] )`**

Change the server's options. `ADD`, `SET`, and `DROP` specify the action to perform. If no operation is explicitly specified, the default operation is `ADD`. Option names must be unique. Apache Cloudberry validates names and values using the server's foreign-data wrapper library.

**`new_owner`**

Specifies the new owner of the foreign server.

**`new_name`**

Specifies the new name of the foreign server.

## Examples {#examples}

Change the definition of a server named `foo` by adding connection options:

```sql
ALTER SERVER foo OPTIONS (host 'foo', dbname 'foodb');
```

Change the option named `host` for a server named `foo`, and set the server version:

```sql
ALTER SERVER foo VERSION '9.1' OPTIONS (SET host 'baz');
```

## Compatibility {#compatibility}

`ALTER SERVER` conforms to ISO/IEC 9075-9 (SQL/MED). The `OWNER TO` and `RENAME` forms are Apache Cloudberry extensions.

## See also {#see-also}

[CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/), [DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/)
