---
title: Security
linkTitle: Security
description: AgensGraph's security model is PostgreSQL's.
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/security.html
upstream_source: agensgraph
upstream_modified: true
---


AgensGraph's security model is PostgreSQL's. Roles, `pg_hba.conf`, TLS, `GRANT` and row-level
security all work exactly as they do there, and
[PostgreSQL's client-authentication](https://www.postgresql.org/docs/18/client-authentication.html)
and [database-roles](https://www.postgresql.org/docs/18/user-manag.html) chapters are the
reference.

What this page adds is how those mechanisms land on a graph. A graph is a schema and a label
is a table, so the grants a Cypher query needs are not always the ones you would guess.

## Authentication {#authentication}

`pg_hba.conf` in the data directory decides who may connect, from where, to which database,
and how. Rules are matched top to bottom and the first match wins.

```
# TYPE  DATABASE  USER      ADDRESS          METHOD
local   all       all                        peer
host    mydb      appuser   10.0.0.0/24      scram-sha-256
hostssl mydb      analyst   0.0.0.0/0        scram-sha-256
host    all       all       0.0.0.0/0        reject
```

Reload after editing:

```shell
ag_ctl -D $AGDATA reload
```

Three things to get right before a server is reachable:

**Replace the default `trust` rules.** `initdb` writes `trust` for local connections, which
means anyone with a shell account can connect as any role, superuser included. Use `peer`
for local Unix-socket connections and `scram-sha-256` for anything over the network.

**Use `scram-sha-256`, not `md5`.** Set `password_encryption = scram-sha-256` before you
create or change passwords, so the stored verifier is the strong one.

**Require TLS for network connections.** `hostssl` in the rule, plus `ssl = on` and a
certificate and key in `postgresql.conf`. `sslmode=verify-full` on the client is what actually
prevents an interception; `require` only encrypts.

The methods available are PostgreSQL's full set — `peer`, `scram-sha-256`, `cert`, `ldap`,
`gss`, `sspi`, `pam`, `radius`, `ident`, `trust`, `reject` — with the same options. See
[PostgreSQL's authentication-methods
chapter](https://www.postgresql.org/docs/18/auth-methods.html).

When a connection is refused, the server log says why, and the message is more specific than
what the client is told. Check it before changing rules.

## Roles {#roles}

Roles are cluster-wide — they belong to the server, not to a database — and a role with
`LOGIN` is what other systems call a user.

```sql
CREATE ROLE appuser LOGIN PASSWORD 'secret';
CREATE ROLE readonly;                       -- a group, no LOGIN
GRANT readonly TO appuser;
```

The attributes that matter operationally are `SUPERUSER`, `CREATEDB`, `CREATEROLE`,
`REPLICATION` and `BYPASSRLS`; grant none of them to an application role. `ALTER ROLE … SET`
pins a setting for a role, which is a clean way to force `graph_path`, or to keep
`enable_graph_dml` off for everyone but a maintenance role:

```sql
ALTER ROLE appuser SET graph_path = moviekb;
ALTER ROLE appuser SET enable_graph_dml = off;
```

## Permissions on a graph {#permissions-on-a-graph}

A graph is a schema and each label is a table, so the grants are ordinary ones. The surprises
come from elsewhere: a Cypher query touches more objects than the labels it names.

### Reading {#reading}

A read needs `USAGE` on the graph's schema and `SELECT` on each label it touches. Follow this
sequence to see where each grant becomes necessary. Start with the schema only:

```sql
CREATE ROLE analyst;
GRANT USAGE ON SCHEMA moviekb TO analyst;
```

```psql
SET ROLE analyst;
```

A Cypher read now fails as a table permission error, naming the label:

```cypher
MATCH (m:movie) RETURN count(m);
```

```
ERROR:  permission denied for table movie
```

Grant the label and it works:

```psql
RESET ROLE;
GRANT SELECT ON moviekb.movie TO analyst;
SET ROLE analyst;
```

```cypher
MATCH (m:movie) RETURN count(m);
```

```
 count
-------
 18
```

**An unlabelled pattern needs `ag_vertex` as well.** `MATCH (n)` scans the graph's
`ag_vertex` parent and every label under it, so a role that can read `movie` but not
`ag_vertex` still cannot run it:

```cypher
MATCH (n) RETURN count(n);
```

```
ERROR:  permission denied for table ag_vertex
```

The same applies to `ag_edge` for an unlabelled edge. So for a read-only analyst role, grant
across the schema rather than label by label:

```psql
RESET ROLE;
```

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA moviekb TO analyst;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb GRANT SELECT ON TABLES TO analyst;
```

The `ALTER DEFAULT PRIVILEGES` line is what makes a label created next month readable too.

### Writing {#writing}

Creating a vertex or an edge needs `INSERT` on the label **and `USAGE` on the label's id
sequence**. That second one is easy to miss. Grant only the `INSERT`:

```psql
RESET ROLE;
```

```sql
GRANT INSERT ON moviekb.movie TO analyst;
```

```psql
SET ROLE analyst;
```

```cypher
CREATE (:movie {title: 'X'});
```

```
ERROR:  permission denied for sequence movie_id_seq
```

Add the sequence and the write goes through:

```psql
RESET ROLE;
```

```sql
GRANT USAGE ON SEQUENCE moviekb.movie_id_seq TO analyst;
```

`SET` and `REMOVE` need `UPDATE` on the label. `DELETE` needs `DELETE` on it. And
`DETACH DELETE` needs a grant on `ag_edge`, because that is how it finds the edges to remove:

```
ERROR:  permission denied for table ag_edge
```

An error naming `ag_edge` or `ag_vertex` is a missing grant on the graph's parent label, not
a row-security result — worth knowing, because it is easy to read it as one.

A working set of grants for a role that reads and writes a whole graph:

```sql
GRANT USAGE ON SCHEMA moviekb TO appuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA moviekb TO appuser;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA moviekb TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO appuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA moviekb GRANT USAGE ON SEQUENCES TO appuser;
```

### Creating labels {#creating-labels}

Creating a label needs `CREATE` on the graph's schema. Creating a graph needs `CREATE` on the
database.

## Row-level security {#row-level-security}

Row-level security works on a label, so a policy can restrict which vertices or edges a role
sees and writes:

```sql
ALTER TABLE moviekb.movie ENABLE ROW LEVEL SECURITY;

CREATE POLICY movie_visible ON moviekb.movie
  FOR SELECT TO analyst
  USING ((properties->>'genre') = 'Sci-Fi');
```

> [!WARNING]
> **Re-test any RLS policy you had on 2.17.** Before 2.18, policies were not properly enforced
> on graph writes: the `USING` clause of an `UPDATE` or `DELETE` policy was attached to a
> relation that is never scanned, so it filtered nothing — a role with no `DELETE` policy at
> all could delete rows. `INSERT` policies were checked against the wrong row, and edge
> creation was not checked at all, so an edge label with row security accepted every insert.
>
> 2.18 enforces all of it. That is the correct behaviour, and it means writes your application
> performs today may start being refused. Test before you upgrade, not after. See [Release
> notes](/agensgraph/release-notes/2.18/#stricter-validation).

Two practical notes:

* A policy expression reads the label's columns, so it works on `properties` — and on a
  [promoted column](/agensgraph/querying/typed-columns/), which is faster and lets the policy use an
  index.
* `BYPASSRLS` and table ownership both skip policies. An application role should have
  neither.

## Two settings that are part of the security posture {#two-settings-that-are-part-of-the-security-posture}

`enable_graph_dml` and `enable_graph_ddl` are off by default, and they gate writing to and
reshaping a label with SQL rather than Cypher. Leaving them off keeps an application on the
Cypher path, where the graph's own checks run — for example that an edge's endpoints exist.

They are not the whole of a graph's integrity, and should not be read as it. `COPY` writes a
label without consulting either setting. What does hold on every path, whatever the settings
say, is that a row's id names the label that stores it: a write that would break that is
refused, whether it comes from Cypher, `INSERT`, `UPDATE`, `COPY` or a replication apply.

Turn them on for maintenance work and turn them off again, or pin them off per role with
`ALTER ROLE … SET`.

`cypher_allow_unsafe_ddl` likewise. See [Server settings](/agensgraph/reference/guc/).

## Encryption at rest {#encryption-at-rest}

AgensGraph does not encrypt data files itself. Use filesystem or block-device encryption, or
[Agens TDE](https://tech.skaiworldwide.com/docs/en/agens-tde/16/) where transparent data
encryption is a requirement. `pgcrypto` covers column-level encryption, and a property is an
ordinary `jsonb` value, so it can hold a `pgcrypto` ciphertext like any other column.
