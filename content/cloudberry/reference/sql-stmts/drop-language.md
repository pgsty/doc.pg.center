---
title: "DROP LANGUAGE"
description: "Removes a procedural language."
weight: 1140
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/drop-language.md"
---

## Synopsis {#synopsis}

```sql
DROP [PROCEDURAL] LANGUAGE [IF EXISTS] <name> [CASCADE | RESTRICT]
```

## Description {#description}

`DROP LANGUAGE` removes the definition of the previously registered procedural language. You must be a superuser or owner of the language to drop a language.

## Parameters {#parameters}

**`PROCEDURAL`**

Optional keyword - has no effect.

**`IF EXISTS`**

Do not throw an error if the language does not exist. A notice is issued in this case.

**`name`**

The name of an existing procedural language. For backward compatibility, the name may be enclosed by single quotes.

**`CASCADE`**

Automatically drop objects that depend on the language (such as functions written in that language), and in turn all objects that depend on those objects.

**`RESTRICT`**

Refuse to drop the language if any objects depend on it. This is the default.

## Examples {#examples}

Remove the procedural language `plsample`:

```sql
DROP LANGUAGE plsample;
```

## Compatibility {#compatibility}

There is no `DROP LANGUAGE` statement in the SQL standard.

## See also {#see-also}

[ALTER LANGUAGE](/cloudberry/reference/sql-stmts/alter-language/), [CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/)
