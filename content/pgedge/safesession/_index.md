---
title: SafeSession
description: pgEdge SafeSession is a PostgreSQL extension that enforces read-only sessions for specified database
  roles.
weight: 40
upstream_source: pgedge-safesession
upstream_link: https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/index.md
upstream_modified: true
upstream_ref: b406cd1e82cf
source_kind: pinned-main-snapshot
linkTitle: SafeSession
icon: fa-solid fa-book-open
sidebar_root_for: self
no_list: true
type: docs
sidebar_root_menu: false
---


> [!NOTE] Source version
> This is a pinned snapshot of upstream `main`; it may differ from the versioned documentation website. Check [versions and sources](/pgedge/about/attribution/) before deploying.


pgEdge SafeSession is a PostgreSQL extension that enforces
read-only sessions for specified database roles. It provides
defense-in-depth protection using executor and utility hooks
to block all write operations, DDL, and other potentially
dangerous commands.

## Features {#features}

- Block DML (INSERT, UPDATE, DELETE, MERGE) for restricted
  roles
- Block DDL (CREATE, ALTER, DROP, TRUNCATE, etc.)
- Block COPY FROM and COPY TO PROGRAM
- Block GRANT/REVOKE, VACUUM/ANALYZE
- Block volatile C-language function execution (which can
  bypass the executor)
- Prevent tampering with read-only GUC settings
- Role membership inheritance: members of restricted roles
  are also restricted
- Superuser exemption: superusers are never restricted, even
  if they are members of restricted roles
- Session-user anchored: SET ROLE cannot escape restrictions
- Configurable protection layers via GUCs

## Requirements {#requirements}

- PostgreSQL 14 or later
- Must be loaded via `shared_preload_libraries`

## Installation {#installation}

### Build from Source {#build-from-source}

```bash
make
make install
```

### Configure PostgreSQL {#configure-postgresql}

Add the extension to `shared_preload_libraries` in
`postgresql.conf`:

```
shared_preload_libraries = 'pgedge_safesession'
```

Restart PostgreSQL for the change to take effect.

### Create the Extension (Optional) {#create-the-extension-optional}

The extension is fully functional once loaded via
`shared_preload_libraries`. Running `CREATE EXTENSION` is
optional, but registers it in the `pg_extension` catalog
so it appears in `\dx` output:

```sql
CREATE EXTENSION pgedge_safesession;
```

## Configuration {#configuration}

All GUCs are SUSET parameters (only superusers can modify
them).

### `pgedge_safesession.roles` {#pgedge_safesessionroles}

A comma-separated list of PostgreSQL role names whose
sessions will be restricted to read-only operations.

```sql
ALTER SYSTEM SET pgedge_safesession.roles =
    'readonly_user, reporting_role';
SELECT pg_reload_conf();
```

Any session authenticated as one of these roles, or as a
role that is a member of one of these roles, will be
restricted to read-only operations.

### `pgedge_safesession.block_dml` {#pgedge_safesessionblock_dml}

Default: `on`

Block INSERT, UPDATE, DELETE, and MERGE for restricted
roles.

### `pgedge_safesession.block_ddl` {#pgedge_safesessionblock_ddl}

Default: `on`

Block DDL and other utility commands for restricted roles.
Uses a whitelist approach: only explicitly allowed
statements (SELECT, EXPLAIN, transaction control, SET,
SHOW, LISTEN/NOTIFY, cursors, DO blocks) can execute.

### `pgedge_safesession.block_c_functions` {#pgedge_safesessionblock_c_functions}

Default: `on`

Block C-language function execution for restricted roles.
By default, only **volatile** C functions are blocked.
IMMUTABLE and STABLE C functions (such as PostGIS geometry
operations or pgvector distance operators) are allowed
since they promise no side effects.

### `pgedge_safesession.block_all_c_functions` {#pgedge_safesessionblock_all_c_functions}

Default: `off`

When enabled, blocks **all** C-language functions
regardless of volatility. This provides stricter
protection at the cost of blocking read-only extension
functions. Only applies when `block_c_functions` is on.

## What is Blocked {#what-is-blocked}

For restricted sessions (with all protections enabled),
the following operations are blocked:

- **DML**: INSERT, UPDATE, DELETE, MERGE (PostgreSQL 15+),
  including data-modifying CTEs
  (`WITH c AS (INSERT ... RETURNING ...) ...`)
- **DDL**: CREATE, ALTER, DROP, TRUNCATE, and all other
  schema modification commands
- **COPY FROM**: data import (COPY TO is allowed)
- **COPY TO PROGRAM**: program execution via COPY
- **CREATE TABLE AS / SELECT INTO**: table creation from
  queries, including their `EXPLAIN ANALYZE` forms
- **EXPLAIN ANALYZE of a writing statement**: it executes
  the statement, so it is treated as a write
- **GRANT / REVOKE**: privilege modifications
- **VACUUM / ANALYZE**: maintenance commands
- **CHECKPOINT**: forces heavy I/O and emits WAL
- **Two-phase commit**: PREPARE TRANSACTION, COMMIT
  PREPARED, ROLLBACK PREPARED
- **Side-effecting functions**: volatile functions in
  untrusted languages (C, internal, or an untrusted PL
  such as `plpython3u`), plus any volatile built-in
  (`pg_catalog`) function that is not on a small allow-list
  of built-ins confirmed to have no observable side effect
  (`random()`, `clock_timestamp()`, and similar). A volatile
  built-in is blocked by default; only functions verified
  harmless are exempted, so a new PostgreSQL release that
  adds a side-effecting built-in is blocked automatically.
  A `DO` block or `CALL` in an untrusted language is
  blocked for the same reason. Arguments count as part of
  the statement, so a blocked function is rejected whether
  it is called directly, passed as a `CALL` argument, or
  passed as an `EXECUTE` parameter (including through
  `EXPLAIN EXECUTE` and `CREATE TABLE AS ... EXECUTE`). A
  function reached only indirectly, through a view body, a
  row-level security policy's `USING`/`WITH CHECK` qual, or
  a domain `CHECK` constraint, is rejected the same way as a
  direct call. For a domain this holds however the coercion
  that runs the constraint is reached: a cast, a prepared
  statement's declared parameter type, a parameter bound
  over the extended query protocol, a PL/pgSQL variable's
  declared type, or a function's `RETURNS` type.
- **Fast-path function calls**: the protocol behind libpq's
  `PQfn`, which the large-object client API is built on. It
  bypasses the parser and planner entirely, so the same
  function policy is applied to it directly.
- **Exclusive locks**: LOCK TABLE with modes above
  ROW SHARE
- **GUC tampering**: any attempt to relax
  `transaction_read_only` or `default_transaction_read_only`,
  whether by setting one of them to a false value, by
  RESET or SET TO DEFAULT, or through SET TRANSACTION READ
  WRITE and SET SESSION CHARACTERISTICS AS TRANSACTION READ
  WRITE

## What is Allowed {#what-is-allowed}

- **SELECT**: all read queries, including those using
  WHERE clauses, aggregates, and built-in functions
- **EXPLAIN**: query plans. Plain EXPLAIN only plans and
  is always allowed; EXPLAIN ANALYZE is allowed only when
  the statement it runs does not write.
- **Transaction control**: BEGIN, COMMIT, ROLLBACK,
  SAVEPOINT
- **SET / RESET**: non-protected GUC changes
  (e.g., work_mem)
- **SET TRANSACTION**: ISOLATION LEVEL and READ ONLY
  (tightening the transaction is allowed)
- **Asserting read-only**: setting `transaction_read_only`
  or `default_transaction_read_only` to on, which asks for
  the state that is already enforced. Clients that assert
  read-only on every connection they open, such as a
  connection pool with writes disabled, therefore work
  against restricted roles.
- **SHOW**: display settings
- **LISTEN / NOTIFY**: notification channels
- **Cursors**: DECLARE, FETCH, CLOSE
- **Connection-pooler resets**: DISCARD ALL, DISCARD
  PLANS, and RESET ALL (they cannot relax the restriction,
  which is re-asserted per statement)
- **DO blocks and CALL**: in a trusted language (PL/pgSQL,
  SQL, ...); any write inside is caught by the executor
  hook
- **PL/pgSQL and SQL functions**: read-only functions
  execute normally; any write attempt inside a function
  is caught by the executor hook, and a blocked function
  called from a SQL function body is rejected before the
  call runs
- **IMMUTABLE/STABLE functions**, and harmless volatile
  built-ins such as `random()` and `clock_timestamp()`

## Security Model {#security-model}

### Session User is the Anchor {#session-user-is-the-anchor}

The session user identity (set at connection time) is the
primary check. Even if a restricted user executes
`SET ROLE` to assume another role, the session user remains
restricted. This prevents bypass via role switching.

### Superuser Exemption {#superuser-exemption}

Superusers are never restricted, even if they are members
of a restricted role. The superuser check is based on the
session user, so SECURITY DEFINER functions owned by
superusers cannot bypass restrictions when called from a
restricted session.

### SECURITY DEFINER Functions {#security-definer-functions}

A SECURITY DEFINER function temporarily changes the
effective user to the function owner. However, SafeSession
checks the session user, not the effective user. This
means a restricted session cannot use a SECURITY DEFINER
function owned by a privileged user to perform writes.

### Role Membership Inheritance {#role-membership-inheritance}

If role `app_reader` is listed in
`pgedge_safesession.roles`, then any role that is a member
of `app_reader` is also restricted. Membership is tested
with PostgreSQL's `is_member_of_role_nosuper()`, so it
follows actual grants only.

The distinction matters because PostgreSQL otherwise reports
a superuser as a member of every role in the database, with
no grant behind it, which is the right answer for a
privilege test and the wrong one here. Any mechanism that
briefly makes the current user a superuser whilst the
session user is not, such as a SECURITY DEFINER function
owned by a superuser or an extension like supautils
elevating a privileged role for a single command, would
otherwise appear to be acting as a member of every
restricted role and be blocked. Enforcement still anchors on
the session user, so such elevation is not a way out of the
restriction either: a restricted session stays restricted
inside a superuser-owned SECURITY DEFINER function.

### Restriction Changes and Cached Plans {#restriction-changes-and-cached-plans}

Side-effecting function calls are detected when a statement
or expression is parsed, and again when it is planned (to
catch a function reached only through a view body or an RLS
qual, which are substituted during query rewrite, after
parse analysis), rather than when it is executed, so a plan
cached before a session became restricted would otherwise be
replayed without either check running again. That matters
because a session can become restricted part-way through its
life: the roles list can be edited and the configuration
reloaded, or a role can be granted membership of a listed
role, whilst sessions are open.

Becoming restricted is therefore treated as an invalidation
event, and the session's cached plans are discarded exactly
as `DISCARD PLANS` does, so that everything is re-analysed
under the new state. This covers prepared statements and the
plans PL/pgSQL caches for its expressions alike. Plans built
whilst a session was restricted are left alone when the
restriction is lifted, since they have already been checked.

### Belt-and-Suspenders {#belt-and-suspenders}

For every restricted session SafeSession also forces the
current transaction read-only (`XactReadOnly`), re-asserted
on each statement. This provides an additional layer of
protection that cannot be turned off: even if something
bypasses the hooks and attempts direct heap writes,
PostgreSQL's own internal read-only checks will catch it.
The setting is applied without writing any session-level
GUC, so it leaves no state behind and does not interfere
with connection poolers.

## Known Limitations {#known-limitations}

- The allow-list of harmless volatile built-in functions is
  deliberately conservative rather than exhaustive: a
  volatile built-in that is actually harmless but missing
  from the list is blocked anyway, which can surface as a
  restricted session being refused a read-only built-in
  call that a future release should add to the list. This
  is a usability trade-off in favour of failing closed: a
  newly added side-effecting built-in is blocked by default
  rather than silently allowed. A volatile function in a
  trusted language is allowed to run, and any write it
  performs is caught at execution instead.
- Enforcement anchors on the session user. A superuser can
  still use `SET SESSION AUTHORIZATION` to become a
  restricted role (that is how the restriction is entered);
  this is by design and is not a bypass.
- The roles list must be set from the server configuration
  (`shared_preload_libraries` is required, and the roles
  are normally set in `postgresql.conf` or with
  `ALTER SYSTEM`). Setting it only for a single session
  with `SET` would be undone by that session's `DISCARD
  ALL` or `RESET ALL`.
- SafeSession and Spock both install executor, utility, and
  planner hooks. They chain correctly, but if both are
  deployed the interaction has not been exhaustively tested.
- A blocked function is caught either when it appears in a
  statement's parse tree or when the executor compiles it as
  part of an expression. A function PostgreSQL calls directly
  through `fmgr`, without compiling an expression around it,
  is seen by neither: a type's own input and output
  functions, and an index access method's support functions,
  are the cases that arise in practice. Reaching one requires
  a type or operator class that somebody else defined, since
  a restricted role cannot create either.

## Example {#example}

```sql
-- As superuser: configure restrictions
ALTER SYSTEM SET pgedge_safesession.roles =
    'reporting_user';
SELECT pg_reload_conf();

-- Connect as reporting_user
-- Reads work normally:
SELECT * FROM sales;          -- OK
SELECT count(*) FROM sales;   -- OK
EXPLAIN SELECT * FROM sales;  -- OK
COPY sales TO '/tmp/out.csv'; -- OK

-- Writes are blocked:
INSERT INTO sales VALUES (1); -- ERROR
CREATE TABLE tmp (id int);    -- ERROR
COPY sales FROM '/tmp/in.csv'; -- ERROR
```

## Licence {#licence}

See the [Licence](/pgedge/safesession/licence/) page for details.

## Continue reading {#continue-reading}

- [LICENCE](/pgedge/safesession/licence/)
- [Changelog](/pgedge/safesession/changelog/)

---

[Upstream source](https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/index.md) · `b406cd1e82cf` · Copyright (c) 2025–2026, pgEdge, Inc. [PostgreSQL License](/pgedge/about/license/).
