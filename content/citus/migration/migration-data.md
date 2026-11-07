---
title: Migrate production data
description: This article introduces the two main paths for migrating production data from a PostgreSQL database to a Citus cluster on Microsoft Azure.
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-data?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
---

At this time, after updating the database schema and application queries to work with Citus, you're ready for the final step. It's time to migrate data to the Citus cluster and cut over the application to its new database.

The data migration path is dependent on downtime requirements and data size, but generally falls into one of the following two categories.

## In this section {#in-this-section}

| Article | Description |
| --- | --- |
| [Small data migrations](/citus/migration/migration-data-small/) | For datasets that allow brief downtime during migration. |
| [Big data migrations](/citus/migration/migration-data-big/) | For large datasets requiring minimal or zero downtime. |

## Related content {#related-content}

- [Migrating an Existing App](/citus/migration/migration/)
- [Query migration](/citus/migration/migration-query/)
- [Schema migration](/citus/migration/migration-schema/)
