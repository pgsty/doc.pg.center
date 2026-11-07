---
title: Docker Quick Start
description: Start DocumentDB Local with Docker, verify the connection, and find troubleshooting and next-step guidance.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 20
---

Run DocumentDB locally with Docker and verify the setup before moving to driver code. For installation choices, open [Docker installation](https://documentdb.io/packages?method=docker) or [Linux packages installation](https://documentdb.io/packages?method=packages).

## Prerequisites {#prerequisites}

- [Docker](https://www.docker.com/)
- [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/) for the fastest connection check
- A local port available for DocumentDB (the examples use `10260`)

<span id="start-document-db"></span>

## Start DocumentDB {#start-documentdb}

Pull the image first; this also replaces an older cached `latest`:

```bash
docker pull ghcr.io/documentdb/documentdb/documentdb-local:latest
```

Then start the container:

```bash
docker run -dt --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest \
  --init-data true
```

> [!NOTE]
> The DocumentDB Local image sends usage telemetry by default. To turn it off, add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

> Replace `<YOUR_USERNAME>` and `<YOUR_PASSWORD>` with your own credentials.
>
> `-p 127.0.0.1:10260:10260` keeps the endpoint on loopback. A bare `-p 10260:10260`
> publishes it on **every** interface, which is rarely what you want on a laptop.
>
> `--init-data true` seeds the built-in sample data into `StoreData`, which the
> verification step below queries. It is **not** enabled by default — without it the
> container starts with no `StoreData` database and `use StoreData` returns nothing. The data is
> seeded once per data volume. Existing volumes are not migrated automatically;
> re-create the volume to seed again. See
> [DocumentDB Local](/documentdb/documentdb-local/) for `--init-data-path`, certificate setup,
> and additional runtime options.

## Verify the container {#verify-the-container}

```bash
docker ps --filter "name=documentdb"
```

You should see the container in an `Up` state with port `10260` published.

> [!IMPORTANT]
> `docker ps` reports `Up` well before DocumentDB accepts connections. Wait for the
> readiness banner, or the first `mongosh` call fails with a connection error:
>
> ```bash
> until docker logs documentdb 2>&1 | grep -q "=== DocumentDB is ready ==="; do sleep 2; done
> ```

## Verify the connection {#verify-the-connection}

Use `mongosh` to confirm authentication, TLS, and the gateway endpoint are working:

The certificate bypass below is for **local development only**. Use a trusted certificate before connecting over a shared or public network.

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

Then run a quick health check. The sample data below needs `--init-data true` on the `docker run` above — without it `StoreData` does not exist:

```javascript
db.runCommand({ ping: 1 })

use StoreData

db.stores.find({}, { _id: 0, name: 1, city: 1, "sales.revenue": 1 }).limit(3)
```

Write and read back your own document; this does not require sample data:

```javascript
use quickstart
db.orders.insertOne({ item: "widget", qty: 5 })
db.orders.find({ item: "widget" })
```

If you prefer certificate validation instead of `--tlsAllowInvalidCertificates`, follow the certificate steps in [DocumentDB Local](/documentdb/documentdb-local/).

## Persistence and initialization {#persistence-and-initialization}

The quick start command above is ideal for disposable local environments. When you need more control:

- Use `--data-path` with a mounted host directory to keep data across container restarts
- Omit `--init-data true` if you want an empty instance instead of the `StoreData` collections
- Use `--init-data-path` to run your own `.js` initialization scripts with `mongosh` at startup

The built-in `StoreData` sample dataset includes 41,505 documents in `stores` and 2 documents in `ratings`.

## Stop, start, and remove {#stop-start-and-remove}

```bash
docker stop documentdb       # stop, keep the data
docker start documentdb      # bring it back later
docker restart documentdb
docker logs documentdb       # gateway and startup output
```

To update the image or start over:

```bash
# DESTROYS the container and its anonymous data volume
docker rm -fv documentdb
docker pull ghcr.io/documentdb/documentdb/documentdb-local:latest
# then run the Start DocumentDB command again
```

Until you remove it, re-running `docker run --name documentdb` fails with
`Conflict. The container name "/documentdb" is already in use`. Mount a named volume
(`-v documentdb-data:/data`) before storing anything you want to keep.

A newer image on an existing data volume does not update the DocumentDB schema in that
volume ([documentdb#773](https://github.com/documentdb/documentdb/issues/773)). To move data
from an earlier release or a 1.0 release candidate to 1.0, start the 1.0 image on a new
volume and reload your data, for example with `mongodump` and `mongorestore`.

## Troubleshooting and debugging {#troubleshooting-and-debugging}

If something does not work as expected:

- Confirm port `10260` is available and that `docker ps` shows the container running
- Inspect startup, authentication, and TLS errors with `docker logs documentdb`
- For more gateway detail, re-create the container with `-e DOCUMENTDB_LOG_LEVEL=debug`. The `--log-level` flag is validated at startup but does not currently change what the container logs, and environment variables are fixed at `docker run` — `docker restart` cannot change either.
- Use the certificate flow in [DocumentDB Local](/documentdb/documentdb-local/) if your client should validate TLS certificates
- Use [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/) for a fuller shell walkthrough

## Next steps {#next-steps}

- [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/)
- [Python Quick Start](/documentdb/getting-started/python-setup/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [Samples Gallery](https://documentdb.io/samples)
- [Linux Packages Quick Start](/documentdb/getting-started/packages/)
- [Install DocumentDB](https://documentdb.io/packages?method=packages)
