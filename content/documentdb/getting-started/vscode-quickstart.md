---
title: Visual Studio Code Quick Start
description: Install the VS Code extension, connect to DocumentDB with Docker or Linux packages, and insert and
  read your first document.
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 40
---

Use the DocumentDB extension for Visual Studio Code to set up a local DocumentDB instance, browse sample data, and create your first database without leaving the editor.

The extension can create the instance for you: it pulls the official image, creates a container and persistent data volume, generates credentials, waits until the database accepts connections, and saves the connection. It does not install Docker.

Already running DocumentDB? Skip provisioning and [connect your existing instance](#connect-an-existing-instance).

## Prerequisites {#prerequisites}

- [Visual Studio Code](https://code.visualstudio.com/)
- The [DocumentDB extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
- Docker Desktop or Docker Engine, set to Linux containers, running wherever VS Code is
- Optional: [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/) for independent connection checks

Docker must be reachable from the environment VS Code runs in. If you work in WSL, a dev container, an SSH remote, or Codespaces, Docker needs to be available there rather than only on your host machine. Setup runs a readiness check and explains what to fix if it cannot reach Docker.

## Install the extension {#install-the-extension}

Install the extension from the VS Code marketplace, or run:

```bash
code --install-extension ms-azuretools.vscode-documentdb
```

To update an older install, add `--force`; without it the command keeps the version you have. Reload VS Code after installing or updating, because the running window keeps using the previous version until then.

<span id="set-up-document-db-local"></span>

## Set up DocumentDB Local {#set-up-documentdb-local}

Use guided setup to let the extension provision DocumentDB Local and save its connection. There are no Docker commands for you to run.

1. Open setup using any of these:
   - Select the DocumentDB icon in the activity bar, expand **Your own DocumentDB** in the Connections view, and select **Set up DocumentDB Local**.
   - Run **DocumentDB: Set up DocumentDB Local** from the Command Palette.
   - Open `vscode://ms-azuretools.vscode-documentdb/local` from your browser and confirm the prompts. This needs extension version 0.10.1 or later, so install or update the extension first; the link cannot always install it for you.
2. On the **Introduction** step, select **Continue**. Nothing is downloaded or created until the next step.
3. On the **Configure** step, review the defaults and select **Start DocumentDB Local**. The defaults give you an available port (starting at `10260`), generated credentials, the `latest` official image, and optional sample data. Expand the advanced options to set the port, image tag, or credentials yourself.
4. Wait for setup to finish. The extension creates a container named `vscode-documentdb-local` with a persistent volume, then waits until the database accepts connections.
5. Select **Open Connection** to reveal the saved connection, then expand it to browse databases and collections.

Sample data is enabled by default. If you keep it enabled, expand the saved connection to browse the sample database and collections.

Right-click the DocumentDB Local entry to **Start**, **Stop**, **Restart**, or **Delete Container**, and to **Copy Connection String**, **Copy Password**, or **View Logs**. Stopping and starting preserves your data; deleting removes the volume and the generated credentials permanently.

## Alternative: start the container yourself {#alternative-start-the-container-yourself}

Use this if you want to manage the container yourself. If DocumentDB is already running, skip this step and [connect your existing instance](#connect-an-existing-instance).

Start it with Docker:

```bash
docker run -dt --pull always --name documentdb \
  -p 127.0.0.1:10260:10260 \
  -e USERNAME='<YOUR_USERNAME>' \
  -e PASSWORD='<YOUR_PASSWORD>' \
  ghcr.io/documentdb/documentdb/documentdb-local:latest
```

> [!NOTE]
> The DocumentDB Local image sends usage telemetry by default. To turn it off, add `-e DOCUMENTDB_USAGE_TELEMETRY=false` before the image name. See [Usage telemetry](/documentdb/documentdb-local/#usage-telemetry) and the [privacy statement](https://github.com/documentdb/documentdb/blob/v1.0-0/documentdb-local/PRIVACY.md).

If you prefer a host installation instead of Docker, use the [Linux Packages Quick Start](/documentdb/getting-started/packages/) on a distribution in the current release matrix.

## Connect an existing instance {#connect-an-existing-instance}

Use this for a DocumentDB instance that is already running. You only add a connection; you do not need to run the setup wizard or create another container. Have the instance's port, username, and password ready.

1. Open the **DocumentDB** view in the VS Code activity bar.
2. In the local connection area, select **DocumentDB Local** and start the **New Local Connection** flow.
3. Enter your instance's port (`10260` for the command above), username, and password.
4. At the TLS/SSL prompt:
   - For **local development only**, choose **Disable TLS/SSL (Not recommended)** if you are using the default self-signed local setup and have not configured trust for the certificate yet.
   - Keep **Enable TLS/SSL (Default)** if you already configured a trusted local certificate.
5. Finish the wizard and confirm the new connection appears in the connections tree.

## Verify the connection in the extension {#verify-the-connection-in-the-extension}

Guided setup loads sample data by default unless you turn that option off. The manual Docker command above starts without sample data; the [Docker Quick Start](/documentdb/getting-started/docker/) shows how to enable it.

1. Expand your saved connection. If sample data was loaded, open a sample database and collection to browse the documents.
2. Create your own database and collection from the context menu. An empty instance is expected when sample data is disabled.
3. In your own collection, add a test document like:

```json
{
  "name": "VS Code Quick Start",
  "source": "vscode",
  "status": "connected"
}
```

Switch between the **Table**, **Tree**, and **JSON** views to confirm the extension can read the document.

If you prefer to validate outside the extension first, use [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/).

## Import, export, and querying {#import-export-and-querying}

After the connection works, the extension can help you continue without leaving VS Code:

- Import JSON documents into a collection
- Export query results or full collections
- Browse documents in multiple views with pagination
- Open the query editor and continue with commands from the [API Reference](/documentdb/reference/)

## Troubleshooting and debugging {#troubleshooting-and-debugging}

If setup or the connection does not work on the first try:

- If the browser link does nothing, confirm VS Code is installed and that you allowed the browser to open it. If VS Code opens but setup does not start, install or update the extension, reload VS Code, and open the link again, or run **DocumentDB: Set up DocumentDB Local** from the Command Palette instead
- If VS Code reports that **a DocumentDB deep-link was opened without a connection string**, the extension is older than 0.10.1. Run `code --install-extension ms-azuretools.vscode-documentdb --force`, reload VS Code, and open the link again
- If VS Code reports **No extension gallery service configured**, or nothing happens when the extension is missing, the link could not install it for you. This is common on managed devices that use a private marketplace. Install the extension yourself with `code --install-extension ms-azuretools.vscode-documentdb`, then open the link again
- If setup reports that Docker is unreachable, fix what it names (Docker not running, or Docker set to Windows containers rather than Linux) and select **Continue setup**; nothing has been created at that point
- Verify the extension is installed and reload VS Code if the DocumentDB view does not appear
- Confirm your local DocumentDB instance is actually running before you connect
- If you used Docker, check `docker ps` and `docker logs documentdb`
- If you used Linux packages, check `sudo documentdb-setup --status`; for a manually built gateway, confirm its process is listening on the port you entered
- If the local connection wizard fails on security, retry and choose the TLS/SSL option that matches your certificate setup
- Use `mongosh` to confirm the endpoint works independently of VS Code

For extension-specific help or bugs:

- [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-documentdb)
- [GitHub repository](https://github.com/microsoft/vscode-documentdb)
- [GitHub discussions](https://github.com/microsoft/vscode-documentdb/discussions)
- [GitHub issues](https://github.com/microsoft/vscode-documentdb/issues)
- [DocumentDB Discord](https://discord.gg/vH7bYu524D)

## Next steps {#next-steps}

- [Documentation for the DocumentDB extension for Visual Studio Code](https://github.com/microsoft/vscode-documentdb/tree/main/docs)
- [Docker Quick Start](/documentdb/getting-started/docker/)
- [Linux Packages Quick Start](/documentdb/getting-started/packages/)
- [Mongo Shell Quick Start](/documentdb/getting-started/mongo-shell-quickstart/)
- [Node.js Quick Start](/documentdb/getting-started/nodejs-setup/)
- [Python Quick Start](/documentdb/getting-started/python-setup/)
- [API Reference](/documentdb/reference/)
