---
title: "pxf"
description: "pxf 工具参考。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/ref/pxf.md"
---

管理本地 Apache Cloudberry 主机上的 PXF 配置和 PXF Service 实例。

## 概要 {#synopsis}

```text
pxf <command> [<option>]
```

其中 \<command\> 为：

```text
cluster
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
version
```

## 说明 {#description}

`pxf` 工具管理本地 Apache Cloudberry 主机上的 PXF 配置和 PXF Service 实例。使用该工具可以：

- 将 PXF 配置从 Coordinator 主机同步到 Standby Coordinator 主机或某台 Segment 主机。
- 启动、停止或重启 Coordinator 主机、Standby Coordinator 主机或某台特定 Segment 主机上的 PXF Service 实例，或显示在 Coordinator、Standby Coordinator 或某台 Segment 主机上运行的 PXF Service 实例的状态。
- 在 Apache Cloudberry 升级之后，将 PXF 扩展控制文件从主机上的 PXF 安装目录复制到该主机上的 Apache Cloudberry 安装目录。
- 在主机上准备新的 `$PXF_BASE` 运行时配置目录。

（使用 [`pxf cluster`](/cloudberry/pxf/ref/pxf-cluster/) 命令可以在所有主机上准备新的 `$PXF_BASE`、将 PXF 扩展控制文件复制到所有主机上的 `$GPHOME`、将 PXF 配置同步到 Apache Cloudberry 集群，或者启动、停止集群中所有主机上的 PXF Service 实例，以及显示其状态。）

## 命令 {#commands}

<dt>cluster</dt>
<dd>管理所有 Apache Cloudberry 主机上的 PXF 配置和 PXF Service 实例。参见 `pxf cluster`。</dd>

<dt>help</dt>
<dd>显示 `pxf` 管理工具的帮助信息，然后退出。</dd>

<dt>init (deprecated)</dt>
<dd>该命令等同于 `register` 命令。</dd>

<dt>migrate</dt>
<dd>将旧版 `$PXF_CONF` 目录中的配置迁移到主机上的 `$PXF_BASE`。运行该命令时，必须通过名为 `PXF_CONF` 的环境变量指明旧版配置目录。PXF 会将配置迁移到当前的 `$PXF_BASE`，并根据需要复制、合并文件和目录。<b>注意：</b>必须手动将 `pxf-log4j.properties` 中的所有自定义设置迁移到 `pxf-log4j2.xml` 文件。</dd>

<dt>prepare</dt>
<dd>在主机上准备新的 `$PXF_BASE` 目录。运行该命令时，必须通过名为 `PXF_BASE` 的环境变量指明新的 PXF 运行时配置目录。PXF 会将运行时配置文件模板和目录复制到该 `$PXF_BASE`。</dd>

<dt>register</dt>
<dd>将 PXF 扩展文件从主机上的 PXF 安装目录复制到该主机上的 Apache Cloudberry 安装目录。该命令要求已设置 `$GPHOME`；在首次安装 PXF 6.x 之后运行一次，或在升级 Apache Cloudberry 安装时运行。</dd>

<dt>reset (deprecated)</dt>
<dd>该命令不执行任何操作。</dd>

<dt>restart</dt>
<dd>重启在本地 Coordinator 主机、Standby Coordinator 主机或 Segment 主机上运行的 PXF Service 实例。</dd>

<dt>start</dt>
<dd>启动本地 Coordinator 主机、Standby Coordinator 主机或 Segment 主机上的 PXF Service 实例。</dd>

<dt>status</dt>
<dd>显示在本地 Coordinator 主机、Standby Coordinator 主机或 Segment 主机上运行的 PXF Service 实例的状态。</dd>

<dt>stop  </dt>
<dd>停止在本地 Coordinator 主机、Standby Coordinator 主机或 Segment 主机上运行的 PXF Service 实例。</dd>

<dt>sync  </dt>
<dd>将 PXF 配置（`$PXF_BASE`）从 Coordinator 主机同步到某台特定的 Apache Cloudberry Standby Coordinator 主机或 Segment 主机。必须在 Coordinator 主机上运行 `pxf sync`。默认情况下，该命令会更新远程主机上的文件，并向远程主机复制文件。也可以指示 PXF 在同步期间同时删除文件；参见下文“选项”。</dd>

<dt>version  </dt>
<dd>显示 PXF 版本，然后退出。</dd>

## 选项 {#options}

必须在 Apache Cloudberry Coordinator 主机上运行的 `pxf sync` 命令接受以下选项和参数：

<dt>&#8211;d | &#8211;&#8211;delete </dt>
<dd>删除 <code>&lt;gphost></code> 上 PXF 用户配置中存在、但 Coordinator 主机上不存在的所有文件。如果指定此选项，必须在命令行中将其置于 <code>&lt;gphost></code> 之前。</dd>

<dt>&lt;gphost> </dt>
<dd>要将 PXF 配置同步到的 Apache Cloudberry 主机。必需。<code>&lt;gphost></code> 必须指定 Standby Coordinator 主机或某台 Segment 主机。</dd>

## 示例 {#examples}

在本地 Apache Cloudberry 主机上启动 PXF Service 实例：

```shell
$ pxf start
```

## 另请参阅 {#see-also}

[`pxf cluster`](/cloudberry/pxf/ref/pxf-cluster/)
