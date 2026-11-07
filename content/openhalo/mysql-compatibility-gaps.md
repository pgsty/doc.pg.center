---
type: docs
upstream_source: openhalo-tests
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "OpenHalo 1.0.14.18 test report; commit 80a8d07"
upstream_notice: /attribution/#openhalo-tests
title: Known MySQL compatibility boundaries
linkTitle: Compatibility boundaries
description: Versioned OpenHalo test results for MySQL features that require rewriting or additional validation.
weight: 60
---

The independent [OpenHalo MySQL Compatibility Testing Report](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md) tested OpenHalo `1.0.14.18 (251127)` with a MySQL 5.7.32 client from November 27 to December 3, 2025. It recorded 42 passed and 15 failed cases out of 57. The 73.7% figure is the pass ratio for that test set, not a compatibility percentage for the product.

These results are historical migration evidence for one OpenHalo build, not an official Halo Database support matrix. Some failures depend on the exact statement and test schema. Re-run the statements against the version and schema you plan to deploy.

## Features that need attention in the report {#reported-boundaries}

| MySQL feature or test | Result in the tested OpenHalo build | Migration direction |
| --- | --- | --- |
| `JSON_EXTRACT`, `JSON_SET`, and related JSON helpers | The test failed during function lookup. | Compare PostgreSQL `json`/`jsonb` operators and functions, including result types and null behavior. |
| One `FORCE INDEX` form | The report's exact index-hint test failed at the index name. | Re-test the precise hint used by the application; inspect the PostgreSQL plan before rewriting it. |
| MySQL partition DDL | `PARTITION BY RANGE (...)` with MySQL partition clauses failed. | Convert to PostgreSQL partition syntax and review partition pruning and unique-key rules. |
| Stored procedures with `BEGIN ... END` | MySQL procedure creation failed at the procedure body. | Replace with PostgreSQL functions, application logic, or a procedural form supported by the target build. |
| `MATCH(...) AGAINST(...)` | The MySQL search expression failed at `AGAINST`. The report's accepted index DDL is not proof that MySQL full-text search is implemented; its index setup has schema limitations. | Use PostgreSQL full-text search or validate the complete search workload separately. |
| Spatial functions such as `POINT()` and `ST_Distance()` | The functions were not found in the tested run. | Use a tested PostgreSQL spatial implementation and rewrite the calls. |
| `HANDLER` statements | The low-level MySQL table-access syntax failed at `HANDLER`. | Replace it with ordinary queries and indexes. |
| `SHOW TABLE STATUS` after `USE` | The test reported an invalid PostgreSQL `search_path` and no selected schema. | Review the database, tenant, and schema preparation; this result does not prove that every `SHOW` command is unsupported. |
| MySQL `GET DIAGNOSTICS` | The statement failed at `GET`. | Use the client driver's affected-row result or PostgreSQL diagnostics in a server-side function. |
| `SELECT ... INTO OUTFILE` | The server-side export clause failed at `INTO`. | Use client-side output redirection or PostgreSQL `COPY` through the PostgreSQL connection. |
| The report's `UNION` statement | The exact unparenthesized form placed `LIMIT` before `UNION` and failed at `UNION`. | Re-test with parenthesized branches; do not infer that every `UNION` form is unsupported. |

The report also notes that a syntax error can leave the current PostgreSQL transaction aborted. After an error, issue `ROLLBACK` or start a new session before interpreting subsequent results.

The current Halo 1.0.16 reference separately documents `mysql.multi_table_delete_methond`, including two compatibility modes. Re-test multi-table `DELETE` on the exact build instead of carrying the old OpenHalo result forward unchanged.

## Features that passed in the report {#passed-features}

The report recorded successful cases for:

- basic `SELECT`, `WHERE`, `LIKE`, `IS NULL`, `ORDER BY`, and `LIMIT`;
- `GROUP BY`, `COUNT`, `AVG`, `MIN`, `MAX`, and `FLOOR`;
- ordinary `INSERT`, `UPDATE`, and `DELETE`;
- ordinary indexes and `SHOW INDEX`;
- inner joins, left joins, multi-table joins, and self joins;
- views, `START TRANSACTION`, `COMMIT`, and `ROLLBACK`;
- `CONCAT`, `SUBSTRING`, `UPPER`, `LOWER`, `LENGTH`, `REPLACE`, and `TRIM`;
- unique, foreign-key, and check constraints;
- derived tables, correlated subqueries, and `EXISTS`.

The official Halo manual separately documents MySQL-oriented syntax and types in [Compatible MySQL statements](/openhalo/mysql-statements/) and [Compatible MySQL data types](/openhalo/mysql-data-types/).

## Migration test plan {#test-plan}

Before switching an application:

1. Connect through the same MySQL driver, authentication method, and listener port used in production.
2. Load a representative schema, including indexes, constraints, generated values, `ENUM`/`SET`, and dump-specific statements.
3. Run DDL and DML in an isolated database and compare row counts, result types, affected-row counts, warnings, and error codes.
4. Exercise transactions, prepared statements, connection pooling, retries, and session variables.
5. Test administrative jobs separately from application queries, especially exports, stored programs, partition maintenance, and optimizer hints.

Do not mark a MySQL workload migrated solely because the client can connect or basic CRUD statements pass.

## Sources {#sources}

This page is an original summary of the [OpenHalo MySQL compatibility test report](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md). No public documentation licence was identified; see the [source notice](/attribution/#openhalo-tests) for version, copyright, and citation details.
