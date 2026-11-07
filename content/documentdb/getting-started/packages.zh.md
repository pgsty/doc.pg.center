---
title: Linux 软件包快速入门
description: 使用 Ubuntu APT 或 EL9 RPM/dnf 包在 Linux 上安装 DocumentDB，设置私有 PostgreSQL 实例，并运行你的第一个查询。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 30
translation_source_sha256: 190cfa7bc91b29eeb0b037b37ae4c342830c2c9adfab8fe7139cf18855a68366
translation_review: AI-assisted bilingual review; 2026-11-07
---

从官方发布的软件包仓库安装 DocumentDB，在自己的主机上获得兼容 MongoDB 的端点。

当前正式版为 **Ubuntu 24.04 和 EL9、PostgreSQL 17 或 18、amd64 或 arm64** 提供全套组件，包括扩展、网关、配置向导和 systemd 单元。EL9 包括 Rocky Linux、AlmaLinux、CentOS Stream，以及已注册的 Red Hat Enterprise Linux；[Linux 软件包安装](https://documentdb.io/packages?method=packages)页面提供各发行版所需的依赖准备命令。从 v0.116 起，官方有意缩小了预编译软件包的支持范围。网站仓库只镜像当前版本的发布文件，不会沿用旧版软件包来造成其他目标平台也获得当前版本支持的假象。

**推荐做法：** 安装全套组件，然后创建一个新的私有 PostgreSQL 18 实例。命令会检测执行它们的 Linux 主机架构。若要使用容器，或在 macOS/Windows 上试用，请选择 [Docker 安装](https://documentdb.io/packages?method=docker)。

> [!IMPORTANT]
> 如果已经通过软件包运行 v0.116 或 v0.117，请按[升级指南](/documentdb/linux-packages/#upgrading)操作，不要重新安装。运行过 1.0 发布候选版的主机没有受支持的升级路径，请改用全新主机。卸载软件包会保留数据库文件，重新安装也不会重置数据。

> [!NOTE]
> 需要其他发行版或 PostgreSQL 主版本？欢迎社区自行构建。检出 `v1.0-0` 标签，传入 `--version 1.0.0`，使用支持版本参数的[打包脚本](https://github.com/documentdb/documentdb/blob/v1.0-0/packaging/README.md)。`build_packages.sh` 构建扩展，`gateway/build_gateway_packages.sh` 构建网关，`build_extra_packages.sh` 构建公共组件、工具、独立部署组件和元软件包。PostgreSQL 15 仅支持扩展，因为配置工具要求 PostgreSQL 16 或更新版本。这些按需构建的产物不属于 documentdb.io 托管的正式发布文件。

无需预先安装 PostgreSQL，配置向导会创建并管理自己的实例。不过，安装过程会添加 PGDG 仓库，并安装 PostgreSQL、PostGIS 等约 160 个软件包（约 140 MB），因此请选用允许配置 PGDG 仓库的主机。

## 全新主机的安装程序 {#clean-host-installer}

在全新安装的 Ubuntu 24.04 或 EL9 主机上，下载并运行安装程序：

```sh
curl -fsSLo documentdb-install.sh https://documentdb.io/install.sh &&
sudo sh documentdb-install.sh
```

此操作会从软件包仓库安装当前版本（v1.0-0），使用 PostgreSQL 18；要使用 PostgreSQL 17，请添加 `--pg-major 17`。
如果主机已配置 DocumentDB，安装程序只会报告状态，不会执行升级。要将现有安装升级到 1.0，请按[升级指南](/documentdb/linux-packages/#upgrading)操作。

## 安装 {#install}

<span id="ubuntu-24-04-postgre-sql-18-apt"></span>

### Ubuntu 24.04，PostgreSQL 18（APT） {#ubuntu-2404-postgresql-18-apt}

```bash
sudo apt update && \
sudo apt install -y curl ca-certificates gnupg && \
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor --yes -o /usr/share/keyrings/postgresql.gpg && \
echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] https://apt.postgresql.org/pub/repos/apt noble-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list >/dev/null && \
curl -fsSL https://documentdb.io/documentdb-archive-keyring.gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/documentdb-archive-keyring.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/documentdb-archive-keyring.gpg] https://documentdb.io/deb stable ubuntu24" | sudo tee /etc/apt/sources.list.d/documentdb.list >/dev/null && \
sudo apt update && \
sudo apt install -y documentdb-18
```

<span id="rocky-linux-alma-linux-or-cent-os-stream-9-postgre-sql-18-rpm"></span>

### Rocky Linux、AlmaLinux 或 CentOS Stream 9，PostgreSQL 18（RPM） {#rocky-linux-almalinux-or-centos-stream-9-postgresql-18-rpm}

```bash
if (. /etc/os-release && [ "$ID" = centos ]) && [ -f /etc/yum.repos.d/pgdg-redhat-all.repo ]; then sudo sed -i 's/rhel-\$releasever_major\.\$releasever_minor-/rhel-$releasever_major-/g' /etc/yum.repos.d/pgdg-redhat-all.repo; fi && \
sudo dnf install -y dnf-plugins-core && \
sudo dnf config-manager --set-enabled crb && \
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm && \
if (. /etc/os-release && [ "$ID" = centos ]) && [ -f /etc/yum.repos.d/pgdg-redhat-all.repo ]; then sudo sed -i 's/rhel-\$releasever_major\.\$releasever_minor-/rhel-$releasever_major-/g' /etc/yum.repos.d/pgdg-redhat-all.repo; fi && \
sudo dnf -qy module disable postgresql && \
sudo rpm --import https://documentdb.io/documentdb-archive-keyring.gpg && \
printf '%s\n' \
  '[documentdb]' \
  'name=DocumentDB Repository' \
  'baseurl=https://documentdb.io/rpm/rhel9' \
  'enabled=1' \
  'gpgcheck=1' \
  'gpgkey=https://documentdb.io/documentdb-archive-keyring.gpg' | sudo tee /etc/yum.repos.d/documentdb.repo >/dev/null && \
sudo dnf install -y documentdb-18
```

<span id="registered-red-hat-enterprise-linux-9-postgre-sql-18-rpm"></span>

### 已注册的 Red Hat Enterprise Linux 9，PostgreSQL 18（RPM） {#registered-red-hat-enterprise-linux-9-postgresql-18-rpm}

此命令需要有效的 Red Hat 订阅。RHEL 通过 `subscription-manager` 提供 CodeReady Builder，而不是使用 Rocky 系列系统的 `crb` 仓库 ID。

```bash
sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(uname -m)-rpms && \
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm && \
sudo dnf -qy module disable postgresql && \
sudo rpm --import https://documentdb.io/documentdb-archive-keyring.gpg && \
printf '%s\n' \
  '[documentdb]' \
  'name=DocumentDB Repository' \
  'baseurl=https://documentdb.io/rpm/rhel9' \
  'enabled=1' \
  'gpgcheck=1' \
  'gpgkey=https://documentdb.io/documentdb-archive-keyring.gpg' | sudo tee /etc/yum.repos.d/documentdb.repo >/dev/null && \
sudo dnf install -y documentdb-18
```

要使用 PostgreSQL 17，请在 [Linux 软件包安装](https://documentdb.io/packages?method=packages)页面中选择相应版本，生成 `documentdb-17` 对应的安装和配置命令；没有 `documentdb-16` 软件包。两种 EL9 流程都会启用 CodeReady Builder，由它提供 PostGIS 依赖的 `libqhull_r.so.7`。

然后安装 `mongosh`，用于连接端点：

```bash
# Ubuntu 24.04
curl -fsSL https://pgp.mongodb.com/server-8.0.asc | sudo gpg --dearmor --yes -o /usr/share/keyrings/mongodb.gpg
echo "deb [signed-by=/usr/share/keyrings/mongodb.gpg] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt update && sudo apt install -y mongodb-mongosh

# EL9
printf '[mongodb-org-8.0]\nname=MongoDB\nbaseurl=https://repo.mongodb.org/yum/redhat/9/mongodb-org/8.0/$basearch/\ngpgcheck=1\nenabled=1\ngpgkey=https://pgp.mongodb.com/server-8.0.asc\n' | sudo tee /etc/yum.repos.d/mongodb.repo
sudo dnf install -y mongodb-mongosh
```

## 配置并连接 {#set-up-and-connect}

> [!IMPORTANT]
> 向导使用自签名证书，并将网关绑定到**所有网络接口**（`0.0.0.0:10260`）。在私人机器以外的环境中运行向导前，请先用防火墙限制对端口 `10260` 的访问，然后阅读[向网络开放服务之前](/documentdb/linux-packages/#before-exposing-it-to-a-network)。

安装软件包只是将文件放到磁盘上，并不会创建数据库或启动端点。这些工作由配置向导完成：

```bash
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

向导会创建一个新的私有 PostgreSQL 18 实例，安装扩展，启动网关，并设置为开机启动。它会**提示输入管理员密码**。显式指定主版本和新建实例选项，可以避免误选其他已安装的 PostgreSQL 主版本或现有系统集群。

示例数据需要主动启用。在配置命令中添加 `--load-sample-data`，即可向 `StoreData` 数据库加载示例数据，其中 `stores` 集合有 41,505 个文档，`ratings` 集合有 2 个文档。此操作需要 `mongosh`；前面的命令创建的是空实例。

自动化部署请使用完整的[无人值守配置](/documentdb/linux-packages/#unattended-setup)命令。若要使用本机上已经由你管理的 PostgreSQL，请按[接管现有 PostgreSQL 实例](/documentdb/linux-packages/#adopt-an-existing-postgre-sql-instance)操作；这会修改配置，可能需要管理员安排重启。如果只通过 SQL 使用，无需网关，请参见[仅安装 PostgreSQL 扩展](/documentdb/linux-packages/#install-the-postgre-sql-extension-only)。

现在用 shell 连接端点。在密码提示处输入配置时设置的管理员密码。跳过自签名证书验证的做法**仅适用于本地开发**；通过网络访问时应使用受信任的证书。

```bash
mongosh localhost:10260 -u admin -p --authenticationMechanism SCRAM-SHA-256 \
        --tls --tlsAllowInvalidCertificates
```

首次写入时将创建数据库和集合：

```javascript
> use quickstart
> db.orders.insertOne({ item: "widget", qty: 5 })
{ acknowledged: true, insertedId: ObjectId('...') }

> db.orders.find()
[ { _id: ObjectId('...'), item: 'widget', qty: 5 } ]
```

**至此，DocumentDB 已可正常使用。** 通过 `sudo documentdb-setup --status` 确认服务状态，通过 `documentdb-gateway --version` 确认版本。

## 接下来该做什么 {#where-to-go-next}

- 开发应用：[Node.js 快速入门](/documentdb/getting-started/nodejs-setup/)或 [Python 快速入门](/documentdb/getting-started/python-setup/)
- 安全配置、服务管理、执行 SQL、升级、卸载，以及在没有 systemd 的主机上运行：[软件包安装的运维](/documentdb/linux-packages/)
- 无互联网连接时安装：[离线或隔离环境安装](/documentdb/linux-packages/offline/)
- 选择已发布的发行版、架构和 PostgreSQL 主版本：[Linux 软件包安装](https://documentdb.io/packages?method=packages)

## 故障排除 {#troubleshooting}

- `Unable to locate package documentdb-18` (apt) / `No match for argument: documentdb-18` (dnf) — 未添加 DocumentDB 存储库，或主机不在当前发行版矩阵中。请检查 [Linux 软件包安装](https://documentdb.io/packages?method=packages)
- `documentdb-18 : Depends: postgresql-18 but it is not installable` — 未先添加 PGDG
- `nothing provides libqhull_r.so.7` — 为所选 EL9 系列未启用 CRB 或 CodeReady Builder
- `MongoServerError: Invalid key` — 密码为空或错误；仅输入 `-p` 会提示输入，因此非交互式 shell 会发送空内容
- 其他任何情况 — `sudo documentdb-setup --status` 会报告监听器状态、服务状态和已解析路径

更多故障情况（包括没有 systemd 的主机）见[软件包安装的运维](/documentdb/linux-packages/#troubleshooting)。

## 使用过旧版仓库目标平台时 {#if-you-used-an-earlier-repository-target}

documentdb.io 不再为 Ubuntu 22.04、Debian 11/12/13、RHEL 8 兼容发行版或 PostgreSQL 16 发布软件包。现有安装仍可运行，但不会收到软件包更新，也无法再从 documentdb.io 重新安装这些软件包。

已停用的仓库 URL 仍保留带签名的空元数据，使 `apt update` 和 `dnf makecache` 可以继续正常执行。对于不准备迁移到当前支持平台的主机，请移除相应软件源：

```bash
# Debian / Ubuntu
sudo rm -f /etc/apt/sources.list.d/documentdb.list
sudo apt update

# RHEL-compatible
sudo rm -f /etc/yum.repos.d/documentdb.repo
sudo dnf clean all
```

若要继续使用旧目标平台，请使用对应 GitHub 发布版的文件，或从匹配的源码标签自行构建。这两种方式都不属于当前托管仓库的支持范围。
