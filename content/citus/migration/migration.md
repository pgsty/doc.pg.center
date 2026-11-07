---
title: Migrate an existing application to Citus
description: This article describes the steps needed to migrate an existing application a Citus cluster on Microsoft Azure.
weight: 10
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
---

Migrating an existing application to Citus sometimes requires adjusting the schema and queries for optimal performance. Citus extends PostgreSQL with distributed functionality, but row-based sharding isn't a drop-in replacement that scales out all workloads. A performant Citus cluster involves thinking about the data model, tooling, and the choice of SQL features to use.

There's another mode of operation in Citus called schema-based sharding. While row-based sharding results in the best performance and hardware efficiency, consider schema-based sharding if you need a more drop-in approach.

## Step 1: Optimize the schema {#step-1-optimize-the-schema}

The first steps are to optimize the existing database schema so that it can work efficiently across multiple computers.

[Schema migration](/citus/migration/migration-schema/)

## Step 2: Update application queries {#step-2-update-application-queries}

Next, update your application code and queries to deal with the schema changes.

[Query migration](/citus/migration/migration-query/)

## Step 3: Migrate production data {#step-3-migrate-production-data}

After you test the changes in a development environment, the last step is to migrate production data to a Citus cluster and switch over the production app. We have techniques to minimize downtime for this step.

[Data migration](/citus/migration/migration-data/)

## Related content {#related-content}

- [What is Citus?](/citus/overview/what-is-citus/)
- [PostgreSQL at any scale with Citus](/citus/overview/postgresql-citus-scale/)
