---
title: "ALTER LANGUAGE"
description: "Changes the definition of a procedural language."
weight: 150
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-language.md"
---

## Synopsis {#synopsis}

```sql
ALTER [ PROCEDURAL ] LANGUAGE <name> RENAME TO <new_name>
ALTER [ PROCEDURAL ] LANGUAGE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
```

## Description {#description}

`ALTER LANGUAGE` changes the definition of a procedural language for a specific database. Definition changes supported include renaming the language or assigning a new owner. You must be superuser or the owner of the language to use `ALTER LANGUAGE`.

## Parameters {#parameters}

**`name`**

Name of a language.

**`new_name`**

The new name of the language.

**`new_owner`**

The new owner of the language.

## Compatibility {#compatibility}

There is no `ALTER LANGUAGE` statement in the SQL standard.

## See also {#see-also}

[CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/), [DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/)
