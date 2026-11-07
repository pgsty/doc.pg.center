---
title: Docker（Mac 或 Linux）
description: 在 Mac 或 Linux 上用 Docker 运行 Citus，快速体验分布式 PostgreSQL。
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/single-node-docker?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

> [!NOTE]
> **此 Docker 镜像仅用于开发和测试**，尚未针对生产环境做好准备。

一条命令即可在 Docker 中启动 Citus：

```bash
# start the image
docker run -d --name citus -p 5432:5432 -e POSTGRES_PASSWORD=mypass \
           citusdata/citus:14.0

# verify it's running, and that Citus is installed:
psql -U postgres -h localhost -d postgres -c "SELECT * FROM citus_version();"
```

你应当看到 Citus 14.x。

集群启动后，可继续阅读多租户应用或实时分析教程，在几分钟内开始使用 Citus。

> [!NOTE]
> 如果本机已经运行 PostgreSQL，启动 Docker 容器时可能遇到以下错误：
>
> ```text
> Error starting userland proxy:
> Bind for 0.0.0.0:5432: unexpected error address already in use
> ```
>
> 这是因为 Citus 镜像尝试绑定 PostgreSQL 的默认端口 5432。使用 `-p` 选项指定其他端口即可解决；`psql` 命令也需要使用这个新端口。

## 相关内容 {#related-content}

- [单节点概览](/citus/installation/single-node/)
- [Ubuntu 或 Debian 单节点安装](/citus/installation/single-node-debian/)
- [CentOS 或 Red Hat 单节点安装](/citus/installation/single-node-rhel/)
