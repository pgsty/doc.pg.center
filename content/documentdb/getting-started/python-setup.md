---
title: Python Quick Start
description: Connect to DocumentDB with Docker or Linux packages with PyMongo and run your first queries from Python.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 60
---

Use PyMongo to connect to DocumentDB, verify authentication and TLS, and run your first document queries from Python.

<span id="have-a-running-document-db-instance"></span>

## Have a running DocumentDB instance? {#have-a-running-documentdb-instance}

If yes, keep it and continue with the client prerequisites below. Otherwise, choose one server installation:

- [Docker](https://documentdb.io/packages?method=docker): run a local container on Linux, macOS, or Windows. Recommended for evaluation and development.
- [Linux packages](https://documentdb.io/packages?method=packages): install the complete stack, then create a private PostgreSQL instance with the setup wizard.

The [Docker Quick Start](/documentdb/getting-started/docker/) and [Linux Packages Quick Start](/documentdb/getting-started/packages/) include the full server instructions. Do not start a second instance if one is already running.

These examples connect to `localhost:10260`, so run the client on the same host as DocumentDB. Use the credentials chosen for Docker, or username `admin` and the password chosen during Linux package setup. If you changed the endpoint, use its configured host and port.

Self-signed certificate bypasses below are for **local development only**. For network access, use a trusted certificate. Linux package setup binds the gateway on **all interfaces** by default: firewall port `10260` before setup and follow [network and certificate guidance](/documentdb/linux-packages/#before-exposing-it-to-a-network). Docker examples publish only on loopback.


## Prerequisites {#prerequisites}

- Python 3.9 or later
- pip
- Optional: [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/) for independent connection checks

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

## Create a virtual environment (optional) {#create-a-virtual-environment-optional}

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If you do not use a virtual environment, run the next commands with the Python interpreter you plan to use for your app.

<span id="install-py-mongo"></span>

## Install PyMongo {#install-pymongo}

```bash
python -m pip install pymongo
```

> PyMongo already includes the `bson` package it needs. Do not install the separate `bson` package from PyPI.

## Connect and run your first queries {#connect-and-run-your-first-queries}

Create a `quickstart.py` file. The certificate bypass is for **local development only**, with the default self-signed certificate from Linux package setup or Docker.

```python
import os

from pymongo import MongoClient

username = os.environ.get("DOCUMENTDB_USERNAME")
password = os.environ.get("DOCUMENTDB_PASSWORD")

if not username or not password:
    raise RuntimeError(
        "Set DOCUMENTDB_USERNAME and DOCUMENTDB_PASSWORD before running this script"
    )

client = MongoClient(
    "mongodb://localhost:10260/",
    username=username,
    password=password,
    authSource="admin",
    tls=True,
    tlsAllowInvalidCertificates=True,
)

try:
    client.admin.command("ping")

    db = client["quickstart"]
    movies = db["movies"]

    movies.delete_many({})
    movies.insert_many(
        [
            {"title": "The Matrix", "year": 1999, "genres": ["sci-fi", "action"]},
            {"title": "Dune", "year": 2021, "genres": ["sci-fi", "adventure"]},
            {"title": "Arrival", "year": 2016, "genres": ["sci-fi", "drama"]},
        ]
    )

    movies.create_index("title")

    for movie in movies.find(
        {"year": {"$gte": 2000}},
        {"_id": 0, "title": 1, "year": 1},
    ).sort("year", -1):
        print(movie)
finally:
    client.close()
```

Run the script:

```bash
python quickstart.py
```

You should see the recent movie documents printed after a successful `ping`.

## Explore the built-in sample data {#explore-the-built-in-sample-data}

Sample data is **opt-in**, not required for your first insert and read. Linux package installations can add `--load-sample-data` during setup, which needs one extra tool; see [Set up and connect](/documentdb/getting-started/packages/#set-up-and-connect). Docker installations can start with `--init-data true`. Without these options, `StoreData` does not exist. Docker seeds the sample once per data volume: re-creating the container with `--init-data true` on a volume that was never seeded loads it without touching your data, and seeding again needs a new volume.

If you loaded the sample, add this snippet after `client.admin.command("ping")`:

```python
for store in client["StoreData"]["stores"].find(
    {},
    {"_id": 0, "name": 1, "city": 1, "sales.revenue": 1},
).limit(3):
    print(store)
```

## Use a trusted local certificate instead {#use-a-trusted-local-certificate-instead}

If you want certificate validation instead of `tlsAllowInvalidCertificates=true`, obtain the trusted certificate or CA file for your endpoint and replace the original `MongoClient` call with the version below. For Linux packages, follow [certificate configuration](/documentdb/linux-packages/#before-exposing-it-to-a-network). For Docker, copy the local certificate with:

```bash
docker cp documentdb:/home/documentdb/.local/state/documentdb-gateway/tls/cert.pem ~/documentdb-cert.pem
```

```python
client = MongoClient(
    "mongodb://localhost:10260/",
    username=username,
    password=password,
    authSource="admin",
    tls=True,
    tlsCAFile="/absolute/path/documentdb-cert.pem",
)
```

## Troubleshooting and debugging {#troubleshooting-and-debugging}

If the Python quick start does not work on the first try:

- Verify your local DocumentDB instance is running before you start Python
- If you used Docker, check `docker ps --filter "name=documentdb"` and `docker logs documentdb`
- If you used Linux packages, check `sudo documentdb-setup --status`; for a manually built gateway, confirm its process is listening on port `10260`
- If Python cannot import `pymongo`, verify the active interpreter with `python -c "import sys; print(sys.executable)"` and reinstall with `python -m pip install pymongo`
- If you see TLS or certificate errors, either use the default local self-signed flow with `tlsAllowInvalidCertificates=true` or switch to a trusted local certificate with `tlsCAFile`
- Use [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/) to validate the endpoint independently of your application code

## Next steps {#next-steps}

- [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/)
- [Visual Studio Code Quick Start](/documentdb/getting-started/vscode-quickstart/)
- [DocumentDB Local](/documentdb/documentdb-local/)
- [API Reference](/documentdb/reference/)
- [Samples Gallery](https://documentdb.io/samples)
