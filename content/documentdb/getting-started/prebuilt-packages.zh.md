---
title: 预编译软件包
description: 通过设置向导安装完整的 DocumentDB 堆栈，或选择单独的 PostgreSQL 和网关包。包含 PGDG 和源码构建选项。
type: docs
upstream_source: documentdb-20261121
upstream_link: https://github.com/documentdb/docs/blob/8fb7fdaffb37c4f5e4c8ba670bd2a05323a92ec5/getting-started/prebuilt-packages.md
source_status: superseded
weight: 1070
translation_source_sha256: f1aea398b94bed1d6e338cf6c7f59790dfaaf91fa23b58dbd9d1c85a8f420a5b
translation_review: AI-assisted incremental bilingual self-review (fidelity, terminology, Chinese prose); 2026-11-21
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

当前版本为 [`v1.2-0`](https://github.com/documentdb/documentdb/releases/tag/v1.2-0)。变更内容见 [1.2 发布说明](/documentdb/getting-started/release-notes-1.2/)。官方 CI 构建并测试了以下完整堆栈：

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

选择版本的方法如下：

| 命令 | 安装内容 | 后续 `apt upgrade` / `dnf upgrade` 的行为 |
| --- | --- | --- |
| `sudo sh documentdb-install.sh` | `latest` 软件包通道的最新版本 | 跟随每个新版本升级 |
| `sudo sh documentdb-install.sh --stable` | `stable` 通道；新版本发布后，它可能暂时保留上一版本 | 跟随 `stable` 升级 |
| `sudo sh documentdb-install.sh --version 1.0.0` | 从 GitHub 发布文件安装指定版本（1.0.0 或更高） | 不升级：未配置 DocumentDB 仓库 |

安装程序会要求确认计划并选择管理员密码。要无人值守运行，请将密码保存在 root 拥有的文件中，并传入 `--yes` 选项：

```sh
printf 'DocumentDB admin password: '; IFS= read -r -s PW; echo
printf '%s\n' "$PW" | sudo install -m 600 /dev/stdin /root/documentdb-admin.pw
sudo sh documentdb-install.sh --yes \
  --admin-password-file /root/documentdb-admin.pw --accept-external-listen
```

`--accept-external-listen` 确认网关默认监听所有接口。
手动步骤安装的是相同版本。若需将现有安装升级到 1.2 版本，请参阅[升级至 1.2](#upgrading-to-12)。

## 设置并连接 {#set-up-and-connect}

这些步骤适用于**全新独立安装**。对于现有部署，请先阅读[升级至 1.2](#upgrading-to-12)。

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

截至 **2026-11-15**，PGDG 为 PostgreSQL **15–18** 提供 DocumentDB **1.2**（扩展版本 `1.2-0`，软件包版本 `1.2-0-1.pgdg…`），覆盖 Debian 13（`trixie-pgdg`）、Debian 14（`forky-pgdg`，testing）和 Ubuntu 26.04（`resolute-pgdg`），包括 **amd64 和 arm64**；Ubuntu 26.10（`stonking-pgdg`）则仅提供 amd64。PGDG 构建可能落后于官方发布，目标平台也与官方支持范围不同；当前发布内容请查阅 [PGDG 包池](https://apt.postgresql.org/pub/repos/apt/pool/main/d/documentdb/)。

全新安装请按 [Debian](https://www.postgresql.org/download/linux/debian/#apt) 或 [Ubuntu](https://www.postgresql.org/download/linux/ubuntu/#apt) 的 PGDG 仓库设置说明配置，然后检查所选 PostgreSQL 主版本的候选软件包：

```bash
sudo apt update
apt-cache policy postgresql-18-documentdb
```

如果候选版本为 `1.2-0-1.pgdg…` 或更高，请安装：

```bash
sudo apt install postgresql-18-documentdb
```

单独配置 PostgreSQL 并为该打包版本创建扩展；上述官方辅助命令不适用。不要使用其他发行版的仓库获取缺失的包，或将供应商切换视为就地升级。

较旧的 PGDG 安装可原地升级；1.2 软件包包含 PGDG 从 0.108 起发布过的所有版本的升级脚本。请先备份；不支持降级。停止应用和自行运行的网关，保持停止状态，直到扩展更新完成。以下命令使用 PostgreSQL 18、集群 `main` 和数据库 `postgres`：请在所有命令中替换为实际值，并更新所有创建过这些扩展的数据库。

升级软件包，并检查 `shared_preload_libraries` 的设置位置：

```bash
sudo apt update && sudo apt install --only-upgrade postgresql-18-documentdb
sudo -u postgres psql --cluster 18/main -d postgres -Atc \
  "SELECT setting, sourcefile FROM pg_settings WHERE name = 'shared_preload_libraries';"
```

如果未列出 `pg_documentdb_extended_rum`（0.116 及更早版本可能缺少），在显示的文件中将其加到现有的 `pg_cron, pg_documentdb_core, pg_documentdb` 旁边，通常是 `/etc/postgresql/18/main/postgresql.conf`；通过 `ALTER SYSTEM` 设置的值位于 `postgresql.auto.conf`，会覆盖前者。DocumentDB [只从该设置加载此库](#extension-and-gateway-on-your-own-postgresql)；当 `documentdb_extended_rum` 扩展已经存在时，即使缺少该设置，扩展更新也会成功，但之后构建索引会失败。无论是否修改配置，接下来都要重启 PostgreSQL 以加载新库，并确认四个库均已列出：

```bash
sudo systemctl restart postgresql@18-main &&
sudo -u postgres psql --cluster 18/main -d postgres -Atc "SHOW shared_preload_libraries;"
```

然后更新扩展，检查软件包、扩展和库版本；PGDG 不提供网关，无法执行下文的 `mongosh` 检查：

```bash
sudo -u postgres psql --cluster 18/main -d postgres -1 -v ON_ERROR_STOP=1 \
  -c "ALTER EXTENSION documentdb_core UPDATE;" \
  -c "ALTER EXTENSION documentdb UPDATE;" \
  -c "CREATE EXTENSION IF NOT EXISTS documentdb_extended_rum CASCADE;" \
  -c "ALTER EXTENSION documentdb_extended_rum UPDATE;"
dpkg-query -W -f='${Version}\n' postgresql-18-documentdb
sudo -u postgres psql --cluster 18/main -d postgres -At \
  -c "SELECT extname, extversion FROM pg_extension WHERE extname LIKE 'documentdb%';" \
  -c "SELECT documentdb_api.binary_version();"
```

预期软件包版本为 `1.2-0-1.pgdg…`，各扩展版本均为 `1.2-0`，库版本为 `1.2.0`。

在安装 PGDG `1.0~RC1` 的主机上，`apt upgrade` 会提供 `1.2-0`，但不支持升级候选发布版。升级前请检查 `dpkg-query`：RC1 已经报告扩展版本 `1.0-0` 和库版本 `1.0.0`，只有软件包版本能将其与 1.0 区分开，且新库不会修复 RC 写入的数据。应将数据迁移到全新的 1.2 实例。`mongodump` 和 `mongorestore` 要求两个实例前端都有兼容 MongoDB 的网关，而 PGDG 不提供网关。

## 社区构建 {#community-builds}

你的目标没有可用包？提供的脚本使用 Docker 构建 DEB 或 RPM 包；选择发行版和 PostgreSQL 主版本，而非自行编写打包文件。

使用与目标架构相同的 Linux 构建环境，并准备 Git、Docker、Bash 4+ 和 GNU 工具。例如，为 Debian 12 和 PostgreSQL 18 构建扩展：

```bash
git clone --depth 1 --branch v1.2-0 https://github.com/documentdb/documentdb.git
cd documentdb
./packaging/build_packages.sh --os deb12 --pg 18 --version 1.2.0 --output-dir packages
```

显式传递 `--version 1.2.0`，使软件包带有正式发布版本号。

对于完整的独立 DEB 集合，需在构建主机上提供 `dpkg-deb`，然后构建网关和共享包：

```bash
./packaging/gateway/build_gateway_packages.sh --os deb12 --pg 18 \
  --version 1.2.0 --output-dir packages
./packaging/build_extra_packages.sh --type deb --pg 18 \
  --version 1.2.0 --output-dir packages
```

输出位于 `packages/`。RPM 额外组件则需要主机 `rpmbuild` 和适用的 RPM 宏。[版本化打包指南](https://github.com/documentdb/documentdb/blob/v1.2-0/packaging/README.md) 列出了目标、前提条件和干净安装检查项。

在你的环境中验证超出官方 CI 矩阵的目标构建。PostgreSQL 15 仅支持扩展；包管理网关设置需要 PostgreSQL 16 或更高版本。

## 下载并验证 {#download-and-verify}

当你需要确切的官方版本而非仓库安装时，请使用发布资产。每个发布都会发布其 Linux 软件包，包含 `SHA256SUMS` 和 `manifest.txt`。

```bash
gh release download v1.2-0 -R documentdb/documentdb -D pkgs && cd pkgs && sha256sum -c SHA256SUMS
```

这将下载所有格式、架构和 PostgreSQL 主版本。仅安装下方匹配的子集，不要安装每个下载的文件。

## 从下载的资产安装 {#install-from-downloaded-assets}

首先启用依赖仓库：PGDG，以及在 EL9 上的 EPEL 和 CRB / CodeReady Builder。将匹配的本地文件传递给 **一个** `apt` 或 `dnf` 命令，以确保依赖在同一次事务中解析。

这些示例安装 `documentdb-18` 及其依赖项；可选的 `documentdb` 元包无需使用。

<span id="deb-ubuntu-24-04-postgre-sql-18-amd64"></span>

### DEB（Ubuntu 24.04，PostgreSQL 18，amd64） {#deb-ubuntu-2404-postgresql-18-amd64}

对于 arm64，请将 `amd64` 替换为 `arm64`。仅网关和扩展文件是架构相关的。

```bash
sudo apt install ./ubuntu24.04-documentdb-18_1.2.0_all.deb \
                 ./ubuntu24.04-documentdb-common_1.2.0_all.deb \
                 ./ubuntu24.04-documentdb-postgresql-tools_1.2.0_all.deb \
                 ./ubuntu24.04-documentdb-gateway_1.2.0_amd64.deb \
                 ./ubuntu24.04-postgresql-18-documentdb_1.2-0_amd64.deb
```

<span id="rpm-rhel-compatible-9-postgre-sql-18-x86-64"></span>

### RPM（RHEL 兼容 9，PostgreSQL 18，x86_64） {#rpm-rhel-compatible-9-postgresql-18-x86_64}

对于 arm64，请将 `x86_64` 替换为 `aarch64`；保持 `noarch` 文件不变。

```bash
sudo dnf install ./documentdb-18-1.2.0-1.noarch.rpm \
                 ./documentdb-common-1.2.0-1.noarch.rpm \
                 ./documentdb-postgresql-tools-1.2.0-1.noarch.rpm \
                 ./documentdb-gateway-1.2.0-1.el9.x86_64.rpm \
                 ./rhel9-postgresql18-documentdb-1.2.0-1.el9.x86_64.rpm
```

对于 PostgreSQL 17，请将两个 PostgreSQL 特定文件替换为它们的 `17` 对应项；共享包保持不变。`documentdb` 元包始终选择 PG18。

对于仅扩展使用，安装扩展和工具文件，然后 [配置 PostgreSQL](#extension-only-installation)。对于完整堆栈，[运行向导](#2-run-the-setup-wizard) 并使用已安装的主版本：PG17 使用 `--pg-version 17`。

文件名前缀如 `ubuntu24.04-` 和 `rhel9-` 用于标识发布资产，而非包名称。DEB 扩展使用版本 `1.2-0`，而其他包使用 `1.2.0`；RPM 使用 `1.2.0`，发布版本为 `1` 或 `1.el9`。

<span id="offline-air-gapped"></span>

### 离线 / 隔离环境 {#offline--air-gapped}

发布文件不包含全部依赖。请在与目标机器具有**相同发行版、版本和架构**的联网机器上，准备 PostgreSQL、所需扩展和所有其他依赖的软件包，也要包括准备机器上已经安装的依赖。按照[离线／隔离环境安装](/documentdb/linux-packages/offline/)的说明，将这些软件包作为本地仓库提供。

<span id="upgrading-to-1-2"></span>

<span id="upgrading-to-10"></span>
<span id="upgrading-to-1-0"></span>

## 升级至 1.2 {#upgrading-to-12}

通过软件包安装的 1.0 可原地升级；请一并升级所有 DocumentDB 软件包。新版本带有新库和新的扩展系统目录版本。PostgreSQL 只有重启后才会加载新库，各数据库中的系统目录也只有执行 `ALTER EXTENSION ... UPDATE` 后才会更新；两步都完成之前，部分命令会报 `InternalError`。请先备份；不支持降级。

曾运行候选发布版的主机不受升级支持，安装程序会拒绝升级。请在全新主机上安装 1.2，用 `mongodump` 和 `mongorestore` 迁移数据。卸载软件包会保留 PostgreSQL 数据；不要通过重置或复用被接管的实例绕过升级限制。

### 独立部署组件 {#stand-alone-stack}

由 1.0 安装程序或 `--stable` 配置的主机跟随 `stable` 软件包通道。两个通道现在均提供 1.2。若希望以后在新版本发布后立即获取，可先选择切换到 `latest`：

```bash
# Debian / Ubuntu
sudo sed -i 's# stable ubuntu24$# latest ubuntu24#' /etc/apt/sources.list.d/documentdb.list

# RHEL-compatible 9
sudo sed -i 's#^baseurl=https://documentdb.io/rpm/rhel9$#baseurl=https://documentdb.io/rpm/latest/rhel9#' /etc/yum.repos.d/documentdb.repo
```

然后升级软件包，并通过配置向导完成升级。指定安装使用的 PostgreSQL 主版本，以及当时使用的 `--data-dir` 或 `--pg-port` 参数：

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install --only-upgrade documentdb-18 postgresql-18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools &&
sudo documentdb-setup --pg-version 18 --yes

# RHEL-compatible 9
sudo dnf upgrade documentdb-18 postgresql18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools &&
sudo documentdb-setup --pg-version 18 --yes
```

软件包会重启网关，但不会重启 PostgreSQL。向导重启 `documentdb-postgresql@18` 一次以加载新库，然后更新 `documentdb_core`、`documentdb` 和 `documentdb_extended_rum`，并保留网关端口和 TLS 设置。未指定 `--admin-user` 时不需要密码，所有 admin 用户及密码保持原样；指定 `--admin-user` 时，会像其他重新运行向导的情况一样重置该用户的密码。PostgreSQL 17 请将所有相关位置改为 `17`。

这些命令假定使用 DocumentDB 软件包仓库。如果原先从发布文件安装，请下载 1.2 发布文件，用[同样的方法](#install-from-downloaded-assets)安装相同的一组文件，以替代 `apt`/`dnf` 命令。共享软件包（`documentdb-common`、`documentdb-gateway`、`documentdb-postgresql-tools`）服务于主机上的所有 PostgreSQL 主版本，因此安装了多个主版本时，需分别运行配置向导。

<span id="extension-and-gateway-on-your-own-postgre-sql"></span>

### 在自行管理的 PostgreSQL 上运行扩展与网关 {#extension-and-gateway-on-your-own-postgresql}

如果通过 `documentdb-setup --target-postgres-instance 18/main` 接管了实例，先升级软件包，再运行：

```bash
sudo documentdb-setup --target-postgres-instance 18/main --yes
```

向导不会重启你的 PostgreSQL。它输出下一步需要运行的重启命令和配置命令，然后停止；请执行这两个命令。第二次运行会更新扩展并保留已有 admin 用户。

其他情况下，按以下顺序停止网关、升级软件包、重启 PostgreSQL 以加载新库，再更新所有创建过这些扩展的数据库；`ALTER EXTENSION` 不会自动更新依赖项。在 Ubuntu 上，假设集群名为 `main`：

```bash
sudo systemctl stop documentdb-gateway &&
sudo apt update && sudo apt install --only-upgrade postgresql-18-documentdb \
  documentdb-postgresql-tools documentdb-gateway &&
sudo systemctl restart postgresql@18-main &&
sudo -u postgres /usr/bin/psql --cluster 18/main -d postgres -1 -v ON_ERROR_STOP=1 \
  -c "ALTER EXTENSION documentdb_core UPDATE;" \
  -c "ALTER EXTENSION documentdb UPDATE;" \
  -c "ALTER EXTENSION documentdb_extended_rum UPDATE;" &&
sudo systemctl start documentdb-gateway
```

仅安装扩展时，省略网关命令。`-1` 将语句作为一个事务运行，失败时所有扩展保持旧版本，且只有成功后才重新启动网关。在 PostgreSQL 重启之前运行这些语句，会报 `could not find function ... in file ".../pg_documentdb.so"`。请在 `shared_preload_libraries` 中保留 `pg_documentdb_extended_rum`：DocumentDB 只通过此设置加载扩展 RUM 库。

### 检查版本 {#check-the-version}

通过 `mongosh` 连接并运行：

```javascript
db.hello().internal.documentdb_versions
```

预期输出为 `[ '1.2-0', '1.2.0' ]`：依次是已安装的扩展版本和已加载的库版本。如果第一个值仍为 `1.0-0`，说明扩展尚未更新。参见 [`hello`](/documentdb/reference/commands/diagnostic/hello/)。

### 容器 {#containers}

较新的 DocumentDB Local 镜像会在启动时更新已有数据卷上的扩展。参见[升级镜像](/documentdb/documentdb-local/#upgrading-the-image)。

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

对于 macOS、Windows 或基于容器的安装，请参阅 [DocumentDB Local](/documentdb/documentdb-local/)。版本 1.2 提供了适用于 PostgreSQL 15-18 的 Linux amd64/arm64 镜像；如需可复现的版本，请使用带版本标签的镜像，而非 `latest`。
