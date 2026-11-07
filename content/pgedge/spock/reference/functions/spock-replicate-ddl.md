---
title: spock.replicate_ddl()
description: spock.replicateddl (command text[], replicationsets text[], searchpath text, role text)
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_replicate_ddl.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
type: docs
---



spock.replicate_ddl()

## SYNOPSIS {#synopsis}

spock.replicate_ddl (command text[], replication_sets text[], search_path text,
role text)

## RETURNS {#returns}

  - true if the DDL command was successfully executed and queued for
    replication.

  - false if the command execution fails or replication queueing fails.

When called with a text array, returns a set of boolean values, one for
each command in the array.

## DESCRIPTION {#description}

Executes DDL commands locally and queues them for replication to subscribers.

This function runs the specified DDL command on the local node first, then
adds it to the replication queue for execution on all subscriber nodes that
are subscribed to one of the specified replication sets.

The function accepts either a single DDL command as text or an array of DDL
commands. When provided with an array, each command is executed and queued
sequentially.

The search_path and role parameters allow you to control the execution
context for the DDL command on both the provider and subscriber nodes.

This function writes to the replication queue and modifies the database
schema locally before propagating changes.

This command must be executed by a user with sufficient privileges to execute
the DDL command.

## ARGUMENTS {#arguments}

command

    A DDL command as text, or an array of DDL commands to execute and
    replicate.

replication_sets

    An array of replication set names. Only subscribers subscribed to one
    of these sets will receive and execute the DDL. Default is '{ddl_sql}'.

search_path

    The schema search path to use when executing the DDL command. Default
    is the current session's search_path setting.

role

    The role (user) under which to execute the DDL command. Default is the
    current user.

## EXAMPLES {#examples}

    The following command creates a table and instructs Spock to replicate the
    DDL to other nodes:

    postgres=# SELECT spock.replicate_ddl('CREATE TABLE users (id SERIAL PRIMARY KEY,
        name TEXT)');
    -[ RECORD 1 ]-+--
    replicate_ddl | t

    The following command alters the table adding a column, and instructs Spock
    to replicate the DDL to other nodes:

    postgres=# SELECT spock.replicate_ddl('ALTER TABLE users ADD COLUMN email TEXT',
        '{default,ddl_sql}');
    -[ RECORD 1 ]-+--
    replicate_ddl | t

    The following command creates a table and an index on the tables, and
    instructs Spock to replicate DDL to other nodes:

    postgres=# SELECT spock.replicate_ddl(ARRAY['CREATE TABLE orders (id SERIAL)',
        'CREATE INDEX ON orders(id)']);
    -[ RECORD 1 ]-+--
    replicate_ddl | t
    -[ RECORD 2 ]-+--
    replicate_ddl | t

---

[Upstream source](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/spock_functions/functions/spock_replicate_ddl.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL License](/pgedge/about/license/).
