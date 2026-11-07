---
title: 安装 AgensGraph
linkTitle: 安装 AgensGraph
description: 通过 Docker、软件包或源码安装 AgensGraph 2.18.6.1，并验证图功能已经可用。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/install.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


有三种途径。Docker 是得到一个可查询服务端的最快方式。软件包是工作站或单个服务器的常用选择。如果需要修改某些内容，或者你的平台没有软件包，就从源码构建。

如果只是想试用 AgensGraph，请使用 Docker，然后直接进入[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

## Docker {#docker}

```shell
docker run --name agensgraph -e POSTGRES_PASSWORD=agensgraph -d skaiworldwide/agensgraph:v2.18.6.1-bookworm
```

然后在容器内打开客户端：

```shell
docker exec -it agensgraph agens -U agens -d postgres
```

这个镜像接受与官方 `postgres` 镜像相同的环境变量——`POSTGRES_USER`、`POSTGRES_DB`、`PGDATA` 及其余变量——因此可以按通常方式发布端口并挂载数据卷：

```shell
docker run -d --name agensgraph \
  -e POSTGRES_PASSWORD=agensgraph \
  -p 5432:5432 \
  -v agensgraph-data:/var/lib/postgresql \
  skaiworldwide/agensgraph:v2.18.6.1-bookworm
```

标签由发布版本加基础镜像组成：`v2.18.6.1-trixie`、`v2.18.6.1-bookworm`、`v2.18.6.1-rocky10`、`v2.18.6.1-rocky9`、`v2.18.6.1-alpine3.24`、`v2.18.6.1-alpine3.23`。请固定其中一个；单独使用 `skaiworldwide/agensgraph` 是一个不断移动的目标。

> [!WARNING]
> 2.18.6.1 镜像遵循 PostgreSQL 18 的目录布局变化。`PGDATA` 现在默认为 `/var/lib/postgresql/18/docker`，声明的数据卷也从 `/var/lib/postgresql/data` 移到了 `/var/lib/postgresql`。较早标签初始化过的宿主机数据卷不会被 2.18.6.1 容器自动找到，除非显式指向它：
>
>     -e PGDATA=/var/lib/postgresql/data -v /custom/mount:/var/lib/postgresql/data
>
> 任何情况下，重用既有数据目录前都要阅读[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)——2.17 的数据目录不能由 2.18 启动。

## 软件包 {#packages}

从 [AgensGraph 下载页](https://tech.skaiworldwide.com/downloads/)下载适合平台的构建，并解压到任意目标位置，例如 `/usr/local/AgensGraph`：

```shell
tar xvf agensgraph-v2.18.6.1-build.tar.gz -C /usr/local
```

如果不确定需要哪个构建，请运行：

```shell
uname -sm
```

然后继续[设置数据库](#set-up-a-database)。

## 源码构建 {#build-from-source}

### 安装构建依赖 {#install-the-build-dependencies}

{{< tabs >}}
{{< tab label="Ubuntu / Debian" >}}
```shell
sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison
```
{{< /tab >}}
{{< tab label="Rocky / RHEL" >}}
```shell
sudo yum install gcc glibc glib-common readline readline-devel zlib zlib-devel flex bison perl
```
{{< /tab >}}
{{< tab label="Fedora" >}}
```shell
sudo dnf install gcc glibc bison flex readline readline-devel zlib zlib-devel
```
{{< /tab >}}
{{< tab label="macOS" >}}
```shell
xcode-select --install
```
{{< /tab >}}
{{< /tabs >}}

### 构建并安装 {#build-and-install}

```shell
git clone https://github.com/skaiworldwide-oss/agensgraph.git
cd agensgraph
./configure --prefix=$(pwd)
make install
```

`--prefix` 决定二进制文件的位置。不指定时，`make install` 会写入 `/usr/local/pgsql`。如上例所示，将它指向源码树可以在试用期间把所有内容保存在同一处。

要同时构建 contrib 模块——`pgvector` 不在其中，但[加载指南](/zh/agensgraph/guides/loading-data/)使用的 `file_fdw` 在其中——请运行：

```shell
make install-world
```

如果 `configure` 找不到所需头文件，用 `--with-includes=/path/to/headers` 告诉它到哪里查找。`./configure --help` 会列出所有选项；这些选项属于 PostgreSQL，[PostgreSQL 的安装章节](https://www.postgresql.org/docs/18/installation.html)有详细说明。

### 把二进制文件加入 PATH {#put-the-binaries-on-your-path}

```shell
export PATH=/path/to/agensgraph/bin:$PATH
export LD_LIBRARY_PATH=/path/to/agensgraph/lib:$LD_LIBRARY_PATH
```

把它们加入 `~/.bashrc`；在 macOS 上则加入 `~/.zshrc`，使设置长期生效。

## 设置数据库 {#set-up-a-database}

这些工具来自 PostgreSQL，只有两个改名：`agens` 是交互式客户端，`ag_ctl` 启动和停止服务端。参见 [agens 客户端](/zh/agensgraph/reference/agens/)。

创建数据目录：

```shell
initdb -D /path/to/data
```

启动服务端：

```shell
ag_ctl -D /path/to/data -l /path/to/data/server.log start
```

创建数据库：

```shell
createdb mydb
```

设置 `AGDATA` 后，后续命令可以省略 `-D`：

```shell
export AGDATA=/path/to/data
```

## 验证安装 {#verify-the-install}

连接：

```shell
agens mydb
```

询问服务端自己是什么：

```sql
SELECT version();
```

```
                                        version
-------------------------------------------------------------------------------------
 PostgreSQL 18.6 (AgensGraph 2.18.6.1) on x86_64-pc-linux-gnu, compiled by gcc ...
```

然后检查图这一半是否存在。普通 PostgreSQL 构建会在这一步失败：

```psql
CREATE GRAPH check_install;
SET graph_path = check_install;
CREATE (:t {ok: true});
MATCH (n:t) RETURN n;
```

```
         n
--------------------
 t[3.1]{"ok": true}
```

```sql
DROP GRAPH check_install CASCADE;
```

`CASCADE` 是必要的，因为图会拥有其中的标签和序列。

## 下一步 {#next}

[加载示例数据集](/zh/agensgraph/get-started/example-dataset/)——本手册每一页都使用它——然后[运行你的第一个查询](/zh/agensgraph/get-started/first-query/)。

生产安装中数据目录放在哪里、`postgresql.conf` 该设置什么、如何用 systemd 运行以及如何锁定安全边界，参见[部署](/zh/agensgraph/operations/deployment/)与[配置](/zh/agensgraph/operations/configuration/)。
