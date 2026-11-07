---
title: Getting Started
description: Choose Docker or Linux packages, create a DocumentDB instance, and insert and read your first document
  with a shell, driver, or editor.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 10
---

## Choose an environment, then run your first query {#choose-an-environment-then-run-your-first-query}

Install with Docker or Linux packages once. Create a working instance, then insert
and read a document using a shell, driver, or editor.

1. **Choose an install path.** Start with Docker on Linux, macOS, or Windows.
   Use Linux packages when you need a host installation.

   **Docker: recommended for evaluation and development.** With Docker installed,
   run a local instance on Linux, macOS, or Windows. Replace the credential
   placeholders before running. The port stays on loopback.

   ```bash
   docker run -dt --pull always --name documentdb \
     -p 127.0.0.1:10260:10260 \
     -e USERNAME='<YOUR_USERNAME>' \
     -e PASSWORD='<YOUR_PASSWORD>' \
     ghcr.io/documentdb/documentdb/documentdb-local:latest
   ```

   > [!NOTE]
   > The DocumentDB Local image sends usage telemetry by default. To turn it off,
   > add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See
   > [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the
   > [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

   Wait for the readiness banner in `docker logs documentdb` before connecting.
   See the [Docker Quick Start](/documentdb/getting-started/docker/).

   **Linux packages.** For environments without Docker, or when you need control
   over PostgreSQL, topology, services, and configuration. Install with apt or dnf
   on Ubuntu 24.04 (Noble) or EL9, then run the setup wizard. Open
   [Linux packages installation](https://documentdb.io/packages?method=packages)
   or the full [Linux Packages Quick Start](/documentdb/getting-started/packages/).

2. **Insert and read your first document.** Pick the client you prefer. Each guide
   connects to the instance you already created and verifies an insert and read.
   Sample data is optional. Start with the
   [Visual Studio Code Quick Start](/documentdb/getting-started/vscode-quickstart/),
   [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/), or
   [Python Quick Start](/documentdb/getting-started/python-setup/).
{.steps}

DocumentDB is an open-source document database platform built on PostgreSQL. It offers developers a fully permissive, open-source platform for document data stores.

<span id="what-is-document-db"></span>

## What is DocumentDB? {#what-is-documentdb}

DocumentDB provides a NoSQL datastore implemented using PostgreSQL, giving developers complete visibility into the architecture and implementation of the engine. It's designed to offer:

- MongoDB wire protocol compatibility through the `pg_documentdb_gw` gateway, so MongoDB drivers and tools connect unmodified
- Public document CRUD and management APIs through the `pg_documentdb` extension
- Native BSON document support via the `pg_documentdb_core` PostgreSQL extension
- Advanced indexing capabilities including single field, multi-key, compound, text, geospatial, and vector indexes
- Vector search functionality powered by the `pgvector` PostgreSQL extension
- SCRAM-SHA-256 authentication and TLS on the gateway
- Full PostgreSQL compatibility for advanced SQL operations

## Key Features {#key-features}

- **PostgreSQL Foundation**: Built on the powerful PostgreSQL engine, allowing you to leverage both document and relational capabilities
- **Open Source**: Released under the MIT license with no restrictions on usage, modification, or distribution
- **Document Database Standard**: First implementation towards creating an open standard for document databases, similar to ANSI SQL for relational databases
- **Runs anywhere**: Linux packages, a container image for local development, and a Kubernetes operator for replicated deployments
- **Developer Friendly**: Rich ecosystem of tools and extensions, including VS Code integration and MongoDB compatibility

## Architecture Components {#architecture-components}

DocumentDB consists of four primary components:

1. **pg_documentdb_core**: Core PostgreSQL extension that provides native BSON storage, field access, and indexing primitives.
2. **pg_documentdb**: Public API surface that implements document commands, CRUD operations, query execution, and index management.
3. **pg_documentdb_gw**: Gateway that translates MongoDB wire protocol requests into PostgreSQL operations and handles authentication, sessions, and TLS.
4. **pg_documentdb_extended_rum**: The index access method behind DocumentDB's document indexes, required in 1.0.

Together, these components let you use DocumentDB through MongoDB-compatible tools and drivers while still benefiting from PostgreSQL internals.



## Common Use Cases {#common-use-cases}

- **Modern Web Applications**: Store and query JSON documents with MongoDB compatibility
- **AI/ML Applications**: Leverage vector search for similarity matching and embeddings
- **Hybrid Data Models**: Combine document and relational data in the same database
- **Migration Path**: Easy transition from existing MongoDB workloads
- **Local Development**: Full-featured local instance for development and testing

## Start here {#start-here}

Choose your environment once, create a working instance, then connect with the client that fits your goal:

1. **Choose Docker or Linux packages.** [Docker installation](https://documentdb.io/packages?method=docker) is recommended for evaluation and development on Linux, macOS, or Windows. [Linux packages installation](https://documentdb.io/packages?method=packages) is for environments without Docker, or when you need control over PostgreSQL, topology, services, and configuration.
2. **Create a working instance.** Follow the [Docker Quick Start](/documentdb/getting-started/docker/) or [Linux Packages Quick Start](/documentdb/getting-started/packages/). Linux package installation has two stages: install packages, then run the setup wizard. Neither copying a command nor installing files alone proves the endpoint is ready.
3. **Insert and read your first document.** Use the [Visual Studio Code Quick Start](/documentdb/getting-started/vscode-quickstart/), [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/), or [Python Quick Start](/documentdb/getting-started/python-setup/). Keep the same running instance; no second server installation is needed.

For advanced control, [use an existing local PostgreSQL instance](/documentdb/linux-packages/#adopt-an-existing-postgre-sql-instance) with administrator-managed configuration and restart, or [install the PostgreSQL extension only](/documentdb/linux-packages/#install-the-postgre-sql-extension-only). Extension-only installation does not install the gateway, so apps and drivers cannot connect; you use it through SQL.


## Verify your setup {#verify-your-setup}

Before moving on to application code, confirm that DocumentDB is reachable and can insert and read a document. For Docker, check `docker ps --filter "name=documentdb"` and wait for the readiness banner in `docker logs documentdb`; for Linux packages, inspect `sudo documentdb-setup --status`.

Run this shell example on the same host as DocumentDB. Use your Docker username, or `admin` for Linux packages, and enter your password at the prompt.

The certificate bypass is for **local development only**. Linux package setup binds the gateway on **all interfaces** by default: firewall port `10260` before setup and follow [network and certificate guidance](/documentdb/linux-packages/#before-exposing-it-to-a-network).

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

Then run:

```javascript
db.runCommand({ ping: 1 })
use quickstart
db.orders.insertOne({ item: "widget", qty: 5 })
db.orders.find({ item: "widget" })
```

The insert should report `acknowledged: true`, and the query should return your document. No sample-data loading is required.

For a fuller walkthrough, use the [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/). Driver-based examples are available in the [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/) and [Python Quick Start](/documentdb/getting-started/python-setup/).


## Troubleshooting and debugging {#troubleshooting-and-debugging}

If setup does not work on the first try:

- For Linux packages, check `sudo documentdb-setup --status` and [package troubleshooting](/documentdb/getting-started/packages/#troubleshooting). The default PostgreSQL 18 install uses `documentdb-local@18.target`, not the meta-package alias.
- For Docker, confirm the container is running and port `10260` is published with `docker ps`. Inspect startup, authentication, and TLS errors with `docker logs documentdb`.
- If you want certificate validation instead of `tlsAllowInvalidCertificates=true`, follow the Linux package [certificate steps](/documentdb/linux-packages/#before-exposing-it-to-a-network) or [DocumentDB Local](/documentdb/documentdb-local/) for Docker.
- For more verbose Docker diagnostics, re-create DocumentDB Local with `-e DOCUMENTDB_LOG_LEVEL=debug` (the `--log-level` flag is currently a no-op); the available runtime options are documented in [DocumentDB Local](/documentdb/documentdb-local/).
- To change your installation choice, open [Docker installation](https://documentdb.io/packages?method=docker) or [Linux packages installation](https://documentdb.io/packages?method=packages).


## Explore key features {#explore-key-features}

Once you can connect successfully, continue with these guides:

- [API Reference](/documentdb/reference/) - MongoDB command and operator coverage
- [Postgres Extension API](/documentdb/postgres-api/) - PostgreSQL-side functions, types, and operators
- [DocumentDB Local](/documentdb/documentdb-local/) - Local runtime options, sample data, certificates, and feature notes
- [Architecture under the hood](/documentdb/architecture/) - How the core, extension, and gateway fit together
- [Samples Gallery](https://documentdb.io/samples) - End-to-end examples you can adapt for your own apps



## Community and Support {#community-and-support}

- **Discord Community**: Join our [Discord server](https://discord.gg/vH7bYu524D) for:
  - Community syncs and office hours
  - Real-time technical support
  - Migration assistance
  - Best practices sharing
- GitHub Repository: [documentdb/documentdb](https://github.com/documentdb/documentdb)
- Documentation: Comprehensive guides and API references
- Issue Tracking: Report bugs and request features on GitHub

## Next Steps {#next-steps}

After you finish the initial setup:

- Continue with the [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/), [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/), or [Python Quick Start](/documentdb/getting-started/python-setup/)
- Explore the [API Reference](/documentdb/reference/) for detailed command and operator documentation
- Join our community to get support and contribute
