---
title: Mongo Shell Quick Start
description: Connect to DocumentDB with Docker or Linux packages with mongosh and insert and read your first document.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 70
---

Use `mongosh` to verify a local DocumentDB instance, inspect sample data, and run your first document commands.

<span id="have-a-running-document-db-instance"></span>

## Have a running DocumentDB instance? {#have-a-running-documentdb-instance}

If yes, keep it and continue with the client prerequisites below. Otherwise, choose one server installation:

- [Docker](https://documentdb.io/packages?method=docker): run a local container on Linux, macOS, or Windows. Recommended for evaluation and development.
- [Linux packages](https://documentdb.io/packages?method=packages): install the complete stack, then create a private PostgreSQL instance with the setup wizard.

The [Docker Quick Start](/documentdb/getting-started/docker/) and [Linux Packages Quick Start](/documentdb/getting-started/packages/) include the full server instructions. Do not start a second instance if one is already running.

These examples connect to `localhost:10260`, so run the client on the same host as DocumentDB. Use the credentials chosen for Docker, or username `admin` and the password chosen during Linux package setup. If you changed the endpoint, use its configured host and port.

Self-signed certificate bypasses below are for **local development only**. For network access, use a trusted certificate. Linux package setup binds the gateway on **all interfaces** by default: firewall port `10260` before setup and follow [network and certificate guidance](/documentdb/linux-packages/#before-exposing-it-to-a-network). Docker examples publish only on loopback.


## Prerequisites {#prerequisites}

- [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/)
- Your instance's endpoint and credentials (the examples use `localhost:10260`)

## Optional: start a Docker instance {#optional-start-a-docker-instance}

Skip this if you installed Linux packages or already have a running instance. If you chose Docker and have [Docker](https://www.docker.com/) installed:

```bash
docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> The DocumentDB Local image sends usage telemetry by default. To turn it off, add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

Replace the placeholders with your own credentials. Wait for the readiness banner in `docker logs documentdb` before connecting; see [Docker Quick Start](/documentdb/getting-started/docker/#verify-the-container).

## Connect and verify the connection {#connect-and-verify-the-connection}

Use your existing instance's credentials. The certificate bypass is for **local development only** with a self-signed certificate, whether you used Docker or installed Linux packages.

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsAllowInvalidCertificates
```

After you connect, run a quick health check:

```javascript
db.runCommand({ ping: 1 })

db.adminCommand({ listDatabases: 1 })
```

Successful output confirms authentication, TLS, and the gateway endpoint are working.

## Explore the built-in sample data {#explore-the-built-in-sample-data}

Sample data is **opt-in**, not required for your first insert and read. Linux package installations can add `--load-sample-data` during setup, which needs one extra tool; see [Set up and connect](/documentdb/getting-started/packages/#set-up-and-connect). Docker installations can start with `--init-data true`. Without these options, `StoreData` does not exist. Docker seeds the sample once per data volume: re-creating the container with `--init-data true` on a volume that was never seeded loads it without touching your data, and seeding again needs a new volume.

If you did not load the sample, skip directly to **Create your own collection** below.

```javascript
use StoreData

db.stores.find(
  {},
  { _id: 0, name: 1, city: 1, "sales.revenue": 1 }
).limit(3)

db.ratings.find({}, { _id: 1, rating: 1 }).limit(2)
```

## Create your own collection {#create-your-own-collection}

```javascript
use quickstart

db.movies.deleteMany({})

db.movies.insertMany([
  { title: "The Matrix", year: 1999, genres: ["sci-fi", "action"] },
  { title: "Dune", year: 2021, genres: ["sci-fi", "adventure"] },
  { title: "Arrival", year: 2016, genres: ["sci-fi", "drama"] }
])

db.movies.createIndex({ title: 1 })

db.movies.find(
  { year: { $gte: 2000 } },
  { _id: 0, title: 1, year: 1 }
).sort({ year: -1 })
```

## Use a trusted local certificate instead {#use-a-trusted-local-certificate-instead}

If you want certificate validation instead of `--tlsAllowInvalidCertificates`, obtain the trusted certificate or CA file for your endpoint. For Linux packages, follow [certificate configuration](/documentdb/linux-packages/#before-exposing-it-to-a-network). For Docker, copy the local certificate with:

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

Then pass your certificate file to `mongosh`:

```bash
mongosh localhost:10260 \
  -u '<YOUR_USERNAME>' \
  -p \
  --authenticationMechanism SCRAM-SHA-256 \
  --tls \
  --tlsCAFile ~/documentdb-cert.pem
```

## Troubleshooting and debugging {#troubleshooting-and-debugging}

If `mongosh` does not connect on the first try:

- Verify the local DocumentDB instance is running before you connect
- If you used Docker, check `docker ps --filter "name=documentdb"` and `docker logs documentdb`
- If you used Linux packages, check `sudo documentdb-setup --status`; for a manually built gateway, confirm its process is listening on port `10260`
- If authentication fails, confirm the username and password you used when you started DocumentDB
- If TLS validation fails, either keep `--tlsAllowInvalidCertificates` for the default local self-signed setup or switch to `--tlsCAFile` with a trusted certificate
- If `mongosh` is not installed, follow the [mongosh install guide](https://www.mongodb.com/docs/mongodb-shell/install/)
- Use [Python Quick Start](/documentdb/getting-started/python-setup/) or [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/) to verify the same endpoint from an application driver

## Next steps {#next-steps}

- [Visual Studio Code Quick Start](/documentdb/getting-started/vscode-quickstart/)
- [API Reference](/documentdb/reference/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [Python Quick Start](/documentdb/getting-started/python-setup/)
- [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/)
- [Samples Gallery](https://documentdb.io/samples)
