---
title: "CREATE ACCESS METHOD"
description: "Defines a new access method."
weight: 520
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-access-method.md"
---

## Synopsis {#synopsis}

```sql
CREATE ACCESS METHOD <name>
    TYPE <access_method_type>
    HANDLER <handler_function>
```

## Description {#description}

`CREATE ACCESS METHOD` creates a new access method.

The access method name must be unique within the database.

Only superusers can define new access methods.

## Parameters {#parameters}

**`name`**

The name of the access method to create.

**`access_method_type`**

The type of access method to define. Only `TABLE` and `INDEX` types are supported at present.

**`handler_function`**

handler_function is the name (possibly schema-qualified) of a previously registered function that represents the access method. The handler function must be declared to take a single argument of type `internal`, and its return type depends on the type of access method; for `TABLE` access methods, it must be `table_am_handler` and for `INDEX` access methods, it must be `index_am_handler`. The C-level API that the handler function must implement varies depending on the type of access method. The table access method API is described in [Table Access Method Interface Definition](https://www.postgresql.org/docs/12/tableam.html) in the PostgreSQL documentation. The index access method API is described in [Index Access Method Interface Definition](https://www.postgresql.org/docs/12/indexam.html).

## Examples {#examples}

Create an index access method `heptree` with handler function `heptree_handler`:

``` sql
CREATE ACCESS METHOD heptree TYPE INDEX HANDLER heptree_handler;
```

## Compatibility {#compatibility}

`CREATE ACCESS METHOD` is a Apache Cloudberry extension.

## See also {#see-also}

[DROP ACCESS METHOD](/cloudberry/reference/sql-stmts/drop-access-method/), [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/), [CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/)
