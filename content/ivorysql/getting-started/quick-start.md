---
title: Quick Start
linkTitle: Quick Start
description: 'IvorySQL v5.6 documentation: Quick Start.'
type: docs
weight: 40
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/3.1.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

## 1. Environmental requirements {#environmental-requirements}

- Hardware

| Parameter | Minimum         | Recommended      |
|---|---|---|
| CPU       | 4 cores         | 16 cores         |
| RAM       | 4GB             | 64GB             |
| Storage   | 800MB,HDD       | 5GB+,SSD or NvMe |
| Network   | Gigabit network | 10G network      |

- Software

  Currently, IvorySQL supports but is not limited to linux(CentOS 8.X/CentOS Stream 9/Ubuntu).

## 2. Quick installation {#quick-installation}

The operating system used for the quick start is CentOS Stream 9.

### 2.1. yum installation {#yum-installation}

- Pre-requirements

  Before getting started, please create an user and grant it root privileges. All the installation steps will be performed by this user. Here we just name it 'ivorysql'. [How to create a sudo user](https://www.ionos.com/help/server-cloud-infrastructure/server-administration/creating-a-sudo-enabled-user)

- installation

  Create or edit IvorySQL yum repository configuration /etc/yum.repos.d/ivorysql.repo

```
vim /etc/yum.repos.d/ivorysql.repo
[ivorysql5]
name=IvorySQL Server 5 $releasever - $basearch
baseurl=https://yum.highgo.com/dists/ivorysql-rpms/5/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=0
```

After saving and exiting, you can install IvorySQL 5 with the following steps

```
$ sudo dnf install -y ivorysql5-5.6
```

<span id="anchor-en-3.1-setting-environment-variables"></span>

- Setting environment variables

  Add below contents in ~/.bash_profile file and source to make it effective:

```
PATH=/usr/ivory-5/bin:$PATH
export PATH
PGDATA=/usr/ivory-5/data
export PGDATA
```

```
$ source ~/.bash_profile
```

- Initializing database

```
$ initdb -D /usr/ivory-5/data
```

The -D option specifies the directory where the database cluster should be stored. This is the only information required by initdb, but you can avoid writing it by setting the PGDATA environment variable, which can be convenient since the database server can find the database directory later by the same variable. For more options, refer to initdb --help.

- Starting IvorySQL service

```
$ pg_ctl -D /usr/ivory-5/data -l ivory.log start
```

The -D option specifies the file system location of the database configuration files. If this option is omitted, the environment variable PGDATA in [Setting environment variables](#anchor-en-3.1-setting-environment-variables) is used. -l option appends the server log output to filename. If the file does not exist, it is created.

For more options, refer to pg_ctl --help.

Confirm it’s successfully started:

```
$ ps -ef | grep postgres
ivorysql  3214     1  0 20:35 ?        00:00:00 /usr/ivory-5/bin/postgres -D /usr/ivory-5/data
ivorysql  3215  3214  0 20:35 ?        00:00:00 postgres: checkpointer
ivorysql  3216  3214  0 20:35 ?        00:00:00 postgres: background writer
ivorysql  3218  3214  0 20:35 ?        00:00:00 postgres: walwriter
ivorysql  3219  3214  0 20:35 ?        00:00:00 postgres: autovacuum launcher
ivorysql  3220  3214  0 20:35 ?        00:00:00 postgres: logical replication launcher
ivorysql  3238  1551  0 20:35 pts/0    00:00:00 grep --color=auto postgres
```

### 2.2. Running IvorySQL in docker {#running-ivorysql-in-docker}

- Get IvorySQL image from Docker Hub

```
$ docker pull ivorysql/ivorysql:5.6-ubi8
```

> [!TIP]
>
> Users in China can also pull from the IvorySQL community Harbor registry for faster downloads, e.g. `docker pull registry.highgo.com/ivorysql/ivorysql:5.6-ubi8`.

- Running IvorySQL

```
$ docker run --name ivorysql -p 5434:5432 -e IVORYSQL_PASSWORD=your_password -d ivorysql/ivorysql:5.6-ubi8
```

- Check if the IvorySQL container is running successfully

```
$ docker ps | grep ivorysql
CONTAINER ID   IMAGE               COMMAND                   CREATED          STATUS          PORTS                              NAMES
6faa2d0ed705   ivorysql/ivorysql:5.6-ubi8   "docker-entrypoint.s…"   50 seconds ago   Up 49 seconds   5866/tcp, 0.0.0.0:5434->5432/tcp   ivorysql
```

## 3. Connecting to IvorySQL {#connecting-to-ivorysql}

Connect to IvorySQL via psql:

```
$ psql -d YOUR_DATABASE
psql (18.6)
Type "help" for help.

ivorysql=#
```

The -d option specifies the name of the database to connect to. ivorysql is the default database of IvorySQL. However,IvorySQL of lower versions need the users themselves to connect to postgres database at the first connection and then create the ivorysql database.The latest IvorySQL can do all these for users. For more options, refer to psql --help.

> [!TIP]
>
> When running IvorySQL in Docker, additional parameters need to be added, like: psql -d ivorysql -U ivorysql -h 127.0.0.1 -p 5434

Now you can start your journey of IvorySQL! Enjoy!

To explore additional installation methods, please refer to the [Installation](/ivorysql/deploy/installation/).
