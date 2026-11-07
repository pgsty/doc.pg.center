---
title: Node.js Quick Start
description: Connect to DocumentDB with Docker or Linux packages with the MongoDB Node.js driver and run your first
  queries.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 50
---

Connect to DocumentDB from Node.js using the official MongoDB driver.

<span id="have-a-running-document-db-instance"></span>

## Have a running DocumentDB instance? {#have-a-running-documentdb-instance}

If yes, keep it and continue with the client prerequisites below. Otherwise, choose one server installation:

- [Docker](https://documentdb.io/packages?method=docker): run a local container on Linux, macOS, or Windows. Recommended for evaluation and development.
- [Linux packages](https://documentdb.io/packages?method=packages): install the complete stack, then create a private PostgreSQL instance with the setup wizard.

The [Docker Quick Start](/documentdb/getting-started/docker/) and [Linux Packages Quick Start](/documentdb/getting-started/packages/) include the full server instructions. Do not start a second instance if one is already running.

These examples connect to `localhost:10260`, so run the client on the same host as DocumentDB. Use the credentials chosen for Docker, or username `admin` and the password chosen during Linux package setup. If you changed the endpoint, use its configured host and port.

Self-signed certificate bypasses below are for **local development only**. For network access, use a trusted certificate. Linux package setup binds the gateway on **all interfaces** by default: firewall port `10260` before setup and follow [network and certificate guidance](/documentdb/linux-packages/#before-exposing-it-to-a-network). Docker examples publish only on loopback.


## Prerequisites {#prerequisites}

- Node.js 20.19 or later (required by the current `mongodb` driver)
- npm
- Basic familiarity with JavaScript

## Set your client credentials {#set-your-client-credentials}

Set these in the terminal that will run your application. Replace the placeholders with your existing instance's credentials (for Linux packages, `admin` and your setup password). The driver passes them as raw values, not embedded in a connection URI.

```bash
export DOCUMENTDB_USERNAME='<YOUR_USERNAME>'
export DOCUMENTDB_PASSWORD='<YOUR_PASSWORD>'
```


## Optional: start a Docker instance {#optional-start-a-docker-instance}

Skip this if you installed Linux packages or already have a running instance. If you chose Docker and have [Docker](https://www.docker.com/) installed, replace the placeholders below with your chosen credentials. This self-contained command also sets the environment variables read by your application:

```bash
export DOCUMENTDB_USERNAME='<YOUR_USERNAME>'
export DOCUMENTDB_PASSWORD='<YOUR_PASSWORD>'

docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME="${DOCUMENTDB_USERNAME:?Set DOCUMENTDB_USERNAME}" \
  -e PASSWORD="${DOCUMENTDB_PASSWORD:?Set DOCUMENTDB_PASSWORD}" \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> The DocumentDB Local image sends usage telemetry by default. To turn it off, add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

Wait for the readiness banner in `docker logs documentdb` before connecting; see [Docker Quick Start](/documentdb/getting-started/docker/#verify-the-container).

## Create a project {#create-a-project}

```bash
mkdir my-documentdb-app
cd my-documentdb-app
npm init -y
npm install mongodb
```

## Connect and run your first queries {#connect-and-run-your-first-queries}

Create an `index.js` file. The certificate bypass is for **local development only**, with the default self-signed certificate from Linux package setup or Docker.

```javascript
const { MongoClient } = require("mongodb");

const username = process.env.DOCUMENTDB_USERNAME;
const password = process.env.DOCUMENTDB_PASSWORD;

if (!username || !password) {
  throw new Error(
    "Set DOCUMENTDB_USERNAME and DOCUMENTDB_PASSWORD before running this script"
  );
}

const uri = "mongodb://localhost:10260/";
const options = {
  auth: { username, password },
  authSource: "admin",
  tls: true,
  tlsAllowInvalidCertificates: true,
  directConnection: true
};

async function main() {
  const client = new MongoClient(uri, options);

  try {
    await client.connect();

    const db = client.db("quickstart");
    await db.command({ ping: 1 });

    const movies = db.collection("movies");

    await movies.insertMany([
      { title: "The Matrix", year: 1999, genres: ["sci-fi", "action"] },
      { title: "Dune", year: 2021, genres: ["sci-fi", "adventure"] },
      { title: "Arrival", year: 2016, genres: ["sci-fi", "drama"] }
    ]);

    await movies.createIndex({ title: 1 });

    const recentMovies = await movies
      .find(
        { year: { $gte: 2000 } },
        { projection: { _id: 0, title: 1, year: 1 } }
      )
      .sort({ year: -1 })
      .toArray();

    console.log("Connected to DocumentDB");
    console.log(recentMovies);
  } finally {
    await client.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Run the script:

```bash
node index.js
```

## Connect with a trusted local certificate instead {#connect-with-a-trusted-local-certificate-instead}

If you want certificate validation instead of `tlsAllowInvalidCertificates=true`, obtain the trusted certificate or CA file for your endpoint and replace the original `options` object with the version below. For Linux packages, follow [certificate configuration](/documentdb/linux-packages/#before-exposing-it-to-a-network). For Docker, copy the local certificate with:

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

```javascript
const options = {
  auth: { username, password },
  authSource: "admin",
  tls: true,
  tlsCAFile: "/absolute/path/documentdb-cert.pem",
  directConnection: true
};
```

## Next steps {#next-steps}

- [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/)
- [Python Quick Start](/documentdb/getting-started/python-setup/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [Samples Gallery](https://documentdb.io/samples)
