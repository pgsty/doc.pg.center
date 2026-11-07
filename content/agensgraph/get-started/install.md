---
title: Install AgensGraph
linkTitle: Install AgensGraph
description: Three routes.
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/install.html
upstream_source: agensgraph
upstream_modified: true
---


Three routes. Docker is the fastest way to a server you can query. A package is the usual
choice for a workstation or a single server. Build from source if you need to change
something, or if your platform has no package.

If you only want to try AgensGraph, use Docker and skip to [the example
dataset](/agensgraph/get-started/example-dataset/).

## Docker {#docker}

```shell
docker run --name agensgraph -e POSTGRES_PASSWORD=agensgraph -d skaiworldwide/agensgraph:v2.18.6.1-bookworm
```

Then open a client inside the container:

```shell
docker exec -it agensgraph agens -U agens -d postgres
```

The image accepts the same environment variables as the official `postgres` image —
`POSTGRES_USER`, `POSTGRES_DB`, `PGDATA` and the rest — so publish a port and mount a volume
the usual way:

```shell
docker run -d --name agensgraph \
  -e POSTGRES_PASSWORD=agensgraph \
  -p 5432:5432 \
  -v agensgraph-data:/var/lib/postgresql \
  skaiworldwide/agensgraph:v2.18.6.1-bookworm
```

Tags follow the release plus a base image: `v2.18.6.1-trixie`, `v2.18.6.1-bookworm`,
`v2.18.6.1-rocky10`, `v2.18.6.1-rocky9`, `v2.18.6.1-alpine3.24`, `v2.18.6.1-alpine3.23`. Pin one;
`skaiworldwide/agensgraph` on its own is a moving target.

> [!WARNING]
> The 2.18.6.1 images follow PostgreSQL 18's layout change. `PGDATA` now defaults to
> `/var/lib/postgresql/18/docker`, and the declared volume moved from
> `/var/lib/postgresql/data` to `/var/lib/postgresql`. A host volume that an earlier tag
> initialised will not be found by a 2.18.6.1 container unless you point at it explicitly:
>
>     -e PGDATA=/var/lib/postgresql/data -v /custom/mount:/var/lib/postgresql/data
>
> Read [Upgrading to 2.18](/agensgraph/release-notes/upgrade-to-2.18/) before reusing an existing data
> directory in any case — a 2.17 data directory cannot be started by 2.18.

## Packages {#packages}

Download a build for your platform from the [AgensGraph download
page](https://tech.skaiworldwide.com/downloads/) and unpack it where you want it, for example
`/usr/local/AgensGraph`:

```shell
tar xvf agensgraph-v2.18.6.1-build.tar.gz -C /usr/local
```

If you are not sure which build you need:

```shell
uname -sm
```

Then continue with [Set up a database](#set-up-a-database).

## Build from source {#build-from-source}

### Install the build dependencies {#install-the-build-dependencies}

{{< tabs >}}
{{< tab label="Ubuntu / Debian" >}}
```shell
sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison
```
{{< /tab >}}
{{< tab label="Rocky / RHEL" >}}
```shell
sudo yum install gcc glibc glib-common readline readline-devel zlib zlib-devel flex bison perl
```
{{< /tab >}}
{{< tab label="Fedora" >}}
```shell
sudo dnf install gcc glibc bison flex readline readline-devel zlib zlib-devel
```
{{< /tab >}}
{{< tab label="macOS" >}}
```shell
xcode-select --install
```
{{< /tab >}}
{{< /tabs >}}
### Build and install {#build-and-install}

```shell
git clone https://github.com/skaiworldwide-oss/agensgraph.git
cd agensgraph
./configure --prefix=$(pwd)
make install
```

`--prefix` decides where the binaries land. Without it, `make install` writes to
`/usr/local/pgsql`. Pointing it at the source tree, as above, keeps everything in one place
while you are trying things out.

To build the contrib modules as well — `pgvector` is not among them, but `file_fdw`, which
the [loading guide](/agensgraph/guides/loading-data/) uses, is:

```shell
make install-world
```

If `configure` cannot find a header it needs, tell it where to look with
`--with-includes=/path/to/headers`. `./configure --help` lists every option; they are
PostgreSQL's, and [PostgreSQL's installation
chapter](https://www.postgresql.org/docs/18/installation.html) documents them.

### Put the binaries on your path {#put-the-binaries-on-your-path}

```shell
export PATH=/path/to/agensgraph/bin:$PATH
export LD_LIBRARY_PATH=/path/to/agensgraph/lib:$LD_LIBRARY_PATH
```

Add those to `~/.bashrc`, or `~/.zshrc` on macOS, to make them stick.

## Set up a database {#set-up-a-database}

The tools are PostgreSQL's, with two renamed: `agens` is the interactive client and `ag_ctl`
starts and stops the server. See [The agens client](/agensgraph/reference/agens/).

Create a data directory:

```shell
initdb -D /path/to/data
```

Start the server:

```shell
ag_ctl -D /path/to/data -l /path/to/data/server.log start
```

Create a database:

```shell
createdb mydb
```

Setting `AGDATA` lets you drop the `-D` from later commands:

```shell
export AGDATA=/path/to/data
```

## Verify the install {#verify-the-install}

Connect:

```shell
agens mydb
```

Ask the server what it is:

```sql
SELECT version();
```

```
                                        version
-------------------------------------------------------------------------------------
 PostgreSQL 18.6 (AgensGraph 2.18.6.1) on x86_64-pc-linux-gnu, compiled by gcc ...
```

Then check that the graph half is there, which is the part a plain PostgreSQL build would
fail:

```psql
CREATE GRAPH check_install;
SET graph_path = check_install;
CREATE (:t {ok: true});
MATCH (n:t) RETURN n;
```

```
         n
--------------------
 t[3.1]{"ok": true}
```

```sql
DROP GRAPH check_install CASCADE;
```

`CASCADE` is needed because a graph owns the labels and sequences inside it.

## Next {#next}

[Load the example dataset](/agensgraph/get-started/example-dataset/), which every page in this manual uses, then
[run your first query](/agensgraph/get-started/first-query/).

For a production install — where the data directory goes, what to set in
`postgresql.conf`, how to run under systemd, and how to lock it down — see
[Deployment](/agensgraph/operations/deployment/) and [Configuration](/agensgraph/operations/configuration/).
