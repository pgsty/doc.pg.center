---
title: 站点维护
description: 构建、预览、校验与更新本社区文档站的方法。
weight: 30
icon: fa-solid fa-wrench
upstream_source: polardb
upstream_link: https://github.com/polardb/polardb-pg-docs/tree/b4733b0350888242afeba432a6837458c348a937
type: docs
---


PG.CENTER 使用 [Hugo Extended](https://gohugo.io/) 0.168.0 和固定的 [OINK v1.5.1](https://github.com/pgsty/oink/tree/v1.5.1) 模块构建，Go 1.27.3 用于解析主题依赖。

## 本地预览 {#preview}

```bash
make serve
```

默认地址为 `http://localhost:1313/`。首页内容在 `data/home/`，导航配置在 `hugo.yaml`，PolarDB 文档在 `content/polardb/`。英文是默认语言，中文页面使用 `.zh.md` 后缀；公开路径分别是 `/polardb/` 与 `/zh/polardb/`。

## 构建与校验 {#build}

```bash
make check
make build
```

检查命令使用临时目录构建，验证站内链接、图片、锚点和输出。生产构建写入 `public/`，可由静态网站服务发布。

## 更新上游 {#upstream}

`data/upstreams.yaml` 记录上游版本，`data/imports/polardb.json` 记录导入来源。`content/polardb/` 中的 Markdown 是持续维护的正文。更新时先检查上游变更与语言覆盖，再应用相应差异并运行校验；一次性导入脚本会拒绝覆盖已维护的内容。原始下载保存在站点目录之外。

数据库问题与原始文档修改请反馈给[上游项目](https://github.com/polardb/polardb-pg-docs)。[贡献文档](/zh/polardb/contributing/contributing-polardb-docs/)介绍的是上游 VuePress 工程流程。
