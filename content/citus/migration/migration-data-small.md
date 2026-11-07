---
title: Small database migration
description: This article describes the steps needed to migrate a small PostgreSQL database to a Citus cluster on Microsoft Azure.
weight: 50
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-data-small?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
---

For smaller environments that can tolerate a little downtime, use a straightforward pg_dump/pg_restore process. Here are the steps.

1. Save the database structure from your development database:

   ```bash
   pg_dump \
      --format=plain \
      --no-owner \
      --schema-only \
      --file=schema.sql \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```
2. Connect to the Citus cluster using psql and create the schema:

   ```psql
   \i schema.sql
   ```
3. Run your `create_distributed_table` and `create_reference_table` statements. If you get an error about foreign keys, it's typically due to the order of operations. Drop foreign keys before distributing tables and then readd them.
4. Put the application into maintenance mode, and disable any other writes to the old database.
5. Save the data from the original production database to disk with `pg_dump`:

   ```bash
   pg_dump \
      --format=custom \
      --no-owner \
      --data-only \
      --file=data.dump \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```
6. Import into Citus using `pg_restore`:

   ```bash
   # remember to use connection details for Citus,
   # not the source database
   pg_restore  \
      --host=host \
      --dbname=dbname \
      --username=username \
      data.dump
   
   # it'll prompt you for the connection password
   ```
7. Test application.
8. Launch!

## Related content {#related-content}

- [Data migration](/citus/migration/migration-data/)
- [Large data migration with replication](/citus/migration/migration-data-big/)
- [Migration overview](/citus/migration/migration/)
