---
title: "pg_config"
description: "获取已安装 Apache Cloudberry 版本的信息。"
weight: 330
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-config.md"
---

## 概要 {#synopsis}

```shell
pg_config [<option> ...]

pg_config -? | --help

pg_config --version
```

## 说明 {#description}

`pg_config` 工具打印当前安装的 Apache Cloudberry 版本的配置参数。例如，需要与 Apache Cloudberry 对接的软件包可以使用它来查找所需的头文件和库。注意，`pg_config` 打印的信息仅适用于 Apache Cloudberry Coordinator。

如果给出多个选项，将按给定顺序打印信息，每项一行。如果未给出任何选项，将打印全部可用信息，并附带标签。

## 选项 {#options}

**`--bindir`**

打印用户可执行文件的位置。例如，可用它查找 `psql` 程序。通常这也是 `pg_config` 程序所在的位置。

**`--docdir`**

打印文档文件的位置。

**`--includedir`**

打印客户端接口 C 头文件的位置。

**`--pkgincludedir`**

打印其他 C 头文件的位置。

**`--includedir-server`**

打印服务器编程所用 C 头文件的位置。

**`--libdir`**

打印目标代码库的位置。

**`--pkglibdir`**

打印可动态加载模块的位置，也就是服务器搜索这些模块的位置。（其他依赖体系结构的数据文件也可能安装在此目录中。）

**`--localedir`**

打印区域设置支持文件的位置。

**`--mandir`**

打印手册页的位置。

**`--sharedir`**

打印与体系结构无关的支持文件的位置。

**`--sysconfdir`**

打印系统级配置文件的位置。

**`--pgxs`**

打印扩展 makefile 的位置。

**`--configure`**

打印配置 Apache Cloudberry 构建时传给 configure 脚本的选项。

**`--cc`**

打印构建 Apache Cloudberry 时使用的 CC 变量值。该值表明所用的 C 编译器。

**`--cppflags`**

打印构建 Apache Cloudberry 时使用的 `CPPFLAGS` 变量值。该值表明预处理阶段所需的 C 编译器开关。

**`--cflags`**

打印构建 Apache Cloudberry 时使用的 `CFLAGS` 变量值。该值表明 C 编译器开关。

**`--cflags_sl`**

打印构建 Apache Cloudberry 时使用的 `CFLAGS_SL` 变量值。该值表明构建共享库时所用的额外 C 编译器开关。

**`--ldflags`**

打印构建 Apache Cloudberry 时使用的 `LDFLAGS` 变量值。该值表明链接器开关。

**`--ldflags_ex`**

打印构建 Apache Cloudberry 时使用的 `LDFLAGS_EX` 变量值。该值表明仅在构建可执行文件时使用的链接器开关。

**`--ldflags_sl`**

打印构建 Apache Cloudberry 时使用的 `LDFLAGS_SL` 变量值。该值表明仅在构建共享库时使用的链接器开关。

**`--libs`**

打印构建 Apache Cloudberry 时使用的 `LIBS` 变量值。该值通常包含用于链接到 Apache Cloudberry 的外部库的 `-l` 开关。

**`--version`**

打印 Apache Cloudberry 的版本。

## 示例 {#examples}

要重现当前 Apache Cloudberry 安装的构建配置，请运行以下命令：

```shell
eval ./configure 'pg_config --configure'
```

`pg_config --configure` 的输出包含 shell 引号，以便正确表示含空格的参数。因此，必须使用 `eval` 才能得到正确结果。
