---
title: 预编译软件包
description: 通过设置向导安装完整的 DocumentDB 堆栈，或选择单独的 PostgreSQL 和网关包。包含 PGDG 和源码构建选项。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/docs/blob/cf69384e6da9524cc0fc723e8ac5b6c0689af432/getting-started/prebuilt-packages.md
source_status: superseded
weight: 1070
translation_source_sha256: e49364fafe53e333ae16df1b264fa4ced71f621f440398964698ea907116a010
translation_review: AI-assisted bilingual review; 2026-11-07
---

> [!NOTE] 已被上游版本取代
> 官方网站现已将此页面重定向至[当前指南](/documentdb/getting-started/packages/)。源文档在此保留以供现有链接使用。

安装完整的 MongoDB 兼容服务，或仅将所需组件添加到你管理的 PostgreSQL 实例中。自 v0.116 起，DocumentDB 的软件包包含设置向导、管理员工具和 systemd 集成。

从 [documentdb.io](https://documentdb.io/packages) 获取官方软件包，从 [PGDG](#pgdg-extension-packages) 获取扩展软件包，或使用提供的脚本为其他目标[构建软件包](#community-builds)。

## 选择安装路径 {#choose-an-installation-path}

| 你的需求 | 安装方式 |
| --- | --- |
| 一个设置最少的可运行 DocumentDB 实例 | **[独立堆栈](#set-up-and-connect)，推荐**：安装 `documentdb` 并运行向导。 |
| 通过 MongoDB 兼容接口访问你管理的 PostgreSQL 实例 | [扩展 + 网关](#add-a-gateway)：分别配置各组件，并保留你原有的 PostgreSQL 服务生命周期。 |
| 通过 SQL 访问 DocumentDB，无需网关 | [仅扩展](#extension-only-installation)：安装扩展及可选的管理员工具。 |

## 官方软件包 {#first-party-packages}

当前版本为 [`v1.0-0`](https://github.com/documentdb/documentdb/releases/tag/v1.0-0)，发布于 **2026-10-19**。请参阅 [1.0 版本发布说明](/documentdb/getting-started/release-notes-1.0/) 了解变更内容和已知问题。官方 CI 构建并测试了以下完整堆栈：

| 发行版 | PostgreSQL | 架构 |
| --- | --- | --- |
| Ubuntu 24.04 (DEB) | 17, 18 | amd64, arm64 |
| RHEL 兼容 9 (RPM) | 17, 18 | x86_64, aarch64 |

默认推荐 Ubuntu 24.04 搭配 PostgreSQL 18。其他目标平台可能可以通过 PGDG 或构建脚本获得支持；它们不属于此托管支持范围。

对于干净的主机，安装程序会配置仓库、安装软件包，并运行设置：

```sh
curl -fsSLo documentdb-install.sh https://documentdb.io/install.sh &&
sudo sh documentdb-install.sh
```

此操作将在 PostgreSQL 18 上安装当前版本。请使用 `--pg-major 17` 安装 PostgreSQL 17。使用 `sudo` 运行：以普通用户身份启动时，会调用 `sudo -v`，即使在默认用户无需密码 sudo 的云镜像上也会提示输入密码。

安装程序会要求确认计划并选择管理员密码。要无人值守运行，请将密码保存在 root 拥有的文件中，并传入 `--yes` 选项：

```sh
printf 'DocumentDB admin password: '; IFS= read -r -s PW; echo
printf '%s\n' "$PW" | sudo install -m 600 /dev/stdin /root/documentdb-admin.pw
sudo sh documentdb-install.sh --yes \
  --admin-password-file /root/documentdb-admin.pw --accept-external-listen
```

`--accept-external-listen` 确认网关默认监听所有接口。
手动步骤安装的是相同版本。若需迁移现有安装至 1.0 版本，请参阅[升级至 1.0](#upgrading-to-10)。

## 设置并连接 {#set-up-and-connect}

这些步骤适用于**全新独立安装**。对于现有部署，请先阅读[升级至 1.0](#upgrading-to-10)。

### 1. 安装堆栈 {#1-install-the-stack}

使用 [软件包查找器](https://documentdb.io/packages) 或 [Linux 软件包快速入门](/documentdb/getting-started/packages/) 配置你发行版和架构的仓库。官方软件包依赖于 PostgreSQL 及 PGDG 提供的扩展；EL9 还需要 EPEL 和 CRB / CodeReady Builder。

仓库配置完成后，在 Ubuntu 上安装堆栈：

```bash
sudo apt install documentdb
```

在 EL9 上，请使用 `sudo dnf install documentdb`。`documentdb`（PG18 默认）和 `documentdb-18`（由软件包查找器使用）均安装完整堆栈。

### 2. 运行设置向导 {#2-run-the-setup-wizard}

> 网关默认监听所有接口。在可网络访问的主机上设置前，请限制对端口 `10260` 的访问；允许远程客户端前请使用受信任的证书。

```bash
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

向导会提示输入管理员密码，创建私有的 PostgreSQL 18 实例，配置扩展和管理员用户，并启动网关。在使用 systemd 的主机上，还会将整个服务栈设置为开机自启。

### 3. 连接 {#3-connect}

需单独安装 [mongosh](https://www.mongodb.com/docs/mongodb-shell/install/)，然后进行交互式连接：

```bash
mongosh localhost:10260 --authenticationMechanism SCRAM-SHA-256 \
  --tls --tlsAllowInvalidCertificates -u admin -p
```

输入向导中设置的密码，然后运行：

```javascript
db.runCommand({ ping: 1 })
```

本地示例接受生成的自签名证书。仅使用 `-p` 时会提示输入密码；非交互式脚本必须显式提供密码。`db.version()` 报告的是 DocumentDB 兼容的 MongoDB 版本，而非 DocumentDB 版本；请参阅[检查版本](#check-the-version)。

### 可选设置控制 {#optional-setup-controls}

| 要求 | 方法 |
| --- | --- |
| 使用 PostgreSQL 17 | 安装 `documentdb-17` 而非 `documentdb`，并使用 `--pg-version 17`。 |
| 预览更改 | 在应用设置前添加 `--dry-run`。 |
| 更改网关端口 | 添加 `--listen-port 27017`，或另一个未使用的端口。 |
| 加载示例数据 | 添加 `--load-sample-data` 以加载 [StoreData](/documentdb/documentdb-local/#built-in-sample-data)；需 `mongosh`。 |
| 自动化设置 | 使用 `--yes` 配合 `--admin-password-file /path/to/protected-file`（模式 `0600`）或 `--admin-password-stdin`。 |
| 采用现有本地 PostgreSQL 实例 | 将 `--use-new-postgres-instance` 替换为 `--target-postgres-instance 18/main`；审查建议的更改并计划 PostgreSQL 重启。 |

使用 `sudo documentdb-setup --pg-version 18 --status` 检查状态。在 systemd 上，使用 `sudo systemctl restart documentdb-local@18.target` 重启此堆栈；已采用的 PostgreSQL 保留其自身生命周期。有关 TLS 及其他操作指导，请参阅[操作包安装](/documentdb/linux-packages/)。

### 删除堆栈 {#remove-the-stack}

先删除实例，再卸载软件包。`documentdb-local-reset` 随 `documentdb-common` 软件包提供，因此必须在清除软件包之前运行；仅清除软件包会保留数据目录。

```bash
sudo documentdb-local-reset --pg-version 18 --confirm-destroy
sudo apt purge -y '*documentdb*'      # Ubuntu
sudo dnf remove -y '*documentdb*'     # EL9
```

重置操作不可逆，且只适用于独立服务栈的私有实例，不包括接管的 PostgreSQL 实例。尚未解决的卸载和清除问题记录在 [#771](https://github.com/documentdb/documentdb/issues/771)。

## 每个版本发布的内容 {#what-each-release-publishes}

`N` 是 PostgreSQL 主版本。包管理器会安装你所选软件包的依赖项。

| 包 | 用途 |
| --- | --- |
| `documentdb` | 方便的元包，选择 `documentdb-18`；同时提供 `documentdb-local.target` 别名。 |
| `documentdb-N` | 适用于 PostgreSQL 主版本 N 的完整独立服务栈；负责管理自身的 systemd 生命周期。 |
| `postgresql-N-documentdb` (DEB) / `postgresqlN-documentdb` (RPM) | 仅包含扩展库和 SQL 文件；不配置现有的 PostgreSQL 实例。 |
| `documentdb-postgresql-tools` | `documentdb-tune`、`documentdb-createcluster`、`documentdb-register-gateway` 和 `documentdb-gateway-admin`。 |
| `documentdb-gateway` | MongoDB 线协议运行时及其服务；不配置 PostgreSQL。 |
| `documentdb-common` | 共享向导、服务模板、辅助工具和示例数据，由 `documentdb-N` 引入。 |

## 仅扩展安装 {#extension-only-installation}

此 **替代方案** 在 Ubuntu 24.04 上使用官方包，并由管理员管理名为 `main` 的 PostgreSQL 18 集群。仅安装扩展和工具，不安装 `documentdb` 或 `documentdb-N`：

```bash
sudo apt install postgresql-18-documentdb documentdb-postgresql-tools
sudo documentdb-tune --pg-version 18 --cluster main --dry-run
```

审查建议的配置，然后在合适的重启窗口中应用：

```bash
sudo documentdb-tune --pg-version 18 --cluster main --yes &&
sudo systemctl restart postgresql@18-main &&
sudo -u postgres /usr/bin/psql --cluster 18/main -d postgres -v ON_ERROR_STOP=1 \
  -c "CREATE EXTENSION IF NOT EXISTS documentdb CASCADE;" \
  -c "CREATE EXTENSION IF NOT EXISTS documentdb_extended_rum CASCADE;"
```

重启后必须执行两条扩展语句；`CASCADE` 不会创建 `documentdb_extended_rum`。根据你的实例调整主版本号和集群名称。对于其他布局，请遵循 `documentdb-tune` 输出的重启和连接命令。

对于 **新** 的 Debian/Ubuntu 集群，`sudo documentdb-createcluster 18 docdb --start` 结合了集群创建、调优、启动和扩展创建。选择一个尚未存在的集群名称。

### 添加网关 {#add-a-gateway}

在完成仅扩展步骤后，安装并注册一个网关。将管理员密码存储在受保护的文件中（模式 `0600`），并在下面替换其路径：

```bash
sudo apt install documentdb-gateway
sudo documentdb-register-gateway --target-postgres-instance 18/main \
  --admin-user admin --admin-password-file /path/to/admin-password --yes
sudo systemctl reload postgresql@18-main
sudo systemctl enable --now documentdb-gateway
```

注册配置了认证和管理员用户。使用与上述相同的 `mongosh` 连接。此路径使用 `documentdb-gateway.service`，而非独立目标，并要求 PostgreSQL 位于 **同一主机** 上；包管理注册不支持远程 TCP/密码后端。

## PGDG 扩展包 {#pgdg-extension-packages}

DocumentDB 也包含在 **PostgreSQL 全球开发组 (PGDG) APT 仓库** 中，由 Debian PostgreSQL 团队维护。这是一个仅扩展的分发版本：不包含官方网关、设置向导或管理员工具。

例如，截至 **2026-09-10**，PGDG 为 Debian 13（`trixie-pgdg`）、PostgreSQL **15-18**，在 **amd64 和 arm64** 上发布 DocumentDB **0.116**。版本和目标与官方发布不同；请查阅 [PGDG 包池](https://apt.postgresql.org/pub/repos/apt/pool/main/d/documentdb/)。

对于新的 Debian 13 安装，请遵循 [PGDG 仓库设置说明](https://www.postgresql.org/download/linux/debian/#apt)，然后检查你所选 PostgreSQL 主版本的候选包：

```bash
sudo apt update
apt-cache policy postgresql-16-documentdb
```

如果 PGDG 提供了你主机的候选包，请安装它：

```bash
sudo apt install postgresql-16-documentdb
```

单独配置 PostgreSQL 并为该打包版本创建扩展；上述官方辅助命令不适用。不要使用其他发行版的仓库获取缺失的包，或将供应商切换视为就地升级。

## 社区构建 {#community-builds}

你的目标没有可用包？提供的脚本使用 Docker 构建 DEB 或 RPM 包；选择发行版和 PostgreSQL 主版本，而非自行编写打包文件。

使用与目标架构相同的 Linux 构建环境，并准备 Git、Docker、Bash 4+ 和 GNU 工具。例如，为 Debian 12 和 PostgreSQL 18 构建扩展：

```bash
git clone --depth 1 --branch v1.0-0 https://github.com/documentdb/documentdb.git
cd documentdb
./packaging/build_packages.sh --os deb12 --pg 18 --version 1.0.0 --output-dir packages
```

显式传递 `--version 1.0.0`。`v1.0-0` 标签与 `v1.0-RC2` 共享其提交；若无 `--version`，构建将从 `git describe` 选取的标签中获取版本，该版本可以是发布候选版。

对于完整的独立 DEB 集合，需在构建主机上提供 `dpkg-deb`，然后构建网关和共享包：

```bash
./packaging/gateway/build_gateway_packages.sh --os deb12 --pg 18 \
  --version 1.0.0 --output-dir packages
./packaging/build_extra_packages.sh --type deb --pg 18 \
  --version 1.0.0 --output-dir packages
```

输出位于 `packages/`。RPM 额外组件则需要主机 `rpmbuild` 和适用的 RPM 宏。[版本化打包指南](https://github.com/documentdb/documentdb/blob/v1.0-0/packaging/README.md) 列出了目标、前提条件和干净安装检查项。

在你的环境中验证超出官方 CI 矩阵的目标构建。PostgreSQL 15 仅支持扩展；包管理网关设置需要 PostgreSQL 16 或更高版本。

## 下载并验证 {#download-and-verify}

当你需要确切的官方版本而非仓库安装时，请使用发布资产。每个发布都会发布其 Linux 软件包，包含 `SHA256SUMS` 和 `manifest.txt`。

```bash
gh release download v1.0-0 -R documentdb/documentdb -D pkgs && cd pkgs && sha256sum -c SHA256SUMS
```

这将下载所有格式、架构和 PostgreSQL 主版本。仅安装下方匹配的子集，不要安装每个下载的文件。

## 从下载的资产安装 {#install-from-downloaded-assets}

首先启用依赖仓库：PGDG，以及在 EL9 上的 EPEL 和 CRB / CodeReady Builder。将匹配的本地文件传递给 **一个** `apt` 或 `dnf` 命令，以确保依赖在同一次事务中解析。

这些示例安装 `documentdb-18` 及其依赖项；可选的 `documentdb` 元包无需使用。

<span id="deb-ubuntu-24-04-postgre-sql-18-amd64"></span>

### DEB（Ubuntu 24.04，PostgreSQL 18，amd64） {#deb-ubuntu-2404-postgresql-18-amd64}

对于 arm64，请将 `amd64` 替换为 `arm64`。仅网关和扩展文件是架构相关的。

```bash
sudo apt install ./ubuntu24.04-documentdb-18_1.0.0_all.deb \
                 ./ubuntu24.04-documentdb-common_1.0.0_all.deb \
                 ./ubuntu24.04-documentdb-postgresql-tools_1.0.0_all.deb \
                 ./ubuntu24.04-documentdb-gateway_1.0.0_amd64.deb \
                 ./ubuntu24.04-postgresql-18-documentdb_1.0-0_amd64.deb
```

<span id="rpm-rhel-compatible-9-postgre-sql-18-x86-64"></span>

### RPM（RHEL 兼容 9，PostgreSQL 18，x86_64） {#rpm-rhel-compatible-9-postgresql-18-x86_64}

对于 arm64，请将 `x86_64` 替换为 `aarch64`；保持 `noarch` 文件不变。

```bash
sudo dnf install ./documentdb-18-1.0.0-1.noarch.rpm \
                 ./documentdb-common-1.0.0-1.noarch.rpm \
                 ./documentdb-postgresql-tools-1.0.0-1.noarch.rpm \
                 ./documentdb-gateway-1.0.0-1.el9.x86_64.rpm \
                 ./rhel9-postgresql18-documentdb-1.0.0-1.el9.x86_64.rpm
```

对于 PostgreSQL 17，请将两个 PostgreSQL 特定文件替换为它们的 `17` 对应项；共享包保持不变。`documentdb` 元包始终选择 PG18。

对于仅扩展使用，安装扩展和工具文件，然后 [配置 PostgreSQL](#extension-only-installation)。对于完整堆栈，[运行向导](#2-run-the-setup-wizard) 并使用已安装的主版本：PG17 使用 `--pg-version 17`。

文件名前缀如 `ubuntu24.04-` 和 `rhel9-` 用于标识发布资产，而非包名称。DEB 扩展使用版本 `1.0-0`，而其他包使用 `1.0.0`；RPM 使用 `1.0.0`，发布版本为 `1` 或 `1.el9`。

<span id="offline-air-gapped"></span>

### 离线 / 隔离环境 {#offline--air-gapped}

发布文件不包含全部依赖。请在与目标机器具有**相同发行版、版本和架构**的联网机器上，准备 PostgreSQL、所需扩展和所有其他依赖的软件包，也要包括准备机器上已经安装的依赖。按照[离线／隔离环境安装](/documentdb/linux-packages/offline/)的说明，将这些软件包作为本地仓库提供。

<span id="upgrading-to-1-0"></span>

## 升级至 1.0 {#upgrading-to-10}

0.116 或 0.117 版本的包安装可就地升级；将整个堆栈一起迁移。升级包会替换库文件并安装升级脚本，但不会更改数据库：每个 PostgreSQL 实例仍会报告旧的扩展版本，直到其扩展被更新。请先备份；不支持降级。

不支持对曾经运行过发布候选版的主机进行升级，安装程序会拒绝这种操作。请在全新主机上安装 1.0，再使用 `mongodump` 和 `mongorestore` 迁移数据。卸载软件包会保留 PostgreSQL 数据；不要通过重置或复用已接管的实例来绕过升级限制。

### 独立堆栈 {#stand-alone-stack}

停止网关，确保客户端在扩展更新前无法访问新库；升级包，重启 PostgreSQL 以加载新库，然后使用初始安装时的选项重新运行设置向导。向导将更新扩展，随后启动网关：

```bash
# Debian / Ubuntu
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo apt update && sudo apt install --only-upgrade documentdb-18 postgresql-18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools &&
sudo systemctl restart documentdb-postgresql@18.service &&
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin

# RHEL-compatible 9
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo dnf upgrade documentdb-18 postgresql18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools &&
sudo systemctl restart documentdb-postgresql@18.service &&
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

这些命令假设使用了 DocumentDB 包仓库，该仓库自发布日起即包含 1.0 版本。若你是从发布资产安装，请下载 1.0 的资产，并以相同方式[安装相同的一组文件](#install-from-downloaded-assets)替代 `apt`/`dnf` 命令，保留 `&&` 以确保仅在安装成功时才重启和运行设置。网关在向导完成前保持停止状态；若向导提前终止，请再次运行。共享包（`documentdb-common`、`documentdb-gateway`、`documentdb-postgresql-tools`）服务于主机上的每个 PostgreSQL 主版本，因此若安装了多个主版本，请先停止每个主版本的网关，再依次升级并重新运行设置。

在已配置的实例上，向导为日常运维操作：它保留网关端口和 TLS 设置，并对每个 DocumentDB 扩展运行 `ALTER EXTENSION ... UPDATE`。它还会提示输入管理员密码，并在警告和确认后，将其设置在现有管理员用户上：输入当前密码以保留原值，任何其他值都会替换它，旧密码将失效。对于 PostgreSQL 17，请全程使用 `17`。若在密码提示处按 Enter 会中止向导，请再次运行向导并输入密码 ([#772](https://github.com/documentdb/documentdb/issues/772))。

<span id="extension-and-gateway-on-your-own-postgre-sql"></span>

### 在你自己的 PostgreSQL 上部署扩展和网关 {#extension-and-gateway-on-your-own-postgresql}

若你使用 `documentdb-setup --target-postgres-instance 18/main` 采用该实例，向导不会为你重启 PostgreSQL。请停止网关（`sudo systemctl stop documentdb-gateway-local@18.service`），升级包，自行重启 PostgreSQL（Ubuntu 上为 `sudo systemctl restart postgresql@18-main`，EL9 上为 `sudo systemctl restart postgresql-18`），然后再次运行相同的 `documentdb-setup --pg-version 18 --target-postgres-instance 18/main --admin-user admin` 命令；它会如上所述提示管理员密码，更新扩展，随后启动网关。若向导必须更改 `shared_preload_libraries`，它会写入配置更改，提示你重启 PostgreSQL，然后退出而不更新扩展：请重启并再次运行向导。

否则，请先停止网关并升级包。在使用名为 `main` 的集群的 Ubuntu 上：

```bash
sudo systemctl stop documentdb-gateway &&
sudo apt update && sudo apt install --only-upgrade postgresql-18-documentdb \
  documentdb-postgresql-tools documentdb-gateway
sudo -u postgres /usr/bin/psql --cluster 18/main -d postgres -Atc "SHOW shared_preload_libraries;"
```

1.0 仅从 `shared_preload_libraries` 加载扩展的 RUM 库；否则 `CREATE EXTENSION documentdb_extended_rum` 会因 `pg_documentdb_extended_rum can only be loaded via shared_preload_libraries` 失败。若 `pg_documentdb_extended_rum` 不在列表中（在 0.116 安装中可能缺失），请使用 `documentdb-tune` 添加，先审查预演结果：

```bash
sudo documentdb-tune --pg-version 18 --cluster main --dry-run
sudo documentdb-tune --pg-version 18 --cluster main --yes
```

然后重启 PostgreSQL，使其加载新库；接着在每个已创建这些扩展的数据库中按下列顺序更新扩展，因为 `ALTER EXTENSION` 不会更新依赖项。`-1` 将所有语句放在一个事务中执行，因此一旦失败，所有扩展都会保持原版本，网关也只会在更新成功后重新启动。不过，这个事务无法发现缺少预加载的问题：如果 `documentdb_extended_rum` 已经存在，即使未预加载，语句也能成功执行，但随后建立索引时会报错 `The index access method extended_rum could not be located`。所以必须先执行前面的预加载检查：

```bash
sudo systemctl restart postgresql@18-main &&
sudo -u postgres /usr/bin/psql --cluster 18/main -d postgres -1 -v ON_ERROR_STOP=1 \
  -c "ALTER EXTENSION documentdb_core UPDATE;" \
  -c "ALTER EXTENSION documentdb UPDATE;" \
  -c "CREATE EXTENSION IF NOT EXISTS documentdb_extended_rum CASCADE;" \
  -c "ALTER EXTENSION documentdb_extended_rum UPDATE;" &&
sudo systemctl start documentdb-gateway
```

### 检查版本 {#check-the-version}

使用 `mongosh` 连接并运行：

```javascript
db.hello().internal.documentdb_versions
```

应输出 `[ '1.0-0', '1.0.0' ]`：已安装的扩展版本，随后是加载的库版本。若第一个值仍为 `0.116-0` 或 `0.117-0`，则扩展未被更新。参见 [`hello`](/documentdb/reference/commands/diagnostic/hello/)。

### 容器 {#containers}

在现有数据卷上使用更新的 DocumentDB Local 镜像不会更新扩展 ([#773](https://github.com/documentdb/documentdb/issues/773))。请在新卷上启动 1.0，并使用 `mongodump` 和 `mongorestore` 移动数据。参见 [升级镜像](/documentdb/documentdb-local/#upgrading-the-image)。

## 已弃用的目标 {#retired-targets}

托管矩阵已排除 PostgreSQL 15/16、Debian 11/12/13、Ubuntu 22.04 以及与 RHEL 兼容的 8 版本。自 v0.116 起，不再保留已弃用目标的旧版包，包括此前为 Ubuntu 24.04 和 EL9 提供的 PG16 扩展。现有安装仍可运行，但无法从 documentdb.io 更新或重新安装这些包。

对于旧版安装，请使用匹配的 [GitHub 发布资产](https://github.com/documentdb/documentdb/releases)，包括其依赖项，或在可用时考虑 PGDG 和源码构建。更换提供方或平台需要兼容性与恢复规划；这不是自动迁移。

已弃用的 URL 保留空的签名元数据，以确保包管理器刷新不会干扰无关操作。若主机不再使用第一方包，请移除其 DocumentDB 仓库条目。这不会移除包或数据；若其他包仍使用 PGDG，请保留它。

```bash
# Debian / Ubuntu
sudo rm -f /etc/apt/sources.list.d/documentdb.list
sudo apt update

# RHEL-compatible
sudo rm -f /etc/yum.repos.d/documentdb.repo
sudo dnf clean all
```

## 容器镜像 {#container-image}

对于 macOS、Windows 或基于容器的安装，请参阅 [DocumentDB Local](/documentdb/documentdb-local/)。版本 1.0 提供了适用于 PostgreSQL 15-18 的 Linux amd64/arm64 镜像；如需可复现的版本，请使用带版本标签的镜像，而非 `latest`。
