---
title: 离线 / 隔离安装
description: 在联网机器上准备完整的依赖闭包，并在无互联网访问的主机上安装 DocumentDB。
type: docs
upstream_source: documentdb
upstream_link: https://github.com/documentdb/documentdb.github.io/blob/90cfa088351557cd618034dfc00ab817c35a5f76/app/services/articleService.ts
upstream_ref: website 90cfa08; DocumentDB 1.0
weight: 20
translation_source_sha256: 0650ca39576e974e60eb6c37c91b9dee6289d29ae92c2e132f987c2e5f7893d3
translation_review: AI-assisted bilingual review; 2026-11-07
---

隔离主机也无法访问 PGDG，而 DocumentDB 需要从那里获取 PostgreSQL、`pg_cron`、`pgvector` 和 PostGIS，因此仅有发布文件还不够。请在与目标主机**发行版、版本和架构完全相同**的联网机器上，准备包含全部直接及间接依赖的软件包。

对于联网主机，请改用 [Linux 软件包快速入门](/documentdb/getting-started/packages/)。

## 准备打包文件（联网机器） {#stage-the-bundle-connected-machine}

按照在线安装的配置方式配置仓库：运行适用于你发行版的整个 [安装](/documentdb/getting-started/packages/#install) 块，**但不包括最后一行 `sudo apt install -y documentdb-18` / `sudo dnf install -y documentdb-18`** —— 删除该行以及其前的 `&& \`。在 RHEL 上，DocumentDB 仓库由末尾附近的 `tee /etc/yum.repos.d/documentdb.repo` 行写入，因此提前停止会导致 `dnf download` 无法找到任何内容。然后：

```bash {tab="Debian / Ubuntu" group="documentdb-offline-os" value="deb"}
# Debian / Ubuntu
sudo apt-get install -y dpkg-dev
mapfile -t PKGS < <(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances documentdb-18 \
  | grep '^[a-zA-Z0-9]' | sort -u)
mkdir -p bundle && cd bundle
apt-get download "${PKGS[@]}"
dpkg-scanpackages . /dev/null > Packages && gzip -k Packages
```

```bash {tab="EL / RHEL" value="rpm"}
# RHEL-compatible
sudo dnf install -y dnf-plugins-core createrepo_c
mkdir -p bundle
sudo dnf download --resolve --alldeps --destdir bundle documentdb-18
createrepo_c bundle
```

> [!NOTE]
> **请使用下载完整依赖集合的选项，不要只用 `--download-only`。** `apt-get install --download-only` 和未添加其他选项的 `dnf download --resolve` 会跳过准备机器上已经安装的软件包。这样得到的包看似完整，但在目标机上会报错 `Depends: adduser but it is not installable`。

预计 DEB 需要约 200 个软件包、200 MB，RPM 需要约 270 个软件包、170 MB，主要是 PostGIS 和 GDAL。由于包含了准备机器上已有的软件包，这比在线安装的下载量更大。`unsandboxed as root` 和 `dpkg-scanpackages ... override file` 警告可以忽略。

## 从打包文件安装（隔离目标主机） {#install-from-the-bundle-air-gapped-target}

将 `bundle/` 复制到目标机，务必包含其中的 `Packages`/`Packages.gz` 或 `repodata/` 索引，后续步骤依靠它们解析依赖。然后让软件包管理器使用这个目录：

```bash {tab="Debian / Ubuntu" group="documentdb-offline-os" value="deb"}
# Debian / Ubuntu
echo "deb [trusted=yes] file:///path/to/bundle ./" \
  | sudo tee /etc/apt/sources.list.d/documentdb-offline.list
sudo apt-get update
sudo apt install -y documentdb-18
```

```bash {tab="EL / RHEL" value="rpm"}
# RHEL-compatible
printf '%s\n' '[documentdb-offline]' 'name=DocumentDB offline bundle' \
  'baseurl=file:///path/to/bundle' 'enabled=1' 'gpgcheck=0' \
  | sudo tee /etc/yum.repos.d/documentdb-offline.repo
sudo dnf install -y --disablerepo='*' --enablerepo=documentdb-offline documentdb-18
```

> [!IMPORTANT]
> `--disablerepo`/`--enablerepo` 这对组合不可省略。如果任何启用的仓库不可达，DNF **会中止整个事务**，而每个 RHEL 兼容镜像都默认启用了 `baseos`、`appstream` 和 `extras` —— 因此若缺少这对组合，即使你的打包文件完全正确，安装也会因 `Error: Failed to download metadata for repo 'baseos'` 失败。APT 在此行为上有所不同：它仅对不可达源发出警告并继续执行。

`[trusted=yes]` / `gpgcheck=0` 允许使用未签名的本地目录。上游签名已在准备阶段验证；若传输经过不可信的环境，请用 `sha256sum` 核验传输前后文件是否一致。

接着按[配置并连接](/documentdb/getting-started/packages/#set-up-and-connect)操作，`documentdb-setup` 不需要联网。

`mongosh` 并非打包文件的一部分，且目标主机无法访问 MongoDB 仓库，因此若希望从隔离主机进行验证，请在同一阶段准备 `mongodb-mongosh`：在快速入门中所示的 MongoDB 仓库配置完成后，将其添加到包列表中。否则，请使用 `sudo documentdb-setup --status` 进行验证，并从具备 `mongosh` 的机器上完成连接。

## 更小规模的离线场景 {#smaller-offline-cases}

如果目标主机已安装 PostgreSQL、PGDG 扩展依赖（`postgresql-N-cron`、`-pgvector`、`-postgis-3`）以及 `jq`，则无需打包文件：

- **只安装扩展，只需一个文件**：`sudo apt install ./ubuntu24.04-postgresql-18-documentdb_1.0-0_amd64.deb`。不包含网关，也不运行 `documentdb-setup`。
- **使用发布文件安装全套组件**：将所选 PostgreSQL 主版本的五个软件包交给*同一次* `apt install` / `dnf install` 命令：`documentdb-N`、对应的 `postgresql-N-documentdb` / `postgresqlN-documentdb` 扩展、`documentdb-common`、`documentdb-gateway` 和 `documentdb-postgresql-tools`。仅使用 PostgreSQL 18 时，还可以加入可选的 `documentdb` 元软件包，它会选择 `documentdb-18`。本地文件安装时只会从已启用的仓库解析依赖，因此缺少依赖的软件包仍会安装失败。
