---
title: Single-node Citus clusters on Ubuntu or Debian
description: Learn how to install single-node Citus on Debian or Ubuntu so you can start using distributed PostgreSQL locally.
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/single-node-debian?view=citus-14
upstream_ref: citus-14; 8445a2831f01
---

This section describes the steps needed to set up a single-node Citus cluster on your own Linux machine from deb packages.

## 1. Install PostgreSQL 18 and the Citus extension {#1-install-postgresql-17-and-the-citus-extension}

```sh
# Add Citus repository for package manager
curl https://install.citusdata.com/community/deb.sh | sudo bash

# install the server and initialize db
sudo apt-get -y install postgresql-18-citus-14.0
```

## 2. Initialize the cluster {#2-initialize-the-cluster}

Create a new database on disk. For convenience with PostgreSQL Unix domain socket connections, use the postgres user.

```sh
# this user has access to sockets in /var/run/postgresql
sudo su - postgres

# include path to PostgreSQL binaries
export PATH=$PATH:/usr/lib/postgresql/18/bin

cd ~
mkdir citus
initdb -D citus
```

Citus is a PostgreSQL extension. To tell PostgreSQL to use this extension, add it to a configuration variable called `shared_preload_libraries`:

```sh
echo "shared_preload_libraries = 'citus'" >> citus/postgresql.conf
```

## 3. Start the database server {#3-start-the-database-server}

Finally, start an instance of PostgreSQL for the new directory:

```sh
pg_ctl -D citus -o "-p 9700" -l citus_logfile start
```

After you add Citus to `shared_preload_libraries`, Citus hooks into some deep parts of PostgreSQL, swapping out the query planner and executor. Here, you load the user-facing side of Citus, such as the functions to call:

```sh
psql -p 9700 -c "CREATE EXTENSION citus;"
```

## 4. Verify that installation succeeded {#4-verify-that-installation-succeeded}

To verify that the installation succeeded, and Citus is installed:

```sh
psql -p 9700 -c "select citus_version();"
```

You should see details of the Citus extension.

After you complete the installation process, you're ready to use your Citus cluster. To help you get started, see [Multitenant applications](/citus/tutorials/tutorial-multi-tenant/). This tutorial has instructions on setting up a Citus cluster with sample data in minutes.

## Related content {#related-content}

- [Single-node overview](/citus/installation/single-node/)
- [Single-node on Docker](/citus/installation/single-node-docker/)
- [Single-node on Fedora, CentOS, or Red Hat](/citus/installation/single-node-rhel/)
