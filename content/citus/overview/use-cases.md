---
title: Use cases
description: This article describes Use Cases.
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/use-cases?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
---

After [Getting Started](/citus/installation/getting-started/), it's time to go deeper into the most common use-cases for Citus.

- [Choosing a distribution column](/citus/modeling/data-modeling/) is a hands-on guide for building the backend of an example ad analytics app. The article reviews data modeling for distributed systems, including how to adapt an existing single-machine database schema. It also outlines common challenges for scaling and how to solve them.
- [Building a scalable PostgreSQL metrics backend using the Citus extension](/citus/articles/metrics-dashboard/) outlines the other prominent Citus use case: super fast, highly parallel aggregate queries. The article shows how to model the backend for a web dashboard for event data. It also discusses managing constantly increasing data, even when the data is unstructured.

Once you learn these use-cases in depth, you can learn more about [Migrating an existing app](/citus/migration/migration/) to port your existing application.

## Related content {#related-content}

- [Multitenant applications tutorial](/citus/tutorials/tutorial-multi-tenant/)
- [Analytics and dashboards tutorial](/citus/tutorials/tutorial-analytics/)
- [What is Citus?](/citus/overview/what-is-citus/)
