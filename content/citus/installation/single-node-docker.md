---
title: Docker (Mac or Linux)
description: Learn how to run Citus using Docker on Mac or Linux so you can quickly test distributed PostgreSQL features.
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/single-node-docker?view=citus-14
upstream_ref: citus-14; 8445a2831f01
---

> [!NOTE]
> **The Docker image is intended for development/testing purposes only**, and isn't prepared for production use.

You can start Citus in Docker with one command:

```bash
# start the image
docker run -d --name citus -p 5432:5432 -e POSTGRES_PASSWORD=mypass \
           citusdata/citus:14.0

# verify it's running, and that Citus is installed:
psql -U postgres -h localhost -d postgres -c "SELECT * FROM citus_version();"
```

You should see Citus 14.x.

Once you have the cluster up and running, you can visit our tutorials on multitenant applications or real-time analytics to get started with Citus in minutes.

> [!NOTE]
> If you already have PostgreSQL running on your machine, you might encounter this error when starting the Docker containers:
> 
> ```text
> Error starting userland proxy:
> Bind for 0.0.0.0:5432: unexpected error address already in use
> ```
> 
> This error occurs when the Citus image attempts to bind to the standard PostgreSQL port 5432. To fix this error, choose a different port with the -p option. You need to also use the new port in the psql command.

## Related content {#related-content}

- [Single-node overview](/citus/installation/single-node/)
- [Single-node on Ubuntu or Debian](/citus/installation/single-node-debian/)
- [Single-node on CentOS or Red Hat](/citus/installation/single-node-rhel/)
