---
title: 安装
weight: 1150
description: 从预构建二进制文件或源码安装 etcd 的步骤
icon: fa-solid fa-download
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/install.md"
---

## 先决条件 {#requirements}

安装 etcd 之前，请参阅以下页面：

- [支持的平台][]
- [硬件建议][]

## 安装预构建二进制文件 {#install-pre-built-binaries}

安装 etcd 最简便的方式是使用预构建的二进制文件：

1. 从 [Releases][] 下载适用于当前平台的压缩归档文件，选择 [v3.7.0][tagged-release] 或更高版本。
2. 解压归档文件。解压后会生成一个包含二进制文件的目录。
3. 将可执行二进制文件添加到 PATH。例如，可将二进制文件重命名或移动到 PATH 中的目录（如 `/usr/local/bin`），也可将上一步创建的目录添加到 PATH。
4. 在 shell 中验证 `etcd` 是否位于 PATH 中：

    ```sh
    $ etcd --version
    etcd Version: 3.7.0
    ...
    ```

## 从源码构建 {#build-from-source}

如果已安装 [Go 版本 1.21+][go]，可按以下步骤从源码构建 etcd：

1. [下载 etcd 仓库的 zip 文件][download] 并解压，或使用以下命令克隆仓库。

    ```sh
    $ git clone -b v3.7.0 https://github.com/etcd-io/etcd.git
    ```
    如需从 `main@HEAD` 构建，请省略 `-b v3.7.0` 标志。

2. 切换目录：

    ```sh
    $ cd etcd
    ```
3. 运行构建脚本：

    ```sh
    $ ./scripts/build.sh
    ```

    二进制文件位于 `bin` 目录下。

4. 将 `bin` 目录的完整路径添加到 PATH 环境变量中，例如：

    ```sh
    $ export PATH="$PATH:`pwd`/bin"
    ```

5. 验证 `etcd` 是否位于 PATH 中：

    ```sh
    $ etcd --version
    ```

## 通过操作系统包安装 {#installation-via-os-packages}
请注意：通过操作系统包管理器安装的 etcd 可能会提供过时版本，因为这些版本不会被 etcd 项目自动维护或官方支持。因此，使用操作系统包时应格外谨慎。

在不同操作系统上安装 etcd 有多种方式，以下仅列举部分示例说明如何操作。

### macOS (Homebrew) {#macos-homebrew}

1. 更新 homebrew：
```sh
$ brew update
```

2. 安装 etcd：
```sh
$ brew install etcd
```

3. 验证安装
```sh
$ etcd --version
```

## Linux {#linux}

尽管可通过多数主流 Linux 发行版的官方软件仓库和包管理器安装 etcd，但发布的版本可能严重过时。因此，强烈不建议采用此方式安装。

在 Linux 上安装 etcd 的推荐方式是通过 [预构建二进制文件](#install-pre-built-binaries)，或使用 Homebrew。

### Linux 上的 Homebrew {#homebrew-on-linux}

Homebrew 可在 Linux 上运行，并可提供较新的软件版本。

- 先决条件
  - 更新 Homebrew：

    ```sh
    $ brew update
    ```

- 操作步骤
  - 使用 `brew` 安装：

    ```sh
    $ brew install etcd
    ```

- 结果
  - 通过获取版本信息验证安装：

    ```sh
    $ etcd --version
    etcd Version: 3.7.0
    ...
    ```

## Docker {#docker}

etcd 使用 [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) 作为主容器注册表，使用 [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) 作为辅助注册表。

使用 Docker 运行 etcd：

```sh
ETCD_VER=v3.7.0

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

## Kubernetes 安装的一部分 {#installation-as-part-of-kubernetes-installation}

- [以 Kubernetes StatefulSet 形式运行 etcd][]

## 安装检查 {#installation-check}

若需对安装进行稍复杂的完整性检查，请参阅[快速入门][]。

[download]: https://github.com/etcd-io/etcd/archive/v3.7.0.zip
[go]: https://golang.org/doc/install
[Hardware recommendations]: /zh/etcd/op-guide/hardware/
[Quickstart]: /zh/etcd/quickstart/
[Running etcd as a Kubernetes StatefulSet]: /zh/etcd/op-guide/kubernetes/
[releases]: https://github.com/etcd-io/etcd/releases/
[tagged-release]: https://github.com/etcd-io/etcd/releases/tag/v3.7.0
[Supported platforms]: /zh/etcd/op-guide/supported-platform/
[Homebrew can run on Linux]: <https://docs.brew.sh/Homebrew-on-Linux>
