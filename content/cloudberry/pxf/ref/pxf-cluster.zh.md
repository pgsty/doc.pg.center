---
title: "pxf cluster"
description: "pxf cluster 工具参考。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/ref/pxf-cluster.md"
---

管理所有 Apache Cloudberry 主机上的 PXF 配置和 PXF Service 实例。

## 概要 {#synopsis}

```text
pxf cluster <command> [<option>]
```

其中 `<command>` 为：

```text
help
init (deprecated)
migrate
prepare
register
reset (deprecated)
restart
start
status
stop
sync
```

## 说明 {#description}

`pxf cluster` 工具命令管理 Coordinator 主机、Standby Coordinator 主机以及所有 Apache Cloudberry Segment 主机上的 PXF。使用该工具可以：

- 启动、停止和重启 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上的 PXF Service 实例。
- 显示 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上 PXF Service 实例的状态。
- 将 PXF 配置从 Apache Cloudberry Coordinator 主机同步到 Standby Coordinator 以及所有 Segment 主机。
- 在 Apache Cloudberry 升级之后，将 PXF 扩展控制文件从每台主机上的 PXF 安装目录复制到该主机上的 Apache Cloudberry 安装目录。
- 准备新的 `$PXF_BASE` 运行时配置目录。
- 将旧版 `$PXF_CONF` 配置迁移到 `$PXF_BASE`。

`pxf cluster` 需要 Apache Cloudberry 集群处于运行状态。必须在 Apache Cloudberry Coordinator 主机上运行该工具。

如果要管理某台特定 Segment 主机上的 PXF Service 实例，请使用 `pxf` 工具。参见 [`pxf`](/cloudberry/pxf/ref/pxf/)。

## 命令 {#commands}

<dt>help</dt>
<dd>显示 `pxf cluster` 帮助信息，然后退出。</dd>

<dt>init (deprecated)</dt>
<dd>该命令等同于 `register` 命令。</dd>

<dt>migrate</dt>
<dd>将旧版 `$PXF_CONF` 目录中的配置迁移到每台 Apache Cloudberry 主机上的 `$PXF_BASE`。运行该命令时，必须通过名为 `PXF_CONF` 的环境变量指明旧版配置目录。PXF 会将配置迁移到 `$PXF_BASE`，并根据需要复制、合并文件和目录。<b>注意：</b>必须手动将 `pxf-log4j.properties` 中的所有自定义设置迁移到 `pxf-log4j2.xml` 文件。</dd>

<dt>prepare</dt>
<dd>在每台 Apache Cloudberry 主机上准备新的 `$PXF_BASE` 目录。运行该命令时，必须通过名为 `PXF_BASE` 的环境变量指明新的 PXF 运行时配置目录。PXF 会将运行时配置文件模板和目录复制到该 `$PXF_BASE`。</dd>

<dt>register</dt>
<dd>将 PXF 扩展控制文件从每台主机上的 PXF 安装目录复制到该主机上的 Apache Cloudberry 安装目录。该命令要求已设置 `$GPHOME`；在首次安装 PXF 6.x 之后运行一次，或在升级 Apache Cloudberry 安装之后运行。</dd>

<dt>reset (deprecated) </dt>
<dd>该命令不执行任何操作。</dd>

<dt>restart</dt>
<dd>先停止、再启动 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上的 PXF Service 实例。</dd>

<dt>start</dt>
<dd>启动 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上的 PXF Service 实例。</dd>

<dt>status  </dt>
<dd>显示 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上 PXF Service 实例的状态。</dd>

<dt>stop  </dt>
<dd>停止 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上的 PXF Service 实例。</dd>

<dt>sync  </dt>
<dd>将 PXF 配置（`$PXF_BASE`）从 Coordinator 主机同步到 Standby Coordinator 主机以及所有 Apache Cloudberry Segment 主机。默认情况下，该命令会更新远程主机上的文件，并向远程主机复制文件。也可以指示 PXF 在同步期间同时删除文件；参见下文“选项”。</dd>
<dd>如果更新了 PXF 用户配置，或添加了新的 JAR 或本地库依赖，则在同步 PXF 配置之后还必须重启 PXF。</dd>

## 选项 {#options}

`pxf cluster sync` 命令接受以下选项：

<dt>&#8211;d | &#8211;&#8211;delete </dt>
<dd>删除 Standby Coordinator 主机和 Segment 主机上 PXF 用户配置中存在、但 Coordinator 主机上不存在的所有文件。</dd>

## 示例 {#examples}

停止 Coordinator 主机、Standby Coordinator 主机及所有 Segment 主机上的 PXF Service 实例：

```shell
$ pxf cluster stop
```

将 PXF 配置同步到 Standby Coordinator 主机和所有 Segment 主机，并删除 Coordinator 主机上不存在的文件：

```shell
$ pxf cluster sync --delete
```

## 另请参阅 {#see-also}

[`pxf`](/cloudberry/pxf/ref/pxf/)
