---
title: "Build with Docker Dev Image"
description: "This guide provides instructions for building Apache Cloudberry using a Docker-based development environment."
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/build-based-on-docker.md"
---

This method is particularly useful for ensuring a consistent build environment across different systems and for saving setup time.

## Prerequisites {#prerequisites}

- Docker: Ensure you have Docker installed on your system. You can download and install Docker from the official website: [Docker](https://www.docker.com/get-started).
- Harddisk space: Ensure you have at least 10 GB of free disk space available for the Docker image and build artifacts.

## Run the Docker Dev Image {#run-the-docker-dev-image}

Run the following command to start a Docker container with the Apache Cloudberry development image:

```bash {tab="Rocky Linux 8"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky8-latest
```
```bash {tab="Rocky Linux 9"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky9-latest
```
```bash {tab="Rocky Linux 10"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky10-latest
```
```bash {tab="Ubuntu 22.04"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-ubuntu22.04-latest
```
```bash {tab="Ubuntu 24.04"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-ubuntu24.04-latest
```

> [!NOTE]
> Rocky Linux 10 and Ubuntu 24.04 are supported starting from Apache Cloudberry 2.2.

Explaination:
- `--name=cbdb-dev` will set the name of the container to `cbdb-dev`. You can change it to any name you prefer.
- `-it` will run the container in interactive mode, allowing you to execute commands inside it.
- `--rm` will remove the container after you exit it. If you want to keep the container for further use, you can remove this option.
- `-h cdw` will set the hostname of the container to `cdw` (Coordinator Data Warehouse).
- `--shm-size=2gb` is used to set the container's shared memory for test suites run successfully. Test failures can occur when the Cloudberry cluster lacks sufficient shared memory resources, then you may need to increase the container's shared memory using this option.

This development environment has done the following things for you:
- Created a user named `gpadmin` with the necessary permissions.
- Set up the environment variables and paths.
- Configured the specific system resource limits.
- Installed the necessary dependencies.

Then you will be inside the Docker container with the Apache Cloudberry development environment ready to use. Before you go on, you need to make sure you have login the docker container as the `gpadmin` user like this:

```
======================================================================

                          ++++++++++       ++++++
                        ++++++++++++++   +++++++
                       ++++        +++++ ++++
                      ++++          +++++++++
                   =+====         =============+
                 ========       =====+      =====
                ====  ====     ====           ====
               ====    ===     ===             ====
               ====            === ===         ====
               ====            ===  ==--       ===
                =====          ===== --       ====
                 =====================     ======
                   ============================
                                     =-----=
     ____  _                    _  _
    / ___|| |  ___   _   _   __| || |__    ___  _ __  _ __  _   _
   | |    | | / _ \ | | | | / _` || '_ \  / _ \| '__|| '__|| | | |
   | |___ | || (_) || |_| || (_| || |_) ||  __/| |   | |   | |_| |
    \____||_| \____  \__,_| \__,_||_.__/  \___||_|   |_|    \__, |
                                                            |___/
----------------------------------------------------------------------

Welcome to the Apache Cloudberry Build Environment!

Container OS ........ : Rocky Linux 9.5 (Blue Onyx)
User ................ : gpadmin
Container hostname .. : cdw
IP Address .......... : 170.17.0.1
CPU Info ............ : Intel(R) Xeon(R) Gold 6151 CPU @ 3.00GHz
CPU(s) .............. : 8
Memory .............. : 15Gi total
======================================================================

[gpadmin@cdw ~]$
```

## What's next? {#whats-next}

- [Download the source code](/cloudberry/build/source/download-source-code/)
- [Configure Apache Cloudberry Build](/cloudberry/build/source/configure/)
- [Build and Install Apache Cloudberry and contrib extensions](/cloudberry/build/source/build-and-install/)
- [Set up a Cloudberry Demo Cluster](/cloudberry/build/source/set-demo-cluster/) (start with the step `Set up Cloudberry environment variables`)
- [Post installation](/cloudberry/build/source/post-installation/)

Or just running the following command more quickly:

> [!NOTE]
> Available since version 2.1.0.

```bash
## Download the source code
git clone --recurse-submodules --branch REL_2_STABLE --single-branch --depth=1 https://github.com/apache/cloudberry.git

## Change directory
cd /home/gpadmin/cloudberry

## Set up the SRC_DIR environment variable and create a directory for build logs
export SRC_DIR=/home/gpadmin/cloudberry
mkdir -p ${SRC_DIR}/build-logs

# Since Cloudberry 2.2
# Pre-stage the Python packages for `--with-pythonsrc-ext` before building
make -C gpMgmt/bin download-python-deps

## Configure, build, and install Cloudberry
./devops/build/automation/cloudberry/scripts/configure-cloudberry.sh
./devops/build/automation/cloudberry/scripts/build-cloudberry.sh

## Set up a Cloudberry Demo Cluster
./devops/build/automation/cloudberry/scripts/create-cloudberry-demo-cluster.sh

## Start a Cloudberry Demo Cluster
source /usr/local/cloudberry-db/cloudberry-env.sh
source /home/gpadmin/cloudberry/gpAux/gpdemo/gpdemo-env.sh
psql -p 7000 postgres
```
