---
title: "pg_rewrite"
description: "The `pg_rewrite` system catalog table stores rewrite rules for tables and views."
weight: 320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-rewrite.md"
---

`pg_class.relhasrules` must be true if a table has any rules in this catalog.

|column|type|references|description|
|------|----|----------|-----------|
|`oid`|oid| |The object ID|
|`rulename`|name||Rule name|
|`ev_class`|oid|pg_class.oid|The table this rule is for|
|`ev_type`|char||Event type that the rule is for: 1 = SELECT, 2 = UPDATE, 3 = INSERT, 4 = DELETE|
|`ev_enabled`|char||Controls in which session replication role mode the rule fires. Always O, rule fires in origin mode.|
|`is_instead`|boolean||True if the rule is an `INSTEAD` rule|
|`ev_qual`|pg_node_tree||Expression tree (in the form of a `nodeToString()` representation) for the rule's qualifying condition|
|`ev_action`|pg_node_tree||Query tree (in the form of a `nodeToString()` representation) for the rule's action|
