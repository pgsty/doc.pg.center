---
title: Changelog
description: All notable changes to the pgEdge SafeSession will be documented in this file.
weight: 200
upstream_source: pgedge-safesession
upstream_link: https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/changelog.md
upstream_modified: true
upstream_ref: b406cd1e82cf
source_kind: pinned-main-snapshot
type: docs
---



All notable changes to the pgEdge SafeSession will be
documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 2026-08-25 {#10---2026-08-25}

### Added {#added}

- `SECURITY.md`, documenting how to report a vulnerability

## [1.0-beta1] - 2026-08-21 {#10-beta1---2026-08-21}

### Added {#added-1}

- Initial release of pgEdge SafeSession
- GUC `pgedge_safesession.roles` (SUSET) to specify
  restricted roles
- ExecutorStart hook to block DML (INSERT, UPDATE, DELETE,
  MERGE) and C-language function execution
- ProcessUtility hook to block DDL, COPY FROM, GRANT/REVOKE,
  VACUUM/ANALYZE, exclusive locks, and GUC tampering
- Session-user anchored role checking: SET ROLE cannot escape
  restrictions
- Superuser exemption: superusers are never restricted
- Role membership inheritance via `is_member_of_role()`
- Belt-and-suspenders: automatic
  `default_transaction_read_only = on` for restricted sessions
- SECURITY DEFINER bypass prevention: session user is always
  checked regardless of effective user
- Comprehensive regression test suite covering:

    - Basic DML blocking
    - SET ROLE bypass prevention
    - PL/pgSQL and SQL function enforcement
    - DDL blocking
    - COPY FROM/TO handling
    - CREATE TABLE AS / SELECT INTO blocking
    - SECURITY DEFINER function enforcement
    - Role membership inheritance and superuser exemption
- Configurable protection layers via new SUSET GUCs:

    - `block_dml`: toggle DML blocking (default: on)
    - `block_ddl`: toggle DDL blocking (default: on)
    - `block_c_functions`: toggle C-language function
      blocking (default: on)
    - `block_all_c_functions`: block all C functions
      regardless of volatility (default: off)

- COPY TO PROGRAM blocking for restricted sessions
- SET TRANSACTION READ WRITE blocking for restricted
  sessions
- New regression tests for advanced attack vectors
  (PREPARE/EXECUTE, DO blocks, aggregates, WHERE clauses,
  SET TRANSACTION)
- New regression tests for GUC toggle behavior

### Changed {#changed}

- C-language function blocking now only blocks VOLATILE
  C functions by default. IMMUTABLE and STABLE C functions
  (e.g., PostGIS geometry operations, pgvector distance
  operators) are allowed. Use `block_all_c_functions = on`
  to restore the previous behavior of blocking all
  C functions.
- Built-in function blocking now denies any VOLATILE
  built-in by default, allowing only a curated list of
  built-ins confirmed to have no observable side effect
  (e.g., `random()`, `clock_timestamp()`). Previously,
  built-ins were allowed by default and blocked only if
  their name matched a fixed denylist, regardless of
  volatility. PostgreSQL ships hundreds of volatile
  built-ins, and the old denylist covered only a small
  fraction of them.

### Fixed {#fixed}

- A blocked function called from the body of a SQL-language
  function was not detected. `sql` is a trusted language, so
  the body was assumed to be caught downstream, which holds
  for writes but not for a built-in off the allow-list of
  safe VOLATILE built-ins, and the planner inlines a simple
  SQL function rather than re-analysing its body at call
  time. Both the old-style text body and a standard
  `BEGIN ATOMIC` body are now inspected. Read-only SQL
  functions are unaffected.
- `pg_current_xact_id()` and `txid_current()` were allowed
  for restricted sessions. Both force the transaction to
  take a real transaction ID, which a read-only transaction
  permits, so a restricted session could consume transaction
  IDs and add wraparound pressure. The `_if_assigned()`
  variants only report an ID already handed out and remain
  allowed.
- `brin_summarize_new_values()`, `brin_summarize_range()`,
  `brin_desummarize_range()` and `gin_clean_pending_list()`
  were allowed for restricted sessions. They modify index
  pages and emit WAL without going through the executor or
  any of core's read-only checks, and the table owner may
  call them, so a restricted role could write to indexes on
  tables it owns. All four are now blocked.
- The large-object read/write function family beyond
  `lo_import`/`lo_export` (`lo_get`, `loread`, `lo_open`,
  `lo_close`, `lo_lseek`, `lo_tell` and others),
  `pg_export_snapshot()`, `pg_stat_clear_snapshot()`,
  `pg_sleep()`/`pg_sleep_for()`/`pg_sleep_until()`, and
  `pg_blocking_pids()`/`pg_lock_status()` were all
  previously allowed for restricted sessions, since none
  of them appeared on the old denylist. They read or hold
  server-side state, or block the backend outright, none
  of which a read-only session should be able to do. All
  are now blocked, since none is on the new allow-list of
  VOLATILE built-ins.
- Cached plans were not discarded when a role was granted
  membership of a listed role. `GRANT <role> TO <role>`
  writes `pg_auth_members`, not `pg_authid`, so it missed
  the callback that resets the plan cache, and a plan built
  before the grant could run once more without the
  blocked-function check.
- SET TRANSACTION READ WRITE was silently accepted by
  restricted sessions (policy gap, not exploitable due to
  belt-and-suspenders protection)
- COPY TO PROGRAM was not explicitly blocked (mitigated by
  PostgreSQL privilege requirements, but added for
  defense-in-depth)
- Restricted sessions rejected SET of `transaction_read_only`
  or `default_transaction_read_only` to on, which asks for
  the state SafeSession already enforces. A client that
  asserts read-only on each connection it opens, such as a
  connection pool running with writes disabled, was locked
  out entirely. Only relaxing either setting is blocked now.
- A restricted session could run any blocked function by
  passing it as a parameter to `EXECUTE`, because the
  parameters of a prepared statement are neither part of the
  prepared query nor evaluated through the executor, so
  neither of the checks that would catch them ever saw them.
  The same evaluation happens for `EXPLAIN EXECUTE`, with or
  without `ANALYZE`, and for `CREATE TABLE AS ... EXECUTE`,
  and all three are now checked.
- Role membership was tested with `is_member_of_role()`,
  which reports a superuser as a member of every role in the
  database with no grant behind it. Any role that briefly
  acts as a superuser whilst its session user does not, such
  as one inside a SECURITY DEFINER function owned by a
  superuser or one elevated for a single command by an
  extension like supautils, was therefore treated as a
  member of every restricted role and blocked, even when it
  was listed nowhere and granted nothing. Membership now
  uses `is_member_of_role_nosuper()` and follows actual
  grants only.
- Side-effecting function calls are detected when a statement
  is parsed, so a plan cached before a session became
  restricted was replayed without the check running again. A
  session that became restricted part-way through its life,
  because the roles list was reloaded or because a role was
  granted membership of a listed role, could therefore go on
  calling blocked functions through any prepared statement or
  PL/pgSQL expression it had already executed. Becoming
  restricted now discards the session's cached plans, so they
  are re-analysed under the new state.
- PostgreSQL 19 no longer compiled, because it reaches
  `GETSTRUCT` through a different header than earlier releases
  and it made the `jstate` argument of
  `post_parse_analyze_hook_type` const. Builds on
  PostgreSQL 14 to 18 are unchanged.
- A restricted session could run a blocked function by selecting
  from a view whose definition called it, or through a row-level
  security policy's `USING`/`WITH CHECK` clause. View bodies and
  RLS quals are both substituted during query rewrite, which runs
  after the parse-analysis stage the function-blocking check used,
  so neither was visible to it. A restricted session could also run
  a blocked function via a domain's `CHECK` constraint, which is
  fetched and evaluated by the executor separately from the query
  tree and so was not examined either. Domain `CHECK` constraints
  reached via a coercion that appears in a query's parse tree,
  including as an `EXECUTE` statement's declared parameter type,
  are now checked too.
- Examining view bodies for blocked functions is a real behaviour
  change, not just a bug fix: a restricted role reading a view
  whose definition calls a side-effecting function in an untrusted
  language, for example a monitoring view built over
  `pg_stat_statements` that happens to wrap such a call, is now
  rejected where it previously was not. This tightening is
  intentional, but worth knowing about if existing read-only
  monitoring queries are built as views.
- A domain `CHECK` constraint could still run a blocked function
  when the coercion that triggers it appeared in no query tree.
  A parameter bound over the extended query protocol is coerced
  in `exec_bind_message()` before the plan is fetched, which is
  the normal path for JDBC, psycopg, node-postgres and npgsql;
  neither a PL/pgSQL variable's declared type nor a function's
  `RETURNS` type produces a `CoerceToDomain` node anywhere at
  all. An object access hook now rejects a blocked function as
  the executor compiles it, which happens before the constraint
  is evaluated, so all of these are caught. The parameter need
  not even be referenced by the query: declaring it is enough,
  since the constraint runs as a side effect of coercion.
- The fast-path function protocol (libpq's `PQfn`, which the
  large-object client API is built on) reached none of the
  hooks, so a restricted session could call any function
  through it. The same object access hook now covers it.

---

[Upstream source](https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/changelog.md) · `b406cd1e82cf` · Copyright (c) 2025–2026, pgEdge, Inc. [PostgreSQL License](/pgedge/about/license/).
