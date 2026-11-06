---
title: "安装所需软件包"
description: "此步骤安装构建 Apache Cloudberry 所需的基本开发工具、库和依赖项。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/install-required-packages.md"
---

## 安装基本系统软件包 {#install-basic-system-packages}

以下命令会安装 Cloudberry 开发所需的全部主要软件包：

{{< tabs >}}
{{< tab label="适用于 Rocky Linux 8+" >}}
```bash
sudo dnf install -y apr-devel \
  bison \
  bzip2-devel \
  curl \
  cmake3 \
  diffutils \
  flex \
  gcc \
  gcc-c++ \
  glibc-langpack-en \
  glibc-locale-source \
  iproute \
  krb5-devel \
  libcurl-devel \
  libevent-devel \
  libxml2-devel \
  libuuid-devel \
  libzstd-devel \
  lz4-devel \
  net-tools \
  openldap-devel \
  openssl-devel \
  openssh-server \
  pam-devel \
  perl \
  perl-ExtUtils-Embed \
  perl-Test-Simple \
  perl-Env \
  python3-devel \
  python3-pip \
  python3-setuptools \
  readline-devel \
  rsync \
  wget \
  which \
  zlib-devel
```

### 启用其他开发工具和库 {#enable-additional-development-tools-and-libraries}

对于 Rocky Linux，还需要安装 `CodeReady Builder (CRB)` 或 `devel` 软件仓库；其中提供其他开发工具和库。

这些仓库在 Rocky Linux 中默认禁用，必须显式启用。

{{< tabs >}}
{{< tab label="适用于 Rocky Linux 8" >}}
- Apache Cloudberry 2.2.0

```bash
sudo dnf install -y --enablerepo=devel liburing-devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel python3-wheel python3-Cython
```

- Apache Cloudberry 2.1.0

```bash
sudo dnf install -y --enablerepo=devel liburing-devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel
```

- Apache Cloudberry 2.0.0

```bash
sudo dnf install -y --enablerepo=devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel
```
{{< /tab >}}
{{< tab label="适用于 Rocky Linux 9" >}}
- Apache Cloudberry 2.2.0

```bash
sudo dnf install -y --enablerepo=crb liburing-devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel python3-wheel python3-Cython
```

- Apache Cloudberry 2.1.0

```bash
sudo dnf install -y --enablerepo=crb liburing-devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel
```

- Apache Cloudberry 2.0.0

```bash
sudo dnf install -y --enablerepo=crb libuv-devel libyaml-devel perl-IPC-Run protobuf-devel
```
{{< /tab >}}
{{< tab label="适用于 Rocky Linux 10" >}}
- Apache Cloudberry 2.2.0

```bash
sudo dnf install -y --enablerepo=crb liburing-devel libuv-devel libyaml-devel perl-IPC-Run protobuf-devel python3-wheel
```
{{< /tab >}}
{{< /tabs >}}

> [!NOTE] 注意
> 在 Red Hat Enterprise Linux（RHEL）中，该软件仓库称为“PowerTools”。

### 为 Rocky Linux 8 安装 gcc 和 gcc-c++ 11+（可选） {#install-gcc-and-gcc-c-11-for-rocky-linux-8-optional}

> [!TIP] 提示
> 只有构建 Apache Cloudberry 2.0.0 时才需要此步骤。构建 Apache Cloudberry 2.1.0+ 时可以跳过。

在 Rocky Linux 8 上，需要安装较高版本的 gcc 和 gcc-c++，才能构建带 PAX 支持的 Apache Cloudberry 2.0.0：

```bash
sudo yum install -y gcc-toolset-11-gcc gcc-toolset-11-gcc-c++
scl enable gcc-toolset-11 bash # for temprory use
sudo echo "source /opt/rh/gcc-toolset-11/enable" >> /etc/profile.d/gcc.sh
sudo source /etc/profile.d/gcc.sh #  for permanent use
```

可以运行以下命令验证 gcc 和 gcc-c++ 11+ 的版本：

```bash
gcc --version
g++ --version
```

### 为 ORCA 安装 Apache Xerces-C {#install-apache-xerces-c-for-orca}

Apache Xerces-C 是在 Cloudberry 中启用 Orca 查询优化器所需的依赖项。以下步骤会下载源码、验证完整性、构建库并安装。

1. 设置变量（辅助变量）

    为简化命令并便于复用，定义以下辅助变量：

    ```bash
    XERCES_LATEST_RELEASE=3.3.0
    XERCES_INSTALL_PREFIX="/usr/local/xerces-c"
    ```

> [!NOTE] 注意
> 这些变量在整个构建过程中指定要安装的 Apache Xerces-C 版本（XERCES_LATEST_RELEASE）和安装目录（XERCES_INSTALL_PREFIX），以保持设置一致并简化命令。

2. 下载并验证源码包

    ```bash
    wget -nv "https://dlcdn.apache.org//xerces/c/3/sources/xerces-c-${XERCES_LATEST_RELEASE}.tar.gz"
    echo "$(curl -sL https://dlcdn.apache.org//xerces/c/3/sources/xerces-c-${XERCES_LATEST_RELEASE}.tar.gz.sha256)" | sha256sum -c -
    ```

> [!NOTE] 注意
> 确保 SHA-256 校验和验证通过（输出：`xerces-c-3.3.0.tar.gz: OK`）。如果验证失败，请停止操作，检查源码包的完整性。

3. 解压、配置、构建、测试并安装

    ```bash
    tar xf "xerces-c-${XERCES_LATEST_RELEASE}.tar.gz"
    rm "xerces-c-${XERCES_LATEST_RELEASE}.tar.gz"
    cd xerces-c-${XERCES_LATEST_RELEASE}

    ./configure --prefix="${XERCES_INSTALL_PREFIX}-${XERCES_LATEST_RELEASE}" | tee configure-$(date "+%Y.%m.%d-%H.%M.%S").log
    make -j$(nproc) | tee make-$(date "+%Y.%m.%d-%H.%M.%S").log
    make check | tee make-check-$(date "+%Y.%m.%d-%H.%M.%S").log
    sudo make install | tee make-install-$(date "+%Y.%m.%d-%H.%M.%S").log
    sudo ln -s ${XERCES_INSTALL_PREFIX}-${XERCES_LATEST_RELEASE} ${XERCES_INSTALL_PREFIX}
    ```

> [!NOTE] 注意
> - `make` 命令以并行方式运行（`-j$(nproc)`），利用所有可用的 CPU 核心来加快构建。`nproc` 命令会动态获取核心数。
> - 在 `make check` 期间，列为 **XFAIL**（预期失败）的失败项可以接受，并不表示构建有问题。
> - 命令输出会保存到带时间戳的日志文件中，便于日后参考或排查问题。
{{< /tab >}}
{{< tab label="适用于 Ubuntu 22.04+" >}}
Ubuntu 用户：

- Ubuntu 20.04+ 中的 gcc 和 g++ 版本足以构建 Apache Cloudberry。
- 我们将使用 Ubuntu 软件仓库提供的默认 `libxerces-c` 版本，该版本与 Apache Cloudberry 兼容。

```bash
sudo apt install -y bison \
  bzip2 \
  cmake \
  curl \
  flex \
  gcc \
  g++ \
  iproute2 \
  iputils-ping \
  language-pack-en \
  locales \
  libapr1-dev \
  libbz2-dev \
  libcurl4-gnutls-dev \
  libevent-dev \
  libkrb5-dev \
  libipc-run-perl \
  libldap2-dev \
  libpam0g-dev \
  libprotobuf-dev \
  libreadline-dev \
  libssl-dev \
  libuv1-dev \
  liblz4-dev \
  libxerces-c-dev \
  libxml2-dev \
  libyaml-dev \
  libzstd-dev \
  libperl-dev \
  make \
  pkg-config \
  protobuf-compiler \
  python3-dev \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  rsync
```

### 构建 PAX 的额外依赖项（可选） {#extra-dependencies-for-building-pax-optional}

> [!TIP] 提示
> 仅 Apache Cloudberry 2.1.0+ 需要此步骤。构建 Apache Cloudberry 2.0.0 时可以跳过。

在 Apache Cloudberry 2.1.0+ 中，我们引入了构建 PAX 所需的新依赖项 `liburing`。

* 对于 Ubuntu 22.04/24.04

```bash
sudo apt install -y liburing-dev
```

* 对于 Ubuntu 20.04（Apache Cloudberry 2.1）

```bash
sudo apt install -y git build-essential
wget https://github.com/axboe/liburing/archive/refs/tags/liburing-2.1.tar.gz
tar -xzf liburing-2.1.tar.gz
rm "liburing-2.1.tar.gz"
cd liburing-liburing-2.1
make -j$(nproc)
sudo make install
sudo ldconfig
```
{{< /tab >}}
{{< /tabs >}}
