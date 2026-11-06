---
title: "SQL Statements Index"
linkTitle: "SQL Statements"
description: "Find Apache Cloudberry SQL statements organized by database object and operation."
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/index.md"
---

## Access Method {#access-method}

- [CREATE ACCESS METHOD](/cloudberry/reference/sql-stmts/create-access-method/) - Defines a new access method.
- [DROP ACCESS METHOD](/cloudberry/reference/sql-stmts/drop-access-method/) - Removes an access method.

## Cast {#cast}

- [CREATE CAST](/cloudberry/reference/sql-stmts/create-cast/) - Defines a new cast.
- [DROP CAST](/cloudberry/reference/sql-stmts/drop-cast/) - Removes a cast.

## Collation {#collation}

- [CREATE COLLATION](/cloudberry/reference/sql-stmts/create-collation/) - Defines a new collation.
- [ALTER COLLATION](/cloudberry/reference/sql-stmts/alter-collation/) - Changes the definition of a collation.
- [DROP COLLATION](/cloudberry/reference/sql-stmts/drop-collation/) - Removes a previously defined collation.

## Conversion {#conversion}

- [CREATE CONVERSION](/cloudberry/reference/sql-stmts/create-conversion/) - Defines a new encoding conversion.
- [ALTER CONVERSION](/cloudberry/reference/sql-stmts/alter-conversion/) - Changes the definition of a conversion.
- [DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/) - Removes a conversion.

## Cursor {#cursor}

- [DECLARE](/cloudberry/reference/sql-stmts/declare/) - Defines a cursor.
- [CLOSE](/cloudberry/reference/sql-stmts/close/) - Closes a cursor.
- [FETCH](/cloudberry/reference/sql-stmts/fetch/) - Retrieves rows from a query using a cursor.
- [MOVE](/cloudberry/reference/sql-stmts/move/) - Positions a cursor.
- [RETRIEVE](/cloudberry/reference/sql-stmts/retrieve/) - Retrieves rows from a query using a parallel retrieve cursor.

## Database {#database}

- [CREATE DATABASE](/cloudberry/reference/sql-stmts/create-database/) - Creates a new database.
- [ALTER DATABASE](/cloudberry/reference/sql-stmts/alter-database/) - Changes the attributes of a database.
- [DROP DATABASE](/cloudberry/reference/sql-stmts/drop-database/) - Removes a database.
- [ANALYZE](/cloudberry/reference/sql-stmts/analyze/) - Collects statistics about a database.
- [VACUUM](/cloudberry/reference/sql-stmts/vacuum/) - Garbage-collects and optionally analyzes a database.
- [CHECKPOINT](/cloudberry/reference/sql-stmts/checkpoint/) - Forces a write-ahead log checkpoint.
- [COMMENT](/cloudberry/reference/sql-stmts/comment/) - Defines or changes the comment of an object.
- [COPY](/cloudberry/reference/sql-stmts/copy/) - Copies data between a file and a table.
- [LOAD](/cloudberry/reference/sql-stmts/load/) - Loads or reloads a shared library file.

## Domain {#domain}

- [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/) - Defines a new domain.
- [ALTER DOMAIN](/cloudberry/reference/sql-stmts/alter-domain/) - Changes the definition of a domain.
- [DROP DOMAIN](/cloudberry/reference/sql-stmts/drop-domain/) - Removes a domain.

## Extension {#extension}

- [CREATE EXTENSION](/cloudberry/reference/sql-stmts/create-extension/) - Registers an extension in a Apache Cloudberry.
- [ALTER EXTENSION](/cloudberry/reference/sql-stmts/alter-extension/) - Change the definition of an extension.
- [DROP EXTENSION](/cloudberry/reference/sql-stmts/drop-extension/) - Removes an extension from a Apache Cloudberry.

## External Table {#external-table}

- [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) - Defines a new external table.
- [ALTER EXTERNAL TABLE](/cloudberry/reference/sql-stmts/alter-external-table/) - Changes the definition of an external table.
- [DROP EXTERNAL TABLE](/cloudberry/reference/sql-stmts/drop-external-table/) - Removes an external table definition.

## Foreign Data Wrapper {#foreign-data-wrapper}

- [CREATE FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/create-foreign-data-wrapper/) - Defines a new foreign-data wrapper.
- [ALTER FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/alter-foreign-data-wrapper/) - Changes the definition of a foreign-data wrapper.
- [DROP FOREIGN DATA WRAPPER](/cloudberry/reference/sql-stmts/drop-foreign-data-wrapper/) - Removes a foreign-data wrapper.

## Function & Aggregate Function {#function--aggregate-function}

### Function {#function}

- [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/) - Defines a new function.
- [ALTER FUNCTION](/cloudberry/reference/sql-stmts/alter-function/) - Changes the definition of a function.
- [DROP FUNCTION](/cloudberry/reference/sql-stmts/drop-function/) - Removes a function.

### Aggregate Function {#aggregate-function}

- [CREATE AGGREGATE](/cloudberry/reference/sql-stmts/create-aggregate/) - Defines a new aggregate function.
- [ALTER AGGREGATE](/cloudberry/reference/sql-stmts/alter-aggregate/) - Changes the definition of an aggregate function.
- [DROP AGGREGATE](/cloudberry/reference/sql-stmts/drop-aggregate/) - Removes an aggregate function.

## Foreign Table {#foreign-table}

- [CREATE FOREIGN TABLE](/cloudberry/reference/sql-stmts/create-foreign-table/) - Defines a new foreign table.
- [ALTER FOREIGN TABLE](/cloudberry/reference/sql-stmts/alter-foreign-table/) - Changes the definition of a foreign table.
- [DROP FOREIGN TABLE](/cloudberry/reference/sql-stmts/drop-foreign-table/) - Removes a foreign table.

## User & Group {#user--group}

- [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) - Defines a new database role (user or group).
- [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) - Changes a database role (user or group).
- [SET ROLE](/cloudberry/reference/sql-stmts/set-role/) - Sets the current role identifier of the current session.
- [DROP ROLE](/cloudberry/reference/sql-stmts/drop-role/) - Removes a database role.
- [CREATE USER](/cloudberry/reference/sql-stmts/create-user/) - Defines a new database role.
- [ALTER USER](/cloudberry/reference/sql-stmts/alter-user/) - Changes the definition of a database role.
- [DROP USER](/cloudberry/reference/sql-stmts/drop-user/) - Removes a database role.
- [CREATE GROUP](/cloudberry/reference/sql-stmts/create-group/) - Defines a new database role.
- [ALTER GROUP](/cloudberry/reference/sql-stmts/alter-group/) - Changes a role name or membership.
- [DROP GROUP](/cloudberry/reference/sql-stmts/drop-group/) - Removes a database role.
- [DROP OWNED](/cloudberry/reference/sql-stmts/drop-owned/) - Removes database objects owned by a database role.
- [REASSIGN OWNED](/cloudberry/reference/sql-stmts/reassign-owned/) - Changes the ownership of database objects owned by a database role.

## Index {#index}

- [CREATE INDEX](/cloudberry/reference/sql-stmts/create-index/) - Defines a new index.
- [ALTER INDEX](/cloudberry/reference/sql-stmts/alter-index/) - Changes the definition of an index.
- [REINDEX](/cloudberry/reference/sql-stmts/reindex/) - Rebuilds indexes.
- [DROP INDEX](/cloudberry/reference/sql-stmts/drop-index/) - Removes an index.

## Notification {#notification}

- [NOTIFY](/cloudberry/reference/sql-stmts/notify/) - Generates a notification.
- [LISTEN](/cloudberry/reference/sql-stmts/listen/) - Listens for a notification.
- [UNLISTEN](/cloudberry/reference/sql-stmts/unlisten/) - Stops listening for a notification.

## Procedural Language {#procedural-language}

- [CREATE LANGUAGE](/cloudberry/reference/sql-stmts/create-language/) - Defines a new procedural language.
- [ALTER LANGUAGE](/cloudberry/reference/sql-stmts/alter-language/) - Changes the definition of a procedural language.
- [DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/) - Removes a procedural language.
- [DO](/cloudberry/reference/sql-stmts/do/) - Runs anonymous code block as a transient anonymous function.

## View and Materialized View {#view-and-materialized-view}

- [CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/) - Defines a new view.
- [ALTER VIEW](/cloudberry/reference/sql-stmts/alter-view/) - Changes properties of a view.
- [DROP VIEW](/cloudberry/reference/sql-stmts/drop-view/) - Removes a view.
- [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/) - Defines a new materialized view.
- [ALTER MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/alter-materialized-view/) - Changes the definition of a materialized view.
- [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/) - Removes a materialized view.
- [REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/) - Replaces the contents of a materialized view.

## Operator & Operator Class & Operator Family {#operator--operator-class--operator-family}

### Operator {#operator}

- [CREATE OPERATOR](/cloudberry/reference/sql-stmts/create-operator/) - Defines a new operator.
- [ALTER OPERATOR](/cloudberry/reference/sql-stmts/alter-operator/) - Changes the definition of an operator.
- [DROP OPERATOR](/cloudberry/reference/sql-stmts/drop-operator/) - Removes an operator.

### Operator Class {#operator-class}

- [CREATE OPERATOR CLASS](/cloudberry/reference/sql-stmts/create-operator-class/) - Defines a new operator class.
- [ALTER OPERATOR CLASS](/cloudberry/reference/sql-stmts/alter-operator-class/) - Changes the definition of an operator class.
- [DROP OPERATOR CLASS](/cloudberry/reference/sql-stmts/drop-operator-class/) - Removes an operator class.

### Operator Family {#operator-family}

- [CREATE OPERATOR FAMILY](/cloudberry/reference/sql-stmts/create-operator-family/) - Defines a new operator family.
- [ALTER OPERATOR FAMILY](/cloudberry/reference/sql-stmts/alter-operator-family/) - Changes the definition of an operator family.
- [DROP OPERATOR FAMILY](/cloudberry/reference/sql-stmts/drop-operator-family/) - Removes an operator family.

## Privilege & Security {#privilege--security}

### Privilege {#privilege}

- [GRANT](/cloudberry/reference/sql-stmts/grant/) - Defines access privileges.
- [ALTER DEFAULT PRIVILEGES](/cloudberry/reference/sql-stmts/alter-default-privileges/) - Changes default access privileges.
- [REVOKE](/cloudberry/reference/sql-stmts/revoke/) - Removes access privileges.

### Row-level Security Policy {#row-level-security-policy}

- [CREATE POLICY](/cloudberry/reference/sql-stmts/create-policy/) - Defines a new row-level security policy for a table.
- [ALTER POLICY](/cloudberry/reference/sql-stmts/alter-policy/) - Changes the definition of a row-level security policy.
- [DROP POLICY](/cloudberry/reference/sql-stmts/drop-policy/) - Removes a row-level security policy from a table.

## Procedure {#procedure}

- [CREATE PROCEDURE](/cloudberry/reference/sql-stmts/create-procedure/) - Defines a new procedure.
- [ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/) - Changes the definition of a procedure.
- [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/) - Removes a procedure.
- [CALL](/cloudberry/reference/sql-stmts/call/) - Invokes a procedure.

## Protocol {#protocol}

- [CREATE PROTOCOL](/cloudberry/reference/sql-stmts/create-protocol/) - Registers a custom data access protocol that can be specified when defining a Apache Cloudberry external table.
- [ALTER PROTOCOL](/cloudberry/reference/sql-stmts/alter-protocol/) - Changes the definition of a protocol.
- [DROP PROTOCOL](/cloudberry/reference/sql-stmts/drop-protocol/) - Removes a data access protocol from a database.

## Resource Management {#resource-management}

### Resource Group {#resource-group}

- [CREATE RESOURCE GROUP](/cloudberry/reference/sql-stmts/create-resource-group/) - Defines a new resource group.
- [ALTER RESOURCE GROUP](/cloudberry/reference/sql-stmts/alter-resource-group/) - Changes the limits of a resource group.
- [DROP RESOURCE GROUP](/cloudberry/reference/sql-stmts/drop-resource-group/) - Removes a resource group.

### Resource Queue {#resource-queue}

- [CREATE RESOURCE QUEUE](/cloudberry/reference/sql-stmts/create-resource-queue/) - Defines a new resource queue.
- [ALTER RESOURCE QUEUE](/cloudberry/reference/sql-stmts/alter-resource-queue/) - Changes the limits of a resource queue.
- [DROP RESOURCE QUEUE](/cloudberry/reference/sql-stmts/drop-resource-queue/) - Removes a resource queue.

## Routine {#routine}

- [ALTER ROUTINE](/cloudberry/reference/sql-stmts/alter-routine/) - Changes the definition of a routine.
- [DROP ROUTINE](/cloudberry/reference/sql-stmts/drop-routine/) - Removes a routine.

## Rule {#rule}

- [CREATE RULE](/cloudberry/reference/sql-stmts/create-rule/) - Defines a new rewrite rule.
- [ALTER RULE](/cloudberry/reference/sql-stmts/alter-rule/) - Changes the definition of a rule.
- [DROP RULE](/cloudberry/reference/sql-stmts/drop-rule/) - Removes a rewrite rule.

## Row {#row}

- [INSERT](/cloudberry/reference/sql-stmts/insert/) - Creates new rows in a table.
- [SELECT](/cloudberry/reference/sql-stmts/select/) - Retrieves rows from a table or view.
- [UPDATE](/cloudberry/reference/sql-stmts/update/) - Updates rows of a table.
- [VALUES](/cloudberry/reference/sql-stmts/values/) - Computes a set of rows.

## Schema {#schema}

- [CREATE SCHEMA](/cloudberry/reference/sql-stmts/create-schema/) - Defines a new schema.
- [ALTER SCHEMA](/cloudberry/reference/sql-stmts/alter-schema/) - Changes the definition of a schema.
- [DROP SCHEMA](/cloudberry/reference/sql-stmts/drop-schema/) - Removes a schema.

## Sequence {#sequence}

- [CREATE SEQUENCE](/cloudberry/reference/sql-stmts/create-sequence/) - Defines a new sequence generator.
- [ALTER SEQUENCE](/cloudberry/reference/sql-stmts/alter-sequence/) - Changes the definition of a sequence generator.
- [DROP SEQUENCE](/cloudberry/reference/sql-stmts/drop-sequence/) - Removes a sequence.

## Session {#session}

- [SET SESSION AUTHORIZATION](/cloudberry/reference/sql-stmts/set-session-authorization/) - Sets the session role identifier and the current role identifier of the current session.
- [DISCARD](/cloudberry/reference/sql-stmts/discard/) - Discards the session state.

## Foreign Server {#foreign-server}

- [CREATE SERVER](/cloudberry/reference/sql-stmts/create-server/) - Defines a new foreign server.
- [ALTER SERVER](/cloudberry/reference/sql-stmts/alter-server/) - Changes the definition of a foreign server.
- [DROP SERVER](/cloudberry/reference/sql-stmts/drop-server/) - Removes a foreign server descriptor.
- [CREATE USER MAPPING](/cloudberry/reference/sql-stmts/create-user-mapping/) - Defines a new mapping of a user to a foreign server.
- [ALTER USER MAPPING](/cloudberry/reference/sql-stmts/alter-user-mapping/) - Changes the definition of a user mapping for a foreign server.
- [DROP USER MAPPING](/cloudberry/reference/sql-stmts/drop-user-mapping/) - Removes a user mapping for a foreign server.

## Statistics Object {#statistics-object}

- [CREATE STATISTICS](/cloudberry/reference/sql-stmts/create-statistics/) - Defines extended statistics.
- [ALTER STATISTICS](/cloudberry/reference/sql-stmts/alter-statistics/) - Changes the definition of an extended statistics object.
- [DROP STATISTICS](/cloudberry/reference/sql-stmts/drop-statistics/) - Removes extended statistics.

## Table {#table}

- [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/) - Defines a new table.
- [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/) - Changes the definition of a table.
- [DROP TABLE](/cloudberry/reference/sql-stmts/drop-table/) - Removes a table.
- [CLUSTER](/cloudberry/reference/sql-stmts/cluster/) - Physically reorders a table on disk according to an index.
- [CREATE TABLE AS](/cloudberry/reference/sql-stmts/create-table-as/) - Defines a new table from the results of a query.
- [DELETE](/cloudberry/reference/sql-stmts/delete/) - Deletes rows from a table
- [TRUNCATE](/cloudberry/reference/sql-stmts/truncate/) - Empties a table or set of tables of all rows.
- [IMPORT FOREIGN SCHEMA](/cloudberry/reference/sql-stmts/import-foreign-schema/) - Imports table definitions from a foreign server.
- [SELECT INTO](/cloudberry/reference/sql-stmts/select-into/) - Defines a new table from the results of a query.

## Tablespace {#tablespace}

- [CREATE TABLESPACE](/cloudberry/reference/sql-stmts/create-tablespace/) - Defines a new tablespace.
- [ALTER TABLESPACE](/cloudberry/reference/sql-stmts/alter-tablespace/) - Changes the definition of a tablespace.
- [DROP TABLESPACE](/cloudberry/reference/sql-stmts/drop-tablespace/) - Removes a tablespace.

## Text Search {#text-search}

### Text Search Configuration {#text-search-configuration}

- [CREATE TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/create-text-search-configuration/) - Defines a new text search configuration.
- [ALTER TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/alter-text-search-configuration/) - Changes the definition of a text search configuration.
- [DROP TEXT SEARCH CONFIGURATION](/cloudberry/reference/sql-stmts/drop-text-search-configuration/) - Removes a text search configuration.

### Text Search Dictionary {#text-search-dictionary}

- [CREATE TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/create-text-search-dictionary/) - Defines a new text search dictionary.
- [ALTER TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/alter-text-search-dictionary/) - Changes the definition of a text search dictionary.
- [DROP TEXT SEARCH DICTIONARY](/cloudberry/reference/sql-stmts/drop-text-search-dictionary/) - Removes a text search dictionary.

### Text Search Parser {#text-search-parser}

- [CREATE TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/create-text-search-parser/) - Defines a new text search parser.
- [ALTER TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/alter-text-search-parser/) - Changes the definition of a text search parser.
- [DROP TEXT SEARCH PARSER](/cloudberry/reference/sql-stmts/drop-text-search-parser/) - Removes a text search parser.

### Text Search Template {#text-search-template}

- [CREATE TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/create-text-search-template/) - Defines a new text search template.
- [ALTER TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/alter-text-search-template/) - Changes the definition of a text search template.
- [DROP TEXT SEARCH TEMPLATE](/cloudberry/reference/sql-stmts/drop-text-search-template/) - Removes a text search template.

## Transform {#transform}

- [CREATE TRANSFORM](/cloudberry/reference/sql-stmts/create-transform/) - Defines a new transform.
- [DROP TRANSFORM](/cloudberry/reference/sql-stmts/drop-transform/) - Removes a transform.

## Trigger {#trigger}

- [CREATE TRIGGER](/cloudberry/reference/sql-stmts/create-trigger/) - Defines a new trigger.
- [ALTER TRIGGER](/cloudberry/reference/sql-stmts/alter-trigger/) - Changes the definition of a trigger.
- [DROP TRIGGER](/cloudberry/reference/sql-stmts/drop-trigger/) - Removes a trigger.

## Data Type {#data-type}

- [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/) - Defines a new data type.
- [ALTER TYPE](/cloudberry/reference/sql-stmts/alter-type/) - Changes the definition of a data type.
- [DROP TYPE](/cloudberry/reference/sql-stmts/drop-type/) - Removes a data type.

## Transaction {#transaction}

- [BEGIN](/cloudberry/reference/sql-stmts/begin/) - Starts a transaction block.
- [ABORT](/cloudberry/reference/sql-stmts/abort/) - Terminates the current transaction.
- [COMMIT](/cloudberry/reference/sql-stmts/commit/) - Commits the current transaction.
- [END](/cloudberry/reference/sql-stmts/end/) - Commits the current transaction.
- [ROLLBACK](/cloudberry/reference/sql-stmts/rollback/) - Stops the current transaction.
- [START TRANSACTION](/cloudberry/reference/sql-stmts/start-transaction/) - Starts a transaction block.
- [SET TRANSACTION](/cloudberry/reference/sql-stmts/set-transaction/) - Sets the characteristics of the current transaction.
- [SAVEPOINT](/cloudberry/reference/sql-stmts/savepoint/) - Defines a new savepoint within the current transaction.
- [RELEASE SAVEPOINT](/cloudberry/reference/sql-stmts/release-savepoint/) - Destroys a previously defined savepoint.
- [ROLLBACK TO SAVEPOINT](/cloudberry/reference/sql-stmts/rollback-to-savepoint/) - Rolls back the current transaction to a savepoint.
- [LOCK](/cloudberry/reference/sql-stmts/lock/) - Locks a table.
- [SET CONSTRAINTS](/cloudberry/reference/sql-stmts/set-constraints/) - Sets constraint check timing for the current transaction.

## Configuration Parameter {#configuration-parameter}

- [SET](/cloudberry/reference/sql-stmts/set/) - Changes the value of a run-time Apache Cloudberry configuration parameter.
- [RESET](/cloudberry/reference/sql-stmts/reset/) - Restores the value of a run-time system configuration parameter to the default value.
- [SHOW](/cloudberry/reference/sql-stmts/show/) - Shows the value of a run-time system configuration parameter.

## SQL Statement {#sql-statement}

- [PREPARE](/cloudberry/reference/sql-stmts/prepare/) - Prepares a statement for execution.
- [DEALLOCATE](/cloudberry/reference/sql-stmts/deallocate/) - Deallocates a prepared statement.
- [EXECUTE](/cloudberry/reference/sql-stmts/execute/) - Runs a prepared SQL statement.
- [EXPLAIN](/cloudberry/reference/sql-stmts/explain/) - Shows the query plan of a statement.
