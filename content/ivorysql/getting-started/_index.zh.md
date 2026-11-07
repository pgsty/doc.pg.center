---
title: 快速上手
description: 从系统要求和快速安装开始运行 IvorySQL。
type: docs
weight: 20
no_list: true
upstream_source: ivorysql
upstream_link: https://github.com/IvorySQL/ivorysql_docs/tree/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1
---


- [快速开始](/zh/ivorysql/getting-started/quick-start/)
{.cards}

## 获取容器镜像 {#container-images}

国内用户也可使用社区 Harbor 镜像服务。拉取镜像后，继续按快速开始中的步骤运行并连接数据库。

```bash {tab="Docker Hub" group="ivorysql-registry" value="docker-hub"}
docker pull ivorysql/ivorysql:5.6-ubi8
```

```bash {tab="Harbor" value="harbor"}
docker pull registry.highgo.com/ivorysql/ivorysql:5.6-ubi8
```
