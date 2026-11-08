---
type: docs
upstream_link: ""
title: OpenHalo 18 and MySQL 5.7 compatibility review
linkTitle: MySQL 5.7 review
description: Independent builds, real MySQL 5.7.32 differential tests, migration results, and seven blocking issues at OpenHalo commit 9dc937f.
weight: 65
---

**OpenHalo 18 can run a limited set of MySQL applications after explicit adaptation. These results do not support using it as a drop-in MySQL 5.7 replacement or approving an unmodified production migration.** Basic queries and client connections work in the tested paths, but crashes, unenforced constraints, ineffective transaction settings, and DDL round-trip changes remain blocking problems.

This is PGSTY's independent review of [`pgsty/openhalo@9dc937f`](https://github.com/pgsty/openhalo/tree/9dc937ff4e81667882c42c3618eafcf4b28ac059), tested on November 7, 2026 (Asia/Shanghai). The issue triage and research notes were consolidated on November 8. It is separate from the [Halo Database 1.0.16 reference](/openhalo/mysql-compatibility/) and the [historical OpenHalo test report](/openhalo/mysql-compatibility-gaps/). A newly discovered problem is not necessarily a regression introduced by this commit.

## Fixed versions and independent builds {#environment}

The tested commit is `9dc937ff4e81667882c42c3618eafcf4b28ac059`, with tree `e45c40bb6c0202f6fe0de59c92ae81e15c938983`. Source was exported with `git archive`; all 7,396 exported files matched the fixed commit. The archive SHA-256 is `08a38f4c4cbc73987178a7ac1acc3fb3c4c8f40acad238b72cdd3d1361357ca2`. Builds, installations, and database initialization were independent of previous test binaries and databases.

| Target | Verified identity and configuration | Role |
| --- | --- | --- |
| OpenHalo main instance | PostgreSQL 18.6 / aux_mysql 1.5, aarch64; GNU make, `--with-openssl --enable-debug --enable-cassert` | Functional and differential testing |
| OpenHalo crash instances | Separate debug/cassert and release/no-cassert installations/data directories; release retains debug symbols | Isolated crash reproduction |
| Primary baseline | Oracle MySQL Community Server **5.7.32**, InnoDB, linux/amd64 | Actual comparison server |
| Supplemental baseline | Oracle MySQL Community Server **5.7.44**, InnoDB, linux/amd64 | Four targeted checks only |

The immutable MySQL image references are:

```text
mysql@sha256:e08834258fcc0efd01df358222333919df53d4a0d9b2a54da05b204b822e3b7b
mysql@sha256:4bc6bc963e6d8443453676cae56536f4b8156d78bae03c0145cbe47c2aad73bb
```

The first is 5.7.32; the second is 5.7.44. `mysqld --version`, SQL version/comment, platform, startup arguments, and binary hashes were recorded. MySQL ran under amd64 emulation while OpenHalo ran on aarch64, so this review makes **no throughput or latency comparison**. The 5.7.44 checks covered unsigned range, TIMESTAMP time zones, trailing-space uniqueness, and repeatable-read visibility; all agreed with 5.7.32. They are not a full 5.7.44 acceptance run.

Both sides used the same clients: Oracle MySQL 5.7.32 CLI, PyMySQL 1.1.1, go-sql-driver/mysql v1.9.3, and Connector/J 8.4.0. The Go tests and JDBC driver were rebuilt from source; the Go source matched the fixed upstream module, and JDBC instrumentation was applied. MariaDB 10.5.29 was also used as an import client, never as the reference server.

The first build wrapper returned 1 after successful build/install because it checked the wrong shared-library directory. The original error was retained, the actual `lib/postgresql` installation was verified, and fresh initialization succeeded. This was a test-wrapper failure, not a product compilation failure.

## Method and configuration tracks {#method}

The common harness recorded SQL acceptance, typed values, binary lengths/hex, decimal precision, temporal fractions, row order where defined, metadata, affected rows, generated IDs, warnings, error numbers/SQLSTATE, server status, and subsequent connection/data state. Unordered results were compared as multisets; ties without a defined order were not reported as sorting defects.

Two tracks were retained: new-instance defaults and explicit common requests (`SET NAMES utf8mb4`, autocommit on, session REPEATABLE READ). The latter is an **alignment request**, not proof that the engines implement the same behavior. In particular, OpenHalo accepted the isolation setting without changing the observed snapshot behavior. Strict SQL modes were not relaxed to conceal failures.

| Setting | OpenHalo | MySQL 5.7.32 | Interpretation |
| --- | --- | --- | --- |
| `sql_mode` | Strict defaults, without `ONLY_FULL_GROUP_BY` | Strict defaults, including `ONLY_FULL_GROUP_BY` | Underlying PostgreSQL still rejects the tested ungrouped-column query |
| Isolation | Reports RR; native setting is read committed | RR | Behavioral failure persists after explicit requests |
| Server character set | utf8mb4 | latin1 | Driver requests and database defaults must be recorded separately |
| System time zone | CST / Asia/Shanghai | UTC | TIMESTAMP tests explicitly requested +00:00, then +08:00 |
| `lower_case_table_names` | 1 | 0 | Table-name behavior differs in these configurations |
| `explicit_defaults_for_timestamp` | 1 | 0 | Implicit first-TIMESTAMP defaults differ |
| `max_allowed_packet` | 64 MiB | 4 MiB | Different default limits, not proof of an ineffective OpenHalo limit |
| Handshake authentication | caching_sha2_password | mysql_native_password | OpenHalo's reported default-auth variable does not describe its actual handshake |

TLS was tested after configuring a test certificate on OpenHalo: PyMySQL negotiated TLS 1.3 with OpenHalo and TLS 1.2 with MySQL. Certificate-chain and hostname verification were not covered. Successful TLS connections are distinct from the failing `SHOW STATUS LIKE 'Ssl_cipher'` metadata path.

## Usable scope and boundaries {#usable-scope}

“Equivalent in the tested scope” applies only to the listed assertions. “Conditional” means a usable path exists with specific restrictions. Accepted-but-different behavior, silent success, explicit rejection, crashes, and untested/environment-blocked cases remain separate categories. Expected rejection can pass a test assertion without making the feature supported.

| Area | What worked in the tested scope | Conditions and remaining boundaries |
| --- | --- | --- |
| Clients and protocol | CLI, Python, Go, JDBC common connection/query paths; prepared execution, streaming, ping | External suites still fail; authentication capabilities and field metadata differ |
| Binary transfer and reset | All bytes 0x00–0xff, empty bytes, 393,216-byte long-data round trips; reset removes uncommitted work, variables, temporary objects, and prepared handles | Fixed-length BINARY padding, full compression coverage, and all packet limits are not established |
| Ordinary data types | Signed integer boundaries, common varchar/text, explicitly declared DECIMAL, VARBINARY/BLOB, ordinary intraday TIME and DATETIME(0/3/6) | Full BIGINT UNSIGNED range, TIMESTAMP zone conversion, negative/long TIME, ENUM/SET differ or fail |
| DDL and queries | Basic table/index operations, rename/truncate, SELECT joins, subqueries, UNION, LIMIT, basic CRUD | JOIN UPDATE crashes; prefix keys and foreign keys do not preserve constraints; not all ALTER or join forms were tested |
| AUTO_INCREMENT | Explicit low values do not lower a configured start; tested LIKE copies advance correctly after explicit imports | Explicit NULL combinations, increment/offset, generated-key and affected-row details remain incompatible |
| Transactions and locks | Commit/rollback, savepoints, tested statement-error recovery, single-row FOR UPDATE and shared locks | RR, read-only settings, delete/reinsert contention, and broader InnoDB locking semantics remain incompatible or untested |
| Ordinary accounts | Create/alter tables, generated values, reads, and diagnostics after business-schema USAGE/CREATE grants | The initial missing-grant fixture failure is not a product defect; full privilege behavior is untested |
| Restart recovery | Four durability/rollback/writability/collation assertions after normal restart and four after immediate/forced recovery, on both sides | No claim about every crash window, storage failure, replication, or failover |

## Seven blocking issues {#blocking-issues}

These are P1 blockers for instance availability, data integrity, or applications that rely on the affected behavior. The two uniqueness failures have separate issues because they require different implementations and acceptance tests.

| Issue | Real MySQL 5.7.32 result | OpenHalo result and impact | Evidence case |
| --- | --- | --- | --- |
| [B01 · UPDATE JOIN](https://github.com/pgsty/openHalo/issues/1) | Updates one matching row | Debug assertion failure and release SIGSEGV; postmaster terminates other backends and recovers | `QUERY-UPDATE-JOIN`, isolated debug/release logs |
| [B02 · Foreign keys](https://github.com/pgsty/openHalo/issues/2) | Invalid child fails with 1452; RESTRICT and CASCADE enforce relationships | Invalid child and restricted parent deletion succeed; cascades do not execute; catalog says `NOT ENFORCED` | `DDL-FK`, migration business chain |
| [B03 · REPEATABLE READ](https://github.com/pgsty/openHalo/issues/3) | Session A reads 10 twice while B commits 11 | A reads 10 then 11 in one transaction, despite reporting RR | `TXN-VISIBILITY-*` |
| [B04 · Read-only settings](https://github.com/pgsty/openHalo/issues/4) | Global read-only rejects ordinary-user writes with 1290; read-only transaction rejects with 1792 | Both settings report success but allow the tested writes | `SETTING-READONLY-GLOBAL`, `TXN-READONLY` |
| [B05 · DECIMAL export](https://github.com/pgsty/openHalo/issues/5) | SHOW CREATE/replay preserves precision and scale | `DECIMAL(8,2)` becomes `decimal`; replay loses rounding and range constraints | `DDL-DECIMAL-REPLAY` |
| [B06 · Collation uniqueness](https://github.com/pgsty/openHalo/issues/6) | utf8mb4_bin rejects both `a` and `a ` in the same unique key | Accepts both; other collation weights also differ | `COLL-BIN-SPACE`, `COLL-*` |
| [B07 · Prefix uniqueness](https://github.com/pgsty/openHalo/issues/7) | `UNIQUE(v(3))` rejects `abcdef` plus `abcxyz`; Sub_part is 3 | Accepts both; Sub_part is NULL | `DDL-PREFIX` |

Each linked issue includes the fixed environment, minimal reproduction, observed results, evidence identifiers, and acceptance criteria. The following examples illustrate why a successful connection or successful DDL is insufficient.

The JOIN UPDATE crash requires only ordinary tables and one matching row. Run it only on a dedicated instance:

```sql
CREATE TABLE t(id INT PRIMARY KEY, v INT);
CREATE TABLE u(id INT PRIMARY KEY, v INT);
INSERT INTO t VALUES(1,1),(2,2);
INSERT INTO u VALUES(1,9);
UPDATE t JOIN u ON t.id=u.id SET t.v=u.v;
```

For DECIMAL, compare the original table with a table recreated from its SHOW CREATE output:

```sql
CREATE TABLE t(n DECIMAL(8,2));
SHOW CREATE TABLE t;
```

On OpenHalo the original table rounds `1.2345` to `1.23` and rejects `1234567.89` with 1264. Replaying its exported definition under another table name preserves `1.2345` and accepts `1234567.89`. The native types are `numeric(8,2)` and unbounded `numeric`, respectively. This is a changed data rule, not merely different DDL formatting.

## Other confirmed differences {#other-differences}

The archive records twenty defect entries in total. The seven blockers above are the first focused issue set; the remaining entries stay in the research backlog rather than being treated as resolved or fully unsupported feature families.

| Archive ID / feature | Observed difference | Application consequence |
| --- | --- | --- |
| B08 · TIMESTAMP | After +00:00 → +08:00, OpenHalo retains 03:04:05.123456; MySQL returns 11:04:05.123456 | Cross-zone time interpretation differs |
| B09 · Explicit AUTO_INCREMENT NULL/0 | `(0,1),(NULL,2)` fails with 1048 on OpenHalo; MySQL generates IDs; NO_AUTO_VALUE_ON_ZERO also differs | Import and insert conventions need adaptation |
| B10 · Increment/offset | Both report increment 3 / offset 2; OpenHalo generates 1,2,3; MySQL 2,5,8 | Do not rely on these settings for ID allocation |
| B11 · REPLACE | OpenHalo retains old ID and reports one affected row; MySQL replaces it with a new ID and reports two | Identity and affected-row semantics differ; trigger side effects were not tested |
| B12 · UPDATE / ODKU results | With CLIENT_FOUND_ROWS off, OpenHalo returns matched rows; MySQL reports changed rows; ODKU IDs/counts also differ | Optimistic updates and driver result checks may be wrong |
| B13 · BINARY(n) | BINARY(5) stores `a ` as 2 bytes on OpenHalo and 5 NUL-padded bytes on MySQL | Fixed-width binary values differ |
| B14 · ANSI_QUOTES | Setting succeeds but quoted strings/identifiers do not switch as on MySQL | SQL generators can change meaning or fail |
| B15 · wait_timeout | After setting 1 and idling 2 seconds, OpenHalo still accepts a query; MySQL disconnects | Pool timeout assumptions fail |
| B16 · Multi-statement syntax error | An intermediate syntax error prevents the preceding statement from executing on OpenHalo; MySQL retains the preceding committed statement | Partial execution and recovery logic differ |
| B17 · Diagnostics and metadata | Missing Note/1051, failing SHOW STATUS, variable result types, alias case, flags/charset/scale, and SQLSTATE differences | ORM and driver behavior needs per-path verification |
| B18 · CHAR padding mode | PAD_CHAR_TO_FULL_LENGTH outputs five characters on both sides; OpenHalo LENGTH returns 1, MySQL 5 | Output and expression semantics disagree |
| B19 · INSERT IGNORE | Truncation cancels the OpenHalo statement; MySQL truncates with warnings and inserts valid rows | Import progress and warning handling differ |
| B20 · Unsigned 64-bit range | OpenHalo rejects 18446744073709551615 and returns -1 for CAST(-1 AS UNSIGNED) | Full MySQL unsigned values are not representable in the tested path |

Explicitly rejected examples include ENUM/SET, negative or long TIME, MySQL stored programs/triggers/events, DO, LOAD DATA, partition DDL, common JSON/spatial functions, and the tested generated-column combinations. JSON storage accepting valid input does not establish JSON-function support. In the tested CHECK example, both servers accepted the clause but allowed a violating value, consistent with that MySQL 5.7 example; it is not evidence of an enforced constraint.

A controlled delete/reinsert race reproduced 3/3 times: after waiting for A to delete and reinsert a row, B's DELETE affects zero rows on OpenHalo, then INSERT fails with 1062; MySQL deletes one row and inserts successfully. This explains one class of sysbench duplicate-key errors. Expected deadlocks with 1213 are not automatically defects.

## Test accounting {#test-accounting}

Counts below have different units. They must not be added together or turned into a product compatibility percentage.

| Suite / scope | OpenHalo | MySQL 5.7.32 |
| --- | --- | --- |
| Bundled suite | 22/22 groups pass; no skips; 23 AB assertions are inside one group | 15/17 common runnable groups pass; 2 fixture failures |
| Go, all top-level tests | 142 pass / 19 fail / 2 skip | 161 pass / 1 fail / 1 skip |
| Go, server-facing driver_test.go subset | 51 pass / 19 fail / 2 skip | 70 pass / 1 fail / 1 skip |
| PyMySQL, all test cases | 132 pass / 30 fail / 12 skip / 1 xfail | Default database: 161/1/12/1; utf8mb4 database: 162/0/12/1 |
| PyMySQL, excluding 8 client-only unit cases | 124 pass / 30 fail / 12 skip / 1 xfail | Default: 153/1/12/1; utf8mb4: 154/0/12/1 |
| SQL catalog | 146 cases: 145 in two tracks, plus isolated debug and release crash records | Paired inputs and observations |
| Additional cases | 11 protocol, 14 concurrency/privilege, 9 supplemental | Paired by case ID |
| Lifecycle | Four assertions per restart mode pass | Four assertions per restart mode pass |

MySQL's bundled raw-statement failure came from the supplied decoder's assumptions; java-auth queried PostgreSQL-only `pg_stat_ssl`. Neither is a MySQL server defect. Independent raw-protocol checks and common Java statement/transaction tests ran on both sides. MySQL's only Go failure was the compressed TestLongData subcase hitting its default 4 MiB packet limit. Its PyMySQL failure disappeared with an explicitly utf8mb4 test database; upstream assertions were not changed.

The archive contains 701 combined result records, including repeated runs, driver units, and paired summaries. The raw SQL labels—206 accepted-different, 74 rejected/conditional, 6 non-5.7, and 4 observational records—include metadata and diagnostics. They do not identify 206 independent defects or define a compatibility denominator. CTEs, window functions, and expression defaults are extra capabilities/negative controls outside the 5.7 denominator.

All four sysbench workloads completed on both sides. OpenHalo point-select/read-only completed 109,227/11,206 events with no ignored errors. Read/write completed 2,742 events with 50 ignored errors; write-only completed 1,289 with 53. MySQL's corresponding event counts were 377,680 / 21,855 / 12,279 / 28,015, with 0 / 0 / 43 / 115 ignored errors. Write workloads did not record per-event retries, so “events minus ignored errors” cannot establish error-free event counts. Verbose error samples are incomplete distributions; these numbers are correctness/accounting evidence, not a performance comparison.

## Migration trial {#migration}

Oracle mysqldump 5.7.32 exported three related tables: customers (24 rows), orders (72), and items (216). The schema included keys, unique/composite indexes, AUTO_INCREMENT, ON UPDATE, Chinese/emoji, binary bytes, DECIMAL, and fractional timestamps. Data generation used seed 573218; unsigned sample IDs remained within the signed BIGINT range.

The original dump ordered tables customers → items → orders. OpenHalo stopped with 1146 when items referenced orders before its creation, despite `FOREIGN_KEY_CHECKS=0`. A separate `--force` import returned zero but still omitted items; a zero exit code did not establish success.

The only adaptation moved complete table/data blocks into customers → orders → items order. It did not alter columns, values, foreign keys, SQL mode, or session preamble/footer. Row counts, primary-key sets, and typed values then matched at a +00:00 query time zone. The subsequent business chain failed integrity checks:

| Operation | OpenHalo | MySQL 5.7.32 |
| --- | --- | --- |
| New customer/order/item IDs | 25 / 73 / 217 | 25 / 73 / 217 |
| Duplicate email | Rejects with 1062 | Rejects with 1062 |
| Delete customer referenced by an order | Succeeds | Rejects with 1451 |
| Insert item referencing absent order 999999 | Succeeds | Rejects with 1452 |
| Roll back amount update | Restores 7.123456 | Restores 7.123456 |
| Items remaining after deleting order 73 | 1 | 0 after CASCADE |
| Final customers / orders / items | 24 / 72 / 218 | 25 / 72 / 216 |

Both migrated foreign keys had `conenforced=false` and `convalidated=false` in the PostgreSQL catalog. **Adapted data transfer succeeded; application semantics did not pass.** Reordering the dump does not fix foreign keys, uniqueness, time zones, unsigned range, or DECIMAL re-export. No complete ORM/application startup or production-scale migration was tested.

## Focused research and minimum repair scope {#research}

Seven separate investigations accompany the issue set. Their purpose is to identify the smallest change that restores the required invariant, together with meaningful regression tests. The review itself changes no product code. A source-level diagnosis or proposed patch is not a verified repair.

| Issue | Source diagnosis | Smallest safe change and acceptance boundary |
| --- | --- | --- |
| [B01 · UPDATE JOIN](https://github.com/pgsty/openHalo/issues/1) | `mys_rewrite.c:1180-1191` trusts nested `RangeFunction` lists; the JOIN grammar also puts an `A_Const` table-name node into `UpdateStmt.targetList`, which the rewriter reads as `ResTarget`. | Add node/list shape guards and return 1235 before traversal. Then support only one target, one right table, `INNER JOIN`, normalized `ResTarget` assignments, and provably unique matches. Debug and release must survive with matching row results. |
| [B02 · Foreign keys](https://github.com/pgsty/openHalo/issues/2) | The table-level FK constructor at `mys_gram.y:7103-7123` leaves PG18 `Constraint.is_enforced` false; PostgreSQL therefore does not install the enforcing and referential-action triggers. | Set `is_enforced=true` in the shared table-level constructor, retain normal validation, and test invalid writes plus RESTRICT/CASCADE/SET NULL. Reject old `ALTER CONSTRAINT`, unadapted FK CTAS, and `foreign_key_checks=0` until their semantics are implemented; audit existing `NOT ENFORCED` data. |
| [B03 · REPEATABLE READ](https://github.com/pgsty/openHalo/issues/3) | `applySystemVarValue()` never applies `transaction_isolation` or `tx_isolation` to PostgreSQL MVCC; parser paths also collapse SESSION and NEXT scopes. | Share state for both aliases across GLOBAL/SESSION/NEXT, apply the selected level before the first snapshot, and verify RR `10→10`, RC `10→11`, new connections, aliases, reset, and prepared execution. If this state machine is not implemented, reject RR instead of echoing it. |
| [B04 · Read-only settings](https://github.com/pgsty/openHalo/issues/4) | `read_only` is stored in the compatibility hash without a cross-backend write gate; `SET TRANSACTION READ ONLY` becomes a session-variable assignment, while `START TRANSACTION READ ONLY` reaches native PostgreSQL protection. | Reject unsupported global/session/NEXT setters before storing their values; retain `START TRANSACTION READ ONLY`, map real read-only transaction errors to 1792/25006, and expose the read-only status bit. A complete global implementation needs a real cross-backend gate and separate privilege/temporary-table rules. |
| [B05 · DECIMAL export](https://github.com/pgsty/openHalo/issues/5) | The SHOW conversion loses PostgreSQL numeric typmod, so `numeric(8,2)` is emitted as unbounded `decimal` and replay changes rounding and overflow behavior. | Centralize typmod formatting for COLUMN_TYPE, SHOW COLUMNS/FULL COLUMNS, SHOW CREATE, and numeric precision/scale metadata; synchronize the SQL generator and upgrade path. Do not guess typmods for historical unbounded columns. |
| [B06 · Collation uniqueness](https://github.com/pgsty/openHalo/issues/6) | MySQL names are compressed to a case-sensitive or ICU approximation; the C-based rule lacks MySQL 5.7 PAD SPACE and weight semantics, and the original rule name is not retained. | Stop silently mapping unsupported names, or explicitly label the approximation. A real rule must keep equality, sorting, hashing, B-tree behavior, and metadata consistent; check conflicts and rebuild existing indexes before changing weights. |
| [B07 · Prefix uniqueness](https://github.com/pgsty/openHalo/issues/7) | The shared grammar action at `mys_gram.y:11063` ignores the prefix length `$3`, so the accepted index becomes a full-column index. | Return 1235 for prefix-index syntax across CREATE/ALTER/CREATE INDEX until metadata, character/byte semantics, SHOW output, and conflict handling are complete. Do not replace it with an expression index as a partial fix; audit previously miscreated indexes from trusted DDL. |

All seven investigations are complete. These are proposed guards or repair designs, not implemented product changes; each acceptance boundary requires a fresh OpenHalo/MySQL 5.7 differential run after a future patch.

Acceptance must exercise actual rows, constraints, snapshots, connection survival, and DDL replay. Changing a reported variable, an error label, or SHOW output alone is insufficient. Where complete semantics require substantial work, the first safe change can be an explicit unsupported error; that must be described as a guard, not newly implemented MySQL support.

## Evidence and untested scope {#evidence}

The retained evidence set is named `mysql57-round2`. It contains REPORT, MYSQL57_SUPPORT, DIFFERENCES, BUGS, TEST_MATRIX, MIGRATION_TRIAL, typed `results.jsonl`, scripts, cases, environment snapshots, raw logs, and a SHA256SUMS manifest covering 635 lightweight files. The website contains this maintained synthesis; the full local archive is not published as a downloadable attachment. The linked GitHub issues carry self-contained minimal reproductions and archive case identifiers.

| Evidence path inside the archive | Purpose |
| --- | --- |
| `artifacts/source-provenance.json`, `environment.json`, `artifacts/source-end.json` | Fixed source, binaries/environment, unchanged source state |
| `logs/sql-final.jsonl`, `logs/protocol.jsonl` | Statement and protocol observations |
| `logs/concurrency.jsonl`, `logs/supplement.jsonl` | Controlled two-session order, ordinary accounts, effective settings |
| `logs/join-debug.jsonl`, `logs/join-release.jsonl`, `logs/crash-symbols.log` | Isolated crashes and symbolized stack |
| `logs/precision-fk.jsonl`, `artifacts/native-constraint-types.json` | DDL round-trip and native catalog evidence |
| `logs/migration-chain.json`, `artifacts/final-summary.json` | Business invariants and counting units |

The evidence directory's `scripts/replay.sh` starts retained test instances and writes new replay logs without overwriting the original results. Large source trees, binaries, downloads, databases, and full dumps remain in the test container or dedicated volumes. The three OpenHalo test instances and both MySQL containers were stopped at the end of the test round; the shared development container was retained.

Untested areas include all client versions and authentication modes; certificate verification; the full character-set/collation/function catalog; every ALTER and multi-table DML form; SERIALIZABLE, READ UNCOMMITTED, XA and complete gap/next-key locking; storage-failure windows; MySQL replication/binlog/GTID/PITR; failover; complete privileges/security; full PostgreSQL world tests and six-platform packaging at this commit; and real application/ORM acceptance. No OpenHalo 14 security audit was performed.

**A MySQL client connection, a 5.7.32 handshake string, or an accepted SQL statement does not establish MySQL 5.7 semantic compatibility.** Deployable scope must be established with the application's own schema, drivers, transactions, migration path, and operational assumptions.
