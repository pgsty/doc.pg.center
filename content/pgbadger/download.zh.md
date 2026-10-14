---
title: "下载与安装"
linkTitle: "下载与安装"
weight: 20
description: "官方发布、系统软件包、运行要求与源码安装方法"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [教程]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## 选择分发渠道 {#distribution-channels}

| 渠道 | 适用场景 | 地址 |
|---|---|---|
| 官方发布 | 源码归档与版本说明 | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPM 软件包 | 基于 RPM 的 Linux 发行版 | [PostgreSQL Yum 仓库](https://yum.postgresql.org/packages/) |
| Debian/Ubuntu 软件包 | 基于 APT 的 Linux 发行版 | [PostgreSQL Apt 仓库](https://wiki.postgresql.org/wiki/Apt) |
| 开发源码 | 尚未正式发布的最新代码 | [darold/pgbadger](https://github.com/darold/pgbadger) |

安装示例使用 pgBadger 13.2。下载前请查看发布页面，选择所需版本。

## 运行要求 {#requirements}

生成与查看 HTML 报告只需要：

- 一套现代 Perl 发行版；
- 一个可运行内嵌 JavaScript 图表的浏览器。

下列可选功能需要额外依赖：

| 功能 | 依赖 |
|---|---|
| 解析 PostgreSQL CSV 日志 | `Text::CSV_XS` |
| 生成 JSON 输出 | `JSON::XS` |
| 读取 `.gz`、`.bz2`、`.lz4`、`.xz`、`.zip` 或 `.zst` 输入 | 对应的 `zcat`、`bzcat`、`lz4cat`、`xz`、`unzip` 或 `zstdcat` 工具 |

在 Debian 或 Ubuntu 上安装 JSON 支持：

```console
$ sudo apt-get install libjson-xs-perl
```

在基于 RPM 的系统上：

```console
$ sudo yum install perl-JSON-XS
```

可通过 `--zcat` 指定解压程序路径。显式指定一个自定义命令后，同一次调用将不能再混合处理多种压缩格式。

`xz` 工具必须支持 `--robot`，以便 pgBadger 读取归档元数据。压缩 lz4 日志时请使用 `--content-size`，使 pgBadger 能确定解压后的文件大小。

## 从官方归档安装 {#install-from-tarball}

下载版本归档后，使用 Perl 的标准工具链构建并安装：

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
$ perl Makefile.PL
$ make
$ sudo make install
```

默认的 `site` 布局会把程序安装为 `/usr/local/bin/pgbadger`，把手册页安装为 `/usr/local/share/man/man1/pgbadger.1`。

若要按 Linux 发行版惯例安装到 `/usr`，可这样生成 Makefile：

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

上游也支持 `INSTALLDIRS=perl` 布局。向受包管理器管理的系统安装前，应先检查生成的目标路径。

## 安装开发版源码 {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

开发分支可能包含尚未进入正式版本说明的改动。生产打包应优先使用带标签的发布归档，以保证可复现性。

## 验证安装 {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

接下来请阅读[命令行参考](/zh/pgbadger/command-line/)与 [PostgreSQL 日志配置](/zh/pgbadger/postgresql-logging/)。
