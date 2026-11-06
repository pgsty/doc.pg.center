---
title: "Download Source Code"
description: "Download an Apache Cloudberry release or development branch and its submodules as the gpadmin user."
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/download-source-code.md"
---

## Use the `gpadmin` user from now on {#use-the-gpadmin-user-from-now-on}

From here on out we execute commands as the `gpadmin` user:

```bash
sudo su - gpadmin
```

## Clone the Apache Cloudberry repository (2.x branch) {#clone-the-apache-cloudberry-repository-2x-branch}

Clone the release source code for Apache Cloudberry into the `gpadmin` user's home directory:

```bash
git clone https://github.com/apache/cloudberry.git ~/cloudberry
cd ~/cloudberry
git fetch --tags

# For Apache Cloudberry 2.2.0
git checkout tags/2.2.0-incubating

# For Apache Cloudberry 2.1.0
git checkout tags/2.1.0-incubating

# For Apache Cloudberry 2.0.0
git checkout tags/2.0.0-incubating

git submodule update --init --recursive
```

> [!NOTE]
> The command `git submodule update --init --recursive` initializes the submodules that the build depends on. In Apache Cloudberry 2.0 and 2.1, these are only needed for building with PAX support, so you can skip this step if you don't plan to enable PAX. Starting from Apache Cloudberry 2.2, other components are shipped as submodules too, such as `gpcontrib/yezzey` for `--with-yezzey`, so run this command unless you are sure you need none of them.

> [!WARNING]
> In the Ubuntu container, you may encounter the following error when cloning the source code: `error: git-remote-https died of signal 4`.
>
> You can set the following environment variable to avoid this error: `export GNUTLS_CPUID_OVERRIDE=0x1`.

## Download the source code archive {#download-the-source-code-archive}

Alternatively, you can download the source code archive from the [Apache Cloudberry releases page](https://cloudberry.apache.org/releases).

- For Apache Cloudberry 2.2.0

```bash
tar xvzf apache-cloudberry-2.2.0-incubating-src.tar.gz
mv apache-cloudberry-2.2.0-incubating cloudberry
```

- For Apache Cloudberry 2.1.0

```bash
tar xvzf apache-cloudberry-2.1.0-incubating-src.tar.gz
mv apache-cloudberry-2.1.0-incubating cloudberry
```

- For Apache Cloudberry 2.0.0

```bash
tar xvzf apache-cloudberry-2.0.0-incubating-src.tar.gz
mv apache-cloudberry-2.0.0-incubating cloudberry
```

> [!NOTE]
> The submodules are already included in the latest 2.x.0 release source code archive, so you don't need to download the submodules manually after extracting the archive.
