---
title: "LOAD"
description: "加载或重新加载共享库文件。"
weight: 1520
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/load.md"
---

## 概要 {#synopsis}

```sql
LOAD '<filename>'
```

## 描述 {#description}

此命令将共享库文件加载到 Apache Cloudberry 服务器的地址空间。如果文件先前已经加载，会先将其卸载。此命令主要用于卸载并重新加载服务器首次加载后发生过变更的共享库文件。要使用该共享库，需要通过 `CREATE FUNCTION` 命令声明其中的函数。

库文件名通常只给出文件名本身，服务器会在库搜索路径（由 `dynamic_library_path` 设置）中查找。也可以给出完整路径。无论哪种形式，都可以省略平台标准的共享库文件扩展名。

注意，在 Apache Cloudberry 中，共享库文件（`.so` 文件）必须位于集群内每台主机（Coordinator、Segment 和镜像）上的相同路径。

非超级用户只能对 `$libdir/plugins/` 中的库文件使用 `LOAD`；指定的 `filename` 必须严格以该字符串开头。必须确保该目录中只安装“安全”的库。

## 参数 {#parameters}

**`filename`**

共享库文件的路径和文件名。此文件必须位于 Apache Cloudberry 集群中所有主机上的相同位置。

## 示例 {#examples}

加载共享库文件：

```sql
LOAD '/usr/local/cloudberry/lib/myfuncs.so';
```

## 兼容性 {#compatibility}

`LOAD` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)
