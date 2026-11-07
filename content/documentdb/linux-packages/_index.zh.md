---
title: 软件包安装的运维
description: 通过 Linux 软件包安装 DocumentDB 后的安全配置、管理、升级和卸载，以及已知的软件包安装问题。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 30
translation_source_sha256: f5bb1676c7758824e7a5e29ff1d89d5a73b05aea60a54bf50bf848b2b8161959
translation_review: AI-assisted bilingual review; 2026-11-07
---

通过 Linux 软件包安装 DocumentDB 后的日常运维：保护端点、管理服务、执行 SQL、升级和卸载。请先按 [Linux 软件包快速入门](/documentdb/getting-started/packages/)完成安装。

## 向网络开放服务之前 {#before-exposing-it-to-a-network}

网关默认绑定 **所有接口**（`0.0.0.0:10260` 和 `[::]:10260`）。其后端的 PostgreSQL 实例仍保持在回环地址上。

在除私有机器外的任何地方使用之前：

- 在 `/etc/documentdb/local/<major>/gateway.env` 中设置 `DOCUMENTDB_LISTEN_ADDR=127.0.0.1:10260` 以限制监听地址，然后重启服务；也可以通过防火墙限制对端口 `10260` 的访问。**重新运行 `documentdb-setup` 会在不提示的情况下将其重置为监听所有地址**，因此之后应使用 `grep DOCUMENTDB_LISTEN_ADDR /etc/documentdb/local/<major>/gateway.env` 再次检查。防火墙规则是更持久的控制措施。
- 为管理员设置强密码，并为各应用创建独立用户，避免共享 `admin`。

### 替换自签名证书 {#replace-the-self-signed-certificate}

`tlsAllowInvalidCertificates=true` 会关闭对服务器身份的验证。要使用正式证书，请在 `/etc/documentdb/local/<major>/gateway.env` 中设置以下三个值：

```ini
DOCUMENTDB_TLS_AUTO_GENERATE=false
DOCUMENTDB_TLS_CERT_FILE=/etc/documentdb/tls/server.crt
DOCUMENTDB_TLS_KEY_FILE=/etc/documentdb/tls/server.key
```

网关以 `documentdb-gateway` 账户运行。该账户必须有权限遍历证书和密钥路径的所有父目录；应限制私钥的访问权限，同时确保该账户可以读取，例如设置属主和属组为 `root:documentdb-gateway`，权限为 `0640`。重启 `documentdb-gateway-local@<major>.service`，确认服务已运行，然后从客户端配置中移除 `tlsAllowInvalidCertificates=true`。

## 服务与路径 {#services-and-paths}

```bash
sudo documentdb-setup --status      # gateway listener, service states, resolved paths
documentdb-gateway --version        # DocumentDB version
dpkg -l | grep documentdb           # or: rpm -qa | grep documentdb
```

| 项目 | 位置 |
| --- | --- |
| 网关端口 | `10260` |
| PostgreSQL 端口 | `9700 + <major>`（PG 18 为 9718），仅限回环 |
| 网关日志 | systemd：`journalctl -u documentdb-gateway-local@18.service` · 否则为 `/var/lib/documentdb-gateway/gateway.log` |
| PostgreSQL 日志 | systemd：`journalctl -u documentdb-postgresql@18.service` · 否则为 `/var/lib/documentdb-local/<major>/data/pglog.log` |
| 安装状态 / 网关环境 | `/etc/documentdb/local/<major>/setup.conf`，`.../gateway.env` |

在使用 systemd 的主机上，两个服务都将日志写入 journal。只有当 `documentdb-setup` 回退到不依赖 systemd 的 `nohup` 模式时，才会生成上述日志**文件**。`documentdb-setup --status` 会显示本机实际使用的日志位置。

systemd 单元按 PostgreSQL 主版本使用模板：

```bash
sudo systemctl status  documentdb-local@18.target
sudo systemctl restart documentdb-local@18.target
sudo systemctl stop    documentdb-local@18.target
```

<span id="adopt-an-existing-postgre-sql-instance"></span>

## 接管现有 PostgreSQL 实例 {#adopt-an-existing-postgresql-instance}

只有 PostgreSQL 已经位于**网关所在的本地主机**，且其服务和数据仍由运维人员管理时，才使用此模式；不支持接管远程 PostgreSQL 实例。修改 PostgreSQL 配置和重启服务需要管理员权限。请先备份实例。向导不会创建、删除、启动或停止这个 PostgreSQL 实例，但会添加受管配置块、创建网关角色、安装 DocumentDB 扩展，并注册网关。

将实例标识为 `<major>/<name>`。在 Ubuntu 上运行 `pg_lsclusters`；典型实例为 `18/main`。EL9 上的标准 PGDG 布局为每个主版本一个实例，也使用 `18/main`；若其监听非默认端口，请添加 `--pg-port`。

```bash
sudo documentdb-setup --target-postgres-instance 18/main --admin-user admin
```

如果修改了 `shared_preload_libraries`，首次运行时会提示需要由管理员重启，而不会直接完成配置。请重启由运维人员管理的 PostgreSQL 服务，然后原样执行向导输出的配置命令。常见的服务名为 Ubuntu 上的 `postgresql@18-main.service`，以及 EL9 上的 `postgresql-18.service`。向导按设计不会自动重启接管的 PostgreSQL 实例。

向导默认设置的 `default_toast_compression` 会影响接管实例中所有数据库新写入的值。如果其他工作负载必须保留 PostgreSQL 自身的默认值，请在两次运行配置命令时都加上前缀 `sudo DOCUMENTDB_TOAST_COMPRESSION=default`。

<span id="install-the-postgre-sql-extension-only"></span>

## 仅安装 PostgreSQL 扩展 {#install-the-postgresql-extension-only}

选择此高级路径以在你自行管理的 PostgreSQL 中启用面向 SQL 的 DocumentDB 功能。它**不**安装网关、为驱动程序创建网络端点，也不运行 `documentdb-setup`。Shell、驱动程序和 VS Code 快速入门需要完整的堆栈。

根据 PostgreSQL 主版本选择扩展软件包：Ubuntu 使用 `postgresql-N-documentdb`，EL9 使用 `postgresqlN-documentdb`。PostgreSQL 配置、启用扩展和服务重启均由你负责。除 `documentdb` 外，还必须创建 `documentdb_extended_rum`：`CREATE EXTENSION documentdb CASCADE` 不会自动创建后者，缺少它时所有索引创建操作都会失败。请按对应发布版的[手动软件包安装说明](https://github.com/documentdb/documentdb/blob/v1.0-0/packaging/README.md)操作；如果已经安装 PostgreSQL 及扩展的全部依赖，也可以按[仅安装扩展的离线说明](/documentdb/linux-packages/offline/#smaller-offline-cases)操作。

## 在软件包管理的私有实例上执行 SQL {#running-sql-against-a-package-managed-private-instance}

新建的 PostgreSQL 实例以 `documentdb-local` 用户运行，通过套接字提供连接，因此直接运行 `psql` 找不到它：

```bash
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres
```

```sql
SELECT extname, extversion FROM pg_extension WHERE extname LIKE 'documentdb%';
```

对于接管的实例，请使用运维人员原有的 PostgreSQL 连接方式。

## 升级 {#upgrading}

通过 v0.116 或 v0.117 软件包安装的实例，可以原地升级到 1.0。应当一并升级整套组件；仅升级 `postgresql-N-documentdb` 不会更新网关、工具、公共组件或 `documentdb-N`。以下步骤使用 systemd，不涵盖没有 systemd 的主机。对于软件包管理的私有 PostgreSQL 18 实例：

> [!WARNING]
> 曾运行过 1.0 发布候选版（RC1 或 RC2）的主机无升级路径。请将其迁移至干净主机或新建的空 PostgreSQL 实例，并遵循 [全新安装](/documentdb/getting-started/packages/)。仅移除包不会创建全新数据库：包移除会保留 PostgreSQL 数据和数据库内内容，后续设置运行将复用已初始化的数据目录。

```bash
# Debian / Ubuntu
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo apt update &&
sudo apt install --only-upgrade documentdb-18 postgresql-18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools

# EL9: use this instead of the apt commands above
sudo systemctl stop documentdb-gateway-local@18.service &&
sudo dnf upgrade documentdb-18 postgresql18-documentdb \
  documentdb-common documentdb-gateway documentdb-postgresql-tools
```

升级软件包不会更新数据库系统目录。最简单的方法是重启 PostgreSQL，使其加载新库，再使用最初安装时的选项重新运行配置向导。向导会更新扩展，随后启动网关：

```bash
sudo systemctl restart documentdb-postgresql@18.service &&
sudo documentdb-setup --pg-version 18 --use-new-postgres-instance --admin-user admin
```

配置向导会添加缺失的 `shared_preload_libraries` 条目，并更新扩展，但扩展更新仅针对 `postgres` 数据库。如果网关使用其他数据库，请采用下文的手动方式。向导还会询问管理员密码，并将其设置到现有管理员用户上；输入当前密码即可保留原密码。

手动更新，或针对安装了 DocumentDB 的其他每个数据库，首先检查扩展的 RUM 库是否已预加载：

```bash
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres -X -Atc "SHOW shared_preload_libraries;"
```

如果缺少 `pg_documentdb_extended_rum`（0.116 安装可能出现此情况），请在更新前添加它；否则下文的更新虽然会成功，但随后建立索引时会失败。如果网关使用 `postgres` 数据库，按前文重新运行配置向导即可。如果使用其他数据库，请自行在实例的 `postgresql.conf` 中将该库加入 `shared_preload_libraries`：运行向导会将网关重新指向 `postgres`。然后重启 PostgreSQL，在一个事务中更新扩展，并且只在更新成功后启动网关：

```bash
sudo systemctl restart documentdb-postgresql@18.service &&
sudo -u documentdb-local psql -h /run/documentdb-local/18/postgresql -p 9718 -d postgres \
  -X -1 -v ON_ERROR_STOP=1 \
  -c 'ALTER EXTENSION documentdb_core UPDATE;' \
  -c 'ALTER EXTENSION documentdb UPDATE;' \
  -c 'CREATE EXTENSION IF NOT EXISTS documentdb_extended_rum CASCADE;' \
  -c 'ALTER EXTENSION documentdb_extended_rum UPDATE;' &&
sudo systemctl start documentdb-gateway-local@18.service
```

`-1` 以一个事务运行这些语句：如果其中任何一条失败，所有扩展将保持在旧版本，且网关将保持停止状态。`-X` 跳过 `~/.psqlrc`，否则可能将 `ON_ERROR_STOP` 关闭。如果 DocumentDB 也安装在其他数据库中，请在最后一行之前对每个数据库运行 `psql` 部分，使用相应的 `-d`，以确保网关仅在每个数据库都更新后才启动。PostgreSQL 会自动应用中间升级脚本。请先进行备份。

在同时运行 PostgreSQL 17 和 18 的主机上，`documentdb-common`、`documentdb-gateway` 和 `documentdb-postgresql-tools` 服务于两个主版本，因此升级它们会影响两者：在升级前停止两个网关（`documentdb-gateway-local@17.service` 和 `@18.service`），然后分别升级每个主版本。

对于接管的 PostgreSQL 实例，配置向导从不重启 PostgreSQL。升级前先停止网关（`documentdb-gateway-local@18.service`），自行重启由运维人员管理的 PostgreSQL 服务，再运行 `documentdb-setup --pg-version 18 --target-postgres-instance 18/main --admin-user admin`（替换为实际集群名）；它会更新扩展，然后启动网关。如果向导需要修改 `shared_preload_libraries`，它会直接退出，不更新扩展：请重启 PostgreSQL，再运行一次向导。手动操作时，使用该实例自己的 `psql` 连接方式。

## 移除或重置 {#remove-or-reset}

### 新建环境：销毁由包管理的实例 {#greenfield-destroy-the-package-managed-instance}

```bash
# Reset reads setup.conf before removing it, stops the services, and destroys
# the package-managed data directory. Do not run --restore first.
sudo documentdb-local-reset --pg-version 18 --confirm-destroy    # DESTROYS the data directory

# Name the package you installed AND the extension: autoremove does not reap
# postgresql-18-documentdb, and 'remove' would leave config behind.
sudo apt purge --autoremove documentdb-18 postgresql-18-documentdb
sudo dnf remove documentdb-18 postgresql18-documentdb && sudo dnf autoremove
```

<span id="brownfield-detach-from-an-existing-postgre-sql-instance"></span>

### 既有环境：从现有 PostgreSQL 实例中分离 {#brownfield-detach-from-an-existing-postgresql-instance}

在恢复前，运行 `sudo documentdb-setup --status` 并记下你将要移除的主版本的网关端口。

在 systemd 主机上，指定主版本的恢复操作会停止并禁用该版本的网关：

```bash
sudo documentdb-setup --restore --pg-version 18
```

在没有 systemd 的主机上，当前配置工具无法可靠地判断某个 nohup 网关进程属于哪个 PostgreSQL 主版本。如果只配置了一个 DocumentDB 主版本，请执行不指定主版本的恢复操作，以触发遗留网关进程的清理：

```bash
sudo documentdb-setup --restore --yes
```

如果在没有 systemd 的主机上配置了多个 DocumentDB 主版本，请安排维护窗口，并执行同样的不指定主版本的恢复操作。它会从所有已配置的主版本中分离 DocumentDB，并停止 nohup 网关。之后，为需要保留的主版本重新运行配置向导。在没有 systemd 的主机上，仅执行指定主版本的恢复操作并不够。

恢复后重启接管的 PostgreSQL 服务，使受管配置的移除生效。不指定主版本、恢复多个版本时，需重启涉及的每个由运维人员管理的 PostgreSQL 服务。

在移除包之前，验证目标网关端口不再监听。替换为你上面记下的端口；该命令不应产生任何输出：

```bash
ss -lnt | grep ':10260'
```

然后移除选定的主版本：

```bash
sudo apt purge --autoremove documentdb-18 postgresql-18-documentdb
sudo dnf remove documentdb-18 postgresql18-documentdb && sudo dnf autoremove
```

对于接管现有实例的安装，不要运行 `documentdb-local-reset`：PostgreSQL 实例和数据属于运维方。重置新建实例前也不要先运行恢复操作，因为恢复会删除用于识别自定义数据目录、保护接管集群的状态记录。

在使用 systemd 且安装多个主版本的主机上，每次只卸载一个主版本，并重新检查保留的版本：共享工具由 `documentdb-common` 提供，而只有 `documentdb-N` 会通过依赖保留它。

## 已知的包安装问题 {#known-package-install-issues}

这些问题属于本版本的缺陷，而非预期行为。大多数需要无 systemd 主机才会触发；状态问题也影响 systemd 主机。

| 范围 | 问题 | 影响环境 |
| --- | --- | --- |
| 状态 | 任意进程占用端口 10260 时，`documentdb-setup --status` 都可能报告为 "active" | **任何主机** |
| 重启 | 重新运行 `documentdb-setup` 进行重启可能卡住；将输出重定向到文件可避免此问题 | 无 systemd |
| 停止 | 指定主版本的 `documentdb-setup --restore --pg-version N` 无法停止 nohup 网关；请按前文没有 systemd 时分离既有实例的步骤操作 | 无 systemd |
| 最小化 RHEL | 请先安装 `procps-ng`，否则 `--restore` 会报告成功，但网关仍继续提供服务，后续运行会报错 `Port 10260 is already in use` | 无 systemd |

**重要环境应优先选择使用 systemd 的主机**，让 systemd 管理服务生命周期，而不是交给配置脚本。

<span id="multiple-postgre-sql-majors"></span>

## 多个 PostgreSQL 主版本 {#multiple-postgresql-majors}

为每个你配置的主版本安装对应的 `documentdb-N`。`documentdb-setup` 会拒绝缺少扩展包的主版本：

```text
ERROR: The DocumentDB extension package is not installed for PostgreSQL 17
(/usr/share/postgresql/17/extension/documentdb.control is missing).
```

每个主版本还需要独立的网关端口。如果不通过 `--gateway-port` 指定其他端口，第二个版本会报错 `Gateway port 10260 is already in use`：

```bash
sudo documentdb-setup --pg-version 17 --use-new-postgres-instance \
  --gateway-port 10261 --admin-user admin
```

## 故障排除 {#troubleshooting}

超出 [快速入门](/documentdb/getting-started/packages/#troubleshooting) 中列出的四种故障模式：

- `pgdg-common` 报错 `Bad GPG signature`：PGDG 仓库 URL 中的架构不正确
- 在容器中执行 `apt install` 卡住：先执行 `export DEBIAN_FRONTEND=noninteractive`；以 `root` 运行时，去掉命令开头的 `sudo`（最小化镜像往往没有 `sudo`）。保留用于切换用户的 `sudo -u <user>`。由于该账户的 shell 为 `/usr/sbin/nologin`，`su documentdb-local -c` 会失败，请改用 `su -s /bin/bash documentdb-local -c '...'`
- 最小化 EL9 主机提示 `ss: command not found`：安装 `iproute`，DocumentDB 软件包不会自动安装它
- `mongosh` 中的 `db.version()` 和 `buildInfo` 报告的是模拟的 MongoDB 线协议版本，而不是 DocumentDB 版本；请使用 `documentdb-gateway --version`

## 无人值守配置 {#unattended-setup}

`documentdb-setup` 会提示输入管理员密码。在服务器或 CI 中，请提供且只提供一种密码来源，并传入 `--yes`。新建私有实例时：

```bash
printf '%s' "$ADMIN_PW" | sudo documentdb-setup --pg-version 18 \
  --use-new-postgres-instance --admin-user admin --admin-password-stdin --yes
```

接管现有实例时，将 `--pg-version 18 --use-new-postgres-instance` 替换为 `--target-postgres-instance 18/main`。也可以使用 `--admin-password-file /path/to/protected/file`，代替从标准输入读取密码。
