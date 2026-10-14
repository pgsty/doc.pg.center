---
title: Install
weight: 1150
description: Instructions for installing etcd from pre-built binaries or from source.
icon: fa-solid fa-download
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/install.md"
---

## Requirements

Before installing etcd, see the following pages:

- [Supported platforms][]
- [Hardware recommendations][]

## Install pre-built binaries

The easiest way to install etcd is from pre-built binaries:

 1. Download the compressed archive file for your platform from [Releases][],
    choosing release [v3.7.2][tagged-release] or later.
 2. Unpack the archive file. This results in a directory containing the binaries.
 3. Add the executable binaries to your path. For example, rename and/or move
    the binaries to a directory in your path (like `/usr/local/bin`), or add the
    directory created by the previous step to your path.
 4. From a shell, test that `etcd` is in your path:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

## Build from source

For etcd v3.7.2, use [Go version 1.26+][go]; the release pins the Go 1.26.8 toolchain.
Build from source by following these steps:

 1. [Download the etcd repo as a zip file][download] and unzip it, or clone the
    repo using the following command.

    ```sh
    $ git clone -b v3.7.2 https://github.com/etcd-io/etcd.git
    ```
    To build from `main@HEAD`, omit the `-b v3.7.2` flag.

 2. Change directory:

    ```sh
    $ cd etcd
    ```
 3. Run the build script:

    ```sh
    $ ./scripts/build.sh
    ```

    The binaries are under the `bin` directory.

 4. Add the full path to the `bin` directory to your path, for example:

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

 5. Test that `etcd` is in your path:

    ```sh
    $ etcd --version
    ```

## Installation via OS packages
*Disclaimer: etcd installations through OS package managers can deliver outdated versions since they are not being automatically maintained nor officially supported by etcd project. Therefore use OS packages with caution.*

There are various ways of installing etcd on different operating systems and these are just some examples how it can be done.

### MacOS (Homebrew)

1. Update homebrew:
```sh
$ brew update
```

2. Install etcd:
```sh
$ brew install etcd
```

3. Verify install
```sh
$ etcd --version
```

## Linux

Although installing etcd through many major Linux distributions' official repositories and package managers is possible, the published versions can be significantly outdated. So, installing this way is strongly discouraged.

The recommended way to install etcd on Linux is either through [pre-built binaries](#install-pre-built-binaries) or by using Homebrew.

### Homebrew on Linux

[Homebrew can run on Linux], and can provide recent software versions.

- Prerequisites
  - Update Homebrew:

    ```sh
    $ brew update
    ```

- Procedure
  - Install using `brew`:

    ```sh
    $ brew install etcd
    ```

- Result
  - Verify installation by getting the version:

    ```sh
    $ etcd --version
    etcd Version: 3.7.2
    ...
    ```

    The output above is an example. Homebrew may provide a different patch version; check the installed version with `etcd --version`.

## Docker

etcd uses [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) as a
primary container registry, and [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) as
secondary.

To run etcd using Docker:

```sh
ETCD_VER=v3.7.2

rm -rf /tmp/etcd-data.tmp && mkdir -p /tmp/etcd-data.tmp && \
  docker rmi gcr.io/etcd-development/etcd:${ETCD_VER} || true && \
  docker run \
  -p 2379:2379 \
  -p 2380:2380 \
  --mount type=bind,source=/tmp/etcd-data.tmp,destination=/etcd-data \
  --name etcd-gcr-${ETCD_VER} \
  gcr.io/etcd-development/etcd:${ETCD_VER} \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://0.0.0.0:2379 \
  --advertise-client-urls http://0.0.0.0:2379 \
  --listen-peer-urls http://0.0.0.0:2380 \
  --initial-advertise-peer-urls http://0.0.0.0:2380 \
  --initial-cluster s1=http://0.0.0.0:2380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --log-level info \
  --logger zap \
  --log-outputs stderr

docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcd --version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdutl version
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl endpoint health
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl put foo bar
docker exec etcd-gcr-${ETCD_VER} /usr/local/bin/etcdctl get foo
```

## Installation as part of Kubernetes installation

- [Running etcd as a Kubernetes StatefulSet][]

## Installation check

For a slightly more involved sanity check of your installation, see
[Quickstart][].

[download]: https://github.com/etcd-io/etcd/archive/v3.7.2.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /etcd/op-guide/hardware/
[Quickstart]: /etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.2
[Supported platforms]: /etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
