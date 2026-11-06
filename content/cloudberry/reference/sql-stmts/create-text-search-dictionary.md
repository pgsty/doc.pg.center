---
title: "CREATE TEXT SEARCH DICTIONARY"
description: "Defines a new text search dictionary."
weight: 860
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-text-search-dictionary.md"
---

## Synopsis {#synopsis}

```sql
CREATE TEXT SEARCH DICTIONARY <name> (
    TEMPLATE = <template>
    [, <option> = <value> [, ... ]]
)
```

## Description {#description}

CREATE TEXT SEARCH DICTIONARY creates a new text search dictionary. A text search dictionary specifies a way of recognizing interesting or uninteresting words for searching. A dictionary depends on a text search template, which specifies the functions that actually perform the work. Typically the dictionary provides some options that control the detailed behavior of the template's functions.

If a schema name is given then the text search dictionary is created in the specified schema. Otherwise it is created in the current schema.

The user who defines a text search dictionary becomes its owner.

## Parameters {#parameters}

**`name`**

The name of the text search dictionary to be created. The name can be schema-qualified.

**`template`**

The name of the text search template that will define the basic behavior of this dictionary.

**`option`**

The name of a template-specific option to be set for this dictionary.

**`value`**

The value to use for a template-specific option. If the value is not a simple identifier or number, it must be quoted (but you can always quote it, if you wish).

The options can appear in any order.

## Examples {#examples}

The following example command creates a Snowball-based dictionary with a nonstandard list of stop words.

```sql
CREATE TEXT SEARCH DICTIONARY my_russian (
    template = snowball,
    language = russian,
    stopwords = myrussian
);
```

## Compatibility {#compatibility}

There is no `CREATE TEXT SEARCH DICTIONARY` statement in the SQL standard.

## See also {#see-also}

[ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/), [DROP TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/drop-text-search-dictionary/)
