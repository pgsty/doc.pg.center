---
title: 自动把表分配到复制集
description: 使用事件触发器按模式和来源自动把新表加入 Spock 复制集。
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/repset_trigger.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



自动 DDL 复制是使用触发器管理复制集的很好的替代方案；但如果你确实需要动态修改复制规则、列或行过滤器，或分区过滤器，这个触发器可能会有用。这个触发器不会跨节点复制 DDL 语句，而是在触发它的节点上自动把新建的表加入复制集。

使用触发器之前，你应修改它，以覆盖你可能运行的所有形式的 `CREATE TABLE` 语句。由于触发器在事务中执行，如果触发器中的代码失败，事务会回滚，包括导致触发器触发的任何 `CREATE TABLE` 语句。这意味着，如果触发器失败，`CREATE UNLOGGED TABLE` 这样的语句也会失败。

请注意，使用触发器时，必须确保禁用了 DDL 命令的自动复制。你可以在 PSQL 命令行使用以下命令禁用自动 DDL 更新：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication=off;
ALTER SYSTEM SET spock.include_ddl_repset=off;
ALTER SYSTEM SET spock.allow_ddl_from_functions=off;
SELECT pg_reload_conf();
```

你可以使用事件触发器设施描述为新建表定义复制集的规则。例如：

```sql
    CREATE OR REPLACE FUNCTION spock_assign_repset()
    RETURNS event_trigger AS $$
    DECLARE obj record;
    BEGIN
        FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands()
        LOOP
            IF obj.object_type = 'table' THEN
                IF obj.schema_name = 'config' THEN
                    PERFORM spock.repset_add_table('configuration', obj.objid);
                ELSIF NOT obj.in_extension THEN
                    PERFORM spock.repset_add_table('default', obj.objid);
                END IF;
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;

    CREATE EVENT TRIGGER spock_assign_repset_trg
        ON ddl_command_end
        WHEN TAG IN ('CREATE TABLE', 'CREATE TABLE AS')
        EXECUTE FUNCTION spock_assign_repset();
```

上面展示的代码片段会把在 `config` 模式中创建的任何新表加入名为 `configuration` 的复制集，并把所有其他新表（不是由扩展创建的表）加入 `default` 复制集。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/repset_trigger.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
